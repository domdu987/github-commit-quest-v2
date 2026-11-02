// "128 ช่อ ที่ไม่ใช่ของเรา" cast: the rider (tanned, short black hair, an orange rider jacket with a reflective band,
// navy jeans, black sneakers, an open-face navy helmet with a visor) and his wife (long dark hair with a yellow clip, a
// coral tee, a long sarong in teal-and-gold batik, slippers); the people he delivers to (a woman in a navy blazer, a
// grandmother, a schoolboy). Props: the scooter with its delivery box, a bouquet in kraft paper and pink cellophane
// with a gift card, a phone seen from the back.
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);

const RIDER17 = { skin: '#b97a50', skinShade: '#9c6440', hair: '#1a1616', hairStyle: 'dad', top: 'hoodie', sleeve: 'long',
  shirt: '#e8862a', shirtDark: '#c86a1a', shirtLight: '#f6a24a', pants: '#2a3456', pantsDark: '#222a46', shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#f4efe6', seed: 191 };
const WIFE17 = { skin: '#e6b48e', skinShade: '#cc986e', hair: '#2a1c18', hairStyle: 'long', clip: '#f2c14e', lashes: true, lips: '#c0505a', top: 'tee', sleeve: 'short',
  shirt: '#f2876e', shirtDark: '#d86c54', shirtLight: '#f8a690', pants: '#e6b48e', pantsDark: '#cc986e', shoeStyle: 'sandal', sole: '#c0505a', seed: 193 };
const FOLKS17 = [
  { skin: '#efc4a2', skinShade: '#d6a684', hair: '#2a1c18', hairStyle: 'bob', lashes: true, top: 'office', tie: null, shirt: '#2f3f6a', shirtDark: '#24325a', shirtLight: '#43568a', sleeve: 'long', pants: '#2f3f6a', pantsDark: '#24325a', shoeStyle: 'sneaker', shoe: '#2b2326', shoeDark: '#1e181b', sole: '#2b2326', seed: 195 },
  { skin: '#c99068', skinShade: '#ad774f', hair: '#d9d3cc', gray: '#f0ece6', hairStyle: 'bun', aged: true, top: 'blouse', sleeve: 'short', shirt: '#9ac0e0', shirtDark: '#7aa0c8', shirtLight: '#bcd8f0', flower: '#ffffff', pants: '#4a3a5a', pantsDark: '#3c2e4a', shoeStyle: 'sandal', sole: '#4a3a5a', seed: 197 },
  { skin: '#e0aa80', skinShade: '#c48f68', hair: '#1f1a1c', hairStyle: 'spiky', top: 'tee', sleeve: 'short', shirt: '#fbf9f4', shirtDark: '#e2ddd2', shirtLight: '#ffffff', pants: '#2a2a3a', pantsDark: '#22222e', shorts: true, shoeStyle: 'sneaker', shoe: '#f4efe6', shoeDark: '#d6cfc2', sole: '#2f5fb8', s: 0.82, seed: 199 },
];

// ---------------- world-space helpers ----------------
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
const wristFW = (pup, p) => pupW(pup, p, pup.wristF[0], pup.wristF[1]);
const wristBW = (pup, p) => pupW(pup, p, pup.wristB[0], pup.wristB[1]);
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);
const torsoT = (p, x, y) => { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; };
const f2 = q => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;

