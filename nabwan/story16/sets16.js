// "50 กุหลาบ" sets: ตาบุญ and ยายแก้ว's old house (butter-yellow walls with a tiny sprig print over walnut panelling,
// a big window with louvred shutters onto a garden of bougainvillea and frangipani, their wedding photo, the calendar,
// a low cabinet with a radio and an orchid, a ceiling fan, a hanging fern, the old dog on a dark floral rug) by morning,
// 49 years ago (sepia) and at night (moon in the window, a table lamp); the market flower stall at dawn (striped awning,
// bare bulbs, buckets of roses and marigolds, jasmine garlands, wet concrete); and a macro world for the album of
// pressed roses (pages that turn, two hands, a pen that writes). Every set returns { people, front, shadowL, top,
// ground, light, update(t), ... }.

function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': o.font || 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}
const SEAT16 = 1206, TBL16 = { x: 540, top: 1112 }, YAIX = 360, TAX = 722;
const HAND_YAI = 'Charm', HAND_TA = 'Itim';

// the garden through the window (far layer): sky, frangipani, bougainvillea over a fence; night = moon and fireflies
function garden16(F, mode) {
  const night = mode === 'night', then = mode === 'then';
  svg('rect', { x: -400, y: -400, width: 1300, height: 1800, fill: lin(F.defs, night ? [[0, '#141a3a'], [0.7, '#2a2a52'], [1, '#3a2e4a']] : [[0, '#9fd0ee'], [0.6, '#dcefe8'], [1, '#f8e6c0']]) }, F.s);
  const stars = [], flies = [];
  if (night) {
    const r = rng(1601);
    for (let i = 0; i < 24; i++) stars.push(svg('circle', { cx: -40 + r() * 400, cy: 300 + r() * 300, r: 1 + r() * 1.6, fill: '#fff' }, F.s));
    svg('circle', { cx: 250, cy: 420, r: 70, fill: rad2(F.defs, [[0, '#fff2d0', 0.5], [1, '#fff2d0', 0]]) }, F.s);
    svg('circle', { cx: 250, cy: 420, r: 28, fill: '#f8eed4' }, F.s);
  } else for (const [x, y, s] of [[60, 420, 1], [300, 380, 0.8]]) { const c = svg('g', { transform: `translate(${x},${y}) scale(${s})`, opacity: 0.9 }, F.s); for (const [dx, rr] of [[0, 34], [40, 44], [84, 32]]) svg('circle', { cx: dx, cy: 0, r: rr, fill: '#ffffff' }, c); }
  const leaf = night ? '#24402e' : then ? '#7aa04a' : '#5a9a4a', leaf2 = night ? '#2e4a34' : '#7ab85a';
  svg('path', { d: 'M150,1330 L170,700 L196,700 L210,1330 Z', fill: night ? '#2a2420' : '#7a5a42' }, F.s);   // the frangipani
  for (const [x, y, r] of [[100, 640, 110], [240, 600, 120], [170, 700, 100]]) svg('circle', { cx: x, cy: y, r, fill: leaf }, F.s);
  for (const [x, y] of [[90, 600], [140, 560], [250, 560], [290, 620], [200, 650], [60, 680]]) { const g = svg('g', { transform: `translate(${x},${y})` }, F.s); for (let k = 0; k < 5; k++) svg('ellipse', { cx: Math.cos(k * 1.2566) * 9, cy: Math.sin(k * 1.2566) * 9, rx: 9, ry: 5, fill: night ? '#c8c0b0' : '#fbf7ef', transform: `rotate(${k * 72} ${Math.cos(k * 1.2566) * 9} ${Math.sin(k * 1.2566) * 9})` }, g); svg('circle', { r: 4, fill: '#f2c14e' }, g); }
  svg('rect', { x: -400, y: 900, width: 1300, height: 30, fill: night ? '#3a3040' : '#e8dcc8' }, F.s);   // the fence
  for (let x = -380; x < 900; x += 36) svg('rect', { x, y: 860, width: 18, height: 120, rx: 4, fill: night ? '#3a3040' : '#efe4d0' }, F.s);
  const bougainvillea = night ? '#6a3a5a' : '#e0508a';
  for (let i = 0; i < 26; i++) { const x = -60 + (i * 53) % 420, y = 780 + ((i * 37) % 120); svg('circle', { cx: x, cy: y, r: 22 + (i % 3) * 6, fill: i % 4 === 0 ? leaf2 : bougainvillea, opacity: 0.95 }, F.s); }
  svg('rect', { x: -400, y: 980, width: 1300, height: 400, fill: night ? '#1e2a24' : '#7aa85a' }, F.s);
  if (night) { const r = rng(1602); for (let i = 0; i < 10; i++) flies.push({ x: r() * 360, y: 700 + r() * 300, ph: r() * 6, el: svg('circle', { r: 3, fill: '#f8f0a0' }, F.s) }); }
  return t => {
    stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i)).toFixed(2)));
    flies.forEach(f => setA(f.el, { cx: (f.x + Math.sin(t * 0.7 + f.ph) * 30).toFixed(1), cy: (f.y + Math.cos(t * 0.9 + f.ph) * 20).toFixed(1), opacity: (0.4 + 0.6 * Math.max(0, Math.sin(t * 3 + f.ph))).toFixed(2) }));
  };
}
// a rattan armchair facing right (seat top at y)
function rattanChair16(g, x, y) {
  const c = svg('g', {}, g), cane = '#c8965a', dark = '#9a6a3a';
  svg('path', { d: `M${x - 70},${y + 6} Q${x - 96},${y - 120} ${x - 60},${y - 190} Q${x - 40},${y - 210} ${x - 26},${y - 180} Q${x - 50},${y - 100} ${x - 40},${y + 6} Z`, fill: cane, stroke: INK, 'stroke-width': 4 }, c);
  for (let k = 0; k < 5; k++) svg('path', { d: `M${x - 80 + k * 6},${y - 30 - k * 30} q20,-4 34,6`, fill: 'none', stroke: dark, 'stroke-width': 3, opacity: 0.6 }, c);
  svg('rect', { x: x - 76, y, width: 150, height: 18, rx: 8, fill: cane, stroke: INK, 'stroke-width': 4 }, c);
  svg('path', { d: `M${x - 66},${y + 18} Q${x - 80},${y + 70} ${x - 70},1330 M${x + 62},${y + 18} Q${x + 76},${y + 70} ${x + 66},1330`, fill: 'none', stroke: dark, 'stroke-width': 9, 'stroke-linecap': 'round' }, c);
  svg('path', { d: `M${x - 70},${y + 70} Q${x},${y + 90} ${x + 70},${y + 70}`, fill: 'none', stroke: dark, 'stroke-width': 6 }, c);
  svg('rect', { x: x - 64, y: y - 14, width: 120, height: 18, rx: 9, fill: '#c8443a', stroke: INK, 'stroke-width': 3 }, c);   // the cushion
  return c;
}
// a plain wooden chair facing left (seat top at y)
function woodChair16(g, x, y) {
  const c = svg('g', {}, g);
  svg('path', { d: `M${x + 54},${y + 4} L${x + 66},${y - 150} L${x + 82},${y - 150} L${x + 70},${y + 8} Z`, fill: '#6a3a24', stroke: INK, 'stroke-width': 4 }, c);
  svg('rect', { x: x + 60, y: y - 150, width: 24, height: 40, fill: '#7a4a2a', stroke: INK, 'stroke-width': 3 }, c);
  svg('rect', { x: x - 60, y, width: 140, height: 16, rx: 4, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, c);
  svg('path', { d: `M${x - 50},${y + 16} L${x - 54},1330 M${x + 64},${y + 16} L${x + 68},1330`, stroke: '#5a3020', 'stroke-width': 9, 'stroke-linecap': 'round' }, c);
  return c;
}
// a small square side table in profile (top at y)
function sideTable16(g, defs, x, y, then) {
  const t = svg('g', {}, g);
  svg('rect', { x: x - 116, y, width: 232, height: 20, rx: 4, fill: then ? '#9a6238' : '#8a5230', stroke: INK, 'stroke-width': 4 }, t);
  svg('rect', { x: x - 106, y: y + 20, width: 212, height: 34, fill: '#6a3a22', stroke: INK, 'stroke-width': 3 }, t);
  svg('circle', { cx: x, cy: y + 37, r: 6, fill: '#e8b04a', stroke: INK, 'stroke-width': 2 }, t);
  svg('path', { d: `M${x - 100},${y + 54} L${x - 104},1330 M${x + 100},${y + 54} L${x + 104},1330`, stroke: '#5a3020', 'stroke-width': 10, 'stroke-linecap': 'round' }, t);
  return t;
}
// sticky notes around the room (she forgets, he labels): n of them shown; the newest pops in
const NOTES16 = [
  { x: 690, y: 960, r: -6, c: '#fff1a0', t: ['กุญแจ', 'อยู่ลิ้นชักนี้'] },
  { x: 540, y: 410, r: 5, c: '#ffc8d8', t: ['ตาบุญ', 'สามียายแก้ว ♥'] },
  { x: 930, y: 640, r: -4, c: '#c8f0d0', t: ['ห้องน้ำ', '→'] },
  { x: 760, y: 470, r: 7, c: '#fff1a0', t: ['กินยา', 'เช้า-เย็น'] },
  { x: 240, y: 880, r: -8, c: '#ffd8a8', t: ['อย่าออกไป', 'คนเดียวนะ'] },
  { x: 830, y: 1020, r: 4, c: '#ffc8d8', t: ['หลาน', 'ชื่อ "ฝน"'] },
];
function house16(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1330, mode = o.mode || 'now', then = mode === 'then', night = mode === 'night', D = M.defs;
  const gd = garden16(F, mode);
  const WX0 = 40, WX1 = 330, WY0 = 320, WY1 = 830, DX0 = 900, DX1 = 1050;
  // walls: butter-yellow with a tiny sprig print over walnut panelling; the window hole
  const id = uidS('wp'), pt = svg('pattern', { id, width: 60, height: 60, patternUnits: 'userSpaceOnUse' }, D);
  svg('rect', { width: 60, height: 60, fill: night ? '#c8a868' : '#f2d79a' }, pt);
  for (const [x, y] of [[15, 15], [45, 45]]) { svg('path', { d: `M${x},${y + 6} q-4,-8 0,-14 q4,6 0,14`, fill: night ? '#a08a52' : '#d8b870', opacity: 0.8 }, pt); svg('circle', { cx: x + 4, cy: y - 6, r: 2.6, fill: night ? '#b08a6a' : '#e8a8a0' }, pt); }
  svg('path', { d: `M-400,-400 L1500,-400 L1500,${G} L-400,${G} Z M${WX0},${WY0} L${WX1},${WY0} L${WX1},${WY1} L${WX0},${WY1} Z`, fill: `url(#${id})`, 'fill-rule': 'evenodd' }, M.s);
  svg('rect', { x: -400, y: 900, width: 1900, height: G - 900, fill: night ? '#3a2018' : '#5a3424' }, M.s);
  svg('rect', { x: -400, y: 892, width: 1900, height: 14, fill: night ? '#4a2a1e' : '#7a4a2e', stroke: INK, 'stroke-width': 2 }, M.s);
  for (let x = -380; x < 1500; x += 110) svg('rect', { x, y: 930, width: 86, height: 360, rx: 4, fill: 'none', stroke: night ? '#2a160e' : '#46281a', 'stroke-width': 4 }, M.s);
  // the window: frame, mullion, open louvred shutters, a lace half-curtain, a sill with a jar of water
  svg('rect', { x: WX0 - 12, y: WY0 - 12, width: WX1 - WX0 + 24, height: WY1 - WY0 + 24, fill: 'none', stroke: '#6a3a24', 'stroke-width': 18 }, M.s);
  svg('rect', { x: (WX0 + WX1) / 2 - 5, y: WY0, width: 10, height: WY1 - WY0, fill: '#6a3a24' }, M.s);
  for (const [x, sg] of [[WX0 - 12, -1], [WX1 + 12, 1]]) { svg('path', { d: `M${x},${WY0 - 10} L${x + sg * 74},${WY0 + 8} L${x + sg * 74},${WY1 - 8} L${x},${WY1 + 10} Z`, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, M.s); for (let k = 0; k < 9; k++) svg('path', { d: `M${x + sg * 8},${WY0 + 26 + k * 54} L${x + sg * 66},${WY0 + 36 + k * 54}`, stroke: '#5a3020', 'stroke-width': 5 }, M.s); }
  const lace = svg('path', { d: `M${WX0},${WY0 + 180} L${WX1},${WY0 + 180} L${WX1},${WY0 + 300} Q${(WX0 + WX1) / 2},${WY0 + 330} ${WX0},${WY0 + 300} Z`, fill: night ? '#c8a888' : '#fbf7ef', opacity: night ? 0.16 : 0.55 }, M.s);
  svg('rect', { x: WX0 - 30, y: WY1 + 8, width: WX1 - WX0 + 60, height: 18, rx: 5, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, M.s);
  // the wedding photo (black and white) or, back then, a painting of the river
  if (then) { svg('rect', { x: 470, y: 380, width: 150, height: 110, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, M.s); svg('rect', { x: 480, y: 390, width: 130, height: 90, fill: '#b8d0c0' }, M.s); svg('path', { d: 'M480,450 Q540,430 610,456 L610,480 L480,480 Z', fill: '#6a9a8a' }, M.s); }
  else {
    svg('rect', { x: 466, y: 360, width: 150, height: 180, fill: '#c8a050', stroke: INK, 'stroke-width': 4 }, M.s);
    svg('rect', { x: 478, y: 372, width: 126, height: 156, fill: '#e2ddd2' }, M.s);
    svg('circle', { cx: 518, cy: 420, r: 16, fill: '#8a847c' }, M.s); svg('circle', { cx: 564, cy: 424, r: 15, fill: '#8a847c' }, M.s);
    svg('path', { d: 'M494,528 Q518,450 542,528 Z', fill: '#4a4a4a' }, M.s); svg('path', { d: 'M538,528 Q564,452 590,528 Z', fill: '#f4f1ea', stroke: '#8a847c', 'stroke-width': 2 }, M.s);
    svg('path', { d: 'M560,412 q6,-12 14,-4', fill: 'none', stroke: '#f4f1ea', 'stroke-width': 4 }, M.s);
  }
  // the calendar: the date, the year; a red marker circle
  const cal = svg('g', {}, M.s);
  svg('rect', { x: 690, y: 420, width: 140, height: 200, rx: 6, fill: '#fbf7ee', stroke: INK, 'stroke-width': 4 }, cal);
  svg('rect', { x: 690, y: 420, width: 140, height: 48, rx: 6, fill: '#d8486a', stroke: INK, 'stroke-width': 4 }, cal);
  svg('circle', { cx: 760, cy: 414, r: 6, fill: '#3a2a24' }, cal);
  wtext(cal, 760, 453, then ? 'ก.พ. 2521' : 'ก.พ. 2570', 24, '#fff2f4', { w: 600 });
  wtext(cal, 760, 560, '14', 84, '#d8283a', { w: 800 });
  wtext(cal, 760, 604, 'วาเลนไทน์', 22, '#3a2a24', { w: 600 });
  const circ = svg('path', { d: 'M760,488 C808,488 818,532 812,556 C804,590 716,594 708,556 C700,518 726,486 768,494', fill: 'none', stroke: '#e0281e', 'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-dasharray': '420', 'stroke-dashoffset': '420' }, cal);
  const clock = wallClock(M.s, 900, 300, 36, '#7a4a2a'); clock(night ? 22.4 : 7.2);
  // the door on the right (half open onto the hall)
  svg('rect', { x: DX0, y: 330, width: DX1 - DX0, height: G - 330, fill: night ? '#2a1a14' : '#d8b880' }, M.s);
  svg('rect', { x: DX0 - 12, y: 318, width: DX1 - DX0 + 24, height: G - 318, fill: 'none', stroke: '#5a3020', 'stroke-width': 16 }, M.s);
  svg('path', { d: `M${DX0},330 L${DX0 + 56},350 L${DX0 + 56},${G - 20} L${DX0},${G} Z`, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, M.s);
  // the low cabinet: radio, an orchid, framed photos, the albums
  const cab = svg('g', {}, M.s);
  svg('rect', { x: 600, y: 900, width: 260, height: G - 900, fill: '#6a3a22', stroke: INK, 'stroke-width': 4 }, cab);
  svg('rect', { x: 612, y: 950, width: 116, height: 150, fill: '#7a4a2a', stroke: INK, 'stroke-width': 3 }, cab); svg('rect', { x: 734, y: 950, width: 116, height: 150, fill: '#7a4a2a', stroke: INK, 'stroke-width': 3 }, cab);
  svg('rect', { x: 620, y: 840, width: 110, height: 60, rx: 10, fill: then ? '#a87a4a' : '#c89a5a', stroke: INK, 'stroke-width': 3 }, cab); svg('circle', { cx: 646, cy: 870, r: 16, fill: '#5a4030' }, cab); svg('rect', { x: 672, y: 856, width: 46, height: 28, rx: 4, fill: '#f2e2b8' }, cab);
  if (!then) { svg('rect', { x: 760, y: 816, width: 60, height: 84, fill: '#c8a050', stroke: INK, 'stroke-width': 3 }, cab); svg('rect', { x: 766, y: 822, width: 48, height: 64, fill: '#d8c8a8' }, cab); }
  svg('path', { d: 'M842,900 L834,860 L862,860 L854,900 Z', fill: '#e8e2d6', stroke: INK, 'stroke-width': 3 }, cab);
  svg('path', { d: 'M848,860 Q840,800 860,770', fill: 'none', stroke: '#4f8a3e', 'stroke-width': 4 }, cab);
  for (const [x, y] of [[860, 772], [852, 790], [866, 806]]) svg('circle', { cx: x, cy: y, r: 9, fill: '#c88ad8', stroke: INK, 'stroke-width': 2 }, cab);
  const lamp = night ? svg('g', {}, cab) : null;
  if (night) { svg('path', { d: 'M740,900 L740,830', stroke: '#3a2a24', 'stroke-width': 6 }, lamp); svg('path', { d: 'M714,830 L766,830 L756,790 L724,790 Z', fill: '#f2d78a', stroke: INK, 'stroke-width': 3 }, lamp); lightPool(M.s, D, 740, 840, 300, 220, '#ffc878', 0.5); lampCone(M.s, D, 740, 830, 260, 140, '#ffd890', 0.35, false); }
  // the ceiling fan, a hanging fern, plants, the rug, the floor
  const fan = (() => { const f = svg('g', {}, M.s), x = 540, y = 140; svg('rect', { x: x - 4, y: y - 160, width: 8, height: 140, fill: '#6a6460' }, f); svg('ellipse', { cx: x, cy: y, rx: 24, ry: 12, fill: '#e8e2d6', stroke: INK, 'stroke-width': 3 }, f); const bl = [0, 1, 2].map(() => svg('ellipse', { cy: y + 4, ry: 8, fill: '#a87a4a', stroke: INK, 'stroke-width': 2.5 }, f)); return t => bl.forEach((b, i) => { const a = t * 6 + i * 2.094, c = Math.cos(a); setA(b, { cx: (x + c * 80).toFixed(1), rx: (Math.abs(Math.sin(a)) * 60 + 18).toFixed(1), opacity: (0.6 + 0.4 * Math.abs(c)).toFixed(2) }); }); })();
  svg('path', { d: 'M380,0 L380,170', stroke: '#6a5a4a', 'stroke-width': 3 }, M.s);
  svg('path', { d: 'M350,170 L410,170 L400,212 L360,212 Z', fill: '#c8643a', stroke: INK, 'stroke-width': 3 }, M.s);
  for (const [a, l] of [[110, 120], [80, 150], [60, 110], [130, 100], [95, 170]]) svg('path', { d: `M380,190 q${(Math.cos(rad(a)) * l * 0.5).toFixed(1)},20 ${(Math.cos(rad(a)) * l).toFixed(1)},${(Math.sin(rad(a)) * l).toFixed(1)}`, fill: 'none', stroke: then ? '#7aa04a' : '#4f8a3e', 'stroke-width': 7, 'stroke-linecap': 'round' }, M.s);
  pottedPlant(M.s, 110, G, 0.7, 'monstera', '#c8643a');
  svg('rect', { x: -400, y: G, width: 1900, height: 900, fill: lin(D, night ? [[0, '#3a2018'], [1, '#140a06']] : [[0, '#6a4228'], [1, '#2e1a0e']]) }, M.s);
  for (let y = G + 30, k = 0; y < 2200; y += 46 + k * 10, k++) svg('rect', { x: -400, y, width: 1900, height: 3, fill: '#1e0e06', opacity: 0.5 }, M.s);
  svg('ellipse', { cx: 560, cy: 1580, rx: 540, ry: 140, fill: '#6a2232', stroke: '#4a1424', 'stroke-width': 6 }, M.s);
  for (let k = 0; k < 10; k++) { const a = k / 10 * Math.PI * 2; svg('circle', { cx: 560 + Math.cos(a) * 420, cy: 1580 + Math.sin(a) * 100, r: 14, fill: '#a8485a', opacity: 0.7 }, M.s); }
  svg('ellipse', { cx: 560, cy: 1580, rx: 300, ry: 66, fill: 'none', stroke: '#8a3446', 'stroke-width': 5, 'stroke-dasharray': '16 10' }, M.s);
  wallAO(M.s, D, G, { op: 0.3 });
  const dog = then ? null : oldDog16(M.s, 900, 1420, 0.62, '#d9b07a');
  // light: sun through the window (morning), the moon and the lamp (night)
  const shaft = night ? lightShaft(M.s, D, [[WX0 + 10, WY0 + 10], [WX1 - 10, WY0 + 10], [WX1 + 300, 1600], [WX0 + 120, 1600]], '#b8c8ff', 0.08, 1603, 10)
    : lightShaft(M.s, D, [[WX0 + 10, WY0 + 10], [WX1 - 10, WY0 + 10], [WX1 + 520, 1650], [WX0 + 200, 1650]], then ? '#ffd890' : '#fff2c8', then ? 0.26 : 0.22, 1604, 28);
  // the sticky notes
  const notesG = svg('g', {}, M.s), notes = NOTES16.map(n => { const g = svg('g', { opacity: 0 }, notesG); svg('rect', { x: -40, y: -36, width: 80, height: 72, fill: n.c, stroke: '#00000022', 'stroke-width': 1 }, g); svg('path', { d: 'M-40,26 L-40,36 L-28,36', fill: shade(n.c, -12) }, g); n.t.forEach((s, i) => wtext(g, 0, -8 + i * 22, s, i ? 15 : 18, '#2a3a8a', { font: HAND_TA, w: 400 })); return { g, n }; });
  // furniture: her chair, his chair, the side table
  const chairs = svg('g', {}, M.s); rattanChair16(chairs, YAIX - 4, SEAT16); woodChair16(chairs, TAX + 10, SEAT16);
  const shadowL = svg('g', {}, M.s);
  const people = svg('g', {}, M.s);
  const front = svg('g', {}, M.s); sideTable16(front, D, TBL16.x, TBL16.top, then);
  const top = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 360], night ? ['#ffd890', '#b8c8ff'] : ['#fff2c8', '#ffd0a0'], 1605, { rMin: 30, rMax: 80, op: night ? 0.22 : 0.28 });
  const vg = html('div', '', S.fx); vg.style.cssText = `position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 48%, ${night ? 'rgba(10,6,24,.62)' : 'rgba(40,18,6,.48)'} 100%)`;
  return {
    people, front, shadowL, top, ground: G, seat: SEAT16, tableTop: TBL16.top, door: (DX0 + DX1) / 2,
    light: night ? { ux: 0.4, uy: -0.9, lx: 740 } : { ux: -0.75, uy: -0.66, lx: 180 },
    notes(k, t = 0) { notes.forEach((o2, i) => { const on = clamp(k - i); o2.g.setAttribute('opacity', on.toFixed(3)); const s = on > 0 && on < 1 ? 1 + 0.4 * Math.sin(Math.PI * on) : 1; o2.g.setAttribute('transform', `translate(${o2.n.x},${o2.n.y}) rotate(${o2.n.r}) scale(${s.toFixed(3)})`); }); },
    circle(k) { circ.setAttribute('stroke-dashoffset', (420 * (1 - clamp(k))).toFixed(1)); },
    update(t) { gd(t); fan(t); shaft(t); if (dog) dog(t); if (bok) bok(t); lace.setAttribute('transform', `skewX(${(Math.sin(t * 0.8) * 2).toFixed(2)})`); },
  };
}

// the flower stall at the morning market, dawn
function market16(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1330, D = M.defs;
  svg('rect', { x: -400, y: -400, width: 1900, height: 1800, fill: lin(F.defs, [[0, '#3a2a5a'], [0.45, '#c8708a'], [0.75, '#f8b070'], [1, '#ffe0a8']]) }, F.s);
  svg('circle', { cx: 760, cy: 760, r: 160, fill: rad2(F.defs, [[0, '#fff0c0', 0.8], [1, '#fff0c0', 0]]) }, F.s);
  svg('path', { d: 'M640,760 L700,600 L720,560 L740,600 L800,760 Z M690,620 L750,620', fill: '#5a3a4a', opacity: 0.6 }, F.s);   // a chedi far off
  for (let i = 0; i < 6; i++) { const x = -360 + i * 260; svg('path', { d: `M${x},780 L${x + 120},700 L${x + 240},780 L${x + 240},1300 L${x},1300 Z`, fill: i % 2 ? '#4a3048' : '#563a50' }, F.s); }
  svg('path', { d: 'M-400,640 Q300,690 1500,620', fill: 'none', stroke: '#2a1a2a', 'stroke-width': 3 }, F.s);
  const bulbsFar = lightString(F.s, -400, 1500, 820, 30, ['#ffd06a'], 18);
  // the stall: striped awning on poles, bulbs, buckets, garlands, the counter
  const aw = svg('g', {}, M.s);
  for (let k = 0; k < 9; k++) svg('path', { d: `M${300 + k * 90},300 L${390 + k * 90},300 L${396 + k * 90},420 Q${351 + k * 90},440 ${306 + k * 90},420 Z`, fill: k % 2 ? '#fbf7ef' : '#d8343c', stroke: INK, 'stroke-width': 3 }, aw);
  svg('rect', { x: 290, y: 286, width: 830, height: 20, fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, aw);
  for (const x of [320, 1060]) svg('rect', { x: x - 8, y: 300, width: 16, height: G - 300, fill: '#8a6a4a', stroke: INK, 'stroke-width': 3 }, M.s);
  const bulbs = []; for (const x of [440, 640, 840]) { svg('path', { d: `M${x},430 L${x},500`, stroke: '#3a2a24', 'stroke-width': 3 }, M.s); bulbs.push(svg('circle', { cx: x, cy: 512, r: 70, fill: rad2(D, [[0, '#ffd890', 0.7], [1, '#ffd890', 0]]), style: 'mix-blend-mode:screen' }, M.s)); svg('circle', { cx: x, cy: 512, r: 13, fill: '#fff2c0', stroke: INK, 'stroke-width': 2.5 }, M.s); }
  for (let k = 0; k < 7; k++) { const x = 400 + k * 90; svg('path', { d: `M${x},440 L${x},${560 + (k % 2) * 30}`, stroke: '#f6efe2', 'stroke-width': 10, 'stroke-dasharray': '10 4', 'stroke-linecap': 'round' }, M.s); svg('circle', { cx: x, cy: 574 + (k % 2) * 30, r: 9, fill: '#d8343c', stroke: INK, 'stroke-width': 2 }, M.s); }   // jasmine garlands
  // a back shelf of buckets
  const bk = (x, y, col, s = 1) => { const g = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, M.s); for (let k = -3; k <= 3; k++) { const fx = k * 12, fy = -70 - Math.abs(k) * -4 - (k % 2) * 10; svg('path', { d: `M${fx * 0.4},0 L${fx},${fy + 10}`, stroke: '#3f7a46', 'stroke-width': 3 }, g); svg('circle', { cx: fx, cy: fy, r: 13, fill: col, stroke: INK, 'stroke-width': 2.2 }, g); } svg('path', { d: 'M-40,-20 L40,-20 L32,40 L-32,40 Z', fill: '#5a7aa8', stroke: INK, 'stroke-width': 3 }, g); };
  svg('rect', { x: 360, y: 820, width: 720, height: 20, fill: '#7a5a3a', stroke: INK, 'stroke-width': 3 }, M.s);
  [[420, '#d8283a'], [520, '#f08aa8'], [620, '#f2a03a'], [720, '#d8283a'], [820, '#f6efe2'], [920, '#f2c14e'], [1020, '#d8283a']].forEach(([x, c]) => bk(x, 780, c, 0.95));
  // ground
  svg('rect', { x: -400, y: G, width: 1900, height: 900, fill: lin(D, [[0, '#5a4a52'], [1, '#1e161c']]) }, M.s);
  for (const [x, w] of [[200, 160], [620, 220], [980, 140]]) svg('ellipse', { cx: x, cy: G + 140, rx: w, ry: 18, fill: '#8a7a9a', opacity: 0.35 }, M.s);   // puddles catching the sky
  for (const x of [440, 640, 840]) svg('ellipse', { cx: x, cy: G + 140, rx: 30, ry: 6, fill: '#ffe0a0', opacity: 0.45 }, M.s);
  wallAO(M.s, D, G, { op: 0.25 });
  const shadowL = svg('g', {}, M.s);
  const people = svg('g', {}, M.s);
  // the counter (front): wooden, with buckets of roses, a stack of newspaper, a scale, the price card
  const front = svg('g', {}, M.s);
  svg('rect', { x: 500, y: 1080, width: 560, height: 250, fill: '#8a5a32', stroke: INK, 'stroke-width': 5 }, front);
  for (let k = 0; k < 6; k++) svg('rect', { x: 500, y: 1100 + k * 40, width: 560, height: 3, fill: '#6a4224', opacity: 0.6 }, front);
  svg('rect', { x: 490, y: 1066, width: 580, height: 20, rx: 4, fill: '#a87040', stroke: INK, 'stroke-width': 4 }, front);
  for (const [x, c] of [[600, '#d8283a'], [700, '#d8283a'], [800, '#f08aa8'], [900, '#f2c14e']]) { const g = svg('g', { transform: `translate(${x},1066)` }, front); for (let k = -2; k <= 2; k++) { svg('path', { d: `M${k * 4},0 L${k * 14},-70`, stroke: '#3f7a46', 'stroke-width': 3 }, g); svg('path', { d: `M${k * 14 - 10},-72 Q${k * 14},-90 ${k * 14 + 10},-72 Q${k * 14},-62 ${k * 14 - 10},-72 Z`, fill: c, stroke: INK, 'stroke-width': 2.2 }, g); } svg('path', { d: 'M-30,0 L30,0 L26,-30 L-26,-30 Z', fill: '#4a6a98', stroke: INK, 'stroke-width': 3 }, g); }
  svg('rect', { x: 950, y: 1040, width: 80, height: 26, fill: '#e8e2d2', stroke: INK, 'stroke-width': 2.5 }, front);
  const card = svg('g', { transform: 'translate(560,1150) rotate(-4)' }, front); svg('rect', { x: -70, y: -34, width: 140, height: 68, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 3 }, card); wtext(card, 0, -6, 'กุหลาบ', 24, '#d8283a', { w: 700 }); wtext(card, 0, 22, 'ดอกละ 20.-', 20, '#3a2a24', { w: 600 });
  const top = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 6, [-100, -60, 1180, 380], ['#ffd06a', '#ffb0a0', '#fff0c0'], 1606, { rMin: 30, rMax: 80, op: 0.3 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 50%, rgba(30,10,20,.5) 100%)';
  return {
    people, front, shadowL, top, ground: G, counter: 1066, light: { ux: 0.2, uy: -0.98, lx: 640 },
    update(t) { bulbs.forEach((b, i) => b.setAttribute('opacity', (0.85 + 0.15 * Math.sin(t * 7 + i * 2)).toFixed(2))); bulbsFar.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2 + i)).toFixed(2))); if (bok) bok(t); },
  };
}

