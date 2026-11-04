// Meta Conversions API: build and send one Purchase event per paid website booking.
// https://developers.facebook.com/docs/marketing-api/conversions-api/parameters
const crypto = require('crypto');

const sha256 = value => crypto.createHash('sha256').update(value, 'utf8').digest('hex');

// Razorpay fills this placeholder when a guest gives no email; it is not the guest's address.
const PLACEHOLDER_EMAILS = new Set(['void@razorpay.com']);

// Meta's normalisation: email trimmed and lower-cased; phone as digits only, with the country code.
function normaliseEmail(email) {
  const e = String(email || '').trim().toLowerCase();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e) && !PLACEHOLDER_EMAILS.has(e) ? e : null;
}
function normalisePhone(phone) {
  let d = String(phone || '').replace(/\D/g, '');
  if (d.length === 11 && d.startsWith('0')) d = d.slice(1);
  if (d.length === 10) d = '91' + d; // Indian numbers given without the country code
  return d.length >= 11 && d.length <= 15 ? d : null;
}
const hashEmail = email => { const e = normaliseEmail(email); return e ? sha256(e) : null; };
const hashPhone = phone => { const p = normalisePhone(phone); return p ? sha256(p) : null; };

// The event_id is fixed per booking, so however often it is sent, Meta keeps one Purchase.
const eventIdFor = booking => `purchase.${booking.id}`;

function purchaseEvent(booking, event) {
  // Personal identifiers only with the guest's consent. Bookings without it are never sent (see deliver in
  // app.js: Meta refuses an event it cannot match); the check here is a second guard.
  const userData = { client_user_agent: booking.userAgent || 'unknown' };
  if (booking.consent) {
    if (booking.emHash) userData.em = [booking.emHash];
    if (booking.phHash) userData.ph = [booking.phHash];
    if (booking.fbp) userData.fbp = booking.fbp;
    if (booking.fbc) userData.fbc = booking.fbc;
    if (booking.clientIp) userData.client_ip_address = booking.clientIp;
  }
  const value = booking.amountPaise / 100;
  return {
    event_name: 'Purchase',
    event_time: booking.paymentTime || Math.floor(booking.paidAt / 1000),
    event_id: eventIdFor(booking),
    action_source: 'website',
    event_source_url: event.sourceUrl,
    user_data: userData,
    custom_data: {
      currency: 'INR',
      value,
      order_id: booking.id,
      num_items: booking.quantity,
      content_type: 'product',
      content_name: event.itemName,
      content_ids: [event.itemId],
      contents: [{ id: event.itemId, quantity: booking.quantity, item_price: booking.unitPricePaise / 100 }],
    },
  };
}

class MetaError extends Error {
  constructor(message, { permanent, fbtraceId } = {}) { super(message); this.permanent = !!permanent; this.fbtraceId = fbtraceId; }
}

function createMeta({ accessToken, datasetId, apiVersion, testEventCode, apiBase }, fetchImpl = fetch) {
  return {
    configured: () => !!(accessToken && datasetId),
    async send(events) {
      const body = { data: events, access_token: accessToken };
      if (testEventCode) body.test_event_code = testEventCode;
      let res, json = null;
      try {
        res = await fetchImpl(`${apiBase}/${apiVersion}/${encodeURIComponent(datasetId)}/events`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body), // the token travels in the body, never in a URL that could be logged
          signal: AbortSignal.timeout(10000),
        });
        json = await res.json().catch(() => null);
      } catch (err) {
        throw new MetaError(`Meta request failed: ${err.message}`);
      }
      if (!res.ok || !json || json.error) {
        const e = json?.error || {};
        // 4xx other than rate limits means the request itself is wrong (token, parameters): retrying will not help.
        const permanent = res.status >= 400 && res.status < 500 && res.status !== 429 && ![4, 17, 32, 613].includes(e.code);
        throw new MetaError(`Meta ${res.status}: ${e.message || 'unexpected response'}${e.error_user_msg ? ' – ' + e.error_user_msg : ''}`,
          { permanent, fbtraceId: e.fbtrace_id });
      }
      return { eventsReceived: json.events_received, fbtraceId: json.fbtrace_id, messages: json.messages };
    },
  };
}

module.exports = { purchaseEvent, createMeta, MetaError, eventIdFor, hashEmail, hashPhone, normaliseEmail, normalisePhone, sha256 };
