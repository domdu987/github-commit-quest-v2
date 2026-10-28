// "47 ครั้งที่ลบข้อความ" sets: his room at night (beanbag, guitar, posters) and her room at night (bed, plushies, fairy lights).

const leafG = (R, x, y, s, a, c, vein = '#3e3448') => {
  const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
  svg('path', { d: 'M0,0 C40,-60 120,-70 200,-20 C120,10 50,20 0,0 Z', fill: c }, g);
  svg('path', { d: 'M8,-2 C70,-30 130,-34 190,-20', fill: 'none', stroke: vein, 'stroke-width': 3, opacity: 0.5 }, g);
  return g;
};
const swayLeaves = (leaves, t) => leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });

function nightWindow(F, x, y, w, h, frame, seed) {
  svg('rect', { x, y, width: w, height: h, rx: 10, fill: frame, stroke: INK, 'stroke-width': 6 }, F.s);
  svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32, fill: lin(F.defs, [[0, '#141b3c'], [1, '#2c2f63']]) }, F.s);
  const r = rng(seed), stars = [];
  for (let i = 0; i < 26; i++) stars.push(svg('circle', { cx: x + 24 + r() * (w - 48), cy: y + 24 + r() * (h * 0.55), r: 1.2 + r() * 1.8, fill: '#fff' }, F.s));
  svg('circle', { cx: x + w * 0.72, cy: y + h * 0.25, r: 70, fill: rad2(F.defs, [[0, '#fff6dc', 0.45], [1, '#fff6dc', 0]]) }, F.s);
  svg('circle', { cx: x + w * 0.72, cy: y + h * 0.25, r: 30, fill: '#f6eed8' }, F.s);
  let bx = x + 16;
  while (bx < x + w - 16) {
    const bw = Math.min(30 + r() * 46, x + w - 16 - bx), bh = 80 + r() * 160;
    svg('rect', { x: bx, y: y + h - 16 - bh, width: bw, height: bh, fill: r() > 0.5 ? '#1d2348' : '#252b55' }, F.s);
    for (let wy = y + h - 6 - bh; wy < y + h - 26; wy += 22) for (let wx = bx + 5; wx < bx + bw - 7; wx += 13) if (r() > 0.6) svg('rect', { x: wx, y: wy, width: 5, height: 8, fill: '#f6c86a', opacity: 0.85 }, F.s);
    bx += bw + 3;
  }
  svg('rect', { x: x + w / 2 - 4, y: y + 16, width: 8, height: h - 32, fill: frame }, F.s);
  return stars;
}
function fairyLights(F, x0, x1, y, sag, colors, n) {
  svg('path', { d: `M${x0},${y} Q${(x0 + x1) / 2},${y + sag * 2} ${x1},${y}`, fill: 'none', stroke: '#4a3e52', 'stroke-width': 3 }, F.s);
  return Array.from({ length: n }, (_, k) => {
    const u = (k + 0.5) / n, bx = x0 + (x1 - x0) * u, by = y + sag * 4 * u * (1 - u) * 1;
    const g = svg('g', {}, F.s);
    svg('circle', { cx: bx, cy: by + 12, r: 18, fill: colors[k % colors.length], opacity: 0.25 }, g);
    svg('circle', { cx: bx, cy: by + 12, r: 7, fill: colors[k % colors.length] }, g);
    return g;
  });
}

