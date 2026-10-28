// "1,095 ข้อความของแม่" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D6; H is the "ถ้า..." hook).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

// scene windows and subtitle heights
const SC = { s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.A7 - 0.11], s1b: [P.A7 - 0.11, P.B0 - 0.08], s2: [P.B0 - 0.08, P.B4 - 0.07], s3: [P.B4 - 0.07, P.C0 - 0.08], s4: [P.C0 - 0.08, P.C8 - 0.05],
  s6: [P.C8 - 0.05, P.title], s7: [P.title, P.D0 - 0.07], s8: [P.D0 - 0.07, P.D3 - 0.06], s9: [P.D3 - 0.06, P.end], s10: [P.end, DURATION] };
const SUB_TOP = [[SC.s0[0], SC.s0[1], 1640], [SC.s1[0], SC.s1[1], 1660], [SC.s1b[0], SC.s1b[1], 1700], [SC.s2[0], SC.s2[1], 1620], [SC.s3[0], SC.s3[1], 1660], [SC.s4[0], SC.s4[1], 1590],
  [SC.s6[0], SC.s7[1], 1650], [SC.s8[0], SC.s8[1], 1590], [SC.s9[0], 99, 1730]];
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: (SUB_TOP.find(([a, b]) => c.a >= a - 0.3 && c.a < b) || [0, 0, 1600])[2] }));

const heartPath = (cx, cy, r) => `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`;
function cardEl(parent, cls, x, y, w) {
  const c = html('div', cls, parent);
  c.style.left = x + 'px'; c.style.top = y + 'px'; if (w) c.style.width = w + 'px';
  const sh = html('div', 'shine', c);
  return { c, sh };
}
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
const SHOTS = [];
const whip = (shot, lt, side) => {
  let k = 0, dx = 0;
  if (side === 'out') { k = clamp((lt - (shot.b - shot.a - 0.09)) / 0.09); dx = -ease.inCubic(k) * 520; }
  else { k = 1 - clamp(lt / 0.09); dx = ease.inCubic(k) * 520; }
  shot.root.style.transform = `translateX(${dx.toFixed(1)}px)`;
  return k;
};
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function earWorld(p) { return toWorld(p, ...torsoPt(p, EAR_L[0], EAR_L[1])); }
function phoneProp(parent, case_ = '#2a2b36') {
  const g = svg('g', {}, parent);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: case_, stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, g);
  return { g, scr };
}
const rectCenter = el => { const r = el.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2, r.width]; };
// both hands on a phone held in front of the chest (fx, fy in the torso frame)
function holdPhone(pup, pose, fx = 78, fy = -RIG.T + 36, tap = 0) {
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, fx, fy));
  pose.aB = pup.reach(pose, tx - 6, ty + 8);
  pose.aF = pup.reach(pose, tx + 6, ty - 2 + tap * 9);
  pose.propRot = -12;
}
const momAv = (n = 64) => portrait3('mom', n, '#fde2e8');
const dauAv = (n = 64) => portrait3('daughter', n, '#dbe7f3');

