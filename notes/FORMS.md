# Enquiries and the inbox list

How someone on the website reaches `thespherewomen@gmail.com`, what you have to do once to
switch it on, and how comparable clubs handle the reply.

## What is on the site now

| Where | What it asks | Subject line that lands in Gmail |
|---|---|---|
| **Request an invitation** dialog — header, hero, A Private Circle section, footer, and every journal page | Name, email, WhatsApp (optional), "What brings you to The Sphere?" (optional), consent tick | `The Sphere — <name> would like to join` |
| **Stay close** section above the footer (`/#inbox`) | Email only | `The Sphere — <email> joined the inbox` |

Both post to the same place. The form is submitted in the background, so the visitor stays on the
page and sees a confirmation in place of the form. If JavaScript is off, the browser posts normally
and lands on `/thank-you/`.

## How it reaches Gmail

The forms post to **FormSubmit** (`formsubmit.co`), a free form-to-email relay. There is no server
and no database — FormSubmit takes the submission and emails it to the club. It is configured to:

- email the club a formatted table of the answers,
- set **Reply-To** to the sender's address, so replying in Gmail goes straight to her,
- send her an **instant auto-reply** in The Sphere's voice (see `AUTORESPONSE` in
  `scripts/build_site.py`),
- ignore bots via a hidden honeypot field.

The address it delivers to lives in one place: `form_endpoint` in `data/site.json`.

## One-time setup — the forms do not deliver until you do this

1. Open the live site and send yourself a test enquiry through **Request an invitation**.
2. FormSubmit emails `thespherewomen@gmail.com` asking you to confirm the address. **Open that
   email and click the activation link.** Nothing is delivered before this.
3. That confirmation page gives you a **random alias** that stands in for the address, something
   like `https://formsubmit.co/xyz123abc`. Copy the alias part.
4. Put it in `data/site.json`:

   ```json
   "form_endpoint": "xyz123abc"
   ```

5. Rebuild and redeploy:

   ```bash
   python3 scripts/build_site.py && python3 scripts/check_content.py
   ```

6. Send one more test enquiry and confirm it arrives.

**Step 4 matters.** Until the alias replaces it, `thespherewomen@gmail.com` is visible in the page
source, where address-harvesting bots find it. The alias delivers to the same inbox without showing
the address.

## What to expect in the inbox

One email per enquiry, from FormSubmit, with the answers as a table. Hit Reply and it goes to her.
Gmail may file the first few under **Promotions** or **Spam** — mark one as "Not spam", then make a
filter: from `formsubmit.co` → never send to spam, apply a label such as *Sphere enquiries*, mark
important. Missing an enquiry costs far more than the filter takes to set up.

## Limits worth knowing before the list grows

- **FormSubmit does not keep a list.** It forwards and forgets. Every "Stay close" signup arrives as
  an email and nowhere else, so keep a running sheet of subscribers, or the list only exists inside
  Gmail search.
- **Gmail is not a newsletter tool.** Sending one message to a few hundred addresses from a personal
  Gmail account will get it filtered, and Gmail caps daily recipients. Once the list is past roughly
  50 people, move it to a proper sender — MailerLite, Brevo and Mailchimp all have free tiers — and
  point the "Stay close" form at that service instead. Only the `action` URL has to change.
- **Consent is recorded** on the enquiry form (an unticked box the sender has to tick), which is
  what India's DPDP Act asks for: consent that is free, specific, informed and unambiguous, never
  pre-ticked. Keep those emails; they are the record. The inbox form states the purpose in plain
  words above the button, which is the affirmative action.

## How clubs like this actually handle the reply

Drawn from the sources below, adapted to a small club in Coimbatore.

**Speed is the whole game.** Contacting a prospect within five minutes makes a connection far more
likely than waiting thirty; for studios, a WhatsApp reply within the first minute converts several
times better than an email sent at the same moment. The auto-reply buys you the first hour. It does
not replace a real reply.

**A workable rhythm:**

1. **Instantly** — the auto-reply lands. Already configured.
2. **Within a few hours, same day** — a personal reply from a person, by name, answering what she
   actually asked. If she left a WhatsApp number, WhatsApp is the better channel in India; say who
   you are and that she wrote in, so the number is not a cold message.
3. **Within two days** — what the club is, what is coming up, and one concrete next step: a date, a
   gathering, an invitation to meet. An enquiry with no next step goes cold.
4. **After she joins** — a short welcome sequence rather than one long email. Three notes in the
   first week, then weekly for a few weeks, is the pattern clubs settle on: welcome and one thing
   she can do straight away, then what membership includes, then an invitation to the next
   gathering. Around 60–70% of members who do not engage in their first 90 days never renew, so the
   first month is the one that counts.
5. **Ongoing, for the inbox list** — rarely, and only when there is something worth pausing for.
   That is what the form promises; keeping the promise is what keeps people subscribed.

**On the form itself:** every field removed lifts completion, which is why "Stay close" asks for an
address and nothing else, and why name and WhatsApp are the only things beyond email on the
enquiry form. THE WELL, a comparable club, asks for an email address alone.

## Sources

- [FormSubmit documentation](https://formsubmit.co/documentation) — endpoints, activation, the alias that hides the address, and the `_autoresponse`, `_subject`, `_template` and honeypot fields used here.
- [Free form backend services compared](https://merginit.com/blog/24062026-free-form-backend-services-comparison) and [Best form backend services 2026](https://forminit.com/blog/best-form-backend-services-2026/) — why a relay, and how FormSubmit compares with Formspree and Web3Forms.
- [Lead response time: the 5-minute rule](https://blog.kraya-ai.com/lead-response-time) and [WhatsApp for spas and studios](https://m.aisensy.com/blog/whatsapp-for-spa-and-salons/) — response speed and the Indian WhatsApp follow-up pattern.
- [New member onboarding 2026](https://joinit.com/blog/the-best-new-member-onboarding-tips-for-your-association) and [Member engagement email campaigns](https://smarthealthclubs.com/blog/12-email-campaigns-that-will-help-you-boost-member-engagement-retention-at-your-health-club/) — the welcome sequence, its cadence, and the first-90-days retention figure.
- [Signup form best practices](https://www.omnisend.com/blog/best-signup-forms-conversions/) and [Double opt-in best practices](https://learn.customer.io/deliverability/double-opt-in-best-practices) — fewer fields, clear value, confirmation.
- [Consent under the DPDP Act](https://ksandk.com/data-protection-and-data-privacy/consent-under-dpdp-act-2023-compliance-strategies/) — explicit, unambiguous, never pre-ticked.
- [THE WELL](https://www.the-well.com/) — a comparable club's email capture, an address and nothing more.
