// "128 ช่อ ที่ไม่ใช่ของเรา" — scenes timed to the narration in vo.js (VO.P: H hook, A the florist at dawn, B the rain,
// C 128 deliveries, D he cannot afford one, the title, E the last order, F his own front door, W his wife's line, G what
// receiving feels like, L the lesson). Bookend: the hook is her holding the bouquet out at the door; the ending pulls
// back from that door to the whole house, lights on the gate.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3], s3: [P.C0 - 0.3, P.D0 - 0.3], s4: [P.D0 - 0.3, P.title],
  s5: [P.title, P.E0 - 0.1], s6: [P.E0 - 0.1, P.F0 - 0.3], s7: [P.F0 - 0.3, P.G0 - 0.3], s8: [P.G0 - 0.3, P.end], s9: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const WARM = 'saturate(1.06) contrast(1.04)';
const NIGHT = 'saturate(1.04) contrast(1.06)';
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
function lightCast17(S, set, groups, pups, o = {}) {
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
function shotCamF(lt, shots, end, o = {}) {
  let i = 0; while (i + 1 < shots.length && lt >= shots[i + 1].t) i++;
  const endOf = j => (j + 1 < shots.length ? shots[j + 1].t : end);
  const at = j => { const sh = shots[j]; return lerpCam(sh.cam(lt), (sh.to || sh.cam)(lt), ease.inOutSine(prog(lt, sh.t, endOf(j)))); };
  let cam = at(i);
  if (shots[i].move && i > 0) cam = lerpCam(at(i - 1), cam, ease.inOutCubic(prog(lt, shots[i].t, shots[i].t + shots[i].move)));
  const hh = o.handheld ?? 1;
  cam.x += hh * (Math.sin(lt * 1.1) * 2.2 + Math.sin(lt * 2.7 + 1) * 1.1);
  cam.y += hh * (Math.sin(lt * 0.9 + 2) * 1.8 + Math.sin(lt * 2.3) * 0.9) + (o.bump ? Math.abs(Math.sin(lt * 17)) * o.bump : 0);
  cam.r = (cam.r || 0) + hh * Math.sin(lt * 0.7) * 0.12;
  cam.y = Math.max(cam.y, o.minY ?? 2);
  cam.shot = i;
  return cam;
}
const fA = (...a) => () => frameAt(...a);
const shotIx = (lt, shots) => { let i = 0; while (i + 1 < shots.length && lt >= shots[i + 1].t) i++; return i; };
const talk = (lt, a, b) => (lt > a && lt < b ? 0.35 + 0.35 * Math.max(0, Math.sin(lt * 15)) + 0.2 * Math.max(0, Math.sin(lt * 23 + 1)) : 0);
function eyesW(pup, p) { const [hx, hy] = headW(pup, p), R = pup.o.R, S = p.s * pup.o.s, f = p.f || 1, a = rad((p.torso || 0) + (p.head || 0)); const pt = (lx, ly) => [hx + f * S * (lx * Math.cos(a) - ly * Math.sin(a)), hy + S * (lx * Math.sin(a) + ly * Math.cos(a))]; return [pt(R * 0.5, R * 0.06), pt(R * 0.02, R * 0.06)]; }
// a bouquet in the world, its waist at (x, y)
function bqAt(g, s = 1, o = {}) { const w = svg('g', {}, g), b = svg('g', {}, w); bouquet17(b, s, o); return { g: w, at(x, y, rot = 0, show = true) { w.setAttribute('display', show ? 'inline' : 'none'); w.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${rot.toFixed(1)})`); } }; }

// the rider on his scooter (scooter at x, on the ground); returns the pose
const SCS = 1.1;
function rideP(rider, sc, x, ground, lt, o = {}) {
  const sx = x, sy = ground, seat = [sx + SCS * sc.seat[0], sy + SCS * sc.seat[1]], bar = [sx + SCS * sc.bar[0], sy + SCS * sc.bar[1]];
  const p = { x: seat[0] + 6, y: seat[1] - 16 + (o.bounce ? Math.abs(Math.sin(lt * 17)) * -2 : 0), s: 1.2, f: 1, torso: o.torso ?? 16, head: o.head ?? -8, lF: [18, 72], lB: [24, 80], t: lt, smile: o.smile ?? 0.6, grin: o.grin ?? 0, eyes: o.eyes ?? 1 };
  p.aF = rider.reach(p, bar[0] - 4, bar[1] + 4); p.aB = rider.reach(p, bar[0] - 18, bar[1] + 10);
  return p;
}
const riderPose = (r, p) => { r.pup.pose(p); r.refl(p); };
function makeRider(parent, D) { const pup = new Puppet(parent, RIDER17, D); const refl = reflect17(pup); const helm = helmet17(pup); return { pup, refl, helm }; }
function makeWife(parent, D) { const pup = new Puppet(parent, WIFE17, D); const sk = sarong17(pup, '#2a6a6a', { batik: '#e8b04a' }); return { pup, sk, pose: p => { pup.pose(p); sk(p); } }; }

// =====================================================================
// the doorstep at night: his wife in the doorway (left), him on the step (right)
// =====================================================================
const WX = 470, RX = 700;
function doorScene(S) {
  const set = home17(S), D = S.L.mid.defs;
  const sc = scooter17(set.people, SCS); sc.g.setAttribute('transform', `translate(150,${set.ground}) scale(${SCS})`);
  const wife = makeWife(set.people, D), r = makeRider(set.people, D);
  const bq = bqAt(set.top, 1.05, { card: true });
  const helmetHeld = svg('g', {}, set.top); { const R = 62 * 0.95; svg('path', { d: `M${-R},${R * 0.2} C${-R * 1.1},${-R * 1.2} ${R},${-R * 1.3} ${R},${-R * 0.3} L${R * 0.8},${R * 0.2} Z`, fill: '#2a3a6a', stroke: INK, 'stroke-width': 4.5 }, helmetHeld); svg('rect', { x: -R * 0.5, y: -R * 0.8, width: R * 0.5, height: R * 0.16, rx: 4, fill: '#f2c14e' }, helmetHeld); }
  set.open(1);
  lightCast17(S, set, [set.people], [wife.pup, r.pup], { light: { rim: '#ffd8a0', rimOp: 0.75 }, shadow: { op: 0.2, k: 0.18, blur: 9 } });
  return { set, sc, wife, r, bq, helmetHeld };
}
// k 0..1: she holds the bouquet out to him (he is stunned); back = she pushes it back into his hands
function doorOffer(m, lt, k, o = {}) {
  const pw = standP(m.wife.pup, WX, m.set.ground, 1.2, 1, Object.assign({ t: lt, smile: 0.95, head: 6, torso: 6 * k }, o.wife || {}));
  const bx = lerp(520, 588, ease.inOutCubic(k)), by = lerp(1130, 1105, ease.inOutCubic(k));
  pw.aF = m.wife.pup.reach(pw, bx - 22, by + 10); pw.aB = m.wife.pup.reach(pw, bx - 28, by + 26); m.wife.pose(pw);
  const pr = standP(m.r.pup, RX, m.set.ground, 1.2, -1, Object.assign({ t: lt, smile: 0.3, head: 4 }, o.rider || {}));
  if (o.takes) { pr.aF = m.r.pup.reach(pr, bx + 22, by + 12); pr.aB = m.r.pup.reach(pr, bx + 26, by + 26); }
  else { const [hx, hy] = torsoW(m.r.pup, pr, -30, -10); pr.aB = m.r.pup.reach(pr, hx, hy); }
  riderPose(m.r, pr); m.r.helm(false);
  const [hbx, hby] = o.takes ? [0, 0] : wristBW(m.r.pup, pr); m.helmetHeld.setAttribute('display', o.takes ? 'none' : 'inline'); m.helmetHeld.setAttribute('transform', `translate(${(hbx + 16).toFixed(1)},${(hby + 30).toFixed(1)})`);
  m.bq.at(bx, by, 4, true);
  return { pw, pr };
}

// =====================================================================
// S0 — hook: she holds a bouquet out to him at their door; his face
// =====================================================================
(() => {
  const [A, B] = SC.s0, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = NIGHT;
  const m = doorScene(S), q = glowQ(S.ui, 820, 560);
  const tCU = L(P.H2) - 0.05;
  const shots = [
    { t: 0, cam: fA(585, 930, 1.6, 540, 1000), to: fA(585, 930, 1.68, 540, 1000) },
    { t: tCU, cam: fA(700, 875, 2.2, 300, 1000), to: fA(700, 875, 2.3, 300, 1000) },
  ];
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    m.set.update(lt); m.sc.update(lt, 0);
    const r = doorOffer(m, lt, prog(lt, 0.2, 1.2), { rider: { smile: si === 1 ? 0.2 : 0.3, eyes: 1, head: 6 } });
    q.update(lt, tCU + 0.3); q.el.style.display = si === 1 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — "วาเลนไทน์ปีนี้ เราขี่มอไซค์ส่งดอกไม้ ตั้งแต่หกโมงเช้า": the florist at dawn; bouquets into the box; off he goes
// =====================================================================
(() => {
  const [A, B] = SC.s1, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const set = shopFront17(S, { mode: 'dawn' }), D = S.L.mid.defs;
  const sc = scooter17(set.people, SCS), r = makeRider(set.people, D);
  const bq = bqAt(set.top, 0.9);
  const crate = svg('g', {}, set.top); svg('rect', { x: -70, y: -50, width: 140, height: 50, fill: '#a87a4a', stroke: INK, 'stroke-width': 3.5 }, crate); for (let k = 0; k < 4; k++) { const b = svg('g', { transform: `translate(${-48 + k * 32},-40) scale(0.55)` }, crate); bouquet17(b, 1); }
  crate.setAttribute('transform', `translate(560,${set.ground + 8})`);
  const chip = timeChip17(S.ui, 60, 130, '14 ก.พ. · 06:00', false);
  lightCast17(S, set, [set.people], [r.pup], { light: { rim: '#ffd8e0', rimOp: 0.7 }, shadow: { op: 0.15, k: 0.15, blur: 10 } });
  const tLoad = 0.2, tRide = L(P.A2) - 0.05;
  const shots = [
    { t: 0, cam: fA(470, 1040, 1.25, 540, 1040), to: fA(480, 1040, 1.3, 540, 1040) },
    { t: tRide, cam: fA(420, 1000, 1.35, 540, 1020), to: fA(560, 1000, 1.35, 540, 1020) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt);
    const go = ease.inCubic(prog(lt, tRide + 0.2, B - A)), sx = 300 + go * 700;
    sc.g.setAttribute('transform', `translate(${sx.toFixed(1)},${set.ground}) scale(${SCS})`); sc.update(lt, go > 0 ? 40 : 0);
    let p;
    if (lt < tRide) {   // standing by the box: crate → box, twice
      const cyc = ((lt - tLoad) / 0.9) % 1, k = Math.sin(Math.PI * cyc);
      p = standP(r.pup, 420, set.ground, 1.2, -1, { t: lt, smile: 0.8, head: 4 + 10 * (1 - k), torso: 18 * (1 - k) });
      const hx = lerp(540, 300, k), hy = lerp(set.ground - 60, set.ground - 230, k);
      p.aF = r.pup.reach(p, hx, hy); p.aB = r.pup.reach(p, hx + 14, hy + 10);
      riderPose(r, p); r.helm(true);
      bq.at(hx, hy - 10, -6, lt > tLoad);
    } else { p = rideP(r.pup ? r.pup : r, sc, sx, set.ground, lt, { smile: 0.8, bounce: go > 0 }); riderPose(r, p); r.helm(true); bq.at(0, 0, 0, false); }
    chip.update(lt, 0.2); chip.el.style.display = lt < tRide ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "ฝนตกก็ต้องเอาตัวบังดอกไม้ไว้ ไม่ให้ช้ำสักกลีบ": riding in the rain, a bouquet held in under his jacket
// =====================================================================
(() => {
  const [A, B] = SC.s2, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = 'saturate(0.96) contrast(1.06)';
  const set = street17(S, { mode: 'rain' }), D = S.L.mid.defs;
  const sc = scooter17(set.people, SCS), r = makeRider(set.people, D), bq = bqAt(set.people, 0.85);
  lightCast17(S, set, [set.people], [], { light: { rim: '#d8e0ff', rimOp: 0.5 } });
  const SX = 470, tCU = L(P.B1) - 0.05;
  const shots = [
    { t: 0, cam: fA(470, 1050, 1.15, 540, 1060), to: fA(470, 1050, 1.2, 540, 1060) },
    { t: tCU, cam: fA(480, 960, 1.85, 560, 1000), to: fA(480, 960, 1.95, 560, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6, minY: -300, bump: 1.5 }));
    set.update(lt, lt * 420);
    sc.g.setAttribute('transform', `translate(${SX},${set.ground}) scale(${SCS})`); sc.update(lt, 40, 0.6);
    const hunch = ease.inOutCubic(prog(lt, tCU - 0.4, tCU + 0.2));
    const p = rideP(r.pup, sc, SX, set.ground, lt, { torso: 16 + 14 * hunch, head: -4 + 10 * hunch, smile: 0.3, bounce: true, eyes: 0.8 });
    if (hunch > 0) { const [bx, by] = torsoW(r.pup, p, 52, -RIG.T + 70); p.aB = r.pup.reach(p, bx + 6, by + 6); }   // the back arm holds the bouquet in close
    riderPose(r, p); r.helm(true);
    const [bx, by] = torsoW(r.pup, p, 58, -RIG.T + 92); bq.at(bx, by, 30 + 10 * hunch, hunch > 0.1);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "ส่งไป 128 ช่อ ทุกคนที่ได้ยิ้มหมด": a woman at her gate, smiling; then the count and the faces of the day
// =====================================================================
(() => {
  const [A, B] = SC.s3, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const set = street17(S, { mode: 'sun' }), D = S.L.mid.defs;
  const sc = scooter17(set.people, SCS), r = makeRider(set.people, D);
  const fk = new Puppet(set.people, FOLKS17[0], D), bq = bqAt(set.top, 0.9);
  const card = deliveries17(S.ui, 90, 110);
  const back = behindSvg(S), hearts = heartsRise(set.top, 760, 900, 0.9, 4, 1712, 0.3);
  lightCast17(S, set, [set.people], [r.pup, fk], { light: { rim: '#fff1c4', rimOp: 0.7 }, shadow: { op: 0.17, k: 0.2, blur: 9 } });
  const tFast = L(P.C1) - 0.05, SX = 240;
  const shots = [
    { t: 0, cam: fA(560, 960, 1.55, 540, 1040), to: fA(565, 960, 1.6, 540, 1040) },
    { t: tFast, cam: fA(400, 1060, 1.12, 540, 1080), to: fA(400, 1060, 1.15, 540, 1080) },
  ];
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300, bump: si === 1 ? 1.2 : 0 }));
    set.update(lt, si === 0 ? 0 : (lt - tFast) * 900);
    sc.g.setAttribute('transform', `translate(${SX},${set.ground}) scale(${SCS})`); sc.update(lt, si === 1 ? 70 : 0);
    if (si === 0) {   // he hands it over at the gate; she lights up
      const k = ease.inOutCubic(prog(lt, 0.15, 0.8));
      const p = standP(r.pup, 520, set.ground, 1.2, 1, { t: lt, smile: 0.95, head: 6, torso: 8 * k });
      const bx = lerp(560, 650, k), by = lerp(1120, 1100, k); p.aF = r.pup.reach(p, bx - 20, by + 12); p.aB = r.pup.reach(p, bx - 26, by + 26); riderPose(r, p); r.helm(true);
      const pf = standP(fk, 770, set.ground, 1.2, -1, { t: lt, smile: 1, grin: lt > 0.9 ? 1 : 0, head: 6, eyes: lt > 1.0 ? 0.6 : 1 });
      if (k > 0.6) { pf.aF = fk.reach(pf, bx + 22, by + 10); pf.aB = fk.reach(pf, bx + 26, by + 24); } fk.pose(pf);
      bq.at(bx, by, 0, true); fk.g.setAttribute('display', 'inline');
    } else { fk.g.setAttribute('display', 'none'); bq.at(0, 0, 0, false); const p = rideP(r.pup, sc, SX, set.ground, lt, { smile: 0.95, grin: 1, bounce: true }); riderPose(r, p); r.helm(true); }
    hearts(lt);
    card.update(lt, tFast - 0.1, B - A - 0.2); card.el.style.display = si === 1 ? 'block' : 'none';
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — "แต่ช่อละห้าร้อย เราซื้อให้เมียไม่ไหวสักช่อ": dusk, the florist's window; the day's money; his face
// =====================================================================
(() => {
  const [A, B] = SC.s4, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const set = shopFront17(S, { mode: 'dusk' }), D = S.L.mid.defs;
  const sc = scooter17(set.people, SCS), r = makeRider(set.people, D), ph = phone17(r.pup.prop);
  sc.g.setAttribute('transform', `translate(1100,${set.ground}) scale(${SCS})`);
  const money = money17(S.ui, 100, 120);
  lightCast17(S, set, [set.people], [r.pup], { light: { rim: '#ffd8a0', rimOp: 0.7 }, shadow: { op: 0.2, k: 0.2, blur: 9 } });
  const tMoney = L(P.D0) + 0.3, tCU = L(P.D2) - 0.05;
  const shots = [
    { t: 0, cam: fA(760, 1000, 1.3, 540, 1020), to: fA(740, 1000, 1.36, 540, 1020) },
    { t: tCU, cam: fA(700, 875, 2.2, 300, 1000), to: fA(700, 875, 2.3, 300, 1000) },
  ];
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt); sc.update(lt, 0);
    const look = lt < tMoney;
    const p = standP(r.pup, 700, set.ground, 1.2, -1, { t: lt, smile: look ? 0.4 : 0.1, head: look ? -6 : 16, torso: look ? 0 : 6, eyes: si === 1 ? 0.75 : 1 });
    if (!look) { const [hx, hy] = torsoW(r.pup, p, 70, -RIG.T + 40); p.aF = r.pup.reach(p, hx + 6, hy); p.aB = r.pup.reach(p, hx - 6, hy + 8); p.propRot = -14; }
    riderPose(r, p); r.helm(false); ph.g.setAttribute('display', look ? 'none' : 'inline');
    money.update(lt, tMoney); money.el.style.display = lt > tMoney - 0.05 ? 'block' : 'none';
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — title: 128 ช่อ / ที่ไม่ใช่ของเรา
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = shopFront17(S, { mode: 'dusk' });
  S.L.far.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 1713, { color: '#ffb0c8', rMin: 14, rMax: 40, speed: 12, op: 0.24, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '250px';
  ic.innerHTML = `<span class="fan16">${Array.from({ length: 5 }, (_, i) => `<i style="--i:${i}">${bouquetIcon17(110)}</i>`).join('')}</span>`;
  const icons = [...ic.querySelectorAll('i')];
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 210px/1 Kanit';
  const digits = ['1', '2', '8'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ช่อ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่ไม่ใช่ของเรา'); t2.style.top = '850px'; t2.style.font = '600 104px/1 Kanit'; t2.style.color = '#ffc4d0';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '985px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffc4d0', boxShadow: '0 0 16px rgba(255,180,200,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt); bok(lt);
    icons.forEach((e, i) => { const k = spring(lt, 0.05 + i * 0.06, 16, 6.5), a = (i - 2) * 12 * Math.min(1, k); e.style.opacity = fadeIn(lt, 0.05 + i * 0.06, 0.08); e.style.transform = `translateY(${((1 - k) * -120).toFixed(1)}px) rotate(${(a + Math.sin(lt * 2 + i) * 3).toFixed(1)}deg)`; });
    digits.forEach((d, i) => { const t0 = 0.3 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.55, 14, 7); unit.style.opacity = fadeIn(lt, 0.55, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.75, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.75, 1.25))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 1.05, 1.45)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — "สี่ทุ่ม แอปเด้งออเดอร์สุดท้าย ดอกไม้หนึ่งช่อ ปลายทาง… บ้านเราเอง": night, the order, the route home
// =====================================================================
(() => {
  const [A, B] = SC.s6, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = NIGHT;
  const set = street17(S, { mode: 'night' }), D = S.L.mid.defs;
  const sc = scooter17(set.people, SCS), r = makeRider(set.people, D), ph = phone17(r.pup.prop);
  const ord = order17(S.ui, 150), rt = route17(S.ui, 110, 380), qq = glowQ(S.ui, 780, 620);
  lightCast17(S, set, [set.people], [r.pup], { light: { rim: '#ffd8a0', rimOp: 0.75 }, shadow: { op: 0.2, k: 0.2, blur: 9 } });
  const SX = 420, tRoute = L(P.E2) - 0.1, tHome = L(P.E4) - 0.05, tCU = L(P.E4) + 0.05;
  const shots = [
    { t: 0, cam: fA(520, 1000, 1.3, 540, 1060), to: fA(525, 1000, 1.36, 540, 1060) },
    { t: tCU, cam: fA(470, 875, 2.2, 640, 1000), to: fA(470, 875, 2.3, 640, 1000) },
  ];
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt, 300);
    sc.g.setAttribute('transform', `translate(${SX},${set.ground}) scale(${SCS})`); sc.update(lt, 0, 1);
    // stopped under a lamp, sitting on the scooter, the phone in both hands (from the back)
    const p = rideP(r.pup, sc, SX, set.ground, lt, { torso: 6, head: si === 1 ? 4 : 10, smile: si === 1 ? 0.2 : 0.4, eyes: 1 });
    const [hx, hy] = torsoW(r.pup, p, 78, -RIG.T + 36); p.aF = r.pup.reach(p, hx + 6, hy - 2); p.aB = r.pup.reach(p, hx - 6, hy + 8); p.propRot = -12;
    riderPose(r, p); r.helm(true); ph.glow.setAttribute('opacity', (0.6 + 0.4 * Math.sin(lt * 4)).toFixed(2));
    ord.update(lt, L(P.E1) - 0.3); ord.el.style.display = si === 0 && lt < tRoute + 0.2 ? 'flex' : 'none';
    rt.update(lt, tRoute, tHome); rt.el.style.display = lt > tRoute - 0.05 ? 'block' : 'none';
    qq.update(lt, tCU + 0.25); qq.el.style.display = si === 1 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — "เราเคาะประตูบ้านตัวเอง เมียเปิดมารับ แล้วยื่นช่อนั้นคืนให้เรา" / เมีย: "ทั้งวันส่งให้คนอื่นแล้ว ช่อนี้ของเธอนะ"
// =====================================================================
(() => {
  const [A, B] = SC.s7, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = NIGHT;
  const m = doorScene(S), card = giftCard17(S.ui, 260, 180);
  const tOpen = L(P.F1) - 0.1, tGive = L(P.F2) - 0.05, tBack = L(P.F2) + 0.6, tW = L(P.W0) - 0.1, tCard = L(P.W1);
  const shots = [
    { t: 0, cam: fA(560, 1000, 1.25, 540, 1030), to: fA(565, 1000, 1.3, 540, 1030) },
    { t: tGive - 0.1, cam: fA(585, 930, 1.85, 540, 1000), to: fA(585, 930, 1.95, 540, 1000) },
    { t: tW, cam: fA(470, 875, 2.2, 800, 1000), to: fA(470, 875, 2.3, 800, 1000) },
  ];
  const XW = lt => lerp(860, RX, ease.inOutSine(prog(lt, 0.05, 1.3)));
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    m.set.update(lt); m.sc.update(lt, 0);
    const op = ease.inOutCubic(prog(lt, tOpen, tOpen + 0.7)); m.set.open(op);
    m.wife.pup.g.setAttribute('display', op > 0.3 ? 'inline' : 'none');
    if (lt < tGive) {
      // he walks up with the bouquet, knocks; she opens
      let pr;
      if (lt < 1.3) { pr = walkP(m.r.pup, XW(lt), m.set.ground, 1.2, -1, lt * 6, { amp: 12, t: lt, smile: 0.5, head: 4 }); }
      else pr = standP(m.r.pup, RX, m.set.ground, 1.2, -1, { t: lt, smile: 0.5, head: 4 });
      const [bx, by] = torsoW(m.r.pup, pr, 46, -RIG.T + 108); pr.aB = m.r.pup.reach(pr, bx, by + 8);
      if (lt > 1.3 && lt < tOpen) { const kn = Math.abs(Math.sin((lt - 1.3) * 9)); pr.aF = m.r.pup.reach(pr, 600 + kn * 14, 980); }
      riderPose(m.r, pr); m.r.helm(lt < 1.6); m.helmetHeld.setAttribute('display', 'none');
      m.bq.at(bx + 10, by + 4, -10, true);
      const pw = standP(m.wife.pup, WX, m.set.ground, 1.2, 1, { t: lt, smile: 0.95, head: 4 }); m.wife.pose(pw);
    } else if (lt < tBack) {   // habit: he holds it out to her — "delivery"
      const k = ease.inOutCubic(prog(lt, tGive, tGive + 0.5));
      const pr = standP(m.r.pup, RX, m.set.ground, 1.2, -1, { t: lt, smile: 0.7, head: 8, torso: 6 * k });
      const bx = lerp(640, 560, k), by = lerp(1120, 1105, k); pr.aF = m.r.pup.reach(pr, bx + 22, by + 12); pr.aB = m.r.pup.reach(pr, bx + 26, by + 26); riderPose(m.r, pr); m.r.helm(false);
      const pw = standP(m.wife.pup, WX, m.set.ground, 1.2, 1, { t: lt, smile: 1, head: 6 }); pw.aF = m.wife.pup.reach(pw, bx - 22, by + 12); pw.aB = m.wife.pup.reach(pw, bx - 26, by + 26); m.wife.pose(pw);
      m.bq.at(bx, by, 0, true); m.helmetHeld.setAttribute('display', 'none');
    } else {   // she pushes it back into his hands
      doorOffer(m, lt, 1 - 0.4 * ease.inOutCubic(prog(lt, tBack, tBack + 0.6)), { takes: true, wife: { mouthO: talk(lt, L(P.W0), L(P.Wend)), smile: 1 }, rider: { smile: 0.35, eyes: si === 2 ? 1 : 0.9, head: 6 } });
    }
    card.update(lt, tCard); card.el.style.display = lt > tCard - 0.05 ? 'block' : 'none';
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — "ส่งดอกไม้มาทั้งวัน เพิ่งรู้ว่าตอนได้รับ มันรู้สึกแบบนี้นี่เอง" (his face; tears and a smile) / "วาเลนไทน์นี้ ส่งความรัก
// ให้คนที่ส่งให้คนอื่นทั้งวันบ้างนะ" (the two at the door; the camera pulls back to the house, the gate lights, the moon)
// =====================================================================
(() => {
  const [A, B] = SC.s8, L = t => t - A, tWide = L(P.L0) - 0.35;
  const S = new Shot(A, A + tWide, LAYERS()); S.grade = NIGHT;
  const m = doorScene(S), tr = [tears(m.set.top, 1714, { n: 3, drift: -1 }), tears(m.set.top, 1715, { n: 3, drift: 1 })];
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(700, 875, 2.2, 300, 1000), to: fA(700, 875, 2.32, 300, 1000) }], tWide, { handheld: 0.45, minY: -300 }));
    m.set.update(lt); m.sc.update(lt, 0);
    const r = doorOffer(m, lt, 0.6, { takes: true, rider: { smile: lerp(0.4, 1, prog(lt, 1.0, 2.0)), head: lerp(10, -2, prog(lt, 0.5, 1.5)), eyes: 0.75 }, wife: { smile: 1 } });
    const cry = prog(lt, 0.3, 0.9), [e1, e2] = eyesW(m.r.pup, r.pr); tr[0](e1[0], e1[1] + 6, cry, lt); tr[1](e2[0], e2[1] + 6, cry, lt);
  };
  SHOTS.push(S);
  const S2 = new Shot(A + tWide, B, LAYERS()); S2.grade = NIGHT; S2.fadeIn = 0.4;
  const m2 = doorScene(S2), hearts = heartsRise(m2.set.top, 590, 860, 0.4, 8, 1716, 0.32), leak = lightLeak(S2.fx);
  S2.update = lt => {
    const k = ease.inOutSine(prog(lt, 0.2, B - A - tWide));
    const c1 = frameAt(590, 930, 1.6, 540, 1010), c2 = frameAt(540, 820, 1.0, 540, 880);
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: () => lerpCam(c1, c2, k), to: () => lerpCam(c1, c2, k) }], 9, { handheld: 0.3, minY: -300 }));
    m2.set.update(lt); m2.sc.update(lt, 0);
    // close together in the doorway: her hand on his arm, his on the bouquet
    const pw = standP(m2.wife.pup, WX + 30, m2.set.ground, 1.2, 1, { t: lt, smile: 1, grin: Math.sin(lt * 3) > 0.4 ? 1 : 0, head: 4, torso: 4 });
    const pr = standP(m2.r.pup, RX - 40, m2.set.ground, 1.2, -1, { t: lt, smile: 1, grin: Math.sin(lt * 3 + 1) > 0.4 ? 1 : 0, head: 2 });
    const [ax, ay] = torsoW(m2.r.pup, pr, 20, -RIG.T + 40); pw.aF = m2.wife.pup.reach(pw, ax, ay); const [wx, wy] = torsoW(m2.wife.pup, pw, 40, -30); pw.aB = m2.wife.pup.reach(pw, wx, wy + 10); m2.wife.pose(pw);
    const [bx, by] = torsoW(m2.r.pup, pr, 50, -RIG.T + 92); pr.aF = m2.r.pup.reach(pr, bx, by + 6); pr.aB = m2.r.pup.reach(pr, bx + 8, by + 18); riderPose(m2.r, pr); m2.r.helm(false);
    m2.bq.at(bx, by + 4, -8, true); m2.helmetHeld.setAttribute('display', 'none');
    hearts(lt); leak(lt, 0.15 + 0.4 * k);
  };
  SHOTS.push(S2);
})();

// =====================================================================
// S9 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#c8606a'], [0.6, '#6a2238'], [1, '#2a0c1a']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 1717, { color: '#ffc0c8', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 1718, ['#ffd66b', '#ffffff', '#ffb0c0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '270px';
  duo.innerHTML = `<span class="duo7">${av17('rider', 190)}</span><span class="duo7h">${bouquetIcon17(100)}</span><span class="duo7">${av17('wife', 190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '14px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '590px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['1', '2', '8'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ช่อ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่ไม่ใช่ของเรา'); t2.style.top = '800px'; t2.style.font = '600 92px/1 Kanit'; t2.style.color = '#ffc4d0';
  const sub = html('div', 'title', wrap, 'ช่อที่ 129 ส่งถึงบ้านเราเอง ♥'); sub.style.top = '950px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9ee';
  const cta = html('div', 'cta', wrap); cta.style.top = '1090px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ทำงานหนักวันวาเลนไทน์</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.65, 14, 7); unit.style.opacity = fadeIn(lt, 0.65, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.8, fl(SC.s4[0]) * 0.6, fl(SC.s5[0]), fl(SC.s6[0]) * 0.6, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = Promise.all(['400 40px Charm', '700 40px Charm'].map(f => document.fonts.load(f, 'กขค 0123'))).then(() => document.fonts.ready).then(() => true);
