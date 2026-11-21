// End-to-end tests of the booking backend over real HTTP, with Razorpay and Meta replaced by fakes.
// Run: npm test. Against MySQL too: TEST_DB_HOST=127.0.0.1 TEST_DB_PORT=3306 TEST_DB_USER=root TEST_DB_NAME=sphere npm test
const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const crypto = require('crypto');
const { loadConfig } = require('../config');
const { FileStore, MySqlStore } = require('../store');
const { createApi, rateLimiter } = require('../app');
const { verifyWebhookSignature, RazorpayError } = require('../razorpay');
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
  // A fake Razorpay as strict as the real one: each reference_id is accepted once, expire_by must be at least
  // 15 minutes ahead, and links can be looked up by reference. `rz.next` scripts the next create call:
  // 'lost' creates the link but the answer never arrives; 'down' fails before anything is created.
  const links = [];
  const rz = { next: [], lookups: 0, creates: 0 };
  const razorpay = {
    async createPaymentLink({ booking, expiresAt }) {
      rz.creates += 1;
      const mode = rz.next.shift();
      if (mode === 'down') throw new TypeError('fetch failed');
      if (mode === 'refuse') throw new RazorpayError('Razorpay POST /payment_links failed (400): The amount is invalid', 400);
      if (links.some(l => l.reference_id === booking.id)) throw new RazorpayError('Razorpay POST /payment_links failed (400): payment link with given reference_id already exists', 400);
      if (Math.floor(expiresAt / 1000) < Math.floor(clock / 1000) + 15 * 60) throw new RazorpayError('Razorpay POST /payment_links failed (400): expire_by should be at least 15 minutes in the future', 400);
      const n = links.length + 1;
      const link = { id: `plink_Fake${String(n).padStart(8, "0")}`, short_url: `https://rzp.io/rzp/x${n}`, booking, expiresAt, reference_id: booking.id,
        amount: booking.amountPaise, currency: 'INR', status: 'created', expire_by: Math.floor(expiresAt / 1000), notes: { source: 'website', booking_id: booking.id } };
      links.push(link);
      if (mode === 'lost') { const e = new Error('The operation was aborted due to timeout'); e.name = 'TimeoutError'; throw e; }
      return link;
    },
    async findPaymentLinksByReference(ref) { rz.lookups += 1; return links.filter(l => l.reference_id === ref); },
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
    config, store, links, rz, metaCalls, api, logs, server,
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

test('without consent the booking is paid but nothing is sent to Meta, even on retry', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 1, consent: false }, { cookie: `_fbp=${FBP}` });
    await webhook(t, paidEvent(t.links[0], await t.store.getBooking(r.body.bookingId)));
    await settle();
    await t.api.sweep({ ignoreBackoff: true });
    const b = await t.store.getBooking(r.body.bookingId);
    assert.equal(b.status, 'paid');
    assert.equal(b.metaStatus, 'skipped');
    assert.equal(b.fbp, null);
    assert.equal(t.metaCalls.length, 0);
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

test('requests that arrive while the app is still starting wait for it, within a limit', async () => {
  const { startBackend } = require('../index');
  const env = { DATA_DIR: require('fs').mkdtempSync(require('path').join(require('os').tmpdir(), 'sphere-')) };
  const serve = backend => http.createServer((req, res) => backend.handle(req, res, new URL(req.url, 'http://x').pathname));
  const get = async server => {
    await new Promise(r => server.listen(0, '127.0.0.1', r));
    try { return (await fetch(`http://127.0.0.1:${server.address().port}/api/health`)).status; }
    finally { await new Promise(r => server.close(r)); }
  };
  // A database that takes a moment to connect (Hostinger waking an idle app): answered once it is ready.
  const slow = startBackend(env, { storeInit: store => new Promise(r => setTimeout(r, 300)).then(() => store.init()) });
  assert.equal(await get(serve(slow)), 200);
  // One that never connects: refused after the wait, and the page falls back to the shared link.
  const stuck = startBackend(env, { startupWaitMs: 50, storeInit: () => new Promise(() => {}) });
  assert.equal(await get(serve(stuck)), 503);
});

// ---------------------------------------------------------------- retry keys

const statuses = async t => (await t.store.stats(t.config.event.slug)).bookings;

