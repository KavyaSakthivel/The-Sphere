// The page Razorpay returns a guest to after paying for a website booking (/<slug>/booked/).
// Razorpay adds the payment link id and our booking reference to the address. The page asks the server
// whether that booking is paid; it never decides that itself, because anyone can open this address.
// Only a paid booking whose guest agreed to share it with Meta sends the browser Purchase, with the same
// event id the server uses, so Meta counts the sale once. Arriving without those details (the shared
// payment page, a bookmark) shows a plain thank-you and sends nothing.
(() => {
  const root = document.querySelector('[data-booked]');
  if (!root) return;
  const params = new URLSearchParams(location.search);
  const id = params.get('razorpay_payment_link_reference_id') || '';
  const link = params.get('razorpay_payment_link_id') || '';
  // Keep the payment details out of the address bar, history and anything the guest shares.
  if (location.search) history.replaceState(null, '', location.pathname);
  if (!/^SPH-\d{6}-[2-9A-Z]{10}$/.test(id) || !/^plink_[A-Za-z0-9]{6,40}$/.test(link)) return; // plain thank-you

  const show = state => { root.dataset.state = state; };
  const field = (name, value) => { const el = root.querySelector(`[data-field="${name}"]`); if (el) el.textContent = value; };
  const rupees = n => '₹' + Number(n).toLocaleString('en-IN');

  const purchase = data => {
    if (!data.consent || typeof window.fbq !== 'function') return;
    const key = 'sphere-purchase-sent-' + data.bookingId;
    try { if (localStorage.getItem(key)) return; } catch {}
    window.fbq('track', 'Purchase', {
      value: data.value, currency: data.currency, num_items: data.quantity, content_type: 'product',
      content_ids: [data.itemId], contents: [{ id: data.itemId, quantity: data.quantity, item_price: data.unitPrice }],
    }, { eventID: data.eventId });
    try { localStorage.setItem(key, '1'); } catch {}
  };

  // Razorpay's confirmation to our server usually lands within seconds of the redirect, so ask a few times.
  const ATTEMPTS = 10, GAP_MS = 2000;
  show('checking');
  (async () => {
    for (let i = 0; i < ATTEMPTS; i++) {
      try {
        const res = await fetch(`/api/bookings/confirmation?booking=${encodeURIComponent(id)}&link=${encodeURIComponent(link)}`,
          { credentials: 'same-origin', cache: 'no-store' });
        if (res.status === 404 || res.status === 400) { show('thanks'); return; }
        const data = res.ok ? await res.json() : null;
        if (data?.status === 'paid') {
          field('bookingId', data.bookingId);
          field('quantity', String(data.quantity));
          field('total', rupees(data.value));
          show('paid');
          purchase(data);
          return;
        }
        if (data?.status === 'closed') { show('closed'); return; }
      } catch { /* try again */ }
      await new Promise(r => setTimeout(r, GAP_MS));
    }
    show('pending');
  })();
})();
