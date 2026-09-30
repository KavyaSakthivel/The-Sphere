"""Build SEO metadata and crawlable journal pages from confirmed brand content."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse
import json,re
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'data/site.json').read_text())
BASE=CONFIG['url'].rstrip('/')
assert urlparse(BASE).scheme=='https' and urlparse(BASE).netloc and not urlparse(BASE).path, 'Set the confirmed HTTPS origin in data/site.json'

def url(path='/'):
 return BASE+path

def org():
 return {'@type':'Organization','@id':url('/#organization'),'name':CONFIG['name'], 'url':url(), 'description':CONFIG['description'], 'logo':url('/assets/brand/circle-lockup.svg'), 'sameAs':[CONFIG['instagram']], 'areaServed':{'@type':'City','name':CONFIG['city'],'containedInPlace':{'@type':'AdministrativeArea','name':CONFIG['region']}}}

def apply_seo(html,entry=None):
 path='/' if entry is None else '/journal/'+entry['slug']+'/'
 title=CONFIG['title'] if entry is None else entry['title']+' | The Sphere Journal'
 description=CONFIG['description'] if entry is None else entry['subtitle']
 html=re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>',html,count=1)
 html=re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="'+escape(description,quote=True)+'">',html,count=1)
 website={'@type':'WebSite','@id':url('/#website'),'url':url(),'name':CONFIG['name'],'inLanguage':'en-IN','publisher':{'@id':url('/#organization')}}
 page={'@type':'WebPage','@id':url(path+'#webpage'),'url':url(path),'name':title,'description':description,'inLanguage':'en-IN','isPartOf':{'@id':url('/#website')},'about':{'@id':url('/#organization')}}
 graph=[org(),website,page]
 if entry:
  graph.append({'@type':'Article','@id':url(path+'#article'),'headline':entry['title'],'description':entry['subtitle'],'articleSection':'The Sphere Journal','inLanguage':'en-IN','mainEntityOfPage':{'@id':url(path+'#webpage')},'author':{'@id':url('/#organization')},'publisher':{'@id':url('/#organization')},'articleBody':'\n\n'.join(entry['paragraphs'])})
  graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'The Sphere','item':url()},{'@type':'ListItem','position':2,'name':entry['title'],'item':url(path)}]})
 structured=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<',r'\u003c')
 metadata=f'''\n  <link rel="canonical" href="{escape(url(path),quote=True)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta property="og:site_name" content="The Sphere">
  <meta property="og:type" content="{'article' if entry else 'website'}">
  <meta property="og:locale" content="en_IN">
  <meta property="og:title" content="{escape(title,quote=True)}">
  <meta property="og:description" content="{escape(description,quote=True)}">
  <meta property="og:url" content="{escape(url(path),quote=True)}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{escape(title,quote=True)}">
  <meta name="twitter:description" content="{escape(description,quote=True)}">
  <script type="application/ld+json">{structured}</script>
'''
 return html.replace('</head>',metadata+'</head>',1)

def build_articles(home,entries):
 # Reuse the site's shell so typography, navigation and branding stay consistent.
 head=re.search(r'<head>(.*?)</head>',(ROOT/'templates/original-index.html').read_text(),re.S)[1]
 shell=re.search(r'<a class="skip".*?<main id="main">',home,re.S)[0].removesuffix('<main id="main">')
 footer=re.search(r'<footer>.*?</footer>',home,re.S)[0]
 invitation=re.search(r'<dialog id="invitation-dialog".*?</dialog>',home,re.S)[0]
 for entry in entries:
  path=ROOT/'dist/journal'/entry['slug'];path.mkdir(parents=True,exist_ok=True)
  related=''.join(f'<a href="/journal/{e["slug"]}/">{escape(e["title"])} <span aria-hidden="true">↗</span></a>' for e in entries if e!=entry)
  html=f'''<!doctype html><html lang="en-IN"><head>{head}</head><body class="article-page">{shell}
  <main id="main"><article class="article-reading">
  <nav class="article-breadcrumb" aria-label="Breadcrumb"><a href="/">The Sphere</a><span aria-hidden="true">/</span><a href="/#journal">Journal</a></nav>
  <p class="eyebrow">THE SPHERE JOURNAL · A SHORT REFLECTION</p>
  <h1>{escape(entry['title'])}</h1><p class="article-deck">{escape(entry['subtitle'])}</p>
  <p class="article-byline">By <a href="/#philosophy">The Sphere</a> · Coimbatore</p>
  <div class="article-prose">{''.join('<p>'+escape(p)+'</p>' for p in entry['paragraphs'])}</div>
  <p class="signature">The Sphere</p><a class="article-back" href="/#journal">← Back to the journal</a>
  <aside class="article-related"><h2>More from the journal</h2>{related}</aside>
  </article></main>{footer}{invitation}</body></html>'''
  # Root-relative assets and anchor links work from every article URL.
  html=re.sub(r'(href|src)="(assets/|style.css|brand.css|site.js)',r'\1="/\2',html)
  html=html.replace('href="#','href="/#').replace('href="/#main"','href="#main"')
  (path/'index.html').write_text(apply_seo(html,entry))

def build_discovery(entries):
 urls=[url()]+[url('/journal/'+e['slug']+'/') for e in entries]
 # Do not invent publication dates or last-modified signals.
 sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 sitemap+=''.join('  <url><loc>'+escape(u)+'</loc></url>\n' for u in urls)+'</urlset>\n'
 (ROOT/'dist/sitemap.xml').write_text(sitemap)
 (ROOT/'dist/robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+url('/sitemap.xml')+'\n')
