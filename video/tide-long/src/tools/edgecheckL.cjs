// 16:9 variant of .claude/skills/rodmai-club-video/scripts/edgecheck.cjs: walk a built part every 0.25 s and report captions, bubbles,
// SFX words, the badge, and text in the screen-space UI layers (-light / -lightwide) that are visible but leave the 1920x1080 page.
// usage: node edgecheckL.cjs <port> <schedule.json>
const playwright = require('playwright'); const fs = require('fs');
(async () => {
  const [port, schedPath] = process.argv.slice(2);
  const sc = JSON.parse(fs.readFileSync(schedPath, 'utf8'));
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  const seen = new Set(); let n = 0, steps = 0;
  for (const x of sc.shots) {
    for (let t = x.start + 0.1; t < x.start + x.dur; t += 0.25) {
      steps++;
      const r = await p.evaluate((t) => {
        const tl = window.__timelines.main; tl.seek(+t, false);
        document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; });
        const vis = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return 0; o *= +cs.opacity; } return o; };
        const els = [...document.querySelectorAll('.capbox, .bubble, .sfxw, .badge, [id$="-light"] text, [id$="-lightwide"] text')];
        const out = [];
        els.forEach((g) => {
          if (vis(g) < 0.35) return;
          const rc = g.getBoundingClientRect(); if (rc.width < 2 || rc.height < 2) return;
          const bad = [];
          if (rc.left < 6) bad.push('L' + Math.round(rc.left)); if (rc.right > 1914) bad.push('R' + Math.round(rc.right));
          if (rc.top < 6) bad.push('T' + Math.round(rc.top)); if (rc.bottom > 1074) bad.push('B' + Math.round(rc.bottom));
          if (bad.length) out.push(`${g.tagName.toLowerCase()}${typeof g.className === 'string' && g.className ? '.' + g.className : ''} "${(g.textContent || '').trim().slice(0, 28)}" ${bad.join(',')}`);
        });
        return out;
      }, t);
      for (const m of r) { const k = x.key + '|' + m.slice(0, 40); if (!seen.has(k)) { seen.add(k); n++; console.log(x.key, t.toFixed(2), m); } }
    }
  }
  console.log(n ? `${n} edge problems (${steps} steps)` : `no edge problems (${steps} steps)`);
  await b.close();
})();
