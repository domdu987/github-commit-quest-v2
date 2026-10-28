// "127 ใบสมัคร" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D8; H is the "ถ้า..." hook).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.B2 - 0.35], s3: [P.B2 - 0.35, P.B4 - 0.1], s4: [P.B4 - 0.1, P.Cst - 0.3], s5: [P.Cst - 0.3, P.C4 - 0.1],
  s6: [P.C4 - 0.1, P.C8 - 0.15], s7: [P.C8 - 0.15, P.title], s8: [P.title, P.D0 - 0.1], s9: [P.D0 - 0.1, P.D4 - 0.15], s10: [P.D4 - 0.15, P.end], s11: [P.end, DURATION] };
const SUB_TOP = [[SC.s4[0], SC.s4[1], 1790], [SC.s7[0], SC.s7[1], 1790]];
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: (SUB_TOP.find(([a, b]) => c.a >= a - 0.3 && c.a < b) || [0, 0, 1640])[2] }));

const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);
function cardEl(parent, cls, x, y, w) {
  const c = html('div', cls, parent);
  c.style.left = x + 'px'; c.style.top = y + 'px'; if (w) c.style.width = w + 'px';
  const sh = html('div', 'shine', c);
  return { c, sh };
}
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function earWorld(p) { return toWorld(p, ...torsoPt(p, EAR_L[0], EAR_L[1])); }
function phoneProp(parent, case_ = '#2a2b36') {
  const g = svg('g', {}, parent);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: case_, stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, g);
  return { g, scr };
}
const rectCenter = el => { const r = el.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2, r.width]; };
function holdPhone(pup, pose, fx = 78, fy = -RIG.T + 36, tap = 0) {
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, fx, fy));
  pose.aB = pup.reach(pose, tx - 6, ty + 8);
  pose.aF = pup.reach(pose, tx + 6, ty - 2 + tap * 9);
  pose.propRot = -12;
  return [tx, ty];
}
function phoneAtEar(pup, pose, k = 1) {
  const a0 = pose.aF || [92, 92];
  pose.armF = lerp(1, 0.85, k);
  const [ex, ey] = earWorld(pose); const toE = pup.reach(pose, ex + 8, ey + 16, true);
  pose.aF = [lerp(a0[0], toE[0], k), lerp(a0[1], toE[1], k)];
  pose.propRot = -20;
}
function seamShot(A, B, color = 'linear-gradient(90deg,#ffd66b,#7fd6c7,#ffd66b)') {
  const seam = new Shot(A, B, []);
  const line = html('div', '', seam.ui); Object.assign(line.style, { position: 'absolute', left: 0, right: 0, top: '954px', height: '12px', background: color, boxShadow: '0 0 24px rgba(255,214,107,.8)' });
  seam.update = lt => { line.style.opacity = (0.75 + 0.25 * Math.sin(lt * 5)).toFixed(3); };
  SHOTS.push(seam);
}

// him, cross-legged on the floor behind the low table
const SEAT = { x: 340, y: 1392, s: 1.15 };
function seatPose(pup, lt, o = {}) {
  const pose = Object.assign({ x: SEAT.x, y: SEAT.y, s: SEAT.s, f: 1, torso: 8, head: 10, lF: [4, 176], lB: [16, 168], t: lt + 1, smile: 0.4 }, o);
  let ph = null;
  if (o.type) {
    const k = Math.sin(lt * 17), k2 = Math.sin(lt * 13 + 1);
    pose.aF = pup.reach(pose, 492 + k * 8, 1318 - Math.max(0, k) * 10);
    pose.aB = pup.reach(pose, 462 + k2 * 8, 1320 - Math.max(0, k2) * 10);
  } else if (o.slump) {
    pose.torso = lerp(pose.torso, 38, o.slump); pose.head = lerp(pose.head, 26, o.slump);
    pose.aF = pup.reach(pose, lerp(492, 470, o.slump), lerp(1318, 1314, o.slump));
    pose.aB = pup.reach(pose, lerp(462, 440, o.slump), 1318);
  } else if (o.phone) ph = holdPhone(pup, pose, o.px || 74, o.py || -RIG.T + 44, o.tap || 0);
  else { pose.aF = pup.reach(pose, 492, 1318); pose.aB = pup.reach(pose, 462, 1320); }   // idle: hands rest on the keyboard, not through the desk
  pup.pose(pose);
  return { pose, ph };
}
// mom, sitting folded on her reed mat, facing left
const MOMP = { x: 600, y: 1432, s: 1.2 };
function momPose(pup, lt, o = {}) {
  const pose = Object.assign({ x: MOMP.x, y: MOMP.y, s: MOMP.s, f: -1, torso: 6, head: 8, lF: [8, 172], lB: [18, 166], t: lt + 5, smile: 0.5 }, o);
  holdPhone(pup, pose, 70, -RIG.T + 46, o.tap || 0);
  if (o.ear) phoneAtEar(pup, pose, o.ear);
  pup.pose(pose);
  return pose;
}

