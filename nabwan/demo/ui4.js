// v4 UI widgets. Each builder returns DOM handles plus an update(t, ...) driven by shot-local time.

const pinSVG = (c, inner = '') => `<svg width="56" height="72" viewBox="-28 -64 56 72"><ellipse cx="0" cy="4" rx="12" ry="4" fill="#000" opacity=".25"/><path d="M0,0 C-8,-18 -24,-26 -24,-42 A24,24 0 1 1 24,-42 C24,-26 8,-18 0,0 Z" fill="${c}"/><circle cy="-42" r="10" fill="#fff"/>${inner}</svg>`;
const busIcon = `<svg width="64" height="40" viewBox="0 0 64 40"><rect x="2" y="2" width="60" height="30" rx="8" fill="#5a4ca0"/><rect x="8" y="7" width="12" height="11" rx="3" fill="#d6c19a"/><rect x="23" y="7" width="12" height="11" rx="3" fill="#d6c19a"/><rect x="38" y="7" width="12" height="11" rx="3" fill="#d6c19a"/><rect x="52" y="7" width="7" height="18" rx="2" fill="#2b2550"/><path d="M2,24 Q20,18 40,24 T62,22" stroke="#d9a94e" stroke-width="3" fill="none"/><circle cx="16" cy="33" r="6" fill="#1c1a24"/><circle cx="48" cy="33" r="6" fill="#1c1a24"/></svg>`;
const houseHeart = (size, c = '#e0577a') => `<svg width="${size}" height="${size}" viewBox="-50 -54 100 100"><path d="M-38,-2 L0,-38 L38,-2 L38,40 L-38,40 Z" fill="#fff7ea" stroke="#b08326" stroke-width="5" stroke-linejoin="round"/><path d="M-46,0 L0,-44 L46,0" fill="none" stroke="#b08326" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="${heartPath(0, 10, 15)}" fill="${c}"/></svg>`;
function dadAvatar() {
  return `<svg width="96" height="96" viewBox="-48 -48 96 96"><circle r="48" fill="#dbe7f3"/>
  <circle r="30" cy="7" fill="#c48d66"/>
  <path d="M-30,0 C-30,-30 30,-30 30,0 C24,-14 -24,-14 -30,0 Z" fill="#9c9696"/>
  <path d="M-12,-4 L-4,-4 M4,-4 L12,-4" stroke="#5a4a44" stroke-width="3" stroke-linecap="round"/>
  <circle cx="-9" cy="5" r="2.6" fill="#1e1718"/><circle cx="9" cy="5" r="2.6" fill="#1e1718"/>
  <path d="M-9,16 Q0,12 9,16" stroke="#6b5a54" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M-7,22 Q0,27 7,22" stroke="#8a4a3c" stroke-width="2.6" fill="none" stroke-linecap="round"/>
  <path d="M-34,48 C-30,36 30,36 34,48 Z" fill="#5c7fae"/></svg>`;
}

