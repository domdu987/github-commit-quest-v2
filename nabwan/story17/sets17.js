// "128 ช่อ" sets: the florist's shopfront at dawn and at dusk (cream-pink facade, a dusty-rose scalloped awning, a window
// of bouquets under a pink neon heart, buckets on the pavement, a chalkboard, a street lamp, the wires); the street he
// rides (a scrolling strip of shophouses, poles and trees over a wet or sunny road; rain with splashes and reflections,
// or night with neon and lamps sweeping over him); and their townhouse at night (warm beige wall, a lit window, the front
// door that opens onto lamplight, fairy lights on the gate, plants, slippers, the moon). Every set returns { people,
// front, shadowL, top, ground, light, update(t, ...) }.

function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': o.font || 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}
const G17 = 1330;
// city rooftops for the far layer
function skyline17(F, top, sky, bld, lit, seed) {
  svg('rect', { x: -500, y: -600, width: 2200, height: 2200, fill: lin(F.defs, sky) }, F.s);
  const r = rng(seed); let x = -480;
  while (x < 1600) { const w = 80 + r() * 140, h = 200 + r() * 420; svg('rect', { x, y: top + 600 - h, width: w, height: h + 600, fill: bld[Math.floor(r() * bld.length)] }, F.s); if (lit) for (let wy = top + 620 - h; wy < top + 860; wy += 30) for (let wx = x + 10; wx < x + w - 14; wx += 20) if (r() > 0.6) svg('rect', { x: wx, y: wy, width: 8, height: 12, fill: lit, opacity: 0.8 }, F.s); x += w + 6; }
}
// the florist (shopfront): mode 'dawn' | 'dusk'
function shopFront17(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = G17, D = M.defs, dusk = o.mode === 'dusk';
  skyline17(F, 0, dusk ? [[0, '#3a2a5a'], [0.5, '#c86a7a'], [1, '#f8a860']] : [[0, '#4a4a8a'], [0.5, '#e890a8'], [1, '#ffd8a8']], ['#5a4a6a', '#6a5a78', '#4a3a5a'], dusk ? '#ffd06a' : null, 1701);
  // the building: upper floor with windows, the shop below
  svg('rect', { x: -300, y: 120, width: 1700, height: G - 120, fill: '#f2d6c8' }, M.s);
  for (let k = 0; k < 4; k++) { const x = 60 + k * 260; svg('rect', { x, y: 200, width: 150, height: 170, rx: 8, fill: dusk ? '#ffd890' : '#8a9ab8', stroke: '#a8786a', 'stroke-width': 8 }, M.s); svg('rect', { x: x + 70, y: 200, width: 10, height: 170, fill: '#a8786a' }, M.s); svg('rect', { x: x - 10, y: 370, width: 170, height: 14, fill: '#a8786a' }, M.s); }
  svg('rect', { x: -300, y: 420, width: 1700, height: 30, fill: '#c89080' }, M.s);
  // the sign board and the scalloped awning
  svg('rect', { x: 330, y: 456, width: 680, height: 84, rx: 10, fill: '#5a3a3a', stroke: INK, 'stroke-width': 4 }, M.s);
  wtext(M.s, 670, 512, 'ร้านดอกไม้ บ้านกุหลาบ', 46, '#ffe0e8', { w: 700 });
  for (let k = 0; k < 10; k++) svg('path', { d: `M${300 + k * 74},540 L${374 + k * 74},540 L${374 + k * 74},590 Q${337 + k * 74},622 ${300 + k * 74},590 Z`, fill: k % 2 ? '#fbeef0' : '#d88a9a', stroke: INK, 'stroke-width': 3 }, M.s);
  // the window: shelves of bouquets, a neon heart
  svg('rect', { x: 380, y: 640, width: 600, height: 560, fill: lin(D, dusk ? [[0, '#ffe8c0'], [1, '#f8c8a8']] : [[0, '#fbe8e0'], [1, '#f2d0c8']]), stroke: '#6a4a4a', 'stroke-width': 12 }, M.s);
  const neon = svg('g', {}, M.s); svg('path', { d: heartPathT(680, 760, 46), fill: 'none', stroke: '#ff6aa0', 'stroke-width': 7 }, neon); const neonGlow = svg('path', { d: heartPathT(680, 760, 46), fill: 'none', stroke: '#ff9ac0', 'stroke-width': 22, opacity: 0.35, filter: blurFilter(D, 6) }, neon);
  for (const y of [900, 1080]) { svg('rect', { x: 392, y, width: 576, height: 12, fill: '#a87a5a' }, M.s); for (let k = 0; k < 6; k++) { const b = svg('g', { transform: `translate(${430 + k * 96},${y}) scale(0.62)` }, M.s); bouquet17(b, 1); } }
  svg('rect', { x: 380, y: 640, width: 600, height: 560, fill: '#ffffff', opacity: 0.1 }, M.s);
  svg('path', { d: 'M420,660 L520,660 L420,800 Z', fill: '#ffffff', opacity: 0.18 }, M.s);
  // the door
  svg('rect', { x: 150, y: 640, width: 190, height: G - 640, fill: dusk ? '#ffe0b0' : '#e8c8c0', stroke: '#6a4a4a', 'stroke-width': 12 }, M.s);
  svg('rect', { x: 168, y: 960, width: 154, height: 10, fill: '#c8a8a0' }, M.s); svg('circle', { cx: 316, cy: 1000, r: 8, fill: '#e8b04a', stroke: INK, 'stroke-width': 2 }, M.s);
  const open = svg('g', {}, M.s); svg('rect', { x: 200, y: 690, width: 90, height: 54, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 3 }, open); wtext(open, 245, 726, dusk ? 'ปิด' : 'เปิด', 26, dusk ? '#c8343c' : '#2f9e5b', { w: 700 });
  // pavement and road
  svg('rect', { x: -300, y: G, width: 1700, height: 70, fill: '#a8988e' }, M.s);
  for (let x = -300; x < 1400; x += 80) svg('path', { d: `M${x},${G} L${x},${G + 70}`, stroke: '#8a7a70', 'stroke-width': 2 }, M.s);
  svg('rect', { x: -300, y: G + 70, width: 1700, height: 16, fill: '#e8e2d6' }, M.s);
  svg('rect', { x: -300, y: G + 86, width: 1700, height: 800, fill: lin(D, [[0, '#4a4248'], [1, '#1a161c']]) }, M.s);
  for (let x = -260; x < 1400; x += 220) svg('rect', { x, y: G + 330, width: 120, height: 10, fill: '#e8d8a0', opacity: 0.5 }, M.s);
  wallAO(M.s, D, G, { op: 0.25 });
  // the lamp and the wires
  svg('rect', { x: 1040, y: 300, width: 14, height: G - 300, fill: '#6a6a72', stroke: INK, 'stroke-width': 2 }, M.s);
  svg('path', { d: 'M1046,310 Q1000,290 980,320', fill: 'none', stroke: '#6a6a72', 'stroke-width': 10 }, M.s);
  svg('path', { d: 'M960,320 L1000,320 L992,340 L968,340 Z', fill: '#fff2c0', stroke: INK, 'stroke-width': 3 }, M.s);
  const lampG = svg('circle', { cx: 980, cy: 360, r: 160, fill: rad2(D, [[0, '#ffe8b0', 0.55], [1, '#ffe8b0', 0]]), style: 'mix-blend-mode:screen' }, M.s);
  for (const [y, sag] of [[160, 40], [190, 60], [230, 30]]) svg('path', { d: `M-300,${y} Q500,${y + sag} 1500,${y - 20}`, fill: 'none', stroke: '#2a2a32', 'stroke-width': 3 }, M.s);
  // buckets on the pavement, the chalkboard
  const bk = (x, col) => { const g = svg('g', { transform: `translate(${x},${G + 10})` }, M.s); for (let k = -2; k <= 2; k++) { svg('path', { d: `M${k * 4},-40 L${k * 12},-110`, stroke: '#3f7a46', 'stroke-width': 4 }, g); svg('circle', { cx: k * 12, cy: -114 + Math.abs(k) * 6, r: 13, fill: col, stroke: INK, 'stroke-width': 2.4 }, g); } svg('path', { d: 'M-34,-50 L34,-50 L28,0 L-28,0 Z', fill: '#c8d8e8', stroke: INK, 'stroke-width': 3 }, g); };
  [[440, '#d8283a'], [540, '#f08aa8'], [640, '#f6efe2'], [740, '#d8283a'], [840, '#f2c14e']].forEach(([x, c]) => bk(x, c));
  const cb = svg('g', { transform: `translate(1180,${G})` }, M.s); svg('path', { d: 'M-70,0 L-50,-230 L50,-230 L70,0', fill: 'none', stroke: '#8a5a32', 'stroke-width': 8 }, cb); svg('rect', { x: -60, y: -220, width: 120, height: 150, rx: 6, fill: '#2a3a2e', stroke: '#8a5a32', 'stroke-width': 6 }, cb); wtext(cb, 0, -176, 'วาเลนไทน์', 22, '#ffe0e8', { w: 600 }); svg('path', { d: heartPathT(0, -146, 10), fill: '#ff6aa0' }, cb); wtext(cb, 0, -102, 'ช่อละ 590.-', 22, '#fbf7ef', { w: 700 });
  const shadowL = svg('g', {}, M.s), people = svg('g', {}, M.s), front = svg('g', {}, M.s), top = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 6, [-100, -60, 1180, 380], ['#ff9ac0', '#ffd890', '#fff0c8'], 1702, { rMin: 30, rMax: 80, op: 0.28 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 50%, rgba(30,10,30,.5) 100%)';
  return {
    people, front, shadowL, top, ground: G, light: { ux: 0.6, uy: -0.8, lx: 980 },
    update(t) { neonGlow.setAttribute('opacity', (0.3 + 0.12 * Math.sin(t * 9) + (Math.sin(t * 23) > 0.97 ? -0.2 : 0)).toFixed(2)); lampG.setAttribute('opacity', dusk ? 1 : 0.55); if (bok) bok(t); },
  };
}

