"""Google Tag Manager: the container's Google tag at the top of every public page's <head>, and the
matching Content-Security-Policy allowances. The container id lives in data/site.json
("google_tag_manager_id"); empty means no tag. Every page here is generated, so the tag is added by
the build, never by hand."""
from pathlib import Path
import base64,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]

def container_id():
 return json.loads((ROOT/'data/site.json').read_text()).get('google_tag_manager_id','').strip()

# The inline part of Tag Manager's installation snippet, verbatim.
_INLINE=("\n  window.dataLayer = window.dataLayer || [];\n"
 "  function gtag(){dataLayer.push(arguments);}\n"
 "  gtag('js', new Date());\n")

def snippet(cid):
 return (f'<script async src="https://www.googletagmanager.com/gtm.js?id={cid}"></script>\n'
  f'<script>{_INLINE}</script>\n')

def script_hash():
 """CSP hash of the inline script, so the policy can stay free of 'unsafe-inline' for scripts."""
 return "'sha256-"+base64.b64encode(hashlib.sha256(_INLINE.encode()).digest()).decode()+"'"

# Google's published allowances for Tag Manager with Google Analytics 4 and Google Ads.
_GOOGLE={'script-src':['https://*.googletagmanager.com','https://*.google-analytics.com',
                       'https://*.googleadservices.com','https://*.doubleclick.net','https://www.google.com'],
 'img-src':['https://*.googletagmanager.com','https://*.google-analytics.com','https://*.analytics.google.com',
            'https://*.g.doubleclick.net','https://www.google.com','https://www.google.co.in'],
 'connect-src':['https://*.googletagmanager.com','https://*.google-analytics.com',
                'https://*.analytics.google.com','https://*.g.doubleclick.net','https://www.google.com',
                'https://www.google.co.in'],
 'frame-src':['https://www.googletagmanager.com','https://td.doubleclick.net']}

def allow_google(csp):
 """Add exactly what Tag Manager needs to a Content-Security-Policy value; safe to apply twice."""
 add={k:list(v) for k,v in _GOOGLE.items()}
 add['script-src']=[script_hash()]+add['script-src']
 def widen(m):
  name,sources=m[1],m[2]
  extra=[s for s in add.get(name,[]) if s not in sources.split()]
  return f'{name} {sources}'+''.join(' '+s for s in extra)
 csp=re.sub(r'(?<![\w-])(script-src|img-src|connect-src|frame-src) ([^;]*)',widen,csp)
 if not re.search(r'(?<![\w-])frame-src ',csp):  # pages without one fall back to default-src 'self'
  csp=re.sub(r'(default-src [^;]*)',lambda m:m[1]+'; frame-src '+' '.join(add['frame-src']),csp,count=1)
 return csp

def add_to_page(html):
 """Tag as high in <head> as the page's own policy allows (right after that policy), policy widened."""
 cid=container_id()
 if not cid or 'googletagmanager.com/gtm.js' in html or '<head>' not in html: return html
 csp=re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)"\s*/?>',html)
 if csp:
  html=html.replace(csp[0],csp[0].replace(csp[1],allow_google(csp[1]))+'\n'+snippet(cid),1)
 else:
  html=html.replace('<head>','<head>\n'+snippet(cid),1)
 return html

def patch_headers(path):
 """The same allowances in the per-page policies of the hosting headers file."""
 if not container_id() or not path.exists(): return
 lines=path.read_text().split('\n')
 path.write_text('\n'.join(
  re.sub(r'^(\s*Content-Security-Policy: )(.*)$',lambda m:m[1]+allow_google(m[2]),line) for line in lines))
