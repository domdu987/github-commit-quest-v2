// "75 วันของพ่อ" widgets, built on icons5.js (iconBox, popSquash, withStk, fourStar) and ui4/fx helpers.

// smartphone illustration (son's new phone): dark body, glossy gradient screen, triple camera
function phoneSVG(w, h, screen = ['#7b5cff', '#ff6fa8']) {
  return `<svg width="${w}" height="${h}" viewBox="0 0 150 260"><defs><linearGradient id="phg${w}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${screen[0]}"/><stop offset="1" stop-color="${screen[1]}"/></linearGradient></defs>
  <rect x="6" y="4" width="138" height="252" rx="26" fill="#1c1d26" stroke="#fff" stroke-width="5"/>
  <rect x="14" y="14" width="122" height="232" rx="19" fill="url(#phg${w})"/>
  <path d="M14,90 L136,40 L136,70 L14,140 Z" fill="#fff" opacity=".18"/>
  <rect x="58" y="20" width="34" height="8" rx="4" fill="#1c1d26"/>
  <circle cx="75" cy="150" r="26" fill="#fff" opacity=".25"/><path d="M68,138 L88,150 L68,162 Z" fill="#fff"/></svg>`;
}
function oldPhoneSVG(w, h, lit = false, text = '') {
  return `<svg width="${w}" height="${h}" viewBox="0 0 120 230">
  <rect x="6" y="4" width="108" height="222" rx="26" fill="#4a4d57" stroke="#fff" stroke-width="5"/>
  <rect x="18" y="20" width="84" height="68" rx="8" fill="${lit ? '#c8f0c0' : '#7f9a86'}"/>
  ${text ? `<text x="60" y="62" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="17" fill="#1f3a26">${text}</text>` : ''}
  ${Array.from({ length: 12 }, (_, i) => `<rect x="${22 + (i % 3) * 27}" y="${104 + Math.floor(i / 3) * 28}" width="22" height="20" rx="6" fill="#2e3038"/>`).join('')}
  <rect x="2" y="150" width="20" height="30" fill="#e9e2cf" opacity=".9" transform="rotate(-8 12 165)"/></svg>`;
}

// ---------------- shopping card: product, price counter, tap-to-buy with a finger ----------------
function productCard(parent, x, y, w) {
  const c = cardEl(parent, 'card shop', x, y, w);
  const hd = html('div', 'lbl', c.c); hd.innerHTML = `<svg width="30" height="30" viewBox="0 0 24 24"><path d="M5,8 L19,8 L18,21 L6,21 Z" fill="#ff7a45"/><path d="M9,8 Q9,3 12,3 Q15,3 15,8" fill="none" stroke="#ff7a45" stroke-width="2"/></svg><span>ช้อปออนไลน์</span>`;
  const row = html('div', 'shoprow', c.c);
  const ph = html('div', 'shopph', row); ph.innerHTML = phoneSVG(118, 205);
  const info = html('div', 'shopinfo', row);
  html('div', 'shopname', info, 'มือถือรุ่นใหม่ล่าสุด');
  const stars = html('div', 'shopstars', info, '★★★★★');
  const pr = html('div', 'shopprice', info); html('span', '', pr, '฿');
  const od = new Odometer(pr, 2); html('span', '', pr, ',000');
  const btn = html('div', 'shopbtn', info, 'สั่งซื้อเลย');
  const ok = html('div', 'shopok', info); ok.innerHTML = '<svg width="34" height="34" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="#2f9e5b"/><path d="M11,21 L17,27 L29,14" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>สั่งซื้อแล้ว';
  const hand = html('div', 'tapHand', c.c); hand.innerHTML = '<svg width="74" height="90" viewBox="0 0 74 90"><path d="M24,40 L24,10 Q24,2 31,2 Q38,2 38,10 L38,34 L40,30 Q46,26 50,32 L52,36 Q58,32 62,38 L63,42 Q69,40 71,46 L71,64 Q71,86 50,88 L36,88 Q22,86 14,72 L4,52 Q2,44 9,42 Q14,41 18,48 L24,58 Z" fill="#ffd9b8" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>';
  const ripple = html('div', 'tapRipple', c.c);
  return {
    c, ph,
    update(t, tin, tprice, ttap) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.6);
      popSquash(ph, t, tin + 0.2, `rotate(${(Math.sin(t * 2) * 3).toFixed(2)}deg)`);
      stars.style.opacity = fadeIn(t, tin + 0.4, 0.2);
      const v = rollValue(t, tprice, tprice + 0.8, 0, 30); od.set(v.v, v.speed);
      const land = 1 + 0.25 * Math.exp(-Math.pow((t - tprice - 0.85) * 7, 2));
      pr.style.transform = `scale(${land.toFixed(3)})`;
      // finger glides in, presses, button flips to "ordered"
      const hk = ease.outCubic(prog(t, ttap - 0.6, ttap - 0.05));
      const press = t > ttap - 0.05 && t < ttap + 0.15 ? 0.85 : 1;
      hand.style.opacity = (fadeIn(t, ttap - 0.6, 0.15) * (1 - prog(t, ttap + 0.5, ttap + 0.8))).toFixed(3);
      hand.style.transform = `translate(${lerp(260, 0, hk).toFixed(1)}px, ${lerp(160, 0, hk).toFixed(1)}px) scale(${press})`;
      const rk = prog(t, ttap, ttap + 0.5);
      ripple.style.opacity = rk > 0 && rk < 1 ? (1 - rk).toFixed(3) : 0;
      ripple.style.transform = `scale(${(0.3 + rk * 1.6).toFixed(3)})`;
      const done = t >= ttap + 0.05;
      btn.style.display = done ? 'none' : 'block';
      ok.style.display = done ? 'flex' : 'none';
      if (done) popSquash(ok, t, ttap + 0.05, '', 0);
      btn.style.transform = `scale(${(1 + 0.05 * Math.sin(t * 8)).toFixed(3)})`;
    },
  };
}
function fxSvgHost(parent) { return svg('svg', { width: 1, height: 1, style: 'position:absolute;left:0;top:0;overflow:visible' }, parent); }

