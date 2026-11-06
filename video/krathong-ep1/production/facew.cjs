// node facew.cjs <port> t...: width (page px at 1080 wide) of every visible rig head at t — the face_w of the CINEMA BIBLE
const { chromium } = require('playwright');
(async () => {
  const [port, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(3000);
  for (const t of ts) {
    const r = await p.evaluate((t) => { window.__timelines.main.seek(+t, false); const out = [];
      document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden';
        if (on) c.querySelectorAll('[id$="-head"]').forEach((h) => { if (!/-a\d+-head$/.test(h.id)) return; const r = h.getBoundingClientRect(); if (r.width > 4 && r.right > 0 && r.left < 1080 && r.bottom > 0 && r.top < 1920) out.push(`${h.id}:${Math.round(r.width)}`); }); });
      return out.join(' '); }, t);
    console.log(t, r);
  }
  await b.close(); })();
