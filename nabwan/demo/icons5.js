// v6 animated icon set: sticker style (white outline under glossy gradient fills, soft drop shadow),
// squash-and-stretch entrances and a looping idle motion per icon. Each builder returns { el, update(t, ...) }.

function iconBox(parent, w, h, vb, cls = '') {
  const d = html('div', 'ic5 ' + cls, parent);
  d.style.width = w + 'px'; d.style.height = h + 'px';
  const s = svg('svg', { width: w, height: h, viewBox: vb || `0 0 ${w} ${h}`, style: 'overflow:visible' }, d);
  return { d, s, defs: svg('defs', {}, s) };
}
const STK = { stroke: '#fff', 'stroke-width': 5, 'paint-order': 'stroke', 'stroke-linejoin': 'round' };
const withStk = (o, w = 5) => Object.assign({}, STK, { 'stroke-width': w }, o);

// squash & stretch pop: overshoot scale, a wobble that squashes then stretches, slight spin-in
function popSquash(el, t, t0, extra = '', rot0 = -18) {
  const k = spring(t, t0, 16, 6.5), x = t - t0;
  const sq = x > 0 ? Math.exp(-x * 7) * Math.sin(x * 26) * 0.22 : 0;
  el.style.opacity = fadeIn(t, t0, 0.08).toFixed(3);
  el.style.transform = `${extra} rotate(${((1 - clamp(k)) * rot0 + sq * 14).toFixed(2)}deg) scale(${Math.max(0.001, k * (1 + sq)).toFixed(3)}, ${Math.max(0.001, k * (1 - sq)).toFixed(3)})`;
  return k;
}
const fourStar = r => `M0,${-r} Q${r * 0.18},${-r * 0.18} ${r},0 Q${r * 0.18},${r * 0.18} 0,${r} Q${-r * 0.18},${r * 0.18} ${-r},0 Q${-r * 0.18},${-r * 0.18} 0,${-r} Z`;

// ---------------- analog clock with crescent moon and twinkling stars ----------------
function clockMoon(parent, size = 80, night = true) {
  const b = iconBox(parent, size, size, '0 0 100 100');
  const g = svg('g', {}, b.s);
  svg('circle', withStk({ cx: 48, cy: 54, r: 38, fill: rad2(b.defs, [[0, night ? '#4253a6' : '#ffffff'], [1, night ? '#161c46' : '#e9eef8']], { cx: 0.35, cy: 0.3, r: 0.8 }) }, 6), g);
  svg('circle', { cx: 48, cy: 54, r: 38, fill: 'none', stroke: '#f2c14e', 'stroke-width': 4 }, g);
  for (let i = 0; i < 12; i++) {
    const a = rad(i * 30), r0 = i % 3 ? 31 : 27;
    svg('line', { x1: 48 + Math.sin(a) * r0, y1: 54 - Math.cos(a) * r0, x2: 48 + Math.sin(a) * 34, y2: 54 - Math.cos(a) * 34, stroke: night ? '#cfd6ff' : '#5a6380', 'stroke-width': i % 3 ? 2 : 3.5, 'stroke-linecap': 'round', opacity: 0.85 }, g);
  }
  const hr = svg('line', { x1: 48, y1: 54, x2: 48, y2: 37, stroke: '#f2c14e', 'stroke-width': 5.5, 'stroke-linecap': 'round' }, g);
  const mn = svg('line', { x1: 48, y1: 54, x2: 48, y2: 28, stroke: night ? '#ffffff' : '#2b3157', 'stroke-width': 3.6, 'stroke-linecap': 'round' }, g);
  const sc = svg('line', { x1: 48, y1: 60, x2: 48, y2: 25, stroke: '#ff6b6b', 'stroke-width': 1.8, 'stroke-linecap': 'round' }, g);
  svg('circle', { cx: 48, cy: 54, r: 4.5, fill: '#f2c14e', stroke: '#fff', 'stroke-width': 1.5 }, g);
  svg('path', { d: 'M24,30 A30,30 0 0 1 52,20', stroke: '#fff', 'stroke-width': 4, fill: 'none', opacity: 0.35, 'stroke-linecap': 'round' }, g);
  // crescent moon via mask + stars
  const mk = svg('mask', { id: uidS('mm') }, b.defs);
  svg('rect', { x: 60, y: -10, width: 50, height: 50, fill: '#fff' }, mk);
  svg('circle', { cx: 92, cy: 6, r: 12, fill: '#000' }, mk);
  const moon = svg('g', {}, b.s);
  svg('circle', withStk({ cx: 84, cy: 14, r: 14, fill: '#f6d77a', mask: `url(#${mk.id})` }, 4), moon);
  const stars = [[12, 14, 6], [96, 44, 5], [66, 0, 4]].map(([x, y, r]) => ({ el: svg('path', { d: fourStar(r), fill: '#fff6c8', transform: `translate(${x},${y})` }, b.s), x, y }));
  return {
    el: b.d,
    update(t, hours, minutes, seconds = null) {
      const m = minutes, h = (hours % 12) + m / 60;
      hr.setAttribute('transform', `rotate(${(h * 30).toFixed(2)} 48 54)`);
      mn.setAttribute('transform', `rotate(${(m * 6).toFixed(2)} 48 54)`);
      const s = seconds == null ? Math.floor(t * 2) * 6 * 2 : seconds * 6;   // ticks twice a second
      sc.setAttribute('transform', `rotate(${s.toFixed(1)} 48 54)`);
      moon.setAttribute('transform', `rotate(${(Math.sin(t * 1.6) * 8).toFixed(2)} 84 14)`);
      stars.forEach((st, i) => { const k = 0.55 + 0.45 * Math.sin(t * 4 + i * 2.1); st.el.setAttribute('transform', `translate(${st.x},${st.y}) scale(${k.toFixed(3)}) rotate(${(t * 40 + i * 30).toFixed(1)})`); st.el.setAttribute('opacity', (0.4 + 0.6 * k).toFixed(3)); });
    },
  };
}

