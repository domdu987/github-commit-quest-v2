// Walk a built episode every 0.25 s and report captions, bubbles, choice buttons, UI cards and screen-space graphics that are
// visible but leave the screen (cut by an edge) — the user notices half-cut labels at once.
// It also fails on duplicated DOM ids, which make GSAP animate the wrong element (captions vanish or jump order).
// usage: node edgecheck.cjs <port> <schedule.json>   (exit 1 on any problem)
let playwright;
try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }
const fs = require('fs');
(async () => {
  const [port, schedPath] = process.argv.slice(2);
  if (!port || !schedPath) { console.error('usage: node edgecheck.cjs <port> <schedule.json>'); process.exit(2); }
  const sc = JSON.parse(fs.readFileSync(schedPath, 'utf8'));
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`);
  await p.waitForTimeout(2500);
  // A duplicated DOM id makes GSAP animate every element that carries it ("#x" selects all of them).
  // krathong EP.1 cut 15: click labels named `${id}-c${c}` took the caption ids `${id}-c${k}` and hijacked the captions.
  // Paint servers repeated with identical markup (the same gradient or clipPath placed twice by a library) are harmless:
  // url(#x) resolves to the first copy, which is the same. Different markup under one id, or any duplicated id outside
  // <defs> (captions, labels, props), is a failure.
  const { dups, same } = await p.evaluate(() => {
    const by = {};
    document.querySelectorAll('[id]').forEach((e) => { if (e.id) (by[e.id] = by[e.id] || []).push(e); });
    const paint = /^(lineargradient|radialgradient|clippath|mask|filter|pattern|symbol|marker)$/i;
    const dups = [], same = [];
    for (const [id, els] of Object.entries(by)) {
      if (els.length < 2) continue;
      const defsOnly = els.every((e) => paint.test(e.tagName) || e.closest('defs'));
      const identical = els.every((e) => e.outerHTML === els[0].outerHTML);
      (defsOnly && identical ? same : dups).push(`${id}×${els.length}`);
    }
    return { dups, same };
  });
  if (same.length) console.log(`note: ${same.length} identical defs repeated (harmless): ${same.slice(0, 12).join(' ')}${same.length > 12 ? ' …' : ''}`);
  if (dups.length) console.log(`DUPLICATE IDS ${dups.length}: ${dups.slice(0, 40).join(' ')}${dups.length > 40 ? ' …' : ''}`);
  const seen = new Set();
  let n = 0;
  for (const x of sc.shots) {
    for (let t = x.start + 0.1; t < x.start + x.dur; t += 0.25) {
      const r = await p.evaluate((t) => {
        const tl = window.__timelines.main; tl.seek(+t, false);
        document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; });
        const vis = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return 0; o *= +cs.opacity; } return o; };
        const sel = '.capbox, .bubble, .opt, .gui, .apill, .sfxw, [id^="ui"]';
        const out = [];
        document.querySelectorAll(sel).forEach((g) => {
          if (/-/.test(g.id || '') && g.id.startsWith('ui')) return; // only the outer group of a screen-space graphic
          if (vis(g) < 0.35) return;
          const rc = g.getBoundingClientRect(); if (rc.width < 2 || rc.height < 2) return;
          const bad = [];
          if (rc.left < 6) bad.push('L' + Math.round(rc.left)); if (rc.right > 1074) bad.push('R' + Math.round(rc.right));
          if (rc.top < 6) bad.push('T' + Math.round(rc.top)); if (rc.bottom > 1914) bad.push('B' + Math.round(rc.bottom));
          if (bad.length) out.push(`${g.className && g.className.baseVal === undefined ? g.className : (g.id || g.tagName)} "${(g.textContent || '').trim().slice(0, 28)}" ${bad.join(',')}`);
        });
        return out;
      }, t);
      for (const m of r) { const k = x.key + '|' + m.slice(0, 40); if (!seen.has(k)) { seen.add(k); n++; console.log(x.key, t.toFixed(2), m); } }
    }
  }
  if (dups.length) console.log(`${dups.length} duplicate ids · rename them (e.g. a prop label "-clk<n>", never "-c<n>", which the engine uses for captions)`);
  console.log(n ? `${n} edge problems` : (dups.length ? 'edges ok but duplicate ids' : 'no edge problems'));
  if (n || dups.length) process.exitCode = 1;
  await b.close();
})();
