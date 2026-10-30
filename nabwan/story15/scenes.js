// "8 ซอง ที่อาม่าไม่เคยแกะ" — scenes timed to the narration in vo.js (VO.P: H hook, A childhood, B the first salary,
// C eight years, the title, D–E this year in Bangkok, G coming home, T อาม่า's own line, F her gift, L the lesson).
// Bookends: the hook shows the open tin without context, G pays it off; the gift dissolves to the same moment 23 years
// ago (sepia) and back, and the ending cranes up into the lanterns.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3], s3: [P.C0 - 0.3, P.title], s4: [P.title, P.D0 - 0.1],
  s5: [P.D0 - 0.1, P.G0 - 0.3], s6: [P.G0 - 0.3, P.T0 - 0.3], s7: [P.T0 - 0.3, P.F0 - 0.3], s8: [P.F0 - 0.3, P.end], s9: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const SEPIA = 'sepia(0.5) saturate(0.92) contrast(1.03) brightness(1.04)';
const WARM = 'saturate(1.06) contrast(1.04)';
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
function lightCast15(S, set, groups, pups, o = {}) {
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
  cam.shot = i;
  return cam;
}
const fA = (...a) => () => frameAt(...a);
const shotIx = (lt, shots) => { let i = 0; while (i + 1 < shots.length && lt >= shots[i + 1].t) i++; return i; };
// both hands on the table edge in front (seated)
function handsOnTable(pup, p, y, lt, mv = 0) {
  const f = p.f || 1, S = p.s * pup.o.s;
  const fx = p.x + f * (70 + Math.sin(lt * 5) * 5 * mv) * S, bx = p.x + f * 46 * S;
  p.aF = pup.reach(p, fx, y - 6); p.aB = pup.reach(p, bx, y - 2);
  return [fx, y - 6];
}
// both wrists on a held object's near edge (world point x, y = its centre); f = the holder's facing
function holdBoth(pup, p, x, y, w = 18) { const f = p.f || 1; p.aF = pup.reach(p, x - f * w, y - 8); p.aB = pup.reach(p, x - f * w, y + 14); }
// a world envelope, centred on (x, y)
function envAt(g, s = 0.9, o = {}) { const w = svg('g', {}, g), e = svg('g', {}, w); angpao15(e, s, o); return { g: w, at(x, y, rot = 0, show = true) { w.setAttribute('display', show ? 'inline' : 'none'); w.setAttribute('transform', `translate(${x.toFixed(1)},${(y + 36 * s).toFixed(1)}) rotate(${rot.toFixed(1)} 0 ${(-36 * s).toFixed(1)})`); } }; }
// speech: the mouth flaps while a line plays
const talk = (lt, a, b) => (lt > a && lt < b ? 0.35 + 0.35 * Math.max(0, Math.sin(lt * 15)) + 0.2 * Math.max(0, Math.sin(lt * 23 + 1)) : 0);
// eye positions (world) on the 3/4 face, for tears
function eyesW(pup, p) { const [hx, hy] = headW(pup, p), R = pup.o.R, S = p.s * pup.o.s, f = p.f || 1, a = rad((p.torso || 0) + (p.head || 0)); const pt = (lx, ly) => [hx + f * S * (lx * Math.cos(a) - ly * Math.sin(a)), hy + S * (lx * Math.sin(a) + ly * Math.cos(a))]; return [pt(R * 0.5, R * 0.06), pt(R * 0.02, R * 0.06)]; }
const TOPY = TABLE15.top;

// =====================================================================
// the table today (or eight years ago): อาม่า on the right, her grandson on the left; the tin, the tea, the oranges
// =====================================================================
function tableScene(S, o = {}) {
  const set = shophouse15(S, { mode: o.mode || 'now' }), D = S.L.mid.defs;
  const ama = new Puppet(set.people, o.ama || AMA15, D), amaM = mandarin15(ama, { hem: true }), amaJ = jade15(ama);
  const luk = new Puppet(set.people, o.luk || LUK15, D);
  const tin = tin15(set.top, 1); tin.g.setAttribute('transform', `translate(560,${TOPY + 8})`);
  const tea = svg('g', { transform: `translate(650,${TOPY + 6})` }, set.top); teaSet15(tea, 0.62);
  const st = () => {};   // no steam: the pot sits under her face
  const bag = oranges15(set.top, 0.9), bagD = svg('g', {}, set.top); orangesDown15(bagD, 0.85); bagD.setAttribute('transform', `translate(432,${TOPY + 8})`);
  const env = envAt(set.top, 0.9);
  lightCast15(S, set, [set.people], [ama, luk], { light: { rim: '#fff1c4', rimOp: 0.7 }, shadow: { op: 0.17, k: 0.24, blur: 10 } });
  const amaPose = p => { ama.pose(p); amaM(p); amaJ(p); };
  return { set, ama, luk, tin, tea, st, bag, bagD, env, amaPose };
}
const AMA_SIT = (ama, lt, o = {}) => chairP(ama, AMAX, SEAT15, 1.2, -1, Object.assign({ t: lt, smile: 0.8, head: 2 }, o));
const LUK_SIT = (luk, lt, o = {}) => chairP(luk, LUKX, SEAT15, 1.2, 1, Object.assign({ t: lt, smile: 0.5, head: 4 }, o));

