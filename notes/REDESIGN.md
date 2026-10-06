# Sphere: premium redesign, 6 October 2026

The new homepage is a quieter invitation into a real women’s circle. It uses the supplied
wordmark and exact ivory, sage and terracotta palette, and the club’s existing session footage.
The references are Surrenne, Equinox and Luxe Wellness Club. The layout and motion are original
Sphere compositions; no photographs, copy, fonts or code were copied from those sites.
Surrenne's stylesheet did not render in the inspection browser, so its precise live animations
were not verified. Equinox and Luxe's rendered opening layouts were inspected.

## Changes

- A full-screen silent film with one eight-word headline and a single entry link.
- Four longer, full-frame shots per device with gentle crossfades. Triptychs removed.
- A brief pinned desktop opening that contracts into the page as it scrolls; no scroll hijacking.
- Soft section reveals, restrained image parallax and small link/photograph hover responses.
- Real gathering images, a staggered experience gallery, a more prominent personal brand note.
- Sparse handwriting, clean Avenir/Avenir Next where installed, bundled Nunito Sans elsewhere.
  Licensed Avenir and Florelie webfont binaries were not supplied or redistributed.
- A clear separation between the private monthly circle and the public Wellness Carnival.
- A shorter homepage, with the complete 103 source lines retained on the linked philosophy page.
- Consistent compact navigation on home, philosophy and journal pages.
- A readable ivory footer, invitation enquiry, existing journal dialogs and crawlable articles.
- Reduced-motion and data-saving visitors get a poster rather than autoplay. A visible pause
  control, off-screen pausing and hidden-tab pausing avoid unnecessary continuous playback.

The note remains attributed to The Sphere because the documents do not supply a founder's name,
portrait or personal testimony. No member quotes, venue promises or exclusivity claims were invented.

## Authoring and regeneration

- `templates/premium-main.html`: concise homepage composition.
- `templates/premium.css`: homepage styling and shared editorial shell.
- `templates/motion.js`: reveal and scroll behaviour.
- `scripts/premium.py`: integration, extended philosophy page and event hooks.
- `dist/site.js`: maintained site behaviour, forms, menus, journal and film controls.
- `scripts/prepare_premium_assets.py`: reproducible stills from local session footage.
- `data/montage-home.json`: revised hero-film shot list.

Run `python3 scripts/build_site.py` after edits. If media changes, run
`python3 scripts/prepare_premium_assets.py` and `python3 scripts/build_montage.py home` first.
Raw sources in `media/` are local and ignored by Git; published stills and silent loops live in
`dist/assets/`. Each script/style URL is versioned by its contents during the build.

Preview: `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`.

## Verification

Following the Equinox and Evolve reference review, the carnival now has a full-width film opening,
a short headline, a prominent header ticket action, and practical facts immediately below the film.
Its photo-led experiences use slow masked reveals; the detailed list sits in a disclosure.
The booking bar stays hidden in the opening and ticket section, and appears between them.
The supplied C9997 group-conversation still replaces the single-person Connect photo.
The homepage's full experience directory, membership details and brand letter now live on
`/experiences/` and `/membership/`, which are included in the sitemap. All supplied source copy
remains accessible. Checkout remains pending the client's payment URL.

The Wellness Carnival promotion opens in a homepage entry dialog, once per tab session.
It uses the current ivory/terracotta theme and a supplied Sphere photograph, links to `/carnival/`,
and supports close, Escape and a continue button. The homepage has no permanent carnival section.
At the client's latest request, a seasonal Carnival link appears in desktop and mobile navigation
across the site. `data/event.json` sets `promotion_until` to 1 January 2027 at midnight India time;
the browser suppresses the popup and removes the navigation link then even without a new deployment.
Future builds also omit them. The event landing page is retired separately by removing its
configuration and rebuilding.

The philosophy now has an image-led opening, alternating photo/copy chapters and five visual
experience pillars. Its full supplied copy is preserved. The `/experiences/` accordion is replaced
by the same always-visible photo atlas. The palette follows the brand and Evolve's editorial rhythm;
Pexels source credits and the verified licence are recorded in `dist/assets/PHOTO-CREDITS.md`.

- Content audit: all 103 source lines present, local references resolve.
- SEO audit: home, five articles, philosophy and event canonicals and discovery pass.
- JavaScript syntax checks and `git diff --check` pass.
- Browser: desktop and narrow phone layouts inspected; no horizontal overflow or console errors.
- Invitation opens from desktop and phone navigation; Escape returns focus to the trigger.
- Empty enquiry validation blocks submission before any external request.
- Journal dialog opens with the correct article; close returns focus to its link.
- Film pause/play state and accessible control labels checked; off-screen film pauses.
- Reduced-motion branches reviewed in CSS and JavaScript; an emulated reduced-motion browser
  was not available through the inspection surface.
- External FormSubmit delivery was not exercised. The existing inbox activation remains a club
  setup requirement, documented in `notes/FORMS.md`.

Existing in-progress event-page edits were retained. This redesign is local; no public deployment
was made during this request.

## Evolve reference refinement — 6 October 2026

Studied Evolve's live desktop navigation, film opening, generous gallery spacing and wellness
pillars. Sphere now uses balanced navigation around its own wordmark, a smaller single-line
desktop film headline, centered introductory copy, and five interactive photographic pillars.
The community and membership sections use different image proportions and quieter backgrounds.
Sphere's supplied palette, original footage and complete source copy remain in use.

`templates/editorial.css` contains this refinement and is appended to the generated premium
stylesheet by `scripts/build_site.py`. The pillar browser progressively enhances the full list:
without JavaScript, every experience remains readable. Keyboard arrows, Home and End change
the active tab; reduced-motion preferences disable the transition animations.

Verified desktop and phone layouts, one visible panel per selection, keyboard tab switching,
loaded images, the prominent invitation action, and mobile navigation to Carnival. Content and
SEO audits pass. Carnival booking remains pending the client's checkout URL.
