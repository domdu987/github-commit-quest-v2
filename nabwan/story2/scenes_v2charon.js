// "75 วันของพ่อ" — scenes timed to the Charon narration in vo.js (VO.P holds phrase onsets A0..D7).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

// scene windows and subtitle heights
const SC = { s1: [0, 7.62], s2: [7.62, 13.40], s3: [13.40, 22.25], s4: [22.25, 28.45], s5: [28.45, 34.35], s6: [34.35, 38.06], s7: [38.06, 40.25], s8a: [40.25, 43.85], s8b: [43.85, 47.62], s8c: [47.62, 51.75], s8d: [51.75, P.end], s9: [P.end, DURATION] };
const SUB_TOP = [[0, 7.62, 1490], [7.62, 28.45, 1700], [28.45, 34.35, 1490], [34.35, 38.06, 1610], [40.25, 43.85, 1490], [43.85, 47.62, 1610], [47.62, 51.75, 1196], [51.75, 99, 1700]];
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: (SUB_TOP.find(([a, b]) => c.a >= a - 0.3 && c.a < b) || [0, 0, 1196])[2] }));

const heartPath = (cx, cy, r) => `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`;
const moonSVG = `<svg width="40" height="40" viewBox="0 0 16 16"><path d="M11.5 11.8A5.5 5.5 0 0 1 6.2 2.3a5.6 5.6 0 1 0 7.3 7.4 5.4 5.4 0 0 1-2 2.1z" fill="#f2d48a"/></svg>`;
const calSVG = c => `<svg width="34" height="34" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="18" rx="4" fill="#fff" stroke="${c}" stroke-width="2"/><rect x="2" y="4" width="20" height="6" rx="3" fill="${c}"/></svg>`;
function cardEl(parent, cls, x, y, w) {
  const c = html('div', cls, parent);
  c.style.left = x + 'px'; c.style.top = y + 'px'; if (w) c.style.width = w + 'px';
  const sh = html('div', 'shine', c);
  return { c, sh };
}
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
const SHOTS = [];
const whip = (shot, lt, side) => {
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
// puppet geometry: torso-frame point -> world
const T150 = RIG.T;
const SS = 1.2, DS = 1.2;   // seated son / Dad scale
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function earWorld(p) { return toWorld(p, ...torsoPt(p, EAR_L[0], EAR_L[1])); }
function phoneProp(parent, oldPhone = false) {
  const g = svg('g', {}, parent);
  if (oldPhone) { svg('rect', { x: -13, y: -50, width: 26, height: 52, rx: 7, fill: '#4a4d57', stroke: INK, 'stroke-width': 3.5 }, g); const scr = svg('rect', { x: -9, y: -45, width: 18, height: 16, rx: 2, fill: '#89a58f' }, g); return { g, scr }; }
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: '#15151b', stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, g);
  return { g, scr };
}
function sweatDrops(parent, n, seed) {
  const r = rng(seed);
  const ds = Array.from({ length: n }, () => ({ el: svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#bfe9ff', stroke: '#fff', 'stroke-width': 1.5 }, parent), ph: r(), dx: (r() - 0.5) * 40 }));
  return (t, hx, hy) => ds.forEach(d => { const q = ((t * 0.9 + d.ph) % 1); setA(d.el, { transform: `translate(${(hx + d.dx + q * 10).toFixed(1)},${(hy + q * q * 120).toFixed(1)}) scale(${(1.2 - q * 0.4).toFixed(2)})`, opacity: (q < 0.1 ? q / 0.1 : 1 - q).toFixed(2) }); });
}
const rectCenter = el => { const r = el.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2, r.width]; };

// =====================================================================
// S1 — midnight: the son orders a 30,000-baht phone in five minutes
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.2], ['mid', 1, 0], ['fore', 1.9, 13]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = sonRoomNight(S);
  const M = S.L.mid;
  const son = new Puppet(M.s, SON, M.defs);
  const ph = phoneProp(son.prop);
  const glow = svg('circle', { r: 150, fill: rad2(M.defs, [[0, '#d4e5ff', 0.55], [1, '#d4e5ff', 0]]) }, M.s);
  const clock = cardEl(S.ui, 'clock', 56, 110);
  clock.c.innerHTML += `<div class="icslot"></div><div><div class="tl">คืนวันศุกร์</div><div class="tt"><span class="hhmm">23:59</span></div><div class="sl"><i style="left:96%"></i></div></div>`;
  const clk = clockMoon(clock.c.querySelector('.icslot'), 82);
  const hhmm = clock.c.querySelector('.hhmm'); hhmm.style.display = 'inline-block';
  const shop = productCard(S.ui, 198, 300, 620);
  const sw = stopwatchChip(S.ui, 198, 700);
  const fxs = fxSvg(S);
  const tTap = P.A2 + 0.3;
  const conf = burst(fxs, 505, 610, tTap + 0.05, 26, 211, ['#ff7a45', '#ffd66b', '#2f9e5b', '#4a7bd8', '#ff4d6d'], 300, 1.0);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-30, 25, k), y: 0, z: lerp(1.18, 1.28, k), fx: 430, fy: 1000 });
    set.update(lt);
    const look = ease.inOutSine(prog(lt, P.A3 + 0.6, P.A3 + 1.1));
    son.pose({ x: 352, y: 1162, s: SS, torso: 6 + Math.sin(lt * 2.2), head: lerp(18, 4, look), aF: [76, -46 + Math.sin(lt * 10) * 2 * (lt < tTap ? 1 : 0)], aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 0.7, smile: lt > tTap ? 1 : 0.55, grin: lt > tTap + 0.1 ? 0.8 : 0 });
    const w = son.wristF;
    setA(glow, { cx: 352 + w[0] * SS + 10, cy: 1162 + w[1] * SS - 26, opacity: (0.8 + 0.2 * Math.sin(lt * 13)).toFixed(3) });
    ph.scr.setAttribute('fill', lt > tTap && lt < tTap + 0.25 ? '#ffffff' : '#d8e8ff');
    enter3d(clock.c, lt, 0.05, 'flipDown'); shine(clock.sh, lt, 0.5);
    const mid = P.A2 + 0.1, flip = prog(lt, mid - 0.12, mid + 0.12);
    hhmm.textContent = lt < mid ? '23:59' : '00:00';
    hhmm.style.transform = `rotateX(${(Math.sin(Math.PI * flip) * 80).toFixed(1)}deg)`;
    clk.update(lt, lt < mid ? 23 : 0, lt < mid ? 59 : 0); popSquash(clk.el, lt, 0.2);
    shop.update(lt, P.A0 - 0.15, P.A1 + 0.2, tTap);
    sw.update(lt, P.A3 + 0.05);
    conf(lt);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — noon on the site: Dad carries cement; 38°C, ฿30,000, sweat, 75 days
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['sky', 0.08, 0], ['far', 0.25, 1.2], ['mid', 1, 0], ['fore', 1.6, 9]]);
  S.grade = 'saturate(1.1) contrast(1.04) brightness(1.03)';
  const set = constructionSite(S, 1640);
  const M = S.L.mid, G = 1640, s = 1.15, hip = G - LEG * s;
  const sh = castShadow(M.s, M.defs, DAD_WORK, G, 40, 0.18, 0.28, 3);
  const dad = new Puppet(M.s, DAD_WORK, M.defs);
  cementBag(dad.shoulderG, M.defs, -112, -6, 0.98);
  const fxs = fxSvg(S);
  const sweat = sweatDrops(fxs, 4, 19);
  const haze = Array.from({ length: 6 }, (_, i) => svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 3, opacity: 0.18 }, fxs));
  const sun = sunThermo(S.ui, 50, 110);
  const money = moneyCard(S.ui, 556, 120);
  const drop = sweatDrop(S.ui, 150, 420, 120);
  const days = daysBigCard(S.ui, 330, 640);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-60, 40, k), y: 0, z: lerp(1.0, 1.06, k), fx: 540, fy: 1300 });
    set.update(lt + 3);
    const x = -120 + 112 * lt;
    const gw = gait(2 * Math.PI * ((x + 120) / 240), 12, 0);
    const pose = { x, y: hip + gw.bob * 0.6, s, f: 1, torso: 12, head: 8, lF: gw.lF, lB: gw.lB, aB: gw.aB, t: lt + 4, smile: 0.2 };
    pose.aF = dad.reach(pose, ...toWorld(pose, ...torsoPt(pose, -66, -T150 - 50)), true);
    dad.pose(pose); sh.pose(pose);
    const [hx, hy] = rectCenter(dad.head);
    sweat(lt, hx + 10, hy + 10);
    haze.forEach((h, i) => { const yy = 1500 - ((lt * 60 + i * 120) % 700); h.setAttribute('d', `M-50,${yy} q60,-14 120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0 t120,0`); h.setAttribute('transform', `translate(${(-((lt * 40 + i * 50) % 120)).toFixed(1)},0)`); });
    const L = t => t - A;
    sun.update(lt, L(P.A4) + 0.1);
    money.update(lt, L(P.A5) - 0.1);
    drop.update(lt, L(P.A6) - 0.05);
    days.update(lt, L(P.A7) - 0.15);
    const inK = 1 - prog(lt, 0, 0.25);
    setGrade(S, inK * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — closer: "พ่อ · ช่างปูน", 400 บาท/วัน, 30,000 ÷ 400 = 75, lifts a bag, back pain
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['sky', 0.08, 0], ['far', 0.25, 2], ['mid', 1, 0], ['fore', 1.6, 10]]);
  S.grade = 'saturate(1.1) contrast(1.05)';
  const set = constructionSite(S, 1640);
  const M = S.L.mid, G = 1640, s = 1.1, hip = G - LEG * s;
  const L = t => t - A;
  // mortar tray, a bag on the ground that gets lifted
  const tray = svg('g', { transform: `translate(560,${G})` }, M.s);
  svg('path', { d: 'M-80,0 L80,0 L66,-34 L-66,-34 Z', fill: '#7a8089', stroke: '#5b6068', 'stroke-width': 4 }, tray);
  svg('ellipse', { cx: 0, cy: -30, rx: 62, ry: 8, fill: '#b9b2a4' }, tray);
  const sh = castShadow(M.s, M.defs, DAD_WORK, G, 40, 0.18, 0.28, 3);
  const bag = svg('g', {}, M.s); cementBag(bag, M.defs, -112, -6, 0.98);
  const dad = new Puppet(M.s, DAD_WORK, M.defs);
  const hoe = svg('g', {}, dad.prop);
  svg('path', { d: 'M0,-60 L0,110', stroke: '#8a5a34', 'stroke-width': 7, 'stroke-linecap': 'round' }, hoe);
  svg('path', { d: 'M-24,104 L24,104 L20,126 L-20,126 Z', fill: '#9aa0aa' }, hoe);
  const fxs = fxSvg(S);
  const sweat = sweatDrops(fxs, 5, 23);
  const pain = svg('g', { opacity: 0 }, fxs);
  for (let i = 0; i < 6; i++) svg('path', { d: 'M0,-18 L6,-6 L18,-8 L8,2 L14,16 L0,8 L-12,16 L-8,2 L-18,-8 L-6,-6 Z', fill: i % 2 ? '#ffd66b' : '#e2382c', transform: `rotate(${i * 60}) translate(0,-46) scale(${0.7 + (i % 3) * 0.2})` }, pain);
  svg('circle', { r: 26, fill: 'none', stroke: '#e2382c', 'stroke-width': 5 }, pain);
  const tag = nameTag(S.ui, 56, 110);
  const wage = wageCard(S.ui, 540, 100);
  const eq = equationCard(S.ui, 70, 420, 940);
  const thermo = sunThermo(S.ui, 760, 640);
  const tLift = L(P.B2) - 0.1, tWalk = L(P.B2) + 0.6, tHurt = L(P.B3) + 0.05;
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-30, 10, k), y: lerp(40, 60, k), z: lerp(1.38, 1.46, k), fx: 520, fy: 1250 });
    set.update(lt + 9);
    const lift = ease.inOutSine(prog(lt, tLift, tLift + 0.7));
    const walkX = lt > tWalk ? 110 * Math.min(lt - tWalk, tHurt - tWalk) : 0;
    const walking = lt > tWalk && lt < tHurt;
    const gw = gait(2 * Math.PI * walkX / 240, walking ? 12 : 0, 0);
    const hurt = ease.inOutSine(prog(lt, tHurt, tHurt + 0.35));
    const mix = lt < tLift ? Math.sin(lt * 5) : 0;
    const x = 400 + walkX;
    const pose = { x, y: hip + (walking ? gw.bob * 0.6 : 0), s, f: 1, torso: lerp(lerp(28 + mix * 4, 12, lift), 4, hurt), head: lerp(lerp(14, 8, lift), -14, hurt), lF: walking ? gw.lF : [84, 92], lB: walking ? gw.lB : [98, 92], t: lt + 6, smile: lerp(0.3, 0, hurt), eyes: hurt > 0.5 ? 0 : null };
    const onShoulder = lift >= 1;
    // bag: on the ground → shoulder; it sits behind Dad, his hand grips its rear corner
    const [sx, sy] = toWorld(pose, ...torsoPt(pose, 0, -T150));
    const gx = x + 190, gy = G;
    const bx = lerp(gx, sx, lift), by = lerp(gy, sy, lift) - Math.sin(Math.PI * lift) * 60;
    const brot = onShoulder ? pose.torso : lerp(0, pose.torso, lift);
    const [gx2, gy2] = [bx + Math.cos(rad(brot)) * -66 * s + Math.sin(rad(brot)) * 50 * s, by + Math.sin(rad(brot)) * -66 * s - Math.cos(rad(brot)) * 50 * s];
    pose.aF = lift < 0.05 ? [lerp(40, 60, (mix + 1) / 2), lerp(70, 100, (mix + 1) / 2)] : dad.reach(pose, gx2, gy2, true);
    pose.aB = hurt > 0 ? [lerp(walking ? gw.aB[0] : 100, 150, hurt), lerp(walking ? gw.aB[1] : 96, 30, hurt)] : (lt < tLift ? [60 + mix * 10, 90] : (walking ? gw.aB : [100, 96]));
    dad.pose(pose); sh.pose(pose);
    hoe.setAttribute('opacity', lt < tLift + 0.1 ? 1 : 0);
    bag.setAttribute('transform', `translate(${bx.toFixed(1)},${by.toFixed(1)}) rotate(${brot.toFixed(2)}) scale(${s})`);
    const [hx, hy] = rectCenter(dad.head);
    sweat(lt, hx + 12, hy + 12);
    const shake = hurt > 0 && lt < tHurt + 0.5 ? Math.sin(lt * 70) * 6 * (1 - prog(lt, tHurt, tHurt + 0.5)) : 0;
    S.root.style.transform = `translateX(${shake.toFixed(1)}px)`;
    const [bkx, bky] = rectCenter(dad.torso);
    pain.setAttribute('opacity', hurt > 0 ? (0.6 + 0.4 * Math.sin(lt * 14)).toFixed(2) : 0);
    pain.setAttribute('transform', `translate(${(bkx - 30).toFixed(1)},${(bky + 30).toFixed(1)}) scale(${(0.8 + 0.25 * spring(lt, tHurt, 14, 5)).toFixed(3)}) rotate(${(lt * 30).toFixed(1)})`);
    // UI: cards come in with the words, then clear for the heat beat
    const out1 = ease.inCubic(prog(lt, tLift - 0.15, tLift + 0.25));
    tag.update(lt, L(P.B0) - 0.05); tag.el.style.opacity = (parseFloat(tag.el.style.opacity) * (1 - out1)).toFixed(3);
    wage.update(lt, L(P.B1) - 0.1); wage.c.c.style.opacity = (parseFloat(wage.c.c.style.opacity) * (1 - out1)).toFixed(3);
    eq.update(lt, L(P.B1) + 1.55); eq.c.c.style.opacity = (parseFloat(eq.c.c.style.opacity) * (1 - out1)).toFixed(3);
    thermo.update(lt, L(P.B2) + 0.2);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — break in the shade: Dad's old keypad phone, ten years old, screen cracked
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['sky', 0.08, 0], ['far', 0.25, 3], ['mid', 1, 2], ['fore', 1.6, 10]]);
  S.grade = 'saturate(0.95) contrast(1.05) brightness(0.92)';
  const set = constructionSite(S, 1640);
  const M = S.L.mid;
  const L = t => t - A;
  svg('rect', { x: 600, y: 700, width: 640, height: 960, fill: '#1d2440', opacity: 0.2, filter: blurFilter(M.defs, 40) }, M.s);
  for (const px of [590, 1230]) svg('rect', { x: px - 7, y: 640, width: 14, height: 1000, rx: 5, fill: '#8a6a3a' }, M.s);
  const tarp = svg('path', { fill: lin(M.defs, [[0, '#3f7fd0'], [1, '#2c5fa8']]) }, M.s);
  const tarpEdge = svg('path', { fill: 'none', stroke: '#9cc4f0', 'stroke-width': 5, opacity: 0.7 }, M.s);
  const dad = new Puppet(M.s, DAD_WORK, M.defs);
  const op = phoneProp(dad.prop, true);
  const card = oldPhoneCard(S.ui, 70, 150);
  const cmp = html('div', 'cmpchip', S.ui); cmp.style.left = '440px'; cmp.style.top = '170px';
  cmp.innerHTML = `${phoneSVG(34, 58)}<span>มือถือลูก <b>฿30,000</b></span>`;
  const cmp2 = html('div', 'cmpchip', S.ui); cmp2.style.left = '440px'; cmp2.style.top = '270px';
  cmp2.innerHTML = `${oldPhoneSVG(30, 58)}<span>มือถือพ่อ <b>ปุ่มกด</b></span>`;
  S.update = lt => {
    S.cam({ x: 40, y: 20, z: lerp(1.3, 1.36, prog(lt, 0, B - A)), fx: 830, fy: 1200 });
    set.update(lt + 14);
    const sag = Math.sin(lt * 1.6) * 6;
    tarp.setAttribute('d', `M560,628 Q900,${(600 + sag).toFixed(1)} 1260,628 L1260,676 Q1180,${(700 + sag).toFixed(1)} 1100,676 Q1020,${(704 + sag).toFixed(1)} 940,676 Q860,${(704 + sag).toFixed(1)} 780,676 Q700,${(700 + sag).toFixed(1)} 620,676 L560,676 Z`);
    tarpEdge.setAttribute('d', `M560,632 Q900,${(604 + sag).toFixed(1)} 1260,632`);
    const take = ease.inOutSine(prog(lt, L(P.B4) - 0.1, L(P.B4) + 0.6));
    const pose = { x: 836, y: 1268, s: 1.1, f: -1, torso: 10, head: lerp(4, 22, take), lF: [-6, 92], lB: [2, 96], t: lt + 2, smile: lerp(0.2, 0.55, take), aB: [96, 80] };
    const [tx, ty] = toWorld(pose, ...torsoPt(pose, 52, -T150 + 40));
    const rest = [100, 60];
    const reachA = dad.reach(pose, tx, ty);
    pose.aF = [lerp(rest[0], reachA[0], take), lerp(rest[1], reachA[1], take)];
    pose.propRot = lerp(0, -70, take);
    dad.pose(pose);
    op.g.setAttribute('opacity', take > 0.2 ? 1 : 0);
    op.scr.setAttribute('fill', Math.sin(lt * 3) > 0 ? '#c8f0c0' : '#89a58f');
    card.update(lt, L(P.B4) + 0.05, L(P.B5) + 0.1, L(P.B6), L(P.B7) + 0.25);
    popSquash(cmp, lt, L(P.B4) + 0.3); popSquash(cmp2, lt, L(P.B5) - 0.05);
    const inK = whip(S, lt, 'out');
    setGrade(S, inK * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — the son, every day on his 30,000-baht phone
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.35, 1.2], ['mid', 1, 0], ['fore', 1.9, 13]]);
  S.grade = 'saturate(1.08) contrast(1.03)';
  const set = condoDay(S);
  const M = S.L.mid;
  const L = t => t - A;
  contactShadow(M.s, M.defs, 420, 1328, 120, 14, 0.3);
  const son = new Puppet(M.s, SON, M.defs);
  const ph = phoneProp(son.prop);
  const fxs = fxSvg(S);
  const bubbles = appBubbles(svg('g', {}, fxs), L(P.C1) + 0.1);
  const tag = html('div', 'pricetag', S.ui, '฿30,000'); tag.style.left = '500px'; tag.style.top = '820px';
  const every = html('div', 'chip big', S.ui); every.style.left = '600px'; every.style.top = '960px';
  const evCal = calendarFlip(every, 52); html('span', '', every, 'ถือทุกวัน');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(20, -10, k), y: 0, z: lerp(1.2, 1.3, k), fx: 430, fy: 1000 });
    set.update(lt);
    son.pose({ x: 352, y: 1162, s: SS, torso: 4 + Math.sin(lt * 2), head: 16, aF: [74, -48 + Math.sin(lt * 9) * 3], aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 3, smile: 0.9, grin: 0.5 });
    ph.scr.setAttribute('fill', ['#ffd1dc', '#d8e8ff', '#fff2c4'][Math.floor(lt * 3) % 3]);
    const [pxs, pys] = rectCenter(ph.scr);
    updateBubbles(bubbles, lt, pxs, pys - 40);
    popSquash(tag, lt, L(P.C1) + 0.5, 'rotate(-6deg)', -20);
    popSquash(every, lt, L(P.C2) + 0.1);
    evCal.update(lt, (Math.floor(lt * 6) % 31) + 1, lt > L(P.C2) + 0.1);
    const inK = whip(S, lt, 'in');
    setGrade(S, inK * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — night at Dad's: phone in hand, no calls — 0 ครั้ง
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.4, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.fadeIn = 0.3;
  S.grade = 'saturate(1.05) sepia(0.06) contrast(1.04)';
  const room = dadRoom(S, true);
  const L = t => t - A;
  const dad = new Puppet(room.people, DAD_HOME, S.L.mid.defs);
  const op = phoneProp(dad.prop, true);
  const log = callLogCard(S.ui, 150, 130, 716);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(0, 30, k), y: 40, z: lerp(1.25, 1.36, k), fx: 560, fy: 1100 });
    room.update(lt + 2);
    const sigh = ease.inOutSine(prog(lt, L(P.C4) - 0.2, L(P.C4) + 0.4));
    const pose = { x: 560, y: 1244, s: DS, f: -1, torso: lerp(6, 14, sigh), head: lerp(24, 6, sigh), lF: [-2, 90], lB: [0, 91], t: lt + 1, smile: lerp(0.3, 0.05, sigh), aB: [62, 12] };
    const [tx, ty] = toWorld(pose, ...torsoPt(pose, 46, -T150 + 46));
    pose.aF = dad.reach(pose, tx, ty); pose.propRot = -70;
    dad.pose(pose);
    op.scr.setAttribute('fill', '#7f9a86');
    room.photoGlow.setAttribute('opacity', (0.6 * sigh).toFixed(3));
    log.update(lt, L(P.C3) - 0.1, L(P.C4));
    setGrade(S, lerp(0, 14, ease.inCubic(prog(lt, B - A - 0.35, B - A))));
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — title: 75 วัน / ของพ่อ
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = dadRoom(S, false);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 93, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '520px';
  const hat = iconBox(ic, 150, 130, '0 0 100 86');
  svg('path', withStk({ d: 'M10,62 C10,14 90,10 92,62 Z', fill: lin(hat.defs, [[0, '#ffd66b'], [1, '#e8a92c']]) }, 5), hat.s);
  svg('rect', withStk({ x: 2, y: 58, width: 98, height: 14, rx: 7, fill: '#e0a12c' }, 4), hat.s);
  const hh = svg('path', withStk({ d: heartPath(74, 30, 12), fill: '#e0577a' }, 3), hat.s);
  const t1 = html('div', 'title', wrap); t1.style.top = '690px'; t1.style.font = '700 190px/1 Kanit';
  const digits = ['7', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'วัน'); unit.style.marginLeft = '0.28em';
  const t2 = html('div', 'title', wrap, 'ของพ่อ'); t2.style.top = '895px'; t2.style.font = '600 130px/1 Kanit';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#e0574b', boxShadow: '0 0 16px rgba(224,87,75,.8)' });
  const glint = html('div', '', wrap); glint.style.cssText = 'position:absolute;left:0;top:680px;width:260px;height:340px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));mix-blend-mode:overlay;opacity:0';
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5);
    bok(lt);
    popSquash(ic, lt, 0.05, `translateY(${(Math.sin(lt * 2) * 6).toFixed(1)}px)`, -16);
    hh.setAttribute('transform', `translate(74,30) scale(${(1 + 0.15 * Math.max(0, Math.sin(lt * 7.5))).toFixed(3)}) translate(-74,-30)`);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.1, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.4, 14, 7); unit.style.opacity = fadeIn(lt, 0.4, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.5, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.5, 0.95))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.75, 1.15)).toFixed(3)})`;
    const gk = prog(lt, 1.1, 1.8);
    glint.style.opacity = gk > 0 && gk < 1 ? 1 : 0;
    glint.style.transform = `translateX(${(150 + gk * 700).toFixed(1)}px) skewX(-20deg)`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8a — "วันนี้ ลองโทรหาพ่อสักครั้ง": the son calls
// =====================================================================
(() => {
  const [A, B] = SC.s8a;
  const S = new Shot(A, B, [['far', 0.35, 1.2], ['mid', 1, 0], ['fore', 1.9, 13]]);
  S.grade = 'saturate(1.08) contrast(1.04) sepia(0.05)';
  const set = sonRoomNight(S, 1);
  const M = S.L.mid;
  const L = t => t - A;
  const son = new Puppet(M.s, SON, M.defs);
  const ph = phoneProp(son.prop);
  const scr = callScreen(S.ui, 560, 96);
  const tTap = L(P.D1) + 0.35, tEar = L(P.D1) + 1.3;
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-20, 10, k), y: 0, z: lerp(1.2, 1.28, k), fx: 430, fy: 1000 });
    set.update(lt + 6);
    const ear = ease.inOutSine(prog(lt, tEar, tEar + 0.5));
    const pose = { x: 352, y: 1162, s: SS, torso: lerp(6, 2, ear), head: lerp(18, 0, ear), aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 9, smile: lerp(0.35, 0.7, ear) };
    const [ex, ey] = earWorld(pose);
    pose.armF = lerp(1, 0.85, ear);
    const toEarF = son.reach(pose, ex + 8, ey + 16, true);
    pose.aF = [lerp(76, toEarF[0], ear), lerp(-46, toEarF[1], ear)];
    pose.propRot = lerp(0, -20, ear);
    son.pose(pose);
    ph.scr.setAttribute('fill', '#bfe8c9');
    scr.update(lt, L(P.D0) - 0.15, tTap);
    scr.el.style.opacity = (parseFloat(scr.el.style.opacity) * (1 - prog(lt, tEar + 0.2, tEar + 0.5))).toFixed(3);
    const inK = 1 - prog(lt, 0, 0.35);
    const out = whip(S, lt, 'out');
    setGrade(S, inK * 8 + out * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8b — Dad's old phone rings: ลูก ❤ — he picks up
// =====================================================================
(() => {
  const [A, B] = SC.s8b;
  const S = new Shot(A, B, [['far', 0.4, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) sepia(0.06) contrast(1.04)';
  const room = dadRoom(S, true);
  const M = S.L.mid;
  const L = t => t - A;
  const dad = new Puppet(room.people, DAD_HOME, M.defs);
  const held = phoneProp(dad.prop, true);
  const benchPh = svg('g', {}, room.people);
  svg('rect', { x: -13, y: -50, width: 26, height: 52, rx: 7, fill: '#4a4d57', transform: 'rotate(90)' }, benchPh);
  const benchScr = svg('rect', { x: -9, y: -45, width: 18, height: 16, rx: 2, fill: '#c8f0c0', transform: 'rotate(90)' }, benchPh);
  const vib = svg('g', {}, room.people);
  for (const sx of [-1, 1]) for (let k = 0; k < 2; k++) svg('path', { d: `M${sx * (36 + k * 14)},-22 Q${sx * (46 + k * 14)},0 ${sx * (36 + k * 14)},22`, fill: 'none', stroke: '#fff', 'stroke-width': 4, 'stroke-linecap': 'round' }, vib);
  const inc = html('div', 'incoming', S.ui); inc.style.top = '150px';
  inc.innerHTML = `<div class="iav"><svg width="120" height="120" viewBox="-48 -48 96 96"><circle r="48" fill="#cfe9e6"/></svg></div><div class="itx"><b>ลูก ❤</b><small>กำลังโทรเข้า…</small></div><div class="ibtn" style="background:#2f9e5b"><svg width="44" height="44" viewBox="0 0 24 24"><path d="M6,3 L10,3 L11,8 L8.5,9.5 Q10,13.5 14.5,15.5 L16,13 L21,14 L21,18 Q21,21 18,21 Q4,20 3,6 Q3,3 6,3 Z" fill="#fff"/></svg></div>`;
  faceFront2(inc.querySelector('.iav svg'), 0, 8, 30, 'son');
  const ibtn = inc.querySelector('.ibtn');
  const fxs = fxSvg(S);
  const hearts = heartsRise(fxs, 560, 900, L(P.D3) + 0.2, 8, 41, 0.3);
  const tSee = L(P.D2) + 0.15, tGrab = L(P.D2) + 0.9, tEar = L(P.D3) - 0.1;
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(0, 20, k), y: 60, z: lerp(1.3, 1.4, k), fx: 600, fy: 1050 });
    room.update(lt + 4);
    const ringing = lt < tGrab;
    const see = ease.inOutSine(prog(lt, tSee, tSee + 0.35));
    const grab = ease.inOutSine(prog(lt, tGrab - 0.3, tGrab));
    const ear = ease.inOutSine(prog(lt, tGrab, tEar));
    const pose = { x: 560, y: 1244, s: DS, f: -1, torso: lerp(10, 4, see), head: lerp(20, -4, see), lF: [-2, 90], lB: [0, 91], t: lt + 5, smile: lerp(0.15, 1, Math.max(see * 0.6, ear)), aB: [62, 12] };
    const benchX = 700, benchY = 1238;
    const [ex, ey] = earWorld(pose);
    const toBench = dad.reach(pose, benchX, benchY - 10);
    pose.armF = lerp(1, 0.85, ear);
    const toEar = dad.reach(pose, ex - 8, ey + 16, true);
    const restA = [100, 70];
    pose.aF = ear > 0 ? [lerp(toBench[0], toEar[0], ear), lerp(toBench[1], toEar[1], ear)] : [lerp(restA[0], toBench[0], grab), lerp(restA[1], toBench[1], grab)];
    pose.propRot = lerp(-90, -20, ear);
    dad.pose(pose);
    held.g.setAttribute('opacity', lt >= tGrab ? 1 : 0);
    held.scr.setAttribute('fill', '#c8f0c0');
    const jit = ringing ? Math.sin(lt * 90) * 3 : 0;
    benchPh.setAttribute('transform', `translate(${(benchX + jit).toFixed(1)},${benchY})`);
    benchPh.setAttribute('opacity', lt < tGrab ? 1 : 0);
    benchScr.setAttribute('fill', Math.sin(lt * 10) > 0 ? '#e6ffe0' : '#c8f0c0');
    vib.setAttribute('transform', `translate(${benchX},${benchY - 4})`);
    vib.setAttribute('opacity', ringing ? (0.55 + 0.45 * Math.sin(lt * 40)).toFixed(2) : 0);
    const kk = spring(lt, 0.15, 13, 6);
    inc.style.opacity = (fadeIn(lt, 0.15, 0.12) * (1 - prog(lt, tEar, tEar + 0.4))).toFixed(3);
    inc.style.transform = `translateY(${((1 - kk) * -200).toFixed(1)}px) rotateX(${((1 - kk) * 25).toFixed(2)}deg) translateX(${ringing ? (Math.sin(lt * 50) * 4).toFixed(1) : 0}px)`;
    ibtn.style.transform = `scale(${(1 + 0.12 * Math.max(0, Math.sin(lt * 8))).toFixed(3)})`;
    hearts(lt);
    const inK = whip(S, lt, 'in');
    setGrade(S, inK * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8c — split screen: son above, Dad below, a voice wave between them; gift ≠ money
// =====================================================================
(() => {
  const [A, B] = SC.s8c;
  const S = new Shot(A, B, [['top', 1, 0], ['bot', 1, 0]]);
  S.grade = 'saturate(1.08) contrast(1.03)';
  const L = t => t - A;
  const T = S.L.top, D = S.L.bot;
  T.el.style.clipPath = 'inset(0 0 50% 0)'; D.el.style.clipPath = 'inset(50% 0 0 0)';
  // top: son's room
  svg('rect', { x: -100, y: -100, width: 1280, height: 1100, fill: lin(T.defs, [[0, '#3f3a5a'], [1, '#5a4e70']]) }, T.s);
  svg('rect', { x: 600, y: 110, width: 360, height: 420, rx: 8, fill: '#2a2236' }, T.s);
  svg('rect', { x: 614, y: 124, width: 332, height: 392, fill: lin(T.defs, [[0, '#141636'], [1, '#2b2c5a']]) }, T.s);
  svg('circle', { cx: 860, cy: 210, r: 26, fill: '#f6eed8' }, T.s);
  floorLamp(T.s, T.defs, 120, 960, '#ffcf8a', 0.7);
  sofa(T.s, T.defs, 260, 780, 520, -6);
  const son = new Puppet(T.s, SON, T.defs); const sph = phoneProp(son.prop);
  // bottom: Dad's room
  const tones = ['#7f5a3e', '#755236', '#866044', '#7b583b'];
  for (let i = 0; i < 14; i++) svg('rect', { x: i * 84, y: 960, width: 84, height: 960, fill: tones[i % 4] }, D.s);
  svg('circle', { cx: 760, cy: 1150, r: 520, fill: rad2(D.defs, [[0, '#ffd9a0', 0.45], [1, '#ffd9a0', 0]]) }, D.s);
  svg('rect', { x: 80, y: 1330, width: 200, height: 245, rx: 8, fill: '#3a2a1e' }, D.s);
  svg('rect', { x: 94, y: 1344, width: 172, height: 217, fill: lin(D.defs, [[0, '#c7d4e2'], [1, '#a9bccf']]) }, D.s);
  svg('path', { d: 'M118,1561 C120,1496 240,1496 242,1561 Z', fill: '#1d1d24' }, D.s);
  faceFront2(D.s, 180, 1462, 36, 'son');
  svg('path', { d: 'M130,1416 L180,1396 L230,1416 L180,1434 Z', fill: '#1d1d24' }, D.s);
  svg('rect', { x: 0, y: 1890, width: 1080, height: 100, fill: '#4d3220' }, D.s);
  for (const lx of [440, 1000]) svg('rect', { x: lx, y: 1730, width: 16, height: 162, fill: '#8a6a3a' }, D.s);
  svg('rect', { x: 420, y: 1712, width: 640, height: 22, rx: 8, fill: '#c9a46a' }, D.s);
  const dad = new Puppet(D.s, DAD_HOME, D.defs); const dph = phoneProp(dad.prop, true);
  // divider + voice wave
  const fxs = fxSvg(S);
  svg('rect', { x: 0, y: 954, width: 1080, height: 12, fill: '#ffd66b' }, fxs);
  const wave = svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 6, 'stroke-linecap': 'round', opacity: 0.9 }, fxs);
  const wave2 = svg('path', { fill: 'none', stroke: '#ffd66b', 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.8 }, fxs);
  const gift = giftVsMoney(S.ui, 250, 830);
  S.update = lt => {
    const sp = { x: 470, y: 774, s: 1.0, f: 1, torso: 2, head: 2 + Math.sin(lt * 2) * 2, aB: [80, -40], lF: [-2, 90], lB: [0, 91], t: lt + 3, smile: 0.85, grin: 0.4 };
    sp.armF = 0.85; const [sx, sy] = earWorld(sp); sp.aF = son.reach(sp, sx + 8, sy + 16, true); sp.propRot = -20;
    son.pose(sp);
    const dp = { x: 660, y: 1706, s: 1.15, f: -1, armF: 0.85, torso: 4, head: -2 + Math.sin(lt * 2.4) * 2, lF: [-2, 90], lB: [0, 91], aB: [62, 12], t: lt + 7, smile: 1, grin: 0.6 };
    const [dx, dy] = earWorld(dp); dp.aF = dad.reach(dp, dx - 8, dy + 16, true); dp.propRot = -20;
    dad.pose(dp);
    sph.scr.setAttribute('fill', '#bfe8c9'); dph.scr.setAttribute('fill', '#c8f0c0');
    let d1 = '', d2 = '';
    for (let x = 0; x <= 1080; x += 12) {
      const env = Math.sin(Math.PI * x / 1080);
      const y1 = 960 + Math.sin(x * 0.045 - lt * 9) * 34 * env * (0.6 + 0.4 * Math.sin(lt * 3));
      const y2 = 960 + Math.sin(x * 0.03 + lt * 7) * 22 * env;
      d1 += (x ? ' L' : 'M') + x + ',' + y1.toFixed(1); d2 += (x ? ' L' : 'M') + x + ',' + y2.toFixed(1);
    }
    wave.setAttribute('d', d1); wave2.setAttribute('d', d2);
    gift.update(lt, L(P.D4) + 0.05, L(P.D5) + 0.35);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8d — close on Dad: "พ่อเหนื่อยไหม" — a tear, a smile
// =====================================================================
(() => {
  const [A, B] = SC.s8d;
  const S = new Shot(A, B, [['far', 0.4, 2.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.1) sepia(0.06) contrast(1.04)';
  const room = dadRoom(S, true);
  const M = S.L.mid;
  const L = t => t - A;
  const dad = new Puppet(room.people, DAD_HOME, M.defs);
  const ph = phoneProp(dad.prop, true);
  const fxs = fxSvg(S);
  const leak = lightLeak(S.fx);
  const tear = svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#cfe8ff', opacity: 0 }, fxs);
  const glint = svg('path', { d: 'M0,-14 L3,-3 L14,0 L3,3 L0,14 L-3,3 L-14,0 L-3,-3 Z', fill: '#fff', opacity: 0 }, fxs);
  const hearts = heartsRise(fxs, 600, 900, L(P.D7) + 0.3, 10, 57, 0.28);
  const bub = speechBubble(S.ui, 400, 540, 'พ่อเหนื่อยไหม');
  const tQ = L(P.D7);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(40, 60, k), y: lerp(170, 190, k), z: lerp(1.9, 2.1, k), fx: 560, fy: 1000 });
    room.update(lt + 7);
    const moved = ease.inOutSine(prog(lt, tQ + 0.1, tQ + 0.6));
    const pose = { x: 560, y: 1244, s: DS, f: -1, torso: lerp(4, 8, moved), head: lerp(-4, 8, moved), lF: [-2, 90], lB: [0, 91], aB: [62, 12], armF: 0.85, t: lt + 8, smile: lerp(0.7, 1, moved), eyes: moved > 0.5 ? 0 : null };
    const [ex, ey] = earWorld(pose); pose.aF = dad.reach(pose, ex - 8, ey + 16, true); pose.propRot = -20;
    dad.pose(pose);
    ph.scr.setAttribute('fill', '#c8f0c0');
    const [gx, gy] = rectCenter(dad.eyeG);
    const tg = prog(lt, tQ - 0.6, tQ + 0.3);
    glint.setAttribute('opacity', (Math.sin(Math.PI * tg) * 0.95).toFixed(3));
    glint.setAttribute('transform', `translate(${gx.toFixed(1)},${gy.toFixed(1)}) rotate(${(lt * 90).toFixed(1)}) scale(${(0.9 + 0.6 * Math.sin(Math.PI * tg)).toFixed(3)})`);
    const td = prog(lt, tQ + 0.2, tQ + 1.4);
    tear.setAttribute('opacity', td > 0 && td < 1 ? (0.95 * (1 - td * 0.5)).toFixed(3) : 0);
    tear.setAttribute('transform', `translate(${(gx - 4).toFixed(1)},${(gy + 18 + 70 * ease.inCubic(td)).toFixed(1)}) scale(1.6)`);
    bub.update(lt, L(P.D6) - 0.05, tQ);
    hearts(lt);
    leak(lt, 0.25 + 0.5 * moved);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S9 — end card: ringing old phone, title, "โทรหาพ่อวันนี้ อย่าให้สาย", CTA
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#5a3550'], [0.6, '#2c1c33'], [1, '#170f1d']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 143, { color: '#ffd9a0', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const fxs = fxSvg(S);
  const rings = Array.from({ length: 3 }, () => svg('circle', { cx: 540, cy: 560, r: 90, fill: 'none', stroke: '#6fe08f', 'stroke-width': 5 }, fxs));
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const icon = html('div', 'title', wrap); icon.style.top = '420px';
  icon.innerHTML = oldPhoneSVG(130, 250, true, 'ลูก ❤');
  const t1 = html('div', 'title', wrap); t1.style.top = '720px'; t1.style.font = '700 170px/1 Kanit';
  const digits = ['7', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'วัน'); unit.style.marginLeft = '0.28em';
  const t2 = html('div', 'title', wrap, 'ของพ่อ'); t2.style.top = '905px'; t2.style.font = '600 120px/1 Kanit';
  const sub = html('div', 'title', wrap, 'โทรหาพ่อวันนี้ อย่าให้สาย'); sub.style.top = '1080px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffd166';
  const cta = html('div', 'cta', wrap); cta.style.top = '1200px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ยังไม่ได้โทรหาพ่อ</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  const spark = burst(fxs, 540, 560, 0.3, 18, 153, ['#ffd66b', '#ffffff', '#6fe08f'], 240, 0.9);
  S.update = lt => {
    bok(lt); leak(lt, 0.45);
    popSquash(icon, lt, 0.15, `rotate(${(Math.sin(lt * 40) * 4 * (lt < 1.6 ? 1 : 0.3)).toFixed(2)}deg)`, -20);
    rings.forEach((rg, i) => { const k = ((lt - 0.3 + i * 0.5) % 1.5 + 1.5) % 1.5 / 1.5; setA(rg, { r: (110 + k * 170).toFixed(1), opacity: (lt > 0.3 ? (1 - k) * 0.5 : 0).toFixed(3) }); });
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.1, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.65, 14, 7); unit.style.opacity = fadeIn(lt, 0.65, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.75, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.75, 1.2))) * 100).toFixed(1)}% -40% 0)`;
    const ks = spring(lt, 1.1, 14, 7); sub.style.opacity = fadeIn(lt, 1.1, 0.15); sub.style.transform = `translateY(${((1 - ks) * 24).toFixed(1)}px)`;
    enter3d(cta, lt, 1.4, 'pop');
    cta.style.boxShadow = `0 0 ${(24 + 18 * Math.sin(lt * 4)).toFixed(1)}px rgba(224,87,122,.65), 0 16px 34px rgba(0,0,0,.4)`;
    plane.update(lt);
  };
  SHOTS.push(S);
})();