// ---------------- his room at night ----------------
function guyRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1700, fill: lin(F.defs, [[0, '#1f2a48'], [1, '#2c3a5e']]) }, F.s);
  const stars = nightWindow(F, 560, 200, 380, 470, '#d9c7a8', 12);
  // posters: guitar + planet
  svg('rect', { x: 120, y: 260, width: 190, height: 250, rx: 6, fill: '#f2c14e', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('circle', { cx: 215, cy: 370, r: 56, fill: '#e0574b' }, F.s);
  svg('ellipse', { cx: 215, cy: 370, rx: 92, ry: 18, fill: 'none', stroke: '#1f2a48', 'stroke-width': 7, transform: 'rotate(-18 215 370)' }, F.s);
  svg('rect', { x: 340, y: 330, width: 150, height: 110, rx: 6, fill: '#7fd6c7', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('path', { d: 'M360,420 L400,370 L430,400 L460,355 L476,420 Z', fill: '#2f6a74' }, F.s);
  const lights = fairyLights(F, 60, 1040, 150, 26, ['#ffd66b', '#7fd6ff', '#ff9fc0'], 12);
  // floor, rug
  woodFloor(M.s, M.defs, 1350, '#4a3a3a', '#2c2226', '#3a2c2e');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#2c2226' }, M.s);
  rug(M.s, M.defs, 470, 1520, 440, 100, '#3f5a8a');
  // low bed on the right
  svg('rect', { x: 600, y: 1080, width: 520, height: 70, rx: 22, fill: '#cfd6e2', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 600, y: 1140, width: 520, height: 160, rx: 12, fill: '#5d6f96', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('path', { d: 'M640,1100 Q800,1040 1120,1090 L1120,1170 Q860,1190 640,1150 Z', fill: '#8fa4c9', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 940, y: 1040, width: 160, height: 70, rx: 30, fill: '#f4f1ea', stroke: INK, 'stroke-width': 5 }, M.s);
  // guitar leaning on the wall
  const gt = svg('g', { transform: 'translate(520,1340) rotate(-12)' }, M.s);
  svg('rect', { x: -8, y: -420, width: 16, height: 250, fill: '#5a3b2a', stroke: INK, 'stroke-width': 4 }, gt);
  svg('path', { d: 'M0,-190 C-70,-190 -76,-110 -40,-90 C-90,-60 -86,10 0,10 C86,10 90,-60 40,-90 C76,-110 70,-190 0,-190 Z', fill: '#e08a3c', stroke: INK, 'stroke-width': 5 }, gt);
  svg('circle', { cx: 0, cy: -100, r: 18, fill: '#3a2620' }, gt);
  svg('rect', { x: -14, y: -440, width: 28, height: 30, rx: 6, fill: '#3a2620' }, gt);
  // desk lamp glow + laundry basket
  svg('circle', { cx: 980, cy: 900, r: 260, fill: rad2(M.defs, [[0, '#ffd59a', 0.35], [1, '#ffd59a', 0]]) }, M.s);
  svg('path', { d: 'M40,1360 L60,1250 L200,1250 L220,1360 Z', fill: '#c9a87a', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('path', { d: 'M70,1250 Q110,1200 150,1240 Q170,1210 190,1250 Z', fill: '#e0574b', stroke: INK, 'stroke-width': 3 }, M.s);
  // beanbag he sits in
  const bean = svg('g', {}, M.s);
  contactShadow(bean, M.defs, 300, 1372, 210, 22, 0.45);
  svg('path', { d: 'M110,1370 C90,1260 150,1180 250,1190 C330,1150 440,1200 470,1290 C490,1350 470,1380 400,1384 L170,1384 C130,1384 112,1380 110,1370 Z', fill: lin(M.defs, [[0, '#ef6a5a'], [1, '#c9473a']]), stroke: INK, 'stroke-width': 6 }, bean);
  svg('path', { d: 'M180,1250 Q240,1230 300,1260', fill: 'none', stroke: '#ff9a8a', 'stroke-width': 6, 'stroke-linecap': 'round', opacity: 0.7 }, bean);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#24473a'), leafG(R, 1150, 1960, 1.4, -150, '#2b5243')] : [];
  return {
    people, top,
    update(t) {
      stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.7)).toFixed(2)));
      lights.forEach((l, i) => l.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.4 + i)).toFixed(2)));
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- her room at night ----------------
function girlRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1700, fill: lin(F.defs, [[0, '#5e4a7e'], [1, '#7a5f92']]) }, F.s);
  for (let i = 0; i < 18; i++) svg('rect', { x: -300 + i * 100, y: -300, width: 50, height: 1700, fill: '#ffffff', opacity: 0.05 }, F.s);
  const stars = nightWindow(F, 140, 220, 360, 440, '#f6efe2', 21);
  const lights = fairyLights(F, 40, 1040, 160, 30, ['#ff9fc0', '#ffd66b', '#ffffff'], 13);
  // shelf with plushies + heart poster
  svg('rect', { x: 600, y: 520, width: 380, height: 16, rx: 6, fill: '#e2c49a', stroke: INK, 'stroke-width': 4 }, F.s);
  for (const [x, c] of [[650, '#ffc4d2'], [740, '#bfe6ff'], [830, '#ffe7a8'], [920, '#c9f0c4']]) {
    svg('circle', { cx: x, cy: 480, r: 34, fill: c, stroke: INK, 'stroke-width': 4 }, F.s);
    for (const ex of [-20, 20]) svg('circle', { cx: x + ex, cy: 452, r: 11, fill: c, stroke: INK, 'stroke-width': 3 }, F.s);
    for (const ex of [-10, 10]) svg('circle', { cx: x + ex, cy: 478, r: 3.5, fill: INK }, F.s);
  }
  svg('rect', { x: 640, y: 260, width: 180, height: 200, rx: 8, fill: '#fff3f6', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('path', { d: 'M730,420 C670,380 680,320 730,350 C780,320 790,380 730,420 Z', fill: '#f07aa8' }, F.s);
  // floor + heart rug
  woodFloor(M.s, M.defs, 1385, '#e7d2c0', '#c9ad98', '#b89a86');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#c9ad98' }, M.s);
  svg('path', { d: 'M460,1690 C300,1600 320,1500 460,1560 C600,1500 620,1600 460,1690 Z', fill: '#ffb6c8', opacity: 0.85 }, M.s);
  // bed
  contactShadow(M.s, M.defs, 780, 1394, 330, 20, 0.35);
  svg('rect', { x: 520, y: 1120, width: 40, height: 270, rx: 14, fill: '#f6efe2', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 540, y: 1240, width: 580, height: 60, rx: 18, fill: '#ffffff', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 540, y: 1290, width: 580, height: 90, rx: 10, fill: '#f6efe2', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('path', { d: 'M820,1250 Q900,1200 1120,1230 L1120,1300 Q960,1320 820,1300 Z', fill: '#f7a8bb', stroke: INK, 'stroke-width': 5 }, M.s);
  // nightstand lamp
  svg('rect', { x: 330, y: 1200, width: 150, height: 190, rx: 10, fill: '#e2c49a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('path', { d: 'M405,1200 L405,1120 M370,1120 L440,1120 L425,1060 L385,1060 Z', stroke: INK, 'stroke-width': 4, fill: '#ffe2a8' }, M.s);
  svg('circle', { cx: 405, cy: 1100, r: 200, fill: rad2(M.defs, [[0, '#ffe9b0', 0.4], [1, '#ffe9b0', 0]]) }, M.s);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.45);
  const leaves = R ? [leafG(R, -120, 1900, 1.6, -60, '#3a6b47'), leafG(R, -80, 1960, 1.4, -25, '#4f8f56')] : [];
  return {
    people, top,
    update(t) {
      stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.3)).toFixed(2)));
      lights.forEach((l, i) => l.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.1 + i)).toFixed(2)));
      swayLeaves(leaves, t);
    },
  };
}
