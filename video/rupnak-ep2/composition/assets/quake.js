// "ตึกโยก" sets, part 1 — "เดอะสกาย 32", a 32-storey condo in central Bangkok, on the Friday afternoon it sways. Daylight, modern, bright.
// Same layer contract as pop2.js (sky / far / mid / set / act / fg; glow above the darkness; light = screen space). Seeded RNG only.
// Needs qkmat.js (the material kit) loaded first. 1 m ≈ 376 units for a character of scale 1 (rig height ~620 = 1.65 m).
// Look (skill rule V10): lit face + shade face + edge highlight + contact shadow on everything; the sun is up on the right.
//   Qk.city(L, o)        the Bangkok skyline: sky with cirrus (o.hz horizon y), sun, clouds; far: two hazy bands of towers and the
//                        landmarks in silhouette (o.marks [[name, x]…] with baiyoke | mahanakhon | state, o.markS their scale);
//                        mid: towers whose side faces turn toward o.vx (sunlit on the right, shaded on the left), window grids, roof
//                        tanks and antennas; o.below: roofs under the horizon seen from above (helipads, gardens, pools) — the view
//                        down from the 27th floor · o.mid false: no mid layer
//   Sets.qkTower(L, o)   the condo from across the road, whole: glass floors (floor n's band is y G-n·FH … G-(n-1)·FH, FH = 96,
//                        G = 1720, centre x 540) with curtains, balconies (glass rails, AC condensers, plants, laundry), a sunlit side
//                        face, the fin, the rooftop pool and palms, the lift room with its mast, the lobby, the canopy, planters; the
//                        street: pavement with a tactile strip, kerb, road, rain trees, concrete poles with the wire tangle, a street-food
//                        cart under an umbrella, a pink taxi, your delivery bike.
//                        ids: #id-tw (the whole tower: rotate it with svgOrigin "540 1720"), #id-wat (pool water, slosh it with x/y),
//                        #id-spillL / #id-spillR (sheets of water over the roof edges: scaleY from 0 around their top), #id-birds
//                        (a flock on the roof rail that bursts off), #id-f27 (the 27th-floor band, for a glow), #id-crack (the canopy),
//                        #id-palm0 / #id-palm1 (rooftop palms: rotate around "0 0"), #id-beacon (the red mast light: blink it),
//                        #id-tree0 / #id-tree1 (street trees: rotate around "0 0"), #id-pole0 / #id-pole1 (rotate around "0 0"),
//                        #id-w0…#id-w{Qk.towerWires-1} (one wire each: scaleY around its "x y" in data-o), #id-umb (the cart's
//                        umbrella: rotate around "0 0") — Qk.reactTower(tl, id, t0, dur, amp) runs all of these
//   Sets.qkLobby(L, o)   the ground-floor lobby side on (floor G 1500, eye level 1080): a coffered ceiling in perspective with downlights,
//                        stone wall panels lit in scallops, the glass entrance on the left with the street outside, the slatted wood
//                        wall with the backlit gold name, the guard desk (fluted walnut, marble top, fan, logbook, monitor; drawn in
//                        L.glow so a guard stands behind it), two lifts on the right in steel architraves (#id-n0 / #id-n1 floor
//                        numbers; the right one has a paper sign "ลิฟต์ขัดข้อง" #id-paper), the call buttons, a notice board, a
//                        monstera (#id-plant: rotate around "640 1500"), polished marble with reflections, a CCTV dome
//   Sets.qkLift(L, o)    first person inside the lift facing the doors (vanishing point 540, 1000): brushed steel walls, a mirror on the
//                        left, handrails, the button panel on the right wall (17–32 with braille, door open/close, alarm, intercom, key
//                        switch), the capacity plate and the inspection certificate (#id-cert: rotate around Qk.liftCertOrigin), the
//                        floor display (#id-num text, #id-arrow), the no-lift-in-fire-or-quake sticker, granite floor, a CCTV dome,
//                        the panel with 27 (#id-b27 lights up: #id-lit27), your green-sleeved hand (#id-hand: tween attr transform
//                        "translate(x,y)"; the fingertip is at its origin; Qk.liftBtn27 = the button), the ceiling light (#id-lite), and
//                        for the power cut #id-dk (darkness, opacity 0) + #id-emg (red emergency lamp, opacity 0)
//   Sets.qkCorridor(L,o) the 27th-floor corridor in one-point perspective (vanishing point 540,870; 24 m long; doors 2701–2716 with
//                        casings, panels, kick plates, levers, peepholes and brass numbers; the lift at the far end and the fire stair
//                        door with a green exit sign), a patterned carpet, wainscot and chair rail, sconces and ceiling lights
//                        (#id-lamps, with their light pools), framed pictures (#id-art0…#id-art5: rotate around data-o), the fire hose
//                        cabinet, CCTV, smoke detectors, a ceiling-hung sign (#id-sign: rotate around its rods' top, see
//                        Qk.corrSignOrigin), o.dark (lights off, only the exit sign), o.open: 2714's door open on the right near the
//                        camera, o.panels: ceiling panels that fall (#id-p0…#id-p2, drop them with y + rotation) · Qk.cP(X, Y, d)
//                        projects a corridor point (metres) to world · Qk.reactCorridor(tl, id, t0, dur, amp) swings the sign and
//                        the pictures and drops plaster dust
//   Qk.swing(tl, sel, origin, t0, dur, amp, per)   a pendulum that settles at the end
//   Qk.debris(tl, layer, o)                         plaster bits falling (o.pts(r) → { x, y0, y1, s }), deterministic in time
(function () {
  const { mk, f1, put, cloud2, crown } = Pop2;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const OUT2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round"`;
  const Qk = (window.Qk = window.Qk || {});
  const T = Qk.tone, CS = Qk.cs, PL = Qk.poly;
  const pt = (p) => `${f1(p[0])},${f1(p[1])}`;
  const SP = (pts) => "M" + pts.map(pt).join("L") + "Z";

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
    <linearGradient id="qkHazeBand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef6f8" stop-opacity="0"/><stop offset=".6" stop-color="#eef6f8" stop-opacity=".75"/><stop offset="1" stop-color="#eef6f8" stop-opacity=".9"/></linearGradient>
    <linearGradient id="qkFacG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6f2"/><stop offset=".3" stop-color="#8ab8d4"/><stop offset=".75" stop-color="#5a8cae"/><stop offset="1" stop-color="#4a7a9c"/></linearGradient>
    <linearGradient id="qkFacSide" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d6eef8"/><stop offset=".5" stop-color="#a8d0e6"/><stop offset="1" stop-color="#8ebcd8"/></linearGradient>
    <linearGradient id="qkPoleG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a8e8a"/><stop offset=".55" stop-color="#c6cac4"/><stop offset="1" stop-color="#eef0ea"/></linearGradient>
    <linearGradient id="qkPave" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ddd6c8"/><stop offset="1" stop-color="#c4bcac"/></linearGradient>
    <linearGradient id="qkAsph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#666c70"/><stop offset="1" stop-color="#3e4448"/></linearGradient>
    <radialGradient id="qkUmb" cx=".62" cy=".2" r=".95"><stop offset="0" stop-color="#ff8a78"/><stop offset="1" stop-color="#b8241e"/></radialGradient>
    <linearGradient id="qkTaxi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb0d0"/><stop offset=".55" stop-color="#f070a4"/><stop offset="1" stop-color="#c84c84"/></linearGradient>
    <linearGradient id="qkCarWin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8eef8"/><stop offset=".45" stop-color="#6a8aa0"/><stop offset="1" stop-color="#2a3e4c"/></linearGradient>
    <linearGradient id="qkTrunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a3a2c"/><stop offset=".6" stop-color="#7a6248"/><stop offset="1" stop-color="#9a8062"/></linearGradient>
    <linearGradient id="qkWallStone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ece5d8"/><stop offset="1" stop-color="#dcd2c0"/></linearGradient>
    <linearGradient id="qkCeil" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f4f1ea"/><stop offset="1" stop-color="#d6d0c4"/></linearGradient>
    <linearGradient id="qkScallop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaea" stop-opacity=".95"/><stop offset=".3" stop-color="#fff4d8" stop-opacity=".5"/><stop offset="1" stop-color="#fff4d8" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkBrass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbe49a"/><stop offset=".5" stop-color="#dcb460"/><stop offset="1" stop-color="#a87e32"/></linearGradient>
    <linearGradient id="qkMirror" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef4f6"/><stop offset=".4" stop-color="#aec2cc"/><stop offset=".65" stop-color="#d4e0e6"/><stop offset="1" stop-color="#90a6b2"/></linearGradient>
    <linearGradient id="qkRedCab" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8483c"/><stop offset="1" stop-color="#a8221a"/></linearGradient>
    <linearGradient id="qkPot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2e2e30"/><stop offset=".62" stop-color="#6e6e72"/><stop offset=".8" stop-color="#8a8a8e"/><stop offset="1" stop-color="#3a3a3c"/></linearGradient>
    <linearGradient id="qkLeafG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#78c066"/><stop offset=".6" stop-color="#3e8a44"/><stop offset="1" stop-color="#2a6232"/></linearGradient>
    <linearGradient id="qkWalnut" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3e2a1e"/><stop offset=".55" stop-color="#6a4a36"/><stop offset="1" stop-color="#4a3226"/></linearGradient>
    <linearGradient id="qkDeskTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#faf6ee"/><stop offset="1" stop-color="#d6cebe"/></linearGradient>
    <linearGradient id="qkCork" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dcae70"/><stop offset="1" stop-color="#b6844a"/></linearGradient>
    <radialGradient id="qkHalo"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".9"/><stop offset=".45" stop-color="#ffd880" stop-opacity=".35"/><stop offset="1" stop-color="#ffd880" stop-opacity="0"/></radialGradient>
    <linearGradient id="qkSteelD" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7e868c"/><stop offset=".16" stop-color="#cfd5d8"/><stop offset=".3" stop-color="#9aa2a8"/><stop offset=".52" stop-color="#e6eaec"/><stop offset=".68" stop-color="#a8b0b6"/><stop offset="1" stop-color="#868e94"/></linearGradient>
    <linearGradient id="qkWainscot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4c2a2"/><stop offset="1" stop-color="#c2ae8c"/></linearGradient>
    <linearGradient id="qkRailT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f8"/><stop offset=".45" stop-color="#b8c0c6"/><stop offset="1" stop-color="#6e767c"/></linearGradient>
    <linearGradient id="qkLiftWL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d2d8dc"/><stop offset="1" stop-color="#9aa2a8"/></linearGradient>
    <linearGradient id="qkLiftWR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#d6dce0"/><stop offset="1" stop-color="#a0a8ae"/></linearGradient>
    <linearGradient id="qkLiftFl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4e52"/><stop offset="1" stop-color="#2e3236"/></linearGradient>
    <linearGradient id="qkWash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkRoomLight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset=".7" stop-color="#ffefd0"/><stop offset="1" stop-color="#d8b07a"/></linearGradient>
    <linearGradient id="qkSkyRefl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf6fc"/><stop offset="1" stop-color="#bcdcee"/></linearGradient>`;

  // ---------------- small helpers shared by the shots ----------------
  // a pendulum: rotation ±amp° around origin "x y", period per; it settles to rest after dur
  Qk.swing = (tl, sel, origin, t0, dur, amp = 6, per = 0.5) => {
    const n = Math.max(1, Math.round(dur / per)), end = n % 2 ? amp : -amp;
    tl.fromTo(sel, { rotation: -amp, svgOrigin: origin }, { rotation: amp, svgOrigin: origin, duration: per, repeat: n - 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(sel, { rotation: end, svgOrigin: origin }, { rotation: 0, svgOrigin: origin, duration: per * 1.6, ease: "elastic.out(1, 0.35)", immediateRender: false }, t0 + n * per);
  };
  // plaster bits shaken off a ceiling: o.pts(r) gives { x, y0, y1, s } for one bit (start, the floor it lands on, size); o.t0, o.dur, o.n
  Qk.debris = (tl, layer, o) => {
    const r = mk(o.seed || 5), n = o.n || 14, id = `qd${Math.floor(r() * 1e9)}`;
    const P = Array.from({ length: n }, () => ({ ...o.pts(r), t: r() * Math.max(0.1, o.dur - 0.8), rot: r() * 360, sp: 0.75 + r() * 0.5, c: ["#d8d2c6", "#b8b0a2", "#ece6da"][Math.floor(r() * 3)], dx: (r() - 0.5) * 50 }));
    put(layer, `<g id="${id}">${P.map((p, k) => `<path id="${id}-${k}" d="M0,${f1(-p.s)}L${f1(p.s * 0.9)},${f1(p.s * 0.3)}L${f1(-p.s * 0.5)},${f1(p.s * 0.8)}Z" fill="${p.c}" stroke="#8a8478" stroke-width="1" opacity="0"/>`).join("")}</g>`);
    P.forEach((p, k) => {
      const fall = Math.sqrt(Math.max(1, p.y1 - p.y0) / 1600) * 0.9 / p.sp;
      tl.fromTo(`#${id}-${k}`, { x: p.x, y: p.y0, rotation: p.rot, opacity: 1 }, { x: p.x + p.dx, y: p.y1, rotation: p.rot + 300 * p.sp, opacity: 1, duration: fall, ease: "power2.in", immediateRender: false }, o.t0 + p.t);
    });
  };

  // ---------------- the city ----------------
  // landmarks of the Bangkok skyline in hazy silhouette: x centre, hz the ground line, s scale, c body, l the sunlit edge, a the sky
  const LM = {
    baiyoke(x, hz, s, c, l) {
      const w = 110 * s, h = 1080 * s, t = hz - h, sw = Math.max(1.5, 7 * s);
      return `<rect x="${f1(x - w / 2)}" y="${f1(t)}" width="${f1(w)}" height="${f1(h + 900)}" fill="${c}"/><rect x="${f1(x + w / 2 - w * 0.17)}" y="${f1(t)}" width="${f1(w * 0.17)}" height="${f1(h + 900)}" fill="${l}"/>
        <rect x="${f1(x - w * 0.34)}" y="${f1(t - 72 * s)}" width="${f1(w * 0.68)}" height="${f1(74 * s)}" fill="${c}"/>
        <rect x="${f1(x - w * 0.64)}" y="${f1(t - 46 * s)}" width="${f1(w * 1.28)}" height="${f1(15 * s)}" rx="${f1(7 * s)}" fill="${c}"/><rect x="${f1(x - w * 0.64)}" y="${f1(t - 46 * s)}" width="${f1(w * 1.28)}" height="${f1(4 * s)}" rx="${f1(2 * s)}" fill="${l}"/>
        <rect x="${f1(x - w * 0.2)}" y="${f1(t - 124 * s)}" width="${f1(w * 0.4)}" height="${f1(54 * s)}" fill="${c}"/>
        <path d="M${f1(x)},${f1(t - 120 * s)}V${f1(t - 340 * s)}" stroke="${c}" stroke-width="${f1(sw)}"/><path d="M${f1(x - 18 * s)},${f1(t - 210 * s)}h${f1(36 * s)}M${f1(x - 11 * s)},${f1(t - 270 * s)}h${f1(22 * s)}" stroke="${c}" stroke-width="${f1(sw * 0.7)}"/>`;
    },
    mahanakhon(x, hz, s, c, l, a) {
      const w = 124 * s, h = 1260 * s, t = hz - h, r = mk(77);
      let g = `<path d="M${f1(x - w / 2)},${f1(hz + 900)}V${f1(t + 26 * s)}L${f1(x - w / 2 + 24 * s)},${f1(t)}H${f1(x + w / 2)}V${f1(hz + 900)}Z" fill="${c}"/><rect x="${f1(x + w / 2 - w * 0.15)}" y="${f1(t)}" width="${f1(w * 0.15)}" height="${f1(h + 900)}" fill="${l}"/>`;
      // the "pixels": a ribbon of cubes spiralling down the tower, bitten out of the silhouette where it turns a corner
      for (let k = 0; k < 74; k++) {
        const u = k / 73, th = u * Math.PI * 5.4 + 0.5, yy = t + 24 * s + u * h * 0.92, sx = Math.sin(th), q = (9 + r() * 15) * s, xx = x + sx * w * 0.52;
        if (Math.abs(sx) > 0.8) g += `<rect x="${f1(xx - q / 2)}" y="${f1(yy)}" width="${f1(q)}" height="${f1(q)}" fill="${a}"/>`;
        else if (Math.cos(th) > 0) g += `<rect x="${f1(xx - q / 2)}" y="${f1(yy)}" width="${f1(q)}" height="${f1(q)}" fill="${T(c, -0.12)}"/><rect x="${f1(xx - q / 2)}" y="${f1(yy)}" width="${f1(q)}" height="${f1(Math.max(1, q * 0.22))}" fill="${l}"/>`;
      }
      return g;
    },
    state(x, hz, s, c, l, a, gold) {
      const w = 200 * s, h = 760 * s, t = hz - h;
      let g = `<rect x="${f1(x - w / 2)}" y="${f1(t)}" width="${f1(w)}" height="${f1(h + 900)}" fill="${c}"/><rect x="${f1(x + w / 2 - w * 0.14)}" y="${f1(t)}" width="${f1(w * 0.14)}" height="${f1(h + 900)}" fill="${l}"/>`;
      for (let k = 1; k < 6; k++) g += `<rect x="${f1(x - w / 2 + k * w / 6 - 2 * s)}" y="${f1(t + 10 * s)}" width="${f1(Math.max(1, 4 * s))}" height="${f1(h + 300)}" fill="${l}" opacity=".45"/>`;
      // the columned drum and the golden dome on top
      g += `<rect x="${f1(x - w * 0.36)}" y="${f1(t - 62 * s)}" width="${f1(w * 0.72)}" height="${f1(64 * s)}" fill="${c}"/>`;
      for (let k = 0; k < 7; k++) g += `<rect x="${f1(x - w * 0.33 + k * w * 0.1)}" y="${f1(t - 56 * s)}" width="${f1(w * 0.04)}" height="${f1(52 * s)}" fill="${l}" opacity=".75"/>`;
      g += `<path d="M${f1(x - w * 0.31)},${f1(t - 62 * s)}A${f1(w * 0.31)},${f1(w * 0.33)} 0 0 1 ${f1(x + w * 0.31)},${f1(t - 62 * s)}Z" fill="${gold}"/>
        <path d="M${f1(x + w * 0.06)},${f1(t - 62 * s - w * 0.3)}A${f1(w * 0.31)},${f1(w * 0.33)} 0 0 1 ${f1(x + w * 0.3)},${f1(t - 66 * s)}" stroke="#fff6d0" stroke-width="${f1(Math.max(1, 4 * s))}" fill="none" opacity=".7"/>
        <path d="M${f1(x)},${f1(t - 62 * s - w * 0.32)}v${f1(-56 * s)}" stroke="${gold}" stroke-width="${f1(Math.max(1.5, 5 * s))}"/>`;
      return g;
    },
  };
  // one hazy far tower: flat, stepped, slanted, spired or pyramid-crowned; a sunlit right edge; faint floor lines
  const farTw = (x, w, h, hz, c, l, r, rows) => {
    const t = hz - h, kind = Math.floor(r() * 6);
    let g = `<rect x="${f1(x)}" y="${f1(t)}" width="${f1(w)}" height="${f1(h + 900)}" fill="${c}"/><rect x="${f1(x + w * 0.82)}" y="${f1(t)}" width="${f1(w * 0.18)}" height="${f1(h + 900)}" fill="${l}"/>`;
    if (kind === 1) g += `<rect x="${f1(x + w * 0.16)}" y="${f1(t - h * 0.07 - 6)}" width="${f1(w * 0.58)}" height="${f1(h * 0.07 + 7)}" fill="${c}"/>`;
    else if (kind === 2) g += `<path d="M${f1(x)},${f1(t + 1)}L${f1(x + w)},${f1(t - w * 0.38)}V${f1(t + 1)}Z" fill="${c}"/>`;
    else if (kind === 3) g += `<path d="M${f1(x + w * 0.5)},${f1(t)}V${f1(t - 50 - r() * 90)}" stroke="${c}" stroke-width="5"/>`;
    else if (kind === 4) g += `<path d="M${f1(x + w * 0.08)},${f1(t + 1)}L${f1(x + w * 0.5)},${f1(t - w * 0.42)}L${f1(x + w * 0.92)},${f1(t + 1)}Z" fill="${c}"/><path d="M${f1(x + w * 0.5)},${f1(t - w * 0.42)}L${f1(x + w * 0.92)},${f1(t + 1)}" stroke="${l}" stroke-width="4"/>`;
    if (rows) { let d = ""; for (let y = t + 12 + r() * 8; y < hz + 60; y += rows) d += `M${f1(x + 5)},${f1(y)}H${f1(x + w - 5)}`; g += `<path d="${d}" stroke="${l}" stroke-width="2.2" opacity=".5"/>`; }
    return g;
  };
  // palettes for the mid towers: [front, sunlit right face, shaded left face, mullion]
  const MGL = [["#7b9db6", "#b2d2e4", "#55758e"], ["#6c90ab", "#a6c8dc", "#4c6c86"], ["#8aaabf", "#c2dcea", "#62849c"], ["#7f98a8", "#b8ccd8", "#5a6e7c"]];
  const MCN = [["#cbc4b4", "#e8e2d4", "#9a9486"], ["#b6babb", "#d8dcda", "#8a8e90"], ["#d4c8b4", "#efe4d2", "#a2988a"], ["#c0b0a0", "#e0d2c0", "#90806e"]];
  Qk.city = (L, o = {}) => {
    const r = mk(o.seed || 11), hz = o.hz ?? 1300, x0 = o.x0 ?? -1500, x1 = o.x1 ?? 2700, id = o.id || "qc", below = !!o.below, vx = o.vx ?? (x0 + x1) / 2;
    // the sky: deep blue overhead, pale toward the horizon (user space, so every shot's horizon is light); thin cirrus high up
    let sk = `<defs><linearGradient id="${id}-sky" gradientUnits="userSpaceOnUse" x1="0" y1="${hz - 2600}" x2="0" y2="${hz}">
        <stop offset="0" stop-color="#3f8fd2"/><stop offset=".5" stop-color="#7fbce6"/><stop offset=".85" stop-color="#cfe6f2"/><stop offset="1" stop-color="#eaf3f2"/></linearGradient></defs>
      <rect x="-3000" y="${hz - 5000}" width="8000" height="${5000 + 1600}" fill="url(#${id}-sky)"/>`;
    for (let k = 0; k < 7; k++) { const cx = -800 + r() * 3200, cy = hz - 2300 + r() * 900, w = 500 + r() * 700; sk += `<path d="M${f1(cx)},${f1(cy)}q${f1(w * 0.5)},${f1(-18 - r() * 20)} ${f1(w)},${f1(-6 + r() * 12)}" stroke="#fff" stroke-width="${f1(8 + r() * 10)}" opacity="${f1(0.14 + r() * 0.14)}" stroke-linecap="round" fill="none"/>`; }
    sk += `<circle cx="${o.sunX ?? 1500}" cy="${hz - 1500}" r="520" fill="url(#qkSun)"/><circle cx="${o.sunX ?? 1500}" cy="${hz - 1500}" r="70" fill="#fffdf2" opacity=".9"/>`
      + [[-600, hz - 1100, 760, 230], [700, hz - 1380, 620, 190], [1900, hz - 900, 820, 240], [200, hz - 640, 520, 150]].map(([x, y, w, h]) => cloud2(x, y, w, h, r, "qkCloud", "#ffffff", "#9ab8cc")).join("");
    put(L.sky, sk);
    // far: the palest band, the landmarks, then a nearer band with floor lines; haze at the horizon
    let far = "";
    const FA = ["#bfd2de", "#c6d8e2", "#b8ccda"], FB = ["#a4bdcd", "#acc4d2", "#9ab6c8", "#b2c8d4"];
    for (let x = x0 - 100; x < x1 + 100;) { const w = (below ? 40 : 70) + r() * (below ? 90 : 140), h = (below ? 40 : 110) + Math.pow(r(), 1.8) * (below ? 170 : 520), c = FA[Math.floor(r() * 3)]; far += farTw(x, w, h, hz, c, T(c, 0.3), r, 0); x += w + r() * 20 - 6; }
    const ms = o.markS ?? (below ? 0.3 : 1), marks = o.marks || [["baiyoke", x0 + (x1 - x0) * 0.24], ["mahanakhon", x0 + (x1 - x0) * 0.6], ["state", x0 + (x1 - x0) * 0.84]];
    marks.forEach(([n, mx]) => { far += LM[n](mx, hz, ms, "#a2b9c9", "#cbdce6", "#d6e6ee", "#dcc890"); });
    for (let x = x0 + r() * 120; x < x1;) { const w = (below ? 50 : 90) + r() * (below ? 110 : 170), h = (below ? 60 : 150) + Math.pow(r(), 1.6) * (below ? 240 : 660), c = FB[Math.floor(r() * 4)]; far += farTw(x, w, h, hz, c, T(c, 0.24), r, 20 + r() * 10); x += w + r() * 50 + 14; }
    far += `<rect x="-3000" y="${hz - 420}" width="8000" height="1600" fill="url(#qkHazeBand)"/>`;
    put(L.far, far);
    if (o.mid === false) return;
    // mid: towers with a front face, a side face turned toward the frame centre, window grids, roofs
    let mid = "";
    for (let x = x0 + r() * 200; x < x1;) {
      const w = 170 + r() * 230, top = below ? hz - 340 + r() * 780 : hz - 260 - Math.pow(r(), 1.3) * 900, glass = r() < 0.55;
      const [cf, cl, cs] = (glass ? MGL : MCN)[Math.floor(r() * 4)], ctr = x + w / 2, toR = ctr < vx, bot = hz + 2400;
      const sw = Math.min(70, w * 0.24) * Math.min(1, Math.abs(ctr - vx) / 700 + 0.18), ex = toR ? x + w : x, fx = toR ? ex + sw : ex - sw;
      const run = (y) => y + (hz - y) * (sw / Math.max(260, Math.abs(vx - ex)));   // a line on the side face runs toward the horizon
      mid += PL([[ex, top], [fx, run(top)], [fx, bot], [ex, bot]], `fill="${toR ? cl : cs}"`);
      mid += `<rect x="${f1(x)}" y="${f1(top)}" width="${f1(w)}" height="${f1(bot - top)}" fill="${cf}"/>`;
      const fh = 24 + r() * 12, bw = 28 + r() * 20, wy1 = hz + (below ? 560 : 300);
      let hl = "", vl = "", cells = "", refl = "", side = "";
      for (let y = top + fh * 0.8; y < wy1; y += fh) { hl += `M${f1(x + 4)},${f1(y)}H${f1(x + w - 4)}`; side += `M${f1(ex)},${f1(y)}L${f1(fx)},${f1(run(y))}`; }
      if (glass) {
        for (let xx = x + bw; xx < x + w - 6; xx += bw) vl += `M${f1(xx)},${f1(top + 6)}V${f1(wy1)}`;
        for (let y = top + fh * 0.8; y < wy1 - fh; y += fh) for (let xx = x; xx < x + w - bw; xx += bw) if (r() < 0.13) refl += `M${f1(xx + 3)},${f1(y + 4)}h${f1(bw - 6)}v${f1(fh - 8)}h${f1(-(bw - 6))}Z`;
        mid += `<path d="${refl}" fill="#e6f4fb" opacity=".5"/><path d="${hl}" stroke="${T(cf, -0.32)}" stroke-width="4" opacity=".55"/><path d="${vl}" stroke="${T(cf, -0.25)}" stroke-width="2" opacity=".5"/>
          <path d="M${f1(x)},${f1(top + w * 1.3)}L${f1(x + w * 0.55)},${f1(top)}H${f1(x + w * 0.78)}L${f1(x)},${f1(top + w * 2.1)}Z" fill="#fff" opacity=".1"/>`;
      } else {
        for (let y = top + fh * 0.8; y < wy1 - fh; y += fh) for (let xx = x + 8; xx < x + w - bw; xx += bw) cells += `M${f1(xx + 4)},${f1(y + 5)}h${f1(bw - 10)}v${f1(fh - 11)}h${f1(-(bw - 10))}Z`;
        mid += `<path d="${cells}" fill="${T(cf, -0.4)}" opacity=".62"/><path d="${hl}" stroke="${T(cf, 0.35)}" stroke-width="3" opacity=".5"/>`;
      }
      mid += `<path d="${side}" stroke="${T(toR ? cl : cs, -0.2)}" stroke-width="2" opacity=".5"/><rect x="${f1(x - 3)}" y="${f1(top - 8)}" width="${f1(w + 6)}" height="9" fill="${T(cf, 0.35)}"/>`;
      if (below && top > hz + 10) {
        // the roof seen from above: its top face recedes toward the vanishing point; tanks, AC units, a helipad, a garden or a pool
        const f = 0.12, far2 = (px, py) => [px + (vx - px) * f, py + (hz - py) * f], a = [x - 3, top - 8], b = [x + w + 3, top - 8], c = far2(...b), d = far2(...a);
        mid += PL([a, b, c, d], `fill="${T(cf, 0.42)}"`) + `<path d="M${pt(a)}L${pt(d)}L${pt(c)}" stroke="${T(cf, 0.6)}" stroke-width="3" fill="none"/>`;
        const mx = (a[0] + b[0] + c[0] + d[0]) / 4, my = (a[1] + b[1] + c[1] + d[1]) / 4, rh = Math.abs(a[1] - d[1]), roll = r();
        if (roll < 0.25) mid += `<ellipse cx="${f1(mx)}" cy="${f1(my)}" rx="${f1(w * 0.22)}" ry="${f1(rh * 0.32)}" fill="#5a5e60" stroke="#f2f0ea" stroke-width="3"/><text x="${f1(mx)}" y="${f1(my + rh * 0.12)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="${f1(rh * 0.36)}" fill="#f2f0ea" transform="scale(1,0.6)" transform-origin="${f1(mx)} ${f1(my)}">H</text>`;
        else if (roll < 0.45) mid += [0, 1, 2, 3, 4].map((k) => `<ellipse cx="${f1(mx - w * 0.3 + k * w * 0.15)}" cy="${f1(my + (k % 2) * 4 - 2)}" rx="${f1(w * 0.08)}" ry="${f1(rh * 0.2)}" fill="${["#5e9a4e", "#4a8a44", "#6aa858"][k % 3]}"/>`).join("");
        else if (roll < 0.58) mid += `<rect x="${f1(mx - w * 0.25)}" y="${f1(my - rh * 0.22)}" width="${f1(w * 0.5)}" height="${f1(rh * 0.44)}" fill="#6ad0e8" stroke="#e8f8fc" stroke-width="2"/>`;
        else mid += `<rect x="${f1(mx - w * 0.3)}" y="${f1(my - rh * 0.3)}" width="${f1(w * 0.18)}" height="${f1(rh * 0.5)}" fill="#cfcac0"/><ellipse cx="${f1(mx + w * 0.15)}" cy="${f1(my - 4)}" rx="${f1(w * 0.08)}" ry="${f1(rh * 0.18)}" fill="#e6e2da" stroke="#9a968e" stroke-width="2"/><rect x="${f1(mx + w * 0.05)}" y="${f1(my - 4)}" width="${f1(w * 0.2)}" height="10" fill="#bcb8b0"/>`;
      } else {
        // rooftop kit above the parapet: water tanks, AC units, antennas, now and then a crane
        if (r() < 0.55) { const tx = x + w * (0.15 + r() * 0.4); mid += `<rect x="${f1(tx)}" y="${f1(top - 46)}" width="40" height="38" fill="${T(cf, 0.15)}"/><ellipse cx="${f1(tx + 20)}" cy="${f1(top - 46)}" rx="20" ry="6" fill="${T(cf, 0.45)}"/><rect x="${f1(tx + 28)}" y="${f1(top - 46)}" width="12" height="38" fill="${T(cf, -0.1)}"/>`; }
        if (r() < 0.5) mid += [0, 1, 2].map((k) => `<rect x="${f1(x + w * 0.6 + k * 22)}" y="${f1(top - 22)}" width="18" height="14" fill="${T(cf, 0.25)}"/>`).join("");
        if (r() < 0.35) mid += `<path d="M${f1(x + w * 0.82)},${f1(top - 8)}V${f1(top - 90 - r() * 70)}" stroke="${T(cf, -0.2)}" stroke-width="4"/>`;
        if (r() < 0.12) { const cx = x + w * 0.5, cy = top; mid += `<g stroke="#e0a43a" stroke-width="6" fill="none"><path d="M${f1(cx)},${f1(cy)}V${f1(cy - 420)}M${f1(cx - 60)},${f1(cy - 400)}H${f1(cx + 300)}"/><path d="M${f1(cx)},${f1(cy - 420)}L${f1(cx + 300)},${f1(cy - 400)}M${f1(cx)},${f1(cy - 420)}L${f1(cx - 60)},${f1(cy - 400)}" stroke-width="3"/><path d="M${f1(cx + 220)},${f1(cy - 400)}v80" stroke="#555" stroke-width="2"/></g>`; }
      }
      x += w + 40 + r() * 140;
    }
    mid += `<rect x="-3000" y="${hz - 200}" width="8000" height="900" fill="url(#qkHazeBand)" opacity="${below ? 0.35 : 0.6}"/>`;
    put(L.mid, mid);
  };

  // ---------------- the condo, outside ----------------
  const FH = 96, NF = 32;
  // a rain tree standing at (0,0): trunk with branches, a layered crown lit from the right
  const rainTree = (r, R = 250) => {
    let g = CS(-30, 6, R * 0.9, 20, 0.9);
    g += `<path d="M-22,0Q-26,-160 -14,-300Q-90,-360 -170,-380L-160,-396Q-80,-372 -2,-330Q4,-400 50,-470L66,-460Q30,-394 22,-320Q90,-350 170,-356L170,-338Q90,-330 26,-290Q20,-150 26,0Z" fill="url(#qkTrunk)" ${OUT3}/>`;
    g += `<path d="M-6,-20Q-8,-150 -2,-280" stroke="#3a2c20" stroke-width="3" opacity=".5" fill="none"/>`;
    g += crown(0, -470, R, r, ["url(#p2LeafD)", "url(#p2LeafM)", "url(#p2LeafL)", "#c8e08a"], 16);
    g += crown(-R * 0.62, -380, R * 0.52, r, ["url(#p2LeafD)", "url(#p2LeafM)", "url(#p2LeafL)", "#c8e08a"], 9);
    g += crown(R * 0.66, -400, R * 0.5, r, ["url(#p2LeafD)", "url(#p2LeafM)", "url(#p2LeafL)", "#d8ec9a"], 9);
    return g;
  };
  // a concrete utility pole standing at (0,0), h tall: cross-arms with insulators, a lamp arm, o.trans a transformer drum, o.sign a soi sign
  const pole = (h, o = {}) => {
    let g = CS(0, 4, 40, 8);
    g += `<path d="M-13,0L-8,${-h}H8L13,0Z" fill="url(#qkPoleG)" ${OUT2}/><path d="M-11,-20H11M-10.5,-60H10.5" stroke="#7a7e7a" stroke-width="2" opacity=".6"/>`;
    for (const [y, w] of [[h - 22, 64], [h - 64, 54]]) g += `<rect x="${-w}" y="${-y - 6}" width="${2 * w}" height="10" fill="#9a9e9a" ${OUT2}/>` + [-w + 8, -w / 3, w / 3, w - 8].map((x) => `<path d="M${f1(x - 4)},${-y - 6}h8v-9h-8z" fill="#f2f0ea" stroke="#6a6e6a" stroke-width="1.5"/>`).join("");
    g += `<path d="M6,${-h + 110}Q60,${-h + 92} 96,${-h + 104}" stroke="#7a7e7a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M84,${-h + 98}h36l-6,14h-24z" fill="#5a5e60" ${OUT2}/><path d="M90,${-h + 112}h24" stroke="#fff6d0" stroke-width="4"/>`;
    if (o.trans) g += `<g transform="translate(-30,${-h + 190})"><rect x="-22" y="-34" width="44" height="64" rx="8" fill="#9aa0a2" ${OUT2}/><path d="M-22,-20h44M-22,-6h44M-22,8h44" stroke="#6a7072" stroke-width="2"/><rect x="-22" y="-34" width="10" height="64" rx="4" fill="#fff" opacity=".3"/><path d="M22,-10h16" stroke="#7a7e7a" stroke-width="6"/></g>`;
    if (o.coil) g += `<g transform="translate(10,${-h + 250})" fill="none" stroke="#1e2226" stroke-width="3"><ellipse rx="26" ry="18"/><ellipse rx="22" ry="15" transform="rotate(12)"/><ellipse rx="28" ry="16" transform="rotate(-8)"/></g>`;
    if (o.sign) g += `<g transform="translate(-14,${-h + 300})"><rect x="-96" y="-22" width="96" height="40" rx="5" fill="#1e5aa8" stroke="#f2f4f6" stroke-width="3"/><text x="-48" y="6" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#fff">${o.sign}</text></g>`;
    return g;
  };
  function qkTower(L, o = {}) {
    const id = o.id || "tw", r = mk(o.seed || 21), G = 1720, X0 = 290, X1 = 790, SIDE = 92, top = G - NF * FH, HZ = G - 120;
    Qk.city(L, { hz: HZ, seed: o.seed || 13, id: `${id}c`, sunX: 1650, vx: 560, marks: [["state", -330], ["baiyoke", 70], ["mahanakhon", 1060]] });
    const sy = (y) => 30 * (HZ - y) / (HZ - top);   // how far a side-face line drops across the side face at height y

    // ---- the street surface: pavement with a tactile strip, kerb, road with its markings, shadows
    let st = `<rect x="-1600" y="${G - 4}" width="4400" height="64" fill="url(#qkPave)"/>`;
    let tj = `M-1600,${G + 26}H2800`;
    for (let x = -1600; x < 2800; x += 52) tj += `M${x},${G - 4}V${G + 60}`;
    st += `<path d="${tj}" stroke="#ada592" stroke-width="2" opacity=".7"/><rect x="-1600" y="${G + 34}" width="4400" height="12" fill="#e8c43a"/>`;
    let dots = ""; for (let x = -1594; x < 2800; x += 12) dots += `M${x},${G + 40}h3`;
    st += `<path d="${dots}" stroke="#b8941e" stroke-width="5"/>`;
    st += `<rect x="-1600" y="${G + 56}" width="4400" height="8" fill="#e6e2da"/><rect x="-1600" y="${G + 64}" width="4400" height="12" fill="#a8a49c"/>`;
    st += [...Array(12)].map((_, k) => `<rect x="${880 + k * 40}" y="${G + 56}" width="20" height="20" fill="#d8312a" opacity=".9"/>`).join("");
    st += `<rect x="-1600" y="${G + 76}" width="4400" height="900" fill="url(#qkAsph)"/><rect x="-1600" y="${G + 76}" width="4400" height="16" fill="#2a2e30" opacity=".35"/>`;
    st += `<path d="M-1600,${G + 360}H2800" stroke="#f2f0ea" stroke-width="10" stroke-dasharray="90 70" opacity=".85"/><path d="M-1600,${G + 150}H2800M-1600,${G + 270}H2800" stroke="#2e3236" stroke-width="26" opacity=".18"/>`;
    st += `<ellipse cx="480" cy="${G + 210}" rx="46" ry="12" fill="#4e5458" stroke="#2e3236" stroke-width="3"/><path d="M450,${G + 206}h60M454,${G + 212}h52" stroke="#3a3e42" stroke-width="2"/>`;
    st += `<rect x="620" y="${G + 78}" width="70" height="14" fill="#2a2e30"/><path d="M628,${G + 80}v10M640,${G + 80}v10M652,${G + 80}v10M664,${G + 80}v10M676,${G + 80}v10" stroke="#7a7e80" stroke-width="2"/>`;
    // the tower's shade on the pavement (sun high on the right) and the canopy's shade by the door
    st += `<path d="M${X0 - 120},${G - 2}H${X0 + 30}L${X0 - 30},${G + 56}H${X0 - 200}Z" fill="#1a2a36" opacity=".14"/>`;

    // ---- the tower
    let tw = "";
    // the side face (sunlit): glass, receding slab edges, curtains, one mullion
    tw += PL([[X1, top], [X1 + SIDE, top + 30], [X1 + SIDE, G - 1], [X1, G]], `fill="url(#qkFacSide)"`);
    let sSlab = "", sShad = "", sCur = "";
    for (let n = 1; n <= NF; n++) {
      const y = G - n * FH, d = sy(y), dn = sy(y + FH), at = (x, yy, dd) => [X1 + x, yy + (dd * x) / SIDE];
      sSlab += SP([at(0, y, d), at(SIDE, y, d), at(SIDE, y + 11, d), at(0, y + 12, d)]);
      sShad += SP([at(0, y + 12, d), at(SIDE, y + 11, d), at(SIDE, y + 20, d), at(0, y + 21, d)]);
      if (n > 2 && r() < 0.5) { const a = 6 + r() * 34, b = a + 16 + r() * 30; sCur += SP([at(a, y + 22, d), at(Math.min(SIDE - 4, b), y + 22, d), at(Math.min(SIDE - 4, b), y + FH, dn), at(a, y + FH, dn)]); }
    }
    tw += `<path d="${sCur}" fill="#f6efe2" opacity=".72"/><path d="${sShad}" fill="#2e5a78" opacity=".24"/><path d="${sSlab}" fill="#fbfbf8"/>`;
    tw += `<path d="M${X1 + 50},${top + 16}V${G - 250}" stroke="#4a7a98" stroke-width="4" opacity=".6"/><path d="M${X1 + 53},${top + 16}V${G - 250}" stroke="#fff" stroke-width="2" opacity=".6"/>`;
    tw += PL([[X1, top - 18], [X1 + SIDE, top + 12], [X1 + SIDE, top + 30], [X1, top]], `fill="#f6f6f2"`) + `<path d="M${X1},${G}V${top - 18}" stroke="#bcc6cc" stroke-width="4"/>`;
    // the front face: glass that holds the sky, brighter up high
    tw += `<rect x="${X0}" y="${top}" width="${X1 - X0}" height="${NF * FH}" fill="url(#qkFacG)"/>`;
    // windows: deep rooms, curtains (drawn, half, sheer), a lamp left on
    const CUR = ["#f6f0e4", "#ebe4d6", "#dfe3e4", "#f2e4c8", "#cfd6da"];
    let deep = "", sheer = "", warm = "", fold = "";
    const cur = CUR.map(() => "");
    for (let n = 3; n <= NF; n++) {
      const y = G - n * FH;
      for (let b = 0; b < 5; b++) {
        const bx = X0 + b * 100, wy0 = y + 14, wy1 = y + FH, roll = r();
        if (roll < 0.2) deep += `M${bx + 4},${wy0 + 8}h92v${wy1 - wy0 - 10}h-92Z`;
        else if (roll < 0.62) {
          const c = Math.floor(r() * CUR.length), m = r();
          const [a, w] = m < 0.34 ? [4, 92] : m < 0.67 ? [4, 40 + r() * 20] : [52 - r() * 10, 44 + r() * 8];
          cur[c] += `M${f1(bx + a)},${wy0 + 4}h${f1(w)}v${wy1 - wy0 - 4}h${f1(-w)}Z`;
          for (let f = a + 10; f < a + w - 4; f += 12) fold += `M${f1(bx + f)},${wy0 + 6}V${wy1 - 2}`;
        } else if (roll < 0.74) sheer += `M${bx + 4},${wy0 + 4}h92v${wy1 - wy0 - 4}h-92Z`;
        if (r() < 0.025) warm += `M${bx + 20},${wy0 + 20}h40v${wy1 - wy0 - 28}h-40Z`;
      }
    }
    tw += `<path d="${deep}" fill="#24445e" opacity=".5"/>` + cur.map((d, k) => `<path d="${d}" fill="${CUR[k]}" opacity=".88"/>`).join("") + `<path d="${fold}" stroke="#9a8e78" stroke-width="2" opacity=".28"/><path d="${sheer}" fill="#fff" opacity=".28"/><path d="${warm}" fill="#ffe2a0" opacity=".55"/>`;
    // the sky's reflection sliding over the glass
    tw += `<path d="M${X0},${top + 900}L${X0 + 200},${top + 300}L${X0 + 300},${top + 300}L${X0 + 100},${top + 900}Z" fill="#fff" opacity=".16"/><path d="M${X0 + 120},${top + 2200}L${X0 + 380},${top + 1400}L${X0 + 430},${top + 1400}L${X0 + 170},${top + 2200}Z" fill="#fff" opacity=".12"/>
      <path d="M${X0 + 300},${top + 1200}L${X0 + 500},${top + 600}V${top + 760}L${X0 + 352},${top + 1200}Z" fill="#fff" opacity=".08"/>`;
    // mullions with depth (a shadow line and a lit edge)
    let mu = "", muL = "";
    for (let b = 1; b < 5; b++) { mu += `M${X0 + b * 100},${top + 10}V${G - 250}`; muL += `M${X0 + b * 100 + 3},${top + 10}V${G - 250}`; }
    tw += `<path d="${mu}" stroke="#1e3a50" stroke-width="5" opacity=".6"/><path d="${muL}" stroke="#e4f2fa" stroke-width="2" opacity=".7"/>`;
    // balconies: level n's rail sits on its floor slab (y G-(n-1)·FH); odd levels on the left two bays, even levels on the right two
    const bal = (n) => (n >= 4 && n <= 31 ? (n % 2 ? [X0 - 8, X0 + 200] : [X0 + 300, X1 + 8]) : null);
    let items = "", rail = "", railTop = "", posts = "", slabs = "", slabHi = "", slabSh = "", lip = "", lipSh = "";
    for (let n = 1; n <= NF; n++) {
      const y = G - n * FH;
      slabs += `M${X0 - 6},${y}h${X1 - X0 + 12}v12h${-(X1 - X0 + 12)}Z`; slabHi += `M${X0 - 6},${y + 1}h${X1 - X0 + 12}`; slabSh += `M${X0},${y + 12}h${X1 - X0}v10h${-(X1 - X0)}Z`;
      const bb = bal(n + 1);
      if (bb) { lip += `M${bb[0]},${y - 3}h${bb[1] - bb[0]}v18h${-(bb[1] - bb[0])}Z`; lipSh += `M${bb[0] + 6},${y + 15}h${bb[1] - bb[0] - 12}v12h${-(bb[1] - bb[0] - 12)}Z`; }
      const b = bal(n);
      if (!b) continue;
      const fy = y + FH, [bx0, bx1] = b, bw = bx1 - bx0, roll = r();
      if (roll < 0.5) { const ax = bx0 + 12 + r() * (bw - 74); items += `<rect x="${f1(ax)}" y="${fy - 33}" width="50" height="33" rx="3" fill="#eceee8" ${OUT2}/><circle cx="${f1(ax + 18)}" cy="${fy - 16}" r="11" fill="#5a6064" stroke="#8a9094" stroke-width="2"/><path d="M${f1(ax + 18)},${fy - 26}v20M${f1(ax + 8)},${fy - 16}h20" stroke="#9aa0a4" stroke-width="2"/><rect x="${f1(ax + 34)}" y="${fy - 28}" width="12" height="22" fill="#d4d6d0"/>`; }
      if (r() < 0.38) { const px = bx0 + 20 + r() * (bw - 40); items += `<path d="M${f1(px - 8)},${fy}l-2,-14h20l-2,14z" fill="#b86a3a"/>` + [0, 1, 2].map((k) => `<ellipse cx="${f1(px - 8 + k * 8)}" cy="${fy - 24 - (k % 2) * 6}" rx="9" ry="7" fill="${["#3e8a44", "#5aa858", "#2e7a3a"][k]}"/>`).join(""); }
      if (r() < 0.14) { const lx = bx0 + 30 + r() * (bw - 110); items += `<path d="M${f1(lx)},${fy - 44}h70" stroke="#8a8a8a" stroke-width="2"/>` + [0, 1, 2].map((k) => `<path d="M${f1(lx + 4 + k * 22)},${fy - 44}h16l2,${16 + (k % 2) * 6}h-20z" fill="${["#e8443a", "#3a7ad8", "#f2c230"][k]}" opacity=".9"/>`).join(""); }
      rail += `M${bx0},${fy - 44}h${bw}v42h${-bw}Z`; railTop += `M${bx0},${fy - 44}h${bw}`;
      for (let px = bx0 + 4; px <= bx1; px += 49) posts += `M${f1(px)},${fy - 44}V${fy - 2}`;
    }
    tw += items + `<path d="${rail}" fill="#e2f4fb" opacity=".38"/><path d="${posts}" stroke="#c8d6dc" stroke-width="2.5"/><path d="${railTop}" stroke="#eef4f6" stroke-width="5" stroke-linecap="round"/>`;
    tw += `<path d="${slabSh}" fill="#16364e" opacity=".22"/><path d="${slabs}" fill="#f4f3ee"/><path d="${slabHi}" stroke="#fff" stroke-width="2"/><path d="${lipSh}" fill="#16364e" opacity=".26"/><path d="${lip}" fill="#fbfbf8" stroke="#c4cacc" stroke-width="1.5"/>`;
    tw += `<g id="${id}-f27" opacity="0"><rect x="${X0}" y="${G - 27 * FH + 14}" width="${X1 - X0}" height="${FH - 14}" fill="#ffe9a0" opacity=".55"/><rect x="${X0}" y="${G - 27 * FH + 14}" width="${X1 - X0}" height="${FH - 14}" fill="none" stroke="#fff6c8" stroke-width="6"/></g>`;
    // the fin: lit right half, shaded left half
    tw += `<rect x="${X0 + 236}" y="${top - 40}" width="14" height="${NF * FH + 40 - 250}" fill="#d6d8d4"/><rect x="${X0 + 250}" y="${top - 40}" width="14" height="${NF * FH + 40 - 250}" fill="#fbfbf8"/><path d="M${X0 + 236},${top - 40}V${G - 250}M${X0 + 264},${top - 40}V${G - 250}" stroke="#a8b0b4" stroke-width="2"/>`;
    // the lobby at the street: warm interior, glass and frames, the doors, the canopy with its crack, the name, columns, planters
    tw += `<rect x="${X0 + 30}" y="${G - 250}" width="440" height="250" fill="#2a2c2e"/><rect x="${X0 + 40}" y="${G - 240}" width="420" height="240" fill="#3e3428"/>
      <rect x="${X0 + 40}" y="${G - 240}" width="420" height="120" fill="#5a4a36" opacity=".6"/><rect x="${X0 + 120}" y="${G - 110}" width="160" height="60" fill="#6a5440"/><rect x="${X0 + 120}" y="${G - 114}" width="160" height="8" fill="#e8dcc8"/>
      ${[X0 + 110, X0 + 250, X0 + 390].map((x) => `<path d="M${x},${G - 240}v40" stroke="#1e1a16" stroke-width="2"/><circle cx="${x}" cy="${G - 192}" r="10" fill="#ffe6a8"/><circle cx="${x}" cy="${G - 192}" r="30" fill="#ffd27a" opacity=".25"/>`).join("")}
      <rect x="${X0 + 40}" y="${G - 240}" width="420" height="240" fill="#bfe0f0" opacity=".22"/>
      <path d="M${X0 + 40},${G - 240}h420M${X0 + 145},${G - 240}V${G}M${X0 + 355},${G - 240}V${G}M${X0 + 250},${G - 240}V${G}" stroke="#2c3a46" stroke-width="7"/>
      <path d="M${X0 + 60},${G - 20}L${X0 + 130},${G - 230}H${X0 + 150}L${X0 + 80},${G - 20}Z" fill="#fff" opacity=".2"/><path d="M${X0 + 270},${G - 20}L${X0 + 340},${G - 230}H${X0 + 350}L${X0 + 280},${G - 20}Z" fill="#fff" opacity=".16"/>
      <path d="M${X0 + 236},${G - 140}v70M${X0 + 264},${G - 140}v70" stroke="#c8ccce" stroke-width="7" stroke-linecap="round"/>
      <path d="M${X0 + 10},${G - 304}H${X0 + 490}L${X0 + 512},${G - 270}H${X0 - 12}Z" fill="#f4f4f0" ${OUT3}/><rect x="${X0 - 12}" y="${G - 270}" width="524" height="10" fill="#c8ccce"/><rect x="${X0 + 20}" y="${G - 260}" width="460" height="14" fill="#1a2a36" opacity=".3"/>
      <path id="${id}-crack" d="M${X0 + 300},${G - 300}l-14,14l10,8l-18,10" stroke="${INK}" stroke-width="3" fill="none"/>
      <rect x="${X0 + 120}" y="${G - 352}" width="260" height="48" rx="6" fill="#1e2a34"/><text x="${X0 + 250}" y="${G - 316}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="url(#qkBrass)">เดอะสกาย 32</text>
      <rect x="${X0 + 26}" y="${G - 270}" width="16" height="270" fill="#e8e8e2" ${OUT2}/><rect x="${X0 + 458}" y="${G - 270}" width="16" height="270" fill="#e8e8e2" ${OUT2}/>`;
    for (const [px, w] of [[X0 - 40, 70], [X0 + 470, 76]]) {
      tw += `<rect x="${px}" y="${G - 44}" width="${w}" height="44" fill="#d8d6d0" ${OUT2}/><rect x="${px}" y="${G - 44}" width="${w}" height="6" fill="#f4f2ee"/>`;
      for (let k = 0; k < 4; k++) tw += `<circle cx="${px + 10 + k * (w - 20) / 3}" cy="${G - 52 - (k % 2) * 8}" r="${16 + (k % 2) * 4}" fill="${["#3e8a44", "#4e9a4a", "#2e7a3a", "#5aa858"][k]}"/>`;
      for (let k = 0; k < 7; k++) tw += `<circle cx="${f1(px + 6 + r() * (w - 12))}" cy="${f1(G - 50 - r() * 22)}" r="4" fill="${r() < 0.6 ? "#e8508a" : "#f6a8c8"}"/>`;
    }
    // the roof: parapet, the lift room with louvres, a door and the mast with the red aviation light
    tw += `<rect x="${X0 - 6}" y="${top - 18}" width="${X1 - X0 + 12}" height="18" fill="#f2f2ee"/><path d="M${X0 - 6},${top - 17}h${X1 - X0 + 12}" stroke="#fff" stroke-width="2"/>
      <rect x="${X0 + 20}" y="${top - 120}" width="150" height="102" fill="#e8e8e2" ${OUT3}/>${PL([[X0 + 170, top - 120], [X0 + 186, top - 114], [X0 + 186, top - 18], [X0 + 170, top - 18]], `fill="#fbfbf8" ${OUT2}`)}
      <path d="M${X0 + 36},${top - 104}h52M${X0 + 36},${top - 96}h52M${X0 + 36},${top - 88}h52M${X0 + 36},${top - 80}h52" stroke="#9aa0a4" stroke-width="3"/><rect x="${X0 + 108}" y="${top - 76}" width="40" height="58" fill="#b8bec2" ${OUT2}/>
      <path d="M${X0 + 70},${top - 120}V${top - 290}" stroke="#7a8084" stroke-width="5"/><path d="M${X0 + 70},${top - 200}l-18,80M${X0 + 70},${top - 200}l18,80" stroke="#9aa0a4" stroke-width="2"/>
      <g id="${id}-beacon"><circle cx="${X0 + 70}" cy="${top - 294}" r="22" fill="url(#qkEmg)"/><circle cx="${X0 + 70}" cy="${top - 294}" r="7" fill="#ff3a2a"/></g>`;
    tw += `<defs><clipPath id="${id}-poolc"><rect x="${X0 + 190}" y="${top - 70}" width="${X1 - X0 - 200}" height="70"/></clipPath></defs>
      <g clip-path="url(#${id}-poolc)"><g id="${id}-wat"><path d="M${X0 + 150},${top - 46}Q${X0 + 300},${top - 56} ${X0 + 450},${top - 46}T${X1 + 60},${top - 46}V${top + 40}H${X0 + 150}Z" fill="url(#qkWater)"/>
        <path d="M${X0 + 200},${top - 44}q40,-8 80,0t80,0t80,0" stroke="#e8fbff" stroke-width="4" fill="none" opacity=".8"/></g></g>
      <rect x="${X0 + 190}" y="${top - 74}" width="${X1 - X0 - 200}" height="56" fill="#cfeef8" opacity=".35"/><path d="M${X0 + 190},${top - 74}H${X1 - 10}" stroke="#eef8fb" stroke-width="5"/>
      ${[X0 + 240, X0 + 330, X0 + 420].map((x) => `<path d="M${x},${top - 74}V${top - 18}" stroke="#d8e6ec" stroke-width="2"/>`).join("")}`;
    // rooftop palms (each sways on its own)
    [X0 + 200, X1 - 40].forEach((px, k) => {
      let p = `<path d="M-4,0Q6,-60 -4,-112" stroke="#7a5a3a" stroke-width="9" fill="none" stroke-linecap="round"/>`;
      for (let j = 0; j < 7; j++) p += `<path d="M${f1(-5 + Math.sin(j) * 2)},${-14 - j * 14}h9" stroke="#5a4028" stroke-width="2"/>`;
      const fr = [[-80, -100], [70, -120], [-50, -150], [40, -158], [-88, -128], [86, -96]];
      fr.forEach(([ex, ey], j) => { p += `<path d="M-4,-112Q${f1(ex * 0.5)},${f1(ey - 30)} ${ex},${ey}" stroke="${j % 2 ? "#3e8a4a" : "#2e7a3e"}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
        for (let q = 1; q < 6; q++) { const u = q / 6, mx = -4 + (ex + 4) * u, my = -112 + (ey + 112) * u - Math.sin(u * Math.PI) * 26; p += `<path d="M${f1(mx)},${f1(my)}l${f1(Math.sign(ex) * 6)},${f1(14 - q)}" stroke="#4e9a54" stroke-width="3" stroke-linecap="round"/>`; } });
      p += `<circle cx="-8" cy="-108" r="5" fill="#8a6a2a"/><circle cx="2" cy="-106" r="5" fill="#7a5a22"/>`;
      tw += `<g transform="translate(${px},${top - 18})"><g id="${id}-palm${k}">${p}</g></g>`;
    });
    tw += `<g transform="translate(${X1 - 60},${top + 160})">${PL([[80, -34], [96, -30], [96, 26], [80, 22]], `fill="#33485a"`)}<rect x="-120" y="-34" width="200" height="56" rx="8" fill="#1e2e3a"/><text x="-20" y="8" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#f6e2a0">เดอะสกาย 32</text><path d="M-112,-30h184" stroke="#fff" stroke-width="2" opacity=".25"/></g>`;
    tw += `<path id="${id}-spillL" d="M${X0 + 186},${top - 20}C${X0 + 150},${top + 60} ${X0 + 120},${top + 400} ${X0 + 90},${top + 900}L${X0 + 30},${top + 900}C${X0 + 70},${top + 400} ${X0 + 110},${top + 40} ${X0 + 186},${top - 20}Z" fill="url(#qkSpill)" opacity="0"/>
      <path id="${id}-spillR" d="M${X1 - 10},${top - 20}C${X1 + 40},${top + 60} ${X1 + 80},${top + 400} ${X1 + 120},${top + 900}L${X1 + 180},${top + 900}C${X1 + 120},${top + 400} ${X1 + 60},${top + 40} ${X1 - 10},${top - 20}Z" fill="url(#qkSpill)" opacity="0"/>`;
    tw += `<g id="${id}-birds">${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${X0 + 220 + k * 46},${top - 80}q8,-8 16,0q8,-8 16,0" stroke="#2a2e34" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    put(L.set, st + `<g id="${id}-tw">${tw}</g>`);

    // ---- in front of the tower: trees, poles and the wire tangle, the street-food cart, the taxi, your bike, bollards
    let fr = "";
    fr += `<g transform="translate(-330,${G + 40})"><g id="${id}-tree0">${rainTree(r, 250)}</g></g>`;
    fr += `<g transform="translate(1320,${G + 40})"><g id="${id}-tree1">${rainTree(r, 230)}</g></g>`;
    const PH = 390, poles = [[40, { sign: "ซอยสุขใจ" }], [1140, { trans: true, coil: true }]];
    poles.forEach(([px, po], k) => { fr += `<g transform="translate(${px},${G + 50})"><g id="${id}-pole${k}">${pole(PH, po)}</g></g>`; });
    // the wires: each hangs between two attachment points at the same height; sags differ; a fat telecom bundle lower down
    const att = [[-56, PH - 28], [-21, PH - 28], [21, PH - 28], [56, PH - 28], [-46, PH - 70], [-15, PH - 70], [15, PH - 70], [46, PH - 70]];
    const spans = [[-1700, 40], [40, 1140], [1140, 2900]];
    let wires = "", wi = 0;
    spans.forEach(([a, b], si) => {
      att.forEach(([dx, h], k) => {
        const xa = a + (si === 0 ? 0 : dx), xb = b + (si === 2 ? 0 : dx), y = G + 50 - h, sag = (b - a) * (0.035 + ((k * 7 + si * 3) % 5) * 0.008);
        wires += `<g id="${id}-w${wi}" data-o="${f1((xa + xb) / 2)} ${f1(y)}"><path d="M${f1(xa)},${f1(y)}Q${f1((xa + xb) / 2)},${f1(y + 2 * sag)} ${f1(xb)},${f1(y)}" stroke="#1c2024" stroke-width="${k % 4 === 0 ? 3 : 2.2}" fill="none"/></g>`;
        wi++;
      });
      const y = G + 50 - (PH - 120), sag = (b - a) * 0.07;
      wires += `<g id="${id}-w${wi}" data-o="${f1((a + b) / 2)} ${f1(y)}">${[0, 1, 2, 3, 4].map((q) => `<path d="M${a},${f1(y + q * 3)}Q${f1((a + b) / 2)},${f1(y + q * 3 + 2 * sag)} ${b},${f1(y + q * 3)}" stroke="${q % 2 ? "#2a2e32" : "#141618"}" stroke-width="3" fill="none"/>`).join("")}</g>`;
      wi++;
    });
    Qk.towerWires = wi;
    // the street-food cart under its umbrella
    fr += `<g transform="translate(985,${G + 44})">${CS(0, 2, 70, 9)}
        <circle cx="-38" cy="-12" r="12" fill="#2a2a2c"/><circle cx="34" cy="-12" r="12" fill="#2a2a2c"/><circle cx="-38" cy="-12" r="5" fill="#aab0b4"/><circle cx="34" cy="-12" r="5" fill="#aab0b4"/>
        <rect x="-60" y="-66" width="120" height="48" rx="4" fill="#d8dcde" ${OUT2}/>${Qk.brushed(-58, -64, 116, 44, 5)}<rect x="-60" y="-66" width="120" height="8" fill="#f4f6f6"/>
        <rect x="-56" y="-110" width="112" height="44" fill="#eaf6fa" opacity=".55" ${OUT2}/>${[-40, -22, -4, 14, 32].map((x, q) => `<path d="M${x},-72v-26" stroke="#c8a060" stroke-width="2"/>${[0, 1, 2].map((j) => `<circle cx="${x}" cy="${-94 + j * 8}" r="4.5" fill="${q % 2 ? "#a8582a" : "#d87a3a"}"/>`).join("")}`).join("")}
        <path d="M-54,-108l26,40" stroke="#fff" stroke-width="4" opacity=".5"/><rect x="62" y="-58" width="26" height="40" rx="4" fill="#e8443a" ${OUT2}/></g>`;
    fr += `<g transform="translate(985,${G - 66})"><g id="${id}-umb"><path d="M0,0V-130" stroke="#6a6e70" stroke-width="5"/>
        <path d="M-120,-112Q0,-196 120,-112Q60,-104 0,-108Q-60,-104 -120,-112Z" fill="url(#qkUmb)" ${OUT2}/>${[-90, -45, 0, 45, 90].map((x) => `<path d="M0,-170Q${x * 0.5},-150 ${x},-110" stroke="#fff" stroke-width="${x ? 9 : 0}" opacity=".85" fill="none"/>`).join("")}
        <path d="M-120,-112q20,10 40,4t40,2t40,-2t40,2t40,-4" stroke="#fff6e8" stroke-width="5" fill="none"/><circle cy="-172" r="6" fill="#f2c230" ${OUT2}/></g></g>`;
    // a pink taxi at the kerb, your delivery bike on the pavement, bollards along the forecourt
    fr += `<g transform="translate(250,${G + 168})">${CS(0, 2, 120, 12)}
        <path d="M-112,-18Q-114,-48 -92,-52L-60,-54L-36,-84Q-28,-92 -14,-92H40Q56,-92 66,-82L88,-54Q112,-52 114,-30L112,-18Z" fill="url(#qkTaxi)" ${OUT3}/>
        <path d="M-30,-80Q-24,-86 -14,-86H10V-56H-50Z" fill="url(#qkCarWin)"/><path d="M18,-86H38Q50,-86 58,-78L76,-56H18Z" fill="url(#qkCarWin)"/><path d="M-20,-84l-14,26" stroke="#fff" stroke-width="3" opacity=".6"/>
        <rect x="-26" y="-104" width="48" height="14" rx="3" fill="#f2f4f6" ${OUT2}/><text x="-2" y="-93" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="11" fill="#c8285e">TAXI-METER</text>
        <path d="M-104,-40H106" stroke="#fff" stroke-width="3" opacity=".45"/><path d="M-6,-56V-20" stroke="#a83a6a" stroke-width="2"/>
        ${[-66, 66].map((x) => `<circle cx="${x}" cy="-16" r="19" fill="#1e1e22"/><circle cx="${x}" cy="-16" r="9" fill="#c8ccce"/>`).join("")}<rect x="100" y="-44" width="12" height="10" rx="3" fill="#ffe08a"/><rect x="-114" y="-44" width="9" height="10" rx="3" fill="#e8443a"/></g>`;
    fr += `<g transform="translate(838,${G + 46})">${CS(0, 0, 50, 7)}
        <circle cx="-30" cy="-14" r="14" fill="#1e1e22"/><circle cx="30" cy="-14" r="14" fill="#1e1e22"/><circle cx="-30" cy="-14" r="6" fill="#9aa0a6"/><circle cx="30" cy="-14" r="6" fill="#9aa0a6"/>
        <path d="M-30,-14L-12,-40H14L30,-14M-12,-40L-20,-56" stroke="#c83a2a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-8,-44H20" stroke="#1e1e22" stroke-width="8" stroke-linecap="round"/><path d="M26,-50l6,-14" stroke="#2a2a2c" stroke-width="4" stroke-linecap="round"/>
        <rect x="-36" y="-94" width="40" height="38" rx="4" fill="#2fa45a" ${OUT2}/><circle cx="-16" cy="-75" r="9" fill="#fff4dc" ${OUT2}/><rect x="-36" y="-94" width="40" height="6" fill="#5ac87a"/></g>`;
    for (let x = X0 + 10; x <= X1 + 10; x += 70) fr += `<g transform="translate(${x},${G + 54})">${CS(0, 0, 12, 3)}<rect x="-5" y="-30" width="10" height="30" rx="3" fill="#9aa0a4" ${OUT2}/><rect x="0" y="-30" width="4" height="30" fill="#e2e6e8" opacity=".8"/><rect x="-6" y="-34" width="12" height="6" rx="3" fill="#6a7074"/></g>`;
    fr += wires;
    put(L.set, fr);
  }
  // the tower set reacting to a quake: trees and poles rock, the wires bounce, the umbrella wobbles, palms whip, the mast light blinks
  Qk.reactTower = (tl, id, t0, dur, amp = 1) => {
    const n = (per) => Math.max(1, Math.ceil(dur / per));
    [0, 1].forEach((k) => tl.fromTo(`#${id}-tree${k}`, { rotation: -1.6 * amp, svgOrigin: "0 0" }, { rotation: 1.6 * amp, svgOrigin: "0 0", duration: 0.46 + k * 0.08, repeat: n(0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + k * 0.1));
    [0, 1].forEach((k) => tl.fromTo(`#${id}-pole${k}`, { rotation: -0.5 * amp, svgOrigin: "0 0" }, { rotation: 0.5 * amp, svgOrigin: "0 0", duration: 0.32, repeat: n(0.32), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + k * 0.07));
    [0, 1].forEach((k) => tl.fromTo(`#${id}-palm${k}`, { rotation: -6 * amp, svgOrigin: "0 0" }, { rotation: 7 * amp, svgOrigin: "0 0", duration: 0.38 + k * 0.06, repeat: n(0.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    tl.fromTo(`#${id}-umb`, { rotation: -5 * amp, svgOrigin: "0 0" }, { rotation: 5 * amp, svgOrigin: "0 0", duration: 0.28, repeat: n(0.28), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    for (let k = 0; k < (Qk.towerWires || 0); k++) {
      const el = document.getElementById(`${id}-w${k}`);
      if (!el) continue;
      const o = el.getAttribute("data-o"), per = 0.3 + (k % 5) * 0.045;
      tl.fromTo(el, { scaleY: 1 - 0.3 * amp, svgOrigin: o }, { scaleY: 1 + 0.32 * amp, svgOrigin: o, duration: per, repeat: Math.ceil(dur / per), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (k % 4) * 0.05);
    }
    tl.fromTo(`#${id}-beacon`, { opacity: 1 }, { opacity: 0.15, duration: 0.5, repeat: n(0.5), yoyo: true, ease: "steps(1)", immediateRender: false }, t0);
  };

  // ---------------- the lobby ----------------
  function qkLobby(L, o = {}) {
    const id = o.id || "lb", G = 1500, CE = 340, VX = 540, VY = 1080, r = mk(o.seed || 41);
    const cx = (xw, y) => VX + (xw - VX) * ((VY - y) / (VY - CE)), crow = (k) => VY - (VY - CE) * k;
    const fxw = (xw, y) => VX + (xw - VX) * ((y - VY) / (G - VY)), frow = (k) => VY + (G - VY) * k;
    let s = "";
    // ---- the ceiling: plaster coffers converging on the eye, a cove with its LED line, downlights in rows, a CCTV dome
    s += `<rect x="-1600" y="-800" width="4600" height="${CE + 800}" fill="url(#qkCeil)"/>`;
    let cl = "";
    for (let xw = -1430; xw <= 2900; xw += 390) cl += `M${f1(xw)},${CE - 30}L${f1(cx(xw, -800))},-800`;
    for (const k of [1.3, 1.85, 2.7]) cl += `M-1600,${f1(crow(k))}H3000`;
    s += `<path d="${cl}" stroke="#c6beae" stroke-width="5" opacity=".75"/><path d="${cl}" stroke="#fff" stroke-width="2" opacity=".5" transform="translate(3,3)"/>`;
    s += `<rect x="-1600" y="${CE - 30}" width="4600" height="30" fill="#cfc6b6"/><rect x="-1600" y="${CE - 30}" width="4600" height="8" fill="#a89e8c"/><path d="M-1600,${CE - 6}H3000" stroke="#fff4d0" stroke-width="5"/>`;
    const DL = [-400, 655, 985, 1230, 1505, 1840];
    for (const [k, xs] of [[1.1, DL], [1.6, [-700, 180, 760, 1300, 1840]], [2.35, [-400, 470, 1300]]]) {
      const y = crow(k);
      xs.forEach((xw) => { const x = cx(xw, y); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(26 * k)}" ry="${f1(9 * k)}" fill="#dcd6ca" stroke="#b8b0a0" stroke-width="2"/><ellipse cx="${f1(x)}" cy="${f1(y + 1)}" rx="${f1(17 * k)}" ry="${f1(5.5 * k)}" fill="#fffbea"/>`; });
    }
    s += `<g transform="translate(${f1(cx(1100, crow(1.45)))},${f1(crow(1.45))})"><ellipse rx="34" ry="12" fill="#f2f0ea" stroke="#9a968e" stroke-width="2"/><path d="M-24,0A24,22 0 0 0 24,0Z" fill="#2a2e32"/><circle cx="4" cy="9" r="5" fill="#5a7a9a"/><path d="M-14,4a14,10 0 0 0 8,8" stroke="#fff" stroke-width="2" opacity=".5" fill="none"/></g>`;
    // ---- the wall: big stone panels (joints, tone, veins), lit in scallops by the downlights at the wall
    s += `<rect x="-1600" y="${CE}" width="4600" height="${G - CE}" fill="url(#qkWallStone)"/>`;
    let pj = "", pt2 = "", veins = "";
    for (let x = -1560; x < 3000; x += 260) for (let y = CE; y < G; y += 290) {
      if (r() < 0.5) pt2 += `M${x + 2},${y + 2}h256v286h-256Z`;
      if (r() < 0.45) { const vx = x + 30 + r() * 200, vy = y + 20; veins += `M${f1(vx)},${f1(vy)}C${f1(vx + 60 - r() * 120)},${f1(vy + 80)} ${f1(vx + 80 - r() * 160)},${f1(vy + 160)} ${f1(vx + 40 - r() * 80)},${f1(vy + 260)}`; }
    }
    for (let x = -1560; x < 3000; x += 260) pj += `M${x},${CE}V${G}`;
    for (let y = CE + 290; y < G; y += 290) pj += `M-1600,${y}H3000`;
    s += `<path d="${pt2}" fill="#fff" opacity=".12"/><path d="${veins}" stroke="#c4b8a2" stroke-width="2" fill="none" opacity=".45"/><path d="${pj}" stroke="#b8ad9a" stroke-width="4"/><path d="${pj}" stroke="#fff" stroke-width="1.5" opacity=".55" transform="translate(2,2)"/>`;
    DL.forEach((x) => { s += `<path d="M${x - 18},${CE + 4}C${x - 50},${CE + 110} ${x - 120},${CE + 250} ${x - 132},${CE + 440}Q${x},${CE + 500} ${x + 132},${CE + 440}C${x + 120},${CE + 250} ${x + 50},${CE + 110} ${x + 18},${CE + 4}Z" fill="url(#qkScallop)" opacity=".85"/><ellipse cx="${x}" cy="${CE + 26}" rx="34" ry="16" fill="#fffdf2" opacity=".55"/>`; });
    s += `<rect x="-1600" y="${CE}" width="4600" height="60" fill="url(#qkAOdn)" opacity=".7"/>`;
    // ---- the entrance: the street outside in daylight through two glass leaves in a steel frame
    s += `<rect x="-924" y="${CE + 36}" width="668" height="${G - CE - 36}" fill="#3a4650" ${OUT3}/>
      <defs><clipPath id="${id}-door"><rect x="-900" y="${CE + 60}" width="620" height="${G - CE - 60}"/></clipPath></defs><g clip-path="url(#${id}-door)">
        <rect x="-900" y="${CE + 60}" width="620" height="${G - CE - 60}" fill="url(#qkSkyRefl)"/>
        <rect x="-880" y="${CE + 140}" width="160" height="${G - CE - 140}" fill="#cbd6dc"/><rect x="-700" y="${CE + 240}" width="220" height="${G - CE - 240}" fill="#d8dcd6"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-690,${CE + 280 + k * 70}h200" stroke="#b8c0c2" stroke-width="5"/>`).join("")}
        ${crown(-420, CE + 330, 150, r, ["#6a9a5a", "#86b46e", "#a8cc84", "#c4dc9a"], 10)}<path d="M-424,${CE + 420}V${G - 200}" stroke="#7a6a52" stroke-width="18"/>
        <rect x="-900" y="${G - 210}" width="620" height="90" fill="#cfcabe"/><rect x="-900" y="${G - 120}" width="620" height="120" fill="#9a9e9e"/><path d="M-900,${G - 122}h620" stroke="#efece4" stroke-width="6"/>
        <g transform="translate(-600,${G - 128})"><circle cx="-26" cy="-12" r="12" fill="#2a2a2c"/><circle cx="26" cy="-12" r="12" fill="#2a2a2c"/><path d="M-26,-12L-10,-34H12L26,-12" stroke="#3a5ac8" stroke-width="6" fill="none"/></g>
      </g>
      <path d="M-590,${CE + 60}V${G}M-900,${CE + 300}H-280" stroke="#3a4650" stroke-width="14"/><path d="M-583,${CE + 60}V${G}" stroke="#8a969e" stroke-width="2"/>
      <path d="M-860,${G - 30}L-700,${CE + 120}H-650L-810,${G - 30}Z" fill="#fff" opacity=".28"/><path d="M-560,${G - 30}L-420,${CE + 140}H-400L-540,${G - 30}Z" fill="#fff" opacity=".22"/>
      <path d="M-616,${CE + 760}V${CE + 960}M-564,${CE + 760}V${CE + 960}" stroke="#c8ccce" stroke-width="10" stroke-linecap="round"/><path d="M-612,${CE + 765}V${CE + 950}" stroke="#fff" stroke-width="3" opacity=".7"/>
      <rect x="-520" y="${CE + 720}" width="74" height="26" rx="4" fill="#e8f0f4" opacity=".85"/><text x="-483" y="${CE + 740}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="18" fill="#2a3a46">ผลัก</text>`;
    // ---- the slatted wood wall with the backlit gold name
    s += `<rect x="-208" y="${CE + 32}" width="776" height="${G - CE - 290}" fill="#4a3020" ${OUT3}/>`;
    let sl = "", slL = "", slD = "";
    for (let x = -198; x < 556; x += 28) { sl += `M${x},${CE + 40}h21V${G - 262}h-21Z`; slL += `M${x + 15},${CE + 40}h6V${G - 262}h-6Z`; slD += `M${x},${CE + 40}h4V${G - 262}h-4Z`; }
    s += `<path d="${sl}" fill="#a07048"/><path d="${slL}" fill="#c89a6c"/><path d="${slD}" fill="#6a4428"/>`;
    s += Qk.grain(-198, CE + 40, 752, G - CE - 302, 9, { dir: "v", op: 0.16, gap: 9, knots: 0 });
    s += `<rect x="-200" y="${CE + 40}" width="760" height="${G - CE - 302}" fill="url(#qkAOdn)" opacity=".35"/>`;
    s += `<ellipse cx="180" cy="${CE + 230}" rx="400" ry="150" fill="url(#qkHalo)" opacity=".6"/>
      <text x="188" y="${CE + 258}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="92" fill="#2a1a0c" opacity=".55">เดอะสกาย 32</text>
      <text x="180" y="${CE + 250}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="92" fill="url(#qkBrass)" stroke="#6a4a12" stroke-width="2.5" paint-order="stroke">เดอะสกาย 32</text>
      <text x="180" y="${CE + 330}" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="44" letter-spacing="14" fill="url(#qkBrass)" opacity=".9">THE SKY 32</text>`;
    // ---- a notice board between the wood wall and the lifts
    s += `<g transform="translate(655,${CE + 290})">${CS(4, 128, 80, 10, 0.5)}<rect x="-80" y="-96" width="160" height="214" rx="6" fill="#7a5236" ${OUT3}/><rect x="-70" y="-62" width="140" height="170" fill="url(#qkCork)"/>
      <rect x="-80" y="-96" width="160" height="34" rx="6" fill="#2e4a3a"/><text y="-71" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#f4ecd8">ประกาศ</text>
      <rect x="-60" y="-50" width="64" height="80" fill="#fbf8ee" transform="rotate(-4 -28 -10)"/><path d="M-54,-36h48M-54,-26h40M-54,-16h46M-54,-6h30" stroke="#7a7a7a" stroke-width="3" transform="rotate(-4 -28 -10)"/>
      <rect x="10" y="-44" width="54" height="64" fill="#fff1c0" transform="rotate(5 37 -12)"/><path d="M16,-30h40M16,-20h34M16,-10h38" stroke="#c8281e" stroke-width="3" transform="rotate(5 37 -12)"/>
      <rect x="-50" y="40" width="96" height="58" fill="#dff0fa" transform="rotate(2 0 69)"/><path d="M-42,54h76M-42,66h60M-42,78h70" stroke="#3a6aa8" stroke-width="3"/>
      ${[[-28, -48], [36, -42], [0, 42]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="#e8443a" stroke="#7a1a12" stroke-width="1.5"/>`).join("")}</g>`;
    // ---- the lifts: steel architraves, brushed doors with reflections, indicators; the call buttons; the paper sign
    const lift = (x, k) => {
      let g = `<rect x="${x - 36}" y="${G - 838}" width="452" height="838" fill="#7e868c" ${OUT3}/><rect x="${x - 24}" y="${G - 826}" width="428" height="826" fill="url(#qkSteelD)"/><path d="M${x - 24},${G - 825}H${x + 404}" stroke="#fff" stroke-width="3" opacity=".7"/>
        <rect x="${x - 4}" y="${G - 804}" width="388" height="804" fill="#3e464c"/><rect x="${x + 376}" y="${G - 804}" width="8" height="804" fill="#c8d0d4"/>
        <rect x="${x}" y="${G - 800}" width="190" height="800" fill="url(#qkSteel)"/><rect x="${x + 190}" y="${G - 800}" width="190" height="800" fill="url(#qkSteel)"/>${Qk.brushed(x, G - 800, 380, 800, 11 + k)}
        <rect x="${x + 36}" y="${G - 800}" width="54" height="800" fill="#fff" opacity=".16"/><rect x="${x + 230}" y="${G - 800}" width="34" height="800" fill="#fff" opacity=".12"/><rect x="${x + 120}" y="${G - 800}" width="40" height="800" fill="#1e262c" opacity=".1"/>
        <path d="M${x + 190},${G - 800}V${G}" stroke="#454d53" stroke-width="5"/><path d="M${x + 193},${G - 800}V${G}" stroke="#e8eef0" stroke-width="1.5" opacity=".7"/>
        <rect x="${x + 100}" y="${G - 928}" width="180" height="82" rx="10" fill="#9aa2a8" ${OUT3}/><rect x="${x + 110}" y="${G - 920}" width="160" height="66" rx="8" fill="#141414"/>
        <path d="M${x + 124},${G - 872}l12,-18l12,18z" fill="#ff5a3a" opacity="${k ? 0.3 : 0.9}"/><path d="M${x + 112},${G - 918}h156" stroke="#fff" stroke-width="3" opacity=".18"/>
        <text id="${id}-n${k}" x="${x + 190}" y="${G - 872}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#ff5a3a">${k ? "12" : "1"}</text>`;
      return g;
    };
    s += lift(780, 0) + lift(1300, 1);
    s += `<g transform="translate(1233,${G - 465})"><rect x="-30" y="-62" width="60" height="124" rx="8" fill="url(#qkSteelD)" ${OUT3}/><rect x="-30" y="-62" width="60" height="124" rx="8" fill="#fff" opacity=".12"/>
      ${Qk.knob(0, -26, 15, "#f4f4ee")}${Qk.knob(0, 24, 15, "#f4f4ee")}<circle cy="-26" r="15" fill="none" stroke="#ffb03a" stroke-width="3"/><path d="M-6,-22l6,-9l6,9zM-6,20l6,9l6,-9z" fill="#5a6064"/></g>`;
    s += `<g id="${id}-paper" transform="translate(1490,${G - 500}) rotate(3)">${CS(6, 74, 120, 10, 0.4)}<rect x="-120" y="-80" width="240" height="150" fill="#fbf8ee" ${OUT3}/><path d="M120,70l-26,0l26,-24z" fill="#e2dccb" stroke="${INK}" stroke-width="2"/><path d="M-120,-80h40v-14h-40zM80,-80h40v-14h-40z" fill="#d8d0b8" opacity=".8"/>
        <text x="0" y="-20" text-anchor="middle" font-family="Mali" font-weight="700" font-size="40" fill="#c8281e">ลิฟต์ขัดข้อง</text><text x="0" y="32" text-anchor="middle" font-family="Mali" font-weight="600" font-size="21" fill="#3a3a3a">ขออภัยในความไม่สะดวก</text></g>`;
    s += `<g transform="translate(1960,${G - 760})"><rect x="-110" y="-150" width="220" height="300" fill="#fff" ${OUT3}/><rect x="-110" y="-150" width="220" height="50" fill="#2fa45a"/>
        <text x="0" y="-114" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#fff">แผนผังหนีไฟ</text><path d="M-80,-60H80V120H-80Z" fill="none" stroke="#5a5a5a" stroke-width="3"/><path d="M-80,30H80M0,-60V120" stroke="#9a9a9a" stroke-width="2"/>
        <path d="M-60,100L60,-40" stroke="#2fa45a" stroke-width="6" stroke-dasharray="14 8"/><circle cx="-60" cy="100" r="10" fill="#d8312a"/></g>`;
    // ---- the floor: polished marble tiles in perspective, veins, the AO line, reflections of the lifts, the wood wall and the door light
    s += `<rect x="-1600" y="${G}" width="4600" height="1500" fill="url(#qkMarble)"/>`;
    let fl = "";
    for (let xw = -1540; xw <= 2900; xw += 130) fl += `M${xw},${G}L${f1(fxw(xw, G + 1500))},${G + 1500}`;
    for (const k of [1.2, 1.47, 1.82, 2.3, 2.95, 3.85]) fl += `M-1600,${f1(frow(k))}H3000`;
    let fv = "";
    for (let k = 0; k < 26; k++) { const x0 = -400 + r() * 2200, y0 = G + 30 + r() * 900, sc = (y0 - VY) / (G - VY); fv += `M${f1(x0)},${f1(y0)}c${f1(40 * sc)},${f1(10 * sc)} ${f1(60 * sc)},${f1(30 * sc)} ${f1(120 * sc)},${f1(24 * sc)}s${f1(50 * sc)},${f1(-16 * sc)} ${f1(90 * sc)},${f1(4 * sc)}`; }
    s += `<path d="${fv}" stroke="#bfb3a0" stroke-width="2.5" fill="none" opacity=".5"/><path d="${fl}" stroke="#bdb2a0" stroke-width="3" opacity=".7"/><path d="${fl}" stroke="#fffaf0" stroke-width="1.2" opacity=".5" transform="translate(2,2)"/>`;
    s += `<defs><linearGradient id="${id}-rf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8dee2" stop-opacity=".55"/><stop offset="1" stop-color="#d8dee2" stop-opacity="0"/></linearGradient>
        <linearGradient id="${id}-rw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b88a5e" stop-opacity=".4"/><stop offset="1" stop-color="#b88a5e" stop-opacity="0"/></linearGradient>
        <linearGradient id="${id}-rk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3226" stop-opacity=".42"/><stop offset="1" stop-color="#4a3226" stop-opacity="0"/></linearGradient>
        <linearGradient id="${id}-rd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>
      ${[780, 1300].map((x) => `<rect x="${x - 24}" y="${G}" width="428" height="340" fill="url(#${id}-rf)"/><rect x="${x + 36}" y="${G}" width="54" height="300" fill="url(#${id}-rd)" opacity=".35"/><rect x="${x + 100}" y="${G + 40}" width="180" height="60" fill="#141414" opacity=".08"/>`).join("")}
      <path d="M-208,${G}h776v200h-776Z" fill="url(#${id}-rw)"/><rect x="-150" y="${G}" width="660" height="230" fill="url(#${id}-rk)"/><rect x="572" y="${G}" width="80" height="150" fill="url(#${id}-rk)" opacity=".6"/><path d="M-900,${G}h620l120,520h-900Z" fill="url(#${id}-rd)"/>`;
    DL.forEach((x) => { const y = frow(1.1); s += `<ellipse cx="${f1(fxw(x, y))}" cy="${f1(y)}" rx="140" ry="34" fill="#fffaf0" opacity=".28"/>`; });
    s += `<rect x="-1600" y="${G}" width="4600" height="26" fill="#2a2016" opacity=".14"/><path d="M-1600,${G}H3000" stroke="#8a7e6c" stroke-width="3"/>`;
    s += `<path d="M-930,${G + 4}H-250L-170,${G + 120}H-1010Z" fill="#3a3a3c"/><path d="M-920,${G + 10}H-258L-188,${G + 112}H-996Z" fill="none" stroke="#8a7a5a" stroke-width="4"/>`;
    // ---- a bird of paradise in a tall planter: paddle leaves on long stalks, lit from the right (sways a little in the draught)
    const PX = 612;
    let pl = CS(PX, G + 8, 110, 15);
    pl += `<path d="M${PX - 56},${G - 214}H${PX + 56}L${PX + 46},${G}H${PX - 46}Z" fill="url(#qkPot)" ${OUT3}/><rect x="${PX - 62}" y="${G - 224}" width="124" height="16" rx="5" fill="#4a4a4e" ${OUT2}/><path d="M${PX + 34},${G - 204}L${PX + 28},${G - 14}" stroke="#fff" stroke-width="5" opacity=".22"/>
      <ellipse cx="${PX}" cy="${G - 216}" rx="50" ry="7" fill="#3a2a1e"/>`;
    const LV = [[-30, 330, 0.9], [-16, 420, 1.05], [-5, 470, 1.12], [6, 450, 1.08], [17, 380, 1.0], [29, 300, 0.92], [-40, 240, 0.8], [40, 230, 0.78]];
    let leaves = "";
    LV.forEach(([deg, len, sc], k) => {
      const a = (deg * Math.PI) / 180, bx = PX + (k - 3.5) * 6, by = G - 214, tx = bx + Math.sin(a) * len, ty = by - Math.cos(a) * len, mx = bx + Math.sin(a) * len * 0.5 + deg * 0.6, my = by - Math.cos(a) * len * 0.52;
      const edge = k === 2 || k === 5, w = (edge ? 24 : 66) * sc, h = 250 * sc;
      leaves += `<path d="M${f1(bx)},${by}Q${f1(mx)},${f1(my)} ${f1(tx)},${f1(ty)}" stroke="#3a7236" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M${f1(bx + 2)},${by}Q${f1(mx + 2)},${f1(my)} ${f1(tx + 2)},${f1(ty)}" stroke="#8ac87a" stroke-width="2" fill="none" opacity=".6"/>`;
      leaves += `<g transform="translate(${f1(tx)},${f1(ty)}) rotate(${f1(deg * 1.15)})"><path d="M0,0C${f1(-w)},${f1(-h * 0.2)} ${f1(-w * 0.9)},${f1(-h * 0.8)} 0,${f1(-h)}C${f1(w * 0.9)},${f1(-h * 0.8)} ${f1(w)},${f1(-h * 0.2)} 0,0Z" fill="url(#qkLeafG)" ${OUT2}/>
        <path d="M0,0C${f1(w * 0.5)},${f1(-h * 0.25)} ${f1(w * 0.6)},${f1(-h * 0.7)} 0,${f1(-h)}" fill="#a8dc8a" opacity=".35"/><path d="M0,-4V${f1(-h + 8)}" stroke="#2a5a2e" stroke-width="2.5"/>
        ${edge ? "" : [0.3, 0.5, 0.7].map((u, q) => `<path d="M${f1((q % 2 ? 1 : -1) * w * 0.82)},${f1(-h * u)}L${f1((q % 2 ? 1 : -1) * w * 0.3)},${f1(-h * u + 8)}" stroke="#ece6da" stroke-width="3" opacity=".8"/>`).join("")}</g>`;
    });
    s += pl + `<g id="${id}-plant">${leaves}</g>`;
    put(L.set, s);
    // ---- the guard desk: drawn in glow so the guard stands behind it
    let dk = `<g transform="translate(180,${G})">${CS(0, 6, 400, 26, 0.9)}
        <rect x="-330" y="-395" width="660" height="395" fill="url(#qkWalnut)" ${OUT}/>`;
    let flute = "", fluteL = "";
    for (let x = -312; x < 320; x += 26) { flute += `M${x},-360V-34`; fluteL += `M${x + 6},-360V-34`; }
    dk += `<path d="${flute}" stroke="#2a1c12" stroke-width="5" opacity=".7"/><path d="${fluteL}" stroke="#a87a56" stroke-width="2.5" opacity=".6"/>
        <rect x="-336" y="-30" width="672" height="30" fill="#d8d0c0" ${OUT3}/><path d="M-334,-28h668" stroke="#fff" stroke-width="2" opacity=".6"/>
        <rect x="-354" y="-424" width="708" height="36" rx="5" fill="url(#qkDeskTop)" ${OUT}/><path d="M-346,-420h692" stroke="#fff" stroke-width="3"/><path d="M-200,-414c40,8 80,-6 140,4s90,4 120,-2" stroke="#c4b8a2" stroke-width="2" fill="none"/>
        <rect x="-330" y="-388" width="660" height="14" fill="#1a100a" opacity=".35"/>
        <rect x="-108" y="-312" width="216" height="76" rx="8" fill="url(#qkBrass)" ${OUT3}/><rect x="-100" y="-304" width="200" height="60" rx="5" fill="none" stroke="#fff6d0" stroke-width="2" opacity=".6"/>
        <text x="0" y="-258" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="38" fill="#4a3210">ติดต่อ</text>
        <g transform="translate(-232,-424)"><rect x="-8" y="-18" width="16" height="18" fill="#5a5e62"/><rect x="-36" y="-6" width="72" height="8" rx="3" fill="#6a6e72"/><rect x="-78" y="-128" width="156" height="112" rx="8" fill="#8a9094" ${OUT3}/><rect x="-70" y="-120" width="140" height="96" rx="5" fill="#9aa0a4"/><circle cx="0" cy="-72" r="16" fill="#7a8084"/><path d="M-60,-114l40,0" stroke="#fff" stroke-width="3" opacity=".4"/></g>
        <g transform="translate(-108,-424)"><path d="M-30,0h60l-6,-10h-48z" fill="#3a6aa8" ${OUT2}/><path d="M0,-10V-50" stroke="#3a6aa8" stroke-width="8"/><circle cy="-86" r="40" fill="#cfe2f2" ${OUT2}/><circle cy="-86" r="36" fill="none" stroke="#9ab8d0" stroke-width="2"/>${[0, 120, 240].map((a) => `<ellipse cx="0" cy="-104" rx="9" ry="18" fill="#5a8ac8" transform="rotate(${a} 0 -86)"/>`).join("")}<circle cy="-86" r="7" fill="#2a4a78"/>${[-30, -15, 0, 15, 30].map((a) => `<path d="M0,-86L${f1(Math.sin((a * Math.PI) / 180) * 40)},${f1(-86 - Math.cos((a * Math.PI) / 180) * 40)}" stroke="#9ab8d0" stroke-width="1.5"/>`).join("")}</g>
        <g transform="translate(40,-428)"><path d="M-62,0L-56,-14H0L56,-14L62,0Z" fill="#f6f2e6" ${OUT2}/><path d="M0,-14V0" stroke="#9a9078" stroke-width="2"/><path d="M-48,-9h40M-48,-5h34M8,-9h40M8,-5h30" stroke="#7a7468" stroke-width="1.5"/><path d="M30,-20l40,-10" stroke="#2a4a8a" stroke-width="4" stroke-linecap="round"/></g>
        <g transform="translate(206,-424)"><path d="M-16,0a16,14 0 0 1 32,0z" fill="#d8b04a" ${OUT2}/><circle cy="-15" r="4" fill="#a8822a"/><path d="M-20,0h40" stroke="${INK}" stroke-width="3"/></g>
        <g transform="translate(262,-424)"><path d="M0,0V-60" stroke="#8a8e90" stroke-width="3"/><rect x="0" y="-60" width="38" height="12" fill="#d8312a"/><rect x="0" y="-52" width="38" height="5" fill="#fff"/><rect x="0" y="-51" width="38" height="3" fill="#2a3a8a"/><rect x="0" y="-48" width="38" height="12" fill="#d8312a" opacity="0"/><path d="M-8,0h16" stroke="#5a5e60" stroke-width="4"/></g></g>`;
    put(L.glow, dk);
    // the downlights' glare (above the darkness)
    put(L.glow, DL.map((xw) => { const y = crow(1.1), x = cx(xw, y); return `<ellipse cx="${f1(x)}" cy="${f1(y + 2)}" rx="60" ry="22" fill="url(#qkDown)" opacity=".6"/>`; }).join(""));
  }

  // ---------------- inside the lift (first person) ----------------
  function qkLift(L, o = {}) {
    const id = o.id || "lf", VX = 540, VY = 1000, r = mk(o.seed || 7);
    const P = (x, y, k) => [VX + (x - VX) * k, VY + (y - VY) * k];                                  // a point of the door wall pushed toward us by k
    const WQ = (x, y0, y1, k0, k1) => [P(x, y0, k0), P(x, y0, k1), P(x, y1, k1), P(x, y1, k0)];       // a quad on a side wall (x 230 / 850)
    const HQ = (y, x0, x1, k0, k1) => [P(x0, y, k0), P(x1, y, k0), P(x1, y, k1), P(x0, y, k1)];       // a quad on the ceiling (300) / floor (1700)
    const wallM = (x, y, k, sx) => { const [px, py] = P(x, y, k), dir = x < VX ? -1 : 1, ux = 310 * dir, uy = y - VY, L2 = Math.hypot(ux, uy); return `matrix(${f1((ux / L2) * sx * k)},${f1((uy / L2) * sx * k)},0,${f1(k)},${f1(px)},${f1(py)})`; };
    let s = `<rect x="-600" y="-600" width="2300" height="3200" fill="#5e666c"/>`;
    // ceiling: plaster, the vent grille, the CCTV dome
    s += PL(HQ(300, 230, 850, 1, 4), `fill="#e2e6e8"`) + PL(HQ(300, 640, 830, 1.03, 1.2), `fill="#c8ced2" ${OUT2}`);
    let vg = ""; for (let k = 1.05; k < 1.2; k += 0.025) vg += `M${pt(P(650, 300, k))}L${pt(P(820, 300, k))}`;
    s += `<path d="${vg}" stroke="#7a8288" stroke-width="3"/>`;
    { const [dx, dy] = P(300, 300, 1.12); s += `<ellipse cx="${f1(dx)}" cy="${f1(dy)}" rx="30" ry="10" fill="#f2f2ee" stroke="#9aa0a4" stroke-width="2"/><path d="M${f1(dx - 22)},${f1(dy)}A22,20 0 0 0 ${f1(dx + 22)},${f1(dy)}Z" fill="#23272b"/><circle cx="${f1(dx + 5)}" cy="${f1(dy + 9)}" r="4" fill="#5a7aa0"/>`; }
    // floor: dark granite with flecks, tile joints, the door sill
    s += PL(HQ(1700, 230, 850, 1, 4), `fill="url(#qkLiftFl)"`);
    let fk = ""; for (let i = 0; i < 260; i++) { const k = 1 + Math.pow(r(), 1.4) * 0.8, [x, y] = P(230 + r() * 620, 1700, k); fk += `M${f1(x)},${f1(y)}h${f1(2 + r() * 2.5 * k)}`; }
    s += `<path d="${fk}" stroke="#9aa0a4" stroke-width="2.5" opacity=".55"/>`;
    let tj = ""; for (let x = 230 + 155; x < 850; x += 155) tj += `M${pt(P(x, 1700, 1.04))}L${pt(P(x, 1700, 4))}`;
    for (const k of [1.22, 1.5]) tj += `M${pt(P(230, 1700, k))}L${pt(P(850, 1700, k))}`;
    s += `<path d="${tj}" stroke="#1e2226" stroke-width="3"/><path d="${tj}" stroke="#7a8086" stroke-width="1" opacity=".6" transform="translate(0,2)"/>`;
    s += PL(HQ(1700, 230, 850, 1, 1.045), `fill="#b8c0c4"`) + `<path d="M${pt(P(230, 1700, 1.02))}L${pt(P(850, 1700, 1.02))}M${pt(P(230, 1700, 1.032))}L${pt(P(850, 1700, 1.032))}" stroke="#6a7278" stroke-width="2"/>`;
    // the doors' reflection on the floor
    s += PL([P(250, 1700, 1.045), P(830, 1700, 1.045), P(830, 1700, 1.5), P(250, 1700, 1.5)], `fill="url(#${id}-flr)"`) + `<defs><linearGradient id="${id}-flr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8d0d4" stop-opacity=".35"/><stop offset="1" stop-color="#c8d0d4" stop-opacity="0"/></linearGradient></defs>`;
    // side walls: brushed steel panels, kick panels, seams
    for (const [x, gr] of [[230, "qkLiftWL"], [850, "qkLiftWR"]]) {
      s += PL(WQ(x, 300, 1700, 1, 4), `fill="url(#${gr})"`);
      s += `<defs><clipPath id="${id}-cw${x}"><path d="${SP(WQ(x, 300, 1700, 1, 4))}"/></clipPath></defs><g clip-path="url(#${id}-cw${x})">${Qk.brushed(x < VX ? -700 : 850, -1800, 850, 5600, x)}</g>`;
      s += PL(WQ(x, 1560, 1700, 1, 4), `fill="#6e767c"`) + `<path d="M${pt(P(x, 1560, 1))}L${pt(P(x, 1560, 4))}" stroke="#d8dee2" stroke-width="2.5"/>`;
      let sm = ""; for (const k of [1.4, 2.0, 2.9]) sm += `M${pt(P(x, 300, k))}L${pt(P(x, 1700, k))}`;
      s += `<path d="${sm}" stroke="#4a5258" stroke-width="3"/><path d="${sm}" stroke="#f2f4f6" stroke-width="1.5" opacity=".6" transform="translate(${x < VX ? 3 : -3},0)"/>`;
      s += `<path d="M${pt(P(x, 300, 1))}L${pt(P(x, 1700, 1))}" stroke="#3e464c" stroke-width="5"/>`;
    }
    // the mirror on the left wall (it holds a faint image of the panel opposite)
    s += PL(WQ(230, 470, 1080, 1.12, 3.4), `fill="#8a9298"`) + PL(WQ(230, 480, 1070, 1.14, 3.4), `fill="url(#qkMirror)"`);
    s += `<defs><clipPath id="${id}-mir"><path d="${SP(WQ(230, 480, 1070, 1.14, 3.4))}"/></clipPath></defs><g clip-path="url(#${id}-mir)">
      ${PL([P(230, 560, 1.5), P(230, 560, 2.0), P(230, 1000, 2.0), P(230, 1000, 1.5)], `fill="#c8d0d4" opacity=".55"`)}${PL([P(230, 470, 1.14), P(230, 470, 1.3), P(230, 1080, 1.3), P(230, 1080, 1.14)], `fill="#6e787e" opacity=".5"`)}
      <path d="M-200,1300L300,300H420L-80,1300Z" fill="#fff" opacity=".3"/><path d="M-420,1300L120,260H170L-370,1300Z" fill="#fff" opacity=".2"/></g>`;
    // handrails: a tube on brackets, with its shadow on the wall
    for (const x of [230, 850]) {
      const xr = x < VX ? x + 14 : x - 14;
      s += PL([P(x, 1166, 1.06), P(x, 1166, 4), P(x, 1196, 4), P(x, 1196, 1.06)], `fill="#000" opacity=".14"`);
      for (const k of [1.3, 2.1, 3.2]) s += PL([P(x, 1148, k), P(xr, 1148, k), P(xr, 1156, k), P(x, 1156, k)], `fill="#7a8288"`);
      s += PL([P(xr, 1128, 1.06), P(xr, 1128, 4), P(xr, 1162, 4), P(xr, 1162, 1.06)], `fill="url(#qkRailT)" stroke="#5a6268" stroke-width="2"`);
      s += `<path d="M${pt(P(xr, 1136, 1.06))}L${pt(P(xr, 1136, 4))}" stroke="#fff" stroke-width="4" opacity=".8" stroke-linecap="round"/>`;
    }
    // the doors in their frame: brushed leaves with reflections, the centre seam, the no-lift-in-fire-or-quake sticker
    s += `<rect x="226" y="296" width="628" height="1408" fill="#4a5258"/><rect x="230" y="300" width="620" height="1400" fill="url(#qkSteelD)"/>${Qk.brushed(230, 300, 620, 1400, 3)}
      <path d="M232,302H848" stroke="#fff" stroke-width="3" opacity=".6"/><rect x="246" y="336" width="588" height="1364" fill="#353c42"/>
      <rect x="250" y="340" width="290" height="1360" fill="url(#qkSteel)"/><rect x="540" y="340" width="290" height="1360" fill="url(#qkSteel)"/>${Qk.brushed(250, 340, 580, 1360, 19)}
      <rect x="292" y="340" width="70" height="1360" fill="#fff" opacity=".16"/><rect x="600" y="340" width="44" height="1360" fill="#fff" opacity=".12"/><rect x="420" y="340" width="56" height="1360" fill="#1e262c" opacity=".09"/><rect x="740" y="340" width="40" height="1360" fill="#1e262c" opacity=".08"/>
      <path d="M300,420L420,1500M640,420L760,1500" stroke="#fff" stroke-width="14" opacity=".12"/>
      <path d="M540,340V1700" stroke="#2e353a" stroke-width="6"/><path d="M544,340V1700" stroke="#eef2f4" stroke-width="1.5" opacity=".7"/><path d="M250,1660H830" stroke="#2e353a" stroke-width="2" opacity=".5"/>
      <g transform="translate(686,980)"><rect x="-68" y="-46" width="136" height="104" rx="8" fill="#fbfbf8" stroke="#c8281e" stroke-width="5"/><circle cx="-34" cy="-10" r="22" fill="none" stroke="#c8281e" stroke-width="5"/><rect x="-44" y="-22" width="20" height="26" fill="#5a6268"/><path d="M-50,6L-18,-26" stroke="#c8281e" stroke-width="5"/>
        <path d="M20,-26q-10,12 -2,22q-14,-2 -12,14q4,10 14,10q12,0 14,-12q0,-12 -14,-34z" fill="#e8682a"/><path d="M6,8l20,-6l-8,14l14,-2" stroke="#5a4a3a" stroke-width="2.5" fill="none"/>
        <text y="34" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="14" fill="#c8281e">ห้ามใช้ลิฟต์</text><text y="50" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="11" fill="#3a3a3a">เมื่อเกิดเพลิงไหม้ · แผ่นดินไหว</text></g>`;
    // the panel on the right wall: 17–32 with braille, then door open / close, alarm and intercom; the key switch; plate and certificate
    s += PL(WQ(850, 772, 1328, 1.13, 1.66), `fill="#5e666c"`) + PL(WQ(850, 780, 1320, 1.15, 1.65), `fill="url(#qkSteelD)"`);
    s += `<defs><clipPath id="${id}-pn"><path d="${SP(WQ(850, 780, 1320, 1.15, 1.65))}"/></clipPath></defs><g clip-path="url(#${id}-pn)">${Qk.brushed(880, 600, 200, 800, 23)}</g>`;
    s += `<path d="M${pt(P(850, 784, 1.16))}L${pt(P(850, 784, 1.64))}" stroke="#fff" stroke-width="2" opacity=".6"/>`;
    const btn = (n, Y, kb, label, face) => {
      const [x, y] = P(850, Y, kb), rx = 13 * kb, ry = 18 * kb, br = P(850, Y, kb + 0.075);
      let b = `<g id="${id}-b${n}"><ellipse cx="${f1(x + 2)}" cy="${f1(y + 3)}" rx="${f1(rx + 3)}" ry="${f1(ry + 3)}" fill="#000" opacity=".22"/><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx + 3)}" ry="${f1(ry + 3)}" fill="#c8ced2" stroke="#4a5258" stroke-width="2"/>
        <ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="${face || "#f2f2ee"}" stroke="#8a9298" stroke-width="1.5"/><ellipse cx="${f1(x - rx * 0.3)}" cy="${f1(y - ry * 0.35)}" rx="${f1(rx * 0.35)}" ry="${f1(ry * 0.25)}" fill="#fff" opacity=".8"/>
        ${label === "bell" ? `<g transform="${wallM(850, Y, kb, 0.7)}"><path d="M-8,5Q-8,-9 0,-10Q8,-9 8,5Z" fill="#5a4a10"/><path d="M-10,5h20" stroke="#5a4a10" stroke-width="2.5"/><circle cy="8" r="2.5" fill="#5a4a10"/></g>`
          : label === "phone" ? `<g transform="${wallM(850, Y, kb, 0.7)}"><path d="M-9,-7q4,-4 7,0l-2,4q3,5 6,7l4,-2q4,3 0,7q-6,3 -13,-6q-6,-7 -2,-10z" fill="#1e5a2e"/></g>`
          : label === "open" || label === "close" ? `<g transform="${wallM(850, Y, kb, 0.7)}" fill="#2e3236">${label === "open" ? `<path d="M-3,-6l-7,6l7,6zM3,-6l7,6l-7,6z"/>` : `<path d="M-10,-6l7,6l-7,6zM10,-6l-7,6l7,6z"/>`}<path d="M0,-8v16" stroke="#2e3236" stroke-width="1.5"/></g>`
          : `<text transform="${wallM(850, Y + 7, kb, 0.7)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${label.length > 2 ? 12 : 19}" fill="#2e3236">${label}</text>`}`;
      for (let q = 0; q < 4; q++) b += `<circle cx="${f1(br[0] + (q % 2) * 4)}" cy="${f1(br[1] - 8 + Math.floor(q / 2) * 7)}" r="${f1(1.6 * kb)}" fill="#4a5258"/>`;
      return b + `</g>`;
    };
    let pn = "";
    for (let k = 0; k < 16; k++) { const n = 32 - k, col = k % 2, row = Math.floor(k / 2); pn += btn(n, 840 + row * 44, col ? 1.47 : 1.27, String(n)); }
    pn += btn("open", 1218, 1.27, "open") + btn("close", 1218, 1.47, "close") + btn("alarm", 1270, 1.27, "bell", "#f6d23a") + btn("call", 1270, 1.47, "phone", "#7ad08a");
    { const [kx, ky] = P(850, 806, 1.56); pn += `<circle cx="${f1(kx)}" cy="${f1(ky)}" r="10" fill="#d8dcde" stroke="#4a5258" stroke-width="2"/><path d="M${f1(kx - 5)},${f1(ky)}h10" stroke="#2e3236" stroke-width="3"/>`; }
    { let sp = ""; for (let q = 0; q < 12; q++) { const [gx, gy] = P(850, 1306, 1.3 + q * 0.025); sp += `M${f1(gx)},${f1(gy)}h1.5`; } pn += `<path d="${sp}" stroke="#2e3236" stroke-width="3" stroke-linecap="round"/>`; }
    s += pn;
    s += PL(WQ(850, 690, 744, 1.2, 1.56), `fill="#e8eaea" stroke="#5a6268" stroke-width="2"`) + `<text transform="${wallM(850, 726, 1.37, 0.55)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="20" fill="#2e3236">13 คน · 1000 กก.</text>`;
    { const [nx, ny] = P(850, 520, 1.35); Qk.liftCertOrigin = `${f1(nx)} ${f1(ny)}`;
      s += `<g id="${id}-cert">${PL(WQ(850, 530, 666, 1.22, 1.5), `fill="#7a5a36" stroke="${INK}" stroke-width="2"`)}${PL(WQ(850, 540, 656, 1.24, 1.48), `fill="#fbf8ee"`)}
        <text transform="${wallM(850, 566, 1.36, 0.5)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="15" fill="#2a3a5a">ใบรับรองการตรวจสอบลิฟต์</text>
        <path d="M${pt(P(850, 590, 1.27))}L${pt(P(850, 590, 1.43))}M${pt(P(850, 606, 1.27))}L${pt(P(850, 606, 1.4))}M${pt(P(850, 622, 1.27))}L${pt(P(850, 622, 1.42))}" stroke="#8a8478" stroke-width="2"/>
        <ellipse cx="${f1(P(850, 630, 1.44)[0])}" cy="${f1(P(850, 630, 1.44)[1])}" rx="9" ry="13" fill="none" stroke="#c8281e" stroke-width="3"/><path d="M${nx},${ny}V${f1(ny + 10)}" stroke="${INK}" stroke-width="2"/></g>`; }
    put(L.set, s);
    // the ceiling light: a diffuser and the light it washes down the doors and walls
    put(L.set, `<g id="${id}-lite">${PL(HQ(300, 360, 720, 1.17, 1.9), `fill="#fffef8" stroke="#c8ced2" stroke-width="3"`)}${PL(HQ(300, 380, 700, 1.19, 1.9), `fill="#fff"`)}
      <rect x="230" y="300" width="620" height="760" fill="url(#qkWash)"/><ellipse cx="540" cy="260" rx="560" ry="420" fill="url(#qkTube)" opacity=".55"/></g>`);
    // the floor display above the doors
    put(L.set, `<rect x="398" y="220" width="284" height="116" rx="14" fill="url(#qkSteelD)" ${OUT3}/><rect x="410" y="230" width="260" height="96" rx="10" fill="#0e0e10"/><rect x="410" y="230" width="260" height="96" rx="10" fill="url(#${id}-scr)"/>
      <defs><linearGradient id="${id}-scr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".1"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
      <path id="${id}-arrow" d="M450,300l22,-38l22,38z" fill="#ff5a3a"/>
      <text id="${id}-num" x="590" y="304" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="74" fill="#ff5a3a">1</text><path d="M420,240h240" stroke="#fff" stroke-width="2" opacity=".15"/>`);
    // the lit ring of 27 (shown when pressed), the hand, the darkness and the emergency lamp
    const k27 = 32 - 27, kb27 = k27 % 2 ? 1.47 : 1.27, [bx, by] = P(850, 840 + Math.floor(k27 / 2) * 44, kb27);
    Qk.liftBtn27 = [bx, by];
    put(L.glow, `<g id="${id}-lit27" opacity="0"><ellipse cx="${f1(bx)}" cy="${f1(by)}" rx="${f1(19 * kb27)}" ry="${f1(24 * kb27)}" fill="none" stroke="#ffb03a" stroke-width="6"/><ellipse cx="${f1(bx)}" cy="${f1(by)}" rx="60" ry="64" fill="url(#qkSun)" opacity=".8"/></g>
      <rect id="${id}-dk" x="-600" y="-600" width="2300" height="3200" fill="#020304" opacity="0"/>
      <g id="${id}-emg" opacity="0"><circle cx="540" cy="150" r="520" fill="url(#qkEmg)"/><rect x="500" y="130" width="80" height="34" rx="8" fill="#ff6a4a"/></g>
      <g id="${id}-hand" transform="translate(${f1(bx + 260)},${f1(by + 760)})">${Qk.povArm()}</g>`);
  }
  // your right forearm in the green jacket, the index finger pointing up-left, its tip at (0,0)
  Qk.povArm = (o = {}) => `<g transform="rotate(${o.rot ?? -28})">
      <path d="M-60,120L-40,980H170L150,110Z" fill="#2fa45a" ${OUT}/><path d="M-50,300H160M-46,520H164" stroke="#e8f0e8" stroke-width="14" opacity=".85"/><path d="M-56,150H154" stroke="#25874a" stroke-width="22"/>
      <path d="M-40,140Q-56,40 -10,10L0,0Q14,-6 22,8L30,40Q60,30 76,60Q100,58 110,86Q134,90 136,124Q132,150 100,160L-30,170Z" fill="#c99068" ${OUT}/>
      <path d="M30,40L36,96M76,60L74,104M110,86L104,118" stroke="#9a6a48" stroke-width="3" fill="none"/><path d="M2,6Q10,0 16,8" stroke="#f6e2d0" stroke-width="5" fill="none"/></g>`;

  // ---------------- the corridor of floor 27 ----------------
  const VX = 540, VY = 870, K = 850, FOC = 5.5, EYE = 1.6, HW = 0.9, CH = 2.6, LEN = 24;
  const cP = (X, Y, d) => { const k = FOC / (FOC + d); return [VX + X * K * k, VY + (EYE - Y) * K * k]; };
  const kz = (d) => FOC / (FOC + d);
  Qk.cP = cP;
  const quad = (pts, attrs) => `<path d="M${pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}Z" ${attrs}/>`;
  // an affine frame lying on a side wall at height Y, depth d: 1 unit = 1 cm, x along the wall in reading direction, y down
  const wallMat = (side, Y, d, minS = 0) => {
    const X = side * HW, p0 = cP(X, Y, d), pu = cP(X, Y, d - side * 0.01), pv = cP(X, Y - 0.01, d);
    let ux = pu[0] - p0[0], uy = pu[1] - p0[1];
    const vx = pv[0] - p0[0], vy = pv[1] - p0[1], lu = Math.hypot(ux, uy), lv = Math.hypot(vx, vy);
    if (lu < lv * minS) { ux *= (lv * minS) / lu; uy *= (lv * minS) / lu; }
    return `matrix(${ux.toFixed(4)},${uy.toFixed(4)},${vx.toFixed(4)},${vy.toFixed(4)},${f1(p0[0])},${f1(p0[1])})`;
  };
  function qkCorridor(L, o = {}) {
    const id = o.id || "cr", dark = !!o.dark, r = mk(o.seed || 27);
    put(L.sky, `<rect x="-1500" y="-1500" width="4000" height="5000" fill="#1a1612"/>`);
    const W = (side, y0, y1, d0, d1) => { const X = side * HW; return [cP(X, y0, d0), cP(X, y1, d0), cP(X, y1, d1), cP(X, y0, d1)]; };
    const Fq = (x0, x1, d0, d1, Y = 0) => [cP(x0, Y, d0), cP(x1, Y, d0), cP(x1, Y, d1), cP(x0, Y, d1)];
    const ln = (a, b) => `M${pt(a)}L${pt(b)}`;
    let s = "";
    // ---- the carpet: a dark border along each wall with a gold line, lozenges down the middle
    s += quad(Fq(-HW, HW, 0, LEN), `fill="#2c4547"`);
    s += `<path d="${SP(Fq(-HW, -HW + 0.17, 0, LEN))}${SP(Fq(HW - 0.17, HW, 0, LEN))}" fill="#1c2f31"/>`;
    s += `<path d="${ln(cP(-HW + 0.17, 0, 0), cP(-HW + 0.17, 0, LEN))}${ln(cP(HW - 0.17, 0, 0), cP(HW - 0.17, 0, LEN))}" stroke="#b89a5a" stroke-width="3" opacity=".65"/>`;
    s += `<path d="${ln(cP(-HW + 0.24, 0, 0), cP(-HW + 0.24, 0, LEN))}${ln(cP(HW - 0.24, 0, 0), cP(HW - 0.24, 0, LEN))}" stroke="#b89a5a" stroke-width="1.5" opacity=".4"/>`;
    let lz = "", lzi = "", lzd = "";
    for (let d = 0; d < LEN; d += 1.2) {
      lz += SP([cP(0, 0, d), cP(0.36, 0, d + 0.6), cP(0, 0, d + 1.2), cP(-0.36, 0, d + 0.6)]);
      lzi += SP([cP(0, 0, d + 0.3), cP(0.18, 0, d + 0.6), cP(0, 0, d + 0.9), cP(-0.18, 0, d + 0.6)]);
      for (const xx of [-0.5, 0.5]) { const [x, y] = cP(xx, 0, d + 0.6), kk = kz(d + 0.6); lzd += `M${f1(x - 5 * kk)},${f1(y)}h${f1(10 * kk)}`; }
    }
    s += `<path d="${lz}" fill="#3d5d5a"/><path d="${lzi}" fill="#22393a"/>`;
    // ---- the walls: paper above a wainscot, a chair rail, a dark skirting, a crown moulding; AO in the corners
    for (const side of [-1, 1]) {
      s += quad(W(side, 0, CH, 0, LEN), `fill="url(#qkCorrWall)"`);
      let wp = ""; for (let d = 0.15; d < LEN; d += 0.3) wp += ln(cP(side * HW, 0.98, d), cP(side * HW, CH - 0.07, d));
      s += `<path d="${wp}" stroke="#cdbb98" stroke-width="1.5" opacity=".35"/>`;
      s += quad(W(side, 0.12, 0.92, 0, LEN), `fill="url(#qkWainscot)"`);
      let wj = ""; for (let d = 0.3; d < LEN; d += 0.6) wj += ln(cP(side * HW, 0.15, d), cP(side * HW, 0.89, d));
      s += `<path d="${wj}" stroke="#9a8460" stroke-width="2" opacity=".45"/>`;
      s += quad(W(side, 0.92, 0.97, 0, LEN), `fill="#7a5a3a"`) + `<path d="${ln(cP(side * HW, 0.97, 0), cP(side * HW, 0.97, LEN))}" stroke="#d8b890" stroke-width="2" opacity=".8"/>`;
      s += quad(W(side, 0, 0.12, 0, LEN), `fill="#3e3024"`) + `<path d="${ln(cP(side * HW, 0.12, 0), cP(side * HW, 0.12, LEN))}" stroke="#a88a64" stroke-width="2.5"/>`;
      s += quad(W(side, CH - 0.08, CH, 0, LEN), `fill="#f6f0e4"`) + `<path d="${ln(cP(side * HW, CH - 0.08, 0), cP(side * HW, CH - 0.08, LEN))}" stroke="#bcae94" stroke-width="2"/>`;
      s += quad(W(side, 0.12, 0.2, 0, LEN), `fill="#000" opacity=".08"`) + quad(Fq(side * HW, side * (HW - 0.08), 0, LEN), `fill="#000" opacity=".22"`);
    }
    // ---- the ceiling: plaster, slot diffusers along the walls, smoke detectors, sprinklers, an access hatch
    s += quad(Fq(-HW, HW, 0, LEN, CH), `fill="#e8e2d6"`);
    s += `<path d="${SP(Fq(-0.72, -0.68, 0.4, LEN - 0.4, CH))}${SP(Fq(0.68, 0.72, 0.4, LEN - 0.4, CH))}" fill="#6a665e" opacity=".7"/>`;
    let sm = "", spk = "";
    for (const d of [2.6, 8.6, 14.6, 20.6]) { const [x, y] = cP(0, CH, d), kk = kz(d); sm += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(70 * kk)}" ry="${f1(18 * kk)}" fill="#fbfbf8" stroke="#a8a49a" stroke-width="${f1(Math.max(1, 3 * kk))}"/><circle cx="${f1(x + 30 * kk)}" cy="${f1(y + 4 * kk)}" r="${f1(Math.max(1, 5 * kk))}" fill="#e8443a"/>`; }
    for (let d = 1.2; d < LEN; d += 3) for (const xx of [-0.42, 0.42]) { const [x, y] = cP(xx, CH, d), kk = kz(d); spk += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(Math.max(1, 6 * kk))}" fill="#a8a296"/>`; }
    s += sm + spk + quad(Fq(-0.3, 0.3, 11.2, 11.8, CH), `fill="none" stroke="#bcb4a4" stroke-width="2"`);
    // ---- the far end: the lift in its frame with an indicator and a call button; the fire stair door; a plant
    const e = (X, Y) => cP(X, Y, LEN);
    s += quad([e(-HW, 0), e(HW, 0), e(HW, CH), e(-HW, CH)], `fill="#e2d8c6"`);
    s += quad([e(-0.86, 0), e(-0.02, 0), e(-0.02, 2.24), e(-0.86, 2.24)], `fill="#8a9298"`) + quad([e(-0.78, 0), e(-0.1, 0), e(-0.1, 2.12), e(-0.78, 2.12)], `fill="url(#qkSteel)"`) + quad([e(-0.45, 0), e(-0.43, 0), e(-0.43, 2.12), e(-0.45, 2.12)], `fill="#4e565c"`);
    s += quad([e(-0.62, 2.3), e(-0.26, 2.3), e(-0.26, 2.44), e(-0.62, 2.44)], `fill="#141414"`) + quad([e(0.03, 1.02), e(0.11, 1.02), e(0.11, 1.2), e(0.03, 1.2)], `fill="#c8ced2"`);
    s += quad([e(0.11, 0), e(0.84, 0), e(0.84, 2.12), e(0.11, 2.12)], `fill="#6e2a1e"`) + quad([e(0.15, 0), e(0.8, 0), e(0.8, 2.05), e(0.15, 2.05)], `fill="#9a3a2a"`);
    s += quad([e(0.4, 1.35), e(0.56, 1.35), e(0.56, 1.8), e(0.4, 1.8)], `fill="#cfe2ea"`) + quad([e(0.2, 0.98), e(0.74, 0.98), e(0.74, 1.06), e(0.2, 1.06)], `fill="#c8ccce"`);
    s += quad([e(0.6, 1.0), e(0.7, 1.0), e(0.7, 1.08), e(0.6, 1.08)], `fill="#d8d0c0"`);
    const [ex, ey] = e(0.47, 2.3);
    const ek = kz(LEN);
    put(L.glow, `<g id="${id}-exit"><ellipse cx="${f1(ex)}" cy="${f1(ey)}" rx="${f1(140 * ek * 6)}" ry="${f1(90 * ek * 6)}" fill="url(#qkExit)"/>
      <rect x="${f1(ex - 46 * ek * 4)}" y="${f1(ey - 16 * ek * 4)}" width="${f1(92 * ek * 4)}" height="${f1(32 * ek * 4)}" rx="3" fill="#18b45a"/>
      <path d="M${f1(ex - 30 * ek * 4)},${f1(ey + 8 * ek * 4)}l${f1(8 * ek * 4)},-${f1(16 * ek * 4)}l${f1(8 * ek * 4)},${f1(8 * ek * 4)}" stroke="#fff" stroke-width="${f1(4 * ek * 4)}" fill="none"/></g>`);
    // ---- the doors: a casing proud of the wall, a two-panel leaf, kick plate, lever, peephole, the brass number
    const doors = [1.4, 4.6, 7.8, 11, 14.2, 17.4, 20.6];
    let open = "";
    doors.forEach((d, k) => {
      for (const side of [-1, 1]) {
        const X = side * HW, Xc = X - side * 0.025, n = side < 0 ? 2701 + 2 * (6 - k) : 2702 + 2 * (6 - k) + (k === 0 ? 12 : 0), kk = kz(d);
        s += quad([cP(Xc, 0, d - 0.08), cP(Xc, 2.18, d - 0.08), cP(Xc, 2.18, d + 1.08), cP(Xc, 0, d + 1.08)], `fill="#c4a882"`);
        s += quad([cP(X, 2.18, d - 0.08), cP(Xc, 2.18, d - 0.08), cP(Xc, 2.18, d + 1.08), cP(X, 2.18, d + 1.08)], `fill="#e2ceb0"`);
        if (o.open && side > 0 && k === 0) {
          // 2714 open: the room's daylight beyond, its floor, the leaf swung in; light spilling on the carpet
          s += quad(W(side, 0, 2.1, d, d + 1.0), `fill="url(#qkRoomLight)"`) + quad(W(side, 0, 0.32, d, d + 1.0), `fill="#c89a68" opacity=".75"`);
          s += quad([cP(X + 0.6, 0.95, d + 0.35), cP(X + 0.6, 1.7, d + 0.35), cP(X + 0.6, 1.7, d + 0.75), cP(X + 0.6, 0.95, d + 0.75)], `fill="#bfe0f2" opacity=".8"`);
          s += quad([cP(X, 0, d + 0.06), cP(X, 2.1, d + 0.06), cP(X + 0.78, 2.1, d + 0.3), cP(X + 0.78, 0, d + 0.3)], `fill="url(#qkDoorWood)" stroke="${INK}" stroke-width="3"`);
          s += quad([cP(X + 0.12, 0.35, d + 0.1), cP(X + 0.12, 0.95, d + 0.1), cP(X + 0.66, 0.95, d + 0.27), cP(X + 0.66, 0.35, d + 0.27)], `fill="#4a2e1a" opacity=".3"`) + quad([cP(X + 0.12, 1.12, d + 0.1), cP(X + 0.12, 1.9, d + 0.1), cP(X + 0.66, 1.9, d + 0.27), cP(X + 0.66, 1.12, d + 0.27)], `fill="#4a2e1a" opacity=".3"`);
          open = quad([cP(X, 0, d), cP(X, 0, d + 1.0), cP(0.15, 0, d + 1.25), cP(0.15, 0, d + 0.2)], `fill="#fff1d0" opacity=".3"`);
          continue;
        }
        s += quad(W(side, 0, 2.1, d, d + 1.0), `fill="url(#qkDoorWood)" stroke="#3a2618" stroke-width="2"`);
        s += `<defs><clipPath id="${id}-dc${k}${side}"><path d="${SP(W(side, 0, 2.1, d, d + 1.0))}"/></clipPath></defs><g clip-path="url(#${id}-dc${k}${side})">${(() => { let gl = ""; for (let q = 0; q < 9; q++) { const dd = d + 0.06 + q * 0.11; gl += ln(cP(X, 0.05, dd + (q % 2) * 0.02), cP(X, 2.05, dd)); } return `<path d="${gl}" stroke="#3e2614" stroke-width="${f1(Math.max(0.8, 2 * kk))}" opacity=".35"/>`; })()}</g>`;
        for (const [y0, y1] of [[0.34, 0.98], [1.12, 1.92]]) {
          s += quad(W(side, y0, y1, d + 0.15, d + 0.85), `fill="#3a2414" opacity=".32"`);
          s += `<path d="${ln(cP(X, y0, d + 0.15), cP(X, y0, d + 0.85))}" stroke="#d09a6e" stroke-width="${f1(Math.max(1, 3 * kk))}" opacity=".75"/><path d="${ln(cP(X, y1, d + 0.15), cP(X, y1, d + 0.85))}" stroke="#20120a" stroke-width="${f1(Math.max(1, 3 * kk))}" opacity=".55"/>`;
        }
        s += quad(W(side, 0.02, 0.22, d + 0.05, d + 0.95), `fill="#b8bec2"`) + `<path d="${ln(cP(X, 0.21, d + 0.05), cP(X, 0.21, d + 0.95))}" stroke="#fff" stroke-width="${f1(Math.max(1, 2 * kk))}" opacity=".7"/>`;
        const hd = side < 0 ? d + 0.88 : d + 0.12, [hx, hy] = cP(X, 1.0, hd), [lx, ly] = cP(X, 1.0, hd + (side < 0 ? -0.14 : 0.14));
        s += `<circle cx="${f1(hx)}" cy="${f1(hy)}" r="${f1(Math.max(2, 20 * kk))}" fill="#b8a060" stroke="#5a4a20" stroke-width="${f1(Math.max(0.8, 2 * kk))}"/><path d="M${f1(hx)},${f1(hy)}L${f1(lx)},${f1(ly)}" stroke="#d8c070" stroke-width="${f1(Math.max(2, 13 * kk))}" stroke-linecap="round"/><path d="M${f1(hx)},${f1(hy - 3 * kk)}L${f1(lx)},${f1(ly - 3 * kk)}" stroke="#fff6d0" stroke-width="${f1(Math.max(0.8, 3 * kk))}" stroke-linecap="round" opacity=".7"/>`;
        const [ph, pv] = cP(X, 1.52, d + 0.5);
        s += `<circle cx="${f1(ph)}" cy="${f1(pv)}" r="${f1(Math.max(1.5, 9 * kk))}" fill="#c8ccce"/><circle cx="${f1(ph)}" cy="${f1(pv)}" r="${f1(Math.max(1, 4 * kk))}" fill="#1a1a1c"/>`;
        s += quad(W(side, 1.66, 1.82, d + 0.32, d + 0.68), `fill="url(#qkBrass)" stroke="#6a4a12" stroke-width="${f1(Math.max(0.6, 2 * kk))}"`);
        s += `<text transform="${wallMat(side, 1.705, d + 0.5, 0.12)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="12" fill="#3a2a10">${n}</text>`;
        s += quad([cP(Xc, 0, d + 1.0), cP(Xc, 2.1, d + 1.0), cP(X, 2.1, d + 1.0), cP(X, 0, d + 1.0)], `fill="#5a3e28"`);
        s += quad([cP(X, 0, d - 0.08), cP(X, 2.18, d - 0.08), cP(Xc, 2.18, d - 0.08), cP(Xc, 0, d - 0.08)], `fill="#a88a64"`);
      }
    });
    s += open;
    // ---- framed pictures between doors (they swing in a quake), the fire hose cabinet, the alarm, the extinguisher, CCTV
    const ART = [
      (g) => `<rect x="-26" y="-20" width="52" height="40" fill="#f2e2c4"/><circle cx="8" cy="-4" r="11" fill="#e8823a"/><path d="M-26,8q13,-8 26,0t26,0V20H-26Z" fill="#4a8aa8"/><path d="M-26,14q13,-6 26,0t26,0" stroke="#fff" stroke-width="1.5" fill="none" opacity=".6"/>`,
      (g) => `<rect x="-26" y="-20" width="52" height="40" fill="#e8ecee"/><rect x="-20" y="-14" width="22" height="18" fill="#3a6ab0"/><rect x="-2" y="-4" width="20" height="20" fill="#e8b83a"/><circle cx="12" cy="-10" r="7" fill="#d8443a"/><path d="M-20,12h18" stroke="#2a2a2a" stroke-width="3"/>`,
      (g) => `<rect x="-26" y="-20" width="52" height="40" fill="#f4efe2"/><path d="M0,16C-16,4 -14,-12 0,-18C14,-12 16,4 0,16Z" fill="#5a9a5a"/><path d="M0,16V-16M0,-4l-8,-6M0,4l8,-6" stroke="#2e5a2e" stroke-width="1.5"/>`,
    ];
    let art = "", ai = 0;
    [[6.7, -1], [6.7, 1], [13.1, -1], [13.1, 1], [19.5, -1], [19.5, 1]].forEach(([c, side], q) => {
      const X = side * HW, [nx, ny] = cP(X, 1.95, c);
      art += `<g id="${id}-art${ai}" data-o="${f1(nx)} ${f1(ny)}">${quad(W(side, 1.22, 1.86, c - 0.36, c + 0.36), `fill="#000" opacity=".12"`)}${quad(W(side, 1.25, 1.9, c - 0.34, c + 0.34), `fill="#2a2420"`)}${quad(W(side, 1.29, 1.86, c - 0.3, c + 0.3), `fill="#f8f6f0"`)}
        <g transform="${wallMat(side, 1.575, c)}">${ART[q % 3]()}</g><path d="M${f1(nx)},${f1(ny)}L${pt(cP(X, 1.9, c - 0.12))}M${f1(nx)},${f1(ny)}L${pt(cP(X, 1.9, c + 0.12))}" stroke="#8a8478" stroke-width="1.5"/></g>`;
      ai++;
    });
    s += art;
    { // fire hose cabinet, the bell and the call point above it, the extinguisher on the floor beside it
      const S2 = -1, X = S2 * HW, c = 9.8;
      s += quad(W(S2, 0.5, 1.5, c - 0.4, c + 0.4), `fill="url(#qkRedCab)" stroke="#5a1410" stroke-width="2"`) + quad(W(S2, 0.58, 1.42, c - 0.34, c + 0.34), `fill="#7a1a14"`);
      s += `<g transform="${wallMat(S2, 1.0, c)}"><circle r="26" fill="#c8281e" stroke="#e8e2d6" stroke-width="4"/><circle r="9" fill="#9a9e9e"/><path d="M-26,0a26,26 0 0 1 26,-26" stroke="#ffd0c0" stroke-width="3" fill="none" opacity=".6"/></g>`;
      s += quad(W(S2, 0.58, 1.42, c - 0.34, c + 0.34), `fill="url(#qkCabGlassX)" opacity=".5"`) + quad(W(S2, 1.32, 1.4, c - 0.3, c + 0.3), `fill="#fbfbf8"`);
      s += `<text transform="${wallMat(S2, 1.345, c)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="6" fill="#c8281e">สายฉีดดับเพลิง</text>`;
      s += `<g transform="${wallMat(S2, 1.8, c)}"><circle r="12" fill="#d8312a" stroke="#5a1410" stroke-width="2"/><circle r="5" fill="#c8ccce"/></g>`;
      s += quad(W(S2, 1.38, 1.55, c + 0.5, c + 0.66), `fill="#d8312a" stroke="#5a1410" stroke-width="1.5"`) + quad(W(S2, 1.42, 1.51, c + 0.54, c + 0.62), `fill="#fbfbf8"`);
      const [fx, fy] = cP(X + 0.12, 0, c + 0.62), fk = kz(c + 0.62);
      s += `<g transform="translate(${f1(fx)},${f1(fy)}) scale(${f1(fk * 1.4)})">${CS(0, 0, 40, 8)}<rect x="-15" y="-120" width="30" height="120" rx="12" fill="url(#qkRedCab)" ${OUT2}/><rect x="-15" y="-80" width="30" height="34" fill="#fbfbf8"/><path d="M-6,-120v-14h14l10,6" stroke="#2a2a2a" stroke-width="5" fill="none"/><rect x="-11" y="-116" width="7" height="110" rx="3" fill="#fff" opacity=".3"/></g>`;
    }
    { const [cx2, cy2] = cP(0.78, CH - 0.06, 2.6), kk = kz(2.6); s += `<g transform="translate(${f1(cx2)},${f1(cy2)}) scale(${f1(kk * 1.3)})"><path d="M0,-6V18" stroke="#9aa0a4" stroke-width="8"/><rect x="-60" y="14" width="76" height="34" rx="8" fill="#f2f2ee" ${OUT2}/><rect x="-74" y="18" width="16" height="26" rx="4" fill="#2a2e32"/><circle cx="-66" cy="31" r="6" fill="#5a7aa0"/><path d="M-50,18h56" stroke="#fff" stroke-width="3" opacity=".7"/></g>`; }
    put(L.set, s);
    // ---- ceiling lights and sconces (their light flickers together), with the pools they throw on the carpet and walls
    let lamps = "";
    for (let d = 1; d < LEN; d += 3) {
      lamps += quad(Fq(-0.28, 0.28, d - 0.03, d + 0.63, CH), `fill="#c8c2b6"`) + quad(Fq(-0.25, 0.25, d, d + 0.6, CH), dark ? `fill="#cfc8bc"` : `fill="#fffbf0"`);
      if (!dark) { const [lx, ly] = cP(0, 0, d + 0.3), kk = kz(d); lamps += `<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="${f1(700 * kk)}" ry="${f1(200 * kk)}" fill="url(#qkDown)" opacity=".5"/>`; }
    }
    for (const [c, side] of [[3.5, -1], [3.5, 1], [9.9, 1], [16.3, -1], [16.3, 1]]) {
      const X = side * HW;
      if (!dark) lamps += quad([cP(X, 2.0, c - 0.05), cP(X, CH - 0.08, c - 0.42), cP(X, CH - 0.08, c + 0.42), cP(X, 2.0, c + 0.05)], `fill="#fff4d6" opacity=".38"`) + quad([cP(X, 1.8, c - 0.05), cP(X, 1.1, c - 0.32), cP(X, 1.1, c + 0.32), cP(X, 1.8, c + 0.05)], `fill="#fff4d6" opacity=".26"`);
      lamps += quad([cP(X, 1.79, c - 0.09), cP(X - side * 0.05, 1.82, c - 0.09), cP(X - side * 0.05, 1.98, c - 0.09), cP(X, 2.01, c - 0.09)], dark ? `fill="#a89c84"` : `fill="#f6e6c0"`)
        + quad(W(side, 1.79, 2.01, c - 0.09, c + 0.09), dark ? `fill="#bcb098"` : `fill="url(#qkSconce)"`)
        + quad(W(side, 1.77, 1.8, c - 0.1, c + 0.1), `fill="#a8843e"`) + quad(W(side, 2.0, 2.03, c - 0.1, c + 0.1), `fill="#a8843e"`);
    }
    put(dark ? L.set : L.glow, `<g id="${id}-lamps">${lamps}</g>`);
    // a sign hung from the ceiling at 5 m: "ลิฟต์ · ทางหนีไฟ"
    const [sx, sy] = cP(0, CH, 5), sk = kz(5);
    Qk.corrSignOrigin = `${f1(sx)} ${f1(sy)}`;
    put(dark ? L.set : L.glow, `<g id="${id}-sign"><path d="M${f1(sx - 200 * sk)},${f1(sy)}V${f1(sy + 150 * sk)}M${f1(sx + 200 * sk)},${f1(sy)}V${f1(sy + 150 * sk)}" stroke="#5a5a5a" stroke-width="${f1(8 * sk)}"/>
      <circle cx="${f1(sx - 200 * sk)}" cy="${f1(sy + 4 * sk)}" r="${f1(9 * sk)}" fill="#8a8a8a"/><circle cx="${f1(sx + 200 * sk)}" cy="${f1(sy + 4 * sk)}" r="${f1(9 * sk)}" fill="#8a8a8a"/>
      <rect x="${f1(sx - 300 * sk)}" y="${f1(sy + 160 * sk)}" width="${f1(600 * sk)}" height="${f1(150 * sk)}" rx="${f1(12 * sk)}" fill="#0e2418"/>
      <rect x="${f1(sx - 300 * sk)}" y="${f1(sy + 150 * sk)}" width="${f1(600 * sk)}" height="${f1(150 * sk)}" rx="${f1(12 * sk)}" fill="#1e3a2c" stroke="#e8e2d0" stroke-width="${f1(6 * sk)}"/>
      <path d="M${f1(sx - 288 * sk)},${f1(sy + 160 * sk)}H${f1(sx + 288 * sk)}" stroke="#fff" stroke-width="${f1(3 * sk)}" opacity=".3"/>
      <text x="${f1(sx)}" y="${f1(sy + 248 * sk)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${f1(70 * sk)}" fill="#f4f0e2">ลิฟต์ · ทางหนีไฟ →</text></g>`);
    // ceiling panels that can fall (drawn in place)
    if (o.panels) put(L.glow, [6.5, 10, 13.5].map((d, k) => `<g id="${id}-p${k}">${quad([cP(-0.6, CH - 0.01, d), cP(0.6, CH - 0.01, d), cP(0.6, CH - 0.01, d + 0.6), cP(-0.6, CH - 0.01, d + 0.6)], `fill="#efe9de" stroke="#9a9286" stroke-width="3"`)}</g>`).join(""));
  }
  Sets.DEFS += `<linearGradient id="qkSconce" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2dcae"/><stop offset=".5" stop-color="#fffaea"/><stop offset="1" stop-color="#ecd29e"/></linearGradient>`;
  Sets.DEFS += `<linearGradient id="qkCabGlassX" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".7"/><stop offset=".45" stop-color="#fff" stop-opacity=".05"/><stop offset=".6" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity=".05"/></linearGradient>`;
  // the corridor reacting to a quake: the hung sign and the pictures swing, plaster dust drops from the ceiling
  Qk.reactCorridor = (tl, id, t0, dur, amp = 1, o = {}) => {
    if (o.sign !== false) Qk.swing(tl, `#${id}-sign`, Qk.corrSignOrigin, t0, dur, 15 * amp, 0.42);
    for (let k = 0; k < 6; k++) { const el = document.getElementById(`${id}-art${k}`); if (el) Qk.swing(tl, el, el.getAttribute("data-o"), t0 + k * 0.04, dur, 4.5 * amp, 0.34 + (k % 3) * 0.05); }
    if (o.layer) Qk.debris(tl, o.layer, { t0, dur, n: o.n || 16, seed: o.seed || 3, pts: (r) => { const d = 1.5 + r() * 12, X = (r() - 0.5) * 1.4, [x, y0] = cP(X, CH, d), y1 = cP(X, 0, d)[1]; return { x, y0, y1, s: 3 + 9 * kz(d) }; } });
  };

  Object.assign(Sets, { qkTower, qkLobby, qkLift, qkCorridor });
})();