// =====================================================================
// S0 — hook: "ถ้าแม่ส่งรูปสวัสดีมาทุกเช้า แล้วคุณแค่ปัดทิ้ง ถ้าวันหนึ่งไม่มีข้อความมา เขาจะเป็นยังไง"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, [['sky', 0.08, 10], ['far', 0.3, 10], ['mid', 1, 10], ['fore', 1.7, 14]]);
  const set = porchDawn(S), L = t => t - A;
  for (const k of ['sky', 'far', 'mid']) S.L[k].el.style.filter = 'blur(10px) brightness(0.55) saturate(1.1)';
  const fxs = fxSvg(S);
  const bok = floaters(fxs, [0, 200, 1080, 1400], 14, 71, { color: '#ffd9a8', rMin: 12, rMax: 36, speed: 10, op: 0.2, base: 0.05, amp: 20 });
  // mom's morning stickers arrive as banners… and get swiped away
  const bans = [[260, 1, L(P.H1) - 0.05, L(P.H4) - 0.15], [470, 2, L(P.H1) + 0.35, L(P.H4) + 0.05], [680, 3, L(P.H2) + 0.2, L(P.H4) + 0.25]]
    .map(([y, d, tin, tsw]) => ({ b: notifBanner(S.ui, y, momAv(96), 'แม่', `ส่งสติกเกอร์<span class="mini">${stickerSVG(d, 64)}</span>`), tin, tsw }));
  // …then one morning nothing comes: Mom under a spotlight, an empty sticker slot, a question mark
  const spot = html('div', 'spot', S.ui);
  const momB = html('div', 'title', S.ui); momB.style.top = '330px'; momB.innerHTML = portrait3('mom', 320, '#fde2e8');
  const msvg = momB.querySelector('svg'); msvg.style.borderRadius = '50%'; msvg.style.boxShadow = '0 0 0 10px #fff, 0 30px 60px rgba(0,0,0,.5)';
  const ghost = html('div', 'cghost', S.ui);
  Object.assign(ghost.style, { position: 'absolute', left: '120px', top: '720px', width: '230px', height: '230px', background: 'rgba(255,255,255,.12)', borderColor: '#e8eef2', color: '#f4f6f8' });
  ghost.innerHTML = `<svg width="84" height="84" viewBox="-50 -50 100 100">${[0, 1, 2, 3, 4, 5].map(k => `<ellipse cx="${(Math.cos(k * 1.047) * 24).toFixed(1)}" cy="${(Math.sin(k * 1.047) * 24).toFixed(1)}" rx="20" ry="14" transform="rotate(${k * 60} ${(Math.cos(k * 1.047) * 24).toFixed(1)} ${(Math.sin(k * 1.047) * 24).toFixed(1)})" fill="none" stroke="#e8eef2" stroke-width="4" stroke-dasharray="6 6"/>`).join('')}<circle r="10" fill="none" stroke="#e8eef2" stroke-width="4"/></svg><small style="font-size:28px">วันนี้<br>ไม่มีดอกไม้</small>`;
  const qw = html('div', 'qwrap', S.ui); qw.style.left = '700px'; qw.style.top = '300px'; html('div', 'qmark', qw, '?');
  const rip = ripples(fxs, 540, 490, 170, '#ffe2a8', 3, 1.4);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.14, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    set.update(lt); bok(lt);
    bans.forEach(({ b, tin, tsw }) => b.update(lt, tin, tsw));
    spot.style.opacity = (0.9 * prog(lt, L(P.H5) - 0.1, L(P.H5) + 0.3)).toFixed(3);
    popSquash(momB, lt, L(P.H5) + 0.05, '', -12); momB.style.opacity = fadeIn(lt, L(P.H5) + 0.05, 0.12);
    popSquash(ghost, lt, L(P.H6) - 0.05, `rotate(${(-6 + Math.sin(lt * 2) * 2).toFixed(1)}deg)`, -10); ghost.style.opacity = (0.95 * fadeIn(lt, L(P.H6) - 0.05, 0.12)).toFixed(3);
    popSquash(qw, lt, L(P.H7) - 0.05, `rotate(${(Math.sin(lt * 5) * 8).toFixed(1)}deg)`, 20); qw.style.opacity = fadeIn(lt, L(P.H7) - 0.05, 0.1);
    rip(lt, prog(lt, L(P.H6), L(P.H6) + 0.3));
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — dawn on Mom's porch: 06:00, a Monday flower sticker, "ขอให้ลูกสุขสบาย", 3 years without a miss
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['sky', 0.08, 0], ['far', 0.3, 1.5], ['mid', 1, 0], ['fore', 1.7, 10]]);
  S.grade = 'saturate(1.08) contrast(1.03)';
  const set = porchDawn(S);
  const L = t => t - A;
  const mom = new Puppet(set.people, MOM, S.L.mid.defs);
  const ph = phoneProp(mom.prop, '#c4566f');
  const clock = sunriseClock(S.ui, 56, 110);
  const chat = chatPhone(S.ui, 610, 190, 410, 640, 'ลูก', dauAv());
  const st = chat.add('sticker', 'R', L(P.A2) + 0.6, { day: 1, meta: 'อ่านแล้ว', read: L(P.A6) + 0.4 });
  chat.add('text', 'R', L(P.A5) + 0.05, { text: 'ขอให้ลูกสุขสบายนะจ๊ะ' });
  const streak = streakChip(S.ui, 56, 300);
  const fxs = fxSvg(S);
  const spark = burst(fxs, 815, 430, L(P.A4) + 0.05, 18, 31, ['#ffd66b', '#ffffff', '#f2c230'], 220, 0.9);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-30, 10, k), y: 0, z: lerp(1.0, 1.07, k), fx: 600, fy: 1100 });
    set.update(lt);
    const happy = lt > L(P.A4);
    const pose = { x: 640, y: 1226, s: 1.25, f: 1, torso: 8 + Math.sin(lt * 1.5), head: 14, lF: [-2, 88], lB: [2, 90], t: lt + 1, smile: happy ? 0.95 : 0.6, grin: happy && lt < L(P.A4) + 1.4 ? 1 : 0 };
    const tap = lt > L(P.A2) + 0.4 && lt < L(P.A2) + 0.58 ? 1 : 0;
    holdPhone(mom, pose, 80, -RIG.T + 34, tap);
    mom.pose(pose);
    ph.scr.setAttribute('fill', lt > L(P.A2) ? '#ffe9c4' : '#d8e8ff');
    clock.update(lt, 0.1, L(P.A1) + 0.1);
    enter3d(chat.el, lt, L(P.A2) - 0.15, 'pop');
    chat.update(lt);
    const bump = Math.exp(-Math.pow((lt - L(P.A4) - 0.25) * 5, 2));
    st.el.style.transform = `scale(${(1 + 0.14 * bump).toFixed(3)}) rotate(${(Math.sin(lt * 3) * 2 * (lt > L(P.A4) ? 1 : 0)).toFixed(2)}deg)`;
    spark(lt);
    streak.update(lt, L(P.A6) + 0.05);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1b — three years of stickers scroll by: 1,095 ข้อความ
