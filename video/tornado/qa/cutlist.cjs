// node cutlist.cjs <port> → JSON [[clip id, start, duration], …] sorted by start
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${process.argv[2]}/index.html`); await p.waitForFunction(() => document.querySelectorAll('.clip').length > 5, null, { timeout: 120000 });
  const r = await p.evaluate(() => [...document.querySelectorAll('.clip')].map((c) => [c.id, +c.dataset.start, +c.dataset.duration]));
  r.sort((a, b) => a[1] - b[1]); console.log(JSON.stringify(r)); await b.close(); })();
