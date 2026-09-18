"""Prepare supplied vector artwork for responsive web placement; preserve paths."""
from pathlib import Path
import xml.etree.ElementTree as ET
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS)
assets=ROOT/'dist/assets/brand';assets.mkdir(exist_ok=True)
for source,name in [('01','wordmark-sage'),('02','wordmark-ivory')]:
 root=ET.parse(ROOT/f'SVG/TheSphere-{source}.svg').getroot()
 for child in list(root):
  if child.tag==f'{{{NS}}}rect':root.remove(child)
 root.set('viewBox','243 414 594 251')
 ET.ElementTree(root).write(assets/f'{name}.svg',encoding='unicode')
root=ET.parse(ROOT/'SVG/TheSphere-07.svg').getroot()
# The final group is the designer's concentric circular artwork.
motif=ET.Element(f'{{{NS}}}svg',{'viewBox':'0 0 1080 1080'})
motif.append(deepcopy(root.find(f'{{{NS}}}defs')))
motif.append(deepcopy(list(root)[-1]))
ET.ElementTree(motif).write(assets/'circles-ivory.svg',encoding='unicode')
# Keep the complete supplied circular lockup, including its sage background.
ET.ElementTree(root).write(assets/'circle-lockup.svg',encoding='unicode')
print('Prepared four brand SVG assets without redrawing the supplied artwork.')
