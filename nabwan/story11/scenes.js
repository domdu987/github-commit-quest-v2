// "12 ฤดูฝน ที่ไหล่ของพ่อเปียก" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D5; H is the
// "ถ้า..." hook). Shot language as in pro.js: every scene is a shot list on a lit, rain-soaked set (wide → medium →
// close-up / insert); walking scenes track with the pair. The memory is warm and, in the montage, sepia; the present is dusk.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0: [0, P.A0 - 0.3], s1a: [P.A0 - 0.3, P.A2 - 0.3], s1b: [P.A2 - 0.3, P.A4 - 0.3], s1c: [P.A4 - 0.3, P.A5 - 0.3], s1d: [P.A5 - 0.3, P.B0 - 0.3],
  s2: [P.B0 - 0.3, P.B4 - 0.1], s2i: [P.B4 - 0.1, P.C0 - 0.3], s3a: [P.C0 - 0.3, P.C2 - 0.3], s3b: [P.C2 - 0.3, P.Cend - 0.15], s3f: [P.Cend - 0.15, P.title],
  s4: [P.title, P.D0 - 0.1], s5a: [P.D0 - 0.1, P.D3 - 0.3], s5b: [P.D3 - 0.3, P.end], s6: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
const SEPIA = (lt, k = 1) => `sepia(${(0.78 * k).toFixed(3)}) saturate(${(1 - 0.2 * k).toFixed(3)}) contrast(1.08) brightness(${(1 + 0.04 * k * Math.sin(lt * 23) * Math.sin(lt * 7)).toFixed(3)})`;
function lightCast(S, set, pups, o = {}) {
  const Lt = set.light || {};
  set.people.setAttribute('filter', charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {})));
  return pups.map(p => castShadow(p, set.shadowL, S.L.mid.defs, Object.assign({ lx: Lt.lx }, o.shadow || {})));
}
const SIT = { lF: [8, 172], lB: [18, 166] };
const MEM_KID = 0.25;   // the kid in the memory scenes is about ป.3

// ---------------- poses ----------------
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
// raise the front hand to a grip point in the torso frame (umbrella over the head); tilt: degrees toward the facing side
function holdUp(pup, p, tilt = 0, gx = 84, gy = -112) {
  const [wx, wy] = torsoW(pup, p, gx, gy);
  p.aF = pup.reach(p, wx, wy);
  p.propRot = tilt;
  return p;
}
// hold a closed umbrella down like a walking stick (tip on the ground)
function holdCane(pup, p, gx = 52, gy = 30, rot = 178) {
  const [wx, wy] = torsoW(pup, p, gx, gy);
  p.aF = pup.reach(p, wx, wy);
  p.propRot = rot;
  return p;
}

// ---------------- camera that can track a moving subject ----------------
// shots: [{ t, cam: lt => cam, to?: lt => cam, move? }]
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

// ---------------- the pair under one umbrella ----------------
// holder (behind, left, nearer the camera) keeps the other (ahead, right) dry. Builds both puppets with reflections on
// the wet road, the umbrella (and its reflection), the soaked patch on the holder's back, the dry "rain shadow" under the
// canopy, water running off the back of the rim onto the holder's shoulder, and splashes where the rain hits him.
function rimDrips(parent, seed) {
  const r = rng(seed);
  const ds = Array.from({ length: 7 }, (_, i) => ({ per: 0.32 + r() * 0.3, ph: r(), u: i % 3, el: svg('path', { fill: '#f6f2ea', opacity: 0.85 }, parent) }));
  return (t, pts, ground, on = 1) => ds.forEach(d => {
    const p0 = pts && pts[d.u];
    if (!p0 || on < 0.5) { d.el.setAttribute('opacity', 0); return; }
    const k = ((t + d.ph) / d.per) % 1, y = p0[1] + (ground - p0[1]) * k * k, x = p0[0], s = 4;
    d.el.setAttribute('d', `M${x.toFixed(1)},${(y - s * 2.8).toFixed(1)} C${(x + s).toFixed(1)},${(y - s).toFixed(1)} ${(x + s).toFixed(1)},${(y + s).toFixed(1)} ${x.toFixed(1)},${(y + s).toFixed(1)} C${(x - s).toFixed(1)},${(y + s).toFixed(1)} ${(x - s).toFixed(1)},${(y - s).toFixed(1)} ${x.toFixed(1)},${(y - s * 2.8).toFixed(1)} Z`);
    d.el.setAttribute('opacity', 0.85);
  });
}
function pointSplash(parent, seed) {
  const r = rng(seed);
  const ss = Array.from({ length: 6 }, () => ({ per: 0.22 + r() * 0.2, ph: r(), dx: (r() - 0.5) * 50, dy: (r() - 0.5) * 30, el: svg('path', { fill: 'none', stroke: '#f6f2ea', 'stroke-width': 3, 'stroke-linecap': 'round' }, parent) }));
  return (t, x, y, on) => ss.forEach(s => {
    const k = ((t + s.ph) / s.per) % 1, h = 18 * Math.sin(Math.PI * k), px = x + s.dx, py = y + s.dy;
    s.el.setAttribute('d', `M${(px - 4).toFixed(1)},${py.toFixed(1)} q-5,${(-h).toFixed(1)} -12,${(-h * 0.5).toFixed(1)} M${(px + 4).toFixed(1)},${py.toFixed(1)} q5,${(-h).toFixed(1)} 12,${(-h * 0.5).toFixed(1)}`);
    s.el.setAttribute('opacity', on ? ((1 - k) * 0.9).toFixed(2) : 0);
  });
}
function umbPair(S, set, holderO, otherO, o = {}) {
  const defs = S.L.mid.defs;
  const other = otherO ? new Puppet(set.people, otherO, defs) : null;
  const holder = new Puppet(set.people, holderO, defs);
  const wet = wetPatch(holder, defs, { color: o.wetC || (holderO === SON ? '#a8802a' : '#86703e') });
  const uo = { R: 165, L: 175, c: o.umbC, faded: o.faded, skin: holderO.skin };
  const umb = umbrella(holder.prop, uo);
  const bp = other && o.backpack ? backpack(other, o.backpack) : null, sb = other && o.backpack ? schoolBadge(other) : null;
  let rH = null, rU = null, rO = null;
  if (set.reflG) { if (other) rO = reflectPup(other, set.reflG, defs, set.ground); rH = reflectPup(holder, set.reflG, defs, set.ground); rU = umbrella(rH.prop, uo); }
  const rs = rainShadow(defs, set.slant || 0.15);
  if (set.rain) set.rain.setAttribute('mask', rs.url);
  const drips = rimDrips(set.top, o.seed || 11), spl = pointSplash(set.top, (o.seed || 11) + 1);
  const fsH = footShadow(set.shadowL, defs, 0.32), fsO = other ? footShadow(set.shadowL, defs, 0.3) : null;
  return {
    holder, other, umb, wet, rs,
    // pH / pO: poses (pO may be null); open: canopy 0..1; wetK: soaked 0..1; dens: rain density
    update(t, pH, pO, open, wetK, dens = 1, opt = {}) {
      umb.set(open, t); if (rU) rU.set(open, t);
      if (other && pO) { other.pose(pO); if (bp) bp(pO); if (sb) sb(pO); other.g.setAttribute('display', 'inline'); if (rO) rO.g.setAttribute('display', 'inline'); }
      else if (other) { other.g.setAttribute('display', 'none'); if (rO) rO.g.setAttribute('display', 'none'); }
      holder.pose(pH);
      wet(wetK, pH.torso || 0);
      umb.g.setAttribute('display', opt.noUmb ? 'none' : 'inline'); if (rU) rU.g.setAttribute('display', opt.noUmb ? 'none' : 'inline');
      const G = set.ground;
      fsH(pH.x, G + 2, 150 * pH.s); if (fsO && pO) fsO(pO.x, G + 2, 150 * pO.s * other.o.s);
      // rain shadow and rim water only once the canopy is up and open
      const gm = umb.geo(), up = Math.cos(rad(pH.propRot || 0)) > 0.5 && !opt.noUmb;
      if (open > 0.6 && up) {
        const a = propW(holder, pH, -gm.w, gm.rimY), b = propW(holder, pH, gm.w, gm.rimY), tp = propW(holder, pH, 0, gm.topY);
        const [L, R] = a[0] < b[0] ? [a, b] : [b, a];
        rs.set(L, R, tp, G - Math.min(L[1], R[1]) + 40);
        const back = (pH.f || 1) > 0 ? L : R, dir = (pH.f || 1) > 0 ? 1 : -1;
        drips(t, [back, [back[0] + dir * 30, back[1] + 4], [back[0] + dir * 64, back[1] + 2]], G, dens);
      } else { rs.set(null); drips(t, null, G, 0); }
      const sh = torsoW(holder, pH, -30, -RIG.T + 6);
      spl(t, sh[0], sh[1], dens > 0.3 && (open < 0.6 || up) && wetK > 0.05 && !opt.noSplash);
    },
  };
}

