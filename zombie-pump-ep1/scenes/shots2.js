/* ============================================================
   SHOTS (ตอนที่ 2/2): ช็อต 11–20 — รัศมี 3 กม. ถึง การ์ดจบ
   ============================================================ */
(() => {
  const { seg, kf, E, clamp, lerp, $, tf, cam, op, show, noise, shake, flicker, fmt, pad2 } = HF;
  const A = ART, P = ART.P;
  const clockStart = C('05', 0) + 0.3;
  const clockStr = t => { const left = 20 * 60 - (t - clockStart); return `${pad2(left / 60)}:${pad2(left % 60)}`; };

  // ============ ช็อต 11: มุมสูงกลางคืน — จุดเดียวที่สว่าง รัศมี 3 กม. ============
  HF.shot({
    id: 'radius', start: C('07', 2), end: T('08').start,
    init(g) {
      const zs = Array.from({ length: 70 }, (_, i) => { const a = HF.hash(i) * 6.283, r = 260 + HF.hash(i + 50) * 420; return { a, r, s: 0.6 + HF.hash(i + 90) }; });
      this.zs = zs;
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#070a14"/>
        <g filter="url(#blur10)" opacity=".8">${Array.from({ length: 80 }, (_, i) => `<ellipse cx="${-300 + ((i * 131) % 1400)}" cy="${-50 + ((i * 197) % 1500)}" rx="${60 + (i % 5) * 20}" ry="${40 + (i % 4) * 16}" fill="${['#0c1a16', '#0e2019', '#0a1512'][i % 3]}"/>`).join('')}</g>
        <!-- ทางหลวง -->
        <path d="M-300 1500 L360 640 L1000 -200" stroke="#161d2e" stroke-width="40" fill="none"/>
        <path d="M-300 1500 L360 640 L1000 -200" stroke="#2a3148" stroke-width="3" stroke-dasharray="10 14" fill="none"/>
        <!-- วงรัศมี -->
        <g class="rings">${[1, 2, 3].map(i => `<g class="ring r${i}"><circle cx="360" cy="640" r="${i * 150}" fill="none" stroke="${P.cream}" stroke-width="2" stroke-dasharray="8 10" opacity=".55"/><rect x="${360 + i * 150 - 44}" y="${640 - 18}" width="88" height="34" rx="17" fill="${P.cream}"/><text x="${360 + i * 150}" y="${640 + 6}" font-family="Kanit" font-weight="600" font-size="17" fill="#2a2622" text-anchor="middle">${i} กม.</text></g>`).join('')}</g>
        <!-- ซอมบี้ (จุดแดง) -->
        <g class="zdots">${zs.map((z, i) => `<g class="zd" transform="translate(${360 + Math.cos(z.a) * z.r} ${640 + Math.sin(z.a) * z.r})"><circle r="${5 * z.s}" fill="#ff5a4a"/><circle class="zr" r="${5 * z.s}" fill="none" stroke="#ff5a4a" stroke-width="1.5"/></g>`).join('')}</g>
        <!-- ปั๊ม = จุดเดียวที่สว่าง -->
        <g class="station" transform="translate(360 640)"><circle class="sglow" r="150" fill="url(#glow)"/><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#fff6d0"/><rect x="-26" y="-18" width="52" height="8" rx="3" fill="${P.orange}"/><circle class="sring" r="40" fill="none" stroke="#fff6d0" stroke-width="2"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const t3 = C('07', 3) - this.start, t4 = C('07', 4) - this.start;
      cam(q(g, '.cam'), { x: 360, y: 640, s: kf(lt, [[0, 1.6], [t3, 1.0], [dur, 0.9]], E.inOutCubic), r: kf(lt, [[0, 0], [dur, 4]], E.linear) });
      q(g, '.sglow').setAttribute('opacity', 0.7 + 0.3 * flicker(t, 14, 3, .5)); q(g, '.sglow').setAttribute('r', 150 + Math.sin(t * 3) * 10);
      q(g, '.sring').setAttribute('r', 20 + ((t * 80) % 120)); q(g, '.sring').setAttribute('opacity', 1 - ((t * 80) % 120) / 120);
      qa(g, '.ring').forEach((r, i) => { const a = seg(lt, t3 - 0.2 + i * 0.3, 0.4, E.outBack); r.setAttribute('opacity', a); r.setAttribute('transform', `translate(360 640) scale(${0.6 + 0.4 * a}) translate(-360 -640)`); });
      const move = seg(lt, t4, dur - t4, E.inQuad);
      qa(g, '.zd').forEach((d, i) => { const z = this.zs[i]; const a = seg(lt, 0.2 + i * 0.03, 0.2, E.linear); const r = z.r - move * 180 * (0.6 + HF.hash(i + 3)); const ang = z.a + Math.sin(t * .7 + i) * 0.02;
        d.setAttribute('transform', `translate(${360 + Math.cos(ang) * r} ${640 + Math.sin(ang) * r})`); d.setAttribute('opacity', a * (0.6 + 0.4 * Math.sin(t * 4 + i)));
        const rr = q(d, '.zr'); rr.setAttribute('r', 5 + ((t * 30 + i * 7) % 24)); rr.setAttribute('opacity', 1 - ((t * 30 + i * 7) % 24) / 24); });
    }
  });
  UI.hud({ start: C('07', 2), end: T('08').start, icon: '⏱', label: 'เหลือเวลา', value: clockStr, cls: 'red' });
  UI.hud({ start: C('07', 3), end: T('08').start, icon: '💡', label: 'มองเห็นได้ในรัศมี', value: '3', unit: 'กม.' });
  UI.hud({ start: C('07', 4), end: T('08').start, icon: '🧟', label: 'กำลังเดินมา', value: t => Math.min(70, Math.floor((t - C('07', 4)) * 40)), unit: 'ตัว', cls: 'red' });

  // ============ ช็อต 12: ในร้าน — พนักงาน 4 ลูกค้า 7 ============
  HF.shot({
    id: 'people', start: T('08').start, end: C('08', 3),
    init(g) {
      const staffC = ['#f28b2b', '#f28b2b', '#f28b2b', '#f28b2b'], custC = ['#3a3f4a', '#5b4a6b', '#2f5a4a', '#6b3a3a', '#3a4f6b', '#4a4a3a', '#5a3f2f'];
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#1a1d26"/>
        <rect x="-400" y="-100" width="1520" height="900" fill="#262a36"/>
        <g class="emlight"><rect x="-400" y="-100" width="1520" height="1700" fill="#2a2010" opacity=".6"/><ellipse cx="360" cy="520" rx="500" ry="420" fill="url(#glow)" opacity=".35"/></g>
        <!-- ชั้นวางของ -->
        ${[0, 1, 2].map(i => `<rect x="-100" y="${300 + i * 110}" width="920" height="10" fill="#4a4f5c"/>${Array.from({ length: 22 }, (_, j) => `<rect x="${-80 + j * 42}" y="${266 + i * 110}" width="30" height="32" rx="4" fill="${['#f28b2b', '#2f9e5a', '#f5c542', '#d7342c', '#1f6fb2', '#e8e4d8'][(i + j) % 6]}" opacity=".7"/>`).join('')}`).join('')}
        <!-- เคาน์เตอร์ -->
        <rect x="-400" y="700" width="1520" height="120" fill="#3b3f4b"/><rect x="-400" y="700" width="1520" height="14" fill="#5a5f6c"/>
        <rect x="-400" y="820" width="1520" height="600" fill="#22252e"/>
        <g class="staff">${staffC.map((c, i) => `<g class="ps" transform="translate(${120 + i * 160} 700) scale(.85)">${A.personFront(c)}<rect x="-30" y="-230" width="60" height="30" fill="#2a2622" opacity=".3"/></g>`).join('')}</g>
        <g class="cust">${custC.map((c, i) => `<g class="pc" transform="translate(${80 + i * 95} 1180) scale(${0.95 + (i % 3) * 0.08})">${A.personFront(c)}</g>`).join('')}</g>
        <g class="ton" transform="translate(-60 1190) scale(.72)">${A.tonSide()}</g>
        ${A.dust(12)}
      </g>`;
    },
    update(lt, g, t, dur) {
      const t1 = C('08', 1) - this.start, t2 = C('08', 2) - this.start;
      cam(q(g, '.cam'), { x: 360, y: 760, s: kf(lt, [[0, 1.08], [dur, 1.0]]) });
      q(g, '.emlight').setAttribute('opacity', 0.8 + 0.2 * flicker(t, 16, 8, .5));
      qa(g, '.ps').forEach((p, i) => { const a = seg(lt, t1 + i * 0.18, 0.3, E.outBack); p.setAttribute('transform', `translate(${120 + i * 160} ${700 + (1 - a) * 30}) scale(.85)`); p.setAttribute('opacity', a); });
      qa(g, '.pc').forEach((p, i) => { const a = seg(lt, t2 + i * 0.14, 0.3, E.outBack); p.setAttribute('transform', `translate(${80 + i * 95} ${1180 + (1 - a) * 30}) scale(${(0.95 + (i % 3) * 0.08) * a})`); });
      const ton = q(g, '.ton'); const x = lerp(-60, 100, seg(lt, 0, 1.2, E.outCubic)); ton.setAttribute('transform', `translate(${x} 1190) scale(.72)`); walkTon(ton, lt * 9, 1 - seg(lt, 1.0, 0.3, E.linear));
      dustUpdate(g, t, [0, 200, 720, 900], 0.6);
    }
  });
  UI.hud({ start: C('08', 1), end: T('09').start, icon: '🧑‍🔧', label: 'พนักงาน', value: t => Math.min(4, Math.floor((t - C('08', 1)) / 0.18) + 1), unit: 'คน' });
  UI.hud({ start: C('08', 2), end: T('09').start, icon: '🧍', label: 'ลูกค้าที่ติดอยู่', value: t => Math.min(7, Math.floor((t - C('08', 2)) / 0.14) + 1), unit: 'คน' });

  // ============ ช็อต 13: หมาปั๊มเห่ารถที่เลี้ยวเข้ามา ============
  HF.shot({
    id: 'bark', start: C('08', 3), end: C('08', 5),
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.skyNight()}
        <g filter="url(#blur6)"><g transform="translate(360 420) scale(1.2)">${A.canopy(900, 4)}</g></g>
        <rect x="-400" y="860" width="1520" height="700" fill="#2d2d36"/>
        <g class="carlight"><path class="beam" d="M900 900 L300 760 L300 1040z" fill="url(#headlight)" opacity="0"/><g class="carbody" transform="translate(1100 1000) scale(-1 1)">${A.pickup('#9aa0a6')}</g></g>
        <g class="dog" transform="translate(240 1120) scale(1.6)">${A.dogSide()}</g>
        <g class="barkfx" transform="translate(380 820)" opacity="0">
          <path d="M0 -40 q40 -30 70 0 M10 0 q40 -20 80 0 M0 40 q40 30 70 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>
          <g class="hong" transform="translate(150 -60) rotate(-8)"><rect x="-80" y="-40" width="160" height="78" rx="14" fill="${P.yellow}"/><text y="18" font-family="Kanit" font-weight="700" font-size="50" fill="#2a2622" text-anchor="middle">โฮ่ง!</text></g>
        </g>
        ${A.dust(10)}
      </g>`;
      qa(g, '.cone').forEach(c => c.setAttribute('opacity', .35));
    },
    update(lt, g, t, dur) {
      const sh = shake(t, 2.5, 30, 11);
      cam(q(g, '.cam'), { x: 360, y: 900, s: kf(lt, [[0, 1.1], [dur, 1.02]], E.outCubic), dx: sh.x, dy: sh.y });
      const car = seg(lt, 0.2, dur - 0.4, E.inOutSine);
      q(g, '.carbody').setAttribute('transform', `translate(${1100 - car * 420} 1000) scale(-1 1)`); q(g, '.beam').setAttribute('opacity', 0.9 * seg(lt, 0.2, 0.3, E.linear)); q(g, '.beam').setAttribute('transform', `translate(${-car * 420} 0)`);
      const bark = 0.5 + 0.5 * Math.sin(t * 22); const dog = q(g, '.dog');
      q(dog, '.dog-jaw').setAttribute('transform', `translate(8 10) rotate(${14 * bark})`);
      q(dog, '.dog-head').setAttribute('transform', `translate(50 ${-92 - 6 * bark}) rotate(${-8 - 6 * bark})`);
      q(dog, '.dog-tail').setAttribute('transform', `translate(-44 -70) rotate(${Math.sin(t * 9) * 16})`);
      qa(dog, '.dl1,.dl2,.dl3,.dl4').forEach((l, i) => l.setAttribute('transform', `translate(0 ${-3 * bark * (i % 2)})`));
      const fx = q(g, '.barkfx'); const fa = seg(lt, 0.35, 0.25, E.outBack); fx.setAttribute('opacity', fa * (0.6 + 0.4 * bark)); fx.setAttribute('transform', `translate(380 820) scale(${0.9 + 0.15 * bark})`);
      q(g, '.hong').setAttribute('transform', `translate(150 -60) rotate(${-8 + Math.sin(t * 22) * 4}) scale(${1 + 0.1 * bark})`);
      dustUpdate(g, t, [0, 700, 720, 500]);
    }
  });
  UI.hud({ start: C('08', 3) + 0.2, end: T('09').start, icon: '🐕', label: 'หมาปั๊ม', value: '1', unit: 'ตัว · เห่าทุกคัน', cls: 'red' });

  // ============ ช็อต 14: ตู้แช่ 12 ตู้ ละลายใน 6 ชั่วโมง ============
  HF.shot({
    id: 'freezers', start: C('08', 5), end: T('09').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#151821"/>
        <rect x="-400" y="740" width="1520" height="800" fill="#1f232d"/>
        <g class="fzrow">${Array.from({ length: 12 }, (_, i) => { const x = 110 + i * 150; const s = 1.9; return `<g class="fzu" transform="translate(${x} 740) scale(${s})"><g class="fzglow" transform="translate(0 -110)"><rect x="-70" y="-120" width="140" height="240" rx="30" fill="url(#glow)" opacity=".35"/></g>${A.freezerUnit()}</g>`; }).join('')}</g>
        <g class="drips">${Array.from({ length: 10 }, (_, i) => `<ellipse class="drip" rx="4" ry="8" fill="#bfe9f7" opacity="0"/>`).join('')}</g>
        <g class="reflect" opacity=".25"><rect x="-400" y="740" width="1520" height="80" fill="url(#glow)"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const t6 = C('08', 6) - this.start;
      cam(q(g, '.cam'), { x: kf(lt, [[0, 420], [dur, 1500]], E.inOutSine), y: 640, s: kf(lt, [[0, 1.0], [t6, 1.0], [dur, 1.1]]) });
      qa(g, '.fzu').forEach((f, i) => { const a = seg(lt, 0.05 + i * 0.07, 0.25, E.outBack); f.setAttribute('opacity', a); q(f, '.fzled').setAttribute('fill', lt > t6 && Math.floor(t * 4) % 2 ? '#d7342c' : '#2bd46b'); q(f, '.fzglow').setAttribute('opacity', 0.8 + 0.2 * flicker(t, 10, i, .5)); });
      qa(g, '.drip').forEach((d, i) => { const k = lt > t6 ? ((t * 0.8 + i * 0.37) % 1) : 0; d.setAttribute('cx', 110 + i * 150 + (i % 2) * 40); d.setAttribute('cy', 700 + k * 70); d.setAttribute('opacity', lt > t6 ? (1 - k) * 0.8 : 0); });
    }
  });
  UI.hud({ start: C('08', 5), end: T('09').start, icon: '🧊', label: 'ตู้แช่', value: t => Math.min(12, Math.floor((t - C('08', 5)) / 0.07) + 1), unit: 'ตู้' });
  UI.hud({ start: C('08', 6), end: T('09').start, icon: '🌡', label: 'ละลายใน', value: t => { const s = 6 * 3600 - (t - C('08', 6)) * 60; return `${pad2(s / 3600)}:${pad2((s % 3600) / 60)}:${pad2(s % 60)}`; }, unit: 'ชม.', cls: 'red' });

  // ============ ช็อต 15: ดับไฟหน้าปั๊มทีละดวง ============
  HF.shot({
    id: 'lightsoff', start: T('09').start, end: C('09', 3),
    init(g) { g.innerHTML = stationWide(true); },
    update(lt, g, t, dur) {
      const t1 = C('09', 1) - this.start, t2 = C('09', 2) - this.start;
      cam(q(g, '.cam'), { x: 370, y: 880, s: kf(lt, [[0, 1.05], [dur, 1.0]]) });
      idleTon(q(g, '.ton'), t); dogIdle(q(g, '.dog'), t);
      qa(g, '.clight').forEach((l, i) => { const off = lt >= 0.25 + i * 0.22; op(l, off ? 0 : 0.9 * flicker(t, 24, i, .85)); });
      // ร้าน: ไฟดับ เหลือตู้แช่เรืองแสงเขียวฟ้า
      const shopDark = seg(lt, t1, 0.3, E.linear);
      q(g, '.glassfill').setAttribute('fill', shopDark > 0.5 ? '#16222c' : P.glass);
      q(g, '.shelves').setAttribute('opacity', 1 - shopDark * 0.85);
      qa(g, '.fzglass').forEach((f, i) => f.setAttribute('fill', lt >= t2 ? `rgba(120,230,255,${0.6 + 0.4 * flicker(t, 8, i, .6)})` : '#9fd6ec'));
      q(g, '.nightmask').setAttribute('opacity', 0.35 * seg(lt, 0.2, 1.4, E.linear));
      qa(g, '.z').forEach((z, i) => { z.setAttribute('transform', `translate(${560 + i * 90 - lt * 6} 728) scale(.3)`); zombieWalk(z, t * 2.2 + i); });
      dustUpdate(g, t, [0, 500, 720, 700], 0.5);
    }
  });
  UI.flash(T('09').start + 0.25, 0.06, 0.3); UI.flash(T('09').start + 0.47, 0.06, 0.3); UI.flash(T('09').start + 0.69, 0.06, 0.3);
  UI.hud({ start: T('09').start, end: C('09', 3), icon: '💡', label: 'ไฟหน้าปั๊ม', value: t => Math.max(0, 5 - Math.floor((t - T('09').start - 0.25) / 0.22) - 1), unit: 'ดวง' });
  UI.hud({ start: C('09', 2), end: C('09', 3), icon: '⚡', label: 'เครื่องปั่นไฟเลี้ยง', value: 'ตู้แช่', unit: 'เท่านั้น', cls: 'green' });

  // ============ ช็อต 16: ลากกระบะ 2 คันปิดทางเข้า (มุมบน) ============
  HF.shot({
    id: 'block', start: C('09', 3), end: C('09', 4),
    init(g) {
      const topPickup = (c) => `<g><rect x="-50" y="-110" width="100" height="220" rx="14" fill="${c}"/><rect x="-44" y="-100" width="88" height="70" rx="8" fill="#2b3a4a"/><rect x="-44" y="-10" width="88" height="100" rx="6" fill="#000" opacity=".2"/><rect x="-46" y="104" width="24" height="8" fill="${P.red}"/><rect x="22" y="104" width="24" height="8" fill="${P.red}"/><rect x="-46" y="-118" width="24" height="8" fill="${P.yellow}"/><rect x="22" y="-118" width="24" height="8" fill="${P.yellow}"/></g>`;
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#1a1c22"/>
        <rect x="-400" y="-100" width="1520" height="1700" fill="#2b2b33"/>
        <!-- ถนนใหญ่ด้านล่าง + ทางเข้าแนวตั้ง -->
        <rect x="-400" y="1000" width="1520" height="300" fill="#1c1f2c"/><rect x="-400" y="1146" width="1520" height="6" fill="${P.line}" opacity=".4"/>
        <rect x="240" y="300" width="240" height="760" fill="#3a3a44"/>
        <rect x="-400" y="-100" width="640" height="1100" fill="#34343d"/><rect x="480" y="-100" width="640" height="1100" fill="#34343d"/>
        <rect x="60" y="120" width="180" height="420" rx="8" fill="${P.white}"/><rect x="60" y="120" width="180" height="420" rx="8" fill="none" stroke="${P.orange}" stroke-width="8"/>
        <rect x="500" y="200" width="170" height="260" rx="6" fill="#e3dccb" stroke="#8e836f" stroke-width="3"/>
        <g class="gate" transform="translate(360 900)"><rect class="gatemark" x="-120" y="-80" width="240" height="160" rx="12" fill="none" stroke="${P.red}" stroke-width="5" stroke-dasharray="14 10" opacity="0"/></g>
        <g class="pk1" transform="translate(-200 900) rotate(90)">${topPickup('#eef0ee')}</g>
        <g class="pk2" transform="translate(920 900) rotate(90)">${topPickup('#c9cfd4')}</g>
        <g class="ton" transform="translate(360 1040) scale(.35)">${A.tonSide()}</g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: 760, s: kf(lt, [[0, 1.25], [dur, 1.0]], E.outCubic), r: kf(lt, [[0, -2], [dur, 0]]) });
      const k1 = seg(lt, 0.2, 1.1, E.outCubic), k2 = seg(lt, 0.6, 1.1, E.outCubic);
      q(g, '.pk1').setAttribute('transform', `translate(${lerp(-200, 255, k1)} 900) rotate(90)`);
      q(g, '.pk2').setAttribute('transform', `translate(${lerp(920, 465, k2)} 900) rotate(90)`);
      q(g, '.gatemark').setAttribute('opacity', seg(lt, 1.6, 0.3, E.linear) * (0.6 + 0.4 * Math.sin(t * 8)));
      const sh = shake(t, 3 * (seg(lt, 1.2, 0.1, E.linear) * (1 - seg(lt, 1.3, 0.3, E.linear)) + seg(lt, 1.6, 0.1, E.linear) * (1 - seg(lt, 1.7, 0.3, E.linear))), 40, 5);
      q(g, '.cam').setAttribute('transform', q(g, '.cam').getAttribute('transform') + ` translate(${sh.x} ${sh.y})`);
    }
  });
  UI.hud({ start: C('09', 3) + 0.2, end: C('09', 4), icon: '🛻', label: 'กระบะปิดทางเข้า', value: t => Math.min(2, Math.floor((t - C('09', 3) - 0.2) / 0.5) + 1), unit: 'คัน', cls: 'green' });

  // ============ ช็อต 17: สมุดจด + การ์ดเสบียง ============
  HF.shot({
    id: 'notebook', start: C('09', 4), end: T('10a').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        <rect x="-400" y="-100" width="1520" height="1700" fill="#2a2016"/>
        <g opacity=".5">${Array.from({ length: 12 }, (_, i) => `<rect x="-400" y="${-100 + i * 150}" width="1520" height="4" fill="#1a130c"/>`).join('')}</g>
        <ellipse class="torch" cx="360" cy="700" rx="520" ry="620" fill="url(#glow)" opacity=".5"/>
        <g transform="translate(360 760) rotate(-4)">
          <rect x="-300" y="-400" width="600" height="800" rx="8" fill="#000" opacity=".35" filter="url(#blur10)"/>
          <rect x="-290" y="-400" width="580" height="800" rx="6" fill="url(#paper)"/>
          <line x1="-210" y1="-400" x2="-210" y2="400" stroke="#e8b4a8" stroke-width="2"/>
          ${Array.from({ length: 16 }, (_, i) => `<line x1="-290" y1="${-340 + i * 48}" x2="290" y2="${-340 + i * 48}" stroke="#cfd8e6" stroke-width="1.5"/>`).join('')}
          <g class="ink" font-family="Sarabun" font-weight="700" font-size="30" fill="#2a3a6b">
            <text class="l0" x="-190" y="-352">คืนที่ 1 — ของที่มี</text>
            <text class="l1" x="-190" y="-256">น้ำดื่ม ......... 400 ขวด</text>
            <text class="l2" x="-190" y="-160">อาหาร ...... 12 คน / 3 อาทิตย์</text>
            <text class="l3" x="-190" y="-64">น้ำมัน ......... 6 แกลลอน</text>
            <text class="l4" x="-190" y="32">ไฟ ........ เลี้ยงตู้แช่เท่านั้น</text>
            <text class="l5" x="-190" y="128">กระบะปิดทางเข้า 2 คัน ✓</text>
          </g>
          <g class="pen"><rect x="-10" y="-200" width="20" height="230" rx="6" fill="#1b1f27" transform="rotate(35)"/><path d="M0 30 l-8 -8 h16z" fill="#d8d3c4" transform="rotate(35)"/></g>
        </g>
        <g transform="translate(120 1180) rotate(-30)"><rect x="-90" y="-22" width="180" height="44" rx="10" fill="#1b1f27"/><rect x="60" y="-26" width="40" height="52" rx="8" fill="#2b2f3a"/><circle cx="100" cy="0" r="22" fill="#fff6d0" filter="url(#softglow)"/></g>
        <g transform="translate(600 1160)"><circle r="40" fill="#1b1f27"/><rect x="-14" y="-14" width="28" height="28" rx="4" fill="${P.red}"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 360, y: kf(lt, [[0, 760], [dur, 700]], E.inOutSine), s: kf(lt, [[0, 1.15], [dur, 1.0]], E.outCubic) });
      q(g, '.torch').setAttribute('opacity', 0.45 + 0.1 * flicker(t, 12, 4, .4));
      const starts = [0.1, C('09', 5) - this.start, C('09', 6) - this.start, C('09', 7) - this.start + 0.1, C('09', 7) - this.start + 0.5, C('09', 7) - this.start + 0.8];
      [0, 1, 2, 3, 4, 5].forEach(i => { const el = q(g, '.l' + i); const k = seg(lt, starts[i], 0.6, E.linear); const full = el.dataset.full || (el.dataset.full = el.textContent); el.textContent = full.slice(0, Math.ceil(full.length * k)); });
      const li = Math.max(0, starts.findIndex(s => lt < s) - 1); const row = li < 0 ? 5 : li; const k = seg(lt, starts[row], 0.6, E.linear);
      q(g, '.pen').setAttribute('transform', `translate(${-190 + 380 * k} ${-352 + row * 96 + Math.sin(t * 30) * 2})`);
    }
  });
  UI.inventory({ start: C('09', 5) - 0.1, end: T('10a').start, title: 'เสบียง · คืนที่ 1', icon: '📋', rows: [
    { ic: '💧', label: 'น้ำดื่ม', value: k => fmt(Math.round(400 * k)), unit: ' ขวด', bar: 0.9, at: C('09', 5) },
    { ic: '🍚', label: 'อาหาร · 12 คน', value: k => Math.round(3 * k), unit: ' อาทิตย์', bar: 0.7, at: C('09', 6) },
    { ic: '🛢', label: 'น้ำมันสำรอง', value: k => Math.round(6 * k), unit: ' แกลลอน', bar: 0.5, at: C('09', 7) + 0.1 },
  ] });

  // ============ ช็อต 18: หมาจ้องไปหลังปั๊ม (ความเงียบ 1 วิ) ============
  HF.shot({
    id: 'dogstare', start: T('10a').start, end: T('10b').start,
    init(g) {
      g.innerHTML = `<g class="cam">
        ${A.skyNight()}
        <g filter="url(#blur10)"><rect x="-400" y="700" width="1520" height="800" fill="#1d1d26"/><g transform="translate(560 760) scale(.9)">${A.restroomBlock()}</g><g transform="translate(360 300) scale(1.3)">${A.canopy(900, 4)}</g></g>
        <rect x="-400" y="1000" width="1520" height="400" fill="#23232c"/>
        <g class="face" transform="translate(300 900) scale(1.3)">${A.dogFace()}</g>
        <g class="halo"><ellipse cx="360" cy="400" rx="400" ry="300" fill="url(#glow)" opacity=".15"/></g>
      </g>`;
      qa(g, '.cone').forEach(c => c.setAttribute('opacity', .3));
    },
    update(lt, g, t, dur) {
      cam(q(g, '.cam'), { x: 320, y: 820, s: kf(lt, [[0, 1.0], [dur, 1.22]], E.inOutSine) });
      const turn = seg(lt, 0.3, 0.6, E.outBack);
      const f = q(g, '.face');
      q(f, '.earL').setAttribute('transform', `translate(-120 -140) rotate(${-8 * turn})`); q(f, '.earR').setAttribute('transform', `translate(120 -140) rotate(${-14 * turn})`);
      q(f, '.eyeL').setAttribute('transform', `translate(${-62 + 10 * turn} ${-40 - 2 * turn})`); q(f, '.eyeR').setAttribute('transform', `translate(${62 + 10 * turn} ${-40 - 2 * turn})`);
      f.setAttribute('transform', `translate(${300 + 20 * turn} ${900 + Math.sin(t * 1.3) * 2}) rotate(${6 * turn}) scale(1.3)`);
    }
  });
  UI.fade(T('10a').start - 0.2, T('10a').start + 0.3, 1, 0);

  // ============ ช็อต 19: ประตูห้องน้ำ — ล็อกจากข้างใน ============
  HF.shot({
    id: 'door', start: T('10b').start, end: TIMELINE.endCardStart,
    init(g) {
      g.innerHTML = `<g class="cam">
        <g transform="translate(360 1060)">${A.doorClose()}</g>
        <ellipse class="torch" cx="360" cy="600" rx="420" ry="700" fill="url(#glow)" opacity=".4"/>
        <g class="lockicon" transform="translate(490 730)" opacity="0"><circle r="54" fill="${P.red}"/><circle class="lring" r="54" fill="none" stroke="${P.red}" stroke-width="4"/><text y="14" font-size="44" text-anchor="middle">🔒</text></g>
        <g class="darkover"><rect x="-400" y="-100" width="1520" height="1700" fill="#000" opacity=".28"/></g>
      </g>`;
    },
    update(lt, g, t, dur) {
      const t1 = C('10b', 1) - this.start, t2 = C('10b', 2) - this.start;
      const s = kf(lt, [[0, 1.0], [t1, 1.15], [t1 + 0.8, 1.9], [t2, 1.9], [t2 + 0.8, 1.15], [dur, 1.25]], E.inOutCubic);
      const cy = kf(lt, [[0, 640], [t1, 660], [t1 + 0.8, 740], [t2, 740], [t2 + 0.8, 900], [dur, 960]], E.inOutCubic);
      const cx = kf(lt, [[0, 360], [t1, 380], [t1 + 0.8, 470], [t2, 470], [t2 + 0.8, 360], [dur, 360]], E.inOutCubic);
      cam(q(g, '.cam'), { x: cx, y: cy, s });
      q(g, '.torch').setAttribute('opacity', 0.25 + 0.08 * flicker(t, 10, 3, .4));
      const la = seg(lt, t1 + 0.1, 0.35, E.outBack) * (1 - seg(lt, t2 + 0.3, 0.4, E.linear)); q(g, '.lockicon').setAttribute('opacity', la); q(g, '.lockicon').setAttribute('transform', `translate(490 730) scale(${la})`);
      q(g, '.lring').setAttribute('r', 54 + ((t * 50) % 50)); q(g, '.lring').setAttribute('opacity', 1 - ((t * 50) % 50) / 50);
      const gl = lt > t2 ? 0.55 + 0.45 * flicker(t, 26, 7, .2) : 0; q(g, '.gaplight').setAttribute('opacity', gl * seg(lt, t2 + 0.2, 0.5, E.linear));
      q(g, '.feet').setAttribute('opacity', seg(lt, t2 + 1.2, 0.5, E.linear));
    }
  });
  UI.fade(TIMELINE.endCardStart - 0.5, TIMELINE.endCardStart, 0, 1);

  // ============ ช็อต 20: การ์ด "ตอนที่ 2" ============
  HF.shot({ id: 'end', start: TIMELINE.endCardStart, end: TIMELINE.total + 1, init(g) { g.innerHTML = '<rect width="720" height="1280" fill="#0b0b0f"/>'; } });
  UI.endcard({ start: TIMELINE.endCardStart, end: TIMELINE.total + 1, title: 'ตอนที่ 2', teaser: 'ใครอยู่ในห้องน้ำ และทำไมเขาถึงไม่ตอบ' });
  UI.fade(TIMELINE.total - 0.6, TIMELINE.total, 0, 1);
})();
