// One-off event page: remove booking once the evening is over, and run the follow-along booking bar.
const eventEnd = Date.parse(document.querySelector('main.event')?.dataset.eventEnd || '');
if (Date.now() > eventEnd) document.body.classList.add('is-past');

// The bar appears after the opening scrolls away and steps aside for the tickets, the close and the footer.
const bar = document.querySelector('[data-event-bar]');
if (bar && 'IntersectionObserver' in window && !document.body.classList.contains('is-past')) {
  const barLink = bar.querySelector('a');
  const inView = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.isIntersecting ? inView.add(entry.target) : inView.delete(entry.target));
    const show = inView.size === 0;
    bar.classList.toggle('is-visible', show);
    bar.setAttribute('aria-hidden', String(!show));
    barLink.tabIndex = show ? 0 : -1;
  });
  ['.event-hero', '#tickets', '.event-close', 'footer']
    .map(selector => document.querySelector(selector))
    .filter(Boolean)
    .forEach(el => observer.observe(el));
}
