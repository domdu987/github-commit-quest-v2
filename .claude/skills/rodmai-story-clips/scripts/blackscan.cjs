// node blackscan.cjs <port> <outdir> — screenshot every clip at start+0.03 / +0.25 / mid and count pure-black pixels in the central band
const playwright = require('playwright'); const fs = require('fs'); const { PNG } = (() => { try { return require('pngjs'); } catch (e) { return {}; } })();
(async () => {
  const [port, dir] = process.argv.slice(2); fs.mkdirSync(dir, { recursive: true });
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html?`); await p.waitForTimeout(2500);
  const clips = await p.evaluate(() => [...document.querySelectorAll('.clip')].map((c) => ({ id: c.id, s: +c.dataset.start, d: +c.dataset.duration })));
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false);
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(800);
  const rows = [];
  for (const c of clips) { for (const off of [0.03, 0.25, c.d / 2]) { const t = +(c.s + off).toFixed(2); await seek(t); await p.waitForTimeout(350);
    const buf = await p.screenshot({ clip: { x: 0, y: 220, width: 1080, height: 1480 } }); const f = `${dir}/${c.id}_${t}.png`; fs.writeFileSync(f, buf); rows.push(`${c.id} ${t} ${f}`); } }
  fs.writeFileSync(`${dir}/list.txt`, rows.join('\n')); await b.close();
})();
