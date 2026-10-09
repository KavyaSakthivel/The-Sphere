const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
const header = document.querySelector('.header');
const updateHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 48);
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });
new ResizeObserver(() => {
  document.documentElement.style.setProperty('--navigation-height', `${header.getBoundingClientRect().height}px`);
}).observe(header);
// An open menu needs an opaque header; otherwise the panel floats over the photograph.
const syncNavState = () => header.classList.toggle('is-nav-open', !mobileNav.hidden);
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  mobileNav.hidden = expanded;
  menuButton.querySelector('span').textContent = expanded ? '☰' : '×';
  syncNavState();
});
mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  mobileNav.hidden = true;
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.querySelector('span').textContent = '☰';
  syncNavState();
}));
document.querySelectorAll('dialog').forEach(dialog => {
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
});
const invitationDialog = document.querySelector('#invitation-dialog');
let invitationTrigger;
document.querySelectorAll('[data-invitation]').forEach(trigger => {
  trigger.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (!invitationDialog || typeof invitationDialog.showModal !== 'function') return;
    event.preventDefault();
    invitationTrigger = trigger.closest('#mobile-nav') ? menuButton : trigger;
    invitationDialog.showModal();
  });
});
invitationDialog?.addEventListener('close', () => invitationTrigger?.focus({ preventScroll: true }));
const entries = JSON.parse(document.querySelector('#journal-data')?.textContent || '[]');
let articleTrigger;
document.querySelector('#article-dialog')?.addEventListener('close', () => articleTrigger?.focus({ preventScroll: true }));
document.querySelectorAll('[data-entry]').forEach(button => {
  button.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    const dialog = document.querySelector('#article-dialog');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    articleTrigger = button;
    const entry = entries[Number(button.dataset.entry)];
    document.querySelector('#article-title').textContent = entry.title;
    const body = document.querySelector('#article-body');
    body.replaceChildren(...entry.paragraphs.map(text => {const p = document.createElement('p'); p.textContent = text; return p;}));
    document.querySelector('#article-dialog').showModal();
  });
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !mobileNav.hidden) {
    mobileNav.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.querySelector('span').textContent = '☰';
    syncNavState();
    menuButton.focus();
  }
});
// Event mentions take themselves down once the event has ended, even before the site is rebuilt.
document.querySelectorAll('[data-event-until]').forEach(el => { if (Date.now() > Date.parse(el.dataset.eventUntil)) el.remove(); });
document.querySelector('#year').textContent = new Date().getFullYear();

const formCopy = {
  enquiry: {
    heading: 'Thank you — your note is with us.',
    body: 'One of us will reply personally within two days. A confirmation is on its way to your inbox; if it is not there, look in promotions or spam.'
  },
  inbox: {
    heading: 'You are on the list.',
    body: 'A short confirmation is on its way to your inbox. You will hear from us only when there is something worth pausing for.'
  }
};
document.querySelectorAll('form[data-sphere-form]').forEach(form => {
  const kind = form.dataset.sphereForm;
  const status = form.querySelector('.form-status');
  const button = form.querySelector('button[type="submit"]');
  const buttonMarkup = button.innerHTML;
  const succeed = () => {
    const note = document.createElement('div');
    note.className = 'form-success';
    const heading = document.createElement('strong');
    heading.textContent = formCopy[kind].heading;
    const body = document.createElement('p');
    body.textContent = formCopy[kind].body;
    note.append(heading, body);
    form.replaceWith(note);
    note.setAttribute('tabindex', '-1');
    note.focus({ preventScroll: true });
  };
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    // A bot that fills the hidden field gets the same reassurance and no delivery.
    if (form.querySelector('[name="_honey"]').value) { succeed(); return; }
    const data = new FormData(form);
    const email = String(data.get('email') || '').trim();
    const name = String(data.get('Name') || '').trim();
    data.set('_replyto', email);
    data.set('_subject', kind === 'enquiry'
      ? `The Sphere — ${name || email} would like to join`
      : `The Sphere — ${email} joined the inbox`);
    data.delete('_next');
    status.textContent = '';
    status.classList.remove('is-error');
    button.disabled = true;
    button.textContent = 'Sending…';
    try {
      const response = await fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' }
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || String(result.success) === 'false') throw new Error(result.message || 'Delivery failed');
      succeed();
    } catch (error) {
      button.disabled = false;
      button.innerHTML = buttonMarkup;
      status.classList.add('is-error');
      status.textContent = 'That did not send. Please try once more, or reach us on Instagram @thespherewomen.';
    }
  });
});

