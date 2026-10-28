// "47 ครั้งที่ลบข้อความ" UI: chat input that types and deletes, delete counter + crumpled paper, worry bubbles,
// profile card with photo carousel, night clock, bear-hug sticker, falling heart, "<1 วินาที" chip, big send button, rival banner.

// bear hugging a heart: the sticker he sends by accident
function bearHugSVG(w, word = 'กอดๆ') {
  const id = 'bh' + Math.random().toString(36).slice(2, 7);
  const c = '#c8895a', c2 = '#e8b98a', ink = INK;
  return `<svg width="${w}" height="${w}" viewBox="0 0 200 200"><defs><radialGradient id="${id}" cx=".5" cy=".45" r=".65"><stop offset="0" stop-color="#fff6fa"/><stop offset="1" stop-color="#ffc4d6"/></radialGradient></defs>
  <rect x="4" y="4" width="192" height="192" rx="34" fill="url(#${id})" stroke="#f07aa8" stroke-width="5"/>
  <circle cx="64" cy="44" r="16" fill="${c}" stroke="${ink}" stroke-width="4"/><circle cx="136" cy="44" r="16" fill="${c}" stroke="${ink}" stroke-width="4"/>
  <ellipse cx="100" cy="128" rx="54" ry="44" fill="${c}" stroke="${ink}" stroke-width="4"/>
  <circle cx="100" cy="72" r="40" fill="${c}" stroke="${ink}" stroke-width="4"/>
  <ellipse cx="100" cy="84" rx="18" ry="13" fill="${c2}"/><ellipse cx="100" cy="79" rx="6" ry="4.5" fill="${ink}"/>
  <path d="M80,66 q6,-7 12,0 M108,66 q6,-7 12,0" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round"/>
  <ellipse cx="74" cy="84" rx="9" ry="5" fill="#f07aa8" opacity=".6"/><ellipse cx="126" cy="84" rx="9" ry="5" fill="#f07aa8" opacity=".6"/>
  <path d="M100,158 C60,134 66,106 100,122 C134,106 140,134 100,158 Z" fill="#f04f7f" stroke="${ink}" stroke-width="4"/>
  <ellipse cx="62" cy="128" rx="16" ry="24" fill="${c}" stroke="${ink}" stroke-width="4" transform="rotate(-30 62 128)"/><ellipse cx="138" cy="128" rx="16" ry="24" fill="${c}" stroke="${ink}" stroke-width="4" transform="rotate(30 138 128)"/>
  <path d="M30,40 l4,-9 l4,9 l9,4 l-9,4 l-4,9 l-4,-9 l-9,-4 Z M168,30 l3,-7 l3,7 l7,3 l-7,3 l-3,7 l-3,-7 l-7,-3 Z" fill="#fff"/>
  <text x="100" y="192" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#e0457a" stroke="#fff" stroke-width="7" paint-order="stroke">${word}</text></svg>`;
}

// chat input bar inside a chatPhone; script = [{t0, t1, text, mode: 'type' | 'del' | 'hold'}]
function chatInput(chat) {
  const scr = chat.el.querySelector('.cscr');
  const bar = html('div', 'cinput', scr);
  const field = html('div', 'cfield', bar); const tx = html('span', '', field); const caret = html('i', 'ccaret', field);
  const send = html('div', 'csend', bar); send.innerHTML = '<svg width="34" height="34" viewBox="0 0 24 24"><path d="M3,11 L21,3 L14,21 L11,13 Z" fill="#fff"/></svg>';
  return {
    bar, send,
    update(t, script) {
      let txt = '';
      for (const sg of script) {
        if (t < sg.t0) break;
        const gs = graphemes(sg.text), k = prog(t, sg.t0, sg.t1);
        if (sg.mode === 'type') txt = gs.slice(0, Math.ceil(k * gs.length)).join('');
        else if (sg.mode === 'del') txt = gs.slice(0, Math.floor((1 - k) * gs.length)).join('');
        else txt = sg.text;
      }
      tx.textContent = txt;
      caret.style.opacity = Math.sin(t * 9) > 0 ? 1 : 0;
      send.classList.toggle('on', txt.length > 0);
    },
  };
}

