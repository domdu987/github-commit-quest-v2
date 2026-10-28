// "4,380 วันที่รอ" widgets: owner face, paw icon, wait chip, pat-vs-phone chips, vet card, day equation + waffle,
// "our life vs his life" comparison.

function ownerFace(parent, cx, cy, r, o = {}) {
  const c = OWNER, ink = INK;
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  svg('path', { fill: c.hair, stroke: ink, 'stroke-width': r * 0.06, d: `M${-r * 1.08},${-r * 0.1} C${-r * 1.14},${-r * 1.3} ${r * 1.14},${-r * 1.3} ${r * 1.08},${-r * 0.1} L${r * 1.06},${r * 0.7} Q${r * 0.8},${r * 0.86} ${r * 0.56},${r * 0.66} L${-r * 0.56},${r * 0.66} Q${-r * 0.8},${r * 0.86} ${-r * 1.06},${r * 0.7} Z` }, g);
  svg('circle', { r, fill: c.skin, stroke: ink, 'stroke-width': r * 0.07 }, g);
  const fr = `M${r * 0.98},${-r * 0.16} Q${r * 0.5},${-r * 0.4} 0,${-r * 0.38} Q${-r * 0.5},${-r * 0.4} ${-r * 0.98},${-r * 0.16}`;
  svg('path', { fill: c.hair, d: `M${-r * 0.98},${-r * 0.16} C${-r},${-r * 1.42} ${r},${-r * 1.42} ${r * 0.98},${-r * 0.16} ${fr.slice(fr.indexOf('Q'))} Z` }, g);
  svg('path', { fill: 'none', stroke: ink, 'stroke-width': r * 0.06, 'stroke-linecap': 'round', d: fr }, g);
  svg('rect', { x: r * 0.3, y: -r * 0.62, width: r * 0.32, height: r * 0.13, rx: r * 0.06, fill: c.clip, stroke: ink, 'stroke-width': r * 0.04, transform: `rotate(-14 ${r * 0.46} ${-r * 0.56})` }, g);
  for (const sx of [-1, 1]) {
    if (o.happy) svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${sx * r * 0.38 - r * 0.13},${r * 0.0} Q${sx * r * 0.38},${-r * 0.16} ${sx * r * 0.38 + r * 0.13},${r * 0.0}` }, g);
    else {
      svg('ellipse', { cx: sx * r * 0.38, cy: -r * 0.02, rx: r * 0.11, ry: r * 0.16, fill: '#2a1d21' }, g);
      svg('circle', { cx: sx * r * 0.38 + r * 0.04, cy: -r * 0.08, r: r * 0.045, fill: '#fff' }, g);
      svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': r * 0.04, 'stroke-linecap': 'round', d: `M${sx * r * 0.46},${-r * 0.14} l${sx * r * 0.1},${-r * 0.06}` }, g);
    }
    svg('ellipse', { cx: sx * r * 0.58, cy: r * 0.28, rx: r * 0.15, ry: r * 0.09, fill: '#f0857f', opacity: 0.5 }, g);
  }
  svg('path', { fill: 'none', stroke: c.lips, 'stroke-width': r * 0.065, 'stroke-linecap': 'round', d: `M${-r * 0.18},${r * 0.42} Q0,${r * 0.62} ${r * 0.18},${r * 0.42}` }, g);
  return g;
}
function ownerAv(n = 64, bg = '#dbe7f3') {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-48 -48 96 96' });
  svg('circle', { r: 48, fill: bg }, d);
  svg('path', { d: 'M-36,48 C-34,30 34,30 36,48 Z', fill: OWNER.shirt, stroke: INK, 'stroke-width': 2.5 }, d);
  ownerFace(d, 0, 4, 26);
  return d.outerHTML;
}
const pawSVG = (n = 48, c = '#bf8650') => `<svg width="${n}" height="${n}" viewBox="-30 -30 60 60"><ellipse cx="0" cy="8" rx="14" ry="12" fill="${c}" stroke="#fff" stroke-width="3"/>${[[-16, -6], [-6, -16], [6, -16], [16, -6]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="6" ry="7.5" fill="${c}" stroke="#fff" stroke-width="3"/>`).join('')}</svg>`;

// "รอมาแล้ว N ชั่วโมง" chip with a paw that taps
function waitChip(parent, x, y) {
  const el = html('div', 'chip big', parent); el.style.left = x + 'px'; el.style.top = y + 'px';
  const ic = html('span', 'ics', el); ic.innerHTML = pawSVG(52);
  const tx = html('span', '', el); tx.innerHTML = 'รอมาแล้ว ';
  const n = html('b', '', tx, '0'); html('span', '', tx, ' ชั่วโมง');
  return {
    el,
    update(t, t0, v) {
      popSquash(el, t, t0);
      n.textContent = Math.max(0, Math.floor(v));
      ic.style.transform = `translateY(${(-6 * Math.max(0, Math.sin(t * 6))).toFixed(1)}px) rotate(${(Math.sin(t * 6) * 8).toFixed(1)}deg)`;
    },
  };
}

// two chips: "ลูบหัว 2 วินาที" vs "มือถือ 3 ชั่วโมง"
function patVsPhone(parent, x, y) {
  const a = html('div', 'chip big', parent); a.style.left = x + 'px'; a.style.top = y + 'px';
  a.innerHTML = `<span class="ics">${pawSVG(52, '#dba468')}</span><span>ลูบหัว <b>2</b> วินาที</span>`;
  const b = html('div', 'chip big', parent); b.style.left = (x + 40) + 'px'; b.style.top = (y + 110) + 'px';
  b.innerHTML = `<span class="ics"><svg width="52" height="52" viewBox="-30 -30 60 60"><rect x="-14" y="-24" width="28" height="48" rx="6" fill="#2a2b36" stroke="#fff" stroke-width="3"/><rect x="-10" y="-19" width="20" height="34" rx="3" fill="#9fc6ff"/></svg></span><span>มือถือ <b>3</b> ชั่วโมง</span>`;
  return { update(t, ta, tb) { popSquash(a, t, ta); popSquash(b, t, tb); } };
}

// vet record card: old ลูกชิ้น, age 12, "เวลาที่เหลืออาจไม่มาก"
function vetCard(parent, x, y, w) {
  const c = cardEl(parent, 'card vet', x, y, w);
  const hd = html('div', 'lbl', c.c); hd.innerHTML = `<span class="ics"><svg width="46" height="46" viewBox="-25 -25 50 50"><circle r="22" fill="#4fae9b"/><path d="M-5,-14 L5,-14 L5,-5 L14,-5 L14,5 L5,5 L5,14 L-5,14 L-5,5 L-14,5 L-14,-5 L-5,-5 Z" fill="#fff"/></svg></span><span>ผลตรวจสุขภาพ</span>`;
  const row = html('div', 'vrow', c.c);
  const av = html('div', 'vav', row); av.innerHTML = dogAv(120, { old: true, bg: '#ffe9c4' });
  const info = html('div', 'vinfo', row);
  info.innerHTML = '<b>ลูกชิ้น</b><small>พันธุ์ไทย · เพศผู้</small>';
  const age = html('div', 'vline', c.c); age.innerHTML = '<span class="hl"><i style="background:#ffe27a"></i><span class="hlt">อายุ <b>12 ปี</b></span></span>';
  const note = html('div', 'vline', c.c); note.innerHTML = '<span class="hl"><i style="background:#ffc2bd"></i><span class="hlt">เวลาที่เหลืออาจไม่มาก</span></span>';
  const bars = [age.querySelector('i'), note.querySelector('i')];
  return {
    c,
    update(t, tin, t1, t2) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      bars[0].style.transform = `scaleX(${ease.outCubic(prog(t, t1, t1 + 0.35)).toFixed(3)})`;
      bars[1].style.transform = `scaleX(${ease.outCubic(prog(t, t2, t2 + 0.45)).toFixed(3)})`;
    },
  };
}

// "12 ปี × 365 = 4,380 วัน" then a waffle where almost every cell is a waiting day
function daysCard(parent, x, y, w) {
  const c = cardEl(parent, 'card days', x, y, w);
  const eq = html('div', 'eqrow', c.c);
  const t1 = html('div', 'eqterm', eq); t1.innerHTML = '<small>อายุ</small><b>12 ปี</b>';
  const op = html('div', 'eqop', eq, '×');
  const t2 = html('div', 'eqterm', eq); t2.innerHTML = '<small>วันละ</small><b>365</b>';
  const op2 = html('div', 'eqop', eq, '=');
  const t3 = html('div', 'eqterm hot', eq); t3.innerHTML = '<small>ทั้งหมด</small>';
  const nb = html('b', '', t3); const od = new Odometer(nb, 4); const fin = html('b', '', t3, '4,380'); fin.style.display = 'none'; html('span', 'eqsub', t3, ' วัน');
  const waf = html('div', 'waffle dog', c.c);
  const cells = Array.from({ length: 144 }, () => html('i', '', waf));
  const leg = html('div', 'legend', c.c);
  leg.innerHTML = `<div class="gold"><s></s>วันที่รอเขา</div><div class="gray"><s></s>วันอื่นๆ</div>`;
  return {
    c,
    update(t, tin, tEq, tRoll, tFill) {
      enter3d(c.c, t, tin, 'flipDown'); shine(c.sh, t, tin + 0.5);
      [t1, op, t2, op2, t3].forEach((e, i) => popSquash(e, t, tEq + i * 0.12));
      const r = rollValue(t, tRoll, tRoll + 1.1, 0, 4380); od.set(r.v, r.speed);
      const done = t > tRoll + 1.12; nb.style.display = done ? 'none' : 'inline-flex'; fin.style.display = done ? 'inline-flex' : 'none';
      const nOn = Math.floor(ease.outCubic(prog(t, tFill, tFill + 1.1)) * 136);
      cells.forEach((cl, i) => cl.className = i < nOn ? 'on' : '');
      leg.style.opacity = fadeIn(t, tFill + 0.6, 0.2);
    },
  };
}

// "ชีวิตเรามีหลายอย่าง" (many icons) vs "แต่ชีวิตเขามีแค่เรา" (one heart with her face)
function lifeCompare(parent, y) {
  const wrap = html('div', 'life', parent); wrap.style.top = y + 'px';
  const L = html('div', 'lcol', wrap); html('div', 'lhd', L, 'ชีวิตเรา');
  const box = html('div', 'lbox', L);
  const icons = ['💼', '📱', '☕', '👫', '✈️', '🎮'];
  const shapes = [
    '<rect x="-20" y="-12" width="40" height="28" rx="5" fill="#8a5d3c"/><rect x="-8" y="-20" width="16" height="10" rx="3" fill="none" stroke="#8a5d3c" stroke-width="4"/>',
    '<rect x="-12" y="-22" width="24" height="44" rx="5" fill="#2a2b36"/><rect x="-8" y="-17" width="16" height="30" rx="2" fill="#9fc6ff"/>',
    '<path d="M-16,-12 L14,-12 L10,18 L-12,18 Z" fill="#f6f1e6" stroke="#8a5d3c" stroke-width="3"/><path d="M14,-4 Q24,-2 14,8" fill="none" stroke="#8a5d3c" stroke-width="3"/>',
    '<circle cx="-9" cy="-8" r="8" fill="#e0aa80"/><circle cx="10" cy="-8" r="8" fill="#c98d62"/><path d="M-22,18 Q-9,0 4,18 Z M-2,18 Q10,0 22,18 Z" fill="#4a7bd8"/>',
    '<path d="M-22,4 L22,-6 L24,0 L-20,10 Z M-4,0 L6,-20 L12,-18 L8,2 Z M-12,6 L-16,16 L-10,16 L-4,6 Z" fill="#9aa3b2"/>',
    '<rect x="-22" y="-12" width="44" height="26" rx="12" fill="#6b5fb8"/><circle cx="-10" cy="1" r="4" fill="#fff"/><circle cx="12" cy="-3" r="3" fill="#f2c14e"/><circle cx="12" cy="6" r="3" fill="#e0574b"/>',
  ];
  const ics = shapes.map((sh, i) => { const e = html('div', 'lic', box); e.innerHTML = `<svg width="84" height="84" viewBox="-30 -30 60 60"><circle r="28" fill="#fff"/>${sh}</svg>`; return e; });
  const R = html('div', 'lcol', wrap); html('div', 'lhd', R, 'ชีวิตเขา');
  const hb = html('div', 'lheart', R);
  const hs = svg('svg', { width: 300, height: 280, viewBox: '-75 -70 150 140' }, hb);
  svg('path', { d: heartPathT(0, 4, 56), fill: '#f04f7f', stroke: '#fff', 'stroke-width': 5 }, hs);
  ownerFace(hs, 0, -2, 26, { happy: true });
  return {
    el: wrap,
    update(t, tL, tR) {
      wrap.style.opacity = fadeIn(t, tL - 0.1, 0.15);
      ics.forEach((e, i) => { popSquash(e, t, tL + i * 0.1); e.style.opacity = fadeIn(t, tL + i * 0.1, 0.08); });
      const k = spring(t, tR, 12, 5), beat = t > tR ? Math.pow(Math.max(0, Math.sin(t * 6)), 4) : 0;
      hb.style.opacity = fadeIn(t, tR, 0.1);
      hb.style.transform = `scale(${(Math.min(1.1, k) * (1 + 0.08 * beat)).toFixed(3)})`;
      R.style.opacity = t > tR - 0.2 ? 1 : 0.35;
    },
  };
}
