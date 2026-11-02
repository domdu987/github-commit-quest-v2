// "50 กุหลาบ" graphics: a red-rose icon, the "49 ปีก่อน" / date chips, the album counter (a พ.ศ. odometer 2521 → 2569
// while the pressed-rose count rolls 1 → 49), the glowing "?", tears.

// a red rose as an inline icon
function roseIcon16(w = 60, o = {}) {
  const red = o.dry ? '#9a3a3a' : '#d8283a';
  return `<svg width="${w}" height="${(w * 1.6).toFixed(0)}" viewBox="-30 -126 60 132"><path d="M0,0 Q4,-40 0,-88" fill="none" stroke="#3f7a46" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M1,-46 q16,-14 26,-6 q-10,12 -26,6 Z" fill="#4f9e5e" stroke="${INK}" stroke-width="2.2"/><path d="M0,-62 q-16,-12 -24,-2 q12,10 24,2 Z" fill="#4f9e5e" stroke="${INK}" stroke-width="2.2"/>
    <path d="M-15,-96 Q-18,-116 0,-122 Q18,-116 15,-96 Q8,-86 0,-86 Q-8,-86 -15,-96 Z" fill="${red}" stroke="${INK}" stroke-width="3"/>
    <path d="M-8,-106 Q0,-116 8,-106 M-11,-98 Q0,-92 11,-98" fill="none" stroke="#a81828" stroke-width="2.4" stroke-linecap="round"/></svg>`;
}
// a small time chip ("23 ปีก่อน" / "พ.ศ. 2562"): update(t, t0)
function timeChip16(parent, x, y, text, sepia) {
  const el = html('div', 'chip big time14' + (sepia ? ' sep14' : ''), parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="44" height="44" viewBox="-22 -22 44 44"><circle r="18" fill="#fbf7ef" stroke="${INK}" stroke-width="3.5"/><path d="M0,0 L0,-11 M0,0 L8,4" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/></svg><span>${text}</span>`;
  return { el, update(t, t0) { popSquash(el, t, t0, '', -10); } };
}
// the album counter: the year rolls 2521 → 2569 while the count of pressed roses rolls 1 → 49; update(t, t0, t1)
function albumCard16(parent, x, y) {
  const el = html('div', 'card alb16', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl">${roseIcon16(30, { dry: true })}กุหลาบในสมุดของยาย</div><div class="ar16"><div><span>วาเลนไทน์ พ.ศ.</span><b class="ay16"></b></div><div class="an16"><b class="ac16"></b><small>ดอก</small></div></div><div class="shine"></div>`;
  const oy = new Odometer(el.querySelector('.ay16'), 4), oc = new Odometer(el.querySelector('.ac16'), 2), sh = el.querySelector('.shine');
  const ocEl = el.querySelector('.ac16');
  return {
    el, update(t, t0, t1) {
      enter3d(el, t, t0, 'flipDown');
      const n = Math.max(1, Math.min(49, Math.round(1 + 48 * ease.inOutCubic(prog(t, t0 + 0.3, t1)))));
      oy.set(2520 + n, 0); oc.set(n, 0);
      const cols = ocEl.querySelectorAll('.ocol'); if (cols.length > 1) cols[0].style.display = n < 10 ? 'none' : 'inline-block';
      shine(sh, t, t1 + 0.1);
    },
  };
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
