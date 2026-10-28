// "39 บาทที่แม่ไม่กล้ากด" UI: 11.11 badge, product tiles, cart cards, LINE banner, the ฿39 slippers (new and old with
// wire), price-vs-shipping card, order summary with quantity / shipping / success, parcel.

// flip-flop pair (top view). o.old: faded, cracked, the strap wired back on
function slippersSVG(w, o = {}) {
  const sole = o.old ? '#b9a37e' : (o.c || '#4fc3e0'), strap = o.old ? '#7a6a8a' : (o.strap || '#f07aa8');
  const one = (x, flip) => `<g transform="translate(${x},0) scale(${flip},1)">
    <path d="M0,-58 C26,-58 34,-30 30,0 C28,30 26,56 0,58 C-26,56 -28,30 -30,0 C-34,-30 -26,-58 0,-58 Z" fill="${sole}" stroke="${INK}" stroke-width="4"/>
    <path d="M0,-58 C20,-56 26,-34 24,-10" fill="none" stroke="${o.old ? '#a08a66' : '#fff'}" stroke-width="4" opacity=".55"/>
    ${o.old ? '<path d="M-12,22 l8,6 l-4,8 l8,6" fill="none" stroke="#6a5a44" stroke-width="2.5"/><path d="M14,-30 l-6,6 l5,5" fill="none" stroke="#6a5a44" stroke-width="2.2"/>' : ''}
    <path d="M-24,-2 Q-14,-30 0,-36 Q14,-30 24,-2" fill="none" stroke="${INK}" stroke-width="12" stroke-linecap="round"/>
    <path d="M-24,-2 Q-14,-30 0,-36 Q14,-30 24,-2" fill="none" stroke="${strap}" stroke-width="7" stroke-linecap="round"/>
    <circle cx="0" cy="-36" r="6" fill="${strap}" stroke="${INK}" stroke-width="3"/>
    ${o.old ? `<g class="wire9">${[-8, -3, 2, 7].map(dy => `<path d="M-8,${-36 + dy} q8,-4 16,0" fill="none" stroke="#c9d2dc" stroke-width="3" stroke-linecap="round"/><path d="M-8,${-36 + dy} q8,-4 16,0" fill="none" stroke="#6b7280" stroke-width="1.2"/>`).join('')}<path d="M8,-30 q10,6 6,14" fill="none" stroke="#9aa3b2" stroke-width="3" stroke-linecap="round"/></g>` : ''}
  </g>`;
  return `<svg width="${w}" height="${w * 0.9}" viewBox="-80 -70 160 140" style="overflow:visible">${one(-36, -1)}${one(36, 1)}</svg>`;
}
// small product icons for the sale grid
const PROD = {
  cream: `<rect x="-22" y="-10" width="44" height="34" rx="8" fill="#ffd6e4" stroke="${INK}" stroke-width="3.5"/><rect x="-24" y="-22" width="48" height="14" rx="5" fill="#f07aa8" stroke="${INK}" stroke-width="3.5"/>`,
  tee: `<path d="M-26,-18 L-12,-26 Q0,-18 12,-26 L26,-18 L34,-4 L22,2 L22,26 L-22,26 L-22,2 L-34,-4 Z" fill="#7fc29e" stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"/>`,
  buds: `<rect x="-26" y="-14" width="52" height="34" rx="16" fill="#fff" stroke="${INK}" stroke-width="3.5"/><circle cx="-10" cy="2" r="7" fill="#c9d2dc"/><circle cx="10" cy="2" r="7" fill="#c9d2dc"/>`,
  bag: `<path d="M-24,-8 L24,-8 L28,26 L-28,26 Z" fill="#f2c463" stroke="${INK}" stroke-width="3.5"/><path d="M-12,-8 Q-12,-26 0,-26 Q12,-26 12,-8" fill="none" stroke="${INK}" stroke-width="3.5"/>`,
  lip: `<rect x="-9" y="-6" width="18" height="30" rx="3" fill="#2a2a33" stroke="${INK}" stroke-width="3"/><path d="M-7,-6 L-7,-24 Q0,-30 7,-20 L7,-6 Z" fill="#e0453b" stroke="${INK}" stroke-width="3"/>`,
  shoe: `<path d="M-30,10 Q-30,-14 -12,-14 L4,-4 Q24,0 30,10 L30,18 L-30,18 Z" fill="#fff" stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"/><path d="M-30,14 L30,14" stroke="#4a7bd8" stroke-width="4"/>`,
};
const prodSVG = (k, w) => `<svg width="${w}" height="${w}" viewBox="-40 -40 80 80">${PROD[k]}</svg>`;

