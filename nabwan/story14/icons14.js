// "720 มื้อ" graphics: a takeaway-bag icon, the meal tally (an odometer 1 → 720 over three rows of bags filling, one per
// school year ป.4 / ป.5 / ป.6), the "20 ปีก่อน" / "ปัจจุบัน" time chips, the glowing "?", tears.

// a pair of takeaway bags (rice + curry) as an inline icon
function bagIcon14(w = 80) {
  const bag = (x, c, s) => `<g transform="translate(${x},96) scale(${s})"><path d="M-22,0 Q-30,-20 -18,-34 L-8,-44 L8,-44 L18,-34 Q30,-20 22,0 Q0,8 -22,0 Z" fill="${c}" stroke="${INK}" stroke-width="3.2" stroke-linejoin="round"/>
    <path d="M-8,-44 L-12,-58 L-2,-50 L2,-60 L8,-44" fill="#f4f6f8" stroke="${INK}" stroke-width="2.6" stroke-linejoin="round"/><ellipse cx="0" cy="-46" rx="9" ry="3.5" fill="none" stroke="#c8343c" stroke-width="3"/>
    <path d="M-12,-36 Q-20,-28 -16,-14" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/></g>`;
  return `<svg width="${w}" height="${(w * 1.0).toFixed(0)}" viewBox="0 0 100 100">${bag(34, '#fbf7ec', 1.0)}${bag(68, '#e88a3a', 0.9)}
    <path d="M28,30 q4,-10 0,-18 M40,26 q4,-10 0,-18" fill="none" stroke="#c9b89a" stroke-width="3" stroke-linecap="round"/></svg>`;
}
// the meal tally card: the count rolls 1 → 720 while three rows of bag icons fill (one row per school year); update(t, t0, t1)
function mealTally14(parent, x, y) {
  const el = html('div', 'card tally14', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const row = (lbl) => `<div class="tr14"><i>${lbl}</i><span>${Array.from({ length: 12 }, () => `<b class="tb14">${bagIcon14(38)}</b>`).join('')}</span></div>`;
  el.innerHTML = `<div class="lbl">มื้อที่ครูซื้อ "เกิน"</div><div class="tn14"><b class="to14"></b><small>มื้อ</small></div>${row('ป.4')}${row('ป.5')}${row('ป.6')}<div class="shine"></div>`;
  const od = new Odometer(el.querySelector('.to14'), 3), bags = [...el.querySelectorAll('.tb14')], sh = el.querySelector('.shine');
  return {
    el, update(t, t0, t1) {
      enter3d(el, t, t0, 'flipDown');
      const k = ease.inOutCubic(prog(t, t0 + 0.3, t1)), n = Math.max(1, Math.round(720 * k));
      od.set(n, 0);
      const on = Math.floor(k * bags.length + 1e-6);
      bags.forEach((b, i) => { const kk = spring(t, t0 + 0.3 + (i / bags.length) * (t1 - t0 - 0.3), 18, 7); b.style.opacity = i < on ? 1 : 0.18; b.style.transform = i < on ? `scale(${(0.6 + 0.4 * Math.min(1.15, kk)).toFixed(3)})` : 'scale(0.8)'; b.style.filter = i < on ? 'none' : 'grayscale(1)'; });
      shine(sh, t, t1 + 0.1);
    },
  };
}
// a small time chip ("20 ปีก่อน" / "ปัจจุบัน"): update(t, t0)
function timeChip14(parent, x, y, text, sepia) {
  const el = html('div', 'chip big time14' + (sepia ? ' sep14' : ''), parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="44" height="44" viewBox="-22 -22 44 44"><circle r="18" fill="#fbf7ef" stroke="${INK}" stroke-width="3.5"/><path d="M0,0 L0,-11 M0,0 L8,4" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/></svg><span>${text}</span>`;
  return { el, update(t, t0) { popSquash(el, t, t0, '', -10); } };
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
