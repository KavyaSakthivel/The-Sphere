"""Extract editorial stills from the club's locally supplied session footage.

Run python3 scripts/prepare_premium_assets.py before build_site.py.
Requires ffmpeg and Pillow; originals in media/home/raw/ are never modified.
"""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SHOTS = [
    ('C4441.MP4', 17, 'session-movement', 960, (3, 4)),
    ('C4451.MP4', 5, 'session-connection', 960, (3, 4)),
    ('C0021.MP4', 2, 'session-sound', 1920, (3, 2)),
    ('C9997.MP4', 2, 'session-group', 960, (3, 4)),
    ('C0001.MP4', 2, 'session-together', 1920, (16, 9)),
]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for name, start, target, width, ratio in SHOTS:
            jpg = Path(tmp) / (target + '.jpg')
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start),
                            '-i', str(ROOT / 'media/home/raw' / name), '-frames:v', '1', str(jpg)], check=True)
            size = (width, round(width * ratio[1] / ratio[0]))
            with Image.open(jpg) as source:
                image = ImageOps.fit(source.convert('RGB'), size, method=Image.Resampling.LANCZOS)
            image = ImageEnhance.Brightness(image).enhance(1.06)
            path = ROOT / 'dist/assets' / f'{target}-{width}.webp'
            image.save(path, quality=84, method=6)
            print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
