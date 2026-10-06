# The Sphere Wellness Carnival — event page

A one-off page for the evening on Sunday 20 December 2026, living at **`/carnival/`** on the existing
site. No subdomain, no server, no second host.

## Where everything lives

| What | File |
|---|---|
| Every fact and switch (date, venue, price, payment, refund text) | `data/event.json` |
| Page layout and copy (copy is word for word from `preview.html`) | `scripts/build_event.py` |
| Page styles and behaviour | `templates/event/event.css`, `templates/event/event.js` |
| Homepage entry popup layout, styles and behaviour | `scripts/premium.py`, `templates/premium.css`, `templates/motion.js` |
| Generated output | `dist/carnival/` |

`python3 scripts/build_site.py` builds it with the rest of the site. The homepage gets an entry
popup and a seasonal Carnival navigation link on desktop and mobile. Both expire after December
using `promotion_until`, even if nobody rebuilds. The permanent homepage has no event section.

## Page layout (4 October 2026)

Follows the pattern ticketed event pages share (Luma, Eventbrite, District): the first screen carries the
date, time, venue, who it is for, the price and the booking button in one card, so a visitor can book
without scrolling. Then the preview's section links (Experience, Schedule, Tickets, FAQs), the
introduction, the experiences as icon cards, the hour-by-hour timeline, *Who is it for* (moved before
the price to answer doubts first), the ticket, questions and the closing invitation. Item titles are in
plain type for quick scanning; the script face is kept for headline accents. The booking bar appears
once the opening card scrolls away and, on wide screens, also carries the section links.

## Booking modes

The page picks its mode from `data/event.json`:

| Setting | What visitors see |
|---|---|
| nothing set (now) | The ticket card shows the preview's own line, "Payment and ticketing link will be available at checkout." No button |
| `razorpay_button_id` | **Recommended.** Razorpay's checkout opens on top of the Sphere page |
| `payment_url` | Every Book button goes to a hosted Razorpay Payment Page |
| after 10 PM on the 20th | Automatic: every booking button and the booking bar disappear |

## When the client sends the payment link

One command, run from the project folder, then deploy `dist/` as usual:

```bash
python3 scripts/set_payment.py "PASTE-THE-LINK-HERE"
```

It accepts whatever Razorpay (or another provider) gives them:

- **A payment link or Payment Page URL** (`https://rzp.io/...`, `https://pages.razorpay.com/...`, or any
  `https://` link): every booking button on the page (header, hero, ticket card, closing section and
  the follow-along bar) goes straight to it.
- **A Razorpay Payment Button** (the embed code, or just its `pl_...` id): Razorpay's own button
  appears in the ticket card and checkout opens on top of the page.

It refuses anything that is not a secure `https://` link, and prints how many buttons it connected.
`python3 scripts/set_payment.py --off` goes back to "Payment and ticketing link will be available at
checkout." The link is stored in `data/event.json` (`payment_url` / `razorpay_button_id`).

## One-time Razorpay setup (the club does this in the dashboard; no code)

1. **Open a Razorpay account and finish KYC now.** Activation needs business documents and can take
   several working days; live payments cannot start before it clears.
2. In **Account & Settings → Branding**, upload the circle logo and set the brand colour to
   `#834C4D` (Deep Terracotta), so checkout matches the site.
3. **Payment Button → Create → Quick Pay / custom.** Set:
   - Button label: `Book your place`, theme **Brand Color**.
   - Amount field: **Item with Quantity**, name `Entry ticket`, price ₹2,799, stock **limited** to
     the venue capacity. Stock is what stops overselling.
   - Customer details: name, email, phone (label it *WhatsApp*). Add a field for guest names if
     couples book two tickets.
   - Receipts on. After payment: show Razorpay's own success message (the site has no
     confirmation page, because the preview has no copy for one).
