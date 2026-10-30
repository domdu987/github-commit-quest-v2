// "8 ซอง" graphics: a red-envelope icon, the "23 ปีก่อน" / "พ.ศ. 2562" chips, the first-salary notification, the
// eight-years card (a พ.ศ. odometer 2562 → 2569 while eight envelope slots fill, each one thicker), the closure letter
// with its stamp, อาม่า's LINE banner, the glowing "?", tears.

// a red envelope (อั่งเปา) as an inline icon; o.thick 0..1 puffs it
function angpaoIcon15(w = 60, o = {}) {
  const th = o.thick ?? 0, h = w * 1.4;
  return `<svg width="${w}" height="${(h + w * 0.12).toFixed(0)}" viewBox="-30 -46 60 ${(92 + 8).toFixed(0)}">
    ${th > 0 ? `<rect x="-20" y="-40" width="44" height="80" rx="4" fill="#8e1e26" stroke="${INK}" stroke-width="2.6" transform="translate(${(2 + th * 3).toFixed(1)},${(-1 - th * 2).toFixed(1)})"/>` : ''}
    <rect x="-22" y="-40" width="44" height="80" rx="4" fill="#d43a40" stroke="${INK}" stroke-width="3"/>
    <rect x="-17" y="-35" width="34" height="70" rx="2" fill="none" stroke="#f2c14e" stroke-width="2"/>
    <path d="M-22,-38 L0,-18 L22,-38" fill="none" stroke="#8e1e26" stroke-width="2.6" stroke-linejoin="round"/>
    <circle cx="0" cy="-18" r="4.5" fill="#f2c14e" stroke="#a8781e" stroke-width="1.5"/>
    <circle cx="0" cy="8" r="11" fill="#f2c14e" stroke="#a8781e" stroke-width="2"/><rect x="-3.5" y="4.5" width="7" height="7" fill="#d43a40"/>
    <path d="M-14,-28 L-14,24" stroke="#ff9a8a" stroke-width="3" stroke-linecap="round" opacity=".5"/></svg>`;
}
// a small time chip ("23 ปีก่อน" / "พ.ศ. 2562"): update(t, t0)
function timeChip15(parent, x, y, text, sepia) {
  const el = html('div', 'chip big time14' + (sepia ? ' sep14' : ''), parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<svg width="44" height="44" viewBox="-22 -22 44 44"><circle r="18" fill="#fbf7ef" stroke="${INK}" stroke-width="3.5"/><path d="M0,0 L0,-11 M0,0 L8,4" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/></svg><span>${text}</span>`;
  return { el, update(t, t0) { popSquash(el, t, t0, '', -10); } };
}
// the first salary landing: a bank notification, the amount counting up; update(t, t0)
function salaryCard15(parent, x, y) {
  const el = html('div', 'card pay15', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl"><span class="bk15">฿</span>เงินเดือนเดือนแรก<small>เข้าแล้ว</small></div><div class="pn15">+<b class="pa15">0</b><small>บาท</small></div><div class="shine"></div>`;
  const a = el.querySelector('.pa15'), sh = el.querySelector('.shine');
  return { el, update(t, t0) { enter3d(el, t, t0, 'flipDown'); const v = Math.round(15000 * ease.outCubic(prog(t, t0 + 0.3, t0 + 1.2))); a.textContent = v.toLocaleString('en-US'); a.style.transform = `scale(${(1 + 0.12 * Math.sin(Math.PI * prog(t, t0 + 1.2, t0 + 1.5))).toFixed(3)})`; shine(sh, t, t0 + 1.25); } };
}
// eight New Years: the year rolls 2562 → 2569 while the slots fill with envelopes, each thicker; update(t, t0, t1)
function yearsCard15(parent, x, y) {
  const el = html('div', 'card yrs15', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const AMT = ['500', '800', '1,000', '1,000', '1,500', '2,000', '2,000', '2,000'];
  el.innerHTML = `<div class="lbl">อั่งเปาที่ให้อาม่า</div><div class="yr15"><span>ตรุษจีน พ.ศ.</span><b class="yo15"></b></div>
    <div class="sl15">${AMT.map((a, i) => `<div class="sc15"><i class="se15">${angpaoIcon15(52, { thick: i / 7 })}</i><small>${a}</small></div>`).join('')}</div><div class="shine"></div>`;
  const od = new Odometer(el.querySelector('.yo15'), 4), slots = [...el.querySelectorAll('.sc15')], sh = el.querySelector('.shine');
  return {
    el, update(t, t0, t1) {
      enter3d(el, t, t0, 'flipDown');
      const k = prog(t, t0 + 0.3, t1), n = Math.min(8, 1 + Math.floor(k * 7.999));
      od.set(2561 + n, 0);
      slots.forEach((s, i) => { const on = i < n, kk = spring(t, t0 + 0.3 + (i / 7.999) * (t1 - t0 - 0.3), 18, 7); s.style.opacity = on ? 1 : 0.22; s.querySelector('i').style.transform = on ? `translateY(${((1 - Math.min(1, kk)) * -40).toFixed(1)}px) scale(${(0.7 + 0.3 * Math.min(1.12, kk)).toFixed(3)})` : 'scale(0.8)'; s.style.filter = on ? 'none' : 'grayscale(1)'; });
      shine(sh, t, t1 + 0.1);
    },
  };
}
// the company's closure letter; the red stamp lands at tStamp; update(t, t0, tStamp)
function closedCard15(parent, x, y) {
  const el = html('div', 'card shut15', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="lbl">ประกาศถึงพนักงานทุกคน</div><div class="tl15">บริษัทขอแจ้งปิดกิจการ</div><div class="ln15"><i></i><i></i><i style="width:60%"></i></div><div class="stp15">ปิดกิจการ</div><div class="shine"></div>`;
  const stp = el.querySelector('.stp15'), sh = el.querySelector('.shine');
  return {
    el, update(t, t0, tStamp) {
      enter3d(el, t, t0, 'flipDown');
      const k = prog(t, tStamp, tStamp + 0.22);
      stp.style.opacity = t > tStamp ? 1 : 0;
      stp.style.transform = `rotate(-12deg) scale(${(t > tStamp ? lerp(2.2, 1, ease.outCubic(k)) : 2.2).toFixed(3)})`;
      el.style.marginLeft = (t > tStamp + 0.2 && t < tStamp + 0.45 ? Math.sin((t - tStamp) * 80) * 4 : 0).toFixed(1) + 'px';
      shine(sh, t, t0 + 0.4);
    },
  };
}
// อาม่า's LINE message (types out, buzzes with a ripple); update(t, t0, tType)
function lineBanner15(parent, y, msg) {
  const el = html('div', 'notif line13', parent); el.style.top = y + 'px';
  el.innerHTML = `<span class="app">LINE</span><div class="av">${av15('ama', 96)}</div><div style="flex:1"><div class="who">อาม่า<small>ตรุษจีน · 08:12</small></div><div class="msg"><span class="ty13"></span><span class="ic13">${orangeIcon15(40)}</span></div></div>`;
  const ty = el.querySelector('.ty13'), ic = el.querySelector('.ic13');
  const rp = html('div', 'rip13', el);
  return {
    el, update(t, t0, tType) {
      enter3d(el, t, t0, 'drop');
      const n = Math.round(prog(t, tType, tType + 0.8) * msg.length);
      ty.textContent = msg.slice(0, n);
      ic.style.opacity = n >= msg.length ? 1 : 0;
      ic.style.transform = n >= msg.length ? `scale(${(0.6 + 0.4 * spring(t, tType + 0.8, 18, 7)).toFixed(3)})` : 'scale(0.6)';
      const bz = t > t0 && t < t0 + 0.5 ? Math.sin((t - t0) * 70) * 5 * (1 - (t - t0) / 0.5) : 0;
      el.style.marginLeft = bz.toFixed(1) + 'px';
      const rk = ((t - t0) % 1.1) / 1.1;
      rp.style.opacity = t > t0 ? ((1 - rk) * 0.6).toFixed(3) : 0; rp.style.transform = `scale(${(1 + rk * 0.12).toFixed(3)})`;
    },
  };
}
const orangeIcon15 = (s = 40) => `<svg width="${s}" height="${s}" viewBox="-20 -22 40 42"><circle cx="0" cy="2" r="16" fill="#f29a2e" stroke="${INK}" stroke-width="2.6"/><circle cx="-5" cy="-3" r="4" fill="#ffd28a" opacity=".8"/><path d="M0,-14 q4,-8 12,-6 q-4,6 -12,6" fill="#4f9e5e" stroke="${INK}" stroke-width="2"/></svg>`;
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
