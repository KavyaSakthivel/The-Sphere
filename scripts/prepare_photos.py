"""Turn the club's RAW session photos into the site's responsive WebP images.

  python3 scripts/prepare_photos.py && python3 scripts/build_site.py

RAW files live in media/home/raw/ (git-ignored). The camera's defaults come out a little dark and
flat, so each photo gets a gentle exposure and contrast lift; colour is otherwise left natural.
Needs macOS `sips` (RAW decode) and Pillow.
"""
from pathlib import Path
import subprocess, tempfile
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'media/home/raw'
OUT = ROOT/'dist/assets'
# output name: (source, widths, (width ratio, height ratio) crop or None, horizontal focus 0-1, brightness, vertical focus 0-1)
PHOTOS = {
 'session-circle': ('DSC09893.ARW', (640, 1200), (3, 2), 0.5, 1.22),   # seated meditation circle
 'session-sound': ('DSC09852.ARW', (640, 1200), (3, 2), 0.5, 1.18),    # bowls played over participants at rest
 'session-bowls': ('DSC09840.ARW', (640, 1200), (2, 3), 0.45, 1.2, 1.0),  # the singing-bowl setup before a session; event hero
}


def decode(raw, tmp):
 jpg = Path(tmp)/(raw.stem+'.jpg')
 subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '95', str(raw), '--out', str(jpg)], check=True, capture_output=True)
 # Vertical frames carry their rotation as an EXIF tag; bake it in.
 return ImageOps.exif_transpose(Image.open(jpg)).convert('RGB')


def crop_to(img, ratio, focus, focus_y=0.5):
 if not ratio:
  return img
 w, h = img.size
 target = ratio[0]/ratio[1]
 if w/h > target:
  nw = round(h*target)
  x = round((w-nw)*focus)
  return img.crop((x, 0, x+nw, h))
 nh = round(w/target)
 y = round((h-nh)*focus_y)
 return img.crop((0, y, w, y+nh))


def main():
 with tempfile.TemporaryDirectory() as tmp:
  for name, (source, widths, ratio, focus, lift, *rest) in PHOTOS.items():
   img = decode(RAW/source, tmp)
   if rest:
    # Trim from the top first (keeps people's legs in the background out of a still-life frame).
    img = img.crop((0, round(img.height*0.18), img.width, img.height))
   img = crop_to(img, ratio, focus, rest[0] if rest else 0.5)
   img = ImageEnhance.Contrast(ImageEnhance.Brightness(img).enhance(lift)).enhance(1.04)
   for width in widths:
    out = img.resize((width, round(img.height*width/img.width)), Image.LANCZOS)
    path = OUT/f'{name}-{width}.webp'
    out.save(path, 'WEBP', quality=80, method=6)
    print(f'{path.relative_to(ROOT)}  {out.width}x{out.height}  {path.stat().st_size/1e3:.0f} KB')


if __name__ == '__main__':
 main()
