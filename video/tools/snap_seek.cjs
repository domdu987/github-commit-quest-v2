// fast frame check without a render: seek the timeline and screenshot. Serve the project first (python3 -m http.server <port> in hf/<proj>)
// usage: node snap_seek.cjs <port> <outdir> t1 t2 ...   (seek(t, false): with events on, or the camera onUpdate never runs)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('CONSOLE', m.type(), m.text()); });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  for (const t of ts) {
    await p.evaluate((t) => {
      const tl = window.__timelines.main; tl.seek(+t, false);
      document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; });
    }, t);
    await p.waitForTimeout(120);
    await p.screenshot({ path: `${out}/t${(+t).toFixed(2)}.png` });
  }
  await b.close();
})();
