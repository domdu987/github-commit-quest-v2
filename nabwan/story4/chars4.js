// "47 ครั้งที่ลบข้อความ" cast in the story2 chibi rig: a shy guy with round glasses, a girl with a ponytail
const GUY = { skin: '#e0aa80', skinShade: '#c48f68', hair: '#1f1a1c', hairStyle: 'fluffy', glasses: '#2a2a30', top: 'stripe', sleeve: 'short', shirt: '#f4f1ea', shirtDark: '#d9d3c6', shirtLight: '#ffffff', stripe: '#3b4a7e', sleeveC: '#3b4a7e', pants: '#8a909e', pantsDark: '#737a88', shoeStyle: 'sandal', sole: '#3b4a7e', seed: 11 };
const GIRL = { skin: '#f3c6a5', skinShade: '#dba882', hair: '#5a3424', hairStyle: 'pony', clip: '#ff7aa2', top: 'heartpj', sleeve: 'short', shirt: '#ffe7a8', shirtDark: '#f2cf7c', shirtLight: '#fff3cc', print: '#f07aa8', pants: '#ffc4d2', pantsDark: '#f2a9bb', shoeStyle: 'sandal', sole: '#ff7aa2', lashes: true, lips: '#d0505e', seed: 12 };

// teddy bear (the girl hugs it; the "หมีกอด" sticker is its cartoon twin)
function teddy(parent, x, y, s = 1) {
  const g = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, parent);
  const c = '#c8895a', c2 = '#e8b98a';
  for (const ex of [-34, 34]) { svg('circle', { cx: ex, cy: -78, r: 18, fill: c, stroke: INK, 'stroke-width': 4.5 }, g); svg('circle', { cx: ex, cy: -78, r: 9, fill: c2 }, g); }
  svg('ellipse', { cx: 0, cy: 10, rx: 52, ry: 56, fill: c, stroke: INK, 'stroke-width': 4.5 }, g);
  svg('ellipse', { cx: 0, cy: 18, rx: 30, ry: 32, fill: c2 }, g);
  svg('circle', { cx: 0, cy: -50, r: 44, fill: c, stroke: INK, 'stroke-width': 4.5 }, g);
  svg('ellipse', { cx: 0, cy: -38, rx: 20, ry: 15, fill: c2 }, g);
  svg('ellipse', { cx: 0, cy: -44, rx: 7, ry: 5, fill: INK }, g);
  for (const ex of [-16, 16]) svg('circle', { cx: ex, cy: -58, r: 5, fill: INK }, g);
  svg('path', { d: 'M-6,-34 Q0,-28 6,-34', stroke: INK, 'stroke-width': 3, fill: 'none', 'stroke-linecap': 'round' }, g);
  svg('path', { d: heartPathT(0, 12, 14), fill: '#f07aa8', stroke: INK, 'stroke-width': 3 }, g);
  return g;
}
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }

function faceFront4(parent, cx, cy, r, who = 'girl') {
  const o = who === 'girl' ? GIRL : GUY, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (who === 'girl') {
    svg('path', { fill: o.hair, stroke: ink, 'stroke-width': r * 0.06, d: `M${r * 0.55},${-r * 0.85} C${r * 1.35},${-r * 0.9} ${r * 1.45},${r * 0.2} ${r * 1.25},${r * 0.95} C${r * 1.15},${r * 1.1} ${r * 0.98},${r * 0.95} ${r * 1.0},${r * 0.7} C${r * 1.05},${r * 0.1} ${r * 0.9},${-r * 0.35} ${r * 0.45},${-r * 0.55} Z` }, g);
    svg('ellipse', { cx: r * 0.7, cy: -r * 0.78, rx: r * 0.16, ry: r * 0.2, fill: o.clip, stroke: ink, 'stroke-width': r * 0.05 }, g);
  } else {
    const puffs = [[-0.62, -0.5, 0.48], [-0.1, -0.82, 0.5], [0.45, -0.62, 0.48], [-0.9, -0.05, 0.3], [0.88, -0.1, 0.3]];
    for (const [x, y, rr] of puffs) svg('circle', { cx: r * x, cy: r * y, r: r * rr + r * 0.06, fill: ink }, g);
    for (const [x, y, rr] of puffs) svg('circle', { cx: r * x, cy: r * y, r: r * rr, fill: o.hair }, g);
  }
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: o.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: o.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  const bangs = who === 'girl'
    ? `Q${r * 0.6},${-r * 0.5} ${r * 0.1},${-r * 0.42} Q${-r * 0.45},${-r * 0.32} ${-r * 0.98},${-r * 0.02}`
    : `Q${r * 0.7},${-r * 0.42} ${r * 0.42},${-r * 0.3} Q${r * 0.22},${-r * 0.58} ${-r * 0.05},${-r * 0.36} Q${-r * 0.3},${-r * 0.6} ${-r * 0.5},${-r * 0.32} Q${-r * 0.78},${-r * 0.36} ${-r * 0.98},${-r * 0.05}`;
  svg('path', { fill: o.hair, d: `M${-r * 0.98},${-r * 0.02} C${-r},${-r * 1.4} ${r},${-r * 1.4} ${r * 0.98},${-r * 0.1} ${bangs} Z` }, g);
  svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M${r * 0.98},${-r * 0.1} ${bangs}` }, g);
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: o.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.3} Q${sx * r * 0.38},${-r * 0.4} ${sx * r * 0.56},${-r * 0.3}` }, g);
    svg('ellipse', { cx: sx * r * 0.38, cy: -r * 0.02, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
    svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.08, r: r * 0.045, fill: '#fff' }, g);
    if (who === 'girl') svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.04, 'stroke-linecap': 'round', d: `M${sx * r * 0.46},${-r * 0.14} l${sx * r * 0.1},${-r * 0.06}` }, g);
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.28, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
    if (who === 'guy') svg('circle', { cx: sx * r * 0.38, cy: -r * 0.02, r: r * 0.24, fill: '#fff', 'fill-opacity': 0.15, stroke: o.glasses, 'stroke-width': r * 0.06 }, g);
  }
  if (who === 'guy') svg('path', { fill: 'none', stroke: o.glasses, 'stroke-width': r * 0.05, d: `M${-r * 0.14},${-r * 0.04} Q0,${-r * 0.12} ${r * 0.14},${-r * 0.04}` }, g);
  svg('path', { fill: 'none', stroke: shade(o.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.16} Q0,${r * 0.24} ${r * 0.06},${r * 0.16}` }, g);
  svg('path', { fill: 'none', stroke: o.lips || '#6a2c2e', 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.44} Q0,${r * 0.62} ${r * 0.18},${r * 0.44}` }, g);
  return g;
}
function portrait4(who, size, bg) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: size, height: size, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: who === 'girl' ? GIRL.shirt : GUY.stripe, stroke: INK, 'stroke-width': 2.5 }, d);
  faceFront4(d, 0, 4, 26, who);
  return d.outerHTML;
}
