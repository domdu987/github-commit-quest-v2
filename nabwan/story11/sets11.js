// "12 ฤดูฝน" sets, each with its own palette: the school gate on a warm rainy afternoon (salmon wall, maroon sign, flame
// tree), the soi of shophouses walking home (barber pole, grocery, spirit house, wires, sodium lamp), the apricot
// townhouse porch (folding iron gate, dragon jar under the downspout, orchids), the mustard living room at night
// (ceiling fan, trophy cabinet, the khaki shirt drying on the window grille, the umbrella drying on the floor), and the
// present-day street at dusk (clinic with a neon cross, a bright minimart, a noodle stall, neon on wet asphalt).
// Every set returns { people, shadowL, top, rain, light, update(t, dens), ground, ... }.

// a text label drawn in the world (Kanit)
function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}
// wet asphalt from y0 down: dark gradient, sheen bands, and light reflections [[x, w, color, op], ...]; returns update(t)
function wetRoad(g, defs, y0, top, bot, refl = []) {
  svg('rect', { x: -400, y: y0, width: 4400, height: 1200, fill: lin(defs, [[0, top], [1, bot]]) }, g);
  for (let i = 0; i < 6; i++) svg('rect', { x: -400, y: y0 + 30 + i * 70, width: 4400, height: 3, fill: '#ffffff', opacity: 0.05 }, g);
  const rs = refl.map(([x, w, c, op]) => svg('rect', { x: x - w / 2, y: y0 + 4, width: w, height: 300, rx: w / 2, fill: lin(defs, [[0, c, op], [1, c, 0]]), style: 'mix-blend-mode:screen' }, g));
  return t => rs.forEach((e, i) => e.setAttribute('transform', `translate(${(Math.sin(t * 2.1 + i) * 3).toFixed(1)},0) scale(1,${(1 + 0.06 * Math.sin(t * 3 + i * 2)).toFixed(3)})`));
}
// background people under umbrellas (simple silhouettes) walking along y; returns update(t)
function umbrellaWalkers(g, defs, n, seed, y, x0, x1, o = {}) {
  const r = rng(seed), cols = o.cols || ['#6a4a5a', '#5a4a6e', '#7a5a4a', '#4a5a6a'];
  const ws = Array.from({ length: n }, (_, i) => {
    const e = svg('g', { opacity: o.op ?? 0.8 }, g), c = cols[i % cols.length], uc = ['#c94f45', '#f2c14e', '#4a7bd8', '#e88aa8', '#5aa05c'][Math.floor(r() * 5)];
    svg('path', { d: 'M-14,0 L-10,-58 Q0,-66 10,-58 L14,0 Z', fill: c }, e);
    svg('circle', { cx: 0, cy: -72, r: 12, fill: shade(c, -10) }, e);
    svg('path', { d: 'M0,-60 L0,-112', stroke: '#2a2028', 'stroke-width': 2.5 }, e);
    svg('path', { d: 'M-46,-104 Q0,-150 46,-104 Q34,-110 23,-104 Q12,-110 0,-104 Q-12,-110 -23,-104 Q-34,-110 -46,-104 Z', fill: uc, opacity: 0.9 }, e);
    const legs = svg('path', { stroke: shade(c, -20), 'stroke-width': 7, 'stroke-linecap': 'round' }, e);
    return { e, legs, x: x0 + r() * (x1 - x0), sp: (r() > 0.5 ? 1 : -1) * (30 + r() * 30), s: (o.s ?? 1) * (0.85 + r() * 0.3), ph: r() * 6 };
  });
  return t => ws.forEach(w => {
    const span = x1 - x0, x = x0 + (((w.x - x0 + t * w.sp) % span) + span) % span, k = Math.sin(t * 7 + w.ph) * 8;
    w.e.setAttribute('transform', `translate(${x.toFixed(1)},${(y - Math.abs(Math.sin(t * 7 + w.ph)) * 2).toFixed(1)}) scale(${(w.sp > 0 ? 1 : -1) * w.s},${w.s})`);
    w.legs.setAttribute('d', `M-5,0 l${(-k * 0.5).toFixed(1)},18 M5,0 l${(k * 0.5).toFixed(1)},18`);
  });
}
// thai flag on a pole (waving); returns update(t)
function thaiFlag(g, x, y, w = 90) {
  const h = w * 0.66, f = svg('g', {}, g);
  const rows = [['#c8343c', 1], ['#f6f1e8', 1], ['#2d3a7a', 2], ['#f6f1e8', 1], ['#c8343c', 1]];
  const ps = []; let yy = 0;
  for (const [c, k] of rows) { ps.push({ el: svg('path', { fill: c }, f), y0: yy, y1: yy + h * k / 6 }); yy += h * k / 6; }
  return t => ps.forEach(p => {
    const wv = u => Math.sin(t * 4 - u * 5) * 6 * u;
    let d = `M${x},${(y + p.y0).toFixed(1)}`;
    for (let u = 0.25; u <= 1.001; u += 0.25) d += ` L${(x + w * u).toFixed(1)},${(y + p.y0 + wv(u)).toFixed(1)}`;
    for (let u = 1; u >= -0.001; u -= 0.25) d += ` L${(x + w * u).toFixed(1)},${(y + p.y1 + wv(u)).toFixed(1)}`;
    p.el.setAttribute('d', d + ' Z');
  });
}

