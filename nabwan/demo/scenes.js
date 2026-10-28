// Demo: 355 วันที่แม่รอ (first ~17 s). Shot times are aligned to the narration onsets (VO starts at 0.4 s).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');

const DAUGHTER = { skin: '#c98e66', skinShade: '#b27752', hair: '#2a2326', hairStyle: 'bob', shirt: '#8fb3de', shirtShade: '#7897c4', sleeve: 'long', pants: '#2f3a5c', pantsShade: '#262f4d', shoe: '#f1f1f1' };
const MOM = { skin: '#c48a62', skinShade: '#aa7350', hair: '#3a3437', gray: '#a9a4a6', hairStyle: 'bun', shirt: '#b2506a', shirtShade: '#9a4259', sleeve: 'short', pants: '#4f3a6e', pantsShade: '#43315e', shoe: '#8a5a3c', sarong: '#5b3f7a', glasses: true };

const CUES = [
  { a: 0.40, b: 2.30, parts: [{ t: 'ถ้าคุณทำงานไกลบ้าน', s: 'w' }] },
  { a: 2.34, b: 4.15, parts: [{ t: 'กลับบ้านปีละ 2 ครั้ง', s: 'w' }] },
  { a: 4.19, b: 5.02, parts: [{ t: 'เคยนับไหม', s: 'w' }] },
  { a: 5.05, b: 8.10, parts: [{ t: 'ว่าเหลือเวลาเจอพ่อแม่', s: 'w' }, { t: 'อีกกี่วัน', s: 'r' }] },
  { a: 8.13, b: 10.36, parts: [{ t: 'ปีหนึ่ง คุณอยู่บ้าน 10 วัน', s: 'y' }] },
  { a: 10.40, b: 14.30, parts: [{ t: 'แต่แม่นับวันรอ 355 วัน', s: 'y' }] },
];

function makeShot() {
  const root = html('div', 'shot', frame);
  frame.insertBefore(root, subsBox);
  const cam = html('div', 'cam', root);
  const s = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920 }, cam);
  const defs = svg('defs', {}, s);
  const ui = html('div', 'ui', root);
  return { root, cam, s, defs, ui };
}
function radial(defs, id, stops, attrs = {}) {
  const g = svg('radialGradient', Object.assign({ id }, attrs), defs);
  for (const [o, c, a] of stops) svg('stop', { offset: o, 'stop-color': c, 'stop-opacity': a == null ? 1 : a }, g);
  return `url(#${id})`;
}
function linear(defs, id, stops, attrs = { x1: 0, y1: 0, x2: 0, y2: 1 }) {
  const g = svg('linearGradient', Object.assign({ id }, attrs), defs);
  for (const [o, c, a] of stops) svg('stop', { offset: o, 'stop-color': c, 'stop-opacity': a == null ? 1 : a }, g);
  return `url(#${id})`;
}
const uid = (() => { let n = 0; return p => `${p}${++n}`; })();
const heartPath = (cx, cy, r) => `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`;
const heartSVG = (size, color) => `<svg width="${size}" height="${size}" viewBox="-12 -12 24 24"><path d="${heartPath(0, 0, 9)}" fill="${color}"/></svg>`;
const moonSVG = `<svg width="38" height="38" viewBox="0 0 16 16"><path d="M11.5 11.8A5.5 5.5 0 0 1 6.2 2.3a5.6 5.6 0 1 0 7.3 7.4 5.4 5.4 0 0 1-2 2.1z" fill="#f2d48a"/></svg>`;
const batterySVG = (pct, color) => `<svg width="56" height="30" viewBox="0 0 56 30"><rect x="2" y="3" width="46" height="24" rx="6" fill="none" stroke="#fff" stroke-width="3"/><rect x="50" y="10" width="4" height="10" rx="2" fill="#fff"/><rect x="6" y="7" width="${Math.max(3, 38 * pct)}" height="16" rx="3" fill="${color}"/></svg>`;
const boltSVG = `<svg width="30" height="38" viewBox="0 0 30 38"><path d="M18 2 L4 22 H14 L11 36 L26 14 H16 Z" fill="#8fd49b"/></svg>`;

