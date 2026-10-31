// เรนเดอร์ทุกเฟรมด้วย Playwright/Chromium แล้วต่อเป็น MP4 ด้วย ffmpeg
// ใช้: node render/render.js [--from 0 --to 80] [--step 1] [--workers 4] [--jpeg]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const args = Object.fromEntries(process.argv.slice(2).map((a, i, arr) => a.startsWith('--') ? [a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true] : []).filter(x => x.length));
const root = path.join(__dirname, '..');
const tl = JSON.parse(fs.readFileSync(path.join(root, 'audio', 'timeline.json'), 'utf8'));
const FPS = tl.fps, from = parseFloat(args.from || 0), to = parseFloat(args.to || tl.total), workers = parseInt(args.workers || 4);
const framesDir = path.join(root, 'out', 'frames'); fs.mkdirSync(framesDir, { recursive: true });
const f0 = Math.floor(from * FPS), f1 = Math.ceil(to * FPS);
(async () => {
  const browser = await chromium.launch();
  const url = 'file://' + path.join(root, 'scenes', 'index.html');
  const t0 = Date.now();
  const ranges = Array.from({ length: workers }, (_, w) => [f0 + Math.floor((f1 - f0) * w / workers), f0 + Math.floor((f1 - f0) * (w + 1) / workers)]);
  await Promise.all(ranges.map(async ([a, b], w) => {
    const page = await browser.newPage({ viewport: { width: 720, height: 1280 }, deviceScaleFactor: 1 });
    page.on('pageerror', e => console.error('PAGE ERROR', e.message));
    await page.goto(url); await page.evaluate(() => window.READY);
    for (let f = a; f < b; f++) {
      const t = f / FPS;
      await page.evaluate(t => window.render(t), t);
      await page.screenshot({ path: path.join(framesDir, `f${String(f).padStart(5, '0')}.png`), type: 'png' });
      if (w === 0 && (f - a) % 60 === 0) console.log(`frame ${f}/${f1} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
    }
    await page.close();
  }));
  await browser.close();
  console.log('frames done', ((Date.now() - t0) / 1000).toFixed(0) + 's');
  if (args['no-video']) return;
  const out = path.join(root, 'out', 'zombie-condo-ep1.mp4');
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-framerate', String(FPS), '-start_number', String(f0), '-i', path.join(framesDir, 'f%05d.png'),
    '-i', path.join(root, 'audio', 'mix.wav'), '-ss', String(from), '-t', String(to - from),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], { stdio: 'inherit' });
  console.log('video:', out);
})();
