// ช่างเชื่อมสายฟ้า · coin glyphs for this story (paper disc, ink line, every glyph keeps moving). Load after bricons.js.
//   kinds: bolt · hairup · batt100 · baht · gate · banana · baby · transformer · tree · fusebox · mask · bike · bulb
(function () {
  const { C, INK, loop } = NkV, G = JKI.GLY;
  const L5 = `fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`;
  const O4 = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  Sets.DEFS += `<radialGradient id="ltBlue"><stop offset="0" stop-color="#dff4ff" stop-opacity=".95"/><stop offset=".4" stop-color="#8ac8ff" stop-opacity=".45"/><stop offset="1" stop-color="#3a70d0" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltWarm"><stop offset="0" stop-color="#fff2c0" stop-opacity=".95"/><stop offset=".5" stop-color="#ffd070" stop-opacity=".35"/><stop offset="1" stop-color="#ff9a30" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltAura"><stop offset="0" stop-color="#bfe8ff" stop-opacity=".5"/><stop offset=".5" stop-color="#6aa8ff" stop-opacity=".18"/><stop offset="1" stop-color="#3a70d0" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltArcG"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#bfe8ff" stop-opacity=".8"/><stop offset="1" stop-color="#60a0ff" stop-opacity="0"/></radialGradient>`;
  Object.assign(G, {
    bolt: (id) => `<g id="${id}-bt"><path d="M6,-36L-20,2H0L-6,36L22,-6H2Z" fill="${C.yellow}" ${O4}/></g><g id="${id}-gl"><path d="M-30,-30l-6,-6M30,-30l6,-6M-34,20l-7,2M34,20l7,2" stroke="${C.yellowD}" stroke-width="4" stroke-linecap="round"/></g>`,
    hairup: (id) => `<circle cy="8" r="22" ${L5}/><path d="M-8,4v3M8,4v3" ${L5}/><path d="M-7,18q7,5 14,0" ${L5}/><g id="${id}-hr"><path d="M-18,-10L-26,-40L-10,-22L-4,-46L4,-22L12,-46L18,-22L28,-40L20,-10Z" fill="${INK}"/></g>
      <g id="${id}-sp"><path d="M-34,-30l6,-6l-4,-6M34,-30l-6,-6l4,-6" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round" fill="none"/></g>`,
    batt100: (id) => `<g id="${id}-bt"><rect x="-28" y="-15" width="50" height="30" rx="6" fill="${C.paper}" ${L5}/><rect x="22" y="-7" width="7" height="14" rx="2" fill="${INK}"/><rect id="${id}-lv" x="-22" y="-9" width="38" height="18" rx="2" fill="${C.green}"/><path d="M-6,-4l4,6l8,-10" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>
      <g id="${id}-zz"><path d="M22,-34l-9,15h12l-9,15" stroke="${C.yellow}" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    baht: (id) => `<g id="${id}-cn"><circle r="30" fill="${C.yellow}" ${O4}/><circle r="22" fill="none" stroke="${C.yellowD}" stroke-width="2.5"/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="${INK}">฿</text></g>`,
    gate: (id) => `<g id="${id}-gt"><rect x="-30" y="-30" width="60" height="60" fill="${C.paper}" ${L5}/><path d="M-15,-30V30M0,-30V30M15,-30V30M-30,0H30" ${L5}/><path d="M-8,-18q8,8 0,16q-8,-8 0,-16" stroke="${INK}" stroke-width="2.5" fill="none"/></g><g id="${id}-sp"><path d="M22,-40l5,-6l-3,-7M30,-30l7,-2" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round" fill="none"/></g>`,
    banana: (id) => `<g id="${id}-bn">${[0, 1, 2].map((k) => `<path d="M${-20 + k * 13},16Q${-16 + k * 13},-18 ${-2 + k * 13},-34" stroke="${C.yellow}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M${-20 + k * 13},16Q${-16 + k * 13},-18 ${-2 + k * 13},-34" stroke="${INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`).join("")}<path d="M-24,-34Q-6,-44 14,-36" stroke="#6a5a2a" stroke-width="8" stroke-linecap="round" fill="none"/></g>`,
    baby: (id) => `<g id="${id}-bx"><path d="M-30,10V-16Q-30,-30 -16,-30H16Q30,-30 30,-16V10Z" fill="#cfe8f8" ${L5}/><rect x="-32" y="10" width="64" height="12" rx="3" fill="${C.paper}" ${L5}/></g><g id="${id}-bb"><ellipse cy="-2" rx="16" ry="8" fill="#ffd8c0" ${O4}/><circle cx="-13" cy="-6" r="7" fill="#f8c8a8" ${O4}/></g><g id="${id}-lp"><path d="M-12,-40h24" stroke="${C.yellow}" stroke-width="5" stroke-linecap="round"/></g>`,
    transformer: (id) => `<path d="M0,36V-40" ${L5}/><path d="M-26,-30H26" ${L5}/><g id="${id}-bx"><rect x="-16" y="-28" width="32" height="30" rx="3" fill="#8a8f98" ${O4}/><path d="M-10,-20h20M-10,-12h20" stroke="${INK}" stroke-width="2"/></g><g id="${id}-sp"><path d="M18,-40l6,-8l-4,-6l8,-6M-20,-42l-6,-6l4,-8" stroke="${C.yellow}" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>`,
    tree: (id) => `<path d="M-4,34Q-6,10 0,-10" stroke="#6a9a3a" stroke-width="8" stroke-linecap="round"/><g id="${id}-lv">${[-150, -100, -40, 20, 80, 140].map((a) => `<path d="M0,-10q${Math.cos(a * Math.PI / 180) * 14},${Math.sin(a * Math.PI / 180) * 10 - 6} ${Math.cos(a * Math.PI / 180) * 34},${Math.sin(a * Math.PI / 180) * 24 + 4}" stroke="${C.green}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}</g><g id="${id}-gd"><path d="M-30,34h60" ${L5}/><path d="M-4,34v8M4,34v8" stroke="${C.yellow}" stroke-width="3"/></g>`,
    fusebox: (id) => `<g id="${id}-fb"><rect x="-24" y="-32" width="48" height="64" rx="4" fill="#8a8f98" ${L5}/><rect x="-14" y="-22" width="28" height="12" rx="2" fill="#2a2a30"/><rect x="-14" y="-4" width="28" height="12" rx="2" fill="#2a2a30"/><rect x="-10" y="-20" width="8" height="8" fill="${C.red}"/><rect x="2" y="-2" width="8" height="8" fill="${C.green}"/></g><g id="${id}-ld"><path d="M24,-32L40,-24V24L24,32" fill="${C.paper}" ${L5}/></g>`,
    mask: (id) => `<g id="${id}-mk"><path d="M-26,-30Q-30,30 0,34Q30,30 26,-30Q0,-40 -26,-30Z" fill="#2a2e34" ${L5}/><rect x="-16" y="-10" width="32" height="12" rx="3" fill="${C.green}"/></g><g id="${id}-sp"><path d="M-36,22l-8,4M36,22l8,4M0,44v8" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round"/></g>`,
    bike: (id) => `<g id="${id}-bk"><circle cx="-20" cy="14" r="12" ${L5}/><circle cx="22" cy="14" r="12" ${L5}/><path d="M-20,14L-4,-6H14L22,14M-4,-6L-10,-16H2" ${L5}/><path d="M-14,-8Q0,-22 18,-16" stroke="${C.red}" stroke-width="7" stroke-linecap="round" fill="none"/></g><g id="${id}-pf"><circle cx="34" cy="-4" r="4" fill="${C.yellow}"/></g>`,
    bulb: (id) => `<g id="${id}-bl"><path d="M-18,-6Q-18,-34 0,-34Q18,-34 18,-6Q18,6 8,12V22H-8V12Q-18,6 -18,-6Z" fill="${C.yellow}" ${L5}/><path d="M-8,28h16" ${L5}/></g><g id="${id}-ry">${[-40, -20, 0, 20, 40].map((a) => `<path d="M0,-40v-10" stroke="${C.yellowD}" stroke-width="4" stroke-linecap="round" transform="rotate(${a})"/>`).join("")}</g>`,
  });
  function idle(tl, id, kind, t0, dur) {
    const q = (s) => `#${id}-${s}`;
    if (!document.querySelector(`#${id}`) || dur <= 0.2) return;
    if (kind === "bolt") { loop(tl, q("bt"), { scale: 1, svgOrigin: "0 0" }, { scale: 1.14, svgOrigin: "0 0" }, 0.3, t0, dur); loop(tl, q("gl"), { opacity: 0.2 }, { opacity: 1 }, 0.3, t0, dur); }
    if (kind === "hairup") { loop(tl, q("hr"), { scaleY: 0.9, svgOrigin: "0 -10" }, { scaleY: 1.12, svgOrigin: "0 -10" }, 0.4, t0, dur); loop(tl, q("sp"), { opacity: 0.1 }, { opacity: 1 }, 0.25, t0, dur); }
    if (kind === "batt100") { loop(tl, q("zz"), { opacity: 1, y: 0 }, { opacity: 0.3, y: -3 }, 0.45, t0, dur); }
    if (kind === "baht") loop(tl, q("cn"), { rotation: -8, svgOrigin: "0 0" }, { rotation: 8, svgOrigin: "0 0" }, 0.8, t0, dur);
    if (kind === "gate") loop(tl, q("sp"), { opacity: 0.1 }, { opacity: 1 }, 0.3, t0, dur);
    if (kind === "banana") loop(tl, q("bn"), { rotation: -6, svgOrigin: "0 -30" }, { rotation: 6, svgOrigin: "0 -30" }, 1.0, t0, dur);
    if (kind === "baby") { loop(tl, q("lp"), { opacity: 0.3 }, { opacity: 1 }, 0.7, t0, dur); loop(tl, q("bb"), { y: 0 }, { y: -2 }, 1.3, t0, dur); }
    if (kind === "transformer") loop(tl, q("sp"), { opacity: 0.1, scale: 0.8, svgOrigin: "0 -40" }, { opacity: 1, scale: 1.15, svgOrigin: "0 -40" }, 0.2, t0, dur);
    if (kind === "tree") { loop(tl, q("lv"), { rotation: -4, svgOrigin: "0 -10" }, { rotation: 4, svgOrigin: "0 -10" }, 1.4, t0, dur); loop(tl, q("gd"), { opacity: 0.4 }, { opacity: 1 }, 0.5, t0, dur); }
    if (kind === "fusebox") loop(tl, q("ld"), { scaleX: 1, svgOrigin: "24 0" }, { scaleX: 0.4, svgOrigin: "24 0" }, 0.9, t0, dur);
    if (kind === "mask") loop(tl, q("sp"), { opacity: 0.1 }, { opacity: 1 }, 0.25, t0, dur);
    if (kind === "bike") { loop(tl, q("bk"), { y: 0 }, { y: -3 }, 0.3, t0, dur); loop(tl, q("pf"), { opacity: 0.2, x: 0 }, { opacity: 1, x: 6 }, 0.5, t0, dur); }
    if (kind === "bulb") { loop(tl, q("ry"), { opacity: 0.2, scale: 0.9, svgOrigin: "0 -10" }, { opacity: 1, scale: 1.1, svgOrigin: "0 -10" }, 0.6, t0, dur); }
  }
  const MINE = new Set(["bolt", "hairup", "batt100", "baht", "gate", "banana", "baby", "transformer", "tree", "fusebox", "mask", "bike", "bulb"]);
  const badge = (tl, layer, t0, dur, o) => { const id = JKI.badge(tl, layer, t0, dur, o); const a = t0 + (o.at ?? 0), end = o.end != null ? t0 + o.end : t0 + dur; if (MINE.has(o.kind)) idle(tl, `${id}-c`, o.kind, a + 0.95, end - a - 0.95); else if (BRI.MINE.has(o.kind)) BRI.idle(tl, `${id}-c`, o.kind, a + 0.95, end - a - 0.95); return id; };
  const counter = (tl, layer, t0, dur, o = {}) => { const id = JKI.counter(tl, layer, t0, dur, o); const a = t0 + (o.at ?? 0); if (MINE.has(o.icon)) idle(tl, `${id}-c`, o.icon, a + 0.8, dur - (o.at ?? 0) - 0.8); return id; };
  const chain = (tl, layer, t0, dur, items, o = {}) => { const id = JKI.chain(tl, layer, t0, dur, items, o);
    items.forEach((it, k) => { const a = t0 + (o.ats ? o.ats[k] : (o.at ?? 0.1) + k * (o.step ?? 0.42)); if (MINE.has(it.icon)) idle(tl, `${id}-i${k}`, it.icon, a + 0.9, t0 + dur - a - 0.9); }); return id; };
  window.LTI = { badge, counter, chain, idle, MINE };
})();
