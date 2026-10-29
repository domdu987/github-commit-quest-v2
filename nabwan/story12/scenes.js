// "9 ผ้าพันคอที่ไม่เคยได้ใช้" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..E3; H is the
// "ถ้า..." hook). Shot language as in pro.js: every scene is a shot list on a lit set (wide → medium → close-up / insert).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0: [0, P.A0 - 0.3], s1a: [P.A0 - 0.3, P.A3 - 0.15], s1b: [P.A3 - 0.15, P.B0 - 0.3], s2: [P.B0 - 0.3, P.B3 - 0.1], s2i: [P.B3 - 0.1, P.C0 - 0.3],
  s3: [P.C0 - 0.3, P.C1 - 0.1], s3i: [P.C1 - 0.1, P.Cend], s3b: [P.Cend, P.title], s4: [P.title, P.D0 - 0.1], s5: [P.D0 - 0.1, P.end], s6: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
const SIT = { lF: [8, 172], lB: [18, 166] };
function lightCast(S, set, pups, o = {}) {
  const Lt = set.light || {};
  set.people.setAttribute('filter', charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {})));
  return pups.map(p => castShadow(p, set.shadowL, S.L.mid.defs, Object.assign({ lx: Lt.lx }, o.shadow || {})));
}
function standP(pup, x, ground, s, f, o = {}) {
  const S = s * pup.o.s;
  return Object.assign({ x, y: ground - LEG * S, s, f, torso: 0, head: 0, lF: [88, 92], lB: [92, 88], aF: [96, 92], aB: [86, 92], smile: 0.6 }, o);
}
function walkP(pup, x, ground, s, f, ph, o = {}) {
  const g = gait(ph, o.amp ?? 16), S = s * pup.o.s;
  const p = Object.assign({ x, y: ground - LEG * S + g.bob * S, s, f, head: -2, lF: g.lF, lB: g.lB, aF: g.aF, aB: g.aB, smile: 0.6 }, o);
  p.torso = g.torso + (o.lean || 0);
  return p;
}
function sitP(pup, x, floor, s, f, o = {}) { return Object.assign({ x, y: floor - 18, s, f, torso: 8, head: 6, lF: SIT.lF, lB: SIT.lB, aF: [70, 30], aB: [80, 40], smile: 0.7 }, o); }
// knitting hands in the lap: both wrists near the lap front, a small alternating stitch motion; returns [front wrist, back wrist] targets
function knitHands(pup, p, lt, speed = 1, amp = 1) {
  const a = lt * 7 * speed;
  const [fx, fy] = torsoW(pup, p, 62 + Math.sin(a) * 6 * amp, -46 + Math.cos(a * 1.3) * 5 * amp);
  const [bx, by] = torsoW(pup, p, 30 + Math.sin(a + 2) * 5 * amp, -40 + Math.cos(a) * 4 * amp);
  p.aF = pup.reach(p, fx, fy); p.aB = pup.reach(p, bx, by);   // (reach is front-arm IK; good enough for the back arm in the lap)
  return [[fx, fy], [bx, by]];
}
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
// a scarf hanging from a hand (prop frame); returns set(colour)
function scarfDrape(parent, defs, c0, len = 150) {
  const g = svg('g', {}, parent);
  const body = svg('path', { stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  const fr = svg('path', { fill: 'none', 'stroke-width': 3, 'stroke-linecap': 'round' }, g);
  return (c, t = 0, show = true) => {
    g.setAttribute('display', show ? 'inline' : 'none');
    const sw = Math.sin(t * 2.4) * 8;
    body.setAttribute('fill', knitFill(defs, c));
    body.setAttribute('d', `M-16,-6 L16,-6 Q${20 + sw * 0.5},${len * 0.5} ${16 + sw},${len} L${-16 + sw},${len} Q${-20 + sw * 0.5},${len * 0.5} -16,-6 Z`);
    fr.setAttribute('stroke', shade(c, -18));
    fr.setAttribute('d', `M${-12 + sw},${len} l-2,14 M${-2 + sw},${len} l0,15 M${8 + sw},${len} l2,14`);
  };
}
// a small box held in the hand
function boxProp(parent, s = 0.55) {
  const g = svg('g', { transform: `translate(0,-10) scale(${s})` }, parent);
  parcel(g, 0, 40, 1, { string: true });
  return g;
}
// a parcel on the floor that can drop in with a bounce: update(t, t0)
function floorParcel(parent, x, y, s = 0.7, o = {}) {
  const g = svg('g', {}, parent), p = parcel(g, 0, 0, s, o);
  return (t, t0, open = 0) => {
    const k = t < t0 ? -1 : Math.min(1, (t - t0) / 0.25), b = t > t0 + 0.25 ? Math.exp(-(t - t0 - 0.25) * 9) * Math.abs(Math.sin((t - t0 - 0.25) * 22)) * 12 : 0;
    g.setAttribute('display', k < 0 ? 'none' : 'inline');
    g.setAttribute('transform', `translate(${x},${(y - (1 - Math.max(0, k)) * 260 - b).toFixed(1)})`);
  };
}

// =====================================================================
// S0 — hook: dawn on ยาย's porch; she knits by the charcoal stove; her hands slow, shake and stop on a half scarf
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = lannaPorch(S, { mode: 'dawn', stoveX: 640, catX: 770 }), L = t => t - A, G = set.ground;
  const yai = new Puppet(set.people, YAI12, S.L.mid.defs);
  lightCast(S, set, [yai], { light: { rim: '#ffe2b0', rimOp: 0.7 }, shadow: { op: 0.2, k: 0.22, blur: 9 } });
  const knit = knitPiece(set.top, S.L.mid.defs, SCARF10);
  const ball = yarnBall(set.top, S.L.mid.defs, 380, 1286, 18, SCARF10);
  const puff = breath(set.top, 31);
  const q = glowQ(S.ui, 780, 640);
  const shots = [
    { t: 0, cam: fA(470, 1110, 1.35, 540, 1040), to: fA(470, 1110, 1.43, 540, 1040) },
    { t: L(P.H2) - 0.05, cam: fA(400, 1210, 3.0, 560, 1160), to: fA(400, 1210, 3.2, 560, 1160) },
    { t: L(P.H4) - 0.05, cam: fA(360, 1110, 2.2, 520, 1160), to: fA(360, 1110, 2.32, 520, 1160) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt);
    const stop = prog(lt, L(P.H3) - 0.2, L(P.H3) + 0.3), shake = lt > L(P.H3) - 0.2 ? 1 : 0;
    const p = sitP(yai, 300, G, 1.2, 1, { t: lt, torso: 12, head: lt > L(P.H4) - 0.1 ? 22 : 16, smile: lerp(0.75, 0.35, stop) });
    const [wf, wb] = knitHands(yai, p, lt, 1 - 0.9 * stop, 1 - stop);
    if (shake) { const j = Math.sin(lt * 60) * 3 * stop; p.aF = yai.reach(p, wf[0] + j, wf[1] + j * 0.6); }
    yai.pose(p);
    const a = wristFW(yai, p), b = wristBW(yai, p);
    knit.set([Math.min(a[0], b[0]) + 6, Math.min(a[1], b[1]) + 4], [Math.max(a[0], b[0]) - 6, Math.max(a[1], b[1]) + 4], 70, lt, [380, 1280]);
    puff(yai, p, lt);
    q.update(lt, L(P.H4) + 0.15);
    setGrade(S, (1 - prog(lt, 0, 0.5)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1a — "9 ปีแล้ว ที่ยายที่เชียงรายถักผ้าพันคอ": the village post office at dawn; the box is stamped and sent
// =====================================================================
(() => {
  const [A, B] = SC.s1a;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = villagePost(S), L = t => t - A, G = set.ground;
  const yai = new Puppet(set.people, YAI12, S.L.mid.defs);
  const held = boxProp(yai.prop, 0.5);
  lightCast(S, set, [yai], { light: { rim: '#ffe2b0', rimOp: 0.7 }, shadow: { op: 0.16, k: 0.2, blur: 10 } });
  const onLedge = svg('g', {}, set.top); parcel(onLedge, 0, 0, 0.5, { string: true });
  const stampMark = svg('g', { opacity: 0 }, onLedge);
  svg('circle', { cx: 10, cy: -24, r: 16, fill: 'none', stroke: '#e0453b', 'stroke-width': 4 }, stampMark);
  svg('path', { d: 'M0,-24 l20,0 M10,-34 l0,20', stroke: '#e0453b', 'stroke-width': 3 }, stampMark);
  const arm = svg('g', {}, set.top);   // the clerk's arm with a rubber stamp, from inside the window
  svg('path', { d: 'M760,1020 L700,1100', stroke: INK, 'stroke-width': 30, 'stroke-linecap': 'round' }, arm);
  svg('path', { d: 'M760,1020 L700,1100', stroke: '#4a7bd8', 'stroke-width': 21, 'stroke-linecap': 'round' }, arm);
  svg('rect', { x: 680, y: 1096, width: 34, height: 26, rx: 4, fill: '#8a5a32', stroke: INK, 'stroke-width': 3 }, arm);
  svg('rect', { x: 674, y: 1120, width: 46, height: 10, rx: 3, fill: '#2a2226' }, arm);
  const yr = yearChip12(S.ui, 40, 120, 'ส่งให้หลาน พ.ศ.');
  const route = routeCard12(S.ui, 230, 300);
  const puff = breath(set.top, 33);
  const tPut = L(P.A2) - 0.3, tStamp = L(P.A2) + 0.15;
  const LX = 660, LY = 1214;   // the counter ledge
  const shots = [
    { t: 0, cam: fA(560, 1150, 1.15, 540, 1060), to: fA(570, 1150, 1.2, 540, 1060) },
    { t: L(P.A2) - 0.1, cam: fA(610, 1130, 1.85, 540, 1160), to: fA(615, 1130, 1.95, 540, 1160) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt);
    const x = lerp(280, 520, ease.outCubic(prog(lt, 0, tPut - 0.1)));
    const walking = lt < tPut - 0.15;
    const p = walking ? walkP(yai, x, G, 1.2, 1, x * 0.045, { amp: 11, t: lt, smile: 0.8, head: 2, lean: 6 }) : standP(yai, x, G, 1.2, 1, { t: lt, smile: 0.85, head: 6, torso: 6 });
    if (lt < tPut) { const [hx, hy] = torsoW(yai, p, 60, -70); p.aF = yai.reach(p, hx + (walking ? 0 : 60 * prog(lt, tPut - 0.4, tPut)), hy); }
    else { const k = prog(lt, tPut, tPut + 0.4); p.aF = yai.reach(p, lerp(LX - 20, x + 60, k), lerp(LY - 30, LY - 20, k)); }
    yai.pose(p);
    held.setAttribute('display', lt < tPut ? 'inline' : 'none');
    onLedge.setAttribute('display', lt >= tPut ? 'inline' : 'none');
    const fly = prog(lt, L(P.A2) + 0.55, L(P.A2) + 0.75);
    onLedge.setAttribute('transform', `translate(${LX + fly * 300},${LY - fly * 60}) scale(${1 - fly})`);
    const sk = lt - tStamp;
    arm.setAttribute('opacity', sk > -0.25 && sk < 0.6 ? 1 : 0);
    arm.setAttribute('transform', `translate(0,${(sk < 0 ? -60 : sk < 0.12 ? -60 + 500 * sk : Math.max(-60, 0 - 300 * (sk - 0.12))).toFixed(1)})`);
    stampMark.setAttribute('opacity', sk > 0.1 ? 1 : 0);
    puff(yai, p, lt);
    const r = rollValue(lt, L(P.A0) + 0.1, L(P.A1) + 0.2, 2561, 2569);
    yr.update(lt, L(P.A0) - 0.05, r.v, r.speed);
    route.update(lt, L(P.A2) + 0.25, prog(lt, L(P.A2) + 0.55, B - A + 0.3));
    route.el.style.display = lt > L(P.A2) + 0.2 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1b — "ส่งมาให้เราที่กรุงเทพฯ ทุกหน้าหนาว": the box lands at the condo door; a scarf a winter, nine colours
// =====================================================================
(() => {
  const [A, B] = SC.s1b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = studio(S, { mode: 'night', month: 'พ.ย.' }), L = t => t - A, G = set.ground;
  const lan = new Puppet(set.people, LAN12, S.L.mid.defs);
  const drape = scarfDrape(lan.prop, S.L.mid.defs, SCARF[0]);
  lightCast(S, set, [lan], { light: { rim: '#ffe2b0', rimOp: 0.6 }, shadow: { op: 0.22, k: 0.25 } });
  const box = floorParcel(set.parcels, 120, G + 4, 0.75, { string: true });
  const row = scarfRow12(S.ui, 60, 140);
  const tLand = 0.12, n0 = 0.55, n1 = L(P.Aend) - 0.15;
  const nT = SCARF.map((_, i) => lerp(n0, n1, i / 8));
  const shots = [{ t: 0, cam: fA(330, 1120, 1.5, 540, 1100), to: fA(340, 1120, 1.6, 540, 1100) }];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt);
    box(lt, tLand);
    const n = nT.filter(v => lt >= v).length, c = SCARF[Math.max(0, n - 1)];
    const p = standP(lan, 330, G, 1.2, -1, { t: lt, smile: 0.95, grin: n > 0 && lt < nT[Math.max(0, n - 1)] + 0.3 ? 1 : 0, head: -10 });
    const lift = ease.outBack(prog(lt, n0 - 0.3, n0));
    const [hx, hy] = torsoW(lan, p, 70, lerp(-20, -150, lift));
    p.aF = lan.reach(p, hx, hy + Math.sin(lt * 9) * 3);
    p.aB = [-50, -100];
    lan.pose(p);
    drape(c, lt, lt > n0 - 0.3);
    row.update(lt, 0.25, n, nT);
    setGrade(S, (1 - prog(lt, 0, 0.2)) * 5);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "แต่กรุงเทพฯไม่เคยหนาวพอ ผ้าพันคอของยายเลยนอนพับอยู่ในลิ้นชัก": a blazing afternoon; the scarf comes off and
// goes into the drawer
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.12) contrast(1.04) brightness(1.03)';
  const set = studio(S, { mode: 'day', month: 'ธ.ค.' }), L = t => t - A, G = set.ground;
  const lan = new Puppet(set.people, LAN12, S.L.mid.defs);
  const wear = scarfWear(lan, S.L.mid.defs, [SCARF[5]], { tail: 64 });
  const drape = scarfDrape(lan.prop, S.L.mid.defs, SCARF[5], 120);
  lightCast(S, set, [lan], { light: { rim: '#fff1c4', rimOp: 0.8 }, shadow: { op: 0.22, k: 0.28, blur: 7 } });
  const temp = tempChip12(S.ui, 40, 120, true);
  const sweat = svg('g', {}, set.top);
  const drops = Array.from({ length: 4 }, () => svg('path', { fill: '#bfe6ff', stroke: INK, 'stroke-width': 2 }, sweat));
  const tOff = L(P.B1) - 0.15, tOpen = L(P.B2) - 0.1, tIn = L(P.B2) + 0.5;
  const shots = [
    { t: 0, cam: fA(560, 1040, 1.5, 560, 1080), to: fA(565, 1040, 1.58, 560, 1080) },
    { t: L(P.B1) - 0.1, cam: fA(470, 1080, 1.6, 540, 1100), to: fA(475, 1080, 1.68, 540, 1100) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5 }));
    const dk = ease.inOutSine(prog(lt, tOpen, tOpen + 0.4));
    set.update(lt, { drawer: dk });
    const off = lt > tOff;
    const p = standP(lan, 600, G, 1.2, -1, { t: lt, smile: off ? 0.6 : 0.3, head: off ? 4 : -8, mouthO: !off && lt > 0.6 ? 0.4 : 0, eyes: !off && Math.sin(lt * 2) > 0.6 ? 0.2 : null });
    if (!off) { p.aB = [-110 + Math.sin(lt * 14) * 25, -150 + Math.sin(lt * 14) * 20]; const [hx, hy] = torsoW(lan, p, 40, -100); p.aF = lan.reach(p, hx, hy); }   // fanning herself, tugging the scarf
    else if (lt < tOpen) { const [hx, hy] = torsoW(lan, p, 60, -70); p.aF = lan.reach(p, hx, hy); }
    else { const k = ease.inOutSine(prog(lt, tOpen, tIn)); p.aF = lan.reach(p, lerp(set.DX + 250, set.DX + 180, k), lerp(set.DY + 40, set.DY - 10, k)); p.torso = 10 * k; }
    lan.pose(p);
    wear.hidden = off; wear(p, lt);
    drape(SCARF[5], lt, off && lt < tIn + 0.1);
    // sweat beads running down her temple while the scarf is on
    const [hx, hy] = torsoW(lan, p, HEAD_C[0], HEAD_C[1]);
    drops.forEach((d, i) => { const u = ((lt * 0.9 + i / 4) % 1), x = hx + (i % 2 ? -50 : 60) * 1.2 * -1, y = hy - 30 + u * 70, s = 6; d.setAttribute('d', `M${x},${y - s * 2} C${x + s},${y - s * 0.4} ${x + s},${y + s} ${x},${y + s} C${x - s},${y + s} ${x - s},${y - s * 0.4} ${x},${y - s * 2} Z`); d.setAttribute('opacity', (!off ? Math.sin(Math.PI * u) : 0).toFixed(2)); });
    const r = rollValue(lt, 0.3, 1.2, 28, 35);
    temp.update(lt, 0.3, r.v, r.speed);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  // wearing toggle: scarfWear reads o.hidden at call time, so wrap it
  SHOTS.push(S);
})();

// insert: the drawer from above — nine scarves, folded, never used — and it slides shut
(() => {
  const [A, B] = SC.s2i;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.grade = 'saturate(1.06) contrast(1.05)';
  const G = S.L.bg, d = G.defs;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: '#5a321e' }, G.s);
  svg('rect', { x: 60, y: 420, width: 960, height: 1160, rx: 18, fill: '#7a4a2a', stroke: INK, 'stroke-width': 10 }, G.s);
  svg('rect', { x: 90, y: 450, width: 900, height: 1100, rx: 10, fill: lin(d, [[0, '#4a2a18'], [1, '#3a2012']]) }, G.s);
  SCARF.forEach((c, i) => { const row = Math.floor(i / 3), col = i % 3; scarfFolded(G.s, d, 120 + col * 290, 640 + row * 330, 260, 170, c); });
  svg('rect', { x: 90, y: 450, width: 900, height: 60, fill: '#000', opacity: 0.25 }, G.s);
  const lid = svg('rect', { x: 60, y: 420, width: 960, height: 1160, rx: 18, fill: '#c88a5a', stroke: INK, 'stroke-width': 10 }, G.s);
  const handle = svg('rect', { x: 440, y: 0, width: 200, height: 36, rx: 18, fill: '#7a4a2a' }, G.s);
  const shadow = svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: '#000', opacity: 0 }, G.s);
  vignette(G.s, d, 0.55);
  const used = usedChip12(S.ui, 300, 180);
  const tClose = 0.95;
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.04, 1.1, prog(lt, 0, B - A)), fx: 540, fy: 1000, r: Math.sin(lt * 0.7) * 0.1 });
    const k = ease.inOutCubic(prog(lt, tClose, B - A - 0.05));
    lid.setAttribute('height', (1160 * k + 1).toFixed(1));   // the dresser top slides over as the drawer goes in
    handle.setAttribute('y', (420 + 1160 * k - 50).toFixed(1)); handle.setAttribute('opacity', k > 0.08 ? 1 : 0);
    shadow.setAttribute('opacity', (0.45 * k).toFixed(3));
    used.update(lt, 0.12);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "ปีนี้กล่องของยายมาช้า": a December night; a smaller box at the door
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.02) contrast(1.05)';
  const set = studio(S, { mode: 'night', month: 'ธ.ค.' }), L = t => t - A, G = set.ground;
  const lan = new Puppet(set.people, LAN12, S.L.mid.defs);
  const held = boxProp(lan.prop, 0.42);
  lightCast(S, set, [lan], { light: { rim: '#ffe2b0', rimOp: 0.6 }, shadow: { op: 0.22, k: 0.25 } });
  const late = lateCard12(S.ui, 180, 150);
  const shots = [
    { t: 0, cam: fA(320, 1080, 1.55, 540, 1120), to: fA(330, 1080, 1.66, 540, 1120) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt);
    const p = standP(lan, 330, G, 1.2, -1, { t: lt, smile: 0.45, head: 14 + Math.sin(lt * 1.5) * 4 });
    const [hx, hy] = torsoW(lan, p, 66, -60 + Math.sin(lt * 3) * 4);
    p.aF = lan.reach(p, hx, hy); p.aB = lan.reach(p, hx - 30, hy + 10);
    p.propRot = Math.sin(lt * 4) * 6;   // turning the light box over in her hands
    lan.pose(p);
    late.update(lt, L(P.C0) + 0.15);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// insert: the open box — half a scarf still on its needles (the missing half drawn as a dashed ghost), a yarn ball, the note
(() => {
  const [A, B] = SC.s3i;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.grade = 'saturate(1.04) contrast(1.05)';
  const G = S.L.bg, d = G.defs, L = t => t - A;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: '#3a2018' }, G.s);
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(d, [[0, '#ffd59a', 0.35], [1, '#ffd59a', 0]], { cx: 0.5, cy: 0.45, r: 0.6 }) }, G.s);
  // box seen from above: flaps open
  svg('path', { d: 'M140,560 L940,560 L940,1500 L140,1500 Z', fill: '#c99a5a', stroke: INK, 'stroke-width': 8 }, G.s);
  svg('path', { d: 'M180,600 L900,600 L900,1460 L180,1460 Z', fill: '#8a6438', stroke: INK, 'stroke-width': 5 }, G.s);
  for (const fl of ['M140,560 L940,560 L860,380 L220,380 Z', 'M140,1500 L940,1500 L860,1680 L220,1680 Z', 'M140,560 L140,1500 L-20,1400 L-20,660 Z', 'M940,560 L940,1500 L1100,1400 L1100,660 Z']) svg('path', { d: fl, fill: '#d9ae6e', stroke: INK, 'stroke-width': 6, 'stroke-linejoin': 'round' }, G.s);
  svg('path', { d: 'M500,380 L580,380 L580,560 L500,560 Z', fill: '#e8d2a0', opacity: 0.9 }, G.s);   // torn tape
  // the half scarf on its needles, and the dashed ghost of the half that isn't there
  const sc = svg('g', {}, G.s);
  svg('rect', { x: 260, y: 700, width: 300, height: 380, rx: 16, fill: knitFill(d, SCARF10), stroke: INK, 'stroke-width': 6 }, sc);
  svg('path', { d: 'M266,860 L554,860', stroke: '#f6efe2', 'stroke-width': 18 }, sc);
  svg('path', { d: 'M266,720 L554,720', stroke: shade(SCARF10, -20), 'stroke-width': 4 }, sc);
  for (const [x1, y1, x2, y2] of [[200, 760, 640, 650], [220, 800, 660, 720]]) { svg('path', { d: `M${x1},${y1} L${x2},${y2}`, stroke: INK, 'stroke-width': 16, 'stroke-linecap': 'round' }, sc); svg('path', { d: `M${x1},${y1} L${x2},${y2}`, stroke: '#d9b48a', 'stroke-width': 9, 'stroke-linecap': 'round' }, sc); }
  const ghost = svg('rect', { x: 260, y: 1080, width: 300, height: 340, rx: 16, fill: 'none', stroke: '#fff6dc', 'stroke-width': 7, 'stroke-dasharray': '22 16' }, G.s);
  const ghostTag = svg('g', {}, G.s);
  svg('rect', { x: 300, y: 1210, width: 220, height: 80, rx: 40, fill: '#fff6dc', stroke: INK, 'stroke-width': 4 }, ghostTag);
  wtext(ghostTag, 410, 1264, 'อีกครึ่ง?', 44, '#c8343c', { w: 700 });
  yarnBall(G.s, d, 720, 1140, 90, SCARF10);
  svg('path', { d: 'M560,880 Q660,1000 700,1060', fill: 'none', stroke: SCARF10, 'stroke-width': 6 }, G.s);
  const folded = svg('g', {}, G.s);   // the folded note in the box (lifts away when it opens)
  svg('rect', { x: 620, y: 1260, width: 220, height: 150, rx: 6, fill: '#fbf7ef', stroke: INK, 'stroke-width': 4, transform: 'rotate(-8 730 1335)' }, folded);
  svg('path', { d: 'M640,1300 l160,-20 M644,1330 l120,-16', stroke: '#4a7bd8', 'stroke-width': 4, transform: 'rotate(-8 730 1335)' }, folded);
  vignette(G.s, d, 0.55);
  svg('rect', { x: -40, y: 1440, width: 1160, height: 520, fill: lin(d, [[0, '#1e0e08', 0], [0.42, '#1e0e08', 0.72], [1, '#1e0e08', 0.9]]) }, G.s);   // keeps the captions off the light flap
  const back = html('div', 'blur12', S.ui);
  const note = noteCard12(S.ui, 150, 560, ['มือยายสั่นแล้ว', 'หลานทำต่อให้ยายหน่อยนะ']);
  const tNote = L(P.C3) + 0.2;
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.04, 1.12, prog(lt, 0, B - A)), fx: 540, fy: 1000, r: Math.sin(lt * 0.7) * 0.1 });
    const gk = prog(lt, L(P.C2) - 0.05, L(P.C2) + 0.35);
    ghost.setAttribute('opacity', (gk * (1 - prog(lt, tNote - 0.2, tNote))).toFixed(3)); ghost.setAttribute('stroke-dashoffset', (-lt * 40).toFixed(1));
    ghostTag.setAttribute('opacity', (gk * (1 - prog(lt, tNote - 0.2, tNote))).toFixed(3));
    ghostTag.setAttribute('transform', `translate(410,1250) scale(${Math.max(0.01, spring(lt, L(P.C2) + 0.1, 14, 6)).toFixed(3)}) translate(-410,-1250)`);
    folded.setAttribute('opacity', (1 - prog(lt, tNote - 0.1, tNote + 0.2)).toFixed(3));
    back.style.opacity = (0.75 * prog(lt, tNote - 0.1, tNote + 0.3)).toFixed(3);
    note.update(lt, tNote, L(P.Cend) - 0.35);
    note.el.style.display = lt > tNote - 0.05 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.2)) * 6);
  };
  SHOTS.push(S);
})();

