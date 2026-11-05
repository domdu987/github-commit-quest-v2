const playwright = require('playwright');
(async () => {
  const [port, t, x, y, dir, hideSel] = process.argv.slice(2);
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html?`); await p.waitForTimeout(2500);
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false);
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(800); await seek(t); await p.waitForTimeout(1500);
  const clip = { x: +x - 150, y: +y - 150, width: 300, height: 300 };
  await p.screenshot({ path: `${dir}/w0.png`, clip });
  await p.evaluate((s) => document.querySelectorAll(s).forEach((e) => { e.style.display = 'none'; }), hideSel); await p.waitForTimeout(400); await p.screenshot({ path: `${dir}/w1_display.png`, clip });
  await p.evaluate((s) => document.querySelectorAll(s).forEach((e) => { e.style.display = ''; e.style.visibility = 'hidden'; }), hideSel); await p.waitForTimeout(400); await p.screenshot({ path: `${dir}/w2_vis.png`, clip });
  await b.close();
})();
