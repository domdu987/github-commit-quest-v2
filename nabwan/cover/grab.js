// grab clean frames (no captions) from a story page: node cover/grab.js <page.html> <outdir> t1 t2 ...
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [pg, out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.error('pageerror', e.message));
  await p.goto('file://' + path.resolve(pg));
  await p.evaluate(() => Promise.all(['400', '500', '600', '700'].map(w => document.fonts.load(`${w} 40px Kanit`, 'กขคง 0123'))));
  await p.evaluate(() => window.ready);
  await p.evaluate(h => { window.HIDE = h; }, process.env.HIDE || '');
  const fr = await p.$('#frame');
  for (const t of ts.map(Number)) {
    await p.evaluate(t => { window.render(t); document.getElementById('subs').style.visibility = 'hidden'; if (window.HIDE) document.querySelectorAll(window.HIDE).forEach(e => e.style.visibility = 'hidden'); }, t);
    await fr.screenshot({ path: path.join(out, `${path.basename(path.dirname(path.resolve(pg)))}_${t.toFixed(2)}.png`) });
  }
  await b.close();
})();
