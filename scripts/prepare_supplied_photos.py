"""Export photographs the client supplied directly (media/supplied/) as responsive site images.

These are used as received: no exposure change, no cropping, and nothing is enlarged past its own
width, so the 1200 and 1920 files are the original size and only the 640 is reduced.
  sphere-necessity     Our story, "Is wellness a luxury or a necessity?"
  sphere-talk-reflect  Experiences, "Talk & Reflect"
  sphere-explore       Experiences, "Explore & Experience"
"""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'media/supplied'
OUT=ROOT/'dist/assets'

def main():
    for source in sorted(SRC.glob('*.webp')):
        with Image.open(source) as opened:
            image=opened.convert('RGB')
        for width in (640,1200,1920):
            target=min(width,image.width)
            resized=image if target==image.width else image.resize((target,round(image.height*target/image.width)),Image.Resampling.LANCZOS)
            resized.save(OUT/f'{source.stem}-{width}.webp',quality=90,method=6)
        print(source.stem,image.size,flush=True)

if __name__=='__main__':main()
