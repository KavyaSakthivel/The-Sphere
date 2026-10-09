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
        if page == 'carnival' or variant == 'tall':
            assert any(shot['file'] in {'C4438.MP4','C4327.MP4','C4441.MP4','C4417.MP4','C4368.MP4','C4397.MP4','C4415.MP4','C4345.MP4'} for shot in flatten(data[variant])), f'{page}/{variant} is missing movement'
        assert any(shot['file'] in {'C0019.MP4','C0027.MP4','C0021.MP4','C0013.MP4','C0007.MP4','C0006.MP4','C0051.MP4','C0020.MP4'} for shot in flatten(data[variant])), f'{page}/{variant} is missing sound healing'
        if page == 'home':
            assert all('diptych' not in shot and 'triptych' not in shot for shot in data[variant]), 'Homepage must use single full-frame shots'
        expected_duration = sum(shot['hold'] - data.get('fade', 1) for shot in data[variant])
        for shot in flatten(data[variant]):
            source = ROOT/'media/home/raw'/shot['file']
            metadata = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)]))
            assert 0 <= shot['start'] < shot['start'] + shot['hold'] * shot.get('speed',1) <= float(metadata['format']['duration']) - .04, 'Source interval must not require a frozen frame'
            if page == 'home' and variant == 'wide' and shot['file'] != 'C4345.MP4':
                # C4345 is the one client-requested exception: a portrait movement class, framed as a wide band.
                original = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
                assert original['width'] > original['height']
                assert not any(abs(d.get('rotation',0)) == 90 for d in original.get('side_data_list',[])), 'Desktop must use native landscape footage'
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
assert {'C4417.MP4','C4345.MP4'} <= (shots['home'] | shots['carnival'])
assert not {'C4451.MP4','C0064.MP4','C0006.MP4'} & (shots['home'] | shots['carnival']), 'Rejected camera-facing speaking portraits returned'
for filename, start, end in intervals['home'] + intervals['carnival']:
    if filename == 'C4441.MP4': assert end <= 5, 'Use the reviewed early floor sequence, not the later shaky camera sweep'
for variant in ('wide', 'tall'):
    for ext in ('mp4', 'webm'):
        assert digests['home', variant, ext] != digests['carnival', variant, ext]
for slug in ('experiences', 'membership'):
    html = (ROOT / f'dist/{slug}/index.html').read_text()
    assert re.search(r'class="soft-hero[^"]*".*?<img', html, re.S)
print('PASS: valid distinct source intervals, native landscape homepage shots, no homepage split screens, movement/sound healing, responsive silent MP4/WebM, dimensions, durations, posters and subpage opening photos.')
