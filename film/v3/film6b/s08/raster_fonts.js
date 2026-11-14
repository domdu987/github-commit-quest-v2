// node raster_fonts.js jobs.json -- like v3/set3d/raster.js, but waits for web fonts (Kanit @font-face) before the screenshot.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const page = await browser.newPage();
  for (const j of jobs) {
    const svg = fs.readFileSync(j.src, 'utf8');
    await page.setViewportSize({ width: j.w, height: j.h });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await page.evaluate(async () => { await document.fonts.ready; for (const f of document.fonts) { await f.load(); } });
    await page.waitForTimeout(50);
    await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: j.h }, omitBackground: true });
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
