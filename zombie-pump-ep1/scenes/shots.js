/* ============================================================
   SHOTS (ตอนที่ 1/2): ช็อต 1–10  — ฮุก ถึง เครื่องปั่นไฟ
   ทุกช็อต: init(g) สร้าง SVG, update(lt, g, t, dur) ตั้งค่าตามเวลา
   ============================================================ */
(() => {
  const { seg, kf, E, clamp, lerp, $, tf, cam, op, show, noise, shake, flicker, fmt, pad2 } = HF;
  const A = ART, P = ART.P;
  const T = id => TIMELINE.clips.find(c => c.id === id);
  const C = (id, i) => CUES.find(c => c.id === id && c.i === i).start;
  const q = (g, sel) => g.querySelector(sel), qa = (g, sel) => [...g.querySelectorAll(sel)];
  window.T = T; window.C = C; window.q = q; window.qa = qa;

  // ---- ตัวช่วย: ท่าเดินของต้น / หมา ----
  window.walkTon = (g, ph, amp = 1) => {
    const s = Math.sin(ph), c = Math.cos(ph);
    q(g, '.legF') && q(g, '.legF').setAttribute('transform', `translate(0 -118) rotate(${28 * s * amp})`);
    q(g, '.legB') && q(g, '.legB').setAttribute('transform', `translate(0 -118) rotate(${-28 * s * amp})`);
    q(g, '.legF-shin') && q(g, '.legF-shin').setAttribute('transform', `translate(0 58) rotate(${Math.max(0, -40 * c) * amp})`);
    q(g, '.legB-shin') && q(g, '.legB-shin').setAttribute('transform', `translate(0 58) rotate(${Math.max(0, 40 * c) * amp})`);
    q(g, '.armF') && q(g, '.armF').setAttribute('transform', `translate(0 -232) rotate(${-24 * s * amp})`);
    q(g, '.armB') && q(g, '.armB').setAttribute('transform', `translate(0 -232) rotate(${24 * s * amp})`);
    q(g, '.head') && q(g, '.head').setAttribute('transform', `translate(4 ${-246 + Math.abs(s) * 3 * amp}) rotate(${2 * s * amp})`);
    q(g, '.torso') && q(g, '.torso').setAttribute('transform', `translate(0 ${Math.abs(s) * 3 * amp})`);
  };
  window.idleTon = (g, t) => {
    q(g, '.head') && q(g, '.head').setAttribute('transform', `translate(4 ${-246 + Math.sin(t * 1.6) * 1.5}) rotate(${Math.sin(t * .9) * 1.5})`);
    q(g, '.torso') && q(g, '.torso').setAttribute('transform', `translate(0 ${Math.sin(t * 1.6) * 1.5})`);
  };
  window.dogTrot = (g, ph, amp = 1) => {
    const s = Math.sin(ph);
    const L = ['.dl1', '.dl2', '.dl3', '.dl4'];
    L.forEach((c, i) => { const el = q(g, c); if (el) el.setAttribute('transform', `translate(0 -56) rotate(${(i % 2 ? 1 : -1) * 22 * s * amp}) translate(0 56)`); });
    q(g, '.dog-tail') && q(g, '.dog-tail').setAttribute('transform', `translate(-44 -70) rotate(${Math.sin(ph * 1.3) * 14})`);
    q(g, '.dog-head') && q(g, '.dog-head').setAttribute('transform', `translate(50 ${-92 + Math.abs(s) * 2 * amp}) rotate(${Math.sin(ph) * 2 * amp})`);
  };
  window.dogIdle = (g, t) => {
    q(g, '.dog-tail') && q(g, '.dog-tail').setAttribute('transform', `translate(-44 -70) rotate(${Math.sin(t * 5) * 10})`);
    q(g, '.dog-head') && q(g, '.dog-head').setAttribute('transform', `translate(50 ${-92 + Math.sin(t * 1.2)}) rotate(${Math.sin(t * .7) * 2})`);
    q(g, '.dog-earF') && q(g, '.dog-earF').setAttribute('transform', `translate(4 -24) rotate(${Math.sin(t * 2.3) * 4})`);
  };
  window.zombieWalk = (g, ph) => {
    q(g, '.zarm').setAttribute('transform', `translate(18 -214) rotate(${Math.sin(ph) * 8 - 6})`);
    q(g, '.zarm2').setAttribute('transform', `translate(-16 -210) rotate(${Math.cos(ph) * 8})`);
    q(g, '.zhead').setAttribute('transform', `translate(6 -236) rotate(${12 + Math.sin(ph * .7) * 6})`);
  };
  window.dustUpdate = (g, t, box = [0, 0, 720, 1280], speed = 1) => {
    qa(g, '.p').forEach((p, i) => {
      const x = box[0] + ((HF.hash(i) * box[2] + t * 12 * speed * (0.5 + HF.hash(i + 9))) % box[2]);
      const y = box[1] + ((HF.hash(i + 3) * box[3] - t * 18 * speed * (0.5 + HF.hash(i + 5)) + 99999) % box[3]);
      p.setAttribute('cx', x); p.setAttribute('cy', y); p.setAttribute('opacity', 0.25 + 0.35 * (0.5 + 0.5 * Math.sin(t * 2 + i)));
    });
  };

  // ---- ฉากปั๊มกว้าง (ใช้ซ้ำช็อต 1 และ 15) ----
  window.stationWide = (night = false) => `
    <g class="cam">
      ${night ? A.skyNight() : A.skyDusk()}
      <g filter="url(#blur6)" opacity=".9">${A.treeline(600, night ? '#13201c' : '#5a7a48', 16, true)}</g>
      <g filter="url(#blur3)">${A.treeline(640, night ? '#0e1814' : '#466638', 12)}</g>
      <!-- ทางหลวงไกล -->
      <rect x="-400" y="640" width="1520" height="90" fill="${night ? '#1c1f2c' : P.asphalt}"/>
      <rect x="-400" y="680" width="1520" height="4" fill="${P.line}" opacity=".5"/>
      <g class="zombies">${[0, 1, 2, 3].map(i => `<g class="z" transform="translate(${200 + i * 48} 728) scale(.3)">${A.zombie(night ? '#07080c' : '#2a2430')}</g>`).join('')}</g>
      <!-- ร้านสะดวกซื้อด้านหลัง -->
      <g transform="translate(540 840) scale(.72)">${A.shopFront(520, 230)}</g>
      <g transform="translate(120 820) scale(.5)">${A.restroomBlock()}</g>
      <!-- ลานปั๊ม -->
      <rect x="-400" y="840" width="1520" height="600" fill="${night ? '#2a2a33' : P.concrete}"/>
      <rect x="-400" y="840" width="1520" height="8" fill="${night ? '#1a1a22' : P.concreteD}"/>
      <g class="sunshadow" opacity="${night ? 0 : .25}"><ellipse cx="300" cy="1040" rx="120" ry="18" fill="#3a2a1a"/><ellipse cx="520" cy="1030" rx="150" ry="18" fill="#3a2a1a"/></g>
      <rect x="150" y="1000" width="420" height="40" rx="8" fill="${night ? '#1d1d26' : P.concreteD}"/>
      <g transform="translate(250 1002) scale(.95)">${A.dispenser()}</g>
      <g transform="translate(470 1002) scale(.95)">${A.dispenser()}</g>
      <g class="bike" transform="translate(360 1110) scale(.72)">${A.motorbike()}</g>
      <g class="ton" transform="translate(255 1115) scale(.68)">${A.tonSide()}</g>
      <g class="dog" transform="translate(560 1120) scale(.62)">${A.dogSide({ sit: true })}</g>
      <g transform="translate(360 470) scale(1.0)">${A.canopy(900, 5)}</g>
      ${A.dust(26)}
      <g class="nightmask" opacity="0"><rect x="-400" y="-100" width="1520" height="1700" fill="#0a0d1f"/></g>
    </g>`;

  // ============ ช็อต 1: ฮุก — ปั๊มกว้างตอนโพล้เพล้ ============
  HF.shot({
    id: 'hook', start: 0, end: T('02').start,
    init(g) { g.innerHTML = stationWide(false); },
    update(lt, g, t, dur) {
      const s = kf(lt, [[0, 1.0], [dur, 1.12]], E.inOutSine);
      cam(q(g, '.cam'), { x: 370, y: 900, s });
      idleTon(q(g, '.ton'), t); dogIdle(q(g, '.dog'), t);
      q(g, '.ton .armF').setAttribute('transform', `translate(0 -232) rotate(${-55 + Math.sin(t * 2) * 2})`);
      qa(g, '.z').forEach((z, i) => { z.setAttribute('transform', `translate(${330 - i * 42 - lt * 7 * (1 + i * .15)} 728) scale(.3)`); zombieWalk(z, t * 2.2 + i); });
      // ไฟหลังคาติดกะพริบตอน 1.5 วิ
      qa(g, '.clight').forEach((l, i) => { const on = seg(lt, 1.4 + i * .12, .4, E.linear) * flicker(t, 24, i, .85); op(l, on); });
      dustUpdate(g, t, [0, 500, 720, 700]);
      q(g, '.sun').setAttribute('cy', 300 + lt * 3);
    }
  });

  // ============ ช็อต 2: คันเร่ง + ตรา "อย่า" ============
  HF.shot({
    id: 'throttle', start: T('02').start, end: T('03').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <g filter="url(#blur10)">${A.skyDusk()}<rect x="-400" y="560" width="1520" height="800" fill="${P.asphalt}"/><rect x="-400" y="560" width="1520" height="60" fill="${P.concrete}"/>
          <g class="roadline">${Array.from({ length: 10 }, (_, i) => `<rect class="rl" x="${-400 + i * 170}" y="900" width="90" height="14" fill="${P.line}" opacity=".7"/>`).join('')}</g></g>
        <!-- แฮนด์ + คันเร่ง ใกล้ ๆ -->
        <g transform="translate(360 700)">
          <ellipse cx="0" cy="430" rx="420" ry="40" fill="#000" opacity=".25"/>
          <!-- เรือนไมล์ -->
          <g transform="translate(-10 -40)"><circle r="150" fill="#1b1f27"/><circle r="136" fill="#0e1116"/>
            ${Array.from({ length: 13 }, (_, i) => { const a = -210 + i * 20; return `<line x1="${110 * Math.cos(a * Math.PI / 180)}" y1="${110 * Math.sin(a * Math.PI / 180)}" x2="${126 * Math.cos(a * Math.PI / 180)}" y2="${126 * Math.sin(a * Math.PI / 180)}" stroke="#e8e4d8" stroke-width="${i % 2 ? 2 : 4}"/>`; }).join('')}
            <text x="-70" y="-50" font-family="Kanit" font-size="18" fill="#d8d3c4">0</text><text x="30" y="-96" font-family="Kanit" font-size="18" fill="#d8d3c4">60</text><text x="82" y="-20" font-family="Kanit" font-size="18" fill="#d8d3c4">120</text>
            <g class="needle"><path d="M0 0 l-6 8 l-96 -2 l96 -14z" fill="${P.red}"/></g><circle r="12" fill="#2a2f3a"/>
            <text x="0" y="70" font-family="Kanit" font-size="16" fill="#8d939c" text-anchor="middle">km/h</text></g>
          <!-- แฮนด์ขวา -->
          <rect x="120" y="60" width="300" height="46" rx="23" fill="#2b2b33"/>
          <g class="grip" transform="translate(300 83)"><rect x="-80" y="-30" width="200" height="60" rx="30" fill="#15161c"/>${Array.from({ length: 8 }, (_, i) => `<rect x="${-66 + i * 24}" y="-30" width="8" height="60" rx="3" fill="#2d2f3a"/>`).join('')}</g>
          <path d="M150 40 q60 -40 150 -50" stroke="#8d939c" stroke-width="12" stroke-linecap="round" fill="none"/>
          <!-- มือ (ถุงมือ) -->
          <g class="hand" transform="translate(300 83)"><path d="M-70 -70 h150 a46 46 0 0 1 0 92 h-150 a46 46 0 0 1 0 -92z" fill="${P.skin}"/>
            ${[0, 1, 2, 3].map(i => `<rect x="${-62 + i * 36}" y="-62" width="30" height="76" rx="14" fill="${P.skin}" stroke="${P.skinD}" stroke-width="2"/>`).join('')}
            <path d="M-80 -66 q-60 10 -60 60 h60z" fill="${P.jacket}"/></g>
          <!-- กระจกมองข้าง -->
          <g transform="translate(470 -140)"><rect x="-6" y="0" width="12" height="160" fill="#2b2b33"/><ellipse rx="60" ry="42" fill="#1b1f27"/><ellipse rx="52" ry="34" fill="#b9d8e8"/><g transform="translate(0 0) scale(.14)">${A.zombie('#2a2430')}</g></g>
        </g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const s = kf(lt, [[0, 1.1], [dur, 1.0]], E.outCubic);
      const twist = kf(lt, [[0, 0], [0.8, -14], [1.0, -2]], E.inOutCubic);
      const sh = shake(t, 3 * seg(lt, 0.9, 0.3, E.linear) * (1 - seg(lt, 1.3, 0.6, E.linear)), 30, 1);
      cam(q(g, '.cam'), { x: 360, y: 700, s, dx: sh.x, dy: sh.y });
      q(g, '.hand').setAttribute('transform', `translate(300 83) rotate(${twist})`);
      q(g, '.grip').setAttribute('transform', `translate(300 83) rotate(${twist})`);
      q(g, '.needle').setAttribute('transform', `rotate(${kf(lt, [[0, -210], [1.0, -150], [dur, -200]])})`);
      qa(g, '.rl').forEach((r, i) => r.setAttribute('x', -400 + ((i * 170 + lt * 300) % 1700)));
    }
  });
  UI.stamp({ start: C('02', 0) + 0.05, end: C('02', 0) + 1.0, text: 'อย่า' });
  UI.flash(C('02', 0) + 0.05, 0.1);

  // ============ ช็อต 3: แผนที่วงกลม — ที่ที่รอดได้ดีที่สุด ============
  HF.shot({
    id: 'mapsafe', start: T('03').start, end: T('04a').start,
    init(g) {
      const chip = (cls, x, y, ic, lb) => `<g class="mchip ${cls}" transform="translate(${x} ${y})"><rect x="-70" y="-28" width="140" height="56" rx="28" fill="${P.cream}" stroke="#2a2622" stroke-width="2"/><text x="-42" y="9" font-size="26" text-anchor="middle">${ic}</text><text x="12" y="8" font-family="Kanit" font-weight="600" font-size="20" fill="#2a2622" text-anchor="middle">${lb}</text></g>`;
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#2f4a2a"/>
        <g filter="url(#blur6)">${Array.from({ length: 70 }, (_, i) => `<circle cx="${-300 + ((i * 131) % 1400)}" cy="${-50 + ((i * 197) % 1400)}" r="${40 + (i % 5) * 14}" fill="${['#3d5e34', '#46703c', '#355a2f'][i % 3]}"/>`).join('')}</g>
        <circle cx="360" cy="560" r="330" fill="#000" opacity=".3" filter="url(#blur10)"/>
        <clipPath id="mapclip"><circle cx="360" cy="540" r="310"/></clipPath>
        <g clip-path="url(#mapclip)">
          <rect x="0" y="200" width="720" height="700" fill="#c9c0ae"/>
          <rect x="300" y="200" width="120" height="700" fill="${P.asphalt}"/>
          <rect x="356" y="200" width="8" height="700" fill="${P.line}" opacity=".6"/>
          <!-- ทางเข้า -->
          <rect x="0" y="470" width="300" height="140" fill="${P.asphaltD}"/>
          <!-- หลังคาปั๊ม -->
          <rect x="60" y="300" width="230" height="200" rx="8" fill="${P.white}"/><rect x="60" y="300" width="230" height="200" rx="8" fill="none" stroke="${P.orange}" stroke-width="8"/>
          ${[0, 1].map(r => [0, 1].map(c => `<rect x="${95 + c * 95}" y="${340 + r * 80}" width="60" height="26" rx="4" fill="${P.concreteD}"/><rect x="${100 + c * 95}" y="${344 + r * 80}" width="18" height="18" rx="3" fill="${P.orange}"/><rect x="${132 + c * 95}" y="${344 + r * 80}" width="18" height="18" rx="3" fill="${P.orange}"/>`).join('')).join('')}
          <!-- ร้าน -->
          <rect x="60" y="640" width="200" height="130" rx="6" fill="#e3dccb" stroke="#8e836f" stroke-width="3"/><rect x="70" y="650" width="180" height="20" fill="${P.red}"/>
          <!-- ถังใต้ดิน -->
          <g class="tanks">${[0, 1, 2].map(i => `<circle cx="${110 + i * 60}" cy="580" r="24" fill="none" stroke="#5b4a35" stroke-width="3" stroke-dasharray="6 5"/>`).join('')}</g>
          <!-- ห้องน้ำ -->
          <rect x="150" y="810" width="90" height="60" rx="4" fill="#9a9183"/><rect x="100" y="815" width="40" height="40" rx="20" fill="#3f7fb8"/>
          <!-- เครื่องปั่นไฟ -->
          <rect x="30" y="800" width="50" height="40" rx="4" fill="${P.red}"/>
        </g>
        <circle cx="360" cy="540" r="310" fill="none" stroke="${P.cream}" stroke-width="10"/>
        <circle cx="360" cy="540" r="330" fill="none" stroke="${P.cream}" stroke-width="2" opacity=".6"/>
        <g class="chips">
          ${chip('c0', 175, 270, '⛽', 'น้ำมัน')}${chip('c1', 545, 300, '⚡', 'ไฟสำรอง')}${chip('c2', 170, 870, '🛒', 'อาหาร')}${chip('c3', 550, 840, '💧', 'น้ำ')}
        </g>
        <g class="warn" transform="translate(190 540)"><circle r="46" fill="${P.red}"/><circle class="ring" r="46" fill="none" stroke="${P.red}" stroke-width="4"/><text y="16" font-family="Kanit" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">?</text></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 560, s: kf(lt, [[0, 1.25], [dur, 1.02]], E.outCubic), r: kf(lt, [[0, -3], [dur, 0]]) });
      const t1 = C('03', 1) - this.start;
      qa(g, '.mchip').forEach((c, i) => { const a = seg(lt, t1 + i * .25, .35, E.outBack); c.style.opacity = a; const m = c.getAttribute('transform').match(/translate\(([-\d.]+) ([-\d.]+)\)/); c.setAttribute('transform', `translate(${m[1]} ${m[2]}) scale(${a}) rotate(${(1 - a) * -10})`); });
      const tw = C('03', 2) - this.start; const wa = seg(lt, tw, .4, E.outBack);
      q(g, '.warn').setAttribute('transform', `translate(190 540) scale(${wa})`);
      q(g, '.ring').setAttribute('r', 46 + ((t * 60) % 60)); q(g, '.ring').setAttribute('opacity', wa * (1 - ((t * 60) % 60) / 60));
    }
  });

  // ============ ช็อต 4: แนะนำ "ต้น" เดินไปหารถ ============
  HF.shot({
    id: 'intro', start: T('04a').start, end: T('04b').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.skyDusk()}
        <g filter="url(#blur6)">${A.treeline(760, '#55763f', 10)}<g transform="translate(560 800) scale(.6)">${A.shopFront(520, 230)}</g></g>
        <rect x="-400" y="800" width="1520" height="700" fill="${P.concrete}"/>
        <g filter="url(#blur3)" transform="translate(360 560)">${A.canopy(1100, 6)}</g>
        <g class="bikeg" transform="translate(620 1060) scale(.9)">${A.motorbike()}</g>
        <g class="dog" transform="translate(-60 1070) scale(.75)">${A.dogSide()}</g>
        <g class="ton" transform="translate(60 1070) scale(.9)">${A.tonSide()}</g>
        <g class="phone" transform="translate(0 0)" opacity="0"><rect x="-70" y="-120" width="140" height="240" rx="22" fill="#15161c"/><rect x="-60" y="-104" width="120" height="208" rx="14" fill="#2a2f3a"/><circle cy="-40" r="30" fill="${P.jacket}"/><text y="-30" font-size="30" text-anchor="middle">👩</text><text y="20" font-family="Kanit" font-weight="600" font-size="24" fill="#fff" text-anchor="middle">แม่</text><text class="ring" y="60" font-family="Kanit" font-size="18" fill="#9fb3c8" text-anchor="middle">กำลังโทร…</text></g>
        ${A.dust(18)}
      </g>`;
    },
    update(lt, g, t, dur) {
      const walk = clamp(lt / (dur - 0.8));
      const x = lerp(60, 430, E.inOutSine(walk));
      const ton = q(g, '.ton'); ton.setAttribute('transform', `translate(${x} 1070) scale(.9)`); walkTon(ton, lt * 9, 1 - seg(lt, dur - 1.0, .4, E.linear));
      const dog = q(g, '.dog'); dog.setAttribute('transform', `translate(${x - 170} 1070) scale(.75)`); dogTrot(dog, lt * 10, 1 - seg(lt, dur - 1.0, .4, E.linear));
      cam(q(g, '.cam'), { x: 360 + (x - 240) * .35, y: 820, s: kf(lt, [[0, 1.05], [dur, 1.0]]) });
      const tp = C('04a', 3) - this.start; const pa = seg(lt, tp, .35, E.outBack);
      const ph = q(g, '.phone'); ph.setAttribute('opacity', pa); ph.setAttribute('transform', `translate(${x + 40} 720) scale(${pa}) rotate(${-8 * (1 - pa)})`);
      q(g, '.ring').textContent = ['กำลังโทร', 'กำลังโทร.', 'กำลังโทร..', 'กำลังโทร...'][Math.floor(t * 3) % 4];
      dustUpdate(g, t, [0, 500, 720, 700]);
    }
  });
  UI.nametag({ start: C('04a', 0) + 0.3, end: C('04a', 2) + 0.3, name: 'ต้น', role: 'ไรเดอร์ส่งอาหาร · อายุ 24', avatar: '<svg viewBox="-60 -330 120 120" width="64" height="64">' + A.tonSide() + '</svg>' });

  // ============ ช็อต 5: "อย่า." — แผนที่มืด ตัวเมืองแดง ============
  HF.shot({
    id: 'no', start: T('04b').start, end: T('05').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#0b0d14"/>
        <g opacity=".5">${Array.from({ length: 60 }, (_, i) => `<rect x="${-300 + ((i * 173) % 1400)}" y="${-80 + ((i * 251) % 1500)}" width="${20 + (i % 4) * 16}" height="${20 + (i % 3) * 22}" fill="#141827"/>`).join('')}</g>
        <!-- ถนนรัศมี -->
        <g class="roads" stroke="#2a3148" stroke-width="12" fill="none">${[0, 1, 2, 3, 4, 5, 6, 7].map(i => { const a = i * Math.PI / 4; return `<line x1="360" y1="420" x2="${360 + Math.cos(a) * 900}" y2="${420 + Math.sin(a) * 900}"/>`; }).join('')}</g>
        <!-- ตัวเมืองแดง -->
        <circle class="blob" cx="360" cy="420" r="220" fill="url(#redglow)"/>
        <g class="dots">${Array.from({ length: 260 }, (_, i) => { const r = Math.sqrt(HF.hash(i)) * 190, a = HF.hash(i + 500) * 6.283; return `<circle class="d" cx="${360 + Math.cos(a) * r}" cy="${420 + Math.sin(a) * r}" r="${1.5 + HF.hash(i + 7) * 2.5}" fill="#ff6a5a"/>`; }).join('')}</g>
        <g transform="translate(360 420)"><rect x="-60" y="-200" width="120" height="36" rx="18" fill="${P.red}"/><text y="-175" font-family="Kanit" font-weight="600" font-size="20" fill="#fff" text-anchor="middle">ตัวเมือง</text></g>
        <!-- ถนนลงมาหาปั๊ม -->
        <line x1="360" y1="640" x2="360" y2="1300" stroke="#2a3148" stroke-width="16"/>
        <g class="cars">${Array.from({ length: 40 }, (_, i) => `<rect class="car" x="${348 + (i % 2) * 10}" y="${660 + i * 16}" width="8" height="12" rx="2" fill="#ff6a5a" opacity="0"/>`).join('')}</g>
        <g transform="translate(360 1180)"><circle r="22" fill="${P.jacket}"/><text y="8" font-size="22" text-anchor="middle">⛽</text><rect x="30" y="-18" width="150" height="36" rx="18" fill="${P.cream}"/><text x="105" y="8" font-family="Kanit" font-weight="600" font-size="18" fill="#2a2622" text-anchor="middle">ปั๊ม · 18 กม.</text></g>
        <rect class="frame" x="40" y="200" width="640" height="900" fill="none" stroke="${P.red}" stroke-width="6" stroke-dasharray="80 1000" opacity="0"/>
      </g>`;
    },
    update(lt, g, t, dur) {
      const sh = shake(t, 10 * (1 - seg(lt, 0, 0.6, E.linear)), 35, 2);
      cam(q(g, '.cam'), { x: 360, y: 640, s: kf(lt, [[0, 1.3], [0.5, 1.0]], E.outExpo), dx: sh.x, dy: sh.y });
      qa(g, '.d').forEach((d, i) => d.setAttribute('opacity', 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(t * 6 + i * 1.7))));
      q(g, '.blob').setAttribute('r', 220 + Math.sin(t * 4) * 10);
      qa(g, '.car').forEach((c, i) => c.setAttribute('opacity', seg(lt, 0.3 + i * 0.012, 0.1, E.linear)));
    }
  });
  UI.stamp({ start: T('04b').start + 0.02, end: T('04b').end + 0.35, text: 'อย่า' });
  UI.red(T('04b').start, T('04c').start, 1);
  UI.flash(T('04b').start + 0.02, 0.14);

  // ============ ช็อต 6: รถติด 2,000 คัน ============
  HF.shot({
    id: 'jam', start: T('04c').start, end: T('05').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#0b0d14"/>
        <g opacity=".5">${Array.from({ length: 60 }, (_, i) => `<rect x="${-300 + ((i * 173) % 1400)}" y="${-80 + ((i * 251) % 1500)}" width="${20 + (i % 4) * 16}" height="${20 + (i % 3) * 22}" fill="#141827"/>`).join('')}</g>
        <circle cx="360" cy="140" r="220" fill="url(#redglow)"/>
        <g transform="translate(360 140)"><rect x="-60" y="-18" width="120" height="36" rx="18" fill="${P.red}"/><text y="7" font-family="Kanit" font-weight="600" font-size="20" fill="#fff" text-anchor="middle">ตัวเมือง</text></g>
        <!-- ถนนมิตรภาพ 4 เลน -->
        <rect x="280" y="240" width="160" height="1100" fill="#2a3148"/><rect x="357" y="240" width="6" height="1100" fill="${P.line}" opacity=".35"/>
        <g class="cars">${Array.from({ length: 160 }, (_, i) => { const lane = i % 4; return `<rect class="car" x="${292 + lane * 38}" y="${250 + Math.floor(i / 4) * 26}" width="22" height="16" rx="3" fill="${['#ff6a5a', '#f5c542', '#e8e4d8', '#ff8a6a'][i % 4]}" opacity="0"/>`; }).join('')}</g>
        <g transform="translate(360 1200)"><circle r="26" fill="${P.jacket}"/><text y="9" font-size="24" text-anchor="middle">⛽</text></g>
        <text x="360" y="1250" font-family="Kanit" font-weight="600" font-size="20" fill="${P.cream}" text-anchor="middle">ปั๊มริมถนนมิตรภาพ</text>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 300], [dur, 700]], E.inOutSine), s: 1.0 });
      qa(g, '.car').forEach((c, i) => { const a = seg(lt, 0.1 + i * 0.012, 0.08, E.linear); c.setAttribute('opacity', a * (0.7 + 0.3 * Math.sin(t * 8 + i))); });
    }
  });
  UI.hud({ start: C('04c', 1), end: T('05').start, icon: '🚗', label: 'รถติดบนถนนเข้าเมือง', value: t => fmt(Math.round(2000 * seg(t, C('04c', 1), 1.2, E.outExpo))), unit: 'คัน', cls: 'red' });

  // ============ ช็อต 7: นาฬิกาเริ่มเดิน — ไฟหน้ารถไกล ๆ ============
  HF.shot({
    id: 'clock', start: T('05').start, end: T('06').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.skyDusk()}
        <g class="nightsky" opacity="0">${A.skyNight()}</g>
        <g filter="url(#blur6)">${A.treeline(600, '#1f2e22', 16, true)}</g>
        <!-- ถนนเปอร์สเปกทีฟ -->
        <path d="M-200 1300 L300 600 L420 600 L920 1300z" fill="${P.asphalt}"/>
        <path d="M-200 1300 L300 600 L420 600 L920 1300z" fill="#0d1020" opacity=".55"/>
        <g class="dash">${Array.from({ length: 10 }, (_, i) => `<rect class="ds" x="356" y="0" width="8" height="30" fill="${P.line}" opacity=".6"/>`).join('')}</g>
        <!-- ไฟหน้ารถ 2 ดวง -->
        <g class="hl" transform="translate(372 640)"><ellipse class="hg" rx="60" ry="24" fill="url(#headlight)"/><circle cx="-8" r="4" fill="#fff9df"/><circle cx="8" r="4" fill="#fff9df"/></g>
        <!-- ต้น + หมา เงาด้านหน้า -->
        <rect x="-400" y="1120" width="1520" height="300" fill="#1c1c24"/>
        <g class="tonS" transform="translate(220 1180) scale(1.0)">${A.tonSilhouette()}</g>
        <g class="dogS" transform="translate(440 1180) scale(.9)" style="filter:brightness(.08)">${A.dogSide({ sit: true })}</g>
        ${A.dust(16)}
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 760, s: kf(lt, [[0, 1.0], [dur, 1.12]], E.inOutSine) });
      q(g, '.nightsky').setAttribute('opacity', seg(lt, 0, dur, E.linear) * 0.85);
      const k = seg(lt, 0.3, dur - 0.3, E.inQuad);
      const hl = q(g, '.hl'); hl.setAttribute('transform', `translate(${372 - k * 30} ${640 + k * 260}) scale(${1 + k * 5})`); q(g, '.hg').setAttribute('opacity', 0.6 + 0.4 * flicker(t, 20, 4, .5));
      qa(g, '.ds').forEach((d, i) => { const p = ((i / 10) + lt * 0.08) % 1; const y = 600 + p * p * 700; d.setAttribute('y', y); d.setAttribute('height', 6 + p * p * 60); d.setAttribute('x', 360 - (2 + p * 10)); d.setAttribute('width', 4 + p * 20); });
      idleTon(q(g, '.tonS'), t); dogIdle(q(g, '.dogS'), t);
      dustUpdate(g, t, [0, 600, 720, 600]);
    }
  });
  // นาฬิกาถอยหลัง 20:00 เดินจริงตลอดเรื่องจนถึงการ์ดจบ
  const clockStart = C('05', 0) + 0.3;
  const clockStr = t => { const left = 20 * 60 - (t - clockStart) * 1.0; return `${pad2(left / 60)}:${pad2(left % 60)}`; };
  UI.hud({ start: clockStart, end: T('06').start, icon: '⏱', label: 'เหลือเวลา', value: clockStr, cls: 'red' });

  // ============ ช็อต 8: ภาพตัดขวาง — ถังใต้ดิน + ปั๊มไฟฟ้า ============
  HF.shot({
    id: 'cross', start: T('06').start, end: C('06', 6),
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.skyDusk()}
        <g class="nightsky" opacity=".75">${A.skyNight()}</g>
        <g filter="url(#blur3)">${A.treeline(420, '#1f2e22', 14, true)}</g>
        <g transform="translate(360 80) scale(.9)">${A.canopy(900, 4)}</g>
        <rect x="-400" y="440" width="1520" height="60" fill="${P.concrete}"/>
        <g transform="translate(360 440) scale(1.1)">${A.dispenser()}</g>
        <g class="ton" transform="translate(240 448) scale(.62)">${A.tonSide()}</g>
        <!-- ใต้ดิน -->
        <rect x="-400" y="500" width="1520" height="900" fill="url(#groundCut)"/>
        <g opacity=".35">${Array.from({ length: 60 }, (_, i) => `<ellipse cx="${-300 + ((i * 97) % 1400)}" cy="${520 + ((i * 61) % 820)}" rx="${4 + (i % 4) * 3}" ry="${3 + (i % 3) * 2}" fill="#3b2a18"/>`).join('')}</g>
        <!-- ถังน้ำมันใต้ดิน -->
        <g transform="translate(360 980)">
          <rect x="-300" y="-150" width="600" height="300" rx="150" fill="#5f6672"/>
          <rect x="-290" y="-140" width="580" height="280" rx="140" fill="#7b838f"/>
          <clipPath id="tankclip"><rect x="-290" y="-140" width="580" height="280" rx="140"/></clipPath>
          <g clip-path="url(#tankclip)"><rect class="fuel" x="-300" y="-80" width="600" height="240" fill="url(#fuel)"/><rect class="wave" x="-300" y="-84" width="600" height="8" fill="#fde28a" opacity=".6"/></g>
          <rect x="-290" y="-140" width="580" height="280" rx="140" fill="none" stroke="#3f454f" stroke-width="6"/>
          <g class="tanklabel" transform="translate(0 -10)"><rect x="-150" y="-46" width="300" height="78" rx="12" fill="${P.cream}" stroke="#2a2622" stroke-width="3"/><text class="tl1" y="-6" font-family="Kanit" font-weight="700" font-size="34" fill="#2a2622" text-anchor="middle">30,000 ลิตร</text><text class="tl2" y="22" font-family="Kanit" font-weight="600" font-size="18" fill="#6b645a" text-anchor="middle">ถังใต้ดิน ×4</text></g>
          <!-- ปั๊มจุ่ม (submersible) -->
          <g class="subpump" transform="translate(120 60)"><rect x="-26" y="-50" width="52" height="100" rx="8" fill="#2b2f38"/><rect x="-18" y="-40" width="36" height="20" rx="4" fill="#8a909a"/><circle class="pled" cy="30" r="7" fill="#2bd46b"/><g class="bolt"><path d="M-4 -200 l-10 24 h12 l-8 24 l22 -32 h-12 l8 -16z" fill="${P.yellow}" filter="url(#softglow)"/></g></g>
          <!-- ท่อขึ้นตู้จ่าย -->
          <rect x="110" y="-480" width="20" height="380" fill="#8a909a"/><rect x="110" y="-480" width="20" height="380" fill="#3f454f" opacity=".4"/>
          <g class="flow">${Array.from({ length: 12 }, (_, i) => `<rect class="fd" x="116" y="${-100 - i * 26}" width="8" height="12" rx="3" fill="${P.yellow}"/>`).join('')}</g>
          <!-- ท่อโค้งเข้าตู้ -->
        </g>
        <path d="M480 500 v-40 q0 -14 -14 -14 h-80" stroke="#8a909a" stroke-width="20" fill="none"/>
        <path d="M480 500 v-40 q0 -14 -14 -14 h-80" stroke="#3f454f" stroke-width="20" fill="none" opacity=".4"/>
        <!-- สายไฟจากเสา -->
        <rect x="640" y="150" width="14" height="300" fill="#4a4237"/><rect x="600" y="160" width="94" height="10" fill="#4a4237"/>
        <path class="wire" d="M647 170 q-150 60 -300 50" stroke="#2a2622" stroke-width="4" fill="none"/>
        <g class="powerbox" transform="translate(640 330)"><rect x="-26" y="-30" width="52" height="60" rx="6" fill="#8a909a"/><circle class="pbled" r="8" fill="#2bd46b"/></g>
        <g class="darkmask" opacity="0"><rect x="-400" y="-100" width="1520" height="1700" fill="#05060c"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const tOff = C('06', 3) - this.start, tNum = C('06', 4) - this.start;
      const s = kf(lt, [[0, 1.3], [1.6, 1.0], [tNum, 1.0], [tNum + 0.8, 1.35]], E.inOutCubic);
      const cy = kf(lt, [[0, 420], [1.6, 700], [tNum, 700], [tNum + 0.8, 1010]], E.inOutCubic);
      cam(q(g, '.cam'), { x: 360, y: cy, s });
      const power = lt < tOff ? 1 : 0;
      q(g, '.ton .armF').setAttribute('transform', `translate(0 -232) rotate(-70)`); idleTon(q(g, '.ton'), t);
      qa(g, '.fd').forEach((d, i) => { d.setAttribute('y', -100 - ((i * 26 + (power ? t * 260 : 0)) % 380)); d.setAttribute('opacity', power ? 1 : 0.15); });
      q(g, '.wave').setAttribute('y', -84 + Math.sin(t * 3) * 3);
      q(g, '.pled').setAttribute('fill', power ? '#2bd46b' : '#5a1a1a'); q(g, '.pbled').setAttribute('fill', power ? '#2bd46b' : '#5a1a1a');
      q(g, '.bolt').setAttribute('opacity', power ? 0.7 + 0.3 * flicker(t, 18, 2, .6) : 0.08);
      q(g, '.darkmask').setAttribute('opacity', 0.55 * seg(lt, tOff, 0.25, E.outExpo) * (0.9 + 0.1 * flicker(t, 30, 5, .7)));
      q(g, '.tl2').textContent = lt < tNum ? 'ถังใต้ดิน ×4' : '= แค่ตัวเลข';
      q(g, '.tl2').setAttribute('fill', lt < tNum ? '#6b645a' : P.red);
      const pulse = lt >= tNum ? 1 + 0.08 * Math.max(0, Math.sin((lt - tNum) * 12)) * (1 - seg(lt, tNum, .7, E.linear)) : 1;
      q(g, '.tanklabel').setAttribute('transform', `translate(0 -10) scale(${pulse})`);
    }
  });
  UI.chips({ start: C('06', 1), end: C('06', 6), offAt: C('06', 3), items: [{ ic: '⚡', lb: 'ไฟฟ้า' }, { ic: '🔩', lb: 'ปั๊มจุ่ม' }, { ic: '⛽', lb: 'น้ำมันไหล' }], state: t => t < C('06', 3) ? ['on', 'on', 'on'] : ['off', 'off', 'off'] });
  UI.flash(C('06', 3), 0.08);

  // ============ ช็อต 9: เติมเต็มถัง + แกลลอน 6 ใบ ============
  HF.shot({
    id: 'gallons', start: C('06', 6), end: T('07').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.skyNight()}
        <g filter="url(#blur6)"><g transform="translate(360 520) scale(1.3)">${A.canopy(900, 4)}</g></g>
        <rect x="-400" y="900" width="1520" height="600" fill="#34343d"/>
        <g class="cone" transform="translate(360 560)"><ellipse rx="420" ry="520" fill="url(#lightCone)" opacity=".7"/></g>
        <g class="pickupg" transform="translate(620 1000) scale(.8)">${A.pickup()}</g>
        <g class="bikeg" transform="translate(130 1010) scale(.7)">${A.motorbike()}</g>
        <g class="fuelok">${[[620, 820], [130, 860]].map(([x, y], i) => `<g class="fok" transform="translate(${x} ${y})"><rect x="-54" y="-24" width="108" height="48" rx="24" fill="${P.cream}" stroke="#2a2622" stroke-width="2"/><text x="-26" y="8" font-size="22" text-anchor="middle">⛽</text><text x="16" y="8" font-family="Kanit" font-weight="700" font-size="20" fill="#2f9e5a" text-anchor="middle">เต็ม</text></g>`).join('')}</g>
        <g class="ton" transform="translate(380 1030) scale(.78)">${A.tonSide()}</g>
        <g class="nozzle" transform="translate(430 880)"><path d="M0 0 h50 l10 14 l-20 10 h-40z" fill="#2b2f38"/><path class="pour" d="M58 14 q10 30 4 60" stroke="${P.yellow}" stroke-width="6" fill="none" stroke-linecap="round"/></g>
        <g class="dog" transform="translate(560 1150) scale(.6)">${A.dogSide({ sit: true })}</g>
        <g class="gals">${Array.from({ length: 6 }, (_, i) => `<g class="gal" transform="translate(${150 + i * 84} 1200) scale(.9)">${A.gallon(i % 2 ? '#f5c542' : '#e8a53a')}</g>`).join('')}</g>
        ${A.dust(14)}
      </g>`;
      qa(g, '.cone').forEach(c => c.setAttribute('opacity', .35));
    },
    update(lt, g, t, dur) {
      const t7 = C('06', 7) - this.start;
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 900], [t7, 920], [t7 + 0.6, 1040]]), s: kf(lt, [[0, 1.0], [t7, 1.05], [t7 + 0.6, 1.25]]) });
      qa(g, '.fok').forEach((f, i) => { const a = seg(lt, 0.4 + i * 0.5, 0.35, E.outBack); const m = f.getAttribute('transform').match(/translate\(([-\d.]+) ([-\d.]+)\)/); f.setAttribute('transform', `translate(${m[1]} ${m[2]}) scale(${a})`); });
      qa(g, '.gal').forEach((ga, i) => { const a = seg(lt, t7 + 0.1 + i * 0.22, 0.35, E.outBack); ga.setAttribute('transform', `translate(${150 + i * 84} ${1200 - (1 - a) * 40}) scale(${0.9 * a})`); });
      q(g, '.ton .armF').setAttribute('transform', `translate(0 -232) rotate(${-60 + Math.sin(t * 3) * 3})`); idleTon(q(g, '.ton'), t); dogIdle(q(g, '.dog'), t);
      q(g, '.pour').setAttribute('opacity', lt < t7 ? 0.9 : 0);
      dustUpdate(g, t, [0, 700, 720, 500]);
    }
  });
  UI.hud({ start: C('06', 7) + 0.1, end: T('07').start, icon: '🛢', label: 'น้ำมันสำรอง', value: t => Math.min(6, Math.floor((t - C('06', 7) - 0.1) / 0.22) + 1), unit: 'แกลลอน', cls: 'green' });

  // ============ ช็อต 10: เครื่องปั่นไฟสตาร์ท ============
  HF.shot({
    id: 'generator', start: T('07').start, end: C('07', 2),
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#120f0c"/>
        <g opacity=".6">${Array.from({ length: 16 }, (_, i) => `<rect x="${-400 + i * 100}" y="-100" width="6" height="1700" fill="#1e1813"/>`).join('')}</g>
        <rect x="-400" y="960" width="1520" height="600" fill="#1a1612"/>
        <g class="bulb" transform="translate(360 150)"><rect x="-2" y="-200" width="4" height="170" fill="#2a2622"/><circle class="bglow" r="260" fill="url(#glow)" opacity="0"/><circle class="bcore" r="26" fill="#3a3630"/></g>
        <g class="lightcone" opacity="0"><path d="M360 160 L-200 1100 L920 1100z" fill="url(#lightCone)"/></g>
        <g class="gen" transform="translate(360 960) scale(1.5)">${A.generator()}</g>
        <g class="cord" transform="translate(360 960) scale(1.5)"><path class="cordline" d="M-96 -170 h0" stroke="#d8d3c4" stroke-width="4" stroke-linecap="round"/><rect class="handle" x="-110" y="-190" width="28" height="18" rx="6" fill="${P.yellow}"/></g>
        <g class="hand" transform="translate(200 700)"><circle r="34" fill="${P.skin}"/><rect x="-30" y="-10" width="60" height="120" rx="22" fill="${P.jacket}"/></g>
        <g class="puffs">${Array.from({ length: 6 }, (_, i) => `<circle class="puff" r="18" fill="#9a9a9a" opacity="0"/>`).join('')}</g>
        <g class="darkover"><rect x="-400" y="-100" width="1520" height="1700" fill="#000" opacity=".35"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const tOn = C('07', 1) - this.start + 0.3;
      const on = seg(lt, tOn, 0.5, E.outExpo) * (0.85 + 0.15 * flicker(t, 20, 6, .6));
      const pull = kf(lt, [[0, 0], [tOn - 0.5, 0], [tOn - 0.1, 1], [tOn + 0.2, 0]], E.inOutCubic);
      const sh = shake(t, 4 * on, 50, 9);
      cam(q(g, '.cam'), { x: 360, y: 760, s: kf(lt, [[0, 1.15], [dur, 1.0]], E.outCubic), dx: sh.x, dy: sh.y });
      q(g, '.hand').setAttribute('transform', `translate(${200 - pull * 150} ${700 - pull * 90})`);
      q(g, '.handle').setAttribute('x', -110 - pull * 100); q(g, '.handle').setAttribute('y', -190 - pull * 60); q(g, '.cordline').setAttribute('d', `M-96 -170 l${-pull * 100} ${-pull * 60}`);
      q(g, '.fanblades').setAttribute('transform', `rotate(${on > 0.1 ? (t * 900) % 360 : 0})`);
      q(g, '.genled').setAttribute('fill', on > 0.3 ? '#2bd46b' : '#5a1a1a');
      q(g, '.bglow').setAttribute('opacity', on); q(g, '.bcore').setAttribute('fill', on > 0.2 ? '#fff6d0' : '#3a3630'); q(g, '.lightcone').setAttribute('opacity', on * 0.7);
      q(g, '.darkover').setAttribute('opacity', 1 - on * 0.9);
      qa(g, '.puff').forEach((p, i) => { const k = on > 0.1 ? ((t * 1.2 + i * 0.17) % 1) : 0; p.setAttribute('cx', 360 + (-103 * 1.5) + k * 40 + Math.sin(k * 10 + i) * 10); p.setAttribute('cy', 960 - 176 * 1.5 - k * 180); p.setAttribute('r', 10 + k * 30); p.setAttribute('opacity', on > 0.1 ? (1 - k) * 0.35 : 0); });
    }
  });
  UI.hud({ start: T('07').start, end: C('07', 2), icon: '⏱', label: 'เหลือเวลา', value: clockStr, cls: 'red' });
  UI.flash(C('07', 1) + 0.3, 0.2);
})();
