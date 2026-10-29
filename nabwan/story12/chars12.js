// "9 ผ้าพันคอที่ไม่เคยได้ใช้" cast: ยาย in Chiang Rai (grey perm, glasses, cream floral blouse under a red knitted vest,
// plum trousers), and her grandchild in Bangkok (bob with a mint clip; coral tee and shorts at home, mustard hoodie for the
// trip north). Scarves: nine colours plus the tenth they finish together, worn singly or stacked to the chin.
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);
const YAI12 = { skin: '#c48a60', skinShade: '#a8714a', hair: '#cfc8c0', gray: '#efebe6', hairStyle: 'perm', glasses: '#7a4a2a', aged: true, top: 'blouse', sleeve: 'long', shirt: '#efe2cc', shirtDark: '#d8c7aa', shirtLight: '#fbf3e4', flower: '#c8343c', vest: '#a8323e', pants: '#4a3a5a', pantsDark: '#3c2e4a', shoeStyle: 'sandal', sole: '#7a4a2a', seed: 121 };
const LAN12 = { skin: '#ecb894', skinShade: '#d19c76', hair: '#2a1f1c', hairStyle: 'bob', clip: '#7fc6a8', lashes: true, top: 'tee', sleeve: 'short', shirt: '#f08a6a', shirtDark: '#d8705a', shirtLight: '#f8a888', pants: '#3a4c7e', pantsDark: '#2e3d68', shorts: true, shoeStyle: 'sandal', sole: '#f2c14e', seed: 123 };
const LAN12_N = Object.assign({}, LAN12, { top: 'hoodie', sleeve: 'long', shirt: '#d9a83e', shirtDark: '#b88a2a', shirtLight: '#ecc464', pants: '#4a3a32', pantsDark: '#3c2e28', shorts: false, shoeStyle: 'sneaker', shoe: '#f4efe6', shoeDark: '#d6cfc2', sole: '#c94f45', seed: 125 });
// the nine scarves (one a winter) and the tenth
const SCARF = ['#e0453b', '#f2a03a', '#f2c14e', '#7fb069', '#4f9e8e', '#4a7bd8', '#8a5fc8', '#e88aa8', '#f6efe2'];
const SCARF10 = '#e8a83a';   // the tenth: the gold of the บัวตอง (and it shows against ยาย's red vest)

// knitted-rib fill for a colour (cached per defs)
function knitFill(defs, c) {
  defs._knit = defs._knit || {};
  if (defs._knit[c]) return defs._knit[c];
  const id = uidS('kn');
  const pt = svg('pattern', { id, width: 14, height: 10, patternUnits: 'userSpaceOnUse' }, defs);
  svg('rect', { width: 14, height: 10, fill: c }, pt);
  svg('path', { d: 'M0,2 L3.5,8 L7,2 M7,2 L10.5,8 L14,2', fill: 'none', stroke: shade(c, -22), 'stroke-width': 1.6, opacity: 0.7 }, pt);
  svg('path', { d: 'M1,1 L3.5,5', stroke: shade(c, 30), 'stroke-width': 1.2, opacity: 0.6 }, pt);
  return (defs._knit[c] = `url(#${id})`);
}

