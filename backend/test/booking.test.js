// End-to-end tests of the booking backend over real HTTP, with Razorpay and Meta replaced by fakes.
// Run: npm test. Against MySQL too: TEST_DB_HOST=127.0.0.1 TEST_DB_PORT=3306 TEST_DB_USER=root TEST_DB_NAME=sphere npm test
const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const crypto = require('crypto');
const { loadConfig } = require('../config');
const { FileStore, MySqlStore } = require('../store');
const { createApi, rateLimiter } = require('../app');
const { verifyWebhookSignature } = require('../razorpay');
const { createMeta, hashEmail, hashPhone, normalisePhone, sha256 } = require('../meta');

const WEBHOOK_SECRET = 'whsec_test_123';
const ORIGIN = 'https://spherewellness.in';
const NOW = Date.parse('2026-11-10T10:00:00+05:30');
const FBP = 'fb.1.1762740000000.1234567890';
const FBC = 'fb.1.1762740000000.IwAR0abcDEF';

function setup({ env = {}, metaFails = 0, metaPermanent = false, limiter } = {}) {
  const config = loadConfig({
    BOOKINGS_ENABLED: 'true', RAZORPAY_KEY_ID: 'rzp_test_abc', RAZORPAY_KEY_SECRET: 'secret', RAZORPAY_WEBHOOK_SECRET: WEBHOOK_SECRET,
    META_ACCESS_TOKEN: 'EAAtoken', META_TEST_EVENT_CODE: 'TEST123', DATA_DIR: '', ...env,
  });
  config.dataDir = null; config.dataDirExplicit = true;
  const store = process.env.TEST_DB_HOST
    ? new MySqlStore({ host: process.env.TEST_DB_HOST, port: Number(process.env.TEST_DB_PORT || 3306), user: process.env.TEST_DB_USER,
      password: process.env.TEST_DB_PASSWORD || '', database: process.env.TEST_DB_NAME })
    : new FileStore(null);
  const links = [];
  const razorpay = {
    async createPaymentLink({ booking, expiresAt }) {
      const link = { id: `plink_${links.length + 1}`, short_url: `https://rzp.io/rzp/x${links.length + 1}`, booking, expiresAt };
      links.push(link);
      return link;
    },
  };
  const metaCalls = [];
  let failuresLeft = metaFails;
  const fakeFetch = async (url, init) => {
    metaCalls.push({ url, body: JSON.parse(init.body) });
    if (failuresLeft > 0) {
      failuresLeft -= 1;
      return new Response(JSON.stringify({ error: { message: 'boom', code: metaPermanent ? 100 : 2, fbtrace_id: 'T1' } }), { status: metaPermanent ? 400 : 500 });
    }
    return new Response(JSON.stringify({ events_received: 1, fbtrace_id: 'TRACE' }), { status: 200 });
  };
  const meta = createMeta(config.meta, fakeFetch);
  let clock = NOW;
  const logs = [];
  const api = createApi({ config, store, razorpay, meta, now: () => clock, log: (level, msg, f) => logs.push({ level, msg, ...f }), limiter });
  const server = http.createServer((req, res) => api.handle(req, res, new URL(req.url, 'http://x').pathname));
  return {
    config, store, links, metaCalls, api, logs, server,
    tick: ms => { clock += ms; },
    async listen() {
      await store.init();
      if (store.kind === 'mysql') { await store.q('DELETE FROM bookings', []); await store.q('DELETE FROM webhook_events', []); }
      await new Promise(r => server.listen(0, '127.0.0.1', r)); this.base = `http://127.0.0.1:${server.address().port}`; },
    async close() { await new Promise(r => server.close(r)); await store.close(); },
  };
}

async function book(t, body, { origin = ORIGIN, cookie = '', ua = 'Mozilla/5.0 Test' } = {}) {
  const headers = { 'Content-Type': 'application/json', 'User-Agent': ua, 'X-Forwarded-For': '203.0.113.7, 10.0.0.1' };
  if (origin) headers.Origin = origin;
  if (cookie) headers.Cookie = cookie;
  const res = await fetch(t.base + '/api/bookings', { method: 'POST', headers, body: JSON.stringify(body) });
  return { status: res.status, body: await res.json() };
}

