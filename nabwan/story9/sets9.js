// "39 บาทที่แม่ไม่กล้ากด" sets — one provincial house: ฝ้าย's room at night, แม่'s living room (night under the tube
// light with the TV on, and morning sun a few days later), and the front-door sill where the wired slippers wait.
// Lit for depth with pro.js (AO, light pools, shafts, cast-shadow layer) and dressed with props8.js.

// ฝ้าย's graduation photo for mom's wall
function faiPhoto(g, x, y, w = 190) {
  const h = w * 1.18;
  svg('rect', { x: x - 6, y: y - 6, width: w + 12, height: h + 12, rx: 8, fill: '#e0b04a', stroke: INK, 'stroke-width': 5 }, g);
  svg('rect', { x: x + 8, y: y + 8, width: w - 16, height: h - 16, fill: '#8a5a2a' }, g);
  svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32, fill: '#cfe3f2' }, g);
  faceFai(g, x + w / 2, y + h * 0.46, w * 0.2, { smile: 0.9 });
  svg('path', { d: `M${x + w * 0.24},${y + h - 16} C${x + w * 0.26},${y + h * 0.72} ${x + w * 0.74},${y + h * 0.72} ${x + w * 0.76},${y + h - 16} Z`, fill: '#2a2a33', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: `M${x + w * 0.3},${y + h * 0.22} L${x + w * 0.5},${y + h * 0.13} L${x + w * 0.7},${y + h * 0.22} L${x + w * 0.5},${y + h * 0.29} Z`, fill: '#2a2a33', stroke: INK, 'stroke-width': 3 }, g);   // mortarboard
  // a jasmine garland over the corner
  for (let k = 0; k < 9; k++) svg('circle', { cx: x + w - 10 - k * 9, cy: y - 2 + Math.sin(k * 0.6) * 10 + k * 3, r: 7, fill: '#fbf8f1', stroke: INK, 'stroke-width': 1.6 }, g);
  svg('circle', { cx: x + w - 6, cy: y + 4, r: 9, fill: '#e0453b', stroke: INK, 'stroke-width': 2 }, g);
}
// November calendar with the 11th circled in red
function saleCalendar(g, x, y, w = 190) {
  const h = w * 1.2;
  svg('rect', { x, y, width: w, height: h, rx: 6, fill: '#fbf8f1', stroke: INK, 'stroke-width': 4 }, g);
  svg('rect', { x, y, width: w, height: h * 0.2, rx: 6, fill: '#e0574b', stroke: INK, 'stroke-width': 4 }, g);
  const tx = svg('text', { x: x + w / 2, y: y + h * 0.15, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': w * 0.13, fill: '#fff6dc' }, g); tx.textContent = 'พฤศจิกายน';
  const cw = (w - 20) / 7;
  for (let d = 1; d <= 30; d++) {
    const c = (d + 5) % 7, r = Math.floor((d + 5) / 7);
    const cx = x + 10 + cw * (c + 0.5), cy = y + h * 0.3 + r * (h * 0.14);
    const t = svg('text', { x: cx, y: cy + 6, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': d === 11 ? 700 : 500, 'font-size': w * 0.085, fill: d === 11 ? '#e0453b' : '#6a5a4a' }, g); t.textContent = d;
    if (d === 11) svg('ellipse', { cx, cy: cy + 1, rx: cw * 0.62, ry: w * 0.07, fill: 'none', stroke: '#e0453b', 'stroke-width': 3.5, transform: `rotate(-8 ${cx} ${cy})` }, g);
  }
}
// garden at night (or day) seen through a window: sky, moon/sun, banana leaves, fireflies; returns update(t)
function gardenView(F, x, y, w, h, mode, seed) {
  const day = mode === 'day';
  svg('rect', { x, y, width: w, height: h, fill: lin(F.defs, day ? [[0, '#8fd0f0'], [1, '#d8f0e0']] : [[0, '#121a3a'], [1, '#283a5a']]) }, F.s);
  if (day) svg('circle', { cx: x + w * 0.75, cy: y + h * 0.2, r: 60, fill: rad2(F.defs, [[0, '#fff6dc', 0.95], [1, '#fff6dc', 0]]) }, F.s);
  else { svg('circle', { cx: x + w * 0.72, cy: y + h * 0.22, r: 64, fill: rad2(F.defs, [[0, '#fff6dc', 0.45], [1, '#fff6dc', 0]]) }, F.s); svg('circle', { cx: x + w * 0.72, cy: y + h * 0.22, r: 26, fill: '#f6eed8' }, F.s); }
  const leafC = day ? ['#4f9e5e', '#3f8a52', '#5aae68'] : ['#14281e', '#1a3226', '#203a2c'];
  const r = rng(seed);
  for (let i = 0; i < 6; i++) {
    const bx = x + r() * w, by = y + h * (0.45 + r() * 0.5), a = -150 + r() * 120, L = 140 + r() * 120;
    const lg = svg('g', { transform: `translate(${bx.toFixed(1)},${by.toFixed(1)}) rotate(${a.toFixed(1)})` }, F.s);
    svg('path', { d: `M0,0 C${L * 0.3},${-L * 0.28} ${L * 0.8},${-L * 0.26} ${L},0 C${L * 0.8},${L * 0.22} ${L * 0.3},${L * 0.24} 0,0 Z`, fill: leafC[i % 3] }, lg);
    for (let k = 1; k < 6; k++) svg('path', { d: `M${L * k / 6},0 l${L * 0.06},${-L * 0.14}`, stroke: day ? '#2f6b3a' : '#0c1a12', 'stroke-width': 3 }, lg);
  }
  svg('rect', { x, y: y + h - 60, width: w, height: 60, fill: day ? '#6aae5a' : '#0e1c16' }, F.s);
  const flies = day ? [] : Array.from({ length: 8 }, () => ({ el: svg('circle', { r: 3.4, fill: '#f6f2a0' }, F.s), u: r(), v: r(), ph: r() * 9 }));
  return t => flies.forEach(f => setA(f.el, { cx: (x + 20 + (w - 40) * ((f.u + 0.05 * Math.sin(t * 0.6 + f.ph)) % 1)).toFixed(1), cy: (y + h * 0.4 + h * 0.5 * f.v + 14 * Math.sin(t * 0.9 + f.ph)).toFixed(1), opacity: (0.4 + 0.6 * Math.max(0, Math.sin(t * 2.2 + f.ph))).toFixed(2) }));
}
// wooden window frame with a white steel grille over the glass
function grilleWindow(F, x, y, w, h) {
  svg('rect', { x: x - 18, y: y - 18, width: w + 36, height: h + 36, rx: 6, fill: 'none', stroke: '#8a5a3a', 'stroke-width': 22 }, F.s);
  svg('rect', { x: x - 18, y: y - 18, width: w + 36, height: h + 36, rx: 6, fill: 'none', stroke: INK, 'stroke-width': 4 }, F.s);
  const gp = svg('g', { stroke: '#efe9dc', 'stroke-width': 6, fill: 'none', opacity: 0.95 }, F.s);
  for (let gx = x; gx <= x + w; gx += w / 4) svg('path', { d: `M${gx},${y} L${gx},${y + h}` }, gp);
  for (let gy = y + h / 3; gy < y + h; gy += h / 3) svg('path', { d: `M${x},${gy} L${x + w},${gy}` }, gp);
  for (let gx = x; gx < x + w; gx += w / 4) for (let gy = y; gy < y + h; gy += h / 3) svg('path', { d: `M${gx + w / 8},${gy + 10} L${gx + w / 4 - 10},${gy + h / 6} L${gx + w / 8},${gy + h / 3 - 10} L${gx + 10},${gy + h / 6} Z` }, gp);
  svg('rect', { x: x - 30, y: y + h + 10, width: w + 60, height: 20, rx: 6, fill: '#a0704a', stroke: INK, 'stroke-width': 4 }, F.s);
}
// standing fan (floor at y); returns update(t) — oscillating head, spinning blades
function standFan(g, x, y, s = 1, c = '#4fb0c6') {
  const f = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('ellipse', { cx: 0, cy: -8, rx: 70, ry: 16, fill: '#e8e2d6', stroke: INK, 'stroke-width': 4 }, f);
  svg('rect', { x: -8, y: -300, width: 16, height: 292, rx: 6, fill: '#e8e2d6', stroke: INK, 'stroke-width': 4 }, f);
  const head = svg('g', { transform: 'translate(0,-330)' }, f);
  const bl = svg('g', {}, head);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 0, cy: -34, rx: 20, ry: 36, fill: c, opacity: 0.8, transform: `rotate(${k * 120})` }, bl);
  svg('circle', { r: 76, fill: 'none', stroke: INK, 'stroke-width': 5 }, head);
  for (let k = 0; k < 10; k++) svg('path', { d: `M0,0 L${(Math.cos(k * 0.628) * 76).toFixed(1)},${(Math.sin(k * 0.628) * 76).toFixed(1)}`, stroke: INK, 'stroke-width': 1.5, opacity: 0.45 }, head);
  svg('circle', { r: 66, fill: 'none', stroke: INK, 'stroke-width': 1.5, opacity: 0.45 }, head);
  svg('circle', { r: 18, fill: '#e8e2d6', stroke: INK, 'stroke-width': 4 }, head);
  return t => { const sw = Math.sin(t * 0.8); head.setAttribute('transform', `translate(0,-330) scale(${(0.82 + 0.18 * Math.abs(Math.cos(t * 0.8))).toFixed(3)},1) skewY(${(sw * 6).toFixed(2)})`); bl.setAttribute('transform', `rotate(${((t * 1100) % 360).toFixed(1)})`); };
}
// box TV on a cabinet; returns { update(t), glow }
function crtTV(g, defs, x, yFloor, on) {
  svg('rect', { x, y: yFloor - 190, width: 240, height: 190, rx: 8, fill: '#9a6a44', stroke: INK, 'stroke-width': 5 }, g);
  for (const dx of [14, 124]) { svg('rect', { x: x + dx, y: yFloor - 172, width: 102, height: 150, rx: 6, fill: '#a87850', stroke: INK, 'stroke-width': 3 }, g); svg('circle', { cx: x + dx + (dx < 50 ? 88 : 14), cy: yFloor - 98, r: 5, fill: '#e0b04a', stroke: INK, 'stroke-width': 2 }, g); }
  const tv = svg('g', {}, g);
  svg('rect', { x: x + 16, y: yFloor - 390, width: 208, height: 196, rx: 18, fill: '#d6d0c2', stroke: INK, 'stroke-width': 5 }, tv);
  svg('rect', { x: x + 32, y: yFloor - 374, width: 140, height: 120, rx: 16, fill: on ? '#2a4a6a' : '#3a4048', stroke: INK, 'stroke-width': 4 }, tv);
  const scr = svg('g', {}, tv);
  if (on) {
    svg('rect', { x: x + 36, y: yFloor - 370, width: 132, height: 112, rx: 14, fill: lin(defs, [[0, '#f2b880'], [1, '#c96a6a']]) }, scr);
    svg('circle', { cx: x + 80, cy: yFloor - 316, r: 22, fill: '#3a2a2a' }, scr); svg('circle', { cx: x + 124, cy: yFloor - 312, r: 20, fill: '#4a2f2f' }, scr);
  }
  svg('path', { d: `M${x + 40},${yFloor - 366} q30,-6 50,6`, stroke: '#fff', 'stroke-width': 4, opacity: 0.35, fill: 'none' }, tv);
  for (let k = 0; k < 3; k++) svg('circle', { cx: x + 198, cy: yFloor - 352 + k * 30, r: 7, fill: '#9a948a', stroke: INK, 'stroke-width': 2.5 }, tv);
  svg('path', { d: `M${x + 90},${yFloor - 390} L${x + 60},${yFloor - 450} M${x + 150},${yFloor - 390} L${x + 186},${yFloor - 446}`, stroke: '#6b7280', 'stroke-width': 4 }, tv);
  const glow = on ? lightPool(g, defs, x + 104, yFloor - 300, 300, 260, '#9fc4ff', 0.28) : null;
  return { glow, update(t) { if (!on) return; const k = 0.75 + 0.25 * Math.sin(t * 7.3) * Math.sin(t * 2.1 + 1); scr.setAttribute('opacity', (0.85 + 0.15 * k).toFixed(3)); glow.setAttribute('opacity', k.toFixed(3)); } };
}

// ---------------- ฝ้าย's room at night: dusty-rose walls, a garden window, the 11.11 calendar, parcels and a clothes rail ----------------
function faiRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#8e505c'], [1, '#ab6c70']]) }, F.s);
  for (let i = 0; i < 26; i++) svg('rect', { x: -300 + i * 70, y: -300, width: 26, height: 2600, fill: '#ffffff', opacity: 0.045 }, F.s);
  const garden = gardenView(F, 640, 250, 330, 420, 'night', 93);
  grilleWindow(F, 640, 250, 330, 420);
  curtains2(F, 576, 960, 210, 540, '#f6efe2', '#e2d6c2', '#d6c8b0');
  svg('rect', { x: 556, y: 200, width: 520, height: 12, rx: 6, fill: '#5a3a2a' }, F.s);
  const bulbs = lightString(F.s, 20, 1060, 120, 30, ['#ffd66b', '#ffe8b0', '#ff9fc0'], 15);
  saleCalendar(F.s, 110, 300, 180);
  // round mirror with photo-booth strips tucked in
  svg('circle', { cx: 405, cy: 400, r: 92, fill: '#e0b04a', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('circle', { cx: 405, cy: 400, r: 76, fill: lin(F.defs, [[0, '#dceaf2'], [1, '#a9c4d6']]) }, F.s);
  svg('path', { d: 'M360,360 Q380,334 410,338', fill: 'none', stroke: '#fff', 'stroke-width': 7, 'stroke-linecap': 'round', opacity: 0.8 }, F.s);
  for (const [px, a] of [[316, -10], [480, 8]]) { const sg = svg('g', { transform: `rotate(${a} ${px} 420)` }, F.s); svg('rect', { x: px - 18, y: 360, width: 36, height: 120, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3 }, sg); for (let k = 0; k < 3; k++) svg('rect', { x: px - 13, y: 366 + k * 37, width: 26, height: 31, fill: ['#f6c6d4', '#bfe0f0', '#ffe2a8'][k] }, sg); }
  // shelf of skincare and a plush
  wallShelf(F.s, 90, 700, 420, '#e8d2b0');
  for (const [bx, bh, c] of [[110, 60, '#f6a6bc'], [140, 80, '#fbf8f1'], [172, 50, '#9fe0ff'], [200, 70, '#f2c14e'], [232, 56, '#c9a8e8']]) { svg('rect', { x: bx, y: 700 - bh, width: 26, height: bh, rx: 7, fill: c, stroke: INK, 'stroke-width': 3 }, F.s); svg('rect', { x: bx + 6, y: 700 - bh - 12, width: 14, height: 14, rx: 3, fill: '#fbf8f1', stroke: INK, 'stroke-width': 2.5 }, F.s); }
  teddy(F.s, 320, 700, 0.85, '#f2d0a8');
  tinyCactus(F.s, 420, 700, '#4a7bd8');
  woodFloor(M.s, M.defs, 1330, '#c99a6e', '#9a6e4c', '#8a5e40');
  svg('rect', { x: -300, y: 1330, width: 300, height: 1000, fill: '#9a6e4c' }, M.s); svg('rect', { x: 1080, y: 1330, width: 300, height: 1000, fill: '#9a6e4c' }, M.s);
  svg('rect', { x: -300, y: 1318, width: 1680, height: 16, fill: '#f6efe2', stroke: INK, 'stroke-width': 3 }, M.s);
  wallAO(M.s, M.defs, 1318);
  rug(M.s, M.defs, 520, 1580, 470, 110, '#3f5a8a');
  svg('ellipse', { cx: 520, cy: 1580, rx: 400, ry: 88, fill: 'none', stroke: '#f2c14e', 'stroke-width': 6, opacity: 0.5, 'stroke-dasharray': '18 14' }, M.s);
  // clothes rail with her shopping, behind the parcels
  const rail = svg('g', {}, M.s);
  for (const px of [820, 1060]) svg('rect', { x: px - 6, y: 760, width: 12, height: 570, fill: '#c9d2dc', stroke: INK, 'stroke-width': 3 }, rail);
  svg('rect', { x: 800, y: 752, width: 290, height: 14, rx: 6, fill: '#c9d2dc', stroke: INK, 'stroke-width': 3 }, rail);
  [['#f6a6bc', 'tee'], ['#fbf8f1', 'shirt'], ['#4a7bd8', 'dress'], ['#f2c14e', 'tee'], ['#7fc6a8', 'shirt'], ['#e0574b', 'dress']].forEach(([c, k], i) => {
    const hx = 846 + i * 38, cg = svg('g', {}, rail);
    svg('path', { d: `M${hx},766 q-10,-14 0,-20 q10,6 0,12`, fill: 'none', stroke: '#6b7280', 'stroke-width': 3 }, cg);
    const len = k === 'dress' ? 260 : 170;
    svg('path', { d: `M${hx - 30},790 L${hx - 8},772 L${hx + 8},772 L${hx + 30},790 L${hx + 26},${780 + len} L${hx - 26},${780 + len} Z`, fill: c, stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, cg);
  });
  const shadowL = svg('g', {}, M.s);
  lampCone(M.s, M.defs, 715, 1030, 300, 520, '#ffe2a8', 0.22);
  contactShadow(M.s, M.defs, 330, 1338, 320, 20, 0.45);
  // bed: white frame, cloud duvet
  svg('rect', { x: 0, y: 930, width: 96, height: 400, rx: 30, fill: '#fbf8f1', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 40, y: 1200, width: 560, height: 120, rx: 14, fill: '#f6efe2', stroke: INK, 'stroke-width': 5 }, M.s);
  for (const lx of [58, 560]) svg('rect', { x: lx, y: 1316, width: 22, height: 20, rx: 4, fill: '#c9b48e', stroke: INK, 'stroke-width': 3 }, M.s);
  svg('rect', { x: 50, y: 1166, width: 540, height: 54, rx: 20, fill: '#fbf6ee', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 70, y: 1108, width: 150, height: 64, rx: 26, fill: '#ffffff', stroke: INK, 'stroke-width': 5, transform: 'rotate(-6 145 1140)' }, M.s);
  svg('path', { d: 'M250,1170 Q400,1120 590,1172 L590,1236 Q420,1252 250,1230 Z', fill: '#9fc6ee', stroke: INK, 'stroke-width': 5 }, M.s);
  for (const [cx, cy] of [[320, 1196], [430, 1180], [540, 1206]]) svg('path', { d: `M${cx - 22},${cy} a12,12 0 0 1 12,-12 a14,14 0 0 1 24,4 a10,10 0 0 1 8,18 Z`, fill: '#ffffff', opacity: 0.75 }, M.s);
  svg('rect', { x: 140, y: 1120, width: 110, height: 70, rx: 30, fill: '#f6c6d4', stroke: INK, 'stroke-width': 5, transform: 'rotate(8 195 1155)' }, M.s);
  // nightstand + lamp
  svg('rect', { x: 640, y: 1170, width: 150, height: 160, rx: 8, fill: '#e6d2b8', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 656, y: 1236, width: 118, height: 8, fill: '#c4ab8c' }, M.s);
  svg('circle', { cx: 715, cy: 1060, r: 290, fill: rad2(M.defs, [[0, '#ffd59a', 0.4], [1, '#ffd59a', 0]]) }, M.s);
  svg('path', { d: 'M690,1170 L740,1170 L732,1090 L698,1090 Z', fill: '#f2d6a2', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('path', { d: 'M672,1090 L758,1090 L738,1030 L692,1030 Z', fill: lin(M.defs, [[0, '#fff2d6'], [1, '#f2d6a2']]), stroke: INK, 'stroke-width': 4 }, M.s);
  mugProp(M.s, 770, 1170, '#7fc6a8');
  // tonight's parcels and two paper shopping bags
  for (const [bx, by, bw, bh] of [[840, 1250, 150, 80], [860, 1186, 110, 64], [990, 1270, 90, 60]]) {
    svg('rect', { x: bx, y: by, width: bw, height: bh, rx: 6, fill: '#d9a86a', stroke: INK, 'stroke-width': 4 }, M.s);
    svg('rect', { x: bx + bw / 2 - 8, y: by, width: 16, height: bh, fill: '#e0574b', opacity: 0.8 }, M.s);
  }
  for (const [bx, c] of [[110, '#f2c14e'], [200, '#f6a6bc']]) { const bg = svg('g', { transform: `translate(${bx},1420)` }, M.s); svg('path', { d: 'M-46,0 L-40,-96 L40,-96 L46,0 Z', fill: c, stroke: INK, 'stroke-width': 4 }, bg); svg('path', { d: 'M-18,-96 Q-18,-124 0,-124 Q18,-124 18,-96', fill: 'none', stroke: INK, 'stroke-width': 4 }, bg); }
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 230, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  lightPool(M.s, M.defs, 715, 1350, 300, 60, '#ffe2a8', 0.35);
  vignette(M.s, M.defs, 0.45);
  const leaves = R ? [leafG(R, -120, 1900, 1.6, -60, '#3a6b47'), leafG(R, -80, 1960, 1.4, -25, '#4f8f56')] : [];
  const bok = R ? bokehField(R.s, R.defs, 7, [-100, 0, 1180, 240], ['#ffd66b', '#ffe8b0', '#ff9fc0'], 95, { rMin: 40, rMax: 90, op: 0.5 }) : null;
  return {
    people, top, pglow, shadowL, light: { ux: 0.94, uy: -0.25, lx: 715 },
    update(t) {
      garden(t);
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.2 + i * 1.7)).toFixed(2)));
      swayLeaves(leaves, t); if (bok) bok(t);
    },
  };
}

// ---------------- แม่'s living room: cream walls over a mint dado, tube light, box TV, standing fan, reed mat ----------------
function momHouse(S, mode = 'night') {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, day = mode === 'day';
  svg('rect', { x: -300, y: -300, width: 1680, height: 1370, fill: lin(F.defs, day ? [[0, '#f2dca6'], [1, '#e8c98a']] : [[0, '#dcc48c'], [1, '#c9a86e']]) }, F.s);
  svg('rect', { x: -300, y: 1070, width: 1680, height: 1300, fill: lin(F.defs, [[0, '#9ccc9a'], [1, '#86b886']]) }, F.s);
  svg('rect', { x: -300, y: 1060, width: 1680, height: 14, fill: '#b98a54', stroke: INK, 'stroke-width': 3 }, F.s);
  const garden = gardenView(F, 680, 300, 300, 400, mode, 97);
  grilleWindow(F, 680, 300, 300, 400);
  svg('path', { d: 'M960,270 Q930,500 970,730 L1010,730 L1010,270 Z', fill: '#fbf8f1', opacity: 0.85, stroke: INK, 'stroke-width': 3 }, F.s);   // lace curtain pulled aside
  faiPhoto(F.s, 150, 300, 200);
  saleCalendar(F.s, 190, 620, 150);
  const clk = wallClock(F.s, 540, 380, 46, '#e0574b');
  // fluorescent tube
  svg('rect', { x: 330, y: 196, width: 380, height: 22, rx: 11, fill: day ? '#e8eef2' : '#fbfdff', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('rect', { x: 320, y: 214, width: 400, height: 10, rx: 4, fill: '#c9d2dc', stroke: INK, 'stroke-width': 3 }, F.s);
  const tube = day ? null : svg('ellipse', { cx: 520, cy: 230, rx: 560, ry: 300, fill: rad2(F.defs, [[0, '#fffbe8', 0.5], [1, '#fffbe8', 0]]) }, F.s);
  // shelf with a radio and a vase of flowers
  wallShelf(F.s, 400, 860, 240, '#a0704a');
  svg('rect', { x: 420, y: 790, width: 110, height: 70, rx: 12, fill: '#c94f45', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('circle', { cx: 452, cy: 826, r: 20, fill: '#3a2a2a', stroke: '#e8dcc4', 'stroke-width': 3 }, F.s);
  svg('rect', { x: 484, y: 806, width: 34, height: 8, rx: 3, fill: '#f2c14e' }, F.s);
  svg('path', { d: 'M560,860 L552,812 L596,812 L588,860 Z', fill: '#4a7bd8', stroke: INK, 'stroke-width': 3.5 }, F.s);
  for (const [fx, fy, c] of [[560, 770, '#f6a6bc'], [584, 760, '#fbf8f1'], [604, 778, '#e0574b']]) { svg('path', { d: `M574,812 L${fx},${fy + 10}`, stroke: '#4f9e5e', 'stroke-width': 3 }, F.s); svg('circle', { cx: fx, cy: fy, r: 13, fill: c, stroke: INK, 'stroke-width': 2.5 }, F.s); }
  if (day) haze(F.s, F.defs, '#fff6dc', 0.12);
  // floor: red-brown tiles
  svg('rect', { x: -300, y: 1380, width: 1680, height: 1000, fill: lin(M.defs, [[0, '#c4704e'], [1, '#8a4a34']]) }, M.s);
  for (let y = 1380, k = 0; y < 2300; y += 50 + k * 12, k++) svg('rect', { x: -300, y, width: 1680, height: 3, fill: '#6a3424', opacity: 0.5 }, M.s);
  for (let i = -6; i < 22; i++) svg('path', { d: `M${540 + (i * 80 - 540) * 1},1380 L${540 + (i * 80 - 540) * 2.2},2300`, stroke: '#6a3424', 'stroke-width': 3, opacity: 0.4 }, M.s);
  svg('rect', { x: -300, y: 1368, width: 1680, height: 14, fill: '#7a8a6a', stroke: INK, 'stroke-width': 3 }, M.s);
  wallAO(M.s, M.defs, 1370, { op: 0.3 });
  const tv = crtTV(M.s, M.defs, 20, 1380, !day);
  const fan = standFan(M.s, 1000, 1400, 0.95);
  const shadowL = svg('g', {}, M.s);
  const shaft = day ? lightShaft(M.s, M.defs, [[690, 300], [980, 300], [640, 1520], [220, 1520]], '#fff1c4', 0.26, 97, 30) : null;
  if (day) lightPool(M.s, M.defs, 430, 1470, 330, 70, '#fff1c4', 0.45);
  contactShadow(M.s, M.defs, 540, 1452, 420, 20, 0.4);
  // reed mat with red and green weave stripes
  svg('path', { d: 'M150,1400 L930,1400 L990,1478 L90,1478 Z', fill: '#e2c47a', stroke: INK, 'stroke-width': 5 }, M.s);
  for (const [v, c] of [[0.22, '#c94f45'], [0.3, '#4f9e5e'], [0.7, '#4f9e5e'], [0.78, '#c94f45']]) svg('path', { d: `M${150 - 60 * v},${1400 + 78 * v} L${930 + 60 * v},${1400 + 78 * v}`, stroke: c, 'stroke-width': 7 }, M.s);
  for (let k = 0; k < 10; k++) svg('path', { d: `M${180 + k * 78},1404 L${140 + k * 84},1474`, stroke: '#c9a85e', 'stroke-width': 3 }, M.s);
  // a tray with a thermos and glasses
  const tray = svg('g', { transform: 'translate(890,1430)' }, M.s);
  svg('ellipse', { cx: 0, cy: 0, rx: 80, ry: 15, fill: '#c0392b', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: -50, y: -96, width: 42, height: 96, rx: 12, fill: '#e04f5f', stroke: INK, 'stroke-width': 4 }, tray);
  svg('rect', { x: -48, y: -108, width: 38, height: 18, rx: 6, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3.5 }, tray);
  svg('path', { d: 'M8,-40 L40,-40 L36,-4 L12,-4 Z', fill: '#f6f1e6', opacity: 0.9, stroke: INK, 'stroke-width': 3.5 }, tray);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 220, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, day ? 0.35 : 0.48);
  const moths = day ? null : floaters(M.s, [330, 150, 710, 240], 8, 91, { color: '#fff6dc', rMin: 2, rMax: 4, speed: 30, op: 0.6, base: 0.2 });
  // near foreground, out of focus: a potted plant at the right edge and a low table edge with a plate of fruit
  let foreG = null, bok = null;
  if (R) {
    foreG = svg('g', {}, R.s);
    pottedPlant(foreG, 1120, 1960, 1.5, 'snake', '#c94f45');
    svg('ellipse', { cx: 120, cy: 1860, rx: 300, ry: 46, fill: '#8a5a3a', stroke: INK, 'stroke-width': 5 }, foreG);
    for (const [fx, c] of [[60, '#f2c14e'], [130, '#e0574b'], [190, '#7fc6a8']]) svg('circle', { cx: fx, cy: 1810, r: 34, fill: c, stroke: INK, 'stroke-width': 4 }, foreG);
    bok = bokehField(R.s, R.defs, 5, [-100, -100, 1180, 200], day ? ['#fff6dc', '#ffe8b0'] : ['#fffbe8', '#ffe2a8'], 99, { rMin: 50, rMax: 100, op: 0.35 });
  }
  return {
    people, top, pglow, shadowL, light: day ? { ux: 0.8, uy: -0.6, lx: 1200 } : { ux: -0.35, uy: -0.94, lx: 300 },
    update(t, hour = 21.4, cam) {
      garden(t); tv.update(t); fan(t); clk(hour);
      if (tube) tube.setAttribute('opacity', (0.92 + 0.08 * Math.sin(t * 31) * Math.sin(t * 7)).toFixed(3));
      if (moths) moths(t); if (shaft) shaft(t); if (bok) bok(t);
      if (foreG) foreG.setAttribute('opacity', cam && cam.z > 1.7 ? 0 : 1);
    },
  };
}

// a flip-flop seen at three-quarters on the floor (centre x, floor y). o.old: faded sole, cracked, the strap wired back on
function slipper3q(g, x, y, s = 1, o = {}) {
  const f = svg('g', { transform: `translate(${x},${y}) scale(${(o.flip ? -1 : 1) * s},${s})` }, g);
  const sole = o.old ? '#c9b48e' : (o.c || '#4fc3e0'), side = o.old ? '#9a8a66' : shade(o.c || '#4fc3e0', -22), strap = o.old ? '#7a6a8a' : (o.strap || '#f07aa8');
  svg('ellipse', { cx: 0, cy: 14, rx: 74, ry: 16, fill: '#000', opacity: 0.22 }, f);
  const outline = 'M-64,0 C-70,-26 -40,-38 0,-36 C40,-38 72,-24 66,0 C62,18 30,22 0,20 C-30,22 -60,16 -64,0 Z';
  svg('path', { d: outline, fill: side, stroke: INK, 'stroke-width': 4, transform: 'translate(0,9)' }, f);
  svg('path', { d: outline, fill: sole, stroke: INK, 'stroke-width': 4 }, f);
  svg('path', { d: 'M-50,-8 C-40,-26 20,-30 46,-14', fill: 'none', stroke: o.old ? '#b09a74' : '#ffffff', 'stroke-width': 4, opacity: 0.5 }, f);
  if (o.old) {
    svg('path', { d: 'M-20,4 l8,-6 l4,6 l8,-7', fill: 'none', stroke: '#6a5a44', 'stroke-width': 2.5 }, f);
    svg('path', { d: 'M30,-14 l-6,8 l7,4', fill: 'none', stroke: '#6a5a44', 'stroke-width': 2.2 }, f);
    svg('ellipse', { cx: 34, cy: -4, rx: 14, ry: 7, fill: '#a8946e', opacity: 0.7 }, f);   // worn heel
  }
  // the V strap stands up off the sole to the toe post
  svg('path', { d: 'M-46,-6 Q-30,-58 -20,-34', fill: 'none', stroke: INK, 'stroke-width': 13, 'stroke-linecap': 'round' }, f);
  svg('path', { d: 'M-46,-6 Q-30,-58 -20,-34', fill: 'none', stroke: strap, 'stroke-width': 7, 'stroke-linecap': 'round' }, f);
  svg('path', { d: 'M-20,-34 Q10,-62 34,-6', fill: 'none', stroke: INK, 'stroke-width': 13, 'stroke-linecap': 'round' }, f);
  svg('path', { d: 'M-20,-34 Q10,-62 34,-6', fill: 'none', stroke: strap, 'stroke-width': 7, 'stroke-linecap': 'round' }, f);
  svg('circle', { cx: -20, cy: -32, r: 6, fill: strap, stroke: INK, 'stroke-width': 3 }, f);
  if (o.old) {   // wire coiled round the broken joint
    for (let k = 0; k < 5; k++) { svg('ellipse', { cx: -26 + k * 3.2, cy: -40 + k * 1.5, rx: 3.4, ry: 8, fill: 'none', stroke: '#e6ecf2', 'stroke-width': 3, transform: `rotate(-30 ${-26 + k * 3.2} ${-40 + k * 1.5})` }, f); svg('ellipse', { cx: -26 + k * 3.2, cy: -40 + k * 1.5, rx: 3.4, ry: 8, fill: 'none', stroke: '#6b7280', 'stroke-width': 1.2, transform: `rotate(-30 ${-26 + k * 3.2} ${-40 + k * 1.5})` }, f); }
    svg('path', { d: 'M-12,-36 q10,4 6,14 q-3,6 4,10', fill: 'none', stroke: '#c9d2dc', 'stroke-width': 3, 'stroke-linecap': 'round' }, f);
    svg('path', { d: 'M-12,-36 q10,4 6,14 q-3,6 4,10', fill: 'none', stroke: '#6b7280', 'stroke-width': 1, 'stroke-linecap': 'round' }, f);
  }
  return f;
}

// ---------------- the front-door sill: mom's wired slippers next to ฝ้าย's new sneakers, moonlight across the tiles ----------------
function doorSill(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1370, fill: lin(F.defs, [[0, '#cdb47e'], [1, '#b89a62']]) }, F.s);
  svg('rect', { x: -300, y: 1070, width: 1680, height: 1300, fill: lin(F.defs, [[0, '#8cbc8a'], [1, '#78a878']]) }, F.s);
  svg('rect', { x: -300, y: 1060, width: 1680, height: 14, fill: '#a07a4a', stroke: INK, 'stroke-width': 3 }, F.s);
  // the open door: frame, the night outside, the door leaf swung in
  svg('rect', { x: 600, y: 360, width: 360, height: 1040, fill: lin(F.defs, [[0, '#0e1630'], [1, '#22304e']]) }, F.s);
  svg('circle', { cx: 860, cy: 520, r: 30, fill: '#f6eed8' }, F.s); svg('circle', { cx: 860, cy: 520, r: 90, fill: rad2(F.defs, [[0, '#fff6dc', 0.35], [1, '#fff6dc', 0]]) }, F.s);
  svg('path', { d: 'M600,1100 Q700,1000 820,1080 Q900,1020 960,1060 L960,1400 L600,1400 Z', fill: '#0c1a14' }, F.s);
  svg('rect', { x: 584, y: 344, width: 392, height: 1060, fill: 'none', stroke: '#8a5a3a', 'stroke-width': 30 }, F.s);
  svg('rect', { x: 584, y: 344, width: 392, height: 1060, fill: 'none', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('path', { d: 'M600,360 L470,420 L470,1360 L600,1400 Z', fill: '#a8744a', stroke: INK, 'stroke-width': 5 }, F.s);
  for (const [y0, y1] of [[460, 820], [880, 1300]]) svg('path', { d: `M585,${y0} L490,${y0 + 40} L490,${y1 - 30} L585,${y1} Z`, fill: 'none', stroke: '#8a5a3a', 'stroke-width': 5 }, F.s);
  svg('circle', { cx: 500, cy: 900, r: 9, fill: '#e0b04a', stroke: INK, 'stroke-width': 3 }, F.s);
  // a gecko on the wall
  const gk = svg('g', { transform: 'translate(250,520) rotate(-20)' }, F.s);
  svg('ellipse', { cx: 0, cy: 0, rx: 34, ry: 12, fill: '#c9b48e', stroke: INK, 'stroke-width': 3 }, gk);
  svg('circle', { cx: 38, cy: -2, r: 12, fill: '#c9b48e', stroke: INK, 'stroke-width': 3 }, gk);
  svg('circle', { cx: 44, cy: -6, r: 2.6, fill: INK }, gk);
  for (const [lx, ly, a] of [[18, -8, -60], [18, 8, 60], [-18, -8, -120], [-18, 8, 120]]) svg('path', { d: `M${lx},${ly} l${(Math.cos(rad(a)) * 18).toFixed(1)},${(Math.sin(rad(a)) * 18).toFixed(1)}`, stroke: '#c9b48e', 'stroke-width': 6, 'stroke-linecap': 'round' }, gk);
  const gtail = svg('path', { fill: 'none', stroke: '#c9b48e', 'stroke-width': 8, 'stroke-linecap': 'round' }, gk);
  // tiles + doormat
  svg('rect', { x: -300, y: 1380, width: 1680, height: 1000, fill: lin(M.defs, [[0, '#b86a4a'], [1, '#7a3e2c']]) }, M.s);
  for (let y = 1380, k = 0; y < 2300; y += 56 + k * 16, k++) svg('rect', { x: -300, y, width: 1680, height: 3, fill: '#5a2a1c', opacity: 0.5 }, M.s);
  for (let i = -6; i < 22; i++) svg('path', { d: `M${540 + (i * 90 - 540)},1380 L${540 + (i * 90 - 540) * 2.4},2300`, stroke: '#5a2a1c', 'stroke-width': 3, opacity: 0.4 }, M.s);
  svg('rect', { x: -300, y: 1368, width: 1680, height: 14, fill: '#6a7a5a', stroke: INK, 'stroke-width': 3 }, M.s);
  wallAO(M.s, M.defs, 1370, { op: 0.32 });
  const beam = lightShaft(M.s, M.defs, [[610, 1400], [960, 1400], [1200, 1900], [520, 1900]], '#cfe0ff', 0.22, 31, 18);
  svg('path', { d: 'M560,1470 L1000,1470 L1050,1560 L520,1560 Z', fill: '#6a7a4a', stroke: INK, 'stroke-width': 5 }, M.s);
  for (let k = 0; k < 9; k++) svg('path', { d: `M${580 + k * 50},1476 L${570 + k * 54},1554`, stroke: '#566440', 'stroke-width': 4 }, M.s);
  // ฝ้าย's sneakers (new, white) and mom's slippers (wired), side by side on the tiles
  const sn = svg('g', { transform: 'translate(250,1640)' }, M.s);
  for (const dx of [-70, 70]) {
    svg('ellipse', { cx: dx, cy: 30, rx: 66, ry: 14, fill: '#000', opacity: 0.25 }, sn);
    svg('path', { d: `M${dx - 60},20 Q${dx - 62},-30 ${dx - 20},-34 L${dx + 10},-10 Q${dx + 56},-4 ${dx + 62},18 L${dx + 62},28 L${dx - 60},28 Z`, fill: '#fbf8f1', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, sn);
    svg('path', { d: `M${dx - 60},22 L${dx + 62},22`, stroke: '#4a7bd8', 'stroke-width': 6 }, sn);
    svg('path', { d: `M${dx - 22},-26 L${dx + 4},-12 M${dx - 14},-30 L${dx + 10},-16`, stroke: '#9aa3b2', 'stroke-width': 4 }, sn);
  }
  slipper3q(M.s, 650, 1650, 1.25, { old: true, flip: true });
  slipper3q(M.s, 800, 1666, 1.25, { old: true });
  const glint = svg('g', { opacity: 0 }, M.s);
  for (const [gx, gy] of [[680, 1604], [772, 1620]]) { svg('path', { d: `M${gx},${gy - 18} L${gx + 4},${gy - 4} L${gx + 18},${gy} L${gx + 4},${gy + 4} L${gx},${gy + 18} L${gx - 4},${gy + 4} L${gx - 18},${gy} L${gx - 4},${gy - 4} Z`, fill: '#ffffff' }, glint); }
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.55);
  return {
    top, glint,
    update(t, tGlint = 99) {
      beam(t);
      gtail.setAttribute('d', `M-32,0 Q-60,${(10 * Math.sin(t * 1.6)).toFixed(1)} -84,${(4 * Math.sin(t * 1.6 + 1)).toFixed(1)}`);
      const k = t - tGlint; glint.setAttribute('opacity', k > 0 && k < 1.4 ? (Math.max(0, Math.sin(k * 7)) * (1 - k / 1.4)).toFixed(2) : 0);
    },
  };
}
