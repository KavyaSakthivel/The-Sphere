// Booking storage. MySQL in production (Hostinger); a small JSON file for local development and
// tests. Both expose the same methods, and every state change is a conditional update, so a webhook
// delivered twice, or twice at once, can never mark a booking paid twice or send Meta two Purchases.
const fs = require('fs');
const path = require('path');

const ACTIVE = ['created', 'paid', 'review'];
const META_MAX_ATTEMPTS = 8;
const META_WINDOW_MS = 7 * 24 * 3600 * 1000; // Meta rejects events older than seven days
const IDENTIFIERS = { fbp: null, fbc: null, clientIp: null, emHash: null, phHash: null };

function newBooking(fields) {
  return {
    id: fields.id, eventSlug: fields.eventSlug, quantity: fields.quantity, unitPricePaise: fields.unitPricePaise,
    amountPaise: fields.amountPaise, currency: 'INR', status: 'created', paymentLinkId: null, paymentLinkUrl: null,
    paymentId: null, consent: !!fields.consent, fbp: fields.fbp || null, fbc: fields.fbc || null,
    clientIp: fields.clientIp || null, userAgent: fields.userAgent || null, emHash: null, phHash: null,
    createdAt: fields.createdAt, expiresAt: fields.expiresAt, paidAt: null, paymentTime: null,
    metaStatus: 'pending', metaAttempts: 0, metaLastAttemptAt: null, metaLastError: null, metaFbtraceId: null,
  };
}

// ------------------------------------------------------------------ JSON file / memory

class FileStore {
  constructor(file) { this.file = file; this.data = { bookings: {}, webhookEvents: {} }; this.kind = file ? 'file' : 'memory'; }

  async init() {
    if (!this.file) return;
    fs.mkdirSync(path.dirname(this.file), { recursive: true });
    if (fs.existsSync(this.file)) this.data = JSON.parse(fs.readFileSync(this.file, 'utf8'));
  }

  save() {
    if (!this.file) return;
    const tmp = this.file + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(this.data), { mode: 0o600 });
    fs.renameSync(tmp, this.file);
  }

  async insertBooking(fields) { const b = newBooking(fields); this.data.bookings[b.id] = b; this.save(); return { ...b }; }
  async getBooking(id) { const b = this.data.bookings[id]; return b ? { ...b } : null; }
  async getBookingByLink(linkId) { const b = Object.values(this.data.bookings).find(x => x.paymentLinkId === linkId); return b ? { ...b } : null; }

  async attachPaymentLink(id, linkId, url) { Object.assign(this.data.bookings[id], { paymentLinkId: linkId, paymentLinkUrl: url }); this.save(); }
  async markFailed(id) { const b = this.data.bookings[id]; if (b && b.status === 'created') { b.status = 'failed'; this.save(); } }

  async countActiveTickets(slug, now) {
    return Object.values(this.data.bookings)
      .filter(b => b.eventSlug === slug && ACTIVE.includes(b.status) && (b.status !== 'created' || b.expiresAt > now))
      .reduce((n, b) => n + b.quantity, 0);
  }

  // Returns true only for the delivery that moved the booking to paid (or review).
  async markPaid(id, { status, paymentId, paidAt, paymentTime, emHash, phHash, metaStatus, metaLastError }) {
    const b = this.data.bookings[id];
    if (!b || b.status === 'paid' || b.status === 'review') return false;
    Object.assign(b, { status, paymentId, paidAt, paymentTime, metaStatus, metaLastError: metaLastError || null });
    if (b.consent) Object.assign(b, { emHash, phHash });
    this.save();
    return true;
  }

  async markClosed(linkId, status) {
    const b = Object.values(this.data.bookings).find(x => x.paymentLinkId === linkId);
    if (b && b.status === 'created') { b.status = status; this.save(); return true; }
    return false;
  }

  async recordWebhookEvent(eventId, event, now) {
    const seen = this.data.webhookEvents[eventId];
    if (seen) return seen.result;
    this.data.webhookEvents[eventId] = { event, receivedAt: now, result: 'processing' };
    this.save();
    return null;
  }
  async finishWebhookEvent(eventId, result) { if (this.data.webhookEvents[eventId]) { this.data.webhookEvents[eventId].result = result; this.save(); } }

  // Atomically take the right to send this booking's Purchase. A claim left 'sending' by a crash is
  // retaken after staleMs.
  async claimMeta(id, now, staleMs) {
    const b = this.data.bookings[id];
    if (!b || b.status !== 'paid' || b.metaAttempts >= META_MAX_ATTEMPTS) return null;
    const stale = b.metaStatus === 'sending' && b.metaLastAttemptAt < now - staleMs;
    if (!['pending', 'failed'].includes(b.metaStatus) && !stale) return null;
    Object.assign(b, { metaStatus: 'sending', metaAttempts: b.metaAttempts + 1, metaLastAttemptAt: now });
    this.save();
    return { ...b };
  }

  async finishMeta(id, { status, error, fbtraceId }) {
    const b = this.data.bookings[id];
    Object.assign(b, { metaStatus: status, metaLastError: error || null, metaFbtraceId: fbtraceId || b.metaFbtraceId });
    // Once Meta has the event (or it is too old to ever be sent), the personal identifiers have served their purpose.
    if (status === 'sent' || status === 'expired') Object.assign(b, IDENTIFIERS);
    this.save();
  }

  async listMetaDue(now, staleMs, limit = 20) {
    return Object.values(this.data.bookings)
      .filter(b => b.status === 'paid' && b.metaAttempts < META_MAX_ATTEMPTS &&
        (['pending', 'failed'].includes(b.metaStatus) || (b.metaStatus === 'sending' && b.metaLastAttemptAt < now - staleMs)))
      .slice(0, limit).map(b => b.id);
  }

  async listUnfinishedMeta(now) {
    return Object.values(this.data.bookings)
      .filter(b => b.status === 'paid' && (b.metaStatus === 'abandoned' || (['pending', 'failed', 'sending'].includes(b.metaStatus) &&
        (b.metaAttempts >= META_MAX_ATTEMPTS || (b.paymentTime && b.paymentTime * 1000 < now - META_WINDOW_MS)))))
      .map(b => ({ id: b.id, attempts: b.metaAttempts, paymentTime: b.paymentTime }));
  }

  async resetMetaAttempts() {
    for (const b of Object.values(this.data.bookings)) if (b.status === 'paid' && b.metaStatus === 'failed') b.metaAttempts = 0;
    this.save();
  }

  async listPending(now) {
    return Object.values(this.data.bookings).filter(b => b.status === 'created' && b.paymentLinkId).map(b => ({ ...b }));
  }

  async stats(slug) {
    const rows = Object.values(this.data.bookings).filter(b => b.eventSlug === slug);
    return summarise(rows);
  }

  async close() {}
}