// =====================================================================
(() => {
  const [A, B] = SC.s1b;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  const G = S.L.bg, L = t => t - A;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: lin(G.defs, [[0, '#3b4380'], [0.5, '#b8678a'], [1, '#ffb48a']]) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 61, { color: '#fff1d6', rMin: 10, rMax: 34, speed: 16, op: 0.25, base: 0.05, amp: 26, filter: blurFilter(G.defs, 4) });
  const chat = chatPhone(S.ui, 230, 560, 620, 1160, 'ลูก', dauAv());
  for (let i = 0; i < 26; i++) chat.add('sticker', 'R', 0.05 + i * 0.13, { day: (i + 1) % 7, size: 220, meta: 'อ่านแล้ว' });
  const cnt = bigCounter(S.ui, 130);
  S.update = lt => {
    bok(lt);
    enter3d(chat.el, lt, 0.0, 'pop');
    chat.update(lt);
    cnt.update(lt, L(P.A7) + 0.1, L(P.A8) + 1.5);
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 12);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — the daughter's office at night: reads, swipes away, mutes, sighs
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.05) contrast(1.05)';
  const set = officeNight(S);
  const M = S.L.mid, L = t => t - A;
  const deskPh = svg('g', { transform: 'translate(600,1170)' }, set.top);
  svg('rect', { x: -40, y: -10, width: 80, height: 14, rx: 6, fill: '#2a2b36', stroke: INK, 'stroke-width': 3.5 }, deskPh);
  const deskGlow = svg('ellipse', { cx: 0, cy: -10, rx: 60, ry: 20, fill: '#bfe6ff', opacity: 0 }, deskPh);
  const dau = new Puppet(set.people, DAUGHTER, M.defs);
  const ph = phoneProp(dau.prop);
  const ban = notifBanner(S.ui, 120, momAv(96), 'แม่', `ส่งสติกเกอร์<span class="mini">${stickerSVG(2, 64)}</span>`);
  const read = html('div', 'readchip', S.ui); read.style.left = '330px'; read.style.top = '400px';
  read.innerHTML = '<svg width="44" height="30" viewBox="0 0 44 30"><path d="M3,16 L11,24 L25,6 M17,22 L19,24 L39,4" stroke="#2f9e5b" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>อ่านแล้ว';
  const mute = muteToggle(S.ui, 300, 380);
  const fxs = fxSvg(S);
  const anger = angerMark(fxs);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-20, 10, k), y: 40, z: lerp(1.15, 1.22, k), fx: 420, fy: 1100 });
    set.update(lt);
    const look = ease.inOutSine(prog(lt, L(P.B0) - 0.35, L(P.B0) + 0.1)) * (1 - ease.inOutSine(prog(lt, L(P.B3) + 0.3, L(P.B3) + 0.7)));
    const annoyed = lt > L(P.B3);
    const pose = { x: 250, y: 1192, s: 1.2, f: 1, torso: 6, head: lerp(12, -4, look), lF: [-4, 86], lB: [2, 90], t: lt + 2, smile: annoyed ? 0.05 : 0.3, angry: annoyed };
    const typ = look < 0.5 ? Math.sin(lt * 18) * 5 : 0;
    const aKey = dau.reach(pose, 470 + typ, 1160);
    const [px, py] = toWorld(pose, ...torsoPt(pose, 74, -RIG.T + 26));
    const aPh = dau.reach(pose, px, py);
    pose.aF = [lerp(aKey[0], aPh[0], look), lerp(aKey[1], aPh[1], look)];
    pose.aB = dau.reach(pose, 440 - typ, 1162);
    pose.propRot = -14;
    dau.pose(pose);
    ph.g.setAttribute('opacity', look > 0.5 ? 1 : 0);
    deskPh.setAttribute('opacity', look > 0.5 ? 0 : 1);
    deskGlow.setAttribute('opacity', lt > L(P.B0) - 0.5 && lt < L(P.B0) ? (0.5 + 0.5 * Math.sin(lt * 30)).toFixed(2) : 0);
    deskPh.setAttribute('transform', `translate(600,1170) rotate(${lt > L(P.B0) - 0.5 && lt < L(P.B0) - 0.1 ? (Math.sin(lt * 80) * 3).toFixed(1) : 0})`);
    ph.scr.setAttribute('fill', '#e9f4ff');
    ban.update(lt, L(P.B0) - 0.4, L(P.B1) + 0.35);
    popSquash(read, lt, L(P.B0) + 0.85);
    read.style.opacity = (parseFloat(read.style.opacity || 0) * (1 - prog(lt, L(P.B2) - 0.4, L(P.B2) - 0.1))).toFixed(3);
    mute.update(lt, L(P.B2) - 0.05, L(P.B2) + 0.85);
    mute.c.c.style.opacity = (parseFloat(mute.c.c.style.opacity || 0) * (1 - prog(lt, L(P.B3) + 1.0, L(P.B3) + 1.3))).toFixed(3);
    const [hx, hy] = rectCenter(dau.head);
    anger(lt, L(P.B3) + 0.05, hx + 70, hy - 70);
    const out = whip(S, lt, 'out');
    setGrade(S, (1 - prog(lt, 0, 0.25)) * 10 + out * 18);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — "แม่ใช้นิ้วเดียว ค่อยๆ จิ้ม": Mom types with one finger, big font, then sends
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['sky', 0.08, 0], ['far', 0.3, 3], ['mid', 1, 0], ['fore', 1.7, 10]]);
  S.grade = 'saturate(1.1) contrast(1.03)';
  const set = porchDawn(S);
  const L = t => t - A;
  const mom = new Puppet(set.people, MOM, S.L.mid.defs);
  const ph = phoneProp(mom.prop, '#c4566f');
  const card = typingCard(S.ui, 216, 130, 'สวัสดีจ้ะลูก');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: 40, y: lerp(150, 170, k), z: lerp(1.55, 1.65, k), fx: 640, fy: 1000 });
    set.update(lt + 14);
    const typing = lt > L(P.B5) && lt < L(P.B7) + 0.7;
    const pose = { x: 640, y: 1226, s: 1.25, f: 1, torso: 12, head: 22, lF: [-2, 88], lB: [2, 90], t: lt + 4, smile: 0.7, eyes: typing ? 0.6 : null };
    holdPhone(mom, pose, 72, -RIG.T + 52, typing ? Math.max(0, Math.sin(lt * 7)) : 0);
    mom.pose(pose);
    ph.scr.setAttribute('fill', '#ffe9c4');
    card.update(lt, L(P.B4) - 0.05, L(P.B5) + 0.25, L(P.B7) - 0.05, L(P.B7) + 0.55);
    const inK = whip(S, lt, 'in');
    setGrade(S, inK * 14 + (1 - prog(lt, B - A - 0.35, B - A)) * 0);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — one morning: 6, 7, 8 o'clock, no flowers, the silence, she calls
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  const set = bedroomMorning(S);
  const M = S.L.mid, L = t => t - A;
  const dau = new Puppet(set.people, DAUGHTER_HOME, M.defs);
  const ph = phoneProp(dau.prop, '#e8869f');
  const SDS = 1.2;
  set.blanket(300, 300 + RIG.THIGH * SDS);
  const clock = flipClock(S.ui, 56, 120);
  const chat = chatPhone(S.ui, 610, 300, 410, 640, 'แม่', momAv());
  chat.add('sticker', 'L', -1, { day: 2, meta: 'เมื่อวาน' });
  chat.add('ghost', 'L', L(P.C4) - 0.1, { text: 'วันนี้<br>ไม่มีดอกไม้' });
  const scr = callScreen(S.ui, 560, 110);
  scr.el.querySelector('.callav').innerHTML = portrait3('mom', 220, '#fde2e8');
  scr.el.querySelector('.callname').textContent = 'แม่';
  const fxs = fxSvg(S);
  const vg = svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(S.L.mid.defs, [[0, '#000', 0], [0.55, '#000', 0.1], [1, '#0a0614', 0.85]]), opacity: 0 }, fxs);
  const tWake = L(P.C0) + 0.5, tCall = L(P.C6) + 0.25, tEar = L(P.C6) + 1.0;
  S.update = lt => {
    const worry = ease.inOutSine(prog(lt, L(P.C5) - 0.2, L(P.C5) + 0.6));
    const push = ease.inOutSine(prog(lt, L(P.C5) - 0.3, L(P.C5) + 1.2));
    S.cam({ x: lerp(0, -40, push), y: lerp(20, 80, push), z: lerp(1.12, 1.45, push) + 0.03 * prog(lt, 0, B - A), fx: 400, fy: 1000 });
    let hh = 6; [L(P.C1), L(P.C2), L(P.C3)].forEach((t0, i) => { if (lt >= t0) hh = 6 + i; });
    set.update(lt, hh, 0);
    const wake = ease.inOutSine(prog(lt, tWake - 0.3, tWake + 0.5));
    const ear = ease.inOutSine(prog(lt, tEar - 0.3, tEar + 0.2));
    const pose = { x: 300, y: 1150, s: SDS, f: 1, torso: lerp(-6, 4, wake) + worry * 6, head: lerp(18, 12, wake) - worry * 4, lF: [0, 0], lB: [2, 2], t: lt + 3, smile: lerp(0.4, 0.35, wake) - worry * 0.4, eyes: wake < 0.5 ? 0 : null };
    holdPhone(dau, pose, lerp(40, 80, wake), -RIG.T + lerp(80, 34, wake));
    if (ear > 0) {
      pose.armF = lerp(1, 0.85, ear);
      const [ex, ey] = earWorld(pose); const toE = dau.reach(pose, ex + 8, ey + 16, true);
      pose.aF = [lerp(pose.aF[0], toE[0], ear), lerp(pose.aF[1], toE[1], ear)];
      pose.aB = [lerp(pose.aB[0], 95, ear), lerp(pose.aB[1], 70, ear)];
      pose.propRot = lerp(-12, -20, ear);
    }
    dau.pose(pose);
    ph.scr.setAttribute('fill', lt > L(P.C5) ? '#9aa6b8' : '#e9f4ff');
    clock.update(lt, L(P.C1) - 0.3, [L(P.C1), L(P.C2), L(P.C3)]);
    enter3d(chat.el, lt, tWake + 0.2, 'pop');
    chat.update(lt);
    chat.el.style.opacity = (parseFloat(chat.el.style.opacity || 0) * (1 - prog(lt, L(P.C6) - 0.3, L(P.C6)))).toFixed(3);
    chat.el.style.filter = `brightness(${(1 - 0.35 * worry).toFixed(3)})`;
    clock.c.c.style.opacity = (parseFloat(clock.c.c.style.opacity || 0) * (1 - prog(lt, L(P.C5) + 0.8, L(P.C5) + 1.2))).toFixed(3);
    scr.update(lt, L(P.C6) - 0.2, tCall);
    scr.el.style.opacity = (parseFloat(scr.el.style.opacity || 0) * (1 - prog(lt, tEar + 0.1, tEar + 0.4))).toFixed(3);
    const beat = Math.pow(Math.max(0, Math.sin(lt * 7.5)), 6);
    vg.setAttribute('opacity', (worry * (0.55 + 0.25 * beat) * (1 - 0.6 * prog(lt, L(P.C6), L(P.C6) + 0.6))).toFixed(3));
    S.grade = `saturate(${(1.05 - 0.5 * worry).toFixed(3)}) contrast(1.03)`;
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — Mom on her floor mattress, sick, phone on the pillow: "แม่แค่ไม่สบาย ไม่ต้องห่วงนะลูก"
// =====================================================================
function lyingMom(room, defs, X, Y, s) {
  const lie = svg('g', { transform: `translate(${X},${Y}) rotate(-90)` }, room.people);
  const mom = new Puppet(lie, MOM, defs);
  const hx = X - (RIG.T + RIG.NECK + RIG.R * 0.84) * s, hy = Y - 4 * s;
  svg('path', { d: `M${X - 126 * s},${Y - 30} Q${X - 70 * s},${Y - 72} ${X + 40 * s},${Y - 62} Q${X + 200 * s},${Y - 58} ${X + 236 * s},${Y - 14} L${X + 240 * s},${Y + 48} L${X - 134 * s},${Y + 48} Z`, fill: lin(defs, [[0, '#8fb8de'], [1, '#6f9cc6']]), stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, room.top);
  for (let k = 0; k < 6; k++) svg('path', { d: `M${X - 90 * s + k * 60},${Y - 40} q10,40 0,80`, stroke: '#ffffff', 'stroke-width': 3, opacity: 0.35, fill: 'none' }, room.top);
  svg('rect', { x: hx - 62, y: hy - 66, width: 76, height: 28, rx: 10, fill: '#ffffff', stroke: INK, 'stroke-width': 4, transform: `rotate(-38 ${hx - 24} ${hy - 52})` }, room.top);   // wet towel
  const phone = svg('g', { transform: `translate(${hx - 120},${hy + 34}) rotate(-8)` }, room.top);
  svg('rect', { x: -34, y: -18, width: 68, height: 36, rx: 8, fill: '#c4566f', stroke: INK, 'stroke-width': 3.5 }, phone);
  const scr = svg('rect', { x: -28, y: -13, width: 56, height: 26, rx: 4, fill: '#3a3d4c' }, phone);
  const waves = [0, 1, 2].map(i => svg('path', { d: `M${-10 - i * 14},${-30 - i * 12} q${20 + i * 14},${-16 - i * 6} ${40 + i * 28},0`, fill: 'none', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0 }, phone));
  return { mom, hx, hy, scr, waves, phone };
}
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.4, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(0.92) contrast(1.03) brightness(0.97)';
  const room = momRoom(S);
  const L = t => t - A;
  const lm = lyingMom(room, S.L.mid.defs, 406, 1332, 1.1);
  const pill = html('div', 'chip big', S.ui); pill.style.left = '330px'; pill.style.top = '110px';
  pill.innerHTML = `<span style="display:inline-block;width:56px;height:56px;border-radius:50%;overflow:hidden">${dauAv(56)}</span><span>สายจากลูก <b class="ctime" style="color:#2f9e5b">00:01</b></span>`;
  const ct = pill.querySelector('.ctime');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-230, -250, k), y: lerp(40, 60, k), z: lerp(1.4, 1.5, k), fx: 380, fy: 1300 });
    room.update(lt + 3);
    const talk = (lt > L(P.C8) && lt < L(P.C8) + 1.2) || (lt > L(P.C9) && lt < L(P.C9) + 1.1);
    lm.mom.pose({ x: 0, y: 0, s: 1.1, f: 1, torso: 0, head: -8, lF: [90, 90], lB: [90, 90], aF: [80, 80], aB: [96, 90], eyes: 0, smile: lt > L(P.C9) ? 0.55 : 0.15, t: lt });
    lm.waves.forEach((w, i) => w.setAttribute('opacity', talk ? (0.4 + 0.6 * Math.max(0, Math.sin(lt * 8 - i))).toFixed(2) : 0.15));
    lm.scr.setAttribute('fill', '#9be38b');
    popSquash(pill, lt, 0.1);
    ct.textContent = '00:' + String(Math.floor(3 + lt)).padStart(2, '0');
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 10 + ease.inCubic(prog(lt, B - A - 0.3, B - A)) * 12);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — title: 1,095 ข้อความ / ของแม่
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = momRoom(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.42) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 93, { color: '#ffd9a0', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '400px';
  ic.innerHTML = stickerSVG(3, 210);
  const t1 = html('div', 'title', wrap); t1.style.top = '690px'; t1.style.font = '700 150px/1 Kanit';
  const digits = ['1', ',', '0', '9', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ข้อความ'); unit.style.marginLeft = '0.25em'; unit.style.fontSize = '96px';
  const t2 = html('div', 'title', wrap, 'ของแม่'); t2.style.top = '880px'; t2.style.font = '600 130px/1 Kanit';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1066px', width: '200px', height: '8px', borderRadius: '4px', background: '#f06aa0', boxShadow: '0 0 16px rgba(240,106,160,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5);
    bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.5, 14, 7); unit.style.opacity = fadeIn(lt, 0.5, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.6, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.6, 1.05))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.85, 1.25)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — "ข้อความที่เราว่าน่ารำคาญ คือหลักฐาน ว่ายังมีคนคิดถึง": scrolling back, bell = heart, notifications back on
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.02) contrast(1.03) sepia(0.05)';
  const set = bedroomMorning(S);
  const M = S.L.mid, L = t => t - A;
  const dau = new Puppet(set.people, DAUGHTER_HOME, M.defs);
  const ph = phoneProp(dau.prop, '#e8869f');
  set.blanket(300, 300 + RIG.THIGH * 1.2);
  const eq = bellEqHeart(S.ui, 90, 120, 836);
  const mute = muteToggle(S.ui, 56, 470);
  const chat = chatPhone(S.ui, 610, 660, 410, 620, 'แม่', momAv());
  for (let i = 0; i < 12; i++) chat.add('sticker', 'L', -1, { day: (i + 4) % 7, size: 190, meta: 'อ่านแล้ว' });
  const fxs = fxSvg(S);
  const tear = svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#cfe8ff', stroke: '#fff', 'stroke-width': 1.5, opacity: 0 }, fxs);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-10, 10, k), y: 30, z: lerp(1.12, 1.18, k), fx: 400, fy: 1050 });
    set.update(lt, 8, 30);
    const soft = ease.inOutSine(prog(lt, L(P.D2) - 0.2, L(P.D2) + 0.5));
    const pose = { x: 300, y: 1150, s: 1.2, f: 1, torso: 8, head: 14, lF: [0, 0], lB: [2, 2], t: lt + 5, smile: lerp(0.1, 0.6, soft) };
    holdPhone(dau, pose, 80, -RIG.T + 36, lt > L(P.D2) + 0.5 && lt < L(P.D2) + 0.7 ? 1 : 0);
    dau.pose(pose);
    ph.scr.setAttribute('fill', '#ffe9c4');
    eq.update(lt, L(P.D0) - 0.05, L(P.D2) + 0.05);
    mute.update(lt, L(P.D1) - 0.2, L(P.D1) - 1, L(P.D2) + 0.6);
    enter3d(chat.el, lt, 0.05, 'pop');
    chat.update(lt, -Math.min(lt, B - A - 0.8) * 160);
    const [gx, gy] = rectCenter(dau.eyeG);
    const td = prog(lt, L(P.D1) - 0.2, L(P.D1) + 1.6);
    tear.setAttribute('opacity', td > 0 && td < 1 ? (0.95 * (1 - td * 0.5)).toFixed(3) : 0);
    tear.setAttribute('transform', `translate(${(gx - 4).toFixed(1)},${(gy + 16 + 60 * ease.inCubic(td)).toFixed(1)}) scale(1.6)`);
    setGrade(S, (1 - prog(lt, 0, 0.35)) * 12);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S9 — split screen: the daughter replies with a Wednesday sticker; Mom's phone lights up, she smiles
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const L = t => t - A;
  const tSend = L(P.D4) + 0.25, tArrive = tSend + 0.55;
  // top: daughter in bed
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  S.root.style.clipPath = 'inset(0 0 50% 0)';
  S.grade = 'saturate(1.06) contrast(1.03)';
  const set = bedroomMorning(S);
  const dau = new Puppet(set.people, DAUGHTER_HOME, S.L.mid.defs);
  const ph = phoneProp(dau.prop, '#e8869f');
  set.blanket(300, 300 + RIG.THIGH * 1.2);
  const chat = chatPhone(S.ui, 610, 60, 410, 860, 'แม่', momAv());
  chat.add('ghost', 'L', -1, { text: 'วันนี้<br>ไม่มีดอกไม้' });
  chat.add('text', 'R', L(P.D3) + 0.1, { text: 'หายไวๆ นะคะแม่ รักแม่นะ', meta: 'ส่งแล้ว', read: tArrive + 0.6 });
  chat.add('sticker', 'R', tSend, { day: 3, size: 200, meta: 'อ่านแล้ว', read: tArrive + 0.9 });
  S.update = lt => {
    S.cam({ x: -20, y: 470, z: 1.0 + 0.04 * prog(lt, 0, B - A), fx: 400, fy: 1000 });
    set.update(lt, 8, 45);
    const pose = { x: 300, y: 1150, s: 1.2, f: 1, torso: 6, head: 12, lF: [0, 0], lB: [2, 2], t: lt + 7, smile: 0.85 };
    holdPhone(dau, pose, 80, -RIG.T + 36, (lt > L(P.D3) && lt < tSend) ? Math.max(0, Math.sin(lt * 14)) : (lt > tSend - 0.1 && lt < tSend + 0.1 ? 1 : 0));
    dau.pose(pose);
    ph.scr.setAttribute('fill', '#ffe9c4');
    chat.update(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 10);
  };
  SHOTS.push(S);
  // bottom: Mom on the mattress
  const S2 = new Shot(A, B, [['far', 0.4, 1.5], ['mid', 1, 0]]);
  S2.root.style.clipPath = 'inset(50% 0 0 0)';
  S2.grade = 'saturate(1.04) contrast(1.03)';
  const room = momRoom(S2);
  const lm = lyingMom(room, S2.L.mid.defs, 406, 1332, 1.1);
  const ban = html('div', 'notif', S2.ui); ban.style.top = '1010px';
  ban.innerHTML = `<div class="app">แชท</div><div class="av">${dauAv(96)}</div><div style="flex:1"><div class="who">ลูก<small>ตอนนี้</small></div><div class="msg">ส่งสติกเกอร์<span class="mini">${stickerSVG(3, 64)}</span></div></div>`;
  const fx2 = fxSvg(S2);
  const hearts = heartsRise(fx2, 480, 1400, tArrive + 0.9, 10, 57, 0.28);
  const tear = svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#cfe8ff', stroke: '#fff', 'stroke-width': 1.5, opacity: 0 }, fx2);
  const leak = lightLeak(S2.fx);
  S2.update = lt => {
    S2.cam({ x: -230, y: -40, z: 1.18 + 0.04 * prog(lt, 0, B - A), fx: 380, fy: 1300 });
    room.update(lt + 6);
    const woke = lt > tArrive + 0.3;
    lm.mom.pose({ x: 0, y: 0, s: 1.1, f: 1, torso: 0, head: woke ? -14 : -8, lF: [90, 90], lB: [90, 90], aF: [80, 80], aB: [96, 90], eyes: woke ? null : 0, smile: woke ? 1 : 0.3, t: lt + 3 });
    const ring = lt > tArrive && lt < tArrive + 0.8;
    lm.scr.setAttribute('fill', lt > tArrive ? '#ffe9c4' : '#3a3d4c');
    lm.phone.setAttribute('transform', `translate(${lm.hx - 120},${lm.hy + 34}) rotate(${(-8 + (ring ? Math.sin(lt * 70) * 4 : 0)).toFixed(1)})`);
    lm.waves.forEach(w => w.setAttribute('opacity', 0));
    const kb = spring(lt, tArrive, 13, 6);
    ban.style.opacity = (fadeIn(lt, tArrive, 0.12) * (1 - prog(lt, L(P.D6) + 0.4, L(P.D6) + 0.8))).toFixed(3);
    ban.style.transform = `translateY(${((1 - kb) * -120).toFixed(1)}px)`;
    hearts(lt);
    const [gx, gy] = rectCenter(lm.mom.eyeG);
    const td = prog(lt, L(P.D5) - 0.2, L(P.D5) + 1.4);
    tear.setAttribute('opacity', td > 0 && td < 1 ? (0.95 * (1 - td * 0.5)).toFixed(3) : 0);
    tear.setAttribute('transform', `translate(${(gx + 10 + 40 * ease.inCubic(td)).toFixed(1)},${(gy + 6).toFixed(1)}) scale(1.6)`);
    leak(lt, 0.2 + 0.4 * prog(lt, tArrive, tArrive + 1.5));
    setGrade(S2, (1 - prog(lt, 0, 0.3)) * 10);
  };
  SHOTS.push(S2);
  // the sticker flies down across the seam
  const S3 = new Shot(A, B, []);
  const seam = html('div', '', S3.ui); Object.assign(seam.style, { position: 'absolute', left: 0, right: 0, top: '954px', height: '12px', background: 'linear-gradient(90deg,#ffd66b,#f06aa0,#ffd66b)', boxShadow: '0 0 24px rgba(255,214,107,.8)' });
  const fly = html('div', '', S3.ui); fly.style.cssText = 'position:absolute;left:0;top:0'; fly.innerHTML = stickerSVG(3, 150);
  const trail = fxSvg(S3);
  const sparks = Array.from({ length: 10 }, () => svg('circle', { r: 5, fill: '#fff6d0', opacity: 0 }, trail));
  S3.update = lt => {
    const q = prog(lt, tSend + 0.05, tArrive), e = ease.inOutSine(q);
    const x = lerp(760, 360, e), y = lerp(560, 1290, e) - Math.sin(Math.PI * e) * 160;
    fly.style.opacity = q > 0 && q < 1 ? 1 : 0;
    fly.style.transform = `translate(${(x - 75).toFixed(1)}px,${(y - 75).toFixed(1)}px) rotate(${(e * 360).toFixed(1)}deg) scale(${(0.6 + 0.4 * Math.sin(Math.PI * e)).toFixed(3)})`;
    sparks.forEach((sp, i) => { const qq = clamp(q - i * 0.05); const ee = ease.inOutSine(qq); setA(sp, { cx: lerp(760, 360, ee).toFixed(1), cy: (lerp(560, 1290, ee) - Math.sin(Math.PI * ee) * 160).toFixed(1), opacity: q > 0 && q < 1.2 && qq > 0 ? (0.8 * (1 - i / 10)).toFixed(2) : 0 }); });
    seam.style.opacity = (0.75 + 0.25 * Math.sin(lt * 5)).toFixed(3);
  };
  SHOTS.push(S3);
})();

