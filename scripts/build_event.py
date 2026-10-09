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


# The client chose DSC09903 for "03 / Connect" (data/media-selection.json, sphere-carnival-connect). Until that
# photograph is exported, the earlier conversation photograph stands in.
CONNECT_PHOTO = 'sphere-carnival-connect' if (Path(__file__).resolve().parents[1]/'dist/assets/sphere-carnival-connect-1200.webp').exists() else 'sphere-conversation'

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
 # On wide screens the event sits on the right, beside the invitation, so the header stays balanced.
 html = re.sub(r'<a class="header-invite"[^>]*>.*?</a>', lambda m: f'<div class="header-actions"><a class="header-event" href="{ev["path"]}" data-event-until="{until}">Wellness Carnival</a>{m[0]}</div>', html, count=1, flags=re.S)
 html = re.sub(r'(<nav id="mobile-nav"[^>]*>)', lambda m: m[1]+link, html, count=1)
 feature = (f'<a class="event-feature" href="{ev["path"]}" data-event-until="{until}">'
  f'<span class="event-feature-date">{full_date(d).upper()}<br>{hours(ev)}</span>'
  f'<span class="event-feature-body"><span class="event-feature-kicker">{escape(ev["audience"]).upper()}</span>'
  f'<span class="event-feature-title">{escape(ev["name"])}</span>'
  f'<span class="event-feature-meta">{escape(ev["tagline"])} {escape(where(ev))}</span></span>'
  f'<span class="event-feature-cta">Reserve Your Spot {arrow()}</span></a>')
 return html.replace('<div class="gatherings-body">', feature+'<div class="gatherings-body">', 1)


# ---------------------------------------------------------------- page content (verbatim from preview.html)

# Simple line icons stand in for the preview's emoji (📅 📍 ⏰ ✨ 🌿 🧘 🔔 🥗 🎶 🤍). They carry no words of their own.
ICON_PATHS = {
 'calendar': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0C18.5 15.4 12 21 12 21z"/><circle cx="12" cy="10" r="2.3"/>',
 'people': '<circle cx="9" cy="8.5" r="3"/><path d="M3.5 19c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5"/><circle cx="16.5" cy="9.5" r="2.4"/><path d="M15.5 14.2c2.6-.3 4.5 1.4 5 4.3"/>',
 'leaf': '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14z"/><path d="M5 19l7-7"/>',
 'breath': '<path d="M3 9h11a3 3 0 1 0-3-3M3 13h15a3 3 0 1 1-3 3M3 17h7"/>',
 'bell': '<path d="M5 15h14l-1.5-2V10a5.5 5.5 0 0 0-11 0v3z"/><path d="M10 18.5a2 2 0 0 0 4 0"/>',
 'bowl': '<path d="M3.5 11h17a8.5 8.5 0 0 1-17 0z"/><path d="M9 7c0-1.5 1-1.5 1-3M13 7c0-1.5 1-1.5 1-3"/>',
 'music': '<path d="M9 18V6l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/>',
 'heart': '<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.3a4.3 4.3 0 0 1 7.5 2.5C19.5 15.4 12 20 12 20z"/>',
}
def icon(name): return f'<svg class="event-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICON_PATHS[name]}</svg>'

