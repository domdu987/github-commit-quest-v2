// Demo v2 — restyled to the reference clip's look. Same narration timing as v1 (VO starts at 0.4 s).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');

const GIRL = { R: 44, skin: '#d8ab86', skinShade: '#c3936d', hair: '#2a2220', hairStyle: 'ponytail', shirt: '#7fa3cf', shirtLight: '#94b5dc', shirtDark: '#6e90bb', sleeve: 'long', shirtLen: 'top', pants: '#2c3555', pantsDark: '#232a45', seed: 1 };
const GIRL_PACK = Object.assign({}, GIRL, { backpack: '#2e3140' });
const MOM = { R: 44, skin: '#c8956e', skinShade: '#b3805b', hair: '#3a3234', gray: '#b5aeae', hairStyle: 'bun', shirt: '#a84d63', shirtLight: '#bb5d73', shirtDark: '#8f4054', sleeve: 'short', shirtLen: 'top', sarong: '#5b3f7a', sarongDark: '#463063', pants: '#5b3f7a', pantsDark: '#4a3266', shoe: '#7b5236', shoeDark: '#5f3e28', earring: null, glasses: true, lashes: false, seed: 2 };

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
const heartPath = (cx, cy, r) => `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`;
const heartSVG = (size, color) => `<svg width="${size}" height="${size}" viewBox="-12 -12 24 24"><path d="${heartPath(0, 0, 9)}" fill="${color}"/></svg>`;
const moonSVG = `<svg width="38" height="38" viewBox="0 0 16 16"><path d="M11.5 11.8A5.5 5.5 0 0 1 6.2 2.3a5.6 5.6 0 1 0 7.3 7.4 5.4 5.4 0 0 1-2 2.1z" fill="#f2d48a"/></svg>`;
const batterySVG = (pct, color) => `<svg width="56" height="30" viewBox="0 0 56 30"><rect x="2" y="3" width="46" height="24" rx="6" fill="none" stroke="#fff" stroke-width="3"/><rect x="50" y="10" width="4" height="10" rx="2" fill="#fff"/><rect x="6" y="7" width="${Math.max(3, 38 * pct)}" height="16" rx="3" fill="${color}"/></svg>`;
function momAvatar() {
  return `<svg width="92" height="92" viewBox="-46 -46 92 92"><circle r="46" fill="#f0d5c4"/>
  <circle cx="0" cy="-34" r="13" fill="#3a3234"/><circle r="30" cy="6" fill="#c8956e"/>
  <path d="M-30,2 C-28,-30 28,-30 30,2 C16,-14 -16,-14 -30,2 Z" fill="#3a3234"/>
  <path d="M-16,-16 C-6,-22 6,-22 16,-16" stroke="#b5aeae" stroke-width="3" fill="none" stroke-linecap="round"/>
  <rect x="-20" y="-2" width="15" height="11" rx="3" fill="none" stroke="#4a3c3a" stroke-width="2.4"/><rect x="5" y="-2" width="15" height="11" rx="3" fill="none" stroke="#4a3c3a" stroke-width="2.4"/>
  <circle cx="-12" cy="4" r="2.6" fill="#1e1718"/><circle cx="12" cy="4" r="2.6" fill="#1e1718"/>
  <path d="M-7,18 Q0,24 7,18" stroke="#8a4a3c" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>`;
}

const SHOTS = [];
// slow dust motes drifting through lamp light
function dust(parent, cx, cy, rw, rh, n, seed, color = '#ffe9c4') {
  const r = rng(seed), motes = [];
  for (let i = 0; i < n; i++) motes.push({ el: svg('circle', { r: 1.5 + r() * 2.5, fill: color }, parent), x: cx + (r() - 0.5) * rw, y: cy + (r() - 0.5) * rh, ph: r() * 6.28, sp: 6 + r() * 10 });
  return t => motes.forEach(m => setA(m.el, { cx: (m.x + Math.sin(t * 0.6 + m.ph) * 18).toFixed(1), cy: (m.y - ((t * m.sp) % 120) + 60).toFixed(1), opacity: (0.25 + 0.35 * (0.5 + 0.5 * Math.sin(t * 1.3 + m.ph))).toFixed(2) }));
}

