# Current direction — Sage & Stone, 8 October 2026

Derived from BrandGuideline.pdf. Five of the seven brand colours cannot carry text on ivory
(sage 2.05:1, dusty blue 2.16:1, coral 3.0:1, olive 3.6:1), so the palette adds one deep
sage anchor and gives every colour a single job. Tokens live at the top of `templates/finish.css`.

| Colour | Hex | Role |
| --- | --- | --- |
| Ivory | #FFF8EC | Page surface (brand) |
| Stone | #F1EADF | Alternate sections (lightened Warm Beige) |
| Deep sage | #24302A | Headings, buttons, footer, presence band, invitation |
| Olive grey | #5C6559 | Body text (darkened Olive Green) |
| Sage | #9AB7A8 | Logo, hairlines, labels on dark (brand) |
| Clay | #834C4D | Accent only: labels, active tab, hover, script words (brand Deep Terracotta) |

Muted coral and dusty blue are not used on the website. Photographs share one soft warm grade
and per-photo focal points that crop the studio equipment along the top of most frames.
Type returns to the brand stack (Avenir Next, bundled Nunito Sans elsewhere).

## Earlier direction (superseded)

# Current direction — cool petrol teal, 8 October 2026

The evergreen proposal below has been superseded by the client-requested cool
palette inspired by the presentation of Evolve for Her. The active colors are
petrol #123E46, deep teal #082C33, pearl #F6F8F6 and mineral mist #E1EBEB.
The original ivory and sage logo artwork is preserved. The Membership reader’s
note now uses a distinct pale mineral backdrop and framed letter-paper surface,
serif italic quotation and handwritten signature. Full rationale and reference
audit: `notes/EVOLVE-BRAND-ANALYSIS.md`.

## Previous direction

# Restrained color direction — 8 October 2026

The final client direction is polished, rich and quiet. The earlier multicolor
proposal has been replaced with a single evergreen family and two warm neutrals.
The supplied sage and ivory logo files remain unchanged.

| Color | Hex | Role |
| --- | --- | --- |
| Evergreen | #263A35 | Navigation, headings, invitation and primary actions |
| Deep evergreen | #1D2D28 | Footer and action hover |
| Original ivory | #FFF8EC | Main reading surface and light text |
| Warm stone | #F0EBE2 | Experiences, newsletter, story opening |
| Original sage | #9AB7A8 | Supplied footer logo |

Burgundy, gold and the filled sage sections have been removed. Headings use one
color instead of contrasting halves. Decorative rings have been removed. The
introduction and community sections use ivory; only the invitation and footer
use dark surfaces. The navigation is consistently evergreen for readable labels
and the supplied ivory logo over every video frame.

The more compact section rhythm from the spacing pass remains. The hero now
scrolls naturally without contracting its video or fading out the headline.
The palette is in `templates/luxury.css`, appended after the existing editorial
styles by `scripts/build_site.py`. Legacy wine/champagne/brass token names are
aliases to this restrained family, preventing older components from adding colors.

See `notes/MEDIA-REVIEW.md` for the authentic image selections and new films.
Changes are local; no public deployment has been made.