// route map card: Bangkok -> Khon Kaen, dotted arc drawing, bus travelling, distance odometer
function routeCard(parent, x, y, w) {
  const c = cardEl(parent, 'card route', x, y, w);
  const lbl = html('div', 'lbl', c.c); lbl.innerHTML = `<svg width="30" height="34" viewBox="-14 -30 28 34"><path d="M0,0 C-4,-9 -12,-13 -12,-21 A12,12 0 1 1 12,-21 C12,-13 4,-9 0,0 Z" fill="#cf483d"/><circle cy="-21" r="5" fill="#fff"/></svg><span>ระยะทางกลับบ้าน</span>`;
  const box = html('div', 'routebox', c.c);
  const W = w - 64, Hh = 168;
  const s = svg('svg', { width: W, height: Hh, viewBox: `0 0 ${W} ${Hh}`, style: 'overflow:visible' }, box);
  const defs = svg('defs', {}, s);
  const mid = svg('mask', { id: uidS('rm') }, defs);
  const d = `M60,128 C${W * 0.32},10 ${W * 0.68},10 ${W - 60},128`;
  const reveal = svg('path', { d, stroke: '#fff', 'stroke-width': 20, fill: 'none', pathLength: 1, 'stroke-dasharray': '1 1', 'stroke-dashoffset': 1 }, mid);
  svg('path', { d, stroke: '#d3cbbd', 'stroke-width': 6, fill: 'none', 'stroke-dasharray': '2 14', 'stroke-linecap': 'round' }, s);
  svg('path', { d, stroke: '#cf483d', 'stroke-width': 7, fill: 'none', 'stroke-dasharray': '2 14', 'stroke-linecap': 'round', mask: `url(#${mid.id})` }, s);
  const geo = svg('path', { d, fill: 'none', stroke: 'none' }, s);
  const p1 = html('div', 'rpin', box); p1.innerHTML = pinSVG('#4a7bd8') + '<b>กรุงเทพฯ</b>'; p1.style.left = '0px';
  const p2 = html('div', 'rpin', box); p2.innerHTML = pinSVG('#cf483d', `<path d="${heartPath(0, -42, 7)}" fill="#cf483d"/>`) + '<b>ขอนแก่น</b>'; p2.style.left = (W - 120) + 'px';
  const bus = html('div', 'rbus', box); bus.innerHTML = busIcon;
  const dist = html('div', 'rdist', box);
  const od = new Odometer(dist, 3); html('small', '', dist, ' กม.');
  const L = geo.getTotalLength();
  return {
    c,
    update(t, t0) {
      enter3d(c.c, t, t0, 'flipDown'); shine(c.sh, t, t0 + 1.0);
      const k1 = spring(t, t0 + 0.15, 15, 6.5), k2 = spring(t, t0 + 0.95, 15, 6.5);
      p1.style.transform = `translateY(${((1 - k1) * -60).toFixed(1)}px) scale(${clamp(k1, 0, 1.2).toFixed(3)})`;
      p2.style.transform = `translateY(${((1 - k2) * -60).toFixed(1)}px) scale(${clamp(k2, 0, 1.2).toFixed(3)})`;
      const k = ease.inOutCubic(prog(t, t0 + 0.25, t0 + 1.05));
      reveal.setAttribute('stroke-dashoffset', (1 - k).toFixed(4));
      const pt = geo.getPointAtLength(k * L), pt2 = geo.getPointAtLength(Math.min(L, k * L + 2));
      const ang = Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180 / Math.PI;
      bus.style.opacity = t > t0 + 0.25 ? 1 : 0;
      bus.style.transform = `translate(${(pt.x - 32).toFixed(1)}px, ${(pt.y - 34).toFixed(1)}px) rotate(${ang.toFixed(1)}deg) translateY(${(Math.sin(t * 30) * 1.2).toFixed(1)}px)`;
      const v = rollValue(t, t0 + 0.25, t0 + 1.05, 0, 445); od.set(v.v, v.speed);
      dist.style.opacity = fadeIn(t, t0 + 0.25, 0.15);
    },
  };
}

// chip: calendar icon + "away from home N days" with an odometer
function daysChip(parent, x, y, text, n) {
  const ch = html('div', 'chip big', parent); ch.style.left = x + 'px'; ch.style.top = y + 'px';
  ch.innerHTML = `${calSVG('#cf483d')}<span>${text}</span>`;
  const b = html('b', '', ch); const od = new Odometer(b, String(n).length); html('span', '', ch, 'วัน');
  return { el: ch, update(t, t0) { enter3d(ch, t, t0, 'pop'); const v = rollValue(t, t0 + 0.1, t0 + 0.9, 0, n); od.set(v.v, v.speed); } };
}

