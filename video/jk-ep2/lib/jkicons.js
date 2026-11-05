// สกิลจอมโกหก · animated icon badges in the channel's coin style (paper disc, coloured ring, ink line glyph), but every glyph keeps
// moving while it is on screen: ears pulse red, the SSR star spins, the snail crawls, the creatures wag their tails, the crown
// sparkles, the horns grow. All on the shot clock. Load after nkui3.js.
//   JKI.badge(tl, layer, t0, dur, { kind, x, y, s, tone, label, at, end })      a coin with a pill label under it
//   JKI.counter(tl, layer, t0, dur, { icon, x, y, w, from, to, unit, at, rollAt, count, steps: [[t, v]], tone, plus })
//   JKI.ring(tl, layer, t0, dur, { x, y, s, from, to, at, count, steps: [[t, v]], tone, label, labelAt })   a percent ring
//   JKI.chain(tl, layer, t0, dur, items: [{ icon, label, tone }], { y, gap, s, ats: [t…] })               coins joined by arrows
//   JKI.coin(kind, x, y, s, id, tone) · JKI.idle(tl, id, kind, t0, dur) · JKI.out(tl, sel, at)
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const { C, INK, enter, loop } = NkV;
  const T = (x, y, size, text, o = {}) => `<text${o.id ? ` id="${o.id}"` : ""} x="${f1(x)}" y="${f1(y)}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 900}" font-size="${size}" fill="${o.fill || INK}">${text}</text>`;
  const L5 = `fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`;
  const O4 = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const TONE = { yellow: C.yellowD, green: C.green, red: C.red, blue: C.blue, white: "#8a8f98", grey: "#9aa0a6" };
  let seq = 0;
  const nid = (p) => `${p}${seq++}`;
  // v2 · depth: a shaded ring, a domed disc with a gloss arc, embossed glyphs, a sheen sweep and a sparkle burst on entry
  Sets.DEFS += `<linearGradient id="jkiRing" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".6"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>
    <radialGradient id="jkiDisc" cx=".4" cy=".34" r=".8"><stop offset="0" stop-color="#fffdf6"/><stop offset=".65" stop-color="${C.paper}"/><stop offset="1" stop-color="#dfd4bc"/></radialGradient>
    <linearGradient id="jkiPill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#e9e0cb"/></linearGradient>
    <linearGradient id="jkiTrack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfc5ad"/><stop offset="1" stop-color="#ece5d4"/></linearGradient>
    <filter id="jkiGlyph" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="2.5" stdDeviation="1.2" flood-color="#2a1a10" flood-opacity=".35"/></filter>
    <filter id="jkiSoft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>`;
  const SPARK = (id) => `<g id="${id}-bs">${[0, 60, 120, 180, 240, 300].map((a, k) => `<g id="${id}-bs${k}" transform="rotate(${a})" opacity="0"><path d="M0,-78v-16M-6,-86h12" stroke="${k % 2 ? C.yellow : "#fff"}" stroke-width="5" stroke-linecap="round"/></g>`).join("")}</g>
    <g id="${id}-cf">${[...Array(10)].map((_, k) => `<rect id="${id}-cf${k}" x="-6" y="-9" width="12" height="18" rx="2" fill="${[C.red, C.yellow, C.blue, C.green, "#fff", "#ff8ab8"][k % 6]}" opacity="0"/>`).join("")}</g><circle id="${id}-fl" r="64" fill="#fff" opacity="0"/>`;

  const face = `<circle r="22" ${L5}/><path d="M-8,-6v3M8,-6v3" ${L5}/>`;
  const GLY = {
    ears: (id) => `${face}<path d="M-8,10h16" ${L5}/><g id="${id}-gl" opacity="0"><circle cx="-26" r="18" fill="${C.red}" opacity=".45"/><circle cx="26" r="18" fill="${C.red}" opacity=".45"/></g>
      <g id="${id}-eL"><ellipse cx="-26" rx="7" ry="10" fill="${C.red}" ${O4}/></g><g id="${id}-eR"><ellipse cx="26" rx="7" ry="10" fill="${C.red}" ${O4}/></g>`,
    earsHeart: (id) => `<g transform="translate(0,8)">${face}<path d="M-7,10q7,6 14,0" ${L5}/><g id="${id}-gl" opacity="0"><circle cx="-26" r="18" fill="${C.red}" opacity=".45"/><circle cx="26" r="18" fill="${C.red}" opacity=".45"/></g>
      <ellipse cx="-26" rx="7" ry="10" fill="${C.red}" ${O4}/><ellipse cx="26" rx="7" ry="10" fill="${C.red}" ${O4}/></g>
      <g id="${id}-ht"><path d="M0,-24C-4,-34 -18,-32 -16,-22C-14,-15 0,-6 0,-6C0,-6 14,-15 16,-22C18,-32 4,-34 0,-24Z" fill="${C.red}" ${O4}/></g>`,
    star: (id) => `<g id="${id}-ry">${[0, 45, 90, 135, 180, 225, 270, 315].map((a) => `<path d="M0,-33V-42" stroke="${C.yellowD}" stroke-width="4" stroke-linecap="round" transform="rotate(${a})"/>`).join("")}</g>
      <g id="${id}-st"><path d="M0,-27L8,-9L27,-9L12,3L17,22L0,11L-17,22L-12,3L-27,-9L-8,-9Z" fill="${C.yellow}" ${O4}/></g>`,
    cardF: (id) => `<g id="${id}-cd"><rect x="-18" y="-26" width="36" height="52" rx="5" fill="#c3c8cd" ${O4}/>${T(0, 12, 30, "F", { fill: "#5a5f66" })}</g>`,
    snail: (id) => `<g id="${id}-sn"><path d="M-30,16Q-26,2 -8,2H22Q30,2 30,10V16Z" fill="${C.paper}" ${L5}/><path d="M-26,6L-30,-8M-18,4L-16,-10" ${L5}/><circle cx="-30" cy="-9" r="3.5" fill="${INK}"/><circle cx="-16" cy="-11" r="3.5" fill="${INK}"/>
      <g id="${id}-sh"><circle cx="8" cy="-8" r="16" fill="${C.yellow}" ${L5}/><circle cx="8" cy="-8" r="8" ${L5}/><circle cx="8" cy="-8" r="2.5" fill="${INK}"/></g></g>`,
    believer: (id) => `<circle cy="-10" r="10" ${L5}/><path d="M-16,28Q-16,6 0,6Q16,6 16,28" ${L5}/>
      <g id="${id}-b"><path d="M8,-36h24v16h-14l-6,6v-6h-4z" fill="${C.yellow}" ${O4}/>${T(20, -24, 13, "+1")}</g>`,
    bucket: (id) => `<path d="M-16,34Q-16,16 0,16Q16,16 16,34" ${L5}/><g id="${id}-bk"><path d="M-20,-30H20L24,12H-24Z" fill="${C.paper}" ${L5}/><path d="M-22,-16h44M-23,-2h46" ${L5}/><path d="M-10,-7h5M5,-7h5" ${L5}/></g>`,
    gecko: (id) => `<g id="${id}-tl"><path d="M-14,4Q-28,10 -32,-4Q-34,-14 -24,-14Q-18,-12 -22,-6" ${L5}/></g>
      <path d="M-14,4Q-6,-9 10,-8Q22,-7 24,0Q14,9 -14,6Z" fill="${C.paper}" ${L5}/><path d="M20,-2Q24,-15 34,-9Q39,-1 30,4Q24,4 20,-2Z" fill="${C.paper}" ${L5}/>
      <path d="M-4,-6l-6,-9M-4,-6l-10,-4M-4,-6l-1,-11M10,-6l5,-10M10,-6l10,-6M10,-6l1,-12M-6,6l-7,8M-6,6l-11,2M8,6l6,9M8,6l10,4" ${L5}/>
      <circle cx="29" cy="-7" r="2.6" fill="${INK}"/><circle cx="-4" cy="-2" r="1.6" fill="${INK}" opacity=".5"/><circle cx="6" cy="-3" r="1.6" fill="${INK}" opacity=".5"/>`,
    monitor: (id) => `<g id="${id}-tl"><path d="M-16,4Q-30,8 -36,-4Q-38,-12 -32,-14" ${L5}/><path d="M-24,2l-2,-6M-30,-2l-2,-6" ${L5}/></g>
      <path d="M-16,4Q-8,-9 10,-9Q26,-9 30,-1Q20,8 -16,7Z" fill="${C.paper}" ${L5}/><path d="M26,-5Q34,-12 41,-5Q39,2 30,2Z" fill="${C.paper}" ${L5}/>
      <path d="M41,-3l7,-1M48,-4l3,-3M48,-4l3,3" stroke="${C.red}" stroke-width="2.6" stroke-linecap="round" fill="none"/>
      <path d="M-8,7l-4,9M-4,7l0,10M8,7l4,9M12,7l1,10" ${L5}/><path d="M-10,-9h4M-2,-10h4M6,-10h4" ${L5}/><circle cx="33" cy="-7" r="2.4" fill="${INK}"/>`,
    croc: (id) => `<g id="${id}-tl"><path d="M-20,3Q-32,4 -36,-6Q-38,-12 -32,-14" ${L5}/><path d="M-26,0l-2,-7M-32,-6l-1,-7" ${L5}/></g>
      <path d="M-20,-1Q-8,-11 8,-7L32,-5Q38,0 32,5L8,7Q-8,9 -20,5Z" fill="${C.paper}" ${L5}/>
      <path d="M-14,-8l3,-6l3,6M-5,-10l3,-6l3,6M4,-9l3,-6l3,6" ${L5}/><path d="M12,0h20" ${L5}/><path d="M14,0l3,4l3,-4l3,4l3,-4l3,4l3,-4" stroke="${INK}" stroke-width="2.4" fill="none" stroke-linejoin="round"/>
      <circle cx="14" cy="-9" r="4" fill="${C.paper}" ${L5}/><circle cx="15" cy="-9" r="1.8" fill="${INK}"/><path d="M-10,8l-3,8M12,8l3,8" ${L5}/>`,
    dragon: (id) => `<g id="${id}-tl"><path d="M-14,8Q-28,8 -32,-6L-36,-10" ${L5}/><path d="M-36,-10l-5,-5l0,8l6,2Z" fill="${INK}"/></g>
      <path d="M-14,6Q-8,-7 6,-7Q18,-7 20,3Q8,12 -14,6Z" fill="${C.paper}" ${L5}/>
      <g id="${id}-wg"><path d="M0,-7L-10,-27L-32,-31Q-24,-24 -26,-17Q-18,-13 -17,-9Q-8,-8 0,-7Z" fill="${C.paper}" ${L5}/><path d="M-10,-27L-26,-17M-10,-27L-17,-9" stroke="${INK}" stroke-width="2"/></g>
      <path d="M18,-1Q22,-17 36,-13L41,-7Q33,0 24,2Z" fill="${C.paper}" ${L5}/><path d="M24,2L39,1L35,8Z" fill="${C.paper}" ${L5}/>
      <path d="M31,-6l2,4M36,-7l2,4" stroke="${INK}" stroke-width="2" stroke-linecap="round"/><path d="M25,-14l-5,-8M30,-16l-1,-9" ${L5}/>
      <circle cx="30" cy="-9" r="2.8" fill="${C.yellow}" stroke="${INK}" stroke-width="1.5"/><circle cx="31" cy="-9" r="1.2" fill="${INK}"/>
      <g id="${id}-fr"><path d="M41,-3q9,-7 14,-2q-7,2 -2,9q-9,-2 -12,-7z" fill="${C.red}"/><path d="M43,-3q5,-3 8,0q-4,1 -1,5q-5,-2 -7,-5z" fill="${C.yellow}"/></g>
      <path d="M-6,10l-2,8M10,10l2,8" ${L5}/>`,
    crown: (id) => `<g id="${id}-sp" opacity="0">${[[-30, -30], [32, -28], [0, 32]].map(([x, y]) => `<path d="M${x},${y - 7}v14M${x - 7},${y}h14" stroke="${C.yellowD}" stroke-width="4" stroke-linecap="round"/>`).join("")}</g>
      <g id="${id}-cr"><path d="M-26,12L-30,-14L-12,0L0,-20L12,0L30,-14L26,12Z" fill="${C.yellow}" ${L5}/><path d="M-26,12H26V22H-26Z" fill="${C.yellowD}" ${L5}/><circle cx="-30" cy="-14" r="3.5" fill="${INK}"/><circle cy="-20" r="3.5" fill="${INK}"/><circle cx="30" cy="-14" r="3.5" fill="${INK}"/></g>`,
    horns: (id) => `<g transform="translate(0,6)"><circle r="20" ${L5}/><path d="M-7,-4v3M7,-4v3" ${L5}/><path d="M-6,9q6,4 12,0" ${L5}/></g>
      <g id="${id}-h1"><path d="M-14,-10Q-26,-24 -16,-40Q-16,-24 -7,-12Z" fill="${C.red}" ${L5}/></g><g id="${id}-h2"><path d="M14,-10Q26,-24 16,-40Q16,-24 7,-12Z" fill="${C.red}" ${L5}/></g>`,
    whisper: (id) => `<circle r="20" cx="-6" cy="2" ${L5}/><path d="M-13,-4v3M1,-4v3" ${L5}/><path d="M-3,13q4,-4 8,0" ${L5}/><path d="M6,24Q16,10 12,0" ${L5}/><g id="${id}-w"><path d="M20,-8h10M22,0h12M20,8h10" ${L5}/></g>`,
    percent: (id) => `<g id="${id}-pc">${T(0, 14, 40, "%")}</g>`,
  };
  const coin = (kind, x, y, s, id, tone = "yellow") => { const tc = TONE[tone] || TONE.yellow;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><ellipse id="${id}-gs" cy="16" rx="58" ry="13" fill="#000" opacity=".26" filter="url(#jkiSoft)"/><g id="${id}">
      <circle r="63" fill="#000" opacity=".16" cy="4"/><circle r="62" fill="${tc}"/><circle r="62" fill="url(#jkiRing)"/><circle r="62" fill="none" stroke="#000" stroke-opacity=".22" stroke-width="2"/>
      <circle r="52" fill="url(#jkiDisc)"/><circle r="52" fill="none" stroke="#000" stroke-opacity=".14" stroke-width="5"/><circle r="49" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>
      <path d="M-38,-26A48,48 0 0 1 24,-42" stroke="#fff" stroke-opacity=".75" stroke-width="5" fill="none" stroke-linecap="round"/>
      <g filter="url(#jkiGlyph)" transform="scale(1.3)">${(GLY[kind] || GLY.percent)(id)}</g>
      <clipPath id="${id}-cp"><circle r="62"/></clipPath><g clip-path="url(#${id}-cp)"><g id="${id}-sw" transform="translate(-150,0)"><rect x="-22" y="-90" width="44" height="180" fill="#fff" opacity=".5" transform="rotate(24)"/><rect x="30" y="-90" width="14" height="180" fill="#fff" opacity=".3" transform="rotate(24)"/></g></g>
      ${SPARK(id)}<circle id="${id}-halo" r="62" fill="none" stroke="${tc}" stroke-width="6" opacity="0"/></g></g>`; };
  // entry with the sheen sweep and the sparkle burst; a slow hover afterwards (the ground shadow breathes with it)
  const enterC = (tl, id, at, o = {}) => { const sel = `#${id}`; tl.set(sel, { autoAlpha: 0 }, 0); tl.set(sel, { autoAlpha: 1 }, at); // autoAlpha: a fully transparent group under the drop-shadow filter paints as a black box in Chrome, so hide it outright until it enters
    // a coin flipped onto the screen: edge-on and small, spinning to face us, lands a little too big, settles with a wobble
    tl.fromTo(sel, { scaleX: 0.06, scaleY: 0.5, rotation: -40, svgOrigin: "0 0" }, { scaleX: 1.14, scaleY: 1.1, rotation: 6, svgOrigin: "0 0", duration: 0.36, ease: "power2.out" }, at);
    tl.to(sel, { scaleX: 1, scaleY: 1, rotation: 0, svgOrigin: "0 0", duration: 0.55, ease: "elastic.out(1.1, 0.42)" }, at + 0.36);
    tl.fromTo(`#${id}-fl`, { opacity: 0.85 }, { opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, at + 0.3);
    tl.fromTo(`#${id}-halo`, { opacity: 0.9, scale: 0.9, svgOrigin: "0 0" }, { opacity: 0, scale: 2.0, svgOrigin: "0 0", duration: 0.6, ease: "power2.out", immediateRender: false }, at + 0.3);
    tl.fromTo(`#${id}-sw`, { x: -150 }, { x: 150, duration: 0.5, ease: "power2.inOut", immediateRender: false }, at + 0.34);
    for (let k = 0; k < 6; k++) tl.fromTo(`#${id}-bs${k}`, { opacity: 1, scale: 0.3, svgOrigin: "0 0" }, { opacity: 0, scale: 1.4, svgOrigin: "0 0", duration: 0.55, ease: "power2.out", immediateRender: false }, at + 0.3 + (k % 3) * 0.04);
    for (let k = 0; k < 10; k++) { const a = (k / 10) * Math.PI * 2 + 0.3, d = 95 + (k % 3) * 22, dx = Math.cos(a) * d, dy = Math.sin(a) * d - 40;
      tl.fromTo(`#${id}-cf${k}`, { x: 0, y: 0, rotation: 0, opacity: 1, scale: 0.6, svgOrigin: "0 0" }, { x: dx, y: dy, rotation: 200 + k * 40, scale: 1, svgOrigin: "0 0", duration: 0.42, ease: "power2.out", immediateRender: false }, at + 0.3);
      tl.to(`#${id}-cf${k}`, { y: dy + 90, rotation: 320 + k * 40, opacity: 0, duration: 0.5, ease: "power1.in" }, at + 0.72); }
    if (o.end != null) { const n = Math.floor((o.end - at - 1.2) / 2.8); for (let k = 1; k <= n; k++) tl.fromTo(`#${id}-sw`, { x: -150 }, { x: 150, duration: 0.6, ease: "power2.inOut", immediateRender: false }, at + 0.34 + k * 2.8); } };
  const hover = (tl, id, t0, dur, amp = 4) => { if (dur <= 0.3) return; loop(tl, `#${id}`, { y: -amp }, { y: amp }, 1.6, t0, dur); loop(tl, `#${id}-gs`, { scale: 1.06, opacity: 0.3, svgOrigin: "0 16" }, { scale: 0.92, opacity: 0.2, svgOrigin: "0 16" }, 1.6, t0, dur); };
  function idle(tl, id, kind, t0, dur) {
    const q = (s) => `#${id}-${s}`;
    if (!document.querySelector(`#${id}`) || dur <= 0.2) return;
    if (kind === "ears" || kind === "earsHeart") { loop(tl, q("gl"), { opacity: 0 }, { opacity: 1 }, 0.55, t0, dur); if (kind === "ears") ["eL", "eR"].forEach((e) => loop(tl, q(e), { scale: 1, svgOrigin: "0 0" }, { scale: 1.18, svgOrigin: "0 0" }, 0.55, t0, dur)); }
    if (kind === "earsHeart") loop(tl, q("ht"), { scale: 1, svgOrigin: "0 -20" }, { scale: 1.25, svgOrigin: "0 -20" }, 0.5, t0, dur);
    if (kind === "star") { loop(tl, q("st"), { rotation: -10, svgOrigin: "0 0" }, { rotation: 10, svgOrigin: "0 0" }, 1.0, t0, dur); loop(tl, q("ry"), { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, svgOrigin: "0 0" }, 4, t0, dur, { yoyo: false }); }
    if (kind === "cardF") loop(tl, q("cd"), { rotation: -8, svgOrigin: "0 0" }, { rotation: 8, svgOrigin: "0 0" }, 0.9, t0, dur);
    if (kind === "snail") { loop(tl, q("sn"), { x: -4 }, { x: 4 }, 1.8, t0, dur); loop(tl, q("sh"), { rotation: -6, svgOrigin: "8 -8" }, { rotation: 6, svgOrigin: "8 -8" }, 0.9, t0, dur); }
    if (kind === "believer") loop(tl, q("b"), { y: 0 }, { y: -5 }, 0.7, t0, dur);
    if (kind === "bucket") loop(tl, q("bk"), { rotation: -6, svgOrigin: "0 12" }, { rotation: 6, svgOrigin: "0 12" }, 1.0, t0, dur);
    if (["gecko", "monitor", "croc", "dragon"].includes(kind)) loop(tl, q("tl"), { rotation: -14, svgOrigin: "-12 4" }, { rotation: 14, svgOrigin: "-12 4" }, kind === "gecko" ? 0.5 : 0.8, t0, dur);
    if (kind === "dragon") loop(tl, q("wg"), { scaleY: 0.8, svgOrigin: "0 -6" }, { scaleY: 1.1, svgOrigin: "0 -6" }, 0.6, t0, dur);
    if (kind === "crown") { loop(tl, q("cr"), { scale: 1, svgOrigin: "0 4" }, { scale: 1.08, svgOrigin: "0 4" }, 0.9, t0, dur); loop(tl, q("sp"), { opacity: 0 }, { opacity: 1 }, 0.5, t0, dur); }
    if (kind === "horns") ["h1", "h2"].forEach((h, i) => loop(tl, q(h), { scale: 0.85, svgOrigin: `${i ? 11 : -11} -12` }, { scale: 1.12, svgOrigin: `${i ? 11 : -11} -12` }, 0.8, t0, dur));
    if (kind === "whisper") loop(tl, q("w"), { opacity: 0.2, x: 0 }, { opacity: 1, x: 3 }, 0.4, t0, dur);
    if (kind === "percent") loop(tl, q("pc"), { scale: 1, svgOrigin: "0 0" }, { scale: 1.15, svgOrigin: "0 0" }, 0.6, t0, dur);
  }
  const pill = (txt, id, o = {}) => { const w = o.w ?? 40 + txt.length * 24;
    return `<g id="${id}"><rect x="${f1(-w / 2)}" y="-21" width="${f1(w)}" height="48" rx="24" fill="#000" opacity=".22"/><rect x="${f1(-w / 2)}" y="-24" width="${f1(w)}" height="48" rx="24" fill="${o.fill || "url(#jkiPill)"}" ${O4}/>
      <rect x="${f1(-w / 2 + 10)}" y="-19" width="${f1(w - 20)}" height="9" rx="4.5" fill="#fff" opacity=".55"/>${T(0, 12, o.size || 30, txt, { fill: o.ink || INK, w: 800 })}</g>`; };
  const out = (tl, sel, at) => tl.to(sel, { scale: 0, opacity: 0, svgOrigin: "0 0", duration: 0.3, ease: "back.in(2)" }, at);
  const FIX = () => window.OVFIX || "";   // landscape: the overlay layer is stretched to the wide frame; each icon undoes that stretch so it stays round
  const G = (layer) => { const g = document.createElementNS("http://www.w3.org/2000/svg", "g"); layer.appendChild(g); return g; };

  // ---------------- a coin with a label under it ----------------
  function badge(tl, layer, t0, dur, o) {
    const id = nid("jki"), s = o.s ?? 1, g = G(layer);
    put(g, `<g data-ovfix="1" transform="translate(${f1(o.x)},${f1(o.y)}) ${FIX()}" filter="url(#nvDrop)"><g id="${id}-w">${coin(o.kind, 0, 0, s, `${id}-c`, o.tone)}
      ${o.label ? `<g transform="translate(0,${f1(96 * s)})">${pill(o.label, `${id}-l`, { size: o.labelSize ?? 30 })}</g>` : ""}</g></g>`);
    const a = t0 + (o.at ?? 0), end = o.end != null ? t0 + o.end : t0 + dur;
    enterC(tl, `${id}-c`, a, { end });
    if (o.label) { tl.fromTo(`#${id}-l`, { opacity: 0, scale: 1.8, rotation: -7, svgOrigin: "0 0" }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.32, ease: "back.out(3.2)" }, a + 0.42);
      tl.fromTo(`#${id}-l rect:nth-of-type(3)`, { opacity: 1 }, { opacity: 0.55, duration: 0.4, immediateRender: false }, a + 0.74); }
    idle(tl, `${id}-c`, o.kind, a + 0.95, end - a - 0.95); hover(tl, `${id}-c`, a + 1.0, end - a - 1.0);
    if (o.end != null) out(tl, `#${id}-w`, end);
    return id;
  }

  // ---------------- a counter sticker: the coin, a number that rolls, its unit ----------------
  function counter(tl, layer, t0, dur, o = {}) {
    const id = nid("jkn"), x = o.x ?? 44, y = o.y ?? 250, w = o.w ?? 330, from = o.from ?? 0, g = G(layer);
    put(g, `<g data-ovfix="1" transform="translate(${x},${y}) ${FIX()} rotate(-3)"><g id="${id}" filter="url(#nvDrop)"><rect width="${w}" height="104" rx="52" fill="url(#jkiPill)" ${O4}/><rect x="14" y="8" width="${w - 28}" height="16" rx="8" fill="#fff" opacity=".5"/>
      ${coin(o.icon, 52, 52, 0.66, `${id}-c`, o.tone || "yellow")}${T(w - 104 - (o.unitW ?? 0), 76, 70, String(from).replace(/\B(?=(\d{3})+(?!\d))/g, ","), { id: `${id}-v`, anchor: "end" })}
      <g id="${id}-pl" opacity="0">${T(w - 100 - (o.unitW ?? 0), 70, 52, "+", { anchor: "start", fill: C.red })}</g>${T(w - 26, 74, 34, o.unit || "", { anchor: "end", w: 800 })}</g></g>`);
    const a = t0 + (o.at ?? 0), c = { v: from }, el = () => document.getElementById(`${id}-v`), fmt = (v) => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    if (!o.still) { tl.fromTo(`#${id}`, { x: -140, opacity: 0, rotation: -8, svgOrigin: "0 52" }, { x: 0, opacity: 1, rotation: 0, svgOrigin: "0 52", duration: 0.5, ease: "back.out(1.8)" }, a); enterC(tl, `${id}-c`, a + 0.15); }
    const steps = o.steps || (o.to != null ? [[(o.rollAt ?? (o.at ?? 0) + 0.3), o.to]] : []), cnt = o.count ?? 0.6;
    steps.forEach(([t, v]) => { tl.to(c, { v, duration: cnt, ease: "power2.out", onUpdate: () => { const e = el(); if (e) e.textContent = fmt(c.v); } }, t0 + t);
      tl.fromTo(`#${id}-v`, { scale: 1.3, svgOrigin: `${w - 140} 52` }, { scale: 1, svgOrigin: `${w - 140} 52`, duration: 0.4, ease: "elastic.out(1, 0.4)", immediateRender: false }, t0 + t + cnt); });
    if (o.plus && steps.length) tl.fromTo(`#${id}-pl`, { opacity: 0, scale: 0, svgOrigin: `${w - 86} 52` }, { opacity: 1, scale: 1, svgOrigin: `${w - 86} 52`, duration: 0.35, ease: "back.out(3)" }, t0 + steps[0][0] + cnt);
    idle(tl, `${id}-c`, o.icon, a + 0.8, dur - (o.at ?? 0) - 0.8);
    return id;
  }

  // ---------------- a percent ring: the arc fills as the count moves, the number in the middle ----------------
  function ring(tl, layer, t0, dur, o = {}) {
    const id = nid("jkr"), s = o.s ?? 1, from = o.from ?? 0, g = G(layer), tone = TONE[o.tone || "yellow"];
    put(g, `<g data-ovfix="1" transform="translate(${f1(o.x)},${f1(o.y)}) ${FIX()} scale(${s})" filter="url(#nvDrop)"><g id="${id}"><circle r="70" cy="7" fill="#000" opacity=".28"/><circle r="66" fill="url(#jkiDisc)" ${O4}/><path d="M-50,-34A60,60 0 0 1 28,-54" stroke="#fff" stroke-opacity=".7" stroke-width="5" fill="none" stroke-linecap="round"/>
      <circle r="50" fill="none" stroke="url(#jkiTrack)" stroke-width="13"/><circle r="56" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="2"/>
      <circle id="${id}-arc" r="50" fill="none" stroke="${tone}" stroke-width="13" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="${100 - from}" transform="rotate(-90)"/>
      <g id="${id}-bd" transform="rotate(${f1(from * 3.6 - 90)})"><circle cx="50" r="9" fill="#fff"/><circle cx="50" r="5" fill="${tone}"/></g>
      <g filter="url(#jkiGlyph)">${T(0, 15, 42, `${from}%`, { id: `${id}-v` })}</g>${SPARK(id)}
      ${o.label ? `<g transform="translate(0,104)">${pill(o.label, `${id}-l`, { size: 28 })}</g>` : ""}</g></g>`);
    const a = t0 + (o.at ?? 0), c = { v: from }, up = () => { const e = document.getElementById(`${id}-v`), r = document.getElementById(`${id}-arc`), b = document.getElementById(`${id}-bd`); if (e) e.textContent = `${Math.round(c.v)}%`;
      const vv = Math.max(0, Math.min(100, c.v)); if (r) r.setAttribute("stroke-dashoffset", f1(100 - vv)); if (b) b.setAttribute("transform", `rotate(${f1(vv * 3.6 - 90)})`); };
    enterC(tl, id, a);
    const steps = o.steps || (o.to != null ? [[(o.rollAt ?? (o.at ?? 0) + 0.4), o.to]] : []), cnt = o.count ?? 0.5;
    steps.forEach(([t, v]) => { tl.to(c, { v, duration: cnt, ease: "power2.out", onUpdate: up }, t0 + t);
      tl.fromTo(`#${id}-v`, { scale: 1.3, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "elastic.out(1, 0.4)", immediateRender: false }, t0 + t + cnt); });
    if (o.label) tl.fromTo(`#${id}-l`, { opacity: 0, y: -12 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, t0 + (o.labelAt ?? (o.at ?? 0) + 0.3));
    if (o.flashAt != null) { tl.to(`#${id}`, { scale: 1.18, svgOrigin: "0 0", duration: 0.12, ease: "power2.out" }, t0 + o.flashAt); tl.to(`#${id}`, { scale: 1, svgOrigin: "0 0", duration: 0.5, ease: "elastic.out(1, 0.4)" }, t0 + o.flashAt + 0.12);
      for (let k = 0; k < 6; k++) tl.fromTo(`#${id}-bs${k}`, { opacity: 1, scale: 0.4, svgOrigin: "0 0" }, { opacity: 0, scale: 1.6, svgOrigin: "0 0", duration: 0.6, ease: "power2.out", immediateRender: false }, t0 + o.flashAt + 0.05); }
    return id;
  }

  // ---------------- coins joined by arrows, each entering at its own time ----------------
  function chain(tl, layer, t0, dur, items, o = {}) {
    const id = nid("jkc"), y = (o.y ?? 1500) - (window.LAND ? 250 : 0), gap = o.gap ?? 250, n = items.length, x0 = 540 - ((n - 1) * gap) / 2, s = o.s ?? 0.85, g = G(layer);
    let h = "";
    items.forEach((it, k) => { const x = x0 + k * gap;
      if (k < n - 1) { const a = x + 72 * s, b = x + gap - 74 * s;
        h += `<path id="${id}-a${k}" d="M${f1(a)},${y}H${f1(b)}" stroke="${INK}" stroke-width="14" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/><path id="${id}-b${k}" d="M${f1(a)},${y}H${f1(b)}" stroke="#fff" stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
          <g id="${id}-h${k}" opacity="0" transform="translate(${f1(b)},${y}) ${FIX()} translate(${f1(-b)},${-y})"><path d="M${f1(b - 16)},${y - 14}L${f1(b)},${y}L${f1(b - 16)},${y + 14}" stroke="${INK}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M${f1(b - 16)},${y - 14}L${f1(b)},${y}L${f1(b - 16)},${y + 14}" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`; }
      h += `<g transform="translate(${x},${y}) ${FIX()}">${coin(it.icon, 0, 0, s, `${id}-i${k}`, it.tone || "yellow")}</g><g transform="translate(${x},${y + 92 * s}) ${FIX()}">${pill(it.label, `${id}-l${k}`, { size: o.labelSize ?? 26 })}</g>`; });
    put(g, `<g id="${id}" data-ovfix="1" filter="url(#nvDrop)">${h}</g>`);
    items.forEach((it, k) => { const a = t0 + (o.ats ? o.ats[k] : (o.at ?? 0.1) + k * (o.step ?? 0.42));
      enterC(tl, `${id}-i${k}`, a, { end: t0 + dur }); tl.fromTo(`#${id}-l${k}`, { opacity: 0, scale: 1.8, rotation: -7, svgOrigin: "0 0" }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.32, ease: "back.out(3.2)" }, a + 0.4);
      if (k < n - 1) { const b = o.ats ? t0 + o.ats[k + 1] - 0.35 : a + 0.3; tl.to(`#${id}-a${k}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out" }, b); tl.to(`#${id}-b${k}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.3, ease: "power2.out" }, b); tl.fromTo(`#${id}-h${k}`, { opacity: 0 }, { opacity: 1, duration: 0.08 }, b + 0.28); }
      idle(tl, `${id}-i${k}`, it.icon, a + 0.9, t0 + dur - a - 0.9); hover(tl, `${id}-i${k}`, a + 1.0, t0 + dur - a - 1.0); });
    return id;
  }
  window.JKI = { badge, counter, ring, chain, coin, idle, out, GLY, enterC, hover };
})();