function summarise(rows) {
  const out = { bookings: {}, ticketsPaid: 0, revenuePaise: 0, meta: {} };
  for (const b of rows) {
    out.bookings[b.status] = (out.bookings[b.status] || 0) + 1;
    if (b.status === 'paid') {
      out.ticketsPaid += b.quantity; out.revenuePaise += b.amountPaise;
      out.meta[b.metaStatus] = (out.meta[b.metaStatus] || 0) + 1;
    }
  }
  return out;
}

// ------------------------------------------------------------------ MySQL

const COLUMNS = {
  id: 'id', eventSlug: 'event_slug', quantity: 'quantity', unitPricePaise: 'unit_price_paise', amountPaise: 'amount_paise',
  currency: 'currency', status: 'status', paymentLinkId: 'payment_link_id', paymentLinkUrl: 'payment_link_url',
  paymentId: 'payment_id', consent: 'consent', fbp: 'fbp', fbc: 'fbc', clientIp: 'client_ip', userAgent: 'user_agent',
  emHash: 'em_hash', phHash: 'ph_hash', createdAt: 'created_at', expiresAt: 'expires_at', paidAt: 'paid_at',
  paymentTime: 'payment_time', metaStatus: 'meta_status', metaAttempts: 'meta_attempts',
  metaLastAttemptAt: 'meta_last_attempt_at', metaLastError: 'meta_last_error', metaFbtraceId: 'meta_fbtrace_id',
};
const NUMERIC = new Set(['quantity', 'unitPricePaise', 'amountPaise', 'createdAt', 'expiresAt', 'paidAt', 'paymentTime', 'metaAttempts', 'metaLastAttemptAt']);
const fromRow = row => {
  if (!row) return null;
  const b = {};
  for (const [key, col] of Object.entries(COLUMNS)) b[key] = row[col] == null ? null : NUMERIC.has(key) ? Number(row[col]) : row[col];
  b.consent = !!Number(row.consent);
  return b;
};

class MySqlStore {
  constructor(options) { this.options = options; this.kind = 'mysql'; }

  async init() {
    const mysql = require('mysql2/promise');
    this.pool = mysql.createPool({ ...this.options, connectionLimit: 5, waitForConnections: true, charset: 'utf8mb4', supportBigNumbers: true });
    const schema = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf8');
    for (const statement of schema.replace(/--[^\n]*/g, '').split(';').map(s => s.trim()).filter(Boolean)) await this.pool.query(statement);
  }

  async q(sql, params) { const [result] = await this.pool.execute(sql, params); return result; }

  async insertBooking(fields) {
    const b = newBooking(fields);
    const keys = Object.keys(COLUMNS);
    await this.q(`INSERT INTO bookings (${keys.map(k => COLUMNS[k]).join(',')}) VALUES (${keys.map(() => '?').join(',')})`,
      keys.map(k => (k === 'consent' ? (b.consent ? 1 : 0) : b[k])));
    return b;
  }
  async getBooking(id) { return fromRow((await this.q('SELECT * FROM bookings WHERE id=?', [id]))[0]); }
  async getBookingByLink(linkId) { return fromRow((await this.q('SELECT * FROM bookings WHERE payment_link_id=?', [linkId]))[0]); }
  async attachPaymentLink(id, linkId, url) { await this.q('UPDATE bookings SET payment_link_id=?, payment_link_url=? WHERE id=?', [linkId, url, id]); }
  async markFailed(id) { await this.q("UPDATE bookings SET status='failed' WHERE id=? AND status='created'", [id]); }

