"""Compose the quieter home page; keep the client's complete source on /philosophy/."""
from pathlib import Path
from html import escape
import re
from seo import CONFIG, url, org
import json
from datetime import datetime
from build_event import load, full_date, hours

ROOT = Path(__file__).resolve().parents[1]

# Every photograph on the site is used once. The home pillars and the Experiences page show
# different moments from the club's own sessions.
# The home page shows the PDF's four elements (Move, Pause, Connect, Discover); the Experiences page
# shows the five curated experiences, so the two sections no longer repeat each other.
ELEMENT_PHOTOS = [
 ('sphere-move-reach-1200.webp','Women reaching their arms overhead in a standing stretch at a Sphere movement class'),
 ('sphere-rest-bowls-1920.webp','Women resting beside singing bowls during sound healing'),
 ('sphere-laughter-1200.webp','Women sharing a laugh at a Sphere gathering'),
 ('sphere-hands-bowls-1200.webp','A woman playing singing bowls with mallets, laid out on a woven mat'),
]
# Each element points at the experience on the Experiences page that is closest to it.
ELEMENT_LINKS = ['/experiences/#practice-1', '/experiences/#practice-2', '/experiences/#practice-5', '/experiences/#practice-4']
ATLAS_PHOTOS = [
 ('sphere-meditation-1200.webp','Women seated on their mats at a Sphere gathering'),
 ('sphere-bowls-cushion-1200.webp','Singing bowls and a cushion laid out for sound healing'),
 ('sphere-talk-reflect-1200.webp','Women talking in the studio, with sound instruments laid out on the floor'),
 ('sphere-explore-1200.webp','Women seated on the studio floor, listening during a Sphere session'),
 ('sphere-connection-1200.webp','Women seated in pairs connecting at a Sphere gathering'),
]


def photo(filename, alt, eager=False):
    stem = re.sub(r'-(640|1200|1920)\.webp$', '', filename)
    responsive = f' srcset="/assets/{stem}-640.webp 640w, /assets/{stem}-1200.webp 1200w, /assets/{stem}-1920.webp 1920w" sizes="(max-width: 700px) 100vw, 60vw"' if stem.startswith('sphere-') else ''
    if stem.startswith('editorial-'):
        responsive = f' srcset="/assets/{stem}-640.webp 640w, /assets/{stem}-1200.webp 1200w" sizes="(max-width: 700px) 100vw, 60vw"'
    treatment = ' aesthetic-photo' if stem.startswith('editorial-') else ''
    return f'<figure class="editorial-photo{treatment}" data-image-reveal><img src="/assets/{filename}"{responsive} alt="{escape(alt, quote=True)}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async"></figure>'


def experience_atlas(articles):
    cards = []
    for i, article in enumerate(re.findall(r'<article>.*?</article>', articles, re.S)):
        filename, alt = ATLAS_PHOTOS[i]
        title = re.search(r'<h3>(.*?)</h3>', article, re.S)[1]
        body = re.search(r'<p>.*?</p>', article, re.S)[0]
        cards.append(f'<article class="atlas-card" id="practice-{i+1}">{photo(filename, alt)}<div class="atlas-copy" data-reveal><p class="eyebrow">0{i+1} / THE SPHERE EXPERIENCE</p><h3>{title}</h3>{body}</div></article>')
    return '<div class="experience-atlas">'+''.join(cards)+'</div>'


def experience_elements():
    """The four elements and their descriptions, exactly as written in the client's source (notes/content.txt)."""
    lines = (ROOT / 'notes/content.txt').read_text().splitlines()
    start = lines.index('THE SPHERE EXPERIENCE')
    block = [l.strip() for l in lines[start+1:start+10] if l.strip()]
    lead = block[3]
    elements = [tuple(part.strip() for part in line.split(':', 1)) for line in block[4:8]]
    return block[1], block[2], lead, elements


def element_cards():
    """All four elements at once, as cards: nothing is hidden behind a tab and the section stays compact."""
    _, _, _, elements = experience_elements()
    cards = []
    for i, (name, copy) in enumerate(elements):
        name = name.title()
        filename, alt = ELEMENT_PHOTOS[i]
        cards.append(f'<article class="element-card" data-reveal>{photo(filename, alt)}<div class="element-copy"><p class="element-number">0{i+1}</p><h3>{name}</h3><p>{escape(copy)}</p><a class="text-link" href="{ELEMENT_LINKS[i]}">Explore this experience <span aria-hidden="true">↗</span></a></div></article>')
    return '<div class="elements-grid">'+''.join(cards)+'</div>'


