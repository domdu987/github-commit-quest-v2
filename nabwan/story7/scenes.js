// "11 ปีที่เพื่อนไม่เคยลืม" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D7; H is the "ถ้า..." hook).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.A3 - 0.15], s2: [P.A3 - 0.15, P.A6 - 0.15], s3: [P.A6 - 0.15, P.B0 - 0.3], s4: [P.B0 - 0.3, P.Cst - 0.3],
  s5: [P.Cst - 0.3, P.C5 - 0.15], s6: [P.C5 - 0.15, P.title], s7: [P.title, P.D0 - 0.1], s8: [P.D0 - 0.1, P.D6 - 0.15], s9: [P.D6 - 0.15, P.end], s10: [P.end, DURATION] };
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));

const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
// an svg in the UI layer created before the cards, so sparkles and hearts stay behind faces and cards
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function phoneProp(parent, case_ = '#2a2b36') {
  const g = svg('g', {}, parent);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: case_, stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, g);
  return { g, scr };
}
function holdPhone(pup, pose, fx = 78, fy = -RIG.T + 36, tap = 0) {
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, fx, fy));
  pose.aB = pup.reach(pose, tx - 6, ty + 8);
  pose.aF = pup.reach(pose, tx + 6, ty - 2 + tap * 9);
  pose.propRot = -12;
  return [tx, ty];
}
// screen position of a world point under a shot camera
const toScreen = (c, d, x, y) => { const z = 1 + (c.z - 1) * d; return [c.fx + (x - c.fx) * z - c.x * d, c.fy + (y - c.fy) * z - c.y * d]; };
function sweatDrop(parent) {
  const g = svg('g', { opacity: 0 }, parent);
  svg('path', { d: 'M0,-22 C8,-8 12,0 12,6 A12,12 0 1 1 -12,6 C-12,0 -8,-8 0,-22 Z', fill: '#bfe3ff', stroke: INK, 'stroke-width': 3.5 }, g);
  svg('ellipse', { cx: -4, cy: 4, rx: 3, ry: 5, fill: '#fff', opacity: 0.8 }, g);
  return (t, t0, x, y) => { const k = prog(t, t0, t0 + 0.9); g.setAttribute('opacity', t > t0 ? (fadeIn(t, t0, 0.1) * (1 - prog(t, t0 + 1.4, t0 + 1.7))).toFixed(3) : 0); g.setAttribute('transform', `translate(${x.toFixed(1)},${(y + 26 * ease.inOutSine(k)).toFixed(1)}) scale(${(0.6 + 0.4 * Math.min(1, k * 3)).toFixed(3)})`); };
}

// him: sitting on the edge of his bed
const ME_P = { x: 330, y: 1172, s: 1.2 };
function mePose(me, lt, o = {}) {
  const pose = Object.assign({ x: ME_P.x, y: ME_P.y, s: ME_P.s, f: 1, torso: 4, head: 12 + Math.sin(lt * 1.2) * 2, lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: 0.5 }, o);
  if (o.phone !== false) holdPhone(me, pose, 78, -RIG.T + 40, o.tap || 0);
  else { pose.aF = o.aF || [76, 8]; pose.aB = o.aB || [82, 14]; }
  if (o.palm) { const [hx, hy] = toWorld(pose, ...torsoPt(pose, HEAD_C[0] + 44, HEAD_C[1] - 4)); const a = me.reach(pose, hx, hy, false); pose.aF = [lerp(pose.aF[0], a[0], o.palm), lerp(pose.aF[1], a[1], o.palm)]; }
  me.pose(pose);
  return pose;
}
const CAM_ROOM = (k, dz = 0) => ({ x: lerp(-20, 0, k), y: lerp(80, 100, k), z: lerp(1.36, 1.42, k) + dz, fx: 460, fy: 1250 });
const YEARS = ['2559', '2560', '2561', '2562', '2563', '2564', '2565', '2566', '2567', '2568'];

