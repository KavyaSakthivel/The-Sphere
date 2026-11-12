# Typography of luxury wellness clubs and private members' clubs (observed 11 Nov 2026) and typefaces a small club can actually use

Evidence labels used throughout:
- **[CS]** = verified by me from the live page with `getComputedStyle`, `document.fonts` and `@font-face` sources (agent-browser, 1440x900 desktop viewport, 11 Nov 2026).
- **[3P]** = reported by a third party (source linked).
- **[ID]** = my identification: the family/file name is verified, but the foundry or "real typeface behind the file" is from my own knowledge of the type market and was not re-verified this session.
- **[RT]** = my own render test (font loaded from the Google Fonts / Fontshare API into a browser canvas and checked for a real U+20B9 glyph and numeral features; method in section 4).

Screenshots saved (all prefixed `type-`) in `/Users/skybridge/Desktop/Sphere/research_notes/Luxury wellness club membership pages/screenshots/`: type-aman-wellness.png, type-thewell-home.png, type-surrenne-membership.png, type-remedyplace-home.png, type-chief-membership.png, type-sohohouse-membership.png, type-thened-membership.png, type-maisonestelle-home.png, type-thirdspace-membership.png, type-thetwentytwo-404.png, type-lanserhof-home.png, type-house120-home.png, type-sainthaven-home.png, type-sha-home.png.

---

## 1. Which typefaces each top club's website really uses

### Takeaway
Of 20 sites verified from computed styles, 16 pair a serif display face with a sans for labels/navigation, 4 are sans-only, and none loads a script or monospace face. Almost every club uses paid retail faces (Commercial Type, Klim, Grilli Type, Swiss Typefaces, Hoefler&Co, Monotype); the one exception is Soho House, which runs entirely on two free OFL families (Cardo + HK Grotesk).

### Cited Findings

Table: all rows [CS] unless marked. px values are computed at 1440px width. "ls" = letter-spacing. Foundry column is [ID] unless a source is given.

