// One-off event page: remove booking once the evening is over, and run the follow-along booking bar.
const eventEnd = Date.parse(document.querySelector('main.event')?.dataset.eventEnd || '');
// Shared motion.js follows this deferred script and handles slow, one-time entrances.
document.querySelectorAll('.event-intro>div,.event-quote,.event-heading,.event-schedule-side,.event-timeline li,.event-who,.event-tickets-copy,.event-card,.event-faq-side,.event-close>h2').forEach(el => el.setAttribute('data-reveal', ''));
if (Date.now() > eventEnd) document.body.classList.add('is-past');

// The bar appears once the opening's booking card scrolls away, and steps aside for the tickets, the close and the footer.
const bar = document.querySelector('[data-event-bar]');
if (bar && 'IntersectionObserver' in window && !document.body.classList.contains('is-past')) {
  const barLinks = bar.querySelectorAll('a');
  const inView = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.isIntersecting ? inView.add(entry.target) : inView.delete(entry.target));
    const show = inView.size === 0;
    bar.classList.toggle('is-visible', show);
    bar.setAttribute('aria-hidden', String(!show));
    barLinks.forEach(link => { link.tabIndex = show ? 0 : -1; });
  });
  ['.event-hero', '.event-pass', '#tickets', '.event-close', 'footer']
    .map(selector => document.querySelector(selector))
    .filter(Boolean)
    .forEach(el => observer.observe(el));
}
