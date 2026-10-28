// "12 ฤดูฝน" UI: the umbrella icon, a school-year chip that flips ป.1 → ม.6 while twelve raindrop pips fill (one per
// rainy season), พ่อ's age odometer, speech bubbles, the tilt protractor ("นิดเดียว"), the glowing raindrop "?",
// and twinkle sparkles for the dry kid.

// umbrella icon (HTML svg string) with falling drops
function umbIcon(w, o = {}) {
  const c = o.c || ['#a8323e', '#f1e6cf'], n = 6, R = 60, top = -34, rim = 0;
  let gores = '';
  for (let i = 0; i < n; i++) {
    const a = R * Math.cos(Math.PI * i / n), b = R * Math.cos(Math.PI * (i + 1) / n);
    gores += `<path d="M0,${top} Q${(a * 0.92).toFixed(1)},${top + 3} ${a.toFixed(1)},${rim} Q${((a + b) / 2).toFixed(1)},${rim - 8} ${b.toFixed(1)},${rim} Q${(b * 0.92).toFixed(1)},${top + 3} 0,${top} Z" fill="${c[i % 2]}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
  }
  const drops = o.drops === false ? '' : [[-46, -64], [30, -78], [62, -48], [-70, -30]].map(([x, y]) => `<path d="M${x},${y - 10} C${x + 6},${y - 2} ${x + 6},${y + 4} ${x},${y + 5} C${x - 6},${y + 4} ${x - 6},${y - 2} ${x},${y - 10} Z" fill="#7fc0e8" stroke="${INK}" stroke-width="2"/>`).join('');
  return `<svg width="${w}" height="${w}" viewBox="-80 -90 160 160" style="overflow:visible">${drops}<path d="M0,0 L0,46 Q0,62 13,62 Q24,62 24,50" fill="none" stroke="${INK}" stroke-width="11" stroke-linecap="round"/><path d="M0,0 L0,46 Q0,62 13,62 Q24,62 24,50" fill="none" stroke="#8a5232" stroke-width="5" stroke-linecap="round"/>${gores}<path d="M0,${top} L0,${top - 14}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><path d="M-30,-20 Q-16,-30 0,-31" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".5"/></svg>`;
}
const GRADES = ['ป.1', 'ป.2', 'ป.3', 'ป.4', 'ป.5', 'ป.6', 'ม.1', 'ม.2', 'ม.3', 'ม.4', 'ม.5', 'ม.6'];
// school-year chip: "ฤดูฝนที่ n" with the grade flipping and 12 drop pips
function gradeChip11(parent, x, y) {
  const el = html('div', 'gr11', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="gr11h"><span class="ic5">${umbIcon(58, { drops: false })}</span><span class="gr11l">ฤดูฝนที่ <b class="gr11n">1</b></span><b class="gr11g">ป.1</b></div><div class="pips11">${GRADES.map(() => '<i></i>').join('')}</div>`;
  const g = el.querySelector('.gr11g'), num = el.querySelector('.gr11n'), pips = [...el.querySelectorAll('.pips11 i')];
  let last = -1, tFlip = -9;
  return {
    el,
    update(t, t0, k) {
      enter3d(el, t, t0, 'flipDown');
      const i = Math.min(11, Math.floor(clamp(k) * 12));
      if (i !== last) { if (last >= 0) tFlip = t; last = i; g.textContent = GRADES[i]; num.textContent = i + 1; }
      const f = prog(t, tFlip, tFlip + 0.18);
      g.style.transform = `rotateX(${(Math.sin(Math.PI * f) * 70).toFixed(1)}deg) scale(${(1 + 0.15 * Math.sin(Math.PI * f)).toFixed(3)})`;
      pips.forEach((p, j) => { const on = j <= i; p.className = on ? 'on' : ''; p.style.transform = `rotate(45deg) scale(${on ? (1 + 0.5 * Math.max(0, 1 - (t - tFlip) / 0.25) * (j === i ? 1 : 0)).toFixed(3) : 0.8})`; });
    },
  };
}
// พ่อ's age chip with a rolling two-digit odometer
function ageChip11(parent, x, y) {
  const el = html('div', 'chip big age11', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="av11">${av11('dad', 64)}</span><span>พ่ออายุ</span><b class="o11"></b><small>ปี</small>`;
  const od = new Odometer(el.querySelector('.o11'), 2);
  return { el, update(t, t0, v, speed) { popSquash(el, t, t0, '', -10); od.set(v, speed); } };
}
// speech bubble; side 'L' puts the tail bottom-left, 'R' bottom-right
function bubble11(parent, x, y, htmlTx, side = 'L') {
  const el = html('div', 'bub10 bub11' + (side === 'R' ? ' r' : ''), parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span>${htmlTx}</span><i></i>`;
  return { el, update(t, t0, t1) { const on = t > t0 && t < t1; const k = spring(t, t0, 14, 6); el.style.opacity = on ? Math.min(fadeIn(t, t0, 0.1), 1 - prog(t, t1 - 0.2, t1)).toFixed(3) : 0; el.style.transform = `scale(${(0.6 + 0.4 * Math.max(0, k)).toFixed(3)}) rotate(${(-2 + Math.sin(t * 2) * 1).toFixed(2)}deg)`; } };
}
// the glowing raindrop "?"
function dropQ(parent, x, y) {
  const el = html('div', 'wq10 dq11', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<b>?</b>${Array.from({ length: 5 }, () => '<i></i>').join('')}`;
  const sp = [...el.querySelectorAll('i')];
  return { el, update(t, t0) { popSquash(el, t, t0, `rotate(${(Math.sin(t * 2.4) * 7).toFixed(1)}deg)`, 16); sp.forEach((s, i) => { const a = t * 1.6 + i * 1.257; s.style.transform = `translate(${(Math.cos(a) * 90).toFixed(1)}px, ${(Math.sin(a) * 60).toFixed(1)}px) scale(${(0.6 + 0.4 * Math.sin(t * 5 + i)).toFixed(2)})`; }); } };
}
// tilt protractor in world space: dashed vertical, an arc to the umbrella shaft, and a "นิดเดียว" tag; update(cx, cy, deg, k)
function tiltArc(parent, label = 'นิดเดียว') {
  const g = svg('g', { opacity: 0 }, parent);
  const vline = svg('path', { stroke: '#fff6dc', 'stroke-width': 5, 'stroke-dasharray': '14 12', 'stroke-linecap': 'round', fill: 'none' }, g);
  const arcO = svg('path', { stroke: INK, 'stroke-width': 12, fill: 'none', 'stroke-linecap': 'round' }, g);
  const arc = svg('path', { stroke: '#ffd166', 'stroke-width': 7, fill: 'none', 'stroke-linecap': 'round' }, g);
  const head = svg('path', { fill: '#ffd166', stroke: INK, 'stroke-width': 3 }, g);
  const tag = svg('g', {}, g);
  svg('rect', { x: -112, y: -40, width: 224, height: 72, rx: 36, fill: '#fff', stroke: INK, 'stroke-width': 5 }, tag);
  wtext(tag, 0, 15, label, 46, '#e0453b', { w: 700 });
  return (cx, cy, deg, k, t = 0) => {
    g.setAttribute('opacity', clamp(k * 3).toFixed(3));
    const rr = 150, a0 = -90, a1 = -90 + deg * clamp(k);
    const p = a => [cx + Math.cos(rad(a)) * rr, cy + Math.sin(rad(a)) * rr];
    vline.setAttribute('d', `M${cx},${cy} L${cx},${cy - rr - 40}`);
    const [x0, y0] = p(a0), [x1, y1] = p(a1);
    const d = `M${x0.toFixed(1)},${y0.toFixed(1)} A${rr},${rr} 0 0,1 ${x1.toFixed(1)},${y1.toFixed(1)}`;
    arc.setAttribute('d', d); arcO.setAttribute('d', d);
    const ta = rad(a1 + 90);
    head.setAttribute('d', `M${(x1 + Math.cos(ta) * 16).toFixed(1)},${(y1 + Math.sin(ta) * 16).toFixed(1)} L${(x1 + Math.cos(ta + 2.4) * 14).toFixed(1)},${(y1 + Math.sin(ta + 2.4) * 14).toFixed(1)} L${(x1 + Math.cos(ta - 2.4) * 14).toFixed(1)},${(y1 + Math.sin(ta - 2.4) * 14).toFixed(1)} Z`);
    const kk = spring(t, 0, 14, 6);
    tag.setAttribute('transform', `translate(${(x1 + 150).toFixed(1)},${(y1 - 40).toFixed(1)}) scale(${Math.max(0.01, clamp(k * 1.4) * (0.8 + 0.2 * kk)).toFixed(3)})`);
  };
}
// four-point sparkles twinkling around a point (world); update(cx, cy, k, t)
function sparkles(parent, n, seed) {
  const r = rng(seed);
  const ss = Array.from({ length: n }, () => ({ a: r() * Math.PI * 2, d: 60 + r() * 70, ph: r() * 6, s: 8 + r() * 10, el: svg('path', { d: fourStar(1), fill: '#fff6dc', stroke: '#e0a12c', 'stroke-width': 0.08 }, parent) }));
  return (cx, cy, k, t) => ss.forEach(s => {
    const tw = Math.max(0, Math.sin(t * 5 + s.ph));
    s.el.setAttribute('transform', `translate(${(cx + Math.cos(s.a + t * 0.6) * s.d).toFixed(1)},${(cy + Math.sin(s.a + t * 0.6) * s.d * 0.8).toFixed(1)}) scale(${(s.s * (0.4 + 0.6 * tw) * clamp(k)).toFixed(2)})`);
    s.el.setAttribute('opacity', (clamp(k) * (0.4 + 0.6 * tw)).toFixed(2));
  });
}