// the street he rides: mode 'rain' | 'sun' | 'night'; update(t, scroll) moves the strip by scroll pixels
function street17(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = G17, D = M.defs, mode = o.mode || 'sun', rain = mode === 'rain', night = mode === 'night';
  skyline17(F, 100, night ? [[0, '#141a3a'], [1, '#3a2a4a']] : rain ? [[0, '#6a6a7a'], [1, '#a89a98']] : [[0, '#8ac8f0'], [1, '#fbe8c8']], night ? ['#1e2240', '#262a4a'] : rain ? ['#6a6272', '#7a7280'] : ['#a8b0c8', '#b8c0d0', '#98a4c0'], night ? '#ffd06a' : null, 1703);
  if (night) svg('circle', { cx: 860, cy: 260, r: 34, fill: '#f8eed4' }, F.s);
  // the strip: two copies of a 1600-px run of shophouses, poles and trees
  const PER = 1600, strip = svg('g', {}, M.s);
  const unit = (g, x0) => {
    const cols = night ? ['#4a3a4a', '#3a3448', '#4a4040'] : rain ? ['#b8a49a', '#a89a9a', '#c0aa98'] : ['#f2c8a0', '#e8d0b0', '#f0b8a8', '#d8c8a8'], signs = ['#c8343c', '#2f6a4a', '#e8b04a', '#4a7bd8'];
    for (let k = 0; k < 6; k++) {
      const x = x0 + k * 260, c = cols[k % cols.length];
      svg('rect', { x, y: 300, width: 254, height: G - 300, fill: c, stroke: shade(c, -25), 'stroke-width': 4 }, g);
      for (const dx of [30, 140]) { svg('rect', { x: x + dx, y: 360, width: 84, height: 150, rx: 6, fill: night ? (k % 2 ? '#ffd890' : '#2a2a3a') : '#7a8aa8', opacity: 0.9 }, g); }
      svg('rect', { x: x + 14, y: 560, width: 226, height: 60, rx: 6, fill: signs[k % 4], stroke: INK, 'stroke-width': 3 }, g);
      svg('rect', { x: x + 30, y: 576, width: 140, height: 20, rx: 4, fill: '#fbf2d8', opacity: 0.85 }, g);
      svg('rect', { x: x + 20, y: 640, width: 214, height: G - 640, fill: night ? '#ffcf88' : '#6a5a52' }, g);
      if (!night) for (let j = 0; j < 14; j++) svg('rect', { x: x + 20, y: 650 + j * 48, width: 214, height: 4, fill: '#4a3a34', opacity: 0.5 }, g);
      if (night) svg('rect', { x: x + 20, y: 640, width: 214, height: G - 640, fill: rad2(D, [[0, '#fff2c0', 0.6], [1, '#ffcf88', 0]]) }, g);
      if (k % 3 === 1) { svg('rect', { x: x + 250, y: 200, width: 14, height: G - 200, fill: '#7a7a82', stroke: INK, 'stroke-width': 2 }, g); for (const [y, sag] of [[220, 30], [240, 46]]) svg('path', { d: `M${x + 257},${y} Q${x + 387},${y + sag} ${x + 517},${y}`, fill: 'none', stroke: '#2a2a32', 'stroke-width': 3 }, g); }
      if (k % 3 === 2) { svg('path', { d: `M${x + 200},${G} L${x + 210},${G - 260} L${x + 230},${G - 260} L${x + 240},${G} Z`, fill: '#6a4a32' }, g); for (const [dx, dy, r] of [[180, -300, 70], [250, -320, 80], [215, -380, 70]]) svg('circle', { cx: x + dx, cy: G + dy, r, fill: night ? '#1e3020' : '#5a9a4a' }, g); }
      if (night && k % 2 === 0) { svg('rect', { x: x + 60, y: 450, width: 130, height: 50, rx: 10, fill: 'none', stroke: ['#ff6aa0', '#6ae0ff', '#ffd06a'][k % 3], 'stroke-width': 6, filter: blurFilter(D, 2) }, g); }
    }
  };
  const s1 = svg('g', {}, strip), s2 = svg('g', {}, strip); unit(s1, 0); unit(s2, 0);
  // pavement, kerb, road and its dashes
  svg('rect', { x: -300, y: G, width: 1700, height: 60, fill: night ? '#3a3440' : rain ? '#7a7276' : '#b8a898' }, M.s);
  svg('rect', { x: -300, y: G + 60, width: 1700, height: 14, fill: '#d8d2c8' }, M.s);
  svg('rect', { x: -300, y: G + 74, width: 1700, height: 900, fill: lin(D, night ? [[0, '#26222c'], [1, '#0e0a12']] : rain ? [[0, '#3a3640'], [1, '#16121a']] : [[0, '#5a5258'], [1, '#2a2228']]) }, M.s);
  const dashes = svg('g', {}, M.s); for (let k = 0; k < 10; k++) svg('rect', { x: k * 220, y: G + 300, width: 130, height: 10, fill: '#e8d8a0', opacity: 0.55 }, dashes);
  const refl = svg('g', { opacity: rain ? 0.4 : night ? 0.3 : 0 }, M.s);   // shop lights on the wet road
  for (let k = 0; k < 8; k++) svg('rect', { x: k * 200 + 40, y: G + 90, width: 40, height: 240, fill: lin(D, [[0, ['#ffd890', '#ff9ac0', '#6ae0ff'][k % 3], 0.8], [1, '#000000', 0]]) }, refl);
  wallAO(M.s, D, G, { op: 0.22 });
  const shadowL = svg('g', {}, M.s), people = svg('g', {}, M.s), front = svg('g', {}, M.s), top = svg('g', {}, M.s);
  const rainL = rain ? rainField(R ? R.s : M.s, [-200, -300, 1300, 2100], 380, 1704, { len: 80, slant: -0.16, speed: 2100, op: 0.6, w: 3 }) : null;
  const rainM = rain ? rainField(M.s, [-200, -300, 1300, 2100], 420, 1705, { len: 50, slant: -0.16, speed: 1600, op: 0.45, w: 2.2 }) : null;
  const spl = rain ? splashField(M.s, -100, 1200, G + 90, G + 520, 26, 1706) : null;
  const lamps = night ? [0, 1, 2].map(i => svg('ellipse', { rx: 220, ry: 520, fill: rad2(D, [[0, '#ffe8b0', 0.32], [1, '#ffe8b0', 0]]), style: 'mix-blend-mode:screen' }, M.s)) : [];
  const vg = html('div', '', S.fx); vg.style.cssText = `position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 48%, ${night ? 'rgba(8,6,24,.62)' : rain ? 'rgba(20,16,30,.55)' : 'rgba(40,20,10,.4)'} 100%)`;
  const lens = rain ? lensDrops(S.fx, 7, 1707) : null;
  return {
    people, front, shadowL, top, ground: G, light: night ? { ux: 0.2, uy: -0.98, lx: 600 } : rain ? { ux: 0.3, uy: -0.95, lx: 700 } : { ux: 0.5, uy: -0.86, lx: 900 },
    update(t, scroll = 0) {
      const x = -(scroll % PER); s1.setAttribute('transform', `translate(${x.toFixed(1)},0)`); s2.setAttribute('transform', `translate(${(x + PER).toFixed(1)},0)`);
      dashes.setAttribute('transform', `translate(${(-((scroll * 1.15) % 220)).toFixed(1)},0)`); refl.setAttribute('transform', `translate(${(-((scroll) % 200)).toFixed(1)},0)`);
      if (rainL) { rainL(t); rainM(t); spl(t); } if (lens) lens(t);
      lamps.forEach((l, i) => { const lx = 1400 - ((scroll * 1.0 + i * 700) % 2100); setA(l, { cx: lx.toFixed(1), cy: 900 }); });
    },
  };
}

