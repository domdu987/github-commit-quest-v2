// "720 มื้อ ที่ครูซื้อเกิน" cast: ครูสมศรี twenty years ago (short side-parted hair with a grey streak, red-framed glasses,
// pink floral blouse, long plum skirt, a wristwatch); the boy she fed (ป.4, spiky hair, a greying school shirt with a blue
// name stitched on the pocket, navy shorts with a patch, rubber sandals), the same boy now a teacher (side part, khaki
// government-teacher uniform with a lanyard), and the girl at the back of his class (long hair, mint clip, white school
// blouse, navy pleated skirt, white socks). Props: drinking-water bottle, Thai takeaway bags of rice and curry tied with
// rubber bands (with steam), a plastic spoon.
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);

const KRU14 = { skin: '#d39a70', skinShade: '#b8805a', hair: '#33221e', gray: '#a8a098', hairStyle: 'part', glasses: '#c8343c', lashes: true, lips: '#b5434e',
  top: 'blouse', sleeve: 'short', shirt: '#f7c6c0', shirtDark: '#e2a9a2', shirtLight: '#fde0dc', flower: '#ffffff', pants: '#d39a70', pantsDark: '#b8805a',
  shoeStyle: 'sneaker', shoe: '#3a2a2e', shoeDark: '#2a1e22', sole: '#3a2a2e', seed: 141 };
const BOY14 = { skin: '#c99068', skinShade: '#ad7650', hair: '#1e1a1a', hairStyle: 'spiky', top: 'tee', sleeve: 'short',
  shirt: '#eeeae0', shirtDark: '#d6d0c2', shirtLight: '#f8f6f0', pants: '#2a3a6e', pantsDark: '#22305a', shorts: true, shoeStyle: 'sandal', sole: '#3a3a3a', s: 0.8, seed: 143 };
