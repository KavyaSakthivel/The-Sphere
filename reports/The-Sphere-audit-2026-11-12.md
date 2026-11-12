# The Sphere: Product, Brand, UX and Editorial Audit

Audited: https://spherewellness.in/ (live) and the project folder, 12 November 2026.
No code was edited, no form was submitted, no payment link was opened, no dependency was installed.

Evidence labels used throughout: **[Observed]** seen in the browser · **[Source]** confirmed in project files · **[Inferred]** reasoned from the above · **[Confirm]** needs a client answer.

Copy rule: every line of proposed copy in section E is a **proposal for client approval**. The client's supplied wording stays the source of truth; nothing here should be published until she has approved it.

---

## A. Executive assessment

Today The Sphere reads as a warm, well-made women's wellness community in Coimbatore. The photography is genuine (real sessions, real rooms), the type pairing (Fraunces and DM Sans) is calm and editorial, and the copy is short and kind. The Carnival page is the most concrete page on the site: date, venue, price, schedule, FAQ, terms.

The gap against the intended private-club positioning is not visual. It is **process and substance**:

1. The site speaks selectively ("the right ones", "a personal conversation", "A private circle") but every "Join The Sphere" button, on every page, opens a **₹10,000 Razorpay payment link**. There is no conversation before payment, and no membership terms. The one-question enquiry form that matches the tone is on the Membership page only, below the payment button, with nothing leading to it.
2. The home page says what The Sphere *feels like* but not what a member *does*: no named programme, no facilitators, no founder, no venue context, no cohort date.
3. A first-day **full-screen Carnival pop-up** covers about 80% of a phone screen 1.8 seconds after arrival, with a call to action that fails contrast.

**Three most valuable improvements:** (1) make the first step a hello, not a payment, once the client confirms the real process (SPH-01, SPH-04); (2) add membership terms and a privacy note before taking money or personal data (SPH-02, SPH-12); (3) replace the pop-up with a quiet announcement and give the home page one concrete "what a month looks like" section (SPH-05, SPH-08).

---

## B. Inspection coverage

**Inspected in the browser (live site):**
- Home at 1440×900 (pop-up timing, dismissal by Escape, hero, first three scroll positions) and at 390×844 (pop-up, hero, mobile menu, tap-target and contrast measurement).
- Membership at 390×844 (all sections scrolled; form field inventory read from the page).
- Carnival at 360×800 (header, hero, sticky booking bar, "at a glance" block, overflow and fixed-element check).
- Experiences at 360×800 (hero, overflow, anchors).

**Inspected in source only** (`dist/*.html`, `dist/site.js`, `dist/motion.js`, `dist/finish.css`, `dist/premium.css`, `dist/_headers`, `dist/sitemap.xml`, `data/site.json`, `data/founder.json`): Our story, Terms, Thank-you, the three redirect stubs (`/circle/`, `/experience/`, `/journal/`), all five journal entries' links, form code and success/error copy.

**Comparison note:** the live home page is byte-identical in size to `dist/index.html` (33,270 bytes). The live membership page differs by a few bytes from the working copy, which has uncommitted changes. Browser findings describe the live site; source findings describe the folder.

**Not inspected or unverified:**
- 1280×800, tablet, and mobile landscape. Not run.
- Keyboard-only tab order, focus rings in use, and back-button behaviour. Not exercised. Focus styles exist in CSS (`:focus-visible` rules in all four stylesheets) but I did not see them rendered.
- The stepped enquiry form's visual states (I read its code and field list; screenshots of the form did not capture).
- Success and error states of both forms: **source only**, not triggered.
- Screen-reader output, Lighthouse, Core Web Vitals, real load times. No numbers are claimed.
- Contrast over the hero video (background is not computable from the DOM). Text contrast on solid backgrounds was measured.
- Razorpay pages, Instagram profile, the five journal article pages' full text, payment and booking flows. Deliberately not opened.
- Browsing the live site loads the site's own Meta Pixel and Tag Manager, which fire page-views. This cannot be avoided in a live inspection.

**Page and component inventory**