// ---------- reusable backgrounds ----------
function condoRoom(s, defs, withGirl = true) {
  const g = svg('g', {}, s);
  svg('rect', { x: 0, y: 0, width: 1080, height: 1350, fill: linear(defs, uid('wall'), [[0, '#3c3355'], [1, '#2d2742']]) }, g);
  svg('rect', { x: 0, y: 1350, width: 1080, height: 570, fill: '#231d33' }, g);
  svg('rect', { x: 0, y: 1350, width: 1080, height: 10, fill: '#1b1628' }, g);
  svg('ellipse', { cx: 560, cy: 1560, rx: 430, ry: 96, fill: '#352e4f' }, g);
  // window with skyline
  svg('rect', { x: 150, y: 250, width: 520, height: 650, rx: 10, fill: '#1f1a2e' }, g);
  svg('rect', { x: 168, y: 268, width: 484, height: 614, fill: linear(defs, uid('sky'), [[0, '#151a3e'], [1, '#2c2f5e']]) }, g);
  const r = rng(7);
  for (let i = 0; i < 40; i++) svg('circle', { cx: 175 + r() * 470, cy: 280 + r() * 260, r: 1.2 + r() * 2, fill: '#fff', opacity: 0.35 + r() * 0.5 }, g);
  svg('circle', { cx: 560, cy: 350, r: 34, fill: '#f3ead2', opacity: 0.9 }, g);
  let x = 168;
  while (x < 652) {
    const w = 46 + r() * 60, h = 160 + r() * 280;
    const bx = x, by = 882 - h, bw = Math.min(w, 652 - x);
    svg('rect', { x: bx, y: by, width: bw, height: h, fill: r() > 0.5 ? '#262b52' : '#2e3360' }, g);
    for (let wy = by + 18; wy < 870; wy += 30) for (let wx = bx + 8; wx < bx + bw - 12; wx += 18)
      if (r() > 0.55) svg('rect', { x: wx, y: wy, width: 8, height: 12, fill: '#f2c66d', opacity: 0.75 }, g);
    x += w + 4;
  }
  svg('rect', { x: 406, y: 268, width: 8, height: 614, fill: '#1f1a2e' }, g);
  // curtains
  for (const cx of [104, 640]) {
    svg('rect', { x: cx, y: 228, width: 96, height: 740, rx: 18, fill: '#5a4a7c' }, g);
    for (let k = 0; k < 3; k++) svg('rect', { x: cx + 14 + k * 28, y: 238, width: 8, height: 720, rx: 4, fill: '#4b3d6a' }, g);
  }
  svg('rect', { x: 80, y: 220, width: 680, height: 14, rx: 7, fill: '#2a2238' }, g);
  // lamp glow + nightstand + lamp
  svg('circle', { cx: 900, cy: 900, r: 360, fill: radial(defs, uid('glow'), [[0, '#ffcf8a', 0.42], [1, '#ffcf8a', 0]]) }, g);
  svg('rect', { x: 800, y: 1090, width: 190, height: 200, rx: 12, fill: '#4b3e66' }, g);
  svg('rect', { x: 800, y: 1090, width: 190, height: 22, rx: 8, fill: '#5a4b78' }, g);
  svg('rect', { x: 818, y: 1290, width: 16, height: 60, fill: '#3b3052' }, g);
  svg('rect', { x: 956, y: 1290, width: 16, height: 60, fill: '#3b3052' }, g);
  svg('rect', { x: 885, y: 990, width: 14, height: 100, fill: '#d8c9a6' }, g);
  svg('path', { d: 'M842,1000 L942,1000 L918,920 L866,920 Z', fill: '#f3d9a8' }, g);
  svg('rect', { x: 960, y: 1180, width: 40, height: 56, rx: 8, fill: '#e8e2f2' }, g); // wall socket
  svg('circle', { cx: 972, cy: 1200, r: 4, fill: '#7a7290' }, g);
  svg('circle', { cx: 988, cy: 1200, r: 4, fill: '#7a7290' }, g);
  // bed (side view): headboard at the left
  svg('rect', { x: 70, y: 930, width: 46, height: 420, rx: 14, fill: '#4a3d6b' }, g);
  svg('rect', { x: 110, y: 1190, width: 640, height: 92, rx: 16, fill: '#5a4b7c' }, g);
  svg('rect', { x: 120, y: 1282, width: 20, height: 68, fill: '#43385f' }, g);
  svg('rect', { x: 720, y: 1282, width: 20, height: 68, fill: '#43385f' }, g);
  svg('rect', { x: 110, y: 1104, width: 640, height: 96, rx: 22, fill: '#d6d0e4' }, g);
  svg('rect', { x: 130, y: 1052, width: 190, height: 70, rx: 30, fill: '#efebf6' }, g);
  svg('path', { d: 'M300,1098 C420,1080 560,1086 742,1098 L752,1196 L300,1196 Z', fill: '#8e7cc0' }, g);
  svg('path', { d: 'M330,1140 C470,1128 600,1132 740,1142', fill: 'none', stroke: '#7d6bb0', 'stroke-width': 6 }, g);
  const out = { g };
  if (withGirl) {
    const cable = svg('path', { d: 'M716,1012 C760,1120 700,1300 860,1330 C930,1342 960,1290 972,1230', fill: 'none', stroke: '#e9e5f2', 'stroke-width': 5, opacity: 0 }, g);
    const p = new Person(g, DAUGHTER);
    const phone = svg('g', {}, p.prop);
    svg('rect', { x: -18, y: -46, width: 36, height: 70, rx: 8, fill: '#16161c' }, phone);
    svg('rect', { x: -14, y: -42, width: 28, height: 60, rx: 5, fill: '#cfe3ff' }, phone);
    const glow = svg('circle', { cx: 0, cy: 0, r: 150, fill: radial(defs, uid('pg'), [[0, '#bcd6ff', 0.55], [1, '#bcd6ff', 0]]) }, g);
    out.p = p; out.glow = glow; out.cable = cable;
    out.pose = (t, look = 1) => {
      const breath = Math.sin(t * 2.4) * 1.2;
      p.pose({ x: 600, y: 1176, f: 1, torso: 10 + breath, head: 16 * look, aF: [62, -48], aB: [68, -42], lF: [-4, 88], lB: [-2, 90], eyes: 1, smile: 0.7 });
      const w = p.wristF; // phone glow follows the hand
      setA(glow, { cx: 600 + w[0] + 14, cy: 1176 + w[1] - 30 });
    };
  }
  return out;
}