// =====================================================================
// S0 — hook, today: the open tin pushed across the table, eight sealed envelopes, his face
// =====================================================================
(() => {
  const [A] = SC.s0, L = t => t - A, tIns = L(P.H2) - 0.05, tCU = L(P.H4) - 0.05;
  // wide, then the close-up (one world)
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = WARM;
  const m = tableScene(S), { set, ama, luk, tin, st, bag, env, amaPose } = m;
  bag.g.setAttribute('display', 'none'); env.at(0, 0, 0, false);
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(545, 990, 1.42, 540, 1010), to: fA(545, 990, 1.5, 540, 1010) }], tIns, { handheld: 0.5, minY: -400 }));
    set.update(lt);
    const k = ease.inOutCubic(prog(lt, 0.3, 1.6)), tx = lerp(600, 520, k);
    tin.g.setAttribute('transform', `translate(${tx.toFixed(1)},${TOPY + 8})`); tin.set(1, 3);
    const pa = AMA_SIT(ama, lt, { smile: 0.95, head: 6, torso: lerp(4, 14, Math.sin(Math.PI * k)) }); holdBoth(ama, pa, tx + 70, TOPY - 14, 4); amaPose(pa);
    const pl = LUK_SIT(luk, lt, { smile: 0.2, head: 10 }); handsOnTable(luk, pl, TOPY, lt); luk.pose(pl);
    st(650 - 26, TOPY - 40, lt, 1);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
  // the insert: the open tin, the envelopes, never opened
  const S2 = new Shot(A + tIns, A + tCU, LAYERS()); S2.grade = WARM;
  const T = tinMacro15(S2);
  S2.update = lt => {
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(540, 1040, 1.0, 540, 980), to: fA(540, 1040, 1.12, 540, 980) }], tCU - tIns, { handheld: 0.4, minY: -600 }), { dof: false });
    T.update(lt); T.set({ open: 1, n: 8, fan: 0.35, glint: lt * 1.6, t: lt });
  };
  SHOTS.push(S2);
  const S3 = new Shot(A + tCU, SC.s0[1], LAYERS()); S3.grade = WARM;
  const m3 = tableScene(S3), q = glowQ(S3.ui, 800, 520);
  m3.bag.g.setAttribute('display', 'none'); m3.env.at(0, 0, 0, false);
  S3.update = lt => {
    applyCam(S3, shotCamF(lt, [{ t: 0, cam: fA(400, 975, 2.2, 700, 1000), to: fA(400, 975, 2.3, 700, 1000) }], 2, { handheld: 0.5, minY: -400 }));
    m3.set.update(lt + tCU); m3.tin.g.setAttribute('transform', `translate(520,${TOPY + 8})`); m3.tin.set(1, 3);
    const pa = AMA_SIT(m3.ama, lt, { smile: 0.95 }); handsOnTable(m3.ama, pa, TOPY, lt); m3.amaPose(pa);
    const pl = LUK_SIT(m3.luk, lt, { smile: 0.1, head: 12, eyes: 0.85 }); handsOnTable(m3.luk, pl, TOPY, lt); m3.luk.pose(pl);
    q.update(lt, 0.15);
  };
  SHOTS.push(S3);
})();

// =====================================================================
// the past (sepia): อาม่า at 57 by the altar, the boy runs in from the street
// =====================================================================
function pastRoom(S) {
  const set = shophouse15(S, { mode: 'then' }), D = S.L.mid.defs;
  set.stools.firstChild.setAttribute('display', 'none');   // her stool stood elsewhere then; the boy stands here
  const ama = new Puppet(set.people, AMA15_Y, D), amaM = mandarin15(ama, { trim: '#c8343c', collar: '#d6c8ac' }), amaJ = jade15(ama);
  const kid = new Puppet(set.people, KID15, D), kidM = mandarin15(kid, { trim: '#f2c14e' });
  const tea = svg('g', { transform: `translate(650,${TOPY + 6})` }, set.top); teaSet15(tea, 0.62);
  const env = envAt(set.top, 0.75);
  lightCast15(S, set, [set.people], [ama, kid], { light: { rim: '#ffe2a8', rimOp: 0.75 }, shadow: { op: 0.18, k: 0.24, blur: 9 } });
  return { set, ama, kid, env, amaPose: p => { ama.pose(p); amaM(p); amaJ(p); }, kidPose: p => { kid.pose(p); kidM(p); } };
}
const KIDX = 720, AMAYX = 885;
// the hand-off between อาม่า (standing, bending) and the boy; k: 0 she holds it out, 1 he has it at his chest
function pastGive(r, lt, k, o = {}) {
  const pa = standP(r.ama, AMAYX, r.set.ground, 1.2, -1, { t: lt, smile: 1, head: 14, torso: 16 });
  const ex = lerp(808, 770, ease.inOutCubic(k)), ey = lerp(1078, 1110, ease.inOutCubic(k));
  if (k < 0.55) holdBoth(r.ama, pa, ex, ey, 20); else { pa.aF = r.ama.reach(pa, 840, 1150); pa.aB = r.ama.reach(pa, 852, 1160); }
  r.amaPose(pa);
  const pk = standP(r.kid, KIDX, r.set.ground, 1.2, 1, { t: lt, smile: o.smile ?? 0.9, grin: o.grin ?? 0, head: -8, torso: 2 });
  holdBoth(r.kid, pk, ex, ey, 18); r.kidPose(pk);
  r.env.at(ex, ey, 0, true);
}

