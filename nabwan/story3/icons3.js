// "1,095 ข้อความของแม่" UI: good-morning flower stickers (Thai day colours), chat phone, sunrise clock, streak chip,
// big counter, notification banner + swipe, mute toggle, anger mark, one-finger typing card, flip clock, bell = heart.

const DAYS = [['อาทิตย์', '#e8504b'], ['จันทร์', '#f2c230'], ['อังคาร', '#f06aa0'], ['พุธ', '#45b45f'], ['พฤหัสบดี', '#f5922a'], ['ศุกร์', '#3f9be0'], ['เสาร์', '#8e5fd0']];
const graphemes = s => Array.from(new Intl.Segmenter('th', { granularity: 'grapheme' }).segment(s), x => x.segment);

// "สวัสดีวัน…" sticker: glowing bouquet in the day's colour with sparkles and outlined lettering
function stickerSVG(dayIdx, w, extra = '') {
  const [name, c] = DAYS[dayIdx];
  const c2 = shade(c, 40), c3 = shade(c, -30), id = 'st' + Math.random().toString(36).slice(2, 7);
  const flower = (x, y, r, col) => {
    let s = '';
    for (let k = 0; k < 6; k++) { const a = k * 60, px = x + Math.cos(a * Math.PI / 180) * r * 0.62, py = y + Math.sin(a * Math.PI / 180) * r * 0.62; s += `<ellipse cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" rx="${(r * 0.5).toFixed(1)}" ry="${(r * 0.36).toFixed(1)}" transform="rotate(${a} ${px.toFixed(1)} ${py.toFixed(1)})" fill="${col}" stroke="#ffffff" stroke-width="2"/>`; }
    return s + `<circle cx="${x}" cy="${y}" r="${(r * 0.32).toFixed(1)}" fill="#ffe36b" stroke="#e0a12c" stroke-width="2"/>`;
  };
  const leaves = [[60, 118, -40], [140, 116, 40], [100, 128, 0]].map(([x, y, a]) => `<ellipse cx="${x}" cy="${y}" rx="26" ry="11" fill="#5cbf6a" transform="rotate(${a} ${x} ${y})"/>`).join('');
  const sp = [[30, 34], [172, 40], [24, 120], [178, 112], [100, 18]].map(([x, y], i) => `<path d="M${x},${y - 9} L${x + 3},${y - 3} L${x + 9},${y} L${x + 3},${y + 3} L${x},${y + 9} L${x - 3},${y + 3} L${x - 9},${y} L${x - 3},${y - 3} Z" fill="#fff" class="spk" style="--i:${i}"/>`).join('');
  return `<svg width="${w}" height="${w}" viewBox="0 0 200 200" ${extra}><defs><radialGradient id="${id}" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#fffdf4"/><stop offset=".6" stop-color="${c2}"/><stop offset="1" stop-color="${c}"/></radialGradient></defs>
  <rect x="4" y="4" width="192" height="192" rx="34" fill="url(#${id})" stroke="${c3}" stroke-width="5"/>${leaves}
  ${flower(64, 86, 34, c)}${flower(136, 82, 32, c3)}${flower(100, 58, 30, c2)}${flower(100, 104, 26, '#ffffff')}${sp}
  <text x="100" y="158" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="${c3}" stroke="#fff" stroke-width="7" paint-order="stroke">สวัสดี</text>
  <text x="100" y="188" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${name.length > 5 ? 22 : 27}" fill="${c3}" stroke="#fff" stroke-width="7" paint-order="stroke">วัน${name}</text></svg>`;
}

