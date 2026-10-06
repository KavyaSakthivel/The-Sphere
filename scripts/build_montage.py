"""Cut the club's own clips and photos into silent, looping hero videos.

  python3 scripts/build_montage.py home       # landing page: wide (desktop) + tall (phone) loops
  python3 scripts/build_montage.py carnival   # event page: independent desktop + phone loops
then  python3 scripts/build_site.py  and deploy.

Footage lives outside git (media/ is ignored). A shot list in data/montage-<target>.json picks the
files, where each shot starts, how long it holds, and where the tall crop sits so faces stay in frame:
  {"wide": [{"file": "C0059.MP4", "start": 1.9}, {"triptych": [{...}, {...}, {...}]}], "tall": [...]}
(or one "shots" list for every cut). A triptych sets three vertical clips side by side in a wide cut.
Without a shot list, every file in the source folder is used in name order.
RAW photos (.ARW and friends) are converted with macOS `sips` first. Needs ffmpeg (brew install ffmpeg).
"""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
VIDEO = {'.mp4', '.mov', '.m4v', '.webm', '.mkv', '.avi', '.mts'}
PHOTO = {'.jpg', '.jpeg', '.png', '.webp', '.heic'}
RAW = {'.arw', '.cr2', '.cr3', '.nef', '.dng', '.raf', '.orf'}
FPS, FADE, HOLD = 25, 1.0, 5.0
GUTTER, PAPER = 6, '0xFFF8EC'   # ivory rules between triptych panels (brand Soft Ivory)
TARGETS = {
 # Independent event cuts from the shared original footage library.
 'carnival': {'source': ROOT/'media/home/raw', 'out': ROOT/'dist/assets/montage-carnival', 'variants': [('wide', 1600, 900), ('tall', 720, 1280)]},
 # The landing page's framed panorama, and its tall phone crop.
 'home': {'source': ROOT/'media/home/raw', 'out': ROOT/'dist/assets/montage', 'variants': [('wide', 1600, 900), ('tall', 720, 1280)]},
}


def run(args):
 result = subprocess.run(args, capture_output=True, text=True)
 if result.returncode:
  sys.exit(f'{args[0]} failed:\n'+result.stderr[-2000:])
 return result.stdout


def duration(path):
 return float(json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)]))['format'].get('duration') or 0)


def still(path, tmp):
 """Camera RAW files become a full-size JPEG that ffmpeg can read."""
 if path.suffix.lower() not in RAW:
  return path
 target = Path(tmp)/(path.stem+'.jpg')
 if not target.exists():
  run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(path), '--out', str(target)])
  # Vertical shots keep their rotation as an EXIF tag, which ffmpeg ignores; bake it into the pixels.
  from PIL import Image, ImageOps
  ImageOps.exif_transpose(Image.open(target)).save(target, quality=92)
 return target


def crop(w, h, focus, focus_y=0.5):
 # Fill the frame, then slide the crop window: focus 0 keeps the left edge, 1 the right, 0.5 the centre.
 return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}:(iw-{w})*{focus}:(ih-{h})*{focus_y},setsar=1"


def render_shot(shot, source, w, h, target, tmp):
 if 'triptych' in shot or 'diptych' in shot:
  return render_triptych(shot, source, w, h, target, tmp)
 path = source/shot['file']
 hold, focus = shot.get('hold', HOLD), shot.get('focus', 0.5)
 enc = ['-an', '-r', str(FPS), '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', str(target)]
 kind = path.suffix.lower()
 if kind in PHOTO | RAW:
  # A slow push-in so photographs breathe like the footage around them.
  frames = round(hold*FPS)
  zoom = f"zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS}"
  run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', str(still(path, tmp)), '-vf', f'{crop(w*2, h*2, focus)},{zoom},setsar=1',
   '-frames:v', str(frames)]+enc)
  return
 length = duration(path)
 start = shot.get('start', min(length*0.2, max(length-hold, 0)))
 speed = shot.get('speed', 1.0)
 take = hold * speed
 if speed <= 0 or start < 0 or start + take > length - .04:
  sys.exit(f'{path.name}: requested interval extends beyond the source; select a shorter hold instead of freezing the final frame.')
 run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.2f}', '-t', f'{take:.2f}', '-i', str(path),
  '-vf', f'setpts=(PTS-STARTPTS)/{speed},{crop(w, h, focus, shot.get("focus_y", .5))},fps={FPS}', '-frames:v', str(round(hold*FPS))]+enc)


