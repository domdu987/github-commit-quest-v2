// "75 วันของพ่อ" sets: son's room at night, construction site at noon, Dad's wooden house at night.

// ---------------- son's room (night), same language as the condo in 355 วัน ----------------
function sonRoomNight(S, warm = 0) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#3f3a5a'], [1, '#544a6a']]) }, F.s);
  svg('rect', { x: 120, y: 200, width: 470, height: 560, rx: 8, fill: '#2a2236' }, F.s);
  svg('rect', { x: 136, y: 216, width: 438, height: 528, fill: lin(F.defs, [[0, '#141636'], [1, '#2b2c5a']]) }, F.s);
  const r = rng(31);
  for (let i = 0; i < 50; i++) svg('circle', { cx: 140 + r() * 430, cy: 222 + r() * 260, r: 1 + r() * 1.8, fill: '#fff', opacity: 0.3 + r() * 0.5 }, F.s);
  svg('circle', { cx: 470, cy: 300, r: 60, fill: rad2(F.defs, [[0, '#fff6dc', 0.5], [1, '#fff6dc', 0]]) }, F.s);
  svg('circle', { cx: 470, cy: 300, r: 30, fill: '#f6eed8' }, F.s);
  const twinkles = [];
  let bx = 136;
  while (bx < 574) {
    const bw = Math.min(40 + r() * 54, 574 - bx), bh = 140 + r() * 240, by = 744 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: r() > 0.5 ? '#22244a' : '#2a2c55' }, F.s);
    for (let wy = by + 14; wy < 734; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14)
      if (r() > 0.55) twinkles.push({ el: svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#f6c86a' }, F.s), ph: r() * 40, rate: 0.2 + r() * 0.5 });
    bx += bw + 3;
  }
  svg('rect', { x: 352, y: 216, width: 6, height: 528, fill: '#2a2236' }, F.s);
  for (const cx of [86, 566]) {
    svg('rect', { x: cx, y: 180, width: 86, height: 640, rx: 16, fill: lin(F.defs, [[0, '#5d6a8a'], [1, '#4b5776']], 1, 0) }, F.s);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: 190, width: 7, height: 620, rx: 3, fill: '#4a5572' }, F.s);
  }
  svg('rect', { x: 70, y: 172, width: 600, height: 12, rx: 6, fill: '#2f2a40' }, F.s);
  // wall: guitar + poster
  svg('rect', { x: 760, y: 300, width: 170, height: 230, rx: 6, fill: '#2b2f4f' }, F.s);
  svg('circle', { cx: 845, cy: 390, r: 46, fill: '#e0574b', opacity: 0.85 }, F.s);
  svg('path', { d: 'M800,470 L890,470', stroke: '#f2c14e', 'stroke-width': 8 }, F.s);
  woodFloor(M.s, M.defs, 1330, '#3a3448', '#221d2c', '#2a2130');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#221d2c' }, M.s);
  rug(M.s, M.defs, 540, 1560, 470, 110, '#41506a');
  svg('path', { d: 'M150,230 L560,230 L980,1560 L240,1560 Z', fill: lin(M.defs, [[0, '#c9d6ff', 0.14], [1, '#c9d6ff', 0.0]]) }, M.s);
  floorLamp(M.s, M.defs, 960, 1330, warm ? '#ffcf8a' : '#ffd59a', 0.55 + 0.2 * warm);
  svg('circle', { cx: 960, cy: 820, r: 120, fill: rad2(M.defs, [[0, '#fff2d0', 0.7], [1, '#fff2d0', 0]]) }, M.s);
  contactShadow(M.s, M.defs, 520, 1338, 470, 26, 0.45);
  sofa(M.s, M.defs, 170, 1140, 700, -6);
  contactShadow(M.s, M.defs, 420, 1328, 120, 14, 0.4);
  const leaves = [leafG(R, -120, 1880, 1.6, -60, '#1d3a2d'), leafG(R, -80, 1900, 1.5, -25, '#24473a'), leafG(R, -160, 1700, 1.4, -5, '#2b5243'), leafG(R, -60, 1960, 1.3, -88, '#1a3328')];
  svg('circle', { cx: 1040, cy: 200, r: 90, fill: '#ffcf8a', opacity: 0.25 }, R.s);
  return {
    update(t) {
      twinkles.forEach(w => w.el.setAttribute('opacity', (Math.sin((t + w.ph) * w.rate * 6) > -0.85 ? 0.85 : 0.15)));
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- construction site at noon: crane, frame, scaffolding, heat haze ----------------
function constructionSite(S, G = 1640) {
  const K = S.L.sky, F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -400, y: -400, width: 1880, height: 2000, fill: lin(K.defs, [[0, '#4fa9e8'], [0.45, '#9fd4f5'], [0.75, '#e4f2f6'], [1, '#fbf1d6']]) }, K.s);
  const sunG = svg('g', { transform: 'translate(850,300)' }, K.s);
  svg('circle', { r: 560, fill: rad2(K.defs, [[0, '#fff6d0', 0.85], [0.3, '#fff0b8', 0.35], [1, '#fff0b8', 0]]) }, sunG);
  const rays = svg('g', {}, sunG);
  for (let i = 0; i < 12; i++) svg('path', { d: 'M-14,-90 L14,-90 L5,-330 L-5,-330 Z', fill: '#fffbe8', opacity: 0.35, transform: `rotate(${i * 30})` }, rays);
  svg('circle', { r: 74, fill: '#fffdf2' }, sunG);
  svg('circle', { r: 110, fill: rad2(K.defs, [[0, '#ffffff', 0.8], [1, '#ffffff', 0]]) }, sunG);
  // far: hazy skyline + tower crane with swinging load
  for (let i = 0; i < 9; i++) svg('rect', { x: -200 + i * 170, y: 1020 - (i % 3) * 90 - (i % 2) * 40, width: 120 + (i % 2) * 40, height: 520, fill: '#c3d6e4', opacity: 0.85 }, F.s);
  const crane = svg('g', {}, F.s);
  const lat = (x0, y0, x1, y1, w) => { svg('rect', { x: x0, y: y0, width: x1 - x0 || w, height: y1 - y0 || w, fill: 'none', stroke: '#e8a92c', 'stroke-width': 6 }, crane); };
  svg('rect', { x: 150, y: 330, width: 34, height: 960, fill: 'none', stroke: '#e8a92c', 'stroke-width': 6 }, crane);
  for (let y = 340; y < 1280; y += 34) svg('path', { d: `M150,${y} L184,${y + 34}`, stroke: '#e8a92c', 'stroke-width': 4 }, crane);
  svg('rect', { x: -60, y: 300, width: 1000, height: 30, fill: 'none', stroke: '#e8a92c', 'stroke-width': 6 }, crane);
  for (let x = -60; x < 940; x += 34) svg('path', { d: `M${x},300 L${x + 34},330`, stroke: '#e8a92c', 'stroke-width': 4 }, crane);
  svg('path', { d: 'M167,300 L167,200 L940,300 M167,200 L-60,300', stroke: '#e8a92c', 'stroke-width': 5, fill: 'none' }, crane);
  svg('rect', { x: 130, y: 330, width: 74, height: 50, rx: 6, fill: '#f2c14e' }, crane);
  svg('rect', { x: -60, y: 330, width: 90, height: 70, fill: '#8a8f99' }, crane);
  const load = svg('g', {}, F.s);
  svg('path', { d: 'M0,0 L0,300', stroke: '#5a5f6a', 'stroke-width': 3 }, load);
  svg('path', { d: 'M-50,300 L50,300 L40,330 L-40,330 Z', fill: '#9a6a44' }, load);
  for (let k = 0; k < 4; k++) svg('rect', { x: -60, y: 306 + k * 6, width: 120, height: 4, rx: 2, fill: '#6b6f78' }, load);
  // mid: building frame with slabs, scaffolding, safety net, workers
  const B = svg('g', {}, M.s);
  for (const y of [560, 780, 1000, 1220]) svg('rect', { x: 520, y, width: 700, height: 26, fill: '#b9b4ab' }, B);
  for (const x of [540, 720, 900, 1080]) svg('rect', { x, y: 560, width: 34, height: 900, fill: '#c9c4ba' }, B);
  for (const x of [540, 720, 900, 1080]) svg('rect', { x, y: 560, width: 10, height: 900, fill: '#e6e1d6', opacity: 0.7 }, B);
  svg('rect', { x: 560, y: 586, width: 640, height: 194, fill: '#4f8a5b', opacity: 0.35 }, B);
  const scaf = svg('g', {}, M.s);
  for (let i = 0; i < 6; i++) svg('rect', { x: 470 + i * 120, y: 520, width: 9, height: 950, fill: '#c99a5a' }, scaf);
  for (let j = 0; j < 9; j++) svg('rect', { x: 460, y: 540 + j * 110, width: 640, height: 7, fill: '#b98a4f' }, scaf);
  for (let i = 0; i < 5; i++) svg('path', { d: `M${474 + i * 120},${560 + (i % 2) * 220} L${594 + i * 120},${780 + (i % 2) * 220}`, stroke: '#b98a4f', 'stroke-width': 6 }, scaf);
  const workers = [[640, 781, 0.55, 1], [980, 1001, 0.53, -1], [800, 1221, 0.55, 1]].map(([x, y, s, f], i) => {
    const q = new Puppet(M.s, { skin: '#8a5f45', skinShade: '#74503a', hair: '#2a2220', hairStyle: 'dad', shirt: ['#5e7fa6', '#7a8f6a', '#9a6f5a'][i], shirtLight: '#7d97b8', shirtDark: '#4e6a8c', sleeve: 'long', top: 'work', vest: i === 1 ? null : '#f39a3a', pants: '#5a5048', pantsDark: '#4a423b', shoe: '#3a2f28', shoeDark: '#2e2520', sole: '#2a2520', hat: 'hardhat', flat: true, ink: '#3b3236', seed: 10 + i }, M.defs);
    return { q, x, y, s, f, ph: i * 1.7 };
  });
  // ground, sand pile, cement bag stack, wheelbarrow, rebar
  svg('rect', { x: -400, y: 1440, width: 1880, height: 900, fill: lin(M.defs, [[0, '#dcc59c'], [0.5, '#c7aa7c'], [1, '#9e8058']]) }, M.s);
  const rr = rng(8);
  for (let i = 0; i < 50; i++) svg('ellipse', { cx: -200 + rr() * 1500, cy: 1460 + rr() * 500, rx: 3 + rr() * 7, ry: 2 + rr() * 3, fill: '#a98a62', opacity: 0.5 }, M.s);
  svg('path', { d: 'M-120,1520 Q60,1330 260,1520 Z', fill: lin(M.defs, [[0, '#ecd29a'], [1, '#d4b47a']]) }, M.s);
  const bagStack = svg('g', {}, M.s);
  [[720, 1420], [830, 1420], [940, 1420], [775, 1370], [885, 1370], [830, 1320]].forEach(([x, y]) => cementBag(bagStack, M.defs, x, y, 1));
  const wb = svg('g', { transform: 'translate(300,1500)' }, M.s);
  svg('path', { d: 'M-70,-60 L60,-60 L40,0 L-50,0 Z', fill: '#3f8f5b', stroke: '#2e6e44', 'stroke-width': 4 }, wb);
  svg('circle', { cx: 50, cy: 14, r: 18, fill: '#2a2733' }, wb);
  svg('path', { d: 'M-50,0 L-110,-10 M-40,-4 L-30,30', stroke: '#6b6f78', 'stroke-width': 7, 'stroke-linecap': 'round' }, wb);
  svg('path', { d: 'M-60,-62 Q-5,-90 55,-62', fill: '#bdb5a5' }, wb);
  // fore: rebar bundle and traffic cone (blurred by layer)
  const fg = svg('g', {}, R.s);
  for (let i = 0; i < 6; i++) svg('path', { d: `M-150,${1980 - i * 12} L640,${1720 - i * 12}`, stroke: '#7a5340', 'stroke-width': 10, 'stroke-linecap': 'round' }, fg);
  svg('path', { d: 'M960,1960 L1010,1740 L1060,1960 Z', fill: '#f07a2b' }, fg);
  svg('rect', { x: 975, y: 1820, width: 70, height: 26, fill: '#fff' }, fg);
  vignette(M.s, M.defs, 0.25);
  return {
    G,
    update(t) {
      rays.setAttribute('transform', `rotate(${(t * 4).toFixed(2)})`);
      load.setAttribute('transform', `translate(700,330) rotate(${(Math.sin(t * 1.1) * 4).toFixed(2)})`);
      workers.forEach(w => w.q.pose({ x: w.x + Math.sin(t * 0.8 + w.ph) * 20, y: w.y, s: w.s, f: w.f, torso: 10 + Math.sin(t * 3 + w.ph) * 6, aF: [40 + Math.sin(t * 3 + w.ph) * 20, 20], aB: [70, 50], lF: [86, 90], lB: [94, 92] }));
    },
  };
}
// a paper cement bag (side view), origin at its bottom-left
function cementBag(g, defs, x, y, s = 1) {
  const b = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('path', { d: 'M0,0 Q-4,-24 6,-46 L100,-46 Q110,-24 104,0 Z', fill: lin(defs, [[0, '#ece6d8'], [1, '#d3cab6']]), stroke: '#b9ae98', 'stroke-width': 3 }, b);
  svg('rect', { x: 14, y: -34, width: 76, height: 10, fill: '#cf483d', opacity: 0.85 }, b);
  svg('circle', { cx: 52, cy: -15, r: 7, fill: '#2e5aa8', opacity: 0.8 }, b);
  return b;
}

