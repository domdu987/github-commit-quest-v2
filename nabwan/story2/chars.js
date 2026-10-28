// story2 cast (new chibi look) + matching front-facing portraits for avatars and photo frames
const SON = { skin: '#ecbd98', skinShade: '#d39d76', hair: '#4a2c20', hairStyle: 'fluffy', top: 'hoodie', sleeve: 'long', shirt: '#f2a23c', shirtDark: '#d9862a', shirtLight: '#f8bf66', pants: '#3a4c7e', pantsDark: '#2e3d68', shoe: '#ffffff', shoeDark: '#e3ddd3', sole: '#e0574b', seed: 3 };
const DAD_WORK = { skin: '#b97c52', skinShade: '#9e6642', hair: '#3a3334', gray: '#cfc8c2', hairStyle: 'dad', top: 'work', sleeve: 'long', shirt: '#5f86b3', shirtDark: '#4c6f98', shirtLight: '#7aa0c9', vest: '#ff8a1f', pants: '#6e5c46', pantsDark: '#5a4a38', shoe: '#6a4c33', shoeDark: '#553c28', sole: '#3a2a20', mustache: true, aged: true, hat: 'hardhat', towel: '#d1453b', seed: 4 };
const DAD_HOME = Object.assign({}, DAD_WORK, { hat: null, towel: null, vest: null, top: 'tank', sleeve: 'none', shirt: '#f6f3ec', shirtDark: '#e1dacb', shirtLight: '#ffffff', pants: '#3d5a9a', pantsDark: '#30497f', shoeStyle: 'sandal', sole: '#2f6a74' });

// front-facing portrait in the same style: who = 'son' | 'dad'
function faceFront2(parent, cx, cy, r, who = 'son') {
  const o = who === 'dad' ? DAD_WORK : SON, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (who === 'son') {
    const puffs = [[-0.62, -0.5, 0.48], [-0.1, -0.82, 0.5], [0.45, -0.62, 0.48], [-0.9, -0.05, 0.3], [0.88, -0.1, 0.3]];
    for (const [x, y, rr] of puffs) svg('circle', { cx: r * x, cy: r * y, r: r * rr + r * 0.06, fill: ink }, g);
    for (const [x, y, rr] of puffs) svg('circle', { cx: r * x, cy: r * y, r: r * rr, fill: o.hair }, g);
  }
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: o.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: o.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  if (who === 'son') {
    const bangs = `Q${r * 0.7},${-r * 0.42} ${r * 0.42},${-r * 0.3} Q${r * 0.22},${-r * 0.58} ${-r * 0.05},${-r * 0.36} Q${-r * 0.3},${-r * 0.6} ${-r * 0.5},${-r * 0.32} Q${-r * 0.78},${-r * 0.36} ${-r * 0.98},${-r * 0.05}`;
    svg('path', { fill: o.hair, d: `M${-r * 0.98},${-r * 0.05} C${-r},${-r * 1.4} ${r},${-r * 1.4} ${r * 0.98},${-r * 0.05} ${bangs} Z` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: `M${r * 0.98},${-r * 0.05} ${bangs}` }, g);
  }
  else {
    svg('path', { fill: o.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round', d: `M${-r * 0.98},${r * 0.05} C${-r * 1.02},${-r * 1.36} ${r * 1.02},${-r * 1.36} ${r * 0.98},${r * 0.05} Q${r * 0.85},${-r * 0.5} ${r * 0.3},${-r * 0.56} Q0,${-r * 0.5} ${-r * 0.3},${-r * 0.56} Q${-r * 0.85},${-r * 0.5} ${-r * 0.98},${r * 0.05} Z` }, g);
    for (const sx of [-1, 1]) svg('path', { fill: 'none', stroke: o.gray, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.9},${-r * 0.05} Q${sx * r * 0.82},${-r * 0.45} ${sx * r * 0.5},${-r * 0.62}` }, g);
  }
  const bw = who === 'dad' ? r * 0.11 : r * 0.08;
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: o.hair, 'stroke-width': bw, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.28} Q${sx * r * 0.38},${-r * 0.38} ${sx * r * 0.56},${-r * 0.28}` }, g);
    svg('ellipse', { cx: sx * r * 0.38, cy: -r * 0.02, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
    svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.08, r: r * 0.045, fill: '#fff' }, g);
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.28, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.45 }, g);
  }
  if (who === 'dad') {
    svg('path', { fill: 'none', stroke: shade(o.skinShade, -18), 'stroke-width': r * 0.035, 'stroke-linecap': 'round', d: `M${-r * 0.62},${-r * 0.06} l${-r * 0.1},${-r * 0.05} M${r * 0.62},${-r * 0.06} l${r * 0.1},${-r * 0.05}` }, g);
    svg('path', { fill: '#6d6461', stroke: ink, 'stroke-width': r * 0.045, 'stroke-linejoin': 'round', d: `M${-r * 0.36},${r * 0.36} Q${-r * 0.3},${r * 0.14} 0,${r * 0.22} Q${r * 0.3},${r * 0.14} ${r * 0.36},${r * 0.36} Q${r * 0.15},${r * 0.28} 0,${r * 0.32} Q${-r * 0.15},${r * 0.28} ${-r * 0.36},${r * 0.36} Z` }, g);
  }
  svg('path', { fill: 'none', stroke: shade(o.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.14} Q0,${r * 0.22} ${r * 0.06},${r * 0.14}` }, g);
  const my = who === 'dad' ? r * 0.5 : r * 0.42;
  svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M${-r * 0.18},${my} Q0,${my + r * 0.18} ${r * 0.18},${my}` }, g);
  return g;
}
function portraitSVG(who, size, bg) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: size, height: size, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  const o = who === 'dad' ? DAD_HOME : SON;
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: who === 'dad' ? DAD_WORK.shirt : SON.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  void o;
  faceFront2(d, 0, 2, 27, who);
  return d.outerHTML;
}
// call log / call screen avatar (replaces the 355 story's dad avatar)
function dadAvatar() { return portraitSVG('dad', 96, '#dbe7f3'); }
