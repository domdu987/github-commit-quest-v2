const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.error('pageerror', e.message)); p.on('console', m => console.log('console', m.text()));
await p.goto('file://' + path.join(__dirname, process.argv[2])); await p.waitForTimeout(300);
await (await p.$('#frame')).screenshot({ path: process.argv[3] }); await b.close(); })();
