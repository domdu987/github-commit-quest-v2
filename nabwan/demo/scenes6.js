// Demo v4 — rhymed narration (A1/B1/C1 takes at 0.50 / 14.75 / 30.35 s), ElevenLabs score, reunion ending.
// Every time below is on the global timeline and comes from the measured narration onsets.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');

const GIRL = { R: 44, skin: '#d8ab86', skinShade: '#c3936d', hair: '#2a2220', hairStyle: 'ponytail', shirt: '#7fa3cf', shirtLight: '#94b5dc', shirtDark: '#6e90bb', sleeve: 'long', shirtLen: 'top', pants: '#2c3555', pantsDark: '#232a45', seed: 1 };
const GIRL_PACK = Object.assign({}, GIRL, { backpack: '#2e3140' });
const MOM = { R: 44, skin: '#c8956e', skinShade: '#b3805b', hair: '#3a3234', gray: '#b5aeae', hairStyle: 'bun', shirt: '#a84d63', shirtLight: '#bb5d73', shirtDark: '#8f4054', sleeve: 'short', shirtLen: 'top', sarong: '#5b3f7a', sarongDark: '#463063', pants: '#5b3f7a', pantsDark: '#4a3266', shoe: '#7b5236', shoeDark: '#5f3e28', earring: null, glasses: true, lashes: false, seed: 2 };
const SIL = { R: 44, skin: '#171827', skinShade: '#141523', hair: '#121320', hairStyle: 'short', shirt: '#1a1b2b', shirtLight: '#1c1d2e', shirtDark: '#151624', sleeve: 'long', shirtLen: 'long', pants: '#141522', pantsDark: '#121320', shoe: '#141522', shoeDark: '#121320', earring: null, lashes: false, flat: true };

// narration landmarks (global seconds)
const P_V4 = {
  thakhun: 0.57, tamngan: 1.86, hang: 3.74, kwa: 5.42, kor: 6.46, song: 7.14, khoei: 9.11, wa: 10.46, ja: 11.97, eek: 13.42,
  sigh: 14.79, pi: 15.75, dai: 17.12, kae: 19.43, sip: 19.71, tae: 21.83, nap: 22.95, sam: 24.07, hawan: 25.31, doi: 26.72,
  mai1: 30.42, mai2: 31.90, pimai: 32.55, wang: 33.91, klap: 34.86, pro: 37.54, maidai: 38.38, taerao: 40.14, luk: 40.83, tuk: 41.51,
};
const CUES_V4 = [
  { a: 0.57, b: 3.30, parts: [{ t: 'ถ้าคุณทำงานไกลบ้าน', s: 'w', at: 0.57, d: 2.5 }] },
  { a: 3.74, b: 5.28, parts: [{ t: 'ห่างกันนาน', s: 'w', at: 3.74, d: 1.0 }] },
  { a: 5.42, b: 8.60, parts: [{ t: 'กว่าจะได้กลับ ก็แค่ปีละ', s: 'w', at: 5.42, d: 2.2 }, { t: '2 ครั้ง', s: 'r', at: 7.12, d: 0.6 }] },
  { a: 9.11, b: 10.40, parts: [{ t: 'เคยนับบ้างไหม', s: 'w', at: 9.11, d: 0.9 }] },
  { a: 10.46, b: 13.36, parts: [{ t: 'ว่าเวลาที่ยังเหลือ', s: 'w', at: 10.46, d: 1.24 }, { t: ' จะได้เจอพ่อแม่', s: 'w', at: 11.97, d: 1.25 }] },
  { a: 13.42, b: 14.50, parts: [{ t: 'อีกกี่วัน', s: 'r', at: 13.42, d: 0.84 }] },
  { a: 15.75, b: 19.36, parts: [{ t: 'ปีหนึ่ง', s: 'y', at: 15.75, d: 0.7 }, { t: ' ได้อยู่บ้านพร้อมหน้ากัน', s: 'y', at: 17.12, d: 1.6 }] },
  { a: 19.43, b: 21.40, parts: [{ t: 'แค่', s: 'w', at: 19.43, d: 0.3 }, { t: '10 วัน', s: 'r', at: 19.69, d: 0.7 }] },
  { a: 21.83, b: 23.98, parts: [{ t: 'แต่แม่', s: 'w', at: 21.83, d: 0.6 }, { t: 'นับวันรอ', s: 'w', at: 22.95, d: 0.92 }] },
  { a: 24.07, b: 26.45, parts: [{ t: '355 วัน', s: 'r', at: 24.07, d: 1.7 }] },
  { a: 26.72, b: 27.95, parts: [{ t: 'โดยไม่เคยท้อ', s: 'y', at: 26.72, d: 1.15 }] },
  { a: 30.42, b: 31.86, parts: [{ t: 'ไม่ต้องรอสงกรานต์', s: 'w', at: 30.42, d: 1.29 }] },
  { a: 31.90, b: 33.86, parts: [{ t: 'ไม่ต้องรอปีใหม่', s: 'w', at: 31.90, d: 1.61 }] },
  { a: 33.91, b: 34.72, parts: [{ t: 'ว่างเมื่อไหร่', s: 'y', at: 33.91, d: 0.76 }] },
  { a: 34.86, b: 36.80, top: 1650, parts: [{ t: 'กลับไปหาแม่เถอะนะ', s: 'y', at: 34.86, d: 1.33 }] },
  { a: 37.54, b: 40.05, top: 1650, parts: [{ t: 'เพราะแม่', s: 'w', at: 37.54, d: 0.65 }, { t: 'ไม่ได้รอแค่วันหยุด', s: 'w', at: 38.38, d: 1.33 }] },
  { a: 40.14, b: 42.55, top: 1650, parts: [{ t: 'แต่รอลูก', s: 'w', at: 40.14, d: 1.09 }, { t: 'ทุกวัน', s: 'r', at: 41.51, d: 0.76 }] },
];

