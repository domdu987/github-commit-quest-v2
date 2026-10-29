// "9 ผ้าพันคอ" UI: scarf icon, the พ.ศ. year odometer, a counter of nine little scarves popping in, the เชียงราย → กรุงเทพฯ
// parcel route, a hot/cold thermometer odometer, the "ใช้ไปแล้ว 0 ครั้ง" chip, the late-parcel calendar with a red marker,
// ยาย's shaky handwritten note, the progress ring of the tenth scarf, and the glowing "?".

function scarfIcon(w, c = '#e0453b', o = {}) {
  const st = o.stripe || '#f6efe2', id = 'si' + c.slice(1) + (o.id || '');
  return `<svg width="${w}" height="${w}" viewBox="-60 -60 120 120" style="overflow:visible"><defs><pattern id="${id}" width="9" height="7" patternUnits="userSpaceOnUse"><rect width="9" height="7" fill="${c}"/><path d="M0,1 L2.25,5.5 L4.5,1 L6.75,5.5 L9,1" fill="none" stroke="${shade(c, -28)}" stroke-width="1.3"/></pattern></defs>
  <path d="M-6,-8 L-26,46 L-6,52 L12,-2 Z" fill="url(#${id})" stroke="${INK}" stroke-width="4.5" stroke-linejoin="round"/>
  <path d="M-21,32 L-3,38" stroke="${st}" stroke-width="6"/>
  <path d="M-25,48 l-4,10 M-17,51 l-3,10 M-9,53 l-2,10" stroke="${shade(c, -15)}" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M-44,-26 C-46,-50 46,-50 44,-26 C42,-6 -42,-6 -44,-26 Z M-24,-28 C-22,-38 22,-38 24,-28 C22,-20 -22,-20 -24,-28 Z" fill="url(#${id})" fill-rule="evenodd" stroke="${INK}" stroke-width="4.5"/>
  <path d="M2,-14 L8,52 L28,50 L22,-14 Z" fill="url(#${id})" stroke="${INK}" stroke-width="4.5" stroke-linejoin="round"/>
  <path d="M5,30 L25,29" stroke="${st}" stroke-width="6"/>
  <path d="M10,53 l0,11 M17,52 l1,11 M24,51 l2,11" stroke="${shade(c, -15)}" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M-32,-38 Q-10,-46 12,-42" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".5"/></svg>`;
}
// year odometer chip
function yearChip12(parent, x, y, label) {
  const el = html('div', 'chip big yr12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="ic5">${scarfIcon(52)}</span><span>${label}</span><b class="o12"></b>`;
  const od = new Odometer(el.querySelector('.o12'), 4);
  return { el, update(t, t0, v, speed) { popSquash(el, t, t0); od.set(v, speed); } };
}
// nine little scarves popping into a row as the years go by; n: how many shown (float)
function scarfRow12(parent, x, y) {
  const el = html('div', 'srow12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="srl12">ผ้าพันคอจากยาย <b class="srn12">0</b> <small>ผืน</small></div><div class="srs12">${SCARF.map(c => `<span>${scarfIcon(64, c)}</span>`).join('')}</div>`;
  const sp = [...el.querySelectorAll('.srs12 span')], num = el.querySelector('.srn12');
  return {
    el,
    update(t, t0, n, nT = []) {
      enter3d(el, t, t0, 'flipDown');
      num.textContent = Math.min(9, Math.floor(n));
      sp.forEach((s, i) => { const on = n >= i + 1, k = on ? spring(t, nT[i] ?? -9, 16, 6.5) : 0; s.style.opacity = on ? 1 : 0.18; s.style.transform = on ? `scale(${Math.max(0.2, k).toFixed(3)}) rotate(${((1 - Math.min(1, k)) * -30).toFixed(1)}deg)` : 'scale(.7)'; s.style.filter = on ? 'none' : 'grayscale(1)'; });
    },
  };
}
// route card: เชียงราย → กรุงเทพฯ with a parcel flying along the dotted path
function routeCard12(parent, x, y) {
  const el = html('div', 'card route12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl"><span class="ic5">${scarfIcon(44)}</span>ส่งมาทุกหน้าหนาว</div><svg class="rt12" width="560" height="170" viewBox="0 0 560 170">
   <path class="rp12" d="M70,110 C190,10 370,10 490,110" fill="none" stroke="#c9b9a6" stroke-width="7" stroke-dasharray="4 14" stroke-linecap="round"/>
   <g transform="translate(70,118)"><path d="M-46,30 L-14,-24 L4,4 L18,-14 L46,30 Z" fill="#7fb069" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M-22,-10 L-14,-24 L-6,-10 Z" fill="#fff"/></g>
   <g transform="translate(490,118)"><rect x="-44" y="-30" width="22" height="60" fill="#8a7a9a" stroke="${INK}" stroke-width="3.5"/><rect x="-18" y="-50" width="26" height="80" fill="#a89ab8" stroke="${INK}" stroke-width="3.5"/><rect x="12" y="-20" width="30" height="50" fill="#8a7a9a" stroke="${INK}" stroke-width="3.5"/></g>
   <g class="pc12"><rect x="-20" y="-18" width="40" height="32" rx="4" fill="#c99a5a" stroke="${INK}" stroke-width="3.5"/><path d="M0,-18 L0,14" stroke="#e8d2a0" stroke-width="5"/></g></svg>
   <div class="rlb12"><span>เชียงราย</span><b>785 กม.</b><span>กรุงเทพฯ</span></div>`;
  const pc = el.querySelector('.pc12');
  const P = u => { const a = [70, 110], b = [190, 10], c = [370, 10], d = [490, 110], m = 1 - u; return [m * m * m * a[0] + 3 * m * m * u * b[0] + 3 * m * u * u * c[0] + u * u * u * d[0], m * m * m * a[1] + 3 * m * m * u * b[1] + 3 * m * u * u * c[1] + u * u * u * d[1]]; };
  return { el, update(t, t0, u) { enter3d(el, t, t0, 'flipDown'); const [px, py] = P(clamp(u)); pc.setAttribute('transform', `translate(${px.toFixed(1)},${py.toFixed(1)}) rotate(${(Math.sin(t * 9) * 8).toFixed(1)})`); pc.style.opacity = u > 0 && u < 1 ? 1 : 0.0; } };
}
// thermometer chip: hot (sun) or cold (snowflake), with an odometer for the degrees
function tempChip12(parent, x, y, hot) {
  const el = html('div', 'chip big tp12 ' + (hot ? 'hot' : 'cold'), parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const icon = hot
    ? `<svg width="58" height="58" viewBox="-30 -30 60 60"><g class="ray12">${Array.from({ length: 8 }, (_, k) => `<path d="M0,-26 L0,-19" stroke="#f2a03a" stroke-width="5" stroke-linecap="round" transform="rotate(${k * 45})"/>`).join('')}</g><circle r="14" fill="#f9c840" stroke="${INK}" stroke-width="3.5"/></svg>`
    : `<svg width="58" height="58" viewBox="-30 -30 60 60"><g class="ray12">${[0, 60, 120].map(a => `<path d="M0,-24 L0,24 M-7,-17 L0,-11 L7,-17 M-7,17 L0,11 L7,17" fill="none" stroke="#5aa8e0" stroke-width="4" stroke-linecap="round" transform="rotate(${a})"/>`).join('')}</g></svg>`;
  el.innerHTML = `<span class="ic5">${icon}</span><span>${hot ? 'กรุงเทพฯ' : 'เชียงราย'}</span><b class="o12"></b><b class="deg12">°C</b>`;
  const od = new Odometer(el.querySelector('.o12'), 2), ray = el.querySelector('.ray12');
  return { el, update(t, t0, v, speed) { popSquash(el, t, t0, '', -10); od.set(v, speed); od.cols[0].col.style.display = v < 9.95 ? 'none' : ''; ray.setAttribute('transform', `rotate(${(t * (hot ? 40 : 20)).toFixed(1)})`); } };
}
// "ใช้ไปแล้ว 0 ครั้ง"
function usedChip12(parent, x, y) {
  const el = html('div', 'chip big used12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="ic5">${scarfIcon(50, '#8a5fc8')}</span><span>ใช้ไปแล้ว</span><b class="z12">0</b><span>ครั้ง</span>`;
  const z = el.querySelector('.z12');
  return { el, update(t, t0) { popSquash(el, t, t0, '', -10); const x = t - t0 - 0.35; z.style.transform = x > 0 ? `rotate(${(Math.sin(x * 30) * 12 * Math.exp(-x * 3)).toFixed(1)}deg) scale(${(1 + 0.25 * Math.exp(-x * 4)).toFixed(3)})` : 'none'; } };
}
// the late parcel: ทุกปี ต้น พ.ย. ✓ vs ปีนี้ 18 ธ.ค. (circled in red)
function lateCard12(parent, x, y) {
  const el = html('div', 'card late12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl"><span class="ic5"><svg width="44" height="44" viewBox="-24 -24 48 48"><rect x="-20" y="-16" width="40" height="36" rx="5" fill="#fbf7ef" stroke="${INK}" stroke-width="3.5"/><rect x="-20" y="-16" width="40" height="11" fill="#c8343c"/><path d="M-11,-22 L-11,-12 M11,-22 L11,-12" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/></svg></span>กล่องจากยาย</div>
   <div class="lr12"><span>ทุกปี</span><b>ต้น พ.ย.</b><i class="ok12">✓</i></div>
   <div class="lr12 now12"><span>ปีนี้</span><b class="mk12">18 ธ.ค.<svg class="mc12" width="210" height="84" viewBox="0 0 210 84"><path d="M30,10 C120,-6 200,20 196,46 C192,74 60,82 16,58 C-8,44 6,14 60,8" fill="none" stroke="#e0453b" stroke-width="6" stroke-linecap="round"/></svg></b><i class="late12">ช้า</i></div>`;
  const mc = el.querySelector('.mc12 path'), late = el.querySelector('.late12');
  const L = 560; mc.style.strokeDasharray = L;
  return { el, update(t, t0) { enter3d(el, t, t0, 'swingLeft'); mc.style.strokeDashoffset = (L * (1 - ease.outCubic(prog(t, t0 + 0.5, t0 + 1.1)))).toFixed(1); popSquash(late, t, t0 + 1.0, '', 14); } };
}
// ยาย's note: shaky handwriting revealed letter by letter
function noteCard12(parent, x, y, lines) {
  const el = html('div', 'note12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const r = rng(91), chars = [];
  lines.forEach(line => {
    const ln = html('div', 'nl12', el);
    for (const seg of segTH.segment(line)) { const s = html('span', 'nc12', ln, seg.segment); s._r = (r() - 0.5) * 7; s._y = (r() - 0.5) * 5; chars.push(s); }
  });
  html('div', 'nh12', el).innerHTML = `<svg width="70" height="60" viewBox="-35 -32 70 60"><path d="${heartPathT(0, 0, 22)}" fill="none" stroke="#c8343c" stroke-width="4" stroke-linecap="round"/></svg>`;
  const heart = el.querySelector('.nh12');
  return {
    el,
    update(t, t0, t1) {
      const k = spring(t, t0, 12, 6.5);
      el.style.opacity = fadeIn(t, t0, 0.15);
      el.style.transform = `translateY(${((1 - k) * 60).toFixed(1)}px) rotate(${(-3 + Math.sin(t * 0.9) * 0.6).toFixed(2)}deg)`;
      const n = chars.length;
      chars.forEach((c, i) => { const ti = lerp(t0 + 0.25, t1, i / n), on = t > ti; c.style.opacity = on ? 1 : 0; const sh = Math.sin(t * 13 + i) * 0.8; c.style.transform = `translateY(${(c._y + sh).toFixed(1)}px) rotate(${(c._r + sh).toFixed(1)}deg)`; });
      heart.style.opacity = fadeIn(t, t1 + 0.1, 0.2); heart.style.transform = `scale(${Math.max(0.01, spring(t, t1 + 0.1, 14, 6)).toFixed(3)})`;
    },
  };
}
// progress ring for the tenth scarf
function progress12(parent, x, y) {
  const el = html('div', 'chip big pg12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="70" height="70" viewBox="-35 -35 70 70"><circle r="27" fill="none" stroke="#e8e0d4" stroke-width="8"/><circle class="pr12" r="27" fill="none" stroke="${SCARF10}" stroke-width="8" stroke-linecap="round" transform="rotate(-90)"/><g class="pck12" opacity="0"><path d="M-12,1 L-3,10 L13,-9" fill="none" stroke="#2f9e5b" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g></svg><span>ผืนที่</span><b class="p10">10</b><small class="pp12">0%</small>`;
  const ring = el.querySelector('.pr12'), ck = el.querySelector('.pck12'), pp = el.querySelector('.pp12');
  const C = 2 * Math.PI * 27; ring.style.strokeDasharray = C;
  return { el, update(t, t0, k) { popSquash(el, t, t0, '', -10); ring.style.strokeDashoffset = (C * (1 - clamp(k))).toFixed(1); ck.setAttribute('opacity', k >= 1 ? 1 : 0); pp.textContent = k >= 1 ? 'เสร็จ!' : `${Math.round(clamp(k) * 100)}%`; } };
}
// the glowing "?"
function glowQ(parent, x, y) {
  const el = html('div', 'wq10 gq12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<b>?</b>${Array.from({ length: 5 }, () => '<i></i>').join('')}`;
  const sp = [...el.querySelectorAll('i')];
  return { el, update(t, t0) { popSquash(el, t, t0, `rotate(${(Math.sin(t * 2.4) * 7).toFixed(1)}deg)`, 16); sp.forEach((s, i) => { const a = t * 1.6 + i * 1.257; s.style.transform = `translate(${(Math.cos(a) * 90).toFixed(1)}px, ${(Math.sin(a) * 60).toFixed(1)}px) scale(${(0.6 + 0.4 * Math.sin(t * 5 + i)).toFixed(2)})`; }); } };
}
// four-point sparkles (world); update(cx, cy, k, t)
function sparkles(parent, n, seed, col = '#fff6dc') {
  const r = rng(seed);
  const ss = Array.from({ length: n }, () => ({ a: r() * Math.PI * 2, d: 60 + r() * 70, ph: r() * 6, s: 8 + r() * 10, el: svg('path', { d: fourStar(1), fill: col, stroke: '#e0a12c', 'stroke-width': 0.08 }, parent) }));
  return (cx, cy, k, t) => ss.forEach(s => {
    const tw = Math.max(0, Math.sin(t * 5 + s.ph));
    s.el.setAttribute('transform', `translate(${(cx + Math.cos(s.a + t * 0.6) * s.d).toFixed(1)},${(cy + Math.sin(s.a + t * 0.6) * s.d * 0.8).toFixed(1)}) scale(${(s.s * (0.4 + 0.6 * tw) * clamp(k)).toFixed(2)})`);
    s.el.setAttribute('opacity', (clamp(k) * (0.4 + 0.6 * tw)).toFixed(2));
  });
}
// tear drops of laughter (world): update(x, y, k, t)
// o.drift: run every drop the same way (+1 / -1 in world x) instead of splitting both ways — for a 3/4 face, so a
// stream never runs across the nose; o.spread scales the start jitter
function tears(parent, seed, o = {}) {
  const sp = o.spread ?? 1, dr = o.drift ?? 0;
  const r = rng(seed), ds = Array.from({ length: o.n ?? 4 }, () => ({ ph: r(), dx: (r() - 0.5) * 20 * sp, el: svg('path', { fill: '#bfe6ff', stroke: INK, 'stroke-width': 2 }, parent) }));
  return (x, y, k, t) => ds.forEach((d, i) => {
    const u = ((t * 1.3 + d.ph) % 1), px = x + d.dx + (dr ? dr * 12 : (i % 2 ? 14 : -14)) * u, py = y + 50 * u * u, s = 6;
    d.el.setAttribute('d', `M${px.toFixed(1)},${(py - s * 2).toFixed(1)} C${(px + s).toFixed(1)},${(py - s * 0.4).toFixed(1)} ${(px + s).toFixed(1)},${(py + s).toFixed(1)} ${px.toFixed(1)},${(py + s).toFixed(1)} C${(px - s).toFixed(1)},${(py + s).toFixed(1)} ${(px - s).toFixed(1)},${(py - s * 0.4).toFixed(1)} ${px.toFixed(1)},${(py - s * 2).toFixed(1)} Z`);
    d.el.setAttribute('opacity', (clamp(k) * Math.sin(Math.PI * u)).toFixed(2));
  });
}
