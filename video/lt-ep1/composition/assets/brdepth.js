// บางระจัน แบต 3% · depth dressing for the story's sets (light cones, contact shadows, haze, motes, flames). Load after jkdepth.js and brset.js.
(function () {
  const { dress, ao, band, cone, cast, motes, breathe, birds, smoke } = JKD;
  const G = (layer) => { const g = document.createElementNS("http://www.w3.org/2000/svg", "g"); layer.appendChild(g); return g; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const flicker = (tl, sh, sel, lo = 0.72, hi = 1, p = 0.16) => { const els = document.querySelectorAll(sel); els.forEach((el, k) => tl.fromTo(el, { opacity: hi, scaleY: 1, svgOrigin: "0 0" }, { opacity: lo, scaleY: 0.86, svgOrigin: "0 0", duration: p + k * 0.013, repeat: Math.ceil(sh.dur / p), yoyo: true, ease: "sine.inOut" }, Math.max(0, sh.start))); };
  dress.brField = (L, tl, sh, id, o) => {
    put(L.set, `${band(1330, 60, 0.5)}${ao(300, 1402, 160, 16, 0.25)}${ao(1300, 1402, 150, 14, 0.25)}`);
    motes(L.glow, tl, sh, { n: 12, color: "#fff6c8", x: -300, y: 900, w: 1700, h: 500, seed: 3 });
    birds(L.far, tl, sh, 400, 700, 4, "#4a4a5a");
  };
  dress.brCamp = (L, tl, sh, id, o) => {
    put(L.set, `${band(1180, 70, 0.6)}${ao(1600, 1404, 190, 18, 0.3)}${ao(330, 1404, 130, 14, 0.25)}${ao(520, 1404, 50, 9, 0.25)}${ao(760, 1404, 40, 9, 0.3)}${cast(1450, 300, 1000, 400, 120, 0.12, 14)}`);
    if (o.night) {
      put(L.glow, `<g style="mix-blend-mode:screen">${o.torches ? `${cone(60, 1100, 60, 500, 0.9, "jkdCone")}${cone(1300, 1100, 60, 500, 0.9, "jkdCone")}` : ""}</g>`);
      motes(L.glow, tl, sh, { n: 10, color: "#d8ff80", x: -300, y: 900, w: 1700, h: 600, seed: 9, r: 3.5 });
      flicker(tl, sh, `#${id}-light .brFlame, #${id}-set .brFlame, #${id}-far .brFlame`);
      if (o.enemy) tl.fromTo(`#${o.id || "brc"}-enemy`, { x: 0 }, { x: -40, duration: 2.2, repeat: Math.ceil(sh.dur / 2.2), yoyo: true, ease: "sine.inOut" }, Math.max(0, sh.start));
    } else {
      motes(L.glow, tl, sh, { n: 14, color: "#fff6c8", x: -300, y: 700, w: 1700, h: 700, seed: 7 });
      birds(L.far, tl, sh, 1500, 600, 3, "#3a3a4a");
    }
    smoke(L.glow, tl, sh, 330, 1200, 5);
    breathe(tl, document.querySelectorAll(`#${id}-set .brFire`), sh, 0.75, 1, 0.5);
  };
  dress.brRoom = (L, tl, sh, id, o) => {
    put(L.set, `${band(1200, 40, 0.5)}${o.kitchen ? ao(900, 1404, 220, 18, 0.28) : ao(650, 1404, 360, 20, 0.3)}`);
    motes(L.glow, tl, sh, { n: 10, color: "#fff6c8", x: 0, y: 500, w: 1200, h: 900, seed: 5 });
  };
})();