// global overlays
const grainTick = makeGrain();
const black = html('div', 'blackout', frame);
const flash = html('div', 'blackout', frame); flash.style.background = '#fffbe8';
const warm = html('div', 'blackout', frame); warm.style.background = '#fff1dc';
window.render = t => {
  for (const sh of SHOTS) {
    const next = SHOTS[SHOTS.indexOf(sh) + 1];
    const until = next && next.fadeIn ? Math.max(sh.b, next.a + next.fadeIn) : sh.b;
    const on = t >= sh.a && t < until;
    sh.root.style.display = on ? 'block' : 'none';
    if (on) { if (sh.fadeIn) sh.root.style.opacity = prog(t, sh.a, sh.a + sh.fadeIn).toFixed(3); sh.update(t - sh.a); }
  }
  renderKinetic2(subsBox, CUES, t);
  grainTick(t);
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, DURATION - 0.45, DURATION)).toFixed(3);
  flash.style.opacity = (0.85 * prog(t, SC.s2[0] - 0.12, SC.s2[0]) * (1 - prog(t, SC.s2[0], SC.s2[0] + 0.35))).toFixed(3);
  const w1 = prog(t, SC.s7[1] - 0.35, SC.s7[1]) * (1 - prog(t, SC.s7[1], SC.s7[1] + 0.4));
  const w2 = prog(t, P.end - 0.35, P.end) * (1 - prog(t, P.end, P.end + 0.45));
  warm.style.opacity = (0.92 * Math.max(w1, w2)).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
