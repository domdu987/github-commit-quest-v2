// Motion-design toolkit: springs, layered parallax shots, odometer counters, kinetic captions,
// particles, light effects, grain. Everything is a pure function of t so frames render deterministically.

// Damped spring 0 -> 1 with overshoot (f = frequency, d = damping).
function spring(t, t0, f = 16, d = 7) {
  if (t <= t0) return 0;
  const x = t - t0;
  return 1 - Math.exp(-d * x) * Math.cos(f * x);
}
const fadeIn = (t, t0, dur = 0.12) => clamp((t - t0) / dur);

// ---------------- layered shot with a parallax camera ----------------
class Shot {
  constructor(a, b, layers, opts = {}) {
    this.a = a; this.b = b;
    this.root = html('div', 'shot', frame);
    frame.insertBefore(this.root, subsBox);
    this.L = {};
    for (const [name, depth, blur] of layers) {
      const el = html('div', 'layer', this.root);
      const s = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'overflow:visible' }, el);
      const defs = svg('defs', {}, s);
      if (blur) el.style.filter = `blur(${blur}px)`;
      this.L[name] = { el, s, defs, depth };
    }
    this.ui = html('div', 'ui3d', this.root);
    this.fx = html('div', 'fxl', this.root);
    if (opts.grade) this.root.style.filter = opts.grade;
    this.updates = [];
  }
  cam(c) {
    for (const k in this.L) {
      const L = this.L[k], d = L.depth;
      const z = 1 + (c.z - 1) * d;
      L.el.style.transformOrigin = `${c.fx}px ${c.fy}px`;
      L.el.style.transform = `translate(${(-c.x * d).toFixed(2)}px, ${(-c.y * d).toFixed(2)}px) scale(${z.toFixed(4)}) rotate(${((c.r || 0) * d).toFixed(3)}deg)`;
    }
  }
}

// ---------------- 3D card / chip / icon entrances ----------------
// kind: 'flipDown' | 'swingLeft' | 'swingRight' | 'pop' | 'drop'
function enter3d(el, t, t0, kind = 'flipDown', extra = '') {
  const k = spring(t, t0, 14, 6.5), o = fadeIn(t, t0, 0.14);
  const float = t > t0 ? ` rotateX(${(Math.sin(t * 1.3) * 2.2).toFixed(2)}deg) rotateY(${(Math.cos(t * 1.05) * 2.8).toFixed(2)}deg)` : '';
  let tr;
  if (kind === 'flipDown') tr = `rotateX(${((1 - k) * -82).toFixed(2)}deg)`;
  else if (kind === 'swingLeft') tr = `rotateY(${((1 - k) * 70).toFixed(2)}deg) translateX(${((1 - k) * -80).toFixed(1)}px)`;
  else if (kind === 'swingRight') tr = `rotateY(${((1 - k) * -70).toFixed(2)}deg) translateX(${((1 - k) * 80).toFixed(1)}px)`;
  else if (kind === 'drop') tr = `translateY(${((1 - k) * -140).toFixed(1)}px)`;
  else tr = `scale(${(0.5 + 0.5 * k).toFixed(4)})`;
  el.style.opacity = o;
  el.style.transform = `${extra} ${tr}${float}`;
  return k;
}
// diagonal shine sweeping once across an element (needs .shine child)
function shine(el, t, t0, dur = 0.7) {
  const k = clamp((t - t0) / dur);
  el.style.transform = `translateX(${(-130 + 260 * ease.inOutCubic(k)).toFixed(1)}%) skewX(-20deg)`;
  el.style.opacity = k > 0 && k < 1 ? 1 : 0;
}