// scarves worn at the neck: n rolls (colours[]) stacked from the collar up, the last one's ends hanging in front.
// Drawn over the head (comic stack to the chin) but under the front arm; returns update(p) to call after pose.
function scarfWear(pup, defs, colours, o = {}) {
  const g = svg('g', {});
  pup.g.insertBefore(g, pup.gArmF);
  const rolls = [], step = o.step ?? 6;   // lower rolls first, each sitting on the one below
  const tail = svg('g', {}, g);
  const tc = colours[colours.length - 1];
  const tailP = svg('path', { fill: knitFill(defs, tc), stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, tail);
  const fr = svg('path', { fill: 'none', stroke: shade(tc, -15), 'stroke-width': 3, 'stroke-linecap': 'round' }, tail);
  colours.forEach((c, i) => {
    const w = 50 - i * 1.2;
    rolls.push(svg('path', { d: `M${-w},0 C${-w},-13 ${w},-13 ${w},0 C${w},14 ${-w},14 ${-w},0 Z`, fill: knitFill(defs, c), stroke: INK, 'stroke-width': 4, transform: `translate(${(4 + (i % 2 ? 2 : -2)).toFixed(1)},${(-i * step).toFixed(1)})` }, g));
  });
  const len = o.tail ?? 70;
  const upd = (p, t = 0) => {
    const ta = rad(p.torso || 0), T = RIG.T;
    g.setAttribute('transform', `translate(${(T * Math.sin(ta)).toFixed(2)},${(-T * Math.cos(ta) + 6).toFixed(2)}) rotate(${(p.torso || 0).toFixed(2)})`);
    const sw = Math.sin(t * 2.2) * 3;
    tailP.setAttribute('d', `M18,6 L36,4 Q${40 + sw},${len * 0.5} ${36 + sw},${len} L${18 + sw},${len + 2} Q${22 + sw * 0.5},${len * 0.5} 18,6 Z`);
    fr.setAttribute('d', `M${20 + sw},${len + 2} l-2,10 M${27 + sw},${len + 1} l0,11 M${34 + sw},${len} l2,10`);
    g.setAttribute('display', upd.hidden ? 'none' : 'inline');
  };
  upd.hidden = !!o.hidden;   // set .hidden before calling to show / hide
  return upd;
}

// a folded scarf seen from above (in the drawer): x,y = bottom-left; chunky rib, two creases, a tasselled end
function scarfFolded(g, defs, x, y, w, h, c) {
  const s = svg('g', {}, g);
  const id = uidS('kb'), pt = svg('pattern', { id, width: 26, height: 22, patternUnits: 'userSpaceOnUse' }, defs);
  svg('rect', { width: 26, height: 22, fill: c }, pt);
  svg('path', { d: 'M0,3 L6.5,17 L13,3 L19.5,17 L26,3', fill: 'none', stroke: shade(c, -24), 'stroke-width': 3, 'stroke-linejoin': 'round' }, pt);
  svg('path', { d: 'M3,8 L6.5,14', stroke: shade(c, 28), 'stroke-width': 2.4 }, pt);
  svg('rect', { x: x + 6, y: y - h + 8, width: w, height: h, rx: 12, fill: '#000', opacity: 0.3 }, s);
  svg('rect', { x, y: y - h, width: w, height: h, rx: 12, fill: `url(#${id})`, stroke: INK, 'stroke-width': 5 }, s);
  for (const v of [0.34, 0.67]) svg('path', { d: `M${x + 4},${y - h + h * v} L${x + w - 4},${y - h + h * v}`, stroke: shade(c, -35), 'stroke-width': 4, opacity: 0.7 }, s);
  svg('path', { d: `M${x + 10},${y - h + h * 0.34 + 4} L${x + w - 10},${y - h + h * 0.34 + 4}`, stroke: '#fff', 'stroke-width': 3, opacity: 0.25 }, s);
  svg('rect', { x: x + w * 0.62, y: y - h, width: w * 0.12, height: h, fill: shade(c, 40), opacity: 0.55 }, s);   // a contrast stripe
  for (let k = 0; k < 6; k++) svg('path', { d: `M${x + w},${y - h + 10 + k * (h - 20) / 5} l16,${k % 2 ? 3 : -3}`, stroke: shade(c, -12), 'stroke-width': 5, 'stroke-linecap': 'round' }, s);   // tassels
  return s;
}
// a hanging knitted piece (on needles): top edge from (x0,y0) to (x1,y1), length len; returns the group
function knitPiece(g, defs, c, o = {}) {
  const k = svg('g', {}, g);
  const body = svg('path', { fill: knitFill(defs, c), stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, k);
  const stripe = svg('path', { fill: 'none', stroke: o.stripe || '#f6efe2', 'stroke-width': 6, opacity: o.stripe === null ? 0 : 0.9 }, k);
  const n1 = svg('path', { stroke: INK, 'stroke-width': 7, 'stroke-linecap': 'round' }, k);
  const n1c = svg('path', { stroke: '#d9b48a', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, k);
  const n2 = svg('path', { stroke: INK, 'stroke-width': 7, 'stroke-linecap': 'round' }, k);
  const n2c = svg('path', { stroke: '#d9b48a', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, k);
  const yarn = svg('path', { fill: 'none', stroke: c, 'stroke-width': 3, 'stroke-linecap': 'round' }, k);
  return {
    g: k,
    set(a, b, len, t = 0, ball = null, needles = true) {
      const sw = Math.sin(t * 1.7) * 4, mx = (a[0] + b[0]) / 2;
      body.setAttribute('d', `M${a[0].toFixed(1)},${a[1].toFixed(1)} L${b[0].toFixed(1)},${b[1].toFixed(1)} L${(b[0] - 6 + sw).toFixed(1)},${(b[1] + len).toFixed(1)} Q${(mx + sw).toFixed(1)},${(Math.max(a[1], b[1]) + len + 8).toFixed(1)} ${(a[0] + 6 + sw).toFixed(1)},${(a[1] + len).toFixed(1)} Z`);
      const sy = Math.max(a[1], b[1]) + len * 0.45;
      stripe.setAttribute('d', len > 40 ? `M${(a[0] + 4 + sw * 0.5).toFixed(1)},${sy.toFixed(1)} L${(b[0] - 4 + sw * 0.5).toFixed(1)},${sy.toFixed(1)}` : 'M0,0');
      const nd = (p, q) => `M${p[0].toFixed(1)},${p[1].toFixed(1)} L${q[0].toFixed(1)},${q[1].toFixed(1)}`;
      const d1 = nd([a[0] - 30, a[1] + 14], [a[0] + 34, a[1] - 26]), d2 = nd([b[0] + 30, b[1] + 14], [b[0] - 34, b[1] - 26]);
      [n1, n1c].forEach(e => e.setAttribute('d', needles ? d1 : 'M0,0')); [n2, n2c].forEach(e => e.setAttribute('d', needles ? d2 : 'M0,0'));
      yarn.setAttribute('d', ball ? `M${b[0].toFixed(1)},${b[1].toFixed(1)} Q${((b[0] + ball[0]) / 2).toFixed(1)},${(Math.max(b[1], ball[1]) + 60).toFixed(1)} ${ball[0].toFixed(1)},${ball[1].toFixed(1)}` : 'M0,0');
    },
  };
}
// yarn ball (world), returns the group
function yarnBall(g, defs, x, y, r, c) {
  const b = svg('g', { transform: `translate(${x},${y})` }, g);
  svg('circle', { r, fill: c, stroke: INK, 'stroke-width': 3.5 }, b);
  for (const a of [-40, 10, 60]) svg('path', { d: `M${-r * 0.9},0 Q0,${-r * 0.6} ${r * 0.9},0`, fill: 'none', stroke: shade(c, -22), 'stroke-width': 2.2, transform: `rotate(${a})` }, b);
  svg('path', { d: `M${-r * 0.4},${-r * 0.55} q${r * 0.3},${-r * 0.2} ${r * 0.6},0`, fill: 'none', stroke: '#fff', 'stroke-width': 2.5, opacity: 0.5 }, b);
  return b;
}

// ---------------- world-space helpers ----------------
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
const wristFW = (pup, p) => pupW(pup, p, pup.wristF[0], pup.wristF[1]);
const wristBW = (pup, p) => pupW(pup, p, pup.wristB[0], pup.wristB[1]);
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);
// a breath puff in the cold air from the mouth: update(pup, p, t, on)
function breath(parent, seed) {
  const r = rng(seed), ps = Array.from({ length: 3 }, () => ({ ph: r(), el: svg('circle', { fill: '#ffffff' }, parent) }));
  return (pup, p, t, on = 1) => {
    const [mx, my] = torsoW(pup, p, HEAD_C[0] + 46, HEAD_C[1] + 30), f = p.f || 1;
    ps.forEach((q, i) => { const k = ((t * 0.5 + q.ph + i / 3) % 1); setA(q.el, { cx: (mx + f * (10 + 60 * k)).toFixed(1), cy: (my - 30 * k).toFixed(1), r: (6 + 22 * k).toFixed(1), opacity: (on * 0.35 * Math.sin(Math.PI * k)).toFixed(3) }); });
  };
}

// ---------------- front faces (avatars, end card) ----------------
function faceYai12(parent, cx, cy, r, o = {}) {
  const c = YAI12, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  const curls = []; for (let i = 0; i <= 10; i++) { const a = rad(160 + i * 22); curls.push([Math.cos(a) * r * 0.98, Math.sin(a) * r * 0.86 - r * 0.12, r * (i % 2 ? 0.26 : 0.3)]); }
  for (const [x, y, rr] of curls) svg('circle', { cx: x, cy: y, r: rr + r * 0.06, fill: ink }, g);
  for (const [x, y, rr] of curls) svg('circle', { cx: x, cy: y, r: rr, fill: c.hair }, g);
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.14, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  for (const [x, y, rr] of [[-0.42, -0.68, 0.2], [-0.12, -0.78, 0.22], [0.2, -0.76, 0.21], [0.5, -0.64, 0.19]]) { svg('circle', { cx: x * r, cy: y * r, r: rr * r + r * 0.05, fill: ink }, g); svg('circle', { cx: x * r, cy: y * r, r: rr * r, fill: c.hair }, g); }
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: '#8e857c', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.26} Q${sx * r * 0.38},${-r * 0.34} ${sx * r * 0.56},${-r * 0.26}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.12} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.34, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
    svg('circle', { cx: sx * r * 0.38, cy: r * 0.0, r: r * 0.23, fill: 'none', stroke: c.glasses, 'stroke-width': r * 0.055 }, g);
  }
  svg('path', { d: `M${-r * 0.15},0 L${r * 0.15},0`, stroke: c.glasses, 'stroke-width': r * 0.055 }, g);
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.22} Q0,${r * 0.28} ${r * 0.06},${r * 0.22}` }, g);
  svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.2},${r * 0.44} Q0,${r * 0.7} ${r * 0.2},${r * 0.44} Z` }, g);
  return g;
}
function faceLan12(parent, cx, cy, r) {
  const c = LAN12, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.07, 'stroke-linejoin': 'round', d: `M${-r * 1.06},${-r * 0.1} C${-r * 1.14},${-r * 1.36} ${r * 1.14},${-r * 1.36} ${r * 1.06},${-r * 0.1} L${r * 1.06},${r * 0.66} Q${r * 0.8},${r * 0.86} ${r * 0.56},${r * 0.7} L${-r * 0.56},${r * 0.7} Q${-r * 0.8},${r * 0.86} ${-r * 1.06},${r * 0.66} Z` }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  const fr = `Q${r * 0.6},${-r * 0.36} ${r * 0.2},${-r * 0.34} Q${-r * 0.2},${-r * 0.33} ${-r * 0.5},${-r * 0.16} Q${-r * 0.74},${-r * 0.02} ${-r * 1.0},${r * 0.04}`;
  svg('path', { fill: c.hair, d: `M${-r * 1.0},${r * 0.04} C${-r * 1.06},${-r * 1.3} ${r * 1.06},${-r * 1.36} ${r * 1.0},${-r * 0.22} ${fr} Z` }, g);
  svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: `M${r * 1.0},${-r * 0.22} ${fr}` }, g);
  svg('rect', { x: r * 0.3, y: -r * 0.64, width: r * 0.3, height: r * 0.12, rx: r * 0.06, fill: c.clip, stroke: ink, 'stroke-width': r * 0.035, transform: `rotate(-14 ${r * 0.45} ${-r * 0.58})` }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.2} Q${sx * r * 0.38},${-r * 0.3} ${sx * r * 0.56},${-r * 0.2}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.06} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.13},${r * 0.06}` }, g);
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.34, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
  }
  svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.46} Q0,${r * 0.78} ${r * 0.22},${r * 0.46} Z` }, g);
  return g;
}
function av12(who, n = 64, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  const defs = svg('defs', {}, d);
  svg('circle', { r: 48, fill: who === 'yai' ? '#f6e2c8' : '#ffe2d6' }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: who === 'yai' ? YAI12.vest : LAN12_N.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  if (who === 'yai') faceYai12(d, 0, 2, 24); else faceLan12(d, 0, 2, 24);
  if (o.scarf) {   // a scarf roll at the neck
    const id = 'avk' + Math.random().toString(36).slice(2, 7);
    const pt = svg('pattern', { id, width: 8, height: 6, patternUnits: 'userSpaceOnUse' }, defs);
    svg('rect', { width: 8, height: 6, fill: o.scarf }, pt); svg('path', { d: 'M0,1 L2,5 L4,1 L6,5 L8,1', fill: 'none', stroke: shade(o.scarf, -25), 'stroke-width': 1 }, pt);
    svg('path', { d: 'M-24,30 C-24,20 24,20 24,30 C24,40 -24,40 -24,30 Z', fill: `url(#${id})`, stroke: INK, 'stroke-width': 2.5 }, d);
  }
  return d.outerHTML;
}
