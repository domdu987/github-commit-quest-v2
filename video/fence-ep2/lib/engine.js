// Episode engine: turns a declarative list of shots into HyperFrames clips + one GSAP timeline.
// A shot = one set (layered), a camera move with parallax, actors driven by Rig tracks, captions,
// small UI cards, speech bubbles and simple FX. All motion is a pure function of timeline time.
(function () {
  const PARALLAX = { sky: 0.05, far: 0.25, mid: 0.6, set: 1, act: 1, fg: 1.5 };
  const lerp = (a, b, k) => a + (b - a) * k;
  const ease = (k) => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);

  function build(root, tl, shots) {
    root.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute"><defs>${Sets.DEFS}</defs></svg>`);
    window.__SHOTS = shots;   // for probes (acting tables)
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
        <linearGradient id="${id}-dkg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05090c" stop-opacity=".85"/><stop offset=".3" stop-color="#05090c" stop-opacity=".55"/><stop offset=".72" stop-color="#05090c" stop-opacity=".5"/><stop offset="1" stop-color="#05090c" stop-opacity=".75"/></linearGradient>
        <rect id="${id}-dark" width="1080" height="1920" fill="url(#${id}-dkg)" opacity="${Math.min(1, (sh.dark ?? 0.35) * 0.9)}" style="mix-blend-mode:multiply"/>
        <g id="${id}-glow"></g>
        <g id="${id}-light"></g>
        <rect id="${id}-fog" x="-200" y="0" width="1480" height="1920" fill="#c9c3b6" opacity="0"/>
      </svg>
      <div class="capwrap" id="${id}-caps"></div>`;
    root.appendChild(div);
    const L = {}; Object.keys(PARALLAX).forEach((k) => (L[k] = document.getElementById(`${id}-${k}`)));
    const world = document.getElementById(`${id}-world`);
    // colour grade: a CSS filter on the whole world plus a tinted multiply over it (sh.grade overrides window.GRADE; false = none)
    // the colour script (user 28 Oct: "สี … ดีแล้วรึยัง"): each time of day has its own look instead of one grey-blue wash —
    // warm afternoon, pale hot noon, soft morning, orange-magenta dusk, moonlit blue night that still reads in the midtones
    const so = sh.setOpts || {}, tod = so.time || (so.night ? "night" : (sh.dark ?? 0.35) >= 0.45 ? "night" : "day");
    const TOD = {
      day: { filter: "saturate(.92) brightness(.99) contrast(1.06)", tint: "#ffcf8a", tintOp: 0.2, blend: "soft-light" },
      morning: { filter: "saturate(.9) brightness(1.01) contrast(1.04)", tint: "#ffd9b0", tintOp: 0.22, blend: "soft-light" },
      noon: { filter: "saturate(.86) brightness(1.03) contrast(1.03)", tint: "#fff0c0", tintOp: 0.24, blend: "soft-light" },
      dusk: { filter: "saturate(1.02) brightness(.96) contrast(1.08)", tint: "#ff7a3a", tintOp: 0.24, blend: "soft-light" },
      night: { filter: "saturate(.78) brightness(.95) contrast(1.06)", tint: "#3a5a8c", tintOp: 0.3, blend: "multiply" },
    };
    const gr = sh.grade === undefined ? (window.GRADE_BY_TIME === false ? window.GRADE : TOD[tod] || TOD.day) : sh.grade;
    if (gr) {
      document.getElementById(`${id}-world`).style.filter = gr.filter || "";
      if (gr.tint) document.getElementById(`${id}-dark`).insertAdjacentHTML("beforebegin", `<rect id="${id}-tint" width="1080" height="1920" fill="${gr.tint}" opacity="${gr.tintOp ?? 0.25}" style="mix-blend-mode:${gr.blend || "multiply"}"/>`);
    }
    L.glow = document.getElementById(`${id}-glow`); // light sources above the darkness, moving with the set
    L.light = document.getElementById(`${id}-light`);
    if (sh.set) Sets[sh.set](L, sh.setOpts || {});
    if (sh.extra) sh.extra(L, id);

    // actors. Depth (user, 28 Oct: "เงา ทำให้มีมิติ"): each figure throws a cast shadow across the ground (a flattened, sheared
    // <use> of the live rig, so it follows every pose) and is edged with light on the side facing the key light (a pale copy
    // nudged up-left behind it: warm by day, moonlight-blue in the dark). Both are plain <use> clones with CSS colour filters —
    // SVG blur/composite filters on the rigs tripled the render time. sh.cast / a.cast = false or {kx, ky, op}; sh.rim / a.rim = false or {f, op, dx, dy}.
    // The key light is the strongest light the shot placed (Fence.light records them in L._lights); a high one acts like the sun
    // (parallel shadows), a low one like a lamp (shadows fan out from it, longer the closer it sits to the floor). No light = late sun, upper left.
    const casts = (sh.actors || []).length ? (L.act.insertAdjacentHTML("afterbegin", `<g id="${id}-casts" style="filter:blur(2.5px)"></g>`), document.getElementById(`${id}-casts`)) : null;
    const key = (L._lights || []).slice().sort((p, q) => q.op * q.R - p.op * p.R)[0] || null;
    const hue = (c) => { const v = parseInt((c || "#ffe6b0").slice(1), 16), r = v >> 16, b = v & 255; return b > r ? "cool" : r - b > 90 ? "warm" : "sun"; };
    const RIMF = { cool: "brightness(0) invert(1) sepia(1) saturate(2) hue-rotate(185deg)", warm: "brightness(0) invert(1) sepia(1) saturate(3.2) hue-rotate(-12deg)", sun: "brightness(0) invert(1) sepia(.7)" };
    const tone = key ? hue(key.col) : (sh.dark ?? 0.35) >= 0.4 ? "cool" : "sun";
    // the rim is drawn INSIDE the silhouette on the lit side (a rim-coloured copy in front, masked to the figure minus the figure
    // nudged away from the light) — only where a lamp or the moon makes it read; by day the rigs' own shading carries the form
    const rim = sh.rim === false || (tone === "sun" && !sh.rim) ? null : { f: RIMF[tone], op: tone === "warm" ? 0.55 : 0.45, w: 4, ...(sh.rim || {}) };
    const lightFor = (a) => {
      if (!key) return { kx: 0.42, ky: 0.13, rx: -4, ry: -3 };
      const h = Math.max(160, a.y - key.y), dx = a.x - key.x;
      if (key.y < 600) { const kx = Math.max(-0.7, Math.min(0.7, dx / 900)); return { kx: Math.abs(kx) < 0.12 ? 0.12 * Math.sign(kx || 1) : kx, ky: 0.15, rx: -4 * Math.sign(dx || 1), ry: -3 }; }   // sky light
      const kx = Math.max(-1.3, Math.min(1.3, (dx / h) * 0.9));
      return { kx, ky: 0.1, rx: -5 * Math.sign(dx || 1), ry: key.y < a.y - 300 ? -3 : 0 };   // a lamp in the scene
    };
    // shot grammar (user 28 Oct, character pass): while a character speaks, the camera eases in to a medium close-up on them
    // (head placed at sh.cu.sy ≈ 860 on screen, zoom so the head is ~225 px tall) and eases back out after the line.
    // sh.cu / a.cu = false turns it off; {s, sx, sy} overrides the framing
    const cus = [];
    // where a character's head is at shot time t: sitting / crouching poses drop the body (their bodyY), so the close-up aims lower
    const headY = (a, t, y) => { let m = (a.track || [])[0]; for (const e of a.track || []) if (e.t <= t) m = e; const f = m && Rig.MODES[m.mode]; const by = f ? (f(0.5, m.opts || {}).bodyY || 0) : 0; return y - (560 - by) * a.s; };
    const castT = (c, gy) => `matrix(1 0 ${-c.kx} ${-c.ky} ${(c.kx * gy).toFixed(1)} ${((1 + c.ky) * gy).toFixed(1)})`;
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
        g.insertAdjacentHTML("afterbegin", `<ellipse cy="6" rx="78" ry="15" fill="#000" opacity=".2"/>`);   // a contact shadow grounds the figure
        g.setAttribute("transform", `translate(${a.x},${a.y}) scale(${a.flip ? -a.s : a.s},${a.s})`);
        const lf = lightFor(a), cast = sh.cast === false || a.cast === false ? null : { kx: lf.kx, ky: lf.ky, op: key && key.y >= 600 ? 0.36 : 0.32, ...(sh.cast || {}), ...(a.cast || {}) };
        if (cast) casts.insertAdjacentHTML("beforeend", `<use id="${aid}-cast" href="#${aid}" transform="${castT(cast, a.y)}" opacity="${cast.op}" style="filter:brightness(0)"/>`);
        if (rim && a.rim !== false) { const k = rim.w / 4, mx = -(rim.dx ?? lf.rx) * k, my = -(rim.dy ?? lf.ry) * k;
          g.insertAdjacentHTML("afterend", `<mask id="${aid}-rm" maskUnits="userSpaceOnUse" x="-4000" y="-4000" width="9000" height="9000"><use href="#${aid}" style="filter:brightness(0) invert(1)"/><use href="#${aid}" transform="translate(${mx.toFixed(1)},${my.toFixed(1)})" style="filter:brightness(0)"/></mask><use id="${aid}-rim" href="#${aid}" mask="url(#${aid}-rm)" opacity="${rim.op}" style="filter:${rim.f}"/>`); }
        // lines this character speaks in the shot move its mouth (make.py merges lipsync.json + the voice→character map into sh.vo);
        // only the first actor of a kind talks, a.talk = false silences one
        const first = (sh.actors || []).findIndex((b) => b.who === a.who) === k;
        const talk = a.talk === false || !first ? [] : (sh.vo || []).filter((v) => v.lip && v.who === a.who).map((v) => ({ t: v.t, lv: v.lip, fps: 30 }));
        // a walker carried by moveTo takes steps that match the ground it covers (no more legs cycling while the body drifts):
        // the stride shrinks for a slow walk, the cadence quickens for a fast one; bob and knee lift scale with the stride
        let track = a.track;
        if (a.moveTo && a.autoStride !== false) {
          const v = Math.hypot(a.moveTo.x - a.x, (a.moveTo.y ?? a.y) - a.y) / Math.max(0.1, a.moveTo.dur) / a.s;
          track = a.track.map((e) => {
            if ((e.mode !== "walk" && e.mode !== "run") || (e.opts && e.opts.stride)) return e;
            const run = e.mode === "run", def = run ? 30 : 16, per0 = (e.opts && e.opts.period) || (run ? 0.56 : 0.96);
            const st = Math.asin(Math.min(1, (v * per0) / (4 * 288))) * 180 / Math.PI, stride = Math.max(run ? 20 : 6, Math.min(def, st));   // a sprint keeps a sprinter's stride even when the shot moves it only a little
            const period = st > def ? Math.max(run ? 0.38 : 0.62, (4 * 288 * Math.sin((def * Math.PI) / 180)) / v) : per0, k2 = Math.max(0.45, stride / def);
            return { ...e, opts: { ...(e.opts || {}), stride, period, bob: (run ? 16 : 9) * k2, knee: (run ? 80 : 42) * Math.max(0.6, k2) } };
          });
        }
        // the others in the shot look at whoever is speaking
        const listen = (sh.vo || []).filter((v) => v.lip && v.who !== a.who).map((v) => {
          const sp = (sh.actors || []).find((b) => b.who === v.who);
          if (!sp) return null;
          const dir = Math.sign(sp.x - a.x) * (a.flip ? -1 : 1);
          return dir ? { t0: v.t - 0.1, t1: v.t + v.lip.length / 30 + 0.3, gx: 2.6 * dir } : null;
        }).filter(Boolean);
        Rig.drive(tl, aid, sh.start, sh.dur, track, a.blinks || Rig.blinkSeq(`${sh.key || id}-${a.who}-${k}`, sh.dur), talk, listen);
        // a speaker on the move (running, walking, dragged along) stays in the wide shot so the danger stays in frame — unless a.cu asks
        const MOVING = new Set(["run", "walk", "drag", "zrun", "shamble", "swing", "knocked", "fall"]);
        const modeAt = (tt) => { let m = a.track[0]; for (const e of a.track) if (e.t <= tt) m = e; return m && m.mode; };
        const movingAt = (tt) => MOVING.has(modeAt(tt)) || (a.moveTo && tt >= (a.moveTo.at || 0) && tt <= (a.moveTo.at || 0) + a.moveTo.dur);
        if (sh.cu !== false && a.cu !== false) talk.forEach((v) => {
          const t0 = v.t - 0.15, t1 = v.t + v.lv.length / 30 + 0.2;
          if (!a.cu && movingAt((t0 + t1) / 2)) return;
          let ax = a.x, ay = a.y;
          if (a.moveTo) { const m = Math.max(0, Math.min(1, ((t0 + t1) / 2 - (a.moveTo.at || 0)) / a.moveTo.dur)); ax = lerp(a.x, a.moveTo.x, m); ay = lerp(a.y, a.moveTo.y ?? a.y, m); }
          (window.__CU || (window.__CU = [])).push({ shot: sh.key, start: sh.start, who: a.who, t0: +t0.toFixed(2), t1: +t1.toFixed(2) });   // for probes
          cus.push({ t0, t1, wx: ax, wy: headY(a, (t0 + t1) / 2, ay), s: Math.max(1.35, Math.min(2.5, 225 / (125 * a.s))), ...(typeof sh.cu === "object" ? sh.cu : {}), ...(typeof a.cu === "object" ? a.cu : {}) });
        });
        if (a.prop && window.Camp) Camp.attach(aid, a.prop);
        if (a.moveTo) { // walk across the set: translate the whole character in sync with the shot clock
          const m = { k: 0 };
          tl.to(m, { k: 1, duration: a.moveTo.dur, ease: a.moveTo.ease || "none", onUpdate: () => {
            const x = lerp(a.x, a.moveTo.x, m.k), y = lerp(a.y, a.moveTo.y ?? a.y, m.k);
            g.setAttribute("transform", `translate(${x},${y}) scale(${a.flip ? -a.s : a.s},${a.s})`);
            if (cast && a.moveTo.y !== undefined) document.getElementById(`${aid}-cast`).setAttribute("transform", castT(cast, y));
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
          const ax = a.x + (d.x || 0) * u, ay = a.y + (d.y || 0) * u, as = a.s * (1 + (d.s ?? 0.012) * u), ar = (a.r || 0) + (d.r || 0) * u;
          return { x: lerp(ax, b.x, e), y: lerp(ay, b.y, e), s: lerp(as, b.s, e), r: lerp(ar, b.r || 0, e) };
        }
        const u = t - a.t, d = a.drift || {};
        return { x: a.x + (d.x || 0) * u, y: a.y + (d.y || 0) * u, s: a.s * (1 + (d.s ?? 0.012) * u), r: (a.r || 0) + (d.r || 0) * u };
      }
      const k = cam.dur ? Math.max(0, Math.min(1, (t - (cam.at || 0)) / cam.dur)) : k0;
      const e = cam.ease === "linear" ? k : ease(k);
      return { x: lerp(cam.from.x, cam.to.x, e), y: lerp(cam.from.y, cam.to.y, e), s: lerp(cam.from.s, cam.to.s, e) };
    };
    // reaction close-ups (user 28 Oct: "เพิ่มภาพใกล้หน้าตอนตกใจหรือตอนตัดสินใจ"): sh.react = [{ a: actor index | who, t, dur = 1.4, s, sx, sy, fast }]
    // a quick push-in on a face for a startle or a decision; `fast` snaps in over 0.12 s (a shock) instead of easing over 0.4 s
    (sh.react || []).forEach((r) => {
      const k = r.a ?? (sh.actors || []).findIndex((b) => b.who === r.who), a = (sh.actors || [])[k];
      if (!a) return;
      let ax = a.x, ay = a.y;
      if (a.moveTo) { const m = Math.max(0, Math.min(1, (r.t - (a.moveTo.at || 0)) / a.moveTo.dur)); ax = lerp(a.x, a.moveTo.x, m); ay = lerp(a.y, a.moveTo.y ?? a.y, m); }
      cus.push({ t0: r.t, t1: r.t + (r.dur ?? 1.4), wx: ax, wy: headY(a, r.t + 0.3, ay), s: r.s ?? Math.max(1.45, Math.min(2.7, 250 / (125 * a.s))), sx: r.sx, sy: r.sy ?? 900, inT: r.fast ? 0.12 : 0.4 });
      (window.__CU || (window.__CU = [])).push({ shot: sh.key, start: sh.start, who: a.who, react: true, t0: +r.t.toFixed(2), t1: +(r.t + (r.dur ?? 1.4)).toFixed(2) });
    });
    const camCU = (t, k0) => {
      let c = camAt(t, k0);
      for (const u of cus) {
        if (t <= u.t0 || t >= u.t1 + 0.45) continue;
        const inT = u.inT || 0.4, w = t < u.t0 + inT ? ease((t - u.t0) / inT) : t > u.t1 ? 1 - ease((t - u.t1) / 0.45) : 1;
        const s = Math.max(u.s, c.s * 1.12), sx = u.sx ?? 540, sy = u.sy ?? 860;
        c = { x: lerp(c.x, u.wx - 540 - (sx - 540) / s, w), y: lerp(c.y, u.wy - 960 - (sy - 960) / s, w), s: lerp(c.s, s, w), r: lerp(c.r || 0, 0, w) };
      }
      return c;
    };
    // depth of field: blur per layer, e.g. blur: { far: 3, fg: 10 }
    Object.entries(sh.blur || {}).forEach(([layer, px]) => { L[layer].style.filter = px ? `blur(${px}px)` : "none"; });
    const applyCam = (k0) => {
      const { x, y, s, r } = camCU(k0 * sh.dur, k0);
      const shake = sh.shake ? sh.shake(k0 * sh.dur) : 0;
      // handheld: a slow, small two-frequency float so no frame sits dead still (sh.handheld scales it; 0 = locked off)
      const hh = sh.handheld ?? 1, t = sh.start + k0 * sh.dur;
      const hx = hh * (2.6 * Math.sin(t * 1.31 + i) + 1.1 * Math.sin(t * 3.07 + 2 * i)), hy = hh * (2.0 * Math.sin(t * 1.07 + 3 * i) + 0.9 * Math.sin(t * 2.71 + i));
      const hr = (r || 0) + hh * 0.07 * Math.sin(t * 0.83 + i);
      const wt = `translate(${hx.toFixed(2)} ${hy.toFixed(2)}) rotate(${hr.toFixed(3)} 540 960)`;
      world.setAttribute("transform", wt);
      Object.entries(PARALLAX).forEach(([layer, p]) => {
        const ls = 1 + (s - 1) * p;
        L[layer].setAttribute("transform", `translate(540 960) scale(${ls}) translate(${-540 - x * p + shake} ${-960 - y * p})`);
      });
      L.glow.setAttribute("transform", `${wt} ${L.set.getAttribute("transform")}`);
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
      div.insertAdjacentHTML("beforeend", `<div id="${id}-b${k}" class="bubble${b.up ? " up" : ""}" style="left:${b.x}px; top:${b.y}px; --tail:${b.tail || 40}px">${Ui.mark(b.text)}</div>`);
      const el = `#${id}-b${k}`;
      tl.fromTo(el, { opacity: 0, scale: 0.6, transformOrigin: b.up ? "20% 0%" : "20% 100%" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }, sh.start + b.t);
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