// Upcoming gatherings are read from a published Google Sheet so the club can edit them itself.
// Anything unexpected in the sheet leaves the static copy in place rather than breaking the page.
const gatheringsSection = document.querySelector('#gatherings');
const parseCsv = text => {
  const rows = [];
  let row = [], field = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (quoted) {
      if (char !== '"') { field += char; continue; }
      if (text[i + 1] === '"') { field += '"'; i++; } else quoted = false;
    } else if (char === '"') quoted = true;
    else if (char === ',') { row.push(field); field = ''; }
    else if (char === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (char !== '\r') field += char;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows.filter(r => r.some(cell => cell.trim()));
};
const columnFor = heading => {
  const key = heading.toLowerCase().replace(/[^a-z]/g, '');
  if (key.startsWith('date') || key === 'when') return 'date';
  if (['gathering','title','what','whatisit','name','experience'].includes(key)) return 'title';
  if (['about','description','details','aboutit','oneline'].includes(key)) return 'about';
  if (key.startsWith('time')) return 'time';
  if (['where','venue','place','location'].includes(key)) return 'where';
  if (key.startsWith('show')) return 'show';
  return null;
};
// Day-first for anything with slashes: this club is in India.
const readDate = value => {
  const text = value.trim();
  if (!text) return null;
  let parts = text.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (parts) return new Date(+parts[1], +parts[2] - 1, +parts[3]);
  parts = text.match(/^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$/);
  if (parts) return new Date(+parts[3], +parts[2] - 1, +parts[1]);
  const parsed = new Date(text);
  return isNaN(parsed.valueOf()) ? null : parsed;
};
const showDate = (date, fallback) => {
  if (!date) return fallback;
  const options = { weekday: 'long', day: 'numeric', month: 'long' };
  if (date.getFullYear() !== new Date().getFullYear()) options.year = 'numeric';
  return date.toLocaleDateString('en-IN', options);
};
const renderGatherings = entries => {
  const list = document.createElement('ol');
  list.className = 'gathering-list';
  entries.forEach(entry => {
    const item = document.createElement('li');
    item.className = 'gathering';
    const when = document.createElement('span');
    when.className = 'gathering-date';
    when.textContent = showDate(entry.on, entry.date);
    const body = document.createElement('div');
    const title = document.createElement('h3');
    title.textContent = entry.title || 'A gathering of The Sphere';
    body.append(title);
    if (entry.about) { const p = document.createElement('p'); p.textContent = entry.about; body.append(p); }
    const meta = [entry.time, entry.where || 'Venue shared by email or WhatsApp'].filter(Boolean).join(' · ');
    const metaLine = document.createElement('p');
    metaLine.className = 'gathering-meta';
    metaLine.textContent = meta;
    item.append(when, body, metaLine);
    list.append(item);
  });
  const note = document.createElement('p');
  note.className = 'gatherings-quiet';
  note.append('Venues are shared with members by email and WhatsApp. ');
  const link = document.createElement('a');
  link.href = '#invitation';
  link.dataset.invitation = '';
  link.setAttribute('aria-haspopup', 'dialog');
  link.textContent = 'Request an invitation ';
  const arrow = document.createElement('span');
  arrow.setAttribute('aria-hidden', 'true');
  arrow.textContent = '↗\uFE0E';
  link.append(arrow);
  link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (!invitationDialog || typeof invitationDialog.showModal !== 'function') return;
    event.preventDefault();
    invitationTrigger = link;
    invitationDialog.showModal();
  });
  note.append(link);
  gatheringsSection.querySelector('.gatherings-body').replaceChildren(list, note);
};
const loadGatherings = async () => {
  const source = gatheringsSection?.dataset.gatherings;
  if (!source) return;
  let rows;
  try {
    const response = await fetch(source, { cache: 'no-store' });
    if (!response.ok) return;
    rows = parseCsv(await response.text());
  } catch (error) { return; }
  if (!rows || rows.length < 2) return;
  const columns = rows[0].map(columnFor);
  const midnight = new Date(); midnight.setHours(0, 0, 0, 0);
  const entries = rows.slice(1).map(row => {
    const entry = {};
    columns.forEach((name, i) => { if (name) entry[name] = (row[i] || '').trim(); });
    entry.on = readDate(entry.date || '');
    return entry;
  }).filter(entry => {
    if (/^(no|false|draft|hide|hidden)$/i.test(entry.show || '')) return false;
    if (!entry.title && !entry.about && !entry.date) return false;
    // An unreadable date is still shown: never silently drop what she typed.
    return !entry.on || entry.on >= midnight;
  }).sort((a, b) => (a.on ? a.on.valueOf() : Infinity) - (b.on ? b.on.valueOf() : Infinity)).slice(0, 4);
  if (entries.length) renderGatherings(entries);
};
loadGatherings();