| Club (URL inspected) | Headlines | Body | Nav / labels / buttons | Real typeface and foundry |
|---|---|---|---|---|
| Aman — [aman.com](https://www.aman.com/) and [aman.com/wellness](https://www.aman.com/wellness) | `Lyon Text Web` 400, 31px/45px, sentence case, ls 0.5px | `Lyon Display Web` (file LyonDisplay-Light-Web) 14px/20.3px, ls 0.8px | `WhitneySSm` 400; labels 10.1px uppercase ls 2px (0.2em); nav 13-14px sentence case ls 0.3-0.7px | Lyon Text / Lyon Display (Commercial Type; site also declares custom-named files `LyonText-Aman-*.woff`) + Whitney ScreenSmart (Hoefler&Co). Third-party confirmation of Lyon (Commercial Type) + Whitney (Hoefler&Co): [shadcn.io design page](https://www.shadcn.io/design/aman/raw) [3P]. Declared but not loaded on these pages: Calligraph810, Beausite Slick, Suisse BP, Janu Sans, Source Code Pro, Noto Serif JP/SC |
| THE WELL — [the-well.com](https://www.the-well.com/) (`/membership` redirected to home) | `Chronicle Display` weight 200 (file ChronicleDisp-XLight), 80px/80px h1, 36-48px h2, Title Case, ls normal; italic used on single words | `Styrene B` 300, 18px/27px and 14px/21px | `Styrene B` 400, 12px uppercase ls 1.2px (0.1em); buttons 14px uppercase ls 1.4px | Chronicle Display (Hoefler&Co) + Styrene B (Commercial Type) |
| Remedy Place — [remedyplace.com](https://www.remedyplace.com/) | `Beausite Slick` 300, 60px/66px h1, 43-52px h2, sentence case, ls 0.01em | `Beausite Classic` 400, 19px/30.4px; 14px/23.8px | `Beausite Classic` 11px uppercase, 400-500, ls 2.2-2.4px (0.2-0.22em) | Beausite Slick + Beausite Classic (Fatype). Sans only: Slick is the high-contrast sans cut used as "display" |
| Continuum Club — continuum.club now redirects to [house120.com](https://house120.com/) ("House 120") | `sweet-sans-pro` 200/400, 32-40px UPPERCASE ls 0.6-0.96px | `sweet-sans-pro` 16px/24px; pull-quote in `nocturne-serif-lights` 23px/33.6px | `sweet-sans-pro` 12px uppercase ls 0.24px | Sweet Sans Pro (MVB Fonts) + Nocturne Serif (Capitalics), both served via Adobe Fonts (`use.typekit.net/yke5jhu.css`) |
| Surrenne — [surrenne.com/en](https://www.surrenne.com/en), [/en/membership](https://www.surrenne.com/en/membership) | `Tiempos Fine` (file TiemposFine-Light, declared 400): 42px sentence case; hero titles 86px/86px UPPERCASE | `Suisse Intl` 300/400, 16px/24px | `Suisse Intl` 14-16px uppercase ls 1.4-1.6px (0.1em) | Tiempos Fine (Klim Type Foundry — "modern serif family for editorial typography", for headline sizes: [klim.co.nz](https://klim.co.nz/retail-fonts/tiempos-fine/)) + Suisse Int'l (Swiss Typefaces). `Commuters Sans` (Dharma Type) is the body default; other Maybourne brand fonts are declared (Romie, Sang Bleu, Neutraface, Felix Titling) |
| Lanserhof — [lanserhof.com/en](https://lanserhof.com/en) | Hero is `Frutiger Serif LT Pro` Light Italic 60px ls 3.87px ("Home of") over caps sans ("HEALTH & BEAUTY") | `Neue Frutiger World` 300, 16px/24px, ls 0.2px | `Neue Frutiger World` 500, 14px uppercase ls 1.12px (0.08em) | Neue Frutiger World + Frutiger Serif (Linotype / Monotype) |
| Six Senses — [sixsenses.com/en](https://www.sixsenses.com/en/) | not measurable | not measurable | not measurable | Page returned "Access Denied" (bot protection). Only font file requests seen: `Canto-Roman.woff2`, `AvenirNext-Regular.woff2`, `AvenirNextCondensed-Medium.woff2` — i.e. Canto serif + Avenir Next. Partial evidence only |
| Saint Haven (Melbourne club) — [sainthaven.com.au](https://sainthaven.com.au/) | `ivypresto-display` 300, 56px/61.6px UPPERCASE ls 6px (0.107em) | `Gt America Standard` 400 16px | `Gt America Extended` 300, 18px uppercase ls 1.8px (0.1em); `Gt America Expanded` 500 | IvyPresto Display (Ivy Foundry, via Adobe Fonts kit) + GT America (Grilli Type) |
| (bonus, unrelated brand) Saint Haven softwear — [sainthaven.com](https://sainthaven.com/) | `Canela-Light-Web` 300, 30-40px, ls 1-2px | `Santral-Book` 14-18px, 300 | `Santral` 12-13px uppercase 500 ls 1.5px | Canela (Commercial Type) + Santral (Taner Ardali). Not the club; kept only as a live example of the Canela look |
| Heimat — [heimat.com](https://heimat.com/) | `Suisse Works RegularItalic` 40-45px UPPERCASE italic, ls 1.5-3px; also `GT America Extended` 40px | `GT America Extended Regular` 20-24px, ls 1.5px, line-height 1.3-1.8 | `GT America Medium` 16px uppercase ls 2px | Suisse Works (Swiss Typefaces) + GT America (Grilli Type) |
| Third Space — [thirdspace.london](https://www.thirdspace.london/), [/membership/](https://www.thirdspace.london/membership/) | `GTSectra` 300 (file GTSectraFine-Book), 50-66px, sentence case; italic on single words | `Circular` 300, 17.5px/26px | `Circular` 700, 12-14px uppercase ls 0.9-1.2px | GT Sectra Fine (Grilli Type; family details: [grillitype.com](https://www.grillitype.com/typeface/gt-sectra)) + Circular (Lineto) |
| KX — [kxlife.co.uk](https://www.kxlife.co.uk/) | `Bicyclette-Bold` 77px UPPERCASE | mix: `Bicyclette-Bold` 12-16px and `GaramondPremrPro` 16px/24px | `Bicyclette-Bold` 14px uppercase ls 1.2px; `GaramondPremrPro` 13px uppercase | Bicyclette (Kostic) + Garamond Premier Pro (Adobe) |
| Bamford — [bamford.com/us](https://www.bamford.com/us/) | `trade-gothic-next` weight 100 (file TradeGothic-Light) 18-36px UPPERCASE ls 1px | same, 16-18px, ls 0.5px | same, 14px uppercase ls 3px (0.21em) | Trade Gothic Next (Linotype / Monotype). Sans only |
| Soho House — [sohohouse.com/en-us](https://www.sohohouse.com/en-us/), [/membership](https://www.sohohouse.com/en-us/membership) | `Cardo` 400, 56px/70px h1, 48px/60px h2, sentence case, no tracking | `HK Grotesk` 400/500, 16-18px | `HK Grotesk` 18px sentence-case nav; 14px bold buttons; no uppercase, no tracking | Cardo (David J. Perry, SIL OFL) + HK Grotesk (Hanken Design Co., SIL OFL), both self-hosted on Soho House's own CDN (`d34if7rq73m6wx.cloudfront.net`) — the only all-free stack in the set |
| The Ned — [thened.com](https://www.thened.com/), [/london/membership](https://www.thened.com/london/membership) | `Plantin` 52.5px/63px UPPERCASE ls 5.25px (0.1em) with lowercase italic connector words ("to", "in", "of") | `Plantin` 16-24px, line-height about 1.2-1.38 | `GillSans` (GillSansMTStd-Medium) 12.6-16px uppercase ls 1.9-2.4px (0.15em) | Plantin MT Pro + Gill Sans MT (Monotype) |
| Casa Cipriani — [casacipriani.com](https://www.casacipriani.com/) | `futura-pt` 18-22px UPPERCASE ls 2-4px | `futura-pt` 18px/27px | `futura-pt` 16-17px uppercase ls 1px | Futura PT (ParaType via Adobe Fonts) plus self-hosted Futura Std files. Sans only |
| Maison Estelle — [maisonestelle.com](https://maisonestelle.com/) | `Fleischman` (FleischmanBTW01-Regular) 40.5px | `DTL Fleischmann D Regular` 18px/28px, centred, italics for names | `DTL Fleischmann SD` 10.8px uppercase ls 3.6px (0.33em); `akzidenz-grotesk` 10px uppercase ls 2.7px on utility buttons | DTL Fleischmann (Dutch Type Library; also a Bitstream "Fleischman BT" web cut) + Akzidenz-Grotesk (Berthold). Essentially serif-only |
| The Twenty Two — the22.london redirects to [thetwentytwo.com](https://www.thetwentytwo.com/) | `Ayer Poster` Medium 48px/43px (96px on the 404 page), italic on single words | `Dia Regular` 16px | `Dia Regular` 15-16px, some uppercase | Ayer Poster (Commercial Type) + Dia (Schick Toikka: four weights with italics, [schick-toikka.com/dia](https://www.schick-toikka.com/dia)) |
| AllBright — allbrightcollective.com redirects to [allbrighteverywoman.com/hub](https://allbrighteverywoman.com/hub/) | `IvyPresto Display` 300 (files Ivy-Presto-Headline-Light / Display-Light), 24-64px | `DM Sans` 16px/24px | `DM Sans` 500-700, 12-17px | IvyPresto (Ivy Foundry) + DM Sans (Google Fonts, OFL); Big Caslon and EB Garamond also declared |
| Chief — [chief.com](https://chief.com/), [/membership](https://chief.com/membership) | `Romie` 500, 64px/76px h1, 40px/48px h2, sentence case, ls -0.16px; italic for emphasis | `NeueHaasGrotesk` 400, 16px/24px and 20px/28px | `NeueHaasGrotesk` 500, 12px uppercase ls 0.17px; nav 15px sentence case | Romie (Margot Lévêque) + Neue Haas Grotesk Text (Linotype / Monotype) |
| SHA Wellness — [shawellness.com/en](https://shawellness.com/en/) | `Graphik` 300, 48px/56px UPPERCASE; bold italic for emphasis | `Graphik` 300, 16px/24px | `Graphik` 400, 14px uppercase ls 1.4px (0.1em) | Graphik (Commercial Type). Sans only |
| Chenot — chenotpalaceweggis.com redirects to [chenot.com/chenot-palace/weggis](https://www.chenot.com/chenot-palace/weggis/) | `Brandon Grotesque` 400, 28-38px UPPERCASE ls 0.06em; accent words in `Portrait` italic 34px | `Verlag` 300, 16-20.8px, line-height 1.46 | `Verlag` 700 12px uppercase ls 1.2px; `Brandon Grotesque` 12-14px uppercase ls 0.1em | Brandon Grotesque (HVD Fonts) + Verlag (Hoefler&Co) + Portrait (Commercial Type) |
| Ananda in the Himalayas — [anandaspa.com](https://www.anandaspa.com/) | — | — | — | Not inspected: site served a Cloudflare "Performing security verification" challenge, which I did not attempt to pass |

- Canela is a Commercial Type display family by Miguel Reyes that "began as an interpretation of Caslon" with flared stroke ends instead of serifs; families Canela, Condensed, Deck and Text, each with italics — [Commercial Type](https://commercialtype.com/catalog/canela)
- Tiempos Fine is by Kris Sowersby and Noe Blanco (2018), 6 weights with italics, variable font supplied with the full family — [Klim](https://klim.co.nz/retail-fonts/tiempos-fine/)
- GT Sectra (2013; Dominik Huber, Marc Kappeler, Noël Leu) comes as Sectra, Sectra Fine and Sectra Display; free trial fonts are offered — [Grilli Type](https://www.grillitype.com/typeface/gt-sectra)

### Inferences
- The dominant recipe is "light-weight contemporary serif for headlines + neutral grotesque for 11-14px tracked uppercase labels". Serif choices cluster in three groups: sharp transitional/"modern" serifs (Lyon, Tiempos Fine, Chronicle Display, GT Sectra Fine, Plantin), soft/flared display serifs (Canela, Romie, IvyPresto) and condensed editorial serifs (Ayer Poster).
- Medical/longevity-led brands skew sans-only (Remedy Place, SHA, Bamford, House 120 mostly, Lanserhof mostly); social/hospitality-led clubs skew serif-led (Aman, Soho House, The Ned, Maison Estelle, Chief, The Twenty Two). A women's circle sits with the second group.
- Soho House proves a top-tier club can look credible on two free OFL fonts; the craft is in sizing, spacing and restraint rather than the licence fee.

### Gaps
- Six Senses and Ananda could not be measured (bot protection); Six Senses' Canto + Avenir Next is inferred from font file requests only.
- No agency case study was found confirming who specified these faces (searches for Surrenne/Pentagram etc. returned nothing relevant); Fonts In Use had no entries surfaced for these clubs.
- Foundry attributions marked [ID] were not individually re-verified against foundry sites, apart from Canela, Tiempos Fine, GT Sectra and Dia.
- Measurements are desktop (1440px) only; mobile computed sizes were not captured.

---

## 2. Typographic styling conventions

### Takeaway
Luxury clubs set headlines large but light (weights 200-400, 40-86px, line-height 1.0-1.25), keep body small (14-19px, line-height 1.45-1.6), and put all navigation/labels in 10-14px uppercase sans with 0.1-0.2em tracking. Italic serif on one or two words is the standard emphasis device (10 of 20 sites); scripts and monospace are absent.

### Cited Findings
All [CS], 11 Nov 2026.

**Headline size relative to body**
- THE WELL: h1 80px vs body 18px (4.4x); h2 36-48px — [the-well.com](https://www.the-well.com/)
- Surrenne: hero title 86px caps vs body 16px (5.4x); secondary heading 42px (2.6x) — [surrenne.com/en/membership](https://www.surrenne.com/en/membership)
- Chief: h1 64px vs body 16-20px (3.2-4x); h2 40px — [chief.com/membership](https://chief.com/membership)
- Remedy Place: h1 60px vs body 19px (3.2x) — [remedyplace.com](https://www.remedyplace.com/)
- Soho House: h1 56px, h2 48px vs body 16-18px (about 3.1-3.5x) — [sohohouse.com/en-us/membership](https://www.sohohouse.com/en-us/membership)
- Third Space: 50-66px vs body 17.5px (2.9-3.8x) — [thirdspace.london/membership](https://www.thirdspace.london/membership/)
- Aman is the outlier: h2 only 31px vs 14px body (2.2x) — the quietest scale in the set — [aman.com/wellness](https://www.aman.com/wellness)

**Weight**
- Light/extra-light display: Chronicle Display weight 200 (THE WELL), Beausite Slick 300 (Remedy Place), GT Sectra Fine Book 300 (Third Space), IvyPresto Display 300 (Saint Haven, AllBright), Frutiger Serif Light Italic (Lanserhof), Graphik 300 (SHA), Tiempos Fine Light file (Surrenne), Trade Gothic Light (Bamford) — URLs as in section 1
- Regular/medium display: Lyon Text 400 (Aman), Cardo 400 (Soho House), Romie 500 (Chief), Ayer Poster Medium (The Twenty Two), Plantin 400 (The Ned)
- Bold display appears only at gym-led brands: Bicyclette Bold (KX), Circular 700 labels (Third Space)

**Tracking on uppercase labels (font-size / letter-spacing)**
- Aman 10.1px / 2px (0.2em); Remedy Place 11px / 2.2-2.4px (0.2-0.22em); Maison Estelle 10.8px / 3.6px (0.33em); Bamford 14px / 3px (0.21em); The Ned 14px / 2.1px (0.15em); Heimat 16px / 2px (0.125em); THE WELL 12px / 1.2px (0.1em); Surrenne 14px / 1.4px (0.1em); SHA 14px / 1.4px (0.1em); Chenot 12px / 1.2px (0.1em); Saint Haven 18px / 1.8px (0.1em); Lanserhof 14px / 1.12px (0.08em); Third Space 12px / 0.9px (0.075em, bold) — URLs as in section 1
- Two sites avoid tracked caps almost entirely: Soho House (sentence-case 18px nav, no tracking) and Chief (12px uppercase with only 0.17px tracking) — [sohohouse.com](https://www.sohohouse.com/en-us/), [chief.com](https://chief.com/)
- Tracked caps in the serif itself: The Ned sets Plantin caps at 0.1em; Saint Haven sets IvyPresto caps at 0.107em — [thened.com](https://www.thened.com/), [sainthaven.com.au](https://sainthaven.com.au/)

**Italics for emphasis (found on 10 of 20 sites)**
- THE WELL italicises single words inside a Chronicle Display sentence ("you", "and") — [the-well.com](https://www.the-well.com/)
- The Ned drops lowercase italic connectors into tracked caps ("FROM LONDON *to* NEW YORK", "MEET, WORK & HAVE A GOOD TIME *in* OUR...") — [thened.com](https://www.thened.com/)
- Lanserhof: "*Home of*" in Frutiger Serif Light Italic above caps sans "HEALTH & BEAUTY" — [lanserhof.com/en](https://lanserhof.com/en)
- Chenot: accent word "*Detox*" in Portrait italic among Brandon Grotesque caps — [chenot.com](https://www.chenot.com/chenot-palace/weggis/)
- Third Space ("*for*"), The Twenty Two ("Stay in *Touch*"), Chief ("*since 2019*"), Maison Estelle (names and places in italic within body copy), Heimat (all headlines in italic Suisse Works caps), SHA (bold italic Graphik) — URLs as in section 1

**Line height and line length** (paragraphs of 160+ characters, measured)
- Aman: 14px serif, line-height 1.45, columns 326-680px, about 41-89 characters per line — [aman.com/wellness](https://www.aman.com/wellness)
- THE WELL: 14px sans, line-height 1.5, 320px cards, about 37-43 cpl; 30px serif intro, line-height 1.2, 800px, about 62 cpl, centred — [the-well.com](https://www.the-well.com/)
- Surrenne: 16px, line-height 1.5, 500-670px, about 54-82 cpl, centred — [surrenne.com/en/membership](https://www.surrenne.com/en/membership)
- Maison Estelle: 18px serif, line-height 1.56, about 574-594px, about 52-74 cpl, centred — [maisonestelle.com](https://maisonestelle.com/)
- The Ned: 16px serif, line-height 1.38, 330px, about 38-44 cpl, centred — [thened.com/london/membership](https://www.thened.com/london/membership)
- Headline line-height: 1.0 (THE WELL h1 80/80, Surrenne 86/86), 1.1 (Remedy Place 60/66, Saint Haven 56/61.6), 1.19-1.25 (Chief 64/76, Soho House 56/70)

**Case**
- Sentence or title case headlines: Aman, THE WELL, Remedy Place, Soho House, Chief, Third Space, The Twenty Two, Maison Estelle
- All-caps headlines: Surrenne (hero only), Saint Haven, SHA, House 120, The Ned, Chenot, Bamford, Heimat, Casa Cipriani, KX

**Serif display + sans label mix**
- 16 of 20: Aman, THE WELL, Surrenne, Third Space, Soho House, Chief, Saint Haven, The Ned, The Twenty Two, AllBright, House 120, Lanserhof, Chenot, Heimat, KX, (Six Senses partial). Sans-only: Remedy Place, SHA, Bamford, Casa Cipriani. Serif-led with almost no sans: Maison Estelle.

**Script and monospace**
- No site loaded a script face. Aman declares `Calligraph810` and `Source Code Pro` in CSS but neither was loaded on the home or wellness pages — [aman.com](https://www.aman.com/)
- No site used a monospaced face for labels or numerals.

### Inferences
- A safe house style for the membership page, derived from the medians: display serif at weight 300-400, about 3-4x body size on desktop, line-height 1.05-1.2, sentence case; body 16-18px at line-height 1.5; labels 11-12px uppercase sans at 0.12-0.2em; one italic word per headline as the "signature".
- Centred, short-measure intro paragraphs (40-75 cpl) are the norm on membership pages; long justified blocks are not.
- The current site's two script faces (Dancing Script, Sacramento) have no equivalent on any of the 20 club sites; an italic of the display serif does the job the script is doing now.

### Gaps
- Mobile type scales were not measured.
- Small caps / OpenType feature usage (e.g. Maison Estelle's dedicated caps fonts) was observed via font names only, not via `font-variant` inspection.

---

## 3. Typography trends in luxury wellness and hospitality branding, 2025-2026

### Takeaway
Trend commentary for 2026 points the same way as the live sites: warm, soft or "modern retro" serifs for display, neutral neo-grotesques for text, and a general move away from uniform geometric-sans branding. Monospaced accents and scripts are talked about in trend pieces but are not actually used by the clubs inspected.

### Cited Findings
- A March 2026 trend round-up names "soft serifs" (Recoleta, Canela, Noe Display, Lora) as most common in wellness, boutique hospitality and lifestyle editorial, and calls Canela suited to "luxury brands, premium hospitality, and editorial contexts" — [Made Good Designs, 19 Mar 2026](https://madegooddesigns.com/?p=674) [3P; a design blog, not primary research]
- The same piece lists display serifs in vogue (Ogg, Reckless Neue, Editorial New, Tiempos, Instrument Serif), neo-grotesques (Söhne, Neue Haas Grotesk, Aktiv Grotesk, Suisse Int'l) and monospace accents (IBM Plex Mono, JetBrains Mono, Space Mono, Geist Mono) — [Made Good Designs](https://madegooddesigns.com/?p=674) [3P]
- It also says geometric sans faces such as Circular, Gilroy and Proxima Nova became so common they stopped differentiating, describes Montserrat and Poppins as template-like, and calls Editorial New the most widely adopted display serif — [Made Good Designs](https://madegooddesigns.com/?p=674) [3P]
- Adobe's "Modern Retro Serif" microtrend (dated 1 Apr 2026) says the look is "an especially good fit for hotels, resorts, and other luxury getaway providers" — [Adobe Express blog](https://www.adobe.com/express/learn/blog/microtrend-modern-retro-serif) [3P]
- Creative Bloq's 2026 trends piece is headlined "Breaking rules and bringing joy" (full text could not be retrieved; a search summary says the uniform sans-serif era is giving way to type with more personality) — [Creative Bloq](https://www.creativebloq.com/design/fonts-typography/breaking-rules-and-bringing-joy-top-typography-trends-for-2026) [3P, headline only verified]
- Live evidence for each trend family [CS]: high-contrast modern serif — Chronicle Display XLight ([THE WELL](https://www.the-well.com/)), Tiempos Fine ([Surrenne](https://www.surrenne.com/en)), GT Sectra Fine ([Third Space](https://www.thirdspace.london/)); soft/flared serif — Romie ([Chief](https://chief.com/)), IvyPresto ([Saint Haven](https://sainthaven.com.au/), [AllBright](https://allbrighteverywoman.com/hub/)), Canela ([sainthaven.com](https://sainthaven.com/)); condensed editorial serif — Ayer Poster ([The Twenty Two](https://www.thetwentytwo.com/)); neo-grotesque sans — Suisse Int'l, Neue Haas Grotesk, Graphik, GT America, Styrene B (Surrenne, Chief, SHA, Heimat/Saint Haven, THE WELL); contrasted sans as display — Beausite Slick ([Remedy Place](https://www.remedyplace.com/)); humanist sans — Whitney ([Aman](https://www.aman.com/)), Neue Frutiger ([Lanserhof](https://lanserhof.com/en)); monospaced accents — none; script — none.

### Inferences
- "Restrained script use" in this tier effectively means no script at all; handwriting, where present, is in illustration or logo artwork (e.g. Maison Estelle's illustrated monogram) rather than a webfont.
- The monospace-accent trend belongs to tech/DTC branding and has not crossed into luxury clubs; using one would read as a departure, not as "club-like".
- Wide/extended grotesques for labels (GT America Extended/Expanded at Heimat and Saint Haven) are a visible 2025-26 sub-trend among newer wellness clubs.

### Gaps
- Most search results for "luxury spa/wellness fonts" were unsourced SEO pages (pages.dev domains) and were discarded. I found no rigorous 2025-26 survey of hospitality typography; Typewolf's annual list URL returned 404 and Brand New was not searched.
- Creative Bloq article body was truncated on fetch; only its headline is confirmed.

---

## 4. Long-list of candidate pairings (10 free-to-premium options)

### Takeaway
Seven fully free, self-hostable pairings reproduce the club looks with verified rupee glyphs; four premium pairings are the "real thing" but cost money and their ₹ coverage was not verified. The strongest free candidates are Newsreader + Figtree (Aman/The Ned), Cormorant + Ysabeau (evolution of today), Fraunces + DM Sans (Chief), Playfair + Albert Sans (THE WELL), Zodiak + General Sans (Surrenne) and EB Garamond + Schibsted Grotesk (Soho House).

### Cited Findings

**Method for ₹ and numerals [RT]:** each font was loaded in the browser from the Google Fonts CSS API (`fonts.googleapis.com/css2?family=...&text=₹0123456789`) or the Fontshare API (`api.fontshare.com/v2/css?f[]=slug@400`) and ₹ was measured on canvas against three fallbacks of different widths; ₹ counts as present only if the width is identical across all three. Figure style was inferred by comparing digit widths under `lnum`, `onum` and `tnum`. The method was cross-checked against the project's own files with fontTools (it agreed: Manrope, Nunito Sans, Dancing Script have ₹; the Sacramento subset does not). No font files were saved to disk. Numeral results are heuristic.

**Licences**
- Google Fonts families below are SIL OFL (self-hosting, subsetting and modification permitted) — specimens linked per row.
- Fontshare: "All Fontshare fonts are 100% free for personal and commercial use"; closed-source families are under the ITF Free Font License (FFL) v2.0 dated 17 Aug 2026, whose notice explicitly covers "downloading, accessing, self-hosting, installing, storing, embedding"; open-source families there are OFL — [fontshare.com/licenses](https://www.fontshare.com/licenses/itf-ffl)
- Collletttivo: "Collletttivo typefaces are released under SIL Open Font License (OFL)"; catalogue includes Mazius Display (4 styles), Ortica (4), Sprat (18 + variable), Apfel Grotezk (5) — [collletttivo.it/typefaces](https://www.collletttivo.it/typefaces)

**Free and self-hostable (weights/axes/designer details are from my knowledge of the specimens [ID]; ₹ and numerals are [RT])**

| # | Display + text (+ accent) | Makers / licence / where | Weights, italics, variable | ₹ and numerals [RT] | Resembles | Mood | vs current site |
|---|---|---|---|---|---|---|---|
| F1 | **Cormorant** (or keep Cormorant Garamond) + **Ysabeau Office**; accent = Cormorant Italic | Both Christian Thalmann / Catharsis Fonts, OFL. [Cormorant](https://fonts.google.com/specimen/Cormorant), [Ysabeau Office](https://fonts.google.com/specimen/Ysabeau+Office) | Cormorant 300-700 + true italics, variable wght. Ysabeau variable wght with true italics | Both ₹ yes. Cormorant: old-style figures by default, lining via `lnum`, tabular via `tnum`. Ysabeau Office: lining + tabular by default (plain Ysabeau defaults to old-style) | Maison Estelle, Saint Haven (light serif caps), Aman's serif + humanist sans | Delicate, literary, feminine | **Evolution** — same serif, sans swapped for its designed companion |
| F2 | **Newsreader** (Display optical sizes for heads, Text sizes for body) + **Figtree** labels | Production Type (Newsreader), Erik Kennedy (Figtree), OFL. [Newsreader](https://fonts.google.com/specimen/Newsreader), [Figtree](https://fonts.google.com/specimen/Figtree) | Newsreader 200-800 + true italics, variable wght + opsz. Figtree 300-900 + italics, variable | Both ₹ yes. Newsreader lining, tabular by default. Figtree tabular via `tnum` | Aman (Lyon Display/Text), The Ned (Plantin) | Calm, editorial, grown-up; sturdier than Cormorant | **Evolution** (still a classical serif + friendly sans, but far more robust on phones) |
| F3 | **Fraunces** (low SOFT/WONK, weight 300-400) + **DM Sans** | Undercase Type (Fraunces), Colophon Foundry (DM Sans), OFL. [Fraunces](https://fonts.google.com/specimen/Fraunces), [DM Sans](https://fonts.google.com/specimen/DM+Sans) | Fraunces 100-900 + italics, variable wght/opsz/SOFT/WONK. DM Sans 100-1000 + italics, variable | Both ₹ yes. Neither showed tabular figures in the test (use for prices in running text, not tables) | Chief (Romie), the "soft serif" trend, AllBright (which uses DM Sans itself [CS]) | Warm, soft, approachable, slightly retro | **Departure** (soft/wonky serif instead of Garamond) |
| F4 | **Playfair** (the newer optical-size family, weight 300, not Playfair Display) + **Albert Sans** | Claus Eggers Sørensen (Playfair), Andreas Rasmussen (Albert Sans), OFL. [Playfair](https://fonts.google.com/specimen/Playfair), [Albert Sans](https://fonts.google.com/specimen/Albert+Sans) | Playfair 300-900 + italics, variable wght + opsz. Albert Sans 100-900 + italics, variable | Both ₹ yes. Playfair old-style default, lining via `lnum`, `tnum` available. Albert Sans no tabular detected | THE WELL (Chronicle Display XLight + Styrene), Third Space (GT Sectra Fine) | Crisp, high-contrast, fashion-editorial | **Departure** (high-contrast modern vs old-style) |
| F5 | **Zodiak** + **General Sans** | Indian Type Foundry via Fontshare, ITF FFL (free commercial, self-host). [Zodiak](https://www.fontshare.com/fonts/zodiak), [General Sans](https://www.fontshare.com/fonts/general-sans) | Zodiak thin to black + italics, variable. General Sans extralight to bold + italics, variable | Both ₹ yes. No tabular figures detected in either | Surrenne (Tiempos Fine + Suisse Int'l) | Confident, contemporary-modern, urban | **Departure** |
| F6 | **EB Garamond** + **Schibsted Grotesk** (or Familjen Grotesk) | Georg Duffner / Octavio Pardo (EB Garamond), Bakken & Bæck (Schibsted Grotesk), OFL. [EB Garamond](https://fonts.google.com/specimen/EB+Garamond), [Schibsted Grotesk](https://fonts.google.com/specimen/Schibsted+Grotesk) | EB Garamond 400-800 + italics, variable. Schibsted Grotesk 400-900 + italics, variable | Both ₹ yes. EB Garamond tabular by default. Schibsted `tnum` | Soho House (Cardo + HK Grotesk, both free [CS]) — note Cardo and Hanken Grotesk themselves lack ₹ [RT] | Bookish, unfussy, "house" warmth | **Evolution** (a sturdier Garamond with a grotesque) |
| F7 | **Ysabeau** Light as display sans + **Manrope** text/labels (no serif) | Christian Thalmann (Ysabeau), Mikhail Sharanda (Manrope), OFL. [Ysabeau](https://fonts.google.com/specimen/Ysabeau), [Manrope](https://fonts.google.com/specimen/Manrope) | Ysabeau variable wght + italics. Manrope 200-800 variable, no italics | Both ₹ yes. Ysabeau old-style default + lining alt, `tnum`. Manrope `tnum` | Remedy Place (Beausite Slick light sans headlines), Lanserhof, SHA | Clinical-calm, modern wellness, less "club" | **Departure** in feel, though it reuses the Manrope already shipped |
| F8 | **Sentient** + **Supreme** | Indian Type Foundry via Fontshare, ITF FFL. [Sentient](https://www.fontshare.com/fonts/sentient), [Supreme](https://www.fontshare.com/fonts/supreme) | Sentient extralight to bold + italics, variable. Supreme thin to extrabold + italics, variable | Both ₹ yes. Sentient lining default with old-style alternate; no tabular detected | Aman / Chief middle ground (soft humanist serif) | Gentle, readable, quietly premium | **Evolution** |

Optional accents for any free pairing: the display serif's own italic (what the clubs do); **Geist Mono** or **IBM Plex Mono** if a monospaced price/label accent is wanted (both ₹ yes, tabular by default [RT]) — [Geist Mono](https://fonts.google.com/specimen/Geist+Mono), [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono); if a script must stay, **Imperial Script** or **Ballet** are formal copperplate options that do include ₹ [RT] — [Imperial Script](https://fonts.google.com/specimen/Imperial+Script), [Ballet](https://fonts.google.com/specimen/Ballet).

**Premium (paid; flagged)**

| # | Display + text | Foundry and price evidence | Styles | Self-host | Resembles | Mood | vs current |
|---|---|---|---|---|---|---|---|
| P1 | **Canela** (or Canela Deck) + **Styrene B** or **Graphik** | Commercial Type. Catalogue lists Canela family $325, Canela Text $350, collection $800, single styles from $50; licence scope/web pricing is by enquiry — [commercialtype.com/catalog/canela](https://commercialtype.com/catalog/canela) | 6 weights thin to black, italics for each; Condensed, Deck, Text cuts | Yes with a web licence (Saint Haven softwear self-hosts `Canela-Light-Web.woff2` [CS]) | The archetypal wellness serif; Saint Haven softwear [CS]; THE WELL's sans is Styrene B [CS]; SHA's is Graphik [CS] | Soft, sculptural, serene | Departure; highest cliché risk |
| P2 | **Tiempos Fine** + **Suisse Int'l** or **Söhne** | Klim Type Foundry (Tiempos, Söhne); Swiss Typefaces (Suisse). Price not retrieved — [klim.co.nz/retail-fonts/tiempos-fine](https://klim.co.nz/retail-fonts/tiempos-fine/) | 6 weights light to black + italics; variable font with full family; WOFF2 33-65kb per style | Yes with web licence | Surrenne exactly [CS] | Sharp, warm, editorial | Departure |
| P3 | **GT Sectra Fine** + **GT America** | Grilli Type; free trial fonts available; price not retrieved — [grillitype.com/typeface/gt-sectra](https://www.grillitype.com/typeface/gt-sectra) | Sectra/Fine: book to black + italics; 30 styles in all | Yes with web licence | Third Space (Sectra Fine) [CS]; Heimat and Saint Haven (GT America) [CS] | Calligraphic-sharp, contemporary | Departure |
| P4 | **PP Editorial New** + **PP Neue Montreal** | Pangram Pangram. "Licenses start at $40"; free to try; 16 styles (8 weights + italics) + variable — [pangrampangram.com/products/editorial-new](https://pangrampangram.com/products/editorial-new) | Thin 100 to Heavy 900 + italics, variable | Yes with web licence | Generic "editorial luxury" look; not used by any club inspected | Narrow, elegant, fashion-blog | Departure; called the most widely adopted display serif ([Made Good Designs](https://madegooddesigns.com/?p=674)) |
| P5 | **Romie** + **Neue Haas Grotesk** | Margot Lévêque (Romie); Monotype/Linotype (NHG). Prices not retrieved | Not verified | With licence | Chief exactly [CS]; Romie is also declared in Surrenne's CSS [CS] | Soft, feminine, assured | Departure |
| P6 | **Ayer Poster** + **Dia** | Commercial Type (Ayer); Schick Toikka (Dia: four weights with italics, trials offered) — [schick-toikka.com/dia](https://www.schick-toikka.com/dia) | Ayer Poster many widths [ID]; Dia 8 fonts | With licence | The Twenty Two exactly [CS] | Glamorous, condensed, magazine-masthead | Clear departure |

### Inferences
- Best "evolution" shortlist candidates: F1 (Cormorant + Ysabeau Office), F2 (Newsreader + Figtree), F6 (EB Garamond + Schibsted Grotesk), F8 (Sentient + Supreme). Best "departure" candidates: F3 (Fraunces + DM Sans), F4 (Playfair + Albert Sans), F5 (Zodiak + General Sans). F7 is the sans-only wildcard.
- For a ₹10,000 fee displayed prominently, pairings whose text face has lining, tabular figures by default (Newsreader, EB Garamond, Ysabeau Office, Nunito Sans) need no extra CSS; with Cormorant or Playfair the price should be set with `font-variant-numeric: lining-nums` or the figures will be old-style and look uneven next to ₹.
- Premium faces buy distinctiveness, not legibility; for a small club the free set covers every look observed except the condensed Ayer Poster style.
- Variable-font versions (F1-F6, F8) keep self-hosted payload small: one file per family per style (roman/italic) covers all weights.

### Gaps
- ₹ coverage of all premium faces (Canela, Tiempos Fine, GT Sectra, Editorial New, Romie, Ayer Poster, Dia, Styrene, Graphik, Söhne, Suisse, GT America, Neue Haas Grotesk) was not verified; check each foundry's glyph list or trial fonts before buying.
- Web-licence prices for Klim, Grilli Type, Swiss Typefaces, Schick Toikka, Margot Lévêque, Sharp Type, Dinamo and Colophon were not retrieved (Klim buy URL returned 404; others show prices only in a configurator). Only Commercial Type's Canela catalogue prices and Pangram Pangram's "from $40" are sourced.
- The FFL's detailed "Embedding" and "Limitations of Usage" clauses were not read in full (page text was cut off after the Notice to User); read them before shipping a Fontshare face, especially regarding subsetting/modifying files.
- ₹ coverage of Collletttivo (Sprat, Mazius Display, Ortica) and Velvetyne faces could not be tested without downloading files; Velvetyne was not researched.
- Weights/axes/designers in the free table are from memory of the specimens, not re-read today.
- Rendering was not tested on a physical Android device.

---

## 5. Evolution of the current Cormorant Garamond + Nunito Sans setup vs clear departure

### Takeaway
The current stack already matches the club recipe structurally (light classical serif + sans); what separates it from the club tier is the rounded sans, two script faces, and a hairline serif used small. Swapping the sans and dropping scripts is an evolution; changing the serif genre (soft, high-contrast or condensed) is the departure.

### Cited Findings
- The site currently ships `CormorantGaramond-latin-wght.woff2` (variable weight, upright only, 229 glyphs), Manrope Regular/Medium/SemiBold, Nunito Sans Regular/Italic/Medium/SemiBold/Bold, Dancing Script Regular/Medium/SemiBold and `Sacramento-latin.woff2` — local files in `/Users/skybridge/Desktop/Sphere/dist/assets/fonts/` (inspected with fontTools)
- No italic Cormorant Garamond file is shipped, so any italic serif on the site today is browser-synthesised — same local directory listing
- None of the 20 club sites loads a script face, and none uses a rounded-terminal sans like Nunito Sans; their sans faces are grotesques or humanist sans (Whitney, Styrene B, Suisse Int'l, GT America, Neue Haas Grotesk, HK Grotesk, Circular, Graphik, Dia) — section 1 [CS]
- Light old-style/display serif in tracked caps, which Cormorant Garamond does well, is exactly Saint Haven's treatment (IvyPresto Display 300, caps, 0.107em) — [sainthaven.com.au](https://sainthaven.com.au/) [CS]

### Inferences
- **Evolution (keeps brand continuity):** F1 Cormorant + Ysabeau Office; F2 Newsreader + Figtree; F6 EB Garamond + Schibsted Grotesk; F8 Sentient + Supreme. Minimum-change version: keep Cormorant Garamond for display only (28px and up), add its true italic for emphasis, use Manrope (already shipped) or Ysabeau Office for body and labels, retire Dancing Script and Sacramento.
- **Clear departure:** F3 Fraunces + DM Sans (soft serif), F4 Playfair + Albert Sans (high contrast), F5 Zodiak + General Sans (modern), F7 sans-only, and all premium pairings P1-P6.
- With a warm ivory (#FFF8EC) ground and sage/ink text, low-contrast soft serifs (Fraunces, Sentient, Newsreader) hold up better than hairline faces (Cormorant Light, Playfair 300) because thin strokes in sage on ivory lose contrast quickly; hairline faces should be set in the ink tone and at display sizes only.

### Gaps
- The site's live CSS was not audited to see where each of the five current families is actually applied; only the shipped font files were inspected.
- No side-by-side render of the candidates on the ivory palette was produced.

---

## 6. Pitfalls

### Takeaway
Three concrete risks: (1) the site's own Cormorant Garamond subset has no ₹ glyph, so the ₹10,000 price is currently falling back to another font; (2) many "luxury" free fonts lack ₹ entirely; (3) the most recognisable luxury-template faces are now clichés, and hairline serifs degrade at small sizes on phones.

### Cited Findings
- **Current site, missing ₹:** `CormorantGaramond-latin-wght.woff2` and `Sacramento-latin.woff2` contain no U+20B9; the Manrope, Nunito Sans and Dancing Script TTFs do — local files in `/Users/skybridge/Desktop/Sphere/dist/assets/fonts/` (fontTools cmap check). The full Cormorant Garamond family does contain ₹ [RT] ([specimen](https://fonts.google.com/specimen/Cormorant+Garamond)); it is the "latin" subset that drops it, so the fix is a subset that includes U+20B9.
- **Free fonts with no ₹ glyph [RT]** (Google Fonts API, 11 Nov 2026): Instrument Serif, Bodoni Moda, DM Serif Display, Libre Caslon Text, Cardo, Marcellus, Italiana, Young Serif, Lora, Gilda Display, Prata, Rufina, Forum, Bellefair, Cinzel, Tenor Sans, Libre Baskerville, Baskervville, Old Standard TT, Sorts Mill Goudy, Hanken Grotesk, Instrument Sans, Jost, Outfit, Red Hat Display, Urbanist, Sora, Onest, Karla, Be Vietnam Pro, Rethink Sans, Hedvig Letters Serif/Sans, DM Mono; scripts Sacramento, Italianno, Pinyon Script, Mrs Saint Delafield, WindSong, Monsieur La Doulaise, Petit Formal Script, La Belle Aurore, Homemade Apple — tested via [fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Inter)
- **Fontshare fonts with no ₹ glyph [RT]:** Gambetta, Satoshi, Switzer, Chillax, Rowan, Recia, Plein — tested via [api.fontshare.com](https://api.fontshare.com/v2/css?f[]=satoshi@400&display=swap). (Zodiak, Sentient, Erode, Boska, Bespoke Serif, Melodrama, General Sans, Cabinet Grotesk, Supreme, Author, Synonym, Britney, Clash Display, Ranade do have it.)
- **Free fonts with ₹ confirmed [RT]:** Cormorant family, Fraunces, Newsreader, Gloock, Playfair and Playfair Display, EB Garamond, Libre Caslon Display, Literata, Source Serif 4, Crimson Pro, Spectral, Castoro, Gelasio, Petrona, Ysabeau, DM Sans, Manrope, Nunito Sans, Figtree, Schibsted Grotesk, Albert Sans, Inter, Work Sans, Mulish, Geist, Host Grotesk, Familjen Grotesk, Plus Jakarta Sans, Montserrat, Poppins, Raleway, Josefin Sans, IBM Plex Mono, Geist Mono, Dancing Script, Ballet, Imperial Script — same method
- **Old-style figures by default** (prices look uneven unless `lnum` is set) [RT]: Cormorant, Cormorant Garamond, Playfair, Playfair Display, Castoro, Ysabeau (not Ysabeau Office), Gelasio, Raleway, Vollkorn, Boska, Author
- **Overuse:** Montserrat and Poppins are described as generic and template-like; Circular, Gilroy and Proxima Nova as so common they no longer differentiate; Editorial New as the most widely adopted display serif — [Made Good Designs, Mar 2026](https://madegooddesigns.com/?p=674) [3P]
- Canela is listed by a font-comparison site as typical of "lifestyle and wellness brand identities", with Cormorant Garamond named as its closest free substitute — [fontalternatives.com](https://fontalternatives.com/compare/cormorant-garamond-vs-canela/) [3P, low-authority]
- IvyPresto appears on two of the 20 sites (Saint Haven, AllBright) and GT America on two (Heimat, Saint Haven) — section 1 [CS]
- Adobe Fonts faces (IvyPresto, Futura PT, Sweet Sans, Nocturne Serif) are delivered from `use.typekit.net` on the club sites that use them (House 120, Saint Haven, Casa Cipriani) — section 1 [CS]

### Inferences
- **Cliché list to avoid or use knowingly:** Playfair Display, Cormorant Garamond set large with wide-tracked Montserrat/Josefin Sans/Raleway caps (the stock "boutique spa template"), Cinzel, Bodoni Moda, any brush/monoline script (Dancing Script, Sacramento, Great Vibes-style), Canela and PP Editorial New / Ogg among paid faces. The current site's Cormorant Garamond + script accents sits close to this template; changing the sans and dropping the scripts moves it away without changing the serif.
- **Small-size rendering on Android:** hairline, small-x-height display serifs (Cormorant Garamond Light/Regular, Playfair at low weights, Bodoni Moda, Italiana, Gloock's thin joins) lose their thin strokes below roughly 18-20px on mid-range Android screens; use them for headings only and put body copy in a text-grade face (Newsreader's text optical sizes, EB Garamond, Sentient, or a sans). Fonts with an optical-size axis (Newsreader, Fraunces, Playfair, DM Sans) adapt automatically. This is reasoned from the designs' stroke contrast, not device-tested.
- **Adobe Fonts faces are unusable here:** the site's security policy blocks third-party font hosts and Adobe Fonts cannot be self-hosted, which rules out IvyPresto-via-Adobe, Futura PT, Sweet Sans and similar even though several clubs use them.
- **Subsetting trap:** any font downloaded as a Google "latin" subset will silently lose ₹ (it sits in the "latin-ext" range); build subsets with U+20B9 explicitly included and test the price line on a phone.
- **Synthesised italics:** the italic-word emphasis convention only looks premium with a true italic file; ship the italic of whichever serif is chosen.
- **Single-style display fonts** (Instrument Serif, Gloock, DM Serif Display, Libre Caslon Display, Italiana) have one weight and limited or no italics, which blocks the light-weight + italic-accent convention seen at the clubs.

### Gaps
- No authoritative design-press source was found that explicitly calls Canela, Cormorant or Playfair "overused"; the cliché list is my professional judgement plus one blog source.
- No real-device Android rendering test was run.
- Whether the live membership page currently renders ₹ in a fallback font was inferred from the font file contents, not observed in a browser.
