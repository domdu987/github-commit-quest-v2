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

  // ---------------------------------------------------------------- shared defs
  Sets.DEFS += `
    <filter id="rxBlur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="38"/></filter>
    <filter id="rxBlurS" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="10"/></filter>
    <radialGradient id="rxAO"><stop offset="0" stop-color="#1a120c" stop-opacity=".6"/><stop offset=".7" stop-color="#1a120c" stop-opacity=".2"/><stop offset="1" stop-color="#1a120c" stop-opacity="0"/></radialGradient>
    <linearGradient id="rxUnder" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".46"/><stop offset="1" stop-color="#000" stop-opacity=".1"/></linearGradient>
    <linearGradient id="rxPost" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
    <linearGradient id="rxWallSh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".36"/><stop offset=".17" stop-color="#000" stop-opacity=".05"/><stop offset=".86" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient>
    <radialGradient id="rxWinGlow"><stop offset="0" stop-color="#ffd890" stop-opacity=".6"/><stop offset=".45" stop-color="#ffb860" stop-opacity=".2"/><stop offset="1" stop-color="#ff9a40" stop-opacity="0"/></radialGradient>
    <pattern id="rxWeave" width="14" height="14" patternUnits="userSpaceOnUse"><path d="M1,3.5H6.5M7.5,10.5H13" stroke="#000" stroke-opacity=".3" stroke-width="2.2"/><path d="M10.5,1V6.5M3.5,8V13" stroke="#000" stroke-opacity=".22" stroke-width="2.2"/><path d="M1,2.4H6.5M7.5,9.4H13" stroke="#fff" stroke-opacity=".12" stroke-width="1"/></pattern>`;

  // ---------------------------------------------------------------- the stilt house, richer on the SAME geometry
  // Every coordinate of the old Rup.house is kept (posts, floor beam, wall, door, window, roof, ladder, granary), so what the
  // episodes draw on top of it — the door that swings open, the lit window, the leaning post, the bulb, the cracks — still sits
  // exactly where it did. What changes is the material: grained posts on footings and a back row in the dark, two-tone planks with
  // the eave's shadow, open shutters, corrugated zinc with rust, a woven granary, and the life under the floor (a hammock, a bamboo
  // bench, a water jar, a fish trap, firewood). A house tinted for night (dark wall) gets a warm lit window.
  const mix = Rup.mix, f = (v) => (+v).toFixed(1);
  const LINE = "#2a1c16", ln = (w = 3) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const lum = (h) => { if (!/^#[0-9a-f]{6}$/i.test(h)) return 0.4; const v = [1, 3, 5].map((i) => parseInt(h.substr(i, 2), 16) / 255); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  RupX.houseOld = Rup.house;
  Rup.house = (x, y, s = 1, o = {}) => {
    const wd = o.w ?? 300, wall = o.wall ?? "#8a5a3a", roof = o.roof ?? "#7a8a96";
    const night = o.night ?? lum(wall) < 0.3, T = (c) => (night ? mix(c, "#1a2448", 0.62) : c), lit = o.lit ?? night;
    const big = wd * s > 190, r = Rup.rng(Math.round(Math.abs(x * 7 + y * 3)) + 17);
    const dk = (c, k) => mix(c, "#140c08", k), lt = (c, k) => mix(c, "#fff4e0", k);
    const post = T("#5a3a24"), beam = T("#6a4228");
    let g = `<g transform="translate(${f(x)},${f(y)}) scale(${s})">`;
    // contact shadow, the back row of posts in the dark, the shade under the floor (deeper at the back)
    g += `<ellipse cx="0" cy="6" rx="${f(wd * 0.72)}" ry="24" fill="url(#rxAO)"/>`;
    [-0.31, 0, 0.31].forEach((t) => { g += `<rect x="${f(t * wd - 5)}" y="-150" width="10" height="144" fill="${dk(post, 0.5)}"/>`; });
    g += `<rect x="${f(-wd / 2 + 6)}" y="-150" width="${f(wd - 12)}" height="150" fill="url(#rxUnder)"/>`;
    if (big) {
      // the hammock between the two left posts
      const h0 = -0.46 * wd + 9, h1 = -0.16 * wd - 9, hm = (h0 + h1) / 2;
      g += `<path d="M${f(h0)},-130Q${f(hm)},-62 ${f(h1)},-130" stroke="${T("#c8a868")}" stroke-width="2.2" fill="none"/>
        <path d="M${f(h0 + 12)},-116Q${f(hm)},-44 ${f(h1 - 12)},-116Q${f(hm)},-72 ${f(h0 + 12)},-116Z" fill="${T(o.cloth2 ?? "#3a6ac8")}" ${ln(1.6)}/>
        <path d="M${f(h0 + 22)},-106Q${f(hm)},-54 ${f(h1 - 22)},-106" stroke="${T("#e8e0c8")}" stroke-width="2" fill="none" opacity=".55"/>`;
      // firewood stacked end-on, the water jar with its dipper
      for (let k = 0; k < 3; k++) for (let j = 0; j < 4 - k; j++) { const cx = -0.14 * wd + j * 12 + k * 6, cy = -6 - k * 10.5;
        g += `<circle cx="${f(cx)}" cy="${f(cy)}" r="5.6" fill="${T(j % 2 ? "#b8885a" : "#a8784a")}" stroke="${T("#4a3020")}" stroke-width="1.4"/><circle cx="${f(cx)}" cy="${f(cy)}" r="2" fill="none" stroke="${T("#7a5232")}" stroke-width="1"/>`; }
      g += `<g transform="translate(${f(0.07 * wd)},0)"><ellipse cx="0" cy="2" rx="26" ry="5" fill="#000" opacity=".3"/>
        <path d="M-15,0Q-31,-22 -18,-44H18Q31,-22 15,0Z" fill="${T("#6a3a22")}" ${ln(1.6)}/><ellipse cx="0" cy="-44" rx="18" ry="4.5" fill="${T("#2a160c")}" ${ln(1.4)}/>
        <path d="M-18,-28Q0,-21 18,-28" stroke="${T("#c89a4a")}" stroke-width="2" fill="none" opacity=".8"/><path d="M-10,-40Q-17,-24 -10,-8" stroke="#fff" stroke-width="2.4" opacity=".16" fill="none"/>
        <path d="M-9,-47Q0,-39 9,-47Z" fill="${T("#c8ccd0")}" ${ln(1)}/></g>`;
      // the bamboo bench (แคร่) between the right posts, a sticky-rice basket on it
      const b0 = 0.16 * wd + 12, b1 = 0.46 * wd - 12;
      g += `<path d="M${f(b0 + 4)},-40V0M${f(b1 - 4)},-40V0" stroke="${T("#7a5a2e")}" stroke-width="5"/><rect x="${f(b0)}" y="-46" width="${f(b1 - b0)}" height="9" fill="${T("#d8b870")}" ${ln(1.6)}/>`;
      for (let k = 0; b0 + 5 + k * 9 < b1 - 2; k++) g += `<path d="M${f(b0 + 5 + k * 9)},-45v7" stroke="${T("#a88a48")}" stroke-width="1.4"/>`;
      g += `<g transform="translate(${f(b0 + 22)},-46)"><path d="M-8,0L-6,-15H6L8,0Z" fill="${T("#c8a058")}" ${ln(1.2)}/><path d="M-9,-15H9" stroke="${T("#8a6a30")}" stroke-width="3"/></g>`;
    }
    // the front posts: grain, a lit edge, a concrete footing
    [-0.46, -0.16, 0.16, 0.46].forEach((t) => { const px = t * wd;
      g += `<rect x="${f(px - 7)}" y="-150" width="14" height="150" fill="${post}"/><rect x="${f(px - 7)}" y="-150" width="14" height="150" fill="url(#rxPost)"/>
        <path d="M${f(px - 2)},-142V-14M${f(px + 3)},-122V-34" stroke="${dk(post, 0.45)}" stroke-width="1.3" opacity=".75"/>
        <rect x="${f(px - 7)}" y="-150" width="14" height="150" fill="none" ${ln(2.4)}/><rect x="${f(px - 10)}" y="-7" width="20" height="9" rx="2" fill="${T("#a8a498")}" ${ln(1.4)}/>`; });
    if (big) g += `<g transform="translate(${f(0.16 * wd + 8)},-138)"><path d="M0,0V8" stroke="${T("#3a2a1a")}" stroke-width="1.4"/><path d="M-8,8Q-11,28 -4,42H4Q11,28 8,8Z" fill="${T("#c8a058")}" ${ln(1.3)}/><path d="M-9,15H9M-9,22H9M-8,29H8M-6,36H6" stroke="${T("#8a6a30")}" stroke-width="1.1"/></g>`;
    // the floor beam with its joist ends
    g += `<rect x="${-wd / 2}" y="-176" width="${wd}" height="28" fill="${beam}" ${ln(2.4)}/><path d="M${-wd / 2 + 3},-171H${wd / 2 - 3}" stroke="${lt(beam, 0.25)}" stroke-width="2.4" opacity=".7"/>
      <path d="M${-wd / 2 + 3},-152H${wd / 2 - 3}" stroke="${dk(beam, 0.4)}" stroke-width="3" opacity=".6"/>`;
    for (let k = 0; -wd / 2 + 12 + k * 30 < wd / 2 - 8; k++) g += `<rect x="${f(-wd / 2 + 12 + k * 30)}" y="-148" width="8" height="8" fill="${dk(beam, 0.35)}"/>`;
    // the wall: vertical planks in shifting tones, a knot here and there, the eave's shadow along the top
    const wx0 = -wd / 2 + 10, ww = wd - 20;
    for (let k = 0; k * 22 < ww; k++) { const tone = [0, 0.08, -0.07, 0.04, -0.03][(k * 3 + Math.floor(r() * 5)) % 5], w2 = Math.min(22, ww - k * 22);
      g += `<rect x="${f(wx0 + k * 22)}" y="-300" width="${f(w2)}" height="126" fill="${tone >= 0 ? lt(wall, tone) : dk(wall, -tone)}"/>`;
      if (k) g += `<path d="M${f(wx0 + k * 22)},-298V-176" stroke="${dk(wall, 0.4)}" stroke-width="2"/>`;
      if (big && r() < 0.3) g += `<ellipse cx="${f(wx0 + k * 22 + 6 + r() * 10)}" cy="${f(-282 + r() * 90)}" rx="2.2" ry="3.6" fill="${dk(wall, 0.32)}"/>`; }
    g += `<path d="M${f(wx0)},-236H${f(wx0 + ww)}" stroke="${dk(wall, 0.3)}" stroke-width="3" opacity=".5"/><rect x="${f(wx0)}" y="-300" width="${f(ww)}" height="126" fill="url(#rxWallSh)"/>
      <rect x="${f(wx0)}" y="-300" width="${f(ww)}" height="126" fill="none" ${ln(2.4)}/>`;
    // the doorway in its frame
    const dx = -wd * 0.12, dw = wd * 0.18;
    g += `<rect x="${f(dx - 5)}" y="-281" width="${f(dw + 10)}" height="95" fill="${T("#5a3a22")}" ${ln(2)}/><rect x="${f(dx)}" y="-276" width="${f(dw)}" height="90" fill="#1a100a" ${ln(2)}/>
      <path d="M${f(dx)},-276h${f(dw)}l-6,10h${f(-dw + 12)}Z" fill="#000" opacity=".4"/>`;
    // the window: shutters swung open, bars, lit warm at night
    const wx = wd * 0.2, wW = wd * 0.14, sw = wd * 0.065;
    g += `<path d="M${f(wx)},-272L${f(wx - sw)},-266V-212L${f(wx)},-214Z" fill="${T("#7a4e30")}" ${ln(1.8)}/><path d="M${f(wx + wW)},-272L${f(wx + wW + sw)},-266V-212L${f(wx + wW)},-214Z" fill="${T("#6a4228")}" ${ln(1.8)}/>
      <path d="M${f(wx - sw * 0.5)},-262V-216M${f(wx + wW + sw * 0.5)},-262V-216" stroke="${T("#4a2e1a")}" stroke-width="1.6" opacity=".7"/>
      <rect x="${f(wx)}" y="-270" width="${f(wW)}" height="54" fill="${lit ? "#ffd890" : T("#140c08")}"/>
      ${lit ? `<rect x="${f(wx)}" y="-270" width="${f(wW)}" height="18" fill="#ffefc0" opacity=".6"/>` : `<rect x="${f(wx)}" y="-270" width="${f(wW)}" height="14" fill="#000" opacity=".35"/>`}
      ${[1, 2, 3].map((k) => `<path d="M${f(wx + (wW * k) / 4)},-270V-216" stroke="${lit ? "#7a4a22" : T("#3a2414")}" stroke-width="2.4"/>`).join("")}
      <rect x="${f(wx)}" y="-270" width="${f(wW)}" height="54" fill="none" ${ln(2.2)}/><rect x="${f(wx - 4)}" y="-217" width="${f(wW + 8)}" height="5" fill="${dk(wall, 0.3)}" ${ln(1.2)}/>`;
    if (lit) g += `<ellipse cx="${f(wx + wW / 2)}" cy="-243" rx="${f(wW * 1.5)}" ry="62" fill="url(#rxWinGlow)" style="mix-blend-mode:screen"/>`;
    // a hat and a sticky-rice basket hung on nails beside the door
    if (big) g += `<g transform="translate(${f(-wd * 0.3)},-262)"><path d="M0,-6V0" stroke="${LINE}" stroke-width="1.4"/><path d="M-22,8Q0,-12 22,8Q0,2 -22,8Z" fill="${T("#d8b870")}" ${ln(1.4)}/><path d="M-12,4Q0,-6 12,4" stroke="${T("#a8884a")}" stroke-width="1.2" fill="none"/></g>
      <g transform="translate(${f(-wd * 0.3)},-226)"><path d="M0,-8V0" stroke="${LINE}" stroke-width="1.2"/><path d="M-9,0L-7,18H7L9,0Z" fill="${T("#c8a058")}" ${ln(1.2)}/><path d="M-9,6H9M-8,12H8" stroke="${T("#8a6a30")}" stroke-width="1"/></g>`;
    // the roof: corrugated zinc, light on the left slope, rust where the rain runs off, barge boards, the eave board
    const rl = -wd / 2 - 30, rr = wd / 2 + 30;
    g += `<path d="M${f(rl)},-292L0,-400L${f(rr)},-292Z" fill="${roof}"/><path d="M${f(rl)},-292L0,-400V-292Z" fill="#fff" opacity=".1"/><path d="M${f(rr)},-292L0,-400V-292Z" fill="#000" opacity=".16"/>`;
    for (let k = 0; k <= 16; k++) { const bx = rl + (k * (rr - rl)) / 16, tx = (k - 8) * 3;
      g += `<path d="M${f(bx)},-293L${f(tx)},-396" stroke="${dk(roof, 0.32)}" stroke-width="2" opacity=".55"/><path d="M${f(bx + 4)},-293L${f(tx + 0.6)},-396" stroke="${lt(roof, 0.3)}" stroke-width="1.2" opacity=".45"/>`; }
    for (let k = 0; k < 5; k++) { const u = 0.12 + k * 0.19 + (r() - 0.5) * 0.06, bx = rl + u * (rr - rl), tx = (u * 16 - 8) * 3, q = 0.14 + r() * 0.12;
      g += `<path d="M${f(bx)},-294L${f(bx + (tx - bx) * q)},${f(-294 - 102 * q)}" stroke="${mix(roof, "#a8643a", 0.65)}" stroke-width="5" opacity=".45" stroke-linecap="round"/>`; }
    g += `<path d="M${f(rl)},-292L0,-400L${f(rr)},-292" stroke="${T("#5a3a22")}" stroke-width="7" fill="none" stroke-linejoin="round"/><path d="M${f(rl)},-292L0,-400L${f(rr)},-292Z" fill="none" ${ln(2.6)}/>
      <path d="M${f(rl - 4)},-291H${f(rr + 4)}" stroke="${LINE}" stroke-width="5"/><path d="M-12,-397L0,-409L12,-397" stroke="${T("#4a3426")}" stroke-width="5" fill="none" stroke-linejoin="round"/>`;
    // the ladder (same lean as before), a cloth over the rail
    g += `<g transform="translate(${-wd / 2 - 40},0) rotate(-24)"><path d="M0,0V-170M30,0V-170" stroke="${LINE}" stroke-width="10" stroke-linecap="round"/><path d="M0,0V-170M30,0V-170" stroke="${beam}" stroke-width="6.5"/>${[1, 2, 3, 4, 5].map((k) => `<path d="M0,${-k * 30}H30" stroke="${LINE}" stroke-width="8"/><path d="M1,${-k * 30}H29" stroke="${lt(beam, 0.15)}" stroke-width="5"/>`).join("")}</g>
      <path d="M${-wd / 2 + 20},-182q30,30 60,0" fill="${T(o.cloth ?? "#c8403a")}" opacity=".92"/><path d="M${-wd / 2 + 28},-178q22,18 44,0M${-wd / 2 + 36},-176q14,10 28,0" stroke="${T("#f0e0b0")}" stroke-width="1.6" fill="none" opacity=".6"/>`;
    if (o.granary) { const gw = T("#a06a3a"), gr = T("#8a8a7a");
      g += `<g transform="translate(${wd / 2 + 120},0)"><ellipse cx="0" cy="4" rx="100" ry="14" fill="url(#rxAO)"/>
        <rect x="-56" y="-90" width="10" height="90" fill="${post}" ${ln(1.6)}/><rect x="46" y="-90" width="10" height="90" fill="${post}" ${ln(1.6)}/>
        <rect x="-64" y="-200" width="128" height="112" fill="${gw}"/><rect x="-64" y="-200" width="128" height="112" fill="url(#rxWeave)"/><rect x="-64" y="-200" width="128" height="112" fill="url(#rxWallSh)"/>
        <rect x="-64" y="-200" width="128" height="112" fill="none" ${ln(2.4)}/><path d="M-64,-144H64" stroke="${dk(gw, 0.4)}" stroke-width="3"/>
        <rect x="-16" y="-178" width="32" height="30" fill="${dk(gw, 0.55)}" ${ln(1.6)}/>
        <path d="M-88,-196L0,-266L88,-196Z" fill="${gr}"/><path d="M-88,-196L0,-266V-196Z" fill="#fff" opacity=".1"/><path d="M88,-196L0,-266V-196Z" fill="#000" opacity=".16"/>
        ${Array.from({ length: 9 }, (_, k) => `<path d="M${-84 + k * 21},-197L${(k - 4) * 2},-262" stroke="${dk(gr, 0.3)}" stroke-width="1.6" opacity=".55"/>`).join("")}
        <path d="M-88,-196L0,-266L88,-196Z" fill="none" ${ln(2.4)}/></g>`; }
    return g + "</g>";
  };

  // ---------------------------------------------------------------- the yard, lit like a lived-in night
  const glow = (x, y, r, op, col = "#ffcf7a") => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="${col}" opacity="${op}" filter="url(#rxBlur)" style="mix-blend-mode:screen"/>`;
  Sets.rupYardRich = (L, o = {}) => {
    const id = o.id || "ry", night = (o.time || "day") === "night";
    Sets.rupYard(L, { ...o, id });
    if (!night) return;
    // the house draws its own lit window (with bars) now: drop the old flat overlay rect
    L.set.querySelectorAll(`rect[x="642"][y="902"]`).forEach((n) => n.remove());
    // above the darkness: the bulb's halo under the floor, the window's spill, a hurricane lantern on the well frame
    put(L.glow, `<g id="${id}-bulbL">${glow(560, 1060, 90, 0.5)}<ellipse cx="560" cy="1236" rx="260" ry="56" fill="#ffcf7a" opacity=".12" style="mix-blend-mode:screen"/></g>` + glow(671, 936, 120, 0.38));
    const wx = (o.wellX ?? 250) + 120, wy = (o.wellY ?? 1560) - 250;
    put(L.set, `<g transform="translate(${wx},${wy})"><path d="M0,0V26" stroke="#1a1a1a" stroke-width="2"/><rect x="-14" y="26" width="28" height="36" rx="6" fill="#ffd27a" stroke="#3a2a14" stroke-width="3"/><path d="M-16,26H16M-16,62H16" stroke="#3a2a14" stroke-width="4"/></g>`);
    put(L.glow, glow(wx, wy + 44, 70, 0.55) + `<ellipse cx="${wx - 50}" cy="${(o.wellY ?? 1560) + 40}" rx="210" ry="48" fill="#ffcf7a" opacity=".1" style="mix-blend-mode:screen"/>`);
  };

  // ---------------------------------------------------------------- the new angles (RupStill) as sets
  // ids inside each piece get the shot's prefix, so a scene used in two shots never resolves to the other shot's gradients
  const scope = (m, p) => { const ids = new Set(); m.replace(/id="([^"]+)"/g, (_, i) => ids.add(i));
    return m.replace(/id="([^"]+)"/g, (_, i) => `id="${p}-${i}"`).replace(/url\(#([^)]+)\)/g, (a, i) => (ids.has(i) ? `url(#${p}-${i})` : a)).replace(/href="#([^"]+)"/g, (a, i) => (ids.has(i) ? `href="#${p}-${i}"` : a)); };
  RupX.scope = scope;
  // Sets.rupStill(L, {id, scene})  a screen-sized still: drone-dusk · drone-moon · measure · measure-note
  Sets.rupStill = (L, o = {}) => { const id = o.id || "rs", sc = RupStill.scene(o.scene || "drone-moon"); put(L.set, scope(`<defs>${sc.defs}</defs>${sc.body}`, id)); };
  // Sets.rupDepth(L, {id})  the tall dive world (1080 × 7400): sky → rim → paddy soil → laterite → sandy clay → limestone → the cave and
  // its groundwater, the pump's pipe going down into it. Frame it with fr(x, y, s); RupX.depth holds SURF / CAVE0 / WT.
  // o.eyes: two amber glints in the side passage at the far end of the water channel (#id-eyes), off until RupX.depthEyes fades them in
  Sets.rupDepth = (L, o = {}) => { const id = o.id || "rd", w = RupStill.world();
    RupX.depth = { H: w.H, SURF: w.SURF, CAVE0: w.CAVE0, WT: w.WT };
    let g = scope(`<defs>${w.defs}</defs>${w.body}`, id);
    if (o.eyes !== false) g += RupX.eyes(`${id}-eyes`, 1012, w.WT + 196, 1);
    put(L.set, g); };
  // a ghost trace: two amber slit-pupil eyes in the dark (#id, #id-l, #id-r), off until RupX.eyesLife fades them in, blinks once, fades out
  RupX.eyes = (id, x, y, s = 1, gap = 30) => `<g id="${id}" opacity="0" transform="translate(${f(x)},${f(y)}) scale(${s})"><circle cx="${gap / 2}" cy="0" r="30" fill="#ffb23a" opacity=".32" filter="url(#rxBlurS)"/>
    <g id="${id}-l"><ellipse cx="0" cy="0" rx="8" ry="5.5" fill="#ffcf5a"/><ellipse cx="0" cy="0" rx="2" ry="5" fill="#1a0e04"/></g>
    <g id="${id}-r"><ellipse cx="${gap}" cy="3" rx="8" ry="5.5" fill="#ffcf5a"/><ellipse cx="${gap}" cy="3" rx="2" ry="5" fill="#1a0e04"/></g></g>`;
  RupX.eyesLife = (tl, id, t0, hold = 1.2) => {
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, t0);
    tl.fromTo([`#${id}-l`, `#${id}-r`], { scaleY: 1, transformOrigin: "50% 50%" }, { scaleY: 0.08, duration: 0.09, yoyo: true, repeat: 1, ease: "power1.inOut", immediateRender: false }, t0 + hold * 0.55);
    tl.to(`#${id}`, { opacity: 0, duration: 0.35, ease: "power2.in", immediateRender: false }, t0 + hold);
  };
  RupX.depthEyes = (tl, id, t0, hold = 1.2) => RupX.eyesLife(tl, `${id}-eyes`, t0, hold);
  // a ghost trace: something long and dark slides along the ground under the house, through the bulb's pool of light (#id)
  RupX.underShadow = (L, id, x, y, len = 520) => put(L.set, `<g id="${id}" opacity="0" transform="translate(0,${f(y)})"><g transform="translate(${f(x)},0)"><path d="M0,0C${f(len * 0.12)},-18 ${f(len * 0.22)},16 ${f(len * 0.36)},0S${f(len * 0.6)},-18 ${f(len * 0.74)},0S${f(len * 0.92)},14 ${f(len)},2" stroke="#040308" stroke-width="40" fill="none" stroke-linecap="round" filter="url(#rpBlur3)" opacity=".86"/>
    <path d="M${f(len - 6)},-14c34,-6 62,6 70,16c-24,12 -52,12 -70,0z" fill="#040308" opacity=".86" filter="url(#rpBlur3)"/></g></g>`);
  RupX.underShadowLife = (tl, id, t0, dur, dx = 700, flick = []) => {
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power1.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}`, { x: 0 }, { x: dx, duration: dur, ease: "sine.inOut", immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.4, ease: "power1.in", immediateRender: false }, t0 + dur - 0.4);
    // the light it passes under stutters: two dips, never a flash (V1b)
    flick.forEach((sel) => { [0.32, 0.5].forEach((u, k) => tl.fromTo(sel, { opacity: 1 }, { opacity: 0.25, duration: 0.07, yoyo: true, repeat: 1 + k, ease: "none", immediateRender: false }, t0 + dur * u)); });
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
    clip.insertAdjacentHTML("beforeend", `<g id="${id}-vil">${village()}</g><g id="${id}-naga">${nagaPuppet(id)}</g>` +
      // o.water: the same body as groundwater, hidden until RupX.legendDrain turns the naga into water and drains it away
      (o.water ? `<path id="${id}-water" d="M120,1320C300,1400 700,1400 830,1260S800,1020 560,1040S200,1010 280,900S560,800 690,800" stroke="#3f8fd0" stroke-width="80" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="0"/>
        <path id="${id}-waterHi" d="M120,1320C300,1400 700,1400 830,1260S800,1020 560,1040S200,1010 280,900S560,800 690,800" stroke="#bfe4ff" stroke-width="10" fill="none" stroke-linecap="round" opacity="0" pathLength="100" stroke-dasharray="6 7" transform="translate(-6,-14)"/>` : ""));
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
  // "the hungry naga is the groundwater that went away": the black puppet turns to water, which drains off head-first back into the earth
  RupX.legendDrain = (tl, id, t, dur = 1.6) => {
    tl.to(`#${id}-naga`, { opacity: 0, duration: 0.35, ease: "power1.inOut", immediateRender: false }, t);
    tl.fromTo([`#${id}-water`, `#${id}-waterHi`], { opacity: 0 }, { opacity: 0.92, duration: 0.35, ease: "power1.inOut", immediateRender: false }, t);
    tl.fromTo(`#${id}-water`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": 100 }, duration: dur, ease: "power1.in", immediateRender: false }, t + 0.45);
    tl.to(`#${id}-waterHi`, { opacity: 0, duration: dur * 0.7, ease: "power1.in", immediateRender: false }, t + 0.45);
    tl.fromTo(`#${id}-waterHi`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -26 }, duration: dur, ease: "none", immediateRender: false }, t);
  };
  RupX.legendLife = (tl, id, t0, dur) => {
    tl.fromTo(`#${id}-naga`, { rotation: -1.2, svgOrigin: "520 1300" }, { rotation: 1.2, svgOrigin: "520 1300", duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: Math.ceil(dur / 1.6), immediateRender: false }, t0);
    tl.fromTo(`#${id}-eyeglow`, { opacity: 0.15 }, { opacity: 0.85, duration: 0.6, ease: "power2.out", immediateRender: false }, t0 + Math.min(2.2, dur * 0.3));
  };
})();