// =====================================================================
// S1 — "ตอนเด็ก อาม่าให้อั่งเปาเราทุกปี ซองละยี่สิบบาท": he runs in, wais, takes it with both hands, jumps for joy
// =====================================================================
(() => {
  const [A, B] = SC.s1, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = SEPIA;
  const r = pastRoom(S), { set, ama, kid, env } = r;
  const chip = timeChip15(S.ui, 60, 130, '23 ปีก่อน', true);
  const back = behindSvg(S), spark = burst(back, 540, 640, L(P.A2) + 0.1, 16, 1511, ['#ffd66b', '#ffffff', '#ffb0a0'], 260, 0.9);
  const tTake = L(P.A1) + 0.5, tJump = L(P.A2) - 0.05;
  const shots = [
    { t: 0, cam: fA(600, 990, 1.15, 540, 1000), to: fA(620, 990, 1.18, 540, 1000) },
    { t: tTake - 0.1, cam: fA(800, 975, 2.1, 540, 1000), to: fA(800, 975, 2.2, 540, 1000) },
    { t: tJump, cam: fA(760, 960, 1.6, 540, 1000), to: fA(760, 950, 1.66, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -400 }));
    set.update(lt);
    const run = prog(lt, 0.05, 0.85);
    if (lt < 0.85) {
      r.amaPose(standP(ama, AMAYX, set.ground, 1.2, -1, { t: lt, smile: 0.9, head: 4 }));
      r.kidPose(walkP(kid, lerp(190, KIDX, ease.outCubic(run)), set.ground, 1.2, 1, lt * 12, { amp: 24, t: lt, smile: 1, grin: 1 }));
      env.at(0, 0, 0, false);
    } else if (lt < tTake) {   // the wai, อาม่า takes out the envelope
      const pa = standP(ama, AMAYX, set.ground, 1.2, -1, { t: lt, smile: 1, head: 10, torso: lerp(0, 16, prog(lt, 1.0, tTake)) });
      holdBoth(ama, pa, lerp(840, 808, prog(lt, 1.0, tTake)), lerp(1150, 1078, prog(lt, 1.0, tTake)), 20); r.amaPose(pa);
      const pk = standP(kid, KIDX, set.ground, 1.2, 1, { t: lt, smile: 0.9, head: lt < 1.25 ? 16 : -6, torso: lt < 1.25 ? 12 : 2 });
      const [hx, hy] = torsoW(kid, pk, 44, -RIG.T + 40); pk.aF = kid.reach(pk, hx + 4, hy - 6); pk.aB = kid.reach(pk, hx - 2, hy + 2); r.kidPose(pk);
      env.at(lerp(840, 808, prog(lt, 1.0, tTake)), lerp(1150, 1078, prog(lt, 1.0, tTake)), 0, lt > 1.0);
    } else if (lt < tJump) pastGive(r, lt, prog(lt, tTake, tTake + 0.7));
    else {   // the jump: the envelope held high, arms out and up
      const j = Math.abs(Math.sin((lt - tJump) * 7.5)), pk = standP(kid, KIDX - 20, set.ground - j * 40, 1.2, 1, { t: lt, smile: 1, grin: 1, head: -10, aF: [-24, -48], aB: [214, 236], lF: j > 0.3 ? [70, 120] : [88, 92], lB: j > 0.3 ? [110, 70] : [92, 88] });
      r.kidPose(pk); const [wx, wy] = wristFW(kid, pk); env.at(wx + 6, wy - 30, 18, true);
      r.amaPose(standP(ama, AMAYX, set.ground, 1.2, -1, { t: lt, smile: 1, grin: 1, head: 2 }));
    }
    spark(lt);
    chip.update(lt, 0.2); chip.el.style.display = lt < tTake - 0.1 ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "พอได้เงินเดือนแรก เราให้อาม่าคืนบ้าง อาม่ารับสองมือ แล้วเก็บใส่กล่องคุกกี้ใบเก่า" (8 years ago)
// =====================================================================
(() => {
  const [A, B] = SC.s2, L = t => t - A, tTwo = L(P.B1) - 0.05, tTake = L(P.B2) - 0.05, tIns = L(P.B3) - 0.05;
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = WARM;
  const m = tableScene(S, { mode: 'b', ama: AMA15_B, luk: LUK15_W }), { set, ama, luk, tin, st, bag, bagD, env, amaPose } = m;
  const chip = timeChip15(S.ui, 60, 120, 'พ.ศ. 2562', false), pay = salaryCard15(S.ui, 150, 230);
  tin.g.setAttribute('transform', `translate(600,${TOPY + 8})`); tin.set(0, 0);
  const shots = [
    { t: 0, cam: fA(560, 990, 1.15, 540, 1000), to: fA(570, 990, 1.18, 540, 1000) },
    { t: tTwo, cam: fA(600, 950, 2.0, 540, 1000), to: fA(600, 950, 2.08, 540, 1000) },
  ];
  const XW = lt => lerp(230, 450, ease.inOutSine(prog(lt, 0.1, tTwo - 0.1)));
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, tIns, { handheld: 0.5, minY: -400 }));
    set.update(lt); set.year(2562);
    let p;
    if (lt < tTwo - 0.1) { p = walkP(luk, XW(lt), set.ground, 1.2, 1, lt * 6.4, { amp: 13, t: lt, smile: 0.95, head: 2 }); }
    else p = standP(luk, 450, set.ground, 1.2, 1, { t: lt, smile: 0.95, head: lt > tTwo + 0.5 ? 12 : 4, torso: lt > tTwo + 0.5 ? 14 : 2 });
    const down = lt > tTwo + 0.05;   // the oranges go on the table
    const k = prog(lt, tTwo + 0.5, tTake), kk = prog(lt, tTake, tTake + 0.5);
    const ex = lerp(578, 618, kk), ey = lerp(1046, 1060, kk);
    if (lt > tTwo + 0.5 && lt < tTake + 0.25) holdBoth(luk, p, lerp(500, ex, ease.outCubic(k)), lerp(1100, ey, ease.outCubic(k)), 18);
    else if (!down) { const [hx, hy] = torsoW(luk, p, 30, -40); p.aF = luk.reach(p, hx, hy); }
    luk.pose(p);
    const [bx, by] = wristBW(luk, p); bag.g.setAttribute('transform', `translate(${bx.toFixed(1)},${by.toFixed(1)})`); bag.update(lt); bag.g.setAttribute('display', down ? 'none' : 'inline'); bagD.setAttribute('display', down ? 'inline' : 'none');
    const pa = AMA_SIT(ama, lt, { smile: 1, grin: lt > tTake ? 1 : 0, head: lt < tTwo ? -4 : 6 });
    if (lt > tTake - 0.2) holdBoth(ama, pa, ex, ey, 18); else handsOnTable(ama, pa, TOPY, lt);
    amaPose(pa);
    env.at(lt > tTwo + 0.5 ? (lt < tTake ? lerp(500, ex, ease.outCubic(k)) : ex) : 0, lt < tTake ? lerp(1100, ey, ease.outCubic(k)) : ey, 0, lt > tTwo + 0.5);
    st(650 - 26, TOPY - 40, lt, 1);
    pay.update(lt, 0.25); pay.el.style.display = lt < tTwo ? 'block' : 'none';
    chip.update(lt, 0.15); chip.el.style.display = lt < tTwo ? 'flex' : 'none';
  };
  SHOTS.push(S);
  // the insert: her hand drops it into the empty tin; the lid goes back on
  const S2 = new Shot(A + tIns, B, LAYERS()); S2.grade = WARM;
  const T = tinMacro15(S2, { heldYear: '2562' });
  S2.update = lt => {
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(540, 1040, 1.04, 540, 980), to: fA(540, 1040, 1.12, 540, 980) }], B - A - tIns, { handheld: 0.4, minY: -600 }), { dof: false });
    T.update(lt);
    const k = ease.inOutCubic(prog(lt, 0.05, 0.55)), drop = lt > 0.6, kl = ease.inOutCubic(prog(lt, 1.15, 1.6));
    T.set({ open: 1 - kl, n: drop ? 1 : 0, arm: lt < 1.0 ? { x: lerp(900, 640, k) + (drop ? (lt - 0.6) * 700 : 0), y: lerp(440, 820, k) - (drop ? (lt - 0.6) * 900 : 0) } : null, held: !drop, t: lt });
  };
  SHOTS.push(S2);
})();