test('retry key: a link created but its answer lost is found again, not made twice', async () => {
  const t = setup(); await t.listen();
  try {
    const requestKey = crypto.randomUUID();
    t.rz.next.push('lost');
    const first = await book(t, { quantity: 2, consent: true, requestKey }, { cookie: `_fbp=${FBP}` });
    assert.equal(first.status, 502);
    assert.equal(first.body.error, 'payment_link_failed');
    assert.equal(t.links.length, 1, 'Razorpay made the link even though the answer was lost');

    const again = await book(t, { quantity: 2, consent: true, requestKey }, { cookie: `_fbp=${FBP}` });
    assert.equal(again.status, 200);
    assert.equal(again.body.url, t.links[0].short_url);
    assert.equal(again.body.amount, 5798);
    assert.equal(t.links.length, 1, 'no second link');
    assert.deepEqual(await statuses(t), { created: 1 }, 'no second booking');
    const b = await t.store.getBooking(again.body.bookingId);
    assert.equal(b.paymentLinkId, t.links[0].id);
    assert.equal(b.requestKey, requestKey);
    assert.equal(b.fbp, FBP);

    // Pressing again returns the stored link without asking Razorpay anything.
    const { creates, lookups } = t.rz;
    const third = await book(t, { quantity: 2, consent: true, requestKey });
    assert.equal(third.status, 200);
    assert.equal(third.body.bookingId, b.id);
    assert.equal(third.body.url, t.links[0].short_url);
    assert.deepEqual([t.rz.creates, t.rz.lookups], [creates, lookups]);

    // Paying that link gives exactly one Purchase.
    assert.equal((await webhook(t, paidEvent(t.links[0], b))).body.outcome, 'paid');
    await settle();
    assert.equal(t.metaCalls.length, 1);
    assert.equal(t.metaCalls[0].body.data[0].custom_data.order_id, b.id);
  } finally { await t.close(); }
});

test('retry key: Razorpay down before creating, a later retry makes the link with a fresh expiry', async () => {
  const t = setup(); await t.listen();
  try {
    const requestKey = crypto.randomUUID();
    t.rz.next.push('down');
    assert.equal((await book(t, { quantity: 1, consent: false, requestKey })).status, 502);
    assert.equal(t.links.length, 0);
    assert.deepEqual(await statuses(t), { created: 1 }, 'kept open for the retry, not failed');

    // Ten minutes on, the original expiry is too close for Razorpay (it needs 15 minutes): a fresh one is used.
    t.tick(10 * 60e3);
    const again = await book(t, { quantity: 1, consent: false, requestKey });
    assert.equal(again.status, 200);
    assert.equal(t.links.length, 1);
    assert.equal(t.links[0].expiresAt, NOW + 30 * 60e3);
    assert.equal((await t.store.getBooking(again.body.bookingId)).expiresAt, NOW + 30 * 60e3);
    assert.deepEqual(await statuses(t), { created: 1 });
  } finally { await t.close(); }
});

test('retry key: two presses at once give one booking and one link', async () => {
  const t = setup(); await t.listen();
  try {
    const requestKey = crypto.randomUUID();
    const [a, b] = await Promise.all([book(t, { quantity: 3, requestKey }), book(t, { quantity: 3, requestKey })]);
    assert.ok(a.status === 201 || a.status === 200, `first: ${a.status} ${JSON.stringify(a.body)}`);
    assert.ok(b.status === 201 || b.status === 200, `second: ${b.status} ${JSON.stringify(b.body)}`);
    assert.equal(a.body.bookingId, b.body.bookingId);
    assert.equal(a.body.url, b.body.url);
    assert.equal(t.links.length, 1);
    assert.deepEqual(await statuses(t), { created: 1 });
  } finally { await t.close(); }
});

test('retry key: a different selection, a paid or expiring booking, or a bad key is never replayed', async () => {
  const t = setup(); await t.listen();
  try {
    const requestKey = crypto.randomUUID();
    const first = await book(t, { quantity: 1, consent: true, requestKey });
    assert.equal(first.status, 201);
    // Consent is never carried over to a selection the guest did not make with it, nor the ticket count changed.
    assert.equal((await book(t, { quantity: 1, consent: false, requestKey })).body.error, 'request_key_mismatch');
    assert.equal((await book(t, { quantity: 2, consent: true, requestKey })).body.error, 'request_key_mismatch');

    const booking = await t.store.getBooking(first.body.bookingId);
    assert.equal((await webhook(t, paidEvent(t.links[0], booking))).body.outcome, 'paid');
    const replay = await book(t, { quantity: 1, consent: true, requestKey });
    assert.equal(replay.status, 409);
    assert.equal(replay.body.error, 'request_key_used');
    const fresh = await book(t, { quantity: 1, consent: true, requestKey: crypto.randomUUID() });
    assert.equal(fresh.status, 201);
    assert.notEqual(fresh.body.bookingId, booking.id);

    // A link about to expire is not handed out again.
    const late = crypto.randomUUID();
    assert.equal((await book(t, { quantity: 1, requestKey: late })).status, 201);
    t.tick(19 * 60e3);
    assert.equal((await book(t, { quantity: 1, requestKey: late })).body.error, 'request_key_used');

    for (const bad of ['short', 'x'.repeat(65), 'has spaces in it here', 12345678901234567]) {
      const r = await book(t, { quantity: 1, requestKey: bad });
      assert.equal(r.status, 400, String(bad));
      assert.equal(r.body.error, 'invalid_request_key');
    }
  } finally { await t.close(); }
});

test('retry key: a definite refusal from Razorpay fails the booking, and the key starts afresh', async () => {
  const t = setup(); await t.listen();
  try {
    const requestKey = crypto.randomUUID();
    t.rz.next.push('refuse');
    assert.equal((await book(t, { quantity: 1, requestKey })).status, 502);
    assert.deepEqual(await statuses(t), { failed: 1 });
    assert.equal((await book(t, { quantity: 1, requestKey })).body.error, 'request_key_used');
  } finally { await t.close(); }
});

