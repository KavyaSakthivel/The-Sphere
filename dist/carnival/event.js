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
