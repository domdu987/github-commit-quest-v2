// "15 ปีใหม่" sets: inside the night tour bus on New Year's Eve (a cut-away along the aisle: mustard seats with white
// headrest covers, burgundy curtains with gold fringe, amber LED strip, a TV counting down, tinsel, the windshield with the
// road ahead and the driver; outside, street lamps and fireworks rush past), the bus on the highway at night, the Bangkok
// bus terminal (platform 92, the flip departure board, New Year lanterns), and ยาย's Isan house on New Year's Eve
// (teak walls, ขันโตก, sticky-rice กระติ๊บ, the plate kept for แม่ under a ฝาชี, the TV countdown).
// Every set returns { people, shadowL, top, light, ground, update(t), ... }.

function wtext(g, x, y, s, size, fill, o = {}) {
  const e = svg('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': o.w || 600, 'font-size': size, fill }, o.a || {}), g);
  e.textContent = s; return e;
}

// ---------------- fireworks: a fixed schedule of bursts (deterministic in t) ----------------
// bursts: [{ t, x, y, c, r, n }]; returns { update(t), flash(t) → [k, colour] }
function fireworks13(parent, defs, bursts, o = {}) {
  const g = svg('g', { style: 'mix-blend-mode:screen' }, parent), rise = o.rise ?? 0.55, life = o.life ?? 1.5, grav = o.grav ?? 90;
  const B = bursts.map((b, i) => {
    const r = rng(1000 + i * 37 + (o.seed || 0)), n = b.n || 26, bg = svg('g', {}, g);
    const halo = svg('circle', { r: 10, fill: rad2(defs, [[0, b.c, 0.35], [1, b.c, 0]]) }, bg);
    const glow = svg('circle', { r: 10, fill: rad2(defs, [[0, '#fff6e0', 1], [0.25, b.c, 0.6], [1, b.c, 0]]) }, bg);
    const trail = svg('path', { fill: 'none', stroke: '#ffe9c4', 'stroke-width': 3, 'stroke-linecap': 'round' }, bg);
    const sp = Array.from({ length: n }, (_, k) => ({ a: (k / n) * Math.PI * 2 + r() * 0.2, v: (b.r || 160) * (0.75 + r() * 0.35),
      el: svg('path', { fill: 'none', stroke: k % 3 ? b.c : '#fff6dc', 'stroke-width': b.w || o.w || 5, 'stroke-linecap': 'round' }, bg) }));
    return Object.assign({}, b, { bg, glow, halo, trail, sp });
  });
  return {
    update(t) {
      for (const b of B) {
        const x = t - b.t;
        if (x < -rise || x > life) { b.bg.setAttribute('display', 'none'); continue; }
        b.bg.removeAttribute('display');
        if (x < 0) {   // rising trail
          const k = (x + rise) / rise, y = b.y + (1 - ease.outCubic(k)) * (o.riseH ?? 380);
          b.trail.setAttribute('d', `M${b.x},${(y + 40).toFixed(1)} L${b.x},${y.toFixed(1)}`); b.trail.setAttribute('opacity', 0.8);
          b.glow.setAttribute('opacity', 0); b.halo.setAttribute('opacity', 0); b.sp.forEach(s => s.el.setAttribute('opacity', 0));
          continue;
        }
        b.trail.setAttribute('opacity', 0);
        const k = x / life, fade = Math.pow(1 - k, 1.4);
        setA(b.glow, { cx: b.x, cy: b.y, r: ((b.r || 160) * (0.5 + 0.6 * ease.outCubic(Math.min(1, x / 0.3)))).toFixed(1), opacity: (Math.max(0, 1 - x / 0.55)).toFixed(3) });
        setA(b.halo, { cx: b.x, cy: b.y, r: ((b.r || 160) * 1.6).toFixed(1), opacity: (fade * 0.8).toFixed(3) });
        for (const s of b.sp) {
          const d = s.v * ease.outCubic(Math.min(1, x / 0.9)), dy = grav * x * x;
          const px = b.x + Math.cos(s.a) * d, py = b.y + Math.sin(s.a) * d + dy;
          const d0 = s.v * ease.outCubic(Math.min(1, Math.max(0, x - 0.12) / 0.9)), qx = b.x + Math.cos(s.a) * d0, qy = b.y + Math.sin(s.a) * d0 + grav * Math.max(0, x - 0.12) ** 2;
          s.el.setAttribute('d', `M${qx.toFixed(1)},${qy.toFixed(1)} L${px.toFixed(1)},${py.toFixed(1)}`);
          s.el.setAttribute('opacity', (fade * (0.75 + 0.25 * Math.sin(x * 40 + s.a * 7))).toFixed(3));
        }
      }
    },
    flash(t) {
      let k = 0, c = '#ffd59a';
      for (const b of B) { const x = t - b.t; if (x >= 0 && x < 0.6) { const v = (1 - x / 0.6) * (b.r || 160) / 200; if (v > k) { k = v; c = b.c; } } }
      return [k, c];
    },
  };
}
// a fixed list of bursts spread over [t0, t1] (seeded), inside a box
function burstPlan(t0, t1, n, box, seed, cols = ['#ffd166', '#ff7a9a', '#8fd0ff', '#b8f28f', '#ffb36b', '#e8a0ff'], o = {}) {
  const r = rng(seed), out = [];
  for (let i = 0; i < n; i++) out.push({ t: t0 + (t1 - t0) * (i + r() * 0.8) / n, x: box[0] + r() * (box[2] - box[0]), y: box[1] + r() * (box[3] - box[1]), c: cols[i % cols.length], r: (o.rMin ?? 90) + r() * ((o.rMax ?? 170) - (o.rMin ?? 90)), n: o.n ?? 24, w: o.w });
  return out;
}

