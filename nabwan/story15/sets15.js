// "8 ซอง" sets: the back room of อาม่า's old Chinese-Thai shophouse on ตรุษจีน morning (ochre plaster over an oxblood
// dado, folding teak doors open on a sunny street hung with lanterns, a red altar shelf with candle lamps, incense and
// a pyramid of oranges, the wall calendar, อากง's photo, a glass cabinet with the cat asleep on top, red lanterns and
// paper-cut garlands up to the beams, a round marble table with two wooden stools, a dark red terrazzo floor) in three
// eras (then = 23 years ago, b = 8 years ago, now); the grandson's rented room in Bangkok at night (plum walls, the city
// through the window, a desk lamp, a cork board with อาม่า's photo, fairy lights, a wine-red rug); two macro "insert"
// worlds: the cookie tin on the marble table (lid, envelopes, อาม่า's sleeve and hand) and the desk at night (an empty
// envelope by an open wallet). Every set returns { people, front, shadowL, top, ground, light, update(t), ... }.

function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}
const TABLE15 = { x: 540, top: 1112 }, SEAT15 = 1206, AMAX = 700, LUKX = 380;
const YEAR15 = { then: 2547, b: 2562, now: 2570 };

// a red paper lantern (hangs from (x, y0) by a cord to its top at y); returns update(t)
function lantern15(g, defs, x, y0, y, s = 1, ph = 0) {
  const L = svg('g', {}, g);
  const cord = svg('path', { stroke: '#3a2a24', 'stroke-width': 3 }, L);
  const body = svg('g', {}, L);
  svg('ellipse', { cx: 0, cy: 60 * s, rx: 120 * s, ry: 130 * s, fill: rad2(defs, [[0, '#ffb070', 0.55], [1, '#ffb070', 0]]), style: 'mix-blend-mode:screen' }, body);
  svg('rect', { x: -24 * s, y: -8 * s, width: 48 * s, height: 14 * s, rx: 3, fill: '#e8b04a', stroke: INK, 'stroke-width': 3 }, body);
  svg('ellipse', { cx: 0, cy: 58 * s, rx: 62 * s, ry: 58 * s, fill: lin(defs, [[0, '#f0503a'], [1, '#b82024']], 1, 0), stroke: INK, 'stroke-width': 4 }, body);
  for (const k of [-0.6, -0.2, 0.2, 0.6]) svg('path', { d: `M${k * 62 * s},${6 * s} Q${k * 74 * s},${58 * s} ${k * 62 * s},${110 * s}`, fill: 'none', stroke: '#8e1e26', 'stroke-width': 2.5, opacity: 0.7 }, body);
  svg('ellipse', { cx: -20 * s, cy: 36 * s, rx: 14 * s, ry: 24 * s, fill: '#ffd0a0', opacity: 0.35 }, body);
  svg('rect', { x: -22 * s, y: 110 * s, width: 44 * s, height: 12 * s, rx: 3, fill: '#e8b04a', stroke: INK, 'stroke-width': 3 }, body);
  svg('path', { d: `M0,${122 * s} L0,${150 * s} M-6,${132 * s} L-8,${170 * s} M0,${132 * s} L0,${176 * s} M6,${132 * s} L8,${170 * s}`, stroke: '#e8b04a', 'stroke-width': 3, 'stroke-linecap': 'round' }, body);
  return t => {
    const a = Math.sin(t * 1.3 + ph) * 3;
    cord.setAttribute('d', `M${x},${y0} L${(x + Math.sin(rad(a)) * (y - y0)).toFixed(1)},${y}`);
    body.setAttribute('transform', `translate(${(x + Math.sin(rad(a)) * (y - y0)).toFixed(1)},${y}) rotate(${a.toFixed(2)})`);
  };
}
// the sunny street outside the folding doors (far layer): facades, shop signs, lanterns strung across, people passing
function street15(F, mode) {
  const then = mode === 'then';
  svg('rect', { x: -500, y: -900, width: 2000, height: 3000, fill: lin(F.defs, [[0, '#ffe2b0'], [0.55, '#fff0d4'], [1, '#f2d2a0']]) }, F.s);
  const cols = ['#e8c49a', '#d6a878', '#f0d6ae', '#e2b488'];
  for (let i = 0; i < 4; i++) {
    const x = -460 + i * 250, c = cols[i];
    svg('rect', { x, y: -200, width: 244, height: 1450, fill: c, stroke: shade(c, -25), 'stroke-width': 4 }, F.s);
    for (const wy of [40, 330]) for (const dx of [30, 134]) { svg('rect', { x: x + dx, y: wy, width: 80, height: 170, rx: 30, fill: '#7a5a46' }, F.s); svg('rect', { x: x + dx + 6, y: wy + 30, width: 68, height: 140, fill: then ? '#c8a888' : '#9ab0b8', opacity: 0.6 }, F.s); }
    svg('rect', { x: x + 14, y: 620, width: 216, height: 70, rx: 6, fill: ['#c8343c', '#2f6a4a', '#c8343c', '#e8b04a'][i], stroke: INK, 'stroke-width': 3 }, F.s);
    svg('rect', { x: x + 40, y: 640, width: 164, height: 28, rx: 4, fill: '#f6e2a8', opacity: 0.8 }, F.s);
    svg('rect', { x: x + 20, y: 740, width: 204, height: 500, fill: '#6a5040' }, F.s);
    for (let k = 0; k < 12; k++) svg('rect', { x: x + 20, y: 750 + k * 40, width: 204, height: 4, fill: '#4a3628', opacity: 0.6 }, F.s);
  }
  svg('rect', { x: -500, y: 1240, width: 2000, height: 400, fill: lin(F.defs, [[0, '#b8a088'], [1, '#8a7464']]) }, F.s);
  const strs = [], r = rng(1501);
  for (const [y, n] of [[260, 6], [520, 5]]) {
    svg('path', { d: `M-500,${y} Q100,${y + 60} 700,${y}`, fill: 'none', stroke: '#3a2a24', 'stroke-width': 3 }, F.s);
    for (let k = 0; k < n; k++) { const u = (k + 0.5) / n, x = -500 + 1200 * u, yy = y + 60 * 4 * u * (1 - u) * 0.5 + 10; strs.push({ x, y: yy, ph: r() * 6, el: svg('g', {}, F.s) }); }
  }
  strs.forEach(s => { svg('ellipse', { cx: 0, cy: 26, rx: 26, ry: 24, fill: '#d8343a', stroke: INK, 'stroke-width': 3 }, s.el); svg('rect', { x: -10, y: 0, width: 20, height: 6, fill: '#e8b04a' }, s.el); svg('path', { d: 'M0,50 L0,68', stroke: '#e8b04a', 'stroke-width': 3 }, s.el); });
  const folk = Array.from({ length: 3 }, (_, i) => { const g = svg('g', { opacity: 0.85 }, F.s); svg('circle', { cx: 0, cy: -150, r: 26, fill: '#3a2a24' }, g); svg('rect', { x: -26, y: -124, width: 52, height: 80, rx: 14, fill: ['#d8343a', '#f2c14e', '#e8e2d6'][i] }, g); svg('rect', { x: -22, y: -44, width: 44, height: 44, fill: '#3a3a4a' }, g); return { g, sp: 40 + i * 22, x0: i * 330 }; });
  return t => {
    strs.forEach(s => s.el.setAttribute('transform', `translate(${s.x.toFixed(1)},${s.y.toFixed(1)}) rotate(${(Math.sin(t * 1.6 + s.ph) * 6).toFixed(1)})`));
    folk.forEach(f => f.g.setAttribute('transform', `translate(${(-420 + ((f.x0 + t * f.sp) % 1100)).toFixed(1)},${(1290 - Math.abs(Math.sin(t * 5 + f.x0)) * 6).toFixed(1)})`));
  };
}
// a round marble table in profile (top at y), on a teak pedestal
function marbleTable15(g, defs, x, y) {
  const t = svg('g', {}, g);
  svg('path', { d: `M${x - 30},${y + 20} L${x - 22},1300 L${x + 22},1300 L${x + 30},${y + 20} Z`, fill: '#4a2a1e', stroke: INK, 'stroke-width': 4 }, t);
  svg('path', { d: `M${x - 110},1332 Q${x},1290 ${x + 110},1332 Z`, fill: '#3a2018', stroke: INK, 'stroke-width': 4 }, t);
  svg('rect', { x: x - 176, y: y + 6, width: 352, height: 18, rx: 6, fill: '#5a3424', stroke: INK, 'stroke-width': 4 }, t);
  svg('ellipse', { cx: x, cy: y + 4, rx: 176, ry: 22, fill: lin(defs, [[0, '#fbf8f2'], [1, '#e2ddd4']]), stroke: INK, 'stroke-width': 4 }, t);
  svg('path', { d: `M${x - 120},${y + 6} q40,-10 70,2 t60,-4 M${x + 30},${y + 14} q30,-8 70,-4`, fill: 'none', stroke: '#b8b2a8', 'stroke-width': 2, opacity: 0.8 }, t);
  return t;
}
// a round wooden stool (seat top at y)
function stool15(g, x, y) {
  const s = svg('g', {}, g);
  svg('path', { d: `M${x - 36},${y + 10} L${x - 50},1330 M${x + 36},${y + 10} L${x + 50},1330 M${x - 12},${y + 12} L${x - 16},1328 M${x + 12},${y + 12} L${x + 16},1328`, stroke: '#6a3a24', 'stroke-width': 9, 'stroke-linecap': 'round' }, s);
  svg('path', { d: `M${x - 44},1270 L${x + 44},1270`, stroke: '#5a3020', 'stroke-width': 6 }, s);
  svg('rect', { x: x - 56, y, width: 112, height: 16, rx: 8, fill: '#9a5a34', stroke: INK, 'stroke-width': 4 }, s);
  return s;
}
function shophouse15(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1330, mode = o.mode || 'now', then = mode === 'then', D = M.defs;
  const st = street15(F, mode);
  // the wall from the beams down, with the door opening on the left
  const DX0 = 10, DX1 = 236, DY0 = 290;
  svg('path', { d: `M-400,-760 L1500,-760 L1500,${G} L-400,${G} Z M${DX0},${DY0} L${DX1},${DY0} L${DX1},${G} L${DX0},${G} Z`, fill: lin(D, [[0, '#c48a44'], [0.5, '#dba862'], [1, '#d09a54']]), 'fill-rule': 'evenodd' }, M.s);
  const r = rng(1502);
  for (let i = 0; i < 16; i++) svg('ellipse', { cx: 260 + r() * 1100, cy: -500 + r() * 1300, rx: 40 + r() * 120, ry: 20 + r() * 60, fill: '#a8723a', opacity: 0.08 + r() * 0.08 }, M.s);   // old plaster patina
  svg('path', { d: `M-400,880 L${DX0},880 L${DX0},${G} L-400,${G} Z M${DX1},880 L1500,880 L1500,${G} L${DX1},${G} Z`, fill: '#7e2e26' }, M.s);   // oxblood dado
  svg('rect', { x: DX1, y: 870, width: 1300, height: 12, fill: '#e8c88a', stroke: INK, 'stroke-width': 2 }, M.s);
  for (let x = DX1 + 40; x < 1500; x += 120) svg('rect', { x, y: 920, width: 80, height: 360, rx: 6, fill: 'none', stroke: '#6a241e', 'stroke-width': 4 }, M.s);
  // beams and the upper floor's joists
  svg('rect', { x: -400, y: -760, width: 1900, height: 120, fill: '#4a2a1e' }, M.s);
  for (let x = -380; x < 1500; x += 160) svg('rect', { x, y: -650, width: 34, height: 70, fill: '#5a3424', stroke: INK, 'stroke-width': 3 }, M.s);
  svg('rect', { x: -400, y: -590, width: 1900, height: 22, fill: '#6a3a24', stroke: INK, 'stroke-width': 3 }, M.s);
  // the door: teak frame, folded doors on the wall, a 福-style diamond of red paper (a gold coin motif, no text)
  svg('rect', { x: DX0 - 12, y: DY0 - 14, width: DX1 - DX0 + 24, height: G - DY0 + 14, fill: 'none', stroke: '#4a2a1e', 'stroke-width': 18 }, M.s);
  for (let k = 0; k < 3; k++) {
    const x = DX1 + 10 + k * 26;
    svg('path', { d: `M${x},${DY0 + 4} L${x + 30},${DY0 + 14} L${x + 30},${G - 6} L${x},${G} Z`, fill: k % 2 ? '#7a4428' : '#8a5030', stroke: INK, 'stroke-width': 3.5 }, M.s);
    for (let j = 0; j < 9; j++) svg('path', { d: `M${x + 5},${DY0 + 60 + j * 100} L${x + 25},${DY0 + 66 + j * 100}`, stroke: '#5a3020', 'stroke-width': 4 }, M.s);
  }
  const dia = svg('g', { transform: `translate(${DX1 + 50},560) rotate(45)` }, M.s);
  svg('rect', { x: -38, y: -38, width: 76, height: 76, fill: '#d43a40', stroke: INK, 'stroke-width': 3 }, dia);
  svg('circle', { r: 22, fill: 'none', stroke: '#f2c14e', 'stroke-width': 5 }, dia); svg('rect', { x: -7, y: -7, width: 14, height: 14, fill: '#f2c14e' }, dia);
  // the calendar (the year flips in the time-lapse)
  const cal = svg('g', {}, M.s);
  svg('rect', { x: 400, y: 420, width: 150, height: 210, rx: 6, fill: '#fbf7ee', stroke: INK, 'stroke-width': 4 }, cal);
  svg('rect', { x: 400, y: 420, width: 150, height: 54, rx: 6, fill: '#c8343c', stroke: INK, 'stroke-width': 4 }, cal);
  svg('circle', { cx: 475, cy: 414, r: 6, fill: '#3a2a24' }, cal);
  const calY = wtext(cal, 475, 458, 'พ.ศ. ' + YEAR15[mode], 24, '#ffe9a8', { w: 600 });
  wtext(cal, 475, 560, '6', 92, '#c8343c', { w: 800 });
  wtext(cal, 475, 610, 'ตรุษจีน', 26, '#3a2a24', { w: 600 });
  const page = svg('rect', { x: 400, y: 474, width: 150, height: 156, fill: '#fbf7ee', stroke: INK, 'stroke-width': 3, opacity: 0 }, cal);
  // อากง's photo (or a mirror, back then), the clock
  if (then) { svg('ellipse', { cx: 655, cy: 500, rx: 56, ry: 72, fill: '#8a5030', stroke: INK, 'stroke-width': 4 }, M.s); svg('ellipse', { cx: 655, cy: 500, rx: 44, ry: 60, fill: lin(D, [[0, '#e8f0ec'], [1, '#c8d4d0']]) }, M.s); svg('path', { d: 'M630,470 L650,450', stroke: '#fff', 'stroke-width': 5, opacity: 0.7 }, M.s); }
  else {
    svg('rect', { x: 600, y: 430, width: 110, height: 140, rx: 4, fill: '#3a2a24', stroke: INK, 'stroke-width': 4 }, M.s);
    svg('rect', { x: 610, y: 440, width: 90, height: 120, fill: '#d8c8a8' }, M.s);
    svg('circle', { cx: 655, cy: 484, r: 22, fill: '#a89878' }, M.s); svg('path', { d: 'M620,560 Q655,500 690,560 Z', fill: '#6a5a48' }, M.s);
    svg('path', { d: 'M600,430 L620,410 L690,410 L710,430', fill: 'none', stroke: '#3a2a24', 'stroke-width': 5 }, M.s);   // a black ribbon bow over the frame
  }
  const clock = wallClock(M.s, 655, 330, 34, '#8a5030'); clock(8.3);
  // the altar shelf: red lacquer, two candle lamps, incense, a pyramid of oranges
  const alt = svg('g', {}, M.s);
  lightPool(alt, D, 920, 400, 240, 170, '#ff9a5a', 0.4);
  svg('rect', { x: 800, y: 420, width: 250, height: 22, rx: 3, fill: '#a8242a', stroke: INK, 'stroke-width': 4 }, alt);
  svg('path', { d: 'M820,442 L840,480 L860,442 M990,442 L1010,480 L1030,442', fill: 'none', stroke: '#a8242a', 'stroke-width': 8 }, alt);
  svg('rect', { x: 870, y: 300, width: 110, height: 120, rx: 6, fill: '#c8343c', stroke: '#e8b04a', 'stroke-width': 5 }, alt);
  svg('circle', { cx: 925, cy: 360, r: 30, fill: 'none', stroke: '#f2c14e', 'stroke-width': 4 }, alt);
  const flames = [];
  for (const x of [830, 1020]) { svg('rect', { x: x - 9, y: 360, width: 18, height: 60, rx: 4, fill: '#d8343a', stroke: INK, 'stroke-width': 3 }, alt); flames.push(svg('path', { fill: '#ffd06a', stroke: '#e88a2a', 'stroke-width': 2 }, alt)); svg('circle', { cx: x, cy: 352, r: 26, fill: rad2(D, [[0, '#ffd06a', 0.6], [1, '#ffd06a', 0]]) }, alt); }
  svg('path', { d: 'M890,420 L894,400 L956,400 L960,420 Z', fill: '#e8b04a', stroke: INK, 'stroke-width': 3 }, alt);
  const smoke = [0, 1, 2].map(() => svg('path', { fill: 'none', stroke: '#fff6ec', 'stroke-width': 3, 'stroke-linecap': 'round' }, alt));
  for (const dx of [-8, 0, 8]) svg('path', { d: `M${925 + dx},400 L${925 + dx * 1.6},360`, stroke: '#8a3a24', 'stroke-width': 3 }, alt);
  for (const [x, y] of [[994, 414], [1018, 414], [1006, 394]]) { svg('circle', { cx: x, cy: y, r: 12, fill: '#f29a2e', stroke: INK, 'stroke-width': 2.5 }, alt); }
  // the glass cabinet (right) with plates, tins and jars; the cat asleep on top
  svg('rect', { x: 880, y: 640, width: 260, height: G - 640, fill: '#6a3a24', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: 900, y: 680, width: 220, height: 300, fill: lin(D, [[0, '#d8e4dc', 0.5], [1, '#a8b8b0', 0.4]]), stroke: '#4a2a1e', 'stroke-width': 5 }, M.s);
  for (let k = 0; k < 3; k++) svg('ellipse', { cx: 940 + k * 50, cy: 760, rx: 22, ry: 40, fill: '#f4efe6', stroke: '#2f4fa0', 'stroke-width': 4 }, M.s);
  svg('rect', { x: 900, y: 830, width: 220, height: 6, fill: '#4a2a1e' }, M.s);
  for (let k = 0; k < 4; k++) svg('rect', { x: 912 + k * 50, y: 880 - k % 2 * 14, width: 40, height: 50 + k % 2 * 14, rx: 6, fill: ['#e8b04a', '#c8d8c0', '#d43a40', '#f6efe2'][k], stroke: INK, 'stroke-width': 3 }, M.s);
  svg('rect', { x: 900, y: 1000, width: 220, height: 300, fill: '#7a4428', stroke: INK, 'stroke-width': 3 }, M.s);
  svg('circle', { cx: 1000, cy: 1140, r: 7, fill: '#e8b04a', stroke: INK, 'stroke-width': 2 }, M.s);
  if (then) { svg('rect', { x: 900, y: 540, width: 150, height: 100, rx: 14, fill: '#4a4a52', stroke: INK, 'stroke-width': 4 }, M.s); svg('rect', { x: 914, y: 552, width: 110, height: 76, rx: 10, fill: '#6a8a9a' }, M.s); }   // an old TV
  else {
    svg('rect', { x: 900, y: 596, width: 70, height: 44, rx: 8, fill: '#c8a060', stroke: INK, 'stroke-width': 3 }, M.s); svg('circle', { cx: 920, cy: 618, r: 12, fill: '#6a4a32' }, M.s);   // a radio
  }
  const cat = then ? null : sleepyCat(M.s, 1040, 640, 0.48, '#e8a050');
  // red string lights and a paper-cut garland
  const bulbs = lightString(M.s, DX1, 1500, 230, 26, ['#ff5a4a', '#ffd06a', '#ff8a5a'], 16);
  bunting(M.s, -400, 1500, -380, 30, 26, ['#d8343a', '#f2c14e', '#d8343a', '#e88a3a']);
  // lucky bamboo in a blue-and-white pot by the door
  const pl = svg('g', {}, M.s);
  svg('path', { d: `M300,${G} L290,${G - 70} Q320,${G - 90} 350,${G - 70} L340,${G} Z`, fill: '#f4efe6', stroke: INK, 'stroke-width': 4 }, pl);
  svg('path', { d: `M296,${G - 40} Q320,${G - 54} 344,${G - 40}`, fill: 'none', stroke: '#2f4fa0', 'stroke-width': 5 }, pl);
  for (const [dx, h] of [[-12, 240], [0, 300], [12, 210]]) { svg('path', { d: `M${320 + dx},${G - 70} L${320 + dx * 1.5},${G - 70 - h}`, stroke: '#7ab85a', 'stroke-width': 10, 'stroke-linecap': 'round' }, pl); for (let k = 1; k < 4; k++) svg('path', { d: `M${320 + dx * 1.5 - 7},${G - 70 - h * k / 4} l14,0`, stroke: '#4f8a3e', 'stroke-width': 4 }, pl); svg('path', { d: `M${320 + dx * 1.5},${G - 70 - h} q${dx > 0 ? 30 : -30},-10 ${dx > 0 ? 44 : -44},10`, fill: '#5aa04a', stroke: INK, 'stroke-width': 2.5 }, pl); }
  // floor: dark red terrazzo
  svg('rect', { x: -400, y: G, width: 1900, height: 900, fill: lin(D, [[0, '#6a2e26'], [1, '#2e120e']]) }, M.s);
  for (let i = 0; i < 140; i++) { const y = G + 10 + Math.pow(r(), 1.4) * 700; svg('circle', { cx: -300 + r() * 1700, cy: y, r: 1.5 + r() * 3.5, fill: ['#e8c8a0', '#2a0e0a', '#c88a6a'][i % 3], opacity: 0.5 }, M.s); }
  slippers(M.s, 170, 1392, '#2a2228', 1.1); slippers(M.s, 980, 1404, '#c8343c', 1.0);
  wallAO(M.s, D, G, { op: 0.32 });
  // sun through the doors, the altar glow
  const shaft = lightShaft(M.s, D, [[DX0 + 10, DY0 + 20], [DX1, DY0 + 20], [DX1 + 560, 1700], [DX0 + 140, 1700]], then ? '#ffd890' : '#fff0c8', then ? 0.24 : 0.2, 1503, 30);
  lightPool(M.s, D, 300, G + 40, 300, 60, '#fff0c8', 0.35);
  // lanterns, high and low
  const lans = [lantern15(M.s, D, 330, -568, 70, 1, 0), lantern15(M.s, D, 780, -568, 40, 1.1, 1.3), lantern15(M.s, D, 560, -568, -260, 0.9, 2.1), lantern15(M.s, D, 1000, -568, -200, 0.8, 0.7), lantern15(M.s, D, 120, -568, -320, 0.8, 2.6)];
  // stools behind the sitters, the table in front
  const stools = svg('g', {}, M.s); stool15(stools, AMAX + 10, SEAT15); stool15(stools, LUKX - 10, SEAT15);
  const shadowL = svg('g', {}, M.s);
  const people = svg('g', {}, M.s);
  const front = svg('g', {}, M.s); marbleTable15(front, D, TABLE15.x, TABLE15.top);
  const top = svg('g', {}, M.s);
  let bok = null;
  if (R) {
    bok = bokehField(R.s, R.defs, 6, [-100, -60, 1180, 380], ['#ff8a5a', '#ffd06a', '#ff5a4a'], 1504, { rMin: 30, rMax: 80, op: 0.32 });
    const fl = svg('g', { transform: 'translate(-40,-80)' }, R.s); lantern15(fl, R.defs, 0, -400, 0, 1.5, 0)(0);   // a near lantern, soft
  }
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 50%, rgba(40,10,6,.5) 100%)';
  return {
    people, front, shadowL, top, ground: G, seat: SEAT15, tableTop: TABLE15.top, door: (DX0 + DX1) / 2, stools,
    light: { ux: -0.72, uy: -0.69, lx: 120 },
    year(y, flip = 0) { calY.textContent = 'พ.ศ. ' + y; page.setAttribute('opacity', (flip > 0 && flip < 1 ? 1 : 0)); page.setAttribute('transform', `translate(0,${(-flip * 40).toFixed(1)}) skewX(${(flip * 20).toFixed(1)})`); },
    update(t) {
      st(t); shaft(t); lans.forEach(l => l(t)); if (cat) cat(t); if (bok) bok(t);
      flames.forEach((fl, i) => { const x = [830, 1020][i], h = 16 + Math.sin(t * 9 + i) * 3; fl.setAttribute('d', `M${x - 6},356 Q${x},${356 - h * 2} ${x + 6},356 Q${x},362 ${x - 6},356 Z`); });
      smoke.forEach((s, i) => { const u = (t * 0.25 + i / 3) % 1; s.setAttribute('d', `M${925 + (i - 1) * 12},${360 - u * 30} q${(8 * Math.sin(t + i)).toFixed(1)},-30 0,-60 q-10,-30 0,-60`); s.setAttribute('opacity', (0.35 * Math.sin(Math.PI * u)).toFixed(2)); });
      bulbs.forEach((b, i) => b.setAttribute('opacity', (0.75 + 0.25 * Math.sin(t * 3 + i * 1.7)).toFixed(2)));
    },
  };
}

