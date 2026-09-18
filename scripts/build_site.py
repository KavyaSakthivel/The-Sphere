from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
heads = ['THE SPHERE','A SPACE THAT FEELS LIKE YOURS','WHY THE SPHERE?','THE SPHERE EXPERIENCE','MORE THAN WELLNESS','CURATED EXPERIENCES','IS WELLNESS A LUXURY OR A NECESSITY?','THE WOMEN OF THE SPHERE','A PRIVATE CIRCLE','THE SPHERE JOURNAL','A NOTE FROM THE SPHERE']
sections = {}
for line in (ROOT/'notes/content.txt').read_text().splitlines():
    line = line.strip()
    if not line: continue
    if line in heads:
        key = line
        sections[key] = []
    else: sections[key].append(line)

def t(section, index): return escape(sections[heads[section]][index])
def label(section): return f'<p class="eyebrow">{escape(heads[section])}</p>'
def ps(section, indices): return ''.join(f'<p>{t(section,i)}</p>' for i in indices)
def h(section, index, tag='h2', emphasis=None):
    text=t(section,index)
    if emphasis: text=text.replace(escape(emphasis),f'<em>{escape(emphasis)}</em>')
    return f'<{tag}>{text}</{tag}>'
def button(text,url): return f'<a class="button button-dark" href="{url}">{text}<span aria-hidden="true">↗</span></a>'