// =====================================================================
// A — the school gate, rainy afternoon
// =====================================================================
function schoolGate(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  // far: mauve rain clouds over a warm glow, the school building, flame tree, flag
  svg('rect', { x: -300, y: -300, width: 1680, height: 1500, fill: lin(F.defs, [[0, '#6f6280'], [0.45, '#a8838e'], [1, '#e2b08a']]) }, F.s);
  const clouds = Array.from({ length: 7 }, (_, i) => svg('ellipse', { cx: -100 + i * 220, cy: 120 + (i % 3) * 70, rx: 220, ry: 70, fill: '#5e5270', opacity: 0.45 }, F.s));
  svg('path', { d: 'M40,560 L1040,560 L1000,500 L80,500 Z', fill: '#a84c38', stroke: '#6a2c22', 'stroke-width': 4 }, F.s);   // roof
  svg('rect', { x: 60, y: 560, width: 960, height: 640, fill: '#ecd29a' }, F.s);
  for (const fy of [700, 860, 1020]) { svg('rect', { x: 60, y: fy, width: 960, height: 20, fill: '#b5583e' }, F.s); svg('rect', { x: 60, y: fy + 20, width: 960, height: 6, fill: '#000', opacity: 0.12 }, F.s); }
  for (let cx = 60; cx <= 1020; cx += 120) svg('rect', { x: cx - 8, y: 560, width: 16, height: 640, fill: '#f6e2b4' }, F.s);
  const r = rng(201);
  for (const fy of [590, 750, 910, 1070]) for (let wx = 84; wx < 1000; wx += 120) svg('rect', { x: wx, y: fy, width: 72, height: 86, rx: 4, fill: r() < 0.3 ? '#ffd98a' : '#6a5a62', opacity: 0.9 }, F.s);
  svg('circle', { cx: 540, cy: 530, r: 26, fill: '#fbf7ef', stroke: '#6a2c22', 'stroke-width': 4 }, F.s);
  svg('path', { d: 'M540,530 L540,514 M540,530 L552,536', stroke: '#33252a', 'stroke-width': 3, 'stroke-linecap': 'round' }, F.s);
  svg('rect', { x: 1076, y: 260, width: 8, height: 940, fill: '#e8e2d6' }, F.s);
  const flag = thaiFlag(F.s, 1084, 270, 96);
  // flame tree (red-orange flowers) on the right, tamarind on the left
  svg('path', { d: 'M930,1200 Q940,900 980,760 M980,840 Q1040,780 1100,760', fill: 'none', stroke: '#4a3028', 'stroke-width': 26, 'stroke-linecap': 'round' }, F.s);
  for (let i = 0; i < 26; i++) svg('ellipse', { cx: 820 + r() * 520, cy: 380 + r() * 330, rx: 70 + r() * 60, ry: 40 + r() * 30, fill: ['#4f8a4a', '#5e9a52', '#47803f'][i % 3] }, F.s);
  for (let i = 0; i < 90; i++) svg('circle', { cx: 800 + r() * 560, cy: 360 + r() * 360, r: 5 + r() * 6, fill: ['#e8542c', '#f2763a', '#d8402a'][i % 3] }, F.s);
  for (let i = 0; i < 16; i++) svg('ellipse', { cx: -220 + r() * 420, cy: 420 + r() * 320, rx: 80 + r() * 50, ry: 50 + r() * 30, fill: ['#3f6e3c', '#4a7a44'][i % 2] }, F.s);
  haze(F.s, F.defs, '#e8c4a0', 0.22, 700, 1300);
  const rainF = rainField(F.s, [-300, -300, 1380, 1300], 160, 202, { len: 40, w: 1.6, op: 0.35, slant: 0.15 });
  // mid: yard behind the gate, waiting shed with kids, the wall and railings, pillars and the maroon sign
  svg('rect', { x: -300, y: 1180, width: 1680, height: 270, fill: lin(M.defs, [[0, '#bba996'], [1, '#9e8c7c']]) }, M.s);
  const shed = svg('g', {}, M.s);
  for (const px of [600, 880]) svg('rect', { x: px, y: 1060, width: 12, height: 380, fill: '#6a5048' }, shed);
  svg('path', { d: 'M560,1040 L930,1040 L940,1070 L550,1070 Z', fill: '#8a6a5a', stroke: INK, 'stroke-width': 3 }, shed);
  for (let x = 560; x < 930; x += 24) svg('path', { d: `M${x},1042 l0,26`, stroke: '#6a5048', 'stroke-width': 3 }, shed);
  for (const [kx, c, bc] of [[650, '#f7f6f0', '#4a7bd8'], [700, '#f7f6f0', '#f2c14e'], [840, '#f7f6f0', '#5aa05c']]) {
    const k = svg('g', { opacity: 0.85 }, shed);
    svg('rect', { x: kx - 13, y: 1340, width: 26, height: 50, rx: 8, fill: c }, k);
    svg('rect', { x: kx - 24, y: 1344, width: 12, height: 32, rx: 4, fill: bc }, k);
    svg('circle', { cx: kx, cy: 1324, r: 16, fill: '#3a2a26' }, k);
    svg('rect', { x: kx - 11, y: 1390, width: 22, height: 40, fill: '#2f3b6a' }, k);
  }
  const wall = svg('g', {}, M.s);
  for (const [x0, x1] of [[-300, 480], [960, 1380]]) {
    for (let x = x0 + 10; x < x1; x += 30) svg('rect', { x, y: 1090, width: 9, height: 220, fill: '#4a3530' }, wall);
    svg('rect', { x: x0, y: 1082, width: x1 - x0, height: 12, fill: '#4a3530' }, wall);
    svg('rect', { x: x0, y: 1300, width: x1 - x0, height: 140, fill: '#d98e74', stroke: INK, 'stroke-width': 4 }, wall);
    svg('rect', { x: x0 - 6, y: 1292, width: x1 - x0 + 12, height: 18, rx: 4, fill: '#f2dcc0', stroke: INK, 'stroke-width': 3.5 }, wall);
    for (let x = x0 + 60; x < x1; x += 120) svg('rect', { x, y: 1340, width: 50, height: 60, rx: 6, fill: '#c97a62', opacity: 0.6 }, wall);
  }
  // sliding gate, half open
  for (let x = 566; x < 680; x += 22) svg('rect', { x, y: 1120, width: 8, height: 318, fill: '#4a3530' }, wall);
  svg('rect', { x: 560, y: 1114, width: 130, height: 10, fill: '#4a3530' }, wall); svg('rect', { x: 560, y: 1270, width: 130, height: 8, fill: '#4a3530' }, wall);
  for (const px of [480, 880]) {
    svg('rect', { x: px, y: 880, width: 80, height: 560, fill: '#e9c9a4', stroke: INK, 'stroke-width': 5 }, wall);
    svg('rect', { x: px + 12, y: 900, width: 56, height: 520, fill: '#dcb48c' }, wall);
    svg('rect', { x: px - 10, y: 864, width: 100, height: 24, rx: 4, fill: '#f2dcc0', stroke: INK, 'stroke-width': 4 }, wall);
    // bougainvillea spilling over the pillar tops
    for (let k = 0; k < 14; k++) svg('circle', { cx: px + 40 + Math.cos(k) * (30 + k * 2), cy: 870 + Math.sin(k * 1.7) * 16 + k * 2, r: 12, fill: ['#e05a9a', '#f07ab4', '#c94a86'][k % 3], stroke: k % 4 ? 'none' : INK, 'stroke-width': 2 }, wall);
  }
  svg('rect', { x: 460, y: 790, width: 520, height: 92, rx: 12, fill: '#7a2a2e', stroke: INK, 'stroke-width': 5 }, wall);
  svg('rect', { x: 472, y: 800, width: 496, height: 72, rx: 8, fill: 'none', stroke: '#f2c14e', 'stroke-width': 3 }, wall);
  svg('circle', { cx: 516, cy: 836, r: 24, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, wall);
  svg('path', { d: 'M506,846 L516,822 L526,846 Z', fill: '#7a2a2e' }, wall);
  wtext(wall, 745, 852, 'โรงเรียนบ้านสวนวิทยา', 40, '#f6e2a8');
  // sidewalk and road
  svg('rect', { x: -300, y: 1440, width: 1680, height: 62, fill: lin(M.defs, [[0, '#a59486'], [1, '#8a7a6e']]) }, M.s);
  for (let x = -280; x < 1380; x += 90) svg('path', { d: `M${x},1442 l-8,58`, stroke: '#7a6a60', 'stroke-width': 2 }, M.s);
  svg('rect', { x: -300, y: 1498, width: 1680, height: 10, fill: '#d8cfc4', stroke: INK, 'stroke-width': 2 }, M.s);
  const road = wetRoad(M.s, M.defs, 1508, '#4a3c40', '#241c22', [[520, 60, '#ffd98a', 0.35], [920, 50, '#ffd98a', 0.3], [720, 140, '#7a2a2e', 0.4], [160, 70, '#e05a9a', 0.2]]);
  wallAO(M.s, M.defs, 1440, { op: 0.22, h: 120 });
  // the meatball cart on the right with its striped parasol and grill smoke
  const cart = svg('g', {}, M.s);
  svg('path', { d: 'M1000,1150 L1220,1150', stroke: '#6a5048', 'stroke-width': 6 }, cart);
  svg('path', { d: 'M960,1030 Q1110,940 1260,1030 Z', fill: '#e0453b', stroke: INK, 'stroke-width': 4 }, cart);
  for (const [a, b] of [[1010, 1060], [1110, 1160]]) svg('path', { d: `M${a},1010 Q${(a + b) / 2},975 ${b},998 L${b - 4},1030 L${a + 4},1030 Z`, fill: '#fbf2e2' }, cart);
  svg('path', { d: 'M1110,1030 L1110,1300', stroke: '#6a5048', 'stroke-width': 6 }, cart);
  svg('rect', { x: 990, y: 1290, width: 240, height: 120, rx: 10, fill: '#c9d2dc', stroke: INK, 'stroke-width': 4 }, cart);
  svg('rect', { x: 1000, y: 1250, width: 220, height: 44, rx: 6, fill: '#e8eef2', stroke: INK, 'stroke-width': 3, opacity: 0.9 }, cart);
  for (let k = 0; k < 8; k++) svg('path', { d: `M${1012 + k * 26},1262 l18,-30`, stroke: '#8a5a32', 'stroke-width': 4 }, cart);
  for (let k = 0; k < 8; k++) svg('circle', { cx: 1018 + k * 26, cy: 1256, r: 7, fill: '#a8603a', stroke: INK, 'stroke-width': 1.5 }, cart);
  for (const wx of [1020, 1200]) { svg('circle', { cx: wx, cy: 1440, r: 30, fill: '#2a2226', stroke: INK, 'stroke-width': 4 }, cart); svg('circle', { cx: wx, cy: 1440, r: 10, fill: '#9aa3b2' }, cart); }
  const cartLamp = lightPool(cart, M.defs, 1110, 1150, 160, 120, '#ffd27a', 0.5);
  svg('circle', { cx: 1110, cy: 1150, r: 9, fill: '#fff1c4' }, cart);
  const smoke = floaters(M.s, [1000, 1060, 220, 200], 9, 203, { color: '#efe6dc', rMin: 10, rMax: 22, speed: 40, op: 0.25, base: 0.08, amp: 14 });
  // parked motorbike on the left
  const mb = svg('g', {}, M.s);
  for (const wx of [-30, 170]) { svg('circle', { cx: wx, cy: 1440, r: 40, fill: '#2a2226', stroke: INK, 'stroke-width': 5 }, mb); svg('circle', { cx: wx, cy: 1440, r: 14, fill: '#9aa3b2' }, mb); }
  svg('path', { d: 'M-40,1380 Q40,1330 120,1360 L190,1350 L210,1400 L20,1420 Z', fill: '#c94f45', stroke: INK, 'stroke-width': 4 }, mb);
  svg('path', { d: 'M20,1350 Q70,1320 130,1344', fill: 'none', stroke: '#2a2226', 'stroke-width': 18, 'stroke-linecap': 'round' }, mb);
  svg('path', { d: 'M180,1350 L200,1270 M186,1276 l36,-8', stroke: '#9aa3b2', 'stroke-width': 6, 'stroke-linecap': 'round' }, mb);
  const puds = [puddle(M.s, M.defs, 330, 1600, 160, 24, '#9a7a88', 204), puddle(M.s, M.defs, 860, 1700, 200, 30, '#a88a94', 205), puddle(M.s, M.defs, 560, 1840, 130, 20, '#8a6a7a', 206)];
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, people);
  const reflG = svg('g', { mask: reflFade(M.defs, 1500, 320) }, M.s); M.s.insertBefore(reflG, shadowL);
  const top = svg('g', {}, M.s);
  const rain = svg('g', {}, M.s);
  const rainM = rainField(rain, [-300, -300, 1380, 1920], 260, 207, { len: 70, w: 2.4, op: 0.5, slant: 0.15 });
  const splash = splashField(M.s, -100, 1180, 1446, 1900, 30, 208);
  const drips = dripLine(M.s, [[480, 882, 1440], [560, 882, 1440], [880, 882, 1440], [960, 882, 1440], [470, 1100, 1440], [990, 1036, 1290], [1230, 1036, 1290], [560, 1072, 1440], [930, 1072, 1440]], 209);
  vignette(M.s, M.defs, 0.45);
  let bok = null, rainR = null;
  if (R) { bok = bokehField(R.s, R.defs, 6, [-150, -100, 1230, 500], ['#fff1dc', '#ffd9b0'], 210, { rMin: 30, rMax: 70, op: 0.25 }); rainR = rainField(R.s, [-300, -300, 1380, 2200], 40, 211, { len: 150, w: 5, op: 0.3, slant: 0.15, speed: 2600 }); }
  return {
    people, shadowL, top, rain, reflG, ground: 1500, slant: 0.15, light: { ux: -0.5, uy: -0.86, lx: 200 },
    update(t, dens = 1) {
      clouds.forEach((c, i) => c.setAttribute('transform', `translate(${((t * 6 + i * 40) % 300).toFixed(1)},0)`));
      flag(t); rainF(t, dens); rainM(t, dens); splash(t, dens); drips(t, dens); smoke(t); road(t);
      puds.forEach(p => p(t, dens));
      if (bok) bok(t); if (rainR) rainR(t, dens);
    },
  };
}

