// Sets drawn in the reference clip's language: soft gradients, blue-grey sofa, wood floors, lamp glow,
// navy bus terminal, purple tour bus, night highway with lamp parallax.
const uidS = (() => { let n = 0; return p => `${p}${++n}`; })();
function lin(defs, stops, x2 = 0, y2 = 1) {
  const id = uidS('lg');
  const g = svg('linearGradient', { id, x1: 0, y1: 0, x2, y2 }, defs);
  for (const [o, c, a] of stops) svg('stop', { offset: o, 'stop-color': c, 'stop-opacity': a == null ? 1 : a }, g);
  return `url(#${id})`;
}
function rad2(defs, stops, attrs = {}) {
  const id = uidS('rg');
  const g = svg('radialGradient', Object.assign({ id }, attrs), defs);
  for (const [o, c, a] of stops) svg('stop', { offset: o, 'stop-color': c, 'stop-opacity': a == null ? 1 : a }, g);
  return `url(#${id})`;
}
function blurFilter(defs, sd) {
  const id = uidS('bf');
  const f = svg('filter', { id, x: '-30%', y: '-30%', width: '160%', height: '160%' }, defs);
  svg('feGaussianBlur', { stdDeviation: sd }, f);
  return `url(#${id})`;
}
function vignette(parent, defs, strength = 0.55) {
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(defs, [[0.55, '#000', 0], [1, '#000', strength]], { cx: 0.5, cy: 0.45, r: 0.75 }), 'pointer-events': 'none' }, parent);
}

// Blue-grey sofa (side view of the long side, like the reference). x,y = left edge of seat top.
function sofa(g, defs, x, y, w = 760, tone = 0) {
  const c = k => shade('#5e798d', k + tone);
  svg('rect', { x: x - 70, y: y - 250, width: w + 140, height: 270, rx: 46, fill: c(-6) }, g);       // back
  svg('rect', { x: x - 40, y: y - 222, width: w / 2 - 2 + 40, height: 200, rx: 30, fill: c(4) }, g); // back cushions
  svg('rect', { x: x + w / 2 + 2, y: y - 222, width: w / 2 - 2 + 40, height: 200, rx: 30, fill: c(4) }, g);
  svg('rect', { x: x - 30, y: y - 24, width: w + 60, height: 78, rx: 22, fill: c(10) }, g);        // seat cushions
  svg('rect', { x: x + w / 2 - 2, y: y - 24, width: 4, height: 78, fill: c(-14) }, g);
  svg('rect', { x: x - 60, y: y + 40, width: w + 120, height: 70, rx: 18, fill: c(-16) }, g);       // base
  svg('rect', { x: x - 126, y: y - 120, width: 112, height: 230, rx: 40, fill: c(-2) }, g);         // arms
  svg('rect', { x: x + w + 14, y: y - 120, width: 112, height: 230, rx: 40, fill: c(-2) }, g);
  svg('rect', { x: x - 104, y: y - 104, width: 70, height: 26, rx: 13, fill: c(8) }, g);
  svg('rect', { x: x + w + 34, y: y - 104, width: 70, height: 26, rx: 13, fill: c(8) }, g);
  for (const lx of [x - 90, x + w + 74]) svg('rect', { x: lx, y: y + 108, width: 18, height: 30, rx: 4, fill: '#2a2226' }, g);
  svg('rect', { x: x - 30, y: y + 50, width: w + 60, height: 10, fill: '#000', opacity: 0.12 }, g);
}
function floorLamp(g, defs, x, yFloor, glowColor = '#ffd59a', glowOp = 0.5) {
  svg('circle', { cx: x, cy: yFloor - 470, r: 330, fill: rad2(defs, [[0, glowColor, glowOp], [1, glowColor, 0]]) }, g);
  svg('rect', { x: x - 4, y: yFloor - 450, width: 8, height: 450, fill: '#2b2327' }, g);
  svg('ellipse', { cx: x, cy: yFloor, rx: 46, ry: 9, fill: '#2b2327' }, g);
  svg('path', { d: `M${x - 70},${yFloor - 440} L${x + 70},${yFloor - 440} L${x + 46},${yFloor - 540} L${x - 46},${yFloor - 540} Z`, fill: lin(defs, [[0, '#f6e3bd'], [1, '#e8c98f']]) }, g);
}
function woodFloor(g, defs, y0, c1, c2, lineC) {
  svg('rect', { x: 0, y: y0, width: 1080, height: 1920 - y0, fill: lin(defs, [[0, c1], [1, c2]]) }, g);
  for (let y = y0 + 40, k = 0; y < 1920; y += 64 + k * 6, k++) svg('rect', { x: 0, y, width: 1080, height: 3, fill: lineC, opacity: 0.55 }, g);
}
function rug(g, defs, cx, cy, rx, ry, c) {
  svg('ellipse', { cx, cy, rx, ry, fill: rad2(defs, [[0, shade(c, 18)], [1, c]], { cx: 0.5, cy: 0.35, r: 0.7 }) }, g);
}