// =====================================================================
// S3 — "ปีต่อๆ มา ซองหนาขึ้นเรื่อยๆ ครบแปดปี แปดซอง": a time-lapse of New Years at the table; a new shirt every year, the
// calendar flips, the card rolls 2562 → 2569; the insert: eight envelopes, the lid closes
// =====================================================================
(() => {
  const [A, B] = SC.s3, L = t => t - A, tIns = L(P.C3) - 0.1, t0 = 0.15, per = (tIns - 0.25 - t0) / 8;
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = WARM;
  const m = tableScene(S, { mode: 'b', ama: AMA15_B, luk: LUK15_T[0] }), { set, ama, luk, tin, st, bag, bagD, env, amaPose } = m;
  bag.g.setAttribute('display', 'none');
  const luks = [luk, ...LUK15_T.slice(1).map(o => new Puppet(set.people, o, S.L.mid.defs))];
  const envs = Array.from({ length: 8 }, (_, i) => envAt(set.top, 0.9, { thick: i / 7 }));
  const card = yearsCard15(S.ui, 70, 96);
  tin.g.setAttribute('transform', `translate(600,${TOPY + 8})`);
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(560, 985, 1.45, 540, 1010), to: fA(560, 985, 1.52, 540, 1010) }], tIns, { handheld: 0.45, minY: -400 }));
    const yi = clamp(Math.floor((lt - t0) / per), 0, 7), u = clamp((lt - t0) / per - yi);
    set.update(lt * 2); set.year(2562 + yi, u < 0.18 ? u / 0.18 : 0);
    const L_ = luks[yi % 4]; luks.forEach(p => p.g.setAttribute('display', p === L_ ? 'inline' : 'none'));
    // one hand-off a year: out (0–.4), she takes it (.4–.6), into the tin (.6–1)
    const ex = u < 0.4 ? lerp(470, 540, u / 0.4) : u < 0.6 ? 540 : lerp(540, 600, (u - 0.6) / 0.4), ey = u < 0.6 ? 1056 : lerp(1056, TOPY - 40, (u - 0.6) / 0.4);
    const pl = LUK_SIT(L_, lt, { smile: 1, grin: u > 0.4 && u < 0.7 ? 1 : 0, head: 2, torso: u < 0.45 ? 4 + 10 * Math.sin(Math.PI * u / 0.45) : 4 });
    if (u < 0.5) holdBoth(L_, pl, ex, ey, 18); else handsOnTable(L_, pl, TOPY, lt); L_.pose(pl);
    const pa = AMA_SIT(ama, lt, { smile: 1, grin: u > 0.45 ? 1 : 0, head: 4 });
    if (u > 0.35) holdBoth(ama, pa, ex, ey, 18); else handsOnTable(ama, pa, TOPY, lt);
    amaPose(pa);
    envs.forEach((e, i) => e.at(ex, ey, 0, i === yi && u < 0.95));
    tin.set(u > 0.55 && u < 0.98 ? Math.sin(Math.PI * (u - 0.55) / 0.43) : 0, 3);
    st(650 - 26, TOPY - 40, lt, 1);
    card.update(lt, 0.05, tIns - 0.2);
  };
  SHOTS.push(S);
  const S2 = new Shot(A + tIns, B, LAYERS()); S2.grade = WARM;
  const T = tinMacro15(S2);
  S2.update = lt => {
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(540, 1040, 1.06, 540, 980), to: fA(540, 1040, 1.14, 540, 980) }], B - A - tIns, { handheld: 0.4, minY: -600 }), { dof: false });
    T.update(lt); T.set({ open: 1 - ease.inOutCubic(prog(lt, 0.45, 0.9)), n: 8, t: lt });
  };
  SHOTS.push(S2);
})();