// =====================================================================
// B — the soi home: a long row of shophouses, wires, lamp; the camera can track along x (vignette in screen space)
// =====================================================================
function shophouse(g, defs, x, w, c, kind, seed) {
  const r = rng(seed);
  svg('rect', { x, y: 330, width: w, height: 1080, fill: c, stroke: INK, 'stroke-width': 5 }, g);
  svg('rect', { x: x - 8, y: 320, width: w + 16, height: 26, fill: shade(c, -18), stroke: INK, 'stroke-width': 4 }, g);
  // upper floors: windows with grilles, AC, plants, laundry
  for (const fy of [400, 690]) {
    svg('rect', { x: x + 30, y: fy, width: w - 60, height: 190, rx: 6, fill: '#4a3a40', stroke: INK, 'stroke-width': 4 }, g);
    const lit = r() < 0.5;
    if (lit) svg('rect', { x: x + 38, y: fy + 8, width: w - 76, height: 174, fill: '#ffd98a', opacity: 0.75 }, g);
    for (let gx = x + 50; gx < x + w - 40; gx += 26) svg('path', { d: `M${gx},${fy + 4} l0,182`, stroke: '#2a2026', 'stroke-width': 3, opacity: 0.8 }, g);
    svg('path', { d: `M${x + 30},${fy + 95} L${x + w - 30},${fy + 95}`, stroke: '#2a2026', 'stroke-width': 3, opacity: 0.8 }, g);
    if (r() < 0.6) { svg('rect', { x: x + w - 120, y: fy + 196, width: 80, height: 50, rx: 4, fill: '#e8e2d6', stroke: INK, 'stroke-width': 3 }, g); for (let k = 0; k < 4; k++) svg('path', { d: `M${x + w - 112},${fy + 206 + k * 10} l64,0`, stroke: '#9a9488', 'stroke-width': 2 }, g); }
    if (r() < 0.6) for (let k = 0; k < 3; k++) { const px = x + 50 + k * 60; svg('path', { d: `M${px - 18},${fy + 194} l36,0 l-5,22 l-26,0 Z`, fill: '#b5583e', stroke: INK, 'stroke-width': 2.5 }, g); svg('circle', { cx: px, cy: fy + 180, r: 18, fill: ['#5aa05c', '#4f8a4a', '#6ab06a'][k] }, g); }
    if (r() < 0.5) { svg('path', { d: `M${x + 36},${fy + 30} L${x + w - 36},${fy + 30}`, stroke: '#2a2026', 'stroke-width': 2 }, g); for (let k = 0; k < 4; k++) svg('rect', { x: x + 50 + k * (w - 100) / 4, y: fy + 30, width: 34, height: 44, fill: ['#e88aa8', '#f2c14e', '#7fc6a8', '#f6f1e8'][k], stroke: INK, 'stroke-width': 2 }, g); }
  }
  // ground floor: shop by kind
  const gy = 1000;
  svg('rect', { x: x + 14, y: gy, width: w - 28, height: 400, fill: '#2a2226', stroke: INK, 'stroke-width': 4 }, g);
  const glow = svg('rect', { x: x + 22, y: gy + 8, width: w - 44, height: 384, fill: lin(defs, [[0, '#ffe2a8'], [1, '#e8b070']]) }, g);
  if (kind === 'grocery') {
    for (const sy of [gy + 80, gy + 170, gy + 260]) { svg('rect', { x: x + 30, y: sy, width: w - 60, height: 10, fill: '#8a5a32' }, g); for (let k = 0; k < 9; k++) svg('rect', { x: x + 36 + k * (w - 72) / 9, y: sy - 40, width: (w - 72) / 9 - 6, height: 40, rx: 3, fill: ['#e0453b', '#f2c14e', '#4a7bd8', '#5aa05c', '#f6f1e8', '#e8935a'][(k + sy) % 6], stroke: INK, 'stroke-width': 1.5 }, g); }
    for (let k = 0; k < 6; k++) svg('rect', { x: x + 40 + k * 40, y: gy + 14, width: 26, height: 40, rx: 4, fill: ['#e88aa8', '#f2c14e', '#7fc6a8'][k % 3], stroke: INK, 'stroke-width': 2 }, g);   // hanging snack packs
    svg('rect', { x: x + w - 120, y: gy + 150, width: 90, height: 240, rx: 8, fill: '#c8343c', stroke: INK, 'stroke-width': 3 }, g);   // drinks fridge
    svg('rect', { x: x + w - 110, y: gy + 165, width: 70, height: 200, rx: 4, fill: '#ffe8d0', opacity: 0.85 }, g);
  } else if (kind === 'barber') {
    svg('rect', { x: x + 40, y: gy + 60, width: w - 80, height: 160, rx: 8, fill: '#bfe0f0', stroke: INK, 'stroke-width': 4, opacity: 0.85 }, g);   // mirror
    svg('path', { d: `M${x + 70},${gy + 300} l60,0 l0,-70 l-60,0 Z`, fill: '#e0453b', stroke: INK, 'stroke-width': 3 }, g);   // chair
    svg('rect', { x: x + 92, y: gy + 300, width: 16, height: 80, fill: '#9aa3b2' }, g);
  } else if (kind === 'shutter') {
    svg('rect', { x: x + 22, y: gy + 8, width: w - 44, height: 384, fill: '#9a9aa2' }, g);
    for (let sy = gy + 18; sy < gy + 390; sy += 16) svg('rect', { x: x + 22, y: sy, width: w - 44, height: 4, fill: '#7a7a82' }, g);
    glow.setAttribute('opacity', 0);
  } else if (kind === 'home') {
    for (let gx = x + 24; gx < x + w - 20; gx += 20) svg('path', { d: `M${gx},${gy + 12} l0,380`, stroke: '#4a3530', 'stroke-width': 5 }, g);   // folding iron gate
    for (let gx = x + 24; gx < x + w - 20; gx += 40) svg('path', { d: `M${gx},${gy + 30} l20,40 l-20,40 l20,40 l-20,40 l20,40 l-20,40 l20,40 l-20,40`, fill: 'none', stroke: '#4a3530', 'stroke-width': 3 }, g);
  }
  return glow;
}
function soiWalk(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const X0 = -400, X1 = 3400;
  svg('rect', { x: X0 - 600, y: -300, width: 5200, height: 1600, fill: lin(F.defs, [[0, '#6e5f7a'], [0.5, '#a68089'], [1, '#d9a585']]) }, F.s);
  const clouds = Array.from({ length: 12 }, (_, i) => svg('ellipse', { cx: X0 + i * 330, cy: 80 + (i % 3) * 60, rx: 240, ry: 60, fill: '#5e5270', opacity: 0.4 }, F.s));
  const r = rng(301);
  for (let x = X0 - 400; x < X1 + 800; x += 140 + r() * 100) { const h = 200 + r() * 320; svg('rect', { x, y: 560 - h, width: 110 + r() * 80, height: h + 700, fill: r() < 0.5 ? '#6a5470' : '#5e4a64' }, F.s); }
  svg('path', { d: 'M1660,120 L1660,330 M1700,120 L1700,330 M1620,120 L1740,120 L1740,60 L1620,60 Z', fill: '#4e3e58', stroke: '#4e3e58', 'stroke-width': 10 }, F.s);   // water tower
  const rainF = rainField(F.s, [X0 - 600, -300, X1 + 1200, 1300], 220, 302, { len: 40, w: 1.6, op: 0.3, slant: 0.18 });
  // mid: the row of shophouses
  const row = [['#e8b4a8', 'barber'], ['#e0b45a', 'grocery'], ['#e89a6a', 'shutter'], ['#c98a8a', 'home'], ['#d4a05a', 'grocery'], ['#e8b4a8', 'shutter'], ['#e0b45a', 'home'], ['#e89a6a', 'barber'], ['#d4a05a', 'grocery'], ['#c98a8a', 'shutter']];
  const glows = [], signs = [['ร้านตัดผม', '#2d3a7a'], ['ร้านชำ', '#c8343c'], ['ก๋วยเตี๋ยว', '#7a2a2e'], ['', ''], ['เจ๊หน่อยของชำ', '#c8343c'], ['ข้าวมันไก่', '#7a2a2e'], ['', ''], ['บาร์เบอร์', '#2d3a7a'], ['โชห่วย', '#c8343c'], ['อู่ซ่อม', '#5a3a2a']];
  let x = X0; const W2 = 380;
  row.forEach(([c, k], i) => {
    glows.push(shophouse(M.s, M.defs, x, W2, c, k, 310 + i));
    const [tx, tc] = signs[i];
    if (tx) { svg('rect', { x: x + 40, y: 905, width: W2 - 80, height: 70, rx: 8, fill: tc, stroke: INK, 'stroke-width': 4 }, M.s); wtext(M.s, x + W2 / 2, 954, tx, 38, '#fbf2e2'); }
    // striped awning
    const aw = svg('g', {}, M.s);
    svg('path', { d: `M${x + 6},985 L${x + W2 - 6},985 L${x + W2 + 14},1050 L${x - 14},1050 Z`, fill: '#fbf2e2', stroke: INK, 'stroke-width': 4 }, aw);
    for (let k = 0; k < 8; k++) { const ax = x + 6 + k * (W2 - 12) / 8; svg('path', { d: `M${ax},985 l${(W2 - 12) / 16},0 l${(W2 - 12) / 16 + 2},65 l${-(W2 - 12) / 16 - 4},0 Z`, fill: ['#c8343c', '#e8935a', '#4f9e5e', '#c8343c'][i % 4] }, aw); }
    x += W2;
  });
  // spirit house between shops 3 and 4
  const sp = svg('g', {}, M.s), spx = X0 + 4 * W2 - 6;
  svg('rect', { x: spx - 6, y: 1220, width: 12, height: 190, fill: '#c9a24a', stroke: INK, 'stroke-width': 3 }, sp);
  svg('rect', { x: spx - 40, y: 1160, width: 80, height: 64, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, sp);
  svg('path', { d: `M${spx - 52},1162 L${spx},1110 L${spx + 52},1162 Z`, fill: '#c8343c', stroke: INK, 'stroke-width': 3 }, sp);
  for (let k = 0; k < 5; k++) svg('circle', { cx: spx - 30 + k * 15, cy: 1236, r: 6, fill: ['#f5a524', '#e05a9a'][k % 2] }, sp);
  // sidewalk + road
  svg('rect', { x: X0 - 400, y: 1405, width: 5200, height: 60, fill: lin(M.defs, [[0, '#9a8a80'], [1, '#7e6e66']]) }, M.s);
  svg('rect', { x: X0 - 400, y: 1462, width: 5200, height: 10, fill: '#d8cfc4', stroke: INK, 'stroke-width': 2 }, M.s);
  const refl = []; for (let i = 0; i < row.length; i++) if (row[i][1] !== 'shutter') refl.push([X0 + i * W2 + W2 / 2, W2 * 0.5, '#ffd98a', 0.28]);
  refl.push([1050, 60, '#ffcf7a', 0.5], [2650, 60, '#ffcf7a', 0.5]);
  const road = wetRoad(M.s, M.defs, 1472, '#4a3a40', '#211a20', refl);
  wallAO(M.s, M.defs, 1405, { op: 0.2, h: 100 });
  // a dog asleep under an awning, potted plants and a water jar along the sidewalk
  const dogU = sleepyCat(M.s, X0 + 9 * W2 + 230, 1418, 0.8, '#d9b48a', { f: -1 });
  for (const px of [X0 + 2 * W2 + 40, X0 + 5 * W2 + 300, X0 + 8 * W2 + 60]) pottedPlant(M.s, px, 1420, 0.55, 'snake', '#b5583e');
  // poles, wires, sodium lamps with light cones
  const lamps = [];
  for (const px of [250, 1050, 1850, 2650]) {
    svg('rect', { x: px - 13, y: 160, width: 26, height: 1260, fill: '#8a8278', stroke: INK, 'stroke-width': 4 }, M.s);
    svg('rect', { x: px - 60, y: 220, width: 120, height: 12, fill: '#6a625a', stroke: INK, 'stroke-width': 3 }, M.s);
    svg('rect', { x: px + 16, y: 300, width: 44, height: 60, rx: 6, fill: '#7a7268', stroke: INK, 'stroke-width': 3 }, M.s);
    if (px === 1050 || px === 2650) {
      svg('path', { d: `M${px},560 q60,-30 110,0`, fill: 'none', stroke: '#6a625a', 'stroke-width': 8 }, M.s);
      const lg = svg('g', {}, M.s);
      lampCone(lg, M.defs, px + 110, 570, 520, 860, '#ffcf7a', 0.28, false);
      svg('ellipse', { cx: px + 110, cy: 568, rx: 30, ry: 12, fill: '#fff1c4', stroke: INK, 'stroke-width': 3 }, lg);
      lightPool(lg, M.defs, px + 110, 1460, 280, 50, '#ffcf7a', 0.35);
      lamps.push({ lg, x: px + 110 });
    }
  }
  for (const [y0, sag, w] of [[230, 70, 3], [250, 90, 2.5], [280, 60, 2], [300, 110, 3]]) for (const px of [250, 1050, 1850]) svg('path', { d: `M${px},${y0} Q${px + 400},${y0 + sag * 2} ${px + 800},${y0}`, fill: 'none', stroke: '#2a2026', 'stroke-width': w }, M.s);
  for (const px of [-550, 250, 1050, 1850, 2650]) svg('path', { d: `M${px},240 Q${px + 400},330 ${px + 800},240`, fill: 'none', stroke: '#2a2026', 'stroke-width': 2 }, M.s);
  const puds = [[150, 1600, 170, 24], [900, 1700, 210, 30], [1500, 1580, 150, 22], [2100, 1680, 200, 28], [2700, 1600, 170, 24], [600, 1850, 140, 22]].map(([cx, cy, rx, ry], i) => puddle(M.s, M.defs, cx, cy, rx, ry, '#a88290', 320 + i));
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, people);
  const reflG = svg('g', { mask: reflFade(M.defs, 1520, 320) }, M.s); M.s.insertBefore(reflG, shadowL);
  const top = svg('g', {}, M.s);
  const rain = svg('g', {}, M.s);
  const rainM = rainField(rain, [X0 - 400, -300, X1 + 400, 1920], 520, 303, { len: 70, w: 2.4, op: 0.5, slant: 0.18 });
  // drops glittering inside the lamp cones
  const sparkle = lamps.map((l, i) => rainField(rain, [l.x - 260, 600, l.x + 260, 1420], 60, 330 + i, { len: 46, w: 2.6, op: 0.75, slant: 0.18, color: '#fff1c4' }));
  const splash = splashField(M.s, X0, X1, 1410, 1900, 70, 304);
  const dripPts = []; for (let i = 0; i < row.length; i++) for (let k = 0; k < 5; k++) dripPts.push([X0 + i * W2 - 10 + k * (W2 + 20) / 4, 1052, 1405]);
  const drips = dripLine(M.s, dripPts, 305);
  let bok = null, rainR = null;
  if (R) { bok = bokehField(R.s, R.defs, 10, [X0, -100, X1, 600], ['#fff1dc', '#ffd9b0', '#ffcf7a'], 306, { rMin: 30, rMax: 80, op: 0.25 }); rainR = rainField(R.s, [X0 - 400, -300, X1 + 400, 2200], 80, 307, { len: 150, w: 5, op: 0.28, slant: 0.18, speed: 2600 }); }
  // the vignette rides with the camera (screen space), so the camera can track along the street
  const vg = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;pointer-events:none' }); S.fx.appendChild(vg);
  vignette(vg, svg('defs', {}, vg), 0.45);
  return {
    people, shadowL, top, rain, reflG, ground: 1520, slant: 0.18, light: { ux: -0.45, uy: -0.89, lx: 1160 }, glows,
    update(t, dens = 1) {
      clouds.forEach((c, i) => c.setAttribute('transform', `translate(${((t * 6 + i * 50) % 300).toFixed(1)},0)`));
      rainF(t, dens); rainM(t, dens); sparkle.forEach(s => s(t, dens)); splash(t, dens); drips(t, dens); road(t); dogU(t);
      puds.forEach(p => p(t, dens));
      lamps.forEach((l, i) => l.lg.setAttribute('opacity', (0.92 + 0.08 * Math.sin(t * 13 + i) * Math.sin(t * 3.1)).toFixed(3)));
      if (bok) bok(t); if (rainR) rainR(t, dens);
    },
  };
}