const KRUMAN14 = { skin: '#c99068', skinShade: '#ad7650', hair: '#1e1a1a', hairStyle: 'part', top: 'office', lanyard: '#2f6fd0', sleeve: 'short',
  shirt: '#c8b07a', shirtDark: '#a8925e', shirtLight: '#dcc896', pants: '#b8a06a', pantsDark: '#9e8858', shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#2b2326', seed: 145 };
const GIRL14 = { skin: '#efc4a2', skinShade: '#d6a684', hair: '#2a1c18', hairStyle: 'long', clip: '#7fc6a8', lashes: true, top: 'tee', sleeve: 'short',
  shirt: '#fbf9f4', shirtDark: '#e2ddd2', shirtLight: '#ffffff', pants: '#efc4a2', pantsDark: '#d6a684', shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#f4f1ea', s: 0.78, seed: 147 };
const KIDS14 = [   // classmates passing outside / in the lunch rush
  { hair: '#1e1a1a', hairStyle: 'spiky', skin: '#d9a07a' }, { hair: '#2a1c18', hairStyle: 'bob', skin: '#efc4a2', clip: '#ff9fc0' },
  { hair: '#2a1f1c', hairStyle: 'dad', skin: '#c99068' }, { hair: '#3b2620', hairStyle: 'pony', skin: '#e2b08a', clip: '#f2c14e' },
].map((o, i) => Object.assign({ top: 'tee', sleeve: 'short', shirt: '#fbf9f4', shirtDark: '#e2ddd2', shirtLight: '#ffffff', pants: '#2a3a6e', pantsDark: '#22305a', shorts: true, shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#f4f1ea', s: 0.78, seed: 151 + i * 2 }, o));

// ---------------- world-space helpers ----------------
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
const wristFW = (pup, p) => pupW(pup, p, pup.wristF[0], pup.wristF[1]);
const wristBW = (pup, p) => pupW(pup, p, pup.wristB[0], pup.wristB[1]);
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);
const torsoT = (p, x, y) => { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; };
const f2 = q => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;

// ---------------- wardrobe overlays ----------------
// a skirt over the thighs (follows the hip and both thighs); o.pleats draws pleat lines
function skirt14(pup, fill, o = {}) {
  const g = svg('g', {});
  pup.g.insertBefore(g, pup.gTorso);
  const body = svg('path', { fill, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  const pl = o.pleats ? svg('path', { fill: 'none', stroke: shade(fill, -22), 'stroke-width': 3, 'stroke-linecap': 'round' }, g) : null;
  const len = o.len ?? 0.86, half = o.half ?? 31;
  return p => {
    const a = rad(p.torso || 0), hipY = -4;
    const th = (ang, off) => { const hx = off * Math.cos(a) - hipY * Math.sin(a), hy = off * Math.sin(a) + hipY * Math.cos(a); return [hx + Math.cos(rad(ang)) * RIG.THIGH * len, hy + Math.sin(rad(ang)) * RIG.THIGH * len]; };
    const lF = (p.lF || [90, 90])[0], lB = (p.lB || [90, 90])[0];
    const seated = Math.abs((lF + lB) / 2 - 90) > 45, L2 = seated ? Math.min(len, 1.05) : len;
    const th2 = (ang, off) => { const hx = off * Math.cos(a) - hipY * Math.sin(a), hy = off * Math.sin(a) + hipY * Math.cos(a); return [hx + Math.cos(rad(ang)) * RIG.THIGH * L2, hy + Math.sin(rad(ang)) * RIG.THIGH * L2]; };
    const kF = th2(lF, 8), kB = th2(lB, -8), hc = [(kF[0] + kB[0]) / 2, (kF[1] + kB[1]) / 2];
    const da = rad((lF + lB) / 2), n = [-Math.sin(da), Math.cos(da)];
    const spread = Math.min(16, Math.hypot(kF[0] - kB[0], kF[1] - kB[1]) * 0.5), w = half + spread;
    const P = (x, y) => torsoT(p, x, y), wb = P(-42, -16), wf = P(37, -16);
    const h1 = [hc[0] - n[0] * w, hc[1] - n[1] * w], h2 = [hc[0] + n[0] * w, hc[1] + n[1] * w];
    body.setAttribute('d', `M${f2(wb)} L${f2(wf)} Q${f2(P(40, 20))} ${f2(h1)} L${f2(h2)} Q${f2(P(-44, 20))} ${f2(wb)} Z`);
    if (pl) { let d = ''; for (const u of [0.25, 0.5, 0.75]) { const t0 = [wb[0] + (wf[0] - wb[0]) * u, wb[1] + (wf[1] - wb[1]) * u], t1 = [h2[0] + (h1[0] - h2[0]) * u, h2[1] + (h1[1] - h2[1]) * u]; d += `M${f2([t0[0] + (t1[0] - t0[0]) * 0.2, t0[1] + (t1[1] - t0[1]) * 0.2])} L${f2(t1)} `; } pl.setAttribute('d', d); }
  };
}
// school shirt details: collar flaps, a pocket with a stitched blue name, an optional bow
function schoolShirt14(pup, o = {}) {
  const g = svg('g', {}), T = RIG.T, top = -T;
  pup.gTorso.insertBefore(g, pup.shoulderG);
  const flaps = svg('path', { fill: pup.o.shirtLight, stroke: INK, 'stroke-width': 3.2, 'stroke-linejoin': 'round' }, g);
  const pocket = svg('path', { fill: 'none', stroke: pup.o.shirtDark, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  const name = svg('path', { fill: 'none', stroke: o.name || '#2f5fb8', 'stroke-width': 2.6, 'stroke-linecap': 'round' }, g);
  const tie = o.bow ? svg('path', { fill: o.bow, stroke: INK, 'stroke-width': 2.6, 'stroke-linejoin': 'round' }, g) : null;
  return p => {
    const P = (x, y) => torsoT(p, x, y);
    flaps.setAttribute('d', `M${f2(P(-8, top + 2))} L${f2(P(10, top + 20))} L${f2(P(13, top + 3))} Z M${f2(P(13, top + 3))} L${f2(P(26, top + 18))} L${f2(P(29, top + 3))} Z`);
    pocket.setAttribute('d', `M${f2(P(-30, top + 34))} L${f2(P(-10, top + 34))} L${f2(P(-10, top + 56))} L${f2(P(-30, top + 56))} Z`);
    name.setAttribute('d', `M${f2(P(-28, top + 28))} q4,-3 8,0 q4,3 8,0`);
    if (tie) tie.setAttribute('d', `M${f2(P(13, top + 10))} L${f2(P(4, top + 4))} L${f2(P(4, top + 18))} Z M${f2(P(13, top + 10))} L${f2(P(22, top + 4))} L${f2(P(22, top + 18))} Z`);
  };
}

// ---------------- props ----------------
function bottle14(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  svg('path', { d: 'M-11,-30 L11,-30 L13,-22 L13,30 Q13,36 7,36 L-7,36 Q-13,36 -13,30 L-13,-22 Z', fill: '#dff2ff', 'fill-opacity': 0.92, stroke: INK, 'stroke-width': 3 }, g);
  svg('rect', { x: -7, y: -40, width: 14, height: 11, rx: 3, fill: '#4a7bd8', stroke: INK, 'stroke-width': 2.5 }, g);
  svg('rect', { x: -13, y: -2, width: 26, height: 14, fill: '#7fc6a8', stroke: INK, 'stroke-width': 2 }, g);
  svg('path', { d: 'M-7,-18 L-7,-8', stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0.8 }, g);
  return g;
}
// a Thai takeaway bag (clear plastic, knotted with a rubber band): kind 'rice' (white grains) or curry colour; bottom-centred
function foodBag14(parent, c = 'rice', s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  const fill = c === 'rice' ? '#fbf7ec' : c;
  svg('path', { d: 'M-22,0 Q-30,-20 -18,-34 L-8,-44 L8,-44 L18,-34 Q30,-20 22,0 Q0,8 -22,0 Z', fill, stroke: INK, 'stroke-width': 3.2, 'stroke-linejoin': 'round' }, g);
  if (c === 'rice') for (const [x, y] of [[-10, -14], [4, -20], [10, -8], [-4, -26], [-14, -6]]) svg('ellipse', { cx: x, cy: y, rx: 3, ry: 1.6, fill: '#e8e0cc' }, g);
  else svg('path', { d: 'M-20,-12 Q0,-18 20,-12', fill: 'none', stroke: shade(c, -20), 'stroke-width': 2.5 }, g);
  svg('path', { d: 'M-12,-38 Q-20,-30 -16,-16', fill: 'none', stroke: '#ffffff', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0.7 }, g);
  svg('path', { d: 'M-8,-44 L-12,-58 L-2,-50 L2,-60 L8,-44', fill: '#f4f6f8', 'fill-opacity': 0.8, stroke: INK, 'stroke-width': 2.6, 'stroke-linejoin': 'round' }, g);   // twisted top
  svg('ellipse', { cx: 0, cy: -46, rx: 9, ry: 3.5, fill: 'none', stroke: '#c8343c', 'stroke-width': 3 }, g);   // rubber band
  return g;
}
// two bags hanging from a finger (rice + curry), swinging; returns { g, update(t) }
function bagPair14(parent, s = 1) {
  const g = svg('g', {}, parent), a = svg('g', {}, g), b = svg('g', {}, g);
  foodBag14(a, 'rice', s); foodBag14(b, '#e88a3a', s * 0.92);
  return { g, update(t) { a.setAttribute('transform', `translate(-10,${58 * s}) rotate(${(Math.sin(t * 6) * 5).toFixed(1)} 0 ${-58 * s})`); b.setAttribute('transform', `translate(14,${54 * s}) rotate(${(Math.sin(t * 6 + 1) * 6).toFixed(1)} 0 ${-54 * s})`); } };
}
// wisps of steam rising from a point (world): update(x, y, t, k)
function steam14(parent, n = 3) {
  const w = Array.from({ length: n }, () => svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linecap': 'round' }, parent));
  return (x, y, t, k = 1) => w.forEach((e, i) => { const u = ((t * 0.7 + i / n) % 1); e.setAttribute('d', `M${(x - 10 + i * 10).toFixed(1)},${(y - u * 60).toFixed(1)} q8,-10 0,-20 q-8,-10 0,-20`); e.setAttribute('opacity', (k * 0.45 * Math.sin(Math.PI * u)).toFixed(2)); });
}

// ---------------- front faces (avatars, end card) ----------------
function faceKru14(parent, cx, cy, r) {
  const c = KRU14, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 1.0},${r * 0.1} C${-r * 1.1},${-r * 1.15} ${r * 1.1},${-r * 1.15} ${r * 1.0},${r * 0.1} Q${r * 0.92},${-r * 0.5} ${r * 0.1},${-r * 0.56} Q${-r * 0.2},${-r * 0.9} ${-r * 0.5},${-r * 0.5} Q${-r * 0.92},${-r * 0.4} ${-r * 1.0},${r * 0.1} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('path', { d: `M${r * 0.1},${-r * 0.9} Q${r * 0.5},${-r * 0.82} ${r * 0.8},${-r * 0.4}`, fill: 'none', stroke: c.gray, 'stroke-width': r * 0.1, 'stroke-linecap': 'round' }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.12},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.12},${r * 0.04}` }, g);
    svg('circle', { cx: sx * r * 0.38, cy: r * 0.0, r: r * 0.24, fill: 'none', stroke: c.glasses, 'stroke-width': r * 0.06 }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.34, rx: r * 0.14, ry: r * 0.08, fill: '#f0857f', opacity: 0.5 }, g);
  }
  svg('path', { d: `M${-r * 0.14},0 L${r * 0.14},0`, stroke: c.glasses, 'stroke-width': r * 0.06 }, g);
  svg('path', { fill: '#b5434e', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.2},${r * 0.44} Q0,${r * 0.68} ${r * 0.2},${r * 0.44} Z` }, g);
  return g;
}
function faceMan14(parent, cx, cy, r) {
  const c = KRUMAN14, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 1.0},${r * 0.05} C${-r * 1.1},${-r * 1.2} ${r * 1.1},${-r * 1.2} ${r * 1.0},${r * 0.05} Q${r * 0.9},${-r * 0.52} ${r * 0.2},${-r * 0.6} Q${-r * 0.1},${-r * 0.8} ${-r * 0.4},${-r * 0.56} Q${-r * 0.9},${-r * 0.42} ${-r * 1.0},${r * 0.05} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.08, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.26} Q${sx * r * 0.38},${-r * 0.34} ${sx * r * 0.56},${-r * 0.26}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.12},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.12},${r * 0.04}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.32, rx: r * 0.13, ry: r * 0.07, fill: '#f0857f', opacity: 0.4 }, g);
  }
  svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.42} Q0,${r * 0.7} ${r * 0.22},${r * 0.42} Z` }, g);
  return g;
}
function av14(who, n = 64) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: who === 'kru' ? '#ffe2d6' : '#f6ecd0' }, d);
  if (who === 'kru') { svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: KRU14.shirt, stroke: INK, 'stroke-width': 2.5 }, d); faceKru14(d, 0, 2, 24); }
  else { svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: KRUMAN14.shirt, stroke: INK, 'stroke-width': 2.5 }, d); svg('path', { d: 'M-8,30 L0,40 L8,30', fill: 'none', stroke: KRUMAN14.shirtDark, 'stroke-width': 3 }, d); faceMan14(d, 0, 2, 24); }
  return d.outerHTML;
}