// hourglass: flips upright on entry, sand drains (faster when urgent)
function hourglass(parent, x, y) {
  const wrap = html('div', 'hgw', parent); wrap.style.left = x + 'px'; wrap.style.top = y + 'px';
  const s = svg('svg', { width: 200, height: 250, viewBox: '-100 -125 200 250' }, wrap);
  const defs = svg('defs', {}, s);
  const ct = svg('clipPath', { id: uidS('hgt') }, defs); svg('path', { d: 'M-60,-96 L60,-96 C60,-40 10,-14 4,0 L-4,0 C-10,-14 -60,-40 -60,-96 Z' }, ct);
  const cb = svg('clipPath', { id: uidS('hgb') }, defs); svg('path', { d: 'M-4,0 L4,0 C10,14 60,40 60,96 L-60,96 C-60,40 -10,14 -4,0 Z' }, cb);
  svg('circle', { r: 118, fill: rad2(defs, [[0, '#ffe9b8', 0.45], [1, '#ffe9b8', 0]]) }, s);
  svg('path', { d: 'M-60,-96 L60,-96 C60,-40 10,-14 4,0 C10,14 60,40 60,96 L-60,96 C-60,40 -10,14 -4,0 C-10,-14 -60,-40 -60,-96 Z', fill: 'rgba(235,245,255,.28)', stroke: '#eef4ff', 'stroke-width': 4 }, s);
  const top = svg('rect', { x: -70, y: -96, width: 140, height: 96, fill: '#f2c14e', 'clip-path': `url(#${ct.id})` }, s);
  const bot = svg('path', { fill: '#e7ad3a', 'clip-path': `url(#${cb.id})` }, s);
  const stream = svg('path', { d: 'M0,0 L0,96', stroke: '#f2c14e', 'stroke-width': 4, 'stroke-dasharray': '6 5' }, s);
  svg('path', { d: 'M-40,-86 C-40,-56 -18,-30 -8,-18', stroke: '#fff', 'stroke-width': 5, fill: 'none', opacity: 0.55, 'stroke-linecap': 'round' }, s);
  for (const yy of [-112, 96]) svg('rect', { x: -78, y: yy, width: 156, height: 16, rx: 7, fill: '#8a5a34' }, s);
  for (const xx of [-70, 62]) svg('rect', { x: xx, y: -100, width: 8, height: 200, rx: 3, fill: '#6b4226' }, s);
  return {
    el: wrap,
    update(t, t0, urgent = 0) {
      const k = spring(t, t0, 12, 6), o = fadeIn(t, t0, 0.12);
      const flip = (1 - ease.outBack(prog(t, t0, t0 + 0.55))) * 180;
      wrap.style.opacity = o;
      const float = Math.sin(t * 1.6) * 6;
      wrap.style.transform = `translateY(${float.toFixed(1)}px) scale(${clamp(k, 0, 1.3).toFixed(3)}) rotate(${flip.toFixed(1)}deg) rotateY(${(Math.sin(t * 1.1) * 10).toFixed(1)}deg)`;
      const drain = clamp((t - t0 - 0.4) * (0.12 + 0.5 * urgent), 0, 0.85);
      const h = 96 * (1 - drain);
      setA(top, { y: (-h).toFixed(1), height: h.toFixed(1) });
      const pile = 14 + 70 * drain;
      bot.setAttribute('d', `M-70,96 L-70,${96 - pile * 0.35} Q0,${96 - pile * 1.25} 70,${96 - pile * 0.35} L70,96 Z`);
      stream.setAttribute('stroke-dashoffset', (-t * (60 + 140 * urgent)).toFixed(1));
      stream.setAttribute('opacity', t > t0 + 0.45 ? 1 : 0);
    },
  };
}

// round avatar badge with a ring and label (Mom / Dad)
function avatarBadge(parent, x, y, inner, label, ring) {
  const b = html('div', 'avb', parent); b.style.left = x + 'px'; b.style.top = y + 'px';
  b.innerHTML = `<div class="avc" style="box-shadow:0 0 0 6px ${ring}, 0 14px 30px rgba(0,0,0,.4)">${inner}</div><b>${label}</b>`;
  return { el: b, update(t, t0) { enter3d(b, t, t0, 'drop', `translateY(${(Math.sin(t * 2 + x) * 5).toFixed(1)}px)`); } };
}

