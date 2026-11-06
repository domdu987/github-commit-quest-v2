const pw = require('playwright'); const path = require('path');
(async () => { const b = await pw.chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'cover.html')); await p.waitForTimeout(1500); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: path.join(__dirname, 'cover.png') }); await b.close(); })();
