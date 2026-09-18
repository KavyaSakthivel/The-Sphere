# The Sphere — design and content notes

## Direction
An editorial, typography-led site using the supplied sage/ivory identity, restrained circles, spacious composition, real photography, and no gradients. All eleven sections in THE SPHERE.pdf are represented across four pages. Website content is limited to the user-supplied text; the journal contains only the supplied titles and descriptions. The earlier drafted articles and added marketing copy have been removed.

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
The Request an Invitation link opens the verified Instagram profile directly. No contact details are collected or stored locally; no submission or membership acceptance is simulated. A live application endpoint can replace this flow when the club supplies its current membership intake process.

## Running locally
Run `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist` from the project folder.
The authored HTML, CSS, JavaScript, images and fonts are in `dist/`; no build dependencies are required.

## Content organization and verification
- `/`: THE SPHERE, A SPACE THAT FEELS LIKE YOURS, WHY THE SPHERE?, IS WELLNESS A LUXURY OR A NECESSITY?, A NOTE FROM THE SPHERE.
- `/experience/`: THE SPHERE EXPERIENCE, MORE THAN WELLNESS, CURATED EXPERIENCES.
- `/circle/`: THE WOMEN OF THE SPHERE, A PRIVATE CIRCLE.
- `/journal/`: THE SPHERE JOURNAL.
- `notes/content.txt` matches the supplied PDF after normalizing whitespace and apostrophes.
- Run `python3 scripts/build_site.py` to regenerate the four static pages.
- Run `python3 scripts/check_content.py` to check all 103 source lines and local references. It writes `notes/content-coverage.json`.