// Hero montage (landing and event pages): silent, looping, and only when the visitor's settings
// welcome motion and data use. It waits for the page to finish loading so the still frame paints first.
const montage = document.querySelector('video[data-montage]');
const montageMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const montageDataAllowed = !(navigator.connection && navigator.connection.saveData);
if (montage && montageDataAllowed) {
  const toggle = montage.closest('section, figure')?.querySelector('.montage-toggle');
  // Landing page: a wide cut for desktop and a tall cut for phones. Event page: a single cut.
  const cut = montage.dataset.tallMp4 ? (window.matchMedia('(max-width: 700px)').matches ? 'tall' : 'wide') : '';
  const source = format => montage.dataset[cut ? cut + format[0].toUpperCase() + format.slice(1) : format];
  let pausedByVisitor = false;
  let started = false;
  let inView = true;
  const play = () => {
    if (!montageMotion.matches && !document.hidden && inView && !pausedByVisitor) montage.play().catch(() => {});
  };
  const start = () => {
    if (started || montageMotion.matches) return;
    started = true;
    [['webm', 'video/webm'], ['mp4', 'video/mp4']].forEach(([format, type]) => {
      if (!source(format)) return;
      const el = document.createElement('source');
      el.src = source(format);
      el.type = type;
      montage.append(el);
    });
    montage.muted = true;
    montage.addEventListener('playing', () => {
      montage.classList.add('is-playing');
      if (toggle) toggle.hidden = false;
    }, { once: true });
    play();
    // Off screen, the video rests so it does not spend battery nobody is watching.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => {
        inView = entry.isIntersecting;
        if (!inView) montage.pause();
        else play();
      }).observe(montage);
    }
  };
  // A pause control is required for motion that lasts longer than five seconds.
  toggle?.addEventListener('click', () => {
    pausedByVisitor = !montage.paused;
    if (pausedByVisitor) montage.pause(); else play();
    toggle.textContent = pausedByVisitor ? 'Play' : 'Pause';
    toggle.setAttribute('aria-label', pausedByVisitor ? 'Play background film' : 'Pause background film');
  });
  montageMotion.addEventListener('change', () => {
    if (montageMotion.matches) {
      montage.pause();
      montage.classList.remove('is-playing');
      if (toggle) toggle.hidden = true;
    } else {
      start();
      if (started && toggle) toggle.hidden = false;
      if (started) montage.classList.add('is-playing');
      play();
    }
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) montage.pause(); else play();
  });
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start, { once: true });
}
