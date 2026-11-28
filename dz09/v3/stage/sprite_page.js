// sprite_page.js -- ONE persistent headless Chromium page that turns SVG text into transparent RGBA PNG files.
//
//   node sprite_page.js            (started and fed by sprites.py; not meant to be run by hand)
//
// Protocol: one JSON object per line on stdin, one JSON reply per line on stdout.
//   {"id": 7, "svg": "<svg ...>...</svg>", "w": 928, "h": 1136, "out": "/abs/file.png", "mode": "canvas" | "screenshot"}
//   -> {"id": 7, "ok": true, "ms": 24.1}          or {"id": 7, "ok": false, "error": "..."}
//   {"cmd": "quit"} closes the browser.
// mode "canvas" (default): the SVG is decoded as an image, drawn into a 2D canvas and encoded with canvas.toBlob (PNG,
//   straight alpha).  About 25 ms for a 928x1136 sprite.
// mode "screenshot": the SVG is put into the DOM and captured with page.screenshot(omitBackground) exactly as v2/render.js
//   does (about 85 ms).  Both routes use the same Skia rasteriser; they differ only in a few edge pixels.
// Nothing here is timed, random or animated: a PNG depends only on its SVG text and size.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

(async () => {
  const browser = await chromium.launch();
  let vw = 1024, vh = 1280;
  const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.setContent(`<!doctype html><html><head><style>
      html,body{margin:0;padding:0;background:transparent;overflow:hidden}
      #stage{position:absolute;left:0;top:0}
      #stage svg{display:block}
    </style></head><body><div id="stage"></div><canvas id="cv" style="display:none"></canvas></body></html>`);

  async function viaCanvas(job) {
    const b64 = await page.evaluate(async ({ s, W, H }) => {
      const cv = document.getElementById('cv');
      if (cv.width !== W) cv.width = W;
      if (cv.height !== H) cv.height = H;
      const c = cv.getContext('2d');
      const url = URL.createObjectURL(new Blob([s], { type: 'image/svg+xml' }));
      const img = new Image();
      img.src = url;
      await img.decode();
      c.clearRect(0, 0, W, H);
      c.drawImage(img, 0, 0, W, H);
      URL.revokeObjectURL(url);
      const blob = await new Promise(r => cv.toBlob(r, 'image/png'));
      const buf = new Uint8Array(await blob.arrayBuffer());
      let bin = '';
      const CH = 0x8000;
      for (let i = 0; i < buf.length; i += CH) bin += String.fromCharCode.apply(null, buf.subarray(i, i + CH));
      return btoa(bin);
    }, { s: job.svg, W: job.w, H: job.h });
    fs.writeFileSync(job.out, Buffer.from(b64, 'base64'));
  }

  async function viaScreenshot(job) {
    if (job.w > vw || job.h > vh) {
      vw = Math.max(vw, job.w); vh = Math.max(vh, job.h);
      await page.setViewportSize({ width: vw, height: vh });
    }
    await page.evaluate(async (s) => {
      document.getElementById('stage').innerHTML = s;
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, job.svg);
    await page.screenshot({ path: job.out, clip: { x: 0, y: 0, width: job.w, height: job.h }, omitBackground: true });
    await page.evaluate(() => { document.getElementById('stage').innerHTML = ''; });
  }

  const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
  process.stdout.write(JSON.stringify({ ready: true }) + '\n');
  for await (const line of rl) {
    if (!line.trim()) continue;
    let job;
    try { job = JSON.parse(line); } catch (e) { process.stdout.write(JSON.stringify({ ok: false, error: 'bad json' }) + '\n'); continue; }
    if (job.cmd === 'quit') break;
    const t0 = process.hrtime.bigint();
    try {
      fs.mkdirSync(path.dirname(job.out), { recursive: true });
      if (job.mode === 'screenshot') await viaScreenshot(job); else await viaCanvas(job);
      const ms = Number(process.hrtime.bigint() - t0) / 1e6;
      process.stdout.write(JSON.stringify({ id: job.id, ok: true, ms }) + '\n');
    } catch (e) {
      process.stdout.write(JSON.stringify({ id: job.id, ok: false, error: String(e && e.message || e) }) + '\n');
    }
  }
  await browser.close();
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
