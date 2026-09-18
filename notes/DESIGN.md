# The Sphere — design and content notes

## Direction
An editorial, typography-led site using the supplied sage/ivory identity, restrained circles, spacious composition, real photography, and no gradients. All twelve topics in THE SPHERE.pdf are represented. Five short journal reflections were newly drafted from the supplied titles and themes; they should receive the club's editorial review before public launch.

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
The enquiry dialog opens the verified Instagram profile. No contact details are collected or stored locally; no submission or membership acceptance is simulated. A live application endpoint can replace this flow when the club supplies its current membership intake process.

## Running locally
Run `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist` from the project folder.
The authored HTML, CSS, JavaScript, images and fonts are in `dist/`; no build dependencies are required.
