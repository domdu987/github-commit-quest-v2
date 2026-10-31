/* ============================================================
   SHOTS 1–10 — "คอนโดชั้น 23": ฮุก → ลูป 1 (น้ำ)
   ============================================================ */
(() => {
  const { seg, kf, E, clamp, lerp, $, tf, cam, op, show, noise, shake, flicker, fmt, pad2 } = HF;
  const A = ART, P = ART.P;
  const T = id => TIMELINE.clips.find(c => c.id === id);
  const C = (id, i) => CUES.find(c => c.id === id && c.i === i).start;
  const q = (g, sel) => g.querySelector(sel), qa = (g, sel) => [...g.querySelectorAll(sel)];
  Object.assign(window, { T, C, q, qa });

  // ---- ท่าเดิน / ยืน ของตัวละครหุ่นข้อต่อ ----
  window.walkChar = (g, ph, amp = 1) => {
    const s = Math.sin(ph), c = Math.cos(ph);
    q(g, '.legF').setAttribute('transform', `translate(0 -118) rotate(${28 * s * amp})`);
    q(g, '.legB').setAttribute('transform', `translate(0 -118) rotate(${-28 * s * amp})`);
    q(g, '.legF-shin').setAttribute('transform', `translate(0 58) rotate(${Math.max(0, -40 * c) * amp})`);
    q(g, '.legB-shin').setAttribute('transform', `translate(0 58) rotate(${Math.max(0, 40 * c) * amp})`);
    q(g, '.armF').setAttribute('transform', `translate(0 -232) rotate(${-24 * s * amp})`);
    q(g, '.armB').setAttribute('transform', `translate(0 -232) rotate(${24 * s * amp})`);
    q(g, '.head').setAttribute('transform', `translate(4 ${-246 + Math.abs(s) * 3 * amp}) rotate(${2 * s * amp})`);
    q(g, '.torso').setAttribute('transform', `translate(0 ${Math.abs(s) * 3 * amp})`);
  };
  window.idleChar = (g, t) => {
    q(g, '.head').setAttribute('transform', `translate(4 ${-246 + Math.sin(t * 1.6) * 1.5}) rotate(${Math.sin(t * .9) * 1.5})`);
    q(g, '.torso').setAttribute('transform', `translate(0 ${Math.sin(t * 1.6) * 1.5})`);
  };
  window.catIdle = (g, t, sit = true) => {
    q(g, '.cat-tail').setAttribute('transform', `translate(-40 ${sit ? -14 : -40}) rotate(${Math.sin(t * 2.2) * 12})`);
    q(g, '.cat-head').setAttribute('transform', `translate(40 ${(sit ? -84 : -58) + Math.sin(t * 1.3)}) rotate(${Math.sin(t * .6) * 3})`);
    q(g, '.cat-earF').setAttribute('transform', `translate(12 -24) rotate(${Math.sin(t * 3.1) * 5})`);
  };
  window.catTrot = (g, ph) => {
    const s = Math.sin(ph);
    ['.cl1', '.cl2', '.cl3', '.cl4'].forEach((c, i) => q(g, c).setAttribute('transform', `translate(0 -24) rotate(${(i % 2 ? 1 : -1) * 24 * s}) translate(0 24)`));
    q(g, '.cat-tail').setAttribute('transform', `translate(-40 -40) rotate(${Math.sin(ph * .8) * 16 - 20})`);
    q(g, '.cat-head').setAttribute('transform', `translate(40 ${-58 + Math.abs(s) * 2}) rotate(${Math.sin(ph) * 2})`);
  };
  window.dustUpdate = (g, t, box = [0, 0, 720, 1280], speed = 1) => {
    qa(g, '.p').forEach((p, i) => {
      const x = box[0] + ((HF.hash(i) * box[2] + t * 12 * speed * (0.5 + HF.hash(i + 9))) % box[2]);
      const y = box[1] + ((HF.hash(i + 3) * box[3] - t * 18 * speed * (0.5 + HF.hash(i + 5)) + 99999) % box[3]);
      p.setAttribute('cx', x); p.setAttribute('cy', y); p.setAttribute('opacity', 0.25 + 0.35 * (0.5 + 0.5 * Math.sin(t * 2 + i)));
    });
  };
  const chip = (cls, x, y, ic, lb, w = 170) => `<g class="mchip ${cls}" transform="translate(${x} ${y})"><rect x="${-w / 2}" y="-30" width="${w}" height="60" rx="30" fill="${P.cream}" stroke="#2a2622" stroke-width="2"/><g transform="translate(${-w / 2 + 12} -22)">${A.icon(ic, 44)}</g><text x="${14}" y="8" font-family="Kanit" font-weight="600" font-size="21" fill="#2a2622" text-anchor="middle">${lb}</text></g>`;
  window.chip = chip;
  window.popChips = (g, lt, t0, step = 0.25) => qa(g, '.mchip').forEach((c, i) => { const a = seg(lt, t0 + i * step, .35, E.outBack); c.style.opacity = a; const m = c.getAttribute('transform').match(/translate\(([-\d.]+) ([-\d.]+)\)/); c.setAttribute('transform', `translate(${m[1]} ${m[2]}) scale(${a}) rotate(${(1 - a) * -10})`); });

  // ============ ช็อต 1: ฮุก — ระเบียงชั้น 23 มองเมืองตอนโพล้เพล้ ============
  HF.shot({
    id: 'hook', start: 0, end: T('02').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="url(#skyDusk)"/>
        <circle class="sun" cx="520" cy="330" r="60" fill="#ffd08a" opacity=".9"/>
        <g filter="url(#blur3)" opacity=".85" transform="translate(0 560) scale(1.1)">${A.skyline(false, 3)}</g>
        <g transform="translate(0 620)">${A.skyline(false, 1)}</g>
        <g class="smokeg" transform="translate(0 560)">${A.smokeColumns(4)}</g>
        <!-- ถนนด้านล่าง รถติด ไฟท้ายแดง -->
        <rect x="-400" y="660" width="1520" height="400" fill="#2a2a36"/>
        <g class="cars">${Array.from({ length: 70 }, (_, i) => `<rect class="car" x="${-380 + (i * 41) % 1480}" y="${680 + (i % 6) * 40}" width="18" height="10" rx="2" fill="${i % 3 ? '#ff5a4a' : '#ffe9b0'}" opacity=".8"/>`).join('')}</g>
        <!-- เงาซอมบี้บนถนนไกล ๆ -->
        <g class="zombies">${[0, 1, 2, 3, 4, 5].map(i => `<g class="z" transform="translate(${60 + i * 120} 940) scale(.22)">${A.zombie('#1b1620')}</g>`).join('')}</g>
        <!-- ระเบียง -->
        <g transform="translate(360 1000)">${A.balconyRail(1000)}</g>
        <g class="cat" transform="translate(150 1176) scale(.8)">${A.catSide({ sit: true })}</g>
        <g class="po" transform="translate(470 1178) scale(.86)">${A.poSide()}</g>
        <g class="sign" transform="translate(600 820)"><rect x="-70" y="-26" width="140" height="52" rx="10" fill="${P.cream}" stroke="#2a2622" stroke-width="2"/><text y="8" font-family="Kanit" font-weight="700" font-size="24" fill="#2a2622" text-anchor="middle">ชั้น 23</text></g>
        ${A.dust(20)}
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 760, s: kf(lt, [[0, 1.0], [dur, 1.1]], E.inOutSine) });
      idleChar(q(g, '.po'), t); catIdle(q(g, '.cat'), t);
      q(g, '.po .armF').setAttribute('transform', `translate(0 -232) rotate(${-40 + Math.sin(t * 2) * 2})`);
      qa(g, '.z').forEach((z, i) => { z.setAttribute('transform', `translate(${60 + i * 120 - lt * 6 * (1 + i * .1)} 940) scale(.22)`); q(z, '.zarm').setAttribute('transform', `translate(18 -214) rotate(${Math.sin(t * 2 + i) * 8 - 6})`); q(z, '.zhead').setAttribute('transform', `translate(6 -236) rotate(${12 + Math.sin(t * 1.4 + i) * 6})`); });
      qa(g, '.sp').forEach((p, i) => { const j = i % 5; p.setAttribute('cx', j * 6 + Math.sin(t * .8 + i) * 8); p.setAttribute('cy', -j * 40 - (t * 8 % 40) * (j === 4 ? 1 : 0)); });
      qa(g, '.car').forEach((c, i) => c.setAttribute('opacity', 0.5 + 0.4 * (0.5 + 0.5 * Math.sin(t * 5 + i))));
      const sa = seg(lt, 1.0, .4, E.outBack); q(g, '.sign').setAttribute('transform', `translate(600 820) scale(${sa})`);
      dustUpdate(g, t, [0, 300, 720, 800], 0.6);
    }
  });

  // ============ ช็อต 2: โถงลิฟต์ — นิ้วจะกดปุ่มลง + ตรา "อย่า" ============
  HF.shot({
    id: 'rule', start: T('02').start, end: T('03').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.corridor()}
        <g transform="translate(360 1000)">${A.elevatorDoors(0)}</g>
        <g class="panel" transform="translate(620 760) scale(1.4)">${A.callPanel()}</g>
        <g class="hand" transform="translate(560 1120)"><rect x="-40" y="40" width="80" height="260" rx="30" fill="${P.blouse}"/><rect x="-36" y="-40" width="72" height="110" rx="26" fill="${P.skin}"/><rect x="-14" y="-150" width="28" height="130" rx="14" fill="${P.skin}"/><rect x="14" y="-30" width="22" height="70" rx="11" fill="${P.skinD}" opacity=".5"/><rect x="-40" y="-20" width="24" height="60" rx="12" fill="${P.skinD}" opacity=".35"/></g>
        <g class="dnglow" transform="translate(620 816)" opacity="0"><circle r="60" fill="url(#redglow)"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const sh = shake(t, 4 * seg(lt, 0.1, 0.1, E.linear) * (1 - seg(lt, 0.3, 0.6, E.linear)), 40, 1);
      cam(q(g, '.cam'), { x: 560, y: 860, s: kf(lt, [[0, 1.25], [dur, 1.1]], E.outCubic), dx: sh.x, dy: sh.y });
      const reach = kf(lt, [[0, 0], [0.5, 1], [0.7, 0.9], [dur, 0.9]], E.outCubic);
      q(g, '.hand').setAttribute('transform', `translate(${560 + reach * 60} ${1120 - reach * 130}) rotate(${-10 * reach})`);
      q(g, '.dnglow').setAttribute('opacity', seg(lt, 0.45, .2, E.linear) * (0.6 + 0.4 * Math.sin(t * 10)));
      q(g, '.btnDn').setAttribute('fill', lt > 0.45 ? '#ff8a7a' : '#e8eef2');
      qa(g, '.clight').forEach((l, i) => op(l, 0.9 * flicker(t, 22, i, .8)));
    }
  });
  UI.stamp({ start: C('02', 0) + 0.1, end: T('03').start, text: 'อย่า' });
  UI.flash(C('02', 0) + 0.1, 0.1);

  // ============ ช็อต 3: ภาพตัดตึก — ที่ที่รอดได้ดีที่สุด ============
  HF.shot({
    id: 'tower', start: T('03').start, end: T('04a').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#1d2433"/>
        <g filter="url(#blur6)" opacity=".5" transform="translate(0 1100) scale(1.6)">${A.skyline(true, 5)}</g>
        ${A.towerSection({ x: 360, y: 1120, fh: 36 })}
        <g class="chips">${chip('c0', 130, 250, 'tank', 'น้ำ 40,000 ล.', 200)}${chip('c1', 590, 330, 'building', 'สูง 23 ชั้น')}${chip('c2', 130, 560, 'firedoor', 'ประตูหนีไฟ')}${chip('c3', 590, 640, 'stairs', 'บันได 2 ทาง')}</g>
        <g class="warn" transform="translate(360 1103)"><circle r="40" fill="${P.red}"/><circle class="ring" r="40" fill="none" stroke="${P.red}" stroke-width="4"/><text y="14" font-family="Kanit" font-weight="700" font-size="40" fill="#fff" text-anchor="middle">?</text></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const t2 = C('03', 2) - this.start;
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 420], [t2, 560], [dur, 900]], E.inOutCubic), s: kf(lt, [[0, 1.3], [t2, 1.0], [dur, 0.95]], E.inOutCubic) });
      popChips(g, lt, C('03', 1) - this.start);
      q(g, '.fl23').setAttribute('transform', `translate(360 ${1120 - 23 * 36}) scale(${1 + 0.05 * Math.sin(t * 6) * (lt < t2 ? 1 : 0)})`);
      const wa = seg(lt, t2, .4, E.outBack); q(g, '.warn').setAttribute('transform', `translate(360 1103) scale(${wa})`);
      q(g, '.ring').setAttribute('r', 40 + ((t * 60) % 60)); q(g, '.ring').setAttribute('opacity', wa * (1 - ((t * 60) % 60) / 60));
      q(g, '.lobbymark').setAttribute('opacity', seg(lt, t2 + .3, .3, E.linear));
      qa(g, '.fd').forEach((d, i) => d.setAttribute('y', 1120 - ((i * 34 + t * 120) % 860)));
      q(g, '.pumpwheel').setAttribute('transform', `rotate(${t * 240})`);
    }
  });

  // ============ ช็อต 4: ปอเดินไปลิฟต์ + กุญแจรถ ============
  HF.shot({
    id: 'intro', start: T('04a').start, end: T('04b').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.corridor()}
        <g transform="translate(900 1000)">${A.elevatorDoors(0)}</g>
        <g class="cat" transform="translate(-100 1000) scale(.7)">${A.catSide({ sit: false })}</g>
        <g class="po" transform="translate(40 1000) scale(.9)">${A.poSide()}</g>
        <g class="bubble" transform="translate(0 0)" opacity="0"><rect x="-120" y="-60" width="240" height="90" rx="18" fill="${P.cream}" stroke="#2a2622" stroke-width="3"/><path d="M-20 30 l20 26 l20 -26z" fill="${P.cream}"/><g transform="translate(-100 -50)">${A.icon('key', 60)}</g><text x="30" y="-8" font-family="Kanit" font-weight="700" font-size="22" fill="#2a2622" text-anchor="middle">ชั้นใต้ดิน B2</text><text x="30" y="18" font-family="Kanit" font-size="16" fill="${P.inkL}" text-anchor="middle">รถจอดอยู่</text></g>
        ${A.dust(14)}
      </g>`;
    },
    update(lt, g, t, dur) {
      const walk = clamp(lt / (dur - 0.6)); const x = lerp(40, 560, E.inOutSine(walk));
      const po = q(g, '.po'); po.setAttribute('transform', `translate(${x} 1000) scale(.9)`); walkChar(po, lt * 9, 1 - seg(lt, dur - 0.8, .4, E.linear));
      const cat = q(g, '.cat'); cat.setAttribute('transform', `translate(${x - 150} 1000) scale(.7)`); catTrot(cat, lt * 11);
      cam(q(g, '.cam'), { x: 360 + (x - 300) * .4, y: 800, s: kf(lt, [[0, 1.05], [dur, 1.0]]) });
      const tb = C('04a', 2) - this.start; const ba = seg(lt, tb, .35, E.outBack);
      q(g, '.bubble').setAttribute('opacity', ba); q(g, '.bubble').setAttribute('transform', `translate(${x + 20} 640) scale(${ba})`);
      qa(g, '.clight').forEach((l, i) => op(l, 0.9 * flicker(t, 22, i, .8)));
      dustUpdate(g, t, [0, 400, 720, 700], 0.5);
    }
  });
  UI.nametag({ start: C('04a', 0) + 0.3, end: C('04a', 2) + 0.3, name: 'ปอ', role: 'พนักงานออฟฟิศ · อายุ 27 · ห้อง 2304', avatar: '<svg viewBox="-60 -330 120 120" width="64" height="64">' + A.poSide() + '</svg>' });

  // ============ ช็อต 5: "อย่า." — ตึกมืด จุดแดง 800 จุดไหลลงล็อบบี้ ============
  HF.shot({
    id: 'no', start: T('04b').start, end: T('05').start,
    init(g) {
      this.dots = Array.from({ length: 300 }, (_, i) => ({ f: 1 + Math.floor(HF.hash(i) * 23), x: -150 + HF.hash(i + 77) * 300, d: 0.3 + HF.hash(i + 99) * 0.7 }));
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#07080f"/>
        <g opacity=".35">${A.towerSection({ x: 360, y: 1120, fh: 36 })}</g>
        <g class="lobbyglow" transform="translate(360 1110)"><ellipse rx="280" ry="110" fill="url(#redglow)"/></g>
        <g class="dots">${this.dots.map(() => `<circle class="d" r="3.5" fill="#ff6a5a"/>`).join('')}</g>
        <g transform="translate(360 1110)"><rect x="-70" y="-18" width="140" height="36" rx="18" fill="${P.red}"/><text y="7" font-family="Kanit" font-weight="600" font-size="20" fill="#fff" text-anchor="middle">ล็อบบี้</text></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const sh = shake(t, 10 * (1 - seg(lt, 0, 0.6, E.linear)), 35, 2);
      cam(q(g, '.cam'), { x: 360, y: 760, s: kf(lt, [[0, 1.3], [0.5, 1.0]], E.outExpo), dx: sh.x, dy: sh.y });
      const k = seg(lt, 0.1, dur - 0.3, E.inQuad);
      qa(g, '.d').forEach((d, i) => { const o = this.dots[i]; const fy = 1120 - o.f * 36 + 18; const y = lerp(fy, 1110, clamp(k * 1.4 - (1 - o.d) * 0.4)); d.setAttribute('cx', 360 + o.x * (1 - clamp(k * 1.4 - (1 - o.d) * 0.4)) * 0.9 + Math.sin(t * 6 + i) * 3); d.setAttribute('cy', y); d.setAttribute('opacity', 0.5 + 0.5 * Math.sin(t * 7 + i)); });
      q(g, '.lobbyglow').setAttribute('opacity', 0.4 + 0.6 * k);
    }
  });
  UI.stamp({ start: T('04b').start + 0.02, end: T('04b').end + 0.35, text: 'อย่า' });
  UI.red(T('04b').start, T('04c').start, 1); UI.flash(T('04b').start + 0.02, 0.14);

  // ============ ช็อต 6: ล็อบบี้ 800 คน ============
  HF.shot({
    id: 'lobby', start: T('04c').start, end: T('05').start,
    init(g) {
      const cols = ['#3a3f4a', '#5b4a6b', '#2f5a4a', '#6b3a3a', '#3a4f6b', '#4a4a3a'];
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#2b2f3a"/>
        <rect x="-400" y="-100" width="1520" height="800" fill="#d9d2c2"/>
        <rect x="-400" y="300" width="1520" height="400" fill="#9ad2e6" opacity=".4"/>
        <g class="stairsL" transform="translate(-40 700)">${[0, 1, 2, 3, 4, 5].map(i => `<rect x="${-i * 40}" y="${-i * 40 - 40}" width="40" height="40" fill="#c9bda8"/>`).join('')}</g>
        <rect x="-400" y="700" width="1520" height="700" fill="#b9ad98"/>
        <g class="crowd">${Array.from({ length: 60 }, (_, i) => `<g class="pc" transform="translate(${-60 + (i * 97) % 840} ${760 + (i * 53) % 420}) scale(${0.5 + ((i * 53) % 420) / 700})">${A.personFront(cols[i % 6])}</g>`).join('')}</g>
        <g class="doors" transform="translate(360 700)"><rect x="-200" y="-400" width="400" height="400" fill="#7fbfd8" opacity=".6"/><rect x="-6" y="-400" width="12" height="400" fill="#2a2f36"/><rect x="-200" y="-400" width="400" height="400" fill="none" stroke="#2a2f36" stroke-width="10"/><g class="zout">${[0, 1, 2].map(i => `<g transform="translate(${-120 + i * 120} -10) scale(.55)">${A.zombie('#1b2a1f')}</g>`).join('')}</g></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 800, s: kf(lt, [[0, 1.0], [dur, 1.15]], E.inOutSine) });
      qa(g, '.pc').forEach((p, i) => { const m = p.getAttribute('transform').match(/translate\(([-\d.]+) ([-\d.]+)\) scale\(([\d.]+)\)/); const a = seg(lt, i * 0.03, .25, E.outBack); p.setAttribute('transform', `translate(${m[1]} ${+m[2] + Math.sin(t * 9 + i) * 4}) scale(${m[3]})`); p.setAttribute('opacity', a); });
      qa(g, '.zout g.zombie').forEach((z, i) => { q(z, '.zarm').setAttribute('transform', `translate(18 -214) rotate(${Math.sin(t * 2 + i) * 8 - 6})`); });
    }
  });
  UI.hud({ start: C('04c', 0) + 0.4, end: T('05').start, icon: A.icon('people', 34), label: 'ลูกบ้านกำลังลงล็อบบี้', value: t => fmt(Math.round(800 * seg(t, C('04c', 0) + 0.4, 1.3, E.outExpo))), unit: 'คน', cls: 'red' });

  // ============ ช็อต 7: นาฬิกา — แผงไฟสำรอง + ลิฟต์ลงทีละชั้น ============
  HF.shot({
    id: 'clock', start: T('05').start, end: T('06').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.corridor()}
        <g transform="translate(360 1000)">${A.elevatorDoors(0)}</g>
        <g class="po" transform="translate(150 1010) scale(.8)">${A.poSide()}</g>
        <g class="cat" transform="translate(60 1012) scale(.6)">${A.catSide({ sit: true })}</g>
        <g class="breaker" transform="translate(620 560)"><rect x="-70" y="-90" width="140" height="180" rx="8" fill="#2a2f36"/><rect x="-60" y="-80" width="120" height="160" rx="6" fill="#3a4049"/><text y="-50" font-family="Kanit" font-weight="600" font-size="14" fill="#f6efe0" text-anchor="middle">ไฟสำรอง</text><rect x="-40" y="-36" width="80" height="22" rx="4" fill="#0d0f14"/><text class="pct" y="-20" font-family="Kanit" font-weight="700" font-size="16" fill="#2bd46b" text-anchor="middle">100%</text>${[0, 1, 2].map(i => `<circle class="bl${i}" cx="${-30 + i * 30}" cy="20" r="8" fill="#2bd46b"/>`).join('')}<rect x="-20" y="40" width="40" height="30" rx="4" fill="#d7342c"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 400, y: 820, s: kf(lt, [[0, 1.0], [dur, 1.15]], E.inOutSine) });
      idleChar(q(g, '.po'), t); catIdle(q(g, '.cat'), t);
      q(g, '.floorno').textContent = Math.max(1, 23 - Math.floor(lt * 2.4));
      q(g, '.arrow').setAttribute('opacity', 1); q(g, '.arrow').setAttribute('transform', `translate(42 -360) rotate(180)`);
      const dim = seg(lt, 0, dur, E.linear);
      qa(g, '.clight').forEach((l, i) => op(l, (0.9 - 0.5 * dim) * flicker(t, 22 + i * 7, i, 0.6)));
      q(g, '.emlight').setAttribute('opacity', seg(lt, 0.5, .3, E.linear)); q(g, '.em1').setAttribute('opacity', Math.floor(t * 2) % 2); q(g, '.em2').setAttribute('opacity', 1 - Math.floor(t * 2) % 2);
      q(g, '.pct').textContent = Math.round(100 - lt * 6) + '%'; q(g, '.pct').setAttribute('fill', lt > 2 ? '#ff5a4a' : '#2bd46b');
      [0, 1, 2].forEach(i => q(g, '.bl' + i).setAttribute('fill', lt > 1 + i * 1.2 ? '#5a1a1a' : '#2bd46b'));
    }
  });
  const clockStart = C('05', 0) + 0.3;
  const clockStr = t => { const left = 15 * 60 - (t - clockStart); return `${pad2(left / 60)}:${pad2(left % 60)}`; };
  window.clockStr = clockStr; window.clockStart = clockStart;
  UI.hud({ start: clockStart, end: T('06').start, icon: A.icon('clock', 34), label: 'ไฟสำรองตัดลิฟต์ใน', value: clockStr, cls: 'red' });

  // ============ ช็อต 8: ภาพตัดตึก — ปั๊มส่งน้ำขึ้นแท็งก์ / ไฟดับ ============
  HF.shot({
    id: 'water', start: T('06').start, end: C('06', 6),
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#1d2433"/>
        <g filter="url(#blur6)" opacity=".5" transform="translate(0 1100) scale(1.6)">${A.skyline(true, 5)}</g>
        ${A.towerSection({ x: 360, y: 1120, fh: 36 })}
        <g class="boltg" transform="translate(240 1156)" opacity="0">${A.icon('bolt', 60)}</g>
        <g class="tanklabel" transform="translate(360 150)" opacity="0"><rect x="-150" y="-46" width="300" height="78" rx="12" fill="${P.cream}" stroke="#2a2622" stroke-width="3"/><text class="tl1" y="-6" font-family="Kanit" font-weight="700" font-size="34" fill="#2a2622" text-anchor="middle">40,000 ลิตร</text><text class="tl2" y="22" font-family="Kanit" font-weight="600" font-size="18" fill="${P.inkL}" text-anchor="middle">น้ำทั้งหมดที่เหลือของตึก</text></g>
        <g class="darkmask" opacity="0"><rect x="-400" y="-100" width="1520" height="1700" fill="#05060c"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const tOff = C('06', 3) - this.start, tNum = C('06', 5) - this.start;
      const cy = kf(lt, [[0, 1000], [1.4, 1000], [3.2, 300], [tNum, 300], [tNum + 0.6, 260]], E.inOutCubic);
      const s = kf(lt, [[0, 1.15], [1.4, 1.15], [3.2, 1.0], [tNum, 1.0], [tNum + 0.6, 1.3]], E.inOutCubic);
      cam(q(g, '.cam'), { x: 360, y: cy, s });
      const power = lt < tOff ? 1 : 0;
      qa(g, '.fd').forEach((d, i) => { d.setAttribute('y', 1120 - ((i * 34 + (power ? t * 160 : 0)) % 860)); d.setAttribute('opacity', power ? 1 : 0.12); });
      q(g, '.pumpwheel').setAttribute('transform', `rotate(${power ? t * 240 : 0})`); q(g, '.pled').setAttribute('fill', power ? '#2bd46b' : '#5a1a1a');
      q(g, '.boltg').setAttribute('opacity', seg(lt, 0.3, .3, E.outBack) * (power ? 0.7 + 0.3 * flicker(t, 18, 2, .6) : 0.1));
      q(g, '.darkmask').setAttribute('opacity', 0.5 * seg(lt, tOff, 0.25, E.outExpo) * (0.9 + 0.1 * flicker(t, 30, 5, .7)));
      const la = seg(lt, tNum - 0.3, .35, E.outBack); q(g, '.tanklabel').setAttribute('opacity', la); q(g, '.tanklabel').setAttribute('transform', `translate(360 150) scale(${la})`);
      q(g, '.tanktxt').setAttribute('opacity', 1 - la);
    }
  });
  UI.chips({ start: C('06', 1), end: C('06', 6), offAt: C('06', 3), items: [{ ic: A.icon('bolt', 32), lb: 'ไฟฟ้า' }, { ic: A.icon('gauge', 32), lb: 'ปั๊มน้ำ' }, { ic: A.icon('tank', 32), lb: 'แท็งก์ดาดฟ้า' }], state: t => t < C('06', 3) ? ['on', 'on', 'on'] : ['off', 'off', 'off'] });
  UI.flash(C('06', 3), 0.08);

  // ============ ช็อต 9: ห้องน้ำ — เปิดน้ำใส่อ่าง ถัง ขวด ============
  HF.shot({
    id: 'fill', start: C('06', 6), end: T('07').start,
    init(g) { g.innerHTML = `<g class="cam">${A.bathroom()}<g class="po" transform="translate(640 1180) scale(-.75 .75)">${A.poSide()}</g>${A.dust(10)}</g>`; },
    update(lt, g, t, dur) {
      const t7 = C('06', 7) - this.start;
      cam(q(g, '.cam'), { x: kf(lt, [[0, 360], [t7, 360], [t7 + 0.6, 420]]), y: kf(lt, [[0, 820], [t7, 820], [t7 + 0.6, 1000]]), s: kf(lt, [[0, 1.0], [t7, 1.05], [t7 + 0.6, 1.3]]) });
      const k = seg(lt, 0.2, dur - 0.5, E.linear);
      q(g, '.tublvl').setAttribute('y', -k * 120); q(g, '.tubwave').setAttribute('opacity', k > 0.05 ? .6 : 0); q(g, '.tubwave').setAttribute('transform', `translate(${Math.sin(t * 2) * 10} ${-k * 120 + 20})`);
      q(g, '.stream').setAttribute('height', 100 + k * 90); q(g, '.stream').setAttribute('width', 10 + Math.sin(t * 20) * 2);
      qa(g, '.bucket .lvl').forEach((l, i) => { const kk = seg(lt, 0.6 + i * 0.5, 1.6, E.outCubic); l.setAttribute('y', -kk * 126); l.setAttribute('height', kk * 126); });
      qa(g, '.bt').forEach((b, i) => { const a = seg(lt, t7 + i * 0.15, .3, E.outBack); const m = b.getAttribute('transform').match(/translate\(([-\d.]+) ([-\d.]+)\)/); b.setAttribute('transform', `translate(${m[1]} ${m[2]}) scale(${a})`); const kk = seg(lt, t7 + 0.3 + i * 0.15, 1.0, E.outCubic); q(b, '.lvl').setAttribute('y', -2 - kk * 64); q(b, '.lvl').setAttribute('height', kk * 64); });
      const po = q(g, '.po'); idleChar(po, t); q(po, '.armF').setAttribute('transform', `translate(0 -232) rotate(${-70 + Math.sin(t * 3) * 4})`);
    }
  });
  UI.hud({ start: C('06', 6) + 0.2, end: T('07').start, icon: A.icon('water', 34), label: 'น้ำที่เก็บได้', value: t => fmt(Math.round(300 * seg(t, C('06', 6) + 0.2, T('07').start - C('06', 6) - 0.6, E.outQuad))), unit: 'ลิตร', cls: 'green' });

  // ============ ช็อต 10: จุดพลิก — ทั้งตึกเปิดน้ำพร้อมกัน ============
  HF.shot({
    id: 'alltaps', start: T('07').start, end: C('07', 2),
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#1d2433"/>
        <g filter="url(#blur6)" opacity=".5" transform="translate(0 1100) scale(1.6)">${A.skyline(true, 5)}</g>
        ${A.towerSection({ x: 360, y: 1120, fh: 36 })}
        <g class="tapicons">${Array.from({ length: 23 }, (_, i) => [0, 1, 2].map(k => `<g class="ti" transform="translate(${250 + k * 110} ${1120 - (i + 1) * 36 + 4})" opacity="0">${A.icon('water', 28)}</g>`).join('')).join('')}</g>
        <g class="darkmask"><rect x="-400" y="-100" width="1520" height="1700" fill="#05060c" opacity=".35"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 900], [dur, 500]], E.inOutSine), s: kf(lt, [[0, 1.0], [dur, 0.95]]) });
      qa(g, '.ti').forEach((e, i) => { const a = seg(lt, 0.4 + HF.hash(i) * (dur - 1.2), .25, E.outBack); e.setAttribute('opacity', a); });
      qa(g, '.fd').forEach((d, i) => d.setAttribute('opacity', 0.12));
      q(g, '.tanklvl').setAttribute('y', 20 + seg(lt, 0.4, dur, E.linear) * 20);
      q(g, '.pled').setAttribute('fill', '#5a1a1a');
    }
  });
  UI.hud({ start: T('07').start, end: C('07', 2), icon: A.icon('clock', 34), label: 'ไฟสำรองตัดลิฟต์ใน', value: clockStr, cls: 'red' });
  UI.hud({ start: C('07', 1), end: C('07', 2), icon: A.icon('tap', 34), label: 'ห้องที่เปิดน้ำพร้อมกัน', value: t => fmt(Math.round(400 * seg(t, C('07', 1), 1.3, E.outExpo))), unit: 'ห้อง', cls: 'red' });
})();