// ---------------- stopwatch chip ----------------
function stopwatchChip(parent, x, y) {
  const ch = html('div', 'chip big', parent); ch.style.left = x + 'px'; ch.style.top = y + 'px';
  const b = iconBox(ch, 54, 54, '0 0 100 100');
  svg('rect', withStk({ x: 42, y: 4, width: 16, height: 12, rx: 4, fill: '#cf483d' }, 4), b.s);
  svg('circle', withStk({ cx: 50, cy: 56, r: 38, fill: rad2(b.defs, [[0, '#ffffff'], [1, '#e9eef8']], { cx: 0.35, cy: 0.3, r: 0.8 }) }, 6), b.s);
  svg('circle', { cx: 50, cy: 56, r: 38, fill: 'none', stroke: '#cf483d', 'stroke-width': 5 }, b.s);
  const arc = svg('path', { fill: '#ffb3a8', opacity: 0.8 }, b.s);
  const hand = svg('line', { x1: 50, y1: 56, x2: 50, y2: 26, stroke: '#2b3157', 'stroke-width': 5, 'stroke-linecap': 'round' }, b.s);
  svg('circle', { cx: 50, cy: 56, r: 5, fill: '#cf483d' }, b.s);
  html('span', '', ch, 'ใช้เวลาแค่');
  const bb = html('b', '', ch); const od = new Odometer(bb, 1); html('span', '', ch, 'นาที');
  return {
    el: ch,
    update(t, t0) {
      popSquash(ch, t, t0, '', -8);
      const k = clamp((t - t0) / 1.0);
      const a = k * 300;
      hand.setAttribute('transform', `rotate(${(t > t0 ? (t - t0) * 360 : 0).toFixed(1)} 50 56)`);
      const e = rad(a - 90);
      arc.setAttribute('d', a > 1 ? `M50,56 L50,20 A36,36 0 ${a > 180 ? 1 : 0} 1 ${(50 + Math.cos(e) * 36).toFixed(1)},${(56 + Math.sin(e) * 36).toFixed(1)} Z` : '');
      const v = rollValue(t, t0 + 0.1, t0 + 0.9, 0, 5); od.set(v.v, v.speed);
    },
  };
}

