// node headcut.cjs <port> <schedule.json> [step]: walk a 16:9 long section every step s (default 0.25) and report every rig head that is
// partly outside the 1920×1080 page (a face cut by the frame edge), plus heads under the caption box. One line per shot+head with the times.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [port, sched, step = '0.25'] = process.argv.slice(2);
  const S = JSON.parse(fs.readFileSync(sched, 'utf8'));
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(3000);
  const hits = {};
  for (let t = 0.05; t < S.total; t += +step) {
    const r = await p.evaluate((t) => { window.__timelines.main.seek(+t, false); const out = [];
      document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration, on = +t >= s && +t < s + d; c.style.visibility = on ? 'visible' : 'hidden';
        if (!on) return;
        const cap = [...c.querySelectorAll('.capbox')].filter((n) => getComputedStyle(n).opacity > 0.3 && n.getBoundingClientRect().width > 0).map((n) => n.getBoundingClientRect());
        c.querySelectorAll('[id$="-head"]').forEach((h) => { if (!/-a\d+-head$/.test(h.id)) return; const r = h.getBoundingClientRect();
          if (r.width < 6) return; let o = getComputedStyle(h).opacity; for (let n = h; n && n !== c; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.opacity === '0' || cs.visibility === 'hidden' || cs.display === 'none') return; }
          if (r.right <= 0 || r.left >= 1920 || r.bottom <= 0 || r.top >= 1080) return;  // fully outside: not seen
          const cut = r.left < 0 || r.right > 1920 || r.top < 0 || r.bottom > 1080;
          const under = cap.some((k) => k.left < r.right && k.right > r.left && k.top < r.bottom - r.height * 0.3 && k.bottom > r.top + r.height * 0.3);
          if (cut || under) out.push(`${c.dataset.start}|${h.id.replace(c.id + '-', '')}|${cut ? 'EDGE' : ''}${under ? 'CAPTION' : ''}`); }); });
      return out; }, t);
    r.forEach((k) => { (hits[k] = hits[k] || []).push(+t.toFixed(2)); });
  }
  const keyOf = (st) => (S.shots.find((x) => Math.abs(x.start - +st) < 0.01) || {}).key;
  const lines = Object.entries(hits).map(([k, ts]) => { const [sid, head, why] = k.split('|'); return `${keyOf(sid)} ${head} ${why} ${ts[0]}–${ts[ts.length - 1]} (${ts.length})`; });
  console.log(lines.length ? lines.join('\n') : 'no cut heads'); await b.close();
})();