| Route | Source | Notes |
|---|---|---|
| `/` Home | `dist/index.html` | Hero film, philosophy, four pillars, "women of The Sphere", private circle, journal list, newsletter, footer |
| `/philosophy/` ("Our story") | `dist/philosophy/index.html` | Founder portrait and bio |
| `/experiences/` | `dist/experiences/index.html` | Five experiences |
| `/membership/` | `dist/membership/index.html` | ₹10,000 offer, how joining works, founder note, enquiry form |
| `/carnival/` | `dist/carnival/index.html` | 20 Dec 2026 event, booking modal (Razorpay) |
| `/terms/` | `dist/terms/index.html` | Carnival terms, linked site-wide |
| `/thank-you/` | `dist/thank-you/index.html` | `noindex`; only reachable by a non-AJAX form post |
| `/journal/<5 entries>/` | `dist/journal/*/index.html` | Open as a dialog on home, also real pages |
| `/circle/`, `/experience/`, `/journal/` | stubs | Meta-refresh redirects, `noindex` |
| `/palette-study/**` | `dist/palette-study/` | Internal colour experiments, **live and reachable**, `noindex,nofollow` |
| `/privacy/` | none | **Returns 404** [Observed] |

Components: Carnival pop-up (`dialog[data-carnival-popup]`), mobile menu (`#mobile-nav`), enquiry dialog (`#invitation-dialog`), journal dialog (`#article-dialog`), enquiry form (membership page), newsletter form (every page), booking modal (Carnival). Social: Instagram `@thespherewomen` only.

---

## C. Prioritised findings

Effort assumes one developer familiar with this static build (hand-edited templates in `templates/` and `scripts/`, output in `dist/`). Small ≈ under half a day, Medium ≈ one to two days, Large ≈ needs new assets or backend work. Impact ratings are qualitative.