// ---- purple tour bus, side view, facing right. (x,y) = bottom-left of body ----
function tourBus(g, defs, x, y, w = 1080, sign = 'กรุงเทพฯ - ขอนแก่น') {
  const h = 330, bg = svg('g', {}, g);
  svg('rect', { x, y: y - h, width: w, height: h, rx: 26, fill: lin(defs, [[0, '#5a4ca0'], [1, '#43377c']]) }, bg);
  svg('rect', { x, y: y - h, width: w, height: 16, rx: 8, fill: '#e9e6f0' }, bg);
  const nWin = Math.floor((w - 140) / 112);
  for (let i = 0; i < nWin; i++) {
    const wx = x + 30 + i * 112;
    svg('rect', { x: wx, y: y - h + 34, width: 96, height: 88, rx: 12, fill: '#2a2550' }, bg);
    svg('rect', { x: wx + 6, y: y - h + 40, width: 84, height: 76, rx: 9, fill: lin(defs, [[0, '#d6c19a'], [1, '#b49b74']]) }, bg);
    svg('path', { d: `M${wx + 14},${y - h + 108} L${wx + 46},${y - h + 46} L${wx + 60},${y - h + 46} L${wx + 28},${y - h + 108} Z`, fill: '#fff', opacity: 0.18 }, bg);
  }
  for (let i = 0; i < Math.min(5, nWin - 2); i++) svg('rect', { x: x + 40 + i * 150, y: y - h + 150, width: 120, height: 52, rx: 10, fill: '#262a52' }, bg);
  svg('path', { d: `M${x},${y - 120} C${x + w * 0.25},${y - 170} ${x + w * 0.45},${y - 70} ${x + w * 0.7},${y - 130} C${x + w * 0.85},${y - 165} ${x + w},${y - 150} ${x + w},${y - 150}`, fill: 'none', stroke: '#d9a94e', 'stroke-width': 18 }, bg);
  svg('path', { d: `M${x},${y - 95} C${x + w * 0.25},${y - 140} ${x + w * 0.45},${y - 45} ${x + w * 0.7},${y - 102} C${x + w * 0.85},${y - 134} ${x + w},${y - 120} ${x + w},${y - 120}`, fill: 'none', stroke: '#d892b8', 'stroke-width': 7 }, bg);
  svg('rect', { x: x + w - 120, y: y - h + 30, width: 92, height: 270, rx: 10, fill: '#2b2550' }, bg); // door
  svg('rect', { x: x + w - 112, y: y - h + 38, width: 76, height: 120, rx: 8, fill: '#3a3566' }, bg);
  svg('rect', { x: x + w - 330, y: y - h - 4, width: 300, height: 40, rx: 6, fill: '#151520' }, bg);
  const st = svg('text', { x: x + w - 180, y: y - h + 24, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 500, 'font-size': 24, fill: '#f0a640' }, bg); st.textContent = sign;
  svg('rect', { x: x - 4, y: y - 112, width: 12, height: 36, rx: 6, fill: '#ff5a4e' }, bg);
  svg('circle', { cx: x - 2, cy: y - 94, r: 40, fill: rad2(defs, [[0, '#ff5a4e', 0.5], [1, '#ff5a4e', 0]]) }, bg);
  const wheels = [];
  for (const wx of [x + 150, x + 300, x + w - 210]) {
    svg('rect', { x: wx - 70, y: y - 46, width: 140, height: 50, rx: 25, fill: '#2a2546' }, bg);
    const wg = svg('g', { transform: `translate(${wx},${y})` }, bg);
    svg('circle', { r: 52, fill: '#1c1a24' }, wg);
    svg('circle', { r: 26, fill: '#8d8fa0' }, wg);
    for (let k = 0; k < 6; k++) svg('rect', { x: -3, y: -24, width: 6, height: 24, fill: '#5d5f70', transform: `rotate(${k * 60})` }, wg);
    wheels.push(wg);
  }
  return { g: bg, wheels };
}

