// "127 ใบสมัคร" cast in the story2 chibi rig: a fresh graduate (side-parted hair, white shirt + tie) and his mom up-country (curly perm)
const GRAD = { skin: '#d9a27a', skinShade: '#bd865f', hair: '#241a17', hairStyle: 'part', top: 'office', tie: '#2c3e7a', tieStripe: '#8fb2ff', sleeve: 'long', shirt: '#f7f7f2', shirtDark: '#d5d8df', shirtLight: '#ffffff', pants: '#2a2a33', pantsDark: '#202028', shoe: '#2f262b', shoeDark: '#221b1f', sole: '#55474e', seed: 21 };
const GRAD_HOME = Object.assign({}, GRAD, { top: 'tee', tie: null, sleeve: 'short', shirt: '#7cbf9a', shirtDark: '#5fa27f', shirtLight: '#a2d9ba', pants: '#5a6378', pantsDark: '#4b5367', shoeStyle: 'sandal', sole: '#3b4a7e' });
const MOM5 = { skin: '#c48a5e', skinShade: '#a8714a', hair: '#3a3034', gray: '#d4cdc6', hairStyle: 'perm', top: 'blouse', sleeve: 'short', shirt: '#4fae9b', shirtDark: '#3a8f7e', shirtLight: '#8fd3c4', flower: '#ffe08a', pants: '#7a4a6a', pantsDark: '#653b57', shoeStyle: 'sandal', sole: '#c94f45', aged: false, lips: '#8a3a3e', seed: 23 };   // no cheek wrinkles: at chibi size they read as whiskers

// front-facing heads for avatars, the video call and the wall photo
function faceFront5(parent, cx, cy, r, who = 'grad', o = {}) {
  const c = who === 'mom' ? MOM5 : GRAD, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (who === 'mom') {
    const curls = [];
    for (let i = 0; i <= 12; i++) { const a = rad(160 + i * 18.3); curls.push([Math.cos(a) * 1.0, Math.sin(a) * 0.92 - 0.06, i % 2 ? 0.26 : 0.3]); }
    for (const [x, y, rr] of curls) svg('circle', { cx: r * x, cy: r * y, r: r * rr + r * 0.06, fill: ink }, g);
    curls.forEach(([x, y, rr], i) => svg('circle', { cx: r * x, cy: r * y, r: r * rr, fill: i === 3 || i === 9 ? c.gray : c.hair }, g));
  } else {
    svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, d: `M${-r * 1.0},${r * 0.1} C${-r * 1.1},${-r * 1.3} ${r * 1.1},${-r * 1.3} ${r * 1.0},${r * 0.1} Z` }, g);
  }
  for (const sx of [-1, 1]) svg('ellipse', { cx: sx * r * 0.95, cy: r * 0.12, rx: r * 0.16, ry: r * 0.2, fill: c.skin, stroke: ink, 'stroke-width': r * 0.06 }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  if (who === 'mom') {
    const fr = [[-0.6, -0.62, 0.22], [-0.25, -0.76, 0.24], [0.12, -0.78, 0.24], [0.48, -0.68, 0.23], [0.78, -0.46, 0.2]];
    for (const [x, y, rr] of fr) svg('circle', { cx: r * x, cy: r * y, r: r * rr + r * 0.05, fill: ink }, g);
    fr.forEach(([x, y, rr], i) => svg('circle', { cx: r * x, cy: r * y, r: r * rr, fill: c.hair }, g));
    svg('path', { fill: 'none', stroke: c.gray, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${r * 0.02},${-r * 0.92} q${r * 0.12},${-r * 0.06} ${r * 0.24},${r * 0.02}` }, g);
  } else {
    // side part: the fringe sweeps from a part on the left across to the right
    const fringe = `M${-r * 0.98},${-r * 0.02} C${-r},${-r * 1.42} ${r},${-r * 1.42} ${r * 0.98},${-r * 0.12} Q${r * 0.7},${-r * 0.52} ${r * 0.05},${-r * 0.5} Q${-r * 0.28},${-r * 0.52} ${-r * 0.4},${-r * 0.78} Q${-r * 0.62},${-r * 0.42} ${-r * 0.98},${-r * 0.02} Z`;
    svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, 'stroke-linejoin': 'round', d: fringe }, g);
    svg('path', { fill: 'none', stroke: shade(c.hair, 45), 'stroke-width': r * 0.06, 'stroke-linecap': 'round', opacity: 0.8, d: `M${-r * 0.1},${-r * 0.9} Q${r * 0.4},${-r * 0.95} ${r * 0.7},${-r * 0.6}` }, g);
  }
  const sm = o.smile == null ? 0.7 : o.smile, cry = o.cry || 0;
  for (const sx of [-1, 1]) {
    const bi = cry ? -r * 0.08 : 0;
    svg('path', { fill: 'none', stroke: c.hair, 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.2},${-r * 0.3 + bi} Q${sx * r * 0.38},${-r * 0.4} ${sx * r * 0.56},${-r * 0.3 - bi * 0.3}` }, g);
    if (o.closed) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${-r * 0.02} Q${sx * r * 0.38},${r * 0.08} ${sx * r * 0.38 + r * 0.13},${-r * 0.02}` }, g);
    else {
      svg('ellipse', { cx: sx * r * 0.38, cy: -r * 0.02, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
      svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.08, r: r * 0.045, fill: '#fff' }, g);
    }
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.28, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
  }
  svg('path', { fill: 'none', stroke: shade(c.skinShade, -15), 'stroke-width': r * 0.05, 'stroke-linecap': 'round', d: `M${-r * 0.06},${r * 0.16} Q0,${r * 0.24} ${r * 0.06},${r * 0.16}` }, g);
  svg('path', { fill: 'none', stroke: c.lips || '#6a2c2e', 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.46 - sm * r * 0.02} Q0,${r * (0.46 + 0.16 * (sm - 0.3))} ${r * 0.18},${r * 0.46 - sm * r * 0.02}` }, g);
  return g;
}
function portrait5(who, size, bg, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: size, height: size, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  if (who === 'mom') svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: MOM5.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  else {
    svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: GRAD.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
    svg('path', { d: 'M-4,32 L4,32 L6,48 L-6,48 Z', fill: GRAD.tie, stroke: INK, 'stroke-width': 2 }, d);
  }
  faceFront5(d, 0, 4, 26, who, o);
  return d.outerHTML;
}
const momAv = (n = 64) => portrait5('mom', n, '#ffe9c4');
const gradAv = (n = 64) => portrait5('grad', n, '#dbe7f3');
function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }
