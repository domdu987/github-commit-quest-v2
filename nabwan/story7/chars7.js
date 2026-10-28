// "11 ปีที่เพื่อนไม่เคยลืม" cast in the story2 chibi rig: him (spiky hair) and แบงค์ (backwards red cap), now and in
// their ม.4 school uniforms.
const ME = { skin: '#e6b48c', skinShade: '#c99670', hair: '#2a1f1c', hairStyle: 'spiky', top: 'tee', sleeve: 'short', shirt: '#4a6fa5', shirtDark: '#3a5a8c', shirtLight: '#6c8fc4', pants: '#6b7280', pantsDark: '#585f6c', shoeStyle: 'sandal', sole: '#2f3448', seed: 41 };
const BANK = { skin: '#c98d62', skinShade: '#ae7550', hair: '#1f1a1c', hairStyle: 'dad', hat: 'cap', capC: '#e0574b', top: 'hoodie', sleeve: 'long', shirt: '#5fa27f', shirtDark: '#4a8a69', shirtLight: '#7fc29e', pants: '#3b3f58', pantsDark: '#30344a', seed: 43 };
const SCHOOL = { top: 'tee', sleeve: 'short', shirt: '#f7f7f2', shirtDark: '#d9dbe0', shirtLight: '#ffffff', pants: '#2c3e7a', pantsDark: '#24336a', shoe: '#2a2228', shoeDark: '#1d171b', sole: '#4a3e44', shoeStyle: 'sneaker' };
const ME_SCHOOL = Object.assign({}, ME, SCHOOL, { seed: 45 });
const BANK_SCHOOL = Object.assign({}, BANK, SCHOOL, { hat: null, hairStyle: 'fluffy', seed: 47 });

function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }

// front-facing heads for avatars and photos
function faceFront7(parent, cx, cy, r, who = 'me', o = {}) {
  const c = who === 'bank' ? BANK : ME, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  if (who === 'me' || o.school) {
    if (who === 'bank') {   // school-days แบงค์: fluffy hair, no cap
      const puffs = [[-0.62, -0.5, 0.48], [-0.1, -0.82, 0.5], [0.45, -0.62, 0.48], [-0.9, -0.05, 0.3], [0.88, -0.1, 0.3]];
      for (const [x, y, rr] of puffs) svg('circle', { cx: r * x, cy: r * y, r: r * rr + r * 0.06, fill: ink }, g);
      for (const [x, y, rr] of puffs) svg('circle', { cx: r * x, cy: r * y, r: r * rr, fill: c.hair }, g);
    }
  }
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  if (who === 'me') {
    const tips = [[-0.98, -0.2], [-0.82, -0.86], [-0.42, -1.18], [0, -1.3], [0.42, -1.18], [0.82, -0.86], [0.98, -0.2]];
    let d = `M${-r * 0.98},${-r * 0.06}`;
    tips.forEach(([x, y], i) => { d += ` L${r * x},${r * y}`; if (i + 1 < tips.length) { const n = tips[i + 1]; d += ` L${r * (x + n[0]) / 2},${r * ((y + n[1]) / 2 + 0.24)}`; } });
    d += ` L${r * 0.98},${-r * 0.06} Q${r * 0.5},${-r * 0.5} 0,${-r * 0.42} Q${-r * 0.5},${-r * 0.5} ${-r * 0.98},${-r * 0.06} Z`;
    svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round', d }, g);
  } else if (o.school) {
    const bangs = `Q${r * 0.7},${-r * 0.42} ${r * 0.42},${-r * 0.3} Q${r * 0.22},${-r * 0.58} ${-r * 0.05},${-r * 0.36} Q${-r * 0.3},${-r * 0.6} ${-r * 0.5},${-r * 0.32} Q${-r * 0.78},${-r * 0.36} ${-r * 0.98},${-r * 0.05}`;
    svg('path', { fill: c.hair, d: `M${-r * 0.98},${-r * 0.02} C${-r},${-r * 1.4} ${r},${-r * 1.4} ${r * 0.98},${-r * 0.1} ${bangs} Z` }, g);
    svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M${r * 0.98},${-r * 0.1} ${bangs}` }, g);
  } else {
    // backwards red cap
    svg('path', { fill: c.capC, stroke: ink, 'stroke-width': r * 0.07, 'stroke-linejoin': 'round', d: `M${-r * 1.0},${-r * 0.16} C${-r * 1.04},${-r * 1.36} ${r * 1.04},${-r * 1.36} ${r * 1.0},${-r * 0.16} Q0,${-r * 0.36} ${-r * 1.0},${-r * 0.16} Z` }, g);
    svg('path', { fill: shade(c.capC, -20), stroke: ink, 'stroke-width': r * 0.06, d: `M${-r * 0.4},${-r * 0.3} Q0,${-r * 0.16} ${r * 0.4},${-r * 0.3} L${r * 0.3},${-r * 0.44} Q0,${-r * 0.32} ${-r * 0.3},${-r * 0.44} Z` }, g);
    svg('circle', { cx: 0, cy: -r * 1.08, r: r * 0.08, fill: shade(c.capC, -20), stroke: ink, 'stroke-width': r * 0.04 }, g);
  }
  const sm = o.smile == null ? 0.7 : o.smile;
  for (const sx of [-1, 1]) {
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.24} Q${sx * r * 0.38},${-r * 0.34} ${sx * r * 0.56},${-r * 0.24}` }, g);
    if (o.happy) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.02} Q${sx * r * 0.38},${-r * 0.14} ${sx * r * 0.38 + r * 0.13},${r * 0.02}` }, g);
    else {
      svg('ellipse', { cx: sx * r * 0.38, cy: r * 0.02, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
      svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.04, r: r * 0.045, fill: '#fff' }, g);
    }
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.3, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.45 }, g);
  }
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.18} Q0,${r * 0.26} ${r * 0.06},${r * 0.18}` }, g);
  if (o.grin) svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': r * 0.05, d: `M${-r * 0.24},${r * 0.42} Q0,${r * 0.76} ${r * 0.24},${r * 0.42} Z` }, g);
  else svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.46} Q0,${r * (0.46 + 0.16 * (sm - 0.3))} ${r * 0.18},${r * 0.46}` }, g);
  return g;
}
function portrait7(who, size, bg, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: size, height: size, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  const c = who === 'bank' ? (o.school ? BANK_SCHOOL : BANK) : (o.school ? ME_SCHOOL : ME);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: c.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  faceFront7(d, 0, 6, 25, who, o);
  return d.outerHTML;
}
const bankAv = (n = 64, o = {}) => portrait7('bank', n, '#ffe2d6', o);
const meAv = (n = 64, o = {}) => portrait7('me', n, '#dbe7f3', o);