// ---------------- odometer counter ----------------
class Odometer {
  constructor(parent, digits, cls = '') {
    this.el = html('span', 'odo ' + cls, parent);
    this.cols = [];
    for (let i = 0; i < digits; i++) {
      const col = html('span', 'ocol', this.el);
      const strip = html('span', 'ostrip', col);
      for (let d = 0; d <= 10; d++) html('span', 'od', strip, String(d % 10));
      this.cols.push({ col, strip });
    }
    this.n = digits;
  }
  set(v, speed = 0) {
    const n = this.n;
    this.cols.forEach((c, i) => {
      const p = n - 1 - i, P = Math.pow(10, p);
      let off;
      if (p === 0) off = v % 10;
      else off = (Math.floor(v / P) % 10) + clamp((v % P) - (P - 1), 0, 1);
      c.strip.style.transform = `translateY(${(-off).toFixed(3)}em)`;
      const hide = p > 0 && v < P - 0.0001 && Math.floor(v / P) === 0 && clamp((v % P) - (P - 1), 0, 1) === 0;
      c.col.style.display = hide ? 'none' : 'inline-block';
      const blur = Math.min(5, (speed / P) * 0.06);
      c.strip.style.filter = blur > 0.3 ? `blur(${blur.toFixed(2)}px)` : 'none';
    });
  }
}
// eased value + numeric speed for an odometer
function rollValue(t, t0, t1, from, to) {
  const f = tt => lerp(from, to, ease.outCubic(prog(tt, t0, t1)));
  return { v: f(t), speed: Math.abs(f(t + 1 / 60) - f(t)) * 60 };
}

// ---------------- kinetic captions ----------------
const segTH = new Intl.Segmenter('th', { granularity: 'word' });
function buildCue(box, cue) {
  box.innerHTML = '';
  const words = [];
  for (const part of cue.parts) {
    const holder = html('span', 'kp kp-' + part.s, box);
    let inner = holder;
    if (part.s === 'r') { holder.classList.add('kbox'); inner = html('span', 'kbox-in', holder); }
    for (const seg of segTH.segment(part.t)) {
      if (seg.segment.trim() === '') { html('span', 'ksp', inner, ' '); continue; }
      words.push({ el: html('span', 'kw', inner, seg.segment), len: seg.segment.length, part, holder });
    }
  }
  // spread word onsets over the spoken part of the cue, proportional to length
  const span = Math.min((cue.b - cue.a) * 0.72, 0.16 * words.length + 0.25);
  const total = words.reduce((s, w) => s + w.len, 0);
  let acc = 0;
  for (const w of words) { w.t = cue.a + span * (acc / total); acc += w.len; }
  return words;
}
function renderKinetic(box, cues, t) {
  const cue = cues.find(c => t >= c.a - 0.02 && t < c.b);
  const key = cue ? cue.a : -1;
  if (box._key !== key) { box._key = key; box._words = cue ? buildCue(box, cue) : []; }
  if (!cue) { box.style.opacity = 0; return; }
  box.style.opacity = 1;
  const out = clamp((t - (cue.b - 0.1)) / 0.1);
  for (const w of box._words) {
    const k = spring(t, w.t, 18, 8), o = fadeIn(t, w.t, 0.09) * (1 - out);
    const b = Math.max(0, 1 - (t - w.t) / 0.14) * 7;
    w.el.style.opacity = o.toFixed(3);
    w.el.style.transform = `translateY(${((1 - k) * 26 - out * 14).toFixed(1)}px) scale(${(0.8 + 0.2 * k).toFixed(3)})`;
    w.el.style.filter = b > 0.2 && t >= w.t ? `blur(${b.toFixed(1)}px)` : 'none';
  }
  for (const h of box.querySelectorAll('.kbox')) {
    const first = box._words.find(w => w.holder === h);
    const k = spring(t, first.t - 0.06, 16, 7);
    h.style.setProperty('--bx', clamp(k, 0, 1.2).toFixed(3));
    h.style.opacity = (1 - out).toFixed(3);
  }
}

