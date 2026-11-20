// render.js -- rasterise the frame SVGs of a manifest with ONE persistent headless Chromium page (Playwright).
//
//   node render.js <manifest.json> [--dsf 1|2] [--only s01,s02] [--from N --to M] [--jpg] [--quality 98]
//
// manifest.json: {"width":720,"height":1280,"frames":[{"svg":"abs/path.svg","out":"abs/path.png","shot":"s01"}, ...]}
// One page is reused for every frame: the SVG text replaces the content of a fixed <div>, fonts are awaited once, and the
// screenshot is clipped to the frame.  No CSS animation, no timers, nothing random: a frame depends only on its SVG.
// --dsf 2 renders at 1440x2560 (supersampling); the post step scales it back to 720x1280 (bilinear), which matches the
// reference edge softness better than dsf 1 (10-90 percent edge rise 1.60 px against 1.39 px; reference 1.56-1.86 px).
// --jpg writes JPEG intermediates (PNG encoding is the bottleneck: 0.32 s against 0.10 s at dsf 1, 1.02 s against 0.32 s at
// dsf 2); at dsf 2 the JPEG loss is averaged away by the 2x downscale (mean difference under 2 levels).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function arg(name, dflt) {
  const i = process.argv.indexOf(name);
  return i > 0 && i + 1 < process.argv.length ? process.argv[i + 1] : dflt;
}

(async () => {
  const manifestPath = process.argv[2];
  if (!manifestPath) { console.error('usage: node render.js manifest.json [--dsf N] [--only shot,shot] [--from N] [--to M] [--jpg]'); process.exit(2); }
  const man = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const W = man.width || 720, H = man.height || 1280;
  const dsf = +arg('--dsf', man.dsf || 1);
  const only = arg('--only', '');
  const from = +arg('--from', 0), to = +arg('--to', 1e9);
  const jpg = process.argv.includes('--jpg');
  const quality = +arg('--quality', 98);
  let frames = man.frames;
  if (only) { const set = new Set(only.split(',')); frames = frames.filter(f => set.has(f.shot)); }
  frames = frames.filter((f, i) => i >= from && i <= to);

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: dsf });
  const page = await ctx.newPage();
  // the page itself: a black body, one stage, and a hidden line of text that forces the set's lettering fonts to load
  await page.setContent(`<!doctype html><html><head><style>
      html,body{margin:0;padding:0;background:#000;overflow:hidden}
      #stage{position:absolute;left:0;top:0;width:${W}px;height:${H}px;overflow:hidden}
      #stage svg{display:block}
      #warm{position:absolute;left:-9999px;top:0;font:bold 20px 'DejaVu Serif','Caladea','Liberation Serif',serif}
      #warm2{position:absolute;left:-9999px;top:40px;font:20px 'DejaVu Sans Mono','Liberation Mono',monospace}
    </style></head><body><div id="stage"></div><div id="warm">U.S. WEATHER BUREAU 0123456789</div><div id="warm2">0123456789</div></body></html>`);
  await page.evaluate(async () => { await document.fonts.ready; });
  const fontsOk = await page.evaluate(() => document.fonts.check("bold 20px 'DejaVu Serif'"));
  if (!fontsOk) console.warn('warning: DejaVu Serif Bold not reported as available; lettering will use a fallback');

  const t0 = Date.now();
  let n = 0, tParse = 0, tShot = 0;
  for (const f of frames) {
    const svg = fs.readFileSync(f.svg, 'utf8');
    const a = Date.now();
    await page.evaluate(async (s) => {
      document.getElementById('stage').innerHTML = s;
      await document.fonts.ready;                       // fonts referenced by this frame
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));   // let layout and paint settle
    }, svg);
    const b = Date.now();
    fs.mkdirSync(path.dirname(f.out), { recursive: true });
    const out = jpg ? f.out.replace(/\.png$/i, '.jpg') : f.out;
    await page.screenshot(Object.assign({ path: out, clip: { x: 0, y: 0, width: W, height: H } }, jpg ? { type: 'jpeg', quality } : {}));
    const c = Date.now();
    tParse += b - a; tShot += c - b; n++;
    if (n % 20 === 0 || n === frames.length) console.log(`  ${n}/${frames.length}  ${((c - t0) / n).toFixed(0)} ms per frame (set content ${(tParse / n).toFixed(0)}, screenshot ${(tShot / n).toFixed(0)})`);
  }
  await browser.close();
  console.log(`rendered ${n} frame(s) at ${W}x${H} dsf ${dsf} in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
})().catch(e => { console.error(e); process.exit(1); });