function momRoom(s, defs, withMom = true) {
  const g = svg('g', {}, s);
  // wooden plank wall
  const tones = ['#7b5538', '#70492f', '#82593b', '#76503a'];
  for (let i = 0; i < 13; i++) {
    svg('rect', { x: i * 84, y: 0, width: 84, height: 1390, fill: tones[i % 4] }, g);
    svg('rect', { x: i * 84, y: 0, width: 4, height: 1390, fill: '#5d3f29', opacity: 0.7 }, g);
  }
  svg('rect', { x: 0, y: 1390, width: 1080, height: 530, fill: '#5a3b28' }, g);
  for (let y = 1420; y < 1920; y += 70) svg('rect', { x: 0, y, width: 1080, height: 4, fill: '#4a3020', opacity: 0.6 }, g);
  svg('rect', { x: 0, y: 1380, width: 1080, height: 16, fill: '#4a3020' }, g);
  // warm bulb
  svg('rect', { x: 776, y: 0, width: 6, height: 150, fill: '#2a1d14' }, g);
  svg('circle', { cx: 779, cy: 170, r: 26, fill: '#ffe2a6' }, g);
  svg('circle', { cx: 779, cy: 300, r: 760, fill: radial(defs, uid('bulb'), [[0, '#ffd99c', 0.45], [0.55, '#ffd99c', 0.12], [1, '#ffd99c', 0]]) }, g);
  // graduation photo
  svg('rect', { x: 66, y: 560, width: 220, height: 270, rx: 8, fill: '#3a2a1e' }, g);
  svg('rect', { x: 82, y: 576, width: 188, height: 238, fill: '#b9c9da' }, g);
  svg('path', { d: 'M110,814 C112,742 240,742 242,814 Z', fill: '#1d1d24' }, g); // gown
  svg('path', { d: 'M150,760 C160,800 192,800 202,760', fill: 'none', stroke: '#f5d76e', 'stroke-width': 10, 'stroke-linecap': 'round' }, g); // garland
  faceFront(g, 176, 700, 44, { skin: '#c98e66', hair: '#2a2326', hairStyle: 'bob' });
  svg('path', { d: 'M120,652 L176,630 L232,652 L176,672 Z', fill: '#1d1d24' }, g); // cap
  svg('rect', { x: 170, y: 650, width: 12, height: 14, fill: '#1d1d24' }, g);
  svg('path', { d: 'M222,654 L230,700', stroke: '#f5d76e', 'stroke-width': 4 }, g);
  // wall calendar: March 2026 starts on Sunday
  const cal = svg('g', { transform: 'translate(330,430)' }, g);
  svg('path', { d: 'M215,-60 L120,0 M215,-60 L310,0', stroke: '#2a1d14', 'stroke-width': 3 }, cal);
  svg('circle', { cx: 215, cy: -62, r: 7, fill: '#2a1d14' }, cal);
  svg('rect', { x: 0, y: 0, width: 430, height: 560, rx: 10, fill: '#f6f1e6' }, cal);
  svg('rect', { x: 0, y: 0, width: 430, height: 86, rx: 10, fill: '#cf483d' }, cal);
  svg('rect', { x: 0, y: 60, width: 430, height: 26, fill: '#cf483d' }, cal);
  svg('text', { x: 215, y: 58, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 40, fill: '#fff' }, cal).textContent = 'มีนาคม 2569';
  const days = ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'];
  days.forEach((d, i) => { svg('text', { x: 34 + i * 60, y: 124, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 500, 'font-size': 22, fill: i === 0 ? '#cf483d' : '#6b6670' }, cal).textContent = d; });
  const cell = d => { const i = d - 1; return [34 + (i % 7) * 60, 176 + Math.floor(i / 7) * 82]; };
  for (let d = 1; d <= 31; d++) {
    const [cx, cy] = cell(d);
    svg('text', { x: cx, y: cy + 12, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 34, fill: '#2f2c33' }, cal).textContent = d;
    if (d <= 27) {
      const o = 19;
      svg('path', { d: `M${cx - o},${cy - o} L${cx + o},${cy + o} M${cx + o},${cy - o} L${cx - o},${cy + o}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.9 }, cal);
    }
  }
  const [x23, y23] = cell(28);
  const o = 19;
  const xA = svg('path', { d: `M${x23 - o},${y23 - o} L${x23 + o},${y23 + o}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-dasharray': 60, 'stroke-dashoffset': 60 }, cal);
  const xB = svg('path', { d: `M${x23 + o},${y23 - o} L${x23 - o},${y23 + o}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-dasharray': 60, 'stroke-dashoffset': 60 }, cal);
  const out = { g, xA, xB, target: [330 + x23, 430 + y23] };
  if (withMom) {
    const p = new Person(g, MOM);
    const marker = svg('g', {}, p.prop);
    svg('rect', { x: -7, y: -48, width: 14, height: 56, rx: 5, fill: '#cf483d' }, marker);
    svg('rect', { x: -7, y: -48, width: 14, height: 16, rx: 5, fill: '#efe9e1' }, marker);
    out.p = p;
  }
  return out;
}

// 2-bone IK in the puppet's local space (front arm).
function reachTo(person, pose, tx, ty) {
  const s = (pose.s || 1) * person.o.s, f = pose.f || 1;
  const lx = (tx - pose.x) / (f * s), ly = (ty - pose.y) / s;
  const tA = rad(pose.torso || 0);
  const sx = Math.sin(tA) * 185 + 6, sy = -Math.cos(tA) * 185 + 10;
  const dx = lx - sx, dy = ly - sy, L1 = 108, L2 = 100;
  const d = Math.min(Math.hypot(dx, dy), L1 + L2 - 0.5);
  const base = Math.atan2(dy, dx);
  const a = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
  const up = base + a; // elbow below the line
  const ex = sx + Math.cos(up) * L1, ey = sy + Math.sin(up) * L1;
  const lo = Math.atan2(sy + Math.sin(base) * d - ey, sx + Math.cos(base) * d - ex);
  return [up * 180 / Math.PI, lo * 180 / Math.PI];
}

// ---------- shots ----------
const SHOTS = [];

// D1 — phone chat: "สงกรานต์นี้กลับบ้านมั้ยลูก"
(() => {
  const S = makeShot();
  const { s, defs } = S;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: linear(defs, 'd1bg', [[0, '#10142b'], [1, '#1f2650']]) }, s);
  const blur = svg('filter', { id: 'bk', x: '-50%', y: '-50%', width: '200%', height: '200%' }, defs);
  svg('feGaussianBlur', { stdDeviation: 22 }, blur);
  const r = rng(3);
  for (let i = 0; i < 16; i++) svg('circle', { cx: r() * 1080, cy: r() * 1920, r: 40 + r() * 80, fill: ['#f2c66d', '#7aa0ff', '#ff9fb2'][i % 3], opacity: 0.18 + r() * 0.15, filter: 'url(#bk)' }, s);
  const ph = svg('g', {}, s);
  svg('rect', { x: 196, y: 236, width: 688, height: 1380, rx: 92, fill: '#0c0d11' }, ph);
  svg('rect', { x: 206, y: 246, width: 668, height: 1360, rx: 84, fill: '#17181f' }, ph);
  svg('rect', { x: 228, y: 268, width: 624, height: 1316, rx: 66, fill: '#efe9df' }, ph);
  svg('rect', { x: 470, y: 286, width: 140, height: 30, rx: 15, fill: '#0c0d11' }, ph);
  const T = (x, y, txt, size, weight, fill, anchor = 'start') => { const e = svg('text', { x, y, 'font-family': 'Kanit', 'font-weight': weight, 'font-size': size, fill, 'text-anchor': anchor }, ph); e.textContent = txt; return e; };
  T(276, 312, '21:40', 30, 600, '#23242f');
  T(732, 312, '3%', 28, 600, '#cf483d', 'end');
  svg('rect', { x: 744, y: 292, width: 50, height: 26, rx: 7, fill: 'none', stroke: '#23242f', 'stroke-width': 3 }, ph);
  svg('rect', { x: 796, y: 299, width: 5, height: 12, rx: 2, fill: '#23242f' }, ph);
  svg('rect', { x: 749, y: 297, width: 6, height: 16, rx: 2, fill: '#cf483d' }, ph);
  svg('rect', { x: 228, y: 340, width: 624, height: 150, fill: '#f8f4ee' }, ph);
  svg('rect', { x: 228, y: 490, width: 624, height: 2, fill: '#ddd5c8' }, ph);
  T(262, 438, '‹', 70, 400, '#4a7bd8');
  svg('circle', { cx: 360, cy: 414, r: 48, fill: '#f0d5c4' }, ph);
  faceFront(ph, 360, 420, 36, { skin: '#c48a62', hair: '#3a3437', gray: '#a9a4a6', hairStyle: 'bun', glasses: true });
  T(428, 404, 'แม่', 40, 600, '#23242f');
  const hh = svg('path', { d: heartPath(500, 392, 13), fill: '#dc6c89' }, ph);
  svg('circle', { cx: 436, cy: 440, r: 7, fill: '#4f9359' }, ph);
  T(452, 450, 'ออนไลน์', 26, 500, '#4f9359');
  T(540, 548, 'วันนี้', 24, 500, '#9a948b', 'middle');
  // incoming message
  const msg = svg('g', {}, ph);
  svg('rect', { x: 262, y: 600, width: 470, height: 176, rx: 38, fill: '#ffffff' }, msg);
  svg('rect', { x: 262, y: 740, width: 60, height: 36, fill: '#ffffff' }, msg);
  const m1 = svg('text', { x: 300, y: 672, 'font-family': 'Kanit', 'font-weight': 500, 'font-size': 42, fill: '#23242f' }, msg); m1.textContent = 'สงกรานต์นี้';
  const m2 = svg('text', { x: 300, y: 734, 'font-family': 'Kanit', 'font-weight': 500, 'font-size': 42, fill: '#23242f' }, msg); m2.textContent = 'กลับบ้านมั้ยลูก';
  const tm = svg('text', { x: 746, y: 772, 'font-family': 'Kanit', 'font-weight': 400, 'font-size': 24, fill: '#9a948b' }, msg); tm.textContent = '21:40';
  // typing indicator (her reply starting)
  const typing = svg('g', {}, ph);
  svg('rect', { x: 668, y: 830, width: 150, height: 76, rx: 38, fill: '#4a7bd8' }, typing);
  const dots = [0, 1, 2].map(i => svg('circle', { cx: 708 + i * 35, cy: 868, r: 9, fill: '#fff' }, typing));
  svg('rect', { x: 256, y: 1480, width: 568, height: 72, rx: 36, fill: '#fff' }, ph);
  T(292, 1527, 'พิมพ์ข้อความ…', 30, 400, '#a8a197');
  SHOTS.push({
    a: 0, b: 2.27, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 2.27), 1.0, 1.07, 540, 720);
      const buzz = lt > 0.22 && lt < 0.5 ? Math.sin(lt * 120) * 4 : 0;
      ph.setAttribute('transform', `translate(${buzz},0)`);
      const p = pop(lt, 0.22);
      msg.setAttribute('transform', `translate(262,776) scale(${p.s}) translate(-262,-776)`);
      msg.setAttribute('opacity', p.o);
      const q = pop(lt, 1.25);
      typing.setAttribute('transform', `translate(818,906) scale(${q.s}) translate(-818,-906)`);
      typing.setAttribute('opacity', q.o);
      dots.forEach((d, i) => d.setAttribute('cy', 868 - Math.max(0, Math.sin((lt - 1.3) * 9 - i * 0.9)) * 9));
      hh.setAttribute('transform', `translate(500,392) scale(${1 + 0.08 * Math.sin(lt * 6)}) translate(-500,-392)`);
    },
  });
})();

// D2 — condo room, 21:40: she replies "กลับค่ะแม่" and plugs in the phone at 3%
(() => {
  const S = makeShot();
  const room = condoRoom(S.s, S.defs, true);
  const clock = html('div', 'clock', S.ui);
  clock.style.left = '60px'; clock.style.top = '120px';
  clock.innerHTML = `<div class="ic">${moonSVG}</div><div><div class="tl">อังคาร</div><div class="tt">21:40</div><div class="sl"><i style="left:68%"></i></div></div>`;
  const bubble = html('div', 'bubble', S.ui);
  bubble.innerHTML = `กลับค่ะแม่ ${heartSVG(34, '#ffd0dc')}`;
  bubble.style.left = '520px'; bubble.style.top = '760px';
  const bat = html('div', 'pill red', S.ui);
  bat.style.left = '700px'; bat.style.top = '128px';
  const setBat = charging => { bat.className = charging ? 'pill green' : 'pill red'; bat.innerHTML = charging ? `${boltSVG}<b>ชาร์จ</b>` : `${batterySVG(0.06, '#ff6b5e')}<b>3%</b>`; };
  setBat(false);
  SHOTS.push({
    a: 2.27, b: 4.12, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 1.85), 1.0, 1.06, 640, 1040);
      room.pose(lt);
      applyPop(clock, lt, 0.05);
      applyPop(bubble, lt, 0.32);
      const charging = lt > 1.05;
      if (bat._c !== charging) { bat._c = charging; setBat(charging); }
      applyPop(bat, lt, charging ? 1.05 : 0.12);
      room.cable.setAttribute('opacity', charging ? 1 : 0);
    },
  });
})();

// D3 — spotlight stage: "เคยนับไหม ว่าเหลือเวลาเจอพ่อแม่อีกกี่วัน"
(() => {
  const S = makeShot();
  const { s, defs } = S;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: linear(defs, 'd3bg', [[0, '#120f24'], [1, '#221c3a']]) }, s);
  svg('rect', { x: 0, y: 1330, width: 1080, height: 590, fill: '#1c1731' }, s);
  svg('path', { d: 'M430,0 L650,0 L960,1360 L120,1360 Z', fill: linear(defs, 'beam', [[0, '#fff6e0', 0.12], [1, '#fff6e0', 0.02]]) }, s);
  svg('ellipse', { cx: 540, cy: 1360, rx: 420, ry: 80, fill: radial(defs, 'spot', [[0, '#fff2d6', 0.35], [1, '#fff2d6', 0]]) }, s);
  const sheets = [];
  const nums = [12, 13, 14, 15, 16, 1, 30, 31];
  const pos = [[180, 520], [860, 430], [250, 1000], [880, 980], [140, 260], [930, 700], [420, 300], [800, 1540]];
  nums.forEach((n, i) => {
    const sg = svg('g', {}, s);
    const sc = 0.7 + (i % 3) * 0.15;
    svg('rect', { x: -85, y: -95, width: 170, height: 190, rx: 16, fill: '#f3efe6' }, sg);
    svg('path', { d: 'M-85,-79 Q-85,-95 -69,-95 L69,-95 Q85,-95 85,-79 L85,-49 L-85,-49 Z', fill: '#cf483d' }, sg);
    const tx = svg('text', { x: 0, y: 52, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 84, fill: '#2f2c33' }, sg); tx.textContent = n;
    sheets.push({ g: sg, x: pos[i][0], y: pos[i][1], sc, ph: i * 1.7 });
  });
  const ring = svg('circle', { cx: 540, cy: 760, r: 130, fill: 'none', stroke: '#9b98b2', 'stroke-width': 10 }, s);
  const ring2 = svg('circle', { cx: 540, cy: 760, r: 130, fill: 'none', stroke: '#9b98b2', 'stroke-width': 8 }, s);
  const q = svg('g', {}, s);
  svg('circle', { cx: 540, cy: 760, r: 130, fill: '#f3efe6' }, q);
  const qt = svg('text', { x: 540, y: 822, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 190, fill: '#cf483d' }, q); qt.textContent = '?';
  SHOTS.push({
    a: 4.12, b: 8.07, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 3.95), 1.0, 1.08, 540, 800);
      for (const sh of sheets) {
        const k = pop(lt, 0.25 + sh.ph * 0.08);
        const y = sh.y - lt * 26 + Math.sin(lt * 1.3 + sh.ph) * 10;
        sh.g.setAttribute('transform', `translate(${sh.x},${y}) rotate(${Math.sin(lt * 0.9 + sh.ph) * 9}) scale(${sh.sc * k.s})`);
        sh.g.setAttribute('opacity', 0.85 * k.o);
      }
      const p = pop(lt, 0.08, 0.4);
      q.setAttribute('transform', `translate(540,760) scale(${p.s}) translate(-540,-760)`);
      q.setAttribute('opacity', p.o);
      for (const [rg, off] of [[ring, 0], [ring2, 0.8]]) {
        const k = ((lt + off) % 1.6) / 1.6;
        setA(rg, { r: 130 + k * 110, opacity: (1 - k) * 0.55 * p.o });
      }
    },
  });
})();

// D4 — waffle card: 365 days, 10 at home
(() => {
  const S = makeShot();
  const room = condoRoom(S.s, S.defs, true);
  S.cam.style.filter = 'blur(14px) brightness(0.72)';
  const card = html('div', 'card pink', S.ui);
  card.style.left = '64px'; card.style.top = '200px'; card.style.width = '952px';
  html('div', 'lbl', card, '1 ปี = 365 วัน');
  const grid = html('div', 'waffle', card);
  const home = new Set([0, 1, 2, 101, 102, 103, 104, 105, 363, 364]);
  const order = [101, 102, 103, 104, 105, 363, 364, 0, 1, 2];
  const cells = [];
  for (let i = 0; i < 365; i++) cells.push(html('i', '', grid));
  const leg = html('div', 'legend', card);
  const l1 = html('div', '', leg); l1.innerHTML = '<s></s>อยู่บ้าน <b id="homeN">0</b> วัน';
  const l2 = html('div', 'gray', leg); l2.innerHTML = '<s></s>อยู่กรุงเทพฯ <b id="bkkN">365</b> วัน';
  const homeN = l1.querySelector('b'), bkkN = l2.querySelector('b');
  SHOTS.push({
    a: 8.07, b: 10.33, S,
    update(lt) {
      room.pose(lt);
      applyPop(card, lt, 0.02);
      let lit = 0;
      order.forEach((idx, k) => {
        const t0 = 0.4 + k * 0.1;
        const on = lt >= t0;
        if (on) lit++;
        const c = cells[idx];
        c.className = on ? 'on' : '';
        const sc = on ? 1 + 0.5 * Math.max(0, 1 - (lt - t0) / 0.2) : 1;
        c.style.transform = `scale(${sc})`;
      });
      homeN.textContent = lit;
      bkkN.textContent = 365 - lit;
    },
  });
})();

// D5 — mom's room at night: she crosses day 23; counter 0 → 355
(() => {
  const S = makeShot();
  const room = momRoom(S.s, S.defs, true);
  const card = html('div', 'card', S.ui);
  card.style.left = '60px'; card.style.top = '120px';
  html('div', 'lbl', card, 'แม่นับวันรอ');
  const num = html('div', 'num', card);
  num.innerHTML = '<span>0</span><small>วัน</small>';
  const n = num.querySelector('span');
  SHOTS.push({
    a: 10.33, b: 14.6, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 4.27), 1.0, 1.08, 560, 760);
      const pose = { x: 885, y: 1195, s: 1.1, f: -1, torso: 4, head: -8, aB: [96, 92], lF: [90, 90], lB: [92, 90], eyes: 1, smile: 0.35 };
      // stroke 1 then stroke 2 of the X, the hand follows the pen tip
      const [tx, ty] = room.target, o = 19;
      const k1 = ease.inOutSine(prog(lt, 0.55, 0.85)), k2 = ease.inOutSine(prog(lt, 1.0, 1.3));
      let px, py;
      if (lt < 0.95) { px = tx - o + 2 * o * k1; py = ty - o + 2 * o * k1; }
      else { px = tx + o - 2 * o * k2; py = ty - o + 2 * o * k2; }
      const raise = ease.inOutSine(prog(lt, 0.05, 0.5)) * (1 - ease.inOutSine(prog(lt, 1.55, 2.0)));
      const restA = [98, 96];
      const reachA = reachTo(room.p, pose, px - 18, py + 50);
      pose.aF = [lerp(restA[0], reachA[0], raise), lerp(restA[1], reachA[1], raise)];
      pose.propRot = lerp(0, -20, raise);
      pose.head = lerp(-4, -14, raise) + lerp(0, -10, ease.inOutSine(prog(lt, 2.0, 2.6)));
      pose.smile = lerp(0.35, 0.8, ease.inOutSine(prog(lt, 2.0, 2.6)));
      room.p.pose(pose);
      room.xA.setAttribute('stroke-dashoffset', 60 * (1 - k1));
      room.xB.setAttribute('stroke-dashoffset', 60 * (1 - k2));
      applyPop(card, lt, 0.1);
      n.textContent = countUp(lt, 0.4, 2.7, 0, 355);
    },
  });
})();

// D6 — title card over the blurred room
(() => {
  const S = makeShot();
  momRoom(S.s, S.defs, true).p.pose({ x: 885, y: 1195, s: 1.1, f: -1, torso: 4, head: -14, aF: [98, 96], aB: [96, 92], eyes: 1, smile: 0.8 });
  S.cam.style.filter = 'blur(16px) brightness(0.45)';
  const pill = html('div', 'pill', S.ui);
  pill.innerHTML = '<svg width="16" height="16"><circle cx="8" cy="8" r="7" fill="#cf483d"/></svg>เดโม';
  pill.style.left = '440px'; pill.style.top = '610px';
  const t1 = html('div', 'title', S.ui, '355 วัน'); t1.style.top = '700px'; t1.style.font = "700 170px/1 Kanit";
  const t2 = html('div', 'title', S.ui, 'ที่แม่รอ'); t2.style.top = '890px'; t2.style.font = "600 120px/1 Kanit";
  const rule = html('div', '', S.ui); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#cf483d' });
  const c1 = html('div', 'title', S.ui, 'เดโมสั้นจากบท "355 วันที่แม่รอ"'); c1.style.top = '1130px'; c1.style.font = "500 40px/1.3 Kanit"; c1.style.color = '#f2c75f';
  const c2 = html('div', 'title', S.ui, 'ฉบับเต็มยาวราว 70 วินาที'); c2.style.top = '1190px'; c2.style.font = "400 36px/1.3 Kanit"; c2.style.color = '#cfd2e6';
  SHOTS.push({
    a: 14.6, b: 17.0, S,
    update(lt) {
      const f = (el, t0) => { const k = ease.outCubic(prog(lt, t0, t0 + 0.45)); el.style.opacity = k; el.style.transform = `translateY(${(1 - k) * 24}px)`; };
      f(pill, 0.1); f(t1, 0.2); f(t2, 0.35); f(rule, 0.5); f(c1, 0.65); f(c2, 0.8);
      rule.style.transform = `scaleX(${ease.outCubic(prog(lt, 0.5, 0.9))})`;
      S.root.style.opacity = 1 - prog(lt, 2.0, 2.4);
    },
  });
})();

const DURATION = 17.0;
window.render = t => {
  for (const sh of SHOTS) {
    const on = t >= sh.a && t < sh.b;
    sh.S.root.style.display = on ? 'block' : 'none';
    if (on) sh.update(t - sh.a);
  }
  renderSubs(subsBox, CUES, t);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
