// Episode engine: turns a declarative list of shots into HyperFrames clips + one GSAP timeline.
// A shot = one set (layered), a camera move with parallax, actors driven by Rig tracks, captions,
// small UI cards, speech bubbles and simple FX. All motion is a pure function of timeline time.
(function () {
  const PARALLAX = { sky: 0.05, far: 0.25, mid: 0.6, set: 1, act: 1, fg: 1.5 };
  const lerp = (a, b, k) => a + (b - a) * k;
  const ease = (k) => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);

  function build(root, tl, shots) {
    root.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute"><defs>${Sets.DEFS}</defs></svg>`);
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
    div.innerHTML = `<svg class="stage" width="1080" height="1920" viewBox="0 0 1080 1920">
        <g id="${id}-world">${Object.keys(PARALLAX).map((L) => `<g id="${id}-${L}"${L === "fg" ? ' class="fgblur"' : ""}></g>`).join("")}</g>
        <rect id="${id}-dark" width="1080" height="1920" fill="#05090c" opacity="${sh.dark ?? 0.35}" style="mix-blend-mode:multiply"/>
        <g id="${id}-glow"></g>
        <g id="${id}-light"></g>
        <rect id="${id}-fog" x="-200" y="0" width="1480" height="1920" fill="#c9c3b6" opacity="0"/>
      </svg>
      <div class="capwrap" id="${id}-caps"></div>`;
    root.appendChild(div);
    const L = {}; Object.keys(PARALLAX).forEach((k) => (L[k] = document.getElementById(`${id}-${k}`)));
    // colour grade: a CSS filter on the whole world plus a tinted multiply over it (sh.grade overrides window.GRADE; false = none)
    const gr = sh.grade === undefined ? window.GRADE : sh.grade;
    if (gr) {
      document.getElementById(`${id}-world`).style.filter = gr.filter || "";
      if (gr.tint) document.getElementById(`${id}-dark`).insertAdjacentHTML("beforebegin", `<rect id="${id}-tint" width="1080" height="1920" fill="${gr.tint}" opacity="${gr.tintOp ?? 0.25}" style="mix-blend-mode:${gr.blend || "multiply"}"/>`);
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
        if (a.prop && window.Camp) Camp.attach(aid, a.prop);
        if (a.moveTo) { // walk across the set: translate the whole character in sync with the shot clock
          const m = { k: 0 };
          tl.to(m, { k: 1, duration: a.moveTo.dur, ease: a.moveTo.ease || "none", onUpdate: () => {
            const x = lerp(a.x, a.moveTo.x, m.k), y = lerp(a.y, a.moveTo.y ?? a.y, m.k);
            g.setAttribute("transform", `translate(${x},${y}) scale(${a.flip ? -a.s : a.s},${a.s})`);
          } }, sh.start + (a.moveTo.at || 0));
        }
      }
      // optional visibility window (lets a shot swap in a turned-around copy of a character)
      if (a.from !== undefined) { tl.set(`#${aid}`, { opacity: 0 }, sh.start); tl.set(`#${aid}`, { opacity: 1 }, sh.start + a.from); }
      if (a.until !== undefined) tl.set(`#${aid}`, { opacity: 0 }, sh.start + a.until);
    });

    // camera: interpolate {x,y,s} and apply per-layer parallax around the frame centre.
    // cam.keys = [{t, x, y, s, drift?, glide?}] gives several framings in one shot: hard cuts at each key
    // (a slow push-in, or `drift` per second, while held), or an eased move into a key marked glide.
    const cam = sh.cam || { from: { x: 0, y: 0, s: 1 }, to: { x: 0, y: 0, s: 1 } };
    const camAt = (t, k0) => {
      if (cam.keys) {
        let i = 0;
        while (i + 1 < cam.keys.length && cam.keys[i + 1].t <= t) i++;
        const a = cam.keys[i], b = cam.keys[i + 1];
        if (b && b.glide && t > b.t - b.glide) {
          const e = ease((t - (b.t - b.glide)) / b.glide), d = a.drift || {}, u = b.t - b.glide - a.t;
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
    const applyCam = (k0) => {
      const { x, y, s } = camAt(k0 * sh.dur, k0);
      const shake = sh.shake ? sh.shake(k0 * sh.dur) : 0;
      Object.entries(PARALLAX).forEach(([layer, p]) => {
        const ls = 1 + (s - 1) * p;
        L[layer].setAttribute("transform", `translate(540 960) scale(${ls}) translate(${-540 - x * p + shake} ${-960 - y * p})`);
      });
      L.glow.setAttribute("transform", L.set.getAttribute("transform"));
    };
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
