// Demo v3 — pro motion design pass. Narration timing as before (VO at 0.4 s).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');

const GIRL = { R: 44, skin: '#d8ab86', skinShade: '#c3936d', hair: '#2a2220', hairStyle: 'ponytail', shirt: '#7fa3cf', shirtLight: '#94b5dc', shirtDark: '#6e90bb', sleeve: 'long', shirtLen: 'top', pants: '#2c3555', pantsDark: '#232a45', seed: 1 };
const GIRL_PACK = Object.assign({}, GIRL, { backpack: '#2e3140' });
const MOM = { R: 44, skin: '#c8956e', skinShade: '#b3805b', hair: '#3a3234', gray: '#b5aeae', hairStyle: 'bun', shirt: '#a84d63', shirtLight: '#bb5d73', shirtDark: '#8f4054', sleeve: 'short', shirtLen: 'top', sarong: '#5b3f7a', sarongDark: '#463063', pants: '#5b3f7a', pantsDark: '#4a3266', shoe: '#7b5236', shoeDark: '#5f3e28', earring: null, glasses: true, lashes: false, seed: 2 };
const SIL = { R: 44, skin: '#171827', skinShade: '#141523', hair: '#121320', hairStyle: 'short', shirt: '#1a1b2b', shirtLight: '#1c1d2e', shirtDark: '#151624', sleeve: 'long', shirtLen: 'long', pants: '#141522', pantsDark: '#121320', shoe: '#141522', shoeDark: '#121320', earring: null, lashes: false, flat: true };

const CUES = [
  { a: 0.40, b: 2.30, parts: [{ t: 'ถ้าคุณทำงานไกลบ้าน', s: 'w' }] },
  { a: 2.34, b: 4.15, parts: [{ t: 'กลับบ้านปีละ 2 ครั้ง', s: 'w' }] },
  { a: 4.19, b: 5.02, parts: [{ t: 'เคยนับไหม', s: 'w' }] },
  { a: 5.05, b: 8.10, parts: [{ t: 'ว่าเหลือเวลาเจอพ่อแม่', s: 'w' }, { t: 'อีกกี่วัน', s: 'r' }] },
  { a: 8.13, b: 10.36, parts: [{ t: 'ปีหนึ่ง คุณอยู่บ้าน 10 วัน', s: 'y' }] },
  { a: 10.40, b: 14.30, parts: [{ t: 'แต่แม่นับวันรอ 355 วัน', s: 'y' }] },
];

const heartPath = (cx, cy, r) => `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`;
const heartSVG = (size, color) => `<svg width="${size}" height="${size}" viewBox="-12 -12 24 24"><path d="${heartPath(0, 0, 9)}" fill="${color}"/></svg>`;
const moonSVG = `<svg width="40" height="40" viewBox="0 0 16 16"><path d="M11.5 11.8A5.5 5.5 0 0 1 6.2 2.3a5.6 5.6 0 1 0 7.3 7.4 5.4 5.4 0 0 1-2 2.1z" fill="#f2d48a"/></svg>`;
const calSVG = c => `<svg width="34" height="34" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="18" rx="4" fill="#fff" stroke="${c}" stroke-width="2"/><rect x="2" y="4" width="20" height="6" rx="3" fill="${c}"/><rect x="7" y="1.5" width="2.4" height="5" rx="1.2" fill="#555"/><rect x="14.6" y="1.5" width="2.4" height="5" rx="1.2" fill="#555"/></svg>`;
function momAvatar() {
  return `<svg width="96" height="96" viewBox="-48 -48 96 96"><circle r="48" fill="#f3dccb"/>
  <circle cx="0" cy="-34" r="13" fill="#3a3234"/><circle r="30" cy="7" fill="#c8956e"/>
  <path d="M-30,3 C-28,-30 28,-30 30,3 C16,-13 -16,-13 -30,3 Z" fill="#3a3234"/>
  <path d="M-16,-15 C-6,-21 6,-21 16,-15" stroke="#b5aeae" stroke-width="3" fill="none" stroke-linecap="round"/>
  <rect x="-20" y="-1" width="15" height="11" rx="3" fill="none" stroke="#4a3c3a" stroke-width="2.4"/><rect x="5" y="-1" width="15" height="11" rx="3" fill="none" stroke="#4a3c3a" stroke-width="2.4"/>
  <circle cx="-12" cy="5" r="2.6" fill="#1e1718"/><circle cx="12" cy="5" r="2.6" fill="#1e1718"/>
  <path d="M-7,19 Q0,25 7,19" stroke="#8a4a3c" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>`;
}
const graphemes = s => Array.from(new Intl.Segmenter('th', { granularity: 'grapheme' }).segment(s), g => g.segment);
function cardEl(parent, cls, x, y, w) {
  const c = html('div', cls, parent);
  c.style.left = x + 'px'; c.style.top = y + 'px'; if (w) c.style.width = w + 'px';
  const sh = html('div', 'shine', c);
  return { c, sh };
}
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
const SHOTS = [];
const whip = (shot, lt, dur, side) => { // side: 'out' at end of shot, 'in' at start
  let k = 0, dx = 0;
  if (side === 'out') { k = clamp((lt - (shot.b - shot.a - 0.09)) / 0.09); dx = -ease.inCubic(k) * 520; }
  else { k = 1 - clamp(lt / 0.09); dx = ease.inCubic(k) * 520; }
  shot.root.style.transform = `translateX(${dx.toFixed(1)}px)`;
  return k;
};
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };

