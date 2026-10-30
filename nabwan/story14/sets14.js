// "720 มื้อ" sets: the old wooden classroom of a rural school twenty years ago (honey-teak planks, a green chalkboard with
// the class written in chalk, sage shutters open on the schoolyard with its rain tree and flagpole, ceiling fans, the ก-ฮ
// chart, the school motto, a broom, sun shafts full of dust), and the classroom today on Teacher's Day (peach walls with a
// terracotta dado, a whiteboard, a TV, the class's drawings, bunting, a พานพุ่ม of marigolds on the teacher's desk, steel
// desks and blue chairs, a newer school building outside). The boy and the girl both sit at the back desk.
// Every set returns { people, front, shadowL, top, ground, light, update(t), ... }.

function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}
const DESK14 = [430, 700, 970];   // desk-row x (students face left, toward the board)
const BENCH14 = 1206;             // seat top
// the schoolyard through the windows (far layer): sky, the rain tree, the flagpole with a waving flag, kids playing far off
function schoolyard14(F, mode, o = {}) {
  const now = mode === 'now';
  svg('rect', { x: -400, y: -200, width: 1900, height: 1300, fill: lin(F.defs, now ? [[0, '#8fc8f0'], [0.6, '#cfe8f4'], [1, '#f8e8c8']] : [[0, '#f4c88a'], [0.6, '#fbe0a8'], [1, '#fff0c8']]) }, F.s);
  for (const [x, y, s] of [[120, 260, 1], [700, 200, 0.8], [1100, 300, 1.1]]) { const c = svg('g', { transform: `translate(${x},${y}) scale(${s})`, opacity: 0.85 }, F.s); for (const [dx, r] of [[0, 40], [44, 52], [96, 38]]) svg('circle', { cx: dx, cy: 0, r, fill: '#ffffff' }, c); }
  if (now) {   // a newer building
    svg('rect', { x: 560, y: 520, width: 700, height: 360, fill: '#f6e6c8', stroke: INK, 'stroke-width': 4 }, F.s);
    svg('path', { d: 'M540,522 L1280,522 L1240,470 L580,470 Z', fill: '#d0643a', stroke: INK, 'stroke-width': 4 }, F.s);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 6; c++) svg('rect', { x: 590 + c * 110, y: 550 + r * 105, width: 70, height: 60, fill: '#8fb8d8', stroke: '#e8d8b8', 'stroke-width': 5 }, F.s);
  }
  svg('rect', { x: -400, y: 880, width: 1900, height: 400, fill: lin(F.defs, [[0, now ? '#8cc46a' : '#a8c86a'], [1, now ? '#5a9a4a' : '#7aa04a']]) }, F.s);
  // the rain tree
  const tree = svg('g', {}, F.s);
  svg('path', { d: 'M180,900 L196,700 L230,700 L246,900 Z', fill: '#6a4a32' }, tree);
  for (const [x, y, r] of [[120, 640, 120], [240, 600, 140], [360, 650, 110], [210, 700, 120]]) svg('circle', { cx: x, cy: y, r, fill: now ? '#5a9a4a' : '#7aa04a', opacity: 0.95 }, tree);
  for (const [x, y, r] of [[160, 610, 60], [280, 570, 60]]) svg('circle', { cx: x, cy: y, r, fill: now ? '#7ab85a' : '#9ac05a', opacity: 0.8 }, tree);
  // flagpole and the Thai flag
  svg('rect', { x: 930, y: 420, width: 8, height: 470, fill: '#d8d2c4' }, F.s);
  const flag = svg('g', {}, F.s);
  const stripes = ['#e0453b', '#fbf7ef', '#2f3f8a', '#fbf7ef', '#e0453b'], hs = [12, 12, 24, 12, 12];
  let y0 = 424; const flagP = stripes.map((c, i) => { const p = svg('path', { fill: c }, flag); const yy = y0; y0 += hs[i]; return [p, yy, hs[i]]; });
  // kids playing far off
  const kids = svg('g', { opacity: 0.75 }, F.s), r = rng(1401);
  const kd = Array.from({ length: 7 }, () => ({ x: 400 + r() * 900, ph: r() * 6, sp: 30 + r() * 50, c: r() > 0.5 ? '#fbf9f4' : '#f2c14e' }));
  const kEl = kd.map(k => { const g = svg('g', {}, kids); svg('circle', { cx: 0, cy: -34, r: 9, fill: '#3a2a24' }, g); svg('rect', { x: -8, y: -26, width: 16, height: 18, rx: 4, fill: k.c }, g); svg('rect', { x: -7, y: -8, width: 14, height: 10, fill: '#2a3a6e' }, g); return g; });
  return t => {
    flagP.forEach(([p, yy, h]) => { let d = `M938,${yy}`; for (let x = 0; x <= 120; x += 10) d += ` L${938 + x},${(yy + Math.sin(t * 5 - x * 0.06) * x * 0.06).toFixed(1)}`; for (let x = 120; x >= 0; x -= 10) d += ` L${938 + x},${(yy + h + Math.sin(t * 5 - x * 0.06) * x * 0.06).toFixed(1)}`; p.setAttribute('d', d + ' Z'); });
    kd.forEach((k, i) => { const x = 380 + ((k.x + t * k.sp) % 980); kEl[i].setAttribute('transform', `translate(${x.toFixed(1)},${(900 - Math.abs(Math.sin(t * 6 + k.ph)) * 12).toFixed(1)})`); });
  };
}
// a ceiling fan (front view, blades as a blur ellipse); returns update(t)
function ceilFan14(g, x, y) {
  const f = svg('g', {}, g);
  svg('rect', { x: x - 4, y: y - 120, width: 8, height: 100, fill: '#6a6460' }, f);
  svg('ellipse', { cx: x, cy: y, rx: 26, ry: 14, fill: '#e8e2d6', stroke: INK, 'stroke-width': 3 }, f);
  const bl = [0, 1, 2].map(() => svg('ellipse', { cy: y + 4, ry: 8, fill: '#c9b89a', stroke: INK, 'stroke-width': 2.5 }, f));
  return t => bl.forEach((b, i) => { const a = t * 18 + i * 2.094, c = Math.cos(a); setA(b, { cx: (x + c * 80).toFixed(1), rx: (Math.abs(Math.sin(a)) * 60 + 18).toFixed(1), opacity: (0.6 + 0.4 * Math.abs(c)).toFixed(2) }); });
}
// a two-seat school desk in profile (students face left): top at y; returns the group
function desk14(g, x, now, defs) {
  const d = svg('g', {}, g), top = 1112;
  if (now) {
    svg('rect', { x: x - 120, y: top, width: 150, height: 18, rx: 4, fill: '#e2c08a', stroke: INK, 'stroke-width': 4 }, d);
    svg('path', { d: `M${x - 110},${top + 18} L${x - 110},1330 M${x + 20},${top + 18} L${x + 20},1330 M${x - 110},1240 L${x + 20},1240`, stroke: '#5a6a8a', 'stroke-width': 7 }, d);
    svg('rect', { x: x - 106, y: top + 22, width: 122, height: 44, fill: '#4a5a7a', opacity: 0.7 }, d);   // book shelf
  } else {
    svg('rect', { x: x - 130, y: top, width: 160, height: 22, rx: 3, fill: '#b07a48', stroke: INK, 'stroke-width': 4 }, d);
    svg('rect', { x: x - 124, y: top + 22, width: 148, height: 60, fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, d);
    svg('path', { d: `M${x - 118},${top + 82} L${x - 118},1330 M${x + 18},${top + 82} L${x + 18},1330`, stroke: '#6a4224', 'stroke-width': 10 }, d);
    svg('path', { d: `M${x - 100},${top + 10} l40,0`, stroke: '#7a4a2a', 'stroke-width': 2, opacity: 0.6 }, d);   // carved initials
  }
  return d;
}
function bench14(g, x, now) {
  const b = svg('g', {}, g);
  if (now) {   // a blue plastic chair
    svg('path', { d: `M${x + 40},${BENCH14} L${x + 120},${BENCH14} L${x + 116},${BENCH14 + 16} L${x + 44},${BENCH14 + 16} Z`, fill: '#3f6fb8', stroke: INK, 'stroke-width': 4 }, b);
    svg('path', { d: `M${x + 112},${BENCH14} L${x + 126},${BENCH14 - 110} L${x + 140},${BENCH14 - 110} L${x + 126},${BENCH14 + 6} Z`, fill: '#3f6fb8', stroke: INK, 'stroke-width': 4 }, b);
    svg('path', { d: `M${x + 50},${BENCH14 + 16} L${x + 46},1330 M${x + 110},${BENCH14 + 16} L${x + 116},1330`, stroke: '#5a6a8a', 'stroke-width': 6 }, b);
  } else {
    svg('rect', { x: x + 20, y: BENCH14, width: 130, height: 16, rx: 3, fill: '#a87040', stroke: INK, 'stroke-width': 4 }, b);
    svg('path', { d: `M${x + 30},${BENCH14 + 16} L${x + 30},1330 M${x + 140},${BENCH14 + 16} L${x + 140},1330`, stroke: '#6a4224', 'stroke-width': 9 }, b);
  }
  return b;
}
function classroom14(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1330, now = o.mode === 'now';
  const yard = schoolyard14(F, o.mode);
  // back wall with the door and three windows (holes onto the yard)
  const WIN = [[340, 520], [600, 780], [860, 1040]], WY0 = 420, WY1 = 820, DX0 = 130, DX1 = 270;
  let wall = `M-300,0 L1400,0 L1400,${G} L-300,${G} Z M${DX0},300 L${DX1},300 L${DX1},${G} L${DX0},${G} Z`;
  for (const [a, b] of WIN) wall += ` M${a},${WY0} L${b},${WY0} L${b},${WY1} L${a},${WY1} Z`;
  const wallFill = now ? '#f2c49a' : (() => { const id = uidS('pl'), pt = svg('pattern', { id, width: 200, height: 46, patternUnits: 'userSpaceOnUse' }, M.defs); svg('rect', { width: 200, height: 46, fill: '#b98250' }, pt); svg('path', { d: 'M0,45 L200,45', stroke: '#8a5a32', 'stroke-width': 3 }, pt); svg('path', { d: 'M60,0 L60,46 M150,0 L150,46', stroke: '#9a6a40', 'stroke-width': 1.5, opacity: 0.5 }, pt); return `url(#${id})`; })();
  svg('path', { d: wall, fill: wallFill, 'fill-rule': 'evenodd' }, M.s);
  if (now) { svg('path', { d: `M-300,980 L${DX0},980 L${DX0},${G} L-300,${G} Z M${DX1},980 L1400,980 L1400,${G} L${DX1},${G} Z`, fill: '#e0885a' }, M.s); svg('rect', { x: -300, y: 976, width: 1700, height: 8, fill: '#a85a3a' }, M.s); }
  // window frames: open sage shutters (then) or aluminium sliders (now)
  for (const [a, b] of WIN) {
    if (now) { svg('rect', { x: a - 6, y: WY0 - 6, width: b - a + 12, height: WY1 - WY0 + 12, fill: 'none', stroke: '#d8d8d2', 'stroke-width': 12 }, M.s); svg('rect', { x: (a + b) / 2 - 4, y: WY0, width: 8, height: WY1 - WY0, fill: '#d8d8d2' }, M.s); svg('rect', { x: a, y: WY0, width: b - a, height: WY1 - WY0, fill: '#cfe8f4', opacity: 0.12 }, M.s); }
    else {
      svg('rect', { x: a - 8, y: WY0 - 8, width: b - a + 16, height: WY1 - WY0 + 16, fill: 'none', stroke: '#6a4224', 'stroke-width': 14 }, M.s);
      for (let k = 1; k < 4; k++) svg('rect', { x: a, y: WY0 + k * (WY1 - WY0) / 4 - 3, width: b - a, height: 6, fill: '#6a4224' }, M.s);   // window bars
      for (const [x, sg] of [[a - 8, -1], [b + 8, 1]]) { svg('path', { d: `M${x},${WY0 - 6} L${x + sg * 70},${WY0 + 10} L${x + sg * 70},${WY1 - 10} L${x},${WY1 + 6} Z`, fill: '#6a9a6a', stroke: INK, 'stroke-width': 4 }, M.s); for (let k = 0; k < 6; k++) svg('path', { d: `M${x + sg * 8},${WY0 + 30 + k * 62} L${x + sg * 62},${WY0 + 40 + k * 62}`, stroke: '#4a7a4a', 'stroke-width': 4 }, M.s); }
    }
  }
  // the door (open onto a bright corridor)
  svg('rect', { x: DX0, y: 300, width: DX1 - DX0, height: G - 300, fill: lin(M.defs, [[0, now ? '#fbe8c8' : '#ffe2a8'], [1, now ? '#e8c89a' : '#e8b878']]) }, M.s);
  svg('rect', { x: DX0 - 10, y: 290, width: DX1 - DX0 + 20, height: G - 290, fill: 'none', stroke: now ? '#a85a3a' : '#5a3418', 'stroke-width': 14 }, M.s);
  svg('path', { d: `M${DX1},300 L${DX1 + 60},330 L${DX1 + 60},${G - 20} L${DX1},${G} Z`, fill: now ? '#c88a5a' : '#8a5a32', stroke: INK, 'stroke-width': 4 }, M.s);   // the door leaf, open
  // the board (left), with its class label, the date and a tally
  const BX0 = -160, BX1 = 100, BY0 = 360, BY1 = 780;
  svg('rect', { x: BX0 - 12, y: BY0 - 12, width: BX1 - BX0 + 24, height: BY1 - BY0 + 24, fill: now ? '#c8c8c4' : '#8a5a32', stroke: INK, 'stroke-width': 5 }, M.s);
  svg('rect', { x: BX0, y: BY0, width: BX1 - BX0, height: BY1 - BY0, fill: now ? '#fbfbf8' : '#2f5a44' }, M.s);
  svg('rect', { x: BX0 - 16, y: BY1 + 10, width: BX1 - BX0 + 32, height: 12, fill: now ? '#a8a8a4' : '#6a4224' }, M.s);
  const ink = now ? '#2f4fa8' : '#f4f1e6', chalk = svg('g', { filter: now ? '' : blurFilter(M.defs, 0.5) }, M.s);
  const cls = wtext(chalk, -20, BY0 + 80, now ? 'ป.4/1' : 'ป.4/2', 64, ink, { w: 600 });
  const date = wtext(chalk, -30, BY0 + 150, now ? 'วันศุกร์ 16 ม.ค.' : 'วันพุธ ที่ 14', 34, ink, { w: 500 });
  const extra = wtext(chalk, -30, BY0 + 230, now ? 'สุขสันต์วันครู' : 'เวร: ด.ช.เอก', 34, now ? '#d0643a' : '#f2c14e', { w: 600 });
  const tally = svg('g', {}, chalk);
  const wipe = svg('rect', { x: BX0, y: BY0, width: 0, height: BY1 - BY0, fill: now ? '#ffffff' : '#3a6a52', opacity: 0.9 }, M.s);
  const eraser = svg('g', { display: 'none' }, M.s); svg('rect', { x: -40, y: -16, width: 80, height: 32, rx: 6, fill: '#e8c070', stroke: INK, 'stroke-width': 3 }, eraser); svg('rect', { x: -40, y: 8, width: 80, height: 10, fill: '#5a4a42' }, eraser);
  // wall pieces
  if (now) {
    bunting(M.s, -200, 1250, 330, 22, 22, ['#e0453b', '#f2c14e', '#7fc6a8', '#f08aa8', '#8a5fc8']);
    corkBoard(M.s, 1080, 420, 220, 280, 1402);
    const tv = svg('g', {}, M.s); svg('rect', { x: 560, y: 180, width: 240, height: 140, rx: 10, fill: '#1a1a22', stroke: INK, 'stroke-width': 5 }, tv); svg('rect', { x: 572, y: 192, width: 216, height: 116, rx: 4, fill: '#3a6aa8' }, tv); wtext(tv, 680, 262, 'วันครู', 40, '#ffe9a8', { w: 700 });
    svg('rect', { x: 340, y: 860, width: 700, height: 100, rx: 8, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4 }, M.s);   // the class's drawings
    for (let k = 0; k < 8; k++) { const x = 356 + k * 86; svg('rect', { x, y: 872, width: 72, height: 76, fill: ['#ffd6a8', '#c8e8f8', '#f8d0e0', '#d8f0c8'][k % 4], stroke: INK, 'stroke-width': 2 }, M.s); svg('circle', { cx: x + 36, cy: 900, r: 12, fill: ['#e0453b', '#f2c14e', '#4f9e5e', '#4a7bd8'][k % 4] }, M.s); svg('path', { d: `M${x + 18},${934} l36,0`, stroke: '#3a2a24', 'stroke-width': 3 }, M.s); }
  } else {
    const ch = svg('g', {}, M.s);   // the ก–ฮ chart
    svg('rect', { x: 340, y: 150, width: 300, height: 200, rx: 6, fill: '#fbf2d8', stroke: INK, 'stroke-width': 4 }, ch);
    'กขฃคฅฆงจฉชซฌญฎฏฐ'.split('').forEach((c, i) => wtext(ch, 370 + (i % 8) * 34, 210 + Math.floor(i / 8) * 60, c, 32, ['#c8343c', '#2f5fb8', '#2f8a4a'][i % 3], { w: 600 }));
    const mt = svg('g', {}, M.s); svg('rect', { x: 700, y: 190, width: 330, height: 120, rx: 8, fill: '#8a5a32', stroke: INK, 'stroke-width': 4 }, mt); svg('rect', { x: 712, y: 202, width: 306, height: 96, fill: '#fbf2d8' }, mt); wtext(mt, 865, 266, 'ความรู้คู่คุณธรรม', 38, '#6a3a1e', { w: 700 });
    svg('path', { d: 'M1100,1330 L1130,960', stroke: '#c8a050', 'stroke-width': 8 }, M.s); svg('path', { d: 'M1110,1330 L1150,1330 L1130,1250 Z', fill: '#d8b870', stroke: INK, 'stroke-width': 3 }, M.s);   // broom
  }
  const clock = wallClock(M.s, now ? 460 : 1150, now ? 240 : 230, 40, now ? '#d0643a' : '#8a5a32'); clock(12.1);
  const fans = now ? [] : [ceilFan14(M.s, 420, 140), ceilFan14(M.s, 880, 140)];
  const wf = now ? wallFan(M.s, 1180, 820, 0.8, '#f2c14e') : null;
  // floor
  svg('rect', { x: -300, y: G, width: 1700, height: 900, fill: lin(M.defs, now ? [[0, '#6a4232'], [1, '#2e1a14']] : [[0, '#6a4224'], [1, '#2e1a0e']]) }, M.s);
  for (let y = G + 26, k = 0; y < 2200; y += 40 + k * 9, k++) svg('rect', { x: -300, y, width: 1700, height: 3, fill: '#1e0e06', opacity: 0.5 }, M.s);
  wallAO(M.s, M.defs, G, { op: 0.3 });
  // sun through the windows
  const shafts = WIN.map(([a, b], i) => lightShaft(M.s, M.defs, [[a + 10, WY0 + 10], [b - 10, WY0 + 10], [b - 140, 1500], [a - 260, 1500]], now ? '#fff6dc' : '#ffd890', now ? 0.14 : 0.22, 1410 + i, 14));
  // teacher's desk (front, left of the door) with the พานพุ่ม of marigolds today
  const td = svg('g', {}, M.s);
  svg('rect', { x: -150, y: 1100, width: 250, height: 24, rx: 4, fill: now ? '#c88a5a' : '#8a5a32', stroke: INK, 'stroke-width': 4 }, td);
  svg('rect', { x: -140, y: 1124, width: 230, height: 206, fill: now ? '#b0784a' : '#6a4224', stroke: INK, 'stroke-width': 4 }, td);
  if (now) {
    svg('path', { d: 'M-70,1100 L-30,1100 L-40,1080 L-60,1080 Z', fill: '#e8b13a', stroke: INK, 'stroke-width': 3 }, td);
    svg('path', { d: 'M-50,1082 Q-90,1040 -50,960 Q-10,1040 -50,1082 Z', fill: '#f2a03a', stroke: INK, 'stroke-width': 3 }, td);
    for (let k = 0; k < 9; k++) svg('circle', { cx: -50 + Math.sin(k * 1.7) * (14 - k), cy: 1070 - k * 12, r: 7, fill: k % 3 ? '#f7b82a' : '#fbe9b8' }, td);
    for (let k = 0; k < 3; k++) svg('rect', { x: 10 + k * 26, y: 1062, width: 22, height: 38, rx: 3, fill: ['#e0453b', '#4a7bd8', '#4f9e5e'][k], stroke: INK, 'stroke-width': 2.5 }, td);   // books
  } else {
    svg('rect', { x: -110, y: 1070, width: 70, height: 30, rx: 3, fill: '#e8e0cc', stroke: INK, 'stroke-width': 2.5 }, td);
    svg('circle', { cx: 40, cy: 1086, r: 14, fill: '#f6efe2', stroke: INK, 'stroke-width': 2.5 }, td);
  }
  // benches (behind the students), desks (in front of them)
  const benches = svg('g', {}, M.s); DESK14.forEach(x => bench14(benches, x, now));
  const shadowL = svg('g', {}, M.s);
  const people = svg('g', {}, M.s);
  const front = svg('g', {}, M.s); DESK14.forEach(x => desk14(front, x, now, M.defs));
  const top = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 6, [-100, -60, 1180, 400], now ? ['#fff6dc', '#ffe2a8'] : ['#ffd890', '#fff0c8'], 1412, { rMin: 30, rMax: 80, op: 0.3 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 50%, rgba(30,14,6,.5) 100%)';
  return {
    people, front, shadowL, top, ground: G, seat: BENCH14, deskTop: 1112, door: (DX0 + DX1) / 2,
    light: { ux: 0.55, uy: -0.83, lx: 900 },
    board(o2 = {}) {
      if (o2.cls != null) cls.textContent = o2.cls;
      if (o2.extra != null) extra.textContent = o2.extra;
      const n = o2.tally ?? 0; tally.innerHTML = '';
      for (let i = 0; i < Math.min(n, 30); i++) { const gx = BX0 + 30 + (Math.floor(i / 5) % 6) * 40, gy = BY1 - 90; const k = i % 5; svg('path', { d: k < 4 ? `M${gx + k * 7},${gy} l0,46` : `M${gx - 4},${gy + 34} l34,-22`, stroke: ink, 'stroke-width': 4, 'stroke-linecap': 'round' }, tally); }
      const w = clamp(o2.wipe ?? 0);
      wipe.setAttribute('width', ((BX1 - BX0) * Math.sin(Math.PI * w)).toFixed(1)); wipe.setAttribute('x', (BX0 + (w > 0.5 ? (BX1 - BX0) * (1 - Math.sin(Math.PI * w)) : 0)).toFixed(1));
      eraser.setAttribute('display', w > 0 && w < 1 ? 'inline' : 'none'); eraser.setAttribute('transform', `translate(${(BX0 + (BX1 - BX0) * w).toFixed(1)},${(BY0 + 140 + Math.sin(w * 30) * 60).toFixed(1)})`);
    },
    update(t) { yard(t); fans.forEach(f => f(t)); if (wf) wf(t); shafts.forEach(s => s(t)); if (bok) bok(t); },
  };
}
