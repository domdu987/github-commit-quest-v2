// "15 ปีใหม่ ที่แม่อยู่บนรถทัวร์" — scenes timed to the narration in vo.js (VO.P holds phrase onsets: H hook, A–C, the
// title, D, แม่'s midnight announcement M (her own voice), F, E). Every scene is a shot list on a lit set.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0a: [0, P.H2 - 0.05], s0b: [P.H2 - 0.05, P.A0 - 0.3], s1: [P.A0 - 0.3, P.A3 - 0.1], s1b: [P.A3 - 0.1, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3],
  s3a: [P.C0 - 0.3, P.C3 - 0.1], s3b: [P.C3 - 0.1, P.title], s4: [P.title, P.D0 - 0.1], s5: [P.D0 - 0.1, P.F2 - 0.1], s5i: [P.F2 - 0.1, P.E0 - 0.1],
  s6: [P.E0 - 0.1, P.end], s7: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
const SIT = { lF: [8, 172], lB: [18, 166] };
// light the cast: rim + core shade on the people groups, a soft cast shadow behind the given puppets
function lightCast13(S, set, groups, pups, o = {}) {
  const Lt = set.light || {}, f = charLight(S.L.mid.defs, Object.assign({ ux: Lt.ux, uy: Lt.uy }, o.light || {}));
  groups.forEach(g => g.setAttribute('filter', f));
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
// sitting in a bus seat: thighs forward, shins down to the footrest, hands in the lap
function chairP(pup, x, s, f, o = {}) { return Object.assign({ x, y: SEAT13 - 18, s, f, torso: -4, head: 2, lF: [4, 84], lB: [10, 90], aF: [62, 14], aB: [70, 20], smile: 0.6 }, o); }
function shotCamF(lt, shots, end, o = {}) {
  let i = 0; while (i + 1 < shots.length && lt >= shots[i + 1].t) i++;
  const endOf = j => (j + 1 < shots.length ? shots[j + 1].t : end);
  const at = j => { const sh = shots[j]; return lerpCam(sh.cam(lt), (sh.to || sh.cam)(lt), ease.inOutSine(prog(lt, sh.t, endOf(j)))); };
  let cam = at(i);
  if (shots[i].move && i > 0) cam = lerpCam(at(i - 1), cam, ease.inOutCubic(prog(lt, shots[i].t, shots[i].t + shots[i].move)));
  const hh = o.handheld ?? 1;
  cam.x += hh * (Math.sin(lt * 1.1) * 2.2 + Math.sin(lt * 2.7 + 1) * 1.1);
  cam.y += hh * (Math.sin(lt * 0.9 + 2) * 1.8 + Math.sin(lt * 2.3) * 0.9);
  if (o.bump) { cam.y += Math.sin(lt * 11) * o.bump + Math.sin(lt * 4.3) * o.bump * 0.6; cam.r = (cam.r || 0) + Math.sin(lt * 3.1) * 0.08 * o.bump; }   // a moving bus
  cam.r = (cam.r || 0) + hh * Math.sin(lt * 0.7) * 0.12;
  cam.y = Math.max(cam.y, o.minY ?? 2);
  return cam;
}
const fA = (...a) => () => frameAt(...a);
// a phone held up in front of the chest (seen from the back)
function holdPhone13(pup, p, fx = 74, fy = -RIG.T + 34) {
  const [tx, ty] = torsoW(pup, p, fx, fy);
  p.aB = pup.reach(p, tx - 6 * (p.f || 1), ty + 8); p.aF = pup.reach(p, tx + 6 * (p.f || 1), ty - 2); p.propRot = -10;
  return [tx, ty];
}
// world point → a puppet's prop frame (front wrist, after pose)
function toProp(pup, p, wx, wy) {
  const s = (p.s || 1) * pup.o.s, f = p.f || 1, lx = (wx - p.x) / (f * s) - pup.wristF[0], ly = (wy - p.y) / s - pup.wristF[1], a = rad(-(p.propRot || 0));
  return [lx * Math.cos(a) - ly * Math.sin(a), lx * Math.sin(a) + ly * Math.cos(a)];
}
// แม่ in uniform: jacket front, gold scarf, name tag, pencil skirt, bow on the bun
function dressMae(pup) {
  const j = jacket13(pup, { inner: '#fbf6ee', lapel: '#6a1c2a', scarf: '#e8b13a', tag: true }), sk = skirt13(pup, '#2a2c4c', { hem: '#1e2038' });
  bunBow13(pup);
  return (p, t) => { j(p, t); sk(p); };
}
function dressLuk(pup) { const j = jacket13(pup, { inner: '#f6efe2', lapel: '#3f5f96', button: '#d8d2c4', pockets: true }); return (p, t) => j(p, t); }
// the busload: uncle in row 2, passengers in rows 3–8 (party hats on some); returns [{pup, x}]
function seatPax(set, defs, o = {}) {
  const uncle = o.uncle ?? 2, empty = o.empty || [], out = [];
  const lung = new Puppet(set.people, LUNG13, defs); out.push({ pup: lung, x: ROW13(uncle), k: uncle });
  const rows = [2, 3, 4, 5, 6, 7, 8].filter(k => k !== uncle && !empty.includes(k));
  PAX13.forEach((c, i) => {
    const k = rows[i]; if (!k) return;
    const pup = new Puppet(set.people, Object.assign({ pants: '#3a3448', pantsDark: '#2e2a3c', shoe: '#5a4a42', shoeDark: '#46382f', sole: '#2a2020', sleeve: 'short' }, c.o), defs);
    if (c.hat) partyHat13(pup, c.hat);
    out.push({ pup, x: ROW13(k), k });
  });
  return out;
}
function posePax(pax, lt, o = {}) {
  for (const q of pax) {
    const ph = q.k * 1.7;
    const p = chairP(q.pup, q.x, 1.2, -1, { t: lt + ph, head: (o.look ? -8 : 2) + Math.sin(lt * 1.3 + ph) * 2, smile: o.smile ?? 0.55, torso: -4 + Math.sin(lt * 9 + ph) * 0.6 });
    p.y += Math.sin(lt * 11 + ph) * 1.2;   // the bus hums under them
    if (o.clap && lt > o.clap) {
      const c = Math.abs(Math.sin((lt - o.clap) * 9 + ph)), [cx, cy] = torsoW(q.pup, p, 66, -RIG.T + 10);
      p.aF = q.pup.reach(p, cx + (p.f || 1) * 10 * c, cy - 4); p.aB = q.pup.reach(p, cx - (p.f || 1) * 18 * c, cy + 4); p.smile = 1; p.grin = 1; p.head = -6;
    }
    if (o.skip && o.skip.includes(q.k)) continue;
    q.pup.pose(p);
  }
}

// =====================================================================
// S0a — hook: the tour bus on the highway at night; fireworks over a distant town
// =====================================================================
(() => {
  const [A, B] = SC.s0a;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.1) contrast(1.05)';
  const set = highway13(S, { busX: 200, busS: 0.78, bursts: [{ t: 0.15, x: 760, y: 560, c: '#ffd166', r: 200, n: 32 }, { t: 0.55, x: 330, y: 700, c: '#ff7a9a', r: 160, n: 28 }, { t: -0.6, x: 560, y: 420, c: '#8fd0ff', r: 150, n: 26 }].concat(burstPlan(1.2, B - A + 0.4, 4, [100, 380, 1000, 860], 1401, undefined, { rMin: 120, rMax: 190, n: 28 })) });
  const shots = [{ t: 0, cam: fA(640, 1100, 1.04, 540, 1000), to: fA(660, 1090, 1.1, 540, 1000) }];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5 }));
    set.update(lt);
    setGrade(S, (1 - prog(lt, 0, 0.5)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S0b — "ถ้าคนที่ยื่นน้ำให้คุณบนรถ ไม่เคยได้อยู่บ้านตอนปีใหม่เลย คุณเคยสังเกตเขาไหม": แม่ hands the uncle his water,
// then stands at the windshield watching the fireworks over a town she won't be in
// =====================================================================
(() => {
  const [A, B] = SC.s0b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.05)';
  const L = t => t - A;
  const set = busCabin(S, { bursts: burstPlan(0, B - A, 9, [-200, 680, 2600, 940], 1411), wsBursts: burstPlan(L(P.H3) - 0.4, B - A, 5, [-180, 480, 200, 760], 1412, undefined, { rMin: 60, rMax: 110 }) });
  const D = S.L.mid.defs;
  const pax = seatPax(set, D, { uncle: 2, empty: [3] });
  const lady = new Puppet(set.people, { skin: '#e2b08a', skinShade: '#c9926c', hair: '#2a1f1c', hairStyle: 'fluffy', top: 'hoodie', shirt: '#7fb069', shirtDark: '#64944f', shirtLight: '#98c884', pants: '#3a3448', pantsDark: '#2e2a3c', seed: 149 }, D);   // a passenger in row 1 that year
  partyHat13(lady, '#ff9fc0');
  const mae = new Puppet(set.stand, MAE13, D), dress = dressMae(mae);
  const drv = new Puppet(set.people, DRIVER13, D);
  const wheel = svg('g', {}, set.arms); svg('ellipse', { cx: -30, cy: 1080, rx: 16, ry: 60, fill: 'none', stroke: '#2a2228', 'stroke-width': 12, transform: 'rotate(-18 -30 1080)' }, wheel);
  const bot = bottle13(mae.prop, 0.9); bot.setAttribute('transform', 'translate(0,-8) scale(0.9)');
  const carry = basket13(mae);
  lightCast13(S, set, [set.people, set.stand], [mae], { light: { rim: '#ffcf8a', rimOp: 0.7 }, shadow: { op: 0.12, k: 0.2, blur: 11 } });
  const q = glowQ(S.ui, 840, 330);
  const shots = [
    { t: 0, cam: fA(815, 960, 2.0, 540, 1000), to: fA(812, 960, 2.1, 540, 1000) },
    { t: L(P.H3) - 0.05, cam: fA(236, 880, 2.2, 640, 990), to: fA(240, 880, 2.34, 650, 990) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, bump: 1.2, minY: -400 }));
    set.update(lt); set.clock('23:52');
    posePax(pax, lt);
    const pl = chairP(lady, ROW13(1), 1.2, -1, { t: lt, smile: 0.5 }); lady.pose(pl);
    const pd = chairP(drv, 70, 1.2, -1, { t: lt, smile: 0.5, head: 4 }); const [wx, wy] = [-20, 1050]; pd.aF = drv.reach(pd, wx, wy); pd.aB = drv.reach(pd, wx + 10, wy + 30); drv.pose(pd);
    let p;
    if (lt < L(P.H3) - 0.05) {   // handing the uncle his water
      p = standP(mae, 895, set.ground, 1.2, -1, { t: lt, smile: 0.95, head: 10, torso: 8 });
      const give = ease.inOutCubic(prog(lt, 0.15, 0.7)) * (1 - ease.inOutCubic(prog(lt, 1.35, 1.7)));
      const [hx, hy] = [lerp(820, 790, give), lerp(1150, 1078, give)];
      p.aF = mae.reach(p, hx, hy);
      const u = pax[0], pu = chairP(u.pup, u.x, 1.2, 1, { t: lt, smile: 0.9, grin: lt > 0.8 ? 1 : 0, head: -6, torso: 6 });
      pu.aF = u.pup.reach(pu, 800 - 4, 1080 + 8 * (1 - give)); u.pup.pose(pu);
      bot.setAttribute('display', lt < 1.45 ? 'inline' : 'none');
    } else {   // at the windshield, watching the town's fireworks
      p = standP(mae, 300, set.ground, 1.2, -1, { t: lt, smile: lerp(0.6, 0.3, prog(lt, L(P.H3), L(P.H4))), head: -12, torso: 2, aF: [80, 30] });
      bot.setAttribute('display', 'none');
    }
    mae.pose(p); dress(p, lt); carry();
    q.update(lt, L(P.H5) + 0.1);
    q.el.style.display = lt > L(P.H5) ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — "แม่เราเป็นพนักงานต้อนรับบนรถทัวร์ สิบห้าปีแล้ว ที่ทุกคืนสิ้นปี": the terminal, platform 92; แม่ carries the
// basket of water and snack boxes to her bus; the "31 ธ.ค." calendar flips through fifteen New Year's Eves
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.04)';
  const L = t => t - A;
  const set = terminal13(S), D = S.L.mid.defs;
  const mae = new Puppet(set.people, MAE13, D), dress = dressMae(mae), carry = basket13(mae);
  lightCast13(S, set, [set.people], [mae], { light: { rim: '#ffd59a', rimOp: 0.7 }, shadow: { op: 0.16, k: 0.2, blur: 10 } });
  const cal = yearCal13(S.ui, 70, 110);   // (the card is zoomed 1.22)
  const tStop = L(P.A1) + 0.3;
  const XW = lt => lerp(1080, 760, ease.outCubic(prog(lt, 0, tStop)));
  const shots = [
    { t: 0, cam: fA(620, 1050, 1.12, 540, 1000), to: fA(640, 1050, 1.16, 540, 1000) },
    { t: L(P.A1) - 0.1, cam: fA(720, 1020, 1.75, 600, 1080), to: fA(725, 1020, 1.85, 600, 1080) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6, minY: -300 }));
    set.update(lt);
    const walking = lt < tStop;
    const p = walking ? walkP(mae, XW(lt), set.ground, 1.2, -1, lt * 6.4, { amp: 14, t: lt, smile: 0.85, head: -2 })
      : standP(mae, 760, set.ground, 1.2, -1, { t: lt, smile: 0.9, head: lt > L(P.A2) ? -8 : 4, torso: 2 });
    if (!walking) { p.aF = [70, 10]; }   // a little wave to the driver
    p.aB = [104, 70];
    mae.pose(p); dress(p, lt); carry();
    cal.update(lt, L(P.A1) - 0.05, L(P.A3) - 0.2);
    cal.el.style.display = lt > L(P.A1) - 0.1 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1b — "แม่อยู่บนถนน": the bus small on the long road at night, tail lights, the town glowing ahead
