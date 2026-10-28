// Check every scale/rotation pivot (GSAP svgOrigin) against the element it turns, before a render.
// GSAP reads svgOrigin in the coordinates the element's shapes are drawn in (its parent's space when the element itself has no
// transform attribute) — verified 28 Oct 2026. A pivot given in screen/world coordinates for an element nested in a translated group
// makes it swing in from far away (เห็ดปอบ EP.3: the board labels flew in from off-screen).
// usage: node origin_check.cjs <port> <body.part or shots.part>
//   finds  tl.fromTo/to/set("#id" | ["#a", "#b"], { ... svgOrigin: "x y" ... })  in the file, loads the served page,
//   and prints ok/BAD per target: BAD = the pivot lies more than 60 units outside the element's own bounding box.
let playwright;
try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }
const fs = require('fs');
(async () => {
  const [port, file] = process.argv.slice(2);
  if (!port || !file) { console.error('usage: node origin_check.cjs <port> <body.part>'); process.exit(2); }
  const src = fs.readFileSync(file, 'utf8');
  const items = [];
  const re = /tl\.(?:fromTo|to|from|set)\(\s*(\[[^\]]*\]|["'`][^"'`]+["'`])\s*,[^;]*?svgOrigin:\s*"([-\d.]+ [-\d.]+)"/g;
  for (let m; (m = re.exec(src));) {
    const sels = m[1].startsWith('[') ? m[1].slice(1, -1).split(',').map((s) => s.trim().replace(/^["'`]|["'`]$/g, '')) : [m[1].slice(1, -1)];
    sels.forEach((s) => { if (!s.includes('${')) items.push([s, m[2]]); });
  }
  if (!items.length) { console.log('no svgOrigin pivots with literal selectors found'); return; }
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html`);
  await p.waitForTimeout(2500);
  const res = await p.evaluate((items) => items.map(([sel, o]) => {
    const e = document.querySelector(sel);
    if (!e || !e.getBBox) return `MISSING ${sel}`;
    const bb = e.getBBox(), [ox, oy] = o.split(' ').map(Number), m = 60;
    const inside = ox >= bb.x - m && ox <= bb.x + bb.width + m && oy >= bb.y - m && oy <= bb.y + bb.height + m;
    return `${inside ? 'ok ' : 'BAD'} ${sel} pivot(${o}) box(${Math.round(bb.x)},${Math.round(bb.y)} ${Math.round(bb.width)}x${Math.round(bb.height)})${e.getAttribute('transform') ? ' has transform attr!' : ''}`;
  }), items);
  console.log(res.join('\n'));
  await b.close();
})();
