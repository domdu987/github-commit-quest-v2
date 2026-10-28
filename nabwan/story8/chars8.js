// "312 ชามที่ไม่มีผักชี" cast in the story2 chibi rig: มิน (wavy shoulder-length hair, floral blouse) and ปั้น (side-part hair,
// mustard tee) — a quiet boyfriend who never says it.
const MIN = { skin: '#f2c4a4', skinShade: '#d9a682', hair: '#6b3a2a', hairStyle: 'wavy', clip: '#ffd166', top: 'blouse', sleeve: 'short', shirt: '#c9b6e8', shirtDark: '#a996d0', shirtLight: '#e3d8f6', flower: '#ffffff', pants: '#4a6aa5', pantsDark: '#3c5a90', shoe: '#ffffff', shoeDark: '#d9dde6', sole: '#c9cfda', shoeStyle: 'sneaker', seed: 61 };
const PAN = { skin: '#d9a27a', skinShade: '#bd865f', hair: '#1f1a1c', hairStyle: 'part', top: 'tee', sleeve: 'short', shirt: '#e2a93b', shirtDark: '#c98f26', shirtLight: '#f2c463', pants: '#5c5a4a', pantsDark: '#4a4838', shoeStyle: 'sandal', sole: '#2f3448', seed: 63 };

function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }

// front-facing heads for avatars, chat headers and the first-date photo
function faceFront8(parent, cx, cy, r, who = 'min', o = {}) {
  const c = who === 'pan' ? PAN : MIN, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (who === 'min') {   // wavy hair falls behind the face to the shoulders
    const back = `M${-r * 1.02},${-r * 0.2} C${-r * 1.14},${-r * 1.36} ${r * 1.14},${-r * 1.36} ${r * 1.02},${-r * 0.2} C${r * 1.1},${r * 0.4} ${r * 1.06},${r * 0.86} ${r * 1.0},${r * 1.08} Q${r * 0.86},${r * 1.26} ${r * 0.72},${r * 1.06} Q${r * 0.6},${r * 1.2} ${r * 0.5},${r * 0.98} L${-r * 0.5},${r * 0.98} Q${-r * 0.6},${r * 1.2} ${-r * 0.72},${r * 1.06} Q${-r * 0.86},${r * 1.26} ${-r * 1.0},${r * 1.08} C${-r * 1.06},${r * 0.86} ${-r * 1.1},${r * 0.4} ${-r * 1.02},${-r * 0.2} Z`;
    svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.07, 'stroke-linejoin': 'round', d: back }, g);
  }
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  if (who === 'min') {   // side-swept fringe from a part on her right
    const fr = `Q${r * 0.92},${-r * 0.62} ${r * 0.44},${-r * 0.7} Q${r * 0.05},${-r * 0.6} ${-r * 0.3},${-r * 0.34} Q${-r * 0.62},${-r * 0.12} ${-r * 1.0},${-r * 0.02}`;
    svg('path', { fill: c.hair, d: `M${-r * 1.0},${-r * 0.02} C${-r * 1.06},${-r * 1.3} ${r * 1.06},${-r * 1.36} ${r * 1.0},${-r * 0.14} ${fr.replace(/^Q/, 'L' + (r * 1.0) + ',' + (-r * 0.14) + ' Q')} Z` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: `M${r * 1.0},${-r * 0.14} ${fr}` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${r * 0.44},${-r * 0.7} Q${r * 0.5},${-r * 0.88} ${r * 0.42},${-r * 1.04}` }, g);
    svg('rect', { x: -r * 0.66, y: -r * 0.46, width: r * 0.3, height: r * 0.12, rx: r * 0.06, fill: c.clip, stroke: ink, 'stroke-width': r * 0.035, transform: `rotate(24 ${-r * 0.51} ${-r * 0.4})` }, g);
  } else {   // ปั้น: neat side part
    const fr = `Q${r * 0.8},${-r * 0.5} ${r * 0.3},${-r * 0.58} Q${-r * 0.2},${-r * 0.62} ${-r * 0.5},${-r * 0.4} Q${-r * 0.8},${-r * 0.24} ${-r * 0.98},${-r * 0.06}`;
    svg('path', { fill: c.hair, d: `M${-r * 0.98},${-r * 0.06} C${-r * 1.06},${-r * 1.34} ${r * 1.06},${-r * 1.38} ${r * 0.98},${-r * 0.18} ${fr} Z` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: `M${-r * 0.98},${-r * 0.06} C${-r * 1.06},${-r * 1.34} ${r * 1.06},${-r * 1.38} ${r * 0.98},${-r * 0.18} ${fr}` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.045, 'stroke-linecap': 'round', d: `M${r * 0.3},${-r * 0.58} Q${r * 0.36},${-r * 0.8} ${r * 0.28},${-r * 1.0}` }, g);
    svg('path', { fill: 'none', stroke: shade(c.hair, 50), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', opacity: 0.8, d: `M${-r * 0.5},${-r * 0.8} Q${-r * 0.1},${-r * 1.0} ${r * 0.14},${-r * 0.92}` }, g);
  }
  const sm = o.smile == null ? 0.7 : o.smile;
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.22} Q${sx * r * 0.38},${-r * 0.32} ${sx * r * 0.56},${-r * 0.22}` }, g);
    if (o.happy) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.04} Q${sx * r * 0.38},${-r * 0.12} ${sx * r * 0.38 + r * 0.13},${r * 0.04}` }, g);
    else {
      svg('ellipse', { cx: sx * r * 0.38, cy: r * 0.04, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
      svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.02, r: r * 0.045, fill: '#fff' }, g);
      if (who === 'min') svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.04, 'stroke-linecap': 'round', d: `M${sx * r * 0.5},${-r * 0.08} l${sx * r * 0.08},${-r * 0.06}` }, g);   // lashes
    }
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.32, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: who === 'min' ? 0.55 : 0.4 }, g);
  }
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.2} Q0,${r * 0.28} ${r * 0.06},${r * 0.2}` }, g);
  if (o.grin) svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.22},${r * 0.44} Q0,${r * 0.76} ${r * 0.22},${r * 0.44} Z` }, g);
  else svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.17},${r * 0.48} Q0,${r * (0.48 + 0.16 * (sm - 0.3))} ${r * 0.17},${r * 0.48}` }, g);
  return g;
}
function portrait8(who, size, bg, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: size, height: size, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  const c = who === 'pan' ? PAN : MIN;
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: c.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  faceFront8(d, 0, 4, 25, who, o);
  return d.outerHTML;
}
const minAv = (n = 64, o = {}) => portrait8('min', n, '#fde2e8', o);
const panAv = (n = 64, o = {}) => portrait8('pan', n, '#fff1d6', o);
