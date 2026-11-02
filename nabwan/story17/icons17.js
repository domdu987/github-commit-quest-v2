// "128 ช่อ" graphics: a bouquet icon, the time chips, the delivery counter (polaroids of the people he delivered to fly
// in while the count rolls to 128), the day's money (what he earned, what goes out, what is left beside the price of one
// bouquet), the last order (an app banner, then the route that ends at his own door), the card in the bouquet, the "?",
// tears.

// a bouquet as an inline icon
function bouquetIcon17(w = 60) {
  return `<svg width="${w}" height="${(w * 1.4).toFixed(0)}" viewBox="-50 -110 100 150"><path d="M-46,-70 L46,-70 L14,40 L-14,40 Z" fill="#f8c8d8" fill-opacity=".8" stroke="${INK}" stroke-width="3"/>
    ${[[-22, -84, 15], [20, -86, 15], [0, -100, 16], [-6, -76, 14], [16, -70, 13]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#d8283a" stroke="${INK}" stroke-width="2.6"/>`).join('')}
    <path d="M-34,-60 L34,-60 L12,34 L-12,34 Z" fill="#c89a62" stroke="${INK}" stroke-width="3"/><path d="M-14,-4 L14,-4 L12,6 L-12,6 Z" fill="#d8486a" stroke="${INK}" stroke-width="2.4"/></svg>`;
}
// a small time chip ("23 ปีก่อน" / "พ.ศ. 2562"): update(t, t0)
function timeChip17(parent, x, y, text, sepia) {
  const el = html('div', 'chip big time14' + (sepia ? ' sep14' : ''), parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="44" height="44" viewBox="-22 -22 44 44"><circle r="18" fill="#fbf7ef" stroke="${INK}" stroke-width="3.5"/><path d="M0,0 L0,-11 M0,0 L8,4" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/></svg><span>${text}</span>`;
  return { el, update(t, t0) { popSquash(el, t, t0, '', -10); } };
}
// the delivery counter: polaroids fly in and stack while the count rolls 1 → 128; update(t, t0, t1)
function deliveries17(parent, x, y) {
  const el = html('div', 'card dlv17', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl"><span class="ics17">${bouquetIcon17(30)}</span>ส่งแล้ววันนี้</div><div class="dn17"><b class="dc17"></b><small>ช่อ</small></div><div class="pl17"></div><div class="shine"></div>`;
  const od = new Odometer(el.querySelector('.dc17'), 3), pl = el.querySelector('.pl17'), sh = el.querySelector('.shine');
  const pols = Array.from({ length: 7 }, (_, i) => { const p = html('div', 'po17', pl); const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); setA(d, { width: 76, height: 76, viewBox: '-38 -38 76 76' }); svg('rect', { x: -38, y: -38, width: 76, height: 76, fill: ['#fde2e8', '#e2eefc', '#fff1c8'][i % 3] }, d); faceFolk17(d, 0, 4, 24, i); p.appendChild(d); html('i', '', p).innerHTML = '♥'; return p; });
  const ocols = () => el.querySelectorAll('.dc17 .ocol');
  return {
    el, update(t, t0, t1) {
      enter3d(el, t, t0, 'flipDown');
      const k = ease.inOutCubic(prog(t, t0 + 0.3, t1)), n = Math.max(1, Math.round(128 * k));
      od.set(n, 0); const c = ocols(); if (c.length === 3) { c[0].style.display = n < 100 ? 'none' : 'inline-block'; c[1].style.display = n < 10 ? 'none' : 'inline-block'; }
      pols.forEach((p, i) => { const ti = t0 + 0.35 + i * (t1 - t0 - 0.4) / 7, kk = spring(t, ti, 16, 7); p.style.opacity = t > ti ? 1 : 0; p.style.transform = `translate(${((1 - Math.min(1, kk)) * 300).toFixed(1)}px, ${((1 - Math.min(1, kk)) * -120).toFixed(1)}px) rotate(${(-8 + (i % 3) * 7).toFixed(1)}deg) scale(${(0.6 + 0.4 * Math.min(1.1, kk)).toFixed(3)})`; });
      shine(sh, t, t1 + 0.1);
    },
  };
}
// the day's money: earned, minus fuel and rent, what is left beside one bouquet's price; update(t, t0)
function money17(parent, x, y) {
  const el = html('div', 'card mon17', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl">รายได้วันนี้</div><div class="mr17"><span>วิ่งงาน</span><b>+820</b></div><div class="mr17 neg"><span>ค่าน้ำมัน</span><b>−180</b></div><div class="mr17 neg"><span>ค่าผ่อนรถ</span><b>−300</b></div><div class="mt17"><span>เหลือ</span><b class="ml17">340</b><em class="vs17">ช่อละ 500</em></div><div class="shine"></div>`;
  const rows = [...el.querySelectorAll('.mr17')], left = el.querySelector('.ml17'), vs = el.querySelector('.vs17'), sh = el.querySelector('.shine');
  return {
    el, update(t, t0) {
      enter3d(el, t, t0, 'flipDown');
      rows.forEach((r, i) => { const k = spring(t, t0 + 0.25 + i * 0.25, 16, 7); r.style.opacity = t > t0 + 0.25 + i * 0.25 ? 1 : 0; r.style.transform = `translateX(${((1 - Math.min(1, k)) * -60).toFixed(1)}px)`; });
      const v = Math.round(lerp(820, 340, ease.outCubic(prog(t, t0 + 0.5, t0 + 1.3)))); left.textContent = v;
      left.style.color = t > t0 + 1.3 ? '#d8283a' : '#23242f';
      const kv = spring(t, t0 + 1.4, 14, 6); vs.style.opacity = t > t0 + 1.4 ? 1 : 0; vs.style.transform = `scale(${(0.5 + 0.5 * Math.min(1.1, kv)).toFixed(3)}) rotate(-4deg)`;
      shine(sh, t, t0 + 1.5);
    },
  };
}
// the last order: an app banner (buzz, ripple); update(t, t0)
function order17(parent, y) {
  const el = html('div', 'notif ord17', parent); el.style.top = y + 'px';
  el.innerHTML = `<span class="app">ส่งด่วน</span><div class="av ordic17">${bouquetIcon17(64)}</div><div style="flex:1"><div class="who">ออเดอร์สุดท้ายของวัน<small>22:04</small></div><div class="msg">ดอกไม้ 1 ช่อ · <b>ปลายทาง: ซอยร่มไม้ 3 บ้านเลขที่ 49/2</b></div></div>`;
  const rp = html('div', 'rip13', el);
  return {
    el, update(t, t0) {
      enter3d(el, t, t0, 'drop');
      const bz = t > t0 && t < t0 + 0.5 ? Math.sin((t - t0) * 70) * 5 * (1 - (t - t0) / 0.5) : 0; el.style.marginLeft = bz.toFixed(1) + 'px';
      const rk = ((t - t0) % 1.1) / 1.1; rp.style.opacity = t > t0 ? ((1 - rk) * 0.6).toFixed(3) : 0; rp.style.transform = `scale(${(1 + rk * 0.12).toFixed(3)})`;
    },
  };
}
// the route: a map; the scooter follows the line to the pin, the pin turns out to be home; update(t, t0, tHome)
function route17(parent, x, y) {
  const el = html('div', 'card rt17', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl">เส้นทางส่ง</div><div class="mp17"><svg width="560" height="250" viewBox="0 0 560 250">
    <rect width="560" height="250" rx="16" fill="#efe8dc"/>${[[0, 70, 560, 70], [0, 180, 560, 180], [140, 0, 140, 250], [400, 0, 400, 250]].map(([a, b, c, d]) => `<path d="M${a},${b} L${c},${d}" stroke="#ffffff" stroke-width="22"/>`).join('')}
    <path class="rl17" d="M40,180 L140,180 L140,70 L400,70 L400,180 L500,180" fill="none" stroke="#e8862a" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="900"/>
    <g class="pin17" transform="translate(500,180)"><path d="M0,0 C-26,-30 -26,-62 0,-62 C26,-62 26,-30 0,0 Z" fill="#d8283a" stroke="${INK}" stroke-width="3"/><circle cx="0" cy="-40" r="10" fill="#fff"/></g>
    <g class="home17" transform="translate(500,180)" opacity="0"><path d="M-30,-6 L-30,-40 L0,-64 L30,-40 L30,-6 Z" fill="#fbf7ef" stroke="${INK}" stroke-width="3"/><path d="${heartPathT(0, -32, 11)}" fill="#d8283a"/></g>
    <g class="bike17"><circle r="14" fill="#e8862a" stroke="${INK}" stroke-width="3"/><path d="M-6,0 L6,0" stroke="#fff" stroke-width="3"/></g></svg>
    <div class="hl17">บ้านเรา</div></div><div class="shine"></div>`;
  const line = el.querySelector('.rl17'), bike = el.querySelector('.bike17'), pin = el.querySelector('.pin17'), home = el.querySelector('.home17'), lab = el.querySelector('.hl17'), sh = el.querySelector('.shine');
  const pts = [[40, 180], [140, 180], [140, 70], [400, 70], [400, 180], [500, 180]], segs = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1])), tot = segs.reduce((a, b) => a + b, 0);
  const at = u => { let d = u * tot; for (let i = 0; i < segs.length; i++) { if (d <= segs[i]) { const k = d / segs[i]; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; } d -= segs[i]; } return pts[pts.length - 1]; };
  return {
    el, update(t, t0, tHome) {
      enter3d(el, t, t0, 'flipDown');
      const u = ease.inOutCubic(prog(t, t0 + 0.3, tHome)); line.setAttribute('stroke-dashoffset', (900 - tot * u).toFixed(1));
      const [bx, by] = at(u); bike.setAttribute('transform', `translate(${bx.toFixed(1)},${by.toFixed(1)})`);
      const kh = spring(t, tHome, 14, 6); home.setAttribute('opacity', t > tHome ? 1 : 0); home.setAttribute('transform', `translate(500,180) scale(${(t > tHome ? Math.min(1.15, kh) : 0).toFixed(3)})`); pin.setAttribute('opacity', t > tHome ? 0 : 1);
      lab.style.opacity = t > tHome + 0.15 ? 1 : 0; lab.style.transform = `scale(${(0.6 + 0.4 * Math.min(1.1, spring(t, tHome + 0.15, 14, 6))).toFixed(3)})`;
      shine(sh, t, tHome + 0.2);
    },
  };
}
// the card in the bouquet (her handwriting); update(t, t0)
function giftCard17(parent, x, y) {
  const el = html('div', 'gift17', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="gh17">${'♥'}</div><div class="gt17">ถึง คนส่งดอกไม้<br>ที่เหนื่อยที่สุดในวันนี้</div><div class="gs17">จาก เมีย</div>`;
  return { el, update(t, t0) { const k = spring(t, t0, 12, 6); el.style.opacity = t > t0 ? 1 : 0; el.style.transform = `translateY(${((1 - Math.min(1, k)) * 80).toFixed(1)}px) rotate(${(-6 + 2 * Math.sin(t * 1.5)).toFixed(1)}deg) scale(${(0.7 + 0.3 * Math.min(1.08, k)).toFixed(3)})`; } };
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
