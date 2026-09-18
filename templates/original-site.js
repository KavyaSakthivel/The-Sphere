const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
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
document.querySelector('[data-invitation]').addEventListener('click', () => document.querySelector('#invitation-dialog').showModal());
const entries = [
  {title:'Wellness is a necessity, not a luxury', subtitle:'Why making space for yourself isn’t selfish.', paragraphs:['For a woman constantly giving her time, energy and attention to everyone around her, taking care of herself can become the last item on the list. It is easy to postpone a quiet hour until everything else is done.','But there will always be another thing to do. Making room for yourself is a way of recognising that you, too, are part of the life you care for.','At The Sphere, we believe wellness belongs in the everyday. A little movement. A meaningful conversation. A moment in which nothing is required of you. Sometimes, choosing yourself begins with simply showing up.']},
  {title:'The art of slowing down', subtitle:'Why rest isn’t something you need to earn.', paragraphs:['There is a particular kind of quiet that comes when you stop measuring a moment by what it produces. A cup of tea can be a cup of tea. A walk can have no destination.','Slowing down does not have to mean stepping away from your ambitions. It can mean making enough space to notice how you feel as you pursue them.','Try leaving a small part of your day unclaimed. No goal, no checklist, no better version of yourself to become. Just a little time to be where you are.']},
  {title:'Women who make space for women', subtitle:'Why community becomes more meaningful as we grow.', paragraphs:['A conversation can begin with what we do. The conversations that stay with us often go a little further: how we are, what we are learning, what we are making room for.','Women arrive from different professions, different stages of life and different worlds. Meaningful connection leaves space for those differences, without requiring anyone to have it all figured out.','The Sphere is built around that possibility. An intimate gathering. An honest conversation. The simple experience of being heard.']},
  {title:'Beyond the checklist', subtitle:'Wellness isn’t another thing to accomplish.', paragraphs:['When even our quiet moments become things to track and complete, care can begin to feel like another obligation. A perfect morning routine is still a routine to keep up with.','What if wellness began with a question instead of a plan? What would feel good today? What would make a little more room? The answer need not look the same every day.','Some days it might be movement. On others, stillness or company. There is room for all of it. There is room for you, as you are.']},
  {title:'The modern woman', subtitle:'Ambitious, nurturing, independent, evolving.', paragraphs:['A founder. A mother. A leader. A daughter. A partner. A friend. Each role can hold something meaningful, and each can ask something of us.','Beyond every role, there is a person whose curiosity, needs and wishes are still unfolding. You do not have to choose a single definition of yourself, or stay the woman you were yesterday.','The Sphere was created for the woman behind all those roles. Come as you are. Stay for what you discover.']}
];
const journalList = document.querySelector('.journal-list');
entries.forEach((entry, index) => {
  const button = document.createElement('button');
  button.className = 'journal-entry';
  button.innerHTML = `<span class="journal-number">0${index + 1}</span><span class="journal-title">${entry.title}</span><span class="journal-subtitle">${entry.subtitle}</span><span class="journal-arrow" aria-hidden="true">↗</span>`;
  button.setAttribute('aria-label', `Read ${entry.title}`);
  button.addEventListener('click', () => {
    document.querySelector('#article-title').textContent = entry.title;
    const body = document.querySelector('#article-body');
    body.replaceChildren(...entry.paragraphs.map(text => {const p = document.createElement('p'); p.textContent = text; return p;}));
    document.querySelector('#article-dialog').showModal();
  });
  journalList.append(button);
});
document.querySelector('#year').textContent = new Date().getFullYear();