// trash chip: "ลบไปแล้ว N ครั้ง", the lid pops on each delete
function deleteCounter(parent, x, y, label = 'ลบไปแล้ว') {
  const el = html('div', 'chip big delchip', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const b = iconBox(el, 60, 60, '-30 -32 60 64');
  svg('path', { d: 'M-17,-12 L17,-12 L13,26 L-13,26 Z', fill: '#9fb3c8', stroke: INK, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, b.s);
  for (const lx of [-7, 0, 7]) svg('path', { d: `M${lx},-6 L${lx * 0.8},20`, stroke: INK, 'stroke-width': 2.5 }, b.s);
  const lid = svg('g', {}, b.s);
  svg('rect', { x: -21, y: -20, width: 42, height: 8, rx: 3, fill: '#c7d4e2', stroke: INK, 'stroke-width': 3.5 }, lid);
  svg('rect', { x: -6, y: -26, width: 12, height: 7, rx: 2, fill: '#c7d4e2', stroke: INK, 'stroke-width': 3 }, lid);
  const tx = html('span', '', el); tx.innerHTML = `${label} `;
  const n = html('b', '', tx); const od = new Odometer(n, 2); html('span', '', tx, ' ครั้ง');
  return {
    el,
    update(t, t0, v, speed = 0, pops = []) {
      popSquash(el, t, t0);
      od.set(v, speed);
      const p = pops.map(tp => Math.exp(-Math.pow((t - tp) * 9, 2))).reduce((a, b) => Math.max(a, b), 0);
      lid.setAttribute('transform', `translate(-17,-12) rotate(${(-40 * p).toFixed(1)}) translate(17,12)`);
      el.style.transform = (el.style.transform || '') + ` scale(${(1 + 0.08 * p).toFixed(3)})`;
    },
  };
}

// crumpled paper balls flying from (x0,y0) into the trash at (x1,y1), one per time in ts
function paperBalls(parent, ts) {
  const balls = ts.map(() => {
    const g = svg('g', { opacity: 0 }, parent);
    svg('path', { d: 'M-16,-4 L-10,-15 L2,-17 L13,-10 L17,2 L10,14 L-3,17 L-14,10 Z', fill: '#ffffff', stroke: INK, 'stroke-width': 3, 'stroke-linejoin': 'round' }, g);
    svg('path', { d: 'M-8,-6 L2,0 L-4,8 M4,-10 L8,2', stroke: '#9aa6b2', 'stroke-width': 2, fill: 'none' }, g);
    return g;
  });
  return (t, x0, y0, x1, y1) => balls.forEach((g, i) => {
    const k = prog(t, ts[i], ts[i] + 0.45);
    if (k <= 0 || k >= 1) { g.setAttribute('opacity', 0); return; }
    const e = ease.inOutSine(k), x = lerp(x0, x1, e), y = lerp(y0, y1, e) - Math.sin(Math.PI * e) * 220;
    g.setAttribute('opacity', 1);
    g.setAttribute('transform', `translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${(k * 540).toFixed(1)}) scale(${(1.2 - 0.5 * k).toFixed(3)})`);
  });
}

// worry thought-bubbles above his head
function fearBubble(parent, x, y, kind, text) {
  const el = html('div', 'fear', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const ic = html('div', 'fic', el);
  if (kind === 'annoyed') {
    ic.innerHTML = portrait4('girl', 92, '#fde2e8') + '<svg class="fmark" width="44" height="44" viewBox="-22 -22 44 44">' + [0, 1, 2, 3].map(k => `<path d="M3,-13 Q3,-3 13,-3" fill="none" stroke="#e0453b" stroke-width="6" stroke-linecap="round" transform="rotate(${k * 90})"/>`).join('') + '</svg>';
  } else if (kind === 'noreply') {
    ic.innerHTML = '<svg width="110" height="92" viewBox="0 0 110 92"><rect x="6" y="8" width="98" height="56" rx="20" fill="#9be38b" stroke="#33252a" stroke-width="4"/><text x="55" y="44" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="22" fill="#23242f">ทักนะ</text><text x="100" y="86" text-anchor="end" font-family="Kanit" font-size="17" fill="#7f8a94">อ่านแล้ว</text><circle cx="20" cy="80" r="5" fill="#9aa6b2"/><circle cx="34" cy="80" r="5" fill="#9aa6b2"/><circle cx="48" cy="80" r="5" fill="#9aa6b2"/></svg>';
  } else {
    ic.innerHTML = `<svg width="100" height="92" viewBox="-50 -46 100 92"><defs><clipPath id="hl${x}"><rect x="-60" y="-60" width="60" height="120"/></clipPath></defs><path d="${heartPathT(0, 4, 34)}" fill="#e9e3ea" stroke="#9aa6b2" stroke-width="4" stroke-dasharray="7 6"/><path d="${heartPathT(0, 4, 34)}" fill="#f04f7f" stroke="#33252a" stroke-width="4" clip-path="url(#hl${x})"/></svg>`;
  }
  html('div', 'ftx', el, text);
  const tail = [0, 1].map(() => html('i', 'ftail', parent));
  return {
    el,
    update(t, t0, tx, ty, out = 99) {
      const k = spring(t, t0, 13, 6), o = fadeIn(t, t0, 0.12) * (1 - prog(t, out, out + 0.3));
      el.style.opacity = o.toFixed(3);
      el.style.transform = `translateY(${(Math.sin(t * 1.6 + x) * 6).toFixed(1)}px) scale(${(0.4 + 0.6 * k).toFixed(3)})`;
      const bx = x + 110, by = y + 190;
      tail.forEach((d, i) => { const u = (i + 1) / 3; d.style.left = lerp(bx, tx, u).toFixed(1) + 'px'; d.style.top = lerp(by, ty, u).toFixed(1) + 'px'; d.style.opacity = (o * (t > t0 + 0.05 * i ? 1 : 0)).toFixed(3); d.style.transform = `scale(${(1 - u * 0.4).toFixed(2)})`; });
    },
  };
}

// her profile: cover, avatar, name, bio and a swiping photo carousel
function profileCard(parent, x, y, w) {
  const c = cardEl(parent, 'card prof', x, y, w);
  const cover = html('div', 'pcover', c.c);
  const av = html('div', 'pav', c.c); av.innerHTML = portrait4('girl', 132, '#fde2e8');
  html('div', 'pname', c.c, 'ฝน');
  html('div', 'pbio', c.c, 'ชอบฝน · ชาไข่มุก · แมว');
  const strip = html('div', 'pstrip', c.c);
  const bgs = ['#ffd6e2', '#cfe8ff', '#fff0c2', '#d8f2d0'];
  const photos = bgs.map(bg => { const ph = html('div', 'pphoto', strip); const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); setA(d, { width: 210, height: 210, viewBox: '-60 -60 120 120' }); svg('rect', { x: -60, y: -60, width: 120, height: 120, fill: bg }, d); faceFront4(d, 0, 6, 34, 'girl'); ph.appendChild(d); return ph; });
  const heart = html('div', 'pheart', c.c); heart.innerHTML = `<svg width="64" height="64" viewBox="-32 -32 64 64"><path d="${heartPathT(0, 2, 22)}" fill="#f04f7f" stroke="#fff" stroke-width="3"/></svg>`;
  return {
    c,
    update(t, tin, tswipe, out = 99) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      c.c.style.opacity = (parseFloat(c.c.style.opacity || 0) * (1 - prog(t, out, out + 0.3))).toFixed(3);
      const idx = Math.max(0, (t - tswipe) / 0.55), i = Math.floor(idx), f = ease.inOutCubic(clamp((idx - i) * 2.2));
      strip.style.transform = `translateX(${(-(Math.min(i, 3) + (i < 3 ? f : 0)) * 226).toFixed(1)}px)`;
      const hk = t > tswipe ? Math.max(0, Math.sin((t - tswipe) * 6)) : 0;
      heart.style.opacity = t > tswipe ? 1 : 0;
      heart.style.transform = `scale(${(0.8 + 0.3 * hk).toFixed(3)})`;
    },
  };
}

// clock card with a moon, showing a given time string
function nightClock(parent, x, y, label) {
  const c = cardEl(parent, 'clock', x, y);
  c.c.innerHTML += `<div class="icslot"></div><div><div class="tl">${label}</div><div class="tt"><span class="hhmm">21:00</span></div></div>`;
  const clk = clockMoon(c.c.querySelector('.icslot'), 82);
  const hhmm = c.c.querySelector('.hhmm');
  return {
    c,
    update(t, tin, minutes) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      const m = Math.floor(minutes) % (24 * 60), hh = Math.floor(m / 60), mm = m % 60;
      hhmm.textContent = `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}`;
      clk.update(t, hh, mm);
    },
  };
}

