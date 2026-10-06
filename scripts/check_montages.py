"""Validate the independent homepage and carnival loops and responsive media wiring."""
from pathlib import Path
import json
import subprocess
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
shots = {}
intervals = {}
digests = {}
def flatten(entries):
    for entry in entries:
        parts = entry.get('diptych') or entry.get('triptych')
        if parts:
            yield from ({**part, 'hold':entry['hold']} for part in parts)
        else:
            yield entry
for page, folder in [('home', 'montage'), ('carnival', 'montage-carnival')]:
    data = json.loads((ROOT / f'data/montage-{page}.json').read_text())
    shots[page] = {shot['file'] for variant in ('wide', 'tall') for shot in flatten(data[variant])}
    intervals[page] = [(shot['file'], shot['start'], shot['start']+shot['hold']*shot.get('speed',1)) for variant in ('wide','tall') for shot in flatten(data[variant])]
    html = (ROOT / ('dist/index.html' if page == 'home' else 'dist/carnival/index.html')).read_text()
    for variant, dimensions in [('wide', (1600, 900)), ('tall', (720, 1280))]:
        assert any(shot['file'] in {'C4438.MP4','C4327.MP4','C4441.MP4','C4417.MP4','C4368.MP4','C4397.MP4'} for shot in flatten(data[variant])), f'{page}/{variant} is missing Kalari'
        assert any(shot['file'] in {'C0019.MP4','C0027.MP4','C0021.MP4','C0013.MP4','C0007.MP4','C0006.MP4','C0051.MP4','C0020.MP4'} for shot in flatten(data[variant])), f'{page}/{variant} is missing sound healing'
        expected_duration = sum(shot['hold'] - 1 for shot in data[variant])
        for ext, codec in [('mp4', 'h264'), ('webm', 'vp9')]:
            path = ROOT / f'dist/assets/{folder}/{variant}.{ext}'
            assert f'assets/{folder}/{variant}.{ext}' in html, f'{page} media is not wired to its own loop'
            meta = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
            assert len(meta['streams']) == 1, f'{path} must have only a silent video stream'
            video = meta['streams'][0]
            assert (video['width'], video['height']) == dimensions
            assert video['codec_name'] == codec
            assert abs(float(meta['format']['duration']) - expected_duration) < .1
            digests[page, variant, ext] = hashlib.sha256(path.read_bytes()).hexdigest()
        assert (ROOT / f'dist/assets/{folder}/{variant}-poster.jpg').exists()
for filename, start, end in intervals['home']:
    for other, other_start, other_end in intervals['carnival']:
        assert filename != other or end <= other_start or other_end <= start, 'The landing pages must use distinct source intervals'
assert not {'C9997.MP4', 'C4420.MP4'} & (shots['home'] | shots['carnival']), 'Rejected shaky clips returned'
assert 'C4372.MP4' not in (shots['home'] | shots['carnival']), 'Rejected rear-facing bending shot returned'
assert {'C4438.MP4','C4441.MP4','C0064.MP4','C0021.MP4','C4417.MP4','C4368.MP4'} <= (shots['home'] | shots['carnival'])
for filename, start, end in intervals['home'] + intervals['carnival']:
    if filename == 'C4441.MP4': assert end <= 5, 'Use the reviewed early floor sequence, not the later shaky camera sweep'
for variant in ('wide', 'tall'):
    for ext in ('mp4', 'webm'):
        assert digests['home', variant, ext] != digests['carnival', variant, ext]
for slug in ('experiences', 'membership'):
    html = (ROOT / f'dist/{slug}/index.html').read_text()
    assert re.search(r'class="subpage-opening photo-opening".*?<img', html, re.S)
print('PASS: distinct source intervals, requested Kalari/sound-healing clips, responsive MP4/WebM wiring, silent codecs, dimensions, loop durations, posters and subpage opening photos.')