// =====================================================================
// A — condo at night: notification from Mom (0.00–2.27)
// =====================================================================
(() => {
  const S = new Shot(0, 2.27, [['far', 0.35, 1.2], ['mid', 1, 0], ['fore', 1.9, 13]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  // far: wall, window city, curtains, picture
  svg('rect', { x: -300, y: -300, width: 1680, height: 1640, fill: lin(F.defs, [[0, '#463c56'], [1, '#594b69']]) }, F.s);
  svg('rect', { x: 120, y: 200, width: 470, height: 560, rx: 8, fill: '#2a2236' }, F.s);
  svg('rect', { x: 136, y: 216, width: 438, height: 528, fill: lin(F.defs, [[0, '#141636'], [1, '#2b2c5a']]) }, F.s);
  const r = rng(11);
  for (let i = 0; i < 50; i++) svg('circle', { cx: 140 + r() * 430, cy: 222 + r() * 260, r: 1 + r() * 1.8, fill: '#fff', opacity: 0.3 + r() * 0.5 }, F.s);
  svg('circle', { cx: 470, cy: 300, r: 60, fill: rad2(F.defs, [[0, '#fff6dc', 0.5], [1, '#fff6dc', 0]]) }, F.s);
  svg('circle', { cx: 470, cy: 300, r: 30, fill: '#f6eed8' }, F.s);
  const plane = svg('circle', { r: 4, fill: '#ff6b6b' }, F.s);
  const twinkles = [];
  let bx = 136;
  while (bx < 574) {
    const bw = Math.min(40 + r() * 54, 574 - bx), bh = 140 + r() * 240, by = 744 - bh;
    svg('rect', { x: bx, y: by, width: bw, height: bh, fill: r() > 0.5 ? '#22244a' : '#2a2c55' }, F.s);
    for (let wy = by + 14; wy < 734; wy += 24) for (let wx = bx + 6; wx < bx + bw - 8; wx += 14)
      if (r() > 0.55) twinkles.push({ el: svg('rect', { x: wx, y: wy, width: 6, height: 9, fill: '#f6c86a' }, F.s), ph: r() * 40, rate: 0.2 + r() * 0.5 });
    bx += bw + 3;
  }
  svg('rect', { x: 352, y: 216, width: 6, height: 528, fill: '#2a2236' }, F.s);
  for (const cx of [86, 566]) {
    svg('rect', { x: cx, y: 180, width: 86, height: 640, rx: 16, fill: lin(F.defs, [[0, '#6b5a84'], [1, '#5a4a72']], 1, 0) }, F.s);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 12 + k * 25, y: 190, width: 7, height: 620, rx: 3, fill: '#55466c' }, F.s);
  }
  svg('rect', { x: 70, y: 172, width: 600, height: 12, rx: 6, fill: '#3a3048' }, F.s);
  svg('rect', { x: 760, y: 330, width: 190, height: 140, rx: 6, fill: '#e9e2d6' }, F.s);
  svg('rect', { x: 772, y: 342, width: 166, height: 116, fill: '#8aa3b8' }, F.s);
  svg('path', { d: 'M772,458 L830,390 L870,430 L900,400 L938,458 Z', fill: '#5f7f6a' }, F.s);
  // mid: floor, rug, moonbeam, lamp, sofa, girl
  woodFloor(M.s, M.defs, 1330, '#3e3448', '#241d2c', '#2a2130');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#241d2c' }, M.s);
  rug(M.s, M.defs, 540, 1560, 470, 110, '#4d4160');
  svg('path', { d: 'M150,230 L560,230 L980,1560 L240,1560 Z', fill: lin(M.defs, [[0, '#c9d6ff', 0.16], [1, '#c9d6ff', 0.0]]) }, M.s);
  floorLamp(M.s, M.defs, 960, 1330, '#ffd59a', 0.55);
  svg('circle', { cx: 960, cy: 820, r: 120, fill: rad2(M.defs, [[0, '#fff2d0', 0.7], [1, '#fff2d0', 0]]) }, M.s);
  contactShadow(M.s, M.defs, 520, 1338, 470, 26, 0.45);
  sofa(M.s, M.defs, 170, 1140, 700);
  contactShadow(M.s, M.defs, 420, 1328, 120, 14, 0.4);
  const p = new Puppet(M.s, GIRL, M.defs);
  const ph = svg('g', {}, p.prop);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: '#15151b' }, ph);
  const scr = svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, ph);
  const glow = svg('circle', { r: 150, fill: rad2(M.defs, [[0, '#d4e5ff', 0.55], [1, '#d4e5ff', 0]]) }, M.s);
  const vib = svg('g', { opacity: 0 }, M.s);
  for (const sx of [-1, 1]) for (let k = 0; k < 2; k++) svg('path', { d: `M${sx * (40 + k * 16)},-30 Q${sx * (52 + k * 16)},0 ${sx * (40 + k * 16)},30`, fill: 'none', stroke: '#fff', 'stroke-width': 4, 'stroke-linecap': 'round' }, vib);
  const dustA = floaters(M.s, [160, 300, 760, 1100], 26, 21, { color: '#e8eeff', rMin: 1.2, rMax: 3.4, speed: 9, op: 0.45, base: 0.1 });
  vignette(M.s, M.defs, 0.55);
  // fore: monstera plant (bottom-left) + warm bokeh (top-right)
  const leaf = (x, y, s, a, c) => {
    const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
    svg('path', { d: 'M0,0 C60,-70 210,-80 270,0 C210,90 60,80 0,0 Z', fill: c }, g);
    svg('path', { d: 'M8,0 L262,0', stroke: shade(c, 30), 'stroke-width': 6 }, g);
    for (const kx of [70, 130, 190]) svg('path', { d: `M${kx},-40 L${kx + 20},-6 M${kx},40 L${kx + 20},6`, stroke: '#3e3448', 'stroke-width': 10 }, g);
    return g;
  };
  const leaves = [leaf(-120, 1880, 1.6, -60, '#1d3a2d'), leaf(-80, 1900, 1.5, -25, '#24473a'), leaf(-160, 1700, 1.4, -5, '#2b5243'), leaf(-60, 1960, 1.3, -88, '#1a3328')];
  svg('circle', { cx: 1040, cy: 200, r: 90, fill: '#ffcf8a', opacity: 0.25 }, R.s);
  svg('circle', { cx: 900, cy: 90, r: 60, fill: '#ffe2b0', opacity: 0.2 }, R.s);
  // UI
  const clock = cardEl(S.ui, 'clock', 56, 110);
  clock.c.innerHTML += `<div class="ic">${moonSVG}</div><div><div class="tl">อังคาร</div><div class="tt"><span>21:</span><span class="mm"></span></div><div class="sl"><i style="left:68%"></i></div></div>`;
  const mm = new Odometer(clock.c.querySelector('.mm'), 2);
  const bat = html('div', 'pill', S.ui); bat.style.left = '752px'; bat.style.top = '126px';
  bat.innerHTML = `<svg width="56" height="30" viewBox="0 0 56 30"><rect x="2" y="3" width="46" height="24" rx="6" fill="none" stroke="#fff" stroke-width="3"/><rect x="50" y="10" width="4" height="10" rx="2" fill="#fff"/><rect class="bf" x="6" y="7" width="5" height="16" rx="3" fill="#ff5e52"/></svg><b>3%</b>`;
  const bf = bat.querySelector('.bf');
  const n = html('div', 'notif', S.ui); n.style.top = '430px';
  n.innerHTML = `<div class="app">ข้อความ</div><div class="av">${momAvatar()}</div><div style="flex:1"><div class="who">แม่ <span class="hh">${heartSVG(28, '#e0577a')}</span><small>เมื่อสักครู่</small></div><div class="msg"></div></div>`;
  const msg = n.querySelector('.msg'), av = n.querySelector('.av'), hh = n.querySelector('.hh');
  const MSG = graphemes('สงกรานต์นี้กลับบ้านมั้ยลูก');
  const fxs = fxSvg(S);
  const sparkA = burst(fxs, 158, 482, 0.62, 16, 5, ['#ffd66b', '#ffffff', '#ff9fb2'], 230, 0.8);
  S.update = lt => {
    const cx = lerp(-30, 24, ease.inOutSine(prog(lt, 0, 2.27)));
    S.cam({ x: cx, y: 0, z: lerp(1.0, 1.07, ease.inOutSine(prog(lt, 0, 2.27))), fx: 430, fy: 1000 });
    twinkles.forEach(w => w.el.setAttribute('opacity', (Math.sin((lt + w.ph) * w.rate * 6) > -0.85 ? 0.85 : 0.15)));
    setA(plane, { cx: 160 + lt * 90, cy: 300 - lt * 14, opacity: Math.sin(lt * 9) > 0.3 ? 1 : 0.15 });
    const br = Math.sin(lt * 2.2) * 1.2, scroll = Math.sin(lt * 10) * 3 * (lt > 0.8 ? 1 : 0);
    p.pose({ x: 352, y: 1162, torso: 6 + br, head: 18, aF: [76, -46 + scroll], aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 0.7, smile: lerp(0.35, 0.75, prog(lt, 0.7, 1.1)) });
    const w = p.wristF;
    setA(glow, { cx: 352 + w[0] + 10, cy: 1162 + w[1] - 26, opacity: 0.8 + 0.2 * Math.sin(lt * 13) });
    scr.setAttribute('fill', lt > 0.22 && lt < 0.5 ? '#ffffff' : '#d8e8ff');
    const vk = lt > 0.2 && lt < 0.75 ? 1 : 0;
    vib.setAttribute('opacity', vk * (0.55 + 0.45 * Math.sin(lt * 40)));
    vib.setAttribute('transform', `translate(${352 + w[0]},${1162 + w[1] - 14})`);
    ph.setAttribute('transform', `translate(${vk ? Math.sin(lt * 120) * 3 : 0},0)`);
    dustA(lt + 4);
    leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(lt * 1.2 + i) * 1.5).toFixed(2)})`); });
    // UI
    enter3d(clock.c, lt, 0.05, 'flipDown'); shine(clock.sh, lt, 0.45);
    const m = rollValue(lt, 0.45, 1.0, 39, 40); mm.set(m.v, m.speed);
    enter3d(bat, lt, 0.12, 'pop');
    bf.setAttribute('opacity', Math.sin(lt * 7) > 0 ? 1 : 0.25);
    const k = spring(lt, 0.28, 13, 6);
    n.style.opacity = fadeIn(lt, 0.28, 0.12);
    n.style.transform = `translateY(${((1 - k) * -220).toFixed(1)}px) rotateX(${((1 - k) * 25).toFixed(2)}deg)`;
    av.style.transform = `scale(${spring(lt, 0.42, 16, 6).toFixed(3)})`;
    hh.style.display = 'inline-block';
    hh.style.transform = `scale(${(spring(lt, 0.5, 18, 6) * (1 + 0.12 * Math.max(0, Math.sin(lt * 9)))).toFixed(3)})`;
    const nch = Math.floor(clamp((lt - 0.5) / 0.55) * MSG.length);
    msg.textContent = MSG.slice(0, nch).join('');
    sparkA(lt);
    const out = whip(S, lt, 0.09, 'out');
    setGrade(S, out * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// B — bus terminal, Friday 20:30 (2.27–4.12)
// =====================================================================
(() => {
  const S = new Shot(2.27, 4.12, [['far', 0.3, 5], ['mid', 1, 0], ['fore', 2.2, 14]]);
  S.grade = 'saturate(1.08) contrast(1.05)';
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2500, fill: lin(F.defs, [[0, '#262c45'], [1, '#353b56']]) }, F.s);
  for (let i = 0; i < 6; i++) {
    svg('circle', { cx: 95 + i * 230 - 230, cy: 66, r: 110, fill: rad2(F.defs, [[0, '#e9f0ff', 0.45], [1, '#e9f0ff', 0]]) }, F.s);
    svg('rect', { x: 20 + i * 230 - 230, y: 58, width: 150, height: 16, rx: 8, fill: '#f2f5ff' }, F.s);
  }
  svg('rect', { x: -300, y: 100, width: 1680, height: 18, fill: '#3f4560' }, F.s);
  const cols = ['#8a3a4a', '#2f6a74', '#7a6a2e', '#5c3a76', '#2e5a8a'];
  for (let i = 0; i < 5; i++) {
    const x0 = -200 + i * 300;
    svg('rect', { x: x0, y: 460, width: 240, height: 420, rx: 20, fill: cols[i], opacity: 0.85 }, F.s);
    svg('rect', { x: x0 + 30, y: 500, width: 180, height: 140, rx: 10, fill: shade(cols[i], 40), opacity: 0.8 }, F.s);
    svg('circle', { cx: x0 + 40, cy: 820, r: 26, fill: '#ffe08a', opacity: 0.8 }, F.s);
    const tx = svg('text', { x: x0 + 120, y: 430, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 46, fill: '#c9cde0', opacity: 0.8 }, F.s); tx.textContent = 15 + i;
  }
  for (let i = 0; i < 5; i++) svg('rect', { x: 10 + i * 300 - 100, y: 118, width: 34, height: 1020, fill: '#272c43' }, F.s);
  // mid: platform, reflections, bus, passengers, girl
  svg('rect', { x: -300, y: 1110, width: 1680, height: 1300, fill: lin(M.defs, [[0, '#343a52'], [1, '#1e2234']]) }, M.s);
  const refl = svg('g', { filter: blurFilter(M.defs, 9), opacity: 0.55 }, M.s);
  for (let i = 0; i < 10; i++) svg('rect', { x: -10 + 30 + i * 112, y: 1170, width: 80, height: 260, rx: 30, fill: '#c9b48f', opacity: 0.22 }, refl);
  svg('rect', { x: -40, y: 1170, width: 30, height: 300, rx: 15, fill: '#ff5a4e', opacity: 0.35 }, refl);
  svg('rect', { x: -300, y: 1110, width: 1680, height: 22, fill: '#d6ad52' }, M.s);
  svg('rect', { x: -300, y: 1150, width: 1680, height: 8, fill: '#d6ad52', opacity: 0.5 }, M.s);
  const bus = tourBus(M.s, M.defs, -40, 1100, 1180, 'กรุงเทพฯ - ขอนแก่น');
  const puffs = Array.from({ length: 8 }, (_, i) => ({ el: svg('circle', { r: 20, fill: '#9aa0b8' }, M.s), b: i * 0.22 }));
  const sils = [[870, 0.5, 0], [925, 0.52, 1]].map(([x, sc, k]) => { const q = new Puppet(M.s, Object.assign({}, SIL, { hairStyle: k ? 'ponytail' : 'short', hairTie: '#121320' }), M.defs); return { q, x, sc, k }; });
  contactShadow(M.s, M.defs, 330, 1478, 110, 14, 0.5);
  const p = new Puppet(M.s, GIRL_PACK, M.defs);
  const ph = svg('g', {}, p.prop);
  svg('rect', { x: -15, y: -42, width: 30, height: 58, rx: 7, fill: '#15151b' }, ph);
  svg('rect', { x: -11, y: -38, width: 22, height: 50, rx: 4, fill: '#d8e8ff' }, ph);
  const glow = svg('circle', { r: 120, fill: rad2(M.defs, [[0, '#cfe1ff', 0.45], [1, '#cfe1ff', 0]]) }, M.s);
  vignette(M.s, M.defs, 0.5);
  // fore: pillar + bokeh
  svg('rect', { x: 990, y: -300, width: 160, height: 2600, fill: '#141726' }, R.s);
  svg('rect', { x: 990, y: -300, width: 20, height: 2600, fill: '#2a2f48' }, R.s);
  const bok = floaters(R.s, [-100, 0, 1300, 500], 7, 9, { color: '#ffd9a0', rMin: 20, rMax: 46, speed: 4, op: 0.18, base: 0.05, amp: 10 });
  // UI
  const clock = cardEl(S.ui, 'clock', 56, 110);
  clock.c.innerHTML += `<div class="ic">${moonSVG}</div><div><div class="tl">ศุกร์</div><div class="tt">20:30</div><div class="sl"><i style="left:62%"></i></div></div>`;
  const led = html('div', 'led', S.ui); led.style.left = '56px'; led.style.top = '300px';
  led.innerHTML = `<div class="a"><span>20:30</span><span>ขอนแก่น</span></div><div class="b">กำลังขึ้นรถ</div>`;
  const ledB = led.querySelector('.b');
  const card = cardEl(S.ui, 'card', 640, 110); card.c.style.minWidth = '340px';
  html('div', 'lbl', card.c, 'กลับบ้าน');
  const num = html('div', 'num', card.c);
  const od = new Odometer(num, 1); html('small', '', num, 'ครั้ง/ปี');
  const chip1 = html('div', 'chip', S.ui); chip1.innerHTML = `${calSVG('#cf483d')}สงกรานต์`; chip1.style.left = '640px'; chip1.style.top = '420px';
  const chip2 = html('div', 'chip', S.ui); chip2.innerHTML = `${calSVG('#4a7bd8')}ปีใหม่`; chip2.style.left = '860px'; chip2.style.top = '420px';
  const fxs = fxSvg(S);
  const spark1 = burst(fxs, 720, 450, 0.72, 10, 13, ['#ffd66b', '#fff'], 170, 0.6);
  const spark2 = burst(fxs, 920, 450, 1.02, 10, 17, ['#9cc0ff', '#fff'], 170, 0.6);
  S.update = lt => {
    S.cam({ x: lerp(-20, 36, ease.inOutSine(prog(lt, 0, 1.85))), y: 0, z: lerp(1.0, 1.07, ease.inOutSine(prog(lt, 0, 1.85))), fx: 330, fy: 1150 });
    bus.g.setAttribute('transform', `translate(0,${(Math.sin(lt * 31) * 0.8).toFixed(2)})`);
    puffs.forEach(pf => { const a = ((lt - pf.b) % 1.76 + 1.76) % 1.76; setA(pf.el, { cx: -30 - a * 60, cy: 1060 - a * 80, r: 14 + a * 40, opacity: (0.35 * (1 - a / 1.76)).toFixed(3) }); });
    sils.forEach(({ q, x, sc, k }) => q.pose({ x, y: 1100 - 300 * sc, s: sc, f: k ? -1 : 1, torso: 2 + Math.sin(lt * 2 + k) * 1, head: 4, aF: [96, 94], aB: [92, 90], eyes: 1 }));
    const look = ease.inOutSine(prog(lt, 0.85, 1.25));
    p.pose({ x: 330, y: 1172, s: 1.02, torso: 3 + Math.sin(lt * 2) * 1, head: lerp(16, -6, look), aF: [80, -30], aB: [96, 94], lF: [88, 90], lB: [93, 92], t: lt + 2.1, smile: lerp(0.45, 0.8, look) });
    const w = p.wristF;
    setA(glow, { cx: 330 + w[0] * 1.02 + 10, cy: 1172 + w[1] * 1.02 - 24 });
    bok(lt);
    enter3d(clock.c, lt, 0.12, 'flipDown'); shine(clock.sh, lt, 0.5);
    enter3d(led, lt, 0.18, 'flipDown');
    ledB.style.opacity = Math.sin(lt * 12) > -0.2 ? 1 : 0.15;
    enter3d(card.c, lt, 0.3, 'swingRight'); shine(card.sh, lt, 1.2);
    const v = rollValue(lt, 0.45, 1.05, 0, 2); od.set(v.v, v.speed);
    enter3d(chip1, lt, 0.68, 'pop'); enter3d(chip2, lt, 0.98, 'pop');
    spark1(lt); spark2(lt);
    const inK = whip(S, lt, 0.09, 'in');
    setGrade(S, inK * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// C — night highway, question mark (4.12–8.07) with zoom-through into her window
// =====================================================================
(() => {
  const S = new Shot(4.12, 8.07, [['sky', 0.1, 0.8], ['far', 0.3, 2.5], ['mid', 1, 0], ['fore', 1.6, 12]]);
  S.grade = 'saturate(1.1) contrast(1.05)';
  const K = S.L.sky, F = S.L.far, M = S.L.mid, R = S.L.fore;
  const OY = 250;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2500, fill: lin(K.defs, [[0, '#121634'], [0.55, '#262a58'], [1, '#141733']]) }, K.s);
  const r = rng(5);
  for (let i = 0; i < 110; i++) svg('circle', { cx: -100 + r() * 1280, cy: -100 + r() * 1100, r: 0.8 + r() * 2.2, fill: '#fff', opacity: 0.2 + r() * 0.6 }, K.s);
  svg('circle', { cx: 860, cy: 330, r: 120, fill: rad2(K.defs, [[0, '#fff3d6', 0.35], [1, '#fff3d6', 0]]) }, K.s);
  svg('circle', { cx: 860, cy: 330, r: 46, fill: '#f6eed8' }, K.s);
  // far skyline with tiny lights
  const sky = svg('g', {}, F.s);
  let x = -300;
  while (x < 2600) {
    const w = 60 + r() * 110, h = 120 + r() * 260;
    svg('rect', { x, y: OY + 1150 - 180 - h, width: w, height: h + 200, fill: '#1c1f43' }, sky);
    for (let k = 0; k < 6; k++) if (r() > 0.4) svg('rect', { x: x + 8 + r() * (w - 16), y: OY + 1150 - 160 - h + r() * h, width: 5, height: 7, fill: '#f6c86a', opacity: 0.7 }, sky);
    x += w + 10;
  }
  // mid: lamps (scroll), road, bus, rail, reflections, oncoming light trails
  const lamps = svg('g', {}, M.s);
  for (let i = 0; i < 7; i++) {
    const g = svg('g', { transform: `translate(${i * 360},${OY})` }, lamps);
    svg('rect', { x: -5, y: 640, width: 10, height: 520, fill: '#3a3d5c' }, g);
    svg('path', { d: 'M0,646 Q20,620 58,624', fill: 'none', stroke: '#3a3d5c', 'stroke-width': 8 }, g);
    svg('circle', { cx: 60, cy: 630, r: 150, fill: rad2(M.defs, [[0, '#ffcf7a', 0.5], [1, '#ffcf7a', 0]]) }, g);
    svg('ellipse', { cx: 60, cy: 632, rx: 18, ry: 8, fill: '#fff1c8' }, g);
    svg('path', { d: 'M42,640 L78,640 L170,1150 L-50,1150 Z', fill: lin(M.defs, [[0, '#ffd590', 0.16], [1, '#ffd590', 0]]) }, g);
  }
  svg('rect', { x: -300, y: OY + 1150, width: 1680, height: 70, fill: '#1e2140' }, M.s);
  const bus = tourBus(M.s, M.defs, 40, OY + 1150, 1000, 'กรุงเทพฯ - ขอนแก่น');
  const winX = 40 + 30 + 4 * 112 + 48, winY = OY + 1150 - 330 + 80;
  svg('circle', { cx: winX, cy: winY - 6, r: 22, fill: '#2b2235' }, bus.g);
  svg('rect', { x: winX - 18, y: winY + 12, width: 36, height: 30, rx: 10, fill: '#2b2235' }, bus.g);
  const sweep = svg('rect', { x: 0, y: OY + 1150 - 330, width: 180, height: 330, fill: lin(M.defs, [[0, '#fff2cc', 0], [0.5, '#fff2cc', 0.28], [1, '#fff2cc', 0]], 1, 0) }, M.s);
  const head = svg('path', { d: `M1040,${OY + 1150 - 120} L1400,${OY + 1150 - 220} L1400,${OY + 1150 + 40} Z`, fill: lin(M.defs, [[0, '#fff6d8', 0.35], [1, '#fff6d8', 0]], 1, 0) }, M.s);
  svg('rect', { x: -300, y: OY + 1150, width: 1680, height: 8, fill: '#e9e6f0', opacity: 0.85 }, M.s);
  const rail = svg('g', {}, M.s);
  for (let i = 0; i < 12; i++) svg('rect', { x: i * 160 - 160, y: OY + 1160, width: 12, height: 64, rx: 3, fill: '#d9d6e6' }, rail);
  svg('rect', { x: -300, y: OY + 1220, width: 1680, height: 900, fill: lin(M.defs, [[0, '#15183a'], [1, '#0d0f28']]) }, M.s);
  const refl = svg('g', { filter: blurFilter(M.defs, 7) }, M.s);
  for (let i = 0; i < 7; i++) svg('rect', { x: i * 360 + 52, y: OY + 1290, width: 16, height: 280, rx: 8, fill: '#ffcf7a', opacity: 0.35 }, refl);
  const trails = Array.from({ length: 5 }, (_, i) => ({ el: svg('rect', { y: OY + 1190 + (i % 2) * 8, height: 6, rx: 3, fill: i % 2 ? '#ff6a5a' : '#fff4d6', opacity: 0.85 }, M.s), ph: i * 0.37, w: 220 + i * 40 }));
  vignette(M.s, M.defs, 0.55);
  // fore: posts and bushes whizzing past
  const fore = svg('g', {}, R.s);
  for (let i = 0; i < 6; i++) {
    svg('rect', { x: i * 420, y: 1500, width: 70, height: 700, rx: 10, fill: '#0c0d1f' }, fore);
    svg('ellipse', { cx: i * 420 + 220, cy: 1880, rx: 200, ry: 120, fill: '#0e1124' }, fore);
  }
  // UI: question mark with ripples and orbiting sparks
  const fxs = fxSvg(S);
  const rip = ripples(fxs, 540, 900, 100, '#d8d4ea', 3, 1.5);
  const orb = [0, 1, 2].map(i => svg('circle', { r: 6, fill: i === 1 ? '#ffd66b' : '#fff' }, fxs));
  const qw = html('div', 'qwrap', S.ui); qw.style.left = '440px'; qw.style.top = '800px';
  const q = html('div', 'qmark', qw, '?');
  const sparkQ = burst(fxs, 540, 900, 0.32, 14, 23, ['#ffffff', '#ffd66b', '#cfd2ff'], 280, 0.8);
  const redT = 6.32 - 4.12;
  S.update = lt => {
    // zoom-through into her window at the end
    const zt = prog(lt, 3.6, 3.95);
    const zz = lerp(1.0, 1.05, ease.inOutSine(prog(lt, 0, 3.6))) * (1 + 5 * ease.inCubic(zt));
    S.cam({ x: 0, y: Math.sin(lt * 1.3) * 4, z: zz, fx: zt > 0 ? winX : 540, fy: zt > 0 ? winY : 1250 });
    lamps.setAttribute('transform', `translate(${-((lt * 300) % 360)},0)`);
    refl.setAttribute('transform', `translate(${-((lt * 300) % 360)},0)`);
    rail.setAttribute('transform', `translate(${-((lt * 700) % 160)},0)`);
    fore.setAttribute('transform', `translate(${-((lt * 1500) % 420)},0)`);
    sky.setAttribute('transform', `translate(${-lt * 18},0)`);
    const sx = 1100 - ((lt * 300 + 40) % 360) * 3.4;
    sweep.setAttribute('x', sx.toFixed(1));
    trails.forEach(tr => { const k = ((lt + tr.ph) % 1.1) / 1.1; setA(tr.el, { x: (1300 - k * 1900).toFixed(1), width: tr.w }); });
    bus.g.setAttribute('transform', `translate(0,${(Math.sin(lt * 9) * 1.6).toFixed(2)})`);
    bus.wheels.forEach(wh => { const m = wh.getAttribute('transform').match(/translate\(([^)]+)\)/)[1]; wh.setAttribute('transform', `translate(${m}) rotate(${(lt * 420) % 360})`); });
    head.setAttribute('opacity', 0.85 + 0.15 * Math.sin(lt * 7));
    // question mark: elastic squash-and-stretch pop, bob, red alert on "อีกกี่วัน"
    const k = spring(lt, 0.15, 14, 5.5);
    const sq = 1 + (k - 1) * 0.6;
    const bob = Math.sin(lt * 2.2) * 10;
    const alarm = lt > redT ? Math.exp(-(lt - redT) * 3) : 0;
    const shake = alarm > 0.05 ? Math.sin(lt * 70) * 8 * alarm : 0;
    qw.style.opacity = fadeIn(lt, 0.15, 0.1) * (1 - zt);
    qw.style.transform = `translate(${shake.toFixed(1)}px, ${bob.toFixed(1)}px) scale(${(k * (2 - sq)).toFixed(3)}, ${(k * sq).toFixed(3)})`;
    q.style.color = alarm > 0.1 ? '#e2382c' : '#cf483d';
    q.style.boxShadow = `0 0 ${(40 + 60 * alarm).toFixed(0)}px rgba(${alarm > 0.1 ? '255,80,60' : '255,255,255'},${(0.35 + 0.4 * alarm).toFixed(2)}), 0 24px 40px rgba(0,0,0,.45)`;
    fxs.setAttribute('transform', `translate(0,${bob.toFixed(1)})`);
    rip(lt, clamp(k) * (1 - zt));
    orb.forEach((o, i) => { const a = lt * 2.4 + i * 2.1; setA(o, { cx: 540 + Math.cos(a) * 140, cy: 900 + Math.sin(a) * 50, opacity: clamp(k) * (1 - zt) * 0.9 }); });
    sparkQ(lt);
    setGrade(S, zt * 14);
  };
  SHOTS.push(S);
})();

// =====================================================================
// D — inside the bus (blurred) + waffle card (8.07–10.33)
// =====================================================================
(() => {
  const S = new Shot(8.07, 10.33, [['far', 0.4, 10], ['mid', 1, 7]]);
  S.grade = 'saturate(1.05)';
  const F = S.L.far, M = S.L.mid;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2500, fill: lin(F.defs, [[0, '#262a4c'], [1, '#1b1e3a']]) }, F.s);
  svg('rect', { x: 120, y: 360, width: 840, height: 520, rx: 40, fill: '#151838' }, F.s);
  svg('rect', { x: 150, y: 390, width: 780, height: 460, rx: 30, fill: lin(F.defs, [[0, '#1b2048'], [1, '#2b2f60']]) }, F.s);
  const passing = svg('g', {}, F.s);
  for (let i = 0; i < 8; i++) svg('circle', { cx: i * 260, cy: 560 + (i % 3) * 70, r: 60 + (i % 2) * 30, fill: rad2(F.defs, [[0, '#ffcf7a', 0.55], [1, '#ffcf7a', 0]]) }, passing);
  svg('rect', { x: 100, y: 330, width: 150, height: 600, rx: 30, fill: '#c25a7c' }, F.s);
  svg('rect', { x: 830, y: 330, width: 150, height: 600, rx: 30, fill: '#c25a7c' }, F.s);
  svg('rect', { x: -300, y: 1420, width: 1680, height: 900, fill: '#161830' }, M.s);
  svg('rect', { x: 330, y: 840, width: 120, height: 560, rx: 50, fill: '#3e5ea8' }, M.s);
  svg('rect', { x: 352, y: 800, width: 90, height: 80, rx: 26, fill: '#e9e6f0' }, M.s);
  svg('rect', { x: 330, y: 1240, width: 330, height: 90, rx: 30, fill: '#4668b6' }, M.s);
  const p = new Puppet(M.s, GIRL, M.defs);
  const lightSweep = svg('rect', { x: 0, y: 300, width: 260, height: 1250, fill: lin(M.defs, [[0, '#ffd590', 0], [0.5, '#ffd590', 0.22], [1, '#ffd590', 0]], 1, 0) }, M.s);
  vignette(M.s, M.defs, 0.6);
  const card = cardEl(S.ui, 'card pink', 64, 190, 952);
  html('div', 'lbl', card.c, '1 ปี = 365 วัน');
  const grid = html('div', 'waffle', card.c);
  const cells = [];
  for (let i = 0; i < 365; i++) cells.push(html('i', '', grid));
  const leg = html('div', 'legend', card.c);
  const l1 = html('div', '', leg); l1.innerHTML = '<s></s>อยู่บ้าน ';
  const o1 = new Odometer(html('b', '', l1), 2); l1.append(' วัน');
  const l2 = html('div', 'gray', leg); l2.innerHTML = '<s></s>อยู่กรุงเทพฯ ';
  const o2 = new Odometer(html('b', '', l2), 3); l2.append(' วัน');
  const order = [101, 102, 103, 104, 105, 363, 364, 0, 1, 2];
  const fxs = fxSvg(S);
  const pos = idx => [64 + 10 + 32 + (idx % 26) * 33 + 14, 190 + 22 + 58 + 22 + Math.floor(idx / 26) * 33 + 14];
  const bursts = order.map((idx, k) => { const [cx, cy] = pos(idx); return burst(fxs, cx, cy, 0.62 + k * 0.085, 7, 40 + k, ['#ffd66b', '#fff4c2'], 90, 0.45); });
  S.update = lt => {
    const zin = 1 - prog(lt, 0, 0.35);
    S.cam({ x: 0, y: 0, z: 1 + 0.35 * ease.outCubic(zin), fx: 520, fy: 900 });
    setGrade(S, zin * 10);
    passing.setAttribute('transform', `translate(${-((lt * 900) % 520)},0)`);
    const sx = 1200 - ((lt * 1.0 + 0.3) % 1.2) / 1.2 * 1700;
    lightSweep.setAttribute('x', sx.toFixed(1));
    p.pose({ x: 470, y: 1250, torso: -6, head: -12 + Math.sin(lt * 5) * 1.2, aF: [80, 12], aB: [84, 16], lF: [-4, 88], lB: [-2, 90], eyes: 0, t: lt, smile: 0.3 });
    enter3d(card.c, lt, 0.12, 'swingLeft'); shine(card.sh, lt, 1.55, 0.8);
    cells.forEach((c, i) => {
      const d = 0.2 + ((i % 26) + Math.floor(i / 26)) * 0.009;
      const k = spring(lt, d, 20, 8);
      c.style.transform = `scale(${clamp(k, 0, 1.3).toFixed(3)})`;
    });
    let lit = 0;
    order.forEach((idx, k) => {
      const t0 = 0.62 + k * 0.085, on = lt >= t0;
      if (on) lit++;
      cells[idx].className = on ? 'on' : '';
      if (on) cells[idx].style.transform = `scale(${(1 + 0.55 * Math.exp(-(lt - t0) * 9)).toFixed(3)})`;
    });
    bursts.forEach(b => b(lt));
    const v1 = rollValue(lt, 0.62, 0.62 + 9 * 0.085 + 0.1, 0, 10); o1.set(v1.v, v1.speed);
    const v2 = rollValue(lt, 0.62, 0.62 + 9 * 0.085 + 0.1, 365, 355); o2.set(v2.v, v2.speed);
  };
  SHOTS.push(S);
})();

// =====================================================================
// shared: Mom's wooden room, layered
// =====================================================================
function momRoom3(S, withFore = true) {
  const F = S.L.far, M = S.L.mid;
  const tones = ['#8a6143', '#7f573a', '#906746', '#86603f'];
  for (let i = -3; i < 16; i++) {
    svg('rect', { x: i * 84, y: -300, width: 84, height: 1680, fill: tones[(i + 12) % 4] }, F.s);
    svg('rect', { x: i * 84, y: -300, width: 3, height: 1680, fill: '#634229', opacity: 0.6 }, F.s);
  }
  svg('rect', { x: 770, y: 230, width: 250, height: 330, rx: 6, fill: '#4b3220' }, F.s);
  svg('rect', { x: 784, y: 244, width: 222, height: 302, fill: lin(F.defs, [[0, '#141636'], [1, '#2c2d5a']]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 50, fill: rad2(F.defs, [[0, '#fff3d6', 0.5], [1, '#fff3d6', 0]]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 26, fill: '#f4ecd6' }, F.s);
  const flies = floaters(F.s, [790, 400, 210, 140], 9, 61, { color: '#fff59a', rMin: 2, rMax: 4, speed: 6, amp: 14, op: 0.9, base: 0.0, twinkle: 3, filter: blurFilter(F.defs, 1.2) });
  svg('rect', { x: 892, y: 244, width: 6, height: 302, fill: '#4b3220' }, F.s);
  svg('rect', { x: 784, y: 392, width: 222, height: 6, fill: '#4b3220' }, F.s);
  svg('rect', { x: -300, y: -300, width: 1680, height: 1680, fill: lin(F.defs, [[0, '#140a18', 0.4], [0.55, '#140a18', 0.0], [1, '#140a18', 0.3]]) }, F.s);
  // mid: floor, cabinet, photo, calendar, mom (+ shadow), bulb
  woodFloor(M.s, M.defs, 1380, '#6a4630', '#3f2817', '#3a2414');
  svg('rect', { x: -300, y: 1900, width: 1680, height: 400, fill: '#3f2817' }, M.s);
  svg('rect', { x: 40, y: 1180, width: 280, height: 200, rx: 10, fill: '#5a3a26' }, M.s);
  svg('rect', { x: 52, y: 1196, width: 124, height: 168, rx: 6, fill: '#6a4630' }, M.s);
  svg('rect', { x: 184, y: 1196, width: 124, height: 168, rx: 6, fill: '#6a4630' }, M.s);
  svg('rect', { x: 80, y: 1100, width: 54, height: 80, rx: 12, fill: '#c94f4a' }, M.s);
  svg('rect', { x: 180, y: 1124, width: 110, height: 56, rx: 10, fill: '#3d4a5c' }, M.s);
  svg('circle', { cx: 210, cy: 1152, r: 16, fill: '#25303f' }, M.s);
  const photoGlow = svg('circle', { cx: 170, cy: 695, r: 190, fill: rad2(M.defs, [[0, '#ffe2a8', 0.5], [1, '#ffe2a8', 0]]), opacity: 0 }, M.s);
  svg('rect', { x: 60, y: 560, width: 220, height: 270, rx: 8, fill: '#3a2a1e' }, M.s);
  svg('rect', { x: 76, y: 576, width: 188, height: 238, fill: lin(M.defs, [[0, '#c7d4e2'], [1, '#a9bccf']]) }, M.s);
  svg('path', { d: 'M104,814 C106,742 234,742 236,814 Z', fill: '#1d1d24' }, M.s);
  svg('path', { d: 'M144,760 C154,800 186,800 196,760', fill: 'none', stroke: '#f5d76e', 'stroke-width': 10, 'stroke-linecap': 'round' }, M.s);
  faceFront(M.s, 170, 700, 42, { skin: '#d8ab86', hair: '#2a2220', hairStyle: 'bob' });
  svg('path', { d: 'M114,654 L170,632 L226,654 L170,674 Z', fill: '#1d1d24' }, M.s);
  svg('path', { d: 'M216,656 L224,702', stroke: '#f5d76e', 'stroke-width': 4 }, M.s);
  const cal = svg('g', { transform: 'translate(320,430)' }, M.s);
  svg('rect', { x: 8, y: 12, width: 430, height: 560, rx: 10, fill: '#000', opacity: 0.22 }, cal);
  svg('path', { d: 'M215,-60 L120,0 M215,-60 L310,0', stroke: '#2a1d14', 'stroke-width': 3 }, cal);
  svg('circle', { cx: 215, cy: -62, r: 7, fill: '#2a1d14' }, cal);
  const page = svg('g', {}, cal);
  svg('rect', { x: 0, y: 0, width: 430, height: 560, rx: 10, fill: '#f6f1e6' }, page);
  svg('path', { d: 'M0,10 Q0,0 10,0 L420,0 Q430,0 430,10 L430,86 L0,86 Z', fill: '#cf483d' }, page);
  const tt = svg('text', { x: 215, y: 58, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 40, fill: '#fff' }, page); tt.textContent = 'มีนาคม 2569';
  ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'].forEach((d, i) => { const e = svg('text', { x: 34 + i * 60, y: 124, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 500, 'font-size': 22, fill: i === 0 ? '#cf483d' : '#6b6670' }, page); e.textContent = d; });
  const cell = d => { const i = d - 1; return [34 + (i % 7) * 60, 176 + Math.floor(i / 7) * 82]; };
  for (let d = 1; d <= 31; d++) {
    const [cx, cy] = cell(d);
    const e = svg('text', { x: cx, y: cy + 12, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 34, fill: '#2f2c33' }, page); e.textContent = d;
    if (d <= 27) svg('path', { d: `M${cx - 19},${cy - 19} L${cx + 19},${cy + 19} M${cx + 19},${cy - 19} L${cx - 19},${cy + 19}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.9 }, page);
  }
  const [x28, y28] = cell(28), o = 19;
  const xA = svg('path', { d: `M${x28 - o},${y28 - o} L${x28 + o},${y28 + o}`, stroke: '#cf483d', 'stroke-width': 6, 'stroke-linecap': 'round', 'stroke-dasharray': 60, 'stroke-dashoffset': 60 }, page);
  const xB = svg('path', { d: `M${x28 + o},${y28 - o} L${x28 - o},${y28 + o}`, stroke: '#cf483d', 'stroke-width': 6, 'stroke-linecap': 'round', 'stroke-dasharray': 60, 'stroke-dashoffset': 60 }, page);
  // bulb + swinging light; Mom's cast shadow on the wall
  const bulbG = svg('g', {}, M.s);
  svg('rect', { x: -2.5, y: 0, width: 5, height: 150, fill: '#2a1d14' }, bulbG);
  svg('circle', { cx: 0, cy: 168, r: 22, fill: '#ffe4ad' }, bulbG);
  svg('circle', { cx: 0, cy: 168, r: 70, fill: rad2(M.defs, [[0, '#fff2c8', 0.8], [1, '#fff2c8', 0]]) }, bulbG);
  const pool = svg('circle', { r: 900, fill: rad2(M.defs, [[0, '#ffd9a0', 0.4], [0.5, '#ffd9a0', 0.12], [1, '#ffd9a0', 0]]) }, M.s);
  const shadowG = svg('g', { opacity: 0.28, filter: blurFilter(M.defs, 7) }, M.s);
  const momShadow = new Puppet(shadowG, Object.assign({}, MOM, { skin: '#1a0e08', skinShade: '#1a0e08', hair: '#1a0e08', gray: null, shirt: '#1a0e08', shirtLight: '#1a0e08', shirtDark: '#1a0e08', sarong: '#1a0e08', sarongDark: '#1a0e08', pants: '#1a0e08', pantsDark: '#1a0e08', shoe: '#1a0e08', shoeDark: '#1a0e08', glasses: false, flat: true }), M.defs);
  contactShadow(M.s, M.defs, 885, 1530, 110, 14, 0.5);
  const mom = new Puppet(M.s, MOM, M.defs);
  const marker = svg('g', {}, mom.prop);
  svg('rect', { x: -6, y: -46, width: 12, height: 54, rx: 5, fill: '#cf483d' }, marker);
  svg('rect', { x: -6, y: -46, width: 12, height: 15, rx: 5, fill: '#efe9e1' }, marker);
  const dust = floaters(M.s, [300, 200, 600, 700], 24, 37, { color: '#ffe9c4', rMin: 1.2, rMax: 3.2, speed: 8, op: 0.45, base: 0.1 });
  vignette(M.s, M.defs, 0.5);
  let cloth = null;
  if (withFore) {
    const R = S.L.fore;
    svg('path', { d: 'M-200,40 Q300,120 900,30', fill: 'none', stroke: '#2b1d12', 'stroke-width': 6 }, R.s);
    cloth = svg('g', { transform: 'translate(-90,60)' }, R.s);
    const id = uidS('plaid');
    const pat = svg('pattern', { id, width: 60, height: 60, patternUnits: 'userSpaceOnUse' }, R.defs);
    svg('rect', { width: 60, height: 60, fill: '#c23b3b' }, pat);
    svg('rect', { x: 0, y: 0, width: 30, height: 60, fill: '#2f4fa0', opacity: 0.75 }, pat);
    svg('rect', { x: 0, y: 0, width: 60, height: 30, fill: '#ffffff', opacity: 0.35 }, pat);
    svg('path', { d: 'M0,0 L210,10 L200,560 Q100,600 10,560 Z', fill: `url(#${id})` }, cloth);
  }
  const target = [320 + x28, 430 + y28];
  return {
    mom, xA, xB, target, page, photoGlow,
    update(lt, pose) {
      const ang = Math.sin(lt * 1.7) * 5;
      const bx = 602 + Math.sin(rad(ang)) * 168, by = Math.cos(rad(ang)) * 168;
      bulbG.setAttribute('transform', `translate(602,0) rotate(${(-ang).toFixed(2)})`);
      setA(pool, { cx: bx.toFixed(1), cy: (by + 200).toFixed(1) });
      mom.pose(pose);
      const shp = Object.assign({}, pose, { x: pose.x + (pose.x - bx) * 0.12 + 40, y: pose.y - 30, s: (pose.s || 1) * 1.04 });
      momShadow.pose(shp);
      flies(lt);
      dust(lt + 2);
      if (cloth) cloth.setAttribute('transform', `translate(-90,60) skewX(${(Math.sin(lt * 1.1) * 2.5).toFixed(2)})`);
    },
  };
}

