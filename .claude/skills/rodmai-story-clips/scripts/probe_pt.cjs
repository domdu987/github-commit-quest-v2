// node probe_pt.cjs <port> <query> <t> <selector>[,<selector>…]  — world (set-layer) coordinates of each element's bbox centre at time t
const playwright = require('playwright');
(async () => {
  const [port, q, t, sels, pre] = process.argv.slice(2);
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html?${q}`); await p.waitForTimeout(2000);
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false); document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  if (pre) await p.evaluate(pre); await seek(0.2); await p.waitForTimeout(500); await seek(t); await p.waitForTimeout(800);
  const out = await p.evaluate((sels) => sels.split(',').map((sel) => { const el = document.querySelector(sel); if (!el) return `${sel}: none`;
    const bb = el.getBBox(), m = el.getCTM(); const svg = el.ownerSVGElement; const layer = el.closest('[id$="-act"], [id$="-set"]') || svg; const lm = layer.getCTM().inverse();
    const pt = (x, y) => { const s = svg.createSVGPoint(); s.x = x; s.y = y; const a = s.matrixTransform(m).matrixTransform(lm); return [a.x.toFixed(0), a.y.toFixed(0)]; };
    const c = pt(bb.x + bb.width / 2, bb.y + bb.height / 2), tl = pt(bb.x, bb.y), br = pt(bb.x + bb.width, bb.y + bb.height); return `${sel}: centre ${c} · corners ${tl} ${br}`; }), sels);
  console.log(out.join('\n')); await b.close();
})();
