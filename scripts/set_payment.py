"""Connect the Wellness Carnival page to the client's payment link, then rebuild the site.

  python3 scripts/set_payment.py "https://rzp.io/rzp/xxxxxx"        # any https payment link
  python3 scripts/set_payment.py '<form><script ... data-payment_button_id="pl_xxx" ...></form>'
  python3 scripts/set_payment.py pl_xxxxxxxxxxxxxx                    # a Razorpay Payment Button id
  python3 scripts/set_payment.py --off                                # back to "Ticket booking will open soon."

A plain link (Razorpay Payment Link or Payment Page, or another provider) makes every booking button
on the page go straight to it. A Razorpay Payment Button id (or the embed code that contains one)
puts Razorpay's own button in the ticket card, so checkout opens on top of the page instead.
Deploy dist/ afterwards as usual.
"""
from pathlib import Path
from urllib.parse import urlparse
import html, json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT/'data/event.json'


def read(value):
 value = value.strip()
 if value == '--off':
  return '', ''
 button = re.search(r'\b(pl_[A-Za-z0-9]{6,})\b', value)
 if button:
  return '', button.group(1)
 url = value.strip('\'"<> ')
 parsed = urlparse(url)
 if parsed.scheme != 'https' or not parsed.netloc or ' ' in url:
  sys.exit(f'Not a secure (https://) payment link: {value!r}\nCopy the full link the client sent, starting with https://')
 return url, ''


def main():
 if len(sys.argv) != 2:
  sys.exit(__doc__)
 url, button = read(sys.argv[1])
 event = json.loads(EVENT.read_text())
 event['payment_url'], event['razorpay_button_id'] = url, button
 EVENT.write_text(json.dumps(event, indent=2, ensure_ascii=False)+'\n')
 subprocess.run([sys.executable, str(ROOT/'scripts/build_site.py')], check=True)
 page = (ROOT/'dist'/event['slug']/'index.html').read_text()
 if url:
  count = page.count(f'href="{html.escape(url, quote=True)}"')
  print(f'Booking is live: {count} buttons on /{event["slug"]}/ now open {url}')
 elif button:
  print(f'Booking is live: Razorpay button {button} is embedded in the ticket card on /{event["slug"]}/')
 else:
  print(f'Booking is off: /{event["slug"]}/ shows "Ticket booking will open soon."')


if __name__ == '__main__':
 main()