// v5 narration (Gemini Charon) supplies its own landmarks via vo5.js; v4 values are the fallback
const P = typeof VO5 !== 'undefined' ? VO5.P : P_V4;
const CUES = typeof VO5 !== 'undefined' ? VO5.CUES : CUES_V4;

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
  <path d="M-7,19 Q0,25 7,19" stroke="#8a4a3c" stroke-width="2.6" fill="none" stroke-linecap="round"/>
  <path d="M-34,48 C-30,36 30,36 34,48 Z" fill="#a84d63"/></svg>`;
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
const whip = (shot, lt, side) => { // side: 'out' at end of shot, 'in' at start
  let k = 0, dx = 0;
  if (side === 'out') { k = clamp((lt - (shot.b - shot.a - 0.09)) / 0.09); dx = -ease.inCubic(k) * 520; }
  else { k = 1 - clamp(lt / 0.09); dx = ease.inCubic(k) * 520; }
  shot.root.style.transform = `translateX(${dx.toFixed(1)}px)`;
  return k;
};
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
const leafG = (R, x, y, s, a, c, vein = '#3e3448') => {
  const g = svg('g', { transform: `translate(${x},${y}) rotate(${a}) scale(${s})` }, R.s);
  svg('path', { d: 'M0,0 C60,-70 210,-80 270,0 C210,90 60,80 0,0 Z', fill: c }, g);
  svg('path', { d: 'M8,0 L262,0', stroke: shade(c, 30), 'stroke-width': 6 }, g);
  for (const kx of [70, 130, 190]) svg('path', { d: `M${kx},-40 L${kx + 20},-6 M${kx},40 L${kx + 20},6`, stroke: vein, 'stroke-width': 10 }, g);
  return g;
};
const swayLeaves = (leaves, t) => leaves.forEach((g, i) => { const base = g.getAttribute('transform').replace(/ skewX\([^)]*\)/, ''); g.setAttribute('transform', `${base} skewX(${(Math.sin(t * 1.2 + i) * 1.5).toFixed(2)})`); });

// =====================================================================
// S1 — condo at night: Mom's message, the way home, days away (0.00–5.30)
// =====================================================================
(() => {
  const S = new Shot(0, 5.30, [['far', 0.35, 1.2], ['mid', 1, 0], ['fore', 1.9, 13]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const F = S.L.far, M = S.L.mid, R = S.L.fore;
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
  const leaves = [leafG(R, -120, 1880, 1.6, -60, '#1d3a2d'), leafG(R, -80, 1900, 1.5, -25, '#24473a'), leafG(R, -160, 1700, 1.4, -5, '#2b5243'), leafG(R, -60, 1960, 1.3, -88, '#1a3328')];
  svg('circle', { cx: 1040, cy: 200, r: 90, fill: '#ffcf8a', opacity: 0.25 }, R.s);
  svg('circle', { cx: 900, cy: 90, r: 60, fill: '#ffe2b0', opacity: 0.2 }, R.s);
  // UI
  const clock = cardEl(S.ui, 'clock', 56, 110);
  clock.c.innerHTML += `<div class="icslot"></div><div><div class="tl">อังคาร</div><div class="tt"><span>21:</span><span class="mm"></span></div><div class="sl"><i style="left:68%"></i></div></div>`;
  const mm = new Odometer(clock.c.querySelector('.mm'), 2);
  const clk = clockMoon(clock.c.querySelector('.icslot'), 82);
  const bat = html('div', 'pill', S.ui); bat.style.left = '752px'; bat.style.top = '126px';
  bat.innerHTML = `<svg width="56" height="30" viewBox="0 0 56 30"><rect x="2" y="3" width="46" height="24" rx="6" fill="none" stroke="#fff" stroke-width="3"/><rect x="50" y="10" width="4" height="10" rx="2" fill="#fff"/><rect class="bf" x="6" y="7" width="5" height="16" rx="3" fill="#ff5e52"/></svg><b>3%</b>`;
  bat.querySelector('svg').remove();
  const batI = batteryIcon(html('span', '', bat)); bat.prepend(batI.el.parentNode);
  const n = html('div', 'notif', S.ui); n.style.top = '270px';
  n.innerHTML = `<div class="app">ข้อความ</div><div class="av"><div class="avring5"></div>${momAvatar()}<i class="online5"></i></div><div style="flex:1"><div class="who">แม่ <span class="hh"></span><small>เมื่อสักครู่</small></div><div class="msg"></div></div>`;
  const msg = n.querySelector('.msg'), av = n.querySelector('.av'), hh = n.querySelector('.hh');
  const avRing = n.querySelector('.avring5'), online = n.querySelector('.online5');
  const hbt = heartBeat(hh, 34);
  const typ = typingDots(msg.parentNode); msg.parentNode.insertBefore(typ.el, msg);
  const MSG = graphemes('สงกรานต์นี้กลับบ้านมั้ยลูก');
  const route = routeCard2(S.ui, 110, 462, 860);
  const days = daysChip2(S.ui, 110, 800, 'ห่างบ้านมาแล้ว', 84);
  const fxs = fxSvg(S);
  const sparkA = burst(fxs, 158, 322, 0.66, 16, 5, ['#ffd66b', '#ffffff', '#ff9fb2'], 230, 0.8);
  const sparkR = burst(fxs, 880, 590, 2.95, 16, 8, ['#ff7a6a', '#ffd66b', '#ffffff'], 220, 0.8);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, 5.3));
    S.cam({ x: lerp(-30, 30, k), y: 0, z: lerp(1.0, 1.1, k), fx: 430, fy: 1000 });
    twinkles.forEach(w => w.el.setAttribute('opacity', (Math.sin((lt + w.ph) * w.rate * 6) > -0.85 ? 0.85 : 0.15)));
    setA(plane, { cx: 160 + lt * 70, cy: 300 - lt * 12, opacity: Math.sin(lt * 9) > 0.3 ? 1 : 0.15 });
    const look = ease.inOutSine(prog(lt, 3.55, 4.2));
    const br = Math.sin(lt * 2.2) * 1.2, scroll = Math.sin(lt * 10) * 3 * (lt > 0.8 && lt < 3.4 ? 1 : 0);
    p.pose({ x: 352, y: 1162, torso: 6 + br, head: lerp(18, -12, look), aF: [lerp(76, 70, look), lerp(-46 + scroll, 6, look)], aB: [80, -40 + 40 * look], lF: [-2, 90], lB: [0, 91], t: lt + 0.7, smile: lerp(lerp(0.35, 0.75, prog(lt, 0.7, 1.1)), 0.2, look) });
    const w = p.wristF;
    setA(glow, { cx: 352 + w[0] + 10, cy: 1162 + w[1] - 26, opacity: (0.8 + 0.2 * Math.sin(lt * 13)) * (1 - 0.5 * look) });
    scr.setAttribute('fill', lt > 0.22 && lt < 0.5 ? '#ffffff' : '#d8e8ff');
    const vk = lt > 0.2 && lt < 0.75 ? 1 : 0;
    vib.setAttribute('opacity', vk * (0.55 + 0.45 * Math.sin(lt * 40)));
    vib.setAttribute('transform', `translate(${352 + w[0]},${1162 + w[1] - 14})`);
    ph.setAttribute('transform', `translate(${vk ? Math.sin(lt * 120) * 3 : 0},0)`);
    dustA(lt + 4);
    swayLeaves(leaves, lt);
    enter3d(clock.c, lt, 0.05, 'flipDown'); shine(clock.sh, lt, 0.45);
    const m = rollValue(lt, 0.45, 1.0, 39, 40); mm.set(m.v, m.speed);
    clk.update(lt, 21, m.v); popSquash(clk.el, lt, 0.2);
    enter3d(bat, lt, 0.12, 'pop'); batI.update(lt, 0.2);
    const kn = spring(lt, 0.28, 13, 6);
    n.style.opacity = fadeIn(lt, 0.28, 0.12);
    n.style.transform = `translateY(${((1 - kn) * -220).toFixed(1)}px) rotateX(${((1 - kn) * 25).toFixed(2)}deg)`;
    av.style.transform = `scale(${spring(lt, 0.42, 16, 6).toFixed(3)})`;
    hh.style.display = 'inline-block';
    hh.style.transform = `scale(${clamp(spring(lt, 0.5, 18, 6), 0, 1.3).toFixed(3)})`;
    hbt.update(lt);
    avRing.style.transform = `rotate(${(lt * 140).toFixed(1)}deg)`; avRing.style.opacity = fadeIn(lt, 0.45, 0.2);
    popSquash(online, lt, 0.7, '', 0);
    typ.update(lt, lt > 0.34 && lt < 0.6);
    msg.textContent = MSG.slice(0, Math.floor(clamp((lt - 0.6) / 0.6) * MSG.length)).join('');
    route.update(lt, P.tamngan - 0.08);
    days.update(lt, P.hang - 0.06);
    sparkA(lt); sparkR(lt);
    const out = whip(S, lt, 'out');
    setGrade(S, out * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — bus terminal: the bus pulls in, "twice a year" (5.30–8.98)
// =====================================================================
(() => {
  const S = new Shot(5.30, 8.98, [['far', 0.3, 5], ['mid', 1, 0], ['fore', 2.2, 14]]);
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
  svg('rect', { x: -300, y: 1110, width: 1680, height: 1300, fill: lin(M.defs, [[0, '#343a52'], [1, '#1e2234']]) }, M.s);
  const refl = svg('g', { filter: blurFilter(M.defs, 9), opacity: 0.55 }, M.s);
  for (let i = 0; i < 10; i++) svg('rect', { x: 20 + i * 112, y: 1170, width: 80, height: 260, rx: 30, fill: '#c9b48f', opacity: 0.22 }, refl);
  svg('rect', { x: -300, y: 1110, width: 1680, height: 22, fill: '#d6ad52' }, M.s);
  svg('rect', { x: -300, y: 1150, width: 1680, height: 8, fill: '#d6ad52', opacity: 0.5 }, M.s);
  const busWrap = svg('g', {}, M.s);
  const bus = tourBus(busWrap, M.defs, -40, 1100, 1180, 'กรุงเทพฯ - ขอนแก่น');
  const puffs = Array.from({ length: 8 }, (_, i) => ({ el: svg('circle', { r: 20, fill: '#9aa0b8' }, M.s), b: i * 0.22 }));
  const sils = [[870, 0.5, 0], [925, 0.52, 1]].map(([x, sc, k]) => ({ q: new Puppet(M.s, Object.assign({}, SIL, { hairStyle: k ? 'ponytail' : 'short', hairTie: '#121320' }), M.defs), x, sc, k }));
  contactShadow(M.s, M.defs, 330, 1478, 110, 14, 0.5);
  const p = new Puppet(M.s, GIRL_PACK, M.defs);
  const ph = svg('g', {}, p.prop);
  svg('rect', { x: -15, y: -42, width: 30, height: 58, rx: 7, fill: '#15151b' }, ph);
  svg('rect', { x: -11, y: -38, width: 22, height: 50, rx: 4, fill: '#d8e8ff' }, ph);
  const glow = svg('circle', { r: 120, fill: rad2(M.defs, [[0, '#cfe1ff', 0.45], [1, '#cfe1ff', 0]]) }, M.s);
  const sweep = svg('rect', { x: 0, y: 760, width: 200, height: 360, fill: lin(M.defs, [[0, '#fff2cc', 0], [0.5, '#fff2cc', 0.3], [1, '#fff2cc', 0]], 1, 0) }, M.s);
  vignette(M.s, M.defs, 0.5);
  svg('rect', { x: 990, y: -300, width: 160, height: 2600, fill: '#141726' }, R.s);
  svg('rect', { x: 990, y: -300, width: 20, height: 2600, fill: '#2a2f48' }, R.s);
  const bok = floaters(R.s, [-100, 0, 1300, 500], 7, 9, { color: '#ffd9a0', rMin: 20, rMax: 46, speed: 4, op: 0.18, base: 0.05, amp: 10 });
  const clock = cardEl(S.ui, 'clock', 56, 110);
  clock.c.innerHTML += `<div class="icslot"></div><div><div class="tl">ศุกร์</div><div class="tt">20:30</div><div class="sl"><i style="left:62%"></i></div></div>`;
  const clk = clockMoon(clock.c.querySelector('.icslot'), 82);
  const led = html('div', 'led', S.ui); led.style.left = '56px'; led.style.top = '300px';
  led.innerHTML = `<div class="a"><span>20:30</span><span>ขอนแก่น</span></div><div class="b">กำลังขึ้นรถ</div>`;
  const ledB = led.querySelector('.b');
  const card = cardEl(S.ui, 'card', 640, 110); card.c.style.minWidth = '340px';
  const clb = html('div', 'lbl', card.c); const hI = houseIcon(clb, 60); html('span', '', clb, 'กลับบ้าน');
  const num = html('div', 'num', card.c);
  const od = new Odometer(num, 1); html('small', '', num, 'ครั้ง/ปี');
  const chip1 = html('div', 'chip', S.ui); chip1.innerHTML = `<span class="ics"></span>สงกรานต์`; chip1.style.left = '640px'; chip1.style.top = '420px';
  const chip2 = html('div', 'chip', S.ui); chip2.innerHTML = `<span class="ics"></span>ปีใหม่`; chip2.style.left = '860px'; chip2.style.top = '420px';
  const wb = waterBowlMini(chip1.querySelector('.ics'), 48), fw = fireworkMini(chip2.querySelector('.ics'), 48);
  const fxs = fxSvg(S);
  const lt0 = P.kor - 5.30;
  const spark0 = burst(fxs, 820, 240, P.song - 5.30 + 0.06, 16, 11, ['#ffd66b', '#fff', '#ff9fb2'], 220, 0.7);
  const spark1 = burst(fxs, 720, 450, lt0 + 1.24, 10, 13, ['#ffd66b', '#fff'], 170, 0.6);
  const spark2 = burst(fxs, 920, 450, lt0 + 1.49, 10, 17, ['#9cc0ff', '#fff'], 170, 0.6);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, 3.68));
    S.cam({ x: lerp(-20, 40, k), y: 0, z: lerp(1.0, 1.08, k), fx: 330, fy: 1150 });
    const arrive = ease.outCubic(prog(lt, 0, 1.15));
    const bx = (1 - arrive) * 1150;
    busWrap.setAttribute('transform', `translate(${bx.toFixed(1)},${(Math.sin(lt * 31) * 0.8).toFixed(2)})`);
    const roll = (1 - Math.pow(1 - prog(lt, 0, 1.15), 2)) * -560;
    bus.wheels.forEach(wh => { const m = wh.getAttribute('transform').match(/translate\(([^)]+)\)/)[1]; wh.setAttribute('transform', `translate(${m}) rotate(${roll.toFixed(1)})`); });
    puffs.forEach(pf => { const a = ((lt - pf.b) % 1.76 + 1.76) % 1.76; setA(pf.el, { cx: bx - 30 - a * 60, cy: 1060 - a * 80, r: 14 + a * 40, opacity: (0.35 * (1 - a / 1.76) * arrive).toFixed(3) }); });
    sils.forEach(({ q, x, sc, k }) => q.pose({ x, y: 1100 - 300 * sc, s: sc, f: k ? -1 : 1, torso: 2 + Math.sin(lt * 2 + k) * 1, head: 4, aF: [96, 94], aB: [92, 90], eyes: 1 }));
    const look = ease.inOutSine(prog(lt, 0.5, 0.95));
    p.pose({ x: 330, y: 1172, s: 1.02, torso: 3 + Math.sin(lt * 2) * 1, head: lerp(16, -6, look), aF: [80, -30], aB: [96, 94], lF: [88, 90], lB: [93, 92], t: lt + 2.1, smile: lerp(0.45, 0.8, look) });
    const w = p.wristF;
    setA(glow, { cx: 330 + w[0] * 1.02 + 10, cy: 1172 + w[1] * 1.02 - 24 });
    sweep.setAttribute('x', (1100 - ((lt * 0.9) % 1.6) / 1.6 * 1500).toFixed(1));
    bok(lt);
    enter3d(clock.c, lt, 0.12, 'flipDown'); shine(clock.sh, lt, 0.5);
    enter3d(led, lt, 0.2, 'flipDown');
    ledB.style.opacity = Math.sin(lt * 12) > -0.2 ? 1 : 0.15;
    enter3d(card.c, lt, lt0 - 0.08, 'swingRight'); shine(card.sh, lt, lt0 + 1.0);
    const v = rollValue(lt, lt0 + 0.3, P.song - 5.30 + 0.06, 0, 2); od.set(v.v, v.speed);
    popSquash(chip1, lt, lt0 + 1.2); popSquash(chip2, lt, lt0 + 1.45);
    wb.update(lt); fw.update(lt);
    clk.update(lt, 20, 30 + lt / 60); popSquash(clk.el, lt, 0.25);
    hI.update(lt); popSquash(hI.el, lt, lt0 + 0.15);
    spark0(lt); spark1(lt); spark2(lt);
    const inK = whip(S, lt, 'in');
    setGrade(S, inK * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — night highway: "?", hourglass, Mom & Dad, red alert, zoom into her window (8.98–14.65)
// =====================================================================
(() => {
  const A = 8.98;
  const S = new Shot(A, 14.65, [['sky', 0.1, 0.8], ['far', 0.3, 2.5], ['mid', 1, 0], ['fore', 1.6, 12]]);
  S.grade = 'saturate(1.1) contrast(1.05)';
  const K = S.L.sky, F = S.L.far, M = S.L.mid, R = S.L.fore;
  const OY = 250;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2500, fill: lin(K.defs, [[0, '#121634'], [0.55, '#262a58'], [1, '#141733']]) }, K.s);
  const r = rng(5);
  for (let i = 0; i < 110; i++) svg('circle', { cx: -100 + r() * 1280, cy: -100 + r() * 1100, r: 0.8 + r() * 2.2, fill: '#fff', opacity: 0.2 + r() * 0.6 }, K.s);
  svg('circle', { cx: 860, cy: 330, r: 120, fill: rad2(K.defs, [[0, '#fff3d6', 0.35], [1, '#fff3d6', 0]]) }, K.s);
  svg('circle', { cx: 860, cy: 330, r: 46, fill: '#f6eed8' }, K.s);
  const sky = svg('g', {}, F.s);
  let x = -300;
  while (x < 2600) {
    const w = 60 + r() * 110, h = 120 + r() * 260;
    svg('rect', { x, y: OY + 1150 - 180 - h, width: w, height: h + 200, fill: '#1c1f43' }, sky);
    for (let k = 0; k < 6; k++) if (r() > 0.4) svg('rect', { x: x + 8 + r() * (w - 16), y: OY + 1150 - 160 - h + r() * h, width: 5, height: 7, fill: '#f6c86a', opacity: 0.7 }, sky);
    x += w + 10;
  }
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
  const fore = svg('g', {}, R.s);
  for (let i = 0; i < 6; i++) {
    svg('rect', { x: i * 420, y: 1500, width: 70, height: 700, rx: 10, fill: '#0c0d1f' }, fore);
    svg('ellipse', { cx: i * 420 + 220, cy: 1880, rx: 200, ry: 120, fill: '#0e1124' }, fore);
  }
  // UI row: "?" (moves left) · hourglass · Mom & Dad
  const fxs = fxSvg(S);
  const qfx = svg('g', {}, fxs);
  const rings = Array.from({ length: 3 }, () => svg('circle', { r: 100, fill: 'none', 'stroke-width': 6 }, qfx));
  const orb = [0, 1, 2].map(i => svg('circle', { r: 6, fill: i === 1 ? '#ffd66b' : '#fff' }, qfx));
  const sparkQ = burst(qfx, 0, 0, P.khoei - A + 0.2, 14, 23, ['#ffffff', '#ffd66b', '#cfd2ff'], 280, 0.8);
  const sparkRed = burst(qfx, 0, 0, P.eek - A + 0.1, 18, 29, ['#ff5a4e', '#ffd66b', '#ffffff'], 300, 0.8);
  const qw = html('div', 'qwrap', S.ui);
  const q = html('div', 'qmark', qw, '?');
  const hg = hourglass(S.ui, 440, 640);
  const mom = avatarBadge(S.ui, 690, 610, momAvatar(), 'แม่', '#e0577a');
  const dad = avatarBadge(S.ui, 850, 660, dadAvatar(), 'พ่อ', '#4a7bd8');
  mom.el.classList.add('big'); dad.el.classList.add('big');
  const pw = html('div', '', S.ui); pw.style.cssText = 'position:absolute;left:806px;top:600px';
  const phb = heartBeat(pw, 60);
  const link = svg('path', { d: 'M640,780 Q680,740 700,730', fill: 'none', stroke: '#ffd66b', 'stroke-width': 4, 'stroke-dasharray': '4 10', 'stroke-linecap': 'round', opacity: 0 }, fxs);
  const tq = P.khoei - A, th = P.wa - A, tp = P.ja - A, tr = P.eek - A;
  S.update = lt => {
    const zt = prog(lt, 5.30, 5.67);
    const zz = lerp(1.0, 1.05, ease.inOutSine(prog(lt, 0, 5.3))) * (1 + 5 * ease.inCubic(zt));
    S.cam({ x: 0, y: Math.sin(lt * 1.3) * 4, z: zz, fx: zt > 0 ? winX : 540, fy: zt > 0 ? winY : 1250 });
    lamps.setAttribute('transform', `translate(${-((lt * 300) % 360)},0)`);
    refl.setAttribute('transform', `translate(${-((lt * 300) % 360)},0)`);
    rail.setAttribute('transform', `translate(${-((lt * 700) % 160)},0)`);
    fore.setAttribute('transform', `translate(${-((lt * 1500) % 420)},0)`);
    sky.setAttribute('transform', `translate(${-lt * 18},0)`);
    sweep.setAttribute('x', (1100 - ((lt * 300 + 40) % 360) * 3.4).toFixed(1));
    trails.forEach(tr2 => { const k = ((lt + tr2.ph) % 1.1) / 1.1; setA(tr2.el, { x: (1300 - k * 1900).toFixed(1), width: tr2.w }); });
    bus.g.setAttribute('transform', `translate(0,${(Math.sin(lt * 9) * 1.6).toFixed(2)})`);
    bus.wheels.forEach(wh => { const m = wh.getAttribute('transform').match(/translate\(([^)]+)\)/)[1]; wh.setAttribute('transform', `translate(${m}) rotate(${(lt * 420) % 360})`); });
    head.setAttribute('opacity', 0.85 + 0.15 * Math.sin(lt * 7));
    // "?" pops centre, then slides left when the hourglass arrives
    const k = spring(lt, tq + 0.04, 14, 5.5);
    const sq = 1 + (k - 1) * 0.6;
    const bob = Math.sin(lt * 2.2) * 10;
    const mv = ease.inOutCubic(prog(lt, th - 0.12, th + 0.3));
    const qx = lerp(540, 250, mv), qy = 760, qs = lerp(1, 0.86, mv);
    const alarm = lt > tr ? Math.exp(-(lt - tr) * 2.2) : 0, red = lt > tr ? 1 : 0;
    const shake = alarm > 0.05 ? Math.sin(lt * 70) * 10 * alarm : 0;
    qw.style.left = (qx - 100).toFixed(1) + 'px'; qw.style.top = (qy - 100).toFixed(1) + 'px';
    qw.style.opacity = fadeIn(lt, tq + 0.04, 0.1) * (1 - zt);
    qw.style.transform = `translate(${shake.toFixed(1)}px, ${bob.toFixed(1)}px) scale(${(qs * k * (2 - sq)).toFixed(3)}, ${(qs * k * sq).toFixed(3)})`;
    q.style.color = red ? '#e2382c' : '#cf483d';
    q.style.boxShadow = `0 0 ${(40 + 70 * alarm + 20 * red).toFixed(0)}px rgba(${red ? '255,80,60' : '255,255,255'},${(0.35 + 0.45 * alarm + 0.1 * red).toFixed(2)}), 0 24px 40px rgba(0,0,0,.45)`;
    qfx.setAttribute('transform', `translate(${(qx + shake).toFixed(1)},${(qy + bob).toFixed(1)}) scale(${qs.toFixed(3)})`);
    rings.forEach((rg, i) => {
      const per = red ? 0.9 : 1.5, kk = ((lt + i * per / 3) % per) / per;
      setA(rg, { r: (100 + kk * 150).toFixed(1), stroke: red ? '#ff5a4e' : '#d8d4ea', opacity: ((1 - kk) * 0.6 * clamp(k) * (1 - zt)).toFixed(3), 'stroke-width': (8 - 6 * kk).toFixed(2) });
    });
    orb.forEach((o, i) => { const a = lt * 2.4 + i * 2.1; setA(o, { cx: Math.cos(a) * 140, cy: Math.sin(a) * 50, opacity: clamp(k) * (1 - zt) * 0.9 }); });
    sparkQ(lt); sparkRed(lt);
    hg.update(lt, th, red);
    hg.el.style.opacity = (parseFloat(hg.el.style.opacity) * (1 - zt)).toFixed(3);
    mom.update(lt, tp); dad.update(lt, tp + 0.14);
    mom.el.style.opacity = (parseFloat(mom.el.style.opacity) * (1 - zt)).toFixed(3);
    dad.el.style.opacity = (parseFloat(dad.el.style.opacity) * (1 - zt)).toFixed(3);
    link.setAttribute('opacity', (fadeIn(lt, tp + 0.3, 0.2) * (1 - zt) * 0.9).toFixed(3));
    link.setAttribute('stroke-dashoffset', (-lt * 30).toFixed(1));
    phb.update(lt); popSquash(pw, lt, tp + 0.35); pw.style.opacity = (parseFloat(pw.style.opacity) * (1 - zt)).toFixed(3);
    setGrade(S, zt * 14);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — inside the bus: sigh, 1 year = 365 days, only 10 at home; push into the moon (14.65–22.00)
// =====================================================================
(() => {
  const A = 14.65;
  const S = new Shot(A, 22.0, [['far', 0.4, 9], ['mid', 1, 5]]);
  S.grade = 'saturate(1.05)';
  const set = busNight(S);
  const M = S.L.mid;
  const p = new Puppet(M.s, GIRL, M.defs);
  const lightSweep = svg('rect', { x: 0, y: 150, width: 260, height: 1300, fill: lin(M.defs, [[0, '#ffd590', 0], [0.5, '#ffd590', 0.22], [1, '#ffd590', 0]], 1, 0) }, M.s);
  vignette(M.s, M.defs, 0.6);
  const card = cardEl(S.ui, 'card pink', 64, 190, 952);
  html('div', 'lbl', card.c, '1 ปี = 365 วัน');
  const grid = html('div', 'waffle', card.c);
  const cells = [];
  for (let i = 0; i < 365; i++) cells.push(html('i', '', grid));
  const leg = html('div', 'legend', card.c);
  const l1 = html('div', 'gold', leg); const lh = houseIcon(l1, 58); l1.append('อยู่บ้าน ');
  const b1 = html('b', '', l1); const o1 = new Odometer(b1, 2); l1.append(' วัน');
  const l2 = html('div', 'gray', leg); const lb = buildingIcon(l2, 54); l2.append('อยู่กรุงเทพฯ ');
  const o2 = new Odometer(html('b', '', l2), 3); l2.append(' วัน');
  const order = [101, 102, 103, 104, 105, 363, 364, 0, 1, 2];
  const fxs = fxSvg(S);
  const pos = idx => [64 + 10 + 32 + (idx % 26) * 33 + 14, 190 + 22 + 58 + 22 + Math.floor(idx / 26) * 33 + 14];
  const tPi = P.pi - A, tDai = P.dai - A, tSip = P.sip - A;
  const litT = k => tDai + 0.08 + k * 0.15;
  const bursts = order.map((idx, k) => { const [cx, cy] = pos(idx); return burst(fxs, cx, cy, litT(k), 7, 40 + k, ['#ffd66b', '#fff4c2'], 90, 0.45); });
  const bigBurst = burst(fxs, 250, 820, tSip + 0.02, 20, 91, ['#ffd66b', '#ffffff', '#ff9fb2'], 260, 0.9);
  S.update = lt => {
    // settle from the zoom-through, hold, then push into the moon outside (rack focus far layer)
    const zin = 1 - prog(lt, 0, 0.35);
    const push = ease.inCubic(prog(lt, 6.0, 7.35));
    const z = (1 + 0.35 * ease.outCubic(zin)) * (1 + 3.5 * push);
    S.cam({ x: 0, y: 0, z, fx: push > 0 ? 940 : 520, fy: push > 0 ? 320 : 900 });
    const fb = lerp(9, 0, ease.inOutSine(prog(lt, 5.9, 6.7)));
    S.L.far.el.style.filter = `blur(${fb.toFixed(1)}px)`;
    S.L.mid.el.style.filter = `blur(${lerp(5, 12, push).toFixed(1)}px)`;
    set.moonGlow.setAttribute('r', (120 + 60 * push).toFixed(1));
    setGrade(S, zin * 10);
    set.update(lt);
    lightSweep.setAttribute('x', (1200 - ((lt * 1.0 + 0.3) % 1.2) / 1.2 * 1700).toFixed(1));
    const sighK = Math.sin(Math.PI * prog(lt, P.sigh - A, P.sigh - A + 0.95));
    const wake = ease.inOutSine(prog(lt, 1.15, 1.6));
    p.pose({ x: 470, y: 1250, torso: -4 - 5 * sighK, head: lerp(-8, -18, wake) + 4 * sighK + Math.sin(lt * 5) * 1.0, aF: [80, 12], aB: [84, 16], lF: [-4, 88], lB: [-2, 90], eyes: lt < 1.2 ? 0 : null, t: lt + 3, smile: lerp(0.3, 0.15, wake) });
    // card exits up before the push
    const out = ease.inCubic(prog(lt, 5.75, 6.25));
    enter3d(card.c, lt, tPi - 0.05, 'swingLeft', `translateY(${(-out * 900).toFixed(1)}px) rotateX(${(out * 35).toFixed(1)}deg)`);
    card.c.style.opacity = (fadeIn(lt, tPi - 0.05, 0.14) * (1 - out)).toFixed(3);
    shine(card.sh, lt, tSip + 0.2, 0.8);
    cells.forEach((c, i) => {
      const d = tPi + 0.1 + ((i % 26) + Math.floor(i / 26)) * 0.012;
      const k = spring(lt, d, 20, 8);
      c.style.transform = `scale(${clamp(k, 0, 1.3).toFixed(3)})`;
    });
    const dim = ease.inOutSine(prog(lt, tSip - 0.05, tSip + 0.4));
    grid.style.setProperty('--off', `rgba(185,176,160,${(1 - 0.45 * dim).toFixed(3)})`);
    order.forEach((idx, k) => {
      const t0 = litT(k), on = lt >= t0;
      cells[idx].className = on ? 'on' : '';
      if (on) cells[idx].style.transform = `scale(${(1 + 0.55 * Math.exp(-(lt - t0) * 9) + 0.35 * Math.exp(-Math.pow((lt - tSip - 0.05 - k * 0.02) * 6, 2))).toFixed(3)})`;
    });
    bursts.forEach(b => b(lt)); bigBurst(lt);
    const v1 = rollValue(lt, litT(0), litT(9) + 0.1, 0, 10); o1.set(v1.v, v1.speed);
    const v2 = rollValue(lt, litT(0), litT(9) + 0.1, 365, 355); o2.set(v2.v, v2.speed);
    const pulse = 1 + 0.55 * Math.exp(-Math.pow((lt - tSip - 0.12) * 4.2, 2));
    b1.style.display = 'inline-block';
    lh.update(lt); lb.update(lt);
    const hj = lt > tSip ? Math.exp(-(lt - tSip) * 4) * Math.abs(Math.sin((lt - tSip) * 14)) : 0;
    lh.el.style.transform = `translateY(${(-hj * 22).toFixed(1)}px) scale(${(1 + 0.25 * hj).toFixed(3)})`;
    b1.style.transform = `scale(${pulse.toFixed(3)})`;
    b1.style.textShadow = `0 0 ${(30 * (pulse - 1) / 0.55).toFixed(1)}px rgba(240,180,60,.9)`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// shared: Mom's wooden room, layered (from v3, plus a moon that matches S4's)
// =====================================================================
function momRoom4(S, withFore = true) {
  const F = S.L.far, M = S.L.mid;
  const tones = ['#8a6143', '#7f573a', '#906746', '#86603f'];
  for (let i = -3; i < 16; i++) {
    svg('rect', { x: i * 84, y: -300, width: 84, height: 1680, fill: tones[(i + 12) % 4] }, F.s);
    svg('rect', { x: i * 84, y: -300, width: 3, height: 1680, fill: '#634229', opacity: 0.6 }, F.s);
  }
  svg('rect', { x: 770, y: 230, width: 250, height: 330, rx: 6, fill: '#4b3220' }, F.s);
  svg('rect', { x: 784, y: 244, width: 222, height: 302, fill: lin(F.defs, [[0, '#141636'], [1, '#2c2d5a']]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 120, fill: rad2(F.defs, [[0, '#fff3d6', 0.5], [1, '#fff3d6', 0]]) }, F.s);
  svg('circle', { cx: 940, cy: 320, r: 26, fill: '#f6eed8' }, F.s);
  svg('circle', { cx: 931, cy: 313, r: 5, fill: '#e6dcc0' }, F.s);
  svg('circle', { cx: 949, cy: 330, r: 3.5, fill: '#e6dcc0' }, F.s);
  const flies = floaters(F.s, [790, 400, 210, 140], 9, 61, { color: '#fff59a', rMin: 2, rMax: 4, speed: 6, amp: 14, op: 0.9, base: 0.0, twinkle: 3, filter: blurFilter(F.defs, 1.2) });
  svg('rect', { x: 892, y: 244, width: 6, height: 302, fill: '#4b3220' }, F.s);
  svg('rect', { x: 784, y: 392, width: 222, height: 6, fill: '#4b3220' }, F.s);
  svg('rect', { x: -300, y: -300, width: 1680, height: 1680, fill: lin(F.defs, [[0, '#140a18', 0.4], [0.55, '#140a18', 0.0], [1, '#140a18', 0.3]]) }, F.s);
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
  return {
    mom, marker, xA, xB, target: [320 + x28, 430 + y28], page, photoGlow,
    update(lt, pose) {
      const ang = Math.sin(lt * 1.7) * 5;
      const bx = 602 + Math.sin(rad(ang)) * 168, by = Math.cos(rad(ang)) * 168;
      bulbG.setAttribute('transform', `translate(602,0) rotate(${(-ang).toFixed(2)})`);
      setA(pool, { cx: bx.toFixed(1), cy: (by + 200).toFixed(1) });
      mom.pose(pose);
      momShadow.pose(Object.assign({}, pose, { x: pose.x + (pose.x - bx) * 0.12 + 40, y: pose.y - 30, s: (pose.s || 1) * 1.04 }));
      flies(lt);
      dust(lt + 2);
      if (cloth) cloth.setAttribute('transform', `translate(-90,60) skewX(${(Math.sin(lt * 1.1) * 2.5).toFixed(2)})`);
    },
  };
}

// =====================================================================
// S5 — Mom's room: pull back from the moon, X on day 28, 0 → 355, hand to heart, a tear (21.70–28.05)
// =====================================================================
(() => {
  const A = 21.70;
  const S = new Shot(A, 28.05, [['far', 0.4, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.fadeIn = 0.3;
  S.grade = 'saturate(1.08) sepia(0.06) contrast(1.04)';
  const room = momRoom4(S, true);
  room.marker.setAttribute('opacity', 1);
  const card = cardEl(S.ui, 'card', 56, 110);
  const mlb = html('div', 'lbl', card.c); const mcal = calendarFlip(mlb, 58); html('span', '', mlb, 'แม่นับวันรอ');
  const num = html('div', 'num', card.c);
  const od = new Odometer(num, 3); html('small', '', num, 'วัน');
  const heart = html('div', '', S.ui); const hbig = heartBeat(heart, 104); heart.style.cssText = 'position:absolute;left:300px;top:190px';
  const fxs = fxSvg(S);
  const tNap = P.nap - A, tSam = P.sam - A, tDoi = P.doi - A, tLand = P.hawan - A + 0.42;
  const sparkX = burst(fxs, room.target[0], room.target[1], tNap + 0.8, 14, 71, ['#ff7a6a', '#ffd66b', '#ffffff'], 200, 0.7);
  const sparkN = burst(fxs, 250, 260, tLand, 18, 73, ['#ffd66b', '#ffffff', '#ff9fb2'], 260, 0.9);
  const tear = svg('g', { opacity: 0 }, fxs);
  const tearStar = svg('path', { d: 'M0,-14 L3,-3 L14,0 L3,3 L0,14 L-3,3 L-14,0 L-3,-3 Z', fill: '#ffffff' }, tear);
  const tearDrop = svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#cfe8ff', opacity: 0.9 }, fxs);
  S.update = lt => {
    // pull back from the moon (matches S4's push), then a slow push toward Mom
    const pull = 1 - ease.inOutSine(prog(lt, 0.2, 1.6));   // hold through the dissolve, then pull back
    if (pull > 0) S.cam({ x: 0, y: 0, z: 1 + 3.5 * pull, fx: 940, fy: 320 });
    else {
      // slow drift, then push in on Mom's face for "โดยไม่เคยท้อ" so the tear reads
      const k = ease.inOutSine(prog(lt, 1.6, 4.4)), c = ease.inOutSine(prog(lt, tDoi - 0.6, tDoi + 0.9));
      S.cam({ x: lerp(lerp(0, -24, k), 385, c), y: lerp(0, 121, c), z: lerp(lerp(1.0, 1.07, k), 1.55, c), fx: 560, fy: 800 });
    }
    const pose = { x: 885, y: 1235, s: 1.12, f: -1, torso: 4, head: -6, aB: [96, 92], lF: [90, 90], lB: [92, 90], t: lt + 0.4, smile: 0.35 };
    const [tx, ty] = room.target, o = 19;
    const k1 = ease.inOutSine(prog(lt, tNap + 0.35, tNap + 0.65)), k2 = ease.inOutSine(prog(lt, tNap + 0.77, tNap + 1.07));
    let px, py;
    if (lt < tNap + 0.71) { px = tx - o + 2 * o * k1; py = ty - o + 2 * o * k1; } else { px = tx + o - 2 * o * k2; py = ty - o + 2 * o * k2; }
    const raise = ease.inOutSine(prog(lt, tNap - 0.15, tNap + 0.3)) * (1 - ease.inOutSine(prog(lt, tNap + 1.55, tNap + 1.95)));
    const reachA = room.mom.reach(pose, px - 18, py + 48);
    pose.aF = [lerp(96, reachA[0], raise), lerp(94, reachA[1], raise)];
    pose.propRot = lerp(0, -20, raise);
    const toChest = ease.inOutSine(prog(lt, tDoi - 0.5, tDoi));
    pose.aB = [lerp(96, 60, toChest), lerp(92, -150, toChest)];
    pose.head = lerp(-4, -12, raise) + lerp(0, -10, toChest);
    pose.smile = lerp(0.35, 0.9, toChest);
    room.update(lt, pose);
    room.xA.setAttribute('stroke-dashoffset', 60 * (1 - k1));
    room.xB.setAttribute('stroke-dashoffset', 60 * (1 - k2));
    const fl0 = tNap + 1.07;
    const flutter = Math.exp(-Math.max(0, lt - fl0) * 4) * (lt > fl0 ? Math.sin((lt - fl0) * 30) : 0);
    room.page.setAttribute('transform', `skewY(${(flutter * 1.2).toFixed(2)})`);
    room.photoGlow.setAttribute('opacity', ease.inOutSine(prog(lt, tDoi - 0.5, tDoi + 0.3)).toFixed(3));
    enter3d(card.c, lt, tSam - 0.25, 'flipDown'); shine(card.sh, lt, tLand + 0.1, 0.8);
    const v = rollValue(lt, tSam - 0.05, tLand, 0, 355); od.set(v.v, v.speed);
    const flipping = lt > tSam - 0.05 && lt < tLand;
    mcal.update(lt, flipping ? (Math.floor(v.v) % 31) + 1 : 28, flipping);
    hbig.update(lt);
    const hk = spring(lt, tDoi + 0.12, 12, 4);
    heart.style.opacity = fadeIn(lt, tDoi + 0.12, 0.1) * (1 - prog(lt, tDoi + 1.0, tDoi + 1.4));
    heart.style.transform = `translateY(${(-lerp(0, 80, prog(lt, tDoi + 0.12, tDoi + 1.4))).toFixed(1)}px) scale(${hk.toFixed(3)})`;
    sparkX(lt); sparkN(lt);
    // tear: a glint at her eye, then a drop sliding down the cheek
    const er = room.mom.eyeG.getBoundingClientRect();
    const ex = er.x + er.width / 2, ey = er.y + er.height / 2;
    const tg = prog(lt, tDoi + 0.45, tDoi + 1.25);
    tear.setAttribute('opacity', (Math.sin(Math.PI * tg) * 0.95).toFixed(3));
    tear.setAttribute('transform', `translate(${(ex - 4).toFixed(1)},${(ey + 2).toFixed(1)}) rotate(${(lt * 90).toFixed(1)}) scale(${(0.6 + 0.5 * Math.sin(Math.PI * tg)).toFixed(3)})`);
    const td = prog(lt, tDoi + 0.75, tDoi + 1.6);
    tearDrop.setAttribute('opacity', (td > 0 && td < 1 ? 0.9 * (1 - td * 0.6) : 0).toFixed(3));
    tearDrop.setAttribute('transform', `translate(${(ex - 6).toFixed(1)},${(ey + 14 + 34 * ease.inCubic(td)).toFixed(1)})`);
    setGrade(S, lerp(0, 14, ease.inCubic(prog(lt, 5.95, 6.35))));
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — title over the blurred room (28.05–30.30), then warm white into morning
// =====================================================================
(() => {
  const A = 28.05;
  const S = new Shot(A, 30.30, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = momRoom4(S, false);
  room.xA.setAttribute('stroke-dashoffset', 0); room.xB.setAttribute('stroke-dashoffset', 0);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 91, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const hb = html('div', 'title', wrap); const thb = heartBeat(hb, 150); hb.style.top = '560px';
  const t1 = html('div', 'title', wrap); t1.style.top = '690px'; t1.style.font = '700 176px/1 Kanit';
  const digits = ['3', '5', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'วัน'); unit.style.marginLeft = '0.28em';
  const t2 = html('div', 'title', wrap, 'ที่แม่รอ'); t2.style.top = '885px'; t2.style.font = '600 124px/1 Kanit';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#e0574b', boxShadow: '0 0 16px rgba(224,87,75,.8)' });
  const glint = html('div', '', wrap); glint.style.cssText = 'position:absolute;left:0;top:680px;width:260px;height:340px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));mix-blend-mode:overlay;opacity:0';
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, 2.25)), fx: 560, fy: 800 });
    room.update(lt + 6, { x: 885, y: 1235, s: 1.12, f: -1, torso: 4, head: -22, aF: [96, 94], aB: [60, -150], eyes: 1, smile: 0.9 });
    bok(lt);
    const f = (el, t0, dy = 24) => { const k = spring(lt, t0, 14, 7); el.style.opacity = fadeIn(lt, t0, 0.15); el.style.transform = `translateY(${((1 - k) * dy).toFixed(1)}px)`; };
    const hk = spring(lt, 0.05, 14, 5);
    hb.style.opacity = fadeIn(lt, 0.05, 0.12); thb.update(lt);
    hb.style.transform = `scale(${(clamp(hk, 0, 1.3) * (1 + 0.09 * Math.max(0, Math.sin(lt * 7.5)))).toFixed(3)})`;
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.09, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; d.style.filter = lt - t0 < 0.12 ? `blur(${(6 * (1 - (lt - t0) / 0.12)).toFixed(1)}px)` : 'none'; });
    f(unit, 0.45);
    t2.style.opacity = fadeIn(lt, 0.55, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.55, 1.0))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.8, 1.2)).toFixed(3)})`;
    const gk = prog(lt, 1.15, 1.85);
    glint.style.opacity = gk > 0 && gk < 1 ? 1 : 0;
    glint.style.transform = `translateX(${(150 + gk * 700).toFixed(1)}px) skewX(-20deg)`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — morning condo: no need to wait for Songkran / New Year → ticket booked (30.30–34.75)
