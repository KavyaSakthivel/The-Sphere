# Carnival bookings and Meta Conversions API

For the developer. Nothing here is operated by the club: the founder keeps using the Razorpay
dashboard as before, and Naveen reads results in Meta Events Manager.

## What it does

```
carnival page ──POST /api/bookings──▶ server.js + backend/ ──create Payment Link──▶ Razorpay
   (1–10 tickets, optional consent)        (MySQL: bookings)                            │
                                                                                          ▼
Meta Events Manager ◀──Purchase (CAPI)── backend/ ◀──payment_link.paid (signed)──  guest pays
```

1. A guest picks a ticket count on `/carnival/`. The server prices it from `data/event.json`
   (never from the browser), saves a booking, and creates **that booking's own** Razorpay Payment Link,
   tagged `notes.source = website`, `booking_id`, `quantity`.
2. The guest pays on Razorpay's hosted checkout. Card and UPI details never reach our server.
3. Razorpay calls `POST /api/webhooks/razorpay`. The server checks the HMAC signature on the raw
   body, recognises the link as a website booking, and reconciles link status, payment status,
   currency, link amount and amount paid against the booking. Anything that does not match is held
   as `review` and never sent.
4. The server sends one `Purchase` to the Conversions API with the amount in INR, quantity and
   booking ID. `event_id = purchase.<booking id>` is fixed per booking, and a database claim
   prevents a second send, so retries and duplicate webhooks still give exactly one Purchase.
