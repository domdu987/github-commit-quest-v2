// landscape snap: node snapL.cjs <port> <out dir> t1 t2 ... → 1920×1080 PNGs; prints each visible clip's landscape placement
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(3000);
  const seek = (t) => p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false);
    let info = ''; document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden'; if (on) info = c.id + ' ' + (c.dataset.land || ''); });
    return info; }, t);
  await seek(0.2); await p.waitForTimeout(1200); await seek(ts[0]); await p.waitForTimeout(1500);
  for (const t of ts) { const info = await seek(t); await p.waitForTimeout(400); await p.screenshot({ path: `${out}/t${(+t).toFixed(2)}.png` }); console.log(t, info); }
  if (ts.length > 1) { await seek(ts[0]); await p.waitForTimeout(800); await p.screenshot({ path: `${out}/t${(+ts[0]).toFixed(2)}.png` }); }
  await b.close(); })();
