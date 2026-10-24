// First-person view kit ("ควันหลง": the viewer is "you" and never sees their own face).
//   Pov.head(o)              shot.shake: a head that breathes, pants, crawls, coughs and flinches ({x, y, r} for engine.js)
//   Pov.lids(tl, id, t0, ev) eyelids over the shot: ev = [[t, "open" | "close" | "blink", dur?]] (a blink is a soft cut)
//   Pov.torch(id, o)         { markup, drive } the phone torch: darkness with a moving pool, a beam that shows in smoke,
//                            the left hand holding the phone (LED end toward the pool); o.keys = [{ t, x, y, r }] in screen px
//   Pov.reach(id, o)         markup: your right arm and round fist (#id), coming in from the bottom right; move it with
//                            an attr transform tween "translate(x,y) rotate(a)" (the fist is at the origin)
//   Pov.smoke(r, o)          markup: a smoke ceiling in world space (dense at the top, a soft drifting lower edge at o.y1)
//   Pov.embers(r, o)         markup: glowing embers and ash (class emb, risen by Pov.life)
//   Pov.life(tl, scope, t0, dur)  drifts smoke (smk), raises embers (emb), flickers fire light (flk), blinks LEDs (led),
//                            moves the heat haze; call once per shot like Mok.life
//   Pov.cough(tl, id, t)     a coughing fit: blur, red edge, a short head jolt is in Pov.head({ cough: [...] })
// Same layer contract as sets.js; seeded RNG only, so every frame seeks deterministically.
(function () {
  const INK = "#2e2a26", OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const SLEEVE = "#5d6f8f", CUFF = "#7f91b2"; // your pyjama sleeves (blue)

  Sets.DEFS += `
    <filter id="pvHaze" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency="0.011 0.045" numOctaves="2" seed="7" result="n"/>
      <feOffset id="pvHazeOff" in="n" dx="0" dy="0" result="m"/><feDisplacementMap in="SourceGraphic" in2="m" scale="18" xChannelSelector="R" yChannelSelector="G"/></filter>
    <filter id="pvSoft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="pvLid" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="26"/></filter>
    <radialGradient id="pvPuff"><stop offset="0" stop-color="#3a3632" stop-opacity=".95"/><stop offset=".55" stop-color="#2e2b28" stop-opacity=".55"/><stop offset="1" stop-color="#2e2b28" stop-opacity="0"/></radialGradient>
    <radialGradient id="pvPuffLit"><stop offset="0" stop-color="#7a5a44" stop-opacity=".85"/><stop offset=".55" stop-color="#5a4434" stop-opacity=".45"/><stop offset="1" stop-color="#5a4434" stop-opacity="0"/></radialGradient>
    <linearGradient id="pvSmokeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1917" stop-opacity=".97"/><stop offset=".7" stop-color="#26231f" stop-opacity=".85"/><stop offset="1" stop-color="#2e2a26" stop-opacity="0"/></linearGradient>
    <radialGradient id="pvEmber"><stop offset="0" stop-color="#fff2b0"/><stop offset=".35" stop-color="#ffb14a"/><stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="pvPool"><stop offset="0" stop-color="#000"/><stop offset=".5" stop-color="#000"/><stop offset="1" stop-color="#fff"/></radialGradient>
    <radialGradient id="pvPoolLit"><stop offset="0" stop-color="#fff6dc" stop-opacity=".22"/><stop offset=".6" stop-color="#fff6dc" stop-opacity=".07"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></radialGradient>
    <linearGradient id="pvBeam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff6dc" stop-opacity=".55"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></linearGradient>`;

  // ---------------- head motion ----------------
  // mode: still | breath | panic | crawl | walk · cough: [t] fits (0.7 s) · flinch: [t] jolts · tilt: steady roll (deg)
  const MODES = { still: [1.2, 0.8, 0.12, 0.7], breath: [2.5, 2.8, 0.25, 1.05], panic: [4, 5, 0.5, 2.1], crawl: [11, 14, 1.6, 2.2], walk: [7, 10, 0.9, 1.8] };
  function head(o = {}) {
    const [ax, ay, ar, f] = MODES[o.mode || "breath"];
    const at = (o.modes || []).slice().sort((a, b) => a[0] - b[0]); // [[t, mode]] switches part-way through the shot
    return (t) => {
      let [x0, y0, r0, fq] = [ax, ay, ar, f];
      at.forEach(([tm, md]) => { if (t >= tm) [x0, y0, r0, fq] = MODES[md]; });
      const w = t * fq * Math.PI * 2;
      let x = x0 * Math.sin(w * 0.5) + 0.6 * Math.sin(t * 13.1), y = y0 * Math.sin(w) + 0.5 * Math.sin(t * 11.3), r = r0 * Math.sin(w * 0.5 + 1) + (o.tilt || 0);
      (o.cough || []).forEach((c) => { const u = t - c; if (u > 0 && u < 0.7) { const e = Math.sin(u / 0.7 * Math.PI); y += 16 * e * Math.sin(u * 52); x += 6 * e * Math.sin(u * 37); r += 1.2 * e * Math.sin(u * 29); } });
      (o.flinch || []).forEach((c) => { const u = t - c; if (u > 0 && u < 0.45) { const e = Math.exp(-u * 9); x += 26 * e * Math.sin(u * 60); y -= 18 * e; r += 2.5 * e * Math.sin(u * 40); } });
      return { x, y, r };
    };
  }

  // ---------------- eyelids ----------------
  function lids(tl, id, t0, ev) {
    const clip = document.getElementById(id);
    clip.insertAdjacentHTML("beforeend", `<svg id="${id}-lids" width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0;z-index:53;pointer-events:none">
      <g filter="url(#pvLid)"><g id="${id}-lt" transform="translate(0,0)"><path d="M-200,-1400H1280V960Q540,1180 -200,960Z" fill="#020202"/></g>
      <g id="${id}-lb" transform="translate(0,0)"><path d="M-200,3300H1280V960Q540,1100 -200,960Z" fill="#020202"/></g></g></svg>`);
    const T = `#${id}-lt`, B = `#${id}-lb`, OPEN = [-1500, 1450];
    const set = (t, k, dur, ease) => {
      tl.to(T, { attr: { transform: `translate(0,${f1(OPEN[0] * k)})` }, duration: dur, ease }, t0 + t);
      tl.to(B, { attr: { transform: `translate(0,${f1(OPEN[1] * k)})` }, duration: dur, ease }, t0 + t);
    };
    const first = ev[0];
    if (!first || first[1] !== "open") { tl.set([T, B], { attr: { transform: "translate(0,0)" } }, t0); set(0, 1, 0.001, "none"); }
    ev.forEach(([t, kind, dur]) => {
      if (kind === "open") { // heavy lids: half open, droop, then open
        const d = dur ?? 1.2;
        set(t, 0.35, d * 0.4, "power2.out"); set(t + d * 0.4, 0.22, d * 0.2, "sine.inOut"); set(t + d * 0.6, 1, d * 0.4, "power2.out");
      } else if (kind === "close") set(t, 0, dur ?? 0.25, "power2.in");
      else { set(t, 0, (dur ?? 0.22) * 0.45, "power2.in"); set(t + (dur ?? 0.22) * 0.55, 1, (dur ?? 0.22) * 0.45, "power2.out"); }
    });
  }

  // ---------------- the phone torch and the hand that holds it ----------------
  function phoneInHand(id) {
    return `<g id="${id}-ph">
      <path d="M40,160L-20,900H330L240,170Z" fill="${INK}"/><path d="M48,168L-10,900H320L232,176Z" fill="${SLEEVE}"/><path d="M60,200L250,210" stroke="${CUFF}" stroke-width="26" stroke-linecap="round"/>
      <g transform="rotate(-8)"><rect x="-70" y="-250" width="200" height="380" rx="34" fill="#1d2026" ${OUT}/><rect x="-58" y="-238" width="176" height="356" rx="26" fill="#2c3038"/>
        <rect x="-40" y="-226" width="74" height="96" rx="20" fill="#14171c" ${OUT}/><circle cx="-14" cy="-198" r="15" fill="#0b0d10" stroke="#5a606a" stroke-width="3"/><circle cx="-14" cy="-156" r="13" fill="#0b0d10" stroke="#5a606a" stroke-width="3"/>
        <circle id="${id}-led" cx="18" cy="-200" r="9" fill="#fffbe8"/><circle cx="18" cy="-200" r="26" fill="#fff6dc" opacity=".35"/>
        <path d="M-50,-120L-50,90" stroke="#fff" stroke-width="6" opacity=".08" stroke-linecap="round"/></g>
      <g transform="translate(70,90)">${Hands.fist({ r: 105 })}</g>
      <ellipse cx="-34" cy="40" rx="40" ry="58" fill="${Hands.SKIN}" ${OUT}/><path d="M-50,10q10,-10 28,-4" stroke="#cc9a74" stroke-width="4" fill="none" stroke-linecap="round"/></g>`;
  }
  // o.keys: [{ t, x, y, r }] pool centre and radius (screen px); o.dark (0..1); o.beam (beam strength in smoke);
  // o.hand: [x, y] where the phone hand rests (default bottom left); o.off: [[a, b]] torch off; o.flicker: [[t, d]]
  function torch(id, o = {}) {
    const [hx, hy] = o.hand || [220, 1700];
    const markup = `<defs><mask id="${id}-tmask" maskUnits="userSpaceOnUse" x="-300" y="-300" width="1680" height="2520">
        <rect x="-300" y="-300" width="1680" height="2520" fill="#fff"/><circle id="${id}-hole" cx="540" cy="900" r="300" fill="url(#pvPool)"/></mask></defs>
      <rect id="${id}-night" x="-300" y="-300" width="1680" height="2520" fill="#020304" opacity="${o.dark ?? 0.82}" mask="url(#${id}-tmask)"/>
      <g id="${id}-beam"><path id="${id}-cone" fill="url(#pvBeam)" opacity="${o.beam ?? 0.35}"/><circle id="${id}-pool" cx="540" cy="900" r="300" fill="url(#pvPoolLit)"/>
        ${Array.from({ length: 26 }, (_, k) => `<circle class="${id}-mote" r="${(1.5 + (k % 4) * 0.8).toFixed(1)}" fill="#fff6dc" opacity="${(0.25 + (k % 5) * 0.1).toFixed(2)}"/>`).join("")}</g>
      ${o.noHand ? "" : `<g id="${id}-hand" transform="translate(${hx},${hy})">${phoneInHand(id)}</g>`}`;
    const r = mk(o.seed || 31), motes = Array.from({ length: 26 }, () => [r(), r(), r()]);
    const sm = (k) => k * k * (3 - 2 * k);
    function at(keys, t) {
      let i = 0;
      while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
      const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
      const k = b.t > a.t ? sm(Math.max(0, Math.min(1, (t - a.t) / (b.t - a.t)))) : 0;
      return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, r: a.r + (b.r - a.r) * k };
    }
    function drive(tl, t0, dur) {
      const hole = document.getElementById(`${id}-hole`), pool = document.getElementById(`${id}-pool`), cone = document.getElementById(`${id}-cone`), hand = document.getElementById(`${id}-hand`);
      const ms = document.querySelectorAll(`.${id}-mote`);
      const c = { t: 0 };
      const go = () => {
        const p = at(o.keys, c.t), bob = 8 * Math.sin(c.t * 2.2) + 3 * Math.sin(c.t * 7.3);
        hole.setAttribute("cx", f1(p.x)); hole.setAttribute("cy", f1(p.y)); hole.setAttribute("r", f1(p.r));
        pool.setAttribute("cx", f1(p.x)); pool.setAttribute("cy", f1(p.y)); pool.setAttribute("r", f1(p.r * 0.9));
        // the hand leans toward the pool; the LED sits ~230 px up the phone
        const th = Math.atan2(p.x - hx, hy - p.y), deg = Math.max(-40, Math.min(40, th * 180 / Math.PI));
        if (hand) hand.setAttribute("transform", `translate(${f1(hx + bob * 0.6)},${f1(hy + bob)}) rotate(${f1(deg)})`);
        const rad = deg * Math.PI / 180, lx = hx + bob * 0.6 + Math.sin(rad) * 230, ly = hy + bob - Math.cos(rad) * 230;
        const dx = p.x - lx, dy = p.y - ly, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, w = p.r * 0.85;
        cone.setAttribute("d", `M${f1(lx - nx * 14)},${f1(ly - ny * 14)}L${f1(p.x - nx * w)},${f1(p.y - ny * w)}L${f1(p.x + nx * w)},${f1(p.y + ny * w)}L${f1(lx + nx * 14)},${f1(ly + ny * 14)}Z`);
        // dust motes floating inside the beam
        ms.forEach((m, k) => {
          const [a, b, s] = motes[k], u = (a + c.t * (0.04 + s * 0.05)) % 1, side = (b - 0.5) * 2 * w * u + 10 * Math.sin(c.t * (1 + s) + k);
          m.setAttribute("cx", f1(lx + dx * u + nx * side)); m.setAttribute("cy", f1(ly + dy * u + ny * side));
        });
        cone.setAttribute("transform", "");
      };
      tl.to(c, { t: dur, duration: dur, ease: "none", onUpdate: go }, t0);
      go();
      (o.flicker || []).forEach(([ft, fd], k) => { if (window.Fx) { Fx.flicker(tl, `#${id}-beam`, t0 + ft, fd, 40 + k); Fx.flicker(tl, `#${id}-hole`, t0 + ft, fd, 40 + k); } });
      (o.off || []).forEach(([a, b]) => { tl.set([`#${id}-beam`, `#${id}-hole`], { opacity: 0 }, t0 + a); if (b !== undefined) tl.set([`#${id}-beam`, `#${id}-hole`], { opacity: 1 }, t0 + b); });
    }
    return { markup, drive };
  }

  // ---------------- your right arm ----------------
  // the fist at the origin, the forearm and sleeve running off toward the bottom right (angle o.a, default 35°)
  function reach(id, o = {}) {
    const r = o.r ?? 95, a = o.a ?? 35;
    return `<g id="${id}" transform="translate(${o.x ?? 1200},${o.y ?? 2300}) rotate(0)"><g transform="rotate(${a})">
      <path d="M0,0H1100" stroke="${INK}" stroke-width="${r * 1.55 + 10}" stroke-linecap="round"/><path d="M0,0H1100" stroke="${Hands.SKIN}" stroke-width="${r * 1.55}" stroke-linecap="round"/>
      <path d="M${r * 1.5},0H1100" stroke="${INK}" stroke-width="${r * 1.9 + 10}"/><path d="M${r * 1.5},0H1100" stroke="${o.sleeve || SLEEVE}" stroke-width="${r * 1.9}"/>
      <rect x="${r * 1.5}" y="${-r * 0.95}" width="${r * 0.42}" height="${r * 1.9}" fill="${CUFF}" ${OUT}/></g>
      <g transform="rotate(${a - 90})">${Hands.fist({ r })}</g></g>`;
  }

  // ---------------- smoke and embers ----------------
  // o: x0, x1 (world span), y0 (ceiling), y1 (lower edge), lit (an orange underside, near a fire), n (blobs), op
  function smoke(r, o = {}) {
    const x0 = o.x0 ?? -600, x1 = o.x1 ?? 1700, y0 = o.y0 ?? -400, y1 = o.y1 ?? 500, op = o.op ?? 1;
    let s = `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="url(#pvSmokeV)" opacity="${op}"/>`;
    for (let k = 0; k < (o.n ?? 26); k++) {
      const x = x0 + r() * (x1 - x0), y = y0 + (y1 - y0) * (0.35 + r() * 0.75), rx = 160 + r() * 260;
      s += `<g class="smk" data-d="${f1(18 + r() * 40)}" data-i="${k}"><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(rx * (0.32 + r() * 0.2))}" fill="url(#${o.lit && r() < 0.5 ? "pvPuffLit" : "pvPuff"})" opacity="${(op * (0.55 + r() * 0.45)).toFixed(2)}"/></g>`;
    }
    return `<g class="pvsmoke">${s}</g>`;
  }
  function embers(r, o = {}) {
    let s = "";
    for (let k = 0; k < (o.n ?? 30); k++) {
      const x = (o.x0 ?? 0) + r() * ((o.x1 ?? 1080) - (o.x0 ?? 0)), y = (o.y0 ?? 900) + r() * ((o.y1 ?? 1900) - (o.y0 ?? 900)), sz = 2 + r() * (o.big ?? 6);
      s += `<g class="emb" data-rise="${f1(160 + r() * 340)}" data-drift="${f1((r() - 0.5) * 140)}" data-p="${f1(1.4 + r() * 2)}" data-o="${f1(r())}"><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(sz)}" fill="url(#pvEmber)"/></g>`;
    }
    return s;
  }

  // ---------------- ambient life ----------------
  function life(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".smk").forEach((el, i) => {
      const d = +(el.dataset.d || 30) * (i % 2 ? -1 : 1);
      tl.fromTo(el, { x: 0, y: 0, scale: 1 }, { x: d * dur, y: 8 * dur, scale: 1.12, duration: dur, ease: "none", immediateRender: false, transformOrigin: "50% 50%" }, t0);
    });
    q(".emb").forEach((el) => {
      const p = +el.dataset.p, rise = +el.dataset.rise, drift = +el.dataset.drift, off = +el.dataset.o * p;
      for (let t = -off; t < dur; t += p) {
        const a = Math.max(0, t), u0 = (a - t) / p;
        tl.fromTo(el, { y: -rise * u0, x: drift * u0, opacity: u0 < 0.15 ? u0 / 0.15 : 1 }, { y: -rise, x: drift, opacity: 0, duration: p * (1 - u0), ease: "none", immediateRender: false }, t0 + a);
      }
    });
    // fire light under doors and in windows: an irregular flicker (seeded)
    q(".flk").forEach((el, i) => {
      const r = mk(70 + i), base = +(el.getAttribute("opacity") || 1);
      for (let t = 0; t < dur; t += 0.06 + r() * 0.08) tl.set(el, { opacity: base * (0.55 + r() * 0.5) }, t0 + t);
    });
    q(".led").forEach((el) => { for (let t = 0; t < dur; t += 1.0) { tl.set(el, { opacity: 1 }, t0 + t); tl.set(el, { opacity: 0.15 }, t0 + t + 0.12); } });
    // fire-engine lights: red and blue take turns
    q(".siren").forEach((el) => { for (let t = 0; t < dur; t += 0.5) { tl.set(el, { opacity: 1 }, t0 + t); tl.set(el, { opacity: 0.1 }, t0 + t + 0.25); } });
    q(".sirenb").forEach((el) => { for (let t = 0; t < dur; t += 0.5) { tl.set(el, { opacity: 0.1 }, t0 + t); tl.set(el, { opacity: 1 }, t0 + t + 0.25); } });
    // heat haze: slide the noise upward through the displacement (shared filter, harmless to restart per shot)
    if (q(".haze").length) tl.fromTo("#pvHazeOff", { attr: { dy: 0 } }, { attr: { dy: -90 * dur }, duration: dur, ease: "none", immediateRender: false }, t0);
  }

  // a coughing fit: the picture blurs and the edges go red for a moment
  function cough(tl, id, t) {
    tl.fromTo(`#${id} .stage`, { filter: "blur(0px)" }, { filter: "blur(5px)", duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, t);
    tl.set(`#${id} .stage`, { filter: "none" }, t + 0.5);
    tl.fromTo("#fxred", { opacity: 0.55 }, { opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, t);
  }

  window.Pov = { head, lids, torch, reach, smoke, embers, life, cough, phoneInHand, SLEEVE, CUFF };
})();
