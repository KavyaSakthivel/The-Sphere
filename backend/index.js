// Wires the booking backend together for server.js. If anything here fails (no database, a missing
// secret), the API answers 503 and the carnival page falls back to the shared Razorpay link:
// the website itself keeps serving either way.
const { loadConfig } = require('./config');
const { createStore } = require('./store');
const { createRazorpay } = require('./razorpay');
const { createMeta } = require('./meta');
const { createApi, defaultLog: log } = require('./app');

const SWEEP_EVERY_MS = 5 * 60 * 1000;

function startBackend(env = process.env) {
  let api = null;
  const config = loadConfig(env);
  const store = createStore(config);

  const ready = (async () => {
    await store.init();
    api = createApi({ config, store, razorpay: createRazorpay(config.razorpay), meta: createMeta(config.meta) });
    log('info', 'backend_ready', {
      store: store.kind, bookings: api.bookingsOpen ? 'open' : 'closed', razorpay: config.razorpay.mode,
      metaTestMode: !!config.meta.testEventCode, blocking: api.issues.blocking, warnings: api.issues.warnings,
    });
    const sweep = () => api.sweep().catch(err => log('error', 'sweep_failed', { error: err.message }));
    setTimeout(sweep, 10e3).unref();
    setInterval(sweep, SWEEP_EVERY_MS).unref();
  })().catch(err => log('error', 'backend_start_failed', { store: store.kind, error: err.message }));

  return {
    ready,
    async handle(req, res, pathname) {
      if (api) return api.handle(req, res, pathname);
      res.writeHead(503, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'Retry-After': '30' });
      res.end('{"error":"bookings_unavailable"}');
    },
  };
}

module.exports = { startBackend };