// =====================================================================
// S0 — hook: a dad and his kid walk home under one umbrella; the rain soaks one shoulder; "คุณเคยสังเกตไหม"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.04) contrast(1.04)';
  const set = soiWalk(S), L = t => t - A, G = set.ground;
  const pair = umbPair(S, set, DAD, kidAt(MEM_KID), { backpack: '#e0574b', seed: 21 });
  lightCast(S, set, [], { light: { rim: '#ffe8c8', rimOp: 0.5 } });
  const q = dropQ(S.ui, 860, 760);
  const X = lt => 560 + 140 * lt;
  const shots = [
    { t: 0, cam: lt => frameAt(X(lt) + 90, 1180, 1.16, 540, 1080), to: lt => frameAt(X(lt) + 90, 1180, 1.24, 540, 1080) },
    { t: L(P.H2) - 0.05, cam: lt => frameAt(X(lt) - 36, 1150, 3.2, 600, 1020), to: lt => frameAt(X(lt) - 36, 1150, 3.4, 600, 1020) },
    { t: L(P.H4) - 0.05, cam: lt => frameAt(X(lt) + 160, 1214, 2.2, 580, 1160), to: lt => frameAt(X(lt) + 160, 1214, 2.35, 580, 1160) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.7 }));
    set.update(lt);
    const x = X(lt), ph = x * 0.04;
    const pD = holdUp(pair.holder, walkP(pair.holder, x, G, 1.2, 1, ph, { amp: 13, t: lt, smile: 0.7, head: 4 }), 15);
    const kid = pair.other, pK = walkP(kid, x + 150, G, 1.2, 1, ph * 1.25 + 1, { amp: 18, t: lt + 3, smile: 0.95, head: lt > L(P.H4) - 0.05 ? -22 : -8 });
    pK.aF = [70, 30]; pK.aB = [80, 40];
    pair.update(lt, pD, pK, 1, 0.5 + 0.3 * prog(lt, L(P.H2), L(P.H4)), 1);
    q.update(lt, L(P.H4) + 0.15);
    setGrade(S, (1 - prog(lt, 0, 0.5)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1a — "ตั้งแต่ ป.1 จน ม.6": the kid waits at the school gate as the rains come; he grows a grade a cut
// =====================================================================
(() => {
  const [A, B] = SC.s1a;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.05) contrast(1.04) sepia(0.08)';
  const set = schoolGate(S), L = t => t - A;
  const ages = [0, 0.3, 0.62, 1];
  const kids = ages.map(a => { const g = svg('g', {}, set.people); const k = new Puppet(g, kidAt(a), S.L.mid.defs); return { g, k, bp: backpack(k, '#e0574b'), sb: schoolBadge(k) }; });
  const fsK = footShadow(set.shadowL, S.L.mid.defs, 0.3);
  lightCast(S, set, [], { light: { rim: '#ffe8c8', rimOp: 0.5 } });
  const chip = gradeChip11(S.ui, 40, 120);
  const sw = [L(P.A0) + 0.45, L(P.A0) + 0.95, L(P.A0) + 1.45];
  const flash = html('div', 'blackout', S.fx); flash.style.background = '#fff4e6'; flash.style.zIndex = 5;
  const shots = [
    { t: 0, cam: fA(705, 1235, 1.7, 540, 1190), to: fA(705, 1235, 1.82, 540, 1190) },
    { t: L(P.A1) - 0.1, cam: fA(600, 1150, 1.14, 540, 1060), to: fA(600, 1150, 1.2, 540, 1060) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    const dens = lerp(0.35, 1, prog(lt, L(P.A1) - 0.3, L(P.A1) + 0.4));
    set.update(lt, dens);
    const st = sw.filter(s => lt >= s).length;
    const look = lt > L(P.A1) - 0.1;
    kids.forEach((K, i) => {
      K.g.setAttribute('display', i === st ? 'inline' : 'none');
      if (i !== st) return;
      const p = standP(K.k, 720, 1435, 1.2, -1, { t: lt + i, head: look ? -24 : 4, smile: look ? 0.8 : 0.5, aF: [70, -30], aB: [80, -20] });
      if (look && lt > L(P.A1) + 0.25) p.aF = K.k.reach(p, 720 - 120 * 1.2 * K.k.o.s, 1435 - 330 * K.k.o.s * 1.2);   // a hand out to feel the rain
      K.k.pose(p); K.bp(p); K.sb(p);
      fsK(720, 1437, 150 * K.k.o.s);
    });
    chip.update(lt, 0.2, prog(lt, L(P.A0) + 0.15, L(P.A1) - 0.15));
    flash.style.opacity = Math.max(...sw.map(s => 0.6 * Math.max(0, 1 - Math.abs(lt - s) / 0.08))).toFixed(3);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1b — "พ่อจะมารอรับหน้าโรงเรียน กับร่มคันเดียว": dad waits outside under his umbrella; the kid runs out to him and
// ducks underneath; dad tilts it over him
// =====================================================================
(() => {
  const [A, B] = SC.s1b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.05) contrast(1.04) sepia(0.08)';
  const set = schoolGate(S), L = t => t - A, G = set.ground;
  const pair = umbPair(S, set, DAD, kidAt(MEM_KID), { backpack: '#e0574b', seed: 31 });
  lightCast(S, set, [], { light: { rim: '#ffe8c8', rimOp: 0.5 } });
  const t0 = L(P.A2) + 0.45, t1 = L(P.A3) - 0.3;   // the run out of the gate
  const shots = [
    { t: 0, cam: fA(560, 1160, 1.12, 540, 1070), to: fA(560, 1160, 1.17, 540, 1070) },
    { t: L(P.A2) + 1.05, cam: fA(420, 1150, 1.55, 520, 1130), to: fA(420, 1150, 1.62, 520, 1130) },
    { t: L(P.A3) - 0.05, cam: fA(420, 1000, 2.3, 540, 1000), to: fA(425, 1000, 2.42, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt + 2);
    const tilt = 16 * ease.inOutSine(prog(lt, L(P.A3) - 0.2, L(P.A3) + 0.35));
    const pD = holdUp(pair.holder, standP(pair.holder, 330, G, 1.2, 1, { t: lt, smile: lt > t0 ? 0.95 : 0.7, head: lt > t1 ? 14 : 2 }), tilt);
    if (lt > L(P.A2) + 1.05 && lt < t1) pD.aB = [-60, -110];   // a wave with the free hand
    const kid = pair.other, ks = kid.o.s;
    let pK;
    if (lt < t0) pK = standP(kid, 720, 1435, 1.2, -1, { t: lt + 3, head: 2, smile: 0.6, aF: [70, -30], aB: [80, -20] });
    else if (lt < t1) {
      const u = prog(lt, t0, t1), x = lerp(720, 480, u), gy = lerp(1435, G, u);
      pK = walkP(kid, x, gy, 1.2, -1, lt * 12, { amp: 28, run: 1, t: lt + 3, smile: 0.95, head: -6 });
      const g2 = gait(lt * 12, 28, 1); pK.lF = g2.lF; pK.lB = g2.lB; pK.aF = [60, 10]; pK.aB = [120, 60]; pK.torso = 12;
    } else pK = standP(kid, 480, G, 1.2, 1, { t: lt + 3, head: -24, smile: 1, aF: [70, 30], aB: [80, 40] });
    pair.update(lt, pD, pK, 1, 0.3 + 0.2 * prog(lt, t1, B - A), 1);
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1c — "เดินกลับบ้านด้วยกัน": tracking down the soi; the canopy leans over the kid, the rain lands on dad's back
// =====================================================================
(() => {
  const [A, B] = SC.s1c;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.05) contrast(1.04) sepia(0.08)';
  const set = soiWalk(S), G = set.ground;
  const pair = umbPair(S, set, DAD, kidAt(MEM_KID), { backpack: '#e0574b', seed: 41 });
  lightCast(S, set, [], { light: { rim: '#ffe8c8', rimOp: 0.5 } });
  const X = lt => 1500 + 140 * lt;
  const shots = [{ t: 0, cam: lt => frameAt(X(lt) + 80, 1180, 1.45, 540, 1110), to: lt => frameAt(X(lt) + 80, 1180, 1.5, 540, 1110) }];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt + 6);
    const x = X(lt), ph = x * 0.04;
    const pD = holdUp(pair.holder, walkP(pair.holder, x, G, 1.2, 1, ph, { amp: 13, t: lt, smile: 0.75, head: 8 }), 16);
    const pK = walkP(pair.other, x + 150, G, 1.2, 1, ph * 1.25 + 1, { amp: 18, t: lt + 3, smile: 0.95, head: -14 });
    pK.aF = [70, 30]; pK.aB = [80, 40];
    pair.update(lt, pD, pK, 1, 0.55 + 0.15 * lt, 1);
    setGrade(S, 0);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1d — "ถึงบ้านทีไร ตัวเราแห้งทุกครั้ง": home under the porch; the kid bounces in bone-dry while dad closes the umbrella,
// his back soaked and dripping onto the tiles
// =====================================================================
(() => {
  const [A, B] = SC.s1d;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04) sepia(0.08)';
  const set = porch(S), L = t => t - A, G = set.ground;
  const kid = new Puppet(set.people, kidAt(MEM_KID), S.L.mid.defs);
  const bp = backpack(kid, '#e0574b'), sb = schoolBadge(kid);
  const dad = new Puppet(set.people, DAD, S.L.mid.defs);
  const wet = wetPatch(dad, S.L.mid.defs, { color: '#86703e' });
  const umb = umbrella(dad.prop, { R: 165, L: 175, skin: DAD.skin });
  const sh = lightCast(S, set, [kid, dad], { light: { rim: '#ffe2a8' }, shadow: { op: 0.2, k: 0.28, blur: 8 } });
  const spark = sparkles(set.top, 9, 61);
  const drip = rimDrips(set.top, 62);
  const pud = svg('ellipse', { fill: '#d8e2e8', opacity: 0 }, set.shadowL);
  const tStop = 1.0, tClose = 0.72;
  const shots = [
    { t: 0, cam: fA(470, 1060, 1.32, 540, 1020), to: fA(480, 1060, 1.38, 540, 1020) },
    { t: L(P.A6) - 0.1, cam: fA(600, 1060, 1.9, 770, 1080), to: fA(600, 1060, 2.0, 770, 1080) },
    { t: L(P.Aend) - 0.35, cam: fA(350, 1050, 2.9, 540, 1000), to: fA(350, 1060, 3.05, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt);
    const u = ease.outCubic(prog(lt, 0, tStop)), xD = lerp(40, 380, u), xK = lerp(200, 600, ease.outCubic(prog(lt, 0, tStop + 0.1)));
    const walking = lt < tStop;
    let pD = walking ? walkP(dad, xD, G, 1.2, 1, xD * 0.04, { amp: 13, t: lt, smile: 0.7, head: 6 }) : standP(dad, xD, G, 1.2, 1, { t: lt, smile: 0.75, head: 10, torso: 4 });
    const open = 1 - prog(lt, tClose, tClose + 0.4);
    const kc = prog(lt, tClose + 0.3, tClose + 0.75);
    if (kc <= 0) holdUp(dad, pD, 16 * (1 - prog(lt, tClose - 0.2, tClose + 0.2)), 84, lerp(-112, -80, prog(lt, tClose, tClose + 0.3)));
    else { const e = ease.inOutSine(kc), shake = 10 * Math.sin((lt - tClose) * 22) * Math.max(0, 1 - Math.abs(lt - tClose - 1.0) / 0.3) * (kc >= 1 ? 1 : 0); holdCane(dad, pD, lerp(84, 60, e), lerp(-80, 10, e), lerp(0, 180, e) + shake); }   // lowered tip-down, then a shake to flick the water off
    umb.set(open, lt);
    dad.pose(pD); wet(0.78, pD.torso || 0);
    const hop = lt > L(P.A6) - 0.1 ? Math.abs(Math.sin((lt - L(P.A6) + 0.1) * 7)) * 22 * Math.max(0, 1 - (lt - L(P.A6)) / 1.2) : 0;
    let pK = lt < tStop + 0.1 ? walkP(kid, xK, G, 1.2, 1, xK * 0.05, { amp: 18, t: lt + 3, smile: 0.95, head: -8 }) : standP(kid, xK, G - hop, 1.2, -1, { t: lt + 3, smile: 1, grin: lt > L(P.A6) ? 1 : 0, head: -6, aF: [-40, -70], aB: [-130, -100] });
    kid.pose(pK); bp(pK); sb(pK);
    spark(xK, G - 300 * kid.o.s * 1.2 * 0.75, prog(lt, L(P.A6) - 0.1, L(P.A6) + 0.3) * (1 - prog(lt, L(P.Aend) - 0.5, L(P.Aend) - 0.35)), lt);
    // water running off his back onto the tiles, a puddle growing under him
    const back = torsoW(dad, pD, -40, -10), elbow = torsoW(dad, pD, -42, -60);
    drip(lt, [back, elbow, [back[0] + 10, back[1] + 6]], G + 4, lt > tStop ? 1 : 0);
    const pk = prog(lt, tStop, B - A);
    setA(pud, { cx: (xD - 40).toFixed(1), cy: G + 6, rx: (20 + 70 * pk).toFixed(1), ry: (5 + 10 * pk).toFixed(1), opacity: (0.5 * Math.min(1, pk * 3)).toFixed(2) });
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "เราเคยถามพ่อว่า ทำไมไม่ซื้อร่มคันใหญ่ / พ่อบอกว่า คันใหญ่มันหนัก พ่อไม่ชอบ": evening, the living room
// =====================================================================
function newspaper(parent) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M-10,-60 L90,-74 L96,40 L-4,52 Z', fill: '#f2ede2', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M40,-66 L46,46', stroke: '#c9c2b4', 'stroke-width': 3 }, g);
  svg('rect', { x: 0, y: -52, width: 34, height: 20, fill: '#c8343c', transform: 'rotate(-8 0 -52)' }, g);
  for (let k = 0; k < 6; k++) svg('path', { d: `M${2},${-24 + k * 12} l32,-4 M${50},${-30 + k * 12} l36,-5`, stroke: '#8a847c', 'stroke-width': 3 }, g);
  return g;
}
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.06) contrast(1.04) sepia(0.08)';
  const set = livingRoom(S), L = t => t - A;
  const dad = new Puppet(set.people, DAD, S.L.mid.defs), kid = new Puppet(set.people, kidAt(0.35), S.L.mid.defs);
  const paper = newspaper(dad.prop);
  lightCast(S, set, [dad, kid], { light: { rim: '#fff1d6', rimOp: 0.55 }, shadow: { op: 0.13, blur: 11, k: 0.2 } });
  const bq = bubble11(S.ui, 440, 600, 'ทำไมพ่อไม่ซื้อ<br>ร่มคันใหญ่ล่ะ?', 'L');
  const ba = bubble11(S.ui, 330, 560, `คันใหญ่มัน<b class="hv11">หนัก</b><br>พ่อไม่ชอบ`, 'R');
  const tB1 = L(P.B1) - 0.1, tB2 = L(P.B2) - 0.1;
  const shots = [
    { t: 0, cam: fA(540, 1200, 1.12, 540, 1080), to: fA(540, 1200, 1.17, 540, 1080) },
    { t: tB1, cam: fA(640, 1290, 2.2, 560, 1160), to: fA(640, 1290, 2.32, 560, 1160) },
    { t: tB2, cam: fA(300, 1090, 2.15, 520, 1190), to: fA(300, 1090, 2.27, 520, 1190) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5 }));
    set.update(lt);
    // dad in the armchair behind his newspaper; he lowers it to answer and grins
    const ans = lt > tB2 - 0.1;
    const pD = { x: 250, y: 1262, s: 1.2, f: 1, torso: -6, head: ans ? -4 : 8, lF: [2, 88], lB: [6, 92], t: lt, smile: ans ? 0.9 : 0.5, grin: ans && lt > L(P.B3) && lt < L(P.B4) + 0.2 ? 1 : 0, eyes: null };
    const [cx, cy] = torsoW(dad, pD, 70, ans ? -40 : -100);
    pD.aF = dad.reach(pD, cx + 30, cy); pD.aB = dad.reach(pD, cx, cy + 10); pD.propRot = ans ? 30 : -6;
    dad.pose(pD);
    // the kid at the low table, writing; turns to ask
    const ask = lt > tB1 - 0.05;
    const pK = { x: 600, y: 1452, s: 1.2, f: ask ? -1 : 1, torso: ask ? -2 : 10, head: ask ? -10 : 16 + Math.sin(lt * 1.3) * 3, lF: SIT.lF, lB: SIT.lB, t: lt + 2, smile: ask ? 0.55 : 0.5 };
    if (!ask) { const [hx, hy] = [700 + Math.sin(lt * 7) * 8, 1376]; pK.aF = kid.reach(pK, hx, hy); pK.aB = [70, 60]; }
    else { pK.aF = [60, 20]; pK.aB = [80, 50]; if (lt > L(P.B2) - 0.1) { pK.smile = 0.85; pK.head = -14; } }
    kid.pose(pK);
    bq.update(lt, L(P.B1) + 0.05, tB2 - 0.05);
    ba.update(lt, L(P.B2) + 0.3, B - A);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// insert: the khaki shirt drying on the window grille — one shoulder soaked dark, still dripping
(() => {
  const [A, B] = SC.s2i;
  const S = new Shot(A, B, [['far', 0.5, 3], ['mid', 1, 0]]);
  S.grade = 'saturate(1.06) contrast(1.05) sepia(0.08)';
  const F = S.L.far, M = S.L.mid;
  svg('rect', { x: -300, y: -300, width: 1680, height: 2600, fill: '#c8913c' }, F.s);
  svg('rect', { x: 140, y: 300, width: 800, height: 1240, rx: 14, fill: '#6a4028', stroke: INK, 'stroke-width': 10 }, F.s);
  svg('rect', { x: 180, y: 340, width: 720, height: 1160, fill: lin(F.defs, [[0, '#2a2440'], [1, '#3e3450']]) }, F.s);
  const r = rng(71);
  for (let i = 0; i < 7; i++) { const lx = 200 + r() * 680, ly = 800 + r() * 500; svg('path', { d: `M${lx},${ly + 400} Q${lx + 20},${ly + 160} ${lx + (r() - 0.5) * 240},${ly}`, fill: 'none', stroke: '#2e4a32', 'stroke-width': 60, 'stroke-linecap': 'round' }, F.s); }
  const rainW = rainField(F.s, [180, 340, 900, 1500], 90, 72, { len: 90, w: 3, op: 0.45, slant: 0.1 });
  for (let gx = 220; gx < 900; gx += 70) svg('path', { d: `M${gx},340 l0,1160`, stroke: '#3a2a26', 'stroke-width': 12 }, M.s);
  for (const gy of [660, 1000]) svg('path', { d: `M180,${gy} l720,0`, stroke: '#3a2a26', 'stroke-width': 12 }, M.s);
  svg('ellipse', { cx: 600, cy: 900, rx: 700, ry: 600, fill: rad2(M.defs, [[0, '#fff6e0', 0.25], [1, '#fff6e0', 0]]), style: 'mix-blend-mode:screen' }, M.s);
  const shirt = svg('g', {}, M.s);
  shirtOnHanger(shirt, 520, 600, 3.4);
  const drip = dripLine(M.s, [[660, 935, 1700], [710, 925, 1700], [760, 915, 1700], [640, 945, 1700], [800, 820, 1700]], 73, { color: '#e8eef2' });
  svg('path', { d: 'M520,1700 L960,1700 L920,1800 L560,1800 Z', fill: '#e8e2d6', stroke: INK, 'stroke-width': 6 }, M.s);   // the bowl catching the drips
  svg('ellipse', { cx: 740, cy: 1704, rx: 210, ry: 22, fill: '#9aaab4', stroke: INK, 'stroke-width': 4 }, M.s);
  const ripple = (() => { const rs = [0, 1, 2].map(() => svg('ellipse', { cx: 720, cy: 1704, fill: 'none', stroke: '#ffffff', 'stroke-width': 3 }, M.s)); return t => rs.forEach((e, i) => { const k = ((t * 1.6 + i / 3) % 1); setA(e, { rx: (8 + k * 150).toFixed(1), ry: (2 + k * 17).toFixed(1), opacity: ((1 - k) * 0.6).toFixed(2) }); }); })();
  vignette(M.s, M.defs, 0.55);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.05, 1.13, prog(lt, 0, B - A)), fx: 600, fy: 900, r: Math.sin(lt * 0.7) * 0.1 });
    rainW(lt); drip(lt); ripple(lt);
    shirt.setAttribute('transform', `rotate(${(Math.sin(lt * 1.6) * 1.0).toFixed(2)} 520 420)`);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3a — present: "ตอนนี้พ่อ 67 แล้ว เดินช้ากว่าเดิม": out of the clinic at dusk, the old umbrella as a walking stick; the
// ghost of the brisk young dad strides past him
// =====================================================================
(() => {
  const [A, B] = SC.s3a;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.05)';
  const set = presentStreet(S), L = t => t - A, G = set.ground;
  const pair = umbPair(S, set, SON, null, { seed: 81 });   // the son (no umbrella yet: hidden)
  const dadG = svg('g', {}, set.people);
  const old = new Puppet(dadG, DAD_OLD, S.L.mid.defs);
  const cane = umbrella(old.prop, { R: 165, L: 175, faded: true, open: 0, c: ['#8a3a40', '#e6dcc6'], skin: DAD_OLD.skin });
  const rOld = reflectPup(old, set.reflG, S.L.mid.defs, G);
  const rCane = umbrella(rOld.prop, { R: 165, L: 175, faded: true, open: 0, c: ['#8a3a40', '#e6dcc6'] });
  const fsD = footShadow(set.shadowL, S.L.mid.defs, 0.32);
  const ghostG = svg('g', { style: 'filter: sepia(0.9) saturate(0.8)', opacity: 0 }, set.people);
  const ghost = new Puppet(ghostG, DAD, S.L.mid.defs);
  lightCast(S, set, [], { light: { rim: '#ffd0b0', rimOp: 0.6 } });
  const age = ageChip11(S.ui, 40, 120);
  const XD = lt => 190 + 52 * lt;
  const shots = [
    { t: 0, cam: lt => frameAt(330, 1180, 1.15, 540, 1080), to: lt => frameAt(340, 1180, 1.2, 540, 1080) },
    { t: L(P.C1) - 0.1, cam: lt => frameAt(XD(lt) + 10, 1200, 1.6, 540, 1150), to: lt => frameAt(XD(lt) + 10, 1200, 1.68, 540, 1150) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt, 0);
    const x = XD(lt), ph = x * 0.06;
    const pD = holdCane(old, walkP(old, x, G, 1.15, 1, ph, { amp: 9, t: lt, smile: 0.55, head: 8, lean: 9 }), 54, -20, 176 + Math.sin(ph) * 4);
    old.pose(pD); cane.set(0, lt); rCane.set(0, lt);
    fsD(x, G + 2, 160);
    // the son keeps pace at his side, a hand at his elbow, the clinic's medicine bag in the other
    const pS = walkP(pair.holder, x - 150, G, 1.2, 1, ph, { amp: 9, t: lt + 2, smile: 0.6, head: 10 });
    const el = torsoW(old, pD, -20, -60); pS.aF = pair.holder.reach(pS, el[0] - 6, el[1]);
    pair.update(lt, pS, null, 0, 0, 0, { noUmb: true, noSplash: true });
    // the brisk young dad of the memories walks straight past him
    const gk = prog(lt, L(P.C1) + 0.05, B - A + 0.2), gx = x - 260 + 900 * gk;
    ghostG.setAttribute('opacity', (0.5 * Math.sin(Math.PI * gk)).toFixed(3));
    ghost.pose(walkP(ghost, gx, G, 1.2, 1, gx * 0.045, { amp: 18, t: lt, smile: 0.7, head: 0 }));
    const r = rollValue(lt, 0.25, 1.3, 40, 67);
    age.update(lt, 0.25, r.v, r.speed);
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3b — "วันหนึ่งฝนตก เป็นครั้งแรกที่เราถือร่มให้พ่อ เราเอียงร่มไปทางพ่อนิดเดียว ไหล่ของเราก็เปียกทั้งข้าง"
// =====================================================================
(() => {
  const [A, B] = SC.s3b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.05)';
  const set = presentStreet(S), L = t => t - A, G = set.ground;
  const UC = ['#8a3a40', '#e6dcc6'];
  const pair = umbPair(S, set, SON, DAD_OLD, { umbC: UC, faded: true, seed: 91 });
  const old = pair.other;
  const cane = umbrella(old.prop, { R: 165, L: 175, faded: true, open: 0, c: UC, skin: DAD_OLD.skin });
  lightCast(S, set, [], { light: { rim: '#ffd0b0', rimOp: 0.6 } });
  const arc = tiltArc(set.top);
  const x0 = 190 + 52 * (SC.s3b[0] - SC.s3a[0]);   // where S3a left them
  const tRain = L(P.C2) - 0.05, tLift = L(P.C3) - 0.7, tTake = L(P.C3) + 0.4, tOpen = L(P.C3) + 0.95, tGo = L(P.C3) + 1.6;
  const tTilt = L(P.C4) + 0.1, tWet = L(P.C5) + 0.05;
  const XD = lt => x0 + (lt < tRain ? 52 * lt : 52 * tRain) + 50 * Math.max(0, lt - tGo);
  const shots = [
    { t: 0, cam: lt => frameAt(XD(lt) - 60, 1120, 1.18, 540, 1040), to: lt => frameAt(XD(lt) - 60, 1120, 1.24, 540, 1040) },
    { t: L(P.C3) - 0.15, cam: lt => frameAt(XD(lt) - 45, 1120, 2.2, 540, 1000), to: lt => frameAt(XD(lt) - 45, 1120, 2.3, 540, 1000) },
    { t: tOpen + 0.25, cam: lt => frameAt(XD(lt) - 70, 1060, 1.5, 540, 1060), to: lt => frameAt(XD(lt) - 70, 1060, 1.56, 540, 1060) },
    { t: L(P.C4) - 0.1, cam: lt => frameAt(XD(lt) - 60, 1060, 1.42, 520, 1060), to: lt => frameAt(XD(lt) - 60, 1060, 1.5, 520, 1060) },
    { t: L(P.C5) - 0.05, cam: lt => frameAt(XD(lt) - 90, 1120, 2.0, 520, 1080), to: lt => frameAt(XD(lt) - 90, 1120, 2.08, 520, 1080) },
    { t: L(P.Cend) - 0.65, cam: lt => frameAt(XD(lt) - 137, 1073, 2.6, 400, 1100), to: lt => frameAt(XD(lt) - 137, 1073, 2.72, 400, 1100) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    const dens = ease.inOutSine(prog(lt, tRain, tRain + 1.4));
    set.update(lt + 4, dens);
    const x = XD(lt), walking = lt < tRain || lt > tGo, ph = x * 0.06;
    const lookUp = lt > tRain + 0.2 && lt < tLift;
    // พ่อ
    let pD = walking ? walkP(old, x, G, 1.15, 1, ph, { amp: 9, t: lt, smile: 0.6, head: 8, lean: 9 }) : standP(old, x, G, 1.15, 1, { t: lt, smile: 0.5, head: lookUp ? -22 : 6, torso: 8 });
    if (lt < tLift) holdCane(old, pD, 54, -20, walking ? 176 + Math.sin(ph) * 4 : 178);
    else if (lt < tTake) { const k = ease.inOutSine(prog(lt, tLift, tLift + 0.45)); holdCane(old, pD, lerp(54, 66, k), lerp(-20, -76, k), lerp(178, 64, k)); pD.head = lerp(pD.head, 10, k); }   // out of habit he lifts it to open it himself
    else { pD.aF = [80, 70]; pD.aB = [88, 80]; pD.head = lt < tOpen + 0.6 ? -16 : 2; pD.smile = 0.85; }
    if (lt > tWet + 1.2) { pD.head = -6; pD.smile = 0.75; }
    old.pose(pD);   // posed first: the son reaches for the handle in his hand
    // the son: steps in, takes the handle from him, opens it over พ่อ and walks him home, tilting it his way
    const xs = x + lerp(-150, -100, ease.inOutSine(prog(lt, tRain, tRain + 0.8))) - 28 * ease.inOutSine(prog(lt, tTake, tOpen)) - 14 * ease.inOutSine(prog(lt, tOpen + 0.3, tGo + 0.6));
    let pS = walking ? walkP(pair.holder, xs, G, 1.2, 1, ph, { amp: 9, t: lt + 2, smile: 0.65, head: 4 }) : standP(pair.holder, xs, G, 1.2, 1, { t: lt + 2, smile: 0.6, head: lookUp ? -20 : 4 });
    const tilt = 14 * ease.inOutSine(prog(lt, tTilt, tTilt + 0.8));
    let open = 0;
    if (lt < tLift + 0.2) { const el = torsoW(old, pD, -20, -60); pS.aF = pair.holder.reach(pS, el[0] - 6, el[1]); }
    else if (lt < tTake) { const k = ease.inOutSine(prog(lt, tLift + 0.2, tTake)); const tgt = propW(old, pD, 0, -8); pS.aF = pair.holder.reach(pS, lerp(pS.x + 60, tgt[0], k), lerp(pS.y - 60, tgt[1], k)); pS.head = 14; }
    else {
      // raise it high and straight, open it above both heads, then bring it down to carrying height
      const k1 = ease.inOutSine(prog(lt, tTake, tTake + 0.3)), k2 = ease.inOutSine(prog(lt, tTake + 0.3, tOpen)), kd = ease.inOutSine(prog(lt, tOpen + 0.35, tOpen + 0.85));
      const hw = propW(old, pD, 0, 0), [lx, ly] = [(hw[0] - pS.x) / 1.2, (hw[1] - pS.y) / 1.2];   // his hand's spot, in the son's frame
      // pull it back to his own side, raise it straight up behind พ่อ's head, then out to carrying position
      holdUp(pair.holder, pS, lerp(64, tilt, k1), lerp(lerp(Math.min(lx, 150), 36, k1), 64, kd), lerp(lerp(lerp(ly, -125, k1), -178, k2), -118, kd));
      if (lt < tOpen + 0.5) pS.head = -14;
      open = prog(lt, tOpen, tOpen + 0.32);
    }
    if (lt > tOpen + 0.6) pS.head = 6;
    if (lt > L(P.Cend) - 0.65) { pS.head = 24; pS.smile = 0.25; pS.eyes = 1; if (lt > L(P.Cend) - 0.2) { pS.head = -6; pS.mouthO = 0.5; } }   // he looks down at his soaked shoulder, then up: he understands
    const sonHas = lt >= tTake;
    pair.update(lt, pS, pD, open, 0.12 + 0.88 * ease.inOutSine(prog(lt, tWet, tWet + 1.0)), dens, { noUmb: !sonHas, noSplash: lt < tGo });
    cane.g.setAttribute('display', sonHas ? 'none' : 'inline'); cane.set(0, lt);
    // the "นิดเดียว" protractor at the son's grip
    const gp = propW(pair.holder, pS, 0, 0);
    arc(gp[0], gp[1] - 10, tilt, prog(lt, tTilt, tTilt + 0.3) * (1 - prog(lt, L(P.C5) - 0.35, L(P.C5) - 0.1)), lt - tTilt);
    setGrade(S, 0);
  };
  SHOTS.push(S);
})();

// memory flash: the young dad's soaked shoulder, years ago (sepia)
(() => {
  const [A, B] = SC.s3f;
  const S = new Shot(A, B, LAYERS());
  S.fadeIn = 0.22;
  const set = soiWalk(S), G = set.ground;
  const pair = umbPair(S, set, DAD, kidAt(MEM_KID), { backpack: '#e0574b', seed: 101 });
  lightCast(S, set, [], { light: { rim: '#ffe8c8', rimOp: 0.5 } });
  const X = lt => 2300 + 140 * lt;
  S.update = lt => {
    S.grade = SEPIA(lt);
    applyCam(S, shotCamF(lt, [{ t: 0, cam: lt => frameAt(X(lt) - 36, 1150, 3.2, 600, 1020), to: lt => frameAt(X(lt) - 36, 1150, 3.4, 600, 1020) }], B - A, { handheld: 0.5 }));
    set.update(lt + 9);
    const x = X(lt), ph = x * 0.04;
    const pD = holdUp(pair.holder, walkP(pair.holder, x, G, 1.2, 1, ph, { amp: 13, t: lt, smile: 0.8, head: 10 }), 16);
    const pK = walkP(pair.other, x + 150, G, 1.2, 1, ph * 1.25, { amp: 18, t: lt, smile: 0.95, head: -12 });
    pK.aF = [70, 30]; pK.aB = [80, 40];
    pair.update(lt, pD, pK, 1, 0.85, 1);
    setGrade(S, 0);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 12 ฤดูฝน / ที่ไหล่ของพ่อเปียก — rain on the lens over the blurred street
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = presentStreet(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  const lens = lensDrops(S.fx, 34, 121);
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 122, { color: '#ffcf9a', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '300px'; ic.innerHTML = umbIcon(420);
  const t1 = html('div', 'title', wrap); t1.style.top = '700px'; t1.style.font = '700 200px/1 Kanit';
  const digits = ['1', '2'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ฤดูฝน'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่ไหล่ของพ่อเปียก'); t2.style.top = '930px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1080px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt + 9); bok(lt); lens(lt, 0.9);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -12);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.08, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.4, 14, 7); unit.style.opacity = fadeIn(lt, 0.4, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5a — sepia montage: "12 ปีที่ผ่านมา พ่อเปียกแบบนี้ทุกครั้ง โดยไม่เคยบอกเราเลย" — the kid grows cut by cut, dad's back
// is soaked every time; twelve raindrop pips fill; at the end he smiles and pushes the umbrella further over his son
// =====================================================================
(() => {
  const [A, B] = SC.s5a;
  const S = new Shot(A, B, LAYERS());
  const set = soiWalk(S), L = t => t - A, G = set.ground;
  const ages = [0, 0.45, 0.75, 1];
  const pair = umbPair(S, set, DAD, kidAt(0), { backpack: '#e0574b', seed: 131 });
  const kids = ages.map(a => { const g = svg('g', {}, set.people); set.people.insertBefore(g, pair.holder.g); const k = new Puppet(g, kidAt(a), S.L.mid.defs); return { g, k, bp: backpack(k, '#e0574b'), sb: schoolBadge(k), rf: reflectPup(k, set.reflG, S.L.mid.defs, G) }; });
  pair.other.g.setAttribute('opacity', 0);
  lightCast(S, set, [], { light: { rim: '#ffe8c8', rimOp: 0.5 } });
  const chip = gradeChip11(S.ui, 40, 120);
  const tc = [0, L(P.D1) - 0.05, L(P.D1) + 1.25, L(P.D2) - 0.05];
  const xs = [200, 900, 1500, 2200];
  const X = lt => { const i = tc.filter(c => lt >= c).length - 1; return xs[i] + 140 * (lt - tc[i]); };
  const shots = [
    { t: tc[0], cam: lt => frameAt(X(lt) + 90, 1180, 1.16, 540, 1080), to: lt => frameAt(X(lt) + 90, 1180, 1.22, 540, 1080) },
    { t: tc[1], cam: lt => frameAt(X(lt) - 36, 1150, 3.2, 600, 1020), to: lt => frameAt(X(lt) - 36, 1150, 3.4, 600, 1020) },
    { t: tc[2], cam: lt => frameAt(X(lt) + 80, 1160, 1.45, 540, 1110), to: lt => frameAt(X(lt) + 80, 1160, 1.5, 540, 1110) },
    { t: tc[3], cam: lt => frameAt(X(lt) + 60, 1030, 2.1, 520, 1150), to: lt => frameAt(X(lt) + 60, 1030, 2.22, 520, 1150) },
  ];
  S.update = lt => {
    S.grade = SEPIA(lt);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6 }));
    set.update(lt + 3);
    const i = tc.filter(c => lt >= c).length - 1, x = X(lt), ph = x * 0.04;
    const last = i === 3;
    const tilt = 16 + (last ? 8 * ease.inOutSine(prog(lt, tc[3] + 0.9, tc[3] + 1.5)) : 0);
    const pD = holdUp(pair.holder, walkP(pair.holder, x, G, 1.2, 1, ph, { amp: 13, t: lt, smile: last ? 0.95 : 0.75, head: last ? 18 : 8 }), tilt);
    kids.forEach((K, j) => {
      K.g.setAttribute('display', j === i ? 'inline' : 'none'); K.rf.g.setAttribute('display', j === i ? 'inline' : 'none');
      if (j !== i) return;
      const p = walkP(K.k, x + 150, G, 1.2, 1, ph * lerp(1.25, 1.05, ages[j]) + 1, { amp: 18, t: lt + 3, smile: 0.9, head: last && lt > tc[3] + 0.5 ? -18 : -8 });
      p.aF = [70, 30]; p.aB = [80, 40];
      K.k.pose(p); K.bp(p); K.sb(p);
    });
    pair.update(lt, pD, null, 1, 0.7 + 0.2 * Math.sin(lt), 1);
    chip.update(lt, 0.2, prog(lt, 0.3, tc[3] + 0.6));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5b — present: "บางความรัก เราจะเข้าใจ ก็ตอนที่ไหล่ของเราเปียกบ้าง" — walking him home, his own shoulder soaked; พ่อ
// pushes the umbrella back to him, he tilts it back with a smile; the camera cranes up the neon street as the rain eases
// =====================================================================
(() => {
  const [A, B] = SC.s5b;
  const S = new Shot(A, B, LAYERS());
  S.fadeIn = 0.6;
  S.grade = 'saturate(1.1) contrast(1.05)';
  const set = presentStreet(S), L = t => t - A, G = set.ground;
  const UC = ['#8a3a40', '#e6dcc6'];
  const pair = umbPair(S, set, SON, DAD_OLD, { umbC: UC, faded: true, seed: 141 });
  lightCast(S, set, [], { light: { rim: '#ffd0b0', rimOp: 0.6 } });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const hearts = heartsRise(back, 560, 640, L(P.D5) + 0.4, 7, 143, 0.35);
  const tPush = L(P.D4) - 0.2;
  const X = lt => 900 + 50 * (lt - clamp(lt - (tPush - 0.3), 0, 1.6));   // they pause while พ่อ pushes it back
  const shots = [
    { t: 0, cam: lt => frameAt(X(lt) - 75, 1060, 1.6, 540, 1080), to: lt => frameAt(X(lt) - 75, 1060, 1.66, 540, 1080) },
    { t: L(P.D4) - 0.4, cam: lt => frameAt(X(lt) - 70, 1000, 2.05, 540, 1060), to: lt => frameAt(X(lt) - 70, 1000, 2.15, 540, 1060) },
    { t: L(P.D5) - 0.1, cam: lt => frameAt(X(lt) - 60, 1120, 1.5, 540, 1150), to: lt => frameAt(X(lt) - 60, 1120, 1.5, 540, 1150) },
    { t: L(P.D5) + 0.6, move: 2.4, cam: lt => frameAt(X(lt) - 40, 900, 1.1, 540, 1080), to: lt => frameAt(X(lt) - 40, 860, 1.08, 540, 1060) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -260 }));
    const dens = lerp(1, 0.45, prog(lt, L(P.D5), B - A));
    set.update(lt + 12, dens);
    const x = X(lt), ph = x * 0.06, paused = lt > tPush - 0.3 && lt < tPush + 1.3;
    // พ่อ notices the soaked shoulder, turns and pushes the umbrella back to his son; the son smiles and tilts it back
    const turned = lt > tPush && lt < tPush + 0.9;
    const push = ease.inOutSine(prog(lt, tPush + 0.15, tPush + 0.55)) * (1 - ease.inOutSine(prog(lt, tPush + 0.75, tPush + 0.95)));
    const back = ease.inOutSine(prog(lt, tPush + 1.0, tPush + 1.5));
    const tilt = lerp(lerp(14, -10, push), 14, lt > tPush + 0.95 ? back : 0);
    const gap = ease.inOutSine(prog(lt, tPush - 0.3, tPush)) * (1 - ease.inOutSine(prog(lt, tPush + 1.0, tPush + 1.3)));   // room for พ่อ to turn
    const pS = holdUp(pair.holder, paused ? standP(pair.holder, x - 142 - 20 * gap, G, 1.2, 1, { t: lt + 2, smile: 0.9, head: 6, torso: -5 * gap }) : walkP(pair.holder, x - 142, G, 1.2, 1, ph, { amp: 9, t: lt + 2, smile: 0.9, head: 6 }), tilt, 64, -118);
    if (lt > tPush + 0.95 && lt < tPush + 1.9) { pS.grin = 1; pS.head = 12; }
    let pD = paused ? standP(pair.other, x + 14 * gap, G, 1.15, turned ? -1 : 1, { t: lt, smile: 0.8, head: turned ? -16 : 2, torso: 8 }) : walkP(pair.other, x, G, 1.15, 1, ph, { amp: 9, t: lt, smile: 0.8, head: 2, lean: 9 });
    pair.holder.pose(pS);
    if (turned) { const g = propW(pair.holder, pS, 0, -60); pD.aF = pair.other.reach(pD, g[0] + 6, g[1]); }
    pair.update(lt, pS, pD, 1, 1, dens);
    leak(lt, 0.15 + 0.35 * prog(lt, L(P.D5), B - A));
    hearts(lt);
    setGrade(S, 0);
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
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#5a3458'], [0.6, '#2e1f40'], [1, '#150e20']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 151, { color: '#ffcf9a', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const rainE = rainField(G.s, [0, 0, 1080, 1920], 90, 152, { len: 50, w: 2, op: 0.18, slant: 0.12 });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 153, ['#ffd66b', '#ffffff', '#ffcf9a'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '290px';
  duo.innerHTML = `<span class="duo7">${av11('son', 190)}</span><span class="duo7h">${umbIcon(190)}</span><span class="duo7">${av11('dad', 190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '6px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['1', '2'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ฤดูฝน'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่ไหล่ของพ่อเปียก'); t2.style.top = '808px'; t2.style.font = '600 92px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'วันพ่อปีนี้ ลองถือร่มให้พ่อสักครั้ง'); sub.style.top = '975px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้พ่อดูสักครั้ง</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); rainE(lt); leak(lt, 0.4);
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
  const dip = tt => prog(t, tt - 0.3, tt) * (1 - prog(t, tt, tt + 0.45));
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, DURATION - 0.45, DURATION) + 0.85 * dip(SC.s3a[0])).toFixed(3);
  const fl = tt => prog(t, tt - 0.25, tt) * (1 - prog(t, tt, tt + 0.3));
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1a[0]) * 0.6, fl(SC.s3f[0] + 0.1) * 0.5, fl(SC.s4[0]), fl(SC.s5a[0]) * 0.6, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
