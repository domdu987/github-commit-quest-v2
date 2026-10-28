// "39 บาทที่แม่ไม่กล้ากด" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D5; H is the "ถ้า..." hook).
// Shot language: each scene is a shot list (wide → medium → close-up / insert) on a lit set; see pro.js.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0a: [0, P.H2 - 0.1], s0b: [P.H2 - 0.1, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3], s3: [P.C0 - 0.3, P.C6 - 0.15],
  s3b: [P.C6 - 0.15, P.title], s4: [P.title, P.D0 - 0.1], s5: [P.D0 - 0.1, P.D3 - 0.05], s6: [P.D3 - 0.05, P.end], s7: [P.end, DURATION] };
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
const HW = (x, y, s, f = 1) => [x + f * s * HEAD_C[0], y + s * HEAD_C[1]];
// light the cast: rim + core shade on the people layer, a cast shadow for each puppet on the wall behind
function lightCast(S, set, pups, o = {}) {
  const Lt = set.light || {};
  set.people.setAttribute('filter', charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {})));
  return pups.map(p => castShadow(p, set.shadowL, S.L.mid.defs, Object.assign({ lx: Lt.lx }, o.shadow || {})));
}
const ROOM_P = { x: 330, y: 1172, s: 1.2 }, H_FAI_ROOM = HW(330, 1172, 1.2);
function faiBed(pup, lt, o = {}) {
  const pose = Object.assign({ x: ROOM_P.x, y: ROOM_P.y, s: ROOM_P.s, f: 1, torso: 4, head: 12 + Math.sin(lt * 1.2) * 2, lF: [-2, 88], lB: [2, 92], t: lt + 1, smile: 0.6 }, o);
  const p = holdPhone(pup, pose, 78, -RIG.T + 40, o.tap || 0);
  pup.pose(pose);
  return [pose, p];
}
// mom's living room: the two of them on the reed mat
const FAI_M = { x: 370, y: 1432, s: 1.2 }, MOM_M = { x: 700, y: 1432, s: 1.2 };
const H_FAI_M = HW(370, 1432, 1.2), H_MOM_M = HW(700, 1432, 1.2, -1);
const SIT = { lF: [8, 172], lB: [18, 166] };
function faiFloor(pup, lt, o = {}) {
  const pose = Object.assign({ x: FAI_M.x, y: FAI_M.y, s: FAI_M.s, f: 1, torso: 8, head: 14 + Math.sin(lt * 1.2) * 1.5, lF: SIT.lF, lB: SIT.lB, t: lt + 1, smile: 0.5 }, o);
  const p = holdPhone(pup, pose, 74, -RIG.T + 44, o.tap || 0);
  pup.pose(pose);
  return [pose, p];
}
function momFloor(pup, lt, o = {}) {
  const pose = Object.assign({ x: MOM_M.x, y: MOM_M.y, s: MOM_M.s, f: -1, torso: 6, head: 10 + Math.sin(lt * 1.1) * 1.5, lF: SIT.lF, lB: SIT.lB, t: lt + 4, smile: 0.5, aF: [70, 30], aB: [74, 34] }, o);
  pup.pose(pose);
  return pose;
}
// a walk cycle blended into sitting down on the floor: u in [0,1] is the sit-down progress
function walkSit(pup, base, lt, xNow, walking, u) {
  const ph = lt * 9.5, s = base.s, standY = 1458 - LEG * s;
  const sw = walking ? 1 : 0;
  const tF = 90 + sw * 24 * Math.sin(ph), tB = 90 - sw * 24 * Math.sin(ph);
  const kF = tF + sw * Math.max(0, 34 * Math.sin(ph - 1.3)), kB = tB + sw * Math.max(0, 34 * Math.sin(ph + Math.PI - 1.3));
  const k = ease.inOutSine(u);
  return Object.assign({}, base, {
    x: xNow, y: lerp(standY - sw * 5 * Math.abs(Math.cos(ph)), base.y, k),
    lF: [lerp(tF, SIT.lF[0], k), lerp(kF, SIT.lF[1], k)], lB: [lerp(tB, SIT.lB[0], k), lerp(kB, SIT.lB[1], k)],
    torso: lerp(4 + sw * 3, base.torso, k),
  });
}

