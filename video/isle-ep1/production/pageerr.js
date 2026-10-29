const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = [];
  p.on('pageerror', (e) => errs.push('PAGEERROR ' + e.message + '\n' + (e.stack || '').split('\n').slice(0, 4).join('\n')));
  p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text().slice(0, 300)); });
  try { await p.goto(process.argv[2], { waitUntil: 'domcontentloaded', timeout: 120000 }); await p.waitForTimeout(8000); } catch (e) { errs.push('GOTO ' + e.message.slice(0, 200)); }
  console.log(errs.slice(0, 12).join('\n') || 'no errors');
  await b.close();
})();