def render_triptych(shot, source, w, h, target, tmp):
 """Portrait movement clips share a wide frame while keeping full bodies visible."""
 parts = shot.get('diptych') or shot['triptych']
 count = len(parts)
 cell = (w-(count-1)*GUTTER)//count//2*2
 cells = []
 for i, part in enumerate(parts):
  cell_path = Path(tmp)/f'{target.stem}-cell{i}.mp4'
  render_shot({**part, 'hold': shot.get('hold', HOLD)}, source, cell, h, cell_path, tmp)
  cells.append(cell_path)
 extra = w-count*cell-(count-1)*GUTTER
 pads = [f'[{i}:v]pad={cell+(GUTTER if i<count-1 else extra)}:{h}:0:0:color={PAPER}[p{i}]' for i in range(count)]
 graph = ';'.join(pads)+';'+''.join(f'[p{i}]' for i in range(count))+f'hstack=inputs={count},setsar=1[out]'
 run(['ffmpeg', '-v', 'error', '-y']+sum((['-i', str(c)] for c in cells), [])+['-filter_complex', graph, '-map', '[out]', '-an',
  '-r', str(FPS), '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-pix_fmt', 'yuv420p', str(target)])


def join(segments, holds, target):
 """Crossfade shot into shot, and the last back into the first, trimmed so the loop has no seam."""
 chain, holds = segments+[segments[0]], holds+[holds[0]]
 inputs = sum((['-i', str(p)] for p in chain), [])
 graph, last, offset = [], '[0:v]', 0.0
 for i in range(1, len(chain)):
  offset += holds[i-1]-FADE
  graph.append(f'{last}[{i}:v]xfade=transition=fade:duration={FADE}:offset={offset:.3f}[x{i}]')
  last = f'[x{i}]'
 graph.append(f'{last}trim=start={FADE}:duration={offset:.3f},setpts=PTS-STARTPTS,format=yuv420p[out]')
 run(['ffmpeg', '-v', 'error', '-y']+inputs+['-filter_complex', ';'.join(graph), '-map', '[out]', '-an',
  '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', str(target)])
 return offset


def encode(master, out, name):
 # VP9 for most browsers (smaller), H.264 for Safari and older phones. No audio track in either.
 run(['ffmpeg', '-v', 'error', '-y', '-i', str(master), '-an', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '27', '-preset', 'slow',
  '-maxrate', '2500k', '-bufsize', '5000k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out/f'{name}.mp4')])
 run(['ffmpeg', '-v', 'error', '-y', '-i', str(master), '-an', '-c:v', 'libvpx-vp9', '-crf', '37', '-b:v', '0', '-row-mt', '1',
  '-deadline', 'good', '-cpu-used', '2', str(out/f'{name}.webm')])
 run(['ffmpeg', '-v', 'error', '-y', '-i', str(master), '-frames:v', '1', '-q:v', '3', str(out/f'{name}-poster.jpg')])


def files_in(shots):
 for s in shots:
  parts = s.get('diptych') or s.get('triptych')
  yield from (files_in(parts) if parts else [s['file']])


def shot_list(key, source, variant):
 manifest = ROOT/f'data/montage-{key}.json'
 if manifest.exists():
  data = json.loads(manifest.read_text())
  shots = data.get(variant) or data['shots']
  missing = [f for f in files_in(shots) if not (source/f).exists()]
  if missing:
   sys.exit('Missing from '+str(source.relative_to(ROOT))+': '+', '.join(missing))
  return shots
 return [{'file': p.name} for p in sorted(source.glob('*')) if p.suffix.lower() in VIDEO | PHOTO | RAW]


def main():
 key = sys.argv[1] if len(sys.argv) > 1 else ''
 if key not in TARGETS:
  sys.exit('Usage: python3 scripts/build_montage.py home|carnival')
 if not shutil.which('ffmpeg'):
  sys.exit('ffmpeg is not installed. Run: brew install ffmpeg')
 target = TARGETS[key]
 with tempfile.TemporaryDirectory() as tmp:
  for name, w, h in target['variants']:
   shots = shot_list(key, target['source'], name) if target['source'].exists() else []
   if len(shots) < 2:
    sys.exit(f'Put at least two clips or photos in {target["source"].relative_to(ROOT)}/ first.')
   target['out'].mkdir(parents=True, exist_ok=True)
   segments = []
   for i, shot in enumerate(shots):
    segment = Path(tmp)/f'{name}-{i:02}.mp4'
    render_shot(shot, target['source'], w, h, segment, tmp)
    segments.append(segment)
   master = Path(tmp)/f'{name}-master.mp4'
   loop = join(segments, [s.get('hold', HOLD) for s in shots], master)
   encode(master, target['out'], name)
   sizes = ', '.join(f"{p.name} {p.stat().st_size/1e6:.1f} MB" for p in sorted(target['out'].glob(f'{name}*')))
   print(f'{name} {w}x{h}: {len(shots)} shots, {loop:.1f}s loop — {sizes}')


if __name__ == '__main__':
 main()
