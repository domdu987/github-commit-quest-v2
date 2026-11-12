// clean frames (no captions, no badge) of a landscape build · usage: node clean.cjs <port> <out prefix> t1 t2 ...
const pw = require("playwright");
(async () => { const [port, pre, ...ts] = process.argv.slice(2);
  const b = await pw.chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  for (const t of ["40", ...ts]) { await p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(+t, false);
      document.querySelectorAll(".clip").forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? "visible" : "hidden"; });
      document.querySelectorAll(".capwrap,.badge,#badge").forEach((e) => (e.style.display = "none")); }, t);
    await p.waitForTimeout(300); await p.screenshot({ path: `${pre}-${t}.png` }); }
  await b.close(); })();