old=(ROOT/'dist/index.html').read_text()
favicon=re.search(r'<link rel="icon"[^>]+>',old).group()
navs=[('/', 'THE SPHERE'),('/experience/','THE SPHERE EXPERIENCE'),('/journal/','THE SPHERE JOURNAL')]
def page(path,title,body):
    nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if url==path else '')+f'>{name.title()}</a>' for url,name in navs)
    mark='<span>THE</span>sphere<span class="wordmark-dot">°</span>'
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — The Sphere</title><meta name="description" content="{t(0,2)}"><meta name="theme-color" content="#f5f3eb">{favicon}<link rel="stylesheet" href="/style.css"><script src="/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="header"><a class="wordmark" href="/" aria-label="The Sphere home">{mark}</a><nav class="desktop-nav" aria-label="Main navigation">{nav}</nav><a class="header-invite" href="/circle/"{' aria-current="page"' if path=='/circle/' else ''}>Request an Invitation <span aria-hidden="true">↗</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav">Menu <span aria-hidden="true">+</span></button></header>
<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden>{nav}<a href="/circle/">A Private Circle</a></nav>
<main id="main">{body}</main>
<footer><div class="footer-top"><a class="wordmark" href="/" aria-label="The Sphere home">{mark}</a><p>{t(0,0)}</p><a href="https://www.instagram.com/thespherewomen/" target="_blank" rel="noopener noreferrer" aria-label="The Sphere on Instagram (opens in a new tab)">@thespherewomen ↗</a></div><nav class="footer-nav" aria-label="Footer navigation">{nav}<a href="/circle/">A Private Circle</a></nav><div class="footer-bottom"><span>© <span id="year">2026</span> The Sphere</span><a href="#main">↑ <span class="sr-only">Back to top</span></a></div></footer></body></html>'''
    out=ROOT/'dist'/path.strip('/')/'index.html'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(html)

home=f'''<section class="hero source-hero" aria-labelledby="hero-title"><div class="hero-copy">{label(0)}<h1 id="hero-title">Crafted calm<br>for the <em>modern<br>woman.</em></h1><p class="hero-description">{t(0,1)}</p>{button('Enter The Sphere','#philosophy')}<div class="hero-bottom"><span class="tiny-circle" aria-hidden="true"></span><p>{t(10,8)}<br>{t(10,9)}</p><a href="#philosophy" aria-label="A space that feels like yours">↓</a></div></div><div class="hero-visual"><img src="/assets/forest.jpg" alt="Sunlight filtering through a quiet forest" fetchpriority="high" width="1600" height="2400"><div class="orbital" aria-hidden="true"><i></i><i></i><i></i></div><p class="image-note">{t(10,2)}<br><em>{t(10,4)}</em></p></div></section>
<section class="opening section-pad"><h2>{t(0,2)}</h2><p>{t(0,3)}</p><div class="ritual-lines">{ps(0,range(4,10))}</div></section>
<section id="philosophy" class="philosophy section-pad">{label(1)}<div class="philosophy-main">{h(1,0,emphasis='beyond the usual.')}<div class="prose">{ps(1,[1])}<p>{' '.join(t(1,i) for i in range(2,7))}</p>{ps(1,[7,8])}</div></div></section>
<section class="why section-pad">{label(2)}{h(2,0,emphasis='just for her.')}<p class="roles">{' '.join(t(2,i) for i in range(1,7))}</p>{ps(2,[7])}<p class="role-return">{t(2,8)}</p>{ps(2,range(9,12))}</section>
<section class="necessity"><div class="necessity-photo"><img src="/assets/ritual.jpg" alt="A ceramic cup of tea in soft afternoon light" loading="lazy" width="1200" height="800"></div><div class="necessity-copy">{label(6)}{h(6,0,emphasis='a necessity.')}{ps(6,range(1,6))}</div></section>
<section class="note section-pad">{label(10)}<div class="note-intro">{ps(10,[0,1])}</div><h2>{t(10,2)}<br>{t(10,3)}<br><em>{t(10,4)}</em></h2>{ps(10,range(5,8))}<p class="note-signoff">{t(10,8)}<br>{t(10,9)}</p><p class="signature">{t(10,10)}</p></section>'''
page('/',sections[heads[0]][0],home)

pillars=''
for i in range(4,8):
    name,copy=sections[heads[3]][i].split(':',1)
    pillars+=f'<article><span class="pillar-number">0{i-3}</span><h3>{escape(name.strip().title())}</h3><p>{escape(copy.strip())}</p></article>'
experiences=''
for i in range(2,7):
    name,copy=sections[heads[5]][i].split(':',1)
    experiences+=f'<article class="offering"><h3>{escape(name.strip())}</h3><p>{escape(copy.strip())}</p></article>'
experience=f'''<section id="experiences" class="experiences section-pad page-opening">{label(3)}{h(3,0,'h1',emphasis='not crowded.')}<div class="experience-preface">{ps(3,range(1,4))}</div><div class="pillars">{pillars}</div></section>
<section class="more-wellness section-pad"><div class="experience-detail"><figure><img src="/assets/together.jpg" alt="Two women talking with yoga mats" loading="lazy" width="1400" height="933"></figure><div>{label(4)}{h(4,0,emphasis='experiences.')}<div class="prose">{ps(4,range(1,5))}</div></div></div></section>
<section class="curated section-pad">{label(5)}{h(5,0,emphasis='a purpose.')}<p class="curated-intro">{t(5,1)}</p><div class="offerings">{experiences}</div></section>'''
page('/experience/','The Sphere Experience',experience)

circle=f'''<section class="community section-pad page-opening">{label(7)}{h(7,0,'h1',emphasis='Shared values.')}{ps(7,range(1,5))}<p class="values">{t(7,5)}</p></section>
<section id="invitation" class="invitation section-pad"><div class="invitation-mark" aria-hidden="true"><span></span><span></span><span></span><em>{t(10,8)}</em></div><div class="invitation-copy">{label(8)}{h(8,0,emphasis='intimate.')}{ps(8,range(1,5))}<a class="button button-dark" href="https://www.instagram.com/thespherewomen/" target="_blank" rel="noopener noreferrer" aria-label="Request an Invitation through The Sphere on Instagram (opens in a new tab)">Request an Invitation <span aria-hidden="true">↗</span></a></div></section>'''
page('/circle/','A Private Circle',circle)

entries=''
for i in range(1,11,2):
    entries+=f'<article class="journal-entry"><span class="journal-number">0{(i+1)//2}</span><h2 class="journal-title">{t(9,i)}</h2><p class="journal-subtitle">{t(9,i+1)}</p></article>'
journal=f'''<section id="journal" class="journal section-pad page-opening"><p class="eyebrow">THE SPHERE</p><h1>The Sphere <em>Journal</em></h1><p class="journal-intro">{t(9,0)}</p><div class="journal-list">{entries}</div></section>'''
page('/journal/','The Sphere Journal',journal)
print('Built 4 pages from the supplied content.')
