// "15 ปีใหม่" graphics: a tour-bus icon, the "31 ธ.ค." calendar that flips through fifteen New Year's Eves (B.E. year
// odometer, a bus driving along the years), the LINE banner from แม่ at midnight, the secret bus ticket (seat 1A circled
// in red, an "แอบจอง" stamp, a perforated stub), the midnight clock, PA sound waves, confetti, the glowing "?", tears.

// a double-decker bus icon (burgundy, gold stripe), facing left
function busIcon13(w = 120, c = '#8e2a3c') {
  return `<svg width="${w}" height="${(w * 0.62).toFixed(0)}" viewBox="0 0 200 124"><rect x="8" y="12" width="184" height="92" rx="18" fill="${c}" stroke="${INK}" stroke-width="6"/>
  <path d="M8,62 L192,62 L192,72 L8,72 Z" fill="#e8b13a"/><rect x="16" y="20" width="34" height="34" rx="8" fill="#ffd59a" stroke="${INK}" stroke-width="4"/>
  ${[0, 1, 2, 3].map(k => `<rect x="${60 + k * 32}" y="22" width="26" height="30" rx="5" fill="#ffd59a" stroke="${INK}" stroke-width="3.5"/>`).join('')}
  <rect x="16" y="78" width="16" height="12" rx="4" fill="#fff6dc" stroke="${INK}" stroke-width="3"/>
  <circle cx="52" cy="106" r="15" fill="#2a2228" stroke="${INK}" stroke-width="5"/><circle cx="150" cy="106" r="15" fill="#2a2228" stroke="${INK}" stroke-width="5"/>
  <circle cx="52" cy="106" r="6" fill="#b8b2aa"/><circle cx="150" cy="106" r="6" fill="#b8b2aa"/></svg>`;
}
const waterIcon13 = (h = 40) => `<svg width="${(h * 0.6).toFixed(0)}" height="${h}" viewBox="-15 -42 30 80"><path d="M-11,-30 L11,-30 L13,-22 L13,30 Q13,36 7,36 L-7,36 Q-13,36 -13,30 L-13,-22 Z" fill="#dff2ff" stroke="${INK}" stroke-width="3"/><rect x="-7" y="-40" width="14" height="11" rx="3" fill="#4a7bd8" stroke="${INK}" stroke-width="2.5"/><rect x="-13" y="-4" width="26" height="18" fill="#4a7bd8"/></svg>`;
const heartIcon13 = (s = 30, c = '#e0577a') => `<svg width="${s}" height="${s}" viewBox="-12 -12 24 24"><path d="${heartPathT(0, 0, 9)}" fill="${c}" stroke="${INK}" stroke-width="2"/></svg>`;

