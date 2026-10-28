// "ตึกโยก" sets, part 1 — "เดอะสกาย 32", a 32-storey condo in central Bangkok, on the Friday afternoon it sways. Daylight, modern, bright.
// Same layer contract as pop2.js (sky / far / mid / set / act / fg; glow above the darkness; light = screen space). Seeded RNG only.
// 1 m ≈ 376 units for a character of scale 1 (rig height ~620 = 1.65 m).
//   Qk.city(L, o)        the Bangkok skyline: sky (o.hz horizon y), sun, clouds, hazy far towers (L.far), mid towers with window grids
//                        (L.mid); o.below: towers whose roofs sit under the horizon (the view down from the 27th floor) · o.dim
//   Sets.qkTower(L, o)   the condo from across the road, whole: glass floors with balconies (floor n's band is y G-n·FH … G-(n-1)·FH,
//                        FH = 96, G = 1720, centre x 540), the rooftop pool behind a glass rail, the name "เดอะสกาย 32", the entrance canopy
//                        with a crack at the street (#id-crack), trees, a parked motorbike.
//                        ids: #id-tw (the whole tower: rotate it with svgOrigin "540 1720"), #id-wat (pool water, slosh it with skewX
//                        around "540 -1380"), #id-spillL / #id-spillR (sheets of water over the roof edges: scaleY from 0 around their
//                        top), #id-birds (a flock on the roof rail that bursts off), #id-f27 (the 27th-floor band, for a glow)
//   Sets.qkLobby(L, o)   the ground-floor lobby side on (floor G 1500): glass entrance on the left with daylight, the guard desk
//                        (front panel redrawn in L.glow so a guard stands behind it), the gold name on a slatted wall, two lifts on the
//                        right (#id-n0 / #id-n1 floor numbers; the right one has a paper sign "ลิฟต์ขัดข้อง" #id-paper), the fire plan,
//                        an extinguisher cabinet, a big plant, downlights
//   Sets.qkLift(L, o)    first person inside the lift facing the doors: steel walls, the floor display (#id-num text, #id-arrow),
//                        the panel on the right with 17–32 (#id-b27 lights up), your green-sleeved hand (#id-hand: tween attr transform
//                        "translate(x,y)"; the fingertip is at its origin), the ceiling light (#id-lite), and for the power cut
//                        #id-dk (darkness, opacity 0) + #id-emg (red emergency lamp, opacity 0)
//   Sets.qkCorridor(L,o) the 27th-floor corridor in one-point perspective (vanishing point 540,870; 24 m long; doors 2701–2716;
//                        the lifts at the far end and the fire stair door with a green exit sign), ceiling lights (#id-lamps),
//                        a ceiling-hung sign (#id-sign: rotate around its rods' top, see Qk.corrSignOrigin), o.dark (lights off,
//                        only the exit sign), o.open: 2714's door open on the right near the camera, o.panels: ceiling panels that
//                        fall (#id-p0…#id-p2, drop them with y + rotation) · Qk.cP(X, Y, d) projects a corridor point (metres) to world
(function () {
  const { mk, f1, put, cloud2 } = Pop2;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const Qk = (window.Qk = window.Qk || {});

  Sets.DEFS += `
    <linearGradient id="qkGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8cc4e0"/><stop offset=".45" stop-color="#4f88ae"/><stop offset="1" stop-color="#7fb6d4"/></linearGradient>
    <linearGradient id="qkGlassSide" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a6684"/><stop offset="1" stop-color="#2a4c66"/></linearGradient>
    <linearGradient id="qkSlab" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f4f2ec"/><stop offset=".7" stop-color="#e2e4e2"/><stop offset="1" stop-color="#c8ccce"/></linearGradient>
    <linearGradient id="qkWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fe0f4"/><stop offset="1" stop-color="#2aa4d0"/></linearGradient>
    <linearGradient id="qkSpill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8fbff" stop-opacity=".95"/><stop offset=".6" stop-color="#9adcf0" stop-opacity=".6"/><stop offset="1" stop-color="#9adcf0" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6e7478"/><stop offset="1" stop-color="#4c5256"/></linearGradient>
    <linearGradient id="qkStone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e4ddd2"/><stop offset="1" stop-color="#cfc6b8"/></linearGradient>
    <linearGradient id="qkMarble" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8e2d8"/><stop offset="1" stop-color="#cfc6b6"/></linearGradient>
    <linearGradient id="qkSlat" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5e3c"/><stop offset=".5" stop-color="#a87650"/><stop offset="1" stop-color="#7e5434"/></linearGradient>
    <linearGradient id="qkSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9aa2a8"/><stop offset=".35" stop-color="#d4d9dc"/><stop offset=".6" stop-color="#b0b7bc"/><stop offset="1" stop-color="#8a9298"/></linearGradient>
    <linearGradient id="qkSteelV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8ced2"/><stop offset="1" stop-color="#8e969c"/></linearGradient>
    <linearGradient id="qkCarpet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e4648"/><stop offset="1" stop-color="#43625f"/></linearGradient>
    <linearGradient id="qkCorrWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efe6d6"/><stop offset="1" stop-color="#ddd0bc"/></linearGradient>
    <linearGradient id="qkDoorWood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a5236"/><stop offset="1" stop-color="#5e3e28"/></linearGradient>
    <radialGradient id="qkDown"><stop offset="0" stop-color="#fff6de" stop-opacity=".85"/><stop offset=".4" stop-color="#ffefc8" stop-opacity=".3"/><stop offset="1" stop-color="#ffefc8" stop-opacity="0"/></radialGradient>
    <radialGradient id="qkSun"><stop offset="0" stop-color="#fffbe8"/><stop offset=".25" stop-color="#fff2c0" stop-opacity=".8"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
    <radialGradient id="qkExit"><stop offset="0" stop-color="#8affb0" stop-opacity=".8"/><stop offset=".45" stop-color="#3fd07a" stop-opacity=".25"/><stop offset="1" stop-color="#3fd07a" stop-opacity="0"/></radialGradient>
    <radialGradient id="qkEmg"><stop offset="0" stop-color="#ff5a46" stop-opacity=".9"/><stop offset=".4" stop-color="#ff3a2a" stop-opacity=".35"/><stop offset="1" stop-color="#ff3a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="qkTube"><stop offset="0" stop-color="#f8fcff" stop-opacity=".9"/><stop offset=".35" stop-color="#e8f4ff" stop-opacity=".35"/><stop offset="1" stop-color="#e8f4ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="qkTreeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ab85a"/><stop offset="1" stop-color="#3e7a34"/></linearGradient>
    <linearGradient id="qkCloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d8e8f2"/></linearGradient>
    <linearGradient id="qkHazeBand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef6f8" stop-opacity="0"/><stop offset=".6" stop-color="#eef6f8" stop-opacity=".75"/><stop offset="1" stop-color="#eef6f8" stop-opacity=".9"/></linearGradient>`;

  // ---------------- the city ----------------
  Qk.city = (L, o = {}) => {
    const r = mk(o.seed || 11), hz = o.hz ?? 1300, x0 = o.x0 ?? -1500, x1 = o.x1 ?? 2700, id = o.id || "qc";
    // the sky: deep blue overhead, pale toward the horizon (user space, so every shot's horizon is light)
    put(L.sky, `<defs><linearGradient id="${id}-sky" gradientUnits="userSpaceOnUse" x1="0" y1="${hz - 2600}" x2="0" y2="${hz}">
        <stop offset="0" stop-color="#3f8fd2"/><stop offset=".5" stop-color="#7fbce6"/><stop offset=".85" stop-color="#cfe6f2"/><stop offset="1" stop-color="#eaf3f2"/></linearGradient></defs>
      <rect x="-3000" y="${hz - 5000}" width="8000" height="${5000 + 1600}" fill="url(#${id}-sky)"/>
      <circle cx="${o.sunX ?? 1500}" cy="${hz - 1500}" r="520" fill="url(#qkSun)"/><circle cx="${o.sunX ?? 1500}" cy="${hz - 1500}" r="70" fill="#fffdf2" opacity=".9"/>`
      + [[-600, hz - 1100, 760, 230], [700, hz - 1380, 620, 190], [1900, hz - 900, 820, 240], [200, hz - 640, 520, 150]].map(([x, y, w, h]) => cloud2(x, y, w, h, r, "qkCloud", "#ffffff", "#9ab8cc")).join(""));
    // far towers: pale, hazy, flat
    let far = "";
    for (let x = x0; x < x1;) {
      const w = 90 + r() * 170, h = 160 + Math.pow(r(), 1.6) * 760, c = ["#a6c0d2", "#b4cad8", "#9db6c8", "#aec3d0"][Math.floor(r() * 4)];
      far += `<rect x="${f1(x)}" y="${f1(hz - h)}" width="${f1(w)}" height="${f1(h + 900)}" fill="${c}"/>`;
      if (r() < 0.25) far += `<path d="M${f1(x + w * 0.5)},${f1(hz - h)}v-${f1(40 + r() * 70)}" stroke="${c}" stroke-width="5"/>`;
      if (r() < 0.5) far += `<path d="M${f1(x + w - 8)},${f1(hz - h)}V${hz + 400}" stroke="#c6d6e0" stroke-width="6" opacity=".6"/>`;
      x += w + r() * 30 - 8;
    }
    far += `<rect x="-3000" y="${hz - 380}" width="8000" height="1600" fill="url(#qkHazeBand)"/>`;
    put(L.far, far);
    if (o.mid === false) return;
    // mid towers: closer, bluer, window grids, rooftop tanks, a crane
    let mid = "";
    for (let x = x0 + r() * 200; x < x1;) {
      const w = 160 + r() * 240, top = o.below ? hz - 500 + r() * 900 : hz - 260 - Math.pow(r(), 1.3) * 900, c = ["#6f90a8", "#7c9cb2", "#61839c", "#86a4b8"][Math.floor(r() * 4)];
      mid += `<rect x="${f1(x)}" y="${f1(top)}" width="${f1(w)}" height="${f1(hz + 2400 - top)}" fill="${c}"/>`;
      mid += `<rect x="${f1(x + w * 0.72)}" y="${f1(top)}" width="${f1(w * 0.28)}" height="${f1(hz + 2400 - top)}" fill="#2a4458" opacity=".22"/>`;
      if (top > hz - 40) mid += `<path d="M${f1(x)},${f1(top)}l${f1(w * 0.18)},-${f1(26)}h${f1(w * 0.82)}l-${f1(w * 0.18)},26z" fill="#a8c0d0" opacity=".9"/><path d="M${f1(x + w * 0.18)},${f1(top - 26)}h${f1(w * 0.82)}" stroke="#dbe8f0" stroke-width="3" opacity=".6"/>`;
      for (let y = top + 30; y < hz + 700; y += 46) mid += `<path d="M${f1(x + 12)},${f1(y)}H${f1(x + w - 12)}" stroke="#cfe2ee" stroke-width="3" opacity=".35"/>`;
      for (let xx = x + 30; xx < x + w - 20; xx += 52) mid += `<path d="M${f1(xx)},${f1(top + 20)}V${hz + 700}" stroke="#4a6a82" stroke-width="2" opacity=".25"/>`;
      if (r() < 0.35) mid += `<rect x="${f1(x + w * 0.2)}" y="${f1(top - 40)}" width="46" height="40" fill="${c}"/><rect x="${f1(x + w * 0.6)}" y="${f1(top - 26)}" width="30" height="26" rx="12" fill="#9ab0c0"/>`;
      if (r() < 0.12) { const cx = x + w * 0.5, cy = top; mid += `<g stroke="#e0a43a" stroke-width="6" fill="none"><path d="M${f1(cx)},${f1(cy)}V${f1(cy - 420)}M${f1(cx - 60)},${f1(cy - 400)}H${f1(cx + 300)}"/><path d="M${f1(cx)},${f1(cy - 420)}L${f1(cx + 300)},${f1(cy - 400)}M${f1(cx)},${f1(cy - 420)}L${f1(cx - 60)},${f1(cy - 400)}" stroke-width="3"/><path d="M${f1(cx + 220)},${f1(cy - 400)}v80" stroke="#555" stroke-width="2"/></g>`; }
      x += w + 40 + r() * 140;
    }
    mid += `<rect x="-3000" y="${hz - 200}" width="8000" height="900" fill="url(#qkHazeBand)" opacity="${o.below ? 0.35 : 0.6}"/>`;
    put(L.mid, mid);
  };

  // ---------------- the condo, outside ----------------
  const FH = 96, NF = 32;
  function qkTower(L, o = {}) {
    const id = o.id || "tw", r = mk(o.seed || 21), G = 1720, X0 = 290, X1 = 790, SIDE = 92, top = G - NF * FH;
    Qk.city(L, { hz: G - 120, seed: o.seed || 13, id: `${id}c`, sunX: 1650 });
    // the street: road, kerb, pavement, rain trees
    let st = `<rect x="-1600" y="${G}" width="4400" height="900" fill="url(#qkRoad)"/><rect x="-1600" y="${G - 6}" width="4400" height="44" fill="#d8d4cc"/>
      <path d="M-1600,${G + 380}H2800" stroke="#f2f0ea" stroke-width="10" stroke-dasharray="90 70" opacity=".8"/>`;
    for (const tx of [-420, 1300, 1720]) st += `<path d="M${tx},${G}V${G - 260}" stroke="#5a4232" stroke-width="22"/>` + cloud2(tx, G - 300, 380, 230, r, "qkTreeG", "#9ac86a", "#2e5a2a");
    // the tower: side face, front face of slab bands and glass, balconies, the fin, the roof
    let tw = `<path d="M${X1},${G}V${top}L${X1 + SIDE},${top + 30}V${G}Z" fill="url(#qkGlassSide)"/>`;
    tw += `<rect x="${X0}" y="${top}" width="${X1 - X0}" height="${NF * FH}" fill="url(#qkGlass)"/>`;
    for (let n = 1; n <= NF; n++) {
      const y = G - n * FH;
      tw += `<rect x="${X0 - 6}" y="${y}" width="${X1 - X0 + 12}" height="14" fill="url(#qkSlab)"/><path d="M${X1},${y + 4}L${X1 + SIDE},${y + 4 + 30 * (1 - n / NF) * 0}" stroke="#a8b4bc" stroke-width="12" opacity=".7"/>`;
      for (let b = 0; b < 4; b++) {
        const bx = X0 + 18 + b * 118;
        if ((b + n) % 2 === 0 && n > 1) tw += `<rect x="${bx}" y="${y + 44}" width="96" height="52" fill="#d8eef6" opacity=".22"/><path d="M${bx},${y + 44}H${bx + 96}" stroke="#eef6f8" stroke-width="4"/>`;
      }
      tw += [0, 1, 2, 3, 4].map((k) => `<path d="M${X0 + k * 125},${y + 14}V${y + FH}" stroke="#2c4e66" stroke-width="3" opacity=".55"/>`).join("");
      if (n === 27) tw += `<g id="${id}-f27" opacity="0"><rect x="${X0}" y="${y + 14}" width="${X1 - X0}" height="${FH - 14}" fill="#ffe9a0" opacity=".55"/><rect x="${X0}" y="${y + 14}" width="${X1 - X0}" height="${FH - 14}" fill="none" stroke="#fff6c8" stroke-width="6"/></g>`;
    }
    // the sun's sheen across the glass, and a vertical white fin
    tw += `<path d="M${X0},${top + 900}L${X0 + 200},${top + 300}L${X0 + 300},${top + 300}L${X0 + 100},${top + 900}Z" fill="#fff" opacity=".14"/><path d="M${X0 + 120},${top + 2200}L${X0 + 380},${top + 1400}L${X0 + 430},${top + 1400}L${X0 + 170},${top + 2200}Z" fill="#fff" opacity=".1"/>
      <rect x="${X0 + 238}" y="${top - 40}" width="24" height="${NF * FH + 40}" fill="#f2f2ee"/><rect x="${X0 + 256}" y="${top - 40}" width="6" height="${NF * FH + 40}" fill="#b8c0c4"/>`;
    // the lobby at the street: glass doors, the canopy with its crack
    tw += `<rect x="${X0 + 40}" y="${G - 250}" width="420" height="250" fill="#2a3a46"/><rect x="${X0 + 60}" y="${G - 230}" width="180" height="230" fill="#9ac8de" opacity=".55"/><rect x="${X0 + 260}" y="${G - 230}" width="180" height="230" fill="#9ac8de" opacity=".55"/>
      <path d="M${X0 + 20},${G - 300}H${X0 + 480}L${X0 + 500},${G - 270}H${X0}Z" fill="#e8e8e2" ${OUT3}/><path d="M${X0 + 40},${G - 270}V${G}M${X0 + 460},${G - 270}V${G}" stroke="#c8ccce" stroke-width="12"/>
      <path id="${id}-crack" d="M${X0 + 300},${G - 300}l-14,14l10,8l-18,10" stroke="${INK}" stroke-width="3" fill="none"/>
      <text x="${X0 + 250}" y="${G - 312}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#2a3a46">เดอะสกาย 32</text>`;
    // the roof: the name, the pool behind its glass rail, palms, the lift machine room
    tw += `<rect x="${X0 + 20}" y="${top - 120}" width="150" height="120" fill="#e8e8e2" ${OUT3}/><rect x="${X0}" y="${top - 18}" width="${X1 - X0 + SIDE}" height="18" fill="#f2f2ee"/>
      <defs><clipPath id="${id}-poolc"><rect x="${X0 + 190}" y="${top - 70}" width="${X1 - X0 - 200}" height="70"/></clipPath></defs>
      <g clip-path="url(#${id}-poolc)"><g id="${id}-wat"><path d="M${X0 + 150},${top - 46}Q${X0 + 300},${top - 56} ${X0 + 450},${top - 46}T${X1 + 60},${top - 46}V${top + 40}H${X0 + 150}Z" fill="url(#qkWater)"/>
        <path d="M${X0 + 200},${top - 44}q40,-8 80,0t80,0t80,0" stroke="#e8fbff" stroke-width="4" fill="none" opacity=".8"/></g></g>
      <rect x="${X0 + 190}" y="${top - 74}" width="${X1 - X0 - 200}" height="56" fill="#cfeef8" opacity=".35"/><path d="M${X0 + 190},${top - 74}H${X1 - 10}" stroke="#eef8fb" stroke-width="5"/>
      ${[X0 + 200, X1 - 40].map((px) => `<path d="M${px},${top - 18}q6,-60 -4,-110" stroke="#7a5a3a" stroke-width="8" fill="none"/><path d="M${px - 4},${top - 128}q-40,-10 -70,20M${px - 4},${top - 128}q40,-16 74,8M${px - 4},${top - 128}q-10,-40 -46,-52M${px - 4},${top - 128}q20,-40 54,-44" stroke="#3e8a4a" stroke-width="12" fill="none" stroke-linecap="round"/>`).join("")}
      <g transform="translate(${X1 - 60},${top + 160})"><rect x="-120" y="-34" width="200" height="56" rx="10" fill="#1e2e3a"/><text x="-20" y="8" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#f6e2a0">เดอะสกาย 32</text></g>`;
    // water sheets that slop over the roof edges
    tw += `<path id="${id}-spillL" d="M${X0 + 186},${top - 20}C${X0 + 150},${top + 60} ${X0 + 120},${top + 400} ${X0 + 90},${top + 900}L${X0 + 30},${top + 900}C${X0 + 70},${top + 400} ${X0 + 110},${top + 40} ${X0 + 186},${top - 20}Z" fill="url(#qkSpill)" opacity="0"/>
      <path id="${id}-spillR" d="M${X1 - 10},${top - 20}C${X1 + 40},${top + 60} ${X1 + 80},${top + 400} ${X1 + 120},${top + 900}L${X1 + 180},${top + 900}C${X1 + 120},${top + 400} ${X1 + 60},${top + 40} ${X1 - 10},${top - 20}Z" fill="url(#qkSpill)" opacity="0"/>`;
    // pigeons on the roof rail
    tw += `<g id="${id}-birds">${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${X0 + 220 + k * 46},${top - 80}q8,-8 16,0q8,-8 16,0" stroke="#2a2e34" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    put(L.set, st + `<g id="${id}-tw">${tw}</g>`);
    // a parked motorbike with its green delivery box at the kerb
    put(L.set, `<g transform="translate(${X1 + 260},${G}) scale(1.1)"><circle cx="-90" cy="-40" r="40" fill="#1e1e22"/><circle cx="90" cy="-40" r="40" fill="#1e1e22"/><circle cx="-90" cy="-40" r="16" fill="#9aa0a6"/><circle cx="90" cy="-40" r="16" fill="#9aa0a6"/>
      <path d="M-90,-40L-40,-110H40L90,-40M-40,-110L-60,-150" stroke="#c83a2a" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-30,-118H50" stroke="#1e1e22" stroke-width="18" stroke-linecap="round"/>
      <rect x="-30" y="-230" width="110" height="100" rx="8" fill="#2fa45a" ${OUT3}/><circle cx="25" cy="-180" r="22" fill="#fff4dc" ${OUT3}/></g>`);
    put(L.fg, `<path d="M-1600,2300H2800V2700H-1600Z" fill="#3c4246"/>`);
  }

  // ---------------- the lobby ----------------
  function qkLobby(L, o = {}) {
    const id = o.id || "lb", G = 1500, CE = 340;
    let s = `<rect x="-1600" y="-400" width="4600" height="${G + 400}" fill="url(#qkStone)"/>`;
    for (let x = -1600; x < 3000; x += 260) s += `<path d="M${x},${CE}V${G}" stroke="#c8beb0" stroke-width="3"/>`;
    s += `<rect x="-1600" y="-400" width="4600" height="${CE + 400}" fill="#ece8e0"/><path d="M-1600,${CE}H3000" stroke="#c8beb0" stroke-width="8"/>`;
    // the entrance: glass doors with daylight, the street and a tree beyond
    s += `<rect x="-900" y="${CE + 60}" width="620" height="${G - CE - 60}" fill="#2c3a44"/>
      <rect x="-880" y="${CE + 80}" width="290" height="${G - CE - 80}" fill="#cfeaf6"/><rect x="-570" y="${CE + 80}" width="270" height="${G - CE - 80}" fill="#cfeaf6"/>
      <path d="M-880,${G - 260}H-300" stroke="#9aa0a4" stroke-width="40" opacity=".5"/><path d="M-760,${G - 260}V${CE + 300}" stroke="#7a6a52" stroke-width="16" opacity=".5"/>
      <ellipse cx="-760" cy="${CE + 280}" rx="160" ry="110" fill="#7ab86a" opacity=".55"/><path d="M-860,${CE + 120}L-700,${G - 200}M-540,${CE + 140}L-420,${G - 300}" stroke="#fff" stroke-width="16" opacity=".35"/>
      <path d="M-590,${CE + 80}V${G}" stroke="#2c3a44" stroke-width="16"/><path d="M-610,${CE + 800}H-570" stroke="#c8ccce" stroke-width="10" stroke-linecap="round"/>`;
    // the slatted wall with the name in gold
    s += `<rect x="-200" y="${CE + 40}" width="760" height="${G - CE - 300}" fill="url(#qkSlat)"/>`;
    for (let x = -190; x < 560; x += 28) s += `<path d="M${x},${CE + 40}V${G - 260}" stroke="#6a4428" stroke-width="5" opacity=".6"/>`;
    s += `<text x="180" y="${CE + 250}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="92" fill="#e8c46a" stroke="#7a5a1a" stroke-width="2" paint-order="stroke">เดอะสกาย 32</text>
      <text x="180" y="${CE + 330}" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="44" letter-spacing="14" fill="#e8c46a" opacity=".85">THE SKY 32</text>`;
    // two lifts with floor numbers; the right one with a hand-written paper sign
    const lift = (x, k) => `<rect x="${x - 30}" y="${G - 830}" width="440" height="830" fill="#8e969c"/><rect x="${x}" y="${G - 800}" width="190" height="800" fill="url(#qkSteel)"/><rect x="${x + 190}" y="${G - 800}" width="190" height="800" fill="url(#qkSteel)"/>
      <path d="M${x + 190},${G - 800}V${G}" stroke="#5e666c" stroke-width="4"/><rect x="${x + 110}" y="${G - 920}" width="160" height="66" rx="8" fill="#141414" ${OUT3}/>
      <text id="${id}-n${k}" x="${x + 190}" y="${G - 872}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#ff5a3a">${k ? "12" : "1"}</text>`;
    s += lift(780, 0) + lift(1300, 1);
    s += `<rect x="1205" y="${G - 520}" width="56" height="110" rx="8" fill="#c8ced2" ${OUT3}/><circle cx="1233" cy="${G - 490}" r="13" fill="#f6f6f0" ${OUT3}/><circle cx="1233" cy="${G - 440}" r="13" fill="#f6f6f0" ${OUT3}/>
      <g id="${id}-paper" transform="translate(1490,${G - 500}) rotate(3)"><rect x="-120" y="-80" width="240" height="150" fill="#fbf8ee" ${OUT3}/><path d="M-120,-80h40v-14h-40zM80,-80h40v-14h-40z" fill="#d8d0b8" opacity=".8"/>
        <text x="0" y="-20" text-anchor="middle" font-family="Mali" font-weight="700" font-size="40" fill="#c8281e">ลิฟต์ขัดข้อง</text><text x="0" y="32" text-anchor="middle" font-family="Mali" font-weight="600" font-size="28" fill="#3a3a3a">ขออภัยในความไม่สะดวก</text></g>`;
    // the fire plan and the extinguisher cabinet
    s += `<g transform="translate(1960,${G - 760})"><rect x="-110" y="-150" width="220" height="300" fill="#fff" ${OUT3}/><rect x="-110" y="-150" width="220" height="50" fill="#2fa45a"/>
        <text x="0" y="-114" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#fff">แผนผังหนีไฟ</text><path d="M-80,-60H80V120H-80Z" fill="none" stroke="#5a5a5a" stroke-width="3"/><path d="M-80,30H80M0,-60V120" stroke="#9a9a9a" stroke-width="2"/>
        <path d="M-60,100L60,-40" stroke="#2fa45a" stroke-width="6" stroke-dasharray="14 8"/><circle cx="-60" cy="100" r="10" fill="#d8312a"/></g>
      <g transform="translate(2240,${G - 520})"><rect x="-70" y="-150" width="140" height="300" rx="6" fill="#c8281e" ${OUT3}/><rect x="-50" y="-130" width="100" height="200" fill="#e8f0f4" opacity=".55"/><rect x="-22" y="-90" width="44" height="140" rx="16" fill="#d8312a" ${OUT3}/></g>`;
    // the floor: polished, with reflections of the lights
    s += `<rect x="-1600" y="${G}" width="4600" height="1400" fill="url(#qkMarble)"/>`;
    for (let k = -14; k < 22; k++) s += `<path d="M${540 + k * 60},${G}L${540 + k * 260},${G + 1400}" stroke="#c4baa8" stroke-width="3" opacity=".6"/>`;
    for (const y of [G + 90, G + 260, G + 520, G + 900]) s += `<path d="M-1600,${y}H3000" stroke="#c4baa8" stroke-width="3" opacity=".6"/>`;
    s += `<path d="M780,${G + 20}H1160L1200,${G + 300}H740Z" fill="#cfd4d8" opacity=".35"/><path d="M1300,${G + 20}H1680L1720,${G + 300}H1260Z" fill="#cfd4d8" opacity=".35"/>
      <path d="M-880,${G}H-300L-200,${G + 500}H-1000Z" fill="#eaf6fb" opacity=".5"/>`;
    // the plant
    s += `<g transform="translate(640,${G})"><path d="M-60,0L-70,-150H70L60,0Z" fill="#3a3a3a" ${OUT3}/>${[[-80, -300], [10, -380], [90, -290], [-40, -420], [60, -440]].map(([lx, ly], k) => `<path d="M0,-150Q${lx * 0.4},${(ly - 150) / 2} ${lx},${ly}" stroke="#2e6a3a" stroke-width="7" fill="none"/><ellipse cx="${lx}" cy="${ly}" rx="58" ry="34" transform="rotate(${-30 + k * 20} ${lx} ${ly})" fill="#3e8a4a" ${OUT3}/>`).join("")}</g>`;
    put(L.set, s);
    // the guard desk: drawn in glow so the guard stands behind it
    put(L.glow, `<g transform="translate(180,${G})"><rect x="-330" y="-395" width="660" height="395" fill="#3a2e28" ${OUT}/><rect x="-350" y="-420" width="700" height="34" rx="6" fill="#d8d0c0" ${OUT}/>
        <path d="M-300,-360H300M-300,-60H300" stroke="#6a5a4a" stroke-width="3" opacity=".6"/><rect x="-130" y="-300" width="260" height="120" rx="8" fill="#2a2420" opacity=".6"/>
        <text x="0" y="-226" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="40" fill="#e8c46a">ติดต่อ</text>
        <rect x="140" y="-560" width="150" height="110" rx="6" fill="#1e2228" ${OUT3}/><path d="M215,-450v30" stroke="#1e2228" stroke-width="12"/>
        <g transform="translate(-230,-420)"><circle cy="-70" r="56" fill="#e8ecee" ${OUT3}/><path d="M0,-70m-40,0a40,40 0 1 0 80,0a40,40 0 1 0 -80,0" fill="none" stroke="#b8c0c4" stroke-width="4"/><path d="M0,-14V0" stroke="#5a5a5a" stroke-width="8"/></g></g>`);
    // downlights
    put(L.glow, [-400, 180, 760, 1300, 1840, 2380].map((x) => `<ellipse cx="${x}" cy="${CE + 4}" rx="26" ry="8" fill="#fffaf0"/><ellipse cx="${x}" cy="${CE + 160}" rx="220" ry="200" fill="url(#qkDown)" opacity=".35"/>`).join(""));
  }

  // ---------------- inside the lift (first person) ----------------
  function qkLift(L, o = {}) {
    const id = o.id || "lf";
    let s = `<rect x="-600" y="-600" width="2300" height="3200" fill="#7e868c"/>`;
    // side walls in perspective, the back is behind us: the doors ahead
    s += `<path d="M-600,-400L230,300V1700L-600,2500Z" fill="url(#qkSteelV)"/><path d="M1680,-400L850,300V1700L1680,2500Z" fill="url(#qkSteelV)"/>
      <path d="M-600,1150L230,1080M1680,1150L850,1080" stroke="#5a6268" stroke-width="22" stroke-linecap="round"/><path d="M-600,1130L230,1066M1680,1130L850,1066" stroke="#e8eef2" stroke-width="5" opacity=".7"/>
      <path d="M-600,-400L230,300H850L1680,-400Z" fill="#e8ecee"/><rect x="330" y="80" width="420" height="120" rx="12" fill="#fffef6"/><g id="${id}-lite"><rect x="330" y="80" width="420" height="120" rx="12" fill="#fff" opacity=".9"/><ellipse cx="540" cy="260" rx="560" ry="420" fill="url(#qkTube)" opacity=".7"/></g>
      <path d="M-600,2500L230,1700H850L1680,2500Z" fill="#3a3e42"/><path d="M230,1700H850" stroke="#c8ced2" stroke-width="8"/>`;
    // the doors and the frame
    s += `<rect x="230" y="300" width="620" height="1400" fill="#5e666c"/><rect x="250" y="340" width="290" height="1360" fill="url(#qkSteel)"/><rect x="540" y="340" width="290" height="1360" fill="url(#qkSteel)"/>
      <path d="M540,340V1700" stroke="#3e464c" stroke-width="5"/><path d="M300,420L420,1500M640,420L760,1500" stroke="#fff" stroke-width="14" opacity=".12"/>`;
    // the display
    s += `<rect x="410" y="230" width="260" height="96" rx="12" fill="#0e0e10" ${OUT3}/><path id="${id}-arrow" d="M450,300l22,-38l22,38z" fill="#ff5a3a"/>
      <text id="${id}-num" x="590" y="304" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="74" fill="#ff5a3a">1</text>`;
    // the panel on the right wall: 17–32 in two columns, 27 lights up
    let pn = `<path d="M890,640L1060,560V1380L890,1340Z" fill="#c8ced2" ${OUT3}/>`;
    for (let k = 0; k < 16; k++) {
      const n = 32 - k, col = k % 2, row = Math.floor(k / 2), x = 932 + col * 64, y = 650 + row * 86 + col * -8;
      pn += `<g id="${id}-b${n}"><ellipse cx="${x}" cy="${y}" rx="24" ry="27" fill="#eef0f0" stroke="#5a6268" stroke-width="3"/><text x="${x}" y="${y + 9}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="24" fill="#3a3e42">${n}</text></g>`;
    }
    s += pn;
    put(L.set, s);
    // the lit ring of 27 (shown when pressed), the hand, the darkness and the emergency lamp
    const k27 = 32 - 27, bx = 932 + (k27 % 2) * 64, by = 650 + Math.floor(k27 / 2) * 86 + (k27 % 2) * -8;
    Qk.liftBtn27 = [bx, by];
    put(L.glow, `<g id="${id}-lit27" opacity="0"><ellipse cx="${bx}" cy="${by}" rx="34" ry="37" fill="none" stroke="#ffb03a" stroke-width="7"/><ellipse cx="${bx}" cy="${by}" rx="60" ry="64" fill="url(#qkSun)" opacity=".8"/></g>
      <rect id="${id}-dk" x="-600" y="-600" width="2300" height="3200" fill="#020304" opacity="0"/>
      <g id="${id}-emg" opacity="0"><circle cx="540" cy="150" r="520" fill="url(#qkEmg)"/><rect x="500" y="130" width="80" height="34" rx="8" fill="#ff6a4a"/></g>
      <g id="${id}-hand" transform="translate(${bx + 260},${by + 760})">${Qk.povArm()}</g>`);
  }
  // your right forearm in the green jacket, the index finger pointing up-left, its tip at (0,0)
  Qk.povArm = (o = {}) => `<g transform="rotate(${o.rot ?? -28})">
      <path d="M-60,120L-40,980H170L150,110Z" fill="#2fa45a" ${OUT}/><path d="M-50,300H160M-46,520H164" stroke="#e8f0e8" stroke-width="14" opacity=".85"/><path d="M-56,150H154" stroke="#25874a" stroke-width="22"/>
      <path d="M-40,140Q-56,40 -10,10L0,0Q14,-6 22,8L30,40Q60,30 76,60Q100,58 110,86Q134,90 136,124Q132,150 100,160L-30,170Z" fill="#c99068" ${OUT}/>
      <path d="M30,40L36,96M76,60L74,104M110,86L104,118" stroke="#9a6a48" stroke-width="3" fill="none"/><path d="M2,6Q10,0 16,8" stroke="#f6e2d0" stroke-width="5" fill="none"/></g>`;

  // ---------------- the corridor of floor 27 ----------------
  const VX = 540, VY = 870, K = 850, FOC = 5.5, EYE = 1.6, HW = 0.9, CH = 2.6, LEN = 24;
  const cP = (X, Y, d) => { const k = FOC / (FOC + d); return [VX + X * K * k, VY + (EYE - Y) * K * k]; };
  Qk.cP = cP;
  const quad = (pts, attrs) => `<path d="M${pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}Z" ${attrs}/>`;
  function qkCorridor(L, o = {}) {
    const id = o.id || "cr", dark = !!o.dark;
    put(L.sky, `<rect x="-1500" y="-1500" width="4000" height="5000" fill="#1a1612"/>`);
    let s = "";
    // floor, ceiling, walls
    s += quad([cP(-HW, 0, 0), cP(HW, 0, 0), cP(HW, 0, LEN), cP(-HW, 0, LEN)], `fill="url(#qkCarpet)"`);
    for (let d = 0.6; d < LEN; d += 1.2) s += quad([cP(-HW, 0, d), cP(HW, 0, d), cP(HW, 0, d + 0.12), cP(-HW, 0, d + 0.12)], `fill="#5a7c78" opacity=".35"`);
    s += quad([cP(-0.28, 0, 0), cP(0.28, 0, 0), cP(0.28, 0, LEN), cP(-0.28, 0, LEN)], `fill="#7a5a3a" opacity=".25"`);
    s += quad([cP(-HW, CH, 0), cP(HW, CH, 0), cP(HW, CH, LEN), cP(-HW, CH, LEN)], `fill="#e8e2d6"`);
    for (const side of [-1, 1]) {
      s += quad([cP(side * HW, 0, 0), cP(side * HW, CH, 0), cP(side * HW, CH, LEN), cP(side * HW, 0, LEN)], `fill="url(#qkCorrWall)"`);
      s += quad([cP(side * HW, 0, 0), cP(side * HW, 0.12, 0), cP(side * HW, 0.12, LEN), cP(side * HW, 0, LEN)], `fill="#6a5a48"`);
      s += quad([cP(side * HW, CH - 0.02, 0), cP(side * HW, CH, 0), cP(side * HW, CH, LEN), cP(side * HW, CH - 0.02, LEN)], `fill="#c8bca8"`);
    }
    // the far end: two lifts and the stair door with its exit sign
    const e = (X, Y) => cP(X, Y, LEN);
    s += quad([e(-HW, 0), e(HW, 0), e(HW, CH), e(-HW, CH)], `fill="#e6dccb"`);
    s += quad([e(-0.78, 0), e(-0.1, 0), e(-0.1, 2.1), e(-0.78, 2.1)], `fill="url(#qkSteel)"`) + quad([e(-0.44, 0), e(-0.43, 0), e(-0.43, 2.1), e(-0.44, 2.1)], `fill="#5e666c"`);
    s += quad([e(0.15, 0), e(0.8, 0), e(0.8, 2.05), e(0.15, 2.05)], `fill="#9a3a2a"`) + quad([e(0.6, 1.0), e(0.7, 1.0), e(0.7, 1.08), e(0.6, 1.08)], `fill="#d8d0c0"`);
    const [ex, ey] = e(0.47, 2.3);
    const ek = FOC / (FOC + LEN);
    put(L.glow, `<g id="${id}-exit"><ellipse cx="${f1(ex)}" cy="${f1(ey)}" rx="${f1(140 * ek * 6)}" ry="${f1(90 * ek * 6)}" fill="url(#qkExit)"/>
      <rect x="${f1(ex - 46 * ek * 4)}" y="${f1(ey - 16 * ek * 4)}" width="${f1(92 * ek * 4)}" height="${f1(32 * ek * 4)}" rx="3" fill="#18b45a"/>
      <path d="M${f1(ex - 30 * ek * 4)},${f1(ey + 8 * ek * 4)}l${f1(8 * ek * 4)},-${f1(16 * ek * 4)}l${f1(8 * ek * 4)},${f1(8 * ek * 4)}" stroke="#fff" stroke-width="${f1(4 * ek * 4)}" fill="none"/></g>`);
    // doors along both walls (odd numbers on the left, even on the right), with their number plates
    const doors = [1.4, 4.6, 7.8, 11, 14.2, 17.4, 20.6];
    doors.forEach((d, k) => {
      for (const side of [-1, 1]) {
        const X = side * HW, n = side < 0 ? 2701 + 2 * (6 - k) : 2702 + 2 * (6 - k) + (k === 0 ? 12 : 0);
        if (o.open && side > 0 && k === 0) {
          // 2714 open: the doorway glows with daylight, the door leaf swung into the room
          s += quad([cP(X, 0, d), cP(X, 2.1, d), cP(X, 2.1, d + 1.0), cP(X, 0, d + 1.0)], `fill="#fff3d8"`);
          s += quad([cP(X, 0, d + 0.08), cP(X, 2.1, d + 0.08), cP(X + 0.75, 2.1, d + 0.3), cP(X + 0.75, 0, d + 0.3)], `fill="url(#qkDoorWood)" stroke="${INK}" stroke-width="3"`);
          continue;
        }
        s += quad([cP(X, 0, d), cP(X, 2.1, d), cP(X, 2.1, d + 1.0), cP(X, 0, d + 1.0)], `fill="url(#qkDoorWood)" stroke="#3a2618" stroke-width="2"`);
        s += quad([cP(X, 0, d - 0.06), cP(X, 2.16, d - 0.06), cP(X, 2.16, d + 1.06), cP(X, 0, d + 1.06)], `fill="none" stroke="#a88a6a" stroke-width="${f1(10 * FOC / (FOC + d))}"`);
        const [hx, hy] = cP(X, 1.0, d + 0.85), [px, py] = cP(X, 1.55, d + 0.5), kk = FOC / (FOC + d);
        s += `<circle cx="${f1(hx)}" cy="${f1(hy)}" r="${f1(Math.max(2, 22 * kk))}" fill="#d8c070"/>`;
        s += `<text x="${f1(px)}" y="${f1(py)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${f1(Math.max(6, 70 * kk))}" fill="#f4e6c0" transform="skewY(${side * 18 * (1 - kk) + side * 12})" transform-origin="${f1(px)} ${f1(py)}">${n}</text>`;
      }
    });
    // the fire alarm and extinguisher on the left wall
    const [ax, ay] = cP(-HW, 1.4, 9.6), ak = FOC / (FOC + 9.6);
    s += `<circle cx="${f1(ax)}" cy="${f1(ay)}" r="${f1(60 * ak)}" fill="#d8312a"/><rect x="${f1(ax - 40 * ak)}" y="${f1(ay + 200 * ak)}" width="${f1(80 * ak)}" height="${f1(230 * ak)}" fill="#c8281e"/>`;
    put(L.set, s);
    // ceiling lights (a ring of glow on the carpet below each), off in the dark version
    let lamps = "";
    for (let d = 1; d < LEN; d += 3) {
      lamps += quad([cP(-0.25, CH, d), cP(0.25, CH, d), cP(0.25, CH, d + 0.6), cP(-0.25, CH, d + 0.6)], dark ? `fill="#cfc8bc"` : `fill="#fffbf0"`);
      if (!dark) { const [lx, ly] = cP(0, 0, d + 0.3), kk = FOC / (FOC + d); lamps += `<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="${f1(700 * kk)}" ry="${f1(200 * kk)}" fill="url(#qkDown)" opacity=".5"/>`; }
    }
    put(L.glow, `<g id="${id}-lamps">${lamps}</g>`);
    // a sign hung from the ceiling at 5 m: "ลิฟต์ · ทางหนีไฟ"
    const [sx, sy] = cP(0, CH, 5), sk = FOC / (FOC + 5);
    Qk.corrSignOrigin = `${f1(sx)} ${f1(sy)}`;
    put(L.glow, `<g id="${id}-sign"><path d="M${f1(sx - 200 * sk)},${f1(sy)}V${f1(sy + 150 * sk)}M${f1(sx + 200 * sk)},${f1(sy)}V${f1(sy + 150 * sk)}" stroke="#5a5a5a" stroke-width="${f1(8 * sk)}"/>
      <rect x="${f1(sx - 300 * sk)}" y="${f1(sy + 150 * sk)}" width="${f1(600 * sk)}" height="${f1(150 * sk)}" rx="${f1(12 * sk)}" fill="#1e3a2c" stroke="#e8e2d0" stroke-width="${f1(6 * sk)}"/>
      <text x="${f1(sx)}" y="${f1(sy + 248 * sk)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${f1(70 * sk)}" fill="#f4f0e2">ลิฟต์ · ทางหนีไฟ →</text></g>`);
    // ceiling panels that can fall (drawn in place)
    if (o.panels) put(L.glow, [6.5, 10, 13.5].map((d, k) => `<g id="${id}-p${k}">${quad([cP(-0.6, CH - 0.01, d), cP(0.6, CH - 0.01, d), cP(0.6, CH - 0.01, d + 0.6), cP(-0.6, CH - 0.01, d + 0.6)], `fill="#efe9de" stroke="#9a9286" stroke-width="3"`)}</g>`).join(""));
  }

  Object.assign(Sets, { qkTower, qkLobby, qkLift, qkCorridor });
})();