| ID | Priority | Page / component | Observed issue | Proposed fix | Brand impact | Usability impact | Effort | Evidence confidence | Dependency |
|---|---|---|---|---|---|---|---|---|---|
| SPH-01 | **P0** | Header "Join The Sphere" (all pages), home "A private circle", Membership hero/offer/footer | Every "Join The Sphere" link has `href="https://rzp.io/rzp/8SMwRyN"` (`data/site.json: membership_payment_url`), opening a payment page in a new tab. Yet the page says the first step is "A note from you. A personal conversation." and "It's a space designed to have the right ones." Payment comes before any conversation. | Decide the real sequence. If conversation first: CTA opens the enquiry (modal or `/membership/#hello`); payment link is shared after the conversation. If open enrolment: drop the selective language. | High | High | Small–Medium | Source + Observed (href read, not opened) | **Client decision** on process |
| SPH-02 | **P0** | Footer "Terms & Conditions"; `/terms/` | Only Carnival terms exist, titled "Terms & Conditions \| The Sphere Wellness Carnival", but linked site-wide as if general. No membership terms (refund, cancellation, what happens if a session is missed, validity). No privacy policy page (`/privacy/` is 404). A ₹10,000 payment link and two data forms exist without either. | Add a short membership terms page and a plain privacy notice; label the existing page "Carnival terms"; link each next to the relevant CTA. | High | Medium | Medium | Observed + Source | Client and her adviser must supply refund/cancellation and data-handling facts |
| SPH-03 | **P1** | Enquiry dialog, success message, thank-you page, auto-reply, newsletter | Promises that need confirming: "reply within two days"; "We read every note ourselves"; "we never share or sell them"; "Your details come straight to The Sphere's own inbox" (they pass through the FormSubmit relay); "Membership is intentionally limited"; "Sent rarely. Never shared." | Keep only what the client can honour. Rewrite the rest (section E). | High | Medium | Small | Source | **Client confirmation** of each |
| SPH-04 | **P1** | Membership enquiry form; home `#invitation-dialog` | The enquiry dialog exists in the HTML of every page but **nothing opens it**: 0 elements with `data-invitation` on home and membership [Observed via JS]. The working enquiry form sits on the fifth screen of `/membership/` on a phone, below the payment button, and no link scrolls to it. A visitor who wants to say hello first has no visible path. The same dead dialog markup is repeated on most other pages. | Give the hello a visible home: secondary link under the primary CTA, "Or write to us first", opening the dialog or scrolling to the form. Remove the unreachable duplicates. | High | High | Small | Observed + Source | Pairs with SPH-01 |
| SPH-05 | **P1** | Home Carnival pop-up (`dialog[data-carnival-popup]`, `dist/motion.js`) | Opens 1.8 s after arrival on every new session [Source + Observed]; on 390×844 it is 358×671 px, about 80% of the screen, over the brand introduction [Observed]. Dismissal works (close ×, "Continue to The Sphere", backdrop, Escape; once per session via `sessionStorage`) [Observed/Source]. **Contrast fails:** "Discover the carnival" 3.13:1 at 13 px; "An invitation to come together" 4.15:1 at 15 px [Observed, computed]. Event details inside are 12 px. | Replace with a slim announcement band under the header (section F), or if the client keeps a modal, delay it until after first scroll, fix contrast, enlarge text to ≥14 px. Keep the existing auto-retirement on `data-promotion-until`. | High | High | Small | Observed + Source | None |
| SPH-06 | **P1** | Carnival page, mobile | At 360 px the first screen carries three payment-style calls: header "Join The Sphere" (membership ₹10,000), hero "Reserve your spot", and a fixed bottom "Reserve Your Spot ₹2,899" bar (`event-bar`, 73 px tall) [Observed]. Two different purchases compete, and the header one is the wrong product for this page. | On `/carnival/`, hide or demote the header membership CTA; keep one ticket CTA in the hero and the sticky bar (usable, and the one place a sticky bar is justified). | Medium | High | Small | Observed | None |
| SPH-07 | **P1** | Positioning overall | Copy is membership-led (Model A) but the evidence of an operating offer sits with the Carnival (date, venue, price, schedule, terms). Membership has a price and "once a month, usually in the first week" but no start date, no venue, no sessions held, no programme. | Treat the Carnival as the threshold into the membership (Model A with event as introduction) once the client confirms the cohort facts (section H). | High | Medium | Medium | Inferred | Client facts |
| SPH-08 | **P1** | Home, Experiences, Membership | The site never says what a member does in a month. Home pillars are abstract ("Practices that create stillness in a world that rarely stops"). Home lists **four** pillars (Move, Pause, Connect, Discover); Experiences lists **five** with different names (Move & Reconnect, Pause & Restore, Talk & Reflect, Explore & Experience, Meet & Connect), and home links "Connect" to `#practice-5`, "Discover" to `#practice-4`. No facilitators, duration, group size or sample month appear. | Pick one set of names. Add one concrete "A month at The Sphere" block using only confirmed facts (the Experiences page already names yoga, Kalaripayattu, sound healing, breathwork). | High | Medium | Medium | Observed + Source | Client supplies session detail |
| SPH-09 | **P1** | Carnival "Join The Sphere / One Evening. Many Experiences. One Community." | A paragraph inviting "influencers, collaborators, wellness brands, marketing partners and sponsors" sits on the consumer page under the same heading as the membership CTA. It reads as a sponsorship pitch and blurs who the page is for. | Move to a separate "Partner with us" line or page; retitle the section. | Medium | Low | Small | Source | Client confirms sponsor outreach channel |
| SPH-10 | **P1** | Site-wide tracking | Meta Pixel (`fbq('init'…)`, `PageView`) and Google Tag Manager load on every page with no notice or choice [Source]. Carnival booking asks consent before sharing booking data with Meta, but page-view tracking has none. A member-privacy promise sits awkwardly beside this. | Add a short, quiet notice and choice (or defer the pixel until accepted); describe tracking in the privacy notice. | High | Low | Medium | Source | Client and adviser decide on consent approach |
| SPH-11 | **P2** | Enquiry consent checkbox | The checkbox "Yes, The Sphere may email or message me about membership and gatherings" is **required** to send an enquiry. Asking permission to reply and permission to market are bundled. | Make the enquiry itself the permission to reply; offer a separate optional box for future notes. | Medium | Medium | Small | Source | None |
| SPH-12 | **P2** | Brand names | "The Sphere", "Sphere Women" (founder role: "Founder, Sphere Women"), "Sphere", "The Sphere Wellness Foundation" (footer, Terms) all appear. Tagline is "modern **woman**" in headings but "modern **women**" in the wordmark alt text on every page and "Calmness crafted for The Modern Women" on the Carnival page. | Settle one trading name and one legal-entity line; fix the plural. | Medium | Low | Small | Source | Client confirms names |
| SPH-13 | **P2** | Contact and footer | Contact is a Gmail address and a mobile number only. On Carnival at 360 px footer links are 20 px tall [Observed]. | Domain email as a setup task (not yet wired); raise footer link height to ≥44 px. | Medium | Medium | Small | Observed + Source | Client creates domain mailbox |
| SPH-14 | **P2** | Newsletter ("Wellness in your inbox") | Appears on every page, including directly under the membership enquiry form, so two asks compete. Footer calls it "Notes by email"; heading says "Stay close." No privacy link, no sign of how often. | Keep it low in the footer on non-home pages; align the name; link privacy. | Low | Low | Small | Source | Real content plan |
| SPH-15 | **P2** | Terms vs programme | Terms refer to "ice plunge, salt bath"; the Carnival schedule does not list them. No refund position for the ₹2,899 ticket. | Align or remove; state refund position. | Medium | Low | Small | Source | Client confirms |
| SPH-16 | **P2** | Metadata | Home and Our story have no `og:image`; home uses `twitter:card=summary`. Links shared on WhatsApp or Instagram will look plain. Carnival and Membership are fine. | Add a calm cover image and `summary_large_image`. | Medium | Low | Small | Source | Pick image |
| SPH-17 | **P2** | Small type | Eyebrows, popup details and footer meta are 12 px (13 px on pop-up). Measured contrast on solid backgrounds is otherwise ≥5.6:1. | Raise to 14 px minimum for anything that carries information. | Low | Medium | Small | Observed (computed) | None |
| SPH-18 | **P2** | Home "women of The Sphere" and Carnival "Women gathering" | Lists roles ("Founders. Leaders. Entrepreneurs. Creatives. Mothers. Professionals.") then says "What brings them together isn't what they do". The role list still defines the audience; it is generic. | Tighten (section E). | Low | None | Small | Source | None |
| SPH-19 | **P3** | Navigation | Desktop order: Our story, Experiences, Journal, Membership, Carnival. Mobile menu: Our story, Experiences, Membership, Journal, Carnival. "Our story" links to `/philosophy/`. | One order; Membership before Journal; rename slug later if wanted. | Low | Low | Small | Source | None |
| SPH-20 | **P3** | Housekeeping | `/palette-study/**` is live (noindex). `dist/assets/` is 42 MB and ships font files not used by the live type pairing (Nunito Sans, Manrope, Dancing Script, Sacramento, Cormorant). Hero films are 2.5–4.3 MB each (preload none, loaded after page load). `premium.css` maps `--forest`, `--forest-deep` and `--wine` all to `#834c4d`. | Remove internal study pages and unused fonts from the published folder; tidy token names. | None | Low | Small | Source | None |

