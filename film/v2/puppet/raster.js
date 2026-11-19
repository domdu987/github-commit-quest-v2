// node raster.js in.svg out.(png|jpg) width height [deviceScaleFactor]
// Rasterises an SVG file with headless Chromium (Playwright).  PNG keeps transparency, JPG is written at quality 92.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [src, out, w, h, dsf] = process.argv.slice(2);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +w, height: +h }, deviceScaleFactor: dsf ? +dsf : 1 });
  const page = await ctx.newPage();
  await page.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(src, 'utf8')}</body></html>`);
  const jpg = /\.jpe?g$/i.test(out);
  await page.screenshot(Object.assign({ path: out, clip: { x: 0, y: 0, width: +w, height: +h } },
    jpg ? { type: 'jpeg', quality: 92 } : { omitBackground: true }));
  await browser.close();
  console.log('wrote', out);
})().catch(e => { console.error(e); process.exit(1); });