// ---------------- low battery: shakes on arrival, red level blinks, plug bolt flickers ----------------
function batteryIcon(parent) {
  const b = iconBox(parent, 64, 34, '0 0 64 34');
  const g = svg('g', {}, b.s);
  svg('rect', { x: 2, y: 4, width: 50, height: 26, rx: 8, fill: 'rgba(255,255,255,.08)', stroke: '#fff', 'stroke-width': 3 }, g);
  svg('rect', { x: 54, y: 12, width: 6, height: 10, rx: 2.5, fill: '#fff' }, g);
  const lvl = svg('rect', { x: 6, y: 8, width: 6, height: 18, rx: 4, fill: '#ff5e52' }, g);
  const glow = svg('rect', { x: 2, y: 4, width: 50, height: 26, rx: 8, fill: 'none', stroke: '#ff5e52', 'stroke-width': 3, opacity: 0 }, g);
  const bolt = svg('path', { d: 'M30,8 L22,19 L28,19 L25,27 L34,15 L28,15 Z', fill: '#ffd166' }, g);
  return {
    el: b.d,
    update(t, t0) {
      const x = t - t0;
      const shake = x > 0 && x < 0.6 ? Math.sin(x * 60) * 3 * (1 - x / 0.6) : 0;
      g.setAttribute('transform', `translate(${shake.toFixed(2)},0)`);
      const blink = Math.sin(t * 7) > 0 ? 1 : 0.25;
      lvl.setAttribute('opacity', blink);
      glow.setAttribute('opacity', (0.6 * Math.max(0, Math.sin(t * 3.5))).toFixed(3));
      bolt.setAttribute('opacity', (Math.sin(t * 11) > 0.2 ? 0.95 : 0.15).toFixed(2));
    },
  };
}

