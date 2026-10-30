"""Meta (Facebook / Instagram) Pixel: the base code in every public page's <head>, and the matching
Content-Security-Policy allowances. The pixel id lives in data/site.json ("meta_pixel_id"); empty means
no pixel. Every page here is generated, so the pixel is added by the build, never by hand."""
from pathlib import Path
import base64,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]

def pixel_id():
 return json.loads((ROOT/'data/site.json').read_text()).get('meta_pixel_id','').strip()

def _script(pid):
 # Meta's base code, verbatim apart from the pixel id.
 return ("\n!function(f,b,e,v,n,t,s)\n"
  "{if(f.fbq)return;n=f.fbq=function(){n.callMethod?\n"
  "n.callMethod.apply(n,arguments):n.queue.push(arguments)};\n"
  "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';\n"
  "n.queue=[];t=b.createElement(e);t.async=!0;\n"
  "t.src=v;s=b.getElementsByTagName(e)[0];\n"
  "s.parentNode.insertBefore(t,s)}(window, document,'script',\n"
  "'https://connect.facebook.net/en_US/fbevents.js');\n"
  f"fbq('init', '{pid}');\n"
  "fbq('track', 'PageView');\n")

def snippet(pid):
 return ('<!-- Meta Pixel Code -->\n'
  f'<script>{_script(pid)}</script>\n'
  '<noscript><img height="1" width="1" style="display:none"\n'
  f'src="https://www.facebook.com/tr?id={pid}&ev=PageView&noscript=1"\n'
  '/></noscript>\n'
  '<!-- End Meta Pixel Code -->\n')

def script_hash(pid):
 """CSP hash of the inline script, so the policy can stay free of 'unsafe-inline' for scripts."""
 return "'sha256-"+base64.b64encode(hashlib.sha256(_script(pid).encode()).digest()).decode()+"'"

def allow_meta(csp,pid):
 """Add exactly what the pixel needs to a Content-Security-Policy value; safe to apply twice."""
 add={'script-src':[script_hash(pid),'https://connect.facebook.net'],
      'img-src':['https://www.facebook.com'],
      'connect-src':['https://www.facebook.com','https://connect.facebook.net']}
 def widen(m):
  name,sources=m[1],m[2]
  extra=[s for s in add.get(name,[]) if s not in sources.split()]
  return f'{name} {sources}'+''.join(' '+s for s in extra)
 return re.sub(r'(?<![\w-])(script-src|img-src|connect-src) ([^;]*)',widen,csp)

def add_to_page(html):
 """Pixel under the existing <head> content (just above </head>), and the page's own CSP widened to match."""
 pid=pixel_id()
 if not pid or 'fbq(' in html or '</head>' not in html: return html
 html=re.sub(r'(<meta http-equiv="Content-Security-Policy" content=")([^"]*)(")',
  lambda m:m[1]+allow_meta(m[2],pid)+m[3],html,count=1)
 return html.replace('</head>',snippet(pid)+'</head>',1)

def patch_headers(path):
 """The same allowances in the per-page policies of the hosting headers file (Netlify / Cloudflare Pages)."""
 pid=pixel_id()
 if not pid or not path.exists(): return
 lines=path.read_text().split('\n')
 path.write_text('\n'.join(
  re.sub(r'^(\s*Content-Security-Policy: )(.*)$',lambda m:m[1]+allow_meta(m[2],pid),line) for line in lines))