// ---------------- sun badge with spinning rays and a thermometer rising to 38°C ----------------
function sunThermo(parent, x, y) {
  const wrap = html('div', 'badge2', parent); wrap.style.left = x + 'px'; wrap.style.top = y + 'px';
  const b = iconBox(wrap, 170, 150, '0 0 170 150');
  const rays = svg('g', { transform: 'translate(64,74)' }, b.s);
  for (let i = 0; i < 10; i++) svg('path', { d: 'M-7,-44 L7,-44 L0,-66 Z', fill: '#ffb238', transform: `rotate(${i * 36})` }, rays);
  svg('circle', withStk({ cx: 64, cy: 74, r: 38, fill: rad2(b.defs, [[0, '#fff3a0'], [1, '#ffb238']], { cx: 0.4, cy: 0.35, r: 0.7 }) }, 6), b.s);
  svg('path', { d: 'M48,80 Q64,94 80,80', stroke: '#c96b1d', 'stroke-width': 4, fill: 'none', 'stroke-linecap': 'round' }, b.s);
  svg('circle', { cx: 52, cy: 66, r: 4, fill: '#c96b1d' }, b.s); svg('circle', { cx: 76, cy: 66, r: 4, fill: '#c96b1d' }, b.s);
  svg('rect', withStk({ x: 128, y: 14, width: 22, height: 100, rx: 11, fill: '#ffffff' }, 5), b.s);
  svg('circle', withStk({ cx: 139, cy: 120, r: 17, fill: '#e2382c' }, 5), b.s);
  const lvl = svg('rect', { x: 133, y: 100, width: 12, height: 20, rx: 6, fill: '#e2382c' }, b.s);
  const lab = html('div', 'thermoLab', wrap); const od = new Odometer(lab, 2); html('span', '', lab, '°C');
  return {
    el: wrap,
    update(t, t0) {
      popSquash(wrap, t, t0, '', -12);
      rays.setAttribute('transform', `translate(64,74) rotate(${(t * 40).toFixed(1)}) scale(${(1 + 0.06 * Math.sin(t * 6)).toFixed(3)})`);
      const k = ease.outCubic(prog(t, t0 + 0.2, t0 + 1.1));
      const h = 20 + 72 * k;
      setA(lvl, { y: (120 - h).toFixed(1), height: h.toFixed(1) });
      const v = rollValue(t, t0 + 0.2, t0 + 1.1, 25, 38); od.set(v.v, v.speed);
      lab.style.color = k > 0.95 && Math.sin(t * 10) > 0 ? '#ff3b2f' : '#e2382c';
    },
  };
}

// ---------------- banknote stack ----------------
function moneyCard(parent, x, y) {
  const c = cardEl(parent, 'card money', x, y, 420);
  const row = html('div', 'moneyrow', c.c);
  const b = iconBox(row, 120, 92, '0 0 120 92');
  const notes = [0, 1, 2].map(i => { const g = svg('g', {}, b.s); svg('rect', withStk({ x: 6, y: 18, width: 104, height: 56, rx: 8, fill: ['#8f7fb8', '#a493cc', '#b9a9de'][i] }, 4), g); svg('circle', { cx: 58, cy: 46, r: 15, fill: '#fff', opacity: 0.5 }, g); svg('text', { x: 58, y: 52, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 16, fill: '#4b3f7a' }, g).textContent = '1000'; return g; });
  const tx = html('div', 'moneytx', row); html('small', '', tx, 'เงินก้อนนี้'); html('b', '', tx, '฿30,000');
  return {
    c,
    update(t, t0) {
      enter3d(c.c, t, t0, 'swingLeft'); shine(c.sh, t, t0 + 0.5);
      notes.forEach((g, i) => { const k = spring(t, t0 + 0.12 + i * 0.08, 14, 6); g.setAttribute('transform', `translate(${((i - 1) * 6).toFixed(1)},${((1 - k) * -40 + (i - 1) * -4).toFixed(1)}) rotate(${((i - 1) * 8 + Math.sin(t * 2 + i) * 2).toFixed(1)} 58 46)`); g.setAttribute('opacity', fadeIn(t, t0 + 0.12 + i * 0.08, 0.1)); });
    },
  };
}

