// Character rig for the series. Characters are built once as SVG groups with pivots at the joints,
// then every frame is posed from a pure function of time, so seeking to any frame is deterministic.
// Local space: origin between the feet, +y down. Hip (0,-300), shoulders (±46,-455), knee +150, elbow +122.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const OUT = 'stroke="#2e2a26" stroke-width="3.5" stroke-linejoin="round"';

  function limb(len, wid, col, shade) {
    return `<rect x="${-wid / 2}" y="-4" width="${wid}" height="${len + 8}" rx="${wid / 2}" fill="${col}" ${OUT}/>` +
      `<rect x="${wid * 0.12}" y="2" width="${wid * 0.32}" height="${len - 4}" rx="${wid * 0.16}" fill="${shade}" opacity=".55"/>`;
  }

  const EYES = {
    normal: `<ellipse cx="-14" cy="-546" rx="4.5" ry="6" fill="#2e2a26"/><ellipse cx="18" cy="-546" rx="4.5" ry="6" fill="#2e2a26"/>
             <path d="M-24,-562q10,-5 18,-1M10,-563q10,-4 18,1" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>`,
    wide: `<circle cx="-14" cy="-546" r="8" fill="#f4ecd8" ${OUT}/><circle cx="18" cy="-546" r="8" fill="#f4ecd8" ${OUT}/>
           <circle cx="-14" cy="-546" r="2.6" fill="#2e2a26"/><circle cx="18" cy="-546" r="2.6" fill="#2e2a26"/>
           <path d="M-25,-566q10,-8 19,-3M9,-569q10,-5 19,3" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>`,
    closed: `<path d="M-21,-545q7,5 14,0M11,-545q7,5 14,0" stroke="#2e2a26" stroke-width="3.5" fill="none" stroke-linecap="round"/>
             <path d="M-24,-560q10,-3 18,0M10,-560q10,-3 18,0" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>`,
    pain: `<path d="M-21,-545l12,-3M11,-548l12,3" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>
           <path d="M-24,-556l16,-8M10,-564l16,8" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>`,
    side: `<ellipse cx="-10" cy="-546" rx="4.5" ry="6" fill="#2e2a26"/><ellipse cx="22" cy="-546" rx="4.5" ry="6" fill="#2e2a26"/>
           <path d="M-22,-562q10,-5 18,-1M12,-563q10,-4 18,1" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>`,
  };
  const MOUTH = {
    smile: `<path d="M-4,-520q6,4 12,0" stroke="#2e2a26" stroke-width="3.5" fill="none" stroke-linecap="round"/>`,
    flat: `<path d="M-5,-519h12" stroke="#2e2a26" stroke-width="3.5" fill="none" stroke-linecap="round"/>`,
    o: `<ellipse cx="2" cy="-518" rx="5" ry="7" fill="#2e2a26"/>`,
    frown: `<path d="M-5,-516q7,-5 14,0" stroke="#2e2a26" stroke-width="3.5" fill="none" stroke-linecap="round"/>`,
    scream: `<path d="M-7,-524q9,-3 18,0q-1,16 -9,16q-8,0 -9,-16z" fill="#2e2a26"/>`,
  };

  function build(parent, id, P) {
    const leg = (side) => `<g id="${id}-th${side}"><g>${limb(150, 38, P.pants, P.pantsS)}</g>
        <g transform="translate(0,150)"><g id="${id}-sh${side}">${limb(138, 34, P.pants, P.pantsS)}
          <path d="M-20,128h34q22,0 22,16v6h-56z" fill="${P.shoe}" ${OUT}/></g></g></g>`;
    const arm = (side, extra = "") => `<g id="${id}-ua${side}">${limb(122, 30, P.sleeve, P.sleeveS)}
        <g transform="translate(0,122)"><g id="${id}-fa${side}">${limb(108, 26, P.sleeve, P.sleeveS)}
          <circle cx="0" cy="118" r="15" fill="${P.skin}" ${OUT}/><g id="${id}-hand${side}">${extra}</g></g></g></g>`;
    const torch = `<g id="${id}-torch" display="none" transform="translate(0,118)"><rect x="-9" y="-6" width="18" height="44" rx="4" fill="#3d3833" ${OUT}/>
          <path id="${id}-beam" d="M-8,38L-230,900H230L8,38Z" fill="url(#beamg)"/></g>`;
    const eyes = Object.entries(EYES).map(([k, v]) => `<g class="eye-${k}" display="${k === "normal" ? "inline" : "none"}">${v}</g>`).join("");
    const mouths = Object.entries(MOUTH).map(([k, v]) => `<g class="mouth-${k}" display="${k === "smile" ? "inline" : "none"}">${v}</g>`).join("");
    const html = `<g id="${id}">
      <ellipse id="${id}-shadow" cx="0" cy="4" rx="90" ry="14" fill="#060c10" opacity=".55"/>
      <g id="${id}-root"><g id="${id}-body">
        <g transform="translate(-20,-300)">${leg("B")}</g>
        <g transform="translate(-46,-455)" opacity=".92">${arm("B")}</g>
        <g id="${id}-torso">
          <path d="M-62,-470Q-66,-482 -44,-486H44Q66,-482 62,-470L56,-300H-56Z" fill="${P.top}" ${OUT}/>
          <path d="M18,-482H40Q58,-478 54,-468L50,-302H24Z" fill="${P.topS}" opacity=".7"/>
          <rect x="-56" y="-318" width="112" height="30" rx="8" fill="${P.belt}" ${OUT}/>
          <g id="${id}-acc">${P.torsoExtra || ""}</g>
          <rect x="-14" y="-506" width="28" height="30" fill="${P.skinS}" ${OUT}/>
          <g id="${id}-head">
            <ellipse cx="0" cy="-548" rx="44" ry="52" fill="${P.skin}" ${OUT}/>
            <path d="M18,-596Q46,-570 40,-520Q30,-500 8,-497Q36,-530 18,-596Z" fill="${P.skinS}" opacity=".55"/>
            <g id="${id}-hair">${P.hair}</g>
            <g id="${id}-eyes">${eyes}</g>${P.face || ""}
            <g id="${id}-mouth">${mouths}</g>
            <g id="${id}-sweat" display="none"><path d="M40,-582c6,10 8,16 2,19c-6,-3 -6,-9 -2,-19z" fill="#cfe2e6" ${OUT}/></g>
          </g>
        </g>
        <g transform="translate(20,-300)">${leg("F")}</g>
        <g transform="translate(46,-455)">${arm("F", torch)}</g>
      </g></g></g>`;
    const g = document.createElementNS(NS, "g");
    g.innerHTML = html;
    parent.appendChild(g.firstElementChild);
    return document.getElementById(id);
  }

  // ---------- pose math ----------
  const smooth = (x) => { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); };
  const lerp = (a, b, k) => a + (b - a) * k;
  const JOINTS = ["thF", "thB", "shF", "shB", "uaF", "faF", "uaB", "faB", "torso", "head", "hair", "acc", "bodyY", "rootX", "rootY", "rootR"];
  const zero = () => Object.fromEntries(JOINTS.map((j) => [j, 0]));

  // each mode returns joint angles (degrees) for local time u since the segment started
  const MODES = {
    idle(u, o) {
      const b = Math.sin(u * 2 * Math.PI / 3.2);
      return { ...zero(), uaF: 4 + b, uaB: -4 - b, faF: -8, faB: -8, torso: 0.6 * b, head: 0.8 * Math.sin(u * 1.3), bodyY: -2 * (b + 1) };
    },
    walk(u, o) { return gait(u, o.period || 0.96, o.stride || 16, o.knee || 42, o.bob || 9, o.arm || 18, o.lean || 1.5); },
    run(u, o) { return gait(u, o.period || 0.56, o.stride || 30, o.knee || 80, o.bob || 16, o.arm || 40, o.lean || 9, true); },
    crouch(u, o) {
      const b = Math.sin(u * 2 * Math.PI / 2.4);
      return { ...zero(), thF: -70, shF: 110, thB: -40, shB: 95, torso: 22, head: -14, uaF: -40, faF: -60, uaB: -20, faB: -40, bodyY: 115 + b };
    },
    sit(u, o) { // sitting on the floor, legs forward
      const b = Math.sin(u * 2 * Math.PI / 3.6);
      return { ...zero(), thF: -88, shF: 10, thB: -86, shB: 14, torso: -4 + 0.5 * b, head: -2, uaF: -20, faF: -40, uaB: 10, faB: -20, bodyY: 290 };
    },
    lie(u, o) { // lying on the side, breathing
      const b = Math.sin(u * 2 * Math.PI / 4.0);
      return { ...zero(), thF: -6, thB: -2, shF: 8, shB: 4, uaF: -12, faF: -24, uaB: 6, faB: -10, torso: 0.4 * b, rootR: -88, rootY: -40, rootX: 0 };
    },
    tremble(u, o) {
      const j = Math.sin(u * 61) * 1.4 + Math.sin(u * 37) * 0.9;
      return { ...zero(), thF: -6, thB: 6, shF: 12, shB: 12, uaF: -24 + j, faF: -110, uaB: -28 - j, faB: -100, torso: 6 + j * 0.6, head: -6 + j, bodyY: 14 };
    },
    holdHead(u, o) { // pain: both hands to the head
      const sway = Math.sin(u * 2.2) * 3;
      return { ...zero(), uaF: -150, faF: -106, uaB: 150, faB: 106, torso: 4 + sway * 0.5, head: 8 + sway, thF: 4, thB: -4, bodyY: 6 };
    },
    sitChair(u, o) { // sitting on a bench/chair: thighs forward, shins down
      const b = Math.sin(u * 2 * Math.PI / 3.6);
      return { ...zero(), thF: -86, shF: 84, thB: -84, shB: 82, torso: -2 + 0.5 * b, head: 0, uaF: -30, faF: -50, uaB: -10, faB: -40, bodyY: 150 };
    },
    raise(u, o) { // arm raised high (phone looking for signal)
      const sway = Math.sin(u * 1.7) * 4;
      return { ...zero(), uaF: -158 + sway, faF: -8, uaB: 4, faB: -12, torso: -3, head: -12, bodyY: -4 };
    },
    phoneEar(u, o) {
      return { ...zero(), uaF: -30, faF: -150, uaB: 4, faB: -12, torso: 1, head: 3 + Math.sin(u * 1.1) * 2, bodyY: -1 };
    },
    point(u, o) {
      const b = Math.sin(u * 2 * Math.PI / 3);
      return { ...zero(), uaF: -95 + b, faF: -6, uaB: -6, faB: -10, torso: 2, head: -4, bodyY: -1 };
    },
    torch(u, o) { // flashlight held forward with a slow search sweep
      return { ...zero(), uaF: -60 + 5 * Math.sin(u * 1.3) + 1.5 * Math.sin(u * 4.1), faF: -16 + 3 * Math.sin(u * 1.3 + 0.7), uaB: 4, faB: -10, torso: 1, head: -2 + 2 * Math.sin(u * 0.9) };
    },
    fall(u, o) { // stumble down onto the knees over ~0.6 s, then stay
      const k = smooth(u / 0.6);
      return { ...zero(), thF: lerp(0, -20, k), shF: lerp(0, 95, k), thB: lerp(0, 20, k), shB: lerp(0, 100, k), torso: lerp(0, 28, k), head: lerp(0, 12, k), uaF: lerp(0, -40, k), faF: lerp(0, -30, k), uaB: lerp(0, -30, k), faB: lerp(0, -40, k), bodyY: lerp(0, 120, k) };
    },
  };

  function gait(u, period, stride, knee, bob, arm, lean, running) {
    const ramp = smooth(u / (running ? 0.3 : 0.6));
    const th = 2 * Math.PI * (u / period);
    const s = Math.sin(th), c = Math.cos(th);
    const A = stride * ramp;
    const kF = knee * Math.pow(Math.max(0, -c), 1.4) + 5 * Math.max(0, c) * Math.max(0, s);
    const kB = knee * Math.pow(Math.max(0, c), 1.4) + 5 * Math.max(0, -c) * Math.max(0, -s);
    const fa = running ? 70 : 14;
    return {
      ...zero(),
      thF: A * s, thB: -A * s, shF: kF * ramp, shB: kB * ramp,
      uaF: -arm * ramp * Math.sin(th - 0.15), uaB: arm * ramp * Math.sin(th - 0.15),
      faF: -(10 + fa * Math.max(0, -Math.sin(th - 0.5))) * ramp - (running ? 40 : 0),
      faB: -(10 + fa * Math.max(0, Math.sin(th - 0.5))) * ramp - (running ? 40 : 0),
      torso: 1.6 * ramp * s * 0.6 + lean * ramp, head: 1.4 * Math.sin(2 * th + 0.8) * ramp - (running ? lean * 0.6 : 0),
      hair: 2.4 * Math.sin(2 * th - 0.9) * ramp, acc: 3 * Math.sin(th - 1.0) * ramp,
      bodyY: -bob * ramp * (Math.cos(2 * th) + 1) / 2,
    };
  }

  // foot speed in px/s for a gait at scale 1 (legLength ~288) — use to move the world under a walker
  const footSpeed = (period, stride) => (2 * 288 * Math.sin(stride * Math.PI / 180)) / (period / 2);

  function evaluate(track, t) {
    // track: [{t, mode, opts, blend, look, eyes, mouth}] sorted by t
    let i = 0;
    while (i + 1 < track.length && track[i + 1].t <= t) i++;
    const cur = track[i];
    const pose = MODES[cur.mode]((t - cur.t), cur.opts || {});
    if (i > 0 && cur.blend) {
      const prev = track[i - 1];
      const k = smooth((t - cur.t) / cur.blend);
      if (k < 1) {
        const pp = MODES[prev.mode]((t - prev.t), prev.opts || {});
        for (const j of JOINTS) pose[j] = lerp(pp[j], pose[j], k);
      }
    }
    pose.head += cur.look || 0;
    pose._eyes = cur.eyes || "normal";
    pose._mouth = cur.mouth || "smile";
    pose._sweat = !!cur.sweat;
    pose._torch = !!(cur.torch);
    return pose;
  }

  function apply(id, p, t, blinkTimes) {
    const R = (sel, deg, ox = 0, oy = 0) => document.getElementById(`${id}-${sel}`).setAttribute("transform", `rotate(${deg.toFixed(3)} ${ox} ${oy})`);
    R("thF", p.thF); R("thB", p.thB); R("shF", p.shF); R("shB", p.shB);
    R("uaF", p.uaF); R("faF", p.faF); R("uaB", p.uaB); R("faB", p.faB);
    R("torso", p.torso, 0, -300); R("head", p.head, 0, -500); R("hair", p.hair, 0, -560); R("acc", p.acc, -40, -480);
    document.getElementById(`${id}-body`).setAttribute("transform", `translate(0 ${p.bodyY.toFixed(2)})`);
    document.getElementById(`${id}-root`).setAttribute("transform", `translate(${p.rootX} ${p.rootY}) rotate(${p.rootR})`);
    const blinking = (blinkTimes || []).some((b) => t >= b && t < b + 0.12);
    const eyes = blinking && p._eyes === "normal" ? "closed" : p._eyes;
    document.querySelectorAll(`#${id}-eyes > g`).forEach((g) => g.setAttribute("display", g.classList.contains(`eye-${eyes}`) ? "inline" : "none"));
    document.querySelectorAll(`#${id}-mouth > g`).forEach((g) => g.setAttribute("display", g.classList.contains(`mouth-${p._mouth}`) ? "inline" : "none"));
    document.getElementById(`${id}-sweat`).setAttribute("display", p._sweat ? "inline" : "none");
    document.getElementById(`${id}-torch`).setAttribute("display", p._torch ? "inline" : "none");
  }

  // Drive a character on a GSAP timeline from t0 for dur seconds using a track (times relative to t0).
  function drive(tl, id, t0, dur, track, blinkTimes) {
    const clock = { t: 0 };
    tl.to(clock, { t: dur, duration: dur, ease: "none", onUpdate: () => apply(id, evaluate(track, clock.t), clock.t, blinkTimes) }, t0);
    apply(id, evaluate(track, 0), 0, blinkTimes);
  }

  const CAST = {
    phum: {
      skin: "#e9bc93", skinS: "#c99672", top: "#b9cdd3", topS: "#8fa9b1", sleeve: "#b9cdd3", sleeveS: "#8fa9b1",
      pants: "#34434f", pantsS: "#24303a", shoe: "#2a2420", belt: "#2e2a26",
      torsoExtra: `<path d="M-14,-482L0,-420L14,-482" fill="none" stroke="#e07a4f" stroke-width="7"/><rect x="-14" y="-430" width="28" height="36" rx="4" fill="#f4ecd8" ${OUT}/>`,
      hair: `<path d="M-46,-552Q-50,-604 -6,-608Q40,-612 48,-560Q44,-574 30,-580Q10,-566 -20,-578Q-30,-566 -46,-552Z" fill="#2b2522" ${OUT}/>`,
      face: `<g fill="none" stroke="#2e2a26" stroke-width="3"><circle cx="-14" cy="-546" r="13"/><circle cx="18" cy="-546" r="13"/><path d="M-1,-546h6"/></g>`,
    },
    fon: {
      skin: "#efc6a0", skinS: "#cf9d79", top: "#d9a441", topS: "#b07f2c", sleeve: "#d9a441", sleeveS: "#b07f2c",
      pants: "#3d4d45", pantsS: "#2b3832", shoe: "#ede3cf", belt: "#3d4d45",
      torsoExtra: `<path d="M-40,-480L36,-330" stroke="#7a3f2a" stroke-width="7"/><rect x="22" y="-352" width="40" height="34" rx="6" fill="#c0603e" ${OUT}/>`,
      hair: `<path d="M-50,-540Q-56,-612 0,-612Q56,-612 50,-540Q52,-500 40,-492Q38,-540 30,-568Q0,-556 -30,-568Q-40,-536 -42,-492Q-54,-500 -50,-540Z" fill="#3e302a" ${OUT}/><rect x="14" y="-592" width="22" height="8" rx="3" fill="#e07a4f" transform="rotate(-20 25 -588)"/>`,
      face: ``,
    },
  };


  // ---------- ส้มโอ the cat: sit / alert / sick (lying, slow breathing) / walk ----------
  function buildCat(parent, id) {
    const html = `<g id="${id}"><ellipse cx="0" cy="4" rx="70" ry="10" fill="#060c10" opacity=".5"/>
      <g id="${id}-root"><g id="${id}-tail"><path d="M40,-20C90,-20 96,-70 76,-96" fill="none" stroke="#2e2a26" stroke-width="20" stroke-linecap="round"/>
        <path d="M40,-20C90,-20 96,-70 76,-96" fill="none" stroke="#e07a4f" stroke-width="12" stroke-linecap="round"/></g>
      <g id="${id}-body"><path d="M-40,0C-50,-40 -30,-80 0,-80C30,-80 50,-40 40,0Z" fill="#e07a4f" ${OUT}/>
        <path d="M-16,0C-20,-30 -10,-56 0,-56C10,-56 20,-30 16,0Z" fill="#f4ecd8"/>
        <path d="M-36,-40q9,1 13,8M36,-40q-9,1 -13,8" stroke="#a9542f" stroke-width="4" fill="none" stroke-linecap="round"/></g>
      <g id="${id}-head"><path d="M-40,-118L-40,-160L-10,-138ZM40,-118L40,-160L10,-138Z" fill="#e07a4f" ${OUT}/>
        <ellipse cx="0" cy="-112" rx="46" ry="38" fill="#e07a4f" ${OUT}/><ellipse cx="0" cy="-98" rx="16" ry="11" fill="#f4ecd8"/>
        <g class="ce-open"><circle cx="-17" cy="-118" r="9" fill="#b9cf98" ${OUT}/><circle cx="17" cy="-118" r="9" fill="#b9cf98" ${OUT}/>
          <ellipse cx="-17" cy="-118" rx="3" ry="7" fill="#2e2a26"/><ellipse cx="17" cy="-118" rx="3" ry="7" fill="#2e2a26"/></g>
        <g class="ce-closed" display="none"><path d="M-25,-117q8,6 16,0M9,-117q8,6 16,0" stroke="#2e2a26" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>
        <path d="M-4,-104h8l-4,5z" fill="#c8664a"/></g></g></g>`;
    parent.insertAdjacentHTML("beforeend", html);
    return document.getElementById(id);
  }
  function catPose(id, mode, u) {
    const R = (sel, deg, ox, oy) => document.getElementById(`${id}-${sel}`).setAttribute("transform", `rotate(${deg.toFixed(2)} ${ox} ${oy})`);
    let tail = 0, head = 0, root = "", sx = 1, sy = 1, eyes = "open";
    if (mode === "sit") { tail = 12 * Math.sin(u * 2.1); head = 3 * Math.sin(u * 0.7); }
    if (mode === "alert") { tail = 4 * Math.sin(u * 9); head = -6 + 2 * Math.sin(u * 13); sy = 1.04; }
    if (mode === "sick") { tail = 2 * Math.sin(u * 0.8); head = 70; root = "translate(0,-6) rotate(-6)"; sy = 0.62 + 0.03 * Math.sin(u * 1.4); sx = 1.25; eyes = "closed"; }
    if (mode === "hiss") { tail = -30 + 3 * Math.sin(u * 20); head = -10; sy = 1.08; }
    R("tail", tail, 40, -20); R("head", head, 0, -80);
    document.getElementById(`${id}-body`).setAttribute("transform", `translate(0 0) scale(${sx} ${sy})`);
    document.getElementById(`${id}-root`).setAttribute("transform", root);
    document.querySelectorAll(`#${id}-head .ce-open`).forEach((g) => g.setAttribute("display", eyes === "open" ? "inline" : "none"));
    document.querySelectorAll(`#${id}-head .ce-closed`).forEach((g) => g.setAttribute("display", eyes === "closed" ? "inline" : "none"));
  }
  function driveCat(tl, id, t0, dur, track) {
    const clock = { t: 0 };
    const at = (t) => { let i = 0; while (i + 1 < track.length && track[i + 1].t <= t) i++; return track[i]; };
    const go = () => { const k = at(clock.t); catPose(id, k.mode, clock.t - k.t); };
    tl.to(clock, { t: dur, duration: dur, ease: "none", onUpdate: go }, t0);
    go();
  }

  window.Rig = { build, drive, evaluate, apply, footSpeed, MODES, CAST, smooth, lerp, buildCat, driveCat };
})();