function paidEvent(link, booking, overrides = {}) {
  const amount = booking.amountPaise;
  return {
    entity: 'event', event: 'payment_link.paid', contains: ['payment_link', 'order', 'payment'],
    payload: {
      payment_link: { entity: { id: link.id, amount, amount_paid: amount, currency: 'INR', status: 'paid', reference_id: booking.id,
        notes: { source: 'website', booking_id: booking.id, quantity: String(booking.quantity) }, ...overrides.link } },
      payment: { entity: { id: `pay_${link.id}`, amount, currency: 'INR', status: 'captured', email: ' Guest@Example.COM ',
        contact: '+91 98431 33380', created_at: Math.floor(NOW / 1000), ...overrides.payment } },
      order: { entity: { id: 'order_1', amount, status: 'paid' } },
    },
    created_at: Math.floor(NOW / 1000),
  };
}

async function webhook(t, payload, { eventId = crypto.randomUUID(), secret = WEBHOOK_SECRET, tamper = false } = {}) {
  const raw = JSON.stringify(payload);
  const signature = crypto.createHmac('sha256', secret).update(raw).digest('hex');
  const res = await fetch(t.base + '/api/webhooks/razorpay', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': signature, 'X-Razorpay-Event-Id': eventId },
    body: tamper ? raw.replace('"captured"', '"failed"') : raw,
  });
  return { status: res.status, body: await res.json() };
}

const settle = () => new Promise(r => setTimeout(r, 30)); // lets the post-response Meta delivery run

// ---------------------------------------------------------------- units

test('webhook signature: valid, wrong secret, tampered, malformed', () => {
  const raw = Buffer.from('{"a":1}');
  const sig = crypto.createHmac('sha256', 's3cret').update(raw).digest('hex');
  assert.equal(verifyWebhookSignature(raw, sig, 's3cret'), true);
  assert.equal(verifyWebhookSignature(raw, sig, 'other'), false);
  assert.equal(verifyWebhookSignature(Buffer.from('{"a":2}'), sig, 's3cret'), false);
  assert.equal(verifyWebhookSignature(raw, 'zz', 's3cret'), false);
  assert.equal(verifyWebhookSignature(raw, undefined, 's3cret'), false);
  assert.equal(verifyWebhookSignature(raw, sig, ''), false);
});

test('Meta normalisation and hashing', () => {
  assert.equal(hashEmail(' Guest@Example.COM '), sha256('guest@example.com'));
  assert.equal(hashEmail('void@razorpay.com'), null);
  assert.equal(hashEmail('not-an-email'), null);
  assert.equal(normalisePhone('+91 98431 33380'), '919843133380');
  assert.equal(normalisePhone('9843133380'), '919843133380');
  assert.equal(normalisePhone('09843133380'), '919843133380');
  assert.equal(normalisePhone('123'), null);
  assert.equal(hashPhone('98431-33380'), sha256('919843133380'));
});

test('rate limiter: per address and in total', () => {
  const limit = rateLimiter({ perIp: 2, global: 3, windowMs: 1000 });
  assert.deepEqual([limit('a', 0), limit('a', 1), limit('a', 2)], [true, true, false]);
  assert.equal(limit('b', 3), false); // global budget of 3 used up
  assert.equal(limit('a', 2000), true); // new window
});

// ---------------------------------------------------------------- bookings

test('booking: price comes from the server, link per booking, consent gates identifiers', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 2, consent: true, amount: 1 }, { cookie: `_fbp=${FBP}; _fbc=${FBC}` });
    assert.equal(r.status, 201);
    assert.equal(r.body.amount, 5798);
    assert.match(r.body.url, /^https:\/\/rzp\.io\//);
    assert.match(r.body.bookingId, /^SPH-\d{6}-[2-9A-Z]{10}$/);
    const b = await t.store.getBooking(r.body.bookingId);
    assert.equal(b.amountPaise, 579800);
    assert.equal(b.fbp, FBP); assert.equal(b.fbc, FBC);
    assert.equal(b.clientIp, '203.0.113.7');
    assert.equal(b.expiresAt, NOW + 20 * 60e3);

    const noConsent = await book(t, { quantity: 1, consent: false }, { cookie: `_fbp=${FBP}; _fbc=${FBC}` });
    const nb = await t.store.getBooking(noConsent.body.bookingId);
    assert.equal(nb.fbp, null); assert.equal(nb.fbc, null); assert.equal(nb.clientIp, null);

    const fromClick = await book(t, { quantity: 1, consent: true, fbclid: 'IwAR123' });
    assert.equal((await t.store.getBooking(fromClick.body.bookingId)).fbc, `fb.1.${NOW}.IwAR123`);

    const badCookie = await book(t, { quantity: 1, consent: true }, { cookie: '_fbp=<script>' });
    assert.equal((await t.store.getBooking(badCookie.body.bookingId)).fbp, null);
  } finally { await t.close(); }
});