**Not defects (checked, working):** no horizontal overflow at 390 or 360 px on any page tested; mobile menu items 58 px tall and the toggle 44×44; pop-up close 44×44; Escape closes the pop-up [Observed]; the hero video has a Pause control, respects reduced motion and Save-Data [Source]; `font-display: swap` throughout; form fields use correct types and autocomplete; the form disables its button while sending and uses a honeypot [Source]; skip link present; heading hierarchy on Membership is clean (one H1) [Observed].

---

## D. Page-by-page review

### Home `/`
**Keep:** hero image and film (tall cut on phones), "A little more room for you.", sound-session photograph, calm section rhythm, Pause button on the film.
**Improve:**
- Fix pop-up (SPH-05).
- "Curated. Not crowded." and "The Sphere is intentionally intimate" repeat the same idea; keep one.
- Add a concrete block: what a month contains (SPH-08).
- Add the founder's name and one line near "The women of The Sphere" (details already on Our story).
- Make "A private circle" show what happens first (hello), not a payment link (SPH-01).
**Remove or consolidate:** the role list in "Different lives. Shared values." (SPH-18); the duplicate "Join The Sphere" in footer plus header plus section.
**Exact changes:** header CTA becomes "Say hello" (pending client decision); announcement band replaces modal; four pillars aligned to Experiences naming.

### Our story `/philosophy/`
**Keep:** founder portrait, bio with named credentials, "Is wellness a luxury or a necessity? We believe it is a necessity.", "Come as you are."
**Improve:** the bio is third person and formal; add one line in the founder's own voice. "Founder, Sphere Women" versus "The Sphere" (SPH-12). Add `og:image`.
**Consolidate:** the "A space to simply be" opening and the Membership note ("We wanted to create a space to simply be") repeat; keep the note on Our story and link from Membership.

### Experiences `/experiences/`
**Keep:** five named experiences, the closing paragraph ("sit across from a woman you've never met…").
**Improve:** each description is one line; add what happens and for how long, only from confirmed facts. Hero image appeared heavily blurred at 360 px [Observed]; confirm whether it was still loading or the asset is too soft, and replace if the latter.
**Fix:** align the five names with the home page (SPH-08).