// =====================================================================
// C — the apricot townhouse porch, evening rain
// =====================================================================
function dragonJar(g, defs, x, y, s = 1) {
  const j = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('ellipse', { cx: 0, cy: 4, rx: 96, ry: 14, fill: '#000', opacity: 0.25 }, j);
  svg('path', { d: 'M-60,-230 Q-110,-170 -100,-90 Q-90,-10 -50,0 L50,0 Q90,-10 100,-90 Q110,-170 60,-230 Z', fill: lin(defs, [[0, '#8a4a2a'], [0.5, '#a8603a'], [1, '#6a3a22']], 1, 0), stroke: INK, 'stroke-width': 5 }, j);
  svg('ellipse', { cx: 0, cy: -232, rx: 62, ry: 14, fill: '#3a2a26', stroke: INK, 'stroke-width': 4 }, j);
  svg('ellipse', { cx: 0, cy: -228, rx: 50, ry: 9, fill: '#7a8a9a', opacity: 0.7 }, j);   // water
  // the dragon coiling round the belly
  svg('path', { d: 'M-90,-120 C-60,-160 -20,-90 10,-130 C40,-170 70,-110 92,-140', fill: 'none', stroke: '#f2c14e', 'stroke-width': 12, 'stroke-linecap': 'round' }, j);
  svg('path', { d: 'M-90,-120 C-60,-160 -20,-90 10,-130 C40,-170 70,-110 92,-140', fill: 'none', stroke: INK, 'stroke-width': 3, 'stroke-dasharray': '6 10' }, j);
  svg('circle', { cx: 92, cy: -142, r: 12, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, j);
  svg('path', { d: 'M-70,-190 Q-80,-120 -70,-60', fill: 'none', stroke: '#ffffff', 'stroke-width': 6, opacity: 0.25, 'stroke-linecap': 'round' }, j);
  return j;
}
function porch(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  // far: the house front — apricot walls, deep-red trim, upper window with grille, the lit doorway
  svg('rect', { x: -300, y: -300, width: 1680, height: 1800, fill: '#e8a87c' }, F.s);
  svg('rect', { x: -300, y: -300, width: 1680, height: 1800, fill: lin(F.defs, [[0, '#000', 0.25], [0.5, '#000', 0], [1, '#000', 0.1]]) }, F.s);
  svg('rect', { x: 560, y: 600, width: 300, height: 700, rx: 6, fill: '#7a3a2a', stroke: INK, 'stroke-width': 6 }, F.s);   // doorway frame
  const door = svg('rect', { x: 580, y: 620, width: 260, height: 680, fill: lin(F.defs, [[0, '#ffe2a8'], [1, '#f2b068']]) }, F.s);
  svg('rect', { x: 600, y: 640, width: 100, height: 660, fill: '#8a4a32', stroke: INK, 'stroke-width': 4 }, F.s);   // door leaf, open inwards
  for (const gy of [680, 860, 1040]) svg('rect', { x: 614, y: gy, width: 72, height: 140, fill: '#ffe2a8', opacity: 0.6, stroke: INK, 'stroke-width': 3 }, F.s);
  svg('rect', { x: 120, y: 700, width: 300, height: 260, rx: 6, fill: '#7a3a2a', stroke: INK, 'stroke-width': 5 }, F.s);   // window
  svg('rect', { x: 136, y: 716, width: 268, height: 228, fill: '#ffd98a', opacity: 0.85 }, F.s);
  for (let gx = 150; gx < 400; gx += 30) svg('path', { d: `M${gx},716 l0,228`, stroke: '#4a2a22', 'stroke-width': 4 }, F.s);
  svg('path', { d: 'M136,830 L404,830', stroke: '#4a2a22', 'stroke-width': 4 }, F.s);
  svg('path', { d: 'M150,730 Q220,800 170,940 L140,940 Z M390,730 Q330,800 380,940 L404,940 Z', fill: '#c8343c', opacity: 0.85 }, F.s);   // curtains
  // a wall clock and the house number plate, a calendar
  wallClock(F.s, 960, 760, 38, '#7a3a2a')(17.25);
  svg('rect', { x: 920, y: 900, width: 100, height: 60, rx: 6, fill: '#2d3a7a', stroke: INK, 'stroke-width': 3 }, F.s);
  wtext(F.s, 970, 942, '45/2', 30, '#fbf2e2');
  // mid: porch ceiling and eave, floor tiles, iron gate, jar, rack, motorbike, orchids, bulb
  svg('rect', { x: -300, y: -300, width: 1680, height: 820, fill: '#b9764e' }, M.s);   // upper floor slab seen from below
  svg('rect', { x: -300, y: 500, width: 1680, height: 40, fill: '#7a3a2a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: -300, y: 1300, width: 1680, height: 900, fill: lin(M.defs, [[0, '#8a3a2e'], [1, '#4a1e1a']]) }, M.s);
  for (let x = -300; x < 1400; x += 120) svg('path', { d: `M${x},1300 L${x - 60 + (x - 540) * 0.3},1920`, stroke: '#3a1612', 'stroke-width': 3, opacity: 0.5 }, M.s);
  for (const y of [1360, 1440, 1540, 1660, 1800]) svg('rect', { x: -300, y, width: 1680, height: 3, fill: '#3a1612', opacity: 0.5 }, M.s);
  wallAO(M.s, M.defs, 1300, { op: 0.3 });
  const jar = dragonJar(M.s, M.defs, 110, 1340, 0.9);
  svg('rect', { x: 196, y: 520, width: 26, height: 700, fill: '#9a9aa2', stroke: INK, 'stroke-width': 4 }, M.s);   // downspout
  svg('path', { d: 'M209,1220 Q209,1250 150,1262', fill: 'none', stroke: '#9a9aa2', 'stroke-width': 26 }, M.s);
  svg('path', { d: 'M209,1220 Q209,1250 150,1262', fill: 'none', stroke: INK, 'stroke-width': 4, 'stroke-dasharray': '1 0' , opacity: 0 }, M.s);
  const pour = svg('path', { fill: 'none', stroke: '#e8eef2', 'stroke-width': 10, 'stroke-linecap': 'round', opacity: 0.7 }, M.s);
  const jarSplash = splashField(M.s, 70, 150, 1124, 1132, 6, 401, { op: 0.7 });
  // shoe rack by the door with a pair of small school shoes
  const rack = svg('g', {}, M.s);
  svg('rect', { x: 880, y: 1180, width: 180, height: 120, rx: 6, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, rack);
  for (const sy of [1220, 1260]) svg('rect', { x: 886, y: sy, width: 168, height: 6, fill: '#5a3a22' }, rack);
  for (const [sx, c] of [[910, '#e0574b'], [960, '#f6f1e8'], [1010, '#4a7bd8']]) svg('path', { d: `M${sx - 18},1216 q18,-18 36,0 Z`, fill: c, stroke: INK, 'stroke-width': 2.5 }, rack);
  // orchid pots hanging from the eave
  const orch = [];
  for (const ox of [330, 470, 1000]) {
    const og = svg('g', {}, M.s);
    svg('path', { d: `M${ox},540 L${ox},640`, stroke: '#5a3a22', 'stroke-width': 3 }, og);
    svg('path', { d: `M${ox - 30},640 L${ox + 30},640 L${ox + 22},690 L${ox - 22},690 Z`, fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, og);
    for (let k = 0; k < 4; k++) svg('path', { d: `M${ox - 20 + k * 12},690 q${-6 + k * 4},60 ${-10 + k * 6},110`, fill: 'none', stroke: '#6ab06a', 'stroke-width': 4 }, og);
    for (let k = 0; k < 6; k++) svg('circle', { cx: ox + 30 + Math.cos(k) * 14, cy: 650 + k * 14, r: 9, fill: ['#b07ad8', '#e05a9a', '#f6f1e8'][k % 3], stroke: INK, 'stroke-width': 1.5 }, og);
    orch.push({ og, ox });
  }
  // folding iron gate pushed to the right edge
  const gate = svg('g', {}, M.s);
  for (let gx = 1130; gx < 1400; gx += 16) svg('path', { d: `M${gx},540 l0,760`, stroke: '#3a2a2a', 'stroke-width': 6 }, gate);
  for (let gy = 560; gy < 1300; gy += 70) svg('path', { d: `M1126,${gy} l270,0`, stroke: '#3a2a2a', 'stroke-width': 3 }, gate);
  // the porch bulb
  const bx = 480, by = 600;
  svg('path', { d: `M${bx},540 L${bx},${by - 24}`, stroke: '#3a2a24', 'stroke-width': 3 }, M.s);
  const bulb = svg('g', {}, M.s);
  svg('circle', { cx: bx, cy: by, r: 420, fill: rad2(M.defs, [[0, '#ffd59a', 0.4], [0.5, '#ffd59a', 0.12], [1, '#ffd59a', 0]]), style: 'mix-blend-mode:screen' }, bulb);
  svg('circle', { cx: bx, cy: by, r: 18, fill: '#fff1c4', stroke: '#e0b04a', 'stroke-width': 3 }, bulb);
  lightPool(M.s, M.defs, bx + 60, 1360, 480, 70, '#ffd59a', 0.35);
  const moths = floaters(M.s, [bx - 80, by - 60, 160, 120], 6, 402, { color: '#fff6dc', rMin: 2, rMax: 4, speed: 36, op: 0.7, base: 0.2 });
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, people);
  const top = svg('g', {}, M.s);
  // drips (a curtain) from the eave edge, and the front rain in the foreground
  const rain = svg('g', {}, M.s);
  const ePts = []; for (let x = -280; x < 1380; x += 34) ePts.push([x, 540, 1300]);
  const drips = dripLine(rain, ePts, 403);
  const curtain = rainField(rain, [-300, 540, 1380, 1300], 70, 404, { len: 80, w: 2, op: 0.2, slant: 0.03 });
  const splash = splashField(M.s, -100, 1180, 1300, 1900, 24, 405);
  vignette(M.s, M.defs, 0.5);
  let rainR = null, bok = null;
  if (R) { rainR = rainField(R.s, [-300, -300, 1380, 2200], 40, 406, { len: 150, w: 5, op: 0.25, slant: 0.1, speed: 2600 }); bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 300], ['#ffd59a', '#fff1c4'], 407, { rMin: 40, rMax: 90, op: 0.3 }); }
  return {
    people, shadowL, top, rain, ground: 1330, slant: 0.03, light: { ux: -0.2, uy: -0.98, lx: bx }, door,
    update(t, dens = 1) {
      bulb.setAttribute('opacity', (0.95 + 0.05 * Math.sin(t * 9) * Math.sin(t * 2.3)).toFixed(3));
      moths(t); drips(t, dens); curtain(t, dens); splash(t, dens); jarSplash(t, dens);
      const w = 8 + 3 * Math.sin(t * 17);
      pour.setAttribute('d', `M150,1262 Q${(130 + w).toFixed(1)},1280 ${(118 + w * 0.5).toFixed(1)},1128`);
      orch.forEach((q, i) => q.og.setAttribute('transform', `rotate(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)} ${q.ox} 540)`));
      if (rainR) rainR(t, dens); if (bok) bok(t);
    },
  };
}

// =====================================================================
// D — the mustard living room at night (memory)
// =====================================================================
function shirtOnHanger(g, x, y, s = 1, c = DAD.shirt, wetC = '#86703e') {
  const h = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('path', { d: 'M0,-40 q0,-14 10,-14 q10,0 10,10 M0,-40 L-70,-10 L70,-10 Z', fill: 'none', stroke: '#8a5a32', 'stroke-width': 5, 'stroke-linejoin': 'round' }, h);
  svg('path', { d: 'M-70,-10 L-110,40 L-84,62 L-62,40 L-62,160 L62,160 L62,40 L84,62 L110,40 L70,-10 L24,-14 Q0,6 -24,-14 Z', fill: c, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, h);
  // one shoulder soaked darker and glossy, still dripping
  svg('path', { d: 'M24,-14 L70,-10 L110,40 L84,62 L62,40 L62,92 Q52,100 46,96 L44,112 Q38,118 34,110 L32,96 Q22,92 20,86 Q6,40 24,-14 Z', fill: wetC, opacity: 0.95 }, h);
  svg('path', { d: 'M30,0 Q40,30 36,70 M58,10 q20,14 34,32', fill: 'none', stroke: '#ffffff', 'stroke-width': 3, opacity: 0.35, 'stroke-linecap': 'round' }, h);
  for (const [dx, l] of [[40, 22], [52, 14], [72, 30]]) svg('path', { d: `M${dx},92 l0,${l}`, stroke: wetC, 'stroke-width': 6, 'stroke-linecap': 'round' }, h);
  svg('path', { d: 'M24,-14 Q0,6 -24,-14 M0,0 L0,150', fill: 'none', stroke: shade(c, -20), 'stroke-width': 3 }, h);
  for (const [px, py] of [[-34, 40], [34, 40]]) svg('rect', { x: px - 14, y: py, width: 28, height: 24, rx: 3, fill: 'none', stroke: shade(c, -20), 'stroke-width': 3 }, h);
  svg('path', { d: 'M40,20 q8,-6 16,-2', fill: 'none', stroke: '#fff', 'stroke-width': 3, opacity: 0.5, 'stroke-linecap': 'round' }, h);
  return h;
}
function livingRoom(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  // far: mustard wall over dark wood wainscot, window with rain on the night garden, cabinet, clock, photo, calendar
  svg('rect', { x: -300, y: -300, width: 1680, height: 1600, fill: '#c8913c' }, F.s);
  for (let x = -300; x < 1400; x += 60) svg('rect', { x, y: -300, width: 2, height: 1350, fill: '#a87428', opacity: 0.4 }, F.s);
  svg('rect', { x: -300, y: 1040, width: 1680, height: 300, fill: '#6a4028' }, F.s);
  for (let x = -300; x < 1400; x += 90) svg('rect', { x, y: 1040, width: 4, height: 300, fill: '#4a2a1a', opacity: 0.6 }, F.s);
  svg('rect', { x: -300, y: 1032, width: 1680, height: 14, fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, F.s);
  // window: night garden in the rain (banana leaves), grille, the khaki shirt hanging on it
  svg('rect', { x: 590, y: 300, width: 420, height: 560, rx: 8, fill: '#6a4028', stroke: INK, 'stroke-width': 6 }, F.s);
  svg('rect', { x: 610, y: 320, width: 380, height: 520, fill: lin(F.defs, [[0, '#2a2440'], [1, '#3e3450']]) }, F.s);
  const r = rng(501);
  for (let i = 0; i < 6; i++) { const lx = 620 + r() * 360, ly = 520 + r() * 300; svg('path', { d: `M${lx},${ly + 200} Q${lx + 10},${ly + 80} ${lx + (r() - 0.5) * 120},${ly}`, fill: 'none', stroke: '#2e4a32', 'stroke-width': 30, 'stroke-linecap': 'round' }, F.s); }
  const winRain = rainField(F.s, [610, 320, 990, 840], 60, 502, { len: 50, w: 2, op: 0.45, slant: 0.1 });
  const flash = svg('rect', { x: 610, y: 320, width: 380, height: 520, fill: '#e8e0ff', opacity: 0 }, F.s);
  for (let gx = 630; gx < 990; gx += 36) svg('path', { d: `M${gx},320 l0,520`, stroke: '#3a2a26', 'stroke-width': 6 }, F.s);
  for (const gy of [480, 660]) svg('path', { d: `M610,${gy} l380,0`, stroke: '#3a2a26', 'stroke-width': 6 }, F.s);
  svg('rect', { x: 576, y: 852, width: 448, height: 22, rx: 6, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, F.s);
  const shirtG = svg('g', {}, F.s);
  shirtOnHanger(shirtG, 860, 430, 0.95);
  const shirtDrip = dripLine(F.s, [[874, 590, 1040], [890, 586, 1040]], 503, { color: '#e8eef2' });
  svg('ellipse', { cx: 884, cy: 1046, rx: 40, ry: 10, fill: '#cfd8de', opacity: 0.5 }, F.s);
  // trophy cabinet and the kid's certificate
  const cab = svg('g', {}, F.s);
  svg('rect', { x: 60, y: 420, width: 380, height: 620, rx: 8, fill: '#7a4a2a', stroke: INK, 'stroke-width': 6 }, cab);
  svg('rect', { x: 80, y: 440, width: 340, height: 580, fill: '#f6e8cc', opacity: 0.35 }, cab);
  for (const sy of [620, 820]) svg('rect', { x: 80, y: sy, width: 340, height: 10, fill: '#5a3420' }, cab);
  for (const [tx, ty, s] of [[130, 620, 1], [200, 620, 1.3], [300, 620, 0.9], [380, 620, 1.1]]) { svg('path', { d: `M${tx - 20 * s},${ty - 80 * s} l${40 * s},0 l${-6 * s},${40 * s} l${-28 * s},0 Z`, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, cab); svg('rect', { x: tx - 6 * s, y: ty - 40 * s, width: 12 * s, height: 26 * s, fill: '#d9a22c', stroke: INK, 'stroke-width': 2.5 }, cab); svg('rect', { x: tx - 18 * s, y: ty - 16 * s, width: 36 * s, height: 16 * s, fill: '#5a3420', stroke: INK, 'stroke-width': 2.5 }, cab); }
  bookRow(cab, 96, 820, 10, 504, 120);
  svg('rect', { x: 260, y: 700, width: 140, height: 110, rx: 4, fill: '#f6efe2', stroke: '#c9a24a', 'stroke-width': 6 }, cab);   // certificate
  for (let k = 0; k < 4; k++) svg('rect', { x: 280, y: 724 + k * 18, width: 100 - k * 14, height: 5, rx: 2, fill: '#8a7a6a' }, cab);
  svg('circle', { cx: 370, cy: 788, r: 12, fill: '#e0453b' }, cab);
  for (let k = 0; k < 6; k++) svg('rect', { x: 100 + k * 52, y: 900, width: 40, height: 110, rx: 6, fill: ['#e8e2d6', '#c9d2dc'][k % 2], stroke: INK, 'stroke-width': 2.5 }, cab);   // glasses
  // clock, family photo, calendar
  wallClock(F.s, 540, 220, 52, '#7a3a2a')(19.5);
  photoFrame(F.s, 260, 340, 150, 120, '#ffe2a8', '#8a5a32');
  svg('rect', { x: 1060, y: 420, width: 150, height: 210, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('rect', { x: 1060, y: 420, width: 150, height: 56, fill: '#c8343c' }, F.s);
  wtext(F.s, 1135, 462, 'ส.ค.', 34, '#fbf2e2');
  for (let k = 0; k < 15; k++) svg('rect', { x: 1074 + (k % 5) * 26, y: 494 + Math.floor(k / 5) * 40, width: 18, height: 24, rx: 3, fill: k === 8 ? '#e0453b' : '#d9d2c4' }, F.s);
  // ceiling: tube light (key) and fan
  svg('rect', { x: -300, y: -300, width: 1680, height: 380, fill: '#e8d6b0' }, F.s);
  svg('rect', { x: -300, y: 72, width: 1680, height: 14, fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, F.s);
  svg('rect', { x: 300, y: 100, width: 300, height: 26, rx: 13, fill: '#fbfbf6', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('ellipse', { cx: 450, cy: 140, rx: 600, ry: 300, fill: rad2(F.defs, [[0, '#fff6e0', 0.35], [1, '#fff6e0', 0]]), style: 'mix-blend-mode:screen' }, F.s);
  // mid: floor, rug, armchair, low table, the umbrella drying open upside down by the door
  svg('rect', { x: -300, y: 1300, width: 1680, height: 900, fill: lin(M.defs, [[0, '#8a3a30'], [1, '#4a1c18']]) }, M.s);
  svg('rect', { x: -300, y: 1300, width: 1680, height: 6, fill: '#000', opacity: 0.3 }, M.s);
  for (let i = 0; i < 6; i++) svg('rect', { x: -300, y: 1340 + i * 90, width: 1680, height: 3, fill: '#ffffff', opacity: 0.05 }, M.s);
  wallAO(M.s, M.defs, 1300, { op: 0.32 });
  svg('path', { d: 'M100,1420 L1000,1420 L1060,1560 L40,1560 Z', fill: '#5a2430', stroke: INK, 'stroke-width': 5 }, M.s);   // maroon mat
  for (const v of [0.2, 0.8]) svg('path', { d: `M${100 - 60 * v},${1420 + 140 * v} L${1000 + 60 * v},${1420 + 140 * v}`, stroke: '#c9a24a', 'stroke-width': 5 }, M.s);
  const chair = svg('g', {}, M.s);   // wooden armchair (dad), back to the left
  svg('rect', { x: 120, y: 1060, width: 34, height: 340, rx: 10, fill: '#7a4a2a', stroke: INK, 'stroke-width': 5 }, chair);
  svg('rect', { x: 120, y: 1260, width: 280, height: 40, rx: 12, fill: '#8a5a32', stroke: INK, 'stroke-width': 5 }, chair);
  svg('rect', { x: 140, y: 1236, width: 240, height: 34, rx: 14, fill: '#c8343c', stroke: INK, 'stroke-width': 4 }, chair);
  for (const lx of [140, 370]) svg('rect', { x: lx, y: 1296, width: 22, height: 110, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, chair);
  svg('rect', { x: 150, y: 1090, width: 30, height: 150, rx: 10, fill: '#c8343c', stroke: INK, 'stroke-width': 3 }, chair);
  const armFront = svg('g', {}, M.s);   // the arm rest is drawn over his legs
  svg('rect', { x: 120, y: 1196, width: 300, height: 26, rx: 10, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, armFront);
  svg('rect', { x: 392, y: 1210, width: 22, height: 196, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, armFront);
  M.s.removeChild(armFront);
  const table = svg('g', {}, M.s);   // the low table (โต๊ะญี่ปุ่น) where the kid does homework
  svg('rect', { x: 660, y: 1378, width: 300, height: 26, rx: 6, fill: '#a8703a', stroke: INK, 'stroke-width': 4 }, table);
  for (const lx of [676, 924]) svg('rect', { x: lx, y: 1400, width: 20, height: 62, fill: '#8a5a32', stroke: INK, 'stroke-width': 3.5 }, table);
  const tableTop = svg('g', {}, M.s); M.s.removeChild(tableTop);
  svg('path', { d: 'M690,1378 l90,-10 l10,10 l-90,6 Z', fill: '#f6efe2', stroke: INK, 'stroke-width': 3 }, tableTop);   // open notebook
  svg('path', { d: 'M800,1374 l60,-22', stroke: '#f2c14e', 'stroke-width': 7, 'stroke-linecap': 'round' }, tableTop);
  svg('rect', { x: 870, y: 1342, width: 46, height: 36, rx: 6, fill: '#4a7bd8', stroke: INK, 'stroke-width': 3 }, tableTop);   // pencil case
  // desk lamp on the table (warm key for the kid)
  svg('path', { d: 'M930,1378 L940,1290 L880,1250', fill: 'none', stroke: '#3a3a42', 'stroke-width': 7, 'stroke-linecap': 'round' }, table);
  svg('path', { d: 'M850,1238 L906,1226 L900,1272 Z', fill: '#2d6a4a', stroke: INK, 'stroke-width': 3.5 }, table);
  lampCone(M.s, M.defs, 875, 1260, 220, 120, '#ffd59a', 0.35, false);
  lightPool(M.s, M.defs, 790, 1382, 160, 30, '#ffd59a', 0.5);
  // the umbrella drying open, upside down, by the door on the right, with a puddle
  const dry = svg('g', {}, M.s);
  svg('ellipse', { cx: 1000, cy: 1520, rx: 130, ry: 18, fill: '#cfd8de', opacity: 0.45 }, dry);
  const ug = svg('g', { transform: 'translate(1000,1470) rotate(160) scale(0.62)' }, dry);
  const dryU = umbrella(ug, { R: 165, L: 175 });
  const dryDrip = dripLine(dry, [[960, 1420, 1514], [1046, 1440, 1514]], 505, { color: '#e8eef2' });
  // fan
  const fan = svg('g', {}, F.s);
  svg('path', { d: 'M820,86 L820,150', stroke: '#3a3a42', 'stroke-width': 6 }, fan);
  const blades = svg('g', {}, fan);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 0, cy: 0, rx: 150, ry: 14, fill: '#8a5a32', stroke: INK, 'stroke-width': 3, transform: `rotate(${k * 60})` }, blades);
  svg('ellipse', { cx: 820, cy: 154, rx: 26, ry: 12, fill: '#e8e2d6', stroke: INK, 'stroke-width': 3 }, fan);
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, chair);
  M.s.appendChild(armFront); M.s.appendChild(tableTop);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 260], ['#ffd59a', '#fff6e0'], 506, { rMin: 40, rMax: 100, op: 0.3 });
  return {
    people, shadowL, top, armFront, tableTop, shirtG, dryU, ground: 1430, light: { ux: 0.1, uy: -0.99, lx: 450 },
    update(t) {
      winRain(t); shirtDrip(t); dryDrip(t);
      flash.setAttribute('opacity', (0.7 * Math.max(0, 1 - Math.abs(t - 2.2) / 0.08) + 0.4 * Math.max(0, 1 - Math.abs(t - 2.45) / 0.06)).toFixed(3));
      blades.setAttribute('transform', `translate(820,150) scale(1,0.32) rotate(${((t * 420) % 360).toFixed(1)})`);
      if (bok) bok(t);
    },
  };
}

// =====================================================================
// E — the present-day street at dusk: clinic, minimart, noodle stall, neon on the wet road
// =====================================================================
function presentStreet(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const X0 = -400, X1 = 2600;
  svg('rect', { x: X0 - 600, y: -300, width: 4400, height: 1500, fill: lin(F.defs, [[0, '#2e1f40'], [0.45, '#5a3458'], [0.8, '#b0566a'], [1, '#e08a6a']]) }, F.s);
  const r = rng(601);
  for (let x = X0 - 400; x < X1 + 800; x += 160 + r() * 120) {
    const h = 300 + r() * 500, w = 120 + r() * 90, bg = svg('g', {}, F.s);
    svg('rect', { x, y: 900 - h, width: w, height: h + 400, fill: r() < 0.5 ? '#3a2848' : '#44304e' }, bg);
    for (let wy = 930 - h; wy < 1000; wy += 34) for (let wx = x + 10; wx < x + w - 16; wx += 26) if (r() < 0.35) svg('rect', { x: wx, y: wy, width: 12, height: 16, fill: r() < 0.7 ? '#ffd98a' : '#ffb0c8', opacity: 0.8 }, bg);
  }
  svg('rect', { x: 1500, y: 300, width: 300, height: 140, rx: 8, fill: '#ffcf7a', opacity: 0.35 }, F.s);   // billboard glow
  const traffic = floaters(F.s, [X0, 900, X1 - X0, 120], 26, 602, { color: '#ffcf7a', rMin: 6, rMax: 16, speed: 4, op: 0.5, base: 0.2, amp: 60, twinkle: 2 });
  const rainF = rainField(F.s, [X0 - 600, -300, X1 + 1200, 1300], 220, 603, { len: 40, w: 1.6, op: 0.3, slant: 0.16 });
  // the clinic (left)
  const cl = svg('g', {}, M.s);
  svg('rect', { x: X0, y: 380, width: 900, height: 1030, fill: '#e8dccb', stroke: INK, 'stroke-width': 5 }, cl);
  svg('rect', { x: X0, y: 380, width: 900, height: 1030, fill: lin(M.defs, [[0, '#2a1830', 0.35], [1, '#2a1830', 0]]) }, cl);
  for (const wx of [X0 + 60, X0 + 340, X0 + 620]) { svg('rect', { x: wx, y: 470, width: 220, height: 220, rx: 6, fill: '#4a3a50', stroke: INK, 'stroke-width': 4 }, cl); svg('rect', { x: wx + 8, y: 478, width: 204, height: 204, fill: '#ffe8c4', opacity: 0.55 }, cl); }
  svg('rect', { x: X0 + 40, y: 780, width: 820, height: 110, rx: 10, fill: '#fbf7ef', stroke: INK, 'stroke-width': 5 }, cl);
  wtext(cl, X0 + 520, 856, 'คลินิกหมอใจดี', 60, '#c8343c', { w: 700 });
  const cross = svg('g', {}, cl);
  svg('circle', { cx: X0 + 160, cy: 835, r: 80, fill: rad2(M.defs, [[0, '#ff5a7a', 0.7], [1, '#ff5a7a', 0]]), style: 'mix-blend-mode:screen' }, cross);
  svg('path', { d: `M${X0 + 140},${795} h40 v20 h20 v40 h-20 v20 h-40 v-20 h-20 v-40 h20 Z`, fill: '#ff4a6a', stroke: '#fff', 'stroke-width': 4 }, cross);
  svg('rect', { x: X0 + 60, y: 930, width: 780, height: 470, fill: '#2a2226', stroke: INK, 'stroke-width': 4 }, cl);
  svg('rect', { x: X0 + 70, y: 940, width: 760, height: 450, fill: lin(M.defs, [[0, '#fff6e6'], [1, '#f2d6b0']]) }, cl);
  for (let k = 0; k < 4; k++) svg('rect', { x: X0 + 100 + k * 90, y: 1250, width: 70, height: 26, rx: 6, fill: '#4a7bd8', opacity: 0.6 }, cl);   // waiting chairs
  svg('rect', { x: X0 + 560, y: 1080, width: 220, height: 120, rx: 8, fill: '#f6efe2', stroke: INK, 'stroke-width': 3, opacity: 0.8 }, cl);
  svg('rect', { x: X0 + 450, y: 940, width: 8, height: 450, fill: '#9aa3b2' }, cl);
  // awning over the clinic door
  svg('path', { d: `M${X0 + 20},900 L${X0 + 880},900 L${X0 + 910},960 L${X0 - 10},960 Z`, fill: '#7a2a40', stroke: INK, 'stroke-width': 4 }, cl);
  // the minimart (bright) in the middle, noodle stall on the right
  const mm = svg('g', {}, M.s);
  svg('rect', { x: 560, y: 520, width: 900, height: 890, fill: '#f2e6d6', stroke: INK, 'stroke-width': 5 }, mm);
  svg('rect', { x: 560, y: 520, width: 900, height: 120, fill: '#e0573a' }, mm);
  svg('rect', { x: 560, y: 640, width: 900, height: 24, fill: '#f2a03a' }, mm);
  wtext(mm, 1010, 604, 'มินิมาร์ท 24 ชม.', 64, '#fbf2e2', { w: 700 });
  svg('rect', { x: 600, y: 700, width: 820, height: 700, fill: '#2a2226', stroke: INK, 'stroke-width': 4 }, mm);
  svg('rect', { x: 610, y: 710, width: 800, height: 680, fill: lin(M.defs, [[0, '#fffaf0'], [1, '#ffe8c8']]) }, mm);
  for (const sy of [820, 960, 1100]) { svg('rect', { x: 640, y: sy, width: 520, height: 10, fill: '#b8b0a4' }, mm); for (let k = 0; k < 13; k++) svg('rect', { x: 646 + k * 40, y: sy - 46, width: 32, height: 46, rx: 4, fill: ['#e0453b', '#f2c14e', '#4a7bd8', '#5aa05c', '#e88aa8', '#f6f1e8'][(k * 7 + sy) % 6], stroke: INK, 'stroke-width': 1.5 }, mm); }
  svg('rect', { x: 1200, y: 760, width: 180, height: 600, rx: 8, fill: '#dfe6ea', stroke: INK, 'stroke-width': 3 }, mm);   // fridges
  for (let k = 0; k < 3; k++) svg('rect', { x: 1210, y: 780 + k * 190, width: 160, height: 170, fill: ['#e0453b', '#5aa05c', '#f2c14e'][k], opacity: 0.35 }, mm);
  svg('rect', { x: 880, y: 700, width: 8, height: 700, fill: '#9aa3b2' }, mm);
  const mmGlow = lightPool(M.s, M.defs, 1010, 1440, 560, 80, '#fff1d6', 0.45);
  const stall = svg('g', {}, M.s);
  svg('path', { d: 'M1500,860 L1980,860 L2010,930 L1470,930 Z', fill: '#2d6a4a', stroke: INK, 'stroke-width': 4 }, stall);
  for (let k = 0; k < 6; k++) svg('path', { d: `M${1500 + k * 80},860 l40,0 l8,70 l-40,0 Z`, fill: '#f6efe2' }, stall);
  svg('rect', { x: 1520, y: 1180, width: 420, height: 230, rx: 10, fill: '#c9d2dc', stroke: INK, 'stroke-width': 4 }, stall);
  for (const [px, c] of [[1600, '#9aa3b2'], [1700, '#b8c0c8']]) svg('ellipse', { cx: px, cy: 1180, rx: 46, ry: 14, fill: c, stroke: INK, 'stroke-width': 3 }, stall);
  for (let k = 0; k < 5; k++) svg('rect', { x: 1760 + k * 30, y: 1120, width: 22, height: 60, rx: 4, fill: ['#f2c14e', '#e0453b'][k % 2], stroke: INK, 'stroke-width': 2 }, stall);
  wtext(stall, 1730, 1300, 'ก๋วยเตี๋ยวเรือ', 40, '#7a2a2e');
  const steam = floaters(M.s, [1560, 1000, 220, 180], 10, 604, { color: '#f6efe6', rMin: 12, rMax: 26, speed: 50, op: 0.25, base: 0.05, amp: 16 });
  const bulbs = lightString(M.s, 1470, 2000, 930, 20, ['#ffd66b', '#ffb0c8', '#fff1c4'], 9);
  // sidewalk, kerb, road with neon reflections
  svg('rect', { x: X0 - 400, y: 1405, width: 4400, height: 60, fill: lin(M.defs, [[0, '#8a7a84'], [1, '#6a5a64']]) }, M.s);
  svg('rect', { x: X0 - 400, y: 1462, width: 4400, height: 10, fill: '#d8cfc4', stroke: INK, 'stroke-width': 2 }, M.s);
  const road = wetRoad(M.s, M.defs, 1472, '#3a2a3a', '#1a1220', [[X0 + 160, 60, '#ff5a7a', 0.55], [X0 + 450, 500, '#fff1d6', 0.25], [1010, 700, '#fff1d6', 0.3], [1010, 120, '#e0573a', 0.45], [1730, 300, '#ffd66b', 0.25]]);
  wallAO(M.s, M.defs, 1405, { op: 0.2, h: 100 });
  // parked motorbikes with rain covers
  for (const mx of [-200, 1980]) { const mb = svg('g', {}, M.s); for (const wx of [mx, mx + 190]) svg('circle', { cx: wx, cy: 1420, r: 38, fill: '#2a2226', stroke: INK, 'stroke-width': 4 }, mb); svg('path', { d: `M${mx - 40},1400 Q${mx + 20},1260 ${mx + 130},1270 Q${mx + 220},1280 ${mx + 230},1400 Z`, fill: '#5a6aa8', stroke: INK, 'stroke-width': 4, opacity: 0.9 }, mb); }
  const walkers = umbrellaWalkers(M.s, M.defs, 6, 605, 1404, X0, X1, { op: 0.55, s: 0.9 });
  const puds = [[200, 1600, 190, 26], [800, 1700, 220, 30], [1400, 1590, 170, 24], [2000, 1680, 200, 28], [500, 1860, 150, 22]].map(([cx, cy, rx, ry], i) => puddle(M.s, M.defs, cx, cy, rx, ry, '#c86a8a', 610 + i));
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, people);
  const reflG = svg('g', { mask: reflFade(M.defs, 1520, 320) }, M.s); M.s.insertBefore(reflG, shadowL);
  const top = svg('g', {}, M.s);
  const rain = svg('g', {}, M.s);
  const rainM = rainField(rain, [X0 - 400, -300, X1 + 400, 1920], 420, 606, { len: 70, w: 2.4, op: 0.5, slant: 0.16 });
  const splash = splashField(M.s, X0, X1, 1410, 1900, 60, 607);
  const dPts = []; for (let x = X0; x < X0 + 900; x += 40) dPts.push([x, 962, 1405]); for (let x = 1470; x < 2010; x += 40) dPts.push([x, 932, 1180]);
  const drips = dripLine(M.s, dPts, 608);
  let bok = null, rainR = null;
  if (R) { bok = bokehField(R.s, R.defs, 9, [X0, -100, X1, 700], ['#ff8aa8', '#ffcf7a', '#fff1d6'], 609, { rMin: 30, rMax: 80, op: 0.3 }); rainR = rainField(R.s, [X0 - 400, -300, X1 + 400, 2200], 70, 611, { len: 150, w: 5, op: 0.25, slant: 0.16, speed: 2600 }); }
  const vg = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;pointer-events:none' }); S.fx.appendChild(vg);
  vignette(vg, svg('defs', {}, vg), 0.5);
  return {
    people, shadowL, top, rain, reflG, ground: 1520, slant: 0.16, light: { ux: 0.6, uy: -0.8, lx: 1010 },
    update(t, dens = 1) {
      traffic(t); rainF(t, dens); rainM(t, dens); splash(t, dens); drips(t, dens); road(t); steam(t); walkers(t);
      puds.forEach(p => p(t, dens));
      cross.setAttribute('opacity', (0.85 + 0.15 * Math.sin(t * 6)).toFixed(3));
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2.6 + i * 1.7)).toFixed(2)));
      if (bok) bok(t); if (rainR) rainR(t, dens);
    },
  };
}