// D1 — condo at night: notification from Mom while she sits on the sofa
(() => {
  const S = makeShot();
  condoNight(S.s, S.defs);
  const shadow = contactShadow(S.s, S.defs, 420, 1328, 120, 14, 0.4);
  const p = new Puppet(S.s, GIRL, S.defs);
  const ph = svg('g', {}, p.prop);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: '#15151b' }, ph);
  svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, ph);
  const glow = svg('circle', { r: 140, fill: rad2(S.defs, [[0, '#cfe1ff', 0.5], [1, '#cfe1ff', 0]]) }, S.s);
  const dust1 = dust(S.s, 900, 860, 360, 380, 18, 21);
  vignette(S.s, S.defs, 0.5);
  const clock = html('div', 'clock', S.ui);
  clock.style.left = '56px'; clock.style.top = '110px';
  clock.innerHTML = `<div class="ic">${moonSVG}</div><div><div class="tl">อังคาร</div><div class="tt">21:40</div><div class="sl"><i style="left:68%"></i></div></div>`;
  const bat = html('div', 'pill red', S.ui);
  bat.style.left = '760px'; bat.style.top = '128px';
  bat.innerHTML = `${batterySVG(0.06, '#ff6b5e')}<b>3%</b>`;
  const n = html('div', 'notif', S.ui);
  n.style.top = '440px';
  n.innerHTML = `<div class="av">${momAvatar()}</div><div style="flex:1"><div class="who">แม่ ${heartSVG(28, '#dc6c89')}<small>เมื่อสักครู่</small></div><div class="msg">สงกรานต์นี้กลับบ้านมั้ยลูก</div></div>`;
  SHOTS.push({
    a: 0, b: 2.27, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 2.27), 1.0, 1.06, 420, 1000);
      dust1(lt + 3);
      const br = Math.sin(lt * 2.2) * 1.2;
      p.pose({ x: 352, y: 1162, torso: 6 + br, head: 18, aF: [76, -46], aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 0.7, smile: 0.45 });
      const w = p.wristF;
      setA(glow, { cx: 352 + w[0] + 10, cy: 1162 + w[1] - 26 });
      applyPop(clock, lt, 0.05);
      applyPop(bat, lt, 0.12);
      const k = ease.outBack(prog(lt, 0.25, 0.65));
      n.style.opacity = clamp(prog(lt, 0.25, 0.45));
      n.style.transform = `translateY(${(1 - k) * -60}px)`;
    },
  });
})();

// D2 — bus terminal, Friday 20:30, purple bus to Khon Kaen
(() => {
  const S = makeShot();
  terminal(S.s, S.defs);
  const bus = tourBus(S.s, S.defs, -40, 1100, 1180, 'กรุงเทพฯ - ขอนแก่น');
  // waiting passengers in silhouette near the door
  const SIL = { R: 44, skin: '#171827', skinShade: '#141523', hair: '#121320', hairStyle: 'short', shirt: '#1a1b2b', shirtLight: '#1c1d2e', shirtDark: '#151624', sleeve: 'long', shirtLen: 'long', pants: '#141522', pantsDark: '#121320', shoe: '#141522', shoeDark: '#121320', earring: null, lashes: false, flat: true };
  const sils = [[870, 0.5, 0], [925, 0.52, 1]].map(([x, sc, k]) => { const q = new Puppet(S.s, Object.assign({}, SIL, { hairStyle: k ? 'ponytail' : 'short', hairTie: '#121320' }), S.defs); q.pose({ x, y: 1100 - 300 * sc, s: sc, f: k ? -1 : 1, torso: 2, head: 4, aF: [96, 94], aB: [92, 90], eyes: 1 }); return q; });
  contactShadow(S.s, S.defs, 330, 1478, 110, 14, 0.5);
  const p = new Puppet(S.s, GIRL_PACK, S.defs);
  const ph = svg('g', {}, p.prop);
  svg('rect', { x: -15, y: -42, width: 30, height: 58, rx: 7, fill: '#15151b' }, ph);
  svg('rect', { x: -11, y: -38, width: 22, height: 50, rx: 4, fill: '#d8e8ff' }, ph);
  const glow = svg('circle', { r: 120, fill: rad2(S.defs, [[0, '#cfe1ff', 0.45], [1, '#cfe1ff', 0]]) }, S.s);
  vignette(S.s, S.defs, 0.45);
  const clock = html('div', 'clock', S.ui);
  clock.style.left = '56px'; clock.style.top = '110px';
  clock.innerHTML = `<div class="ic">${moonSVG}</div><div><div class="tl">ศุกร์</div><div class="tt">20:30</div><div class="sl"><i style="left:62%"></i></div></div>`;
  const led = html('div', 'led', S.ui);
  led.style.left = '56px'; led.style.top = '300px';
  led.innerHTML = `<div class="a"><span>20:30</span><span>ขอนแก่น</span></div><div class="b">กำลังขึ้นรถ</div>`;
  const bay = html('div', 'bay', S.ui, 'ชานชาลา 18');
  bay.style.left = '760px'; bay.style.top = '290px';
  const card = html('div', 'card', S.ui);
  card.style.left = '640px'; card.style.top = '110px'; card.style.minWidth = '330px';
  html('div', 'lbl', card, 'กลับบ้าน');
  const num = html('div', 'num', card);
  num.innerHTML = '<span>0</span><small>ครั้ง/ปี</small>';
  const nEl = num.querySelector('span');
  SHOTS.push({
    a: 2.27, b: 4.12, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 1.85), 1.0, 1.08, 330, 1150);
      const br = Math.sin(lt * 2.0) * 1;
      p.pose({ x: 330, y: 1172, s: 1.02, torso: 3 + br, head: 16, aF: [80, -30], aB: [96, 94], lF: [88, 90], lB: [93, 92], t: lt + 2.1, smile: 0.55 });
      const w = p.wristF;
      setA(glow, { cx: 330 + w[0] * 1.02 + 10, cy: 1172 + w[1] * 1.02 - 24 });
      applyPop(clock, lt, 0.02);
      applyPop(led, lt, 0.08);
      bay.style.opacity = 1 - prog(lt, 0.0, 0.3);
      applyPop(card, lt, 0.3);
      nEl.textContent = countUp(lt, 0.45, 1.1, 0, 2);
    },
  });
})();