// =====================================================================
// S4 — title: 8 ซอง / ที่อาม่าไม่เคยแกะ
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = shophouse15(S, { mode: 'now' });
  S.L.far.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 1512, { color: '#ffb070', rMin: 14, rMax: 40, speed: 12, op: 0.24, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '300px';
  ic.innerHTML = `<span class="fan15">${Array.from({ length: 8 }, (_, i) => `<i style="--i:${i}">${angpaoIcon15(96)}</i>`).join('')}</span>`;
  const icons = [...ic.querySelectorAll('i')];
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 230px/1 Kanit';
  const digit = html('span', 'tdig', t1, '8');
  const unit = html('span', 'tdig', t1, 'ซอง'); unit.style.marginLeft = '0.25em'; unit.style.fontSize = '130px';
  const t2 = html('div', 'title', wrap, 'ที่อาม่าไม่เคยแกะ'); t2.style.top = '870px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1000px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt); bok(lt);
    icons.forEach((e, i) => { const k = spring(lt, 0.05 + i * 0.05, 16, 6.5), a = (i - 3.5) * 11 * Math.min(1, k); e.style.opacity = fadeIn(lt, 0.05 + i * 0.05, 0.08); e.style.transform = `translateY(${((1 - k) * -120).toFixed(1)}px) rotate(${(a + Math.sin(lt * 2 + i) * 3).toFixed(1)}deg)`; });
    const kd = spring(lt, 0.3, 15, 6); digit.style.opacity = fadeIn(lt, 0.3, 0.08); digit.style.transform = `translateY(${((1 - kd) * -150).toFixed(1)}px)`;
    const ku = spring(lt, 0.5, 14, 7); unit.style.opacity = fadeIn(lt, 0.5, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.7, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.7, 1.2))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 1.0, 1.4)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — Bangkok, this year: "แต่ปีนี้ บริษัทปิด เราตกงาน" (he carries his box home) / "อาม่าทักไลน์มาว่า ปีนี้กลับไหม"
// (on the bed, the phone) / "เราเกือบไม่กลับ" (close-up) / "เพราะไม่มีซองจะให้" (insert: an empty envelope, a wallet)
// =====================================================================
(() => {
  const [A, B] = SC.s5, L = t => t - A, tBed = L(P.E0) - 0.1, tCU = L(P.E2) - 0.05, tIns = L(P.E3) - 0.05;
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = 'saturate(1.04) contrast(1.05)';
  const set = room15(S), D = S.L.mid.defs;
  const luk = new Puppet(set.people, LUK15, D);
  const box = svg('g', {}, set.top); officeBox15(box, 0.95);
  const ph = phone15(luk.prop);
  lightCast15(S, set, [set.people], [luk], { light: { rim: '#ffd8a0', rimOp: 0.75 }, shadow: { op: 0.22, k: 0.22, blur: 8 } });
  const shut = closedCard15(S.ui, 140, 130), line = lineBanner15(S.ui, 150, 'ปีนี้กลับไหม');
  const tDown = L(P.Dend) - 0.4;
  const shots = [
    { t: 0, cam: fA(540, 990, 1.15, 540, 1000), to: fA(520, 990, 1.18, 540, 1000) },
    { t: tBed, cam: fA(650, 960, 1.6, 540, 1040), to: fA(655, 960, 1.66, 540, 1040) },
    { t: tCU, cam: fA(680, 975, 2.2, 520, 1000), to: fA(680, 975, 2.3, 520, 1000) },
  ];
  const XW = lt => lerp(240, 330, ease.inOutSine(prog(lt, 0.05, tDown)));
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, tIns, { handheld: 0.5, minY: -300 }));
    set.update(lt);
    let p;
    ph.g.setAttribute('display', si > 0 ? 'inline' : 'none');
    if (si === 0) {
      const bend = Math.sin(Math.PI * prog(lt, tDown, tDown + 0.8));
      if (lt < tDown) p = walkP(luk, XW(lt), set.ground, 1.2, 1, lt * 5.6, { amp: 11, t: lt, smile: 0.1, head: 10 });
      else p = standP(luk, 330, set.ground, 1.2, 1, { t: lt, smile: 0.05, head: 14 + bend * 10, torso: bend * 26 });
      const carry = lt < tDown + 0.45;
      const [cx, cy] = carry ? torsoW(luk, p, 76, -RIG.T + 70) : [0, 0];
      if (carry) { p.aF = luk.reach(p, cx + 10, cy - 6); p.aB = luk.reach(p, cx - 4, cy - 2); }
      luk.pose(p);
      const bx = carry ? cx + 6 : 430, by = carry ? cy + 70 : set.ground;
      box.setAttribute('transform', `translate(${bx.toFixed(1)},${(carry ? Math.min(by, lerp(by, set.ground, prog(lt, tDown, tDown + 0.45))) : by).toFixed(1)}) scale(0.95)`);
    } else {
      box.setAttribute('transform', `translate(430,${set.ground}) scale(0.95)`);
      const low = si === 2 ? ease.inOutCubic(prog(lt, tCU + 0.2, tCU + 0.7)) : 0;
      p = chairP(luk, 700, 1206, 1.2, -1, { t: lt, smile: si === 2 ? 0.05 : 0.3, head: 6 + low * 14, torso: 8 + low * 6, eyes: si === 2 ? 0.8 : 1 });
      const [hx, hy] = torsoW(luk, p, 70 - low * 10, -RIG.T + 30 + low * 60);
      p.aF = luk.reach(p, hx + 6, hy - 2); p.aB = luk.reach(p, hx - 6, hy + 8); p.propRot = -14;
      luk.pose(p);
      ph.glow.setAttribute('opacity', (0.6 + 0.4 * Math.sin(lt * 3)).toFixed(2));
    }
    shut.update(lt, L(P.D1) - 0.2, L(P.D1) + 0.45); shut.el.style.display = si === 0 ? 'block' : 'none';
    line.update(lt, tBed + 0.02, L(P.E1) - 0.2); line.el.style.display = si === 1 ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 6);
  };
  SHOTS.push(S);
  const S2 = new Shot(A + tIns, B, LAYERS()); S2.grade = 'saturate(1.04) contrast(1.05)';
  const Dm = deskMacro15(S2);
  S2.update = lt => { applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(590, 1180, 1.22, 540, 1060), to: fA(590, 1180, 1.32, 540, 1060) }], B - A - tIns, { handheld: 0.35, minY: -600 }), { dof: false }); Dm.update(lt); };
  SHOTS.push(S2);
})();

