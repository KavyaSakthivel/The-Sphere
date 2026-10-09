# Authentic media review — 8 October 2026

Inspected all 36 original video clips at six temporal positions each (8%, 24%,
40%, 56%, 72%, 88% of duration), all 13 original camera RAW photographs, and 49
existing raster brand/editorial/site images. Selected source intervals and both
finished films were inspected again at the timestamps recorded in
`notes/MONTAGE-VALIDATION.json`. Contact sheets and the complete inventory remain
locally in `media/review/`. Original files were not modified.

The available real collection depicts two sessions in a studio, not a luxury
resort. The edit presents those sessions honestly through composed group scenes,
practice details and quiet portraits. Stock flowers, reading, pottery and
landscape images are no longer referenced by any generated public HTML page.
No synthetic photographs were created. Generic stock assets remain on disk so
existing files are preserved, but are not used on the pages.

## Original photograph decisions

| Source | Decision / strongest role |
| --- | --- |
| DSC09830 | Buddha detail; reviewed but omitted in favor of participants |
| DSC09831 | Warm, genuine smile; story opening and modern-woman journal cover |
| DSC09834 | Three-person conversation; story chapter and Carnival Connect |
| DSC09836 | Listening and eye contact; story chapter |
| DSC09837 | Similar conversation with a visible phone; omitted as redundant |
| DSC09840 | Bowl/instrument arrangement; Discover experience and still-life detail |
| DSC09846 | Seated meditation circle; story chapter |
| DSC09847 | Individual meditation; Reflect experience and slowing-down journal cover |
| DSC09852 | Facilitator and resting group; homepage interlude and wellness journal |
| DSC09876 | Bowl practice with participants; Experiences opening and Pause |
| DSC09881 | Resting participants; philosophy and beyond-checklist journal cover |
| DSC09893 | Intimate circle; homepage community section and story chapter |
| DSC09897 | Paired connection; Membership opening, homepage invitation, Connect and community journal |

Responsive exports preserve camera detail and use a modest exposure lift and
slight contrast adjustment. No facial retouching, replacement or generative edits.
All captions describe what is visible; no founder identity or testimonial is implied.
`data/media-selection.json` records the originals and exposure factors.
`scripts/prepare_authentic_assets.py` produces 640px, 1200px and 1920px WebP versions.

## Video decisions

| Sources | Review finding / use |
| --- | --- |
| C0001 | Native landscape circle establishes the homepage film |
| C0002 | Similar group angle, foreground obstruction; omitted as redundant |
| C0006, C0007 | C0006 removed as a camera-facing portrait; C0007 side-on seated facilitation closes the phone homepage |
| C0013 | Steady meditation portrait; selected for phone homepage |
| C0019 | Native landscape bowl practice; selected for desktop homepage |
| C0020 | Facilitator reaches over bowls; retained only in existing Carnival cut |
| C0021 | Broad resting-group scene; reviewed, C0022 gives a more intimate homepage angle |
| C0022 | Native landscape resting participants; desktop homepage closing scene |
| C0026 | Portrait setup with foliage drifting across frame; omitted |
| C0027 | Landscape hands/instruments detail; desktop homepage |
| C0028 | Landscape instrument arrangement; selected for Carnival detail |
| C0051 | Standing bowl practice; existing Carnival cut |
| C0059 | Seated stretching; still at 2.6s for Move, existing Carnival film |
| C0064 | Participant speaking; removed from Carnival |
| C4324 | Instructor with foreground backs; omitted from homepage |
| C4327 | Instructor then pan across participants; omitted from homepage |
| C4330 | Composed seated participants; phone homepage opening |
| C4338 | Moving pan across group; omitted |
| C4368 | Strong early group movement; selected for Carnival phone edit |
| C4372 | Rear-facing bending and walking; omitted |
| C4397 | Several direction changes/instructor turns; omitted |
| C4401 | Handheld movement and changing framing; omitted |
| C4417 | Early coordinated movement keeps bodies visible; phone homepage |
| C4420 | Rapid, inconsistent reframing; omitted |
| C4438 | Partner practice with backs in foreground; existing Carnival only |
| C4441 | Early floor practice, later sweeping pan; existing Carnival early interval only |
| C4451 | Removed from both montages at client request; separate welcome still remains |
| C4453 | Speaking with hand near face and changing gestures; omitted |
| C9985 | Lantern detail; reviewed, omitted in favor of meaningful practice detail |
| C9986 | Plant detail; reviewed, omitted as generic decoration |
| C9992 | Buddha/foliage detail; reviewed, omitted |
| C9993 | Steady portrait bowl arrangement; phone homepage |
| C9996 | Standing conversation with foreground back; omitted |
| C9997 | Conversation with camera drift; stills replaced by camera RAW photos |
| C9998 | Room setup; selected short interval closes Carnival phone edit |

## New homepage films

Desktop: C0001 establishes the circle, C0027 shows the craft, C0019 shows the
facilitator, and C0022 closes on shared stillness. All four are native landscape
clips. No portrait enlargement, split panels or static photos are used.

Phone: C4330 introduces the participants, C4417 shows movement, C0013 brings
stillness, C9993 shows the instruments, and C0007 ends on side-on seated facilitation. The separate
portrait composition preserves faces and body language.

Both edits use 90% playback speed and 0.65-second dissolves. They loop without a
hard cut, with no audio or frozen-frame padding. The desktop loop is 15.8 seconds;
the phone loop is 19.08 seconds. MP4 and WebM files are approximately 1.7–2.3 MB.
Posters match their encoded first frames. Pause/play, reduced-motion, data-saving
and off-screen pausing remain supported. Source intervals differ from Carnival.

## Rebuild and checks

1. Run `scripts/prepare_authentic_assets.py` with Python/Pillow and macOS RAW decoding.
2. Run `python3 scripts/build_montage.py home`.
3. Run `python3 scripts/build_site.py`.
4. Run content, SEO and montage checks.

Validated actual desktop and portrait playback sources, codecs, resolution,
duration, silence, valid source intervals, loop sample decoding and public image
references. Desktop and phone page crops were visually reviewed. No deployment.

## Client-requested montage revision

The attached screenshot identified C4451, a camera-facing participant. That clip
and the other speaking portraits C0064 and C0006 are excluded from both shot lists.
Carnival now uses authentic seated stretching, coordinated movement, bowl practice
and room preparation. The phone hero opens on a practitioner using a bowl, with
the framing positioned to keep her hands and instrument visible. The wide edit
uses the native landscape C0028 instrument detail instead of a portrait enlargement.
The homepage phone closing shot is side-on seated facilitation from C0007.

All four revised outputs were decoded at eight times and inspected in
`media/review/{home,carnival}-{wide,tall}-revised.jpg`. Duration and continuity
records are in `notes/MONTAGE-VALIDATION.json`. The latest build versions each
video URL so browsers load the replacement rather than a cached old edit.

## Client-selected DSC09844

The original DSC09844.ARW was retrieved from the client-provided shared Google
Drive folder (file 1r54uwAkbsJHr2ehft2LRuMoQBSTg3Vtv). The original 7008 × 4672
landscape photograph is exported as sphere-intimate at 640, 1200 and 1920px,
with the same modest exposure correction as the other real photographs.
It appears beside “Intentionally intimate” on both the homepage and Membership.
The complete 3:2 composition is retained, keeping the circle visible on phones.
The temporary screenshot crop has been replaced; no Drive interface is included.
