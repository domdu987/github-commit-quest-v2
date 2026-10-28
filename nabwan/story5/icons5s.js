// "127 ใบสมัคร" widgets: rejection inbox, application counter, grad-months chip, rejection / offer mails, cost chips,
// bank balance, bus-ticket booking with a hovering finger, transfer slip, video call, tears.

const COMPANIES = [['สยามมาร์เก็ตติ้ง', '#e0574b'], ['รุ่งเรืองค้าปลีก', '#4a7bd8'], ['ไทยดีไซน์สตูดิโอ', '#2f9e5b'], ['บางกอกดิจิทัล', '#9a5fc8'],
  ['แสงทองการบัญชี', '#e8a33c'], ['ซันไชน์เอเจนซี่', '#e0577a'], ['ภูผาคอนสตรัคชั่น', '#5a6f8f'], ['นครโลจิสติกส์', '#1f9aa8']];
const FINGER = '<svg width="110" height="130" viewBox="0 0 74 90"><path d="M24,40 L24,10 Q24,2 31,2 Q38,2 38,10 L38,34 L40,30 Q46,26 50,32 L52,36 Q58,32 62,38 L63,42 Q69,40 71,46 L71,64 Q71,86 50,88 L36,88 Q22,86 14,72 L4,52 Q2,44 9,42 Q14,41 18,48 L24,58 Z" fill="#e8b48e" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>';

// mail app with "เสียใจด้วย" rows arriving on top, newest first
function inboxCard(parent, x, y, w, h) {
  const el = html('div', 'mail', parent);
  Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
  const hd = html('div', 'mhead', el); hd.innerHTML = '<span>กล่องจดหมาย</span>';
  const badge = html('b', 'mbadge', hd);
  const list = html('div', 'mlist', el);
  const rows = [];
  const row = i => {
    const [name, col] = COMPANIES[i % COMPANIES.length];
    const r = html('div', 'mrow', list);
    r.innerHTML = `<div class="mav" style="background:${col}">${name[0]}</div><div class="mtx"><b>${name}</b><small>ขอบคุณที่สนใจ แต่เสียใจด้วย...</small></div><div class="mtag">ไม่ผ่าน</div>`;
    return r;
  };
  return {
    el,
    update(t, tin, times, count) {
      enter3d(el, t, tin, 'pop');
      const n = times.filter(tt => t >= tt).length;
      while (rows.length < n) rows.push(row(rows.length));
      rows.forEach((r, i) => {
        const age = n - 1 - i;                       // 0 = newest, drawn on top
        const k = spring(t, times[i], 16, 7);
        const yy = age * 104 - (age === 0 ? (1 - k) * 104 : 0);
        r.style.transform = `translateY(${yy.toFixed(1)}px)`;
        r.style.opacity = age === 0 ? fadeIn(t, times[i], 0.08) : 1;
        r.style.display = age < 7 ? 'flex' : 'none';
        r.style.background = age === 0 ? `rgba(255,236,236,${(1 - prog(t, times[i], times[i] + 0.5)).toFixed(2)})` : '#fff';
      });
      badge.textContent = Math.round(count);
      badge.style.display = count > 0 ? 'inline-block' : 'none';
    },
  };
}

