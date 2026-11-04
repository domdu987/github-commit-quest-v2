// node probe_hands.cjs <port> <actor ids comma-separated> t1 t2 ... → page-pixel centres of each actor's hands (F/B), its head box,
// and the gap between every pair of hands of different actors (to stage a hand-hold: the gap should be ~0)
const { chromium } = require('playwright');
(async () => {
  const [port, idsArg, ...ts] = process.argv.slice(2); const ids = idsArg.split(',');
  const b = await chromium.launch({ args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(4000);
  for (const t of ts) {
    const r = await p.evaluate(([t, ids]) => { const tl = window.__timelines.main; tl.seek(+t, false);
      let clip = null; document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden'; if (on) clip = c; });
      const pt = (el, x, y) => { const m = el.getScreenCTM(); return [Math.round(m.a * x + m.c * y + m.e), Math.round(m.b * x + m.d * y + m.f)]; };
      const out = {}; ids.forEach((id) => { const q = (s) => clip && clip.querySelector('#' + id + '-' + s); const o = {};
        ['F', 'B'].forEach((sd) => { const fa = q('fa' + sd); if (fa) o['hand' + sd] = pt(fa, 0, 120); const ua = q('ua' + sd); if (ua) o['shoulder' + sd] = pt(ua, 0, 0); });
        const h = q('head'); if (h) { const bb = h.getBoundingClientRect(); o.head = [Math.round(bb.left), Math.round(bb.top), Math.round(bb.right), Math.round(bb.bottom)]; }
        out[id] = o; }); return { clip: clip && clip.id, out }; }, [t, ids]);
    console.log('t', t, r.clip); const all = [];
    for (const [id, o] of Object.entries(r.out)) { console.log(' ', id, JSON.stringify(o)); ['handF', 'handB'].forEach((k) => o[k] && all.push([id, k, o[k]])); }
    for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++) if (all[i][0] !== all[j][0]) { const [a, b2] = [all[i][2], all[j][2]]; console.log('   gap', all[i][0] + '.' + all[i][1], all[j][0] + '.' + all[j][1], Math.round(Math.hypot(a[0] - b2[0], a[1] - b2[1]))); }
  }
  await b.close(); })();