// reaction: her eyes fill; she looks at the drawer
(() => {
  const [A, B] = SC.s3b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.02) contrast(1.05)';
  const set = studio(S, { mode: 'night', month: 'ธ.ค.' }), G = set.ground;
  const lan = new Puppet(set.people, LAN12, S.L.mid.defs);
  lightCast(S, set, [lan], { light: { rim: '#ffe2b0', rimOp: 0.6 }, shadow: { op: 0.22, k: 0.25 } });
  const tr = tears(set.top, 41);
  const shots = [{ t: 0, cam: fA(560, 900, 2.3, 600, 1120), to: fA(560, 900, 2.45, 600, 1120) }];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5 }));
    set.update(lt);
    const p = standP(lan, 580, G, 1.2, -1, { t: lt, smile: 0.2, head: lt > 0.3 ? 6 : 16, eyes: 1, aF: [80, 20], aB: [84, 40] });
    lan.pose(p);
    const [ex, ey] = torsoW(lan, p, HEAD_C[0] + 30, HEAD_C[1] + 6);
    tr(ex, ey, 0.6, lt);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 9 ผ้าพันคอ / ที่ไม่เคยได้ใช้ — over the blurred drawer of scarves
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = lannaPorch(S, { mode: 'dawn' });
  S.L.far.el.style.filter = 'blur(14px) brightness(0.55) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.55) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 801, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '330px';
  ic.innerHTML = `<span class="tsc12">${SCARF.map((c, i) => `<i style="--i:${i}">${scarfIcon(190, c, { id: 't' })}</i>`).join('')}</span>`;
  const icons = [...ic.querySelectorAll('i')];
  const t1 = html('div', 'title', wrap); t1.style.top = '640px'; t1.style.font = '700 210px/1 Kanit';
  const digits = ['9'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ผ้าพันคอ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่ไม่เคยได้ใช้'); t2.style.top = '890px'; t2.style.font = '600 108px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1040px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt + 9); bok(lt);
    icons.forEach((e, i) => { const k = spring(lt, 0.05 + i * 0.05, 16, 6.5); e.style.opacity = fadeIn(lt, 0.05 + i * 0.05, 0.08); e.style.transform = `translateY(${((1 - k) * -120).toFixed(1)}px) rotate(${(Math.sin(lt * 2 + i) * 6).toFixed(1)}deg)`; });
    digits.forEach((d, i) => { const t0 = 0.3, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.45, 14, 7); unit.style.opacity = fadeIn(lt, 0.45, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.65, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.65, 1.15))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.95, 1.35)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — "เราขึ้นเหนือไปหายาย พันผ้าพันคอของยายไปทั้งหมด ยายขำจนน้ำตาไหล แล้วสอนเราถักต่อจนเสร็จ" — then the tenth scarf
