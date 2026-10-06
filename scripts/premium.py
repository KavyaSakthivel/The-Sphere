"""Compose the quieter home page; keep the client's complete source on /philosophy/."""
from pathlib import Path
from html import escape
import re
from seo import CONFIG, url, org
import json
from datetime import datetime
from build_event import load, full_date, hours

ROOT = Path(__file__).resolve().parents[1]

EXPERIENCE_PHOTOS = [
    ('session-movement-960.webp', 'Mindful movement at a Sphere gathering'),
    ('session-sound-1920.webp', 'Sound healing at a Sphere gathering'),
    ('editorial-journal-1200.webp', 'A quiet moment of reading and reflection'),
    ('editorial-making-1200.webp', 'Two women exploring pottery together'),
    ('session-group-960.webp', 'Three women sharing a conversation at The Sphere'),
]


def photo(filename, alt, eager=False):
    return f'<figure class="editorial-photo" data-image-reveal><img src="/assets/{filename}" alt="{escape(alt, quote=True)}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async"></figure>'


def experience_atlas(articles):
    cards = []
    for i, article in enumerate(re.findall(r'<article>.*?</article>', articles, re.S)):
        filename, alt = EXPERIENCE_PHOTOS[i]
        title = re.search(r'<h3>(.*?)</h3>', article, re.S)[1]
        body = re.search(r'<p>.*?</p>', article, re.S)[0]
        cards.append(f'<article class="atlas-card" id="practice-{i+1}">{photo(filename, alt)}<div class="atlas-copy" data-reveal><p class="eyebrow">0{i+1} / THE SPHERE EXPERIENCE</p><h3>{title}</h3>{body}</div></article>')
    return '<div class="experience-atlas">'+''.join(cards)+'</div>'


