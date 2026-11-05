// node probe.cjs <port> <js expression evaluated in the page after load> → prints JSON
const { chromium } = require('playwright');
(async () => {
  const [port, expr] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  const r = await p.evaluate(expr); console.log(JSON.stringify(r, null, 1)); await b.close(); })();
