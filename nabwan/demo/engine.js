// Frame-deterministic 2D animation helpers. Every visual is a pure function of time t (seconds).
const W = 1080, H = 1920, FPS = 30;
const NS = 'http://www.w3.org/2000/svg';

const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lerp = (a, b, k) => a + (b - a) * k;
const prog = (t, a, b) => clamp((t - a) / (b - a));
const rad = d => d * Math.PI / 180;
const ease = {
  outCubic: k => 1 - Math.pow(1 - k, 3),
  inCubic: k => k * k * k,
  inOutCubic: k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
  inOutSine: k => -(Math.cos(Math.PI * k) - 1) / 2,
  outBack: k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); },
};

function svg(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function html(tag, cls, parent, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
function setA(e, attrs) { for (const k in attrs) e.setAttribute(k, attrs[k]); }
function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

// Scale+fade "pop" used by every card, pill and icon: slight overshoot, then settle.
function pop(t, t0, dur = 0.34) {
  const k = prog(t, t0, t0 + dur);
  return { s: k <= 0 ? 0.001 : 0.72 + 0.28 * ease.outBack(k), o: clamp(k * 2.2) };
}
function applyPop(el, t, t0, extra = '') {
  const p = pop(t, t0);
  el.style.opacity = p.o;
  el.style.transform = `${extra} scale(${p.s})`;
}
// Number roll used by counters.
function countUp(t, t0, t1, from, to) {
  return Math.round(lerp(from, to, ease.outCubic(prog(t, t0, t1))));
}
// Camera: slow push-in on a scene container. focus in frame px.
function camera(el, k, fromS, toS, fx, fy) {
  const s = lerp(fromS, toS, ease.inOutSine(k));
  el.style.transformOrigin = `${fx}px ${fy}px`;
  el.style.transform = `scale(${s})`;
}

// ---------- Side-view puppet (faces right; flip with facing=-1) ----------
class Person {
  constructor(parent, o) {
    this.o = Object.assign({
      skin: '#c98e66', skinShade: '#b27752', hair: '#2a2326', hairStyle: 'bob',
      shirt: '#8fb3de', shirtShade: '#7a9ccb', sleeve: 'long', pants: '#2f3a5c', pantsShade: '#273150',
      shoe: '#f1f1f1', sarong: null, glasses: false, s: 1,
    }, o);
    const O = this.o;
    this.g = svg('g', {}, parent);
    const L = (g, c, w) => svg('path', { fill: 'none', stroke: c, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
    // back limbs (darker), then torso, front limbs, head
    this.gBackArm = svg('g', {}, this.g);
    this.gBackLeg = svg('g', {}, this.g);
    this.gTorso = svg('g', {}, this.g);
    this.gFrontLeg = svg('g', {}, this.g);
    this.gHead = svg('g', {}, this.g);
    this.gFrontArm = svg('g', {}, this.g);
    const armShade = O.sleeve === 'long' ? O.shirtShade : O.skinShade;
    this.bArmU = L(this.gBackArm, O.shirtShade, 27);
    this.bArmF = L(this.gBackArm, armShade, 23);
    this.bHand = svg('circle', { r: 13, fill: O.skinShade }, this.gBackArm);
    this.bLegU = L(this.gBackLeg, O.pantsShade, 40);
    this.bLegL = L(this.gBackLeg, O.pantsShade, 34);
    this.bShoe = svg('path', { fill: shade(O.shoe, -18) }, this.gBackLeg);
    this.torso = L(this.gTorso, O.shirt, 78);
    this.waist = L(this.gTorso, O.pants, 74);
    if (O.sarong) {
      this.sarong = svg('path', { fill: O.sarong }, this.gTorso);
      this.sarongStripe = svg('path', { fill: 'none', stroke: shade(O.sarong, 28), 'stroke-width': 6, opacity: 0.8 }, this.gTorso);
    }
    if (O.pattern) this.pattern = svg('g', { opacity: 0.55 }, this.gTorso);
    this.fLegU = L(this.gFrontLeg, O.pants, 40);
    this.fLegL = L(this.gFrontLeg, O.pants, 34);
    this.fShoe = svg('path', { fill: O.shoe }, this.gFrontLeg);
    this.neck = L(this.gHead, O.skinShade, 26);
    this.head = svg('g', {}, this.gHead);
    this.buildHead();
    this.fArmU = L(this.gFrontArm, O.shirt, 28);
    this.fArmF = L(this.gFrontArm, O.sleeve === 'long' ? O.shirt : O.skin, 24);
    this.fHand = svg('circle', { r: 14, fill: O.skin }, this.gFrontArm);
    this.prop = svg('g', {}, this.gFrontArm); // things held in the front hand
  }
  buildHead() {
    const O = this.o, h = this.head;
    if (O.hairStyle === 'bob') {
      this.hairBack = svg('path', { fill: O.hair, d: 'M30,-44 C6,-66 -46,-62 -60,-20 C-66,8 -62,40 -54,58 C-40,66 -18,62 -6,54 L-4,0 Z' }, h);
    } else if (O.hairStyle === 'bun') {
      svg('circle', { cx: -50, cy: -30, r: 24, fill: O.hair }, h);
      this.hairBack = svg('path', { fill: O.hair, d: 'M32,-42 C8,-64 -44,-62 -56,-22 C-60,-2 -56,18 -48,30 L-4,6 Z' }, h);
    } else if (O.hairStyle === 'short') {
      this.hairBack = svg('path', { fill: O.hair, d: 'M36,-38 C14,-64 -40,-64 -54,-24 C-58,-6 -54,12 -46,20 L-2,0 Z' }, h);
    }
    svg('circle', { cx: 0, cy: 0, r: 50, fill: O.skin }, h);
    svg('ellipse', { cx: -10, cy: 6, rx: 9, ry: 12, fill: O.skinShade }, h); // ear
    svg('circle', { cx: 47, cy: 8, r: 7, fill: O.skin }, h); // nose
    svg('circle', { cx: 22, cy: 16, r: 9, fill: '#e98a86', opacity: 0.33 }, h); // blush
    // fringe over the forehead
    if (O.hairStyle === 'bob') svg('path', { fill: O.hair, d: 'M-48,-14 C-44,-58 18,-66 44,-26 C30,-34 14,-36 2,-30 C-14,-36 -30,-30 -48,-14 Z' }, h);
    if (O.hairStyle === 'bun') svg('path', { fill: O.hair, d: 'M-50,-12 C-44,-58 20,-64 46,-24 C26,-36 -4,-40 -50,-12 Z' }, h);
    if (O.hairStyle === 'short') svg('path', { fill: O.hair, d: 'M-50,-6 C-46,-60 24,-66 48,-22 C30,-34 -6,-36 -50,-6 Z' }, h);
    if (O.gray) svg('path', { fill: 'none', stroke: O.gray, 'stroke-width': 5, 'stroke-linecap': 'round', d: 'M-30,-40 C-14,-50 6,-50 22,-42' }, h);
    this.brow = svg('path', { fill: 'none', stroke: O.hair, 'stroke-width': 4, 'stroke-linecap': 'round', d: 'M15,-23 Q24,-29 34,-24' }, h);
    this.eye = svg('ellipse', { cx: 26, cy: -6, rx: 4.6, ry: 6.5, fill: '#231d20' }, h);
    this.eyeLid = svg('path', { fill: 'none', stroke: '#231d20', 'stroke-width': 3.6, 'stroke-linecap': 'round', d: 'M20,-5 Q26,0 32,-5', opacity: 0 }, h);
    if (O.glasses) {
      svg('rect', { x: 14, y: -17, width: 26, height: 20, rx: 6, fill: 'rgba(255,255,255,0.12)', stroke: '#3b3236', 'stroke-width': 3 }, h);
      svg('path', { fill: 'none', stroke: '#3b3236', 'stroke-width': 3, d: 'M14,-8 L-6,-4' }, h);
    }
    this.mouth = svg('path', { fill: 'none', stroke: '#7a3a33', 'stroke-width': 3.6, 'stroke-linecap': 'round', d: 'M30,27 Q37,32 43,26' }, h);
  }
  // p: {x,y,f(acing),s(cale),torso,head, aF:[u,l], aB:[u,l], lF:[u,l], lB:[u,l], eyes(0..1), smile(0..1)}
  pose(p) {
    const O = this.o, s = (p.s || 1) * O.s, f = p.f || 1;
    this.g.setAttribute('transform', `translate(${p.x},${p.y}) scale(${f * s},${s})`);
    const tA = rad(p.torso || 0);
    const sh = [Math.sin(tA) * 185, -Math.cos(tA) * 185];
    const seg = (a, len, from) => [from[0] + Math.cos(rad(a)) * len, from[1] + Math.sin(rad(a)) * len];
    const line = (el, pts) => el.setAttribute('d', 'M' + pts.map(q => q[0].toFixed(1) + ',' + q[1].toFixed(1)).join(' L'));
    // torso + waist
    line(this.torso, [[Math.sin(tA) * 20, -Math.cos(tA) * 20], sh]);
    line(this.waist, [[0, 0], [Math.sin(tA) * 14, -Math.cos(tA) * 14]]);
    // legs
    const legs = (U, Lw, shoe, ang, off) => {
      const hip = [off, 0], knee = seg(ang[0], 150, hip), ank = seg(ang[1], 145, knee);
      line(U, [hip, knee]); line(Lw, [knee, ank]);
      const a = ank;
      shoe.setAttribute('d', `M${a[0] - 16},${a[1] - 6} Q${a[0] - 18},${a[1] + 16} ${a[0]},${a[1] + 16} L${a[0] + 40},${a[1] + 16} Q${a[0] + 50},${a[1] + 8} ${a[0] + 36},${a[1] - 2} Z`);
      return ank;
    };
    const ankF = legs(this.fLegU, this.fLegL, this.fShoe, p.lF || [90, 90], 8);
    const ankB = legs(this.bLegU, this.bLegL, this.bShoe, p.lB || [90, 90], -8);
    if (this.sarong) {
      const top = 4, bot = Math.max(ankF[1], ankB[1]) - 18;
      const xs = [ankF[0], ankB[0]];
      const xmin = Math.min(...xs) - 34, xmax = Math.max(...xs) + 34;
      this.sarong.setAttribute('d', `M-40,${-top} L40,${-top} L${xmax},${bot} Q${(xmin + xmax) / 2},${bot + 10} ${xmin},${bot} Z`);
      this.sarongStripe.setAttribute('d', `M${xmin + 6},${bot - 30} Q${(xmin + xmax) / 2},${bot - 22} ${xmax - 6},${bot - 30}`);
    }
    // neck + head
    const nk = [sh[0] + Math.sin(tA) * 26, sh[1] - Math.cos(tA) * 26];
    line(this.neck, [sh, nk]);
    const hc = [sh[0] + Math.sin(tA) * 70, sh[1] - Math.cos(tA) * 70];
    this.head.setAttribute('transform', `translate(${hc[0].toFixed(1)},${hc[1].toFixed(1)}) rotate(${(p.torso || 0) + (p.head || 0)})`);
    const eo = p.eyes == null ? 1 : p.eyes;
    this.eye.setAttribute('ry', (6.5 * eo).toFixed(2));
    this.eye.setAttribute('opacity', eo < 0.2 ? 0 : 1);
    this.eyeLid.setAttribute('opacity', eo < 0.2 ? 1 : 0);
    const sm = p.smile == null ? 0.6 : p.smile;
    this.mouth.setAttribute('d', `M30,27 Q37,${(27 + 9 * sm).toFixed(1)} 44,${(27 - 2 * sm).toFixed(1)}`);
    // arms
    const arm = (U, Fo, hand, ang, off) => {
      const s0 = [sh[0] + off, sh[1] + 10], el = seg(ang[0], 108, s0), wr = seg(ang[1], 100, el);
      line(U, [s0, el]); line(Fo, [el, wr]);
      setA(hand, { cx: wr[0].toFixed(1), cy: wr[1].toFixed(1) });
      return wr;
    };
    this.wristF = arm(this.fArmU, this.fArmF, this.fHand, p.aF || [95, 95], 6);
    this.wristB = arm(this.bArmU, this.bArmF, this.bHand, p.aB || [95, 95], -6);
    this.prop.setAttribute('transform', `translate(${this.wristF[0].toFixed(1)},${this.wristF[1].toFixed(1)}) rotate(${p.propRot || 0})`);
  }
}

// Front-facing round face (avatars, photos)
function faceFront(parent, cx, cy, r, o) {
  const g = svg('g', { transform: `translate(${cx},${cy})` }, parent);
  if (o.hairStyle === 'bun') svg('circle', { cx: 0, cy: -r * 0.95, r: r * 0.42, fill: o.hair }, g);
  if (o.hairStyle === 'bob') svg('path', { fill: o.hair, d: `M${-r * 1.08},${r * 0.55} C${-r * 1.2},${-r * 1.15} ${r * 1.2},${-r * 1.15} ${r * 1.08},${r * 0.55} Z` }, g);
  svg('circle', { cx: 0, cy: 0, r, fill: o.skin }, g);
  const fr = o.hairStyle === 'bob'
    ? `M${-r},${-r * 0.05} C${-r * 0.9},${-r * 1.15} ${r * 0.9},${-r * 1.15} ${r},${-r * 0.05} C${r * 0.4},${-r * 0.55} ${-r * 0.4},${-r * 0.55} ${-r},${-r * 0.05} Z`
    : `M${-r * 0.98},${-r * 0.1} C${-r * 0.9},${-r * 1.12} ${r * 0.9},${-r * 1.12} ${r * 0.98},${-r * 0.1} C${r * 0.5},${-r * 0.62} ${-r * 0.5},${-r * 0.62} ${-r * 0.98},${-r * 0.1} Z`;
  svg('path', { fill: o.hair, d: fr }, g);
  if (o.gray) svg('path', { fill: 'none', stroke: o.gray, 'stroke-width': r * 0.08, 'stroke-linecap': 'round', d: `M${-r * 0.55},${-r * 0.62} C${-r * 0.2},${-r * 0.85} ${r * 0.2},${-r * 0.85} ${r * 0.55},${-r * 0.62}` }, g);
  for (const sx of [-1, 1]) {
    svg('ellipse', { cx: sx * r * 0.36, cy: r * 0.08, rx: r * 0.085, ry: r * 0.12, fill: '#231d20' }, g);
    svg('circle', { cx: sx * r * 0.5, cy: r * 0.36, r: r * 0.16, fill: '#e98a86', opacity: 0.33 }, g);
  }
  if (o.glasses) for (const sx of [-1, 1]) svg('rect', { x: sx * r * 0.36 - r * 0.24, y: -r * 0.08, width: r * 0.48, height: r * 0.34, rx: r * 0.1, fill: 'none', stroke: '#3b3236', 'stroke-width': r * 0.05 }, g);
  svg('path', { fill: 'none', stroke: '#7a3a33', 'stroke-width': r * 0.07, 'stroke-linecap': 'round', d: `M${-r * 0.22},${r * 0.42} Q0,${r * 0.6} ${r * 0.22},${r * 0.42}` }, g);
  return g;
}

function shade(hex, amt) {
  const n = parseInt(hex.slice(1), 16);
  const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map(v => clamp(v + amt, 0, 255) | 0);
  return '#' + c.map(v => v.toString(16).padStart(2, '0')).join('');
}

// ---------- Subtitles ----------
// cues: [{a, b, parts:[{t, s}]}] where s is 'w' | 'y' | 'r'
function renderSubs(box, cues, t) {
  const cue = cues.find(c => t >= c.a && t < c.b);
  const key = cue ? cue.a : -1;
  if (box._key !== key) {
    box._key = key;
    box.innerHTML = '';
    if (cue) for (const p of cue.parts) html('span', 'sub-' + p.s, box, p.t);
  }
  if (cue) {
    const k = prog(t, cue.a, cue.a + 0.12);
    box.style.opacity = k;
    box.style.transform = `translateY(${(1 - k) * 10}px)`;
  } else box.style.opacity = 0;
}