### Membership `/membership/`
**Keep:** ₹10,000, "inclusive of GST", "One session each month", "Venue and gathering details are shared with members privately", the singing-bowls photograph, the founder's note. The price card is clear and not pushy.
**Improve:** reorder so "How joining works" matches the real process (SPH-01). Put the enquiry form directly after the price card, not three sections later. "Membership is intentionally limited" needs a fact behind it, or goes (SPH-03). Add terms link beside the price (SPH-02).
**Remove or consolidate:** repeated "Venue and gathering details are shared with members privately" (appears twice) and the third step, which restates it.

### Carnival `/carnival/`
**Keep:** at-a-glance block, schedule, "alcohol-free" clarity, price shown early, FAQ, mobile sticky bar.
**Improve:** header CTA conflict (SPH-06); sponsor paragraph (SPH-09); "Open to Women Only" and "WHO" capitalisation inconsistent with "When" and "Where"; "Calmness crafted for The Modern Women" (SPH-12); end-of-event state: the site already removes the Carnival nav link on 1 Jan 2027 (`data-event-until`), but the Carnival page itself, the home pop-up promotion window and the sitemap entry need a plan (question 8).
**Add:** one line under the schedule: "The Sphere also meets monthly as a private circle" with a quiet link to Membership.

### Terms `/terms/`
Rename "Carnival terms". Add membership terms separately (SPH-02). Align health examples with the schedule (SPH-15). The final sentence ("You agree to share information entered on this page with THE SPHERE WELLNESS FOUNDATION… and Razorpay") reads like a payment-page boilerplate on a page with no inputs; remove or move.

### Thank-you `/thank-you/`
Only reached by a non-AJAX submission, which the site's JavaScript avoids. It is effectively orphaned and repeats the two-day promise. Keep as a fallback if JS fails; align wording with SPH-03.

### Journal entries
Not read in full (links and titles only). Titles are strong and quietly on-brand. Journal opens as a dialog from home while pages also exist; check that the page URLs are the ones shared. [Unverified]

---

## E. Copy rewrite pack

### Hero directions (proposals; placeholders in [brackets])

**Direction 1: clear and quietly confident**
- Headline: *A women's wellness club in Coimbatore.*
- Supporting text: *One gathering a month, for six months, among women who want a little more room. Movement, stillness and conversation, hosted by [founder name].*
- Primary CTA: *Say hello*
- Secondary link: *See how membership works*
- Why it fits: names the thing, the place and the rhythm in the first screen; confident without adjectives. Depends on confirming "hosted by" and the six-month rhythm (the Membership page already states six months and one session each month).

**Direction 2: more evocative, with a concrete explanation**
- Headline: *A little more room for you.* (kept from the current site)
- Supporting text: *The Sphere is a women's wellness club in Coimbatore. Each month, members gather for one session of [movement, sound or conversation], in a private setting. Membership is ₹10,000 for six months.*
- Primary CTA: *Say hello*
- Secondary link: *Meet the founder*
- Why it fits: keeps the existing line the brand already owns and gives it a factual floor. Price on the home page is optional; the client may prefer it only on Membership.

### Key copy fixes

| Page / section | Current copy | Issue | Recommended copy | Facts to confirm |
|---|---|---|---|---|
| Home, "A space that asks nothing of you" | "A private space for women who do a lot, carry a lot, and deserve a space that asks nothing of them." | "space" three times; "deserve" is mildly salesy | "A private place for women who carry a lot, and ask nothing of them in return." | Client approves wording |
| Home, "Curated. Not crowded." | "The Sphere is intentionally intimate. We believe meaningful experiences happen when there is room to connect… Every experience is thoughtfully curated around four elements:" | "intentionally", "thoughtfully curated", "meaningful" stack | "Small by design. Every session is built around four things:" | Group size, if the client will state it |
| Home, pillar Pause | "Practices that create stillness in a world that rarely stops." | Abstract | "Sound healing, meditation and breathwork." (already named on Experiences) | None; reuses existing copy |
| Home, "The women of The Sphere" | "Different lives. Shared values. Founders. Leaders. Entrepreneurs. Creatives. Mothers. Professionals…Curious. Intentional. Open. Evolving." | Role list; four adjectives | "Different lives, shared values. What brings them together isn't what they do. It's how they choose to live." | None; trims existing copy |
| Membership, "A private circle" | "Membership is intentionally limited to preserve the intimacy… It's a space designed to have the right ones." | Unverified scarcity; "right ones" implies judgement of worth | Remove, or: "We keep each circle small so everyone has room to be heard." | Is there a cap? What number? |
| Membership, "The first step" | "A note from you. A personal conversation." | Contradicts the payment link | Keep **if** conversation really comes first; otherwise remove | The real order |
| Wordmark alt text (all pages) | "The Sphere — Crafted calm for the modern women" | Plural | "The Sphere — Crafted calm for the modern woman" | None |
| Carnival, About | "Calmness crafted for The Modern Women." | Plural, capitals | "Crafted calm for the modern woman." | None |
| Carnival, "Join The Sphere" | "One Evening. Many Experiences. One Community… We invite influencers, collaborators, wellness brands, marketing partners and sponsors…" | Sponsorship pitch on consumer page | "Partner with us" with an email line | Sponsor contact |
| Terms §4 | "ice plunge, salt bath, breathwork, sound healing and the fire ceremony" | Not in the schedule | List only scheduled activities | Programme |

