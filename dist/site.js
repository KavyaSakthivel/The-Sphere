const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
const header = document.querySelector('.header');
const updateHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 48);
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });
new ResizeObserver(() => {
  document.documentElement.style.setProperty('--navigation-height', `${header.getBoundingClientRect().height}px`);
}).observe(header);
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  mobileNav.hidden = expanded;
  menuButton.querySelector('span').textContent = expanded ? '+' : '−';
});
mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  mobileNav.hidden = true;
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.querySelector('span').textContent = '+';
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
document.querySelectorAll('[data-entry]').forEach(button => {
  button.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    const dialog = document.querySelector('#article-dialog');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    event.preventDefault();
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
    menuButton.querySelector('span').textContent = '+';
    menuButton.focus();
  }
});
document.querySelector('#year').textContent = new Date().getFullYear();