test('booking: rejects bad input, other sites, closed bookings, sold out, finished event', async () => {
  const t = setup(); await t.listen();
  try {
    for (const quantity of [0, -1, 1.5, '2', 11, null]) assert.equal((await book(t, { quantity })).status, 400, String(quantity));
    assert.equal((await book(t, { quantity: 1 }, { origin: 'https://evil.example' })).status, 403);
    assert.equal((await book(t, { quantity: 1 }, { origin: null })).status, 403);
    const res = await fetch(t.base + '/api/bookings', { method: 'POST', headers: { Origin: ORIGIN, 'Content-Type': 'text/plain' }, body: '{}' });
    assert.equal(res.status, 415);
    assert.equal((await fetch(t.base + '/api/bookings')).status, 405);
    assert.equal((await fetch(t.base + '/api/nope')).status, 404);
  } finally { await t.close(); }

  const closed = setup({ env: { BOOKINGS_ENABLED: 'false' } }); await closed.listen();
  try { assert.equal((await book(closed, { quantity: 1 })).status, 503); } finally { await closed.close(); }

  const noKeys = setup({ env: { RAZORPAY_WEBHOOK_SECRET: '' } }); await noKeys.listen();
  try { assert.equal((await book(noKeys, { quantity: 1 })).status, 503); } finally { await noKeys.close(); }
  const { loadConfig: load, problems } = require('../config');
  assert.match(problems(load({ BOOKINGS_ENABLED: 'true' })).blocking.join(), /no database/);
  assert.doesNotMatch(problems(load({ DB_HOST: 'db' })).blocking.join(), /no database/);

  const limited = setup(); limited.config.event.websiteTicketLimit = 3; await limited.listen();
  try {
    assert.equal((await book(limited, { quantity: 2 })).status, 201);
    assert.equal((await book(limited, { quantity: 2 })).status, 409);
    limited.tick(21 * 60e3); // the first link expired unpaid, so its tickets are free again
    assert.equal((await book(limited, { quantity: 2 })).status, 201);
  } finally { await limited.close(); }

  const over = setup(); over.tick(60 * 24 * 3600e3); await over.listen();
  try { assert.equal((await book(over, { quantity: 1 })).status, 410); } finally { await over.close(); }

  const throttled = setup({ limiter: rateLimiter({ perIp: 1 }) }); await throttled.listen();
  try {
    assert.equal((await book(throttled, { quantity: 1 })).status, 201);
    assert.equal((await book(throttled, { quantity: 1 })).status, 429);
  } finally { await throttled.close(); }
});

// ---------------------------------------------------------------- webhook to Meta

