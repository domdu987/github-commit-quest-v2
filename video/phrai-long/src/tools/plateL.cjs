// clean landscape plate: node plateL.cjs <port> <out dir> <hide css selectors|-> t1 t2 ... (same seek path as snapL.cjs)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, out, hide, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(3000);
  if (hide !== '-') await p.addStyleTag({ content: `${hide} { display: none !important; }` });
  const seek = (t) => p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false);
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(1200); await seek(ts[0]); await p.waitForTimeout(1500);
  for (const t of ts) { await seek(t); await p.waitForTimeout(2000); await p.screenshot({ path: `${out}/p${(+t).toFixed(2)}.png` }); console.log(t); }
  await b.close(); })();
