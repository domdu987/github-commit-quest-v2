// Look at frames without rendering: seek the composition's timeline and screenshot each time.
// Serve the built project first:  (cd <work>/hf/<proj> && (python3 -m http.server <port> >/dev/null 2>&1 &))
// usage: node snap.cjs <port> <out dir> t1 t2 ...      → <out dir>/t<sec>.png (1080×1920)
// Console errors and warnings of the page are printed (a page error usually means a broken shot).
// The first screenshot after load can paint a stale frame, so a throw-away frame is taken first.
let playwright;
try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }
const fs = require('fs');
(async () => {
  const [port, out, ...ts] = process.argv.slice(2);
  if (!port || !out || !ts.length) { console.error('usage: node snap.cjs <port> <out dir> t1 t2 ...'); process.exit(2); }
  fs.mkdirSync(out, { recursive: true });
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('CONSOLE', m.type(), m.text()); });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`);
  await p.waitForTimeout(2500);
  const seek = (t) => p.evaluate((t) => {
    const tl = window.__timelines.main; tl.seek(+t, false); // events on: the camera is driven by onUpdate
    document.querySelectorAll('.clip').forEach((c) => {
      const s = +c.dataset.start, d = +c.dataset.duration;
      c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden';
    });
  }, t);
  await seek(0.2); await p.waitForTimeout(1200); // warm-up frame, not saved
  await seek(ts[0]); await p.waitForTimeout(1500); // heavy first shots (blur filters, big paths) can still paint black on the first real frame
  for (const t of ts) {
    await seek(t);
    await p.waitForTimeout(400);
    await p.screenshot({ path: `${out}/t${(+t).toFixed(2)}.png` });
  }
  // the first real frame can still come out half-painted (black blocks): shoot it again now that the page is warm
  if (ts.length > 1) { await seek(ts[0]); await p.waitForTimeout(800); await p.screenshot({ path: `${out}/t${(+ts[0]).toFixed(2)}.png` }); }
  await b.close();
})();
