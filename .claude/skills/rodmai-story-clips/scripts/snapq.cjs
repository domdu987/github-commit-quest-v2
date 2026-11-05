// node snapq.cjs <port> <query> <outfile.png> <t>   — one portrait frame of index.html?<query> at time t
const playwright = require('playwright');
(async () => {
  const [port, q, out, t, w = 1080, h = 1920] = process.argv.slice(2);
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  p.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto(`http://localhost:${port}/index.html?${q}`); await p.waitForTimeout(2500);
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false);
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(1000); await seek(t); await p.waitForTimeout(1500);
  await p.evaluate(() => document.fonts.ready); await seek(t); await p.waitForTimeout(900); await p.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))); await p.waitForTimeout(300);
  // a frame may be captured half-painted when the machine is busy: shoot until two consecutive screenshots agree
  let prev = null; for (let k = 0; k < 6; k++) { const buf = await p.screenshot(); if (prev && buf.equals(prev)) { require('fs').writeFileSync(out, buf); prev = null; break; } prev = buf; await p.waitForTimeout(500); }
  if (prev) require('fs').writeFileSync(out, prev);
  await b.close();
})();