// festival card with icon, title, date and an animated strike-through
function festivalCard(parent, x, y, w, icon, title, date, accent) {
  const c = cardEl(parent, 'card fest', x, y, w);
  c.c.style.borderLeftColor = accent;
  const ic = html('div', 'fic', c.c); ic.innerHTML = icon;
  html('div', 'ftitle', c.c, title);
  html('div', 'fdate', c.c, date);
  const st = html('div', 'strike', c.c);
  const stamp = html('div', 'stamp', c.c, 'ไม่ต้องรอ');
  return {
    c,
    update(t, tin, tstrike, tout) {
      const outK = ease.inCubic(prog(t, tout, tout + 0.4));
      enter3d(c.c, t, tin, 'flipDown', `translateY(${(outK * 260).toFixed(1)}px) rotateZ(${(outK * (x < 400 ? -18 : 18)).toFixed(1)}deg)`);
      c.c.style.opacity = (fadeIn(t, tin, 0.14) * (1 - outK)).toFixed(3);
      shine(c.sh, t, tin + 0.5);
      const sk = ease.outCubic(prog(t, tstrike, tstrike + 0.28));
      st.style.transform = `rotate(-14deg) scaleX(${sk.toFixed(3)})`;
      c.c.style.filter = sk > 0 ? `grayscale(${(0.85 * sk).toFixed(2)}) brightness(${(1 - 0.12 * sk).toFixed(2)})` : 'none';
      const sp = spring(t, tstrike + 0.18, 16, 6);
      stamp.style.opacity = fadeIn(t, tstrike + 0.18, 0.08);
      stamp.style.transform = `rotate(-12deg) scale(${(2.2 - 1.2 * clamp(sp, 0, 1.15)).toFixed(3)})`;
      return outK;
    },
  };
}
// icons for the festival cards (animated parts returned via update)
function songkranIcon() {
  return `<svg width="150" height="120" viewBox="-75 -70 150 120"><ellipse cx="0" cy="34" rx="46" ry="8" fill="#000" opacity=".15"/>
  <path d="M-48,-6 L48,-6 L36,30 Q0,40 -36,30 Z" fill="#d9a94e"/><path d="M-48,-6 L48,-6" stroke="#f3cf7a" stroke-width="6" stroke-linecap="round"/>
  <path d="M-30,6 L30,6" stroke="#b5862f" stroke-width="3"/><path d="M-26,16 L26,16" stroke="#b5862f" stroke-width="3"/>
  <g class="drops"><path class="d1" d="M-14,-30 C-8,-40 -4,-46 -4,-50 C-4,-46 0,-40 6,-30 A10,10 0 1 1 -14,-30 Z" fill="#5ab4e8"/>
  <path class="d2" d="M18,-42 C22,-48 24,-52 24,-55 C24,-52 26,-48 30,-42 A6,6 0 1 1 18,-42 Z" fill="#7cc8f0"/>
  <path class="d3" d="M-36,-40 C-33,-45 -31,-48 -31,-51 C-31,-48 -29,-45 -26,-40 A5,5 0 1 1 -36,-40 Z" fill="#7cc8f0"/></g>
  <path d="M-62,-14 Q-70,-30 -60,-44" stroke="#5ab4e8" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M62,-14 Q72,-30 62,-44" stroke="#5ab4e8" stroke-width="4" fill="none" stroke-linecap="round"/></svg>`;
}
function newYearIcon() {
  let rays = '';
  for (let i = 0; i < 12; i++) { const a = i * 30 * Math.PI / 180; rays += `<path d="M${(Math.cos(a) * 14).toFixed(1)},${(Math.sin(a) * 14).toFixed(1)} L${(Math.cos(a) * 34).toFixed(1)},${(Math.sin(a) * 34).toFixed(1)}" stroke="${i % 2 ? '#f2c14e' : '#e0577a'}" stroke-width="5" stroke-linecap="round"/>`; }
  let rays2 = '';
  for (let i = 0; i < 8; i++) { const a = (i * 45 + 20) * Math.PI / 180; rays2 += `<path d="M${(Math.cos(a) * 8).toFixed(1)},${(Math.sin(a) * 8).toFixed(1)} L${(Math.cos(a) * 20).toFixed(1)},${(Math.sin(a) * 20).toFixed(1)}" stroke="#7cc8f0" stroke-width="4" stroke-linecap="round"/>`; }
  return `<svg width="150" height="120" viewBox="-75 -70 150 120"><g class="fw1" transform="translate(-18,-14)">${rays}<circle r="5" fill="#fff"/></g>
  <g class="fw2" transform="translate(36,-34)">${rays2}<circle r="4" fill="#fff"/></g>
  <path d="M-18,40 L-18,20" stroke="#f2c14e" stroke-width="3" stroke-dasharray="3 4"/>
  <text x="34" y="36" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#4a7bd8">2570</text></svg>`;
}

