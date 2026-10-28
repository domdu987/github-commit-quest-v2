// "312 ชามที่ไม่มีผักชี" sets, in the story2 language: ปั้น's living room at night (the two of them on the sofa), มิน's
// bedroom at night, and their usual noodle shop — warm bulbs, a steaming pot, a stainless table with two bowls.

// a small coriander leaf (three rounded lobes) centred on 0,0
function corianderLeaf(parent, s = 1, c = '#4fae5a') {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M0,4 C-9,6 -13,-4 -6,-7 C-6,-13 4,-14 5,-7 C12,-6 11,5 0,4 Z', fill: c, stroke: '#2f6b3a', 'stroke-width': 1.6, transform: `scale(${s})` }, g);
  svg('path', { d: 'M0,4 L0,-6 M0,0 L-5,-4 M0,0 L5,-3', stroke: '#2f6b3a', 'stroke-width': 1.2, fill: 'none', transform: `scale(${s})` }, g);
  return g;
}

// noodle bowl (front view) with optional coriander leaves on top; returns the leaf elements
function noodleBowl(parent, x, y, nLeaves, seed, scale = 1) {
  const g = svg('g', { transform: `translate(${x},${y}) scale(${scale})` }, parent);
  svg('ellipse', { cx: 0, cy: 52, rx: 52, ry: 7, fill: '#000', opacity: 0.18 }, g);
  svg('path', { d: 'M-72,0 Q-66,52 -26,56 L26,56 Q66,52 72,0 Z', fill: '#fbf8f1', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M-68,14 Q0,26 68,14', fill: 'none', stroke: '#4a7bd8', 'stroke-width': 5 }, g);
  svg('path', { d: 'M-62,26 Q0,38 62,26', fill: 'none', stroke: '#4a7bd8', 'stroke-width': 2.5, opacity: 0.8 }, g);
  svg('rect', { x: -28, y: 54, width: 56, height: 8, rx: 3, fill: '#efe9dc', stroke: INK, 'stroke-width': 3.5 }, g);
  svg('ellipse', { cx: 0, cy: 0, rx: 72, ry: 17, fill: '#fbf8f1', stroke: INK, 'stroke-width': 4.5 }, g);
  svg('ellipse', { cx: 0, cy: 1, rx: 62, ry: 12, fill: '#d9a35e' }, g);
  for (const [dx, w] of [[-30, 26], [-4, 30], [22, 24]]) svg('path', { d: `M${dx - w / 2},2 q${w / 4},-6 ${w / 2},0 t${w / 2},0`, fill: 'none', stroke: '#f6ead0', 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
  for (const [mx, my] of [[-38, -2], [34, 1]]) svg('circle', { cx: mx, cy: my, r: 7, fill: '#9a6a48', stroke: INK, 'stroke-width': 2.5 }, g);
  const r = rng(seed), leaves = [], pos = [];
  for (let i = 0; i < nLeaves; i++) {
    const lg = corianderLeaf(g, 0.9 + r() * 0.3);
    const lx = -48 + 96 * ((i + 0.5) / nLeaves) + (r() - 0.5) * 10, ly = -6 + r() * 9;
    lg.setAttribute('transform', `translate(${lx.toFixed(1)},${ly.toFixed(1)}) rotate(${(r() * 360).toFixed(0)})`);
    leaves.push(lg); pos.push([x + lx * scale, y + ly * scale]);
  }
  return { g, leaves, pos };
}

// ---------------- ปั้น's living room at night: olive walls, terracotta sofa, his cat asleep on the rug ----------------
function loungeNight(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#56603c'], [1, '#727a4a']]) }, F.s);
  for (let i = 0; i < 18; i++) svg('rect', { x: -300 + i * 96, y: -300, width: 3, height: 2600, fill: '#2f3420', opacity: 0.18 }, F.s);   // board-and-batten
  const stars = winNight(F, 640, 210, 360, 470, '#e8dcc4', 81);
  curtains2(F, 580, 990, 186, 560, '#e8a84a', '#c98a32', '#b87a2a');
  svg('rect', { x: 560, y: 176, width: 540, height: 12, rx: 6, fill: '#3a2e24' }, F.s);
  // his wall: cat poster, game print, record, a shelf with a speaker, plants and console boxes, a clock
  poster(F.s, 110, 300, 200, 240, 'cat');
  poster(F.s, 340, 330, 170, 130, 'game', '#2b2f4f');
  poster(F.s, 350, 490, 120, 120, 'music', '#f2c14e');
  const clk = wallClock(F.s, 520, 250, 42, '#e8a84a');
  wallShelf(F.s, 90, 680, 420, '#b07a4a');
  bookRow(F.s, 104, 680, 4, 811, 80, ['#e0574b', '#4a7bd8', '#f2c14e', '#23242f']);
  svg('rect', { x: 210, y: 610, width: 70, height: 70, rx: 10, fill: '#23242f', stroke: INK, 'stroke-width': 3.5 }, F.s);   // speaker
  svg('circle', { cx: 245, cy: 645, r: 20, fill: '#3a3b48', stroke: '#6a6b78', 'stroke-width': 3 }, F.s);
  tinyCactus(F.s, 320, 680, '#e0574b');
  // trailing pothos from the shelf end
  const pg = svg('g', {}, F.s);
  svg('path', { d: 'M420,680 L470,680 L462,640 L428,640 Z', fill: '#e8e2d6', stroke: INK, 'stroke-width': 3.5 }, pg);
  for (const [vx, len] of [[430, 210], [450, 150], [466, 260]]) {
    svg('path', { d: `M${vx},660 Q${vx + 14},${660 + len / 2} ${vx - 4},${660 + len}`, fill: 'none', stroke: '#3f7c46', 'stroke-width': 3 }, pg);
    for (let k = 1; k < len / 34; k++) svg('ellipse', { cx: vx + (k % 2 ? 9 : -5), cy: 660 + k * 34, rx: 11, ry: 8, fill: k % 2 ? '#5aae68' : '#4f9e5e', stroke: INK, 'stroke-width': 2, transform: `rotate(${k % 2 ? 30 : -30} ${vx} ${660 + k * 34})` }, pg);
  }
  woodFloor(M.s, M.defs, 1330, '#8a5c3c', '#5a3a28', '#4a2e20');
  svg('rect', { x: -300, y: 1330, width: 300, height: 1000, fill: '#5a3a28' }, M.s); svg('rect', { x: 1080, y: 1330, width: 300, height: 1000, fill: '#5a3a28' }, M.s);
  svg('rect', { x: -300, y: 1318, width: 1680, height: 16, fill: '#e8dcc4', stroke: INK, 'stroke-width': 3 }, M.s);   // skirting
  rug(M.s, M.defs, 560, 1560, 500, 120, '#9a4434');
  svg('ellipse', { cx: 560, cy: 1560, rx: 430, ry: 96, fill: 'none', stroke: '#f2c14e', 'stroke-width': 8, opacity: 0.6 }, M.s);
  svg('ellipse', { cx: 560, cy: 1560, rx: 360, ry: 76, fill: 'none', stroke: '#e8d8b8', 'stroke-width': 5, opacity: 0.45 }, M.s);
  floorLamp(M.s, M.defs, 90, 1330, '#ffd59a', 0.45);
  pottedPlant(M.s, 1020, 1330, 1.05, 'snake', '#c95a4a');
  wallAO(M.s, M.defs, 1318);
  const shadowL = svg('g', {}, M.s);
  lightPool(M.s, M.defs, 90, 860, 260, 380, '#ffd59a', 0.18);
  contactShadow(M.s, M.defs, 560, 1338, 380, 22, 0.45);
  svg('rect', { x: 190, y: 1040, width: 740, height: 170, rx: 32, fill: '#d47c5c', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 170, y: 1196, width: 780, height: 134, rx: 18, fill: '#c46a4c', stroke: INK, 'stroke-width': 5 }, M.s);
  for (const lx of [200, 900]) svg('rect', { x: lx, y: 1326, width: 20, height: 18, rx: 4, fill: '#3a2620' }, M.s);
  for (const ax of [130, 910]) svg('rect', { x: ax, y: 1110, width: 80, height: 220, rx: 30, fill: '#d47c5c', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 230, y: 1100, width: 120, height: 86, rx: 30, fill: '#f2c14e', stroke: INK, 'stroke-width': 5, transform: 'rotate(-8 290 1143)' }, M.s);
  for (let k = 0; k < 3; k++) svg('path', { d: `M${246 + k * 30},1110 l0,64`, stroke: '#e0a12c', 'stroke-width': 5, transform: 'rotate(-8 290 1143)' }, M.s);
  svg('rect', { x: 790, y: 1096, width: 112, height: 84, rx: 28, fill: '#4f8f7a', stroke: INK, 'stroke-width': 5, transform: 'rotate(10 846 1138)' }, M.s);
  svg('path', { d: 'M930,1110 L1000,1100 L1004,1290 Q970,1300 940,1286 Z', fill: '#e8d8b8', stroke: INK, 'stroke-width': 4 }, M.s);   // throw over the arm
  for (let k = 0; k < 4; k++) svg('path', { d: `M${944 + k * 14},1290 l0,16`, stroke: '#c9b48e', 'stroke-width': 4, 'stroke-linecap': 'round' }, M.s);
  // his cat asleep on the rug, a controller and two mugs on the floor
  const cat = sleepyCat(M.s, 830, 1470, 0.9, '#e8a050', { f: -1 });
  const ctl = svg('g', { transform: 'translate(340,1480) rotate(-14)' }, M.s);
  svg('path', { d: 'M-44,-14 h88 a20,20 0 0 1 0,40 l-14,8 h-60 l-14,-8 a20,20 0 0 1 0,-40 Z', fill: '#2f3448', stroke: INK, 'stroke-width': 3.5 }, ctl);
  for (const [dx, c] of [[24, '#f2c14e'], [34, '#e0574b']]) svg('circle', { cx: dx, cy: 2 + (c === '#e0574b' ? 8 : 0), r: 5, fill: c }, ctl);
  svg('path', { d: 'M-32,6 h16 M-24,-2 v16', stroke: '#9aa3b2', 'stroke-width': 4 }, ctl);
  mugProp(M.s, 560, 1470, '#f6efe2'); mugProp(M.s, 610, 1478, '#f2c14e');
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 220, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  const pglow2 = svg('circle', { cx: 0, cy: 0, r: 220, fill: rad2(M.defs, [[0, '#ffe0ec', 0.4], [1, '#ffe0ec', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.45);
  const leaves = R ? [leafG(R, 1180, 1900, 1.6, -120, '#24473a'), leafG(R, 1150, 1960, 1.4, -150, '#2b5243')] : [];
  return { people, top, pglow, pglow2, shadowL, light: { ux: -0.85, uy: -0.45, lx: 90 }, update(t) { stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.7)).toFixed(2))); clk(21.7 + t / 600); cat(t); swayLeaves(leaves, t); } };
}

// ---------------- มิน's bedroom at night: navy walls, fairy lights, a cork board of their photos, a pink bed ----------------
function herRoom(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: lin(F.defs, [[0, '#24315c'], [1, '#33457a']]) }, F.s);
  for (let gy = -260; gy < 1400; gy += 96) for (let gx = -280 + ((gy / 96) % 2 ? 48 : 0); gx < 1380; gx += 96)
    svg('path', { d: `M${gx},${gy - 7} L${gx + 2},${gy - 2} L${gx + 7},${gy} L${gx + 2},${gy + 2} L${gx},${gy + 7} L${gx - 2},${gy + 2} L${gx - 7},${gy} L${gx - 2},${gy - 2} Z`, fill: '#ffffff', opacity: 0.08 }, F.s);   // star wallpaper
  const stars = winNight(F, 620, 230, 350, 440, '#f2e6d0', 83);
  curtains2(F, 560, 966, 196, 560, '#f6a6bc', '#e08aa0', '#d27c94');
  svg('rect', { x: 540, y: 186, width: 530, height: 12, rx: 6, fill: '#2f2a40' }, F.s);
  const bulbs = lightString(F.s, 20, 1060, 120, 34, ['#ffd66b', '#ff9fc0', '#9fe0ff'], 15);
  corkBoard(F.s, 90, 290, 330, 260, 87);
  wallShelf(F.s, 80, 690, 400, '#e2c49a');
  const bx = bookRow(F.s, 96, 690, 5, 813, 84);
  teddy(F.s, bx + 50, 690, 0.9, '#d9a06a');
  photoFrame(F.s, bx + 100, 690, 70, 86, '#f6c6d4');
  tinyCactus(F.s, 452, 690, '#4a7bd8');
  woodFloor(M.s, M.defs, 1330, '#b07a52', '#8a5a3c', '#7a4c32');
  svg('rect', { x: -300, y: 1330, width: 300, height: 1000, fill: '#8a5a3c' }, M.s); svg('rect', { x: 1080, y: 1330, width: 300, height: 1000, fill: '#8a5a3c' }, M.s);
  svg('rect', { x: -300, y: 1318, width: 1680, height: 16, fill: '#f2e6d0', stroke: INK, 'stroke-width': 3 }, M.s);
  rug(M.s, M.defs, 520, 1580, 470, 110, '#a8445e');
  svg('ellipse', { cx: 520, cy: 1580, rx: 400, ry: 88, fill: 'none', stroke: '#ffd0dc', 'stroke-width': 7, opacity: 0.55, 'stroke-dasharray': '22 14' }, M.s);
  svg('path', { d: 'M620,216 L980,216 L1180,1560 L420,1560 Z', fill: lin(M.defs, [[0, '#c9d6ff', 0.08], [1, '#c9d6ff', 0]]) }, M.s);
  wallAO(M.s, M.defs, 1318);
  const shadowL = svg('g', {}, M.s);
  lampCone(M.s, M.defs, 715, 1030, 300, 520, '#ffe2a8', 0.22);
  contactShadow(M.s, M.defs, 330, 1338, 320, 20, 0.45);
  // bed: cream headboard, wooden base, white sheet, pink polka-dot blanket, pillows
  svg('rect', { x: 0, y: 930, width: 96, height: 400, rx: 40, fill: '#f4ead8', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 18, y: 960, width: 60, height: 120, rx: 26, fill: '#e8dcc4' }, M.s);
  svg('rect', { x: 40, y: 1200, width: 560, height: 120, rx: 14, fill: '#d9a06a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 60, y: 1250, width: 520, height: 8, rx: 4, fill: '#b98a54' }, M.s);
  for (const lx of [58, 560]) svg('rect', { x: lx, y: 1316, width: 22, height: 20, rx: 4, fill: '#8a5a3c', stroke: INK, 'stroke-width': 3 }, M.s);
  svg('rect', { x: 50, y: 1166, width: 540, height: 54, rx: 20, fill: '#fbf6ee', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 70, y: 1108, width: 150, height: 64, rx: 26, fill: '#ffffff', stroke: INK, 'stroke-width': 5, transform: 'rotate(-6 145 1140)' }, M.s);
  const bl = svg('g', {}, M.s);
  svg('path', { d: 'M250,1170 Q400,1120 590,1172 L590,1236 Q420,1252 250,1230 Z', fill: '#f6a6bc', stroke: INK, 'stroke-width': 5 }, bl);
  for (const [dx, dy] of [[300, 1180], [360, 1210], [420, 1162], [480, 1200], [540, 1176], [550, 1222], [330, 1224]]) svg('circle', { cx: dx, cy: dy, r: 7, fill: '#ffffff', opacity: 0.8 }, bl);
  svg('path', { d: heartPathT(150, 1150, 42), fill: '#f07aa8', stroke: INK, 'stroke-width': 5 }, M.s);   // heart pillow
  // nightstand: drawer, lamp, alarm clock, a glass of water
  svg('rect', { x: 640, y: 1170, width: 150, height: 160, rx: 8, fill: '#e2c49a', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 656, y: 1236, width: 118, height: 8, fill: '#c4ab8c' }, M.s);
  svg('circle', { cx: 715, cy: 1280, r: 7, fill: '#8a6a4a', stroke: INK, 'stroke-width': 2.5 }, M.s);
  svg('circle', { cx: 715, cy: 1060, r: 300, fill: rad2(M.defs, [[0, '#ffe2a8', 0.42], [1, '#ffe2a8', 0]]) }, M.s);
  svg('path', { d: 'M690,1170 L740,1170 L732,1090 L698,1090 Z', fill: '#f2c14e', stroke: INK, 'stroke-width': 4 }, M.s);
  svg('path', { d: 'M672,1090 L758,1090 L738,1030 L692,1030 Z', fill: lin(M.defs, [[0, '#fff6dc'], [1, '#ffe2a8']]), stroke: INK, 'stroke-width': 4 }, M.s);
  const ac = svg('g', { transform: 'translate(768,1170)' }, M.s);
  svg('rect', { x: -14, y: -34, width: 30, height: 34, rx: 8, fill: '#9fe0ff', stroke: INK, 'stroke-width': 3 }, ac);
  svg('circle', { cx: 1, cy: -18, r: 9, fill: '#fbf7ef' }, ac);
  // her tall plant and slippers, a tote bag slumped by the bed
  pottedPlant(M.s, 1024, 1330, 1.05, 'monstera', '#f6efe2');
  slippers(M.s, 560, 1420, '#f6a6bc');
  const tb = svg('g', { transform: 'translate(180,1400)' }, M.s);
  svg('path', { d: 'M-50,0 L-44,-80 L44,-80 L50,0 Z', fill: '#efe2c8', stroke: INK, 'stroke-width': 4 }, tb);
  svg('path', { d: 'M-24,-80 Q-24,-120 0,-120 Q24,-120 24,-80', fill: 'none', stroke: INK, 'stroke-width': 4 }, tb);
  svg('path', { d: heartPathT(0, -42, 14), fill: '#f07aa8' }, tb);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 230, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  lightPool(M.s, M.defs, 715, 1350, 300, 60, '#ffe2a8', 0.35);
  vignette(M.s, M.defs, 0.45);
  const leaves = R ? [leafG(R, -120, 1900, 1.6, -60, '#3a6b47'), leafG(R, -80, 1960, 1.4, -25, '#4f8f56')] : [];
  const bok = R ? bokehField(R.s, R.defs, 7, [-100, 0, 1180, 260], ['#ffd66b', '#ff9fc0', '#9fe0ff'], 85, { rMin: 40, rMax: 90, op: 0.55 }) : null;
  return {
    people, top, pglow, shadowL, light: { ux: 0.94, uy: -0.25, lx: 715 },
    update(t) {
      stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.3)).toFixed(2)));
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.2 + i * 1.7)).toFixed(2)));
      swayLeaves(leaves, t); if (bok) bok(t);
    },
  };
}

