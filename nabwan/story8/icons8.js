// "312 ชามที่ไม่มีผักชี" UI: bowl icons, a "said love: 0 times" chip, his photo-only profile, other couples' sweet posts,
// the first-date polaroid, the 3 years × 52 weeks × 2 bowls card with a filling grid, and the two kinds of "I love you".

// noodle bowl icon (svg string); crossed = a red "no coriander" mark on a leaf beside it
function bowlSVG(w, o = {}) {
  const leaf = (x, y, s, a) => `<g transform="translate(${x},${y}) rotate(${a}) scale(${s})"><path d="M0,4 C-9,6 -13,-4 -6,-7 C-6,-13 4,-14 5,-7 C12,-6 11,5 0,4 Z" fill="#4fae5a" stroke="#2f6b3a" stroke-width="1.6"/></g>`;
  return `<svg width="${w}" height="${w}" viewBox="-60 -60 120 120" style="overflow:visible">
  ${o.steam ? `<path class="stm8" d="M-20,-30 q-8,-12 0,-24 M0,-34 q-8,-12 0,-24 M20,-30 q-8,-12 0,-24" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".75"/>` : ''}
  <ellipse cx="0" cy="38" rx="40" ry="6" fill="#000" opacity=".18"/>
  <path d="M-52,-6 Q-48,34 -18,38 L18,38 Q48,34 52,-6 Z" fill="#fbf8f1" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M-49,6 Q0,15 49,6" fill="none" stroke="#4a7bd8" stroke-width="4"/>
  <ellipse cx="0" cy="-6" rx="52" ry="13" fill="#fbf8f1" stroke="${INK}" stroke-width="4"/>
  <ellipse cx="0" cy="-5" rx="44" ry="9" fill="#d9a35e"/>
  <path d="M-30,-5 q6,-5 12,0 t12,0 M2,-4 q6,-5 12,0 t12,0" fill="none" stroke="#f6ead0" stroke-width="3.5" stroke-linecap="round"/>
  ${o.leaves ? leaf(-22, -8, 1, 20) + leaf(8, -7, 0.9, -40) + leaf(26, -4, 0.8, 70) : ''}
  ${o.crossed ? `<g transform="translate(40,-34)"><circle r="20" fill="#fff" stroke="#e0453b" stroke-width="5"/>${leaf(0, 0, 1.2, 0)}<path d="M-13,13 L13,-13" stroke="#e0453b" stroke-width="5" stroke-linecap="round"/></g>` : ''}</svg>`;
}
const heartSVG = (w, c = '#f04f7f') => `<svg width="${w}" height="${w}" viewBox="-20 -20 40 40"><path d="${heartPathT(0, 0, 13)}" fill="${c}" stroke="#fff" stroke-width="3"/></svg>`;

// "ปั้นพูดว่ารัก 0 ครั้ง": a speech bubble with รัก struck through
function saidLoveChip(parent, x, y, label = 'ปั้นพูดคำว่ารัก') {
  const el = html('div', 'chip big love8', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="ic5"><svg width="64" height="54" viewBox="-34 -30 68 58"><path d="M-28,-22 Q-28,-26 -24,-26 L24,-26 Q28,-26 28,-22 L28,8 Q28,12 24,12 L-6,12 L-16,24 L-14,12 L-24,12 Q-28,12 -28,8 Z" fill="#fff" stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"/><text x="0" y="1" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="20" fill="#f04f7f">รัก</text><path class="slash8" d="M-24,-20 L24,8" stroke="#e0453b" stroke-width="5" stroke-linecap="round"/></svg></span><span>${label} <b class="n8">0</b> ครั้ง</span>`;
  const slash = el.querySelector('.slash8');
  return { el, update(t, t0, tslash) { popSquash(el, t, t0); const k = ease.outCubic(prog(t, tslash, tslash + 0.25)); slash.setAttribute('stroke-dasharray', '60'); slash.setAttribute('stroke-dashoffset', (60 * (1 - k)).toFixed(1)); } };
}

// big rolling "312 ครั้ง?" card for the hook
function loveCounter(parent, x, y) {
  const c = card7(parent, 'card cnt8 pink', x, y);
  ins(c.c, `<div class="lbl"><span class="ic5">${heartSVG(40)}</span>เขาบอกรักไปแล้ว</div>`);
  const row = ins(c.c, `<div class="num"><span class="o8"></span><small>ครั้ง</small><span class="q8">?</span></div>`);
  const od = new Odometer(row.querySelector('.o8'), 3);
  const q = row.querySelector('.q8');
  return {
    c,
    update(t, tin, t0, t1, tq) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      const r = rollValue(t, t0, t1, 0, 312); od.set(r.v, r.speed);
      popSquash(q, t, tq, '', 20);
    },
  };
}

