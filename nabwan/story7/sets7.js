// "11 ปีที่เพื่อนไม่เคยลืม" sets, in the story2 language: his bedroom at night, แบงค์'s room in another city,
// the school canteen in ม.4 (shown sepia), and the หมูกระทะ place at the end.

const leafG = (R, x, y, s, a, c, vein = '#3e3448') => {
  const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
  svg('path', { d: 'M0,0 C40,-60 120,-70 200,-20 C120,10 50,20 0,0 Z', fill: c }, g);
  svg('path', { d: 'M8,-2 C70,-30 130,-34 190,-20', fill: 'none', stroke: vein, 'stroke-width': 3, opacity: 0.5 }, g);
  return g;
};
const swayLeaves = (leaves, t) => leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });

// night window with stars, moon and twinkling city
function nightCity(F, x, y, w, h, seed, frame = '#2a2236') {
  svg('rect', { x, y, width: w, height: h, rx: 8, fill: frame }, F.s);
  svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32, fill: lin(F.defs, [[0, '#141636'], [1, '#2b2c5a']]) }, F.s);
  const r = rng(seed), tw = [];
  for (let i = 0; i < 36; i++) svg('circle', { cx: x + 22 + r() * (w - 44), cy: y + 22 + r() * (h * 0.4), r: 1 + r() * 1.8, fill: '#fff', opacity: 0.3 + r() * 0.5 }, F.s);
  svg('circle', { cx: x + w * 0.72, cy: y + 90, r: 56, fill: rad2(F.defs, [[0, '#fff6dc', 0.5], [1, '#fff6dc', 0]]) }, F.s);
  svg('circle', { cx: x + w * 0.72, cy: y + 90, r: 26, fill: '#f6eed8' }, F.s);
  let bx = x + 16;
  while (bx < x + w - 16) {
    const bw = Math.min(40 + r() * 54, x + w - 16 - bx), bh = 110 + r() * 190, by = y + h - 16 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: r() > 0.5 ? '#22244a' : '#2a2c55' }, F.s);
    for (let wy = by + 14; wy < y + h - 26; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14)
      if (r() > 0.55) tw.push({ el: svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#f6c86a' }, F.s), ph: r() * 40, rate: 0.2 + r() * 0.5 });
    bx += bw + 3;
  }
  svg('rect', { x: x + w / 2 - 3, y: y + 16, width: 6, height: h - 32, fill: frame }, F.s);
  return t => tw.forEach(w => w.el.setAttribute('opacity', (Math.sin((t + w.ph) * w.rate * 6) > -0.85 ? 0.85 : 0.15)));
}
function curtains2(F, x0, x1, y, h, c1, c2, pleat) {
  for (const cx of [x0, x1]) {
    svg('rect', { x: cx, y, width: 86, height: h, rx: 16, fill: lin(F.defs, [[0, c1], [1, c2]], 1, 0) }, F.s);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: y + 10, width: 7, height: h - 20, rx: 3, fill: pleat }, F.s);
  }
}
// the ม.4 photo on his wall: two boys in white school shirts grinning
function schoolPhoto(g, x, y, w = 200) {
  const h = w * 0.86;
  svg('rect', { x, y, width: w, height: h + 34, rx: 4, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4, transform: `rotate(-4 ${x + w / 2} ${y + h / 2})` }, g);
  const ph = svg('g', { transform: `rotate(-4 ${x + w / 2} ${y + h / 2})` }, g);
  svg('rect', { x: x + 10, y: y + 10, width: w - 20, height: h - 14, fill: '#cfe3f2' }, ph);
  for (const [dx, who] of [[0.32, 'me'], [0.68, 'bank']]) {
    svg('path', { d: `M${x + w * dx - 40},${y + h - 4} C${x + w * dx - 38},${y + h - 50} ${x + w * dx + 38},${y + h - 50} ${x + w * dx + 40},${y + h - 4} Z`, fill: '#f7f7f2', stroke: INK, 'stroke-width': 2.5 }, ph);
    faceFront7(ph, x + w * dx, y + h * 0.5, w * 0.15, who, { school: true, happy: true, grin: who === 'bank' });
  }
  const tx = svg('text', { x: x + w / 2, y: y + h + 24, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 20, fill: '#5a4a44' }, ph);
  tx.textContent = 'ม.4/2';
}