// ---------------- "typing…" dots ----------------
function typingDots(parent) {
  const d = html('span', 'typing5', parent);
  const dots = [0, 1, 2].map(() => html('i', '', d));
  return { el: d, update(t, on) { d.style.display = on ? 'inline-flex' : 'none'; dots.forEach((e, i) => { const k = Math.max(0, Math.sin(t * 12 - i * 0.9)); e.style.transform = `translateY(${(-k * 9).toFixed(1)}px)`; e.style.opacity = (0.45 + 0.55 * k).toFixed(2); }); } };
}

// ---------------- heart that beats lub-dub and lets small hearts float away ----------------
function heartBeat(parent, size = 34, color = '#e0577a') {
  const b = iconBox(parent, size, size, '-20 -20 40 40');
  const g = svg('g', {}, b.s);
  svg('path', withStk({ d: heartPath(0, 0, 12), fill: lin(b.defs, [[0, shade(color, 35)], [1, color]]) }, 3.5), g);
  svg('ellipse', { cx: -6, cy: -6, rx: 3.2, ry: 2, fill: '#fff', opacity: 0.6, transform: 'rotate(-35 -6 -6)' }, g);
  const minis = [0, 1, 2].map(() => svg('path', { d: heartPath(0, 0, 4.5), fill: color }, b.s));
  return {
    el: b.d,
    update(t) {
      const p = (t % 0.9) / 0.9;
      const beat = 1 + 0.16 * Math.exp(-Math.pow((p - 0.08) * 18, 2)) + 0.1 * Math.exp(-Math.pow((p - 0.3) * 18, 2));
      g.setAttribute('transform', `scale(${beat.toFixed(3)})`);
      minis.forEach((m, i) => { const q = ((t * 0.7 + i / 3) % 1); setA(m, { transform: `translate(${(Math.sin(q * 9 + i) * 8 + (i - 1) * 9).toFixed(1)},${(-12 - q * 34).toFixed(1)}) scale(${(1 - q * 0.5).toFixed(2)})`, opacity: (q < 0.15 ? q / 0.15 : 1 - q).toFixed(2) }); });
    },
  };
}

// ---------------- little house with lit window, heart vent and curling chimney smoke ----------------
function houseIcon(parent, size = 56) {
  const b = iconBox(parent, size, size, '0 0 100 100');
  const smoke = [0, 1, 2].map(() => svg('circle', { r: 6, fill: '#ffffff' }, b.s));
  const g = svg('g', {}, b.s);
  svg('rect', withStk({ x: 63, y: 18, width: 12, height: 22, rx: 2, fill: '#b5523b' }, 5), g);
  svg('rect', withStk({ x: 20, y: 44, width: 60, height: 46, rx: 6, fill: lin(b.defs, [[0, '#fff5e2'], [1, '#f0d7b0']]) }, 6), g);
  svg('path', withStk({ d: 'M8,50 L50,13 L92,50 Z', fill: lin(b.defs, [[0, '#ef6a5a'], [1, '#c23b30']]) }, 6), g);
  svg('path', { d: 'M24,42 L50,20', stroke: '#fff', 'stroke-width': 3.5, opacity: 0.4, 'stroke-linecap': 'round' }, g);
  const win = svg('rect', { x: 27, y: 56, width: 16, height: 15, rx: 3, fill: '#ffd56b' }, g);
  svg('path', { d: 'M35,56 L35,71 M27,63.5 L43,63.5', stroke: '#c48a3a', 'stroke-width': 2 }, g);
  svg('rect', { x: 52, y: 62, width: 16, height: 28, rx: 4, fill: '#8a5a34' }, g);
  svg('circle', { cx: 64, cy: 77, r: 1.8, fill: '#f2c14e' }, g);
  svg('circle', { cx: 50, cy: 36, r: 7, fill: '#fff5e2' }, g);
  svg('path', { d: heartPath(50, 36.5, 4.2), fill: '#e0577a' }, g);
  return {
    el: b.d,
    update(t) {
      win.setAttribute('fill', Math.sin(t * 9) > 0.92 ? '#fff0b0' : '#ffd56b');
      smoke.forEach((c, i) => { const q = ((t * 0.55 + i / 3) % 1); setA(c, { cx: (69 + Math.sin(q * 6 + i) * 6 + q * 10).toFixed(1), cy: (14 - q * 34).toFixed(1), r: (4 + q * 9).toFixed(1), opacity: (0.75 * (q < 0.15 ? q / 0.15 : 1 - q)).toFixed(2) }); });
    },
  };
}

