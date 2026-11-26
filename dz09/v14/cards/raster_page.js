// raster_page.js -- one persistent headless Chromium page (Playwright) that turns SVG text into RGBA PNG files.
// Started and fed by raster.py (one JSON object per line on stdin, one JSON reply per line on stdout):
//   {"id": 1, "svg": "<svg ...>", "w": 256, "h": 256, "out": "/abs/x.png", "bg": null | "#rrggbb"}
//   -> {"id": 1, "ok": true, "ms": 31.2}
//   {"cmd": "quit"}
// The page is loaded from a file:// URL (page.html beside this script) so its @font-face rules (Work Sans Black,
// Kanit Black from PROJ/fonts) apply to text inside the SVG.  The SVG is put in the DOM and captured with
// page.screenshot(omitBackground) -> straight-alpha PNG.  Deterministic: no time, no randomness.
const { chromium } = require('playwright');
const path = require('path');
const readline = require('readline');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 512, height: 512 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto('file://' + path.join(__dirname, 'page.html'));
  await page.evaluate(() => document.fonts.ready);
  let vw = 512, vh = 512;
  const rl = readline.createInterface({ input: process.stdin });
  for await (const line of rl) {
    if (!line.trim()) continue;
    let job; try { job = JSON.parse(line); } catch (e) { continue; }
    if (job.cmd === 'quit') break;
    const t0 = Date.now();
    try {
      if (job.w !== vw || job.h !== vh) { vw = job.w; vh = job.h; await page.setViewportSize({ width: vw, height: vh }); }
      await page.evaluate(([svg, bg]) => {
        document.body.style.background = bg || 'transparent';
        document.getElementById('stage').innerHTML = svg;
        return document.fonts.ready;
      }, [job.svg, job.bg || null]);
      await page.screenshot({ path: job.out, clip: { x: 0, y: 0, width: job.w, height: job.h }, omitBackground: !job.bg });
      process.stdout.write(JSON.stringify({ id: job.id, ok: true, ms: Date.now() - t0 }) + '\n');
    } catch (e) {
      process.stdout.write(JSON.stringify({ id: job.id, ok: false, error: String(e) }) + '\n');
    }
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
