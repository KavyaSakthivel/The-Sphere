// One-off event page: retire booking once the evening is over, run the phone booking bar,
// and mark the section being read in the sticky contents row.
const eventEnd = Date.parse(document.querySelector('main.event')?.dataset.eventEnd || '');
if (Date.now() > eventEnd) document.body.classList.add('is-past');

// Phones get a slim price-and-tickets bar once the opening and the at-a-glance band have scrolled
// away; it steps aside while the ticket section or the closing call to action is on screen.
const bar = document.querySelector('[data-event-bar]');
const phone = window.matchMedia('(max-width: 700px)');
if (bar && !document.body.classList.contains('is-past')) {
  const link = bar.querySelector('a');
  const inView = new Set();
  const update = () => {
    const show = phone.matches && inView.size === 0 && window.scrollY > 200;
    bar.classList.toggle('is-visible', show);
    bar.setAttribute('aria-hidden', String(!show));
    if (link) link.tabIndex = show ? 0 : -1;
    document.body.classList.toggle('has-event-dock', show);
  };
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? inView.add(entry.target) : inView.delete(entry.target));
      update();
    });
    ['.event-cinematic', '.cv-glance', '#tickets', '.cv-close', 'footer']
      .map(selector => document.querySelector(selector))
      .filter(Boolean)
      .forEach(el => observer.observe(el));
  }
  window.addEventListener('scroll', update, { passive: true });
  phone.addEventListener('change', update);
  update();
}

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

// Booking through The Sphere's own API (data/event.json booking_api): the guest picks a ticket count,
// the server creates that booking's own Razorpay link, and the guest pays there. Every button keeps the
// shared Razorpay link as its href, so without JavaScript, or whenever the API fails, booking still works.
(() => {
  const dialog = document.querySelector('[data-booking-dialog]');
  if (!dialog || typeof dialog.showModal !== 'function' || document.body.classList.contains('is-past')) return;
  const params = new URLSearchParams(location.search);
  if (dialog.dataset.mode !== 'on' && params.get('booking') !== 'preview') return;

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
    error.hidden = true;
    let fbclid = null;
    try { fbclid = params.get('fbclid') || sessionStorage.getItem('sphere-fbclid'); } catch {}
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const res = await fetch('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ quantity, consent: consent.checked, fbclid }),
        signal: controller.signal,
      });
      const data = await res.json().catch(() => ({}));
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
    } finally {
      clearTimeout(timer);
    }
    error.hidden = false;
    busy(false);
  });
})();
