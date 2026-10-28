// "1,095 ข้อความของแม่" sets: Mom's porch at dawn, the daughter's office at night, her bedroom in the
// morning, and Mom's room on the morning she is sick. Palettes kept away from the purple condo look.

const leafG = (R, x, y, s, a, c, vein = '#3e3448') => {
  const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
  svg('path', { d: 'M0,0 C40,-60 120,-70 200,-20 C120,10 50,20 0,0 Z', fill: c }, g);
  svg('path', { d: 'M8,-2 C70,-30 130,-34 190,-20', fill: 'none', stroke: vein, 'stroke-width': 3, opacity: 0.5 }, g);
  return g;
};
const swayLeaves = (leaves, t) => leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });

// terracotta pot with a flowering bush (bougainvillea / marigold / jasmine)
function flowerPot(g, defs, x, y, s, kind, seed) {
  const p = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  const r = rng(seed);
  const col = { bougain: ['#e8508a', '#f27aa8', '#c93a72'], marigold: ['#f59a1c', '#ffb53c', '#e07a12'], jasmine: ['#ffffff', '#f6f1e6', '#e9e2d2'] }[kind];
  const sway = svg('g', {}, p);
  for (let i = 0; i < 9; i++) svg('ellipse', { cx: -60 + r() * 120, cy: -150 + r() * 90, rx: 34 + r() * 20, ry: 22 + r() * 12, fill: ['#3f7a4a', '#4f8f56', '#356b40'][i % 3] }, sway);
  for (let i = 0; i < (kind === 'jasmine' ? 26 : 18); i++) {
    const fx = -70 + r() * 140, fy = -190 + r() * 110, fr = kind === 'jasmine' ? 6 : 9 + r() * 5;
    if (kind === 'jasmine') for (let k = 0; k < 5; k++) svg('ellipse', { cx: fx + Math.cos(k * 1.2566) * 5, cy: fy + Math.sin(k * 1.2566) * 5, rx: 4, ry: 2.6, fill: col[0], transform: `rotate(${k * 72} ${fx + Math.cos(k * 1.2566) * 5} ${fy + Math.sin(k * 1.2566) * 5})` }, sway);
    else svg('circle', { cx: fx, cy: fy, r: fr, fill: col[i % 3] }, sway);
  }
  svg('path', { d: 'M-62,-60 L62,-60 L50,0 L-50,0 Z', fill: lin(defs, [[0, '#d0774a'], [1, '#a9532f']]), stroke: INK, 'stroke-width': 4 }, p);
  svg('rect', { x: -70, y: -72, width: 140, height: 18, rx: 6, fill: '#c76a3e', stroke: INK, 'stroke-width': 4 }, p);
  return sway;
}