def experience_browser(articles):
    """Progressively enhanced pillars: readable in full when JavaScript is unavailable."""
    labels = ['Move', 'Pause', 'Reflect', 'Discover', 'Connect']
    tabs, panels = [], []
    for i, article in enumerate(re.findall(r'<article>.*?</article>', articles, re.S)):
        filename, alt = EXPERIENCE_PHOTOS[i]
        title = re.search(r'<h3>(.*?)</h3>', article, re.S)[1]
        body = re.search(r'<p>.*?</p>', article, re.S)[0]
        tabs.append(f'<button type="button" id="pillar-tab-{i}" aria-controls="pillar-panel-{i}">{labels[i]}</button>')
        panels.append(f'<article class="pillar-panel" id="pillar-panel-{i}">{photo(filename, alt)}<div class="pillar-copy"><p class="eyebrow">0{i+1} / THE SPHERE EXPERIENCE</p><h3>{title}</h3>{body}<a class="text-link" href="/experiences/#practice-{i+1}">Explore this experience <span aria-hidden="true">↗</span></a></div></article>')
    return '<div class="pillar-browser" data-pillar-browser><div class="pillar-tabs" aria-label="Explore the wellness experiences" hidden>'+''.join(tabs)+'</div>'+''.join(panels)+'</div>'


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
    main = re.sub(r'<div class="experience-gallery">.*?</div>', experience_browser(offerings), main, flags=re.S)
    main = re.sub(r'<div class="discover-line".*?</div>', '', main, flags=re.S)
    main = re.sub(r'<details class="experience-directory".*?</details>', '<a class="text-link experience-page-link" href="/experiences/">Explore the experiences <span aria-hidden="true">↗</span></a>', main, flags=re.S)
    main = re.sub(r'<section class="home-letter\b[^\"]*".*?</section>', '', main, flags=re.S)
    main = re.sub(r'<div class="membership-notes".*?</dl></div>', '<div class="membership-notes" data-reveal><p>A small circle. A monthly rhythm.<br>A personal conversation first.</p><a class="text-link" href="/membership/">Discover membership <span aria-hidden="true">↗</span></a></div>', main, flags=re.S)
    main = re.sub(r'<details id="joining".*?</details>', '', main, flags=re.S)
    main = main.replace('<section id="invitation" class="home-invitation section-pad">', '<section id="invitation" class="home-invitation section-pad">'+photo('editorial-flowers-1200.webp', 'Flowers in soft afternoon light, an invitation to slow down'))
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
              <div class="carnival-popup-layout"><div class="carnival-popup-photo"><img src="/assets/session-circle-1200.webp" alt="Women gathering together at The Sphere" width="1200" height="800"></div>
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
    membership = re.search(r'<section id="invitation".*?</section>', full_main, re.S)[0]
    letter = re.search(r'<section class="home-letter\b[^\"]*".*?</section>', full_main, re.S)[0]
    for slug, title, description, body in [
        ('experiences', 'The experiences', 'Movement, sound healing, mindfulness and meaningful connection. Explore the thoughtfully curated experiences at The Sphere, Coimbatore.', experience),
        ('membership', 'Your place in the circle', 'An intentionally intimate women’s wellness circle in Coimbatore. Discover the monthly rhythm and how to request an invitation to The Sphere.', membership + letter),
    ]:
        page_head = re.sub(r'<title>.*?</title>', '<title>'+title+' | The Sphere</title>', head)
        page_head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="'+escape(description, quote=True)+'">', page_head)
        meta = f'<link rel="canonical" href="{url("/"+slug+"/")}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:title" content="{title} | The Sphere"><meta property="og:url" content="{url("/"+slug+"/")}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:image" content="{url("/assets/session-together-1920.webp")}">'
        graph = {'@context':'https://schema.org','@graph':[org(),{'@type':'WebPage','url':url('/'+slug+'/'),'name':title+' | The Sphere'}]}
        opening_photo = ('session-sound-1920.webp', 'A sound-healing experience with women at The Sphere') if slug == 'experiences' else ('session-together-1920.webp', 'Women coming together in The Sphere circle')
        opening = f'<section class="subpage-opening photo-opening">{photo(*opening_photo, eager=True)}<div class="photo-opening-copy"><p class="eyebrow">THE SPHERE / {slug.upper()}</p><h1>{title}.</h1><a class="text-link light-link" href="#'+('experiences' if slug == 'experiences' else 'invitation')+'">Discover more <span aria-hidden="true">↓</span></a></div></section>'
        html = f'<!doctype html><html lang="en-IN"><head>{page_head}{meta}<script type="application/ld+json">{json.dumps(graph,ensure_ascii=False)}</script></head><body class="premium-home club-subpage">{shell}<main id="main">{opening}{body}</main>{footer}{dialog}</body></html>'
        html = re.sub(r'(href|src)="(assets/|style.css|brand.css|premium.css|site.js|motion.js)', r'\1="/\2', html)
        html = html.replace('srcset="assets/', 'srcset="/assets/').replace(', assets/', ', /assets/')
        html = html.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"')
        html = html.replace('href="/#experiences"', 'href="#experiences"') if slug == 'experiences' else html.replace('href="/#invitation">Discover more', 'href="#invitation">Discover more')
        path = ROOT/'dist'/slug; path.mkdir(exist_ok=True)
        (path/'index.html').write_text(html)


