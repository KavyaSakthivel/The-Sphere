# Membership application, enquiry, waitlist and "request an invitation" forms at luxury wellness and private members' clubs (observed live, 11 November 2026)

Method note: every form below was opened live in a browser on 11 Nov 2026, read-only (nothing typed, nothing submitted). Field lists come from the page DOM; styling values are computed CSS. "Required" is reported as the page signals it (asterisk or `required` attribute). Anything not seen is listed under Gaps. Screenshots are in `screenshots/` (file names given per form).

## 1. Per-form catalogue: type, location, fields, steps, styling, consent, after-submit

### Takeaway
Fifteen real forms were seen. They fall into two clear families: (a) short "register interest / enquiry" forms of 4 to 8 fields, almost always underline-only inputs on a calm background, and (b) long multi-step applications (Peoplevine or custom) of 20 to 30+ fields with headshot, proposers and card details. Nearly every flagship club uses a hosted third-party tool (Peoplevine, HubSpot, Typeform, WPForms, Webflow) rather than custom code.

### Cited Findings

**A. Saint Haven (Melbourne) – short interest form in a full-screen modal** (`forms-sainthaven-apply.png`)
- Opens from the hero button "APPLY FOR MEMBERSHIP" as a full-screen white overlay with logo top centre and a close X; built on Webflow forms (`w-form` classes). — [Saint Haven](https://sainthaven.com.au/)
- Heading (serif, sentence case): "We welcome your interest in learning more about Saint Haven Private Club"; sub-line: "Membership is limited; we value your interest and will be in touch as opportunities to join become available." — [Saint Haven](https://sainthaven.com.au/)
- Fields in order, two columns: First name *, Last name *, Phone * (country-flag dial-code picker; it auto-selected the India flag for our Indian IP), Email *, Postcode *, Select a location * (dropdown of clubs), "What interests you most about joining Saint Haven?*" (single line, full width), "Referred By" (shown without asterisk, though the DOM marks it required). — [Saint Haven](https://sainthaven.com.au/)
- Styling: no visible labels, placeholder only; underline-only inputs (0 top / 1px bottom, near-black), transparent background, 52px tall, 16px grotesque sans; button is a solid black rectangle, white uppercase widely letter-spaced 12px text, 56px tall, wording "APPLY FOR MEMBERSHIP". — [Saint Haven](https://sainthaven.com.au/)
- Consent: one required tick-box, "By registering your interest, you are agreeing to our Privacy Collection Statement and our Privacy Policy and opting in to receive communications from SAINT HAVEN. You can opt out at any time *". — [Saint Haven](https://sainthaven.com.au/)
- Success state (present in the DOM, replaces the form in place): "Application received. Your application has been received, and we honour your commitment to this next step. Membership is limited, and as space becomes available, our team will be in touch to guide you further." No reply time promised. Error state is the Webflow default "Oops! Something went wrong while submitting the form." — [Saint Haven](https://sainthaven.com.au/)

**B. Six Senses Place London – short enquiry, inline on its own page** (`forms-sixsensesplace-enquiry.png`)
- Own page "/enquiry/", form inline beside the left-hand heading "LET'S START FROM HERE"; custom CMS form (Umbraco-style GUID field names). — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/)
- Fields: FIRST NAME, LAST NAME, EMAIL, PHONE (two columns), then a large textarea labelled "WHAT ENCOURAGES YOU TO ENQUIRE?" with placeholder "Your message". No asterisks shown. — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/)
- Styling: small uppercase letter-spaced labels ABOVE each field plus a light grey placeholder repeating the label; underline-only inputs (1px, 60% black), transparent, 31px tall, 16px Poppins; button is an outlined pill (1px black, radius 100px, transparent, 14px uppercase, 46px tall) reading "Submit". — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/)
- Consent: two separate tick-boxes under small headings SUBSCRIBE ("I'd like to hear what's happening at Six Senses Place London. I understand that I can opt out at any time by unsubscribing.") and PRIVACY ("By clicking "Submit" I have read and accept the Privacy Statement."). — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/)

**C. Six Senses Place London – multi-step application on Peoplevine** (`forms-sixsensesplace-apply-step.png`, `forms-sixsensesplace-join.png`)
- "/join-us/" shows four priced tiers (e.g. Social: £1,000 joining + £3,000 annual; Beyond: £37,500 annual), each with a "CHOOSE PLAN" link to apply.sixsensesplace.com, a Peoplevine-hosted portal (scripts load from storage.peoplevine.com). — [Six Senses Place join](https://www.sixsensesplace.com/join-us/); [application step 1](https://apply.sixsensesplace.com/membership/51/1711)
- Intro copy: "We're delighted you're joining our community. Please complete the form below to help us build a clearer picture of you." — [application step 1](https://apply.sixsensesplace.com/membership/51/1711)
- Step 1 fields in order (asterisk = required, shown inside the placeholder): *First Name, Preferred name, *Last Name, *Date of Birth, Gender (Male / Female / Other / Prefer Not to Say), *Nationality, *@your_Instagram, Any other supporting links, *Email Address, *Preferred Phone (Mobile / Landline / Office), dial-code select + *Phone number, "*How would you like us to contact you?" (Email / Phone / SMS tick-boxes), Primary Residence: *Your address, *Suite / Apt, Additional address line, *City, *Postal Code / Zip Code, *Country, Profile Photo upload ("Upload a clear head shot that can be used to verify who you are when entering Six Senses Place"; "Square jpg or png, max 5MB, with face centred"), "Your proposer" (if you have one), "How did you hear about Six Senses Place?". Button "Next". — [application step 1](https://apply.sixsensesplace.com/membership/51/1711)
- Characterful: Instagram handle is REQUIRED; "Preferred name"; note "Please ensure you are using different details to any prior applications." — [application step 1](https://apply.sixsensesplace.com/membership/51/1711)
- Styling: boxed inputs (1px black border, square corners, white fill, 48px tall, 17px Poppins Light), placeholder-as-label; black pill button (radius 25px) white uppercase 13px "NEXT". — [application step 1](https://apply.sixsensesplace.com/membership/51/1711)

**D. Surrenne (Maybourne, London) – two-step Peoplevine application** (`forms-surrenne-apply.png`)
- "/en/apply" is a chooser (tabs Belgravia / Riviera, cards Individual / Joint) linking to apply.surrenne.com; plus "Make an Enquiry" as a plain mailto link to a named person. — [Surrenne apply](https://www.surrenne.com/en/apply)
- Form page headed "MEMBERSHIP APPLICATION (INDIVIDUAL)", "Step 1 of 2", preceded by the full benefits list and price ("£10,000 plus a £5,000 joining fee"). — [Surrenne application](https://apply.surrenne.com/wellbeing)
- Fields under three serif uppercase section headings. PERSONAL DETAILS: Title (Ms., Mrs., Miss., Mr., Mx., Dr., Sir, Lady…), Forename, Surname, Nationality, Gender, Date of Birth (calendar picker). CONTACT DETAILS: Address, Town, County, Country, Postcode, Telephone (dial code + number), Mobile (dial code + number), Email (placeholder "email@domain.com"), Contact Preference (Telephone / Mobile / Email). OCCUPATION AND INDUSTRY: Occupation or profession, Industry (dropdown), Upload photograph ("Jpeg or png format only. Max file size 10MB"). Button "Continue". — [Surrenne application](https://apply.surrenne.com/wellbeing)
- Styling: small sentence-case label ABOVE each field with a red asterisk before the label; underline-only inputs (1px black bottom), transparent on a warm stone background, 51px tall, 17px Suisse Intl; outlined navy pill button (radius 50px, 14px uppercase, 47px). Dropdown placeholder "Select an answer". — [Surrenne application](https://apply.surrenne.com/wellbeing)
- Helper copy under fields: "Please ensure that you have not used this email address for any previous applications." — [Surrenne application](https://apply.surrenne.com/wellbeing)

**E. Maison Estelle (London) – custom 4-step application with payment** (`forms-maisonestelle-apply.png`)
- Own page; thin progress bar at the very top plus "Step 1 of 4" text top right; watercolour illustration beside the form. Intro: "To apply for a membership at Maison Estelle, please fill out your details below. Please note that we do not accept membership applications through any social media accounts or third parties." — [Maison Estelle application](https://maisonestelle.com/245-application/)
- Step 1 "Please select your membership": Annual / Patron tabs, then large outlined radio cards (Single £4,250 p.a. + £2,250 joining; Joint; U30), "All prices are inclusive of VAT". — [Maison Estelle application](https://maisonestelle.com/245-application/)
- Step 2 "Your Details": headshot upload ("We like to put a face to your name. Please upload a recent headshot of yourself."), First Name *, Last Name *, Gender *, Email *, Nationality (optional), Country code *, Mobile number *, Address *, City *, Country *, Postcode *, Date of birth (DD/MM/YYYY); "Your Work": Company *, Industry *; "Your Bio": textarea "Please provide a short bio about yourself *" with a 0/500 counter; "Proposer(s) Details": "Do you know anyone in the Maison Estelle community? Please provide the full names and email addresses of two proposers." (Proposer Name * / Proposer Email * twice). — [Maison Estelle application](https://maisonestelle.com/245-application/)
- Step 3 "Staying Connected and Our Policies": "I've read, understood and accepted Maison Estelle's Small Print and Privacy Policy"; "I would like to stay connected and hear about members events, upcoming parties and weekend trips." — [Maison Estelle application](https://maisonestelle.com/245-application/)
- Step 4 "Payment Details": Name On Card, Card Number, Expiry, CVV (Stripe Elements iframes), Billing Address "Same as personal address". Buttons are lowercase, widely letter-spaced, near-black rectangles: "next", "back", "review & submit". — [Maison Estelle application](https://maisonestelle.com/245-application/)

**F. The Ned (Ned's Club London) – 7-step application with numbered stepper** (`forms-thened-apply.png`)
- "Apply" on the club page goes to membership.thened.com, a separate app. Seven-stage numbered stepper (circles 01 to 07): Contact Details, Your photo, Occupation, Proposers, You and The Ned, Payment, Submit. — [Ned's Club application](https://membership.thened.com/en/ned)
- Step 1 fields: First name, Last name, Gender (Pick one: Male / Female / Non binary / Prefer not to say / Other), Date of Birth (Day / Month / Year selects), Address line 1, Address line 2, Town / City, Postcode, Country, Telephone, Email Address, Re-Enter Email Address, Device type (Iphone / Android). Button "CONTINUE". — [Ned's Club application](https://membership.thened.com/en/ned)
- Styling: dark racing-green page, white text; centred small labels above underline-only inputs (1px, 40% white), 38px tall; white button with green uppercase letter-spaced text. Native grey OS dropdowns clash visibly with the rest. — [Ned's Club application](https://membership.thened.com/en/ned)

**G. Soho House – account creation before application** (`forms-sohohouse-apply.png`)
- "Apply for membership / Start application" (sohohouse.com/apply?type=HOUSE) redirects to an account-creation screen headed "Get started": First name*, Last name*, Email*, Create password*, Re-enter password*. The application itself sits behind this login and was not viewed. — [Soho House apply](https://www.sohohouse.com/apply?type=HOUSE)
- Styling: black page, large white serif heading; fields are a single stacked, bordered group (one white 1px outline, hairline dividers between rows, radius ~4px) with the label inside each row; 18px grotesque. Consent line in small grey: "By signing up, you agree to the Soho House privacy policy and terms and conditions. You can change the way we contact you or unsubscribe at any time." plus a toggle switch (not a tick-box) for "I would like to receive updates, events and news and benefits from Soho House & Co." — [Soho House apply](https://www.sohohouse.com/apply?type=HOUSE)

**H. Casa Cipriani (New York) – Peoplevine, identity gate first** (`forms-casacipriani-apply.png`)
- Tier chooser page (e.g. NY Individual: $3,900 annual + $2,000 initiation) with "APPLY" per tier; footer "Powered by PeopleVine". — [Casa Cipriani application](https://members.casacipriani.com/application)
- First screen "BEFORE YOU APPLY": only "Your E-mail Address" and "Your Mobile Number", button "Verify & Continue"; copy: "Please enter your unique e-mail address and mobile number to continue." Boxed white inputs, 1px grey border, 50px tall; outlined square button. Later steps not viewed. — [Casa Cipriani step 1](https://members.casacipriani.com/membership/1118/2888)

**I. Zero Bond (New York) – Peoplevine, "before we start" declaration screen** (`forms-zerobond-apply.png`)
- Tier cards with "START APPLICATION"; first screen has no fields, only a "BEFORE WE START" statement and a gold outlined "Continue" button. Key lines: "All information shall be treated in confidence."; "A clear and recent headshot must be included."; "A letter of recommendation from a current member is highly encouraged."; "Your provided billing details will not be charged until your membership application has been reviewed and accepted by our Membership Committee."; "This form will take around ten minutes to complete." Fields beyond this screen not viewed. — [Zero Bond application](https://apply.zerobondny.com/membership/1011/8640)

**J. The Conduit (London) – Peoplevine application plus HubSpot "talk to us" menu** (`forms-conduit-apply.png`, `forms-conduit-enquiry.png`)
- Application intro (no fields, red "Continue" button): "Membership openings are limited each month. Applications are reviewed with care, and successful applicants are typically notified within 14 days." — [Conduit apply](https://apply.uk.theconduit.com/join)
- Separate "Find Out More" page offers four routes instead of an enquiry form: Book a Membership Experience Day (£10), Book an Open Evening (£10), Book an In-person Meeting, Book a Call; the last two link to HubSpot Meetings scheduling pages for named team members ("Available from 8am-7pm, Monday to Friday"). — [Conduit find out more](https://hubspot.theconduit.com/find-out-more)

**K. Chief (US, women leaders) – 3-step application, 6 fields on step one** (`forms-chief-apply.png`)
- Landing page sets expectations before the form: "Complete online in 2 minutes or less."; "you'll hear from us within a few business days to schedule a 30-minute interview." — [Chief apply](https://chief.com/apply)
- Form page: "STEP 1 OF 3 – Tell us a little bit about you:" First Name*, Last Name*, Email*, Mobile Phone*, Postal Code*, LinkedIn Profile URL*. Visible labels above boxed white inputs (1px 20%-opacity border, radius 4px, 42px, 18px); dark green pill button "NEXT". Consent by action, no tick-box: "By hitting "Next" you are agreeing to receive marketing communications from Chief. You may opt-out at any time." — [Chief application form](https://chief.com/apply/application-form)

**L. THE WELL (Bay Harbor Islands) – Typeform "Membership Invitation Request"** (`forms-thewell-typeform.png`)
- Linked from the contact page as "Membership Interest Form"; a hosted Typeform, one question group per screen, proportional progress bar enabled. Welcome screen: "Membership Invitation Request – Thanks for your interest in Membership at THE WELL Bay Harbor Islands. This form registers your interest in receiving an invitation to join our community." Button "Get Started". — [THE WELL Typeform](https://the-well.typeform.com/to/xym3GHkW)
- Questions in order (from the form's public Typeform definition): Contact Information (First name*, Last name*, Phone number*, Email*); "What is your address?" (all optional); "[First name], have you been referred by someone? If so, please provide their full name:" (optional); "How did you find out about THE WELL if not referred?" (optional); "Tell us more about yourself. We want to understand why you're interested in joining THE WELL and what you're looking for in this community." (required long text); "Feel free to share any of your social media links here so we can get to know you better." (optional); consent as a required single choice "I agree" to "By submitting this form, you are agreeing to our Terms of Service". Thank-you screen: "Thank you for your interest, [First name]." — [Typeform form definition](https://api.typeform.com/forms/xym3GHkW)

**M. House 120, New York (continuum.club now redirects here) – single long page application** (`forms-house120-apply.png`)
- continuum.club redirected to house120.com on the day of research; the site describes itself as "New York's first longevity lifestyle members club". Form is WPForms, inline on "/apply/". — [House 120 apply](https://house120.com/apply/)
- Fields: Name* (First / Last), E-mail*, Phone, Address (street, city, state, ZIP), Personal Links ("LinkedIn, Instagram, Website, Media"), "WERE YOU REFERRED BY A CURRENT MEMBER?" Yes / No ("A member referral is not required to apply."), "WHY ARE YOU INTERESTED IN JOINING HOUSE 120?" (3 tick-boxes), "PLEASE CHECK THE SERVICES YOU ARE INTERESTED IN:" (12 tick-boxes), "ARE YOU INTERESTED IN JOINING AS" Individual / Family / Couple, "WHAT IS YOUR DESIRED TIMEFRAME TO JOIN?" ASAP / 0-3M / 3-6M / 6M+, "DO YOU PREFER STILL OR SPARKLING WATER?", "COFFEE OR TEA?" (Coffee / Tea / Neither), "DO YOU BELONG TO ANY PRIVATE MEMBER CLUBS? IF SO, PLEASE LIST WHICH ONES." — [House 120 apply](https://house120.com/apply/)
- Styling: dark page, warm off-white text, underline-only inputs (1px, 25% opacity taupe), 43px, uppercase letter-spaced question labels; bronze solid rectangle button (rgb 139,106,67) "APPLY FOR MEMBERSHIP". Reassurance: "If you have any questions about membership please reach out to [named person's email]". — [House 120 apply](https://house120.com/apply/)

**N. The Quorum (Mumbai / Gurugram / Hyderabad) – Indian club, long single-step form** (`forms-quorum-join.png`)
- "/join-the-q/" opens with the line "We are private, but the best things are, aren't they?", an accordion of membership types (Standard, Under 35, Under 30, Woman Only, Corporate, Outstation, Expatriate), then the form; reCAPTCHA invisible. — [The Quorum join](https://thequorumclub.com/join-the-q/)
- Fields (placeholder-only, uppercase): First NAME*, Last NAME*, EMAIL*, PHONE NUMBER* (plain text field, no dial-code picker), AGE*, INDUSTRY*, COMPANY, WHERE DO YOU LIVE*, PLACE OF WORK*, Preferred club location* (Mumbai / Gurugram / Hyderabad), HOW DID YOU HEAR ABOUT US* (Social Media / Publication / Friend or Colleague / Other), PREFERRED SOCIAL MEDIA (LinkedIn / Facebook / Instagram), LINK TO PROFILE, REFERENCE 1, REFERENCE 2, a tick-box, textarea "Something we should know about you", button "SUBMIT". — [The Quorum join](https://thequorumclub.com/join-the-q/)
- Styling: cream page, dark green serif (Ibarra Real Nova) 18px, underline-only inputs (1px dark green), 43px. — [The Quorum join](https://thequorumclub.com/join-the-q/)

**O. Third Space (London) – HubSpot callback form in a slide-in "Join us" panel** (`forms-thirdspace-join.png`)
- "JOIN US / BECOME A MEMBER" opens a modal panel; HubSpot form. Fields: Name*, Email*, Phone Number*, Club* (dropdown), "Which other club are you interested in training at?", tick-box "Are you interested in Personal Training?", tick-box "I agree to receive communications from Third Space." Button: white pill "Send". Copy beside it: "Don't want to wait for a call back? Book a tour directly with one of our team." Dark panel, underline-only inputs (1px, 40% white), ~37px. — [Third Space membership](https://www.thirdspace.london/membership/)

**P. SHA Wellness – 2-step HubSpot contact form with WhatsApp alongside** (`forms-sha-contact.png`)
- Step "1/2": First Name*, Last Name*, Email*, Phone Number* (flag dial-code picker, showed the India flag for our IP), button "Next". Consent tick-boxes: "I would like to join the SHA community and receive communications about health and longevity."; "I confirm that I have read and accept the Privacy Policy.*". Boxed white inputs, radius 4px, 42px, visible labels. Site-wide "Contact via WhatsApp" button with wa.me links and a HubSpot live chat. — [SHA contact](https://shawellness.com/en/contact-us/)

**Q. No-form, human-first patterns**
- Aman: the contact page has no enquiry form at all; it lists a reservations email, direct-dial numbers, and "Contact us via WhatsApp" with a wa.me link, stating the team operates "24 hours a day, 7 days a week". — [Aman contact](https://www.aman.com/contact-us)
- Surrenne "Make an Enquiry" and Zero Bond lifetime membership are plain mailto links; KX lists a phone number ("please contact the club on 020 7584 5333") above its Peoplevine tier list. — [Surrenne apply](https://www.surrenne.com/en/apply); [Zero Bond](https://zerobondny.com/apply-for-membership/); [KX apply](https://apply.kxlife.club/our-memberships)
- Maison Estelle's house rules state members can "ring, email or message us via WhatsApp - your direct link to your Maison Estelle team". — [Maison Estelle manifesto](https://245.maisonestelle.com/)
- Remedy Place has no application: "You never need a membership to come to Remedy… Only two hundred members per club.", tiers with a "GET STARTED" button, and an email-only "SIGN UP" list field. — [Remedy Place membership](https://www.remedyplace.com/book/membership)

### Inferences
- Peoplevine is the default back-end for application-style clubs (Six Senses Place, Surrenne, KX, Casa Cipriani, Zero Bond, The Conduit all resolve to Peoplevine-pattern portals). These need a staff login to review applicants, so they are unsuitable for a founder who must not log in to anything.
- Geo-IP defaulting of the dial code (Saint Haven, SHA) shows +91 pre-selection is easy to get "for free" from standard phone-input widgets.
- The clubs that feel most personal put a named human or a direct channel beside the form (House 120 named email, Surrenne named mailto, Conduit named meeting links).

### Gaps
- Not seen live: Heimat (application host returned an "Access denied" block), Ananda in the Himalayas (bot-verification wall; not bypassed), Jolie's (jolies.in failed to load; correct URL not established), Soho House Mumbai (not checked separately from the global Soho House flow), Lanserhof at The Arts Club (page only exposed a "Contact us" control; its form was not opened), The Twenty Two (no membership form found on the members-club page), AllBright (now redirects to allbrighteverywoman.com; its Pardot iframe form was not inspected), Aman Club (URL redirected to aman.com home).
- Steps beyond the first were deliberately not viewed for Soho House, The Ned, Casa Cipriani, Zero Bond, The Conduit, Chief, Surrenne, SHA and Six Senses (would require entering data). KX per-tier form not opened.
- Error-state visuals were not triggered anywhere (would require submitting). Only Saint Haven's success and error text was readable from the DOM. THE WELL Typeform's visual theme beyond the welcome screen was not viewed.
- Required flags on Six Senses enquiry, Quorum's tick-box wording, and Third Space's panel animation (modal vs slide-over) could not be confirmed.

## 2. Taxonomy of form types, with pros and cons for a small club

### Takeaway
Seven types cover everything seen. For a tiny circle, only the short enquiry, the conversational request, and the human-first (WhatsApp / call) types are proportionate; multi-step vetted applications signal scale and bureaucracy the circle does not have.

### Cited Findings
- Type 1, short "register interest" enquiry (4 to 8 fields, one screen, modal or inline): Saint Haven, Six Senses enquiry, Third Space. — [Saint Haven](https://sainthaven.com.au/); [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/); [Third Space](https://www.thirdspace.london/membership/)
- Type 2, conversational one-question-per-screen invitation request: THE WELL on Typeform, with name piping into later questions and the thank-you. — [THE WELL Typeform](https://the-well.typeform.com/to/xym3GHkW)
- Type 3, single long-page application with "get to know you" questions: House 120, The Quorum. — [House 120](https://house120.com/apply/); [The Quorum](https://thequorumclub.com/join-the-q/)
- Type 4, multi-step vetted application with headshot, proposers and card capture: Maison Estelle (4 steps), The Ned (7), Surrenne (2), Six Senses, Zero Bond, Casa Cipriani. — [Maison Estelle](https://maisonestelle.com/245-application/); [The Ned](https://membership.thened.com/en/ned)
- Type 5, account-first (create a login, then apply): Soho House. — [Soho House](https://www.sohohouse.com/apply?type=HOUSE)
- Type 6, concierge booking (pick a call, tour or open evening): The Conduit via HubSpot Meetings; Third Space's "Book a tour directly". — [Conduit find out more](https://hubspot.theconduit.com/find-out-more)
- Type 7, no form: WhatsApp, phone or named email: Aman, Surrenne enquiry, KX, SHA's WhatsApp button. — [Aman contact](https://www.aman.com/contact-us); [SHA contact](https://shawellness.com/en/contact-us/)
- Email-only waitlist appears only as a secondary list (Remedy Place "SIGN UP", Chief "Subscribe"), never as the membership route. — [Remedy Place](https://www.remedyplace.com/book/membership); [Chief apply](https://chief.com/apply)
- No gated PDF brochure request was found on any membership page examined. — [Six Senses Place join](https://www.sixsensesplace.com/join-us/); [Surrenne apply](https://www.surrenne.com/en/apply)

### Inferences
- Type 1 pros: fastest, works with FormSubmit to an inbox, no login. Cons: little signal about the person unless one good open question is included.
- Type 2 pros: feels like a conversation, suits warm questions. Cons: needs a third-party tool whose responses normally live in a dashboard (email notifications can cover this, but it is one more service); more taps on a phone.
- Type 3 pros: rich picture of the applicant. Cons: 15+ fields is heavy for a ₹10,000 membership.
- Type 4 and 5 cons: need staff systems, logins and review queues; overkill.
- Type 6 pros: very personal. Cons: needs a calendar tool the founder would have to maintain.
- Type 7 pros: matches how Indian customers already talk to small businesses and needs no tooling. Cons: no structured record, no consent capture unless wording is added.

### Gaps
- No conversion-rate data comparing these types for clubs was found; the pros and cons are reasoned, not measured.

## 3. Styling conventions that read as luxurious rather than transactional

### Takeaway
The recurring recipe is: underline-only inputs on a tinted or dark ground, generous height (roughly 43 to 52px), a serif sentence-case heading that speaks like a host, small uppercase letter-spaced labels or buttons, one restrained button, and scarcity or care copy in place of marketing copy.

### Cited Findings
- Underline-only inputs (no box, transparent fill, 1px bottom rule) are used by Saint Haven, Six Senses enquiry, Surrenne, The Ned, House 120, The Quorum and Third Space; boxed inputs appear on the more functional Peoplevine, Chief and SHA forms. — [Saint Haven](https://sainthaven.com.au/); [Surrenne](https://apply.surrenne.com/wellbeing); [Chief](https://chief.com/apply/application-form)
- Measured input heights: Saint Haven 52px, Surrenne 51px, Six Senses application 48px, House 120 and Quorum 43px, Chief 42px; input text 16 to 18px. — [Saint Haven](https://sainthaven.com.au/); [Surrenne](https://apply.surrenne.com/wellbeing); [The Quorum](https://thequorumclub.com/join-the-q/)
- Buttons are either a solid dark rectangle with wide-tracked uppercase text (Saint Haven, Maison Estelle in lowercase, House 120 in bronze) or a thin outlined pill (Six Senses, Surrenne); wording is specific ("Apply for Membership", "Continue", "review & submit") more often than "Submit". — [Saint Haven](https://sainthaven.com.au/); [Maison Estelle](https://maisonestelle.com/245-application/); [Surrenne](https://apply.surrenne.com/wellbeing)
- Host-voice headings and questions: "We welcome your interest…", "LET'S START FROM HERE", "WHAT ENCOURAGES YOU TO ENQUIRE?", "We like to put a face to your name.", "We are private, but the best things are, aren't they?", "COFFEE OR TEA?". — [Saint Haven](https://sainthaven.com.au/); [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/); [Maison Estelle](https://maisonestelle.com/245-application/); [The Quorum](https://thequorumclub.com/join-the-q/); [House 120](https://house120.com/apply/)
- Scarcity and care copy near the form: "Membership is limited…"; "Applications are reviewed with care, and successful applicants are typically notified within 14 days."; "All information shall be treated in confidence."; "Only two hundred members per club." — [Saint Haven](https://sainthaven.com.au/); [Conduit apply](https://apply.uk.theconduit.com/join); [Zero Bond](https://apply.zerobondny.com/membership/1011/8640); [Remedy Place](https://www.remedyplace.com/book/membership)
- Progress is shown quietly: text "Step 1 of 2" (Surrenne), "STEP 1 OF 3" (Chief), "1/2" (SHA), a hairline bar plus "Step 1 of 4" (Maison Estelle); only The Ned uses a heavy numbered stepper. — [Surrenne](https://apply.surrenne.com/wellbeing); [Chief](https://chief.com/apply/application-form); [Maison Estelle](https://maisonestelle.com/245-application/); [The Ned](https://membership.thened.com/en/ned)
- Counter-example: The Ned's unstyled grey native dropdowns sit awkwardly on the dark green page. — [The Ned](https://membership.thened.com/en/ned)

### Inferences
- Confirmation copy that promises something concrete (Conduit's 14 days, Chief's "few business days") is rarer than vague "we will be in touch"; a founder who replies personally can out-do the big clubs here with a specific promise.
- Unusual, human questions (still or sparkling, coffee or tea) do more for tone than any visual treatment.

### Gaps
- Focus, hover and error styling were not observed (no interaction with fields).

## 4. How many fields is too many, and accessibility

### Takeaway
Usability research says keep forms short, single column, with visible labels and explicit error text. The luxury sector's favourite pattern (placeholder-only labels on a hairline) directly contradicts the accessibility guidance, so the circle should copy the look of Surrenne or Six Senses enquiry (small label above an underline) rather than Saint Haven or Quorum.

### Cited Findings
- NN/g: "Keep it short"; remove any field whose data can be derived, collected later or dropped; single column, one field per row; keep optional fields to one or two and label them as optional; error messages must be highly visible and specific, not colour alone, and must keep the user's input. — [NN/g web form design](https://www.nngroup.com/articles/web-form-design/)
- NN/g on placeholders replacing labels: the hint disappears on typing (memory strain), users cannot review entries before submitting, errors are harder to fix, keyboard users lose the hint, and placeholder text can be mistaken for a pre-filled value. — [NN/g placeholders](https://www.nngroup.com/articles/form-design-placeholders/)
- Baymard: the average checkout had 11.3 form fields in 2024, while most sites need only 8; field count affects usability more than step count. — [Baymard](https://baymard.com/blog/checkout-flow-average-form-fields)
- Observed field counts: short enquiry forms carry 5 (Six Senses enquiry), 6 (Chief step 1), 7 (Third Space) or 8 (Saint Haven) inputs; application forms carry 20+ (Surrenne step 1 has 19 inputs plus upload; Six Senses step 1 about 24). — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/); [Saint Haven](https://sainthaven.com.au/); [Surrenne](https://apply.surrenne.com/wellbeing)
- Placeholder-only labelling was observed on Saint Haven, The Quorum, Maison Estelle and the Six Senses application; visible labels above fields on Surrenne, Six Senses enquiry, Chief, SHA, The Ned and House 120. — [Saint Haven](https://sainthaven.com.au/); [The Quorum](https://thequorumclub.com/join-the-q/); [Surrenne](https://apply.surrenne.com/wellbeing)
- Clubs set time expectations in words: "Complete online in 2 minutes or less." (Chief); "This form will take around ten minutes to complete." (Zero Bond). — [Chief apply](https://chief.com/apply); [Zero Bond](https://apply.zerobondny.com/membership/1011/8640)

### Inferences
- For a personal-reply circle, 4 to 6 fields is the proportionate ceiling for first contact; the existing form (name, email, optional WhatsApp, optional note, consent) is already within the range the best short forms use, so the redesign is about tone and styling, not adding fields.
- Light grey placeholder text on hairline inputs, and 40%-opacity rules on dark grounds, are likely to fail contrast guidance; a visible label and a darker rule keep the look and fix the problem.

### Gaps
- No club-specific or luxury-specific research on field count versus completion was found; the Baymard figure is from e-commerce checkouts and is an analogy only.
- Typeform and Tally's own design guidance was not consulted.

## 5. Indian conventions: WhatsApp, +91, and DPDP consent

### Takeaway
The one Indian club form seen (The Quorum) uses a plain phone field with no WhatsApp label; international luxury brands, by contrast, increasingly expose WhatsApp as a first-class contact channel. Under India's DPDP regime, consent must be specific to stated purposes with an easy withdrawal route, so a bundled "I agree" line should be replaced by a short itemised notice.

### Cited Findings
- The Quorum asks for "PHONE NUMBER*" as a plain text field with no dial-code selector and no WhatsApp wording, plus two "REFERENCE" fields and a social profile link. — [The Quorum join](https://thequorumclub.com/join-the-q/)
- Phone widgets on Saint Haven and SHA defaulted to the India flag / dial code for an Indian visitor. — [Saint Haven](https://sainthaven.com.au/); [SHA contact](https://shawellness.com/en/contact-us/)
- WhatsApp as a named channel: Aman ("Contact us via WhatsApp", wa.me link), SHA ("Contact via WhatsApp" button), Maison Estelle (member concierge via WhatsApp). — [Aman contact](https://www.aman.com/contact-us); [SHA contact](https://shawellness.com/en/contact-us/); [Maison Estelle manifesto](https://245.maisonestelle.com/)
- DPDP Rules 2025 were notified by MeitY in mid-November 2025 (sources give 13 or 14 November) and operationalise the DPDP Act 2023. — [SCC Online](https://www.scconline.com/blog/post/2025/12/26/digital-personal-data-protection-rules-2025-key-highlights/); [Mondaq](https://www.mondaq.com/india/data-protection/1708164/digital-personal-data-protection-rules-2025-notified)
- Practitioner commentary on Rule 3: the notice must itemise the personal data collected and the specific purposes; generic statements and blanket "I Agree" consents are not valid; the notice must give a direct means to withdraw consent, with withdrawal as easy as giving it. — [Tsaaro](https://tsaaro.com/blogs/ensuring-informed-consent-a-deep-dive-into-consent-notice-requirements-under-the-dpdpa-and-draft-dpdp-rules-2025); [GoTrust](https://www.gotrust.tech/blog/dpdpa-consent-management-how-to-collect-store-and-withdraw-user-consent-legally); [dpdpa.com Rule 3](https://dpdpa.com/dpdparules/rule3.html)
- Separating marketing opt-in from privacy acceptance into two tick-boxes is already the pattern at Six Senses, SHA and Maison Estelle; Saint Haven and Chief bundle them. — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/); [SHA contact](https://shawellness.com/en/contact-us/); [Saint Haven](https://sainthaven.com.au/); [Chief](https://chief.com/apply/application-form)

### Inferences
- A suitable field for the circle: label "WhatsApp number (optional)", fixed "+91" prefix shown as text before a 10-digit numeric input, with helper text saying what it will be used for.
- A DPDP-style consent line would name the data (name, email, WhatsApp number, note), the purpose (to reply about membership), and how to withdraw (reply to the email or message the same number), with a separate unticked box for event news.

### Gaps
- The official gazette text of Rule 3 was not read; the points above are secondary commentary and the commencement date of the notice obligations is reported inconsistently (one source says May 2027). Legal confirmation is needed before final wording.
- No Indian wellness-club form with an explicit WhatsApp field or DPDP-worded consent was seen live (Jolie's, Soho House Mumbai and Ananda were not reached).

## 6. Recommendation for a tiny founder-run circle (Razorpay link, personal reply, no logins)

### Takeaway
Use Type 1 as the core (a short "request an invitation" form, restyled, still posting to the founder's inbox), pair it with Type 7 (a WhatsApp button as an equal alternative), and borrow the Type 2 conversational tone inside the single form. Keep payment separate and after the personal reply, as the big clubs do.

### Cited Findings
- Model for layout and copy: Saint Haven's modal (welcome heading, scarcity line, one open question "What interests you most about joining…?", "Referred By", single button, in-place confirmation). — [Saint Haven](https://sainthaven.com.au/)
- Model for accessible luxury styling: Six Senses enquiry and Surrenne (small label above an underline-only field; outlined pill or solid button). — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/); [Surrenne](https://apply.surrenne.com/wellbeing)
- Model for the open question: Six Senses "WHAT ENCOURAGES YOU TO ENQUIRE?"; THE WELL "Tell us more about yourself… what you're looking for in this community." — [Six Senses Place enquiry](https://www.sixsensesplace.com/enquiry/); [THE WELL Typeform](https://the-well.typeform.com/to/xym3GHkW)
- Model for a concrete promise after submit: The Conduit ("typically notified within 14 days"), Chief ("within a few business days"). — [Conduit apply](https://apply.uk.theconduit.com/join); [Chief apply](https://chief.com/apply)
- Model for payment timing: Zero Bond states billing details "will not be charged until your membership application has been reviewed and accepted"; Six Senses, Surrenne and Maison Estelle show the price before the form. — [Zero Bond](https://apply.zerobondny.com/membership/1011/8640); [Surrenne](https://apply.surrenne.com/wellbeing); [Maison Estelle](https://maisonestelle.com/245-application/)
- Model for the human alternative: Aman's WhatsApp link; House 120's named contact under the form. — [Aman contact](https://www.aman.com/contact-us); [House 120](https://house120.com/apply/)

### Inferences
- Suggested field set (5 inputs + consent): Your name (required); Email (required); WhatsApp number, +91 prefix (optional); "What brings you to the circle?" textarea (optional); "Who told you about us?" (optional, replaces formal proposers); itemised consent tick-box (required) and a separate unticked "send me event news" box.
- Suggested flow: form submit, then an in-place thank-you naming the founder and a reply time she can keep, then her personal reply carrying the Razorpay link. The price (₹10,000 for six months) should be visible near the form so nobody is surprised.
- Avoid: account creation, headshot upload, proposers with emails, card capture in the form, multi-step steppers, any tool whose responses must be read in a dashboard.
- A Typeform or Tally version is viable only if email notifications fully replace the dashboard; otherwise the existing FormSubmit route better fits the no-login rule.

### Gaps
- Whether the circle's membership is selective (apply and be accepted) or open (enquire and pay) is not known from this research and changes the button wording ("Request an invitation" vs "Join").
- FormSubmit's ability to render a custom in-place success state and an auto-reply to the enquirer was not checked here.