// their townhouse at night
function home17(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = G17, D = M.defs;
  skyline17(F, 200, [[0, '#121838'], [0.7, '#2a2a52'], [1, '#4a3050']], ['#1e2240', '#22264a'], '#ffd06a', 1708);
  svg('circle', { cx: 880, cy: 180, r: 90, fill: rad2(F.defs, [[0, '#fff2d0', 0.5], [1, '#fff2d0', 0]]) }, F.s); svg('circle', { cx: 880, cy: 180, r: 36, fill: '#f8eed4' }, F.s);
  const stars = []; { const r = rng(1709); for (let i = 0; i < 30; i++) stars.push(svg('circle', { cx: -200 + r() * 1400, cy: 40 + r() * 300, r: 1 + r() * 1.6, fill: '#fff' }, F.s)); }
  // the house front
  svg('rect', { x: -40, y: 360, width: 1000, height: G - 360, fill: '#e8c8a0' }, M.s);
  svg('path', { d: 'M-80,370 L1000,370 L1000,330 L-80,330 Z', fill: '#a8584a', stroke: INK, 'stroke-width': 4 }, M.s);
  for (let x = -60; x < 1000; x += 46) svg('path', { d: `M${x},330 L${x + 23},300 L${x + 46},330`, fill: '#c86a5a', stroke: INK, 'stroke-width': 3 }, M.s);
  svg('rect', { x: -40, y: 1100, width: 1000, height: G - 1100, fill: '#c8a078' }, M.s);
  // the window (lit), with a curtain and a cat silhouette
  svg('rect', { x: 620, y: 520, width: 280, height: 300, fill: lin(D, [[0, '#ffe2a8'], [1, '#ffc878']]), stroke: '#7a4a2a', 'stroke-width': 12 }, M.s);
  svg('path', { d: 'M620,520 Q680,620 650,820 L620,820 Z M900,520 Q840,620 870,820 L900,820 Z', fill: '#d8486a', opacity: 0.85 }, M.s);
  svg('rect', { x: 756, y: 520, width: 8, height: 300, fill: '#7a4a2a' }, M.s);
  svg('path', { d: 'M800,820 q-10,-40 6,-54 l6,-14 l8,12 l8,-12 l4,16 q14,16 4,52 Z', fill: '#3a2a30' }, M.s);
  lightPool(M.s, D, 760, 670, 300, 260, '#ffc878', 0.35);
  // the door: frame, the leaf (opens), the warm hall beyond, the lamp above
  const DX0 = 360, DX1 = 560, DY = 520;
  svg('rect', { x: DX0, y: DY, width: DX1 - DX0, height: G - DY, fill: lin(D, [[0, '#ffe8c0'], [1, '#f8b878']]) }, M.s);
  svg('rect', { x: DX0 + 50, y: DY + 100, width: 70, height: 200, fill: '#e8a868', opacity: 0.5 }, M.s);   // a picture in the hall
  const leaf = svg('g', {}, M.s); svg('rect', { x: DX0, y: DY, width: DX1 - DX0, height: G - DY, fill: '#7a4a2a', stroke: INK, 'stroke-width': 4 }, leaf); svg('rect', { x: DX0 + 30, y: DY + 40, width: DX1 - DX0 - 60, height: 300, rx: 6, fill: '#5a3420' }, leaf); svg('rect', { x: DX0 + 30, y: DY + 380, width: DX1 - DX0 - 60, height: 300, rx: 6, fill: '#5a3420' }, leaf); svg('circle', { cx: DX1 - 26, cy: DY + 380, r: 9, fill: '#e8b04a', stroke: INK, 'stroke-width': 2 }, leaf);
  svg('rect', { x: DX0 - 14, y: DY - 14, width: DX1 - DX0 + 28, height: G - DY + 14, fill: 'none', stroke: '#5a3420', 'stroke-width': 16 }, M.s);
  const spill = svg('path', { d: `M${DX0},${G} L${DX1},${G} L${DX1 + 260},${G + 500} L${DX0 - 260},${G + 500} Z`, fill: lin(D, [[0, '#ffd890', 0.55], [1, '#ffd890', 0]]), style: 'mix-blend-mode:screen', opacity: 0 }, M.s);
  svg('path', { d: 'M446,470 L474,470 L470,490 L450,490 Z', fill: '#fff2c0', stroke: INK, 'stroke-width': 3 }, M.s);
  const lampG = svg('circle', { cx: 460, cy: 500, r: 200, fill: rad2(D, [[0, '#ffe2a0', 0.6], [1, '#ffe2a0', 0]]), style: 'mix-blend-mode:screen' }, M.s);
  wtext(M.s, 640, 470, '49/2', 30, '#5a3420', { w: 700 });
  // plants, slippers, the gate with fairy lights, the yard
  pottedPlant(M.s, 270, G, 0.62, 'snake', '#c8643a'); pottedPlant(M.s, 640, G, 0.5, 'monstera', '#e8e2d6');
  slippers(M.s, 600, G + 8, '#f08aa8', 0.9); slippers(M.s, 300, G + 10, '#4a5a7a', 1.0);
  svg('rect', { x: -300, y: G, width: 1700, height: 900, fill: lin(D, [[0, '#4a3a3a'], [1, '#1a1216']]) }, M.s);
  for (let x = -300; x < 1400; x += 120) svg('path', { d: `M${x},${G} L${x - 60},${G + 600}`, stroke: '#2a1e22', 'stroke-width': 3, opacity: 0.6 }, M.s);
  svg('rect', { x: 960, y: 900, width: 18, height: G - 900, fill: '#3a3a42' }, M.s); for (let y = 920; y < G; y += 60) svg('path', { d: `M970,${y} L1300,${y}`, stroke: '#3a3a42', 'stroke-width': 6 }, M.s);
  const fairy = lightString(M.s, 960, 1400, 930, 20, ['#ffd06a', '#ff9ac0', '#fff2c0'], 9);
  const fairy2 = lightString(M.s, -40, 360, 400, 18, ['#ffd06a', '#ff9ac0', '#fff2c0'], 8);
  wallAO(M.s, D, G, { op: 0.3 });
  const shadowL = svg('g', {}, M.s), people = svg('g', {}, M.s), front = svg('g', {}, M.s), top = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 6, [-100, -60, 1180, 380], ['#ffd06a', '#ff9ac0', '#fff2c0'], 1710, { rMin: 30, rMax: 80, op: 0.3 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 48%, rgba(8,6,24,.6) 100%)';
  return {
    people, front, shadowL, top, ground: G, door: (DX0 + DX1) / 2, light: { ux: -0.3, uy: -0.95, lx: 460 },
    open(k) { leaf.setAttribute('transform', `translate(${DX0},0) scale(${(1 - 0.85 * clamp(k)).toFixed(3)},1) translate(${-DX0},0)`); spill.setAttribute('opacity', clamp(k).toFixed(3)); },
    update(t) { stars.forEach((s, i) => s.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 2 + i)).toFixed(2))); [...fairy, ...fairy2].forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2.6 + i)).toFixed(2))); lampG.setAttribute('opacity', (0.9 + 0.1 * Math.sin(t * 5)).toFixed(2)); if (bok) bok(t); },
  };
}
