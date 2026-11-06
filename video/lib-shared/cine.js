// cine.js — the CINEMA BIBLE layer (owner, 6 Nov 2569) on top of engine.js. Built once, used by every new story.
// Rules: video/release/CINEMA-BIBLE.md · checker: .claude/skills/rodmai-club-video/scripts/shotlist_check.py
//
// One call styles a whole episode from the two plans the visual desk writes before rendering:
//   Cine.episode(shots, { shotlist, colorscript })      // call it right before Engine.build(root, tl, shots)
//     shotlist    = { cuts: [{ n, key, t, dur, emotion, size, angle, move, ... }] }   (absolute times, one entry per cut)
//     colorscript = { bands: [{ from, to, stage }], keep: "yellow" | "red" | "orange" | null, overrides: { stage: {...} } }
//   Per cut it sets the grade of its stage, the vignette, the grain, the parallax and a camera modifier:
//     handheld breathing noise (±2 px, ~0.3 Hz) on every cut except emotion "choice" and move "hold"
//     move "cut" / "hold" / emotion "hook" / "choice": the camera is frozen at the cut's first frame (no drift)
//     move "dutch" (cut.deg, default 10): tilt + zoom that keeps the frame covered (cut.cover === false to skip the zoom)
//     move "whip" (cut.dir ±1): 0.2 s whip-pan into the cut with motion blur
//     move "shake": a short rumble (0.45 s) at the start of the cut, never held
//   Optional per cut: dof { layer: px } · rack { at, dur, to: { layer: px } } · lowkey { cx, cy, r, dark, keys? }
//     flicker: true | { n, depth, kind: "dark" | "flash" } · silhouette: "<css selector inside the shot>" (rim: "cold" | "warm")
//
// Building blocks (for hand-made shots; Cine.episode uses the same pieces):
//   Cine.grade(stage, keep?) → filter url · Cine.vignette(strength) → look.vignette value
//   Cine.grain() → { grain } fine layer (the coarse shadow layer lives inside every grade filter)
//   Cine.dof(layer, px) → { blur } · Cine.parallax(groups, ratios) → { parallax }
//   Cine.cam.pushIn(from, to) / pullOut(from, to) / holdStill(at) / whip(from, to, at) / dutch(at, deg) → { cam }
//   Cine.flicker(opts) → fx function · Cine.fx(f1, f2, …) chains fx functions
//   Cine.STAGES holds the colour-script numbers (feColorMatrix, saturation, tone tables) for the colour-script sheet.
(function () {
  const W = 1080, H = 1920;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const f3 = (v) => (+v).toFixed(3);
  const ease = (k) => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);
  const easeOut = (k) => 1 - Math.pow(1 - clamp(k), 3);

  // ---- colour script ----------------------------------------------------------------------------
  // teal shadows / amber highlights as offsets from the identity curve at 9 points (scaled per stage by `split`),
  // plus an S-curve for contrast (scaled by `contrast`)
  const ID = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1];
  const SPLIT = {
    R: [0, -0.02, -0.02, -0.008, 0.006, 0.018, 0.024, 0.018, 0],
    G: [0.012, 0.008, 0.002, 0, 0, 0, 0, -0.006, -0.02],
    B: [0.05, 0.045, 0.032, 0.018, 0, -0.018, -0.035, -0.05, -0.065],
  };
  const SCURVE = [0, -0.022, -0.034, -0.022, 0, 0.022, 0.034, 0.022, 0];
  const STAGES = {
    // ปลอดภัย: อุ่น อิ่มสี
    safe: { mat: [1.04, 0, 0, 0, 0.012, 0, 1.0, 0, 0, 0.004, 0, 0, 0.95, 0, 0, 0, 0, 0, 1, 0], sat: 1.12, split: 0.7, contrast: 0.3, vig: 0.18, grain: 0.35 },
    // ผิดปกติ: สีจางลง 30% (1.12 → 0.78) เย็นลงนิดหนึ่ง
    uneasy: { mat: [0.98, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 1.03, 0, 0.01, 0, 0, 0, 1, 0], sat: 0.78, split: 0.9, contrast: 0.5, vig: 0.25, grain: 0.45 },
    // ภัย: เย็น เขียวอมเทา ลดอีก 20% (0.78 → 0.62) contrast ขึ้น
    threat: { mat: [0.88, 0.04, 0, 0, 0, 0, 0.98, 0.03, 0, 0.012, 0, 0.05, 1.0, 0, 0.022, 0, 0, 0, 1, 0], sat: 0.62, split: 1.0, contrast: 0.8, vig: 0.32, grain: 0.55 },
    // ภัยแบบแดงแคบจากแหล่งแสงเดียว (ไฟไหม้ ไฟฉุกเฉิน): ใช้คู่กับ keep "red"
    red: { mat: [1.0, 0, 0, 0, 0, 0, 0.9, 0, 0, 0, 0, 0, 0.88, 0, 0, 0, 0, 0, 1, 0], sat: 0.6, split: 0.8, contrast: 0.8, vig: 0.32, grain: 0.55 },
  };
  // the one colour that stays saturated in every stage: alpha = a·R + b·G + c·B + d (then clipped to 0–1)
  //   yellow: (R+G)/2 − B > 0.45 → vinegar bottle, duck float · sand and skin stay out
  const KEEP = { yellow: [4, 4, -8, -3.6], red: [8, -4, -4, -3.2], orange: [6, 2, -8, -4] };
  const FEAR_VIG = 0.4; // ขอบมืด 40% ในช็อตกลัว
  const curve = (ch, st) => ID.map((v, i) => f3(clamp(v + SPLIT[ch][i] * st.split + SCURVE[i] * st.contrast))).join(" ");

  function stageOf(name, overrides) {
    const base = STAGES[name] || STAGES.safe;
    return { ...base, ...((overrides || {})[name] || {}) };
  }

  function gradeFilter(name, st, keep) {
    const k = keep && KEEP[keep];
    const g = window.GRAIN_PNG;
    // coarse grain only in the shadows: tile the grain texture big, mask it with (1 − 2·luminance), overlay it
    const grain = g ? `
      <feImage class="cine-gi" href="${g}" x="0" y="0" width="640" height="640" preserveAspectRatio="none" result="gi"/>
      <feTile in="gi" result="gt"/>
      <feColorMatrix in="tone" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -0.425 -1.43 -0.144 0 1.15" result="sh"/>
      <feComposite in="sh" in2="SourceAlpha" operator="in" result="sh2"/>
      <feComposite in="gt" in2="sh2" operator="in" result="gs"/>
      <feComponentTransfer in="gs" result="gs2"><feFuncA type="linear" slope="${f3(st.grain)}"/></feComponentTransfer>
      <feBlend in="gs2" in2="tone" mode="overlay" result="graded"/>` : `<feOffset in="tone" result="graded"/>`;
    const keepChain = k ? `
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  ${k[0]} ${k[1]} ${k[2]} 0 ${k[3]}" result="ka"/>
      <feComposite in="ka" in2="SourceAlpha" operator="in" result="kb"/>
      <feComposite in="SourceGraphic" in2="kb" operator="in" result="kc"/>
      <feMerge><feMergeNode in="graded"/><feMergeNode in="kc"/></feMerge>` : "";
    return `<filter id="cine-${name}${k ? "-" + keep : ""}" filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix" values="${st.mat.join(" ")}" result="m"/>
      <feColorMatrix in="m" type="saturate" values="${f3(st.sat)}" result="s"/>
      <feComponentTransfer in="s" result="tone"><feFuncR type="table" tableValues="${curve("R", st)}"/><feFuncG type="table" tableValues="${curve("G", st)}"/><feFuncB type="table" tableValues="${curve("B", st)}"/></feComponentTransfer>${grain}${keepChain}
    </filter>`;
  }

  const SIL = { cold: "#cfe8ff", warm: "#ffd9a0" };
  const silFilter = (rim, col) => `<filter id="cine-sil-${rim}" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.03  0 0 0 0 0.04  0 0 0 1 0" result="black"/>
      <feMorphology in="SourceAlpha" operator="erode" radius="3" result="er"/>
      <feComposite in="SourceAlpha" in2="er" operator="out" result="edge"/>
      <feGaussianBlur in="edge" stdDeviation="2" result="edgeB"/>
      <feFlood flood-color="${col}" flood-opacity=".85"/>
      <feComposite in2="edgeB" operator="in" result="rim"/>
      <feMerge><feMergeNode in="black"/><feMergeNode in="rim"/></feMerge></filter>`;

  let installed = null; // the colour script the filters were built for
  function install(colorscript) {
    if (installed) return;
    installed = colorscript || {};
    const keep = installed.keep || null;
    const ov = installed.overrides || {};
    const defs = Object.keys(STAGES).map((n) => gradeFilter(n, stageOf(n, ov), null) + (keep ? gradeFilter(n, stageOf(n, ov), keep) : "")).join("")
      + Object.entries(SIL).map(([k, c]) => silFilter(k, c)).join("");
    document.body.insertAdjacentHTML("afterbegin", `<svg id="cine-defs" width="0" height="0" style="position:absolute"><defs>${defs}</defs></svg>`);
  }
  const grade = (stage, keep) => `url(#cine-${STAGES[stage] ? stage : "safe"}${keep && KEEP[keep] ? "-" + keep : ""})`;

  // ---- camera ------------------------------------------------------------------------------------
  // handheld breathing noise: ±2 px at ~0.3 Hz with a smaller second wobble, a hair of roll
  const handheld = (t, seed, amp = 1) => {
    const p = seed * 1.7;
    return {
      x: amp * (2.0 * Math.sin(2 * Math.PI * 0.3 * t + p) + 0.6 * Math.sin(2 * Math.PI * 0.71 * t + 2.1 * p)),
      y: amp * (1.4 * Math.sin(2 * Math.PI * 0.27 * t + 0.6 * p) + 0.5 * Math.sin(2 * Math.PI * 0.63 * t + 1.3 * p)),
      r: amp * 0.05 * Math.sin(2 * Math.PI * 0.21 * t + 0.9 * p),
    };
  };
  const coverZoom = (deg) => { const a = (Math.abs(deg) * Math.PI) / 180; return Math.cos(a) + (H / W) * Math.sin(a); };
  const FROZEN = { cut: 1, hold: 1 };

  function camModFor(sh, cuts, seed) {
    return (t, c, camAt) => {
      const cut = cuts.find((u) => t >= u.lt && t < u.lt + u.dur) || cuts[cuts.length - 1];
      if (!cut) return c;
      const u = t - cut.lt, emo = cut.emotion, mv = cut.move;
      let { x, y, s, hx, hy, r } = c;
      const still = emo === "choice" || mv === "hold";
      if (still || FROZEN[mv] || emo === "hook") ({ x, y, s } = camAt(cut.lt)); // no drift inside the cut
      if (still || emo === "hook") { hx = 0; hy = 0; r = 0; } // the bible: the hook cuts, never shakes · the choice is dead still
      if (!still) {
        const n = handheld(t + cut.lt * 0.37, seed + cut.n, emo === "hook" ? 0.5 : 1);
        hx += n.x; hy += n.y; r += n.r;
      }
      if (mv === "dutch") {
        const deg = cut.deg ?? 10, k = easeOut(u / 0.15);
        r += deg * k;
        if (cut.cover !== false) s *= 1 + (coverZoom(deg) - 1) * k;
      }
      if (mv === "whip" && u < 0.2) x += (cut.dir || 1) * 640 * Math.pow(1 - easeOut(u / 0.2), 2);
      if (mv === "shake" && u < 0.45) {
        const d = 1 - u / 0.45;
        hx += 14 * d * Math.sin(u * 70); hy += 9 * d * Math.sin(u * 53); r += 0.6 * d * Math.sin(u * 41);
      }
      return { x, y, s, hx, hy, r };
    };
  }

  const cam = {
    pushIn: (from, to) => ({ cam: { from, to, ease: "linear" } }),
    pullOut: (from, to) => ({ cam: { from, to, ease: "linear" } }),
    holdStill: (at) => ({ cam: { keys: [{ t: 0, ...at, drift: { s: 0 } }] } }),
    whip: (from, to, at) => ({ cam: { keys: [{ t: 0, ...from, drift: { s: 0 } }, { t: at, ...to, drift: { s: 0 } }] } }),
    dutch: (at, deg = 10) => ({ cam: { keys: [{ t: 0, ...at, s: at.s * coverZoom(deg), drift: { s: 0 } }] }, shake: () => ({ x: 0, y: 0, r: deg }) }),
  };

  // ---- fx pieces ---------------------------------------------------------------------------------
  let lastFlash = -1e9; // V1b: at most one bright flash per 10 s, layer ≤ .28
  const rng = (seed) => { let a = seed * 9301 + 49297; return () => ((a = (a * 9301 + 49297) % 233280) / 233280); };

  function flickerFx(cut, id, start, tl, div) {
    const o = cut.flicker === true ? {} : cut.flicker;
    const n = clamp(o.n ?? 2 + (cut.n % 2), 1, 3), R = rng(cut.n + 7);
    for (let i = 0; i < n; i++) {
      const at = start + cut.lt + (0.15 + R() * 0.7) * cut.dur, len = 0.05 + R() * 0.07;
      if ((o.kind || "dark") === "flash") {
        if (at - lastFlash < 10) continue;
        lastFlash = at;
        let fl = document.getElementById(`${id}-cineflash`);
        if (!fl) { div.querySelector("svg.stage").insertAdjacentHTML("beforeend", `<rect id="${id}-cineflash" width="${W}" height="${H}" fill="#eef4ff" opacity="0"/>`); fl = document.getElementById(`${id}-cineflash`); }
        tl.to(fl, { attr: { opacity: Math.min(0.28, o.depth ?? 0.22) }, duration: 0.03, ease: "none" }, at);
        tl.to(fl, { attr: { opacity: 0 }, duration: len, ease: "none" }, at + 0.03);
      } else {
        const dk = document.getElementById(`${id}-dark`);
        const base = +dk.getAttribute("opacity");
        tl.to(dk, { attr: { opacity: clamp(base + (o.depth ?? 0.45)) }, duration: 0.02, ease: "none" }, at);
        tl.to(dk, { attr: { opacity: base }, duration: len, ease: "none" }, at + 0.02);
      }
    }
  }

  function lowkeyFx(cut, id, start, tl, div) {
    const o = cut.lowkey, svg = div.querySelector("svg.stage"), gid = `${id}-lk${cut.n}`;
    svg.querySelector("defs").insertAdjacentHTML("beforeend", `<radialGradient id="${gid}g" gradientUnits="userSpaceOnUse" cx="${o.cx ?? 540}" cy="${o.cy ?? 900}" r="${o.r ?? 520}">
      <stop offset="0" stop-color="#04070a" stop-opacity="0"/><stop offset=".55" stop-color="#04070a" stop-opacity="${f3((o.dark ?? 0.65) * 0.6)}"/><stop offset="1" stop-color="#04070a" stop-opacity="${f3(o.dark ?? 0.65)}"/></radialGradient>`);
    const vig = document.getElementById(`${id}-vig`);
    const html = `<rect id="${gid}" width="${W}" height="${H}" fill="url(#${gid}g)" opacity="0"/>`;
    if (vig) vig.insertAdjacentHTML("beforebegin", html); else svg.insertAdjacentHTML("beforeend", html);
    const el = document.getElementById(gid), gr = document.getElementById(`${gid}g`);
    tl.set(el, { attr: { opacity: 1 } }, start + cut.lt);
    tl.set(el, { attr: { opacity: 0 } }, start + cut.lt + cut.dur);
    (o.keys || []).forEach((k, i, ks) => { if (i) tl.to(gr, { attr: { cx: k.cx, cy: k.cy, r: k.r ?? o.r ?? 520 }, duration: k.t - ks[i - 1].t, ease: "none" }, start + cut.lt + ks[i - 1].t); });
  }

  function layerBlur(L, layer, px) { if (L[layer]) L[layer].style.filter = px > 0.05 ? `blur(${f3(px)}px)` : "none"; }

  // ---- the episode pass --------------------------------------------------------------------------
  function bandStage(t, bands) {
    const b = (bands || []).find((x) => t >= x.from && t < x.to);
    return b ? b.stage : null;
  }

  function episode(shots, plan = {}) {
    const cs = plan.colorscript || {}, keep = cs.keep || null, cutsAll = ((plan.shotlist || {}).cuts || []).slice().sort((a, b) => a.t - b.t);
    shots.forEach((sh, si) => {
      const end = sh.start + sh.dur;
      let cuts = cutsAll.filter((c) => c.t >= sh.start - 1e-3 && c.t < end - 1e-3).map((c) => ({ ...c, lt: Math.max(0, c.t - sh.start), dur: Math.min(c.dur, end - c.t) }));
      if (!cuts.length || cuts[0].lt > 1e-3) cuts.unshift({ n: 1000 + si, key: sh.key, lt: 0, dur: cuts.length ? cuts[0].lt : sh.dur, emotion: cuts.length ? cuts[0].emotion : "safe", move: "pushIn", implicit: true });
      cuts.forEach((c) => { c.stage = c.stage || bandStage(sh.start + c.lt, cs.bands) || (c.emotion === "fear" || c.emotion === "choice" ? "threat" : c.emotion === "uneasy" ? "uneasy" : "safe"); });
      const ov = cs.overrides || {};
      const vigOf = (c) => (c.emotion === "fear" ? FEAR_VIG : stageOf(c.stage, ov).vig) / 0.85; // lookVig is .85 black at the edge
      sh.look = { ...(sh.look || {}), vignette: vigOf(cuts[0]), grain: (sh.look && sh.look.grain) || 0.07 };
      sh.parallax = { far: 0.3, ...(sh.parallax || {}) };
      sh.camMod = camModFor(sh, cuts, si * 3 + 1);
      const prevFx = sh.fx, baseBlur = { ...(sh.blur || {}) };
      sh.fx = (tl, id, start, L) => {
        install(cs);
        const div = document.getElementById(id), world = document.getElementById(`${id}-world`), vig = document.getElementById(`${id}-vig`);
        cuts.forEach((c, k) => {
          const at = start + c.lt;
          tl.set(world, { attr: { filter: grade(c.stage, keep) } }, at);
          if (vig) tl.set(vig, { attr: { opacity: f3(vigOf(c)) } }, at);
          if (c.dof) Object.entries(c.dof).forEach(([layer, px]) => tl.call(() => layerBlur(L, layer, px), null, at));
          if (c.rack) {
            const from = { ...baseBlur, ...(c.dof || {}) }, to = c.rack.to || {}, p = { k: 0 };
            tl.fromTo(p, { k: 0 }, { k: 1, duration: c.rack.dur ?? 0.4, ease: "power1.inOut", immediateRender: false,
              onUpdate: () => Object.keys({ ...from, ...to }).forEach((layer) => layerBlur(L, layer, (from[layer] || 0) + ((to[layer] || 0) - (from[layer] || 0)) * p.k)) }, at + (c.rack.at ?? 0));
          }
          if (c.move === "whip") {
            const p = { k: 0 }, base = { ...baseBlur, ...(c.dof || {}) };
            tl.fromTo(p, { k: 1 }, { k: 0, duration: 0.2, ease: "power2.out", immediateRender: false,
              onUpdate: () => ["far", "mid", "set", "act"].forEach((layer) => layerBlur(L, layer, (base[layer] || 0) + 12 * p.k)) }, at);
          }
          if (c.flicker) flickerFx(c, id, start, tl, div);
          if (c.lowkey) lowkeyFx(c, id, start, tl, div);
          if (c.silhouette) {
            const els = div.querySelectorAll(c.silhouette);
            els.forEach((el) => {
              const orig = el.getAttribute("filter") || "none";
              tl.set(el, { attr: { filter: `url(#cine-sil-${c.rim || "cold"})` } }, at);
              tl.set(el, { attr: { filter: orig } }, at + c.dur);
            });
          }
          if (k === 0) world.setAttribute("filter", grade(c.stage, keep));
        });
        // the coarse grain moves every frame like real film grain (24 fps cadence)
        const gis = () => document.querySelectorAll("#cine-defs .cine-gi");
        const q = { k: 0 };
        tl.to(q, { k: 1, duration: sh.dur, ease: "none", onUpdate: () => {
          const f = Math.floor(q.k * sh.dur * 24) + si * 13, gx = -((f * 97) % 256) * 2.5, gy = -((f * 61) % 256) * 2.5;
          gis().forEach((g) => { g.setAttribute("x", gx); g.setAttribute("y", gy); });
        } }, start);
        if (prevFx) prevFx(tl, id, start, L);
      };
    });
    return shots;
  }

  const fx = (...fns) => (tl, id, start, L) => fns.forEach((f) => f && f(tl, id, start, L));
  const flicker = (opts = {}) => (tl, id, start) => flickerFx({ n: opts.seed ?? 1, lt: opts.at ?? 0, dur: opts.dur ?? 1.5, flicker: opts }, id, start, tl, document.getElementById(id));

  window.Cine = {
    STAGES, KEEP, FEAR_VIG,
    install, episode, grade, cam, fx, flicker, handheld, coverZoom,
    vignette: (strength) => strength / 0.85,
    grain: () => ({ grain: 0.07 }),
    dof: (layer, px) => ({ blur: { [layer]: px } }),
    parallax: (groups, ratios) => ({ parallax: Object.fromEntries(groups.map((g, i) => [g, ratios[i]])) }),
    curves: (stage) => { const st = stageOf(stage); return { R: curve("R", st), G: curve("G", st), B: curve("B", st) }; },
  };
})();
