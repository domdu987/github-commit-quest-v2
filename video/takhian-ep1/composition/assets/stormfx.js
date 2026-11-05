// StormFX — storm effects for ต้นตะเคียนกลางนา (lane C for lane B · 2 Nov 2026)
// Load after takhian.js (it only needs the engine's layers L, a GSAP timeline and #flashw). All coordinates are world
// coordinates of the layer named (default: the layer the shot's set lives in), times are absolute timeline seconds.
// Every call returns a small handle; nothing is drawn outside the shot it is given.
// Wiring: copy into hf/lib, add "stormfx.js" after "takhian.js" in make.py's lib list and a <script src="assets/stormfx.js"> after
// takhian.js in head.part. Give tkField rain: 0 and flash: 0 (StormFX draws both). A working shot: video/takhian-kit/demo/demo.body.part
// Sound for the same events: video/takhian-kit/stormsfx.py (pitched events only, no noise bed).
//
//   StormFX.bolt(L, tl, t, o)        a branching strike: a dim stepped leader crawls down (o.leader s, default 0.15), then the
//        return stroke: white core, blue-violet glow, 2–3 flickers; #flashw full-screen white for 2–3 frames; the cloud lit
//        from inside; a dark afterimage of the channel; optional silhouette beat (o.sil s) on the given layers.
//        o: x0,y0 (in the cloud) x1,y1 (the hit) · seed · w (thickness, 1) · layer "glow"|"sky" (sky = far bolt behind the land)
//           flash 0..1 (#flashw strength, 1) · cloud true (light the cloud base) · sil 0 · rain handle(s) to light up (o.lit)
//        returns { tR } — the time of the return stroke (sync sound and other hits to it)
//   StormFX.strikeTree(L, tl, t, o)  what the strike does to the tree (tree = Tk.tree at o.x,o.y scale o.s):
//        the trunk split glowing then charring, bark chips thrown with gravity, sparks, smoke rising off the scar (looping),
//        o.branch (default true) a limb snapping off the crown and falling · o.seed · o.side ±1 which side the limb falls
//   StormFX.ground(L, tl, t, o)      ground current: branching lines of light running over the wet field from the foot (o.x,o.y)
//        to each point of o.to [[x,y],…], then each target puddle flashes and rings · o.layer "glow" · o.s line scale
//   StormFX.rain(L, tl, t0, dur, o)  rain with depth: near (big, blurred, fast, screen layer) · mid · far (behind the set) streaks,
//        all leaning with o.wind (dx per dy, 0.25); o.curtain: veils of rain sweeping across the far field; o.ripples
//        [{x,y,w,h,n,layer}] rings popping in the paddies; o.splash [[x,y,s],…] water jumping at feet; o.density (1).
//        returns a handle: pass it as o.lit to bolt() so every drop flashes white with the lightning
//   StormFX.wind(L, tl, t0, dur, o)  o.rice: a row of out-of-focus rice in front of the lens rolling in waves · o.ribbons
//        [[x,y,len,colour],…] ผ้าแพร tails fluttering (world, set layer) · o.leaves n leaves blown across the frame · o.dir ±1
(function () {
  const SF = (window.StormFX = window.StormFX || {});
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let UID = 0;
  const nid = (p) => `sf${p}${++UID}`;
  const defs = () => {
    if (document.getElementById("sfSil")) return;
    document.body.insertAdjacentHTML("beforeend", `<svg width="0" height="0" style="position:absolute"><defs>
      <filter id="sfSil"><feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0 0.06  0 0 0 1 0"/></filter>
      <radialGradient id="sfCloudLit"><stop offset="0" stop-color="#f4f2ff" stop-opacity=".95"/><stop offset=".35" stop-color="#b8b0ff" stop-opacity=".55"/><stop offset="1" stop-color="#6a60c0" stop-opacity="0"/></radialGradient>
      <radialGradient id="sfHit"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset=".3" stop-color="#dfe6ff" stop-opacity=".7"/><stop offset="1" stop-color="#9a8aff" stop-opacity="0"/></radialGradient>
      <radialGradient id="sfEmber"><stop offset="0" stop-color="#fff2b0"/><stop offset=".4" stop-color="#ff8a1a" stop-opacity=".8"/><stop offset="1" stop-color="#ff3a0a" stop-opacity="0"/></radialGradient>
      <radialGradient id="sfSmoke"><stop offset="0" stop-color="#d8dce2" stop-opacity=".8"/><stop offset=".6" stop-color="#a8acb6" stop-opacity=".4"/><stop offset="1" stop-color="#6a6e78" stop-opacity="0"/></radialGradient>
      <radialGradient id="sfPuddle"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".5" stop-color="#cfe0ff" stop-opacity=".5"/><stop offset="1" stop-color="#9ab0ff" stop-opacity="0"/></radialGradient>
      <linearGradient id="sfVeil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9aa0b4" stop-opacity="0"/><stop offset=".3" stop-color="#9aa0b4" stop-opacity=".32"/><stop offset="1" stop-color="#7a8090" stop-opacity=".12"/></linearGradient>
    </defs></svg>`);
  };
  const D = (pts) => "M" + pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L");

  // ------------------------------------------------------------------ the channel
  // a main channel from (x0,y0) to (x1,y1) and forks that run downward and fade; every path knows when the leader reaches it
  SF.channel = (x0, y0, x1, y1, seed = 7, o = {}) => {
    const r = mk(seed), out = [], H = Math.max(1, y1 - y0);
    const walk = (ax, ay, bx, by, depth, width, down) => {
      const n = Math.max(5, Math.round(Math.hypot(bx - ax, by - ay) / 55)), pts = [[ax, ay]];
      let px = ax, py = ay;
      for (let k = 1; k < n; k++) {
        const t = k / n, jx = (r() - 0.5) * 120 * (1 - t * 0.4) * (depth ? 0.6 : 1), jy = (r() - 0.5) * 26;
        px = ax + (bx - ax) * t + jx; py = ay + (by - ay) * t + jy; pts.push([px, py]);
      }
      pts.push([bx, by]);
      out.push({ pts, d: D(pts), width, depth, main: depth === 0 && !down, at: (ay - y0) / H });
      if (depth < (o.depth ?? 3)) pts.slice(1, -2).forEach((p) => {
        if (r() < (depth ? 0.22 : 0.42)) {
          const len = (180 + r() * 320) / (depth + 1), ang = Math.PI / 2 + (r() < 0.5 ? -1 : 1) * (0.35 + r() * 0.75);
          walk(p[0], p[1], p[0] + Math.cos(ang) * len, p[1] + Math.sin(ang) * len * 0.9, depth + 1, width * 0.5, true);
        }
      });
    };
    walk(x0, y0, x1, y1, 0, 1, false);
    return out;
  };
  const drawChannel = (paths, w, cls) => {
    const g = paths.map((p) => `<path d="${p.d}" stroke="#8a6aff" stroke-width="${f1(78 * w * p.width)}" fill="none" opacity="${p.main ? 0.24 : 0.14}" stroke-linejoin="round" stroke-linecap="round"/>`).join("");
    const m = paths.map((p) => `<path d="${p.d}" stroke="#b8ccff" stroke-width="${f1(24 * w * p.width)}" fill="none" opacity="${p.main ? 0.8 : 0.55}" stroke-linejoin="round" stroke-linecap="round"/>`).join("");
    const c = paths.map((p) => `<path d="${p.d}" stroke="#ffffff" stroke-width="${f1(8 * w * p.width + 1.5)}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`).join("");
    return `<g class="${cls || ""}">${g}${m}${c}</g>`;
  };

  // ------------------------------------------------------------------ lighting things up for one flash pattern
  const FLICK = [[0, 1], [0.045, 0.3], [0.085, 1], [0.13, 0.25], [0.19, 0.85], [0.25, 0.15], [0.31, 0.6], [0.4, 0]];
  const lightUp = (tl, tR, lit, k = 1) => {
    [].concat(lit || []).forEach((h) => (h && h.els ? h.els : []).forEach((e) => {
      const base = e.style.filter && e.style.filter !== "none" ? e.style.filter + " " : "";
      FLICK.forEach(([dt, v]) => tl.set(e, { filter: v > 0.2 ? `${base}brightness(${f1(1 + 1.6 * v * k)})` : base.trim() || "none" }, tR + dt));
    }));
  };

  SF.bolt = (L, tl, t, o = {}) => {
    defs();
    const id = nid("b"), w = o.w ?? 1, lay = L[o.layer || "glow"], leader = o.leader ?? 0.15, tR = t + leader, k = o.flash ?? 1;
    const paths = SF.channel(o.x0, o.y0, o.x1, o.y1, o.seed ?? 7, o);
    // the cloud lit from inside: a soft violet-white bloom where the channel leaves the cloud, and a wider one over the base
    if (o.cloud !== false) put(L.sky, `<g id="${id}-cl" opacity="0" style="mix-blend-mode:screen"><ellipse cx="${o.cx ?? o.x0}" cy="${o.cy ?? 420}" rx="${f1(900 * (o.cloudR ?? 1))}" ry="${f1(300 * (o.cloudR ?? 1))}" fill="url(#sfCloudLit)"/><ellipse cx="${o.cx ?? o.x0}" cy="${o.cy ?? 420}" rx="${f1(380 * (o.cloudR ?? 1))}" ry="${f1(160 * (o.cloudR ?? 1))}" fill="url(#sfCloudLit)"/></g>`);
    // leader: thin dim strokes drawn top-down, each fork starting when the leader reaches its root
    const ld = paths.map((p, i) => `<path id="${id}-l${i}" d="${p.d}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" stroke="#e8eeff" stroke-width="${f1((p.main ? 7 : 4) * w)}" fill="none" opacity="${p.main ? 0.95 : 0.7}" stroke-linecap="round"/>`).join("");
    put(lay, `<g id="${id}"><g id="${id}-ld" opacity="0">${ld}</g><g id="${id}-rs" opacity="0">${drawChannel(paths, w)}<circle cx="${o.x1}" cy="${o.y1}" r="${f1(260 * w)}" fill="url(#sfHit)"/></g>
      <g id="${id}-ai" opacity="0">${paths.filter((p) => p.depth < 2).map((p) => `<path d="${p.d}" stroke="#04050c" stroke-width="${f1((p.main ? 20 : 9) * w)}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`).join("")}</g></g>`);
    tl.set(`#${id}-ld`, { opacity: 1 }, t);
    paths.forEach((p, i) => { const a = t + leader * p.at * 0.9, len = Math.max(0.03, leader * (1 - p.at) * (p.main ? 1 : 0.6));
      tl.fromTo(`#${id}-l${i}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: len, ease: "none", immediateRender: false }, a); });
    tl.set(`#${id}-ld`, { opacity: 0 }, tR);
    // return stroke + flickers; the cloud follows; #flashw: 2–3 frames of white, a weaker re-flash on the second pulse
    FLICK.forEach(([dt, v]) => { tl.set(`#${id}-rs`, { opacity: v }, tR + dt); if (o.cloud !== false) tl.set(`#${id}-cl`, { opacity: v * 0.95 }, tR + dt); });
    if (k > 0) SF.flash(tl, tR, k, k >= 0.9 ? 3 : k >= 0.5 ? 2 : 1);
    // afterimage: the channel burnt into the eye as a dark line, gone in a third of a second
    tl.set(`#${id}-ai`, { opacity: 0.6 }, tR + 0.4); tl.to(`#${id}-ai`, { opacity: 0, duration: 0.35, ease: "power1.out" }, tR + 0.42);
    // silhouette beat: OFF under V1b (a black-out right after a flash is one more flicker); kept for o.silForce only
    if (o.silForce) { defs(); [L.set, L.act, L.mid, L.far].filter(Boolean).forEach((e) => { tl.set(e, { attr: { filter: "url(#sfSil)" } }, tR + 2.6 / 60); tl.set(e, { attr: { filter: "none" } }, tR + 2.6 / 60 + o.sil); }); }
    lightUp(tl, tR, o.lit, Math.min(k, 0.4));
    return { tR, id };
  };

  // ------------------------------------------------------------------ V1b: the one gate for every full-screen flash
  // (owner 3 Nov 2569 "ผมดูแลปวดตามาก"): peak ≤ .28, one soft pulse that fades (no strobing), at most one per 10 s of the episode.
  // Requests are queued while the shots are built and resolved once at the end (foot part: StormFX.flashResolve()) by priority —
  // strikes (3) before mid bolts (2) before flickers (1), earlier first — so a passing flicker never takes the strike's slot.
  SF._fq = [];
  SF.flash = (tl, t, peak = 0.28, prio = 1) => { SF._fq.push({ tl, t, peak: Math.min(peak, 0.28), prio }); };
  SF.flashResolve = () => { const ok = [];
    SF._fq.slice().sort((a, b) => b.prio - a.prio || a.t - b.t).forEach((q) => { if (ok.every((g) => Math.abs(g.t - q.t) >= 10)) ok.push(q); });
    ok.forEach((q) => { q.tl.set("#flashw", { opacity: q.peak }, q.t); q.tl.to("#flashw", { opacity: 0, duration: 0.34, ease: "power2.out", immediateRender: false }, q.t + 1 / 60); });
    SF._fq = []; return ok.map((q) => +q.t.toFixed(2)).sort((a, b) => a - b); };

  // ------------------------------------------------------------------ the tree hit
  SF.strikeTree = (L, tl, t, o = {}) => {
    defs();
    const id = nid("t"), s = o.s ?? 1, X = (v) => o.x + v * s, Y = (v) => o.y + v * s, r = mk(o.seed ?? 19);
    const scar = [[10, -1232], [-20, -980], [20, -760], [-14, -520], [18, -300], [-4, -60]].map(([a, b]) => [X(a), Y(b)]);
    // the split: white-hot, then orange, then a charred black seam with embers that breathe
    // (owner review 2 พ.ย.) the seam is Tk.scarGroove — bark blown off in a ragged strip, a charred split — and the heat is
    // Tk.scarEmbers: glowing cracks along its lips that flare, then die down to a breathing glow
    const TT = `transform="translate(${f1(o.x)},${f1(o.y)}) scale(${f1(s)})"`;
    put(L.set, `<g id="${id}-sc"><g ${TT}>${window.Tk && Tk.scarGroove ? Tk.scarGroove(5) : ""}</g>
      <g id="${id}-hot" opacity="0"><g ${TT}>${window.Tk && Tk.scarEmbers ? Tk.scarEmbers(5) : ""}</g></g>
      <path id="${id}-wh" d="${D(scar)}" stroke="#fff6d0" stroke-width="${f1(8 * s)}" fill="none" stroke-linejoin="round" opacity="0"/></g>`);
    tl.set(`#${id}-sc`, { opacity: 0 }, 0); tl.set(`#${id}-sc`, { opacity: 1 }, t);
    tl.set(`#${id}-wh`, { opacity: 1 }, t); tl.to(`#${id}-wh`, { opacity: 0, duration: 0.6, ease: "power2.in" }, t + 0.1);
    tl.set(`#${id}-hot`, { opacity: 1 }, t); tl.to(`#${id}-hot`, { opacity: 0.12, duration: 1.6, ease: "power2.out" }, t + 0.2);
    tl.to(`#${id}-hot`, { opacity: 0.3, duration: 0.6, yoyo: true, repeat: Math.ceil((o.dur ?? 6) / 0.6), ease: "sine.inOut" }, t + 1.8);
    // embers along the seam
    put(L.glow, `<g id="${id}-em" opacity="0">${scar.slice(0, 5).map(([x, y], k) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1((50 - k * 6) * s)}" fill="url(#sfEmber)"/>`).join("")}</g>`);
    tl.set(`#${id}-em`, { opacity: 1 }, t); tl.to(`#${id}-em`, { opacity: 0.25, duration: 1.6, ease: "power2.out" }, t + 0.2);
    // bark chips: thrown out from points down the trunk, arc up, fall with gravity, tumbling
    let ch = "";
    for (let k = 0; k < 26; k++) { const p = scar[Math.floor(r() * 4)], sz = (8 + r() * 14) * s;
      ch += `<g transform="translate(${f1(p[0] + (r() - 0.5) * 30 * s)},${f1(p[1])})"><path id="${id}-c${k}" d="M0,0l${f1(sz)},${f1(-sz * 0.5)}l${f1(sz * 0.5)},${f1(sz)}l${f1(-sz)},${f1(sz * 0.4)}z" fill="${k % 3 ? "#5a3e28" : "#8a6a4a"}" stroke="#1e140e" stroke-width="${f1(2 * s)}" opacity="0"/></g>`; }
    put(L.glow, `<g id="${id}-ch">${ch}</g>`);
    const rc = mk((o.seed ?? 19) + 5);
    for (let k = 0; k < 26; k++) { const dir = rc() < 0.5 ? -1 : 1, vx = dir * (120 + rc() * 520) * s, up = (60 + rc() * 260) * s, fall = (500 + rc() * 700) * s, T = 0.7 + rc() * 0.6;
      const e = `#${id}-c${k}`; tl.set(e, { opacity: 1 }, t + 0.01);
      tl.fromTo(e, { x: 0 }, { x: vx, duration: T, ease: "power1.out", immediateRender: false }, t + 0.01);
      tl.fromTo(e, { y: 0 }, { keyframes: [{ y: -up, duration: T * 0.3, ease: "power2.out" }, { y: fall, duration: T * 0.7, ease: "power2.in" }], immediateRender: false }, t + 0.01);
      tl.fromTo(e, { rotation: 0, svgOrigin: "0 0" }, { rotation: dir * (300 + rc() * 600), svgOrigin: "0 0", duration: T, ease: "none", immediateRender: false }, t + 0.01);
      tl.to(e, { opacity: 0, duration: 0.15 }, t + T); }
    // sparks: short white-yellow streaks bursting from the hit and from the split, fast, gone in under half a second
    let sp = "";
    for (let k = 0; k < 34; k++) { const p = k < 20 ? scar[0] : scar[1 + Math.floor(r() * 3)], a = r() * Math.PI * 2, L0 = (18 + r() * 30) * s;
      sp += `<g transform="translate(${f1(p[0])},${f1(p[1])}) rotate(${f1(a * 180 / Math.PI)})"><path id="${id}-p${k}" d="M0,0h${f1(L0)}" stroke="${k % 3 ? "#fff6c0" : "#ffb84a"}" stroke-width="${f1(4 * s)}" stroke-linecap="round" opacity="0"/></g>`; }
    put(L.glow, `<g id="${id}-sp" style="mix-blend-mode:screen">${sp}</g>`);
    for (let k = 0; k < 34; k++) { const e = `#${id}-p${k}`, d = (160 + rc() * 420) * s, T = 0.18 + rc() * 0.3;
      tl.set(e, { opacity: 1 }, t); tl.fromTo(e, { x: 0 }, { x: d, duration: T, ease: "power2.out", immediateRender: false }, t); tl.to(e, { opacity: 0, duration: T * 0.6 }, t + T * 0.4); }
    // smoke: soft grey puffs rising off the seam, widening and drifting with the wind, looping for the rest of the shot
    if (o.smoke !== false) { const n = 14; let sm = "";
      for (let k = 0; k < n; k++) { const p = scar[k % 4]; sm += `<g transform="translate(${f1(p[0])},${f1(p[1])})"><circle id="${id}-s${k}" r="${f1(80 * s)}" fill="url(#sfSmoke)" opacity="0"/></g>`; }
      put(L.set, `<g id="${id}-sm">${sm}</g>`);
      const dur = o.dur ?? 6;
      for (let k = 0; k < n; k++) { const e = `#${id}-s${k}`, P = 1.6 + (k % 3) * 0.3, rep = Math.ceil(dur / P);
        tl.fromTo(e, { x: 0, y: 0, scale: 0.5, opacity: 0.95, svgOrigin: "0 0" }, { x: (o.windX ?? 220) * s, y: -520 * s, scale: 3.2, opacity: 0, svgOrigin: "0 0", duration: P, ease: "power1.out", repeat: rep, immediateRender: false }, t + 0.25 + k * 0.12); } }
    // a limb snaps off the crown and falls, spinning, to the field
    if (o.branch !== false) { const sd = o.side ?? 1, bx = X(sd * 330), by = Y(-1300), G = Y(0) + 40 * s;
      put(L.set, `<g id="${id}-br"><g transform="translate(${f1(bx)},${f1(by)}) scale(${f1(s)})">
        <path d="M${-sd * 200},-20Q0,-60 ${sd * 160},-110" stroke="#1e1a16" stroke-width="40" fill="none" stroke-linecap="round"/><path d="M${-sd * 200},-20Q0,-60 ${sd * 160},-110" stroke="#4a3222" stroke-width="26" fill="none" stroke-linecap="round"/>
        <path d="M${-sd * 214},-34l${-sd * 26},${10}l${sd * 10},${22}z" fill="#fff2b0" opacity=".9"/>
        ${[[60, -120, 110], [160, -150, 90], [-20, -90, 80]].map(([cx, cy, rr]) => `<ellipse cx="${sd * cx}" cy="${cy}" rx="${rr}" ry="${f1(rr * 0.6)}" fill="#18301e" stroke="#1e1a16" stroke-width="4"/><ellipse cx="${sd * cx - 10}" cy="${cy - 12}" rx="${f1(rr * 0.7)}" ry="${f1(rr * 0.4)}" fill="#2a4430"/>`).join("")}</g></g>`);
      tl.set(`#${id}-br`, { opacity: 0 }, 0); tl.set(`#${id}-br`, { opacity: 1 }, t);
      const t1 = t + 0.12, T = 0.8;
      tl.fromTo(`#${id}-br`, { rotation: 0, svgOrigin: `${f1(bx - sd * 200 * s)} ${f1(by)}` }, { rotation: sd * 70, svgOrigin: `${f1(bx - sd * 200 * s)} ${f1(by)}`, duration: 0.25, ease: "power2.in", immediateRender: false }, t1);
      tl.fromTo(`#${id}-br`, { y: 0, x: 0 }, { y: G - by - 60 * s, x: sd * 120 * s, duration: T, ease: "power2.in", immediateRender: false }, t1 + 0.12);
      tl.to(`#${id}-br`, { rotation: sd * 100, duration: T, ease: "power1.in" }, t1 + 0.25); }
    return { id };
  };

  // ------------------------------------------------------------------ ground current
  SF.ground = (L, tl, t, o = {}) => {
    defs();
    const id = nid("g"), lay = L[o.layer || "glow"], s = o.s ?? 1, r = mk(o.seed ?? 31);
    let g = "", pools = "";
    (o.to || []).forEach(([tx, ty], i) => {
      const run = (ax, ay, bx, by, depth) => { const n = 9, pts = [[ax, ay]];
        for (let k = 1; k < n; k++) { const u = k / n; pts.push([ax + (bx - ax) * u + (r() - 0.5) * 70 * s, ay + (by - ay) * u + (r() - 0.5) * 22 * s]); }
        pts.push([bx, by]);
        g += `<g class="${id}-r${i}"><path d="${D(pts)}" stroke="#a8c0ff" stroke-width="${f1((16 - depth * 5) * s)}" fill="none" opacity=".5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
          <path d="${D(pts)}" stroke="#ffffff" stroke-width="${f1((5 - depth * 1.5) * s)}" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></g>`;
        if (depth < 2) pts.slice(2, -2).forEach((p) => { if (r() < 0.3) { const a = Math.atan2(by - ay, bx - ax) + (r() < 0.5 ? -1 : 1) * (0.5 + r() * 0.6), l = Math.hypot(bx - ax, by - ay) * (0.18 + r() * 0.2); run(p[0], p[1], p[0] + Math.cos(a) * l, p[1] + Math.sin(a) * l * 0.4, depth + 1); } }); };
      run(o.x, o.y, tx, ty, 0);
      pools += `<g id="${id}-p${i}" opacity="0"><ellipse cx="${tx}" cy="${ty}" rx="${f1(120 * s)}" ry="${f1(34 * s)}" fill="url(#sfPuddle)"/>${[0, 1, 2].map((k) => `<ellipse class="${id}-ring${i}" cx="${tx}" cy="${ty}" rx="${f1(40 * s)}" ry="${f1(12 * s)}" fill="none" stroke="#e8f0ff" stroke-width="${f1(3 * s)}" opacity=".8"/>`).join("")}</g>`;
    });
    put(lay, `<g id="${id}" style="mix-blend-mode:screen"><ellipse id="${id}-foot" cx="${o.x}" cy="${o.y}" rx="${f1(240 * s)}" ry="${f1(70 * s)}" fill="url(#sfPuddle)" opacity="0"/>${g}${pools}</g>`);
    const run = o.run ?? 0.14;
    tl.set(`#${id}-foot`, { opacity: 1 }, t); tl.to(`#${id}-foot`, { opacity: 0, duration: 0.5 }, t + 0.25);
    (o.to || []).forEach((_, i) => {
      const paths = `.${id}-r${i} path`;
      tl.fromTo(paths, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: run, ease: "power1.in", immediateRender: false }, t + i * 0.02);
      [[0.04, 0.3], [0.08, 1], [0.13, 0.4], [0.18, 0.9], [0.3, 0]].forEach(([dt, v]) => tl.set(`.${id}-r${i}`, { opacity: v }, t + run + dt));
      tl.set(`#${id}-p${i}`, { opacity: 1 }, t + run); tl.to(`#${id}-p${i}`, { opacity: 0, duration: 0.6, ease: "power1.in" }, t + run + 0.15);
      tl.fromTo(`.${id}-ring${i}`, { scale: 1, svgOrigin: `${o.to[i][0]} ${o.to[i][1]}` }, { scale: 3.2, opacity: 0, svgOrigin: `${o.to[i][0]} ${o.to[i][1]}`, duration: 0.6, ease: "power2.out", stagger: 0.1, immediateRender: false }, t + run);
    });
    return { id };
  };

  // ------------------------------------------------------------------ rain with depth
  // one tile of streaks covering the frame twice in height, scrolled down and sideways with the wind and looped
  const streaks = (r, n, x0, x1, H, len, wd, op, wind, col) => { let g = ""; for (let i = 0; i < n; i++) { const x = x0 + r() * (x1 - x0), y = r() * H, l = len[0] + r() * (len[1] - len[0]);
    g += `<path d="M${f1(x)},${f1(y)}l${f1(-l * wind)},${f1(l)}" stroke="${col}" stroke-width="${f1(wd[0] + r() * (wd[1] - wd[0]))}" opacity="${f1(op[0] + r() * (op[1] - op[0]))}" stroke-linecap="round"/>`; } return g; };
  SF.rain = (L, tl, t0, dur, o = {}) => {
    defs();
    const id = nid("r"), r = mk(o.seed ?? 101), wind = o.wind ?? 0.25, k = o.density ?? 1, els = [];
    const layer = (lay, name, n, len, wd, op, period, blur, x0 = -300, x1 = 1400, H = 1920, col = "#d4dcee") => {
      const tile = streaks(r, Math.round(n * k), x0, x1, H, len, wd, op, wind, col);
      put(lay, `<g id="${id}-${name}"${blur ? ` style="filter:blur(${blur}px)"` : ""}><g id="${id}-${name}m">${tile}<g transform="translate(${f1(H * wind)},${-H})">${tile}</g></g></g>`);
      const rep = Math.ceil(dur / period) + 1;
      tl.fromTo(`#${id}-${name}m`, { x: 0, y: 0 }, { x: -H * wind, y: H, duration: period, ease: "none", repeat: rep, immediateRender: false }, t0);
      els.push(`#${id}-${name}`);
    };
    // far: fine streaks behind the set (they sit in the mid layer, over the paddies, under the tree)
    if (o.far !== false) layer(L.mid, "far", 90, [26, 46], [1.2, 1.8], [0.15, 0.3], 1.4, 0, -1200, 2300, 2400, "#c8d0e2");
    // the veils: wide pale curtains of rain crossing the far field
    if (o.curtain !== false) { const hz = o.horizon ?? 980; let v = "";
      for (let i = 0; i < 4; i++) { const x = -900 + i * 760 + r() * 200, w = 260 + r() * 260; v += `<path d="M${f1(x)},${hz - 520}L${f1(x + w)},${hz - 520}L${f1(x + w - 200)},${hz + 30}L${f1(x - 200)},${hz + 30}Z" fill="url(#sfVeil)"/>`; }
      put(L.far, `<g id="${id}-veil">${v}</g>`);
      tl.fromTo(`#${id}-veil`, { x: -150 }, { x: 650, duration: Math.max(dur, 6), ease: "none", immediateRender: false }, t0); }
    // mid and near in the screen layer: in front of everything
    if (o.mid === true) layer(L.light, "mid", 150, [70, 120], [2.2, 3.4], [0.32, 0.6], 0.55, 0);
    if (o.near === true) layer(L.light, "near", 26, [190, 320], [6, 10], [0.18, 0.32], 0.34, 3.5);
    // ripples popping in the paddies
    (o.ripples || []).forEach((z, zi) => { const lay = L[z.layer || "mid"]; let g = "";
      for (let i = 0; i < (z.n ?? 24); i++) g += `<ellipse id="${id}-rp${zi}-${i}" cx="${f1(z.x + r() * z.w)}" cy="${f1(z.y + r() * z.h)}" rx="${f1(z.r ?? 16)}" ry="${f1((z.r ?? 16) * 0.3)}" fill="none" stroke="#dfe6f4" stroke-width="${f1(z.sw ?? 2.4)}" opacity="0"/>`;
      put(lay, `<g>${g}</g>`);
      for (let i = 0; i < (z.n ?? 24); i++) { const e = `#${id}-rp${zi}-${i}`, P = 0.6 + r() * 0.5, c = document.querySelector(e);
        const og = `${c.getAttribute("cx")} ${c.getAttribute("cy")}`;
        tl.fromTo(e, { scale: 0.2, opacity: 0.85, svgOrigin: og }, { scale: 2.4, opacity: 0, svgOrigin: og, duration: P, ease: "power1.out", repeat: Math.ceil(dur / P), immediateRender: false }, t0 + r() * P); } });
    // water jumping at feet (or on the bund, a roof edge…): a little crown of droplets and a ring, again and again
    (o.splash || []).forEach(([x, y, s = 1], si) => { let g = "";
      for (let j = 0; j < 3; j++) { g += `<g id="${id}-sp${si}-${j}" opacity="0"><ellipse cx="${x + (j - 1) * 34 * s}" cy="${y}" rx="${f1(26 * s)}" ry="${f1(7 * s)}" fill="none" stroke="#e8eef8" stroke-width="${f1(3 * s)}"/>${[-1, -0.4, 0.4, 1].map((a) => `<circle class="${id}-dr${si}-${j}" cx="${x + (j - 1) * 34 * s}" cy="${y}" r="${f1(4 * s)}" fill="#e8eef8" data-a="${a}"/>`).join("")}</g>`; }
      put(L.act || L.set, `<g>${g}</g>`);
      for (let j = 0; j < 3; j++) { const P = 0.42 + j * 0.07, e = `#${id}-sp${si}-${j}`, rep = Math.ceil(dur / P);
        tl.fromTo(e, { opacity: 1, scale: 0.4, svgOrigin: `${x + (j - 1) * 34 * s} ${y}` }, { opacity: 0, scale: 1.4, svgOrigin: `${x + (j - 1) * 34 * s} ${y}`, duration: P, ease: "power1.out", repeat: rep, immediateRender: false }, t0 + j * 0.13);
        document.querySelectorAll(`.${id}-dr${si}-${j}`).forEach((d) => { const a = +d.dataset.a;
          tl.fromTo(d, { x: 0, y: 0 }, { keyframes: [{ x: a * 22 * s, y: -38 * s * (1.2 - Math.abs(a) * 0.4), duration: P * 0.45, ease: "power2.out" }, { x: a * 34 * s, y: 4 * s, duration: P * 0.55, ease: "power2.in" }], repeat: rep, immediateRender: false }, t0 + j * 0.13); }); } });
    return { id, els: els.map((s) => document.querySelector(s)).filter(Boolean) };
  };

  // ------------------------------------------------------------------ wind
  SF.wind = (L, tl, t0, dur, o = {}) => {
    defs();
    const id = nid("w"), r = mk(o.seed ?? 202), dir = o.dir ?? 1;
    // rice in front of the lens: out of focus (the fg layer blurs), rolling in a wave that runs across the frame
    if (o.rice) { const n = o.rice === true ? 16 : o.rice, base = o.riceY ?? 2010; let g = "";
      for (let i = 0; i < n; i++) { const x = -80 + i * (1240 / n) + r() * 30, h = 260 + r() * 200, c = o.riceCol || "#2a4628";
        g += `<g id="${id}-ri${i}"><path d="M${f1(x)},${base}q-14,-${f1(h * 0.6)} -${f1(36 + r() * 20)},-${f1(h)}M${f1(x + 12)},${base}q10,-${f1(h * 0.7)} ${f1(26 + r() * 14)},-${f1(h * 1.08)}M${f1(x + 24)},${base}q28,-${f1(h * 0.5)} ${f1(60 + r() * 20)},-${f1(h * 0.88)}M${f1(x + 6)},${base}q2,-${f1(h * 0.8)} ${f1(-4 + r() * 8)},-${f1(h * 1.2)}" stroke="${c}" stroke-width="${f1(14 + r() * 6)}" fill="none" stroke-linecap="round"/>
          <path d="M${f1(x + 6)},${f1(base - h * 1.2)}q10,30 4,70" stroke="#6a7a3a" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/></g>`; }
      put(L.fg, `<g>${g}</g>`);
      for (let i = 0; i < n; i++) { const x = -80 + i * (1240 / n), P = 1.1;
        tl.fromTo(`#${id}-ri${i}`, { rotation: -3 * dir, svgOrigin: `${f1(x + 12)} ${base}` }, { rotation: 11 * dir, svgOrigin: `${f1(x + 12)} ${base}`, duration: P / 2, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / (P / 2)) + 1, immediateRender: false }, t0 + (dir > 0 ? i : n - i) / n * P * 0.8); } }
    // ผ้าแพร tails: a chain of segments, each turning a little after the one before → a travelling flutter
    (o.ribbons || []).forEach(([x, y, len, col], bi) => { const N = 7, seg = len / N; let g = "", close = "";
      for (let j = 0; j < N; j++) { g += `<g transform="translate(${j ? f1(seg) : f1(x)},${j ? 0 : f1(y)})"><g id="${id}-rb${bi}-${j}"><path d="M0,${f1(-10 + j * 0.6)}L${f1(seg + 2)},${f1(-9 + j * 0.7)}L${f1(seg + 2)},${f1(9 - j * 0.7)}L0,${f1(10 - j * 0.6)}Z" fill="${col}" stroke="#1e1a16" stroke-width="2.5"/>`; close += "</g></g>"; }
      put(L.set, g + close);
      for (let j = 0; j < N; j++) { const P = 0.5 + r() * 0.12;
        tl.fromTo(`#${id}-rb${bi}-${j}`, { rotation: j ? -7 : 28 * dir, svgOrigin: "0 0" }, { rotation: j ? 7 : 44 * dir, svgOrigin: "0 0", duration: P / 2, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / (P / 2)) + 1, immediateRender: false }, t0 + j * 0.06 + bi * 0.1); } });
    // leaves torn off and blown across the frame (screen layer), tumbling
    if (o.leaves) { let g = "";
      for (let i = 0; i < o.leaves; i++) g += `<g transform="translate(${dir > 0 ? -80 : 1160},${f1(200 + r() * 1300)})"><g id="${id}-lf${i}"><path d="M0,0q18,-16 36,0q-18,16 -36,0z" fill="${["#2e5a2e", "#4a7a3a", "#6a8a3a"][i % 3]}" stroke="#14281a" stroke-width="2"/><path d="M0,0h34" stroke="#14281a" stroke-width="1.6"/></g></g>`;
      put(L.light, `<g>${g}</g>`);
      for (let i = 0; i < o.leaves; i++) { const P = 1.2 + r() * 0.9, e = `#${id}-lf${i}`;
        tl.fromTo(e, { x: 0, y: 0, rotation: 0, svgOrigin: "18 0" }, { x: dir * (1300 + r() * 200), y: -120 + r() * 360, rotation: dir * (540 + r() * 540), svgOrigin: "18 0", duration: P, ease: "none", repeat: Math.ceil(dur / P), immediateRender: false }, t0 + r() * P); } }
    return { id };
  };
})();