// "11.11" sale badge
function saleBadge(parent, x, y) {
  const el = html('div', 'sale9', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = '<b>11.11</b><small>ลดทั้งแอป</small>';
  return { el, update(t, t0) { popSquash(el, t, t0, `rotate(${(-6 + Math.sin(t * 3) * 2).toFixed(2)}deg)`, -20); } };
}

// sale grid on her phone: six products, each "+" flips to ✓ as it lands in the cart
function saleGrid(parent, x, y, w) {
  const c = card7(parent, 'card grid9', x, y, w);
  ins(c.c, `<div class="lbl"><span class="sb9">11.11</span>ลดแรง ทั้งแอป</div>`);
  const items = [['cream', 'ครีม', 159], ['tee', 'เสื้อ', 199], ['buds', 'หูฟัง', 399], ['bag', 'กระเป๋า', 259], ['lip', 'ลิป', 89], ['shoe', 'รองเท้า', 590]];
  const grid = ins(c.c, `<div class="g9">${items.map(([k, n, p]) => `<div class="t9"><span class="ti9">${prodSVG(k, 84)}</span><b>${n}</b><small>฿${p}</small><i class="add9">+</i></div>`).join('')}</div>`);
  const tiles = [...grid.children];
  return { c, update(t, tin, adds) { enter3d(c.c, t, tin, 'pop'); shine(c.sh, t, tin + 0.5); tiles.forEach((tl, i) => { const on = adds[i] != null && t >= adds[i]; tl.classList.toggle('on', on); tl.querySelector('.add9').textContent = on ? '✓' : '+'; tl.style.transform = `scale(${(1 + 0.12 * Math.exp(-Math.pow((t - (adds[i] ?? -9)) * 8, 2))).toFixed(3)})`; }); } };
}

// cart count chip with an odometer
function cartChip(parent, x, y, label) {
  const el = html('div', 'chip big cart9', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="ic5"><svg width="58" height="54" viewBox="-30 -28 60 56"><path d="M-26,-20 L-16,-20 L-8,12 L20,12 L26,-12 L-12,-12" fill="none" stroke="${INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/><path d="M-12,-12 L26,-12 L20,12 L-8,12 Z" fill="#ff8a5a"/><circle cx="-4" cy="22" r="5" fill="${INK}"/><circle cx="16" cy="22" r="5" fill="${INK}"/></svg></span><span>${label} </span><b class="o9"></b><span> ชิ้น</span>`;
  const od = new Odometer(el.querySelector('.o9'), 2);
  return { el, update(t, t0, v, speed) { popSquash(el, t, t0); od.set(v, speed); } };
}

// LINE-style banner from แม่
function lineBanner(parent, y, msgHTML) {
  const el = html('div', 'notif ln9', parent); el.style.top = y + 'px';
  el.innerHTML = `<div class="app" style="background:#06c755">LINE</div><div class="av">${mom9Av(96)}</div><div style="flex:1;min-width:0"><div class="who">แม่<small>23:41</small></div><div class="msg">${msgHTML}</div></div>`;
  return el;
}

// a cart card: avatar + "ตะกร้าของ…", rows of items, item count
function cartCard9(parent, x, y, w, title, avHTML, rows) {
  const c = card7(parent, 'card cartc9', x, y, w);
  ins(c.c, `<div class="cc9h"><span class="pav8">${avHTML}</span><b>${title}</b><span class="cc9n">0</span></div>`);
  const n = c.c.querySelector('.cc9n');
  const list = ins(c.c, `<div class="cc9l">${rows.map(([ic, name, price]) => `<div class="cc9r"><span>${ic}</span><b>${name}</b><small>${price}</small></div>`).join('')}</div>`);
  const rs = [...list.children];
  return { c, rows: rs, update(t, tin, times) { enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.4); let k = 0; rs.forEach((r, i) => { const on = t >= times[i]; if (on) k++; r.style.display = on ? 'flex' : 'none'; r.style.opacity = fadeIn(t, times[i], 0.08); }); n.textContent = k; } };
}

// mom's cart on her phone: the one item, the date it was added
function momCart9(parent, x, y, w) {
  const c = card7(parent, 'card mcart9', x, y, w);
  ins(c.c, `<div class="lbl"><span class="ic5"><svg width="40" height="38" viewBox="-30 -28 60 56"><path d="M-26,-20 L-16,-20 L-8,12 L20,12 L26,-12 L-12,-12" fill="none" stroke="${INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/><path d="M-12,-12 L26,-12 L20,12 L-8,12 Z" fill="#ff8a5a"/></svg></span>ตะกร้าของแม่ <span class="mc9n">(1)</span></div>`);
  const row = ins(c.c, `<div class="mc9r"><span class="mc9img">${slippersSVG(150, { c: '#4fc3e0', strap: '#f07aa8' })}</span><div class="mc9tx"><b>รองเท้าแตะ ใส่สบาย</b><small>สีฟ้า · ไซซ์ 38</small><span class="mc9p">฿39</span></div></div>`);
  const date = ins(c.c, `<div class="mc9d">เพิ่มลงตะกร้าเมื่อ <b>11.11.2568</b><i></i></div>`);
  const hl = date.querySelector('i');
  const stamp = ins(c.c, `<div class="stamp big st9">1 ปี</div>`);
  return {
    c,
    update(t, tin, trow, tdate, tstamp) {
      enter3d(c.c, t, tin, 'pop'); shine(c.sh, t, tin + 0.4);
      const kr = spring(t, trow, 15, 6); row.style.opacity = fadeIn(t, trow, 0.1); row.style.transform = `translateY(${((1 - kr) * 40).toFixed(1)}px)`;
      date.style.opacity = fadeIn(t, tdate, 0.12); hl.style.transform = `scaleX(${ease.outCubic(prog(t, tdate + 0.1, tdate + 0.5)).toFixed(3)})`;
      const ks = spring(t, tstamp, 18, 6); stamp.style.opacity = fadeIn(t, tstamp, 0.06); stamp.style.transform = `rotate(-12deg) scale(${(2.2 - 1.2 * ks).toFixed(3)})`;
    },
  };
}

// ฿39 shoes vs ฿40 shipping
function priceVs9(parent, x, y, w) {
  const c = card7(parent, 'card vs9', x, y, w);
  const row = ins(c.c, `<div class="vs9r"><div class="vs9t"><span class="ic5">${slippersSVG(110)}</span><small>รองเท้า</small><b>฿39</b></div><i class="vs9s">&lt;</i><div class="vs9t hot"><span class="ic5"><svg width="110" height="99" viewBox="-60 -50 120 100"><path d="M-50,-20 L14,-20 L14,22 L-50,22 Z" fill="#f2c463" stroke="${INK}" stroke-width="4"/><path d="M14,-8 L36,-8 L50,8 L50,22 L14,22 Z" fill="#e0574b" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M20,-2 L34,-2 L42,8 L20,8 Z" fill="#cfe4ff" stroke="${INK}" stroke-width="2.5"/><circle cx="-30" cy="26" r="10" fill="#2a2a33" stroke="${INK}" stroke-width="3"/><circle cx="34" cy="26" r="10" fill="#2a2a33" stroke="${INK}" stroke-width="3"/></svg></span><small>ค่าส่ง</small><b>฿40</b></div></div>`);
  const [a, sgn, b] = row.children;
  const note = ins(c.c, `<div class="vs9n">ค่าส่ง <b>แพงกว่ารองเท้า</b> อีก</div>`);
  return {
    c,
    update(t, tin, ta, tb, tnote) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      [[a, ta], [b, tb]].forEach(([e, t0]) => { e.style.opacity = fadeIn(t, t0, 0.1); e.style.transform = `scale(${Math.max(0.01, spring(t, t0, 16, 6)).toFixed(3)})`; });
      sgn.style.opacity = fadeIn(t, tb + 0.1, 0.1);
      popSquash(note, t, tnote, '', 10);
    },
  };
}

