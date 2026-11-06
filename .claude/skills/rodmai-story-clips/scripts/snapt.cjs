// node snapt.cjs <port> <outdir> t1 t2 ...  — frames with captions/HUD kept, only the active clip visible
const pw = require('playwright'); const path = require('path');
(async () => { const [port, out, ...times] = process.argv.slice(2); const b = await pw.chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html`, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(2500); await p.evaluate(() => document.fonts.ready);
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false); document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  for (const t of times) { await seek(t); await p.waitForTimeout(700); await p.screenshot({ path: path.join(out, `t${t}.png`) }); }
  await b.close(); })();
