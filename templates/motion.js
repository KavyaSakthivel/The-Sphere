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
    revealTargets.forEach(el => { el.classList.remove('will-reveal'); el.classList.add('is-visible'); });
  };
  const update = () => {
    frame = 0;
    if (!stage || !film || !copy) return;
    if (reduced.matches || small.matches || stage.offsetHeight <= window.innerHeight + 2) {
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
