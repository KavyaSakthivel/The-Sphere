"""Build client-supplied palette comparisons and real-page previews locally."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/palette-study'

def build():
    palettes = json.loads((ROOT / 'data/palette-comparison.json').read_text())
    OUT.mkdir(exist_ok=True)
    for name in ('css', 'js'):
        (OUT / f'study.{name}').write_text((ROOT / f'templates/palette-study.{name}').read_text())
    cards = []
    for p in palettes:
        slug = p['slug']
        folder = OUT / slug
        folder.mkdir(exist_ok=True)
        colors = ';'.join(f'--{k}:{p[k]}' for k in ('primary','surface','deep','accent','detail'))
        swatches = ''.join(f'<div class="palette-swatch"><i style="--swatch:{c}"></i><span>{c}</span></div>' for c in p['colors'])
        note = f'<p class="palette-note">{escape(p["note"])}</p>' if p.get('note') else ''
        cards.append(f'''<article class="palette-option" data-palette="{slug}" style="{colors}">
          <div class="palette-label"><h2>{escape(p['name'])}</h2><span>Reference {p['reference']}</span></div>
          <p class="palette-impression">{escape(p['impression'])}</p>
          <div class="sphere-snippet">
            <div class="snippet-nav"><img src="/assets/brand/wordmark-ivory.svg" alt="The Sphere"><span>Our story · Membership</span></div>
            <div class="snippet-invitation"><img src="/assets/sphere-intimate-640.webp" width="640" height="427" alt="Women meditating together at a real Sphere gathering"><div><p class="snippet-kicker">A PRIVATE CIRCLE</p><h3>Intentionally<br>intimate.</h3><p>For women who value privacy, meaningful connection and thoughtfully curated experiences.</p><a class="snippet-action" href="/palette-study/{slug}/membership/">Request an invitation ↗</a></div></div>
            <div class="snippet-reading"><h3>Room for thought.</h3><p>Reflections on modern womanhood.</p></div>
            <div class="snippet-note"><div class="snippet-paper"><p>A NOTE FROM THE SPHERE</p><blockquote>“We wanted to create a space to simply be.”</blockquote><p>The Sphere was created for the woman behind all the roles she carries.</p><span class="snippet-signature">The Sphere</span></div></div>
            <div class="snippet-footer"><span>PEACE. PURPOSE. CONNECTION.</span><span>COIMBATORE</span></div>
          </div>
          <div class="palette-swatches" aria-label="Palette colours">{swatches}</div>
          <div class="palette-links"><a href="/palette-study/{slug}/membership/">Full Membership preview ↗</a><a href="/palette-study/{slug}/carnival/">Full Carnival preview ↗</a></div>{note}
        </article>''')
        # Keep the existing page structure, photographs, typography and controls.
        mapping = {
            '#123e46':p['primary'], '#082c33':p['deep'], '#f6f8f6':p['surface'],
            '#e1ebeb':p['surface'], '#f9faf8':p['surface'], '#476369':p['primary'],
            '#cadbdd':p['detail'], '#a9c6cc':p['surface'], '#d4e2e4':p['surface'],
            '#d6e3e5':p['detail'], '#f9faf6':p['surface'], '#becfd2':p['detail'],
            '#35565d':p['deep'], '#fff8ec':p['surface'], '#93b0c2':p['detail']
        }
        def recolor(match):
            value = match[0].lower()
            return mapping.get(value[:7],value[:7]) + value[7:]
        theme = re.sub(r'#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?\b', recolor, (ROOT/'templates/palette-base.css').read_text())
        theme += f'''
/* Preview-only role mapping: accent is selective, text remains readable. */
:root{{--wine:{p['primary']};--palette-accent:{p['accent']};--palette-detail:{p['detail']};}}
.premium-home .letter-heading h2{{color:{p['accent']};}}
.home-invitation .invitation-heading .text-link,.sphere-form button[type=submit],body .header .nav-right .header-invite{{background:{p['accent']};color:#fff8ec;}}
.home-invitation .invitation-heading .text-link:hover,body .header .nav-right .header-invite:hover{{background:{p['deep']};color:#fff8ec;}}
.event .event-card{{--ink:{p['deep']};--muted:{p['primary']};--rule:{p['detail']};}}
.event .event-tickets-copy{{--ink:{p['surface']};--muted:{p['surface']};}}
.palette-preview-return{{position:fixed;right:16px;bottom:80px;z-index:80;padding:12px 18px;background:{p['deep']};color:{p['surface']};border:1px solid {p['surface']};font:14px 'Nunito Sans',sans-serif;text-decoration:none;box-shadow:0 4px 20px #0002;}}
'''
        (folder/'theme.css').write_text(theme)
        for route in ('membership','carnival'):
            html = (ROOT/f'dist/{route}/index.html').read_text()
            html = re.sub(r'<link rel="canonical"[^>]*>', '', html)
            html = re.sub(r'<meta name="robots"[^>]*>', '', html)
            html = re.sub(r'<title>.*?</title>', f'<title>{escape(p["name"])} — {route.title()} preview | The Sphere</title>', html)
            html = html.replace('</head>',f'<meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/palette-study/{slug}/theme.css"></head>')
            for target in ('membership','carnival'):
                html = html.replace(f'href="/{target}/"',f'href="/palette-study/{slug}/{target}/"').replace(f'href="/{target}/#',f'href="/palette-study/{slug}/{target}/#')
            html = html.replace('</body>', '<a class="palette-preview-return" href="/palette-study/">← Compare all palettes</a></body>')
            path = folder/route;path.mkdir(exist_ok=True)
            (path/'index.html').write_text(html)
    options = ''.join(f'<option value="{p["slug"]}">{escape(p["name"])}</option>' for p in palettes)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Palette comparison | The Sphere</title><link rel="stylesheet" href="/assets/fonts.css"><link rel="stylesheet" href="/palette-study/study.css"><script src="/palette-study/study.js" defer></script></head><body>
      <header class="study-header"><div><p>THE SPHERE / COLOUR STUDY</p><h1>{len(palettes)} palettes. The same Sphere.</h1><p>Compare the same photograph, logo, invitation and reader’s note. Open the full page previews to explore each direction.</p></div><a href="/">Return to The Sphere ↗</a></header>
      <div class="study-controls"><label for="palette-picker">View<select id="palette-picker"><option value="all">Compare all {len(palettes)}</option>{options}</select></label></div>
      <main class="study-grid">{''.join(cards)}</main>
      <p class="study-footnote">The original ivory logo is retained in every option. Colour roles are adapted for readability. Reference 5’s Mossy Green uses the visible olive swatch because its printed hex specifies pink. These are previews for comparison.</p>
    </body></html>'''
    (OUT/'index.html').write_text(html)
    print(f'Built {len(palettes)} palette snippets and {len(palettes) * 2} full-page previews at /palette-study/.')

if __name__ == '__main__':
    build()