// =====================================================================
// S0 — hook: "ถ้าหางานไม่ได้ แล้วคุณบอกแม่ว่าสบายดี ถ้าวันหนึ่งแม่รู้ความจริง เขาจะทำยังไง"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, [['far', 0.4, 10], ['mid', 1, 10]]);
  const room = rentRoom(S, 'night'), L = t => t - A;
  S.L.far.el.style.filter = 'blur(10px) brightness(0.55) saturate(1.1)'; S.L.mid.el.style.filter = 'blur(10px) brightness(0.55) saturate(1.1)';
  const fxs = fxSvg(S);
  const bok = floaters(fxs, [0, 200, 1080, 1400], 14, 71, { color: '#ffd9a8', rMin: 12, rMax: 36, speed: 10, op: 0.2, base: 0.05, amp: 20 });
  const minis = [0, 1, 2].map(i => mailCard(S.ui, 150 + i * 30, 330 + i * 150, 780, false, COMPANIES[i + 1], 'ผลการสมัครงาน', [['ขอบคุณที่สนใจ แต่เสียใจด้วย', null]]));
  const chat = chatPhone(S.ui, 290, 250, 500, 900, 'แม่', momAv());
  chat.add('text', 'L', -1, { text: 'เป็นไงบ้างลูก งานได้ยัง', meta: '20:14' });
  chat.add('text', 'R', L(P.H3) - 0.1, { text: 'สบายดีครับแม่ ใกล้ได้แล้ว', meta: 'อ่านแล้ว', read: L(P.H4) + 0.3 });
  const inp = chatInput(chat);
  const spot = html('div', 'spot', S.ui);
  const momB = html('div', 'title', S.ui); momB.style.top = '330px'; momB.innerHTML = portrait5('mom', 320, '#ffe9c4', { smile: 0.35 });
  const msvg = momB.querySelector('svg'); msvg.style.borderRadius = '50%'; msvg.style.boxShadow = '0 0 0 10px #fff, 0 30px 60px rgba(0,0,0,.5)';
  const qw = html('div', 'qwrap', S.ui); qw.style.left = '700px'; qw.style.top = '300px'; html('div', 'qmark', qw, '?');
  const rip = ripples(fxs, 540, 500, 170, '#ffe2a8', 3, 1.4);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.14, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    room.update(lt); bok(lt);
    const out1 = ease.inCubic(prog(lt, L(P.H1) - 0.25, L(P.H1) + 0.05));
    minis.forEach((m, i) => {
      m.update(lt, L(P.H0) + 0.05 + i * 0.16, [99], L(P.H0) + 0.3 + i * 0.16);
      m.el.style.opacity = (fadeIn(lt, L(P.H0) + 0.05 + i * 0.16, 0.12) * (1 - out1)).toFixed(3);
      m.el.style.transform += ` translateX(${(-out1 * 700).toFixed(1)}px) rotate(${(-6 + i * 5).toFixed(1)}deg)`;
    });
    const out2 = ease.inCubic(prog(lt, L(P.H4) - 0.3, L(P.H4)));
    enter3d(chat.el, lt, L(P.H1) - 0.1, 'pop');
    chat.el.style.opacity = (fadeIn(lt, L(P.H1) - 0.1, 0.12) * (1 - out2)).toFixed(3);
    chat.el.style.transform += ` translateX(${(out2 * 800).toFixed(1)}px)`;
    chat.update(lt);
    inp.update(lt, [{ t0: L(P.H1) + 0.1, t1: L(P.H3) - 0.25, text: 'สบายดีครับแม่ ใกล้ได้แล้ว', mode: 'type' }, { t0: L(P.H3) - 0.15, t1: L(P.H3) - 0.1, text: '', mode: 'hold' }]);
    spot.style.opacity = (0.9 * prog(lt, L(P.H4) - 0.1, L(P.H4) + 0.3)).toFixed(3);
    popSquash(momB, lt, L(P.H4) + 0.05, '', -12); momB.style.opacity = fadeIn(lt, L(P.H4) + 0.05, 0.12);
    popSquash(qw, lt, L(P.H6) - 0.05, `rotate(${(Math.sin(lt * 5) * 8).toFixed(1)}deg)`, 20); qw.style.opacity = fadeIn(lt, L(P.H6) - 0.05, 0.1);
    rip(lt, prog(lt, L(P.H5), L(P.H5) + 0.3));
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — night, 8 months after graduating: rejection mails pile up to 127, then "ขอบคุณที่สนใจ แต่เสียใจด้วย"
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = rentRoom(S, 'night'), L = t => t - A;
  const me = new Puppet(set.people, GRAD_HOME, S.L.mid.defs);
  const months = monthsChip(S.ui, 56, 96);
  const counter = appCounter(S.ui, 560, 96);
  const inbox = inboxCard(S.ui, 110, 230, 860, 700);
  const times = Array.from({ length: 13 }, (_, i) => i < 4 ? L(P.A1) + 0.05 + i * 0.22 : L(P.A2) + (i - 4) * 0.11);
  const mail = mailCard(S.ui, 90, 300, 900, false, COMPANIES[0], 'ผลการพิจารณาใบสมัครงาน',
    [['เรียน ผู้สมัครทุกท่าน', null], ['ขอบคุณที่สนใจร่วมงานกับเรา', '#ffe27a'], ['แต่เสียใจด้วย ตำแหน่งนี้ได้ผู้สมัครแล้ว', '#ffc2bd']]);
  const fxs = fxSvg(S);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-10, 10, k), y: -60, z: lerp(1.28, 1.34, k), fx: 420, fy: 1250 });
    set.update(lt);
    const slump = ease.inOutSine(prog(lt, L(P.A5) + 0.25, L(P.A5) + 0.7));
    const typing = lt > L(P.A1) - 0.2 && lt < L(P.A3) + 0.3;
    seatPose(me, lt, { type: typing && !slump, slump: slump || null, smile: lerp(lt < L(P.A3) ? 0.45 : 0.15, 0.05, slump), eyes: slump > 0.6 ? 0 : null });
    months.update(lt, L(P.A0) - 0.05, L(P.A1) - 0.1);
    const n = times.filter(tt => lt >= tt).length;
    const roll = rollValue(lt, L(P.A2) - 0.05, L(P.A2) + 0.95, 4, 127);
    const v = lt < L(P.A2) - 0.05 ? n : roll.v;
    counter.update(lt, L(P.A1) - 0.05, v, lt < L(P.A2) - 0.05 ? 0 : roll.speed, times.slice(0, 4));
    const out = ease.inCubic(prog(lt, L(P.A4) - 0.35, L(P.A4) - 0.05));
    inbox.update(lt, L(P.A1) - 0.15, times, v);
    if (out > 0) { inbox.el.style.opacity = (1 - out).toFixed(3); inbox.el.style.filter = `blur(${(out * 10).toFixed(1)}px)`; } else inbox.el.style.filter = 'none';
    mail.update(lt, L(P.A4) - 0.2, [99, L(P.A4) + 0.05, L(P.A5)], L(P.A5) + 0.45);
    mail.el.style.display = lt > L(P.A4) - 0.25 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — morning: shirt and tie on, rent 3,500, rice 50 a meal
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) contrast(1.03) brightness(1.03)';
  const set = rentRoom(S, 'day'), L = t => t - A;
  const fold = folderProp(set.people);
  const me = new Puppet(set.people, GRAD, S.L.mid.defs);
  const c1 = costChip(S.ui, 70, 330, 'house', 'ค่าห้อง', '3,500', '/เดือน');
  const c2 = costChip(S.ui, 470, 470, 'rice', 'ข้าว', '50', '/มื้อ');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(20, 0, k), y: lerp(40, 20, k), z: lerp(1.42, 1.5, k), fx: 460, fy: 1150 });
    set.update(lt + 2);
    const pose = { x: 430, y: 1196, s: 1.15, f: 1, torso: 2, head: lerp(-4, 6, prog(lt, 0.8, 1.2)), lF: [88, 90], lB: [92, 92], t: lt + 3, smile: 0.55 };
    const wig = Math.sin(lt * 11) * 5;
    const [nx, ny] = toWorld(pose, ...torsoPt(pose, 20, -RIG.T + 14));
    pose.aF = me.reach(pose, nx + 10 + wig, ny + 6);
    pose.aB = [100, 84];
    me.pose(pose);
    const [wx, wy] = toWorld(pose, ...me.wristB);
    fold.setAttribute('transform', `translate(${wx.toFixed(1)},${(wy + 30).toFixed(1)}) rotate(-6) scale(1.15)`);
    c1.update(lt, L(P.B0) - 0.05); c2.update(lt, L(P.B1) - 0.05);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — squeezed in the morning skytrain on the way to another interview
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.25, 3], ['mid', 1, 0], ['fore', 1.6, 14]]);
  S.grade = 'saturate(1.05) contrast(1.04)';
  const set = skytrain(S), L = t => t - A;
  const me = new Puppet(set.people, GRAD, S.L.mid.defs);
  const fold = folderProp(me.prop);
  const pill = html('div', 'pill', S.ui); pill.style.left = '250px'; pill.style.top = '120px';
  pill.innerHTML = '<span class="icslot"></span><span>สัมภาษณ์งาน <b>09:00</b></span>';
  const clk = clockMoon(pill.querySelector('.icslot'), 54, false);
  const fxs = fxSvg(S);
  const sweat = Array.from({ length: 3 }, () => svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#bfe9ff', stroke: '#fff', 'stroke-width': 1.5, opacity: 0 }, fxs));
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    const shake = Math.sin(lt * 31) * 2;
    S.cam({ x: 0 + shake, y: lerp(120, 150, k), z: lerp(1.3, 1.38, k), fx: 540, fy: 1000 });
    set.update(lt + 4);
    const sw = set.sway(lt + 4);
    const pose = { x: 540 + sw * 0.6, y: 1335, s: 1.2, f: 1, torso: sw * 0.5, head: 4 + Math.sin(lt * 3) * 3, lF: [90, 90], lB: [90, 92], t: lt + 1, smile: 0.12 };
    pose.aB = me.reach(pose, 540 - 30, 392, true);
    const [fx, fy] = toWorld(pose, ...torsoPt(pose, 46, -RIG.T + 56));
    pose.aF = me.reach(pose, fx, fy); pose.propRot = -10;
    me.pose(pose);
    fold.setAttribute('transform', 'translate(-6,-20) rotate(-80) scale(1.2)');
    popSquash(pill, lt, 0.1); clk.update(lt, 8, 40 + lt * 6);
    const [hx, hy] = rectCenter(me.head);
    sweat.forEach((s, i) => { const q = ((lt * 0.9 + i * 0.33) % 1); setA(s, { opacity: (1 - q).toFixed(2), transform: `translate(${(hx + 70 + i * 16).toFixed(1)},${(hy - 70 + q * 70).toFixed(1)}) scale(2.2)` }); });
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — split, night: he calls home from the balcony ("สบายดีครับ"); mom listens in her wooden house
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const L = t => t - A;
  const top = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  top.root.style.clipPath = 'inset(0 0 50% 0)'; top.grade = 'saturate(1.08) contrast(1.04)';
  const bset = balconyNight(top);
  const me = new Puppet(bset.people, GRAD, top.L.mid.defs); const ph = phoneProp(me.prop);
  const bub = html('div', 'bubble2', top.ui); bub.style.left = '520px'; bub.style.top = '210px'; bub.textContent = 'สบายดีครับ!';
  top.update = lt => {
    top.cam({ x: 0, y: 360, z: 1.1, fx: 420, fy: 1000 });
    bset.update(lt + 6);
    const fake = lt > L(P.B6) - 0.1 && lt < L(P.B7) + 0.6;
    const pose = { x: 420, y: 1102, s: 1.2, f: 1, torso: 4, head: fake ? -2 : 8, lF: [90, 90], lB: [88, 92], t: lt + 2, smile: fake ? 1 : (lt > L(P.B7) + 0.6 ? 0.08 : 0.3), grin: fake ? 1 : 0, aB: [80, 40] };
    holdPhone(me, pose, 60, -RIG.T + 40);
    phoneAtEar(me, pose, ease.inOutSine(prog(lt, 0, 0.35)));
    pose.aB = [70, 10];
    me.pose(pose);
    popSquash(bub, lt, L(P.B6) - 0.05, '', -10);
    bub.style.opacity = (fadeIn(lt, L(P.B6) - 0.05, 0.1) * (1 - prog(lt, L(P.B7) + 0.9, L(P.B7) + 1.1))).toFixed(3);
    setGrade(top, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(top);
  const bot = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  bot.root.style.clipPath = 'inset(50% 0 0 0)'; bot.grade = 'saturate(1.05) contrast(1.03)';
  const hset = momHome(bot);
  const mom = new Puppet(hset.people, MOM5, bot.L.mid.defs); phoneProp(mom.prop, '#c4566f');
  bot.update = lt => {
    bot.cam({ x: 0, y: -150, z: 1.1, fx: 540, fy: 1000 });
    hset.update(lt + 3, 20.75);
    const listen = lt > L(P.B6);
    momPose(mom, lt, { ear: ease.inOutSine(prog(lt, 0, 0.35)), smile: listen ? 0.2 : 0.55, head: listen ? 14 : 6, eyes: null });
    hset.photoGlow.setAttribute('opacity', (0.6 + 0.4 * prog(lt, L(P.B6), L(P.B7) + 0.5)).toFixed(3));
    setGrade(bot, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(bot);
  seamShot(A, B);
})();

// =====================================================================
// S5 — dark room: 210 baht left; he opens a bus booking home; his finger hangs over "ยืนยัน"
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(0.95) contrast(1.06)';
  const set = rentRoom(S, 'dark'), L = t => t - A;
  const me = new Puppet(set.people, GRAD_HOME, S.L.mid.defs); const ph = phoneProp(me.prop);
  const bank = bankCard(S.ui, 150, 200, 780);
  const book = bookCard(S.ui, 150, 560, 780);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: 0, y: lerp(-60, -40, k), z: lerp(1.28, 1.34, k), fx: 420, fy: 1250 });
    set.update(lt + 9);
    const { ph: pp } = seatPose(me, lt, { phone: true, smile: 0.05, head: 16, torso: 12, tap: 0 });
    ph.scr.setAttribute('fill', '#cfe4ff');
    setA(set.pglow, { cx: pp[0].toFixed(1), cy: (pp[1] - 30).toFixed(1), opacity: 1 });
    bank.update(lt, L(P.C0) - 0.45, L(P.C0) - 0.2, L(P.C0) + 0.7);
    const up = ease.inOutCubic(prog(lt, L(P.C1) - 0.2, L(P.C1) + 0.2));
    bank.el.style.transform += ` translateY(${(-60 * up).toFixed(1)}px) scale(${(1 - 0.12 * up).toFixed(3)})`;
    book.update(lt, L(P.C1) - 0.1, L(P.C2) + 0.1, 99);
    book.el.style.display = lt > L(P.C1) - 0.15 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — mom's message pops up: she sent 2,000
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.0) contrast(1.05)';
  const set = rentRoom(S, 'dark'), L = t => t - A;
  const me = new Puppet(set.people, GRAD_HOME, S.L.mid.defs); const ph = phoneProp(me.prop);
  const book = bookCard(S.ui, 150, 560, 780);
  const ban = notifBanner(S.ui, 150, momAv(96), 'แม่', 'ส่งเงินให้คุณ <b style="color:#2f9e5b">฿2,000</b>');
  ban.el.querySelector('.app').textContent = 'แชท';
  const chat = chatPhone(S.ui, 560, 220, 470, 880, 'แม่', momAv());
  chat.add('text', 'L', -1, { text: 'กินข้าวยังลูก', meta: 'เมื่อวาน' });
  chat.add('text', 'R', -1, { text: 'กินแล้วครับ สบายดี', meta: 'อ่านแล้ว' });
  const slip = chat.add('custom', 'L', L(P.C5) + 0.05, { html: slipHTML('2,000') });
  const fxs = fxSvg(S);
  const spark = burst(fxs, 760, 760, L(P.C6), 16, 211, ['#9be38b', '#ffffff', '#ffd66b'], 220, 0.8);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(10, 25, k), y: lerp(20, 40, k), z: lerp(1.56, 1.64, k), fx: 380, fy: 1200 });
    set.update(lt + 14);
    const shock = lt > L(P.C6) - 0.1;
    const { ph: pp } = seatPose(me, lt, { phone: true, smile: shock ? 0.2 : 0.05, mouthO: shock ? 1 : 0, head: shock ? 4 : 16, torso: shock ? 2 : 12 });
    ph.scr.setAttribute('fill', '#e9f4ff');
    setA(set.pglow, { cx: pp[0].toFixed(1), cy: (pp[1] - 30).toFixed(1), opacity: 1 });
    book.update(lt, -1, -0.5, L(P.C4) - 0.1);
    book.el.style.display = lt < L(P.C4) + 0.4 ? 'block' : 'none';
    ban.update(lt, L(P.C4) + 0.05, L(P.C5) - 0.2);
    enter3d(chat.el, lt, L(P.C5) - 0.05, 'pop');
    chat.update(lt);
    const pk = Math.exp(-Math.pow((lt - L(P.C6) - 0.1) * 6, 2));
    slip.el.style.transform = `scale(${(1 + 0.12 * pk).toFixed(3)})`;
    spark(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — split: "แม่รู้นะว่ายังไม่ได้งาน ไม่ต้องรีบ กินข้าวให้อิ่มก่อน" — he cries and smiles; mom sends it with one finger
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const L = t => t - A;
  const top = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0]]);
  top.root.style.clipPath = 'inset(0 0 50% 0)'; top.grade = 'saturate(1.02) contrast(1.05)';
  const set = rentRoom(top, 'dark');
  const me = new Puppet(set.people, GRAD_HOME, top.L.mid.defs); const ph = phoneProp(me.prop);
  const chat = chatPhone(top.ui, 590, 70, 450, 830, 'แม่', momAv());
  chat.add('custom', 'L', -1, { html: slipHTML('2,000') });
  chat.add('text', 'L', L(P.C8) - 0.05, { text: 'แม่รู้นะว่ายังไม่ได้งาน' });
  chat.add('text', 'L', L(P.C9) - 0.05, { text: 'ไม่ต้องรีบ' });
  chat.add('text', 'L', L(P.C10) - 0.05, { text: 'กินข้าวให้อิ่มก่อนนะลูก' });
  const fxs = fxSvg(top);
  const cry = tears(fxs, 4);
  top.update = lt => {
    top.cam({ x: 18, y: 765, z: 1.5, fx: 380, fy: 1000 });
    set.update(lt + 19);
    const moved = lt > L(P.C8) + 0.3;
    const { ph: pp } = seatPose(me, lt, { phone: true, smile: moved ? 0.5 : 0.2, head: moved ? 18 : 12, torso: 10, eyes: moved ? 0 : null });
    ph.scr.setAttribute('fill', '#ffe9c4');
    setA(set.pglow, { cx: pp[0].toFixed(1), cy: (pp[1] - 30).toFixed(1), opacity: 1 });
    chat.update(lt);
    const [ex, ey] = rectCenter(me.eyeNear.g);
    cry(lt, moved ? L(P.C8) + 0.3 : 999, ex, ey + 12);
    setGrade(top, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(top);
  const bot = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  bot.root.style.clipPath = 'inset(50% 0 0 0)'; bot.grade = 'saturate(1.06) contrast(1.03)';
  const hset = momHome(bot);
  const mom = new Puppet(hset.people, MOM5, bot.L.mid.defs); const mph = phoneProp(mom.prop, '#c4566f');
  const fx2 = fxSvg(bot);
  const hearts = heartsRise(fx2, 820, 1540, L(P.C10), 8, 307, 0.3);   // rise beside her, never across her face
  bot.update = lt => {
    bot.cam({ x: 0, y: -150, z: 1.1, fx: 540, fy: 1000 });
    hset.update(lt + 6, 21.2);
    const typing = [P.C8, P.C9, P.C10].some(tc => lt > L(tc) - 0.6 && lt < L(tc) - 0.05);
    momPose(mom, lt, { smile: 0.75, head: typing ? 18 : 10, tap: typing ? Math.max(0, Math.sin(lt * 7)) : 0, eyes: typing ? 0.6 : null });
    mph.scr.setAttribute('fill', '#ffe9c4');
    hset.photoGlow.setAttribute('opacity', 1);
    hearts(lt);
    setGrade(bot, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(bot);
  seamShot(A, B, 'linear-gradient(90deg,#ffd66b,#ff9fc0,#ffd66b)');
})();

// =====================================================================
// S8 — title: 127 ใบสมัคร / ที่แม่รู้มาตลอด
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = momHome(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 93, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '420px';
  ic.innerHTML = `<svg width="220" height="210" viewBox="-60 -62 120 116"><path d="M-30,-44 L10,-44 L26,-28 L26,44 L-30,44 Z" fill="#ffffff" stroke="${INK}" stroke-width="5" stroke-linejoin="round" transform="rotate(-10)"/><path d="M-22,-40 L18,-40 L34,-24 L34,48 L-22,48 Z" fill="#f6f1e6" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M-12,-14 L22,-14 M-12,0 L22,0 M-12,14 L14,14" stroke="#9aa6b2" stroke-width="5" stroke-linecap="round"/><path d="${heartPathT(20, 30, 20)}" fill="#f04f7f" stroke="${INK}" stroke-width="4"/></svg>`;
  const t1 = html('div', 'title', wrap); t1.style.top = '650px'; t1.style.font = '700 200px/1 Kanit';
  const digits = ['1', '2', '7'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ใบสมัคร'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่แม่รู้มาตลอด'); t2.style.top = '880px'; t2.style.font = '600 108px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1040px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5); bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.42, 14, 7); unit.style.opacity = fadeIn(lt, 0.42, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S9 — three weeks later, morning: application #128 → "เริ่มงานวันจันทร์"; he jumps up
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.12) contrast(1.03) brightness(1.04)';
  const set = rentRoom(S, 'day'), L = t => t - A;
  const me = new Puppet(set.people, GRAD_HOME, S.L.mid.defs);
  const cal = monthsChip(S.ui, 56, 96); cal.el.innerHTML = ''; const cic = calendarFlip(cal.el, 62); html('span', '', cal.el).innerHTML = '<b>3</b> สัปดาห์ต่อมา';
  const counter = appCounter(S.ui, 500, 96);
  const ok = html('div', 'okstamp', S.ui); Object.assign(ok.style, { left: '960px', top: '84px', right: 'auto', bottom: 'auto' }); ok.innerHTML = '✓';
  const mail = mailCard(S.ui, 90, 300, 900, true, COMPANIES[7], 'ยินดีด้วย! คุณผ่านการคัดเลือก',
    [['ขอแสดงความยินดีกับคุณ', null], ['เริ่มงานวันจันทร์ เวลา 09:00 น.', '#bff0c8']]);
  const fxs = fxSvg(S);
  const confs = [[540, 560, 409], [220, 980, 411], [860, 1000, 413]].map(([cx, cy, sd]) => burst(fxs, cx, cy, L(P.D3) + 0.1, 28, sd, ['#ffd66b', '#7fd6c7', '#ff9fc0', '#ffffff', '#4a7bd8'], 360, 1.6));
  const conf = t => confs.forEach(c => c(t));
  const leak = lightLeak(S.fx);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(0, 10, k), y: -60, z: lerp(1.28, 1.34, k), fx: 420, fy: 1250 });
    set.update(lt + 21);
    const up = ease.outBack(prog(lt, L(P.D3) + 0.05, L(P.D3) + 0.35));
    if (up <= 0) seatPose(me, lt, { type: lt > L(P.D1) - 0.3 && lt < L(P.D2), smile: lt > L(P.D2) ? 0.8 : 0.4, mouthO: lt > L(P.D2) + 0.2 ? 1 : 0, head: 8 });
    else {
      const hop = Math.abs(Math.sin((lt - L(P.D3)) * 7)) * 34 * (1 - prog(lt, L(P.D3) + 1.2, L(P.D3) + 2.2));
      const pose = { x: lerp(SEAT.x, 236, Math.min(1, up)), y: lerp(SEAT.y, 1176, Math.min(1, up)) - hop, s: 1.15, f: 1, torso: lerp(8, -4, up), head: -8, lF: [lerp(4, 84, up), lerp(176, 96, up)], lB: [lerp(16, 96, up), lerp(168, 90, up)], t: lt, smile: 1, grin: 1, aF: [lerp(90, -58, up), lerp(90, -66, up)], aB: [lerp(90, -122, up), lerp(90, -114, up)] };
      me.pose(pose);
    }
    cic.update(lt, 3, lt < 0.6);
    popSquash(cal.el, lt, 0.05);
    const r = rollValue(lt, L(P.D2) - 0.1, L(P.D2) + 0.3, 127, 128);
    counter.update(lt, 0.15, r.v, r.speed, [L(P.D2) + 0.3]);
    popSquash(ok, lt, L(P.D2) + 0.35);
    ok.style.opacity = lt > L(P.D2) + 0.3 ? 1 : 0;
    mail.update(lt, L(P.Dx) - 0.1, [99, L(P.D3)], L(P.D3) + 0.35);
    mail.el.style.display = lt > L(P.Dx) - 0.15 ? 'block' : 'none';
    conf(lt); leak(lt, 0.25 + 0.4 * prog(lt, L(P.D3), L(P.D3) + 0.6));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S10 — video call home, telling the truth now; "แค่อยากรู้ว่าเราไหวไหม"