def render_home(html):
    main = (ROOT / 'templates/premium-main.html').read_text()
    entries = re.search(r'<div class="journal-list">(.*?)</div>', html, re.S)[1]
    event = load()
    inbox = re.search(r'<section id="inbox".*?</section>', html, re.S)[0]
    offerings = re.search(r'<div class="experience-list">(.*?)</div>', html, re.S)[1]
    # One disclosure for the extended list, with its descriptions immediately readable.
    offerings = re.sub(r'<details(?: open)?>\s*<summary>(.*?)\s*<span.*?</span></summary>(.*?)</details>',
                       r'<article><h3>\1</h3>\2</article>', offerings, flags=re.S)
    for token, value in {
        '@JOURNAL_ENTRIES@': entries,
        '@EVENT_FEATURE@': '',
        '@INBOX@': inbox,
        '@OFFERINGS@': offerings,
        '@GATHERINGS_CSV@': escape(CONFIG.get('gatherings_csv', ''), quote=True),
    }.items():
        main = main.replace(token, value)
    main = main.replace('<figure>', '<figure data-image-reveal>')
    full_main = main
    # The homepage introduces the club; practical detail lives on focused reading pages.
    intimate, belief, lead, _ = experience_elements()
    intro = f'<div class="elements-intro" data-reveal><p>{escape(intimate)}<br>{escape(belief)}</p><p class="elements-lead">{escape(lead)}</p></div>'
    main = re.sub(r'<p data-reveal>We believe meaningful experiences happen.*?</p>', lambda _: intro, main, count=1, flags=re.S)
    main = re.sub(r'<div class="experience-gallery">.*?</div>', lambda _: element_cards(), main, flags=re.S)
    main = re.sub(r'<div class="discover-line".*?</div>', '', main, flags=re.S)
    main = re.sub(r'<details class="experience-directory".*?</details>', '', main, flags=re.S)
    main = re.sub(r'<section class="home-letter\b[^\"]*".*?</section>', '', main, flags=re.S)
    main = re.sub(r'<div class="membership-notes".*?</dl></div>', '<div class="membership-notes" data-reveal><p>A small circle. A monthly rhythm.<br>A personal conversation first.</p><a class="text-link" href="/membership/">Discover membership <span aria-hidden="true">↗</span></a></div>', main, flags=re.S)
    main = re.sub(r'<details id="joining".*?</details>', '', main, flags=re.S)
    main = re.sub(r'^[ \t]+$', '', main, flags=re.M)
    if not CONFIG.get('gatherings_csv'):
        main = re.sub(r'[ \t]*<section id="gatherings".*?</section>', '', main, flags=re.S)
    else:
        main = main.replace('AN OPEN INVITATION', 'WHAT IS COMING UP').replace('Beyond the circle.', 'The next gathering.')
        main = main.replace('A public experience from The Sphere.<br>A different way to meet us.', 'The circle gathers once a month.<br>Details shared with members, personally.')
    html = re.sub(r'<main id="main">.*?</main>', lambda _: main, html, count=1, flags=re.S)
    html = html.replace('class="landing-page"', 'class="landing-page premium-home"')
    html = re.sub(r'<footer>.*?</footer>', lambda m: m[0].replace('wordmark-ivory.svg', 'wordmark-sage.svg'), html, flags=re.S, count=1)
    # Seasonal promotion lives only in the entry dialog, outside the permanent home content.
    html = re.sub(r'<div class="header-actions"><a class="header-event".*?</a>(.*?)</div>',
                  r'\1', html, flags=re.S, count=1)
    html = re.sub(r'<a[^>]*data-event-until="[^"]*"[^>]*>Wellness Carnival</a>', '', html)
    html = html.replace('href="#experiences"', 'href="/experiences/"')
    # Header navigation goes to the full story; the hero can still introduce it in-page.
    html = re.sub(r'(<nav[^>]*(?:desktop-nav|mobile-nav)[^>]*>)(.*?)(</nav>)', lambda m: m[1]+m[2].replace('href="#philosophy"','href="/philosophy/"')+m[3], html, flags=re.S)
    if event and event.get('show_on_home'):
        until = event.get('promotion_until', event['end'])
        if datetime.now(datetime.fromisoformat(until).tzinfo) < datetime.fromisoformat(until):
            link = f'<a class="carnival-nav" href="{event["path"]}" data-event-until="{escape(until, quote=True)}">Carnival</a>'
            html = re.sub(r'(<nav[^>]*(?:desktop-nav|mobile-nav)[^>]*>)(.*?)(</nav>)', lambda m: m[1]+m[2]+link+m[3], html, flags=re.S)
    # Balanced navigation around the wordmark, with one clear invitation action.
    seasonal = re.search(r'<a class="carnival-nav".*?</a>', html)
    seasonal = seasonal[0] if seasonal else ''
    html = re.sub(r'<nav class="desktop-nav".*?</nav>', '<nav class="desktop-nav" aria-label="Discover The Sphere"><a href="/philosophy/">Our story</a><a href="/experiences/">Experiences</a><a href="/#journal">Journal</a></nav>', html, count=1, flags=re.S)
    html = re.sub(r'(<a class="header-invite".*?</a>)', lambda m: '<div class="nav-right"><nav class="desktop-nav secondary-nav" aria-label="Join The Sphere"><a href="/membership/">Membership</a>'+seasonal+'</nav>'+m[1]+'</div>', html, count=1, flags=re.S)
    html = re.sub(r'<nav id="mobile-nav".*?</nav>', '<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden><p class="eyebrow">DISCOVER THE SPHERE</p><a href="/philosophy/">Our story</a><a href="/experiences/">Experiences</a><a href="/membership/">Membership</a><a href="/#journal">Journal</a>'+seasonal+'<a href="/#invitation" data-invitation aria-haspopup="dialog">Request an invitation ↗</a></nav>', html, count=1, flags=re.S)
    build_subpages(html, full_main)
    if event and event.get('show_on_home'):
        until = event.get('promotion_until', event['end'])
        if datetime.now(datetime.fromisoformat(until).tzinfo) < datetime.fromisoformat(until):
            popup = f'''<dialog id="carnival-dialog" class="carnival-popup" aria-labelledby="carnival-popup-title" aria-describedby="carnival-popup-description" data-carnival-popup data-promotion-until="{escape(until, quote=True)}" data-promotion-key="{escape(event['slug'] + event['start'], quote=True)}">
              <button type="button" class="dialog-close carnival-close" aria-label="Close carnival invitation">×</button>
              <div class="carnival-popup-layout"><div class="carnival-popup-photo"><img src="/assets/sphere-circle-1200.webp" alt="Women gathering together at The Sphere" width="1200" height="800"></div>
              <div class="carnival-popup-copy"><p class="eyebrow">AN INVITATION TO COME TOGETHER</p><p class="carnival-popup-brand">The Sphere presents</p><h2 id="carnival-popup-title">Wellness<br>Carnival.</h2><p id="carnival-popup-description">{escape(event['tagline'])}</p>
              <div class="carnival-popup-details"><p>{full_date(event['start_at'])} · {hours(event)}</p><p>{escape(event['venue'])}, {escape(event['city'])}</p><p>{escape(event['audience'])}</p></div>
              <a class="carnival-popup-cta" href="{event['path']}">Discover the carnival <span aria-hidden="true">↗</span></a><button type="button" class="carnival-continue" data-dismiss-carnival>Continue to The Sphere</button></div></div></dialog>'''
            html = html.replace('</body>', popup + '</body>')
    return html


