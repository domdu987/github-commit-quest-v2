// "312 ชามที่ไม่มีผักชี" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D5; H is the "ถ้า..." hook).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3], s3: [P.C0 - 0.3, P.E0 - 0.2], s4: [P.E0 - 0.2, P.title],
  s5: [P.title, P.D0 - 0.1], s6: [P.D0 - 0.1, P.D3 - 0.15], s7: [P.D3 - 0.15, P.end], s8: [P.end, DURATION] };
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));

const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
// the screen faces whoever holds it, so the viewer sees the back of the phone (case + camera) and only a sliver of
// screen light on the edge turned toward the face
function phoneProp(parent, case_ = '#2a2b36') {
  const g = svg('g', {}, parent);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: case_, stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -15, y: -39, width: 5, height: 52, rx: 2.5, fill: '#d8e8ff' }, g);
  svg('rect', { x: -1, y: -39, width: 14, height: 17, rx: 4, fill: shade(case_, -28), stroke: INK, 'stroke-width': 2 }, g);
  svg('circle', { cx: 4, cy: -34, r: 2.6, fill: '#15151c' }, g); svg('circle', { cx: 4, cy: -27, r: 2.6, fill: '#15151c' }, g);
  svg('circle', { cx: 9.5, cy: -30.5, r: 1.4, fill: '#fff6dc' }, g);
  return { g, scr };
}
function holdPhone(pup, pose, fx = 78, fy = -RIG.T + 36, tap = 0) {
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, fx, fy));
  pose.aB = pup.reach(pose, tx - 6, ty + 8);
  pose.aF = pup.reach(pose, tx + 6, ty - 2 + tap * 9);
  pose.propRot = -12;
  return [tx, ty];
}
const toScreen = (c, d, x, y) => { const z = 1 + (c.z - 1) * d; return [c.fx + (x - c.fx) * z - c.x * d, c.fy + (y - c.fy) * z - c.y * d]; };
const ROOM_P = { x: 330, y: 1172, s: 1.2 };
// world head centres of the resting poses, for framing close-ups
const HW = (x, y, s, f = 1) => [x + f * s * HEAD_C[0], y + s * HEAD_C[1]];
const H_MIN_ROOM = HW(330, 1172, 1.2), H_MIN_LOUNGE = HW(400, 1200, 1.2), H_PAN_LOUNGE = HW(720, 1200, 1.2, -1);
const H_MIN_SHOP = HW(360, 1215, 1.25), H_PAN_SHOP = HW(720, 1215, 1.25, -1);
// light the cast: rim + core shade on the people layer, a cast shadow for each puppet on the wall behind
function lightCast(S, set, pups, o = {}) {
  const Lt = set.light || {};
  set.people.setAttribute('filter', charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {})));
  return pups.map(p => castShadow(p, set.shadowL, S.L.mid.defs, Object.assign({ lx: Lt.lx }, o.shadow || {})));
}
const CAM_ROOM = (k, dz = 0) => ({ x: lerp(-20, 0, k), y: lerp(-10, 0, k), z: lerp(1.1, 1.15, k) + dz, fx: 460, fy: 1100 });
// มิน on the edge of her bed with her phone
function minBed(pup, lt, o = {}) {
  const pose = Object.assign({ x: ROOM_P.x, y: ROOM_P.y, s: ROOM_P.s, f: 1, torso: 4, head: 12 + Math.sin(lt * 1.2) * 2, lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: 0.5 }, o);
  holdPhone(pup, pose, 78, -RIG.T + 40, o.tap || 0);
  pup.pose(pose);
  return pose;
}
function angryMark(parent) {
  const g = svg('g', { opacity: 0 }, parent);
  for (const a of [0, 90, 180, 270]) svg('path', { d: 'M5,-5 Q14,-14 22,-6', fill: 'none', stroke: '#e0453b', 'stroke-width': 6, 'stroke-linecap': 'round', transform: `rotate(${a})` }, g);
  return (t, t0, t1, x, y) => { const on = t > t0 && t < t1; g.setAttribute('opacity', on ? fadeIn(t, t0, 0.08) : 0); g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${(on ? 0.9 + 0.12 * Math.sin(t * 16) : 1).toFixed(3)})`); };
}

// =====================================================================
// S0 — hook: "ถ้าคุณมีแฟนที่ไม่เคยพูดคำว่ารัก ถ้าเขาบอกรักคุณมาแล้วสามร้อยกว่าครั้ง คุณจะรู้ตัวไหม"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = herRoom(S), L = t => t - A;
  const min = new Puppet(set.people, MIN, S.L.mid.defs); const ph = phoneProp(min.prop, '#f07aa8');
  lightCast(S, set, [min], { light: { rim: '#ffe0b0' } });
  const shots = [
    { t: 0, cam: frameAt(470, 1150, 1.1, 540, 1070), to: frameAt(450, 1140, 1.16, 540, 1070) },
    { t: L(P.H2) - 0.05, cam: frameAt(H_MIN_ROOM[0] + 60, H_MIN_ROOM[1] + 90, 1.5, 420, 1130), to: frameAt(H_MIN_ROOM[0] + 50, H_MIN_ROOM[1] + 80, 1.58, 420, 1130) },
    { t: L(P.H4) - 0.05, cam: frameAt(H_MIN_ROOM[0] + 30, H_MIN_ROOM[1] + 30, 2.0, 470, 1180), to: frameAt(H_MIN_ROOM[0] + 30, H_MIN_ROOM[1] + 30, 2.12, 470, 1180) },
  ];
  const chat = chatThread7(S.ui, 540, 100, 490, 560, 'ปั้น', panAv(64), [
    { k: 'R', text: 'รักนะ', meta: 'อ่านแล้ว', t0: L(P.H0) + 0.15 }, { k: 'L', text: 'อืม', t0: L(P.H1) + 0.35 },
  ]);
  chat.el.classList.add('big7');
  const said = saidLoveChip(S.ui, 40, 120);
  const cnt = loveCounter(S.ui, 140, 230);
  const back = behindSvg(S);
  const qw = html('div', 'qwrap', S.ui); Object.assign(qw.style, { left: '470px', top: '560px', width: '130px', height: '130px' }); html('div', 'qmark', qw, '?').style.fontSize = '92px';
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt);
    const look = lt > L(P.H4) - 0.1;
    const p = minBed(min, lt, { smile: look ? 0.25 : 0.35, head: look ? -6 : 12 + Math.sin(lt * 1.2) * 2, torso: look ? 0 : 4, tap: lt < L(P.H0) + 0.1 ? Math.max(0, Math.sin(lt * 8)) * 0.6 : 0 });
    const [px, py] = toWorld(p, ...torsoPt(p, 78, -RIG.T + 40));
    ph.scr.setAttribute('fill', '#ffe4ee');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    const out = ease.inCubic(prog(lt, L(P.H2) - 0.25, L(P.H2) + 0.05));
    enter3d(chat.el, lt, 0.05, 'pop'); chat.update(lt);
    chat.el.style.opacity = (parseFloat(chat.el.style.opacity) * (1 - out)).toFixed(3);
    said.update(lt, L(P.H1) + 0.05, L(P.H1) + 0.45);
    said.el.style.opacity = (parseFloat(said.el.style.opacity) * (1 - out)).toFixed(3);
    cnt.update(lt, L(P.H2) + 0.02, L(P.H2) + 0.3, L(P.H3) + 0.6, L(P.H4) + 0.1);
    cnt.c.c.style.opacity = (parseFloat(cnt.c.c.style.opacity) * (lt > L(P.H2) ? 1 : 0)).toFixed(3);
    const [qx, qy] = toScreen(cam, 1, ...toWorld(p, ...torsoPt(p, HEAD_C[0] + 70, HEAD_C[1] - 120)));
    qw.style.left = (qx - 65).toFixed(1) + 'px'; qw.style.top = (qy - 65).toFixed(1) + 'px';
    popSquash(qw, lt, L(P.H4) + 0.2, `rotate(${(Math.sin(lt * 5) * 8).toFixed(1)}deg)`, 20); qw.style.opacity = fadeIn(lt, L(P.H4) + 0.2, 0.1);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — three years together: he's on his game, never says it; his feed has no couple photos; other couples post sweet captions
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = loungeNight(S), L = t => t - A;
  const min = new Puppet(set.people, MIN, S.L.mid.defs);
  const pan = new Puppet(set.people, PAN, S.L.mid.defs); const pph = phoneProp(pan.prop);
  lightCast(S, set, [min, pan], { shadow: { k: 0.22, skewK: 0.02 } });
  const shots = [
    { t: 0, cam: frameAt(560, 1130, 1.1, 540, 1080), to: frameAt(545, 1120, 1.15, 540, 1080) },
    { t: L(P.A2) - 0.05, cam: frameAt(H_PAN_LOUNGE[0] - 60, H_PAN_LOUNGE[1] + 90, 1.55, 620, 1150), to: frameAt(H_PAN_LOUNGE[0] - 60, H_PAN_LOUNGE[1] + 80, 1.63, 620, 1150) },
    { t: L(P.A3) - 0.15, cam: frameAt(560, 1110, 1.12, 540, 1100), to: frameAt(560, 1100, 1.18, 540, 1100) },
    { t: L(P.A5) - 0.1, move: 0.9, cam: frameAt(H_MIN_LOUNGE[0] + 40, H_MIN_LOUNGE[1] + 100, 1.45, 470, 1160), to: frameAt(H_MIN_LOUNGE[0] + 40, H_MIN_LOUNGE[1] + 90, 1.5, 470, 1160) },
  ];
  const yrs = chip7(S.ui, 50, 110, 'คบกันมา <b>3 ปี</b>', 'today7');
  const cal = calendarFlip(yrs.slot, 58, '#f04f7f');
  const said = saidLoveChip(S.ui, 50, 210);
  const prof = profileGrid8(S.ui, 36, 300, 470);
  const post = postCard8(S.ui, 578, 300, 466, 'ploy.love', coupleAv(64), anniversaryPhoto(470, 260).replace('width="470" height="260"', 'width="470" height="255"'), `ที่รักของเค้า รักที่สุดในโลก <span class="ic5">${heartSVG(30)}</span>`, '1,204');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 2);
    // ปั้น: thumbs flying on a phone game
    const pp = { x: 720, y: 1200, s: 1.2, f: -1, torso: 6, head: 16 + Math.sin(lt * 1.1) * 1.5, lF: [-2, 88], lB: [2, 92], t: lt + 3, smile: 0.55 };
    const [px, py] = holdPhone(pan, pp, 76, -RIG.T + 42, Math.max(0, Math.sin(lt * 15)) * 0.8);
    pan.pose(pp);
    pph.scr.setAttribute('fill', '#cfe4ff');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    // มิน: looks at him, waiting for something; slumps a little when nothing comes
    const sigh = ease.inOutSine(prog(lt, L(P.A2b), L(P.A2b) + 0.5));
    const mp = { x: 400, y: 1200, s: 1.2, f: 1, torso: lerp(-2, 6, sigh), head: lerp(-6, 8, sigh) + Math.sin(lt * 1.3) * 1.5, lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: lerp(0.6, 0.25, sigh), aF: [70, 18], aB: [76, 22] };
    if (lt > L(P.A2) - 0.2 && lt < L(P.A2b)) { const [hx, hy] = toWorld(pp, ...torsoPt(pp, -10, -RIG.T + 40)); const k2 = Math.max(0, Math.sin((lt - L(P.A2)) * 9)); mp.aF = min.reach(mp, hx - 24 + k2 * 10, hy); }   // pokes his arm
    min.pose(mp);
    popSquash(yrs.el, lt, L(P.A0) + 0.05); cal.update(lt, 3, lt < L(P.A1) + 0.3);
    said.update(lt, L(P.A2) - 0.05, L(P.A2b));
    const chipOut = 1 - prog(lt, L(P.A3) - 0.3, L(P.A3) - 0.05);
    yrs.el.style.opacity = (parseFloat(yrs.el.style.opacity) * chipOut).toFixed(3); said.el.style.opacity = (parseFloat(said.el.style.opacity) * chipOut).toFixed(3);
    prof.update(lt, L(P.A3) - 0.1, L(P.A3) + 0.7);
    const kp = spring(lt, L(P.A4) - 0.05, 13, 6);
    post.style.opacity = fadeIn(lt, L(P.A4) - 0.05, 0.12);
    post.style.transform = `translateX(${((1 - kp) * 260).toFixed(1)}px) rotate(${(3 * kp).toFixed(2)}deg)`;
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — that night: a friend's anniversary surprise; she types "เธอไม่เคยบอกรักเราเลยนะ"; he answers "พรุ่งนี้ไปกินก๋วยเตี๋ยวกัน"
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.05) contrast(1.04)';
  const set = herRoom(S), L = t => t - A;
  const min = new Puppet(set.people, MIN, S.L.mid.defs); const ph = phoneProp(min.prop, '#f07aa8');
  lightCast(S, set, [min], { light: { rim: '#ffe0b0' } });
  const mark = angryMark(set.top);
  const post = postCard8(S.ui, 70, 110, 560, 'mint_ww', coupleAv(64), anniversaryPhoto(560, 300).replace('width="560" height="300"', 'width="560" height="300"'), `แฟนเซอร์ไพรส์ครบรอบ 3 ปี <span class="ic5">${heartSVG(30)}</span>`, '892');
  const tSend = L(P.B3) + 1.1, tReply = L(P.B5) - 0.05;
  const chat = chatThread7(S.ui, 470, 90, 580, 820, 'ปั้น', panAv(64), [
    { k: 'date', text: 'วันนี้' },
    { k: 'R', text: 'เธอไม่เคยบอกรักเราเลยนะ', meta: '22:47', t0: tSend },
    { k: 'L', text: 'พรุ่งนี้ไปกินก๋วยเตี๋ยวกัน', t0: tReply },
  ], true);
  chat.el.classList.add('big7');
  const shots = [
    { t: 0, cam: frameAt(480, 1140, 1.12, 540, 1080), to: frameAt(470, 1130, 1.17, 540, 1080) },
    { t: L(P.B2) - 0.15, cam: frameAt(H_MIN_ROOM[0] + 80, H_MIN_ROOM[1] + 140, 1.36, 300, 1200), to: frameAt(H_MIN_ROOM[0] + 80, H_MIN_ROOM[1] + 130, 1.42, 300, 1200) },
    { t: L(P.B5) + 0.3, cam: frameAt(H_MIN_ROOM[0] + 30, H_MIN_ROOM[1] + 40, 1.9, 330, 1220), to: frameAt(H_MIN_ROOM[0] + 30, H_MIN_ROOM[1] + 40, 2.0, 330, 1220) },
  ];
  const typ = html('div', 'crow L', chat.el.querySelector('.clist')); const typB = html('div', 'cbub ctyping', typ); for (let k = 0; k < 3; k++) html('i', '', typB);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 3);
    const mad = lt > tReply + 0.35;
    const sad = lt > L(P.B0) + 0.4 && lt < L(P.B2);
    const p = minBed(min, lt, { smile: mad ? 0.05 : sad ? 0.15 : 0.35, angry: mad ? 1 : null, head: mad ? -4 : 14 + Math.sin(lt * 1.2) * 2, torso: mad ? -6 : 4, tap: lt > L(P.B2) + 0.1 && lt < tSend - 0.1 ? Math.max(0, Math.sin(lt * 18)) : 0 });
    const [px, py] = toWorld(p, ...torsoPt(p, 78, -RIG.T + 40));
    ph.scr.setAttribute('fill', '#ffe4ee');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    const [hx, hy] = toWorld(p, ...torsoPt(p, HEAD_C[0] + 52, HEAD_C[1] - 62));
    mark(lt, tReply + 0.35, 99, hx, hy);
    // the friend's post, then her chat
    const kp = spring(lt, L(P.B0) + 0.05, 13, 6), outp = ease.inCubic(prog(lt, L(P.B2) - 0.3, L(P.B2)));
    post.style.opacity = (fadeIn(lt, L(P.B0) + 0.05, 0.12) * (1 - outp)).toFixed(3);
    post.style.transform = `translateY(${((1 - kp) * -200 - outp * 120).toFixed(1)}px) rotate(${(-2 * kp).toFixed(2)}deg)`;
    const shown = lt > L(P.B2) - 0.15;
    if (shown) enter3d(chat.el, lt, L(P.B2) - 0.15, 'pop'); else chat.el.style.opacity = 0;
    chat.update(lt);
    chat.type(lt, [{ t0: L(P.B2) + 0.15, t1: tSend - 0.2, text: 'เธอไม่เคยบอกรักเราเลยนะ', mode: 'type' }, { t0: tSend - 0.05, t1: tSend, text: '', mode: 'hold' }]);
    const tyOn = lt > L(P.B4) - 0.2 && lt < tReply;
    typ.style.opacity = tyOn ? 1 : 0; typ.style.position = 'absolute'; typ.style.top = '175px';
    [...typB.children].forEach((d, j) => { d.style.transform = `translateY(${(-6 * Math.max(0, Math.sin(lt * 9 - j * 0.9))).toFixed(1)}px)`; });
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// noodle-shop staging shared by S3, S6, S7
// =====================================================================
const SHOP = { minX: 360, panX: 720, y: 1215, s: 1.25, herX: 470, hisX: 668, saucerX: 572 };
const TIP = 57;   // chopstick tips sit TIP px left of and below his wrist
const CAM_SHOP = (k, dz = 0) => ({ x: lerp(-8, 8, k), y: lerp(5, 15, k), z: lerp(1.15, 1.19, k) + dz, fx: 540, fy: 1100 });
function shopCast(S) {
  const set = noodleShop(S, { herX: SHOP.herX, hisX: SHOP.hisX, saucerX: SHOP.saucerX, minX: SHOP.minX, panX: SHOP.panX });
  const min = new Puppet(set.people, MIN, S.L.mid.defs);
  const pan = new Puppet(set.people, PAN, S.L.mid.defs);
  lightCast(S, set, [min, pan], { light: { rim: '#ffe6b8', rimOp: 0.6, shadeOp: 0.34 }, shadow: { k: 0.04, dy: 40, sx: 1.04, sy: 1.0, skewK: 0, op: 0.16, blur: 9 } });
  // chopsticks in his front hand; the carried leaf sits at their tips
  const sticks = svg('g', {}, pan.prop);
  svg('path', { d: 'M-6,-2 L44,48 M2,-8 L50,42', stroke: '#c98f4a', 'stroke-width': 5, 'stroke-linecap': 'round' }, sticks);
  const carried = corianderLeaf(sticks, 1.05); carried.setAttribute('transform', 'translate(46,45)'); carried.setAttribute('opacity', 0);
  // pick her leaves nearest to him first
  const order = set.herBowl.pos.map((p, i) => [p[0], i]).sort((a, b) => b[0] - a[0]).map(v => v[1]);
  return { set, min, pan, carried, sticks, order };
}
// his pose: picking the leaves out of her bowl one at a time, or resting the chopsticks over his own bowl
function panPick(cast, lt, picks, o = {}) {
  const { pan, carried, set, order, sticks } = cast;
  const pose = Object.assign({ x: SHOP.panX, y: SHOP.y, s: SHOP.s, f: -1, torso: 12, head: 16, lF: [-2, 88], lB: [2, 92], t: lt + 2, smile: 0.45, aB: [72, 34], propRot: 0 }, o);
  const W = ([x, y]) => [x + TIP, y - TIP];   // wrist position that puts the tips on (x, y)
  const sauc = W([SHOP.saucerX + 6, 1142]), rest = [628, 1112];   // resting hand low on the table, never up by his face
  let tgt = rest, carry = false, dip = 0;
  const n = picks.filter(t0 => lt >= t0).length;
  if (n > 0 && n <= order.length && lt < picks[n - 1] + 0.9) {
    const leaf = W(set.herBowl.pos[order[n - 1]]);
    const u = (lt - picks[n - 1]) / 0.9;
    if (u < 0.4) tgt = mv2(n > 1 ? sauc : rest, leaf, u / 0.4);
    else if (u < 0.5) { tgt = leaf; dip = Math.sin(Math.PI * (u - 0.4) / 0.1) * 8; }
    else if (u < 0.88) { tgt = mv2(leaf, sauc, (u - 0.5) / 0.38); carry = true; }
    else { tgt = sauc; dip = Math.sin(Math.PI * (u - 0.88) / 0.12) * 6; }
  } else if (n > 0) tgt = mv2(sauc, rest, prog(lt, picks[n - 1] + 0.9, picks[n - 1] + 1.4));
  if (o.hold) tgt = o.hold;
  else tgt = [tgt[0], tgt[1] + Math.sin(lt * 1.7) * 2];
  pose.aF = pan.reach(pose, tgt[0], tgt[1] + dip);
  pan.pose(pose);
  sticks.setAttribute('opacity', o.hold ? 0 : 1);
  carried.setAttribute('opacity', carry ? 1 : 0);
  const picked = picks.filter(t0 => lt >= t0 + 0.45 * 0.9).length, dropped = picks.filter(t0 => lt >= t0 + 0.9 * 0.9).length;
  order.forEach((li, k) => set.herBowl.leaves[li].setAttribute('opacity', k < picked ? 0 : 1));
  set.saucer.forEach((lf, i) => lf.setAttribute('opacity', i < dropped ? 1 : 0));
  return pose;
}
const mv2 = (a, b, k) => [lerp(a[0], b[0], ease.inOutSine(k)), lerp(a[1], b[1], ease.inOutSine(k))];
const PICKS = Array.from({ length: 7 }, (_, i) => P.C2 + 0.35 + i * 0.95);

// =====================================================================
// S3 — the usual noodle shop: she sulks, then sees him picking the coriander out of her bowl, one leaf at a time
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.08) contrast(1.03)';
  const L = t => t - A;
  const cast = shopCast(S);
  const mark = angryMark(cast.set.top);
  const pol = firstDatePolaroid(S.ui, 50, 200, 400);
  const picks = PICKS.map(L);
  const shots = [
    { t: 0, cam: frameAt(540, 1110, 1.14, 540, 1110), to: frameAt(530, 1100, 1.19, 540, 1110) },
    { t: L(P.C2) - 0.1, cam: frameAt(H_MIN_SHOP[0] + 40, H_MIN_SHOP[1] + 110, 1.55, 400, 1180), to: frameAt(H_MIN_SHOP[0] + 40, H_MIN_SHOP[1] + 100, 1.62, 400, 1180) },
    { t: L(P.C3) - 0.1, cam: frameAt(SHOP.herX + 30, 1105, 3.0, 540, 1290), to: frameAt(SHOP.herX + 40, 1105, 3.2, 540, 1290) },
    { t: L(P.C5) - 0.1, cam: frameAt(560, 1090, 1.3, 600, 1180), to: frameAt(560, 1080, 1.36, 600, 1180) },
    { t: L(P.C7) - 0.05, cam: frameAt(H_MIN_SHOP[0] + 50, H_MIN_SHOP[1] + 60, 1.85, 430, 1180), to: frameAt(H_MIN_SHOP[0] + 50, H_MIN_SHOP[1] + 60, 1.95, 430, 1180) },
  ];
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    cast.set.update(lt, cam);
    panPick(cast, lt, picks, { smile: 0.45 });
    // มิน: arms crossed and looking away, then she notices, softens, and finally smiles
    const notice = ease.inOutSine(prog(lt, L(P.C2) - 0.1, L(P.C2) + 0.4));
    const soft = ease.inOutSine(prog(lt, L(P.C7), L(P.C8) + 0.3));
    const mp = { x: SHOP.minX, y: SHOP.y, s: SHOP.s, f: 1, torso: lerp(-8, 6, notice), head: lerp(-14, 14, notice) + Math.sin(lt * 1.3) * 1.5, lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: lerp(lerp(0.08, 0.35, notice), 0.85, soft), angry: notice < 0.5 ? 1 : null, eyes: soft > 0.6 ? 0 : null };
    const [cx, cy] = toWorld(mp, ...torsoPt(mp, 34, -RIG.T + 62));
    const crossF = min => min.reach(mp, cx + 12, cy), crossB = min => min.reach(mp, cx - 6, cy + 10);
    if (notice < 0.5) { mp.aF = crossF(cast.min); mp.aB = crossB(cast.min); }
    else { const [chx, chy] = toWorld(mp, ...torsoPt(mp, HEAD_C[0] + 46, HEAD_C[1] + 56)); mp.aF = cast.min.reach(mp, lerp(cx + 12, chx, notice), lerp(cy, chy, notice)); mp.aB = [72, 20]; }   // chin in her hand, watching
    cast.min.pose(mp);
    const [hx, hy] = toWorld(mp, ...torsoPt(mp, HEAD_C[0] + 50, HEAD_C[1] - 62));
    mark(lt, 0.05, L(P.C2), hx, hy);
    pol.update(lt, L(P.C5) - 0.05, L(P.C7) + 0.3);
    pol.el.style.opacity = (parseFloat(pol.el.style.opacity) * (1 - prog(lt, B - A - 0.35, B - A - 0.05))).toFixed(3);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — 3 years × 52 weeks × 2 bowls = 312 bowls; he never once mentioned it
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 12], ['mid', 1, 12]]);
  const L = t => t - A;
  const cast = shopCast(S);
  S.L.far.el.style.filter = 'blur(12px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(12px) brightness(0.5) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 200, 1080, 1400], 16, 831, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const card = bowlMath8(S.ui, 50, 150, 980);
  const never = chip7(S.ui, 170, 860, 'เขาไม่เคยพูดถึงมัน <b>สักครั้ง</b>', 'long7');
  never.slot.innerHTML = `<span class="ic5"><svg width="58" height="50" viewBox="-30 -26 60 52"><path d="M-24,-18 Q-24,-22 -20,-22 L20,-22 Q24,-22 24,-18 L24,6 Q24,10 20,10 L-4,10 L-12,20 L-11,10 L-20,10 Q-24,10 -24,6 Z" fill="#fff" stroke="${INK}" stroke-width="3"/><path d="M-12,-6 L12,-6" stroke="${INK}" stroke-width="4" stroke-linecap="round"/><path d="M-8,-10 L-8,-2 M0,-10 L0,-2 M8,-10 L8,-2" stroke="${INK}" stroke-width="2"/></svg></span>`;
  const spark = burst(back, 540, 520, L(P.E4) + 0.6, 22, 833, ['#ffd66b', '#ffffff', '#7fd6c7'], 340, 1.0);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    cast.set.update(lt + 9); bok(lt);
    panPick(cast, lt, PICKS.map(() => -9), {});
    cast.min.pose({ x: SHOP.minX, y: SHOP.y, s: SHOP.s, f: 1, torso: 4, head: 10, lF: [-2, 88], lB: [2, 92], t: lt, smile: 0.6, aF: [70, 20], aB: [72, 20] });
        card.update(lt, 0.05, [L(P.E0), L(P.E1) + 0.1, L(P.E2), L(P.E3)], L(P.E3) + 0.1, L(P.E4) + 0.6);
    spark(lt);
    popSquash(never.el, lt, L(P.E5) + 0.1);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — title: 312 ชาม / ที่ไม่มีผักชี
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const cast = shopCast(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 841, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '360px'; ic.innerHTML = bowlSVG(280, { crossed: true, steam: true });
  const t1 = html('div', 'title', wrap); t1.style.top = '700px'; t1.style.font = '700 200px/1 Kanit';
  const digits = ['3', '1', '2'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ชาม'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่ไม่มีผักชี'); t2.style.top = '930px'; t2.style.font = '600 112px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    cast.set.update(lt + 12); bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.45, 14, 7); unit.style.opacity = fadeIn(lt, 0.45, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — "บางคนบอกรักด้วยคำพูด บางคนบอกรักด้วยการจำว่าเราไม่ชอบอะไร"
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.1) contrast(1.03)';
  const L = t => t - A;
  const cast = shopCast(S);
  const two = twoLoves8(S.ui, 400);   // below the menu board, above their heads
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    const cam = applyCam(S, shotCam(lt, [{ t: 0, cam: frameAt(540, 1060, 1.22, 540, 1150), to: frameAt(540, 1050, 1.3, 540, 1150) }], B - A));
    cast.set.update(lt + 14, cam);
    panPick(cast, lt, PICKS.map(() => -9), { smile: 0.55, head: 8 });
        const mp = { x: SHOP.minX, y: SHOP.y, s: SHOP.s, f: 1, torso: 6, head: 6 + Math.sin(lt * 1.3) * 1.5, lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: 0.9, aB: [72, 20] };
    const [chx, chy] = toWorld(mp, ...torsoPt(mp, HEAD_C[0] + 46, HEAD_C[1] + 56));
    mp.aF = cast.min.reach(mp, chx, chy);
    cast.min.pose(mp);
    two.update(lt, L(P.D0) + 0.05, L(P.D2) - 0.05);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — "ลองหันไปดูคนข้างๆ เขาอาจบอกรักคุณอยู่ทุกวัน": they look at each other; she leans on his shoulder
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.12) contrast(1.03) brightness(1.03)';
  const L = t => t - A;
  const cast = shopCast(S);
  const hearts = heartsRise(svg('g', {}, cast.set.people), 560, 1060, L(P.D4) + 0.1, 10, 851, 0.28);
  cast.set.people.insertBefore(cast.set.people.lastChild, cast.set.people.firstChild);   // hearts behind both of them
  const leak = lightLeak(S.fx);
  const shots = [
    { t: 0, cam: frameAt(540, 1010, 1.42, 540, 1060), to: frameAt(540, 1005, 1.5, 540, 1060) },
    { t: L(P.D4) - 0.2, cam: frameAt(586, 1118, 3.0, 540, 1290), to: frameAt(586, 1118, 3.2, 540, 1290) },
    { t: L(P.D4) + 1.0, move: 1.6, cam: frameAt(540, 1060, 1.22, 540, 1100), to: frameAt(540, 1050, 1.26, 540, 1100) },
  ];
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    cast.set.update(lt + 16, cam);
        const turn = ease.inOutSine(prog(lt, L(P.D3), L(P.D3) + 0.4));
    const lean = ease.inOutSine(prog(lt, L(P.D4) - 0.2, L(P.D4) + 0.5));
    hearts(lt);
    const hold = ease.inOutSine(prog(lt, L(P.D4) - 0.3, L(P.D4) + 0.3));
    panPick(cast, lt, PICKS.map(() => -9), { head: lerp(16, -2, turn), torso: lerp(12, 4, turn), smile: lerp(0.5, 0.95, turn), grin: lean > 0.6 ? 1 : 0, hold: hold > 0.01 ? mv2([628, 1112], [600, 1112], hold) : null });
    const mp = { x: SHOP.minX + 30 * lean, y: SHOP.y, s: SHOP.s, f: 1, torso: lerp(6, 16, lean), head: lerp(6, 14, lean), lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: 1, grin: turn > 0.5 && lean < 0.5 ? 1 : 0, eyes: lean > 0.6 ? 0 : null, aB: [72, 20] };
    mp.aF = cast.min.reach(mp, lerp(470, 572, hold), lerp(1130, 1114, hold));   // her hand slides across the table into his
    cast.min.pose(mp);
    leak(lt, 0.25 + 0.35 * lean);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#6a4a6e'], [0.6, '#352440'], [1, '#170f1f']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 861, { color: '#ffe2a8', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 863, ['#ffd66b', '#ffffff', '#ff9fc0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '300px';
  duo.innerHTML = `<span class="duo7">${minAv(190, { happy: true, grin: true })}</span><span class="duo7h" style="margin:0 18px">${bowlSVG(120, { crossed: true })}</span><span class="duo7">${panAv(190, { smile: 0.8 })}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '4px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['3', '1', '2'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ชาม'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่ไม่มีผักชี'); t2.style.top = '808px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'บางคนบอกรักด้วยการกระทำ'); sub.style.top = '975px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ไม่ค่อยพูดว่ารัก</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.65, 14, 7); unit.style.opacity = fadeIn(lt, 0.65, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.8, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.8, 1.2))) * 100).toFixed(1)}% -40% 0)`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.6, fl(SC.s2[0]) * 0.5, fl(SC.s3[0]) * 0.8, fl(SC.s4[0]) * 0.6, fl(SC.s5[0]), fl(SC.s6[0]) * 0.7, fl(SC.s7[0]) * 0.5, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