// D3 — the bus on the night highway, a question mark above it
(() => {
  const S = makeShot();
  const world = svg('g', { transform: 'translate(0,250)' }, S.s);
  svg('rect', { x: 0, y: -250, width: 1080, height: 260, fill: '#161a3a' }, world);
  const hw = highway(world, S.defs);
  const bus = tourBus(world, S.defs, 40, 1150, 1000, 'กรุงเทพฯ - ขอนแก่น');
  // her silhouette in a window
  svg('circle', { cx: 40 + 30 + 4 * 112 + 48, cy: 1150 - 330 + 74, r: 22, fill: '#2b2235' }, bus.g);
  svg('rect', { x: 40 + 30 + 4 * 112 + 30, y: 1150 - 330 + 92, width: 36, height: 30, rx: 10, fill: '#2b2235' }, bus.g);
  vignette(S.s, S.defs, 0.5);
  const q = html('div', 'qmark', S.ui, '?');
  q.style.left = '445px'; q.style.top = '790px';
  SHOTS.push({
    a: 4.12, b: 8.07, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 3.95), 1.0, 1.05, 540, 1250);
      hw.lamps.setAttribute('transform', `translate(${-((lt * 260) % 360)},0)`);
      hw.rail.setAttribute('transform', `translate(${-((lt * 620) % 160)},0)`);
      hw.refl.setAttribute('transform', `translate(${-((lt * 260) % 360)},0)`);
      bus.g.setAttribute('transform', `translate(0,${Math.sin(lt * 9) * 1.4})`);
      bus.wheels.forEach(w => { const m = w.getAttribute('transform').match(/translate\(([^)]+)\)/)[1]; w.setAttribute('transform', `translate(${m}) rotate(${(lt * 400) % 360})`); });
      const pp = pop(lt, 0.15, 0.45);
      const pulse = 1 + 0.04 * Math.sin(lt * 5);
      q.style.opacity = pp.o;
      q.style.transform = `scale(${pp.s * pulse})`;
      q.style.boxShadow = `0 0 0 ${14 + 10 * (0.5 + 0.5 * Math.sin(lt * 5))}px rgba(200,196,215,${0.25 + 0.15 * Math.sin(lt * 5)}), 0 20px 40px rgba(0,0,0,.4)`;
    },
  });
})();