def build_philosophy(home, sections, heads):
    head = re.search(r'<head>(.*?)</head>', home, re.S)[1]
    head = re.sub(r'<title>.*?</title>', '<title>Our philosophy | The Sphere</title>', head)
    head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="The ideas behind The Sphere: an intimate women’s wellness circle in Coimbatore, created around movement, stillness and meaningful connection.">', head)
    shell = re.search(r'<a class="skip".*?<main id="main">', home, re.S)[0].removesuffix('<main id="main">')
    footer = re.search(r'<footer>.*?</footer>', home, re.S)[0]
    dialog = re.search(r'<dialog id="invitation-dialog".*?</dialog>', home, re.S)[0]
    chapters = []
    imagery = [
        ('session-together-1920.webp', 'Women seated together in a Sphere sound-healing circle'),
        ('editorial-flowers-1200.webp', 'Sunlight falling on flowers and a ceramic vase'),
        ('editorial-journal-1200.webp', 'A woman taking a quiet moment to read'),
        ('session-movement-960.webp', 'Grounded movement at a Sphere gathering'),
        ('session-group-960.webp', 'Women connecting in conversation at The Sphere'),
        ('editorial-making-1200.webp', 'Women learning a creative practice together'),
        ('misty-meadow-1920.webp', 'A peaceful meadow beneath softly misted mountains'),
        ('session-connection-960.webp', 'A woman sharing her perspective in the circle'),
        ('session-circle-1200.webp', 'An intimate meditation circle at The Sphere'),
        ('editorial-reading-1200.webp', 'A woman reading and making time for herself'),
        ('session-bowls-1200.webp', 'Singing bowls and a cushion prepared for a moment of stillness'),
    ]
    for i, heading in enumerate(heads):
        lines = sections[heading]
        # This reading page preserves the complete supplied document without crowding the opening.
        paragraphs = ''
        for line in lines:
            if line == '[Enter The Sphere]':
                paragraphs += '<p><a class="text-link" href="/experiences/">Enter The Sphere <span aria-hidden="true">↗</span></a></p>'
            elif line == '[Request an Invitation]':
                paragraphs += '<p><button class="text-link" data-invitation>Request an invitation <span aria-hidden="true">↗</span></button></p>'
            else:
                paragraphs += '<p>' + escape(line) + '</p>'
        if heading != 'THE SPHERE JOURNAL':
            paragraphs = re.sub(r'(?:<p>[^<]{1,68}</p>){3,}', lambda m: '<p class="story-mantra">'+''.join('<span>'+line+'</span>' for line in re.findall(r'<p>(.*?)</p>', m[0]))+'</p>', paragraphs)
        if heading == 'CURATED EXPERIENCES':
            articles = ''.join('<article><h3>'+escape(line.split(':',1)[0].strip())+'</h3><p>'+escape(line.split(':',1)[1].strip())+'</p></article>' for line in lines[2:])
            chapters.append(f'<section class="story-practices" id="curated-experiences"><div class="story-practices-heading" data-reveal><p class="eyebrow">{i+1:02} / {heading}</p><h2>{escape(lines[0])}</h2><p>{escape(lines[1])}</p></div>{experience_atlas(articles)}</section>')
        else:
            filename, alt = imagery[i]
            title = heading.capitalize().replace('sphere', 'Sphere')
            chapters.append(f'<section class="story-chapter" id="chapter-{i+1}">{photo(filename, alt)}<div class="story-chapter-copy" data-reveal><p class="eyebrow">{i+1:02} / OUR PHILOSOPHY</p><h2>{escape(title)}</h2><div class="story-prose">{paragraphs}</div></div></section>')
    html = f'''<!doctype html><html lang="en-IN"><head>{head}
    <link rel="canonical" href="{url('/philosophy/')}">
    <meta name="robots" content="index,follow,max-image-preview:large">
    <meta property="og:title" content="Our philosophy | The Sphere">
    <meta property="og:url" content="{url('/philosophy/')}">
    <meta property="og:description" content="A space for the woman behind every role she carries.">
    <script type="application/ld+json">{json.dumps({'@context':'https://schema.org', '@graph':[org(), {'@type':'WebPage','url':url('/philosophy/'),'name':'Our philosophy | The Sphere','about':{'@id':url('/#organization')}}]}, ensure_ascii=False)}</script>
    </head><body class="story-page">{shell}<main id="main"><section class="story-opening"><div class="story-opening-copy"><a class="text-link" href="/">← The Sphere</a><p class="eyebrow">OUR PHILOSOPHY</p><h1>A space to<br>simply be.</h1><p>The thoughts behind the circle.</p><a class="text-link" href="#chapter-1">Discover our story <span aria-hidden="true">↓</span></a></div>{photo('editorial-flowers-1200.webp','A sunlit floral arrangement in soft, earthy colours',True)}</section>{''.join(chapters)}<div class="story-close"><p class="eyebrow">YOUR PLACE IN THE CIRCLE</p><h2>Come as you are.</h2><button class="text-link" data-invitation>Request an invitation <span aria-hidden="true">↗</span></button></div></main>{footer}{dialog}</body></html>'''
    html = re.sub(r'(href|src)="(assets/|style.css|brand.css|premium.css|site.js|motion.js)', r'\1="/\2', html)
    html = html.replace('href="#', 'href="/#').replace('href="/#main"', 'href="#main"').replace('href="/#chapter-', 'href="#chapter-')
    path = ROOT / 'dist/philosophy'; path.mkdir(exist_ok=True)
    (path / 'index.html').write_text(html)
