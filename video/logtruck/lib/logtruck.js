// "ท่อนซุงลงเขา" world kit (เลน B · 1 พ.ย. 2569): a long mountain descent in the late-afternoon sun, a log truck ahead with its
// load chained down, our car between it and a big vehicle glued to our bumper (an LPG tanker — the F6 twist, planted in the mirror).
// No real brands, no real plates. Seeded RNG only.
//   Lt.logEnd(cx, cy, r, seed, o)   a log's cut end: rough bark ring, pale sapwood, growth rings, radial checks, pith
//   Lt.logSide(x, y, len, r, seed)  a log seen from the side (left end at x): bark cylinder with a lit top, the cut end on the right
//   Lt.truckRear(id, x, y, s, o)    the log truck from behind (origin = ground under the centre): dual wheels, mud flaps, the striped
//                                   under-run bar, tail lights (#id-brake glow), the deck and the stakes, the log ends stacked 4-3-2-1,
//                                   two chains over the stack (#id-ch0 front, #id-ch1 back; each in halves #id-ch0L / #id-ch0R for the snap),
//                                   the loose top log (#id-top), red rag on the long log (class flag), brake smoke at the wheels (#id-smoke)
//   Lt.truckSide(id, x, y, s, o)    the log truck in profile facing right: cab, deck, long logs over the back, stakes, chains (#id-chs0…)
//   Lt.tankerFront(id, x, y, s, o)  the tanker's face: wide chrome grille, headlights (#id-hl), the white tank's round shoulder over the cab,
//                                   the orange plate "1075" (o.plate false hides it), the red flammable-gas diamond
//   Lt.tankerSide(id, x, y, s, o)   the tanker in profile facing right (EP.2's reveal)
//   Lt.carSide(id, x, y, s, o)      our small hatchback in profile facing right (mint green), o.brake the brake lights
//   Sets.ltPOV(L, o)                the driver's seat: the descent ahead, the truck's back (o.truck {x,y,s}), the cabin, the mirror with the
//                                   tanker's grille filling it (o.mirror 0..1 how close; o.mirror false = empty road), hands on the wheel,
//                                   o.sign {x,y,s,kind,km} a roadside sign coming up. ids: ${id}-truck, ${id}-mirImg, ${id}-road, ${id}-sun
//   Sets.ltSlope(L, o)              the descent in profile: the hillside, the road sloping down to the right, guardrail, valley haze;
//                                   o.convoy draws truck / car / tanker on the road (ids ${id}-truck, ${id}-car, ${id}-tank)
//   Sets.ltMirror(L, o)             the rear-view mirror filling the frame: o.show "tanker" | "glare", ${id}-img to scale / move
//   Sets.ltWheel(L, o)              close on the truck's rear wheels and the chain binder, smoke (#id-smoke), the binder lever (#id-lever)
//   Lt.life(tl, scope, t0, dur)     looping motion: road flow, flags, smoke, sun flicker through trees, mirror judder
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const OUT2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Lt = (window.Lt = window.Lt || {});

  Sets.DEFS += `
    <linearGradient id="ltSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fa6d6"/><stop offset=".55" stop-color="#bcd6e6"/><stop offset=".85" stop-color="#f6dcb0"/><stop offset="1" stop-color="#ffd59a"/></linearGradient>
    <linearGradient id="ltSkyLate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f78b0"/><stop offset=".5" stop-color="#c49aa8"/><stop offset=".85" stop-color="#f2b07a"/><stop offset="1" stop-color="#ffcf86"/></linearGradient>
    <radialGradient id="ltSun"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset=".18" stop-color="#fff2c4" stop-opacity=".9"/><stop offset=".5" stop-color="#ffd890" stop-opacity=".35"/><stop offset="1" stop-color="#ffc870" stop-opacity="0"/></radialGradient>
    <linearGradient id="ltRidge1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb2c8"/><stop offset="1" stop-color="#c9d2da"/></linearGradient>
    <linearGradient id="ltRidge2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f8aa0"/><stop offset="1" stop-color="#9fb0bc"/></linearGradient>
    <linearGradient id="ltRidge3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#47705e"/><stop offset="1" stop-color="#6e8c78"/></linearGradient>
    <linearGradient id="ltHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbe6c4" stop-opacity="0"/><stop offset=".6" stop-color="#fbe6c4" stop-opacity=".55"/><stop offset="1" stop-color="#fbe6c4" stop-opacity=".1"/></linearGradient>
    <linearGradient id="ltRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8288"/><stop offset="1" stop-color="#4a4e54"/></linearGradient>
    <linearGradient id="ltRoadS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a5e64"/><stop offset="1" stop-color="#6c7076"/></linearGradient>
    <linearGradient id="ltRock" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a6a58"/><stop offset=".6" stop-color="#9c8a72"/><stop offset="1" stop-color="#b8a486"/></linearGradient>
    <linearGradient id="ltBark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6242"/><stop offset=".35" stop-color="#6a4428"/><stop offset="1" stop-color="#3a2414"/></linearGradient>
    <radialGradient id="ltWood" cx=".46" cy=".44" r=".6"><stop offset="0" stop-color="#f6d8a4"/><stop offset=".6" stop-color="#e2b47a"/><stop offset="1" stop-color="#b98450"/></radialGradient>
    <linearGradient id="ltSteel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b949c"/><stop offset=".5" stop-color="#5c646c"/><stop offset="1" stop-color="#363c42"/></linearGradient>
    <linearGradient id="ltCab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a8ac0"/><stop offset=".6" stop-color="#2f6a9e"/><stop offset="1" stop-color="#1f4a70"/></linearGradient>
    <linearGradient id="ltTank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="#eef1f3"/><stop offset=".7" stop-color="#c4cbd2"/><stop offset="1" stop-color="#8e979f"/></linearGradient>
    <linearGradient id="ltChrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f7fa"/><stop offset=".45" stop-color="#9aa4ae"/><stop offset=".55" stop-color="#5e6870"/><stop offset="1" stop-color="#c8d0d8"/></linearGradient>
    <linearGradient id="ltMint" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b6ecd8"/><stop offset=".55" stop-color="#7cc9ae"/><stop offset="1" stop-color="#4c9a80"/></linearGradient>
    <linearGradient id="ltGlassD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6a8aa4"/><stop offset=".5" stop-color="#2e4256"/><stop offset="1" stop-color="#1a2836"/></linearGradient>
    <linearGradient id="ltDash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3632"/><stop offset=".25" stop-color="#26231f"/><stop offset="1" stop-color="#141210"/></linearGradient>
    <linearGradient id="ltLiner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#262320"/><stop offset="1" stop-color="#3a3530"/></linearGradient>
    <radialGradient id="ltRed"><stop offset="0" stop-color="#ff6a4a" stop-opacity="1"/><stop offset=".35" stop-color="#ff2a1a" stop-opacity=".55"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltHead"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset=".25" stop-color="#fff6d8" stop-opacity=".75"/><stop offset="1" stop-color="#fff0c0" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltSmoke"><stop offset="0" stop-color="#e8e4de" stop-opacity=".85"/><stop offset=".6" stop-color="#cfcac2" stop-opacity=".4"/><stop offset="1" stop-color="#bcb6ae" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltDust"><stop offset="0" stop-color="#d8bf98" stop-opacity=".9"/><stop offset=".6" stop-color="#c8a87a" stop-opacity=".4"/><stop offset="1" stop-color="#b8986a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltSpark"><stop offset="0" stop-color="#fffbe0"/><stop offset=".3" stop-color="#ffd04a" stop-opacity=".8"/><stop offset="1" stop-color="#ff8a1a" stop-opacity="0"/></radialGradient>
    <linearGradient id="ltGlare" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>`;

  // ---------------------------------------------------------------- pieces
  const rough = (r, R, n, j) => {   // a closed rough circle path (bark edge)
    let d = "";
    for (let k = 0; k < n; k++) { const a = (k / n) * Math.PI * 2, rr = R * (1 + (r() - 0.5) * j); d += `${k ? "L" : "M"}${f1(Math.cos(a) * rr)},${f1(Math.sin(a) * rr)}`; }
    return d + "Z";
  };
  Lt.logEnd = (cx, cy, R, seed = 1, o = {}) => {
    const r = mk(seed * 977 + 13), ox = (r() - 0.5) * R * 0.25, oy = (r() - 0.5) * R * 0.25;
    let g = `<g transform="translate(${f1(cx)},${f1(cy)})${o.rot ? ` rotate(${o.rot})` : ""}">`;
    g += `<path d="${rough(r, R, 22, 0.1)}" fill="#4a2e1a" ${OUT3}/>`;
    g += `<circle r="${f1(R * 0.84)}" fill="#efcf98"/><circle r="${f1(R * 0.78)}" fill="url(#ltWood)"/>`;
    for (let k = 1; k <= 4; k++) g += `<circle cx="${f1(ox * (1 - k / 5))}" cy="${f1(oy * (1 - k / 5))}" r="${f1(R * 0.78 * k / 5)}" fill="none" stroke="#b47c46" stroke-width="${f1(Math.max(1.2, R * 0.022))}" opacity=".55"/>`;
    for (let k = 0; k < 3; k++) { const a = r() * Math.PI * 2, l = R * (0.3 + r() * 0.4); g += `<path d="M${f1(ox + Math.cos(a) * R * 0.12)},${f1(oy + Math.sin(a) * R * 0.12)}L${f1(ox + Math.cos(a) * l)},${f1(oy + Math.sin(a) * l)}" stroke="#7a4e2a" stroke-width="${f1(Math.max(1.5, R * 0.03))}" stroke-linecap="round" opacity=".8"/>`; }
    g += `<circle cx="${f1(ox)}" cy="${f1(oy)}" r="${f1(R * 0.05)}" fill="#8a5a30"/>`;
    g += `<path d="M${f1(-R * 0.62)},${f1(-R * 0.38)}A${f1(R * 0.72)},${f1(R * 0.72)} 0 0 1 ${f1(R * 0.2)},${f1(-R * 0.7)}" stroke="#fff6e0" stroke-width="${f1(R * 0.06)}" fill="none" opacity=".45" stroke-linecap="round"/>`;
    g += `<path d="M${f1(R * 0.7)},${f1(R * 0.1)}A${f1(R * 0.8)},${f1(R * 0.8)} 0 0 1 ${f1(-R * 0.1)},${f1(R * 0.78)}" stroke="#2a1608" stroke-width="${f1(R * 0.08)}" fill="none" opacity=".35"/>`;
    return g + `</g>`;
  };
  Lt.logSide = (x, y, len, R, seed = 1) => {
    const r = mk(seed * 331 + 7);
    let g = `<g transform="translate(${f1(x)},${f1(y)})"><path d="M0,${-R}H${len}A${f1(R * 0.38)},${R} 0 0 1 ${len},${R}H0A${f1(R * 0.38)},${R} 0 0 1 0,${-R}Z" fill="url(#ltBark)" ${OUT3}/>`;
    for (let k = 0; k < len / 40; k++) { const px = 20 + r() * (len - 40), py = -R * 0.8 + r() * R * 1.5; g += `<path d="M${f1(px)},${f1(py)}h${f1(30 + r() * 70)}" stroke="#2e1a0c" stroke-width="${f1(2 + r() * 3)}" opacity=".5" stroke-linecap="round"/>`; }
    g += `<path d="M6,${f1(-R * 0.62)}H${len - 6}" stroke="#c09468" stroke-width="${f1(R * 0.16)}" opacity=".55" stroke-linecap="round"/>`;
    g += `<ellipse cx="${len}" cy="0" rx="${f1(R * 0.38)}" ry="${R}" fill="#efcf98" ${OUT3}/><ellipse cx="${len}" cy="0" rx="${f1(R * 0.3)}" ry="${f1(R * 0.8)}" fill="url(#ltWood)"/>`;
    return g + `</g>`;
  };
  // a chain along a polyline: dark links with a bright glint, drawn as two dashed strokes offset by half a link
  const chain = (d, w = 12) => `<path d="${d}" stroke="${INK}" stroke-width="${w + 5}" fill="none" stroke-linejoin="round"/><path d="${d}" stroke="#7d868e" stroke-width="${w}" fill="none" stroke-dasharray="${w * 1.6} ${w * 0.5}" stroke-linejoin="round"/><path d="${d}" stroke="#d6dde2" stroke-width="${w * 0.35}" fill="none" stroke-dasharray="${w * 0.8} ${w * 1.3}" stroke-linejoin="round" opacity=".9"/>`;
  Lt.chain = chain;
  const dual = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-62" y="-150" width="124" height="150" rx="26" fill="#17181a" ${OUT}/>${[-30, 0, 30].map((dx) => `<path d="M${dx},-146V-4" stroke="#2c2e31" stroke-width="5"/>`).join("")}<rect x="-62" y="-150" width="124" height="22" rx="10" fill="#2c2e31" opacity=".8"/></g>`;
  const smokeCloud = (x, y, s, seed) => {
    const r = mk(seed);
    return `<g transform="translate(${x},${y}) scale(${s})">${Array.from({ length: 6 }, (_, k) => `<g class="puff" data-k="${k}"><circle cx="${f1((r() - 0.5) * 90)}" cy="${f1(-k * 34 - r() * 20)}" r="${f1(50 + k * 16)}" fill="url(#ltSmoke)"/></g>`).join("")}</g>`;
  };

  // the log truck from behind: origin = the ground under the centre, ~700 units wide, ~880 tall at s 1
  Lt.truckRear = (id, x, y, s, o = {}) => {
    const r = mk(o.seed || 41);
    let g = `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${s})"><ellipse cx="0" cy="6" rx="390" ry="34" fill="#1a1612" opacity=".5"/>`;
    // the chassis behind the wheels, the axle shadow
    g += `<rect x="-300" y="-200" width="600" height="70" fill="#1e1f22" ${OUT}/><rect x="-120" y="-170" width="240" height="40" fill="#2a2b2e"/>`;
    g += dual(-230, 0) + dual(230, 0);
    g += `<g>${[-180, 180].map((mx) => `<path d="M${mx - 52},-150H${mx + 52}V-24Q${mx},-14 ${mx - 52},-24Z" fill="#101113" ${OUT3}/><path d="M${mx - 40},-134H${mx + 40}" stroke="#3a3c40" stroke-width="5"/>`).join("")}</g>`;
    // under-run bar (red / white), tail lights, the plate (blank: no real numbers)
    g += `<rect x="-300" y="-128" width="600" height="34" fill="#f2f0ea" ${OUT}/>${Array.from({ length: 8 }, (_, k) => `<path d="M${-300 + k * 75},-128h38l-20,34h-38z" fill="#d8352a"/>`).join("")}<rect x="-300" y="-128" width="600" height="34" fill="none" ${OUT}/>`;
    g += `<rect x="-62" y="-200" width="124" height="54" rx="6" fill="#f2e6a8" ${OUT3}/><path d="M-44,-180h88M-36,-162h72" stroke="#6a5a2a" stroke-width="6" stroke-linecap="round" opacity=".55"/>`;
    g += [-1, 1].map((sd) => `<g><rect x="${sd < 0 ? -344 : 270}" y="-232" width="74" height="44" rx="8" fill="#5a0e0a" ${OUT3}/><rect x="${sd < 0 ? -336 : 278}" y="-226" width="26" height="32" rx="5" fill="#ff4a2a"/><rect x="${sd < 0 ? -306 : 308}" y="-226" width="26" height="32" rx="5" fill="#ffb22a"/></g>`).join("");
    // the deck and the stakes
    g += `<rect x="-340" y="-262" width="680" height="40" fill="url(#ltSteel)" ${OUT}/><path d="M-340,-246H340" stroke="#a8b0b8" stroke-width="3" opacity=".6"/>`;
    // the log ends: rows 4 / 3 / 2 / 1 with a little jitter (the top one is #id-top, it comes loose)
    const rows = [[4, 76], [3, 74], [2, 72]], ends = [];
    let yy = -262;
    rows.forEach(([n, R], ri) => {
      const cy = yy - R + ri * 8;
      for (let k = 0; k < n; k++) ends.push([(k - (n - 1) / 2) * (R * 2 - 6) + (r() - 0.5) * 10, cy + (r() - 0.5) * 8, R + (r() - 0.5) * 10]);
      yy = cy - R * 0.62 + 8;
    });
    g += ends.map(([cx, cy, R], k) => Lt.logEnd(cx, cy, R, (o.seed || 41) + k)).join("");
    const topY = yy - 64;
    g += [-1, 1].map((sd) => `<g><rect x="${sd * 318 - 12}" y="${topY - 30}" width="24" height="${-262 - topY + 30}" fill="url(#ltSteel)" ${OUT3}/><rect x="${sd * 318 - 16}" y="${topY - 40}" width="32" height="16" rx="4" fill="#3a3f45" ${OUT3}/></g>`).join("");
    // chains: from the left stake bottom, over the stack's shoulder, down to the binder on the right
    const cy0 = -262, peak = topY + 22, chainD = (dy, sx) => `M${-318 * sx},${cy0 - 8 + dy}C${-330 * sx},${peak + 120 + dy} ${-170 * sx},${peak + dy} 0,${peak - 6 + dy}`;
    const half = (k, side, dy) => `<g id="${id}-ch${k}${side}">${chain(side === "L" ? chainD(dy, 1) : chainD(dy, -1))}</g>`;
    g += `<g id="${id}-ch1" opacity=".85">${half(1, "L", 70)}${half(1, "R", 70)}</g>`;
    // the loose top log sits between the chains
    g += `<g id="${id}-top">${Lt.logEnd(0, topY + 10, 70, (o.seed || 41) + 20)}</g>`;
    g += `<g id="${id}-ch0">${half(0, "L", 0)}${half(0, "R", 0)}</g>`;
    // the binder (ratchet) on the right stake
    g += `<g id="${id}-binder" transform="translate(300,-300)"><rect x="-14" y="-40" width="28" height="80" rx="8" fill="#c88a1a" ${OUT3}/><path d="M0,-30L44,-80" stroke="${INK}" stroke-width="13" stroke-linecap="round"/><path d="M0,-30L44,-80" stroke="#e0a42a" stroke-width="8" stroke-linecap="round"/></g>`;
    // the red rag tied on the longest log (bottom right)
    g += `<g transform="translate(${f1(ends[3][0] + 30)},${f1(ends[3][1] + 40)})"><path d="M0,0V60" stroke="#3a2a1a" stroke-width="4"/><path class="flag" d="M0,8Q40,0 70,16Q44,32 0,40Z" fill="#d8301e" ${OUT2}/></g>`;
    g += `<g id="${id}-smoke" opacity="${o.smoke ?? 0}">${smokeCloud(-230, -60, 1, 5)}${smokeCloud(230, -60, 1, 9)}</g>`;
    g += `<g id="${id}-brake" opacity="${o.brake ?? 0}">${[-307, 307].map((bx) => `<circle cx="${bx}" cy="-210" r="120" fill="url(#ltRed)"/>`).join("")}</g>`;
    return g + `</g>`;
  };

  // the log truck in profile facing right (origin = ground under the rear axle), ~1500 long at s 1
  Lt.truckSide = (id, x, y, s, o = {}) => {
    let g = `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})"><ellipse cx="520" cy="6" rx="900" ry="30" fill="#1a1612" opacity=".45"/>`;
    g += `<rect x="-260" y="-200" width="1360" height="56" fill="#1e1f22" ${OUT}/>`;
    // the cab (generic, no badge): blue, a sun visor, the window with the driver's arm (#id-arm) on the sill
    g += `<g><path d="M1040,-150V-560Q1040,-600 1080,-600H1260Q1310,-600 1330,-540L1380,-330Q1392,-290 1392,-250V-150Z" fill="url(#ltCab)" ${OUT}/>
      <path d="M1100,-560H1250Q1286,-560 1300,-520L1336,-380H1100Z" fill="url(#ltGlassD)" ${OUT3}/><path d="M1086,-600H1300L1310,-620H1076Z" fill="#1f4a70" ${OUT3}/>
      <rect x="1060" y="-330" width="300" height="20" fill="#9cc4e6" opacity=".5"/><rect x="1352" y="-280" width="44" height="36" rx="8" fill="#fff6d0" ${OUT3}/>
      <path d="M1360,-200H1400" stroke="${INK}" stroke-width="8"/><rect x="1040" y="-210" width="360" height="60" fill="#2a2b2e" ${OUT3}/>
      <g id="${id}-arm" opacity="${o.arm ?? 0}"><path d="M1180,-390Q1150,-470 1100,-500" stroke="${INK}" stroke-width="40" stroke-linecap="round" fill="none"/><path d="M1180,-390Q1150,-470 1100,-500" stroke="#c88a5a" stroke-width="32" stroke-linecap="round" fill="none"/><circle cx="1096" cy="-508" r="24" fill="#c88a5a" ${OUT3}/></g></g>`;
    // the deck, stakes, logs (long, over the back), chains wrapping down to the deck
    g += `<rect x="-320" y="-250" width="1340" height="50" fill="url(#ltSteel)" ${OUT}/>`;
    const logs = [[-250, -300, 1260, 50], [-200, -390, 1180, 48], [-300, -476, 1230, 46], [-170, -560, 1120, 44], [-230, -640, 1100, 42]];
    g += logs.map(([lx, ly, len, R], k) => `<g${k === logs.length - 1 ? ` id="${id}-top"` : ""}>${Lt.logSide(lx, ly, len, R, k + 3)}</g>`).join("");
    g += [-180, 220, 620, 960].map((sx) => `<rect x="${sx}" y="-690" width="22" height="440" fill="url(#ltSteel)" ${OUT3}/>`).join("");
    g += [0, 1].map((k) => `<g id="${id}-chs${k}">${chain(`M${80 + k * 520},-250L${80 + k * 520},-690`, 11)}</g>`).join("");
    g += `<g transform="translate(-300,-460)"><path d="M0,0V60" stroke="#3a2a1a" stroke-width="4"/><path class="flag" d="M0,8Q-40,0 -70,16Q-44,32 0,40Z" fill="#d8301e" ${OUT2}/></g>`;
    g += [0, 160, 1250].map((wx) => `<g transform="translate(${wx},0)"><circle cy="-70" r="78" fill="#17181a" ${OUT}/><circle cy="-70" r="40" fill="#6a7178" ${OUT3}/><g class="spin"><path d="M-28,-70H28M0,-98V-42" stroke="${INK}" stroke-width="6"/></g></g>`).join("");
    g += `<g id="${id}-smoke" opacity="${o.smoke ?? 0}">${smokeCloud(0, -40, 0.9, 3)}${smokeCloud(160, -40, 0.9, 7)}</g>`;
    g += `<g id="${id}-brake" opacity="${o.brake ?? 0}"><circle cx="-320" cy="-226" r="90" fill="url(#ltRed)"/></g><rect x="-336" y="-240" width="22" height="30" rx="5" fill="#ff4a2a" ${OUT2}/>`;
    return g + `</g>`;
  };

  // the LPG tanker's face (origin = ground under the centre), ~640 wide at s 1
  Lt.tankerFront = (id, x, y, s, o = {}) => {
    let g = `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${s})"><ellipse cx="0" cy="6" rx="380" ry="30" fill="#141210" opacity=".5"/>`;
    // the white tank's round shoulder rising over the cab, its red band
    g += `<path d="M-330,-840Q-330,-1080 0,-1090Q330,-1080 330,-840Z" fill="url(#ltTank)" ${OUT}/><path d="M-318,-900Q0,-930 318,-900" stroke="#d8352a" stroke-width="18" fill="none"/>`;
    // the cab
    g += `<path d="M-300,-140V-820Q-300,-860 -260,-860H260Q300,-860 300,-820V-140Z" fill="#f2f2ee" ${OUT}/>`;
    g += `<path d="M-262,-820H262V-560H-262Z" fill="url(#ltGlassD)" ${OUT3}/><path d="M-250,-806L-60,-806L-220,-580H-250Z" fill="#fff" opacity=".18"/><path d="M0,-820V-560" stroke="${INK}" stroke-width="5"/>`;
    g += `<rect x="-280" y="-880" width="560" height="26" rx="8" fill="#ffb22a" ${OUT3}/>${[-200, -100, 0, 100, 200].map((lx) => `<circle cx="${lx}" cy="-867" r="7" fill="#fff2b0"/>`).join("")}`;
    // the chrome grille, headlights, bumper, the plate (orange hazard plate under it)
    g += `<rect x="-230" y="-520" width="460" height="250" rx="16" fill="url(#ltChrome)" ${OUT}/>${Array.from({ length: 7 }, (_, k) => `<path d="M-214,${-500 + k * 34}H214" stroke="#4a525a" stroke-width="8"/>`).join("")}`;
    g += `<g id="${id}-hl">${[-1, 1].map((sd) => `<g><rect x="${sd < 0 ? -292 : 196}" y="-330" width="96" height="58" rx="12" fill="#fffbe8" ${OUT3}/><circle cx="${sd * 244}" cy="-301" r="18" fill="#fff"/></g>`).join("")}</g>`;
    g += `<rect x="-310" y="-250" width="620" height="90" rx="14" fill="#c8ccd0" ${OUT}/><rect x="-300" y="-160" width="600" height="20" fill="#2a2b2e"/>`;
    if (o.plate !== false) g += `<g id="${id}-plate"><rect x="-96" y="-238" width="192" height="68" rx="4" fill="#ff8a1a" ${OUT3}/><path d="M-90,-204H90" stroke="${INK}" stroke-width="4"/><text x="0" y="-212" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}">23</text><text x="0" y="-178" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}">1075</text></g>`;
    if (o.dia) g += `<g id="${id}-dia" transform="translate(200,-700) rotate(45)"><rect x="-56" y="-56" width="112" height="112" fill="#d8301e" stroke="#fff" stroke-width="8"/><rect x="-56" y="-56" width="112" height="112" fill="none" ${OUT3}/></g><g transform="translate(200,-700)"><path d="M0,-34C14,-14 22,-4 14,12C10,22 -10,22 -14,12C-20,-2 -6,-10 0,-34Z" fill="#fff"/><text x="0" y="44" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="#fff">2</text></g>`;
    g += `<rect x="-300" y="-120" width="140" height="120" rx="26" fill="#17181a" ${OUT}/><rect x="160" y="-120" width="140" height="120" rx="26" fill="#17181a" ${OUT}/>`;
    g += `<g id="${id}-beam" opacity="${o.beam ?? 0}">${[-1, 1].map((sd) => `<circle cx="${sd * 244}" cy="-301" r="200" fill="url(#ltHead)"/>`).join("")}</g>`;
    return g + `</g>`;
  };
  // the tanker in profile facing right (origin = ground under the rear axle) ~1500 long
  Lt.tankerSide = (id, x, y, s, o = {}) => {
    let g = `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})"><ellipse cx="520" cy="6" rx="900" ry="30" fill="#141210" opacity=".45"/>`;
    g += `<rect x="-240" y="-200" width="1360" height="56" fill="#1e1f22" ${OUT}/>`;
    if (!o.cabOnly) {
    g += `<path d="M-260,-560Q-330,-560 -330,-420Q-330,-280 -260,-280H940Q1010,-280 1010,-420Q1010,-560 940,-560Z" fill="url(#ltTank)" ${OUT}/>`;
    g += `<path d="M-300,-470H990" stroke="#d8352a" stroke-width="22"/><path d="M-310,-500Q340,-560 980,-500" stroke="#fff" stroke-width="10" fill="none" opacity=".7"/>`;
    g += `<text x="340" y="-370" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#d8352a">ไวไฟ · ห้ามสูบบุหรี่</text>`;
    g += `<g transform="translate(-120,-380) rotate(45)"><rect x="-46" y="-46" width="92" height="92" fill="#d8301e" stroke="#fff" stroke-width="6"/></g><g transform="translate(-120,-380)"><path d="M0,-28C12,-12 18,-3 12,10C8,18 -8,18 -12,10C-16,-2 -5,-8 0,-28Z" fill="#fff"/></g>`;
    g += `<g><rect x="-60" y="-262" width="160" height="56" rx="4" fill="#ff8a1a" ${OUT3}/><path d="M-56,-234H96" stroke="${INK}" stroke-width="3"/><text x="20" y="-240" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${INK}">23</text><text x="20" y="-212" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="${INK}">1075</text></g>`;
    }
    g += `<g><path d="M1040,-150V-560Q1040,-600 1080,-600H1260Q1310,-600 1330,-540L1380,-330Q1392,-290 1392,-250V-150Z" fill="#f2f2ee" ${OUT}/><path d="M1100,-560H1250Q1286,-560 1300,-520L1336,-380H1100Z" fill="url(#ltGlassD)" ${OUT3}/><rect x="1352" y="-280" width="44" height="36" rx="8" fill="#fff6d0" ${OUT3}/><rect x="1040" y="-210" width="360" height="60" fill="#2a2b2e" ${OUT3}/><path d="M1076,-610H1300" stroke="#ffb22a" stroke-width="16" stroke-linecap="round"/></g>`;
    g += [0, 160, 1250].map((wx) => `<g transform="translate(${wx},0)"><circle cy="-70" r="78" fill="#17181a" ${OUT}/><circle cy="-70" r="40" fill="#6a7178" ${OUT3}/><g class="spin"><path d="M-28,-70H28M0,-98V-42" stroke="${INK}" stroke-width="6"/></g></g>`).join("");
    g += `<g id="${id}-smoke" opacity="${o.smoke ?? 0}">${smokeCloud(0, -40, 0.9, 13)}${smokeCloud(160, -40, 0.9, 17)}</g>`;
    g += `<g id="${id}-hl" opacity="${o.hl ?? 1}"><circle cx="1400" cy="-262" r="130" fill="url(#ltHead)"/></g>`;
    return g + `</g>`;
  };
  // our hatchback in profile facing right (origin = ground under the middle), ~760 long at s 1
  Lt.carSide = (id, x, y, s, o = {}) => {
    let g = `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})"><ellipse cx="0" cy="6" rx="400" ry="24" fill="#141210" opacity=".5"/>`;
    g += `<path d="M-380,-60Q-392,-200 -340,-230L-250,-250Q-200,-370 -60,-380H120Q220,-372 290,-260L360,-236Q396,-222 392,-140V-60Q392,-24 360,-24H-350Q-380,-26 -380,-60Z" fill="url(#ltMint)" ${OUT}/>`;
    g += `<path d="M-230,-252Q-180,-350 -70,-358H40V-252Z" fill="url(#ltGlassD)" ${OUT3}/><path d="M60,-358H116Q200,-352 262,-262L266,-252H60Z" fill="url(#ltGlassD)" ${OUT3}/>`;
    g += `<path d="M50,-360V-36M-240,-250V-40" stroke="${INK}" stroke-width="4"/><path d="M-60,-220h40M120,-220h40" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><path d="M-370,-140H384" stroke="#fff" stroke-width="6" opacity=".35"/>`;
    g += `<rect x="370" y="-210" width="26" height="34" rx="8" fill="#fff6d0" ${OUT3}/><rect x="-392" y="-212" width="22" height="46" rx="6" fill="#a8261c" ${OUT3}/>`;
    g += [-240, 250].map((wx) => `<g transform="translate(${wx},-34)"><circle r="70" fill="#17181a" ${OUT}/><circle r="38" fill="#a8b0b8" ${OUT3}/><g class="spin"><path d="M-26,0H26M0,-26V26" stroke="${INK}" stroke-width="6"/></g></g>`).join("");
    g += `<g id="${id}-brake" opacity="${o.brake ?? 0}"><circle cx="-384" cy="-190" r="70" fill="url(#ltRed)"/></g>`;
    return g + `</g>`;
  };

  // ---------------------------------------------------------------- backgrounds
  const ridge = (r, y, amp, n, x0 = -900, x1 = 2000) => {
    let d = `M${x0},${y}`;
    for (let k = 0; k <= n; k++) d += `L${f1(x0 + (x1 - x0) * k / n)},${f1(y - amp * (0.4 + r() * 0.6) * (k % 2 ? 1 : 0.55))}`;
    return d + `L${x1},2800H${x0}Z`;
  };
  const canopy = (r, x0, x1, y, n, col, hi, sz = 60) => Array.from({ length: n }, () => { const x = x0 + r() * (x1 - x0), yy = y + r() * 40, R = sz * (0.7 + r() * 0.7); return `<g><circle cx="${f1(x)}" cy="${f1(yy)}" r="${f1(R)}" fill="${col}"/><circle cx="${f1(x - R * 0.25)}" cy="${f1(yy - R * 0.3)}" r="${f1(R * 0.55)}" fill="${hi}" opacity=".7"/></g>`; }).join("");
  const sky = (L, r, o) => {
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#${o.late ? "ltSkyLate" : "ltSky"})"/>
      <g id="${o.id}-sun"><circle cx="${o.sunX ?? 160}" cy="${o.sunY ?? 420}" r="520" fill="url(#ltSun)"/><circle cx="${o.sunX ?? 160}" cy="${o.sunY ?? 420}" r="60" fill="#fffdf2"/></g>
      ${Array.from({ length: 5 }, () => `<g class="cloud" data-d="${f1(6 + r() * 10)}"><ellipse cx="${f1(-400 + r() * 1900)}" cy="${f1(80 + r() * 380)}" rx="${f1(160 + r() * 200)}" ry="${f1(30 + r() * 30)}" fill="#fff8ec" opacity=".55"/></g>`).join("")}`);
  };
  const ridges = (L, r, hz) => put(L.far, `<path d="${ridge(r, hz - 60, 260, 9)}" fill="url(#ltRidge1)"/><path d="${ridge(r, hz + 40, 220, 7)}" fill="url(#ltRidge2)"/><rect x="-900" y="${hz - 160}" width="2900" height="420" fill="url(#ltHaze)"/>`);

  // ---------------------------------------------------------------- the driver's seat
  // the road ahead bends gently left and drops away; the valley below on the right behind a guardrail; rock cut on the left
  Sets.ltPOV = function (L, o = {}) {
    const id = o.id || "lp", r = mk(o.seed || 211), HZ = 900, VX = o.vx ?? 600;
    sky(L, r, { id, late: o.late, sunX: o.sunX ?? 120, sunY: o.sunY ?? 520 });
    ridges(L, r, HZ - 60);
    // the valley floor far below with fields and haze; the near ridge (green) the road is cut into
    let far = `<path d="${ridge(r, HZ + 60, 120, 6)}" fill="url(#ltRidge3)"/>${canopy(r, 700, 2000, HZ + 40, 26, "#3e6a4e", "#7a9a6a", 44)}<rect x="-900" y="${HZ - 40}" width="2900" height="200" fill="url(#ltHaze)" opacity=".7"/>`;
    put(L.far, far);
    // the road: asphalt wedge to the vanishing point, the yellow centre line flowing toward us, the guardrail on the right, rock on the left
    let s = `<path d="M-900,${HZ + 20}L${VX - 40},${HZ + 4}Q${VX - 160},${HZ + 120} -300,1500H-900Z" fill="url(#ltRock)"/>`;
    s += canopy(r, -900, VX - 160, HZ - 40, 22, "#2f5a3e", "#6f9a5e", 70);
    s += `<path d="M${VX - 40},${HZ + 4}L${VX + 30},${HZ + 4}L1700,1500H-300Q${VX - 160},${HZ + 120} ${VX - 40},${HZ + 4}Z" fill="url(#ltRoad)"/>`;
    s += `<path d="M${VX - 30},${HZ + 6}Q${VX - 140},${HZ + 120} -250,1500" stroke="#f2f0e4" stroke-width="10" fill="none" opacity=".8"/><path d="M${VX + 26},${HZ + 6}L1650,1500" stroke="#f2f0e4" stroke-width="10" fill="none" opacity=".8"/>`;
    // the guardrail: posts flowing toward us + the beam
    s += `<path d="M${VX + 40},${HZ - 6}L1900,1330" stroke="#c8ccd0" stroke-width="16" fill="none"/><path d="M${VX + 40},${HZ - 14}L1900,1300" stroke="#eef0f2" stroke-width="5" fill="none"/>`;
    put(L.far, s);
    // flowing pieces (class flow, Mok.life drives them): centre dashes, guardrail posts, roadside reflector posts on the left
    const flow = (from, to, p, k, n, body) => `<g class="flow" data-from="${from}" data-to="${to}" data-p="${p}" data-o="${(k / n).toFixed(3)}" transform="translate(${from.split(",")[0]},${from.split(",")[1]}) scale(${from.split(",")[2]})">${body}</g>`;
    let fl = "";
    for (let k = 0; k < 6; k++) fl += flow(`${VX},${HZ + 8},0.04`, `${VX - 420},1560,1.5`, 1.1, k, 6, `<path d="M-9,-70L9,-70L13,70L-13,70Z" fill="#f2c230"/>`);
    for (let k = 0; k < 5; k++) fl += flow(`${VX + 44},${HZ - 4},0.04`, `1500,1400,1.6`, 1.3, k, 5, `<rect x="-10" y="-90" width="20" height="120" fill="#9aa2aa"/><rect x="-14" y="-96" width="28" height="30" fill="#eef0f2"/>`);
    for (let k = 0; k < 4; k++) fl += flow(`${VX - 60},${HZ + 2},0.04`, `-500,1500,1.7`, 1.5, k + 0.5, 4, `<rect x="-9" y="-110" width="18" height="110" rx="4" fill="#eef0f2"/><rect x="-9" y="-96" width="18" height="16" fill="#ff9a3a"/>`);
    put(L.mid, `<g id="${id}-road">${fl}</g>`);
    // an optional roadside sign (positioned by the shot; kind "km" = distance board, "ramp" = escape ramp, "gear" = low gear)
    if (o.sign) put(L.mid, `<g id="${id}-sign">${Lt.sign(o.sign.x ?? 160, o.sign.y ?? 1100, o.sign.s ?? 0.6, o.sign)}</g>`);
    // the truck
    const T = o.truck || {};
    put(L.set, `<g id="${id}-truckW">${o.truck === false ? "" : Lt.truckRear(`${id}-truck`, T.x ?? 560, T.y ?? 1330, T.s ?? 0.62, T)}</g>`);
    // a loose log lying across the road (the one that fell): ${id}-loose, centred on its own origin; shots move it
    if (o.loose) put(L.set, `<g id="${id}-loose" transform="translate(${o.loose.x ?? 540},${o.loose.y ?? 1300}) scale(${o.loose.s ?? 1})" opacity="${o.loose.op ?? 1}"><ellipse cx="0" cy="70" rx="300" ry="26" fill="#1a1612" opacity=".35" class="lsh"/><g class="lroll">${Lt.logSide(-260, 0, 520, 62, 11)}</g></g>`);
    // sun dapple through the windscreen
    put(L.set, `<g id="${id}-dapple" opacity=".5">${Array.from({ length: 6 }, () => `<ellipse class="dap" cx="${f1(-100 + r() * 1300)}" cy="${f1(500 + r() * 900)}" rx="${f1(200 + r() * 200)}" ry="${f1(60 + r() * 80)}" fill="#ffe8b8" opacity=".14"/>`).join("")}</g>`);
    // the cabin: roof liner, A-pillars, sun visors, the mirror (its image = the tanker's grille), the garland hanging under it, dash, wheel
    let c = `<path d="M-900,-600H2000V330Q1500,270 1160,270L1010,350Q540,300 70,350L-80,270Q-420,270 -900,330Z" fill="url(#ltLiner)"/>`;
    c += `<path d="M-80,270L70,350L-80,1560H-900V330Q-420,270 -80,270Z" fill="#2a2622"/><path d="M1160,270L1010,350L1160,1560H2000V330Q1500,270 1160,270Z" fill="#2a2622"/>`;
    c += `<path d="M70,350L-80,1560" stroke="#3e3832" stroke-width="10"/><path d="M1010,350L1160,1560" stroke="#3e3832" stroke-width="10"/>`;
    c += `<path d="M90,330H420Q440,330 440,350V420Q300,440 100,400Z" fill="#4a443c" ${OUT3}/>`;
    // the mirror: frame + clip + image
    const MX = o.mirX ?? 700, MY = o.mirY ?? 310, MW = 300, MH = 104;
    c += `<path d="M${MX},${MY - MH / 2 - 40}V${MY - MH / 2}" stroke="#1a1816" stroke-width="18"/>`;
    c += `<clipPath id="${id}-mclip"><rect x="${MX - MW / 2}" y="${MY - MH / 2}" width="${MW}" height="${MH}" rx="22"/></clipPath>`;
    c += `<rect x="${MX - MW / 2 - 12}" y="${MY - MH / 2 - 12}" width="${MW + 24}" height="${MH + 24}" rx="30" fill="#141210" ${OUT}/>`;
    const mir = o.mirror === false ? "" : Lt.tankerFront(`${id}-mt`, 0, 0, 1, { plate: true, beam: o.mirBeam ?? 0 });
    const near = o.mirror === false ? 0 : (o.mirror ?? 0.6);
    c += `<g clip-path="url(#${id}-mclip)"><rect x="${MX - MW / 2}" y="${MY - MH / 2}" width="${MW}" height="${MH}" fill="#c8b89a"/>`;
    c += `<rect x="${MX - MW / 2}" y="${MY - MH / 2}" width="${MW}" height="${MH * 0.55}" fill="#e8d8b4"/><path d="M${MX - MW / 2},${MY + 10}L${MX + MW / 2},${MY + 6}" stroke="#7a7e84" stroke-width="40"/>`;
    c += `<g id="${id}-mirImg" transform="translate(${MX},${f1(MY + 52 + near * 120)}) scale(${f1(0.08 + near * 0.32)})">${mir}</g>`;
    c += `<rect x="${MX - MW / 2}" y="${MY - MH / 2}" width="${MW}" height="${MH}" fill="url(#ltGlare)"/></g>`;
    c += `<rect x="${MX - MW / 2}" y="${MY - MH / 2}" width="${MW}" height="${MH}" rx="22" fill="none" stroke="#3a3632" stroke-width="5"/>`;
    // the jasmine garland with a red rose and ribbons, hanging from the mirror stem (class swing)
    c += `<g transform="translate(${MX - 40},${MY + MH / 2 + 4})"><g class="swing" data-a="5">${Array.from({ length: 9 }, (_, k) => `<circle cx="${f1(Math.sin(k * 0.7) * 6)}" cy="${12 + k * 16}" r="10" fill="#f6f2e0" ${OUT2}/>`).join("")}<circle cx="0" cy="160" r="18" fill="#d8302a" ${OUT2}/><path d="M-8,176L-16,250M8,176L16,250" stroke="#e8c030" stroke-width="7" stroke-linecap="round"/></g></g>`;
    // dashboard + the wheel (right-hand drive) with the driver's hands
    c += `<path d="M-900,1480Q540,1380 2000,1480V2800H-900Z" fill="url(#ltDash)"/><path d="M-900,1480Q540,1380 2000,1480" stroke="#4a443c" stroke-width="10" fill="none"/>`;
    c += `<path d="M-900,1440Q540,1350 2000,1440" stroke="#ffe8b8" stroke-width="3" fill="none" opacity=".25"/>`;
    put(L.set, ""); put(L.act, c);
    const SLV = o.sleeve || "#3a6ea8", CUF = o.cuff || "#5a8ec8";
    const grip = (x, y, side) => {
      const ex = side < 0 ? -40 : 1160, ey = 2360, d = Math.hypot(ex - x, ey - y), ux = (ex - x) / d, uy = (ey - y) / d;
      return `<path d="M${x},${y}L${ex},${ey}" stroke="${INK}" stroke-width="134" stroke-linecap="round"/><path d="M${x},${y}L${ex},${ey}" stroke="${SLV}" stroke-width="124" stroke-linecap="round"/>
        <path d="M${f1(x + ux * 70)},${f1(y + uy * 70)}L${f1(x + ux * 112)},${f1(y + uy * 112)}" stroke="${INK}" stroke-width="134"/><path d="M${f1(x + ux * 74)},${f1(y + uy * 74)}L${f1(x + ux * 108)},${f1(y + uy * 108)}" stroke="${CUF}" stroke-width="124"/>
        <g transform="translate(${x},${y}) rotate(${side < 0 ? -25 : 25})">${Hands.fist({ r: 84 })}</g>`;
    };
    let w = `<g id="${id}-wheel"><g class="steer" transform="translate(720,1860)"><circle r="330" fill="none" stroke="#0e0d0c" stroke-width="66"/><circle r="330" fill="none" stroke="#2c2926" stroke-width="50"/><path d="M-316,30Q0,110 316,30M0,100V330" stroke="#1c1a18" stroke-width="72" fill="none"/><circle r="100" fill="#1c1a18" ${OUT}/><circle r="36" fill="#2c2926"/>
      <g transform="translate(-306,-100) rotate(-25)">${""}</g></g>`;
    w += `<g id="${id}-gripL">${grip(430, 1700, -1)}</g><g id="${id}-gripR">${grip(1010, 1700, 1)}</g></g>`;
    put(L.fg, w);
    put(L.glow, `<g id="${id}-glare" opacity="${o.glare ?? 0.6}"><path d="M-200,400L400,400L-200,1300Z" fill="#fff6dc" opacity=".08"/><circle cx="${o.sunX ?? 120}" cy="${o.sunY ?? 520}" r="300" fill="url(#ltSun)" opacity=".5"/></g>`);
  };

  // a roadside sign (Thai DOH style, generic text; no real place names): kind "km" green distance board, "slope" yellow warning,
  // "gear" white rectangular, "ramp" green escape-ramp board with arrow
  Lt.sign = (x, y, s, o = {}) => {
    const k = o.kind || "km";
    let g = `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><rect x="-10" y="-300" width="20" height="300" fill="#c8ccd0" ${OUT3}/>`;
    if (k === "slope") g += `<g transform="translate(0,-420)"><rect x="-150" y="-150" width="300" height="300" rx="24" fill="#ffc81e" transform="rotate(45)" ${OUT}/><path d="M-90,60L90,-40V60Z" fill="${INK}"/><text x="40" y="-6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="${INK}">${o.pct || "12%"}</text></g>`;
    else if (k === "gear") g += `<g transform="translate(0,-420)"><rect x="-220" y="-130" width="440" height="260" rx="18" fill="#fff" stroke="#d8302a" stroke-width="14"/><text x="0" y="-30" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="66" fill="${INK}">ลงเขา</text><text x="0" y="62" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="66" fill="#d8302a">ใช้เกียร์ต่ำ</text></g>`;
    else if (k === "ramp") g += `<g transform="translate(0,-440)"><rect x="-260" y="-150" width="520" height="300" rx="20" fill="#1e7a46" stroke="#fff" stroke-width="10"/><text x="0" y="-50" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#fff">ทางหนีภัย</text><text x="-30" y="62" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="80" fill="#ffd84a">${o.km || "1 กม."}</text><path d="M170,80V10H140L190,-40L240,10H210V80Z" fill="#fff"/></g>`;
    else g += `<g transform="translate(0,-420)"><rect x="-260" y="-140" width="520" height="280" rx="20" fill="#1e7a46" stroke="#fff" stroke-width="10"/><text x="0" y="-36" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#fff">${o.top || "ทางลงเขาลาดชัน"}</text><text x="0" y="74" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="86" fill="#ffd84a">${o.km || "อีก 8 กม."}</text></g>`;
    return g + `</g>`;
  };

  // ---------------------------------------------------------------- the descent in profile
  // the road runs from upper left down to the right at o.slope degrees (default 9); hillside above, valley haze below
  Sets.ltSlope = function (L, o = {}) {
    const id = o.id || "ls", r = mk(o.seed || 223), A = (o.slope ?? 9) * Math.PI / 180, G = o.ground ?? 1300, tn = Math.tan(A);
    const yAt = (x) => G + (x - 540) * tn;
    sky(L, r, { id, late: o.late, sunX: o.sunX ?? 120, sunY: o.sunY ?? 360 });
    ridges(L, r, 760);
    put(L.far, `<path d="${ridge(r, 900, 140, 8)}" fill="url(#ltRidge3)"/>${canopy(r, -900, 2000, 880, 40, "#3e6a4e", "#7a9a6a", 46)}<rect x="-900" y="760" width="2900" height="300" fill="url(#ltHaze)" opacity=".8"/>`);
    // the hillside the road is cut into (above the road), the road band, the guardrail on the valley edge (below), the drop
    const X0 = -1600, X1 = 2800;
    let s = `<path d="M${X0},${f1(yAt(X0) - 900)}L${X1},${f1(yAt(X1) - 700)}L${X1},${f1(yAt(X1) - 40)}L${X0},${f1(yAt(X0) - 40)}Z" fill="url(#ltRock)"/>`;
    s += canopy(r, X0, X1, 0, 0, "", "");
    for (let k = 0; k < 40; k++) { const x = X0 + r() * (X1 - X0), yy = yAt(x) - 120 - r() * 520, R = 50 + r() * 60; s += `<g><circle cx="${f1(x)}" cy="${f1(yy)}" r="${f1(R)}" fill="#2f5a3e"/><circle cx="${f1(x - R * 0.3)}" cy="${f1(yy - R * 0.3)}" r="${f1(R * 0.55)}" fill="#6f9a5e" opacity=".75"/></g>`; }
    let road = `<path d="M${X0},${f1(yAt(X0) - 60)}L${X1},${f1(yAt(X1) - 60)}L${X1},${f1(yAt(X1) + 60)}L${X0},${f1(yAt(X0) + 60)}Z" fill="url(#ltRoadS)"/>`;
    road += `<path d="M${X0},${f1(yAt(X0) - 60)}L${X1},${f1(yAt(X1) - 60)}" stroke="#8a7a62" stroke-width="10"/><path d="M${X0},${f1(yAt(X0) + 10)}L${X1},${f1(yAt(X1) + 10)}" stroke="#f2c230" stroke-width="8" stroke-dasharray="80 60"/>`;
    s += `<path d="M${X0},${f1(yAt(X0) + 60)}L${X1},${f1(yAt(X1) + 60)}L${X1},2800L${X0},2800Z" fill="#4e6a4a"/>`;
    for (let k = 0; k < 30; k++) { const x = X0 + r() * (X1 - X0), yy = yAt(x) + 200 + r() * 600, R = 60 + r() * 70; s += `<g><circle cx="${f1(x)}" cy="${f1(yy)}" r="${f1(R)}" fill="#355e44"/><circle cx="${f1(x - R * 0.3)}" cy="${f1(yy - R * 0.3)}" r="${f1(R * 0.5)}" fill="#7a9a6a" opacity=".6"/></g>`; }
    put(L.set, s);
    // the guardrail in front of the vehicles (fg): beam + posts
    let gr = `<path d="M${X0},${f1(yAt(X0) + 40)}L${X1},${f1(yAt(X1) + 40)}" stroke="#c8ccd0" stroke-width="22"/><path d="M${X0},${f1(yAt(X0) + 34)}L${X1},${f1(yAt(X1) + 34)}" stroke="#f2f4f6" stroke-width="6"/>`;
    for (let x = X0; x < X1; x += 220) gr += `<rect x="${x - 8}" y="${f1(yAt(x) + 30)}" width="16" height="90" fill="#9aa2aa"/>`;
    put(L.act, road);
    // the convoy (on the road line; rotated to the slope). o.convoy { truck: x, car: x, tank: x | false } in road x
    const C = o.convoy || {}, rot = (o.slope ?? 9);
    const at = (x, dy = 0) => `translate(${f1(x)},${f1(yAt(x) + dy)}) rotate(${rot})`;
    let v = "";
    // the id group carries no transform (shots slide it with x / y along the slope); the inner group sits it on the road
    if (C.tank !== false && C.tank != null) v += `<g id="${id}-tank"><g transform="${at(C.tank, 4)}">${Lt.tankerSide(`${id}-tk`, 0, 0, C.ts ?? 0.42, { smoke: C.tsmoke, cabOnly: C.cabOnly })}</g></g>`;
    if (C.car != null) v += `<g id="${id}-car"><g transform="${at(C.car, 4)}">${Lt.carSide(`${id}-c`, 0, 0, C.cs ?? 0.42, { brake: C.cbrake })}</g></g>`;
    if (C.truck != null) v += `<g id="${id}-truck"><g transform="${at(C.truck, 4)}">${Lt.truckSide(`${id}-t`, 0, 0, C.trs ?? 0.42, { smoke: C.smoke, brake: C.brake, arm: C.arm })}</g></g>`;
    put(L.act, v + `<g id="${id}-rail">${gr}</g>`);
  };
  Lt.slopeY = (o, x) => (o.ground ?? 1300) + (x - 540) * Math.tan((o.slope ?? 9) * Math.PI / 180);

  // ---------------------------------------------------------------- the mirror, filling the frame
  Sets.ltMirror = function (L, o = {}) {
    const id = o.id || "lm", r = mk(o.seed || 227);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#1c1916"/>`);
    put(L.far, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#ltLiner)"/><path d="M-900,1500Q540,1360 2000,1500V2800H-900Z" fill="#6a8aa4" opacity=".25"/>`);
    // the frame
    let s = `<rect x="-60" y="560" width="1200" height="560" rx="110" fill="#0e0d0c" ${OUT}/><path d="M540,560V300" stroke="#0e0d0c" stroke-width="60"/>`;
    s += `<clipPath id="${id}-clip"><rect x="-30" y="590" width="1140" height="500" rx="90"/></clipPath>`;
    s += `<g clip-path="url(#${id}-clip)"><rect x="-30" y="590" width="1140" height="500" fill="url(#ltSky)"/>`;
    s += `<path d="${ridge(r, 820, 120, 6, -60, 1160)}" fill="url(#ltRidge2)"/><path d="M-30,900L1110,880V1090H-30Z" fill="#6a6e74"/><path d="M540,890L540,1090" stroke="#f2c230" stroke-width="10" stroke-dasharray="30 30"/>`;
    s += `<g id="${id}-img" transform="translate(${o.ix ?? 540},${o.iy ?? 1290}) scale(${o.is ?? 1.05})">${o.show === "glare" ? "" : Lt.tankerFront(`${id}-t`, 0, 0, 1, { plate: o.plate !== false, beam: o.beam ?? 0 })}</g>`;
    s += `<g id="${id}-flash" opacity="0"><rect x="-30" y="590" width="1140" height="500" fill="#fffbe8"/></g>`;
    s += `<rect x="-30" y="590" width="1140" height="500" fill="url(#ltGlare)"/><path d="M80,620L360,620L120,1060H-30Z" fill="#fff" opacity=".07"/></g>`;
    s += `<rect x="-30" y="590" width="1140" height="500" rx="90" fill="none" stroke="#3a3632" stroke-width="10"/>`;
    put(L.set, s);
    put(L.fg, `<g transform="translate(380,1130)"><g class="swing" data-a="7">${Array.from({ length: 12 }, (_, k) => `<circle cx="${f1(Math.sin(k * 0.7) * 10)}" cy="${18 + k * 34}" r="22" fill="#f6f2e0" ${OUT3}/>`).join("")}<circle cx="0" cy="440" r="40" fill="#d8302a" ${OUT3}/><path d="M-16,476L-34,640M16,476L34,640" stroke="#e8c030" stroke-width="14" stroke-linecap="round"/></g></g>`);
  };

  // ---------------------------------------------------------------- close on the truck's back corner: wheels, binder, chain
  Sets.ltWheel = function (L, o = {}) {
    const id = o.id || "lw", r = mk(o.seed || 229);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#ltSky)"/>`);
    ridges(L, r, 700);
    put(L.far, `<rect x="-900" y="1500" width="2900" height="1400" fill="url(#ltRoad)"/>`);
    // the scroll of road texture under the wheel (class scroll)
    put(L.set, `<g class="scroll" data-w="400" data-v="${o.speed ?? 1400}">${Array.from({ length: 10 }, (_, k) => `<path d="M${-900 + k * 400},1640h160" stroke="#f2c230" stroke-width="14"/>`).join("")}</g>`);
    let s = `<g transform="translate(540,1560) scale(2.2)">${Lt.truckRear(`${id}-t`, 0, 0, 1, { smoke: 0, brake: o.brake ?? 0, seed: 43 })}</g>`;
    put(L.act, s);
    put(L.glow, `<g id="${id}-smoke" opacity="${o.smoke ?? 0.8}">${smokeCloud(40, 1450, 3.2, 21)}${smokeCloud(1040, 1450, 3.2, 23)}</g>`);
  };


  // ---------------------------------------------------------------- V11 coins (same 2.5D build and classes as HnFx.coin, so HnFx.pop / HnFx.life drive them)
  const tone = (hex, k) => { const n = parseInt(hex.slice(1), 16), c = [n >> 16, (n >> 8) & 255, n & 255].map((v) => Math.round(k > 0 ? v + (255 - v) * k : v * (1 + k))); return `#${c.map((v) => v.toString(16).padStart(2, "0")).join("")}`; };
  const CP = { gap: ["#d8f0c8", "#4a9a4a"], mirror: ["#cfe8f6", "#3a8ab8"], gear: ["#fde59a", "#e3a632"], nolift: ["#fbe0da", "#d8584a"], call: ["#fdeaea", "#d8302a"], orange: ["#ffe0c0", "#e8701a"], back: ["#e4e0f4", "#7a6ab8"] };
  let cdefs = "";
  for (const [n, [f, r]] of Object.entries(CP)) cdefs += `<radialGradient id="ltF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${tone(f, 0.7)}"/><stop offset=".55" stop-color="${f}"/><stop offset="1" stop-color="${tone(f, -0.12)}"/></radialGradient><linearGradient id="ltR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset=".6" stop-color="${tone(r, -0.15)}"/><stop offset="1" stop-color="${tone(r, -0.4)}"/></linearGradient>`;
  Sets.DEFS += cdefs + `<clipPath id="ltFace"><circle cx="60" cy="57" r="46"/></clipPath>`;
  const O = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const miniCar = (x, y, c) => `<g transform="translate(${x},${y})"><path d="M-16,0V-8Q-14,-14 -8,-15L-4,-22H8L13,-15Q18,-14 18,-8V0Z" fill="${c}" ${O(2)}/><circle cx="-8" cy="1" r="4" fill="${INK}"/><circle cx="10" cy="1" r="4" fill="${INK}"/></g>`;
  const miniTruck = (x, y) => `<g transform="translate(${x},${y})"><rect x="-26" y="-22" width="36" height="22" fill="#8a6242" ${O(2)}/><circle cx="-18" cy="-27" r="6" fill="#e2b47a" ${O(1.5)}/><circle cx="-6" cy="-27" r="6" fill="#e2b47a" ${O(1.5)}/><rect x="10" y="-20" width="16" height="20" rx="3" fill="#2f6a9e" ${O(2)}/><circle cx="-16" cy="1" r="4" fill="${INK}"/><circle cx="16" cy="1" r="4" fill="${INK}"/></g>`;
  const CPIC = {
    gap: () => [`<path d="M0,92H120" stroke="#6a6e74" stroke-width="22"/><path d="M8,92H112" stroke="#f2c230" stroke-width="2.5" stroke-dasharray="8 6"/>${miniCar(28, 90, "#7cc9ae")}${miniTruck(90, 90)}
      <g class="ltGapA"><path d="M46,66H70" stroke="#2fa864" stroke-width="5" stroke-linecap="round"/><path d="M46,60V72M70,60V72" stroke="#2fa864" stroke-width="4"/></g><g transform="translate(46,40)"><circle r="13" fill="#fff" ${O(2.5)}/><path d="M0,0V-8M0,0L6,3" stroke="${INK}" stroke-width="2.5" stroke-linecap="round"/><rect x="-3" y="-19" width="6" height="5" fill="${INK}"/></g><text x="76" y="50" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}">2</text>`, ""],
    mirror: () => [`<rect x="24" y="22" width="44" height="64" rx="10" fill="#2a2b2e" ${O(3)}/><rect x="29" y="27" width="34" height="54" rx="6" fill="#bfe0f4"/><circle cx="46" cy="50" r="10" fill="url(#hxSkin)" ${O(2)}/><circle cx="43" cy="48" r="1.6" fill="${INK}"/><circle cx="49" cy="48" r="1.6" fill="${INK}"/>
      <g class="ltEye"><path d="M74,64q14,-14 28,0q-14,14 -28,0Z" fill="#fff" ${O(2.5)}/><circle cx="88" cy="64" r="5" fill="${INK}"/></g><path d="M68,54h-6" stroke="${INK}" stroke-width="3"/>`, ""],
    gear: () => [`<rect x="36" y="80" width="48" height="16" rx="6" fill="#3a3632" ${O(3)}/><g class="ltShift"><path d="M60,82V44" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M60,82V44" stroke="#6a6e74" stroke-width="4" stroke-linecap="round"/><circle cx="60" cy="38" r="12" fill="#2a2b2e" ${O(3)}/><text x="60" y="43" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="15" fill="#ffd84a">L</text></g>
      <path d="M18,40l18,10M18,60l14,0" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/>`, ""],
    nolift: () => [`<path d="M0,96H120" stroke="#6a6e74" stroke-width="20"/><g class="ltRoll">${Lt.logSide(14, 78, 72, 14, 9)}</g><g class="ltReach"><circle cx="72" cy="48" r="11" fill="url(#hxSkin)" ${O(2.5)}/><path d="M72,59l-8,14" stroke="#3a6ea8" stroke-width="7" stroke-linecap="round"/></g>`,
      `<circle cx="60" cy="57" r="40" fill="none" stroke="#c8241a" stroke-width="8"/><path d="M32,85L88,29" stroke="#c8241a" stroke-width="8" stroke-linecap="round"/>`],
    call: () => [`<g class="ltRing"><rect x="40" y="24" width="40" height="72" rx="8" fill="#2a2a32" ${O(3)}/><rect x="45" y="32" width="30" height="52" rx="3" fill="#1e7a46"/><text x="60" y="56" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="12" fill="#fff">1586</text><text x="60" y="72" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="12" fill="#ffd84a">1193</text></g>
      <g class="ltWv"><path d="M88,40q8,8 0,16M94,34q14,14 0,28" stroke="#1e7a46" stroke-width="4" fill="none" stroke-linecap="round"/></g>`, ""],
    orange: () => [`<rect x="14" y="40" width="92" height="44" rx="4" fill="#ff8a1a" ${O(3.5)}/><path d="M16,62H104" stroke="${INK}" stroke-width="3"/><text x="60" y="58" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="16" fill="${INK}">23</text><text x="60" y="79" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="16" fill="${INK}">1075</text>
      <g class="ltFlame"><path d="M92,30C100,40 104,46 99,54C96,59 88,59 85,54C81,46 89,42 92,30Z" fill="#d8301e" ${O(2)}/></g>`, ""],
    back: () => [`<path d="M0,94H120" stroke="#6a6e74" stroke-width="18"/><g class="ltBack">${miniCar(64, 92, "#7cc9ae")}</g><path d="M36,58H16M16,58l10,-8M16,58l10,8" stroke="#7a6ab8" stroke-width="6" stroke-linecap="round" fill="none"/>
      <g transform="translate(96,70)"><rect x="-14" y="-26" width="28" height="26" fill="#ff8a1a" ${O(2)}/></g>`, ""],
  };
  Lt.coin = (name, x, y, s = 1, id = "") => {
    const [inside, top] = CPIC[name]();
    return `<g transform="translate(${x},${y}) scale(${s}) translate(-60,-60)"><g ${id ? `id="${id}"` : ""} class="hxCoin">
      <ellipse class="hxSh" cx="60" cy="122" rx="48" ry="9" fill="url(#hxSh)"/>
      <g class="hxBob"><g class="hxSq">
        <circle cx="60" cy="67" r="52" fill="url(#ltR-${name})" ${OUT}/><path d="M12,67A48,48 0 0 0 108,67" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
        <circle cx="60" cy="57" r="52" fill="url(#ltF-${name})" ${OUT}/><circle cx="60" cy="57" r="46" fill="none" stroke="url(#hxBev)" stroke-width="4"/>
        <g clip-path="url(#ltFace)">${inside}</g>${top || ""}
        <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle class="hxGlint" cx="53.5" cy="15.5" r="3" fill="#fff" opacity=".8"/>
      </g></g></g></g>`;
  };
  Lt.coinIn = (tl, id, t, dur) => {
    HnFx.pop(tl, id, t); HnFx.life(tl, id, t, dur);
    const r = document.getElementById(id); if (!r) return;
    const q = (c) => r.querySelectorAll(c), N = (p) => Math.ceil(dur / p) + 1;
    q(".ltGapA").forEach((e) => tl.fromTo(e, { scaleX: 0.2, svgOrigin: "46 66" }, { scaleX: 1, svgOrigin: "46 66", duration: 0.6, repeat: N(1.2), yoyo: true, ease: "power2.inOut", immediateRender: false }, t));
    q(".ltEye").forEach((e) => tl.fromTo(e, { scaleY: 1, svgOrigin: "88 64" }, { scaleY: 0.1, svgOrigin: "88 64", duration: 0.08, repeat: N(1.1), repeatDelay: 1, yoyo: true, immediateRender: false }, t + 0.5));
    q(".ltShift").forEach((e) => tl.fromTo(e, { rotation: 18, svgOrigin: "60 84" }, { rotation: -14, svgOrigin: "60 84", duration: 0.25, repeat: N(1.2), repeatDelay: 0.7, yoyo: true, ease: "back.out(3)", immediateRender: false }, t + 0.3));
    q(".ltRoll").forEach((e) => tl.fromTo(e, { x: -20 }, { x: 10, duration: 0.6, repeat: N(0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".ltReach").forEach((e) => tl.fromTo(e, { y: 0 }, { y: 6, duration: 0.3, repeat: N(0.3), yoyo: true, immediateRender: false }, t));
    q(".ltRing").forEach((e) => tl.fromTo(e, { rotation: -6, svgOrigin: "60 60" }, { rotation: 6, svgOrigin: "60 60", duration: 0.06, repeat: N(0.06), yoyo: true, ease: "none", immediateRender: false }, t));
    q(".ltWv").forEach((e) => tl.fromTo(e, { opacity: 0, x: -4 }, { opacity: 1, x: 4, duration: 0.3, repeat: N(0.6), yoyo: true, immediateRender: false }, t));
    q(".ltFlame").forEach((e) => tl.fromTo(e, { scale: 0.85, svgOrigin: "92 56" }, { scale: 1.2, svgOrigin: "92 56", duration: 0.18, repeat: N(0.18), yoyo: true, immediateRender: false }, t));
    q(".ltBack").forEach((e) => tl.fromTo(e, { x: 0 }, { x: -22, duration: 0.8, repeat: N(0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
  };
  // sparks bursting from a point (glow layer): n streaks flying out and falling, gone in 0.5 s
  Lt.sparks = (tl, layer, t, x, y, s = 1, n = 14, seed = 3) => {
    const r = mk(seed), gid = `lts${Math.round(x)}_${Math.round(y)}_${Math.round(t * 100)}`;
    let g = `<g id="${gid}" opacity="0"><circle cx="${x}" cy="${y}" r="${f1(90 * s)}" fill="url(#ltSpark)"/>`;
    const parts = [];
    for (let k = 0; k < n; k++) { const a = r() * Math.PI * 2, d = (80 + r() * 200) * s; parts.push([Math.cos(a) * d, Math.sin(a) * d + 60 * s]); g += `<g class="sp"><path d="M${x},${y}l${f1(Math.cos(a) * 18 * s)},${f1(Math.sin(a) * 18 * s)}" stroke="#ffe27a" stroke-width="${f1(5 * s)}" stroke-linecap="round"/></g>`; }
    put(layer, g + `</g>`);
    tl.set(`#${gid}`, { opacity: 1 }, t); tl.to(`#${gid}`, { opacity: 0, duration: 0.2 }, t + 0.35);
    document.querySelectorAll(`#${gid} .sp`).forEach((e, k) => tl.fromTo(e, { x: 0, y: 0 }, { x: parts[k][0], y: parts[k][1], duration: 0.5, ease: "power2.out", immediateRender: false }, t));
  };

  // ---------------------------------------------------------------- motion
  Lt.life = function (tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    Mok.life(tl, scope, t0, dur);   // .flow / .scroll
    q(".flag").forEach((el, i) => tl.fromTo(el, { attr: { transform: "skewY(0)" } }, { attr: { transform: "skewY(14)" }, duration: 0.14, repeat: Math.ceil(dur / 0.14), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.05));
    q(".puff").forEach((el, i) => { const k = +el.dataset.k; tl.fromTo(el, { y: 0, x: 0, opacity: 0.2, scale: 0.6, transformOrigin: "50% 50%" }, { y: -140 - k * 20, x: -60 - k * 10, opacity: 0, scale: 1.6, duration: 1.1, repeat: Math.ceil(dur / 1.1), ease: "power1.out", immediateRender: false }, t0 + (k * 0.18) % 1.1); });
    q(".swing").forEach((el, i) => { const a = +el.dataset.a || 5; tl.fromTo(el, { rotation: -a, svgOrigin: "0 0" }, { rotation: a, svgOrigin: "0 0", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); });
    q(".cloud").forEach((el) => tl.fromTo(el, { x: 0 }, { x: -(+el.dataset.d) * dur, duration: dur, ease: "none", immediateRender: false }, t0));
    q(".dap").forEach((el, i) => tl.fromTo(el, { x: 400 }, { x: -900, duration: 1.4 + (i % 3) * 0.3, repeat: Math.ceil(dur / 1.4), ease: "none", immediateRender: false }, t0 + i * 0.21));
    q(".spin").forEach((el) => tl.fromTo(el, { rotation: 0, svgOrigin: "0 -70" }, { rotation: 360, svgOrigin: "0 -70", duration: 0.3, repeat: Math.ceil(dur / 0.3), ease: "none", immediateRender: false }, t0));
    q(".steer").forEach((el) => tl.fromTo(el, { rotation: -3, svgOrigin: "720 1860" }, { rotation: 3, svgOrigin: "720 1860", duration: 1.7, repeat: Math.ceil(dur / 1.7), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
  };

  // the hook: the front chain snaps (halves whip out, sparks), the top log jumps the stake and tumbles end-first at the lens.
  // id = the ltPOV id; t0 the snap; the log fills the frame by t0 + dur
  Lt.snap = function (tl, id, t0, o = {}) {
    const T = `#${id}-truck`;
    tl.to(`${T}-ch0L`, { rotation: -38, svgOrigin: "-318 -270", duration: 0.16, ease: "power3.out" }, t0);
    tl.to(`${T}-ch0R`, { rotation: 42, svgOrigin: "318 -270", duration: 0.16, ease: "power3.out" }, t0);
    tl.to(`${T}-ch0`, { opacity: 0, duration: 0.2 }, t0 + 0.22);
    tl.to(`${T}-binder`, { rotation: 70, svgOrigin: "300 -300", duration: 0.12, ease: "back.out(3)" }, t0);
  };
  window.Lt = Lt;
})();
