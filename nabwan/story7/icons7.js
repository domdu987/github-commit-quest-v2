// "11 ปีที่เพื่อนไม่เคยลืม" UI: chat-list row, birthday cake card, midnight birthday notifications (a stacked deck of
// years), chat thread with scroll + typing, birthday score card, แบงค์'s profile card, หมูกระทะ sticker, "คนแรก" badge.

const ins = (el, h) => { el.insertAdjacentHTML('beforeend', h); return el.lastElementChild; };
function card7(parent, cls, x, y, w) {
  const c = html('div', cls, parent);
  c.style.left = x + 'px'; c.style.top = y + 'px'; if (w) c.style.width = w + 'px';
  const sh = html('div', 'shine', c);
  return { c, sh };
}

// birthday cake with one candle; returns the svg string (flame has class fl7 for flicker)
function cakeSVG(w) {
  return `<svg width="${w}" height="${w}" viewBox="-60 -70 120 130" style="overflow:visible">
  <ellipse cx="0" cy="52" rx="54" ry="8" fill="#000" opacity=".18"/>
  <path d="M-46,10 L46,10 L46,46 Q0,56 -46,46 Z" fill="#f6c6d4" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M-46,10 Q-38,24 -30,12 Q-22,26 -14,12 Q-6,26 2,12 Q10,26 18,12 Q26,26 34,12 Q40,22 46,10 Z" fill="#fff8f0" stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"/>
  <path d="M-36,-14 L36,-14 L36,12 L-36,12 Z" fill="#a9763f" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M-36,-14 Q-28,-2 -20,-12 Q-12,0 -4,-12 Q4,0 12,-12 Q20,0 28,-12 Q32,-6 36,-14 Z" fill="#fff8f0" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>
  ${[[-24, 30, '#e0577a'], [0, 32, '#4a7bd8'], [24, 30, '#f2c14e'], [-12, -2, '#e0577a'], [14, -2, '#5fa27f']].map(([x, y, c]) => `<circle cx="${x}" cy="${y}" r="4.5" fill="${c}"/>`).join('')}
  <rect x="-4" y="-40" width="8" height="28" rx="3" fill="#7fc0f0" stroke="${INK}" stroke-width="3"/>
  <g class="fl7"><ellipse cx="0" cy="-52" rx="16" ry="20" fill="#ffd66b" opacity=".35"/><path d="M0,-64 C7,-54 8,-48 0,-42 C-8,-48 -7,-54 0,-64 Z" fill="#ffb03a" stroke="${INK}" stroke-width="2.5"/><path d="M0,-56 C3,-51 3,-48 0,-45 C-3,-48 -3,-51 0,-56 Z" fill="#fff3c4"/></g></svg>`;
}
const flicker = (root, t) => root.querySelectorAll('.fl7').forEach((f, i) => f.setAttribute('transform', `translate(0,-42) scale(${(1 + 0.08 * Math.sin(t * 23 + i)).toFixed(3)},${(1 + 0.12 * Math.sin(t * 17 + i * 2)).toFixed(3)}) skewX(${(Math.sin(t * 11 + i) * 6).toFixed(1)}) translate(0,42)`));

// mookrata pan sticker: domed grill, pork slices, steam, "ไปป่ะ"
function mookrataSticker(w) {
  return `<svg width="${w}" height="${w}" viewBox="0 0 200 200"><rect x="4" y="4" width="192" height="192" rx="34" fill="#ffe9d6" stroke="#f08a5a" stroke-width="5"/>
  <path d="M70,40 q-10,-14 0,-26 M100,36 q-10,-14 0,-26 M130,40 q-10,-14 0,-26" fill="none" stroke="#c9b8a8" stroke-width="5" stroke-linecap="round"/>
  <path d="M56,150 L144,150 L134,126 L66,126 Z" fill="#c96a3a" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
  <ellipse cx="100" cy="124" rx="70" ry="14" fill="#6b7280" stroke="${INK}" stroke-width="5"/>
  <path d="M42,120 Q100,40 158,120 Z" fill="#aab3c2" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
  ${[[78, 92, -20], [104, 76, 10], [124, 98, 30], [96, 104, -5]].map(([x, y, a]) => `<ellipse cx="${x}" cy="${y}" rx="15" ry="8" fill="#ef9a9a" stroke="${INK}" stroke-width="3" transform="rotate(${a} ${x} ${y})"/>`).join('')}
  <text x="100" y="186" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="32" fill="#d9542a" stroke="#fff" stroke-width="7" paint-order="stroke">ไปป่ะ</text></svg>`;
}

