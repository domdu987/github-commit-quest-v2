// "50 กุหลาบ ที่ยายจำไม่ได้" cast: ตาบุญ (white side-parted hair, a white moustache, a mustard knit vest over a cream
// shirt, brown trousers, a walking cane) and ยายแก้ว (a short white bob with a red hair clip, a peach blouse with green
// sprigs, a long batik ผ้าถุง); the two of them 49 years ago (black hair, his white shirt and flares, her long hair with a
// flower, a rose-pink blouse); their granddaughter (ponytail, lavender tee, jeans); the old flower seller at the market
// (grey bun, striped top, a green apron). Props: a red rose (fresh, wrapped in newspaper, pressed), the album, a cane,
// sticky notes, a marker, a ballpoint pen; a sleeping old dog.
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);

const TA16 = { skin: '#c99068', skinShade: '#ad774f', hair: '#ece8e2', gray: '#fbf9f6', hairStyle: 'part', mustache: true, aged: true,
  top: 'stripe', stripe: '#b0603a', sleeve: 'short', shirt: '#efe2c8', shirtDark: '#d8c8a8', shirtLight: '#fbf3e2',
  pants: '#6a4a36', pantsDark: '#5a3c2a', shoeStyle: 'sandal', sole: '#4a3426', seed: 171 };
const YAI16 = { skin: '#e2b08a', skinShade: '#c8946e', hair: '#e6e2dc', hairStyle: 'bob', clip: '#d8343c', aged: true, lashes: true, lips: '#b5546a',
  top: 'blouse', sleeve: 'long', shirt: '#f6c8a8', shirtDark: '#e2ac8a', shirtLight: '#fde0c8', flower: '#7fb069',
  pants: '#e2b08a', pantsDark: '#c8946e', shoeStyle: 'sandal', sole: '#8a4a3a', seed: 173 };
const TA16_Y = Object.assign({}, TA16, { hair: '#1c1818', gray: null, mustache: false, aged: false, top: 'tee', sleeve: 'long', shirt: '#fbf9f4', shirtDark: '#e2ddd2', shirtLight: '#ffffff',
  pants: '#4a3a5a', pantsDark: '#3c2e4a', seed: 175 });
const YAI16_Y = Object.assign({}, YAI16, { hair: '#1e1616', hairStyle: 'long', clip: '#f6efe2', aged: false, shirt: '#f08aa8', shirtDark: '#d8708e', shirtLight: '#f8b0c6', flower: '#ffffff', seed: 177 });
const LAN16 = { skin: '#ecbc96', skinShade: '#d2a07a', hair: '#3a2620', hairStyle: 'pony', clip: '#f2c14e', lashes: true, top: 'tee', sleeve: 'short',
  shirt: '#b8a0d8', shirtDark: '#9a82c0', shirtLight: '#d2c0ec', pants: '#3a4c7e', pantsDark: '#2e3d68', shoeStyle: 'sneaker', shoe: '#f4efe6', shoeDark: '#d6cfc2', sole: '#8a7ab0', seed: 179 };
const VENDOR16 = { skin: '#c48a60', skinShade: '#a8714a', hair: '#5a504c', gray: '#a8a098', hairStyle: 'bun', aged: true, top: 'stripe', stripe: '#c8343c', sleeve: 'short',
  shirt: '#f6efe2', shirtDark: '#ddd2c0', shirtLight: '#ffffff', vest: '#3f7a52', pants: '#3a3040', pantsDark: '#2e2634', shoeStyle: 'sandal', sole: '#3a3040', seed: 181 };

// ---------------- world-space helpers ----------------
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
const wristFW = (pup, p) => pupW(pup, p, pup.wristF[0], pup.wristF[1]);
const wristBW = (pup, p) => pupW(pup, p, pup.wristB[0], pup.wristB[1]);
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);
const torsoT = (p, x, y) => { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; };
const f2 = q => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;

