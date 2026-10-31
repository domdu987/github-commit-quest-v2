// "ต่อหัวเสือ" motion kit (skill V11, 31 ต.ค. 2569: "Icon เอฟเฟค ขยับอย่ากาก ทำดีๆดิ"). Loads after hnui.js and replaces its cards.
// 2.5D coins in the house style of quakeui.js: a rim slab under a lit face (radial gradient), bevel, gloss arc and spark, a soft shadow;
// pop in with squash & stretch (elastic), staggered; then keep a secondary motion (bob + the pictogram's own action) until the shot ends.
//   HnFx.coin(name, x, y, s, id)       place a coin (120-unit box, face centre 60,57). names: still swat nojump run house field hospital stings
//                                      clock kidney soap ice timer lungs lips faint phone cup
//   HnFx.pop(tl, id, t) / HnFx.life(tl, id, t, dur)   entry / secondary motion of a placed coin
//   HnFx.tick(tl, layer, t, x, y, s) / HnFx.cross(tl, layer, t, x, y, s)   ✓ with a glow ring + sparks · ✗ that shakes with a red flash
//   HnFx.yard(tl, L, t0, dur, o)       atmosphere for any yard shot: dust motes in the sun, tamarind leaves drifting down, gnats; o.leaves n
//   HnFx.dust(tl, layer, t0, x, y, s)  a dust puff at a foot strike · HnFx.run(tl, layer, t0, dur, path, s) puffs along a run
//   HnFx.sting(tl, L, t, x, y, s)      a sting: white-red flash, a ring, then a welt that swells and throbs
//   HnFx.splash(tl, layer, t, x, y, s) water: a crown of spray, droplets in arcs, rings spreading
//   HnFx.swarm(tl, layer, o)           Hn.swarm + motion trails behind each hornet and blurred wing discs (same options)
//   HnFx.shakeNear(t0, a, b, amp)      a shake function for add({ shake }): rises from a to b (seconds into the shot)
//   Cards (screen space, replace HnUI.*): still indoors kidney aid count danger rules — 2.5D slab cards with coins, staged entries, idle
(function () {
  const INK = "#26201c", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const hex = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  const tone = (h, k) => { const c = hex(h), t = k >= 0 ? 255 : 0, a = Math.abs(k); return "#" + c.map((v) => Math.round(v + (t - v) * a).toString(16).padStart(2, "0")).join(""); };
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  let seq = 0;
  const HnFx = (window.HnFx = {});
  const R = (dur, p) => Math.ceil(dur / p) + 1;

  const PAL = {
    still: ["#d8f0c8", "#6aaa52"], swat: ["#fbe0da", "#d8584a"], nojump: ["#cfe8f6", "#3a8ab8"], run: ["#fde59a", "#e3a632"],
    house: ["#d8f0c8", "#6aaa52"], field: ["#fbe0da", "#d8584a"], hospital: ["#fdeaea", "#d8302a"], stings: ["#fde4d4", "#d8845e"],
    clock: ["#fde59a", "#e3a632"], kidney: ["#fbe0da", "#c8483a"], soap: ["#e0f0fb", "#4f9cc8"], ice: ["#e0f4fb", "#4fa8c8"],
    timer: ["#d8f0c8", "#4a9a4a"], lungs: ["#fbe0e4", "#d8586a"], lips: ["#fde4d4", "#d8845e"], faint: ["#e4e0f4", "#7a6ab8"],
    phone: ["#fdeaea", "#d8302a"], cup: ["#f4ead8", "#a8743a"],
  };
  let defs = `<radialGradient id="hxSh"><stop offset="0" stop-color="#1a120c" stop-opacity=".45"/><stop offset="1" stop-color="#1a120c" stop-opacity="0"/></radialGradient>
    <linearGradient id="hxBev" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>
    <radialGradient id="hxSkin" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffd8b8"/><stop offset="1" stop-color="#d89a6a"/></radialGradient>
    <linearGradient id="hxWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ac8ec"/><stop offset="1" stop-color="#2a6a9a"/></linearGradient>
    <radialGradient id="hxGlow"><stop offset="0" stop-color="#fff8c8" stop-opacity=".95"/><stop offset=".5" stop-color="#ffe060" stop-opacity=".45"/><stop offset="1" stop-color="#ffe060" stop-opacity="0"/></radialGradient>
    <radialGradient id="hxRed"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="#ff5a4a" stop-opacity=".7"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="hxWelt" cx=".45" cy=".4"><stop offset="0" stop-color="#ffb0a0"/><stop offset=".6" stop-color="#ff6a5a" stop-opacity=".8"/><stop offset="1" stop-color="#ff6a5a" stop-opacity="0"/></radialGradient>
    <linearGradient id="hxCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#f2e6cc"/></linearGradient>
    <linearGradient id="hxGloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <clipPath id="hxFace"><circle cx="60" cy="57" r="46"/></clipPath>`;
  for (const [n, [f, r]] of Object.entries(PAL)) defs += `<radialGradient id="hxF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${tone(f, 0.7)}"/><stop offset=".55" stop-color="${f}"/><stop offset="1" stop-color="${tone(f, -0.18)}"/></radialGradient>
    <linearGradient id="hxR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset=".6" stop-color="${tone(r, -0.15)}"/><stop offset="1" stop-color="${tone(r, -0.4)}"/></linearGradient>`;
  Sets.DEFS += defs;

  const hornetMini = (x, y, s, cls = "") => `<g transform="translate(${x},${y})"><g class="${cls}"><g transform="scale(${s})">${Hn.hornet({ s: 1 })}</g></g></g>`;
  const fig = (x, y, c, cls = "") => `<g transform="translate(${x},${y})" class="${cls}"><circle cx="0" cy="-30" r="9" fill="url(#hxSkin)" ${OUT(2.5)}/><path d="M0,-21v24M0,3l-10,16M0,3l10,16M0,-14l-12,8M0,-14l12,-6" stroke="${c}" stroke-width="7" stroke-linecap="round" fill="none"/></g>`;
  // the pictograms in the 0–120 coin space (centre 60,57): [inside the face clip, on top]
  const PIC = {
    still: () => [`<circle cx="60" cy="74" r="24" fill="url(#hxSkin)" ${OUT(3.5)}/><path d="M36,70C36,46 84,46 84,70Q72,58 60,60Q48,58 36,70Z" fill="#2a1e18"/>
      <path d="M50,76q4,3 8,0M64,76q4,3 8,0M54,88h12" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round"/>`, `<g class="hxOrbit">${hornetMini(60, 26, 0.42)}</g>`],
    swat: () => [`<circle cx="62" cy="74" r="22" fill="url(#hxSkin)" ${OUT(3.5)}/><path d="M52,70l8,4M72,70l-8,4M54,86q8,-6 16,0" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <g class="hxBurst" opacity="0"><circle cx="80" cy="66" r="14" fill="url(#hxRed)"/></g>`,
      `<g class="hxSwing"><path d="M22,48C14,40 16,28 26,30L40,44" fill="url(#hxSkin)" ${OUT(3)}/><path d="M20,52l-10,6" stroke="#ffffff" stroke-width="3" opacity=".7" stroke-linecap="round"/></g>${hornetMini(78, 54, 0.4, "hxJit")}`],
    nojump: () => [`<rect x="0" y="66" width="120" height="60" fill="url(#hxWater)"/><path d="M0,66q10,-6 20,0t20,0t20,0t20,0t20,0t20,0" stroke="#e6f6ff" stroke-width="4" fill="none" class="hxWave"/>
      <g class="hxDive">${fig(60, 70, "#2f62c8")}</g>${hornetMini(34, 40, 0.3, "hxJit")}${hornetMini(80, 34, 0.3, "hxJit")}`,
      `<path d="M22,98L98,18" stroke="#c8241a" stroke-width="10" stroke-linecap="round"/><path d="M22,98L98,18" stroke="#ff8a7a" stroke-width="3" stroke-linecap="round" opacity=".8"/>`],
    run: () => [`<path d="M0,96H120" stroke="#8a6a3a" stroke-width="8"/><g class="hxRunF">${fig(64, 90, "#2f62c8")}</g>
      <g class="hxLines"><path d="M18,52h20M12,64h24M20,76h16" stroke="#fff" stroke-width="4" stroke-linecap="round"/></g>`, ""],
    house: () => [`<path d="M0,100H120" stroke="#6aaa52" stroke-width="16"/><path d="M28,98V58L60,32L92,58V98Z" fill="#c8884a" ${OUT(3.5)}/><path d="M22,60L60,28L98,60" stroke="#a01e18" stroke-width="9" fill="none" stroke-linecap="round"/>
      <rect x="50" y="70" width="20" height="28" fill="#3a2010"/><g class="hxDoor"><rect x="50" y="70" width="20" height="28" fill="#7a4a28" ${OUT(2.5)}/></g><rect x="74" y="64" width="12" height="12" fill="#cfe6f4" ${OUT(2)}/>`, ""],
    field: () => [`<path d="M0,96H120" stroke="#8aaa52" stroke-width="20"/><circle cx="86" cy="30" r="12" fill="#ffd23a" ${OUT(2.5)}/>${fig(54, 90, "#2f62c8")}
      ${hornetMini(36, 50, 0.26, "hxJit")}${hornetMini(66, 44, 0.26, "hxJit")}${hornetMini(50, 36, 0.26, "hxJit")}`, ""],
    hospital: () => [`<path d="M24,100V44H96V100Z" fill="#fff" ${OUT(3.5)}/><rect x="24" y="44" width="72" height="12" fill="#e8e4dc"/><g class="hxPulse"><path d="M54,58h12v10h10v12h-10v10h-12v-10h-10v-12h10z" fill="#d8302a" ${OUT(2.5)}/></g>`, ""],
    stings: () => [`<g transform="rotate(-25 60 60)"><rect x="12" y="44" width="96" height="34" rx="17" fill="url(#hxSkin)" ${OUT(3.5)}/>
      ${[[30, 56], [46, 66], [60, 54], [74, 64], [88, 56]].map(([x, y]) => `<g class="hxWelt"><circle cx="${x}" cy="${y}" r="7" fill="url(#hxWelt)"/><circle cx="${x}" cy="${y}" r="2.2" fill="#a01e18"/></g>`).join("")}</g>`, ""],
    clock: () => [`<circle cx="60" cy="60" r="34" fill="#fff" ${OUT(3.5)}/><path d="M60,26v6M60,88v6M26,60h6M88,60h6" stroke="${INK}" stroke-width="3"/>
      <g class="hxHand"><path d="M60,60V36" stroke="${INK}" stroke-width="4.5" stroke-linecap="round"/></g><g class="hxHand2"><path d="M60,60L76,60" stroke="#d8302a" stroke-width="4" stroke-linecap="round"/></g><circle cx="60" cy="60" r="4" fill="${INK}"/>`, ""],
    kidney: () => [`<g class="hxBeat"><path d="M40,34C18,34 18,86 40,86C54,86 52,66 58,60C52,54 54,34 40,34Z" fill="#c8504a" ${OUT(3.5)}/><path d="M80,34C102,34 102,86 80,86C66,86 68,66 62,60C68,54 66,34 80,34Z" fill="#c8504a" ${OUT(3.5)}/>
      <path d="M30,46q-4,12 0,24M90,46q4,12 0,24" stroke="#f0a090" stroke-width="4" fill="none" stroke-linecap="round"/></g>`, ""],
    soap: () => [`<rect x="30" y="58" width="60" height="32" rx="12" fill="#f4c8e0" ${OUT(3.5)}/><path d="M38,64h28" stroke="#fff" stroke-width="4" opacity=".7" stroke-linecap="round"/>
      <g class="hxBub">${[[44, 46, 7], [62, 38, 9], [80, 46, 6]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#e8f6ff" stroke="#6aaad0" stroke-width="2"/>`).join("")}</g>`, ""],
    ice: () => [`<rect x="24" y="44" width="72" height="44" rx="14" fill="#e8e4d8" ${OUT(3.5)}/>${[36, 60, 84].map((x) => `<rect x="${x - 10}" y="56" width="20" height="20" rx="4" fill="#bfe4f8" stroke="#4f9cc8" stroke-width="2"/>`).join("")}
      <g class="hxSpark"><path d="M30,36l3,-8l3,8l8,3l-8,3l-3,8l-3,-8l-8,-3z" fill="#fff"/><path d="M88,32l2,-5l2,5l5,2l-5,2l-2,5l-2,-5l-5,-2z" fill="#fff"/></g>`, ""],
    timer: () => [`<circle cx="60" cy="62" r="32" fill="#fff" ${OUT(3.5)}/><rect x="54" y="22" width="12" height="8" rx="2" fill="${INK}"/>
      <path class="hxArc" d="M60,30A32,32 0 1 1 59.9,30" stroke="#2fa864" stroke-width="7" fill="none" pathLength="1" stroke-dasharray="1 1"/><text x="60" y="70" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${INK}">20</text>`, ""],
    lungs: () => [`<g class="hxBreath"><path d="M56,40C30,36 20,84 30,92C42,98 54,88 56,72Z" fill="#f4a0a8" ${OUT(3.5)}/><path d="M64,40C90,36 100,84 90,92C78,98 66,88 64,72Z" fill="#f4a0a8" ${OUT(3.5)}/></g>
      <path d="M60,24V56" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`, ""],
    lips: () => [`<circle cx="60" cy="62" r="32" fill="url(#hxSkin)" ${OUT(3.5)}/><circle cx="48" cy="54" r="3.5" fill="${INK}"/><circle cx="72" cy="54" r="3.5" fill="${INK}"/>
      <g class="hxSwell"><path d="M44,74q16,-10 32,0q-16,16 -32,0Z" fill="#e85a5a" ${OUT(2.5)}/></g>`, ""],
    faint: () => [`<path d="M14,92H106" stroke="${INK}" stroke-width="4"/><circle cx="32" cy="80" r="10" fill="url(#hxSkin)" ${OUT(2.5)}/><path d="M44,84h44" stroke="#2a2a30" stroke-width="12" stroke-linecap="round"/>
      <g class="hxStars">${[[22, 58], [36, 50], [50, 58]].map(([x, y]) => `<path d="M${x},${y - 6}l2,4l4,2l-4,2l-2,4l-2,-4l-4,-2l4,-2z" fill="#ffd23a" stroke="${INK}" stroke-width="1.2"/>`).join("")}</g>`, ""],
    phone: () => [`<g class="hxRing"><rect x="40" y="26" width="40" height="70" rx="8" fill="#2a2a32" ${OUT(3.5)}/><rect x="45" y="34" width="30" height="50" rx="3" fill="#d8302a"/>
      <text x="60" y="64" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="13" fill="#fff">1669</text></g>
      <g class="hxWv"><path d="M88,40q8,8 0,16M94,34q14,14 0,28" stroke="#d8302a" stroke-width="4" fill="none" stroke-linecap="round"/></g>`, ""],
    cup: () => [`<path d="M38,32h44l-6,62h-32Z" fill="#fff" ${OUT(3.5)}/><g class="hxSlosh"><path d="M41,62q19,-6 38,0l-4,30h-30Z" fill="#7a4a1a"/></g><path d="M44,40v14" stroke="#fff" stroke-width="4" opacity=".7" stroke-linecap="round"/>`, ""],
  };
  HnFx.coin = (name, x, y, s = 1, id = "") => {
    const [inside, top] = PIC[name]();
    return `<g transform="translate(${x},${y}) scale(${s}) translate(-60,-60)"><g ${id ? `id="${id}"` : ""} class="hxCoin">
      <ellipse class="hxSh" cx="60" cy="122" rx="48" ry="9" fill="url(#hxSh)"/>
      <g class="hxBob"><g class="hxSq">
        <circle cx="60" cy="67" r="52" fill="url(#hxR-${name})" ${OUT(4)}/><path d="M12,67A48,48 0 0 0 108,67" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
        <circle cx="60" cy="57" r="52" fill="url(#hxF-${name})" ${OUT(4)}/><circle cx="60" cy="57" r="46" fill="none" stroke="url(#hxBev)" stroke-width="4"/>
        <g clip-path="url(#hxFace)">${inside}</g>${top || ""}
        <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle class="hxGlint" cx="53.5" cy="15.5" r="3" fill="#fff" opacity=".8"/>
      </g></g></g></g>`;
  };
  HnFx.pop = (tl, id, t) => {
    const r = document.getElementById(id); if (!r) return;
    tl.set(r, { opacity: 0 }, 0); tl.set(r, { opacity: 1 }, t);
    r.querySelectorAll(".hxSq").forEach((e) => tl.fromTo(e, { scaleX: 0.25, scaleY: 1.6, svgOrigin: "60 118" }, { scaleX: 1, scaleY: 1, svgOrigin: "60 118", duration: 0.8, ease: "elastic.out(1, 0.4)", immediateRender: false }, t));
    r.querySelectorAll(".hxBob").forEach((e) => tl.fromTo(e, { y: -70 }, { y: 0, duration: 0.45, ease: "bounce.out", immediateRender: false }, t));
  };
  HnFx.life = (tl, id, t, dur) => {
    const r = document.getElementById(id); if (!r) return;
    const q = (s) => r.querySelectorAll(s);
    q(".hxBob").forEach((e) => tl.fromTo(e, { y: 0 }, { y: -6, duration: 0.85, repeat: R(dur, 0.85), yoyo: true, ease: "sine.inOut", immediateRender: false }, t + 0.5));
    q(".hxSh").forEach((e) => tl.fromTo(e, { scaleX: 1, opacity: 1, svgOrigin: "60 122" }, { scaleX: 0.8, opacity: 0.55, svgOrigin: "60 122", duration: 0.85, repeat: R(dur, 0.85), yoyo: true, ease: "sine.inOut", immediateRender: false }, t + 0.5));
    q(".hxGlint").forEach((e) => tl.fromTo(e, { scale: 0.4, opacity: 0.3, svgOrigin: "53.5 15.5" }, { scale: 1.6, opacity: 1, svgOrigin: "53.5 15.5", duration: 0.5, repeat: R(dur, 1.4), repeatDelay: 0.9, yoyo: true, ease: "sine.inOut", immediateRender: false }, t + 0.7));
    q(".hxOrbit").forEach((e) => tl.fromTo(e, { rotation: 0, svgOrigin: "60 70" }, { rotation: 360, svgOrigin: "60 70", duration: 1.6, repeat: R(dur, 1.6), ease: "none", immediateRender: false }, t));
    q(".hxSwing").forEach((e) => tl.fromTo(e, { rotation: -26, svgOrigin: "40 44" }, { rotation: 18, svgOrigin: "40 44", duration: 0.22, repeat: R(dur, 0.22), yoyo: true, ease: "power2.inOut", immediateRender: false }, t));
    q(".hxBurst").forEach((e) => tl.fromTo(e, { opacity: 0, scale: 0.4, svgOrigin: "80 66" }, { opacity: 1, scale: 1.3, svgOrigin: "80 66", duration: 0.22, repeat: R(dur, 0.44), yoyo: true, ease: "power2.out", immediateRender: false }, t + 0.11));
    q(".hxJit").forEach((e, i) => tl.fromTo(e, { x: -3, y: 2 }, { x: 3, y: -2, duration: 0.09 + i * 0.01, repeat: R(dur, 0.09), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".hxWave").forEach((e) => tl.fromTo(e, { x: 0 }, { x: -40, duration: 1, repeat: R(dur, 1), ease: "none", immediateRender: false }, t));
    q(".hxDive").forEach((e) => tl.fromTo(e, { y: 30 }, { y: -6, duration: 0.7, repeat: R(dur, 1.4), yoyo: true, ease: "power2.inOut", immediateRender: false }, t));
    q(".hxRunF").forEach((e) => tl.fromTo(e, { y: 0, rotation: -4, svgOrigin: "64 90" }, { y: -6, rotation: 6, svgOrigin: "64 90", duration: 0.16, repeat: R(dur, 0.16), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".hxLines").forEach((e) => tl.fromTo(e, { x: 10, opacity: 1 }, { x: -14, opacity: 0.2, duration: 0.3, repeat: R(dur, 0.3), ease: "power1.in", immediateRender: false }, t));
    q(".hxDoor").forEach((e) => tl.fromTo(e, { scaleX: 0.05, svgOrigin: "50 70" }, { scaleX: 1, svgOrigin: "50 70", duration: 0.35, repeat: R(dur, 1.6), repeatDelay: 1.25, ease: "back.out(3)", immediateRender: false }, t + 0.4));
    q(".hxPulse").forEach((e) => tl.fromTo(e, { scale: 1, svgOrigin: "60 74" }, { scale: 1.18, svgOrigin: "60 74", duration: 0.3, repeat: R(dur, 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".hxWelt").forEach((e, i) => tl.fromTo(e, { scale: 0.7, transformOrigin: "50% 50%" }, { scale: 1.3, transformOrigin: "50% 50%", duration: 0.35, repeat: R(dur, 0.7), yoyo: true, ease: "sine.inOut", immediateRender: false }, t + i * 0.08));
    q(".hxHand").forEach((e) => tl.fromTo(e, { rotation: 0, svgOrigin: "60 60" }, { rotation: 360, svgOrigin: "60 60", duration: 1.2, repeat: R(dur, 1.2), ease: "none", immediateRender: false }, t));
    q(".hxHand2").forEach((e) => tl.fromTo(e, { rotation: 0, svgOrigin: "60 60" }, { rotation: 360, svgOrigin: "60 60", duration: 4, repeat: R(dur, 4), ease: "none", immediateRender: false }, t));
    q(".hxBeat").forEach((e) => tl.fromTo(e, { scale: 1, svgOrigin: "60 60" }, { scale: 0.9, svgOrigin: "60 60", duration: 0.26, repeat: R(dur, 0.52), yoyo: true, ease: "power2.inOut", immediateRender: false }, t));
    q(".hxBub").forEach((e) => tl.fromTo(e, { y: 6, opacity: 1 }, { y: -14, opacity: 0, duration: 0.9, repeat: R(dur, 0.9), ease: "power1.out", immediateRender: false }, t));
    q(".hxSpark").forEach((e) => tl.fromTo(e, { opacity: 0.2, scale: 0.7, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1.2, transformOrigin: "50% 50%", duration: 0.4, repeat: R(dur, 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".hxArc").forEach((e) => tl.fromTo(e, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: Math.max(1, dur - 0.5), ease: "power1.inOut", immediateRender: false }, t));
    q(".hxBreath").forEach((e) => tl.fromTo(e, { scaleX: 1, scaleY: 1, svgOrigin: "60 60" }, { scaleX: 0.86, scaleY: 0.93, svgOrigin: "60 60", duration: 0.32, repeat: R(dur, 0.32), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".hxSwell").forEach((e) => tl.fromTo(e, { scale: 1, svgOrigin: "60 74" }, { scale: 1.35, svgOrigin: "60 74", duration: 0.4, repeat: R(dur, 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".hxStars").forEach((e) => tl.fromTo(e, { rotation: 0, svgOrigin: "36 58" }, { rotation: 360, svgOrigin: "36 58", duration: 1.4, repeat: R(dur, 1.4), ease: "none", immediateRender: false }, t));
    q(".hxRing").forEach((e) => tl.fromTo(e, { rotation: -6, svgOrigin: "60 60" }, { rotation: 6, svgOrigin: "60 60", duration: 0.06, repeat: R(dur, 0.06), yoyo: true, ease: "none", immediateRender: false }, t));
    q(".hxWv").forEach((e) => tl.fromTo(e, { opacity: 0, x: -4 }, { opacity: 1, x: 4, duration: 0.3, repeat: R(dur, 0.6), yoyo: true, ease: "power1.out", immediateRender: false }, t));
    q(".hxSlosh").forEach((e) => tl.fromTo(e, { rotation: -6, svgOrigin: "60 76" }, { rotation: 6, svgOrigin: "60 76", duration: 0.5, repeat: R(dur, 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
  };
  const coinIn = (tl, id, t, dur) => { HnFx.pop(tl, id, t); HnFx.life(tl, id, t, Math.max(0.5, dur)); };

  // ✓: a green 2.5D stamp with a glow ring and sparks · ✗: a red stamp that shakes and flashes
  HnFx.tick = (tl, layer, t, x, y, s = 1) => {
    const id = `hxk${seq++}`;
    put(layer, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}" opacity="0"><circle id="${id}-g" r="60" fill="url(#hxGlow)"/>
      <circle cy="6" r="34" fill="#0a4a26" ${OUT(3)}/><circle r="34" fill="#2fa864" stroke="#fff" stroke-width="5"/><path d="M-22,-8A24,24 0 0 1 -6,-24" stroke="#fff" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/>
      <path id="${id}-c" d="M-15,0l10,11l20,-23" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1"/>
      <g id="${id}-s">${[0, 1, 2, 3, 4, 5].map((k) => { const a = k * 1.047; return `<path d="M${f1(Math.cos(a) * 44)},${f1(Math.sin(a) * 44)}l${f1(Math.cos(a) * 14)},${f1(Math.sin(a) * 14)}" stroke="#ffe060" stroke-width="5" stroke-linecap="round"/>`; }).join("")}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0, scale: 0.2, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.5, ease: "back.out(3.5)", immediateRender: false }, t);
    tl.fromTo(`#${id}-c`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.28, ease: "power2.out", immediateRender: false }, t + 0.15);
    tl.fromTo(`#${id}-g`, { scale: 0.3, opacity: 1, svgOrigin: "0 0" }, { scale: 1.6, opacity: 0, svgOrigin: "0 0", duration: 0.6, ease: "power2.out", immediateRender: false }, t + 0.2);
    tl.fromTo(`#${id}-s`, { scale: 0.5, opacity: 1, svgOrigin: "0 0" }, { scale: 1.5, opacity: 0, svgOrigin: "0 0", duration: 0.5, ease: "power2.out", immediateRender: false }, t + 0.25);
    return id;
  };
  HnFx.cross = (tl, layer, t, x, y, s = 1) => {
    const id = `hxx${seq++}`;
    put(layer, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}" opacity="0"><circle id="${id}-f" r="64" fill="url(#hxRed)"/>
      <circle cy="6" r="36" fill="#6a0e0a" ${OUT(3)}/><circle r="36" fill="#d8302a" stroke="#fff" stroke-width="5"/><path d="M-22,-10A26,26 0 0 1 -6,-26" stroke="#fff" stroke-width="4" fill="none" opacity=".55" stroke-linecap="round"/>
      <path d="M-14,-14L14,14M14,-14L-14,14" stroke="#fff" stroke-width="10" stroke-linecap="round"/></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0, scale: 1.8, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.25, ease: "power3.in", immediateRender: false }, t);
    tl.fromTo(`#${id}`, { x: 0 }, { x: 9, duration: 0.45, ease: (p) => Math.sin(p * Math.PI * 8) * (1 - p), immediateRender: false }, t + 0.25);
    tl.fromTo(`#${id}-f`, { scale: 0.4, opacity: 1, svgOrigin: "0 0" }, { scale: 1.8, opacity: 0, svgOrigin: "0 0", duration: 0.5, ease: "power2.out", immediateRender: false }, t + 0.22);
    return id;
  };

  // ---------------- atmosphere and effects ----------------
  HnFx.yard = (tl, L, t0, dur, o = {}) => {
    Pop2.particles(tl, L.glow, { type: "dust", n: o.dust ?? 26, box: o.box || [-300, 300, 1700, 1300], t0, dur, seed: o.seed || 11 });
    const r = mk(o.seed || 17), n = o.leaves ?? 6, id = `hxl${seq++}`;
    let s = "";
    for (let k = 0; k < n; k++) s += `<g id="${id}-${k}"><path d="M0,-9C7,-6 7,6 0,9C-7,6 -7,-6 0,-9Z" fill="${["#9ab84a", "#c8b44a", "#7a9a3a"][k % 3]}" stroke="#4a5a20" stroke-width="1.6"/></g>`;
    put(L.fg, `<g>${s}</g>`);
    for (let k = 0; k < n; k++) {
      const x0 = (o.leafX ?? 200) + r() * (o.leafW ?? 900), y0 = (o.leafY ?? 300) + r() * 200, fall = 700 + r() * 500, sp = 3.2 + r() * 2.5, ph = r() * 3;
      const el = document.getElementById(`${id}-${k}`), c = { t: 0 };
      const place = (t) => { const u = ((t + ph) % sp) / sp; el.setAttribute("transform", `translate(${f1(x0 + Math.sin(u * 9 + k) * 70 + u * 120)},${f1(y0 + u * fall)}) rotate(${f1(u * 540 + k * 40)}) scale(${(1.2 + (k % 3) * 0.4).toFixed(2)})`); el.setAttribute("opacity", f1(Math.min(1, (1 - u) * 3))); };
      place(0); tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => place(c.t) }, t0);
    }
  };
  HnFx.dust = (tl, layer, t, x, y, s = 1) => {
    const id = `hxd${seq++}`;
    put(layer, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}" opacity="0">${[[-30, -6, 22], [0, -14, 30], [28, -4, 20], [-12, -22, 16]].map(([dx, dy, r]) => `<circle cx="${dx}" cy="${dy}" r="${r}" fill="#d8b88a" opacity=".55"/>`).join("")}</g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0.9, scale: 0.4, y: 0, svgOrigin: "0 0" }, { opacity: 0, scale: 1.6, y: -20, svgOrigin: "0 0", duration: 0.7, ease: "power2.out", immediateRender: false }, t);
  };
  HnFx.run = (tl, layer, t0, dur, path, s = 1, step = 0.28) => {   // path [[t, x, y]…] relative to t0 (feet)
    for (let t = 0.1; t < dur; t += step) {
      let p = path[0]; for (let i = 1; i < path.length; i++) if (t >= path[i - 1][0] && t <= path[i][0]) { const u = (t - path[i - 1][0]) / (path[i][0] - path[i - 1][0] || 1); p = [t, path[i - 1][1] + (path[i][1] - path[i - 1][1]) * u, path[i - 1][2] + (path[i][2] - path[i - 1][2]) * u]; }
      if (t > path[path.length - 1][0]) p = path[path.length - 1];
      HnFx.dust(tl, layer, t0 + t, p[1], p[2], s);
    }
  };
  HnFx.sting = (tl, L, t, x, y, s = 1) => {
    const id = `hxs${seq++}`;
    put(L.glow, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}" opacity="0"><circle id="${id}-f" r="70" fill="url(#hxRed)"/><circle id="${id}-r" r="30" fill="none" stroke="#fff" stroke-width="6"/>
      <g id="${id}-w"><circle r="18" fill="url(#hxWelt)"/><circle r="5" fill="#a01e18"/></g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0); tl.set(`#${id}`, { opacity: 1 }, t);
    tl.fromTo(`#${id}-f`, { scale: 0.3, opacity: 1, svgOrigin: "0 0" }, { scale: 1.8, opacity: 0, svgOrigin: "0 0", duration: 0.35, ease: "power2.out", immediateRender: false }, t);
    tl.fromTo(`#${id}-r`, { scale: 0.3, opacity: 1, svgOrigin: "0 0" }, { scale: 2.2, opacity: 0, svgOrigin: "0 0", duration: 0.45, ease: "power2.out", immediateRender: false }, t);
    tl.fromTo(`#${id}-w`, { scale: 0.2, svgOrigin: "0 0" }, { scale: 1.15, svgOrigin: "0 0", duration: 0.5, ease: "back.out(3)", immediateRender: false }, t + 0.1);
    tl.to(`#${id}-w`, { scale: 0.95, svgOrigin: "0 0", duration: 0.3, repeat: 12, yoyo: true, ease: "sine.inOut" }, t + 0.6);
    put(L.light, `<rect id="${id}-x" width="1080" height="1920" fill="#ff3a2a" opacity="0"/>`); tl.set(`#${id}-x`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}-x`, { opacity: 0.35 }, { opacity: 0, duration: 0.3, immediateRender: false }, t);
  };
  HnFx.splash = (tl, layer, t, x, y, s = 1) => {
    const id = `hxp${seq++}`, r = mk(seq * 7 + 3);
    let drops = "";
    for (let k = 0; k < 14; k++) drops += `<g id="${id}-d${k}"><path d="M0,-8c-6,10 -6,16 0,16c6,0 6,-6 0,-16z" fill="#cfe8f6" stroke="#4a8ab0" stroke-width="1.5"/></g>`;
    put(layer, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}" opacity="0">
      ${[0, 1, 2].map((k) => `<ellipse id="${id}-r${k}" rx="60" ry="14" fill="none" stroke="#e6f6ff" stroke-width="5"/>`).join("")}
      <path id="${id}-c" d="M-60,0Q-50,-90 -24,-40Q-10,-120 0,-50Q12,-120 26,-40Q52,-90 60,0Z" fill="#e6f6ff" opacity=".85" stroke="#7ab8d8" stroke-width="3"/>${drops}</g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0); tl.set(`#${id}`, { opacity: 1 }, t);
    tl.fromTo(`#${id}-c`, { scaleY: 0.1, scaleX: 0.6, opacity: 1, svgOrigin: "0 0" }, { scaleY: 1, scaleX: 1.2, opacity: 0, svgOrigin: "0 0", duration: 0.7, ease: "power2.out", immediateRender: false }, t);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-r${k}`, { scale: 0.3, opacity: 1, svgOrigin: "0 0" }, { scale: 2.6, opacity: 0, svgOrigin: "0 0", duration: 1.1, ease: "power1.out", immediateRender: false }, t + k * 0.22));
    for (let k = 0; k < 14; k++) { const a = -Math.PI * (0.15 + 0.7 * r()), v = 120 + r() * 160, dx = Math.cos(a) * v, dy = Math.sin(a) * v;
      tl.fromTo(`#${id}-d${k}`, { x: 0, y: 0, opacity: 1 }, { x: dx * 1.4, y: 0, duration: 0.8, ease: "none", immediateRender: false }, t);
      tl.fromTo(`#${id}-d${k}`, { y: 0 }, { y: dy, duration: 0.35, ease: "power2.out", immediateRender: false }, t);
      tl.to(`#${id}-d${k}`, { y: 60, opacity: 0, duration: 0.45, ease: "power2.in" }, t + 0.35); }
  };
  // the swarm with trails and wing blur: wraps Hn.swarm, then adds a short streak behind every hornet each frame
  HnFx.swarm = (tl, layer, o = {}) => {
    const id = Hn.swarm(tl, layer, o), root = document.getElementById(id);
    const kids = [...root.children];
    kids.forEach((g) => { g.insertAdjacentHTML("afterbegin", `<path class="hxTr" d="M0,0" stroke="#3a2a1a" stroke-width="${f1(4 * (o.s ?? 0.5))}" stroke-linecap="round" opacity=".28" fill="none"/>`);
      g.querySelector(".hnw")?.insertAdjacentHTML("afterbegin", `<ellipse cx="-24" cy="-10" rx="30" ry="16" fill="#e8eef4" opacity=".3"/>`); });
    const prev = kids.map(() => null), c = { t: 0 };
    const trail = () => kids.forEach((g, k) => {
      const m = /translate\(([-\d.]+),([-\d.]+)\)/.exec(g.getAttribute("transform") || ""); if (!m) return;
      const x = +m[1], y = +m[2], p = prev[k] || [x, y]; prev[k] = [x, y];
      const dx = (p[0] - x) * 4, dy = (p[1] - y) * 4;
      g.querySelector(".hxTr").setAttribute("d", `M0,0L${f1(Math.max(-90, Math.min(90, dx)))},${f1(Math.max(-90, Math.min(90, dy)))}`);
    });
    tl.to(c, { t: o.dur, duration: o.dur, ease: "none", immediateRender: false, onUpdate: trail }, o.t0 || 0);
    return id;
  };
  HnFx.shakeNear = (a, b, amp = 8) => (t) => { const k = Math.max(0, Math.min(1, (t - a) / Math.max(0.01, b - a))); return k ? { x: amp * k * Math.sin(t * 47), y: amp * 0.7 * k * Math.sin(t * 53), r: 0 } : 0; };

  // ---------------- 2.5D cards (replace HnUI's flat ones) ----------------
  const slabCard = (id, x, y, W, H, head, hc) => `<g transform="translate(${x},${y})"><g id="${id}">
    <rect x="${-W / 2}" y="14" width="${W}" height="${H}" rx="36" fill="${tone(hc, -0.45)}" ${OUT(5)}/>
    <g filter="url(#muDrop)"><rect x="${-W / 2}" y="0" width="${W}" height="${H}" rx="36" fill="url(#hxCard)" ${OUT(5)}/></g>
    <path d="M${-W / 2},36Q${-W / 2},0 ${-W / 2 + 36},0H${W / 2 - 36}Q${W / 2},0 ${W / 2},36V112H${-W / 2}Z" fill="${hc}" ${OUT(5)}/>
    <rect x="${-W / 2 + 20}" y="8" width="${W - 40}" height="40" rx="18" fill="url(#hxGloss)"/>
    <text y="80" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#fff" stroke="${tone(hc, -0.5)}" stroke-width="6" paint-order="stroke">${head}</text>`;
  const cardIn = (tl, id, t0, dur) => {
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { y: 140, opacity: 0, rotation: -3, svgOrigin: "0 0" }, { y: 0, opacity: 1, rotation: 0, svgOrigin: "0 0", duration: 0.55, ease: "back.out(2.2)", immediateRender: false }, t0);
    tl.fromTo(`#${id}`, { rotation: 0, svgOrigin: "0 400" }, { rotation: 0.8, svgOrigin: "0 400", duration: 1.3, repeat: R(dur, 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.55);
    tl.to(`#${id}`, { opacity: 0, y: -40, duration: 0.22, ease: "power2.in" }, t0 + dur - 0.22);
  };
  const label = (x, y, t, c = INK, fs = 40) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${fs}" fill="${c}">${t}</text>`;
  const coinRow = (id, items, cy, scale = 2.3) => items.map(([n, x, lab, c], k) => `<g id="${id}-w${k}">${HnFx.coin(n, x, cy, scale, `${id}-c${k}`)}${lab ? label(x, cy + 66 * scale + 40, lab, c, scale > 2 ? 46 : 40) : ""}</g>`).join("");
  const rowIn = (tl, id, items, t0, dur, gap = 0.16) => items.forEach((_, k) => { coinIn(tl, `${id}-c${k}`, t0 + 0.35 + k * gap, dur - 0.35 - k * gap);
    tl.set(`#${id}-w${k} text`, { opacity: 0 }, 0); tl.fromTo(`#${id}-w${k} text`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, t0 + 0.6 + k * gap); });

  HnUI.still = (tl, layer, t0, dur, o = {}) => {
    const id = `hq${seq++}`, Y = o.y ?? 360, items = [["still", -220, "ยืนนิ่ง", "#1e7a48"], ["swat", 220, "ปัด = โดนต่อย", "#a01e18"]];
    put(layer, slabCard(id, 540, Y, 940, 600, "ต่อตัวเดียว · ทำยังไง?", "#e3a632") + coinRow(id, items, 320) + `</g></g>`);
    cardIn(tl, id, t0, dur); rowIn(tl, id, items, t0, dur, 0.25);
    HnFx.tick(tl, layer, t0 + 1.0, 540 - 220 + 130, Y + 200, 1.1); HnFx.cross(tl, layer, t0 + 1.4, 540 + 220 + 130, Y + 200, 1.1);
  };
  HnUI.indoors = (tl, layer, t0, dur, o = {}) => {
    const id = `hq${seq++}`, Y = o.y ?? 360, items = [["field", -220, "ที่โล่ง", "#a01e18"], ["house", 220, "เข้าบ้าน", "#1e7a48"]];
    put(layer, slabCard(id, 540, Y, 940, 600, "ถูกรุม · วิ่งไปไหน?", "#1e7a48") + coinRow(id, items, 330) + `</g></g>`);
    cardIn(tl, id, t0, dur); rowIn(tl, id, items, t0, dur, 0.25);
    HnFx.cross(tl, layer, t0 + 1.0, 540 - 220 + 130, Y + 200, 1.1); HnFx.tick(tl, layer, t0 + 1.5, 540 + 220 + 130, Y + 200, 1.1);
  };
  HnUI.kidney = (tl, layer, t0, dur, o = {}) => {
    const id = `hq${seq++}`, Y = o.y ?? 340, items = [["stings", -300, "หลายแผล"], ["clock", 0, "ภายใน 2 วัน"], ["kidney", 300, "ไต", "#a01e18"]];
    put(layer, slabCard(id, 540, Y, 980, 800, "พิษที่มาทีหลัง", "#a01e18") + coinRow(id, items, 320, 1.85)
      + `<g id="${id}-ar">${[-150, 150].map((x) => `<path d="M${x - 30},330h50l-14,-14M${x + 20},330l-14,14" stroke="${INK}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`).join("")}</g>
      <g id="${id}-u">${HnFx.coin("cup", -330, 660, 0.95, `${id}-cu`)}<rect x="-230" y="620" width="560" height="84" rx="42" fill="#fff3d6" ${OUT(4)}/>${label(50, 676, "ฉี่น้อย · สีเข้มเหมือนชา", "#a01e18", 42)}</g></g></g>`);
    cardIn(tl, id, t0, dur); rowIn(tl, id, items, t0, dur, 0.3);
    tl.set(`#${id}-ar`, { opacity: 0 }, 0); tl.fromTo(`#${id}-ar`, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.3, immediateRender: false }, t0 + 0.9);
    tl.set(`#${id}-u`, { opacity: 0 }, 0); tl.fromTo(`#${id}-u`, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0 + 1.3); coinIn(tl, `${id}-cu`, t0 + 1.3, dur - 1.3);
  };
  HnUI.aid = (tl, layer, t0, dur, o = {}) => {
    const id = `hq${seq++}`, Y = o.y ?? 380, at = o.at || [0.8, 1.6, 2.4], items = [["soap", -300, "น้ำ + สบู่"], ["ice", 0, "ประคบเย็น"], ["timer", 300, "20 นาที"]];
    put(layer, slabCard(id, 540, Y, 980, 700, "ปฐมพยาบาล", "#1e7a48") + coinRow(id, items, 320, 1.85) + `</g></g>`);
    cardIn(tl, id, t0, dur); rowIn(tl, id, items, t0, dur, 0.25);
    at.forEach((a, k) => HnFx.tick(tl, layer, t0 + a, 540 + items[k][1] + 100, Y + 220, 0.85));
  };
  HnUI.count = (tl, layer, t0, dur, o = {}) => {
    const id = `hq${seq++}`, Y = o.y ?? 360, n = o.n || 14;
    const dots = Array.from({ length: n }, (_, k) => [-250 + ((k * 137) % 500), -30 + ((k * 61) % 60)]);
    put(layer, slabCard(id, 540, Y, 960, 780, "ยังไม่พอ", "#d8302a") + `<g transform="translate(0,330)">
      <rect x="-330" y="-56" width="660" height="140" rx="70" fill="#a8744a" ${OUT(4)}/><rect x="-330" y="-70" width="660" height="140" rx="70" fill="url(#hxSkin)" ${OUT(4)}/>
      <path d="M-290,-40H260" stroke="#fff" stroke-width="10" opacity=".35" stroke-linecap="round"/>
      ${dots.map(([x, y], k) => `<g id="${id}-d${k}" opacity="0"><g transform="translate(${x},${y})"><g class="${id}-dw"><circle r="20" fill="url(#hxWelt)"/><circle r="5" fill="#a01e18"/></g></g></g>`).join("")}</g>
      <g transform="translate(0,560)"><g id="${id}-nb"><text id="${id}-n" y="10" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="120" fill="#a01e18" stroke="#fff" stroke-width="10" paint-order="stroke">0</text></g>
      ${label(0, 80, "แผล", INK, 40)}</g>
      <g id="${id}-w" opacity="0" transform="translate(0,690)"><rect x="-340" y="-36" width="680" height="84" rx="42" fill="#6a0e0a" ${OUT(4)}/><rect x="-340" y="-46" width="680" height="84" rx="42" fill="#d8302a" ${OUT(4)}/>${label(0, 10, "เกิน 10 แผล เสี่ยงอาการรุนแรง", "#fff", 42)}</g></g></g>`);
    cardIn(tl, id, t0, dur);
    const span = Math.min(dur * 0.5, 2.2), el = () => document.getElementById(`${id}-n`);
    tl.call(() => { const e = el(); if (e) e.textContent = "0"; }, null, t0);
    dots.forEach((_, k) => { const t = t0 + 0.5 + (k / n) * span; tl.set(`#${id}-d${k}`, { opacity: 0 }, 0);
      tl.fromTo(`#${id}-d${k}`, { opacity: 0 }, { opacity: 1, duration: 0.05, immediateRender: false }, t);
      tl.fromTo(`#${id}-d${k} .${id}-dw`, { scale: 0.2, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(4)", immediateRender: false }, t);
      tl.call(() => { const e = el(); if (e) e.textContent = String(k + 1); }, null, t);
      tl.fromTo(`#${id}-nb`, { scale: 1.25, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.15, ease: "power2.out", immediateRender: false }, t); });
    const tw = t0 + 0.5 + span * (10 / n);
    tl.set(`#${id}-w`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}-w`, { opacity: 0, scale: 0.4, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(3)", immediateRender: false }, tw);
    tl.fromTo(`#${id}-w`, { x: 0 }, { x: 8, duration: 0.4, ease: (p) => Math.sin(p * Math.PI * 8) * (1 - p), immediateRender: false }, tw + 0.45);
  };
  HnUI.danger = (tl, layer, t0, dur, o = {}) => {
    const id = `hq${seq++}`, Y = o.y ?? 360, items = [["lungs", -300, "หายใจลำบาก"], ["lips", 0, "ปากบวม"], ["faint", 300, "เป็นลม"]];
    put(layer, slabCard(id, 540, Y, 980, 820, "อาการแบบนี้ โทรทันที", "#d8302a") + coinRow(id, items, 320, 1.85)
      + `<g transform="translate(0,680)"><g id="${id}-ph">${HnFx.coin("phone", -190, 0, 1.0, `${id}-pc`)}<rect x="-110" y="-30" width="320" height="104" rx="52" fill="#6a0e0a" ${OUT(4)}/><rect x="-110" y="-44" width="320" height="104" rx="52" fill="#d8302a" ${OUT(4)}/>
        ${label(50, 28, "โทร 1669", "#fff", 64)}</g></g></g></g>`);
    cardIn(tl, id, t0, dur); rowIn(tl, id, items, t0, dur, 0.28);
    tl.set(`#${id}-ph`, { opacity: 0 }, 0); tl.fromTo(`#${id}-ph`, { opacity: 0, scale: 0.4, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.5, ease: "back.out(3)", immediateRender: false }, t0 + 1.3);
    tl.fromTo(`#${id}-ph`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.07, svgOrigin: "0 0", duration: 0.3, repeat: R(dur, 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.8);
    coinIn(tl, `${id}-pc`, t0 + 1.3, dur - 1.3);
  };
  // the rule board: the teak board hung from the shrine by its cloth; 2.5D coins per rule, the active row with a highlighter swipe
  const RULECOIN = ["nojump", "hospital"];
  HnUI.rules = (tl, layer, t0, dur, o = {}) => {
    const id = `hr${seq++}`, active = o.active ?? -1, done = o.done || [], Y = o.y ?? 420, W = 940, H = 260 + HnUI.RULES.length * 220;
    let c = `<path d="M-300,-${Y}L-260,40M300,-${Y}L260,40" stroke="#d8302a" stroke-width="22"/><path d="M-300,-${Y}L-260,40M300,-${Y}L260,40" stroke="#ffd23a" stroke-width="6" stroke-dasharray="18 22"/>
      <rect x="${-W / 2}" y="36" width="${W}" height="${H}" rx="24" fill="#5a3418" ${OUT(6)}/>
      <g filter="url(#muDrop)"><rect x="${-W / 2}" y="20" width="${W}" height="${H}" rx="22" fill="#9a6234" ${OUT(6)}/></g>
      ${Array.from({ length: 8 }, (_, k) => `<path d="M${-W / 2 + 20},${80 + k * 110}q${W / 2},${k % 2 ? 14 : -12} ${W - 40},0" stroke="#6a3e1e" stroke-width="3" fill="none" opacity=".5"/>`).join("")}
      <rect x="${-W / 2 + 26}" y="46" width="${W - 52}" height="${H - 52}" rx="14" fill="url(#hxCard)" ${OUT(4)}/><rect x="${-W / 2 + 40}" y="54" width="${W - 80}" height="50" rx="20" fill="url(#hxGloss)"/>
      <text y="140" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#a01e18" stroke="#fff" stroke-width="8" paint-order="stroke">กฎของตาเพิ่ม</text>
      <path id="${id}-ul0" d="M-200,164q200,14 400,0" stroke="#f08a1a" stroke-width="6" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1"/>
      ${[-290, 290].map((x) => `<circle cx="${x}" cy="120" r="13" fill="#6a3e1e"/><circle cx="${x - 3}" cy="117" r="4" fill="#c8884a"/>`).join("")}`;
    HnUI.RULES.forEach(([a, b], k) => {
      const y = 310 + k * 220, st = done.includes(k) ? "done" : k === active ? "active" : active < 0 ? "all" : "next";
      c += `<g id="${id}-row${k}" opacity="${st === "next" ? 0.38 : 1}">`;
      if (st === "active") c += `<rect id="${id}-hl" x="-290" y="${y - 78}" width="690" height="156" rx="22" fill="#ffd23a" opacity=".6"/>`;
      c += HnFx.coin(RULECOIN[k] || "hospital", -350, y, 1.15, `${id}-i${k}`);
      c += `<text x="-260" y="${y - 12}" font-family="Kanit" font-weight="${st === "active" ? 900 : 800}" font-size="${a.length > 14 ? 46 : 54}" fill="${INK}">${a}</text>
        <text x="-260" y="${y + 56}" font-family="Kanit" font-weight="900" font-size="54" fill="#a01e18">${b}</text>`;
      if (st === "active") c += `<path id="${id}-ul" d="M-260,${y + 72}h${b.length * 34}" stroke="#d8302a" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
      c += `</g>`;
    });
    put(layer, `<g transform="translate(540,${Y})"><g id="${id}">${c}</g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { y: -760, rotation: -5, opacity: 1, svgOrigin: `0 -${Y}` }, { y: 0, rotation: 0, svgOrigin: `0 -${Y}`, duration: 0.8, ease: "bounce.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}`, { rotation: 0, svgOrigin: `0 -${Y}` }, { rotation: 1.4, svgOrigin: `0 -${Y}`, duration: 1.1, repeat: R(dur, 1.1), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.8);
    tl.fromTo(`#${id}-ul0`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.4, immediateRender: false }, t0 + 0.6);
    HnUI.RULES.forEach((_, k) => { HnFx.pop(tl, `${id}-i${k}`, t0 + 0.7 + k * 0.15); HnFx.life(tl, `${id}-i${k}`, t0 + 0.7, dur - 0.7); });
    done.forEach((k) => HnFx.tick(tl, layer, t0 + 0.9 + k * 0.15, 540 + 390, Y + 310 + k * 220, 0.85));
    if (active >= 0) {
      tl.fromTo(`#${id}-hl`, { scaleX: 0, svgOrigin: "-290 0" }, { scaleX: 1, svgOrigin: "-290 0", duration: 0.45, ease: "power3.out", immediateRender: false }, t0 + 0.9);
      tl.fromTo(`#${id}-ul`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, immediateRender: false }, t0 + 1.3);
    }
    tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  };
})();