// "31 ธ.ค." calendar card: the B.E. year rolls 2555 → 2569 while a bus drives along fifteen ticks; update(t, t0, t1)
function yearCal13(parent, x, y) {
  const el = html('div', 'card cal13', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl">คืนสิ้นปีของแม่</div><div class="cr13"><div class="pg13"><i>ธ.ค.</i><b>31</b></div>
   <div class="cy13"><span class="yl13">พ.ศ.</span><b class="yo13"></b><span class="yn13">บนถนน <em class="yk13">1</em> ปี</span></div></div>
   <div class="trk13"><svg width="560" height="70" viewBox="0 0 560 70"><path d="M10,52 L550,52" stroke="#d3cbbd" stroke-width="6" stroke-linecap="round"/>
   ${Array.from({ length: 15 }, (_, k) => `<circle class="tk13" cx="${(18 + k * 37).toFixed(1)}" cy="52" r="7" fill="#d3cbbd"/>`).join('')}</svg><span class="bi13">${busIcon13(84)}</span></div><div class="shine"></div>`;
  const od = new Odometer(el.querySelector('.yo13'), 4), tk = [...el.querySelectorAll('.tk13')], bi = el.querySelector('.bi13'), yk = el.querySelector('.yk13'), sh = el.querySelector('.shine'), pg = el.querySelector('.pg13');
  return {
    el, update(t, t0, t1) {
      enter3d(el, t, t0, 'flipDown');
      const k = ease.inOutCubic(prog(t, t0 + 0.35, t1)), n = Math.min(15, 1 + Math.floor(k * 14.999));
      od.set(2555 + (n - 1), 0); yk.textContent = n;
      tk.forEach((c, i) => c.setAttribute('fill', i < n ? '#c8343c' : '#d3cbbd'));
      bi.style.transform = `translate(${(18 + (n - 1 + (k * 14.999 % 1) * (n < 15 ? 1 : 0)) * 37 - 42).toFixed(1)}px, -6px) translateY(${(Math.abs(Math.sin(t * 14)) * -3).toFixed(1)}px)`;
      pg.style.transform = `rotateX(${(n > 1 && n < 15 ? Math.max(0, 1 - ((k * 14.999) % 1) * 4) * -70 : 0).toFixed(1)}deg)`;
      shine(sh, t, t1 + 0.1);
    },
  };
}
// the LINE banner from แม่ at midnight (types out, buzzes with a ripple); update(t, t0, tType)
function lineBanner13(parent, y, msg) {
  const el = html('div', 'notif line13', parent); el.style.top = y + 'px';
  el.innerHTML = `<span class="app">LINE</span><div class="av">${av13('mae', 96)}</div><div style="flex:1"><div class="who">แม่ ${heartIcon13(28)}<small>00:00</small></div><div class="msg"><span class="ty13"></span><span class="ic13">${waterIcon13(40)}</span></div></div>`;
  const ty = el.querySelector('.ty13'), ic = el.querySelector('.ic13');
  const rp = html('div', 'rip13', el);
  return {
    el, update(t, t0, tType) {
      enter3d(el, t, t0, 'drop');
      const n = Math.round(prog(t, tType, tType + 1.0) * msg.length);
      ty.textContent = msg.slice(0, n);
      ic.style.opacity = n >= msg.length ? 1 : 0;
      ic.style.transform = n >= msg.length ? `scale(${(0.6 + 0.4 * spring(t, tType + 1.0, 18, 7)).toFixed(3)})` : 'scale(0.6)';
      const bz = t > t0 && t < t0 + 0.5 ? Math.sin((t - t0) * 70) * 5 * (1 - (t - t0) / 0.5) : 0;
      el.style.marginLeft = bz.toFixed(1) + 'px';
      const rk = ((t - t0) % 1.1) / 1.1;
      rp.style.opacity = t > t0 ? ((1 - rk) * 0.6).toFixed(3) : 0; rp.style.transform = `scale(${(1 + rk * 0.12).toFixed(3)})`;
    },
  };
}
// the secret ticket: route, date, time; seat 1A circled; "แอบจอง" stamp lands; update(t, t0, tCircle, tStamp)
function ticket13(parent, x, y) {
  const el = html('div', 'card tk13c', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="th13">${busIcon13(70)}<b>สายใยทัวร์</b><small>VIP 24 ที่นั่ง</small></div>
   <div class="tr13"><div><i>จาก</i><b>กรุงเทพฯ</b></div><span class="ar13"><svg width="70" height="30" viewBox="0 0 70 30"><path d="M4,15 L56,15 M44,4 L60,15 L44,26" fill="none" stroke="#c8343c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg></span><div><i>ถึง</i><b>อุบลราชธานี</b></div></div>
   <div class="tg13"><div><i>วันที่</i><b>31 ธ.ค. 69</b></div><div><i>ออก</i><b>22:30</b></div><div class="st13"><i>ที่นั่ง</i><b>1A</b>
   <svg class="sc13" width="170" height="120" viewBox="0 0 170 120"><path d="M28,14 C110,-4 168,22 160,62 C152,104 50,112 14,80 C-8,58 8,24 60,12" fill="none" stroke="#e0453b" stroke-width="7" stroke-linecap="round"/></svg></div></div>
   <div class="stp13">แอบจอง</div><div class="perf13"></div><div class="shine"></div>`;
  const sc = el.querySelector('.sc13 path'), stp = el.querySelector('.stp13'), sh = el.querySelector('.shine');
  const L = sc.getTotalLength ? 420 : 420; sc.style.strokeDasharray = L;
  return {
    el, update(t, t0, tCircle, tStamp) {
      enter3d(el, t, t0, 'swingLeft');
      sc.style.strokeDashoffset = (L * (1 - ease.outCubic(prog(t, tCircle, tCircle + 0.45)))).toFixed(1);
      const ks = spring(t, tStamp, 16, 7);
      stp.style.opacity = t > tStamp ? 1 : 0;
      stp.style.transform = `rotate(-14deg) scale(${(2.2 - 1.2 * Math.min(1.1, ks)).toFixed(3)})`;
      shine(sh, t, t0 + 0.3);
    },
  };
}
// midnight clock chip: hh:mm:ss counting from `from` seconds before midnight; at 0 → "00:00:00" + a burst of the chip
function clock13(parent, x, y) {
  const el = html('div', 'chip big clk13', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="54" height="54" viewBox="-27 -27 54 54"><circle r="22" fill="#fbf7ef" stroke="${INK}" stroke-width="4"/><path class="hh13" d="M0,0 L0,-12" stroke="${INK}" stroke-width="4" stroke-linecap="round"/><path class="mm13" d="M0,0 L0,-17" stroke="#c8343c" stroke-width="3" stroke-linecap="round"/></svg><b class="ct13">23:59:57</b><span class="hy13">สวัสดีปีใหม่!</span>`;
  const ct = el.querySelector('.ct13'), hy = el.querySelector('.hy13'), mm = el.querySelector('.mm13');
  return {
    el, update(t, t0, tMid) {
      popSquash(el, t, t0, '', -10);
      const left = Math.max(0, Math.ceil(tMid - t)), s = 60 - left;
      ct.textContent = t < tMid ? `23:59:${String(Math.min(59, s)).padStart(2, '0')}` : '00:00:00';
      ct.style.color = t < tMid ? '#23242f' : '#c8343c';
      mm.setAttribute('transform', `rotate(${(t < tMid ? -6 + (s / 60) * 6 : 0).toFixed(1)})`);
      const kh = spring(t, tMid, 16, 7);
      hy.style.maxWidth = t > tMid ? `${(Math.min(1, kh) * 260).toFixed(0)}px` : '0px';
      hy.style.opacity = t > tMid ? 1 : 0;
      el.style.boxShadow = t > tMid ? `0 0 ${(30 + 16 * Math.sin(t * 6)).toFixed(0)}px rgba(255,200,90,.8), 0 14px 30px rgba(0,0,0,.35)` : '';
    },
  };
}
// sound waves from a mic or ceiling speaker (world): update(x, y, gain, t, dir)
function paWaves13(parent, n = 3) {
  const arcs = Array.from({ length: n }, () => svg('path', { fill: 'none', stroke: '#fff1c4', 'stroke-width': 6, 'stroke-linecap': 'round' }, parent));
  return (x, y, gain, t, dir = 1) => arcs.forEach((a, i) => {
    const k = ((t * 1.6 + i / n) % 1), r = 26 + k * 70;
    a.setAttribute('d', `M${(x + dir * r * Math.cos(-0.7)).toFixed(1)},${(y + r * Math.sin(-0.7)).toFixed(1)} A${r.toFixed(1)},${r.toFixed(1)} 0 0 ${dir > 0 ? 1 : 0} ${(x + dir * r * Math.cos(0.7)).toFixed(1)},${(y + r * Math.sin(0.7)).toFixed(1)}`);
    a.setAttribute('opacity', (gain * (1 - k) * 0.85).toFixed(3));
  });
}
// confetti falling from t0 inside box (world); update(t)
function confetti13(parent, box, n, seed, t0) {
  const r = rng(seed), cols = ['#f2c14e', '#e0453b', '#ff9fc0', '#7fc6a8', '#8fb0ff', '#ffffff'];
  const ps = Array.from({ length: n }, (_, i) => ({ x: box[0] + r() * (box[2] - box[0]), d: r() * 0.8, sp: 260 + r() * 260, sw: 20 + r() * 30, ph: r() * 6, rot: r() * 360, el: svg('rect', { x: -7, y: -4, width: 14, height: 8, rx: 2, fill: cols[i % cols.length] }, parent) }));
  return t => ps.forEach(p => {
    const x = t - t0 - p.d;
    if (x < 0) { p.el.setAttribute('opacity', 0); return; }
    const y = box[1] + x * p.sp, op = y > box[3] ? 0 : 1;
    p.el.setAttribute('opacity', op);
    p.el.setAttribute('transform', `translate(${(p.x + Math.sin(x * 3 + p.ph) * p.sw).toFixed(1)},${y.toFixed(1)}) rotate(${(p.rot + x * 400).toFixed(0)}) scale(1,${Math.cos(x * 8 + p.ph).toFixed(2)})`);
  });
}
// the glowing "?"
function glowQ(parent, x, y) {
  const el = html('div', 'wq10 gq12', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<b>?</b>${Array.from({ length: 5 }, () => '<i></i>').join('')}`;
  const sp = [...el.querySelectorAll('i')];
  return { el, update(t, t0) { popSquash(el, t, t0, `rotate(${(Math.sin(t * 2.4) * 7).toFixed(1)}deg)`, 16); sp.forEach((s, i) => { const a = t * 1.6 + i * 1.257; s.style.transform = `translate(${(Math.cos(a) * 90).toFixed(1)}px, ${(Math.sin(a) * 60).toFixed(1)}px) scale(${(0.6 + 0.4 * Math.sin(t * 5 + i)).toFixed(2)})`; }); } };
}
// tears (world), one stream per eye on the 3/4 face (drift outward): update(x, y, k, t)
function tears(parent, seed, o = {}) {
  const sp = o.spread ?? 1, dr = o.drift ?? 0;
  const r = rng(seed), ds = Array.from({ length: o.n ?? 4 }, () => ({ ph: r(), dx: (r() - 0.5) * 20 * sp, el: svg('path', { fill: '#bfe6ff', stroke: INK, 'stroke-width': 2 }, parent) }));
  return (x, y, k, t) => ds.forEach((d, i) => {
    const u = ((t * 1.1 + d.ph) % 1), px = x + d.dx + (dr ? dr * 10 : (i % 2 ? 14 : -14)) * u, py = y + 46 * u * u, s = 5.5;
    d.el.setAttribute('d', `M${px.toFixed(1)},${(py - s * 2).toFixed(1)} C${(px + s).toFixed(1)},${(py - s * 0.4).toFixed(1)} ${(px + s).toFixed(1)},${(py + s).toFixed(1)} ${px.toFixed(1)},${(py + s).toFixed(1)} C${(px - s).toFixed(1)},${(py + s).toFixed(1)} ${(px - s).toFixed(1)},${(py - s * 0.4).toFixed(1)} ${px.toFixed(1)},${(py - s * 2).toFixed(1)} Z`);
    d.el.setAttribute('opacity', (clamp(k) * Math.sin(Math.PI * u)).toFixed(2));
  });
}
