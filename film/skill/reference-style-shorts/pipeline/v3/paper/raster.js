// node raster.js jobs.json   jobs: [{src:'file.svg', out:'file.png', w:int, h:int, transparent:bool}]
// Headless Chromium (Playwright). Waits for the embedded @font-face fonts before each screenshot.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage();
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  for (const j of jobs) {
    const svg = fs.readFileSync(j.src, 'utf8'); await page.setViewportSize({ width: j.w, height: j.h });
    const t0 = Date.now();
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(30);
    await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: j.h }, omitBackground: !!j.transparent });
    console.log('wrote', j.out, (Date.now() - t0) + ' ms');
  }
  await browser.close();
})();