// ---------------- big sweat drop that wobbles and drips ----------------
function sweatDrop(parent, x, y, size = 110) {
  const wrap = html('div', 'badge2', parent); wrap.style.left = x + 'px'; wrap.style.top = y + 'px';
  const b = iconBox(wrap, size, size * 1.3, '-50 -70 100 130');
  const drop = svg('path', withStk({ d: 'M0,-60 C14,-36 36,-12 36,10 A36,36 0 1 1 -36,10 C-36,-12 -14,-36 0,-60 Z', fill: lin(b.defs, [[0, '#bfe9ff'], [1, '#4aa8e8']]) }, 6), b.s);
  svg('ellipse', { cx: -13, cy: 4, rx: 7, ry: 14, fill: '#fff', opacity: 0.6, transform: 'rotate(20 -13 4)' }, b.s);
  const small = svg('path', { d: 'M0,-10 C4,-4 8,0 8,4 A8,8 0 1 1 -8,4 C-8,0 -4,-4 0,-10 Z', fill: '#4aa8e8' }, b.s);
  return {
    el: wrap,
    update(t, t0) {
      popSquash(wrap, t, t0, '', 10);
      const w = Math.sin(t * 5) * 0.05;
      drop.setAttribute('transform', `scale(${(1 + w).toFixed(3)},${(1 - w).toFixed(3)})`);
      const q = ((t - t0) % 1.1) / 1.1;
      small.setAttribute('transform', `translate(0,${(46 + q * q * 60).toFixed(1)})`);
      small.setAttribute('opacity', t > t0 ? (1 - q).toFixed(2) : 0);
    },
  };
}

// ---------------- "75 วัน" calendar card ----------------
function daysBigCard(parent, x, y) {
  const c = cardEl(parent, 'card days75', x, y, 420);
  const row = html('div', 'moneyrow', c.c);
  const cal = calendarFlip(row, 110);
  const tx = html('div', 'moneytx', row); html('small', '', tx, 'เท่ากับเหงื่อพ่อ');
  const bb = html('b', 'big75', tx); const od = new Odometer(bb, 2); html('span', '', bb, ' วัน');
  return {
    c,
    update(t, t0) {
      enter3d(c.c, t, t0, 'flipDown'); shine(c.sh, t, t0 + 1.0);
      const v = rollValue(t, t0 + 0.1, t0 + 0.95, 0, 75); od.set(v.v, v.speed);
      cal.update(t, Math.max(1, Math.round(v.v)), t > t0 + 0.1 && t < t0 + 0.95);
      const land = 1 + 0.3 * Math.exp(-Math.pow((t - t0 - 1.0) * 6, 2));
      bb.style.transform = `scale(${land.toFixed(3)})`;
    },
  };
}

