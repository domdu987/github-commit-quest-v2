// "127 ใบสมัคร" sets: his rented room (night / morning / dark), a packed skytrain car, his balcony over the city at night,
// and mom's wooden house up-country.

const leafG = (R, x, y, s, a, c, vein = '#3e3448') => {
  const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
  svg('path', { d: 'M0,0 C40,-60 120,-70 200,-20 C120,10 50,20 0,0 Z', fill: c }, g);
  svg('path', { d: 'M8,-2 C70,-30 130,-34 190,-20', fill: 'none', stroke: vein, 'stroke-width': 3, opacity: 0.5 }, g);
  return g;
};
const swayLeaves = (leaves, t) => leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });

// city block silhouettes with lit windows, drawn into g between x0..x1 standing on y
function cityBlocks(g, x0, x1, y, seed, o = {}) {
  const r = rng(seed), lit = [];
  const cols = o.cols || ['#1d2348', '#252b55', '#2b3160'], win = o.win || '#f6c86a', hMin = o.hMin || 120, hMax = o.hMax || 420;
  let bx = x0;
  while (bx < x1) {
    const bw = 60 + r() * 110, bh = hMin + r() * (hMax - hMin);
    svg('rect', { x: bx, y: y - bh, width: bw, height: bh + 4, fill: cols[Math.floor(r() * cols.length)] }, g);
    if (r() > 0.6) svg('rect', { x: bx + bw * 0.4, y: y - bh - 30, width: 4, height: 30, fill: cols[0] }, g);
    for (let wy = y - bh + 14; wy < y - 16; wy += 26) for (let wx = bx + 8; wx < bx + bw - 12; wx += 18)
      if (r() > (o.dens || 0.55)) lit.push(svg('rect', { x: wx, y: wy, width: 8, height: 12, fill: win, opacity: 0.85 }, g));
    bx += bw + 4;
  }
  return lit;
}

// the graduation photo on the wall: him in gown and cap, gold frame
function gradPhoto(g, x, y, w = 190) {
  const h = w * 1.25;
  svg('rect', { x, y, width: w, height: h, rx: 6, fill: '#c9a24a', stroke: INK, 'stroke-width': 5 }, g);
  svg('rect', { x: x + 12, y: y + 12, width: w - 24, height: h - 24, fill: '#b7cde4' }, g);
  const cx = x + w / 2, cy = y + h * 0.48, r = w * 0.2;
  svg('path', { d: `M${cx - w * 0.36},${y + h - 12} C${cx - w * 0.34},${cy + r * 1.3} ${cx + w * 0.34},${cy + r * 1.3} ${cx + w * 0.36},${y + h - 12} Z`, fill: '#1d1d24' }, g);
  svg('path', { d: `M${cx - r * 0.5},${cy + r * 1.2} L${cx},${cy + r * 1.9} L${cx + r * 0.5},${cy + r * 1.2}`, fill: 'none', stroke: '#f5d76e', 'stroke-width': 5 }, g);
  faceFront5(g, cx, cy, r, 'grad', { smile: 0.9 });
  svg('path', { d: `M${cx - r * 1.4},${cy - r * 1.1} L${cx},${cy - r * 1.6} L${cx + r * 1.4},${cy - r * 1.1} L${cx},${cy - r * 0.6} Z`, fill: '#1d1d24', stroke: INK, 'stroke-width': 2 }, g);
  svg('path', { d: `M${cx + r * 0.9},${cy - r * 1.2} L${cx + r * 1.2},${cy - r * 0.2}`, stroke: '#f5d76e', 'stroke-width': 4 }, g);
  return { cx, cy };
}