// the grandson's rented room in Bangkok at night
function room15(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1330, D = M.defs;
  // the city through the window (far)
  svg('rect', { x: -400, y: -400, width: 1900, height: 1700, fill: lin(F.defs, [[0, '#1a1638'], [0.7, '#3a2a5a'], [1, '#6a3a5a']]) }, F.s);
  const r = rng(1505), stars = [];
  for (let i = 0; i < 30; i++) stars.push(svg('circle', { cx: 560 + r() * 520, cy: 220 + r() * 260, r: 1 + r() * 1.8, fill: '#fff' }, F.s));
  svg('circle', { cx: 900, cy: 340, r: 80, fill: rad2(F.defs, [[0, '#fff2d0', 0.5], [1, '#fff2d0', 0]]) }, F.s);
  svg('circle', { cx: 900, cy: 340, r: 34, fill: '#f8eed4' }, F.s);
  let bx = 520;
  while (bx < 1180) { const bw = 40 + r() * 60, bh = 140 + r() * 260; svg('rect', { x: bx, y: 760 - bh, width: bw, height: bh + 40, fill: r() > 0.5 ? '#251f44' : '#2e2650' }, F.s); for (let wy = 780 - bh; wy < 760; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14) if (r() > 0.55) svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#f6c86a', opacity: 0.85 }, F.s); bx += bw + 4; }
  // plum walls with the window hole, the door on the left
  const WX0 = 600, WX1 = 1000, WY0 = 300, WY1 = 760;
  svg('path', { d: `M-400,-400 L1500,-400 L1500,${G} L-400,${G} Z M${WX0},${WY0} L${WX1},${WY0} L${WX1},${WY1} L${WX0},${WY1} Z`, fill: lin(D, [[0, '#4e3354'], [1, '#6a4670']]), 'fill-rule': 'evenodd' }, M.s);
  svg('rect', { x: WX0 - 10, y: WY0 - 10, width: WX1 - WX0 + 20, height: WY1 - WY0 + 20, fill: 'none', stroke: '#e8dccc', 'stroke-width': 16 }, M.s);
  svg('rect', { x: (WX0 + WX1) / 2 - 5, y: WY0, width: 10, height: WY1 - WY0, fill: '#e8dccc' }, M.s);
  svg('rect', { x: WX0 - 30, y: WY1 + 4, width: WX1 - WX0 + 60, height: 18, rx: 5, fill: '#d8ccbc', stroke: INK, 'stroke-width': 4 }, M.s);
  for (const [x, sg] of [[WX0 - 20, -1], [WX1 + 20, 1]]) svg('path', { d: `M${x},${WY0 - 40} Q${x + sg * 60},${(WY0 + WY1) / 2} ${x + sg * 30},${WY1 + 60} L${x + sg * 90},${WY1 + 60} Q${x + sg * 110},${(WY0 + WY1) / 2} ${x + sg * 80},${WY0 - 40} Z`, fill: '#c88a5a', stroke: INK, 'stroke-width': 4 }, M.s);
  const fairy = lightString(M.s, WX0 - 40, WX1 + 40, WY0 - 50, 22, ['#ffd06a', '#ffb0c8', '#fff2c0'], 13);
  svg('rect', { x: 20, y: 360, width: 170, height: G - 360, fill: '#3a2440', stroke: '#2a1a30', 'stroke-width': 10 }, M.s);   // the door (closed), its frame
  svg('circle', { cx: 160, cy: 860, r: 9, fill: '#e8c070', stroke: INK, 'stroke-width': 3 }, M.s);
  // the desk: lamp, closed laptop, a mug, papers; a cork board with อาม่า's photo, a poster
  const dk = svg('g', {}, M.s);
  svg('rect', { x: 240, y: 1040, width: 300, height: 22, rx: 4, fill: '#8a5a3a', stroke: INK, 'stroke-width': 4 }, dk);
  svg('path', { d: 'M256,1062 L256,1330 M524,1062 L524,1330', stroke: '#6a4228', 'stroke-width': 12 }, dk);
  svg('rect', { x: 300, y: 1026, width: 150, height: 14, rx: 4, fill: '#9a9aa8', stroke: INK, 'stroke-width': 3 }, dk);
  mugProp(dk, 480, 1040, '#e8a84a');
  for (let k = 0; k < 3; k++) svg('rect', { x: 262 + k * 4, y: 1028 - k * 6, width: 34, height: 6, fill: '#f6efe2', stroke: INK, 'stroke-width': 1.5 }, dk);
  svg('path', { d: 'M500,1040 L500,940 L520,930', fill: 'none', stroke: '#3a2a3a', 'stroke-width': 6 }, dk);
  svg('path', { d: 'M486,930 L540,930 L530,890 L496,890 Z', fill: '#f2c14e', stroke: INK, 'stroke-width': 4 }, dk);
  lampCone(M.s, D, 513, 932, 260, 120, '#ffd890', 0.35, false);
  lightPool(M.s, D, 500, 900, 260, 200, '#ffc878', 0.35);
  corkBoard(M.s, 250, 560, 230, 230, 1506);
  const ph = svg('g', { transform: 'rotate(-5 380 690)' }, M.s);   // the polaroid of อาม่า
  svg('rect', { x: 340, y: 640, width: 80, height: 96, fill: '#fbf8f2', stroke: INK, 'stroke-width': 3 }, ph);
  svg('rect', { x: 348, y: 648, width: 64, height: 64, fill: '#e8c49a' }, ph);
  svg('circle', { cx: 380, cy: 676, r: 16, fill: '#f0cba8' }, ph); svg('circle', { cx: 372, cy: 660, r: 8, fill: '#ece8e2' }, ph); svg('path', { d: 'M358,712 Q380,690 402,712 Z', fill: '#a82a35' }, ph);
  svg('circle', { cx: 380, cy: 644, r: 5, fill: '#e0453b', stroke: INK, 'stroke-width': 1.5 }, ph);
  poster(M.s, 1060, 420, 160, 220, 'mountain', '#f2c14e');
  const clock = wallClock(M.s, 300, 440, 30, '#c88a5a'); clock(23.7);
  pottedPlant(M.s, 580, G, 0.6, 'snake', '#e8e2d6');
  // the bed (right)
  const bed = svg('g', {}, M.s);
  svg('rect', { x: 640, y: 1150, width: 600, height: 180, rx: 10, fill: '#5a3a2a', stroke: INK, 'stroke-width': 5 }, bed);
  svg('rect', { x: 640, y: 1120, width: 600, height: 60, rx: 16, fill: '#efe2d0', stroke: INK, 'stroke-width': 4 }, bed);
  svg('path', { d: 'M760,1118 Q900,1100 1240,1110 L1240,1200 Q980,1196 740,1200 Z', fill: '#d9a83e', stroke: INK, 'stroke-width': 4 }, bed);
  for (let k = 0; k < 6; k++) svg('path', { d: `M${790 + k * 70},1124 l20,60`, stroke: '#b88a2a', 'stroke-width': 5, opacity: 0.6 }, bed);
  svg('rect', { x: 1090, y: 1060, width: 160, height: 70, rx: 28, fill: '#f6efe2', stroke: INK, 'stroke-width': 4 }, bed);
  // floor: dark wood and a wine rug
  svg('rect', { x: -400, y: G, width: 1900, height: 900, fill: lin(D, [[0, '#4a2a34'], [1, '#1e0e14']]) }, M.s);
  for (let y = G + 30, k = 0; y < 2200; y += 46 + k * 10, k++) svg('rect', { x: -400, y, width: 1900, height: 3, fill: '#140810', opacity: 0.5 }, M.s);
  svg('ellipse', { cx: 520, cy: 1560, rx: 520, ry: 130, fill: '#5a2236', stroke: '#3a1424', 'stroke-width': 6 }, M.s);
  svg('ellipse', { cx: 520, cy: 1560, rx: 430, ry: 96, fill: 'none', stroke: '#7a3248', 'stroke-width': 6, 'stroke-dasharray': '18 12' }, M.s);
  wallAO(M.s, D, G, { op: 0.34 });
  svg('rect', { x: 196, y: 1250, width: 70, height: 80, rx: 14, fill: '#3f5a8a', stroke: INK, 'stroke-width': 4 }, M.s);   // a backpack by the door
  slippers(M.s, 900, 1400, '#e8a84a', 1.1);
  const shadowL = svg('g', {}, M.s);
  const people = svg('g', {}, M.s);
  const front = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 340], ['#ffd06a', '#ffb0c8', '#ff9a6a'], 1507, { rMin: 26, rMax: 70, op: 0.26 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 46%, rgba(16,6,20,.6) 100%)';
  return {
    people, front, shadowL, top, ground: G, seat: 1150, light: { ux: -0.5, uy: -0.86, lx: 500 },
    update(t) { stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i * 1.3)).toFixed(2))); fairy.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2.4 + i)).toFixed(2))); if (bok) bok(t); },
  };
}

