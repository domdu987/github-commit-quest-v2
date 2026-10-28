// Rain toolkit for "12 ฤดูฝน": slanted rain streaks (one path per layer, so thousands of drops stay cheap), ground splashes,
// puddles with ripples, drips off edges, water drops on the lens, the umbrella (opens, tilts, sheds water), the rain
// "shadow" under the canopy (a mask that keeps whoever is under it dry), and mirrored reflections on the wet ground.

// rain streaks inside box [x0, y0, x1, y1]; slant = dx per dy (positive: wind blowing right)
function rainField(parent, box, n, seed, o = {}) {
  const [x0, y0, x1, y1] = box, Hh = y1 - y0, Ww = x1 - x0, r = rng(seed);
  const len = o.len ?? 60, slant = o.slant ?? 0.18, sp = o.speed ?? 1700;
  const drops = Array.from({ length: n }, () => ({ x: r() * Ww, y: r() * Hh, l: len * (0.6 + 0.8 * r()), v: sp * (0.85 + 0.3 * r()) }));
  const el = svg('path', { fill: 'none', stroke: o.color || '#f2eee6', 'stroke-width': o.w ?? 2.4, 'stroke-linecap': 'round', opacity: o.op ?? 0.5 }, parent);
  return (t, dens = 1) => {
    let d = '';
    const m = Math.floor(n * clamp(dens));
    for (let k = 0; k < m; k++) {
      const p = drops[k], yy = (p.y + t * p.v) % Hh, x = x0 + ((p.x + yy * slant) % Ww + Ww) % Ww;
      d += `M${x.toFixed(1)},${(y0 + yy).toFixed(1)}l${(-slant * p.l).toFixed(1)},${(-p.l).toFixed(1)}`;
    }
    el.setAttribute('d', d || 'M0,0');
  };
}
// splash crowns + rings where drops hit the ground between yA (far, small) and yB (near, big)
function splashField(parent, x0, x1, yA, yB, n, seed, o = {}) {
  const r = rng(seed), col = o.color || '#f6f2ea';
  const sp = Array.from({ length: n }, (_, i) => ({ per: 0.45 + r() * 0.5, ph: r() * 3, i,
    ring: svg('ellipse', { fill: 'none', stroke: col, 'stroke-width': 2.2 }, parent),
    crown: svg('path', { fill: 'none', stroke: col, 'stroke-width': 2.4, 'stroke-linecap': 'round' }, parent) }));
  return (t, dens = 1) => sp.forEach(s => {
    const c = Math.floor((t + s.ph) / s.per), k = ((t + s.ph) / s.per - c) / 0.5;
    const h = rng(s.i * 7919 + c * 104729 + seed)();
    const h2 = rng(s.i * 31 + c * 7 + seed * 3)();
    if (k > 1 || s.i >= n * dens) { s.ring.setAttribute('opacity', 0); s.crown.setAttribute('opacity', 0); return; }
    const y = yA + (yB - yA) * h2, sc = 0.45 + 0.75 * (y - yA) / Math.max(1, yB - yA), x = x0 + (x1 - x0) * h;
    const rr = (4 + 22 * ease.outCubic(k)) * sc;
    setA(s.ring, { cx: x.toFixed(1), cy: y.toFixed(1), rx: rr.toFixed(1), ry: (rr * 0.28).toFixed(1), opacity: ((1 - k) * (o.op ?? 0.55)).toFixed(2) });
    const ch = 16 * sc * Math.sin(Math.PI * Math.min(1, k * 1.6));
    s.crown.setAttribute('d', `M${(x - 6 * sc).toFixed(1)},${y.toFixed(1)} q${(-4 * sc).toFixed(1)},${(-ch).toFixed(1)} ${(-9 * sc).toFixed(1)},${(-ch * 0.6).toFixed(1)} M${(x + 6 * sc).toFixed(1)},${y.toFixed(1)} q${(4 * sc).toFixed(1)},${(-ch).toFixed(1)} ${(9 * sc).toFixed(1)},${(-ch * 0.6).toFixed(1)} M${x.toFixed(1)},${y.toFixed(1)} l0,${(-ch * 1.1).toFixed(1)}`);
    s.crown.setAttribute('opacity', (k < 0.6 ? 0.8 : (1 - k) * 2).toFixed(2));
  });
}
// puddle: dark glossy pool reflecting `sky`, with rings from drops; returns update(t, dens)
function puddle(parent, defs, cx, cy, rx, ry, sky, seed, o = {}) {
  const g = svg('g', {}, parent);
  svg('ellipse', { cx, cy, rx: rx + 6, ry: ry + 3, fill: '#000', opacity: 0.18 }, g);
  svg('ellipse', { cx, cy, rx, ry, fill: lin(defs, [[0, shade(sky, 25)], [1, shade(sky, -25)]]), opacity: o.op ?? 0.85 }, g);
  svg('path', { d: `M${cx - rx * 0.6},${cy - ry * 0.25} q${rx * 0.3},${-ry * 0.25} ${rx * 0.7},${-ry * 0.1}`, fill: 'none', stroke: '#ffffff', 'stroke-width': 3, opacity: 0.35, 'stroke-linecap': 'round' }, g);
  const r = rng(seed), rings = Array.from({ length: 5 }, () => ({ u: r() * 2 - 1, v: r() * 2 - 1, ph: r() * 2, el: svg('ellipse', { fill: 'none', stroke: '#ffffff', 'stroke-width': 2 }, g) }));
  return (t, dens = 1) => rings.forEach((q, i) => {
    const k = ((t * 1.1 + q.ph) % 1);
    const x = cx + q.u * rx * 0.6, y = cy + q.v * ry * 0.5, rr = 4 + k * rx * 0.28;
    setA(q.el, { cx: x.toFixed(1), cy: y.toFixed(1), rx: rr.toFixed(1), ry: (rr * ry / rx).toFixed(1), opacity: (dens > i / 5 ? (1 - k) * 0.5 : 0).toFixed(2) });
  });
}
// drops falling from edge points [[x, y, fallTo], ...]; returns update(t, dens)
function dripLine(parent, pts, seed, o = {}) {
  const r = rng(seed);
  const ds = pts.map(([x, y, y2]) => ({ x, y, y2: y2 ?? y + 400, per: 0.5 + r() * 0.6, ph: r() * 2, el: svg('path', { fill: o.color || '#f2eee6', opacity: 0.8 }, parent) }));
  return (t, dens = 1) => ds.forEach((q, i) => {
    const k = ((t + q.ph) / q.per) % 1, fall = (q.y2 - q.y), y = q.y + fall * k * k, s = 3.2;
    q.el.setAttribute('d', `M${q.x},${(y - s * 2.6).toFixed(1)} C${q.x + s},${(y - s).toFixed(1)} ${q.x + s},${(y + s).toFixed(1)} ${q.x},${(y + s).toFixed(1)} C${q.x - s},${(y + s).toFixed(1)} ${q.x - s},${(y - s).toFixed(1)} ${q.x},${(y - s * 2.6).toFixed(1)} Z`);
    q.el.setAttribute('opacity', i < pts.length * dens ? (0.85 * (1 - k * 0.4)).toFixed(2) : 0);
  });
}
// water drops on the lens (screen space, an svg in S.fx); some slide down slowly leaving a trail; returns update(t, op)
function lensDrops(fxParent, n, seed, o = {}) {
  const s = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920, style: 'position:absolute;inset:0;overflow:visible;pointer-events:none' });
  fxParent.appendChild(s);
  const defs = svg('defs', {}, s), r = rng(seed);
  const body = rad2(defs, [[0, '#ffffff', 0.04], [0.75, '#ffffff', 0.1], [1, '#ffffff', 0.35]], { cx: 0.45, cy: 0.4, r: 0.6 });
  const ds = Array.from({ length: n }, (_, i) => {
    const big = r() < 0.3, rr = big ? 14 + r() * 16 : 4 + r() * 8, g = svg('g', {}, s);
    svg('ellipse', { rx: rr, ry: rr * 1.05, fill: body, stroke: '#ffffff', 'stroke-opacity': 0.25, 'stroke-width': 1.5 }, g);
    svg('path', { d: `M${-rr * 0.5},${rr * 0.55} q${rr * 0.5},${rr * 0.4} ${rr},0`, fill: 'none', stroke: '#000', 'stroke-opacity': 0.25, 'stroke-width': Math.max(1.5, rr * 0.18) }, g);
    svg('ellipse', { cx: -rr * 0.35, cy: -rr * 0.4, rx: rr * 0.22, ry: rr * 0.14, fill: '#ffffff', opacity: 0.85 }, g);
    const trail = big && r() < 0.6 ? svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-opacity': 0.12, 'stroke-width': rr * 0.6, 'stroke-linecap': 'round' }, s) : null;
    if (trail) s.insertBefore(trail, g);
    return { x: r() * 1080, y: r() * 1920, rr, slide: trail ? 20 + r() * 50 : 0, ph: r() * 5, g, trail };
  });
  return (t, op = 1) => {
    s.style.opacity = clamp(op).toFixed(3);
    ds.forEach(d => {
      const y = d.y + d.slide * Math.max(0, t - d.ph * 0.3);
      d.g.setAttribute('transform', `translate(${d.x.toFixed(1)},${y.toFixed(1)})`);
      if (d.trail) d.trail.setAttribute('d', `M${d.x.toFixed(1)},${d.y.toFixed(1)} L${d.x.toFixed(1)},${y.toFixed(1)}`);
    });
  };
}

