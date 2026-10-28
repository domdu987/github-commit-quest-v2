// Slender side-view puppet in the style of the reference clip: long thin limbs, long torso,
// big round head with almond eyes, hair cap + ponytail/bun/short spikes. Faces right; flip with f=-1.
class Puppet {
  constructor(parent, o, defs) {
    this.o = o = Object.assign({
      R: 44, skin: '#d6a780', skinShade: '#bf8f69', hair: '#241d1e', hairStyle: 'ponytail', hairTie: '#c9433c',
      shirt: '#e08477', shirtLight: '#ec978a', shirtDark: '#c96f63', sleeve: 'short', shirtLen: 'top',
      pants: '#2c3555', pantsDark: '#232a45', belt: '#1c2036', shoe: '#ece9e8', shoeDark: '#cfcaca',
      lashes: true, earring: '#f2c14e', glasses: false, gray: null, sarong: null, sarongDark: null, s: 1, seed: 1,
    }, o);
    this.g = svg('g', {}, parent);
    const id = 'pp' + Math.random().toString(36).slice(2, 8);
    if (defs) {
      const lg = svg('linearGradient', { id: id + 'sh', x1: 0, y1: 0, x2: 1, y2: 0 }, defs);
      svg('stop', { offset: 0, 'stop-color': o.shirtDark }, lg);
      svg('stop', { offset: 0.55, 'stop-color': o.shirt }, lg);
      svg('stop', { offset: 1, 'stop-color': o.shirtLight }, lg);
      this.shirtFill = `url(#${id}sh)`;
    } else this.shirtFill = o.shirt;
    const line = (g, c, w) => svg('path', { fill: 'none', stroke: c, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
    this.gArmB = svg('g', {}, this.g);
    this.gLegB = svg('g', {}, this.g);
    this.gLegF = svg('g', {}, this.g);
    this.gTorso = svg('g', {}, this.g);
    this.gHead = svg('g', {}, this.g);
    this.gArmF = svg('g', {}, this.g);
    const backSleeve = o.sleeve === 'long' ? o.shirtDark : o.skinShade;
    this.aBu = line(this.gArmB, o.shirtDark, 16);
    this.aBl = line(this.gArmB, backSleeve, 13);
    this.hB = svg('circle', { r: 8.5, fill: o.skinShade }, this.gArmB);
    this.lBu = line(this.gLegB, o.pantsDark, 23);
    this.lBl = line(this.gLegB, o.pantsDark, 20);
    this.sB = svg('path', { fill: o.shoeDark }, this.gLegB);
    this.lFu = line(this.gLegF, o.pants, 23);
    this.lFl = line(this.gLegF, o.pants, 20);
    this.sF = svg('path', { fill: o.shoe }, this.gLegF);
    this.sFsole = svg('path', { fill: 'none', stroke: o.shoeDark, 'stroke-width': 3 }, this.gLegF);
    if (o.sarong) {
      this.sar = svg('path', { fill: o.sarong }, this.gTorso);
      this.sarB = svg('path', { fill: 'none', stroke: o.sarongDark || shade(o.sarong, -20), 'stroke-width': 7, opacity: 0.9 }, this.gTorso);
      this.sarB2 = svg('path', { fill: 'none', stroke: o.sarongDark || shade(o.sarong, -20), 'stroke-width': 3, opacity: 0.9 }, this.gTorso);
    }
    if (o.backpack) this.pack = svg('path', { fill: o.backpack }, this.gTorso);
    this.torsoG = svg('g', {}, this.gTorso);
    this.torso = svg('path', { fill: this.shirtFill }, this.torsoG);
    this.torsoSeam = svg('path', { fill: 'none', stroke: o.shirtDark, 'stroke-width': 3, opacity: 0.55 }, this.torsoG);
    if (o.shirtLen === 'top' && !o.sarong) this.beltEl = svg('rect', { fill: o.belt, rx: 3 }, this.torsoG);
    if (o.pattern) { this.pat = svg('g', { opacity: 0.55 }, this.torsoG); }
    if (o.backpack) this.strap = svg('path', { fill: 'none', stroke: shade(o.backpack, -12), 'stroke-width': 8, 'stroke-linecap': 'round' }, this.torsoG);
    if (o.towel) {
      this.towelBack = svg('path', { fill: shade(o.towel, -25) }, this.torsoG);
      this.towel = svg('path', { fill: o.towel }, this.torsoG);
      this.towelStripe = svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 2.5, opacity: 0.6 }, this.torsoG);
    }
    this.shoulderG = svg('g', {}, this.gTorso);
    this.neck = line(this.gHead, o.skinShade, 15);
    this.head = svg('g', {}, this.gHead);
    this.buildHead();
    this.aFu = line(this.gArmF, o.sleeve === 'long' ? o.shirt : o.shirt, 16);
    this.aFl = line(this.gArmF, o.sleeve === 'long' ? o.shirt : o.skin, 13);
    this.cuff = o.sleeve === 'long' ? svg('circle', { r: 7.5, fill: o.shirtLight }, this.gArmF) : null;
    this.hF = svg('circle', { r: 9, fill: o.skin }, this.gArmF);
    this.prop = svg('g', {}, this.gArmF);
    this.blinkSeed = rng(o.seed * 97 + 3);
    this.blinks = Array.from({ length: 40 }, (_, i) => i * 2.6 + this.blinkSeed() * 1.6);
  }
  buildHead() {
    const o = this.o, R = o.R, h = this.head;
    // ponytail behind everything
    if (o.hairStyle === 'ponytail') {
      this.tail = svg('g', {}, h);
      svg('path', { fill: o.hair, d: `M${-R * 0.78},${-R * 0.2} C${-R * 1.25},${R * 0.6} ${-R * 1.0},${R * 1.9} ${-R * 0.95},${R * 2.9} C${-R * 0.88},${R * 3.1} ${-R * 0.78},${R * 3.0} ${-R * 0.76},${R * 2.8} C${-R * 0.72},${R * 1.8} ${-R * 0.75},${R * 0.7} ${-R * 0.46},${R * 0.05} Z` }, this.tail);
      svg('rect', { x: -R * 0.98, y: R * 0.28, width: R * 0.3, height: R * 0.16, rx: 3, fill: o.hairTie, transform: `rotate(-14 ${-R * 0.83} ${R * 0.36})` }, this.tail);
    }
    if (o.hairStyle === 'bun') svg('circle', { cx: -R * 0.78, cy: -R * 0.5, r: R * 0.42, fill: o.hair }, h);
    // back hair mass
    const cap = {
      ponytail: `M${R * 0.62},${-R * 0.62} C${R * 0.3},${-R * 1.1} ${-R * 0.75},${-R * 1.12} ${-R * 0.98},${-R * 0.25} C${-R * 1.05},${R * 0.15} ${-R * 0.9},${R * 0.5} ${-R * 0.62},${R * 0.62} L${-R * 0.3},${R * 0.22} C${-R * 0.2},${-R * 0.05} ${-R * 0.05},${-R * 0.35} ${R * 0.62},${-R * 0.62} Z`,
      short: `M${R * 0.66},${-R * 0.66} C${R * 0.35},${-R * 1.12} ${-R * 0.75},${-R * 1.15} ${-R * 1.0},${-R * 0.25} C${-R * 1.04},${R * 0.2} ${-R * 0.9},${R * 0.55} ${-R * 0.66},${R * 0.66} L${-R * 0.34},${R * 0.24} C${-R * 0.26},${-R * 0.05} ${-R * 0.08},${-R * 0.32} ${R * 0.36},${-R * 0.45} C${R * 0.5},${-R * 0.48} ${R * 0.6},${-R * 0.55} ${R * 0.66},${-R * 0.66} Z`,
      bun: `M${R * 0.6},${-R * 0.62} C${R * 0.3},${-R * 1.08} ${-R * 0.75},${-R * 1.1} ${-R * 0.96},${-R * 0.25} C${-R * 1.0},${R * 0.1} ${-R * 0.88},${R * 0.38} ${-R * 0.62},${R * 0.5} L${-R * 0.3},${R * 0.2} C${-R * 0.2},${-R * 0.05} ${-R * 0.05},${-R * 0.35} ${R * 0.6},${-R * 0.62} Z`,
    }[o.hairStyle];
    svg('path', { fill: o.hair, d: cap }, h);
    // face
    svg('path', { fill: o.skin, d: `M${-R * 0.62},${R * 0.1} C${-R * 0.7},${-R * 0.9} ${R * 0.85},${-R * 1.05} ${R * 0.98},${-R * 0.05} C${R * 1.02},${R * 0.55} ${R * 0.62},${R * 0.98} ${R * 0.05},${R * 0.98} C${-R * 0.45},${R * 0.98} ${-R * 0.6},${R * 0.6} ${-R * 0.62},${R * 0.1} Z` }, h);
    svg('path', { fill: o.hair, d: `M${R * 0.66},${-R * 0.66} C${R * 0.3},${-R * 1.04} ${-R * 0.5},${-R * 1.06} ${-R * 0.68},${-R * 0.3} C${-R * 0.4},${-R * 0.62} ${R * 0.15},${-R * 0.72} ${R * 0.66},${-R * 0.66} Z` }, h);
    if (o.hairStyle === 'short') {
      svg('path', { fill: o.hair, d: `M${-R * 0.25},${-R * 0.98} L${-R * 0.12},${-R * 1.22} L${R * 0.02},${-R * 1.0} L${R * 0.2},${-R * 1.18} L${R * 0.28},${-R * 0.92} Z` }, h);
    }
    if (o.gray) {
      for (const k of [0, 1]) svg('path', { fill: 'none', stroke: o.gray, 'stroke-width': 3.2, 'stroke-linecap': 'round', d: `M${-R * (0.62 - k * 0.2)},${-R * (0.62 + k * 0.1)} C${-R * (0.3 - k * 0.2)},${-R * (0.92 + k * 0.05)} ${R * 0.1},${-R * 0.95} ${R * (0.38 - k * 0.1)},${-R * 0.82}` }, h);
    }
    // ear + earring
    svg('ellipse', { cx: -R * 0.16, cy: R * 0.06, rx: R * 0.13, ry: R * 0.18, fill: o.skinShade }, h);
    svg('path', { fill: 'none', stroke: shade(o.skinShade, -25), 'stroke-width': 2, d: `M${-R * 0.2},${-R * 0.02} Q${-R * 0.1},${R * 0.05} ${-R * 0.18},${R * 0.14}` }, h);
    if (o.earring) svg('circle', { cx: -R * 0.15, cy: R * 0.3, r: 3.2, fill: o.earring }, h);
    // brow, eye, mouth (hidden for flat silhouettes)
    const fd = svg('g', { display: o.flat ? 'none' : 'inline' }, h);
    this.brow = svg('path', { fill: 'none', stroke: o.hair, 'stroke-width': 3, 'stroke-linecap': 'round', d: `M${R * 0.3},${-R * 0.36} Q${R * 0.46},${-R * 0.46} ${R * 0.64},${-R * 0.38}` }, fd);
    this.eyeG = svg('g', { transform: `translate(${R * 0.5},${-R * 0.12})` }, fd);
    this.eyeOpen = svg('g', {}, this.eyeG);
    svg('path', { fill: '#f7f1ec', d: 'M-9,1 Q0,-7 9,0 Q1,5 -9,1 Z' }, this.eyeOpen);
    svg('circle', { cx: 2.5, cy: -0.5, r: 4.4, fill: '#1e1718' }, this.eyeOpen);
    svg('circle', { cx: 3.6, cy: -1.8, r: 1.3, fill: '#fff' }, this.eyeOpen);
    svg('path', { fill: 'none', stroke: '#1e1718', 'stroke-width': o.lashes ? 3.2 : 2.6, 'stroke-linecap': 'round', d: o.lashes ? 'M-10,1 Q0,-8 10,0 L13,-3' : 'M-9,1 Q0,-7 9,0' }, this.eyeOpen);
    this.eyeClosed = svg('path', { fill: 'none', stroke: '#1e1718', 'stroke-width': 2.8, 'stroke-linecap': 'round', d: o.lashes ? 'M-9,0 Q0,5 10,0 L12,2' : 'M-9,0 Q0,5 9,0', opacity: 0 }, this.eyeG);
    if (o.glasses) {
      svg('rect', { x: R * 0.28, y: -R * 0.32, width: R * 0.5, height: R * 0.38, rx: 8, fill: 'rgba(255,255,255,0.14)', stroke: '#4a3c3a', 'stroke-width': 2.6 }, fd);
      svg('path', { fill: 'none', stroke: '#4a3c3a', 'stroke-width': 2.6, d: `M${R * 0.28},${-R * 0.16} L${-R * 0.12},${-R * 0.08}` }, fd);
    }
    svg('circle', { cx: R * 0.42, cy: R * 0.28, r: R * 0.14, fill: '#e58f86', opacity: 0.22 }, fd);
    if (o.mustache) svg('path', { fill: o.gray || o.hair, d: `M${R * 0.42},${R * 0.4} Q${R * 0.6},${R * 0.27} ${R * 0.82},${R * 0.36} Q${R * 0.64},${R * 0.47} ${R * 0.42},${R * 0.4} Z` }, fd);
    if (o.aged) svg('path', { fill: 'none', stroke: shade(o.skinShade, -20), 'stroke-width': 1.8, 'stroke-linecap': 'round', d: `M${R * 0.72},${-R * 0.02} l${R * 0.12},${-R * 0.05} M${R * 0.72},${R * 0.04} l${R * 0.12},${R * 0.03}` }, fd);
    this.mouth = svg('path', { fill: 'none', stroke: '#8a4a3c', 'stroke-width': 2.8, 'stroke-linecap': 'round' }, fd);
    this.teeth = svg('path', { fill: '#fff', opacity: 0 }, fd);
    if (o.hat === 'hardhat') {
      svg('path', { fill: '#f2c14e', d: `M${-R * 0.98},${-R * 0.3} C${-R * 0.95},${-R * 1.32} ${R * 0.98},${-R * 1.36} ${R * 1.02},${-R * 0.3} Z` }, h);
      svg('path', { fill: 'none', stroke: '#d9a530', 'stroke-width': 4, d: `M${-R * 0.1},${-R * 1.16} C${R * 0.05},${-R * 0.9} ${R * 0.06},${-R * 0.6} ${R * 0.02},${-R * 0.32}` }, h);
      svg('rect', { x: -R * 1.05, y: -R * 0.38, width: R * 2.45, height: 8, rx: 4, fill: '#e0ad38' }, h);
      svg('path', { fill: 'none', stroke: '#fff7d6', 'stroke-width': 3, opacity: 0.6, 'stroke-linecap': 'round', d: `M${-R * 0.62},${-R * 0.62} C${-R * 0.5},${-R * 0.98} ${-R * 0.2},${-R * 1.1} ${R * 0.1},${-R * 1.1}` }, h);
    }
  }
  // p: x,y (hip), f, s, torso(deg lean fwd), head(deg), aF/aB/lF/lB [upper, lower] absolute deg (90 = down),
  // eyes (0..1), smile (0..1), grin (0..1), t (for blinking & sway)
  pose(p) {
    const o = this.o, R = o.R, s = (p.s || 1) * o.s, f = p.f || 1, T = 150;
    this.g.setAttribute('transform', `translate(${p.x.toFixed(1)},${p.y.toFixed(1)}) scale(${(f * s).toFixed(4)},${s.toFixed(4)})`);
    if (this.overlays) for (const u of this.overlays) u.setAttribute('transform', this.g.getAttribute('transform'));
    const ta = rad(p.torso || 0), sin = Math.sin(ta), cos = Math.cos(ta);
    const P = (x, y) => [x * cos - y * sin, x * sin + y * cos]; // torso frame -> local
    const sh = P(0, -T);
    const L = (el, pts) => el.setAttribute('d', 'M' + pts.map(q => q[0].toFixed(1) + ',' + q[1].toFixed(1)).join(' L'));
    const seg = (a, len, from) => [from[0] + Math.cos(rad(a)) * len, from[1] + Math.sin(rad(a)) * len];
    // legs
    const leg = (U, Lw, shoe, sole, ang, off) => {
      const hip = P(off, 0), knee = seg(ang[0], 150, hip), ank = seg(ang[1], 148, knee);
      L(U, [hip, knee]); L(Lw, [knee, ank]);
      const [ax, ay] = ank;
      shoe.setAttribute('d', `M${ax - 13},${ay - 4} C${ax - 15},${ay + 11} ${ax - 8},${ay + 13} ${ax},${ay + 13} L${ax + 30},${ay + 13} C${ax + 40},${ay + 13} ${ax + 40},${ay + 1} ${ax + 26},${ay - 3} Z`);
      if (sole) sole.setAttribute('d', `M${ax - 12},${ay + 10} L${ax + 34},${ay + 10}`);
      return ank;
    };
    const aF = leg(this.lFu, this.lFl, this.sF, this.sFsole, p.lF || [90, 90], 4);
    const aB = leg(this.lBu, this.lBl, this.sB, null, p.lB || [90, 90], -4);
    // torso polygon in torso frame (shoulder at y=-T, hip at 0)
    const long = o.shirtLen === 'long';
    const hem = long ? 26 : 4;
    const pts = [[-17, -T - 2], [15, -T - 2], [20, -T * 0.55], [long ? 25 : 20, hem], [long ? -27 : -22, hem + 2], [-24, -T * 0.45]];
    const w = pts.map(q => P(q[0], q[1]));
    this.torso.setAttribute('d', `M${w[0]} Q${P(4, -T - 10)} ${w[1]} L${w[2]} L${w[3]} L${w[4]} L${w[5]} Z`.replace(/(-?\d+\.\d+)\d*/g, '$1'));
    this.torsoSeam.setAttribute('d', `M${P(-6, -T + 6)} L${P(-9, hem - 4)}`);
    if (this.pack) {
      const q = [[-64, -T + 14], [-16, -T + 6], [-14, -36], [-66, -30]].map(v => P(v[0], v[1]));
      this.pack.setAttribute('d', `M${q[0]} Q${P(-40, -T - 4)} ${q[1]} L${q[2]} Q${P(-40, -22)} ${q[3]} Z`);
      this.strap.setAttribute('d', `M${P(-10, -T + 6)} Q${P(12, -T + 40)} ${P(6, -T + 96)}`);
    }
    if (this.beltEl) {
      const c = P(-1, -2);
      setA(this.beltEl, { x: -23, y: -6, width: 44, height: 8, transform: `translate(${c[0].toFixed(1)},${c[1].toFixed(1)}) rotate(${(p.torso || 0).toFixed(2)})` });
    }
    if (this.sar) {
      const hemY = Math.max(aF[1], aB[1]) - 6;
      const xs = [aF[0], aB[0]], x0 = Math.min(...xs) - 30, x1 = Math.max(...xs) + 34;
      const top = P(0, -6);
      this.sar.setAttribute('d', `M${top[0] - 26},${top[1]} L${top[0] + 24},${top[1]} L${x1},${hemY} Q${(x0 + x1) / 2},${hemY + 8} ${x0},${hemY} Z`);
      this.sarB.setAttribute('d', `M${x0 + 4},${hemY - 18} Q${(x0 + x1) / 2},${hemY - 12} ${x1 - 4},${hemY - 18}`);
      this.sarB2.setAttribute('d', `M${x0 + 2},${hemY - 34} Q${(x0 + x1) / 2},${hemY - 28} ${x1 - 2},${hemY - 34}`);
    }
    if (this.towel) {
      const q = v => P(v[0], v[1]);
      this.towelBack.setAttribute('d', `M${q([-20, -T + 2])} Q${q([0, -T - 14])} ${q([20, -T + 2])} L${q([16, -T + 10])} Q${q([0, -T - 2])} ${q([-16, -T + 10])} Z`);
      this.towel.setAttribute('d', `M${q([6, -T - 2])} L${q([20, -T + 4])} L${q([22, -T + 62])} L${q([10, -T + 64])} Z`);
      this.towelStripe.setAttribute('d', `M${q([10, -T + 6])} L${q([14, -T + 58])} M${q([16, -T + 6])} L${q([19, -T + 58])}`);
    }
    this.shoulderG.setAttribute('transform', `translate(${P(0, -T).map(v => v.toFixed(1)).join(',')}) rotate(${(p.torso || 0).toFixed(2)})`);
    // neck & head
    const nk0 = P(0, -T - 2), nk1 = P(1, -T - 26);
    L(this.neck, [nk0, nk1]);
    const hc = P(4, -T - 26 - R * 0.9);
    const ha = (p.torso || 0) + (p.head || 0);
    this.head.setAttribute('transform', `translate(${hc[0].toFixed(1)},${hc[1].toFixed(1)}) rotate(${ha.toFixed(2)})`);
    if (this.tail) this.tail.setAttribute('transform', `rotate(${(-ha * 0.6 + Math.sin((p.t || 0) * 1.7) * 2.5).toFixed(2)} ${-R * 0.7} ${-R * 0.1})`);
    // eyes: blink automatically unless eyes given
    let eo = p.eyes == null ? 1 : p.eyes;
    if (p.t != null && p.eyes == null) for (const b of this.blinks) if (p.t > b && p.t < b + 0.14) eo = 0;
    this.eyeOpen.setAttribute('opacity', eo > 0.4 ? 1 : 0);
    this.eyeClosed.setAttribute('opacity', eo > 0.4 ? 0 : 1);
    const sm = p.smile == null ? 0.5 : p.smile, gr = p.grin || 0;
    const mx = R * 0.66, my = R * 0.5;
    this.mouth.setAttribute('d', `M${mx - 9},${my} Q${mx},${my + 7 * sm} ${mx + 8},${my - 3 * sm}`);
    this.teeth.setAttribute('d', `M${mx - 8},${my + 0.5} Q${mx},${my + 9} ${mx + 7},${my - 1} Q${mx},${my + 3} ${mx - 8},${my + 0.5} Z`);
    this.teeth.setAttribute('opacity', gr);
    // arms
    const arm = (U, Lo, hand, cuff, ang, off, k = 1) => {  // k < 1 foreshortens an arm reaching around someone
      const s0 = P(off, -T + 12), el = seg(ang[0], 112 * k, s0), wr = seg(ang[1], 104 * k, el);
      L(U, [s0, el]); L(Lo, [el, wr]);
      setA(hand, { cx: wr[0].toFixed(1), cy: wr[1].toFixed(1) });
      if (cuff) setA(cuff, { cx: (wr[0] - Math.cos(rad(ang[1])) * 8).toFixed(1), cy: (wr[1] - Math.sin(rad(ang[1])) * 8).toFixed(1) });
      return wr;
    };
    this.wristF = arm(this.aFu, this.aFl, this.hF, this.cuff, p.aF || [92, 92], 3, p.armF || 1);
    this.wristB = arm(this.aBu, this.aBl, this.hB, null, p.aB || [92, 92], -3, p.armB || 1);
    this.prop.setAttribute('transform', `translate(${this.wristF[0].toFixed(1)},${this.wristF[1].toFixed(1)}) rotate(${p.propRot || 0})`);
    this.shoulder = sh;
  }
  // a live copy of the front arm drawn in another group (e.g. over a second character during a hug)
  armOverlay(parent) {
    if (!this.gArmF.id) this.gArmF.id = 'arm' + Math.random().toString(36).slice(2, 8);
    const u = svg('use', { href: '#' + this.gArmF.id }, parent);
    (this.overlays = this.overlays || []).push(u);
    return u;
  }
  // world <-> local helpers for IK
  reach(p, tx, ty, elbowUp = false) {
    const s = (p.s || 1) * this.o.s, f = p.f || 1, T = 150;
    const lx = (tx - p.x) / (f * s), ly = (ty - p.y) / s;
    const ta = rad(p.torso || 0);
    const sx = 3 * Math.cos(ta) - (-T + 12) * Math.sin(ta), sy = 3 * Math.sin(ta) + (-T + 12) * Math.cos(ta);
    const k = p.armF || 1, dx = lx - sx, dy = ly - sy, L1 = 112 * k, L2 = 104 * k;
    const d = Math.min(Math.hypot(dx, dy), L1 + L2 - 0.5);
    const base = Math.atan2(dy, dx);
    const a = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
    const up = elbowUp ? base - a : base + a;
    const ex = sx + Math.cos(up) * L1, ey = sy + Math.sin(up) * L1;
    const lo = Math.atan2(sy + Math.sin(base) * d - ey, sx + Math.cos(base) * d - ex);
    return [up * 180 / Math.PI, lo * 180 / Math.PI];
  }
}

