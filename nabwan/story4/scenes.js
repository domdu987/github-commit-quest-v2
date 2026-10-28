// "47 ครั้งที่ลบข้อความ" — scenes timed to the Charon narration in vo.js (VO.P holds phrase onsets A0..D6).
const frame = document.getElementById('frame');
const subsBox = document.getElementById('subs');
const P = VO.P;
const DURATION = P.DUR;

const SC = { s0: [0, P.A0 - 0.3], s1: [P.A0 - 0.3, P.B0 - 0.3], s2: [P.B0 - 0.3, P.Cst - 0.3], s3: [P.Cst - 0.3, P.C4 - 0.1], s4: [P.C4 - 0.1, P.title], s5: [P.title, P.D0 - 0.1], s6: [P.D0 - 0.1, P.D4 - 0.2], s7: [P.D4 - 0.2, P.end], s8: [P.end, DURATION] };
const SUB_TOP = [[0, SC.s4[0], 1630], [SC.s4[0], P.title, 1790], [SC.s6[0], SC.s6[1], 1640], [SC.s7[0], 99, 1790]];
const CUES = VO.CUES.map(c => Object.assign({}, c, { top: (SUB_TOP.find(([a, b]) => c.a >= a - 0.3 && c.a < b) || [0, 0, 1640])[2] }));

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
const rectCenter = el => { const r = el.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2, r.width]; };
function holdPhone(pup, pose, fx = 78, fy = -RIG.T + 36, tap = 0) {
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, fx, fy));
  pose.aB = pup.reach(pose, tx - 6, ty + 8);
  pose.aF = pup.reach(pose, tx + 6, ty - 2 + tap * 9);
  pose.propRot = -12;
}
const girlAv = (n = 64) => portrait4('girl', n, '#fde2e8');
const guyAv = (n = 64) => portrait4('guy', n, '#dbe7f3');
const GUYP = { x: 300, y: 1296, s: 1.2 };       // guy on the beanbag
const GIRLP = { x: 640, y: 1250, s: 1.2 };      // girl on the bed edge
// the guy, knees up on the beanbag, phone in both hands
function guyPose(guy, lt, o = {}) {
  const pose = Object.assign({ x: GUYP.x, y: GUYP.y, s: GUYP.s, f: 1, torso: 2, head: 14, lF: [-38, 62], lB: [-32, 66], t: lt + 1, smile: 0.6 }, o);
  holdPhone(guy, pose, 82, -RIG.T + 44, o.tap || 0);
  if (o.palm) { const [hx, hy] = toWorld(pose, ...torsoPt(pose, HEAD_C[0] + 50, HEAD_C[1] - 6)); const a = guy.reach(pose, hx, hy); pose.aF = [lerp(pose.aF[0], a[0], o.palm), lerp(pose.aF[1], a[1], o.palm)]; }
  guy.pose(pose);
  return pose;
}
// the girl on her bed, hugging the teddy with her back arm, phone in front hand
function girlPose(girl, lt, o = {}) {
  const kick = o.kick ? Math.sin(lt * 14) * 18 * o.kick : 0;
  const pose = Object.assign({ x: GIRLP.x, y: GIRLP.y, s: GIRLP.s, f: -1, torso: 6, head: -4, lF: [-8 + kick, 80 + kick], lB: [-2 - kick, 86 - kick], t: lt + 2, smile: 0.8, ponyKick: kick * 0.4 }, o);
  const [tx, ty] = toWorld(pose, ...torsoPt(pose, 74, -RIG.T + 40));
  pose.aB = girl.reach(pose, tx + 10, ty + 30);
  pose.aF = girl.reach(pose, tx, ty - 6 + (o.tap || 0) * 9);
  pose.propRot = -12;
  girl.pose(pose);
  return pose;
}