// ---------------- wardrobe overlays ----------------
// a reflective band across the rider jacket (chest and the front sleeve); returns update(p)
function reflect17(pup) {
  const g = svg('g', {});
  pup.gTorso.insertBefore(g, pup.shoulderG);
  const band = svg('path', { fill: 'none', stroke: '#e8eef2', 'stroke-width': 9, opacity: 0.95 }, g), glint = svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 3, opacity: 0.8 }, g);
  return p => { const P = (x, y) => torsoT(p, x, y); const d = `M${f2(P(-40, -RIG.T + 64))} L${f2(P(38, -RIG.T + 64))}`; band.setAttribute('d', d); glint.setAttribute('d', d); };
}
// an open-face helmet with a visor (on the head group); show(bool)
function helmet17(pup, c = '#2a3a6a') {
  const R = pup.o.R, g = svg('g', {}, pup.head);
  svg('path', { d: `M${-R * 1.04},${R * 0.22} C${-R * 1.16},${-R * 1.12} ${R * 1.02},${-R * 1.3} ${R * 1.02},${-R * 0.34} L${R * 0.86},${-R * 0.3} Q${R * 0.2},${-R * 0.5} ${-R * 0.5},${-R * 0.34} L${-R * 0.7},${R * 0.3} Z`, fill: c, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: `M${-R * 0.6},${-R * 0.9} Q${R * 0.1},${-R * 1.2} ${R * 0.7},${-R * 0.7}`, fill: 'none', stroke: '#ffffff', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.35 }, g);
  svg('path', { d: `M${R * 0.5},${-R * 0.46} L${R * 1.22},${-R * 0.46} Q${R * 1.26},${-R * 0.3} ${R * 1.1},${-R * 0.26} L${R * 0.6},${-R * 0.3} Z`, fill: '#7f9ce0', 'fill-opacity': 0.55, stroke: INK, 'stroke-width': 3.5 }, g);   // the visor, up
  svg('rect', { x: -R * 0.5, y: -R * 0.78, width: R * 0.5, height: R * 0.16, rx: R * 0.06, fill: '#f2c14e', stroke: INK, 'stroke-width': 2 }, g);   // a reflective sticker
  svg('path', { d: `M${-R * 0.62},${R * 0.26} Q${-R * 0.2},${R * 0.86} ${R * 0.3},${R * 0.82}`, fill: 'none', stroke: INK, 'stroke-width': 3, opacity: 0.7 }, g);   // the chin strap
  return on => g.setAttribute('display', on ? 'inline' : 'none');
}
// a long sarong (ผ้าถุง) over the thighs, teal-and-gold batik band
function sarong17(pup, fill, o = {}) {
  const g = svg('g', {});
  pup.g.insertBefore(g, pup.gTorso);
  const body = svg('path', { fill, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  const band = svg('path', { fill: 'none', stroke: o.batik || '#e8b04a', 'stroke-width': 7, 'stroke-linecap': 'round', opacity: 0.9 }, g);
  const len = o.len ?? 1.75, half = o.half ?? 34;
  return p => {
    const a = rad(p.torso || 0), hipY = -4, lF = (p.lF || [90, 90])[0], lB = (p.lB || [90, 90])[0];
    const seated = Math.abs((lF + lB) / 2 - 90) > 45, L2 = seated ? Math.min(len, 1.05) : len;
    const th2 = (ang, off) => { const hx = off * Math.cos(a) - hipY * Math.sin(a), hy = off * Math.sin(a) + hipY * Math.cos(a); return [hx + Math.cos(rad(ang)) * RIG.THIGH * L2, hy + Math.sin(rad(ang)) * RIG.THIGH * L2]; };
    const kF = th2(lF, 8), kB = th2(lB, -8), hc = [(kF[0] + kB[0]) / 2, (kF[1] + kB[1]) / 2];
    const da = rad((lF + lB) / 2), n = [-Math.sin(da), Math.cos(da)], spread = Math.min(16, Math.hypot(kF[0] - kB[0], kF[1] - kB[1]) * 0.5), w = half + spread;
    const P = (x, y) => torsoT(p, x, y), wb = P(-42, -16), wf = P(37, -16), h1 = [hc[0] - n[0] * w, hc[1] - n[1] * w], h2 = [hc[0] + n[0] * w, hc[1] + n[1] * w];
    body.setAttribute('d', `M${f2(wb)} L${f2(wf)} Q${f2(P(40, 20))} ${f2(h1)} L${f2(h2)} Q${f2(P(-44, 20))} ${f2(wb)} Z`);
    const u = 0.84, b1 = [h1[0] + (wf[0] - h1[0]) * (1 - u), h1[1] + (wf[1] - h1[1]) * (1 - u)], b2 = [h2[0] + (wb[0] - h2[0]) * (1 - u), h2[1] + (wb[1] - h2[1]) * (1 - u)];
    band.setAttribute('d', `M${f2(b1)} L${f2(b2)}`);
  };
}

// ---------------- props ----------------
// a bouquet (held at the wrap's waist, 0,0; blooms up): kraft paper, pink cellophane, red roses, baby's breath, a ribbon,
// the gift card (o.card)
function bouquet17(parent, s = 1, o = {}) {
  const g = svg('g', { transform: `scale(${s})` }, parent);
  svg('path', { d: 'M-46,-70 L46,-70 L14,40 L-14,40 Z', fill: '#f8c8d8', 'fill-opacity': 0.75, stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  for (const [x, y] of [[-30, -84], [30, -84], [-14, -100], [14, -98], [0, -86], [-40, -66], [40, -66]]) svg('circle', { cx: x, cy: y, r: 5, fill: '#ffffff', stroke: '#c8c0b8', 'stroke-width': 1 }, g);
  for (const [x, y, r] of [[-22, -84, 15], [20, -86, 15], [0, -100, 16], [-6, -76, 14], [16, -70, 13]]) { svg('circle', { cx: x, cy: y, r, fill: '#d8283a', stroke: INK, 'stroke-width': 2.6 }, g); svg('path', { d: `M${x - r * 0.5},${y} Q${x},${y - r * 0.6} ${x + r * 0.5},${y}`, fill: 'none', stroke: '#a81828', 'stroke-width': 2.2 }, g); }
  svg('path', { d: 'M-34,-60 L34,-60 L12,34 L-12,34 Z', fill: '#c89a62', stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M-26,-50 L-8,24 M24,-50 L8,24', stroke: '#a87a42', 'stroke-width': 2, opacity: 0.6 }, g);
  svg('path', { d: 'M-14,-4 L14,-4 L12,6 L-12,6 Z', fill: '#d8486a', stroke: INK, 'stroke-width': 2.4 }, g);
  svg('path', { d: 'M0,0 q-18,-14 -22,4 q14,6 22,-4 q18,-14 22,4 q-14,6 -22,-4 M-2,4 L-10,24 M2,4 L10,24', fill: '#f06a8a', stroke: INK, 'stroke-width': 2.2 }, g);
  if (o.card) { const c = svg('g', { transform: 'translate(30,-30) rotate(12)' }, g); svg('rect', { x: -14, y: -10, width: 30, height: 22, rx: 3, fill: '#fbf7ef', stroke: INK, 'stroke-width': 2 }, c); svg('path', { d: heartPathT(1, 1, 5), fill: '#d8283a' }, c); }
  return g;
}
// the scooter (faces right; rear wheel at -110, front at +116, ground at 0) with the delivery box; returns { g, seat,
// bar, update(t, speed) }
function scooter17(parent, s = 1, o = {}) {
  const g = svg('g', {}, parent), b = svg('g', {}, g), body = o.body || '#c8343c';
  const wheel = x => { const w = svg('g', { transform: `translate(${x},-34)` }, b); svg('circle', { r: 34, fill: '#2a2a32', stroke: INK, 'stroke-width': 4 }, w); svg('circle', { r: 18, fill: '#a8a8b0', stroke: INK, 'stroke-width': 3 }, w); const sp = svg('path', { d: 'M-14,0 L14,0 M0,-14 L0,14', stroke: '#6a6a72', 'stroke-width': 4 }, w); return sp; };
  const sp1 = wheel(-110), sp2 = wheel(116);
  svg('path', { d: 'M-150,-62 Q-150,-120 -90,-128 L-10,-128 Q20,-128 30,-96 L60,-60 L-40,-60 Q-60,-40 -100,-40 Q-150,-40 -150,-62 Z', fill: body, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, b);   // rear body
  svg('path', { d: 'M-118,-130 L-6,-130 Q8,-130 8,-120 L-120,-120 Q-128,-120 -118,-130 Z', fill: '#2a2a32', stroke: INK, 'stroke-width': 3.5 }, b);   // the seat
  svg('path', { d: 'M30,-62 L96,-62 L104,-40 L20,-40 Z', fill: '#3a3a42', stroke: INK, 'stroke-width': 3.5 }, b);   // the floorboard
  svg('path', { d: 'M88,-56 Q96,-150 120,-196 L142,-190 Q122,-140 118,-40 Z', fill: body, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, b);   // the leg shield
  svg('path', { d: 'M116,-40 L124,-34 M120,-190 L116,-40', stroke: INK, 'stroke-width': 6 }, b);
  svg('path', { d: 'M98,-34 Q116,-80 140,-60 Q132,-40 124,-34 Z', fill: body, stroke: INK, 'stroke-width': 3.5 }, b);   // the mudguard
  svg('path', { d: 'M108,-214 L158,-210', stroke: INK, 'stroke-width': 9, 'stroke-linecap': 'round' }, b);   // the handlebar
  svg('ellipse', { cx: 150, cy: -196, rx: 14, ry: 12, fill: '#fff2c0', stroke: INK, 'stroke-width': 3 }, b);   // the headlamp
  const beam = svg('path', { d: 'M160,-200 L420,-260 L420,-120 Z', fill: '#fff2c0', opacity: 0, style: 'mix-blend-mode:screen' }, b);
  svg('path', { d: 'M-150,-150 L-150,-132 L-60,-132 L-60,-150 Z', fill: '#4a4a52', stroke: INK, 'stroke-width': 3 }, b);   // the rack
  const box = svg('g', { transform: 'translate(-104,-150)' }, b);   // the delivery box
  svg('rect', { x: -66, y: -126, width: 132, height: 126, rx: 10, fill: o.box || '#e8862a', stroke: INK, 'stroke-width': 4.5 }, box);
  svg('rect', { x: -66, y: -126, width: 132, height: 22, rx: 8, fill: shade(o.box || '#e8862a', -18), stroke: INK, 'stroke-width': 3.5 }, box);
  svg('path', { d: heartPathT(0, -58, 22), fill: '#fbf7ef', stroke: INK, 'stroke-width': 3 }, box); svg('path', { d: 'M-8,-62 l8,-10 l8,10', fill: 'none', stroke: '#d8283a', 'stroke-width': 4 }, box);
  svg('rect', { x: -60, y: -20, width: 120, height: 8, fill: '#e8eef2', opacity: 0.8 }, box);   // reflective strip
  svg('ellipse', { cx: -150, cy: -70, rx: 8, ry: 10, fill: '#d8283a', stroke: INK, 'stroke-width': 2.5 }, b);   // tail light
  g.setAttribute('transform', `scale(${s})`);
  return { g, b, box, beam, seat: [-60, -130], bar: [140, -212], floor: [60, -62], update(t, speed = 0, lamp = 0) { const a = (t * speed * 6) % 360; sp1.setAttribute('transform', `rotate(${a.toFixed(1)})`); sp2.setAttribute('transform', `rotate(${a.toFixed(1)})`); b.setAttribute('transform', `translate(0,${(speed > 0 ? -Math.abs(Math.sin(t * 18)) * 2 : 0).toFixed(1)})`); beam.setAttribute('opacity', (0.28 * lamp).toFixed(2)); } };
}
// a phone seen from the back: case, camera, a sliver of screen light on the edge
function phone17(parent) {
  const g = svg('g', {}, parent);
  svg('rect', { x: -15, y: -46, width: 30, height: 60, rx: 7, fill: '#2a2a3a', stroke: INK, 'stroke-width': 3.5 }, g);
  svg('rect', { x: -9, y: -40, width: 12, height: 14, rx: 4, fill: '#1a1a24', stroke: '#5a5a72', 'stroke-width': 1.5 }, g);
  svg('circle', { cx: -3, cy: -33, r: 3, fill: '#4a5a8a' }, g);
  const glow = svg('rect', { x: 12, y: -44, width: 5, height: 56, rx: 2.5, fill: '#d8ecff', opacity: 0.9 }, g);
  return { g, glow };
}

// ---------------- front faces (avatars, end card) ----------------
function faceRider17(parent, cx, cy, r, helmet = false) {
  const c = RIDER17, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  if (helmet) { svg('path', { d: `M${-r * 1.08},${r * 0.2} C${-r * 1.16},${-r * 1.3} ${r * 1.16},${-r * 1.3} ${r * 1.08},${r * 0.2} L${r * 0.86},${r * 0.2} Q${r * 0.8},${-r * 0.56} 0,${-r * 0.6} Q${-r * 0.8},${-r * 0.56} ${-r * 0.86},${r * 0.2} Z`, fill: '#2a3a6a', stroke: ink, 'stroke-width': r * 0.06 }, g); svg('rect', { x: -r * 0.3, y: -r * 0.98, width: r * 0.6, height: r * 0.16, rx: r * 0.06, fill: '#f2c14e' }, g); }
  else svg('path', { d: `M${-r * 1.0},${r * 0.05} C${-r * 1.1},${-r * 1.2} ${r * 1.1},${-r * 1.2} ${r * 1.0},${r * 0.05} Q${r * 0.9},${-r * 0.52} ${r * 0.2},${-r * 0.6} Q${-r * 0.1},${-r * 0.8} ${-r * 0.4},${-r * 0.56} Q${-r * 0.9},${-r * 0.42} ${-r * 1.0},${r * 0.05} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.08, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.26} Q${sx * r * 0.38},${-r * 0.34} ${sx * r * 0.56},${-r * 0.26}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.12},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.12},${r * 0.04}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.32, rx: r * 0.13, ry: r * 0.07, fill: '#f0857f', opacity: 0.4 }, g);
  }
  svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.42} Q0,${r * 0.7} ${r * 0.22},${r * 0.42} Z` }, g);
  return g;
}
function faceWife17(parent, cx, cy, r) {
  const c = WIFE17, ink = INK, g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('path', { d: `M${-r * 1.08},${r * 1.2} C${-r * 1.3},${-r * 1.1} ${r * 1.3},${-r * 1.1} ${r * 1.08},${r * 1.2} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 0.98},${-r * 0.05} C${-r * 1.0},${-r * 1.12} ${r * 1.0},${-r * 1.12} ${r * 0.98},${-r * 0.05} Q${r * 0.5},${-r * 0.6} ${-r * 0.1},${-r * 0.52} Q${-r * 0.7},${-r * 0.42} ${-r * 0.98},${-r * 0.05} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('rect', { x: r * 0.36, y: -r * 0.8, width: r * 0.34, height: r * 0.14, rx: r * 0.07, fill: c.clip, stroke: ink, 'stroke-width': r * 0.04, transform: `rotate(-22 ${r * 0.53} ${-r * 0.73})` }, g);
  for (const sx of [-1, 1]) {
    svg('ellipse', { cx: sx * r * 0.38, cy: r * 0.02, rx: r * 0.09, ry: r * 0.13, fill: '#2a1d21' }, g);
    svg('circle', { cx: sx * r * 0.38 + r * 0.03, cy: -r * 0.04, r: r * 0.035, fill: '#fff' }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.34, rx: r * 0.15, ry: r * 0.08, fill: '#f0857f', opacity: 0.55 }, g);
  }
  svg('path', { fill: '#c0505a', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.44} Q0,${r * 0.7} ${r * 0.22},${r * 0.44} Z` }, g);
  return g;
}
function av17(who, n = 64, helmet = false) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: who === 'wife' ? '#ffe2d6' : '#ffe8c8' }, d);
  if (who === 'wife') { svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: WIFE17.shirt, stroke: INK, 'stroke-width': 2.5 }, d); faceWife17(d, 0, 2, 23); }
  else { svg('path', { d: 'M-38,48 C-36,26 36,26 38,48 Z', fill: RIDER17.shirt, stroke: INK, 'stroke-width': 2.5 }, d); svg('path', { d: 'M-36,40 L36,40', stroke: '#e8eef2', 'stroke-width': 4 }, d); faceRider17(d, 0, 2, 24, helmet); }
  return d.outerHTML;
}
// front faces for the delivery polaroids
function faceFolk17(parent, cx, cy, r, i) { const o = FOLKS17[i % FOLKS17.length]; return faceFront(parent, cx, cy, r, Object.assign({}, o, { hairStyle: o.hairStyle === 'spiky' ? 'dad' : o.hairStyle })); }
