// "4,380 วันที่รอ" sets, in the story2 language: the entrance at home (sunset → night, the door can open), the living room
// at night, the vet clinic, and her office late at night.

const leafG = (R, x, y, s, a, c, vein = '#3e3448') => {
  const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
  svg('path', { d: 'M0,0 C40,-60 120,-70 200,-20 C120,10 50,20 0,0 Z', fill: c }, g);
  svg('path', { d: 'M8,-2 C70,-30 130,-34 190,-20', fill: 'none', stroke: vein, 'stroke-width': 3, opacity: 0.5 }, g);
  return g;
};
const swayLeaves = (leaves, t) => leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });
const mixC = (a, b, k) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * clamp(k, 0, 1)).toString(16).padStart(2, '0')).join(''); };

// a window into the city whose sky runs from sunset (k=0) to night (k=1); returns an updater
function cityWindow(F, x, y, w, h, seed, frame = '#2a2236') {
  svg('rect', { x, y, width: w, height: h, rx: 8, fill: frame }, F.s);
  const id = 'cw' + Math.random().toString(36).slice(2, 7);
  const cp = svg('clipPath', { id }, F.defs); svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32 }, cp);
  const g = svg('g', { 'clip-path': `url(#${id})` }, F.s);
  const day = svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32, fill: lin(F.defs, [[0, '#6a5a9a'], [0.45, '#f08c7a'], [0.8, '#ffc58a'], [1, '#ffe2b0']]) }, g);
  const night = svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32, fill: lin(F.defs, [[0, '#141636'], [1, '#2b2c5a']]), opacity: 0 }, g);
  const sun = svg('circle', { cx: x + w * 0.3, cy: y + h * 0.62, r: 46, fill: '#fff1c8' }, g);
  const moon = svg('circle', { cx: x + w * 0.72, cy: y + 90, r: 28, fill: '#f6eed8', opacity: 0 }, g);
  const r = rng(seed), lit = [], blds = [];
  let bx = x + 16;
  while (bx < x + w - 16) {
    const bw = Math.min(40 + r() * 54, x + w - 16 - bx), bh = 110 + r() * 200, by = y + h - 16 - bh;
    blds.push(svg('rect', { x: bx, y: by, width: bw, height: bh, fill: '#6a5878' }, g));
    for (let wy = by + 14; wy < y + h - 26; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14) if (r() > 0.5) lit.push({ el: svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#f6c86a', opacity: 0 }, g), th: r() });
    bx += bw + 3;
  }
  svg('rect', { x: x + w / 2 - 3, y: y + 16, width: 6, height: h - 32, fill: frame }, F.s);
  return (k, t) => {
    night.setAttribute('opacity', clamp(k * 1.3, 0, 1).toFixed(3));
    sun.setAttribute('opacity', (1 - clamp(k * 2.5, 0, 1)).toFixed(3)); sun.setAttribute('cy', (y + h * 0.62 + k * 160).toFixed(1));
    moon.setAttribute('opacity', clamp(k * 1.6 - 0.6, 0, 1).toFixed(3));
    const bc = mixC('#6a5878', '#22244a', k);
    blds.forEach(b => b.setAttribute('fill', bc));
    lit.forEach(w => w.el.setAttribute('opacity', (k > w.th * 0.6 ? (Math.sin(t * 1.3 + w.th * 40) > -0.85 ? 0.9 : 0.2) : 0).toFixed(2)));
  };
}
function curtains(F, x0, x1, y, h, night) {
  for (const cx of [x0, x1]) {
    svg('rect', { x: cx, y, width: 86, height: h, rx: 16, fill: lin(F.defs, night ? [[0, '#5d6a8a'], [1, '#4b5776']] : [[0, '#f4ecdf'], [1, '#e4d8c6']], 1, 0) }, F.s);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: y + 10, width: 7, height: h - 20, rx: 3, fill: night ? '#4a5572' : '#ddd0bc' }, F.s);
  }
}