// close-up card of mom's worn-out slippers held together with wire
function oldSlipCard(parent, x, y, w) {
  const c = card7(parent, 'card old9', x, y, w);
  ins(c.c, `<div class="lbl">รองเท้าคู่เก่าของแม่</div>`);
  const pic = ins(c.c, `<div class="old9p">${slippersSVG(w * 0.62, { old: true })}<span class="old9l">ลวดมัดไว้</span></div>`);
  const lab = pic.querySelector('.old9l');
  return {
    c,
    update(t, tin, twire) {
      enter3d(c.c, t, tin, 'pop'); shine(c.sh, t, tin + 0.4);
      const k = spring(t, twire, 16, 6); lab.style.opacity = fadeIn(t, twire, 0.1); lab.style.transform = `scale(${Math.max(0.01, k).toFixed(3)}) rotate(-6deg)`;
      pic.querySelectorAll('.wire9').forEach(g => g.setAttribute('opacity', t > twire && t < twire + 1.2 ? (0.55 + 0.45 * Math.sin((t - twire) * 18)).toFixed(3) : 1));
    },
  };
}

// order summary: quantity 1→2, shipping paid, then the success state
function orderCard9(parent, x, y, w) {
  const c = card7(parent, 'card ord9', x, y, w);
  ins(c.c, `<div class="lbl">สั่งซื้อให้แม่</div>`);
  ins(c.c, `<div class="o9r"><span class="ic5">${slippersSVG(110)}</span><div class="o9tx"><b>รองเท้าแตะ ใส่สบาย</b><small>฿39 / คู่</small></div><div class="o9q"><i>−</i><b class="q9">1</b><i>+</i></div></div>`);
  const ship = ins(c.c, `<div class="o9s"><span>ค่าส่ง</span><b>฿40</b><em>ฝ้ายจ่ายให้</em></div>`);
  const btn = ins(c.c, `<div class="o9b">สั่งซื้อ <span class="tot9">฿118</span></div>`);
  const ok = ins(c.c, `<div class="o9ok"><span class="ic5"><svg width="60" height="60" viewBox="-30 -30 60 60"><circle r="26" fill="#2f9e5b"/><path d="M-12,0 L-3,10 L14,-10" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></span>สั่งซื้อสำเร็จ · 2 คู่</div>`);
  const q = c.c.querySelector('.q9');
  return {
    c, btn,
    update(t, tin, tq, tship, ttap, tok) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      q.textContent = t >= tq ? '2' : '1'; q.style.transform = `scale(${(1 + 0.5 * Math.exp(-Math.pow((t - tq - 0.05) * 9, 2))).toFixed(3)})`;
      ship.classList.toggle('paid', t >= tship); ship.style.transform = `scale(${(1 + 0.08 * Math.exp(-Math.pow((t - tship - 0.05) * 9, 2))).toFixed(3)})`;
      btn.classList.toggle('on', t >= ttap && t < ttap + 0.25);
      const k = spring(t, tok, 15, 6); ok.style.opacity = fadeIn(t, tok, 0.1); ok.style.transform = `scale(${Math.max(0.01, k).toFixed(3)})`;
      btn.style.opacity = (1 - fadeIn(t, tok, 0.1)).toFixed(3);
    },
  };
}

