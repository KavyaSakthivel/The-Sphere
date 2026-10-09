# Carnival mobile experience

The mobile layout takes cues from the client's Learnvium workshop reference:
rounded cards, compact information, touch controls and a persistent action near
the bottom of the screen. The Sphere's existing teal palette, photography and
event copy are retained.

At 700px and below, the carnival has a compact header and rounded film, event
detail cards, a native swipe gallery with previous/next controls, schedule cards,
and a bottom navigation dock with price and a ticket action. The current section
is highlighted as the visitor scrolls. The dock respects phone safe areas and
steps aside for the site menu. Mobile content appears immediately when jumping
between sections. Desktop keeps its existing composition and booking-bar behavior.

Authoring: `scripts/build_event.py`, `templates/event/event.css` and
`templates/event/event.js`. Generated output: `dist/carnival/`.

Booking is still in `soon` mode in `data/event.json`. The dock says “View tickets”
and links to the ticket section, where the existing booking-opening-soon message
is shown. Configured payment links or Razorpay buttons retain their existing flow.

Verified in Chromium at 320, 375, 390 and 430px phone widths, 768px tablet and
1440px desktop. No horizontal page overflow. Checked section links and active
states, carousel navigation, FAQs, menu opening/Escape, and reduced-motion film
and carousel behavior. Content and SEO validation scripts pass.

Preview: `notes/carnival-mobile-app.png`. Local page:
`http://127.0.0.1:4173/carnival/`. Changes have not been published.