// =====================================================================
// S6 — "สุดท้ายเรากลับบ้าน มีแค่ส้มถุงเดียว อาม่าเปิดกล่องคุกกี้ออกมา แปดซอง ไม่เคยถูกแกะเลยสักซอง"
// =====================================================================
(() => {
  const [A, B] = SC.s6, L = t => t - A, tTwo = L(P.G1) - 0.05, tSit = L(P.G2) - 0.05, tIns = L(P.G3) - 0.05;
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = WARM;
  const m = tableScene(S), { set, ama, luk, tin, st, bag, bagD, env, amaPose } = m;
  env.at(0, 0, 0, false);
  const shots = [
    { t: 0, cam: fA(560, 990, 1.15, 540, 1000), to: fA(570, 990, 1.18, 540, 1000) },
    { t: tTwo, cam: fA(550, 950, 2.0, 540, 1000), to: fA(550, 950, 2.08, 540, 1000) },
    { t: tSit, cam: fA(560, 990, 1.5, 540, 1010), to: fA(560, 990, 1.58, 540, 1010) },
  ];
  const XW = lt => lerp(230, 410, ease.inOutSine(prog(lt, 0.1, tTwo - 0.1)));
  const tLift = tSit + 0.15, tOpen = tSit + 1.1;
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, tIns, { handheld: 0.5, minY: -400 }));
    set.update(lt + 40);
    // him: walks in with the oranges, sets them down, head low; then seated across from her
    const putK = prog(lt, tTwo + 0.1, tTwo + 0.7), down = lt > tTwo + 0.6;
    if (si < 2) {
      let p;
      if (lt < tTwo - 0.1) p = walkP(luk, XW(lt), set.ground, 1.2, 1, lt * 5.8, { amp: 11, t: lt, smile: 0.35, head: 8 });
      else p = standP(luk, 410, set.ground, 1.2, 1, { t: lt, smile: 0.2, head: 10 + 12 * prog(lt, tTwo + 0.6, tTwo + 1.0), torso: 16 * Math.sin(Math.PI * putK) });
      const [hx, hy] = down ? [0, 0] : (lt < tTwo ? torsoW(luk, p, 40, -30) : [lerp(torsoW(luk, p, 40, -30)[0], 450, putK), lerp(torsoW(luk, p, 40, -30)[1], TOPY - 92, putK)]);
      if (!down) p.aF = luk.reach(p, hx, hy);
      luk.pose(p);
      if (!down) { const [wx, wy] = wristFW(luk, p); bag.g.setAttribute('transform', `translate(${wx.toFixed(1)},${(wy + 6).toFixed(1)})`); bag.update(lt, lt < tTwo ? 1 : 0.3); }
    } else { const pl = LUK_SIT(luk, lt, { smile: 0.15, head: 12 }); handsOnTable(luk, pl, TOPY, lt); luk.pose(pl); }
    bag.g.setAttribute('display', down ? 'none' : 'inline'); bagD.setAttribute('display', down ? 'inline' : 'none');
    // her: looks up and smiles, a little wave; then lifts the tin onto the table and opens it
    const pa = AMA_SIT(ama, lt, { smile: 1, grin: lt > 0.6 && lt < 1.6 ? 1 : 0, head: si === 0 ? -6 : 6 });
    const kl = ease.inOutCubic(prog(lt, tLift, tLift + 0.6)), ko = ease.inOutCubic(prog(lt, tOpen, tOpen + 0.5));
    const tx = 600, ty = lerp(TOPY + 120, TOPY + 8, kl);
    if (si === 0 && lt > 0.6 && lt < 1.6) { const [hx, hy] = torsoW(ama, pa, 60, -RIG.T + 10); pa.aF = ama.reach(pa, hx, hy - 10 * Math.sin(lt * 10)); }
    else if (si === 2 && lt < tOpen + 0.6) { holdBoth(ama, pa, tx + (lt > tOpen ? 40 * ko : 0), ty - 30 - (lt > tOpen ? 30 * Math.sin(Math.PI * ko) : 0), 50); }
    else handsOnTable(ama, pa, TOPY, lt);
    amaPose(pa);
    tin.g.setAttribute('display', si === 2 ? 'inline' : 'none'); tin.g.setAttribute('transform', `translate(${tx},${ty.toFixed(1)})`); tin.set(ko, 3);
    st(650 - 26, TOPY - 40, lt, 1);
  };
  SHOTS.push(S);
  const S2 = new Shot(A + tIns, B, LAYERS()); S2.grade = WARM;
  const T = tinMacro15(S2);
  const tG = L(P.G4) - tIns;
  S2.update = lt => {
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(540, 1040, 1.02, 540, 980), to: fA(540, 1060, 1.16, 540, 980) }], B - A - tIns, { handheld: 0.4, minY: -600 }), { dof: false });
    T.update(lt);
    const fan = ease.inOutCubic(prog(lt, 0.45, 1.5)), ak = prog(lt, 0.2, 0.45), ar = prog(lt, 1.6, 2.0);
    T.set({ open: 1, n: 8, fan, arm: lt < 2.0 ? { x: lerp(lerp(1000, 380, ak), 1100, ar) + fan * 380 * (1 - ar), y: lerp(lerp(420, 1060, ak), 300, ar) - fan * 40 * (1 - ar) } : null, glint: lt - tG, t: lt });
  };
  SHOTS.push(S2);
})();