test('no retry key (a page cached before keys): every request is its own booking, as before', async () => {
  const t = setup(); await t.listen();
  try {
    const a = await book(t, { quantity: 1 });
    const b = await book(t, { quantity: 1 });
    assert.equal(a.status, 201); assert.equal(b.status, 201);
    assert.notEqual(a.body.bookingId, b.body.bookingId);
    t.rz.next.push('lost');
    assert.equal((await book(t, { quantity: 1 })).status, 502);
    assert.deepEqual(await statuses(t), { created: 2, failed: 1 }, 'nothing can come back for it, so it fails');
  } finally { await t.close(); }
});

// ---------------------------------------------------------------- confirmation page

const confirm = async (t, booking, link) => {
  const res = await fetch(`${t.base}/api/bookings/confirmation?booking=${encodeURIComponent(booking)}&link=${encodeURIComponent(link)}`);
  return { status: res.status, body: await res.json() };
};

test('confirmation: says paid only after the signed webhook, with what the page needs for the Purchase', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 2, consent: true, requestKey: crypto.randomUUID() });
    const booking = await t.store.getBooking(r.body.bookingId);
    const link = t.links[0];

    // Arriving on the page proves nothing: before Razorpay's webhook it is pending, and asking changes nothing.
    assert.deepEqual((await confirm(t, booking.id, link.id)).body, { status: 'pending' });
    assert.equal((await t.store.getBooking(booking.id)).status, 'created');

    await webhook(t, paidEvent(link, booking));
    const paid = await confirm(t, booking.id, link.id);
    assert.equal(paid.status, 200);
    assert.deepEqual(paid.body, { status: 'paid', bookingId: booking.id, quantity: 2, value: 5798, unitPrice: 2899, currency: 'INR',
      consent: true, itemId: t.config.event.itemId, eventId: `purchase.${booking.id}` });
    await settle();
    // The browser Purchase uses the same event id as the server's, so Meta keeps one.
    assert.equal(t.metaCalls[0].body.data[0].event_id, paid.body.eventId);
  } finally { await t.close(); }
});

test('confirmation: no consent, wrong or made-up ids, and closed bookings reveal nothing to send', async () => {
  const t = setup(); await t.listen();
  try {
    const r = await book(t, { quantity: 1, consent: false });
    const booking = await t.store.getBooking(r.body.bookingId);
    await webhook(t, paidEvent(t.links[0], booking));
    assert.equal((await confirm(t, booking.id, t.links[0].id)).body.consent, false);

    const other = await book(t, { quantity: 1, consent: true });
    assert.equal((await confirm(t, other.body.bookingId, t.links[0].id)).status, 404, 'link of another booking');
    assert.equal((await confirm(t, 'SPH-261110-ABCDEFGHJK', 'plink_abcdef')).status, 404, 'no such booking');
    for (const [b, l] of [['x', t.links[0].id], [booking.id, 'nope'], ['', ''], [`${booking.id}'`, t.links[0].id]]) {
      assert.equal((await confirm(t, b, l)).status, 400, `${b} ${l}`);
    }

    const expired = paidEvent(t.links[1], await t.store.getBooking(other.body.bookingId));
    expired.event = 'payment_link.expired'; expired.payload.payment_link.entity.status = 'expired';
    await webhook(t, expired);
    assert.deepEqual((await confirm(t, other.body.bookingId, t.links[1].id)).body, { status: 'closed' });
  } finally { await t.close(); }
});

test('confirmation page: Razorpay is told to return guests to it only once the client approves the wording', async () => {
  const { createRazorpay } = require('../razorpay');
  const bodies = [];
  const rz = createRazorpay({ keyId: 'k', keySecret: 's', apiBase: 'https://api.example' }, async (url, init) => {
    bodies.push(JSON.parse(init.body));
    return new Response(JSON.stringify({ id: 'plink_abc123', short_url: 'https://rzp.io/x' }), { status: 200 });
  });
  const booking = { id: 'SPH-261110-ABCDEFGHJK', amountPaise: 289900, quantity: 1 };
  const event = { name: 'Carnival', slug: 'carnival' };
  await rz.createPaymentLink({ booking, event, expiresAt: NOW + 20 * 60e3 });
  await rz.createPaymentLink({ booking, event: { ...event, confirmationUrl: 'https://spherewellness.in/carnival/booked/' }, expiresAt: NOW + 20 * 60e3 });
  assert.equal(bodies[0].callback_url, undefined);
  assert.equal(bodies[0].callback_method, undefined);
  assert.equal(bodies[1].callback_url, 'https://spherewellness.in/carnival/booked/');
  assert.equal(bodies[1].callback_method, 'get');

  const draft = loadConfig({});
  assert.equal(draft.event.confirmationUrl, require('../../data/event.json').booking_confirmation?.draft === false
    ? 'https://spherewellness.in/carnival/booked/' : null);
});
