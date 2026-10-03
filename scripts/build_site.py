from pathlib import Path
from html import escape
import re, json
from seo import apply_seo, build_articles, build_discovery, CONFIG, url
import build_event
ROOT=Path(__file__).resolve().parents[1]
journal_data=json.loads((ROOT/'data/journal.json').read_text())
heads=['THE SPHERE','A SPACE THAT FEELS LIKE YOURS','WHY THE SPHERE?','THE SPHERE EXPERIENCE','MORE THAN WELLNESS','CURATED EXPERIENCES','IS WELLNESS A LUXURY OR A NECESSITY?','THE WOMEN OF THE SPHERE','A PRIVATE CIRCLE','THE SPHERE JOURNAL','A NOTE FROM THE SPHERE']
sections={}
for line in (ROOT/'notes/content.txt').read_text().splitlines():
 line=line.strip()
 if not line:continue
 if line in heads:key=line;sections[key]=[]
 else:sections[key].append(line)
def t(s,i):return escape(sections[heads[s]][i])
def ps(s,ids):return ''.join('<p>'+t(s,i)+'</p>' for i in ids)
def group(s,ids):return '<p>'+' '.join(t(s,i) for i in ids)+'</p>'
def label(s,prefix=''):return '<p class="eyebrow">'+prefix+escape(heads[s])+'</p>'
# Membership enquiries and inbox signups post to the club's own address.
ENDPOINT='https://formsubmit.co/'+CONFIG['form_endpoint']
REPLY_PROMISE='We read every note ourselves and reply within two days.'
AUTORESPONSE=("Thank you for writing to The Sphere.\n\n"
 "Your note has reached us and one of us will reply personally within two days, "
 "with a little more about the circle and the gatherings coming up.\n\n"
 "Until then you are welcome to meet us on Instagram @thespherewomen.\n\n"
 "With warmth,\nThe Sphere\nCoimbatore")
INBOX_AUTORESPONSE=("Thank you for joining the inbox of The Sphere.\n\n"
 "You will hear from us only when it matters: early word on gatherings, "
 "a gentle reminder to pause, and the occasional note from the circle.\n\n"
 "If you would like to enquire about membership, simply reply to this email.\n\n"
 "With warmth,\nThe Sphere\nCoimbatore")
def attr(v):return escape(v,quote=True)
def hidden(kind,autoresponse):
 # FormSubmit reads these to label the email, auto-reply, and catch bots.
 return (f'<input type="hidden" name="_subject" value="The Sphere — new {kind}">'
  '<input type="hidden" name="_template" value="table">'
  '<input type="hidden" name="_captcha" value="false">'
  f'<input type="hidden" name="_next" value="{attr(url("/thank-you/"))}">'
  f'<input type="hidden" name="_autoresponse" value="{attr(autoresponse)}">'
  f'<input type="hidden" name="Came from" value="The Sphere website — {escape(kind)}">'
  '<input class="sphere-honey" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">')
enquiry_form=(f'<form class="sphere-form" data-sphere-form="enquiry" action="{attr(ENDPOINT)}" method="POST" novalidate>'
 +hidden('membership enquiry',AUTORESPONSE)+
 '<div class="field"><label for="enquiry-name">Your name</label>'
 '<input id="enquiry-name" name="Name" type="text" required autocomplete="name" placeholder="First and last name"></div>'
 '<div class="field"><label for="enquiry-email">Email</label>'
 '<input id="enquiry-email" name="email" type="email" required autocomplete="email" inputmode="email" placeholder="you@example.com"></div>'
 '<div class="field"><label for="enquiry-phone">WhatsApp <span class="optional">optional</span></label>'
 '<input id="enquiry-phone" name="WhatsApp" type="tel" autocomplete="tel" inputmode="tel" placeholder="+91"></div>'
 '<div class="field"><label for="enquiry-note">What brings you to The Sphere? <span class="optional">optional</span></label>'
 '<textarea id="enquiry-note" name="Message" rows="3" placeholder="A line or two is plenty."></textarea></div>'
 '<label class="consent"><input type="checkbox" name="Consent" value="Yes — happy to be contacted" required>'
 '<span>Yes, The Sphere may email or message me about membership and gatherings.</span></label>'
 '<button class="button button-dark" type="submit">Send my enquiry <span aria-hidden="true">↗</span></button>'
 '<p class="form-status" role="status" aria-live="polite"></p></form>')
