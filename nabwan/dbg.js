const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
p.on('pageerror', e => console.error('ERR', e.stack)); await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForTimeout(1500); await b.close(); })();
