"""Build the one-off event page from data/event.json, and retire it cleanly once that file is gone.

All visible copy is the client's own, taken word for word from preview.html. Do not add facts here
that the client has not supplied.

Everything the event adds lives in dist/<slug>/ plus a few marked hooks on the home page, so removing
the event is: delete data/event.json, run build_site.py, deploy. The old URL then redirects home.
"""
from pathlib import Path
from html import escape
from datetime import datetime
import json, re, shutil
from seo import CONFIG, url, org

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/event.json'
TEMPLATES = ROOT/'templates/event'
MONTAGE = TEMPLATES/'montage'


def load():
 if not SOURCE.exists():
  return None
 ev = json.loads(SOURCE.read_text())
 ev['start_at'] = datetime.fromisoformat(ev['start'])
 ev['end_at'] = datetime.fromisoformat(ev['end'])
 ev['path'] = '/'+ev['slug']+'/'
 # An embedded Razorpay button first; then a hosted payment link; otherwise payment is not connected yet.
 if ev.get('razorpay_button_id'): ev['mode'] = 'button'
 elif ev.get('payment_url'): ev['mode'] = 'link'
 else: ev['mode'] = 'soon'
 return ev


def a(v): return escape(str(v), quote=True)
def rupees(n): return '₹'+f'{n:,}'
def time_of(d): return d.strftime('%-I:%M %p')
def full_date(d): return d.strftime('%-d %B %Y')
def hours(ev): return f"{time_of(ev['start_at'])} – {time_of(ev['end_at'])}"
def where(ev): return f"{ev['venue']}, {ev['city']}"
def book_href(ev): return ev['payment_url'] if ev['mode'] == 'link' else '#tickets'
def arrow(): return '<span aria-hidden="true">&#8599;</span>'


# ---------------------------------------------------------------- home page hooks

def feature_home(html, ev):
 """Point the home page at the event. Each hook removes itself in the browser once the event ends."""
 if not ev or not ev.get('show_on_home'):
  return html
 until = a(ev['end'])
 d = ev['start_at']
 chip = (f'<a class="hero-event" href="{ev["path"]}" data-event-until="{until}">'
  f'<span class="hero-event-date">{d.strftime("%-d %b").upper()}<span class="hero-event-long">{d.strftime("%B")[3:].upper()} {d.year}</span></span>'
  f'<span class="hero-event-name">{escape(ev["name"]).replace("The Sphere ", "<span class=hero-event-long>The Sphere </span>", 1)}</span>'
  f'<span class="hero-event-cta">Get Your Ticket {arrow()}</span></a>')
 html = html.replace('<div class="hero-prelude">', chip+'<div class="hero-prelude">', 1)
 link = f'<a href="{ev["path"]}" data-event-until="{until}">Wellness Carnival</a>'
 html = re.sub(r'(<nav class="desktop-nav"[^>]*>.*?)(</nav>)', lambda m: m[1]+link+m[2], html, count=1, flags=re.S)
 html = re.sub(r'(<nav id="mobile-nav"[^>]*>)', lambda m: m[1]+link, html, count=1)
 feature = (f'<a class="event-feature" href="{ev["path"]}" data-event-until="{until}">'
  f'<span class="event-feature-date">{full_date(d).upper()}<br>{hours(ev)}</span>'
  f'<span class="event-feature-body"><span class="event-feature-kicker">{escape(ev["audience"]).upper()}</span>'
  f'<span class="event-feature-title">{escape(ev["name"])}</span>'
  f'<span class="event-feature-meta">{escape(ev["tagline"])} {escape(where(ev))}</span></span>'
  f'<span class="event-feature-cta">Reserve Your Spot {arrow()}</span></a>')
 return html.replace('<div class="gatherings-body">', feature+'<div class="gatherings-body">', 1)


# ---------------------------------------------------------------- page content (verbatim from preview.html)