// ---------------- city tower (Bangkok) ----------------
function buildingIcon(parent, size = 44, tone = '#7c9fc9') {
  const b = iconBox(parent, size, size, '0 0 100 100');
  const g = svg('g', {}, b.s);
  svg('rect', withStk({ x: 14, y: 40, width: 30, height: 52, rx: 4, fill: shade(tone, -25) }, 6), g);
  svg('rect', withStk({ x: 40, y: 12, width: 40, height: 80, rx: 5, fill: lin(b.defs, [[0, shade(tone, 25)], [1, tone]]) }, 6), g);
  svg('rect', { x: 57, y: 2, width: 6, height: 12, fill: shade(tone, -30) }, g);
  const lights = [];
  for (let r = 0; r < 6; r++) for (let c = 0; c < 3; c++) lights.push(svg('rect', { x: 47 + c * 10, y: 20 + r * 11, width: 6, height: 6, rx: 1.2, fill: '#fff3c4' }, g));
  return { el: b.d, update(t) { lights.forEach((l, i) => l.setAttribute('opacity', Math.sin(t * 1.3 + i * 2.7) > -0.3 ? 0.95 : 0.25)); } };
}

// ---------------- 3D map pin: drops in, squashes on landing, ripple ring ----------------
function pin3D(parent, color, inner) {
  const b = iconBox(parent, 64, 86, '-32 -78 64 86');
  const ring = svg('ellipse', { cx: 0, cy: 2, rx: 6, ry: 2, fill: 'none', stroke: color, 'stroke-width': 3 }, b.s);
  const sh = svg('ellipse', { cx: 0, cy: 3, rx: 12, ry: 4, fill: '#000', opacity: 0.25 }, b.s);
  const g = svg('g', {}, b.s);
  svg('path', withStk({ d: 'M0,0 C-8,-18 -26,-28 -26,-46 A26,26 0 1 1 26,-46 C26,-28 8,-18 0,0 Z', fill: rad2(b.defs, [[0, shade(color, 45)], [0.6, color], [1, shade(color, -30)]], { cx: 0.35, cy: 0.3, r: 0.75 }) }, 5), g);
  svg('circle', { cx: 0, cy: -46, r: 15, fill: '#fff' }, g);
  svg('ellipse', { cx: -11, cy: -58, rx: 5, ry: 9, fill: '#fff', opacity: 0.35, transform: 'rotate(-30 -11 -58)' }, g);
  const ic = svg('g', { transform: 'translate(0,-46)' }, g);
  ic.innerHTML = inner;
  return {
    el: b.d,
    update(t, t0) {
      const x = t - t0, T = 0.24;
      let y, sx = 1, sy = 1;
      if (x < 0) { b.d.style.opacity = 0; return; }
      b.d.style.opacity = 1;
      if (x < T) y = -120 * (1 - Math.pow(x / T, 2));
      else { const u = x - T; y = -22 * Math.exp(-u * 6) * Math.abs(Math.sin(u * 13)); const sq = 0.28 * Math.exp(-u * 11); sx = 1 + sq * 0.8; sy = 1 - sq; }
      g.setAttribute('transform', `translate(0,${y.toFixed(1)}) scale(${sx.toFixed(3)},${sy.toFixed(3)})`);
      const h = clamp(-y / 120);
      setA(sh, { rx: (12 * (1 - 0.6 * h)).toFixed(1), opacity: (0.25 * (1 - 0.7 * h)).toFixed(3) });
      const q = x > T ? ((x - T) % 1.6) / 1.6 : -1;
      setA(ring, { rx: q < 0 ? 0 : (6 + q * 30).toFixed(1), ry: q < 0 ? 0 : (2 + q * 9).toFixed(1), opacity: q < 0 ? 0 : ((1 - q) * 0.7).toFixed(3) });
    },
  };
}
const PIN_CITY = '<rect x="-9" y="-7" width="7" height="14" rx="1.5" fill="#4a7bd8"/><rect x="0" y="-11" width="9" height="18" rx="1.5" fill="#2e5aa8"/><rect x="2" y="-8" width="2" height="2" fill="#fff"/><rect x="5" y="-8" width="2" height="2" fill="#fff"/><rect x="2" y="-4" width="2" height="2" fill="#fff"/><rect x="5" y="-4" width="2" height="2" fill="#fff"/>';
const PIN_HOME = () => '<path d="M-10,-1 L0,-10 L10,-1" fill="none" stroke="#cf483d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><rect x="-7" y="-2" width="14" height="10" rx="1.5" fill="#cf483d"/><path d="' + heartPath(0, 3, 3) + '" fill="#fff"/>';