inbox_form=(f'<form class="sphere-form sphere-form-inline" data-sphere-form="inbox" action="{attr(ENDPOINT)}" method="POST" novalidate>'
 +hidden('inbox signup',INBOX_AUTORESPONSE)+
 '<div class="field"><label for="inbox-email">Email address</label>'
 '<input id="inbox-email" name="email" type="email" required autocomplete="email" inputmode="email" placeholder="you@example.com"></div>'
 '<button class="button button-dark" type="submit">Join the list <span aria-hidden="true">↗</span></button>'
 '<p class="form-status" role="status" aria-live="polite"></p></form>')
html=(ROOT/'templates/original-index.html').read_text()
# Restore the original composition and integrate the complete source into it.
html=re.sub(r'<p class="hero-description">.*?</p>',f'<p class="hero-description">{t(0,1)}</p>',html,count=1)
intro=f'''<section class="club-introduction section-pad">{label(0)}<h2>{t(0,2)}</h2><p>{t(0,3)}</p><div class="ritual-lines">{ps(0,range(4,10))}</div></section>'''
html=html.replace('  <section id="philosophy"',intro+'\n  <section id="philosophy"',1)
philosophy=f'''<section id="philosophy" class="philosophy section-pad">{label(1,'01 / ')}<div class="philosophy-main"><h2>Wellness,<br><em>beyond the usual.</em></h2><div class="prose">{ps(1,[1])}{group(1,range(2,7))}{ps(1,[7,8])}</div></div></section>'''
html=re.sub(r'<section id="philosophy".*?</section>',lambda _:philosophy,html,flags=re.S,count=1)
why=f'''<section class="why section-pad">{label(2)}<p class="why-subtitle">{t(2,0)}</p><h2>{t(2,1)} {t(2,2)} {t(2,3)}<br>{t(2,4)} {t(2,5)} {t(2,6)}<br><em>{t(2,8)}</em></h2>{ps(2,[7])}{group(2,range(9,12))}</section>'''
html=re.sub(r'<section class="why.*?</section>',lambda _:why,html,flags=re.S,count=1)
pillars=''
for i in range(4,8):
 name,copy=sections[heads[3]][i].split(':',1)
 pillars+=f'<article><span class="pillar-number">0{i-3}</span><h3>{escape(name.strip().title())}</h3><p>{escape(copy.strip())}</p></article>'
offerings=''
for i in range(2,7):
 name,copy=sections[heads[5]][i].split(':',1)
 offerings+=f'<details{" open" if i==2 else ""}><summary>{escape(name.strip())} <span aria-hidden="true">+</span></summary><p>{escape(copy.strip())}</p></details>'