// D4 — on the bus seat (blurred), waffle card: 365 days, 10 at home
(() => {
  const S = makeShot();
  busSeat(S.s, S.defs);
  const p = new Puppet(S.s, GIRL, S.defs);
  S.cam.style.filter = 'blur(12px) brightness(0.78)';
  const card = html('div', 'card pink', S.ui);
  card.style.left = '64px'; card.style.top = '190px'; card.style.width = '952px';
  html('div', 'lbl', card, '1 ปี = 365 วัน');
  const grid = html('div', 'waffle', card);
  const order = [101, 102, 103, 104, 105, 363, 364, 0, 1, 2];
  const cells = [];
  for (let i = 0; i < 365; i++) cells.push(html('i', '', grid));
  const leg = html('div', 'legend', card);
  const l1 = html('div', '', leg); l1.innerHTML = '<s></s>อยู่บ้าน <b>0</b> วัน';
  const l2 = html('div', 'gray', leg); l2.innerHTML = '<s></s>อยู่กรุงเทพฯ <b>365</b> วัน';
  const homeN = l1.querySelector('b'), bkkN = l2.querySelector('b');
  SHOTS.push({
    a: 8.07, b: 10.33, S,
    update(lt) {
      p.pose({ x: 470, y: 1250, torso: -6, head: -12, aF: [80, 12], aB: [84, 16], lF: [-4, 88], lB: [-2, 90], eyes: 0, t: lt, smile: 0.3 });
      applyPop(card, lt, 0.02);
      let lit = 0;
      order.forEach((idx, k) => {
        const t0 = 0.4 + k * 0.1, on = lt >= t0;
        if (on) lit++;
        cells[idx].className = on ? 'on' : '';
        cells[idx].style.transform = `scale(${on ? 1 + 0.5 * Math.max(0, 1 - (lt - t0) / 0.2) : 1})`;
      });
      homeN.textContent = lit;
      bkkN.textContent = 365 - lit;
    },
  });
})();

