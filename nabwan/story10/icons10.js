// "52 ปีกับกระทงสองใบ" UI: a พ.ศ. year odometer, หลาน's speech bubble, a time-lapse clock chip, the glowing wish "?",
// and the krathong pair icon for the title and end card.

// year odometer chip: "ลอยด้วยกันตั้งแต่ พ.ศ. ____"
function yearChip10(parent, x, y, label) {
  const el = html('div', 'chip big yr10', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="ic5">${ktIcon(54)}</span><span>${label}</span><b class="o10"></b>`;
  const od = new Odometer(el.querySelector('.o10'), 4);
  return { el, update(t, t0, v, speed) { popSquash(el, t, t0); od.set(v, speed); } };
}
// speech bubble with a tail pointing down-left at the speaker
function bubble10(parent, x, y, text) {
  const el = html('div', 'bub10', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span>${text}</span><i></i>`;
  return { el, update(t, t0, t1) { const on = t > t0 && t < t1; const k = spring(t, t0, 14, 6); el.style.opacity = on ? Math.min(fadeIn(t, t0, 0.1), 1 - prog(t, t1 - 0.2, t1)).toFixed(3) : 0; el.style.transform = `scale(${(0.6 + 0.4 * Math.max(0, k)).toFixed(3)}) rotate(${(-3 + Math.sin(t * 2) * 1).toFixed(2)}deg)`; } };
}
// clock chip for the time-lapse: hands spin, the time counts from h0 to h1 (hours as floats)
function timeChip10(parent, x, y) {
  const el = html('div', 'chip big tm10', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<span class="ic5"><svg width="58" height="58" viewBox="-30 -30 60 60"><circle r="26" fill="#fbf7ef" stroke="${INK}" stroke-width="4"/><path class="hh" d="M0,0 L0,-13" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><path class="mm" d="M0,0 L0,-20" stroke="#e0453b" stroke-width="3.5" stroke-linecap="round"/><circle r="3.5" fill="${INK}"/></svg></span><b class="t10">21:00</b><small class="n10">น.</small>`;
  const hh = el.querySelector('.hh'), mm = el.querySelector('.mm'), tx = el.querySelector('.t10');
  return {
    el,
    update(t, t0, t1, h0 = 21, h1 = 23.67) {
      popSquash(el, t, t0);
      const h = lerp(h0, h1, ease.inOutSine(prog(t, t0 + 0.2, t1)));
      hh.setAttribute('transform', `rotate(${((h % 12) * 30).toFixed(1)})`); mm.setAttribute('transform', `rotate(${((h % 1) * 360).toFixed(1)})`);
      const H = Math.floor(h), M = Math.floor((h - H) * 60);
      tx.textContent = `${H}:${String(M).padStart(2, '0')}`;
    },
  };
}
// the wish: a glowing question mark with sparkles orbiting it
function wishQ(parent, x, y) {
  const el = html('div', 'wq10', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<b>?</b>${Array.from({ length: 5 }, () => '<i></i>').join('')}`;
  const sp = [...el.querySelectorAll('i')];
  return { el, update(t, t0) { popSquash(el, t, t0, `rotate(${(Math.sin(t * 2.4) * 7).toFixed(1)}deg)`, 16); sp.forEach((s, i) => { const a = t * 1.6 + i * 1.257; s.style.transform = `translate(${(Math.cos(a) * 90).toFixed(1)}px, ${(Math.sin(a) * 60).toFixed(1)}px) scale(${(0.6 + 0.4 * Math.sin(t * 5 + i)).toFixed(2)})`; }); } };
}
// krathong icon (HTML svg string) — a lit one, or a pair for the title / end card
function ktIcon(w, o = {}) {
  const one = (x, c) => `<g transform="translate(${x},0)"><ellipse cx="0" cy="-58" rx="70" ry="66" fill="url(#kti)"/><path d="M-56,0 Q-56,16 0,16 Q56,16 56,0 L52,-12 Q0,-2 -52,-12 Z" fill="#c9b07a" stroke="${INK}" stroke-width="4"/>${[-40, -20, 0, 20, 40].map(px => `<path d="M${px - 11},-12 L${px},-44 L${px + 11},-12 Z" fill="#4f9e4e" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>`).join('')}<path d="M0,-30 C-18,-42 -12,-68 0,-80 C12,-68 18,-42 0,-30 Z" fill="${c}" stroke="${INK}" stroke-width="3.5"/><rect x="14" y="-90" width="10" height="50" rx="3" fill="#fff3c4" stroke="${INK}" stroke-width="3"/><path d="M19,-110 C26,-99 26,-94 19,-88 C12,-94 12,-99 19,-110 Z" fill="#ffb03a" stroke="${INK}" stroke-width="2.5"/></g>`;
  const defs = `<defs><radialGradient id="kti"><stop offset="0" stop-color="#ffd27a" stop-opacity=".6"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient></defs>`;
  if (o.pair) return `<svg width="${w}" height="${w * 0.62}" viewBox="-150 -130 300 186" style="overflow:visible">${defs}${one(-66, '#b49ad8')}${one(66, '#f07aa8')}</svg>`;
  return `<svg width="${w}" height="${w}" viewBox="-70 -120 140 140" style="overflow:visible">${defs}${one(0, o.c || '#f07aa8')}</svg>`;
}
