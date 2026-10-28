// Production-level lighting, depth and camera on top of the story2 rig: characters get a rim light on the side that
// faces the key light and a soft core shadow on the far side, a cast shadow on the wall behind them, contact shadows,
// ambient occlusion where walls meet floors, light shafts with dust, foreground bokeh, and a shot-list camera that
// cuts between framings (wide / medium / close-up / insert) with a slow drift, a little handheld life and depth of
// field that follows the shot size.

// ---------------- character light ----------------
// ux, uy: unit vector from the character toward the key light. rim: light colour, shade: shadow colour.
function charLight(defs, o = {}) {
  const ux = o.ux ?? 0.8, uy = o.uy ?? -0.6, rw = o.rimW ?? 9, sw = o.shadeW ?? 26;
  const id = uidS('cl');
  const f = svg('filter', { id, x: '-15%', y: '-15%', width: '130%', height: '130%', 'color-interpolation-filters': 'sRGB' }, defs);
  svg('feOffset', { in: 'SourceAlpha', dx: (-ux * rw).toFixed(2), dy: (-uy * rw).toFixed(2), result: 'ro' }, f);
  svg('feComposite', { in: 'SourceAlpha', in2: 'ro', operator: 'out', result: 'rm' }, f);
  svg('feGaussianBlur', { in: 'rm', stdDeviation: o.rimBlur ?? 1.2, result: 'rmb0' }, f);
  svg('feComposite', { in: 'rmb0', in2: 'SourceAlpha', operator: 'in', result: 'rmb' }, f);
  svg('feFlood', { 'flood-color': o.rim || '#ffd9a0', 'flood-opacity': o.rimOp ?? 0.75, result: 'rc' }, f);
  svg('feComposite', { in: 'rc', in2: 'rmb', operator: 'in', result: 'rim' }, f);
  svg('feOffset', { in: 'SourceAlpha', dx: (ux * sw).toFixed(2), dy: (uy * sw).toFixed(2), result: 'so' }, f);
  svg('feComposite', { in: 'SourceAlpha', in2: 'so', operator: 'out', result: 'sm' }, f);
  svg('feGaussianBlur', { in: 'sm', stdDeviation: o.shadeBlur ?? 9, result: 'smb' }, f);
  svg('feComposite', { in: 'smb', in2: 'SourceAlpha', operator: 'in', result: 'smc' }, f);
  svg('feFlood', { 'flood-color': o.shade || '#3a2050', 'flood-opacity': o.shadeOp ?? 0.42, result: 'sc' }, f);
  svg('feComposite', { in: 'sc', in2: 'smc', operator: 'in', result: 'sh' }, f);
  svg('feBlend', { in: 'sh', in2: 'SourceGraphic', mode: 'multiply', result: 'b1' }, f);
  svg('feBlend', { in: 'rim', in2: 'b1', mode: 'screen' }, f);
  return `url(#${id})`;
}

// ---------------- cast shadows ----------------
// a dark copy of the puppet, blurred and thrown onto the wall behind, away from the light at (lx, ly)
function castShadow(pup, parent, defs, o = {}) {
  const bid = uidS('cb');
  const bf = svg('filter', { id: bid, x: '-30%', y: '-30%', width: '160%', height: '160%' }, defs);
  svg('feGaussianBlur', { stdDeviation: o.blur ?? 7 }, bf);
  const g = svg('g', { opacity: o.op ?? 0.24, filter: `url(#${bid})` }, parent);
  const inner = svg('g', {}, g);
  const dark = {};
  for (const k in pup.o) dark[k] = typeof pup.o[k] === 'string' && pup.o[k][0] === '#' ? (o.color || '#1a0f22') : pup.o[k];
  dark.flat = true; dark.ink = o.color || '#1a0f22';
  const sh = new Puppet(inner, dark, null);
  const orig = pup.pose.bind(pup);
  const st = { on: true };
  pup.pose = p => {
    orig(p);
    if (!st.on) { g.setAttribute('display', 'none'); return; }
    g.removeAttribute('display');
    sh.pose(p);
    const lx = o.lx ?? 900, k = o.k ?? 0.3, ay = o.floorY ?? p.y, ax = p.x;
    const dx = (ax - lx) * k + (o.dx || 0), sk = clamp((ax - lx) * (o.skewK ?? 0.025), -18, 18);
    inner.setAttribute('transform', `translate(${(ax + dx).toFixed(1)},${(ay + (o.dy || 0)).toFixed(1)}) skewX(${sk.toFixed(2)}) scale(${o.sx ?? 1.1},${o.sy ?? 1.06}) translate(${-ax.toFixed(1)},${-ay.toFixed(1)})`);
  };
  return st;
}
// soft elliptical contact shadow that follows a point on the floor; returns update(x, y, w)
function footShadow(parent, defs, op = 0.35) {
  const e = svg('ellipse', { rx: 80, ry: 14, fill: rad2(defs, [[0, '#120a14', op], [1, '#120a14', 0]]) }, parent);
  return (x, y, w = 160) => setA(e, { cx: x.toFixed(1), cy: y.toFixed(1), rx: (w / 2).toFixed(1), ry: (w * 0.1).toFixed(1) });
}

