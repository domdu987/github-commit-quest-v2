// บางระจัน แบต 3% · the story's own coin glyphs in the channel's icon style (paper disc, coloured ring, ink line glyph, every glyph keeps moving).
// Adds kinds to JKI.GLY and wraps JKI.badge / counter / chain so the new kinds get their idle motion too. Load after jkicons.js.
//   kinds: battery (the red bar flashes) · phone (the glint pulses) · lime (a wobble, sparks) · torch (the flame licks) · alarm (the bell swings)
//          msg (the red dot pulses) · buffalo (the tongue wags) · drum (hands beat) · chicken · banana · butterfly (wings flap) · rope (the knot sways) · eye (the pupils dart)
//   BRI.badge / BRI.counter / BRI.chain  = JKI versions + idle for these kinds · BRI.idle(tl, coinId, kind, t0, dur)
(function () {
  const { C, INK, loop } = NkV, G = JKI.GLY;
  const L5 = `fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`;
  const O4 = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  Sets.DEFS += `<radialGradient id="brPhoneGlow"><stop offset="0" stop-color="#cfe8ff" stop-opacity=".95"/><stop offset=".4" stop-color="#8ab8ff" stop-opacity=".45"/><stop offset="1" stop-color="#4a70c0" stop-opacity="0"/></radialGradient>
    <filter id="brBlur" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
    <radialGradient id="brRedGlow"><stop offset="0" stop-color="#ff6a5a" stop-opacity=".8"/><stop offset="1" stop-color="#ff3a2a" stop-opacity="0"/></radialGradient>`;
  Object.assign(G, {
    battery: (id) => `<g id="${id}-bt"><rect x="-28" y="-15" width="50" height="30" rx="6" fill="${C.paper}" ${L5}/><rect x="22" y="-7" width="7" height="14" rx="2" fill="${INK}"/><rect id="${id}-lv" x="-22" y="-9" width="8" height="18" rx="2" fill="${C.red}"/>
      <path d="M-8,-9v18M4,-9v18" stroke="${INK}" stroke-width="2" opacity=".35"/></g><g id="${id}-zz"><path d="M22,-34l-9,15h12l-9,15" stroke="${C.yellow}" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
    phone: (id) => `<g id="${id}-ph"><rect x="-19" y="-32" width="38" height="64" rx="7" fill="${C.paper}" ${L5}/><rect x="-14" y="-24" width="28" height="42" rx="3" fill="${C.blue}" opacity=".85"/><path d="M-5,26h10" ${L5}/></g>
      <g id="${id}-gl"><path d="M-26,-34l-4,-11M-30,-27l-10,-4M-24,-40l6,-9" stroke="${C.yellow}" stroke-width="4" stroke-linecap="round"/></g>`,
    lime: (id) => `<g id="${id}-lm"><rect x="-3" y="-42" width="6" height="24" fill="#9aa0a6" stroke="${INK}" stroke-width="2.5"/><rect x="-7" y="-44" width="14" height="5" fill="#6a7078" stroke="${INK}" stroke-width="2"/>
      <circle r="22" fill="${C.green}" ${O4}/><circle cx="-7" cy="-7" r="7" fill="#fff" opacity=".35"/><path d="M-10,8q10,8 20,0" stroke="${INK}" stroke-width="2.5" fill="none" opacity=".5"/></g>
      <g id="${id}-sp"><path d="M20,-34l3,-6M26,-28l6,-2M14,-38l-1,-7" stroke="${C.yellow}" stroke-width="3.5" stroke-linecap="round"/></g>`,
    torch: (id) => `<rect x="-5" y="-6" width="10" height="40" rx="3" fill="#8a5a32" ${O4}/><path d="M-10,-6h20l-3,-8h-14z" fill="#b08048" ${O4}/>
      <g id="${id}-fl"><path d="M0,-12Q-18,-30 -5,-50Q0,-34 7,-44Q20,-24 0,-12Z" fill="${C.yellow}" ${O4}/><path d="M0,-16Q-7,-26 -2,-36Q2,-27 5,-31Q10,-20 0,-16Z" fill="${C.red}"/></g>`,
    alarm: (id) => `<g id="${id}-bl"><path d="M-21,12Q-23,-24 0,-27Q23,-24 21,12Z" fill="${C.yellow}" ${O4}/><path d="M-28,12H28" ${L5}/><circle cy="21" r="5.5" fill="${INK}"/><path d="M0,-27v-7" ${L5}/><path d="M-10,-14q-4,10 -3,20" stroke="#fff" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/></g>
      <g id="${id}-wv"><path d="M-32,-16q-9,11 0,22M32,-16q9,11 0,22" ${L5}/></g>`,
    msg: (id) => `<g id="${id}-ms"><path d="M-30,-24h60v36h-32l-12,11v-11h-16z" fill="${C.paper}" ${L5}/><path d="M-18,-12h36M-18,-2h22" ${L5}/></g><g id="${id}-dt"><circle cx="26" cy="-26" r="9" fill="${C.red}" ${O4}/></g>`,
    buffalo: (id) => `<g id="${id}-bh"><path d="M-22,-16Q-50,-36 -40,-58Q-26,-46 -14,-26Z" fill="${C.paper}" ${L5}/><path d="M22,-16Q50,-36 40,-58Q26,-46 14,-26Z" fill="${C.paper}" ${L5}/>
      <path d="M-20,-24Q0,-32 20,-24Q31,0 21,22Q0,31 -21,22Q-31,0 -20,-24Z" fill="#3a3430" ${O4}/><circle cx="-9" cy="-5" r="4" fill="#fff"/><circle cx="9" cy="-5" r="4" fill="#fff"/><circle cx="-8" cy="-5" r="1.8" fill="${INK}"/><circle cx="10" cy="-5" r="1.8" fill="${INK}"/>
      <circle cx="-6" cy="14" r="2.6" fill="${INK}"/><circle cx="6" cy="14" r="2.6" fill="${INK}"/><g id="${id}-tg"><path d="M-7,24q7,16 14,0Z" fill="${C.red}" ${O4}/></g></g>`,
    drum: (id) => `<g id="${id}-dr"><path d="M-15,-30H15L11,30H-11Z" fill="#a8743a" ${O4}/><ellipse cy="-30" rx="15" ry="5.5" fill="${C.paper}" ${O4}/><path d="M-13,-10h26M-12,8h24" stroke="${INK}" stroke-width="2" opacity=".4"/></g>
      <g id="${id}-hd"><path d="M-32,-44q10,8 12,10M32,-44q-10,8 -12,10" ${L5}/><circle cx="-33" cy="-46" r="5" fill="${C.paper}" ${O4}/><circle cx="33" cy="-46" r="5" fill="${C.paper}" ${O4}/></g>`,
    chicken: (id) => `<g id="${id}-ck"><path d="M-6,8L-22,34" stroke="${C.paper}" stroke-width="8" stroke-linecap="round"/><path d="M-6,8L-22,34" ${L5}/><path d="M-16,-4Q-24,-32 0,-34Q24,-32 16,-4Q8,10 -16,-4Z" fill="#d8863a" ${O4}/><path d="M-10,-14q6,-10 14,-8" stroke="#fff" stroke-width="3" fill="none" opacity=".5" stroke-linecap="round"/></g>`,
    banana: (id) => `<g id="${id}-bn">${[0, 1, 2].map((k) => `<path d="M${-20 + k * 13},16Q${-16 + k * 13},-18 ${-2 + k * 13},-34" stroke="${C.yellow}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M${-20 + k * 13},16Q${-16 + k * 13},-18 ${-2 + k * 13},-34" stroke="${INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`).join("")}<path d="M-24,-34Q-6,-44 14,-36" stroke="#6a5a2a" stroke-width="8" stroke-linecap="round" fill="none"/></g>`,
    butterfly: (id) => `<g id="${id}-wL"><path d="M-2,0Q-34,-36 -38,-8Q-34,10 -14,4Q-34,22 -16,32Q-4,32 -2,8Z" fill="${C.blue}" ${O4}/><circle cx="-22" cy="-12" r="4" fill="#fff" opacity=".6"/></g>
      <g id="${id}-wR"><path d="M2,0Q34,-36 38,-8Q34,10 14,4Q34,22 16,32Q4,32 2,8Z" fill="${C.blue}" ${O4}/><circle cx="22" cy="-12" r="4" fill="#fff" opacity=".6"/></g><path d="M0,-14V24" ${L5}/><path d="M0,-14l-8,-13M0,-14l8,-13" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>`,
    rope: (id) => `<g id="${id}-rp"><path d="M-32,-12Q-12,-32 0,-12T32,8" stroke="#c8a860" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M-32,-12Q-12,-32 0,-12T32,8" ${L5}/>
      <circle r="13" fill="#c8a860" ${O4}/><path d="M-8,-2q8,-7 16,2M-6,4q6,5 12,0" stroke="${INK}" stroke-width="2.5" fill="none"/></g>`,
    eye: (id) => `<g id="${id}-ey"><path d="M-38,0Q-20,-18 -2,0Q-20,18 -38,0Z" fill="#fff" ${L5}/><path d="M2,0Q20,-18 38,0Q20,18 2,0Z" fill="#fff" ${L5}/><circle id="${id}-p1" cx="-20" r="6.5" fill="${INK}"/><circle id="${id}-p2" cx="20" r="6.5" fill="${INK}"/></g>`,
  });
  function idle(tl, id, kind, t0, dur) {
    const q = (s) => `#${id}-${s}`;
    if (!document.querySelector(`#${id}`) || dur <= 0.2) return;
    if (kind === "battery") { loop(tl, q("lv"), { opacity: 1 }, { opacity: 0.15 }, 0.45, t0, dur); loop(tl, q("zz"), { opacity: 1, y: 0 }, { opacity: 0.3, y: -3 }, 0.45, t0, dur); }
    if (kind === "phone") loop(tl, q("gl"), { opacity: 0.2, scale: 0.8, svgOrigin: "-24 -32" }, { opacity: 1, scale: 1.1, svgOrigin: "-24 -32" }, 0.6, t0, dur);
    if (kind === "lime") { loop(tl, q("lm"), { rotation: -6, svgOrigin: "0 0" }, { rotation: 6, svgOrigin: "0 0" }, 0.9, t0, dur); loop(tl, q("sp"), { opacity: 0.1 }, { opacity: 1 }, 0.3, t0, dur); }
    if (kind === "torch") loop(tl, q("fl"), { scaleY: 0.82, scaleX: 1.06, svgOrigin: "0 -10" }, { scaleY: 1.12, scaleX: 0.94, svgOrigin: "0 -10" }, 0.28, t0, dur);
    if (kind === "alarm") { loop(tl, q("bl"), { rotation: -16, svgOrigin: "0 -32" }, { rotation: 16, svgOrigin: "0 -32" }, 0.22, t0, dur); loop(tl, q("wv"), { opacity: 0.2, scale: 0.9, svgOrigin: "0 -5" }, { opacity: 1, scale: 1.1, svgOrigin: "0 -5" }, 0.22, t0, dur); }
    if (kind === "msg") loop(tl, q("dt"), { scale: 0.8, svgOrigin: "26 -26" }, { scale: 1.3, svgOrigin: "26 -26" }, 0.5, t0, dur);
    if (kind === "buffalo") { loop(tl, q("tg"), { scaleY: 0.5, svgOrigin: "0 24" }, { scaleY: 1.3, svgOrigin: "0 24" }, 0.35, t0, dur); loop(tl, q("bh"), { rotation: -4, svgOrigin: "0 0" }, { rotation: 4, svgOrigin: "0 0" }, 0.7, t0, dur); }
    if (kind === "drum") { loop(tl, q("hd"), { y: -4 }, { y: 5 }, 0.22, t0, dur); loop(tl, q("dr"), { rotation: -4, svgOrigin: "0 0" }, { rotation: 4, svgOrigin: "0 0" }, 0.44, t0, dur); }
    if (kind === "chicken") loop(tl, q("ck"), { rotation: -10, svgOrigin: "-14 20" }, { rotation: 10, svgOrigin: "-14 20" }, 0.8, t0, dur);
    if (kind === "banana") loop(tl, q("bn"), { rotation: -6, svgOrigin: "0 -30" }, { rotation: 6, svgOrigin: "0 -30" }, 1.0, t0, dur);
    if (kind === "butterfly") { loop(tl, q("wL"), { scaleX: 1, svgOrigin: "0 0" }, { scaleX: 0.35, svgOrigin: "0 0" }, 0.26, t0, dur); loop(tl, q("wR"), { scaleX: 1, svgOrigin: "0 0" }, { scaleX: 0.35, svgOrigin: "0 0" }, 0.26, t0, dur); }
    if (kind === "rope") loop(tl, q("rp"), { rotation: -6, svgOrigin: "0 -30" }, { rotation: 6, svgOrigin: "0 -30" }, 1.1, t0, dur);
    if (kind === "eye") { loop(tl, q("p1"), { x: -4 }, { x: 4 }, 1.1, t0, dur); loop(tl, q("p2"), { x: -4 }, { x: 4 }, 1.1, t0, dur); }
  }
  const MINE = new Set(["battery", "phone", "lime", "torch", "alarm", "msg", "buffalo", "drum", "chicken", "banana", "butterfly", "rope", "eye"]);
  const badge = (tl, layer, t0, dur, o) => { const id = JKI.badge(tl, layer, t0, dur, o); const a = t0 + (o.at ?? 0), end = o.end != null ? t0 + o.end : t0 + dur; if (MINE.has(o.kind)) idle(tl, `${id}-c`, o.kind, a + 0.95, end - a - 0.95); return id; };
  const counter = (tl, layer, t0, dur, o = {}) => { const id = JKI.counter(tl, layer, t0, dur, o); const a = t0 + (o.at ?? 0); if (MINE.has(o.icon)) idle(tl, `${id}-c`, o.icon, a + 0.8, dur - (o.at ?? 0) - 0.8); return id; };
  const chain = (tl, layer, t0, dur, items, o = {}) => { const id = JKI.chain(tl, layer, t0, dur, items, o);
    items.forEach((it, k) => { const a = t0 + (o.ats ? o.ats[k] : (o.at ?? 0.1) + k * (o.step ?? 0.42)); if (MINE.has(it.icon)) idle(tl, `${id}-i${k}`, it.icon, a + 0.9, t0 + dur - a - 0.9); }); return id; };
  window.BRI = { badge, counter, chain, idle, MINE };
})();
