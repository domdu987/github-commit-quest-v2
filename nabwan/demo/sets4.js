// v4 sets: Thai street dog, coconut broom, morning condo, golden-hour Isan yard with a stilt house,
// night bus interior with the moon. Same flat-gradient language as sets.js.

// ---------------- dog (side view, faces right; ground at y = 0 in local space) ----------------
class Dog {
  constructor(parent, o = {}) {
    this.o = o = Object.assign({ coat: '#c98b4a', coatDark: '#a86f38', light: '#f1d3a6', collar: '#d9473f' }, o);
    this.g = svg('g', {}, parent);
    const line = (c, w) => svg('path', { fill: 'none', stroke: c, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, this.g);
    this.legBR = line(o.coatDark, 11); this.legBF = line(o.coatDark, 11);
    this.tail = svg('path', { fill: 'none', stroke: o.coat, 'stroke-width': 11, 'stroke-linecap': 'round' }, this.g);
    this.body = svg('g', {}, this.g);
    svg('path', { fill: o.coat, d: 'M-72,-96 C-82,-62 -58,-50 -26,-54 L34,-56 C62,-56 74,-80 66,-102 C58,-120 18,-114 -10,-112 C-42,-114 -68,-114 -72,-96 Z' }, this.body);
    svg('path', { fill: o.light, d: 'M-40,-58 C-10,-50 30,-50 50,-60 C40,-52 10,-46 -20,-48 Z', opacity: 0.9 }, this.body);
    svg('ellipse', { cx: 56, cy: -78, rx: 14, ry: 21, fill: o.light }, this.body);
    this.head = svg('g', {}, this.body);
    svg('path', { fill: o.coatDark, d: 'M62,-134 L70,-166 L88,-138 Z' }, this.head);
    svg('circle', { cx: 80, cy: -124, r: 25, fill: o.coat }, this.head);
    svg('path', { fill: o.light, d: 'M92,-128 C108,-130 122,-124 122,-112 C122,-102 108,-100 94,-104 Z' }, this.head);
    svg('ellipse', { cx: 120, cy: -118, rx: 6, ry: 5, fill: '#2a1d1a' }, this.head);
    this.tongue = svg('path', { fill: '#e8737a', d: 'M104,-104 C106,-92 114,-90 116,-100 Z', opacity: 0 }, this.head);
    svg('path', { fill: 'none', stroke: '#2a1d1a', 'stroke-width': 2.4, 'stroke-linecap': 'round', d: 'M100,-104 Q108,-100 116,-104' }, this.head);
    this.eye = svg('g', { transform: 'translate(92,-132)' }, this.head);
    svg('circle', { r: 4.6, fill: '#1e1718' }, this.eye);
    svg('circle', { cx: 1.4, cy: -1.6, r: 1.5, fill: '#fff' }, this.eye);
    this.ear = svg('path', { fill: o.coat, d: 'M70,-140 L76,-170 L92,-144 Z' }, this.head);
    svg('path', { fill: 'none', stroke: o.collar, 'stroke-width': 8, 'stroke-linecap': 'round', d: 'M60,-106 Q66,-96 76,-98' }, this.body);
    svg('circle', { cx: 70, cy: -94, r: 4.5, fill: '#f2c14e' }, this.body);
    this.legFR = line(o.coat, 12); this.legFF = line(o.coat, 12);
  }
  // p: x, y (ground), f, s, ph (gait phase), run 0..1, wag 0..1, sit 0..1, head (deg), t, jump (px)
  pose(p) {
    const s = p.s || 1, f = p.f || 1, run = p.run || 0, sit = p.sit || 0, ph = p.ph || 0, t = p.t || 0;
    const bob = run * -7 * Math.abs(Math.sin(ph)) - (p.jump || 0);
    const pitch = run * 4 * Math.sin(ph) - sit * 24 + (p.pitch || 0);
    this.g.setAttribute('transform', `translate(${p.x.toFixed(1)},${p.y.toFixed(1)}) scale(${(f * s).toFixed(3)},${s.toFixed(3)})`);
    this.body.setAttribute('transform', `translate(0,${(bob + sit * 22).toFixed(1)}) rotate(${pitch.toFixed(2)} 40 -70)`);
    this.head.setAttribute('transform', `rotate(${(p.head || 0) + sit * 18} 74 -106)`);
    const A = 12 + 26 * run;
    const leg = (el, hx, hy, off, front) => {
      // hip position follows the body rotation
      const a = rad(pitch), cx = 40, cy = -70;
      const hx2 = cx + (hx - cx) * Math.cos(a) - (hy - cy) * Math.sin(a);
      const hy2 = cy + (hx - cx) * Math.sin(a) + (hy - cy) * Math.cos(a) + bob + sit * 22;
      let up = 90 + A * Math.sin(ph + off) * (run > 0.02 ? 1 : 0);
      let bend = (14 + 40 * run) * Math.max(0, Math.cos(ph + off));
      let lo = front ? up - bend * 0.7 : up + bend;
      if (!front && sit > 0) { up = lerp(up, -8, sit); lo = lerp(lo, 120, sit); }
      const L1 = front ? 36 : 38, L2 = front ? 36 : 34;
      const k = [hx2 + Math.cos(rad(up)) * L1, hy2 + Math.sin(rad(up)) * L1];
      const e = [k[0] + Math.cos(rad(lo)) * L2, k[1] + Math.sin(rad(lo)) * L2];
      el.setAttribute('d', `M${hx2.toFixed(1)},${hy2.toFixed(1)} L${k[0].toFixed(1)},${k[1].toFixed(1)} L${e[0].toFixed(1)},${e[1].toFixed(1)} l7,0`);
    };
    leg(this.legFR, 46, -70, 0, true); leg(this.legFF, 40, -70, 2.6, true);
    leg(this.legBR, -50, -72, Math.PI, false); leg(this.legBF, -56, -72, Math.PI + 2.6, false);
    const wag = (p.wag || 0) * Math.sin(t * 22) * 28;
    const ta = rad(pitch);
    const bx = 40 + (-70 - 40) * Math.cos(ta) - (-98 + 70) * Math.sin(ta), by = -70 + (-70 - 40) * Math.sin(ta) + (-98 + 70) * Math.cos(ta) + bob + sit * 22;
    const tipA = rad(-120 + wag - sit * 30);
    this.tail.setAttribute('d', `M${bx.toFixed(1)},${by.toFixed(1)} Q${(bx - 30).toFixed(1)},${(by - 8).toFixed(1)} ${(bx + Math.cos(tipA) * 44).toFixed(1)},${(by + Math.sin(tipA) * 44).toFixed(1)}`);
    this.tongue.setAttribute('opacity', run > 0.3 || p.pant ? 1 : 0);
    this.ear.setAttribute('transform', `rotate(${(-run * 18 * Math.abs(Math.sin(ph))).toFixed(1)} 76 -142)`);
  }
}

// coconut-leaf broom held at the top (prop space: hand at 0,0, broom hangs along +y)
function broom(parent) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M0,-20 L0,170', stroke: '#8a5a34', 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
  svg('rect', { x: -7, y: 150, width: 14, height: 24, rx: 4, fill: '#6b4226' }, g);
  for (let i = -9; i <= 9; i++) svg('path', { d: `M${i * 0.6},170 Q${i * 2.6},215 ${i * 4.4},262`, stroke: i % 3 ? '#d1ad72' : '#b88f55', 'stroke-width': 2.4, fill: 'none' }, g);
  return g;
}

