# Updated 8 October 2026

The homepage edit below has been superseded by the calm, single-frame edit in
`notes/MEDIA-REVIEW.md`. Current shot list: `data/montage-home.json`.
Desktop 15.8 seconds; phone 19.08 seconds. Carnival remains independent.

## Previous edit record

# Independent landing-page films

Both pages use only footage from the supplied Sphere collection in `media/home/raw/`.
The raw files remain local and unmodified. Published videos have no audio track.

| Page | Direction | Desktop | Phone | Shot list |
|---|---|---|---|---|
| Sphere | Kalari-led group movement, stillness and bowls | 19.3 seconds | 17.9 seconds | `data/montage-home.json` |
| Carnival | Kalari, movement, facilitated wellness and conversations | 18.8 seconds | 15.5 seconds | `data/montage-carnival.json` |

The homepage now opens with coordinated group Kalari movement from `C4417` and the steady
early portion of `C4368`, followed by sound healing and front-facing group movement from `C4397`.
The rear-facing bending shot from `C4372` has been removed. Seated
instruction and the static detail shot were replaced to make the movement more visible.
Desktop uses paired portrait scenes to keep full bodies in view; phone uses full-frame portrait
footage. Both formats on both pages include Kalari and sound-healing sessions.
The pages use distinct edits and source intervals, including different portions of `C4438`.
Carnival shows past gatherings as an introduction to the experience,
not footage of the upcoming December event. Each page has a wide desktop cut and a separately
selected portrait phone cut, encoded as MP4 and WebM with a matching first-frame poster.

Camera-motion estimates and beginning/middle/end frame inspection were used to select intervals.
The early `C4441` floor sequence (0.8–4.4 seconds) is used; its later shaky camera sweep remains
excluded. Handheld group `C9997` and rapidly moving `C4420` remain excluded. Portrait Kalari
sequences are framed individually for desktop so faces and training gestures stay visible.
Clips have slight slow motion and one-second crossfades, including the last shot
back into the first. Short source intervals are rejected rather than padded with a frozen frame.
`notes/MONTAGE-VALIDATION.json` records decoded-frame continuity checks at the loop boundaries.

Rebuild:

```
python3 scripts/build_montage.py home
python3 scripts/build_montage.py carnival
python3 scripts/build_site.py
python3 scripts/check_montages.py
python3 scripts/check_content.py
python3 scripts/check_seo.py
```

The site build adds content versions to montage sources and posters. The existing play/pause,
off-screen pause, reduced-motion and data-saving behavior remains in place.

Experiences and Membership now open with full-width photographs. Philosophy retains its photo
opening, and each journal article has a relevant opening image. Desktop and phone layouts,
in-page links, actual responsive playback sources and pause/play controls were checked locally.