// heart dropping out of frame with speed lines ("ใจหล่นวูบ")
function fallingHeart(parent) {
  const g = svg('g', { opacity: 0 }, parent);
  for (const lx of [-34, 0, 34]) svg('path', { d: `M${lx},-90 L${lx},-40`, stroke: '#ffffff', 'stroke-width': 6, 'stroke-linecap': 'round', opacity: 0.8 }, g);
  svg('path', { d: heartPathT(0, 0, 46), fill: '#f04f7f', stroke: INK, 'stroke-width': 5 }, g);
  return (t, t0, x, y) => {
    const k = prog(t, t0, t0 + 0.9);
    g.setAttribute('opacity', k > 0 && k < 1 ? 1 : 0);
    g.setAttribute('transform', `translate(${(x + Math.sin(k * 20) * 8).toFixed(1)},${(y + 900 * k * k).toFixed(1)}) rotate(${(Math.sin(k * 14) * 12).toFixed(1)})`);
  };
}

// stopwatch chip: "ไม่ถึง 1 วินาที"
function fastChip(parent, x, y) {
  const el = html('div', 'chip big', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const b = iconBox(el, 56, 56, '-30 -30 60 60');
  svg('circle', { r: 22, fill: '#fff', stroke: INK, 'stroke-width': 4 }, b.s);
  svg('rect', { x: -5, y: -32, width: 10, height: 8, rx: 2, fill: INK }, b.s);
  const hand = svg('path', { d: 'M0,0 L0,-16', stroke: '#e0453b', 'stroke-width': 4, 'stroke-linecap': 'round' }, b.s);
  const tx = html('span', '', el); tx.innerHTML = 'ไม่ถึง <b>1</b> วินาที';
  return { el, update(t, t0) { popSquash(el, t, t0); hand.setAttribute('transform', `rotate(${((t - t0) * 360).toFixed(1)})`); } };
}

// big round send button with ripples
function bigSend(parent, x, y) {
  const el = html('div', 'bigsend', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = '<div class="bsr"></div><div class="bsr"></div><div class="bsb"><svg width="96" height="96" viewBox="0 0 24 24"><path d="M3,11 L21,3 L14,21 L11,13 Z" fill="#fff"/></svg></div><div class="bsl">ส่ง</div>';
  const btn = el.querySelector('.bsb'), rings = el.querySelectorAll('.bsr');
  return {
    el,
    update(t, tin, presses, out = 99) {
      popSquash(el, t, tin);
      el.style.opacity = (parseFloat(el.style.opacity || 0) * (1 - prog(t, out, out + 0.3))).toFixed(3);
      const p = presses.some(tp => t > tp && t < tp + 0.14);
      btn.style.transform = `scale(${p ? 0.88 : 1 + 0.04 * Math.sin(t * 6)})`;
      rings.forEach((r, i) => { const last = presses.filter(tp => t >= tp).pop(); const q = last != null ? prog(t, last + i * 0.1, last + 0.7 + i * 0.1) : 0; r.style.opacity = q > 0 && q < 1 ? (1 - q).toFixed(2) : 0; r.style.transform = `scale(${(1 + q * 1.2).toFixed(3)})`; });
    },
  };
}

// a rival's message banner on her phone
function rivalBanner(parent, y) {
  const el = html('div', 'notif', parent); el.style.top = y + 'px';
  el.innerHTML = `<div class="app">แชท</div><div class="av"><svg width="96" height="96" viewBox="-48 -48 96 96"><circle r="48" fill="#d9dde6"/><circle cy="-6" r="22" fill="#9aa3b2"/><path d="M-36,48 C-32,16 32,16 36,48 Z" fill="#9aa3b2"/></svg></div><div style="flex:1"><div class="who">ต้น<small>ตอนนี้</small></div><div class="msg">กินข้าวยังครับ</div></div>`;
  return {
    el,
    update(t, tin, tswipe = 99) {
      const k = spring(t, tin, 13, 6), sw = ease.inCubic(prog(t, tswipe, tswipe + 0.35));
      el.style.opacity = (fadeIn(t, tin, 0.12) * (1 - prog(t, tswipe + 0.2, tswipe + 0.4))).toFixed(3);
      el.style.transform = `translateY(${((1 - k) * -160).toFixed(1)}px) translateX(${(sw * 1100).toFixed(1)}px) rotate(${(sw * 8).toFixed(2)}deg)`;
    },
  };
}