// chat-list row: แบงค์'s chat gathering dust, last message 8 months ago
function chatRow7(parent, x, y, w) {
  const c = card7(parent, 'card crow7', x, y, w);
  ins(c.c, `<div class="cr7"><div class="cr7av">${bankAv(112)}</div><div class="cr7tx"><b>แบงค์</b><small>ว่างเมื่อไหร่ไปกินหมูกระทะกัน</small></div><div class="cr7t">8 เดือนก่อน</div></div>`);
  const web = ins(c.c, `<svg class="cr7web" width="110" height="110" viewBox="0 0 100 100"><g fill="none" stroke="#b9b2a6" stroke-width="2.4">${[0, 22, 45, 68, 90].map(a => `<path d="M100,0 L${(100 - Math.cos(a * Math.PI / 180) * 100).toFixed(1)},${(Math.sin(a * Math.PI / 180) * 100).toFixed(1)}"/>`).join('')}${[30, 55, 80].map(r => `<path d="M${100 - r},0 Q${100 - r * 0.62},${r * 0.3} ${(100 - r * 0.71).toFixed(1)},${(r * 0.71).toFixed(1)} Q${100 - r * 0.3},${r * 0.62} 100,${r}"/>`).join('')}</g></svg>`);
  return {
    c,
    update(t, tin, tweb) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.45);
      const k = ease.outBack(prog(t, tweb, tweb + 0.4));
      web.style.opacity = prog(t, tweb, tweb + 0.15).toFixed(3);
      web.style.transform = `scale(${k.toFixed(3)})`;
    },
  };
}

// "วันเกิดคุณ" card: cake with a flickering candle and the date
function cakeCard7(parent, x, y, label, date) {
  const c = card7(parent, 'card cake7 pink', x, y);
  ins(c.c, `<div class="ck7"><div class="ck7ic">${cakeSVG(150)}</div><div class="ck7tx"><small>${label}</small><b>${date}</b></div></div>`);
  return {
    c,
    update(t, tin) { enter3d(c.c, t, tin, 'pop'); shine(c.sh, t, tin + 0.4); flicker(c.c, t); },
  };
}

// one midnight notification from แบงค์ with a year tag
function bdayNotif(parent, x, y, w, year, who = 'แบงค์', av = null, msg = 'สุขสันต์วันเกิดนะเพื่อน') {
  const el = html('div', 'notif bn7', parent);
  Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  el.innerHTML = `<div class="app">แชท</div><div class="av">${av || bankAv(96)}</div><div style="flex:1;min-width:0"><div class="who">${who}<small>00:00</small></div><div class="msg">${msg}<span class="mini">${cakeSVG(46)}</span></div></div>${year ? `<div class="yr7">${year}</div>` : ''}`;
  return el;
}
// deck of yearly notifications: the newest drops on top, older ones sink back behind it
function notifDeck(parent, x, y, w, years) {
  const cards = years.map(yr => bdayNotif(parent, x, y, w, yr));
  return {
    cards,
    update(t, times) {
      let newest = -1;
      times.forEach((t0, i) => { if (t >= t0) newest = i; });
      cards.forEach((el, i) => {
        const on = i <= newest, back = newest - i;
        el.style.zIndex = 100 - back;
        if (!on || back > 4) { el.style.opacity = 0; return; }
        const k = spring(t, times[i], 15, 6.5);
        const sink = back === 0 ? 0 : 1, kk = back === 0 ? 0 : spring(t, times[newest], 15, 7);
        const depth = back - 1 + kk;
        const ty = back === 0 ? (1 - k) * -140 : depth * 30 + 0;
        const sc = back === 0 ? 1 : 1 - 0.05 * depth;
        el.style.opacity = back === 0 ? fadeIn(t, times[i], 0.06).toFixed(3) : (sink * (1 - 0.18 * depth)).toFixed(3);
        el.style.setProperty('--co', back === 0 ? 1 : back === 1 ? (1 - clamp(kk * 2.5)).toFixed(3) : 0);   // sinking cards fade to blank backs
        el.style.transform = `translateY(${ty.toFixed(1)}px) scale(${sc.toFixed(3)})`;
        el.style.filter = back === 0 ? 'none' : `brightness(${(1 - 0.1 * depth).toFixed(3)})`;
        flicker(el, t + i);
      });
    },
  };
}

