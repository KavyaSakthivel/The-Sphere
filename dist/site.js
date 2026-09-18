const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() {
  mobileNav.hidden = true;
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.querySelector('span').textContent = '+';
}
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  mobileNav.hidden = expanded;
  menuButton.querySelector('span').textContent = expanded ? '+' : '−';
});
mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !mobileNav.hidden) {
    closeMenu();
    menuButton.focus();
  }
});
// Preserve previously shared section links after the content was grouped into pages.
const previousSections = {'#experiences':'/experience/', '#invitation':'/circle/#invitation', '#journal':'/journal/'};
if (location.pathname === '/' && previousSections[location.hash]) location.replace(previousSections[location.hash]);
document.querySelector('#year').textContent = new Date().getFullYear();
