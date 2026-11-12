# Urban luxury wellness / longevity clubs: websites and membership pages (visited live 11 Nov 2026)

Method note. Every "live" observation below was read from the real site on 11 Nov 2026 with a headless browser at 1280 px wide (plus a 390 px pass for six pages). Colours and fonts are computed CSS values converted to hex; where a colour was only eyeballed from a screenshot it is marked "approx.". Page heights are document heights at 1280 px (one desktop screen is roughly 800 px). Word counts include navigation and footer, so real body copy is lower. Screenshots are in `screenshots/` with the prefix `urban-`.

Coverage and verification status:

| Club | Verified live | URL(s) | Status |
|---|---|---|---|
| Remedy Place (NY/LA/Boston) | Yes | https://www.remedyplace.com/ , https://www.remedyplace.com/memberships | Full. Note `/membership` (singular) is a 404. |
| Surrenne (London, Maybourne) | Yes | https://www.surrenne.com/en , /en/membership , /en/membership/surrenne-belgravia , /en/apply | Full |
| Six Senses Place (London) | Yes | https://www.sixsensesplace.com/london , https://www.sixsensesplace.com/join-us/ | Full. `sixsenses.com/en/place/london` returned "Access Denied". |
| Continuum Club (NY) | Yes, but rebranded | https://continuum.club/ redirects to https://house120.com/ | Now "House 120". Single-page site; `/membership/` is a 404. Lower half of the page did not render in the full-page screenshot (scroll-reveal animation), so that part is from page text and CSS only. |
| HEIMAT (LA) | Yes | https://heimat.com/ , https://heimat.com/membership/ | Full |
| Saint Haven (Melbourne/Sydney) | Yes | https://sainthaven.com.au/ , https://sainthaven.com.au/location/collingwood | Public site is only a location chooser plus one-screen location pages. Application form not opened. |
| The Lanesborough Club & Spa (London) | Yes | https://www.lanesboroughclubandspa.com/membership/ | Full |
| Third Space (London) | Yes | https://www.thirdspace.london/membership/ | Full |
| KX (London) | Yes | https://www.kxlife.co.uk/membership/ | Full, but a cookie panel sat over the screenshot |
| THE WELL | Partly | https://www.the-well.com/ , https://www.the-well.com/locations/bay-harbor-islands | No New York club and no standalone membership page found on the live site; `the-well.com/membership` resolves to the homepage. Site now centres on Miami clubs, residences and offices. |
| Othership (Toronto/NY) | Yes | https://www.othership.us/memberships | Full |
| Bathhouse (NY) | Yes | https://bathhouse.com/memberships | Full (added as a comparison) |
| Equinox | Yes | https://www.equinox.com/memberbenefits | Full. E by Equinox not found or visited. |
| Lanserhof at The Arts Club | Partly | https://www.theartsclub.co.uk/lanserhof-at-the-arts-club/ | Only the Arts Club's own page. `lanserhof.com/en/lanserhof-at-the-arts-club` rendered an empty shell and `lanserhof.com/en/london` is a 404. |
| Aman Club / Aman Spa | Partly | https://www.aman.com/wellness | `aman.com/aman-club` redirects to the homepage; no public Aman Club membership page found. |
| Bamford Wellness Club | No | https://www.bamfordclub.com/ | Redirects to the Bamford shop homepage (bamford.com/us/). Not verified. |
| Sanctum | No | https://www.sanctum.club/ | Resolved to a parked lander page. Not verified. |

---

## 1. Homepage look: palette, photography, whitespace, motion, navigation, mood

### Takeaway
The top tier splits into two camps: near-black "cinematic" sites with warm stone text (Remedy Place, House 120, Equinox, Bathhouse) and warm cream "editorial" sites with one saturated accent (Surrenne, HEIMAT, Lanesborough, THE WELL, Aman). Almost none uses pure white with pure black; almost all pair one thin display face with small, letter-spaced uppercase labels.

### Cited Findings

