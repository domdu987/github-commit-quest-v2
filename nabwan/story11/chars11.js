// "12 ฤดูฝน ที่ไหล่ของพ่อเปียก" cast: พ่อ at about 40 (khaki uniform shirt, black mustache), the same พ่อ at 67 (grey hair,
// grey mustache, glasses, faded khaki long sleeves, sandals), the son in school uniform from ป.1 (white shirt, navy shorts,
// backpack) to ม.6, and the grown son (mustard knit shirt).
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);
const DAD = { skin: '#c98a5e', skinShade: '#ab7048', hair: '#221a1a', hairStyle: 'dad', mustache: true, top: 'tee', sleeve: 'short', shirt: '#c9b27a', shirtDark: '#a8915c', shirtLight: '#ddc994', pants: '#4a4038', pantsDark: '#3c332c', shoe: '#3a2c26', shoeDark: '#2a201c', sole: '#1e1614', shoeStyle: 'sneaker', seed: 91 };
const DAD_OLD = Object.assign({}, DAD, { hair: '#d4cdc4', gray: '#efebe6', glasses: '#5a4636', aged: true, sleeve: 'long', shirt: '#b9aa82', shirtDark: '#9c8e68', shirtLight: '#d0c4a0', pants: '#5a5048', pantsDark: '#4a4038', shoeStyle: 'sandal', sole: '#6a5040', seed: 93 });
const KID = { skin: '#e2ad84', skinShade: '#c69168', hair: '#1f1a1c', hairStyle: 'fluffy', top: 'tee', sleeve: 'short', shirt: '#f7f6f0', shirtDark: '#dedcd2', shirtLight: '#ffffff', pants: '#2f3b6a', pantsDark: '#26305a', shorts: true, shoe: '#2a2a32', shoeDark: '#1e1e26', sole: '#14141a', s: 0.62, seed: 95 };
const KID_M6 = Object.assign({}, KID, { hairStyle: 'part', pants: '#2a2a32', pantsDark: '#202028', shorts: false, s: 0.88, seed: 96 });
const SON = { skin: '#dca47c', skinShade: '#c08a62', hair: '#1f1a1c', hairStyle: 'part', top: 'tee', sleeve: 'short', shirt: '#e9c46a', shirtDark: '#c9a24a', shirtLight: '#f4d68a', pants: '#33394f', pantsDark: '#2a2f42', shoe: '#f4efe6', shoeDark: '#d6cfc2', sole: '#7a5a40', seed: 97 };
// school kid at age k (0 = ป.1 … 1 = ม.6): scale and look between KID and KID_M6
const kidAt = k => Object.assign({}, k < 0.5 ? KID : KID_M6, { s: lerp(0.62, 0.88, k) });

// ---------------- world-space helpers on a posed puppet ----------------
// puppet-local point → world (local = the rig's own frame before the puppet's translate/scale/flip)
function pupW(pup, p, lx, ly) { const s = (p.s || 1) * pup.o.s, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
// a point in the torso frame (rotated with the lean) → world
function torsoW(pup, p, x, y) { const a = rad(p.torso || 0); return pupW(pup, p, x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)); }
// a point in the front-hand prop frame → world (call after pose)
function propW(pup, p, lx, ly) { const r = rad(p.propRot || 0), [wx, wy] = pup.wristF; return pupW(pup, p, wx + lx * Math.cos(r) - ly * Math.sin(r), wy + lx * Math.sin(r) + ly * Math.cos(r)); }
const headW = (pup, p) => torsoW(pup, p, HEAD_C[0], HEAD_C[1]);

