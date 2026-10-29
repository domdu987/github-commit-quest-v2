// "9 ผ้าพันคอ" sets: ยาย's Lanna house porch on a Chiang Rai hillside at dawn (kalae gable, clay charcoal stove, paper
// lantern, rattan yarn basket, a sea of fog between lavender ridges, Mexican-sunflower บัวตอง in the garden), the misty
// village lane with a red mailbox and Lanna ตุง flags, and the Bangkok condo studio in butter yellow and terracotta (day:
// blazing window, AC, fan; night: lamp, BTS train past the window), plus the drawer of nine scarves for the insert.
// Every set returns { people, shadowL, top, light, update(t), ... }.

function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}
// dawn / morning sky over layered ridges with a drifting sea of fog; returns update(t)
function hillsFar(F, mode = 'dawn', o = {}) {
  const dawn = mode === 'dawn';
  svg('rect', { x: -300, y: -300, width: 1680, height: 1700, fill: lin(F.defs, dawn ? [[0, '#5e4f7e'], [0.42, '#c98a8e'], [0.7, '#f2b48a'], [1, '#f8d79e']] : [[0, '#a890b4'], [0.45, '#efbfa2'], [1, '#fbe4b4']]) }, F.s);
  const sx = o.sunX ?? 860, sy = dawn ? 900 : 660;
  svg('circle', { cx: sx, cy: sy, r: 520, fill: rad2(F.defs, [[0, '#fff1c4', 0.75], [0.35, '#ffd9a0', 0.35], [1, '#ffd9a0', 0]]) }, F.s);
  svg('circle', { cx: sx, cy: sy, r: 70, fill: '#fff6dc' }, F.s);
  const r = rng(o.seed || 701);
  const birds = Array.from({ length: 5 }, () => ({ x: r() * 1200 - 100, y: 300 + r() * 300, sp: 20 + r() * 20, ph: r() * 6, el: svg('path', { fill: 'none', stroke: '#5a4660', 'stroke-width': 3, 'stroke-linecap': 'round' }, F.s) }));
  const cols = dawn ? ['#9a7ea8', '#856a98', '#6e5888', '#55456e'] : ['#b8a2c4', '#9c86b4', '#7e6a9e', '#5e4e7e'];
  const fogs = [];
  [890, 975, 1060, 1150].forEach((yb, i) => {
    let d = `M-300,${yb + 400} L-300,${yb}`;
    for (let x = -300; x <= 1400; x += 60) d += ` L${x},${(yb - 40 - 50 * Math.sin(x / (180 + i * 40) + i * 2) - 30 * Math.sin(x / 70 + i)).toFixed(1)}`;
    svg('path', { d: d + ` L1400,${yb + 400} Z`, fill: cols[i] }, F.s);
    if (i >= 2) for (let k = 0; k < 9; k++) { const px = -250 + r() * 1600, py = yb - 50 - 40 * Math.sin(px / (180 + i * 40) + i * 2); svg('path', { d: `M${px},${py - 60 - i * 6} L${px - 16},${py + 4} L${px + 16},${py + 4} Z`, fill: shade(cols[i], -12) }, F.s); }
    const fg = svg('g', { opacity: dawn ? 0.85 : 0.6, filter: blurFilter(F.defs, 10) }, F.s);
    for (let k = 0; k < 6; k++) svg('ellipse', { cx: -200 + k * 300 + r() * 80, cy: yb + 10, rx: 220 + r() * 120, ry: 34 + r() * 16, fill: dawn ? '#fdeee6' : '#fffaf2' }, fg);
    fogs.push({ g: fg, sp: 6 + i * 3 });
  });
  return t => {
    fogs.forEach((f, i) => f.g.setAttribute('transform', `translate(${(Math.sin(t * 0.15 + i) * 40 + t * f.sp % 200 - 100).toFixed(1)},0)`));
    birds.forEach(b => { const x = ((b.x + t * b.sp) % 1500) - 200, y = b.y + Math.sin(t * 0.8 + b.ph) * 10, w = 9 + 4 * Math.sin(t * 9 + b.ph); b.el.setAttribute('d', `M${(x - 12).toFixed(1)},${(y - w * 0.4).toFixed(1)} Q${(x - 6).toFixed(1)},${(y - w).toFixed(1)} ${x.toFixed(1)},${y.toFixed(1)} Q${(x + 6).toFixed(1)},${(y - w).toFixed(1)} ${(x + 12).toFixed(1)},${(y - w * 0.4).toFixed(1)}`); });
  };
}
// a Mexican-sunflower (บัวตอง) bloom at x,y (radius r)
function buaTong(g, x, y, r, a = 0) {
  const f = svg('g', { transform: `translate(${x},${y}) rotate(${a})` }, g);
  for (let k = 0; k < 9; k++) svg('ellipse', { cx: 0, cy: -r * 0.62, rx: r * 0.26, ry: r * 0.48, fill: k % 2 ? '#f6b42c' : '#f9c840', stroke: INK, 'stroke-width': 2, transform: `rotate(${k * 40})` }, f);
  svg('circle', { r: r * 0.36, fill: '#d9701c', stroke: INK, 'stroke-width': 2.5 }, f);
  svg('circle', { r: r * 0.14, fill: '#a84a10' }, f);
  return f;
}
function buaTongBush(g, x, y, s, seed) {
  const r = rng(seed);
  for (let k = 0; k < 7; k++) svg('path', { d: `M${x + (r() - 0.5) * 80 * s},${y} q${(r() - 0.5) * 40},${-80 * s} ${(r() - 0.5) * 60 * s},${-(120 + r() * 80) * s}`, fill: 'none', stroke: '#4f7a3a', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
  for (let k = 0; k < 8; k++) svg('ellipse', { cx: x + (r() - 0.5) * 140 * s, cy: y - (40 + r() * 120) * s, rx: 26 * s, ry: 12 * s, fill: ['#5a8a44', '#4f7a3a', '#6a9a4c'][k % 3], transform: `rotate(${(r() - 0.5) * 80} ${x} ${y})` }, g);
  const fl = [];
  for (let k = 0; k < 6; k++) fl.push(buaTong(g, x + (r() - 0.5) * 150 * s, y - (100 + r() * 120) * s, (18 + r() * 8) * s, r() * 40));
  return fl;
}
// Lanna paper lantern hanging at x,y; returns the group (sway it)
function lannaLantern(g, defs, x, y, lit) {
  const l = svg('g', {}, g);
  svg('path', { d: `M${x},${y - 200} L${x},${y}`, stroke: '#2a1a14', 'stroke-width': 3 }, l);
  if (lit) svg('circle', { cx: x, cy: y + 60, r: 170, fill: rad2(defs, [[0, '#ffb060', 0.45], [1, '#ffb060', 0]]), style: 'mix-blend-mode:screen' }, l);
  svg('path', { d: `M${x - 44},${y + 20} L${x + 44},${y + 20} L${x + 54},${y + 60} L${x + 44},${y + 100} L${x - 44},${y + 100} L${x - 54},${y + 60} Z`, fill: lit ? '#e0453b' : '#c8343c', stroke: INK, 'stroke-width': 4 }, l);
  for (const dx of [-26, 0, 26]) svg('path', { d: `M${x + dx},${y + 22} L${x + dx * 1.1},${y + 98}`, stroke: '#f2c14e', 'stroke-width': 3 }, l);
  svg('rect', { x: x - 48, y: y + 10, width: 96, height: 12, rx: 4, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, l);
  svg('rect', { x: x - 48, y: y + 98, width: 96, height: 12, rx: 4, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, l);
  for (let k = 0; k < 7; k++) svg('path', { d: `M${x - 42 + k * 14},${y + 110} l0,${40 + (k % 2) * 14}`, stroke: k % 2 ? '#f2c14e' : '#e0453b', 'stroke-width': 3, 'stroke-linecap': 'round' }, l);
  return l;
}
// Lanna kalae (crossed carved boards at the gable apex)
function kalae(g, x, y, s = 1) {
  const k = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  for (const sx of [-1, 1]) {
    svg('path', { d: `M0,60 L${sx * 70},-90 Q${sx * 96},-130 ${sx * 70},-150 Q${sx * 60},-120 ${sx * 50},-110 L${sx * -12},40 Z`, fill: '#7a4a2a', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, k);
    svg('path', { d: `M${sx * 30},-30 l${sx * 22},-30 M${sx * 46},-66 l${sx * 12},-18`, stroke: '#c99560', 'stroke-width': 4, 'stroke-linecap': 'round' }, k);
  }
  return k;
}

// =====================================================================
// A — ยาย's porch at dawn / in the morning
// =====================================================================
function lannaPorch(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, dawn = (o.mode || 'dawn') === 'dawn';
  const sky = hillsFar(F, o.mode || 'dawn', { sunX: 880 });
  // the house: plank wall with a shuttered window lit from inside, the deep roof with its kalae
  const wall = svg('g', {}, M.s);
  svg('rect', { x: -300, y: 300, width: 650, height: 1010, fill: '#6a3e26' }, wall);
  for (let x = -300; x < 350; x += 46) svg('rect', { x, y: 300, width: 3, height: 1010, fill: '#4a2a18', opacity: 0.7 }, wall);
  svg('rect', { x: 330, y: 300, width: 26, height: 1010, fill: '#5a321e', stroke: INK, 'stroke-width': 4 }, wall);
  svg('rect', { x: 20, y: 640, width: 220, height: 260, fill: '#2a1a14', stroke: INK, 'stroke-width': 5 }, wall);
  svg('rect', { x: 30, y: 650, width: 200, height: 240, fill: lin(M.defs, [[0, '#ffd9a0'], [1, '#e8a060']]) }, wall);
  svg('rect', { x: 50, y: 760, width: 160, height: 8, fill: '#8a5a32' }, wall);
  for (const [bx, c] of [[60, '#e0453b'], [86, '#f2c14e'], [112, '#7fb069'], [150, '#f6efe2']]) svg('rect', { x: bx, y: 724, width: 20, height: 36, rx: 3, fill: c, stroke: INK, 'stroke-width': 2 }, wall);
  for (const sx of [-1, 1]) svg('path', { d: sx < 0 ? 'M20,640 L-60,620 L-60,920 L20,900 Z' : 'M240,640 L320,620 L320,920 L240,900 Z', fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, wall);   // shutters
  svg('rect', { x: -40, y: 920, width: 300, height: 20, rx: 4, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, wall);
  for (const [px, c] of [[10, '#e0453b'], [110, '#f2a03a'], [210, '#e88aa8']]) { svg('path', { d: `M${px - 26},920 l52,0 l-8,-40 l-36,0 Z`, fill: '#b5583e', stroke: INK, 'stroke-width': 3 }, wall); for (let k = 0; k < 5; k++) svg('circle', { cx: px - 16 + k * 8, cy: 872 - (k % 2) * 8, r: 8, fill: c, stroke: INK, 'stroke-width': 1.5 }, wall); }   // geraniums on the sill
  // roof: deep eave over the porch, rafters, kalae at the apex
  svg('path', { d: 'M-300,-300 L-300,300 L820,470 L820,400 Q400,250 160,-300 Z', fill: '#4a2a1a', stroke: INK, 'stroke-width': 5 }, M.s);
  for (let k = 0; k < 9; k++) { const x0 = -260 + k * 120; svg('path', { d: `M${x0},${300 + (x0 + 300) * 0.152} L${x0 + 200},${-200}`, stroke: '#3a2012', 'stroke-width': 8 }, M.s); }
  svg('path', { d: 'M-300,300 L820,470', stroke: '#8a5a32', 'stroke-width': 18 }, M.s);
  kalae(M.s, 150, -40, 1.1);
  // porch floor, raised on stilts; the space underneath in shadow
  svg('rect', { x: -300, y: 1300, width: 1110, height: 34, fill: '#a87850', stroke: INK, 'stroke-width': 4 }, M.s);
  for (let x = -300; x < 810; x += 70) svg('path', { d: `M${x},1302 l0,30`, stroke: '#7a5032', 'stroke-width': 3 }, M.s);
  svg('rect', { x: -300, y: 1334, width: 1110, height: 34, fill: '#6a4028', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('rect', { x: -300, y: 1368, width: 1110, height: 700, fill: lin(M.defs, [[0, '#2a1a14'], [1, '#1a100c']]) }, M.s);
  for (const px of [-120, 180, 480, 760]) svg('rect', { x: px, y: 1368, width: 34, height: 600, fill: '#3a2418', stroke: INK, 'stroke-width': 3 }, M.s);
  // garden on the right: soil path, steps up, a bamboo fence, บัวตอง
  svg('path', { d: 'M780,1380 L1400,1380 L1400,2100 L780,2100 Z', fill: lin(M.defs, [[0, '#5a6a3a'], [0.3, '#3e4a2a'], [1, '#22281a']]) }, M.s);
  svg('path', { d: 'M820,1560 Q1000,1520 1400,1560 L1400,1660 Q1000,1610 820,1640 Z', fill: '#8a6a4a', opacity: 0.9 }, M.s);   // the path
  for (let k = 0; k < 4; k++) svg('rect', { x: 790 + k * 12, y: 1340 + k * 56, width: 120, height: 22, rx: 4, fill: '#9a7050', stroke: INK, 'stroke-width': 3.5 }, M.s);   // steps
  svg('rect', { x: 760, y: 420, width: 30, height: 900, fill: '#5a321e', stroke: INK, 'stroke-width': 4 }, M.s);   // porch post
  for (let x = 900; x < 1400; x += 34) svg('path', { d: `M${x},1400 l0,-120`, stroke: '#b89060', 'stroke-width': 8, 'stroke-linecap': 'round' }, M.s);
  svg('path', { d: 'M880,1330 L1400,1330 M880,1370 L1400,1370', stroke: '#a07a4a', 'stroke-width': 6 }, M.s);
  const tong = [...buaTongBush(M.s, 1000, 1520, 1.2, 703), ...buaTongBush(M.s, 1240, 1500, 1.4, 704), ...buaTongBush(M.s, 880, 1700, 1.1, 705)];
  wallAO(M.s, M.defs, 1300, { op: 0.26, h: 120 });
  // the porch things: rattan yarn basket, clay charcoal stove with kettle, a cat, a mug
  const bsk = svg('g', {}, M.s);
  svg('path', { d: 'M90,1300 L210,1300 L222,1230 L78,1230 Z', fill: '#c99a5a', stroke: INK, 'stroke-width': 4 }, bsk);
  bsk.setAttribute('transform', `translate(${o.basketDX ?? 0},0)`);
  for (let k = 0; k < 4; k++) svg('path', { d: `M${82 + k * 4},${1246 + k * 14} L${218 - k * 4},${1246 + k * 14}`, stroke: '#a07a3a', 'stroke-width': 3 }, bsk);
  [['#e0453b', 110, 1222], ['#f2c14e', 150, 1216], ['#7fb069', 188, 1224], ['#f6efe2', 132, 1206]].forEach(([c, x, y]) => yarnBall(bsk, M.defs, x, y, 20, c));
  svg('path', { d: 'M160,1214 l40,-70 M172,1218 l52,-60', stroke: '#d9b48a', 'stroke-width': 5, 'stroke-linecap': 'round' }, bsk);
  const stoveX = o.stoveX ?? 640;
  const stove = svg('g', {}, M.s);
  svg('path', { d: `M${stoveX - 56},1300 L${stoveX + 56},1300 L${stoveX + 70},1200 L${stoveX - 70},1200 Z`, fill: '#c97a4a', stroke: INK, 'stroke-width': 4 }, stove);
  svg('rect', { x: stoveX - 74, y: 1188, width: 148, height: 20, rx: 6, fill: '#a85a32', stroke: INK, 'stroke-width': 4 }, stove);
  svg('rect', { x: stoveX - 26, y: 1240, width: 52, height: 36, rx: 6, fill: '#2a1410', stroke: INK, 'stroke-width': 3 }, stove);
  const coals = [0, 1, 2, 3].map(k => svg('circle', { cx: stoveX - 16 + k * 11, cy: 1262 + (k % 2) * 6, r: 7, fill: '#ff7a2a' }, stove));
  svg('path', { d: `M${stoveX - 44},1188 C${stoveX - 48},1120 ${stoveX + 48},1120 ${stoveX + 44},1188 Z`, fill: '#9aa3b2', stroke: INK, 'stroke-width': 4 }, stove);   // kettle
  svg('path', { d: `M${stoveX + 40},1160 q34,-6 40,-30`, fill: 'none', stroke: INK, 'stroke-width': 8, 'stroke-linecap': 'round' }, stove);
  svg('path', { d: `M${stoveX - 30},1140 Q${stoveX},1100 ${stoveX + 30},1140`, fill: 'none', stroke: INK, 'stroke-width': 6 }, stove);
  const glow = lightPool(M.s, M.defs, stoveX, 1290, 260, 60, '#ff9a4a', 0.55);
  const glowUp = svg('circle', { cx: stoveX, cy: 1230, r: 260, fill: rad2(M.defs, [[0, '#ffa060', 0.32], [1, '#ffa060', 0]]), style: 'mix-blend-mode:screen' }, M.s);
  const steam = floaters(M.s, [stoveX + 60, 980, 120, 160], 7, 706, { color: '#ffffff', rMin: 8, rMax: 18, speed: 34, op: 0.3, base: 0.05, amp: 12 });
  const cat = sleepyCat(M.s, o.catX ?? 760, 1298, 0.62, '#4a3a3a', { f: -1 });
  const lantern = lannaLantern(M.s, M.defs, 560, 470, dawn);
  const fern = svg('g', {}, M.s);
  svg('path', { d: 'M-40,380 L-40,470', stroke: '#2a1a14', 'stroke-width': 3 }, fern);
  svg('path', { d: 'M-70,470 L-10,470 L-18,510 L-62,510 Z', fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, fern);
  for (let k = 0; k < 7; k++) svg('path', { d: `M-40,490 q${-50 + k * 16},${40 + (k % 3) * 20} ${-60 + k * 20},${120 + (k % 2) * 40}`, fill: 'none', stroke: ['#5a8a44', '#4f7a3a'][k % 2], 'stroke-width': 6, 'stroke-linecap': 'round' }, fern);
  // sunbeams from the right across the porch
  const shaft = lightShaft(M.s, M.defs, [[1100, 380], [1250, 520], [300, 1300], [80, 1200]], '#ffe2b0', dawn ? 0.16 : 0.24, 707, 24);
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, bsk);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.45);
  let bok = null, fore = null;
  if (R) {
    bok = bokehField(R.s, R.defs, 6, [-150, -100, 1230, 500], ['#fff1dc', '#ffd9b0'], 708, { rMin: 40, rMax: 90, op: 0.28 });
    fore = svg('g', {}, R.s);
    buaTong(fore, -40, 1880, 110, 10); buaTong(fore, 1130, 1840, 90, -20);
  }
  return {
    people, shadowL, top, ground: 1300, light: { ux: 0.9, uy: -0.35, lx: 1000 }, stoveX, tong,
    update(t) {
      sky(t); shaft(t); steam(t); cat(t);
      coals.forEach((c, i) => c.setAttribute('fill', ['#ff7a2a', '#ffb03a', '#e0452a'][Math.floor(t * 5 + i * 1.7) % 3]));
      const gl = 0.85 + 0.15 * Math.sin(t * 7) * Math.sin(t * 2.3); glow.setAttribute('opacity', gl.toFixed(3)); glowUp.setAttribute('opacity', gl.toFixed(3));
      lantern.setAttribute('transform', `rotate(${(Math.sin(t * 1.1) * 2).toFixed(2)} 560 270)`);
      fern.setAttribute('transform', `rotate(${(Math.sin(t * 1.3) * 1.5).toFixed(2)} -40 380)`);
      tong.forEach((f, i) => { const b = f.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); f.setAttribute('transform', `${b} skewX(${(Math.sin(t * 1.5 + i) * 3).toFixed(2)})`); });
      if (bok) bok(t);
    },
  };
}

// =====================================================================
// B — the misty village lane with the red mailbox and ตุง flags
// =====================================================================
function villagePost(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const sky = hillsFar(F, 'dawn', { sunX: 960, seed: 711 });
  // a house on the left; the wooden post office on the right with its sign, service window and counter ledge
  const hs = svg('g', {}, M.s);
  svg('rect', { x: -300, y: 780, width: 500, height: 700, fill: '#7a4a2a', stroke: INK, 'stroke-width': 5 }, hs);
  for (let px = -300; px < 200; px += 44) svg('rect', { x: px, y: 780, width: 3, height: 700, fill: '#3a2012', opacity: 0.6 }, hs);
  svg('path', { d: 'M-360,800 L-50,560 L260,800 Z', fill: '#4a2a1a', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, hs);
  kalae(hs, -50, 580, 0.8);
  svg('rect', { x: -200, y: 980, width: 200, height: 200, fill: '#ffd9a0', stroke: INK, 'stroke-width': 4 }, hs);
  for (let gx = -180; gx < 0; gx += 24) svg('path', { d: `M${gx},980 l0,200`, stroke: '#4a2a1a', 'stroke-width': 4 }, hs);
  // a big old tree behind
  svg('path', { d: 'M330,1480 Q310,1100 370,860 M370,960 Q450,880 530,860', fill: 'none', stroke: '#4a3424', 'stroke-width': 40, 'stroke-linecap': 'round' }, M.s);
  const r = rng(712);
  for (let i = 0; i < 18; i++) svg('ellipse', { cx: 190 + r() * 420, cy: 600 + r() * 300, rx: 80 + r() * 50, ry: 50 + r() * 30, fill: ['#4f7a3a', '#5a8a44', '#46703a'][i % 3] }, M.s);
  const po = svg('g', {}, M.s);
  svg('rect', { x: 540, y: 820, width: 800, height: 660, fill: '#8a5a36', stroke: INK, 'stroke-width': 5 }, po);
  for (let px = 540; px < 1340; px += 44) svg('rect', { x: px, y: 820, width: 3, height: 660, fill: '#4a2a18', opacity: 0.55 }, po);
  svg('path', { d: 'M480,840 L940,560 L1400,840 Z', fill: '#4a2a1a', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, po);
  kalae(po, 940, 580, 0.85);
  svg('rect', { x: 600, y: 870, width: 640, height: 80, rx: 8, fill: '#c8343c', stroke: INK, 'stroke-width': 5 }, po);
  wtext(po, 920, 926, 'ที่ทำการไปรษณีย์', 44, '#fbf2e2', { w: 700 });
  svg('rect', { x: 610, y: 975, width: 300, height: 225, fill: '#2a1a14', stroke: INK, 'stroke-width': 5 }, po);
  svg('rect', { x: 620, y: 985, width: 280, height: 205, fill: lin(M.defs, [[0, '#ffe2a8'], [1, '#d99a5a']]) }, po);
  svg('path', { d: 'M760,1190 L760,1100 Q800,1050 840,1100 L840,1190 Z M800,1080 m-26,0 a26,26 0 1,0 52,0 a26,26 0 1,0 -52,0', fill: '#6a4a3a', opacity: 0.55 }, po);   // the clerk inside
  for (let k = 0; k < 4; k++) svg('rect', { x: 640 + k * 60, y: 1000, width: 44, height: 30, rx: 3, fill: ['#f2c14e', '#e0453b', '#7fb069', '#f6efe2'][k], opacity: 0.8 }, po);   // parcels on a shelf
  svg('rect', { x: 596, y: 1214, width: 330, height: 20, rx: 4, fill: '#a87850', stroke: INK, 'stroke-width': 4 }, po);   // counter ledge
  svg('rect', { x: 1000, y: 1000, width: 240, height: 300, fill: '#ffd9a0', stroke: INK, 'stroke-width': 4 }, po);
  for (let gx = 1020; gx < 1240; gx += 26) svg('path', { d: `M${gx},1000 l0,300`, stroke: '#4a2a1a', 'stroke-width': 4 }, po);
  // lane
  svg('rect', { x: -300, y: 1480, width: 1680, height: 700, fill: lin(M.defs, [[0, '#7a5a42'], [0.25, '#4a3628'], [1, '#2a1e18']]) }, M.s);
  for (let i = 0; i < 20; i++) svg('ellipse', { cx: -200 + r() * 1400, cy: 1500 + r() * 300, rx: 8 + r() * 14, ry: 4 + r() * 5, fill: '#5a4232', opacity: 0.7 }, M.s);
  wallAO(M.s, M.defs, 1480, { op: 0.22, h: 100 });
  // ตุง flags on bamboo poles
  const flags = [];
  for (const [fx, c1, c2] of [[150, '#e0453b', '#f2c14e'], [470, '#f2a03a', '#e0453b'], [1250, '#7fb069', '#f6efe2']]) {
    svg('path', { d: `M${fx},1480 L${fx},660`, stroke: '#c9a24a', 'stroke-width': 9, 'stroke-linecap': 'round' }, M.s);
    const fg = svg('g', {}, M.s); flags.push({ g: fg, x: fx, c1, c2 });
  }
  // the red mailbox on its post
  const mbx = svg('g', {}, M.s), MX = o.boxX ?? 300;
  svg('rect', { x: MX - 10, y: 1260, width: 20, height: 220, fill: '#4a4a52', stroke: INK, 'stroke-width': 4 }, mbx);
  svg('rect', { x: MX - 56, y: 1110, width: 112, height: 160, rx: 14, fill: '#d8342c', stroke: INK, 'stroke-width': 5 }, mbx);
  svg('path', { d: `M${MX - 56},1124 Q${MX},1086 ${MX + 56},1124`, fill: '#b82a24', stroke: INK, 'stroke-width': 5 }, mbx);
  svg('rect', { x: MX - 36, y: 1140, width: 72, height: 12, rx: 6, fill: '#2a1a1a' }, mbx);   // slot
  svg('rect', { x: MX - 40, y: 1176, width: 80, height: 30, rx: 6, fill: '#f6efe2' }, mbx);
  wtext(mbx, MX, 1200, 'ไปรษณีย์', 20, '#d8342c', { w: 700 });
  svg('path', { d: `M${MX - 44},1230 l88,0`, stroke: '#f6efe2', 'stroke-width': 5 }, mbx);
  svg('path', { d: `M${MX - 46},1120 q8,-10 30,-12`, fill: 'none', stroke: '#fff', 'stroke-width': 5, opacity: 0.4, 'stroke-linecap': 'round' }, mbx);
  // a motorbike with a vegetable basket, a stone wall with flowers
  const mb = svg('g', {}, M.s);
  for (const wx of [1180, 1360]) { svg('circle', { cx: wx, cy: 1450, r: 36, fill: '#2a2226', stroke: INK, 'stroke-width': 4 }, mb); svg('circle', { cx: wx, cy: 1450, r: 12, fill: '#9aa3b2' }, mb); }
  svg('path', { d: 'M1160,1400 Q1240,1340 1330,1370 L1380,1360 L1400,1410 L1200,1430 Z', fill: '#4a7bd8', stroke: INK, 'stroke-width': 4 }, mb);
  
  svg('rect', { x: -300, y: 1400, width: 440, height: 80, fill: '#8a8278', stroke: INK, 'stroke-width': 4 }, M.s);
  for (let k = 0; k < 6; k++) buaTong(M.s, -240 + k * 70, 1394 - (k % 2) * 16, 22, k * 17);
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, mbx);
  const top = svg('g', {}, M.s);
  const mist = svg('g', { filter: blurFilter(M.defs, 14), opacity: 0.5 }, M.s);
  for (let k = 0; k < 5; k++) svg('ellipse', { cx: -100 + k * 300, cy: 1440, rx: 260, ry: 50, fill: '#fdeee6' }, mist);
  vignette(M.s, M.defs, 0.45);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 6, [-150, -100, 1230, 500], ['#fff1dc', '#ffd9b0'], 713, { rMin: 40, rMax: 90, op: 0.28 });
  return {
    people, shadowL, top, ground: 1480, boxX: MX, light: { ux: 0.9, uy: -0.4, lx: 1100 },
    update(t) {
      sky(t); if (bok) bok(t);
      mist.setAttribute('transform', `translate(${(Math.sin(t * 0.3) * 40).toFixed(1)},0)`);
      flags.forEach((f, i) => {
        let d = `M${f.x},680`; const n = 8;
        for (let k = 0; k <= n; k++) { const y = 680 + k * 52, w = Math.sin(t * 2.6 - k * 0.6 + i) * 12 * (k / n); d += ` L${(f.x + 54 + w).toFixed(1)},${y}`; }
        for (let k = n; k >= 0; k--) { const y = 680 + k * 52, w = Math.sin(t * 2.6 - k * 0.6 + i) * 12 * (k / n); d += ` L${(f.x + 6 + w).toFixed(1)},${y}`; }
        f.g.innerHTML = '';
        svg('path', { d: d + ' Z', fill: f.c1, stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, f.g);
        for (let k = 1; k < 8; k += 2) { const w = Math.sin(t * 2.6 - k * 0.6 + i) * 12 * (k / n); svg('rect', { x: f.x + 8 + w, y: 680 + k * 52, width: 44, height: 20, fill: f.c2 }, f.g); }
      });
    },
  };
}

// =====================================================================
// C — the Bangkok condo studio (day / night)
// =====================================================================
function bkkSkyline(F, x, y, w, h, night, seed) {
  svg('rect', { x, y, width: w, height: h, fill: lin(F.defs, night ? [[0, '#1e1a40'], [1, '#3a2e5a']] : [[0, '#f8d8a0'], [1, '#f2b07a']]) }, F.s);
  const r = rng(seed);
  if (!night) svg('circle', { cx: x + w * 0.72, cy: y + h * 0.22, r: 90, fill: rad2(F.defs, [[0, '#fffbe6', 1], [0.4, '#fff1c4', 0.7], [1, '#fff1c4', 0]]) }, F.s);
  let bx = x;
  while (bx < x + w) {
    const bw = 40 + r() * 70, bh = 120 + r() * (h * 0.7);
    svg('rect', { x: bx, y: y + h - bh, width: bw, height: bh, fill: night ? (r() > 0.5 ? '#2a2650' : '#332e5e') : (r() > 0.5 ? '#d89a7a' : '#c88a70'), opacity: night ? 1 : 0.8 }, F.s);
    for (let wy = y + h - bh + 12; wy < y + h - 10; wy += 20) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14) if (r() > (night ? 0.55 : 0.8)) svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: night ? '#ffd98a' : '#f6e2c8', opacity: night ? 0.9 : 0.6 }, F.s);
    bx += bw + 4;
  }
}
function studio(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, night = o.mode === 'night';
  // wall, window with skyline + BTS track, curtains, AC, shelf, posters, photo of ยาย, calendar, clock
  svg('rect', { x: -300, y: -300, width: 1680, height: 1610, fill: night ? '#d9a85a' : '#f0cf78' }, F.s);
  svg('rect', { x: -300, y: 1180, width: 1680, height: 130, fill: night ? '#b5583e' : '#d06a48' }, F.s);   // terracotta dado
  svg('rect', { x: -300, y: 1176, width: 1680, height: 8, fill: '#8a3a2a' }, F.s);
  const WX = 620, WY = 340, WW = 420, WH = 640;
  svg('rect', { x: WX - 14, y: WY - 14, width: WW + 28, height: WH + 28, rx: 6, fill: '#e8e2d6', stroke: INK, 'stroke-width': 6 }, F.s);
  bkkSkyline(F, WX, WY, WW, WH, night, 721);
  svg('rect', { x: WX, y: WY + WH * 0.62, width: WW, height: 22, fill: night ? '#3a3454' : '#b88a70' }, F.s);   // elevated track
  for (let px = WX + 30; px < WX + WW; px += 110) svg('rect', { x: px, y: WY + WH * 0.62 + 22, width: 18, height: WH * 0.38, fill: night ? '#2e2a48' : '#a87a62' }, F.s);
  const train = svg('g', {}, F.s);
  svg('rect', { x: 0, y: WY + WH * 0.62 - 44, width: 340, height: 46, rx: 12, fill: night ? '#4a5a8a' : '#e8e2d6', stroke: INK, 'stroke-width': 3 }, train);
  for (let k = 0; k < 7; k++) svg('rect', { x: 16 + k * 46, y: WY + WH * 0.62 - 36, width: 30, height: 18, rx: 3, fill: night ? '#ffe9a8' : '#7a8aa8' }, train);
  const clipW = uidS('cw'); const cp = svg('clipPath', { id: clipW }, F.defs); svg('rect', { x: WX, y: WY, width: WW, height: WH }, cp);
  train.setAttribute('clip-path', `url(#${clipW})`);
  svg('rect', { x: WX + WW / 2 - 5, y: WY, width: 10, height: WH, fill: '#e8e2d6' }, F.s);
  if (!night) { const haze = svg('rect', { x: WX, y: WY, width: WW, height: WH, fill: '#fff1c4', opacity: 0.18 }, F.s); }
  for (const [cx, sgn] of [[WX - 40, 1], [WX + WW + 40, -1]]) svg('path', { d: `M${cx - 50},${WY - 40} L${cx + 50},${WY - 40} L${cx + 40 + sgn * 20},${WY + WH + 40} L${cx - 40 + sgn * 20},${WY + WH + 40} Z`, fill: '#c8583e', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('rect', { x: WX - 110, y: WY - 56, width: WW + 220, height: 14, rx: 7, fill: '#8a5a32' }, F.s);
  const fairy = lightString(F.s, WX - 90, WX + WW + 90, WY - 40, 26, ['#ffd66b', '#ff9fc0', '#fff1c4'], 12);
  const ac = svg('g', {}, F.s);
  svg('rect', { x: 240, y: 180, width: 300, height: 92, rx: 16, fill: '#f6f6f2', stroke: INK, 'stroke-width': 5 }, ac);
  svg('rect', { x: 256, y: 246, width: 268, height: 12, rx: 6, fill: '#c9d2dc' }, ac);
  svg('circle', { cx: 512, cy: 204, r: 5, fill: '#5ad06a' }, ac);
  const acAir = Array.from({ length: 4 }, (_, k) => svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.5 }, ac));
  wallShelf(F.s, 40, 520, 300, '#b07a4a'); bookRow(F.s, 60, 520, 7, 722, 80); pottedPlant(F.s, 290, 520, 0.32, 'snake', '#d06a48');
  poster(F.s, 60, 600, 150, 200, 'mountain', '#fbe6b8');   // the north on her wall
  // framed photo of the two of them
  const ph = svg('g', {}, F.s);
  svg('rect', { x: 250, y: 610, width: 170, height: 140, rx: 6, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, ph);
  svg('rect', { x: 262, y: 622, width: 146, height: 116, fill: '#fde6c8' }, ph);
  faceYai12(ph, 305, 678, 26); faceLan12(ph, 365, 684, 24);
  const cal = svg('g', {}, F.s);
  svg('rect', { x: 460, y: 600, width: 130, height: 170, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4 }, cal);
  svg('rect', { x: 460, y: 600, width: 130, height: 44, fill: '#c8343c' }, cal);
  wtext(cal, 525, 632, o.month || 'พ.ย.', 28, '#fbf2e2');
  for (let k = 0; k < 15; k++) svg('rect', { x: 472 + (k % 5) * 22, y: 656 + Math.floor(k / 5) * 34, width: 16, height: 22, rx: 3, fill: '#d9d2c4' }, cal);
  const clock = wallClock(F.s, 160, 300, 44, '#c8583e'); clock(night ? 22.4 : 13.2);
  // floor and rug
  svg('rect', { x: -300, y: 1300, width: 1680, height: 900, fill: lin(M.defs, [[0, '#8a4a32'], [1, '#4a2018']]) }, M.s);
  for (let y = 1320, k = 0; y < 2100; y += 40 + k * 10, k++) svg('rect', { x: -300, y, width: 1680, height: 3, fill: '#3a160e', opacity: 0.5 }, M.s);
  svg('path', { d: 'M60,1420 L1000,1420 L1060,1560 L0,1560 Z', fill: '#6a2a24', stroke: INK, 'stroke-width': 5 }, M.s);
  for (const v of [0.18, 0.82]) svg('path', { d: `M${60 - 60 * v},${1420 + 140 * v} L${1000 + 60 * v},${1420 + 140 * v}`, stroke: '#e0a060', 'stroke-width': 5 }, M.s);
  wallAO(M.s, M.defs, 1300, { op: 0.3 });
  // the front door on the left (parcels arrive here)
  const door = svg('g', {}, M.s);
  svg('rect', { x: -80, y: 560, width: 240, height: 740, fill: '#f6efe2', stroke: INK, 'stroke-width': 6 }, door);
  svg('rect', { x: -60, y: 600, width: 200, height: 300, rx: 6, fill: 'none', stroke: '#d8cfc0', 'stroke-width': 4 }, door);
  svg('rect', { x: -60, y: 940, width: 200, height: 320, rx: 6, fill: 'none', stroke: '#d8cfc0', 'stroke-width': 4 }, door);
  svg('circle', { cx: 130, cy: 940, r: 12, fill: '#c9a24a', stroke: INK, 'stroke-width': 3 }, door);
  svg('circle', { cx: 40, cy: 720, r: 7, fill: '#2a2226' }, door);
  // dresser with the drawer of scarves, lamp, mirror, perfume
  const dr = svg('g', {}, M.s), DX = 260, DY = 1010;
  svg('rect', { x: DX, y: DY, width: 300, height: 290, rx: 8, fill: '#b07a4a', stroke: INK, 'stroke-width': 5 }, dr);
  const drawerFront = svg('g', {}, M.s);
  for (const [k, dy] of [[0, 30], [1, 120], [2, 210]]) {
    const f = k === 0 ? drawerFront : dr;
    svg('rect', { x: DX + 16, y: DY + dy - 10, width: 268, height: 76, rx: 6, fill: '#c88a5a', stroke: INK, 'stroke-width': 4 }, f);
    svg('rect', { x: DX + 120, y: DY + dy + 22, width: 60, height: 12, rx: 6, fill: '#7a4a2a' }, f);
  }
  const drawerIn = svg('g', {}, M.s);   // the open drawer seen from above, nine scarves inside
  M.s.insertBefore(drawerIn, drawerFront);
  svg('path', { d: `M${DX + 6},${DY + 20} L${DX + 294},${DY + 20} L${DX + 280},${DY - 50} L${DX + 20},${DY - 50} Z`, fill: '#5a321e', stroke: INK, 'stroke-width': 4 }, drawerIn);
  SCARF.forEach((c, i) => svg('rect', { x: DX + 26 + i * 28.5, y: DY - 44, width: 26, height: 60, rx: 6, fill: knitFill(M.defs, c), stroke: INK, 'stroke-width': 2.5 }, drawerIn));
  svg('rect', { x: DX + 190, y: DY - 140, width: 90, height: 130, rx: 40, fill: '#bfe0f0', stroke: '#8a5a32', 'stroke-width': 8, opacity: 0.9 }, dr);   // mirror
  svg('rect', { x: DX + 30, y: DY - 36, width: 22, height: 36, rx: 6, fill: '#f6a6bc', stroke: INK, 'stroke-width': 3 }, dr);
  tinyCactus(dr, DX + 90, DY, '#e8935a');
  const lampX = DX + 150, lampY = DY - 110;
  svg('path', { d: `M${lampX},${DY} L${lampX},${lampY + 30}`, stroke: '#3a3a42', 'stroke-width': 7 }, dr);
  svg('path', { d: `M${lampX - 50},${lampY + 34} L${lampX + 50},${lampY + 34} L${lampX + 34},${lampY - 20} L${lampX - 34},${lampY - 20} Z`, fill: '#f2c14e', stroke: INK, 'stroke-width': 4 }, dr);
  if (night) { lampCone(M.s, M.defs, lampX, lampY + 34, 300, 260, '#ffd59a', 0.4, false); lampCone(M.s, M.defs, lampX, lampY - 20, 260, 300, '#ffd59a', 0.3, true); lightPool(M.s, M.defs, lampX, 1320, 360, 60, '#ffd59a', 0.4); }
  // bed corner, standing fan, monstera
  const bed = svg('g', {}, M.s);
  svg('rect', { x: 760, y: 1160, width: 420, height: 150, rx: 18, fill: '#f6efe2', stroke: INK, 'stroke-width': 5 }, bed);
  svg('rect', { x: 760, y: 1190, width: 420, height: 120, rx: 14, fill: '#f08a6a', stroke: INK, 'stroke-width': 4 }, bed);
  svg('rect', { x: 800, y: 1130, width: 140, height: 60, rx: 26, fill: '#fde6c8', stroke: INK, 'stroke-width': 4 }, bed);
  teddy(bed, 990, 1192, 0.7, '#d9a06a');
  const fan = svg('g', {}, M.s);
  svg('path', { d: 'M640,1300 L640,1090', stroke: '#9aa3b2', 'stroke-width': 10 }, fan);
  svg('ellipse', { cx: 640, cy: 1300, rx: 46, ry: 10, fill: '#9aa3b2', stroke: INK, 'stroke-width': 3 }, fan);
  const blades = svg('g', {}, fan);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 0, cy: -34, rx: 16, ry: 32, fill: '#7fc6d8', opacity: 0.85, transform: `rotate(${k * 120})` }, blades);
  svg('circle', { cx: 640, cy: 1060, r: 56, fill: 'none', stroke: INK, 'stroke-width': 5 }, fan);
  svg('circle', { cx: 640, cy: 1060, r: 12, fill: '#e8e2d6', stroke: INK, 'stroke-width': 3 }, fan);
  pottedPlant(M.s, 1040, 1300, 0.62, 'monstera', '#d06a48');
  let shaft = null;
  if (!night) shaft = lightShaft(M.s, M.defs, [[WX + 40, WY + 40], [WX + WW - 40, WY + 40], [WX + 200, 1500], [WX - 360, 1500]], '#fff1c4', 0.22, 723, 26);
  const heat = night ? null : svg('g', { opacity: 0.25 }, M.s);
  const heatW = heat ? Array.from({ length: 5 }, (_, k) => svg('path', { fill: 'none', stroke: '#fff6dc', 'stroke-width': 4, 'stroke-linecap': 'round' }, heat)) : [];
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, dr);
  const parcels = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 300], night ? ['#ffd59a', '#ff9fc0'] : ['#fff1c4', '#ffe2a8'], 724, { rMin: 40, rMax: 90, op: 0.28 });
  return {
    people, shadowL, top, parcels, drawerFront, drawerIn, ground: 1330, DX, DY,
    light: night ? { ux: -0.75, uy: -0.66, lx: lampX } : { ux: 0.85, uy: -0.5, lx: 950 },
    update(t, o2 = {}) {
      const dk = clamp(o2.drawer ?? 0);   // 0 closed … 1 open
      drawerFront.setAttribute('transform', `translate(0,${(dk * 34).toFixed(1)})`);
      drawerIn.setAttribute('opacity', dk.toFixed(3)); drawerIn.setAttribute('transform', `translate(0,${((1 - dk) * 40).toFixed(1)})`);
      train.setAttribute('transform', `translate(${(((t * 160) % 1500) + WX - 700).toFixed(1)},0)`);
      fairy.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2.6 + i * 1.7)).toFixed(2)));
      blades.setAttribute('transform', `translate(640,1060) rotate(${((t * 900) % 360).toFixed(1)})`);
      acAir.forEach((a, k) => { const u = ((t * 0.8 + k / 4) % 1); a.setAttribute('d', `M${300 + k * 60},${266 + u * 70} q12,${10 + u * 10} 0,${20 + u * 16}`); a.setAttribute('opacity', (0.5 * Math.sin(Math.PI * u)).toFixed(2)); });
      heatW.forEach((h, k) => { const u = ((t * 0.5 + k / 5) % 1), x = WX - 300 + k * 160; h.setAttribute('d', `M${x},${1290 - u * 200} q14,-18 0,-36 q-14,-18 0,-36`); h.setAttribute('opacity', Math.sin(Math.PI * u).toFixed(2)); });
      if (shaft) shaft(t); if (bok) bok(t);
    },
  };
}
// a cardboard parcel (world), x,y = bottom centre; returns { g, lid }
function parcel(g, x, y, s = 1, o = {}) {
  const p = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('path', { d: 'M-70,0 L70,0 L70,-90 L-70,-90 Z', fill: '#c99a5a', stroke: INK, 'stroke-width': 4 }, p);
  svg('path', { d: 'M-70,-90 L-50,-112 L90,-112 L70,-90 Z', fill: '#d9ae6e', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, p);
  svg('path', { d: 'M70,0 L90,-22 L90,-112 L70,-90 Z', fill: '#a87a42', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, p);
  svg('path', { d: 'M0,0 L0,-90 L20,-112', fill: 'none', stroke: '#e8d2a0', 'stroke-width': 10 }, p);   // tape
  svg('rect', { x: -58, y: -76, width: 48, height: 34, rx: 3, fill: '#fbf7ef', stroke: INK, 'stroke-width': 2.5 }, p);   // label
  for (let k = 0; k < 3; k++) svg('path', { d: `M-52,${-66 + k * 9} l${30 - k * 6},0`, stroke: '#4a7bd8', 'stroke-width': 2 }, p);
  if (o.string) svg('path', { d: 'M-70,-46 L70,-46 M-20,0 L-20,-90', stroke: '#c8343c', 'stroke-width': 4 }, p);
  return p;
}