// =====================================================================
(() => {
  const A = 30.30;
  const S = new Shot(A, 34.75, [['far', 0.35, 1.2], ['mid', 1, 0], ['fore', 1.9, 13]]);
  S.grade = 'saturate(1.08) contrast(1.03)';
  const set = condoDay(S);
  const M = S.L.mid;
  contactShadow(M.s, M.defs, 420, 1328, 120, 14, 0.3);
  const p = new Puppet(M.s, GIRL, M.defs);
  const ph = svg('g', {}, p.prop);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: '#15151b' }, ph);
  svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#eaf4ff' }, ph);
  const sk = festivalCard(S.ui, 56, 250, 450, '', 'สงกรานต์', '13 เม.ย.', '#3f9bd8');
  const ny = festivalCard(S.ui, 534, 250, 450, '', 'ปีใหม่', '1 ม.ค.', '#e0577a');
  const skI = waterBowlMini(sk.c.c.querySelector('.fic'), 150), nyI = fireworkMini(ny.c.c.querySelector('.fic'), 150);
  const tk = ticketCard(S.ui, 70, 300, 940);
  const fxs = fxSvg(S);
  const tS = P.mai1 - A, tN = P.mai2 - A, tW = P.wang - A;
  const sparkT = burst(fxs, 820, 560, tW + 0.45, 20, 121, ['#2f9e5b', '#ffd66b', '#ffffff'], 260, 0.9);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, 4.45));
    S.cam({ x: lerp(20, -20, k), y: 0, z: lerp(1.03, 1.1, k), fx: 430, fy: 1000 });
    set.update(lt);
    const joy = ease.inOutSine(prog(lt, tW + 0.3, tW + 0.7));
    p.pose({ x: 352, y: 1162, torso: 6 + Math.sin(lt * 2.2), head: lerp(16, -6, joy), aF: [76, -46 + Math.sin(lt * 10) * 2], aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 1.7, smile: lerp(0.6, 1, joy), grin: joy });
    sk.update(lt, tS - 0.12, tS + 1.02, tW - 0.55);
    ny.update(lt, tN - 0.12, P.pimai - A + 0.25, tW - 0.5);
    skI.update(lt); nyI.update(lt);
    tk.update(lt, tW - 0.3, tW + 0.42);
    sparkT(lt);
    const inK = 1 - prog(lt, 0, 0.35);
    S.root.style.opacity = 1;
    const out = whip(S, lt, 'out');
    setGrade(S, out * 18 + inK * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — golden hour at home: Mom drops the broom, runs, the hug (34.75–42.70)
// =====================================================================
(() => {
  const A = 34.75;
  const S = new Shot(A, 42.70, [['sky', 0.06, 0], ['far', 0.2, 1.4], ['field', 0.42, 0.6], ['house', 0.68, 0], ['mid', 1, 0], ['fore', 1.7, 9]]);
  S.grade = 'saturate(1.12) contrast(1.03)';
  const set = isanYard(S);
  const M = S.L.mid;
  const G = 1600;                      // ground line for the people
  const sG = 0.92, sM = 0.84;
  const hipG = G - 311 * sG, hipM = G - 311 * sM;
  const shG = castShadow(M.s, M.defs, GIRL_PACK, G, -58, 0.24, 0.32, 3);
  const shM = castShadow(M.s, M.defs, MOM, G, -58, 0.24, 0.32, 3);
  const csG = contactShadow(M.s, M.defs, 0, G + 4, 70, 9, 0.45);
  const csM = contactShadow(M.s, M.defs, 0, G + 4, 70, 9, 0.45);
  const brm = svg('g', {}, M.s);
  broom(brm);
  const girl = new Puppet(M.s, GIRL_PACK, M.defs);
  const mom = new Puppet(M.s, MOM, M.defs);          // Mom in front so her face shows in the hug
  const top = svg('g', {}, M.s);
  girl.armOverlay(top);                               // the girl's near arm lies over Mom's back
  const dogSh = contactShadow(M.s, M.defs, 0, G + 2, 74, 9, 0.4);
  const dog = new Dog(M.s);
  const fxs = fxSvg(S);
  const flare = lensFlare(fxs, svg('defs', {}, fxs));
  const leak = lightLeak(S.fx);
  const hx = 438, hy = 1170;
  const hearts = heartsRise(fxs, hx, hy, P.maidai - A + 0.35, 16, 5, 0.26);
  const bigHeart = burst(fxs, hx, hy - 40, P.luk - A, 22, 131, ['#e0577a', '#ffd66b', '#ffffff', '#ff9fb2'], 300, 1.0);
  const tPro = P.pro - A, tHug = P.maidai - A - 0.05, tTuk = P.tuk - A;
  // girl x: walk in, stop; mom x: sweep, then run to her
  const girlX = lt => lt < 2.3 ? -230 + 270 * lt - 60 * ease.inCubic(prog(lt, 1.95, 2.3)) * 0.35 : -230 + 270 * 2.3 - 21 + 60 * ease.inOutSine(prog(lt, 2.9, tHug));
  S.update = lt => {
    const wide = ease.inOutSine(prog(lt, 0, 3.4)), push = ease.inOutSine(prog(lt, 3.3, 7.1)), rise = ease.inOutSine(prog(lt, 6.8, 7.95));
    S.cam({ x: lerp(-70, 30, wide) + lerp(0, -100, push), y: lerp(0, -40, push) - 70 * rise, z: 1 + 0.34 * push + 0.04 * rise, fx: hx, fy: 1250 });
    set.update(lt);
    // ---- girl ----
    const gx = girlX(lt);
    const walkK = 1 - ease.inOutSine(prog(lt, 1.95, 2.35));
    const gph = 2 * Math.PI * ((gx + 230) / 265);
    const gw = gait(gph, 14 * walkK, 0);
    const hug = ease.inOutSine(prog(lt, tHug - 0.25, tHug + 0.15));
    const open = ease.inOutSine(prog(lt, 2.7, 3.15));
    const gPose = { x: gx, y: hipG + gw.bob * walkK, s: sG, f: 1, torso: lerp(2 + gw.torso * walkK, 12, hug), head: lerp(lerp(2, -10, open), 22, hug), lF: walkK > 0.02 ? gw.lF : [86, 90], lB: walkK > 0.02 ? gw.lB : [94, 92], t: lt + 5, smile: lerp(0.55, 1, open), eyes: hug > 0.6 ? 0 : null };
    const mx = lt < 2.35 ? 860 : lerp(860, gx + 84, ease.inOutSine(prog(lt, 2.35, tHug)));
    const armOpen = [lerp(gw.aF[0], 40, open), lerp(gw.aF[1], -6, open)];
    gPose.armF = lerp(1, 0.56, hug);
    const tgtG = girl.reach(gPose, mx + 18 + Math.sin(lt * 7) * 3 * hug, hipM - 116);
    gPose.aF = [lerp(armOpen[0], tgtG[0], hug), lerp(armOpen[1], tgtG[1], hug)];
    gPose.aB = [lerp(lerp(gw.aB[0], 50, open), 96, hug), lerp(lerp(gw.aB[1], 4, open), 92, hug)];  // far arm tucked behind her own body
    // ---- mom ----
    const sweep = lt < 1.5 ? Math.sin(lt * 6.5) : 0;
    const up = ease.inOutSine(prog(lt, 1.45, 1.85));
    const surprised = ease.inOutSine(prog(lt, 1.8, 2.1)) * (1 - ease.inOutSine(prog(lt, 2.35, 2.6)));
    const runK = ease.inOutSine(prog(lt, 2.35, 2.55)) * (1 - ease.inOutSine(prog(lt, tHug - 0.3, tHug)));
    const mph = 2 * Math.PI * ((860 - mx) / 300);
    const mw = gait(mph, 24, 0.8);
    const mPose = { x: mx, y: hipM + (runK > 0.02 ? mw.bob * runK : 0), s: sM, f: -1, torso: lerp(lerp(24, 3, up) + 8 * runK, 12, hug), head: lerp(lerp(14, -14, up), 8, hug), lF: runK > 0.02 ? mw.lF : [lerp(78, 88, up), lerp(96, 90, up)], lB: runK > 0.02 ? mw.lB : [lerp(100, 93, up), lerp(92, 91, up)], t: lt + 9, smile: lerp(0.3, 1, Math.max(up * 0.6, hug)), eyes: hug > 0.6 ? 0 : (surprised > 0.5 ? 1 : null) };
    const sweepA = [lerp(70 + sweep * 10, 98, up), lerp(110 + sweep * 16, 96, up)];
    const runA = [lerp(mw.aF[0], 20, ease.inOutSine(prog(lt, 2.9, tHug))), lerp(mw.aF[1], -6, ease.inOutSine(prog(lt, 2.9, tHug)))];
    mPose.armF = lerp(1, 0.6, hug);
    const tgtM = mom.reach(mPose, gx - 30, hipG - 80 + Math.sin(lt * 6) * 6 * hug);
    const preHug = lt < 2.35 ? sweepA : runA;
    mPose.aF = [lerp(preHug[0], tgtM[0], hug), lerp(preHug[1], tgtM[1], hug)];
    mPose.aB = lt < 2.35 ? [lerp(lerp(76 + sweep * 8, 96, up), 200, surprised), lerp(lerp(118 + sweep * 12, 94, up), 250, surprised)] : [lerp(mw.aB[0], 96, hug), lerp(mw.aB[1], 92, hug)];
    const sway = Math.sin(lt * 2.1) * 1.6 * hug;
    gPose.torso += sway; mPose.torso += sway;
    mom.pose(mPose); girl.pose(gPose);
    shM.pose(mPose); shG.pose(gPose);
    setA(csG, { cx: (gx + 6).toFixed(1) }); setA(csM, { cx: (mx - 6).toFixed(1) });
    // broom: swept, then dropped at 2.2
    const drop = ease.outBack(prog(lt, 2.2, 2.6));
    if (lt < 2.2) {
      const w = mom.wristF; // local to mom (mirrored)
      brm.setAttribute('transform', `translate(${(mx - w[0] * sM).toFixed(1)},${(hipM + w[1] * sM).toFixed(1)}) rotate(${(18 + sweep * 14 - 20 * up).toFixed(1)}) scale(${sM})`);
    } else brm.setAttribute('transform', `translate(${lerp(874, 934, drop).toFixed(1)},${lerp(1403, G - 10, drop).toFixed(1)}) rotate(${lerp(-2, 82, drop).toFixed(1)}) scale(${sM})`);  // falls from her hand and stays put
    // ---- dog: rests, perks up, races to the girl, jumps, then sits wagging ----
    const dRun = prog(lt, 1.15, 2.15);
    let dx = lerp(760, gx + 150, ease.inOutSine(dRun)), dy = G, dsit = 1 - ease.inOutSine(prog(lt, 0.9, 1.15)), drun = dRun > 0 && dRun < 1 ? 1 : 0;
    let df = -1, jump = 0;
    if (lt > 2.15) { jump = Math.max(0, Math.sin((lt - 2.15) * 9)) * 40 * (lt < 2.85 ? 1 : 0); }
    if (lt > 3.0) { const k2 = ease.inOutSine(prog(lt, 3.0, 3.7)); dx = lerp(gx + 150, gx - 200, k2); df = k2 > 0.5 ? 1 : -1; drun = k2 > 0 && k2 < 1 ? 1 : 0; dsit = ease.inOutSine(prog(lt, 3.7, 4.0)); }
    dog.pose({ x: dx, y: dy, f: df, s: 0.95, ph: lt * 15, run: drun, wag: lt > 0.95 ? 1 : 0.2, sit: dsit, head: lt < 0.95 ? 14 : -6, t: lt, jump, pant: lt > 1.1 });
    setA(dogSh, { cx: dx.toFixed(1), rx: (74 - jump).toFixed(1) });
    // ---- light ----
    const sx = set.SUN[0] - (lerp(-70, 30, wide) + lerp(0, -100, push)) * 0.06, sy = set.SUN[1];
    const tukK = Math.exp(-Math.pow((lt - tTuk - 0.3) * 1.6, 2));
    flare(sx, sy, 0.75 + 0.5 * tukK);
    leak(lt, 0.3 + 0.25 * hug + 0.45 * tukK + 0.4 * rise);
    hearts(lt); bigHeart(lt);
    const inK = whip(S, lt, 'in');
    setGrade(S, inK * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S9 — end card (42.70–46.0)
// =====================================================================
(() => {
  const A = 42.70;
  const S = new Shot(A, 46.0, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const B = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(B.defs, [[0, '#5a3550'], [0.6, '#2c1c33'], [1, '#170f1d']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, B.s);
  const bok = floaters(B.s, [0, 0, 1080, 1920], 22, 141, { color: '#ffd9a0', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(B.defs, 4) });
  const leak = lightLeak(S.fx);
  const fxs = fxSvg(S);
  const ring = Array.from({ length: 3 }, () => svg('circle', { cx: 540, cy: 560, r: 90, fill: 'none', stroke: '#f2c14e', 'stroke-width': 5 }, fxs));
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const icon = html('div', 'title', wrap); const endHouse = houseIcon(icon, 210); icon.style.top = '470px';
  const t1 = html('div', 'title', wrap); t1.style.top = '700px'; t1.style.font = '700 168px/1 Kanit';
  const digits = ['3', '5', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'วัน'); unit.style.marginLeft = '0.28em';
  const t2 = html('div', 'title', wrap, 'ที่แม่รอ'); t2.style.top = '890px'; t2.style.font = '600 118px/1 Kanit';
  const sub = html('div', 'title', wrap, 'ว่างเมื่อไหร่ กลับบ้านไปหาแม่นะ'); sub.style.top = '1070px'; sub.style.font = '500 46px/1.3 Kanit'; sub.style.color = '#ffd166';
  const cta = html('div', 'cta', wrap); cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ทำงานไกลบ้านดู</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  const spark = burst(fxs, 540, 560, 0.3, 18, 151, ['#ffd66b', '#ffffff', '#ff9fb2'], 240, 0.9);
  S.update = lt => {
    bok(lt); leak(lt, 0.45);
    const ik = spring(lt, 0.2, 13, 5.5);
    icon.style.opacity = fadeIn(lt, 0.2, 0.1);
    icon.style.transform = `translateY(${(Math.sin(lt * 2) * 6).toFixed(1)}px) scale(${clamp(ik, 0, 1.3).toFixed(3)}) rotate(${((1 - clamp(ik)) * -20).toFixed(1)}deg)`;
    ring.forEach((rg, i) => { const k = ((lt - 0.3 + i * 0.5) % 1.5 + 1.5) % 1.5 / 1.5; setA(rg, { r: (90 + k * 160).toFixed(1), opacity: (lt > 0.3 ? (1 - k) * 0.5 : 0).toFixed(3) }); });
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.45 + i * 0.09, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.75, 14, 7); unit.style.opacity = fadeIn(lt, 0.75, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.85, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.85, 1.3))) * 100).toFixed(1)}% -40% 0)`;
    const ks = spring(lt, 1.25, 14, 7); sub.style.opacity = fadeIn(lt, 1.25, 0.15); sub.style.transform = `translateY(${((1 - ks) * 24).toFixed(1)}px)`;
    const kc = enter3d(cta, lt, 1.55, 'pop');
    cta.style.boxShadow = `0 0 ${(24 + 18 * Math.sin(lt * 4)).toFixed(1)}px rgba(224,87,122,.65), 0 16px 34px rgba(0,0,0,.4)`;
    const pk = prog(lt, 2.1, 2.9);
    plane.update(lt); endHouse.update(lt);
  };
  SHOTS.push(S);
})();

// global overlays: film grain, start/end fades, flash at the highway cut, warm whites between acts
const grainTick = makeGrain();
const black = html('div', 'blackout', frame);
const flash = html('div', 'blackout', frame); flash.style.background = '#fff6e0';
const warm = html('div', 'blackout', frame); warm.style.background = '#fff1dc';

const DURATION = 46.0;
window.render = t => {
  for (const sh of SHOTS) {
    const next = SHOTS[SHOTS.indexOf(sh) + 1];
    const until = next && next.fadeIn ? Math.max(sh.b, next.a + next.fadeIn) : sh.b;
    const on = t >= sh.a && t < until;
    sh.root.style.display = on ? 'block' : 'none';
    if (on) {
      if (sh.fadeIn) sh.root.style.opacity = prog(t, sh.a, sh.a + sh.fadeIn).toFixed(3);
      sh.update(t - sh.a);
    }
  }
  renderKinetic2(subsBox, CUES, t);
  grainTick(t);
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, 45.55, 46.0)).toFixed(3);
  flash.style.opacity = t >= 8.98 ? (0.32 * (1 - prog(t, 8.98, 9.16))).toFixed(3) : 0;
  const w1 = prog(t, 29.85, 30.30) * (1 - prog(t, 30.30, 30.75));
  const w2 = prog(t, 42.35, 42.70) * (1 - prog(t, 42.70, 43.15));
  warm.style.opacity = (0.92 * Math.max(w1, w2)).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