// ---------------- night outside a moving vehicle (far layer): sky, town lights, lamps and trees rushing past ----------------
// box: [x0, y0, x1, y1] to fill; speed px/s (things move +x: the bus drives to the left); returns update(t)
function nightOutside13(F, box, o = {}) {
  const [x0, y0, x1, y1] = box, hz = o.horizon ?? (y0 + (y1 - y0) * 0.7), sp = o.speed ?? 520;
  svg('rect', { x: x0, y: y0, width: x1 - x0, height: y1 - y0, fill: lin(F.defs, [[0, '#14143a'], [0.55, '#3a2a5e'], [0.85, '#a8566a'], [1, '#e89a6a']]) }, F.s);
  const r = rng(o.seed || 1301);
  for (let i = 0; i < 90; i++) svg('circle', { cx: x0 + r() * (x1 - x0), cy: y0 + r() * (hz - y0) * 0.8, r: 0.8 + r() * 1.8, fill: '#fff6e8', opacity: 0.4 + r() * 0.5 }, F.s);
  if (o.moon) { svg('circle', { cx: o.moon[0], cy: o.moon[1], r: 90, fill: rad2(F.defs, [[0, '#fff2cc', 0.5], [1, '#fff2cc', 0]]) }, F.s); svg('circle', { cx: o.moon[0], cy: o.moon[1], r: 34, fill: '#fff4d8' }, F.s); }
  const fw = o.bursts ? fireworks13(F.s, F.defs, o.bursts, { seed: 3 }) : null;
  // distant town: a band of tiny warm windows, slow
  const town = svg('g', {}, F.s);
  for (let i = 0; i < 2; i++) for (let x = 0; x < 1800; x += 30 + r() * 40) {
    const h = 20 + r() * 70; svg('rect', { x: x + i * 1800, y: hz - h, width: 22 + r() * 30, height: h, fill: '#1e1a3a' }, town);
    for (let k = 0; k < 3; k++) if (r() > 0.4) svg('rect', { x: x + i * 1800 + 4 + r() * 14, y: hz - h + 6 + r() * (h - 12), width: 4, height: 5, fill: '#ffd59a', opacity: 0.8 }, town);
  }
  svg('rect', { x: x0, y: hz, width: x1 - x0, height: y1 - hz, fill: lin(F.defs, [[0, '#2a1e2e'], [1, '#120c18']]) }, F.s);
  // traffic and roadside lights (warm bokeh) streaming past at window height
  const lights = svg('g', { style: 'mix-blend-mode:screen' }, F.s);
  for (let i = 0; i < 2; i++) for (let k = 0; k < 34; k++) { const x = i * 2400 + r() * 2400, y = hz - 190 + r() * 210, c = ['#ffc070', '#ff7a5a', '#ffe9a8', '#ff9a40'][k % 4], rr = 8 + r() * 18; svg('circle', { cx: x, cy: y, r: rr * 2.2, fill: rad2(F.defs, [[0, c, 0.7], [0.4, c, 0.3], [1, c, 0]]) }, lights); }
  // trees and street lamps rushing past (two copies wrap)
  const near = svg('g', {}, F.s), lamps = [];
  for (let i = 0; i < 2; i++) for (let x = 0; x < 2400; x += 400) {
    const X = x + i * 2400;
    svg('path', { d: `M${X + 120},${hz + 20} q-40,-120 0,-200 q40,80 0,200 Z`, fill: '#0e0a14', opacity: 0.9 }, near);
    svg('rect', { x: X + 300, y: hz - 260, width: 8, height: 300, fill: '#1a1420' }, near);
    svg('path', { d: `M${X + 304},${hz - 258} q40,-20 70,0`, fill: 'none', stroke: '#1a1420', 'stroke-width': 7 }, near);
    lamps.push(svg('circle', { cx: X + 372, cy: hz - 250, r: 70, fill: rad2(F.defs, [[0, '#ffc070', 0.85], [0.3, '#ff9a40', 0.35], [1, '#ff9a40', 0]]) }, near));
  }
  return {
    fw,
    update(t) {
      town.setAttribute('transform', `translate(${(x0 + ((t * sp * 0.08) % 1800) - 1800).toFixed(1)},0)`);
      near.setAttribute('transform', `translate(${(x0 + ((t * sp) % 2400) - 2400).toFixed(1)},0)`);
      lights.setAttribute('transform', `translate(${(x0 + ((t * sp * 0.6) % 2400) - 2400).toFixed(1)},0)`);
      if (fw) fw.update(t);
    },
  };
}
// a band of light from a passing street lamp sweeping across the interior (screen blend); returns update(t)
function lightSweep13(parent, defs, box, o = {}) {
  const [x0, y0, x1, y1] = box, w = o.w ?? 420, period = o.period ?? (400 / (o.speed ?? 520)), c = o.color || '#ffb060';
  const g = svg('g', { style: 'mix-blend-mode:screen', opacity: o.op ?? 0.3 }, parent);
  const band = svg('rect', { y: y0, width: w, height: y1 - y0, fill: lin(defs, [[0, c, 0], [0.5, c, 1], [1, c, 0]], 1, 0) }, g);
  const span = x1 - x0 + w * 2;
  return t => { const u = ((t / period) % 1); band.setAttribute('x', (x0 - w + u * span).toFixed(1)); band.setAttribute('transform', `skewX(-12)`); };
}

