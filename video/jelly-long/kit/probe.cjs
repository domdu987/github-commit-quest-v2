const pw = require('playwright');
(async () => { const b = await pw.chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${process.argv[2]}/index.html`); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => [...document.querySelectorAll('.clip')].map((c) => { const svg = c.querySelector('svg.stage'); const vb = svg.viewBox.baseVal;
    const s = svg.getBoundingClientRect(); const kx = vb.width / s.width;
    const box = (k) => { const e = document.getElementById(c.id + '-' + k); if (!e) return '-'; const q = e.getBoundingClientRect(); return q.width ? [Math.round(vb.x + (q.left - s.left) * kx), Math.round(vb.x + (q.right - s.left) * kx)].join('..') : '0'; };
    return c.id + ' ' + c.dataset.land + ' sky ' + box('sky') + ' far ' + box('far') + ' mid ' + box('mid') + ' set ' + box('set'); }));
  console.log(r.join('\n')); await b.close(); })();
