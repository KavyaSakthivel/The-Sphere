// One-off event page: remove booking once the evening is over, and run the follow-along booking bar.
const eventEnd = Date.parse(document.querySelector('main.event')?.dataset.eventEnd || '');
// Shared motion.js follows this deferred script and handles slow, one-time entrances.
document.querySelectorAll('.event-intro>div,.event-quote,.event-heading,.event-schedule-side,.event-timeline li,.event-who,.event-tickets-copy,.event-card,.event-faq-side,.event-close>h2').forEach(el => el.setAttribute('data-reveal', ''));
if (Date.now() > eventEnd) document.body.classList.add('is-past');

// A persistent mobile dock; the desktop bar steps aside for the page's booking controls.
const bar = document.querySelector('[data-event-bar]');
const mobileEvent = window.matchMedia('(max-width: 700px)');
if (bar && !document.body.classList.contains('is-past')) {
  const barLinks = bar.querySelectorAll('a');
  const inView = new Set();
  const updateBar = () => {
    const hero = document.querySelector('.event-cinematic');
    const show = !!hero && hero.getBoundingClientRect().bottom <= 64 && inView.size === 0;
    bar.classList.toggle('is-visible', show);
    bar.setAttribute('aria-hidden', String(!show));
    barLinks.forEach(link => { link.tabIndex = show && link.getClientRects().length ? 0 : -1; });
    document.body.classList.toggle('has-event-dock', mobileEvent.matches && show);
  };
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? inView.add(entry.target) : inView.delete(entry.target));
      updateBar();
    });
    ['.event-hero', '.event-pass', '#tickets', '.event-close', 'footer']
      .map(selector => document.querySelector(selector))
      .filter(Boolean)
      .forEach(el => observer.observe(el));
  }
  window.addEventListener('scroll', updateBar, {passive:true});
  updateBar();
  mobileEvent.addEventListener('change', updateBar);
}

// Follow the section being read, including native anchor jumps and browser history.
(() => {
  const links = [...document.querySelectorAll('.event-mobile-links a, .event-jump a')];
  const sections = ['experience', 'schedule', 'tickets', 'faq'].map(id => document.getElementById(id));
  let frame = 0;
  const update = () => {
    frame = 0;
    const readingLine = Math.min(innerHeight * .3, 220);
    const active = sections.filter(section => section.getBoundingClientRect().top <= readingLine).at(-1);
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

// Native swipe and scroll-snap keep the photo rail usable without JavaScript.
(() => {
  const gallery = document.querySelector('#event-gallery');
  const tools = document.querySelector('.event-gallery-tools');
  if (!gallery || !tools) return;
  const cards = [...gallery.querySelectorAll('figure')];
  const prev = tools.querySelector('[data-gallery-prev]');
  const next = tools.querySelector('[data-gallery-next]');
  const count = tools.querySelector('[data-gallery-count]');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let frame = 0;
  tools.hidden = false;
  const update = () => {
    frame = 0;
    const left = gallery.getBoundingClientRect().left;
    current = cards.reduce((nearest, card, i) => Math.abs(card.getBoundingClientRect().left - left) < Math.abs(cards[nearest].getBoundingClientRect().left - left) ? i : nearest, 0);
    const label = `${current + 1} / ${cards.length}`;
    if (count.textContent !== label) count.textContent = label;
    prev.disabled = current === 0;
    next.disabled = current === cards.length - 1;
  };
  const move = direction => {
    const index = Math.max(0, Math.min(cards.length - 1, current + direction));
    gallery.scrollTo({ left: gallery.scrollLeft + cards[index].getBoundingClientRect().left - gallery.getBoundingClientRect().left, behavior: reduced.matches ? 'instant' : 'smooth' });
  };
  prev.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  gallery.addEventListener('scroll', () => { if (!frame) frame = requestAnimationFrame(update); }, { passive: true });
  gallery.addEventListener('keydown', event => {
    if (mobileEvent.matches && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      event.preventDefault();
      move(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  window.addEventListener('resize', update, { passive: true });
  update();
})();