// clock card: "เที่ยงคืนวันเกิด 23:59" → flips to 00:00
function clock7(parent, x, y, label) {
  const c = card7(parent, 'clock', x, y);
  ins(c.c, `<div class="icslot"></div>`);
  const tx = ins(c.c, `<div><div class="tl">${label}</div><div class="tt"><span class="hhmm">23:59</span></div></div>`);
  const clk = clockMoon(c.c.querySelector('.icslot'), 82);
  const hhmm = tx.querySelector('.hhmm'); hhmm.style.display = 'inline-block';
  return {
    c,
    update(t, tin, tflip) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      const f = prog(t, tflip - 0.12, tflip + 0.12);
      hhmm.textContent = t < tflip ? '23:59' : '00:00';
      hhmm.style.transform = `rotateX(${(Math.sin(Math.PI * f) * 80).toFixed(1)}deg)`;
      hhmm.style.color = t < tflip ? '#23242f' : '#e0574b';
      clk.update(t, t < tflip ? 23 : 0, t < tflip ? 59 : 0, t < tflip ? Math.floor(t * 2) * 6 % 60 : 0);
    },
  };
}

// chip with an icon slot
function chip7(parent, x, y, htmlTx, cls = '') {
  const el = html('div', 'chip big ' + cls, parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const slot = html('span', 'icslot', el);
  const tx = html('span', '', el); tx.innerHTML = htmlTx;
  return { el, slot, tx };
}

// chat thread on a phone; items: {k: 'date' | 'L' | 'R' | 'stk', text, meta, t0}
function chatThread7(parent, x, y, w, h, title, avHTML, items, withInput = false) {
  const ph = html('div', 'cphone ct7', parent);
  Object.assign(ph.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
  const scr = html('div', 'cscr', ph);
  const hd = html('div', 'chead', scr); hd.innerHTML = `<span class="cav">${avHTML}</span><b>${title}</b><i class="cdots">⋯</i>`;
  const body = html('div', 'cbody', scr);
  const list = html('div', 'clist', body);
  const its = items.map(o => {
    const row = html('div', 'crow ' + (o.k === 'R' ? 'R' : 'L'), list);
    let el;
    if (o.k === 'date') { row.classList.add('dt7'); el = html('div', 'date7', row, o.text); }
    else if (o.k === 'stk') { el = html('div', 'csticker', row); el.innerHTML = o.html; }
    else el = html('div', 'cbub ' + (o.k === 'R' ? 'R' : ''), row, o.text);
    const meta = o.k === 'date' ? null : html('div', 'cmeta', row, o.meta || '');
    return Object.assign({}, o, { row, el, meta, h: 0 });
  });
  let input = null;
  if (withInput) {
    const bar = html('div', 'cinput', scr);
    const field = html('div', 'cfield', bar); const tx = html('span', '', field); const caret = html('i', 'ccaret', field);
    const send = html('div', 'csend', bar); send.innerHTML = '<svg width="34" height="34" viewBox="0 0 24 24"><path d="M3,11 L21,3 L14,21 L11,13 Z" fill="#fff"/></svg>';
    input = { bar, field, tx, caret, send };
  }
  return {
    el: ph, items: its, input,
    // scrollUp: px scrolled up from the bottom of the visible thread
    update(t, scrollUp = 0) {
      let yy = 0;
      for (const it of its) {
        if (!it.h) it.h = it.row.offsetHeight + 18;
        const on = it.t0 == null || t >= it.t0;
        it.row.style.visibility = on ? 'visible' : 'hidden';
        if (!on) continue;
        const k = it.t0 == null ? 1 : spring(t, it.t0, 15, 6.5);
        it.row.style.transform = `translateY(${(yy + (1 - k) * 60).toFixed(1)}px) scale(${(0.6 + 0.4 * Math.min(1.08, k)).toFixed(3)})`;
        it.row.style.opacity = it.t0 == null ? 1 : fadeIn(t, it.t0, 0.12);
        it.y = yy; yy += it.h;
      }
      const view = body.clientHeight - 20;
      list.style.transform = `translateY(${(-Math.max(0, yy - view) + scrollUp).toFixed(1)}px)`;
      return { content: yy, view };
    },
    type(t, script) {
      if (!input) return '';
      let txt = '';
      for (const sg of script) {
        if (t < sg.t0) break;
        const gs = graphemes(sg.text), k = prog(t, sg.t0, sg.t1);
        txt = sg.mode === 'type' ? gs.slice(0, Math.ceil(k * gs.length)).join('') : sg.text;
      }
      input.tx.textContent = txt;
      input.caret.style.opacity = Math.sin(t * 9) > 0 ? 1 : 0;
      input.send.classList.toggle('on', txt.length > 0);
      return txt;
    },
  };
}

// score card: แบงค์ remembered my birthday 11/11 — I remembered his 0/11
function scoreCard7(parent, x, y, w) {
  const c = card7(parent, 'card score7', x, y, w);
  ins(c.c, `<div class="lbl">จำวันเกิดเพื่อนได้กี่ปี</div>`);
  const row = (av, name, cls) => ins(c.c, `<div class="sc7row ${cls}"><div class="sc7av">${av}</div><div class="sc7mid"><b>${name}</b><div class="sc7dots">${Array.from({ length: 11 }, () => '<i></i>').join('')}</div></div><div class="sc7n"><span class="v">0</span><small>/11</small></div></div>`);
  const r1 = row(bankAv(92), 'แบงค์จำวันเกิดเขา', 'good');
  const r2 = row(meAv(92), 'เขาจำวันเกิดแบงค์', 'bad');
  const d1 = [...r1.querySelectorAll('.sc7dots i')], d2 = [...r2.querySelectorAll('.sc7dots i')];
  const v1 = r1.querySelector('.v'), v2 = r2.querySelector('.v'), n2 = r2.querySelector('.sc7n');
  return {
    c,
    update(t, tin, t1a, t1b, t2, tzero) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      const n = Math.floor(11 * prog(t, t1a, t1b) + 1e-6);
      d1.forEach((d, i) => { const on = i < n; d.classList.toggle('on', on); const k = on ? spring(t, t1a + (t1b - t1a) * i / 11, 18, 6) : 0; d.style.transform = `scale(${(on ? 0.4 + 0.6 * k : 1).toFixed(3)})`; });
      v1.textContent = String(n);
      r2.style.opacity = fadeIn(t, t2, 0.15);
      r2.style.transform = `translateX(${((1 - spring(t, t2, 14, 6.5)) * -60).toFixed(1)}px)`;
      // each empty dot shakes once as the scan passes it
      d2.forEach((d, i) => { const ts = t2 + 0.3 + i * 0.09, x = t - ts; d.style.transform = x > 0 && x < 0.3 ? `translateY(${(Math.sin(x * 40) * 4 * (1 - x / 0.3)).toFixed(1)}px)` : ''; });
      const thump = 1 + 0.35 * Math.exp(-Math.pow((t - tzero - 0.08) * 7, 2));
      n2.style.transform = `scale(${thump.toFixed(3)})`;
      r2.classList.toggle('hot', t >= tzero);
    },
  };
}

// แบงค์'s profile: cover, avatar, name, birthday row (+ "พรุ่งนี้!" stamp)
function profile7(parent, x, y, w) {
  const c = card7(parent, 'card prof prof7', x, y, w);
  ins(c.c, `<div class="pcover" style="background:linear-gradient(120deg,#ffc9a8,#f2a0b8 50%,#b7c8ff)"></div><div class="pav">${bankAv(132)}</div><div class="pname">แบงค์</div><div class="pbio">เพื่อนตั้งแต่ ม.4</div>`);
  const bd = ins(c.c, `<div class="bd7"><span class="bd7ic">${cakeSVG(70)}</span><span class="bd7tx"><small>วันเกิด</small><b>15 พฤศจิกายน</b></span><i class="bd7hl"></i></div>`);
  const hl = bd.querySelector('.bd7hl');
  const stamp = ins(c.c, `<div class="stamp big st7">พรุ่งนี้!</div>`);
  return {
    c,
    update(t, tin, thl, tstamp) {
      enter3d(c.c, t, tin, 'pop'); shine(c.sh, t, tin + 0.4); flicker(c.c, t);
      hl.style.transform = `scaleX(${ease.outCubic(prog(t, thl, thl + 0.45)).toFixed(3)})`;
      const k = spring(t, tstamp, 18, 6);
      stamp.style.opacity = fadeIn(t, tstamp, 0.06);
      stamp.style.transform = `rotate(-12deg) scale(${(2.2 - 1.2 * k).toFixed(3)})`;
      bd.style.transform = t > tstamp && t < tstamp + 0.25 ? `translateY(${(Math.sin((t - tstamp) * 60) * 4).toFixed(1)}px)` : '';
    },
  };
}

// "วันนี้ 14 พ.ย." calendar chip
function todayChip7(parent, x, y) {
  const ch = chip7(parent, x, y, 'วันนี้ <b>14 พ.ย.</b>', 'today7');
  const cal = calendarFlip(ch.slot, 58, '#4a7bd8');
  return { el: ch.el, update(t, t0) { popSquash(ch.el, t, t0); cal.update(t, 14, false); } };
}

// lightbulb "นึกขึ้นได้" drawn in world space above a head
function bulb7(parent) {
  const g = svg('g', { opacity: 0 }, parent);
  const rays = svg('g', {}, g);
  for (let k = 0; k < 8; k++) svg('path', { d: 'M0,-58 L0,-78', stroke: '#ffd66b', 'stroke-width': 7, 'stroke-linecap': 'round', transform: `rotate(${k * 45 - 157.5})` }, rays);
  svg('circle', { r: 46, fill: '#ffe9a0', opacity: 0.35 }, g);
  svg('path', { d: 'M-28,-6 C-28,-44 28,-44 28,-6 C28,10 16,16 14,28 L-14,28 C-16,16 -28,10 -28,-6 Z', fill: '#ffe066', stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, g);
  svg('rect', { x: -14, y: 28, width: 28, height: 16, rx: 4, fill: '#9aa3b2', stroke: INK, 'stroke-width': 4 }, g);
  svg('path', { d: 'M-8,8 L-4,-6 L0,6 L4,-6 L8,8', fill: 'none', stroke: '#c98a1a', 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, g);
  svg('path', { d: 'M-16,-18 Q-14,-30 -2,-32', fill: 'none', stroke: '#fff', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
  return (t, t0, x, y) => {
    const k = spring(t, t0, 16, 6);
    g.setAttribute('opacity', fadeIn(t, t0, 0.08));
    g.setAttribute('transform', `translate(${x.toFixed(1)},${(y - 30 * k).toFixed(1)}) scale(${Math.max(0.001, k).toFixed(3)})`);
    rays.setAttribute('opacity', (0.6 + 0.4 * Math.sin(t * 14)).toFixed(3));
  };
}

// small "คนแรก!" medal badge
function firstBadge7(parent, x, y) {
  const el = html('div', 'first7', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="64" height="74" viewBox="-32 -30 64 74"><path d="M-14,8 L-22,40 L-8,32 L0,44 L4,10 Z M14,8 L22,40 L8,32 L0,44 L-4,10 Z" fill="#e0574b" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/><circle r="24" fill="#f2c14e" stroke="${INK}" stroke-width="4"/><circle r="15" fill="none" stroke="#fff3c4" stroke-width="3"/><text y="8" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#8a5a10">1</text></svg><b>คนแรก!</b>`;
  return { el, update(t, t0) { popSquash(el, t, t0, '', 20); } };
}

// a row of year dots under the deck; each lights up as that year's wish arrives
function yearLine7(parent, x, y, w, years) {
  const el = html('div', 'yl7', parent); Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  html('i', 'yl7bar', el);
  const fill = html('i', 'yl7fill', el);
  const dots = years.map((yr, i) => { const d = html('div', 'yl7d', el); d.style.left = (i / (years.length - 1) * 100) + '%'; html('span', '', d); html('b', '', d, yr); return d; });
  return {
    el,
    update(t, tin, times) {
      el.style.opacity = fadeIn(t, tin, 0.2);
      let n = 0;
      dots.forEach((d, i) => { const on = t >= times[i]; if (on) n = i; d.classList.toggle('on', on); const k = on ? spring(t, times[i], 18, 6) : 1; d.style.transform = `translateX(-50%) scale(${(on ? 0.6 + 0.4 * k : 1).toFixed(3)})`; });
      fill.style.width = (t >= times[0] ? n / (dots.length - 1) * 100 : 0).toFixed(2) + '%';
    },
  };
}