// =====================================================================
// S10 — end card: Wednesday sticker, title, "ตอบแม่วันนี้ สักคำก็ยังดี", CTA
// =====================================================================
(() => {
  const [A, B] = SC.s10;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#7a3f62'], [0.6, '#36203d'], [1, '#1a1020']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 143, { color: '#ffd9e6', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const fxs = fxSvg(S);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const icon = html('div', 'title', wrap); icon.style.top = '330px'; icon.innerHTML = stickerSVG(3, 260);
  const t1 = html('div', 'title', wrap); t1.style.top = '660px'; t1.style.font = '700 140px/1 Kanit';
  const digits = ['1', ',', '0', '9', '5'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ข้อความ'); unit.style.marginLeft = '0.25em'; unit.style.fontSize = '90px';
  const t2 = html('div', 'title', wrap, 'ของแม่'); t2.style.top = '830px'; t2.style.font = '600 120px/1 Kanit';
  const sub = html('div', 'title', wrap, 'ตอบแม่วันนี้ สักคำก็ยังดี'); sub.style.top = '1010px'; sub.style.font = '500 52px/1.3 Kanit'; sub.style.color = '#ffd166';
  const cta = html('div', 'cta', wrap); cta.style.top = '1140px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่ยังไม่เคยตอบแม่</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  const spark = burst(fxs, 540, 460, 0.3, 18, 153, ['#ffd66b', '#ffffff', '#5cbf6a'], 240, 0.9);
  S.update = lt => {
    bok(lt); leak(lt, 0.45);
    popSquash(icon, lt, 0.15, `rotate(${(Math.sin(lt * 2.4) * 5).toFixed(2)}deg)`, -20);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.75, 14, 7); unit.style.opacity = fadeIn(lt, 0.75, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.85, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.85, 1.3))) * 100).toFixed(1)}% -40% 0)`;
    const ks = spring(lt, 1.15, 14, 7); sub.style.opacity = fadeIn(lt, 1.15, 0.15); sub.style.transform = `translateY(${((1 - ks) * 24).toFixed(1)}px)`;
    enter3d(cta, lt, 1.45, 'pop');
    cta.style.boxShadow = `0 0 ${(24 + 18 * Math.sin(lt * 4)).toFixed(1)}px rgba(224,87,122,.65), 0 16px 34px rgba(0,0,0,.4)`;
    plane.update(lt);
  };
  SHOTS.push(S);
})();

// global overlays
const grainTick = makeGrain();
const black = html('div', 'blackout', frame);
const warm = html('div', 'blackout', frame); warm.style.background = '#fff1dc';
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
  const w0 = prog(t, SC.s1b[0] - 0.2, SC.s1b[0]) * (1 - prog(t, SC.s1b[0], SC.s1b[0] + 0.3));
  const w1 = prog(t, SC.s7[0] - 0.3, SC.s7[0]) * (1 - prog(t, SC.s7[0], SC.s7[0] + 0.35));
  const w2 = prog(t, SC.s7[1] - 0.3, SC.s7[1]) * (1 - prog(t, SC.s7[1], SC.s7[1] + 0.35));
  const w3 = prog(t, P.end - 0.35, P.end) * (1 - prog(t, P.end, P.end + 0.45));
  const wh = prog(t, SC.s1[0] - 0.2, SC.s1[0]) * (1 - prog(t, SC.s1[0], SC.s1[0] + 0.3));
  warm.style.opacity = (0.9 * Math.max(wh * 0.8, w0 * 0.7, w1, w2, w3)).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
