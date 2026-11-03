// The booking API, mounted by server.js under /api/.
//
//   POST /api/bookings                 the carnival page asks for a payment link for n tickets
//   POST /api/webhooks/razorpay        Razorpay reports a paid, expired or cancelled link
//   GET  /api/health                   is the API up (no configuration details are exposed)
//
// A Purchase reaches Meta only after Razorpay's signed webhook says the link is paid and the amount,
// currency and booking all match what this server created. Website bookings are the only ones
// reported: links made in the Razorpay dashboard or QR payments are recognised and ignored.
const crypto = require('crypto');
const { problems } = require('./config');
const { verifyWebhookSignature } = require('./razorpay');
const { purchaseEvent, hashEmail, hashPhone } = require('./meta');
const { META_MAX_ATTEMPTS, META_WINDOW_MS } = require('./store');

const BOOKING_BODY_LIMIT = 4 * 1024;
const WEBHOOK_BODY_LIMIT = 1024 * 1024;
const SENDING_STALE_MS = 2 * 60 * 1000;
// Wait before retry n (1-based) after a failed Meta delivery.
const RETRY_DELAYS_MS = [0, 60e3, 5 * 60e3, 15 * 60e3, 30 * 60e3, 60 * 60e3, 2 * 3600e3, 4 * 3600e3];

class HttpError extends Error { constructor(status, code, message) { super(message || code); this.status = status; this.code = code; } }

