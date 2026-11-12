// node raster.js jobs.json   jobs: [{src:'file.svg', out:'file.png', w:720, h:1280, transparent:false}]
// One Chromium launch for all jobs (Playwright). PNG; transparent jobs keep alpha.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const page = await browser.newPage();
  for (const j of jobs) {
    const svg = fs.readFileSync(j.src, 'utf8');
    await page.setViewportSize({ width: j.w, height: j.h });
    await page.setContent(`<html><body style="margin:0;background:${j.transparent ? 'transparent' : '#000'}">${svg}</body></html>`);
    await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: j.h }, omitBackground: !!j.transparent });
    console.log('wrote', j.out);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