// ---------------- the umbrella (side view), built into a puppet's front-hand prop group ----------------
// The hand grips the shaft at 0,0; the canopy sits L above. set(open 0..1) folds / opens it; rim(k) gives the rim points
// (prop frame) for drips. c: panel colours; faded: an older, washed-out cloth with a patch.
function umbrella(parent, o = {}) {
  const R = o.R ?? 165, L = o.L ?? 175, n = 6, c = o.c || ['#a8323e', '#f1e6cf'];
  const g = svg('g', {}, parent);
  const shaftO = svg('path', { stroke: INK, 'stroke-width': 9, 'stroke-linecap': 'round', fill: 'none' }, g);
  const shaft = svg('path', { stroke: '#cfc6b8', 'stroke-width': 4, 'stroke-linecap': 'round', fill: 'none' }, g);
  svg('path', { d: 'M0,26 L0,46 Q0,68 17,68 Q32,68 32,52', fill: 'none', stroke: INK, 'stroke-width': 14, 'stroke-linecap': 'round' }, g);
  svg('path', { d: 'M0,26 L0,46 Q0,68 17,68 Q32,68 32,52', fill: 'none', stroke: o.handle || '#8a5232', 'stroke-width': 7, 'stroke-linecap': 'round' }, g);
  const can = svg('g', {}, g);
  const gores = Array.from({ length: n }, (_, i) => svg('path', { fill: c[i % 2], stroke: INK, 'stroke-width': 4, 'stroke-linejoin': 'round' }, can));
  const shadeP = svg('path', { fill: '#2a1418', opacity: 0.22 }, can);
  const hi = svg('path', { fill: 'none', stroke: '#ffffff', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.45 }, can);
  const patch = o.faded ? svg('path', { fill: '#d9b68a', stroke: INK, 'stroke-width': 2.5, opacity: 0.9 }, can) : null;
  const beads = Array.from({ length: 7 }, () => svg('circle', { r: 3, fill: '#ffffff', opacity: 0.7 }, can));
  const tip = svg('path', { stroke: INK, 'stroke-width': 6, 'stroke-linecap': 'round' }, g);
  const grip = o.skin ? svg('path', { fill: o.skin, stroke: INK, 'stroke-width': 3.5 }, g) : null;
  if (grip) grip.setAttribute('d', 'M-11,-2 Q-12,-12 0,-12 Q12,-12 11,-2 Q10,8 0,8 Q-10,8 -11,-2 Z');
  let geo = null;
  const api = {
    g, R, L,
    set(open, t = 0) {
      const k = clamp(open), e = ease.outBack(k) * 0.85 + k * 0.15;
      const w = lerp(15, R, e), rimY = lerp(-L + 130, -L, k), topY = -L - lerp(46, R * 0.46, k), sc = 16 * k;
      const xs = Array.from({ length: n + 1 }, (_, i) => w * Math.cos(Math.PI * i / n));
      const rib = x => `${(x * 0.92).toFixed(1)},${(topY + (rimY - topY) * 0.08).toFixed(1)}`;
      gores.forEach((gp, i) => {
        const a = xs[i], b = xs[i + 1];
        gp.setAttribute('d', `M0,${topY.toFixed(1)} Q${rib(a)} ${a.toFixed(1)},${rimY.toFixed(1)} Q${((a + b) / 2).toFixed(1)},${(rimY - sc).toFixed(1)} ${b.toFixed(1)},${rimY.toFixed(1)} Q${rib(b)} 0,${topY.toFixed(1)} Z`);
      });
      shadeP.setAttribute('d', `M${-w},${rimY} Q${(-w * 0.9).toFixed(1)},${(rimY - (rimY - topY) * 0.3).toFixed(1)} 0,${(rimY - (rimY - topY) * 0.32).toFixed(1)} Q${(w * 0.9).toFixed(1)},${(rimY - (rimY - topY) * 0.3).toFixed(1)} ${w},${rimY} Z`);
      hi.setAttribute('d', `M${(-w * 0.55).toFixed(1)},${(topY + (rimY - topY) * 0.38).toFixed(1)} Q${(-w * 0.3).toFixed(1)},${(topY + (rimY - topY) * 0.08).toFixed(1)} ${(w * 0.05).toFixed(1)},${(topY + 8).toFixed(1)}`);
      hi.setAttribute('opacity', (0.45 * k).toFixed(2));
      if (patch) patch.setAttribute('d', `M${(w * 0.42).toFixed(1)},${(topY + (rimY - topY) * 0.42).toFixed(1)} l${(22 * k).toFixed(1)},-4 l3,${(20 * k).toFixed(1)} l${(-22 * k).toFixed(1)},4 Z`);
      beads.forEach((b, i) => { const u = (i + 0.5) / beads.length * 2 - 1, x = u * w * 0.8, y = topY + (rimY - topY) * (0.12 + 0.75 * u * u); setA(b, { cx: x.toFixed(1), cy: (y + 6).toFixed(1), opacity: (0.6 * k * (0.5 + 0.5 * Math.sin(t * 3 + i * 2))).toFixed(2) }); });
      const d = `M0,30 L0,${(topY + 10).toFixed(1)}`;
      shaftO.setAttribute('d', d); shaft.setAttribute('d', d);
      tip.setAttribute('d', `M0,${topY.toFixed(1)} L0,${(topY - 18).toFixed(1)}`);
      geo = { w, rimY, topY };
    },
    rim(u) { return [geo.w * u, geo.rimY]; },   // u -1 (back) … 1 (front)
    geo: () => geo,
  };
  api.set(o.open ?? 1);
  return api;
}
// the dry patch under a canopy: mask out rain in the polygon below the rim, sheared by the rain's slant
function rainShadow(defs, slant, o = {}) {
  const id = uidS('rs');
  const m = svg('mask', { id, maskUnits: 'userSpaceOnUse', x: -2000, y: -2000, width: 6000, height: 6000 }, defs);
  svg('rect', { x: -2000, y: -2000, width: 6000, height: 6000, fill: '#fff' }, m);
  const poly = svg('path', { fill: '#000' }, m);
  return {
    url: `url(#${id})`,
    // rim points in world coords: left, right; D: how far below the shadow reaches
    set(L, Rr, top, D = 900) {
      if (!L) { poly.setAttribute('d', 'M0,0'); return; }
      poly.setAttribute('d', `M${L[0].toFixed(1)},${L[1].toFixed(1)} Q${top[0].toFixed(1)},${(top[1] - 30).toFixed(1)} ${Rr[0].toFixed(1)},${Rr[1].toFixed(1)} L${(Rr[0] + slant * D).toFixed(1)},${(Rr[1] + D).toFixed(1)} L${(L[0] + slant * D).toFixed(1)},${(L[1] + D).toFixed(1)} Z`);
    },
  };
}
// mirrored copy of a puppet on wet ground (full colour, blurred, fading away from the feet); returns the copy
function reflectPup(pup, parent, defs, groundY, o = {}) {
  const g = svg('g', { opacity: o.op ?? 0.3, filter: blurFilter(defs, o.blur ?? 2.2), transform: `translate(0,${2 * groundY}) scale(1,-1)` }, parent);
  const cp = new Puppet(g, Object.assign({}, pup.o), defs);
  const orig = pup.pose.bind(pup);
  pup.pose = p => { orig(p); cp.pose(p); };
  return cp;
}
// fade mask for a reflection group: opaque at the ground line, gone `len` below it
function reflFade(defs, groundY, len = 300) {
  const id = uidS('rf');
  const m = svg('mask', { id, maskUnits: 'userSpaceOnUse', x: -2000, y: -2000, width: 6000, height: 6000 }, defs);
  svg('rect', { x: -2000, y: groundY, width: 6000, height: len, fill: lin(defs, [[0, '#fff', 1], [1, '#fff', 0]]) }, m);
  return `url(#${id})`;
}