// ---------------- the wet shirt: a darker soaked patch spreading from the back shoulder ----------------
// Clipped to the live torso outline, so it bends with the lean; returns set(k) for 0..1 wetness.
function wetPatch(pup, defs, o = {}) {
  const tid = uidS('tor'); pup.torso.id = tid;
  const cid = uidS('wc');
  svg('use', { href: '#' + tid }, svg('clipPath', { id: cid }, defs));
  const outer = svg('g', { 'clip-path': `url(#${cid})` });
  pup.torsoG.insertBefore(outer, pup.torso.nextSibling);
  const inner = svg('g', {}, outer);
  const wc = o.color || shade(pup.o.shirt, -30);
  const blob = svg('path', { fill: wc, opacity: 0.9 }, inner);
  const edge = svg('path', { fill: 'none', stroke: shade(wc, -12), 'stroke-width': 3, opacity: 0.55 }, inner);
  const drips = svg('path', { fill: 'none', stroke: wc, 'stroke-width': 7, 'stroke-linecap': 'round' }, inner);
  const glint = svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 3.5, 'stroke-linecap': 'round', opacity: 0.6 }, inner);
  const stub = pup.stubB, stubC = stub ? stub.getAttribute('stroke') : null;
  let cur = -1;
  return (k, torso = 0) => {
    inner.setAttribute('transform', `rotate(${torso.toFixed(2)})`);
    k = clamp(k);
    if (Math.abs(k - cur) < 1e-3) return;
    cur = k;
    outer.setAttribute('display', k < 0.01 ? 'none' : 'inline');
    const T = RIG.T, cx = -30 + 10 * k, cy = -T + 6 + 30 * k, rx = 16 + 32 * k, ry = 14 + 46 * k;
    // a lumpy blob from the shoulder seam down the back
    const n = 14, r = rng(23); let d = '';
    for (let i = 0; i <= n; i++) {
      const a = i / n * Math.PI * 2, w = 1 + 0.14 * Math.sin(a * 3 + 1) + 0.08 * (r() - 0.5);
      const x = cx + Math.cos(a) * rx * w, y = cy + Math.sin(a) * ry * w - (Math.sin(a) < 0 ? 18 * k : 0);
      d += (i ? ' L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1);
    }
    blob.setAttribute('d', d + ' Z'); edge.setAttribute('d', d + ' Z');
    const by = cy + ry * 0.9;
    drips.setAttribute('d', [-14, 2, 16].map((dx, i) => `M${(cx + dx).toFixed(1)},${(by - 8).toFixed(1)} l0,${(k * (14 + i * 9)).toFixed(1)}`).join(' '));
    glint.setAttribute('d', `M${(cx - rx * 0.4).toFixed(1)},${(cy - ry * 0.5).toFixed(1)} q6,-5 12,-3 M${(cx + 2).toFixed(1)},${(cy - ry * 0.1).toFixed(1)} l7,-2`);
    if (stub) stub.setAttribute('stroke', k > 0.25 ? shade(stubC, -22) : stubC);
  };
}
// school backpack on the kid's back (drawn behind the torso, turns with the lean)
function backpack(pup, c = '#e0574b') {
  const g = svg('g', {});
  pup.gTorso.insertBefore(g, pup.gTorso.firstChild);
  svg('rect', { x: -66, y: -RIG.T + 10, width: 40, height: 86, rx: 14, fill: c, stroke: INK, 'stroke-width': 5 }, g);
  svg('rect', { x: -62, y: -RIG.T + 52, width: 30, height: 30, rx: 8, fill: shade(c, -14), stroke: INK, 'stroke-width': 3.5 }, g);
  svg('path', { d: `M-58,${-RIG.T + 20} L-34,${-RIG.T + 20}`, stroke: '#ffd166', 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
  return p => g.setAttribute('transform', `rotate(${(p.torso || 0).toFixed(2)})`);
}
// school pocket badge (blue initials) on the kid's shirt
function schoolBadge(pup) {
  const g = svg('g', {}, pup.detail);
  svg('path', { d: `M8,${-RIG.T + 34} l14,0 M8,${-RIG.T + 40} l10,0`, stroke: '#3a5bb8', 'stroke-width': 3, 'stroke-linecap': 'round' }, g);
  return p => g.setAttribute('transform', `rotate(${(p.torso || 0).toFixed(2)})`);
}

// ---------------- front faces (avatars, end card) ----------------
function faceDad11(parent, cx, cy, r, o = {}) {
  const c = o.old ? DAD_OLD : DAD, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 0.98},${-r * 0.06} C${-r * 1.02},${-r * 1.24} ${r * 1.02},${-r * 1.24} ${r * 0.98},${-r * 0.06} Q${r * 0.62},${-r * 0.62} ${r * 0.12},${-r * 0.58} Q${-r * 0.5},${-r * 0.6} ${-r * 0.98},${-r * 0.06} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round' }, g);
  if (o.old) svg('path', { d: `M${-r * 0.5},${-r * 0.84} Q0,${-r * 1.0} ${r * 0.5},${-r * 0.84}`, fill: 'none', stroke: '#ffffff', 'stroke-width': r * 0.06, 'stroke-linecap': 'round', opacity: 0.7 }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: o.old ? '#8e857c' : c.hair, 'stroke-width': r * 0.08, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.24} Q${sx * r * 0.38},${-r * 0.32} ${sx * r * 0.56},${-r * 0.24}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.34, rx: r * 0.14, ry: r * 0.08, fill: '#f0857f', opacity: 0.4 }, g);
    if (o.old) svg('circle', { cx: sx * r * 0.38, cy: r * 0.0, r: r * 0.23, fill: 'none', stroke: DAD_OLD.glasses, 'stroke-width': r * 0.055 }, g);
  }
  if (o.old) svg('path', { d: `M${-r * 0.15},0 L${r * 0.15},0`, stroke: DAD_OLD.glasses, 'stroke-width': r * 0.055 }, g);
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.22} Q0,${r * 0.28} ${r * 0.06},${r * 0.22}` }, g);
  svg('path', { d: `M${-r * 0.3},${r * 0.4} Q${-r * 0.16},${r * 0.28} 0,${r * 0.34} Q${r * 0.16},${r * 0.28} ${r * 0.3},${r * 0.4} Q${r * 0.14},${r * 0.38} 0,${r * 0.42} Q${-r * 0.14},${r * 0.38} ${-r * 0.3},${r * 0.4} Z`, fill: o.old ? '#8e857c' : '#2a2020', stroke: ink, 'stroke-width': r * 0.035 }, g);   // mustache
  svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M${-r * 0.14},${r * 0.52} Q0,${r * 0.62} ${r * 0.14},${r * 0.52}` }, g);
  return g;
}
function faceSon11(parent, cx, cy, r) {
  const c = SON, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 0.98},${-r * 0.02} C${-r * 1.04},${-r * 1.3} ${r * 1.04},${-r * 1.3} ${r * 0.98},${-r * 0.1} Q${r * 0.9},${-r * 0.5} ${r * 0.4},${-r * 0.56} Q${-r * 0.1},${-r * 0.6} ${-r * 0.32},${-r * 0.82} Q${-r * 0.56},${-r * 0.4} ${-r * 0.98},${-r * 0.02} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round' }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.08, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.24} Q${sx * r * 0.38},${-r * 0.32} ${sx * r * 0.56},${-r * 0.24}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.34, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.45 }, g);
  }
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.22} Q0,${r * 0.28} ${r * 0.06},${r * 0.22}` }, g);
  svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.2},${r * 0.44} Q0,${r * 0.72} ${r * 0.2},${r * 0.44} Z` }, g);
  return g;
}
function av11(who, n = 64) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: who === 'son' ? '#ffe9c4' : '#f6e2c8' }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: who === 'son' ? SON.shirt : DAD_OLD.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  if (who === 'son') faceSon11(d, 0, 4, 25); else faceDad11(d, 0, 4, 25, { old: true });
  return d.outerHTML;
}
