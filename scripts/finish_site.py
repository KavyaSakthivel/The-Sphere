"""Shared editorial finishing pass, excluding the historical palette studies."""
from pathlib import Path
import re,json,base64,math
ROOT=Path(__file__).resolve().parents[1]
COVERS=['sphere-sound-session','sphere-meditation','sphere-connection','sphere-rest','sphere-smile']
STAR='<svg class="journal-star" viewBox="0 0 24 24" width="28" height="28" aria-hidden="true" focusable="false"><path d="M12 2.6l2.8 5.7 6.3.9-4.55 4.45 1.07 6.27L12 16.97l-5.62 2.95 1.07-6.27L2.9 9.2l6.3-.9z"/></svg>'
# Pages that close with the "Stay close" inbox, as the homepage does.
INBOX_PAGES={'experiences','membership','philosophy'}
NAV_TARGETS={'philosophy':'/philosophy/','experiences':'/experiences/','membership':'/membership/','carnival':'/carnival/'}

def current_page(s,where):
 """Mark the navigation link for the page being viewed, in the header and the mobile menu."""
 target=NAV_TARGETS.get(where) or ('/#journal' if where.startswith('journal') else None)
 if not target: return s
 def mark(m):
  return m[0].replace(f'<a href="{target}"',f'<a href="{target}" aria-current="page"').replace(f'<a class="carnival-nav" href="{target}"',f'<a class="carnival-nav" href="{target}" aria-current="page"')
 s=re.sub(r'<header.*?</header>',mark,s,count=1,flags=re.S)
 return re.sub(r'<nav id="mobile-nav".*?</nav>',mark,s,count=1,flags=re.S)

def founder_section():
 """Our story's founder chapter, written only from data/founder.json; absent until it is filled in."""
 f=json.loads((ROOT/'data/founder.json').read_text())
 if not (f.get('name') and f.get('paragraphs')): return ''
 from html import escape as e
 photo=''
 if f.get('photo'):
  photo=f'<figure class="founder-photo"><img src="/assets/{e(f["photo"],quote=True)}" alt="{e(f.get("photo_alt") or f["name"],quote=True)}" loading="lazy" decoding="async"></figure>'
 quote=f'<blockquote class="founder-quote">“{e(f["quote"])}”</blockquote>' if f.get('quote') else ''
 role=f'<p class="founder-role">{e(f["role"])}</p>' if f.get('role') else ''
 creds=f'<p class="founder-credentials">{e(f["credentials"])}</p>' if f.get('credentials') else ''
 body=''.join(f'<p>{e(x)}</p>' for x in f['paragraphs'])
 return (f'<section id="founder" class="story-founder{" has-photo" if photo else ""}" aria-labelledby="founder-name">{photo}'
  f'<div class="founder-head"><p class="eyebrow">{e(f.get("label") or "THE FOUNDER")}</p><h2 id="founder-name">{e(f["name"])}</h2>{creds}{role}</div>'
  f'<div class="founder-text">{quote}{body}</div></section>')

