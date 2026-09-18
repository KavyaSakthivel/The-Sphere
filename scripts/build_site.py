from pathlib import Path
from html import escape
import re, json
from seo import apply_seo, build_articles, build_discovery
ROOT=Path(__file__).resolve().parents[1]
journal_data=json.loads((ROOT/'data/journal.json').read_text())
heads=['THE SPHERE','A SPACE THAT FEELS LIKE YOURS','WHY THE SPHERE?','THE SPHERE EXPERIENCE','MORE THAN WELLNESS','CURATED EXPERIENCES','IS WELLNESS A LUXURY OR A NECESSITY?','THE WOMEN OF THE SPHERE','A PRIVATE CIRCLE','THE SPHERE JOURNAL','A NOTE FROM THE SPHERE']
sections={}
for line in (ROOT/'notes/content.txt').read_text().splitlines():
 line=line.strip()
 if not line:continue
 if line in heads:key=line;sections[key]=[]
 else:sections[key].append(line)
def t(s,i):return escape(sections[heads[s]][i])
def ps(s,ids):return ''.join('<p>'+t(s,i)+'</p>' for i in ids)
def group(s,ids):return '<p>'+' '.join(t(s,i) for i in ids)+'</p>'
def label(s,prefix=''):return '<p class="eyebrow">'+prefix+escape(heads[s])+'</p>'
html=(ROOT/'templates/original-index.html').read_text()
# Restore the original composition and integrate the complete source into it.
html=re.sub(r'<p class="hero-description">.*?</p>',f'<p class="hero-description">{t(0,1)}</p>',html,count=1)
intro=f'''<section class="club-introduction section-pad">{label(0)}<h2>{t(0,2)}</h2><p>{t(0,3)}</p><div class="ritual-lines">{ps(0,range(4,10))}</div></section>'''
html=html.replace('  <section id="philosophy"',intro+'\n  <section id="philosophy"',1)
philosophy=f'''<section id="philosophy" class="philosophy section-pad">{label(1,'01 / ')}<div class="philosophy-main"><h2>Wellness,<br><em>beyond the usual.</em></h2><div class="prose">{ps(1,[1])}{group(1,range(2,7))}{ps(1,[7,8])}</div></div></section>'''
html=re.sub(r'<section id="philosophy".*?</section>',lambda _:philosophy,html,flags=re.S,count=1)
why=f'''<section class="why section-pad">{label(2)}<p class="why-subtitle">{t(2,0)}</p><h2>{t(2,1)} {t(2,2)} {t(2,3)}<br>{t(2,4)} {t(2,5)} {t(2,6)}<br><em>{t(2,8)}</em></h2>{ps(2,[7])}{group(2,range(9,12))}</section>'''
html=re.sub(r'<section class="why.*?</section>',lambda _:why,html,flags=re.S,count=1)
pillars=''
for i in range(4,8):
 name,copy=sections[heads[3]][i].split(':',1)
 pillars+=f'<article><span class="pillar-number">0{i-3}</span><h3>{escape(name.strip().title())}</h3><p>{escape(copy.strip())}</p></article>'
offerings=''
for i in range(2,7):
 name,copy=sections[heads[5]][i].split(':',1)
 offerings+=f'<details{" open" if i==2 else ""}><summary>{escape(name.strip())} <span aria-hidden="true">+</span></summary><p>{escape(copy.strip())}</p></details>'
