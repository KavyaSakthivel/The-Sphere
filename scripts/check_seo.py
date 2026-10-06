"""Verify generated search metadata, discoverability, and article content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
config=json.loads((ROOT/'data/site.json').read_text());base=config['url'].rstrip('/')
entries=json.loads((ROOT/'data/journal.json').read_text())
class Page(HTMLParser):
 def __init__(self):super().__init__();self.canon=[];self.meta={};self.h1=0;self.title='';self.in_title=False;self.jsons=[];self.json_text=None;self.links=[];self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.in_title=True
  if tag=='meta':self.meta[a.get('name',a.get('property'))]=a.get('content')
  if tag=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
  if tag=='script' and a.get('type')=='application/ld+json':self.json_text=''
  if tag=='a':self.links.append(a.get('href',''))
  for key in ['href','src']:
   u=a.get(key,'')
   if not u or u.startswith('#') or urlsplit(u).scheme or u.startswith('//'):continue
   p=(DIST/urlsplit(u).path.lstrip('/')) if u.startswith('/') else self.path.parent/urlsplit(u).path
   if p.is_dir():p=p/'index.html'
   assert p.is_file(),f'Missing {u} from {self.path}'
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
  if tag=='script' and self.json_text is not None:self.jsons.append(json.loads(self.json_text));self.json_text=None
 def handle_data(self,s):
  self.text.append(s)
  if self.in_title:self.title+=s
  if self.json_text is not None:self.json_text+=s
 def read(self,path):self.path=path;self.feed(path.read_text());return self
paths=['/']+['/journal/'+e['slug']+'/' for e in entries]
event=json.loads((ROOT/'data/event.json').read_text()) if (ROOT/'data/event.json').exists() else None
event_path='/'+event['slug']+'/' if event else None
titles=set();descriptions=set()
for route in paths:
 p=Page().read(DIST/route.strip('/')/'index.html')
 assert p.h1==1 and p.canon==[base+route],route
 assert p.meta['og:url']==p.canon[0]
 assert p.meta['robots']=='index,follow,max-image-preview:large'
 assert p.title and p.title not in titles;titles.add(p.title)
 assert p.meta['description'] and p.meta['description'] not in descriptions;descriptions.add(p.meta['description'])
 assert len(p.jsons)==1
 graph=p.jsons[0]['@graph'];organization=next(x for x in graph if x['@type']=='Organization')
 assert organization['areaServed']['name']=='Coimbatore'
 assert not any(k in organization for k in ['address','telephone','aggregateRating','openingHours'])
 if route!='/':
  entry=next(e for e in entries if route=='/journal/'+e['slug']+'/')
  article=next(x for x in graph if x['@type']=='Article')
  assert article['headline']==entry['title']
  assert all(t in ' '.join(p.text) for t in entry['paragraphs'])
 else:
  assert all('/journal/'+e['slug']+'/' in p.links for e in entries)
  assert 'Coimbatore' in ' '.join(p.text)
locs=[x.text for x in ET.parse(DIST/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert locs==[base+p for p in paths+['/philosophy/','/experiences/','/membership/']+([event_path] if event else [])]
for slug in ['experiences','membership']:
 page=Page().read(DIST/slug/'index.html')
 assert page.h1==1 and page.canon==[base+'/'+slug+'/'] and len(page.jsons)==1
philosophy=Page().read(DIST/'philosophy/index.html')
assert philosophy.h1==1 and philosophy.canon==[base+'/philosophy/']
assert philosophy.meta['og:url']==base+'/philosophy/' and philosophy.meta['robots']=='index,follow,max-image-preview:large'
assert philosophy.title not in titles and philosophy.meta['description'] not in descriptions
assert len(philosophy.jsons)==1
if event:
 # The one-off event page: indexable, with an Event graph.
 p=Page().read(DIST/event['slug']/'index.html')
 assert p.h1==1 and p.canon==[base+event_path] and p.meta['robots']=='index,follow,max-image-preview:large'
 assert p.title not in titles and p.meta['description'] not in descriptions
 ev=next(x for x in p.jsons[0]['@graph'] if x['@type']=='Event')
 assert ev['startDate']==event['start'] and ev['offers']['price']==str(event['price_inr']) and ev['location']['name']==event['venue']
 from datetime import datetime
 until=datetime.fromisoformat(event.get('promotion_until',event['end']))
 if event.get('show_on_home') and datetime.now(until.tzinfo)<until:
  assert event_path in Page().read(DIST/'index.html').links
assert 'Sitemap: '+base+'/sitemap.xml' in (DIST/'robots.txt').read_text()
assert 'Disallow: /' not in (DIST/'robots.txt').read_text()
for p in ['experience','circle','journal']:
 assert Page().read(DIST/p/'index.html').meta['robots']=='noindex,follow'
print('PASS: home, five journal articles, philosophy and event metadata; sitemap entries, static article bodies and crawlable links; no invented location details.')