// ---------------- the cabin ----------------
const ROW13 = k => 470 + (k - 1) * 250;   // seat-row centre x, row 1 at the front
const SEAT13 = 1172;                        // cushion top
function busCabin(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1330, NR = o.rows ?? 8;
  const XL = -260, XR = ROW13(NR) + 300;
  // outside (far layer): sky, town, lamps, fireworks
  const out = nightOutside13(F, [XL - 600, 200, XR + 600, 1400], { horizon: 900, speed: 520, moon: [1500, 480], bursts: o.bursts, seed: 1302 });
  // ceiling and luggage rack
  svg('rect', { x: XL, y: -200, width: XR - XL, height: 700, fill: lin(M.defs, [[0, '#2a1220'], [1, '#4a1e2c']]) }, M.s);
  for (let x = XL; x < XR; x += 90) svg('path', { d: `M${x},0 L${x + 45},480`, stroke: '#3a1626', 'stroke-width': 3 }, M.s);
  for (let k = 1; k <= NR; k++) { const x = ROW13(k); svg('rect', { x: x - 50, y: 380, width: 100, height: 22, rx: 11, fill: '#2a1a24', stroke: '#6a4a3a', 'stroke-width': 3 }, M.s); for (let j = 0; j < 4; j++) svg('rect', { x: x - 40 + j * 22, y: 386, width: 14, height: 10, rx: 3, fill: '#1a0e16' }, M.s); }
  svg('rect', { x: XL, y: 500, width: XR - XL, height: 100, fill: lin(M.defs, [[0, '#5a2a34'], [1, '#3a1a24']]) }, M.s);   // rack
  svg('rect', { x: XL, y: 590, width: XR - XL, height: 16, fill: '#2a1218' }, M.s);
  const led = svg('rect', { x: XL, y: 604, width: XR - XL, height: 7, fill: '#ffbf5a' }, M.s);
  svg('rect', { x: XL, y: 600, width: XR - XL, height: 60, fill: lin(M.defs, [[0, '#ffb04a', 0.45], [1, '#ffb04a', 0]]), style: 'mix-blend-mode:screen' }, M.s);
  // tinsel garland along the rack lip
  const tinsel = svg('g', {}, M.s);
  for (let x = XL; x < XR; x += 140) svg('path', { d: `M${x},592 Q${x + 70},640 ${x + 140},592`, fill: 'none', stroke: (x / 140) % 2 < 1 ? '#f2c14e' : '#e0453b', 'stroke-width': 9, 'stroke-dasharray': '3 4', 'stroke-linecap': 'round' }, tinsel);
  // side wall with window holes (the outside shows through)
  let wall = `M${XL},606 L${XR},606 L${XR},1180 L${XL},1180 Z`;
  const WIN = [];
  for (let k = 1; k <= NR; k++) { const x = ROW13(k), a = x - 108, b = x + 108; WIN.push([a, b]); wall += ` M${a + 24},640 L${b - 24},640 Q${b},640 ${b},664 L${b},1004 Q${b},1028 ${b - 24},1028 L${a + 24},1028 Q${a},1028 ${a},1004 L${a},664 Q${a},640 ${a + 24},640 Z`; }
  svg('path', { d: wall, fill: '#c9a47a', 'fill-rule': 'evenodd' }, M.s);
  svg('rect', { x: XL, y: 1028, width: XR - XL, height: 152, fill: '#a8805a' }, M.s);
  svg('rect', { x: XL, y: 1026, width: XR - XL, height: 6, fill: '#7a5636' }, M.s);
  // glass: a cool tint + diagonal reflection streaks on each window
  for (const [a, b] of WIN) {
    svg('rect', { x: a, y: 640, width: b - a, height: 388, rx: 24, fill: lin(M.defs, [[0, '#8fa8d8', 0.08], [1, '#2a1e40', 0.1]]) }, M.s);
    svg('path', { d: `M${a + 30},1020 L${a + 120},650 L${a + 150},650 L${a + 60},1020 Z M${a + 90},1020 L${a + 170},650 L${a + 180},650 L${a + 100},1020 Z`, fill: '#ffffff', opacity: 0.07 }, M.s);
    svg('rect', { x: a - 3, y: 637, width: b - a + 6, height: 394, rx: 26, fill: 'none', stroke: '#5a3a26', 'stroke-width': 7 }, M.s);
  }
  // curtains: gathered at the pillars, a scalloped valance with gold fringe
  for (const [a, b] of WIN) for (const [x, sg] of [[a, 1], [b, -1]]) {   // pleated curtains gathered at the pillars
    svg('path', { d: `M${x - sg * 8},636 L${x + sg * 20},636 Q${x + sg * 26},760 ${x + sg * 10},840 Q${x + sg * 22},940 ${x + sg * 16},1030 L${x - sg * 8},1030 Z`, fill: '#8e2a3c', stroke: INK, 'stroke-width': 3 }, M.s);
    svg('path', { d: `M${x + sg * 6},644 Q${x + sg * 10},760 ${x + sg * 4},1024`, fill: 'none', stroke: '#6a1c2a', 'stroke-width': 2.5 }, M.s);
    svg('ellipse', { cx: x + sg * 10, cy: 842, rx: 13, ry: 6, fill: '#e8b13a', stroke: INK, 'stroke-width': 2.5 }, M.s);   // tie-back
  }
  for (let x = XL; x < XR; x += 40) {   // a short valance with gold fringe
    svg('path', { d: `M${x},608 L${x + 40},608 L${x + 40},626 Q${x + 20},640 ${x},626 Z`, fill: '#8e2a3c', stroke: INK, 'stroke-width': 2 }, M.s);
    for (let j = 0; j < 4; j++) svg('path', { d: `M${x + 6 + j * 9},634 l0,9`, stroke: '#e8b13a', 'stroke-width': 2.6, 'stroke-linecap': 'round' }, M.s);
  }
  // front: bulkhead, windshield with the road ahead, dashboard clock, banner, TV
  const front = svg('g', {}, M.s);
  svg('rect', { x: XL, y: 300, width: 520, height: 1030, fill: '#3a1a24' }, front);
  const wsClip = uidS('ws'); const cp = svg('clipPath', { id: wsClip }, M.defs); svg('path', { d: 'M-230,430 L210,430 Q240,430 240,460 L240,1000 L-230,1000 Z' }, cp);
  const ws = svg('g', { 'clip-path': `url(#${wsClip})` }, front);
  svg('rect', { x: -240, y: 420, width: 500, height: 600, fill: lin(M.defs, [[0, '#1a1a44'], [0.6, '#4a2e62'], [1, '#c26a6a']]) }, ws);
  const wsFW = fireworks13(ws, M.defs, o.wsBursts || [], { seed: 9, riseH: 200 });
  svg('path', { d: 'M-240,880 L240,880 L240,1010 L-240,1010 Z', fill: '#1a1220' }, ws);
  svg('path', { d: 'M-10,880 L40,880 L240,1010 L-240,1010 Z', fill: '#2e2630' }, ws);   // road in perspective
  const dashes = Array.from({ length: 6 }, () => svg('path', { fill: '#ffe6a8' }, ws));
  for (const x of [-180, 140]) svg('circle', { cx: x, cy: 874, r: 6, fill: '#ffd59a' }, ws);
  svg('path', { d: 'M-230,430 L210,430 Q240,430 240,460 L240,1000 L-230,1000 Z', fill: 'none', stroke: '#1a0e14', 'stroke-width': 14 }, front);
  svg('path', { d: 'M-200,450 L-80,450 L-180,980 L-220,980 Z', fill: '#ffffff', opacity: 0.06 }, front);
  // dashboard + clock + mic clip, driver
  svg('path', { d: 'M-260,1000 L260,1000 L280,1060 L280,1180 L-260,1180 Z', fill: '#2a1e26', stroke: INK, 'stroke-width': 5 }, front);
  const clockG = svg('g', {}, front);
  svg('rect', { x: 120, y: 1018, width: 130, height: 54, rx: 8, fill: '#0d0e14', stroke: '#5a4a3a', 'stroke-width': 3 }, clockG);
  const clockT = wtext(clockG, 185, 1060, '23:59', 40, '#ffb34a', { w: 600, a: { 'font-family': 'Kanit', 'letter-spacing': 2 } });
  const micClip = svg('g', {}, front);
  svg('rect', { x: 262, y: 1000, width: 22, height: 40, rx: 6, fill: '#55586a', stroke: INK, 'stroke-width': 3 }, micClip);
  svg('rect', { x: -260, y: 1180, width: 540, height: 150, fill: '#241820' }, front);
  // the banner and the TV
  const ban = svg('g', {}, M.s);
  svg('path', { d: 'M-220,320 L240,320 L230,392 L-210,392 Z', fill: '#c8343c', stroke: INK, 'stroke-width': 4 }, ban);
  wtext(ban, 10, 370, 'สวัสดีปีใหม่ 2570', 44, '#ffe9a8', { w: 700 });
  for (const x of [-200, 220]) { svg('circle', { cx: x, cy: 356, r: 22, fill: '#f2c14e', stroke: INK, 'stroke-width': 3 }, ban); svg('path', { d: `M${x},378 l0,30`, stroke: '#f2c14e', 'stroke-width': 4 }, ban); }
  const tv = svg('g', {}, M.s), TX = 360, TY = 410;
  svg('rect', { x: TX - 6, y: 300, width: 12, height: TY - 300, fill: '#2a2228' }, tv);
  svg('rect', { x: TX - 100, y: TY, width: 200, height: 120, rx: 10, fill: '#15151c', stroke: INK, 'stroke-width': 5 }, tv);
  const tvScr = svg('rect', { x: TX - 90, y: TY + 10, width: 180, height: 100, rx: 4, fill: '#2a3a7a' }, tv);
  const tvTxt = wtext(tv, TX, TY + 78, '23:59', 46, '#ffe9a8', { w: 700 });
  const tvGlow = lightPool(M.s, M.defs, TX, TY + 60, 220, 140, '#8fb0ff', 0.18);
  // reading lights on a few rows, LED wash on the wall
  const reading = [];
  for (let k = 1; k <= NR; k++) if ([2, 4, 5, 7].includes(k)) reading.push(lampCone(M.s, M.defs, ROW13(k), 402, 150, 560, '#ffd59a', 0.1, false));
  lightPool(M.s, M.defs, (XL + XR) / 2, 640, (XR - XL) / 2, 120, '#ffb04a', 0.2);
  // floor (aisle carpet) with LED dots
  svg('rect', { x: XL, y: G, width: XR - XL, height: 900, fill: lin(M.defs, [[0, '#3a2030'], [1, '#1a0e18']]) }, M.s);
  for (let x = XL; x < XR; x += 60) svg('path', { d: `M${x},${G + 40} l30,18 l30,-18`, fill: 'none', stroke: '#4a2a3a', 'stroke-width': 3 }, M.s);
  const aisle = [];
  for (let x = XL + 20; x < XR; x += 120) aisle.push(svg('circle', { cx: x, cy: G + 16, r: 5, fill: '#ffb04a' }, M.s));
  // seats (behind the people) and the aisle-side armrests (in front of them)
  const seatC = o.seat || '#c98a2e', seatD = shade(seatC, -26);
  const seatPat = (() => { const id = uidS('sf'), pt = svg('pattern', { id, width: 24, height: 24, patternUnits: 'userSpaceOnUse' }, M.defs); svg('rect', { width: 24, height: 24, fill: seatC }, pt); svg('path', { d: 'M0,12 L12,0 L24,12 L12,24 Z', fill: 'none', stroke: seatD, 'stroke-width': 2, opacity: 0.6 }, pt); return `url(#${id})`; })();
  const seats = svg('g', {}, M.s);
  for (let k = 1; k <= NR; k++) {
    const x = ROW13(k);
    svg('path', { d: `M${x + 30},${SEAT13 + 10} L${x + 54},860 Q${x + 60},818 ${x + 96},822 L${x + 112},826 Q${x + 132},836 ${x + 124},880 L${x + 92},${SEAT13 + 20} Z`, fill: seatPat, stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, seats);
    svg('path', { d: `M${x + 54},866 Q${x + 58},818 ${x + 96},822 L${x + 112},826 Q${x + 134},836 ${x + 126},882 L${x + 120},910 L${x + 50},906 Z`, fill: '#f8f4ec', stroke: INK, 'stroke-width': 4 }, seats);   // headrest cover
    svg('path', { d: `M${x + 54},890 L${x + 122},894`, stroke: '#c8343c', 'stroke-width': 6 }, seats);
    svg('path', { d: `M${x - 80},${SEAT13} L${x + 70},${SEAT13} Q${x + 84},${SEAT13 + 4} ${x + 80},${SEAT13 + 40} L${x - 76},${SEAT13 + 40} Q${x - 92},${SEAT13 + 20} ${x - 80},${SEAT13} Z`, fill: seatPat, stroke: INK, 'stroke-width': 5 }, seats);
    svg('rect', { x: x - 10, y: SEAT13 + 40, width: 26, height: G - SEAT13 - 40, fill: '#2a2228' }, seats);
    svg('rect', { x: x - 70, y: G - 8, width: 150, height: 10, rx: 5, fill: '#2a2228' }, seats);
    svg('path', { d: `M${x - 120},${SEAT13 + 70} L${x - 60},${SEAT13 + 70}`, stroke: '#4a3a3a', 'stroke-width': 8, 'stroke-linecap': 'round' }, seats);   // footrest
  }
  const people = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, seats);
  const arms = svg('g', {}, M.s);
  for (let k = 1; k <= NR; k++) { const x = ROW13(k); svg('rect', { x: x - 30, y: SEAT13 - 34, width: 110, height: 20, rx: 10, fill: '#3a2a2e', stroke: INK, 'stroke-width': 4 }, arms); }
  const stand = svg('g', {}, M.s);
  const top = svg('g', {}, M.s);
  const sweep = lightSweep13(M.s, M.defs, [XL, 300, XR, 1500], { speed: 520, op: o.sweepOp ?? 0.22, w: 380 });
  const flash = svg('rect', { x: XL - 200, y: -300, width: XR - XL + 400, height: 2400, fill: '#ffd59a', opacity: 0, style: 'mix-blend-mode:screen' }, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 6, [XL, -60, XR, 500], ['#ffbf5a', '#ff9fc0', '#ffe9a8'], 1305, { rMin: 30, rMax: 80, op: 0.3 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 46%, rgba(10,4,16,.6) 100%)';
  return {
    people, stand, shadowL, top, arms, ground: G, seat: SEAT13, micClip, XL, XR,
    light: { ux: -0.2, uy: -0.98, lx: 600 },
    clock(s) { clockT.textContent = s; tvTxt.textContent = s; },
    update(t, o2 = {}) {
      out.update(t); wsFW.update(t); sweep(t); if (bok) bok(t);
      dashes.forEach((d, i) => { const u = ((t * 1.6 + i / 6) % 1), y = 884 + 130 * u * u, w = 2 + 10 * u, h = 4 + 26 * u; d.setAttribute('d', `M${(15 - w / 2).toFixed(1)},${y.toFixed(1)} l${w.toFixed(1)},0 l${(w * 0.3).toFixed(1)},${h.toFixed(1)} l${(-w * 1.6).toFixed(1)},0 Z`); });
      aisle.forEach((a, i) => a.setAttribute('opacity', (0.55 + 0.45 * Math.sin(t * 3 + i)).toFixed(2)));
      led.setAttribute('opacity', (0.85 + 0.15 * Math.sin(t * 5)).toFixed(2));
      tvScr.setAttribute('fill', o2.tvFlash ? '#ffd59a' : '#2a3a7a');
      const [fk, fc] = out.fw ? out.fw.flash(t) : [0, '#ffd59a'];
      const [wk, wc] = wsFW.flash(t);
      const k = Math.max(fk * 0.6, wk), c = wk > fk * 0.6 ? wc : fc;
      flash.setAttribute('fill', c); flash.setAttribute('opacity', (Math.min(0.28, k * 0.28) + (o2.flash || 0)).toFixed(3));
    },
  };
}

// ---------------- the bus (side view, facing left): burgundy and gold livery, lit windows, wheels ----------------
// x, y = front-bottom corner on the road; returns { g, update(t) }
function tourBus13(parent, defs, x, y, o = {}) {
  const g = svg('g', { transform: `translate(${x},${y}) scale(${o.s ?? 1})` }, parent), L = 1180, H = 470;
  svg('ellipse', { cx: L / 2, cy: 6, rx: L / 2 + 40, ry: 22, fill: '#000', opacity: 0.45 }, g);
  svg('path', { d: `M30,-40 L${L},-40 L${L},-${H} Q${L},-${H + 30} ${L - 40},-${H + 30} L90,-${H + 30} Q20,-${H + 30} 10,-${H - 40} L0,-120 Q0,-40 30,-40 Z`, fill: '#8e2a3c', stroke: INK, 'stroke-width': 7, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: `M4,-200 L${L},-200 L${L},-176 L2,-176 Z`, fill: '#e8b13a', stroke: INK, 'stroke-width': 4 }, g);   // gold stripe
  svg('path', { d: `M20,-120 Q160,-150 ${L},-118 L${L},-104 Q160,-136 18,-106 Z`, fill: '#f2c14e', opacity: 0.85 }, g);
  // windshield (two decks) and side windows with silhouettes
  svg('path', { d: `M14,-${H - 20} Q20,-${H + 20} 90,-${H + 18} L150,-${H + 18} L150,-280 L8,-280 Z`, fill: lin(defs, [[0, '#ffd59a'], [1, '#c87a4a']]), stroke: INK, 'stroke-width': 5 }, g);
  svg('path', { d: `M6,-262 L150,-262 L150,-214 L4,-214 Z`, fill: '#ffcf8a', stroke: INK, 'stroke-width': 5 }, g);
  const sil = rng(o.seed || 1311);
  for (const [wy, wh] of [[-(H + 4), 150], [-262, 52]]) for (let wx = 180; wx < L - 40; wx += 120) {
    svg('rect', { x: wx, y: wy, width: 104, height: wh, rx: 10, fill: '#ffd59a', stroke: INK, 'stroke-width': 4 }, g);
    if (wh > 100 && sil() > 0.25) { const hx = wx + 30 + sil() * 44; svg('circle', { cx: hx, cy: wy + 74, r: 22, fill: '#7a3a3a', opacity: 0.55 }, g); svg('rect', { x: hx - 26, y: wy + 94, width: 52, height: 60, rx: 18, fill: '#7a3a3a', opacity: 0.5 }, g); }
    svg('path', { d: `M${wx + 4},${wy + 8} q12,-6 24,0 l-2,${wh - 16} q-12,4 -22,0 Z M${wx + 100},${wy + 8} q-12,-6 -24,0 l2,${wh - 16} q12,4 22,0 Z`, fill: '#8e2a3c', opacity: 0.9 }, g);   // curtains
  }
  wtext(g, 640, -128, o.name || 'สายใยทัวร์', 56, '#fbe9b8', { w: 700 });
  svg('rect', { x: 2, y: -130, width: 30, height: 34, rx: 8, fill: '#fff6dc', stroke: INK, 'stroke-width': 4 }, g);   // headlight
  const beam = svg('path', { d: 'M4,-112 L-520,-220 L-520,40 Z', fill: lin(defs, [[0, '#fff2cc', 0.55], [1, '#fff2cc', 0]], -1, 0), style: 'mix-blend-mode:screen' }, g);
  svg('rect', { x: L - 26, y: -150, width: 22, height: 50, rx: 6, fill: '#e0453b', stroke: INK, 'stroke-width': 4 }, g);
  const wheels = [];
  for (const wx of [200, 860, 1010]) {
    svg('circle', { cx: wx, cy: -40, r: 66, fill: '#3a1a24' }, g);
    const w = svg('g', {}, g); wheels.push([w, wx]);
    svg('circle', { r: 56, fill: '#1e1a1e', stroke: INK, 'stroke-width': 5 }, w);
    svg('circle', { r: 28, fill: '#b8b2aa', stroke: INK, 'stroke-width': 4 }, w);
    for (let k = 0; k < 5; k++) svg('circle', { cx: Math.cos(k * 1.2566) * 15, cy: Math.sin(k * 1.2566) * 15, r: 4, fill: '#6a6460' }, w);
  }
  return { g, update(t) { wheels.forEach(([w, wx]) => w.setAttribute('transform', `translate(${wx},-40) rotate(${(-t * 520) % 360})`)); beam.setAttribute('opacity', (0.85 + 0.1 * Math.sin(t * 9)).toFixed(2)); } };
}
// the highway at night: the bus drives left through rice fields under fireworks over a distant town
function highway13(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = o.ground ?? 1560;
  svg('rect', { x: -1400, y: -2600, width: 3900, height: 4200, fill: lin(F.defs, [[0, '#0c0c2a'], [0.6, '#2a1e52'], [0.82, '#7a3a66'], [1, '#e08a6a']]) }, F.s);
  const r = rng(1321);
  for (let i = 0; i < 160; i++) svg('circle', { cx: -1200 + r() * 3500, cy: -2500 + r() * 3400, r: 0.8 + r() * 2, fill: '#fff6e8', opacity: 0.3 + r() * 0.6 }, F.s);
  svg('circle', { cx: 860, cy: 300, r: 140, fill: rad2(F.defs, [[0, '#fff2cc', 0.45], [1, '#fff2cc', 0]]) }, F.s);
  svg('circle', { cx: 860, cy: 300, r: 46, fill: '#fff4d8' }, F.s);
  const fw = fireworks13(F.s, F.defs, o.bursts || [], { seed: 5 });
  // distant town skyline with a temple spire, glowing
  const town = svg('g', {}, F.s);
  svg('path', { d: 'M-1400,1180 L2500,1180 L2500,1400 L-1400,1400 Z', fill: '#1a1430' }, town);
  for (let x = -1300; x < 2400; x += 40 + r() * 50) { const h = 20 + r() * 90; svg('rect', { x, y: 1180 - h, width: 30 + r() * 40, height: h, fill: '#1e1838' }, town); if (r() > 0.4) svg('rect', { x: x + 8, y: 1180 - h + 10, width: 5, height: 6, fill: '#ffd59a' }, town); }
  svg('path', { d: 'M300,1180 L300,1020 L316,960 L332,1020 L332,1180 Z', fill: '#1e1838' }, town);
  svg('rect', { x: -1400, y: 1140, width: 3900, height: 60, fill: lin(F.defs, [[0, '#ff9a5a', 0], [1, '#ff9a5a', 0.35]]) }, F.s);
  // rice fields (mid), guard rail and lamps rushing past, the road
  svg('rect', { x: -1400, y: 1200, width: 3900, height: G - 1200, fill: lin(M.defs, [[0, '#1e1a2e'], [1, '#2a2030']]) }, M.s);
  for (let y = 1230; y < G - 60; y += 34) svg('path', { d: `M-1400,${y} L2500,${y + 6}`, stroke: '#3a2e40', 'stroke-width': 3 }, M.s);
  const rush = svg('g', {}, M.s);
  for (let i = 0; i < 2; i++) for (let x = 0; x < 2600; x += 520) {
    const X = x + i * 2600;
    svg('rect', { x: X, y: G - 520, width: 10, height: 480, fill: '#1a1420' }, rush);
    svg('path', { d: `M${X + 5},${G - 516} q50,-26 92,0`, fill: 'none', stroke: '#1a1420', 'stroke-width': 9 }, rush);
    svg('circle', { cx: X + 96, cy: G - 506, r: 120, fill: rad2(M.defs, [[0, '#ffc070', 0.8], [0.3, '#ff9a40', 0.3], [1, '#ff9a40', 0]]), style: 'mix-blend-mode:screen' }, rush);
    svg('path', { d: `M${X + 96},${G - 500} L${X - 40},${G} L${X + 240},${G} Z`, fill: lin(M.defs, [[0, '#ffb060', 0.22], [1, '#ffb060', 0]]), style: 'mix-blend-mode:screen' }, rush);
  }
  const rail = svg('g', {}, M.s);
  for (let i = 0; i < 2; i++) { svg('rect', { x: i * 2600, y: G - 70, width: 2600, height: 16, fill: '#8a8070' }, rail); for (let x = 0; x < 2600; x += 130) svg('rect', { x: i * 2600 + x, y: G - 70, width: 10, height: 70, fill: '#6a6050' }, rail); }
  svg('rect', { x: -1400, y: G, width: 3900, height: 900, fill: lin(M.defs, [[0, '#2e2630'], [0.25, '#201a24'], [1, '#120e16']]) }, M.s);
  const lane = svg('g', {}, M.s);
  for (let i = 0; i < 2; i++) for (let x = 0; x < 2600; x += 260) svg('rect', { x: i * 2600 + x, y: G + 120, width: 140, height: 12, rx: 4, fill: '#f2d27a' }, lane);
  const bus = tourBus13(M.s, M.defs, o.busX ?? 120, G + 60, { s: o.busS ?? 0.8 });
  const people = svg('g', {}, M.s), top = svg('g', {}, M.s), shadowL = svg('g', {}, M.s);
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-200, G + 200, 1300, G + 500], ['#ffbf5a', '#ff9a40'], 1322, { rMin: 50, rMax: 110, op: 0.28 });
  const vg = html('div', '', S.fx); vg.style.cssText = 'position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 48%, rgba(10,4,16,.55) 100%)';
  return {
    people, top, shadowL, ground: G, bus, fw, light: { ux: -0.6, uy: -0.8, lx: 0 },
    update(t) {
      const sp = 700;
      rush.setAttribute('transform', `translate(${(((t * sp) % 2600) - 2600).toFixed(1)},0)`);
      rail.setAttribute('transform', `translate(${(((t * sp) % 2600) - 2600).toFixed(1)},0)`);
      lane.setAttribute('transform', `translate(${(((t * sp) % 2600) - 2600).toFixed(1)},0)`);
      town.setAttribute('transform', `translate(${((t * 18) % 400).toFixed(1)},0)`);
      bus.update(t); fw.update(t); if (bok) bok(t);
      bus.g.setAttribute('transform', `translate(${(o.busX ?? 120) + Math.sin(t * 1.3) * 3},${(G + 60 + Math.sin(t * 7) * 1.5).toFixed(1)}) scale(${o.busS ?? 0.8})`);
    },
  };
}