// =====================================================================
// S7 — อาม่า: "ลื้อกลับมา อาม่าก็ได้อั่งเปาแล้ว" (her close-up; his, in tears; her hand on his)
// =====================================================================
(() => {
  const [A, B] = SC.s7, L = t => t - A, tHim = L(P.T1) + 0.4, tTwo = L(P.Tend) - 0.55;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const m = tableScene(S), { set, ama, luk, tin, st, bag, env, amaPose } = m;
  bag.g.setAttribute('display', 'none'); env.at(0, 0, 0, false);
  const tr = [tears(set.top, 1513, { n: 3, drift: 1 }), tears(set.top, 1514, { n: 3, drift: -1 })];
  const shots = [
    { t: 0, cam: fA(680, 975, 2.2, 380, 1000), to: fA(680, 975, 2.3, 380, 1000) },
    { t: tHim, cam: fA(400, 975, 2.2, 700, 1000), to: fA(400, 975, 2.3, 700, 1000) },
    { t: tTwo, cam: fA(540, 985, 1.7, 540, 1010), to: fA(540, 985, 1.76, 540, 1010) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.45, minY: -400 }));
    set.update(lt + 50);
    tin.g.setAttribute('transform', `translate(600,${TOPY + 8})`); tin.set(1, 3);
    const reach = ease.inOutCubic(prog(lt, L(P.T1), L(P.T1) + 0.8));
    const pa = AMA_SIT(ama, lt, { smile: 1, head: 8, torso: 4 + reach * 8, mouthO: talk(lt, L(P.T0), L(P.Tend)), eyes: lt > L(P.T1) ? 0.55 : 1 });
    handsOnTable(ama, pa, TOPY, lt); if (reach > 0) pa.aF = ama.reach(pa, lerp(620, 474, reach), TOPY - 12);
    amaPose(pa);
    const pl = LUK_SIT(luk, lt, { smile: lt > tHim + 0.8 ? 0.8 : 0.3, head: 6, mouthO: 0 });
    handsOnTable(luk, pl, TOPY, lt); luk.pose(pl);
    const cry = prog(lt, tHim - 0.2, tHim + 0.3), [e1, e2] = eyesW(luk, pl);
    tr[0](e1[0], e1[1] + 6, cry, lt); tr[1](e2[0], e2[1] + 6, cry, lt);
    st(650 - 26, TOPY - 40, lt, 1);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — "อาม่ายื่นกล่องคืนมา พร้อมซองยี่สิบบาท เหมือนตอนเด็ก" (the tin pushed back, a new envelope, both hands) — a
// dissolve to the same moment 23 years ago — "ตรุษจีนนี้ ไม่มีซอง ก็กลับบ้านได้" (back to today, the crane up into
// the lanterns, hands together on the table, hearts)
// =====================================================================
(() => {
  const [A, B] = SC.s8, L = t => t - A, tGive = L(P.F1) - 0.1, tPast = L(P.F2) - 0.1, tNow = L(P.L0) - 0.1;
  const S = new Shot(A, A + tPast, LAYERS()); S.grade = WARM;
  const m = tableScene(S), { set, ama, luk, tin, st, bag, env, amaPose } = m;
  bag.g.setAttribute('display', 'none');
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(540, 970, 2.15, 540, 1000), to: fA(540, 970, 2.24, 540, 1000) }], tPast, { handheld: 0.45, minY: -400 }));
    set.update(lt + 60);
    const kp = ease.inOutCubic(prog(lt, 0.3, 1.3)), tx = lerp(600, 468, kp);
    tin.g.setAttribute('transform', `translate(${tx.toFixed(1)},${TOPY + 8})`); tin.set(0, 0);
    const kg = ease.inOutCubic(prog(lt, tGive, tGive + 0.6)), ex = lerp(600, 545, kg), ey = lerp(1080, 1052, kg);
    const pa = AMA_SIT(ama, lt, { smile: 1, grin: lt > tGive + 0.8 ? 1 : 0, head: 6, torso: 4 + 10 * Math.sin(Math.PI * kp) });
    if (lt < 1.4) holdBoth(ama, pa, tx + 64, TOPY - 16, 4); else if (lt > tGive - 0.3) holdBoth(ama, pa, ex, ey, 18); else handsOnTable(ama, pa, TOPY, lt);
    amaPose(pa);
    const pl = LUK_SIT(luk, lt, { smile: lt > tGive + 0.5 ? 0.9 : 0.4, head: lt > tGive ? 0 : 8 });
    if (lt > tGive + 0.3) holdBoth(luk, pl, ex, ey, 18); else handsOnTable(luk, pl, TOPY, lt);
    luk.pose(pl);
    env.at(ex, ey, 0, lt > tGive - 0.3);
    st(650 - 26, TOPY - 40, lt, 1);
  };
  SHOTS.push(S);
  // the same moment, 23 years ago
  const SP = new Shot(A + tPast, A + tNow, LAYERS()); SP.grade = SEPIA; SP.fadeIn = 0.45;
  const r = pastRoom(SP);
  SP.update = lt => {
    applyCam(SP, shotCamF(lt, [{ t: 0, cam: fA(800, 975, 2.1, 540, 1000), to: fA(800, 975, 2.18, 540, 1000) }], tNow - tPast, { handheld: 0.4, minY: -400 }));
    r.set.update(lt); pastGive(r, lt, prog(lt, 0.1, 0.8), { grin: lt > 0.7 ? 1 : 0 });
  };
  SHOTS.push(SP);
  // today again: the crane up into the lanterns
  const SN = new Shot(A + tNow, B, LAYERS()); SN.grade = WARM; SN.fadeIn = 0.45;
  const mn = tableScene(SN);
  mn.bag.g.setAttribute('display', 'none');
  const back = behindSvg(SN), hearts = heartsRise(mn.set.top, 540, 1000, 0.5, 8, 1515, 0.32), leak = lightLeak(SN.fx);
  SN.update = lt => {
    const k = ease.inOutSine(prog(lt, 0.3, B - A - tNow));
    const c1 = frameAt(540, 1000, 1.25, 540, 1000), c2 = frameAt(540, 680, 1.0, 540, 800);
    applyCam(SN, shotCamF(lt, [{ t: 0, cam: () => lerpCam(c1, c2, k), to: () => lerpCam(c1, c2, k) }], 9, { handheld: 0.35, minY: -900 }));
    mn.set.update(lt + 70);
    mn.tin.g.setAttribute('transform', `translate(468,${TOPY + 8})`); mn.tin.set(0, 0);
    const pa = AMA_SIT(mn.ama, lt, { smile: 1, grin: Math.sin(lt * 3) > 0 ? 1 : 0, head: 4 });
    const pl = LUK_SIT(mn.luk, lt, { smile: 1, grin: Math.sin(lt * 3 + 1) > 0 ? 1 : 0, head: 2 });
    const hk = ease.inOutCubic(prog(lt, 0.4, 1.2));   // their hands meet on the table
    handsOnTable(mn.ama, pa, TOPY, lt); pa.aF = mn.ama.reach(pa, lerp(600, 556, hk), TOPY - 14);
    handsOnTable(mn.luk, pl, TOPY, lt); pl.aF = mn.luk.reach(pl, lerp(490, 530, hk), TOPY - 10);
    mn.amaPose(pa); mn.luk.pose(pl);
    mn.env.at(512, TOPY - 40, -70, true);
    mn.st(650 - 26, TOPY - 40, lt, 1);
    hearts(lt); leak(lt, 0.2 + 0.45 * k);
  };
  SHOTS.push(SN);
})();