// =====================================================================
// S0a — hook, ฝ้าย: "ถ้าคุณกดสั่งของวัน 11.11 ได้โดยไม่ต้องคิด" — her cart fills without a thought
// =====================================================================
(() => {
  const [A, B] = SC.s0a;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = faiRoom(S), L = t => t - A;
  const fai = new Puppet(set.people, FAI, S.L.mid.defs); const ph = phoneProp(fai.prop, '#4a7bd8');
  lightCast(S, set, [fai], { light: { rim: '#ffe0b0' } });
  const mine = cartChip2(S.ui, 40, 120, 'ตะกร้าของฝ้าย');
  const shots = [
    { t: 0, cam: frameAt(480, 1150, 1.12, 540, 1070), to: frameAt(470, 1140, 1.18, 540, 1070) },
    { t: L(P.H1) - 0.15, cam: frameAt(H_FAI_ROOM[0] + 70, H_FAI_ROOM[1] + 110, 1.6, 400, 1180), to: frameAt(H_FAI_ROOM[0] + 70, H_FAI_ROOM[1] + 100, 1.7, 400, 1180) },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt);
    const [pose, [px, py]] = faiBed(fai, lt, { smile: 0.85, grin: lt > L(P.H1) ? 1 : 0, head: 12 + Math.sin(lt * 1.2) * 2, tap: Math.max(0, Math.sin(lt * 16)) });
    ph.scr.setAttribute('fill', '#ffe9d6');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    const r = rollValue(lt, L(P.H0) + 0.1, L(P.H1) + 0.5, 0, 12);
    mine.update(lt, L(P.H0), r.v, r.speed);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S0b — hook, แม่: "ถ้าแม่มีของอยู่ชิ้นเดียวในตะกร้า เขาคิดมาแล้วทั้งปี" — her thumb creeps toward the button, then pulls back
// =====================================================================
(() => {
  const [A, B] = SC.s0b;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.04) contrast(1.04)';
  const set = momHouse(S, 'night'), L = t => t - A;
  const mom = new Puppet(set.people, MOM9, S.L.mid.defs); const ph = phoneProp(mom.prop, '#c4566f');
  lightCast(S, set, [mom], { light: { rim: '#fff4dc', rimOp: 0.6 }, shadow: { op: 0.13, blur: 11, k: 0.22 } });
  const momc = cartCard9(S.ui, 330, 230, 600, 'ตะกร้าของแม่', mom9Av(72), [[`<span class="ic5">${slippersSVG(64)}</span>`, 'รองเท้าแตะ', '฿39']]);
  const year = chip7(S.ui, 380, 470, 'ค้างในตะกร้ามา <b>1 ปี</b>', 'long7');
  const ycal = calendarFlip(year.slot, 58, '#e0574b');
  const H = HW(600, 1432, 1.2, -1);
  const shots = [
    { t: 0, cam: frameAt(600, 1270, 1.3, 560, 1260), to: frameAt(600, 1260, 1.38, 560, 1260) },
    { t: L(P.H4) - 0.05, cam: frameAt(H[0] - 40, H[1] + 40, 2.0, 560, 1260), to: frameAt(H[0] - 40, H[1] + 40, 2.12, 560, 1260) },
  ];
  S.update = lt => {
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt, 21.6, cam);
    const sigh = ease.inOutSine(prog(lt, L(P.H4) + 0.2, L(P.H4) + 0.9));
    const pose = { x: 600, y: 1432, s: 1.2, f: -1, torso: lerp(10, 16, sigh), head: lerp(14, 26, sigh) + Math.sin(lt * 1.1) * 1.2, lF: SIT.lF, lB: SIT.lB, t: lt + 4, smile: lerp(0.45, 0.3, sigh) };
    const hover = lt > 0.6 && lt < L(P.H4) ? Math.max(0, Math.sin((lt - 0.6) * 2.2)) : 0;
    const [px, py] = holdPhone(mom, pose, lerp(74, 60, sigh), -RIG.T + lerp(44, 70, sigh), -hover * 0.6);
    mom.pose(pose);
    ph.scr.setAttribute('fill', '#ffe9d6');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: (1 - 0.5 * sigh).toFixed(3) });
    momc.update(lt, 0.05, [0.3]);
    popSquash(year.el, lt, L(P.H4) + 0.05); ycal.update(lt, 1, lt < L(P.H4) + 0.6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — 11.11 at midnight: twelve things in the cart without a thought; then แม่'s LINE: "ช่วยสั่งของให้แม่หน่อย แม่กดไม่เป็น"
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) contrast(1.04)';
  const set = faiRoom(S), L = t => t - A;
  const fai = new Puppet(set.people, FAI, S.L.mid.defs); const ph = phoneProp(fai.prop, '#4a7bd8');
  lightCast(S, set, [fai], { light: { rim: '#ffe0b0' } });
  const badge = saleBadge2(S.ui, 40, 100);
  const grid = saleGrid(S.ui, 440, 110, 560);
  const cnt = cartChip2(S.ui, 40, 300, 'ใส่ตะกร้า');
  const back = behindSvg(S);
  const spark = burst(back, 160, 160, L(P.A0) + 0.1, 22, 911, ['#ff8a5a', '#ffd66b', '#ffffff', '#ff4d6d'], 300, 1.0);
  const banner = lineBanner2(S.ui, 120, 'ช่วยสั่งของให้แม่หน่อย แม่กดไม่เป็น');
  const adds = [L(P.A3), L(P.A3) + 0.45, L(P.A3) + 0.9, L(P.A2) - 0.25, L(P.A2) + 0.15, L(P.A2) + 0.55];
  const shots = [
    { t: 0, cam: frameAt(480, 1150, 1.12, 540, 1080), to: frameAt(470, 1140, 1.17, 540, 1080) },
    { t: L(P.A3) - 0.1, cam: frameAt(H_FAI_ROOM[0] + 60, H_FAI_ROOM[1] + 120, 1.55, 300, 1200), to: frameAt(H_FAI_ROOM[0] + 60, H_FAI_ROOM[1] + 110, 1.62, 300, 1200) },
    { t: L(P.A5) + 0.02, cam: frameAt(H_FAI_ROOM[0] + 40, H_FAI_ROOM[1] + 40, 2.1, 420, 1240), to: frameAt(H_FAI_ROOM[0] + 40, H_FAI_ROOM[1] + 40, 2.3, 420, 1240) },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 2);
    const ping = lt > L(P.A5);
    const [pose, [px, py]] = faiBed(fai, lt, { smile: ping ? 0.5 : 0.95, grin: !ping && lt > L(P.A2) && lt < L(P.A4) ? 1 : 0, head: ping ? 2 : 14 + Math.sin(lt * 1.2) * 2, torso: ping ? 0 : 4, tap: !ping ? Math.max(0, Math.sin(lt * 14)) : 0, mouthO: ping && lt < L(P.A5) + 0.6 ? 0.8 : 0 });
    ph.scr.setAttribute('fill', ping ? '#dff7e7' : '#ffe0d0');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    badge.update(lt, L(P.A0) + 0.02); spark(lt);
    grid.update(lt, L(P.A1) - 0.2, adds);
    const r = rollValue(lt, L(P.A2) - 0.3, L(P.A2) + 0.7, 0, 12);
    cnt.update(lt, L(P.A2) - 0.35, r.v, r.speed);
    const out = ease.inCubic(prog(lt, L(P.A5) - 0.35, L(P.A5) - 0.05));
    for (const e of [badge.el, grid.c.c, cnt.el]) e.style.opacity = (parseFloat(e.style.opacity || 1) * (1 - out)).toFixed(3);
    banner.update(lt, L(P.A5), L(P.A6) - 0.1);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — ฝ้าย walks into แม่'s room, sits down beside her and opens her app: one item, a pair of ฿39 slippers, added a year ago
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.05) contrast(1.04)';
  const set = momHouse(S, 'night'), L = t => t - A;
  const fai = new Puppet(set.people, FAI, S.L.mid.defs); const fph = phoneProp(fai.prop, '#c4566f');
  const mom = new Puppet(set.people, MOM9, S.L.mid.defs); const mph = phoneProp(mom.prop, '#c4566f');
  lightCast(S, set, [fai, mom], { light: { rim: '#fff4dc', rimOp: 0.6 }, shadow: { op: 0.13, blur: 11, k: 0.22 } });
  const cart = momCart9(S.ui, 120, 110, 840);
  const dateEl = cart.c.c.querySelector('.mc9d b');
  const mark = markerCircle(dateEl, 250, 70)(L(P.B3) + 0.3);
  const tWalk = 1.15, tSit = 1.65, tHand = 1.5;
  const shots = [
    { t: 0, cam: frameAt(520, 1250, 1.1, 540, 1170), to: frameAt(540, 1245, 1.14, 540, 1170) },
    { t: L(P.B1) - 0.05, cam: frameAt(540, 1250, 1.42, 540, 1270), to: frameAt(540, 1245, 1.5, 540, 1270) },
    { t: L(P.B4) - 0.1, cam: frameAt(H_MOM_M[0] - 30, H_MOM_M[1] + 40, 2.05, 600, 1260), to: frameAt(H_MOM_M[0] - 30, H_MOM_M[1] + 40, 2.18, 600, 1260) },
  ];
  S.update = lt => {
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt, 21.7, cam);
    const surprised = lt > L(P.B4) - 0.1;
    // ฝ้าย: walks in from the left, sits down, takes the phone
    const walking = lt < tWalk, u = prog(lt, tWalk, tSit);
    const xNow = lerp(-140, FAI_M.x, ease.outCubic(prog(lt, 0, tWalk)) * 0.4 + prog(lt, 0, tWalk) * 0.6);
    const base = { x: FAI_M.x, y: FAI_M.y, s: FAI_M.s, f: 1, torso: 8, head: 14 + Math.sin(lt * 1.2) * 1.5, t: lt + 1, smile: surprised ? 0.2 : 0.55, mouthO: lt > L(P.B5) - 0.1 && lt < L(P.B5) + 0.6 ? 0.8 : 0 };
    const fp = walkSit(fai, base, lt, xNow, walking, u);
    const hasPhone = lt > tHand + 0.15;
    if (hasPhone) holdPhone(fai, fp, 74, -RIG.T + 44, lt > L(P.B0) + 1.3 && lt < L(P.B1) + 0.5 ? Math.max(0, Math.sin(lt * 10)) * 0.6 : 0);
    else { fp.aF = [80, 70]; fp.aB = [96, 84]; }
    fai.pose(fp);
    fph.g.setAttribute('opacity', hasPhone ? 1 : 0);
    const [px, py] = toWorld(fp, ...torsoPt(fp, 74, -RIG.T + 44));
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: hasPhone ? 1 : 0 });
    fph.scr.setAttribute('fill', '#ffe9d6');
    // แม่: holds the phone out to her, then leans in to watch
    const mp = { x: MOM_M.x, y: MOM_M.y, s: MOM_M.s, f: -1, torso: hasPhone ? -2 : 8, head: hasPhone ? -14 : 6, lF: SIT.lF, lB: SIT.lB, t: lt + 4, smile: surprised ? 0.75 : 0.6 };
    if (!hasPhone) { const reachK = ease.inOutSine(prog(lt, 0.6, tHand)); const [hx, hy] = toWorld(mp, ...torsoPt(mp, lerp(70, 150, reachK), -RIG.T + 40)); mp.aF = mom.reach(mp, hx, hy); mp.aB = [74, 34]; mp.propRot = -12; }
    else { mp.aF = [70, 30]; mp.aB = [74, 34]; }
    mom.pose(mp);
    mph.g.setAttribute('opacity', hasPhone ? 0 : 1);
    cart.update(lt, L(P.B0) + 1.3, L(P.B1) + 0.2, L(P.B3) + 0.1, L(P.B5) + 0.05);
    mark(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "แม่ไม่กล้ากด": the shipping (฿40) outweighs the shoes (฿39) on the scale
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.04) contrast(1.04)';
  const set = momHouse(S, 'night'), L = t => t - A;
  const fai = new Puppet(set.people, FAI, S.L.mid.defs); const ph = phoneProp(fai.prop, '#c4566f');
  const mom = new Puppet(set.people, MOM9, S.L.mid.defs);
  lightCast(S, set, [fai, mom], { light: { rim: '#fff4dc', rimOp: 0.6 }, shadow: { op: 0.13, blur: 11, k: 0.22 } });
  const bal = balance9(S.ui, 110, 100, 860);
  const shots = [
    { t: 0, cam: frameAt(560, 1240, 1.36, 540, 1250), to: frameAt(580, 1240, 1.44, 540, 1250) },
    { t: L(P.C1) - 0.05, cam: frameAt(H_MOM_M[0] - 20, H_MOM_M[1] + 30, 2.15, 600, 1240), to: frameAt(H_MOM_M[0] - 20, H_MOM_M[1] + 30, 2.3, 600, 1240) },
    { t: L(P.C3) - 0.3, cam: frameAt(540, 1260, 1.16, 540, 1260), to: frameAt(540, 1255, 1.22, 540, 1260) },
  ];
  S.update = lt => {
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 3, 21.8, cam);
    const shy = lt < L(P.C1) + 0.1, down = lt > L(P.C1) + 0.1;
    momFloor(mom, lt, { smile: shy ? 0.7 : 0.35, head: shy ? 4 + Math.sin(lt * 3) * 3 : 22, torso: down ? 10 : 4, eyes: down && lt < L(P.C3) ? 0 : null });
    const [pose, [px, py]] = faiFloor(fai, lt, { smile: lt > L(P.C4) ? 0.15 : 0.4, head: lt > L(P.C1) ? -6 : 6, torso: 6 });
    ph.scr.setAttribute('fill', '#ffe9d6');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 0.8 });
    bal.update(lt, L(P.C3) - 0.2, L(P.C4) - 0.1, L(P.C5));
    bal.c.c.style.opacity = (parseFloat(bal.c.c.style.opacity || 0) * (1 - prog(lt, B - A - 0.25, B - A))).toFixed(3);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3b — insert at the front door: ฝ้าย's new sneakers, then แม่'s slippers held together with wire