// goes round ยาย's neck: "ของบางอย่าง ไม่ได้ส่งมาให้เราใช้ แต่ส่งมาบอกว่า มีคนคิดถึงเราอยู่ทุกปี"
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.04)';
  const set = lannaPorch(S, { mode: 'morning', stoveX: 640, catX: 770, basketDX: -150 }), L = t => t - A, G = set.ground;
  const yai = new Puppet(set.people, YAI12, S.L.mid.defs);
  const lan = new Puppet(set.people, LAN12_N, S.L.mid.defs);
  const stack = scarfWear(lan, S.L.mid.defs, [SCARF[8], SCARF[6], SCARF[5], SCARF[4], SCARF[3], SCARF[2], SCARF[1], SCARF[7], SCARF[0]], { tail: 70, step: 5 });
  const yaiScarf = scarfWear(yai, S.L.mid.defs, [SCARF10], { tail: 60, step: 7 });
  lightCast(S, set, [yai, lan], { light: { rim: '#fff1c4', rimOp: 0.75 }, shadow: { op: 0.18, k: 0.22, blur: 9 } });
  const knit = knitPiece(set.top, S.L.mid.defs, SCARF10);
  const ball = yarnBall(set.top, S.L.mid.defs, 400, 1288, 18, SCARF10);
  const puffY = breath(set.top, 51), puffL = breath(set.top, 52);
  const trN = tears(set.top, 53, { spread: 0.3, drift: 1, n: 3 }), trF = tears(set.top, 54, { spread: 0.3, drift: -1, n: 2 });
  const temp = tempChip12(S.ui, 40, 120, false);
  const prg = progress12(S.ui, 60, 130);
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const hearts = heartsRise(back, 540, 700, L(P.E3) + 0.2, 7, 55, 0.35);
  const wrapScarf = scarfDrape(lan.prop, S.L.mid.defs, SCARF10, 110);
  const tArrive = L(P.D1) - 0.1, tLaugh = L(P.D2) - 0.1, tKnit = L(P.D3) - 0.1, tWrap = L(P.Dend) + 0.1, tSide = L(P.E0) - 0.05, tCrane = L(P.E3) - 0.1;
  const XW = lt => lerp(1000, 860, prog(lt, 0, tArrive));   // walking in along the garden path
  const shots = [
    { t: 0, cam: fA(600, 1180, 1.14, 540, 1060), to: fA(600, 1180, 1.18, 540, 1060) },
    { t: tArrive, cam: fA(525, 1060, 1.66, 540, 1010), to: fA(525, 1060, 1.74, 540, 1010) },
    { t: tLaugh, cam: fA(341, 1077, 2.3, 540, 1120), to: fA(341, 1077, 2.42, 540, 1120) },
    { t: tKnit, cam: fA(430, 1150, 1.85, 540, 1120), to: fA(430, 1150, 1.93, 540, 1120) },
    { t: tWrap, cam: fA(425, 1110, 1.84, 540, 1090), to: fA(425, 1110, 1.92, 540, 1090) },
    { t: tSide, cam: fA(270, 1090, 2.05, 540, 1120), to: fA(270, 1090, 2.15, 540, 1120) },
    { t: tCrane, cam: fA(300, 1120, 1.6, 540, 1160) },
    { t: tCrane + 0.5, move: 2.0, cam: fA(560, 760, 1.08, 540, 1180), to: fA(560, 740, 1.06, 540, 1200) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.55, minY: -260 }));
    const lapse = lt > tKnit && lt < tWrap;
    set.update(lapse ? lt + (lt - tKnit) * 4 : lt + (lt > tWrap ? (tWrap - tKnit) * 4 : 0));
    const ph = lt * 6;
    // ยาย
    let pY = sitP(yai, 300, G, 1.2, 1, { t: lt, torso: 10, head: 8, smile: 0.8 });
    let pL;
    let knitOn = false;
    if (lt < tArrive) {
      pY.head = lt > 0.8 ? -6 : 10; pY.smile = 0.9;
      knitHands(yai, pY, lt, 0.4, 0.5);
      pL = walkP(lan, XW(lt), 1590, 1.2, -1, ph, { amp: 16, t: lt + 2, smile: 0.9, head: -4 });
    } else if (lt < tKnit) {
      pY.head = -10; pY.smile = 1; pY.grin = lt > tLaugh ? 1 : 0; pY.torso = lt > tLaugh ? 4 + Math.sin(lt * 9) * 3 : 8;
      if (lt > tLaugh) { const [hx, hy] = torsoW(yai, pY, 50, -70); pY.aF = yai.reach(pY, hx, hy); pY.aB = [60, 10]; }
      const hop = Math.sin(Math.PI * prog(lt, tArrive, tArrive + 0.32));
      pL = standP(lan, 670, G, 1.2, -1, { t: lt + 2, smile: 1, grin: 1, head: -6, aF: [-24, -48], aB: [214, 236] });   // ta-da: arms out wide
      pL.y -= 26 * hop;
      if (lt > tLaugh - 0.15) { const [cx, cy] = torsoW(lan, pL, 40, -64); pL.aF = lan.reach(pL, cx, cy); pL.aB = lan.reach(pL, cx - 26, cy + 10); }   // arms down, hugging the pile, while ยาย laughs
    } else if (lt < tWrap) {
      knitOn = true;
      pY.head = 18; pY.smile = 0.95;
      pL = sitP(lan, 560, G, 1.2, -1, { t: lt + 2, torso: 14, head: 18, smile: 0.9 });
    } else if (lt < tSide) {
      pY.head = 2; pY.smile = 1;
      pL = sitP(lan, 560, G, 1.2, -1, { t: lt + 2, smile: 0.95, head: 10, torso: 12 });   // still beside her, leaning in
    } else {
      pY.head = lt > L(P.E2) ? -2 : 4; pY.smile = 1;
      pL = sitP(lan, 140, G, 1.2, 1, { t: lt + 2, torso: lt > L(P.E2) ? 4 + 18 * ease.inOutSine(prog(lt, L(P.E2), L(P.E2) + 0.5)) : 4, head: lt > L(P.E2) ? 16 : 2, smile: 1, eyes: lt > L(P.E2) + 0.6 ? 0 : null });   // behind ยาย, then her cheek on ยาย's shoulder
    }
    // the knitting: ยาย's hands on hers, the tenth scarf growing in the time-lapse
    let kProg = prog(lt, tKnit + 0.2, tWrap - 0.15);
    if (knitOn) {
      const [lf, lb] = knitHands(lan, pL, lt, 1.4, 1);
      const [gx, gy] = torsoW(lan, pL, 66, -46);
      pY.aF = yai.reach(pY, gx + 6, gy - 4); pY.aB = yai.reach(pY, gx - 20, gy + 6);
    }
    if (lt >= tWrap && lt < tSide) {   // wrapping it round ยาย's neck
      const u = prog(lt, tWrap, tSide - 0.15), [nx, ny] = torsoW(yai, pY, 4, -RIG.T + 10);
      pL.aF = lan.reach(pL, nx + 34 + Math.cos(u * 6.3) * 30, ny + 40 + Math.sin(u * 6.3) * 10); pL.aB = lan.reach(pL, nx + 56, ny + 52);   // round the shoulders, below her face
    }
    yai.pose(pY); lan.pose(pL);
    stack(pL, lt);
    yaiScarf.hidden = lt < tWrap + 0.5; yaiScarf(pY, lt);
    // knit piece
    if (knitOn) { const a = wristFW(lan, pL), b = wristBW(lan, pL); knit.set([Math.min(a[0], b[0]) + 6, Math.min(a[1], b[1])], [Math.max(a[0], b[0]) - 6, Math.max(a[1], b[1])], lerp(70, 150, kProg), lt, [400, 1282]); knit.g.setAttribute('display', 'inline'); }
    else if (lt < tArrive) { const a = wristFW(yai, pY), b = wristBW(yai, pY); knit.set([Math.min(a[0], b[0]) + 6, Math.min(a[1], b[1]) + 4], [Math.max(a[0], b[0]) - 6, Math.max(a[1], b[1]) + 4], 70, lt, [400, 1282]); knit.g.setAttribute('display', 'inline'); }
    else knit.g.setAttribute('display', 'none');
    ball.setAttribute('display', knitOn || lt < tArrive ? 'inline' : 'none');
    wrapScarf(SCARF10, lt, lt >= tWrap && lt < tWrap + 0.55);
    puffY(yai, pY, lt); puffL(lan, pL, lt + 0.4, lt > tArrive ? 1 : 0);
    const kT = lt > tLaugh && lt < tKnit ? 1 : 0;
    trN(...torsoW(yai, pY, HEAD_C[0] + 46, HEAD_C[1] + 12), kT, lt);   // outer corner of the near eye
    trF(...torsoW(yai, pY, HEAD_C[0] - 8, HEAD_C[1] + 12), kT, lt + 0.37);
    const r = rollValue(lt, 0.2, 1.0, 20, 9);
    temp.update(lt, 0.2, r.v, r.speed);
    temp.el.style.display = lt < tArrive + 1.2 ? 'flex' : 'none';
    prg.update(lt, tKnit + 0.1, kProg);
    prg.el.style.display = lt > tKnit && lt < tSide + 0.6 ? 'flex' : 'none';
    leak(lt, 0.15 + 0.35 * prog(lt, tCrane, B - A));
    hearts(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#7a5a7e'], [0.6, '#3e2e52'], [1, '#1c1428']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 851, { color: '#ffd9a0', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 853, ['#ffd66b', '#ffffff', '#ffd9a0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '290px';
  duo.innerHTML = `<span class="duo7">${av12('lan', 190, { scarf: SCARF[2] })}</span><span class="duo7h">${scarfIcon(170, SCARF10)}</span><span class="duo7">${av12('yai', 190, { scarf: SCARF10 })}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '6px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['9'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ผ้าพันคอ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่ไม่เคยได้ใช้'); t2.style.top = '808px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'หน้าหนาวนี้ โทรหาคนที่คิดถึงเราบ้างนะ'); sub.style.top = '975px'; sub.style.font = '500 48px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ยายรอให้กลับบ้าน</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(duo, lt, 0.15, '', -10);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.55, 14, 7); unit.style.opacity = fadeIn(lt, 0.55, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
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
  const dip = tt => prog(t, tt - 0.3, tt) * (1 - prog(t, tt, tt + 0.45));
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, DURATION - 0.45, DURATION) + 0.85 * dip(SC.s3[0])).toFixed(3);
  const fl = tt => prog(t, tt - 0.25, tt) * (1 - prog(t, tt, tt + 0.3));
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1a[0]) * 0.5, fl(SC.s2[0]) * 0.6, fl(SC.s4[0]), fl(SC.s5[0]) * 0.7, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