// ---------------- the album (macro world) ----------------
const ALBUM_NOTES = ['ดอกแรก ♥', 'เขามารับไปดูหนัง', 'ฝนตกทั้งวัน', 'แต่งงานแล้ว!', 'ลูกคนแรก', 'กินข้าวมันไก่', 'เขามาสาย', 'บ้านใหม่', 'น้ำท่วม', 'หลานเกิด', 'ไปทะเล', 'เขาลืมใส่แว่น'];
// draw one page (year i, 1-based) into g: x0..x0+w, y0..y0+h; who = 'yai' (her hand) or 'ta' (his, year 50)
function albumPage16(g, defs, i, x0, y0, w, h, o = {}) {
  g.innerHTML = '';
  svg('rect', { x: x0, y: y0, width: w, height: h, fill: lin(defs, [[0, '#f6ecd6'], [1, '#ead9b8']], 1, 0), stroke: '#b8a07a', 'stroke-width': 3 }, g);
  for (let k = 0; k < 10; k++) svg('rect', { x: x0 + 20 + ((k * 97) % (w - 60)), y: y0 + 20 + ((k * 211) % (h - 60)), width: 30, height: 18, fill: '#d8c098', opacity: 0.18, transform: `rotate(${k * 17})` }, g);   // foxing
  if (i < 1) return;
  const ta = o.ta, font = ta ? HAND_TA : HAND_YAI, ink = ta ? '#1e2a4a' : '#2a3a8a';
  const head = svg('text', { x: x0 + w / 2, y: y0 + 74, 'text-anchor': 'middle', 'font-family': font, 'font-weight': 700, 'font-size': 52, fill: ink }, g); head.textContent = `ปีที่ ${i}`;
  const date = svg('text', { x: x0 + w / 2, y: y0 + 120, 'text-anchor': 'middle', 'font-family': font, 'font-weight': 400, 'font-size': 32, fill: ink, opacity: 0.85 }, g); date.textContent = `14 ก.พ. ${2520 + i}`;
  if (!o.noRose) {
    const rg = svg('g', { transform: `translate(${x0 + w / 2 + 10},${y0 + h * 0.78}) rotate(${-24 + (i % 3) * 10}) scale(2.3)` }, g); rose16(rg, 1, { dry: true });
    for (const [dx, dy, a] of [[-24, -40, -20], [28, -150, 18]]) svg('rect', { x: x0 + w / 2 + dx - 40, y: y0 + h * 0.78 + dy - 12, width: 80, height: 24, fill: '#ffffff', opacity: 0.45, transform: `rotate(${a} ${x0 + w / 2 + dx} ${y0 + h * 0.78 + dy})` }, g);   // clear tape
  }
  if (!ta) { const n = svg('text', { x: x0 + w / 2, y: y0 + h - 34, 'text-anchor': 'middle', 'font-family': font, 'font-size': 30, fill: '#a8343c' }, g); n.textContent = i === 1 ? ALBUM_NOTES[0] : ALBUM_NOTES[1 + (i * 7) % (ALBUM_NOTES.length - 1)]; }
  return { head, date };
}
function albumMacro16(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, D = M.defs, night = o.night;
  svg('rect', { x: -400, y: -400, width: 1900, height: 1400, fill: lin(F.defs, night ? [[0, '#2a1a24'], [1, '#4a2a2a']] : [[0, '#c8a868'], [1, '#7a4a2a']]) }, F.s);
  for (const [x, y, c, rr] of [[180, 220, night ? '#ffc878' : '#fff2c8', 110], [860, 180, '#ffd0a0', 90], [520, 340, '#ffe8b0', 60]]) svg('circle', { cx: x, cy: y, r: rr, fill: rad2(F.defs, [[0, c, 0.7], [1, c, 0]]) }, F.s);
  svg('path', { d: 'M-400,560 L1480,520 L1480,2200 L-400,2200 Z', fill: lin(D, night ? [[0, '#6a3a22'], [1, '#2a140a']] : [[0, '#8a5230'], [1, '#3a1e10']]) }, M.s);
  for (let k = 0; k < 8; k++) svg('path', { d: `M-400,${640 + k * 200} Q540,${620 + k * 200} 1480,${630 + k * 200}`, fill: 'none', stroke: '#4a2814', 'stroke-width': 4, opacity: 0.45 }, M.s);
  lightPool(M.s, D, 540, 960, 760, 480, night ? '#ffc878' : '#fff2d0', night ? 0.45 : 0.32);
  // the album: covers, page stacks, the spine; pages L (fixed) and R (fixed), plus a turning page
  const X0 = 110, X1 = 970, SP = 540, Y0 = 600, Y1 = 1340, W = SP - X0 - 14, H = Y1 - Y0;
  svg('rect', { x: X0 - 26, y: Y0 - 24, width: X1 - X0 + 52, height: H + 52, rx: 14, fill: '#000', opacity: 0.3, filter: blurFilter(D, 14) }, M.s);
  svg('rect', { x: X0 - 22, y: Y0 - 22, width: X1 - X0 + 44, height: H + 44, rx: 12, fill: '#8e2a3c', stroke: INK, 'stroke-width': 6 }, M.s);
  for (let k = 0; k < 4; k++) { svg('rect', { x: X0 - 10 + k * 2, y: Y0 - 10 + k * 2, width: SP - X0 + 6 - k * 2, height: H + 14 - k * 2, fill: '#efe2c4', stroke: '#c8b48a', 'stroke-width': 2 }, M.s); svg('rect', { x: SP + 4, y: Y0 - 10 + k * 2, width: X1 - SP + 6 - k * 2, height: H + 14 - k * 2, fill: '#efe2c4', stroke: '#c8b48a', 'stroke-width': 2 }, M.s); }
  const pL = svg('g', {}, M.s), pR = svg('g', {}, M.s);
  svg('rect', { x: SP - 14, y: Y0 - 8, width: 28, height: H + 16, fill: lin(D, [[0, '#00000000'], [0.5, '#0000003a'], [1, '#00000000']], 1, 0) }, M.s);
  const turnG = svg('g', {}, M.s), turnF = svg('g', {}, turnG), turnB = svg('g', {}, turnG), turnShade = svg('rect', { x: SP, y: Y0, width: W, height: H, fill: '#000', opacity: 0 }, turnG);
  const glow = svg('g', { opacity: 0 }, M.s); svg('rect', { x: X0, y: Y0, width: X1 - X0, height: H, fill: rad2(D, [[0, '#fff6c0', 0.4], [1, '#fff6c0', 0]]) }, glow);
  // hands: her floral sleeve from the bottom left; his knit cuff from the right, holding a pen
  const mkArm = (pat, skin) => { const a = svg('g', {}, M.s), sl = svg('path', { fill: pat, stroke: INK, 'stroke-width': 8, 'stroke-linejoin': 'round' }, a), hd = svg('g', {}, a); svg('path', { d: 'M-70,-40 C-90,30 -40,92 20,86 C80,80 96,20 74,-30 C56,-70 -50,-78 -70,-40 Z', fill: skin, stroke: INK, 'stroke-width': 8 }, hd); svg('path', { d: 'M-66,10 C-110,8 -116,52 -84,62 C-62,68 -48,46 -44,30', fill: skin, stroke: INK, 'stroke-width': 8 }, hd); return { a, sl, hd }; };
  const floral = (() => { const id = uidS('fl'), pt = svg('pattern', { id, width: 70, height: 70, patternUnits: 'userSpaceOnUse' }, D); svg('rect', { width: 70, height: 70, fill: '#f6c8a8' }, pt); for (const [x, y] of [[18, 18], [52, 52]]) { for (let k = 0; k < 5; k++) svg('circle', { cx: x + Math.cos(k * 1.2566) * 7, cy: y + Math.sin(k * 1.2566) * 7, r: 5.5, fill: '#7fb069' }, pt); svg('circle', { cx: x, cy: y, r: 3.5, fill: '#fde0c8' }, pt); } return `url(#${id})`; })();
  const knit = (() => { const id = uidS('kn'), pt = svg('pattern', { id, width: 40, height: 22, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(38)' }, D); svg('rect', { width: 40, height: 22, fill: '#efe2c8' }, pt); svg('rect', { y: 13, width: 40, height: 7, fill: '#b0603a' }, pt); return `url(#${id})`; })();   // his striped shirt sleeve
  const yaiH = mkArm(o.young ? (() => { const id = uidS('fy'), pt = svg('pattern', { id, width: 70, height: 70, patternUnits: 'userSpaceOnUse' }, D); svg('rect', { width: 70, height: 70, fill: '#f08aa8' }, pt); for (const [x, y] of [[18, 18], [52, 52]]) for (let k = 0; k < 5; k++) svg('circle', { cx: x + Math.cos(k * 1.2566) * 7, cy: y + Math.sin(k * 1.2566) * 7, r: 5.5, fill: '#ffffff' }, pt); return `url(#${id})`; })() : floral, '#e2b08a'), taH = mkArm(knit, '#c99068');
  const pen = svg('g', {}, taH.hd); svg('path', { d: 'M-10,40 L-80,150', stroke: INK, 'stroke-width': 14, 'stroke-linecap': 'round' }, pen); svg('path', { d: 'M-10,40 L-80,150', stroke: '#2f4fa0', 'stroke-width': 8, 'stroke-linecap': 'round' }, pen); taH.hd.insertBefore(pen, taH.hd.firstChild);
  const held = svg('g', {}, taH.hd); taH.hd.insertBefore(held, taH.hd.firstChild); const hr = svg('g', { transform: 'translate(-40,60) rotate(-150) scale(2.2)' }, held); rose16(hr, 1, {});
  const place = (A, hx, hy, ux, uy) => { if (!hx && hx !== 0) { A.a.setAttribute('display', 'none'); return; } A.a.setAttribute('display', 'inline'); const nx = -uy, ny = ux, w = 92, wx = hx + ux * 90, wy = hy + uy * 90, ex = wx + ux * 1400, ey = wy + uy * 1400; A.sl.setAttribute('d', `M${(wx + nx * w).toFixed(1)},${(wy + ny * w).toFixed(1)} L${(ex + nx * (w + 18)).toFixed(1)},${(ey + ny * (w + 18)).toFixed(1)} L${(ex - nx * (w + 18)).toFixed(1)},${(ey - ny * (w + 18)).toFixed(1)} L${(wx - nx * w).toFixed(1)},${(wy - ny * w).toFixed(1)} Z`); A.hd.setAttribute('transform', `translate(${hx.toFixed(1)},${hy.toFixed(1)}) rotate(${(Math.atan2(uy, ux) * 180 / Math.PI - 130).toFixed(1)})`); };
  const sh = lightShaft(M.s, D, [[-200, -200], [300, -200], [900, 1900], [200, 1900]], night ? '#ffd890' : '#fff0c8', 0.12, 1607, 18);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 4, [-100, 1500, 1180, 2000], ['#ffd890', '#ffb0a0'], 1608, { rMin: 60, rMax: 120, op: 0.26 });
  const vg = html('div', '', S.fx); vg.style.cssText = `position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 46%, ${night ? 'rgba(14,6,18,.66)' : 'rgba(40,14,6,.5)'} 100%)`;
  const band = html('div', '', S.fx); band.style.cssText = 'position:absolute;left:0;right:0;top:1440px;bottom:0;background:linear-gradient(180deg, rgba(20,8,6,0), rgba(20,8,6,.62) 38%, rgba(20,8,6,.78))';
  let shownL = -1, shownR = -1, shownT = -2, last = null;
  return {
    // spread: the year on the left page (right page = year + 1); turn 0..1 flips the right page over to the left;
    // yai / ta: hand positions {x, y} or null; write 0..1 reveals the last page's handwriting; rose: the 50th rose placed
    set({ year = 1, turn = 0, yai = null, ta = null, write = -1, rose = 0, glowK = 0, t = 0 } = {}) {
      const L50 = year >= 50;
      if (shownL !== year) { last = albumPage16(pL, D, year, X0, Y0, W, H, { ta: year === 50, noRose: year === 50 }); shownL = year; }   // his rose goes on fresh }
      const rY = year + 1 <= 50 ? year + 1 : 0;
      if (shownR !== rY) { albumPage16(pR, D, rY > 0 && rY < 50 ? rY : 0, SP + 14, Y0, W, H); shownR = rY; }
      if (turn > 0 && turn < 1) {
        if (shownT !== year) { albumPage16(turnF, D, year + 1 < 50 ? year + 1 : 0, SP + 14, Y0, W, H); albumPage16(turnB, D, 0, SP + 14, Y0, W, H); shownT = year; }
        const sx = Math.cos(Math.PI * turn);
        turnG.setAttribute('display', 'inline'); turnG.setAttribute('transform', `translate(${SP},0) scale(${sx.toFixed(4)},1) translate(${-SP},0)`);
        turnF.setAttribute('display', sx > 0 ? 'inline' : 'none'); turnB.setAttribute('display', sx > 0 ? 'none' : 'inline');
        turnShade.setAttribute('opacity', (0.25 * Math.sin(Math.PI * turn)).toFixed(3));
      } else turnG.setAttribute('display', 'none');
      if (year === 50 && last) {   // his page: the rose goes down, then the words appear as he writes
        const w = clamp(write);
        if (!last.msg) { last.msg = [svg('text', { x: X0 + W / 2, y: Y0 + H - 150, 'text-anchor': 'middle', 'font-family': HAND_TA, 'font-size': 36, fill: '#1e2a4a' }, pL), svg('text', { x: X0 + W / 2, y: Y0 + H - 100, 'text-anchor': 'middle', 'font-family': HAND_TA, 'font-size': 36, fill: '#1e2a4a' }, pL)]; last.msg[0].textContent = 'เธอจำไม่ได้ ไม่เป็นไรนะ'; last.msg[1].textContent = 'ฉันจำแทนเธอเอง ♥'; const cid = uidS('cw'); const cp = svg('clipPath', { id: cid }, D); last.clip = svg('rect', { x: X0, y: Y0 + H - 200, width: 0, height: 130 }, cp); last.msg.forEach(m => m.setAttribute('clip-path', `url(#${cid})`)); last.clip2 = svg('rect', { x: X0, y: Y0 + H - 130, width: 0, height: 60 }, cp); }
        last.clip.setAttribute('width', (W * clamp(w * 2)).toFixed(1)); last.clip.setAttribute('height', '66'); last.clip2.setAttribute('width', (W * clamp(w * 2 - 1)).toFixed(1));
        held.setAttribute('display', rose < 1 ? 'inline' : 'none');
        if (rose >= 1 && !last.roseDown) { const rg = svg('g', { transform: `translate(${X0 + W / 2 + 10},${Y0 + H * 0.62}) rotate(-24) scale(2.3)` }, pL); rose16(rg, 1, {}); last.roseDown = true; }
      } else held.setAttribute('display', 'none');
      glow.setAttribute('opacity', clamp(glowK).toFixed(3));
      place(yaiH, yai ? yai.x : null, yai ? yai.y : 0, -0.55, 0.83);
      place(taH, ta ? ta.x : null, ta ? ta.y : 0, 0.62, 0.78);
      pen.setAttribute('display', year === 50 && rose >= 1 ? 'inline' : 'none');
      if (ta && year === 50 && rose >= 1) pen.setAttribute('transform', `translate(${(Math.sin(t * 18) * 4).toFixed(1)},${(Math.cos(t * 23) * 3).toFixed(1)})`);
    },
    spine: SP, X0, X1, Y0, Y1, W, H,
    update(t) { sh(t); if (bok) bok(t); },
  };
}
