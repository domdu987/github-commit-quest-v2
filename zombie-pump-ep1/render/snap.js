// ถ่ายภาพนิ่งหลายเวลาเพื่อตรวจภาพ: node render/snap.js 0.5 6 10 ...  -> out/snap_<t>.png + out/sheet.png
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
const root = path.join(__dirname, '..'); const times = process.argv.slice(2).map(Number);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 720, height: 1280 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message)); p.on('console', m => m.type() === 'error' && console.error('CONSOLE', m.text()));
  await p.goto('file://' + path.join(root, 'scenes', 'index.html')); await p.evaluate(() => window.READY);
  const files = [];
  for (const t of times) { await p.evaluate(t => window.render(t), t); const f = path.join(root, 'out', `snap_${t}.png`); await p.screenshot({ path: f }); files.push(f); }
  await b.close();
  if (files.length === 1) { console.log('snap:', files[0]); return; }
  const cols = Math.min(4, files.length), rows = Math.ceil(files.length / cols);
  const args = ['-y', '-v', 'error']; files.forEach(f => args.push('-i', f));
  const layout = files.map((_, i) => `${(i % cols) * 360}_${Math.floor(i / cols) * 640}`).join('|');
  args.push('-filter_complex', files.map((_, i) => `[${i}:v]scale=360:640[s${i}]`).join(';') + ';' + files.map((_, i) => `[s${i}]`).join('') + `xstack=inputs=${files.length}:layout=${layout}:fill=black[o]`, '-map', '[o]', path.join(root, 'out', 'sheet.png'));
  execFileSync('ffmpeg', args); console.log('sheet:', path.join(root, 'out', 'sheet.png'));
})();
