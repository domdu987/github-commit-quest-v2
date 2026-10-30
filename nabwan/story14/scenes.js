// "720 มื้อ ที่ครูซื้อเกิน" — scenes timed to the narration in vo.js (VO.P: H hook, A–C the past, the title, D–G today,
// F the lesson; T is ครูสมศรี's own line, G the narrator saying it to the girl). Bookends: the hook shows today's moment,
// G pays it off; the past is sepia and dissolves into the present on a matched close-up; the ending is a split screen.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3], s3: [P.C0 - 0.3, P.title], s4: [P.title, P.D0 - 0.1],
  s5: [P.D0 - 0.1, P.E0 - 0.1], s6: [P.E0 - 0.1, P.F0 - 0.3], s7: [P.F0 - 0.3, P.end], s8: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const SEPIA = 'sepia(0.5) saturate(0.92) contrast(1.03) brightness(1.04)';
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
function lightCast14(S, set, groups, pups, o = {}) {
  const Lt = set.light || {}, f = charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {}));
  groups.forEach(g => g.setAttribute('filter', f));
  return pups.map(p => castShadow(p, set.shadowL, S.L.mid.defs, Object.assign({ lx: Lt.lx }, o.shadow || {})));
}
function standP(pup, x, ground, s, f, o = {}) { const S = s * pup.o.s; return Object.assign({ x, y: ground - LEG * S, s, f, torso: 0, head: 0, lF: [88, 92], lB: [92, 88], aF: [96, 92], aB: [86, 92], smile: 0.6 }, o); }
function walkP(pup, x, ground, s, f, ph, o = {}) {
  const g = gait(ph, o.amp ?? 16), S = s * pup.o.s;
  const p = Object.assign({ x, y: ground - LEG * S + g.bob * S, s, f, head: -2, lF: g.lF, lB: g.lB, aF: g.aF, aB: g.aB, smile: 0.6 }, o);
  p.torso = g.torso + (o.lean || 0);
  return p;
}
// seated on a bench / chair: thighs forward, shins down, hands on the desk
function chairP(pup, x, seat, s, f, o = {}) { return Object.assign({ x, y: seat - 18, s, f, torso: 4, head: 4, lF: [4, 86], lB: [10, 92], aF: [40, -10], aB: [50, 0], smile: 0.6 }, o); }
function shotCamF(lt, shots, end, o = {}) {
  let i = 0; while (i + 1 < shots.length && lt >= shots[i + 1].t) i++;
  const endOf = j => (j + 1 < shots.length ? shots[j + 1].t : end);
  const at = j => { const sh = shots[j]; return lerpCam(sh.cam(lt), (sh.to || sh.cam)(lt), ease.inOutSine(prog(lt, sh.t, endOf(j)))); };
  let cam = at(i);
  if (shots[i].move && i > 0) cam = lerpCam(at(i - 1), cam, ease.inOutCubic(prog(lt, shots[i].t, shots[i].t + shots[i].move)));
  const hh = o.handheld ?? 1;
  cam.x += hh * (Math.sin(lt * 1.1) * 2.2 + Math.sin(lt * 2.7 + 1) * 1.1);
  cam.y += hh * (Math.sin(lt * 0.9 + 2) * 1.8 + Math.sin(lt * 2.3) * 0.9);
  cam.r = (cam.r || 0) + hh * Math.sin(lt * 0.7) * 0.12;
  cam.y = Math.max(cam.y, o.minY ?? 2);
  return cam;
}
const fA = (...a) => () => frameAt(...a);
// hands on the desk in front (both wrists), with a little motion; returns the front wrist
function handsOnDesk(pup, p, deskY, lt, eat = 0) {
  const f = p.f || 1, [sx] = torsoW(pup, p, 0, 0);
  const fx = p.x + f * (62 + Math.sin(lt * 7) * 6 * eat) * (p.s * pup.o.s), bx = p.x + f * 40 * (p.s * pup.o.s);
  const fy = deskY - 8 - Math.max(0, Math.sin(lt * 7)) * 46 * eat;
  p.aF = pup.reach(p, fx, fy); p.aB = pup.reach(p, bx, deskY - 4);
  return [fx, fy];
}
// a wooden chair pulled up beside the back desk (faces right); returns the group
function sideChair(g, x, seat, now) {
  const c = svg('g', {}, g), col = now ? '#3f6fb8' : '#a87040';
  svg('rect', { x: x - 50, y: seat, width: 100, height: 14, rx: 3, fill: col, stroke: INK, 'stroke-width': 4 }, c);
  svg('path', { d: `M${x - 52},${seat + 4} L${x - 66},${seat - 120}`, stroke: col, 'stroke-width': 10, 'stroke-linecap': 'round' }, c);
  svg('path', { d: `M${x - 40},${seat + 14} L${x - 44},1330 M${x + 40},${seat + 14} L${x + 44},1330`, stroke: now ? '#5a6a8a' : '#6a4224', 'stroke-width': 7 }, c);
  return c;
}
const BOYX = DESK14[2] + 80, KRUX = 862;   // the back-desk pupil; the chair beside it