function readBody(req, limit) {
  return new Promise((resolve, reject) => {
    const chunks = []; let size = 0;
    req.on('data', chunk => {
      size += chunk.length;
      if (size > limit) { reject(new HttpError(413, 'too_large')); req.destroy(); return; }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function sendJson(res, status, body, extra = {}) {
  const text = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
    'Content-Length': Buffer.byteLength(text), ...extra,
  });
  res.end(text);
}

function parseCookies(header) {
  const out = {};
  for (const part of String(header || '').split(';')) {
    const i = part.indexOf('=');
    if (i > 0) { try { out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim()); } catch { /* skip malformed */ } }
  }
  return out;
}

function clientIp(req, trustProxy) {
  const forwarded = trustProxy && String(req.headers['x-forwarded-for'] || '').split(',')[0].trim();
  const ip = forwarded || req.socket.remoteAddress || '';
  return ip.replace(/^::ffff:/, '').slice(0, 64) || null;
}

// Booking ids: readable, unguessable, and valid as a Razorpay reference_id (at most 40 characters).
const ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ';
function bookingId(now) {
  const bytes = crypto.randomBytes(10);
  let s = '';
  for (const b of bytes) s += ALPHABET[b % ALPHABET.length];
  return `SPH-${new Date(now).toISOString().slice(2, 10).replace(/-/g, '')}-${s}`;
}

const FBP = /^fb\.[0-2]\.\d{10,13}\.\d{1,30}$/;
const FBC = /^fb\.[0-2]\.\d{10,13}\.[\w-]{1,480}$/;
const FBCLID = /^[\w-]{1,480}$/;

// Fixed-window limits: per address, and for the whole site so a botnet cannot mint links without end.
function rateLimiter({ perIp = 10, global = 300, windowMs = 10 * 60e3 } = {}) {
  let windowStart = 0, total = 0, counts = new Map();
  return (ip, now) => {
    if (now - windowStart > windowMs) { windowStart = now; total = 0; counts = new Map(); }
    const n = (counts.get(ip) || 0) + 1;
    counts.set(ip, n); total += 1;
    return n <= perIp && total <= global;
  };
}

function createApi({ config, store, razorpay, meta, now = () => Date.now(), log = defaultLog, limiter = rateLimiter() }) {
  const issues = problems(config);
  const bookingsOpen = config.bookingsEnabled && issues.blocking.length === 0;
  const event = config.event;

  // ------------------------------------------------------------ POST /api/bookings
  async function createBooking(req, res) {
    const t = now();
    if (!bookingsOpen) throw new HttpError(503, 'bookings_unavailable');
    if (t > event.end) throw new HttpError(410, 'event_over');

    // Only the site's own pages may ask for links: browsers always send Origin on a POST fetch.
    const origin = req.headers.origin;
    if (!origin || !config.allowedOrigins.includes(origin)) throw new HttpError(403, 'origin_not_allowed');
    if (!/^application\/json\b/i.test(req.headers['content-type'] || '')) throw new HttpError(415, 'json_required');

    const ip = clientIp(req, config.trustProxy);
    if (!limiter(ip || 'unknown', t)) throw new HttpError(429, 'too_many_requests');

    let input;
    try { input = JSON.parse((await readBody(req, BOOKING_BODY_LIMIT)).toString('utf8')); } catch (e) { if (e instanceof HttpError) throw e; throw new HttpError(400, 'invalid_json'); }
    const quantity = input?.quantity;
    if (typeof quantity !== 'number' || !Number.isInteger(quantity) || quantity < 1 || quantity > event.maxPerBooking) throw new HttpError(400, 'invalid_quantity');
    const consent = input.consent === true;

    if (event.websiteTicketLimit != null) {
      const taken = await store.countActiveTickets(event.slug, t);
      if (taken + quantity > event.websiteTicketLimit) throw new HttpError(409, 'sold_out');
    }

    // Meta's browser identifiers, read from the first-party cookies the pixel sets. Kept only with consent.
    let fbp = null, fbc = null;
    if (consent) {
      const cookies = parseCookies(req.headers.cookie);
      if (FBP.test(cookies._fbp || '')) fbp = cookies._fbp;
      if (FBC.test(cookies._fbc || '')) fbc = cookies._fbc;
      else if (typeof input.fbclid === 'string' && FBCLID.test(input.fbclid)) fbc = `fb.1.${t}.${input.fbclid}`;
    }

    // The price always comes from data/event.json on the server, never from the browser.
    const expiresAt = t + config.bookingTtlMinutes * 60e3;
    const booking = await store.insertBooking({
      id: bookingId(t), eventSlug: event.slug, quantity, unitPricePaise: event.unitPricePaise,
      amountPaise: event.unitPricePaise * quantity, consent, fbp, fbc,
      clientIp: consent ? ip : null, userAgent: String(req.headers['user-agent'] || '').slice(0, 512) || null,
      createdAt: t, expiresAt,
    });

    let link;
    try {
      link = await razorpay.createPaymentLink({ booking, event, expiresAt });
    } catch (err) {
      await store.markFailed(booking.id);
      log('error', 'payment_link_failed', { booking: booking.id, error: err.message });
      throw new HttpError(502, 'payment_link_failed');
    }
    await store.attachPaymentLink(booking.id, link.id, link.short_url);
    log('info', 'booking_created', { booking: booking.id, quantity, consent, link: link.id });
    sendJson(res, 201, { bookingId: booking.id, url: link.short_url, amount: booking.amountPaise / 100, currency: 'INR' });
  }

  // ------------------------------------------------------------ POST /api/webhooks/razorpay
  async function webhook(req, res) {
    const raw = await readBody(req, WEBHOOK_BODY_LIMIT);
    if (!verifyWebhookSignature(raw, req.headers['x-razorpay-signature'], config.razorpay.webhookSecret)) {
      log('warn', 'webhook_bad_signature', { ip: clientIp(req, config.trustProxy) });
      throw new HttpError(400, 'invalid_signature');
    }
    let body;
    try { body = JSON.parse(raw.toString('utf8')); } catch { throw new HttpError(400, 'invalid_json'); }
    const eventId = String(req.headers['x-razorpay-event-id'] || '').slice(0, 64) ||
      crypto.createHash('sha256').update(raw).digest('hex').slice(0, 64);

    const seen = await store.recordWebhookEvent(eventId, String(body.event || '').slice(0, 64), now());
    if (seen && seen !== 'processing' && seen !== 'error') { sendJson(res, 200, { ok: true, duplicate: true }); return; }

    let result;
    try {
      result = await handleEvent(body);
    } catch (err) {
      await store.finishWebhookEvent(eventId, 'error');
      throw err; // 500: Razorpay retries, and every step below is safe to repeat
    }
    await store.finishWebhookEvent(eventId, result.outcome);
    sendJson(res, 200, { ok: true, outcome: result.outcome });
    if (result.bookingId) setImmediate(() => deliver(result.bookingId).catch(err => log('error', 'meta_deliver_crash', { error: err.message })));
  }

  async function handleEvent(body) {
    const type = body.event;
    const linkEntity = body.payload?.payment_link?.entity;
    if (!linkEntity?.id) return { outcome: 'ignored' };
    const booking = await store.getBookingByLink(linkEntity.id);
    // Links created in the dashboard (for WhatsApp) also fire these events; only ours are website sales.
    if (!booking || linkEntity.notes?.source !== 'website' || linkEntity.reference_id !== booking.id) {
      return { outcome: 'not_website_booking' };
    }

    if (type === 'payment_link.expired' || type === 'payment_link.cancelled') {
      await store.markClosed(linkEntity.id, type === 'payment_link.expired' ? 'expired' : 'cancelled');
      log('info', 'booking_closed', { booking: booking.id, event: type });
      return { outcome: 'closed' };
    }
    if (type !== 'payment_link.paid') return { outcome: 'ignored' };

    const payment = body.payload?.payment?.entity || {};
    // Reconcile what Razorpay says was paid with what this server asked for.
    const mismatch = [
      linkEntity.status !== 'paid' && 'link status',
      payment.status !== 'captured' && 'payment status',
      (linkEntity.currency !== 'INR' || payment.currency !== 'INR') && 'currency',
      Number(linkEntity.amount) !== booking.amountPaise && 'link amount',
      Number(linkEntity.amount_paid) !== booking.amountPaise && 'amount paid',
      !(Number(payment.amount) >= booking.amountPaise) && 'payment amount',
    ].filter(Boolean);

    const paid = {
      status: mismatch.length ? 'review' : 'paid',
      paymentId: payment.id || null,
      paidAt: now(),
      paymentTime: Number(payment.created_at) || Math.floor(now() / 1000),
      emHash: hashEmail(payment.email),
      phHash: hashPhone(payment.contact),
      metaStatus: mismatch.length ? 'skipped' : 'pending',
      metaLastError: mismatch.length ? `not sent: ${mismatch.join(', ')} did not match` : null,
    };
    const changed = await store.markPaid(booking.id, paid);
    if (mismatch.length) {
      log('error', 'payment_mismatch', { booking: booking.id, payment: payment.id, mismatch });
      return { outcome: 'review' };
    }
    if (changed) log('info', 'booking_paid', { booking: booking.id, payment: payment.id, quantity: booking.quantity, amount: booking.amountPaise / 100 });
    return { outcome: changed ? 'paid' : 'already_paid', bookingId: booking.id };
  }

  // ------------------------------------------------------------ Meta delivery
  async function deliver(id) {
    if (!meta.configured()) return 'waiting_for_meta_config';
    const t = now();
    const booking = await store.claimMeta(id, t, SENDING_STALE_MS);
    if (!booking) return 'not_claimed';
    if (booking.paymentTime && booking.paymentTime * 1000 < t - META_WINDOW_MS) {
      await store.finishMeta(id, { status: 'expired', error: 'older than Meta accepts (7 days)' });
      log('error', 'meta_expired', { booking: id });
      return 'expired';
    }
    try {
      const result = await meta.send([purchaseEvent(booking, event)]);
      await store.finishMeta(id, { status: 'sent', fbtraceId: result.fbtraceId });
      log('info', 'meta_purchase_sent', { booking: id, eventsReceived: result.eventsReceived, fbtrace: result.fbtraceId, test: !!config.meta.testEventCode });
      return 'sent';
    } catch (err) {
      const last = booking.metaAttempts >= META_MAX_ATTEMPTS;
      await store.finishMeta(id, { status: last ? 'abandoned' : 'failed', error: err.message, fbtraceId: err.fbtraceId });
      log('error', 'meta_purchase_failed', { booking: id, attempt: booking.metaAttempts, permanent: !!err.permanent, error: err.message, fbtrace: err.fbtraceId });
      return 'failed';
    }
  }

  // Retries anything not yet delivered (Meta down, token not yet set, a crash mid-send), with backoff.
  async function sweep({ ignoreBackoff = false } = {}) {
    const t = now();
    const due = await store.listMetaDue(t, SENDING_STALE_MS, 50);
    let sent = 0;
    for (const id of due) {
      const b = await store.getBooking(id);
      if (!ignoreBackoff && b.metaStatus === 'failed' && b.metaLastAttemptAt + (RETRY_DELAYS_MS[b.metaAttempts] ?? RETRY_DELAYS_MS.at(-1)) > t) continue;
      if ((await deliver(id)) === 'sent') sent += 1;
    }
    // Anything Meta can no longer accept: mark it, which also deletes the identifiers kept for it.
    for (const u of await store.listUnfinishedMeta(t)) {
      if (u.paymentTime && u.paymentTime * 1000 < t - META_WINDOW_MS) await store.finishMeta(u.id, { status: 'expired', error: 'older than Meta accepts (7 days)' });
    }
    return { due: due.length, sent };
  }

  // ------------------------------------------------------------ routing
  const routes = {
    'POST /api/bookings': createBooking,
    'POST /api/webhooks/razorpay': webhook,
    'GET /api/health': (req, res) => sendJson(res, 200, { ok: true, bookings: bookingsOpen ? 'open' : 'closed' }),
    'HEAD /api/health': (req, res) => sendJson(res, 200, {}),
  };

  async function handle(req, res, pathname) {
    const route = routes[`${req.method} ${pathname.replace(/\/+$/, '')}`];
    try {
      if (!route) {
        const known = Object.keys(routes).some(k => k.endsWith(' ' + pathname.replace(/\/+$/, '')));
        throw new HttpError(known ? 405 : 404, known ? 'method_not_allowed' : 'not_found');
      }
      await route(req, res);
    } catch (err) {
      const status = err instanceof HttpError ? err.status : 500;
      if (status === 500) log('error', 'api_error', { path: pathname, error: err.message });
      if (!res.headersSent) sendJson(res, status, { error: err instanceof HttpError ? err.code : 'server_error' });
    }
  }

  return { handle, deliver, sweep, handleEvent, bookingsOpen, issues };
}

// One JSON line per event: easy to read in Hostinger's logs. Callers never pass secrets or raw personal data.
function defaultLog(level, msg, fields = {}) {
  const line = JSON.stringify({ t: new Date().toISOString(), level, msg, ...fields });
  (level === 'error' || level === 'warn' ? console.error : console.log)(line);
}

module.exports = { createApi, rateLimiter, parseCookies, bookingId, HttpError, defaultLog };