// ---------------- name tag: พ่อ · ช่างปูน ----------------
function nameTag(parent, x, y) {
  const c = html('div', 'chip big nametag', parent); c.style.left = x + 'px'; c.style.top = y + 'px';
  const b = iconBox(c, 58, 50, '0 0 100 86');
  svg('path', withStk({ d: 'M10,62 C10,14 90,10 92,62 Z', fill: lin(b.defs, [[0, '#ffd66b'], [1, '#e8a92c']]) }, 6), b.s);
  svg('rect', withStk({ x: 2, y: 58, width: 98, height: 14, rx: 7, fill: '#e0a12c' }, 4), b.s);
  svg('path', { d: 'M30,26 Q38,18 50,18', stroke: '#fff7d6', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round', opacity: 0.7 }, b.s);
  html('span', '', c, 'พ่อ · ช่างปูน');
  return { el: c, update(t, t0) { popSquash(c, t, t0, '', -8); b.s.setAttribute('transform', `rotate(${(Math.sin(t * 3) * 6).toFixed(2)})`); } };
}

// ---------------- wage card: four 100-baht coins drop into a stack, 400 บาท/วัน ----------------
function wageCard(parent, x, y) {
  const c = cardEl(parent, 'card wage', x, y, 420);
  html('div', 'lbl', c.c, 'ค่าแรงพ่อ');
  const row = html('div', 'moneyrow', c.c);
  const b = iconBox(row, 110, 120, '0 0 110 120');
  const coins = [0, 1, 2, 3].map(i => { const g = svg('g', {}, b.s); svg('ellipse', withStk({ cx: 55, cy: 0, rx: 40, ry: 13, fill: '#e8b53c' }, 4), g); svg('ellipse', { cx: 55, cy: -3, rx: 30, ry: 8, fill: '#ffd66b' }, g); svg('text', { x: 55, y: 2, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 12, fill: '#a8771c' }, g).textContent = '100'; return g; });
  const tx = html('div', 'moneytx', row);
  const bb = html('b', '', tx); const od = new Odometer(bb, 3); html('small', '', tx, 'บาท / วัน');
  return {
    c,
    update(t, t0) {
      enter3d(c.c, t, t0, 'swingRight'); shine(c.sh, t, t0 + 1.0);
      coins.forEach((g, i) => {
        const tt = t0 + 0.25 + i * 0.16, x = t - tt, yEnd = 104 - i * 16;
        let yy = x < 0 ? -60 : x < 0.18 ? lerp(-60, yEnd, Math.pow(x / 0.18, 2)) : yEnd - 6 * Math.exp(-(x - 0.18) * 10) * Math.abs(Math.sin((x - 0.18) * 20));
        g.setAttribute('transform', `translate(0,${yy.toFixed(1)})`); g.setAttribute('opacity', x < 0 ? 0 : 1);
      });
      const v = rollValue(t, t0 + 0.25, t0 + 0.25 + 0.64, 0, 400); od.set(v.v, v.speed);
    },
  };
}

// ---------------- equation: [phone 30,000] ÷ [coin 400] = [calendar 75 วัน] ----------------
function equationCard(parent, x, y, w) {
  const c = cardEl(parent, 'card eq', x, y, w);
  const row = html('div', 'eqrow', c.c);
  const term = (icon, txt, cls = '') => { const d = html('div', 'eqterm ' + cls, row); d.innerHTML = icon + `<b>${txt}</b>`; return d; };
  const op = s => html('div', 'eqop', row, s);
  const a = term(phoneSVG(44, 76), '30,000'), o1 = op('÷');
  const bb = term('<svg width="60" height="60" viewBox="-30 -30 60 60"><circle r="26" fill="#e8b53c" stroke="#fff" stroke-width="4"/><circle r="18" fill="#ffd66b"/><text y="6" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="16" fill="#a8771c">฿</text></svg>', '400'), o2 = op('=');
  const cc = term('<svg width="60" height="60" viewBox="0 0 100 100"><rect x="10" y="16" width="80" height="76" rx="12" fill="#fff" stroke="#e0574b" stroke-width="6"/><path d="M10,28 Q10,16 22,16 L78,16 Q90,16 90,28 L90,38 L10,38 Z" fill="#e0574b"/><text x="50" y="78" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#2f2c33">75</text></svg>', '75 วัน', 'hot');
  const parts = [a, o1, bb, o2, cc];
  return {
    c,
    update(t, t0) {
      enter3d(c.c, t, t0, 'flipDown');
      parts.forEach((p, i) => popSquash(p, t, t0 + 0.12 + i * 0.13, '', i === 4 ? -14 : -6));
      cc.style.boxShadow = t > t0 + 0.7 ? `0 0 ${(18 + 10 * Math.sin(t * 8)).toFixed(1)}px rgba(224,87,75,.7)` : 'none';
    },
  };
}

// ---------------- big cracked keypad phone with age badge ----------------
function oldPhoneCard(parent, x, y) {
  const wrap = html('div', 'oldph', parent); wrap.style.left = x + 'px'; wrap.style.top = y + 'px';
  const b = iconBox(wrap, 300, 560, '0 0 120 224');
  b.s.innerHTML += `<rect x="6" y="4" width="108" height="216" rx="26" fill="#4a4d57" stroke="#fff" stroke-width="4"/><rect x="10" y="8" width="20" height="200" rx="10" fill="#fff" opacity=".08"/>
    <rect x="18" y="20" width="84" height="66" rx="7" fill="#89a58f"/><text x="60" y="48" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="15" fill="#22382a">12:05</text>
    <rect x="24" y="26" width="3" height="5" fill="#22382a"/><rect x="29" y="23" width="3" height="8" fill="#22382a"/><rect x="34" y="20" width="3" height="11" fill="#22382a" opacity=".3"/>
    <rect x="80" y="25" width="16" height="7" rx="2" fill="none" stroke="#22382a" stroke-width="1.5"/><rect x="82" y="27" width="3" height="3" fill="#c0392b"/>
    <text x="60" y="76" text-anchor="middle" font-family="Kanit" font-weight="500" font-size="10" fill="#22382a">ไม่มีสายที่ไม่ได้รับ</text>`;
  const keys = Array.from({ length: 12 }, (_, i) => svg('rect', { x: 22 + (i % 3) * 27, y: 100 + Math.floor(i / 3) * 27, width: 22, height: 19, rx: 6, fill: '#2e3038' }, b.s));
  svg('rect', { x: 0, y: 140, width: 22, height: 34, fill: '#e9e2cf', opacity: 0.92, transform: 'rotate(-10 11 157)' }, b.s);
  const cracks = ['M60,20 L54,40 L64,52 L50,70 L56,86', 'M54,40 L34,46 L22,40', 'M64,52 L86,58 L100,48', 'M50,70 L30,82', 'M60,20 L74,30 L92,24'].map(d => svg('path', { d, fill: 'none', stroke: '#f6fff6', 'stroke-width': 1.6, pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, b.s));
  const badge = html('div', 'chip big agebadge', wrap); badge.innerHTML = '<span>ใช้มาแล้ว</span><b>10</b><span>ปี</span>';
  return {
    el: wrap,
    update(t, tin, tkeys, tage, tcrack) {
      popSquash(wrap, t, tin, `rotate(${(Math.sin(t * 1.4) * 3).toFixed(2)}deg)`, -14);
      keys.forEach((k, i) => k.setAttribute('fill', t > tkeys + i * 0.06 && t < tkeys + i * 0.06 + 0.25 ? '#8fd18a' : '#2e3038'));
      popSquash(badge, t, tage, '', 12);
      cracks.forEach((cr, i) => cr.setAttribute('stroke-dashoffset', (1 - ease.outCubic(prog(t, tcrack + i * 0.07, tcrack + i * 0.07 + 0.25))).toFixed(3)));
      const sh = t > tcrack && t < tcrack + 0.3 ? Math.sin(t * 80) * 4 : 0;
      b.s.style.transform = `translateX(${sh.toFixed(1)}px)`;
    },
  };
}

// ---------------- app bubbles rising from the son's phone ----------------
function appBubbles(parent, t0s) {
  const defs = [['#ff4d6d', 'heart'], ['#4a7bd8', 'chat'], ['#ff7a45', 'play'], ['#9b5de5', 'note'], ['#2f9e5b', 'bag'], ['#f2c14e', 'star'], ['#ff4d6d', 'heart'], ['#4a7bd8', 'chat']];
  const glyph = { heart: `<path d="${heartPath(0, 1, 8)}" fill="#fff"/>`, chat: '<path d="M-10,-7 L10,-7 Q13,-7 13,-4 L13,4 Q13,7 10,7 L-2,7 L-8,12 L-7,7 L-10,7 Q-13,7 -13,4 L-13,-4 Q-13,-7 -10,-7 Z" fill="#fff"/>', play: '<path d="M-5,-8 L9,0 L-5,8 Z" fill="#fff"/>', note: '<path d="M-3,8 A4,4 0 1 1 -3,7 L-3,-9 L8,-12 L8,4 A4,4 0 1 1 8,3 L8,-6 L-1,-4" fill="#fff"/>', bag: '<path d="M-8,-3 L8,-3 L7,10 L-7,10 Z M-4,-3 Q-4,-9 0,-9 Q4,-9 4,-3" fill="#fff" stroke="#fff" stroke-width="2"/>', star: `<path d="${fourStar(10)}" fill="#fff"/>` };
  return defs.map(([col, g], i) => {
    const el = svg('g', { opacity: 0 }, parent);
    svg('circle', { r: 24, fill: col, stroke: '#fff', 'stroke-width': 4 }, el);
    el.innerHTML += glyph[g];
    return { el, t0: t0s + i * 0.32, dx: (i % 2 ? 1 : -1) * (60 + (i * 37) % 90), ph: i };
  });
}
function updateBubbles(bs, t, ox, oy) {
  bs.forEach(b => {
    const x = t - b.t0, life = 2.2;
    if (x < 0 || x > life) { b.el.setAttribute('opacity', 0); return; }
    const k = x / life, sp = spring(t, b.t0, 16, 6);
    b.el.setAttribute('transform', `translate(${(ox + b.dx * ease.outCubic(Math.min(1, k * 1.6)) + Math.sin(x * 3 + b.ph) * 10).toFixed(1)},${(oy - 360 * ease.outCubic(k)).toFixed(1)}) scale(${(clamp(sp, 0, 1.3) * (1 - 0.3 * k)).toFixed(3)})`);
    b.el.setAttribute('opacity', (k < 0.75 ? 1 : (1 - k) / 0.25).toFixed(3));
  });
}

// ---------------- call log: พ่อ — 0 ครั้ง ----------------
function callLogCard(parent, x, y, w) {
  const c = cardEl(parent, 'card calllog', x, y, w);
  const hd = html('div', 'lbl', c.c); hd.innerHTML = '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M6,3 L10,3 L11,8 L8.5,9.5 Q10,13.5 14.5,15.5 L16,13 L21,14 L21,18 Q21,21 18,21 Q4,20 3,6 Q3,3 6,3 Z" fill="#2f9e5b"/></svg><span>ประวัติการโทร</span>';
  const rowEl = html('div', 'logrow', c.c);
  const av = html('div', 'logav', rowEl); av.innerHTML = dadAvatar();
  const nm = html('div', 'logname', rowEl); nm.innerHTML = '<b>พ่อ</b><small>โทรล่าสุด: —</small>';
  const cnt = html('div', 'logcount', rowEl); const od = new Odometer(cnt, 1); html('small', '', cnt, 'ครั้ง');
  const empty = html('div', 'logempty', c.c, 'ยังไม่เคยโทรหาพ่อ');
  return {
    c,
    update(t, tin, tzero) {
      enter3d(c.c, t, tin, 'swingLeft'); shine(c.sh, t, tin + 0.5);
      od.set(0, 0);
      const zk = t > tzero ? Math.exp(-(t - tzero) * 3) : 0;
      cnt.style.transform = `scale(${(1 + 0.5 * zk).toFixed(3)}) translateX(${(Math.sin(t * 60) * 6 * zk).toFixed(1)}px)`;
      cnt.style.color = t > tzero ? '#e2382c' : '#6b6670';
      empty.style.opacity = fadeIn(t, tzero, 0.2);
      empty.style.transform = `translateY(${((1 - spring(t, tzero, 14, 7)) * 16).toFixed(1)}px)`;
    },
  };
}

// ---------------- son's phone screen: contact "พ่อ" → tap call → calling rings ----------------
function callScreen(parent, x, y) {
  const wrap = html('div', 'callscr', parent); wrap.style.left = x + 'px'; wrap.style.top = y + 'px';
  const scr = html('div', 'callinner', wrap);
  const rings = [0, 1, 2].map(() => html('i', 'cring', scr));
  const av = html('div', 'callav', scr); av.innerHTML = dadAvatar();
  html('div', 'callname', scr, 'พ่อ');
  const st = html('div', 'callstatus', scr, 'มือถือ');
  const btn = html('div', 'callbtn', scr); btn.innerHTML = '<svg width="40" height="40" viewBox="0 0 24 24"><path d="M6,3 L10,3 L11,8 L8.5,9.5 Q10,13.5 14.5,15.5 L16,13 L21,14 L21,18 Q21,21 18,21 Q4,20 3,6 Q3,3 6,3 Z" fill="#fff"/></svg>';
  const hand = html('div', 'tapHand', wrap); hand.innerHTML = '<svg width="74" height="90" viewBox="0 0 74 90"><path d="M24,40 L24,10 Q24,2 31,2 Q38,2 38,10 L38,34 L40,30 Q46,26 50,32 L52,36 Q58,32 62,38 L63,42 Q69,40 71,46 L71,64 Q71,86 50,88 L36,88 Q22,86 14,72 L4,52 Q2,44 9,42 Q14,41 18,48 L24,58 Z" fill="#ffd9b8" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>';
  return {
    el: wrap,
    update(t, tin, ttap) {
      popSquash(wrap, t, tin, `rotate(${(Math.sin(t * 1.3) * 2).toFixed(2)}deg)`, -10);
      const hk = ease.outCubic(prog(t, ttap - 0.55, ttap - 0.05));
      hand.style.opacity = (fadeIn(t, ttap - 0.55, 0.15) * (1 - prog(t, ttap + 0.4, ttap + 0.7))).toFixed(3);
      hand.style.transform = `translate(${lerp(220, 0, hk).toFixed(1)}px, ${lerp(200, 0, hk).toFixed(1)}px) scale(${t > ttap - 0.05 && t < ttap + 0.15 ? 0.85 : 1})`;
      const calling = t >= ttap;
      st.textContent = calling ? 'กำลังโทร' + '.'.repeat(1 + Math.floor(t * 3) % 3) : 'มือถือ';
      btn.style.transform = `scale(${(calling ? 1 : 1 + 0.08 * Math.sin(t * 7)).toFixed(3)})`;
      btn.style.background = calling ? '#e2382c' : '#2f9e5b';
      btn.style.transform += calling ? ' rotate(135deg)' : '';
      rings.forEach((r, i) => { const q = calling ? (((t - ttap) * 0.9 + i / 3) % 1) : 0; r.style.opacity = calling ? (1 - q).toFixed(2) : 0; r.style.transform = `translate(-50%,-50%) scale(${(1 + q * 1.4).toFixed(3)})`; });
    },
  };
}

// ---------------- gift box: lid pops, a heart floats out; money gets crossed out ----------------
function giftVsMoney(parent, x, y) {
  const wrap = html('div', 'giftw', parent); wrap.style.left = x + 'px'; wrap.style.top = y + 'px';
  const gb = iconBox(wrap, 170, 170, '-60 -80 120 120');
  const heart = svg('path', withStk({ d: heartPath(0, -10, 18), fill: '#e0577a' }, 4), gb.s);
  svg('rect', withStk({ x: -40, y: -6, width: 80, height: 44, rx: 6, fill: lin(gb.defs, [[0, '#ff8fa8'], [1, '#e0577a']]) }, 5), gb.s);
  svg('rect', { x: -7, y: -6, width: 14, height: 44, fill: '#ffd66b' }, gb.s);
  const lid = svg('g', {}, gb.s);
  svg('rect', withStk({ x: -46, y: -20, width: 92, height: 16, rx: 5, fill: '#ff6f8f' }, 5), lid);
  svg('rect', { x: -7, y: -20, width: 14, height: 16, fill: '#ffd66b' }, lid);
  svg('path', { d: 'M0,-20 C-18,-40 -30,-22 0,-20 C30,-22 18,-40 0,-20 Z', fill: '#ffd66b', stroke: '#fff', 'stroke-width': 3 }, lid);
  const mw = html('div', 'moneyx', wrap);
  const mb = iconBox(mw, 130, 100, '0 0 130 100');
  [0, 1].forEach(i => { svg('rect', withStk({ x: 10 + i * 8, y: 22 + i * 10, width: 100, height: 54, rx: 8, fill: i ? '#b9a9de' : '#8f7fb8' }, 4), mb.s); });
  svg('circle', withStk({ cx: 104, cy: 30, r: 18, fill: '#f2c14e' }, 4), mb.s);
  const x1 = svg('path', { d: 'M8,8 L122,92', stroke: '#e2382c', 'stroke-width': 10, 'stroke-linecap': 'round', pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, mb.s);
  const x2 = svg('path', { d: 'M122,8 L8,92', stroke: '#e2382c', 'stroke-width': 10, 'stroke-linecap': 'round', pathLength: 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, mb.s);
  return {
    el: wrap,
    update(t, tgift, tx) {
      popSquash(gb.d, t, tgift, '', -10);
      const open = ease.outBack(prog(t, tgift + 0.35, tgift + 0.7));
      lid.setAttribute('transform', `translate(${(open * 30).toFixed(1)},${(-open * 34).toFixed(1)}) rotate(${(open * 28).toFixed(1)})`);
      const hk = prog(t, tgift + 0.45, tgift + 1.6);
      heart.setAttribute('transform', `translate(0,${(-40 * ease.outCubic(hk) + 14 * (1 - Math.min(1, hk * 4))).toFixed(1)}) scale(${(0.4 + 0.8 * ease.outBack(Math.min(1, hk * 2))).toFixed(3)})`);
      heart.setAttribute('opacity', t > tgift + 0.45 ? 1 : 0);
      popSquash(mw, t, tx - 0.25, '', 8);
      x1.setAttribute('stroke-dashoffset', (1 - ease.outCubic(prog(t, tx, tx + 0.18))).toFixed(3));
      x2.setAttribute('stroke-dashoffset', (1 - ease.outCubic(prog(t, tx + 0.15, tx + 0.33))).toFixed(3));
      mw.style.filter = t > tx ? `grayscale(${(0.8 * prog(t, tx, tx + 0.3)).toFixed(2)})` : 'none';
    },
  };
}

// ---------------- speech bubble from the phone: typing… then "พ่อเหนื่อยไหม" ----------------
function speechBubble(parent, x, y, text) {
  const b = html('div', 'bubble2', parent); b.style.left = x + 'px'; b.style.top = y + 'px';
  const typ = typingDots(b);
  const tx = html('span', 'bubtext', b, text);
  const hb = heartBeat(b, 46);
  return {
    el: b,
    update(t, tin, ttext) {
      popSquash(b, t, tin, '', -6);
      const on = t >= ttext;
      typ.update(t, !on);
      tx.style.display = on ? 'inline' : 'none';
      hb.el.style.display = on ? 'inline-block' : 'none';
      if (on) { tx.style.opacity = fadeIn(t, ttext, 0.15); hb.update(t); }
    },
  };
}