// =====================================================================
(() => {
  const [A, B] = SC.s1b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.05)';
  const set = highway13(S, { busX: 300, busS: 0.6, bursts: burstPlan(0, 2, 3, [0, 500, 1000, 900], 1421) });
  const shots = [{ t: 0, cam: fA(560, 1180, 1.0, 540, 1080), to: fA(520, 1170, 1.06, 540, 1080) }];
  S.update = lt => { applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.4 })); set.update(lt); };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — flashback: "ทุกปี เรานับถอยหลังกับยายที่บ้าน พอเที่ยงคืน แม่จะส่งไลน์มาว่า สวัสดีปีใหม่ลูก แม่แจกน้ำอยู่นะ"
// ยาย and the girl at the ขันโตก, the TV counting down, แม่'s plate under the ฝาชี; at midnight the phone buzzes
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'sepia(0.28) saturate(1.12) contrast(1.03) brightness(1.02)';
  const L = t => t - A, tMid = L(P.B2) + 0.05;
  const set = isanHome13(S, { bursts: burstPlan(tMid, B - A, 5, [640, 420, 960, 640], 1431, undefined, { rMin: 50, rMax: 90 }), tvBursts: burstPlan(tMid, B - A, 4, [810, 900, 970, 960], 1432, undefined, { rMin: 24, rMax: 40, n: 14, w: 2.4 }) });
  const D = S.L.mid.defs;
  const yai = new Puppet(set.people, YAI13, D), sk = skirt13(yai, mudmeeFill(D), { hem: '#e8b13a', half: 34 });
  const kid = new Puppet(set.people, KID13, D);
  const ph = phoneProp(kid.prop, '#f07aa8');
  lightCast13(S, set, [set.people], [yai, kid], { light: { rim: '#ffd59a', rimOp: 0.6 }, shadow: { op: 0.2, k: 0.24 } });
  const ban = lineBanner13(S.ui, 150, 'สวัสดีปีใหม่ลูก แม่แจกน้ำอยู่นะ ');
  const shots = [
    { t: 0, cam: fA(525, 1110, 1.3, 540, 1010), to: fA(527, 1110, 1.33, 540, 1010) },
    { t: L(P.B1) - 0.1, cam: fA(578, 1250, 3.3, 540, 1040), to: fA(578, 1250, 3.5, 540, 1040) },
    { t: L(P.B2) - 0.1, cam: fA(525, 1080, 1.3, 540, 1040), to: fA(527, 1080, 1.34, 540, 1040) },
    { t: L(P.B3) + 0.05, cam: fA(360, 1112, 2.4, 640, 1010), to: fA(360, 1112, 2.4, 640, 1010) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt);
    const n = Math.max(0, Math.ceil(tMid - lt)); set.tv(lt < tMid ? String(Math.min(10, n)) : '2556', lt > tMid);
    const cheer = lt > tMid && lt < L(P.B3) + 0.05;
    const py = sitP(yai, 190, set.ground, 1.2, 1, { t: lt, torso: 6, head: cheer ? -10 : 0, smile: cheer ? 1 : 0.75, grin: cheer ? 1 : 0 });
    if (cheer) { const c = Math.abs(Math.sin(lt * 9)), [cx, cy] = torsoW(yai, py, 72, -RIG.T + 66); py.aF = yai.reach(py, cx + 8 * c, cy); py.aB = yai.reach(py, cx - 16 * c, cy + 6); }   // clapping, below her face
    yai.pose(py); sk(py);
    const pk = sitP(kid, 360, set.ground, 1.2, 1, { t: lt + 1, torso: 8, head: cheer ? -12 : 4, smile: cheer ? 1 : 0.7, grin: cheer ? 1 : 0 });
    if (cheer) { pk.aF = [-6, -40]; pk.aB = [200, 226]; ph.g.setAttribute('display', 'none'); }
    else if (lt > L(P.B3) + 0.05) { holdPhone13(kid, pk); pk.head = 14; pk.smile = lerp(0.85, 0.4, prog(lt, L(P.B5), L(P.B5) + 0.6)); ph.g.setAttribute('display', 'inline'); }
    else ph.g.setAttribute('display', 'none');
    kid.pose(pk);
    ph.scr.setAttribute('fill', lt > L(P.B3) ? '#c8f5d4' : '#d8e8ff');
    ban.update(lt, L(P.B3) + 0.15, L(P.B4) - 0.15);
    ban.el.style.display = lt > L(P.B3) + 0.1 ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3a — present, matched on the girl's close-up: "ปีนี้ เราเลยแอบจองที่นั่ง รถเที่ยวที่แม่ทำงาน" — the daughter at the
// terminal in a cap and mask, her ticket for seat 1A; she peeks from behind a pillar as แม่ boards
// =====================================================================
(() => {
  const [A, B] = SC.s3a;
  const S = new Shot(A, B, LAYERS());
  S.fadeIn = 0.45;
  S.grade = 'saturate(1.08) contrast(1.04)';
  const L = t => t - A;
  const set = terminal13(S), D = S.L.mid.defs;
  const luk = new Puppet(set.people, LUK13, D), dl = dressLuk(luk), dis = disguise13(luk);
  const mae = new Puppet(set.people, MAE13, D), dress = dressMae(mae), carry = basket13(mae);
  const ph = phoneProp(luk.prop, '#2a2b36');
  lightCast13(S, set, [set.people], [luk, mae], { light: { rim: '#ffd59a', rimOp: 0.7 }, shadow: { op: 0.16, k: 0.2, blur: 10 } });
  const tk = ticket13(S.ui, 150, 150);
  const tWide = L(P.C2) - 0.1;
  const shots = [
    { t: 0, cam: fA(424.8, 953.6, 1.92, 649, 1017), to: fA(424.8, 953.6, 2.0, 649, 1017) },   // matched to the girl's close-up (same head size and place)
    { t: tWide, cam: fA(500, 1050, 1.12, 540, 1000), to: fA(515, 1050, 1.16, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.6, minY: -300 }));
    set.update(lt);
    let p;
    if (lt < tWide) {
      p = standP(luk, 420, set.ground, 1.2, 1, { t: lt, smile: 0.9, head: 10 }); holdPhone13(luk, p); ph.g.setAttribute('display', 'inline');
      set.pillarFront.setAttribute('display', 'none');
    } else {   // peeking out from behind the pillar
      p = standP(luk, 150, set.ground, 1.2, 1, { t: lt, smile: 0.9, head: -4, torso: 20 + Math.sin(lt * 3) * 2, aF: [40, -20] });
      ph.g.setAttribute('display', 'none'); set.pillarFront.setAttribute('display', 'inline');
    }
    luk.pose(p); dl(p, lt); dis(1, 1);
    ph.scr.setAttribute('fill', '#ffe9a8');
    const pm = lt > tWide ? walkP(mae, lerp(900, 690, prog(lt, tWide, B - A)), set.ground, 1.2, -1, lt * 6.4, { amp: 14, t: lt, smile: 0.8 }) : standP(mae, 2000, set.ground, 1.2, -1, {});
    pm.aB = [104, 70];
    mae.pose(pm); dress(pm, lt); carry();
    tk.update(lt, L(P.C1) - 0.05, L(P.C1) + 0.35, L(P.C1) + 0.75);
    tk.el.style.display = lt > L(P.C1) - 0.1 && lt < tWide ? 'block' : 'none';
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3b — "พอแม่เดินมาแจกน้ำถึงที่นั่งเรา แม่ก็ยืนนิ่งไปเลย": แม่ works down the aisle; at row 1 the cap and mask come off;
// she freezes (crash zoom, the bottle slips)
// =====================================================================
(() => {
  const [A, B] = SC.s3b;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.08) contrast(1.05)';
  const L = t => t - A;
  const set = busCabin(S, { bursts: burstPlan(0, B - A, 6, [-200, 680, 2600, 940], 1441) }), D = S.L.mid.defs;
  const pax = seatPax(set, D, { uncle: 3, empty: [2] });
  const luk = new Puppet(set.people, LUK13, D), dl = dressLuk(luk), dis = disguise13(luk);
  const mae = new Puppet(set.stand, MAE13, D), dress = dressMae(mae), carry = basket13(mae);
  const drv = new Puppet(set.people, DRIVER13, D);
  const bot = bottle13(mae.prop, 0.9); bot.setAttribute('transform', 'translate(0,-8) scale(0.9)');
  const drop = svg('g', {}, set.top); bottle13(drop, 0.9);
  lightCast13(S, set, [set.people, set.stand], [mae], { light: { rim: '#ffcf8a', rimOp: 0.7 }, shadow: { op: 0.12, k: 0.2, blur: 11 } });
  const tTwo = L(P.C4) - 0.1, tOff = L(P.C4) + 0.25, tFreeze = L(P.C5) - 0.1;
  const XW = lt => lerp(1240, 640, ease.outCubic(prog(lt, 0, tTwo)));
  const shots = [
    { t: 0, cam: () => frameAt(XW(0) - 60, 960, 1.6, 540, 1000), to: () => frameAt(XW(tTwo) - 40, 960, 1.65, 540, 1000) },
    { t: tTwo, cam: fA(552, 940, 2.1, 540, 1000), to: fA(552, 940, 2.18, 540, 1000) },
    { t: tFreeze, cam: fA(552, 910, 2.2, 540, 1000), to: fA(552, 910, 2.2, 540, 1000) },
  ];
  S.update = lt => {
    const cam = shotCamF(lt, shots, B - A, { handheld: 0.5, bump: 1.0, minY: -400 });
    if (lt > tFreeze) { const k = ease.outCubic(prog(lt, tFreeze, tFreeze + 0.22)); const c2 = frameAt(552, 910, lerp(2.2, 2.5, k), 540, 1000); Object.assign(cam, { x: c2.x + Math.sin(lt * 60) * 3 * (1 - k), y: c2.y, z: c2.z }); }   // crash zoom on the two of them
    applyCam(S, cam);
    set.update(lt); set.clock('23:58');
    posePax(pax, lt);
    const pd = chairP(drv, 70, 1.2, -1, { t: lt, smile: 0.5, head: 4 }); pd.aF = drv.reach(pd, -20, 1050); pd.aB = drv.reach(pd, -10, 1080); drv.pose(pd);
    // the daughter, disguised in row 1, turns to the aisle and takes the cap and mask off
    const turned = lt > tTwo;
    const pl = chairP(luk, ROW13(1), 1.2, turned ? 1 : -1, { t: lt, smile: turned ? 1 : 0.7, grin: lt > tOff + 0.2 ? 1 : 0, head: turned ? -4 : 2, torso: turned ? 6 : -4 });
    const off = prog(lt, tOff, tOff + 0.35);
    if (turned && lt < tOff + 0.4) { const [hx, hy] = torsoW(luk, pl, -46, -RIG.T - 110 - off * 50); pl.aB = luk.reach(pl, hx, hy); }   // the far hand, behind her head
    luk.pose(pl); dl(pl, lt); dis(1 - off, 1 - off);
    // แม่
    let p;
    if (lt < tTwo) {
      p = walkP(mae, XW(lt), set.ground, 1.2, -1, lt * 6.4, { amp: 12, t: lt, smile: 0.85, head: 4 });
      if (lt > 0.1 && lt < 0.6) { const k = Math.sin(Math.PI * prog(lt, 0.1, 0.6)); p.aF = mae.reach(p, lerp(XW(lt) - 40, ROW13(3) + 60, k), lerp(1150, 1080, k)); }
      bot.setAttribute('display', 'inline');
    } else if (lt < tFreeze) {
      p = standP(mae, 640, set.ground, 1.2, -1, { t: lt, smile: 0.9, head: 8, torso: 6 });
      p.aF = mae.reach(p, 568, 1080);
      bot.setAttribute('display', 'inline');
    } else {   // frozen: eyes wide, mouth "O", the bottle slips and drops
      p = standP(mae, 640, set.ground, 1.2, -1, { t: lt, smile: 0.4, head: -2, torso: 0, eyes: 1, mouthO: 0.9 });
      p.aF = [70, 60];
      bot.setAttribute('display', 'none');
    }
    p.aB = [104, 70];
    mae.pose(p); dress(p, lt); carry();
    const df = lt - tFreeze - 0.1, [dx, dy] = [600, 1080];
    drop.setAttribute('display', df > 0 ? 'inline' : 'none');
    if (df > 0) { const y = Math.min(set.ground - 30, dy + 900 * df * df), b = y >= set.ground - 30 ? Math.abs(Math.sin((df - 0.36) * 14)) * Math.exp(-(df - 0.36) * 5) * 30 : 0; drop.setAttribute('transform', `translate(${dx - df * 40},${(y - b).toFixed(1)}) rotate(${(df * 520).toFixed(0)})`); }
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 15 ปีใหม่ / ที่แม่อยู่บนรถทัวร์ — over the blurred cabin; the bus icon drives across fifteen sparks
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = busCabin(S, { bursts: burstPlan(0, 3, 5, [-200, 420, 2000, 820], 1451) });
  S.L.far.el.style.filter = 'blur(14px) brightness(0.55) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 1452, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '360px';
  ic.innerHTML = `<span class="bus13">${busIcon13(360)}</span><span class="spk13">${Array.from({ length: 15 }, (_, i) => `<i style="--i:${i}"></i>`).join('')}</span>`;
  const bus = ic.querySelector('.bus13'), spk = [...ic.querySelectorAll('.spk13 i')];
  const t1 = html('div', 'title', wrap); t1.style.top = '620px'; t1.style.font = '700 210px/1 Kanit';
  const digits = ['1', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ปีใหม่'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่แม่อยู่บนรถทัวร์'); t2.style.top = '870px'; t2.style.font = '600 100px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1012px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt); bok(lt);
    const kb = ease.outCubic(prog(lt, 0.0, 0.9));
    bus.style.transform = `translateX(${lerp(560, -40, kb).toFixed(1)}px) translateY(${(Math.abs(Math.sin(lt * 14)) * -4).toFixed(1)}px)`;
    spk.forEach((s, i) => { const t0 = 0.05 + (14 - i) * 0.055, k = spring(lt, t0, 18, 7); s.style.opacity = fadeIn(lt, t0, 0.06); s.style.transform = `scale(${(0.3 + 0.7 * k).toFixed(3)})`; });
    digits.forEach((d, i) => { const t0 = 0.3 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.5, 14, 7); unit.style.opacity = fadeIn(lt, 0.5, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.7, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.7, 1.2))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 1.0, 1.4)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — "เที่ยงคืนตรง แม่หยิบไมค์ขึ้นมาเหมือนทุกปี" + แม่ on the PA: "สวัสดีปีใหม่ค่ะ ผู้โดยสารทุกท่าน ปีนี้ ลูกสาวของดิฉัน
// ก็นั่งอยู่บนรถคันนี้ด้วยนะคะ" — the cabin cheers; "15 ปี นี่เป็นปีแรก"
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.1) contrast(1.05)';
  const L = t => t - A, tMid = L(P.D0) + 0.35;
  const set = busCabin(S, {
    bursts: [{ t: tMid, x: 700, y: 760, c: '#ffd166', r: 220, n: 32 }, { t: tMid + 0.25, x: 1250, y: 820, c: '#ff7a9a', r: 200, n: 30 }].concat(burstPlan(tMid + 0.5, B - A, 30, [-300, 680, 2700, 900], 1461, undefined, { rMin: 160, rMax: 250, n: 30 })),
    wsBursts: burstPlan(tMid, B - A, 14, [-200, 470, 220, 800], 1462, undefined, { rMin: 70, rMax: 130 }),
  }), D = S.L.mid.defs;
  const pax = seatPax(set, D, { uncle: 3, empty: [2] });
  const luk = new Puppet(set.people, LUK13, D), dl = dressLuk(luk);
  const lukS = new Puppet(set.stand, LUK13, D), dlS = dressLuk(lukS);   // standing up for the hug
  const mae = new Puppet(set.stand, MAE13, D), dress = dressMae(mae);
  const drv = new Puppet(set.people, DRIVER13, D);
  const mic = mic13(mae.prop);
  const waves = paWaves13(set.top), wavesC = paWaves13(set.top);
  const trL = tears(set.top, 1463, { spread: 0.3, drift: -1, n: 3 }), trM = tears(set.top, 1464, { spread: 0.3, drift: 1, n: 2 });
  const conf = confetti13(set.top, [200, 520, 1500, 1400], 70, 1465, L(P.Mend) + 0.15);
  const clk = clock13(S.ui, 60, 140);
  lightCast13(S, set, [set.people, set.stand], [mae, lukS], { light: { rim: '#ffcf8a', rimOp: 0.75 }, shadow: { op: 0.12, k: 0.2, blur: 11 } });
  const tGrab = L(P.D1) - 0.1, tUp = L(P.D2) - 0.1, tPA = L(P.M0) - 0.1, tLuk = L(P.M2) - 0.1, tTwo = L(P.M3) - 0.1, tCheer = L(P.Mend) + 0.2, tClose = L(P.F0) - 0.1;
  const shots = [
    { t: 0, cam: fA(520, 930, 1.18, 540, 1000), to: fA(515, 930, 1.24, 540, 1000) },
    { t: tGrab, cam: fA(380, 930, 2.1, 540, 1000), to: fA(380, 930, 2.16, 540, 1000) },
    { t: tUp, cam: fA(385, 915, 2.0, 540, 1000), to: fA(390, 915, 2.08, 540, 1000) },
    { t: tPA, cam: fA(585, 940, 1.42, 540, 1000), to: fA(590, 940, 1.5, 540, 1000) },
    { t: tLuk, cam: fA(466, 944, 2.3, 600, 1010), to: fA(466, 944, 2.42, 600, 1010) },
    { t: tTwo, cam: fA(390, 925, 1.85, 540, 1000), to: fA(390, 925, 1.93, 540, 1000) },
    { t: tCheer, cam: fA(640, 940, 1.22, 540, 1000), to: fA(630, 940, 1.28, 540, 1000) },
    { t: tClose, cam: fA(395, 900, 2.0, 540, 1000), to: fA(395, 900, 2.1, 540, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, bump: 0.9, minY: -400 }));
    set.update(lt, { tvFlash: lt > tMid && Math.sin(lt * 10) > 0 }); set.clock(lt < tMid ? '23:59' : '00:00');
    posePax(pax, lt, { look: lt > tMid && lt < tGrab + 0.5, smile: lt > tMid ? 0.9 : 0.6, clap: tCheer });
    const pd = chairP(drv, 70, 1.2, -1, { t: lt, smile: lt > tMid ? 0.9 : 0.5, head: 4 }); pd.aF = drv.reach(pd, -20, 1050); pd.aB = drv.reach(pd, -10, 1080); drv.pose(pd);
    // the daughter: in row 1 looking up at แม่; stands for the hug at the cheer
    const standing = lt > tCheer;
    luk.g.setAttribute('display', standing ? 'none' : 'inline'); lukS.g.setAttribute('display', standing ? 'inline' : 'none');
    const pl = chairP(luk, ROW13(1), 1.2, -1, { t: lt, smile: lt > tLuk ? 0.85 : 0.75, head: lt > tPA ? -8 : 2, torso: -2 });
    luk.pose(pl); dl(pl, lt);
    const crying = lt > tLuk + 0.3;
    // แม่
    let p, micOn = lt > tGrab + 0.25;
    if (lt < tGrab) p = standP(mae, 300, set.ground, 1.2, 1, { t: lt, smile: lt > tMid ? 0.95 : 0.7, head: lt > tMid ? -10 : 4, torso: 2 });
    else if (lt < tUp) {
      p = standP(mae, 330, set.ground, 1.2, -1, { t: lt, smile: 0.9, head: 6, torso: 10 });
      const k = ease.inOutCubic(prog(lt, tGrab, tGrab + 0.35)), [cx, cy] = [273, 1018];
      p.aF = mae.reach(p, lerp(330 - 60, cx, k), lerp(1150, cy, k)); p.propRot = 0;
      if (lt > tGrab + 0.45) { const u = ease.inOutCubic(prog(lt, tGrab + 0.45, tUp)); p.aF = mae.reach(p, lerp(cx, 300, u), lerp(cy, 1050, u)); }
    } else {
      p = standP(mae, 300, set.ground, 1.2, 1, { t: lt, smile: 0.9, head: lt > tLuk ? 10 : -2, torso: 0, grin: 0 });
      const [mx, my] = torsoW(mae, p, 66, -RIG.T + 6);   // at the collar, below the chin: never over the face
      p.aF = mae.reach(p, mx, my); p.propRot = -34;
      if (lt > tTwo && lt < tCheer) { const [gx, gy] = torsoW(mae, p, 104, -44); p.aB = mae.reach(p, gx, gy); }   // "my daughter" — an open hand toward her, low
    }
    if (standing) {   // arm round her shoulders; the daughter leans in
      const ps = standP(lukS, 480, set.ground, 1.2, -1, { t: lt, smile: 1, grin: lt < tClose ? 1 : 0, head: 6, torso: 6 });
      const [sx, sy] = torsoW(lukS, ps, -20, -RIG.T + 14); p.aB = mae.reach(p, sx, sy);
      const [ox, oy] = torsoW(mae, p, 10, -RIG.T + 20); ps.aF = lukS.reach(ps, ox + 30, oy + 30);
      lukS.pose(ps); dlS(ps, lt);
      const [ex, ey] = torsoW(lukS, ps, HEAD_C[0] + 46, HEAD_C[1] + 12); trL(ex, ey, lt > tClose ? 1 : 0, lt);
    } else {
      const [ex, ey] = torsoW(luk, pl, HEAD_C[0] + 46, HEAD_C[1] + 12); trL(ex, ey, crying ? 1 : 0, lt);
    }
    if (lt > tUp) { p.mouthO = 0; }
    mae.pose(p); dress(p, lt);
    const [cx, cy] = toProp(mae, p, 273, 1030);
    mic(cx, cy, micOn);
    const [mex, mey] = torsoW(mae, p, HEAD_C[0] + 46, HEAD_C[1] + 12); trM(mex, mey, lt > tTwo ? 0.8 : 0, lt);
    const talk = (lt > L(P.M0) && lt < L(P.M1) + 1.2) || (lt > L(P.M2) && lt < L(P.Mend));
    const [wx, wy] = wristFW(mae, p);
    waves(wx + 20, wy - 30, talk ? 0.9 : 0, lt, 1);
    wavesC(1200, 470, talk ? 0.7 : 0, lt + 0.3, 1);
    conf(lt);
    clk.update(lt, 0.05, tMid);
    clk.el.style.display = lt < tGrab ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5i — "ที่เราได้นับถอยหลังกับแม่": the window — fireworks over the fields outside, and on the glass, the two of them
// =====================================================================
(() => {
  const [A, B] = SC.s5i;
  const S = new Shot(A, B, [['out', 0.5, 1.2], ['glass', 1, 0]]);
  S.grade = 'saturate(1.12) contrast(1.05)';
  const O = S.L.out, G = S.L.glass;
  const out = nightOutside13(O, [-400, -200, 1500, 2100], { horizon: 1260, speed: 520, moon: [880, 360], bursts: burstPlan(0, B - A + 0.5, 12, [60, 260, 1020, 900], 1471, undefined, { rMin: 120, rMax: 210, n: 30 }) });
  // reflections: แม่ and the daughter, mirrored and faint on the glass
  const refl = svg('g', { opacity: 0.5, filter: blurFilter(G.defs, 1.4), transform: 'translate(1080,0) scale(-1,1)' }, G.s);
  const mae = new Puppet(refl, MAE13, G.defs), dress = dressMae(mae);
  const luk = new Puppet(refl, LUK13, G.defs), dl = dressLuk(luk);
  svg('rect', { x: -100, y: -100, width: 1280, height: 2200, fill: lin(G.defs, [[0, '#8fa8d8', 0.12], [1, '#2a1e40', 0.2]]) }, G.s);
  const streaks = svg('g', { style: 'mix-blend-mode:screen' }, G.s);
  for (let k = 0; k < 4; k++) svg('path', { d: `M${100 + k * 260},1900 L${420 + k * 260},0 L${470 + k * 260},0 L${150 + k * 260},1900 Z`, fill: '#ffffff', opacity: 0.05 }, streaks);
  // the window frame and gathered curtains in the foreground, the sill below
  svg('path', { d: 'M-100,-100 L1180,-100 L1180,2100 L-100,2100 Z M60,140 L1020,140 Q1050,140 1050,170 L1050,1530 Q1050,1560 1020,1560 L60,1560 Q30,1560 30,1530 L30,170 Q30,140 60,140 Z', fill: '#c9a47a', 'fill-rule': 'evenodd' }, G.s);
  svg('rect', { x: 26, y: 136, width: 1028, height: 1428, rx: 32, fill: 'none', stroke: '#5a3a26', 'stroke-width': 12 }, G.s);
  for (const [x, sg] of [[0, 1], [1080, -1]]) svg('path', { d: `M${x - sg * 60},100 L${x + sg * 120},100 Q${x + sg * 150},800 ${x + sg * 70},1100 Q${x + sg * 120},1400 ${x + sg * 110},1700 L${x - sg * 60},1700 Z`, fill: '#8e2a3c', stroke: INK, 'stroke-width': 5 }, G.s);
  svg('rect', { x: -100, y: 1600, width: 1280, height: 600, fill: lin(G.defs, [[0, '#4a2a22'], [1, '#1e120e']]) }, G.s);
  const sw = lightSweep13(G.s, G.defs, [-200, 0, 1300, 1600], { speed: 520, op: 0.18, w: 300 });
  const flash = svg('rect', { x: -100, y: -100, width: 1280, height: 2200, fill: '#ffd59a', opacity: 0, style: 'mix-blend-mode:screen' }, G.s);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.0, 1.06, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    out.update(lt); sw(lt);
    const pm = standP(mae, 370, 1760, 2.2, 1, { t: lt, smile: 0.95, head: 6, eyes: 0 }), pl = standP(luk, 700, 1760, 2.2, -1, { t: lt, smile: 1, head: 8, eyes: 0, torso: 6 });
    const [sx, sy] = torsoW(luk, pl, -20, -RIG.T + 14); pm.aB = mae.reach(pm, sx, sy);
    mae.pose(pm); dress(pm, lt); luk.pose(pl); dl(pl, lt);
    const [k, c] = out.fw.flash(lt); flash.setAttribute('fill', c); flash.setAttribute('opacity', Math.min(0.25, k * 0.25).toFixed(3));
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — "บางคนไม่ได้กลับบ้านช่วงปีใหม่ เพราะเขาต้องพาคนอื่นกลับบ้าน": the bus under the fireworks; crane up into the sky
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, LAYERS());
  S.grade = 'saturate(1.1) contrast(1.05)';
  const L = t => t - A, tCrane = L(P.E1) - 0.3;
  const set = highway13(S, { busX: 140, busS: 0.8, bursts: burstPlan(0, B - A + 0.5, 16, [-200, -500, 1200, 900], 1481, undefined, { rMin: 120, rMax: 220, n: 30 }) });
  const back = behindSvg(S);
  const hearts = heartsRise(back, 540, 900, L(P.E2) + 0.1, 7, 1482, 0.3);
  const leak = lightLeak(S.fx);
  const shots = [
    { t: 0, cam: fA(600, 1220, 1.18, 540, 1100), to: fA(620, 1210, 1.24, 540, 1100) },
    { t: tCrane, move: 1.8, cam: fA(560, 120, 1.05, 540, 900), to: fA(560, 40, 1.04, 540, 900) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.4, minY: -1400 }));
    set.update(lt); hearts(lt);
    leak(lt, 0.15 + 0.4 * prog(lt, tCrane, B - A));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 6);
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
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#7a3a5a'], [0.6, '#3e1e3e'], [1, '#1c1024']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const fw = fireworks13(G.s, G.defs, burstPlan(0.2, 3.2, 7, [120, 120, 960, 520], 1491, undefined, { rMin: 70, rMax: 130 }));
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 1492, { color: '#ffd9a0', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 1493, ['#ffd66b', '#ffffff', '#ffd9a0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '290px';
  duo.innerHTML = `<span class="duo7">${av13('luk', 190)}</span><span class="duo7h">${busIcon13(170)}</span><span class="duo7">${av13('mae', 190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '10px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['1', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ปีใหม่'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '104px';
  const t2 = html('div', 'title', wrap, 'ที่แม่อยู่บนรถทัวร์'); t2.style.top = '808px'; t2.style.font = '600 92px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'ปีใหม่นี้ ขอบคุณคนที่พาเรากลับบ้านนะ'); sub.style.top = '960px'; sub.style.font = '500 48px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1100px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ทำงานคืนข้ามปี</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  S.update = lt => {
    bok(lt); leak(lt, 0.4); fw.update(lt);
    popSquash(duo, lt, 0.15, '', -10);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
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
  black.style.opacity = ((1 - prog(t, 0, 0.3)) + prog(t, DURATION - 0.45, DURATION)).toFixed(3);
  const fl = tt => prog(t, tt - 0.25, tt) * (1 - prog(t, tt, tt + 0.3));
  warm.style.opacity = (0.85 * Math.max(fl(SC.s2[0]) * 0.8, fl(SC.s4[0]), fl(SC.s5[0]) * 0.5, fl(SC.s6[0]) * 0.6, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
