// For every fitted clip (data-land="fit") of a landscape build: screenshot its middle frame, keep the centre column (the fitted card),
// blow it up to 1920×1080, blur and dim it → assets/bg-<i>.jpg, and write assets/landbg.js (shot key -> image) for landscape.js.
// usage: node fitbg.cjs <port> <project dir> <vertical schedule.json> [src.json: shot key -> the time of a wide shot of the same place]
// With src.json the blow-up comes from that wide shot (the place the card belongs to), else from the shot itself.
const pw = require('playwright'); const fs = require('fs'); const { execFileSync } = require('child_process');
(async () => {
  const [port, dir, schedPath, srcPath] = process.argv.slice(2);
  const SRC = srcPath ? JSON.parse(fs.readFileSync(srcPath, 'utf8')) : {};
  const b = await pw.chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  const clips = await p.evaluate(() => [...document.querySelectorAll('.clip')].map((c, i) => ({ i, id: c.id, land: c.dataset.land, world: (c.dataset.world || '').split(',').map(Number) })));
  const keys = await p.evaluate(() => (window.__shotKeys || null));
  const sched = JSON.parse(fs.readFileSync(schedPath, "utf8")).shots;
  const map = {};
  for (const c of clips) {
    const w = c.world; const narrow = c.land === 'fit' || w.length < 4 || w[0] > -480 || w[2] < 1560;
    if (!narrow) continue;
    const sh = sched[c.i]; if (!sh) continue;
    const own = SRC[sh.key] == null; const t = own ? sh.start + sh.dur * 0.55 : SRC[sh.key];
    await p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false); }, t); await p.waitForTimeout(400);
    await p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t - 0.02, false); tl.seek(+t, false); }, t); await p.waitForTimeout(600);
    const raw = `${dir}/assets/bgraw-${c.i}.png`; await p.screenshot({ path: raw, clip: !own ? { x: 0, y: 0, width: 1920, height: 1080 } : c.land === 'fit' ? { x: 656, y: 0, width: 608, height: 1080 } : { x: Math.max(0, Math.round(528 + 0.8 * Math.max(w[0], -660))) + 40, y: 0, width: Math.min(1920, Math.round(0.8 * (Math.min(w[2], 1740) - Math.max(w[0], -660)))) - 80, height: 1080 } });
    const out = `assets/bg-${c.i}.jpg`;
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', raw, '-vf', 'scale=1920:-2,crop=1920:1080,gblur=sigma=38,eq=brightness=-0.16:saturation=0.75', '-q:v', '4', `${dir}/${out}`]);
    fs.unlinkSync(raw); map[sh.key] = out; console.log('bg', c.i, sh.key, t.toFixed(2));
  }
  fs.writeFileSync(`${dir}/assets/landbg.js`, `window.LANDBG = ${JSON.stringify(map)};\n`);
  await b.close();
})();
