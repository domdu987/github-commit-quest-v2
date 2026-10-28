// "39 บาทที่แม่ไม่กล้ากด" cast: ฝ้าย (long hair, blue heart pyjamas) and แม่ (her own look, not the 127 mom: dark bun with a
// grey streak, reading glasses, coral floral blouse, indigo trousers, old slippers with a faded strap).
const FAI = { skin: '#f0c3a0', skinShade: '#d8a27c', hair: '#2e1f1c', hairStyle: 'long', clip: '#7fd6c7', top: 'heartpj', sleeve: 'short', shirt: '#cfe4fb', shirtDark: '#a7c8ec', shirtLight: '#e8f2ff', print: '#4a7bd8', pants: '#a7c8ec', pantsDark: '#8db2dc', shoeStyle: 'sandal', sole: '#f07aa8', seed: 71 };
const MOM9 = { skin: '#b98058', skinShade: '#9c6844', hair: '#2a2226', gray: '#8e8580', hairStyle: 'bun', glasses: '#7a4a3a', top: 'blouse', sleeve: 'short', shirt: '#e0735a', shirtDark: '#c45a44', shirtLight: '#f29a82', flower: '#fff2d6', pants: '#3e4a7a', pantsDark: '#323d66', shoeStyle: 'sandal', sole: '#9a8aa6', lips: '#8a3a3e', aged: false, seed: 73 };
const MOM9_NEW = Object.assign({}, MOM9, { sole: '#4fc3e0', seed: 73 });   // the same mom in her new slippers

// แม่, front-facing (avatars): bun on top with a grey streak, glasses
function faceMom9(parent, cx, cy, r, o = {}) {
  const c = MOM9, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('circle', { cx: 0, cy: -r * 1.04, r: r * 0.38, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('path', { d: `M${-r * 0.3},${-r * 1.2} q${r * 0.3},${-r * 0.12} ${r * 0.6},0`, fill: 'none', stroke: '#e0453b', 'stroke-width': r * 0.07, 'stroke-linecap': 'round' }, g);   // red hair tie
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  svg('path', { d: `M${-r * 0.98},${-r * 0.02} C${-r * 1.04},${-r * 1.3} ${r * 1.04},${-r * 1.3} ${r * 0.98},${-r * 0.02} Q${r * 0.74},${-r * 0.5} ${r * 0.06},${-r * 0.58} Q${-r * 0.7},${-r * 0.5} ${-r * 0.98},${-r * 0.02} Z`, fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: `M${r * 0.2},${-r * 0.98} Q${r * 0.62},${-r * 0.86} ${r * 0.8},${-r * 0.42}`, fill: 'none', stroke: c.gray, 'stroke-width': r * 0.1, 'stroke-linecap': 'round' }, g);   // grey streak
  const sm = o.smile == null ? 0.8 : o.smile;
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.24} Q${sx * r * 0.38},${-r * 0.32} ${sx * r * 0.56},${-r * 0.24}` }, g);
    if (o.happy) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.12},${r * 0.04} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.12},${r * 0.04}` }, g);
    else { svg('ellipse', { cx: sx * r * 0.38, cy: r * 0.02, rx: r * 0.09, ry: r * 0.13, fill: '#2a1d21' }, g); svg('circle', { cx: sx * r * 0.38 + r * 0.03, cy: -r * 0.03, r: r * 0.035, fill: '#fff' }, g); }
    svg('circle', { cx: sx * r * 0.38, cy: r * 0.02, r: r * 0.23, fill: 'none', stroke: c.glasses, 'stroke-width': r * 0.055 }, g);
    svg('ellipse', { cx: sx * r * 0.6, cy: r * 0.36, rx: r * 0.14, ry: r * 0.08, fill: '#f0857f', opacity: 0.45 }, g);
  }
  svg('path', { d: `M${-r * 0.15},${r * 0.0} L${r * 0.15},${r * 0.0}`, stroke: c.glasses, 'stroke-width': r * 0.055 }, g);
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.24} Q0,${r * 0.3} ${r * 0.06},${r * 0.24}` }, g);
  if (o.grin) svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.2},${r * 0.48} Q0,${r * 0.76} ${r * 0.2},${r * 0.48} Z` }, g);
  else svg('path', { fill: 'none', stroke: c.lips, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.5} Q0,${r * (0.5 + 0.16 * (sm - 0.3))} ${r * 0.18},${r * 0.5}` }, g);
  return g;
}
function mom9Av(n = 64, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: '#ffe2cc' }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: MOM9.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  for (const [fx, fy] of [[-20, 40], [4, 36], [24, 42]]) svg('circle', { cx: fx, cy: fy, r: 3, fill: MOM9.flower }, d);
  faceMom9(d, 0, 6, 24, o);
  return d.outerHTML;
}

// ฝ้าย, front-facing (avatars)
function faceFai(parent, cx, cy, r, o = {}) {
  const c = FAI, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.07, 'stroke-linejoin': 'round', d: `M${-r * 1.02},${-r * 0.2} C${-r * 1.14},${-r * 1.36} ${r * 1.14},${-r * 1.36} ${r * 1.02},${-r * 0.2} L${r * 1.06},${r * 1.3} Q${r * 0.8},${r * 1.42} ${r * 0.56},${r * 1.24} L${-r * 0.56},${r * 1.24} Q${-r * 0.8},${r * 1.42} ${-r * 1.06},${r * 1.3} Z` }, g);
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  const fr = `Q${r * 0.7},${-r * 0.46} ${r * 0.3},${-r * 0.4} Q${-r * 0.1},${-r * 0.36} ${-r * 0.44},${-r * 0.18} Q${-r * 0.7},${-r * 0.04} ${-r * 1.0},${r * 0.04}`;
  svg('path', { fill: c.hair, d: `M${-r * 1.0},${r * 0.04} C${-r * 1.06},${-r * 1.3} ${r * 1.06},${-r * 1.36} ${r * 1.0},${-r * 0.1} ${fr} Z` }, g);
  svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: `M${r * 1.0},${-r * 0.1} ${fr}` }, g);
  svg('rect', { x: r * 0.36, y: -r * 0.62, width: r * 0.3, height: r * 0.12, rx: r * 0.06, fill: c.clip, stroke: ink, 'stroke-width': r * 0.035, transform: `rotate(-20 ${r * 0.51} ${-r * 0.56})` }, g);
  const sm = o.smile == null ? 0.7 : o.smile;
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.2} Q${sx * r * 0.38},${-r * 0.3} ${sx * r * 0.56},${-r * 0.2}` }, g);
    if (o.happy) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.06} Q${sx * r * 0.38},${-r * 0.1} ${sx * r * 0.38 + r * 0.13},${r * 0.06}` }, g);
    else {
      svg('ellipse', { cx: sx * r * 0.38, cy: r * 0.06, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
      svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: 0, r: r * 0.045, fill: '#fff' }, g);
    }
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.34, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
  }
  if (o.grin) svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.46} Q0,${r * 0.78} ${r * 0.22},${r * 0.46} Z` }, g);
  else svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.17},${r * 0.5} Q0,${r * (0.5 + 0.16 * (sm - 0.3))} ${r * 0.17},${r * 0.5}` }, g);
  return g;
}
function faiAv(n = 64, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: '#dbe7f3' }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: FAI.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  faceFai(d, 0, 2, 25, o);
  return d.outerHTML;
}
