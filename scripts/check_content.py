from pathlib import Path
from html.parser import HTMLParser
import re,json
ROOT=Path(__file__).resolve().parents[1]
class Content(HTMLParser):
 def __init__(self):super().__init__();self.main=False;self.text=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='main':self.main=True
  if self.main and tag in ('br','p','h1','h2','h3','span'):self.text.append(' ')
  for k,v in attrs:
   if k in ('href','src') and v:self.links.append(v)
 def handle_endtag(self,tag):
  if tag=='main':self.main=False
  if self.main:self.text.append(' ')
 def handle_data(self,data):
  if self.main:self.text.append(data)
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
source=(ROOT/'notes/content.txt').read_text()
pages={}
for path in sorted((ROOT/'dist').rglob('*.html')):
 p=Content();p.feed(path.read_text())
 if p.text:pages[str(path.relative_to(ROOT/'dist'))]=' '.join(p.text)
 for link in p.links:
  if not link.startswith('/') or link.startswith('//'):continue
  target=ROOT/'dist'/link.split('#')[0].lstrip('/')
  if target.is_dir():target=target/'index.html'
  assert target.is_file(),f'Broken local reference: {path}: {link}'
missing=[];coverage=[]
for line in source.splitlines():
 if not line.strip():continue
 found=[path for path,text in pages.items() if norm(line) in norm(text)]
 if not found:missing.append(line)
 coverage.append({'source':line.strip(),'pages':found})
assert not missing,'Missing source content: '+repr(missing)
allcopy=' '.join(pages.values())
for restored in ['A little more room for you', 'Room for thought']:
 assert norm(restored) in norm(allcopy), f'Original design headline missing: {restored}'
assert 'data-entry' in (ROOT/'dist/index.html').read_text()
assert 'Try leaving a small part of your day unclaimed' in (ROOT/'dist/site.js').read_text()
(ROOT/'notes/content-coverage.json').write_text(json.dumps(coverage,indent=2,ensure_ascii=False)+'\n')
print(f'PASS: {len(coverage)} source lines are present across {len(pages)} pages; local links and assets resolve; original headlines and journal interactions restored.')