5. If Meta is down or the token is missing, the Purchase waits and is retried with backoff
   (1 min → 4 h, up to 8 attempts, within Meta's 7-day window).

Links made by hand in the Razorpay dashboard (the WhatsApp link), QR payments and the shared
`payment_url` are **not** website bookings: they also fire webhooks, and they are ignored. That keeps
Meta's ad optimisation trained only on sales that went through the website.

If the API is unreachable, the dialog offers the shared Razorpay link instead, and every booking
button keeps that link as its `href`, so without JavaScript booking works exactly as before.
Those sales are simply not reported to Meta.

## Naveen's requirements, and where each one is met

| Requirement | Where |
|---|---|
| Conversions API on the backend | `backend/meta.js` (`purchaseEvent`, `createMeta`) |
| `payment_link.paid` webhook | `backend/app.js` → `webhook`, `handleEvent` |
| Verify Razorpay webhook signatures | `backend/razorpay.js` → `verifyWebhookSignature` (HMAC-SHA256, constant time, raw body) |
| Purchase only after verified payment | Signature + reconciliation of status, currency and amounts against our own booking |
| Actual amount, in INR | `value` = amount paid ÷ 100, `currency: INR` |
| Ticket quantity and booking/order ID | `num_items`, `contents[].quantity`, `order_id` = booking ID (also Razorpay `reference_id`) |
| `fbc` / `fbp` where available and consented | Read from the pixel's first-party cookies (or built from `fbclid`) only when the guest ticks the consent box |
| Unique event ID, duplicate prevention | `event_id = purchase.<booking id>`, webhook event log, atomic claim in the database |
| Test 1, 2 and 3 tickets in Test Events | `npm test` covers all three; the live test is below |

Without consent, nothing about the booking is sent to Meta. We would hold nothing Meta can match on,
and it refuses such an event ("no customer information parameters"; seen in live testing). The sale is
still paid and recorded here (`meta_status = skipped`), and `npm run bookings -- stats` counts it.

## Hostinger setup (once)

Today Hostinger serves `dist/` as static files; `server.js` is not running. The API needs the site
to run as a Node.js app:

1. **Websites → spherewellness.in → the Git deployment settings.** Keep the repository and branch.
   Set the Node.js version to **20 or 22** (18 is end-of-life). Install command `npm install`
   (or `npm ci`), start command `npm start` (entry file `server.js`). Remove any static output-directory
   setting so the start command serves the site. `server.js` serves every page in `dist/` exactly as
   now, plus `/api/`.
2. **Databases → MySQL Databases.** Create a database and user. The tables are created on first start.
3. **Environment Variables** for the app: everything in `.env.example`, with test keys first.
4. Redeploy, then check `https://spherewellness.in/api/health` returns `{"ok":true,"bookings":"open"}`
   and the startup log line `backend_ready` lists no `blocking` items.

If Hostinger cannot run the app this way, the backend runs unchanged on any Node host; point the
page's `fetch` and Razorpay's webhook at that host and add it to the page CSP's `connect-src`.

## Razorpay setup

In **test mode** first, then again in live mode (keys and webhooks are separate per mode):

- **API Keys:** generate a key; put the id and secret in the environment variables.
- **Webhooks → Add:** URL `https://spherewellness.in/api/webhooks/razorpay`, a long random secret
  (the same value as `RAZORPAY_WEBHOOK_SECRET`), events **`payment_link.paid`**,
  **`payment_link.expired`**, **`payment_link.cancelled`**.

## Meta setup

- Accept Sumi's Conversions API invitation from inside `business.facebook.com` (not the email link).
- Events Manager → dataset `1150068800700841` → Settings → Conversions API → generate an access token
  → `META_ACCESS_TOKEN`. The token Naveen pasted in chat should be revoked.
- Test Events → copy the test code → `META_TEST_EVENT_CODE`.

## Testing on the live server (test keys, nothing visible to guests)

1. In `data/event.json`, `booking_api` is `"preview"`: the dialog exists but only runs at
   `/carnival/?booking=preview`. Everyone else keeps the shared link.
2. Open `https://spherewellness.in/carnival/?booking=preview`, choose 1 ticket, tick the consent box,
   continue, and pay with Razorpay's test UPI ID or test card (Razorpay docs → test card details).
3. Repeat for 2 and 3 tickets, and once without consent (that one must not reach Meta).
4. Check each in Meta **Events Manager → Test Events**: `Purchase`, value 2,899 / 5,798 / 8,697 INR,
   matching order ID, and (with consent) email, phone, fbp/fbc shown as received.
5. In Razorpay → Webhooks, resend one `payment_link.paid` delivery: the log shows
   `duplicate` or `already_paid`, and Test Events still shows one Purchase for that booking.
6. `npm run bookings -- stats` (with the environment set) shows bookings, tickets paid, and Meta states.

## Going live

1. Client approves the dialog wording in `data/event.json` → `booking_dialog`; set `"draft": false`.
2. Client confirms the privacy points below are in place.
3. Live Razorpay keys and live webhook; **remove `META_TEST_EVENT_CODE`**.
4. `booking_api: "on"`, `python3 scripts/build_site.py`, checks, merge, deploy.
5. One real small purchase, check Events Manager (Overview, not Test Events), refund it.

## Operations

- **Logs:** one JSON line per event (`booking_created`, `booking_paid`, `meta_purchase_sent`,
  `meta_purchase_failed`, `payment_mismatch`, `webhook_bad_signature`). No secrets or raw personal data.
- **A webhook never arrived:** `npm run bookings -- reconcile` asks Razorpay about unpaid links.
- **Meta token was wrong, now fixed:** `npm run bookings -- retry`.
- **`review` bookings:** money and booking disagree; look the payment up in Razorpay. Never sent to Meta.
- **Optional caps:** `max_tickets_per_booking` (default 10) and `website_ticket_limit` (website
  bookings only; WhatsApp and QR sales are not counted, so it cannot stop overselling across channels).
- **Tests:** `npm test` (18 tests, file store). Against MySQL:
  `TEST_DB_HOST=… TEST_DB_USER=… TEST_DB_NAME=… npm test`. Both pass on Node 18 and 24 and MySQL 9.

## Privacy and compliance

- **Consent:** identifiers for Meta are used only after the guest ticks an unticked, optional box
  (affirmative, specific, can be refused without losing the booking), in line with India's DPDP Act 2023
  and DPDP Rules 2025 and with Naveen's "where consented to".
- **Minimisation:** we never store email or phone, only their SHA-256 hashes, and only with consent.
  `fbp`, `fbc`, IP and the hashes are deleted as soon as Meta has the event (or after 7 days).
- **Payments:** hosted Razorpay checkout; no card or UPI data on our server.
- **Still needed from the client (not code):**
  - A privacy notice on the site. Meta's Business Tools Terms require one that explains the pixel,
    cookies and sharing with Meta. The site has none, and the Terms page does not cover it.
  - A decision on the page-view pixel: it runs for every visitor today, with no consent banner.
  - Approved wording for the booking dialog, including the consent sentence.

## Known limits

- Sales via the WhatsApp link or QR code are not reported, by design.
- Ads that open WhatsApp cannot be measured this way.
- Meta optimises best with about 50 purchases a week; one event with limited tickets may not reach that.
