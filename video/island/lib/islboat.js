// "ติดเกาะ" — on ลุงเจี๊ยบ's longtail out at sea, and the wreck seen from the beach of เกาะผี.
// Same layer contract as tide.js. Seeded RNG only, no filters. Everything that moves is redrawn from the timeline clock by one proxy
// tween per call (Isl.sail / Isl.wash), so any seek gives the same frame. Needs pop2.js, qkmat.js, tide.js (Tide.longtail) and
// islpier.js (shared gradients) loaded first.
//
//   Sets.islBoat(L, o)   the camera sits in the bow looking aft along the boat: the two gunwales run from the bottom corners to the
//                        stern (the transom at y ~1200), three thwarts, the plank floor, a foam cooler box (the one that washes ashore),
//                        a fuel can, a bucket, a rope coil, a life vest; the engine on its pivot at the stern with the tiller and the long
//                        shaft back into the water; the sea all round, the home island receding behind the stern, the sky.
//                        o.weather "sunny" (default) | "squall" (a dark lid of cloud, rain in L.glow over everyone, big waves, spray,
//                        the horizon rolls) | "wreck" (squall + black rocks hard by the right gunwale, white water, the horizon pitched)
//                        · o.seed · o.cooler false hides the box · ids (redrawn): #id-wv0…5 waves, #id-sp spray, #id-rain, #id-flash
//                        (the lightning rect in L.glow, opacity), #id-tsky / #id-tfar (the world's roll), #id-dark (the darkening lid)
//                        Actor spots (feet, rig scale): Isl.BOAT.spots.uncle (560, 1352, 0.5 — sits on the aft thwart, mode sitChair),
//                        .fa (420, 1612, 0.78 — the middle thwart), .phum (720, 1760, 0.6 — the near thwart). The gunwale rails and the
//                        inner strake are drawn again in L.glow so they stay in front of whoever sits by them.
//   Isl.sail(tl, id, t0, dur, o)  runs the boat: o.roll (deg, default 1.5 sunny / 7 squall), o.period (s), o.storm [a, b] seconds into the
//                        call over which the sky darkens and the rain comes (0 … 1 ramp; the set's weather fixes the start value),
//                        o.flashes [t…] lightning (0.25 s white flashes at those seconds), o.hit (s: a jolt when the hull strikes)
//   Sets.islWash(L, o)   low in the surf on เกาะผี's beach looking out into the rain: swells and foam close by, the uncle's boat pitched
//                        and drifting away with a figure clinging to its hull (#id-boat), the red cap afloat near the camera (#id-cap),
//                        rain curtains, the squall sky · o.seed · ids (redrawn): #id-sw0…7 swells, #id-boat, #id-cap, #id-rain
//   Isl.wash(tl, id, t0, dur, o)  the boat drifts from its start to o.to (default far right, small) over the call (o.ease), the cap bobs
(function () {
  const { mk, f1, put, cloud2 } = Pop2;
  const Isl = (window.Isl = window.Isl || {});
  const ST = (Isl._st = Isl._st || {});
  const INK = "#2e2a26", OUT2 = `stroke="${INK}" stroke-width="2.5" stroke-linejoin="round"`, OUT3 = `stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"`;
  const T = Qk.tone, CS = Qk.cs, el = (id) => document.getElementById(id);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), lerp = (a, b, k) => a + (b - a) * k, sm = (a, b, x) => { const k = clamp((x - a) / (b - a), 0, 1); return k * k * (3 - 2 * k); };
  Sets.DEFS += `
    <linearGradient id="isSkyS" gradientUnits="userSpaceOnUse" x1="0" y1="-1200" x2="0" y2="800"><stop offset="0" stop-color="#2c3842"/><stop offset=".5" stop-color="#5e6c76"/><stop offset=".85" stop-color="#949ea2"/><stop offset="1" stop-color="#b6bab2"/></linearGradient>
    <linearGradient id="isSeaS" gradientUnits="userSpaceOnUse" x1="0" y1="780" x2="0" y2="2000"><stop offset="0" stop-color="#8a968e"/><stop offset=".08" stop-color="#53666a"/><stop offset=".5" stop-color="#3a5560"/><stop offset="1" stop-color="#2a4048"/></linearGradient>
    <linearGradient id="isSeaB" gradientUnits="userSpaceOnUse" x1="0" y1="780" x2="0" y2="2000"><stop offset="0" stop-color="#b9dfe6"/><stop offset=".07" stop-color="#2a9fb8"/><stop offset=".5" stop-color="#2690ad"/><stop offset="1" stop-color="#1d7a9a"/></linearGradient>
    <linearGradient id="isHullIn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9b07a"/><stop offset=".5" stop-color="#a97a46"/><stop offset="1" stop-color="#5e3f22"/></linearGradient>
    <linearGradient id="isFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6a44"/><stop offset="1" stop-color="#5a4028"/></linearGradient>
    <linearGradient id="isRock" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a4a4e"/><stop offset=".6" stop-color="#2a2a30"/><stop offset="1" stop-color="#15161a"/></linearGradient>`;

  // ---------------- the boat interior ----------------
  const B = { NL: [20, 1960], NR: [1060, 1960], SL: [440, 1200], SR: [640, 1200], HZ: 780 };
  const edge = (y, side) => { const [nx, ny] = side < 0 ? B.NL : B.NR, [sx, sy] = side < 0 ? B.SL : B.SR, k = (ny - y) / (ny - sy); return lerp(nx, sx, k); };
  const spots = { uncle: { x: 560, y: 1352, s: 0.5 }, fa: { x: 420, y: 1612, s: 0.78 }, phum: { x: 720, y: 1760, s: 0.6 } };
  Isl.BOAT = { ...B, edge, spots };

  function boatSky(L, id, weather, seed) {
    const r = mk(seed), storm = weather !== "sunny", hz = B.HZ;
    let g = `<g id="${id}-tsky"><rect x="-3000" y="${hz - 4200}" width="8000" height="${4200 + hz + 2200}" fill="url(#${storm ? "isSkyS" : "isSkyM"})"/>`;
    if (!storm) g += `<circle cx="1300" cy="${hz - 1150}" r="760" fill="url(#qkSun)" opacity=".7"/>`;
    for (let k = 0; k < 7; k++) g += cloud2(-760 + k * 560 + r() * 220, hz - (storm ? 500 : 760) - r() * 640, (storm ? 520 : 300) + r() * 320, (storm ? 170 : 90) + r() * 60, r, storm ? "tdCloudS" : "tdCloudM", storm ? "#a8b0ae" : "#ffffff", storm ? "#3a444a" : "#9fb8ca");
    if (storm) for (let k = 0; k < 6; k++) g += cloud2(-900 + k * 600 + r() * 200, hz - 1200 + r() * 700, 900 + r() * 500, 300 + r() * 160, r, "tdCloudS", "#6a7472", "#141a20");
    g += `<rect id="${id}-dark" x="-3000" y="${hz - 4200}" width="8000" height="7000" fill="#1a2430" opacity="${storm ? 0.45 : 0}"/></g>`;
    put(L.sky, g);
  }
  function waves(id, n) { let g = ""; for (let k = 0; k < n; k++) g += `<path id="${id}-wv${k}" d="" fill="#ffffff" opacity="0"/>`; return g; }
  function islBoat(L, o = {}) {
    const id = o.id || "bt", w = o.weather || "sunny", storm = w !== "sunny", r = mk(o.seed || 7), hz = B.HZ;
    boatSky(L, id, w, (o.seed || 7) + 1);
    // far: the sea to the horizon (rolls with the sky), the home island receding behind the stern, far whitecaps
    let f = `<g id="${id}-tfar"><rect x="-3000" y="${hz}" width="8000" height="1600" fill="url(#${storm ? "isSeaS" : "isSeaB"})"/>`;
    f += `<path d="M60,${hz + 2}C220,${hz - 30} 380,${hz - 58} 560,${hz - 40}C680,${hz - 28} 740,${hz - 12} 820,${hz + 2}Z" fill="${storm ? "#58686a" : "#7fa3a0"}" opacity=".75"/><path d="M120,${hz + 2}C260,${hz - 26} 390,${hz - 52} 540,${hz - 38}L560,${hz + 2}Z" fill="${storm ? "#66767a" : "#9bbcb2"}" opacity=".45"/>`;
    f += `<rect x="-3000" y="${hz - 14}" width="8000" height="22" fill="${storm ? "#aab2ac" : "#e4f0ee"}" opacity=".5"/>`;
    for (let k = 0; k < 60; k++) { const y = hz + 10 + Math.pow(r(), 1.7) * 500, x = -800 + r() * 2700, len = 12 + (y - hz) * 0.3 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1 + (y - hz) / 220)}" opacity="${f1((storm ? 0.3 : 0.18) + r() * 0.3)}" stroke-linecap="round"/>`; }
    f += waves(id, 6) + `</g>`;
    put(L.far, f);
    // set: the hull seen from inside: the inner planking up to the gunwales, the floor, the thwarts, the stern and the engine, the props
    let s = "";
    if (w === "wreck") {
      // black rocks hard by the right side, foam boiling at their feet
      s += `<g transform="translate(1180,1420)"><path d="M-260,120C-240,20 -160,-120 -40,-150C60,-176 140,-80 170,-10C210,80 160,160 60,170C-60,182 -200,190 -260,120Z" fill="url(#isRock)" ${OUT3}/><path d="M-200,60C-170,-20 -120,-100 -40,-130C20,-150 60,-120 50,-100C-20,-90 -110,-30 -150,70Z" fill="#6a6a70" opacity=".45"/><path d="M-230,100C-120,110 0,118 120,100" stroke="#fff" stroke-width="10" opacity=".55" fill="none"/></g>`;
      s += `<g transform="translate(1340,1200)"><path d="M-160,120C-150,30 -90,-60 0,-80C90,-100 150,-20 160,60C170,130 100,160 20,160C-60,162 -160,170 -160,120Z" fill="url(#isRock)" ${OUT3}/><path d="M-120,70C-90,0 -40,-50 20,-60L30,-40C-20,-30 -80,20 -100,80Z" fill="#6a6a70" opacity=".4"/></g>`;
      s += `<path id="${id}-foam" d="" fill="#ffffff" opacity=".8"/>`;
    }
    const hullIn = (side) => { const [nx, ny] = side < 0 ? B.NL : B.NR, [sx, sy] = side < 0 ? B.SL : B.SR, ox = side * 110, oy = -36; return `M${f1(nx)},${f1(ny)}L${f1(sx)},${f1(sy)}L${f1(sx + side * 26)},${f1(sy - 12)}L${f1(nx + ox)},${f1(ny + oy)}Z`; };
    // the outside of the far side of the hull is not seen; the inner planking of both sides, lit from the right
    s += `<path d="${hullIn(-1)}" fill="url(#isHullIn)" ${OUT3}/><path d="${hullIn(1)}" fill="${T("#a97a46", 0.08)}" ${OUT3}/>`;
    [-1, 1].forEach((side) => { for (let k = 1; k < 4; k++) { const q = k / 4, [nx, ny] = side < 0 ? B.NL : B.NR, [sx, sy] = side < 0 ? B.SL : B.SR; s += `<path d="M${f1(nx + side * 110 * q)},${f1(ny - 36 * q)}L${f1(sx + side * 26 * q)},${f1(sy - 12 * q)}" stroke="#6a4a28" stroke-width="2" opacity=".6"/>`; } });
    // the floor: planks converging to the stern, a bilge line, the ribs
    s += `<path d="M${f1(B.NL[0] + 110)},${f1(B.NL[1] - 36)}L${f1(B.SL[0] + 26)},${f1(B.SL[1] - 12)}L${f1(B.SR[0] - 26)},${f1(B.SR[1] - 12)}L${f1(B.NR[0] - 110)},${f1(B.NR[1] - 36)}Z" fill="url(#isFloor)" ${OUT2}/>`;
    for (let k = 1; k < 6; k++) { const q = k / 6, x0 = lerp(B.NL[0] + 110, B.NR[0] - 110, q), x1 = lerp(B.SL[0] + 26, B.SR[0] - 26, q); s += `<path d="M${f1(x0)},${f1(B.NL[1] - 36)}L${f1(x1)},${f1(B.SL[1] - 12)}" stroke="#3e2a16" stroke-width="2.2" opacity=".7"/>`; }
    for (let k = 0; k < 9; k++) { const y = 1220 + (k / 9) * 700 + k * k * 1.2, q = (B.NL[1] - 36 - y) / (B.NL[1] - 36 - B.SL[1] + 12), xl = lerp(B.NL[0] + 110, B.SL[0] + 26, q), xr = lerp(B.NR[0] - 110, B.SR[0] - 26, q); s += `<path d="M${f1(xl)},${f1(y)}H${f1(xr)}" stroke="#5a4028" stroke-width="${f1(3 + (1 - q) * 6)}" opacity=".55"/>`; }
    // the stern: the transom, the engine on its pivot, the tiller forward, the shaft and propeller back in the water
    s += `<path d="M${f1(B.SL[0] - 6)},${f1(B.SL[1] - 12)}H${f1(B.SR[0] + 6)}L${f1(B.SR[0] + 18)},${f1(B.SR[1] - 70)}H${f1(B.SL[0] - 18)}Z" fill="#b98a52" ${OUT3}/><path d="M${f1(B.SL[0] + 10)},${f1(B.SL[1] - 20)}H${f1(B.SR[0] - 10)}" stroke="#fff" stroke-width="3" opacity=".25"/>`;
    s += `<path d="M560,${B.SL[1] - 70}L560,${B.SL[1] - 150}" stroke="#5a5048" stroke-width="12"/><g transform="translate(560,${B.SL[1] - 196})"><rect x="-56" y="-40" width="112" height="76" rx="10" fill="#6a7074" ${OUT2}/>${[-34, -17, 0, 17, 34].map((xx) => `<path d="M${xx},-36v66" stroke="#4a5054" stroke-width="5"/>`).join("")}<rect x="-56" y="-40" width="112" height="14" rx="6" fill="#9aa2a6"/><circle cx="-34" cy="-48" r="12" fill="#d84a36" ${OUT2}/><rect x="56" y="-6" width="18" height="30" fill="#3e4448" ${OUT2}/><path d="M-20,-22h30v10h-30z" fill="#e8e0d0" opacity=".7"/></g>`;
    s += `<path d="M560,${B.SL[1] - 150}L690,${B.SL[1] - 310}" stroke="#7e868a" stroke-width="10" stroke-linecap="round"/><path d="M560,${B.SL[1] - 150}L690,${B.SL[1] - 310}" stroke="#d8dcdc" stroke-width="3" opacity=".6"/><g transform="translate(696,${B.SL[1] - 318}) rotate(-50)"><ellipse rx="8" ry="26" fill="#c8a040" ${OUT2}/></g>`;
    s += `<path d="M520,${B.SL[1] - 196}L300,${B.SL[1] - 120}" stroke="#5a5048" stroke-width="9" stroke-linecap="round"/><circle cx="300" cy="${B.SL[1] - 120}" r="8" fill="#3a3430"/>`;
    // the thwarts: near (wide), middle, aft; each a plank with its front face, dark shadow under it
    const thwart = (y, h, lip) => { const q = (B.NL[1] - 36 - y) / (B.NL[1] - 36 - B.SL[1] + 12), xl = lerp(B.NL[0] + 110, B.SL[0] + 26, q) - lip, xr = lerp(B.NR[0] - 110, B.SR[0] - 26, q) + lip; return `<path d="M${f1(xl)},${f1(y + h * 0.6)}H${f1(xr)}v${f1(h * 1.4)}H${f1(xl)}Z" fill="#000" opacity=".22"/><path d="M${f1(xl)},${f1(y)}H${f1(xr)}v${f1(h)}H${f1(xl)}Z" fill="#8a6238" ${OUT2}/><path d="M${f1(xl)},${f1(y - h * 0.55)}H${f1(xr)}v${f1(h * 0.55)}H${f1(xl)}Z" fill="#c49a62" ${OUT2}/><path d="M${f1(xl + 8)},${f1(y - h * 0.3)}H${f1(xr - 8)}" stroke="#fff" stroke-width="3" opacity=".22"/>`; };
    s += thwart(1300, 22, 14) + thwart(1560, 30, 18) + thwart(1760, 40, 22);
    // props: the foam cooler by the middle thwart, a fuel can and a bucket at the stern, a rope coil and a life vest forward
    if (o.cooler !== false) s += `<g transform="translate(800,1500)">${CS(0, 6, 90, 14, 0.6)}<rect x="-70" y="-100" width="140" height="100" rx="8" fill="#f4f6f4" ${OUT2}/><rect x="-74" y="-112" width="148" height="22" rx="8" fill="#2a8ad0" ${OUT2}/><path d="M-70,-50H70" stroke="#d8dcdc" stroke-width="3"/><path d="M-60,-96V-10" stroke="#fff" stroke-width="5" opacity=".5"/><text x="0" y="-22" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="20" fill="#2a6ab8">น้ำแข็ง</text><path d="M-20,-112V-124H20V-112" stroke="#1e4e94" stroke-width="5" fill="none"/></g>`;
    s += `<g transform="translate(450,1262)">${CS(0, 4, 40, 8, 0.6)}<rect x="-26" y="-56" width="52" height="56" rx="5" fill="#d8b232" ${OUT2}/><rect x="-10" y="-66" width="20" height="12" rx="3" fill="#8a7020"/><path d="M-18,-50v40" stroke="#fff" stroke-width="3" opacity=".3"/></g>`;
    s += `<g transform="translate(680,1270)">${CS(0, 3, 34, 7, 0.6)}<path d="M-26,-44L-20,0H20L26,-44Z" fill="#2a6ab8" ${OUT2}/><ellipse cx="0" cy="-44" rx="26" ry="7" fill="#4a8ad8" ${OUT2}/><path d="M-26,-44Q0,-80 26,-44" stroke="#1e4e94" stroke-width="4" fill="none"/></g>`;
    s += `<g transform="translate(240,1850)">${CS(0, 4, 60, 12, 0.5)}<ellipse rx="52" ry="20" fill="none" stroke="#e8d8a8" stroke-width="9"/><ellipse rx="30" ry="11" fill="none" stroke="#d8c898" stroke-width="7"/><path d="M-52,0q20,-18 52,-10" stroke="#c8b488" stroke-width="5" fill="none"/></g>`;
    s += `<g transform="translate(120,1700) rotate(-30)"><path d="M-70,-40Q-80,20 -50,60L50,66Q80,20 66,-44Q30,-60 0,-54Q-40,-60 -70,-40Z" fill="#ff8a3a" ${OUT2}/><path d="M-50,-20Q0,-10 50,-24M-44,10Q0,20 46,6" stroke="#c8561a" stroke-width="4" fill="none"/><rect x="-12" y="-54" width="24" height="110" fill="#2a2420" opacity=".2"/></g>`;
    s += `<g transform="translate(930,1780)"><rect x="-14" y="-70" width="28" height="70" rx="6" fill="#dff4f8" opacity=".8" ${OUT2}/><rect x="-7" y="-82" width="14" height="14" rx="3" fill="#2a8ad0"/><rect x="-11" y="-52" width="22" height="22" fill="#2a8ad0" opacity=".9"/></g>`;
    // spray and the near water seen over the bow corners (the hull's outside is below the frame)
    s += `<g id="${id}-sp">${Array.from({ length: 14 }, (_, k) => `<circle id="${id}-sp${k}" r="4" fill="#ffffff" opacity="0"/>`).join("")}</g>`;
    put(L.set, s);
    // glow: the gunwale rails and the top strake again, so they stay in front of whoever sits against them; the lightning
    let g = `<path d="${hullIn(-1)}" fill="url(#isHullIn)" ${OUT3} clip-path="inset(0 0 0 0)"/>`.replace(` clip-path="inset(0 0 0 0)"`, "");
    g = "";
    [-1, 1].forEach((side) => { const [nx, ny] = side < 0 ? B.NL : B.NR, [sx, sy] = side < 0 ? B.SL : B.SR; g += `<path d="M${f1(nx)},${f1(ny)}L${f1(sx)},${f1(sy)}L${f1(sx + side * 8)},${f1(sy - 4)}L${f1(nx + side * 34)},${f1(ny - 12)}Z" fill="#8a6238" ${OUT2}/><path d="M${f1(nx)},${f1(ny)}L${f1(sx)},${f1(sy)}" stroke="#e2bd86" stroke-width="7" stroke-linecap="round"/><path d="M${f1(nx)},${f1(ny - 2)}L${f1(sx)},${f1(sy - 1)}" stroke="#fff" stroke-width="2.5" opacity=".55"/>`; });
    if (storm) { let rain = ""; for (let k = 0; k < 150; k++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, len = 40 + r() * 70; rain += `<path d="M${f1(x)},${f1(y)}l-14,${f1(len)}" stroke="#dfe8ec" stroke-width="${f1(1.2 + r() * 1.6)}" opacity="${f1(0.35 + r() * 0.4)}" stroke-linecap="round"/>`; } g += `<g id="${id}-rain" opacity="0">${rain}<g transform="translate(0,-2200)">${rain}</g></g>`; }
    g += `<rect id="${id}-flash" x="-200" y="-200" width="1480" height="2320" fill="#ffffff" opacity="0"/>`;
    put(L.glow, g);
    ST[id] = { kind: "boat", storm: storm ? 1 : 0, wreck: w === "wreck", hz, roll: storm ? 7 : 1.5, tiltBase: w === "wreck" ? -9 : 0 };
    boatDraw(id, 0, { storm: storm ? 1 : 0 });
  }
  function boatDraw(id, t, o = {}) {
    const S = ST[id], st = clamp(o.storm ?? S.storm, 0, 1), roll = (o.roll ?? S.roll) * Math.sin(t * (2 * Math.PI) / (o.period || (S.storm ? 2.6 : 4.2))) + S.tiltBase + (o.jolt || 0), hz = S.hz;
    const tr = `rotate(${f1(roll)} 540 1100) translate(0,${f1(6 * st * Math.sin(t * 2.1))})`;
    const a = el(`${id}-tsky`), b = el(`${id}-tfar`);
    if (a) a.setAttribute("transform", tr);
    if (b) b.setAttribute("transform", tr);
    const dk = el(`${id}-dark`); if (dk) dk.setAttribute("opacity", f1(0.5 * st));
    for (let k = 0; k < 6; k++) {
      const e = el(`${id}-wv${k}`); if (!e) continue;
      const q = (((k / 6) + t * (0.08 + 0.06 * st)) % 1 + 1) % 1, y = hz + 20 + Math.pow(q, 1.5) * 1500, d0 = clamp((y - hz) / 900, 0.05, 1.6), amp = (3 + 30 * st) * d0, hgt = (2 + 18 * st) * d0;
      let up = "", dn = ""; for (let x = -1300; x <= 2400; x += 40) { const yy = y + amp * Math.sin(x * 0.009 + t * 1.3 + k) + amp * 0.5 * Math.sin(x * 0.027 - t * 2 + k); up += `${up ? "L" : "M"}${f1(x)},${f1(yy)}`; dn = `L${f1(x)},${f1(yy + hgt)}` + dn; }
      e.setAttribute("d", up + dn + "Z");
      e.setAttribute("opacity", f1((0.3 + 0.6 * st) * Math.sin(Math.PI * q) * (0.5 + 0.5 * d0)));
    }
    const rn = el(`${id}-rain`); if (rn) { rn.setAttribute("opacity", f1(0.9 * sm(0.15, 0.6, st))); rn.setAttribute("transform", `translate(${f1(-((t * 900) % 2200) * 0.14)},${f1((t * 900) % 2200)})`); }
    const fm = el(`${id}-foam`); if (fm) { let d = ""; for (let x = 860; x <= 1500; x += 30) d += `${d ? "L" : "M"}${f1(x)},${f1(1540 + 14 * Math.sin(x * 0.03 + t * 5) + 8 * Math.sin(x * 0.11 - t * 7))}`; fm.setAttribute("d", d + "L1500,1640L860,1640Z"); }
    for (let k = 0; k < 14; k++) { const sp = el(`${id}-sp${k}`); if (!sp) continue; const ph = t * (2.2 + k * 0.3) + k * 1.7, u = (ph % 1 + 1) % 1, side = k % 2 ? 1 : -1, x = (side < 0 ? 60 : 1020) + side * (-20 + 60 * u) + 14 * Math.sin(k), y = 1500 + k * 28 - 180 * u + 120 * u * u; sp.setAttribute("cx", f1(x)); sp.setAttribute("cy", f1(y)); sp.setAttribute("r", f1(3 + 5 * st)); sp.setAttribute("opacity", f1(st * 0.8 * Math.sin(Math.PI * u))); }
  }
  Isl.sail = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], c = { t: 0 }, [a, b] = o.storm || [99, 100], fl = o.flashes || [], hitAt = o.hit;
    const stAt = (tt) => Math.max(S.storm, clamp((tt - a) / Math.max(0.01, b - a), 0, 1));
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => {
      const tt = c.t, st = stAt(tt);
      let jolt = 0; if (hitAt !== undefined && tt >= hitAt) { const u = tt - hitAt; jolt = -14 * Math.exp(-u * 2.2) * Math.cos(u * 9); }
      boatDraw(id, t0 + tt, { storm: st, roll: o.roll ?? lerp(1.5, 7, st), period: o.period, jolt });
      const f = el(`${id}-flash`); if (f) { let op = 0; fl.forEach((ft) => { const u = tt - ft; if (u >= 0 && u < 0.3) op = Math.max(op, u < 0.06 ? 0.95 : u < 0.12 ? 0.3 : u < 0.18 ? 0.8 : 0.9 * (1 - (u - 0.18) / 0.12)); }); f.setAttribute("opacity", f1(op)); }
    } }, t0);
  };

  // ---------------- the wreck from the beach of เกาะผี ----------------
  function islWash(L, o = {}) {
    const id = o.id || "bw", r = mk(o.seed || 11), hz = 820;
    boatSky(L, id, "squall", (o.seed || 11) + 1);
    let f = `<g id="${id}-tfar"><rect x="-3000" y="${hz}" width="8000" height="1600" fill="url(#isSeaS)"/><rect x="-3000" y="${hz - 14}" width="8000" height="22" fill="#aab2ac" opacity=".4"/>`;
    for (let k = 0; k < 50; k++) { const y = hz + 10 + Math.pow(r(), 1.6) * 400, x = -800 + r() * 2700, len = 16 + (y - hz) * 0.4 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1.2 + (y - hz) / 200)}" opacity="${f1(0.3 + r() * 0.3)}" stroke-linecap="round"/>`; }
    f += `</g>`;
    put(L.far, f);
    // mid: the boat pitched over, a figure clinging to the near gunwale (ลุงเจี๊ยบ: the yellow polo, bare head), drifting
    const cling = `<g transform="translate(-80,-150)"><circle cx="0" cy="-60" r="26" fill="#c8906a" ${OUT2}/><path d="M-26,-66Q0,-96 26,-66" fill="#2a2420"/><path d="M-40,-30Q0,-50 40,-30L46,0H-46Z" fill="#f2c030" ${OUT2}/><path d="M-46,-26L-90,-6M46,-26L90,-6" stroke="#c8906a" stroke-width="12" stroke-linecap="round"/><circle cx="-96" cy="-4" r="10" fill="#c8906a" ${OUT2}/><circle cx="96" cy="-4" r="10" fill="#c8906a" ${OUT2}/></g>`;
    put(L.mid, `<g id="${id}-boatP"><g id="${id}-boat"><ellipse cx="0" cy="60" rx="620" ry="70" fill="#ffffff" opacity=".35"/><g transform="rotate(-18)">${Tide.longtail({ hull: "#f2c030", band: "#1e4e94", no: "เจี๊ยบทัวร์", flip: true, water: "#3a5560", seed: 3, k: 90 })}${cling}</g></g></g>`);
    // set: the swells close by, foam, the red cap afloat, rain over everything in glow
    let s = `<rect x="-1300" y="1200" width="3700" height="1000" fill="#2a4048"/>`;
    for (let k = 0; k < 8; k++) s += `<path id="${id}-sw${k}" d="" fill="${k % 2 ? "#3a5560" : "#2e4a52"}" stroke="#ffffff" stroke-width="${f1(2 + k)}" opacity=".95"/><path id="${id}-sf${k}" d="" fill="#ffffff" opacity=".6"/>`;
    s += `<g id="${id}-capP"><g id="${id}-cap"><ellipse cx="0" cy="18" rx="70" ry="14" fill="#1a2a30" opacity=".5"/><path d="M-56,8Q-56,-44 0,-44Q56,-44 56,8Z" fill="#d8302a" ${OUT2}/><path d="M-62,8Q0,22 62,8L70,18Q0,34 -70,18Z" fill="#b02018" ${OUT2}/><path d="M-30,-30Q0,-40 30,-30" stroke="#fff" stroke-width="4" fill="none" opacity=".6"/><path d="M-6,-44V-54" stroke="#2a2420" stroke-width="4"/></g></g>`;
    put(L.set, s);
    let rain = ""; for (let k = 0; k < 170; k++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, len = 50 + r() * 90; rain += `<path d="M${f1(x)},${f1(y)}l-18,${f1(len)}" stroke="#dfe8ec" stroke-width="${f1(1.4 + r() * 1.8)}" opacity="${f1(0.4 + r() * 0.4)}" stroke-linecap="round"/>`; }
    put(L.glow, `<g id="${id}-rain">${rain}<g transform="translate(0,-2200)">${rain}</g></g><rect id="${id}-flash" x="-200" y="-200" width="1480" height="2320" fill="#ffffff" opacity="0"/>`);
    ST[id] = { kind: "wash", hz, boat: { from: { x: 700, y: 1210, s: 0.55 }, to: o.to || { x: 1100, y: 1000, s: 0.2 } } };
    washDraw(id, 0, 0);
  }
  function washDraw(id, t, go) {
    const S = ST[id], hz = S.hz;
    const tf = el(`${id}-tfar`); if (tf) tf.setAttribute("transform", `rotate(${f1(3 * Math.sin(t * 1.4))} 540 1100)`);
    for (let k = 0; k < 8; k++) {
      const e = el(`${id}-sw${k}`), fo = el(`${id}-sf${k}`); if (!e) continue;
      const q = (((k / 8) + t * 0.11) % 1 + 1) % 1, y = 1180 + Math.pow(q, 1.4) * 900, d0 = 0.3 + q, amp = 40 * d0, hgt = 60 * d0;
      let up = "", dn = ""; for (let x = -1300; x <= 2400; x += 40) { const yy = y + amp * Math.sin(x * 0.006 + t * 1.1 + k) + amp * 0.45 * Math.sin(x * 0.021 - t * 1.9 + k * 2); up += `${up ? "L" : "M"}${f1(x)},${f1(yy)}`; dn = `L${f1(x)},${f1(yy + hgt)}` + dn; }
      e.setAttribute("d", up + `L2400,2400L-1300,2400Z`);
      let fd = ""; for (let x = -1300; x <= 2400; x += 40) { const yy = y + amp * Math.sin(x * 0.006 + t * 1.1 + k) + amp * 0.45 * Math.sin(x * 0.021 - t * 1.9 + k * 2); fd += `${fd ? "L" : "M"}${f1(x)},${f1(yy + 4 * Math.sin(x * 0.1 + t * 6))}`; }
      fo.setAttribute("d", fd + `L2400,${f1(y + hgt * 0.35 + 40)}L-1300,${f1(y + hgt * 0.35 + 40)}Z`);
      fo.setAttribute("opacity", f1(0.25 + 0.4 * Math.sin(Math.PI * q)));
      e.setAttribute("opacity", f1(0.4 + 0.6 * Math.sin(Math.PI * Math.min(1, q * 1.4))));
    }
    const bp = el(`${id}-boatP`); if (bp) { const E = go * go * (3 - 2 * go), F = S.boat.from, Tt = S.boat.to, x = lerp(F.x, Tt.x, E), y = lerp(F.y, Tt.y, E), s = lerp(F.s, Tt.s, E); bp.setAttribute("transform", `translate(${f1(x + 10 * Math.sin(t * 0.8))},${f1(y + 18 * Math.sin(t * 1.5))}) rotate(${f1(6 * Math.sin(t * 1.2))}) scale(${f1(s)})`); }
    const cp = el(`${id}-capP`); if (cp) cp.setAttribute("transform", `translate(${f1(330 + 60 * Math.sin(t * 0.5) + 40 * go)},${f1(1640 + 26 * Math.sin(t * 1.6))}) rotate(${f1(10 * Math.sin(t * 1.3))})`);
    const rn = el(`${id}-rain`); if (rn) rn.setAttribute("transform", `translate(${f1(-((t * 1000) % 2200) * 0.16)},${f1((t * 1000) % 2200)})`);
  }
  Isl.wash = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, E = gsap.parseEase(o.ease || "power1.inOut"), fl = o.flashes || [];
    if (o.to) ST[id].boat.to = o.to;
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { washDraw(id, t0 + c.t, E(clamp(c.t / dur, 0, 1))); const f = el(`${id}-flash`); if (f) { let op = 0; fl.forEach((ft) => { const u = c.t - ft; if (u >= 0 && u < 0.3) op = Math.max(op, u < 0.06 ? 0.95 : u < 0.12 ? 0.3 : u < 0.18 ? 0.8 : 0.9 * (1 - (u - 0.18) / 0.12)); }); f.setAttribute("opacity", f1(op)); } } }, t0);
  };
  Object.assign(Sets, { islBoat, islWash });
})();
