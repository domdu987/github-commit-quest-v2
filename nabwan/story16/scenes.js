// "50 กุหลาบ ที่ยายจำไม่ได้" — scenes timed to the narration in vo.js (VO.P: H hook, A–B the young couple and the album,
// C she forgets, the title, D the granddaughter, E the market at dawn, T ตาบุญ introduces himself, G the album again,
// Y ยายแก้ว's line, K ตาบุญ's line at night, L the lesson). Bookend: the hook is the morning he gives her the rose and she
// does not know him; the ending is the same two chairs at night, his hand on hers.
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = {
  s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.C0 - 0.3], s3: [P.C0 - 0.3, P.title], s4: [P.title, P.D0 - 0.1],
  s5: [P.D0 - 0.1, P.E0 - 0.3], s6: [P.E0 - 0.3, P.T0 - 0.3], s7: [P.T0 - 0.3, P.G0 - 0.3], s8: [P.G0 - 0.3, P.K0 - 0.3], s9: [P.K0 - 0.3, P.end], s10: [P.end, DURATION],
};
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));
const SHOTS = [];
const SEPIA = 'sepia(0.5) saturate(0.92) contrast(1.03) brightness(1.04)';
const WARM = 'saturate(1.06) contrast(1.04)';
const NIGHT = 'saturate(1.02) contrast(1.06) brightness(0.96)';
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function behindSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.ui); }
const LAYERS = () => [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 13]];
function lightCast16(S, set, groups, pups, o = {}) {
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
function handsOnTable(pup, p, y, lt, mv = 0) {
  const f = p.f || 1, S = p.s * pup.o.s;
  const fx = p.x + f * (70 + Math.sin(lt * 5) * 5 * mv) * S, bx = p.x + f * 46 * S;
  p.aF = pup.reach(p, fx, y - 6); p.aB = pup.reach(p, bx, y - 2);
  return [fx, y - 6];
}
function handsInLap(pup, p) { const [x, y] = torsoW(pup, p, 50, -18); p.aF = pup.reach(p, x + 8, y + 6); p.aB = pup.reach(p, x - 6, y + 10); }
function holdBoth(pup, p, x, y, w = 18) { const f = p.f || 1; p.aF = pup.reach(p, x - f * w, y - 8); p.aB = pup.reach(p, x - f * w, y + 14); }
const talk = (lt, a, b) => (lt > a && lt < b ? 0.35 + 0.35 * Math.max(0, Math.sin(lt * 15)) + 0.2 * Math.max(0, Math.sin(lt * 23 + 1)) : 0);
function eyesW(pup, p) { const [hx, hy] = headW(pup, p), R = pup.o.R, S = p.s * pup.o.s, f = p.f || 1, a = rad((p.torso || 0) + (p.head || 0)); const pt = (lx, ly) => [hx + f * S * (lx * Math.cos(a) - ly * Math.sin(a)), hy + S * (lx * Math.sin(a) + ly * Math.cos(a))]; return [pt(R * 0.5, R * 0.06), pt(R * 0.02, R * 0.06)]; }
// a rose in the world, its stem held at (x, y); rot tilts it
function roseAt(g, s = 0.9, o = {}) { const w = svg('g', {}, g), r = svg('g', {}, w); rose16(r, s, o); return { g: w, at(x, y, rot = 0, show = true) { w.setAttribute('display', show ? 'inline' : 'none'); w.setAttribute('transform', `translate(${x.toFixed(1)},${(y + 20).toFixed(1)}) rotate(${rot.toFixed(1)})`); } }; }
const TOPY = TBL16.top;

// =====================================================================
// the two of them by the side table: ยายแก้ว in her rattan chair (left), ตาบุญ on his wooden chair (right)
// =====================================================================
function homeScene(S, o = {}) {
  const set = house16(S, { mode: o.mode || 'now' }), D = S.L.mid.defs, then = o.mode === 'then';
  const yai = new Puppet(set.people, then ? YAI16_Y : YAI16, D), ysk = sarong16(yai, then ? '#e8d8b8' : '#7a3a5a', { batik: then ? '#c8a070' : '#e8b04a', dot: then ? '#fbf7ef' : '#f6efe2' });
  if (!then) hairClip16(yai);
  const ta = new Puppet(set.people, then ? TA16_Y : TA16, D);
  const album = svg('g', {}, set.top); albumClosed16(album, 0.9); album.setAttribute('transform', `translate(${TBL16.x},${TOPY + 6})`);
  const rose = roseAt(set.top, 0.85);
  lightCast16(S, set, [set.people], [yai, ta], o.mode === 'night' ? { light: { rim: '#ffd8a0', rimOp: 0.7 }, shadow: { op: 0.22, k: 0.2, blur: 9 } } : { light: { rim: '#fff1c4', rimOp: 0.72 }, shadow: { op: 0.17, k: 0.24, blur: 10 } });
  return { set, yai, ta, album, rose, yaiPose: p => { yai.pose(p); ysk(p); } };
}
const YAI_SIT = (pup, lt, o = {}) => chairP(pup, YAIX, SEAT16, 1.2, 1, Object.assign({ t: lt, smile: 0.6, head: 2, torso: 2 }, o));
const TA_SIT = (pup, lt, o = {}) => chairP(pup, TAX, SEAT16, 1.2, -1, Object.assign({ t: lt, smile: 0.7, head: 4 }, o));
// the offering: he holds the rose out over the table; k 0..1 = reaching out, take = she has it
function offer(m, lt, k, take, o = {}) {
  const pt = TA_SIT(m.ta, lt, Object.assign({ smile: 0.95, head: 8, torso: 4 + 8 * k }, o.ta || {}));
  const rx = lerp(640, 552, ease.inOutCubic(k)), ry = lerp(1090, 1046, ease.inOutCubic(k));
  if (take < 1) { pt.aF = m.ta.reach(pt, rx + 6, ry); const [bx, by] = torsoW(m.ta, pt, 40, -20); pt.aB = m.ta.reach(pt, bx, by + 20); } else handsOnTable(m.ta, pt, TOPY, lt);
  m.ta.pose(pt);
  const py = YAI_SIT(m.yai, lt, Object.assign({ smile: 0.4, head: 4 }, o.yai || {}));
  if (take > 0) { const tx = lerp(rx, 455, ease.inOutCubic(clamp(take - 0.2))), ty = lerp(ry, 1095, ease.inOutCubic(clamp(take - 0.2))); py.aF = m.yai.reach(py, tx - 6, ty + 4); py.aB = m.yai.reach(py, tx - 14, ty + 18); m.rose.at(tx, ty, lerp(-10, 42, ease.inOutCubic(clamp(take - 0.2))), true); }
  else { handsInLap(m.yai, py); m.rose.at(rx, ry, -10, true); }
  m.yaiPose(py);
  return { pt, py };
}

// =====================================================================
// S0 — hook (today): he holds out a rose; she does not know who he is; his face
// =====================================================================
(() => {
  const [A, B] = SC.s0, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const m = homeScene(S), q = glowQ(S.ui, 300, 560);
  const tCUy = L(P.H2) - 0.05, tCUt = L(P.H4) - 0.05;
  const shots = [
    { t: 0, cam: fA(545, 990, 1.45, 540, 1010), to: fA(545, 990, 1.52, 540, 1010) },
    { t: tCUy, cam: fA(380, 975, 2.2, 690, 1000), to: fA(380, 975, 2.3, 690, 1000) },
    { t: tCUt, cam: fA(702, 975, 2.2, 400, 1000), to: fA(702, 975, 2.3, 400, 1000) },
  ];
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    m.set.update(lt);
    m.set.notes(6);
    offer(m, lt, prog(lt, 0.2, 1.4), 0, { yai: { smile: 0.25, head: si === 1 ? 8 : 2, eyes: 1 }, ta: { smile: si === 2 ? 0.85 : 0.95, eyes: si === 2 ? 0.7 : 1 } });
    q.update(lt, tCUy + 0.2); q.el.style.display = si === 1 ? 'block' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — 49 years ago (sepia): "ตาบุญให้กุหลาบยายแก้ว ปีละหนึ่งดอก ทุกวาเลนไทน์ มา 49 ปี" — he comes in with the first rose
// =====================================================================
(() => {
  const [A, B] = SC.s1, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = SEPIA;
  const m = homeScene(S, { mode: 'then' }), { set, yai, ta, rose, album } = m;
  const chip = timeChip16(S.ui, 60, 130, '49 ปีก่อน · พ.ศ. 2521', true);
  const back = behindSvg(S), hearts = heartsRise(set.top, 470, 940, L(P.A2) + 0.1, 5, 1611, 0.28);
  album.setAttribute('display', 'none');
  const book = svg('g', {}, set.top); albumClosed16(book, 0.75); book.setAttribute('transform', `translate(500,${TOPY + 6})`);
  const tTwo = L(P.A1) - 0.05, tPress = L(P.A2) - 0.05;
  const shots = [
    { t: 0, cam: fA(600, 990, 1.15, 540, 1000), to: fA(610, 990, 1.18, 540, 1000) },
    { t: tTwo, cam: fA(510, 950, 2.0, 540, 1000), to: fA(510, 950, 2.08, 540, 1000) },
    { t: tPress, cam: fA(470, 1000, 1.7, 540, 1010), to: fA(470, 1000, 1.78, 540, 1010) },
  ];
  const XW = lt => lerp(860, 640, ease.inOutSine(prog(lt, 0.1, tTwo - 0.1)));
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt);
    let p;
    if (lt < tTwo - 0.1) { p = walkP(ta, XW(lt), set.ground, 1.2, -1, lt * 6, { amp: 12, t: lt, smile: 0.8, head: 4 }); const [hx, hy] = torsoW(ta, p, -30, -30); p.aB = ta.reach(p, hx, hy); rose.at(0, 0, 0, false); }
    else p = standP(ta, 640, set.ground, 1.2, -1, { t: lt, smile: 1, grin: lt > tPress ? 1 : 0, head: 10, torso: 10 });
    const k = prog(lt, tTwo, tTwo + 0.6), take = prog(lt, tTwo + 0.9, tTwo + 1.4);
    const rx = lerp(560, 520, k), ry = lerp(1080, 1030, k);
    if (lt >= tTwo - 0.1 && take < 1) p.aF = ta.reach(p, rx + 8, ry);
    ta.pose(p);
    const py = YAI_SIT(yai, lt, { smile: lt > tTwo + 0.3 ? 1 : 0.6, head: lt > tTwo ? -4 : 8, eyes: lt > tTwo + 1.5 ? 0.6 : 1 });
    if (lt > tPress) { const kp = prog(lt, tPress, tPress + 0.6); py.aF = yai.reach(py, lerp(455, 500, kp), lerp(1095, TOPY - 10, kp)); py.aB = yai.reach(py, 470, TOPY - 6); rose.at(lerp(455, 500, kp), lerp(1095, TOPY - 6, kp), lerp(42, 80, kp), kp < 0.95); }
    else if (take > 0) { py.aF = yai.reach(py, lerp(rx, 455, take) - 6, lerp(ry, 1095, take) + 4); py.aB = yai.reach(py, lerp(rx, 455, take) - 14, lerp(ry, 1095, take) + 16); rose.at(lerp(rx, 455, take), lerp(ry, 1095, take), lerp(-10, 42, take), true); }
    else { handsOnTable(yai, py, TOPY, lt); rose.at(rx, ry, -10, lt >= tTwo - 0.1); }
    m.yaiPose(py);
    hearts(lt);
    chip.update(lt, 0.2); chip.el.style.display = lt < tTwo ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — "ยายทับดอกไม้ไว้ในสมุดทุกดอก แล้วเขียนกำกับไว้ทุกหน้า": the album, page after page; sepia warms to today
// =====================================================================
(() => {
  const [A, B] = SC.s2, L = t => t - A;
  const S = new Shot(A, B, LAYERS());
  const Al = albumMacro16(S, { young: true });
  const card = albumCard16(S.ui, 90, 110);
  const t1 = L(P.B1) - 0.2, tEnd = B - A;
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(540, 960, 1.22, 540, 940), to: fA(540, 970, 1.3, 540, 940) }], tEnd, { handheld: 0.35, minY: -600 }), { dof: false });
    Al.update(lt);
    // the first page holds, then pages turn faster and faster, years jumping
    const u = prog(lt, 0.7, tEnd - 0.2), flips = Math.floor(ease.inCubic(u) * 16), year = Math.min(49, 1 + Math.round(flips * 3)), turn = u > 0 && flips < 16 ? (ease.inCubic(u) * 16) % 1 : 0;
    Al.set({ year, turn, yai: { x: lerp(880, 300, Math.sin(Math.PI * turn) * 0.9) , y: 1240 - Math.sin(Math.PI * turn) * 120 }, glowK: lt > t1 ? 0.6 * Math.sin(Math.PI * prog(lt, t1, t1 + 0.8)) : 0, t: lt });
    card.update(lt, 0.15, tEnd - 0.3);
    const sep = 1 - prog(lt, 0.8, tEnd - 0.3);
    S.root.style.filter = `sepia(${(0.5 * sep).toFixed(3)}) saturate(${(0.92 + 0.14 * (1 - sep)).toFixed(3)}) contrast(1.04)`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "สองปีก่อน ยายเริ่มลืม ลืมกุญแจ ลืมชื่อหลาน จนวันหนึ่ง ยายจำตาไม่ได้": the notes go up around the house; the
// granddaughter at the door; then he comes in with her tea and she looks at him like a stranger
// =====================================================================
(() => {
  const [A, B] = SC.s3, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const m = homeScene(S), { set, yai, ta, rose, album } = m;
  const lan = new Puppet(set.people, LAN16, S.L.mid.defs);
  const chip = timeChip16(S.ui, 60, 130, '2 ปีก่อน', false);
  const keys = svg('g', {}, set.top); svg('circle', { r: 9, fill: 'none', stroke: '#c8a050', 'stroke-width': 4 }, keys); svg('path', { d: 'M6,6 L24,22 M16,16 L20,12 M20,20 L24,16', stroke: '#c8a050', 'stroke-width': 4, 'stroke-linecap': 'round' }, keys);
  const qS = glowQ(S.ui, 0, 0), qB = glowQ(S.ui, 300, 560);
  rose.at(0, 0, 0, false);
  const tLan = L(P.C2) + 0.9, tTa = L(P.C3) - 0.05, tCU = L(P.C4) + 0.35;
  const shots = [
    { t: 0, cam: fA(560, 900, 1.15, 540, 960), to: fA(570, 900, 1.18, 540, 960) },
    { t: tTa, cam: fA(545, 960, 2.0, 540, 1000), to: fA(545, 960, 2.08, 540, 1000) },
    { t: tCU, cam: fA(702, 975, 2.25, 400, 1000), to: fA(702, 975, 2.32, 400, 1000) },
  ];
  S.update = lt => {
    const si = shotIx(lt, shots);
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt);
    set.notes(1 + 5 * prog(lt, L(P.C1) - 0.2, tTa - 0.3), lt);
    // her: looking for the keys, puzzled at the granddaughter, blank at him
    const look = lt < tLan ? Math.sin(lt * 2.2) * 14 : 0;
    const py = YAI_SIT(yai, lt, { smile: lt > tTa ? 0.2 : 0.3, head: look + (lt > tLan ? -6 : 4), eyes: 1 });
    handsInLap(yai, py); m.yaiPose(py);
    keys.setAttribute('transform', `translate(${(TBL16.x + 70).toFixed(1)},${TOPY - 6})`); keys.setAttribute('display', lt < tLan ? 'inline' : 'none');
    // the granddaughter waves from the door
    const lanOn = lt > tLan - 0.2 && lt < tTa;
    lan.g.setAttribute('display', lanOn ? 'inline' : 'none');
    if (lanOn) { const pl = standP(lan, 930, set.ground, 1.2, -1, { t: lt, smile: 1, grin: 1, head: 4 }); const [hx, hy] = torsoW(lan, pl, 50, -RIG.T); pl.aF = lan.reach(pl, hx + 10, hy - 30 - 14 * Math.sin(lt * 12)); lan.pose(pl); }
    // him: in his chair, then (one day) he comes in from the door with her tea; in the close-up he sits, his smile fading
    let pt;
    if (si === 0) { pt = TA_SIT(ta, lt, { smile: 0.8, head: 6 }); handsOnTable(ta, pt, TOPY, lt); ta.g.setAttribute('display', lt < tLan - 0.2 ? 'inline' : 'none'); }
    else { ta.g.setAttribute('display', 'inline'); pt = TA_SIT(ta, lt, { smile: lerp(0.9, 0.15, prog(lt, tCU, tCU + 0.8)), head: si === 2 ? 10 : 6, eyes: si === 2 ? 0.75 : 1 }); handsOnTable(ta, pt, TOPY, lt); }
    ta.pose(pt);
    qS.update(lt, tLan + 0.2); qS.el.style.display = lanOn ? 'block' : 'none';
    if (lanOn) { const [hx, hy] = headW(yai, py); qS.el.style.left = (540 + (hx - 560) * 1.17 + 40).toFixed(0) + 'px'; qS.el.style.top = (960 + (hy - 900) * 1.17 - 150).toFixed(0) + 'px'; qS.el.style.transform += ' scale(0.6)'; }
    qB.update(lt, tTa + 0.25); qB.el.style.display = si === 1 ? 'block' : 'none';
    chip.update(lt, 0.15); chip.el.style.display = lt < tTa ? 'flex' : 'none';
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — title: 50 กุหลาบ / ที่ยายจำไม่ได้
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const set = house16(S, { mode: 'now' });
  S.L.far.el.style.filter = 'blur(14px) brightness(0.5) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const back = behindSvg(S);
  const bok = floaters(back, [0, 300, 1080, 1300], 16, 1612, { color: '#ffb0b8', rMin: 14, rMax: 40, speed: 12, op: 0.24, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '250px';
  ic.innerHTML = `<span class="fan16">${Array.from({ length: 5 }, (_, i) => `<i style="--i:${i}">${roseIcon16(100, { dry: i !== 2 })}</i>`).join('')}</span>`;
  const icons = [...ic.querySelectorAll('i')];
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 220px/1 Kanit';
  const digits = ['5', '0'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'กุหลาบ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '110px';
  const t2 = html('div', 'title', wrap, 'ที่ยายจำไม่ได้'); t2.style.top = '860px'; t2.style.font = '600 104px/1 Kanit'; t2.style.color = '#ffc4d0';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '995px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffc4d0', boxShadow: '0 0 16px rgba(255,180,200,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    set.update(lt); bok(lt);
    icons.forEach((e, i) => { const k = spring(lt, 0.05 + i * 0.06, 16, 6.5), a = (i - 2) * 14 * Math.min(1, k); e.style.opacity = fadeIn(lt, 0.05 + i * 0.06, 0.08); e.style.transform = `translateY(${((1 - k) * -120).toFixed(1)}px) rotate(${(a + Math.sin(lt * 2 + i) * 3).toFixed(1)}deg)`; });
    digits.forEach((d, i) => { const t0 = 0.3 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.5, 14, 7); unit.style.opacity = fadeIn(lt, 0.5, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.7, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.7, 1.2))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 1.0, 1.4)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — "หลานบอกว่า ไม่ต้องซื้อแล้วก็ได้นะตา": the granddaughter beside his chair; then the calendar, 14 circled in red
// =====================================================================
(() => {
  const [A, B] = SC.s5, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const m = homeScene(S), { set, yai, ta, rose } = m;
  const lan = new Puppet(set.people, LAN16, S.L.mid.defs);
  rose.at(0, 0, 0, false); set.notes(6);
  const tCal = L(P.D1) + 0.5;
  const shots = [
    { t: 0, cam: fA(600, 940, 1.6, 540, 1000), to: fA(605, 940, 1.66, 540, 1000) },
    { t: tCal, cam: fA(760, 520, 3.1, 540, 1100), to: fA(760, 520, 3.25, 540, 1100) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.4, minY: -1700 }));
    set.update(lt); set.notes(6);
    set.circle(prog(lt, tCal + 0.15, tCal + 0.9));
    const py = YAI_SIT(yai, lt, { smile: 0.3, head: 4 }); handsInLap(yai, py); m.yaiPose(py);
    const pl = standP(lan, 500, set.ground, 1.2, 1, { t: lt, smile: 0.35, head: 4, torso: 2, mouthO: talk(lt, L(P.D1), L(P.Dend)) });
    const [hx, hy] = torsoW(lan, pl, 60, -30); pl.aF = lan.reach(pl, hx + 10, hy + 10); lan.pose(pl);
    const pt = TA_SIT(ta, lt, { smile: 0.5, head: lt > L(P.D1) + 0.2 ? -14 : 2, eyes: 0.9 }); handsOnTable(ta, pt, TOPY, lt); ta.pose(pt);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — "แต่เช้าวันวาเลนไทน์ ตาก็ยังไปตลาด ซื้อกุหลาบมาหนึ่งดอก เหมือนทุกปี": the stall at dawn
// =====================================================================
(() => {
  const [A, B] = SC.s6, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const set = market16(S), D = S.L.mid.defs;
  const ta = new Puppet(set.people, TA16, D), ven = new Puppet(set.people, VENDOR16, D);
  const cane = cane16(set.top), rose = roseAt(set.top, 0.85, { wrap: true });
  const coins = svg('g', {}, set.top); for (const dx of [0, 14]) svg('ellipse', { cx: dx, cy: 0, rx: 9, ry: 4, fill: '#d8c070', stroke: INK, 'stroke-width': 2 }, coins);
  const chip = timeChip16(S.ui, 60, 130, '14 ก.พ. · 05:40', false);
  lightCast16(S, set, [set.people], [ta, ven], { light: { rim: '#ffd8a0', rimOp: 0.75 }, shadow: { op: 0.13, k: 0.12, blur: 11 } });
  const tTwo = L(P.E2) - 0.05;
  const shots = [
    { t: 0, cam: fA(560, 990, 1.15, 540, 1000), to: fA(570, 990, 1.18, 540, 1000) },
    { t: tTwo, cam: fA(560, 940, 2.0, 540, 1000), to: fA(560, 940, 2.08, 540, 1000) },
  ];
  const XW = lt => lerp(200, 420, ease.inOutSine(prog(lt, 0.1, tTwo - 0.15)));
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.5, minY: -300 }));
    set.update(lt);
    let p;
    if (lt < tTwo - 0.15) p = walkP(ta, XW(lt), set.ground, 1.2, 1, lt * 4.6, { amp: 9, t: lt, smile: 0.7, head: 4, lean: 6 });
    else p = standP(ta, 420, set.ground, 1.2, 1, { t: lt, smile: 0.95, head: 4, torso: 6 });
    // the cane in the back hand; the front hand takes the rose
    const [cbx, cby] = torsoW(ta, p, -10, -RIG.T + 120); p.aB = ta.reach(p, cbx + 30, cby + 30);
    const give = prog(lt, tTwo + 0.3, tTwo + 0.9), pay = prog(lt, tTwo + 1.2, tTwo + 1.6);
    const rx = lerp(688, 560, ease.inOutCubic(give)), ry = lerp(1086, 1040, give);
    if (give > 0.6) p.aF = ta.reach(p, lerp(rx - 6, 520, pay), lerp(ry + 6, 1050, pay)); else { const [hx, hy] = torsoW(ta, p, 40, -30); p.aF = ta.reach(p, hx, hy); }
    ta.pose(p);
    const [wbx, wby] = wristBW(ta, p); cane.setAttribute('transform', `translate(${wbx.toFixed(1)},${(wby - 4).toFixed(1)}) rotate(${(-6 + Math.sin(lt * 4.6) * 4 * (lt < tTwo ? 1 : 0)).toFixed(1)})`);
    const pv = standP(ven, 720, set.ground, 1.2, -1, { t: lt, smile: 0.95, grin: give > 0.5 ? 1 : 0, head: 6, torso: 8, mouthO: talk(lt, tTwo + 0.9, tTwo + 1.6) * 0.6 });
    if (give < 1) pv.aF = ven.reach(pv, rx + 10, ry + 6); else { const [hx, hy] = torsoW(ven, pv, 50, -30); pv.aF = ven.reach(pv, hx, hy); }
    ven.pose(pv);
    rose.at(give < 0.7 ? rx : lerp(rx, wristFW(ta, p)[0], pay), give < 0.7 ? ry : lerp(ry, wristFW(ta, p)[1] - 4, pay), -8, lt > 0.2);
    coins.setAttribute('transform', `translate(640,${set.counter - 2})`); coins.setAttribute('display', pay > 0.9 ? 'inline' : 'none');
    chip.update(lt, 0.2); chip.el.style.display = lt < tTwo ? 'flex' : 'none';
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 6);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — ตาบุญ: "สวัสดีครับ ผมชื่อบุญ เป็นแฟนคุณครับ" — he holds out the rose; she takes it, shy; for a moment the girl of
// 49 years ago smiles through her
// =====================================================================
(() => {
  const [A, B] = SC.s7, L = t => t - A;
  const S = new Shot(A, B, LAYERS()); S.grade = WARM;
  const m = homeScene(S), { set, yai, ta } = m;
  const ghostG = svg('g', { opacity: 0, filter: 'sepia(0.85)' }, set.top);
  const ghost = new Puppet(ghostG, YAI16_Y, S.L.mid.defs), gsk = sarong16(ghost, '#e8d8b8', { batik: '#c8a070', dot: '#fbf7ef' });
  const tCU = L(P.T2) - 0.05;
  const shots = [
    { t: 0, cam: fA(545, 960, 2.05, 540, 1000), to: fA(545, 960, 2.12, 540, 1000) },
    { t: tCU, cam: fA(380, 975, 2.25, 690, 1000), to: fA(380, 975, 2.34, 690, 1000) },
  ];
  S.update = lt => {
    applyCam(S, shotCamF(lt, shots, B - A, { handheld: 0.45, minY: -300 }));
    set.update(lt + 20); set.notes(6);
    const take = prog(lt, tCU + 0.2, tCU + 1.0);
    const r = offer(m, lt, prog(lt, 0.1, 0.9), take, { yai: { smile: lt > tCU ? 0.95 : 0.4, head: lt > tCU ? -6 : 4, eyes: lt > tCU + 1.0 ? 0.6 : 1 }, ta: { smile: 0.95, mouthO: talk(lt, L(P.T0), L(P.Tend)) } });
    const gk = Math.sin(Math.PI * prog(lt, tCU + 0.4, B - A + 0.3));
    ghostG.setAttribute('opacity', (0.38 * gk).toFixed(3));
    const pg = Object.assign({}, r.py, { smile: 1 }); ghost.pose(pg); gsk(pg);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — "ยายเปิดสมุดเล่มนั้น เจอกุหลาบ 49 ดอก กับลายมือตัวเองทุกหน้า" (the album: her hand, her pages) / ยาย: "คนคนนี้ คงรัก
// ฉันมากเลยนะคะ" (her close-up) / his face, in tears
// =====================================================================
(() => {
  const [A, B] = SC.s8, L = t => t - A, tIns = L(P.G1) - 0.25, tYai = L(P.Y0) - 0.15, tTa = L(P.Y1) + 1.3;
  // the two-shot (she opens it), then the close-ups after the insert
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = WARM;
  const m = homeScene(S), { set, yai, ta, rose, album } = m;
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(520, 990, 1.6, 540, 1010), to: fA(520, 990, 1.68, 540, 1010) }], tIns, { handheld: 0.45, minY: -300 }));
    set.update(lt + 30); set.notes(6);
    const py = YAI_SIT(yai, lt, { smile: 0.6, head: 14, torso: 10 }); const k = prog(lt, 0.2, 1.0);
    py.aF = yai.reach(py, lerp(470, 520, k), lerp(1080, TOPY - 14, k)); py.aB = yai.reach(py, 480, TOPY - 8); m.yaiPose(py);
    rose.at(452, 1100, 50, true);
    const pt = TA_SIT(ta, lt, { smile: 0.8, head: 10 }); handsOnTable(ta, pt, TOPY, lt); ta.pose(pt);
    album.setAttribute('transform', `translate(${TBL16.x},${TOPY + 6}) scale(1,${(1 + 0.4 * Math.sin(Math.PI * k * 0.5)).toFixed(3)})`);
  };
  SHOTS.push(S);
  const S2 = new Shot(A + tIns, A + tYai, LAYERS()); S2.grade = WARM;
  const Al = albumMacro16(S2), tGlow = L(P.G2) - tIns;
  S2.update = lt => {
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(540, 980, 1.02, 540, 960), to: fA(300, 900, 1.3, 540, 960) }], tYai - tIns, { handheld: 0.35, minY: -600 }), { dof: false });
    Al.update(lt);
    const u = prog(lt, 0.3, tGlow), flips = Math.floor(u * 6), turn = u > 0 && u < 1 ? (u * 6) % 1 : 0;
    Al.set({ year: 1 + flips * 8 > 49 ? 49 : 1 + flips * 8, turn, yai: { x: lerp(880, 320, Math.sin(Math.PI * turn) * 0.9), y: 1250 - Math.sin(Math.PI * turn) * 140 }, glowK: lt > tGlow ? 0.7 * Math.min(1, (lt - tGlow) / 0.4) : 0, t: lt });
  };
  SHOTS.push(S2);
  const S3 = new Shot(A + tYai, B, LAYERS()); S3.grade = WARM;
  const m3 = homeScene(S3);
  const tr = [tears(m3.set.top, 1613, { n: 3, drift: 1 }), tears(m3.set.top, 1614, { n: 3, drift: -1 })];
  const tr2 = [tears(m3.set.top, 1615, { n: 3, drift: -1 }), tears(m3.set.top, 1616, { n: 3, drift: 1 })];
  const shots3 = [
    { t: 0, cam: fA(380, 975, 2.25, 690, 1000), to: fA(380, 975, 2.34, 690, 1000) },
    { t: tTa - tYai, cam: fA(702, 975, 2.25, 400, 1000), to: fA(702, 975, 2.34, 400, 1000) },
  ];
  S3.update = lt => {
    const si = shotIx(lt, shots3), T = lt + tYai;
    applyCam(S3, shotCamF(lt, shots3, B - A - tYai, { handheld: 0.45, minY: -300 }));
    m3.set.update(lt + 40); m3.set.notes(6);
    const py = YAI_SIT(m3.yai, lt, { smile: 0.9, head: si === 0 ? lerp(14, -4, prog(lt, 0.2, 0.9)) : -4, torso: 6, mouthO: talk(T, L(P.Y0), L(P.Yend)), eyes: 0.85 });
    py.aF = m3.yai.reach(py, 520, TOPY - 14); py.aB = m3.yai.reach(py, 480, TOPY - 8); m3.yaiPose(py);
    m3.rose.at(452, 1100, 50, true);
    m3.album.setAttribute('transform', `translate(${TBL16.x},${TOPY + 6}) scale(1,1.4)`);
    const cry = prog(lt, 0.6, 1.2), [e1, e2] = eyesW(m3.yai, py); tr[0](e1[0], e1[1] + 6, cry * 0.7, lt); tr[1](e2[0], e2[1] + 6, cry * 0.7, lt);
    const pt = TA_SIT(m3.ta, lt, { smile: 0.75, head: 6, eyes: 0.8 }); handsOnTable(m3.ta, pt, TOPY, lt); m3.ta.pose(pt);
    const c2 = prog(lt, tTa - tYai, tTa - tYai + 0.4), [f1, f2] = eyesW(m3.ta, pt); tr2[0](f1[0], f1[1] + 6, c2, lt); tr2[1](f2[0], f2[1] + 6, c2, lt);
  };
  SHOTS.push(S3);
})();