// =====================================================================
// S9 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#a8443a'], [0.6, '#5a1e1a'], [1, '#2a0c0a']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 1516, { color: '#ffc070', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 1517, ['#ffd66b', '#ffffff', '#ffb0a0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '280px';
  duo.innerHTML = `<span class="duo7">${av15('ama', 190)}</span><span class="duo7h">${angpaoIcon15(110)}</span><span class="duo7">${av15('luk', 190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '14px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '590px'; t1.style.font = '700 190px/1 Kanit';
  const digit = html('span', 'tdig', t1, '8');
  const unit = html('span', 'tdig', t1, 'ซอง'); unit.style.marginLeft = '0.25em'; unit.style.fontSize = '110px';
  const t2 = html('div', 'title', wrap, 'ที่อาม่าไม่เคยแกะ'); t2.style.top = '800px'; t2.style.font = '600 92px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'อาม่าไม่ได้รอซอง… อาม่ารอลื้อ'); sub.style.top = '950px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1090px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ลังเลจะกลับบ้าน</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
    spark(lt);
    const kd = spring(lt, 0.4, 15, 6); digit.style.opacity = fadeIn(lt, 0.4, 0.08); digit.style.transform = `translateY(${((1 - kd) * -150).toFixed(1)}px)`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.9, fl(SC.s2[0]) * 0.7, fl(SC.s4[0]), fl(SC.s5[0]) * 0.9, fl(SC.s6[0]) * 0.7, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
