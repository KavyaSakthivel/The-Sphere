// Razorpay: create one Payment Link per website booking, and verify webhook signatures.
// Card and UPI details never touch this server; guests pay on Razorpay's hosted checkout.
const crypto = require('crypto');

// Razorpay signs the exact raw request body with the webhook secret (HMAC-SHA256, hex).
// Compare in constant time, and on the raw bytes, never on re-serialised JSON.
function verifyWebhookSignature(rawBody, signature, secret) {
  if (!secret || typeof signature !== 'string' || !/^[0-9a-f]{64}$/i.test(signature)) return false;
  const expected = crypto.createHmac('sha256', secret).update(rawBody).digest();
  const given = Buffer.from(signature, 'hex');
  return given.length === expected.length && crypto.timingSafeEqual(given, expected);
}

class RazorpayError extends Error {
  constructor(message, status, detail) { super(message); this.status = status; this.detail = detail; }
}

function createRazorpay({ keyId, keySecret, apiBase }, fetchImpl = fetch) {
  const auth = 'Basic ' + Buffer.from(`${keyId}:${keySecret}`).toString('base64');

  async function call(method, path, body) {
    const res = await fetchImpl(apiBase + path, {
      method,
      headers: { Authorization: auth, 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(10000),
    });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch { /* keep text for the error */ }
    if (!res.ok) {
      const description = json?.error?.description || text.slice(0, 200);
      throw new RazorpayError(`Razorpay ${method} ${path} failed (${res.status}): ${description}`, res.status, json?.error);
    }
    return json;
  }

  return {
    // https://razorpay.com/docs/api/payments/payment-links/create-standard/
    createPaymentLink({ booking, event, expiresAt }) {
      return call('POST', '/payment_links', {
        amount: booking.amountPaise,
        currency: 'INR',
        accept_partial: false,
        reference_id: booking.id,
        description: `${event.name}: ${booking.quantity} × Entry ticket`.slice(0, 2048),
        expire_by: Math.floor(expiresAt / 1000),
        reminder_enable: false,
        notify: { sms: false, email: false },
        // Notes come back in every webhook and show in the dashboard, so they tell website sales apart from
        // links sent on WhatsApp. They hold no personal data.
        notes: { source: 'website', booking_id: booking.id, quantity: String(booking.quantity), event: event.slug },
      });
    },
    fetchPaymentLink(id) { return call('GET', `/payment_links/${encodeURIComponent(id)}`); },
    fetchPayment(id) { return call('GET', `/payments/${encodeURIComponent(id)}`); },
  };
}

module.exports = { verifyWebhookSignature, createRazorpay, RazorpayError };