// ---------------- morning condo (S7), three depth layers ----------------
function condoDay(S) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#e3d6c3'], [1, '#cfbfa8']]) }, F.s);
  svg('rect', { x: 120, y: 200, width: 470, height: 560, rx: 8, fill: '#bfae98' }, F.s);
  svg('rect', { x: 136, y: 216, width: 438, height: 528, fill: lin(F.defs, [[0, '#8fc3ea'], [0.7, '#cfe6f6'], [1, '#f4efe2']]) }, F.s);
  const r = rng(12);
  svg('circle', { cx: 210, cy: 290, r: 150, fill: rad2(F.defs, [[0, '#fffbe8', 0.95], [0.25, '#fff4cf', 0.6], [1, '#fff4cf', 0]]) }, F.s);
  for (let i = 0; i < 3; i++) svg('ellipse', { cx: 300 + i * 120, cy: 330 + (i % 2) * 40, rx: 70, ry: 18, fill: '#ffffff', opacity: 0.7 }, F.s);
  let bx = 136;
  while (bx < 574) {
    const bw = Math.min(40 + r() * 54, 574 - bx), bh = 120 + r() * 230, by = 744 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: r() > 0.5 ? '#9fb3c8' : '#b4c4d4' }, F.s);
    for (let wy = by + 14; wy < 734; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14)
      if (r() > 0.5) svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#e8f1f8', opacity: 0.8 }, F.s);
    bx += bw + 3;
  }
  svg('rect', { x: 352, y: 216, width: 6, height: 528, fill: '#bfae98' }, F.s);
  for (const cx of [86, 566]) {
    svg('rect', { x: cx, y: 180, width: 86, height: 640, rx: 16, fill: lin(F.defs, [[0, '#f4ecdf'], [1, '#e4d8c6']], 1, 0) }, F.s);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: 190, width: 7, height: 620, rx: 3, fill: '#ddd0bc' }, F.s);
  }
  svg('rect', { x: 70, y: 172, width: 600, height: 12, rx: 6, fill: '#a8927a' }, F.s);
  // framed photo of mom & daughter + wall shelf with a plant
  svg('rect', { x: 760, y: 330, width: 190, height: 140, rx: 6, fill: '#fbf7ef' }, F.s);
  svg('rect', { x: 772, y: 342, width: 166, height: 116, fill: '#f0c9a8' }, F.s);
  faceFront(F.s, 820, 402, 30, { skin: '#c8956e', hair: '#3a3234', hairStyle: 'bun', gray: '#b5aeae', glasses: true });
  faceFront(F.s, 890, 406, 28, { skin: '#d8ab86', hair: '#2a2220', hairStyle: 'bob' });
  svg('rect', { x: 740, y: 560, width: 240, height: 12, rx: 6, fill: '#a8927a' }, F.s);
  svg('rect', { x: 780, y: 506, width: 46, height: 54, rx: 8, fill: '#d9774f' }, F.s);
  for (let k = 0; k < 5; k++) svg('ellipse', { cx: 803 + (k - 2) * 12, cy: 494 - Math.abs(k - 2) * 4, rx: 9, ry: 22, fill: '#4f8a5b', transform: `rotate(${(k - 2) * 22} ${803 + (k - 2) * 12} 500)` }, F.s);
  // mid: floor, sun patch, sofa, girl
  woodFloor(M.s, M.defs, 1330, '#b48d67', '#8e6a4a', '#7d5c3f');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#8e6a4a' }, M.s);
  rug(M.s, M.defs, 540, 1560, 470, 110, '#d8b48e');
  const beams = svg('g', { opacity: 0.55 }, M.s);
  svg('path', { d: 'M136,216 L574,216 L1020,1500 L330,1500 Z', fill: lin(M.defs, [[0, '#fffbea', 0.42], [1, '#fffbea', 0]]) }, beams);
  svg('path', { d: 'M330,1500 L1020,1500 L1080,1640 L360,1640 Z', fill: '#fff6dc', opacity: 0.3 }, M.s);
  floorLamp(M.s, M.defs, 960, 1330, '#fff3dc', 0.12);
  contactShadow(M.s, M.defs, 520, 1338, 470, 26, 0.35);
  sofa(M.s, M.defs, 170, 1140, 700, 8);
  // backpack leaning on the sofa arm
  const bp = svg('g', { transform: 'translate(700,1150)' }, M.s);
  svg('path', { d: 'M-46,0 C-50,-90 50,-90 46,0 L48,150 C48,170 -48,170 -48,150 Z', fill: '#2e3140' }, bp);
  svg('rect', { x: -34, y: 50, width: 68, height: 70, rx: 14, fill: '#3a3e52' }, bp);
  svg('path', { d: 'M-24,-60 Q0,-96 24,-60', fill: 'none', stroke: '#23252f', 'stroke-width': 8 }, bp);
  svg('rect', { x: -6, y: 60, width: 12, height: 6, rx: 3, fill: '#d6ad52' }, bp);
  const dust = floaters(M.s, [200, 260, 700, 1000], 30, 31, { color: '#fffaf0', rMin: 1.2, rMax: 3.6, speed: 7, op: 0.55, base: 0.08 });
  vignette(M.s, M.defs, 0.28);
  // fore: bright monstera + sun bokeh
  const leaf = (x, y, s, a, c) => {
    const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
    svg('path', { d: 'M0,0 C60,-70 210,-80 270,0 C210,90 60,80 0,0 Z', fill: c }, g);
    svg('path', { d: 'M8,0 L262,0', stroke: shade(c, 30), 'stroke-width': 6 }, g);
    for (const kx of [70, 130, 190]) svg('path', { d: `M${kx},-40 L${kx + 20},-6 M${kx},40 L${kx + 20},6`, stroke: '#cdbca4', 'stroke-width': 10 }, g);
    return g;
  };
  const leaves = [leaf(-120, 1880, 1.6, -60, '#2f6b45'), leaf(-80, 1900, 1.5, -25, '#3d7d52'), leaf(-160, 1700, 1.4, -5, '#4a8c5d'), leaf(-60, 1960, 1.3, -88, '#2b5f3e')];
  svg('circle', { cx: 1040, cy: 200, r: 90, fill: '#fff1c4', opacity: 0.35 }, R.s);
  svg('circle', { cx: 900, cy: 90, r: 60, fill: '#fff6dc', opacity: 0.3 }, R.s);
  return {
    update(t) {
      dust(t + 3);
      beams.setAttribute('opacity', (0.5 + 0.08 * Math.sin(t * 1.3)).toFixed(3));
      leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });
    },
  };
}

