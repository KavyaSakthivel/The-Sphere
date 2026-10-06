/* One experience at a time, with native keyboard navigation and a readable no-script layout. */
document.querySelectorAll('[data-pillar-browser]').forEach(browser => {
  const tablist = browser.querySelector('.pillar-tabs');
  const tabs = [...tablist.querySelectorAll('button')];
  const panels = [...browser.querySelectorAll('.pillar-panel')];
  tablist.hidden = false;
  tablist.setAttribute('role', 'tablist');
  const select = (index, focus = false) => {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    panels[index].querySelectorAll('[data-image-reveal]').forEach(image => image.classList.add('is-visible'));
    if (focus) tabs[index].focus({preventScroll: true});
  };
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].setAttribute('aria-labelledby', tab.id);
    tab.addEventListener('click', () => select(i));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); select(next, true); }
    });
  });
  select(0);
});

/* Native scroll, restrained reveals, and a short film-to-page transition. No scroll hijacking. */
(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const small = window.matchMedia('(max-width: 700px)');
  const stage = document.querySelector('[data-film-stage]');
  const film = document.querySelector('[data-film-image]');
  const copy = document.querySelector('[data-film-copy]');
  const parallax = document.querySelector('[data-parallax]');
  let observer;
  let frame = 0;
  const revealTargets = [...document.querySelectorAll('[data-reveal], [data-image-reveal]')];
  const initialiseReveals = () => {
    observer?.disconnect();
    if (reduced.matches || !('IntersectionObserver' in window)) {
      revealTargets.forEach(el => el.classList.remove('will-reveal'));
      return;
    }
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .08, rootMargin: '0px 0px -24px 0px' });
    revealTargets.forEach(el => {
      // Do not hide an already visible heading while the page initialises or a preference changes.
      if (el.getBoundingClientRect().top < window.innerHeight - 24) el.classList.add('is-visible');
      el.classList.add('will-reveal');
      observer.observe(el);
    });
  };
  const update = () => {
    frame = 0;
    if (!stage || !film || !copy) return;
    if (reduced.matches || small.matches) {
      film.style.removeProperty('--film-inset');
      copy.style.removeProperty('--film-copy-y');
      copy.style.removeProperty('--film-copy-opacity');
      parallax?.style.removeProperty('--parallax-y');
      return;
    }
    const rect = stage.getBoundingClientRect();
    const travel = Math.max(stage.offsetHeight - window.innerHeight, 1);
    const progress = Math.min(1, Math.max(0, -rect.top / travel));
    film.style.setProperty('--film-inset', `${progress * Math.min(window.innerWidth * .028, 42)}px`);
    copy.style.setProperty('--film-copy-y', `${-progress * 45}px`);
    copy.style.setProperty('--film-copy-opacity', `${1 - progress * .8}`);
    if (parallax) {
      const box = parallax.parentElement.getBoundingClientRect();
      if (box.bottom > 0 && box.top < window.innerHeight) {
        const position = (window.innerHeight / 2 - box.top - box.height / 2) / window.innerHeight;
        parallax.style.setProperty('--parallax-y', `${Math.max(-45, Math.min(45, position * 55))}px`);
      }
    }
  };
  const schedule = () => { if (!frame) frame = window.requestAnimationFrame(update); };
  initialiseReveals();
  update();
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  reduced.addEventListener('change', () => { initialiseReveals(); schedule(); });
  small.addEventListener('change', schedule);
})();

// A seasonal invitation on entry, once per tab session, with a fixed India-time expiry.
(() => {
  const popup = document.querySelector('[data-carnival-popup]');
  if (!popup) return;
  const until = Date.parse(popup.dataset.promotionUntil);
  if (!Number.isFinite(until) || Date.now() >= until) { popup.remove(); return; }
  const key = `sphere-promotion:${popup.dataset.promotionKey}`;
  try { if (sessionStorage.getItem(key)) return; } catch (_) { /* Storage may be disabled. */ }
  if (typeof popup.showModal !== 'function') return;
  const previousFocus = document.activeElement;
  popup.querySelector('[data-dismiss-carnival]').addEventListener('click', () => popup.close());
  popup.addEventListener('close', () => {
    if (previousFocus instanceof HTMLElement && previousFocus !== document.body) previousFocus.focus({ preventScroll: true });
    else document.querySelector('.header .wordmark')?.focus({ preventScroll: true });
  });
  popup.showModal();
  try { sessionStorage.setItem(key, 'seen'); } catch (_) { /* Still usable without storage. */ }
})();