// phone with a chat thread; side 'R' = the phone owner, 'L' = the other person
function chatPhone(parent, x, y, w, h, title, avatarHTML) {
  const ph = html('div', 'cphone', parent);
  Object.assign(ph.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
  const scr = html('div', 'cscr', ph);
  const hd = html('div', 'chead', scr); hd.innerHTML = `<span class="cav">${avatarHTML}</span><b>${title}</b><i class="cdots">⋯</i>`;
  const body = html('div', 'cbody', scr);
  const list = html('div', 'clist', body);
  const items = [];
  const api = {
    el: ph, head: hd, body,
    add(kind, side, t0, opt = {}) {
      const row = html('div', 'crow ' + side, list);
      let el;
      if (kind === 'sticker') { el = html('div', 'csticker', row); el.innerHTML = stickerSVG(opt.day, opt.size || Math.round(w * 0.5)); }
      else if (kind === 'ghost') { el = html('div', 'cghost', row); el.style.width = el.style.height = Math.round(w * 0.5) + 'px'; el.innerHTML = `<svg width="84" height="84" viewBox="-50 -50 100 100">${[0, 1, 2, 3, 4, 5].map(k => `<ellipse cx="${(Math.cos(k * 1.047) * 24).toFixed(1)}" cy="${(Math.sin(k * 1.047) * 24).toFixed(1)}" rx="20" ry="14" transform="rotate(${k * 60} ${(Math.cos(k * 1.047) * 24).toFixed(1)} ${(Math.sin(k * 1.047) * 24).toFixed(1)})" fill="none" stroke="#8d99a2" stroke-width="4" stroke-dasharray="6 6"/>`).join('')}<circle r="10" fill="none" stroke="#8d99a2" stroke-width="4"/></svg><small>${opt.text || ''}</small>`; }
      else if (kind === 'typing') { el = html('div', 'cbub ' + side + ' ctyping', row); for (let k = 0; k < 3; k++) html('i', '', el); }
      else if (kind === 'custom') { el = html('div', 'csticker', row); el.innerHTML = opt.html; }
      else { el = html('div', 'cbub ' + side, row, opt.text); }
      const meta = html('div', 'cmeta', row, opt.meta || '');
      const it = { row, el, meta, t0, side, read: opt.read, until: opt.until, h: 0, typing: kind === 'typing' };
      items.push(it);
      return it;
    },
    update(t, scrollBias = 0) {
      let yy = 0, last = 0;
      for (const it of items) {
        if (!it.h) it.h = it.row.offsetHeight + 18;
        const on = t >= it.t0 && !(it.until != null && t >= it.until);
        it.row.style.display = on ? 'flex' : 'none';
        if (!on) continue;
        const k = spring(t, it.t0, 15, 6.5);
        it.row.style.transform = `translateY(${(yy + (1 - k) * 60).toFixed(1)}px) scale(${(0.6 + 0.4 * Math.min(1.08, k)).toFixed(3)})`;
        it.row.style.opacity = fadeIn(t, it.t0, 0.12);
        if (it.read != null) it.meta.style.opacity = t >= it.read ? 1 : 0;
        if (it.typing) Array.from(it.el.children).forEach((d, j) => { d.style.transform = `translateY(${(-6 * Math.max(0, Math.sin(t * 9 - j * 0.9))).toFixed(1)}px)`; });
        yy += it.h; last = yy;
      }
      const view = body.clientHeight - 20;
      const target = Math.max(0, Math.max(0, last - view) + scrollBias);
      api._s = api._s == null ? target : api._s + (target - api._s) * 0.35;
      list.style.transform = `translateY(${(-api._s).toFixed(1)}px)`;
    },
  };
  return api;
}

// sunrise clock card: "ทุกเช้า 05:59 → 06:00"
function sunriseClock(parent, x, y) {
  const c = cardEl(parent, 'clock', x, y);
  c.c.innerHTML += `<div class="icslot"></div><div><div class="tl">ทุกเช้า</div><div class="tt"><span class="hhmm">05:59</span></div><div class="sl" style="background:linear-gradient(90deg,#33427e,#f08c7a,#ffd08a)"><i style="left:4%"></i></div></div>`;
  const b = iconBox(c.c.querySelector('.icslot'), 84, 84, '-50 -50 100 100');
  svg('circle', { r: 48, fill: lin(b.defs, [[0, '#ffcf9a'], [1, '#f08c7a']]) }, b.s);
  const sun = svg('g', {}, b.s);
  for (let k = 0; k < 8; k++) svg('path', { d: 'M-3,-30 L3,-30 L1.5,-40 L-1.5,-40 Z', fill: '#fff6d0', transform: `rotate(${k * 45})` }, sun);
  svg('circle', { r: 20, fill: '#fff3c4', stroke: '#e0a12c', 'stroke-width': 3 }, sun);
  svg('rect', { x: -50, y: 14, width: 100, height: 40, fill: '#6c5a8a' }, b.s);
  svg('path', { d: 'M-50,14 Q-20,6 0,14 T50,12', fill: 'none', stroke: '#4f4270', 'stroke-width': 4 }, b.s);
  const hhmm = c.c.querySelector('.hhmm'), knob = c.c.querySelector('.sl i');
  hhmm.style.display = 'inline-block';
  return {
    c,
    update(t, tin, tflip) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      const rise = ease.outCubic(prog(t, tin, tflip + 0.6));
      sun.setAttribute('transform', `translate(0,${(26 - 34 * rise).toFixed(1)}) rotate(${(t * 20).toFixed(1)})`);
      const f = prog(t, tflip - 0.12, tflip + 0.12);
      hhmm.textContent = t < tflip ? '05:59' : '06:00';
      hhmm.style.transform = `rotateX(${(Math.sin(Math.PI * f) * 80).toFixed(1)}deg)`;
      knob.style.left = (4 + 92 * rise).toFixed(1) + '%';
    },
  };
}

