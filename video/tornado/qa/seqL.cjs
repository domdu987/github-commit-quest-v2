// node seqL.cjs <port> <out dir> <fps> <a-b> [<c-d> …] → JPEG frame sequences (1920×1080) for short motion previews,
// one fresh browser per range (stale paint tiles stay out), frames in <out>/seg<k>/f00000.jpg …
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, out, fpsS, ...ranges] = process.argv.slice(2); const fps = +fpsS;
  for (let k = 0; k < ranges.length; k++) {
    const [a, b] = ranges[k].split('-').map(Number); const dir = `${out}/seg${k}`; fs.mkdirSync(dir, { recursive: true });
    const br = await chromium.launch({ args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
    await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(4000);
    const seek = (t) => p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false);
      document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
    await seek(a); await p.waitForTimeout(1500);
    const n = Math.round((b - a) * fps);
    for (let i = 0; i < n; i++) { await seek(a + i / fps); await p.waitForTimeout(90);
      await p.screenshot({ path: `${dir}/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 85, timeout: 120000 }); }
    console.log('seg', k, a, b, n, 'frames'); await br.close();
  }
})();