// ---- night living room (purple), used for the daughter's condo ----
function condoNight(s, defs) {
  const g = svg('g', {}, s);
  svg('rect', { x: 0, y: 0, width: 1080, height: 1330, fill: lin(defs, [[0, '#4a3f58'], [1, '#574a66']]) }, g);
  // window with city at night
  svg('rect', { x: 120, y: 200, width: 470, height: 560, rx: 8, fill: '#2a2236' }, g);
  svg('rect', { x: 136, y: 216, width: 438, height: 528, fill: lin(defs, [[0, '#18193a'], [1, '#2a2b58']]) }, g);
  const r = rng(11);
  for (let i = 0; i < 46; i++) svg('circle', { cx: 140 + r() * 430, cy: 222 + r() * 260, r: 1 + r() * 1.8, fill: '#fff', opacity: 0.3 + r() * 0.5 }, g);
  svg('circle', { cx: 470, cy: 300, r: 30, fill: '#f4ecd6', opacity: 0.9 }, g);
  let bx = 136;
  while (bx < 574) {
    const bw = Math.min(40 + r() * 54, 574 - bx), bh = 140 + r() * 240, by = 744 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: r() > 0.5 ? '#24264a' : '#2b2d55' }, g);
    for (let wy = by + 14; wy < 734; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14)
      if (r() > 0.58) svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#f3c86e', opacity: 0.8 }, g);
    bx += bw + 3;
  }
  svg('rect', { x: 352, y: 216, width: 6, height: 528, fill: '#2a2236' }, g);
  for (const cx of [86, 566]) {
    svg('rect', { x: cx, y: 180, width: 86, height: 640, rx: 16, fill: '#66557e' }, g);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: 190, width: 7, height: 620, rx: 3, fill: '#58496f' }, g);
  }
  svg('rect', { x: 70, y: 172, width: 600, height: 12, rx: 6, fill: '#3a3048' }, g);
  // small framed pictures and a wall shelf for life
  svg('rect', { x: 760, y: 330, width: 190, height: 140, rx: 6, fill: '#e9e2d6' }, g);
  svg('rect', { x: 772, y: 342, width: 166, height: 116, fill: '#8aa3b8' }, g);
  svg('path', { d: 'M772,458 L830,390 L870,430 L900,400 L938,458 Z', fill: '#5f7f6a' }, g);
  woodFloor(g, defs, 1330, '#3e3448', '#2c2434', '#2a2130');
  rug(g, defs, 540, 1560, 470, 110, '#4d4160');
  floorLamp(g, defs, 960, 1330);
  const sf = svg('g', {}, g);
  contactShadow(sf, defs, 520, 1338, 470, 26, 0.45);
  sofa(sf, defs, 170, 1140, 700);
  return g;
}