// =====================================================================
// S0 — hook: "ถ้าคุณมีเพื่อนที่ไม่ได้คุยกันเป็นปี / ถ้าวันเกิดคุณปีนี้ / เขายังจะจำได้ไหม"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.05) contrast(1.04)';
  const set = myRoom(S), L = t => t - A;
  const me = new Puppet(set.people, ME, S.L.mid.defs); const ph = phoneProp(me.prop);
  const row = chatRow7(S.ui, 60, 150, 960);
  const quiet = chip7(S.ui, 250, 350, 'ไม่ได้คุยกัน<b>เป็นปี</b>', 'long7');
  const qcal = calendarFlip(quiet.slot, 58, '#8a8f99');
  const back = behindSvg(S);
  const cake = cakeCard7(S.ui, 70, 170, 'วันเกิดคุณ', 'ปีนี้');
  const spark = burst(back, 260, 270, L(P.H2) + 0.1, 16, 701, ['#ffd66b', '#ffffff', '#ff9fc0'], 260, 0.9);
  const bk = avatarBadge(S.ui, 650, 150, bankAv(200), 'แบงค์', '#e0574b'); bk.el.classList.add('big7');
  const spot = html('div', 'spot', S.ui); Object.assign(spot.style, { left: '370px', top: '-200px', width: '640px', height: '900px' });
  S.ui.appendChild(bk.el);
  const qw = html('div', 'qwrap', S.ui); Object.assign(qw.style, { left: '862px', top: '64px', width: '130px', height: '130px' }); html('div', 'qmark', qw, '?').style.fontSize = '92px';
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-40, -20, k), y: lerp(50, 70, k), z: lerp(1.42, 1.48, k), fx: 460, fy: 1250 });
    set.update(lt);
    const look = lt > L(P.H4);
    const [px, py] = (() => { const p = mePose(me, lt, { smile: look ? 0.2 : 0.35, head: look ? -2 : 12 + Math.sin(lt * 1.2) * 2, torso: look ? 0 : 4, tap: lt < L(P.H2) ? Math.max(0, Math.sin(lt * 7)) * 0.5 : 0 }); return toWorld(p, ...torsoPt(p, 78, -RIG.T + 40)); })();
    ph.scr.setAttribute('fill', '#cfe4ff');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    // chat row + "เป็นปี" chip, then they slide away for the cake
    const out = ease.inCubic(prog(lt, L(P.H2) - 0.25, L(P.H2) + 0.05));
    row.update(lt, 0.15, L(P.H1) + 0.25);
    row.c.c.style.opacity = (parseFloat(row.c.c.style.opacity) * (1 - out)).toFixed(3);
    row.c.c.style.transform += ` translateY(${(-out * 120).toFixed(1)}px)`;
    popSquash(quiet.el, lt, L(P.H1) + 0.05); qcal.update(lt, 12, lt < L(P.H1) + 0.6);
    quiet.el.style.opacity = (parseFloat(quiet.el.style.opacity) * (1 - out)).toFixed(3);
    cake.update(lt, L(P.H2) + 0.05);
    cake.c.c.style.opacity = (parseFloat(cake.c.c.style.opacity) * (lt > L(P.H2) ? 1 : 0)).toFixed(3);
    spark(lt);
    bk.update(lt, L(P.H4) - 0.05);
    bk.el.style.opacity = (parseFloat(bk.el.style.opacity) * (lt > L(P.H4) - 0.06 ? 1 : 0)).toFixed(3);
    spot.style.opacity = (0.7 * prog(lt, L(P.H4) - 0.1, L(P.H4) + 0.3)).toFixed(3);
    popSquash(qw, lt, L(P.H5), `rotate(${(Math.sin(lt * 5) * 8).toFixed(1)}deg)`, 20); qw.style.opacity = fadeIn(lt, L(P.H5), 0.1);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — ม.4: the two of them at the canteen, laughing (sepia memory)
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  S.grade = 'sepia(0.55) saturate(0.95) contrast(1.03) brightness(1.02)';
  const set = canteen(S), L = t => t - A;
  const bench = svg('g', {}, set.people);
  svg('rect', { x: 180, y: 1236, width: 720, height: 24, rx: 8, fill: '#a8744e', stroke: INK, 'stroke-width': 5 }, bench);
  for (const lx of [220, 840]) svg('rect', { x: lx, y: 1260, width: 18, height: 70, fill: '#6a4428', stroke: INK, 'stroke-width': 4 }, bench);
  const me = new Puppet(set.people, ME_SCHOOL, S.L.mid.defs);
  const bk = new Puppet(set.people, BANK_SCHOOL, S.L.mid.defs);
  S.L.mid.s.appendChild(set.top);
  const yr = chip7(S.ui, 70, 150, 'ม.4 <b>ปี 2559</b>', 'today7');
  const cal = calendarFlip(yr.slot, 58, '#b08326');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-10, 10, k), y: 190, z: lerp(1.3, 1.36, k), fx: 540, fy: 1150 });
    const laugh = Math.sin(lt * 11);
    const mp = { x: 380, y: 1236, s: 1.2, f: 1, torso: 4 + laugh * 2, head: -4 + laugh * 3, lF: [-2, 88], lB: [2, 92], t: lt, smile: 1, grin: 1, eyes: 0, aB: [70, 10] };
    const slap = Math.max(0, Math.sin(lt * 9));
    mp.aF = me.reach(mp, 500 + 20 * slap, 1062); me.pose(mp);
    const bp = { x: 700, y: 1236, s: 1.2, f: -1, torso: -2 - laugh * 4, head: -4 - laugh * 5, lF: [-2, 88], lB: [2, 92], t: lt, smile: 1, grin: 1, eyes: lt % 1.2 < 0.6 ? 0 : null };
    bp.aF = bk.reach(bp, 566 - 20 * slap, 1064); bp.aB = [70, 40];
    bk.pose(bp);
    popSquash(yr.el, lt, 0.15); cal.update(lt, 4, lt < 0.6);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "ทุกปีพอเที่ยงคืนวันเกิด ข้อความแรกที่เด้งขึ้นมา จะเป็นของแบงค์เสมอ": a deck of ten years of midnight wishes
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.4, 12], ['mid', 1, 12]]);
  const room = myRoom(S), L = t => t - A;
  S.L.far.el.style.filter = 'blur(12px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(12px) brightness(0.5) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 200, 1080, 1400], 16, 711, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const clock = clock7(S.ui, 56, 110, 'เที่ยงคืนวันเกิด');
  const t0 = L(P.A4), t1 = L(P.A5) - 0.12;
  const times = YEARS.map((_, i) => t0 + (t1 - t0) * Math.pow(i / (YEARS.length - 1), 0.85));
  const deck = notifDeck(S.ui, 90, 420, 900, YEARS);
  const yl = yearLine7(S.ui, 120, 790, 840, YEARS);
  const streak = chip7(S.ui, 230, 960, 'แบงค์ทักเป็นคนแรก <b>ทุกปี</b>', 'streak7');
  const hb = heartBeat(streak.slot, 58);
  const spark = burst(back, 540, 1000, L(P.A5) + 0.05, 22, 713, ['#ffd66b', '#ffffff', '#ff9fc0'], 360, 1.0);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    room.update(lt + 3); bok(lt);
    clock.update(lt, 0.05, L(P.A4) - 0.35);
    deck.update(lt, times);
    yl.update(lt, L(P.A4) - 0.3, times);
    popSquash(streak.el, lt, L(P.A5) + 0.05); hb.update(lt);
    spark(lt);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "ปีนี้ก็เหมือนเดิม ทั้งที่ไม่ได้คุยกันมาเกือบปี"
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = myRoom(S), L = t => t - A;
  const me = new Puppet(set.people, ME, S.L.mid.defs); const ph = phoneProp(me.prop);
  const back = behindSvg(S);
  const conf = burst(back, 540, 260, L(P.A6) + 0.15, 22, 721, ['#ffd66b', '#ffffff', '#ff9fc0', '#7fd6c7'], 320, 1.1);
  const nt = bdayNotif(S.ui, 110, 150, 860, 'ปีนี้');
  const far = chip7(S.ui, 230, 380, 'ไม่ได้คุยกันมา<b>เกือบปี</b>', 'long7');
  const fcal = calendarFlip(far.slot, 58, '#e0574b');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam(CAM_ROOM(k, 0.04));
    set.update(lt + 4);
    const fade = ease.inOutSine(prog(lt, L(P.A7) - 0.1, L(P.A7) + 0.5));
    const p = mePose(me, lt, { smile: lerp(0.95, 0.25, fade), grin: lt > L(P.A6) + 0.2 && fade < 0.3 ? 1 : 0, head: lerp(4, 16, fade) + Math.sin(lt * 1.2) * 2, torso: lerp(0, 6, fade) });
    const [px, py] = toWorld(p, ...torsoPt(p, 78, -RIG.T + 40));
    ph.scr.setAttribute('fill', lt > L(P.A6) ? '#ffe4ee' : '#cfe4ff');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    const kn = spring(lt, L(P.A6), 13, 6);
    nt.style.opacity = fadeIn(lt, L(P.A6), 0.12);
    nt.style.transform = `translateY(${((1 - kn) * -220).toFixed(1)}px)`;
    flicker(nt, lt);
    conf(lt);
    popSquash(far.el, lt, L(P.A8) - 0.05); fcal.update(lt, 11, lt < L(P.A8) + 0.5);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — he scrolls up: the message before today's was แบงค์'s หมูกระทะ invite, 8 months ago — read, never answered
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.04) contrast(1.04)';
  const set = myRoom(S), L = t => t - A;
  const me = new Puppet(set.people, ME, S.L.mid.defs); const ph = phoneProp(me.prop);
  const sweat = sweatDrop(set.top);
  const items = [
    { k: 'date', text: '2 ปีก่อน' }, { k: 'L', text: 'สุขสันต์วันเกิดนะเพื่อน', meta: '00:00' }, { k: 'R', text: 'ขอบใจ', meta: '10:42' },
    { k: 'date', text: 'ปีที่แล้ว' }, { k: 'L', text: 'สุขสันต์วันเกิดนะเพื่อน', meta: '00:00' }, { k: 'R', text: 'ขอบใจ', meta: '11:15' },
    { k: 'date', text: '8 เดือนก่อน' }, { k: 'L', text: 'ว่างเมื่อไหร่ไปกินหมูกระทะกัน', meta: '19:20' }, { k: 'stk', html: mookrataSticker(200) },
    { k: 'date', text: 'วันนี้' }, { k: 'L', text: 'สุขสันต์วันเกิดนะเพื่อน', meta: '00:00' },
  ];
  const chat = chatThread7(S.ui, 420, 110, 620, 860, 'แบงค์', bankAv(64), items); chat.el.classList.add('big7');
  const [dOld, invite, stk] = [chat.items[6], chat.items[7], chat.items[8]];
  invite.meta.classList.add('read7');
  const stamp = html('div', 'stamp big', chat.el.querySelector('.cbody')); stamp.textContent = 'ไม่ได้ตอบ';
  Object.assign(stamp.style, { right: '40px', left: 'auto', top: '0px', opacity: 0, transformOrigin: '50% 50%' });
  const hand = html('div', 'swipeHand', S.ui); hand.innerHTML = '<svg width="110" height="126" viewBox="0 0 74 90"><path d="M24,40 L24,10 Q24,2 31,2 Q38,2 38,10 L38,34 L40,30 Q46,26 50,32 L52,36 Q58,32 62,38 L63,42 Q69,40 71,46 L71,64 Q71,86 50,88 L36,88 Q22,86 14,72 L4,52 Q2,44 9,42 Q14,41 18,48 L24,58 Z" fill="#ffd9b8" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>';
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(44, 64, k), y: lerp(-300, -330, k), z: lerp(1.24, 1.28, k), fx: 460, fy: 1250 });
    set.update(lt + 6);
    const lean = ease.inOutSine(prog(lt, L(P.B2) - 0.2, L(P.B2) + 0.3));
    const cringe = ease.inOutSine(prog(lt, L(P.B6) - 0.1, L(P.B6) + 0.3));
    const p = mePose(me, lt, { smile: lerp(0.4, -0.1, cringe), head: lerp(8, 2, lean) + lerp(0, 14, cringe) + Math.sin(lt * 1.2) * 1.5, torso: lerp(2, 8, lean) + cringe * 4, tap: lt > L(P.B0) && lt < L(P.B1) ? Math.max(0, Math.sin(lt * 8)) * 0.7 : 0 });
    const [px, py] = toWorld(p, ...torsoPt(p, 78, -RIG.T + 40));
    ph.scr.setAttribute('fill', '#ffe9d6');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    const [hx, hy] = toWorld(p, ...torsoPt(p, HEAD_C[0] + 66, HEAD_C[1] - 46));
    sweat(lt, L(P.B6) + 0.15, hx, hy);
    enter3d(chat.el, lt, 0.05, 'pop');
    const sc = 120 * ease.inOutCubic(prog(lt, L(P.B0) + 0.15, L(P.B1) + 0.2));
    const lay = chat.update(lt, sc);
    const hk = prog(lt, L(P.B0) - 0.05, L(P.B1) + 0.35);
    hand.style.opacity = hk > 0 && hk < 1 ? Math.min(1, Math.sin(Math.PI * hk) * 2).toFixed(3) : 0;
    hand.style.transform = `translate(${(760).toFixed(1)}px, ${(360 + ease.inOutCubic(prog(hk, 0.15, 0.75)) * 200).toFixed(1)}px) rotate(-8deg)`;
    invite.el.classList.toggle('glow', lt > L(P.B2) - 0.05);
    stk.el.style.transform = lt > L(P.B3) ? `rotate(${(Math.sin((lt - L(P.B3)) * 8) * 5 * Math.exp(-(lt - L(P.B3)) * 1.5)).toFixed(2)}deg)` : '';
    dOld.el.classList.toggle('hot', lt > L(P.B4) - 0.05);
    dOld.el.style.transform = `scale(${(1 + 0.25 * Math.exp(-Math.pow((lt - L(P.B4) - 0.05) * 8, 2))).toFixed(3)})`;
    invite.meta.textContent = lt > L(P.B5) ? 'อ่านแล้ว' : '19:20';
    invite.meta.style.transform = `scale(${(1 + 0.4 * Math.exp(-Math.pow((lt - L(P.B5) - 0.05) * 8, 2))).toFixed(3)})`;
    // "ไม่ได้ตอบ" stamp slams over the sticker
    const ks = spring(lt, L(P.B6) + 0.05, 18, 6);
    stamp.style.top = ((stk.y || 0) - Math.max(0, lay.content - lay.view) + sc + 50).toFixed(1) + 'px';
    stamp.style.opacity = fadeIn(lt, L(P.B6) + 0.05, 0.06);
    stamp.style.transform = `rotate(-12deg) scale(${(2.2 - 1.2 * ks).toFixed(3)})`;
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
  S.chat = chat;
})();

