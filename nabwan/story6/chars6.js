// "4,380 วันที่รอ" cast: the owner (short bob, office blouse / home tee) in the story2 chibi rig, and ลูกชิ้น the dog —
// a tan Thai street dog drawn in the same chunky sticker style, posable as sit / lie / stand / run / jump.
const OWNER = { skin: '#f0c09a', skinShade: '#d8a27c', hair: '#3a2622', hairStyle: 'bob', clip: '#f2c14e', top: 'office', sleeve: 'long', shirt: '#f6e3b4', shirtDark: '#e2c98e', shirtLight: '#fff4d6', lanyard: '#4a7bd8', pants: '#3b3f58', pantsDark: '#30344a', shoe: '#2e2b33', shoeDark: '#24212a', sole: '#4a4552', lashes: true, lips: '#c0505a', seed: 31 };
const OWNER_HOME = Object.assign({}, OWNER, { top: 'tee', sleeve: 'short', shirt: '#f08a7a', shirtDark: '#d86e60', shirtLight: '#f7aca0', pants: '#7a86a8', pantsDark: '#66718f', shoeStyle: 'sandal', sole: '#f2a0b6' });

function heartPathT(cx, cy, r) { return `M${cx},${cy + r * 0.9} C${cx - r * 1.6},${cy - r * 0.1} ${cx - r * 0.7},${cy - r * 1.3} ${cx},${cy - r * 0.35} C${cx + r * 0.7},${cy - r * 1.3} ${cx + r * 1.6},${cy - r * 0.1} ${cx},${cy + r * 0.9} Z`; }

// capsule limb: ink outline + fur fill, updated with set(x1,y1,x2,y2)
function dogLimb(parent, color, w) {
  const o = svg('path', { fill: 'none', stroke: INK, 'stroke-width': w + 9, 'stroke-linecap': 'round' }, parent);
  const i = svg('path', { fill: 'none', stroke: color, 'stroke-width': w, 'stroke-linecap': 'round' }, parent);
  return v => {
    const on = !!v; o.setAttribute('display', on ? 'inline' : 'none'); i.setAttribute('display', on ? 'inline' : 'none');
    if (!on) return;
    const d = `M${v[0].toFixed(1)},${v[1].toFixed(1)} L${v[2].toFixed(1)},${v[3].toFixed(1)}`; o.setAttribute('d', d); i.setAttribute('d', d);
  };
}