for (const quantity of [1, 2, 3]) {
  test(`paid webhook sends one Purchase for ${quantity} ticket(s) with the real amount`, async () => {
    const t = setup(); await t.listen();
    try {
      const r = await book(t, { quantity, consent: true }, { cookie: `_fbp=${FBP}; _fbc=${FBC}` });
      const booking = await t.store.getBooking(r.body.bookingId);
      const w = await webhook(t, paidEvent(t.links[0], booking));
      assert.deepEqual(w, { status: 200, body: { ok: true, outcome: 'paid' } });
      await settle();

      assert.equal(t.metaCalls.length, 1);
      const { url, body } = t.metaCalls[0];
      assert.equal(url, 'https://graph.facebook.com/v24.0/1150068800700841/events');
      assert.equal(body.test_event_code, 'TEST123');
      assert.equal(body.access_token, 'EAAtoken');
      const [e] = body.data;
      assert.equal(e.event_name, 'Purchase');
      assert.equal(e.event_id, `purchase.${booking.id}`);
      assert.equal(e.action_source, 'website');
      assert.equal(e.event_source_url, 'https://spherewellness.in/carnival/');
      assert.equal(e.event_time, Math.floor(NOW / 1000));
      assert.deepEqual(e.custom_data, {
        currency: 'INR', value: 2899 * quantity, order_id: booking.id, num_items: quantity, content_type: 'product',
        content_name: 'The Sphere Wellness Carnival – Entry ticket', content_ids: ['carnival-entry'],
        contents: [{ id: 'carnival-entry', quantity, item_price: 2899 }],
      });
      assert.deepEqual(e.user_data, {
        client_user_agent: 'Mozilla/5.0 Test', em: [sha256('guest@example.com')], ph: [sha256('919843133380')],
        fbp: FBP, fbc: FBC, client_ip_address: '203.0.113.7',
      });

      const after = await t.store.getBooking(booking.id);
      assert.equal(after.status, 'paid');
      assert.equal(after.metaStatus, 'sent');
      assert.equal(after.paymentId, `pay_${t.links[0].id}`);
      // Identifiers are deleted once Meta has the event.
      assert.deepEqual([after.fbp, after.fbc, after.clientIp, after.emHash, after.phHash], [null, null, null, null, null]);
      assert.deepEqual((await t.store.stats('carnival')).ticketsPaid, quantity);
    } finally { await t.close(); }
  });
}

test('without consent Meta gets the sale but no personal identifiers', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 1, consent: false }, { cookie: `_fbp=${FBP}` });
    await webhook(t, paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId)));
    await settle();
    assert.deepEqual(t.metaCalls[0].body.data[0].user_data, { client_user_agent: 'Mozilla/5.0 Test' });
    assert.equal(t.metaCalls[0].body.data[0].custom_data.value, 2899);
  } finally { await t.close(); }
});

test('duplicate and concurrent webhooks give exactly one Purchase', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 2, consent: true });
    const payload = paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId));
    const first = await webhook(t, payload, { eventId: 'evt_1' });
    const again = await webhook(t, payload, { eventId: 'evt_1' });
    assert.equal(first.body.outcome, 'paid');
    assert.equal(again.body.duplicate, true);
    // Same payment, different delivery ids, all at once.
    const burst = await Promise.all([1, 2, 3, 4, 5].map(i => webhook(t, payload, { eventId: `evt_x${i}` })));
    assert.ok(burst.every(b => b.status === 200 && b.body.outcome === 'already_paid'));
    await settle();
    await t.api.sweep({ ignoreBackoff: true });
    assert.equal(t.metaCalls.length, 1);
  } finally { await t.close(); }
});

test('signature failures are rejected and change nothing', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 1, consent: true });
    const payload = paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId));
    assert.equal((await webhook(t, payload, { secret: 'wrong' })).status, 400);
    assert.equal((await webhook(t, payload, { tamper: true })).status, 400);
    const unsigned = await fetch(t.base + '/api/webhooks/razorpay', { method: 'POST', body: JSON.stringify(payload) });
    assert.equal(unsigned.status, 400);
    await settle();
    assert.equal((await t.store.getBooking(r.body.bookingId)).status, 'created');
    assert.equal(t.metaCalls.length, 0);
  } finally { await t.close(); }
});

test('links made outside the website (WhatsApp, dashboard) are ignored', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 1 });
    const booking = await t.store.getBooking(r.body.bookingId);
    const foreign = paidEvent({ id: 'plink_dashboard' }, booking, { link: { notes: {}, reference_id: '' } });
    assert.equal((await webhook(t, foreign)).body.outcome, 'not_website_booking');
    // Our link id but notes stripped: still not trusted as a website sale.
    const stripped = paidEvent(t.links[0], booking, { link: { notes: {} } });
    assert.equal((await webhook(t, stripped)).body.outcome, 'not_website_booking');
    assert.equal((await webhook(t, { event: 'payment.captured', payload: { payment: { entity: {} } } })).body.outcome, 'ignored');
    await settle();
    assert.equal(t.metaCalls.length, 0);
  } finally { await t.close(); }
});