// bus ticket that slides in, with a "booked" stamp
function ticketCard(parent, x, y, w) {
  const tk = html('div', 'ticket', parent); tk.style.left = x + 'px'; tk.style.top = y + 'px'; tk.style.width = w + 'px';
  tk.innerHTML = `<div class="tstub">${busIcon}<span>ตั๋วรถทัวร์</span></div>
  <div class="tmain"><div class="troute"><b>กรุงเทพฯ</b><svg width="70" height="24" viewBox="0 0 70 24"><path d="M2,12 L60,12" stroke="#b08326" stroke-width="4" stroke-dasharray="6 6"/><path d="M56,4 L68,12 L56,20" fill="none" stroke="#b08326" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><b>ขอนแก่น</b></div>
  <div class="tinfo"><span>เสาร์นี้</span><span>07:00 น.</span><span>ที่นั่ง 12A</span></div>
  <div class="tbar"></div></div>`;
  const bar = tk.querySelector('.tbar');
  for (let i = 0; i < 46; i++) html('i', '', bar).style.width = (2 + (i * 7 % 5)) + 'px';
  const sh = html('div', 'shine', tk);
  const stamp = html('div', 'okstamp', tk); stamp.innerHTML = '<svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#2f9e5b"/><path d="M11,21 L17,27 L29,14" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>จองแล้ว';
  return {
    el: tk,
    update(t, tin, tstamp) {
      enter3d(tk, t, tin, 'swingRight');
      shine(sh, t, tin + 0.45, 0.6);
      const sp = spring(t, tstamp, 15, 6);
      stamp.style.opacity = fadeIn(t, tstamp, 0.08);
      stamp.style.transform = `rotate(-10deg) scale(${(2.4 - 1.4 * clamp(sp, 0, 1.15)).toFixed(3)})`;
    },
  };
}

// lens flare: ghosts on the line from the light through frame centre
function lensFlare(parent, defs) {
  const g = svg('g', { style: 'mix-blend-mode:screen' }, parent);
  const specs = [[0.25, 46, '#ffcf8a', 0.22], [0.5, 22, '#ffe6b0', 0.3], [0.72, 70, '#f6a07a', 0.14], [1.0, 34, '#bfe0ff', 0.18], [1.3, 110, '#ffc8a0', 0.1], [1.55, 18, '#ffffff', 0.3]];
  const ghosts = specs.map(([k, r, c, o]) => ({ k, o, el: svg('circle', { r, fill: rad2(defs, [[0, c, o * 1.6], [0.7, c, o], [1, c, 0]]) }, g) }));
  const streak = svg('ellipse', { rx: 420, ry: 5, fill: rad2(defs, [[0, '#fff2d0', 0.75], [1, '#fff2d0', 0]]) }, g);
  return (sx, sy, gain = 1) => {
    const cx = 540, cy = 960;
    ghosts.forEach(q => setA(q.el, { cx: (sx + (cx - sx) * q.k * 2).toFixed(1), cy: (sy + (cy - sy) * q.k * 2).toFixed(1), opacity: gain.toFixed(3) }));
    setA(streak, { cx: sx.toFixed(1), cy: sy.toFixed(1), opacity: (0.8 * gain).toFixed(3) });
  };
}
// light leak overlay (warm blobs drifting, screen blend)
function lightLeak(parent) {
  const el = html('div', 'leak', parent);
  return (t, gain = 1) => {
    const a = 30 + 20 * Math.sin(t * 0.6), b = 70 + 15 * Math.cos(t * 0.45);
    el.style.background = `radial-gradient(circle at ${a.toFixed(1)}% ${(25 + 10 * Math.sin(t * 0.5)).toFixed(1)}%, rgba(255,170,90,.55), rgba(255,170,90,0) 42%), radial-gradient(circle at ${b.toFixed(1)}% ${(70 + 8 * Math.cos(t * 0.7)).toFixed(1)}%, rgba(255,110,140,.35), rgba(255,110,140,0) 38%)`;
    el.style.opacity = clamp(gain, 0, 1).toFixed(3);
  };
}
// hearts that rise and sway from a point, spawned on a schedule
function heartsRise(parent, cx, cy, t0, n, seed, every = 0.32) {
  const r = rng(seed);
  const hs = Array.from({ length: n }, (_, i) => {
    const el = svg('path', { d: heartPath(0, 0, 10 + r() * 10), fill: ['#e0577a', '#ff8fa8', '#f2c14e', '#ff6f6f'][i % 4] }, parent);
    return { el, t: t0 + i * every + r() * 0.12, dx: (r() - 0.5) * 220, ph: r() * 6, life: 1.6 + r() * 0.6 };
  });
  return t => hs.forEach(h => {
    const x = t - h.t;
    if (x < 0 || x > h.life) { h.el.setAttribute('opacity', 0); return; }
    const k = x / h.life;
    const px = cx + h.dx * ease.outCubic(k) + Math.sin(x * 4 + h.ph) * 14, py = cy - 340 * ease.outCubic(k);
    const sc = Math.min(1, x / 0.18) * (1 - 0.3 * k);
    h.el.setAttribute('transform', `translate(${px.toFixed(1)},${py.toFixed(1)}) scale(${sc.toFixed(3)}) rotate(${(Math.sin(x * 3 + h.ph) * 12).toFixed(1)})`);
    h.el.setAttribute('opacity', (k < 0.7 ? 1 : (1 - k) / 0.3).toFixed(3));
  });
}

