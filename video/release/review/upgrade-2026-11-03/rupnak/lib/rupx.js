// รูพญานาค · picture upgrade to the level of the four reference stories (owner 3 Nov 2569: "คุณเคยทำมาแล้ว น่าจะทำให้เหมือนได้นะ").
// Load after rupnak2.js. Reuses what the channel already built instead of drawing new flat boxes:
//   Sets.rupYardRich(L, o)  ยาย's yard as before, but the houses are เห็ดปอบ's detailed stilt house (Pop2.house2) with lit windows,
//                           a bulb under the floor pooling warm light on the ground, a lantern on the well, a woven granary
//   Sets.rupLegend3(L, o)   the naga legend on ผีแม่ม่าย's shadow-puppet screen (Sets.legend3): the village on a strip of earth at the
//                           top, the naga coiled under it as a black punched-leather puppet, only its eye lit (#id-naga, #id-eye)
//   RupX.legendLife(tl, id, t0, dur)  the puppet sways on its rods, the eye glows up once the line reaches it
(() => {
  const { put, f1 } = window.Pop2;
  const RupX = (window.RupX = window.RupX || {});

  // ---------------------------------------------------------------- the yard with real houses
  const granary = (x, G, s, night) => {
    const wall = night ? "#3a2a22" : "#a8784a", roof = night ? "#3a3e48" : "#8a8a7a";
    let g = `<g transform="translate(${f1(x)},${f1(G)}) scale(${f1(s)})"><ellipse cx="0" cy="6" rx="140" ry="18" fill="#000" opacity=".3"/>`;
    [-90, -30, 30, 90].forEach((px) => { g += `<rect x="${px - 8}" y="-170" width="16" height="170" fill="${night ? "#2a1c14" : "#5a3a24"}" stroke="#1a120c" stroke-width="3"/>`; });
    g += `<rect x="-110" y="-330" width="220" height="166" fill="${wall}" stroke="#1a120c" stroke-width="3.5"/>`;
    for (let k = 0; k < 9; k++) g += `<path d="M-110,${-318 + k * 18}H110" stroke="${night ? "#2a1e18" : "#7a5230"}" stroke-width="3" opacity=".8"/>`;
    for (let k = 0; k < 10; k++) g += `<path d="M${-100 + k * 22},-330V-164" stroke="${night ? "#2a1e18" : "#8a6038"}" stroke-width="1.6" opacity=".5"/>`;
    g += `<path d="M-150,-322L0,-430L150,-322Z" fill="${roof}" stroke="#1a120c" stroke-width="3.5"/>`;
    for (let k = 0; k < 9; k++) g += `<path d="M${-140 + k * 35},-326L${f1((k - 4) * 4)},-424" stroke="#1a1c22" stroke-width="2" opacity=".35"/>`;
    return g + `</g>`;
  };
  // a hanging bulb with its cone of light and a warm pool on the ground
  const bulb = (x, yTop, yBulb, G, col = "#ffe2a0") => `<path d="M${x},${yTop}V${yBulb - 10}" stroke="#1a1a1a" stroke-width="2.4"/>
    <ellipse cx="${x}" cy="${yBulb}" rx="11" ry="14" fill="#fff6d0" stroke="#8a7a40" stroke-width="1.6"/>
    <path d="M${x},${yBulb + 8}L${x - 260},${G}H${x + 260}Z" fill="${col}" opacity=".13" style="mix-blend-mode:screen"/>`;
  const glow = (x, y, r, op, col = "#ffcf7a") => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="${col}" opacity="${op}" filter="url(#rxBlur)" style="mix-blend-mode:screen"/>`;

  Sets.rupYardRich = (L, o = {}) => {
    const id = o.id || "ry", night = (o.time || "day") === "night";
    if (!document.getElementById("rxBlur")) put(L.sky, `<defs><filter id="rxBlur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="38"/></filter>
      <filter id="rxBlurS" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="10"/></filter></defs>`);
    // draw the old yard with every Rup.house swapped for the detailed stilt house
    const keep = Rup.house; const houses = [];
    Rup.house = (x, y, s = 1, ho = {}) => {
      const wd = (ho.w ?? 300) * s, s2 = wd / 520;
      houses.push({ x, y, s2, main: wd > 300 });
      let g = Pop2.house2(x, y, s2, { time: night ? "night" : "day", lit: night, under: true });
      if (night) g = `<g filter="brightness(.62) saturate(.8)">${g}</g>`;
      if (ho.granary) g += granary(x + wd * 0.5 + 150 * s2 * 1.6, y + 6, s2 * 1.15, night);
      return g;
    };
    try { Sets.rupYard(L, { ...o, id }); } finally { Rup.house = keep; }
    // the old overlays were drawn for the low flat house: the door, the lit window rect and the bulb now float, so take them out
    const door = document.getElementById(`${id}-door`); if (door && door.parentNode) door.parentNode.remove();
    document.querySelectorAll(`#layer-set rect[x="642"][y="902"], rect[x="642"][y="902"]`).forEach((n) => n.remove());
    document.querySelectorAll(`ellipse[cx="560"][cy="1060"], path[d="M560,1010V1050"], path[d="M560,1066L380,1236H740Z"]`).forEach((n) => n.remove());
    if (!night) return;
    const main = houses.find((h) => h.main) || houses[0], G = 1240, floor = G - 450 * main.s2;
    // warm lights: the bulb under the floor, the glow out of the windows, a hurricane lantern hanging on the well frame
    let s = bulb(main.x - 30, floor, floor + 70, G) + (window.Rup2 && Rup2.pool ? Rup2.pool(main.x - 30, G - 4, 330, 80) : "");
    put(L.set, s);
    put(L.glow, glow(main.x - 30, floor + 70, 120, 0.55) + glow(main.x + 60, floor - 150 * main.s2 * 2, 160, 0.35) +
      glow(370, 1345, 60, 0.5));
    put(L.set, `<g transform="translate(${250 + 120},${1560 - 250})"><path d="M0,0V26" stroke="#1a1a1a" stroke-width="2"/><rect x="-14" y="26" width="28" height="36" rx="6" fill="#ffd27a" stroke="#3a2a14" stroke-width="3"/><path d="M-16,26H16M-16,62H16" stroke="#3a2a14" stroke-width="4"/></g>`);
    put(L.glow, `<ellipse cx="320" cy="1600" rx="200" ry="46" fill="#ffcf7a" opacity=".1" style="mix-blend-mode:screen"/>`);
  };

  // ---------------------------------------------------------------- the naga on the shadow-puppet screen
  // a punched-leather หนังประโมทัย puppet: black silhouette, light only through the punched holes and the eye
  const nagaPuppet = (id) => {
    const body = "M120,1320C300,1400 700,1400 830,1260S800,1020 560,1040S200,1010 280,900S560,800 690,800";
    const tail = "M120,1320C60,1290 40,1240 70,1200";
    let g = `<path id="${id}-spine" d="${body}" fill="none" stroke="none"/>`;
    g += `<path d="${tail}" stroke="#050404" stroke-width="34" fill="none" stroke-linecap="round"/>`;
    g += `<path d="${body}" stroke="#050404" stroke-width="86" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
    // the crest (หงอนนาค): flame-shaped spikes along the head and neck
    const crest = [[650, 770, -20], [620, 760, -40], [590, 765, -60], [560, 785, -75], [535, 812, -90]];
    crest.forEach(([x, y, a]) => { g += `<g transform="translate(${x},${y}) rotate(${a})"><path d="M0,0C-10,-40 6,-70 -4,-110C14,-80 26,-50 22,-4Z" fill="#050404"/></g>`; });
    // the head: long snout, open jaw with fangs, the eye punched and lit
    g += `<g transform="translate(690,800) rotate(-8)">
      <path d="M-40,-46C20,-70 110,-60 170,-30L196,-8L140,0L196,12L170,40C110,60 20,64 -40,46Z" fill="#050404"/>
      <path d="M140,0L150,-14L158,0ZM164,4L172,18L178,4Z" fill="url(#mmScreen)"/>
      <path d="M20,-58C40,-90 70,-96 96,-80" stroke="#050404" stroke-width="16" fill="none" stroke-linecap="round"/>
      <circle id="${id}-eyeglow" cx="60" cy="-22" r="34" fill="#ffd25a" opacity=".55" filter="url(#rxBlurS)"/>
      <ellipse id="${id}-eye" cx="60" cy="-22" rx="15" ry="11" fill="#ffe27a"/><ellipse cx="60" cy="-22" rx="4" ry="9" fill="#050404"/></g>`;
    // the rods that work it, down out of the bottom of the screen
    g += `<path d="M470,1060L430,1500M760,1240L800,1500M690,820L740,1500" stroke="#120c08" stroke-width="7"/>`;
    return g;
  };
  const village = () => {
    // a strip of earth across the top: paddies, palms and three stilt houses in silhouette
    let g = `<path d="M60,700H1020V740H60Z" fill="#050404"/>`;
    for (let k = 0; k < 18; k++) g += `<path d="M${80 + k * 54},700l10,-26l10,26" fill="#050404"/>`;
    [[230, 0.9], [520, 1.1], [820, 0.85]].forEach(([x, s]) => {
      g += `<g transform="translate(${x},700) scale(${s})"><path d="M-70,0V-60M-30,0V-60M30,0V-60M70,0V-60" stroke="#050404" stroke-width="9"/>
        <rect x="-86" y="-120" width="172" height="62" fill="#050404"/><path d="M-110,-114L0,-196L110,-114Z" fill="#050404"/>
        <rect x="-20" y="-104" width="26" height="30" fill="url(#mmScreen)"/></g>`; });
    [[380, 1], [690, 0.8]].forEach(([x, s]) => { g += `<g transform="translate(${x},700) scale(${s})"><path d="M0,0V-150" stroke="#050404" stroke-width="10"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M0,-150q${(k - 2.5) * 30},${-30 + Math.abs(k - 2.5) * 12} ${(k - 2.5) * 56},${10 + Math.abs(k - 2.5) * 14}" stroke="#050404" stroke-width="8" fill="none"/>`).join("")}</g>`; });
    // the soil under the village: a few punched stars, the dark of the cave the naga lies in
    g += `<path d="M80,760C300,820 760,800 1000,770V1380H80Z" fill="#000" opacity=".18"/>`;
    return g;
  };
  Sets.rupLegend3 = (L, o = {}) => {
    const id = o.id || "lg";
    if (!document.getElementById("rxBlur")) put(L.sky, `<defs><filter id="rxBlur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="38"/></filter>
      <filter id="rxBlurS" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="10"/></filter></defs>`);
    Sets.legend3(L, { id, shirt: false });
    ["widow", "man"].forEach((p) => { const n = document.getElementById(`${id}-${p}`); if (n) n.setAttribute("opacity", "0"); });
    const clip = document.querySelector(`[clip-path="url(#${id}-clip)"]`);
    clip.insertAdjacentHTML("beforeend", `<g id="${id}-vil">${village()}</g><g id="${id}-naga">${nagaPuppet(id)}</g>`);
    // punched holes along the body, so the screen light shows through like real หนังประโมทัย
    const spine = document.getElementById(`${id}-spine`), len = spine.getTotalLength();
    let holes = "";
    for (let d = 40; d < len - 60; d += 34) { const p = spine.getPointAtLength(d), p2 = spine.getPointAtLength(d + 2), a = Math.atan2(p2.y - p.y, p2.x - p.x);
      const nx = -Math.sin(a), ny = Math.cos(a);
      holes += `<circle cx="${f1(p.x)}" cy="${f1(p.y)}" r="6" fill="url(#mmScreen)"/>`;
      holes += `<path d="M${f1(p.x + nx * 24)},${f1(p.y + ny * 24)}q${f1(Math.cos(a) * 10)},${f1(Math.sin(a) * 10)} ${f1(Math.cos(a) * 20)},0" stroke="url(#mmScreen)" stroke-width="3" fill="none"/>`;
      holes += `<path d="M${f1(p.x - nx * 24)},${f1(p.y - ny * 24)}q${f1(Math.cos(a) * 10)},${f1(Math.sin(a) * 10)} ${f1(Math.cos(a) * 20)},0" stroke="url(#mmScreen)" stroke-width="3" fill="none"/>`; }
    document.getElementById(`${id}-naga`).insertAdjacentHTML("beforeend", holes);
  };
  RupX.legendLife = (tl, id, t0, dur) => {
    tl.fromTo(`#${id}-naga`, { rotation: -1.2, svgOrigin: "520 1300" }, { rotation: 1.2, svgOrigin: "520 1300", duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 1.6), immediateRender: false }, t0);
    tl.fromTo(`#${id}-eyeglow`, { opacity: 0.15 }, { opacity: 0.85, duration: 0.6, ease: "power2.out", immediateRender: false }, t0 + Math.min(2.2, dur * 0.3));
  };
})();