// ---------------- the noodle shop: orange wall, bunting, red menu board, lucky cat, steaming cart, red plastic stools ----------------
function redStool(g, x, ySeat, c = '#e0453b', w = 110) {
  const h = 1330 - ySeat;
  svg('path', { d: `M${x - w / 2 + 6},${ySeat + 10} L${x - w / 2 - 6},${ySeat + h} L${x - w / 2 + 14},${ySeat + h} L${x - w / 2 + 22},${ySeat + 12} Z M${x + w / 2 - 6},${ySeat + 10} L${x + w / 2 + 6},${ySeat + h} L${x + w / 2 - 14},${ySeat + h} L${x + w / 2 - 22},${ySeat + 12} Z`, fill: shade(c, -12), stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  svg('rect', { x: x - w / 2 + 8, y: ySeat + h * 0.55, width: w - 16, height: 10, rx: 4, fill: shade(c, -12), stroke: INK, 'stroke-width': 3 }, g);
  svg('rect', { x: x - w / 2, y: ySeat, width: w, height: 16, rx: 8, fill: c, stroke: INK, 'stroke-width': 3.5 }, g);
}
function noodleShop(S, o = {}) {
  const F = S.L.far, M = S.L.mid;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1220, fill: lin(F.defs, [[0, '#a8603a'], [1, '#d4955a']]) }, F.s);
  svg('rect', { x: -300, y: 900, width: 1680, height: 1700, fill: '#ecdcb8' }, F.s);
  for (let x = -280; x < 1380; x += 64) svg('rect', { x, y: 900, width: 2, height: 1700, fill: '#cdb98e' }, F.s);
  for (let y = 964; y < 2600; y += 64) svg('rect', { x: -300, y, width: 1680, height: 2, fill: '#cdb98e' }, F.s);
  svg('rect', { x: -300, y: 892, width: 1680, height: 14, fill: '#8a5a3a' }, F.s);
  wallAO(F.s, F.defs, 1330, { op: 0.22 });
  bunting(F.s, -60, 1140, 96, 22, 18);
  // menu board
  svg('rect', { x: 90, y: 300, width: 420, height: 290, rx: 14, fill: '#b8322a', stroke: INK, 'stroke-width': 6 }, F.s);
  svg('rect', { x: 106, y: 316, width: 388, height: 258, rx: 8, fill: 'none', stroke: '#f6d27a', 'stroke-width': 3 }, F.s);
  const tt = (x, y, s, w, txt, c = '#fff6dc', a = 'middle') => { const e = svg('text', { x, y, 'text-anchor': a, 'font-family': 'Kanit', 'font-weight': w, 'font-size': s, fill: c }, F.s); e.textContent = txt; return e; };
  tt(300, 382, 56, 700, 'ก๋วยเตี๋ยว', '#ffe08a');
  [['เส้นเล็กน้ำใส', '50'], ['เย็นตาโฟ', '55'], ['ต้มยำ', '60']].forEach(([n, p], i) => { tt(130, 446 + i * 44, 30, 500, n, '#fff6dc', 'start'); tt(470, 446 + i * 44, 30, 600, p, '#ffe08a', 'end'); });
  // shelf under the menu: stacked blue-rim bowls, a jar of pickled chilli, the lucky cat
  wallShelf(F.s, 90, 690, 430, '#8a5a3a');
  for (const [sx, n] of [[130, 4], [200, 3]]) for (let k = 0; k < n; k++) { svg('path', { d: `M${sx - 30},${690 - 14 - k * 14} Q${sx},${690 + 2 - k * 14} ${sx + 30},${690 - 14 - k * 14} Z`, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3 }, F.s); svg('path', { d: `M${sx - 26},${690 - 10 - k * 14} Q${sx},${690 - k * 14} ${sx + 26},${690 - 10 - k * 14}`, fill: 'none', stroke: '#4a7bd8', 'stroke-width': 2.5 }, F.s); }
  svg('rect', { x: 262, y: 628, width: 52, height: 62, rx: 10, fill: '#f6efe2', opacity: 0.85, stroke: INK, 'stroke-width': 3.5 }, F.s);
  svg('rect', { x: 268, y: 652, width: 40, height: 32, rx: 6, fill: '#d9542a' }, F.s);
  svg('rect', { x: 258, y: 618, width: 60, height: 14, rx: 5, fill: '#e0453b', stroke: INK, 'stroke-width': 3 }, F.s);
  const lucky = luckyCat(F.s, 440, 690, 0.95);
  // clock + calendar
  const clk = wallClock(F.s, 640, 330, 46, '#fbf7ef');
  svg('rect', { x: 588, y: 420, width: 108, height: 150, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('rect', { x: 588, y: 420, width: 108, height: 30, rx: 6, fill: '#e0453b', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('rect', { x: 600, y: 458, width: 84, height: 44, fill: '#7fc6a8' }, F.s);
  for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) svg('rect', { x: 600 + c * 14, y: 512 + r * 16, width: 9, height: 9, fill: '#c4b8a4' }, F.s);
  // kitchen cart on the right: glass case, steaming pot, hanging ladles, cabinet underneath
  svg('rect', { x: 720, y: 520, width: 340, height: 380, rx: 10, fill: '#c9d2dc', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('rect', { x: 736, y: 536, width: 308, height: 150, rx: 6, fill: '#e8f2f8', stroke: INK, 'stroke-width': 3.5 }, F.s);
  for (let i = 0; i < 5; i++) svg('circle', { cx: 770 + i * 30, cy: 650, r: 12, fill: '#a87a56', stroke: INK, 'stroke-width': 2.5 }, F.s);
  for (let i = 0; i < 3; i++) svg('path', { d: `M${920 + i * 34},660 q8,-30 16,0`, fill: 'none', stroke: '#f6ead0', 'stroke-width': 6, 'stroke-linecap': 'round' }, F.s);
  svg('rect', { x: 736, y: 706, width: 308, height: 26, rx: 6, fill: '#e0453b', stroke: INK, 'stroke-width': 3.5 }, F.s);
  const tc = svg('text', { x: 890, y: 727, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 22, fill: '#fff6dc' }, F.s); tc.textContent = 'ก๋วยเตี๋ยวเรือ';
  svg('rect', { x: 720, y: 900, width: 340, height: 420, rx: 8, fill: '#aab3c2', stroke: INK, 'stroke-width': 5 }, F.s);
  for (const dx of [736, 896]) { svg('rect', { x: dx, y: 920, width: 148, height: 360, rx: 6, fill: '#bcc5d2', stroke: INK, 'stroke-width': 3 }, F.s); svg('rect', { x: dx + (dx === 736 ? 124 : 12), y: 1060, width: 10, height: 50, rx: 4, fill: '#6b7280' }, F.s); }
  svg('rect', { x: 760, y: 420, width: 150, height: 110, rx: 10, fill: '#aab3c2', stroke: INK, 'stroke-width': 5 }, F.s);
  svg('rect', { x: 750, y: 408, width: 170, height: 22, rx: 8, fill: '#9aa3b2', stroke: INK, 'stroke-width': 4 }, F.s);
  for (const lx of [960, 1000]) { svg('path', { d: `M${lx},430 L${lx},500`, stroke: '#6b7280', 'stroke-width': 5 }, F.s); svg('ellipse', { cx: lx, cy: 506, rx: 14, ry: 9, fill: '#9aa3b2', stroke: INK, 'stroke-width': 3 }, F.s); }
  const fan = wallFan(F.s, 1000, 300, 0.75);
  const steam = Array.from({ length: 6 }, () => svg('circle', { r: 26, fill: '#fff8ea', opacity: 0 }, F.s));
  // bulbs on cords
  const bulbs = [];
  for (const bx of [260, 540, 820]) {
    svg('path', { d: `M${bx},-300 L${bx},180`, stroke: '#2a1e1a', 'stroke-width': 3 }, F.s);
    const g = svg('g', {}, F.s);
    svg('circle', { cx: bx, cy: 205, r: 120, fill: rad2(F.defs, [[0, '#ffe2a8', 0.55], [1, '#ffe2a8', 0]]) }, g);
    svg('path', { d: `M${bx - 26},180 L${bx + 26},180 L${bx + 16},162 L${bx - 16},162 Z`, fill: '#3a2a24' }, g);
    svg('circle', { cx: bx, cy: 200, r: 20, fill: '#fff1c4' }, g);
    bulbs.push(g);
  }
  // floor: warm terrazzo tiles
  svg('rect', { x: -300, y: 1330, width: 1680, height: 1000, fill: lin(M.defs, [[0, '#b39a7e'], [1, '#7a6250']]) }, M.s);
  for (let y = 1330, k = 0; y < 2300; y += 46 + k * 10, k++) svg('rect', { x: -300, y, width: 1680, height: 3, fill: '#6a5444', opacity: 0.45 }, M.s);
  const rt = rng(815);
  for (let i = 0; i < 90; i++) svg('circle', { cx: -100 + rt() * 1300, cy: 1340 + rt() * 600, r: 2 + rt() * 3, fill: ['#e8dcc4', '#8a6a52', '#c98a6a'][i % 3], opacity: 0.5 }, M.s);
  // drinks fridge on the left, behind them
  const fr = svg('g', {}, M.s);
  svg('rect', { x: -40, y: 760, width: 200, height: 570, rx: 12, fill: '#e0453b', stroke: INK, 'stroke-width': 5 }, fr);
  svg('rect', { x: -24, y: 820, width: 168, height: 440, rx: 8, fill: '#dff0f4', stroke: INK, 'stroke-width': 4 }, fr);
  const tf = svg('text', { x: 60, y: 806, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 34, fill: '#fff6dc' }, fr); tf.textContent = 'เย็นชื่นใจ';
  for (let r = 0; r < 4; r++) {
    svg('rect', { x: -24, y: 920 + r * 100, width: 168, height: 5, fill: '#9aa3b2' }, fr);
    for (let c = 0; c < 5; c++) { const bc = ['#4f9e5e', '#f2a03c', '#e0453b', '#4a7bd8', '#f2c14e'][(r + c) % 5]; svg('rect', { x: -14 + c * 32, y: 920 + r * 100 - 70, width: 22, height: 70, rx: 7, fill: bc, stroke: INK, 'stroke-width': 2 }, fr); svg('rect', { x: -10 + c * 32, y: 920 + r * 100 - 80, width: 14, height: 12, rx: 3, fill: '#fbf8f1', stroke: INK, 'stroke-width': 2 }, fr); }
  }
  svg('rect', { x: 120, y: 1000, width: 10, height: 120, rx: 4, fill: '#9aa3b2', stroke: INK, 'stroke-width': 2 }, fr);
  contactShadow(M.s, M.defs, 540, 1336, 470, 22, 0.4);
  const shadowL = svg('g', {}, M.s);
  // red plastic stools under the two of them and a spare by the cart
  redStool(M.s, (o.minX || 360), 1226, '#e0453b');
  redStool(M.s, (o.panX || 720), 1226, '#e0453b');
  redStool(M.s, 1010, 1240, '#4a7bd8', 100);
  const people = svg('g', {}, M.s);
  // the table and everything on it sits in front of the people: stainless top, open frame, legs to the floor
  const table = svg('g', {}, M.s);
  contactShadow(table, M.defs, 540, 1416, 430, 16, 0.35);
  for (const lx of [214, 852]) svg('rect', { x: lx, y: 1196, width: 14, height: 136, fill: '#8a949f', stroke: INK, 'stroke-width': 3 }, table);   // back legs
  for (const lx of [176, 890]) svg('rect', { x: lx, y: 1196, width: 20, height: 220, rx: 4, fill: '#aab3c2', stroke: INK, 'stroke-width': 4 }, table);   // front legs
  svg('rect', { x: 176, y: 1350, width: 734, height: 10, rx: 4, fill: '#8a949f', stroke: INK, 'stroke-width': 3 }, table);
  svg('rect', { x: 160, y: 1182, width: 760, height: 24, rx: 6, fill: '#8a949f', stroke: INK, 'stroke-width': 4 }, table);
  svg('rect', { x: 130, y: 1148, width: 820, height: 38, rx: 10, fill: lin(M.defs, [[0, '#eef2f6'], [1, '#c3cbd5']]), stroke: INK, 'stroke-width': 5 }, table);
  // condiment caddy (sugar, fish sauce, chilli, vinegar) + chopstick tub
  svg('rect', { x: 150, y: 1092, width: 150, height: 60, rx: 8, fill: '#c9d2dc', stroke: INK, 'stroke-width': 4 }, table);
  [['#fbf8f1', 162], ['#c98a3a', 196], ['#d9542a', 230], ['#f2e2b0', 264]].forEach(([c, jx]) => { svg('rect', { x: jx, y: 1060, width: 28, height: 46, rx: 6, fill: c, stroke: INK, 'stroke-width': 3 }, table); svg('rect', { x: jx + 4, y: 1052, width: 20, height: 10, rx: 3, fill: '#9aa3b2', stroke: INK, 'stroke-width': 2.5 }, table); });
  svg('rect', { x: 892, y: 1066, width: 54, height: 84, rx: 8, fill: '#e0574b', stroke: INK, 'stroke-width': 4 }, table);
  for (let i = 0; i < 5; i++) svg('path', { d: `M${902 + i * 8},1068 L${896 + i * 10},1010`, stroke: '#e8c98f', 'stroke-width': 4, 'stroke-linecap': 'round' }, table);
  const herBowl = noodleBowl(table, o.herX || 420, 1112, 7, 811, 0.85);
  const hisBowl = noodleBowl(table, o.hisX || 660, 1112, 5, 813, 0.85);
  // saucer for the picked-out coriander
  const sx = o.saucerX || 540;
  svg('ellipse', { cx: sx, cy: 1150, rx: 46, ry: 11, fill: '#fbf8f1', stroke: INK, 'stroke-width': 3.5 }, table);
  const saucer = Array.from({ length: 8 }, (_, i) => { const lg = corianderLeaf(table, 0.8); lg.setAttribute('transform', `translate(${(sx - 22 + (i % 4) * 14 + (i > 3 ? 6 : 0)).toFixed(1)},${(1146 - (i > 3 ? 5 : 0)).toFixed(1)}) rotate(${i * 47})`); lg.setAttribute('opacity', 0); return lg; });
  const top = svg('g', {}, M.s);
  const glow = svg('circle', { cx: 540, cy: 1000, r: 420, fill: rad2(M.defs, [[0, '#ffcf8a', 0.22], [1, '#ffcf8a', 0]]) }, M.s);
  vignette(M.s, M.defs, 0.45);
  // near foreground, out of focus: bulb bokeh along the top, the edge of the next table with a chilli jar and cups
  const R = S.L.fore; let bok = null, foreG = null;
  if (R) {
    bok = bokehField(R.s, R.defs, 6, [-200, -160, 1280, 160], ['#ffe2a8', '#ffcf8a', '#fff1c4'], 817, { rMin: 50, rMax: 110, op: 0.45 });
    foreG = svg('g', {}, R.s);
  }
  return {
    people, table, top, herBowl, hisBowl, saucer, shadowL, light: { ux: 0.15, uy: -1, lx: 540 },
    update(t, cam) {
      if (bok) bok(t);
      if (foreG) foreG.setAttribute('opacity', cam && cam.z > 1.6 ? 0 : 1);
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.9 + 0.1 * Math.sin(t * 3 + i * 2)).toFixed(2)));
      steam.forEach((s, i) => { const k = ((t * 0.45 + i / 6) % 1); setA(s, { cx: (835 + Math.sin(k * 6 + i) * 26).toFixed(1), cy: (400 - k * 300).toFixed(1), r: (16 + k * 34).toFixed(1), opacity: (0.32 * Math.sin(Math.PI * k)).toFixed(3) }); });
      glow.setAttribute('opacity', (0.9 + 0.1 * Math.sin(t * 2.3)).toFixed(3));
      lucky(t); fan(t); clk(12.3 + t / 600);
    },
  };
}
