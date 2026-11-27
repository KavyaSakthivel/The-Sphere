# Carnival page: introducing the two artists (24 November 2026)

What was looked at, and what it actually gave us. Searches were run on 24 Nov 2026.

| Source | What it showed | Use for The Sphere |
|---|---|---|
| Dribbble / Contra search ("wellness retreat event landing page facilitators") | General wellness landing pages; no Dribbble shot with a facilitator or artist line-up section surfaced | Little. Confirms the calm, photo-led look the site already has |
| [Awwwards: Klangtherapie Festival line-up](https://www.awwwards.com/inspiration/artist-cards-klangtherapie-festival) (agentur-brandmarker) | Tagged line-up, grid, filter, card, popup: artist cards that open into a detail view | The card idea. With two artists a filterable grid is overkill, so each gets one large editorial card instead |
| [Awwwards: Festivent mobile](https://www.awwwards.com/inspiration/mobile-festivent) (Monument) | Image only, no described pattern | None |
| Ticketed event pages already followed (Luma, Eventbrite, District; see notes/EVENT.md) | Essentials and price on the first screen | Kept: the artists are added without pushing date, venue or price down |
| Custom cursor guidance ([MDN cursor](https://developer.mozilla.org/en-US/docs/Web/CSS/cursor), [Eric Bailey, "Don't use custom CSS mouse cursors"](https://ericwbailey.website/published/dont-use-custom-css-mouse-cursors/)) | Keep images 32px, set the hotspot, always give a keyword fallback; custom cursors ignore Windows pointer-size settings | Flame on the carnival page only, mouse/trackpad only, text cursor kept in fields |

Figma: no reference file was supplied, so nothing was read from Figma.

## Decisions

- The artists are named in the opening film ("Featuring Alena Gukina & Deepa", linked to their section), so they are seen on the first screen on phones as well as desktop.
- A dark, ember-toned section comes straight after the essentials: two tall cards, the second set lower for an editorial rhythm, each with what the artist leads (the poster's own lines) and her Instagram.
- Until the club sends approved portraits, each card shows a line motif on a warm glow (fire for Alena, cacao for Deepa). Photos taken from Instagram are not used.
- The programme marks the artists' sessions ("Led by ...") and links back to their cards.

## Glow cursor (24 November 2026)

The client asked for a glowing, circular cursor that leaves a trail, replacing the flame.

| Source | Pattern |
|---|---|
| [Framer: Glow Trail Cursor](https://framer.com/marketplace/components/glow-trail-cursor/?via=elliot-li) | Dots that follow the pointer with a layered glow; dot count, fade time, glow softness adjustable |
| [Awwwards: Cursor Bloom Trail (Broth)](https://www.awwwards.com/inspiration/cursor-bloom-trail-broth), [Mouse Follower (Eduard Bodak)](https://www.awwwards.com/inspiration/mouse-follower-eduard-bodak-portfolio) | A soft bloom trail; a ring that lags behind a precise dot |
| [DEV: glowing mouse trail with canvas](https://dev.to/mawayalebo/creating-an-interactive-glowing-mouse-trail-with-html5-canvas-and-javascript-4a04), [DEV: spring-based cursor trail](https://dev.to/uuuulala/coding-an-interactive-and-damn-satisfying-cursor-7-simple-steps-2kb-of-code-1c8b) | Canvas, requestAnimationFrame, fading circles |

Built: a warm orb that eases after the pointer and leaves a short fading trail (about 0.65 s), drawn on one
canvas, with a sharp ivory dot exactly on the pointer so clicks stay precise. It swells slightly over links and
buttons. No library. Mouse and trackpad only; reduced-motion, touch, text fields and open dialogs keep the normal
cursor. It stops drawing when the pointer rests.
