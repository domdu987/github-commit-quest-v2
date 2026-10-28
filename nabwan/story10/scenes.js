// "52 ปีกับกระทงสองใบ" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D3; H is the "ถ้า..." hook).
// Shot language as in pro.js: every scene is a shot list on a lit set (wide → medium → close-up / insert).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0: [0, P.A0 - 0.3], s1a: [P.A0 - 0.3, P.A3 - 0.15], s1b: [P.A3 - 0.15, P.A5 - 0.1], s1c: [P.A5 - 0.1, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3],
  s3: [P.C0 - 0.3, P.title], s4: [P.title, P.D0 - 0.1], s5: [P.D0 - 0.1, P.end], s6: [P.end, DURATION] };
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));

function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
const HW = (x, y, s, f = 1) => [x + f * s * HEAD_C[0], y + s * HEAD_C[1]];
function lightCast(S, set, pups, o = {}) {
  const Lt = set.light || {};
  set.people.setAttribute('filter', charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {})));
  return pups.map(p => castShadow(p, set.shadowL, S.L.mid.defs, Object.assign({ lx: Lt.lx }, o.shadow || {})));
}
const SIT = { lF: [8, 172], lB: [18, 166] };
const VT = { x: 330, y: 1452, s: 1.2 }, VY = { x: 560, y: 1452, s: 1.2 };   // veranda: ตา, ยาย's cushion
const PT = { x: 420, y: 1290, s: 1.2 };                                     // pier: ตา at the end of the deck
const H_VT = HW(VT.x, VT.y, VT.s), H_PT = HW(PT.x, PT.y, PT.s);
// folding a banana leaf in his lap
function foldHands(pup, pose, lt, speed = 1) {
  const [cx, cy] = toWorld(pose, ...torsoPt(pose, 84, -RIG.T + 76));
  const a = lt * 6 * speed;
  pose.aF = pup.reach(pose, cx + 16 + Math.sin(a) * 14, cy - 8 + Math.cos(a * 1.3) * 9);
  pose.aB = pup.reach(pose, cx - 10 + Math.sin(a + 2) * 10, cy + 4 + Math.cos(a) * 6);
  pose.propRot = Math.sin(a) * 22;
}
function leafProp(parent) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M-6,-6 L34,-34 L48,8 Z', fill: '#4f9a4a', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M4,-8 L36,-26', stroke: '#7fc07a', 'stroke-width': 2.5 }, g);
  return g;
}
function lighterProp(parent) {
  const g = svg('g', {}, parent);
  svg('rect', { x: -8, y: -30, width: 18, height: 34, rx: 4, fill: '#e0453b', stroke: INK, 'stroke-width': 3 }, g);
  svg('rect', { x: -6, y: -38, width: 14, height: 9, rx: 2, fill: '#c9d2dc', stroke: INK, 'stroke-width': 2.5 }, g);
  const fl = svg('g', {}, g);
  svg('circle', { cx: 1, cy: -52, r: 26, fill: 'url(#ktglow)' }, fl);
  svg('path', { d: 'M1,-64 C8,-54 8,-48 1,-42 C-6,-48 -6,-54 1,-64 Z', fill: '#ffb03a', stroke: INK, 'stroke-width': 2 }, fl);
  return { g, fl };
}
// a krathong whose position is animated in world space (on the deck, in his hands, then drifting on the water)
function liveKT(parent, defs, o) {
  const refl = ktReflection(parent, defs);
  const k = krathong(parent, 0, 0, 1, o);
  return {
    k, at(x, y, s, t, lit, onWater) {
      k.g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${s.toFixed(3)})`);
      k.flame.setAttribute('opacity', lit ? 1 : 0); k.glow.setAttribute('opacity', lit ? 1 : 0);
      if (lit) flickerK(k, t, x);
      if (onWater && lit) refl(x, y, s, t); else refl(-999, -999, 0.01, t);
    },
  };
}
// path of a krathong set down at the pier's end and drifting out toward the moon
function driftPos(t, t0) {
  const u = Math.max(0, t - t0);
  return [692 + 30 * u + 6 * Math.sin(u * 0.9), 1346 - 15 * u + 2 * Math.sin(u * 1.7), Math.max(0.3, 0.62 - 0.022 * u)];
}

// =====================================================================
// S0 — hook: two krathongs drift side by side; one candle goes out; "คุณจะขอพรว่าอะไร"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.1) contrast(1.05)';
  const set = riverPier(S), L = t => t - A;
  const ka = liveKT(set.water, S.L.mid.defs, { c: '#f07aa8' }), kb = liveKT(set.water, S.L.mid.defs, { c: '#b49ad8' });
  const q = wishQ(S.ui, 560, 720);
  const smoke = svg('g', { opacity: 0 }, set.water);
  for (let i = 0; i < 4; i++) svg('circle', { r: 8 + i * 4, fill: '#d6d0e0', opacity: 0.4 - i * 0.08 }, smoke);
  const shots = [
    { t: 0, cam: frameAt(660, 1140, 1.12, 540, 1060), to: frameAt(660, 1160, 1.22, 540, 1060) },
    { t: L(P.H2) - 0.05, cam: frameAt(735, 1205, 2.0, 540, 1200), to: frameAt(730, 1205, 2.12, 540, 1200) },
    { t: L(P.H4) - 0.05, cam: frameAt(700, 1180, 3.1, 540, 1250), to: frameAt(700, 1180, 3.35, 540, 1250) },
  ];
  S.update = lt => {
    const cam = applyCam(S, shotCam(lt, shots, B - A, { handheld: 0.7 }));
    set.update(lt);
    const dx = lt * 6;
    ka.at(690 + dx, 1250 + Math.sin(lt * 1.3) * 3, 0.85, lt, true, true);
    const out = prog(lt, L(P.H3) - 0.1, L(P.H3) + 0.5);   // her candle goes out and her krathong slips away into the dark
    kb.at(800 + dx + out * 60, 1236 + Math.sin(lt * 1.2 + 1) * 3 - out * 30, 0.82 - out * 0.2, lt, lt < L(P.H3) - 0.05, true);
    kb.k.g.setAttribute('opacity', (1 - prog(lt, L(P.H3) + 0.2, L(P.H4))).toFixed(3));
    const sk = prog(lt, L(P.H3) - 0.05, L(P.H3) + 1.2);
    smoke.setAttribute('opacity', sk > 0 && sk < 1 ? (1 - sk).toFixed(2) : 0);
    [...smoke.children].forEach((c, i) => setA(c, { cx: (800 + dx + 18 * 0.82 + Math.sin(lt * 3 + i) * 6 * sk).toFixed(1), cy: (1236 - 96 * 0.82 - sk * (40 + i * 26)).toFixed(1) }));
    q.update(lt, L(P.H4) + 0.15);
    setGrade(S, (1 - prog(lt, 0, 0.5)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1a — memory on the same pier, years ago (sepia): the young couple set two krathongs down; they age into ตาสม and ยายบัว
// =====================================================================
(() => {
  const [A, B] = SC.s1a;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  const set = riverPier(S, { moonX: 860 }), L = t => t - A;
  const old = svg('g', {}, set.people), young = svg('g', {}, set.people);
  const ty = new Puppet(young, TA_YOUNG, S.L.mid.defs), yy = new Puppet(young, YAI_YOUNG, S.L.mid.defs);
  const to = new Puppet(old, TA, S.L.mid.defs), yo = new Puppet(old, YAI, S.L.mid.defs);
  lightCast(S, set, [], { light: { rim: '#fff1c4', rimOp: 0.65 } });
  const k1 = liveKT(set.water, S.L.mid.defs, { c: '#f07aa8' }), k2 = liveKT(set.water, S.L.mid.defs, { c: '#b49ad8' });
  const yr = yearChip10(S.ui, 40, 120, 'ลอยด้วยกัน พ.ศ.');
  const y52 = chip7(S.ui, 40, 230, 'ด้วยกันมา <b>52 ปี</b>', 'today7');
  y52.slot.innerHTML = `<span class="ic5">${ktIcon(56, { pair: true })}</span>`;
  const leak = lightLeak(S.fx);
  const shots = [{ t: 0, cam: frameAt(480, 1160, 1.3, 540, 1150), to: frameAt(500, 1150, 1.4, 540, 1150) }];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A, { handheld: 0.5 }));
    set.update(lt + 3);
    const age = ease.inOutSine(prog(lt, L(P.A2) - 0.35, L(P.A2) + 0.35));
    young.setAttribute('opacity', (1 - age).toFixed(3)); old.setAttribute('opacity', age.toFixed(3));
    for (const [pup, x, f, who] of [[ty, 360, 1, 't'], [yy, 500, 1, 'y'], [to, 360, 1, 't'], [yo, 500, 1, 'y']]) {
      const p = { x, y: 1290, s: 1.2, f, torso: 8, head: who === 'y' ? -6 + Math.sin(lt * 1.2) * 2 : 8, lF: SIT.lF, lB: SIT.lB, t: lt + (who === 'y' ? 2 : 0), smile: 0.85, aF: [60, 40], aB: [70, 50] };
      if (who === 't') { const [hx, hy] = toWorld(p, ...torsoPt(p, 60, -RIG.T + 50)); p.aF = pup.reach(p, hx + 30, hy + 20); }
      pup.pose(p);
    }
    for (const [kk, t0, x0] of [[k1, -1.2, 0], [k2, -0.6, 70]]) { const [x, y, s] = driftPos(lt, t0); kk.at(x + x0, y + (x0 ? 10 : 0), s, lt, true, true); }
    const r = rollValue(lt, L(P.A1) - 0.2, L(P.A2) + 0.2, 2516, 2568);
    yr.update(lt, 0.15, r.v, r.speed);
    popSquash(y52.el, lt, L(P.A2) + 0.1);
    // the past is sepia and flickers; colour comes back as they age into the present
    const sep = 1 - age;
    S.grade = `sepia(${(0.75 * sep).toFixed(3)}) saturate(${(1 - 0.25 * sep + 0.1 * age).toFixed(3)}) contrast(${(1.05 + 0.04 * sep).toFixed(3)}) brightness(${(1 + 0.04 * sep * Math.sin(lt * 23) * Math.sin(lt * 7)).toFixed(3)})`;
    leak(lt, 0.25 + 0.3 * sep);
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1b — every year on the veranda, ตา folds two krathongs from banana leaves while ยาย watches
// =====================================================================
(() => {
  const [A, B] = SC.s1b;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.06) contrast(1.04) sepia(0.12)';
  const set = veranda(S, { yai: true }), L = t => t - A;
  const ta = new Puppet(set.people, TA, S.L.mid.defs), yai = new Puppet(set.people, YAI, S.L.mid.defs);
  const leaf = leafProp(ta.prop);
  lightCast(S, set, [ta, yai], { light: { rim: '#ffe2a8' }, shadow: { k: 0.32 } });
  const kts = [krathong(set.made, 430, 1468, 0.62, { c: '#f07aa8' }), krathong(set.made, 520, 1468, 0.62, { c: '#b49ad8' })];
  const shots = [
    { t: 0, cam: frameAt(445, 1300, 1.62, 540, 1240), to: frameAt(450, 1300, 1.72, 540, 1240) },
    { t: L(P.A4) - 0.15, cam: frameAt(475, 1430, 3.4, 540, 1060), to: frameAt(475, 1430, 3.6, 540, 1060) },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt);
    const tp = { x: VT.x, y: VT.y, s: VT.s, f: 1, torso: 12, head: 20 + Math.sin(lt * 1.1) * 2, lF: SIT.lF, lB: SIT.lB, t: lt, smile: 0.6 };
    foldHands(ta, tp, lt, 1); ta.pose(tp);
    yai.pose({ x: VY.x, y: VY.y, s: VY.s, f: -1, torso: 4, head: 8 + Math.sin(lt * 1.3) * 2, lF: SIT.lF, lB: SIT.lB, t: lt + 2, smile: 0.9, aF: [70, 30], aB: [74, 34] });
    kts.forEach((k, i) => { const t0 = L(P.A4) + i * 0.18; const kk = spring(lt, t0, 14, 6); k.g.setAttribute('transform', `translate(${430 + i * 90},1468) scale(${(0.62 * Math.max(0.001, kk)).toFixed(3)})`); k.g.setAttribute('opacity', lt > t0 ? 1 : 0); k.flame.setAttribute('opacity', 0); k.glow.setAttribute('opacity', 0); });
    leaf.setAttribute('opacity', lt < L(P.A4) ? 1 : 0);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1c — insert: the two krathongs on the mat, tagged ของตา and ของยาย
// =====================================================================
(() => {
  const [A, B] = SC.s1c;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  S.grade = 'saturate(1.06) contrast(1.04) sepia(0.12)';
  const set = veranda(S, { yai: true }), L = t => t - A;
  const ta = new Puppet(set.people, TA, S.L.mid.defs), yai = new Puppet(set.people, YAI, S.L.mid.defs);
  lightCast(S, set, [ta, yai], { light: { rim: '#ffe2a8' }, shadow: { k: 0.32 } });
  const kT = krathong(set.made, 430, 1468, 0.62, { c: '#f07aa8', tag: 'ของตา' }), kY = krathong(set.made, 520, 1468, 0.62, { c: '#b49ad8', tag: 'ของยาย' });
  const hl = [kT, kY].map(k => { const h = svg('ellipse', { cx: 0, cy: -50, rx: 90, ry: 90, fill: 'url(#ktglow)', opacity: 0 }, k.g); k.g.insertBefore(h, k.g.firstChild); return h; });
  const shots = [{ t: 0, cam: frameAt(475, 1430, 3.5, 540, 1040), to: frameAt(480, 1430, 3.7, 540, 1040) }];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt + 3);
    const tp = { x: VT.x, y: VT.y, s: VT.s, f: 1, torso: 14, head: 22, lF: SIT.lF, lB: SIT.lB, t: lt, smile: 0.7 };
    const [hx, hy] = [lerp(430, 520, ease.inOutSine(prog(lt, L(P.A6) - 0.2, L(P.A6) + 0.4))) - 40, 1430];   // his hand rests by his, then slides hers toward ยาย
    tp.aF = ta.reach(tp, hx, hy); tp.aB = [74, 40];
    ta.pose(tp);
    yai.pose({ x: VY.x, y: VY.y, s: VY.s, f: -1, torso: 6, head: 14, lF: SIT.lF, lB: SIT.lB, t: lt + 2, smile: 1, aF: [70, 30], aB: [74, 34] });
    const push = 18 * ease.inOutSine(prog(lt, L(P.A6) - 0.2, L(P.A6) + 0.4));
    kY.g.setAttribute('transform', `translate(${(520 + push).toFixed(1)},1468) scale(0.62)`);
    [kT, kY].forEach(k => { k.flame.setAttribute('opacity', 0); k.glow.setAttribute('opacity', 0); });
    hl[0].setAttribute('opacity', (0.9 * fadeIn(lt, L(P.A5) + 0.05, 0.2) * (1 - 0.6 * prog(lt, L(P.A6), L(P.A6) + 0.3))).toFixed(3));
    hl[1].setAttribute('opacity', (0.9 * fadeIn(lt, L(P.A6) + 0.05, 0.2)).toFixed(3));
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — this year: ยาย's cushion is empty; หลาน says one is enough; ตา folds until late and makes two, as always
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(0.96) contrast(1.05)';
  const set = veranda(S, { yai: false }), L = t => t - A;
  const ta = new Puppet(set.people, TA, S.L.mid.defs), lan = new Puppet(set.people, LAN, S.L.mid.defs);
  const leaf = leafProp(ta.prop);
  lightCast(S, set, [ta, lan], { light: { rim: '#ffe2a8' }, shadow: { k: 0.32 } });
  const bub = bubble10(S.ui, 200, 660, 'ทำใบเดียวก็พอนะตา');
  const clk = timeChip10(S.ui, 40, 120);
  const kts = [krathong(set.made, 430, 1468, 0.62, { c: '#f07aa8', tag: 'ของตา' }), krathong(set.made, 520, 1468, 0.62, { c: '#b49ad8', tag: 'ของยาย' })];
  const tB1 = L(P.B1) - 0.1, tB2 = L(P.B2) - 0.1, tB3 = L(P.B3) - 0.15;
  const shots = [
    { t: 0, cam: frameAt(565, 1410, 3.0, 540, 1300), to: frameAt(500, 1400, 2.8, 540, 1300) },
    { t: tB1, cam: frameAt(380, 1200, 1.12, 540, 1120), to: frameAt(380, 1195, 1.18, 540, 1120) },
    { t: tB2, cam: frameAt(H_VT[0] + 70, H_VT[1] + 150, 1.75, 420, 1200), to: frameAt(H_VT[0] + 70, H_VT[1] + 150, 1.8, 420, 1200) },
    { t: tB2 + 1.2, cam: frameAt(430, 1420, 2.5, 540, 1180), to: frameAt(440, 1420, 2.6, 540, 1180) },
    { t: tB2 + 2.3, cam: frameAt(H_VT[0] + 40, H_VT[1] + 60, 2.2, 440, 1240), to: frameAt(H_VT[0] + 40, H_VT[1] + 60, 2.3, 440, 1240) },
    { t: tB3, cam: frameAt(500, 1430, 2.4, 540, 1220), to: frameAt(500, 1430, 2.6, 540, 1220) },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A));
    const lapse = lt > tB2 && lt < tB3;
    set.update(lapse ? lt * 3 : lt);
    const lookUp = lt > L(P.B1) + 0.6 && lt < tB2 - 0.4;
    const tp = { x: VT.x, y: VT.y, s: VT.s, f: 1, torso: lookUp ? 2 : 12, head: lookUp ? -18 : 20 + Math.sin(lt * 1.1) * 2, lF: SIT.lF, lB: SIT.lB, t: lt, smile: lookUp ? 0.85 : 0.5, eyes: lt > tB2 + 2.3 && lt < tB3 && Math.sin(lt * 1.7) > 0.3 ? 0 : null };
    if (lt > tB3) { tp.aF = ta.reach(tp, 500, 1440); tp.aB = [74, 40]; tp.head = 24; tp.smile = 0.8; }
    else foldHands(ta, tp, lt, lapse ? 2.6 : 1);
    ta.pose(tp);
    leaf.setAttribute('opacity', lt > tB3 ? 0 : 1);
    // หลาน leans in the doorway
    const lanOn = lt > tB1 - 0.05 && lt < tB2;
    lan.pose({ x: 150, y: 1420 - LEG * 1.2 * LAN.s, s: 1.2, f: 1, torso: 6, head: 6, lF: [92, 90], lB: [86, 90], t: lt + 5, smile: 0.6, aF: [84, 96], aB: [94, 88] });
    lan.g.setAttribute('opacity', lanOn ? 1 : 0);
    bub.update(lt, L(P.B1) + 0.7, tB2 - 0.1);
    clk.update(lt, tB2 + 0.1, tB3 - 0.2);
    clk.el.style.opacity = lt > tB2 && lt < tB3 + 0.4 ? clk.el.style.opacity : 0;
    kts.forEach((k, i) => { const t0 = tB3 + 0.1 + i * 0.25; k.g.setAttribute('opacity', lt > t0 ? 1 : 0); const kk = spring(lt, t0, 14, 6); k.g.setAttribute('transform', `translate(${430 + i * 90},1468) scale(${(0.62 * Math.max(0.001, kk)).toFixed(3)})`); k.flame.setAttribute('opacity', 0); k.glow.setAttribute('opacity', 0); });
    set.photoGlow.setAttribute('opacity', (0.7 + 0.3 * prog(lt, tB3, tB3 + 1)).toFixed(3));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — at the river: he lights both candles, sets ยาย's krathong on the water first — "ยายกลัวมืด ต้องให้ไปก่อน ตาจะลอยตามไป"
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.08) contrast(1.05)';
  const set = riverPier(S), L = t => t - A;
  const ta = new Puppet(set.people, TA, S.L.mid.defs);
  const li = lighterProp(ta.prop);
  lightCast(S, set, [ta], { light: { rim: '#fff1c4', rimOp: 0.7 } });
  const kY = liveKT(set.water, S.L.mid.defs, { c: '#b49ad8', tag: 'ของยาย' }), kT = liveKT(set.water, S.L.mid.defs, { c: '#f07aa8', tag: 'ของตา' });
  const deck = svg('g', {}, set.top);   // while on the deck the krathongs sit in front of him
  const tLight1 = L(P.C1) + 0.45, tLight2 = L(P.C1) + 1.25;
  const tLiftY = L(P.C2) + 0.1, tDownY = L(P.C2) + 1.3, tLiftT = L(P.C5) + 0.05, tDownT = L(P.C5) + 1.2;
  const shots = [
    { t: 0, cam: frameAt(560, 1150, 1.3, 540, 1100), to: frameAt(540, 1160, 1.38, 540, 1100) },
    { t: L(P.C1) - 0.1, cam: frameAt(548, 1220, 2.9, 540, 1150), to: frameAt(552, 1220, 3.05, 540, 1150) },
    { t: L(P.C2) - 0.1, cam: frameAt(570, 1200, 1.55, 540, 1130), to: frameAt(620, 1200, 1.62, 540, 1130) },
    { t: L(P.C3) - 0.1, cam: frameAt(H_PT[0] + 40, H_PT[1] + 40, 2.35, 430, 1150), to: frameAt(H_PT[0] + 40, H_PT[1] + 40, 2.5, 430, 1150) },
    { t: L(P.C5) - 0.1, cam: frameAt(600, 1200, 1.6, 540, 1150), to: frameAt(595, 1120, 1.15, 540, 1060) },
  ];
  const lift = (t, tl, td, x0) => {   // deck → hands → water
    if (t < tl) return [x0, 1284, 0.6, false];
    if (t < td) { const u = ease.inOutSine(prog(t, tl, td)); return [lerp(x0, 692, u), lerp(1284, 1346, u) - Math.sin(Math.PI * u) * 60, lerp(0.6, 0.62, u), false]; }
    const [x, y, s] = driftPos(t, td); return [x, y, s, true];
  };
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A));
    set.update(lt + 5);
    const pY = lift(lt, tLiftY, tDownY, 575), pT = lift(lt, tLiftT, tDownT, 520);
    kY.at(pY[0], pY[1], pY[2], lt, lt > tLight1, pY[3]); kT.at(pT[0], pT[1], pT[2], lt, lt > tLight2, pT[3]);
    // on the deck they draw over his legs; once lifted they go back to the water layer
    (lt < tDownY - 0.3 ? deck : set.water).appendChild(kY.k.g); (lt < tDownT - 0.3 ? deck : set.water).appendChild(kT.k.g);
    const tp = { x: PT.x, y: PT.y, s: PT.s, f: 1, torso: 16, head: 18, lF: SIT.lF, lB: SIT.lB, t: lt, smile: 0.55 };
    const lighting = lt > L(P.C1) - 0.2 && lt < tLight2 + 0.4;
    li.g.setAttribute('opacity', lighting ? 1 : 0); li.fl.setAttribute('opacity', lighting && lt > L(P.C1) + 0.15 ? 1 : 0);
    if (lighting) { const tx = lt < tLight1 + 0.2 ? 575 : 520; const [wx, wy] = [tx + 12, 1284 - 0.6 * 120]; tp.aF = ta.reach(tp, wx - 4, wy + 74); tp.aB = [70, 40]; tp.propRot = -10; }
    else if (lt > tLiftY - 0.2 && lt < tDownY + 0.3) { tp.aF = ta.reach(tp, pY[0] - 20, pY[1] - 26); tp.aB = ta.reach(tp, pY[0] - 44, pY[1] - 14); tp.torso = 22; }
    else if (lt > tLiftT - 0.2 && lt < tDownT + 0.3) { tp.aF = ta.reach(tp, pT[0] - 20, pT[1] - 26); tp.aB = ta.reach(tp, pT[0] - 44, pT[1] - 14); tp.torso = 22; }
    else { tp.aF = [62, 70]; tp.aB = [74, 60]; }
    if (lt > L(P.C3) - 0.1 && lt < L(P.C5) - 0.1) { tp.head = -8 + Math.sin(lt * 1.1) * 2; tp.torso = 4; tp.smile = 0.7; tp.eyes = Math.sin(lt * 1.3) > 0.85 ? 0 : null; }   // looking out after her
    ta.pose(tp);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 52 ปี / กับกระทงสองใบ
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = riverPier(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 1031, { color: '#ffd27a', rMin: 14, rMax: 40, speed: 12, op: 0.24, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '420px'; ic.innerHTML = ktIcon(360, { pair: true });
  const t1 = html('div', 'title', wrap); t1.style.top = '700px'; t1.style.font = '700 200px/1 Kanit';
  const digits = ['5', '2'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ปี'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'กับกระทงสองใบ'); t2.style.top = '930px'; t2.style.font = '600 108px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt + 9); bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 3).toFixed(1)}deg)`, -12);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.4, 14, 7); unit.style.opacity = fadeIn(lt, 0.4, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — the two lights drift out together into the moon's path; the camera cranes up to the moon
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 14]]);
  S.grade = 'saturate(1.1) contrast(1.05)';
  const set = riverPier(S), L = t => t - A;
  const ta = new Puppet(set.people, TA, S.L.mid.defs);
  lightCast(S, set, [ta], { light: { rim: '#fff1c4', rimOp: 0.7 } });
  const kY = liveKT(set.water, S.L.mid.defs, { c: '#b49ad8' }), kT = liveKT(set.water, S.L.mid.defs, { c: '#f07aa8' });
  const star = svg('path', { fill: 'none', stroke: '#fff6dc', 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0 }, S.L.far.s);
  const shots = [
    { t: 0, cam: frameAt(790, 1220, 2.0, 540, 1250), to: frameAt(795, 1180, 1.9, 540, 1200) },
    { t: L(P.D2) - 0.1, move: 3.2, cam: { x: 22, y: 6, z: 1.08, fx: 540, fy: 960 }, to: { x: 22, y: 6, z: 1.1, fx: 540, fy: 960 } },
  ];
  S.update = lt => {
    applyCam(S, shotCam(lt, shots, B - A, { handheld: 0.5 }));
    set.update(lt + 14);
    // hers a little ahead; his catches up and they float side by side into the moon's path
    const xy = 800 + 12 * lt, yy = 1230 - 10 * lt, sy = 0.5 - 0.012 * lt;
    const join = ease.inOutSine(prog(lt, L(P.D2), L(P.D3) + 0.5));
    kY.at(xy, yy, sy, lt, true, true); kT.at(lerp(700 + 16 * lt, xy - 70 * sy / 0.5, join), lerp(1270 - 11 * lt, yy + 8, join), lerp(0.54 - 0.012 * lt, sy, join), lt, true, true);
    ta.pose({ x: 380, y: PT.y, s: PT.s, f: 1, torso: 4, head: -10, lF: SIT.lF, lB: SIT.lB, t: lt, smile: 0.7, aF: [62, 70], aB: [74, 60] });
    const sk = prog(lt, L(P.D3) + 0.2, L(P.D3) + 1.0);   // a shooting star over the moon
    star.setAttribute('d', `M${(980 - 260 * sk).toFixed(1)},${(120 + 90 * sk).toFixed(1)} l${(70).toFixed(0)},${(-24).toFixed(0)}`);
    star.setAttribute('opacity', sk > 0 && sk < 1 ? Math.sin(Math.PI * sk).toFixed(2) : 0);
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
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#4a3a6e'], [0.6, '#241c40'], [1, '#0f0c1f']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 1061, { color: '#ffd27a', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 1063, ['#ffd66b', '#ffffff', '#ffd27a'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '300px';
  duo.innerHTML = `<span class="duo7">${taAv(190)}</span><span class="duo7h">${ktIcon(170, { pair: true })}</span><span class="duo7">${yaiAv(190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '6px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['5', '2'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ปี'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'กับกระทงสองใบ'); t2.style.top = '808px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'ลอยกระทงปีนี้ ลอยให้คนที่ยังอยู่ในใจ'); sub.style.top = '975px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่อยากลอยกระทงด้วยทุกปี</span>`;
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
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, DURATION - 0.45, DURATION) + 0.85 * (prog(t, SC.s2[0] - 0.3, SC.s2[0]) * (1 - prog(t, SC.s2[0], SC.s2[0] + 0.45)))).toFixed(3);
  const fl = tt => prog(t, tt - 0.25, tt) * (1 - prog(t, tt, tt + 0.3));
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1a[0]) * 0.9, fl(SC.s1b[0]) * 0.5, fl(SC.s3[0]) * 0.5, fl(SC.s4[0]), fl(SC.s5[0]) * 0.6, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