def build():
 entries=json.loads((ROOT/'data/journal.json').read_text())
 home=(ROOT/'dist/index.html').read_text()
 found=re.search(r'<section id="inbox".*?</section>',home,re.S)
 inbox=found[0] if found else ''
 founder_html=founder_section()
 for page in (ROOT/'dist').rglob('index.html'):
  if 'palette-study' in page.parts: continue
  s=page.read_text()
  if '<header' not in s: continue
  where=page.relative_to(ROOT/'dist').parent.as_posix()
  if where in INBOX_PAGES and 'id="inbox"' not in s and inbox:
   s=s.replace('</main>',inbox+'</main>',1)
  if where=='philosophy' and founder_html:
   s=s.replace('<section class="story-chapter" id="chapter-11"',founder_html+'<section class="story-chapter" id="chapter-11"',1)
  s=current_page(s,where)
  s=re.sub(r'<dialog[^>]*data-carnival-popup.*?</dialog>','',s,flags=re.S)
  s=re.sub(r'<div class="intro-end".*?</div>','',s,flags=re.S)
  s=re.sub(r'<figcaption>A LITTLE ROOM TO SIMPLY BE</figcaption>','',s)
  s=s.replace('<span>PEACE. PURPOSE. CONNECTION.</span>','')
  s=re.sub(r'(<p class="eyebrow"[^>]*>)\d+\s*/\s*',r'\1',s)
  s=re.sub(r'(<p class="eyebrow"[^>]*>)0\d\s*/\s*',r'\1',s)
  s=re.sub(r'<p class="form-small">This is the inbox list.*?</p>','',s,flags=re.S)
  s=re.sub(r'\s*<br\s*/?>\s*',' <br> ',s)
  s=s.replace('Stay <em>close.</em>','Stay close.')
  s=re.sub(r'(<button class="menu-toggle"[^>]*>.*?)<span aria-hidden="true">\+</span>',r'\1<span aria-hidden="true">☰</span>',s,count=1,flags=re.S)
  # Keep one authentic photograph beside each short journal preview.
  def journal(m):
   body=m[0]; slug=re.search(r'/journal/([^/]+)/',body)[1]
   idx=next((i for i,e in enumerate(entries) if e['slug']==slug),0)
   body=re.sub(r'<span class="journal-number">.*?</span>',STAR,body)
   return body
  s=re.sub(r'<a class="journal-entry".*?</a>',journal,s,flags=re.S)
  # Arrow meaning follows destination, not decoration.
  def arrows(m):
   arrow='→' if 'data-invitation' in m[0] else ('↗' if re.search(r'href="https?://',m[0]) else ('↓' if re.search(r'href="(?:/)?#',m[0]) else '→'))
   return re.sub(r'↗(?:&#xFE0E;|\ufe0e)?',arrow,m[0])
  s=re.sub(r'<a\b[^>]*>.*?</a>',arrows,s,flags=re.S)
  s=re.sub(r'(<button\b[^>]*>.*?</button>)',lambda m:re.sub(r'↗(?:&#xFE0E;|\ufe0e)?','→',m[0]),s,flags=re.S)
  # Remove photo-overlay copy, retaining the full-width hero film headline.
  s=s.replace('class="photo-opening-copy"','class="photo-opening-copy reading-opening-copy"')
  # Hide unavailable booking actions while retaining existing booking-open copy.
  if 'carnival' in page.parts:
   from build_event import load
   if load()['mode']=='soon':
    s=re.sub(r'<p data-book>.*?</p>','',s,flags=re.S)
    s=re.sub(r'<a[^>]*data-book[^>]*>.*?</a>','',s,flags=re.S)
  def logo(m):
   return re.sub(r'wordmark-sage.svg','wordmark-ink.svg',m[0])
  s=re.sub(r'<header.*?</header>',logo,s,flags=re.S)
  s=re.sub(r'<img[^>]*src="[^"]*wordmark-(ink|ivory)\.svg"[^>]*>',lambda m:'<picture><source media="(max-width:700px)" srcset="/assets/brand/wordmark-'+m[1]+'-compact.svg">'+m[0]+'</picture>',s)
  # Tiny blurred previews are prebuilt from the same authentic image.
  def preview(m):
   block=m[0];img=re.search(r'<img[^>]*src="([^"]+)"',block)
   if not img: return block
   name=Path(img[1].split('?')[0]).stem
   tiny=ROOT/'dist/assets/previews'/f'{name}.webp'
   if tiny.exists():
    data=base64.b64encode(tiny.read_bytes()).decode()
    block=block.replace('>',f' style="background-image:url(data:image/webp;base64,{data});background-size:cover;background-position:center;">',1)
   return block
  s=re.sub(r'<figure\b[^>]*>.*?</figure>',preview,s,flags=re.S)
  s=s.replace('</head>','<link rel="stylesheet" href="/finish.css"></head>')
  s="\n".join(line.rstrip() for line in s.splitlines())+"\n"
  page.write_text(s)
 (ROOT/'dist/finish.css').write_text((ROOT/'templates/finish.css').read_text())