// =====================================================================
// S0 — hook, today (the bookend): the teacher sets a bag of rice on the girl's desk and sits beside her
// =====================================================================
function presentMoment(S, A, B, o = {}) {
  const L = t => t - A;
  const set = classroom14(S, { mode: 'now' }), D = S.L.mid.defs;
  const girl = new Puppet(set.people, GIRL14, D), gsk = skirt14(girl, '#2a3a6e', { pleats: true, half: 30 }), gsh = schoolShirt14(girl, { name: '#2f5fb8', bow: '#2a3a6e' });
  const man = new Puppet(set.people, KRUMAN14, D);
  const chair = sideChair(set.people, KRUX, set.seat, true); set.people.insertBefore(chair, set.people.firstChild);
  const bot = bottle14(set.top, 0.8);
  const pair = bagPair14(man.prop, 0.9);
  const onDesk = svg('g', {}, set.top); const b1 = svg('g', {}, onDesk); foodBag14(b1, 'rice', 0.9); const b2 = svg('g', {}, onDesk); foodBag14(b2, '#e88a3a', 0.82);
  const mine = svg('g', {}, set.top); foodBag14(mine, 'rice', 0.8);
  const st = steam14(set.top);
  lightCast14(S, set, [set.people], [man], { light: { rim: '#fff1c4', rimOp: 0.7 }, shadow: { op: 0.13, k: 0.2, blur: 11 } });
  return { set, girl, gsk, gsh, man, pair, bot, onDesk, b1, b2, mine, st, L };
}
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04)';
  const m = presentMoment(S, A, B), { set, girl, gsk, gsh, man, pair, bot, onDesk, b1, b2, mine, st, L } = m;
  const q = glowQ(S.ui, 800, 380);
  const tPut = L(P.H2) + 0.2, tSit = L(P.H3) + 0.3;
  const XW = lt => lerp(285, 850, ease.inOutSine(prog(lt, 0.2, tPut - 0.15)));
  const shots = [
    { t: 0, cam: fA(650, 1000, 1.14, 540, 1000), to: fA(660, 1000, 1.18, 540, 1000) },
    { t: L(P.H2) - 0.05, cam: fA(955, 985, 2.0, 540, 1000), to: fA(955, 985, 2.08, 540, 1000) },
    { t: L(P.H4) - 0.05, cam: fA(956, 1000, 2.25, 540, 1060), to: fA(956, 1000, 2.34, 540, 1060) },   // both faces whole
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt); set.board({ cls: 'ป.4/1', extra: 'สุขสันต์วันครู' });
    const pg = chairP(girl, BOYX, set.seat, 1.2, -1, { t: lt, smile: lt > tSit + 0.5 ? 0.85 : 0.35, head: lt > tPut ? -14 : 8, mouthO: lt > tPut && lt < tSit + 0.5 ? 0.7 : 0 });
    const [gx, gy] = handsOnDesk(girl, pg, set.deskTop, lt, 0); girl.pose(pg); gsk(pg); gsh(pg);
    bot.setAttribute('transform', `translate(${(BOYX - 100).toFixed(0)},${set.deskTop - 34}) scale(0.8)`);
    let p;
    if (lt < tPut - 0.15) { p = walkP(man, XW(lt), set.ground, 1.2, 1, lt * 6.4, { amp: 13, t: lt, smile: 0.85, head: 4 }); const [hx, hy] = torsoW(man, p, 30, -40); p.aF = man.reach(p, hx, hy); }
    else if (lt < tSit) { p = standP(man, 850, set.ground, 1.2, 1, { t: lt, smile: 0.9, head: 12, torso: 10 }); p.aF = man.reach(p, lerp(900, 948, prog(lt, tPut - 0.15, tPut + 0.2)), lerp(1060, 1096, prog(lt, tPut - 0.15, tPut + 0.2))); }
    else { p = chairP(man, KRUX, set.seat, 1.2, 1, { t: lt, smile: 0.95, head: 6 }); handsOnDesk(man, p, set.deskTop - 6, lt, 0); }
    man.pose(p); pair.update(lt);
    pair.g.setAttribute('display', lt < tPut ? 'inline' : 'none');
    onDesk.setAttribute('display', lt >= tPut ? 'inline' : 'none'); b1.setAttribute('transform', `translate(${BOYX - 150},${set.deskTop})`); b2.setAttribute('transform', `translate(${BOYX - 112},${set.deskTop})`);
    mine.setAttribute('display', lt >= tSit ? 'inline' : 'none'); mine.setAttribute('transform', `translate(${KRUX + 60},${set.deskTop + 2})`);
    st(BOYX - 94, set.deskTop - 44, lt, lt >= tPut ? 1 : 0);
    q.update(lt, L(P.H4) + 0.1); q.el.style.display = lt > L(P.H4) ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// the past (sepia): ครูสมศรี and the boy at the back desk