// a social post card: who, photo (svg string), caption, likes
function postCard8(parent, x, y, w, who, avHTML, photo, caption, likes) {
  const el = html('div', 'post8', parent); Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  el.innerHTML = `<div class="ph8"><span class="pav8">${avHTML}</span><b>${who}</b><i>⋯</i></div><div class="pp8">${photo}</div><div class="pl8"><span class="ic5">${heartSVG(38)}</span><b>${likes}</b> ถูกใจ</div><div class="pc8">${caption}</div>`;
  return el;
}
// a couple avatar (two small faces) for other people's posts
function coupleAv(n) {
  return `<svg width="${n}" height="${n}" viewBox="-48 -48 96 96"><circle r="48" fill="#ffe2d6"/>
  <circle cx="-16" cy="2" r="20" fill="#f0c09a" stroke="${INK}" stroke-width="2.5"/><path d="M-36,0 C-38,-26 4,-30 4,-4 Q-14,-14 -36,0 Z" fill="#3a2622"/>
  <circle cx="17" cy="6" r="19" fill="#c98d62" stroke="${INK}" stroke-width="2.5"/><path d="M-2,2 C-2,-24 36,-24 36,2 Q18,-12 -2,2 Z" fill="#1f1a1c"/>
  ${[-22, -10, 11, 23].map(ex => `<circle cx="${ex}" cy="${ex < 0 ? 4 : 8}" r="2.4" fill="${INK}"/>`).join('')}</svg>`;
}
// anniversary photo: balloons, cake and a big heart
const anniversaryPhoto = (w, h) => `<svg width="${w}" height="${h}" viewBox="0 0 400 260"><rect width="400" height="260" fill="#ffe3ec"/>
  ${[[70, 70, '#f04f7f'], [120, 50, '#ffd166'], [300, 60, '#7fd6ff'], [345, 85, '#f07aa8']].map(([bx, by, c]) => `<path d="M${bx},${by + 34} q6,40 -6,80" stroke="#c9a" stroke-width="2" fill="none"/><ellipse cx="${bx}" cy="${by}" rx="26" ry="32" fill="${c}" stroke="${INK}" stroke-width="3"/>`).join('')}
  <path d="${heartPathT(200, 120, 60)}" fill="#f04f7f" stroke="${INK}" stroke-width="4"/><text x="200" y="128" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#fff">3 ปี</text>
  <rect x="150" y="190" width="100" height="44" rx="6" fill="#f6c6d4" stroke="${INK}" stroke-width="3"/><rect x="196" y="168" width="8" height="24" fill="#7fc0f0" stroke="${INK}" stroke-width="2"/></svg>`;
// his photo-only profile: noodles, cat, game pad… and zero couple photos
function profileGrid8(parent, x, y, w) {
  const c = card7(parent, 'card prof8', x, y, w);
  const tiles = [
    `<rect width="100" height="100" fill="#ffe9c4"/><g transform="translate(50,56) scale(.7)">${bowlSVG(100).replace(/^<svg[^>]*>|<\/svg>$/g, '')}</g>`,
    `<rect width="100" height="100" fill="#f2c97a"/><path d="M28,84 C24,50 34,40 50,40 C66,40 76,50 72,84 Z M32,46 L36,26 L46,40 Z M54,40 L64,26 L68,46 Z" fill="#fbf7ef" stroke="${INK}" stroke-width="3"/>`,
    `<rect width="100" height="100" fill="#3a4478"/><path d="M22,40 h56 a14,14 0 0 1 0,28 l-9,8 h-38 l-9,-8 a14,14 0 0 1 0,-28 Z" fill="#7a8ad8" stroke="#fff" stroke-width="3"/>`,
    `<rect width="100" height="100" fill="#9fd0f0"/><circle cx="70" cy="30" r="14" fill="#fff3c4"/><path d="M0,80 L30,56 L52,72 L74,50 L100,74 L100,100 L0,100 Z" fill="#5fa27f"/>`,
    `<rect width="100" height="100" fill="#ffd9c4"/><circle cx="50" cy="52" r="26" fill="#fbf8f1" stroke="${INK}" stroke-width="3"/><circle cx="50" cy="52" r="16" fill="#e8a04a"/>`,
    `<rect width="100" height="100" fill="#f6efe2"/><path d="M30,78 C26,50 36,42 50,42 C64,42 74,50 70,78 Z M34,48 L38,30 L47,42 Z M53,42 L62,30 L66,48 Z" fill="#555" stroke="${INK}" stroke-width="3"/>`,
  ];
  ins(c.c, `<div class="pg8h"><span class="pav8">${panAv(84)}</span><div><b>pan.jj</b><small>โพสต์ 48 · ผู้ติดตาม 210</small></div></div>`);
  const grid = ins(c.c, `<div class="pg8">${tiles.map(tl => `<svg viewBox="0 0 100 100">${tl}</svg>`).join('')}</div>`);
  const badge = ins(c.c, `<div class="pg8b">รูปคู่ <b>0</b></div>`);
  return { c, update(t, tin, tbadge) { enter3d(c.c, t, tin, 'swingRight'); shine(c.sh, t, tin + 0.5); [...grid.children].forEach((s, i) => { const k = spring(t, tin + 0.15 + i * 0.06, 16, 6); s.style.transform = `scale(${Math.max(0.01, k).toFixed(3)})`; }); popSquash(badge, t, tbadge, '', 16); } };
}

