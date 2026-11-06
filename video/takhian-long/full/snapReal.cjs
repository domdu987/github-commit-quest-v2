// node snapReal.cjs <port> <out dir> t1 t2 ... → the real 16:9 page at each time (as rendered), plus page errors
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message)); p.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(3000);
  const seek = (t) => p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false); let info = '';
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden'; if (on) info = c.id + ' ' + (c.dataset.land || ''); });
    return info; }, t);
  await seek(0.2); await p.waitForTimeout(800);
  for (const t of ts) { const info = await seek(t); await p.waitForTimeout(700); await p.screenshot({ path: `${out}/r${(+t).toFixed(2)}.jpg`, type: 'jpeg', quality: 80 }); console.log(t, info); }
  console.log('flashes', JSON.stringify(await p.evaluate(() => window.__flashes)));
  await b.close(); })();
