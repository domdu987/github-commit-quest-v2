// story2 character rig — chunky "sticker" chibi: big round head with a 3/4 face (two eyes, brows, nose, cheeks),
// short rounded torso, thick ink-outlined limbs, mitten hands, chunky shoes. Faces right; flip with f=-1.
// Same pose()/reach() API as demo/puppet.js, so the scenes drive it the same way.
const RIG = { T: 112, NECK: 10, R: 62, SH: 18, UARM: 76, FARM: 72, THIGH: 92, SHIN: 92 };
const LEG = RIG.THIGH + RIG.SHIN + 14;   // hip height above the ground when standing
const INK = '#33252a';

class Puppet {
  constructor(parent, o, defs) {
    this.o = o = Object.assign({
      R: RIG.R, skin: '#e2b08a', skinShade: '#c9926c', hair: '#3a2620', hairStyle: 'fluffy', gray: null,
      top: 'tee', shirt: '#4fa58f', shirtDark: '#3c8a76', shirtLight: '#69bba5', sleeve: 'short',
      pants: '#2f3a5c', pantsDark: '#262f4c', shoe: '#f4efe6', shoeDark: '#d6cfc2', sole: '#c94f45', shoeStyle: 'sneaker',
      mustache: false, aged: false, hat: null, towel: null, vest: null, flat: false, ink: INK, s: 1, seed: 1,
    }, o);
    const ink = o.ink, R = o.R;
    this.g = svg('g', {}, parent);
    const id = 'pq' + Math.random().toString(36).slice(2, 8);
    if (defs && !o.flat) {
      const lg = svg('linearGradient', { id: id + 'sh', x1: 0, y1: 0, x2: 1, y2: 0 }, defs);
      svg('stop', { offset: 0, 'stop-color': o.shirtDark }, lg);
      svg('stop', { offset: 0.5, 'stop-color': o.shirt }, lg);
      svg('stop', { offset: 1, 'stop-color': o.shirtLight }, lg);
      this.shirtFill = `url(#${id}sh)`;
    } else this.shirtFill = o.shirt;
    const ln = (g, c, w) => svg('path', { fill: 'none', stroke: c, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
    const fmt = q => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;
    // two-segment limb: both outlines first, then both fills, so the joint shows no seam
    const limb = (g, cU, cL, w) => {
      const uo = ln(g, ink, w + 9), lo = ln(g, ink, w + 9), u = ln(g, cU, w), l = ln(g, cL, w);
      return (a, b, c) => { const d1 = `M${fmt(a)} L${fmt(b)}`, d2 = `M${fmt(b)} L${fmt(c)}`; uo.setAttribute('d', d1); u.setAttribute('d', d1); lo.setAttribute('d', d2); l.setAttribute('d', d2); };
    };
    this.fmt = fmt;
    this.gArmB = svg('g', {}, this.g);
    this.gLegB = svg('g', {}, this.g);
    this.gLegF = svg('g', {}, this.g);
    this.gTorso = svg('g', {}, this.g);
    this.gHead = svg('g', {}, this.g);
    this.gArmF = svg('g', {}, this.g);
    // arms: long sleeves are shirt-coloured to the wrist; short sleeves / tank tops show skin with a sleeve stub
    const longS = o.sleeve === 'long';
    this.armB = limb(this.gArmB, longS ? o.shirtDark : o.skinShade, longS ? o.shirtDark : o.skinShade, 21);
    this.stubB = o.top === 'tank' || longS ? null : ln(this.gArmB, o.shirtDark, 30);
    this.hB = svg('circle', { r: 12.5, fill: o.skinShade, stroke: ink, 'stroke-width': 4.5 }, this.gArmB);
    // legs + shoes
    this.legB = limb(this.gLegB, o.pantsDark, o.pantsDark, 29);
    this.sB = svg('path', { fill: o.shoeStyle === 'sandal' ? o.skinShade : o.shoeDark, stroke: ink, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, this.gLegB);
    this.soleB = svg('path', { fill: 'none', stroke: o.flat ? o.shoe : o.sole, 'stroke-width': 5, 'stroke-linecap': 'round' }, this.gLegB);
    this.legF = limb(this.gLegF, o.pants, o.pants, 29);
    this.sF = svg('path', { fill: o.shoeStyle === 'sandal' ? o.skin : o.shoe, stroke: ink, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, this.gLegF);
    this.soleF = svg('path', { fill: 'none', stroke: o.flat ? o.shoe : o.sole, 'stroke-width': 5, 'stroke-linecap': 'round' }, this.gLegF);
    this.strapF = o.shoeStyle === 'sandal' ? ln(this.gLegF, o.sole, 6) : null;
    // torso
    if (o.top === 'hoodie') this.hood = svg('path', { fill: o.shirtDark, stroke: ink, 'stroke-width': 4.5, 'stroke-linejoin': 'round' }, this.gTorso);
    this.torsoG = svg('g', {}, this.gTorso);
    if (o.top === 'tank') this.chest = svg('path', { fill: o.skin, stroke: ink, 'stroke-width': 5, 'stroke-linejoin': 'round' }, this.torsoG);
    this.torso = svg('path', { fill: this.shirtFill, stroke: ink, 'stroke-width': 5, 'stroke-linejoin': 'round' }, this.torsoG);
    this.detail = svg('g', { display: o.flat ? 'none' : 'inline' }, this.torsoG);
    if (o.top === 'hoodie') {
      this.pocket = svg('path', { fill: o.shirtLight, stroke: ink, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, this.detail);
      this.strings = ln(this.detail, '#fff7ea', 4);
    }
    if (o.top === 'tee' || o.top === 'work') this.collar = ln(this.detail, o.shirtDark, 5);
    if (o.vest) {
      this.vestP = svg('path', { fill: o.vest, stroke: ink, 'stroke-width': 4, 'stroke-linejoin': 'round' }, this.detail);
      this.vestS = ln(this.detail, '#eef2f4', 7);
    }
    this.belt = ln(this.detail, shade(o.pants, -30), 6);
    if (o.towel) {
      this.towelBack = svg('path', { fill: shade(o.towel, -25), stroke: ink, 'stroke-width': 3.5 }, this.torsoG);
      this.towel = svg('path', { fill: o.towel, stroke: ink, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, this.torsoG);
      this.towelStripe = svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 3, opacity: 0.75 }, this.torsoG);
    }
    this.shoulderG = svg('g', {}, this.gTorso);
    // neck + head
    this.neckO = ln(this.gHead, ink, 31); this.neck = ln(this.gHead, o.skinShade, 22);
    this.head = svg('g', {}, this.gHead);
    this.buildHead();
    // front arm (drawn over everything)
    this.armF = limb(this.gArmF, longS ? o.shirt : o.skin, longS ? o.shirt : o.skin, 21);
    this.stubF = o.top === 'tank' || longS ? null : ln(this.gArmF, o.shirt, 30);
    this.cuff = longS && !o.flat ? svg('circle', { r: 10, fill: o.shirtLight, stroke: ink, 'stroke-width': 3.5 }, this.gArmF) : null;
    this.hF = svg('circle', { r: 13, fill: o.skin, stroke: ink, 'stroke-width': 4.5 }, this.gArmF);
    this.prop = svg('g', {}, this.gArmF);
    this.blinkSeed = rng(o.seed * 97 + 3);
    this.blinks = Array.from({ length: 40 }, (_, i) => i * 2.6 + this.blinkSeed() * 1.6);
  }
  buildHead() {
    const o = this.o, R = o.R, h = this.head, ink = o.ink;
    const hairStyle = o.hairStyle === 'fluffy' ? 'fluffy' : 'dad';
    // back hair: a cloud of circles, one ink pass under one colour pass so it reads as a single outlined shape
    if (hairStyle === 'fluffy' && !o.hat) {
      const puffs = [[-0.6, -0.42, 0.5], [-0.18, -0.76, 0.5], [0.3, -0.72, 0.44], [-0.84, 0.02, 0.36], [0.66, -0.46, 0.3]];
      for (const [x, y, r] of puffs) svg('circle', { cx: R * x, cy: R * y, r: R * r + 4.5, fill: ink }, h);
      for (const [x, y, r] of puffs) svg('circle', { cx: R * x, cy: R * y, r: R * r, fill: o.hair }, h);
    }
    if (hairStyle === 'dad' && !o.hat) svg('path', { fill: o.hair, stroke: ink, 'stroke-width': 4.5, d: `M${-R * 0.92},${R * 0.2} C${-R * 1.04},${-R * 0.95} ${R * 0.55},${-R * 1.2} ${R * 0.8},${-R * 0.5} L${R * 0.2},${-R * 0.4} Z` }, h);
    // ear (the visible one sits at the back of a 3/4 face)
    svg('ellipse', { cx: -R * 0.8, cy: R * 0.12, rx: R * 0.17, ry: R * 0.22, fill: o.skin, stroke: ink, 'stroke-width': 4 }, h);
    svg('path', { fill: 'none', stroke: o.skinShade, 'stroke-width': 3.5, 'stroke-linecap': 'round', d: `M${-R * 0.84},${R * 0.02} Q${-R * 0.74},${R * 0.12} ${-R * 0.82},${R * 0.24}` }, h);
    // face
    svg('ellipse', { cx: R * 0.04, cy: R * 0.03, rx: R * 0.9, ry: R * 0.92, fill: o.skin, stroke: ink, 'stroke-width': 5 }, h);
    svg('path', { fill: o.skinShade, opacity: 0.35, d: `M${-R * 0.7},${R * 0.3} C${-R * 0.5},${R * 0.85} ${R * 0.3},${R * 1.0} ${R * 0.7},${R * 0.55} C${R * 0.3},${R * 0.82} ${-R * 0.3},${R * 0.8} ${-R * 0.7},${R * 0.3} Z` }, h);
    // front hair
    if (hairStyle === 'fluffy' && !o.hat) {
      const bangs = `M${R * 0.92},${-R * 0.36} Q${R * 0.68},${-R * 0.5} ${R * 0.5},${-R * 0.3} Q${R * 0.36},${-R * 0.56} ${R * 0.1},${-R * 0.34} Q${-R * 0.1},${-R * 0.56} ${-R * 0.38},${-R * 0.3} Q${-R * 0.6},${-R * 0.28} ${-R * 0.9},${-R * 0.05}`;
      svg('path', { fill: o.hair, d: `M${-R * 0.9},${-R * 0.05} C${-R * 1.05},${-R * 1.15} ${R * 0.55},${-R * 1.4} ${R * 0.92},${-R * 0.36} ${bangs.slice(bangs.indexOf('Q'))} Z` }, h);
      svg('path', { fill: 'none', stroke: ink, 'stroke-width': 4.5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: bangs }, h);
      svg('path', { fill: 'none', stroke: shade(o.hair, 40), 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.8, d: `M${-R * 0.5},${-R * 0.7} Q${-R * 0.1},${-R * 0.92} ${R * 0.3},${-R * 0.8}` }, h);
      svg('path', { fill: o.hair, stroke: ink, 'stroke-width': 4, 'stroke-linejoin': 'round', d: `M${-R * 0.12},${-R * 0.92} C${-R * 0.2},${-R * 1.25} ${R * 0.2},${-R * 1.3} ${R * 0.18},${-R * 1.06} C${R * 0.1},${-R * 1.16} ${-R * 0.02},${-R * 1.1} ${R * 0.04},${-R * 0.92} Z` }, h);   // cowlick
    }
    if (hairStyle === 'dad' && !o.hat) {
      svg('path', { fill: o.hair, stroke: ink, 'stroke-width': 4.5, 'stroke-linejoin': 'round', d: `M${-R * 0.9},${R * 0.05} C${-R * 1.0},${-R * 1.1} ${R * 0.35},${-R * 1.32} ${R * 0.72},${-R * 0.58} Q${R * 0.3},${-R * 0.66} ${R * 0.02},${-R * 0.56} Q${-R * 0.4},${-R * 0.44} ${-R * 0.6},${R * 0.06} Z` }, h);
      if (o.gray) svg('path', { fill: 'none', stroke: o.gray, 'stroke-width': 5, 'stroke-linecap': 'round', d: `M${-R * 0.78},${-R * 0.2} Q${-R * 0.6},${-R * 0.62} ${-R * 0.2},${-R * 0.78} M${-R * 0.72},${R * 0.02} L${-R * 0.66},${-R * 0.22}` }, h);
    }
    // features (hidden for flat silhouettes)
    const fd = svg('g', { display: o.flat ? 'none' : 'inline' }, h);
    const browC = o.gray && o.aged ? shade(o.hair, -10) : o.hair, bw = o.mustache ? 7 : 5.5;
    this.browN = svg('path', { fill: 'none', stroke: browC, 'stroke-width': bw, 'stroke-linecap': 'round' }, fd);
    this.browF = svg('path', { fill: 'none', stroke: browC, 'stroke-width': bw, 'stroke-linecap': 'round' }, fd);
    const eye = (cx, cy, rx, ry) => {
      const g = svg('g', { transform: `translate(${cx},${cy})` }, fd);
      const open = svg('g', {}, g);
      svg('ellipse', { rx, ry, fill: '#2a1d21' }, open);
      svg('circle', { cx: rx * 0.35, cy: -ry * 0.38, r: rx * 0.42, fill: '#fff' }, open);
      svg('circle', { cx: -rx * 0.3, cy: ry * 0.42, r: rx * 0.18, fill: '#fff', opacity: 0.8 }, open);
      const closed = svg('path', { fill: 'none', stroke: '#2a1d21', 'stroke-width': 4.5, 'stroke-linecap': 'round', d: `M${-rx * 1.2},0 Q0,${ry * 0.75} ${rx * 1.2},0`, opacity: 0 }, g);
      return { g, open, closed };
    };
    this.eyeFar = eye(R * 0.02, -R * 0.05, R * 0.085, R * 0.13);
    this.eyeNear = eye(R * 0.5, -R * 0.05, R * 0.1, R * 0.145);
    this.eyeG = this.eyeNear.g;
    if (o.aged) svg('path', { fill: 'none', stroke: shade(o.skinShade, -18), 'stroke-width': 2.6, 'stroke-linecap': 'round', d: `M${R * 0.68},${-R * 0.1} l${R * 0.12},${-R * 0.06} M${R * 0.68},${-R * 0.0} l${R * 0.13},${R * 0.03} M${R * 0.08},${R * 0.3} q${R * 0.02},${R * 0.12} ${R * 0.1},${R * 0.2} M${R * 0.6},${R * 0.28} q${R * 0.0},${R * 0.12} ${-R * 0.06},${R * 0.2}` }, fd);
    for (const [cx, cy] of [[R * -0.02, R * 0.26], [R * 0.66, R * 0.24]]) svg('ellipse', { cx, cy, rx: R * 0.13, ry: R * 0.08, fill: '#f0857f', opacity: 0.42 }, fd);
    svg('path', { fill: 'none', stroke: shade(o.skinShade, -15), 'stroke-width': 4, 'stroke-linecap': 'round', d: `M${R * 0.26},${R * 0.08} Q${R * 0.32},${R * 0.2} ${R * 0.42},${R * 0.13}` }, fd);   // nose
    this.mx = R * 0.32; this.my = o.mustache ? R * 0.5 : R * 0.42;
    this.mouth = svg('path', { fill: 'none', stroke: '#6a2c2e', 'stroke-width': 4.5, 'stroke-linecap': 'round' }, fd);
    this.openM = svg('path', { fill: '#7a2f33', stroke: ink, 'stroke-width': 3.5, 'stroke-linejoin': 'round', opacity: 0 }, fd);
    this.teeth = svg('path', { fill: '#fff', opacity: 0 }, fd);
    if (o.mustache) {
      const mx = R * 0.33, my = R * 0.33, mc = o.gray ? '#6d6461' : o.hair;
      svg('path', { fill: mc, stroke: ink, 'stroke-width': 3.5, 'stroke-linejoin': 'round', d: `M${mx - R * 0.27},${my + R * 0.08} Q${mx - R * 0.22},${my - R * 0.1} ${mx},${my - R * 0.03} Q${mx + R * 0.22},${my - R * 0.1} ${mx + R * 0.27},${my + R * 0.08} Q${mx + R * 0.12},${my + R * 0.02} ${mx},${my + R * 0.06} Q${mx - R * 0.12},${my + R * 0.02} ${mx - R * 0.27},${my + R * 0.08} Z` }, fd);
    }
    if (o.hat === 'hardhat') {
      svg('path', { fill: o.flat ? o.shirt : '#f6c343', stroke: ink, 'stroke-width': 5, 'stroke-linejoin': 'round', d: `M${-R * 1.0},${-R * 0.26} C${-R * 1.02},${-R * 1.42} ${R * 1.0},${-R * 1.46} ${R * 1.02},${-R * 0.26} Z` }, h);
      if (!o.flat) {
        svg('path', { fill: 'none', stroke: '#dba22a', 'stroke-width': 6, 'stroke-linecap': 'round', d: `M${-R * 0.02},${-R * 1.2} C${R * 0.1},${-R * 0.9} ${R * 0.1},${-R * 0.6} ${R * 0.06},${-R * 0.32}` }, h);
        svg('path', { fill: 'none', stroke: '#fff6cf', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.7, d: `M${-R * 0.7},${-R * 0.6} C${-R * 0.6},${-R * 0.95} ${-R * 0.3},${-R * 1.12} ${-R * 0.05},${-R * 1.14}` }, h);
        svg('circle', { cx: -R * 0.48, cy: -R * 0.68, r: R * 0.15, fill: '#2f9e5b', stroke: ink, 'stroke-width': 3 }, h);
        svg('path', { fill: 'none', stroke: '#fff', 'stroke-width': 3.5, 'stroke-linecap': 'round', d: `M${-R * 0.48},${-R * 0.76} L${-R * 0.48},${-R * 0.6} M${-R * 0.56},${-R * 0.68} L${-R * 0.4},${-R * 0.68}` }, h);
      }
      svg('rect', { x: -R * 1.08, y: -R * 0.36, width: R * 2.5, height: 15, rx: 7.5, fill: o.flat ? o.shirt : '#e2a52c', stroke: ink, 'stroke-width': 4.5 }, h);
    }
  }
  // p: x,y (hip), f, s, torso(deg lean fwd), head(deg), aF/aB/lF/lB [upper, lower] absolute deg (90 = down),
  // eyes (0..1), smile (0..1), grin (0..1), t (for blinking & sway), armF/armB foreshortening, propRot
  pose(p) {
    const o = this.o, R = o.R, s = (p.s || 1) * o.s, f = p.f || 1, T = RIG.T;
    this.g.setAttribute('transform', `translate(${p.x.toFixed(1)},${p.y.toFixed(1)}) scale(${(f * s).toFixed(4)},${s.toFixed(4)})`);
    if (this.overlays) for (const u of this.overlays) u.setAttribute('transform', this.g.getAttribute('transform'));
    const ta = rad(p.torso || 0), sin = Math.sin(ta), cos = Math.cos(ta);
    const P = (x, y) => [x * cos - y * sin, x * sin + y * cos];
    const seg = (a, len, from) => [from[0] + Math.cos(rad(a)) * len, from[1] + Math.sin(rad(a)) * len];
    const fmt = this.fmt;
    const poly = pts => pts.map(q => fmt(q)).join(' ');
    // legs
    const leg = (set, shoe, sole, ang, off, strap) => {
      const hip = P(off, -4), knee = seg(ang[0], RIG.THIGH, hip), ank = seg(ang[1], RIG.SHIN, knee);
      set(hip, knee, ank);
      const [ax, ay] = ank;
      if (o.shoeStyle === 'sandal') {
        shoe.setAttribute('d', `M${ax - 12},${ay - 6} C${ax - 16},${ay + 8} ${ax - 8},${ay + 11} ${ax},${ay + 11} L${ax + 26},${ay + 11} C${ax + 36},${ay + 11} ${ax + 36},${ay + 1} ${ax + 22},${ay - 3} Z`);
        sole.setAttribute('d', `M${ax - 14},${ay + 14} L${ax + 36},${ay + 14}`);
        if (strap) strap.setAttribute('d', `M${ax + 4},${ay - 2} L${ax + 16},${ay + 10}`);
      } else {
        shoe.setAttribute('d', `M${ax - 16},${ay - 8} C${ax - 20},${ay + 10} ${ax - 12},${ay + 14} ${ax},${ay + 14} L${ax + 32},${ay + 14} C${ax + 46},${ay + 14} ${ax + 46},${ay - 2} ${ax + 26},${ay - 8} Z`);
        sole.setAttribute('d', `M${ax - 13},${ay + 10} L${ax + 38},${ay + 10}`);
      }
      return ank;
    };
    leg(this.legF, this.sF, this.soleF, p.lF || [90, 90], 8, this.strapF);
    leg(this.legB, this.sB, this.soleB, p.lB || [90, 90], -8, null);
    // torso: a rounded block, chest at +x
    const hem = 6, top = -T;
    const tp = [[-28, top], [-40, top + 4], [-42, top + 18], [-40, hem - 12], [-36, hem], [30, hem], [36, hem - 12], [36, top + 18], [32, top + 4], [22, top]].map(q => P(q[0], q[1]));
    this.torso.setAttribute('d', `M${fmt(tp[0])} Q${fmt(tp[1])} ${fmt(tp[2])} L${fmt(tp[3])} Q${fmt(tp[4])} ${fmt(P(-24, hem))} L${fmt(P(20, hem))} Q${fmt(tp[5])} ${fmt(tp[6])} L${fmt(tp[7])} Q${fmt(tp[8])} ${fmt(tp[9])} Z`);
    if (this.chest) {
      // tank top: skin shoulders, the vest-shaped top covers from the chest down
      this.chest.setAttribute('d', this.torso.getAttribute('d'));
      const k = [[-30, top + 2], [-20, top + 2], [-16, top + 40], [14, top + 40], [14, top + 2], [24, top + 2], [34, top + 30], [36, hem - 12], [30, hem], [-36, hem], [-40, hem - 12], [-40, top + 30]].map(q => P(q[0], q[1]));
      this.torso.setAttribute('d', `M${fmt(k[0])} L${fmt(k[1])} Q${fmt(P(-16, top + 24))} ${fmt(k[2])} Q${fmt(P(0, top + 52))} ${fmt(k[3])} Q${fmt(P(16, top + 24))} ${fmt(k[4])} L${fmt(k[5])} Q${fmt(P(32, top + 8))} ${fmt(k[6])} L${fmt(k[7])} Q${fmt(k[8])} ${fmt(P(20, hem))} L${fmt(P(-26, hem))} Q${fmt(k[9])} ${fmt(k[10])} L${fmt(k[11])} Q${fmt(P(-40, top + 6))} ${fmt(k[0])} Z`);
    }
    if (this.hood) this.hood.setAttribute('d', `M${fmt(P(-6, top + 6))} C${fmt(P(-12, top - 26))} ${fmt(P(-46, top - 22))} ${fmt(P(-48, top + 6))} C${fmt(P(-50, top + 26))} ${fmt(P(-36, top + 30))} ${fmt(P(-24, top + 22))} Z`);
    if (this.pocket) this.pocket.setAttribute('d', `M${fmt(P(-4, -44))} L${fmt(P(24, -44))} Q${fmt(P(32, -44))} ${fmt(P(32, -34))} L${fmt(P(32, -16))} L${fmt(P(-10, -16))} Z`);
    if (this.strings) this.strings.setAttribute('d', `M${fmt(P(14, top + 10))} L${fmt(P(16, top + 40))} M${fmt(P(24, top + 8))} L${fmt(P(27, top + 36))}`);
    if (this.collar) this.collar.setAttribute('d', `M${fmt(P(-14, top + 2))} Q${fmt(P(4, top + 22))} ${fmt(P(24, top + 4))}`);
    if (this.vestP) {
      const v = [[-36, top + 16], [-12, top + 4], [-8, top + 36], [8, top + 60], [10, hem - 2], [-38, hem - 2]].map(q => P(q[0], q[1]));
      this.vestP.setAttribute('d', `M${fmt(v[0])} Q${fmt(P(-34, top + 2))} ${fmt(v[1])} L${fmt(v[2])} Q${fmt(P(2, top + 50))} ${fmt(v[3])} L${fmt(v[4])} L${fmt(v[5])} Z`);
      this.vestS.setAttribute('d', `M${fmt(P(-38, -46))} L${fmt(P(8, -46))} M${fmt(P(-38, -24))} L${fmt(P(9, -24))}`);
    }
    this.belt.setAttribute('d', `M${fmt(P(-38, hem - 8))} L${fmt(P(32, hem - 8))}`);
    if (this.towel) {
      const q = v => fmt(P(v[0], v[1]));
      this.towelBack.setAttribute('d', `M${q([-34, top + 4])} Q${q([-4, top - 18])} ${q([26, top + 4])} L${q([22, top + 14])} Q${q([-4, top - 4])} ${q([-30, top + 14])} Z`);
      this.towel.setAttribute('d', `M${q([10, top - 2])} L${q([30, top + 6])} L${q([32, top + 66])} L${q([14, top + 68])} Z`);
      this.towelStripe.setAttribute('d', `M${q([16, top + 8])} L${q([19, top + 62])} M${q([24, top + 8])} L${q([26, top + 62])}`);
    }
    this.shoulderG.setAttribute('transform', `translate(${fmt(P(0, -T))}) rotate(${(p.torso || 0).toFixed(2)})`);
    // neck & head
    const nk = `M${fmt(P(0, -T + 6))} L${fmt(P(2, -T - RIG.NECK - 8))}`;
    this.neckO.setAttribute('d', nk); this.neck.setAttribute('d', nk);
    const hc = P(4, -T - RIG.NECK - R * 0.84);
    const ha = (p.torso || 0) + (p.head || 0);
    this.head.setAttribute('transform', `translate(${fmt(hc)}) rotate(${ha.toFixed(2)})`);
    // eyes blink automatically unless given
    let eo = p.eyes == null ? 1 : p.eyes;
    if (p.t != null && p.eyes == null) for (const b of this.blinks) if (p.t > b && p.t < b + 0.14) eo = 0;
    for (const e of [this.eyeFar, this.eyeNear]) { e.open.setAttribute('opacity', eo > 0.4 ? 1 : 0); e.closed.setAttribute('opacity', eo > 0.4 ? 0 : 1); }
    const sm = p.smile == null ? 0.5 : p.smile, gr = p.grin || 0;
    // brows: lift with a smile, knit when sad (smile < 0.2)
    const sad = clamp((0.25 - sm) * 4, 0, 1), lift = R * 0.04 * sm;
    this.browN.setAttribute('d', `M${R * 0.36},${-R * 0.3 - lift + sad * 4} Q${R * 0.5},${-R * 0.4 - lift} ${R * 0.66},${-R * 0.32 - lift - sad * 6}`);
    this.browF.setAttribute('d', `M${-R * 0.12},${-R * 0.32 - lift - sad * 6} Q${R * 0.02},${-R * 0.4 - lift} ${R * 0.16},${-R * 0.3 - lift + sad * 4}`);
    const mx = this.mx, my = this.my, w = R * 0.13;
    this.mouth.setAttribute('d', `M${mx - w},${my + sad * 4} Q${mx},${my + R * 0.16 * (sm - sad * 0.8)} ${mx + w},${my + sad * 4}`);
    this.mouth.setAttribute('opacity', gr > 0.5 ? 0 : 1);
    this.openM.setAttribute('d', `M${mx - w * 1.15},${my - 1} Q${mx},${my + R * 0.3} ${mx + w * 1.15},${my - 1} Z`);
    this.teeth.setAttribute('d', `M${mx - w},${my + 1} Q${mx},${my + 6} ${mx + w},${my + 1} L${mx + w * 0.9},${my - 1} L${mx - w * 0.9},${my - 1} Z`);
    this.openM.setAttribute('opacity', gr > 0.5 ? 1 : 0); this.teeth.setAttribute('opacity', gr > 0.5 ? 1 : 0);
    // arms
    const arm = (set, stub, hand, cuff, ang, off, k = 1) => {
      const s0 = P(off, -T + RIG.SH), el = seg(ang[0], RIG.UARM * k, s0), wr = seg(ang[1], RIG.FARM * k, el);
      set(s0, el, wr);
      if (stub) stub.setAttribute('d', `M${fmt(s0)} L${fmt(seg(ang[0], RIG.UARM * k * 0.42, s0))}`);
      setA(hand, { cx: wr[0].toFixed(1), cy: wr[1].toFixed(1) });
      if (cuff) setA(cuff, { cx: (wr[0] - Math.cos(rad(ang[1])) * 12).toFixed(1), cy: (wr[1] - Math.sin(rad(ang[1])) * 12).toFixed(1) });
      return wr;
    };
    this.wristF = arm(this.armF, this.stubF, this.hF, this.cuff, p.aF || [92, 92], 4, p.armF || 1);
    this.wristB = arm(this.armB, this.stubB, this.hB, null, p.aB || [92, 92], -6, p.armB || 1);
    this.prop.setAttribute('transform', `translate(${fmt(this.wristF)}) rotate(${p.propRot || 0})`);
    this.shoulder = P(0, -T);
  }
  // a live copy of the front arm drawn in another group (e.g. over a second character)
  armOverlay(parent) {
    if (!this.gArmF.id) this.gArmF.id = 'arm' + Math.random().toString(36).slice(2, 8);
    const u = svg('use', { href: '#' + this.gArmF.id }, parent);
    (this.overlays = this.overlays || []).push(u);
    return u;
  }
  // IK for the front arm: joint angles that put the wrist on world point (tx, ty)
  reach(p, tx, ty, elbowUp = false) {
    const s = (p.s || 1) * this.o.s, f = p.f || 1, T = RIG.T;
    const lx = (tx - p.x) / (f * s), ly = (ty - p.y) / s;
    const ta = rad(p.torso || 0);
    const sx = 4 * Math.cos(ta) - (-T + RIG.SH) * Math.sin(ta), sy = 4 * Math.sin(ta) + (-T + RIG.SH) * Math.cos(ta);
    const k = p.armF || 1, dx = lx - sx, dy = ly - sy, L1 = RIG.UARM * k, L2 = RIG.FARM * k;
    const d = Math.max(1e-3, Math.min(Math.hypot(dx, dy), L1 + L2 - 0.5));
    const base = Math.atan2(dy, dx);
    const a = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
    const up = elbowUp ? base - a : base + a;
    const ex = sx + Math.cos(up) * L1, ey = sy + Math.sin(up) * L1;
    const lo = Math.atan2(sy + Math.sin(base) * d - ey, sx + Math.cos(base) * d - ex);
    return [up * 180 / Math.PI, lo * 180 / Math.PI];
  }
}
// head-centre and ear positions in the torso frame (for scenes that aim a hand at the head)
const HEAD_C = [4, -RIG.T - RIG.NECK - RIG.R * 0.84];
const EAR_L = [HEAD_C[0] - RIG.R * 0.8, HEAD_C[1] + RIG.R * 0.12];

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
  const flat = Object.assign({}, o, { skin: c, skinShade: c, hair: c, gray: null, shirt: c, shirtLight: c, shirtDark: c, pants: c, pantsDark: c, shoe: c, shoeDark: c, sole: c, vest: o.vest ? c : null, towel: o.towel ? c : null, ink: c, flat: true });
  return new Puppet(g, flat, null);
}