// parcel box (world space)
function parcel9(parent) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M-70,-10 L70,-10 L70,60 L-70,60 Z', fill: '#d9a86a', stroke: INK, 'stroke-width': 5 }, g);
  const flapL = svg('path', { d: 'M-70,-10 L-6,-10 L-20,-44 L-80,-38 Z', fill: '#e8bc80', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  const flapR = svg('path', { d: 'M70,-10 L6,-10 L20,-44 L80,-38 Z', fill: '#e8bc80', stroke: INK, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, g);
  svg('rect', { x: -26, y: 8, width: 52, height: 30, rx: 4, fill: '#fff', stroke: INK, 'stroke-width': 3 }, g);
  svg('path', { d: 'M-18,18 h36 M-18,28 h24', stroke: '#8a847c', 'stroke-width': 3 }, g);
  return g;
}

// ======================= pro upgrades =======================
// ฿39 shoes vs ฿40 shipping on a balance scale: the shoes sit on the left pan, the shipping box drops onto the right
// pan and the beam swings over to it with a heavy, damped overshoot
function balance9(parent, x, y, w) {
  const c = card7(parent, 'card bal9', x, y, w);
  ins(c.c, `<div class="lbl">รองเท้า <b class="b9a">฿39</b><span class="b9vs">กับ</span>ค่าส่ง <b class="b9b">฿40</b></div>`);
  const W = w - 64;
  const box = `<g transform="translate(0,-4)"><path d="M-58,-62 L58,-62 L58,0 L-58,0 Z" fill="#d9a86a" stroke="${INK}" stroke-width="5"/><path d="M-58,-62 L-36,-84 L80,-84 L58,-62 Z" fill="#e8bc80" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M58,0 L80,-22 L80,-84 L58,-62 Z" fill="#c4935a" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M-8,-62 L-8,0 M8,-62 L8,0" stroke="#e0574b" stroke-width="7"/><rect x="-46" y="-48" width="34" height="22" rx="3" fill="#fff" stroke="${INK}" stroke-width="2.5"/><g transform="translate(20,-40)"><path d="M-14,-10 L6,-10 L6,10 L-14,10 Z M6,-4 L14,-4 L18,4 L18,10 L6,10" fill="#4a7bd8" stroke="${INK}" stroke-width="2.5" stroke-linejoin="round"/><circle cx="-8" cy="12" r="3.5" fill="${INK}"/><circle cx="12" cy="12" r="3.5" fill="${INK}"/></g></g>`;
  const pan = (cls, inner, tag, tagC) => `<g class="${cls}"><path d="M0,0 L-96,128 M0,0 L96,128" stroke="#8a7a5a" stroke-width="3"/><circle r="9" fill="#c9952e" stroke="${INK}" stroke-width="3.5"/>
    <g class="load" transform="translate(0,126)">${inner}</g>
    <path d="M-120,126 Q0,176 120,126 Z" fill="url(#bal9g)" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
    <text x="0" y="214" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="52" fill="${tagC}" stroke="#fff" stroke-width="8" paint-order="stroke">${tag}</text></g>`;
  const slip = slippersSVG(150).replace('<svg ', '<svg x="-75" y="-110" ');
  const wrap = ins(c.c, `<div class="bal9w"><svg width="${W}" height="${W * 0.62}" viewBox="-420 -70 840 520" style="overflow:visible">
    <defs><linearGradient id="bal9g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6dc8a"/><stop offset="1" stop-color="#c9952e"/></linearGradient></defs>
    <ellipse cx="0" cy="430" rx="150" ry="16" fill="#000" opacity=".16"/>
    <path d="M-110,430 L110,430 L76,384 L-76,384 Z" fill="url(#bal9g)" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
    <rect x="-14" y="10" width="28" height="380" rx="10" fill="url(#bal9g)" stroke="${INK}" stroke-width="5"/>
    <g class="beam"><rect x="-300" y="-11" width="600" height="22" rx="11" fill="url(#bal9g)" stroke="${INK}" stroke-width="5"/><path d="M-280,-3 L280,-3" stroke="#fff3c4" stroke-width="4" stroke-linecap="round" opacity=".7"/></g>
    ${pan('panL', slip, '฿39', '#2e8fb3')}
    ${pan('panR', box, '฿40', '#e0453b')}
    <circle r="22" fill="#f6e3a8" stroke="${INK}" stroke-width="5"/><circle r="7" fill="${INK}"/>
  </svg></div>`);
  const beam = wrap.querySelector('.beam'), pL = wrap.querySelector('.panL'), pR = wrap.querySelector('.panR');
  const loadR = pR.querySelector('.load'), tagR = pR.querySelector('text');
  const note = ins(c.c, `<div class="vs9n">ค่าส่ง <b>แพงกว่ารองเท้า</b> อีก</div>`);
  return {
    c,
    update(t, tin, tb, tnote) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      // angle: tipped left by the shoes, then swung right when the box lands (damped overshoot)
      const kd = spring(t, tb + 0.28, 9, 3.2);
      const ang = -9 + 18 * kd + (t < tb + 0.28 ? Math.sin(t * 2.4) * 0.8 : 0);
      beam.setAttribute('transform', `rotate(${ang.toFixed(2)})`);
      const a = rad(ang);
      pL.setAttribute('transform', `translate(${(-290 * Math.cos(a)).toFixed(1)},${(-290 * Math.sin(a)).toFixed(1)})`);
      pR.setAttribute('transform', `translate(${(290 * Math.cos(a)).toFixed(1)},${(290 * Math.sin(a)).toFixed(1)})`);
      const kb = Math.pow(prog(t, tb, tb + 0.28), 2), bounce = t > tb + 0.28 ? Math.exp(-(t - tb - 0.28) * 9) * Math.sin((t - tb - 0.28) * 30) * 10 : 0;
      loadR.setAttribute('transform', `translate(0,${(126 - (1 - kb) * 420 - bounce).toFixed(1)}) scale(${(1 + (t > tb + 0.28 ? 0.12 * Math.exp(-(t - tb - 0.28) * 14) : 0)).toFixed(3)},${(1 - (t > tb + 0.28 ? 0.12 * Math.exp(-(t - tb - 0.28) * 14) : 0)).toFixed(3)})`);
      loadR.setAttribute('opacity', t > tb ? 1 : 0); tagR.setAttribute('opacity', fadeIn(t, tb + 0.3, 0.1));
      popSquash(note, t, tnote, '', 10);
    },
  };
}

// 11.11 badge over a slowly turning starburst, with sparks flicking off
function saleBadge2(parent, x, y) {
  const el = html('div', 'sale9b', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const rays = Array.from({ length: 16 }, (_, k) => `<path d="M0,0 L${(Math.cos(k * Math.PI / 8 - 0.09) * 190).toFixed(1)},${(Math.sin(k * Math.PI / 8 - 0.09) * 190).toFixed(1)} L${(Math.cos(k * Math.PI / 8 + 0.09) * 190).toFixed(1)},${(Math.sin(k * Math.PI / 8 + 0.09) * 190).toFixed(1)} Z" fill="${k % 2 ? '#ffd66b' : '#ff9a5a'}"/>`).join('');
  el.innerHTML = `<svg class="burst9" width="380" height="380" viewBox="-190 -190 380 380"><defs><radialGradient id="sb9r"><stop offset=".25" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><mask id="sb9m"><circle r="190" fill="url(#sb9r)"/></mask></defs><g mask="url(#sb9m)">${rays}</g></svg><div class="sale9 in9"><b>11.11</b><small>ลดทั้งแอป</small></div>`;
  const bur = el.querySelector('.burst9'), badge = el.querySelector('.sale9');
  return { el, update(t, t0) { popSquash(badge, t, t0, `rotate(${(-6 + Math.sin(t * 3) * 2).toFixed(2)}deg)`, -20); bur.style.opacity = (0.85 * fadeIn(t, t0 + 0.05, 0.2)).toFixed(3); bur.style.transform = `rotate(${(t * 18).toFixed(1)}deg) scale(${(0.6 + 0.4 * spring(t, t0, 10, 5)).toFixed(3)})`; } };
}

// cart chip whose cart jumps each time an item flies in
function cartChip2(parent, x, y, label) {
  const ch = cartChip(parent, x, y, label);
  const ic = ch.el.querySelector('.ic5');
  const fly = html('span', 'fly9', ch.el);
  fly.innerHTML = prodSVG('cream', 46);
  const kinds = ['cream', 'tee', 'buds', 'bag', 'lip', 'shoe'];
  let last = -1;
  return {
    el: ch.el,
    update(t, t0, v, speed) {
      ch.update(t, t0, v, speed);
      const n = Math.floor(v);
      if (n !== last) { fly.innerHTML = prodSVG(kinds[(n + 6) % 6], 46); last = n; }
      const u = v - n;   // the next item arcs in from above-right over each step of the count
      const on = t > t0 && v < 12 && speed > 0.05;
      fly.style.opacity = on ? (Math.sin(Math.PI * u) * 1).toFixed(2) : 0;
      fly.style.transform = `translate(${(80 - 80 * u).toFixed(1)}px, ${(-90 + 120 * u - 60 * Math.sin(Math.PI * u)).toFixed(1)}px) rotate(${(u * 200).toFixed(0)}deg) scale(${(1 - 0.5 * u).toFixed(2)})`;
      ic.style.transform = `translateY(${(-8 * Math.max(0, Math.sin(Math.PI * Math.min(1, u * 3 - 2)))).toFixed(1)}px) rotate(${(-6 * Math.max(0, Math.sin(Math.PI * Math.min(1, u * 3 - 2)))).toFixed(1)}deg)`;
    },
  };
}

// LINE banner that buzzes as it lands, with a ping ripple behind mom's avatar
function lineBanner2(parent, y, msgHTML) {
  const el = lineBanner(parent, y, msgHTML);
  const av = el.querySelector('.av');
  const rip = html('i', 'rip9', av), rip2 = html('i', 'rip9', av);
  return {
    el,
    update(t, t0, tMsg) {
      const kn = spring(t, t0, 13, 6), buzz = t > t0 && t < t0 + 0.5 ? Math.sin((t - t0) * 70) * 6 * (1 - (t - t0) / 0.5) : 0;
      el.style.opacity = fadeIn(t, t0, 0.12);
      el.style.transform = `translateY(${((1 - kn) * -220).toFixed(1)}px) translateX(${buzz.toFixed(1)}px) rotate(${(buzz * 0.15).toFixed(2)}deg)`;
      el.querySelector('.msg').style.opacity = fadeIn(t, tMsg, 0.15);
      [rip, rip2].forEach((r, i) => { const k = ((t - t0 - 0.1 - i * 0.45) % 0.9) / 0.9; const on = t > t0 + 0.1 + i * 0.45 && t < t0 + 2.4; r.style.opacity = on ? (0.6 * (1 - k)).toFixed(2) : 0; r.style.transform = `scale(${(1 + 0.8 * k).toFixed(3)})`; });
    },
  };
}

// a red marker circle drawn around an element (stroke animates on)
function markerCircle(parent, w, h) {
  const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(s, { width: w, height: h, viewBox: `0 0 ${w} ${h}`, class: 'mark9' });
  const p = svg('path', { d: `M${w * 0.12},${h * 0.3} C${w * 0.3},${-h * 0.05} ${w * 0.95},${h * 0.02} ${w * 0.97},${h * 0.5} C${w * 0.98},${h * 0.95} ${w * 0.2},${h * 1.02} ${w * 0.05},${h * 0.62} C${-w * 0.02},${h * 0.38} ${w * 0.2},${h * 0.12} ${w * 0.4},${h * 0.08}`, fill: 'none', stroke: '#e0453b', 'stroke-width': 6, 'stroke-linecap': 'round' }, s);
  parent.appendChild(s);
  const L = 2.6 * (w + h);
  p.setAttribute('stroke-dasharray', L); p.setAttribute('stroke-dashoffset', L);
  return t0 => t => p.setAttribute('stroke-dashoffset', (L * (1 - ease.outCubic(prog(t, t0, t0 + 0.45)))).toFixed(1));
}