// ---------------- the bus terminal at night: platform 92 ----------------
function terminal13(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1400;
  // far: hall ceiling with warm lamps, the flip board, crowds
  svg('rect', { x: -500, y: -300, width: 2100, height: 1800, fill: lin(F.defs, [[0, '#2a1e3e'], [0.7, '#4a3050'], [1, '#6a4048']]) }, F.s);
  for (let x = -400; x < 1600; x += 260) { svg('rect', { x: x - 60, y: 120, width: 120, height: 14, rx: 7, fill: '#ffe2a8' }, F.s); lightPool(F.s, F.defs, x, 150, 160, 70, '#ffd59a', 0.4); }
  const board = svg('g', {}, F.s);
  svg('rect', { x: 120, y: 260, width: 840, height: 300, rx: 14, fill: '#0d0e14', stroke: '#5a4a3a', 'stroke-width': 6 }, board);
  wtext(board, 540, 316, 'เที่ยวรถออก · DEPARTURES', 34, '#ffe9a8', { w: 500 });
  const rows = [['22:00', 'ขอนแก่น', '88'], ['22:30', 'อุบลราชธานี', '92'], ['23:15', 'อุดรธานี', '95']];
  rows.forEach(([tm, to, pf], i) => {
    const y = 380 + i * 64;
    wtext(board, 230, y, tm, 40, '#ffb34a', { w: 600 }); wtext(board, 520, y, to, 40, '#ffb34a', { w: 600 }); wtext(board, 860, y, pf, 40, i === 1 ? '#6fe08f' : '#ffb34a', { w: 700 });
    svg('rect', { x: 150, y: y + 12, width: 780, height: 2, fill: '#2a2a34' }, board);
  });
  const crowd = svg('g', { opacity: 0.85 }, F.s), r = rng(1331);
  for (let i = 0; i < 26; i++) { const x = -300 + r() * 1700, h = 170 + r() * 60; svg('circle', { cx: x, cy: 1180 - h, r: 26, fill: '#3a2a40' }, crowd); svg('rect', { x: x - 30, y: 1180 - h + 22, width: 60, height: h - 30, rx: 22, fill: '#3a2a40' }, crowd); if (r() > 0.6) svg('rect', { x: x + 30, y: 1120, width: 40, height: 56, rx: 6, fill: '#4a3048' }, crowd); }
  // New Year lanterns across the hall
  const lant = svg('g', {}, F.s);
  svg('path', { d: 'M-400,40 Q540,160 1500,40', fill: 'none', stroke: '#2a1a24', 'stroke-width': 4 }, lant);
  for (let i = 0; i < 12; i++) { const u = i / 11, x = -400 + u * 1900, y = 40 + Math.sin(u * Math.PI) * 60; svg('path', { d: `M${x},${y} l0,20`, stroke: '#2a1a24', 'stroke-width': 3 }, lant); svg('ellipse', { cx: x, cy: y + 44, rx: 24, ry: 28, fill: i % 2 ? '#e0453b' : '#f2c14e', stroke: INK, 'stroke-width': 3 }, lant); }
  // mid: platform, bay pillar, the bus front at bay 92, the big pillar
  svg('rect', { x: -500, y: 1180, width: 2100, height: G - 1180, fill: '#3a2e3a' }, M.s);
  const bus = svg('g', {}, M.s);
  svg('path', { d: 'M560,1400 L560,700 Q560,640 620,640 L1100,640 L1100,1400 Z', fill: '#8e2a3c', stroke: INK, 'stroke-width': 7 }, bus);
  svg('path', { d: 'M600,700 Q600,676 624,676 L1100,676 L1100,980 L600,980 Z', fill: lin(M.defs, [[0, '#ffd59a'], [1, '#c87a4a']]), stroke: INK, 'stroke-width': 5 }, bus);
  svg('rect', { x: 560, y: 1080, width: 540, height: 26, fill: '#e8b13a', stroke: INK, 'stroke-width': 4 }, bus);
  wtext(bus, 910, 1040, 'อุบลราชธานี', 46, '#ffe9a8', { w: 700 });
  svg('rect', { x: 620, y: 1220, width: 120, height: 50, rx: 10, fill: '#fff6dc', stroke: INK, 'stroke-width': 4 }, bus);
  svg('rect', { x: 960, y: 1220, width: 120, height: 50, rx: 10, fill: '#fff6dc', stroke: INK, 'stroke-width': 4 }, bus);
  svg('path', { d: 'M850,1400 A90,90 0 0 1 1030,1400 Z', fill: '#2a1218' }, bus); svg('circle', { cx: 940, cy: 1400, r: 70, fill: '#1e1a1e', stroke: INK, 'stroke-width': 5 }, bus); svg('circle', { cx: 940, cy: 1400, r: 32, fill: '#b8b2aa', stroke: INK, 'stroke-width': 4 }, bus);
  const door = svg('g', {}, bus);
  svg('rect', { x: 600, y: 1106, width: 120, height: 294, fill: '#7a3a2a', stroke: INK, 'stroke-width': 5 }, door);
  svg('rect', { x: 612, y: 1120, width: 96, height: 120, rx: 8, fill: '#ffcf8a', stroke: INK, 'stroke-width': 3 }, door);
  for (let k = 0; k < 3; k++) svg('rect', { x: 600, y: 1280 + k * 40, width: 120, height: 8, fill: '#c8343c' }, door);
  const bay = svg('g', {}, M.s);
  svg('rect', { x: 400, y: 640, width: 110, height: 70, rx: 10, fill: '#f2c14e', stroke: INK, 'stroke-width': 5 }, bay);
  wtext(bay, 455, 692, '92', 46, '#2a1a24', { w: 800 });
  svg('rect', { x: 446, y: 710, width: 18, height: 690, fill: '#6a5a6a' }, bay);
  svg('rect', { x: -500, y: G, width: 2100, height: 900, fill: lin(M.defs, [[0, '#4a3a42'], [1, '#1e1620']]) }, M.s);
  svg('rect', { x: -500, y: G + 30, width: 2100, height: 14, fill: '#f2c14e' }, M.s);   // platform edge line
  for (let x = -500; x < 1600; x += 80) svg('rect', { x, y: G + 30, width: 40, height: 14, fill: '#2a2228' }, M.s);
  // the big pillar the daughter hides behind (left), a food cart (right)
  const pillar = svg('g', {}, M.s);
  svg('rect', { x: 40, y: 300, width: 200, height: G - 300, fill: lin(M.defs, [[0, '#8a7a7a'], [0.5, '#b0a09a'], [1, '#7a6a6a']], 1, 0), stroke: INK, 'stroke-width': 6 }, pillar);
  svg('rect', { x: 60, y: 760, width: 160, height: 220, rx: 8, fill: '#f6efe2', stroke: INK, 'stroke-width': 4 }, pillar);
  wtext(pillar, 140, 826, 'สวัสดี', 40, '#c8343c', { w: 700 }); wtext(pillar, 140, 880, 'ปีใหม่', 40, '#c8343c', { w: 700 }); wtext(pillar, 140, 940, '2570', 40, '#e8b13a', { w: 800 });
  const cart = svg('g', {}, M.s);
  svg('rect', { x: 1110, y: 1180, width: 220, height: 160, rx: 10, fill: '#e0453b', stroke: INK, 'stroke-width': 5 }, cart);
  svg('rect', { x: 1100, y: 1100, width: 240, height: 30, fill: '#f2c14e', stroke: INK, 'stroke-width': 4 }, cart);
  for (let k = 0; k < 4; k++) svg('ellipse', { cx: 1140 + k * 50, cy: 1170, rx: 20, ry: 12, fill: '#c87a3a', stroke: INK, 'stroke-width': 3 }, cart);
  svg('circle', { cx: 1150, cy: 1350, r: 26, fill: '#2a2228' }, cart); svg('circle', { cx: 1290, cy: 1350, r: 26, fill: '#2a2228' }, cart);
  wallAO(M.s, M.defs, 1180, { op: 0.25 });
  lightPool(M.s, M.defs, 540, G, 700, 90, '#ffd59a', 0.3);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, pillar);
  const people = svg('g', {}, M.s), front = svg('g', {}, M.s), top = svg('g', {}, M.s);
  const pillarFront = svg('g', {}, M.s);   // a copy of the pillar's edge to hide behind
  svg('rect', { x: 40, y: 300, width: 200, height: G - 300, fill: lin(M.defs, [[0, '#8a7a7a'], [0.5, '#b0a09a'], [1, '#7a6a6a']], 1, 0), stroke: INK, 'stroke-width': 6 }, pillarFront);
  svg('rect', { x: 60, y: 760, width: 160, height: 220, rx: 8, fill: '#f6efe2', stroke: INK, 'stroke-width': 4 }, pillarFront);
  wtext(pillarFront, 140, 826, 'สวัสดี', 40, '#c8343c', { w: 700 }); wtext(pillarFront, 140, 880, 'ปีใหม่', 40, '#c8343c', { w: 700 }); wtext(pillarFront, 140, 940, '2570', 40, '#e8b13a', { w: 800 });
  pillarFront.setAttribute('display', 'none');
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 7, [-200, -60, 1280, 500], ['#ffd59a', '#e0453b', '#f2c14e'], 1332, { rMin: 40, rMax: 90, op: 0.32 });
  vignette(M.s, M.defs, 0.5);
  const band = html('div', '', S.fx); band.style.cssText = 'position:absolute;left:0;right:0;top:1440px;height:480px;background:linear-gradient(180deg, rgba(20,10,18,0), rgba(20,10,18,.7) 45%, rgba(20,10,18,.85))';
  return {
    people, front, top, shadowL, ground: G, pillarFront, light: { ux: 0.2, uy: -0.98, lx: 540 },
    update(t) { crowd.setAttribute('transform', `translate(${(Math.sin(t * 0.4) * 30).toFixed(1)},0)`); if (bok) bok(t); },
  };
}