// ---------------- Mom's porch at dawn ----------------
function porchDawn(S) {
  const K = S.L.sky, F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -400, y: -400, width: 1880, height: 2400, fill: lin(K.defs, [[0, '#33427e'], [0.3, '#8a5f9e'], [0.52, '#f08c7a'], [0.66, '#ffc58a'], [0.8, '#ffe2b0']]) }, K.s);
  const sunG = svg('g', {}, K.s);
  svg('circle', { r: 420, fill: rad2(K.defs, [[0, '#fff1c8', 0.7], [0.35, '#ffd08a', 0.3], [1, '#ffd08a', 0]]) }, sunG);
  svg('circle', { r: 70, fill: '#fff6dc' }, sunG);
  const clouds = [];
  for (const [cx, cy, w, o] of [[180, 520, 260, 0.55], [760, 380, 320, 0.45], [520, 640, 220, 0.4], [980, 600, 200, 0.35]]) {
    const c = svg('g', { opacity: o }, K.s);
    svg('ellipse', { cx: 0, cy: 0, rx: w * 0.5, ry: 26, fill: '#ffd3c0' }, c);
    svg('ellipse', { cx: -w * 0.15, cy: -18, rx: w * 0.25, ry: 24, fill: '#ffe2d2' }, c);
    clouds.push({ c, cx, cy });
  }
  // far: tree line, palms, misty fields
  svg('path', { d: 'M-300,1000 Q-100,930 100,990 T500,980 T900,960 T1400,990 L1400,1300 L-300,1300 Z', fill: '#6c5a8a' }, F.s);
  for (const [x, h] of [[90, 260], [260, 300], [880, 240], [1010, 280]]) {
    svg('path', { d: `M${x},1000 Q${x + 8},${1000 - h * 0.5} ${x + 4},${1000 - h}`, stroke: '#4f4270', 'stroke-width': 10, fill: 'none' }, F.s);
    for (let k = 0; k < 6; k++) svg('path', { d: `M${x + 4},${1000 - h} q${Math.cos(k * 1.05) * 70},${-20 + Math.sin(k * 1.05) * 30} ${Math.cos(k * 1.05) * 120},${30 + Math.sin(k * 1.05) * 20}`, stroke: '#4f4270', 'stroke-width': 9, fill: 'none', 'stroke-linecap': 'round' }, F.s);
  }
  svg('rect', { x: -300, y: 1050, width: 1700, height: 400, fill: lin(F.defs, [[0, '#9aa07c'], [1, '#7c875f']]) }, F.s);
  for (let i = 0; i < 9; i++) svg('path', { d: `M-300,${1080 + i * 30} L1400,${1070 + i * 30}`, stroke: '#b4b88e', 'stroke-width': 3, opacity: 0.5 }, F.s);
  const mists = [0, 1, 2].map(i => svg('ellipse', { cx: 300 + i * 400, cy: 1040 + i * 30, rx: 520, ry: 40, fill: '#fff4ea', opacity: 0.35 }, F.s));
  const birds = [0, 1, 2].map(() => svg('path', { d: 'M-14,0 Q-7,-8 0,0 Q7,-8 14,0', fill: 'none', stroke: '#4a3a5a', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, F.s));
  // mid: the wooden house and porch
  const W = svg('g', {}, M.s);
  const tones = ['#a8724a', '#9c6a44', '#b07a50', '#a06d46'];
  for (let i = 0; i < 12; i++) svg('rect', { x: 500 + i * 70, y: 260, width: 70, height: 1100, fill: tones[i % 4] }, W);
  for (let i = 0; i < 12; i++) svg('rect', { x: 500 + i * 70, y: 260, width: 3, height: 1100, fill: '#7a4f30', opacity: 0.7 }, W);
  svg('rect', { x: 500, y: 260, width: 900, height: 1100, fill: lin(M.defs, [[0, '#2a1830', 0.05], [1, '#2a1830', 0.3]]) }, W);
  // window with open shutters
  svg('rect', { x: 640, y: 560, width: 250, height: 290, fill: '#3a2620', stroke: INK, 'stroke-width': 5 }, W);
  svg('rect', { x: 652, y: 572, width: 226, height: 266, fill: lin(M.defs, [[0, '#5a3a2e'], [1, '#2e1d18']]) }, W);
  svg('rect', { x: 760, y: 572, width: 8, height: 266, fill: '#3a2620' }, W);
  for (const sx of [570, 892]) {
    svg('rect', { x: sx, y: 556, width: 76, height: 298, fill: '#7f9fb0', stroke: INK, 'stroke-width': 5 }, W);
    for (let k = 0; k < 7; k++) svg('rect', { x: sx + 8, y: 572 + k * 40, width: 60, height: 10, rx: 4, fill: '#6a8a9c' }, W);
  }
  svg('rect', { x: 630, y: 846, width: 270, height: 18, rx: 6, fill: '#8a5a38', stroke: INK, 'stroke-width': 4 }, W);
  // eave + post + hanging orchid
  svg('path', { d: 'M380,250 L1400,250 L1400,330 L420,330 Z', fill: '#5a3b2a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 452, y: 320, width: 40, height: 1040, fill: lin(M.defs, [[0, '#9a6a44'], [1, '#7f5434']], 1, 0), stroke: INK, 'stroke-width': 5 }, M.s);
  const orchid = svg('g', {}, M.s);
  svg('path', { d: 'M0,0 L0,150', stroke: '#5a4030', 'stroke-width': 3 }, orchid);
  svg('rect', { x: -40, y: 150, width: 80, height: 40, rx: 8, fill: '#8a6a44', stroke: INK, 'stroke-width': 4 }, orchid);
  for (let k = 0; k < 6; k++) svg('path', { d: `M${-10 + k * 4},150 q${-40 + k * 16},-50 ${-30 + k * 14},-90`, stroke: '#4f8f56', 'stroke-width': 6, fill: 'none', 'stroke-linecap': 'round' }, orchid);
  for (let k = 0; k < 7; k++) {
    const fx = 40 + k * 12, fy = 190 + k * 22;
    svg('circle', { cx: fx, cy: fy, r: 13, fill: k % 2 ? '#b35ad6' : '#d07ae8', stroke: INK, 'stroke-width': 2.5 }, orchid);
    svg('circle', { cx: fx, cy: fy, r: 4, fill: '#fff2a0' }, orchid);
  }
  // porch floor
  svg('rect', { x: -300, y: 1350, width: 1700, height: 700, fill: lin(M.defs, [[0, '#b57d52'], [1, '#7f5232']]) }, M.s);
  for (let k = 0; k < 9; k++) svg('rect', { x: -300, y: 1360 + k * 64 + k * k * 3, width: 1700, height: 4, fill: '#6e4528', opacity: 0.6 }, M.s);
  svg('rect', { x: -300, y: 1346, width: 1700, height: 10, fill: '#5a3b2a' }, M.s);
  // bamboo bench (Mom sits here)
  contactShadow(M.s, M.defs, 760, 1356, 300, 18, 0.35);
  for (const lx of [560, 940]) svg('rect', { x: lx, y: 1250, width: 18, height: 104, fill: '#9a7a44', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('rect', { x: 530, y: 1228, width: 460, height: 28, rx: 9, fill: '#d9b878', stroke: INK, 'stroke-width': 5 }, M.s);
  for (let i = 0; i < 9; i++) svg('rect', { x: 548 + i * 50, y: 1232, width: 3, height: 20, fill: '#b08f52' }, M.s);
  const pots = [flowerPot(M.s, M.defs, 110, 1356, 1.05, 'bougain', 3), flowerPot(M.s, M.defs, 290, 1356, 0.9, 'marigold', 5), flowerPot(M.s, M.defs, 1030, 1356, 0.8, 'jasmine', 9)];
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  // dawn light: beams and warm wash
  const beams = svg('g', { opacity: 0.22 }, M.s);
  for (let k = 0; k < 4; k++) svg('path', { d: `M${120 + k * 90},${880} L${700 + k * 160},${1920} L${790 + k * 160},${1920} L${170 + k * 90},${880} Z`, fill: '#ffe6b8' }, beams);
  vignette(M.s, M.defs, 0.4);
  const leaves = R ? [leafG(R, 1180, 1900, 1.7, -130, '#2f5a3c'), leafG(R, 1140, 1960, 1.5, -150, '#3a6b47'), leafG(R, -120, 1960, 1.5, -40, '#2f5a3c')] : [];
  return {
    people, top, sunG,
    update(t) {
      const rise = Math.min(1, t / 14);
      sunG.setAttribute('transform', `translate(300,${(1010 - 170 * rise).toFixed(1)})`);
      clouds.forEach((c, i) => c.c.setAttribute('transform', `translate(${(c.cx + t * (6 + i * 2)).toFixed(1)},${c.cy})`));
      mists.forEach((m, i) => m.setAttribute('transform', `translate(${(Math.sin(t * 0.2 + i) * 60).toFixed(1)},0)`));
      birds.forEach((b, i) => { const x = -100 + ((t * (60 + i * 14) + i * 300) % 1400); b.setAttribute('transform', `translate(${x.toFixed(1)},${(560 + i * 60 + Math.sin(t * 2 + i) * 14).toFixed(1)}) scale(${(1 + 0.15 * Math.sin(t * 9 + i)).toFixed(3)},1)`); });
      pots.forEach((p, i) => p.setAttribute('transform', `skewX(${(Math.sin(t * 1.3 + i) * 1.6).toFixed(2)})`));
      orchid.setAttribute('transform', `translate(560,330) rotate(${(Math.sin(t * 1.1) * 3).toFixed(2)})`);
      beams.setAttribute('opacity', (0.16 + 0.08 * Math.sin(t * 0.7)).toFixed(3));
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- the daughter's office at night (overtime) ----------------
function officeNight(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1800, fill: lin(F.defs, [[0, '#18263c'], [1, '#22344f']]) }, F.s);
  svg('rect', { x: 60, y: 140, width: 960, height: 760, rx: 10, fill: '#0f1a2c', stroke: '#2e4466', 'stroke-width': 10 }, F.s);
  svg('rect', { x: 70, y: 150, width: 940, height: 740, fill: lin(F.defs, [[0, '#0e1630'], [1, '#22305a']]) }, F.s);
  const r = rng(77), lights = [];
  let bx = 70;
  while (bx < 1010) {
    const bw = Math.min(50 + r() * 70, 1010 - bx), bh = 200 + r() * 420, by = 890 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: r() > 0.5 ? '#1a2546' : '#22305a' }, F.s);
    for (let wy = by + 16; wy < 880; wy += 26) for (let wx = bx + 8; wx < bx + bw - 10; wx += 16)
      if (r() > 0.6) lights.push({ el: svg('rect', { x: wx, y: wy, width: 7, height: 10, fill: r() > 0.3 ? '#7fd6ff' : '#ffd27a' }, F.s), ph: r() * 40, rate: 0.2 + r() * 0.4 });
    bx += bw + 4;
  }
  svg('circle', { cx: 860, cy: 260, r: 36, fill: '#f4f0dc' }, F.s);
  for (let x = 120; x < 1010; x += 220) svg('rect', { x, y: 150, width: 6, height: 740, fill: '#2e4466' }, F.s);
  for (const x of [200, 640]) svg('rect', { x, y: 40, width: 280, height: 18, rx: 9, fill: '#d9f2ff', opacity: 0.8 }, F.s);
  // mid: partition, desk, monitor, lamp, mug, files
  svg('rect', { x: -300, y: 960, width: 1700, height: 260, fill: '#2f4560' }, M.s);
  svg('rect', { x: -300, y: 950, width: 1700, height: 16, fill: '#4a6688' }, M.s);
  svg('rect', { x: -300, y: 1420, width: 1700, height: 700, fill: lin(M.defs, [[0, '#2a3b55'], [1, '#18243a']]) }, M.s);
  const mon = svg('g', {}, M.s);
  svg('rect', { x: 776, y: 1080, width: 26, height: 90, fill: '#3a4258', stroke: INK, 'stroke-width': 4 }, mon);
  svg('rect', { x: 730, y: 1160, width: 120, height: 16, rx: 6, fill: '#3a4258', stroke: INK, 'stroke-width': 4 }, mon);
  svg('rect', { x: 600, y: 820, width: 380, height: 270, rx: 14, fill: '#2a3044', stroke: INK, 'stroke-width': 6 }, mon);
  const scr = svg('rect', { x: 614, y: 834, width: 352, height: 242, rx: 6, fill: lin(M.defs, [[0, '#dff3ff'], [1, '#b8dcf5']]) }, mon);
  const bars = [0, 1, 2, 3, 4, 5].map(i => svg('rect', { x: 640 + i * 52, y: 1040, width: 30, height: 10, fill: ['#4a7bd8', '#2f9e5b', '#e0574b'][i % 3] }, mon));
  for (let k = 0; k < 4; k++) svg('rect', { x: 640, y: 852 + k * 22, width: 120 + (k % 2) * 90, height: 10, rx: 5, fill: '#7f9ab8' }, mon);
  for (const [x, y, c, a] of [[592, 846, '#ffe66b', -6], [940, 870, '#ff9fc0', 8]]) svg('rect', { x, y, width: 52, height: 52, fill: c, stroke: INK, 'stroke-width': 3, transform: `rotate(${a} ${x + 26} ${y + 26})` }, mon);
  const glow = svg('ellipse', { cx: 790, cy: 960, rx: 420, ry: 300, fill: rad2(M.defs, [[0, '#bfe6ff', 0.45], [1, '#bfe6ff', 0]]) }, M.s);
  // desk
  svg('rect', { x: 360, y: 1176, width: 900, height: 34, rx: 8, fill: '#c9a87a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 380, y: 1206, width: 860, height: 220, fill: '#a98a62', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 640, y: 1158, width: 230, height: 20, rx: 6, fill: '#e9edf2', stroke: INK, 'stroke-width': 4 }, M.s);   // keyboard
  for (let k = 0; k < 8; k++) svg('rect', { x: 652 + k * 27, y: 1162, width: 20, height: 5, rx: 2, fill: '#b9c2cc' }, M.s);
  const mug = svg('g', { transform: 'translate(1020,1176)' }, M.s);
  svg('path', { d: 'M-24,-56 L24,-56 L20,0 L-20,0 Z', fill: '#e0574b', stroke: INK, 'stroke-width': 4 }, mug);
  svg('path', { d: 'M22,-44 q20,4 14,22 q-4,10 -16,8', fill: 'none', stroke: INK, 'stroke-width': 5 }, mug);
  const steam = [0, 1, 2].map(i => svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.5 }, mug));
  // desk lamp
  const lamp = svg('g', {}, M.s);
  svg('path', { d: 'M1150,1176 L1150,1160 M1150,1160 L1110,960 L1010,900', stroke: '#2e3446', 'stroke-width': 10, fill: 'none', 'stroke-linecap': 'round' }, lamp);
  svg('ellipse', { cx: 1150, cy: 1172, rx: 50, ry: 10, fill: '#2e3446' }, lamp);
  svg('path', { d: 'M960,880 L1050,890 L1030,950 Z', fill: '#f2c14e', stroke: INK, 'stroke-width': 4 }, lamp);
  svg('circle', { cx: 990, cy: 950, r: 160, fill: rad2(M.defs, [[0, '#ffe9b0', 0.4], [1, '#ffe9b0', 0]]) }, M.s);
  for (let k = 0; k < 4; k++) svg('rect', { x: 400, y: 1150 - k * 16, width: 160, height: 14, rx: 3, fill: ['#f2f0ea', '#9fc6ea', '#f2f0ea', '#f6c343'][k], stroke: INK, 'stroke-width': 3 }, M.s);
  // office chair (behind the daughter)
  const chair = svg('g', {}, M.s);
  svg('rect', { x: 236, y: 880, width: 70, height: 300, rx: 30, fill: '#3a3f52', stroke: INK, 'stroke-width': 5 }, chair);
  svg('rect', { x: 250, y: 1190, width: 190, height: 30, rx: 12, fill: '#3a3f52', stroke: INK, 'stroke-width': 5 }, chair);
  svg('rect', { x: 334, y: 1220, width: 16, height: 120, fill: '#5a6070' }, chair);
  svg('path', { d: 'M240,1350 L440,1350', stroke: '#5a6070', 'stroke-width': 12, 'stroke-linecap': 'round' }, chair);
  for (const wx of [250, 430]) svg('circle', { cx: wx, cy: 1368, r: 14, fill: '#2a2e3a' }, chair);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  const leaves = R ? [leafG(R, -120, 1880, 1.6, -60, '#1d3a2d'), leafG(R, -80, 1920, 1.5, -25, '#24473a')] : [];
  return {
    people, top, scr, glow,
    update(t) {
      lights.forEach(w => w.el.setAttribute('opacity', Math.sin((t + w.ph) * w.rate * 6) > -0.8 ? 0.85 : 0.2));
      bars.forEach((b, i) => { const h = 40 + 110 * (0.5 + 0.5 * Math.sin(t * 1.3 + i * 1.7)); setA(b, { y: (1060 - h).toFixed(1), height: h.toFixed(1) }); });
      steam.forEach((s, i) => { const k = ((t * 0.6 + i / 3) % 1); s.setAttribute('d', `M${-8 + i * 8},${-62 - k * 70} q10,-14 0,-28 q-10,-14 0,-28`); s.setAttribute('opacity', (0.5 * Math.sin(Math.PI * k)).toFixed(3)); });
      glow.setAttribute('opacity', (0.85 + 0.15 * Math.sin(t * 2.3)).toFixed(3));
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- the daughter's bedroom in the morning ----------------
function bedroomMorning(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1700, fill: lin(F.defs, [[0, '#cfe6dc'], [1, '#b6d6c8']]) }, F.s);
  for (let i = 0; i < 18; i++) svg('rect', { x: -300 + i * 100, y: -300, width: 50, height: 1700, fill: '#ffffff', opacity: 0.12 }, F.s);
  // window with morning sky
  svg('rect', { x: 600, y: 230, width: 400, height: 520, rx: 12, fill: '#f6efe2', stroke: INK, 'stroke-width': 6 }, F.s);
  svg('rect', { x: 618, y: 248, width: 364, height: 484, fill: lin(F.defs, [[0, '#9fd2f5'], [0.7, '#ffe3c2'], [1, '#ffd0a8']]) }, F.s);
  svg('circle', { cx: 900, cy: 600, r: 120, fill: rad2(F.defs, [[0, '#fffbe8', 0.9], [1, '#fffbe8', 0]]) }, F.s);
  for (let i = 0; i < 6; i++) svg('rect', { x: 630 + i * 60, y: 600 - (i % 3) * 50, width: 46, height: 140 + (i % 3) * 50, fill: '#c7d6e6' }, F.s);
  svg('rect', { x: 794, y: 248, width: 10, height: 484, fill: '#f6efe2' }, F.s);
  for (const cx of [560, 960]) svg('path', { d: `M${cx},210 Q${cx + 30},500 ${cx - 10},800 L${cx + 70},800 Q${cx + 90},500 ${cx + 80},210 Z`, fill: '#ffffff', opacity: 0.75 }, F.s);
  svg('rect', { x: 540, y: 200, width: 520, height: 14, rx: 7, fill: '#c9a87a' }, F.s);
  // fairy lights + photo of mom & daughter
  svg('path', { d: 'M40,180 Q300,260 560,190', fill: 'none', stroke: '#6a5a4a', 'stroke-width': 3 }, F.s);
  const bulbs = [];
  for (let k = 0; k < 9; k++) { const x = 60 + k * 60, y = 190 + Math.sin(k / 8 * Math.PI) * 52; bulbs.push(svg('circle', { cx: x, cy: y + 10, r: 9, fill: ['#ffd66b', '#ff9fc0', '#9fe0ff'][k % 3] }, F.s)); }
  svg('rect', { x: 200, y: 360, width: 230, height: 180, rx: 8, fill: '#f6efe2', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('rect', { x: 214, y: 374, width: 202, height: 152, fill: '#ffe2c6' }, F.s);
  faceFront3(F.s, 280, 452, 36, 'mom'); faceFront3(F.s, 356, 456, 34, 'daughter');
  // mid: bed, nightstand, floor
  woodFloor(M.s, M.defs, 1350, '#e9cfa8', '#c9a87a', '#b89466');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#c9a87a' }, M.s);
  rug(M.s, M.defs, 560, 1620, 420, 100, '#f2b6c4');
  const sunbeam = svg('path', { d: 'M620,250 L980,250 L1160,1600 L560,1600 Z', fill: lin(M.defs, [[0, '#fff3d6', 0.35], [1, '#fff3d6', 0]]) }, M.s);
  contactShadow(M.s, M.defs, 420, 1360, 420, 22, 0.35);
  svg('path', { d: 'M40,1160 L40,780 Q40,720 100,720 L300,720 Q360,720 360,780 L360,1160 Z', fill: '#d9a87a', stroke: INK, 'stroke-width': 6 }, M.s);   // headboard
  svg('rect', { x: 30, y: 1150, width: 800, height: 60, rx: 18, fill: '#ffffff', stroke: INK, 'stroke-width': 5 }, M.s);      // mattress
  svg('rect', { x: 30, y: 1200, width: 800, height: 140, rx: 10, fill: '#c9956a', stroke: INK, 'stroke-width': 5 }, M.s);     // bed frame
  for (const lx of [50, 800]) svg('rect', { x: lx, y: 1336, width: 20, height: 24, fill: '#8a6040' }, M.s);
  svg('rect', { x: 70, y: 1060, width: 190, height: 100, rx: 40, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, M.s);    // pillow
  // nightstand + alarm clock + lamp
  svg('rect', { x: 870, y: 1120, width: 170, height: 230, rx: 10, fill: '#e2c49a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 890, y: 1200, width: 130, height: 10, rx: 5, fill: '#b89466' }, M.s);
  const alarm = svg('g', { transform: 'translate(915,1120)' }, M.s);
  svg('circle', { cx: 0, cy: -34, r: 30, fill: '#ff8a7a', stroke: INK, 'stroke-width': 4 }, alarm);
  svg('circle', { cx: 0, cy: -34, r: 21, fill: '#fffaf0' }, alarm);
  const hands = svg('path', { stroke: INK, 'stroke-width': 3.5, 'stroke-linecap': 'round', fill: 'none' }, alarm);
  for (const sx of [-1, 1]) svg('circle', { cx: sx * 22, cy: -62, r: 9, fill: '#ff8a7a', stroke: INK, 'stroke-width': 3 }, alarm);
  svg('path', { d: 'M990,1120 L990,1040 M960,1040 L1020,1040 L1006,990 L974,990 Z', stroke: INK, 'stroke-width': 4, fill: '#ffe2a8' }, M.s);
  const people = svg('g', {}, M.s);
  // blanket over the legs (drawn above the daughter)
  const top = svg('g', {}, M.s);
  const blanket = svg('path', { fill: lin(M.defs, [[0, '#f7a8bb'], [1, '#e8869f']]), stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, top);
  const blanketDots = svg('g', {}, top);
  vignette(M.s, M.defs, 0.35);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#3a6b47'), leafG(R, 1150, 1960, 1.4, -150, '#4f8f56')] : [];
  return {
    people, top, sunbeam, alarm,
    blanket(hipX, kneeX) {
      // a puffy duvet from the waist to past the feet
      blanket.setAttribute('d', `M${hipX - 30},1190 Q${hipX - 20},1120 ${hipX + 60},1110 Q${(hipX + kneeX) / 2 + 80},1080 ${kneeX + 160},1110 Q${kneeX + 260},1120 820,1150 L828,1240 Q500,1270 ${hipX - 40},1236 Z`);
      blanketDots.innerHTML = '';
      for (let k = 0; k < 10; k++) svg('circle', { cx: hipX + 30 + k * 48, cy: 1170 + (k % 2) * 30, r: 7, fill: '#ffffff', opacity: 0.6 }, blanketDots);
    },
    update(t, hh = 6, mm = 0) {
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.6 + 0.4 * Math.sin(t * 2 + i)).toFixed(3)));
      const ha = (hh % 12 + mm / 60) * 30 - 90, ma = mm * 6 - 90;
      hands.setAttribute('d', `M0,-34 l${(Math.cos(rad(ha)) * 12).toFixed(1)},${(Math.sin(rad(ha)) * 12).toFixed(1)} M0,-34 l${(Math.cos(rad(ma)) * 17).toFixed(1)},${(Math.sin(rad(ma)) * 17).toFixed(1)}`);
      sunbeam.setAttribute('opacity', (0.8 + 0.2 * Math.sin(t * 0.8)).toFixed(3));
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- Mom's room, the morning she is sick ----------------
function momRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const tones = ['#9a6c48', '#8e6342', '#a4744e', '#946846'];
  for (let i = -3; i < 16; i++) {
    svg('rect', { x: i * 84, y: -300, width: 84, height: 2200, fill: tones[(i + 12) % 4] }, F.s);
    svg('rect', { x: i * 84, y: -300, width: 3, height: 2200, fill: '#6a4428', opacity: 0.6 }, F.s);
  }
  // window with soft morning light
  svg('rect', { x: 700, y: 220, width: 280, height: 360, rx: 6, fill: '#5a3a22', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('rect', { x: 714, y: 234, width: 252, height: 332, fill: lin(F.defs, [[0, '#cfe7f7'], [1, '#ffe7c6']]) }, F.s);
  svg('rect', { x: 836, y: 234, width: 8, height: 332, fill: '#5a3a22' }, F.s);
  svg('rect', { x: 714, y: 396, width: 252, height: 8, fill: '#5a3a22' }, F.s);
  svg('rect', { x: -300, y: -300, width: 1680, height: 2200, fill: lin(F.defs, [[0, '#1a0e14', 0.3], [0.6, '#1a0e14', 0.05], [1, '#1a0e14', 0.25]]) }, F.s);
  woodFloor(M.s, M.defs, 1380, '#8a5d3c', '#5a3b24', '#4d321e');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#5a3b24' }, M.s);
  // graduation photo of the daughter + small altar shelf
  const photoGlow = svg('circle', { cx: 230, cy: 560, r: 200, fill: rad2(M.defs, [[0, '#ffe2a8', 0.5], [1, '#ffe2a8', 0]]), opacity: 0 }, M.s);
  svg('rect', { x: 120, y: 420, width: 220, height: 270, rx: 8, fill: '#3a2a1e', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('rect', { x: 136, y: 436, width: 188, height: 238, fill: lin(M.defs, [[0, '#c7d4e2'], [1, '#a9bccf']]) }, M.s);
  svg('path', { d: 'M164,674 C166,606 294,606 296,674 Z', fill: '#1d1d24' }, M.s);
  faceFront3(M.s, 230, 566, 40, 'daughter');
  svg('path', { d: 'M178,520 L230,500 L282,520 L230,540 Z', fill: '#1d1d24' }, M.s);
  svg('path', { d: 'M204,620 C214,650 246,650 256,620', fill: 'none', stroke: '#f5d76e', 'stroke-width': 9, 'stroke-linecap': 'round' }, M.s);
  // wall calendar
  svg('rect', { x: 430, y: 460, width: 180, height: 220, rx: 8, fill: '#f6f1e6', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('path', { d: 'M430,468 Q430,460 438,460 L602,460 Q610,460 610,468 L610,500 L430,500 Z', fill: '#5cbf6a' }, M.s);
  for (let i = 0; i < 20; i++) svg('rect', { x: 444 + (i % 5) * 32, y: 516 + Math.floor(i / 5) * 38, width: 20, height: 20, rx: 4, fill: '#d9d2c4' }, M.s);
  // light beam from the window
  const beam = svg('path', { d: 'M714,234 L966,234 L1180,1700 L520,1700 Z', fill: lin(M.defs, [[0, '#fff3d6', 0.3], [1, '#fff3d6', 0]]) }, M.s);
  // floor mattress, pillow, tray with medicine and water
  contactShadow(M.s, M.defs, 520, 1450, 470, 22, 0.4);
  svg('rect', { x: 90, y: 1376, width: 860, height: 74, rx: 22, fill: '#f0e2c4', stroke: INK, 'stroke-width': 5 }, M.s);
  for (let k = 0; k < 8; k++) svg('rect', { x: 120 + k * 104, y: 1380, width: 44, height: 66, fill: '#e4b86a', opacity: 0.5 }, M.s);
  svg('rect', { x: 110, y: 1300, width: 210, height: 86, rx: 38, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, M.s);
  const tray = svg('g', { transform: 'translate(980,1450)' }, M.s);
  svg('rect', { x: -10, y: -12, width: 150, height: 14, rx: 6, fill: '#a87a50', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: 0, y: -70, width: 38, height: 58, rx: 8, fill: '#ffffff', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: 4, y: -46, width: 30, height: 30, fill: '#9fd2f5', opacity: 0.7 }, tray);
  svg('rect', { x: 60, y: -64, width: 30, height: 52, rx: 6, fill: '#e8a04a', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: 58, y: -76, width: 34, height: 14, rx: 4, fill: '#ffffff', stroke: INK, 'stroke-width': 3 }, tray);
  svg('rect', { x: 100, y: -30, width: 46, height: 10, rx: 5, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3 }, tray);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  const dust = floaters(M.s, [600, 300, 500, 900], 16, 39, { color: '#fff2d0', rMin: 1.2, rMax: 3, speed: 6, op: 0.5, base: 0.1 });
  const leaves = R ? [leafG(R, -120, 1900, 1.6, -60, '#2a4a34'), leafG(R, -80, 1960, 1.5, -25, '#335a3e')] : [];
  return {
    people, top, photoGlow,
    update(t) {
      beam.setAttribute('opacity', (0.85 + 0.15 * Math.sin(t * 0.7)).toFixed(3));
      dust(t);
      swayLeaves(leaves, t);
    },
  };
}