// =====================================================================
// S0 — hook: "ถ้าคุณแอบชอบใคร คุณพิมพ์แล้วลบอยู่ทั้งคืน ถ้าเขาก็แอบชอบคุณอยู่ เขาจะทำแบบเดียวกันไหม"
// =====================================================================
(() => {
  const [A, B] = SC.s0;
  const S = new Shot(A, B, [['far', 0.4, 10], ['mid', 1, 10]]);
  const room = guyRoom(S), L = t => t - A;
  S.L.far.el.style.filter = 'blur(10px) brightness(0.55) saturate(1.1)'; S.L.mid.el.style.filter = 'blur(10px) brightness(0.55) saturate(1.1)';
  const fxs = fxSvg(S);
  const behind = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible' }, S.ui);   // bokeh + hearts sit behind the cards and her portrait, never across a face
  const bok = floaters(behind, [0, 200, 1080, 1400], 14, 71, { color: '#ffc4d6', rMin: 12, rMax: 36, speed: 10, op: 0.2, base: 0.05, amp: 20 });
  const prof = profileCard(S.ui, 250, 280, 580);
  const chat = chatPhone(S.ui, 290, 250, 500, 900, 'ฝน', girlAv());
  chat.add('text', 'L', -1, { text: 'ขอบคุณที่ช่วยเรื่องงานนะ', meta: 'เมื่อวาน' });
  const inp = chatInput(chat);
  const words = ['กินข้าวยัง', 'ทำอะไรอยู่', 'ว่างไหม', 'นอนยัง', 'หวัดดี'];
  const script = []; const dels = [];
  for (let i = 0, t = L(P.H1) + 0.05; t < L(P.H4) - 0.4; i++, t += 0.5) {
    script.push({ t0: t, t1: t + 0.25, text: words[i % words.length], mode: 'type' }, { t0: t + 0.3, t1: t + 0.42, text: words[i % words.length], mode: 'del' });
    dels.push(t + 0.3);
  }
  const clock = nightClock(S.ui, 56, 110, 'คืนวันศุกร์');
  const spot = html('div', 'spot', S.ui);
  const herB = html('div', 'title', S.ui); herB.style.top = '330px'; herB.innerHTML = portrait4('girl', 320, '#fde2e8');
  const hsvg = herB.querySelector('svg'); hsvg.style.borderRadius = '50%'; hsvg.style.boxShadow = '0 0 0 10px #fff, 0 30px 60px rgba(0,0,0,.5)';
  const qw = html('div', 'qwrap', S.ui); qw.style.left = '700px'; qw.style.top = '300px'; html('div', 'qmark', qw, '?');
  const rip = ripples(fxs, 540, 500, 170, '#ffc4d6', 3, 1.4);
  const hearts = heartsRise(behind, 540, 640, L(P.H5), 6, 41, 0.3);
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.14, prog(lt, 0, B - A)), fx: 540, fy: 900 });
    room.update(lt); bok(lt);
    const out0 = ease.inCubic(prog(lt, L(P.H1) - 0.25, L(P.H1) + 0.05));
    prof.update(lt, L(P.H0) + 0.05, L(P.H0) + 0.5);
    prof.c.c.style.opacity = (fadeIn(lt, L(P.H0) + 0.05, 0.12) * (1 - out0)).toFixed(3);
    prof.c.c.style.transform += ` translateX(${(-out0 * 700).toFixed(1)}px)`;
    const out1 = ease.inCubic(prog(lt, L(P.H4) - 0.3, L(P.H4)));
    enter3d(chat.el, lt, L(P.H1) - 0.1, 'pop');
    chat.el.style.opacity = (fadeIn(lt, L(P.H1) - 0.1, 0.12) * (1 - out1)).toFixed(3);
    chat.el.style.transform += ` translateX(${(out1 * 800).toFixed(1)}px)`;
    chat.update(lt); inp.update(lt, script);
    clock.update(lt, L(P.H1), 21 * 60 + Math.floor(ease.inOutSine(prog(lt, L(P.H1), L(P.H4))) * 270));
    clock.c.c.style.opacity = (fadeIn(lt, L(P.H1), 0.12) * (1 - out1)).toFixed(3);
    spot.style.opacity = (0.9 * prog(lt, L(P.H4) - 0.1, L(P.H4) + 0.3)).toFixed(3);
    popSquash(herB, lt, L(P.H4) + 0.05, '', -12); herB.style.opacity = fadeIn(lt, L(P.H4) + 0.05, 0.12);
    popSquash(qw, lt, L(P.H6) - 0.05, `rotate(${(Math.sin(lt * 5) * 8).toFixed(1)}deg)`, 20); qw.style.opacity = fadeIn(lt, L(P.H6) - 0.05, 0.1);
    rip(lt, prog(lt, L(P.H5), L(P.H5) + 0.3)); hearts(lt);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S1 — 21:00: he types "กินข้าวยัง", deletes, retypes, deletes… 47 times