// =====================================================================
// S9 — night: "เธอจำไม่ได้ ไม่เป็นไรนะ ฉันจำแทนเธอเอง" (he presses the 50th rose and writes) / "ความรักบางเรื่อง ไม่ต้องให้
// อีกคนจำได้ แค่เรายังจำได้ก็พอ" (the two chairs, his hand on hers, the camera rises to the moon in the window)
// =====================================================================
(() => {
  const [A, B] = SC.s9, L = t => t - A, tIns = 0.7, tWide = L(P.L0) - 0.35;
  const S = new Shot(A, A + tIns, LAYERS()); S.grade = NIGHT;
  const m = homeScene(S, { mode: 'night' }), blanket = svg('path', { fill: '#8a5a9a', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, m.set.top);
  const sleepYai = (mm, bl, lt) => { const py = YAI_SIT(mm.yai, lt, { smile: 0.5, head: 24, torso: -6, eyes: 0 }); handsInLap(mm.yai, py); mm.yaiPose(py); const [hx, hy] = torsoW(mm.yai, py, 0, -RIG.T + 30); bl.setAttribute('d', `M${(hx - 60).toFixed(1)},${(hy - 10).toFixed(1)} Q${(hx + 20).toFixed(1)},${(hy - 30).toFixed(1)} ${(hx + 110).toFixed(1)},${(hy + 40).toFixed(1)} L${(hx + 120).toFixed(1)},${(hy + 170).toFixed(1)} L${(hx - 60).toFixed(1)},${(hy + 170).toFixed(1)} Z`); return py; };
  S.update = lt => {
    applyCam(S, shotCamF(lt, [{ t: 0, cam: fA(560, 980, 1.5, 540, 1010), to: fA(560, 980, 1.55, 540, 1010) }], tIns, { handheld: 0.4, minY: -300 }));
    m.set.update(lt); m.set.notes(6);
    sleepYai(m, blanket, lt); m.rose.at(0, 0, 0, false);
    const pt = TA_SIT(m.ta, lt, { smile: 0.7, head: 14, torso: 10 }); handsOnTable(m.ta, pt, TOPY, lt); m.ta.pose(pt);
    m.album.setAttribute('transform', `translate(${TBL16.x},${TOPY + 6}) scale(1,1.4)`);
  };
  SHOTS.push(S);
  const S2 = new Shot(A + tIns, A + tWide, LAYERS()); S2.grade = NIGHT;
  const Al = albumMacro16(S2, { night: true });
  const tW0 = L(P.K0) - tIns, tW1 = L(P.Kend) - tIns;
  S2.update = lt => {
    applyCam(S2, shotCamF(lt, [{ t: 0, cam: fA(330, 980, 1.25, 540, 980), to: fA(330, 1000, 1.38, 540, 980) }], tWide - tIns, { handheld: 0.3, minY: -600 }), { dof: false });
    Al.update(lt);
    const kr = ease.inOutCubic(prog(lt, 0.0, 0.7)), placed = lt > 0.75 ? 1 : 0, w = prog(lt, tW0 + 0.3, tW1);
    const line = w < 0.5 ? 0 : 1, wx = 110 + 40 + (Al.W - 80) * ((w * 2) % 1), wy = Al.Y1 - 150 + line * 50;
    Al.set({ year: 50, ta: placed ? { x: wx + 130, y: wy + 110 } : { x: lerp(900, 360, kr), y: lerp(500, 1000, kr) }, rose: placed, write: w, t: lt });
  };
  SHOTS.push(S2);
  const S3 = new Shot(A + tWide, B, LAYERS()); S3.grade = NIGHT; S3.fadeIn = 0.4;
  const m3 = homeScene(S3, { mode: 'night' }), bl3 = svg('path', { fill: '#8a5a9a', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, m3.set.top);
  const hearts = heartsRise(m3.set.top, 540, 960, 0.6, 7, 1617, 0.36), leak = lightLeak(S3.fx);
  S3.update = lt => {
    const k = ease.inOutSine(prog(lt, 0.3, B - A - tWide));
    const c1 = frameAt(540, 990, 1.4, 540, 1010), c2 = frameAt(470, 760, 1.05, 540, 820);
    applyCam(S3, shotCamF(lt, [{ t: 0, cam: () => lerpCam(c1, c2, k), to: () => lerpCam(c1, c2, k) }], 9, { handheld: 0.3, minY: -300 }));
    m3.set.update(lt + 10); m3.set.notes(6);
    const py = sleepYai(m3, bl3, lt); m3.rose.at(0, 0, 0, false);
    const hk = ease.inOutCubic(prog(lt, 0.2, 1.0));   // his hand reaches over to hers
    const pt = TA_SIT(m3.ta, lt, { smile: 0.95, head: 10, torso: 4 + 8 * hk }); handsOnTable(m3.ta, pt, TOPY, lt);
    const [yx, yy] = torsoW(m3.yai, py, 50, -18); pt.aF = m3.ta.reach(pt, lerp(600, yx + 30, hk), lerp(TOPY - 10, yy + 8, hk)); m3.ta.pose(pt);
    m3.album.setAttribute('transform', `translate(${TBL16.x},${TOPY + 6})`);
    hearts(lt); leak(lt, 0.15 + 0.35 * k);
  };
  SHOTS.push(S3);
})();

// =====================================================================
// S10 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s10;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#a8586a'], [0.6, '#5a2234'], [1, '#2a0c18']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 1618, { color: '#ffc0c8', rMin: 10, rMax: 34, speed: 14, op: 0.22, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const back = behindSvg(S);
  const spark = burst(back, 540, 420, 0.3, 18, 1619, ['#ffd66b', '#ffffff', '#ffb0c0'], 240, 0.9);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const duo = html('div', 'title', wrap); duo.style.top = '270px';
  duo.innerHTML = `<span class="duo7">${av16('ta', 190)}</span><span class="duo7h">${roseIcon16(110)}</span><span class="duo7">${av16('yai', 190)}</span>`;
  Object.assign(duo.style, { display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '14px' });
  duo.querySelectorAll('.duo7 svg').forEach(s => { s.style.borderRadius = '50%'; s.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)'; });
  const t1 = html('div', 'title', wrap); t1.style.top = '590px'; t1.style.font = '700 180px/1 Kanit';
  const digits = ['5', '0'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'กุหลาบ'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '96px';
  const t2 = html('div', 'title', wrap, 'ที่ยายจำไม่ได้'); t2.style.top = '800px'; t2.style.font = '600 92px/1 Kanit'; t2.style.color = '#ffc4d0';
  const sub = html('div', 'title', wrap, 'เขาลืมได้… เราจำแทนเขาเอง'); sub.style.top = '950px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9ee';
  const cta = html('div', 'cta', wrap); cta.style.top = '1090px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่อยากรักกันไปจนแก่</span>`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.9, fl(SC.s3[0]) * 0.7, fl(SC.s4[0]), fl(SC.s6[0]) * 0.7, fl(SC.s9[0]) * 0.5, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = Promise.all(['400 40px Charm', '700 40px Charm', '400 40px Itim'].map(f => document.fonts.load(f, 'กขค 0123'))).then(() => document.fonts.ready).then(() => true);