// ---------------- particles ----------------
// radial burst: sparkles flying out, slowing, fading
function burst(parent, cx, cy, t0, n, seed, colors = ['#ffd66b', '#ffffff', '#ff9fb2'], power = 260, life = 0.9) {
  const r = rng(seed), ps = [];
  for (let i = 0; i < n; i++) {
    const a = r() * Math.PI * 2, sp = power * (0.4 + r() * 0.8), size = 3 + r() * 6;
    const el = svg(r() > 0.5 ? 'circle' : 'path', {}, parent);
    if (el.tagName === 'circle') setA(el, { r: size * 0.6, fill: colors[i % colors.length] });
    else setA(el, { d: `M0,${-size} L${size * 0.3},${-size * 0.3} L${size},0 L${size * 0.3},${size * 0.3} L0,${size} L${-size * 0.3},${size * 0.3} L${-size},0 L${-size * 0.3},${-size * 0.3} Z`, fill: colors[i % colors.length] });
    ps.push({ el, a, sp, rot: r() * 360, spin: (r() - 0.5) * 600 });
  }
  return t => {
    const x = t - t0;
    for (const p of ps) {
      if (x < 0 || x > life) { p.el.setAttribute('opacity', 0); continue; }
      const d = p.sp * (1 - Math.exp(-3.2 * x)) / 3.2;
      const px = cx + Math.cos(p.a) * d, py = cy + Math.sin(p.a) * d + 60 * x * x;
      p.el.setAttribute('transform', `translate(${px.toFixed(1)},${py.toFixed(1)}) rotate(${(p.rot + p.spin * x).toFixed(1)}) scale(${(1 - x / life * 0.6).toFixed(3)})`);
      p.el.setAttribute('opacity', (1 - x / life).toFixed(3));
    }
  };
}
// drifting motes / bokeh / fireflies
function floaters(parent, box, n, seed, o = {}) {
  const r = rng(seed), ps = [];
  const [x0, y0, w, h] = box;
  for (let i = 0; i < n; i++) {
    const el = svg('circle', { r: (o.rMin || 1.5) + r() * ((o.rMax || 4) - (o.rMin || 1.5)), fill: o.color || '#ffe9c4' }, parent);
    if (o.filter) el.setAttribute('filter', o.filter);
    ps.push({ el, x: x0 + r() * w, y: y0 + r() * h, ph: r() * 6.28, sp: (o.speed || 10) * (0.5 + r()), amp: (o.amp || 18) * (0.5 + r()), base: o.base || 0.3 });
  }
  return t => ps.forEach(p => {
    const yy = y0 + ((p.y - y0 - t * p.sp) % h + h) % h;
    const tw = o.twinkle ? (0.5 + 0.5 * Math.sin(t * (o.twinkle) + p.ph * 3)) : 1;
    setA(p.el, { cx: (p.x + Math.sin(t * 0.7 + p.ph) * p.amp).toFixed(1), cy: yy.toFixed(1), opacity: (p.base + (o.op || 0.4) * tw * (0.5 + 0.5 * Math.sin(t * 1.4 + p.ph))).toFixed(3) });
  });
}
// expanding rings (ripples)
function ripples(parent, cx, cy, r0, color, count = 3, period = 1.4) {
  const rings = Array.from({ length: count }, () => svg('circle', { cx, cy, r: r0, fill: 'none', stroke: color, 'stroke-width': 6 }, parent));
  return (t, gain = 1) => rings.forEach((rg, i) => {
    const k = ((t + i * period / count) % period) / period;
    setA(rg, { r: (r0 + k * 150).toFixed(1), opacity: ((1 - k) * 0.6 * gain).toFixed(3), 'stroke-width': (8 - 6 * k).toFixed(2) });
  });
}

// ---------------- film grain ----------------
const GRAIN = [];
function makeGrain() {
  for (let i = 0; i < 4; i++) {
    const c = document.createElement('canvas'); c.width = 540; c.height = 960;
    const x = c.getContext('2d'), img = x.createImageData(540, 960), r = rng(100 + i);
    for (let j = 0; j < img.data.length; j += 4) { const v = 128 + (r() - 0.5) * 255; img.data[j] = img.data[j + 1] = img.data[j + 2] = v; img.data[j + 3] = 255; }
    x.putImageData(img, 0, 0);
    GRAIN.push(c.toDataURL());
  }
  const g = html('div', 'grain', frame);
  return t => { g.style.backgroundImage = `url(${GRAIN[Math.floor(t * 24) % 4]})`; };
}