// ---------------- his rented room, in the story2 condo language: 'night' (lamp + laptop glow), 'day' (morning sun), 'dark' (lamp off) ----------------
function rentRoom(S, mode = 'night') {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const night = mode !== 'day', dark = mode === 'dark';
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, night ? [[0, '#3f3a5a'], [1, '#544a6a']] : [[0, '#e3d6c3'], [1, '#cfbfa8']]) }, F.s);
  // big window with curtains: night city + moon, or a hazy morning sky
  const wx = 580, wy = 190, ww = 420, wh = 470;
  svg('rect', { x: wx, y: wy, width: ww, height: wh, rx: 8, fill: night ? '#2a2236' : '#bfae98' }, F.s);
  svg('rect', { x: wx + 16, y: wy + 16, width: ww - 32, height: wh - 32, fill: lin(F.defs, night ? [[0, '#141636'], [1, '#2b2c5a']] : [[0, '#8fc3ea'], [0.7, '#cfe6f6'], [1, '#f4efe2']]) }, F.s);
  const r = rng(37), twinkles = [];
  if (night) {
    for (let i = 0; i < 40; i++) svg('circle', { cx: wx + 22 + r() * (ww - 44), cy: wy + 22 + r() * 220, r: 1 + r() * 1.8, fill: '#fff', opacity: 0.3 + r() * 0.5 }, F.s);
    svg('circle', { cx: wx + ww * 0.72, cy: wy + 100, r: 60, fill: rad2(F.defs, [[0, '#fff6dc', 0.5], [1, '#fff6dc', 0]]) }, F.s);
    svg('circle', { cx: wx + ww * 0.72, cy: wy + 100, r: 30, fill: '#f6eed8' }, F.s);
  } else {
    svg('circle', { cx: wx + 90, cy: wy + 90, r: 150, fill: rad2(F.defs, [[0, '#fffbe8', 0.95], [0.25, '#fff4cf', 0.6], [1, '#fff4cf', 0]]) }, F.s);
    for (let i = 0; i < 3; i++) svg('ellipse', { cx: wx + 170 + i * 100, cy: wy + 120 + (i % 2) * 40, rx: 60, ry: 16, fill: '#ffffff', opacity: 0.7 }, F.s);
  }
  let bx = wx + 16;
  while (bx < wx + ww - 16) {
    const bw = Math.min(40 + r() * 54, wx + ww - 16 - bx), bh = 120 + r() * 200, by = wy + wh - 16 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: night ? (r() > 0.5 ? '#22244a' : '#2a2c55') : (r() > 0.5 ? '#9fb3c8' : '#b4c4d4') }, F.s);
    for (let wy2 = by + 14; wy2 < wy + wh - 26; wy2 += 24) for (let wx2 = bx + 6; wx2 < bx + bw - 8; wx2 += 14)
      if (r() > 0.55) {
        const el = svg('rect', { x: wx2, y: wy2, width: 6, height: 9, fill: night ? '#f6c86a' : '#e8f1f8', opacity: night ? 1 : 0.8 }, F.s);
        if (night) twinkles.push({ el, ph: r() * 40, rate: 0.2 + r() * 0.5 });
      }
    bx += bw + 3;
  }
  svg('rect', { x: wx + ww / 2 - 3, y: wy + 16, width: 6, height: wh - 32, fill: night ? '#2a2236' : '#bfae98' }, F.s);
  for (const cx of [wx - 34, wx + ww - 52]) {
    svg('rect', { x: cx, y: wy - 10, width: 86, height: wh + 90, rx: 16, fill: lin(F.defs, night ? [[0, '#5d6a8a'], [1, '#4b5776']] : [[0, '#f4ecdf'], [1, '#e4d8c6']], 1, 0) }, F.s);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: wy, width: 7, height: wh + 70, rx: 3, fill: night ? '#4a5572' : '#ddd0bc' }, F.s);
  }
  svg('rect', { x: wx - 50, y: wy - 18, width: ww + 100, height: 12, rx: 6, fill: night ? '#2f2a40' : '#a8927a' }, F.s);
  // wall: graduation photo, the interview shirt on its hanger, a calendar crossed off day by day
  gradPhoto(F.s, 90, 300, 190);
  svg('circle', { cx: 400, cy: 300, r: 7, fill: '#8a8f99', stroke: INK, 'stroke-width': 3 }, F.s);
  const hang = svg('g', { transform: 'translate(400,300)' }, F.s);
  svg('path', { d: 'M0,4 L0,22 M-70,62 L0,22 L70,62 Z', fill: 'none', stroke: '#8a8f99', 'stroke-width': 5, 'stroke-linejoin': 'round' }, hang);
  svg('path', { d: 'M-68,60 L-92,110 L-74,124 L-60,104 L-58,250 L58,250 L60,104 L74,124 L92,110 L68,60 L20,52 L0,74 L-20,52 Z', fill: '#f7f7f2', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, hang);
  svg('path', { d: 'M-6,74 L6,74 L10,170 L0,184 L-10,170 Z', fill: '#2c3e7a', stroke: INK, 'stroke-width': 3.5 }, hang);
  const cal = svg('g', { transform: 'translate(170,700)' }, F.s);
  svg('rect', { x: 0, y: 0, width: 150, height: 180, rx: 8, fill: '#f6f1e6', stroke: INK, 'stroke-width': 4 }, cal);
  svg('path', { d: 'M0,8 Q0,0 8,0 L142,0 Q150,0 150,8 L150,34 L0,34 Z', fill: '#e0574b' }, cal);
  for (let i = 0; i < 20; i++) {
    const cx = 14 + (i % 5) * 26, cy = 46 + Math.floor(i / 5) * 32;
    svg('rect', { x: cx, y: cy, width: 18, height: 18, rx: 3, fill: '#d9d2c4' }, cal);
    if (i < 17) svg('path', { d: `M${cx + 2},${cy + 2} L${cx + 16},${cy + 16} M${cx + 16},${cy + 2} L${cx + 2},${cy + 16}`, stroke: '#e0574b', 'stroke-width': 3 }, cal);
  }
  if (night) svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: '#120e1e', opacity: dark ? 0.35 : 0.08 }, F.s);
  // floor: warm wood planks + rug, like the condo in story2
  const fc = night ? ['#3a3448', '#221d2c', '#2a2130'] : ['#c9a27a', '#a87f58', '#8f6a48'];
  svg('rect', { x: -300, y: 1300, width: 1680, height: 1000, fill: fc[1] }, M.s);
  woodFloor(M.s, M.defs, 1300, ...fc);
  rug(M.s, M.defs, 470, 1480, 420, 84, night ? '#41506a' : '#d98a7a');
  if (night) svg('path', { d: `M${wx + 16},${wy + 16} L${wx + ww - 16},${wy + 16} L${wx + ww + 200},1560 L${wx - 260},1560 Z`, fill: lin(M.defs, [[0, '#c9d6ff', dark ? 0.08 : 0.14], [1, '#c9d6ff', 0]]) }, M.s);
  else svg('path', { d: `M${wx + 16},${wy + 16} L${wx + ww - 16},${wy + 16} L${wx + ww + 160},1560 L${wx - 300},1560 Z`, fill: lin(M.defs, [[0, '#fff3d6', 0.45], [1, '#fff3d6', 0]]) }, M.s);
  // floor lamp in the corner: warm at night, off when he sits in the dark
  floorLamp(M.s, M.defs, 1010, 1300, '#ffd59a', night && !dark ? 0.55 : 0);
  if (night && !dark) svg('circle', { cx: 1010, cy: 810, r: 120, fill: rad2(M.defs, [[0, '#fff2d0', 0.7], [1, '#fff2d0', 0]]) }, M.s);
  // mattress on the floor (right) with a crumpled blanket
  contactShadow(M.s, M.defs, 900, 1390, 260, 18, 0.4);
  svg('rect', { x: 680, y: 1300, width: 460, height: 84, rx: 18, fill: '#e9e3d6', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('path', { d: 'M700,1310 Q800,1250 900,1290 Q980,1240 1100,1300 L1100,1350 Q900,1380 700,1350 Z', fill: '#e8a26a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 1000, y: 1262, width: 130, height: 50, rx: 22, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, M.s);
  // standing fan (left)
  const fan = svg('g', { transform: 'translate(70,1150)' }, M.s);
  svg('rect', { x: -6, y: 0, width: 12, height: 200, fill: '#cfd6e2', stroke: INK, 'stroke-width': 4 }, fan);
  svg('ellipse', { cx: 0, cy: 202, rx: 60, ry: 14, fill: '#cfd6e2', stroke: INK, 'stroke-width': 4 }, fan);
  svg('circle', { cx: 0, cy: -10, r: 74, fill: '#dfe6ef', 'fill-opacity': 0.4, stroke: INK, 'stroke-width': 5 }, fan);
  const blades = svg('g', { transform: 'translate(0,-10)' }, fan);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 0, cy: -34, rx: 18, ry: 34, fill: '#7fc3e8', stroke: INK, 'stroke-width': 3, transform: `rotate(${k * 120})` }, blades);
  svg('circle', { cx: 0, cy: -10, r: 12, fill: '#cfd6e2', stroke: INK, 'stroke-width': 4 }, fan);
  // instant noodle cups stacked by the table
  const cups = svg('g', { transform: 'translate(640,1300)' }, M.s);
  const cup = (x, y) => { svg('path', { d: `M${x - 26},${y - 56} L${x + 26},${y - 56} L${x + 20},${y} L${x - 20},${y} Z`, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3.5 }, cups); svg('rect', { x: x - 26, y: y - 42, width: 52, height: 16, fill: '#e0574b' }, cups); };
  cup(0, 0); cup(-46, 0); cup(-23, -58);
  // low folding table + laptop
  const people = svg('g', {}, M.s);
  const table = svg('g', {}, M.s);
  contactShadow(table, M.defs, 470, 1442, 200, 16, 0.45);
  svg('rect', { x: 290, y: 1330, width: 360, height: 26, rx: 8, fill: '#b9875a', stroke: INK, 'stroke-width': 5 }, table);
  for (const lx of [314, 610]) svg('rect', { x: lx, y: 1354, width: 16, height: 84, fill: '#8d6440', stroke: INK, 'stroke-width': 4 }, table);
  const lap = svg('g', { transform: 'translate(540,1330)' }, table);
  svg('path', { d: 'M-90,0 L90,0 L104,-8 L-76,-8 Z', fill: '#9aa3b2', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, lap);
  svg('path', { d: 'M-76,-8 L-96,-130 L74,-130 L94,-8 Z', fill: '#4a5262', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, lap);
  const scr = svg('path', { d: 'M-70,-16 L-86,-122 L66,-122 L82,-16 Z', fill: dark ? '#26324a' : '#dcecff' }, lap);
  const glow = svg('circle', { cx: 500, cy: 1200, r: 300, fill: rad2(M.defs, [[0, '#bfe0ff', 0.4], [1, '#bfe0ff', 0]]), opacity: night && !dark ? 1 : 0 }, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 260, fill: rad2(M.defs, [[0, '#cfe4ff', 0.5], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  const dust = night ? null : floaters(M.s, [560, 260, 520, 1000], 16, 39, { color: '#fff2d0', rMin: 1.2, rMax: 3, speed: 6, op: 0.5, base: 0.1 });
  vignette(M.s, M.defs, night ? 0.5 : 0.35);
  const leaves = R ? [leafG(R, -120, 1880, 1.6, -60, '#1d3a2d'), leafG(R, -80, 1900, 1.5, -25, '#24473a'), leafG(R, -160, 1700, 1.4, -5, '#2b5243')] : [];
  if (R && night && !dark) svg('circle', { cx: 1040, cy: 200, r: 90, fill: '#ffcf8a', opacity: 0.25 }, R.s);
  return {
    people, top, scr, lap, pglow,
    update(t) {
      blades.setAttribute('transform', `translate(0,-10) rotate(${(t * 900) % 360})`);
      twinkles.forEach(w => w.el.setAttribute('opacity', (Math.sin((t + w.ph) * w.rate * 6) > -0.85 ? 0.85 : 0.15)));
      glow.setAttribute('opacity', night && !dark ? (0.85 + 0.15 * Math.sin(t * 9)).toFixed(3) : 0);
      if (dust) dust(t);
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- packed skytrain car, city scrolling past the windows ----------------
function skytrain(S, crowdOpts = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -400, y: -300, width: 1880, height: 2400, fill: lin(F.defs, [[0, '#f0b27a'], [0.45, '#f8d3a0'], [1, '#fdeccb']]) }, F.s);
  svg('circle', { cx: 880, cy: 420, r: 360, fill: rad2(F.defs, [[0, '#fff3d0', 0.9], [0.3, '#ffe2a8', 0.4], [1, '#ffe2a8', 0]]) }, F.s);
  const city = svg('g', {}, F.s);
  for (const k of [0, 1]) {
    const g = svg('g', { transform: `translate(${k * 1600},0)` }, city);
    cityBlocks(g, -300, 1300, 1000, 41 + k, { cols: ['#c49a86', '#d1ab92', '#b58c7c'], win: '#fff3dc', hMin: 220, hMax: 640, dens: 0.75 });
  }
  const poles = svg('g', {}, F.s);
  for (let i = 0; i < 6; i++) svg('rect', { x: i * 520 - 300, y: 300, width: 26, height: 900, fill: '#8a6a5e' }, poles);
  // car body: wall with big windows (window holes show the far layer)
  const body = svg('path', { fill: '#efe4d4', 'fill-rule': 'evenodd', stroke: INK, 'stroke-width': 6, d: 'M-300,-300 L1380,-300 L1380,2200 L-300,2200 Z M-40,330 L460,330 Q480,330 480,350 L480,880 Q480,900 460,900 L-40,900 Z M600,330 L1100,330 Q1120,330 1120,350 L1120,880 Q1120,900 1100,900 L600,900 Z' }, M.s);
  svg('rect', { x: -300, y: 940, width: 1680, height: 30, fill: '#3f9a6a' }, M.s);
  svg('rect', { x: -300, y: 1360, width: 1680, height: 700, fill: lin(M.defs, [[0, '#9a8a80'], [1, '#7a6c64']]) }, M.s);
  svg('rect', { x: -300, y: 1350, width: 1680, height: 14, fill: '#6f625b' }, M.s);
  for (const bx0 of [-40, 600]) svg('path', { d: `M${bx0},330 L${bx0 + 500},330 L${bx0 + 380},1360 L${bx0 - 260},1360 Z`, fill: lin(M.defs, [[0, '#fff1d0', 0.22], [1, '#fff1d0', 0]]) }, M.s);
  // handrail + swinging straps
  svg('rect', { x: -300, y: 230, width: 1680, height: 16, rx: 8, fill: '#d8cfc2', stroke: INK, 'stroke-width': 4 }, M.s);
  const straps = [];
  for (let i = 0; i < 9; i++) {
    const g = svg('g', { transform: `translate(${-120 + i * 160},246)` }, M.s);
    svg('rect', { x: -5, y: 0, width: 10, height: 120, fill: '#3a4a6a' }, g);
    svg('circle', { cx: 0, cy: 140, r: 24, fill: 'none', stroke: '#f2c14e', 'stroke-width': 9 }, g);
    straps.push(g);
  }
  svg('rect', { x: 520, y: 230, width: 22, height: 1140, fill: '#d8cfc2', stroke: INK, 'stroke-width': 4 }, M.s);
  // a crowd of commuters standing around him
  const back = svg('g', {}, M.s);
  const people = svg('g', {}, M.s);
  const front = svg('g', {}, M.s);
  const palette = [['#6b7fa8', '#2f3448'], ['#c96a5a', '#3a3a44'], ['#e2b14e', '#4a4a56'], ['#7aa88c', '#2f3448'], ['#9a7ab8', '#3a3048'], ['#d98aa8', '#2a2a33']];
  const hair = ['#241a17', '#3a2620', '#1f1a1c', '#4a3428'];
  const spots = crowdOpts.spots || [[150, 1330, 1.05, 1, back], [330, 1340, 1.08, -1, back], [760, 1335, 1.06, -1, back], [940, 1325, 1.04, 1, back], [40, 1420, 1.25, 1, front], [1040, 1430, 1.28, -1, front]];
  const crowd = spots.map(([x, y, s, f, layer], i) => {
    const [sh, pa] = palette[i % palette.length];
    const o = { skin: ['#e0aa80', '#c98d62', '#f0c3a0'][i % 3], skinShade: ['#c48f68', '#ae7550', '#d8a27c'][i % 3], hair: hair[i % 4], hairStyle: ['dad', 'long', 'fluffy', 'pony', 'part', 'bun'][i % 6], top: ['tee', 'office', 'blouse', 'tee', 'office', 'tee'][i % 6], sleeve: i % 2 ? 'long' : 'short', shirt: sh, shirtDark: shade(sh, -22), shirtLight: shade(sh, 18), pants: pa, pantsDark: shade(pa, -10), lanyard: '#e0574b', seed: 40 + i };
    const p = new Puppet(layer, o, M.defs);
    return { p, x, y, s, f, ph: i * 1.3, hold: i % 2 === 0 };
  });
  svg('rect', { x: -300, y: -300, width: 1680, height: 2400, fill: '#ffd9a0', opacity: 0.1 }, M.s);
  const mdust = floaters(M.s, [0, 300, 1080, 1000], 18, 57, { color: '#fff2d0', rMin: 1.2, rMax: 3, speed: 8, op: 0.5, base: 0.1 });
  vignette(M.s, M.defs, 0.45);
  const fg = R ? [svg('ellipse', { cx: 120, cy: 1780, rx: 260, ry: 340, fill: '#4a3a3a' }, R.s), svg('ellipse', { cx: 980, cy: 1820, rx: 240, ry: 320, fill: '#5a4048' }, R.s)] : [];
  return {
    people, crowd,
    sway: t => Math.sin(t * 2.2) * 6 + Math.sin(t * 5.1) * 2,
    update(t) {
      city.setAttribute('transform', `translate(${(-(t * 900) % 1600).toFixed(1)},0)`);
      mdust(t);
      poles.setAttribute('transform', `translate(${(-(t * 1500) % 520).toFixed(1)},0)`);
      const sw = Math.sin(t * 2.2) * 6 + Math.sin(t * 5.1) * 2;
      straps.forEach((g, i) => g.setAttribute('transform', `translate(${-120 + i * 160},246) rotate(${(sw * 0.8 + Math.sin(t * 3 + i) * 2).toFixed(2)})`));
      for (const c of crowd) {
        const pose = { x: c.x + sw * 0.6, y: c.y, s: c.s, f: c.f, torso: sw * 0.4 + Math.sin(t * 1.3 + c.ph) * 2, head: 6 + Math.sin(t * 0.9 + c.ph) * 4, lF: [92, 92], lB: [88, 90], t: t + c.ph, smile: 0.25, eyes: null };
        if (c.hold) { const [hx, hy] = [c.x + c.f * 30, 380]; pose.aF = c.p.reach(pose, hx, hy, true); }
        else pose.aF = [100, 70];
        pose.aB = [96, 96];
        c.p.pose(pose);
      }
    },
  };
}

// ---------------- his balcony at night: the city, laundry, AC unit ----------------
function balconyNight(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -400, y: -400, width: 1880, height: 2400, fill: lin(F.defs, [[0, '#121733'], [0.55, '#2c2c5e'], [0.8, '#5a3a6a'], [1, '#8a4a5e']]) }, F.s);
  const r = rng(61), stars = [];
  for (let i = 0; i < 40; i++) stars.push(svg('circle', { cx: r() * 1080, cy: r() * 700, r: 1 + r() * 1.8, fill: '#fff' }, F.s));
  svg('circle', { cx: 820, cy: 260, r: 120, fill: rad2(F.defs, [[0, '#fff6dc', 0.45], [1, '#fff6dc', 0]]) }, F.s);
  svg('circle', { cx: 820, cy: 260, r: 46, fill: '#f6eed8' }, F.s);
  const lit1 = cityBlocks(F.s, -300, 1400, 1180, 71, { cols: ['#252b55', '#2b3160', '#1d2348'], hMin: 200, hMax: 640 });
  // skytrain line crossing the city, a train gliding along it
  svg('rect', { x: -300, y: 1010, width: 1700, height: 26, fill: '#3a3f66' }, F.s);
  for (let i = 0; i < 9; i++) svg('rect', { x: -200 + i * 190, y: 1036, width: 22, height: 150, fill: '#2f3458' }, F.s);
  const train = svg('g', {}, F.s);
  for (let k = 0; k < 3; k++) {
    svg('rect', { x: k * 150, y: 960, width: 144, height: 50, rx: 14, fill: '#d9dee8' }, train);
    svg('rect', { x: k * 150 + 6, y: 964, width: 132, height: 10, fill: '#2f9e5b' }, train);
    for (let w = 0; w < 4; w++) svg('rect', { x: k * 150 + 12 + w * 32, y: 978, width: 24, height: 18, rx: 4, fill: '#ffe9a8' }, train);
  }
  const lit2 = cityBlocks(F.s, -300, 1400, 1300, 73, { cols: ['#1a1f40', '#20264a'], hMin: 120, hMax: 300 });
  // balcony: railing, laundry line, AC unit, little plant
  svg('rect', { x: -300, y: 1340, width: 1680, height: 900, fill: '#5d5a66' }, M.s);
  svg('rect', { x: -300, y: 1330, width: 1680, height: 20, fill: '#48454f' }, M.s);
  svg('path', { d: 'M-300,140 L1380,140', stroke: '#9aa3b2', 'stroke-width': 5 }, M.s);
  const laundry = svg('g', {}, M.s);
  const shirtP = 'M-50,0 L-80,40 L-62,54 L-48,34 L-46,170 L46,170 L48,34 L62,54 L80,40 L50,0 L16,-6 L0,14 L-16,-6 Z';
  svg('path', { d: shirtP, fill: '#f7f7f2', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round', transform: 'translate(200,146)' }, laundry);
  svg('path', { d: shirtP, fill: '#7cbf9a', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round', transform: 'translate(380,146) scale(0.9)' }, laundry);
  svg('rect', { x: 500, y: 140, width: 90, height: 120, rx: 6, fill: '#e0a26a', stroke: INK, 'stroke-width': 4 }, laundry);
  const ac = svg('g', { transform: 'translate(860,1210)' }, M.s);
  svg('rect', { x: -120, y: -110, width: 240, height: 150, rx: 12, fill: '#dfe3ea', stroke: INK, 'stroke-width': 5 }, ac);
  svg('circle', { cx: -40, cy: -36, r: 52, fill: '#9aa3b2', stroke: INK, 'stroke-width': 4 }, ac);
  const acf = svg('g', { transform: 'translate(-40,-36)' }, ac);
  for (let k = 0; k < 4; k++) svg('path', { d: 'M0,0 L10,-42 L-10,-42 Z', fill: '#6d7686', transform: `rotate(${k * 90})` }, acf);
  for (let k = 0; k < 5; k++) svg('rect', { x: 40, y: -90 + k * 22, width: 60, height: 8, rx: 3, fill: '#b9c0cc' }, ac);
  const people = svg('g', {}, M.s);
  // railing in front of him
  const rail = svg('g', {}, M.s);
  svg('rect', { x: -300, y: 1100, width: 1680, height: 18, rx: 8, fill: '#c9d2dc', stroke: INK, 'stroke-width': 4 }, rail);
  for (let i = 0; i < 30; i++) svg('rect', { x: -280 + i * 60, y: 1118, width: 10, height: 222, fill: '#aeb8c6', stroke: INK, 'stroke-width': 2 }, rail);
  svg('rect', { x: -300, y: 1330, width: 1680, height: 12, fill: '#c9d2dc', stroke: INK, 'stroke-width': 3 }, rail);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 240, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.5);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#24473a'), leafG(R, 1150, 1960, 1.4, -150, '#2b5243')] : [];
  return {
    people, top, pglow,
    update(t) {
      stars.forEach((s, i) => s.setAttribute('opacity', (0.4 + 0.5 * Math.sin(t * 2 + i * 1.7)).toFixed(2)));
      [...lit1, ...lit2].forEach((w, i) => { if (i % 3 === 0) w.setAttribute('opacity', (0.55 + 0.35 * Math.sin(t * 1.3 + i)).toFixed(2)); });
      train.setAttribute('transform', `translate(${(((t * 260) % 2200) - 700).toFixed(1)},0)`);
      acf.setAttribute('transform', `translate(-40,-36) rotate(${(t * 700) % 360})`);
      laundry.setAttribute('transform', `skewX(${(Math.sin(t * 1.4) * 1.5).toFixed(2)})`);
      swayLeaves(leaves, t);
    },
  };
}

// ---------------- mom's wooden house up-country, at night ----------------
function momHome(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  const tones = ['#8e6342', '#9a6c48', '#946846', '#a4744e'];
  for (let i = -4; i < 17; i++) {
    svg('rect', { x: i * 84, y: -300, width: 84, height: 2200, fill: tones[(i + 12) % 4] }, F.s);
    svg('rect', { x: i * 84, y: -300, width: 3, height: 2200, fill: '#6a4428', opacity: 0.6 }, F.s);
  }
  // night window with a moon and palms
  svg('rect', { x: 700, y: 240, width: 280, height: 340, rx: 6, fill: '#5a3a22', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('rect', { x: 714, y: 254, width: 252, height: 312, fill: lin(F.defs, [[0, '#18204a'], [1, '#2d3a5e']]) }, F.s);
  svg('circle', { cx: 900, cy: 320, r: 26, fill: '#f6eed8' }, F.s);
  svg('path', { d: 'M714,566 L714,470 Q760,430 800,470 Q840,420 880,470 Q930,440 966,480 L966,566 Z', fill: '#16261e' }, F.s);
  svg('rect', { x: 836, y: 254, width: 8, height: 312, fill: '#5a3a22' }, F.s);
  // his graduation photo (the proudest thing on the wall) + wall clock
  const photoGlow = svg('circle', { cx: 270, cy: 470, r: 220, fill: rad2(F.defs, [[0, '#ffe2a8', 0.45], [1, '#ffe2a8', 0]]) }, F.s);
  gradPhoto(F.s, 170, 330, 200);
  svg('rect', { x: 140, y: 600, width: 260, height: 18, rx: 6, fill: '#c9a24a', stroke: INK, 'stroke-width': 4 }, F.s);
  const clock = svg('g', { transform: 'translate(520,380)' }, F.s);
  svg('circle', { r: 56, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, clock);
  const hh = svg('path', { d: 'M0,0 L0,-28', stroke: INK, 'stroke-width': 6, 'stroke-linecap': 'round' }, clock);
  const mm = svg('path', { d: 'M0,0 L0,-42', stroke: INK, 'stroke-width': 4, 'stroke-linecap': 'round' }, clock);
  // fluorescent tube light
  svg('rect', { x: 330, y: 150, width: 380, height: 22, rx: 11, fill: '#f6fbff', stroke: INK, 'stroke-width': 4 }, F.s);
  const tube = svg('ellipse', { cx: 520, cy: 200, rx: 520, ry: 260, fill: rad2(F.defs, [[0, '#e8f6ff', 0.35], [1, '#e8f6ff', 0]]) }, F.s);
  woodFloor(M.s, M.defs, 1380, '#8a5d3c', '#5a3b24', '#4d321e');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#5a3b24' }, M.s);
  // reed mat, thermos + cups on a tray, old fan
  contactShadow(M.s, M.defs, 540, 1452, 420, 20, 0.4);
  svg('path', { d: 'M150,1400 L930,1400 L980,1470 L100,1470 Z', fill: '#d9b46a', stroke: INK, 'stroke-width': 5 }, M.s);
  for (let k = 0; k < 9; k++) svg('path', { d: `M${180 + k * 86},1404 L${150 + k * 92},1466`, stroke: '#b98f48', 'stroke-width': 5 }, M.s);
  const tray = svg('g', { transform: 'translate(820,1420)' }, M.s);
  svg('ellipse', { cx: 0, cy: 0, rx: 90, ry: 16, fill: '#c0392b', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: -60, y: -100, width: 44, height: 100, rx: 12, fill: '#e04f5f', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: -58, y: -112, width: 40, height: 18, rx: 6, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3.5 }, tray);
  for (const cx of [10, 50]) svg('path', { d: `M${cx - 16},-40 L${cx + 16},-40 L${cx + 12},-4 L${cx - 12},-4 Z`, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3.5 }, tray);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  const moths = floaters(M.s, [300, 120, 460, 200], 8, 81, { color: '#fff6dc', rMin: 2, rMax: 4, speed: 30, op: 0.6, base: 0.2 });
  const leaves = R ? [leafG(R, -120, 1900, 1.6, -60, '#2a4a34'), leafG(R, -80, 1960, 1.5, -25, '#335a3e')] : [];
  return {
    people, top, photoGlow,
    update(t, hour = 20.5) {
      tube.setAttribute('opacity', (0.9 + 0.1 * Math.sin(t * 31) * Math.sin(t * 7)).toFixed(3));
      hh.setAttribute('transform', `rotate(${(hour % 12) * 30})`); mm.setAttribute('transform', `rotate(${(hour % 1) * 360})`);
      moths(t);
      swayLeaves(leaves, t);
    },
  };
}
