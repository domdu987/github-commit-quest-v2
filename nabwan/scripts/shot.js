const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2], out = process.argv[3];
  const browser = await chromium.launch();
  const wrap = (html) => `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${html}</body></html>`;
  const fs = require('fs');
  fs.writeFileSync(dir + '/_preview.html', wrap(fs.readFileSync(dir + '/index.html', 'utf8')));
  const errors = [];
  for (const [name, vp, scheme] of [['desk-light', {width: 1280, height: 900}, 'light'], ['phone-dark', {width: 390, height: 844}, 'dark']]) {
    const ctx = await browser.newContext({ viewport: vp, colorScheme: scheme, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    page.on('console', m => { if (m.type() === 'error') errors.push(name + ': ' + m.text()); });
    page.on('pageerror', e => errors.push(name + ': ' + e.message));
    await page.goto('file://' + dir + '/_preview.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);
    const sw = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth, document.fonts.check('16px Kanit'), document.fonts.check('16px "IBM Plex Sans Thai"')]);
    console.log(name, 'scrollWidth/innerWidth/fonts', JSON.stringify(sw));
    // capture a few key regions
    for (const sel of ['header.top', '#structure', '#script', '#s14', '#s23', '#style', '#sound']) {
      const el = await page.$(sel);
      if (el) await el.screenshot({ path: `${out}/${name}_${sel.replace(/[#.\s]/g,'')}.png` });
    }
    await ctx.close();
  }
  console.log('errors:', JSON.stringify(errors));
  await browser.close();
})();
