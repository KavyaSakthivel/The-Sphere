"""Encode curated licensed editorial images; originals remain unchanged."""
from pathlib import Path
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]
SELECTED={'editorial-flow':8534435,'editorial-sky':4909322,'editorial-air':7289120,'editorial-move':8534772,'editorial-pause':7113299,'editorial-reflect':4057861,'editorial-connect':3822725}
for name,number in SELECTED.items():
    with Image.open(ROOT/f'media/editorial/wellness-{number}.jpg') as source:
        image=ImageOps.exif_transpose(source).convert('RGB')
        for width in (640,1200):
            image.resize((width,round(width*image.height/image.width)),Image.Resampling.LANCZOS).save(ROOT/f'dist/assets/{name}-{width}.webp',quality=86,method=6)
