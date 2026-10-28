const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.error('pageerror', e.message));
  for (const k of process.argv.slice(2)) {
    await p.goto('file://' + path.resolve(__dirname, 'cover.html') + '?' + k);
    await p.evaluate(() => Promise.all(['500', '600', '700'].map(w => document.fonts.load(`${w} 40px Kanit`, 'กขคง 0123'))));
    await p.evaluate(() => window.ready);
    await (await p.$('#frame')).screenshot({ path: path.join(__dirname, `cover_${k}.png`) });
  }
  await b.close();
})();