  async countActiveTickets(slug, now) {
    const rows = await this.q(`SELECT COALESCE(SUM(quantity),0) AS n FROM bookings WHERE event_slug=?
      AND (status IN ('paid','review') OR (status='created' AND expires_at > ?))`, [slug, now]);
    return Number(rows[0].n);
  }

  async markPaid(id, { status, paymentId, paidAt, paymentTime, emHash, phHash, metaStatus, metaLastError }) {
    const r = await this.q(`UPDATE bookings SET status=?, payment_id=?, paid_at=?, payment_time=?, meta_status=?, meta_last_error=?,
      em_hash=IF(consent=1, ?, NULL), ph_hash=IF(consent=1, ?, NULL)
      WHERE id=? AND status NOT IN ('paid','review')`,
      [status, paymentId, paidAt, paymentTime, metaStatus, metaLastError || null, emHash || null, phHash || null, id]);
    return r.affectedRows === 1;
  }

  async markClosed(linkId, status) {
    const r = await this.q("UPDATE bookings SET status=? WHERE payment_link_id=? AND status='created'", [status, linkId]);
    return r.affectedRows === 1;
  }

  async recordWebhookEvent(eventId, event, now) {
    const r = await this.q("INSERT IGNORE INTO webhook_events (event_id, event, received_at, result) VALUES (?,?,?,'processing')", [eventId, event, now]);
    if (r.affectedRows === 1) return null;
    return (await this.q('SELECT result FROM webhook_events WHERE event_id=?', [eventId]))[0].result;
  }
  async finishWebhookEvent(eventId, result) { await this.q('UPDATE webhook_events SET result=? WHERE event_id=?', [result, eventId]); }

  async claimMeta(id, now, staleMs) {
    const r = await this.q(`UPDATE bookings SET meta_status='sending', meta_attempts=meta_attempts+1, meta_last_attempt_at=?
      WHERE id=? AND status='paid' AND meta_attempts < ? AND
      (meta_status IN ('pending','failed') OR (meta_status='sending' AND meta_last_attempt_at < ?))`,
      [now, id, META_MAX_ATTEMPTS, now - staleMs]);
    return r.affectedRows === 1 ? this.getBooking(id) : null;
  }

  async finishMeta(id, { status, error, fbtraceId }) {
    const clear = status === 'sent' || status === 'expired';
    await this.q(`UPDATE bookings SET meta_status=?, meta_last_error=?, meta_fbtrace_id=COALESCE(?, meta_fbtrace_id)
      ${clear ? ', fbp=NULL, fbc=NULL, client_ip=NULL, em_hash=NULL, ph_hash=NULL' : ''} WHERE id=?`,
      [status, error ? String(error).slice(0, 500) : null, fbtraceId || null, id]);
  }

  async listMetaDue(now, staleMs, limit = 20) {
    const rows = await this.q(`SELECT id FROM bookings WHERE status='paid' AND meta_attempts < ? AND
      (meta_status IN ('pending','failed') OR (meta_status='sending' AND meta_last_attempt_at < ?)) ORDER BY paid_at LIMIT ${Number(limit)}`,
      [META_MAX_ATTEMPTS, now - staleMs]);
    return rows.map(r => r.id);
  }

  async listUnfinishedMeta(now) {
    const rows = await this.q(`SELECT id, meta_attempts, payment_time FROM bookings WHERE status='paid'
      AND (meta_status='abandoned' OR (meta_status IN ('pending','failed','sending') AND (meta_attempts >= ? OR payment_time < ?)))`,
      [META_MAX_ATTEMPTS, Math.floor((now - META_WINDOW_MS) / 1000)]);
    return rows.map(r => ({ id: r.id, attempts: Number(r.meta_attempts), paymentTime: Number(r.payment_time) }));
  }

  async resetMetaAttempts() { await this.q("UPDATE bookings SET meta_attempts=0 WHERE status='paid' AND meta_status='failed'"); }

  async listPending() { return (await this.q("SELECT * FROM bookings WHERE status='created' AND payment_link_id IS NOT NULL")).map(fromRow); }

  async stats(slug) { return summarise((await this.q('SELECT * FROM bookings WHERE event_slug=?', [slug])).map(fromRow)); }

  async close() { if (this.pool) await this.pool.end(); }
}

function createStore(config) {
  if (config.db) return new MySqlStore(config.db);
  return new FileStore(config.dataDir ? path.join(config.dataDir, 'bookings.json') : null);
}

module.exports = { createStore, FileStore, MySqlStore, META_MAX_ATTEMPTS, META_WINDOW_MS };