// "ส่งใบสมัคร 127 ที่" chip with a paper-plane document icon that hops on each send
function appCounter(parent, x, y) {
  const el = html('div', 'chip big appchip', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const b = iconBox(el, 62, 62, '-32 -32 64 64');
  const doc = svg('g', {}, b.s);
  svg('path', { d: 'M-18,-26 L8,-26 L20,-14 L20,26 L-18,26 Z', fill: '#ffffff', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, doc);
  svg('path', { d: 'M8,-26 L8,-14 L20,-14', fill: '#d9e2ec', stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, doc);
  for (const ly of [-6, 4, 14]) svg('path', { d: `M-10,${ly} L12,${ly}`, stroke: '#9aa6b2', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, doc);
  svg('circle', { cx: -4, cy: -14, r: 6, fill: '#f2c14e', stroke: INK, 'stroke-width': 2.5 }, doc);
  const tx = html('span', '', el); tx.innerHTML = 'ส่งใบสมัคร ';
  const n = html('b', '', tx); const od = new Odometer(n, 3); html('span', '', tx, ' ที่');
  return {
    el,
    update(t, t0, v, speed = 0, pops = []) {
      popSquash(el, t, t0);
      od.set(v, speed);
      const p = pops.map(tp => Math.exp(-Math.pow((t - tp) * 9, 2))).reduce((a, c) => Math.max(a, c), 0);
      doc.setAttribute('transform', `translate(0,${(-10 * p).toFixed(1)}) rotate(${(12 * p).toFixed(1)})`);
      el.style.transform = (el.style.transform || '') + ` scale(${(1 + 0.06 * p).toFixed(3)})`;
    },
  };
}

// "จบมา 8 เดือน" chip with a flipping calendar
function monthsChip(parent, x, y) {
  const el = html('div', 'chip big', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const cal = calendarFlip(el, 62);
  const tx = html('span', '', el); tx.innerHTML = 'จบมา ';
  const n = html('b', '', tx, '1'); html('span', '', tx, ' เดือน');
  return {
    el,
    update(t, t0, t1) {
      popSquash(el, t, t0);
      const v = Math.max(1, Math.round(lerp(1, 8, ease.outCubic(prog(t, t0 + 0.1, t1)))));
      n.textContent = v; cal.update(t, v, t > t0 + 0.1 && t < t1);
    },
  };
}

// an opened e-mail; ok=false: rejection (yellow + red highlights, red stamp); ok=true: offer (green)
function mailCard(parent, x, y, w, ok, company, subject, lines) {
  const [name, col] = company;
  const el = html('div', 'rmail' + (ok ? ' ok' : ''), parent);
  Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  el.innerHTML = `<div class="rh"><div class="mav" style="background:${col}">${name[0]}</div><div><b>${name}</b><small>ถึง: ฉัน · เมื่อสักครู่</small></div></div><div class="rs">${subject}</div>`;
  const hls = lines.map(([text, hl]) => {
    const p = html('p', '', el);
    if (!hl) { p.textContent = text; return null; }
    const s = html('span', 'hl', p); const bar = html('i', '', s); bar.style.background = hl; html('span', 'hlt', s, text);
    return bar;
  });
  const st = html('div', 'stamp big', el); st.innerHTML = ok ? '✓ ผ่าน' : 'ไม่ผ่าน';
  if (ok) { st.style.color = '#2f9e5b'; st.style.borderColor = '#2f9e5b'; }
  return {
    el,
    update(t, tin, hlTimes, tStamp) {
      enter3d(el, t, tin, 'flipDown');
      hls.forEach((bar, i) => { if (bar) bar.style.transform = `scaleX(${ease.outCubic(prog(t, hlTimes[i], hlTimes[i] + 0.35)).toFixed(3)})`; });
      const k = spring(t, tStamp, 15, 6);
      st.style.opacity = t >= tStamp ? 1 : 0;
      st.style.transform = `rotate(${ok ? -8 : -12}deg) scale(${(2.4 - 1.4 * Math.min(1.05, k)).toFixed(3)})`;
    },
  };
}

// cost chips: house / rice bowl icon + amount
function costChip(parent, x, y, kind, label, amount, unit) {
  const el = html('div', 'chip big costchip', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  let ic;
  if (kind === 'house') ic = houseIcon(el, 64);
  else {
    const b = iconBox(el, 64, 64, '-50 -50 100 100');
    const steam = [0, 1, 2].map(k => svg('path', { d: `M${-18 + k * 18},-26 q-8,-10 0,-20 q8,-10 0,-20`, fill: 'none', stroke: '#c9d2dc', 'stroke-width': 5, 'stroke-linecap': 'round' }, b.s));
    svg('ellipse', withStk({ cx: 0, cy: -8, rx: 40, ry: 14, fill: '#ffffff' }, 5), b.s);
    svg('path', withStk({ d: 'M-42,-8 Q-40,36 0,38 Q40,36 42,-8 Z', fill: '#4a7bd8' }, 6), b.s);
    svg('path', { d: 'M-30,12 Q0,22 30,12', fill: 'none', stroke: '#ffffff', 'stroke-width': 4, opacity: 0.6 }, b.s);
    svg('path', { d: 'M10,-14 L34,-36 M18,-12 L40,-30', stroke: '#c9a24a', 'stroke-width': 4, 'stroke-linecap': 'round' }, b.s);
    ic = { update: t => steam.forEach((s, k) => s.setAttribute('opacity', (0.3 + 0.6 * Math.max(0, Math.sin(t * 3 + k * 1.4))).toFixed(2))) };
  }
  const tx = html('span', '', el); tx.innerHTML = `${label} <b>฿${amount}</b><small>${unit}</small>`;
  return {
    el,
    update(t, t0) { popSquash(el, t, t0); if (ic.update) ic.update(t); },
  };
}

// bank app card: balance rolls down and turns red
function bankCard(parent, x, y, w) {
  const el = html('div', 'bank', parent);
  Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  el.innerHTML = '<div class="bl">ยอดเงินคงเหลือ</div><div class="bacct">บัญชีออมทรัพย์ ···· 4521</div>';
  const bn = html('div', 'bn', el); html('small', '', bn, '฿');
  const numW = html('span', '', bn); const od = new Odometer(numW, 4);
  const warn = html('div', 'bwarn', el); warn.innerHTML = '⚠ เงินใกล้หมด';
  const sh = html('div', 'shine', el);
  return {
    el,
    update(t, tin, t0, t1) {
      enter3d(el, t, tin, 'flipDown'); shine(sh, t, tin + 0.4);
      const r = rollValue(t, t0, t1, 1250, 210);
      od.set(r.v, r.speed);
      const low = t > t1 - 0.2;
      bn.style.color = low ? '#ffd0cc' : '#ffffff';
      warn.style.opacity = fadeIn(t, t1 - 0.1, 0.15);
      warn.style.transform = `scale(${(0.6 + 0.4 * spring(t, t1 - 0.1, 14, 6)).toFixed(3)}) rotate(${low ? (Math.sin(t * 20) * 2).toFixed(2) : 0}deg)`;
    },
  };
}

// bus ticket booking with a finger hovering over "ยืนยัน", trembling, never pressing
function bookCard(parent, x, y, w) {
  const el = html('div', 'book', parent);
  Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  el.innerHTML = '<div class="bt">จองตั๋วรถทัวร์</div>';
  const rt = html('div', 'route', el);
  html('span', '', rt, 'กรุงเทพฯ');
  const bus = busCute(rt, 92);
  html('span', '', rt, 'ขอนแก่น');
  el.insertAdjacentHTML('beforeend', '<div class="info"><span>คืนนี้ 21:30</span><span>ที่นั่ง 1 ที่</span></div><div class="price">฿489</div>');
  const btn = html('div', 'bbtn', el, 'ยืนยันการจอง');
  const fin = html('div', 'tfinger', el); fin.innerHTML = FINGER;
  return {
    el,
    update(t, tin, tHover, tOut) {
      enter3d(el, t, tin, 'swingRight');
      if (bus.update) bus.update(t);
      const k = ease.outCubic(prog(t, tHover - 0.5, tHover));
      const tremble = t > tHover ? Math.sin(t * 38) * 3 + Math.sin(t * 23) * 2 : 0;
      fin.style.opacity = prog(t, tHover - 0.5, tHover - 0.3);
      fin.style.transform = `translate(${(w * 0.5 - 30 + tremble).toFixed(1)}px, ${(lerp(560, 330, k) + tremble * 0.6).toFixed(1)}px) rotate(-8deg)`;
      btn.style.boxShadow = t > tHover ? `0 0 ${(18 + 12 * Math.sin(t * 6)).toFixed(1)}px rgba(255,90,80,.7)` : '0 10px 22px rgba(255,90,80,.4)';
      const out = ease.inCubic(prog(t, tOut, tOut + 0.4));
      if (out > 0) { el.style.opacity = (1 - out).toFixed(3); el.style.filter = `blur(${(out * 8).toFixed(1)}px)`; }
      else el.style.filter = 'none';
    },
  };
}

// transfer slip that sits in the chat as mom's message
function slipHTML(amount) {
  return `<div class="slip"><div class="sl1"><svg width="46" height="46" viewBox="-25 -25 50 50"><circle r="22" fill="#2f9e5b"/><path d="M-10,0 L-3,8 L11,-8" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg><span>ส่งเงินสำเร็จ</span></div><div class="sl2">฿${amount}</div><div class="sl3">จาก แม่ ถึง ลูก</div></div>`;
}

// video call: mom's face fills the screen, his small self-view in the corner
function videoCall(parent, x, y, w, h) {
  const el = html('div', 'vcall', parent);
  Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
  const scr = html('div', 'vscr', el);
  const big = svg('svg', { width: w - 24, height: h - 24, viewBox: `0 0 ${w - 24} ${h - 24}` }, scr);
  const bd = svg('defs', {}, big);
  svg('rect', { width: w - 24, height: h - 24, fill: lin(bd, [[0, '#a4744e'], [1, '#6a4428']]) }, big);
  for (let i = 0; i < 6; i++) svg('rect', { x: i * 80, y: 0, width: 3, height: h, fill: '#5a3a22', opacity: 0.5 }, big);
  const cx = (w - 24) / 2, cy = (h - 24) * 0.46;
  svg('rect', { x: cx - 46, y: cy + 110, width: 92, height: 120, fill: MOM5.skinShade, stroke: INK, 'stroke-width': 6 }, big);
  svg('path', { d: `M${cx - 300},${h} C${cx - 290},${cy + 75} ${cx + 290},${cy + 75} ${cx + 300},${h} Z`, fill: MOM5.shirt, stroke: INK, 'stroke-width': 6 }, big);
  svg('path', { d: `M${cx - 50},${cy + 206} Q${cx},${cy + 262} ${cx + 50},${cy + 206}`, fill: MOM5.skinShade, stroke: INK, 'stroke-width': 6 }, big);
  const faceG = svg('g', {}, big);
  const faces = [faceFront5(faceG, cx, cy, 160, 'mom', { smile: 0.9 }), faceFront5(faceG, cx, cy, 160, 'mom', { smile: 1, closed: true })];
  const hd = html('div', 'vhead', el); hd.innerHTML = '<b>แม่</b><small>00:00</small>';
  const timer = hd.querySelector('small');
  const self = html('div', 'vself', el); self.innerHTML = portrait5('grad', 150, '#dbe7f3', { smile: 1 });
  const bar = html('div', 'vbar', el);
  bar.innerHTML = '<i class="vb"></i><i class="vb end"></i><i class="vb"></i>';
  return {
    el,
    update(t, tin) {
      enter3d(el, t, tin, 'pop');
      const s = Math.max(0, Math.floor(t - tin));
      timer.textContent = `00:${String(s).padStart(2, '0')}`;
      const laugh = Math.sin(t * 1.7) > 0.6;
      faces[0].setAttribute('opacity', laugh ? 0 : 1); faces[1].setAttribute('opacity', laugh ? 1 : 0);
      faceG.setAttribute('transform', `translate(0,${(Math.sin(t * 2.4) * 6).toFixed(1)}) rotate(${(Math.sin(t * 1.3) * 3).toFixed(2)} ${cx} ${cy})`);
    },
  };
}

// tears: drops falling from an eye point
function tears(parent, n = 4) {
  const drops = Array.from({ length: n }, () => svg('path', { d: 'M0,-9 C4,-3 7,2 7,5 A7,7 0 1 1 -7,5 C-7,2 -4,-3 0,-9 Z', fill: '#bfe9ff', stroke: '#ffffff', 'stroke-width': 2, opacity: 0 }, parent));
  return (t, t0, x, y, every = 0.55) => drops.forEach((d, i) => {
    const tt = t - t0 - i * every; const q = tt > 0 ? (tt % (every * n)) / 0.8 : -1;
    const on = q >= 0 && q < 1;
    setA(d, { opacity: on ? (1 - q * 0.8).toFixed(2) : 0, transform: `translate(${(x + (i % 2 ? 6 : -4)).toFixed(1)},${(y + q * q * 70).toFixed(1)}) scale(${(1.4 - q * 0.4).toFixed(2)})` });
  });
}

// a thin manila application folder he carries
function folderProp(parent) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M-34,-46 L-8,-46 L-2,-38 L34,-38 L34,40 L-34,40 Z', fill: '#e2b664', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  svg('rect', { x: -26, y: -30, width: 50, height: 62, fill: '#ffffff', stroke: INK, 'stroke-width': 2.5 }, g);
  svg('path', { d: 'M-34,-30 L34,-30 L34,40 L-34,40 Z', fill: '#efc77a', stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round', transform: 'skewY(4)' }, g);
  return g;
}