// kinetic captions v2: each part may carry its own spoken onset (at) and duration (d)
function buildCue2(box, cue) {
  box.innerHTML = '';
  const words = [];
  for (const part of cue.parts) {
    const holder = html('span', 'kp kp-' + part.s, box);
    let inner = holder;
    if (part.s === 'r') { holder.classList.add('kbox'); inner = html('span', 'kbox-in', holder); }
    const pw = [];
    for (const seg of segTH.segment(part.t)) {
      if (seg.segment.trim() === '') { html('span', 'ksp', inner, ' '); continue; }
      const w = { el: html('span', 'kw', inner, seg.segment), len: seg.segment.length, part, holder };
      pw.push(w); words.push(w);
    }
    const a = part.at != null ? part.at : cue.a;
    const span = Math.min((part.d || 1.0) * 0.72, 0.16 * pw.length + 0.25);
    const total = pw.reduce((s, w) => s + w.len, 0);
    let acc = 0;
    for (const w of pw) { w.t = a + span * (acc / total); acc += w.len; }
  }
  return words;
}
function renderKinetic2(box, cues, t) {
  const cue = cues.find(c => t >= c.a - 0.02 && t < c.b);
  const key = cue ? cue.a : -1;
  if (box._key !== key) { box._key = key; box._words = cue ? buildCue2(box, cue) : []; }
  if (!cue) { box.style.opacity = 0; return; }
  box.style.opacity = 1;
  box.style.top = (cue.top || 1196) + 'px';
  const out = clamp((t - (cue.b - 0.1)) / 0.1);
  for (const w of box._words) {
    const k = spring(t, w.t, 18, 8), o = fadeIn(t, w.t, 0.09) * (1 - out);
    const b = Math.max(0, 1 - (t - w.t) / 0.14) * 7;
    w.el.style.opacity = o.toFixed(3);
    w.el.style.transform = `translateY(${((1 - k) * 26 - out * 14).toFixed(1)}px) scale(${(0.8 + 0.2 * k).toFixed(3)})`;
    w.el.style.filter = b > 0.2 && t >= w.t ? `blur(${b.toFixed(1)}px)` : 'none';
  }
  for (const h of box.querySelectorAll('.kbox')) {
    const first = box._words.find(w => w.holder === h);
    const k = spring(t, first.t - 0.06, 16, 7);
    h.style.setProperty('--bx', clamp(k, 0, 1.2).toFixed(3));
    h.style.opacity = (1 - out).toFixed(3);
  }
}