// =====================================================================
(() => {
  const [A, B] = SC.s3b;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0]]);
  S.grade = 'saturate(1.02) contrast(1.06)';
  const set = doorSill(S), L = t => t - A;
  const tag = chip7(S.ui, 560, 820, 'ลวดมัดไว้', 'long7');
  tag.slot.innerHTML = `<span class="ic5"><svg width="54" height="54" viewBox="-27 -27 54 54"><path d="M-18,-6 q6,-12 12,0 t12,0 t12,0" fill="none" stroke="#6b7280" stroke-width="5" stroke-linecap="round"/><path d="M-18,6 q6,-12 12,0 t12,0 t12,0" fill="none" stroke="#9aa3b2" stroke-width="5" stroke-linecap="round"/></svg></span>`;
  const shots = [
    { t: 0, cam: frameAt(260, 1630, 2.1, 540, 1180), to: frameAt(700, 1640, 2.25, 540, 1180) },
    { t: L(P.C8) - 0.15, cam: frameAt(725, 1630, 3.1, 540, 1180), to: frameAt(725, 1630, 3.3, 540, 1180) },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A, { handheld: 0.6 }), { base: 2.5 });
    set.update(lt, L(P.C8) + 0.05);
    popSquash(tag.el, lt, L(P.C8) + 0.1, 'rotate(-5deg)');
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 39 บาท / ที่แม่ไม่กล้ากด
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = momHouse(S, 'night');
  S.L.far.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 931, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '400px'; ic.innerHTML = slippersSVG(300, { old: true });
  const t1 = html('div', 'title', wrap); t1.style.top = '700px'; t1.style.font = '700 200px/1 Kanit';
  const digits = ['3', '9'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'บาท'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่แม่ไม่กล้ากด'); t2.style.top = '930px'; t2.style.font = '600 110px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5); bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.4, 14, 7); unit.style.opacity = fadeIn(lt, 0.4, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — that night, back in her room, ฝ้าย orders two pairs and pays the shipping
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) contrast(1.04)';
  const set = faiRoom(S), L = t => t - A;
  const fai = new Puppet(set.people, FAI, S.L.mid.defs); const ph = phoneProp(fai.prop, '#c4566f');
  lightCast(S, set, [fai], { light: { rim: '#ffe0b0' } });
  const ord = orderCard9(S.ui, 130, 100, 820);
  const back = behindSvg(S);
  const tTap = L(P.D2) + 0.5, tOk = L(P.D2) + 0.7;
  const conf = burst(back, 540, 480, tOk, 24, 951, ['#ffd66b', '#ffffff', '#7fd6c7', '#ff9fc0'], 340, 1.1);
  const shots = [
    { t: 0, cam: frameAt(H_FAI_ROOM[0] + 90, H_FAI_ROOM[1] + 160, 1.36, 360, 1230), to: frameAt(H_FAI_ROOM[0] + 90, H_FAI_ROOM[1] + 150, 1.44, 360, 1230) },
    { t: tOk + 0.05, cam: frameAt(H_FAI_ROOM[0] + 40, H_FAI_ROOM[1] + 50, 1.95, 420, 1250), to: frameAt(H_FAI_ROOM[0] + 40, H_FAI_ROOM[1] + 50, 2.05, 420, 1250) },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 7);
    const done = lt > tOk;
    const [pose, [px, py]] = faiBed(fai, lt, { smile: done ? 1 : 0.7, grin: done ? 1 : 0, head: done ? 0 : 12, tap: !done ? Math.max(0, Math.sin(lt * 12)) : 0 });
    ph.scr.setAttribute('fill', done ? '#dff7e7' : '#ffe9d6');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: 1 });
    ord.update(lt, 0.1, L(P.D1), L(P.D2), tTap, tOk);
    conf(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — a few days later, morning: แม่'s feet in the new slippers (insert), then the two of them with the open parcel
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.12) contrast(1.03) brightness(1.04)';
  const set = momHouse(S, 'day'), L = t => t - A;
  const hearts = heartsRise(svg('g', {}, set.people), 560, 1120, L(P.D4), 10, 961, 0.3);
  const box = parcel9(set.people); box.setAttribute('transform', 'translate(860,1440) scale(1.1)');
  const fai = new Puppet(set.people, FAI, S.L.mid.defs);
  const mom = new Puppet(set.people, MOM9_NEW, S.L.mid.defs);
  lightCast(S, set, [fai, mom], { light: { rim: '#fff1c4', rimOp: 0.8 }, shadow: { k: 0.2, skewK: 0.02, op: 0.16, blur: 9 } });
  const fsF = footShadow(set.shadowL, S.L.mid.defs), fsM = footShadow(set.shadowL, S.L.mid.defs);
  const chip = chip7(S.ui, 370, 120, 'รองเท้าใหม่ของแม่ <b>2 คู่</b>', 'today7');
  chip.slot.innerHTML = `<span class="ic5">${slippersSVG(70)}</span>`;
  const later = chip7(S.ui, 40, 120, 'สามวันต่อมา', 'today7');
  const lcal = calendarFlip(later.slot, 58, '#4a7bd8');
  const leak = lightLeak(S.fx);
  const shots = [
    { t: 0, cam: frameAt(655, 1440, 5.4, 540, 1250), to: frameAt(655, 1440, 5.7, 540, 1250) },
    { t: L(P.D4) - 0.1, cam: frameAt(560, 1180, 1.12, 540, 1050), to: frameAt(560, 1170, 1.3, 540, 1050) },
  ];
  S.update = lt => {
    const cam = applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 9, 10.2, cam);
    hearts(lt);
    const tap = Math.max(0, Math.sin(lt * 6)) * prog(lt, 0.2, 0.6);
    // แม่ shows off the new slippers (front foot lifted, a little cheer); ฝ้าย claps
    const mp = { x: 680, y: 1220, s: 1.2, f: -1, torso: -4, head: -6 + Math.sin(lt * 2) * 2, lF: [lerp(90, 66, tap), lerp(90, 98, tap)], lB: [92, 90], t: lt + 4, smile: 1, grin: 1, aF: [-50 + Math.sin(lt * 5) * 6, -100], aB: [100, 110] };
    mom.pose(mp);
    const fp = { x: 430, y: 1220, s: 1.2, f: 1, torso: 4, head: 6, lF: [90, 90], lB: [92, 90], t: lt + 1, smile: 1, grin: 1, eyes: lt > 2.6 ? 0 : null };
    const clap = Math.abs(Math.sin(lt * 7)) * 14;
    const [cx, cy] = toWorld(fp, ...torsoPt(fp, 66, -RIG.T + 44));
    fp.aF = fai.reach(fp, cx + clap * 0.5, cy); fp.aB = fai.reach(fp, cx - clap * 0.5, cy + 4);
    fai.pose(fp);
    fsF(430, 1462, 170); fsM(680, 1462, 170);
    lcal.update(lt, 14, lt < 0.7); popSquash(later.el, lt, 0.1); later.el.style.opacity = (parseFloat(later.el.style.opacity) * (1 - prog(lt, L(P.D4) - 0.3, L(P.D4)))).toFixed(3);
    popSquash(chip.el, lt, L(P.D4) + 0.2);
    leak(lt, 0.3 + 0.2 * prog(lt, 0, B - A));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#6a4a6e'], [0.6, '#352440'], [1, '#170f1f']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 971, { color: '#ffe2a8', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 973, ['#ffd66b', '#ffffff', '#ff9fc0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '300px';
  duo.innerHTML = `<span class="duo7">${faiAv(190, { happy: true, grin: true })}</span><span class="duo7h">${slippersSVG(140)}</span><span class="duo7">${mom9Av(190, { happy: true })}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '6px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['3', '9'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'บาท'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่แม่ไม่กล้ากด'); t2.style.top = '808px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, '11.11 ปีนี้ ลองเปิดดูตะกร้าของแม่'); sub.style.top = '975px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่รอช็อป 11.11</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.6, fl(SC.s2[0]) * 0.6, fl(SC.s4[0]), fl(SC.s5[0]) * 0.6, fl(SC.s6[0]) * 0.9, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
