"""Prepare selected, authentic Sphere photos from the reviewed local originals.

Rebuild with the bundled Python/Pillow runtime. RAW decoding uses macOS ImageIO
through sips; the macOS sandbox may require approval for its decoding service.
Only exposure, slight contrast and responsive resizing are applied. No originals
are modified. data/media-selection.json records the source of every output.
"""
from pathlib import Path
import json, subprocess, sys, tempfile
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'media/home/raw'
OUT=ROOT/'dist/assets'

def main():
    selection=json.loads((ROOT/'data/media-selection.json').read_text())
    with tempfile.TemporaryDirectory() as tmp:
        only=set(sys.argv[1:])  # optional: rebuild just the named outputs
        for item in selection['photos']+selection['stills']:
            if only and item['name'] not in only: continue
            source=RAW/item['source']
            if not source.exists():
                print('skipped (original not in media/home/raw yet):',item['name'],flush=True)
                continue
            jpeg=Path(tmp)/(item['name']+'.jpg')
            if source.suffix.lower()=='.arw':
                subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','95',str(source),'--out',str(jpeg)],check=True,capture_output=True)
            else:
                subprocess.run(['ffmpeg','-v','error','-y','-ss',str(item['time']),'-i',str(source),'-frames:v','1',str(jpeg)],check=True)
            with Image.open(jpeg) as raw:
                image=ImageOps.exif_transpose(raw).convert('RGB')
            image=ImageEnhance.Brightness(image).enhance(item['exposure'])
            image=ImageEnhance.Contrast(image).enhance(1.025)
            if item.get('soft'):
                # Soft-focus openings: a deliberate out-of-focus wash in the warm palette, so the
                # photograph sets a mood behind the words (and no face or equipment reads clearly).
                image=image.filter(ImageFilter.GaussianBlur(image.width*0.009))
                image=Image.blend(image,Image.new('RGB',image.size,(196,160,128)),0.14)
            for width in (640,1200,1920):
                resized=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
                path=OUT/f'{item["name"]}-{width}.webp'
                resized.save(path,quality=87,method=6)
            print(item['name'],source.name,flush=True)

if __name__=='__main__':main()