// =====================================================================
(() => {
  const [A, B] = SC.s1;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) contrast(1.04)';
  const set = guyRoom(S), L = t => t - A;
  const guy = new Puppet(set.people, GUY, S.L.mid.defs);
  const ph = phoneProp(guy.prop);
  const clock = nightClock(S.ui, 56, 110, 'คืนวันศุกร์');
  const chat = chatPhone(S.ui, 600, 250, 420, 760, 'ฝน', girlAv());
  chat.add('text', 'L', -1, { text: 'ขอบคุณที่ช่วยเรื่องงานนะ', meta: 'เมื่อวาน' });
  const inp = chatInput(chat);
  // typing / deleting script and the delete times
  const script = [{ t0: L(P.A3) - 0.2, t1: L(P.A3) + 0.8, text: 'กินข้าวยัง', mode: 'type' }, { t0: L(P.A4), t1: L(P.A4) + 0.35, text: 'กินข้าวยัง', mode: 'del' },
    { t0: L(P.A5), t1: L(P.A5) + 0.6, text: 'ทำอะไรอยู่', mode: 'type' }, { t0: L(P.A6), t1: L(P.A6) + 0.3, text: 'ทำอะไรอยู่', mode: 'del' }];
  const dels = [L(P.A4), L(P.A6)];
  const words = ['สวัสดี', 'เฮ้', 'ว่างไหม', 'กินข้าวยัง', 'ฝน', 'หวัดดี', 'นอนยัง'];
  for (let i = 0, t = L(P.A7); t < L(P.A8) + 1.6; i++, t += 0.42) {
    script.push({ t0: t, t1: t + 0.22, text: words[i % words.length], mode: 'type' }, { t0: t + 0.26, t1: t + 0.38, text: words[i % words.length], mode: 'del' });
    dels.push(t + 0.26);
  }
  const del = deleteCounter(S.ui, 56, 300);
  const fxs = fxSvg(S);
  const balls = paperBalls(fxs, dels);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-20, 10, k), y: 30, z: lerp(1.08, 1.14, k), fx: 420, fy: 1100 });
    set.update(lt);
    const deleting = dels.some(td => lt > td && lt < td + 0.3);
    const palm = ease.inOutSine(prog(lt, L(P.A8) + 0.7, L(P.A8) + 1.0)) * (1 - ease.inOutSine(prog(lt, B - A - 0.4, B - A)));
    guyPose(guy, lt, { smile: deleting ? 0.15 : 0.55, head: 14 + (deleting ? Math.sin(lt * 20) * 4 : 0), palm, eyes: palm > 0.5 ? 0 : null, tap: lt > L(P.A3) - 0.2 && lt < L(P.A3) + 0.8 ? Math.max(0, Math.sin(lt * 18)) : 0 });
    ph.scr.setAttribute('fill', '#e9f4ff');
    clock.update(lt, 0.05, 21 * 60 + Math.floor(prog(lt, 0.8, B - A) * 9));
    enter3d(chat.el, lt, L(P.A1) - 0.1, 'pop');
    chat.update(lt); inp.update(lt, script);
    // count: one by one, then rolls up to 47 on "ลบไปสี่สิบเจ็ดครั้ง"
    const n = dels.filter(td => lt >= td).length;
    const roll = rollValue(lt, L(P.A8) + 0.2, L(P.A8) + 1.4, Math.min(n, 9), 47);
    const v = lt < L(P.A8) + 0.2 ? Math.min(n, 9) : roll.v;
    del.update(lt, L(P.A4) - 0.05, v, lt < L(P.A8) + 0.2 ? 0 : roll.speed, dels);
    const [bx, by] = rectCenter(inp.bar), [dx, dy] = rectCenter(del.el);
    balls(lt, bx - 60, by, dx - 120, dy);
    setGrade(S, (1 - prog(lt, 0, 0.4)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S2 — the worries, then her profile on repeat until 1:30 am
// =====================================================================
(() => {
  const [A, B] = SC.s2;
  const S = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.08) contrast(1.04)';
  const set = guyRoom(S), L = t => t - A;
  const guy = new Puppet(set.people, GUY, S.L.mid.defs);
  const ph = phoneProp(guy.prop);
  const clock = nightClock(S.ui, 56, 110, 'คืนวันศุกร์');
  const f1 = fearBubble(S.ui, 60, 330, 'annoyed', 'รำคาญ?');
  const f2 = fearBubble(S.ui, 410, 250, 'noreply', 'ไม่ตอบ?');
  const f3 = fearBubble(S.ui, 760, 330, 'oneside', 'ฝ่ายเดียว?');
  const prof = profileCard(S.ui, 250, 260, 580);
  const fxs = fxSvg(S);
  const hearts = heartsRise(fxs, 340, 780, L(P.B4) + 0.6, 8, 31, 0.35);
  S.update = lt => {
    const k = ease.inOutSine(prog(lt, 0, B - A));
    S.cam({ x: lerp(-60, -40, k), y: lerp(80, 110, k), z: lerp(1.3, 1.36, k), fx: 380, fy: 1100 });
    set.update(lt + 3);
    const dreamy = lt > L(P.B4);
    const worried = lt < L(P.B4) - 0.2;
    guyPose(guy, lt, { smile: dreamy ? 0.95 : (worried ? 0.1 : 0.5), head: dreamy ? 10 : 18, torso: dreamy ? -4 : 4, eyes: null });
    ph.scr.setAttribute('fill', dreamy ? '#ffe4ee' : '#e9f4ff');
    const spin = ease.inOutSine(prog(lt, L(P.B5) - 0.1, L(P.B5) + 1.4));
    clock.update(lt, -1, 21 * 60 + 12 + Math.floor(spin * 258));
    const [hx, hy] = rectCenter(guy.head);
    f1.update(lt, L(P.B0) - 0.05, hx, hy - 90, L(P.B4) - 0.35);
    f2.update(lt, L(P.B1) - 0.05, hx, hy - 90, L(P.B4) - 0.35);
    f3.update(lt, L(P.B2) + 0.1, hx, hy - 90, L(P.B4) - 0.35);
    prof.update(lt, L(P.B4) - 0.1, L(P.B4) + 0.5);
    hearts(lt);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S3 — 1:30 am, he dozes, the thumb slips: bear-hug sticker sent. Heart drops. Under a second later: read + typing…
// =====================================================================
(() => {
  const [A, B] = SC.s3;
  const S = new Shot(A, B, [['far', 0.35, 2], ['mid', 1, 0], ['fore', 1.8, 12]]);
  S.grade = 'saturate(1.04) contrast(1.05)';
  const set = guyRoom(S), L = t => t - A;
  const guy = new Puppet(set.people, GUY, S.L.mid.defs);
  const ph = phoneProp(guy.prop);
  const chat = chatPhone(S.ui, 570, 200, 460, 880, 'ฝน', girlAv());
  chat.add('text', 'L', -1, { text: 'ขอบคุณที่ช่วยเรื่องงานนะ', meta: 'เมื่อวาน' });
  const tSend = L(P.C1) - 0.15;
  chat.add('custom', 'R', tSend, { html: bearHugSVG(230), meta: 'อ่านแล้ว', read: L(P.C3) + 0.15 });
  chat.add('typing', 'L', L(P.C3) + 0.45, {});
  const inp = chatInput(chat);
  const fast = fastChip(S.ui, 70, 1030);
  const fxs = fxSvg(S);
  const drop = fallingHeart(fxs);
  const sweat = Array.from({ length: 3 }, () => svg('path', { d: 'M0,-7 C3,-2 5,2 5,4 A5,5 0 1 1 -5,4 C-5,2 -3,-2 0,-7 Z', fill: '#bfe9ff', stroke: '#fff', 'stroke-width': 1.5, opacity: 0 }, fxs));
  S.update = lt => {
    const shock = lt > L(P.C2) - 0.1 && lt < L(P.C3) + 0.2;
    const shake = shock ? Math.sin(lt * 70) * 7 * (1 - prog(lt, L(P.C2) - 0.1, L(P.C2) + 0.6)) : 0;
    S.cam({ x: -60 + shake, y: lerp(160, 190, prog(lt, 0, B - A)), z: lerp(1.5, 1.58, prog(lt, 0, B - A)), fx: 380, fy: 1100 });
    set.update(lt + 9);
    const doze = ease.inOutSine(prog(lt, 0.2, L(P.C0) + 0.8)) * (1 - (lt > tSend + 0.15 ? 1 : 0));
    const happy = lt > L(P.C3) + 0.4;
    guyPose(guy, lt, { head: 14 + doze * 18, torso: 2 + doze * 6, eyes: doze > 0.6 ? 0 : null, smile: shock ? 0 : (happy ? 0.7 : 0.4), mouthO: shock ? 1 : 0, tap: lt > tSend - 0.2 && lt < tSend ? 1 : 0 });
    ph.scr.setAttribute('fill', '#e9f4ff');
    enter3d(chat.el, lt, 0.05, 'pop');
    chat.update(lt); inp.update(lt, []);
    drop(lt, L(P.C2) - 0.05, ...rectCenter(guy.torso).slice(0, 2));
    const [hx, hy] = rectCenter(guy.head);
    sweat.forEach((s, i) => { const q = prog(lt, L(P.C2) + i * 0.15, L(P.C2) + 0.9 + i * 0.15); setA(s, { opacity: q > 0 && q < 1 ? (1 - q).toFixed(2) : 0, transform: `translate(${(hx + 60 + i * 18).toFixed(1)},${(hy - 50 + q * 60).toFixed(1)}) scale(2)` }); });
    fast.update(lt, L(P.C3) + 0.05);
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S4 — split: her reply lands on his phone; below, her 52 deleted drafts
// =====================================================================
(() => {
  const [A, B] = SC.s4;
  const L = t => t - A;
  const top = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  top.root.style.clipPath = 'inset(0 0 50% 0)'; top.grade = 'saturate(1.08) contrast(1.04)';
  const gset = guyRoom(top);
  const guy = new Puppet(gset.people, GUY, top.L.mid.defs); const gph = phoneProp(guy.prop);
  const gchat = chatPhone(top.ui, 600, 60, 420, 830, 'ฝน', girlAv());
  gchat.add('custom', 'R', -1, { html: bearHugSVG(180), meta: 'อ่านแล้ว' });
  gchat.add('typing', 'L', -1, { until: L(P.C5) - 0.05 });
  gchat.add('text', 'L', L(P.C5) - 0.05, { text: 'รอเธอทักอยู่ตั้งนาน' });
  const gfx = fxSvg(top);
  const ghearts = heartsRise(gfx, 330, 600, L(P.C5) + 0.2, 10, 77, 0.25);
  top.update = lt => {
    top.cam({ x: 10, y: 530, z: 1.1, fx: 400, fy: 1000 });
    gset.update(lt + 12);
    const yay = lt > L(P.C5);
    guyPose(guy, lt, { smile: yay ? 1 : 0.5, grin: yay && lt < L(P.C5) + 2.2 ? 1 : 0, head: yay ? 4 : 14, torso: yay ? -6 : 2 });
    gph.scr.setAttribute('fill', yay ? '#ffe4ee' : '#e9f4ff');
    gchat.update(lt);
    ghearts(lt);
    setGrade(top, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(top);
  const bot = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  bot.root.style.clipPath = 'inset(50% 0 0 0)'; bot.grade = 'saturate(1.08) contrast(1.03)';
  const rset = girlRoom(bot);
  const girl = new Puppet(rset.people, GIRL, bot.L.mid.defs); const rph = phoneProp(girl.prop, '#f07aa8');
  const bear = svg('g', {}, rset.top); teddy(bear, 0, 0, 0.82);
  const rchat = chatPhone(bot.ui, 600, 1010, 430, 700, 'ภูมิ', guyAv());
  rchat.add('custom', 'L', -1, { html: bearHugSVG(170) });
  rchat.add('text', 'R', L(P.C5) - 0.05, { text: 'รอเธอทักอยู่ตั้งนาน', meta: 'ส่งแล้ว' });
  const rin = chatInput(rchat);
  const dc = cardEl(bot.ui, 'card drafts', 40, 990, 430);
  html('div', 'lbl', dc.c, 'ข้อความที่เธอลบทิ้ง');
  const lines = ['กินข้าวยัง', 'ทำอะไรอยู่จ๊ะ', 'ว่างไหม'].map(t => { const d = html('div', 'dl', dc.c, t); const st = html('i', '', d); return st; });
  const rdel = deleteCounter(bot.ui, 56, 1222, 'ลบไป');
  bot.update = lt => {
    bot.cam({ x: 344, y: -365, z: 1.1, fx: 600, fy: 1000 });
    rset.update(lt + 4);
    const typing = lt > L(P.C4) && lt < L(P.C5) - 0.1;
    const shy = ease.inOutSine(prog(lt, L(P.C6) - 0.2, L(P.C6) + 0.3));
    const pose = girlPose(girl, lt, { smile: 0.95, grin: lt > L(P.C6) ? 1 : 0, eyes: lt > L(P.C7) ? 0 : null, kick: prog(lt, L(P.C7), L(P.C7) + 0.3), tap: typing ? Math.max(0, Math.sin(lt * 18)) : 0, head: lerp(-4, 10, shy) });
    rph.scr.setAttribute('fill', '#ffe4ee');
    const [bx, by] = toWorld(pose, ...torsoPt(pose, 40, -RIG.T + lerp(96, 40, shy)));
    bear.setAttribute('transform', `translate(${bx.toFixed(1)},${by.toFixed(1)}) rotate(${(-8 + Math.sin(lt * 3) * 3).toFixed(1)})`);
    enter3d(rchat.el, lt, 0.05, 'pop');
    rchat.update(lt);
    rin.update(lt, [{ t0: L(P.C4), t1: L(P.C5) - 0.2, text: 'รอเธอทักอยู่ตั้งนาน', mode: 'type' }, { t0: L(P.C5) - 0.1, t1: L(P.C5) - 0.05, text: '', mode: 'hold' }]);
    enter3d(dc.c, lt, L(P.C6) - 0.05, 'swingLeft'); shine(dc.sh, lt, L(P.C6) + 0.4);
    lines.forEach((st, i) => { st.style.transform = `scaleX(${ease.outCubic(prog(lt, L(P.C7) + i * 0.25, L(P.C7) + 0.25 + i * 0.25)).toFixed(3)})`; });
    const r = rollValue(lt, L(P.C8) - 0.1, L(P.C8) + 1.0, 0, 52);
    rdel.update(lt, L(P.C8) - 0.25, r.v, r.speed, [L(P.C8) + 1.0]);
    setGrade(bot, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(bot);
  const seam = new Shot(A, B, []);
  const line = html('div', '', seam.ui); Object.assign(line.style, { position: 'absolute', left: 0, right: 0, top: '954px', height: '12px', background: 'linear-gradient(90deg,#ffd66b,#f07aa8,#ffd66b)', boxShadow: '0 0 24px rgba(255,214,107,.8)' });
  seam.update = lt => { line.style.opacity = (0.75 + 0.25 * Math.sin(lt * 5)).toFixed(3); };
  SHOTS.push(seam);
})();

// =====================================================================
// S5 — title: 47 ครั้ง / ที่ลบข้อความ
// =====================================================================
(() => {
  const [A, B] = SC.s5;
  const S = new Shot(A, B, [['far', 0.4, 14], ['mid', 1, 14]]);
  const room = girlRoom(S);
  S.L.far.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  S.L.mid.el.style.filter = 'blur(14px) brightness(0.45) saturate(1.1)';
  const bok = floaters(fxSvg(S), [0, 300, 1080, 1300], 16, 93, { color: '#ffc4d6', rMin: 14, rMax: 40, speed: 12, op: 0.22, base: 0.05, amp: 22 });
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const ic = html('div', 'title', wrap); ic.style.top = '430px';
  ic.innerHTML = `<svg width="210" height="200" viewBox="-60 -60 120 116"><path d="M-30,-14 L30,-14 L24,50 L-24,50 Z" fill="#9fb3c8" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><rect x="-36" y="-26" width="72" height="12" rx="5" fill="#c7d4e2" stroke="${INK}" stroke-width="5" transform="rotate(-18 -36 -14)"/><path d="${heartPathT(4, -38, 18)}" fill="#f04f7f" stroke="${INK}" stroke-width="4"/><path d="M-12,0 L-10,40 M0,0 L0,40 M12,0 L10,40" stroke="${INK}" stroke-width="3.5"/></svg>`;
  const t1 = html('div', 'title', wrap); t1.style.top = '660px'; t1.style.font = '700 190px/1 Kanit';
  const digits = ['4', '7'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ครั้ง'); unit.style.marginLeft = '0.25em'; unit.style.fontSize = '120px';
  const t2 = html('div', 'title', wrap, 'ที่ลบข้อความ'); t2.style.top = '880px'; t2.style.font = '600 112px/1 Kanit';
  const rule = html('div', '', wrap); Object.assign(rule.style, { position: 'absolute', left: '440px', top: '1050px', width: '200px', height: '8px', borderRadius: '4px', background: '#f07aa8', boxShadow: '0 0 16px rgba(240,122,168,.8)' });
  S.update = lt => {
    S.cam({ x: 0, y: 0, z: lerp(1.08, 1.12, prog(lt, 0, B - A)), fx: 560, fy: 800 });
    room.update(lt + 5); bok(lt);
    popSquash(ic, lt, 0.05, `rotate(${(Math.sin(lt * 2) * 4).toFixed(1)}deg)`, -16);
    digits.forEach((d, i) => { const t0 = 0.15 + i * 0.1, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.4, 14, 7); unit.style.opacity = fadeIn(lt, 0.4, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
    t2.style.opacity = fadeIn(lt, 0.55, 0.1);
    t2.style.clipPath = `inset(-40% ${((1 - ease.outCubic(prog(lt, 0.55, 1.0))) * 100).toFixed(1)}% -40% 0)`;
    rule.style.transform = `scaleX(${ease.outBack(prog(lt, 0.8, 1.2)).toFixed(3)})`;
  };
  SHOTS.push(S);
})();

// =====================================================================
// S6 — two phones, both "typing…" at each other: the one you fear annoying may be waiting for you
// =====================================================================
(() => {
  const [A, B] = SC.s6;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  const G = S.L.bg, L = t => t - A;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: lin(G.defs, [[0, '#26214a'], [0.6, '#4a2f63'], [1, '#7a3f62']]) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 26, 17, { color: '#ffd9e6', rMin: 8, rMax: 30, speed: 12, op: 0.22, base: 0.05, amp: 26, filter: blurFilter(G.defs, 4) });
  const left = chatPhone(S.ui, 40, 360, 470, 900, 'ฝน', girlAv());
  left.add('custom', 'R', -1, { html: bearHugSVG(150), meta: 'อ่านแล้ว' });
  left.add('typing', 'L', 0.2, {});
  const right = chatPhone(S.ui, 570, 360, 470, 900, 'ภูมิ', guyAv());
  right.add('custom', 'L', -1, { html: bearHugSVG(150) });
  right.add('typing', 'L', 0.35, {});
  const li = chatInput(left), ri = chatInput(right);
  const cap1 = html('div', 'chip big', S.ui); cap1.style.left = '70px'; cap1.style.top = '1300px'; cap1.innerHTML = '<span>เขา: <b>กลัวเธอรำคาญ</b></span>';
  const cap2 = html('div', 'chip big', S.ui); cap2.style.left = '600px'; cap2.style.top = '1300px'; cap2.innerHTML = '<span>เธอ: <b>รอเขาทักอยู่</b></span>';
  const fxs = fxSvg(S);
  const heart = svg('path', { d: heartPathT(0, 0, 60), fill: '#f04f7f', stroke: '#fff', 'stroke-width': 6 }, fxs);
  const glow = svg('circle', { r: 170, fill: rad2(G.defs, [[0, '#ff9fc0', 0.7], [1, '#ff9fc0', 0]]) }, fxs);
  fxs.insertBefore(glow, heart);
  S.update = lt => {
    bok(lt);
    enter3d(left.el, lt, 0.02, 'swingLeft'); enter3d(right.el, lt, 0.12, 'swingRight');
    left.update(lt); right.update(lt);
    const cyc = (t0, w) => [{ t0, t1: t0 + 0.55, text: w, mode: 'type' }, { t0: t0 + 0.75, t1: t0 + 0.95, text: w, mode: 'del' }];
    li.update(lt, [...cyc(0.25, 'กินข้าวยัง'), ...cyc(1.2, 'ว่างไหม'), ...cyc(2.15, 'หวัดดี')]);
    ri.update(lt, [...cyc(0.4, 'ทักมาสิ'), ...cyc(1.35, 'กินข้าวยัง'), ...cyc(2.3, 'คิดถึง')]);
    popSquash(cap1, lt, L(P.D1) + 0.1); popSquash(cap2, lt, L(P.D2) + 0.1);
    const beat = Math.pow(Math.max(0, Math.sin(lt * 6)), 4), on = spring(lt, L(P.D2), 13, 6);
    heart.setAttribute('transform', `translate(540,300) scale(${(on * (1 + 0.15 * beat)).toFixed(3)})`);
    glow.setAttribute('transform', 'translate(540,300)'); glow.setAttribute('opacity', (on * (0.6 + 0.4 * beat)).toFixed(3));
    setGrade(S, (1 - prog(lt, 0, 0.3)) * 10);
  };
  SHOTS.push(S);
})();

// =====================================================================
// S7 — split: he finally sends; a rival pops up on her phone; he panics and sends three bears; she laughs
// =====================================================================
(() => {
  const [A, B] = SC.s7;
  const L = t => t - A;
  const tPress = L(P.D4) + 0.3, tRival = L(P.D5) + 0.05, tSpam = [L(P.D6) + 0.05, L(P.D6) + 0.35, L(P.D6) + 0.65];
  const top = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  top.root.style.clipPath = 'inset(0 0 50% 0)'; top.grade = 'saturate(1.08) contrast(1.04)';
  const gset = guyRoom(top);
  const guy = new Puppet(gset.people, GUY, top.L.mid.defs); const gph = phoneProp(guy.prop);
  const gchat = chatPhone(top.ui, 600, 60, 420, 830, 'ฝน', girlAv());
  gchat.add('text', 'L', -1, { text: 'รอเธอทักอยู่ตั้งนาน' });
  gchat.add('text', 'R', tPress + 0.05, { text: 'กินข้าวยัง', meta: 'อ่านแล้ว', read: tPress + 0.8 });
  tSpam.forEach(ts => gchat.add('custom', 'R', ts, { html: bearHugSVG(130) }));
  const send = bigSend(top.ui, 40, 150);
  top.update = lt => {
    top.cam({ x: 10, y: 530, z: 1.1, fx: 400, fy: 1000 });
    gset.update(lt + 15);
    const panic = lt > tRival && lt < tSpam[2] + 0.4;
    guyPose(guy, lt, { smile: panic ? 0.05 : 0.9, mouthO: panic ? 1 : 0, tap: [tPress, ...tSpam].some(tp => lt > tp - 0.1 && lt < tp + 0.05) ? 1 : 0, head: panic ? 6 : 12 });
    gph.scr.setAttribute('fill', '#ffe4ee');
    send.update(lt, L(P.D4) - 0.25, [tPress], tPress + 0.6);
    gchat.update(lt);
    setGrade(top, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(top);
  const bot = new Shot(A, B, [['far', 0.35, 1.5], ['mid', 1, 0]]);
  bot.root.style.clipPath = 'inset(50% 0 0 0)'; bot.grade = 'saturate(1.08) contrast(1.03)';
  const rset = girlRoom(bot);
  const girl = new Puppet(rset.people, GIRL, bot.L.mid.defs); const rph = phoneProp(girl.prop, '#f07aa8');
  const bear = svg('g', {}, rset.top); teddy(bear, 0, 0, 0.82);
  const rchat = chatPhone(bot.ui, 600, 1010, 430, 700, 'ภูมิ', guyAv());
  rchat.add('text', 'R', -1, { text: 'รอเธอทักอยู่ตั้งนาน' });
  rchat.add('text', 'L', tPress + 0.25, { text: 'กินข้าวยัง' });
  tSpam.forEach(ts => rchat.add('custom', 'L', ts + 0.15, { html: bearHugSVG(120) }));
  const rival = rivalBanner(bot.ui, 1000);
  const fx2 = fxSvg(bot);
  const hearts = heartsRise(fx2, 320, 1350, tSpam[2] + 0.3, 8, 91, 0.3);
  const leak = lightLeak(bot.fx);
  bot.update = lt => {
    bot.cam({ x: 344, y: -365, z: 1.1, fx: 600, fy: 1000 });
    rset.update(lt + 8);
    const laugh = lt > tSpam[1];
    const pose = girlPose(girl, lt, { smile: 1, grin: laugh ? 1 : 0, eyes: laugh ? 0 : null, kick: laugh ? 1 : 0 });
    rph.scr.setAttribute('fill', '#ffe4ee');
    const [bx, by] = toWorld(pose, ...torsoPt(pose, 40, -RIG.T + 96));
    bear.setAttribute('transform', `translate(${bx.toFixed(1)},${by.toFixed(1)}) rotate(${(-8 + Math.sin(lt * 3) * 3).toFixed(1)})`);
    rchat.update(lt);
    rival.update(lt, tRival, tSpam[2] + 0.4);
    hearts(lt); leak(lt, 0.2 + 0.3 * prog(lt, tSpam[2], tSpam[2] + 1));
    setGrade(bot, (1 - prog(lt, 0, 0.3)) * 8);
  };
  SHOTS.push(bot);
  const seam = new Shot(A, B, []);
  const line = html('div', '', seam.ui); Object.assign(line.style, { position: 'absolute', left: 0, right: 0, top: '954px', height: '12px', background: 'linear-gradient(90deg,#ffd66b,#f07aa8,#ffd66b)', boxShadow: '0 0 24px rgba(255,214,107,.8)' });
  seam.update = lt => { line.style.opacity = (0.75 + 0.25 * Math.sin(lt * 5)).toFixed(3); };
  SHOTS.push(seam);
})();

// =====================================================================
// S8 — end card
// =====================================================================
(() => {
  const [A, B] = SC.s8;
  const S = new Shot(A, B, [['bg', 1, 0]]);
  S.fadeIn = 0.35;
  const G = S.L.bg;
  svg('rect', { x: 0, y: 0, width: 1080, height: 1920, fill: rad2(G.defs, [[0, '#7a3f62'], [0.6, '#36203d'], [1, '#1a1020']], { cx: 0.5, cy: 0.42, r: 0.8 }) }, G.s);
  const bok = floaters(G.s, [0, 0, 1080, 1920], 22, 143, { color: '#ffd9e6', rMin: 10, rMax: 34, speed: 14, op: 0.2, base: 0.04, amp: 26, filter: blurFilter(G.defs, 4) });
  const leak = lightLeak(S.fx);
  const fxs = fxSvg(S);
  const wrap = html('div', '', S.ui); wrap.style.cssText = 'position:absolute;inset:0';
  const icon = html('div', 'title', wrap); icon.style.top = '330px'; icon.innerHTML = bearHugSVG(250);
  const t1 = html('div', 'title', wrap); t1.style.top = '640px'; t1.style.font = '700 170px/1 Kanit';
  const digits = ['4', '7'].map(d => html('span', 'tdig', t1, d));
  const unit = html('span', 'tdig', t1, 'ครั้ง'); unit.style.marginLeft = '0.25em'; unit.style.fontSize = '110px';
  const t2 = html('div', 'title', wrap, 'ที่ลบข้อความ'); t2.style.top = '840px'; t2.style.font = '600 104px/1 Kanit';
  const sub = html('div', 'title', wrap, 'กล้าทักสักครั้ง อาจมีคนรออยู่'); sub.style.top = '1010px'; sub.style.font = '500 50px/1.3 Kanit'; sub.style.color = '#ffd166';
  const cta = html('div', 'cta', wrap); cta.style.top = '1140px';
  cta.innerHTML = `<span class="ics"></span><span>ส่งให้คนที่คุณอยากทัก</span>`;
  const plane = paperPlane(cta.querySelector('.ics'), 64);
  const spark = burst(fxs, 540, 460, 0.3, 18, 153, ['#ffd66b', '#ffffff', '#f07aa8'], 240, 0.9);
  S.update = lt => {
    bok(lt); leak(lt, 0.45);
    popSquash(icon, lt, 0.15, `rotate(${(Math.sin(lt * 2.4) * 5).toFixed(2)}deg)`, -20);
    spark(lt);
    digits.forEach((d, i) => { const t0 = 0.4 + i * 0.1, k = spring(lt, t0, 15, 6); d.style.opacity = fadeIn(lt, t0, 0.08); d.style.transform = `translateY(${((1 - k) * -150).toFixed(1)}px)`; });
    const ku = spring(lt, 0.65, 14, 7); unit.style.opacity = fadeIn(lt, 0.65, 0.15); unit.style.transform = `translateY(${((1 - ku) * 24).toFixed(1)}px)`;
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
const warm = html('div', 'blackout', frame); warm.style.background = '#fff1f4';
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
  warm.style.opacity = (0.85 * Math.max(fl(SC.s1[0]) * 0.8, fl(SC.s2[0]) * 0.6, fl(SC.s4[0]) * 0.7, fl(SC.s5[0]), fl(SC.s6[0]), fl(SC.s7[0]) * 0.7, fl(P.end))).toFixed(3);
};
window.DURATION = DURATION;
window.ready = document.fonts.ready.then(() => true);
