// Room props in the story2/47-ครั้ง language (flat fills, INK outlines, small highlights), shared by stories 8-10 so every
// room can be dressed richly without repeating one template: a night window with moon and city, fairy lights, potted
// plants, shelves of books and knick-knacks, posters, a cork board, a wall clock, a sleeping cat, a fan, a lucky cat.

// window at night: frame, moon, stars, city blocks with lit windows; returns the stars so they can twinkle
function winNight(F, x, y, w, h, frame, seed) {
  svg('rect', { x, y, width: w, height: h, rx: 10, fill: frame, stroke: INK, 'stroke-width': 6 }, F.s);
  svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h - 32, fill: lin(F.defs, [[0, '#141b3c'], [1, '#2c2f63']]) }, F.s);
  const r = rng(seed), stars = [];
  for (let i = 0; i < 26; i++) stars.push(svg('circle', { cx: x + 24 + r() * (w - 48), cy: y + 24 + r() * (h * 0.55), r: 1.2 + r() * 1.8, fill: '#fff' }, F.s));
  svg('circle', { cx: x + w * 0.72, cy: y + h * 0.25, r: 70, fill: rad2(F.defs, [[0, '#fff6dc', 0.45], [1, '#fff6dc', 0]]) }, F.s);
  svg('circle', { cx: x + w * 0.72, cy: y + h * 0.25, r: 30, fill: '#f6eed8' }, F.s);
  let bx = x + 16;
  while (bx < x + w - 16) {
    const bw = Math.min(30 + r() * 46, x + w - 16 - bx), bh = 80 + r() * 160;
    svg('rect', { x: bx, y: y + h - 16 - bh, width: bw, height: bh, fill: r() > 0.5 ? '#1d2348' : '#252b55' }, F.s);
    for (let wy = y + h - 6 - bh; wy < y + h - 26; wy += 22) for (let wx = bx + 5; wx < bx + bw - 7; wx += 13) if (r() > 0.6) svg('rect', { x: wx, y: wy, width: 5, height: 8, fill: '#f6c86a', opacity: 0.85 }, F.s);
    bx += bw + 3;
  }
  svg('rect', { x: x + w / 2 - 4, y: y + 16, width: 8, height: h - 32, fill: frame }, F.s);
  svg('rect', { x: x - 14, y: y + h - 6, width: w + 28, height: 18, rx: 6, fill: shade(frame, -10), stroke: INK, 'stroke-width': 4 }, F.s);   // sill
  return stars;
}
// string of bulbs; returns the bulb groups so they can flicker
function lightString(parent, x0, x1, y, sag, colors, n) {
  svg('path', { d: `M${x0},${y} Q${(x0 + x1) / 2},${y + sag * 2} ${x1},${y}`, fill: 'none', stroke: '#3a2e40', 'stroke-width': 3 }, parent);
  return Array.from({ length: n }, (_, k) => {
    const u = (k + 0.5) / n, bx = x0 + (x1 - x0) * u, by = y + sag * 4 * u * (1 - u);
    const g = svg('g', {}, parent);
    svg('circle', { cx: bx, cy: by + 12, r: 19, fill: colors[k % colors.length], opacity: 0.25 }, g);
    svg('circle', { cx: bx, cy: by + 12, r: 7, fill: colors[k % colors.length] }, g);
    return g;
  });
}
// potted plant standing on the floor at (x, yFloor). kind: 'monstera' | 'snake' | 'palm'
function pottedPlant(g, x, yFloor, s = 1, kind = 'monstera', pot = '#e8e2d6') {
  const p = svg('g', { transform: `translate(${x},${yFloor}) scale(${s})` }, g);

  if (kind === 'monstera') {
    for (const [a, l, c] of [[-148, 200, '#3f8a52'], [-118, 240, '#4f9e5e'], [-64, 230, '#459455'], [-34, 190, '#3a8050'], [-92, 260, '#5aae68']]) {
      const ex = Math.cos(rad(a)) * l, ey = -110 + Math.sin(rad(a)) * l;
      svg('path', { d: `M0,-100 Q${ex * 0.4},${-110 + (ey + 110) * 0.6} ${ex},${ey}`, fill: 'none', stroke: '#2f6b3a', 'stroke-width': 5 }, p);
      const lg = svg('g', { transform: `translate(${ex.toFixed(1)},${ey.toFixed(1)}) rotate(${a + 90})` }, p);
      svg('path', { d: 'M0,10 C-62,0 -66,-80 0,-96 C66,-80 62,0 0,10 Z', fill: c, stroke: INK, 'stroke-width': 4 }, lg);
      for (const sy of [-30, -56]) for (const sx of [-1, 1]) svg('path', { d: `M${sx * 58},${sy} L${sx * 26},${sy + 6}`, stroke: shade(c, -30), 'stroke-width': 7, 'stroke-linecap': 'round' }, lg);
      svg('path', { d: 'M0,4 L0,-86', stroke: shade(c, -25), 'stroke-width': 3 }, lg);
    }
  } else if (kind === 'snake') {
    for (const [dx, h, a, c] of [[-26, 230, -10, '#4a8a4e'], [0, 290, -2, '#5aa05c'], [24, 250, 8, '#3f7c46'], [-8, 180, -18, '#6ab06a'], [14, 200, 16, '#4f9452']]) {
      const lg = svg('g', { transform: `translate(${dx},-90) rotate(${a})` }, p);
      svg('path', { d: `M-14,0 C-18,${-h * 0.5} -8,${-h * 0.9} 0,${-h} C8,${-h * 0.9} 18,${-h * 0.5} 14,0 Z`, fill: c, stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, lg);
      svg('path', { d: `M-8,${-h * 0.3} L8,${-h * 0.34} M-8,${-h * 0.55} L8,${-h * 0.59}`, stroke: '#d9e6a0', 'stroke-width': 3, opacity: 0.7 }, lg);
    }
  } else {
    for (const a of [-160, -130, -100, -70, -40, -20]) {
      const ex = Math.cos(rad(a)) * 200, ey = -100 + Math.sin(rad(a)) * 170;
      svg('path', { d: `M0,-96 Q${ex * 0.5},${ey - 60} ${ex},${ey}`, fill: 'none', stroke: '#3f8a52', 'stroke-width': 18, 'stroke-linecap': 'round' }, p);
      svg('path', { d: `M0,-96 Q${ex * 0.5},${ey - 60} ${ex},${ey}`, fill: 'none', stroke: '#5aae68', 'stroke-width': 8, 'stroke-linecap': 'round', 'stroke-dasharray': '4 10' }, p);
    }
  }
  svg('path', { d: 'M-62,-104 L62,-104 L48,0 L-48,0 Z', fill: pot, stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, p);
  svg('rect', { x: -70, y: -116, width: 140, height: 22, rx: 8, fill: shade(pot, 6), stroke: INK, 'stroke-width': 5 }, p);
  svg('path', { d: 'M-44,-70 L44,-70', stroke: shade(pot, -18), 'stroke-width': 6 }, p);
  return p;
}
// a row of book spines standing on yBase from x; returns the right edge
function bookRow(g, x, yBase, n, seed, maxH = 90, cols = ['#e0574b', '#f2c14e', '#4a7bd8', '#7fc6a8', '#f6efe2', '#b07ad8', '#e8935a']) {
  const r = rng(seed);
  for (let i = 0; i < n; i++) {
    const w = 18 + r() * 12, h = maxH * (0.7 + r() * 0.3), c = cols[Math.floor(r() * cols.length)];
    const lean = i === n - 1 && r() > 0.4 ? 10 : 0;
    const b = svg('g', { transform: lean ? `rotate(${lean} ${x + w} ${yBase})` : '' }, g);
    svg('rect', { x, y: yBase - h, width: w, height: h, rx: 3, fill: c, stroke: INK, 'stroke-width': 3 }, b);
    svg('rect', { x: x + 4, y: yBase - h + 12, width: w - 8, height: 5, fill: shade(c, -25) }, b);
    x += w + 1;
  }
  return x;
}
// wooden wall shelf with brackets
function wallShelf(g, x, y, w, c = '#c99560') {
  svg('rect', { x, y, width: w, height: 16, rx: 5, fill: c, stroke: INK, 'stroke-width': 4 }, g);
  for (const bx of [x + 24, x + w - 36]) svg('path', { d: `M${bx},${y + 16} l12,0 l0,26 Z`, fill: shade(c, -20), stroke: INK, 'stroke-width': 3 }, g);
}
// small things for shelves (bottom at y)
function tinyCactus(g, x, y, c = '#e8935a') {
  svg('path', { d: `M${x - 8},${y - 36} C${x - 10},${y - 70} ${x + 10},${y - 70} ${x + 8},${y - 36} Z`, fill: '#5aae68', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: `M${x - 8},${y - 52} q-14,0 -12,-14 M${x + 8},${y - 46} q12,0 12,-12`, fill: 'none', stroke: '#5aae68', 'stroke-width': 8, 'stroke-linecap': 'round' }, g);
  svg('path', { d: `M${x - 20},${y - 38} L${x + 20},${y - 38} L${x + 15},${y} L${x - 15},${y} Z`, fill: c, stroke: INK, 'stroke-width': 3.5 }, g);
}
function teddy(g, x, y, s = 1, c = '#d9a06a') {
  const t = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('ellipse', { cx: 0, cy: -24, rx: 26, ry: 24, fill: c, stroke: INK, 'stroke-width': 3.5 }, t);
  for (const sx of [-1, 1]) { svg('circle', { cx: sx * 22, cy: -78, r: 10, fill: c, stroke: INK, 'stroke-width': 3.5 }, t); svg('ellipse', { cx: sx * 16, cy: -4, rx: 10, ry: 7, fill: shade(c, 10), stroke: INK, 'stroke-width': 3 }, t); }
  svg('circle', { cx: 0, cy: -62, r: 24, fill: c, stroke: INK, 'stroke-width': 3.5 }, t);
  svg('ellipse', { cx: 0, cy: -55, rx: 10, ry: 7, fill: shade(c, 25) }, t);
  for (const sx of [-1, 1]) svg('circle', { cx: sx * 9, cy: -67, r: 2.8, fill: INK }, t);
  svg('circle', { cx: 0, cy: -58, r: 3, fill: INK }, t);
  svg('path', { d: 'M-10,-36 L10,-36 L0,-28 Z', fill: '#e0574b', stroke: INK, 'stroke-width': 2 }, t);
}
function photoFrame(g, x, y, w, h, bg = '#bfe0f0', c = '#f6efe2') {
  svg('rect', { x, y: y - h, width: w, height: h, rx: 4, fill: c, stroke: INK, 'stroke-width': 3.5 }, g);
  svg('rect', { x: x + 7, y: y - h + 7, width: w - 14, height: h - 14, fill: bg }, g);
  svg('path', { d: heartPathT(x + w / 2, y - h / 2 + 2, Math.min(w, h) * 0.16), fill: '#f04f7f', opacity: 0.85 }, g);
}
// framed posters: 'cat' | 'planet' | 'mountain' | 'heart' | 'game' | 'flower' | 'music'
function poster(g, x, y, w, h, kind, bg) {
  const P = svg('g', {}, g);
  svg('rect', { x, y, width: w, height: h, rx: 6, fill: bg || '#f6efe2', stroke: INK, 'stroke-width': 5 }, P);
  const cx = x + w / 2, cy = y + h / 2;
  if (kind === 'planet') {
    svg('circle', { cx, cy, r: w * 0.28, fill: '#e0574b' }, P);
    svg('ellipse', { cx, cy, rx: w * 0.46, ry: w * 0.09, fill: 'none', stroke: '#1f2a48', 'stroke-width': 7, transform: `rotate(-18 ${cx} ${cy})` }, P);
  } else if (kind === 'mountain') {
    svg('path', { d: `M${x + 14},${y + h - 14} L${x + w * 0.38},${y + h * 0.42} L${x + w * 0.56},${y + h * 0.62} L${x + w * 0.78},${y + h * 0.3} L${x + w - 14},${y + h - 14} Z`, fill: '#2f6a74' }, P);
    svg('circle', { cx: x + w * 0.28, cy: y + h * 0.3, r: w * 0.08, fill: '#ffd66b' }, P);
  } else if (kind === 'heart') {
    svg('path', { d: heartPathT(cx, cy, w * 0.22), fill: '#f07aa8' }, P);
  } else if (kind === 'game') {
    svg('path', { d: `M${cx - w * 0.3},${cy - h * 0.1} h${w * 0.6} a${w * 0.13},${w * 0.13} 0 0 1 0,${w * 0.26} l${-w * 0.09},${w * 0.07} h${-w * 0.42} l${-w * 0.09},${-w * 0.07} a${w * 0.13},${w * 0.13} 0 0 1 0,${-w * 0.26} Z`, fill: '#7a8ad8', stroke: INK, 'stroke-width': 3 }, P);
    svg('path', { d: `M${cx - w * 0.26},${cy + h * 0.02} h${w * 0.1} M${cx - w * 0.21},${cy - h * 0.04} v${h * 0.12}`, stroke: '#fff', 'stroke-width': 4 }, P);
    for (const [dx, dy, c] of [[0.2, -0.02, '#f2c14e'], [0.27, 0.05, '#e0574b']]) svg('circle', { cx: cx + w * dx, cy: cy + h * dy, r: w * 0.035, fill: c }, P);
  } else if (kind === 'flower') {
    for (let k = 0; k < 6; k++) svg('ellipse', { cx: cx + Math.cos(k * 1.047) * w * 0.14, cy: cy - h * 0.06 + Math.sin(k * 1.047) * w * 0.14, rx: w * 0.1, ry: w * 0.1, fill: '#f6a6bc' }, P);
    svg('circle', { cx, cy: cy - h * 0.06, r: w * 0.08, fill: '#f2c14e' }, P);
    svg('path', { d: `M${cx},${cy + h * 0.06} L${cx},${y + h - 16}`, stroke: '#4f9e5e', 'stroke-width': 5 }, P);
  } else if (kind === 'music') {
    svg('circle', { cx, cy, r: w * 0.3, fill: '#23242f' }, P); svg('circle', { cx, cy, r: w * 0.09, fill: '#e0574b' }, P);
    svg('circle', { cx, cy, r: w * 0.2, fill: 'none', stroke: '#3a3b48', 'stroke-width': 3 }, P);
  } else if (kind === 'cat') {
    svg('rect', { x: x + 16, y: y + 16, width: w - 32, height: h * 0.68, fill: '#f2c97a' }, P);
    const s = w / 210, ox = cx - 225 * s, oy = y + 16 - 348 * s;
    svg('path', { d: 'M175,500 C170,440 190,420 225,420 C260,420 280,440 275,500 Z M185,430 L195,395 L212,422 Z M238,422 L255,395 L265,430 Z', fill: '#f6efe2', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round', transform: `translate(${ox},${oy}) scale(${s})` }, P);
    for (const ex of [205, 245]) svg('circle', { cx: ox + ex * s, cy: oy + 455 * s, r: 5 * s, fill: INK }, P);
  }
  return P;
}
// cork board with pinned photos and notes
function corkBoard(g, x, y, w, h, seed) {
  svg('rect', { x, y, width: w, height: h, rx: 8, fill: '#c48a52', stroke: INK, 'stroke-width': 5 }, g);
  svg('rect', { x: x + 12, y: y + 12, width: w - 24, height: h - 24, fill: '#dcae74' }, g);
  const r = rng(seed);
  for (let i = 0; i < 40; i++) svg('circle', { cx: x + 16 + r() * (w - 32), cy: y + 16 + r() * (h - 32), r: 1.6, fill: '#b98a54' }, g);
  const items = [['photo', 0.06, 0.1, -6, '#f6c6d4'], ['note', 0.4, 0.14, 5, '#ffe68a'], ['photo', 0.66, 0.08, 4, '#bfe0f0'], ['note', 0.1, 0.56, 3, '#b8e6c4'], ['photo', 0.38, 0.5, -4, '#ffe2a8'], ['ticket', 0.68, 0.6, -8, '#f6a6bc']];
  for (const [k, u, v, a, c] of items) {
    const ix = x + u * w, iy = y + v * h, iw = k === 'ticket' ? w * 0.26 : w * 0.24, ih = k === 'ticket' ? h * 0.18 : h * 0.34;
    const it = svg('g', { transform: `rotate(${a} ${ix + iw / 2} ${iy})` }, g);
    if (k === 'photo') { svg('rect', { x: ix, y: iy, width: iw, height: ih, rx: 2, fill: '#fbf7ef', stroke: INK, 'stroke-width': 3 }, it); svg('rect', { x: ix + 6, y: iy + 6, width: iw - 12, height: ih - 22, fill: c }, it); svg('path', { d: heartPathT(ix + iw / 2, iy + ih * 0.38, iw * 0.14), fill: '#f04f7f', opacity: 0.8 }, it); }
    else if (k === 'note') { svg('rect', { x: ix, y: iy, width: iw, height: iw, fill: c, stroke: INK, 'stroke-width': 3 }, it); for (let l = 0; l < 3; l++) svg('rect', { x: ix + 8, y: iy + 14 + l * 14, width: iw - 18 - l * 8, height: 4, rx: 2, fill: '#6a5a4a', opacity: 0.5 }, it); }
    else { svg('rect', { x: ix, y: iy, width: iw, height: ih, rx: 4, fill: c, stroke: INK, 'stroke-width': 3 }, it); svg('path', { d: `M${ix + iw * 0.7},${iy + 4} L${ix + iw * 0.7},${iy + ih - 4}`, stroke: INK, 'stroke-width': 2, 'stroke-dasharray': '4 4' }, it); }
    svg('circle', { cx: ix + iw / 2, cy: iy + 4, r: 5, fill: '#e0453b', stroke: INK, 'stroke-width': 2 }, it);
  }
}
// wall clock; returns a function that sets the time (hours as a float)
function wallClock(g, x, y, r = 46, rim = '#e0574b') {
  svg('circle', { cx: x, cy: y, r: r + 6, fill: rim, stroke: INK, 'stroke-width': 5 }, g);
  svg('circle', { cx: x, cy: y, r, fill: '#fbf7ef' }, g);
  for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; svg('circle', { cx: x + Math.cos(a) * r * 0.8, cy: y + Math.sin(a) * r * 0.8, r: k % 3 ? 2 : 3.5, fill: INK }, g); }
  const hh = svg('path', { stroke: INK, 'stroke-width': 6, 'stroke-linecap': 'round' }, g);
  const mm = svg('path', { stroke: INK, 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
  svg('circle', { cx: x, cy: y, r: 5, fill: INK }, g);
  return h => {
    const ah = (h % 12) / 12 * 2 * Math.PI - Math.PI / 2, am = (h % 1) * 2 * Math.PI - Math.PI / 2;
    hh.setAttribute('d', `M${x},${y} L${(x + Math.cos(ah) * r * 0.5).toFixed(1)},${(y + Math.sin(ah) * r * 0.5).toFixed(1)}`);
    mm.setAttribute('d', `M${x},${y} L${(x + Math.cos(am) * r * 0.75).toFixed(1)},${(y + Math.sin(am) * r * 0.75).toFixed(1)}`);
  };
}
// curled-up sleeping cat (ground at y); returns update(t) for the breathing and the tail tip
function sleepyCat(g, x, y, s = 1, c = '#e8a050', o = {}) {
  const k = svg('g', { transform: `translate(${x},${y}) scale(${(o.f || 1) * s},${s})` }, g);
  svg('ellipse', { cx: 0, cy: 4, rx: 96, ry: 12, fill: '#000', opacity: 0.18 }, k);
  const body = svg('g', {}, k);
  svg('path', { d: 'M-86,0 C-96,-66 -20,-96 30,-80 C78,-66 96,-30 86,0 Z', fill: c, stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, body);
  for (const sx of [-40, -10, 20]) svg('path', { d: `M${sx},-84 q10,14 4,30`, fill: 'none', stroke: shade(c, -22), 'stroke-width': 6, 'stroke-linecap': 'round' }, body);
  const tailO = svg('path', { fill: 'none', stroke: INK, 'stroke-width': 26, 'stroke-linecap': 'round' }, k);
  const tail = svg('path', { fill: 'none', stroke: c, 'stroke-width': 17, 'stroke-linecap': 'round' }, k);
  const head = svg('g', { transform: 'translate(-58,-20)' }, k);
  for (const sx of [-1, 1]) svg('path', { d: `M${sx * 14 - 12},-24 L${sx * 24 - 8},-50 L${sx * 30 + 2},-20 Z`, fill: c, stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, head);
  svg('ellipse', { cx: -6, cy: -4, rx: 40, ry: 32, fill: c, stroke: INK, 'stroke-width': 4.5 }, head);
  svg('ellipse', { cx: -10, cy: 10, rx: 20, ry: 13, fill: '#fbefdc' }, head);
  for (const sx of [-24, 8]) svg('path', { d: `M${sx - 8},-6 q8,7 16,0`, fill: 'none', stroke: INK, 'stroke-width': 3.5, 'stroke-linecap': 'round' }, head);
  svg('path', { d: 'M-12,6 l6,0 l-3,4 Z', fill: '#e07a7a' }, head);
  svg('path', { d: 'M-36,-2 q-6,8 -2,14', fill: 'none', stroke: '#f6a6bc', 'stroke-width': 5, opacity: 0.5 }, head);
  const zz = svg('text', { x: -40, y: -70, 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 30, fill: '#fff6dc', stroke: INK, 'stroke-width': 2, opacity: 0, transform: `scale(${o.f || 1},1)` }, k); zz.textContent = 'Z';
  return t => {
    const br = 1 + 0.03 * Math.sin(t * 2.4);
    body.setAttribute('transform', `translate(0,0) scale(1,${br.toFixed(3)})`);
    head.setAttribute('transform', `translate(-58,${(-20 - 2 * Math.sin(t * 2.4)).toFixed(1)})`);
    const w = Math.sin(t * 1.3) * 10;
    const td = `M80,-8 C120,-6 110,30 60,26 C30,24 ${(-10 + w).toFixed(1)},28 ${(-30 + w).toFixed(1)},18`; tail.setAttribute('d', td); tailO.setAttribute('d', td);
    const zk = (t * 0.5) % 1; setA(zz, { x: ((o.f || 1) * (-90 - zk * 30)).toFixed(1), y: (-90 - zk * 50).toFixed(1), opacity: (Math.sin(Math.PI * zk) * 0.8).toFixed(2), 'font-size': (22 + zk * 14).toFixed(1) });
  };
}
// wall fan with spinning blades; returns update(t)
function wallFan(g, x, y, s = 1, c = '#7fc6d8') {
  const f = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('rect', { x: -14, y: -96, width: 28, height: 40, rx: 8, fill: '#e8e2d6', stroke: INK, 'stroke-width': 4 }, f);
  const bl = svg('g', {}, f);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 0, cy: -30, rx: 16, ry: 30, fill: c, opacity: 0.85, transform: `rotate(${k * 120})` }, bl);
  svg('circle', { r: 58, fill: 'none', stroke: INK, 'stroke-width': 5 }, f);
  for (let k = 0; k < 8; k++) svg('path', { d: `M0,0 L${(Math.cos(k * 0.785) * 58).toFixed(1)},${(Math.sin(k * 0.785) * 58).toFixed(1)}`, stroke: INK, 'stroke-width': 1.6, opacity: 0.5 }, f);
  svg('circle', { r: 14, fill: '#e8e2d6', stroke: INK, 'stroke-width': 4 }, f);
  return t => bl.setAttribute('transform', `rotate(${((t * 900) % 360).toFixed(1)})`);
}
// lucky cat with a waving paw (bottom at y); returns update(t)
function luckyCat(g, x, y, s = 1) {
  const k = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, g);
  svg('rect', { x: -34, y: -60, width: 68, height: 60, rx: 22, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3.5 }, k);
  svg('ellipse', { cx: 0, cy: -30, rx: 16, ry: 18, fill: '#f2c14e', stroke: INK, 'stroke-width': 2.5 }, k);
  const paw = svg('g', {}, k);
  svg('rect', { x: 18, y: -104, width: 20, height: 46, rx: 10, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3.5 }, paw);
  for (const sx of [-1, 1]) svg('path', { d: `M${sx * 12 - 8},-112 L${sx * 22 - 4},-134 L${sx * 26 + 2},-108 Z`, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3 }, k);
  svg('circle', { cx: 0, cy: -92, r: 30, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3.5 }, k);
  for (const sx of [-1, 1]) svg('path', { d: `M${sx * 12 - 6},-96 q6,-6 12,0`, fill: 'none', stroke: INK, 'stroke-width': 3, 'stroke-linecap': 'round' }, k);
  svg('path', { d: 'M-6,-82 q6,6 12,0', fill: 'none', stroke: INK, 'stroke-width': 2.5 }, k);
  svg('rect', { x: -22, y: -66, width: 44, height: 8, rx: 4, fill: '#e0453b' }, k);
  return t => paw.setAttribute('transform', `rotate(${(-12 + 22 * Math.sin(t * 5)).toFixed(1)} 28 -62)`);
}
// pair of slippers on the floor seen from the front-top (centre x, floor y)
function slippers(g, x, y, c = '#f6a6bc', s = 1) {
  for (const dx of [-26, 26]) {
    const sl = svg('g', { transform: `translate(${x + dx * s},${y}) rotate(${dx > 0 ? 8 : -6}) scale(${s})` }, g);
    svg('ellipse', { cx: 0, cy: 0, rx: 22, ry: 11, fill: shade(c, -10), stroke: INK, 'stroke-width': 3.5 }, sl);
    svg('path', { d: 'M-18,-2 Q0,-16 18,-2', fill: c, stroke: INK, 'stroke-width': 3.5 }, sl);
  }
}
// mug (bottom centre x,y)
function mugProp(g, x, y, c = '#e0574b', steam = false) {
  svg('path', { d: `M${x + 14},${y - 26} q16,0 14,12 q-2,10 -14,8`, fill: 'none', stroke: INK, 'stroke-width': 4 }, g);
  svg('rect', { x: x - 18, y: y - 36, width: 34, height: 36, rx: 6, fill: c, stroke: INK, 'stroke-width': 4 }, g);
  svg('rect', { x: x - 14, y: y - 30, width: 8, height: 18, rx: 4, fill: '#fff', opacity: 0.35 }, g);
}
// triangle bunting across the wall; colors cycle
function bunting(g, x0, x1, y, sag, n, cols = ['#e0453b', '#f2c14e', '#4f9e5e', '#4a7bd8']) {
  svg('path', { d: `M${x0},${y} Q${(x0 + x1) / 2},${y + sag * 2} ${x1},${y}`, fill: 'none', stroke: '#3a2a24', 'stroke-width': 3 }, g);
  for (let k = 0; k < n; k++) {
    const u = (k + 0.5) / n, bx = x0 + (x1 - x0) * u, by = y + sag * 4 * u * (1 - u);
    svg('path', { d: `M${bx - 18},${by} L${bx + 18},${by} L${bx},${by + 36} Z`, fill: cols[k % cols.length], stroke: INK, 'stroke-width': 2.5 }, g);
  }
}
