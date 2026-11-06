// node headcap.cjs <port> <from> <to> [step]: per t, every actor's head box vs the visible caption box (page px)
const { chromium } = require('playwright');
(async () => {
  const [port, a, z, st = 0.1] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`, { timeout: 600000 }); await p.waitForTimeout(3000);
  for (let t = +a; t < +z; t += +st) {
    const r = await p.evaluate((t) => { window.__timelines.main.seek(+t, false); let clip;
      document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden'; if (on) clip = c; });
      const vis = (el) => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < 0.05) return false; } return true; };
      const caps = [...clip.querySelectorAll('.capbox')].filter(vis).map((e) => e.getBoundingClientRect());
      const heads = [...clip.querySelectorAll('[id$="-head"]')].filter((e) => /-a\d-head$/.test(e.id) && vis(e)).map((e) => { const r = e.getBoundingClientRect(); return [e.id, Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
      const cap = caps.length ? caps.map((r) => [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]) : [];
      return { cap, heads }; }, t);
    console.log(t.toFixed(2), JSON.stringify(r));
  }
  await b.close(); })();
