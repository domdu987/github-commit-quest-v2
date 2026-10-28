// "52 ปีกับกระทงสองใบ" sets: the river pier on Loy Krathong night (full moon, far-bank temple lights, drifting krathongs)
// and ตา's wooden house at night. Krathong builder used both in the world and as an icon.

// banana-leaf krathong (side-front view), centred on its base at 0,0. Returns { g, flame, glow }
function krathong(parent, x, y, s = 1, o = {}) {
  const g = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, parent);
  const glow = svg('ellipse', { cx: 0, cy: -60, rx: 120, ry: 110, fill: 'url(#ktglow)', opacity: o.lit === false ? 0 : 1 }, g);
  svg('ellipse', { cx: 0, cy: 6, rx: 62, ry: 14, fill: '#000', opacity: 0.22 }, g);
  svg('path', { d: 'M-60,0 Q-60,18 0,18 Q60,18 60,0 L56,-14 Q0,-2 -56,-14 Z', fill: '#c9b07a', stroke: INK, 'stroke-width': 4 }, g);   // banana-trunk base
  // folded leaf petals all round, two layers
  for (const [ry, n, w, h, c] of [[-12, 9, 22, 34, '#3f8f4a'], [-22, 7, 20, 30, '#5fb05a']]) {
    for (let i = 0; i < n; i++) {
      const u = (i + 0.5) / n, px = -54 + 108 * u, py = ry - Math.sin(Math.PI * u) * 4;
      svg('path', { d: `M${px - w / 2},${py} L${px},${py - h} L${px + w / 2},${py} Z`, fill: c, stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
      svg('path', { d: `M${px},${py - h + 6} L${px},${py - 2}`, stroke: shade(c, 30), 'stroke-width': 2 }, g);
    }
  }
  // flowers: a pink lotus bud in the middle, marigolds round it
  for (const [fx, fy] of [[-34, -34], [-14, -40], [16, -40], [36, -34]]) {
    for (let k = 0; k < 6; k++) svg('circle', { cx: fx + Math.cos(k * 1.047) * 6, cy: fy + Math.sin(k * 1.047) * 5, r: 6, fill: '#f5a524', stroke: '#c97a10', 'stroke-width': 1.5 }, g);
    svg('circle', { cx: fx, cy: fy, r: 4, fill: '#ffd34a' }, g);
  }
  svg('path', { d: 'M0,-34 C-20,-46 -14,-74 0,-86 C14,-74 20,-46 0,-34 Z', fill: o.c || '#f07aa8', stroke: INK, 'stroke-width': 3.5 }, g);
  svg('path', { d: 'M0,-38 C-8,-50 -6,-66 0,-78', fill: 'none', stroke: '#ffd0e0', 'stroke-width': 3 }, g);
  // incense + candle
  for (const ix of [-22, -16, -10]) svg('path', { d: `M${ix},-40 L${ix - 6},-104`, stroke: '#8a3a2a', 'stroke-width': 3 }, g);
  svg('rect', { x: 14, y: -96, width: 12, height: 56, rx: 3, fill: '#fff3c4', stroke: INK, 'stroke-width': 3 }, g);
  const flame = svg('g', { opacity: o.lit === false ? 0 : 1 }, g);
  svg('path', { d: 'M20,-118 C28,-106 28,-100 20,-94 C12,-100 12,-106 20,-118 Z', fill: '#ffb03a', stroke: INK, 'stroke-width': 2.5 }, flame);
  svg('path', { d: 'M20,-110 C23,-105 23,-102 20,-99 C17,-102 17,-105 20,-110 Z', fill: '#fff3c4' }, flame);
  if (o.tag) {
    const tg = svg('g', { transform: 'translate(-48,-6) rotate(-8)' }, g);
    svg('rect', { x: -4, y: -14, width: 46, height: 22, rx: 5, fill: '#fffaf0', stroke: INK, 'stroke-width': 2.5 }, tg);
    const tx = svg('text', { x: 19, y: 3, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 15, fill: '#8a3a2a' }, tg); tx.textContent = o.tag;
  }
  return { g, flame, glow };
}
// the warm candle-glow gradient, shared by every krathong in a shot
function ktDefs(defs) {
  const r = svg('radialGradient', { id: 'ktglow' }, defs);
  svg('stop', { offset: 0, 'stop-color': '#ffd27a', 'stop-opacity': 0.5 }, r);
  svg('stop', { offset: 1, 'stop-color': '#ffd27a', 'stop-opacity': 0 }, r);
}
const flickerK = (k, t, i = 0) => k.flame.setAttribute('transform', `translate(20,-94) scale(${(1 + 0.1 * Math.sin(t * 21 + i)).toFixed(3)},${(1 + 0.16 * Math.sin(t * 15 + i * 2)).toFixed(3)}) translate(-20,94)`);

// ---------------- ตา's wooden house at night: ยาย's photo on the wall, banana leaves on the mat ----------------
function yaiPhoto(g, x, y, w = 190) {
  const h = w * 1.18;
  svg('rect', { x, y, width: w, height: h, rx: 6, fill: '#c9a24a', stroke: INK, 'stroke-width': 5 }, g);
  svg('rect', { x: x + 14, y: y + 14, width: w - 28, height: h - 28, fill: '#f2e4f6' }, g);
  svg('path', { d: `M${x + w * 0.2},${y + h - 14} C${x + w * 0.22},${y + h * 0.72} ${x + w * 0.78},${y + h * 0.72} ${x + w * 0.8},${y + h - 14} Z`, fill: YAI.shirt, stroke: INK, 'stroke-width': 3 }, g);
  faceElder(g, x + w / 2, y + h * 0.48, w * 0.21, 'yai');
  // jasmine garland draped over the corner
  for (let k = 0; k < 9; k++) svg('circle', { cx: x + 10 + k * 10, cy: y + 8 + Math.sin(k / 8 * Math.PI) * 26, r: 6, fill: '#fffaf0', stroke: '#c9c0a8', 'stroke-width': 1.5 }, g);
  svg('circle', { cx: x + 50, cy: y + 40, r: 8, fill: '#e0574b' }, g);
}
// ---------------- the river pier on Loy Krathong night ----------------
// The pier runs in from the left; the river fills the rest of the frame down to the bottom edge, so krathongs set
// down at the pier's end float out to the right and away toward the moon. mode 'memory' is the same place years ago.
function riverPier(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  ktDefs(M.defs);
  const mx = o.moonX ?? 790, my = o.moonY ?? 300;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1120, fill: lin(F.defs, [[0, '#1c1c4a'], [0.5, '#3f3068'], [1, '#9a5470']]) }, F.s);
  svg('ellipse', { cx: 540, cy: 760, rx: 1000, ry: 220, fill: rad2(F.defs, [[0, '#ffb070', 0.35], [1, '#ffb070', 0]]) }, F.s);
  const r = rng(101), stars = [];
  for (let i = 0; i < 60; i++) stars.push(svg('circle', { cx: -200 + r() * 1480, cy: -250 + r() * 760, r: 0.8 + r() * 1.8, fill: '#fff', opacity: 0.3 + r() * 0.5 }, F.s));
  svg('circle', { cx: mx, cy: my, r: 260, fill: rad2(F.defs, [[0, '#fff1c4', 0.5], [1, '#fff1c4', 0]]) }, F.s);
  svg('circle', { cx: mx, cy: my, r: 96, fill: '#fff6dc' }, F.s);
  svg('circle', { cx: mx - 28, cy: my - 20, r: 17, fill: '#f2e6c4', opacity: 0.7 }, F.s); svg('circle', { cx: mx + 32, cy: my + 24, r: 12, fill: '#f2e6c4', opacity: 0.6 }, F.s);
  // sky lanterns drifting up, and small distant fireworks over the far bank
  const lanterns = Array.from({ length: 9 }, () => ({ x: -100 + r() * 1300, y0: 500 + r() * 400, sp: 10 + r() * 14, ph: r() * 9, s: 0.5 + r() * 0.6, el: svg('g', {}, F.s) }));
  lanterns.forEach(l => { svg('circle', { r: 26, fill: rad2(F.defs, [[0, '#ffcf7a', 0.55], [1, '#ffcf7a', 0]]) }, l.el); svg('path', { d: 'M-8,-10 L8,-10 L10,10 L-10,10 Z', fill: '#ffd27a', stroke: '#c9752a', 'stroke-width': 1.5 }, l.el); svg('rect', { x: -4, y: 4, width: 8, height: 5, fill: '#fff6dc' }, l.el); });
  const fw = Array.from({ length: 3 }, (_, i) => ({ x: 120 + i * 360 + r() * 100, y: 360 + r() * 200, t0: i * 2.3 + r(), c: ['#ffd66b', '#ff9fc0', '#9fe0ff'][i], g: svg('g', {}, F.s) }));
  fw.forEach(f => { for (let k = 0; k < 14; k++) svg('circle', { r: 2.6, fill: f.c }, f.g); });
  // far bank: trees, a temple with a chedi and its lights, string lights along the bank
  svg('path', { d: 'M-300,860 L-300,770 Q-200,700 -120,760 Q-40,690 60,750 Q140,700 220,760 L1380,760 L1380,860 Z', fill: '#1d1830' }, F.s);
  svg('path', { d: 'M500,770 L500,640 L560,590 L620,640 L620,770 Z M450,700 L670,700 L648,664 L472,664 Z', fill: '#2a2140' }, F.s);
  svg('path', { d: 'M560,590 L560,500', stroke: '#2a2140', 'stroke-width': 7 }, F.s);
  for (let k = 0; k < 7; k++) svg('circle', { cx: 470 + k * 30, cy: 700, r: 4, fill: '#ffd27a' }, F.s);
  for (const tx of [820, 960, 1100, 120, -40]) svg('path', { d: `M${tx},770 Q${tx - 40},700 ${tx},650 Q${tx + 40},700 ${tx},770 Z`, fill: '#221c36' }, F.s);
  const bulbs = [];
  svg('path', { d: 'M-100,710 Q300,760 700,710 Q1000,760 1300,710', fill: 'none', stroke: '#2a2236', 'stroke-width': 2 }, F.s);
  for (let k = 0; k < 24; k++) { const u = k / 23, bx = -100 + 1400 * u, by = 710 + 34 * Math.sin(Math.PI * ((u * 2) % 1)); bulbs.push(svg('circle', { cx: bx, cy: by + 6, r: 5, fill: ['#ffd66b', '#ff9fc0', '#7fd6ff'][k % 3] }, F.s)); }
  // the river: far water with the moon's broken reflection and far krathong lights
  svg('rect', { x: -300, y: 780, width: 1680, height: 1700, fill: lin(F.defs, [[0, '#4a3a72'], [0.35, '#30295e'], [1, '#1a1838']]) }, F.s);
  svg('ellipse', { cx: 540, cy: 800, rx: 1000, ry: 90, fill: rad2(F.defs, [[0, '#ffb070', 0.3], [1, '#ffb070', 0]]) }, F.s);
  // reflections of the bank lights and the temple, wobbling
  const streaks = [];
  for (let k = 0; k < 24; k += 2) { const bx = -100 + 1400 * (k / 23); streaks.push(svg('rect', { x: bx - 3, y: 790, width: 6, height: 120 + (k % 5) * 20, rx: 3, fill: lin(F.defs, [[0, ['#ffd66b', '#ff9fc0', '#7fd6ff'][k % 3], 0.6], [1, '#ffd66b', 0]]) }, F.s)); }
  for (let k = 0; k < 7; k++) streaks.push(svg('rect', { x: 467 + k * 30, y: 790, width: 6, height: 160, rx: 3, fill: lin(F.defs, [[0, '#ffd27a', 0.7], [1, '#ffd27a', 0]]) }, F.s));
  const glints = Array.from({ length: 46 }, () => ({ el: svg('rect', { width: 10 + r() * 22, height: 3, rx: 1.5, fill: '#ffe8b0' }, F.s), x: -200 + r() * 1480, y: 800 + r() * 900, ph: r() * 9 }));
  const refl = Array.from({ length: 12 }, (_, i) => svg('rect', { x: mx - 70 + (i % 3) * 16, y: 800 + i * 46, width: 140 - i * 7, height: 6, rx: 3, fill: '#fff1c4', opacity: 0.55 - i * 0.035 }, F.s));
  const far = Array.from({ length: 22 }, () => ({ el: svg('circle', { r: 3 + r() * 4, fill: '#ffd27a' }, F.s), x0: r() * 1400 - 200, y: 800 + r() * 420, sp: 6 + r() * 12, ph: r() * 6 }));
  // near water: ripples, lit krathongs from other people drifting past with their reflections
  const ripples = Array.from({ length: 16 }, (_, i) => svg('path', { fill: 'none', stroke: '#8a86c8', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0.35 }, M.s));
  const water = svg('g', {}, M.s);   // krathongs set on the water live here
  const passers = Array.from({ length: 8 }, (_, i) => { const sc = [0.34, 0.42, 0.5, 0.38, 0.6, 0.46, 0.36, 0.55][i]; const rf = ktReflection(water, M.defs); const k = krathong(water, 0, 0, sc, { c: ['#f07aa8', '#f5a524', '#ffffff', '#c9a8e8'][i % 4] }); return { k, rf, sc, x0: 90 + i * 190, y: 960 + sc * 420 + (i % 3) * 30, sp: 6 + i * 1.5 }; });
  // the pier: plank deck from the left edge to x 600, posts into the water
  const pier = svg('g', {}, M.s);
  for (const px of [40, 300, 560]) { svg('rect', { x: px, y: 1360, width: 34, height: 220, fill: '#3a2620', stroke: INK, 'stroke-width': 4 }, pier); svg('ellipse', { cx: px + 17, cy: 1580, rx: 40, ry: 8, fill: '#8a86c8', opacity: 0.4 }, pier); }
  svg('rect', { x: -300, y: 1300, width: 920, height: 70, fill: '#7a5440', stroke: INK, 'stroke-width': 5 }, pier);
  svg('path', { d: 'M-300,1300 L620,1300 L600,1268 L-300,1268 Z', fill: '#9a6e52', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, pier);
  for (let x = -280; x < 600; x += 70) svg('path', { d: `M${x},1270 L${x + 4},1298`, stroke: '#6a4632', 'stroke-width': 3 }, pier);
  for (const [px, top] of [[600, 860], [40, 900]]) {   // lantern poles with hanging paper lanterns
    svg('rect', { x: px - 9, y: top, width: 18, height: 1300 - top, rx: 6, fill: '#5a3a2a', stroke: INK, 'stroke-width': 4 }, pier);
    svg('path', { d: `M${px},${top + 10} L${px - 60},${top + 10}`, stroke: '#5a3a2a', 'stroke-width': 8 }, pier);
  }
  svg('path', { d: 'M40,920 Q320,1010 600,880', fill: 'none', stroke: '#2a1a14', 'stroke-width': 3 }, pier);
  const pierBulbs = [];
  for (let k = 0; k < 9; k++) { const u = (k + 0.5) / 9, bx = 40 + 560 * u, by = 920 + (880 - 920) * u + 4 * 90 * u * (1 - u) * 0.9; const b = svg('g', {}, pier); svg('circle', { cx: bx, cy: by + 10, r: 22, fill: ['#ffd66b', '#ff9fc0', '#ffe8b0'][k % 3], opacity: 0.25 }, b); svg('circle', { cx: bx, cy: by + 10, r: 7, fill: ['#ffd66b', '#ff9fc0', '#ffe8b0'][k % 3] }, b); pierBulbs.push(b); }
  const lanterns2 = [];
  for (const [lx, ly] of [[540, 880], [-20, 920]]) {
    const lg = svg('g', {}, pier);
    svg('path', { d: `M${lx},${ly} L${lx},${ly + 26}`, stroke: '#2a1a14', 'stroke-width': 3 }, lg);
    svg('circle', { cx: lx, cy: ly + 70, r: 150, fill: rad2(M.defs, [[0, '#ffb060', 0.45], [1, '#ffb060', 0]]), style: 'mix-blend-mode:screen' }, lg);
    svg('ellipse', { cx: lx, cy: ly + 66, rx: 34, ry: 40, fill: '#e0453b', stroke: INK, 'stroke-width': 4 }, lg);
    for (const dx of [-16, 0, 16]) svg('path', { d: `M${lx + dx},${ly + 28} Q${lx + dx * 1.6},${ly + 66} ${lx + dx},${ly + 104}`, fill: 'none', stroke: '#b8322a', 'stroke-width': 2.5 }, lg);
    svg('rect', { x: lx - 14, y: ly + 22, width: 28, height: 8, rx: 3, fill: '#f2c14e', stroke: INK, 'stroke-width': 2.5 }, lg);
    svg('rect', { x: lx - 14, y: ly + 102, width: 28, height: 8, rx: 3, fill: '#f2c14e', stroke: INK, 'stroke-width': 2.5 }, lg);
    svg('path', { d: `M${lx},${ly + 110} L${lx},${ly + 140}`, stroke: '#f2c14e', 'stroke-width': 4 }, lg);
    lanterns2.push(lg);
  }
  lightPool(pier, M.defs, 470, 1286, 300, 34, '#ffb060', 0.45);
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  // moonlight path on the near water
  const shaft = lightShaft(M.s, M.defs, [[mx - 60, 820], [mx + 60, 820], [mx + 220, 1920], [mx - 180, 1920]], '#fff1c4', 0.12, 105, 0);
  vignette(M.s, M.defs, 0.5);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 7, [-150, -100, 1230, 300], ['#ffd27a', '#ff9fc0', '#ffe8b0'], 107, { rMin: 40, rMax: 100, op: 0.45 });
  return {
    people, top, water, shadowL, light: { ux: 0.62, uy: -0.78, lx: 560 },
    update(t) {
      stars.forEach((s2, i) => { if (i % 3 === 0) s2.setAttribute('opacity', (0.4 + 0.4 * Math.sin(t * 2 + i)).toFixed(2)); });
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.2 + i * 1.3)).toFixed(2)));
      refl.forEach((e, i) => e.setAttribute('transform', `translate(${(Math.sin(t * 1.6 + i) * 12).toFixed(1)},0)`));
      far.forEach(f => { const x = ((f.x0 + t * f.sp) % 1500 + 1500) % 1500 - 200; setA(f.el, { cx: x.toFixed(1), cy: (f.y + Math.sin(t * 1.4 + f.ph) * 3).toFixed(1), opacity: (0.6 + 0.4 * Math.sin(t * 5 + f.ph)).toFixed(2) }); });
      lanterns.forEach(l => { const y = l.y0 - ((t * l.sp + l.ph * 40) % 900); l.el.setAttribute('transform', `translate(${(l.x + Math.sin(t * 0.5 + l.ph) * 20).toFixed(1)},${y.toFixed(1)}) scale(${l.s.toFixed(2)})`); l.el.setAttribute('opacity', (Math.min(1, (y + 200) / 300)).toFixed(2)); });
      fw.forEach(f => { const k = ((t - f.t0) % 4.2 + 4.2) % 4.2 / 1.1; [...f.g.children].forEach((c, i) => { const a = i * 2 * Math.PI / 14; const on = k < 1; setA(c, { cx: (f.x + Math.cos(a) * 60 * ease.outCubic(Math.min(k, 1))).toFixed(1), cy: (f.y + Math.sin(a) * 60 * ease.outCubic(Math.min(k, 1)) + 20 * k * k).toFixed(1), opacity: on ? (1 - k).toFixed(2) : 0 }); }); });
      ripples.forEach((rp, i) => { const y = 1100 + (i % 8) * 100 + (i > 7 ? 40 : 0), x = ((i * 173 + t * 14) % 1400) - 200; rp.setAttribute('d', `M${x.toFixed(1)},${y} q20,-6 40,0 q20,6 40,0`); });
      passers.forEach(p => { const x = ((p.x0 + t * p.sp) % 1500) - 200, y = p.y + Math.sin(t * 1.3 + p.x0) * 3; p.k.g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${p.sc})`); flickerK(p.k, t, p.x0); p.rf(x, y, p.sc, t + p.x0); });
      streaks.forEach((e, i) => e.setAttribute('transform', `translate(${(Math.sin(t * 2 + i) * 4).toFixed(1)},0) scale(1,${(1 + 0.1 * Math.sin(t * 3 + i)).toFixed(3)})`));
      glints.forEach(g => setA(g.el, { x: (g.x + Math.sin(t * 0.8 + g.ph) * 10).toFixed(1), y: g.y.toFixed(1), opacity: Math.max(0, Math.sin(t * 2.4 + g.ph)).toFixed(2) }));
      shaft(t); if (bok) bok(t);
      pierBulbs.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2.6 + i * 1.9)).toFixed(2)));
      lanterns2.forEach((l, i) => l.setAttribute('transform', `rotate(${(Math.sin(t * 1.1 + i) * 2).toFixed(2)} ${i ? -20 : 540} ${i ? 920 : 880})`));
    },
  };
}
// reflection streak under a lit krathong on water (world coords); returns update(x, y, s, t)
function ktReflection(parent, defs) {
  const e = svg('ellipse', { rx: 18, ry: 70, fill: rad2(defs, [[0, '#ffd27a', 0.55], [1, '#ffd27a', 0]]), style: 'mix-blend-mode:screen' }, parent);
  return (x, y, s, t) => setA(e, { cx: (x + 10 * s + Math.sin(t * 3) * 3 * s).toFixed(1), cy: (y + 70 * s).toFixed(1), rx: (16 * s * (1 + 0.15 * Math.sin(t * 5))).toFixed(1), ry: (70 * s).toFixed(1) });
}

// ---------------- the veranda of ตา's teak house at night ----------------
// open veranda under the eaves: a bulb hanging from the beam, ยาย's photo on the wall, the village and a palm against
// the night sky past the railing, a mat with banana leaves; ยาย's cushion beside ตา's (empty now unless o.yai)
function veranda(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  ktDefs(M.defs);
  svg('rect', { x: -300, y: -300, width: 1680, height: 1700, fill: lin(F.defs, [[0, '#121838'], [0.7, '#2a2c58'], [1, '#43355e']]) }, F.s);
  const r = rng(111);
  for (let i = 0; i < 40; i++) svg('circle', { cx: 500 + r() * 800, cy: -200 + r() * 700, r: 0.8 + r() * 1.6, fill: '#fff', opacity: 0.3 + r() * 0.5 }, F.s);
  svg('circle', { cx: 930, cy: 260, r: 150, fill: rad2(F.defs, [[0, '#fff1c4', 0.4], [1, '#fff1c4', 0]]) }, F.s);
  svg('circle', { cx: 930, cy: 260, r: 54, fill: '#fff6dc' }, F.s);
  // village silhouettes with lit windows, a coconut palm
  svg('path', { d: 'M440,1000 L440,880 L520,830 L600,880 L600,1000 Z M640,1000 L640,900 L730,850 L820,900 L820,1000 Z M860,1000 L860,870 L960,820 L1060,870 L1060,1000 Z', fill: '#1a1a34' }, F.s);
  for (const [wx, wy] of [[500, 920], [700, 930], [780, 930], [930, 905], [1000, 920]]) svg('rect', { x: wx, y: wy, width: 18, height: 22, fill: '#ffcf7a', opacity: 0.85 }, F.s);
  svg('path', { d: 'M760,1000 Q770,760 820,560', fill: 'none', stroke: '#1a1a34', 'stroke-width': 16 }, F.s);
  for (const a of [-170, -130, -90, -50, -10, 30]) svg('path', { d: `M820,560 q${(Math.cos(rad(a)) * 90).toFixed(0)},${(Math.sin(rad(a)) * 60 - 30).toFixed(0)} ${(Math.cos(rad(a)) * 170).toFixed(0)},${(Math.sin(rad(a)) * 110 + 30).toFixed(0)}`, fill: 'none', stroke: '#1a1a34', 'stroke-width': 14, 'stroke-linecap': 'round' }, F.s);
  const flies = Array.from({ length: 10 }, () => ({ el: svg('circle', { r: 3.4, fill: '#f6f2a0' }, F.s), x: 450 + r() * 650, y: 820 + r() * 260, ph: r() * 9 }));
  // the house wall on the left: teak planks, a doorway, ยาย's photo, a calendar
  const wall = svg('g', {}, F.s);
  const tones = ['#8a5a36', '#965f3a', '#8e5c38', '#9c6640'];
  for (let i = -4; i < 6; i++) { svg('rect', { x: i * 84, y: -300, width: 84, height: 1700, fill: tones[(i + 12) % 4] }, wall); svg('rect', { x: i * 84, y: -300, width: 3, height: 1700, fill: '#5a3a22', opacity: 0.6 }, wall); }
  svg('rect', { x: 420, y: -300, width: 26, height: 1700, fill: '#6a4428', stroke: INK, 'stroke-width': 4 }, wall);   // corner post
  svg('rect', { x: 40, y: 560, width: 220, height: 840, fill: '#2a1a14', stroke: '#5a3a22', 'stroke-width': 16 }, wall);   // doorway into the house
  svg('rect', { x: 52, y: 572, width: 196, height: 820, fill: lin(F.defs, [[0, '#5a3a24'], [1, '#2a1a14']]) }, wall);
  const photoGlow = svg('circle', { cx: 340, cy: 400, r: 170, fill: rad2(F.defs, [[0, '#ffe2a8', 0.45], [1, '#ffe2a8', 0]]) }, wall);
  yaiPhoto(wall, 270, 300, 150);
  // roof eave and beam across the top, the bulb hanging from it
  svg('path', { d: 'M-300,-300 L1380,-300 L1380,120 L-300,190 Z', fill: '#4a2e1e', stroke: INK, 'stroke-width': 5 }, F.s);
  for (let x = -260; x < 1380; x += 90) svg('path', { d: `M${x},${190 - (x + 300) * 0.042} L${x + 40},-300`, stroke: '#3a2416', 'stroke-width': 6 }, F.s);
  // veranda railing behind ตา (mid layer), floor planks
  svg('rect', { x: -300, y: 1380, width: 1680, height: 1000, fill: lin(M.defs, [[0, '#a87850'], [1, '#6a4630']]) }, M.s);
  for (let y = 1380, k = 0; y < 2300; y += 54 + k * 12, k++) svg('rect', { x: -300, y, width: 1680, height: 4, fill: '#5a3a26', opacity: 0.7 }, M.s);
  const rail = svg('g', {}, M.s);
  svg('rect', { x: 446, y: 1060, width: 900, height: 22, rx: 4, fill: '#8a5a36', stroke: INK, 'stroke-width': 4 }, rail);
  for (let x = 470; x < 1340; x += 52) svg('rect', { x, y: 1082, width: 18, height: 300, fill: '#7a4e30', stroke: INK, 'stroke-width': 3 }, rail);
  svg('rect', { x: 446, y: 1360, width: 900, height: 22, fill: '#7a4e30', stroke: INK, 'stroke-width': 4 }, rail);
  wallAO(M.s, M.defs, 1382, { op: 0.3 });
  const shadowL = svg('g', {}, M.s);
  const bulbX = 560, bulbY = 520;
  svg('path', { d: `M${bulbX},-300 L${bulbX},${bulbY - 30}`, stroke: '#2a1a14', 'stroke-width': 3 }, M.s);
  const bulb = svg('g', {}, M.s);
  svg('circle', { cx: bulbX, cy: bulbY, r: 360, fill: rad2(M.defs, [[0, '#ffd59a', 0.42], [0.5, '#ffd59a', 0.14], [1, '#ffd59a', 0]]), style: 'mix-blend-mode:screen' }, bulb);
  svg('path', { d: `M${bulbX - 14},${bulbY - 30} L${bulbX + 14},${bulbY - 30} L${bulbX + 10},${bulbY - 12} L${bulbX - 10},${bulbY - 12} Z`, fill: '#3a2a24' }, bulb);
  svg('circle', { cx: bulbX, cy: bulbY, r: 20, fill: '#fff1c4', stroke: '#e0b04a', 'stroke-width': 3 }, bulb);
  lightPool(M.s, M.defs, bulbX, 1440, 420, 80, '#ffd59a', 0.4);
  const moths = floaters(M.s, [bulbX - 90, bulbY - 80, bulbX + 90, bulbY + 60], 7, 113, { color: '#fff6dc', rMin: 2, rMax: 4, speed: 40, op: 0.7, base: 0.2 });
  // the mat: banana leaves, a bowl of flowers, pins, scissors; ยาย's cushion (and her folded shawl when she isn't here)
  svg('path', { d: 'M180,1410 L960,1410 L1010,1480 L130,1480 Z', fill: '#e2c47a', stroke: INK, 'stroke-width': 5 }, M.s);
  for (const [v, c] of [[0.25, '#c94f45'], [0.75, '#4f9e5e']]) svg('path', { d: `M${180 - 50 * v},${1410 + 70 * v} L${960 + 50 * v},${1410 + 70 * v}`, stroke: c, 'stroke-width': 6 }, M.s);
  const cushion = svg('g', {}, M.s);
  svg('rect', { x: 475, y: 1400, width: 170, height: 40, rx: 16, fill: '#b49ad8', stroke: INK, 'stroke-width': 4 }, cushion);
  svg('rect', { x: 487, y: 1404, width: 146, height: 10, rx: 5, fill: '#d6c6ee' }, cushion);
  const shawl = svg('g', { opacity: o.yai ? 0 : 1 }, M.s);
  svg('path', { d: 'M499,1402 Q565,1380 625,1400 L621,1412 Q565,1396 503,1414 Z', fill: '#f2e4f6', stroke: INK, 'stroke-width': 3 }, shawl);
  for (let k = 0; k < 4; k++) svg('circle', { cx: 525 + k * 26, cy: 1402 - Math.sin(k) * 4, r: 3.5, fill: '#b49ad8' }, shawl);
  const props = svg('g', {}, M.s);
  for (const [lx, a] of [[150, -8], [190, 6], [230, -4]]) svg('path', { d: `M${lx - 70},1440 Q${lx},1400 ${lx + 70},1440 Q${lx},1460 ${lx - 70},1440 Z`, fill: '#4f9a4a', stroke: INK, 'stroke-width': 3.5, transform: `rotate(${a} ${lx} 1440)` }, props);
  svg('ellipse', { cx: 780, cy: 1440, rx: 46, ry: 14, fill: '#e8dcc4', stroke: INK, 'stroke-width': 3.5 }, props);
  for (const [fx, c] of [[762, '#f5a524'], [780, '#f07aa8'], [798, '#f5a524']]) svg('circle', { cx: fx, cy: 1428, r: 9, fill: c, stroke: INK, 'stroke-width': 2 }, props);
  svg('path', { d: 'M840,1466 l40,-14 M846,1474 l36,-6', stroke: '#9aa3b2', 'stroke-width': 4 }, props);
  const people = svg('g', {}, M.s);
  const made = svg('g', {}, M.s);   // finished krathongs appear here
  const top = svg('g', {}, M.s);
  vignette(M.s, M.defs, 0.5);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 260], ['#ffd59a', '#fff1c4'], 115, { rMin: 50, rMax: 110, op: 0.35 });
  return {
    people, made, top, shadowL, photoGlow, cushion, shawl, light: { ux: 0.15, uy: -0.99, lx: bulbX },
    update(t) {
      bulb.setAttribute('opacity', (0.94 + 0.06 * Math.sin(t * 9) * Math.sin(t * 2.3)).toFixed(3));
      moths(t);
      flies.forEach(f => setA(f.el, { cx: (f.x + 18 * Math.sin(t * 0.7 + f.ph)).toFixed(1), cy: (f.y + 12 * Math.sin(t * 0.9 + f.ph)).toFixed(1), opacity: (0.3 + 0.7 * Math.max(0, Math.sin(t * 2 + f.ph))).toFixed(2) }));
      if (bok) bok(t);
    },
  };
}