// =====================================================================
// S5 — "แล้วเขาก็นึกขึ้นได้ 11 ปีมานี้ เขาไม่เคยจำวันเกิดแบงค์ได้เลยสักปี"
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.03) contrast(1.04)';
  const set = myRoom(S), L = t => t - A;
  const me = new Puppet(set.people, ME, S.L.mid.defs);
  const bed = phoneProp(set.people); bed.g.setAttribute('transform', 'translate(170,1168) rotate(-90) scale(1.1)'); bed.scr.setAttribute('fill', '#ffe9d6');
  set.people.insertBefore(bed.g, set.people.firstChild);
  const bulb = bulb7(set.top);
  const sweat = sweatDrop(set.top);
  const card = scoreCard7(S.ui, 70, 120, 940);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam(CAM_ROOM(k));
    set.update(lt + 8);
    const up = lt > L(P.Cst) && lt < L(P.C2);
    const palm = ease.inOutSine(prog(lt, L(P.C4) - 0.25, L(P.C4) + 0.1));
    const p = mePose(me, lt, { phone: false, smile: up ? 0.3 : lerp(0.2, -0.1, palm), mouthO: up && lt < L(P.C1) + 0.3 ? 1 : 0, head: up ? -6 : lerp(6, 18, palm) + Math.sin(lt * 1.2) * 2, torso: up ? -4 : lerp(2, 10, palm), eyes: palm > 0.6 ? 0 : null, palm });
    const [hx, hy] = toWorld(p, ...torsoPt(p, HEAD_C[0] + 10, HEAD_C[1] - 120));
    bulb(lt, L(P.Cst) + 0.05, hx, hy);
    set.top.firstChild.style.opacity = (1 - prog(lt, L(P.C1) - 0.4, L(P.C1) - 0.1)).toFixed(3);
    const [sx, sy] = toWorld(p, ...torsoPt(p, HEAD_C[0] + 66, HEAD_C[1] - 46));
    sweat(lt, L(P.C4) + 0.2, sx, sy);
    card.update(lt, L(P.C1) - 0.25, L(P.C1), L(P.C1b) + 0.15, L(P.C2), L(P.C4));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — "พอเปิดดูโปรไฟล์ วันเกิดแบงค์คือพรุ่งนี้"
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.05) contrast(1.04)';
  const set = myRoom(S), L = t => t - A;
  const me = new Puppet(set.people, ME, S.L.mid.defs); const ph = phoneProp(me.prop);
  const back = behindSvg(S);
  const spark = burst(back, 640, 470, L(P.C7) + 0.05, 20, 731, ['#ffd66b', '#ffffff', '#ff7b6e'], 300, 0.9);
  const prof = profile7(S.ui, 190, 100, 700);
  const today = todayChip7(S.ui, 560, 600);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    const jolt = lt > L(P.C7) && lt < L(P.C7) + 0.3 ? Math.sin((lt - L(P.C7)) * 60) * 6 * (1 - prog(lt, L(P.C7), L(P.C7) + 0.3)) : 0;
    S.cam(Object.assign(CAM_ROOM(k), { x: lerp(-20, 0, k) + jolt }));
    set.update(lt + 10);
    const shock = ease.outBack(prog(lt, L(P.C7) - 0.05, L(P.C7) + 0.25));
    const p = mePose(me, lt, { smile: lerp(0.4, 0.2, shock), mouthO: shock > 0.5 ? 1 : 0, head: lerp(10, -8, shock) + Math.sin(lt * 1.2) * 2, torso: lerp(4, -8, shock), tap: lt < L(P.C6) ? Math.max(0, Math.sin(lt * 8)) * 0.6 : 0 });
    const [px, py] = toWorld(p, ...torsoPt(p, 78, -RIG.T + 40));
    ph.scr.setAttribute('fill', '#ffe4ee');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    prof.update(lt, 0.1, L(P.C6) + 0.2, L(P.C7));
    today.update(lt, L(P.C6) + 0.6);
    spark(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — title: 11 ปี / ที่เพื่อนไม่เคยลืม
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = myRoom(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 741, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ph = html('div', 'title', wrap); ph.style.top = '250px';
  const psv = svg('svg', { width: 400, height: 400, viewBox: '0 0 260 260', style: 'overflow:visible;filter:drop-shadow(0 24px 30px rgba(0,0,0,.45))' }, ph);
  schoolPhoto(psv, 20, 30, 220);
  const t1 = html('div', 'title', wrap); t1.style.top = '700px'; t1.style.font = '700 200px/1 Kanit';
  const digits = ['1', '1'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ปี'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่เพื่อนไม่เคยลืม'); t2.style.top = '930px'; t2.style.font = '600 104px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5); bok(lt);
    popSquash(ph, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 3).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.4, 14, 7); unit.style.opacity = fadeIn(lt, 0.4, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — split: he waits for 00:00 and sends first; แบงค์'s phone lights up, he grins and replies
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const L = t => t - A;
  const tSend = L(P.D4), tRep1 = tSend + 0.95, tRep2 = tSend + 1.65, tRep3 = tSend + 2.35;
  // top: his room
  const top = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  top.root.style.clipPath = 'inset(0 0 50% 0)'; top.grade = 'saturate(1.08) contrast(1.04)';
  const mset = myRoom(top);
  const me = new Puppet(mset.people, ME, top.L.mid.defs); const mph = phoneProp(me.prop);
  const clock = clock7(top.ui, 40, 60, 'คืนวันเกิดแบงค์');
  const chat = chatThread7(top.ui, 560, 40, 480, 870, 'แบงค์', bankAv(64), [
    { k: 'L', text: 'สุขสันต์วันเกิดนะเพื่อน', meta: 'เมื่อวาน' }, { k: 'R', text: 'ขอบใจ', meta: 'เมื่อวาน' },
    { k: 'R', text: 'สุขสันต์วันเกิดนะเพื่อน', meta: '00:00', t0: tSend },
    { k: 'L', text: 'เฮ้ย! จำได้ด้วย', t0: tRep1 }, { k: 'L', text: 'หมูกระทะเสาร์นี้ เลี้ยงเอง', t0: tRep2 }, { k: 'R', text: 'ไป!!', t0: tRep3 },
  ], true);
  const first = firstBadge7(top.ui, 300, 196);
  top.update = lt => {
    top.cam({ x: 10, y: 530, z: 1.1, fx: 400, fy: 1000 });
    mset.update(lt + 12);
    const typing = lt > L(P.D3) && lt < tSend - 0.1;
    const yay = lt > tRep1;
    const p = mePose(me, lt, { smile: yay ? 1 : 0.6, grin: yay ? 1 : 0, head: yay ? 2 : 12, torso: yay ? -4 : 4, tap: typing ? Math.max(0, Math.sin(lt * 18)) : 0 });
    const [px, py] = toWorld(p, ...torsoPt(p, 78, -RIG.T + 40));
    mph.scr.setAttribute('fill', '#cfe4ff');
    setA(mset.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    clock.update(lt, 0.05, L(P.D2) + 0.1);
    enter3d(chat.el, lt, 0.1, 'pop');
    chat.update(lt);
    chat.type(lt, [{ t0: L(P.D3), t1: tSend - 0.2, text: 'สุขสันต์วันเกิดนะเพื่อน', mode: 'type' }, { t0: tSend - 0.05, t1: tSend, text: '', mode: 'hold' }]);
    first.update(lt, tSend + 0.3);
    setGrade(top, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(top);
  // bottom: แบงค์'s room, another city
  const bot = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  bot.root.style.clipPath = 'inset(50% 0 0 0)'; bot.grade = 'saturate(1.08) contrast(1.03)';
  const bset = bankRoom(bot);
  const hearts = heartsRise(svg('g', {}, bset.people), 560, 1120, tSend + 0.7, 10, 751, 0.25);
  const bk = new Puppet(bset.people, BANK, bot.L.mid.defs); const bph = phoneProp(bk.prop, '#e0574b');
  const ban = bdayNotif(bot.ui, 30, 996, 640, null, 'ต้น', meAv(96)); ban.classList.add('narrow');
  bot.update = lt => {
    bot.cam({ x: -100, y: -200, z: 1.15, fx: 600, fy: 1000 });
    bset.update(lt + 4);
    hearts(lt);
    const ping = lt > tSend + 0.25, wow = ping && lt < tSend + 0.7, yay = lt > tSend + 0.7;
    const pose = { x: 700, y: 1196, s: 1.2, f: -1, torso: yay ? -6 : 4, head: wow ? -10 : yay ? 0 : 10 + Math.sin(lt * 1.3) * 2, lF: [-2, 88], lB: [2, 92], t: lt + 3, smile: yay ? 1 : 0.4, grin: yay ? 1 : 0, mouthO: wow ? 1 : 0 };
    const [px, py] = holdPhone(bk, pose, 78, -RIG.T + 40, yay && lt < tRep2 ? Math.max(0, Math.sin(lt * 18)) : 0);
    bk.pose(pose);
    bph.scr.setAttribute('fill', ping ? '#ffe4ee' : '#cfe4ff');
    setA(bset.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: ping ? 1 : 0.5 });
    const kn = spring(lt, tSend + 0.25, 13, 6);
    ban.style.opacity = fadeIn(lt, tSend + 0.25, 0.12);
    ban.style.transform = `translateY(${((1 - kn) * -200).toFixed(1)}px)`;
    flicker(ban, lt);
    setGrade(bot, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(bot);
  const seam = new Shot(A, B, []);
  const line = html('div', '', seam.ui); Object.assign(line.style, { position: 'absolute', left: 0, right: 0, top: '954px', height: '12px', background: 'linear-gradient(90deg,#ffd66b,#f07aa8,#ffd66b)', boxShadow: '0 0 24px rgba(255,214,107,.8)' });
  seam.update = lt => { line.style.opacity = (0.75 + 0.25 * Math.sin(lt * 5)).toFixed(3); };
  SHOTS.push(seam);
})();

// =====================================================================
// S9 — "แต่อย่าให้เป็นฝ่ายเดียวที่จำ": หมูกระทะ together, glasses up
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  S.grade = 'saturate(1.12) contrast(1.03) brightness(1.03)';
  const set = mookrata(S), L = t => t - A;
  const me = new Puppet(set.people, ME, S.L.mid.defs);
  const bk = new Puppet(set.people, BANK, S.L.mid.defs);
  const glass = pup => { const g = svg('g', {}, pup.prop); svg('path', { d: 'M-15,-52 L15,-52 L12,8 L-12,8 Z', fill: '#f6c86a', opacity: 0.92, stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g); svg('path', { d: 'M-15,-52 L15,-52 L14,-40 L-14,-40 Z', fill: '#fff8ea' }, g); return g; };
  glass(me); glass(bk);
  S.L.mid.s.appendChild(set.top);
  const fxs = fxSvg(S);
  const leak = lightLeak(S.fx);
  const tClink = L(P.D7) - 0.05;
  const camAt = lt => { const k = ease.inOutSine(prog(lt, 0, B - A)); return { x: 0, y: lerp(220, 236, k), z: lerp(1.5, 1.58, k), fx: 540, fy: 1000 }; };
  const clinkBurst = burst(fxs, ...toScreen(camAt(tClink), 1, 540, 990), tClink, 22, 761, ['#ffd66b', '#ffffff', '#ff9fc0'], 300, 0.9);
  S.update = lt => {
    S.cam(camAt(lt));
    set.update(lt);
    const lift = ease.inOutCubic(prog(lt, tClink - 0.5, tClink));
    const laugh = Math.sin(lt * 10);
    const mp = { x: 350, y: 1210, s: 1.25, f: 1, torso: 4 + laugh * 1.5, head: 4 + laugh * 2, lF: [-2, 88], lB: [2, 92], t: lt, smile: 1, grin: 1, eyes: lt > tClink ? 0 : null };
    const bp = { x: 730, y: 1210, s: 1.25, f: -1, torso: -2 - laugh * 2, head: -2 - laugh * 3, lF: [-2, 88], lB: [2, 92], t: lt + 2, smile: 1, grin: 1, eyes: lt > tClink + 0.1 ? 0 : null };
    mp.aF = me.reach(mp, lerp(430, 520, lift), lerp(1120, 1020, lift)); mp.aB = [74, 10];
    bp.aF = bk.reach(bp, lerp(650, 560, lift), lerp(1120, 1020, lift)); bp.aB = [74, 10];
    mp.propRot = lerp(0, 14, lift); bp.propRot = lerp(0, 14, lift);
    me.pose(mp); bk.pose(bp);
    clinkBurst(lt);
    leak(lt, 0.25 + 0.35 * prog(lt, tClink, tClink + 0.5));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S10 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s10;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#6a4a6e'], [0.6, '#352440'], [1, '#170f1f']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 771, { color: '#ffe2a8', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 400, 0.3, 18, 773, ['#ffd66b', '#ffffff', '#ff9fc0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '300px';
  duo.innerHTML = `<span class="duo7">${meAv(200)}</span><span class="duo7h"><svg width="90" height="90" viewBox="-30 -30 60 60"><path d="${heartPath(0, 0, 18)}" fill="#f04f7f" stroke="#fff" stroke-width="4"/></svg></span><span class="duo7">${bankAv(200)}</span>`;
  duo.style.display = 'flex'; duo.style.justifyContent = 'center'; duo.style.alignItems = 'center'; duo.style.gap = '6px';
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const hrt = duo.querySelector('.duo7h');
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['1', '1'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ปี'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่เพื่อนไม่เคยลืม'); t2.style.top = '808px'; t2.style.font = '600 96px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'คืนนี้ลองเป็นฝ่ายทักก่อนดูนะ'); sub.style.top = '975px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้เพื่อนที่ไม่ได้คุยกันนาน</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
    hrt.style.transform = `scale(${(1 + 0.16 * Math.exp(-Math.pow(((lt % 0.9) - 0.08) * 18, 2))).toFixed(3)})`;
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.6, 14, 7); unit.style.opacity = fadeIn(lt, 0.6, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.9, fl(SC.s2[0]) * 0.9, fl(SC.s3[0]) * 0.6, fl(SC.s4[0]) * 0.4, fl(SC.s5[0]) * 0.4, fl(SC.s7[0]), fl(SC.s8[0]) * 0.8, fl(SC.s9[0]) * 0.8, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
