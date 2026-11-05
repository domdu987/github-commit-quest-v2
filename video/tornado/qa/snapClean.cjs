// node snapClean.cjs <port> <out dir> t1 t2 … → 1920×1080 PNGs without captions, source chips, live UI comments or the corner badge
// (clean plates for covers and thumbnails)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(4000);
  await p.addStyleTag({ content: '.capwrap, .srcchip, #badge, .badge { display: none !important; }' });
  for (const t of ts) {
    await p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false);
      document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
    await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/c${(+t).toFixed(2)}.png` }); console.log('ok', t);
  }
  await b.close(); })();