// shared builder for mom's room (used by D5 and blurred under D6)
function momScene(S) {
  momHouse(S.s, S.defs);
  const g = S.s;
  // graduation photo
  svg('rect', { x: 60, y: 560, width: 220, height: 270, rx: 8, fill: '#3a2a1e' }, g);
  svg('rect', { x: 76, y: 576, width: 188, height: 238, fill: lin(S.defs, [[0, '#c7d4e2'], [1, '#a9bccf']]) }, g);
  svg('path', { d: 'M104,814 C106,742 234,742 236,814 Z', fill: '#1d1d24' }, g);
  svg('path', { d: 'M144,760 C154,800 186,800 196,760', fill: 'none', stroke: '#f5d76e', 'stroke-width': 10, 'stroke-linecap': 'round' }, g);
  faceFront(g, 170, 700, 42, { skin: '#d8ab86', hair: '#2a2220', hairStyle: 'bob' });
  svg('path', { d: 'M114,654 L170,632 L226,654 L170,674 Z', fill: '#1d1d24' }, g);
  svg('path', { d: 'M216,656 L224,702', stroke: '#f5d76e', 'stroke-width': 4 }, g);
  // calendar (March 2026 starts on Sunday)
  const cal = svg('g', { transform: 'translate(320,430)' }, g);
  svg('rect', { x: 6, y: 10, width: 430, height: 560, rx: 10, fill: '#000', opacity: 0.18 }, cal);
  svg('path', { d: 'M215,-60 L120,0 M215,-60 L310,0', stroke: '#2a1d14', 'stroke-width': 3 }, cal);
  svg('circle', { cx: 215, cy: -62, r: 7, fill: '#2a1d14' }, cal);
  svg('rect', { x: 0, y: 0, width: 430, height: 560, rx: 10, fill: '#f6f1e6' }, cal);
  svg('path', { d: 'M0,10 Q0,0 10,0 L420,0 Q430,0 430,10 L430,86 L0,86 Z', fill: '#cf483d' }, cal);
  const tt = svg('text', { x: 215, y: 58, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 40, fill: '#fff' }, cal); tt.textContent = 'มีนาคม 2569';
  ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'].forEach((d, i) => { const e = svg('text', { x: 34 + i * 60, y: 124, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 500, 'font-size': 22, fill: i === 0 ? '#cf483d' : '#6b6670' }, cal); e.textContent = d; });
  const cell = d => { const i = d - 1; return [34 + (i % 7) * 60, 176 + Math.floor(i / 7) * 82]; };
  for (let d = 1; d <= 31; d++) {
    const [cx, cy] = cell(d);
    const e = svg('text', { x: cx, y: cy + 12, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 600, 'font-size': 34, fill: '#2f2c33' }, cal); e.textContent = d;
    if (d <= 27) svg('path', { d: `M${cx - 19},${cy - 19} L${cx + 19},${cy + 19} M${cx + 19},${cy - 19} L${cx - 19},${cy + 19}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.9 }, cal);
  }
  const [x28, y28] = cell(28), o = 19;
  const xA = svg('path', { d: `M${x28 - o},${y28 - o} L${x28 + o},${y28 + o}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-dasharray': 60, 'stroke-dashoffset': 60 }, cal);
  const xB = svg('path', { d: `M${x28 + o},${y28 - o} L${x28 - o},${y28 + o}`, stroke: '#cf483d', 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-dasharray': 60, 'stroke-dashoffset': 60 }, cal);
  // a low cabinet with a thermos and a radio, for a lived-in home
  svg('rect', { x: 40, y: 1180, width: 280, height: 200, rx: 10, fill: '#5a3a26' }, g);
  svg('rect', { x: 52, y: 1196, width: 124, height: 168, rx: 6, fill: '#6a4630' }, g);
  svg('rect', { x: 184, y: 1196, width: 124, height: 168, rx: 6, fill: '#6a4630' }, g);
  svg('rect', { x: 80, y: 1100, width: 54, height: 80, rx: 12, fill: '#c94f4a' }, g);
  svg('rect', { x: 180, y: 1124, width: 110, height: 56, rx: 10, fill: '#3d4a5c' }, g);
  svg('circle', { cx: 210, cy: 1152, r: 16, fill: '#25303f' }, g);
  contactShadow(g, S.defs, 885, 1530, 110, 14, 0.5);
  const p = new Puppet(g, MOM, S.defs);
  const marker = svg('g', {}, p.prop);
  svg('rect', { x: -6, y: -46, width: 12, height: 54, rx: 5, fill: '#cf483d' }, marker);
  svg('rect', { x: -6, y: -46, width: 12, height: 15, rx: 5, fill: '#efe9e1' }, marker);
  return { p, xA, xB, target: [320 + x28, 430 + y28] };
}

// D5 — Mom crosses out day 28; counter 0 → 355
(() => {
  const S = makeShot();
  const room = momScene(S);
  const dust5 = dust(S.s, 600, 420, 700, 520, 22, 37);
  vignette(S.s, S.defs, 0.5);
  const card = html('div', 'card', S.ui);
  card.style.left = '56px'; card.style.top = '110px';
  html('div', 'lbl', card, 'แม่นับวันรอ');
  const num = html('div', 'num', card);
  num.innerHTML = '<span>0</span><small>วัน</small>';
  const n = num.querySelector('span');
  SHOTS.push({
    a: 10.33, b: 14.6, S,
    update(lt) {
      camera(S.cam, prog(lt, 0, 4.27), 1.0, 1.08, 560, 800);
      dust5(lt + 1);
      const pose = { x: 885, y: 1235, s: 1.12, f: -1, torso: 4, head: -6, aB: [96, 92], lF: [90, 90], lB: [92, 90], t: lt + 0.4, smile: 0.35 };
      const [tx, ty] = room.target, o = 19;
      const k1 = ease.inOutSine(prog(lt, 0.55, 0.85)), k2 = ease.inOutSine(prog(lt, 1.0, 1.3));
      let px, py;
      if (lt < 0.95) { px = tx - o + 2 * o * k1; py = ty - o + 2 * o * k1; } else { px = tx + o - 2 * o * k2; py = ty - o + 2 * o * k2; }
      const raise = ease.inOutSine(prog(lt, 0.05, 0.5)) * (1 - ease.inOutSine(prog(lt, 1.55, 2.0)));
      const reachA = room.p.reach(pose, px - 18, py + 48);
      pose.aF = [lerp(96, reachA[0], raise), lerp(94, reachA[1], raise)];
      pose.propRot = lerp(0, -20, raise);
      pose.head = lerp(-4, -12, raise) + lerp(0, -8, ease.inOutSine(prog(lt, 2.0, 2.6)));
      pose.smile = lerp(0.35, 0.85, ease.inOutSine(prog(lt, 2.0, 2.6)));
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
  const room = momScene(S);
  room.p.pose({ x: 885, y: 1235, s: 1.12, f: -1, torso: 4, head: -12, aF: [96, 94], aB: [96, 92], eyes: 1, smile: 0.85 });
  room.xA.setAttribute('stroke-dashoffset', 0); room.xB.setAttribute('stroke-dashoffset', 0);
  S.cam.style.filter = 'blur(16px) brightness(0.42)';
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