def build_subpages(home, full_main):
    head = re.search(r'<head>(.*?)</head>', home, re.S)[1]
    shell = re.search(r'<a class="skip".*?<main id="main">', home, re.S)[0].removesuffix('<main id="main">')
    footer = re.search(r'<footer>.*?</footer>', home, re.S)[0]
    dialog = re.search(r'<dialog id="invitation-dialog".*?</dialog>', home, re.S)[0]
    experience = re.search(r'<section id="experiences".*?</section>', full_main, re.S)[0]
    directory = re.search(r'<div class="directory-grid">(.*?)</div>', experience, re.S)[1]
    experience = re.sub(r'<div class="experience-gallery">.*?</div>', '', experience, flags=re.S)
    experience = re.sub(r'<div class="discover-line".*?</div>', '', experience, flags=re.S)
    experience = re.sub(r'<details class="experience-directory".*?</details>', experience_atlas(directory), experience, flags=re.S)
    experience = re.sub(r'<h2>Curated\.<br><span class="accent">Not crowded\.</span></h2>', '<h2>Every gathering<br>has a purpose.</h2>', experience, count=1)
    experience = re.sub(r'<p data-reveal>We believe meaningful experiences happen.*?</p>', '<p data-reveal>Our experiences are designed to create moments that stay with you.</p>', experience, count=1, flags=re.S)
    more = ('<section class="more-wellness-story" aria-labelledby="more-title">'
     + photo('sphere-buddha-garden-1200.webp', 'A Buddha figure among plants at The Sphere')
     + '<div class="st-copy"><p class="eyebrow">MORE THAN WELLNESS</p><h2 id="more-title">A community built<br>around experiences.</h2>'
     '<p class="st-lead">At The Sphere, you might begin your morning with yoga, discover the grounding power of Kalaripayattu, experience the stillness of sound healing, or explore a completely new form of movement.</p>'
     '<p>You might sit across from a woman you’ve never met and leave with a conversation you’ll never forget.</p>'
     '<p class="st-emphasis">Because sometimes wellness isn’t about what you do.<br>It’s about what you feel.</p></div></section>')
    experience = experience + more
    membership = re.search(r'<section id="invitation".*?</section>', full_main, re.S)[0]
    # Membership shows its own circle photograph rather than the homepage's.
    steps = re.findall(r'<li><span>(\d+)</span><div><h3>(.*?)</h3><p>(.*?)</p></div></li>', membership)
    membership = re.sub(r'\s*<details id="joining".*?</details>', '', membership, flags=re.S)
    joining = ('<section id="joining" class="join-steps" aria-labelledby="joining-title"><h2 id="joining-title">How joining works.</h2><ol>'
        + ''.join(f'<li><span class="join-number">{n}</span><h3>{h}</h3><p>{t}</p></li>' for n, h, t in steps)
        + '</ol><button class="soft-hero-cta join-cta" type="button" data-invitation aria-haspopup="dialog">Request an invitation <span aria-hidden="true">→</span></button></section>')
    membership = membership + joining
    membership = membership.replace('sphere-intimate-', 'sphere-facilitator-rest-').replace('A small circle of women meditating together around singing bowls at The Sphere', 'A facilitator seated among singing bowls as women rest')
    letter = re.search(r'<section class="home-letter\b[^\"]*".*?</section>', full_main, re.S)[0]
    for slug, title, description, body in [
        ('experiences', 'The experiences', 'Movement, sound healing, mindfulness and meaningful connection. Explore the thoughtfully curated experiences at The Sphere, Coimbatore.', experience),
        ('membership', 'Your place in the circle', 'An intentionally intimate women’s wellness circle in Coimbatore. Discover the monthly rhythm and how to request an invitation to The Sphere.', membership + letter),
    ]:
        page_head = re.sub(r'<title>.*?</title>', '<title>'+title+' | The Sphere</title>', head)
        page_head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="'+escape(description, quote=True)+'">', page_head)
        meta = f'<link rel="canonical" href="{url("/"+slug+"/")}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:title" content="{title} | The Sphere"><meta property="og:url" content="{url("/"+slug+"/")}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:image" content="{url("/assets/sphere-connection-1920.webp")}">'
        graph = {'@context':'https://schema.org','@graph':[org(),{'@type':'WebPage','url':url('/'+slug+'/'),'name':title+' | The Sphere'}]}
        if slug == 'experiences':
            opening = (f'<section class="soft-hero" aria-labelledby="opening-title">{photo("sphere-soft-bowls-1920.webp", "Singing bowls in soft focus at The Sphere", eager=True)}'
                '<div class="soft-hero-copy"><p class="eyebrow">THE SPHERE / EXPERIENCES</p><h1 id="opening-title">The experiences.</h1>'
                '<a class="soft-hero-link" href="#experiences">Discover more <span aria-hidden="true">↓</span></a></div></section>')
        else:
            opening = (f'<section class="soft-hero soft-hero-centred" aria-labelledby="opening-title">{photo("sphere-soft-circle-1920.webp", "A circle of women gathered at The Sphere, in soft focus", eager=True)}'
                '<div class="soft-hero-copy"><p class="eyebrow">THE SPHERE / MEMBERSHIP</p><h1 id="opening-title">Your place in the circle.</h1>'
                '<button class="soft-hero-cta" type="button" data-invitation aria-haspopup="dialog">Request an invitation <span aria-hidden="true">→</span></button></div></section>')
        html = f'<!doctype html><html lang="en-IN"><head>{page_head}{meta}<script type="application/ld+json">{json.dumps(graph,ensure_ascii=False)}</script></head><body class="premium-home club-subpage">{shell}<main id="main">{opening}{body}</main>{footer}{dialog}</body></html>'
        html = re.sub(r'(href|src)="(assets/|style.css|brand.css|premium.css|site.js|motion.js)', r'\1="/\2', html)
        html = html.replace('srcset="assets/', 'srcset="/assets/').replace(', assets/', ', /assets/')
        html = html.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"')
        html = html.replace('href="/#experiences"', 'href="#experiences"') if slug == 'experiences' else html
        path = ROOT/'dist'/slug; path.mkdir(exist_ok=True)
        (path/'index.html').write_text(html)