// ---------------- his bedroom at night ----------------
function myRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#3f3a5a'], [1, '#544a6a']]) }, F.s);
  const tw = nightCity(F, 600, 200, 400, 470, 51);
  curtains2(F, 566, 966, 180, 560, '#5d6a8a', '#4b5776', '#4a5572');
  svg('rect', { x: 550, y: 172, width: 520, height: 12, rx: 6, fill: '#2f2a40' }, F.s);
  schoolPhoto(F.s, 150, 320, 220);
  svg('rect', { x: 120, y: 600, width: 160, height: 110, rx: 6, fill: '#2b2f4f' }, F.s);
  svg('circle', { cx: 200, cy: 655, r: 34, fill: '#f2c14e', opacity: 0.85 }, F.s);
  svg('path', { d: 'M170,655 L230,655 M200,625 L200,685', stroke: '#2b2f4f', 'stroke-width': 5 }, F.s);   // football poster
  woodFloor(M.s, M.defs, 1330, '#3a3448', '#221d2c', '#2a2130');
  svg('rect', { x: -300, y: 1330, width: 300, height: 1000, fill: '#2a2130' }, M.s); svg('rect', { x: 1080, y: 1330, width: 300, height: 1000, fill: '#2a2130' }, M.s);
  rug(M.s, M.defs, 520, 1560, 460, 100, '#41506a');
  svg('path', { d: 'M616,216 L984,216 L1180,1560 L420,1560 Z', fill: lin(M.defs, [[0, '#c9d6ff', 0.12], [1, '#c9d6ff', 0]]) }, M.s);
  // bed along the left wall
  contactShadow(M.s, M.defs, 330, 1338, 320, 20, 0.45);
  svg('rect', { x: 20, y: 1000, width: 60, height: 330, rx: 14, fill: '#6a5a8a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 40, y: 1200, width: 560, height: 130, rx: 16, fill: '#7a6a9a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 50, y: 1166, width: 540, height: 54, rx: 20, fill: '#eae6f2', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('path', { d: 'M260,1170 Q400,1120 590,1172 L590,1222 Q420,1240 260,1222 Z', fill: '#f2a07a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 90, y: 1120, width: 150, height: 60, rx: 26, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, M.s);
  // nightstand + lamp
  svg('rect', { x: 640, y: 1170, width: 150, height: 160, rx: 8, fill: '#a8744e', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 656, y: 1236, width: 118, height: 8, fill: '#6a4428' }, M.s);
  svg('path', { d: 'M690,1170 L740,1170 L732,1090 L698,1090 Z', fill: '#f2d6a2', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('path', { d: 'M672,1090 L758,1090 L738,1030 L692,1030 Z', fill: lin(M.defs, [[0, '#f6e3bd'], [1, '#e8c98f']]), stroke: INK, 'stroke-width': 4 }, M.s);
  svg('circle', { cx: 715, cy: 1060, r: 280, fill: rad2(M.defs, [[0, '#ffd59a', 0.45], [1, '#ffd59a', 0]]) }, M.s);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 230, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.5);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#24473a'), leafG(R, 1150, 1960, 1.4, -150, '#2b5243')] : [];
  if (R) svg('circle', { cx: 60, cy: 220, r: 90, fill: '#ffcf8a', opacity: 0.22 }, R.s);
  return { people, top, pglow, update(t) { tw(t); swayLeaves(leaves, t); } };
}

// ---------------- แบงค์'s room in another city: warm teal, string lights, shelf ----------------
function bankRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#2f5a5e'], [1, '#3a6a6a']]) }, F.s);
  const tw = nightCity(F, 90, 220, 380, 440, 57, '#1f3a3c');
  const bulbs = [];
  svg('path', { d: 'M40,150 Q540,230 1040,150', fill: 'none', stroke: '#2a3a3a', 'stroke-width': 3 }, F.s);
  for (let k = 0; k < 12; k++) { const u = (k + 0.5) / 12, bx = 40 + 1000 * u, by = 150 + 80 * 4 * u * (1 - u) * 0.5 * 2; const g = svg('g', {}, F.s); svg('circle', { cx: bx, cy: by + 14, r: 18, fill: '#ffd66b', opacity: 0.25 }, g); svg('circle', { cx: bx, cy: by + 14, r: 7, fill: ['#ffd66b', '#ff9fc0', '#7fd6ff'][k % 3] }, g); bulbs.push(g); }
  // shelf with a football trophy and a red cap
  svg('rect', { x: 600, y: 520, width: 380, height: 14, rx: 6, fill: '#c9a27a', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('path', { d: 'M650,520 L700,520 L692,480 L658,480 Z M660,480 C640,440 640,420 675,420 C710,420 710,440 690,480 Z', fill: '#f2c14e', stroke: INK, 'stroke-width': 3.5 }, F.s);
  schoolPhoto(F.s, 760, 330, 180);
  woodFloor(M.s, M.defs, 1330, '#4a3a3a', '#2c2226', '#3a2c2e');
  svg('rect', { x: -300, y: 1330, width: 300, height: 1000, fill: '#2c2226' }, M.s); svg('rect', { x: 1080, y: 1330, width: 300, height: 1000, fill: '#2c2226' }, M.s);
  rug(M.s, M.defs, 560, 1560, 440, 100, '#7a4a5a');
  // low sofa-bed on the right
  contactShadow(M.s, M.defs, 700, 1338, 330, 20, 0.45);
  svg('rect', { x: 420, y: 1200, width: 600, height: 130, rx: 16, fill: '#c96a5a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 420, y: 1060, width: 600, height: 150, rx: 26, fill: '#d97a6a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 860, y: 1110, width: 130, height: 90, rx: 30, fill: '#f6f1e6', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('circle', { cx: 300, cy: 900, r: 260, fill: rad2(M.defs, [[0, '#ffd59a', 0.35], [1, '#ffd59a', 0]]) }, M.s);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 230, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.5);
  return { people, top, pglow, update(t) { tw(t); bulbs.forEach((b, i) => b.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.4 + i)).toFixed(2))); } };
}

// ---------------- the ม.4 canteen (the shot is graded sepia) ----------------
function canteen(S) {
  const F = S.L.far, M = S.L.mid;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#f2e6cc'], [1, '#e6d6b6']]) }, F.s);
  svg('rect', { x: -300, y: 900, width: 1680, height: 440, fill: '#9cc7a4' }, F.s);
  svg('rect', { x: -300, y: 892, width: 1680, height: 14, fill: '#6f9e7a' }, F.s);
  svg('rect', { x: 330, y: 180, width: 420, height: 110, rx: 12, fill: '#2f6f5a', stroke: INK, 'stroke-width': 5 }, F.s);
  const sign = svg('text', { x: 540, y: 255, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 64, fill: '#fff6dc' }, F.s); sign.textContent = 'โรงอาหาร';
  for (const fx of [200, 880]) { svg('rect', { x: fx - 4, y: -300, width: 8, height: 380, fill: '#8a8f99' }, F.s); svg('ellipse', { cx: fx, cy: 90, rx: 120, ry: 14, fill: '#8a8f99' }, F.s); }
  for (const wx of [60, 820]) { svg('rect', { x: wx, y: 380, width: 200, height: 300, rx: 6, fill: '#bfe0f0', stroke: '#8a7a5a', 'stroke-width': 8 }, F.s); svg('rect', { x: wx + 96, y: 380, width: 8, height: 300, fill: '#8a7a5a' }, F.s); }
  svg('rect', { x: -300, y: 1330, width: 1680, height: 1000, fill: '#cbb894' }, M.s);
  for (let i = -3; i < 16; i++) svg('path', { d: `M${i * 100},1330 L${i * 140 - 160},1920`, stroke: '#b8a47c', 'stroke-width': 3 }, M.s);
  const people = svg('g', {}, M.s);
  // long table in front of them with two food trays
  const table = svg('g', {}, M.s);
  svg('rect', { x: 100, y: 1180, width: 880, height: 36, rx: 8, fill: '#d8c08a', stroke: INK, 'stroke-width': 5 }, table);
  for (const lx of [150, 900]) svg('rect', { x: lx, y: 1216, width: 22, height: 140, fill: '#8a8f99', stroke: INK, 'stroke-width': 4 }, table);
  for (const tx of [300, 640]) {
    svg('rect', { x: tx, y: 1150, width: 170, height: 34, rx: 6, fill: '#c9d2dc', stroke: INK, 'stroke-width': 4 }, table);
    svg('ellipse', { cx: tx + 50, cy: 1152, rx: 34, ry: 12, fill: '#f6f1e6', stroke: INK, 'stroke-width': 3 }, table);
    svg('ellipse', { cx: tx + 118, cy: 1154, rx: 30, ry: 10, fill: '#e8a04a', stroke: INK, 'stroke-width': 3 }, table);
  }
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.55);
  return { people, top, update() {} };
}

// ---------------- the หมูกระทะ place at night: string lights, grill, plates ----------------
function mookrata(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#1c1a3a'], [0.7, '#3a2a4a'], [1, '#5a3a4a']]) }, F.s);
  const bulbs = [];
  for (const [y0, sag, n, sd] of [[560, 50, 13, 0], [700, 40, 11, 1]]) {
    svg('path', { d: `M-100,${y0} Q540,${y0 + sag * 2} 1180,${y0}`, fill: 'none', stroke: '#1a1428', 'stroke-width': 3 }, F.s);
    for (let k = 0; k < n; k++) { const u = (k + 0.5) / n, bx = -100 + 1280 * u, by = y0 + sag * 4 * u * (1 - u); const g = svg('g', {}, F.s); svg('circle', { cx: bx, cy: by + 12, r: 26, fill: '#ffd66b', opacity: 0.22 }, g); svg('circle', { cx: bx, cy: by + 12, r: 9, fill: '#ffe2a8' }, g); bulbs.push(g); }
  }
  for (let i = 0; i < 4; i++) svg('rect', { x: -40 + i * 300, y: 820, width: 200, height: 340, rx: 10, fill: '#2a2440', opacity: 0.9 }, F.s);   // other tables, out of focus
  svg('rect', { x: -300, y: 1100, width: 1680, height: 900, fill: '#3a2a2e' }, M.s);
  const people = svg('g', {}, M.s);
  // the table + grill between them
  const table = svg('g', {}, M.s);
  svg('rect', { x: 140, y: 1150, width: 800, height: 40, rx: 10, fill: '#c9a27a', stroke: INK, 'stroke-width': 5 }, table);
  const ging = uidS('ging'), pat = svg('pattern', { id: ging, width: 44, height: 44, patternUnits: 'userSpaceOnUse' }, M.defs);
  svg('rect', { width: 44, height: 44, fill: '#e6d3bf' }, pat);
  svg('rect', { width: 22, height: 44, fill: '#c9544e', opacity: 0.38 }, pat);
  svg('rect', { width: 44, height: 22, fill: '#c9544e', opacity: 0.38 }, pat);
  svg('rect', { x: 180, y: 1190, width: 720, height: 210, fill: `url(#${ging})`, stroke: INK, 'stroke-width': 5 }, table);
  svg('path', { d: 'M180,1190 L900,1190 L900,1214 ' + Array.from({ length: 18 }, (_, i) => `Q${900 - i * 40 - 20},1234 ${900 - (i + 1) * 40},1214`).join(' ') + ' Z', fill: '#e8d2bf', stroke: INK, 'stroke-width': 4 }, table);
  svg('path', { d: 'M470,1150 L610,1150 L596,1070 L484,1070 Z', fill: '#c96a3a', stroke: INK, 'stroke-width': 5 }, table);   // charcoal bucket
  svg('ellipse', { cx: 540, cy: 1066, rx: 96, ry: 18, fill: '#6b7280', stroke: INK, 'stroke-width': 5 }, table);
  svg('path', { d: 'M470,1062 Q540,980 610,1062 Z', fill: '#9aa3b2', stroke: INK, 'stroke-width': 5 }, table);   // the domed pan
  for (const [mx, my] of [[512, 1030], [548, 1012], [578, 1036]]) svg('ellipse', { cx: mx, cy: my, rx: 14, ry: 7, fill: '#e8a0a0', stroke: INK, 'stroke-width': 2.5 }, table);
  for (const [px, c] of [[290, '#e8a0a0'], [780, '#7fc29e']]) { svg('ellipse', { cx: px, cy: 1146, rx: 70, ry: 16, fill: '#f6f1e6', stroke: INK, 'stroke-width': 4 }, table); svg('ellipse', { cx: px, cy: 1138, rx: 46, ry: 10, fill: c }, table); }
  const glow = svg('circle', { cx: 540, cy: 1060, r: 260, fill: rad2(M.defs, [[0, '#ffb070', 0.45], [1, '#ffb070', 0]]) }, M.s);
  const smoke = Array.from({ length: 6 }, () => svg('circle', { r: 26, fill: '#f6f1e6', opacity: 0 }, M.s));
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  return {
    people, top,
    update(t) {
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2 + i * 1.3)).toFixed(2)));
      glow.setAttribute('opacity', (0.85 + 0.15 * Math.sin(t * 7) * Math.sin(t * 3.1)).toFixed(3));
      smoke.forEach((s, i) => { const k = ((t * 0.5 + i / 6) % 1); setA(s, { cx: (540 + Math.sin(k * 6 + i) * 30).toFixed(1), cy: (990 - k * 380).toFixed(1), r: (18 + k * 40).toFixed(1), opacity: (0.35 * Math.sin(Math.PI * k)).toFixed(3) }); });
    },
  };
}
