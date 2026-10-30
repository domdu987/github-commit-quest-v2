// "8 ซอง ที่อาม่าไม่เคยแกะ" cast: อาม่า today (white bun with a jade-beaded pin, fair skin, a burgundy silk blouse with a
// mandarin collar and gold frog buttons, black trousers, cloth slippers, a jade bangle), อาม่า eight years ago (grey bun),
// อาม่า twenty-three years ago (dark bun with grey streaks, ivory floral blouse); her grandson as a seven-year-old (bowl cut,
// red mandarin shirt for ตรุษจีน, shorts, sandals), at 22 on his first salary (white shirt, navy tie), through the years
// (a shirt a year) and today (black round glasses, brick-red hoodie, jeans). Props: the red envelopes (gold coin
// medallion, sealed flap, the year in อาม่า's hand), the old blue cookie tin, a mesh bag of mandarins, a clay tea set,
// an office box, a phone seen from the back.
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);

const AMA15 = { skin: '#f0cba8', skinShade: '#d6ab86', hair: '#ece8e2', gray: '#fbf9f6', hairStyle: 'bun', aged: true, lips: '#a8445a',
  top: 'blouse', sleeve: 'long', shirt: '#a82a35', shirtDark: '#86202a', shirtLight: '#c23e48', flower: '#e8b04a',
  pants: '#2a2228', pantsDark: '#201a20', shoeStyle: 'sneaker', shoe: '#2a2228', shoeDark: '#201a20', sole: '#2a2228', seed: 151 };
const AMA15_B = Object.assign({}, AMA15, { hair: '#bdb6ae', gray: '#e2ddd6', seed: 153 });   // eight years ago
const AMA15_Y = Object.assign({}, AMA15, { hair: '#4a3c38', gray: '#a8a098', aged: false, shirt: '#ede2cc', shirtDark: '#d6c8ac', shirtLight: '#f8f0e0', flower: '#c8343c',
  pants: '#3a3040', pantsDark: '#2e2634', seed: 155 });                                       // twenty-three years ago
const LUK15 = { skin: '#f2cca6', skinShade: '#d8ae86', hair: '#1c1818', hairStyle: 'spiky', glasses: '#2a2228', top: 'hoodie', sleeve: 'long',
  shirt: '#b8402f', shirtDark: '#963022', shirtLight: '#cf5a44', pants: '#2f3a5c', pantsDark: '#262f4c', shoeStyle: 'sneaker', shoe: '#f4efe6', shoeDark: '#d6cfc2', sole: '#b8402f', seed: 157 };
const LUK15_W = Object.assign({}, LUK15, { top: 'office', sleeve: 'short', tie: '#2f4f8a', shirt: '#f6f5f0', shirtDark: '#dcdad2', shirtLight: '#ffffff',
  pants: '#3a3a48', pantsDark: '#2e2e3a', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#2b2326', seed: 159 });   // the first salary
// a shirt a year through the time-lapse
const LUK15_T = [['#f6f5f0', '#2f4f8a'], ['#9cc0e4', null], ['#e8c070', '#8e2a3c'], ['#86b886', null]].map(([c, tie], i) =>
  Object.assign({}, LUK15_W, { shirt: c, shirtDark: shade(c, -22), shirtLight: shade(c, 18), tie, seed: 161 + i * 2 }));
const KID15 = { skin: '#f2cca6', skinShade: '#d8ae86', hair: '#1c1818', hairStyle: 'fluffy', top: 'tee', sleeve: 'short',
  shirt: '#d0343c', shirtDark: '#ac2830', shirtLight: '#e24a50', pants: '#2a2a3a', pantsDark: '#22222e', shorts: true, shoeStyle: 'sandal', sole: '#c8343c', s: 0.72, seed: 169 };

// ---------------- world-space helpers ----------------
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
const wristFW = (pup, p) => pupW(pup, p, pup.wristF[0], pup.wristF[1]);
const wristBW = (pup, p) => pupW(pup, p, pup.wristB[0], pup.wristB[1]);
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);
const torsoT = (p, x, y) => { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; };
const f2 = q => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;

// ---------------- wardrobe overlays ----------------
// a mandarin collar, the diagonal placket and gold frog buttons over the shirt (อาม่า's blouse, the boy's ตรุษจีน shirt)
function mandarin15(pup, o = {}) {
  const g = svg('g', {}), top = -RIG.T, trim = o.trim || '#e8b04a';
  pup.gTorso.insertBefore(g, pup.shoulderG);
  const collar = svg('path', { fill: o.collar || pup.o.shirtDark, stroke: INK, 'stroke-width': 3.4, 'stroke-linejoin': 'round' }, g);
  const plk = svg('path', { fill: 'none', stroke: trim, 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
  const btn = [0, 1, 2, 3].map(() => [svg('path', { fill: 'none', stroke: trim, 'stroke-width': 3.4, 'stroke-linecap': 'round' }, g), svg('circle', { r: 4.2, fill: trim, stroke: INK, 'stroke-width': 1.8 }, g)]);
  const hem = o.hem ? svg('path', { fill: 'none', stroke: trim, 'stroke-width': 3.5, 'stroke-linecap': 'round', opacity: 0.85 }, g) : null;
  return p => {
    const P = (x, y) => torsoT(p, x, y);
    collar.setAttribute('d', `M${f2(P(-10, top + 6))} Q${f2(P(10, top + 13))} ${f2(P(32, top + 6))} L${f2(P(32, top - 5))} Q${f2(P(10, top + 1))} ${f2(P(-10, top - 6))} Z`);
    plk.setAttribute('d', `M${f2(P(16, top + 10))} Q${f2(P(26, top + 20))} ${f2(P(36, top + 34))} L${f2(P(35, -12))}`);
    [[24, top + 20], [35, top + 42], [35, top + 66], [35, top + 90]].forEach(([x, y], i) => { btn[i][0].setAttribute('d', `M${f2(P(x - 9, y))} L${f2(P(x + 7, y))}`); btn[i][1].setAttribute('cx', P(x - 1, y)[0].toFixed(1)); btn[i][1].setAttribute('cy', P(x - 1, y)[1].toFixed(1)); });
    if (hem) hem.setAttribute('d', `M${f2(P(-42, -8))} Q${f2(P(0, -2))} ${f2(P(38, -8))}`);
  };
}
// a jade bead on the bun's pin and a jade bangle on the front wrist; returns update(p) (call after pose)
function jade15(pup) {
  const R = pup.o.R;
  svg('circle', { cx: -R * 1.2, cy: -R * 0.48, r: 7, fill: '#5fb08a', stroke: INK, 'stroke-width': 3 }, pup.head);
  svg('circle', { cx: -R * 1.22, cy: -R * 0.5, r: 2.4, fill: '#d8f4e6' }, pup.head);
  const b = svg('ellipse', { rx: 6, ry: 14, fill: 'none', stroke: '#4f9e7a', 'stroke-width': 6 }, pup.gArmF);
  const bh = svg('ellipse', { rx: 6, ry: 14, fill: 'none', stroke: '#bfe8d2', 'stroke-width': 2, opacity: 0.7 }, pup.gArmF);
  pup.gArmF.insertBefore(b, pup.hF); pup.gArmF.insertBefore(bh, pup.hF);
  return p => {
    const a = rad((p.aF || [90, 90])[1]), [wx, wy] = pup.wristF, x = wx - Math.cos(a) * 16, y = wy - Math.sin(a) * 16, r = `rotate(${((p.aF || [90, 90])[1]).toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})`;
    for (const e of [b, bh]) setA(e, { cx: x.toFixed(1), cy: y.toFixed(1), transform: r });
  };
}

// ---------------- props ----------------
// a red envelope (อั่งเปา), upright, bottom-centred: gold border, a gold coin medallion, the sealed flap, the year in
// อาม่า's blue biro; o.thick puffs it (more notes inside), o.flat = empty
function angpao15(parent, s = 1, o = {}) {
  const g = svg('g', { transform: `scale(${s})` }, parent), w = 46, h = 72, th = o.thick ?? 0;
  if (th > 0) svg('rect', { x: -w / 2 + 4, y: -h - 2, width: w, height: h, rx: 4, fill: '#8e1e26', stroke: INK, 'stroke-width': 3 }, g);   // a fat envelope shows its side
  svg('rect', { x: -w / 2, y: -h, width: w, height: h, rx: 4, fill: o.flat ? '#c23a42' : '#d43a40', stroke: INK, 'stroke-width': 3.2 }, g);
  svg('rect', { x: -w / 2 + 5, y: -h + 5, width: w - 10, height: h - 10, rx: 2, fill: 'none', stroke: '#f2c14e', 'stroke-width': 2 }, g);
  svg('path', { d: `M${-w / 2},${-h + 2} L0,${-h + 22} L${w / 2},${-h + 2}`, fill: 'none', stroke: '#8e1e26', 'stroke-width': 2.6, 'stroke-linejoin': 'round' }, g);   // the flap
  svg('circle', { cx: 0, cy: -h + 22, r: 5, fill: '#f2c14e', stroke: '#a8781e', 'stroke-width': 1.6 }, g);   // the seal
  svg('circle', { cx: 0, cy: -h / 2 + 6, r: 11, fill: '#f2c14e', stroke: '#a8781e', 'stroke-width': 2 }, g);
  svg('rect', { x: -3.5, y: -h / 2 + 2.5, width: 7, height: 7, fill: '#d43a40' }, g);
  if (th > 0) svg('path', { d: `M${-w / 2 + 4},-6 Q0,${-2 + th * 4} ${w / 2 - 4},-6`, fill: 'none', stroke: '#ff8a80', 'stroke-width': 2, opacity: 0.6 }, g);
  if (o.year) { const t = svg('text', { x: 0, y: -10, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 13, fill: '#1e3a8a', transform: 'rotate(-4)' }, g); t.textContent = o.year; }
  return g;
}
// the old cookie tin (side view, bottom-centred): royal blue with a gold rim and a painted band; lid() lifts it
function tin15(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent), W = 58, H = 40;
  const back = svg('g', {}, g), inside = svg('g', {}, g), front = svg('g', {}, g), lid = svg('g', {}, g);
  svg('ellipse', { cx: 0, cy: -H, rx: W, ry: 13, fill: '#1e2c5a', stroke: INK, 'stroke-width': 3.5 }, back);
  svg('path', { d: `M${-W},${-H} L${-W},0 Q0,16 ${W},0 L${W},${-H} Q0,${-H + 14} ${-W},${-H} Z`, fill: '#2f4fa0', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, front);
  svg('path', { d: `M${-W},${-H + 14} Q0,${-H + 28} ${W},${-H + 14} L${W},${-H + 26} Q0,${-H + 40} ${-W},${-H + 26} Z`, fill: '#f2e6c8', opacity: 0.9 }, front);
  for (let k = -3; k <= 3; k++) svg('circle', { cx: k * 15, cy: -H + 21 + 6 * Math.cos(k * 0.45), r: 3.5, fill: '#2f4fa0' }, front);
  svg('path', { d: `M${-W + 8},${-H + 4} L${-W + 8},-6`, stroke: '#7f9ce0', 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.6 }, front);
  svg('ellipse', { cx: 0, cy: -H - 4, rx: W + 3, ry: 14, fill: '#2f4fa0', stroke: INK, 'stroke-width': 3.5 }, lid);
  svg('path', { d: `M${-W - 3},${-H - 4} L${-W - 3},${-H + 4} Q0,${-H + 20} ${W + 3},${-H + 4} L${W + 3},${-H - 4}`, fill: '#26408a', stroke: INK, 'stroke-width': 3.5 }, lid);
  svg('ellipse', { cx: 0, cy: -H - 5, rx: W - 12, ry: 8, fill: 'none', stroke: '#e8b04a', 'stroke-width': 3 }, lid);
  svg('ellipse', { cx: -14, cy: -H - 8, rx: 16, ry: 4, fill: '#ffffff', opacity: 0.3 }, lid);
  const env = [0, 1, 2].map(i => { const e = svg('g', { transform: `translate(${-18 + i * 18},${-H + 6}) rotate(${-8 + i * 8})` }, inside); angpao15(e, 0.7); return e; });
  return {
    g, lid, inside, set(open, n = 3) {   // open 0..1: the lid lifts up and over to the right
      lid.setAttribute('transform', `translate(${(open * 60).toFixed(1)},${(-open * 26).toFixed(1)}) rotate(${(open * 20).toFixed(1)} 0 ${-H})`);
      lid.setAttribute('display', open > 0.7 ? 'none' : 'inline');   // set down beside her, below the table
      inside.setAttribute('display', open > 0.05 && n > 0 ? 'inline' : 'none');
      env.forEach((e, i) => e.setAttribute('display', i < n ? 'inline' : 'none'));
    },
  };
}
// a red mesh bag of mandarins hanging from a hand (handle at 0,0); returns { g, update(t) }
function oranges15(parent, s = 1) {
  const g = svg('g', {}, parent), b = svg('g', {}, g);
  svg('path', { d: 'M-14,0 Q0,-14 14,0', fill: 'none', stroke: '#d43a40', 'stroke-width': 4 }, b);
  for (const [x, y, r] of [[-16, 30, 15], [14, 30, 15], [0, 50, 16], [-18, 58, 14], [18, 58, 14], [0, 22, 13]]) {
    svg('circle', { cx: x, cy: y, r, fill: '#f29a2e', stroke: INK, 'stroke-width': 3 }, b);
    svg('circle', { cx: x - r * 0.35, cy: y - r * 0.35, r: r * 0.25, fill: '#ffd28a', opacity: 0.8 }, b);
  }
  svg('path', { d: 'M-30,14 L30,14 L32,70 Q0,84 -32,70 Z', fill: 'none', stroke: '#d43a40', 'stroke-width': 2.4, 'stroke-dasharray': '6 5', opacity: 0.9 }, b);
  svg('path', { d: 'M-10,16 L-20,74 M10,16 L20,74 M-30,44 L30,44', stroke: '#d43a40', 'stroke-width': 2, opacity: 0.6 }, b);
  svg('path', { d: 'M-4,12 q4,-8 10,-6', fill: 'none', stroke: '#3f8a52', 'stroke-width': 4, 'stroke-linecap': 'round' }, b);
  return { g, update(t, swing = 1) { b.setAttribute('transform', `scale(${s}) rotate(${(Math.sin(t * 6) * 5 * swing).toFixed(1)})`); } };
}
// the bag set down (bottom-centred)
function orangesDown15(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  for (const [x, y, r] of [[-22, -16, 16], [10, -16, 16], [34, -14, 14], [-6, -38, 15], [22, -38, 14]]) {
    svg('circle', { cx: x, cy: y, r, fill: '#f29a2e', stroke: INK, 'stroke-width': 3 }, g);
    svg('circle', { cx: x - r * 0.35, cy: y - r * 0.35, r: r * 0.25, fill: '#ffd28a', opacity: 0.8 }, g);
  }
  svg('path', { d: 'M-40,-4 Q6,6 50,-4 L44,-40 Q6,-60 -36,-40 Z', fill: 'none', stroke: '#d43a40', 'stroke-width': 2.4, 'stroke-dasharray': '6 5', opacity: 0.9 }, g);
  return g;
}
// a clay teapot and two tiny cups (on the table, bottom at 0)
function teaSet15(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  svg('path', { d: 'M-34,-26 Q-56,-30 -58,-44', fill: 'none', stroke: INK, 'stroke-width': 9, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M-34,-26 Q-56,-30 -58,-44', fill: 'none', stroke: '#9a4a2e', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M24,-34 Q46,-34 40,-14 Q36,-6 26,-10', fill: 'none', stroke: INK, 'stroke-width': 4 }, g);
  svg('path', { d: 'M-30,0 Q-40,-36 0,-44 Q40,-36 30,0 Z', fill: '#9a4a2e', stroke: INK, 'stroke-width': 3.5 }, g);
  svg('ellipse', { cx: 0, cy: -44, rx: 18, ry: 5, fill: '#7a3620', stroke: INK, 'stroke-width': 3 }, g);
  svg('circle', { cx: 0, cy: -52, r: 5, fill: '#7a3620', stroke: INK, 'stroke-width': 2.5 }, g);
  svg('path', { d: 'M-18,-30 Q-20,-14 -12,-6', fill: 'none', stroke: '#d08a60', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0.7 }, g);
  for (const x of [56, 86]) { svg('path', { d: `M${x - 10},-18 L${x + 10},-18 L${x + 7},0 L${x - 7},0 Z`, fill: '#f4efe6', stroke: INK, 'stroke-width': 3 }, g); svg('path', { d: `M${x - 9},-14 L${x + 9},-14`, stroke: '#2f4fa0', 'stroke-width': 2.5 }, g); }
  return g;
}
// wisps of steam rising from a point (world): update(x, y, t, k)
function steam15(parent, n = 3) {
  const w = Array.from({ length: n }, () => svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linecap': 'round' }, parent));
  return (x, y, t, k = 1) => w.forEach((e, i) => { const u = ((t * 0.7 + i / n) % 1); e.setAttribute('d', `M${(x - 8 + i * 8).toFixed(1)},${(y - u * 54).toFixed(1)} q7,-9 0,-18 q-7,-9 0,-18`); e.setAttribute('opacity', (k * 0.42 * Math.sin(Math.PI * u)).toFixed(2)); });
}
// a cardboard box of office things (a plant, a mug, a frame), carried in front (bottom-centred)
function officeBox15(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  svg('path', { d: 'M-12,-74 Q-30,-120 -6,-140 M-6,-80 Q6,-130 28,-136 M-2,-78 Q-2,-110 -20,-150', fill: 'none', stroke: '#4f9e5e', 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
  for (const [x, y, a] of [[-24, -140, -30], [28, -136, 30], [-20, -152, -10]]) svg('ellipse', { cx: x, cy: y, rx: 14, ry: 7, fill: '#5aae68', stroke: INK, 'stroke-width': 2.5, transform: `rotate(${a} ${x} ${y})` }, g);
  svg('rect', { x: 20, y: -104, width: 34, height: 40, rx: 4, fill: '#e8a84a', stroke: INK, 'stroke-width': 3, transform: 'rotate(10 37 -84)' }, g);
  svg('rect', { x: -56, y: -100, width: 30, height: 32, rx: 5, fill: '#f6efe2', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: 'M-70,-74 L70,-74 L64,0 L-64,0 Z', fill: '#c99a62', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M-70,-74 L-88,-96 L-56,-96 L-40,-74 M70,-74 L88,-96 L56,-96 L40,-74', fill: '#b8884e', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  svg('rect', { x: -26, y: -50, width: 52, height: 20, rx: 3, fill: '#f6efe2', stroke: INK, 'stroke-width': 2.5 }, g);
  svg('path', { d: 'M-18,-40 L18,-40', stroke: '#8a847c', 'stroke-width': 3 }, g);
  return g;
}
// a phone seen from the back: case, camera, a sliver of screen light on the edge
function phone15(parent) {
  const g = svg('g', {}, parent);
  svg('rect', { x: -15, y: -46, width: 30, height: 60, rx: 7, fill: '#3a2e40', stroke: INK, 'stroke-width': 3.5 }, g);
  svg('rect', { x: -9, y: -40, width: 12, height: 14, rx: 4, fill: '#20182a', stroke: '#6a5a72', 'stroke-width': 1.5 }, g);
  svg('circle', { cx: -3, cy: -33, r: 3, fill: '#4a5a8a' }, g);
  const glow = svg('rect', { x: 12, y: -44, width: 5, height: 56, rx: 2.5, fill: '#d8ecff', opacity: 0.9 }, g);
  return { g, glow };
}

// ---------------- front faces (avatars, end card) ----------------
function faceAma15(parent, cx, cy, r) {
  const c = AMA15, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { cx: 0, cy: -r * 1.02, r: r * 0.42, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);   // the bun on top
  svg('path', { d: `M${-r * 0.5},${-r * 1.2} L${r * 0.55},${-r * 0.9}`, stroke: '#e0a12c', 'stroke-width': r * 0.08, 'stroke-linecap': 'round' }, g);
  svg('circle', { cx: r * 0.6, cy: -r * 0.88, r: r * 0.1, fill: '#5fb08a', stroke: ink, 'stroke-width': r * 0.04 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 1.0},${r * 0.12} C${-r * 1.1},${-r * 1.15} ${r * 1.1},${-r * 1.15} ${r * 1.0},${r * 0.12} Q${r * 0.9},${-r * 0.56} ${r * 0.0},${-r * 0.62} Q${-r * 0.9},${-r * 0.56} ${-r * 1.0},${r * 0.12} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.12} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    svg('path', { fill: 'none', stroke: shade(c.skinShade, -18), 'stroke-width': r * 0.035, 'stroke-linecap': 'round', d: `M${sx * r * 0.62},${-r * 0.02} l${sx * r * 0.14},${-r * 0.06} M${sx * r * 0.62},${r * 0.08} l${sx * r * 0.15},${r * 0.02}` }, g);
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.34, rx: r * 0.15, ry: r * 0.08, fill: '#f0857f', opacity: 0.55 }, g);
  }
  svg('path', { fill: '#a8445a', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.44} Q0,${r * 0.7} ${r * 0.22},${r * 0.44} Z` }, g);
  return g;
}
function faceLuk15(parent, cx, cy, r) {
  const c = LUK15, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 1.0},${r * 0.0} C${-r * 1.1},${-r * 1.25} ${r * 1.1},${-r * 1.25} ${r * 1.0},${r * 0.0} L${r * 0.7},${-r * 0.52} L${r * 0.5},${-r * 0.36} L${r * 0.3},${-r * 0.6} L${r * 0.05},${-r * 0.4} L${-r * 0.2},${-r * 0.62} L${-r * 0.45},${-r * 0.4} L${-r * 0.7},${-r * 0.56} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round' }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.12},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.12},${r * 0.04}` }, g);
    svg('circle', { cx: sx * r * 0.38, cy: r * 0.0, r: r * 0.25, fill: '#ffffff', 'fill-opacity': 0.15, stroke: c.glasses, 'stroke-width': r * 0.07 }, g);
    svg('ellipse', { cx: sx * r * 0.64, cy: r * 0.36, rx: r * 0.13, ry: r * 0.07, fill: '#f0857f', opacity: 0.4 }, g);
  }
  svg('path', { d: `M${-r * 0.13},0 L${r * 0.13},0`, stroke: c.glasses, 'stroke-width': r * 0.06 }, g);
  svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.44} Q0,${r * 0.7} ${r * 0.22},${r * 0.44} Z` }, g);
  return g;
}
function av15(who, n = 64) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: who === 'ama' ? '#ffe2d6' : '#f6ecd0' }, d);
  if (who === 'ama') {
    svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: AMA15.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
    svg('path', { d: 'M-10,30 Q0,34 10,30 L10,26 Q0,30 -10,26 Z', fill: AMA15.shirtDark, stroke: INK, 'stroke-width': 1.5 }, d);
    for (const y of [36, 43]) svg('circle', { cx: 6, cy: y, r: 2.2, fill: '#e8b04a' }, d);
    faceAma15(d, 0, 4, 22);
  } else {
    svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: LUK15.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
    svg('path', { d: 'M-6,30 L-8,44 M6,30 L8,44', stroke: '#fff7ea', 'stroke-width': 2.5, 'stroke-linecap': 'round' }, d);
    faceLuk15(d, 0, 2, 24);
  }
  return d.outerHTML;
}
