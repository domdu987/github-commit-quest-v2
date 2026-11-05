// 16:9 band check: node snapFit.cjs <port> <out dir> t1 t2 ... → for each time, the whole vertical frame (fitted, the widened
// world included) with the 16:9 band outlined in red: anything outside the red box is cut from the long version.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(3000);
  const FIT = 1080 / 1920;
  const seek = (t) => p.evaluate(([t, FIT]) => { const tl = window.__timelines.main; tl.seek(+t, false);
    let info = ''; document.querySelectorAll('.bandbox').forEach((n) => n.remove());
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden';
      if (!on) return; info = c.id + ' ' + (c.dataset.land || ''); const vf = c.querySelector('.vf'); if (!vf) return;
      vf.style.transform = `translate(${(1920 - 1080 * FIT) / 2}px, 0px) scale(${FIT})`;
      const m = /y0=(\d+)/.exec(c.dataset.land || ''); if (!m) return; const y0 = +m[1];
      const bx = document.createElement('div'); bx.className = 'bandbox';
      Object.assign(bx.style, { position: 'absolute', left: `${(1920 - 1080 * FIT) / 2 - 660 * FIT}px`, top: `${y0 * FIT}px`, width: `${2400 * FIT}px`, height: `${1350 * FIT}px`,
        border: '4px solid #ff2020', boxSizing: 'border-box', zIndex: 99999, pointerEvents: 'none' });
      c.appendChild(bx); });
    return info; }, [t, FIT]);
  await seek(0.2); await p.waitForTimeout(1200); await seek(ts[0]); await p.waitForTimeout(1500);
  for (const t of ts) { const info = await seek(t); await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/t${(+t).toFixed(2)}.png` }); console.log(t, info); }
  await b.close(); })();