EXPERIENCES = [
 ('Mindful Experiences', 'Moments designed to help you slow down, reconnect and be present.'),
 ('Breath &amp; Movement', 'A guided Breath Walk to help you reconnect with yourself.'),
 ('Sound Healing', 'An immersive experience created around relaxation and mindful connection.'),
 ('Nourishing Food', 'A curated dinner to enjoy alongside meaningful conversations.'),
 ('Sober Party', 'Music, movement and celebration &mdash; without alcohol.'),
 ('Community &amp; Connection', 'Meet like-minded people and create new connections.'),
]
SCHEDULE = [
 ('3:00 – 5:00 PM', 'Settle In', 'Arrive, register, get comfortable and connect with fellow attendees.'),
 ('5:00 – 5:30 PM', 'Inauguration', 'A warm welcome to begin the evening.'),
 ('5:30 – 6:00 PM', 'Breath Walk', 'A guided breathwork experience to help you slow down and become present.'),
 ('6:00 – 7:00 PM', 'Sound Healing', 'An immersive sound healing experience designed for relaxation and mindful connection.'),
 ('7:00 – 8:00 PM', 'Dinner', 'Nourishing food, conversations and community.'),
 ('8:00 – 10:00 PM', 'Sober Party', 'Music, movement and celebration to close the evening.'),
]
FAQS = [
 ('What is The Sphere Wellness Carnival?', 'A wellness-led social experience bringing together mindful activities, sound healing, food, music and community.'),
 ('When and where is the event?', "20 December 2026, from 3:00 PM to 10:00 PM at Jenney's Residency, Coimbatore."),
 ('Do I need prior wellness experience?', 'No. The experience is designed to be accessible to participants.'),
 ('Is alcohol served?', 'No. The evening concludes with a sober party featuring music, movement and social experiences.'),
 ('Can I attend alone?', 'Yes. The event is designed to encourage community and meaningful connections.'),
 ('Is dinner included?', 'Dinner is part of the event schedule.'),
]


def faqs(ev):
 items = [(q, escape(ans)) for q, ans in FAQS]
 # Shown only once the club has supplied its own policy wording.
 if ev.get('refund_policy'):
  items.append(('Can I cancel or transfer my ticket?', escape(ev['refund_policy'])))
 return ''.join(f'<details{" open" if i == 0 else ""}><summary>{q} <span aria-hidden="true">+</span></summary><p>{ans}</p></details>'
  for i, (q, ans) in enumerate(items))


def ticket_action(ev):
 if ev['mode'] == 'button':
  # Razorpay renders its own button here; checkout opens over this page, with no server of ours involved.
  return (f'<form class="event-rzp"><script src="https://checkout.razorpay.com/v1/payment-button.js" '
   f'data-payment_button_id="{a(ev["razorpay_button_id"])}" async></script></form>')
 if ev['mode'] == 'link':
  return f'<a class="button button-dark event-card-book" href="{a(ev["payment_url"])}">Book Your Experience {arrow()}</a>'
 # Payment not connected yet: the client's own placeholder line, and no button that goes nowhere.
 return '<p class="event-card-small">Payment and ticketing link will be available at checkout.</p>'


def has_montage(): return (MONTAGE/'hero.mp4').exists()


def hero_visual(ev):
 if not has_montage():
  return ('<img src="/assets/session-bowls-1200.webp" srcset="/assets/session-bowls-640.webp 640w, /assets/session-bowls-1200.webp 1200w" '
   'sizes="(max-width: 700px) 88vw, 44vw" alt="Singing bowls, a cushion and mats laid out before a Sphere session" fetchpriority="high" width="1200" height="1800">')
 # The club's own montage (scripts/build_montage.py). The poster is its first frame, so the swap is invisible;
 # site.js only starts the video when motion and data use are welcome. It adds nothing to the page's words.
 base = ev['path']
 return (f'<img src="{base}hero-poster.jpg" alt="" fetchpriority="high" width="720" height="900">'
  f'<video class="event-hero-video" muted loop playsinline preload="none" aria-hidden="true" data-montage '
  f'data-webm="{base}hero.webm" data-mp4="{base}hero.mp4"></video>'
  '<button class="event-video-toggle montage-toggle" type="button" hidden>Pause</button>')