// ---------------- set lighting ----------------
// darkening where the wall meets the floor and along a vertical corner
function wallAO(parent, defs, yFloor, o = {}) {
  svg('rect', { x: -300, y: yFloor - (o.h ?? 150), width: 1680, height: o.h ?? 150, fill: lin(defs, [[0, '#000', 0], [1, '#000', o.op ?? 0.28]]) }, parent);
  svg('rect', { x: -300, y: yFloor, width: 1680, height: 60, fill: lin(defs, [[0, '#000', (o.op ?? 0.28) * 0.9], [1, '#000', 0]]) }, parent);
}
// pool of light (radial) — on a wall or a floor (squashed)
function lightPool(parent, defs, cx, cy, rx, ry, color, op) {
  return svg('ellipse', { cx, cy, rx, ry, fill: rad2(defs, [[0, color, op], [0.55, color, op * 0.35], [1, color, 0]]), style: 'mix-blend-mode:screen' }, parent);
}
// lamp cone thrown up/down a wall from a shade at (x, y)
function lampCone(parent, defs, x, y, w, h, color, op, up = true) {
  const d = up ? `M${x - 30},${y} L${x + 30},${y} L${x + w / 2},${y - h} L${x - w / 2},${y - h} Z` : `M${x - 30},${y} L${x + 30},${y} L${x + w / 2},${y + h} L${x - w / 2},${y + h} Z`;
  return svg('path', { d, fill: lin(defs, up ? [[0, color, 0], [1, color, op]] : [[0, color, op], [1, color, 0]]), style: 'mix-blend-mode:screen' }, parent);
}
// shaft of light (polygon) with slow dust motes drifting inside; returns update(t)
function lightShaft(parent, defs, pts, color, op, seed = 7, nDust = 26) {
  const [a, b, c, d] = pts;
  const g = svg('g', { style: 'mix-blend-mode:screen' }, parent);
  svg('path', { d: `M${a} L${b} L${c} L${d} Z`, fill: lin(defs, [[0, color, op], [1, color, 0]], 0.4, 1) }, g);
  const r = rng(seed), motes = [];
  for (let i = 0; i < nDust; i++) motes.push({ u: r(), v: r(), ph: r() * 9, sp: 0.02 + r() * 0.04, sz: 1.5 + r() * 2.5, el: svg('circle', { r: 2, fill: '#fff8e8' }, g) });
  return t => motes.forEach(m => {
    const v = (m.v + t * m.sp) % 1, u = m.u + 0.04 * Math.sin(t * 0.7 + m.ph);
    const top = [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u], bot = [d[0] + (c[0] - d[0]) * u, d[1] + (c[1] - d[1]) * u];
    setA(m.el, { cx: (top[0] + (bot[0] - top[0]) * v).toFixed(1), cy: (top[1] + (bot[1] - top[1]) * v).toFixed(1), r: m.sz.toFixed(1), opacity: (0.7 * Math.sin(Math.PI * v) * (0.5 + 0.5 * Math.sin(t * 2 + m.ph))).toFixed(2) });
  });
}
// big soft out-of-focus discs (for a blurred foreground layer); returns update(t)
function bokehField(parent, defs, n, box, colors, seed = 3, o = {}) {
  const r = rng(seed), bs = [];
  for (let i = 0; i < n; i++) {
    const c = colors[i % colors.length];
    bs.push({ x: box[0] + r() * (box[2] - box[0]), y: box[1] + r() * (box[3] - box[1]), rr: (o.rMin ?? 30) + r() * ((o.rMax ?? 80) - (o.rMin ?? 30)), ph: r() * 9,
      el: svg('circle', { fill: rad2(defs, [[0, c, 0.55], [0.7, c, 0.35], [1, c, 0]]), style: 'mix-blend-mode:screen' }, parent) });
  }
  return t => bs.forEach(b => setA(b.el, { cx: (b.x + Math.sin(t * 0.3 + b.ph) * 12).toFixed(1), cy: (b.y + Math.cos(t * 0.25 + b.ph) * 8).toFixed(1), r: b.rr.toFixed(1), opacity: ((o.op ?? 0.8) * (0.7 + 0.3 * Math.sin(t * 1.3 + b.ph))).toFixed(2) }));
}
// atmospheric depth: a soft wash over the far layer
function haze(parent, defs, color, op, y0 = -300, y1 = 1400) {
  svg('rect', { x: -300, y: y0, width: 1680, height: y1 - y0, fill: lin(defs, [[0, color, op], [1, color, op * 0.3]]) }, parent);
}

