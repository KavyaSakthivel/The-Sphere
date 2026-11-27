// Settings for the booking backend. Secrets come only from the environment (Hostinger's
// Environment Variables, or a local .env that git ignores); event facts come from data/event.json,
// the same file that builds the page, so the price a guest sees is the price they are charged.
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const readJson = file => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));

const flag = value => /^(1|true|yes|on)$/i.test(String(value || '').trim());
const int = (value, fallback) => (Number.isInteger(Number(value)) && String(value).trim() !== '' ? Number(value) : fallback);

function loadConfig(env = process.env) {
  const site = readJson('data/site.json');
  let event = null;
  try { event = readJson('data/event.json'); } catch { /* no event: bookings stay closed */ }

  const siteUrl = (env.SITE_URL || site.url).replace(/\/+$/, '');
  const testMode = flag(env.TEST_MODE);
  const config = {
    siteUrl,
    // The site's own origin, with and without www, may ask for payment links.
    allowedOrigins: [siteUrl, siteUrl.replace(/^(https?:\/\/)(?!www\.)/, '$1www.'),
      ...String(env.EXTRA_ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean)],
    trustProxy: env.TRUST_PROXY === undefined ? true : flag(env.TRUST_PROXY),
    bookingsEnabled: flag(env.BOOKINGS_ENABLED),
    bookingTtlMinutes: Math.max(16, int(env.BOOKING_TTL_MINUTES, 20)), // Razorpay needs at least 15 minutes
    event: event && {
      slug: event.slug,
      name: event.name,
      end: Date.parse(event.end),
      unitPricePaise: Math.round(Number(event.price_inr) * 100),
      maxPerBooking: int(event.max_tickets_per_booking, 10),
      websiteTicketLimit: event.website_ticket_limit == null ? null : int(event.website_ticket_limit, null),
      itemId: `${event.slug}-entry`,
      itemName: `${event.name} – Entry ticket`,
      sourceUrl: `${siteUrl}/${event.slug}/`,
      // The club's Razorpay Payment Page: its paid sales are reported to Meta too (see handlePagePayment in app.js).
      paymentPage: event.payment_page && /^pl_[A-Za-z0-9]{6,40}$/.test(event.payment_page.razorpay_page_id || '') ? {
        id: event.payment_page.razorpay_page_id,
        metaSharing: event.payment_page.meta_sharing === 'notice' ? 'notice' : 'off',
        consentField: String(event.payment_page.consent_field || '').trim() || null,
      } : null,
      // Where Razorpay sends the guest after paying. Only once the client has approved the page's wording.
      confirmationUrl: event.booking_confirmation && event.booking_confirmation.draft === false
        ? `${siteUrl}/${event.slug}/booked/` : null,
    },
    // TEST_MODE=on switches to the RAZORPAY_TEST_* keys for a short trial on the live site, without
    // touching the live keys (Razorpay shows a live secret only once). Webhooks signed with either secret are
    // accepted meanwhile, so live notices that arrive during the trial are not refused.
    razorpay: testMode ? {
      keyId: env.RAZORPAY_TEST_KEY_ID || '',
      keySecret: env.RAZORPAY_TEST_KEY_SECRET || '',
      webhookSecret: env.RAZORPAY_TEST_WEBHOOK_SECRET || '',
      webhookSecrets: [env.RAZORPAY_TEST_WEBHOOK_SECRET, env.RAZORPAY_WEBHOOK_SECRET].filter(Boolean),
      apiBase: env.RAZORPAY_API_BASE || 'https://api.razorpay.com/v1',
    } : {
      keyId: env.RAZORPAY_KEY_ID || '',
      keySecret: env.RAZORPAY_KEY_SECRET || '',
      webhookSecret: env.RAZORPAY_WEBHOOK_SECRET || '',
      webhookSecrets: [env.RAZORPAY_WEBHOOK_SECRET].filter(Boolean),
      apiBase: env.RAZORPAY_API_BASE || 'https://api.razorpay.com/v1',
    },
    testMode,
    meta: {
      accessToken: env.META_ACCESS_TOKEN || '',
      datasetId: env.META_DATASET_ID || site.meta_pixel_id || '',
      apiVersion: env.META_API_VERSION || 'v24.0',
      testEventCode: env.META_TEST_EVENT_CODE || '',
      apiBase: env.META_API_BASE || 'https://graph.facebook.com',
    },
    db: env.DB_HOST ? {
      host: env.DB_HOST, port: int(env.DB_PORT, 3306), user: env.DB_USER, password: env.DB_PASSWORD, database: env.DB_NAME,
    } : null,
    // Without MySQL, bookings go in a JSON file. Only for local development, or a folder the host never
    // wipes: a redeploy that deletes it would orphan unpaid bookings, and their payments would go unreported.
    dataDir: env.DATA_DIR || path.join(ROOT, '.data'),
    dataDirExplicit: !!env.DATA_DIR,
  };
  config.razorpay.mode = /^rzp_live_/.test(config.razorpay.keyId) ? 'live' : /^rzp_test_/.test(config.razorpay.keyId) ? 'test' : 'unset';
  return config;
}

// What stops bookings opening (blocking), and what only delays Meta reporting (warnings).
// Never includes secret values.
function problems(config) {
  const blocking = [], warnings = [];
  if (!config.event) blocking.push('data/event.json is missing');
  else if (!(config.event.unitPricePaise > 0)) blocking.push('event price_inr is not a positive number');
  const k = config.testMode ? 'RAZORPAY_TEST_' : 'RAZORPAY_';
  if (!config.razorpay.keyId || !config.razorpay.keySecret) blocking.push(`${k}KEY_ID / ${k}KEY_SECRET not set`);
  if (!config.razorpay.webhookSecret) blocking.push(`${k}WEBHOOK_SECRET not set`);
  if (config.testMode && config.razorpay.mode !== 'test') blocking.push('TEST_MODE is on but RAZORPAY_TEST_KEY_ID is not a rzp_test_ key');
  if (config.testMode && !config.meta.testEventCode) blocking.push('TEST_MODE is on without META_TEST_EVENT_CODE: test sales would reach the real Meta reports');
  if (!config.db && !config.dataDirExplicit) blocking.push('no database: set DB_HOST, DB_USER, DB_PASSWORD and DB_NAME (or DATA_DIR on disk that survives redeploys)');
  if (!config.meta.accessToken) warnings.push('META_ACCESS_TOKEN not set: Purchase events wait until it is');
  if (!config.meta.datasetId) warnings.push('META_DATASET_ID not set: Purchase events wait until it is');
  if (config.razorpay.mode === 'live' && config.meta.testEventCode) warnings.push('live Razorpay keys with META_TEST_EVENT_CODE still set: Meta asks for it to be removed in production');
  return { blocking, warnings };
}

module.exports = { loadConfig, problems, ROOT };