// ---------------- cute side-view tour bus with turning wheels, exhaust puffs and speed lines ----------------
function busCute(parent, w = 92) {
  const b = iconBox(parent, w, w * 0.6, '0 0 92 55');
  const puffs = [0, 1, 2].map(() => svg('circle', { r: 4, fill: '#d9dceb' }, b.s));
  const lines = [0, 1, 2].map(i => svg('line', { x1: -14, y1: 16 + i * 9, x2: -2, y2: 16 + i * 9, stroke: '#fff', 'stroke-width': 3, 'stroke-linecap': 'round' }, b.s));
  const body = svg('g', {}, b.s);
  svg('path', withStk({ d: 'M4,10 Q4,4 10,4 L74,4 Q86,4 88,16 L90,36 Q90,42 84,42 L8,42 Q4,42 4,36 Z', fill: lin(b.defs, [[0, '#7464d2'], [1, '#4b3f9a']]) }, 5), body);
  svg('path', { d: 'M70,9 L80,9 Q84,9 85,14 L86,24 L70,24 Z', fill: '#bfe3ff' }, body);
  svg('path', { d: 'M73,11 L77,11 L73,22 Z', fill: '#fff', opacity: 0.6 }, body);
  for (let i = 0; i < 3; i++) svg('rect', { x: 11 + i * 19, y: 10, width: 15, height: 13, rx: 3.5, fill: '#d6e9ff' }, body);
  svg('path', { d: 'M4,31 Q24,25 46,31 T90,29', stroke: '#f2c14e', 'stroke-width': 4, fill: 'none' }, body);
  svg('circle', { cx: 87, cy: 33, r: 3, fill: '#ffe08a' }, body);
  const wheels = [22, 68].map(cx => {
    const wg = svg('g', {}, b.s);
    svg('circle', { cx: 0, cy: 0, r: 9, fill: '#2a2733', stroke: '#fff', 'stroke-width': 3 }, wg);
    svg('circle', { cx: 0, cy: 0, r: 3.8, fill: '#c9cbd6' }, wg);
    for (let k = 0; k < 4; k++) svg('rect', { x: -1, y: -8, width: 2, height: 5, fill: '#8d8fa0', transform: `rotate(${k * 90})` }, wg);
    return { wg, cx };
  });
  return {
    el: b.d,
    update(t, speed = 1) {
      const bob = Math.abs(Math.sin(t * 18)) * 1.6 * speed;
      body.setAttribute('transform', `translate(0,${(-bob).toFixed(2)})`);
      wheels.forEach(w2 => w2.wg.setAttribute('transform', `translate(${w2.cx},44) rotate(${((t * 720 * speed) % 360).toFixed(1)})`));
      puffs.forEach((p, i) => { const q = ((t * 1.8 + i / 3) % 1); setA(p, { cx: (2 - q * 22).toFixed(1), cy: (38 - q * 8).toFixed(1), r: (2 + q * 6).toFixed(1), opacity: (0.8 * (1 - q) * speed).toFixed(2) }); });
      lines.forEach((l, i) => { const q = ((t * 3 + i * 0.37) % 1); setA(l, { x1: (-6 - q * 18).toFixed(1), x2: (2 - q * 18).toFixed(1), opacity: (speed * (1 - q) * 0.8).toFixed(2) }); });
    },
  };
}

