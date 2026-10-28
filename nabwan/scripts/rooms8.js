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
  rug(M.s, M.defs, 560, 1560, 500, 120, '#e8d8b8');
  svg('ellipse', { cx: 560, cy: 1560, rx: 430, ry: 96, fill: 'none', stroke: '#c95a4a', 'stroke-width': 8, opacity: 0.7 }, M.s);
  svg('ellipse', { cx: 560, cy: 1560, rx: 360, ry: 76, fill: 'none', stroke: '#4f8f7a', 'stroke-width': 6, opacity: 0.6 }, M.s);
  floorLamp(M.s, M.defs, 90, 1330, '#ffd59a', 0.45);
  pottedPlant(M.s, 1020, 1330, 1.05, 'snake', '#c95a4a');
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
  return { people, top, pglow, pglow2, update(t) { stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.7)).toFixed(2))); clk(21.7 + t / 600); cat(t); swayLeaves(leaves, t); } };
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
  rug(M.s, M.defs, 520, 1580, 470, 110, '#f2c14e');
  svg('ellipse', { cx: 520, cy: 1580, rx: 400, ry: 88, fill: 'none', stroke: '#fff6dc', 'stroke-width': 7, opacity: 0.6, 'stroke-dasharray': '22 14' }, M.s);
  svg('path', { d: 'M620,216 L980,216 L1180,1560 L420,1560 Z', fill: lin(M.defs, [[0, '#c9d6ff', 0.08], [1, '#c9d6ff', 0]]) }, M.s);
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
  pottedPlant(M.s, 920, 1330, 1.1, 'monstera', '#f6efe2');
  slippers(M.s, 560, 1420, '#f6a6bc');
  const tb = svg('g', { transform: 'translate(180,1400)' }, M.s);
  svg('path', { d: 'M-50,0 L-44,-80 L44,-80 L50,0 Z', fill: '#efe2c8', stroke: INK, 'stroke-width': 4 }, tb);
  svg('path', { d: 'M-24,-80 Q-24,-120 0,-120 Q24,-120 24,-80', fill: 'none', stroke: INK, 'stroke-width': 4 }, tb);
  svg('path', { d: heartPathT(0, -42, 14), fill: '#f07aa8' }, tb);
  const people = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const pglow = svg('circle', { cx: 0, cy: 0, r: 230, fill: rad2(M.defs, [[0, '#cfe4ff', 0.45], [1, '#cfe4ff', 0]]), opacity: 0 }, M.s);
  vignette(M.s, M.defs, 0.45);
  const leaves = R ? [leafG(R, -120, 1900, 1.6, -60, '#3a6b47'), leafG(R, -80, 1960, 1.4, -25, '#4f8f56')] : [];
  return {
    people, top, pglow,
    update(t) {
      stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.3)).toFixed(2)));
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.65 + 0.35 * Math.sin(t * 2.2 + i * 1.7)).toFixed(2)));
      swayLeaves(leaves, t);
    },
  };
}