experience=f'''<section id="experiences" class="experiences section-pad"><div class="section-heading"><div>{label(3,'02 / ')}<h2>Curated, <em>not crowded.</em></h2></div><p>{t(3,1)}<br>{t(3,2)}</p></div><p class="pillar-intro">{t(3,3)}</p><div class="pillars">{pillars}</div><div class="more-wellness"><div>{label(4)}<h3>A community built<br>around <em>experiences.</em></h3></div><div class="prose">{ps(4,[1,2])}{group(4,[3,4])}</div></div><div class="experience-detail"><figure><img src="assets/session-circle-1200.webp" srcset="assets/session-circle-640.webp 640w, assets/session-circle-1200.webp 1200w" sizes="(max-width: 700px) 86vw, 42vw" alt="Women seated in meditation on green mats during a Sphere session" loading="lazy" width="1200" height="800"><figcaption>MORE THAN WHAT YOU DO. IT’S WHAT YOU FEEL.</figcaption></figure><div>{label(5)}<h3>Every gathering<br>has a <em>purpose.</em></h3><p class="experience-intro">{t(5,1)}</p><div class="experience-list">{offerings}</div></div></div></section>'''
html=re.sub(r'<section id="experiences".*?</section>',lambda _:experience,html,flags=re.S,count=1)
necessity=f'''<section class="necessity"><div class="necessity-photo"><img src="assets/session-sound-1200.webp" srcset="assets/session-sound-640.webp 640w, assets/session-sound-1200.webp 1200w" sizes="(max-width: 700px) 100vw, 49vw" alt="A facilitator plays singing bowls while participants rest on their mats" loading="lazy" width="1200" height="800"></div><div class="necessity-copy">{label(6)}<h2>Taking care of yourself<br>isn’t a luxury.<br><em>It’s a necessity.</em></h2><p class="source-statement">{t(6,0)}</p>{ps(6,[1])}{group(6,range(2,5))}{ps(6,[5])}</div></section>'''
html=re.sub(r'<section class="necessity".*?</section>',lambda _:necessity,html,flags=re.S,count=1)
community=f'''<section class="community section-pad">{label(7,'03 / ')}<h2>Different lives.<br><em>Shared values.</em></h2>{ps(7,[1,2])}{group(7,[3,4])}<div class="values"><span>Curious.</span><span>Intentional.</span><span>Open.</span><span>Evolving.</span></div></section>'''
html=re.sub(r'<section class="community.*?</section>',lambda _:community,html,flags=re.S,count=1)
invitation=f'''<section id="invitation" class="invitation section-pad"><div class="invitation-brand"><img src="assets/brand/circle-lockup.svg" alt="The Sphere logo encircled by its signature organic rings" loading="lazy" width="1080" height="1080"><p>you belong in your life.</p></div><div class="invitation-copy">{label(8)}<h2>Intentionally<br><em>intimate.</em></h2>{ps(8,[1,2])}{group(8,[3,4])}<button class="button button-dark" data-invitation>Request an Invitation <span aria-hidden="true">↗</span></button><p class="invitation-small">Your first step into The Sphere.</p><p class="venue-note">The circle gathers once a month, usually in the first week. Venue details are shared by email or WhatsApp.</p></div></section>'''
html=re.sub(r'<section id="invitation".*?</section>',lambda _:invitation,html,flags=re.S,count=1)
steps=[('Write to us','Send a short note through the invitation form: your name, your email, and whatever you would like us to know. A line or two is plenty.'),
 ('We reply, personally','One of us reads every note and answers within two days &mdash; by email, or on WhatsApp if you have left a number.'),
 ('We meet, then you join','A conversation first, so the circle fits both ways. Venue and gathering details follow by email or WhatsApp.')]
joining=('<section id="joining" class="joining section-pad" aria-labelledby="joining-title">'
 '<div class="section-heading"><div><p class="eyebrow">HOW JOINING WORKS</p>'
 '<h2 id="joining-title">Three steps,<br><em>no forms to chase.</em></h2></div>'
 '<p>Membership is by invitation, so it begins with a conversation rather than a checkout.</p></div>'
 '<ol class="joining-steps">'
 +''.join(f'<li><span class="joining-number">0{i}</span><h3>{name}</h3><p>{copy}</p></li>'
  for i,(name,copy) in enumerate(steps,1))+
 '</ol><p class="joining-cta"><button class="button button-dark" data-invitation>Request an invitation <span aria-hidden="true">&#8599;</span></button></p></section>')
html=html.replace('<section id="journal"',joining+'<section id="journal"',1)
# Upcoming gatherings come from a published Google Sheet; the static copy stands in until then.
gatherings=('<section id="gatherings" class="gatherings section-pad" aria-labelledby="gatherings-title"'
 f' data-gatherings="{attr(CONFIG.get("gatherings_csv",""))}">'
 '<div class="section-heading"><div><p class="eyebrow">WHAT IS COMING UP</p>'
 '<h2 id="gatherings-title">The next <em>gathering.</em></h2></div>'
 '<p>The circle meets once a month, usually in the first week.</p></div>'
 '<div class="gatherings-body"><p class="gatherings-quiet">Dates and venues are shared with members '
 'by email and WhatsApp. <a href="#invitation" data-invitation aria-haspopup="dialog">'
 'Request an invitation <span aria-hidden="true">&#8599;</span></a></p></div></section>')
