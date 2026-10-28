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
  return {
    people, table, top, herBowl, hisBowl, saucer,
    update(t) {
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.9 + 0.1 * Math.sin(t * 3 + i * 2)).toFixed(2)));
      steam.forEach((s, i) => { const k = ((t * 0.45 + i / 6) % 1); setA(s, { cx: (835 + Math.sin(k * 6 + i) * 26).toFixed(1), cy: (400 - k * 300).toFixed(1), r: (16 + k * 34).toFixed(1), opacity: (0.32 * Math.sin(Math.PI * k)).toFixed(3) }); });
      glow.setAttribute('opacity', (0.9 + 0.1 * Math.sin(t * 2.3)).toFixed(3));
      lucky(t); fan(t); clk(12.3 + t / 600);
    },
  };
}
