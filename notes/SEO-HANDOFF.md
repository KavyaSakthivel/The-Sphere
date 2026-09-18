# The Sphere — SEO launch handoff

## Current status

The website is prepared for a Coimbatore audience. It currently uses the existing Sites URL and remains owner-private. Google cannot index pages behind that access restriction. The purchased domain is held by the digital marketer and has not yet been provided or connected.

The Sphere has changing venues. The website identifies Coimbatore, Tamil Nadu, India and explains that venue details are shared by email or WhatsApp. It does not publish a permanent street address or business phone number.

## Implemented

- Coimbatore-focused homepage title and description, with natural location references in the visible page.
- Unique titles, descriptions and canonical URLs for the homepage and five existing journal reflections.
- Static, crawlable journal pages with semantic headings, breadcrumbs and related links. The original homepage reading dialogs still work.
- Organization, WebSite and WebPage structured data; Article and BreadcrumbList data for journal pages. No fabricated address, dates, reviews, ratings or opening hours.
- XML sitemap at `/sitemap.xml` and crawler instructions at `/robots.txt`.
- Social sharing titles and descriptions.
- Responsive WebP hero images: approximately 60–85% smaller than the previous JPEG, depending on screen size.
- Existing brand styling, free licensed fonts, logos and all 103 source-content lines preserved.

## Launch sequence for the marketer

1. Confirm the purchased domain and the preferred HTTPS hostname (with or without `www`). Supply DNS access through the registrar's normal delegation process, rather than sending passwords.
2. Connect the custom domain through Sites using the exact DNS records returned for that domain. Wait for domain verification and HTTPS provisioning; no DNS records have been guessed in this handoff.
3. Change `url` in `data/site.json` to the verified HTTPS origin, without a trailing path, and set `domain_confirmed` to `true`. Run the build and checks below, then publish the generated `dist` folder through the existing Sites project. This updates every canonical URL, schema identifier, social URL and sitemap entry together.
4. At the owner's launch instruction, change the site audience to public. Check the homepage, all five articles, robots.txt and sitemap.xml without signing in. They must be accessible without an authentication screen. Verify the canonical pages return HTTP 200, and check response headers for any indexing restriction.
5. Configure supported permanent redirects from alternate domain variants to the preferred hostname. If the Sites hostname remains accessible, verify its pages identify the final domain in their canonical tags. Preserve the five journal paths when moving hosts.
6. Verify a Domain property in Google Search Console using the TXT record Google supplies. Submit the final-domain sitemap and use URL Inspection on the homepage and an article. Indexing and rankings are Google's decisions, not guaranteed by submission. See [Google's indexing requirements](https://developers.google.com/search/docs/essentials/technical) and [sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
7. Review mobile performance on the public domain using PageSpeed Insights and later Search Console's Core Web Vitals report. Compression was verified locally; no production performance score or field-data result is claimed.

Build and validation from the project folder:

```sh
python3 scripts/build_site.py
python3 scripts/check_content.py
python3 scripts/check_seo.py
node --check dist/site.js
```

## Local discovery and ongoing work

Keep the name “The Sphere,” Coimbatore location and official Instagram identity consistent across public profiles. Assess Google Business Profile eligibility against the actual operating model before creating a listing. A changing event venue is not a permanent business address; do not use a temporary venue, virtual office or invented address to obtain a listing. See [Google's business eligibility and representation guidelines](https://support.google.com/business/answer/3038177?hl=en).

When real events are confirmed, publish useful event pages with accurate dates, locations, booking details and Event data that matches visible information. Do not add placeholder events or change publication dates just to imply freshness. Keep any private venue details private until the club authorizes their publication.

After launch, review Search Console impressions, clicks, indexing and queries such as women's wellness club in Coimbatore. Improve content from actual member questions and confirmed offerings. Obtain genuine reviews where the club has an eligible profile, and relevant local mentions through real partnerships. Avoid purchased links, repeated city keyword stuffing and fabricated testimonials. [Google describes local results](https://support.google.com/business/answer/7091?hl=en) as depending principally on relevance, distance and prominence/popularity.

The invitation flow currently leads to the official Instagram profile. No email or WhatsApp intake endpoint has been invented. Replace that destination only when the club provides its chosen membership process. No analytics or advertising tracker was added in this update.

## Checks completed

All 103 source lines remain present. Six canonical pages have distinct titles and descriptions, valid JSON-LD, matching sitemap entries and working local assets. Desktop and mobile layouts, article reading, the homepage journal dialog and mobile navigation were checked. No horizontal overflow or browser console errors were observed in those checks. Live-domain indexing, DNS, Search Console and public performance checks remain launch tasks.