// =====================================================================
function pastRoom(S, o = {}) {
  const set = classroom14(S, { mode: 'then' }), D = S.L.mid.defs;
  const boy = new Puppet(set.people, Object.assign({}, BOYX_O(o.grow || 0)), D), bsh = schoolShirt14(boy, { name: '#2f5fb8' });
  const kru = new Puppet(set.people, KRU14, D), ksk = skirt14(kru, '#6a3a6e', { len: 1.6, half: 34 });
  const chair = sideChair(set.people, KRUX, set.seat, false); set.people.insertBefore(chair, set.people.firstChild);
  const bot = bottle14(set.top, 0.8);
  const pair = bagPair14(kru.prop, 0.9);
  const onDesk = svg('g', {}, set.top); const b1 = svg('g', {}, onDesk); foodBag14(b1, 'rice', 0.9); const b2 = svg('g', {}, onDesk); foodBag14(b2, '#e88a3a', 0.82);
  const mine = svg('g', {}, set.top); foodBag14(mine, 'rice', 0.8);
  const st = steam14(set.top);
  lightCast14(S, set, [set.people], [kru], { light: { rim: '#ffe2a8', rimOp: 0.75 }, shadow: { op: 0.16, k: 0.22, blur: 9 } });
  return { set, boy, bsh, kru, ksk, chair, bot, pair, onDesk, b1, b2, mine, st };
}
const BOYX_O = grow => Object.assign({}, BOY14, { s: 0.8 + 0.08 * grow });

