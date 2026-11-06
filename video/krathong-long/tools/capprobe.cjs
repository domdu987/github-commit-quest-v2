const { chromium } = require('playwright');
(async () => { const [port, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  for (const t of ts) { const r = await p.evaluate((t) => { window.__timelines.main.seek(+t, false); const out = [];
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; if (!(+t >= s && +t < s + d)) return;
      const cw = c.querySelector('.capwrap'); out.push('capwrap top=' + (cw && cw.style.top) + ' cls=' + (cw && cw.className));
      c.querySelectorAll('.capbox').forEach((n) => { const r = n.getBoundingClientRect(); const o = getComputedStyle(n).opacity; out.push(`${n.textContent.slice(0, 30)} op=${(+o).toFixed(2)} y=${r.top | 0}-${r.bottom | 0}`); }); });
    return out.join('\n'); }, t); console.log('== ' + t + '\n' + r); }
  await b.close(); })();