EXPERIENCES = [
 ('leaf', 'Mindful Experiences', 'Moments designed to help you slow down, reconnect and be present.'),
 ('breath', 'Breath &amp; Movement', 'A guided Breath Walk to help you reconnect with yourself.'),
 ('bell', 'Sound Healing', 'An immersive experience created around relaxation and mindful connection.'),
 ('bowl', 'Nourishing Food', 'A curated dinner to enjoy alongside meaningful conversations.'),
 ('music', 'Sober Party', 'Music, movement and celebration &mdash; without alcohol.'),
 ('heart', 'Community &amp; Connection', 'Meet like-minded people and create new connections.'),
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
# The preview's own header links, reused as a jump row so a reader can go straight to what they need.
SECTIONS = [('experience', 'Experience'), ('schedule', 'Schedule'), ('tickets', 'Tickets'), ('faq', 'FAQs')]


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
  return f'<a class="cv-button" href="{a(ev["payment_url"])}">Book Your Experience {arrow()}</a>'
 # Payment not connected yet: the client's own placeholder line, and no button that goes nowhere.
 return '<p class="cv-ticket-small">Ticket booking will open soon.</p>'


def has_montage(): return (MONTAGE/'hero.mp4').exists()


def hero_visual(ev):
 if (ROOT/'dist/assets/montage-carnival/wide.mp4').exists():
  return ('<picture><source media="(max-width:700px)" srcset="/assets/montage-carnival/tall-poster.jpg"><img src="/assets/montage-carnival/wide-poster.jpg" alt="" fetchpriority="high" width="1600" height="900"></picture>'
   '<video class="event-hero-video" muted loop playsinline preload="none" aria-hidden="true" data-montage '
   'data-wide-webm="/assets/montage-carnival/wide.webm" data-wide-mp4="/assets/montage-carnival/wide.mp4" '
   'data-tall-webm="/assets/montage-carnival/tall.webm" data-tall-mp4="/assets/montage-carnival/tall.mp4"></video>'
   '<button class="event-video-toggle montage-toggle" type="button" hidden aria-label="Pause background film">Pause</button>')
 if not has_montage():
  return ('<img src="/assets/sphere-bowls-1200.webp" srcset="/assets/sphere-bowls-640.webp 640w, /assets/sphere-bowls-1200.webp 1200w" '
   'sizes="(max-width: 900px) 88vw, 40vw" alt="Singing bowls, a cushion and mats laid out before a Sphere session" fetchpriority="high" width="1200" height="1800">')
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


def jump_links(): return ''.join(f'<a href="#{i}">{t}</a>' for i, t in SECTIONS)


def mobile_links():
 icons = ['leaf', 'clock', 'calendar', 'heart']
 return ''.join(f'<a href="#{section}" tabindex="-1">{icon(symbol)}<span>{label}</span></a>'
  for (section, label), symbol in zip(SECTIONS, icons))


def page(ev):
 """The carnival page. Every visible line comes from the client's preview; the layout puts the
 answers a guest looks for first (when, where, who, what it includes, what it costs) in plain view."""
 book = book_href(ev)
 price = rupees(ev['price_inr'])
 ticket_note = f'<p class="cv-ticket-note">{escape(ev["ticket_note"])}</p>' if ev.get('ticket_note') else ''
 date, time, place = full_date(ev['start_at']), hours(ev), escape(where(ev))
 audience = escape(ev['audience'])
 offer = ''.join(f'<li><span class="cv-icon">{icon(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in EXPERIENCES)
 schedule = ''.join(f'<li><p class="cv-time">{w}</p><div><h3>{t}</h3><p>{d}</p></div></li>' for w, t, d in SCHEDULE)
 moments = ''.join(f'<figure><img src="/assets/{f}-1200.webp" srcset="/assets/{f}-640.webp 640w, /assets/{f}-1200.webp 1200w" sizes="(max-width:700px) 86vw, 28vw" alt="{alt}" width="1200" height="1500" loading="lazy" decoding="async"><figcaption><span>{k}</span>{h}</figcaption></figure>'
  for f, alt, k, h in [('sphere-move-smile', 'A woman smiling as she stretches her arms overhead in a Sphere movement class', '01 / MOVE', 'Return to your body.'),
                        ('sphere-bowls', 'Singing bowls prepared for sound healing', '02 / PAUSE', 'Make room for stillness.'),
                        (CONNECT_PHOTO, 'Women connecting at a Sphere gathering', '03 / CONNECT', 'Find your people.')])
 glance_cta = (f'<a class="cv-glance-cta" href="#tickets">View tickets <span aria-hidden="true">↓</span></a>' if ev['mode'] == 'soon'
  else f'<a class="cv-glance-cta" href="{a(book)}" data-book>Reserve your spot {arrow()}</a>')
 return f"""<main id="main" class="event carnival" data-event-end="{a(ev['end'])}">
<section class="event-hero event-cinematic" aria-labelledby="event-title">
 <figure class="event-hero-visual">{hero_visual(ev)}</figure>
 <div class="event-hero-copy">
  <p class="eyebrow">{escape(ev['name']).upper()}</p>
  <h1 id="event-title"><span>Pause.</span> <span>Connect.</span><br><span>Celebrate.</span></h1>
  <p class="event-tagline">{date} &nbsp;·&nbsp; Coimbatore<span class="cv-sep"> &nbsp;·&nbsp; </span><span class="cv-hero-time">{time}</span></p>
  <p data-book><a class="cv-button cv-button-light" href="{a(book)}">Reserve your spot {arrow()}</a></p>
 </div>
 <a class="event-scroll-cue" href="#event-details" aria-label="Explore the carnival">SCROLL TO DISCOVER <span aria-hidden="true">↓</span></a>
</section>

<section id="event-details" class="cv-glance" aria-label="Your evening, at a glance">
 <dl>
  <div>{icon('calendar')}<dt>WHEN</dt><dd><strong>{date}</strong><span>{time}</span></dd></div>
  <div>{icon('pin')}<dt>WHERE</dt><dd><strong>{place}</strong></dd></div>
  <div>{icon('people')}<dt>WHO</dt><dd><strong>{audience}</strong></dd></div>
  <div class="cv-glance-price"><dt>ENTRY TICKET</dt><dd><strong>{price}</strong><span>{escape(ev['price_note'])}</span></dd></div>
 </dl>
 {glance_cta}
</section>

<nav class="cv-jump" aria-label="On this page">{jump_links()}</nav>

<section class="cv-intro" aria-labelledby="intro-title">
 <div class="cv-intro-copy">
  <p class="eyebrow">MORE THAN AN EVENT</p>
  <h2 id="intro-title">Make space<br>for yourself.</h2>
  <p class="cv-lead">Step away from the rush of everyday life and into an evening created around wellness, connection and celebration.</p>
  <p>The Sphere Wellness Carnival brings together mindful experiences, movement, sound, nourishing food, music and community &mdash; creating a space where you can slow down, reconnect and enjoy the moment.</p>
  <blockquote class="cv-quote">&ldquo;Sometimes, you simply need a space to pause, breathe deeply, meet new people and leave feeling a little lighter.&rdquo;</blockquote>
 </div>
 <aside class="cv-who" aria-labelledby="who-title">
  <p class="eyebrow">WHO IS IT FOR?</p>
  <h2 id="who-title">Come as you are.</h2>
  <p><strong>Women &amp; Couples are welcome.</strong> Whether you want to slow down, reconnect, meet new people, explore wellness, enjoy good food or simply dance freely &mdash; there is space for you at The Sphere.</p>
  <ul class="cv-pillars"><li>WELLNESS</li><li>NOURISH</li><li>MUSIC</li><li>COMMUNITY</li></ul>
 </aside>
</section>

<section id="experience" class="cv-experience" aria-labelledby="experience-title">
 <div class="cv-heading"><div><p class="eyebrow">THE EXPERIENCE</p><h2 id="experience-title">Come for the experience.<br>Stay for the feeling.</h2></div>
 <p>An evening thoughtfully brought together around well-being, community and celebration.</p></div>
 <ul class="cv-offer">{offer}</ul>
 <div class="cv-moments">{moments}</div>
 <p class="cv-photo-note">Moments from The Sphere’s past gatherings.</p>
</section>

<section class="cv-interlude" aria-label="Together at The Sphere"><img src="/assets/sphere-circle-session-1920.webp" srcset="/assets/sphere-circle-session-1200.webp 1200w, /assets/sphere-circle-session-1920.webp 1920w" sizes="100vw" alt="A facilitator leading a seated circle beside singing bowls" width="1920" height="1280" loading="lazy" decoding="async"><div><p class="eyebrow">A LITTLE LESS RUSH. A LITTLE MORE YOU.</p><p>Come as you are.<br>Leave a little lighter.</p></div></section>

<section id="schedule" class="cv-schedule" aria-labelledby="schedule-title">
 <div class="cv-schedule-side">
  <p class="eyebrow">YOUR EVENING</p><h2 id="schedule-title">A little preview<br>of your day.</h2>
  <ul class="cv-facts">
   <li>{icon('calendar')}{date}</li>
   <li>{icon('clock')}{time}</li>
   <li>{icon('pin')}{place}</li>
  </ul>
 </div>
 <ol class="cv-timeline">{schedule}</ol>
</section>

<section id="tickets" class="cv-tickets" aria-labelledby="tickets-title">
 <div class="cv-tickets-copy">
  <p class="eyebrow">TICKETS</p>
  <h2 id="tickets-title">Choose your moment<br>to join us.</h2>
  <p>Your ticket to an evening of wellness, connection, nourishing food and celebration.</p>
  <p class="cv-welcome">{icon('people')}Women &amp; Couples Welcome</p>
 </div>
 <div class="cv-ticket">
  <div class="cv-ticket-top">
   <p class="eyebrow">ENTRY TICKET</p>
   <p class="cv-price">{price}</p>
   <p class="cv-price-note">{escape(ev['price_note'])}</p>{ticket_note}
  </div>
  <ul class="cv-facts">
   <li>{icon('calendar')}{date}</li>
   <li>{icon('clock')}{time}</li>
   <li>{icon('pin')}{place}</li>
  </ul>
  <div class="cv-ticket-action">{ticket_action(ev)}</div>
 </div>
</section>

<section id="faq" class="cv-faq" aria-labelledby="faq-title">
 <div class="cv-faq-side"><p class="eyebrow">GOOD TO KNOW</p><h2 id="faq-title">Frequently asked<br>questions.</h2></div>
 <div class="cv-questions">{faqs(ev)}</div>
</section>

<section class="cv-close">
 <p class="eyebrow">{escape(ev['name']).upper()}</p>
 <h2>Your next chapter can begin<br>with a pause.</h2>
 <p>Come slow down. Come connect. Come celebrate.</p>
 <p class="cv-close-meta">{date} &nbsp;&bull;&nbsp; {place} &nbsp;&bull;&nbsp; {time}</p>
 <p data-book><a class="cv-button" href="{a(book)}">Reserve Your Spot {arrow()}</a></p>
</section>
</main>
<div class="event-bar" data-event-bar aria-hidden="true">
 <p class="cv-bar-price"><strong>{price}</strong><span>{escape(ev['price_note'])}</span></p>
 <a class="cv-button" href="{a(book) if ev['mode'] != 'soon' else '#tickets'}" tabindex="-1">{'View tickets' if ev['mode'] == 'soon' else 'Book Your Experience'} <span aria-hidden="true">{'↓' if ev['mode'] == 'soon' else '&#8599;'}</span></a>
</div>"""


# ---------------------------------------------------------------- assembly

def seo(ev, path, title):
 image = url('/assets/sphere-bowls-1200.webp')
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
 head = head.replace('width=device-width,initial-scale=1', 'width=device-width,initial-scale=1,viewport-fit=cover')
 head = re.sub(r'<meta name="theme-color"[^>]*>', '<meta name="theme-color" content="#24302a">', head, count=1)
 head = head.replace('</script>', '</script>\n  <link rel="stylesheet" href="/'+ev['slug']+'/event.css?v=5">\n  <script src="/'+ev['slug']+'/event.js?v=5" defer></script>', 1)
 shell = re.search(r'<a class="skip".*?<main id="main">', home, re.S)[0].removesuffix('<main id="main">')
 # On the event page the header's call to action is the ticket itself.
 shell = shell.replace(f'href="{ev["path"]}" data-event-until', f'href="{ev["path"]}" aria-current="page" data-event-until')
 footer = re.search(r'<footer>.*?</footer>', home, re.S)[0]
 invitation = re.search(r'<dialog id="invitation-dialog".*?</dialog>', home, re.S)[0]
 # Hash links borrowed from the home page point back to it; the event's own in-page links stay on this page.
 home_links = lambda part: part.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"').replace('href="/#tickets"', 'href="#tickets"')
 shell, footer, invitation = home_links(shell), home_links(footer), home_links(invitation)
 html = f'<!doctype html><html lang="en-IN"><head>{head}{seo(ev, path, title)}</head><body class="event-page">{shell}\n{body}{footer}{invitation}</body></html>'
 html = re.sub(r'(href|src|srcset)="(assets/|style.css|brand.css|premium.css|site.js|motion.js)', r'\1="/\2', html)
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
 print(f"Built {ev['path']} ({ev['mode']} booking mode, {'montage' if has_montage() or (ROOT/'dist/assets/montage-carnival/wide.mp4').exists() else 'photo'} hero).")


def retire(folder):
 # Links shared on WhatsApp and Instagram keep working after the event: they land on the home page.
 if not folder.exists():
  return
 shutil.rmtree(folder)
 folder.mkdir()
 (folder/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  '<meta http-equiv="refresh" content="0;url=/"><title>The Sphere</title><meta name="robots" content="noindex,follow"></head>'
  '<body><a href="/">Enter The Sphere</a></body></html>')
 print(f'Retired /{folder.name}/ to a redirect.')