// =====================================================================
// S1 — "ตอน ป.4 บ้านเราไม่มีเงินให้มาโรงเรียน พักเที่ยง เราเลยนั่งดื่มน้ำอยู่หลังห้องคนเดียว"
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, LAYERS());
  S.grade = SEPIA;
  const L = t => t - A;
  const r = pastRoom(S), { set, boy, bsh, kru, bot } = r;
  kru.g.setAttribute('display', 'none'); r.onDesk.setAttribute('display', 'none'); r.mine.setAttribute('display', 'none'); r.pair.g.setAttribute('display', 'none');
  const chip = timeChip14(S.ui, 60, 130, '20 ปีก่อน', true);
  const tSip = L(P.A3) - 0.1;
  const shots = [
    { t: 0, cam: fA(660, 1000, 1.15, 540, 1000), to: fA(680, 1000, 1.2, 540, 1000) },
    { t: L(P.A2) - 0.1, cam: fA(1040, 1015, 2.4, 560, 1080), to: fA(1040, 1015, 2.52, 560, 1080) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt); set.board({ cls: 'ป.4/2', extra: 'เวร: ด.ช.เอก' });
    const p = chairP(boy, BOYX, set.seat, 1.2, -1, { t: lt, smile: 0.25, head: lt > L(P.A2) ? -12 : 6, torso: 2 });
    handsOnDesk(boy, p, set.deskTop, lt, 0);
    const sip = Math.sin(Math.PI * prog(lt, tSip, tSip + 0.8));
    if (sip > 0) { const [mx, my] = torsoW(boy, p, 60, -RIG.T + 10); p.aF = boy.reach(p, lerp(BOYX - 100, mx, sip), lerp(set.deskTop - 8, my, sip)); }
    boy.pose(p); bsh(p);
    const [wx, wy] = sip > 0 ? wristFW(boy, p) : [BOYX - 100, set.deskTop - 30];
    bot.setAttribute('transform', `translate(${wx.toFixed(1)},${(sip > 0 ? wy - 6 : wy).toFixed(1)}) rotate(${(sip * -40).toFixed(1)}) scale(0.8)`);
    chip.update(lt, 0.2); chip.el.style.display = lt < L(P.A2) - 0.1 ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "วันหนึ่ง ครูสมศรีเดินเข้ามา ถือข้าวมาสองถุง" + ครู: "ครูซื้อมาเกิน กินช่วยครูหน่อยนะ"
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, LAYERS());
  S.grade = SEPIA;
  const L = t => t - A;
  const r = pastRoom(S), { set, boy, bsh, kru, ksk, bot, pair, onDesk, b1, b2, mine, st } = r;
  const tPut = L(P.T0) - 0.05, tSit = L(P.T1) - 0.1;
  const XW = lt => lerp(285, 850, ease.inOutSine(prog(lt, 0.15, L(P.B2) + 0.2)));
  const shots = [
    { t: 0, cam: fA(660, 1000, 1.15, 540, 1000), to: fA(690, 1000, 1.2, 540, 1000) },
    { t: L(P.B2) - 0.05, cam: fA(860, 1000, 2.0, 520, 1000), to: fA(865, 1000, 2.08, 520, 1000) },
    { t: tPut - 0.05, cam: fA(955, 985, 2.0, 540, 1000), to: fA(955, 985, 2.1, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt); set.board({ cls: 'ป.4/2', extra: 'เวร: ด.ช.เอก' });
    const looks = lt > L(P.B0) + 0.5;
    const pb = chairP(boy, BOYX, set.seat, 1.2, -1, { t: lt, smile: lt > tSit + 0.4 ? 0.9 : 0.3, head: looks ? -10 : 6, mouthO: lt > tPut && lt < tSit + 0.4 ? 0.7 : 0 });
    handsOnDesk(boy, pb, set.deskTop, lt, lt > tSit + 0.6 ? 1 : 0); boy.pose(pb); bsh(pb);
    bot.setAttribute('transform', `translate(${BOYX - 100},${set.deskTop - 34}) scale(0.8)`);
    let p;
    if (lt < L(P.B2) + 0.2) { p = walkP(kru, XW(lt), set.ground, 1.2, 1, lt * 6.2, { amp: 12, t: lt, smile: 0.85, head: 4 }); const [hx, hy] = torsoW(kru, p, 36, -36); p.aF = kru.reach(p, hx, hy); }
    else if (lt < tSit) { p = standP(kru, 850, set.ground, 1.2, 1, { t: lt, smile: 0.95, head: 12, torso: 10 }); const k = prog(lt, tPut - 0.2, tPut + 0.2); p.aF = kru.reach(p, lerp(894, 948, k), lerp(1060, 1096, k)); }
    else { p = chairP(kru, KRUX, set.seat, 1.2, 1, { t: lt, smile: 0.95, head: 6 }); handsOnDesk(kru, p, set.deskTop - 6, lt, lt > tSit + 0.6 ? 1 : 0); }
    kru.pose(p); ksk(p); pair.update(lt);
    pair.g.setAttribute('display', lt < tPut ? 'inline' : 'none');
    onDesk.setAttribute('display', lt >= tPut ? 'inline' : 'none'); b1.setAttribute('transform', `translate(${BOYX - 150},${set.deskTop})`); b2.setAttribute('transform', `translate(${BOYX - 112},${set.deskTop})`);
    mine.setAttribute('display', lt >= tSit ? 'inline' : 'none'); mine.setAttribute('transform', `translate(${KRUX + 60},${set.deskTop + 2})`);
    st(BOYX - 94, set.deskTop - 44, lt, lt >= tPut ? 1 : 0);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "หลังจากวันนั้น ครูซื้อเกินทุกวัน 3 ปี จนเราจบ ป.6 ไม่เคยขาดสักวัน": a time-lapse of lunches; the board goes
// ป.4 → ป.5 → ป.6 (eraser wipes), the tally card rolls to 720; the boy grows
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, LAYERS());
  S.grade = SEPIA;
  const L = t => t - A;
  const r = pastRoom(S, { grow: 0 }), { set, boy, bsh, kru, ksk, bot, pair, onDesk, b1, b2, mine, st } = r;
  const boy6 = new Puppet(set.people, BOYX_O(1), S.L.mid.defs), bsh6 = schoolShirt14(boy6, { name: '#2f5fb8' });
  pair.g.setAttribute('display', 'none'); bot.setAttribute('display', 'none');
  const tally = mealTally14(S.ui, 96, 96);   // (zoomed 1.25 in CSS)
  const tBoard = L(P.C2) - 0.1, tBack = L(P.C3) - 0.1;
  const shots = [
    { t: 0, cam: fA(955, 985, 1.7, 540, 1080), to: fA(955, 985, 1.78, 540, 1080) },
    { t: tBoard, cam: fA(-30, 600, 2.1, 540, 900), to: fA(-30, 600, 2.18, 540, 900) },
    { t: tBack, cam: fA(955, 980, 2.0, 540, 1000), to: fA(955, 980, 2.1, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.45, minY: -900 }));
    const k = prog(lt, 0.2, tBack), day = (lt * 4) % 1;   // four lunches a second
    set.update(lt + (lt < tBack ? lt * 3 : 0));
    const yr = k < 0.34 ? 0 : k < 0.67 ? 1 : 2, w = (k * 3) % 1;
    set.board({ cls: ['ป.4/2', 'ป.5/2', 'ป.6/2'][yr], extra: 'เวร: ด.ช.เอก', tally: Math.floor(k * 30), wipe: yr < 2 && w > 0.85 ? (w - 0.85) / 0.15 : 0 });
    const grown = lt > tBack;
    boy.g.setAttribute('display', grown ? 'none' : 'inline'); boy6.g.setAttribute('display', grown ? 'inline' : 'none');
    const B_ = grown ? boy6 : boy, bs = grown ? bsh6 : bsh;
    const pb = chairP(B_, BOYX, set.seat, 1.2, -1, { t: lt, smile: grown ? 1 : 0.85, grin: grown && Math.sin(lt * 3) > 0 ? 1 : 0, head: -2 });
    handsOnDesk(B_, pb, set.deskTop, lt, 1); B_.pose(pb); bs(pb);
    const pk = chairP(kru, KRUX, set.seat, 1.2, 1, { t: lt, smile: 1, grin: grown && Math.sin(lt * 3 + 1) > 0 ? 1 : 0, head: 6 });
    handsOnDesk(kru, pk, set.deskTop - 6, lt, 1); kru.pose(pk); ksk(pk);
    const full = grown || day < 0.7;   // the bags come and go each "day"
    onDesk.setAttribute('display', full ? 'inline' : 'none'); mine.setAttribute('display', full ? 'inline' : 'none');
    b1.setAttribute('transform', `translate(${BOYX - 150},${set.deskTop}) scale(${grown ? 1 : (1 - day * 0.4).toFixed(3)},1)`); b2.setAttribute('transform', `translate(${BOYX - 112},${set.deskTop})`);
    mine.setAttribute('transform', `translate(${KRUX + 60},${set.deskTop + 2})`);
    st(BOYX - 94, set.deskTop - 44, lt, full ? 1 : 0);
    tally.update(lt, 0.05, tBack - 0.3); tally.el.style.display = lt < tBoard ? 'block' : 'none';
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 720 มื้อ / ที่ครูซื้อเกิน
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = classroom14(S, { mode: 'then' });
  S.L.far.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 1451, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '330px';
  ic.innerHTML = `<span class="bg14">${Array.from({ length: 3 }, (_, i) => `<i style="--i:${i}">${bagIcon14(170)}</i>`).join('')}</span>`;
  const icons = [...ic.querySelectorAll('i')];
  const t1 = html('div', 'title', wrap); t1.style.top = '620px'; t1.style.font = '700 210px/1 Kanit';
  const digits = ['7', '2', '0'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'มื้อ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่ครูซื้อเกิน'); t2.style.top = '870px'; t2.style.font = '600 108px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1010px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt); bok(lt);
    icons.forEach((e, i) => { const k = spring(lt, 0.05 + i * 0.08, 16, 6.5); e.style.opacity = fadeIn(lt, 0.05 + i * 0.08, 0.08); e.style.transform = `translateY(${((1 - k) * -120).toFixed(1)}px) rotate(${(Math.sin(lt * 2 + i) * 6).toFixed(1)}deg)`; });
    digits.forEach((d, i) => { const t0 = 0.3 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.55, 14, 7); unit.style.opacity = fadeIn(lt, 0.55, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.75, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.75, 1.25))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 1.05, 1.45)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — today: "วันนี้ เราเป็นครูแล้ว เมื่อวานตอนพักเที่ยง เราเห็นเด็กคนหนึ่ง นั่งดื่มน้ำอยู่หลังห้องคนเดียว" —