// ---------------- Dad's wooden house at night: bench, photo of his son, fan, swinging bulb ----------------
function dadRoom(S, withFore = true) {
  const F = S.L.far, M = S.L.mid;
  const tones = ['#7f5a3e', '#755236', '#866044', '#7b583b'];
  for (let i = -3; i < 16; i++) {
    svg('rect', { x: i * 84, y: -300, width: 84, height: 2200, fill: tones[(i + 12) % 4] }, F.s);
    svg('rect', { x: i * 84, y: -300, width: 3, height: 2200, fill: '#5a3c25', opacity: 0.6 }, F.s);
  }
  svg('rect', { x: 770, y: 230, width: 250, height: 330, rx: 6, fill: '#4b3220' }, F.s);
  svg('rect', { x: 784, y: 244, width: 222, height: 302, fill: lin(F.defs, [[0, '#141636'], [1, '#2c2d5a']]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 120, fill: rad2(F.defs, [[0, '#fff3d6', 0.5], [1, '#fff3d6', 0]]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 26, fill: '#f6eed8' }, F.s);
  const flies = floaters(F.s, [790, 400, 210, 140], 8, 63, { color: '#fff59a', rMin: 2, rMax: 4, speed: 6, amp: 14, op: 0.9, base: 0.0, twinkle: 3, filter: blurFilter(F.defs, 1.2) });
  svg('rect', { x: 892, y: 244, width: 6, height: 302, fill: '#4b3220' }, F.s);
  svg('rect', { x: 784, y: 392, width: 222, height: 6, fill: '#4b3220' }, F.s);
  svg('rect', { x: -300, y: -300, width: 1680, height: 1680, fill: lin(F.defs, [[0, '#140a18', 0.45], [0.55, '#140a18', 0.05], [1, '#140a18', 0.3]]) }, F.s);
  woodFloor(M.s, M.defs, 1380, '#664530', '#3d2716', '#382313');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#3d2716' }, M.s);
  // graduation photo of the son
  const photoGlow = svg('circle', { cx: 190, cy: 640, r: 200, fill: rad2(M.defs, [[0, '#ffe2a8', 0.5], [1, '#ffe2a8', 0]]), opacity: 0 }, M.s);
  svg('rect', { x: 80, y: 500, width: 220, height: 270, rx: 8, fill: '#3a2a1e' }, M.s);
  svg('rect', { x: 96, y: 516, width: 188, height: 238, fill: lin(M.defs, [[0, '#c7d4e2'], [1, '#a9bccf']]) }, M.s);
  svg('path', { d: 'M124,754 C126,682 254,682 256,754 Z', fill: '#1d1d24' }, M.s);
  svg('path', { d: 'M164,700 C174,740 206,740 216,700', fill: 'none', stroke: '#f5d76e', 'stroke-width': 10, 'stroke-linecap': 'round' }, M.s);
  faceFront2(M.s, 190, 648, 40, 'son');
  svg('path', { d: 'M134,594 L190,572 L246,594 L190,614 Z', fill: '#1d1d24' }, M.s);
  svg('path', { d: 'M236,596 L244,642', stroke: '#f5d76e', 'stroke-width': 4 }, M.s);
  // wall calendar (no crosses here) and a small shelf radio
  svg('rect', { x: 400, y: 520, width: 200, height: 250, rx: 8, fill: '#f6f1e6' }, M.s);
  svg('path', { d: 'M400,528 Q400,520 408,520 L592,520 Q600,520 600,528 L600,566 L400,566 Z', fill: '#cf483d' }, M.s);
  for (let i = 0; i < 20; i++) svg('rect', { x: 416 + (i % 5) * 36, y: 588 + Math.floor(i / 5) * 42, width: 22, height: 22, rx: 4, fill: '#d9d2c4' }, M.s);
  // fan with spinning blades
  const fan = svg('g', { transform: 'translate(930,1250)' }, M.s);
  svg('path', { d: 'M-8,0 L-14,140 L14,140 L8,0 Z', fill: '#d9d6e6' }, fan);
  svg('ellipse', { cx: 0, cy: 146, rx: 50, ry: 12, fill: '#cfcbd9' }, fan);
  svg('circle', { r: 64, fill: 'none', stroke: '#e6e3ee', 'stroke-width': 4 }, fan);
  const blades = svg('g', {}, fan);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 0, cy: -32, rx: 15, ry: 32, fill: '#7cc8f0', opacity: 0.75, transform: `rotate(${k * 120})` }, blades);
  svg('circle', { r: 10, fill: '#4a7bd8' }, fan);
  // bamboo bench (แคร่)
  svg('ellipse', { cx: 520, cy: 1430, rx: 330, ry: 22, fill: '#000', opacity: 0.3 }, M.s);
  for (const lx of [240, 790]) svg('rect', { x: lx, y: 1270, width: 18, height: 160, fill: '#8a6a3a' }, M.s);
  svg('rect', { x: 220, y: 1250, width: 600, height: 26, rx: 8, fill: '#c9a46a' }, M.s);
  for (let i = 0; i < 12; i++) svg('rect', { x: 226 + i * 49, y: 1252, width: 3, height: 22, fill: '#a5824c' }, M.s);
  // bulb + pool + Dad's wall shadow slot
  const bulbG = svg('g', {}, M.s);
  svg('rect', { x: -2.5, y: 0, width: 5, height: 150, fill: '#2a1d14' }, bulbG);
  svg('circle', { cx: 0, cy: 168, r: 22, fill: '#ffe4ad' }, bulbG);
  svg('circle', { cx: 0, cy: 168, r: 70, fill: rad2(M.defs, [[0, '#fff2c8', 0.8], [1, '#fff2c8', 0]]) }, bulbG);
  const pool = svg('circle', { r: 900, fill: rad2(M.defs, [[0, '#ffd9a0', 0.4], [0.5, '#ffd9a0', 0.12], [1, '#ffd9a0', 0]]) }, M.s);
  const people = svg('g', {}, M.s);
  const dust = floaters(M.s, [300, 200, 600, 700], 20, 39, { color: '#ffe9c4', rMin: 1.2, rMax: 3.2, speed: 8, op: 0.45, base: 0.1 });
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  let cloth = null;
  if (withFore) {
    const R = S.L.fore;
    svg('path', { d: 'M-200,40 Q300,120 900,30', fill: 'none', stroke: '#2b1d12', 'stroke-width': 6 }, R.s);
    cloth = svg('g', { transform: 'translate(-90,60)' }, R.s);
    const id = uidS('plaid');
    const pat = svg('pattern', { id, width: 60, height: 60, patternUnits: 'userSpaceOnUse' }, R.defs);
    svg('rect', { width: 60, height: 60, fill: '#2f6a74' }, pat);
    svg('rect', { x: 0, y: 0, width: 30, height: 60, fill: '#c23b3b', opacity: 0.7 }, pat);
    svg('rect', { x: 0, y: 0, width: 60, height: 30, fill: '#ffffff', opacity: 0.3 }, pat);
    svg('path', { d: 'M0,0 L210,10 L200,560 Q100,600 10,560 Z', fill: `url(#${id})` }, cloth);
  }
  return {
    people, top, photoGlow,
    update(t) {
      const ang = Math.sin(t * 1.7) * 5;
      const bx = 520 + Math.sin(rad(ang)) * 168, by = Math.cos(rad(ang)) * 168;
      bulbG.setAttribute('transform', `translate(520,0) rotate(${(-ang).toFixed(2)})`);
      setA(pool, { cx: bx.toFixed(1), cy: (by + 200).toFixed(1) });
      blades.setAttribute('transform', `rotate(${((t * 900) % 360).toFixed(1)})`);
      flies(t); dust(t + 2);
      if (cloth) cloth.setAttribute('transform', `translate(-90,60) skewX(${(Math.sin(t * 1.1) * 2.5).toFixed(2)})`);
    },
  };
}