class Luukchin {
  constructor(parent, o = {}) {
    this.o = o = Object.assign({ fur: '#dba468', furDark: '#bf8650', furLight: '#f6dcb4', collar: '#e0574b', old: false }, o);
    const ink = INK, sw = 5;
    this.g = svg('g', {}, parent);
    this.shadow = svg('ellipse', { cx: 0, cy: 2, rx: 80, ry: 12, fill: '#000', opacity: 0.18 }, this.g);
    this.body = svg('g', {}, this.g);
    // tail (behind everything)
    this.tail = svg('g', {}, this.body);
    svg('path', { d: 'M4,4 C-18,-6 -34,-34 -26,-62 C-22,-76 -6,-74 -10,-60 C-16,-38 -4,-18 14,-6 Z', fill: o.fur, stroke: ink, 'stroke-width': sw, 'stroke-linejoin': 'round' }, this.tail);
    svg('path', { d: 'M-24,-58 C-22,-68 -12,-70 -12,-62', fill: 'none', stroke: o.furLight, 'stroke-width': 5, 'stroke-linecap': 'round' }, this.tail);
    // far legs
    this.legFarB = dogLimb(this.body, o.furDark, 22); this.legFarF = dogLimb(this.body, o.furDark, 22);
    // torso shapes for each posture
    this.sitT = svg('g', {}, this.body);
    svg('ellipse', { cx: -26, cy: -40, rx: 46, ry: 40, fill: o.fur, stroke: ink, 'stroke-width': sw }, this.sitT);
    svg('ellipse', { cx: 6, cy: -80, rx: 36, ry: 62, fill: o.fur, stroke: ink, 'stroke-width': sw, transform: 'rotate(-16 6 -80)' }, this.sitT);
    svg('ellipse', { cx: 24, cy: -84, rx: 15, ry: 36, fill: o.furLight, transform: 'rotate(-16 24 -84)' }, this.sitT);
    svg('ellipse', { cx: -2, cy: -6, rx: 28, ry: 11, fill: o.fur, stroke: ink, 'stroke-width': sw }, this.sitT);
    this.standT = svg('g', {}, this.body);
    svg('ellipse', { cx: 0, cy: -78, rx: 74, ry: 38, fill: o.fur, stroke: ink, 'stroke-width': sw }, this.standT);
    svg('ellipse', { cx: 10, cy: -62, rx: 48, ry: 15, fill: o.furLight }, this.standT);
    this.lieT = svg('g', {}, this.body);
    svg('ellipse', { cx: -12, cy: -34, rx: 76, ry: 32, fill: o.fur, stroke: ink, 'stroke-width': sw }, this.lieT);
    svg('ellipse', { cx: -44, cy: -22, rx: 34, ry: 22, fill: o.fur, stroke: ink, 'stroke-width': sw }, this.lieT);
    svg('ellipse', { cx: 6, cy: -18, rx: 44, ry: 10, fill: o.furLight }, this.lieT);
    // near legs
    this.legNearB = dogLimb(this.body, o.fur, 22); this.legNearF = dogLimb(this.body, o.fur, 22);
    this.legNearF2 = dogLimb(this.body, o.fur, 22);
    // collar + tag, then the head
    this.collar = svg('g', {}, this.body);
    svg('rect', { x: -26, y: -8, width: 52, height: 16, rx: 8, fill: o.collar, stroke: ink, 'stroke-width': 4 }, this.collar);
    svg('circle', { cx: 6, cy: 14, r: 8, fill: '#f2c14e', stroke: ink, 'stroke-width': 3 }, this.collar);
    this.head = svg('g', {}, this.body);
    this.earFar = svg('g', {}, this.head);
    svg('path', { d: 'M-10,4 L2,-48 L24,-4 Z', fill: o.furDark, stroke: ink, 'stroke-width': sw, 'stroke-linejoin': 'round' }, this.earFar);
    svg('ellipse', { cx: 0, cy: 0, rx: 48, ry: 43, fill: o.fur, stroke: ink, 'stroke-width': sw }, this.head);
    svg('path', { d: 'M-40,14 C-30,36 10,44 30,30', fill: 'none', stroke: o.furDark, 'stroke-width': 4, opacity: 0.35 }, this.head);
    this.earNear = svg('g', {}, this.head);
    svg('path', { d: 'M-12,4 L2,-52 L26,-6 Z', fill: o.fur, stroke: ink, 'stroke-width': sw, 'stroke-linejoin': 'round' }, this.earNear);
    svg('path', { d: 'M-2,-6 L4,-34 L14,-8 Z', fill: '#f4b7a8' }, this.earNear);
    svg('ellipse', { cx: 34, cy: 12, rx: 27, ry: 19, fill: o.furLight, stroke: ink, 'stroke-width': 4 }, this.head);
    if (o.old) {
      svg('ellipse', { cx: 34, cy: 14, rx: 22, ry: 14, fill: '#e4ded6' }, this.head);
      for (const ex of [-6, 20]) svg('path', { d: `M${ex - 8},-24 l6,-4 l6,4 l6,-4`, fill: 'none', stroke: '#e8e2da', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, this.head);
    }
    svg('ellipse', { cx: 57, cy: 2, rx: 10, ry: 8, fill: '#2a1d21' }, this.head);
    svg('ellipse', { cx: 54, cy: -1, rx: 3, ry: 2, fill: '#fff', opacity: 0.8 }, this.head);
    const eye = (cx, cy, rx, ry) => {
      const open = svg('g', {}, this.head);
      svg('ellipse', { cx, cy, rx, ry, fill: '#2a1d21' }, open);
      svg('circle', { cx: cx + rx * 0.35, cy: cy - ry * 0.4, r: rx * 0.45, fill: '#fff' }, open);
      const shut = svg('path', { d: `M${cx - rx * 1.3},${cy} Q${cx},${cy + ry} ${cx + rx * 1.3},${cy}`, fill: 'none', stroke: '#2a1d21', 'stroke-width': 4, 'stroke-linecap': 'round' }, this.head);
      const happy = svg('path', { d: `M${cx - rx * 1.3},${cy + 2} Q${cx},${cy - ry * 1.2} ${cx + rx * 1.3},${cy + 2}`, fill: 'none', stroke: '#2a1d21', 'stroke-width': 4.5, 'stroke-linecap': 'round' }, this.head);
      return { open, shut, happy };
    };
    this.eyes = [eye(-4, -8, 6, 8), eye(22, -8, 7, 9)];
    this.brows = svg('path', { fill: 'none', stroke: o.furDark, 'stroke-width': 4, 'stroke-linecap': 'round' }, this.head);
    for (const [cx, cy] of [[-14, 10], [26, 26]]) svg('ellipse', { cx, cy, rx: 9, ry: 5, fill: '#f0857f', opacity: 0.45 }, this.head);
    this.mouth = svg('path', { d: 'M56,10 Q52,22 42,20 M56,10 Q60,22 68,18', fill: 'none', stroke: '#2a1d21', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, this.head);
    this.mouthOpen = svg('g', {}, this.head);
    svg('path', { d: 'M40,16 Q54,42 70,14 Q56,22 40,16 Z', fill: '#7a2f33', stroke: ink, 'stroke-width': 3.5, 'stroke-linejoin': 'round' }, this.mouthOpen);
    this.tongue = svg('path', { d: 'M48,24 Q50,44 58,44 Q66,44 64,26 Z', fill: '#f07a8a', stroke: ink, 'stroke-width': 3 }, this.mouthOpen);
    this.blinkT = Array.from({ length: 30 }, (_, i) => i * 2.9 + (i * 1.37) % 1.2);
  }
  // p: x, y (ground), s, f (1 faces right), mode 'sit'|'stand'|'run'|'lie'|'jump', t, wag (0..1), perk (0 droop..1 up),
  //    tilt (deg head), look (deg head lift), eyes 'open'|'shut'|'happy', mouth 0..1, ph (gait phase), rot (body deg)
  pose(p) {
    const s = p.s || 1, f = p.f || 1, t = p.t || 0, mode = p.mode || 'sit';
    this.g.setAttribute('transform', `translate(${p.x.toFixed(1)},${p.y.toFixed(1)}) scale(${(f * s).toFixed(4)},${s.toFixed(4)})`);
    this.body.setAttribute('transform', `rotate(${(p.rot || 0).toFixed(2)} 0 -60)`);
    this.sitT.setAttribute('display', mode === 'sit' ? 'inline' : 'none');
    this.standT.setAttribute('display', mode === 'stand' || mode === 'run' || mode === 'jump' ? 'inline' : 'none');
    this.lieT.setAttribute('display', mode === 'lie' ? 'inline' : 'none');
    const wag = p.wag == null ? 0.5 : p.wag, perk = p.perk == null ? 1 : p.perk;
    let head, tailB, tailA, legs;
    const breathe = Math.sin(t * 2.2) * 1.5;
    if (mode === 'sit') {
      head = [22, -142 + breathe]; tailB = [-62, -16]; tailA = 20;
      legs = { nf: [30, -62, 34, -6], nf2: null, ff: [12, -60, 14, -6], nb: null, fb: null };
    } else if (mode === 'lie') {
      head = [76, -52 + breathe * 0.6]; tailB = [-84, -20]; tailA = 70;
      legs = { nf: [40, -16, 100, -10], nf2: [30, -10, 92, -4], ff: null, nb: null, fb: null };
    } else {
      const run = mode === 'run' ? 1 : 0, ph = p.ph || 0, amp = mode === 'run' ? 34 : (mode === 'jump' ? 0 : 6 * Math.sin(ph));
      const sw = a => mode === 'run' ? 34 * Math.sin(a) : (mode === 'jump' ? 0 : 0);
      const leg = (hx, hy, ang, len = 66) => [hx, hy, hx + Math.sin(rad(ang)) * len, hy + Math.cos(rad(ang)) * len];
      const bob = run ? -Math.abs(Math.sin(ph)) * 10 : 0;
      head = [66, -116 + bob + breathe]; tailB = [-70, -92 + bob]; tailA = run ? -40 : -20;
      if (mode === 'jump') legs = { nf: leg(44, -76, 125), ff: leg(36, -78, 110), nb: leg(-46, -72, -40), fb: leg(-40, -74, -25), nf2: null };
      else legs = { nf: leg(44, -70 + bob, sw(ph)), ff: leg(34, -72 + bob, sw(ph + Math.PI)), nb: leg(-46, -66 + bob, sw(ph + Math.PI)), fb: leg(-38, -68 + bob, sw(ph)), nf2: null };
      this.standT.setAttribute('transform', `translate(0,${bob.toFixed(1)})`);
    }
    this.legNearF(legs.nf); this.legFarF(legs.ff); this.legNearB(legs.nb); this.legFarB(legs.fb); this.legNearF2(legs.nf2);
    const wagA = Math.sin(t * (6 + 12 * wag)) * (8 + 26 * wag);
    this.tail.setAttribute('transform', `translate(${tailB[0]},${tailB[1]}) rotate(${(tailA + wagA).toFixed(1)})`);
    const tilt = (p.tilt || 0) + (p.look || 0);
    this.head.setAttribute('transform', `translate(${head[0]},${head[1]}) rotate(${tilt.toFixed(2)})`);
    this.collar.setAttribute('transform', `translate(${(head[0] - 12).toFixed(1)},${(head[1] + 40).toFixed(1)}) rotate(${(mode === 'lie' ? -10 : -24)})`);
    const ea = lerp(70, 0, perk);
    this.earNear.setAttribute('transform', `translate(-12,-30) rotate(${(-ea + Math.sin(t * 3) * 2).toFixed(1)})`);
    this.earFar.setAttribute('transform', `translate(-36,-20) rotate(${(-ea * 0.7 - 16).toFixed(1)})`);
    let ey = p.eyes || 'open';
    if (ey === 'open') for (const b of this.blinkT) if (t > b && t < b + 0.13) ey = 'shut';
    for (const e of this.eyes) { e.open.setAttribute('opacity', ey === 'open' ? 1 : 0); e.shut.setAttribute('opacity', ey === 'shut' ? 1 : 0); e.happy.setAttribute('opacity', ey === 'happy' ? 1 : 0); }
    const sad = p.sad || 0;
    this.brows.setAttribute('d', `M-12,${-24 + sad * 2} Q-4,${-30 + sad * 4} 4,${-26 - sad * 6} M14,${-26 - sad * 6} Q22,${-32 + sad * 4} 30,${-26 + sad * 2}`);
    this.brows.setAttribute('opacity', sad > 0.05 ? 1 : 0);
    const mo = p.mouth || 0;
    this.mouth.setAttribute('opacity', mo > 0.5 ? 0 : 1); this.mouthOpen.setAttribute('opacity', mo > 0.5 ? 1 : 0);
    this.tongue.setAttribute('transform', `translate(0,${(Math.sin(t * 9) * 2 * mo).toFixed(1)})`);
    this.shadow.setAttribute('rx', mode === 'lie' ? 110 : (mode === 'sit' ? 70 : 84));
    this.shadow.setAttribute('opacity', mode === 'jump' ? 0.08 : 0.18);
  }
}

// front-facing dog head (avatars, the title card, the "his life" heart)
function dogFace(parent, cx, cy, r, o = {}) {
  const c = Object.assign({ fur: '#dba468', furDark: '#bf8650', furLight: '#f6dcb4' }, o);
  const g = svg('g', { transform: `translate(${cx},${cy}) scale(${(r / 48).toFixed(4)})` }, parent);
  for (const sx of [-1, 1]) svg('path', { d: `M${sx * 18},-30 L${sx * 40},-80 L${sx * 52},-18 Z`, fill: c.fur, stroke: INK, 'stroke-width': 5, 'stroke-linejoin': 'round' }, g);
  for (const sx of [-1, 1]) svg('path', { d: `M${sx * 28},-34 L${sx * 40},-66 L${sx * 46},-30 Z`, fill: '#f4b7a8' }, g);
  svg('ellipse', { rx: 52, ry: 46, fill: c.fur, stroke: INK, 'stroke-width': 5 }, g);
  svg('ellipse', { cx: 0, cy: 18, rx: 28, ry: 20, fill: c.furLight, stroke: INK, 'stroke-width': 4 }, g);
  if (o.old) svg('ellipse', { cx: 0, cy: 20, rx: 22, ry: 15, fill: '#e4ded6' }, g);
  svg('ellipse', { cx: 0, cy: 8, rx: 11, ry: 8, fill: '#2a1d21' }, g);
  for (const sx of [-1, 1]) {
    if (o.happy) svg('path', { d: `M${sx * 20 - 9},-6 Q${sx * 20},-18 ${sx * 20 + 9},-6`, fill: 'none', stroke: '#2a1d21', 'stroke-width': 5, 'stroke-linecap': 'round' }, g);
    else { svg('ellipse', { cx: sx * 20, cy: -8, rx: 7, ry: 9, fill: '#2a1d21' }, g); svg('circle', { cx: sx * 20 + 3, cy: -12, r: 3, fill: '#fff' }, g); }
    svg('ellipse', { cx: sx * 34, cy: 12, rx: 9, ry: 5, fill: '#f0857f', opacity: 0.5 }, g);
  }
  svg('path', { d: 'M0,16 Q-6,28 -14,26 M0,16 Q6,28 14,26', fill: 'none', stroke: '#2a1d21', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, g);
  if (o.tongue) svg('path', { d: 'M-7,26 Q-6,44 0,44 Q7,44 7,26 Z', fill: '#f07a8a', stroke: INK, 'stroke-width': 3 }, g);
  return g;
}
function dogAv(n = 64, o = {}) {
  const d = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  setA(d, { width: n, height: n, viewBox: '-60 -60 120 120' });
  svg('circle', { r: 60, fill: o.bg || '#ffe9c4' }, d);
  dogFace(d, 0, 8, 38, o);
  return d.outerHTML;
}