// ---------------- night bus interior with the moon outside (S4) ----------------
// far layer: night sky + moon at (940, 320) + passing lamps; mid: window frame, seat, girl
function busNight(S) {
  const F = S.L.far, M = S.L.mid;
  svg('rect', { x: -400, y: -400, width: 1880, height: 2700, fill: lin(F.defs, [[0, '#141738'], [0.5, '#272a5c'], [1, '#1b1e3e']]) }, F.s);
  const r = rng(77);
  for (let i = 0; i < 90; i++) svg('circle', { cx: -100 + r() * 1300, cy: -100 + r() * 1000, r: 0.8 + r() * 2, fill: '#fff', opacity: 0.25 + r() * 0.55 }, F.s);
  const moonGlow = svg('circle', { cx: 940, cy: 320, r: 120, fill: rad2(F.defs, [[0, '#fff3d6', 0.5], [1, '#fff3d6', 0]]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 26, fill: '#f6eed8' }, F.s);
  svg('circle', { cx: 931, cy: 313, r: 5, fill: '#e6dcc0' }, F.s);
  svg('circle', { cx: 949, cy: 330, r: 3.5, fill: '#e6dcc0' }, F.s);
  const hills = svg('g', {}, F.s);
  for (let i = 0; i < 4; i++) svg('path', { d: `M${-300 + i * 700},900 Q${50 + i * 700},640 ${400 + i * 700},900 Z`, fill: '#1a1c3c' }, hills);
  const passing = svg('g', {}, F.s);
  for (let i = 0; i < 9; i++) svg('circle', { cx: i * 260, cy: 720 + (i % 3) * 60, r: 50 + (i % 2) * 28, fill: rad2(F.defs, [[0, '#ffcf7a', 0.6], [1, '#ffcf7a', 0]]) }, passing);
  // mid: interior wall with a big window cut-out (evenodd), curtains, seat, girl
  svg('path', { 'fill-rule': 'evenodd', fill: lin(M.defs, [[0, '#2c2f58'], [1, '#1d2040']]), d: 'M-400,-400 L1480,-400 L1480,2300 L-400,2300 Z M110,150 L1040,150 Q1070,150 1070,180 L1070,870 Q1070,900 1040,900 L110,900 Q80,900 80,870 L80,180 Q80,150 110,150 Z' }, M.s);
  svg('rect', { x: 80, y: 150, width: 990, height: 750, rx: 30, fill: 'none', stroke: '#3a3e6e', 'stroke-width': 18 }, M.s);
  svg('rect', { x: 80, y: 150, width: 990, height: 750, rx: 30, fill: lin(M.defs, [[0, '#ffffff', 0.05], [0.5, '#ffffff', 0], [1, '#ffffff', 0.04]], 1, 1) }, M.s);
  svg('rect', { x: 40, y: 120, width: 120, height: 820, rx: 30, fill: '#c25a7c' }, M.s);
  svg('rect', { x: 52, y: 140, width: 18, height: 790, rx: 8, fill: '#a94a6a' }, M.s);
  svg('rect', { x: -400, y: 1420, width: 1880, height: 900, fill: '#141630' }, M.s);
  svg('rect', { x: 330, y: 840, width: 120, height: 560, rx: 50, fill: '#3e5ea8' }, M.s);
  svg('rect', { x: 352, y: 800, width: 90, height: 80, rx: 26, fill: '#e9e6f0' }, M.s);
  svg('rect', { x: 330, y: 1240, width: 330, height: 90, rx: 30, fill: '#4668b6' }, M.s);
  svg('rect', { x: 470, y: 1330, width: 24, height: 120, fill: '#2a2d4a' }, M.s);
  return {
    moonGlow,
    update(t) {
      passing.setAttribute('transform', `translate(${-((t * 900) % 520)},0)`);
      hills.setAttribute('transform', `translate(${-((t * 60) % 700)},0)`);
    },
  };
}

// ---------------- golden-hour Isan yard with a stilt house (S8) ----------------
// layers: sky, far (hills, sugar palms, birds), field, house, mid (yard + characters), fore
function isanYard(S) {
  const K = S.L.sky, F = S.L.far, D = S.L.field, H = S.L.house, M = S.L.mid, R = S.L.fore;
  const SUN = [240, 1150];
  svg('rect', { x: -400, y: -400, width: 1880, height: 2000, fill: lin(K.defs, [[0, '#5d5a9a'], [0.35, '#c07f9a'], [0.62, '#f2a77c'], [0.8, '#ffd08f'], [1, '#ffe2a8']]) }, K.s);
  svg('circle', { cx: SUN[0], cy: SUN[1], r: 900, fill: rad2(K.defs, [[0, '#fff1c8', 0.75], [0.25, '#ffd48f', 0.35], [1, '#ffb070', 0]]) }, K.s);
  const clouds = svg('g', {}, K.s);
  [[620, 420, 260, 34], [880, 560, 200, 26], [280, 640, 240, 30], [760, 760, 300, 22], [140, 300, 180, 22]].forEach(([x, y, w, h], i) => {
    svg('ellipse', { cx: x, cy: y, rx: w, ry: h, fill: i % 2 ? '#ffc6a8' : '#f7b3a2', opacity: 0.55 }, clouds);
    svg('ellipse', { cx: x - w * 0.3, cy: y - h * 0.6, rx: w * 0.45, ry: h * 0.9, fill: '#ffd9bd', opacity: 0.45 }, clouds);
  });
  svg('circle', { cx: SUN[0], cy: SUN[1], r: 64, fill: '#fff7e0' }, K.s);
  svg('circle', { cx: SUN[0], cy: SUN[1], r: 100, fill: rad2(K.defs, [[0, '#ffffff', 0.7], [1, '#ffffff', 0]]) }, K.s);
  // far: layered hazy hills + sugar palms + birds
  svg('path', { d: 'M-400,1260 Q-100,1140 200,1210 T800,1180 T1480,1230 L1480,1500 L-400,1500 Z', fill: '#c98a8e', opacity: 0.75 }, F.s);
  svg('path', { d: 'M-400,1290 Q0,1220 400,1270 T1100,1250 T1480,1280 L1480,1500 L-400,1500 Z', fill: '#b47680', opacity: 0.8 }, F.s);
  const palm = (x, y, h, s) => {
    const g = svg('g', { transform: `translate(${x},${y}) scale(${s})` }, F.s);
    svg('path', { d: `M-4,0 Q-2,${-h * 0.5} 2,${-h} L6,${-h} Q4,${-h * 0.5} 6,0 Z`, fill: '#7d4f5f' }, g);
    for (let k = 0; k < 14; k++) {
      const a = -Math.PI + (k / 13) * Math.PI * 1.0 - 0.0;
      const L = 46 + (k % 3) * 8;
      svg('path', { d: `M3,${-h} Q${3 + Math.cos(a) * L * 0.6},${-h + Math.sin(a) * L * 0.6 - 10} ${3 + Math.cos(a) * L},${-h + Math.sin(a) * L * 0.4 + 14}`, stroke: '#7d4f5f', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round' }, g);
    }
    svg('circle', { cx: 3, cy: -h + 4, r: 14, fill: '#7d4f5f' }, g);
  };
  palm(60, 1280, 260, 1); palm(150, 1290, 300, 0.9); palm(930, 1270, 240, 1); palm(1010, 1285, 280, 0.85); palm(-60, 1300, 220, 1);
  const birds = Array.from({ length: 5 }, (_, i) => ({ el: svg('path', { fill: 'none', stroke: '#5b3a4c', 'stroke-width': 3.4, 'stroke-linecap': 'round' }, F.s), x0: -100 - i * 70, y0: 520 + (i % 3) * 40 + i * 14, ph: i * 1.3 }));
  // field: rice paddies with rows, bunds, a far tree line
  svg('rect', { x: -400, y: 1300, width: 1880, height: 260, fill: lin(D.defs, [[0, '#c9b45a'], [1, '#9aa04a']]) }, D.s);
  for (let i = 0; i < 9; i++) svg('rect', { x: -400, y: 1312 + i * i * 3.2, width: 1880, height: 2 + i * 0.4, fill: '#e8d27a', opacity: 0.55 }, D.s);
  svg('path', { d: 'M-400,1360 L1480,1340', stroke: '#b38b52', 'stroke-width': 6, opacity: 0.6 }, D.s);
  svg('path', { d: 'M-400,1420 L1480,1398', stroke: '#a57d48', 'stroke-width': 8, opacity: 0.6 }, D.s);
  for (let i = 0; i < 12; i++) svg('ellipse', { cx: -300 + i * 160, cy: 1302, rx: 70 + (i % 3) * 20, ry: 26 + (i % 2) * 10, fill: '#8f7a52', opacity: 0.7 }, D.s);
  // house: Isan stilt house on the right
  const hs = H.s;
  svg('ellipse', { cx: 860, cy: 1452, rx: 420, ry: 26, fill: '#5a3424', opacity: 0.35 }, hs);
  svg('rect', { x: 540, y: 1080, width: 620, height: 370, fill: lin(H.defs, [[0, '#3d261c'], [1, '#5a3a28']]) }, hs); // shade under the house
  // under-house life: bench, jar, hammock
  svg('rect', { x: 850, y: 1340, width: 190, height: 18, rx: 4, fill: '#a77a4c' }, hs);
  for (const lx of [862, 1020]) svg('rect', { x: lx, y: 1356, width: 10, height: 70, fill: '#7a5534' }, hs);
  svg('path', { d: 'M712,1450 C680,1440 676,1360 700,1340 L760,1340 C784,1360 780,1440 748,1450 Z', fill: '#4a2c22' }, hs);
  svg('ellipse', { cx: 730, cy: 1340, rx: 32, ry: 8, fill: '#2d1a14' }, hs);
  svg('path', { d: 'M712,1376 Q730,1366 748,1376', stroke: '#c79a5a', 'stroke-width': 3, fill: 'none', opacity: 0.7 }, hs);
  const hammock = svg('path', { fill: '#d0574b', opacity: 0.9 }, hs);
  for (const px of [560, 700, 840, 980, 1120]) {
    svg('rect', { x: px - 11, y: 1070, width: 22, height: 382, fill: '#6b4a33' }, hs);
    svg('rect', { x: px - 11, y: 1070, width: 7, height: 382, fill: '#e2a36a', opacity: 0.35 }, hs);
  }
  svg('rect', { x: 528, y: 1062, width: 650, height: 28, fill: '#5a3c28' }, hs);
  // walls (vertical planks) with warm window + door
  for (let i = 0; i < 20; i++) svg('rect', { x: 582 + i * 30, y: 858, width: 30, height: 206, fill: ['#9b6b45', '#8f613d', '#a3734b'][i % 3] }, hs);
  for (let i = 0; i < 20; i++) svg('rect', { x: 582 + i * 30, y: 858, width: 2, height: 206, fill: '#5e3d26', opacity: 0.6 }, hs);
  svg('rect', { x: 700, y: 905, width: 104, height: 96, rx: 4, fill: '#ffcf8a' }, hs);
  svg('rect', { x: 700, y: 905, width: 104, height: 96, rx: 4, fill: rad2(H.defs, [[0, '#fff1c8', 0.9], [1, '#ffb867', 0.2]]) }, hs);
  svg('rect', { x: 664, y: 902, width: 36, height: 102, fill: '#7a5134' }, hs);
  svg('rect', { x: 804, y: 902, width: 36, height: 102, fill: '#7a5134' }, hs);
  svg('rect', { x: 900, y: 880, width: 82, height: 184, fill: '#3a2216' }, hs);
  svg('rect', { x: 908, y: 890, width: 66, height: 174, fill: rad2(H.defs, [[0, '#ffcf8a', 0.75], [1, '#8a4f2a', 0.3]]) }, hs);
  // gable wall (plank boards + a small warm vent) under a weathered zinc roof with a sun-side highlight
  svg('path', { d: 'M560,870 L858,672 L1160,870 Z', fill: lin(H.defs, [[0, '#9b6b45'], [1, '#7f5638']]) }, hs);
  for (let x = 590; x < 1140; x += 30) {
    const top = 870 - (x < 858 ? (x - 560) : (1160 - x)) * (198 / 300);
    svg('path', { d: `M${x},${top.toFixed(1)} L${x},870`, stroke: '#5e3d26', 'stroke-width': 2, opacity: 0.55 }, hs);
  }
  svg('path', { d: 'M858,742 L884,782 L858,822 L832,782 Z', fill: '#3a2216' }, hs);
  svg('path', { d: 'M858,752 L876,782 L858,812 L840,782 Z', fill: rad2(H.defs, [[0, '#ffd99a', 0.9], [1, '#c77a3a', 0.4]]) }, hs);
  svg('path', { d: 'M520,880 L858,640 L1200,880 L1180,900 L858,676 L540,900 Z', fill: '#6f5a58' }, hs);
  svg('path', { d: 'M540,872 L858,648 L1180,872 L1160,874 L858,686 L560,874 Z', fill: lin(H.defs, [[0, '#d9b08a'], [0.5, '#a89290'], [1, '#8a7a7a']], 1, 0) }, hs);
  // porch + railing + stairs down to the yard (left)
  svg('rect', { x: 528, y: 1040, width: 60, height: 24, fill: '#7a5134' }, hs);
  for (let i = 0; i < 4; i++) svg('rect', { x: 532 + i * 16, y: 972, width: 6, height: 70, fill: '#7a5134' }, hs);
  svg('rect', { x: 524, y: 966, width: 70, height: 10, rx: 3, fill: '#8a5d3b' }, hs);
  for (let i = 0; i < 7; i++) svg('rect', { x: 440 + i * 14, y: 1420 - i * 52, width: 80, height: 12, rx: 3, fill: '#8a5d3b' }, hs);
  svg('path', { d: 'M436,1440 L536,1066', stroke: '#6b4a33', 'stroke-width': 10 }, hs);
  svg('path', { d: 'M520,1440 L590,1066', stroke: '#6b4a33', 'stroke-width': 10 }, hs);
  // banana tree left of the stairs
  const ban = svg('g', { transform: 'translate(380,1450)' }, hs);
  svg('path', { d: 'M-10,0 Q-6,-180 0,-330 L14,-330 Q10,-180 12,0 Z', fill: '#7d8a3c' }, ban);
  const banLeaves = [];
  [[-140, -0.9], [-60, -0.5], [20, -0.2], [100, 0.3], [160, 0.7]].forEach(([dx, a], i) => {
    const lg = svg('g', { transform: `translate(4,-320) rotate(${a * 57})` }, ban);
    svg('path', { d: 'M0,0 C40,-30 150,-40 220,10 C150,30 50,30 0,0 Z', fill: i % 2 ? '#8faa45' : '#a6bd52' }, lg);
    svg('path', { d: 'M0,0 C70,-10 150,-8 220,10', stroke: '#d8e08a', 'stroke-width': 3, fill: 'none', opacity: 0.8 }, lg);
    banLeaves.push({ lg, a, i });
  });
  // laundry line with a plaid pha khao ma + shirt
  svg('path', { d: 'M1120,1150 Q1000,1190 880,1160', stroke: '#3a2a20', 'stroke-width': 3, fill: 'none' }, hs);
  const pid = uidS('plaid');
  const pat = svg('pattern', { id: pid, width: 30, height: 30, patternUnits: 'userSpaceOnUse' }, H.defs);
  svg('rect', { width: 30, height: 30, fill: '#c23b3b' }, pat);
  svg('rect', { width: 15, height: 30, fill: '#2f4fa0', opacity: 0.75 }, pat);
  svg('rect', { width: 30, height: 15, fill: '#ffffff', opacity: 0.35 }, pat);
  const cloth = svg('path', { d: 'M1030,1176 L1100,1162 L1104,1290 Q1070,1300 1036,1300 Z', fill: `url(#${pid})` }, hs);
  const shirt = svg('path', { d: 'M900,1166 L960,1176 L976,1200 L962,1206 L960,1270 L908,1266 L906,1200 L890,1196 Z', fill: '#e9d7b8' }, hs);
  // yard (mid): warm dirt, light pool, pebbles, grass tufts
  svg('rect', { x: -400, y: 1440, width: 1880, height: 900, fill: lin(M.defs, [[0, '#d39a63'], [0.35, '#b47a4e'], [1, '#6e4630']]) }, M.s);
  svg('ellipse', { cx: 380, cy: 1560, rx: 700, ry: 120, fill: rad2(M.defs, [[0, '#ffd9a0', 0.45], [1, '#ffd9a0', 0]]) }, M.s);
  const rr = rng(4);
  for (let i = 0; i < 40; i++) svg('ellipse', { cx: -200 + rr() * 1500, cy: 1470 + rr() * 500, rx: 3 + rr() * 6, ry: 2 + rr() * 3, fill: '#8a5a3c', opacity: 0.5 }, M.s);
  for (let i = 0; i < 16; i++) {
    const gx = -200 + rr() * 1500, gy = 1460 + rr() * 480;
    for (let k = -2; k <= 2; k++) svg('path', { d: `M${gx},${gy} q${k * 4},-14 ${k * 7},-24`, stroke: k % 2 ? '#8f9a3e' : '#a9b24c', 'stroke-width': 3, fill: 'none', 'stroke-linecap': 'round' }, M.s);
  }
  // fore: blurred grass + flowers, top-left mango branch
  const fg = svg('g', {}, R.s);
  for (let i = 0; i < 16; i++) svg('path', { d: `M${-160 + i * 90},2140 Q${-140 + i * 90},1950 ${-100 + i * 90 + (i % 3) * 20},${1800 + (i % 4) * 40}`, stroke: i % 2 ? '#5e6a28' : '#73802f', 'stroke-width': 26, fill: 'none', 'stroke-linecap': 'round' }, fg);
  for (let i = 0; i < 6; i++) svg('circle', { cx: -40 + i * 230, cy: 1880 + (i % 2) * 50, r: 26, fill: i % 2 ? '#f2c14e' : '#f08a6a', opacity: 0.85 }, fg);
  const branch = svg('g', {}, R.s);
  svg('path', { d: 'M-200,-60 Q120,40 330,10', stroke: '#3c2a22', 'stroke-width': 26, fill: 'none', 'stroke-linecap': 'round' }, branch);
  for (let i = 0; i < 9; i++) svg('ellipse', { cx: -100 + i * 50, cy: 30 + (i % 3) * 30, rx: 56, ry: 20, fill: i % 2 ? '#3f5a26' : '#557532', transform: `rotate(${30 + i * 13} ${-100 + i * 50} ${30 + (i % 3) * 30})` }, branch);
  return {
    SUN,
    update(t) {
      clouds.setAttribute('transform', `translate(${(t * 6).toFixed(1)},0)`);
      birds.forEach(b => {
        const x = b.x0 + t * 120, y = b.y0 - t * 10 + Math.sin(t * 2 + b.ph) * 6, w = 12 * Math.sin(t * 13 + b.ph);
        b.el.setAttribute('d', `M${(x - 14).toFixed(1)},${(y - w).toFixed(1)} Q${(x - 6).toFixed(1)},${(y - 4).toFixed(1)} ${x.toFixed(1)},${y.toFixed(1)} Q${(x + 6).toFixed(1)},${(y - 4).toFixed(1)} ${(x + 14).toFixed(1)},${(y - w).toFixed(1)}`);
      });
      banLeaves.forEach(({ lg, a, i }) => lg.setAttribute('transform', `translate(4,-320) rotate(${(a * 57 + Math.sin(t * 1.4 + i) * 3).toFixed(2)})`));
      cloth.setAttribute('transform', `skewX(${(Math.sin(t * 1.6) * 3).toFixed(2)})`);
      shirt.setAttribute('transform', `skewX(${(Math.sin(t * 1.6 + 1) * 3).toFixed(2)})`);
      hammock.setAttribute('d', `M560,1250 Q630,${(1320 + Math.sin(t * 1.2) * 6).toFixed(1)} 700,1250 L700,1262 Q630,${(1334 + Math.sin(t * 1.2) * 6).toFixed(1)} 560,1262 Z`);
      fg.setAttribute('transform', `skewX(${(Math.sin(t * 1.1) * 2).toFixed(2)})`);
      branch.setAttribute('transform', `rotate(${(Math.sin(t * 0.9) * 1.2).toFixed(2)} -200 -60)`);
    },
  };
}
