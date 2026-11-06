// ช่างเชื่อมสายฟ้า · depth dressing for the story's sets (contact shadows, light cones, rain that falls, clouds that drift, lamps that hum, distant lightning). Load after jkdepth.js and ltset.js.
(function () {
  const { dress, ao, band, cone, cast, motes, breathe, birds } = JKD;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const rain = (tl, sh, id) => { const el = document.getElementById(`${id}-rain`); if (!el) return; tl.fromTo(el, { y: 0 }, { y: 2600, duration: 0.55, repeat: Math.ceil(sh.dur / 0.55) + 1, ease: "none" }, Math.max(0, sh.start)); };
  const drift = (tl, sh, sel, dx = 60, p = 9) => { document.querySelectorAll(sel).forEach((el, k) => tl.fromTo(el, { x: 0 }, { x: dx * (k % 2 ? -1 : 1), duration: p + k * 0.7, repeat: Math.ceil(sh.dur / p), yoyo: true, ease: "sine.inOut" }, Math.max(0, sh.start))); };
  const hum = (tl, sh, sel, lo = 0.86, p = 0.11) => { document.querySelectorAll(sel).forEach((el, k) => tl.fromTo(el, { opacity: 1 }, { opacity: lo, duration: p + k * 0.017, repeat: Math.ceil(sh.dur / p), yoyo: true, ease: "none" }, Math.max(0, sh.start))); };
  // far lightning behind the clouds: the sheet flashes twice, at the times given (or at a seeded rhythm)
  const farBolts = (tl, sh, id, ats) => { const el = document.getElementById(`${id}-sheet`); if (!el) return;
    (ats || [1.1, 1.25, 4.6, 7.9, 8.05, 12.2].filter((t) => t < sh.dur)).forEach((t) => tl.fromTo(el, { opacity: 0.35 }, { opacity: 0, duration: 0.32, ease: "power2.out", immediateRender: false }, Math.max(0, sh.start) + t)); };
  const wetShine = (L, y, op = 0.18) => put(L.set, `<rect x="-2400" y="${y}" width="7600" height="260" fill="url(#jkHazeW)" opacity="${op}"/>`);

  dress.ltShop = (L, tl, sh, id, o) => {
    const night = o.time === "night" || o.time === "storm", lit = night && !o.blackout;
    put(L.set, `${band(1250, 60, 0.55)}${ao(760, 1404, 200, 16, 0.3)}${ao(230, 1404, 80, 10, 0.3)}${ao(420, 1404, 80, 10, 0.3)}${o.bike === false ? "" : ao(1450, 1404, 210, 16, 0.3)}${o.table ? ao(o.tableX ?? 1200, 1404, 160, 12, 0.28) : ""}${o.banana ? ao(1850, 1404, 90, 12, 0.3) : ""}${cast(360, 1040, 1250, 110, -60, night ? 0.3 : 0.14, 14)}`);
    if (o.rain || o.puddle) wetShine(L, 1400, 0.12);
    if (lit) { put(L.glow, `<g style="mix-blend-mode:screen">${cone(1488, 600, 40, 800, 0.7, "jkdCone")}</g>`); hum(tl, sh, `#${id}-lamps`, 0.9, 0.13); motes(L.glow, tl, sh, { n: 8, color: "#fff2c0", x: 1200, y: 500, w: 600, h: 800, seed: 5, r: 2.6 }); }
    else if (!night) { motes(L.glow, tl, sh, { n: 12, color: "#fff6c8", x: -200, y: 500, w: 1600, h: 900, seed: 3 }); birds(L.far, tl, sh, 300, 500, 3, "#3a3a4a"); }
    if (o.time === "storm") { drift(tl, sh, `#${id}-sky .ltCloud, .ltCloud`, 70, 8); farBolts(tl, sh, id, o.bolts); }
    rain(tl, sh, id);
  };
  dress.ltRoof = (L, tl, sh, id, o) => {
    put(L.set, `${band(1400, 50, 0.5)}${ao(760, 1404, 90, 12, 0.35)}${ao(1860, 1404, 90, 12, 0.35)}${ao(300, 1404, 50, 8, 0.3)}${cast(734, 52, 1400, 120, 160, 0.16, 12)}${cast(1834, 52, 1400, 120, 160, 0.16, 12)}`);
    if (o.storm !== false) { wetShine(L, 1400, 0.1); drift(tl, sh, `#${id}-clouds .ltCloud`, 90, 7); farBolts(tl, sh, id, o.bolts); hum(tl, sh, `#${id}-far .ltWin`, 0.7, 0.9); }
    else motes(L.glow, tl, sh, { n: 10, color: "#fff6c8", x: 0, y: 300, w: 1400, h: 900, seed: 11 });
    rain(tl, sh, id);
  };
  dress.ltWard = (L, tl, sh, id, o) => {
    put(L.set, `${band(1240, 50, 0.5)}${o.nursery ? [420, 900, 1380].map((x) => ao(x, 1404, 110, 12, 0.3)).join("") : [420, 1080, 1740].map((x) => ao(x, 1404, 300, 18, 0.3)).join("") + ao(1560, 1404, 110, 10, 0.3)}`);
    if (!o.blackout) { put(L.glow, `<g style="mix-blend-mode:screen">${[400, 1100, 1800].map((x) => cone(x, 560, 120, 700, 0.5, "jkdCone")).join("")}</g>`); hum(tl, sh, `#${id}-lights`, 0.94, 0.09); motes(L.glow, tl, sh, { n: 8, color: "#ffffff", x: 0, y: 500, w: 1400, h: 800, seed: 13, r: 2.4 }); }
    if (!o.nursery && !o.blackout) { const ln = document.getElementById(`${id}-ecgLine`); if (ln) tl.fromTo(ln, { strokeDasharray: "260 400", strokeDashoffset: 260 }, { strokeDashoffset: -400, duration: 1.6, repeat: Math.ceil(sh.dur / 1.6), ease: "none" }, Math.max(0, sh.start)); }
    if (o.nursery) document.querySelectorAll(`#${id}-set .ltIncLed`).forEach((el) => { if (!o.blackout) { el.setAttribute("opacity", "1"); breathe(tl, el, sh, 0.2, 1, 1.0); } });
  };
  dress.ltRoom = (L, tl, sh, id, o) => {
    put(L.set, `${band(1240, 50, 0.6)}${ao(1800, 1404, 80, 10, 0.3)}${ao(560, 1404, 100, 10, 0.3)}${cast(850, 300, 1240, 160, -40, 0.22, 14)}`);
    if (!o.blackout) { put(L.glow, `<g style="mix-blend-mode:screen">${cone(1300, 600, 30, 760, 0.8, "jkdCone")}</g>`); hum(tl, sh, `#${id}-lamps, #${id}-mid .ltBulbOn`, 0.8, 0.07); motes(L.glow, tl, sh, { n: 8, color: "#fff2c0", x: 900, y: 500, w: 800, h: 800, seed: 17, r: 2.4 }); }
  };
  dress.ltSky = (L, tl, sh, id, o) => {
    put(L.set, `${band(1260, 60, 0.6)}${ao(-150, 1404, 70, 10, 0.3)}`); wetShine(L, 1400, 0.1);
    if (!o.blackout) { put(L.glow, `<g style="mix-blend-mode:screen">${cone(1338, 600, 40, 800, 0.6, "jkdCone")}</g>`); hum(tl, sh, `#${id}-lights`, 0.9, 0.12); hum(tl, sh, `#${id}-far .ltWin`, 0.6, 0.7); }
    if (o.storm !== false) { drift(tl, sh, `#${id}-clouds .ltCloud`, 90, 7); farBolts(tl, sh, id, o.bolts); }
    rain(tl, sh, id);
  };
})();
