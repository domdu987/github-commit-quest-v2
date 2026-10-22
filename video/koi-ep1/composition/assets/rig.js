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
    glow: `<circle cx="-14" cy="-546" r="20" fill="#d8ff9a" opacity=".3"/><circle cx="18" cy="-546" r="20" fill="#d8ff9a" opacity=".3"/>
           <circle cx="-14" cy="-546" r="9" fill="#e9ffc0"/><circle cx="18" cy="-546" r="9" fill="#e9ffc0"/>
           <path d="M-25,-560q10,4 19,1M9,-559q10,3 19,-2" stroke="#2e2a26" stroke-width="4" fill="none" stroke-linecap="round"/>`,
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
        <g transform="translate(0,122)"><g id="${id}-fa${side}">${limb(108, 26, P.forearm || P.sleeve, P.forearmS || P.sleeveS)}
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
            <ellipse cx="-44" cy="-540" rx="10" ry="15" fill="${P.skin}" ${OUT}/><ellipse cx="44" cy="-540" rx="10" ry="15" fill="${P.skin}" ${OUT}/>
            <ellipse cx="0" cy="-548" rx="44" ry="52" fill="${P.skin}" ${OUT}/>
            <path d="M18,-596Q46,-570 40,-520Q30,-500 8,-497Q36,-530 18,-596Z" fill="${P.skinS}" opacity=".55"/>
            <path d="M5,-537q6,8 -1,12" stroke="${P.skinS}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
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
    whistle(u, o) { // hand at the mouth (whistle, or a finger to the lips)
      const j = Math.sin(u * 9) * 1.2;
      return { ...zero(), uaF: -113 + j, faF: -158, uaB: 4, faB: -12, torso: -2, head: -6, bodyY: -1 };
    },
    wave(u, o) { // slow beckoning wave
      return { ...zero(), uaF: -150, faF: -20 + 24 * Math.sin(u * 2 * Math.PI / (o.period || 1.6)), uaB: 4, faB: -10, head: 4 * Math.sin(u * 0.8), torso: -1 };
    },
    phoneLook(u, o) { // looking down at something held in front (phone, camera)
      return { ...zero(), uaF: -52 + Math.sin(u * 1.1), faF: -92, uaB: 4, faB: -12, torso: 2, head: 10, bodyY: -1 };
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
    joe: {
      skin: "#d9a27a", skinS: "#b8835e", top: "#6e8f62", topS: "#57744d", sleeve: "#6e8f62", sleeveS: "#57744d",
      pants: "#8a7b5e", pantsS: "#6f6249", shoe: "#3a2f26", belt: "#4a3f33",
      torsoExtra: `<circle cx="0" cy="-424" r="22" fill="#f4ecd8" ${OUT}/><path d="M-10,-414Q-12,-436 10,-440Q12,-418 -10,-414Z" fill="#6e8f62"/><path d="M-10,-414L6,-432" stroke="#2e2a26" stroke-width="2.5"/><path d="M-30,-484Q0,-440 30,-484" fill="none" stroke="#e07a4f" stroke-width="5"/>`,
      hair: `<path d="M-46,-548Q-46,-560 -40,-566L-40,-540Z" fill="#2b2522"/><path d="M-48,-560Q-46,-614 0,-614Q46,-614 48,-560Z" fill="#4f6b48" ${OUT}/><path d="M22,-566h50q8,0 4,9h-54z" fill="#3e5639" ${OUT}/>`,
      face: `<path d="M-8,-504q10,7 22,0" stroke="#5a4636" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>`,
    },
    chai: {
      skin: "#c98f66", skinS: "#a87350", top: "#6b7350", topS: "#565d40", sleeve: "#6b7350", sleeveS: "#565d40",
      pants: "#565d40", pantsS: "#454b33", shoe: "#1e1a17", belt: "#2e2a26",
      torsoExtra: `<rect x="14" y="-462" width="26" height="30" rx="4" fill="#d9a441" ${OUT}/><path d="M-50,-470h22v26h-22z" fill="#8a3f2a" ${OUT}/><path d="M-36,-480V-300" stroke="#565d40" stroke-width="4"/>`,
      hair: `<path d="M-46,-560q-6,22 4,40" stroke="#9a948c" stroke-width="9" fill="none" stroke-linecap="round"/><ellipse cx="2" cy="-584" rx="74" ry="13" fill="#5a6045" ${OUT}/><path d="M-40,-586Q-38,-630 2,-632Q42,-630 44,-586Z" fill="#6b7350" ${OUT}/><path d="M-40,-596H44" stroke="#3e4230" stroke-width="7"/>`,
      face: `<path d="M-6,-529q13,-9 26,0q-13,5 -26,0z" fill="#3a3330"/><path d="M-30,-576q8,-3 14,0" stroke="#7a5a44" stroke-width="2.5" fill="none"/>`,
    },
    // ---- ค่ายคืนสุดท้าย ----
    pin: { // ปิ่น: brave volunteer, high ponytail + orange headband, teal camp tee, whistle on a lanyard
      skin: "#e8b98f", skinS: "#c8946c", top: "#4f8f86", topS: "#3a6e67", sleeve: "#4f8f86", sleeveS: "#3a6e67", forearm: "#e8b98f", forearmS: "#c8946c",
      pants: "#6f7552", pantsS: "#585d40", shoe: "#5a3f2a", belt: "#3a3f2e",
      torsoExtra: `<path d="M-24,-484L0,-428L24,-484" stroke="#e8705a" stroke-width="5" fill="none"/><path d="M-10,-436h16v-7h8a8,8 0 1 1 -8,10h-16z" fill="#f2c55c" ${OUT}/>
        <path d="M24,-450q14,-14 24,0q-10,12 -24,0z" fill="#f4ecd8" opacity=".85"/><path d="M-56,-470q4,80 2,160" stroke="#2f5550" stroke-width="5" fill="none" opacity=".6"/>`,
      hair: `<path d="M-38,-596Q-100,-588 -94,-516Q-90,-476 -70,-462Q-74,-520 -42,-570Z" fill="#3a2a22" ${OUT}/>
        <path d="M-48,-546Q-54,-606 0,-610Q52,-608 48,-556Q36,-584 2,-586Q-30,-584 -40,-560Q-42,-552 -48,-546Z" fill="#3a2a22" ${OUT}/>
        <path d="M-46,-568Q0,-598 47,-572" stroke="#e07a4f" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="-42" cy="-592" r="8" fill="#e07a4f" ${OUT}/>`,
      face: `<g fill="#c8846a"><circle cx="-24" cy="-527" r="2.2"/><circle cx="-17" cy="-523" r="2.2"/><circle cx="26" cy="-527" r="2.2"/><circle cx="33" cy="-523" r="2.2"/></g>`,
    },
    kla: { // กล้า: named "brave", is not; bucket hat, maroon flannel, backpack, plaster on the cheek
      skin: "#d6a27c", skinS: "#b5825e", top: "#9c4a3c", topS: "#7d3a2f", sleeve: "#9c4a3c", sleeveS: "#7d3a2f",
      pants: "#3b4a63", pantsS: "#2c3850", shoe: "#e8e2d4", belt: "#2e2a26",
      torsoExtra: `<rect x="-92" y="-474" width="40" height="150" rx="14" fill="#3d4d45" ${OUT}/>
        <path d="M-40,-482V-306M-8,-486V-306M24,-486V-306M-60,-440H60M-58,-378H58" stroke="#6a2e25" stroke-width="5" opacity=".75"/>
        <path d="M-20,-486Q0,-462 20,-486" fill="#f4ecd8" ${OUT}/><path d="M-34,-482Q-40,-400 -34,-322" stroke="#3d4d45" stroke-width="12" fill="none"/>`,
      hair: `<path d="M-46,-556q-10,10 -3,22q-9,7 -2,17M44,-556q8,10 2,20" stroke="#2b2522" stroke-width="10" fill="none" stroke-linecap="round"/>
        <path d="M-50,-566Q-48,-618 0,-620Q48,-618 50,-566Z" fill="#c9b98f" ${OUT}/><path d="M-48,-580Q0,-596 48,-580" stroke="#8a7a52" stroke-width="7" fill="none"/>
        <path d="M-72,-562Q0,-584 72,-562Q74,-550 62,-548Q0,-566 -62,-548Q-74,-550 -72,-562Z" fill="#b3a376" ${OUT}/>`,
      face: `<rect x="14" y="-534" width="22" height="9" rx="3" fill="#ead7b6" stroke="#2e2a26" stroke-width="2" transform="rotate(-18 25 -530)"/><path d="M-30,-532q3,3 6,0M30,-532q3,3 6,0" stroke="#d98a70" stroke-width="3" fill="none" opacity=".7"/>`,
    },
  };


  // ---- เสียงกอย ----
  Object.assign(CAST, {
    fa: { // ฟ้า: vlogger in a yellow rain poncho, black bob with bangs, white sneakers
      skin: "#ebbd95", skinS: "#cb9670", top: "#e8b830", topS: "#c4931c", sleeve: "#e8b830", sleeveS: "#c4931c", forearm: "#e8b830", forearmS: "#c4931c",
      pants: "#2f3438", pantsS: "#22272a", shoe: "#f0ece2", belt: "#d9a826",
      torsoExtra: `<path d="M-54,-486Q0,-502 54,-486Q44,-466 0,-462Q-44,-466 -54,-486Z" fill="#c4931c" ${OUT}/><path d="M0,-462V-320" stroke="#c4931c" stroke-width="4"/>
        ${[-430, -390, -350].map((y) => `<circle cx="0" cy="${y}" r="4" fill="#8a6a14"/>`).join("")}<path d="M-30,-470Q-40,-400 -20,-340" stroke="#e05a6a" stroke-width="5" fill="none"/>`,
      hair: `<path d="M-50,-540Q-58,-608 0,-612Q58,-608 50,-540L52,-498Q40,-490 32,-498L32,-560Q0,-574 -32,-560L-32,-498Q-40,-490 -52,-498Z" fill="#1f1a18" ${OUT}/>
        <path d="M-40,-572Q-6,-594 34,-580Q24,-560 -4,-566Q-24,-554 -40,-560Z" fill="#1f1a18"/>`,
      face: `<g fill="#e08a7a" opacity=".7"><ellipse cx="-24" cy="-526" rx="8" ry="4"/><ellipse cx="30" cy="-526" rx="8" ry="4"/></g>`,
    },
    tae: { // เต้: nursing student, navy rain jacket with a red-cross patch, rectangular glasses
      skin: "#e0ae86", skinS: "#bf8a64", top: "#34506e", topS: "#26405a", sleeve: "#34506e", sleeveS: "#26405a",
      pants: "#8a7b5e", pantsS: "#6f6249", shoe: "#3a2f26", belt: "#26405a",
      torsoExtra: `<path d="M0,-484V-310" stroke="#1d3046" stroke-width="5"/><rect x="16" y="-450" width="30" height="30" rx="5" fill="#f4ecd8" ${OUT}/><path d="M31,-445V-425M21,-435H41" stroke="#d8443a" stroke-width="6"/>
        <path d="M-44,-484Q-50,-400 -40,-320" stroke="#5a4636" stroke-width="10" fill="none"/>`,
      hair: `<path d="M-46,-560Q-50,-608 -4,-614Q44,-614 48,-562L40,-574L32,-560L22,-576L10,-562L-4,-578L-16,-562L-28,-576L-38,-560Z" fill="#1c1816" ${OUT}/>`,
      face: `<g fill="none" stroke="#2e2a26" stroke-width="3"><rect x="-28" y="-556" width="26" height="19" rx="6"/><rect x="6" y="-556" width="26" height="19" rx="6"/><path d="M-2,-548h8"/></g>`,
    },
    mad: { // บังหมาด: local guide, white kopiah cap, short beard, dark green shirt, walking stick
      skin: "#b9805a", skinS: "#98653f", top: "#3e5a44", topS: "#2f4734", sleeve: "#3e5a44", sleeveS: "#2f4734",
      pants: "#6b5a44", pantsS: "#544634", shoe: "#1e1e1e", belt: "#2e2a26",
      torsoExtra: `<path d="M-30,-484L0,-452L30,-484" stroke="#2f4734" stroke-width="5" fill="none"/><path d="M-50,-470Q-20,-430 -40,-330" stroke="#2f4734" stroke-width="4" fill="none" opacity=".7"/>`,
      hair: `<path d="M-46,-560q-5,16 2,30M46,-560q5,16 -2,30" stroke="#4a4440" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M-44,-570Q-44,-616 0,-618Q44,-616 44,-570Z" fill="#f0ece2" ${OUT}/><path d="M-44,-578H44" stroke="#c9c3b6" stroke-width="5"/>`,
      face: `<path d="M-38,-532Q-30,-488 4,-486Q38,-488 42,-532Q32,-506 4,-504Q-24,-506 -38,-532Z" fill="#3a3330" opacity=".85"/><path d="M-10,-526q14,-7 26,0" stroke="#3a3330" stroke-width="5" fill="none" stroke-linecap="round"/>`,
    },
  });

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