// ---------------- calendar whose pages flip while a counter runs ----------------
function calendarFlip(parent, size = 46, color = '#e0574b') {
  const b = iconBox(parent, size, size, '0 0 100 100');
  const g = svg('g', {}, b.s);
  svg('rect', withStk({ x: 10, y: 16, width: 80, height: 76, rx: 12, fill: '#fff' }, 6), g);
  svg('path', { d: 'M10,28 Q10,16 22,16 L78,16 Q90,16 90,28 L90,38 L10,38 Z', fill: color }, g);
  for (const x of [30, 62]) svg('rect', { x, y: 6, width: 8, height: 18, rx: 4, fill: '#3a3540', stroke: '#fff', 'stroke-width': 2 }, g);
  const num = svg('text', { x: 50, y: 78, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 36, fill: '#2f2c33' }, g);
  const flap = svg('rect', { x: 14, y: 40, width: 72, height: 24, rx: 4, fill: '#f1ece3' }, g);
  return {
    el: b.d,
    update(t, value, flipping) {
      num.textContent = Math.round(value);
      const f = flipping ? ((t * 9) % 1) : 1;
      flap.setAttribute('transform', `translate(0,${(40 + 24 * f).toFixed(1)}) scale(1,${(1 - f).toFixed(3)}) translate(0,-40)`);
      flap.setAttribute('opacity', flipping ? 0.95 : 0);
      g.setAttribute('transform', flipping ? `rotate(${(Math.sin(t * 30) * 3).toFixed(2)} 50 50)` : '');
    },
  };
}

// ---------------- mini Songkran bowl with splashing drops / mini firework ----------------
function waterBowlMini(parent, size = 38) {
  const b = iconBox(parent, size, size, '-50 -50 100 100');
  const drops = [0, 1, 2, 3].map(i => svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: i % 2 ? '#7cc8f0' : '#3f9bd8' }, b.s));
  svg('path', withStk({ d: 'M-38,0 L38,0 L28,30 Q0,40 -28,30 Z', fill: lin(b.defs, [[0, '#f3cf7a'], [1, '#c9922b']]) }, 6), b.s);
  svg('path', { d: 'M-38,0 L38,0', stroke: '#fff3c4', 'stroke-width': 5, 'stroke-linecap': 'round' }, b.s);
  return { el: b.d, update(t) { drops.forEach((d, i) => { const q = ((t * 1.3 + i / 4) % 1), dir = i % 2 ? 1 : -1, sx = dir * (8 + i * 6) * q; setA(d, { transform: `translate(${sx.toFixed(1)},${(-6 - 60 * q + 70 * q * q).toFixed(1)}) scale(${(1.2 - q * 0.5).toFixed(2)})`, opacity: (1 - q * q).toFixed(2) }); }); } };
}
function fireworkMini(parent, size = 38) {
  const b = iconBox(parent, size, size, '-50 -50 100 100');
  const bursts = [[-12, -8, '#e0577a', 0], [16, 10, '#f2c14e', 0.45], [8, -20, '#4a7bd8', 0.8]].map(([x, y, c, ph]) => {
    const gg = svg('g', { transform: `translate(${x},${y})` }, b.s);
    const rays = Array.from({ length: 10 }, (_, k) => svg('line', { stroke: c, 'stroke-width': 5, 'stroke-linecap': 'round', 'data-a': k * 36 }, gg));
    return { gg, rays, ph, x, y };
  });
  return {
    el: b.d,
    update(t) {
      bursts.forEach(bu => {
        const q = ((t * 0.9 + bu.ph) % 1), r0 = 6 + q * 24, r1 = 12 + q * 34;
        bu.rays.forEach(l => { const a = rad(+l.getAttribute('data-a')); setA(l, { x1: (Math.cos(a) * r0).toFixed(1), y1: (Math.sin(a) * r0).toFixed(1), x2: (Math.cos(a) * r1).toFixed(1), y2: (Math.sin(a) * r1).toFixed(1), opacity: (1 - q).toFixed(2) }); });
      });
    },
  };
}