def date_chip(ev):
 d = ev['start_at']
 return (f'<p class="event-date-chip" aria-hidden="true"><span>{d.strftime("%B").upper()}</span>'
  f'<strong>{d.day}</strong><em>{d.year}</em></p>')


def page(ev):
 book = book_href(ev)
 price = rupees(ev['price_inr'])
 ticket_note = f'<p class="event-card-note">{escape(ev["ticket_note"])}</p>' if ev.get('ticket_note') else ''
 date, time, place = full_date(ev['start_at']), hours(ev), escape(where(ev))
 experiences = ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in EXPERIENCES)
 schedule = ''.join(f'<li><span class="event-time">{w}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for w, t, d in SCHEDULE)
 return f'''<main id="main" class="event" data-event-end="{a(ev['end'])}">
<section class="event-hero" aria-labelledby="event-title">
 <div class="event-hero-copy">
  <nav class="event-crumb" aria-label="Breadcrumb"><a href="/">The Sphere</a><span aria-hidden="true">/</span><span aria-current="page">Wellness Carnival</span></nav>
  <p class="eyebrow">{escape(ev['name']).upper()}</p>
  <h1 id="event-title">A day to pause.<br><em>Breathe. Connect. Celebrate.</em></h1>
  <p class="event-tagline">Crafted calm for the modern woman.</p>
  <dl class="event-facts">
   <div><dt>When</dt><dd>{date}<br><span>{time}</span></dd></div>
   <div><dt>Where</dt><dd>{place}</dd></div>
   <div><dt>Who</dt><dd>{escape(ev['audience'])}</dd></div>
   <div><dt>Entry</dt><dd>{price} <span>{escape(ev['price_note'])}</span></dd></div>
  </dl>
  <div class="event-actions" data-book><a class="button button-dark" href="{a(book)}">Reserve Your Spot {arrow()}</a></div>
 </div>
 <figure class="event-hero-visual">
  {hero_visual(ev)}
  {date_chip(ev)}
 </figure>
</section>
<div class="quiet-line"><span>WELLNESS</span><span>NOURISH</span><span>MUSIC</span><span>COMMUNITY</span></div>

<section class="event-intro section-pad">
 <div>
  <p class="eyebrow">MORE THAN AN EVENT</p>
  <h2>Make space<br><em>for yourself.</em></h2>
  <div class="prose">
   <p>Step away from the rush of everyday life and into an evening created around wellness, connection and celebration.</p>
   <p>The Sphere Wellness Carnival brings together mindful experiences, movement, sound, nourishing food, music and community &mdash; creating a space where you can slow down, reconnect and enjoy the moment.</p>
  </div>
 </div>
 <blockquote class="event-quote">&ldquo;Sometimes, you simply need a space to pause, breathe deeply, meet new people and leave feeling a little lighter.&rdquo;</blockquote>
</section>

<section id="experience" class="event-experience section-pad" aria-labelledby="experience-title">
 <div class="section-heading"><div><p class="eyebrow">THE EXPERIENCE</p><h2 id="experience-title">Come for the experience.<br><em>Stay for the feeling.</em></h2></div>
 <p>An evening thoughtfully brought together around well-being, community and celebration.</p></div>
 <ul class="event-grid">{experiences}</ul>
</section>

<section id="schedule" class="event-schedule section-pad" aria-labelledby="schedule-title">
 <p class="eyebrow">YOUR EVENING</p><h2 id="schedule-title">A little preview<br><em>of your day.</em></h2>
 <ol class="event-timeline">{schedule}</ol>
</section>

<section id="tickets" class="event-tickets section-pad" aria-labelledby="tickets-title">
 <div class="event-tickets-copy">
  <p class="eyebrow">TICKETS</p>
  <h2 id="tickets-title">Choose your moment<br><em>to join us.</em></h2>
  <p>Your ticket to an evening of wellness, connection, nourishing food and celebration.</p>
  <p class="event-welcome">Women &amp; Couples Welcome</p>
 </div>
 <div class="event-card">
  <p class="eyebrow">ENTRY TICKET</p>
  <p class="event-price">{price}</p>
  <p class="event-card-note">{escape(ev['price_note'])}</p>{ticket_note}
  <ul class="event-card-facts">
   <li>{date}</li>
   <li>{place}</li>
  </ul>
  <div class="event-card-action">{ticket_action(ev)}</div>
 </div>
</section>

<section class="event-who section-pad" aria-labelledby="who-title">
 <p class="eyebrow">WHO IS IT FOR?</p>
 <h2 id="who-title">Come <em>as you are.</em></h2>
 <p><strong>Women &amp; Couples are welcome.</strong> Whether you want to slow down, reconnect, meet new people, explore wellness, enjoy good food or simply dance freely &mdash; there is space for you at The Sphere.</p>
</section>

<section id="faq" class="event-faq section-pad" aria-labelledby="faq-title">
 <div class="event-faq-side"><p class="eyebrow">GOOD TO KNOW</p><h2 id="faq-title">Frequently asked<br><em>questions.</em></h2></div>
 <div class="experience-list event-questions">{faqs(ev)}</div>
</section>

<section class="event-close section-pad">
 <p class="eyebrow">{escape(ev['name']).upper()}</p>
 <h2>Your next chapter can begin<br><em>with a pause.</em></h2>
 <p>Come slow down. Come connect. Come celebrate.</p>
 <p class="event-close-meta">{date} &nbsp;&bull;&nbsp; {place} &nbsp;&bull;&nbsp; {time}</p>
 <p data-book><a class="button button-dark" href="{a(book)}">Reserve Your Spot {arrow()}</a></p>
</section>
</main>
<div class="event-bar" data-event-bar aria-hidden="true">
 <p><strong>{ev['start_at'].strftime('%-d %b %Y')} &middot; {place}</strong><span>{time} &middot; Entry {price} + Applicable Fee</span></p>
 <a class="button button-dark" href="{a(book)}" tabindex="-1">Book Your Experience {arrow()}</a>
</div>'''


# ---------------------------------------------------------------- assembly

def seo(ev, path, title):
 image = url('/assets/session-bowls-1200.webp')
 meta = f'''
  <link rel="canonical" href="{a(url(path))}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta property="og:site_name" content="The Sphere">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_IN">
  <meta property="og:title" content="{a(title)}">
  <meta property="og:description" content="{a(ev['description'])}">
  <meta property="og:url" content="{a(url(path))}">
  <meta property="og:image" content="{a(image)}">
  <meta property="og:image:alt" content="Singing bowls, a cushion and mats laid out before a Sphere session">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{a(title)}">
  <meta name="twitter:description" content="{a(ev['description'])}">
  <meta name="twitter:image" content="{a(image)}">'''
 offer = {'@type': 'Offer', 'name': 'Entry ticket', 'price': str(ev['price_inr']), 'priceCurrency': 'INR', 'url': url(path)}
 if ev['mode'] != 'soon':
  offer['availability'] = 'https://schema.org/InStock'
 event = {'@type': 'Event', '@id': url(path+'#event'), 'name': ev['name'], 'description': ev['description'],
  'startDate': ev['start'], 'endDate': ev['end'], 'eventStatus': 'https://schema.org/EventScheduled',
  'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'image': [image], 'url': url(path),
  'location': {'@type': 'Place', 'name': ev['venue'], 'address': {'@type': 'PostalAddress', 'addressLocality': ev['city'],
   'addressRegion': CONFIG['region'], 'addressCountry': CONFIG['country']}},
  'organizer': {'@id': url('/#organization')}, 'offers': offer}
 crumbs = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'The Sphere', 'item': url()},
  {'@type': 'ListItem', 'position': 2, 'name': ev['name'], 'item': url(path)}]}
 data = json.dumps({'@context': 'https://schema.org', '@graph': [org(), event, crumbs]}, ensure_ascii=False).replace('<', r'<')
 return meta+f'\n  <script type="application/ld+json">{data}</script>\n'


