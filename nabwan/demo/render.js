// Usage:
//   node render.js stills <out_dir> t1 t2 ...      -> PNG stills at the given times
//   node render.js video <out.mp4> [fps]            -> silent H.264 video of the whole timeline
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');

(async () => {
  const [mode, out, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('pageerror:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('console:', m.text()); });
  await page.goto('file://' + path.join(__dirname, process.env.PAGE || 'index.html'));
  await page.evaluate(() => Promise.all(['400', '500', '600', '700'].map(w => document.fonts.load(`${w} 40px Kanit`, 'กขคงจ 0123 abc'))));
  await page.evaluate(() => window.ready);
  const frameEl = await page.$('#frame');
  if (mode === 'stills') {
    for (const t of rest.map(Number)) {
      await page.evaluate(t => window.render(t), t);
      await frameEl.screenshot({ path: path.join(out, `still_${t.toFixed(2)}.png`) });
      console.log('still', t);
    }
  } else {
    const fps = Number(rest[0] || 30);
    const dur = await page.evaluate(() => window.DURATION);
    // optional sub-range [t0, t1) for re-rendering one segment
    const i0 = rest[1] != null ? Math.round(Number(rest[1]) * fps) : 0;
    const n = rest[2] != null ? Math.round(Number(rest[2]) * fps) : Math.round(dur * fps);
    const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', String(fps), out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = i0; i < n; i++) {
      await page.evaluate(t => window.render(t), i / fps);
      const buf = await frameEl.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) console.log(`frame ${i}/${n} ${((Date.now() - t0) / 1000).toFixed(1)}s`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log('done', n, 'frames');
  }
  await browser.close();
})();