4. Run `python3 scripts/set_payment.py` with the button's embed code or `pl_…` id (see above), then deploy.
5. Make one real ₹1 test (temporarily change the price), refund it from the dashboard, then set the
   price back. When stock runs out, Razorpay deactivates the button on its own.

The **attendee list** for the door is the button's payments in the Razorpay dashboard, exportable
as a spreadsheet.

**"+ applicable fee"**: Razorpay only adds the gateway fee on top of the ticket if the account has
the customer-pays-fee (convenience fee) option enabled — ask Razorpay support. Without it, the fee
comes out of the ₹2,799, and `price_note` should be emptied so the page does not promise a fee
that never appears.

## Content rule

Every visible word on the page comes from `preview.html`. Anything new — refund wording, a couple
price, a confirmation message — should come from the club before it goes on the page.

## Still to confirm with the club

- **Couples:** one ticket each (₹2,799 × 2), or a couple price? If different, add a second amount
  field in Razorpay and put the wording in `ticket_note`.
- **Refunds and transfers:** put the policy in `refund_policy`; it then appears as a question in the
  FAQ. It is deliberately not shown until it exists.
- **Capacity**, for the Razorpay stock limit.

## Hero montage (optional)

The photograph beside the headline can be replaced by a silent, looping montage of the club's own
footage. Nothing is set up until clips exist; the page shows the photograph meanwhile.

1. Put clips and/or photos in `media/carnival/`. They play in name order, so name them `01-…`,
   `02-…`. Six to ten shots is plenty. Raw footage is git-ignored and never published.
2. Run `python3 scripts/build_montage.py`, then `python3 scripts/build_site.py`, then deploy.

What the script does: takes about 3 seconds from each clip (skipping the first fifth, where phone
footage is usually unsteady), gives photos a slow push-in, crops everything to the 4:5 portrait hero
frame, crossfades between shots, loops without a visible jump, and removes all sound. Output is in
`templates/event/montage/` (MP4 + WebM, around 0.15 MB per second, plus a first-frame poster). It
warns if the files pass 6 MB.

On the page the video starts muted and silent, has a Pause button, rests when scrolled out of view,
and does not play at all for visitors whose phones ask for reduced motion or data saving. They see
the first frame as a still. To go back to the photograph, delete `templates/event/montage/` and
rebuild.

**Footage to ask the club for:** vertical phone clips, held still for 5 seconds or more, of previous
gatherings — breathwork, sound bowls, food, people talking or dancing. Centre the subject, because
landscape clips are cropped at the sides. **Anyone recognisable must have agreed to appear on a
public web page.**

## After the event

The current carnival design uses the responsive home montage with a short cinematic opening,
then a fact row, three editorial photos, the evening schedule, tickets and FAQs. Reveals respect
reduced-motion preferences. The filled header action remains visible on phones. Until the client
supplies a payment link, ticket actions lead to the ticket section with a booking-soon notice.

The seasonal homepage entry popup expires automatically on 1 January 2027 at midnight India time,
using `promotion_until` in `data/event.json`. It appears once per tab session, links to the event
landing page and can be dismissed. A seasonal Carnival link is present in desktop and mobile
navigation, expires at the same time, and points to `/carnival/`. No permanent homepage event
section is present.

Nothing is required on the night. When convenient: delete `data/event.json`, run
`python3 scripts/build_site.py`, deploy. `/carnival/` becomes a redirect to the homepage so links
shared on WhatsApp and Instagram still land somewhere; the homepage mentions and sitemap entry are
gone. `templates/event/` can stay as the starting point for the next event.

## Sources

- [Razorpay Payment Button FAQs](https://razorpay.com/docs/payments/payment-button/faqs/) — brand colour theme, item with quantity, stock, settlement.
- [Create a Razorpay Payment Page](https://razorpay.com/docs/payments/payment-pages/create/) — stock, min/max quantity, expiry, redirect after payment.
- [Customise Payment Pages](https://razorpay.com/docs/payments/payment-pages/customise/) — pre-filled fields.