// ---------------- wardrobe overlays ----------------
// a long skirt / ผ้าถุง over the thighs (follows the hip and both thighs); o.batik draws a band pattern
function sarong16(pup, fill, o = {}) {
  const g = svg('g', {});
  pup.g.insertBefore(g, pup.gTorso);
  const body = svg('path', { fill, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  const band = o.batik ? svg('path', { fill: 'none', stroke: o.batik, 'stroke-width': 7, 'stroke-linecap': 'round', opacity: 0.85 }, g) : null;
  const dots = o.batik ? svg('path', { fill: 'none', stroke: o.dot || '#f2c14e', 'stroke-width': 4, 'stroke-linecap': 'round', 'stroke-dasharray': '1 11' }, g) : null;
  const len = o.len ?? 1.7, half = o.half ?? 34;
  return p => {
    const a = rad(p.torso || 0), hipY = -4;
    const lF = (p.lF || [90, 90])[0], lB = (p.lB || [90, 90])[0];
    const seated = Math.abs((lF + lB) / 2 - 90) > 45, L2 = seated ? Math.min(len, 1.05) : len;
    const th2 = (ang, off) => { const hx = off * Math.cos(a) - hipY * Math.sin(a), hy = off * Math.sin(a) + hipY * Math.cos(a); return [hx + Math.cos(rad(ang)) * RIG.THIGH * L2, hy + Math.sin(rad(ang)) * RIG.THIGH * L2]; };
    const kF = th2(lF, 8), kB = th2(lB, -8), hc = [(kF[0] + kB[0]) / 2, (kF[1] + kB[1]) / 2];
    const da = rad((lF + lB) / 2), n = [-Math.sin(da), Math.cos(da)];
    const spread = Math.min(16, Math.hypot(kF[0] - kB[0], kF[1] - kB[1]) * 0.5), w = half + spread;
    const P = (x, y) => torsoT(p, x, y), wb = P(-42, -16), wf = P(37, -16);
    const h1 = [hc[0] - n[0] * w, hc[1] - n[1] * w], h2 = [hc[0] + n[0] * w, hc[1] + n[1] * w];
    body.setAttribute('d', `M${f2(wb)} L${f2(wf)} Q${f2(P(40, 20))} ${f2(h1)} L${f2(h2)} Q${f2(P(-44, 20))} ${f2(wb)} Z`);
    if (band) { const u = 0.82, b1 = [h1[0] + (wf[0] - h1[0]) * (1 - u), h1[1] + (wf[1] - h1[1]) * (1 - u)], b2 = [h2[0] + (wb[0] - h2[0]) * (1 - u), h2[1] + (wb[1] - h2[1]) * (1 - u)]; const d = `M${f2(b1)} L${f2(b2)}`; band.setAttribute('d', d); dots.setAttribute('d', `M${f2([b1[0], b1[1] - 12])} L${f2([b2[0], b2[1] - 12])}`); }
  };
}

// ---------------- props ----------------
// a red rose on a long stem (bottom of the stem at 0,0, pointing up); o.wrap wraps it in newspaper; o.dry = pressed colours
function rose16(parent, s = 1, o = {}) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  const red = o.dry ? '#9a3a3a' : '#d8283a', dark = o.dry ? '#6a2626' : '#a81828', leaf = o.dry ? '#7a7a4a' : '#4f9e5e';
  if (o.wrap) svg('path', { d: 'M-26,-30 L26,-30 L10,6 L-10,6 Z', fill: '#e8e2d2', stroke: INK, 'stroke-width': 2.6, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M0,0 Q4,-40 0,-88', fill: 'none', stroke: '#3f7a46', 'stroke-width': 4.5, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M1,-46 q16,-14 26,-6 q-10,12 -26,6 Z', fill: leaf, stroke: INK, 'stroke-width': 2.2 }, g);
  svg('path', { d: 'M0,-62 q-16,-12 -24,-2 q12,10 24,2 Z', fill: leaf, stroke: INK, 'stroke-width': 2.2 }, g);
  svg('path', { d: 'M-15,-96 Q-18,-116 0,-122 Q18,-116 15,-96 Q8,-86 0,-86 Q-8,-86 -15,-96 Z', fill: red, stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M-8,-106 Q0,-116 8,-106 M-11,-98 Q0,-92 11,-98', fill: 'none', stroke: dark, 'stroke-width': 2.4, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M-10,-112 q4,-6 10,-6', fill: 'none', stroke: '#ffb0b8', 'stroke-width': 2.2, 'stroke-linecap': 'round', opacity: o.dry ? 0.2 : 0.7 }, g);
  if (o.wrap) { svg('path', { d: 'M-22,-28 L-34,-70 L-6,-34 M22,-28 L34,-70 L6,-34', fill: '#f0eadc', stroke: INK, 'stroke-width': 2.4, 'stroke-linejoin': 'round' }, g); for (const y of [-14, -6]) svg('path', { d: `M-12,${y} L12,${y}`, stroke: '#8a847c', 'stroke-width': 1.6, opacity: 0.7 }, g); svg('path', { d: 'M-12,-18 L12,-18', stroke: '#c8343c', 'stroke-width': 3 }, g); }
  return g;
}
// a walking cane (handle at 0,0)
function cane16(parent) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M0,0 Q0,-14 14,-14 Q26,-14 26,-2', fill: 'none', stroke: INK, 'stroke-width': 10, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M0,0 L0,190', stroke: INK, 'stroke-width': 10, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M0,0 Q0,-14 14,-14 Q26,-14 26,-2 M0,0 L0,190', fill: 'none', stroke: '#7a4a2a', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
  return g;
}
// the old album, closed (bottom-centred, lying on a table, seen from the side): returns the group
function albumClosed16(parent, s = 1) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  svg('path', { d: 'M-56,0 L56,0 L64,-16 L-48,-16 Z', fill: '#f6efe2', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: 'M-58,-16 L66,-16 L70,-26 L-54,-26 Z', fill: '#8e2a3c', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: 'M-60,0 L58,0 L58,6 L-60,6 Z', fill: '#7a2232', stroke: INK, 'stroke-width': 3 }, g);
  for (let k = 0; k < 3; k++) svg('path', { d: `M${-40 + k * 30},-2 L${-36 + k * 30},-14`, stroke: '#d8283a', 'stroke-width': 3, opacity: 0.6 }, g);   // dried petals peeking out
  return g;
}
// a sleeping old dog (ground at y): returns update(t)
function oldDog16(g, x, y, s = 1, c = '#d9b07a') {
  const k = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('ellipse', { cx: 0, cy: 4, rx: 110, ry: 12, fill: '#000', opacity: 0.18 }, k);
  const body = svg('g', {}, k);
  svg('path', { d: 'M-70,0 C-80,-56 10,-80 60,-60 C96,-44 104,-14 92,0 Z', fill: c, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, body);
  svg('path', { d: 'M20,-66 q20,10 30,30', fill: 'none', stroke: shade(c, -20), 'stroke-width': 6, 'stroke-linecap': 'round' }, body);
  const head = svg('g', {}, k);
  svg('path', { d: 'M-118,-6 C-124,-40 -96,-56 -70,-48 C-50,-42 -48,-10 -60,0 Z', fill: c, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, head);
  svg('path', { d: 'M-118,-8 Q-136,-6 -134,6 Q-124,10 -110,4', fill: shade(c, 12), stroke: INK, 'stroke-width': 4 }, head);
  svg('circle', { cx: -134, cy: 0, r: 5, fill: INK }, head);
  svg('path', { d: 'M-96,-46 C-110,-40 -112,-10 -96,-2 C-86,-14 -86,-36 -96,-46 Z', fill: shade(c, -28), stroke: INK, 'stroke-width': 4 }, head);
  svg('path', { d: 'M-112,-24 q6,4 12,0', fill: 'none', stroke: INK, 'stroke-width': 3.5, 'stroke-linecap': 'round' }, head);
  const tail = svg('path', { fill: 'none', stroke: INK, 'stroke-width': 13, 'stroke-linecap': 'round' }, k), tailC = svg('path', { fill: 'none', stroke: c, 'stroke-width': 7, 'stroke-linecap': 'round' }, k);
  return t => {
    body.setAttribute('transform', `scale(1,${(1 + 0.03 * Math.sin(t * 2.2)).toFixed(3)})`);
    const w = Math.sin(t * 1.1) * 14, d = `M90,-10 Q120,${(-14 + w).toFixed(1)} 134,${(-2 + w * 0.6).toFixed(1)}`;
    tail.setAttribute('d', d); tailC.setAttribute('d', d);
  };
}

// ---------------- front faces (avatars, end card) ----------------
function faceTa16(parent, cx, cy, r) {
  const c = TA16, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 1.0},${r * 0.05} C${-r * 1.1},${-r * 1.2} ${r * 1.1},${-r * 1.2} ${r * 1.0},${r * 0.05} Q${r * 0.9},${-r * 0.52} ${r * 0.2},${-r * 0.62} Q${-r * 0.1},${-r * 0.8} ${-r * 0.4},${-r * 0.56} Q${-r * 0.9},${-r * 0.42} ${-r * 1.0},${r * 0.05} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: '#d8d2ca', 'stroke-width': r * 0.08, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.26} Q${sx * r * 0.38},${-r * 0.34} ${sx * r * 0.56},${-r * 0.26}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.12},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.12},${r * 0.04}` }, g);
    svg('path', { fill: 'none', stroke: shade(c.skinShade, -18), 'stroke-width': r * 0.035, 'stroke-linecap': 'round', d: `M${sx * r * 0.62},${-r * 0.02} l${sx * r * 0.14},${-r * 0.06}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.32, rx: r * 0.13, ry: r * 0.07, fill: '#f0857f', opacity: 0.4 }, g);
  }
  svg('path', { d: `M${-r * 0.34},${r * 0.42} Q0,${r * 0.22} ${r * 0.34},${r * 0.42} Q0,${r * 0.36} ${-r * 0.34},${r * 0.42} Z`, fill: '#f3efe8', stroke: ink, 'stroke-width': r * 0.04 }, g);   // the moustache
  svg('path', { fill: 'none', stroke: '#7a2f33', 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.16},${r * 0.56} Q0,${r * 0.66} ${r * 0.16},${r * 0.56}` }, g);
  return g;
}
function faceYai16(parent, cx, cy, r) {
  const c = YAI16, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('path', { d: `M${-r * 1.08},${r * 0.62} C${-r * 1.22},${-r * 1.0} ${r * 1.22},${-r * 1.0} ${r * 1.08},${r * 0.62} Q${r * 0.9},${r * 0.78} ${r * 0.7},${r * 0.6} L${-r * 0.7},${r * 0.6} Q${-r * 0.9},${r * 0.78} ${-r * 1.08},${r * 0.62} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 0.98},${-r * 0.05} C${-r * 1.0},${-r * 1.12} ${r * 1.0},${-r * 1.12} ${r * 0.98},${-r * 0.05} Q${r * 0.5},${-r * 0.58} ${-r * 0.1},${-r * 0.5} Q${-r * 0.7},${-r * 0.42} ${-r * 0.98},${-r * 0.05} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('rect', { x: r * 0.36, y: -r * 0.78, width: r * 0.34, height: r * 0.14, rx: r * 0.07, fill: c.clip, stroke: ink, 'stroke-width': r * 0.04, transform: `rotate(-22 ${r * 0.53} ${-r * 0.71})` }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.12} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    svg('path', { fill: 'none', stroke: shade(c.skinShade, -18), 'stroke-width': r * 0.035, 'stroke-linecap': 'round', d: `M${sx * r * 0.62},${-r * 0.02} l${sx * r * 0.14},${-r * 0.06}` }, g);
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.34, rx: r * 0.15, ry: r * 0.08, fill: '#f0857f', opacity: 0.55 }, g);
  }
  svg('path', { fill: '#b5546a', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.44} Q0,${r * 0.7} ${r * 0.22},${r * 0.44} Z` }, g);
  return g;
}
function av16(who, n = 64) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: who === 'yai' ? '#ffe2d6' : '#f6ecd0' }, d);
  if (who === 'yai') { svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: YAI16.shirt, stroke: INK, 'stroke-width': 2.5 }, d); for (const [x, y] of [[-16, 40], [10, 36], [24, 44]]) svg('circle', { cx: x, cy: y, r: 3, fill: YAI16.flower }, d); faceYai16(d, 0, 2, 23); }
  else { svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: TA16.shirt, stroke: INK, 'stroke-width': 2.5 }, d); for (const y of [36, 44]) svg('path', { d: `M-34,${y} L34,${y}`, stroke: TA16.stripe, 'stroke-width': 3 }, d); faceTa16(d, 0, 2, 24); }
  return d.outerHTML;
}
// a little flower clip on the bob (the rig draws clips only on long hair)
function hairClip16(pup, c) {
  const R = pup.o.R, g = svg('g', { transform: `translate(${R * 0.44},${-R * 0.78})` }, pup.head);
  for (let k = 0; k < 5; k++) svg('circle', { cx: Math.cos(k * 1.2566) * 6, cy: Math.sin(k * 1.2566) * 6, r: 5.5, fill: c || '#f08aa8', stroke: INK, 'stroke-width': 1.8 }, g);
  svg('circle', { r: 3.5, fill: '#f2c14e' }, g);
}
