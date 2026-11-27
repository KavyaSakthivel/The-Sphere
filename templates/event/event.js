// One-off event page: retire booking once the evening is over, run the phone booking bar,
// and mark the section being read in the sticky contents row.
const eventEnd = Date.parse(document.querySelector('main.event')?.dataset.eventEnd || '');
if (Date.now() > eventEnd) document.body.classList.add('is-past');

// The phone booking bar (Reserve Your Spot and the price) stays on screen from top to bottom; the stylesheet
// shows it on phones and the is-past rule above hides it once the evening is over.

// The contents row underlines the section being read, including after anchor jumps.
(() => {
  const links = [...document.querySelectorAll('.cv-jump a')];
  const sections = links.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
  let frame = 0;
  const update = () => {
    frame = 0;
    const line = Math.min(innerHeight * .35, 260);
    const active = sections.filter(section => section.getBoundingClientRect().top <= line).at(-1);
    links.forEach(link => {
      if (active && link.hash === '#' + active.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  update();
})();

// Booking (data/event.json booking_api): the guest picks a ticket count. In 'page' mode the page then sends
// them to the club's Razorpay Payment Page with that count filled in. In 'on' mode The Sphere's own API
// creates that booking's own Razorpay link, and the guest pays there. Every button keeps the
// shared Razorpay link as its href, so without JavaScript, or whenever the API fails, booking still works.
(() => {
  const dialog = document.querySelector('[data-booking-dialog]');
  if (!dialog || typeof dialog.showModal !== 'function' || document.body.classList.contains('is-past')) return;
  const params = new URLSearchParams(location.search);
  const mode = dialog.dataset.mode;
  if (mode !== 'on' && mode !== 'page' && params.get('booking') !== 'preview') return;

  const price = Number(dialog.dataset.price);
  const max = Math.max(1, Number(dialog.dataset.max) || 1);
  const form = dialog.querySelector('form');
  const out = dialog.querySelector('[data-qty-value]');
  const total = dialog.querySelector('[data-booking-total]');
  const submit = dialog.querySelector('[data-booking-submit]');
  const error = dialog.querySelector('[data-booking-error]');
  const fallback = dialog.querySelector('[data-booking-fallback]');
  const consent = dialog.querySelector('[data-booking-consent]');
  const [fewer, more] = dialog.querySelectorAll('[data-qty]');
  const rupees = n => '₹' + n.toLocaleString('en-IN');
  // A Meta ad click id, kept for the visit in case the guest wanders before booking.
  try { if (params.get('fbclid')) sessionStorage.setItem('sphere-fbclid', params.get('fbclid')); } catch {}
  let quantity = 1;

  // One retry key per selection (ticket count and consent answer). Pressing Continue again, or reloading
  // after an answer was lost, repeats the same request, and the server returns the same booking and link
  // instead of making a second one. A different selection is a different booking, so it gets a new key.
  const KEY_STORE = 'sphere-booking-attempt';
  const newKey = () => (crypto.randomUUID ? crypto.randomUUID()
    : Array.from(crypto.getRandomValues(new Uint8Array(16)), b => b.toString(16).padStart(2, '0')).join(''));
  let attempt = null;
  try { attempt = JSON.parse(sessionStorage.getItem(KEY_STORE) || 'null'); } catch {}
  const keyFor = (q, c) => {
    if (!attempt || attempt.quantity !== q || attempt.consent !== c || typeof attempt.key !== 'string') {
      attempt = { key: newKey(), quantity: q, consent: c };
      try { sessionStorage.setItem(KEY_STORE, JSON.stringify(attempt)); } catch {}
    }
    return attempt.key;
  };
  const forgetKey = () => { attempt = null; try { sessionStorage.removeItem(KEY_STORE); } catch {} };

  const render = () => {
    out.value = out.textContent = String(quantity);
    total.textContent = rupees(price * quantity);
    fewer.disabled = quantity <= 1;
    more.disabled = quantity >= max;
  };
  const busy = on => { submit.disabled = on; submit.setAttribute('aria-busy', String(on)); };

  document.addEventListener('click', e => {
    const link = e.target.closest('a[data-booking]');
    if (!link || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    error.hidden = true;
    busy(false);
    render();
    dialog.showModal();
  });
  dialog.querySelectorAll('[data-qty]').forEach(button => button.addEventListener('click', () => {
    quantity = Math.min(max, Math.max(1, quantity + Number(button.dataset.qty)));
    render();
  }));
  dialog.querySelector('[data-booking-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (submit.disabled) return;
    busy(true);
    // Payment Page mode: straight to the club's Razorpay page with the ticket count filled in. Razorpay
    // asks for name, email and phone there. Only ever leave for Razorpay.
    if (mode === 'page') {
      try {
        const target = new URL(dialog.dataset.page);
        if (target.protocol === 'https:' && /(^|\.)razorpay\.com$/.test(target.hostname)) {
          target.searchParams.set(dialog.dataset.pageQty, String(quantity));
          location.assign(target.href);
          return;
        }
      } catch {}
      location.assign(dialog.dataset.fallback);
      return;
    }
    error.hidden = true;
    let fbclid = null;
    try { fbclid = params.get('fbclid') || sessionStorage.getItem('sphere-fbclid'); } catch {}
    const post = async requestKey => {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 15000);
      try {
        const res = await fetch('/api/bookings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify({ quantity, consent: consent.checked, fbclid, requestKey }),
          signal: controller.signal,
        });
        return { res, data: await res.json().catch(() => ({})) };
      } finally {
        clearTimeout(timer);
      }
    };
    try {
      let { res, data } = await post(keyFor(quantity, consent.checked));
      // That key's booking is paid, closed or about to expire: this is a new booking, with a new key.
      if (data.error === 'request_key_used' || data.error === 'request_key_mismatch') {
        forgetKey();
        ({ res, data } = await post(keyFor(quantity, consent.checked)));
      }
      const target = res.ok && data.url ? new URL(data.url) : null;
      // Only ever leave for Razorpay.
      if (target && target.protocol === 'https:' && /(^|\.)(rzp\.io|razorpay\.com)$/.test(target.hostname)) {
        location.assign(target.href);
        return;
      }
      // Sold out on the website: the shared link would oversell, so it is not offered.
      fallback.hidden = data.error === 'sold_out' || data.error === 'event_over';
    } catch {
      fallback.hidden = false;
    }
    error.hidden = false;
    busy(false);
  });

  // Coming back from Razorpay with the browser's back button restores this page as it was left, with
  // Continue still marked busy. Let the guest use it again; the same selection returns the same link.
  window.addEventListener('pageshow', e => { if (e.persisted) busy(false); });
})();

// The glow cursor: a warm orb that trails a short, fading line of light behind the pointer, with a sharp dot
// exactly on the pointer so clicks stay precise. Mouse and trackpad only; touch screens, keyboard use and
// visitors who prefer reduced motion keep their normal cursor. It also steps aside while a dialog is open,
// because dialogs sit above everything else on the page and would hide it.
(() => {
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  if (!fine.matches || still.matches || !document.body.classList.contains('event-page')) return;

  const root = document.documentElement;
  const canvas = document.createElement('canvas');
  canvas.className = 'glow-cursor-trail';
  canvas.setAttribute('aria-hidden', 'true');
  const dot = document.createElement('div');
  dot.className = 'glow-cursor-dot';
  dot.setAttribute('aria-hidden', 'true');
  document.body.append(canvas, dot);
  const ctx = canvas.getContext('2d');

  const LIFE = 650;          // how long a point of the trail glows, in ms
  const points = [];          // {x, y, t}
  const head = { x: -100, y: -100 };
  const pointer = { x: -100, y: -100 };
  let ratio = 1, frame = 0, inside = false, hot = 0, hotTarget = 0;

  const size = () => {
    ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = innerWidth * ratio;
    canvas.height = innerHeight * ratio;
  };
  size();
  addEventListener('resize', size, { passive: true });

  const dialogOpen = () => !!document.querySelector('dialog[open]');
  const setOn = on => {
    root.classList.toggle('has-glow-cursor', on);
    root.classList.toggle('glow-cursor-on', on);
    if (!on) { points.length = 0; ctx.clearRect(0, 0, canvas.width, canvas.height); }
  };

  const glow = (x, y, r, alpha) => {
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, `rgba(255, 228, 170, ${alpha})`);
    g.addColorStop(0.35, `rgba(246, 168, 74, ${alpha * 0.7})`);
    g.addColorStop(0.7, `rgba(217, 87, 43, ${alpha * 0.25})`);
    g.addColorStop(1, 'rgba(217, 87, 43, 0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  };

  const draw = now => {
    frame = 0;
    // The orb eases towards the pointer, which gives the trail its soft, slightly lagging sweep.
    head.x += (pointer.x - head.x) * 0.32;
    head.y += (pointer.y - head.y) * 0.32;
    hot += (hotTarget - hot) * 0.18;
    points.push({ x: head.x, y: head.y, t: now });
    while (points.length && now - points[0].t > LIFE) points.shift();

    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    for (const p of points) {
      const life = 1 - (now - p.t) / LIFE;       // 1 for the newest point, 0 for the oldest
      glow(p.x, p.y, 6 + 20 * life, 0.3 * Math.pow(life, 1.5));
    }
    // The orb itself, which swells a little over links and buttons.
    glow(head.x, head.y, 30 + 16 * hot, 0.7 + 0.2 * hot);
    ctx.strokeStyle = `rgba(143, 43, 29, ${0.35 + 0.3 * hot})`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(head.x, head.y, 11 + 9 * hot, 0, Math.PI * 2);
    ctx.stroke();

    const settled = Math.abs(pointer.x - head.x) < 0.3 && Math.abs(pointer.y - head.y) < 0.3 && Math.abs(hotTarget - hot) < 0.01;
    // Keep animating until the trail has faded and the orb has come to rest; then sleep until the next move.
    if (inside && (!settled || points.length > 1)) frame = requestAnimationFrame(draw);
    else if (!inside) { points.length = 0; ctx.clearRect(0, 0, innerWidth, innerHeight); }
  };
  const wake = () => { if (!frame) frame = requestAnimationFrame(draw); };

  document.addEventListener('pointermove', e => {
    if (e.pointerType !== 'mouse') return;
    if (dialogOpen()) { setOn(false); return; }
    if (!inside) { head.x = e.clientX; head.y = e.clientY; inside = true; }
    setOn(true);
    pointer.x = e.clientX; pointer.y = e.clientY;
    dot.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
    const t = e.target instanceof Element ? e.target : null;
    hotTarget = t && t.closest('a, button, summary, label, [role="button"]') ? 1 : 0;
    // Over a text field the normal text cursor takes over.
    root.classList.toggle('glow-cursor-on', !(t && t.closest('input:not([type=checkbox]):not([type=radio]), textarea, select')));
    wake();
  }, { passive: true });
  document.addEventListener('pointerleave', () => { inside = false; root.classList.remove('glow-cursor-on'); wake(); });
  document.documentElement.addEventListener('mouseleave', () => { inside = false; root.classList.remove('glow-cursor-on'); wake(); });
  // Opening a dialog (booking, invitation) brings the normal cursor back at once.
  document.addEventListener('click', () => setTimeout(() => { if (dialogOpen()) setOn(false); }, 0), true);
  still.addEventListener?.('change', e => { if (e.matches) { setOn(false); canvas.remove(); dot.remove(); } });
})();
