// "52 ปีกับกระทงสองใบ" cast: ตาสม (grey hair, glasses, cream shirt), ยายบัว (grey bun, lilac floral blouse), their young
// selves for the memory, and หลาน (grandson, red tee).
const TA = { skin: '#c99068', skinShade: '#ad774f', hair: '#d9d3cc', hairStyle: 'dad', glasses: '#4a3a30', top: 'tee', sleeve: 'short', shirt: '#f2ead8', shirtDark: '#d9cfb8', shirtLight: '#fffaf0', pants: '#6a5a4a', pantsDark: '#5a4a3c', shoeStyle: 'sandal', sole: '#5a4a3c', seed: 81 };
const YAI = { skin: '#d9a07a', skinShade: '#bd865f', hair: '#d6d0ca', gray: '#eeeae6', hairStyle: 'bun', top: 'blouse', sleeve: 'short', shirt: '#b49ad8', shirtDark: '#9a80c0', shirtLight: '#d6c6ee', flower: '#ffffff', pants: '#5a4a6a', pantsDark: '#4a3c5a', shoeStyle: 'sandal', sole: '#c94f45', seed: 83 };
const TA_YOUNG = Object.assign({}, TA, { hair: '#1f1a1c', glasses: null, shirt: '#f6f1e4', seed: 85 });
const YAI_YOUNG = Object.assign({}, YAI, { hair: '#2a1f1c', gray: null, shirt: '#e88aa8', shirtDark: '#cc6e8c', shirtLight: '#f6b6ca', seed: 87 });
const LAN = { skin: '#e0aa80', skinShade: '#c48f68', hair: '#1f1a1c', hairStyle: 'fluffy', top: 'tee', sleeve: 'short', shirt: '#e0574b', shirtDark: '#c44337', shirtLight: '#f07a6e', pants: '#3a4c7e', pantsDark: '#2e3d68', shoeStyle: 'sandal', sole: '#2f3448', s: 0.92, seed: 89 };

// front faces for the photo on the wall and the avatars
function faceElder(parent, cx, cy, r, who = 'yai', o = {}) {
  const c = who === 'ta' ? TA : YAI, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (who === 'yai') {
    svg('circle', { cx: 0, cy: -r * 1.02, r: r * 0.4, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);   // bun on top
    svg('path', { d: `M${-r * 0.3},${-r * 1.18} q${r * 0.3},${-r * 0.1} ${r * 0.6},0`, fill: 'none', stroke: '#e0a12c', 'stroke-width': r * 0.06, 'stroke-linecap': 'round' }, g);
  }
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  const top = who === 'yai'
    ? `M${-r * 0.98},${-r * 0.02} C${-r * 1.04},${-r * 1.3} ${r * 1.04},${-r * 1.3} ${r * 0.98},${-r * 0.02} Q${r * 0.7},${-r * 0.52} 0,${-r * 0.56} Q${-r * 0.7},${-r * 0.52} ${-r * 0.98},${-r * 0.02} Z`
    : `M${-r * 0.98},${-r * 0.1} C${-r * 1.02},${-r * 1.24} ${r * 1.02},${-r * 1.24} ${r * 0.98},${-r * 0.1} Q${r * 0.5},${-r * 0.66} ${r * 0.1},${-r * 0.62} Q${-r * 0.5},${-r * 0.6} ${-r * 0.98},${-r * 0.1} Z`;
  svg('path', { d: top, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: `M${-r * 0.4},${-r * 0.82} Q0,${-r * 0.98} ${r * 0.4},${-r * 0.82}`, fill: 'none', stroke: '#ffffff', 'stroke-width': r * 0.05, 'stroke-linecap': 'round', opacity: 0.6 }, g);
  const sm = o.smile == null ? 0.8 : o.smile;
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: shade(c.hair, -40), 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.22} Q${sx * r * 0.38},${-r * 0.3} ${sx * r * 0.56},${-r * 0.22}` }, g);
    svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.12} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);   // smiling eyes
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.32, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.45 }, g);
    if (who === 'ta') svg('circle', { cx: sx * r * 0.38, cy: r * 0.0, r: r * 0.22, fill: 'none', stroke: TA.glasses, 'stroke-width': r * 0.05 }, g);
  }
  if (who === 'ta') svg('path', { d: `M${-r * 0.16},0 L${r * 0.16},0`, stroke: TA.glasses, 'stroke-width': r * 0.05 }, g);
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.2} Q0,${r * 0.28} ${r * 0.06},${r * 0.2}` }, g);
  svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.48} Q0,${r * (0.48 + 0.16 * (sm - 0.3))} ${r * 0.18},${r * 0.48}` }, g);
  return g;
}
function elderAv(who, n = 64, bg = '#ffe9c4') {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: (who === 'ta' ? TA : YAI).shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  faceElder(d, 0, 6, 24, who);
  return d.outerHTML;
}
const yaiAv = (n = 64) => elderAv('yai', n, '#f2e4f6');
const taAv = (n = 64) => elderAv('ta', n, '#fff1d6');