def build_philosophy(home, sections, heads):
    head = re.search(r'<head>(.*?)</head>', home, re.S)[1]
    head = re.sub(r'<title>.*?</title>', '<title>Our story | The Sphere</title>', head)
    head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="The ideas behind The Sphere: an intimate women’s wellness circle in Coimbatore, created around movement, stillness and meaningful connection.">', head)
    shell = re.search(r'<a class="skip".*?<main id="main">', home, re.S)[0].removesuffix('<main id="main">')
    footer = re.search(r'<footer>.*?</footer>', home, re.S)[0]
    dialog = re.search(r'<dialog id="invitation-dialog".*?</dialog>', home, re.S)[0]
    # Our story is curated, not the whole document: the founder first, then only the three ideas
    # that appear nowhere else on the site. Every line is the client's own (notes/content.txt);
    # sections already told on Home, Experiences, Membership or the Journal are not repeated here.
    why, belief, necessity = sections[heads[2]], sections[heads[1]], sections[heads[6]]
    p = lambda line, cls='': f'<p{" class=" + chr(34) + cls + chr(34) if cls else ""}>{escape(line)}</p>'
    roles = ''.join(f'<li>{escape(line)}</li>' for line in why[1:7])
    mantra = ''.join(f'<li>{escape(line)}</li>' for line in belief[2:7])
    story = (
        '<div data-founder-slot></div>'
        f'<section class="st-why" id="why" aria-labelledby="why-title"><p class="eyebrow">{escape(heads[2])}</p>'
        f'<h2 id="why-title">{escape(why[0])}</h2><ul class="st-roles">{roles}</ul>'
        f'<div class="st-why-close">{p(why[7])}{p(why[8])}{p(why[9], "st-emphasis")}</div></section>'
        f'<section class="st-belief" aria-labelledby="belief-title">{photo("sphere-meditation-circle-1200.webp", "Women seated together in a quiet meditation circle at The Sphere")}'
        f'<div class="st-copy"><p class="eyebrow">{escape(heads[1])}</p><h2 id="belief-title">{escape(belief[0])}</h2>'
        f'{p(belief[1], "st-lead")}<ul class="st-mantra">{mantra}</ul>{p(belief[7])}</div></section>'
        f'<section class="st-necessity" aria-labelledby="necessity-title"><div class="st-copy"><p class="eyebrow">{escape(heads[6])}</p>'
        f'<h2 id="necessity-title">{escape(necessity[0])}</h2>{p(necessity[1], "st-lead")}'
        f'<p>{escape(necessity[2])} {escape(necessity[3])} {escape(necessity[4])}</p>{p(necessity[5], "st-emphasis")}</div>'
        f'{photo("sphere-necessity-1200.webp", "Women seated in quiet meditation on green mats at The Sphere")}</section>'
    )
    html = f'''<!doctype html><html lang="en-IN"><head>{head}
    <link rel="canonical" href="{url('/philosophy/')}">
    <meta name="robots" content="index,follow,max-image-preview:large">
    <meta property="og:title" content="Our story | The Sphere">
    <meta property="og:url" content="{url('/philosophy/')}">
    <meta property="og:description" content="A space for the woman behind every role she carries.">
    <script type="application/ld+json">{json.dumps({'@context':'https://schema.org', '@graph':[org(), {'@type':'WebPage','url':url('/philosophy/'),'name':'Our story | The Sphere','about':{'@id':url('/#organization')}}]}, ensure_ascii=False)}</script>
    </head><body class="story-page">{shell}<main id="main"><section class="soft-hero" aria-labelledby="story-title">{photo('sphere-soft-garden-1920.webp','Leaves and a Buddha figure in soft focus at The Sphere',True)}<div class="soft-hero-copy"><p class="eyebrow">OUR STORY</p><h1 id="story-title">A space to<br>simply be.</h1><p>The thoughts behind the circle.</p></div></section>{story}<section class="soft-band" aria-labelledby="close-title">{photo('sphere-soft-rest-1920.webp','Women resting together at The Sphere, in soft focus')}<div class="soft-hero-copy"><p class="eyebrow">YOUR PLACE IN THE CIRCLE</p><h2 id="close-title">Come as you are.</h2><button class="soft-hero-cta" type="button" data-invitation aria-haspopup="dialog">Request an invitation <span aria-hidden="true">→</span></button></div></section></main>{footer}{dialog}</body></html>'''
    html = re.sub(r'(href|src)="(assets/|style.css|brand.css|premium.css|site.js|motion.js)', r'\1="/\2', html)
    html = html.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"').replace('href="/#chapter-', 'href="#chapter-')
    path = ROOT / 'dist/philosophy'; path.mkdir(exist_ok=True)
    (path / 'index.html').write_text(html)
