# Upcoming gatherings

The club adds its own monthly gatherings by typing a row into a Google Sheet. There is no login,
no admin panel and no server: the website reads the sheet directly.

**Right now this is switched off.** `gatherings_csv` in `data/site.json` is empty, so the section
shows only the honest standing line — *"Dates and venues are shared with members by email and
WhatsApp"* — and nothing else is published. It stays that way until the steps below are done, so
the client can decide first whether she wants dates on the open web at all.

## One-time setup (about ten minutes, done once)

1. Create a new Google Sheet in the club's own account, named something like **The Sphere —
   Gatherings**. Row 1 must be these six headings, in any order:

   | Date | Gathering | About it | Time | Where | Show on website |
   |---|---|---|---|---|---|
   | 4 October 2026 | Sound & Stillness | Sound healing, breathwork and a slow morning together | 10am – 12pm |  | yes |

2. **File → Share → Publish to web.** Choose the sheet's tab, choose **Comma-separated values
   (.csv)**, press **Publish**. Copy the link it gives you — it ends in `pub?output=csv`.
3. Paste that link into `data/site.json`:

   ```json
   "gatherings_csv": "https://docs.google.com/spreadsheets/d/e/…/pub?output=csv"
   ```

4. Rebuild and redeploy:

   ```bash
   python3 scripts/build_site.py && python3 scripts/check_content.py
   ```

5. Give the client the sheet link and tell her to bookmark it. That link is the whole admin panel.

Publishing makes only that sheet readable to anyone holding the link. Keep private notes, member
names and phone numbers in a **different** sheet — never on the published tab.

## Every month (about a minute, done by the club)

Open the bookmarked sheet and add one row per gathering. That is the entire job. The website
catches up within a few minutes; Google caches the published file briefly, so it is not instant.

- **Date** — type it as `4 October 2026`. `2026-10-04` works too. Day comes first in slash dates,
  so `06/12/2026` means 6 December.
- **Gathering** — the name, e.g. *Move & Reconnect*.
- **About it** — one line. Two at most.
- **Time** — `10am – 12pm`, or leave it blank.
- **Where** — usually leave this **blank**. Blank prints *"Venue shared by email or WhatsApp"*,
  which keeps the venue private.
- **Show on website** — leave blank or write `yes`. Write `no` to keep a row hidden while it is
  still being planned.

Things that are handled for her, so nothing has to be tidied up:

- Past gatherings drop off on their own. Old rows can stay in the sheet as a record.
- The four soonest gatherings show, in date order, however the rows are arranged.
- A date that cannot be read — `Early next year` — is printed exactly as typed rather than dropped.
- Commas and quotes inside a description are fine.
- If the sheet is empty, unreachable, or the internet is having a bad day, the page falls back to
  the standing line. **A broken sheet can never break the website.**

## What this does not do

- Gatherings are fetched by the browser, so search engines will not index them. For an
  invitation-only club whose venue is private, that is the right trade.
- Nothing validates what she types. A wrong date is live until she corrects it.
- It depends on Google keeping "publish to web" alive. If that ever goes away, the fallback line
  appears and the fix is to move the same six columns into `data/gatherings.json` and read that
  instead.

## If a real admin login is ever wanted

It would need a server, a database, and accounts to maintain — worth it only once there is much
more to manage than one row a month (journal posts, a member directory, photographs). Until then
this costs nothing to run and has nothing to go down.

## Sources

- [Publish a file from Google Drive](https://support.google.com/docs/answer/37579) — the publish-to-web step and what it exposes.
- CORS on the published CSV endpoint was confirmed directly against `docs.google.com` on 21 September 2026: the response carries `access-control-allow-origin`, so a static page can read it in the browser.
