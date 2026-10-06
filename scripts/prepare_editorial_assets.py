"""Download and encode the selected Pexels editorial photographs.

Source pages, photographers and licence are recorded in assets/PHOTO-CREDITS.md.
These illustrate the philosophy; they do not depict Sphere members or premises.
"""
from pathlib import Path
import urllib.request
import ssl
import certifi
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PHOTOS = {'editorial-reading': 4049630, 'editorial-journal': 9031737, 'editorial-making': 6694742, 'editorial-flowers': 29547110}


def main():
    folder = ROOT/'media/editorial'; folder.mkdir(parents=True, exist_ok=True)
    for name, number in PHOTOS.items():
        original = folder/(name+'.jpg')
        if not original.exists():
            url = f'https://images.pexels.com/photos/{number}/pexels-photo-{number}.jpeg?auto=compress&cs=tinysrgb&w=1600'
            request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            original.write_bytes(urllib.request.urlopen(request, timeout=30, context=ssl.create_default_context(cafile=certifi.where())).read())
        with Image.open(original) as source:
            image = ImageOps.exif_transpose(source).convert('RGB')
            for width in (640, 1200):
                result = image.resize((width, round(width*image.height/image.width)), Image.Resampling.LANCZOS)
                output = ROOT/'dist/assets'/f'{name}-{width}.webp'
                result.save(output, quality=83, method=6)
                print(output.relative_to(ROOT))


if __name__ == '__main__':
    main()
