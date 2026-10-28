// "1,095 ข้อความของแม่" cast in the story2 chibi rig + matching front-facing portraits
const MOM = { skin: '#c98d62', skinShade: '#ae7550', hair: '#4a4044', gray: '#dcd6d0', hairStyle: 'bun', top: 'blouse', sleeve: 'short', shirt: '#e0708a', shirtDark: '#c4566f', shirtLight: '#f6b3c2', flower: '#ffffff', pants: '#6d4a7a', pantsDark: '#583b63', shoeStyle: 'sandal', sole: '#c94f45', glasses: '#8a5a3c', aged: true, lips: '#8a3a3e', seed: 7 };
const DAUGHTER = { skin: '#f0c3a0', skinShade: '#d8a27c', hair: '#2e1f1c', hairStyle: 'long', clip: '#ff7aa2', top: 'office', sleeve: 'long', shirt: '#a3c9ec', shirtDark: '#80a9d2', shirtLight: '#c6e0f6', lanyard: '#e0574b', pants: '#3b3f58', pantsDark: '#30344a', shoe: '#2e2b33', shoeDark: '#24212a', sole: '#4a4552', lashes: true, lips: '#c0505a', seed: 5 };
const DAUGHTER_HOME = Object.assign({}, DAUGHTER, { top: 'tee', sleeve: 'short', shirt: '#b9a6e2', shirtDark: '#9c87cc', shirtLight: '#d3c6f0', pants: '#9d88cc', pantsDark: '#8572b5', shoeStyle: 'sandal', sole: '#f2a0b6' });

function faceFront3(parent, cx, cy, r, who = 'mom') {
  const o = who === 'mom' ? MOM : DAUGHTER, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (who === 'daughter') svg('path', { fill: o.hair, stroke: ink, 'stroke-width': r * 0.06, d: `M${-r * 1.05},${-r * 0.2} C${-r * 1.1},${-r * 1.3} ${r * 1.1},${-r * 1.3} ${r * 1.05},${-r * 0.2} L${r * 1.12},${r * 1.25} Q${r * 0.9},${r * 1.35} ${r * 0.7},${r * 1.2} L${-r * 0.7},${r * 1.2} Q${-r * 0.9},${r * 1.35} ${-r * 1.12},${r * 1.25} Z` }, g);
  if (who === 'mom') svg('circle', { cx: 0, cy: -r * 1.02, r: r * 0.38, fill: o.hair, stroke: ink, 'stroke-width': r * 0.06 }, g);
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: o.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: o.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  if (who === 'mom') {
    svg('path', { fill: o.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round', d: `M${-r * 0.98},${r * 0.1} C${-r * 1.02},${-r * 1.36} ${r * 1.02},${-r * 1.36} ${r * 0.98},${r * 0.1} Q${r * 0.8},${-r * 0.55} 0,${-r * 0.62} Q${-r * 0.8},${-r * 0.55} ${-r * 0.98},${r * 0.1} Z` }, g);
    svg('path', { fill: 'none', stroke: o.gray, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M0,${-r * 0.64} Q${-r * 0.5},${-r * 0.92} ${-r * 0.82},${-r * 0.4} M0,${-r * 0.64} Q${r * 0.5},${-r * 0.92} ${r * 0.82},${-r * 0.4}` }, g);
  } else {
    const bangs = `Q${r * 0.6},${-r * 0.5} ${r * 0.1},${-r * 0.42} Q${-r * 0.45},${-r * 0.32} ${-r * 0.98},${-r * 0.02}`;
    svg('path', { fill: o.hair, d: `M${-r * 0.98},${-r * 0.02} C${-r},${-r * 1.4} ${r},${-r * 1.4} ${r * 0.98},${-r * 0.1} ${bangs} Z` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M${r * 0.98},${-r * 0.1} ${bangs}` }, g);
    svg('rect', { x: r * 0.3, y: -r * 0.72, width: r * 0.34, height: r * 0.13, rx: r * 0.06, fill: o.clip, stroke: ink, 'stroke-width': r * 0.04, transform: `rotate(-20 ${r * 0.47} ${-r * 0.66})` }, g);
  }
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: o.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.3} Q${sx * r * 0.38},${-r * 0.4} ${sx * r * 0.56},${-r * 0.3}` }, g);
    svg('ellipse', { cx: sx * r * 0.38, cy: -r * 0.02, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
    svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.08, r: r * 0.045, fill: '#fff' }, g);
    if (who === 'daughter') svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.04, 'stroke-linecap': 'round', d: `M${sx * r * 0.46},${-r * 0.14} l${sx * r * 0.1},${-r * 0.06}` }, g);
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.28, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.45 }, g);
    if (who === 'mom') svg('circle', { cx: sx * r * 0.38, cy: -r * 0.02, r: r * 0.24, fill: '#fff', 'fill-opacity': 0.15, stroke: o.glasses, 'stroke-width': r * 0.06 }, g);
  }
  if (who === 'mom') svg('path', { fill: 'none', stroke: o.glasses, 'stroke-width': r * 0.05, d: `M${-r * 0.14},${-r * 0.04} Q0,${-r * 0.12} ${r * 0.14},${-r * 0.04}` }, g);
  svg('path', { fill: 'none', stroke: shade(o.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.16} Q0,${r * 0.24} ${r * 0.06},${r * 0.16}` }, g);
  svg('path', { fill: 'none', stroke: o.lips, 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.44} Q0,${r * 0.62} ${r * 0.18},${r * 0.44}` }, g);
  return g;
}
function portrait3(who, size, bg) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: size, height: size, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: who === 'mom' ? MOM.shirt : DAUGHTER.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  faceFront3(d, 0, 4, 26, who);
  return d.outerHTML;
}