// ---------------- ยาย's Isan house on New Year's Eve ----------------
function isanHome13(S, o = {}) {
  const F = S.L.far, M = S.L.mid, R = S.L.fore, G = 1300;
  // teak plank wall, window with the village night + fireworks, photo of แม่ in uniform, calendar, string lights
  svg('rect', { x: -300, y: -300, width: 1680, height: 1610, fill: '#8a5230' }, F.s);
  for (let x = -300; x < 1400; x += 64) svg('rect', { x, y: -300, width: 4, height: 1610, fill: '#6a3a20', opacity: 0.8 }, F.s);
  const WX = 600, WY = 330, WW = 400, WH = 430;
  const nclip = uidS('hw'); const cp = svg('clipPath', { id: nclip }, F.defs); svg('rect', { x: WX, y: WY, width: WW, height: WH }, cp);
  const view = svg('g', { 'clip-path': `url(#${nclip})` }, F.s);
  svg('rect', { x: WX, y: WY, width: WW, height: WH, fill: lin(F.defs, [[0, '#14143a'], [0.7, '#3a2a5e'], [1, '#7a4a66']]) }, view);
  const fw = fireworks13(view, F.defs, o.bursts || [], { seed: 11, riseH: 160 });
  svg('path', { d: `M${WX},${WY + WH - 60} q60,-50 120,-10 q60,-60 140,-20 q80,-40 140,10 L${WX + WW},${WY + WH} L${WX},${WY + WH} Z`, fill: '#0e0a18' }, view);
  svg('rect', { x: WX - 16, y: WY - 16, width: WW + 32, height: WH + 32, fill: 'none', stroke: '#5a3018', 'stroke-width': 18 }, F.s);
  svg('rect', { x: WX + WW / 2 - 6, y: WY, width: 12, height: WH, fill: '#5a3018' }, F.s);
  for (let k = 1; k < 4; k++) svg('rect', { x: WX, y: WY + k * WH / 4, width: WW, height: 3, fill: '#5a3018', opacity: 0.5 }, F.s);
  for (const [x, sg] of [[WX - 30, 1], [WX + WW + 30, -1]]) svg('path', { d: `M${x - 40},${WY - 30} L${x + 40},${WY - 30} L${x + 30 + sg * 16},${WY + WH + 30} L${x - 30 + sg * 16},${WY + WH + 30} Z`, fill: '#e8b13a', stroke: INK, 'stroke-width': 4, opacity: 0.95 }, F.s);
  const fairy = lightString(F.s, WX - 80, WX + WW + 80, WY - 40, 30, ['#ffd66b', '#ff9fc0', '#fff1c4', '#9fe0ff'], 14);
  const ph = svg('g', {}, F.s);   // แม่'s photo in her uniform
  svg('rect', { x: 230, y: 380, width: 200, height: 240, rx: 8, fill: '#c8a050', stroke: INK, 'stroke-width': 5 }, ph);
  svg('rect', { x: 246, y: 396, width: 168, height: 208, fill: '#fde6c8' }, ph);
  svg('path', { d: 'M260,604 C262,540 398,540 400,604 Z', fill: MAE13.shirt, stroke: INK, 'stroke-width': 3 }, ph);
  svg('path', { d: 'M318,560 L342,560 L330,590 Z', fill: '#fbf6ee' }, ph);
  faceMae13(ph, 330, 500, 46);
  const cal = svg('g', {}, F.s);
  svg('rect', { x: 60, y: 420, width: 130, height: 170, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4 }, cal);
  svg('rect', { x: 60, y: 420, width: 130, height: 44, fill: '#c8343c' }, cal);
  wtext(cal, 125, 452, 'ธ.ค.', 30, '#fbf2e2');
  wtext(cal, 125, 560, '31', 74, '#2a1a24', { w: 800 });
  wallClock(F.s, 470, 250, 40, '#c8a050')(23.98);
  wallShelf(F.s, 40, 700, 200, '#6a3a1e');   // a shelf: radio, a little plant, a jasmine garland
  svg('rect', { x: 60, y: 640, width: 90, height: 60, rx: 10, fill: '#c8343c', stroke: INK, 'stroke-width': 4 }, F.s);
  svg('circle', { cx: 86, cy: 670, r: 16, fill: '#3a2a2a', stroke: INK, 'stroke-width': 3 }, F.s); svg('path', { d: 'M110,656 L140,656 M110,668 L140,668 M110,680 L140,680', stroke: '#fbe9b8', 'stroke-width': 3 }, F.s);
  tinyCactus(F.s, 190, 700, '#c8a050');
  for (let k = 0; k < 9; k++) svg('circle', { cx: 300 + Math.sin(k * 0.7) * 26, cy: 660 + k * 12, r: 7, fill: '#fbf7ef', stroke: '#c9b89a', 'stroke-width': 1.5 }, F.s);
  svg('path', { d: 'M286,760 L300,800 L314,760 Z', fill: '#e0453b' }, F.s);
  // floor mat, low table (ขันโตก) with food, TV cabinet, the covered plate for แม่, cushions
  svg('rect', { x: -300, y: G, width: 1680, height: 900, fill: lin(M.defs, [[0, '#5a3020'], [1, '#2a140c']]) }, M.s);
  for (let y = G + 20, k = 0; y < 2200; y += 46 + k * 8, k++) svg('rect', { x: -300, y, width: 1680, height: 3, fill: '#2a120a', opacity: 0.6 }, M.s);
  svg('path', { d: 'M40,1360 L1040,1360 L1080,1560 L0,1560 Z', fill: '#7a3a5a', stroke: INK, 'stroke-width': 5 }, M.s);   // เสื่อ
  for (let k = 1; k < 10; k++) svg('path', { d: `M${40 + k * 100},1360 L${k * 108},1560`, stroke: '#9a5a7a', 'stroke-width': 4 }, M.s);
  wallAO(M.s, M.defs, G, { op: 0.32 });
  const tv = svg('g', {}, M.s);
  svg('rect', { x: 690, y: 1050, width: 240, height: 250, fill: '#6a3a1e', stroke: INK, 'stroke-width': 5 }, tv);
  svg('rect', { x: 696, y: 870, width: 228, height: 170, rx: 12, fill: '#1a1a22', stroke: INK, 'stroke-width': 5 }, tv);
  const tvScr = svg('rect', { x: 708, y: 882, width: 204, height: 136, rx: 6, fill: '#2a3a7a' }, tv);
  const tvNum = wtext(tv, 810, 976, '10', 76, '#ffe9a8', { w: 800 });
  const tvFW = fireworks13(tv, M.defs, (o.tvBursts || []), { seed: 13, riseH: 40, grav: 30 });
  const tvGlow = lightPool(M.s, M.defs, 810, 960, 340, 260, '#8fb0ff', 0.22);
  const table = svg('g', {}, M.s);
  svg('ellipse', { cx: 420, cy: 1300, rx: 230, ry: 34, fill: '#8a5a2a', stroke: INK, 'stroke-width': 5 }, table);
  svg('path', { d: 'M230,1300 L250,1352 L590,1352 L610,1300', fill: '#6a3a1a', stroke: INK, 'stroke-width': 5 }, table);
  const kratip = svg('g', {}, table);   // sticky rice basket
  svg('path', { d: 'M290,1290 L280,1220 Q310,1196 340,1220 L330,1290 Z', fill: '#d9a85a', stroke: INK, 'stroke-width': 4 }, kratip);
  for (let k = 0; k < 4; k++) svg('path', { d: `M284,${1232 + k * 15} L336,${1232 + k * 15}`, stroke: '#a8783a', 'stroke-width': 2.5 }, kratip);
  svg('ellipse', { cx: 410, cy: 1288, rx: 54, ry: 16, fill: '#f6efe2', stroke: INK, 'stroke-width': 4 }, table);   // som tam
  svg('path', { d: 'M372,1284 q20,-14 40,-2 q20,-14 36,2', fill: '#f2a03a', stroke: '#7fb069', 'stroke-width': 4 }, table);
  svg('ellipse', { cx: 500, cy: 1290, rx: 46, ry: 14, fill: '#f6efe2', stroke: INK, 'stroke-width': 4 }, table);   // grilled chicken
  svg('path', { d: 'M470,1284 q30,-24 60,0', fill: '#b85a2a', stroke: INK, 'stroke-width': 3 }, table);
  // แม่'s place: a cushion and her plate under a pink ฝาชี with a note
  const mae = svg('g', {}, M.s);
  svg('path', { d: 'M560,1330 L700,1330 L690,1290 L570,1290 Z', fill: '#c8343c', stroke: INK, 'stroke-width': 4 }, mae);
  svg('path', { d: 'M640,1290 L700,1290 L670,1240 Z', fill: '#e8b13a', stroke: INK, 'stroke-width': 4 }, mae);   // หมอนขิด
  svg('ellipse', { cx: 560, cy: 1278, rx: 52, ry: 12, fill: '#f6efe2', stroke: INK, 'stroke-width': 3 }, mae);
  const cover = svg('path', { d: 'M506,1276 Q506,1206 560,1204 Q614,1206 614,1276 Z', fill: '#f07aa8', 'fill-opacity': 0.75, stroke: INK, 'stroke-width': 4 }, mae);
  for (let k = 0; k < 5; k++) svg('path', { d: `M${516 + k * 22},1274 Q${520 + k * 20},1220 560,1208`, fill: 'none', stroke: '#c84a7a', 'stroke-width': 2 }, mae);
  svg('circle', { cx: 560, cy: 1200, r: 7, fill: '#c84a7a', stroke: INK, 'stroke-width': 2.5 }, mae);
  const note = svg('g', { transform: 'translate(596,1236) rotate(8)' }, mae);
  svg('rect', { x: -2, y: -16, width: 66, height: 34, rx: 3, fill: '#fff6a8', stroke: INK, 'stroke-width': 2.5 }, note);
  wtext(note, 31, 8, 'ของแม่', 20, '#c8343c', { w: 700 });
  svg('path', { d: 'M150,1330 L290,1330 L280,1292 L160,1292 Z', fill: '#7a3f8e', stroke: INK, 'stroke-width': 4 }, M.s);   // ยาย's cushion
  sleepyCat(M.s, 1040, 1330, 0.8, '#e8a050');
  pottedPlant(M.s, -10, 1300, 0.6, 'snake', '#c8a050');
  lightPool(M.s, M.defs, 420, 1180, 380, 160, '#ffd59a', 0.35);
  const people = svg('g', {}, M.s), top = svg('g', {}, M.s);
  const shadowL = svg('g', {}, M.s); M.s.insertBefore(shadowL, table);
  M.s.insertBefore(people, table);   // they sit behind the low table
  let bok = null;
  if (R) bok = bokehField(R.s, R.defs, 5, [-100, -60, 1180, 300], ['#ffd66b', '#ff9fc0'], 1341, { rMin: 40, rMax: 90, op: 0.3 });
  vignette(M.s, M.defs, 0.55);
  return {
    people, top, shadowL, ground: G, cover, fw, light: { ux: 0.85, uy: -0.45, lx: 960 },
    tv(n, flash = 0) { tvNum.textContent = n; tvScr.setAttribute('fill', flash ? '#3a2a6a' : '#2a3a7a'); },
    update(t) { fw.update(t); tvFW.update(t); fairy.forEach((b, i) => b.setAttribute('opacity', (0.7 + 0.3 * Math.sin(t * 2.6 + i * 1.7)).toFixed(2))); if (bok) bok(t); },
  };
}
