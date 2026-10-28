// "4,380 วันที่รอ" — scenes timed to the Puck narration in vo.js (VO.P holds phrase onsets H0..D7; H is the "ถ้า..." hook).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0a: [0, P.H2 - 0.15], s0b: [P.H2 - 0.15, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.Cst - 0.3], s3: [P.Cst - 0.3, P.C5 - 0.15],
  s4: [P.C5 - 0.15, P.title], s5: [P.title, P.D0 - 0.1], s6: [P.D0 - 0.1, P.D5 - 0.15], s7: [P.D5 - 0.15, P.D7 - 0.15], s8: [P.D7 - 0.15, P.end], s9: [P.end, DURATION] };
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: 1640 }));

const heartPath = (cx, cy, r) => heartPathT(cx, cy, r);
function cardEl(parent, cls, x, y, w) {
  const c = html('div', cls, parent);
  c.style.left = x + 'px'; c.style.top = y + 'px'; if (w) c.style.width = w + 'px';
  const sh = html('div', 'shine', c);
  return { c, sh };
}
function fxSvg(shot) { return svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, shot.fx); }
const SHOTS = [];
const setGrade = (shot, extraBlur = 0) => { shot.root.style.filter = (shot.grade || '') + (extraBlur > 0.2 ? ` blur(${extraBlur.toFixed(1)}px)` : ''); };
function torsoPt(p, x, y) { const a = rad(p.torso || 0); return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; }
function toWorld(p, lx, ly) { const s = p.s || 1, f = p.f || 1; return [p.x + f * s * lx, p.y + s * ly]; }
function phoneProp(parent, case_ = '#2a2b36') {
  const g = svg('g', {}, parent);
  svg('rect', { x: -16, y: -44, width: 32, height: 62, rx: 7, fill: case_, stroke: INK, 'stroke-width': 3.5 }, g);
  const scr = svg('rect', { x: -12, y: -40, width: 24, height: 54, rx: 4, fill: '#d8e8ff' }, g);
  return { g, scr };
}
function holdPhone(pup, pose, fx = 78, fy = -RIG.T + 36, tap = 0) {
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, fx, fy));
  pose.aB = pup.reach(pose, tx - 6, ty + 8);
  pose.aF = pup.reach(pose, tx + 6, ty - 2 + tap * 9);
  pose.propRot = -12;
  return [tx, ty];
}
// clock card: time HH:MM with a sun/moon dial
function timeChip(parent, x, y, label) {
  const c = cardEl(parent, 'clock', x, y);
  c.c.innerHTML += `<div class="icslot"></div><div><div class="tl">${label}</div><div class="tt"><span class="hhmm">18:00</span></div></div>`;
  const clk = clockMoon(c.c.querySelector('.icslot'), 82);
  const hhmm = c.c.querySelector('.hhmm');
  return {
    c,
    update(t, tin, hours) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      const m = Math.floor(hours * 60) % (24 * 60), hh = Math.floor(m / 60), mm = m % 60;
      hhmm.textContent = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}`;
      clk.update(t, hh, mm);
    },
  };
}
const DOOR_DOG = { x: 540, y: 1410, s: 1.3 };   // where ลูกชิ้น sits, facing the door

// =====================================================================
// S0a — hook: "ถ้าคุณกลับบ้านดึกทุกวัน คุณคงไม่ทันเห็น" — she is still at her desk
// =====================================================================
(() => {
  const [A, B] = SC.s0a;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0]]);
  S.grade = 'saturate(1.05) contrast(1.04)';
  const set = officeLate(S), L = t => t - A;
  const chair = svg('g', {}, set.people);
  svg('rect', { x: 370, y: 960, width: 30, height: 250, rx: 12, fill: '#3a3f58', stroke: INK, 'stroke-width': 5 }, chair);
  svg('rect', { x: 380, y: 1184, width: 170, height: 26, rx: 10, fill: '#4a5072', stroke: INK, 'stroke-width': 5 }, chair);
  svg('rect', { x: 456, y: 1210, width: 14, height: 80, fill: '#2a2d3a' }, chair);
  svg('path', { d: 'M400,1300 L526,1300', stroke: '#2a2d3a', 'stroke-width': 12, 'stroke-linecap': 'round' }, chair);
  const me = new Puppet(set.people, OWNER, S.L.mid.defs);
  const clock = timeChip(S.ui, 56, 110, 'ยังไม่ได้กลับบ้าน');
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-30, -10, k), y: lerp(40, 60, k), z: lerp(1.3, 1.36, k), fx: 560, fy: 1100 });
    set.update(lt);
    const pose = { x: 470, y: 1184, s: 1.2, f: 1, torso: 8, head: 12 + Math.sin(lt * 1.3) * 2, lF: [0, 90], lB: [4, 92], t: lt + 2, smile: 0.15, eyes: null };
    const a = Math.sin(lt * 17), b = Math.sin(lt * 13 + 1);
    pose.aF = me.reach(pose, 650 + a * 8, 1012 - Math.max(0, a) * 8);
    pose.aB = me.reach(pose, 618 + b * 8, 1016 - Math.max(0, b) * 8);
    me.pose(pose);
    clock.update(lt, 0.1, 21 + 42 / 60 + lt / 60);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S0b — hook: "ถ้ามีใครนั่งรอหน้าประตูทุกคืน เขารอมานานแค่ไหน" — ลูกชิ้น at the door, under a spotlight
// =====================================================================
(() => {
  const [A, B] = SC.s0b;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0]]);
  S.grade = 'saturate(1.0) contrast(1.05) brightness(0.9)';
  const set = entrance(S), L = t => t - A;
  const dog = new Luukchin(set.people);
  const spot = html('div', 'spot', S.ui); spot.style.left = '200px';
  const qw = html('div', 'qwrap', S.ui); qw.style.left = '620px'; qw.style.top = '640px'; html('div', 'qmark', qw, '?');
  const fxs = fxSvg(S);
  const rip = ripples(fxs, 560, 1080, 150, '#ffe2a8', 3, 1.4);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: 0, y: lerp(120, 160, k), z: lerp(1.25, 1.35, k), fx: 480, fy: 1200 });
    set.update(lt + 3, 1, 0, 23.4 + lt / 60);
    dog.pose(Object.assign({}, DOOR_DOG, { f: -1, mode: 'sit', t: lt, wag: 0.15, perk: 0.9, eyes: 'open', look: -6 }));
    spot.style.opacity = (0.85 * prog(lt, 0.1, 0.5)).toFixed(3);
    popSquash(qw, lt, L(P.H5) - 0.05, `rotate(${(Math.sin(lt * 5) * 8).toFixed(1)}deg)`, 20); qw.style.opacity = fadeIn(lt, L(P.H5) - 0.05, 0.1);
    rip(lt, prog(lt, L(P.H4), L(P.H4) + 0.3));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — every evening at six he sits by the door: ears up, tail going… 9 pm, 10 pm, still waiting
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) contrast(1.03)';
  const set = entrance(S), L = t => t - A;
  const dog = new Luukchin(set.people);
  const clock = timeChip(S.ui, 56, 110, 'ลูกชิ้นรอเจ้าของ');
  const wait = waitChip(S.ui, 560, 120);
  const fxs = fxSvg(S);
  const zz = Array.from({ length: 3 }, (_, i) => { const e = svg('text', { 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 40 + i * 8, fill: '#fff6dc', opacity: 0 }, fxs); e.textContent = 'z'; return e; });
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, L(P.A6), L(P.A9)));
    const camK = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-20, 10, camK), y: lerp(120, 150, camK), z: lerp(1.22, 1.3, camK), fx: 480, fy: 1250 });
    const hour = 18 + 4 * k + prog(lt, L(P.A9), B - A) * 0.6;
    set.update(lt, k, 0, hour);
    const lie = ease.inOutSine(prog(lt, L(P.A9) - 0.1, L(P.A9) + 0.4));
    const perkUp = lt > L(P.A4) - 0.1 && lt < L(P.A6) + 0.4;
    const wagHard = lt > L(P.A5) - 0.1 && lt < L(P.A6) + 0.6;
    const hop = perkUp ? Math.abs(Math.sin((lt - L(P.A4)) * 8)) * 8 * (1 - prog(lt, L(P.A5) + 0.5, L(P.A6))) : 0;
    dog.pose(Object.assign({}, DOOR_DOG, { y: DOOR_DOG.y - hop, f: -1, mode: lie > 0.5 ? 'lie' : 'sit', t: lt, wag: wagHard ? 1 : lerp(0.45, 0.12, k), perk: perkUp ? 1 : lerp(0.95, 0.55, k), look: perkUp ? -10 : -4, eyes: 'open', sad: lerp(0, 0.6, k) * (perkUp ? 0 : 1) }));
    clock.update(lt, L(P.A0) - 0.1, hour);
    wait.update(lt, L(P.A6) - 0.1, 4 * k);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — home at last: one pat on the head, then the phone all night; ลูกชิ้น lies at her feet and watches her
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.06) contrast(1.04)';
  const set = livingNight(S), L = t => t - A;
  const me = new Puppet(set.people, OWNER, S.L.mid.defs); const ph = phoneProp(me.prop);
  const dog = new Luukchin(set.people);
  const chips = patVsPhone(S.ui, 470, 260);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-20, 0, k), y: lerp(110, 140, k), z: lerp(1.28, 1.36, k), fx: 460, fy: 1250 });
    set.update(lt + 2);
    const pat = ease.inOutSine(prog(lt, L(P.B2) - 0.35, L(P.B2))) * (1 - ease.inOutSine(prog(lt, L(P.B2) + 0.35, L(P.B3) - 0.05)));
    const lie = ease.inOutSine(prog(lt, L(P.B4) - 0.25, L(P.B4) + 0.3));
    const dx = 548 + 30 * lie;
    dog.pose({ x: dx, y: 1420, s: 1.2, f: -1, mode: lie > 0.5 ? 'lie' : 'sit', t: lt, wag: lt < L(P.B3) ? 0.9 : 0.15, perk: lt < L(P.B3) ? 1 : 0.6, look: lie > 0.5 ? -14 : -8, eyes: lt > L(P.B2) - 0.1 && lt < L(P.B2) + 0.35 ? 'happy' : 'open', sad: lt > L(P.B5) ? 0.5 : 0 });
    const pose = { x: 352, y: 1162, s: 1.2, f: 1, torso: 6 + 24 * pat, head: lerp(14, 26, pat) + Math.sin(lt * 1.2) * 2, lF: [-2, 90], lB: [0, 91], t: lt + 4, smile: lt > L(P.B3) ? 0.45 : 0.3, eyes: null };
    const [px, py] = holdPhone(me, pose, 74, -RIG.T + 44, lt > L(P.B3) ? Math.max(0, Math.sin(lt * 9)) * 0.6 : 0);
    if (pat > 0) { const toH = me.reach(pose, 518, 1246); pose.aF = [lerp(pose.aF[0], toH[0], pat), lerp(pose.aF[1], toH[1], pat)]; }
    me.pose(pose);
    ph.scr.setAttribute('fill', '#cfe4ff');
    setA(set.pglow, { cx: px.toFixed(1), cy: (py - 40).toFixed(1), opacity: lt > L(P.B3) - 0.2 ? 1 : 0 });
    chips.update(lt, L(P.B2) + 0.35, L(P.B3) + 0.3);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — the vet: twelve years old, time may be short
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.0) contrast(1.03)';
  const set = vetClinic(S), L = t => t - A;
  const dog = new Luukchin(set.people, { old: true });
  const me = new Puppet(set.people, OWNER_HOME, S.L.mid.defs);
  const card = vetCard(S.ui, 110, 170, 860);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(0, 20, k), y: lerp(240, 260, k), z: lerp(1.2, 1.26, k), fx: 560, fy: 1150 });
    set.update(lt);
    dog.pose({ x: 520, y: 1044, s: 1.15, f: 1, mode: 'lie', t: lt * 0.7, wag: 0.05, perk: 0.25, look: -8, eyes: lt > L(P.C4) && lt < L(P.C4) + 0.5 ? 'shut' : 'open', sad: 0.8 });
    const pose = { x: 800, y: 1102, s: 1.2, f: -1, torso: 12, head: 18, lF: [90, 90], lB: [88, 92], t: lt + 1, smile: lt > L(P.C3) ? 0.0 : 0.3, eyes: null, aB: [96, 84] };
    const stroke = Math.sin(lt * 2.2) * 18;
    pose.aF = me.reach(pose, 572 + stroke * 0.6, 958);
    me.pose(pose);
    card.update(lt, L(P.C1) - 0.2, L(P.C3) - 0.05, L(P.C4));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — 12 × 365 = 4,380 days… and almost every one of them spent waiting for her
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.02) contrast(1.04)';
  const set = entrance(S), L = t => t - A;
  const dog = new Luukchin(set.people, { old: true });
  const card = daysCard(S.ui, 90, 210, 900);
  S.update = lt => {
    const push = ease.inOutCubic(prog(lt, L(P.C9) - 0.4, L(P.C9) + 0.6));
    S.cam({ x: lerp(0, 10, push), y: lerp(60, 170, push), z: lerp(1.05, 1.4, push), fx: 520, fy: 1250 });
    set.update(lt + 5, 1, 0, 21.5 + lt / 60);
    dog.pose(Object.assign({}, DOOR_DOG, { f: -1, mode: 'sit', t: lt, wag: 0.2, perk: 0.7, look: -6, eyes: 'open', sad: 0.3 }));
    card.update(lt, 0.05, L(P.C6) - 0.1, L(P.C7) - 0.15, L(P.C8) - 0.05);
    const out = ease.inCubic(prog(lt, L(P.C9) - 0.35, L(P.C9) + 0.1));
    card.c.c.style.opacity = (parseFloat(card.c.c.style.opacity || 1) * (1 - out)).toFixed(3);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S5 — title: 4,380 วัน / ที่รอ
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = entrance(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 93, { color: '#ffe2a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '400px'; ic.innerHTML = dogAv(230, { old: true, bg: '#ffe9c4' });
  const isvg = ic.querySelector('svg'); isvg.style.borderRadius = '50%'; isvg.style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.45)';
  const t1 = html('div', 'title', wrap); t1.style.top = '690px'; t1.style.font = '700 190px/1 Kanit';
  const digits = ['4', ',', '3', '8', '0'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'วัน'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '110px';
  const t2 = html('div', 'title', wrap, 'ที่รอ'); t2.style.top = '910px'; t2.style.font = '600 120px/1 Kanit'; t2.style.color = '#ffd166';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1070px', width: '200px', height: '8px', borderRadius: '4px', background: '#ffd166', boxShadow: '0 0 16px rgba(255,209,102,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5, 1, 0, 22); bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.5, 14, 7); unit.style.opacity = fadeIn(lt, 0.5, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.65, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.65, 1.1))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.9, 1.3)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — today she is home at six: the door opens, ลูกชิ้น runs and jumps, they both go down laughing
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.12) contrast(1.03) brightness(1.03)';
  const set = entrance(S), L = t => t - A;
  const me = new Puppet(set.people, OWNER, S.L.mid.defs);
  const dog = new Luukchin(set.people, { old: true });
  const clock = timeChip(S.ui, 56, 110, 'วันนี้กลับบ้าน');
  const ok = html('div', 'okstamp', S.ui); Object.assign(ok.style, { left: '440px', top: '118px', right: 'auto', bottom: 'auto' }); ok.innerHTML = '✓ ตรงเวลา';
  const fxs = fxSvg(S);
  const hearts = heartsRise(fxs, 480, 1100, L(P.D4) + 0.1, 12, 611, 0.22);
  const confs = [[300, 900, 613], [700, 900, 617]].map(([cx, cy, sd]) => burst(fxs, cx, cy, L(P.D4), 26, sd, ['#ffd66b', '#ff9fc0', '#ffffff', '#7fd6c7'], 340, 1.4));
  const leak = lightLeak(S.fx);
  S.update = lt => {
    const shake = lt > L(P.D4) && lt < L(P.D4) + 0.3 ? Math.sin(lt * 70) * 6 * (1 - prog(lt, L(P.D4), L(P.D4) + 0.3)) : 0;
    S.cam({ x: 0 + shake, y: 130, z: 1.22, fx: 500, fy: 1250 });
    const open = ease.inOutCubic(prog(lt, L(P.D1) - 0.3, L(P.D1) + 0.3));
    set.update(lt + 7, 0.05, open, 18 + lt / 60);
    // her: steps in, then sits down hard with the dog in her lap
    const fall = ease.inOutSine(prog(lt, L(P.D4) - 0.05, L(P.D4) + 0.3));
    const step = ease.inOutSine(prog(lt, L(P.D1), L(P.D2)));
    const pose = { x: lerp(300, 330, step), y: lerp(1170, 1352, fall), s: 1.2, f: 1, torso: lerp(0, -26, fall), head: lerp(4, -14, fall), lF: [lerp(90, -6, fall), lerp(90, 8, fall)], lB: [lerp(88, 4, fall), lerp(92, 14, fall)], t: lt, smile: lt > L(P.D2) ? 1 : 0.7, grin: lt > L(P.D3) ? 1 : 0, eyes: lt > L(P.D4) + 0.2 ? 0 : null, aB: [lerp(96, -150, fall), lerp(80, -120, fall)], aF: [lerp(84, -40, fall), lerp(70, -70, fall)] };
    if (lt > L(P.D2) && fall < 0.5) { pose.aF = [-20, -60]; pose.aB = [-160, -120]; }
    me.pose(pose);
    // him: runs in from the right, leaps, lands on her lap licking
    const run = prog(lt, L(P.D2) - 0.2, L(P.D3));
    const jump = prog(lt, L(P.D3), L(P.D4) + 0.1);
    let dp;
    if (lt < L(P.D2) - 0.2) dp = { x: 940, y: 1430, mode: 'sit', look: -10, perk: 1, wag: 1 };
    else if (jump <= 0) dp = { x: lerp(940, 560, run), y: 1430, mode: 'run', ph: lt * 22, wag: 1, mouth: 1 };
    else if (lt < L(P.D4) + 0.1) dp = { x: lerp(560, 450, jump), y: 1430 - Math.sin(Math.PI * jump) * 170, mode: 'jump', rot: lerp(-30, 10, jump), wag: 1, mouth: 1, eyes: 'happy' };
    else dp = { x: 470, y: 1330, mode: 'stand', rot: 18, wag: 1, mouth: 1, eyes: 'happy', look: -16 + Math.sin(lt * 14) * 6 };
    dog.pose(Object.assign({ s: 1.2, f: -1, t: lt, perk: 1 }, dp));
    clock.update(lt, 0.05, 18 + lt / 60);
    popSquash(ok, lt, L(P.D1) + 0.1); ok.style.opacity = lt > L(P.D1) + 0.05 ? 1 : 0;
    hearts(lt); confs.forEach(c => c(lt)); leak(lt, 0.2 + 0.4 * prog(lt, L(P.D4), L(P.D4) + 0.6));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — "ชีวิตเรามีหลายอย่าง แต่ชีวิตเขามีแค่เรา"
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const S = new Shot(A, B, [['far', 0.4, 12], ['mid', 1, 12]]);
  const room = livingNight(S), L = t => t - A;
  S.L.far.el.style.filter = 'blur(12px) brightness(0.55) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(12px) brightness(0.55) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 97, { color: '#ffd9a8', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const life = lifeCompare(S.ui, 520);
  const dogB = html('div', 'title', S.ui); dogB.style.top = '1180px'; dogB.style.left = '560px'; dogB.style.right = '40px'; dogB.innerHTML = dogAv(170, { old: true, happy: true, bg: '#ffe9c4' });
  dogB.querySelector('svg').style.borderRadius = '50%';
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.06, 1.1, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    room.update(lt + 9); bok(lt);
    life.update(lt, 0.1, L(P.D6) + 0.1);
    popSquash(dogB, lt, L(P.D6) + 0.35, `rotate(${(Math.sin(lt * 3) * 5).toFixed(1)}deg)`, -12); dogB.style.opacity = fadeIn(lt, L(P.D6) + 0.35, 0.1);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S8 — "กลับบ้านไปกอดเขาบ้างนะ": she hugs him on the rug
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.1) contrast(1.03)';
  const set = livingNight(S), L = t => t - A;
  const me = new Puppet(set.people, OWNER_HOME, S.L.mid.defs);
  const dog = new Luukchin(set.people, { old: true });
  const fxs = fxSvg(S);
  const hearts = heartsRise(fxs, 540, 1150, 0.2, 12, 707, 0.2);
  const leak = lightLeak(S.fx);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: 0, y: lerp(200, 220, k), z: lerp(1.35, 1.45, k), fx: 520, fy: 1350 });
    set.update(lt + 11);
    const pose = { x: 430, y: 1500, s: 1.25, f: 1, torso: 14, head: 20, lF: [4, 176], lB: [16, 168], t: lt, smile: 1, grin: 0.6, eyes: 0 };
    pose.aF = me.reach(pose, 640, 1370); pose.aB = me.reach(pose, 610, 1350);
    dog.pose({ x: 590, y: 1530, s: 1.2, f: -1, mode: 'sit', t: lt, wag: 1, perk: 0.8, look: 14, tilt: 6, eyes: 'happy', mouth: 0 });
    me.pose(pose);
    hearts(lt); leak(lt, 0.45);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S9 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s9;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#6a4a6e'], [0.6, '#352440'], [1, '#170f1f']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 143, { color: '#ffe2a8', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const fxs = fxSvg(S);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const icon = html('div', 'title', wrap); icon.style.top = '300px'; icon.innerHTML = dogAv(230, { old: true, happy: true, tongue: true, bg: '#ffe9c4' });
  icon.querySelector('svg').style.borderRadius = '50%'; icon.querySelector('svg').style.boxShadow = '0 0 0 8px #fff, 0 20px 40px rgba(0,0,0,.4)';
  const t1 = html('div', 'title', wrap); t1.style.top = '600px'; t1.style.font = '700 170px/1 Kanit';
  const digits = ['4', ',', '3', '8', '0'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'วัน'); unit.style.marginLeft = '0.2em'; unit.style.fontSize = '96px';
  const t2 = html('div', 'title', wrap, 'ที่รอ'); t2.style.top = '800px'; t2.style.font = '600 108px/1 Kanit'; t2.style.color = '#ffd166';
  const sub = html('div', 'title', wrap, 'วันนี้กลับบ้านไปกอดเขาบ้างนะ'); sub.style.top = '975px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffe9c4';
  const cta = html('div', 'cta', wrap); cta.style.top = '1110px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่มีน้องรออยู่บ้าน</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  const spark = burst(fxs, 540, 420, 0.3, 18, 153, ['#ffd66b', '#ffffff', '#ff9fc0'], 240, 0.9);
  S.update = lt => {
    bok(lt); leak(lt, 0.4);
    popSquash(icon, lt, 0.15, `rotate(${(Math.sin(lt * 2.4) * 4).toFixed(2)}deg)`, -20);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.07, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.7, 14, 7); unit.style.opacity = fadeIn(lt, 0.7, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.8, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.8, 1.2))) * 100).toFixed(1)}% -40% 0)`;
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.8, fl(SC.s2[0]) * 0.5, fl(SC.s3[0]) * 0.5, fl(SC.s5[0]), fl(SC.s6[0]) * 0.8, fl(SC.s7[0]) * 0.6, fl(SC.s8[0]) * 0.6, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