### Membership explanation (proposal)
*Membership is ₹10,000 for six months, inclusive of GST. For six months you take part in one gathering a month, usually in the first week. Venue and gathering details are shared with members privately.* (This is the client's existing wording, lightly reordered; the first-step line depends on SPH-01.)

### Enquiry dialog (proposal; response time and process lines are conditional)

| Element | Proposed copy |
|---|---|
| Primary CTA | Say hello |
| Dialog title | It begins with a hello. |
| Intro | Tell us a little about yourself and what brings you to The Sphere. *[A member of the team will write back personally.]* |
| Labels | Your name · Email · WhatsApp (optional) · What brings you to The Sphere? (optional) |
| Placeholders | First and last name · you@example.com · +91 · A line or two is plenty. |
| Consent text | *We'll use your details only to reply to you.* Link: Privacy. Optional separate box: *I'd also like occasional notes about gatherings.* |
| Submit | Send |
| Loading | Sending… |
| Success | Thank you. Your note has reached us. *[We'll reply within [N] days.]* |
| Error | That didn't send. Please try again, or message us on Instagram @thespherewomen. |

Minimum fields and why: **name** (to reply), **email** (to reply), **WhatsApp** (optional; many members will prefer it), **a line** (optional; starts a conversation). Do not add income, family or status questions. Treat this as an **enquiry**: the lightest accurate flow unless the client confirms there is a real application step. Bracketed lines depend on confirmation.

### Newsletter (proposal)
Name: keep **Notes by email** (matches the footer). Heading: *Notes by email.* Line: *Early word on gatherings, and the occasional note from the circle. [Roughly once a month.]* Consent: *Your email is used only for these notes. Privacy.* Success: *Thank you. You're on the list.* Frequency line depends on the client's content plan.

### Footer (proposal)
*The Sphere. A women's wellness club in Coimbatore.* · Contact · Instagram · Privacy · Membership terms · Carnival terms · © 2026 *[legal entity]*.

### Four pillars (proposal, using only wording already on the site)
- **Move.** Yoga, functional movement and traditional practices such as Kalaripayattu.
- **Pause.** Sound healing, meditation and breathwork.
- **Talk.** Honest conversations on womanhood, ambition, relationships and identity.
- **Explore.** Something new each time.
Connect is the thread through all four, not a fifth item. (Align Experiences to match.)

**Publishable now (no new facts):** wordmark alt fix, "Carnival terms" title, tagline plural, trimmed home lines. **Needs client confirmation:** everything in brackets, any response time, any cap on members, any "hosted by" line.

---

## F. UI and CSS recommendations (not applied)

Existing tokens in `dist/premium.css` (lines ~308–322): `--paper #fff8ec`, `--sage #9ab7a8`, `--terracotta #834c4d`, `--ink #30362e`, `--muted #45483e`. Fonts: Fraunces (headings) and DM Sans (body). Keep them.

**Compact specification** (adapt after measuring the current values in `finish.css`):

| Item | Proposed |
|---|---|
| Content width | 1200 px max |
| Reading width | 62 ch (about 600–640 px) |
| Gutters | 24 px desktop, 16–20 px mobile (add `env(safe-area-inset-*)`) |
| Body / small | 17–18 px / 14 px minimum |
| Section spacing | 96–120 px desktop, 64–80 px mobile |
| Buttons | 48 px high, 44 px minimum touch target |
| Dialog | 560 px wide desktop; full-width minus 16 px on phones, `max-height: 90dvh` |
| Image ratios | 3:2 for scene photos, 4:5 for portraits |
| Motion | 200–250 ms, opacity and transform only |

**Pop-up contrast fix (if modal is kept)**
```css
.carnival-popup-cta { background: #fff8ec; color: #834c4d; } /* 6.4:1 */
.carnival-popup .eyebrow { color: #fff8ec; }                 /* was #dfc6b6, 4.15:1 */
```

**Announcement band replacing the modal (illustrative)**
```html
<aside class="announce" aria-label="Upcoming event">
  Wellness Carnival · 20 December 2026 · Jenney's Club, Coimbatore
  <a href="/carnival/">Details</a>
  <button type="button" aria-label="Dismiss">×</button>
</aside>
```
```css
.announce { padding: 10px 16px; font-size: 14px; text-align: center; }
@media (prefers-reduced-motion: reduce) { .announce { transition: none; } }
```
Reuse the existing `data-event-until` removal logic in `dist/site.js` so it retires itself after the event. Source of truth lives in `templates/` and `scripts/` (`build_site.py`, `finish_site.py`); `dist/` is generated, so changes should be made there.

**Targets:** footer links `min-height: 44px; display: inline-flex; align-items: center;`

---

## G. Delivery sequence

1. **Immediate corrections (no client facts needed):** SPH-05 contrast and pop-up timing, SPH-06 carnival header CTA, SPH-12 plural fix and alt text, SPH-13 footer targets, SPH-16 social images, SPH-19 nav order, SPH-20 housekeeping, SPH-04 remove unreachable duplicate dialogs.
2. **Content and design improvements:** SPH-08 pillar alignment and "a month at The Sphere" block, SPH-09 sponsor line, SPH-11 consent split, SPH-14 newsletter placement, SPH-15 terms alignment, SPH-17 type sizes, SPH-18 copy trims.
3. **Client decisions or new assets:** SPH-01 process, SPH-02 terms and privacy, SPH-03 promises, SPH-07 positioning model, SPH-10 tracking consent, domain email (SPH-13), any founder or home-page photography.

---

## H. Client questions

1. **What happens after someone wants to join: a conversation first, or payment first?** Unlocks SPH-01, SPH-04 and the whole membership page order.
2. **Is membership limited or reviewed?** If yes, how many places, and who decides? Unlocks "intentionally limited" and any selective language (SPH-03).
3. **How long does a reply take, and who writes it?** Unlocks the "two days" promise and the success message.
4. **What is the refund and cancellation position for membership and Carnival tickets?** Unlocks SPH-02 and SPH-15.
5. **When does the next membership cohort begin, and where do sessions happen (a named venue, or varied)?** Unlocks SPH-07 and SPH-08.
6. **Which name does the brand trade under, and what is the legal entity line?** Unlocks SPH-12.
7. **Which facilitators and sessions can be named publicly, with their consent?** Unlocks "a month at The Sphere" and the founder line.
8. **What happens to the Carnival page after 20 December: archive, retire, or become a recurring event?** Unlocks the post-event homepage and the nav.

Also useful, not blocking: whether a domain email will be set up.

---

## I. Proposed implementation scope

**First batch (all independent of client answers): SPH-05, SPH-06, SPH-12, SPH-13, SPH-16, SPH-19, SPH-20, plus the dead-dialog removal part of SPH-04.**
- **Outcome:** Home loads without a screen-covering pop-up that fails contrast; the Carnival page has one ticket call to action; plural/typo fixes; footer links meet touch size; shared links get an image; internal study pages and unused fonts leave the published folder.
- **Affected pages:** home, Carnival, all pages (header, footer, alt text), plus `dist/_headers`/`sitemap.xml` untouched.
- **Dependencies:** none; the announcement band uses existing text from the pop-up.
- **How to verify:** at 390×844 and 360×800, load home and confirm no modal opens, the band is dismissible and readable, contrast ≥4.5:1 by computed check; confirm Carnival shows a single ticket CTA above the fold; `scrollWidth === innerWidth` on every page; link-preview check for og:image; `npm test` (booking tests) still passes; no form submitted.

**Second batch (after client answers):** SPH-01, SPH-02, SPH-03, SPH-04 (CTA path), SPH-08, SPH-11.

Waiting for your selection of finding IDs before any code changes.