experience=f'''<section id="experiences" class="experiences section-pad"><div class="section-heading"><div>{label(3,'02 / ')}<h2>Curated, <em>not crowded.</em></h2></div><p>{t(3,1)}<br>{t(3,2)}</p></div><p class="pillar-intro">{t(3,3)}</p><div class="pillars">{pillars}</div><div class="more-wellness"><div>{label(4)}<h3>A community built<br>around <em>experiences.</em></h3></div><div class="prose">{ps(4,[1,2])}{group(4,[3,4])}</div></div><div class="experience-detail"><figure><img src="assets/shared-making-1200.webp" srcset="assets/shared-making-640.webp 640w, assets/shared-making-1200.webp 1200w" sizes="(max-width: 700px) 86vw, 42vw" alt="Two women sharing a quiet moment of creativity at a pottery table" loading="lazy" width="1400" height="933"><figcaption>MORE THAN WHAT YOU DO. IT’S WHAT YOU FEEL.</figcaption></figure><div>{label(5)}<h3>Every gathering<br>has a <em>purpose.</em></h3><p class="experience-intro">{t(5,1)}</p><div class="experience-list">{offerings}</div></div></div></section>'''
html=re.sub(r'<section id="experiences".*?</section>',lambda _:experience,html,flags=re.S,count=1)
necessity=f'''<section class="necessity"><div class="necessity-photo"><img src="assets/mindful-hands-1200.webp" srcset="assets/mindful-hands-640.webp 640w, assets/mindful-hands-1200.webp 1200w" sizes="(max-width: 700px) 100vw, 49vw" alt="Hands gently shaping clay on a pottery wheel" loading="lazy" width="1200" height="800"></div><div class="necessity-copy">{label(6)}<h2>Taking care of yourself<br>isn’t a luxury.<br><em>It’s a necessity.</em></h2><p class="source-statement">{t(6,0)}</p>{ps(6,[1])}{group(6,range(2,5))}{ps(6,[5])}</div></section>'''
html=re.sub(r'<section class="necessity".*?</section>',lambda _:necessity,html,flags=re.S,count=1)
community=f'''<section class="community section-pad">{label(7,'03 / ')}<h2>Different lives.<br><em>Shared values.</em></h2>{ps(7,[1,2])}{group(7,[3,4])}<div class="values"><span>Curious.</span><span>Intentional.</span><span>Open.</span><span>Evolving.</span></div></section>'''
html=re.sub(r'<section class="community.*?</section>',lambda _:community,html,flags=re.S,count=1)
invitation=f'''<section id="invitation" class="invitation section-pad"><div class="invitation-brand"><img src="assets/brand/circle-lockup.svg" alt="The Sphere logo encircled by its signature organic rings" loading="lazy" width="1080" height="1080"><p>you belong in your life.</p></div><div class="invitation-copy">{label(8)}<h2>Intentionally<br><em>intimate.</em></h2>{ps(8,[1,2])}{group(8,[3,4])}<button class="button button-dark" data-invitation>Request an Invitation <span aria-hidden="true">↗</span></button><p class="invitation-small">Your first step into The Sphere.</p><p class="venue-note">Venue details are shared by email or WhatsApp.</p></div></section>'''
html=re.sub(r'<section id="invitation".*?</section>',lambda _:invitation,html,flags=re.S,count=1)
entries=''
for i in range(1,11,2):
 slug=journal_data[(i-1)//2]['slug']
 entries+=f'<a class="journal-entry" href="/journal/{slug}/" data-entry="{(i-1)//2}" aria-label="Read {t(9,i)}"><span class="journal-number">0{(i+1)//2}</span><span class="journal-title">{t(9,i)}</span><span class="journal-subtitle">{t(9,i+1)}</span><span class="journal-arrow" aria-hidden="true">↗</span></a>'
journal=f'''<section id="journal" class="journal section-pad"><div class="section-heading"><div>{label(9,'04 / ')}<h2>Room for <em>thought.</em></h2></div><p>{t(9,0)}</p></div><div class="journal-list">{entries}</div></section>'''
html=re.sub(r'<section id="journal".*?</section>',lambda _:journal,html,flags=re.S,count=1)
note=f'''<section class="note section-pad">{label(10)}<h2>“We wanted to create<br>a space to <em>simply be.</em>”</h2>{ps(10,[0,1])}<p class="note-pause">{t(10,2)}<br>{t(10,3)}<br>{t(10,4)}</p>{group(10,[5,6])}{ps(10,[7])}<p class="note-signoff">{t(10,8)} {t(10,9)}<br>{t(10,10)}</p><span class="signature">The Sphere</span></section>'''
html=re.sub(r'<section class="note.*?</section>',lambda _:note,html,flags=re.S,count=1)
html=apply_seo(html)
html=html.replace('</main>', '</main><script type="application/json" id="journal-data">'+json.dumps(journal_data,ensure_ascii=False).replace('<','\\u003c')+'</script>',1)
(ROOT/'dist/index.html').write_text(html)
build_articles(html,journal_data)
build_discovery(journal_data)
# Keep links from the interim four-page version working.
for route,target in [('experience','experiences'),('circle','invitation'),('journal','journal')]:
 (ROOT/'dist'/route/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=/#{target}"><title>The Sphere</title><meta name="robots" content="noindex,follow"></head><body><a href="/#{target}">Enter The Sphere</a></body></html>')
print('Restored the original single-page design with all 11 source sections.')