// the first-date polaroid: the same noodle shop, younger them, and her bubble "ไม่กินผักชีนะ"
function firstDatePolaroid(parent, x, y, w) {
  const el = html('div', 'pol8', parent); Object.assign(el.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
  const ph = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); setA(ph, { viewBox: '0 0 300 240', width: w - 28, height: (w - 28) * 0.8 });
  svg('rect', { width: 300, height: 240, fill: '#e9c79a' }, ph);
  svg('rect', { y: 150, width: 300, height: 90, fill: '#c9d2dc' }, ph);
  faceFront8(ph, 92, 104, 46, 'min', { smile: 0.8 });
  faceFront8(ph, 212, 108, 44, 'pan', { smile: 0.5 });
  const b = svg('g', { transform: 'translate(150,196) scale(.9)' }, ph); b.innerHTML = bowlSVG(110, { leaves: true }).replace(/^<svg[^>]*>|<\/svg>$/g, '');
  el.appendChild(ph);
  html('div', 'pol8t', el, 'เดทแรก · 3 ปีก่อน');
  const bub = html('div', 'bub8', el); bub.innerHTML = `ไม่กินผักชีนะ <span class="ic5">${bowlSVG(50, { crossed: true }).replace('width="50" height="50"', 'width="44" height="44"')}</span>`;
  return {
    el,
    update(t, tin, tbub) {
      const k = spring(t, tin, 13, 6);
      el.style.opacity = fadeIn(t, tin, 0.12);
      el.style.transform = `translateY(${((1 - k) * -120).toFixed(1)}px) rotate(${(-6 + (1 - k) * -14).toFixed(2)}deg)`;
      popSquash(bub, t, tbub, '', -14);
    },
  };
}

// 3 ปี × 52 สัปดาห์ × 2 ชาม = 312 ชาม, with a grid of 312 little bowls filling up
function bowlMath8(parent, x, y, w) {
  const c = card7(parent, 'card math8', x, y, w);
  ins(c.c, `<div class="lbl"><span class="ic5">${bowlSVG(46)}</span>ชามที่ไม่มีผักชี</div>`);
  const eq = ins(c.c, `<div class="eq8"><span class="t8"><b>3</b><small>ปี</small></span><i>×</i><span class="t8"><b>52</b><small>สัปดาห์</small></span><i>×</i><span class="t8"><b>2</b><small>ชาม</small></span><i>=</i><span class="t8 hot"><b class="r8"></b><small>ชาม</small></span></div>`);
  const terms = [...eq.querySelectorAll('.t8, i')];
  const od = new Odometer(eq.querySelector('.r8'), 3);
  const grid = ins(c.c, `<div class="bg8">${Array.from({ length: 312 }, () => '<i></i>').join('')}</div>`);
  const cells = [...grid.children];
  return {
    c,
    update(t, tin, tterms, t0, t1) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      terms.forEach((e, i) => { const tt = tterms[Math.min(i >> 1, tterms.length - 1)] + (i % 2) * 0.08; e.style.opacity = fadeIn(t, tt, 0.1); e.style.transform = `scale(${Math.max(0.01, spring(t, tt, 16, 6)).toFixed(3)})`; });
      const r = rollValue(t, t0, t1, 0, 312); od.set(r.v, r.speed);
      const n = Math.round(r.v);
      cells.forEach((e, i) => e.classList.toggle('on', i < n));
    },
  };
}

// two ways to say it: words vs remembering what you don't like
function twoLoves8(parent, y) {
  const el = html('div', 'two8', parent); el.style.top = y + 'px';
  el.innerHTML = `<div class="tc8"><small>บางคน</small><span class="ic5"><svg width="96" height="80" viewBox="-40 -34 80 68"><path d="M-34,-26 Q-34,-30 -30,-30 L30,-30 Q34,-30 34,-26 L34,10 Q34,14 30,14 L-6,14 L-18,28 L-15,14 L-30,14 Q-34,14 -34,10 Z" fill="#fff" stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"/><text x="0" y="0" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#f04f7f">รักนะ</text></svg></span><b>บอกรักด้วยคำพูด</b></div>
  <div class="tc8 hot"><small>บางคน</small><span class="ic5">${bowlSVG(96, { crossed: true })}</span><b>จำว่าเราไม่ชอบอะไร</b></div>`;
  const [a, b] = el.children;
  return { el, update(t, ta, tb) { enter3d(a, t, ta, 'swingLeft'); enter3d(b, t, tb, 'swingRight'); } };
}