// at the board on Teacher's Day; the bell, the class runs out; the girl at the back desk, matched to the boy (his memory
// flickers over her)
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04)';
  const L = t => t - A;
  const m = presentMoment(S, A, B), { set, girl, gsk, gsh, man, bot, onDesk, mine, pair } = m;
  onDesk.setAttribute('display', 'none'); mine.setAttribute('display', 'none'); pair.g.setAttribute('display', 'none');
  const kids = KIDS14.map(o => new Puppet(set.top, o, S.L.mid.defs));
  const ghostG = svg('g', { opacity: 0, filter: 'sepia(0.8)' }, set.top);   // the boy he was, over her
  const ghost = new Puppet(ghostG, BOY14, S.L.mid.defs), gbs = schoolShirt14(ghost, { name: '#2f5fb8' });
  const chip = timeChip14(S.ui, 640, 130, 'ปัจจุบัน', false);
  const tBell = L(P.D1) - 0.05, tSee = L(P.D2) - 0.1, tGirl = L(P.D3) - 0.1;
  const shots = [
    { t: 0, cam: fA(110, 930, 1.75, 540, 1040), to: fA(118, 930, 1.82, 540, 1040) },
    { t: tBell, cam: fA(640, 1000, 1.14, 540, 1000), to: fA(642, 1000, 1.16, 540, 1000) },
    { t: tSee, cam: fA(260, 900, 2.0, 380, 1000), to: fA(262, 900, 2.06, 380, 1000) },
    { t: tGirl, cam: fA(1040, 1015, 2.4, 560, 1080), to: fA(1040, 1015, 2.52, 560, 1080) },   // = the boy's close-up in S1
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt); set.board({ cls: 'ป.4/1', extra: 'สุขสันต์วันครู' });
    // the teacher: writing the date at the board, then turning to the back of the room
    let p;
    if (lt < tBell) { p = standP(man, 170, set.ground, 1.2, 1, { t: lt, smile: 0.9, head: -6, torso: 2 }); p.aF = man.reach(p, 60, 1096); }   // at his desk by the พานพุ่ม, a hand on the flowers
    else p = standP(man, lt < tSee ? 245 : 260, set.ground, 1.2, 1, { t: lt, smile: lerp(0.8, 0.45, prog(lt, tSee, tSee + 0.6)), head: 6, torso: 0 });
    man.pose(p);
    // the class runs out at the bell
    kids.forEach((k, i) => {
      const t0 = tBell + 0.1 + i * 0.1, x = lerp(600 + i * 110, 120, prog(lt, t0, t0 + 0.8));   // running out to lunch, gone before the next cut
      k.g.setAttribute('display', lt > t0 - 0.05 && lt < t0 + 0.8 ? 'inline' : 'none');
      if (lt > t0 - 0.05) k.pose(walkP(k, x, set.ground, 1.2, -1, lt * 12 + i, { amp: 26, t: lt, smile: 0.9, grin: 1 }));
    });
    const pg = chairP(girl, BOYX, set.seat, 1.2, -1, { t: lt, smile: 0.25, head: lt > tGirl ? -12 : 6, torso: 2 });
    handsOnDesk(girl, pg, set.deskTop, lt, 0);
    const sip = Math.sin(Math.PI * prog(lt, tGirl + 0.3, tGirl + 1.1));
    if (sip > 0) { const [mx, my] = torsoW(girl, pg, 60, -RIG.T + 10); pg.aF = girl.reach(pg, lerp(BOYX - 100, mx, sip), lerp(set.deskTop - 8, my, sip)); }
    girl.pose(pg); gsk(pg); gsh(pg);
    const [wx, wy] = sip > 0 ? wristFW(girl, pg) : [BOYX - 100, set.deskTop - 30];
    bot.setAttribute('transform', `translate(${wx.toFixed(1)},${(sip > 0 ? wy - 6 : wy).toFixed(1)}) rotate(${(sip * -40).toFixed(1)}) scale(0.8)`);
    // memory: the boy he was flickers over her
    const gk = Math.sin(Math.PI * prog(lt, tGirl + 0.1, B - A + 0.2));
    ghostG.setAttribute('opacity', (0.42 * gk).toFixed(3));
    const pgh = chairP(ghost, BOYX, set.seat, 1.2, -1, { t: lt, smile: 0.25, head: -12, torso: 2 }); handsOnDesk(ghost, pgh, set.deskTop, lt, 0); ghost.pose(pgh); gbs(pgh);
    chip.update(lt, 0.15); chip.el.style.display = lt < tBell ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — "เราเลยเดินไปซื้อข้าวมาสองถุง แล้วบอกเขาว่า" + "ครูซื้อมาเกิน กินช่วยครูหน่อยนะ": framed like ครูสมศรี's walk in
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04)';
  const m = presentMoment(S, A, B), { set, girl, gsk, gsh, man, pair, bot, onDesk, b1, b2, mine, st, L } = m;
  const hearts = heartsRise(set.top, 1000, 900, L(P.Gend) + 0.1, 5, 1461, 0.3);
  const tPut = L(P.E1) - 0.05, tSit = L(P.G1) - 0.1;
  const XW = lt => lerp(285, 850, ease.inOutSine(prog(lt, 0.15, tPut - 0.15)));
  const shots = [
    { t: 0, cam: fA(660, 1000, 1.15, 540, 1000), to: fA(690, 1000, 1.2, 540, 1000) },
    { t: tPut - 0.1, cam: fA(955, 985, 2.0, 540, 1000), to: fA(955, 985, 2.1, 540, 1000) },
    { t: L(P.Gend) + 0.1, cam: fA(956, 1000, 2.25, 540, 1060), to: fA(956, 1000, 2.34, 540, 1060) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt); set.board({ cls: 'ป.4/1', extra: 'สุขสันต์วันครู' });
    const pg = chairP(girl, BOYX, set.seat, 1.2, -1, { t: lt, smile: lt > tSit + 0.5 ? 1 : 0.3, grin: lt > L(P.Gend) + 0.2 ? 1 : 0, head: lt > tPut ? -12 : 6, mouthO: lt > tPut && lt < tSit + 0.5 ? 0.7 : 0 });
    handsOnDesk(girl, pg, set.deskTop, lt, lt > L(P.Gend) ? 1 : 0); girl.pose(pg); gsk(pg); gsh(pg);
    bot.setAttribute('transform', `translate(${(BOYX - 100).toFixed(0)},${set.deskTop - 34}) scale(0.8)`);
    let p;
    if (lt < tPut - 0.15) { p = walkP(man, XW(lt), set.ground, 1.2, 1, lt * 6.4, { amp: 13, t: lt, smile: 0.85, head: 4 }); const [hx, hy] = torsoW(man, p, 30, -40); p.aF = man.reach(p, hx, hy); }
    else if (lt < tSit) { p = standP(man, 850, set.ground, 1.2, 1, { t: lt, smile: 0.95, head: 12, torso: 10 }); const k = prog(lt, tPut - 0.15, tPut + 0.2); p.aF = man.reach(p, lerp(900, 948, k), lerp(1060, 1096, k)); }
    else { p = chairP(man, KRUX, set.seat, 1.2, 1, { t: lt, smile: 0.95, head: 6 }); handsOnDesk(man, p, set.deskTop - 6, lt, lt > L(P.Gend) ? 1 : 0); }
    man.pose(p); pair.update(lt);
    pair.g.setAttribute('display', lt < tPut ? 'inline' : 'none');
    onDesk.setAttribute('display', lt >= tPut ? 'inline' : 'none'); b1.setAttribute('transform', `translate(${BOYX - 150},${set.deskTop})`); b2.setAttribute('transform', `translate(${BOYX - 112},${set.deskTop})`);
    mine.setAttribute('display', lt >= tSit ? 'inline' : 'none'); mine.setAttribute('transform', `translate(${KRUX + 60},${set.deskTop + 2})`);
    st(BOYX - 94, set.deskTop - 44, lt, lt >= tPut ? 1 : 0);
    hearts(lt);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — "ความใจดีบางอย่าง ไม่ได้จบที่เรา มันแค่รอวันส่งต่อ": split screen, then and now, eating together; the past slides
// away and the present opens to the whole room
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const L = t => t - A, tMerge = L(P.F2) - 0.1;
  // left: the past
  const SL = new Shot(A, B, LAYERS()); SL.grade = SEPIA;
  const r = pastRoom(SL, { grow: 0.5 }), { set: setL, boy, bsh, kru, ksk } = r;
  r.pair.g.setAttribute('display', 'none'); r.bot.setAttribute('display', 'none');
  SL.update = lt => {
    const k = ease.inOutCubic(prog(lt, tMerge, tMerge + 0.7));
    applyCam(SL, shotCamF(lt, [{ t: 0, cam: fA(955, 980, 1.38, 270, 1000), to: fA(955, 980, 1.44, 270, 1000) }], B - A, { handheld: 0.4, minY: -300 }));
    SL.root.style.clipPath = `inset(0 ${(50 + 50 * k).toFixed(2)}% 0 0)`;
    setL.update(lt); setL.board({ cls: 'ป.4/2', extra: 'เวร: ด.ช.เอก' });
    const pb = chairP(boy, BOYX, setL.seat, 1.2, -1, { t: lt, smile: 1, grin: Math.sin(lt * 3) > 0.3 ? 1 : 0, head: -2 }); handsOnDesk(boy, pb, setL.deskTop, lt, 1); boy.pose(pb); bsh(pb);
    const pk = chairP(kru, KRUX, setL.seat, 1.2, 1, { t: lt, smile: 1, head: 6 }); handsOnDesk(kru, pk, setL.deskTop - 6, lt, 1); kru.pose(pk); ksk(pk);
    r.b1.setAttribute('transform', `translate(${BOYX - 150},${setL.deskTop})`); r.b2.setAttribute('transform', `translate(${BOYX - 112},${setL.deskTop})`); r.mine.setAttribute('transform', `translate(${KRUX + 60},${setL.deskTop + 2})`);
    r.st(BOYX - 94, setL.deskTop - 44, lt, 1);
  };
  // right: today
  const SR = new Shot(A, B, LAYERS()); SR.grade = 'saturate(1.06) contrast(1.04)';
  const m = presentMoment(SR, A, B), { set: setR, girl, gsk, gsh, man, bot } = m;
  m.pair.g.setAttribute('display', 'none');
  const divider = html('div', 'div14', SR.fx);
  const leak = lightLeak(SR.fx);
  const back = behindSvg(SR);
  const hearts = heartsRise(back, 540, 980, tMerge + 0.4, 7, 1471, 0.3);
  SR.update = lt => {
    const k = ease.inOutCubic(prog(lt, tMerge, tMerge + 0.7));
    const c1 = frameAt(955, 980, 1.38, 810, 1000), c2 = frameAt(640, 960, 1.12, 540, 1000);
    const cam = shotCamF(lt, [{ t: 0, cam: () => lerpCam(c1, c2, k), to: () => lerpCam(c1, c2, k) }], B - A, { handheld: 0.4, minY: -300 });
    applyCam(SR, cam);
    SR.root.style.clipPath = `inset(0 0 0 ${(50 - 50 * k).toFixed(2)}%)`;
    divider.style.opacity = (1 - k).toFixed(3);
    setR.update(lt); setR.board({ cls: 'ป.4/1', extra: 'สุขสันต์วันครู' });
    const pg = chairP(girl, BOYX, setR.seat, 1.2, -1, { t: lt, smile: 1, grin: Math.sin(lt * 3 + 1) > 0.3 ? 1 : 0, head: -2 }); handsOnDesk(girl, pg, setR.deskTop, lt, 1); girl.pose(pg); gsk(pg); gsh(pg);
    const pm = chairP(man, KRUX, setR.seat, 1.2, 1, { t: lt, smile: 1, head: 6 }); handsOnDesk(man, pm, setR.deskTop - 6, lt, 1); man.pose(pm);
    bot.setAttribute('transform', `translate(${(BOYX - 100).toFixed(0)},${setR.deskTop - 34}) scale(0.8)`);
    m.onDesk.setAttribute('display', 'inline'); m.b1.setAttribute('transform', `translate(${BOYX - 150},${setR.deskTop})`); m.b2.setAttribute('transform', `translate(${BOYX - 112},${setR.deskTop})`);
    m.mine.setAttribute('display', 'inline'); m.mine.setAttribute('transform', `translate(${KRUX + 60},${setR.deskTop + 2})`);
    m.st(BOYX - 94, setR.deskTop - 44, lt, 1);
    leak(lt, 0.15 + 0.4 * prog(lt, tMerge, B - A)); hearts(lt);
  };
  SHOTS.push(SL, SR);
})();

// =====================================================================
// S8 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#8a6a4a'], [0.6, '#4a3424'], [1, '#22160e']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 1481, { color: '#ffd9a0', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 1482, ['#ffd66b', '#ffffff', '#ffd9a0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '290px';
  duo.innerHTML = `<span class="duo7">${av14('kru', 190)}</span><span class="duo7h">${bagIcon14(150)}</span><span class="duo7">${av14('man', 190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '10px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['7', '2', '0'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'มื้อ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่ครูซื้อเกิน'); t2.style.top = '808px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'ความใจดี ไม่ได้จบที่เรา ส่งต่อได้เสมอ'); sub.style.top = '960px'; sub.style.font = '500 48px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1100px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้ครูที่เคยใจดีกับเรา</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.6, 14, 7); unit.style.opacity = fadeIn(lt, 0.6, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.8, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.8, 1.25))) * 100).toFixed(1)}% -40% 0)`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.9, fl(SC.s4[0]), fl(SC.s5[0]) * 0.9, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