// ---- bus terminal at night (reference opening shot) ----
function terminal(s, defs) {
  const g = svg('g', {}, s);
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: lin(defs, [[0, '#2a3048'], [1, '#353b55']]) }, g);
  for (let i = 0; i < 5; i++) svg('rect', { x: 20 + i * 230, y: 60, width: 150, height: 14, rx: 7, fill: '#e8ecf5', opacity: 0.85 }, g);
  svg('rect', { x: 0, y: 100, width: 1080, height: 18, fill: '#3f4560' }, g);
  const bg = svg('g', { filter: blurFilter(defs, 7) }, g);
  const cols = ['#7e3846', '#2f6a74', '#7a6a2e', '#5c3a76'];
  for (let i = 0; i < 4; i++) {
    const bx = -60 + i * 300;
    svg('rect', { x: bx, y: 460, width: 240, height: 420, rx: 20, fill: cols[i], opacity: 0.85 }, bg);
    svg('rect', { x: bx + 30, y: 500, width: 180, height: 140, rx: 10, fill: shade(cols[i], 40), opacity: 0.8 }, bg);
    const t = svg('text', { x: bx + 120, y: 430, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 46, fill: '#c9cde0', opacity: 0.8 }, bg); t.textContent = 16 + i;
  }
  for (let i = 0; i < 4; i++) svg('rect', { x: 210 + i * 300, y: 118, width: 34, height: 1020, fill: '#272c43' }, g);
  svg('rect', { x: 0, y: 1110, width: 1080, height: 810, fill: lin(defs, [[0, '#33384f'], [1, '#262a3d']]) }, g);
  svg('rect', { x: 0, y: 1110, width: 1080, height: 22, fill: '#c9a24a' }, g);
  svg('rect', { x: 0, y: 1150, width: 1080, height: 8, fill: '#c9a24a', opacity: 0.5 }, g);
  return g;
}

// ---- night highway with lamp + guardrail parallax ----
function highway(s, defs) {
  const g = svg('g', {}, s);
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: lin(defs, [[0, '#161a3a'], [0.6, '#262a55'], [1, '#1a1d3c']]) }, g);
  const r = rng(5);
  for (let i = 0; i < 90; i++) svg('circle', { cx: r() * 1080, cy: r() * 900, r: 1 + r() * 2, fill: '#fff', opacity: 0.25 + r() * 0.5 }, g);
  const lamps = svg('g', {}, g);
  for (let i = 0; i < 6; i++) {
    const lx = i * 360;
    const lg = svg('g', { transform: `translate(${lx},0)` }, lamps);
    svg('rect', { x: -5, y: 640, width: 10, height: 520, fill: '#3a3d5c' }, lg);
    svg('path', { d: 'M0,646 Q20,620 58,624', fill: 'none', stroke: '#3a3d5c', 'stroke-width': 8 }, lg);
    svg('circle', { cx: 60, cy: 630, r: 110, fill: rad2(defs, [[0, '#ffcf7a', 0.55], [1, '#ffcf7a', 0]]) }, lg);
    svg('ellipse', { cx: 60, cy: 632, rx: 18, ry: 8, fill: '#fff1c8' }, lg);
  }
  svg('rect', { x: 0, y: 1150, width: 1080, height: 70, fill: '#1e2140' }, g);
  svg('rect', { x: 0, y: 1150, width: 1080, height: 8, fill: '#e9e6f0', opacity: 0.85 }, g);
  const rail = svg('g', {}, g);
  for (let i = 0; i < 9; i++) svg('rect', { x: i * 160, y: 1160, width: 12, height: 64, rx: 3, fill: '#d9d6e6' }, rail);
  svg('rect', { x: 0, y: 1220, width: 1080, height: 700, fill: lin(defs, [[0, '#15183a'], [1, '#0f1130']]) }, g);
  const refl = svg('g', { filter: blurFilter(defs, 6) }, g);
  for (let i = 0; i < 6; i++) svg('rect', { x: i * 360 + 52, y: 1290, width: 14, height: 260, rx: 7, fill: '#ffcf7a', opacity: 0.35 }, refl);
  return { g, lamps, rail, refl };
}

