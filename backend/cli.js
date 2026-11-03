// Developer commands for the booking backend, run where the environment variables are set:
//
//   npm run bookings -- check       configuration problems (no secret values printed)
//   npm run bookings -- stats       website bookings, tickets paid, and Meta delivery states
//   npm run bookings -- reconcile   ask Razorpay about unpaid links, in case a webhook never arrived
//   npm run bookings -- retry       send any Purchase still waiting (resets failed or abandoned ones)
const { loadConfig, problems } = require('./config');
const { createStore } = require('./store');
const { createRazorpay } = require('./razorpay');
const { createMeta } = require('./meta');
const { createApi } = require('./app');

async function main(command) {
  const config = loadConfig();
  if (command === 'check') {
    const { blocking, warnings } = problems(config);
    console.log(JSON.stringify({ bookingsEnabled: config.bookingsEnabled, razorpay: config.razorpay.mode, store: config.db ? 'mysql' : 'file',
      metaTestMode: !!config.meta.testEventCode, blocking, warnings }, null, 2));
    return;
  }
  const store = createStore(config);
  await store.init();
  const razorpay = createRazorpay(config.razorpay);
  const api = createApi({ config, store, razorpay, meta: createMeta(config.meta), log: (l, m, f) => console.log(l, m, JSON.stringify(f)) });
  try {
    if (command === 'stats') {
      const s = await store.stats(config.event.slug);
      console.log(JSON.stringify({ ...s, revenueInr: s.revenuePaise / 100, unfinishedMeta: await store.listUnfinishedMeta(Date.now()) }, null, 2));
    } else if (command === 'reconcile') {
      // The Razorpay API is authenticated with our own key, so its answer is as trustworthy as a signed webhook.
      for (const b of await store.listPending(Date.now())) {
        const link = await razorpay.fetchPaymentLink(b.paymentLinkId);
        const captured = (link.payments || []).find(p => p.status === 'captured');
        if (link.status === 'paid' && captured) {
          const payment = await razorpay.fetchPayment(captured.payment_id);
          const r = await api.handleEvent({ event: 'payment_link.paid', payload: { payment_link: { entity: link }, payment: { entity: payment } } });
          console.log(b.id, r.outcome);
          if (r.bookingId) console.log(b.id, 'meta', await api.deliver(r.bookingId));
        } else if (['expired', 'cancelled'].includes(link.status)) {
          console.log(b.id, (await api.handleEvent({ event: `payment_link.${link.status}`, payload: { payment_link: { entity: link } } })).outcome);
        } else console.log(b.id, link.status);
      }
    } else if (command === 'retry') {
      for (const u of await store.listUnfinishedMeta(Date.now())) await store.finishMeta(u.id, { status: 'failed', error: 'manual retry' });
      if (store.resetMetaAttempts) await store.resetMetaAttempts();
      console.log(JSON.stringify(await api.sweep({ ignoreBackoff: true })));
    } else {
      console.log('Commands: check | stats | reconcile | retry');
      process.exitCode = 1;
    }
  } finally { await store.close(); }
}

main(process.argv[2]).catch(err => { console.error(err.message); process.exitCode = 1; });
