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

## Invitation behavior — updated 21 September 2026
The invitation dialog now carries a real enquiry form (name, email, optional WhatsApp, optional note, explicit consent tick), and a "Stay close" section above the footer takes an email address alone. Both post to FormSubmit, which emails the submission to the club's own address and sends the sender an instant auto-reply; nothing is stored on this site and no membership acceptance is simulated. The Instagram profile remains in the dialog as the second route. Delivery address and setup live in `data/site.json` (`form_endpoint`) and `notes/FORMS.md`; the forms do not deliver until the club clicks FormSubmit's one-time activation email.

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

## UI/UX pass — 21 September 2026
A full read of every page, state and breakpoint (360, 375, 768, 900, 1024, 1280, 1600 CSS px),
with the fixes applied in the same pass.

**Journey.** A visitor could read the whole page and still not know what actually happens after
she writes in — the steps only existed inside the invitation dialog. A `How joining works` section
now sits between A Private Circle and the Journal: write to us, we reply personally within two
days, we meet and then you join. It repeats the invitation CTA at the point where the question is
asked. Its wording describes the club's own stated process (invitation-only, limited membership,
venue shared privately); nothing about price, schedule or venue is invented.

**"Join the club" was a trap.** On a page about joining a members' club, an email field captioned
`Join the club` reads as a membership application. The inbox band now says `Join the list`, states
plainly that it is not an application, and links across to the invitation form.

**Accessibility.**
- Focus rings were `--ink` everywhere, so they vanished against the photographic header and hero.
  Those surfaces now take a `--paper` ring; the skip link takes terracotta, visible on both.
- Body copy on the beige *necessity* panel sat at 4.29:1 against its background. It now uses
  `--ink` (6.9:1). A full computed-contrast sweep of every text node against its painted
  background now reports no failures at AA.
- Form placeholders were `#a79b8d` on ivory (2.6:1) and now use `#776d60` (4.8:1).
- Accordion summaries were 30px tall; they and the footer's back-to-top link are now 44px.
  Remaining targets are all above the 24px WCAG 2.2 minimum.

**Layout and state.**
- Opening the mobile menu left the landing header transparent, so the ivory panel floated over the
  photograph with a seam above it. The header now takes an `is-nav-open` class: opaque ground,
  sage wordmark, dark toggle.
- `A WOMEN'S WELLNESS CLUB` / `IN COIMBATORE` ran together as `CLUBIN COIMBATORE` on phones, where
  the line break is suppressed. A space before the break fixes it at every width.
- Journal step headings in the new section are height-matched above 900px so the three paragraphs
  share a baseline.

**Pages.** `/thank-you/` was inheriting the home page title and had no `h1`; it now carries its own
title, og:title and heading. The journal breadcrumb's `Journal` step is a link rather than inert
text. No horizontal overflow and no console errors on any page at any width tested.

## Monthly gatherings — 21 September 2026
The club meets once a month, usually in the first week (confirmed by the client). That rhythm is
now stated in the A Private Circle section beside the existing venue note, where it needs no
maintenance.

A `What is coming up` section sits between How joining works and the Journal. It reads upcoming
gatherings from a Google Sheet the club publishes to the web, so the club edits its own dates with
no login, server or deploy. The section ships **dormant**: `gatherings_csv` in `data/site.json` is
empty, so only the standing line about dates travelling by email and WhatsApp is published, until
the client decides whether gathering dates should be public at all. Setup, the sheet's six columns
and the failure modes are in `notes/GATHERINGS.md`.

The loader is deliberately forgiving, and was verified against a deliberately messy sheet: past
rows drop off, rows marked `no` stay hidden, quoted commas parse, slash dates read day-first for
India, and a date it cannot parse is printed as typed rather than discarded. An empty, malformed or
unreachable sheet leaves the static fallback in place, so the sheet cannot break the page.

## Wellness Carnival event page — 29 September 2026
A one-off ticketed page at `/carnival/` for 20 December 2026, built from `data/event.json` by
`scripts/build_event.py` and styled only with the existing tokens: ivory ground, sage ticket
section, dusty-blue close, Nunito Sans with Pinyon Script accents, fine rules, square buttons, no
gradients. The client's draft (`preview.html`) did not bring over its bright gradient palette or its Playfair/DM Sans type.

**Copy is the client's, word for word.** Every visible line — headline, experiences, schedule,
ticket, "Who is it for?", FAQ answers, closing, booking bar — is taken from `preview.html` in its
order. Nothing is inferred or embellished (no weekday, no countdown, no per-item times outside the
schedule, no extra FAQs). The only non-preview words are structural labels (When, Where, Who,
Entry) and the breadcrumb. A text audit of the built page against the preview confirms this.

**Reference patterns.** Luma and Eventbrite put date, place, price and one booking action above the
fold and keep a slim booking bar within reach on long pages; the layout does the same with the
client's words.

**Payment.** Razorpay Payment Button, embedded in the ticket card, so checkout opens over the page
with no server. A hosted Payment Page link is the fallback. Until either is configured the card
shows the preview's own line, "Payment and ticketing link will be available at checkout." Setup
and open questions are in `notes/EVENT.md`.

**Lifecycle.** Homepage mentions (hero note, nav link from 1240px, featured row in *What is coming
up*) and all booking controls switch off in the browser once the evening ends. Deleting
`data/event.json` and rebuilding turns `/carnival/` into a redirect home.

**Checked.** 375, 1024 and 1440 CSS px; no horizontal overflow; no console errors. Content and SEO
checks pass, including an Event structured-data check.

## Landing montage from the club's own sessions — 30 September 2026
The misty landscape behind "The Sphere" is replaced by a silent, looping montage of two real Sphere
sessions: sound healing (10 July) and Kalaripayattu (4 September), from the club's Google Drive.
Chosen for the brief "people talking, smiling and doing wellness activities": every shot has people
moving; detail shots with no people (lanterns, plant, statue, empty bowls) were reviewed and left out.

- **Two cuts.** The Kalaripayattu session was filmed vertically, the sound session mostly
  horizontally. Phones get a tall 720×1280 cut, with vertical clips full frame (12 shots, 24 s).
  Desktop gets a wide 1600×900 cut (7 shots, 19 s) alternating full-frame landscape shots with
  triptychs — three vertical clips side by side divided by 6px Soft Ivory rules, echoing the
  hero's ivory frame — so vertical footage is never cropped to a sliver.
- **Edit.** In-points were picked from frame strips of each clip; shot list and crops are in
  `data/montage-home.json`. 0.6 s crossfades; the loop has no seam. All audio is removed.
- **Legibility.** The footage is dimmed (brightness .66, .58 on phones) with a soft shadow under the
  small hero copy so the ivory type reads over busy frames.
- **Behaviour.** The first frame is the poster, so the swap from still to video is invisible; the
  video loads only after the page has, never for reduced-motion or data-saver visitors, pauses off
  screen, and has a Pause control. One controller in `site.js` also drives the event-page montage.
- **Weight.** Wide ≈ 4.3 MB, tall ≈ 3.5 MB (WebM, with MP4 for Safari).
- **Rebuild.** Raw footage in `media/home/raw/` (git-ignored), then
  `python3 scripts/build_montage.py home && python3 scripts/build_site.py`. Delete
  `dist/assets/montage/` and rebuild to return to the landscape photograph.
- **Consent.** Participants are identifiable; the club confirms everyone visible agreed to appear.