// ---- bus interior: seat + window, for the waffle-card backdrop ----
function busSeat(s, defs) {
  const g = svg('g', {}, s);
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: lin(defs, [[0, '#262a4c'], [1, '#1d203c']]) }, g);
  svg('rect', { x: 120, y: 360, width: 840, height: 520, rx: 40, fill: '#151838' }, g);
  svg('rect', { x: 150, y: 390, width: 780, height: 460, rx: 30, fill: lin(defs, [[0, '#1b2048'], [1, '#2b2f60']]) }, g);
  for (let i = 0; i < 4; i++) svg('circle', { cx: 230 + i * 210, cy: 560 + (i % 2) * 60, r: 70, fill: rad2(defs, [[0, '#ffcf7a', 0.4], [1, '#ffcf7a', 0]]) }, g);
  svg('rect', { x: 100, y: 330, width: 150, height: 600, rx: 30, fill: '#c25a7c' }, g);
  svg('rect', { x: 830, y: 330, width: 150, height: 600, rx: 30, fill: '#c25a7c' }, g);
  svg('rect', { x: 0, y: 1420, width: 1080, height: 500, fill: '#181a33' }, g);
  // seat (side view) facing right
  svg('rect', { x: 330, y: 840, width: 120, height: 560, rx: 50, fill: '#3e5ea8' }, g);
  svg('rect', { x: 352, y: 800, width: 90, height: 80, rx: 26, fill: '#e9e6f0' }, g);
  svg('rect', { x: 330, y: 1240, width: 330, height: 90, rx: 30, fill: '#4668b6' }, g);
  svg('rect', { x: 470, y: 1330, width: 24, height: 120, fill: '#2a2d4a' }, g);
  return g;
}

// ---- mom's house: wooden Isan room at night ----
function momHouse(s, defs) {
  const g = svg('g', {}, s);
  const tones = ['#8a6143', '#7f573a', '#906746', '#86603f'];
  for (let i = 0; i < 13; i++) {
    svg('rect', { x: i * 84, y: 0, width: 84, height: 1380, fill: tones[i % 4] }, g);
    svg('rect', { x: i * 84, y: 0, width: 3, height: 1380, fill: '#634229', opacity: 0.6 }, g);
  }
  svg('rect', { x: 0, y: 0, width: 1080, height: 1380, fill: lin(defs, [[0, '#1b1020', 0.35], [0.6, '#1b1020', 0.0], [1, '#1b1020', 0.25]]) }, g);
  // window with night + moon at the right
  svg('rect', { x: 770, y: 230, width: 250, height: 330, rx: 6, fill: '#4b3220' }, g);
  svg('rect', { x: 784, y: 244, width: 222, height: 302, fill: lin(defs, [[0, '#18193a'], [1, '#2c2d5a']]) }, g);
  svg('circle', { cx: 940, cy: 320, r: 30, fill: '#f4ecd6' }, g);
  svg('rect', { x: 892, y: 244, width: 6, height: 302, fill: '#4b3220' }, g);
  svg('rect', { x: 784, y: 392, width: 222, height: 6, fill: '#4b3220' }, g);
  woodFloor(g, defs, 1380, '#6a4630', '#4c311f', '#3f2817');
  // bulb glow
  svg('rect', { x: 600, y: 0, width: 5, height: 150, fill: '#2a1d14' }, g);
  svg('circle', { cx: 602, cy: 168, r: 22, fill: '#ffe4ad' }, g);
  svg('circle', { cx: 602, cy: 360, r: 820, fill: rad2(defs, [[0, '#ffd9a0', 0.42], [0.5, '#ffd9a0', 0.12], [1, '#ffd9a0', 0]]) }, g);
  return g;
}
