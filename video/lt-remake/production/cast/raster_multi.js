// node raster_multi.js jobs.json
// jobs.json = [{"svg": "in.svg", "out": "out.png|jpg", "w": 800, "h": 600, "dsf": 1, "bg": "transparent|#rrggbb"}, ...]
// Rasterises many SVG files with ONE headless Chromium (Playwright).  PNG keeps transparency, JPG is quality 92.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  // one context and page for the whole batch (a fresh context per job started failing to capture after a container restart)
  const ctx = await browser.newContext({ viewport: { width: 64, height: 64 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  for (const j of jobs) {
    await page.setViewportSize({ width: +j.w, height: +j.h });
    const bg = j.bg || 'transparent';
    await page.setContent(`<html><body style="margin:0;background:${bg}">${fs.readFileSync(j.svg, 'utf8')}</body></html>`);
    const jpg = /\.jpe?g$/i.test(j.out);
    await page.screenshot(Object.assign({ path: j.out, clip: { x: 0, y: 0, width: +j.w, height: +j.h } },
      jpg ? { type: 'jpeg', quality: 92 } : { omitBackground: bg === 'transparent' }));
  }
  await ctx.close();
  await browser.close();
  console.log('rasterised', jobs.length, 'file(s)');
})().catch(e => { console.error(e); process.exit(1); });