**Remedy Place** — [homepage](https://www.remedyplace.com/), [memberships](https://www.remedyplace.com/memberships)
- Palette: background `#000000`; body text warm stone `#B9B2AA`; headings off-white `#EDECEA` or `#FFFFFF`; card and panel fill is the stone colour at 7% opacity (`rgba(185,178,170,0.07)`); hairline borders are the stone colour at 40% opacity. No accent colour other than a tan numeral (approx. `#B5A98C`). — [Remedy Place](https://www.remedyplace.com/memberships)
- Type: headings in "Beausite Slick" at weight 300, sentence case, 41–59 px, letter-spacing about 0.01em; body in "Beausite Classic" at 14–16 px; labels in 10.5–11 px uppercase with 0.16–0.2em tracking. — [Remedy Place](https://www.remedyplace.com/)
- Photography: very dark, low-key interiors and warm-skin portraits in a cedar sauna; images sit under a dark overlay so text reads directly on them. One video element on the homepage. — [Remedy Place](https://www.remedyplace.com/)
- Navigation: single thin top bar, wordmark left, six small uppercase links, one outlined "BOOK" box at the right; a small floating "CONCIERGE" pill sits on the right edge. — [Remedy Place](https://www.remedyplace.com/memberships)
- Homepage length about 7,170 px. Includes a founder pull quote attributed to "Dr. Jonathan Leary · Founder & CEO". — [Remedy Place](https://www.remedyplace.com/)

**Surrenne** — [homepage](https://www.surrenne.com/en)
- Palette: cream `#F2E9D4` page; sage `#B6C5B8` alternate band and footer; coral `#FF6F4D` for the single filled button; black text. — [Surrenne](https://www.surrenne.com/en)
- Type: "Tiempos Fine" serif, uppercase, 80.5 px for section titles (26 px for sub-titles); "Suisse Intl" 15.7 px uppercase for eyebrow labels; "Commuters Sans" for body. — [Surrenne](https://www.surrenne.com/en)
- Imagery: on membership pages the hero is not a gym at all but soft-focus, saturated macro flower photography (green, cobalt, orange), with facility photos kept small and secondary. Two videos on the homepage. — [Surrenne Belgravia membership](https://www.surrenne.com/en/membership/surrenne-belgravia)
- Navigation: centred wordmark, a row of uppercase dropdown links beneath, and the coral "APPLY" pill fixed at top right on every page. Giant wordmark repeated full-width above the footer. — [Surrenne](https://www.surrenne.com/en)
- Homepage about 6,520 px; cites being named World's Best Private Members' Club Spa by the World Spa Awards three years running. — [Surrenne](https://www.surrenne.com/en)

**House 120 (formerly Continuum Club)** — [homepage](https://house120.com/)
- `continuum.club` now redirects to `house120.com`, titled "Home - House 120". — [House 120](https://house120.com/)
- Palette: near-black `#0D0D0D`; text warm bone `#D8D2C8`; bronze `#8B6A43` for filled buttons and accents; a deep green `#1F4E46` band behind the membership section; button text `#F5F2EC`. — [House 120](https://house120.com/)
- Type: "sweet-sans-pro" uppercase at weight 200, 32–40 px, for section titles; a serif for the "Why" statement; 14 px uppercase sub-heads. Gold key emblem as a brand device. — [House 120](https://house120.com/)
- Layout: split hero (text panel left, dim amber interior photo right), a three-item icon strip, one large video still with play button, then numbered philosophy items 01/02/03. About 8,860 px, one video. — [House 120](https://house120.com/)

**HEIMAT** — [homepage](https://heimat.com/)
- Palette: cream `#F7F3E2`; vermilion `#DD3A23`; terracotta `#CE4F2D`; charcoal `#282829`. — [HEIMAT](https://heimat.com/membership/)
- Type: "Suisse Works" italic uppercase serif for hero lines (40–56 px); "GT America Extended" uppercase for everything else. — [HEIMAT](https://heimat.com/)
- Photography: golden-hour lifestyle shots of people laughing at a rooftop pool; two videos on the homepage. Homepage about 4,250 px. — [HEIMAT](https://heimat.com/)

**Six Senses Place London** — [London page](https://www.sixsensesplace.com/london)
- Palette: white `#FFFFFF` alternating with warm off-white `#F6F3F0`; text `#212529`; cream footer (approx. `#FDF6E0`). Type is Poppins throughout, 32 px sentence-case statements rather than big titles. — [Six Senses Place](https://www.sixsensesplace.com/london)
- Hero imagery is an extreme close-up of a face with eyes closed, not the building. Page about 7,960 px and written as a day-in-the-life narrative. — [Six Senses Place](https://www.sixsensesplace.com/join-us/)

**The Lanesborough Club & Spa** — [membership](https://www.lanesboroughclubandspa.com/membership/)
- Palette: warm paper `#F5F4F2` and `#F0EFEB`; slate-navy text `#333F48`; dark slate footer strip. Type: "Boska" italic serif headings at 50 px in sentence case; Gill Sans body; 13 px uppercase buttons. — [Lanesborough Club & Spa](https://www.lanesboroughclubandspa.com/membership/)
- Photography: warm, classical interiors and still-life details (robes hanging, mosaic pool) with generous margins around every image. — [Lanesborough Club & Spa](https://www.lanesboroughclubandspa.com/membership/)

**THE WELL** — [homepage](https://www.the-well.com/)
- Palette: white with warm greige bands `#F2EDE9` and `#F8F6F4`; all text and the footer in one espresso brown `#4D362B`. Type: "Chronicle Display" at weight 200, 80 px hero, title case; "Styrene B" body. Two videos. About 5,590 px. — [THE WELL](https://www.the-well.com/)

**Saint Haven** — [homepage](https://sainthaven.com.au/), [Collingwood](https://sainthaven.com.au/location/collingwood)
- The entire public site is one screen per page: a video or photo hero inset with a white margin, hamburger menu left, centred wordmark with "Private Club" beneath, and nothing below the fold. Type: "ivypresto-display" at weight 300, uppercase, 56 px, with wide-tracked "GT America" sub-lines. Text `#333333` on white. — [Saint Haven](https://sainthaven.com.au/location/collingwood)

**Others**
- Third Space: dark `#1E1E1E` bands with full-bleed photography; "GT Sectra" serif at weight 300, 48 px, sentence case; Circular body. — [Third Space](https://www.thirdspace.london/membership/)
- KX: white page, antique gold `#B4A97C` 77 px heading in "Bicyclette". — [KX](https://www.kxlife.co.uk/membership/)
- Aman: paper `#F3EEE7`, text `#313131`, "Lyon Display/Text" serif at only 31 px for H2 and 19.6 px for H3. — [Aman Wellness](https://www.aman.com/wellness)
- Equinox: black, "Equinox Sans" uppercase 64–72 px, two videos, and a "Black Friday early access" promotion as the homepage headline. — [Equinox](https://www.equinox.com/memberbenefits)
- Othership: warm grey `#ECE8E3`, aubergine `#372338`, rust `#A24E2B`; "Lido Condensed" headings. — [Othership](https://www.othership.us/memberships)
- Bathhouse: black with "Roboto Mono" everywhere. — [Bathhouse](https://bathhouse.com/memberships)

### Inferences
- The "expensive" signal is restraint: two or three colours total, one of them an off-white or off-black, and at most one accent used only on the action button (Surrenne coral, House 120 bronze, HEIMAT vermilion).
- Display type is light (weight 200–400) and large; nothing in the top tier uses bold headlines. Aman goes the other way and uses small serif headings, which reads as the most confident of all.
- The most distinctive sites avoid showing equipment in the hero: Surrenne uses flowers, Six Senses Place a face, HEIMAT friends at a pool.
- For a small women's circle without a building to photograph, the Surrenne (abstract nature macro) and Six Senses Place (close-up portrait) approaches transfer far better than the interior-led approach of Remedy Place or Lanesborough.

### Gaps
- Scroll-triggered motion could not be observed in a headless browser; only the count of video elements is reliable.
- Aman Club, Bamford Club, Sanctum, E by Equinox and Lanserhof's own page for the Arts Club could not be seen (see table).

---

## 2. Membership page: section order, length and amount of copy

### Takeaway
Top-tier membership pages are short: 3,500–7,000 px and 230–900 words including navigation. The common spine is hero, one statement paragraph, the offer (one to four options), what is included, how to join, a final call to action. FAQ, testimonials and founder notes are rare on the membership page itself.

### Cited Findings

**Remedy Place** — about 6,940 px, about 895 words, no videos, only two images — [source](https://www.remedyplace.com/memberships)
1. Hero over a dark interior: eyebrow "WAYS IN", headline saying membership is not required, one line of explanation, then three ways in listed as small label-plus-sentence pairs (à la carte, day pass, membership), one white button.
2. "Plans and pricing": headline stating the starting monthly price, four small cards (one per club) each with a "from" price, a one-line range and a "See plans" text link; a "Compare every tier" outlined button; a fine-print line about what every tier includes and the cancellation terms.
3. Text-only statement block: headline "We are not a private members club." plus two short paragraphs.
4. Split screen: portrait photo left; right, eyebrow "WHO IT IS FOR", headline, paragraph, then three label-plus-sentence qualifiers.
5. Full-bleed dark image band with a short hospitality statement.
6. Centred oversized numeral "200", headline about the member cap, paragraph, a pull quote, a second paragraph.
7. Text-only block on how joining works (no application; come and visit first).
8. Split: "Start a conversation" headline left, a bordered form card right (club, name, email, phone, visited before, note) with a white button worded as the concierge reaching out.
9. Centred closing headline with a single outlined "Find a club" button.
10. Newsletter row and footer.

**Surrenne (hub page)** — about 3,840 px, about 284 words — [source](https://www.surrenne.com/en/membership)
1. Centred 80 px "MEMBERSHIP" title. 2. Full-bleed image. 3. Statement headline "A new era of wellness" plus one paragraph. 4. Two location blocks (Belgravia, Riviera), each a one-sentence pitch and "Discover more". 5. Giant wordmark and footer.

**Surrenne Belgravia** — about 4,460 px, about 442 words — [source](https://www.surrenne.com/en/membership/surrenne-belgravia)
1. Breadcrumb, small eyebrow with the location, 80 px serif "MEMBERSHIP".
2. Full-bleed macro flower image.
3. Split: square image left; right, eyebrow "Invest in a year of", serif sub-head, three short paragraphs, outlined "View brochure" pill.
4. Offer row: large serif statement at left; two image tiles at right labelled Individual membership and Joint membership, each with a coral "Apply" pill. No prices.
5. Sage band: eyebrow "Annual membership inclusion", 80 px "HIGHLIGHTS", then a horizontal slider of seven image cards (counter "1 / 7", two round arrow buttons), each a label and one sentence.
6. Split cross-sell to the other location with an outlined pill.
7. Giant wordmark, sage footer.

**Surrenne apply page** — about 1,970 px, about 202 words: 80 px "Apply for membership" title, then just the two tiles (Individual, Joint) each with a coral "Apply" pill. — [source](https://www.surrenne.com/en/apply)

**Six Senses Place** — [Join Us](https://www.sixsensesplace.com/join-us/), about 2,400 px, about 287 words
1. Short image hero with "JOIN US". 2. Tagline ("One membership. Every rhythm") and a two-sentence instruction. 3. A 2 x 2 grid of tier cards; each card is a dark gradient panel (name, a five-word positioning line, age rule) above a white panel with the joining fee, the annual fee, a "Choose plan" outlined pill and a collapsed "What's included" row with one sentence. 4. Footer with FAQ link.
- The longer [London page](https://www.sixsensesplace.com/london) (about 7,960 px, about 858 words) carries the persuasion: seven alternating white and off-white chapters, each a 32 px sentence headline, one paragraph, and a row of captioned image cards, ending in a full-bleed "Explore London membership" band with a "Join us" pill and an underlined "Request information" link.

**House 120** — single page, about 8,860 px, about 697 words — [source](https://house120.com/)
Hero with statement and "Apply for membership"; three-icon strip; video; "Why House 120" two-column statement; "The Philosophy" with numbered items 01–03; "The Experience" with four items; "The Care Team"; "Member Testimonials" (two quotes); "The Membership" on a deep green band with three tiers (Access, House, Concierge) each described in a paragraph; "Apply for membership"; closing mission line.

**HEIMAT** — about 3,600 px, about 231 words — [source](https://heimat.com/membership/)
1. Full-bleed lifestyle photo with a two-line italic serif headline. 2. One uppercase headline plus two accordion bars (Movement & Recovery, Community) holding the inclusions as bare lists, and a filled "Apply" pill. 3. Terracotta band: the price as the headline, contract length and age rule as two sub-lines, a dark "Apply now" pill, then two small lines about committee review and inclusivity. 4. Vermilion contact band with phone and email.

**Saint Haven** — one screen (577 px), about 20 words: location eyebrow, one headline, one sentence, one button "Apply for membership". — [source](https://sainthaven.com.au/location/collingwood)

**Lanesborough** — about 4,130 px, about 563 words — [source](https://www.lanesboroughclubandspa.com/membership/)
1. Two offset images (one tall, one small) with an italic serif headline, two short paragraphs and an outlined "Enquire now". 2. A grey tab bar of six membership types as underlined text links. 3. Split: tall image left; right, the selected membership's name, one paragraph, four accordion rows (Fitness & classes, Spa & treatments, Dining & entertaining, Hotel & services) with bulleted benefits, "Enquire now". 4. Full-width image carousel with caption. 5. Statement plus paragraph with "Gallery" and "Virtual tour" buttons. 6. Instagram row. 7. Three small closing actions. The enquiry form opens as an overlay.

**Third Space** — about 7,450 px, about 783 words, 85 images: hero statement; "Become a member and enjoy…" benefit cards; amenities cards; clubs; "Membership Add-Ons" with prices; a "Membership FAQ's" accordion; an "Enquire today" form. — [source](https://www.thirdspace.london/membership/)

**KX** — about 3,550 px, about 483 words: gold title; intro paragraphs; "Membership Options" (individual, joint, out-of-town) with "Apply now"; "KX Wellness Assessment" with "Apply now"; "Club Features". — [source](https://www.kxlife.co.uk/membership/)

**Othership** — about 7,330 px, about 989 words: hero; three access benefits; perks; "Member[ship] Options"; experience; corporate; "Milestone Gifts"; FAQ; newsletter; app. — [source](https://www.othership.us/memberships)

**Bathhouse** — about 4,000 px, about 352 words: hero; two plan cards with price in the heading; "The Perks"; rates; sign up. — [source](https://bathhouse.com/memberships)

**Equinox** — about 8,540 px, about 684 words: benefits page of uppercase headline bands and video, with "Join today" and "Inquire now". — [source](https://www.equinox.com/memberbenefits)

**THE WELL** — membership is a paragraph inside the club location page (about 6,770 px) contrasting day guests with club members, with inclusions written as dot-separated lists. — [source](https://www.the-well.com/locations/bay-harbor-islands)

**Lanserhof at The Arts Club** — the Arts Club page gives membership one short paragraph and asks applicants to email reception. — [source](https://www.theartsclub.co.uk/lanserhof-at-the-arts-club/)

### Inferences
- The more exclusive the club, the shorter the page: Saint Haven (one screen), Surrenne apply (two tiles), HEIMAT (231 words). Long pages with FAQs and add-on prices (Third Space, Othership, Equinox) read as premium-mass rather than private.
- Only Remedy Place uses long-form argument, and it does so in very short blocks (headline plus two paragraphs) with a lot of black space between them.
- Founder notes and testimonials are almost absent from membership pages. Remedy uses one unattributed pull quote; House 120 has two testimonials. FAQs appear only at Third Space and Othership (Six Senses Place and Surrenne link to a separate FAQ page).
- A workable order for a single-offer circle: hero statement; who it is for; what a membership holds (three to six items); the price stated once, plainly; how joining works in two or three sentences; one closing action.

### Gaps
- Section order for House 120 below the philosophy section is from headings and text only; its visual treatment was not seen.
- The application forms themselves (Surrenne, HEIMAT's app.heimat.com, Saint Haven, Six Senses "Choose plan") were deliberately not opened or submitted, so their length and questions are unknown.

---

## 3. How price and tiers are presented

### Takeaway
Hiding price is no longer the rule. Of twelve sites read, eight show prices openly; only Surrenne, Saint Haven, House 120 and Lanesborough keep the fee behind an application or enquiry. Where price is shown, it is stated once, large and without decoration.

### Cited Findings
- HEIMAT states one offer as a headline on a coloured band: a monthly figure plus an initiation fee, with "one year contract" and the minimum age as the only qualifiers. No tiers, no table. — [HEIMAT](https://heimat.com/membership/)
- Six Senses Place shows four tiers as cards (Beyond, Full, Under 35, Social) with a joining fee and an annual fee each: £37,500 annual with no joining fee for Beyond; £1,000 joining plus £7,500, £5,700 and £3,000 annual for the others. Each tier gets a five-word positioning line and a one-sentence "for those who…" description; details sit in a collapsed row. — [Six Senses Place](https://www.sixsensesplace.com/join-us/)
- Remedy Place uses a "starts at" headline ($249 a month) and four small per-club cards with a from-price and range (for example $299 to $3,500 in New York), linking out to per-club plans; it also states monthly billing and cancellation after the first month in fine print. — [Remedy Place](https://www.remedyplace.com/memberships)
- Surrenne shows no price anywhere on the membership, location or apply pages; tiers are two image tiles (Individual, Joint) and inclusions are counted ("Twelve annual studio classes", "Four … treatments or facials", "One consultation"). A brochure is offered by button. — [Surrenne Belgravia](https://www.surrenne.com/en/membership/surrenne-belgravia)
- House 120 names three tiers (Access, House, Concierge) in prose with no prices. — [House 120](https://house120.com/)
- Lanesborough shows no membership fee but does print small add-on prices (locker hire at £1,000 or £500 a year) inside the benefits list; six membership types are tabs. — [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
- Saint Haven shows no price and no tiers. — [Saint Haven](https://sainthaven.com.au/location/collingwood)
- KX lists option types (individual, joint, out-of-town) without prices. — [KX](https://www.kxlife.co.uk/membership/)
- Third Space shows add-on prices (lockers £40 and £80 a month, training from £85 an hour) but routes the membership price to an enquiry form. — [Third Space](https://www.thirdspace.london/membership/)
- Bathhouse puts the price in the plan heading ($145 and $225) with a per-visit equivalent beneath. — [Bathhouse](https://bathhouse.com/memberships)
- Othership and Equinox run promotional banners (a two-week trial price with an end date; a zero-initiation offer "ends soon"). — [Othership](https://www.othership.us/memberships), [Equinox](https://www.equinox.com/memberbenefits)
- Press reports, not the club's site: Continuum launched at about $10,000 a month and later introduced lower tiers; one outlet reports current House 120 dues of about $16,500 to $71,500 a year. — [ThePricer](https://www.thepricer.org/how-much-does-house-120-membership-cost-formerly-continuum-club/) (single low-authority source; treat as unconfirmed)
- Press reports put Aman Club at roughly a $200,000 initiation fee plus about $15,000 a year; Aman publishes no price page. — [Yahoo](https://ca.news.yahoo.com/people-pay-200k-initiation-fee-171529983.html)

### Inferences
- Price shown plainly reads as confident, not cheap, when it is (a) a single figure, (b) set in the same type as the headlines, (c) free of strikethroughs, "save", countdowns or "limited offer" language. Countdown and discount banners are the clearest marker separating Othership and Equinox from the tier above.
- The HEIMAT pattern (price as a headline on a colour band, two qualifiers, one button, one line on how applications are reviewed) is the closest model for a single ₹10,000 six-month offer paid by link.
- Surrenne's counted inclusions ("twelve", "four", "one") are a useful way to describe what a term holds, for example the number of gatherings in six months.
- If a single offer needs a comparison point, Six Senses Place's one-line "for those who…" sentence does the work a feature table would otherwise do.

### Gaps
- Surrenne, Saint Haven, House 120, Lanesborough and KX fees could not be confirmed from their own sites.
- Whether Six Senses Place's "Choose plan" leads to payment or to an application was not tested.

---

## 4. Primary call to action: wording, placement, styling

### Takeaway
"Apply" is the dominant word (Surrenne, HEIMAT, House 120, Saint Haven, KX, Six Senses Place), with "Enquire" for hotel clubs and "Join" only at the mass-premium end. The button is small, uppercase, letter-spaced, and either a full pill or a square-cornered box; it sits in the header on every page and is repeated once beside the offer.

### Cited Findings
- Surrenne: "APPLY" as a coral `#FF6F4D` pill, black text, 14 px uppercase, 0.1em tracking, padding 12 x 32 px, radius 100 px, fixed in the header; repeated under each membership tile. Secondary actions ("View brochure", "Explore … membership") are outlined pills. — [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia)
- HEIMAT: "APPLY" as an outlined vermilion pill in the fixed header (16 px italic uppercase, 2 px tracking, radius 600 px); filled vermilion "APPLY" under the inclusions; charcoal filled "APPLY NOW" under the price. Three placements on a 3,600 px page. — [HEIMAT](https://heimat.com/membership/)
- House 120: "APPLY" as a bronze `#8B6A43` square-cornered block in the top bar and "APPLY FOR MEMBERSHIP" in the hero and again after the tiers; 12 px uppercase, radius 0. — [House 120](https://house120.com/)
- Saint Haven: one translucent grey square-cornered box, "APPLY FOR MEMBERSHIP", wide-tracked uppercase, centred in the hero. It is the only link on the page besides the menu. — [Saint Haven](https://sainthaven.com.au/location/collingwood)
- Six Senses Place: "APPLY FOR LONDON MEMBERSHIP" as a white-outlined pill in the header (14 px uppercase, radius 28 px); "JOIN US" outlined pill (18 px, radius 100 px) on the closing band beside an underlined text link "Request information"; "CHOOSE PLAN" outlined pills in the tier cards; "ENQUIRY" as a plain text link top left. — [Six Senses Place](https://www.sixsensesplace.com/london)
- Remedy Place: no "apply" or "join" button at all. Actions are "See options at your club" (white filled box, 11 px uppercase, 0.2em tracking, radius 0), "Compare every tier" and "Find a club" (1 px outlined boxes), and a form button worded as having the concierge reach out. The enquiry section is headed "Start a conversation." — [Remedy Place](https://www.remedyplace.com/memberships)
- Lanesborough: "ENQUIRE NOW" as a 1 px outlined box, radius 4 px, 13 px uppercase with 1 px tracking, padding 15 x 40 px; "JOIN THE CLUB" in the sticky header in the same style. Membership types are underlined text links. — [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
- KX: "APPLY NOW" as a white box with a 1 px black border, radius 0. — [KX](https://www.kxlife.co.uk/membership/)
- Third Space: "JOIN US" as a white pill fixed in the header; "Enquire today" form at the foot. — [Third Space](https://www.thirdspace.london/membership/)
- Equinox: "JOIN TODAY" and "INQUIRE NOW". Bathhouse: "SIGN UP". Othership: "JOIN NOW". — [Equinox](https://www.equinox.com/memberbenefits), [Bathhouse](https://bathhouse.com/memberships), [Othership](https://www.othership.us/memberships)
- The Arts Club asks Lanserhof applicants to email reception, with no button. — [The Arts Club](https://www.theartsclub.co.uk/lanserhof-at-the-arts-club/)

### Inferences
- Shared button recipe: 11–14 px uppercase, tracking 0.07–0.2em, 1 px border or one flat fill, no shadow, no gradient, no icon, generous horizontal padding (28–40 px). Corners are either fully round or fully square; nothing in between except Lanesborough's 4 px.
- One filled button per screen at most; everything else is outlined or an underlined text link.
- Verb choice tracks positioning: "Apply" implies review; "Enquire" implies a conversation with a person; "Join" and "Sign up" imply a transaction. Remedy's "Start a conversation" is the warmest and least transactional wording seen.
- For a circle that takes payment by link, an honest two-step works: a soft primary verb for the page-level action, and the payment button appearing only once, directly beneath the stated fee (as HEIMAT does with "Apply now" under the price).

### Gaps
- Hover and focus states were not captured.

---

## 5. Signalling exclusivity and limited numbers without sounding salesy

### Takeaway
The strongest pages state a limit as a plain fact, give a non-commercial reason for it, and describe who the membership is for. None of the top-tier pages uses urgency, countdowns or "only X places left".

### Cited Findings
- Remedy Place states a cap of two hundred members per club, shows it as an oversized "200" numeral, and immediately explains the reason as being about members representing the club rather than keeping people out; it says of the cap that it is "Not to be exclusive". — [Remedy Place](https://www.remedyplace.com/memberships)
- Remedy Place also defines the audience in a "Who it is for" block with three short qualifiers (comes often, wants a routine, leads by example), and says there is no application form because joining follows from visiting. — [Remedy Place](https://www.remedyplace.com/memberships)
- HEIMAT uses one sentence: applications are being accepted and are reviewed by a committee on a rolling basis, followed by one sentence on inclusivity. — [HEIMAT](https://heimat.com/membership/)
- House 120 says membership is intentionally curated to bring together people with a shared commitment. — [House 120](https://house120.com/)
- Six Senses Place closes with a single sentence saying membership is open to people "curious about themselves" who care about making change. — [Six Senses Place](https://www.sixsensesplace.com/london)
- Surrenne signals exclusivity through members-only events ("private invitations" to a calendar of member events), a personal assessment at the start of every membership, a members' login in the header, and a "Surrenne Etiquette" link in the footer. — [Surrenne Belgravia](https://www.surrenne.com/en/membership/surrenne-belgravia)
- Saint Haven does it by withholding: wordmark with "Private Club" beneath, one sentence, one button. — [Saint Haven](https://sainthaven.com.au/location/collingwood)
- Lanesborough offers a personal tour with the membership team rather than a sign-up. — [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
- KX and Surrenne both say every membership begins with a personal assessment. — [KX](https://www.kxlife.co.uk/membership/), [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia)
- A press release reported by a news aggregator says Continuum capped its New York flagship at 250 members. — [Webull/PR Newswire](https://www.webull.com/news/14071949012321280) (not confirmed on the House 120 site)
- By contrast Othership and Equinox use time-limited offers with end dates. — [Othership](https://www.othership.us/memberships), [Equinox](https://www.equinox.com/memberbenefits)

### Inferences
- Five non-salesy devices recur: (1) a real number stated once, (2) a values-based reason for the limit, (3) "who it is for" written as recognition rather than qualification, (4) a human step (assessment, tour, conversation, committee) before or at joining, (5) members-only gatherings named as a benefit.
- A small circle has a naturally true version of (1) and (2): the size of the room and the wish that everyone knows everyone. Stating the actual number as a large numeral, as Remedy does, would be accurate rather than theatrical. The number itself must come from the client; none is assumed here.
- Warmth beats gatekeeping in 2026 copy: Remedy and Six Senses Place both go out of their way to sound welcoming while still being limited.

### Gaps
- No site visited shows a waitlist; "Join the waitlist" and "Request an invitation" were not found as live wording on any of these pages.

---

## 6. Notable layout devices

### Takeaway
A small set of devices does nearly all the work: a quiet hero, alternating split screens, one oversized element per page (a word, a numeral or the wordmark), label-plus-sentence lists instead of bullets, and one colour band that isolates the offer.

### Cited Findings
- Oversized single element: Remedy's "200" numeral; Surrenne's 80 px one-word section titles ("MEMBERSHIP", "HIGHLIGHTS") and the full-width wordmark above the footer. — [Remedy Place](https://www.remedyplace.com/memberships), [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia)
- Eyebrow plus headline: a 10–16 px uppercase label above every headline ("WAYS IN", "WHO IT IS FOR", "INVEST IN A YEAR OF", "ANNUAL MEMBERSHIP INCLUSION"). — [Remedy Place](https://www.remedyplace.com/memberships), [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia)
- Split screens with image one side and text the other, alternating: Remedy (portrait left, "who it is for" right), Surrenne (square image left, statement right), Lanesborough (tall image left, accordion right), House 120 (text left, photo right in the hero). — sources as above and [Lanesborough](https://www.lanesboroughclubandspa.com/membership/), [House 120](https://house120.com/)
- Label-plus-sentence lists in place of bullets: Remedy's three ways in and three qualifiers. — [Remedy Place](https://www.remedyplace.com/memberships)
- Numbered steps: House 120's philosophy as 01, 02, 03 with a thin vertical rule. — [House 120](https://house120.com/)
- Pull quote: Remedy sets one centred serif-like quote between two paragraphs under the numeral; the homepage carries a founder quote with name and title in small caps. — [Remedy Place](https://www.remedyplace.com/)
- Horizontal scroller: Surrenne's seven "Highlights" cards with a "1 / 7" counter and two round arrow buttons; Lanesborough's image carousel with dots. — [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia), [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
- Accordions for inclusions: Lanesborough's four category rows; HEIMAT's two coloured bars; Six Senses Place's "What's included" row inside each card. — [Lanesborough](https://www.lanesboroughclubandspa.com/membership/), [HEIMAT](https://heimat.com/membership/), [Six Senses Place](https://www.sixsensesplace.com/join-us/)
- Colour band isolating the offer: HEIMAT's terracotta price band; House 120's deep green membership band; Surrenne's sage highlights band. — [HEIMAT](https://heimat.com/membership/), [House 120](https://house120.com/), [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia)
- Form as a bordered card inside the page rather than a separate page: Remedy's concierge form; Lanesborough's overlay; Third Space's foot-of-page form. — [Remedy Place](https://www.remedyplace.com/memberships), [Third Space](https://www.thirdspace.london/membership/)
- Offset image pair (one large, one small, different heights) as a hero instead of a full-bleed banner. — [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
- Tier cards with a dark gradient "cover" and a white details panel. — [Six Senses Place](https://www.sixsensesplace.com/join-us/)
- Dark versus light: Remedy, House 120, Equinox and Bathhouse are dark throughout; Surrenne, HEIMAT, Lanesborough, Six Senses Place and THE WELL are light throughout with one tinted band. None alternates black and white sections. — sources as above
- Sticky elements on desktop are limited to the header button (Surrenne, HEIMAT, Lanesborough, Third Space) and Remedy's small edge "Concierge" pill. — sources as above

### Inferences
- One oversized thing per page, not several. Remedy has the numeral; Surrenne has the one-word titles; everything else stays at body size.
- Label-plus-sentence lists and accordions keep long inclusion lists from looking like a feature comparison.
- Pages commit to one mood. Mixing a dark cinematic hero with cream editorial sections is not something any of these sites does.

### Gaps
- No site in this set uses a sticky bottom bar on desktop.

---

## 7. What works on mobile (390 px)

### Takeaway
All six pages tested reflow to a single column with no horizontal scroll; the membership action stays reachable either in a fixed header or, at Six Senses Place, in a fixed bottom bar.

### Cited Findings
- Six Senses Place Join Us: a fixed bottom bar 74 px tall and full width carrying "APPLY FOR LONDON MEMBERSHIP"; top bar reduces to hamburger, wordmark and account icon; H1 40 px, body 18 px; page 4,434 px. The cookie panel covers the lower half of the first screen until dismissed. — [Six Senses Place](https://www.sixsensesplace.com/join-us/)
- Surrenne Belgravia: fixed 72 px header that keeps the "APPLY" pill visible; section titles drop from 80 px to about 50 px; body 16 px; page 5,544 px. — [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia)
- Remedy Place memberships: 64 px sticky header with "BOOK"; H1 drops from 56 px to 30 px; body 16 px; two 50 px round floating buttons bottom corners; page 7,862 px. — [Remedy Place](https://www.remedyplace.com/memberships)
- HEIMAT membership: fixed 80 px header keeps "APPLY"; H1 24 px; body text only 12 px; page 4,246 px. — [HEIMAT](https://heimat.com/membership/)
- House 120: no fixed or sticky element at 390 px; H1 32 px, body 14 px; page 9,655 px. — [House 120](https://house120.com/)
- Saint Haven: still exactly one screen (844 px), H1 28 px, body 16 px. — [Saint Haven](https://sainthaven.com.au/location/collingwood)
- None of the six pages overflowed horizontally at 390 px. — measured on each URL above

### Inferences
- Body text at 16–18 px (Remedy, Surrenne, Six Senses, Saint Haven) reads far better than HEIMAT's 12 px uppercase; uppercase body copy at small sizes is the weakest mobile choice seen.
- A persistent action is the norm on phones. The fixed bottom bar (Six Senses Place) is the most thumb-friendly; the Sphere carnival page already uses the same idea.
- Headline sizes roughly halve on mobile (56 to 30, 80 to 50); the light weight is kept.
- Short pages win on phones: Saint Haven and HEIMAT need three or four thumb scrolls; House 120 needs more than eleven with no persistent button.

### Gaps
- Mobile was checked by viewport emulation only, not on a physical device; touch behaviour of sliders and accordions was not tested.
- Only the first screen was captured in mobile screenshots.

---

## 8. Who designed these sites, and why

### Takeaway
Reliable public design credits are scarce; only Remedy Place's earlier site has a documented rationale.

### Cited Findings
- Remedy Place's site was a 2023 Webby nominee in Health & Wellness. The entry describes the aim as "Moody, sexy, sleek, functional, engaging", says three high-fidelity concepts were presented and the client chose the simplest, and lists Next.js, Sanity and Locomotive Scroll. — [Webby Awards](https://www.webbyawards.com/crafted-with-code/remedy-place/)
- Maybourne's group identity was created by FutureBrand London. — [FutureBrand](https://www.futurebrand.com/our-work/maybourne)
- Saint Haven is a GURNER Group brand; architecture, interiors and photography for the first club are credited in-house. — [The Local Project](https://thelocalproject.com.au/articles/saint-haven-by-gurner-group-project-feature-the-local-project/)
- The Third Space site footer credits "Without" as branding agency and "Plug & Play" as web agency. — [Third Space](https://www.thirdspace.london/membership/)

### Inferences
- The Webby note that the client "preferred the simplest" concept matches what the live pages show across the tier: reduction is the brief.
- The Remedy membership page seen in November 2026 (with its "not a private members club" argument and four clubs) is probably a later iteration than the 2023 award entry; the entry describes applying for membership, which the current page explicitly drops.

### Gaps
- A search summary attributed the Remedy Place build to an agency called Boundary, but the Webby page itself did not show a credit when fetched; unverified.
- A search result pointed to a Made Thought case study for Surrenne (madethought.com/work/surrenne), but the page fetched did not contain Surrenne content; the identity credit is unverified.
- No Awwwards, Siteinspire, It's Nice That, Brand New, Wallpaper* or Monocle coverage of these specific websites was found in the searches run. No credit found for House 120, HEIMAT, Six Senses Place or Lanesborough.

---

## 9. Synthesis: recurring patterns and page archetypes

### Takeaway
Ten patterns recur across the best pages, and the pages fall into four archetypes. For a one-offer, women-only circle paying by link, the closest fits are the "minimal single offer" (HEIMAT, Saint Haven) for structure and the "editorial manifesto" (Remedy Place) for voice, in a light cream palette like Surrenne's.

### Cited Findings (patterns, each tied to where it was observed)
1. **A tinted neutral, never pure white.** Cream `#F2E9D4` (Surrenne), `#F7F3E2` (HEIMAT), paper `#F5F4F2` (Lanesborough), `#F3EEE7` (Aman), greige `#F2EDE9` (THE WELL); or an off-black with warm stone text `#B9B2AA` on `#000000` (Remedy), `#D8D2C8` on `#0D0D0D` (House 120). — [Surrenne](https://www.surrenne.com/en), [HEIMAT](https://heimat.com/membership/), [Lanesborough](https://www.lanesboroughclubandspa.com/membership/), [Aman](https://www.aman.com/wellness), [THE WELL](https://www.the-well.com/), [Remedy Place](https://www.remedyplace.com/memberships), [House 120](https://house120.com/)
2. **One accent, used almost only on the action.** Coral `#FF6F4D` (Surrenne), bronze `#8B6A43` (House 120), vermilion `#DD3A23` (HEIMAT). — same sources
3. **Light-weight display type at large size, with tiny tracked uppercase labels.** Tiempos Fine 80 px (Surrenne), Chronicle Display weight 200 at 80 px (THE WELL), Beausite Slick weight 300 (Remedy), Boska italic 50 px (Lanesborough), GT Sectra weight 300 (Third Space), ivypresto weight 300 (Saint Haven); labels 10–16 px uppercase. — same sources and [Third Space](https://www.thirdspace.london/membership/), [Saint Haven](https://sainthaven.com.au/location/collingwood)
4. **Short pages, few words.** 230–900 words and 3,500–7,000 px for the pages that feel most private; one screen at Saint Haven. — [HEIMAT](https://heimat.com/membership/), [Surrenne](https://www.surrenne.com/en/membership), [Saint Haven](https://sainthaven.com.au/location/collingwood), [Remedy Place](https://www.remedyplace.com/memberships)
5. **Declarative headlines that are complete sentences.** Remedy's section headlines each state a position; Six Senses Place's chapter headings are sentences about a day at the club. — [Remedy Place](https://www.remedyplace.com/memberships), [Six Senses Place](https://www.sixsensesplace.com/london)
6. **Price said once, plainly, or not at all; never discounted.** HEIMAT's price band; Six Senses Place's fee pairs; Surrenne's silence. — [HEIMAT](https://heimat.com/membership/), [Six Senses Place](https://www.sixsensesplace.com/join-us/), [Surrenne](https://www.surrenne.com/en/apply)
7. **A small, quiet button with a considered verb, present in the header and once beside the offer.** — [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia), [HEIMAT](https://heimat.com/membership/), [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
8. **A limit or a human step stated as fact.** Remedy's two hundred; HEIMAT's committee; Surrenne's and KX's personal assessment; Lanesborough's personal tour. — [Remedy Place](https://www.remedyplace.com/memberships), [HEIMAT](https://heimat.com/membership/), [KX](https://www.kxlife.co.uk/membership/), [Lanesborough](https://www.lanesboroughclubandspa.com/membership/)
9. **Inclusions as counted, concrete items, tucked into a slider or accordion.** Surrenne's highlights; Lanesborough's accordion; Six Senses Place's collapsed row. — [Surrenne](https://www.surrenne.com/en/membership/surrenne-belgravia), [Lanesborough](https://www.lanesboroughclubandspa.com/membership/), [Six Senses Place](https://www.sixsensesplace.com/join-us/)
10. **Imagery of feeling rather than facilities, with large margins.** Surrenne's flowers, Six Senses Place's face, HEIMAT's friends, Lanesborough's still lifes. — same sources

**Archetypes**

| Archetype | What defines it | Exemplars (live) | Typical length |
|---|---|---|---|
| A. Editorial manifesto (long-read) | A sequence of short positions, each a sentence headline plus two paragraphs; one oversized numeral or quote; form at the end | [Remedy Place](https://www.remedyplace.com/memberships); partly [Six Senses Place London](https://www.sixsensesplace.com/london) | 7,000–8,000 px, 850–900 words |
| B. Dark cinematic | Near-black ground, warm bone text, metallic accent, dim interior photography and video, numbered philosophy, tiers in prose | [House 120](https://house120.com/); [Remedy Place homepage](https://www.remedyplace.com/); [Equinox](https://www.equinox.com/memberbenefits) | 7,000–9,000 px |
| C. Minimal single offer | One image, one statement, the offer stated once (with or without price), one button; little or nothing else | [HEIMAT](https://heimat.com/membership/); [Saint Haven](https://sainthaven.com.au/location/collingwood); [Surrenne apply](https://www.surrenne.com/en/apply) | 600–3,600 px, 20–230 words |
| D. Light editorial, application-first | Cream ground, big serif one-word titles, art-directed imagery, counted inclusions in a slider, no price, "Apply" fixed in the header | [Surrenne Belgravia](https://www.surrenne.com/en/membership/surrenne-belgravia); [Lanesborough](https://www.lanesboroughclubandspa.com/membership/) (with "Enquire") | 4,000–4,500 px, 450–550 words |
| (E. Transparent tier cards) | Tier cards with fees and a "choose plan" button; closer to a pricing page | [Six Senses Place Join Us](https://www.sixsensesplace.com/join-us/); [Bathhouse](https://bathhouse.com/memberships); [Othership](https://www.othership.us/memberships) | 2,400–7,300 px |

### Inferences
- Recommended blend for the Sphere membership page (design inference, not client copy): archetype C's structure with archetype A's voice and archetype D's palette. Concretely: cream ground with one accent; a light serif headline; a "who it is for" split block; a counted description of what six months holds; the fee as a single headline on a tinted band with the payment button directly beneath and one line on what happens next; a fixed bottom action bar on phones.
- Things to avoid because they mark the tier below: discount or countdown banners, pricing tables with ticks, more than one filled button per screen, bold headlines, stock gym imagery, long FAQs on the membership page, uppercase body copy at small sizes.
- All wording on the Sphere page must still come from the client's source copy; the structures above are containers only.

### Gaps
- No women-only or small-circle club was in this set; all are venue-based clubs with facilities, so the "inclusions" patterns need adapting to gatherings rather than amenities.
- No Indian comparators were visited; rupee price presentation conventions were not researched here.
- E by Equinox, Aman Club, Bamford Club, Sanctum and Lanserhof's own Arts Club page remain unverified.