html=html.replace('<section id="journal"',gatherings+'<section id="journal"',1)
entries=''
for i in range(1,11,2):
 slug=journal_data[(i-1)//2]['slug']
 entries+=f'<a class="journal-entry" href="/journal/{slug}/" data-entry="{(i-1)//2}" aria-label="Read {t(9,i)}"><span class="journal-number">0{(i+1)//2}</span><span class="journal-title">{t(9,i)}</span><span class="journal-subtitle">{t(9,i+1)}</span><span class="journal-arrow" aria-hidden="true">↗</span></a>'
journal=f'''<section id="journal" class="journal section-pad"><div class="section-heading"><div>{label(9,'04 / ')}<h2>Room for <em>thought.</em></h2></div><p>{t(9,0)}</p></div><div class="journal-list">{entries}</div></section>'''
html=re.sub(r'<section id="journal".*?</section>',lambda _:journal,html,flags=re.S,count=1)
note=f'''<section class="note section-pad">{label(10)}<h2>“We wanted to create<br>a space to <em>simply be.</em>”</h2>{ps(10,[0,1])}<p class="note-pause">{t(10,2)}<br>{t(10,3)}<br>{t(10,4)}</p>{group(10,[5,6])}{ps(10,[7])}<p class="note-signoff">{t(10,8)} {t(10,9)}<br>{t(10,10)}</p><span class="signature">The Sphere</span></section>'''
html=re.sub(r'<section class="note.*?</section>',lambda _:note,html,flags=re.S,count=1)
dialog=('<dialog id="invitation-dialog" aria-labelledby="invitation-title">'
 '<button class="dialog-close" aria-label="Close invitation">×</button>'
 '<p class="eyebrow">YOUR PLACE IN THE CIRCLE</p>'
 '<h2 id="invitation-title">It begins with<br><em>a hello.</em></h2>'
 f'<p>Tell us a little about yourself and what brings you to The Sphere. {REPLY_PROMISE}</p>'
 +enquiry_form+
 '<p class="dialog-or"><span>or</span></p>'
 '<a class="dialog-instagram" href="https://www.instagram.com/thespherewomen/" target="_blank" rel="noopener noreferrer">Meet us on Instagram <span aria-hidden="true">↗</span></a>'
 f'<p class="dialog-small">Your details come straight to The Sphere\u2019s own inbox. We use them only to reply to you, and we never share or sell them.</p></dialog>')
html=re.sub(r'<dialog id="invitation-dialog".*?</dialog>',lambda _:dialog,html,flags=re.S,count=1)
inbox=('<section id="inbox" class="inbox section-pad">'
 '<p class="eyebrow">WELLNESS IN YOUR INBOX</p>'
 '<h2>Stay <em>close.</em></h2>'
 '<p class="inbox-intro">Early word on gatherings, gentle reminders to pause, and the occasional '
 'note from the circle. Sent rarely. Never shared.</p>'
 +inbox_form+
 '<p class="form-small">This is the inbox list, not a membership application. '
 'Joining it asks us to email you about The Sphere; one line back and we stop.<br>'
 '<a class="form-small-link" href="#invitation" data-invitation aria-haspopup="dialog">'
 'Looking to join the club itself? Request an invitation <span aria-hidden="true">↗</span></a></p></section>')
html=html.replace('</main>',inbox+'</main>',1)
# The club's own session footage replaces the landscape photograph once scripts/build_montage.py has run.
# Posters are each cut's first frame, so the photograph-to-video handover is invisible; site.js decides
# whether to play at all (reduced motion and data saving keep the still).
MONTAGE=ROOT/'dist/assets/montage'
if all((MONTAGE/f).exists() for f in ('wide.mp4','wide.webm','wide-poster.jpg','tall.mp4','tall.webm','tall-poster.jpg')):
 hero_media=('<div class="hero-visual has-montage"><picture><source media="(max-width: 700px)" srcset="assets/montage/tall-poster.jpg">'
  '<img src="assets/montage/wide-poster.jpg" alt="" fetchpriority="high" width="1600" height="900"></picture>'
  '<video class="hero-montage" muted loop playsinline preload="none" aria-hidden="true" data-montage '
  'data-wide-webm="assets/montage/wide.webm" data-wide-mp4="assets/montage/wide.mp4" '
  'data-tall-webm="assets/montage/tall.webm" data-tall-mp4="assets/montage/tall.mp4"></video></div>'
  # Outside the video layer, so the headline block can never sit on top of the control.
  '<button class="montage-toggle" type="button" hidden>Pause</button>')
 html=re.sub(r'<div class="hero-visual">.*?</div>',lambda _:hero_media,html,count=1,flags=re.S)
# A one-off event (data/event.json) adds a hero note, a nav link and a featured gathering.
html=build_event.feature_home(html,build_event.load())
html=apply_seo(html)
html=html.replace('</main>', '</main><script type="application/json" id="journal-data">'+json.dumps(journal_data,ensure_ascii=False).replace('<','\\u003c')+'</script>',1)
(ROOT/'dist/index.html').write_text(html)
build_articles(html,journal_data)
build_discovery(journal_data)
build_event.build(html)
# Where the form lands when JavaScript is unavailable and FormSubmit redirects back.
head=re.search(r'<head>(.*?)</head>',html,re.S)[1]
shell=re.search(r'<a class="skip".*?<main id="main">',html,re.S)[0].removesuffix('<main id="main">')
footer=re.search(r'<footer>.*?</footer>',html,re.S)[0]
thanks=f'''<!doctype html><html lang="en-IN"><head>{head}</head><body>{shell}
<main id="main"><section class="thank-you section-pad"><p class="eyebrow">YOUR PLACE IN THE CIRCLE</p>\
<h1>Thank you for<br><em>writing to us.</em></h1>\
<p>Your note has reached The Sphere. {REPLY_PROMISE} A confirmation is on its way to your inbox \
&mdash; if you do not see it, it may be resting in your promotions or spam folder.</p>\
<a class="button button-dark" href="/">Back to The Sphere <span aria-hidden="true">&#8599;</span></a>\
</section></main>{footer}{dialog}</body></html>'''
thanks=re.sub(r'(href|src)="(assets/|style.css|brand.css|site.js)',r'\1="/\2',thanks)
thanks=thanks.replace('href="#','href="/#').replace('href="/#main"','href="#main"')
thanks=re.sub(r'<link rel="canonical"[^>]*>','',thanks,count=1)
thanks=re.sub(r'<meta name="robots"[^>]*>','<meta name="robots" content="noindex,follow">',thanks,count=1)
thanks=re.sub(r'<script type="application/ld\+json">.*?</script>','',thanks,flags=re.S,count=1)
thanks=re.sub(r'<title>.*?</title>','<title>Thank you | The Sphere</title>',thanks,count=1)
thanks=re.sub(r'<meta property="og:title"[^>]*>','<meta property="og:title" content="Thank you | The Sphere">',thanks,count=1)
(ROOT/'dist/thank-you').mkdir(parents=True,exist_ok=True)
(ROOT/'dist/thank-you/index.html').write_text(thanks)
# Keep links from the interim four-page version working.
for route,target in [('experience','experiences'),('circle','invitation'),('journal','journal')]:
 (ROOT/'dist'/route/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=/#{target}"><title>The Sphere</title><meta name="robots" content="noindex,follow"></head><body><a href="/#{target}">Enter The Sphere</a></body></html>')
# Version every stylesheet and script link by its content, so a returning visitor's browser can never
# keep a stale copy after an update (and the files can be cached for a long time in between).
import hashlib
def stamp(page):
 html=page.read_text()
 def version(m):
  path=m.group(1)
  target=ROOT/'dist'/path.lstrip('/') if path.startswith('/') else page.parent/path
  if not target.exists(): return m.group(0)
  return f'{path}?v={hashlib.sha256(target.read_bytes()).hexdigest()[:10]}"'
 page.write_text(re.sub(r'((?:/|\.\./)*[\w/.-]*\.(?:css|js))(?:\?v=[^"]*)?"',version,html))
for page in (ROOT/'dist').rglob('*.html'):
 stamp(page)
print('Restored the original single-page design with all 11 source sections.')