def assemble(home, ev, path, title, body):
 head = re.search(r'<head>(.*?)</head>', (ROOT/'templates/original-index.html').read_text(), re.S)[1]
 head = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>', head, count=1)
 head = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{a(ev["description"])}">', head, count=1)
 head = head.replace('</script>', '</script>\n  <link rel="stylesheet" href="/'+ev['slug']+'/event.css?v=4">\n  <script src="/'+ev['slug']+'/event.js?v=4" defer></script>', 1)
 shell = re.search(r'<a class="skip".*?<main id="main">', home, re.S)[0].removesuffix('<main id="main">')
 # On the event page the header's call to action is the ticket itself.
 shell = re.sub(r'<a class="header-invite"[^>]*>.*?</a>',
  f'<a class="header-invite" href="{a(book_href(ev))}" data-book>Get Your Ticket {arrow()}</a>', shell, count=1, flags=re.S)
 shell = shell.replace(f'<a href="{ev["path"]}" data-event-until', f'<a href="{ev["path"]}" aria-current="page" data-event-until')
 footer = re.search(r'<footer>.*?</footer>', home, re.S)[0]
 invitation = re.search(r'<dialog id="invitation-dialog".*?</dialog>', home, re.S)[0]
 html = f'<!doctype html><html lang="en-IN"><head>{head}{seo(ev, path, title)}</head><body class="event-page">{shell}\n{body}{footer}{invitation}</body></html>'
 html = re.sub(r'(href|src|srcset)="(assets/|style.css|brand.css|site.js)', r'\1="/\2', html)
 html = html.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"').replace('href="/#tickets"', 'href="#tickets"')
 return html