// soft contact shadow under a character or object
function contactShadow(parent, defs, cx, cy, rx, ry, op = 0.35) {
  const id = 'cs' + Math.random().toString(36).slice(2, 7);
  const g = svg('radialGradient', { id }, defs);
  svg('stop', { offset: 0, 'stop-color': '#000', 'stop-opacity': op }, g);
  svg('stop', { offset: 1, 'stop-color': '#000', 'stop-opacity': 0 }, g);
  return svg('ellipse', { cx, cy, rx, ry, fill: `url(#${id})` }, parent);
}

// Walk/run cycle for Puppet.pose. ph in radians; returns limb angles plus hip bob and torso lean.
function gait(ph, amp = 22, run = 0) {
  const leg = p => {
    const th = amp * Math.sin(p);
    const flex = 6 + (36 + 34 * run) * Math.pow(Math.max(0, Math.cos(p)), 1.5);
    return [90 - th, 90 - th + flex];
  };
  const arm = p => {
    const a = 90 + (14 + 22 * run) * Math.sin(p);
    return [a, a - 14 - 50 * run];
  };
  return {
    lF: leg(ph), lB: leg(ph + Math.PI), aF: arm(ph), aB: arm(ph + Math.PI),
    bob: -(4 + 6 * run) * Math.cos(2 * ph), torso: 3 + 9 * run,
  };
}
// Ground shadow cast by a puppet: a flat copy squashed onto the ground plane and skewed away from the light.
function castShadow(parent, defs, o, groundY, skew = -55, squash = 0.26, op = 0.3, blurPx = 3) {
  const g = svg('g', { opacity: op, transform: `translate(0,${groundY}) scale(1,${-squash}) skewX(${skew}) translate(0,${-groundY})` }, parent);
  if (blurPx) g.setAttribute('filter', blurFilter(defs, blurPx));
  const c = '#3b1f14';
  const flat = Object.assign({}, o, { skin: c, skinShade: c, hair: c, gray: null, shirt: c, shirtLight: c, shirtDark: c, sarong: o.sarong ? c : null, sarongDark: c, pants: c, pantsDark: c, shoe: c, shoeDark: c, belt: c, backpack: o.backpack ? c : null, glasses: false, earring: null, flat: true, hairTie: c });
  return new Puppet(g, flat, null);
}
