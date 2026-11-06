// node bikemeas.cjs <port> t...: page-px heights of every visible parked/riding bike and every visible rig actor at each t
const { chromium } = require('playwright');
(async () => {
  const [port, ...ts] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(`http://localhost:${port}/index.html`, { timeout: 600000 }); await p.waitForTimeout(3000);
  for (const t of ts) {
    const r = await p.evaluate((t) => { window.__timelines.main.seek(+t, false);
      let shot = ''; document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden'; if (on) shot = c.id; });
      const vis = (el) => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < 0.05) return false; } return true; };
      const box = (e) => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; };
      const out = { shot, bikes: [], actors: [] };
      document.querySelectorAll('[id]').forEach((e) => { if (!vis(e)) return; const id = e.id;
        if (/bk\d+$/.test(id) || /bike$/i.test(id)) out.bikes.push([id, ...box(e)]);
        else if (/-a\d$/.test(id)) { const q = (k) => e.querySelector(`#${id}-${k}`); const h = q('head'), f1 = q('shF'), f2 = q('shB');
          if (h && f1) { const top = h.getBoundingClientRect().top, bot = Math.max(f1.getBoundingClientRect().bottom, f2 ? f2.getBoundingClientRect().bottom : 0); out.actors.push([id, Math.round(bot - top)]); } } });
      return out; }, t);
    console.log(t, JSON.stringify(r));
  }
  await b.close(); })();