// ---------------- the entrance: front door, shoe rack, dog mat; k: 0 = 18:00 sunset … 1 = 22:00 night ----------------
function entrance(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const wall = svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: '#c9a98a' }, F.s);
  const wallShade = svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#000', 0.0], [1, '#000', 0.18]]) }, F.s);
  const win = cityWindow(F, 640, 250, 360, 430, 61);
  curtains(F, 606, 966, 230, 500, false);
  svg('rect', { x: 590, y: 222, width: 460, height: 12, rx: 6, fill: '#8a6a52' }, F.s);
  // wall clock above the door
  const clock = svg('g', { transform: 'translate(310,190)' }, F.s);
  svg('circle', { r: 58, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, clock);
  for (let k = 0; k < 12; k++) svg('rect', { x: -2, y: -50, width: 4, height: k % 3 ? 6 : 12, fill: INK, transform: `rotate(${k * 30})` }, clock);
  const hh = svg('path', { d: 'M0,0 L0,-28', stroke: INK, 'stroke-width': 6, 'stroke-linecap': 'round' }, clock);
  const mm = svg('path', { d: 'M0,0 L0,-42', stroke: INK, 'stroke-width': 4, 'stroke-linecap': 'round' }, clock);
  svg('circle', { r: 5, fill: INK }, clock);
  // the door (opens on its left hinge) with the hallway light behind it
  svg('rect', { x: 150, y: 290, width: 320, height: 1030, fill: '#3a2a22', stroke: INK, 'stroke-width': 6 }, F.s);
  const hall = svg('rect', { x: 160, y: 300, width: 300, height: 1020, fill: lin(F.defs, [[0, '#fff2c8'], [1, '#e8c98f']]) }, F.s);
  const outside = svg('g', {}, F.s);
  const door = svg('g', {}, F.s);
  svg('rect', { x: 160, y: 300, width: 300, height: 1020, fill: lin(F.defs, [[0, '#a8744e'], [1, '#8a5d3c']], 1, 0), stroke: INK, 'stroke-width': 5 }, door);
  for (const [py, ph] of [[340, 420], [800, 470]]) svg('rect', { x: 196, y: py, width: 228, height: ph, rx: 8, fill: 'none', stroke: '#6a4428', 'stroke-width': 5 }, door);
  svg('circle', { cx: 422, cy: 820, r: 13, fill: '#f2c14e', stroke: INK, 'stroke-width': 4 }, door);
  svg('circle', { cx: 310, cy: 470, r: 7, fill: '#2a1d21' }, door);
  // floor, doormat, shoe rack with shoes, umbrella, plant, the dog's water bowl
  const fl = svg('rect', { x: -300, y: 1320, width: 1680, height: 1000, fill: '#8a5d3c' }, M.s);
  woodFloor(M.s, M.defs, 1320, '#9a6c48', '#6a4428', '#5a3b24');
  svg('path', { d: 'M120,1360 L500,1360 L540,1440 L80,1440 Z', fill: '#c96a5a', stroke: INK, 'stroke-width': 5 }, M.s);
  for (let k = 0; k < 6; k++) svg('path', { d: `M${150 + k * 62},1366 L${132 + k * 66},1434`, stroke: '#a85446', 'stroke-width': 5 }, M.s);
  const rack = svg('g', { transform: 'translate(560,1140)' }, M.s);
  svg('rect', { x: 0, y: 0, width: 240, height: 190, rx: 10, fill: '#c9a27a', stroke: INK, 'stroke-width': 5 }, rack);
  for (const ry of [62, 126]) svg('rect', { x: 8, y: ry, width: 224, height: 8, fill: '#8a6a52' }, rack);
  for (const [sx, sy, c] of [[20, 30, '#4a7bd8'], [120, 30, '#f2c14e'], [30, 94, '#e0574b'], [130, 94, '#2f9e5b'], [24, 158, '#f6f1e6']]) svg('path', { d: `M${sx},${sy + 26} L${sx},${sy + 6} Q${sx + 30},${sy} ${sx + 54},${sy + 18} L${sx + 80},${sy + 22} L${sx + 80},${sy + 26} Z`, fill: c, stroke: INK, 'stroke-width': 3.5 }, rack);
  svg('rect', { x: 830, y: 1060, width: 16, height: 270, rx: 8, fill: '#4a7bd8', stroke: INK, 'stroke-width': 4, transform: 'rotate(8 838 1330)' }, M.s);
  const plant = svg('g', { transform: 'translate(960,1330)' }, M.s);
  svg('path', { d: 'M-50,-90 L50,-90 L40,0 L-40,0 Z', fill: '#d0774a', stroke: INK, 'stroke-width': 5 }, plant);
  for (let k = 0; k < 7; k++) svg('ellipse', { cx: (k - 3) * 22, cy: -150 - Math.abs(k - 3) * -10, rx: 16, ry: 60, fill: k % 2 ? '#4f8a5b' : '#3f7a4c', stroke: INK, 'stroke-width': 3, transform: `rotate(${(k - 3) * 16} ${(k - 3) * 22} -95)` }, plant);
  const bowl = svg('g', { transform: 'translate(690,1420)' }, M.s);
  svg('ellipse', { cx: 0, cy: 0, rx: 56, ry: 16, fill: '#e0574b', stroke: INK, 'stroke-width': 4 }, bowl);
  svg('ellipse', { cx: 0, cy: -6, rx: 42, ry: 9, fill: '#9fd2f5' }, bowl);
  // warm hallway spill when the door opens + room light that dims with the hour
  const spill = svg('path', { d: 'M160,300 L460,300 L640,1600 L60,1600 Z', fill: lin(M.defs, [[0, '#fff2c8', 0.5], [1, '#fff2c8', 0]]), opacity: 0 }, M.s);
  const lamp = svg('circle', { cx: 900, cy: 700, r: 520, fill: rad2(M.defs, [[0, '#ffd59a', 0.35], [1, '#ffd59a', 0]]), opacity: 0 }, M.s);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const dusk = svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: '#1a1430', opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.45);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#24473a'), leafG(R, 1150, 1960, 1.4, -150, '#2b5243')] : [];
  return {
    people, top, outside, doorX: 160,
    update(t, k = 0, open = 0, hour = 18) {
      win(k, t);
      wall.setAttribute('fill', mixC('#d9b48e', '#4a4062', k));
      fl.setAttribute('fill', mixC('#8a5d3c', '#2c2230', k));
      dusk.setAttribute('opacity', (0.18 * k).toFixed(3));
      lamp.setAttribute('opacity', clamp(k * 1.5, 0, 1).toFixed(3));
      door.setAttribute('transform', `translate(160,0) scale(${(1 - 0.85 * open).toFixed(3)},1) translate(-160,0)`);
      spill.setAttribute('opacity', (open * 0.9).toFixed(3));
      hall.setAttribute('opacity', open > 0.01 ? 1 : 0);
      hh.setAttribute('transform', `rotate(${((hour % 12) * 30).toFixed(1)})`); mm.setAttribute('transform', `rotate(${((hour % 1) * 360).toFixed(1)})`);
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- living room at night: sofa, floor lamp, rug, TV glow ----------------
function livingNight(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#3f3a5a'], [1, '#544a6a']]) }, F.s);
  const win = cityWindow(F, 140, 210, 440, 520, 73);
  curtains(F, 106, 546, 190, 620, true);
  svg('rect', { x: 90, y: 182, width: 560, height: 12, rx: 6, fill: '#2f2a40' }, F.s);
  // framed photo: her and the puppy, years ago
  svg('rect', { x: 740, y: 330, width: 210, height: 170, rx: 6, fill: '#fbf7ef' }, F.s);
  svg('rect', { x: 754, y: 344, width: 182, height: 142, fill: '#f0c9a8' }, F.s);
  dogFace(F.s, 880, 430, 30, { happy: true });
  ownerFace(F.s, 808, 424, 30, { happy: true });
  woodFloor(M.s, M.defs, 1330, '#3a3448', '#221d2c', '#2a2130');
  svg('rect', { x: -300, y: 1330, width: 300, height: 1000, fill: '#2a2130' }, M.s); svg('rect', { x: 1080, y: 1330, width: 300, height: 1000, fill: '#2a2130' }, M.s);
  rug(M.s, M.defs, 540, 1560, 470, 110, '#41506a');
  svg('path', { d: 'M156,226 L564,226 L980,1560 L240,1560 Z', fill: lin(M.defs, [[0, '#c9d6ff', 0.12], [1, '#c9d6ff', 0.0]]) }, M.s);
  floorLamp(M.s, M.defs, 960, 1330, '#ffd59a', 0.5);
  svg('circle', { cx: 960, cy: 820, r: 120, fill: rad2(M.defs, [[0, '#fff2d0', 0.7], [1, '#fff2d0', 0]]) }, M.s);
  contactShadow(M.s, M.defs, 520, 1338, 470, 26, 0.45);
  sofa(M.s, M.defs, 170, 1140, 700, -6);
  const tv = svg('ellipse', { cx: 1080, cy: 1200, rx: 380, ry: 520, fill: rad2(M.defs, [[0, '#9fc6ff', 0.3], [1, '#9fc6ff', 0]]) }, M.s);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 220, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.5);
  const leaves = R ? [leafG(R, -120, 1880, 1.6, -60, '#1d3a2d'), leafG(R, -80, 1900, 1.5, -25, '#24473a'), leafG(R, -160, 1700, 1.4, -5, '#2b5243')] : [];
  if (R) svg('circle', { cx: 1040, cy: 200, r: 90, fill: '#ffcf8a', opacity: 0.25 }, R.s);
  return {
    people, top, pglow,
    update(t) {
      win(1, t);
      tv.setAttribute('opacity', (0.75 + 0.25 * Math.sin(t * 7) * Math.sin(t * 2.3)).toFixed(3));
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- vet clinic: mint walls, exam table, poster, lamp ----------------
function vetClinic(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#cfe6dc'], [1, '#b9d8cc']]) }, F.s);
  for (let i = -4; i < 18; i++) svg('rect', { x: i * 80, y: 980, width: 78, height: 360, fill: '#e8f3ee', stroke: '#c4ddd2', 'stroke-width': 3 }, F.s);
  // blinds window with soft daylight
  svg('rect', { x: 620, y: 220, width: 360, height: 400, rx: 8, fill: '#9fb8ae' }, F.s);
  svg('rect', { x: 634, y: 234, width: 332, height: 372, fill: lin(F.defs, [[0, '#d8eef8'], [1, '#fff6e2']]) }, F.s);
  for (let k = 0; k < 13; k++) svg('rect', { x: 634, y: 240 + k * 28, width: 332, height: 14, fill: '#f6f1e6', opacity: 0.9 }, F.s);
  // poster: a dog and a cat with a heart cross
  svg('rect', { x: 140, y: 280, width: 260, height: 330, rx: 10, fill: '#fffaf2', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('rect', { x: 140, y: 280, width: 260, height: 70, rx: 10, fill: '#4fae9b' }, F.s);
  svg('path', { d: 'M256,300 L284,300 L284,312 L296,312 L296,328 L284,328 L284,340 L256,340 L256,328 L244,328 L244,312 L256,312 Z', fill: '#fff' }, F.s);
  dogFace(F.s, 222, 470, 46, { happy: true });
  svg('circle', { cx: 324, cy: 486, r: 40, fill: '#9aa3b2', stroke: INK, 'stroke-width': 4 }, F.s);
  for (const sx of [-1, 1]) svg('path', { d: `M${324 + sx * 14},458 L${324 + sx * 34},420 L${324 + sx * 38},466 Z`, fill: '#9aa3b2', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, F.s);
  for (const sx of [-1, 1]) svg('circle', { cx: 324 + sx * 14, cy: 482, r: 5, fill: INK }, F.s);
  // cabinet with bottles
  svg('rect', { x: 860, y: 720, width: 200, height: 260, rx: 8, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, F.s);
  for (const [bx, c] of [[880, '#e8a04a'], [930, '#4a7bd8'], [980, '#e0574b'], [1020, '#2f9e5b']]) svg('rect', { x: bx, y: 760, width: 30, height: 60, rx: 6, fill: c, stroke: INK, 'stroke-width': 3 }, F.s);
  svg('rect', { x: -300, y: 1340, width: 1680, height: 1000, fill: lin(M.defs, [[0, '#d9d2c4'], [1, '#bfb6a6']]) }, M.s);
  for (let i = -3; i < 14; i++) svg('path', { d: `M${i * 120},1340 L${i * 160 - 120},1920`, stroke: '#c4bca9', 'stroke-width': 3 }, M.s);
  // exam lamp + steel table
  svg('circle', { cx: 540, cy: 520, r: 380, fill: rad2(M.defs, [[0, '#fffbe8', 0.4], [1, '#fffbe8', 0]]) }, M.s);
  const table = svg('g', {}, M.s);
  contactShadow(table, M.defs, 540, 1350, 330, 22, 0.35);
  for (const lx of [330, 730]) svg('rect', { x: lx, y: 1080, width: 22, height: 270, fill: '#aeb8c6', stroke: INK, 'stroke-width': 4 }, table);
  svg('rect', { x: 280, y: 1060, width: 520, height: 40, rx: 12, fill: lin(M.defs, [[0, '#e6ebf0'], [1, '#b9c2cc']]), stroke: INK, 'stroke-width': 5 }, table);
  svg('rect', { x: 300, y: 1040, width: 480, height: 24, rx: 10, fill: '#7fc3b5', stroke: INK, 'stroke-width': 4 }, table);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.35);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#24473a'), leafG(R, 1150, 1960, 1.4, -150, '#2b5243')] : [];
  return { people, top, update(t) { swayLeaves(leaves, t); } };
}

// ---------------- her office late at night ----------------
function officeLate(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#2a2f52'], [1, '#3a3f66']]) }, F.s);
  const win = cityWindow(F, 80, 180, 920, 620, 91, '#1d2140');
  svg('rect', { x: 380, y: 196, width: 6, height: 588, fill: '#1d2140' }, F.s); svg('rect', { x: 700, y: 196, width: 6, height: 588, fill: '#1d2140' }, F.s);
  svg('rect', { x: -300, y: 1300, width: 1680, height: 1000, fill: lin(M.defs, [[0, '#2c2a40'], [1, '#1c1a2a']]) }, M.s);
  // desk, monitor, desk lamp, paper stack, coffee
  const people = svg('g', {}, M.s);
  const desk = svg('g', {}, M.s);
  contactShadow(desk, M.defs, 600, 1310, 380, 18, 0.45);
  svg('rect', { x: 360, y: 1020, width: 620, height: 34, rx: 8, fill: '#c9a27a', stroke: INK, 'stroke-width': 5 }, desk);
  svg('rect', { x: 400, y: 1054, width: 24, height: 256, fill: '#8a6a52', stroke: INK, 'stroke-width': 4 }, desk);
  svg('rect', { x: 920, y: 1054, width: 24, height: 256, fill: '#8a6a52', stroke: INK, 'stroke-width': 4 }, desk);
  svg('rect', { x: 600, y: 790, width: 300, height: 200, rx: 12, fill: '#2a2d3a', stroke: INK, 'stroke-width': 5 }, desk);
  const scr = svg('rect', { x: 614, y: 804, width: 272, height: 172, rx: 6, fill: '#cfe4ff' }, desk);
  for (let k = 0; k < 5; k++) svg('rect', { x: 632, y: 824 + k * 28, width: 120 + (k * 37) % 110, height: 10, rx: 5, fill: '#8fa9cc' }, desk);
  svg('rect', { x: 730, y: 990, width: 40, height: 30, fill: '#2a2d3a' }, desk);
  for (let k = 0; k < 5; k++) svg('rect', { x: 880 + (k % 2) * 6, y: 990 - k * 12, width: 90, height: 12, fill: '#f6f1e6', stroke: INK, 'stroke-width': 2.5 }, desk);
  svg('rect', { x: 930, y: 970, width: 36, height: 50, rx: 6, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3.5 }, desk);
  svg('circle', { cx: 760, cy: 900, r: 320, fill: rad2(M.defs, [[0, '#bfe0ff', 0.35], [1, '#bfe0ff', 0]]) }, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  return { people, top, scr, update(t) { win(1, t); } };
}
