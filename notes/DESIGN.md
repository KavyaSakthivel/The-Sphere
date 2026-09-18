# The Sphere — design and content notes

## Direction
An editorial, typography-led site using the supplied sage/ivory identity, restrained circles, spacious composition, real photography, and no gradients. The original single-page composition, marketing headlines, invitation dialog, and five journal reflections are restored at the user’s request. All eleven PDF sections and all 103 source lines are incorporated into the main page. Journal listing titles and descriptions match the PDF; the original expanded reflections remain available in dialogs.

## Research — 18 September 2026
- https://www.instagram.com/thespherewomen/ — inspected public profile and feed. Sage circular identity, real gatherings, yoga and traditional movement. Its linked Google Form is for a June 6 gathering, so it is not presented as an upcoming event.
- https://www.the-well.com/ — inspected home page: restrained navigation, immersive imagery, serif-led wellness storytelling and a clear membership path.
- https://www.othership.us/ — inspected home page: experience-led navigation and clear explanations of practices and community; its louder visual language was intentionally not adopted.
- https://www.sixsenses.com/en/ — reviewed wellness/hospitality content structure and emphasis on experience and place.

This is a focused international reference set, not a claim to have reviewed every wellness club or an objective ranking.

## Assets
- Forest: Michael Held, Unsplash. https://unsplash.com/photos/green-trees-on-forest-during-daytime-gghk1DME6Cw
- Movement/conversation: Elina Fairytale, Pexels. https://www.pexels.com/photo/women-with-yoga-mats-talking-3823204/
- Tea: Prajna, Unsplash. https://unsplash.com/photos/a-cup-of-tea-sitting-on-top-of-a-table-3M1jYgYVQLk
- Licenses: https://unsplash.com/license and https://www.pexels.com/license/
- Fonts: Cormorant Garamond and DM Sans, served locally from Google Fonts downloads.
- These are illustrative stock photographs, not representations of Sphere members or venues.

## Invitation behavior
The restored invitation dialog leads to the verified Instagram profile. No contact details are collected or stored locally; no submission or membership acceptance is simulated. A live application endpoint can replace this flow when the club supplies its current membership intake process.

## Running locally
Run `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist` from the project folder.
The authored HTML, CSS, JavaScript, images and fonts are in `dist/`; no build dependencies are required.

## Content organization and verification
- The original single-page design is restored. All 103 source lines are present in `dist/index.html`.
- Original journal reflections and invitation dialog are restored, alongside the exact source titles and descriptions.
- `/experience/`, `/circle/`, and `/journal/` redirect to the corresponding sections to preserve interim links.
- `templates/original-index.html` preserves the initial design used by `scripts/build_site.py`.
- Run `python3 scripts/build_site.py` to regenerate the main page and legacy redirects.
- Run `python3 scripts/check_content.py` to check source coverage, local assets, original headlines and restored journal content.

## Additional international design references
- The Bothy by Wildsmith: https://heckfieldplace.com/the-bothy-by-wildsmith/spaces — natural photography and spacious, quiet composition.
- Asaya Hong Kong: https://www.rosewoodhotels.com/en/hong-kong/wellness — refined serif typography and restrained content hierarchy.
- Surrenne Belgravia: https://www.surrenne.com/en/destinations/surrenne-belgravia — warm neutral palette, fine rules, membership and journal navigation.
- THE WELL was revisited; its live page returned a server error on this pass. The prior successful visual inspection remains the reference.
- Six Senses wellness content was revisited via its official website.
