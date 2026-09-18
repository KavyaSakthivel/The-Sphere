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

## Supplied brand identity — September 18 update
- Reviewed all six BrandGuideline.pdf pages, nine logo variants, transparent PNGs, and six Post1 social creatives.
- Applied exact Soft Ivory #FFF8EC, Sage Green #9AB7A8, Dusty Blue #93B0C2, Warm Beige #DFC6B6, Deep Terracotta #834C4D, with coral/olive supporting accents. Dark neutral text provides readable contrast on lighter brand colours.
- Supplied SVG 01/02 wordmarks replace the approximate text logo. Only artboard/background removed for responsive placement; original path geometry and colours preserved. 172px+ wordmarks retain 45mm-equivalent minimum width and generous clear space.
- Supplied SVG 07 circle lockup anchors membership and supplies the favicon; its original circular artwork is used over the forest photograph. No invented replacement logo or gradients.
- Primary typography now Avenir Next / Avenir where locally installed, with bundled DM Sans fallback elsewhere. Florelie local support for restrained accents, with existing Cormorant italic fallback. No font binaries were supplied; commercial/system fonts were not extracted or redistributed.
- Post1 contains finished text-over-photo social compositions, not clean standalone photography. Reviewed as brand reference; retained existing photography to avoid duplicated copy and baked-in tiny text.
- Original editorial structure, complete PDF source copy, invitation behavior and five restored journal reflections remain.
- scripts/prepare_brand.py reproduces web-ready SVGs from the provided originals.
- QA: desktop (1309 CSS px) and mobile (354 CSS px) screenshots reviewed; no horizontal overflow. All seven image instances load. Invitation dialog, mobile menu, journal dialog and experience accordion checked. No browser console errors. Content audit passes all 103 source lines; JavaScript syntax and diff checks pass.

## Approved free typography alternatives
- User selected free alternatives to the guideline's commercial Avenir Next and Florelie fonts.
- Nunito Sans now supplies primary body, navigation and headings; Allura supplies handwritten accents, replacing the serif fallback. Font stacks no longer depend on locally installed brand fonts.
- Six actual TTF webfonts downloaded from the official Google Fonts CSS API / fonts.gstatic.com: Nunito Sans Regular, Medium, SemiBold, Bold, Italic, plus Allura Regular. Source URLs and the SIL Open Font License texts are included in dist/assets/fonts.
- Direct versioned font CSS and hero font preloads replace the old nested CSS import to prevent stale fallback rendering on returning browsers. Script uses natural non-italic style, zero letter spacing, and adjusted sizing/line heights.
- Verified font resource responses, desktop and mobile screenshots (1309 / 354 CSS px), no horizontal overflow, no console errors, and mobile journal and invitation dialogs. All 103 brief lines remain covered by the existing content check.
- Personal-use Florelie demo remains outside deployment output in font-review and is not included in the website.

## Coimbatore SEO preparation
- Confirmed location: Coimbatore, Tamil Nadu; venues change and are communicated by email or WhatsApp. These details now appear naturally in the homepage.
- data/site.json centralizes the canonical origin and confirmed business details. Domain remains unconfirmed; current Sites audience remains owner-private.
- scripts/seo.py generates six canonical pages, unique metadata, Organization/WebSite/WebPage/Article/BreadcrumbList JSON-LD, sitemap.xml and robots.txt. Legacy section redirects are excluded from the sitemap and marked noindex,follow.
- Five existing approved journal reflections moved into data/journal.json, shared by crawlable article pages and the original homepage dialogs. Article pages retain the brand's typefaces, colours and navigation.
- Responsive forest WebP files reduce hero transfer size by approximately 60–85% compared with the existing JPEG. This is an asset-size comparison, not a measured Core Web Vitals claim.
- Content coverage and SEO tests pass; desktop/mobile article layouts, homepage journal dialog and mobile navigation checked with no horizontal overflow or console errors.
- notes/SEO-HANDOFF.md records domain connection, public launch, canonical migration, Search Console and eligibility-aware local discovery steps for the marketer.

## Persistent navigation and reference-inspired footer
- Navigation remains visible throughout scrolling and becomes a compact ivory bar after the first 48px. Reserved document space keeps the content from jumping; anchor offsets leave section headings below the bar.
- Mobile navigation opens beneath the measured header, with a scrollable panel on shorter screens. Existing menu closing and Escape behavior remain.
- Replaced the dark footer with an airy ivory four-column layout: supplied wordmark, existing brand/location copy, section links, Instagram and an underlined invitation link. It rearranges into two link columns on mobile.
- Used the existing membership destination rather than adding an unconnected newsletter form. Footer and persistent navigation are shared by all five journal pages.
- Verified desktop and mobile scrolling, header position, section clearance, menu interaction, footer layout, no horizontal overflow and no console errors. Existing content and SEO checks pass.

## Direct invitation and editorial photography refresh
- Header, mobile menu and footer invitation links now open the existing dialog immediately. The private-circle navigation link still leads to its descriptive section. Journal pages include the same invitation dialog, so their headers behave identically.
- Normal links remain as a progressive fallback. Modal closing returns focus to its trigger, or the visible menu button for mobile navigation.
- Reviewed Surrenne (https://www.surrenne.com/en), The Bothy (https://heckfieldplace.com/the-bothy-by-wildsmith/spaces), Pinterest retreat references and Dribbble wellness directions. Chose warm natural-light human photography over generic nature imagery and literal facility imagery.
- Replaced forest, yoga-mat conversation and teacup photos with a singing-bowl session, two women making pottery, and hands shaping clay. All three are licensed Pexels images; source URLs and photographer credits are recorded in dist/assets/PHOTO-CREDITS.md.
- Removed oversized rings and dark grading from the hero photograph, preserving the supplied rings in the membership lockup. Retained image labels and a small ivory note. Responsive WebP versions are 640px and 1200px wide.
- Illustrative photographs do not represent Sphere members or permanent premises. No new service claims, article copy or venue details were added.

## Panoramic landing and calligraphic typography
- Adapted the user's Elysian Club reference (https://dribbble.com/shots/27516845-Wellness-Club-Website-Design-Concept) into a full-height framed landscape with a centred supplied logo, quiet side copy, large ivory title and centred pill CTA.
- Self-hosted SIL OFL Pinyon Script replaces Allura as the decorative face. It is a freely licensed interpretation of the reference, not a claim to use its exact proprietary typeface. Nunito Sans remains the readable body and navigation face.
- Script now carries through section accents, experience headings, journal titles, membership details and the invitation dialog. Original PDF text and restored journal reflections remain intact.
- Used a real licensed misty landscape photograph. Retained the existing pottery/community photography below the hero. Photograph and font sources are included beside the assets.
- Checked desktop and mobile hero screenshots, mobile section and journal typography, sticky navigation, anchor clearance and one-click invitation opening/closing. No mobile horizontal overflow or browser console errors observed. Content coverage passes all 103 source lines and SEO checks pass for six pages.