// flame streak chip: "ส่งทุกวัน ไม่เคยขาด · 3 ปี"
function streakChip(parent, x, y) {
  const el = html('div', 'chip big streak', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const b = iconBox(el, 58, 58, '-30 -34 60 64');
  const outer = svg('path', { fill: '#ff8a2a', stroke: INK, 'stroke-width': 3 }, b.s);
  const inner = svg('path', { fill: '#ffd34a' }, b.s);
  const tx = html('span', '', el); tx.innerHTML = 'ส่งทุกเช้า ไม่เคยขาด <b class="yr">1</b> <b>ปี</b>';
  const yr = tx.querySelector('.yr');
  return {
    el,
    update(t, t0) {
      popSquash(el, t, t0);
      const w = Math.sin(t * 9) * 3, h = Math.sin(t * 13) * 2;
      outer.setAttribute('d', `M0,${-30 - h} C${12 + w},-14 22,-6 22,8 C22,22 12,28 0,28 C-12,28 -22,22 -22,8 C-22,-4 ${-10 + w},-10 -6,-20 C-2,-12 2,-10 0,${-30 - h} Z`);
      inner.setAttribute('d', `M0,${-8 - h} C8,0 12,6 12,13 C12,21 6,24 0,24 C-6,24 -12,21 -12,13 C-12,6 ${-4 + w * 0.5},2 0,${-8 - h} Z`);
      yr.textContent = String(1 + Math.min(2, Math.floor(Math.max(0, t - t0 - 0.2) / 0.35)));
    },
  };
}

// giant counter: 1,095 ข้อความ
function bigCounter(parent, y) {
  const wrap = html('div', 'bigcnt', parent); wrap.style.top = y + 'px';
  const n = html('div', 'bcn', wrap); const od = new Odometer(n, 4);
  const comma = document.createElement('span'); comma.textContent = ','; comma.className = 'ocomma'; od.el.insertBefore(comma, od.cols[1].col);
  html('div', 'bcl', wrap, 'ข้อความ');
  return {
    el: wrap,
    update(t, t0, t1) {
      wrap.style.opacity = fadeIn(t, t0 - 0.1, 0.15);
      const v = rollValue(t, t0, t1, 0, 1095); od.set(v.v, v.speed);
      const land = 1 + 0.18 * Math.exp(-Math.pow((t - t1 - 0.05) * 6, 2));
      wrap.style.transform = `translateX(-50%) scale(${land.toFixed(3)})`;
      comma.style.display = od.cols[0].col.style.display === 'none' ? 'none' : 'inline-block';
    },
  };
}

// notification banner on the daughter's phone
function notifBanner(parent, y, avatarHTML, who, msg) {
  const el = html('div', 'notif', parent); el.style.top = y + 'px';
  el.innerHTML = `<div class="app">แชท</div><div class="av">${avatarHTML}</div><div style="flex:1"><div class="who">${who}<small>ตอนนี้</small></div><div class="msg">${msg}</div></div>`;
  const hand = html('div', 'swipeHand', parent); hand.innerHTML = '<svg width="96" height="110" viewBox="0 0 74 90"><path d="M24,40 L24,10 Q24,2 31,2 Q38,2 38,10 L38,34 L40,30 Q46,26 50,32 L52,36 Q58,32 62,38 L63,42 Q69,40 71,46 L71,64 Q71,86 50,88 L36,88 Q22,86 14,72 L4,52 Q2,44 9,42 Q14,41 18,48 L24,58 Z" fill="#ffd9b8" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>';
  hand.style.top = (y + 40) + 'px';
  return {
    el,
    update(t, tin, tswipe) {
      const k = spring(t, tin, 13, 6);
      const sw = ease.inCubic(prog(t, tswipe, tswipe + 0.35));
      el.style.opacity = (fadeIn(t, tin, 0.12) * (1 - prog(t, tswipe + 0.2, tswipe + 0.4))).toFixed(3);
      el.style.transform = `translateY(${((1 - k) * -220).toFixed(1)}px) translateX(${(-sw * 1100).toFixed(1)}px) rotate(${(-sw * 8).toFixed(2)}deg)`;
      const hk = prog(t, tswipe - 0.45, tswipe + 0.35);
      hand.style.opacity = hk > 0 && hk < 1 ? Math.min(1, Math.sin(Math.PI * hk) * 2).toFixed(3) : 0;
      hand.style.transform = `translateX(${(700 - ease.inOutSine(hk) * 640).toFixed(1)}px) rotate(${(-10 + hk * 20).toFixed(1)}deg)`;
    },
  };
}

// mute toggle card: bell rings, switch flips off (and optionally back on with a heart)
function muteToggle(parent, x, y) {
  const c = cardEl(parent, 'card mute', x, y, 470);
  const row = html('div', 'muterow', c.c);
  const b = iconBox(row, 96, 96, '-50 -50 100 100');
  const bell = svg('g', {}, b.s);
  svg('path', { d: 'M-26,18 C-26,-6 -22,-30 0,-32 C22,-30 26,-6 26,18 L34,26 L-34,26 Z', fill: '#f6c343', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, bell);
  svg('circle', { cx: 0, cy: 34, r: 8, fill: '#f6c343', stroke: INK, 'stroke-width': 4 }, bell);
  svg('circle', { cx: 0, cy: -36, r: 5, fill: INK }, bell);
  const slash = svg('path', { d: 'M-38,-38 L38,38', stroke: '#e0574b', 'stroke-width': 9, 'stroke-linecap': 'round' }, b.s);
  const heart = svg('path', { d: heartPath(28, -28, 14), fill: '#e0577a', stroke: '#fff', 'stroke-width': 3 }, b.s);
  const tx = html('div', 'mutetx', row); tx.innerHTML = '<small>การแจ้งเตือนจาก</small><b>แม่</b>';
  const sw = html('div', 'sw', row); const knob = html('i', '', sw);
  return {
    c,
    update(t, tin, toff, ton = 99) {
      enter3d(c.c, t, tin, 'swingLeft'); shine(c.sh, t, tin + 0.4);
      const ring = t < toff ? Math.sin(t * 40) * 14 * Math.exp(-Math.max(0, t - tin) * 1.5) : 0;
      bell.setAttribute('transform', `rotate(${ring.toFixed(1)})`);
      const off = ease.outBack(prog(t, toff, toff + 0.3)) * (1 - ease.outBack(prog(t, ton, ton + 0.3)));
      knob.style.transform = `translateX(${(44 * (1 - off)).toFixed(1)}px)`;
      sw.style.background = off > 0.5 ? '#c9c4bd' : '#2f9e5b';
      const sk = prog(t, toff + 0.05, toff + 0.3) * (1 - prog(t, ton, ton + 0.2));
      slash.setAttribute('stroke-dasharray', '110'); slash.setAttribute('stroke-dashoffset', (110 * (1 - sk)).toFixed(1));
      heart.setAttribute('opacity', t > ton ? 1 : 0);
      heart.setAttribute('transform', `translate(28,-28) scale(${(t > ton ? 0.6 + 0.4 * spring(t, ton, 14, 5) + 0.08 * Math.sin(t * 8) : 0).toFixed(3)}) translate(-28,28)`);
    },
  };
}

// 💢 annoyance mark + sigh puff, drawn in an fx svg, placed beside a head
function angerMark(parent) {
  const g = svg('g', { opacity: 0 }, parent);
  for (let k = 0; k < 4; k++) svg('path', { d: 'M4,-16 Q4,-4 16,-4', fill: 'none', stroke: '#e0453b', 'stroke-width': 7, 'stroke-linecap': 'round', transform: `rotate(${k * 90})` }, g);
  const puff = svg('g', { opacity: 0 }, parent);
  for (const [x, y, r] of [[0, 0, 16], [18, -6, 12], [32, -2, 9]]) svg('circle', { cx: x, cy: y, r, fill: '#ffffff', stroke: INK, 'stroke-width': 3 }, puff);
  return (t, t0, x, y) => {
    const k = spring(t, t0, 14, 5);
    g.setAttribute('opacity', t > t0 ? 1 : 0);
    g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) scale(${(k * (1 + 0.12 * Math.sin(t * 12))).toFixed(3)})`);
    const pk = prog(t, t0 + 0.3, t0 + 1.3);
    puff.setAttribute('opacity', pk > 0 && pk < 1 ? (1 - pk).toFixed(3) : 0);
    puff.setAttribute('transform', `translate(${(x + 40 + pk * 40).toFixed(1)},${(y + 80 - pk * 30).toFixed(1)}) scale(${(0.6 + pk * 0.6).toFixed(3)})`);
  };
}

// one-finger typing: phone close-up, keyboard, a big finger pokes one key per character, then "ส่ง"
function typingCard(parent, x, y, text) {
  const el = html('div', 'tcard', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const field = html('div', 'tfield', el); const tx = html('span', '', field); const caret = html('i', 'tcaret', field);
  const size = html('div', 'tsize', el, 'ขนาดตัวอักษร: ใหญ่มาก');
  const kb = html('div', 'tkb', el);
  const keys = [];
  for (let r = 0; r < 3; r++) for (let c = 0; c < 8; c++) { const k = html('i', '', kb); keys.push(k); }
  const send = html('div', 'tsend', el, 'ส่ง');
  const finger = html('div', 'tfinger', el); finger.innerHTML = '<svg width="120" height="150" viewBox="0 0 74 90"><path d="M24,40 L24,10 Q24,2 31,2 Q38,2 38,10 L38,34 L40,30 Q46,26 50,32 L52,36 Q58,32 62,38 L63,42 Q69,40 71,46 L71,64 Q71,86 50,88 L36,88 Q22,86 14,72 L4,52 Q2,44 9,42 Q14,41 18,48 L24,58 Z" fill="#c98d62" stroke="#33252a" stroke-width="3.5" stroke-linejoin="round"/><path d="M27,12 Q31,8 35,12" stroke="#fff" stroke-width="2" fill="none" opacity=".6"/></svg>';
  const gs = graphemes(text);
  const seq = gs.map((_, i) => (i * 7 + 3) % keys.length);
  return {
    el,
    update(t, tin, t0, t1, tsend) {
      enter3d(el, t, tin, 'pop');
      const n = Math.max(0, Math.min(gs.length, Math.floor(prog(t, t0, t1) * gs.length + (t >= t0 ? 1 : 0))));
      tx.textContent = gs.slice(0, n).join('');
      caret.style.opacity = Math.sin(t * 10) > 0 ? 1 : 0;
      // finger: hop to the key for the next character, press, lift
      const per = (t1 - t0) / gs.length, i = clamp(Math.floor((t - t0) / per), 0, gs.length - 1), ph = ((t - t0) / per) % 1;
      const key = t < tsend - 0.3 ? keys[seq[i]] : send;
      const kr = key.getBoundingClientRect(), er = el.getBoundingClientRect(), sc = er.width / el.offsetWidth || 1;
      const kx = (kr.x - er.x) / sc + kr.width / sc / 2 - 38, ky = (kr.y - er.y) / sc + kr.height / sc / 2 - 6;
      const press = t < tsend - 0.3 ? (ph > 0.45 && ph < 0.75 ? 1 : 0) : (t > tsend && t < tsend + 0.2 ? 1 : 0);
      finger.style.transform = `translate(${kx.toFixed(1)}px,${(ky - 30 * (1 - press) - (t < t0 ? 60 : 0)).toFixed(1)}px) scale(${press ? 0.94 : 1})`;
      finger.style.opacity = fadeIn(t, tin + 0.2, 0.2) * (1 - prog(t, tsend + 0.4, tsend + 0.7));
      keys.forEach((k, j) => k.classList.toggle('on', press === 1 && key === k && j >= 0));
      send.classList.toggle('on', t > tsend && t < tsend + 0.25);
      const fly = ease.inCubic(prog(t, tsend + 0.2, tsend + 0.6));
      field.style.transform = `translateY(${(-fly * 260).toFixed(1)}px) scale(${(1 - fly * 0.3).toFixed(3)})`;
      field.style.opacity = (1 - fly).toFixed(3);
      size.style.opacity = fadeIn(t, tin + 0.4, 0.2);
    },
  };
}

// big flip clock: 06:00 → 07:00 → 08:00 (8 goes red)
function flipClock(parent, x, y) {
  const c = cardEl(parent, 'clock flipc', x, y);
  c.c.innerHTML += `<div class="icslot"></div><div><div class="tl">ยังไม่มีข้อความจากแม่</div><div class="tt"><span class="hhmm">06:00</span></div></div>`;
  const b = iconBox(c.c.querySelector('.icslot'), 84, 84, '-50 -50 100 100');
  svg('circle', { r: 44, fill: '#fffaf0', stroke: INK, 'stroke-width': 5 }, b.s);
  const hands = svg('path', { stroke: INK, 'stroke-width': 5, 'stroke-linecap': 'round', fill: 'none' }, b.s);
  svg('circle', { r: 5, fill: '#e0574b' }, b.s);
  const hhmm = c.c.querySelector('.hhmm'); hhmm.style.display = 'inline-block';
  return {
    c,
    update(t, tin, ts) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      let h = 6; ts.forEach((tt, i) => { if (t >= tt) h = 6 + i; });
      const flips = ts.map(tt => prog(t, tt - 0.12, tt + 0.12)).find(f => f > 0 && f < 1) || 0;
      hhmm.textContent = `0${h}:00`;
      hhmm.style.transform = `rotateX(${(Math.sin(Math.PI * flips) * 80).toFixed(1)}deg)`;
      hhmm.style.color = h >= 8 ? '#e0453b' : '#23242f';
      const ha = (h % 12) * 30 - 90 + flips * 30;
      hands.setAttribute('d', `M0,0 L${(Math.cos(rad(ha)) * 22).toFixed(1)},${(Math.sin(rad(ha)) * 22).toFixed(1)} M0,0 L0,-32`);
      if (h >= 8) c.c.style.boxShadow = `0 0 ${(20 + 14 * Math.sin(t * 8)).toFixed(1)}px rgba(224,69,59,.55), 0 20px 40px rgba(0,0,0,.42)`;
    },
  };
}

// 🔔 แจ้งเตือนน่ารำคาญ = ❤️ มีคนคิดถึง
function bellEqHeart(parent, x, y, w) {
  const c = cardEl(parent, 'card eqb', x, y, w);
  const row = html('div', 'eqrow', c.c);
  const a = html('div', 'eqcell', row); const ab = iconBox(a, 110, 110, '-50 -50 100 100');
  svg('path', { d: 'M-26,18 C-26,-6 -22,-30 0,-32 C22,-30 26,-6 26,18 L34,26 L-34,26 Z', fill: '#f6c343', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, ab.s);
  svg('circle', { cx: 0, cy: 34, r: 8, fill: '#f6c343', stroke: INK, 'stroke-width': 4 }, ab.s);
  const badge = svg('g', {}, ab.s); svg('circle', { cx: 28, cy: -30, r: 17, fill: '#e0453b', stroke: '#fff', 'stroke-width': 3 }, badge);
  svg('text', { x: 28, y: -24, 'text-anchor': 'middle', 'font-family': 'Kanit', 'font-weight': 700, 'font-size': 18, fill: '#fff' }, badge).textContent = '99+';
  html('small', '', a, 'แจ้งเตือนน่ารำคาญ');
  const eq = html('div', 'eqsign', row, '=');
  const b = html('div', 'eqcell', row); const bb = iconBox(b, 110, 110, '-50 -50 100 100');
  const hp = svg('path', { d: heartPath(0, 0, 34), fill: '#e0577a', stroke: INK, 'stroke-width': 4.5 }, bb.s);
  html('small', '', b, 'มีคนคิดถึง');
  return {
    c,
    update(t, t0, t1) {
      enter3d(c.c, t, t0, 'flipDown'); shine(c.sh, t, t1 + 0.2);
      a.style.opacity = fadeIn(t, t0 + 0.1, 0.15);
      eq.style.opacity = fadeIn(t, t1 - 0.2, 0.12);
      eq.style.transform = `scale(${(0.5 + 0.5 * spring(t, t1 - 0.2, 14, 6)).toFixed(3)})`;
      b.style.opacity = fadeIn(t, t1, 0.15);
      hp.setAttribute('transform', `scale(${(spring(t, t1, 13, 5) * (1 + 0.1 * Math.max(0, Math.sin(t * 7)))).toFixed(3)})`);
      badge.setAttribute('transform', `rotate(${(Math.sin(t * 30) * 6 * (t < t1 ? 1 : 0)).toFixed(1)} 28 -30)`);
    },
  };
}