// =====================================================================
// E — Mom crosses out day 28, counter 0 → 355 (10.33–14.6)
// =====================================================================
(() => {
  const S = new Shot(10.33, 14.6, [['far', 0.4, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) sepia(0.06) contrast(1.04)';
  const room = momRoom3(S, true);
  const card = cardEl(S.ui, 'card', 56, 110);
  html('div', 'lbl', card.c, 'แม่นับวันรอ');
  const num = html('div', 'num', card.c);
  const od = new Odometer(num, 3); html('small', '', num, 'วัน');
  const heart = html('div', '', S.ui); heart.innerHTML = heartSVG(70, '#e0577a'); heart.style.cssText = 'position:absolute;left:300px;top:190px';
  const fxs = fxSvg(S);
  const sparkX = burst(fxs, room.target[0], room.target[1], 1.32, 14, 71, ['#ff7a6a', '#ffd66b', '#ffffff'], 200, 0.7);
  const sparkN = burst(fxs, 250, 260, 2.72, 18, 73, ['#ffd66b', '#ffffff', '#ff9fb2'], 260, 0.9);
  S.update = lt => {
    S.cam({ x: lerp(0, -28, ease.inOutSine(prog(lt, 0, 4.27))), y: 0, z: lerp(1.0, 1.08, ease.inOutSine(prog(lt, 0, 4.27))), fx: 560, fy: 800 });
    const pose = { x: 885, y: 1235, s: 1.12, f: -1, torso: 4, head: -6, aB: [96, 92], lF: [90, 90], lB: [92, 90], t: lt + 0.4, smile: 0.35 };
    const [tx, ty] = room.target, o = 19;
    const k1 = ease.inOutSine(prog(lt, 0.55, 0.85)), k2 = ease.inOutSine(prog(lt, 1.0, 1.3));
    let px, py;
    if (lt < 0.95) { px = tx - o + 2 * o * k1; py = ty - o + 2 * o * k1; } else { px = tx + o - 2 * o * k2; py = ty - o + 2 * o * k2; }
    const raise = ease.inOutSine(prog(lt, 0.05, 0.5)) * (1 - ease.inOutSine(prog(lt, 1.55, 2.0)));
    const reachA = room.mom.reach(pose, px - 18, py + 48);
    pose.aF = [lerp(96, reachA[0], raise), lerp(94, reachA[1], raise)];
    pose.propRot = lerp(0, -20, raise);
    const toChest = ease.inOutSine(prog(lt, 2.05, 2.6));
    pose.aB = [lerp(96, 60, toChest), lerp(92, -150, toChest)];
    pose.head = lerp(-4, -12, raise) + lerp(0, -8, ease.inOutSine(prog(lt, 2.0, 2.6)));
    pose.smile = lerp(0.35, 0.9, ease.inOutSine(prog(lt, 2.0, 2.6)));
    room.update(lt, pose);
    room.xA.setAttribute('stroke-dashoffset', 60 * (1 - k1));
    room.xB.setAttribute('stroke-dashoffset', 60 * (1 - k2));
    const flutter = Math.exp(-Math.max(0, lt - 1.3) * 4) * (lt > 1.3 ? Math.sin((lt - 1.3) * 30) : 0);
    room.page.setAttribute('transform', `skewY(${(flutter * 1.2).toFixed(2)})`);
    room.photoGlow.setAttribute('opacity', ease.inOutSine(prog(lt, 2.0, 2.8)).toFixed(3));
    enter3d(card.c, lt, 0.1, 'flipDown'); shine(card.sh, lt, 2.8, 0.8);
    const v = rollValue(lt, 0.4, 2.7, 0, 355); od.set(v.v, v.speed);
    const hk = spring(lt, 2.75, 12, 4);
    heart.style.opacity = fadeIn(lt, 2.75, 0.1) * (1 - prog(lt, 3.6, 4.1));
    heart.style.transform = `translateY(${(-lerp(0, 80, prog(lt, 2.75, 4.1))).toFixed(1)}px) scale(${hk.toFixed(3)})`;
    sparkX(lt); sparkN(lt);
    setGrade(S, 0);
  };
  SHOTS.push(S);
})();

// =====================================================================
// F — kinetic title over the blurred room (14.6–17.0)
// =====================================================================
(() => {
  const S = new Shot(14.6, 17.0, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = momRoom3(S, false);
  room.xA.setAttribute('stroke-dashoffset', 0); room.xB.setAttribute('stroke-dashoffset', 0);
  S.grade = '';
  S.L.far.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 91, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const pill = html('div', 'pill', wrap); pill.innerHTML = '<svg width="16" height="16"><circle cx="8" cy="8" r="7" fill="#e0574b"/></svg>เดโม'; pill.style.left = '450px'; pill.style.top = '600px';
  const t1 = html('div', 'title', wrap); t1.style.top = '690px'; t1.style.font = '700 176px/1 Kanit';
  const digits = ['3', '5', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, ' วัน');
  const t2 = html('div', 'title', wrap, 'ที่แม่รอ'); t2.style.top = '885px'; t2.style.font = '600 124px/1 Kanit';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#e0574b', boxShadow: '0 0 16px rgba(224,87,75,.8)' });
  const c1 = html('div', 'title', wrap, 'เดโมสั้นจากบท "355 วันที่แม่รอ"'); c1.style.top = '1130px'; c1.style.font = '500 40px/1.3 Kanit'; c1.style.color = '#ffd166';
  const c2 = html('div', 'title', wrap, 'ฉบับเต็มยาวราว 70 วินาที'); c2.style.top = '1190px'; c2.style.font = '400 36px/1.3 Kanit'; c2.style.color = '#cfd2e6';
  const glint = html('div', '', wrap); glint.style.cssText = 'position:absolute;left:0;top:680px;width:260px;height:340px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));mix-blend-mode:overlay;opacity:0';
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, 2.4)), fx: 560, fy: 800 });
    room.update(lt + 4, { x: 885, y: 1235, s: 1.12, f: -1, torso: 4, head: -12, aF: [96, 94], aB: [60, -150], eyes: 1, smile: 0.9 });
    bok(lt);
    const f = (el, t0, dy = 24) => { const k = spring(lt, t0, 14, 7); el.style.opacity = fadeIn(lt, t0, 0.15); el.style.transform = `translateY(${((1 - k) * dy).toFixed(1)}px)`; };
    f(pill, 0.05);
    digits.forEach((d, i) => { const k = spring(lt, 0.15 + i * 0.09, 15, 6); d.style.opacity = fadeIn(lt, 0.15 + i * 0.09, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; d.style.filter = lt - (0.15 + i * 0.09) < 0.12 ? `blur(${(6 * (1 - (lt - 0.15 - i * 0.09) / 0.12)).toFixed(1)}px)` : 'none'; });
    f(unit, 0.45);
    t2.style.opacity = fadeIn(lt, 0.55, 0.1);
    t2.style.clipPath = `inset(0 ${((1 - ease.outCubic(prog(lt, 0.55, 1.0))) * 100).toFixed(1)}% 0 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.8, 1.2)).toFixed(3)})`;
    f(c1, 1.0); f(c2, 1.12);
    const gk = prog(lt, 1.2, 1.9);
    glint.style.opacity = gk > 0 && gk < 1 ? 1 : 0;
    glint.style.transform = `translateX(${(150 + gk * 700).toFixed(1)}px) skewX(-20deg)`;
    wrap.style.opacity = 1 - prog(lt, 2.0, 2.4);
    S.L.mid.el.style.opacity = 1 - prog(lt, 2.0, 2.4);
  };
  SHOTS.push(S);
})();

// global overlays: film grain, start fade, flash between B and C
const grainTick = makeGrain();
const black = html('div', 'blackout', frame);
const flash = html('div', 'blackout', frame); flash.style.background = '#fff6e0';

const DURATION = 17.0;
window.render = t => {
  for (const sh of SHOTS) {
    const on = t >= sh.a && t < sh.b;
    sh.root.style.display = on ? 'block' : 'none';
    if (on) sh.update(t - sh.a);
  }
  renderKinetic(subsBox, CUES, t);
  grainTick(t);
  black.style.opacity = (1 - prog(t, 0, 0.3)) + prog(t, 16.6, 17.0);
  flash.style.opacity = t >= 4.12 ? (0.32 * (1 - prog(t, 4.12, 4.3))).toFixed(3) : 0;
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
