/* ============================================================
   SHOTS 11–20 — แรงดันน้ำ → นับของ → ค้ำประตู → ลิฟต์ตัวที่ 3 → การ์ดจบ
   ============================================================ */
(() => {
  const { seg, kf, E, clamp, lerp, cam, op, shake, flicker, fmt, pad2 } = HF;
  const A = ART, P = ART.P;

  // ============ ช็อต 11: ก๊อกชั้น 23 — แรงดันตก น้ำหยุดไหล ============
  HF.shot({
    id: 'pressure', start: C('07', 2), end: T('08').start,
    init(g) { g.innerHTML = `<g class="cam">${A.tapClose()}<g class="fl" transform="translate(160 300)"><rect x="-110" y="-30" width="220" height="60" rx="30" fill="${P.cream}" stroke="#2a2622" stroke-width="3"/><g transform="translate(-98 -22)">${A.icon('building', 44)}</g><text x="20" y="9" font-family="Kanit" font-weight="700" font-size="24" fill="#2a2622" text-anchor="middle">ชั้น 23</text></g></g>`; },
    update(lt, g, t, dur) {
      const t3 = C('07', 3) - this.start, t4 = C('07', 4) - this.start;
      cam(q(g, '.cam'), { x: kf(lt, [[0, 360], [t4, 360], [dur, 300]]), y: kf(lt, [[0, 520], [t4, 520], [dur, 560]]), s: kf(lt, [[0, 1.0], [t4, 1.05], [dur, 1.35]], E.inOutCubic) });
      const p = 1 - seg(lt, 0.3, t4, E.inQuad); // แรงดัน 1→0
      q(g, '.needle').setAttribute('transform', `rotate(${lerp(-160, -20, 1 - p) + Math.sin(t * 30) * (1 - p) * 2})`);
      const st = q(g, '.stream'); st.setAttribute('height', lt < t4 ? 400 * p : 0); st.setAttribute('width', 8 + 16 * p); st.setAttribute('x', -300 + 8 * (1 - p));
      qa(g, '.drop').forEach((d, i) => { const k = lt > t4 - 0.5 ? ((t * 0.9 + i * 0.33) % 1) : 0; const on = lt > t4 - 0.5 && lt < t4 + 2.2; d.setAttribute('cy', k * 420); d.setAttribute('opacity', on ? (1 - k) * 0.9 : 0); d.setAttribute('ry', 8 + k * 10); });
      const fa = seg(lt, t3 - 0.2, .35, E.outBack); q(g, '.fl').setAttribute('transform', `translate(160 300) scale(${fa})`);
    }
  });
  UI.hud({ start: C('07', 2), end: T('08').start, icon: A.icon('gauge', 34), label: 'แรงดันน้ำชั้น 23', value: t => Math.round(100 * (1 - seg(t, C('07', 2) + 0.3, C('07', 4) - C('07', 2), E.inQuad))) + '%', cls: 'red' });
  UI.hud({ start: C('07', 4), end: T('08').start, icon: A.icon('clock', 34), label: 'น้ำชั้นนี้หยุดไหลใน', value: t => { const s = 2 * 3600 - (t - C('07', 4)) * 40; return `${pad2(s / 3600)}:${pad2((s % 3600) / 60)}:${pad2(s % 60)}`; }, cls: 'red' });

  // ============ ช็อต 12: นับของ — 800 คน / บันได 2 / ลิฟต์ 3 ============
  HF.shot({
    id: 'count', start: T('08').start, end: C('08', 4),
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#1d2433"/>
        <g filter="url(#blur6)" opacity=".5" transform="translate(0 1100) scale(1.6)">${A.skyline(true, 5)}</g>
        ${A.towerSection({ x: 360, y: 1120, fh: 36 })}
        <g class="ppl">${Array.from({ length: 23 }, (_, i) => [0, 1, 2, 3, 4, 5].map(k => `<g class="pp" transform="translate(${215 + k * 58} ${1120 - (i + 1) * 36 + 6})" opacity="0">${A.icon('people', 24)}</g>`).join('')).join('')}</g>
        <g class="stairs"><rect class="sL" x="140" y="${1120 - 23 * 36}" width="34" height="${23 * 36}" fill="${P.orange}" opacity="0"/><rect class="sR" x="546" y="${1120 - 23 * 36}" width="34" height="${23 * 36}" fill="${P.orange}" opacity="0"/>${[140, 546].map(x => Array.from({ length: 46 }, (_, i) => `<rect class="st" x="${x + 4}" y="${1120 - 23 * 36 + i * 18}" width="26" height="2" fill="#4a2a0a" opacity="0"/>`).join('')).join('')}</g>
        <g class="lifts">${[0, 1, 2].map(k => `<g class="lf" transform="translate(${300 + k * 60} ${1120 - 23 * 36 - 50})" opacity="0">${A.icon('elevator', 48)}<rect x="-4" y="50" width="56" height="${23 * 36}" fill="${P.steel}" opacity=".35"/></g>`).join('')}</g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const t1 = C('08', 1) - this.start, t2 = C('08', 2) - this.start, t3 = C('08', 3) - this.start;
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 700], [dur, 620]], E.inOutSine), s: kf(lt, [[0, 1.05], [dur, 1.0]]) });
      qa(g, '.pp').forEach((e, i) => e.setAttribute('opacity', seg(lt, t1 + HF.hash(i) * 1.2, .2, E.outBack)));
      const sa = seg(lt, t2, .4, E.outBack); qa(g, '.sL,.sR').forEach(e => e.setAttribute('opacity', sa * .9)); qa(g, '.st').forEach(e => e.setAttribute('opacity', sa));
      qa(g, '.lf').forEach((e, i) => e.setAttribute('opacity', seg(lt, t3 + i * 0.15, .3, E.outBack)));
      qa(g, '.fd').forEach(d => d.setAttribute('opacity', 0.1)); q(g, '.pled').setAttribute('fill', '#5a1a1a');
    }
  });
  UI.hud({ start: C('08', 1), end: T('09').start, icon: A.icon('people', 34), label: 'ลูกบ้านทั้งตึก', value: t => fmt(Math.round(800 * seg(t, C('08', 1), 1.2, E.outExpo))), unit: 'คน' });
  UI.hud({ start: C('08', 2), end: T('09').start, icon: A.icon('stairs', 34), label: 'บันไดหนีไฟ', value: t => Math.min(2, Math.floor((t - C('08', 2)) / 0.3) + 1), unit: 'ทาง' });
  UI.hud({ start: C('08', 3), end: T('09').start, icon: A.icon('elevator', 34), label: 'ลิฟต์', value: t => Math.min(3, Math.floor((t - C('08', 3)) / 0.15) + 1), unit: 'ตัว' });

  // ============ ช็อต 13: แมวส้มร้องที่ประตู ============
  HF.shot({
    id: 'meow', start: C('08', 4), end: T('09').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.corridor()}
        <g class="shadowz" transform="translate(1000 1000) scale(.9)" opacity=".0">${A.zombie('#2a2622')}</g>
        <g class="cat" transform="translate(300 1130) scale(1.5)">${A.catSide({ sit: true })}</g>
        <g class="meowfx" transform="translate(470 920)" opacity="0"><path d="M0 -40 q40 -30 70 0 M10 0 q40 -20 80 0 M0 40 q40 30 70 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/><g class="tag" transform="translate(150 -60) rotate(-8)"><rect x="-80" y="-40" width="160" height="78" rx="14" fill="${P.yellow}"/><text y="18" font-family="Kanit" font-weight="700" font-size="50" fill="#2a2622" text-anchor="middle">แมว!</text></g></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const sh = shake(t, 2, 30, 11);
      cam(q(g, '.cam'), { x: 380, y: 900, s: kf(lt, [[0, 1.1], [dur, 1.02]], E.outCubic), dx: sh.x, dy: sh.y });
      const m = 0.5 + 0.5 * Math.sin(t * 18); const cat = q(g, '.cat');
      q(cat, '.cat-mouth').setAttribute('transform', `translate(25 10) scale(1 ${1 + 2.5 * m})`);
      q(cat, '.cat-head').setAttribute('transform', `translate(40 ${-84 - 6 * m}) rotate(${-10 - 6 * m})`);
      q(cat, '.cat-earF').setAttribute('transform', `translate(12 -24) rotate(${-20 * m})`); q(cat, '.cat-earB').setAttribute('transform', `translate(-16 -22) rotate(${16 * m})`);
      q(cat, '.cat-tail').setAttribute('transform', `translate(-40 -14) rotate(${Math.sin(t * 9) * 20})`);
      const fa = seg(lt, 0.3, .25, E.outBack); const fx = q(g, '.meowfx'); fx.setAttribute('opacity', fa * (0.6 + 0.4 * m)); fx.setAttribute('transform', `translate(470 920) scale(${0.9 + 0.15 * m})`);
      q(g, '.tag').setAttribute('transform', `translate(150 -60) rotate(${-8 + Math.sin(t * 18) * 4}) scale(${1 + 0.1 * m})`);
      const zx = 1000 - seg(lt, 0.2, dur, E.linear) * 300; q(g, '.shadowz').setAttribute('transform', `translate(${zx} 1000) scale(.9)`); q(g, '.shadowz').setAttribute('opacity', 0.35 * seg(lt, 0.2, .5, E.linear));
      q(g, '.shadowz .zarm').setAttribute('transform', `translate(18 -214) rotate(${Math.sin(t * 2) * 8 - 6})`);
      qa(g, '.clight').forEach((l, i) => op(l, 0.35 * flicker(t, 22, i, .6))); q(g, '.emlight').setAttribute('opacity', 1); q(g, '.em1').setAttribute('opacity', Math.floor(t * 2) % 2); q(g, '.em2').setAttribute('opacity', 1 - Math.floor(t * 2) % 2);
    }
  });
  UI.hud({ start: C('08', 4) + 0.2, end: T('09').start, icon: A.icon('cat', 34), label: 'แมวส้ม', value: '1', unit: 'ตัว · ร้องทุกเสียง', cls: 'red' });

  // ============ ช็อต 14: ลากตู้เหล็กค้ำประตูหนีไฟ ============
  HF.shot({
    id: 'block', start: T('09').start, end: C('09', 2),
    init(g) { g.innerHTML = `<g class="cam">${A.fireDoorScene()}<g class="po" transform="translate(-320 1000) scale(.85)">${A.poSide()}</g><g class="lockicon" transform="translate(560 700)" opacity="0"><circle r="46" fill="${P.green}"/><g transform="translate(-24 -24)">${A.icon('lock', 48)}</g></g>${A.dust(10)}</g>`; },
    update(lt, g, t, dur) {
      const k = seg(lt, 0.2, dur - 0.9, E.inOutSine); const cx = lerp(-200, 380, k);
      q(g, '.cabinet').setAttribute('transform', `translate(${cx} ${1000 + Math.sin(k * 60) * 2 * (k < 1 ? 1 : 0)})`);
      qa(g, '.sc').forEach((s, i) => s.setAttribute('opacity', k > 0.1 ? .6 : 0));
      const po = q(g, '.po'); po.setAttribute('transform', `translate(${cx - 130} 1000) scale(.85)`); walkChar(po, lt * 7, k < 1 ? 1 : 0);
      q(po, '.armF').setAttribute('transform', `translate(0 -232) rotate(-80)`); q(po, '.armB').setAttribute('transform', `translate(0 -232) rotate(-70)`);
      const hit = seg(lt, dur - 0.9, 0.08, E.linear) * (1 - seg(lt, dur - 0.8, 0.4, E.linear)); const sh = shake(t, 6 * hit, 40, 5);
      cam(q(g, '.cam'), { x: kf(lt, [[0, 300], [dur, 460]], E.inOutSine), y: 820, s: kf(lt, [[0, 1.0], [dur, 1.1]]), dx: sh.x, dy: sh.y });
      const la = seg(lt, dur - 0.85, .35, E.outBack); q(g, '.lockicon').setAttribute('opacity', la); q(g, '.lockicon').setAttribute('transform', `translate(560 700) scale(${la})`);
      qa(g, '.clight').forEach((l, i) => op(l, 0.3 * flicker(t, 22, i, .6))); q(g, '.emlight').setAttribute('opacity', 1); q(g, '.em1').setAttribute('opacity', Math.floor(t * 2) % 2); q(g, '.em2').setAttribute('opacity', 1 - Math.floor(t * 2) % 2);
      dustUpdate(g, t, [0, 500, 720, 600], 0.5);
    }
  });
  UI.hud({ start: C('09', 1), end: C('09', 4), icon: A.icon('firedoor', 34), label: 'ประตูหนีไฟค้ำแล้ว', value: t => Math.min(2, Math.floor((t - C('09', 1)) / 0.5) + 1), unit: 'ฝั่ง', cls: 'green' });

  // ============ ช็อต 15: ลิฟต์ 2 ตัวค้างเปิดที่ชั้น 23 ============
  HF.shot({
    id: 'holdlift', start: C('09', 2), end: C('09', 4),
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.corridor()}
        <g class="l1" transform="translate(60 1000) scale(.8)">${A.elevatorDoors(0)}</g>
        <g class="l2" transform="translate(360 1000) scale(.8)">${A.elevatorDoors(0)}</g>
        <g class="l3" transform="translate(660 1000) scale(.8)">${A.elevatorDoors(0)}</g>
        <g class="cat" transform="translate(200 1010) scale(.55)">${A.catSide({ sit: true })}</g>
        <g class="po" transform="translate(500 1004) scale(.7)">${A.poSide()}</g>
        ${[60, 360].map((x, i) => `<g class="holdtag t${i}" transform="translate(${x} 640)" opacity="0"><rect x="-70" y="-24" width="140" height="48" rx="24" fill="${P.green}"/><text y="8" font-family="Kanit" font-weight="700" font-size="20" fill="#fff" text-anchor="middle">ค้างเปิด</text></g>`).join('')}
        <g class="qtag" transform="translate(660 640)" opacity="0"><rect x="-40" y="-24" width="80" height="48" rx="24" fill="${P.red}"/><text y="9" font-family="Kanit" font-weight="700" font-size="26" fill="#fff" text-anchor="middle">?</text></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 820, s: kf(lt, [[0, 1.0], [dur, 1.08]], E.inOutSine) });
      [0, 1].forEach(i => { const o = seg(lt, 0.3 + i * 0.6, 0.8, E.inOutCubic); const l = q(g, '.l' + (i + 1)); q(l, '.doorL').setAttribute('x', -140 - o * 130); q(l, '.doorL2').setAttribute('x', -140 - o * 130); q(l, '.doorR').setAttribute('x', o * 130); q(l, '.doorR2').setAttribute('x', o * 130); q(l, '.shaft').setAttribute('opacity', 1); const ta = seg(lt, 0.9 + i * 0.6, .3, E.outBack); const tg = q(g, '.t' + i); tg.setAttribute('opacity', ta); tg.setAttribute('transform', `translate(${[60, 360][i]} 640) scale(${ta})`); });
      q(g, '.l3 .floorno').textContent = '1';
      const qa_ = seg(lt, dur - 0.9, .3, E.outBack); q(g, '.qtag').setAttribute('opacity', qa_); q(g, '.qtag').setAttribute('transform', `translate(660 640) scale(${qa_})`);
      idleChar(q(g, '.po'), t); catIdle(q(g, '.cat'), t);
      qa(g, '.clight').forEach((l, i) => op(l, 0.3 * flicker(t, 22, i, .6))); q(g, '.emlight').setAttribute('opacity', 1);
    }
  });
  UI.hud({ start: C('09', 2) + 0.9, end: C('09', 4), icon: A.icon('elevator', 34), label: 'ลิฟต์ค้างเปิดชั้น 23', value: t => Math.min(2, Math.floor((t - C('09', 2) - 0.9) / 0.6) + 1), unit: 'ตัว', cls: 'green' });

  // ============ ช็อต 16: สมุดจด + การ์ดเสบียง ============
  HF.shot({
    id: 'notebook', start: C('09', 4), end: T('10a').start,
    init(g) { g.innerHTML = `<g class="cam">${A.notebook(['คืนที่ 1 — ห้อง 2304', 'น้ำ ......... 300 ลิตร', 'บะหมี่ ......... 40 ซอง', 'ข้าวสาร ......... 5 กก.', 'ประตูหนีไฟค้ำแล้ว 2 ฝั่ง ✓', 'ลิฟต์ค้างเปิด 2 ตัว ✓', 'อยู่ได้ ~30 วัน'])}</g>`; },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 760], [dur, 700]], E.inOutSine), s: kf(lt, [[0, 1.15], [dur, 1.0]], E.outCubic) });
      q(g, '.torch').setAttribute('opacity', 0.45 + 0.1 * flicker(t, 12, 4, .4));
      const starts = [0.1, C('09', 5) - this.start, C('09', 6) - this.start, C('09', 6) - this.start + 0.6, C('09', 7) - this.start, C('09', 7) - this.start + 0.5, C('09', 7) - this.start + 1.0];
      starts.forEach((s0, i) => { const el = q(g, '.l' + i); const k = seg(lt, s0, 0.55, E.linear); const full = el.dataset.full || (el.dataset.full = el.textContent); el.textContent = full.slice(0, Math.ceil(full.length * k)); });
      let row = 0; starts.forEach((s0, i) => { if (lt >= s0) row = i; }); const k = seg(lt, starts[row], 0.55, E.linear);
      q(g, '.pen').setAttribute('transform', `translate(${-190 + 380 * k} ${-352 + row * 96 + Math.sin(t * 30) * 2})`);
    }
  });
  UI.inventory({ start: C('09', 5) - 0.1, end: T('10a').start, title: 'เสบียง · ห้อง 2304', icon: A.icon('rice', 26), rows: [
    { ic: A.icon('water', 28), label: 'น้ำ', value: k => fmt(Math.round(300 * k)), unit: ' ลิตร', bar: 0.85, at: C('09', 5) },
    { ic: A.icon('noodle', 28), label: 'บะหมี่กึ่งสำเร็จรูป', value: k => Math.round(40 * k), unit: ' ซอง', bar: 0.6, at: C('09', 6) },
    { ic: A.icon('clock', 28), label: 'อยู่ได้ราว', value: k => Math.round(30 * k), unit: ' วัน', bar: 0.75, at: C('09', 7) },
  ] });

  // ============ ช็อต 17: แมวจ้องไปที่โถงลิฟต์ (เงียบ 1 วิ) ============
  HF.shot({
    id: 'catstare', start: T('10a').start, end: T('10b').start,
    init(g) { g.innerHTML = `<g class="cam"><g filter="url(#blur10)">${A.corridor()}<g transform="translate(360 1000)">${A.elevatorDoors(0)}</g></g><g class="dark"><rect x="-400" y="-100" width="1520" height="1700" fill="#05060c" opacity=".6"/></g><g class="face" transform="translate(360 920) scale(1.25)">${A.catFace()}</g></g>`; },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 860, s: kf(lt, [[0, 1.0], [dur, 1.2]], E.inOutSine) });
      const turn = seg(lt, 0.3, 0.6, E.outBack); const f = q(g, '.face');
      q(f, '.earL').setAttribute('transform', `translate(-110 -120) rotate(${-14 * turn})`); q(f, '.earR').setAttribute('transform', `translate(110 -120) rotate(${-26 * turn})`);
      const dil = 8 + 14 * turn; q(f, '.pupilL').setAttribute('rx', dil); q(f, '.pupilR').setAttribute('rx', dil);
      q(f, '.eyeL').setAttribute('transform', `translate(${-62 + 12 * turn} ${-30 - 4 * turn})`); q(f, '.eyeR').setAttribute('transform', `translate(${62 + 12 * turn} ${-30 - 4 * turn})`);
      f.setAttribute('transform', `translate(${360 + 16 * turn} ${920 + Math.sin(t * 1.3) * 2}) rotate(${7 * turn}) scale(1.25)`);
      qa(g, '.clight').forEach((l, i) => op(l, 0.25 * flicker(t, 22, i, .6)));
    }
  });
  UI.fade(T('10a').start - 0.2, T('10a').start + 0.3, 1, 0);

  // ============ ช็อต 18: ลิฟต์ตัวที่ 3 ขยับขึ้นจากชั้น 1 ============
  HF.shot({
    id: 'lift3', start: T('10b').start, end: TIMELINE.endCardStart,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.corridor()}
        <g class="l3" transform="translate(360 1000)">${A.elevatorDoors(0)}</g>
        <g class="cat" transform="translate(130 1012) scale(.6)">${A.catSide({ sit: true })}</g>
        <g class="dark"><rect x="-400" y="-100" width="1520" height="1700" fill="#05060c" opacity=".55"/></g>
        <g class="dispglow" transform="translate(360 650)" opacity="0"><ellipse rx="120" ry="60" fill="url(#redglow)"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const t1 = C('10b', 1) - this.start, t2 = C('10b', 2) - this.start;
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 840], [t1, 820], [t1 + 1.0, 660], [dur, 650]], E.inOutCubic), s: kf(lt, [[0, 1.0], [t1, 1.05], [t1 + 1.0, 2.0], [dur, 2.2]], E.inOutCubic) });
      const moving = lt > t1 + 0.2; const fl = moving ? Math.min(22, 1 + Math.floor((lt - t1 - 0.2) * 2.6)) : 1;
      q(g, '.floorno').textContent = fl; q(g, '.floorno').setAttribute('fill', moving ? '#ff4d3d' : '#7a2a24');
      q(g, '.arrow').setAttribute('opacity', moving ? (Math.floor(t * 3) % 2 ? 1 : 0.3) : 0);
      q(g, '.dispglow').setAttribute('opacity', moving ? 0.5 + 0.3 * Math.sin(t * 6) : 0);
      const cat = q(g, '.cat'); catIdle(cat, t); q(cat, '.cat-head').setAttribute('transform', `translate(40 -84) rotate(${-18 * seg(lt, t1, .5, E.outBack)})`);
      const sh = shake(t, moving ? 1.2 : 0, 25, 8); if (moving) q(g, '.cam').setAttribute('transform', q(g, '.cam').getAttribute('transform') + ` translate(${sh.x} ${sh.y})`);
      qa(g, '.clight').forEach((l, i) => op(l, 0.25 * flicker(t, 22, i, .6))); q(g, '.emlight').setAttribute('opacity', 1); q(g, '.em1').setAttribute('opacity', Math.floor(t * 2) % 2); q(g, '.em2').setAttribute('opacity', 1 - Math.floor(t * 2) % 2);
    }
  });
  UI.fade(TIMELINE.endCardStart - 0.5, TIMELINE.endCardStart, 0, 1);

  // ============ ช็อต 19: การ์ด "ตอนที่ 2" ============
  HF.shot({ id: 'end', start: TIMELINE.endCardStart, end: TIMELINE.total + 1, init(g) { g.innerHTML = '<rect width="720" height="1280" fill="#0b0b0f"/>'; } });
  UI.endcard({ start: TIMELINE.endCardStart, end: TIMELINE.total + 1, title: 'ตอนที่ 2', teaser: 'ใครกดลิฟต์ขึ้นมา และทำไมมันหยุดที่ชั้น 22' });
  UI.fade(TIMELINE.total - 0.6, TIMELINE.total, 0, 1);
})();
