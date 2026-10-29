// "15 ปีใหม่ ที่แม่อยู่บนรถทัวร์" cast: แม่, a tour-bus hostess in her forties (neat bun with a burgundy bow, burgundy
// uniform jacket over a white blouse, gold neck scarf and name tag, navy pencil skirt); her daughter now (long hair with
// a mustard clip, denim jacket, cap-and-mask disguise for the surprise) and as a girl in heart pyjamas (the flashback);
// ยาย in Ubon (white bun, cream blouse with purple flowers, a purple mudmee ซิ่น); the uncle in row 2, the driver, and
// a busload of New Year passengers (some in party hats).
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);

const MAE13 = { skin: '#d9a07a', skinShade: '#be845e', hair: '#2a1c1c', hairStyle: 'bun', lashes: true, lips: '#b5434e', top: 'tee', sleeve: 'long',
  shirt: '#8e2a3c', shirtDark: '#71202f', shirtLight: '#a8384c', pants: '#c98e6a', pantsDark: '#b07a58', shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#2b2326', seed: 131 };
const LUK13 = { skin: '#efc4a2', skinShade: '#d6a684', hair: '#3b2620', hairStyle: 'long', clip: '#f2c14e', lashes: true, lips: '#a8445a', top: 'tee', sleeve: 'long',
  shirt: '#4f74b0', shirtDark: '#3f5f96', shirtLight: '#6a8ccc', pants: '#2c2b3a', pantsDark: '#222130', shoeStyle: 'sneaker', shoe: '#f6f1e8', shoeDark: '#d9d2c4', sole: '#4f9e5e', seed: 133 };
const KID13 = { skin: '#efc4a2', skinShade: '#d6a684', hair: '#3b2620', hairStyle: 'pony', clip: '#ff7aa2', lashes: true, top: 'heartpj', sleeve: 'long',
  shirt: '#f9d4e0', shirtDark: '#e8b4c6', shirtLight: '#ffe6ee', print: '#e0577a', pants: '#f4c2d4', pantsDark: '#e0a8bc', shoeStyle: 'sandal', sole: '#e0577a', s: 0.8, seed: 135 };
const YAI13 = { skin: '#b98258', skinShade: '#9c6a44', hair: '#e6e0d8', gray: '#f4f0ea', hairStyle: 'bun', aged: true, top: 'blouse', sleeve: 'long',
  shirt: '#f3e6c8', shirtDark: '#dccaa4', shirtLight: '#fbf3de', flower: '#7a3f8e', pants: '#b98258', pantsDark: '#9c6a44', shoeStyle: 'sandal', sole: '#7a4a2a', seed: 137 };
const LUNG13 = { skin: '#c99068', skinShade: '#ad7650', hair: '#3a2a24', gray: '#a8a29a', hairStyle: 'dad', mustache: true, top: 'stripe', sleeve: 'short',
  shirt: '#efe1c0', shirtDark: '#d8c79e', shirtLight: '#f8eed6', stripe: '#b5443a', pants: '#4a4a5e', pantsDark: '#3a3a4c', shoeStyle: 'sneaker', shoe: '#5a4232', shoeDark: '#46321f', sole: '#2a2020', seed: 139 };
const DRIVER13 = { skin: '#c48a60', skinShade: '#a8714a', hair: '#2a201c', hairStyle: 'dad', hat: 'cap', capC: '#2b3a6b', top: 'office', tie: '#8e2a3c', sleeve: 'short',
  shirt: '#fbf7ee', shirtDark: '#e2d8c6', shirtLight: '#ffffff', pants: '#2b3050', pantsDark: '#22263f', shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#2b2326', seed: 141 };
// passengers in the rows (front to back); hat: a paper party hat colour
const PAX13 = [
  { o: { skin: '#e2b08a', hair: '#1e1a1a', hairStyle: 'spiky', top: 'hoodie', shirt: '#d9534f', shirtDark: '#b8433f', shirtLight: '#e8706a', seed: 151 }, hat: '#f2c14e' },
  { o: { skin: '#d9a07a', hair: '#2e2222', hairStyle: 'perm', top: 'blouse', shirt: '#f5c8d8', shirtDark: '#e2aec0', shirtLight: '#fbe0ea', flower: '#e0577a', seed: 153 } },
  { o: { skin: '#c99068', hair: '#2a1f1c', hairStyle: 'part', top: 'tee', shirt: '#4f9e8e', shirtDark: '#3e8476', shirtLight: '#69b8a8', seed: 155 }, hat: '#e0577a' },
  { o: { skin: '#b98258', hair: '#d8d2cc', gray: '#f0ece6', hairStyle: 'dad', aged: true, top: 'stripe', shirt: '#f2e8d4', stripe: '#3b4a7e', seed: 157 } },
  { o: { skin: '#efc4a2', hair: '#4a2e22', hairStyle: 'bob', clip: '#7fc6a8', top: 'tee', shirt: '#f2a03a', shirtDark: '#d8862a', shirtLight: '#f8b85a', seed: 159 }, hat: '#7fb069' },
  { o: { skin: '#d9a07a', hair: '#2a1c1c', hairStyle: 'wavy', top: 'tee', shirt: '#8a5fc8', shirtDark: '#7048aa', shirtLight: '#a07ad8', seed: 161 } },
];

// ---------------- world-space helpers ----------------
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
const wristFW = (pup, p) => pupW(pup, p, pup.wristF[0], pup.wristF[1]);
const wristBW = (pup, p) => pupW(pup, p, pup.wristB[0], pup.wristB[1]);
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);
const torsoT = (p, x, y) => { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; };
const f2 = q => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;

// ---------------- wardrobe overlays (drawn in the puppet's own frame; call upd(p) after pose) ----------------
// a jacket front over the torso: inner shirt V, lapels, buttons; o.scarf adds a knotted neck scarf, o.tag a name tag
function jacket13(pup, o = {}) {
  const g = svg('g', {}), T = RIG.T, top = -T;
  pup.gTorso.insertBefore(g, pup.shoulderG);
  const v = svg('path', { fill: o.inner || '#fbf6ee', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  const lapL = svg('path', { fill: o.lapel || shade(pup.o.shirt, -18), stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  const lapR = svg('path', { fill: o.lapel || shade(pup.o.shirt, -18), stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  const btn = [0, 1].map(() => svg('circle', { r: 3.4, fill: o.button || '#e8b13a', stroke: INK, 'stroke-width': 1.6 }, g));
  const pocket = o.pockets ? svg('path', { fill: 'none', stroke: shade(pup.o.shirt, -25), 'stroke-width': 3.5, 'stroke-linecap': 'round' }, g) : null;
  const tag = o.tag ? svg('g', {}, g) : null;
  if (tag) { svg('rect', { x: -9, y: -4, width: 18, height: 8, rx: 2, fill: '#f2d27a', stroke: INK, 'stroke-width': 1.6 }, tag); svg('path', { d: 'M-6,0 L6,0', stroke: '#8a5a2a', 'stroke-width': 1.4 }, tag); }
  const sc = o.scarf ? svg('g', {}, g) : null;
  let scK, scT1, scT2;
  if (sc) {
    scT1 = svg('path', { fill: o.scarf, stroke: INK, 'stroke-width': 2.6, 'stroke-linejoin': 'round' }, sc);
    scT2 = svg('path', { fill: shade(o.scarf, -14), stroke: INK, 'stroke-width': 2.6, 'stroke-linejoin': 'round' }, sc);
    scK = svg('ellipse', { rx: 7, ry: 5.5, fill: o.scarf, stroke: INK, 'stroke-width': 2.6 }, sc);
  }
  const upd = (p, t = 0) => {
    const P = (x, y) => torsoT(p, x, y);
    v.setAttribute('d', `M${f2(P(-4, top + 2))} L${f2(P(25, top + 2))} L${f2(P(13, top + 46))} Z`);
    lapL.setAttribute('d', `M${f2(P(-7, top + 1))} L${f2(P(12, top + 47))} L${f2(P(-3, top + 30))} Z`);
    lapR.setAttribute('d', `M${f2(P(28, top + 1))} L${f2(P(14, top + 47))} L${f2(P(31, top + 22))} Z`);
    btn.forEach((b, i) => { const q = P(14, top + 58 + i * 20); setA(b, { cx: q[0].toFixed(1), cy: q[1].toFixed(1) }); });
    if (pocket) pocket.setAttribute('d', `M${f2(P(-30, top + 40))} L${f2(P(-8, top + 40))} M${f2(P(-30, -26))} L${f2(P(-6, -26))}`);
    if (tag) { const q = P(26, top + 54); tag.setAttribute('transform', `translate(${f2(q)}) rotate(${(p.torso || 0).toFixed(1)})`); }
    if (sc) {
      const k = P(11, top + 8), sw = Math.sin(t * 2.4) * 1.5;
      setA(scK, { cx: k[0].toFixed(1), cy: k[1].toFixed(1) });
      scT1.setAttribute('d', `M${f2(P(8, top + 9))} L${f2(P(1 + sw, top + 33))} L${f2(P(8 + sw, top + 31))} L${f2(P(13, top + 10))} Z`);
      scT2.setAttribute('d', `M${f2(P(13, top + 9))} L${f2(P(19 + sw, top + 30))} L${f2(P(24 + sw, top + 25))} L${f2(P(16, top + 8))} Z`);
    }
  };
  return upd;
}
// a skirt over the thighs (pencil for แม่, a mudmee ซิ่น for ยาย): follows the hip and both thighs; o.pattern = fill
function skirt13(pup, fill, o = {}) {
  const g = svg('g', {});
  pup.g.insertBefore(g, pup.gTorso);
  const body = svg('path', { fill, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  const hem = o.hem ? svg('path', { fill: 'none', stroke: o.hem, 'stroke-width': 7, 'stroke-linecap': 'round' }, g) : null;
  const len = o.len ?? 0.86, half = o.half ?? 31;
  return p => {
    const a = rad(p.torso || 0), hipY = -4;
    const th = (ang, off) => { const hx = off * Math.cos(a) - hipY * Math.sin(a), hy = off * Math.sin(a) + hipY * Math.cos(a); return [hx + Math.cos(rad(ang)) * RIG.THIGH * len, hy + Math.sin(rad(ang)) * RIG.THIGH * len]; };
    const lF = (p.lF || [90, 90])[0], lB = (p.lB || [90, 90])[0];
    const kF = th(lF, 8), kB = th(lB, -8), hc = [(kF[0] + kB[0]) / 2, (kF[1] + kB[1]) / 2];
    const da = rad((lF + lB) / 2), n = [-Math.sin(da), Math.cos(da)];
    const spread = Math.min(16, Math.hypot(kF[0] - kB[0], kF[1] - kB[1]) * 0.5), w = half + spread;
    const P = (x, y) => torsoT(p, x, y), wb = P(-42, -16), wf = P(37, -16);
    const h1 = [hc[0] - n[0] * w, hc[1] - n[1] * w], h2 = [hc[0] + n[0] * w, hc[1] + n[1] * w];
    body.setAttribute('d', `M${f2(wb)} L${f2(wf)} Q${f2(P(40, 20))} ${f2(h1)} L${f2(h2)} Q${f2(P(-44, 20))} ${f2(wb)} Z`);
    if (hem) hem.setAttribute('d', `M${f2([h1[0] + (h2[0] - h1[0]) * 0.06, h1[1] + (h2[1] - h1[1]) * 0.06])} L${f2([h2[0] - (h2[0] - h1[0]) * 0.06, h2[1] - (h2[1] - h1[1]) * 0.06])}`);
  };
}
// Isan mudmee stripes for ยาย's ซิ่น
function mudmeeFill(defs, base = '#6a2f7e') {
  const id = uidS('mm'), pt = svg('pattern', { id, width: 40, height: 26, patternUnits: 'userSpaceOnUse' }, defs);
  svg('rect', { width: 40, height: 26, fill: base }, pt);
  svg('path', { d: 'M0,8 L10,4 L20,8 L30,4 L40,8', fill: 'none', stroke: '#e8b13a', 'stroke-width': 2.4 }, pt);
  svg('path', { d: 'M0,18 L10,22 L20,18 L30,22 L40,18', fill: 'none', stroke: shade(base, 30), 'stroke-width': 2.2 }, pt);
  svg('circle', { cx: 20, cy: 13, r: 2, fill: '#f4efe6' }, pt);
  return `url(#${id})`;
}
// head details: a bow on แม่'s bun, pearl earrings
function bunBow13(pup, c = '#8e2a3c') {
  const R = pup.o.R, h = pup.head, g = svg('g', { transform: `translate(${-R * 0.86},${-R * 0.5}) rotate(-20)` }, h);
  svg('path', { d: 'M0,0 L-16,-11 L-16,11 Z M0,0 L16,-11 L16,11 Z', fill: c, stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  svg('circle', { r: 5, fill: shade(c, -18), stroke: INK, 'stroke-width': 2.5 }, g);
  svg('circle', { cx: -R * 0.8, cy: R * 0.36, r: 4.5, fill: '#fbf6ee', stroke: INK, 'stroke-width': 2 }, h);
}
// a paper party hat on a passenger
function partyHat13(pup, c) {
  const R = pup.o.R, g = svg('g', { transform: `translate(${-R * 0.1},${-R * 0.86}) rotate(-12)` }, pup.head);
  svg('path', { d: `M${-R * 0.34},0 L0,${-R * 0.9} L${R * 0.34},0 Z`, fill: c, stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: `M${-R * 0.2},${-R * 0.3} L${R * 0.16},${-R * 0.18} M${-R * 0.1},${-R * 0.6} L${R * 0.08},${-R * 0.52}`, stroke: '#fff', 'stroke-width': 3, opacity: 0.8 }, g);
  svg('circle', { cy: -R * 0.92, r: 6, fill: '#fff', stroke: INK, 'stroke-width': 2.5 }, g);
}
// the daughter's disguise: a cap and a face mask that come off (set(capOn 0..1, maskOn 0..1))
function disguise13(pup, capC = '#2f3f6a') {
  const R = pup.o.R, h = pup.head;
  const cap = svg('g', {}, h), mask = svg('g', {}, h);
  svg('path', { fill: capC, stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round', d: `M${-R * 1.0},${-R * 0.14} C${-R * 1.04},${-R * 1.36} ${R * 1.02},${-R * 1.42} ${R * 1.0},${-R * 0.28} Z` }, cap);
  svg('path', { fill: shade(capC, -20), stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round', d: `M${R * 0.7},${-R * 0.34} Q${R * 1.4},${-R * 0.36} ${R * 1.56},${-R * 0.12} Q${R * 1.2},${-R * 0.02} ${R * 0.66},${-R * 0.12} Z` }, cap);
  svg('path', { fill: 'none', stroke: '#f2c14e', 'stroke-width': 4, 'stroke-linecap': 'round', d: `M${-R * 0.2},${-R * 0.86} Q${R * 0.1},${-R * 0.98} ${R * 0.36},${-R * 0.82}` }, cap);
  svg('path', { fill: '#f4f6f8', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round', d: `M${-R * 0.08},${R * 0.1} Q${R * 0.36},${R * 0.02} ${R * 0.86},${R * 0.12} Q${R * 0.84},${R * 0.62} ${R * 0.36},${R * 0.7} Q${-R * 0.04},${R * 0.62} ${-R * 0.08},${R * 0.1} Z` }, mask);
  svg('path', { fill: 'none', stroke: '#c9d2dc', 'stroke-width': 2.5, d: `M${R * 0.0},${R * 0.3} Q${R * 0.4},${R * 0.26} ${R * 0.8},${R * 0.3} M${R * 0.02},${R * 0.46} Q${R * 0.4},${R * 0.44} ${R * 0.76},${R * 0.48}` }, mask);
  svg('path', { fill: 'none', stroke: '#f4f6f8', 'stroke-width': 3, d: `M${-R * 0.08},${R * 0.16} Q${-R * 0.5},${R * 0.08} ${-R * 0.74},${R * 0.1}` }, mask);
  return (capOn, maskOn) => {
    cap.setAttribute('display', capOn > 0.02 ? 'inline' : 'none');
    cap.setAttribute('transform', `translate(${(-(1 - capOn) * 30).toFixed(1)},${(-(1 - capOn) * 90).toFixed(1)}) rotate(${(-(1 - capOn) * 40).toFixed(1)})`);
    cap.setAttribute('opacity', Math.min(1, capOn * 2.5).toFixed(2));
    mask.setAttribute('display', maskOn > 0.02 ? 'inline' : 'none');
    mask.setAttribute('transform', `translate(0,${((1 - maskOn) * 46).toFixed(1)})`);
    mask.setAttribute('opacity', Math.min(1, maskOn * 2.5).toFixed(2));
  };
}

// ---------------- props ----------------
// a phone seen from the back (case, camera, a sliver of screen light)
function phoneProp(parent, case_ = '#2a2b36') {
  const g = svg('g', {}, parent);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: case_, stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -15, y: -39, width: 5, height: 52, rx: 2.5, fill: '#d8e8ff' }, g);
  svg('rect', { x: -1, y: -39, width: 14, height: 17, rx: 4, fill: shade(case_, -28), stroke: INK, 'stroke-width': 2 }, g);
  svg('circle', { cx: 4, cy: -34, r: 2.6, fill: '#15151c' }, g); svg('circle', { cx: 4, cy: -27, r: 2.6, fill: '#15151c' }, g);
  svg('circle', { cx: 9.5, cy: -30.5, r: 1.4, fill: '#fff6dc' }, g);
  return { g, scr };
}
// a small bottle of drinking water (cap, blue label), centred on the grip
function bottle13(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  svg('path', { d: 'M-11,-30 L11,-30 L13,-22 L13,30 Q13,36 7,36 L-7,36 Q-13,36 -13,30 L-13,-22 Z', fill: '#dff2ff', 'fill-opacity': 0.92, stroke: INK, 'stroke-width': 3 }, g);
  svg('rect', { x: -7, y: -40, width: 14, height: 11, rx: 3, fill: '#4a7bd8', stroke: INK, 'stroke-width': 2.5 }, g);
  svg('rect', { x: -13, y: -4, width: 26, height: 18, fill: '#4a7bd8', stroke: INK, 'stroke-width': 2 }, g);
  svg('path', { d: 'M-8,5 Q0,0 8,5', fill: 'none', stroke: '#fff', 'stroke-width': 2.4 }, g);
  svg('path', { d: 'M-7,-18 L-7,-8', stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0.8 }, g);
  return g;
}
// the white snack box every passenger gets (red ribbon logo), bottom-centred
function snackBox13(parent, x = 0, y = 0, s = 1) {
  const g = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, parent);
  svg('path', { d: 'M-26,0 L26,0 L26,-30 L-26,-30 Z', fill: '#fbf7ef', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: 'M-26,-30 L-18,-38 L34,-38 L26,-30 Z', fill: '#efe6d4', stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M26,0 L34,-8 L34,-38 L26,-30 Z', fill: '#d9ccb2', stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M-6,-30 L-6,0', stroke: '#c8343c', 'stroke-width': 5 }, g);
  svg('path', { d: heartPathT(-6, -18, 6), fill: '#c8343c' }, g);
  return g;
}
// a little basket of bottles and snack boxes on แม่'s back arm (follows the back wrist; call upd() after pose)
function basket13(pup) {
  const g = svg('g', {}, pup.gArmB);
  pup.gArmB.insertBefore(g, pup.hB);
  svg('path', { d: 'M-46,-6 L46,-6 L38,34 L-38,34 Z', fill: '#c99a5a', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  for (let k = -36; k <= 36; k += 12) svg('path', { d: `M${k},-4 L${k * 0.85},32`, stroke: '#a87a42', 'stroke-width': 3 }, g);
  for (const x of [-30, -12, 6]) { const b = bottle13(g, 0.8); b.setAttribute('transform', `translate(${x},-26) scale(0.8)`); }
  snackBox13(g, 26, -6, 0.6);
  svg('path', { d: 'M-40,-6 Q0,-70 40,-6', fill: 'none', stroke: INK, 'stroke-width': 9, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M-40,-6 Q0,-70 40,-6', fill: 'none', stroke: '#c99a5a', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
  return () => g.setAttribute('transform', `translate(${(pup.wristB[0] + 2).toFixed(1)},${(pup.wristB[1] + 50).toFixed(1)})`);
}
// a hand mic (black, mesh head) with its curly cord running to (cx, cy) in the prop frame; set(cordTo)
function mic13(parent) {
  const g = svg('g', {}, parent);
  const cord = svg('path', { fill: 'none', stroke: '#2a2228', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, g);
  svg('rect', { x: -7, y: -6, width: 14, height: 46, rx: 6, fill: '#2a2b36', stroke: INK, 'stroke-width': 3 }, g);
  svg('circle', { cx: 0, cy: -16, r: 13, fill: '#55586a', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: 'M-9,-20 L9,-20 M-10,-14 L10,-14 M-6,-25 L6,-25', stroke: '#8a8ea2', 'stroke-width': 1.6 }, g);
  svg('rect', { x: -3, y: 6, width: 6, height: 10, rx: 2, fill: '#5ad06a' }, g);
  return (cx, cy, on = 1) => {
    g.setAttribute('display', on ? 'inline' : 'none');
    let d = 'M0,40', n = 14;
    for (let i = 1; i <= n; i++) { const u = i / n, x = cx * u + Math.sin(u * 30) * 7, y = 40 + (cy - 40) * u + Math.cos(u * 30) * 7; d += ` L${x.toFixed(1)},${y.toFixed(1)}`; }
    cord.setAttribute('d', d);
  };
}

// ---------------- front faces (avatars, end card) ----------------
function faceMae13(parent, cx, cy, r) {
  const c = MAE13, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { cx: 0, cy: -r * 1.02, r: r * 0.42, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);   // bun on top
  svg('path', { d: `M0,${-r * 1.0} L${-r * 0.36},${-r * 1.24} L${-r * 0.36},${-r * 0.8} Z M0,${-r * 1.0} L${r * 0.36},${-r * 1.24} L${r * 0.36},${-r * 0.8} Z`, fill: '#8e2a3c', stroke: ink, 'stroke-width': r * 0.04 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 1.0},${r * 0.05} C${-r * 1.06},${-r * 1.12} ${r * 1.06},${-r * 1.12} ${r * 1.0},${r * 0.05} Q${r * 0.7},${-r * 0.52} 0,${-r * 0.5} Q${-r * 0.7},${-r * 0.52} ${-r * 1.0},${r * 0.05} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.24} Q${sx * r * 0.38},${-r * 0.34} ${sx * r * 0.56},${-r * 0.24}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.12} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.32, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
    svg('circle', { cx: sx * r * 1.0, cy: r * 0.3, r: r * 0.08, fill: '#fbf6ee', stroke: ink, 'stroke-width': r * 0.03 }, g);
  }
  svg('path', { fill: '#b5434e', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.2},${r * 0.44} Q0,${r * 0.7} ${r * 0.2},${r * 0.44} Z` }, g);
  return g;
}
function faceLuk13(parent, cx, cy, r, o = {}) {
  const c = LUK13, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.07, 'stroke-linejoin': 'round', d: `M${-r * 1.06},${-r * 0.1} C${-r * 1.14},${-r * 1.36} ${r * 1.14},${-r * 1.36} ${r * 1.06},${-r * 0.1} L${r * 1.1},${r * 1.2} Q${r * 0.7},${r * 1.36} ${r * 0.6},${r * 0.9} L${-r * 0.6},${r * 0.9} Q${-r * 0.7},${r * 1.36} ${-r * 1.1},${r * 1.2} Z` }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { fill: c.hair, d: `M${-r * 1.0},${r * 0.04} C${-r * 1.06},${-r * 1.2} ${r * 1.06},${-r * 1.2} ${r * 1.0},${r * 0.04} Q${r * 0.5},${-r * 0.5} ${-r * 0.1},${-r * 0.42} Q${-r * 0.6},${-r * 0.34} ${-r * 1.0},${r * 0.04} Z`, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('rect', { x: r * 0.3, y: -r * 0.66, width: r * 0.32, height: r * 0.13, rx: r * 0.06, fill: c.clip, stroke: ink, 'stroke-width': r * 0.035, transform: `rotate(-18 ${r * 0.46} ${-r * 0.6})` }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.2} Q${sx * r * 0.38},${-r * 0.3} ${sx * r * 0.56},${-r * 0.2}` }, g);
    if (o.happy) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.06} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.13},${r * 0.06}` }, g);
    else { svg('ellipse', { cx: sx * r * 0.38, cy: r * 0.0, rx: r * 0.09, ry: r * 0.13, fill: '#2a1d21' }, g); svg('circle', { cx: sx * r * 0.38 + r * 0.03, cy: -r * 0.05, r: r * 0.035, fill: '#fff' }, g); }
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.34, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
  }
  svg('path', { fill: '#a8445a', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.46} Q0,${r * 0.78} ${r * 0.22},${r * 0.46} Z` }, g);
  return g;
}
function av13(who, n = 64) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: who === 'mae' ? '#ffe2d6' : '#e2ecff' }, d);
  if (who === 'mae') {
    svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: MAE13.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
    svg('path', { d: 'M-8,30 L8,30 L0,46 Z', fill: '#fbf6ee', stroke: INK, 'stroke-width': 2 }, d);
    svg('ellipse', { cx: 0, cy: 31, rx: 6, ry: 4.5, fill: '#e8b13a', stroke: INK, 'stroke-width': 2 }, d);
    faceMae13(d, 0, 2, 24);
  } else {
    svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: LUK13.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
    svg('path', { d: 'M-10,30 L10,30 L0,46 Z', fill: '#f6efe2', stroke: INK, 'stroke-width': 2 }, d);
    faceLuk13(d, 0, 2, 24, { happy: true });
  }
  return d.outerHTML;
}