// =====================================================================
(() => {
  const [A, B] = SC.s10;
  const S = new Shot(A, B, [['far', 0.35, 10], ['mid', 1, 10]]);
  S.grade = 'saturate(1.1) contrast(1.02)';
  const set = balconyNight(S), L = t => t - A;
  S.L.far.el.style.filter = 'blur(8px) brightness(0.7)'; S.L.mid.el.style.filter = 'blur(8px) brightness(0.7)';
  const behind = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, S.ui);
  const call = videoCall(S.ui, 170, 200, 740, 1200);
  const b1 = html('div', 'bubble2', S.ui); b1.style.left = '120px'; b1.style.top = '1010px'; b1.textContent = 'ไหวไหมลูก';
  const b2 = html('div', 'bubble2 me', S.ui); b2.style.left = '560px'; b2.style.top = '960px'; b2.textContent = 'ไหวครับแม่';
  b2.style.background = '#9be38b';
  const fxs = fxSvg(S);
  const hearts = heartsRise(behind, 540, 1100, L(P.D8) + 0.2, 10, 503, 0.25);
  const leak = lightLeak(S.fx);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: 0, y: 0, z: lerp(1.02, 1.08, k), fx: 540, fy: 900 });
    set.update(lt + 30);
    call.update(lt, 0.05);
    call.el.style.transform += ` scale(${lerp(1, 1.04, k).toFixed(4)})`;
    popSquash(b1, lt, L(P.D8) - 0.1, '', -10); b1.style.opacity = fadeIn(lt, L(P.D8) - 0.1, 0.1);
    popSquash(b2, lt, L(P.D8) + 0.75, '', 10); b2.style.opacity = fadeIn(lt, L(P.D8) + 0.75, 0.1);
    hearts(lt); leak(lt, 0.3 + 0.3 * prog(lt, L(P.D8), L(P.D8) + 1));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S11 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s11;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#6a4a6e'], [0.6, '#352440'], [1, '#170f1f']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 143, { color: '#ffe2a8', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const fxs = fxSvg(S);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const icon = html('div', 'title', wrap); icon.style.top = '300px'; icon.innerHTML = portrait5('mom', 230, '#ffe9c4', { smile: 1 });
  icon.querySelector('svg').style.borderRadius = '50%'; icon.querySelector('svg').style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)';
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['1', '2', '7'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ใบสมัคร'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '96px';
  const t2 = html('div', 'title', wrap, 'ที่แม่รู้มาตลอด'); t2.style.top = '810px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'ไม่ไหวก็บอกที่บ้านได้นะ'); sub.style.top = '980px'; sub.style.font = '500 52px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1120px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่กำลังหางาน</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  const spark = burst(fxs, 540, 420, 0.3, 18, 153, ['#ffd66b', '#ffffff', '#ff9fc0'], 240, 0.9);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(icon, lt, 0.15, `rotate(${(Math.sin(lt * 2.4) * 4).toFixed(2)}deg)`, -20);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
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
const warm = html('div', 'blackout', frame); warm.style.background = '#fff4e6';
window.render = t => {
  for (const sh of SHOTS) {
    const next = SHOTS.find(o => o.a >= sh.b - 1e-6 && o.a < sh.b + 0.5);
    const until = next && next.fadeIn ? Math.max(sh.b, next.a + next.fadeIn) : sh.b;
    const on = t >= sh.a && t < until;
    sh.root.style.display = on ? 'block' : 'none';
    if (on) { if (sh.fadeIn) sh.root.style.opacity = prog(t, sh.a, sh.a + sh.fadeIn).toFixed(3); sh.update(t - sh.a); }
  }
  renderKinetic2(subsBox, CUES, t);
  grainTick(t);
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, DURATION - 0.45, DURATION)).toFixed(3);
  const fl = tt => prog(t, tt - 0.25, tt) * (1 - prog(t, tt, tt + 0.3));
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.8, fl(SC.s2[0]) * 0.6, fl(SC.s4[0]) * 0.5, fl(SC.s7[0]) * 0.5, fl(SC.s8[0]), fl(SC.s9[0]) * 0.8, fl(SC.s10[0]) * 0.6, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
