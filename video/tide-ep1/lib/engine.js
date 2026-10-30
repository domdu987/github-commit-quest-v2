// Episode engine: turns a declarative list of shots into HyperFrames clips + one GSAP timeline.
// A shot = one set (layered), a camera move with parallax, actors driven by Rig tracks, captions,
// small UI cards, speech bubbles and simple FX. All motion is a pure function of timeline time.
(function () {
  const PARALLAX = { sky: 0.05, far: 0.25, mid: 0.6, set: 1, act: 1, fg: 1.5 };
  const lerp = (a, b, k) => a + (b - a) * k;
  const f2 = (v) => (+v).toFixed(1);
  const ease = (k) => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);
  // glide eases by name (key.ease): "drop" falls faster and faster, then brakes hard on the landing
  const EASES = { drop: (k) => (k < 0.8 ? 0.85 * Math.pow(k / 0.8, 2.2) : 0.85 + 0.15 * (1 - Math.pow(1 - (k - 0.8) / 0.2, 2))) };

  function build(root, tl, shots) {
    root.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute"><defs>${Sets.DEFS}
      <radialGradient id="lookVig" cx=".5" cy=".46" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient>
      <radialGradient id="lookCast"><stop offset="0" stop-color="#000" stop-opacity=".8"/><stop offset=".6" stop-color="#000" stop-opacity=".35"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
      ${window.GRAIN_PNG ? `<pattern id="lookGrain" width="256" height="256" patternUnits="userSpaceOnUse"><image href="${window.GRAIN_PNG}" width="256" height="256"/></pattern>` : ""}</defs></svg>`);
    shots.forEach((sh, i) => buildShot(root, tl, sh, i));
  }

  function buildShot(root, tl, sh, i) {
    const id = `s${i}`;
    const div = document.createElement("div");
    div.className = "clip";
    div.id = id;
    div.setAttribute("data-start", sh.start);
    div.setAttribute("data-duration", sh.dur);
    div.setAttribute("data-track-index", "0");
    const look = { ...(Engine.look || {}), ...(sh.look || {}) };
    div.innerHTML = `<svg class="stage" width="1080" height="1920" viewBox="0 0 1080 1920"><defs id="${id}-defs"></defs>
        <g id="${id}-world">${Object.keys(PARALLAX).map((L) => `<g id="${id}-${L}"${L === "fg" ? ' class="fgblur"' : ""}></g>`).join("")}</g>
        <rect id="${id}-dark" width="1080" height="1920" fill="#05090c" opacity="${sh.dark ?? 0.35}" style="mix-blend-mode:multiply"/>
        <g id="${id}-glow"></g>
        <g id="${id}-light"></g>
        <rect id="${id}-fog" x="-200" y="0" width="1480" height="1920" fill="#c9c3b6" opacity="0"/>
        ${sh.grade ? `<rect id="${id}-grade" width="1080" height="1920" fill="url(#${id}-gradeg)" opacity="${sh.grade.op ?? 0.5}" style="mix-blend-mode:${sh.grade.blend || "soft-light"}"/>` : ""}
        ${look.vignette ? `<rect id="${id}-vig" width="1080" height="1920" fill="url(#lookVig)" opacity="${look.vignette}"/>` : ""}
        ${look.grain && window.GRAIN_PNG ? `<rect id="${id}-grain" x="-256" y="-256" width="1600" height="2440" fill="url(#lookGrain)" opacity="${look.grain}" style="mix-blend-mode:overlay"/>` : ""}
      </svg>
      <div class="capwrap" id="${id}-caps"></div>`;
    root.appendChild(div);
    const L = {}; Object.keys(PARALLAX).forEach((k) => (L[k] = document.getElementById(`${id}-${k}`)));
    const defs = document.getElementById(`${id}-defs`);
    if (sh.grade) defs.insertAdjacentHTML("beforeend", `<linearGradient id="${id}-gradeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${sh.grade.top}"/><stop offset="1" stop-color="${sh.grade.bottom || sh.grade.top}"/></linearGradient>`);
    // key light on the cast: a rim on the lit edge, a soft core shadow on the far edge (one filter per facing), and a cast shadow on the ground
    const lt = sh.light === false ? null : sh.light || look.light;
    if (lt) {
      const dir = lt.from === "right" ? 1 : -1;
      [["", dir], ["F", -dir]].forEach(([suf, d]) => defs.insertAdjacentHTML("beforeend", `<filter id="${id}-lit${suf}" x="-25%" y="-15%" width="150%" height="130%" color-interpolation-filters="sRGB">
        <feOffset in="SourceAlpha" dx="${-d * (lt.rimW ?? 5)}" dy="1" result="o1"/><feComposite in="SourceAlpha" in2="o1" operator="out" result="rA"/>
        <feFlood flood-color="${lt.rim || "#ffe6b8"}" flood-opacity="${lt.rimOp ?? 0.85}"/><feComposite in2="rA" operator="in" result="rim"/>
        <feOffset in="SourceAlpha" dx="${d * (lt.shadeW ?? 34)}" dy="-4" result="o2"/><feComposite in="SourceAlpha" in2="o2" operator="out" result="sA"/>
        <feGaussianBlur in="sA" stdDeviation="${lt.soft ?? 10}" result="sB"/><feComposite in="sB" in2="SourceAlpha" operator="in" result="sC"/>
        <feFlood flood-color="${lt.shade || "#1c1430"}" flood-opacity="${lt.shadeOp ?? 0.5}"/><feComposite in2="sC" operator="in" result="shd"/>
        <feGaussianBlur in="rim" stdDeviation="1.6" result="rimS"/>
        ${lt.vol === false ? `<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shd"/><feMergeNode in="rimS"/></feMerge></filter>` : `        <feGaussianBlur in="SourceAlpha" stdDeviation="${lt.round ?? 12}" result="bump"/>
        <feDiffuseLighting in="bump" surfaceScale="${lt.depth ?? 7}" diffuseConstant="1" lighting-color="#ffffff" result="dl"><feDistantLight azimuth="${d < 0 ? 210 : 330}" elevation="42"/></feDiffuseLighting>
        <feComponentTransfer in="dl" result="dl2"><feFuncR type="linear" slope="1.38" intercept="0.04"/><feFuncG type="linear" slope="1.38" intercept="0.04"/><feFuncB type="linear" slope="1.32" intercept="0.07"/></feComponentTransfer>
        <feBlend in="SourceGraphic" in2="dl2" mode="multiply" result="vol"/><feComposite in="vol" in2="SourceAlpha" operator="in" result="volIn"/>
        <feMerge><feMergeNode in="volIn"/><feMergeNode in="shd"/><feMergeNode in="rimS"/></feMerge></filter>`}`));
    }
    L.glow = document.getElementById(`${id}-glow`); // light sources above the darkness, moving with the set
    L.light = document.getElementById(`${id}-light`);
    if (sh.set) Sets[sh.set](L, sh.setOpts || {});
    if (sh.extra) sh.extra(L, id);

    // actors
    (sh.actors || []).forEach((a, k) => {
      const aid = `${id}-a${k}`;
      if (a.who === "cat") {
        Rig.buildCat(L.act, aid).setAttribute("transform", `translate(${a.x},${a.y}) scale(${a.flip ? -a.s : a.s},${a.s})`);
        Rig.driveCat(tl, aid, sh.start, sh.dur, a.track);
      } else if (a.who === "ghost") {
        L.act.insertAdjacentHTML("beforeend", ghost(aid, a));
        if (a.track) a.track(tl, aid, sh.start);
      } else {
        Rig.build(L.act, aid, Rig.CAST[a.who]);
        const g = document.getElementById(aid);
        g.setAttribute("transform", `translate(${a.x},${a.y}) scale(${a.flip ? -a.s : a.s},${a.s})`);
        Rig.drive(tl, aid, sh.start, sh.dur, a.track, a.blinks || [0.9, 2.7, 4.6]);
        if (lt && a.lit !== false) {
          document.getElementById(`${aid}-root`).setAttribute("filter", `url(#${id}-lit${a.flip ? "F" : ""})`);
          const cs = lt.cast ?? { len: 2.2, op: 0.4 }, d = (lt.from === "right" ? 1 : -1) * (a.flip ? -1 : 1);
          if (cs) document.getElementById(`${aid}-shadow`).insertAdjacentHTML("beforebegin", `<ellipse cx="${-d * 70 * cs.len}" cy="8" rx="${f2(80 * cs.len)}" ry="20" fill="url(#lookCast)" opacity="${cs.op}"/>`);
        }
        if (a.prop && window.Camp) Camp.attach(aid, a.prop);
        if (a.path) { // walk a route [{ t, x, y, flip }] (t = seconds into the shot; each leg faces the way its first point says): stairs, turns
          const P = a.path, c = { t: 0 };
          // a point may carry its own scale s (walking toward or away from the camera grows or shrinks the character)
          const pos = (t) => { let i = 0; while (i < P.length - 1 && t > P[i + 1].t) i++; const p = P[i], q = P[Math.min(i + 1, P.length - 1)];
            const k = q.t > p.t ? Math.min(1, Math.max(0, (t - p.t) / (q.t - p.t))) : 1;
            return [lerp(p.x, q.x, k), lerp(p.y, q.y, k), p.flip ?? a.flip, lerp(p.s ?? a.s, q.s ?? p.s ?? a.s, k)]; };
          const put0 = (t) => { const [x, y, f, sc] = pos(t); g.setAttribute("transform", `translate(${x},${y}) scale(${f ? -sc : sc},${sc})`); };
          put0(0);
          tl.to(c, { t: sh.dur, duration: sh.dur, ease: "none", onUpdate: () => put0(c.t) }, sh.start);
        }
        if (a.moveTo) { // walk across the set: translate the whole character in sync with the shot clock
          const m = { k: 0 };
          tl.to(m, { k: 1, duration: a.moveTo.dur, ease: a.moveTo.ease || "none", onUpdate: () => {
            const x = lerp(a.x, a.moveTo.x, m.k), y = lerp(a.y, a.moveTo.y ?? a.y, m.k), sc = lerp(a.s, a.moveTo.s ?? a.s, m.k); // moveTo.s: the scale at the end
            g.setAttribute("transform", `translate(${x},${y}) scale(${a.flip ? -sc : sc},${sc})`);
          } }, sh.start + (a.moveTo.at || 0));
        }
      }
      // optional visibility window (lets a shot swap in a turned-around copy of a character)
      if (a.from !== undefined) { tl.set(`#${aid}`, { opacity: 0 }, sh.start); tl.set(`#${aid}`, { opacity: 1 }, sh.start + a.from); }
      if (a.until !== undefined) tl.set(`#${aid}`, { opacity: 0 }, sh.start + a.until);
    });

    // camera: interpolate {x,y,s} and apply per-layer parallax around the frame centre.
    // cam.keys = [{t, x, y, s, drift?, glide?}] gives several framings in one shot: hard cuts at each key
    // (a slow push-in, or `drift` per second, while held), or an eased move into a key marked glide (ease: "drop" optional).
    const cam = sh.cam || { from: { x: 0, y: 0, s: 1 }, to: { x: 0, y: 0, s: 1 } };
    const camAt = (t, k0) => {
      if (cam.keys) {
        let i = 0;
        while (i + 1 < cam.keys.length && cam.keys[i + 1].t <= t) i++;
        const a = cam.keys[i], b = cam.keys[i + 1];
        if (b && b.glide && t > b.t - b.glide) {
          const e = (EASES[b.ease] || ease)((t - (b.t - b.glide)) / b.glide), d = a.drift || {}, u = b.t - b.glide - a.t;
          const ax = a.x + (d.x || 0) * u, ay = a.y + (d.y || 0) * u, as = a.s * (1 + (d.s ?? 0.012) * u);
          return { x: lerp(ax, b.x, e), y: lerp(ay, b.y, e), s: lerp(as, b.s, e) };
        }
        const u = t - a.t, d = a.drift || {};
        return { x: a.x + (d.x || 0) * u, y: a.y + (d.y || 0) * u, s: a.s * (1 + (d.s ?? 0.012) * u) };
      }
      const k = cam.dur ? Math.max(0, Math.min(1, (t - (cam.at || 0)) / cam.dur)) : k0;
      const e = cam.ease === "linear" ? k : ease(k);
      return { x: lerp(cam.from.x, cam.to.x, e), y: lerp(cam.from.y, cam.to.y, e), s: lerp(cam.from.s, cam.to.s, e) };
    };
    // depth of field: blur per layer, e.g. blur: { far: 3, fg: 10 }
    Object.entries(sh.blur || {}).forEach(([layer, px]) => { L[layer].style.filter = px ? `blur(${px}px)` : "none"; });
    // shake(t) returns px of sideways shake, or { x, y, r } for a first-person head (bob up and down, roll in degrees)
    const applyCam = (k0) => {
      const { x, y, s } = camAt(k0 * sh.dur, k0);
      const sk = sh.shake ? sh.shake(k0 * sh.dur) : 0, hx = typeof sk === "number" ? sk : sk.x || 0, hy = typeof sk === "number" ? 0 : sk.y || 0;
      const roll = typeof sk === "number" || !sk.r ? "" : ` rotate(${sk.r.toFixed(3)})`;
      Object.entries(PARALLAX).forEach(([layer, p]) => {
        const ls = 1 + (s - 1) * p;
        L[layer].setAttribute("transform", `translate(540 960)${roll} scale(${ls}) translate(${-540 - x * p + hx} ${-960 - y * p + hy})`);
      });
      L.glow.setAttribute("transform", L.set.getAttribute("transform"));
      if (grainEl) { const f = Math.floor(k0 * sh.dur * 24), gx = ((f * 97) % 256), gy = ((f * 61) % 256); grainEl.setAttribute("transform", `translate(${gx} ${gy})`); }
    };
    const grainEl = document.getElementById(`${id}-grain`);
    const c = { k: 0 };
    tl.to(c, { k: 1, duration: sh.dur, ease: "none", onUpdate: () => applyCam(c.k) }, sh.start);
    applyCam(0);

    // captions (one at a time, comic narration box)
    const capWrap = document.getElementById(`${id}-caps`);
    (sh.captions || []).forEach((cp, k) => {
      capWrap.insertAdjacentHTML("beforeend", Ui.caption(`${id}-c${k}`, cp.text));
      const el = `#${id}-c${k}`;
      tl.fromTo(el, { opacity: 0, y: 26, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "back.out(2)", immediateRender: false }, sh.start + cp.t);
      tl.to(el, { opacity: 0, duration: 0.12 }, sh.start + (cp.end ?? sh.dur - 0.12));
    });
    // small top UI cards
    (sh.cards || []).forEach((cd, k) => {
      div.insertAdjacentHTML("beforeend", Ui.card(`${id}-u${k}`, cd));
      const el = `#${id}-u${k}`;
      const fromX = cd.side === "right" ? 420 : -620;
      tl.fromTo(el, { opacity: 0, x: fromX }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.5)", immediateRender: false }, sh.start + cd.t);
      if (cd.end !== undefined) tl.to(el, { opacity: 0, x: fromX * 0.3, duration: 0.25 }, sh.start + cd.end);
    });
    // game HUD components (choices, QTE, illustrated tips...)
    (sh.ui || []).forEach((u, k) => GameUI.add(div, tl, id, sh.start, u, k));
    // speech bubbles
    (sh.bubbles || []).forEach((b, k) => {
      div.insertAdjacentHTML("beforeend", `<div id="${id}-b${k}" class="bubble" style="left:${b.x}px; top:${b.y}px; --tail:${b.tail || 40}px">${Ui.mark(b.text)}</div>`);
      const el = `#${id}-b${k}`;
      tl.fromTo(el, { opacity: 0, scale: 0.6, transformOrigin: "20% 100%" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, sh.start + b.t);
      tl.to(el, { opacity: 0, duration: 0.15 }, sh.start + (b.end ?? sh.dur - 0.15));
    });
    // comic SFX words
    (sh.sfxText || []).forEach((w, k) => {
      div.insertAdjacentHTML("beforeend", `<div id="${id}-w${k}" class="sfxw" style="left:${w.x}px; top:${w.y}px; transform:rotate(${w.rot || -6}deg); font-size:${w.size || 110}px; color:${w.color || "#f2d6a0"}">${w.text}</div>`);
      const el = `#${id}-w${k}`;
      tl.fromTo(el, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.18, ease: "back.out(3)", immediateRender: false }, sh.start + w.t);
      tl.to(el, { opacity: 0, duration: 0.25 }, sh.start + (w.end ?? w.t + 1.1));
    });
    if (sh.fx) sh.fx(tl, id, sh.start, L);
  }

  // translucent old woman silhouette used for the twist
  function ghost(id, a) {
    return `<g id="${id}" transform="translate(${a.x},${a.y}) scale(${a.s})" opacity="0">
      <path d="M-60,0C-70,-120 -60,-260 -40,-330Q0,-350 40,-330C60,-260 70,-120 60,0Z" fill="#dfe7e4" opacity=".35"/>
      <ellipse cx="0" cy="-380" rx="40" ry="46" fill="#dfe7e4" opacity=".4"/>
      <ellipse cx="0" cy="-424" rx="30" ry="18" fill="#dfe7e4" opacity=".45"/>
      <path d="M-40,-300Q-90,-220 -70,-150M40,-300Q90,-220 76,-160" stroke="#dfe7e4" stroke-width="16" opacity=".3" fill="none" stroke-linecap="round"/>
      <ellipse cx="-14" cy="-384" rx="5" ry="3" fill="#0b1114" opacity=".7"/><ellipse cx="14" cy="-384" rx="5" ry="3" fill="#0b1114" opacity=".7"/></g>`;
  }

  window.Engine = { build };
})();