// ---------------- macro inserts ----------------
// an envelope lying flat in the tin (world, macro scale): returns its group
function flatEnv15(parent, defs, x, y, a, year, o = {}) {
  const g = svg('g', { transform: `translate(${x},${y}) scale(1,0.52) rotate(${a})` }, parent), w = 220, h = 330;
  svg('rect', { x: -w / 2 + 8, y: -h / 2 + 10, width: w, height: h, rx: 10, fill: '#000', opacity: 0.25 }, g);
  svg('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: 10, fill: o.flat ? '#c23a42' : lin(defs, [[0, '#e04a48'], [1, '#b82a32']]), stroke: INK, 'stroke-width': 6 }, g);
  svg('rect', { x: -w / 2 + 16, y: -h / 2 + 16, width: w - 32, height: h - 32, rx: 4, fill: 'none', stroke: '#f2c14e', 'stroke-width': 5 }, g);
  svg('path', { d: `M${-w / 2},${-h / 2 + 6} L0,${-h / 2 + 96} L${w / 2},${-h / 2 + 6}`, fill: 'none', stroke: '#8e1e26', 'stroke-width': 6, 'stroke-linejoin': 'round' }, g);
  svg('circle', { cx: 0, cy: -h / 2 + 96, r: 20, fill: '#f2c14e', stroke: '#a8781e', 'stroke-width': 4 }, g);   // the seal, never broken
  svg('circle', { cx: 0, cy: 30, r: 46, fill: '#f2c14e', stroke: '#a8781e', 'stroke-width': 5 }, g);
  svg('rect', { x: -15, y: 15, width: 30, height: 30, fill: '#d43a40' }, g);
  if (year) wtext(g, 40, h / 2 - 34, year, 46, '#1e3a8a', { w: 600, a: { transform: 'rotate(-6 40 130)', 'font-style': 'italic' } });
  return g;
}
// the cookie tin on the marble table, seen from above at an angle; returns controls
function tinMacro15(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, D = M.defs;
  // the room behind, out of focus (far)
  svg('rect', { x: -400, y: -400, width: 1900, height: 1400, fill: lin(F.defs, [[0, '#c48a44'], [0.7, '#9a5a30'], [1, '#6a2e26']]) }, F.s);
  for (const [x, y, c, rr] of [[180, 220, '#ff5a4a', 90], [820, 160, '#ff8a5a', 110], [500, 300, '#ffd06a', 60], [980, 420, '#ff5a4a', 70], [60, 520, '#ffd06a', 50]]) svg('circle', { cx: x, cy: y, r: rr, fill: rad2(F.defs, [[0, c, 0.8], [1, c, 0]]) }, F.s);
  // the marble table top (mid)
  svg('path', { d: 'M-400,640 Q540,560 1480,640 L1480,2200 L-400,2200 Z', fill: lin(D, [[0, '#ece4d6'], [0.6, '#d2c6b2'], [1, '#a8988a']]) }, M.s);
  svg('path', { d: 'M-400,640 Q540,560 1480,640', fill: 'none', stroke: '#a89c8c', 'stroke-width': 6 }, M.s);
  for (const d of ['M-100,900 q200,-40 380,30 t400,-20', 'M200,1500 q240,-60 520,10 t300,40', 'M-60,1760 q300,-30 600,40', 'M700,820 q120,30 300,-10']) svg('path', { d, fill: 'none', stroke: '#b8b0a4', 'stroke-width': 4, opacity: 0.7 }, M.s);
  lightPool(M.s, D, 420, 1150, 700, 420, '#fff2d0', 0.35);
  // the rest of the table at the frame edges: the teacups (top right), the mandarins he brought (bottom left)
  for (const [x, y] of [[930, 740], [1060, 790]]) { svg('ellipse', { cx: x, cy: y + 40, rx: 70, ry: 22, fill: '#3a2018', opacity: 0.18 }, M.s); svg('path', { d: `M${x - 62},${y - 30} L${x + 62},${y - 30} L${x + 46},${y + 36} Q${x},${y + 50} ${x - 46},${y + 36} Z`, fill: '#f4efe6', stroke: INK, 'stroke-width': 6 }, M.s); svg('ellipse', { cx: x, cy: y - 30, rx: 62, ry: 18, fill: '#b8702a', stroke: INK, 'stroke-width': 6 }, M.s); svg('path', { d: `M${x - 54},${y - 4} Q${x},${y + 8} ${x + 54},${y - 4}`, fill: 'none', stroke: '#2f4fa0', 'stroke-width': 7 }, M.s); }
  for (const [x, y, r] of [[60, 1430, 96], [200, 1500, 84], [-40, 1300, 80], [120, 1300, 70]]) { svg('circle', { cx: x, cy: y, r, fill: '#f29a2e', stroke: INK, 'stroke-width': 7 }, M.s); svg('circle', { cx: x - r * 0.35, cy: y - r * 0.35, r: r * 0.25, fill: '#ffd28a', opacity: 0.8 }, M.s); svg('path', { d: `M${x},${y - r} q14,-26 40,-20`, fill: 'none', stroke: '#3f8a52', 'stroke-width': 8, 'stroke-linecap': 'round' }, M.s); }
  const cx = 540, cy = 1060, RX = 380, RY = 170, H = 260;
  const shadow = svg('ellipse', { cx: cx + 30, cy: cy + H + 30, rx: RX + 40, ry: RY * 0.8, fill: '#3a2018', opacity: 0.25, filter: blurFilter(D, 18) }, M.s);
  // the tin: outer wall, inside, rim
  svg('path', { d: `M${cx - RX},${cy} L${cx - RX},${cy + H} A${RX},${RY} 0 0 0 ${cx + RX},${cy + H} L${cx + RX},${cy} Z`, fill: lin(D, [[0, '#26408a'], [0.5, '#3a5cb0'], [1, '#22387a']], 1, 0), stroke: INK, 'stroke-width': 7 }, M.s);
  svg('path', { d: `M${cx - RX},${cy + 70} A${RX},${RY} 0 0 0 ${cx + RX},${cy + 70} L${cx + RX},${cy + 150} A${RX},${RY} 0 0 1 ${cx - RX},${cy + 150} Z`, fill: '#f2e6c8', opacity: 0.92 }, M.s);
  for (let k = 0; k < 9; k++) { const a = Math.PI * (0.1 + k * 0.1), x = cx - Math.cos(a) * RX * 0.98, y = cy + 110 + Math.sin(a) * RY; svg('circle', { cx: x, cy: y, r: 16, fill: '#2f4fa0' }, M.s); }
  svg('path', { d: `M${cx - RX + 30},${cy + 40} L${cx - RX + 30},${cy + H - 10}`, stroke: '#9ab4f0', 'stroke-width': 12, 'stroke-linecap': 'round', opacity: 0.45 }, M.s);
  svg('ellipse', { cx, cy, rx: RX, ry: RY, fill: '#1a2850', stroke: INK, 'stroke-width': 7 }, M.s);
  svg('ellipse', { cx, cy: cy + 26, rx: RX - 26, ry: RY - 22, fill: '#f6efe2' }, M.s);   // the paper doily at the bottom
  for (let k = 0; k < 24; k++) { const a = k / 24 * Math.PI * 2; svg('circle', { cx: cx + Math.cos(a) * (RX - 40), cy: cy + 26 + Math.sin(a) * (RY - 34), r: 9, fill: '#e8dccc' }, M.s); }
  // the envelopes inside: eight, years in อาม่า's hand; the order they were put in
  const envG = svg('g', {}, M.s), envs = [];
  const YRS = ['2562', '2563', '2564', '2565', '2566', '2567', '2568', '2569'];
  for (let i = 0; i < 8; i++) { const e = svg('g', {}, envG); envs.push({ g: e, inner: flatEnv15(e, D, 0, 0, 0, YRS[i]) }); }
  const glints = envs.map(() => { const g = svg('g', { opacity: 0 }, M.s); svg('path', { d: 'M0,-26 L6,-6 L26,0 L6,6 L0,26 L-6,6 L-26,0 L-6,-6 Z', fill: '#fffbe8' }, g); svg('circle', { r: 34, fill: rad2(D, [[0, '#fff6c0', 0.8], [1, '#fff6c0', 0]]) }, g); return g; });
  svg('path', { d: `M${cx - RX},${cy} A${RX},${RY} 0 0 0 ${cx + RX},${cy}`, fill: 'none', stroke: '#e8b04a', 'stroke-width': 10 }, M.s);   // the front rim over the envelopes
  // the lid
  const lid = svg('g', {}, M.s);
  svg('path', { d: `M${cx - RX - 14},${cy - 8} L${cx - RX - 14},${cy + 30} A${RX + 14},${RY + 10} 0 0 0 ${cx + RX + 14},${cy + 30} L${cx + RX + 14},${cy - 8} Z`, fill: '#26408a', stroke: INK, 'stroke-width': 7 }, lid);
  svg('ellipse', { cx, cy: cy - 8, rx: RX + 14, ry: RY + 10, fill: lin(D, [[0, '#4a6cc8'], [1, '#2a4490']]), stroke: INK, 'stroke-width': 7 }, lid);
  svg('ellipse', { cx, cy: cy - 8, rx: RX - 50, ry: RY - 36, fill: 'none', stroke: '#e8b04a', 'stroke-width': 8 }, lid);
  svg('ellipse', { cx, cy: cy - 8, rx: RX - 110, ry: RY - 80, fill: '#f2e6c8', opacity: 0.9 }, lid);
  for (let k = 0; k < 10; k++) { const a = k / 10 * Math.PI * 2; svg('circle', { cx: cx + Math.cos(a) * (RX - 160), cy: cy - 8 + Math.sin(a) * (RY - 112), r: 14, fill: '#2f4fa0' }, lid); }
  svg('ellipse', { cx: cx - 140, cy: cy - 70, rx: 120, ry: 22, fill: '#ffffff', opacity: 0.28, transform: `rotate(-8 ${cx - 140} ${cy - 70})` }, lid);
  // อาม่า's arm (burgundy silk sleeve with gold flowers, a gold cuff, the jade bangle) and her mitten hand, from the upper right
  const arm = svg('g', {}, M.s);
  const silk = (() => { const id = uidS('sk'), pt = svg('pattern', { id, width: 70, height: 70, patternUnits: 'userSpaceOnUse' }, D); svg('rect', { width: 70, height: 70, fill: '#a82a35' }, pt); for (const [x, y] of [[18, 18], [52, 52]]) { for (let k = 0; k < 5; k++) svg('circle', { cx: x + Math.cos(k * 1.2566) * 8, cy: y + Math.sin(k * 1.2566) * 8, r: 6.5, fill: '#e8b04a', opacity: 0.85 }, pt); svg('circle', { cx: x, cy: y, r: 4, fill: '#c23e48' }, pt); } return `url(#${id})`; })();
  const sleeve = svg('path', { fill: silk, stroke: INK, 'stroke-width': 8, 'stroke-linejoin': 'round' }, arm);
  const cuff = svg('path', { fill: '#e8b04a', stroke: INK, 'stroke-width': 7, 'stroke-linejoin': 'round' }, arm);
  const hand = svg('g', {}, arm);
  const held = svg('g', {}, hand); flatEnv15(held, D, -30, 70, -8, o.heldYear || '2562');
  svg('path', { d: 'M-70,-40 C-90,30 -40,92 20,86 C80,80 96,20 74,-30 C56,-70 -50,-78 -70,-40 Z', fill: '#f0cba8', stroke: INK, 'stroke-width': 8, 'stroke-linejoin': 'round' }, hand);
  svg('path', { d: 'M-66,10 C-110,8 -116,52 -84,62 C-62,68 -48,46 -44,30', fill: '#f0cba8', stroke: INK, 'stroke-width': 8, 'stroke-linejoin': 'round' }, hand);   // the thumb
  svg('path', { d: 'M-20,-40 q22,-12 44,0 M-10,20 q20,8 40,-2', fill: 'none', stroke: '#d6ab86', 'stroke-width': 6, 'stroke-linecap': 'round' }, hand);
  const bangle = svg('ellipse', { rx: 34, ry: 70, fill: 'none', stroke: '#4f9e7a', 'stroke-width': 22 }, arm);
  const bangleH = svg('ellipse', { rx: 34, ry: 70, fill: 'none', stroke: '#bfe8d2', 'stroke-width': 5, opacity: 0.7 }, arm);
  const sh = lightShaft(M.s, D, [[-200, -200], [300, -200], [900, 1900], [200, 1900]], '#fff0c8', 0.16, 1508, 22);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 4, [-100, 1500, 1180, 2000], ['#ff8a5a', '#ffd06a'], 1509, { rMin: 60, rMax: 120, op: 0.28 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 46%, rgba(40,10,6,.55) 100%)';
  const band = html('div', '', S.fx); band.style.cssText = 'position:absolute;left:0;right:0;top:1440px;bottom:0;background:linear-gradient(180deg, rgba(30,10,6,0), rgba(30,10,6,.62) 38%, rgba(30,10,6,.78))';
  // envelope layouts: stacked (as they went in) and fanned (spread by อาม่า's hand)
  const stackAt = i => [cx - 40 + (i % 2 ? 26 : -18) + i * 4, cy + 40 - i * 10, -14 + (i % 3) * 9];
  const fanAt = i => [cx - 214 + i * 61, cy + 26 + Math.abs(i - 3.5) * 9, -24 + i * 7];
  return {
    cx, cy,
    // open 0..1 (lid off to the upper right), n envelopes inside, fan 0..1, arm {x, y, k (0 = away)}, held (an envelope in the hand)
    set({ open = 1, n = 8, fan = 0, arm: A = null, held: hv = false, glint = -1, t = 0 } = {}) {
      lid.setAttribute('transform', `translate(${(open * 520).toFixed(1)},${(-open * 560).toFixed(1)}) rotate(${(open * 18).toFixed(1)} ${cx} ${cy})`);
      lid.setAttribute('display', open > 0.98 ? 'none' : 'inline');
      envs.forEach((e, i) => {
        const a = stackAt(i), b = fanAt(i), k = ease.inOutCubic(clamp(fan * 1.4 - i * 0.05));
        e.g.setAttribute('display', i < n ? 'inline' : 'none');
        e.g.setAttribute('transform', `translate(${lerp(a[0], b[0], k).toFixed(1)},${lerp(a[1], b[1], k).toFixed(1)}) rotate(${lerp(a[2], b[2], k).toFixed(1)})`);
        const gk = glint >= 0 ? Math.sin(Math.PI * clamp((glint - i * 0.12) / 0.4)) : 0, sx = lerp(a[0], b[0], k), sy = lerp(a[1], b[1], k) - 70;
        glints[i].setAttribute('opacity', (i < n ? gk : 0).toFixed(3)); glints[i].setAttribute('transform', `translate(${sx.toFixed(1)},${sy.toFixed(1)}) scale(${(0.6 + 0.6 * gk).toFixed(3)}) rotate(${(t * 90).toFixed(1)})`);
      });
      arm.setAttribute('display', A ? 'inline' : 'none');
      if (A) {
        const hx = A.x, hy = A.y, ux = 0.62, uy = -0.78, nx = -uy, ny = ux, w0 = 110, w1 = 92, L = 1400;
        const wx = hx + ux * 96, wy = hy + uy * 96, ex = wx + ux * L, ey = wy + uy * L;
        sleeve.setAttribute('d', `M${(wx + nx * w1).toFixed(1)},${(wy + ny * w1).toFixed(1)} L${(ex + nx * w0).toFixed(1)},${(ey + ny * w0).toFixed(1)} L${(ex - nx * w0).toFixed(1)},${(ey - ny * w0).toFixed(1)} L${(wx - nx * w1).toFixed(1)},${(wy - ny * w1).toFixed(1)} Z`);
        const c0 = [wx, wy], c1 = [wx + ux * 40, wy + uy * 40];
        cuff.setAttribute('d', `M${(c0[0] + nx * (w1 + 4)).toFixed(1)},${(c0[1] + ny * (w1 + 4)).toFixed(1)} L${(c1[0] + nx * (w1 + 6)).toFixed(1)},${(c1[1] + ny * (w1 + 6)).toFixed(1)} L${(c1[0] - nx * (w1 + 6)).toFixed(1)},${(c1[1] - ny * (w1 + 6)).toFixed(1)} L${(c0[0] - nx * (w1 + 4)).toFixed(1)},${(c0[1] - ny * (w1 + 4)).toFixed(1)} Z`);
        const bx = hx + ux * 70, by = hy + uy * 70, br = `rotate(${(Math.atan2(uy, ux) * 180 / Math.PI).toFixed(1)} ${bx.toFixed(1)} ${by.toFixed(1)})`;
        for (const e of [bangle, bangleH]) setA(e, { cx: bx.toFixed(1), cy: by.toFixed(1), transform: br });
        hand.setAttribute('transform', `translate(${hx.toFixed(1)},${hy.toFixed(1)}) rotate(-30)`);
        held.setAttribute('display', hv ? 'inline' : 'none');
      }
    },
    update(t) { sh(t); if (bok) bok(t); },
  };
}
// the desk at night: an empty envelope lying flat by an open wallet, under the lamp
function deskMacro15(S) {
  const F = S.L.far, M = S.L.mid, D = M.defs;
  svg('rect', { x: -400, y: -400, width: 1900, height: 1400, fill: lin(F.defs, [[0, '#3a2440'], [1, '#5a3a5e']]) }, F.s);
  for (const [x, y, c, rr] of [[200, 260, '#ffd06a', 70], [760, 200, '#ffb0c8', 90], [960, 420, '#fff2c0', 60], [420, 120, '#ffd06a', 50]]) svg('circle', { cx: x, cy: y, r: rr, fill: rad2(F.defs, [[0, c, 0.7], [1, c, 0]]) }, F.s);
  svg('path', { d: 'M-400,700 L1480,640 L1480,2200 L-400,2200 Z', fill: lin(D, [[0, '#8a5a3a'], [1, '#4a2a1e']]) }, M.s);
  for (let k = 0; k < 7; k++) svg('path', { d: `M-400,${820 + k * 190} Q540,${790 + k * 190} 1480,${800 + k * 190}`, fill: 'none', stroke: '#5a3424', 'stroke-width': 4, opacity: 0.5 }, M.s);
  lightPool(M.s, D, 640, 1000, 720, 460, '#ffc878', 0.5);
  const env = svg('g', {}, M.s); flatEnv15(env, D, 0, 0, 0, null, { flat: true });
  env.setAttribute('transform', 'translate(380,1120) scale(1.5) rotate(-10)');
  const w = svg('g', { transform: 'translate(760,1180) scale(1,0.55) rotate(14)' }, M.s);   // the open wallet: an empty note slot, two coins
  svg('rect', { x: -230, y: -150, width: 460, height: 300, rx: 30, fill: '#6a3a24', stroke: INK, 'stroke-width': 8 }, w);
  svg('rect', { x: -210, y: -130, width: 200, height: 260, rx: 18, fill: '#7e4a30', stroke: '#4a2416', 'stroke-width': 5 }, w);
  svg('rect', { x: 10, y: -130, width: 200, height: 260, rx: 18, fill: '#7e4a30', stroke: '#4a2416', 'stroke-width': 5 }, w);
  svg('path', { d: 'M-200,-60 L-20,-60 M30,-60 L200,-60', stroke: '#4a2416', 'stroke-width': 5 }, w);
  for (const [x, y] of [[960, 1320], [1010, 1290]]) { svg('ellipse', { cx: x, cy: y, rx: 40, ry: 22, fill: '#d8c070', stroke: INK, 'stroke-width': 5 }, M.s); svg('ellipse', { cx: x, cy: y - 3, rx: 26, ry: 13, fill: 'none', stroke: '#a8903a', 'stroke-width': 3 }, M.s); }
  const motes = lightShaft(M.s, D, [[300, -200], [800, -200], [1100, 1900], [200, 1900]], '#ffd890', 0.1, 1510, 18);
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 55%, rgba(0,0,0,0) 40%, rgba(16,6,20,.7) 100%)';
  return { update(t) { motes(t); } };
}
