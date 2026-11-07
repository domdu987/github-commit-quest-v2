// คนเดินดิน · coin glyphs for this story (paper disc, ink line, every glyph keeps moving). Load after lticons.js.
//   kinds: ring · zero · stairs · scope · graph · days7 · dog · captain · nofeet · tea
(function () {
  const { C, INK, loop } = NkV, G = JKI.GLY;
  const L5 = `fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`;
  const O4 = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  Object.assign(G, {
    ring: (id) => `<g id="${id}-rg"><circle r="26" fill="none" stroke="${C.yellow}" stroke-width="10"/><circle r="26" fill="none" stroke="${INK}" stroke-width="2.5"/><circle r="16" fill="none" stroke="${INK}" stroke-width="2.5"/></g><g id="${id}-ry">${[-60, 0, 60].map((a) => `<path d="M0,-34v-10" stroke="${C.yellowD}" stroke-width="4" stroke-linecap="round" transform="rotate(${a})"/>`).join("")}</g>`,
    zero: (id) => `<g id="${id}-mt"><path d="M-30,16A30,30 0 0,1 30,16" ${L5}/><path d="M-30,16H30" ${L5}/><g id="${id}-nd"><path d="M0,16L-18,-6" stroke="${C.red}" stroke-width="5" stroke-linecap="round"/></g><circle cy="16" r="5" fill="${INK}"/></g><text y="42" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${C.red}">0%</text>`,
    stairs: (id) => `<g id="${id}-st"><path d="M-32,30H-16V14H0V-2H16V-18H32V-34" ${L5}/><path d="M-32,30V14M-16,14V-2M0,-2V-18M16,-18V-34" stroke="${INK}" stroke-width="2.5"/></g><g id="${id}-sp"><path d="M20,-40l6,-6M30,-30l7,-2" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round"/></g>`,
    scope: (id) => `<g id="${id}-sc"><g transform="rotate(-35)"><rect x="-10" y="-34" width="20" height="56" rx="6" fill="${C.paper}" ${L5}/><rect x="-14" y="-40" width="28" height="12" rx="4" fill="${INK}"/></g><path d="M-6,22L-22,40M6,22L22,40M0,22V40" ${L5}/></g><g id="${id}-tw"><circle cx="28" cy="-30" r="4" fill="${C.yellow}"/><circle cx="36" cy="-16" r="2.5" fill="${C.yellow}"/></g>`,
    graph: (id) => `<g id="${id}-gr"><path d="M-30,30V-30M-30,30H30" ${L5}/><path id="${id}-ln" d="M-24,-14L-8,-10L4,0L14,14L28,26" stroke="${C.red}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g><g id="${id}-ar"><path d="M20,10l8,16l-16,-2" stroke="${C.red}" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>`,
    days7: (id) => `<g id="${id}-cl"><rect x="-28" y="-26" width="56" height="54" rx="6" fill="${C.paper}" ${L5}/><rect x="-28" y="-26" width="56" height="14" fill="${C.red}"/><text y="18" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}">7</text></g><g id="${id}-tk"><path d="M-36,-30l-6,-4M36,-30l6,-4" stroke="${C.red}" stroke-width="3.5" stroke-linecap="round"/></g>`,
    dog: (id) => `<g id="${id}-dg"><ellipse cy="8" rx="26" ry="14" fill="${C.yellow}" ${O4}/><circle cx="24" cy="-6" r="13" fill="${C.yellow}" ${O4}/><path d="M14,-16q-6,-14 2,-14M30,-16q6,-14 -2,-14" stroke="${INK}" stroke-width="3" fill="none"/><circle cx="30" cy="-6" r="2.5" fill="${INK}"/><path d="M-26,0q-14,-12 -8,-24" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round" id="${id}-tl"/></g><g id="${id}-bk"><path d="M42,-14l8,-4M44,-4l10,0" stroke="${INK}" stroke-width="3" stroke-linecap="round"/></g>`,
    captain: (id) => `<g id="${id}-cp"><path d="M-22,-10Q-22,-34 0,-34Q22,-34 22,-10Z" fill="${C.yellow}" ${O4}/><path d="M-20,-10H20V0H-20Z" fill="${INK}"/><path d="M-26,6H26L22,34H-22Z" fill="${C.yellow}" ${O4}/><circle cy="18" r="7" fill="${C.red}"/></g><g id="${id}-sh"><path d="M-40,-20l-6,-6M40,-20l6,-6M0,-44v-8" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round"/></g>`,
    nofeet: (id) => `<g id="${id}-ft"><path d="M-14,-30V-4Q-14,6 -4,6H14" ${L5}/><path d="M8,-30V-4Q8,6 18,6H34" ${L5}/></g><path d="M-34,28H40" stroke="${INK}" stroke-width="4" stroke-linecap="round"/><g id="${id}-gp"><path d="M-14,18l6,-6M4,18l6,-6M22,18l6,-6" stroke="${C.red}" stroke-width="3.5" stroke-linecap="round"/></g>`,
    tea: (id) => `<g id="${id}-cu"><path d="M-18,-24H18L14,30H-14Z" fill="${C.paper}" ${L5}/><path d="M-14,4H14L13,30H-13Z" fill="#8a6a4a"/>${[-6, 2].map((x) => `<circle cx="${x}" cy="22" r="3" fill="${INK}"/>`).join("")}<path d="M6,-24V-42" stroke="${C.red}" stroke-width="5" stroke-linecap="round"/></g>`,
  });
  function idle(tl, id, kind, t0, dur) {
    const q = (s) => `#${id}-${s}`;
    if (!document.querySelector(`#${id}`) || dur <= 0.2) return;
    if (kind === "ring") { loop(tl, q("rg"), { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, svgOrigin: "0 0" }, 2.4, t0, dur, "none"); loop(tl, q("ry"), { opacity: 0.2 }, { opacity: 1 }, 0.5, t0, dur); }
    if (kind === "zero") loop(tl, q("nd"), { rotation: -4, svgOrigin: "0 16" }, { rotation: 6, svgOrigin: "0 16" }, 0.35, t0, dur);
    if (kind === "stairs") { loop(tl, q("st"), { y: 0 }, { y: -3 }, 0.6, t0, dur); loop(tl, q("sp"), { opacity: 0.1 }, { opacity: 1 }, 0.3, t0, dur); }
    if (kind === "scope") { loop(tl, q("sc"), { rotation: -3, svgOrigin: "0 22" }, { rotation: 3, svgOrigin: "0 22" }, 1.2, t0, dur); loop(tl, q("tw"), { opacity: 0.2 }, { opacity: 1 }, 0.5, t0, dur); }
    if (kind === "graph") { loop(tl, q("ar"), { y: 0, opacity: 1 }, { y: 4, opacity: 0.4 }, 0.5, t0, dur); }
    if (kind === "days7") { loop(tl, q("tk"), { opacity: 0.2 }, { opacity: 1 }, 0.5, t0, dur); loop(tl, q("cl"), { rotation: -3, svgOrigin: "0 0" }, { rotation: 3, svgOrigin: "0 0" }, 0.5, t0, dur); }
    if (kind === "dog") { loop(tl, q("tl"), { rotation: -14, svgOrigin: "-26 0" }, { rotation: 14, svgOrigin: "-26 0" }, 0.22, t0, dur); loop(tl, q("bk"), { opacity: 0.1, x: 0 }, { opacity: 1, x: 3 }, 0.3, t0, dur); }
    if (kind === "captain") loop(tl, q("sh"), { opacity: 0.2, scale: 0.9, svgOrigin: "0 0" }, { opacity: 1, scale: 1.1, svgOrigin: "0 0" }, 0.6, t0, dur);
    if (kind === "nofeet") { loop(tl, q("ft"), { y: 0 }, { y: -4 }, 0.8, t0, dur); loop(tl, q("gp"), { opacity: 0.2 }, { opacity: 1 }, 0.4, t0, dur); }
    if (kind === "tea") loop(tl, q("cu"), { rotation: -5, svgOrigin: "0 30" }, { rotation: 5, svgOrigin: "0 30" }, 0.7, t0, dur);
  }
  const MINE = new Set(["ring", "zero", "stairs", "scope", "graph", "days7", "dog", "captain", "nofeet", "tea"]);
  const badge = (tl, layer, t0, dur, o) => { const id = JKI.badge(tl, layer, t0, dur, o); const a = t0 + (o.at ?? 0), end = o.end != null ? t0 + o.end : t0 + dur; if (MINE.has(o.kind)) idle(tl, `${id}-c`, o.kind, a + 0.95, end - a - 0.95); else return LTI.badge ? id : id; return id; };
  const counter = (tl, layer, t0, dur, o = {}) => { const id = JKI.counter(tl, layer, t0, dur, o); const a = t0 + (o.at ?? 0); if (MINE.has(o.icon)) idle(tl, `${id}-c`, o.icon, a + 0.8, dur - (o.at ?? 0) - 0.8); return id; };
  const chain = (tl, layer, t0, dur, items, o = {}) => { const id = JKI.chain(tl, layer, t0, dur, items, o);
    items.forEach((it, k) => { const a = t0 + (o.ats ? o.ats[k] : (o.at ?? 0.1) + k * (o.step ?? 0.42)); if (MINE.has(it.icon)) idle(tl, `${id}-i${k}`, it.icon, a + 0.9, t0 + dur - a - 0.9); }); return id; };
  window.FLI = { badge, counter, chain, idle, MINE };
})();