// ---------------- paper plane that loops away and back with a dotted trail ----------------
function paperPlane(parent, size = 48) {
  const b = iconBox(parent, size, size, '-30 -30 60 60');
  const trail = Array.from({ length: 7 }, () => svg('circle', { r: 2.2, fill: '#fff' }, b.s));
  const g = svg('g', {}, b.s);
  svg('path', withStk({ d: 'M-20,2 L22,-16 L8,20 L2,6 Z', fill: '#ffffff' }, 3), g);
  svg('path', { d: 'M2,6 L22,-16 L-2,4 Z', fill: '#d9dceb' }, g);
  const pos = q => [Math.sin(q * Math.PI * 2) * 26, -Math.sin(q * Math.PI * 4) * 12];
  return {
    el: b.d,
    update(t) {
      const q = (t * 0.45) % 1, [x, y] = pos(q), [x2, y2] = pos(q + 0.01);
      g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${(Math.atan2(y2 - y, x2 - x) * 180 / Math.PI + 20).toFixed(1)}) scale(0.8)`);
      trail.forEach((c, i) => { const [tx, ty] = pos(q - (i + 1) * 0.03); setA(c, { cx: tx.toFixed(1), cy: ty.toFixed(1), opacity: (0.7 - i * 0.09).toFixed(2) }); });
    },
  };
}

// ---------------- v6 route card: pins drop in, a comet-lit dotted road draws, the bus drives home ----------------
function routeCard2(parent, x, y, w) {
  const c = cardEl(parent, 'card route', x, y, w);
  const lbl = html('div', 'lbl', c.c);
  const lic = html('span', '', lbl); lic.style.display = 'inline-flex';
  const lbus = busCute(lic, 46);
  html('span', '', lbl, 'ระยะทางกลับบ้าน');
  const box = html('div', 'routebox', c.c);
  const W = w - 64;
  const s = svg('svg', { width: W, height: 196, viewBox: `0 0 ${W} 196`, style: 'overflow:visible' }, box);
  const defs = svg('defs', {}, s);
  const d = `M60,128 C${W * 0.32},6 ${W * 0.68},6 ${W - 60},128`;
  const m = svg('mask', { id: uidS('rm') }, defs);
  const reveal = svg('path', { d, stroke: '#fff', 'stroke-width': 22, fill: 'none', pathLength: 1, 'stroke-dasharray': '1 1', 'stroke-dashoffset': 1 }, m);
  svg('path', { d, stroke: '#ddd5c6', 'stroke-width': 6, fill: 'none', 'stroke-dasharray': '2 14', 'stroke-linecap': 'round' }, s);
  const road = svg('path', { d, stroke: '#e0574b', 'stroke-width': 7, fill: 'none', 'stroke-dasharray': '2 14', 'stroke-linecap': 'round', mask: `url(#${m.id})` }, s);
  const geo = svg('path', { d, fill: 'none', stroke: 'none' }, s);
  const L = geo.getTotalLength();
  const comet = svg('circle', { r: 26, fill: rad2(defs, [[0, '#ffe3a0', 0.9], [1, '#ffe3a0', 0]]) }, s);
  const trail = Array.from({ length: 8 }, () => svg('circle', { r: 3, fill: '#f2c14e' }, s));
  const p1w = html('div', 'pinw', box); p1w.style.left = '28px'; p1w.style.top = '50px';
  const p1 = pin3D(p1w, '#4a7bd8', PIN_CITY);
  const p2w = html('div', 'pinw', box); p2w.style.left = (W - 92) + 'px'; p2w.style.top = '50px';
  const p2 = pin3D(p2w, '#e0574b', PIN_HOME());
  const t1 = html('div', 'rlab', box, 'กรุงเทพฯ'); t1.style.left = '0px';
  const t2 = html('div', 'rlab', box, 'ขอนแก่น'); t2.style.left = (W - 120) + 'px';
  const bw = html('div', 'rbus2', box);
  const bus = busCute(bw, 92);
  const hearts = burst(s, W - 60, 82, 0, 14, 77, ['#e0577a', '#ffd66b', '#ffffff'], 160, 0.8);
  const dist = html('div', 'rdist', box);
  const od = new Odometer(dist, 3); html('small', '', dist, ' กม.');
  return {
    c,
    update(t, t0) {
      enter3d(c.c, t, t0, 'flipDown'); shine(c.sh, t, t0 + 1.25);
      lbus.update(t, 0.6);
      p1.update(t, t0 + 0.12); p2.update(t, t0 + 0.4);
      t1.style.opacity = fadeIn(t, t0 + 0.4, 0.15); t2.style.opacity = fadeIn(t, t0 + 0.7, 0.15);
      const k = ease.inOutCubic(prog(t, t0 + 0.3, t0 + 1.15));
      reveal.setAttribute('stroke-dashoffset', (1 - k).toFixed(4));
      road.setAttribute('stroke-dashoffset', (-t * 30).toFixed(1));
      const pt = geo.getPointAtLength(k * L), pt2 = geo.getPointAtLength(Math.min(L, k * L + 2));
      const ang = Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180 / Math.PI;
      const arrive = ease.inCubic(prog(t, t0 + 1.1, t0 + 1.3));
      const moving = t > t0 + 0.3 && arrive < 1;
      bw.style.opacity = moving ? 1 : 0;
      bw.style.transform = `translate(${(pt.x - 46).toFixed(1)}px, ${(pt.y - 52).toFixed(1)}px) rotate(${ang.toFixed(1)}deg) scale(${(1 - 0.8 * arrive).toFixed(3)})`;
      bus.update(t, 1);
      setA(comet, { cx: pt.x.toFixed(1), cy: (pt.y - 6).toFixed(1), opacity: moving ? 0.8 : 0 });
      trail.forEach((tc, i) => { const q = geo.getPointAtLength(Math.max(0, k * L - (i + 1) * 16)); setA(tc, { cx: q.x.toFixed(1), cy: q.y.toFixed(1), r: (3.2 - i * 0.3).toFixed(1), opacity: moving ? (0.9 - i * 0.1).toFixed(2) : 0 }); });
      hearts(t - (t0 + 1.25));
      const v = rollValue(t, t0 + 0.3, t0 + 1.15, 0, 445); od.set(v.v, v.speed);
      dist.style.opacity = fadeIn(t, t0 + 0.3, 0.15);
      const pulse = 1 + 0.25 * Math.exp(-Math.pow((t - t0 - 1.2) * 6, 2));
      dist.style.transform = `scale(${pulse.toFixed(3)})`;
    },
  };
}

// ---------------- v6 days chip: flipping calendar + rolling counter ----------------
function daysChip2(parent, x, y, text, n) {
  const ch = html('div', 'chip big', parent); ch.style.left = x + 'px'; ch.style.top = y + 'px';
  const cal = calendarFlip(ch, 56);
  html('span', '', ch, text);
  const b = html('b', '', ch); const od = new Odometer(b, String(n).length); html('span', '', ch, 'วัน');
  return {
    el: ch,
    update(t, t0) {
      popSquash(ch, t, t0, '', -8);
      const v = rollValue(t, t0 + 0.1, t0 + 0.9, 0, n); od.set(v.v, v.speed);
      cal.update(t, v.v, t > t0 + 0.1 && t < t0 + 0.9);
      const land = 1 + 0.3 * Math.exp(-Math.pow((t - t0 - 0.95) * 7, 2));
      b.style.transform = `scale(${land.toFixed(3)})`;
    },
  };
}