// ---------------- shot-list camera ----------------
// shots: [{ t, cam: {x,y,z,fx,fy}, to?: {...}, move?: seconds }] — each shot drifts from cam to `to` until the next
// shot starts. A shot with `move` glides from the previous framing instead of cutting.
const lerpCam = (a, b, k) => ({ x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k), z: lerp(a.z, b.z, k), fx: lerp(a.fx, b.fx, k), fy: lerp(a.fy, b.fy, k), r: lerp(a.r || 0, b.r || 0, k) });
function shotCam(lt, shots, end, o = {}) {
  let i = 0; while (i + 1 < shots.length && lt >= shots[i + 1].t) i++;
  const s = shots[i], t1 = i + 1 < shots.length ? shots[i + 1].t : end;
  const drift = (sh, tt, te) => lerpCam(sh.cam, sh.to || sh.cam, ease.inOutSine(prog(tt, sh.t, te)));
  let cam = drift(s, lt, t1);
  if (s.move && i > 0) { const pc = drift(shots[i - 1], s.t, s.t); cam = lerpCam(pc, cam, ease.inOutCubic(prog(lt, s.t, s.t + s.move))); }
  const hh = o.handheld ?? 1;
  cam.x += hh * (Math.sin(lt * 1.1) * 2.2 + Math.sin(lt * 2.7 + 1) * 1.1);
  cam.y += hh * (Math.sin(lt * 0.9 + 2) * 1.8 + Math.sin(lt * 2.3) * 0.9);
  cam.r = (cam.r || 0) + hh * Math.sin(lt * 0.7) * 0.12;
  cam.shot = i;
  return cam;
}
// apply a camera and set depth of field from its zoom: closer framings throw the far layer further out of focus
function applyCam(S, cam, o = {}) {
  S.cam(cam);
  const far = S.L.far;
  if (far && o.dof !== false) {
    const b = (o.base ?? 1.5) + Math.max(0, cam.z - 1.15) * (o.k ?? 7);
    far.el.style.filter = `blur(${b.toFixed(2)}px)` + (o.farGrade || '');
  }
  return cam;
}
// world point → screen point through a camera at layer depth d
const toScreenP = (c, d, x, y) => { const z = 1 + (c.z - 1) * d; return [c.fx + (x - c.fx) * z - c.x * d, c.fy + (y - c.fy) * z - c.y * d]; };
// framing helper: a camera that puts world point (wx, wy) at screen point (sx, sy) at zoom z (layer depth 1)
function frameAt(wx, wy, z, sx = 540, sy = 960, fx = 540, fy = 960) { return { x: fx + (wx - fx) * z - sx, y: fy + (wy - fy) * z - sy, z, fx, fy }; }

// ---------------- polish for the UI cards ----------------
(function proCSS() {
  const st = document.createElement('style');
  st.textContent = `
  .card { box-shadow: 0 2px 0 rgba(255,255,255,.65) inset, 0 -3px 0 rgba(0,0,0,.06) inset, 0 34px 60px rgba(10,4,20,.42), 0 12px 22px rgba(10,4,20,.26), 0 2px 4px rgba(10,4,20,.2) !important; }
  .card::after { content: ''; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; background: linear-gradient(180deg, rgba(255,255,255,.35), rgba(255,255,255,0) 38%); }
  .layer { will-change: auto !important; }
  .chip { box-shadow: 0 2px 0 rgba(255,255,255,.6) inset, 0 18px 34px rgba(10,4,20,.38), 0 6px 12px rgba(10,4,20,.22) !important; }
  `;
  document.head.appendChild(st);
})();