def build(home):
 ev = load()
 folder = ROOT/'dist'/(ev['slug'] if ev else 'carnival')
 if not ev:
  retire(folder)
  return
 if folder.exists():
  shutil.rmtree(folder)
 folder.mkdir(parents=True)
 for name in ('event.css', 'event.js'):
  shutil.copyfile(TEMPLATES/name, folder/name)
 if has_montage():
  for name in ('hero.mp4', 'hero.webm', 'hero-poster.jpg'):
   shutil.copyfile(MONTAGE/name, folder/name)
 title = f"{ev['name']} | {full_date(ev['start_at'])}, {ev['city']}"
 (folder/'index.html').write_text(assemble(home, ev, ev['path'], title, page(ev)))
 sitemap = ROOT/'dist/sitemap.xml'
 loc = '  <url><loc>'+escape(url(ev['path']))+'</loc></url>\n'
 if loc not in sitemap.read_text():
  sitemap.write_text(sitemap.read_text().replace('</urlset>', loc+'</urlset>'))
 print(f"Built {ev['path']} ({ev['mode']} booking mode, {'montage' if has_montage() else 'photo'} hero).")


def retire(folder):
 # Links shared on WhatsApp and Instagram keep working after the event: they land on the home page.
 if not folder.exists():
  return
 shutil.rmtree(folder)
 folder.mkdir()
 (folder/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  '<meta http-equiv="refresh" content="0;url=/#gatherings"><title>The Sphere</title><meta name="robots" content="noindex,follow"></head>'
  '<body><a href="/#gatherings">Enter The Sphere</a></body></html>')
 print(f'Retired /{folder.name}/ to a redirect.')
