// node whatis.cjs <port> t x y : the elements under a page point at time t (innermost first, with their ancestry)
const { chromium } = require('playwright');
(async () => { const [port, t, x, y] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(4000);
  const seek = (t) => p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false); document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(1200); await seek(t); await p.waitForTimeout(1500);
  const r = await p.evaluate(([t, x, y]) => {
    return document.elementsFromPoint(+x, +y).slice(0, 6).map((e) => { let a = [], n = e; for (let k = 0; k < 6 && n; k++, n = n.parentElement) a.push(n.tagName + (n.id ? '#' + n.id : '') + (n.getAttribute && n.getAttribute('class') ? '.' + n.getAttribute('class') : '') + (n.getAttribute && n.getAttribute('transform') ? '[' + n.getAttribute('transform').slice(0, 40) + ']' : ''));
      return (e.outerHTML || '').slice(0, 160) + '\n      ' + a.join(' < '); }); }, [t, x, y]);
  console.log(r.join('\n')); await b.close(); })();