test('amount, currency or status mismatches are held for review, never sent', async () => {
  for (const overrides of [
    { link: { amount_paid: 100 } }, { link: { amount: 100, amount_paid: 100 } }, { payment: { currency: 'USD' } },
    { payment: { status: 'authorized' } }, { link: { status: 'partially_paid' } },
  ]) {
    const t = setup(); await t.listen();
    try {
      const r = await book(t, { quantity: 2, consent: true });
      const w = await webhook(t, paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId), overrides));
      assert.equal(w.body.outcome, 'review', JSON.stringify(overrides));
      await settle();
      const b = await t.store.getBooking(r.body.bookingId);
      assert.equal(b.status, 'review'); assert.equal(b.metaStatus, 'skipped');
      assert.equal(t.metaCalls.length, 0);
    } finally { await t.close(); }
  }
});

test('Meta outage: retried with backoff until delivered', async () => {
  const t = setup({ metaFails: 2 }); await t.listen();
  try {
    const r = await book(t, { quantity: 3, consent: true });
    await webhook(t, paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId)));
    await settle();
    let b = await t.store.getBooking(r.body.bookingId);
    assert.equal(b.metaStatus, 'failed'); assert.equal(b.metaAttempts, 1);
    assert.ok(b.emHash, 'identifiers kept for the retry');

    await t.api.sweep(); // too soon: backoff
    assert.equal(t.metaCalls.length, 1);
    t.tick(61e3); await t.api.sweep(); // second attempt fails
    t.tick(5 * 60e3 + 1); await t.api.sweep(); // third succeeds
    b = await t.store.getBooking(r.body.bookingId);
    assert.equal(b.metaStatus, 'sent'); assert.equal(t.metaCalls.length, 3);
    assert.equal(new Set(t.metaCalls.map(c => c.body.data[0].event_id)).size, 1, 'same event_id every time');
  } finally { await t.close(); }
});

test('Purchases older than Meta accepts are marked expired and their identifiers deleted', async () => {
  const t = setup({ metaFails: 99, metaPermanent: true }); await t.listen();
  try {
    const r = await book(t, { quantity: 1, consent: true });
    await webhook(t, paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId)));
    await settle();
    t.tick(8 * 24 * 3600e3);
    await t.api.sweep();
    const b = await t.store.getBooking(r.body.bookingId);
    assert.equal(b.metaStatus, 'expired'); assert.equal(b.emHash, null);
  } finally { await t.close(); }
});

test('expired and cancelled links release the booking', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 2 });
    const booking = await t.store.getBooking(r.body.bookingId);
    const payload = paidEvent(t.links[0], booking);
    payload.event = 'payment_link.expired';
    payload.payload.payment_link.entity.status = 'expired';
    assert.equal((await webhook(t, payload)).body.outcome, 'closed');
    assert.equal((await t.store.getBooking(booking.id)).status, 'expired');
    // A payment that still lands for it (paid in the last second) is honoured.
    assert.equal((await webhook(t, paidEvent(t.links[0], booking))).body.outcome, 'paid');
  } finally { await t.close(); }
});

test('Meta not configured yet: bookings still work and the Purchase waits', async () => {
  const t = setup({ env: { META_ACCESS_TOKEN: '' } }); await t.listen();
  try {
    const r = await book(t, { quantity: 1, consent: true });
    assert.equal(r.status, 201, 'bookings work without Meta');
    await webhook(t, paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId)));
    await settle();
    assert.equal((await t.store.getBooking(r.body.bookingId)).metaStatus, 'pending');
    assert.equal(t.metaCalls.length, 0);
  } finally { await t.close(); }
});

test('server.js serves the site and mounts the API', async () => {
  process.env.SPHERE_NO_LISTEN = '1';
  process.env.DATA_DIR = require('fs').mkdtempSync(require('path').join(require('os').tmpdir(), 'sphere-'));
  const { server, backend } = require('../../server');
  await backend.ready;
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    const home = await fetch(base + '/');
    assert.equal(home.status, 200);
    assert.match(await home.text(), /The Sphere/);
    const health = await fetch(base + '/api/health');
    assert.equal(health.status, 200);
    assert.equal((await health.json()).ok, true);
    assert.equal((await fetch(base + '/api/webhooks/razorpay', { method: 'POST', body: '{}' })).status, 400);
    assert.equal((await fetch(base + '/style.css', { method: 'POST' })).status, 405);
  } finally { await new Promise(r => server.close(r)); }
});
