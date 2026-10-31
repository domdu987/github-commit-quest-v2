// "ตึกโยก" sets, part 2 — room 2714 (มิว's condo), seen from the entrance toward the window wall, plus its close-ups.
// Load after qkmat.js and quake.js (uses Qk.city and the material kit). Same layer contract as pop2.js. Seeded RNG only.
// The room is a real box in one-point perspective: Qk.room3(X, Y, Z) → screen, in metres (X right of the view axis, Y up from the
// floor, Z away from the camera; the back wall at Z 6, the ceiling at 4.31 m, the eye at 2.07 m). Screen anchors the shots rely on:
// the back wall's floor line y 1380, its ceiling line y 300, the vanishing point (1050, 860), the window x 380…1720 × y 330…1360,
// the table's front legs on y 1640 (FLOOR) with its top's front edge at y 1358, x 690…1410.
//   Sets.qkRoom(L, o)    the room front on. Ceiling with downlights; the window wall (deep reveal, dark aluminium frame, a transom,
//                        sliding-door handles) with the balcony outside (tiles, a glass balustrade, potted plants) and the city
//                        beyond; linen drapes on tie-backs over sheers; an oak floor with the sun's patch through the panes and the
//                        table's shadow in it; a cream rug with a rust border under the dining table; two chairs; the pendant lamp.
//                        Left wall (seen in close-ups): the fridge with magnets and the note, the microwave, the kitchen (upper
//                        cabinets, tiled splash-back, granite top, the portable gas stove #id-stove and its spare canister #id-can,
//                        the kettle, the rice cooker), the Buddha cabinet (#id-candles, #id-drawer), the family photo (#id-photo), the
//                        clock (#id-cH / #id-cM). Right: a side table and a floor lamp, the bookshelf (#id-shelf, books #id-books with
//                        .qkBook children), the air conditioner, the aquarium (#id-tank, #id-aqw water, #id-fish) and a print (#id-photo2).
//                        Reactive props (Qk.react swings them): #id-curL / #id-curR (drapes), #id-photo / #id-photo2, #id-clock,
//                        #id-plant, #id-tprops (things on the table), #id-kprops (on the counter), #id-chL / #id-chR (chairs),
//                        #id-bplants (balcony plants), #id-flamp (floor lamp). Pivots ride on data-o="x y".
//                        The dining table #id-tbl (props and its shadow inside; Qk.tableFront redraws its near parts over people
//                        under it), the glass of water #id-cup, the lamp #id-lamp (swing it around Qk.lampPivot) and its light
//                        #id-lampGlow (in glow).
//                        o.lampDown: the lamp lies on the table · o.after: the aftermath (broken panes, shards, the shelf down, books,
//                        the lamp on the table, a chair over, the photo on the floor, plaster, the canister on the floor with its
//                        shimmer #id-gas, the clock stopped crooked) · o.dark: lamps off · o.bag: the delivery bag on the table ·
//                        o.frame "door": the corridor wall with 2714's doorway (x 700…1400, y 330…1700) and the hooks inside the door
//                        (#id-hooks: school bag, the red emergency bag with a torch) · o.under {x, top, half, G}: the table huge in
//                        glow as a foreground frame for under-the-table shots
//   Qk.react(tl, id, t0, dur, a, o)  the room answers the quake: drapes, frames, the clock, plants, chairs, the things on the table and
//                        counter, books, the balcony plants; a (0…1.5) scales it; o.fall [t…] drops books off the shelf at those
//                        seconds into the shot; o.dust adds plaster dust from the ceiling
//   Sets.qkFridge(L, o)  the fridge door close: magnets, a child's drawing (#id-draw falls), a photo strip, the note's spot (#id-note)
//   Sets.qkCup(L, o)     insert on the tabletop: the glass of water (#id-rings ripple, #id-surf), มิว's phone showing the time
//                        (#id-t19 / #id-t20), crayons; the room soft behind
//   Sets.qkPlan(L, o)    แผนผังห้อง that แม่ drew on graph paper (top-down): walls, window (blue), door, table, chairs, shelf, tank,
//                        fridge, stove, the lamp; danger zones #id-z0…#id-z3 (glass, shelf, tank, gas; red, hatched) with labels #id-l0…#id-l3, the safe zone
//                        #id-safe (green) with two dots #id-you #id-mew and a tick #id-ok
(function () {
  const { mk, f1, put } = Pop2;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const OUT2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round"`;
  const Qk = (window.Qk = window.Qk || {});
  const { cs, tone, grain, brushed, streaks, knob, handle } = Qk;
  const GB = 1380, CEIL = 300, VPX = 1050, VPY = 860;
  const FOC = 1504, EYE = 2.074, ZW = 6, HC = 4.31;
  const R = (X, Y, Z) => [VPX + (FOC * X) / Z, VPY + (FOC * (EYE - Y)) / Z];
  Qk.room3 = R;
  Qk.lampPivot = "1050 103";
  const f4 = (v) => (+v).toFixed(4);
  const pp = (a) => a.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L");
  const poly = (a, at = "") => `<path d="M${pp(a)}Z" ${at}/>`;
  const ln = (a, b) => `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}`;
  const hq = (x0, x1, z0, z1, Y, at) => poly([R(x0, Y, z0), R(x1, Y, z0), R(x1, Y, z1), R(x0, Y, z1)], at);
  const vq = (x0, x1, y0, y1, Z, at) => poly([R(x0, y0, Z), R(x1, y0, Z), R(x1, y1, Z), R(x0, y1, Z)], at);
  const sq = (X, y0, y1, z0, z1, at) => poly([R(X, y0, z0), R(X, y1, z0), R(X, y1, z1), R(X, y0, z1)], at);
  // a box in the room (metres): the faces the camera can see
  const box3 = (x0, x1, y0, y1, z0, z1, o) => {
    const at = (f) => `fill="${f}" ${o.out ?? OUT2}`;
    let s = "";
    if (x1 < 0 && o.side) s += sq(x1, y0, y1, z0, z1, at(o.side));
    if (x0 > 0 && o.side) s += sq(x0, y0, y1, z0, z1, at(o.side));
    if (y1 < EYE && o.top) s += hq(x0, x1, z0, z1, y1, at(o.top));
    if (y0 > EYE && o.bottom) s += hq(x0, x1, z0, z1, y0, at(o.bottom));
    if (o.front) s += vq(x0, x1, y0, y1, z0, at(o.front));
    return s;
  };
  // things against the back wall: the back face in wall-plane screen coordinates, d metres deep; WM(d) maps wall-plane coordinates onto
  // the front face (draw details on the front inside <g transform="WM(d)">)
  const WS = (d) => ZW / (ZW - d);
  const wf = (x, y, d) => { const s = WS(d); return [VPX + (x - VPX) * s, VPY + (y - VPY) * s]; };
  const WM = (d) => { const s = WS(d); return `matrix(${f4(s)},0,0,${f4(s)},${f1(VPX * (1 - s))},${f1(VPY * (1 - s))})`; };
  const wbox = (x0, y0, x1, y1, d, o) => {
    const F = (x, y) => wf(x, y, d), at = (f) => `fill="${f}" ${o.out ?? OUT2}`;
    let s = "";
    if (x1 < VPX && o.side) s += poly([[x1, y0], F(x1, y0), F(x1, y1), [x1, y1]], at(o.side));
    if (x0 > VPX && o.side) s += poly([[x0, y0], F(x0, y0), F(x0, y1), [x0, y1]], at(o.side));
    if (y0 > VPY && o.top) s += poly([[x0, y0], [x1, y0], F(x1, y0), F(x0, y0)], at(o.top));
    if (y1 < VPY && o.bottom) s += poly([[x0, y1], [x1, y1], F(x1, y1), F(x0, y1)], at(o.bottom));
    const [a, b] = F(x0, y0), [c, e] = F(x1, y1);
    if (o.front) s += `<rect x="${f1(a)}" y="${f1(b)}" width="${f1(c - a)}" height="${f1(e - b)}" fill="${o.front}" ${o.out ?? OUT2}/>`;
    return s;
  };
  // a soft shadow on the floor along the front bottom edge of a wall-standing thing
  const footShadow = (x0, x1, d, op = 0.55) => { const [a, y] = wf(x0, GB, d), [b] = wf(x1, GB, d); return cs((a + b) / 2, y + 4, (b - a) / 2 + 30, 18, op); };

  Sets.DEFS += `
    <linearGradient id="qkRoomWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ebe2d4"/><stop offset=".5" stop-color="#f3ece1"/><stop offset="1" stop-color="#e8decf"/></linearGradient>
    <linearGradient id="qkCeil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfc5b4"/><stop offset=".7" stop-color="#e6ded1"/><stop offset="1" stop-color="#efe8dc"/></linearGradient>
    <radialGradient id="qkBloom"><stop offset="0" stop-color="#fffaf0" stop-opacity=".75"/><stop offset=".6" stop-color="#fff6e6" stop-opacity=".25"/><stop offset="1" stop-color="#fff6e6" stop-opacity="0"/></radialGradient>
    <linearGradient id="qkFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d6ae80"/><stop offset="1" stop-color="#a87a4e"/></linearGradient>
    <linearGradient id="qkTable" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a36"/><stop offset=".5" stop-color="#a8764a"/><stop offset="1" stop-color="#7a4e2e"/></linearGradient>
    <linearGradient id="qkTableTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8875a"/><stop offset="1" stop-color="#a07048"/></linearGradient>
    <linearGradient id="qkTopW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cf9a64"/><stop offset=".35" stop-color="#b98450"/><stop offset="1" stop-color="#a26c3c"/></linearGradient>
    <linearGradient id="qkFrontW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#94603a"/><stop offset="1" stop-color="#6c4022"/></linearGradient>
    <linearGradient id="qkLegW" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7e4c2a"/><stop offset=".4" stop-color="#a06a40"/><stop offset="1" stop-color="#6a3e22"/></linearGradient>
    <linearGradient id="qkPane" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".26"/><stop offset=".4" stop-color="#d8f0fa" stop-opacity=".06"/><stop offset=".55" stop-color="#ffffff" stop-opacity=".16"/><stop offset="1" stop-color="#d8f0fa" stop-opacity=".05"/></linearGradient>
    <linearGradient id="qkRail" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2f4f8" stop-opacity=".35"/><stop offset="1" stop-color="#8fc0cc" stop-opacity=".55"/></linearGradient>
    <linearGradient id="qkBalc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b4b0a8"/><stop offset="1" stop-color="#d4d0c6"/></linearGradient>
    <linearGradient id="qkLinen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a99a84"/><stop offset=".45" stop-color="#cdbfa9"/><stop offset="1" stop-color="#b3a48e"/></linearGradient>
    <linearGradient id="qkSheer" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".6"/><stop offset="1" stop-color="#f4f0e8" stop-opacity=".42"/></linearGradient>
    <linearGradient id="qkDome" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#262a2e"/><stop offset=".32" stop-color="#5c636a"/><stop offset=".55" stop-color="#3a3f44"/><stop offset="1" stop-color="#181b1e"/></linearGradient>
    <linearGradient id="qkCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".5"/><stop offset="1" stop-color="#ffe9b0" stop-opacity="0"/></linearGradient>
    <radialGradient id="qkLampG" cx=".5" cy=".1" r=".9"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".75"/><stop offset=".5" stop-color="#ffd88a" stop-opacity=".22"/><stop offset="1" stop-color="#ffd88a" stop-opacity="0"/></radialGradient>
    <linearGradient id="qkFridgeG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e2e6e8"/><stop offset=".55" stop-color="#f8f8f6"/><stop offset="1" stop-color="#d0d5d8"/></linearGradient>
    <linearGradient id="qkGranite" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#55565a"/><stop offset="1" stop-color="#303033"/></linearGradient>
    <linearGradient id="qkCab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4eee4"/><stop offset="1" stop-color="#e0d6c6"/></linearGradient>
    <linearGradient id="qkTeak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#84492a"/><stop offset="1" stop-color="#5a2e16"/></linearGradient>
    <linearGradient id="qkGoldG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff2b0"/><stop offset=".45" stop-color="#e8b83a"/><stop offset="1" stop-color="#9a6a14"/></linearGradient>
    <linearGradient id="qkPotG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c8c0b2"/><stop offset=".38" stop-color="#f4f0e8"/><stop offset="1" stop-color="#a8a092"/></linearGradient>
    <linearGradient id="qkTerra" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a85a3a"/><stop offset=".4" stop-color="#d27e56"/><stop offset="1" stop-color="#8a4428"/></linearGradient>
    <linearGradient id="qkLeafG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#62ad5c"/><stop offset="1" stop-color="#2c6634"/></linearGradient>
    <linearGradient id="qkAq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fe2ee" stop-opacity=".85"/><stop offset="1" stop-color="#2a8aa8" stop-opacity=".92"/></linearGradient>
    <linearGradient id="qkACG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdfdfa"/><stop offset="1" stop-color="#d8d8d2"/></linearGradient>
    <linearGradient id="qkCurtain" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfc8bc"/><stop offset=".25" stop-color="#e8e2d8"/><stop offset=".5" stop-color="#c8c0b2"/><stop offset=".75" stop-color="#e4ddd2"/><stop offset="1" stop-color="#c6beb0"/></linearGradient>
    <linearGradient id="qkLightShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6dc" stop-opacity=".5"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></linearGradient>
    <linearGradient id="qkReflect" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0" stop-opacity=".3"/><stop offset="1" stop-color="#fffaf0" stop-opacity="0"/></linearGradient>
    <pattern id="qkGrid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0H0V40" fill="none" stroke="#9cc4dc" stroke-width="1.6" opacity=".7"/></pattern>
    <pattern id="qkHatch" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="22" height="22" fill="#e8443a" opacity=".22"/><path d="M0,0V22" stroke="#e8443a" stroke-width="7" opacity=".55"/></pattern>
    <pattern id="qkTiles" width="60" height="30" patternUnits="userSpaceOnUse"><rect width="60" height="30" fill="#f6f4ee"/><path d="M0,29.5H60M30,0V15M0,14.5H60M0,15V30M60,15V30" stroke="#c8c2b6" stroke-width="2"/><path d="M2,2H28" stroke="#fff" stroke-width="2" opacity=".8"/></pattern>`;

  // ---------------- small things ----------------
  // leaves fanning out of a point (pot plants): n leaves of length len around angle a0 ± spread (degrees, 0 = up)
  const leaves = (x, y, n, len, spread, seed, o = {}) => {
    const r = mk(seed), cols = o.cols || ["#4e9a4c", "#3e8840", "#5aa858", "#2f7234"];
    let s = "";
    for (let i = 0; i < n; i++) {
      const a = ((o.a0 ?? 0) + (i / Math.max(1, n - 1) - 0.5) * 2 * spread + (r() - 0.5) * 14) * Math.PI / 180, L = len * (0.65 + r() * 0.45);
      const ex = x + Math.sin(a) * L, ey = y - Math.cos(a) * L, w = (o.w ?? 0.34) * L, nx = Math.cos(a) * w, ny = Math.sin(a) * w;
      const mx = x + Math.sin(a) * L * 0.55, my = y - Math.cos(a) * L * 0.55, c = cols[Math.floor(r() * cols.length)];
      s += `<path d="M${f1(x)},${f1(y)}Q${f1(mx - nx)},${f1(my - ny)} ${f1(ex)},${f1(ey)}Q${f1(mx + nx)},${f1(my + ny)} ${f1(x)},${f1(y)}Z" fill="${c}" stroke="#1e3a20" stroke-width="1.6"/>`;
      s += `<path d="M${f1(x)},${f1(y)}Q${f1(mx - nx * 0.15)},${f1(my - ny * 0.15)} ${f1(ex)},${f1(ey)}" stroke="#9ad08a" stroke-width="1.6" fill="none" opacity=".55"/>`;
      if (o.split) for (let k = 1; k <= 3; k++) { const t = 0.3 + k * 0.17, px = x + Math.sin(a) * L * t, py = y - Math.cos(a) * L * t; s += `<path d="M${f1(px + nx * 0.9)},${f1(py + ny * 0.9)}L${f1(px + nx * 0.3 + Math.sin(a) * 6)},${f1(py + ny * 0.3 - Math.cos(a) * 6)}" stroke="#efe6d6" stroke-width="3" opacity=".6"/>`; }
    }
    return s;
  };
  // a round pot (truncated cone) standing at (x, y) screen, top radius rt, height h, with a soil top
  const pot = (x, y, rt, h, fill = "url(#qkPotG)") => `${cs(x, y + 2, rt * 1.5, rt * 0.32, 0.8)}<path d="M${f1(x - rt)},${f1(y - h)}L${f1(x - rt * 0.74)},${f1(y)}Q${f1(x)},${f1(y + rt * 0.16)} ${f1(x + rt * 0.74)},${f1(y)}L${f1(x + rt)},${f1(y - h)}Z" fill="${fill}" ${OUT2}/>
    <ellipse cx="${f1(x)}" cy="${f1(y - h)}" rx="${f1(rt)}" ry="${f1(rt * 0.2)}" fill="#4a3424" ${OUT2}/><path d="M${f1(x - rt * 0.8)},${f1(y - h * 0.8)}L${f1(x - rt * 0.62)},${f1(y - h * 0.15)}" stroke="#fff" stroke-width="${f1(Math.max(2, rt * 0.1))}" opacity=".45" stroke-linecap="round"/>`;
  // a book standing on a shelf: spine with bands and a title stripe; lean in degrees around its foot
  const book = (x, y, w, h, c, r, lean = 0) => {
    const g = `<rect x="${f1(x)}" y="${f1(y - h)}" width="${f1(w)}" height="${f1(h)}" fill="${c}" stroke="${INK}" stroke-width="1.6"/><path d="M${f1(x + 2)},${f1(y - h + 6)}H${f1(x + w - 2)}M${f1(x + 2)},${f1(y - 8)}H${f1(x + w - 2)}" stroke="${tone(c, 0.45)}" stroke-width="2" opacity=".8"/>
      ${r() < 0.6 ? `<rect x="${f1(x + w * 0.22)}" y="${f1(y - h * 0.7)}" width="${f1(w * 0.56)}" height="${f1(h * 0.28)}" fill="${tone(c, r() < 0.5 ? 0.6 : -0.35)}" opacity=".85"/>` : ""}<path d="M${f1(x + 1.5)},${f1(y - h + 2)}V${f1(y - 2)}" stroke="#fff" stroke-width="1.6" opacity=".35"/>`;
    return lean ? `<g transform="rotate(${f1(lean)} ${f1(lean > 0 ? x + w : x)} ${f1(y)})">${g}</g>` : g;
  };
  const BOOKC = ["#c8463a", "#3a6a9a", "#e8b83a", "#4a8a5a", "#8a4a8a", "#e8e2d6", "#2e4a6a", "#d87a3a", "#6a8a9a"];

  // ---------------- the room ----------------
  function qkRoom(L, o = {}) {
    const id = o.id || "rm", r = mk(o.seed || 31), A = !!o.after, dark = !!o.dark || A;
    Qk.city(L, { hz: 860, seed: 17, id: `${id}c`, below: true, sunX: 1350, x0: 200, x1: 1900 });
    let s = "", gl = "";

    // ceiling: panel joints in perspective, AO along the wall, downlights (their halos go in glow)
    s += `<rect x="-2400" y="-2600" width="6000" height="${CEIL + 2600}" fill="url(#qkCeil)"/>`;
    let cj = "";
    for (const X of [-8.4, -6, -3.6, -1.2, 1.2, 3.6, 6, 8.4]) cj += ln(R(X, HC, ZW), R(X, HC, 1.3));
    for (const Z of [1.7, 2.2, 2.9, 3.8, 4.9]) cj += ln(R(-16, HC, Z), R(16, HC, Z));
    s += `<path d="${cj}" stroke="#bfb4a2" stroke-width="2" opacity=".5"/><rect x="-2400" y="${CEIL - 80}" width="6000" height="80" fill="url(#qkAOup)"/>`;
    for (const [X, Z] of [[-2.4, 2.5], [2.4, 2.5], [-2.4, 4.1], [2.4, 4.1], [-5.6, 3.3], [5.6, 3.3], [0, 2.1]]) {
      const [x, y] = R(X, HC, Z), rx = (FOC * 0.09) / Z, ry = (rx * (HC - EYE)) / Z;
      s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx * 1.45)}" ry="${f1(ry * 1.45)}" fill="#f8f4ec" stroke="#a89e8e" stroke-width="2"/><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" fill="${dark ? "#b8b0a2" : "#fffbe8"}"/>`;
      if (!dark) gl += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx * 6)}" ry="${f1(ry * 6)}" fill="url(#qkPoolW)" opacity=".45"/>`;
    }
    { const [x, y] = R(1.1, HC, 3.4); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="26" ry="16" fill="#f4f2ec" stroke="#9a9286" stroke-width="2"/><ellipse cx="${f1(x)}" cy="${f1(y + 3)}" rx="14" ry="8" fill="#e2ded6"/><circle cx="${f1(x + 9)}" cy="${f1(y + 2)}" r="3" fill="${dark ? "#d83a2a" : "#4ac85a"}"/>`; }
    for (const [X, Z] of [[-1.2, 3.0], [1.2, 3.0], [-3.6, 4.4], [3.6, 4.4]]) { const [x, y] = R(X, HC, Z); s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="6" fill="#c8c2b6" stroke="#8a8478" stroke-width="1.5"/>`; }

    // the back wall with the window opening (a deep reveal) cut out; crown and skirting; AO; a soft bloom around the window
    s += `<path d="M-2400,${CEIL}H3600V${GB}H-2400Z M352,318V${GB}H1748V318Z" fill="url(#qkRoomWall)" fill-rule="evenodd"/>`;
    s += `<rect x="-2400" y="${CEIL}" width="6000" height="70" fill="url(#qkAOdn)"/><ellipse cx="1050" cy="840" rx="1050" ry="720" fill="url(#qkBloom)" opacity=".55"/>`;
    s += `<rect x="-2400" y="${CEIL}" width="6000" height="18" fill="#f8f4ec"/><path d="M-2400,${CEIL + 18}H3600" stroke="#cbbfac" stroke-width="3"/><path d="M-2400,${CEIL + 3}H3600" stroke="#fff" stroke-width="3" opacity=".7"/>`;
    s += `<rect x="-2400" y="${GB - 110}" width="6000" height="110" fill="url(#qkAOup)" opacity=".55"/>`;
    s += `<rect x="-2400" y="${GB - 30}" width="6000" height="30" fill="#f6f1e8"/><path d="M-2400,${GB - 30}H3600" stroke="#cfc3b0" stroke-width="3"/><path d="M-2400,${GB - 27}H3600" stroke="#fff" stroke-width="2" opacity=".8"/><path d="M-2400,${GB - 1}H3600" stroke="#a89a86" stroke-width="2"/>`;

    // outside: the balcony (tiles, a glass balustrade, posts, the handrail, potted plants), clipped to the glass
    let bal = hq(-4.2, 4.2, 6.12, 7.6, -0.02, `fill="url(#qkBalc)"`);
    let bt = ""; for (let X = -4.2; X <= 4.21; X += 0.6) bt += ln(R(X, -0.02, 6.12), R(X, -0.02, 7.6)); for (const Z of [6.6, 7.1]) bt += ln(R(-4.2, -0.02, Z), R(4.2, -0.02, Z));
    bal += `<path d="${bt}" stroke="#8e8a82" stroke-width="2" opacity=".55"/>`;
    bal += `<g id="${id}-bplants">`;
    for (const [X, Z, k] of [[-2.15, 7.3, 0], [1.95, 7.32, 1]]) {
      const [px, py] = R(X, 0, Z), rt = (FOC * 0.17) / Z, ph = (FOC * 0.32) / Z;
      bal += pot(px, py, rt, ph, "url(#qkTerra)") + leaves(px, py - ph, 11, (FOC * 0.62) / Z, 70, 300 + k, { w: 0.3 });
    }
    bal += `</g>`;
    bal += vq(-4.2, 4.2, 0, 1.05, 7.6, `fill="url(#qkRail)"`) + streaks(R(-4.2, 1.05, 7.6)[0], R(0, 1.05, 7.6)[1], 1500, R(0, 0, 7.6)[1] - R(0, 1.05, 7.6)[1], { op: 0.16 });
    for (let X = -3.6; X <= 3.61; X += 1.2) bal += vq(X - 0.025, X + 0.025, 0, 1.05, 7.6, `fill="#59616a"`);
    { const [x0, y0] = R(-4.2, 1.05, 7.6), [x1] = R(4.2, 1.05, 7.6); bal += `<rect x="${f1(x0)}" y="${f1(y0 - 7)}" width="${f1(x1 - x0)}" height="13" rx="6" fill="#8a9298" ${OUT2}/><path d="M${f1(x0)},${f1(y0 - 3)}H${f1(x1)}" stroke="#eef4f6" stroke-width="3" opacity=".75"/>`; }
    bal += vq(-4.2, 4.2, -0.02, 0.07, 7.6, `fill="#5e656c"`);
    s += `<defs><clipPath id="${id}-win"><rect x="380" y="330" width="1340" height="1030"/></clipPath></defs><g clip-path="url(#${id}-win)">${bal}</g>`;

    // the reveal (head, jambs, sill) between the wall's face and the glass
    s += poly([[352, 318], [1748, 318], [1720, 330], [380, 330]], `fill="#d4cbbd"`) + poly([[352, 318], [380, 330], [380, 1360], [352, GB]], `fill="#fbf7f0"`)
      + poly([[1748, 318], [1720, 330], [1720, 1360], [1748, GB]], `fill="#ddd3c3"`) + poly([[352, GB], [1748, GB], [1720, 1360], [380, 1360]], `fill="#efe9de"`);

    // panes (each its own group so it can crack and burst)
    for (let k = 0; k < 4; k++) {
      const x = 380 + k * 335;
      s += `<g id="${id}-pane${k}">${A ? "" : `<rect x="${x}" y="330" width="335" height="1030" fill="url(#qkPane)"/>${streaks(x + 20, 340, 300, 1010, { op: 0.11 })}`}</g>`;
    }
    if (A) {
      // what is left of the panes: jagged teeth along the frame, cracked
      const jag = (pts) => `<path d="M${pp(pts)}Z" fill="#dff2fa" opacity=".5" stroke="#9cc4d4" stroke-width="2"/>`;
      for (let k = 0; k < 4; k++) {
        const x = 380 + k * 335, x1 = x + 335;
        let top = [[x, 330]]; for (let t = 0; t <= 1.001; t += 0.125) top.push([x + 335 * t, 330 + 30 + r() * 110 * Math.sin(Math.PI * t) + 10]); top.push([x1, 330]);
        let lt = [[x, 330]]; for (let t = 0; t <= 1.001; t += 0.1) lt.push([x + 20 + r() * 60 * Math.sin(Math.PI * t), 330 + 1030 * t]); lt.push([x, 1360]);
        let bt2 = [[x, 1360]]; for (let t = 0; t <= 1.001; t += 0.14) bt2.push([x + 335 * t, 1360 - 20 - r() * 90 * Math.sin(Math.PI * t)]); bt2.push([x1, 1360]);
        s += jag(top) + (k % 2 ? jag(lt) : "") + jag(bt2);
        s += `<path d="M${x + 60},${360 + r() * 60}l${30 + r() * 40},${60 + r() * 50}l-20,40M${x1 - 40},1340l-40,-60l20,-30" stroke="#f4fbff" stroke-width="3" fill="none" opacity=".8"/>`;
      }
    }
    // the frame: outer, mullions with their depth, a transom, the sliding doors' handles
    const FR = "#3c4248", FRH = "#7e868e", FRS = "#24282c";
    s += `<rect x="372" y="322" width="1356" height="16" fill="${FR}" ${OUT2}/><path d="M374,325H1726" stroke="${FRH}" stroke-width="2" opacity=".8"/>
      <rect x="370" y="1350" width="1360" height="20" fill="${FR}" ${OUT2}/><path d="M372,1353H1728" stroke="${FRH}" stroke-width="3" opacity=".8"/>
      <rect x="368" y="322" width="22" height="1048" fill="${FR}" ${OUT2}/><rect x="1710" y="322" width="22" height="1048" fill="${FR}" ${OUT2}/>`;
    for (const x of [715, 1050, 1385]) {
      s += `<rect x="${x - 9}" y="330" width="18" height="1030" fill="${FR}" ${OUT2}/><path d="M${x - 6},332V1358" stroke="${FRH}" stroke-width="2" opacity=".7"/>`;
      if (x < 1050) s += `<rect x="${x + 9}" y="330" width="5" height="1030" fill="${FRS}"/>`;
      if (x > 1050) s += `<rect x="${x - 14}" y="330" width="5" height="1030" fill="${FRS}"/>`;
    }
    s += `<rect x="380" y="748" width="1340" height="14" fill="${FR}" ${OUT2}/><rect x="380" y="762" width="1340" height="4" fill="${FRS}"/><path d="M382,750H1718" stroke="${FRH}" stroke-width="2" opacity=".7"/>`;
    s += handle(1026, 960, 120, { t: 12, col: "#9aa2a8" }) + handle(1062, 960, 120, { t: 12, col: "#9aa2a8" });
    // cracks across the panes (hidden; drawn on by the shot) and shards (hidden; fall when the glass bursts)
    let cr = "";
    for (let k = 0; k < 4; k++) {
      const cx = 380 + k * 335 + 120 + r() * 100, cy = 600 + r() * 400;
      for (let j = 0; j < 7; j++) { let d = `M${f1(cx)},${f1(cy)}`, x = cx, y = cy, a = (j / 7) * Math.PI * 2 + r() * 0.5; for (let q = 0; q < 4; q++) { x += Math.cos(a) * (40 + r() * 70); y += Math.sin(a) * (40 + r() * 70); a += (r() - 0.5) * 0.8; d += `L${f1(x)},${f1(y)}`; } cr += `<path d="${d}" stroke="#f4fbff" stroke-width="4" fill="none" opacity=".95"/><path d="${d}" stroke="#5a7a8a" stroke-width="1.5" fill="none" opacity=".6"/>`; }
      cr += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="30" fill="none" stroke="#f4fbff" stroke-width="3" opacity=".9"/>`;
    }
    s += `<g id="${id}-crack" opacity="0">${cr}</g>`;
    let sh = "";
    for (let k = 0; k < 46; k++) {
      const x = 400 + r() * 1300, y = 360 + r() * 980, w = 30 + r() * 70, h = 40 + r() * 90;
      sh += `<g class="qkShard" data-x="${f1(x)}" data-y="${f1(y)}"><path d="M${f1(x)},${f1(y)}l${f1(w)},${f1(h * 0.3)}l${f1(-w * 0.6)},${f1(h)}Z" fill="#e4f6fc" opacity=".75" stroke="#9cc4d4" stroke-width="2"/></g>`;
    }
    s += `<g id="${id}-shards" opacity="0">${sh}</g>`;

    // linen drapes on tie-backs over sheers, the rod with rings and finials (each side sways as #id-curL / #id-curR)
    const drape = (side) => {
      const M = (x) => f1(side < 0 ? x : 2100 - x);
      let c = `<path d="M${M(330)},328C${M(345)},700 ${M(360)},900 ${M(392)},1000C${M(380)},1150 ${M(350)},1300 ${M(340)},1376H${M(570)}C${M(548)},1300 ${M(486)},1150 ${M(436)},1000C${M(504)},900 ${M(566)},700 ${M(590)},328Z" fill="url(#qkSheer)"/>`;
      for (let i = 0; i < 6; i++) { const a = 335 + i * 45, b = 395 + i * 7, e = 345 + i * 40; c += `<path d="M${M(a)},328C${M(a)},700 ${M(b)},900 ${M(b)},1000C${M(b)},1150 ${M(e)},1300 ${M(e)},1376" stroke="#fff" stroke-width="10" fill="none" opacity=".3"/>`; }
      const shape = `M${M(240)},328C${M(250)},600 ${M(282)},820 ${M(270)},986C${M(252)},1150 ${M(236)},1300 ${M(234)},1378H${M(456)}C${M(452)},1300 ${M(420)},1150 ${M(396)},986C${M(420)},820 ${M(472)},600 ${M(474)},328Z`;
      const cid = `${id}-dr${side < 0 ? "L" : "R"}`;
      c += `<defs><clipPath id="${cid}"><path d="${shape}"/></clipPath></defs><path d="${shape}" fill="url(#qkLinen)" ${OUT3}/><g clip-path="url(#${cid})">`;
      for (let i = 0; i <= 8; i++) { const a = 240 + i * 29.25, b = 270 + i * 15.75, e = 234 + i * 27.75; c += `<path d="M${M(a)},328C${M(a)},600 ${M(b)},820 ${M(b)},986C${M(b)},1150 ${M(e)},1300 ${M(e)},1378" stroke="${i % 2 ? "#5a4a36" : "#fff"}" stroke-width="${i % 2 ? 12 : 16}" fill="none" opacity="${i % 2 ? 0.16 : 0.22}"/>`; }
      c += `<rect x="0" y="1352" width="2100" height="30" fill="#7a6a54" opacity=".35"/><rect x="0" y="328" width="2100" height="40" fill="url(#qkAOdn)"/></g>`;
      c += `<path d="M${M(262)},978Q${M(333)},1004 ${M(404)},978" stroke="#8a6a3a" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M${M(262)},976Q${M(333)},998 ${M(404)},976" stroke="#d8b878" stroke-width="3" fill="none" opacity=".8"/><path d="M${M(262)},980v40" stroke="#8a6a3a" stroke-width="4"/><path d="M${M(254)},1018h16l-2,38h-12z" fill="#b08a4a" ${OUT2}/>`;
      for (let x = 246; x <= 470; x += 28) c += `<ellipse cx="${M(x)}" cy="326" rx="8" ry="5" fill="none" stroke="#5a4e44" stroke-width="3"/>`;
      return `<g id="${id}-cur${side < 0 ? "L" : "R"}" data-o="${side < 0 ? 357 : 1743} 326">${A && side < 0 ? `<g transform="rotate(3 200 324)">${c}</g>` : c}</g>`;
    };
    s += drape(-1) + drape(1);
    s += `<rect x="196" y="318" width="1708" height="11" rx="5" fill="#4a4038" ${OUT2}/><path d="M200,320H1900" stroke="#9a8a7a" stroke-width="2" opacity=".8"/>${[196, 1904].map((x) => `<circle cx="${x}" cy="323" r="13" fill="#4a4038" ${OUT2}/><circle cx="${x - 4}" cy="319" r="4" fill="#fff" opacity=".4"/>`).join("")}`;

    // the oak floor: boards running to the vanishing point, their seams, end joints and grain
    const TONES = ["#c99a66", "#d2a571", "#c4935f", "#cd9f6a", "#bf8e5b", "#d6aa76", "#c6965f"];
    let seams = "", joints = "", gr = "";
    for (let X = -13; X < 10; X += 0.2) {
      s += hq(X, X + 0.2, 1.15, ZW, 0, `fill="${TONES[Math.floor(r() * TONES.length)]}"`);
      seams += ln(R(X, 0, ZW), R(X, 0, 1.15));
      let z = ZW - r() * 1.8; while (z > 1.2) { joints += ln(R(X, 0, z), R(X + 0.2, 0, z)); z -= 1.2 + r() * 1.3; }
      for (const f of [0.28, 0.66]) if (r() < 0.85) gr += ln(R(X + 0.2 * f, 0, ZW - r() * 0.6), R(X + 0.2 * f, 0, 1.2 + r() * 1.5));
    }
    s += `<path d="${seams}" stroke="#7a5230" stroke-width="2" opacity=".42"/><path d="${joints}" stroke="#6a4626" stroke-width="2.2" opacity=".5"/><path d="${gr}" stroke="#7e532e" stroke-width="1.5" opacity=".2" stroke-dasharray="60 24 120 40"/>`;
    // the window mirrored softly in the varnish, AO along the wall
    for (let k = 0; k < 4; k++) s += `<path d="M${392 + k * 335},${GB + 6}H${703 + k * 335}L${703 + k * 335 + (703 + k * 335 - 1050) * 0.5},${GB + 380}H${392 + k * 335 + (392 + k * 335 - 1050) * 0.5}Z" fill="url(#qkReflect)" opacity=".7"/>`;
    s += `<rect x="-2400" y="${GB}" width="6000" height="46" fill="url(#qkAOdn)"/>`;

    // the rug under the table: rust border with a navy line, cream field with a lattice, diamonds on the border, fringe
    {
      const X0 = -2.3, X1 = 2.3, Z0 = 3.3, Z1 = 5.5, Y = 0.012;
      let rg = vq(X0, X1, 0, Y, Z0, `fill="#7a3a26"`) + hq(X0, X1, Z0, Z1, Y, `fill="#b4603f"`);
      rg += hq(X0 + 0.24, X1 - 0.24, Z0 + 0.24, Z1 - 0.24, Y, `fill="#ece2cc"`);
      for (const [i, c, w] of [[0.06, "#2f4858", 3], [0.19, "#2f4858", 2], [0.3, "#c47a56", 3]]) rg += hq(X0 + i, X1 - i, Z0 + i, Z1 - i, Y, `fill="none" stroke="${c}" stroke-width="${w}"`);
      let lat = "";
      const xa = X0 + 0.36, xb = X1 - 0.36, za = Z0 + 0.36, zb = Z1 - 0.36;
      for (let c = xa - zb; c <= xb - za; c += 0.34) { const z0 = Math.max(za, xa - c), z1 = Math.min(zb, xb - c); if (z1 > z0) lat += ln(R(z0 + c, Y, z0), R(z1 + c, Y, z1)); }
      for (let c = xa + za; c <= xb + zb; c += 0.34) { const z0 = Math.max(za, c - xb), z1 = Math.min(zb, c - xa); if (z1 > z0) lat += ln(R(c - z0, Y, z0), R(c - z1, Y, z1)); }
      rg += `<path d="${lat}" stroke="#c47a56" stroke-width="2" opacity=".42"/>`;
      const dia = (X, Z) => poly([R(X - 0.055, Y, Z), R(X, Y, Z - 0.055), R(X + 0.055, Y, Z), R(X, Y, Z + 0.055)], `fill="#efe4cc"`);
      for (let X = X0 + 0.25; X <= X1 - 0.2; X += 0.3) rg += dia(X, Z0 + 0.125) + dia(X, Z1 - 0.125);
      for (let Z = Z0 + 0.4; Z <= Z1 - 0.3; Z += 0.3) rg += dia(X0 + 0.125, Z) + dia(X1 - 0.125, Z);
      let fr = ""; for (let X = X0 + 0.02; X < X1; X += 0.045) { fr += ln(R(X, 0.006, Z0), R(X + 0.006, 0, Z0 - 0.075)); fr += ln(R(X, 0.006, Z1), R(X + 0.006, 0, Z1 + 0.06)); }
      rg += `<path d="${fr}" stroke="#f2ead8" stroke-width="2.4" stroke-linecap="round"/>`;
      s += rg;
    }

    // the sun's patch through the panes (light from the upper right, behind the glass), and what stands in it casts a shadow
    const LD = [-0.45, -0.72, -0.5], hit = (X, Y, Z) => { const t = Y / -LD[1]; return [X + LD[0] * t, 0.02, Z + LD[2] * t]; };
    const patch = [];
    for (let k = 0; k < 4; k++) {
      const xa = ((392 + k * 335 + (k ? 10 : 0)) - VPX) * 6.12 / FOC, xb = ((703 + k * 335 - (k < 3 ? 10 : 0)) - VPX) * 6.12 / FOC;
      for (const [ya, yb] of [[0.08, 2.4], [2.5, 4.15]]) patch.push([hit(xa, ya, 6.12), hit(xb, ya, 6.12), hit(xb, yb, 6.12), hit(xa, yb, 6.12)].map((p) => R(p[0], p[1], p[2])));
    }
    if (!o.under) {
      s += `<defs><clipPath id="${id}-sun">${patch.map((q) => poly(q)).join("")}</clipPath></defs>`;
      s += `<g opacity="${A ? 0.75 : 1}">${patch.map((q) => poly(q, `fill="#fff3d2" opacity=".4"`)).join("")}</g>`;
    }

    // left wall: the fridge (magnets, the note), the microwave on it, the kitchen, the Buddha cabinet, the photo, the clock
    {
      let k = "";
      k += footShadow(-1270, -1090, 0.68) + wbox(-1270, 916, -1090, GB, 0.68, { front: "url(#qkFridgeG)", side: "#b8bec2", out: OUT3 });
      k += `<g transform="${WM(0.68)}"><path d="M-1270,1060H-1090" stroke="#9aa2a6" stroke-width="4"/>${brushed(-1266, 920, 172, 456, 41)}${handle(-1112, 950, 90, { t: 10 })}${handle(-1112, 1080, 150, { t: 10 })}
        <text x="-1180" y="1048" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="11" fill="#8a9296" letter-spacing="2">FROST</text>
        <g transform="translate(-1215,1110) rotate(-4)"><rect x="-34" y="-40" width="68" height="84" fill="#fbf8ee" ${OUT2}/><path d="M-26,-26h48M-26,-14h40M-26,-2h46M-26,10h30" stroke="#c8281e" stroke-width="3" opacity=".75"/><circle cy="-40" r="7" fill="#e8443a" ${OUT2}/></g>
        <g transform="translate(-1150,1200) rotate(5)"><rect x="-30" y="-24" width="60" height="48" fill="#fff" ${OUT2}/><circle cx="-8" cy="-2" r="9" fill="#e8b88e"/><circle cx="10" cy="4" r="7" fill="#c99068"/><circle cy="-24" r="5" fill="#3aa0e8" ${OUT2}/></g>
        <g transform="translate(-1200,1260) rotate(-3)"><rect x="-32" y="-22" width="64" height="46" fill="#fffbe6" ${OUT2}/><circle cx="16" cy="-8" r="7" fill="#f6c935"/><path d="M-20,12q10,-14 20,0" stroke="#d8312a" stroke-width="3" fill="none"/></g>
        <circle cx="-1140" cy="1000" r="7" fill="#f2c230" ${OUT2}/><circle cx="-1230" cy="980" r="6" fill="#4a8a5a" ${OUT2}/></g>`;
      k += wbox(-1258, 838, -1102, 916, 0.42, { front: "#2a2c30", side: "#1e2024", out: OUT2 }) + `<g transform="${WM(0.42)}"><rect x="-1250" y="846" width="110" height="62" rx="4" fill="#14161a" ${OUT2}/><path d="M-1244,852l40,0l-50,48" fill="#fff" opacity=".1"/><rect x="-1132" y="850" width="22" height="16" fill="#0a2a1a"/><text x="-1121" y="862" text-anchor="middle" font-family="Kanit" font-size="10" fill="#5aff8a">13:18</text>${knob(-1121, 884, 6, "#c8ccce")}</g>`;
      // the splash-back tiles, the upper cabinets with a light under them
      k += `<rect x="-1075" y="1003" width="620" height="151" fill="url(#qkTiles)" ${OUT2}/><rect x="-1075" y="1003" width="620" height="60" fill="#fff6d8" opacity=".35"/>`;
      k += `<g transform="translate(-700,1003)"><path d="M-260,40H40" stroke="#8a9096" stroke-width="5" stroke-linecap="round"/>${[-230, -170, -110, -50].map((x, i) => `<path d="M${x},40v${30 + (i % 2) * 12}" stroke="#6a6e72" stroke-width="3"/>` + (i % 2 ? `<ellipse cx="${x}" cy="${78}" rx="9" ry="12" fill="#8a9096" ${OUT2}/>` : `<rect x="${x - 7}" y="${70}" width="14" height="26" rx="3" fill="#b8bec2" ${OUT2}/>`)).join("")}</g>`;
      k += wbox(-1075, 828, -455, 1003, 0.36, { front: "url(#qkCab)", side: "#cfc5b4", out: OUT3 }) + `<g transform="${WM(0.36)}">${[-1075, -920, -765, -610].map((x) => `<rect x="${x + 6}" y="836" width="143" height="159" rx="3" fill="#f2ece2" ${OUT2}/><rect x="${x + 16}" y="846" width="123" height="139" fill="none" stroke="#d8cebe" stroke-width="2"/>`).join("")}${[-933, -778, -623, -468].map((x) => handle(x, 960, 26, { t: 7, dir: "v" })).join("")}<rect x="-1075" y="995" width="620" height="8" fill="#fff8d0"/></g>`;
      // the counter: base cabinets, the toe kick, the granite top
      k += footShadow(-1075, -455, 0.62, 0.7) + wbox(-1075, 1356, -455, GB, 0.56, { front: "#3a342c", side: "#2a241e", out: OUT2 });
      k += wbox(-1075, 1166, -455, 1356, 0.62, { front: "url(#qkCab)", side: "#cbbfac", out: OUT3 }) + `<g transform="${WM(0.62)}">${[-1075, -920, -765, -610].map((x) => `<rect x="${x + 6}" y="1172" width="143" height="44" rx="3" fill="#f0e9de" ${OUT2}/>${handle(x + 52, 1190, 50, { t: 7, dir: "h" })}<rect x="${x + 6}" y="1222" width="143" height="128" rx="3" fill="#f0e9de" ${OUT2}/>${handle(x + 52, 1236, 50, { t: 7, dir: "h" })}`).join("")}</g>`;
      k += wbox(-1080, 1152, -450, 1166, 0.65, { front: "url(#qkGranite)", side: "#2a2a2c", top: "#5a5b60", out: OUT2 });
      { let sp = ""; const q = mk(91); for (let i = 0; i < 70; i++) { const [x, y] = wf(-1080 + q() * 630, 1152 + q() * 14, 0.65); sp += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(0.8 + q() * 1.4)}" fill="${q() < 0.5 ? "#c8c8c8" : "#1a1a1a"}" opacity=".6"/>`; } k += sp; }
      { const [a, y] = wf(-1080, 1152, 0.65), [b] = wf(-450, 1152, 0.65); k += `<path d="M${f1(a)},${f1(y + 1)}H${f1(b)}" stroke="#b8b8bc" stroke-width="2" opacity=".8"/>`; }
      // on the counter (the props move together as #id-kprops): the stove, the canister, the kettle, the rice cooker, a bottle
      const CZ = 5.66, CY = 0.92, at = (X) => R(X, CY, CZ), sc = FOC / CZ;
      let kp = "";
      { const [x, y] = at(-7.75), w = 0.36 * sc, h = 0.11 * sc;
        kp += `<g id="${id}-stove"><g transform="${A ? `rotate(-8 ${f1(x)} ${f1(y)})` : "translate(0,0)"}"><path d="M${f1(x - w / 2)},${f1(y)}V${f1(y - h)}H${f1(x + w / 2)}V${f1(y)}Z" fill="#2a2a2c" ${OUT2}/><path d="M${f1(x - w / 2)},${f1(y - h)}L${f1(x - w / 2 + 6)},${f1(y - h - 8)}H${f1(x + w / 2 - 6)}L${f1(x + w / 2)},${f1(y - h)}Z" fill="#4a4a4e" ${OUT2}/>
          <ellipse cx="${f1(x - 6)}" cy="${f1(y - h - 6)}" rx="${f1(w * 0.28)}" ry="5" fill="none" stroke="#8a8a8e" stroke-width="3"/>${[-1, 0, 1].map((i) => `<path d="M${f1(x - 6 + i * w * 0.22)},${f1(y - h - 4)}v-10" stroke="#5a5a5e" stroke-width="3"/>`).join("")}
          ${knob(x + w * 0.36, y - h * 0.45, 7, "#d8d8d8")}<rect x="${f1(x - w * 0.42)}" y="${f1(y - h * 0.72)}" width="${f1(w * 0.5)}" height="6" fill="#d8312a"/>
          <path d="M${f1(x - w * 0.3)},${f1(y - h - 14)}h${f1(w * 0.5)}l-6,-28h${f1(-w * 0.5 + 12)}z" fill="#9aa0a6" ${OUT2}/><path d="M${f1(x - w * 0.3 - 4)},${f1(y - h - 40)}h${f1(w * 0.5 + 8)}" stroke="#7a8086" stroke-width="5" stroke-linecap="round"/><path d="M${f1(x + w * 0.24)},${f1(y - h - 34)}h22" stroke="#2a2a2c" stroke-width="6" stroke-linecap="round"/></g></g>`; }
      if (!A) { const [x, y] = at(-7.36), w = 0.075 * sc, h = 0.2 * sc;
        kp += `<g id="${id}-can"><rect x="${f1(x - w / 2)}" y="${f1(y - h)}" width="${f1(w)}" height="${f1(h)}" rx="5" fill="url(#qkPotG)" ${OUT2}/><rect x="${f1(x - w / 2)}" y="${f1(y - h * 0.72)}" width="${f1(w)}" height="${f1(h * 0.3)}" fill="#d8312a"/><path d="M${f1(x - w * 0.25)},${f1(y - h * 0.6)}h${f1(w * 0.5)}" stroke="#fff" stroke-width="2"/><path d="M${f1(x - 5)},${f1(y - h)}v-7h10v7" fill="#9aa0a4" ${OUT2}/></g>`; }
      { const [x, y] = at(-6.98), w = 0.17 * sc, h = 0.24 * sc;
        kp += `<path d="M${f1(x - w / 2)},${f1(y)}L${f1(x - w * 0.42)},${f1(y - h)}H${f1(x + w * 0.42)}L${f1(x + w / 2)},${f1(y)}Z" fill="#e8ecee" ${OUT2}/><path d="M${f1(x + w * 0.42)},${f1(y - h * 0.85)}q${f1(w * 0.45)},4 ${f1(w * 0.2)},${f1(h * 0.7)}" stroke="#2a2c30" stroke-width="5" fill="none"/><path d="M${f1(x - w * 0.42)},${f1(y - h * 0.8)}l-12,-6" stroke="#2a2c30" stroke-width="4"/><ellipse cx="${f1(x)}" cy="${f1(y - h)}" rx="${f1(w * 0.42)}" ry="4" fill="#2a2c30"/><path d="M${f1(x - w * 0.3)},${f1(y - h * 0.8)}V${f1(y - h * 0.15)}" stroke="#fff" stroke-width="3" opacity=".7"/>`; }
      { const [x, y] = at(-6.5), w = 0.3 * sc, h = 0.24 * sc;
        kp += `<path d="M${f1(x - w / 2)},${f1(y)}V${f1(y - h * 0.7)}Q${f1(x - w / 2)},${f1(y - h)} ${f1(x)},${f1(y - h)}Q${f1(x + w / 2)},${f1(y - h)} ${f1(x + w / 2)},${f1(y - h * 0.7)}V${f1(y)}Z" fill="#f8f6f0" ${OUT2}/><path d="M${f1(x - w / 2)},${f1(y - h * 0.62)}H${f1(x + w / 2)}" stroke="#c8c2b4" stroke-width="2"/>
          ${[0, 1, 2].map((i) => `<circle cx="${f1(x - w * 0.25 + i * w * 0.25)}" cy="${f1(y - h * 0.32)}" r="5" fill="${["#e88aa0", "#f2c230", "#e88aa0"][i]}"/>`).join("")}<rect x="${f1(x - 10)}" y="${f1(y - h * 0.55)}" width="20" height="10" rx="2" fill="#2a2c30"/><circle cx="${f1(x + 4)}" cy="${f1(y - h * 0.5)}" r="2" fill="${dark ? "#555" : "#ff6a3a"}"/><path d="M${f1(x - w * 0.36)},${f1(y - h * 0.9)}q${f1(w * 0.2)},-6 ${f1(w * 0.4)},-4" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/>`; }
      { const [x, y] = at(-6.2), w = 0.06 * sc, h = 0.26 * sc;
        kp += `<path d="M${f1(x - w / 2)},${f1(y)}V${f1(y - h * 0.62)}Q${f1(x - w / 2)},${f1(y - h * 0.78)} ${f1(x - 3)},${f1(y - h * 0.86)}V${f1(y - h)}H${f1(x + 3)}V${f1(y - h * 0.86)}Q${f1(x + w / 2)},${f1(y - h * 0.78)} ${f1(x + w / 2)},${f1(y - h * 0.62)}V${f1(y)}Z" fill="#8a3a1a" opacity=".9" ${OUT2}/><rect x="${f1(x - w / 2)}" y="${f1(y - h * 0.5)}" width="${f1(w)}" height="${f1(h * 0.24)}" fill="#f2e6c8"/><rect x="${f1(x - 4)}" y="${f1(y - h - 6)}" width="8" height="7" fill="#d8312a"/>`; }
      k += `<g id="${id}-kprops" data-o="${f1(at(-7)[0])} ${f1(at(-7)[1])}">${kp}</g>`;

      // the Buddha cabinet: teak, a carved drawer (#id-drawer), panelled doors; on top a red runner, the Buddha, two candles, garland,
      // vases with flowers, an incense bowl
      k += footShadow(-400, -40, 0.45, 0.7) + wbox(-400, 1104, -40, GB, 0.45, { front: "url(#qkTeak)", side: "#4a2412", top: "#9a5a34", out: OUT3 });
      k += `<g transform="${WM(0.45)}">${grain(-396, 1108, 352, 268, 12, { col: "#2a1206", op: 0.25 })}
        <g id="${id}-drawer"><rect x="-380" y="1124" width="320" height="64" rx="4" fill="#8a4c2a" ${OUT2}/><rect x="-370" y="1132" width="300" height="48" fill="none" stroke="#c89a4a" stroke-width="2" opacity=".7"/>${knob(-220, 1156, 8, "#e8c46a")}</g>
        ${[-380, -220].map((x) => `<rect x="${x}" y="1196" width="156" height="170" rx="4" fill="#7a4022" ${OUT2}/><rect x="${x + 14}" y="1210" width="128" height="142" rx="3" fill="none" stroke="#c89a4a" stroke-width="2" opacity=".6"/><path d="M${x + 78},1250l18,30l-18,30l-18,-30z" fill="none" stroke="#c89a4a" stroke-width="2" opacity=".6"/>${knob(x + (x < -300 ? 140 : 16), 1282, 6, "#e8c46a")}`).join("")}
        <path d="M-404,1104H-36" stroke="#c89a4a" stroke-width="4"/></g>`;
      { // the top (seen from above): runner, Buddha, candles, flowers, incense
        const TZ = 5.78, TY = 1.1, T = (X, dz = 0) => R(X, TY, TZ + dz), sc2 = FOC / TZ, cx = -5.07;
        const [rx0, ry0] = T(cx - 0.5, -0.12), [rx1] = T(cx + 0.5, -0.12);
        k += `<path d="M${f1(rx0)},${f1(ry0)}H${f1(rx1)}L${f1(rx1 + 4)},${f1(ry0 + 26)}H${f1(rx0 - 4)}Z" fill="#b8282a" ${OUT2}/><path d="M${f1(rx0)},${f1(ry0 + 22)}H${f1(rx1)}" stroke="#e8c46a" stroke-width="3"/>`;
        const [bx, by] = T(cx, 0.05), u = sc2 / 260;
        k += `<g transform="translate(${f1(bx)},${f1(by)}) scale(${f4(u)})"><path d="M-70,0H70L58,-30H-58Z" fill="url(#qkGoldG)" ${OUT2}/><path d="M-50,-30H50L40,-50H-40Z" fill="#c8961e" ${OUT2}/>
          <path d="M-44,-50Q-54,-120 -30,-140Q0,-150 30,-140Q54,-120 44,-50Z" fill="url(#qkGoldG)" ${OUT2}/><path d="M-30,-70Q0,-58 30,-70" stroke="#9a6a14" stroke-width="3" fill="none"/>
          <circle cy="-166" r="26" fill="url(#qkGoldG)" ${OUT2}/><path d="M0,-192q-8,-14 0,-30q8,16 0,30z" fill="url(#qkGoldG)" ${OUT2}/><circle cx="-8" cy="-174" r="7" fill="#fff" opacity=".5"/>
          <path d="M-90,-140Q-100,-210 0,-240Q100,-210 90,-140" fill="none" stroke="#e8b83a" stroke-width="5" opacity=".6"/></g>`;
        k += `<g id="${id}-candles">${[cx - 0.24, cx + 0.24].map((X) => { const [x, y] = T(X, 0.04), w = 0.03 * sc2, h = 0.17 * sc2; return `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w * 1.6)}" ry="4" fill="#c8961e" ${OUT2}/><rect x="${f1(x - w / 2)}" y="${f1(y - h)}" width="${f1(w)}" height="${f1(h)}" fill="#f6f0e0" ${OUT2}/><path d="M${f1(x)},${f1(y - h)}v-6" stroke="${INK}" stroke-width="2"/>`; }).join("")}</g>`;
        for (const X of [cx - 0.42, cx + 0.42]) { const [x, y] = T(X, 0.0), h = 0.15 * sc2; k += `<path d="M${f1(x - 9)},${f1(y)}L${f1(x - 6)},${f1(y - h)}H${f1(x + 6)}L${f1(x + 9)},${f1(y)}Z" fill="#e8d8a8" ${OUT2}/>` + [[-14, -h - 18, "#f6f2ea"], [10, -h - 22, "#f47b20"], [0, -h - 34, "#f2c230"], [-6, -h - 10, "#f6f2ea"]].map(([dx, dy, c]) => `<circle cx="${f1(x + dx)}" cy="${f1(y + dy)}" r="9" fill="${c}" ${OUT2}/>`).join("") + `<path d="M${f1(x)},${f1(y - h)}l-6,-18M${f1(x)},${f1(y - h)}l8,-16" stroke="#3e7a3a" stroke-width="3"/>`; }
        { const [x, y] = T(cx, -0.16); k += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="22" ry="8" fill="#c8961e" ${OUT2}/><path d="M${f1(x - 22)},${f1(y)}q22,22 44,0" fill="#a87418" ${OUT2}/>${[-8, 0, 8].map((dx) => `<path d="M${f1(x + dx)},${f1(y - 2)}l${dx / 3},-34" stroke="#8a2a1a" stroke-width="2.4"/>`).join("")}`; }
        // the garland draped over the front edge
        const [gx0, gy0] = T(cx - 0.36, -0.2), [gx1] = T(cx + 0.36, -0.2);
        let gd = ""; for (let t = 0; t <= 1.001; t += 1 / 14) { const x = gx0 + (gx1 - gx0) * t, y = gy0 + 6 + Math.sin(Math.PI * t) * 26; gd += `<circle cx="${f1(x)}" cy="${f1(y)}" r="6" fill="${Math.round(t * 14) % 3 ? "#f8f6ee" : "#f47b20"}" stroke="#8a7a5a" stroke-width="1"/>`; }
        k += gd + `<path d="M${f1((gx0 + gx1) / 2)},${f1(gy0 + 32)}v30" stroke="#e8443a" stroke-width="4"/><circle cx="${f1((gx0 + gx1) / 2)}" cy="${f1(gy0 + 66)}" r="7" fill="#e8443a" ${OUT2}/>`;
      }
      // the family photo (swings on its nail) and the clock
      k += `${A ? `<rect x="46" y="848" width="108" height="136" fill="#f9f4ea" opacity=".8"/><circle cx="100" cy="812" r="4" fill="#5a5048"/>` : `<g id="${id}-photo" data-o="100 812"><path d="M100,812L54,846M100,812L146,846" stroke="#5a5048" stroke-width="2"/><circle cx="100" cy="812" r="4" fill="#5a5048"/>
        <rect x="44" y="846" width="112" height="140" fill="#3a2a1c" ${OUT2}/><rect x="54" y="856" width="92" height="120" fill="#f8f4ea"/><rect x="62" y="864" width="76" height="98" fill="#bcd8e6"/>
        <circle cx="86" cy="900" r="13" fill="#e8b88e"/><path d="M70,962q16,-44 32,0" fill="#e8682a"/><circle cx="114" cy="914" r="10" fill="#e8b88e"/><path d="M102,962q12,-34 24,0" fill="#f2c230"/><path d="M76,890q10,-12 22,0" stroke="#24170f" stroke-width="7" fill="none"/>
        <path d="M66,868l24,0l-30,40z" fill="#fff" opacity=".35"/></g>`}`;
      const ca = A ? 7 : 0;
      k += `<g id="${id}-clock" data-o="100 700"><g transform="rotate(${ca} 100 700)"><circle cx="104" cy="706" r="52" fill="#000" opacity=".14"/><circle cx="100" cy="700" r="52" fill="#3a3a3c" ${OUT2}/><circle cx="100" cy="700" r="45" fill="#fbf8ee"/>${Array.from({ length: 12 }, (_, i) => { const a = (i / 12) * Math.PI * 2; return `<path d="M${f1(100 + Math.sin(a) * 36)},${f1(700 - Math.cos(a) * 36)}L${f1(100 + Math.sin(a) * 41)},${f1(700 - Math.cos(a) * 41)}" stroke="${INK}" stroke-width="${i % 3 ? 2 : 4}"/>`; }).join("")}
        <g id="${id}-cH"><path d="M100,700L${f1(100 + Math.sin(((1 + 20 / 60) / 12) * Math.PI * 2) * 22)},${f1(700 - Math.cos(((1 + 20 / 60) / 12) * Math.PI * 2) * 22)}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/></g>
        <g id="${id}-cM"><path d="M100,700V666" stroke="${INK}" stroke-width="3" stroke-linecap="round" transform="rotate(${(o.min ?? 18) * 6} 100 700)"/></g><circle cx="100" cy="700" r="4" fill="${INK}"/><path d="M70,676a40,40 0 0 1 30,-20" stroke="#fff" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/></g></g>`;
      // a light switch and the intercom by the curtain
      k += `<rect x="190" y="1000" width="34" height="54" rx="4" fill="#f8f6f0" stroke="#b8ae9e" stroke-width="2"/><rect x="198" y="1010" width="18" height="16" rx="2" fill="#e8e4dc" stroke="#a8a090" stroke-width="1.5"/><rect x="198" y="1030" width="18" height="16" rx="2" fill="#e8e4dc" stroke="#a8a090" stroke-width="1.5"/>`;
      s += k;
    }

    // right wall: the print, the air conditioner, the bookshelf with its books, the aquarium
    {
      let k = "";
      if (!A) k += `<g id="${id}-photo2" data-o="2320 830"><path d="M2320,830L2250,850M2320,830L2390,850" stroke="#5a5048" stroke-width="2"/><rect x="2245" y="846" width="150" height="114" fill="#f4efe4" ${OUT2}/><rect x="2257" y="858" width="126" height="90" fill="#e8d4b0"/><circle cx="2350" cy="884" r="14" fill="#e8822a"/><path d="M2257,948l38,-44l30,30l20,-18l38,32z" fill="#6a9a8a"/><path d="M2257,948l38,-44l12,12" fill="none" stroke="#4a7a6a" stroke-width="2"/></g>`;
      k += wbox(1890, 692, 2120, 760, 0.24, { front: "url(#qkACG)", side: "#c8c8c2", bottom: "#b8b8b2", out: OUT2 }) + `<g transform="${WM(0.24)}"><path d="M1900,740H2110" stroke="#b8b8b2" stroke-width="3"/><path d="M1904,748H2106" stroke="#9a9a94" stroke-width="4"/><circle cx="2090" cy="712" r="3" fill="${dark ? "#888" : "#4ac8ff"}"/><text x="1920" y="716" font-family="Kanit" font-size="10" font-weight="700" fill="#9a9a94" letter-spacing="2">COOL</text></g>`;
      // bookshelf (topples in the aftermath)
      let sf = footShadow(1880, 2110, 0.35, 0.7) + wbox(1880, 878, 2110, GB, 0.35, { front: "#a87048", side: "#7a4a2a", out: OUT3 });
      sf += `<g transform="${WM(0.35)}">${grain(1884, 882, 222, 494, 55, { col: "#4a2a12", op: 0.2, dir: "v" })}`;
      let bk = "";
      const rb = mk(66);
      for (let i = 0; i < 5; i++) {
        const y0 = 890 + i * 97, y1 = y0 + 84;
        sf += `<rect x="1894" y="${y0}" width="202" height="${y1 - y0}" fill="#5e3a20"/><rect x="1894" y="${y0}" width="202" height="16" fill="url(#qkAOdn)"/><rect x="1888" y="${y1}" width="214" height="13" fill="#b8804e" ${OUT2}/><path d="M1890,${y1 + 2}H2100" stroke="#e0b080" stroke-width="2"/>`;
        let x = 1898;
        while (x < 2088) {
          const kind = rb();
          if (kind < 0.1 && x < 2040) { // a lying stack
            for (let j = 0; j < 3; j++) bk += `<rect x="${f1(x)}" y="${f1(y1 - 10 - j * 10)}" width="${f1(46 - j * 4)}" height="10" fill="${BOOKC[Math.floor(rb() * BOOKC.length)]}" stroke="${INK}" stroke-width="1.4"/>`;
            if (i === 2) bk += pot(x + 22, y1 - 30, 13, 16) + leaves(x + 22, y1 - 46, 6, 26, 60, 77, { w: 0.4 });
            x += 50;
          } else if (kind < 0.16 && x < 2060 && i === 0) { bk += `<rect x="${f1(x)}" y="${y1 - 50}" width="34" height="50" fill="#f4efe4" ${OUT2}/><rect x="${f1(x + 5)}" y="${y1 - 44}" width="24" height="38" fill="#9ac0d8"/><circle cx="${f1(x + 17)}" cy="${y1 - 30}" r="6" fill="#e8b88e"/>`; x += 38; }
          else if (kind < 0.22 && x < 2060 && i === 4) { bk += `<ellipse cx="${f1(x + 16)}" cy="${y1 - 18}" rx="16" ry="18" fill="#f4a0b4" ${OUT2}/><circle cx="${f1(x + 26)}" cy="${y1 - 24}" r="3" fill="${INK}"/><path d="M${f1(x + 4)},${y1 - 32}l4,-8l6,6" fill="#f4a0b4" ${OUT2}/>`; x += 36; }
          else {
            const w = 12 + rb() * 12, h = 52 + rb() * 28, c = BOOKC[Math.floor(rb() * BOOKC.length)];
            const fall = rb() < 0.22 && i < 3;
            const bb = book(x, y1, w, h, c, rb, x > 2070 && rb() < 0.5 ? -8 : 0);
            bk += fall ? `<g class="qkBook" data-x="${f1(x + w / 2)}" data-y="${y1}">${bb}</g>` : bb;
            x += w + 1;
          }
        }
      }
      sf += `<g id="${id}-books">${bk}</g></g>`;
      k += A ? `<g transform="rotate(80 ${f1(wf(2110, GB, 0.35)[0])} ${f1(wf(2110, GB, 0.35)[1])})">${sf}</g>` : `<g id="${id}-shelf">${sf}</g>`;
      // aquarium cabinet and tank
      k += footShadow(2170, 2470, 0.42, 0.7) + wbox(2170, 1192, 2470, GB, 0.42, { front: "#2e3034", side: "#1e2024", top: "#4a4c50", out: OUT3 }) + `<g transform="${WM(0.42)}"><rect x="2180" y="1204" width="136" height="164" rx="3" fill="#36383c" ${OUT2}/><rect x="2324" y="1204" width="136" height="164" rx="3" fill="#36383c" ${OUT2}/>${handle(2302, 1260, 40, { t: 6, dir: "v" })}${handle(2330, 1260, 40, { t: 6, dir: "v" })}</g>`;
      const tank = `<g id="${id}-tank">${wbox(2180, 1066, 2460, 1080, 0.38, { front: "#2a2c30", side: "#1a1c20", out: OUT2 })}<g transform="${WM(0.38)}">
          <rect x="2182" y="1080" width="276" height="112" fill="#d8f2f8" opacity=".3" ${OUT2}/>
          <defs><clipPath id="${id}-aqc"><rect x="2185" y="1083" width="270" height="106"/></clipPath></defs>
          <g clip-path="url(#${id}-aqc)"><g id="${id}-aqw"><path d="M2120,${A ? 1120 : 1094}Q2230,${A ? 1112 : 1086} 2320,${A ? 1120 : 1094}T2520,${A ? 1120 : 1094}V1200H2120Z" fill="url(#qkAq)"/></g>
            <path d="M2185,1189Q2260,1176 2320,1182T2455,1178V1192H2185Z" fill="#d8c8a0"/>${Array.from({ length: 16 }, (_, i) => `<circle cx="${2190 + i * 17}" cy="${1186 - (i % 3) * 2}" r="3" fill="${["#c8b890", "#a89870", "#e8dcc0"][i % 3]}"/>`).join("")}
            <path d="M2210,1186q8,-40 -4,-80M2230,1186q-6,-34 8,-64M2420,1186q8,-30 -4,-60M2436,1186q-4,-26 6,-46" stroke="#3e8a4a" stroke-width="6" fill="none" stroke-linecap="round"/>
            <path d="M2350,1188l10,-30h24l10,30z" fill="#8a8a92" ${OUT2}/><rect x="2362" y="1170" width="8" height="10" fill="#2a2a2e"/>
            ${[0, 1, 2, 3, 4].map((i) => `<circle cx="${2286 + (i % 2) * 4}" cy="${1176 - i * 16}" r="${2 + i * 0.5}" fill="none" stroke="#f4fcff" stroke-width="1.5" opacity=".8"/>`).join("")}
            <g id="${id}-fish"><path d="M2280,1130q22,-14 42,0q-20,14 -42,0zM2322,1130l14,-10v20z" fill="#f47b20" ${OUT2}/><circle cx="2290" cy="1128" r="2" fill="${INK}"/><path d="M2380,1150q18,-10 34,0q-16,10 -34,0zM2414,1150l11,-8v16z" fill="#e8c43a" ${OUT2}/></g></g>
          <path d="M2192,1084L2230,1188" stroke="#fff" stroke-width="10" opacity=".22"/>${A ? `<path d="M2240,1090l30,40l-14,30l34,30" stroke="#fff" stroke-width="3" fill="none"/>` : ""}</g></g>`;
      k += tank;
      if (A) { const [ax, ay] = wf(2320, GB, 0.42); k += `<ellipse cx="${f1(ax - 40)}" cy="${f1(ay + 40)}" rx="260" ry="46" fill="#9adcf0" opacity=".45"/><ellipse cx="${f1(ax - 70)}" cy="${f1(ay + 36)}" rx="120" ry="16" fill="#fff" opacity=".35"/>`; }
      s += k;
    }

    // the monstera in front of the left drape, the side table and floor lamp in front of the right one
    {
      const [px, py] = R(-3.02, 0, 5.55), sc = FOC / 5.55;
      const pl = pot(px, py, 0.2 * sc, 0.38 * sc) + leaves(px, py - 0.38 * sc, 9, 0.95 * sc, 75, 401, { w: 0.42, split: true, cols: ["#3e8a44", "#2f7a3a", "#4a9a4e"] }) + leaves(px - 10, py - 0.38 * sc, 4, 0.7 * sc, 40, 402, { w: 0.45, split: true, a0: -20 });
      s += `<g id="${id}-plant" data-o="${f1(px)} ${f1(py)}">${A ? `<g transform="rotate(64 ${f1(px + 30)} ${f1(py)})">${pl}</g><path d="M${f1(px + 20)},${f1(py + 8)}q40,-14 90,-4q30,8 60,2" stroke="#4a3424" stroke-width="10" fill="none" stroke-linecap="round"/>` : pl}</g>`;
      const [tx, ty] = R(2.3, 0, 5.25), st = FOC / 5.25, [ttx, tty] = R(2.3, 0.55, 5.25);
      s += cs(tx, ty + 3, 0.3 * st, 0.06 * st, 0.8) + `<path d="M${f1(tx)},${f1(ty)}V${f1(tty)}" stroke="#3a3632" stroke-width="7"/><ellipse cx="${f1(tx)}" cy="${f1(ty)}" rx="${f1(0.14 * st)}" ry="${f1(0.025 * st)}" fill="#3a3632" ${OUT2}/>
        <ellipse cx="${f1(ttx)}" cy="${f1(tty + 5)}" rx="${f1(0.24 * st)}" ry="${f1(0.06 * st)}" fill="#7a4a2a" ${OUT2}/><ellipse cx="${f1(ttx)}" cy="${f1(tty)}" rx="${f1(0.24 * st)}" ry="${f1(0.06 * st)}" fill="#c48c58" ${OUT2}/>
        <rect x="${f1(ttx - 34)}" y="${f1(tty - 14)}" width="60" height="9" fill="#3a6a9a" ${OUT2}/><rect x="${f1(ttx - 30)}" y="${f1(tty - 22)}" width="54" height="8" fill="#e8b83a" ${OUT2}/>${pot(ttx + 24, tty - 4, 12, 16)}<path d="M${f1(ttx + 24)},${f1(tty - 20)}v-22" stroke="#4a8a4a" stroke-width="9" stroke-linecap="round"/>`;
      const [lx, ly] = R(2.78, 0, 5.6), sl = FOC / 5.6, [, lt] = R(2.78, 1.58, 5.6);
      s += `<g id="${id}-flamp" data-o="${f1(lx)} ${f1(ly)}">${cs(lx, ly + 2, 0.2 * sl, 0.04 * sl, 0.8)}<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="${f1(0.15 * sl)}" ry="${f1(0.03 * sl)}" fill="#2a2a2c" ${OUT2}/><path d="M${f1(lx)},${f1(ly)}V${f1(lt + 0.2 * sl)}" stroke="#2a2a2c" stroke-width="5"/>
        <path d="M${f1(lx - 0.17 * sl)},${f1(lt + 0.22 * sl)}L${f1(lx - 0.13 * sl)},${f1(lt)}H${f1(lx + 0.13 * sl)}L${f1(lx + 0.17 * sl)},${f1(lt + 0.22 * sl)}Z" fill="${dark ? "#e6dccb" : "#fff4dc"}" ${OUT2}/><path d="M${f1(lx - 0.12 * sl)},${f1(lt + 4)}V${f1(lt + 0.2 * sl)}" stroke="#fff" stroke-width="4" opacity=".7"/></g>`;
      if (!dark) gl += `<ellipse cx="${f1(lx)}" cy="${f1(lt + 0.1 * sl)}" rx="${f1(0.5 * sl)}" ry="${f1(0.45 * sl)}" fill="url(#qkPoolW)" opacity=".55"/>`;
    }

    // a coat stand behind the table, by the window: the red emergency bag (a torch clipped on) and the school bag hang on its hooks
    if (o.frame === "door") { const [x, y] = R(0.75, 0, 5.1), u = FOC / 5.1, [, yt] = R(0.75, 1.78, 5.1);
        s += `<g id="${id}-hooks">${cs(x, y + 3, 0.26 * u, 0.04 * u, 0.85)}<path d="M${f1(x - 0.2 * u)},${f1(y)}L${f1(x)},${f1(y - 0.12 * u)}L${f1(x + 0.2 * u)},${f1(y)}M${f1(x - 0.06 * u)},${f1(y + 4)}L${f1(x)},${f1(y - 0.12 * u)}" stroke="#4a2e1a" stroke-width="9" stroke-linecap="round" fill="none"/>
          <rect x="${f1(x - 7)}" y="${f1(yt)}" width="14" height="${f1(y - yt - 0.1 * u)}" rx="6" fill="url(#qkLegW)" ${OUT2}/><circle cx="${f1(x)}" cy="${f1(yt - 6)}" r="11" fill="#8a5634" ${OUT2}/>
          ${[[-1, 0.06], [1, 0.1]].map(([d, dy]) => `<path d="M${f1(x)},${f1(yt + dy * u)}q${f1(d * 0.1 * u)},-6 ${f1(d * 0.12 * u)},-26" stroke="#8a5634" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}
          <g transform="translate(${f1(x - 0.08 * u)},${f1(yt + 0.03 * u)}) scale(${f4(u / 520)})"><path d="M-50,10Q-60,120 -54,220H54Q60,120 50,10Q0,-6 -50,10Z" fill="#c8312a" ${OUT3}/><path d="M-50,10Q-60,120 -54,220H-30Q-38,120 -28,8Z" fill="#000" opacity=".15"/><path d="M-40,10Q0,-60 40,10" stroke="#1e1e1e" stroke-width="7" fill="none"/>
            <rect x="-34" y="60" width="68" height="60" rx="6" fill="#fff" opacity=".9"/><path d="M-12,90h24M0,78v24" stroke="#c8312a" stroke-width="8"/><path d="M-40,40Q-20,26 10,30" stroke="#fff" stroke-width="5" opacity=".35" fill="none"/>
            <g transform="translate(40,140) rotate(-20)"><rect x="-10" y="-40" width="20" height="56" rx="5" fill="#2a2a2c" ${OUT3}/><rect x="-14" y="-52" width="28" height="16" rx="4" fill="#f2c230" ${OUT3}/></g></g>
          <g transform="translate(${f1(x + 0.12 * u)},${f1(yt + 0.07 * u)}) scale(${f4(u / 560)})"><path d="M-40,10Q-50,110 -44,200H44Q50,110 40,10Q0,-4 -40,10Z" fill="#8a6ac8" ${OUT3}/><path d="M-30,10Q0,-50 30,10" stroke="#5a4a8a" stroke-width="6" fill="none"/><rect x="-30" y="110" width="60" height="50" rx="6" fill="#a88ae0" ${OUT3}/></g></g>`; }
    // the chairs at the ends of the table (each faces the table; the back on the outer side)
    const chair = (cx, face, cid, over) => {
      const D = 0.44, W = 0.44, SY = 0.46, BY = 0.98, cz = 4.44, x0 = cx - D / 2, x1 = cx + D / 2, z0 = cz - W / 2, z1 = cz + W / 2, bx = face > 0 ? x0 : x1 - 0.045;
      let c = "";
      const leg = (lx, lz, h = SY) => box3(lx - 0.022, lx + 0.022, 0, h, lz - 0.022, lz + 0.022, { front: "url(#qkLegW)", side: "#5e3418" });
      c += cs(...R(cx, 0, cz), (FOC * 0.36) / cz, (FOC * 0.36 * EYE) / (cz * cz) * 0.5, 0.75);
      c += leg(face > 0 ? x0 + 0.03 : x1 - 0.03, z1 - 0.03, BY) + leg(face > 0 ? x1 - 0.03 : x0 + 0.03, z1 - 0.03);
      c += box3(bx, bx + 0.045, BY - 0.12, BY, z0 + 0.03, z1 - 0.03, { front: "#9a6438", side: "#7a4a2a", top: "#b07a4c" });
      c += box3(bx, bx + 0.045, BY - 0.3, BY - 0.24, z0 + 0.03, z1 - 0.03, { front: "#9a6438", side: "#7a4a2a", top: "#b07a4c" });
      c += leg(face > 0 ? x0 + 0.03 : x1 - 0.03, z0 + 0.03, BY) + leg(face > 0 ? x1 - 0.03 : x0 + 0.03, z0 + 0.03);
      c += box3(x0, x1, SY - 0.04, SY, z0, z1, { top: "#b98250", front: "#8a5634", side: "#74462a" });
      { const a = R(x0 + 0.04, SY, z0 + 0.06), b = R(x1 - 0.04, SY, z1 - 0.1); c += `<path d="M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}" stroke="#e0b07a" stroke-width="3" opacity=".5"/>`; }
      if (over) { const [ox, oy] = R(cx, 0, cz); return `<g id="${cid}"><g transform="rotate(${face > 0 ? -78 : 78} ${f1(ox)} ${f1(oy)}) translate(0,8)">${c}</g></g>`; }
      return `<g id="${cid}" data-o="${f1(R(cx, 0, cz)[0])} ${f1(R(cx, 0, cz)[1])}">${c}</g>`;
    };
    if (!o.under) s += chair(-1.26, 1, `${id}-chL`, false) + chair(1.26, -1, `${id}-chR`, A);

    // the table, its shadow in the sun patch, what is on it
    s += `<g id="${id}-tbl"${o.under ? ' display="none"' : ""}>`;
    if (!o.under) {
      const sh2 = (X, Y, Z) => { const p = hit(X, Y, Z); return R(p[0], 0.02, p[2]); };
      s += `<g clip-path="url(#${id}-sun)" opacity=".7">${poly([sh2(-0.957, 0.75, 4.0), sh2(0.957, 0.75, 4.0), sh2(0.957, 0.75, 4.88), sh2(-0.957, 0.75, 4.88)], `fill="#3a2410" opacity=".3"`)}
        ${[[-0.9, 4.04], [0.9, 4.04], [-0.9, 4.84], [0.9, 4.84]].map(([X, Z]) => poly([R(X - 0.03, 0.02, Z), R(X + 0.03, 0.02, Z), sh2(X + 0.03, 0.75, Z), sh2(X - 0.03, 0.75, Z)], `fill="#3a2410" opacity=".3"`)).join("")}
        ${[-1.26, 1.26].map((cx) => poly([sh2(cx - 0.22, 0.46, 4.22), sh2(cx + 0.22, 0.46, 4.22), sh2(cx + 0.22, 0.46, 4.66), sh2(cx - 0.22, 0.46, 4.66)], `fill="#3a2410" opacity=".26"`)).join("")}</g>`;
    }
    s += Qk.table();
    // things on the table (they jitter in the quake as #id-tprops; the glass is #id-cup)
    let tp = "";
    const TY = 0.75, onT = (X, Z) => R(X, TY, Z);
    {
      // a rattan placemat under the glass
      const [mx, my] = onT(-0.43, 4.35), mrx = (FOC * 0.2) / 4.35, mry = ((FOC * (EYE - TY)) * 0.15) / (4.35 * 4.35);
      tp += `<ellipse cx="${f1(mx)}" cy="${f1(my)}" rx="${f1(mrx)}" ry="${f1(mry)}" fill="#d8b878" stroke="#9a7a3a" stroke-width="2"/><ellipse cx="${f1(mx)}" cy="${f1(my)}" rx="${f1(mrx * 0.72)}" ry="${f1(mry * 0.72)}" fill="none" stroke="#b8945a" stroke-width="2"/><ellipse cx="${f1(mx)}" cy="${f1(my)}" rx="${f1(mrx * 0.42)}" ry="${f1(mry * 0.42)}" fill="none" stroke="#b8945a" stroke-width="2"/>`;
      // มิว's phone lying face up
      tp += poly([onT(-0.8, 4.16), onT(-0.66, 4.16), onT(-0.66, 4.33), onT(-0.8, 4.33)], `fill="#1e2228" ${OUT2}`) + poly([onT(-0.79, 4.175), onT(-0.67, 4.175), onT(-0.67, 4.315), onT(-0.79, 4.315)], `fill="#3a5a8a"`);
      // the open exercise book, a pencil, crayons
      tp += poly([onT(0.1, 4.12), onT(0.3, 4.1), onT(0.3, 4.4), onT(0.1, 4.4)], `fill="#fbfaf4" ${OUT2}`) + poly([onT(0.3, 4.1), onT(0.5, 4.12), onT(0.5, 4.4), onT(0.3, 4.4)], `fill="#f4f2ea" ${OUT2}`);
      let bl = ""; for (let z = 4.16; z < 4.38; z += 0.035) { bl += ln(onT(0.12, z), onT(0.28, z)) + ln(onT(0.32, z), onT(0.48, z)); } tp += `<path d="${bl}" stroke="#9cc4dc" stroke-width="1.4"/>`;
      tp += poly([onT(0.18, 4.2), onT(0.21, 4.2), onT(0.42, 4.32), onT(0.39, 4.33)], `fill="#f2c230" ${OUT2}`);
      for (const [X, Z, c] of [[0.6, 4.18, "#e8443a"], [0.66, 4.2, "#3a7ad8"], [0.63, 4.26, "#4ab85a"]]) tp += poly([onT(X, Z), onT(X + 0.09, Z + 0.01), onT(X + 0.09, Z + 0.025), onT(X, Z + 0.015)], `fill="${c}" ${OUT2}`);
      // a tissue box and a small vase with a flower
      tp += box3(0.6, 0.8, TY, TY + 0.1, 4.56, 4.7, { top: "#f4f0e6", front: "#8ac8d8", side: "#6aa8b8" }) + (() => { const [x, y] = onT(0.7, 4.63); return `<path d="M${f1(x - 10)},${f1(y - 14)}q10,-26 22,-4q-4,6 -22,4z" fill="#fff" ${OUT2}/>`; })();
      { const [x, y] = onT(0.22, 4.74), h = (FOC * 0.14) / 4.74; tp += `<path d="M${f1(x - 8)},${f1(y)}Q${f1(x - 12)},${f1(y - h * 0.6)} ${f1(x - 4)},${f1(y - h)}H${f1(x + 4)}Q${f1(x + 12)},${f1(y - h * 0.6)} ${f1(x + 8)},${f1(y)}Z" fill="#cfe8ee" opacity=".8" ${OUT2}/><path d="M${f1(x)},${f1(y - h)}q4,-30 -2,-56" stroke="#3e7a3a" stroke-width="3" fill="none"/>${[0, 1, 2, 3, 4].map((i) => { const a = (i / 5) * Math.PI * 2; return `<ellipse cx="${f1(x - 2 + Math.cos(a) * 8)}" cy="${f1(y - h - 58 + Math.sin(a) * 6)}" rx="7" ry="5" fill="#f4a0c8" ${OUT2}/>`; }).join("")}<circle cx="${f1(x - 2)}" cy="${f1(y - h - 58)}" r="4" fill="#f2c230"/>`; }
    }
    if (o.bag) tp += `<g transform="translate(1210,1318)">${cs(0, 2, 90, 10, 0.8)}<rect x="-80" y="-120" width="160" height="120" rx="10" fill="#2fa45a" ${OUT3}/><rect x="-80" y="-120" width="160" height="26" rx="10" fill="#25874a"/><path d="M-60,-120q0,-34 60,-34q60,0 60,34" stroke="#1e1e1e" stroke-width="8" fill="none"/><circle cx="0" cy="-60" r="28" fill="#fff4dc" ${OUT3}/><path d="M-16,-62h32q-2,15 -16,17q-14,-2 -16,-17z" fill="#e2a92e"/></g>`;
    s += `<g id="${id}-tprops" data-o="1050 1320">${A ? `<g transform="translate(0,6)">${tp}</g>` : tp}</g>`;
    s += A ? `<g transform="translate(860,1330) rotate(-84)"><path d="M-26,-90L-20,0H20L26,-90Z" fill="#e8f6fa" opacity=".55" ${OUT3}/></g><ellipse cx="800" cy="1338" rx="90" ry="12" fill="#9adcf0" opacity=".5"/>`
      : `<g id="${id}-cup"><g transform="translate(900,1318)">${cs(0, 2, 34, 7, 0.7)}<path d="M-26,-90L-20,0H20L26,-90Z" fill="#e8f6fa" opacity=".55" ${OUT3}/><path d="M-24,-56L-20,0H20L24,-56Z" fill="#9adcf0" opacity=".7"/><ellipse cx="0" cy="-56" rx="24" ry="5" fill="#c8eef8" stroke="#7ab8c8" stroke-width="1.5"/><path d="M-16,-80V-10" stroke="#fff" stroke-width="5" opacity=".6"/><ellipse cx="0" cy="-90" rx="26" ry="5" fill="none" ${OUT2}/></g></g>`;
    if (A || o.lampDown) s += `<g transform="translate(1120,1312) rotate(-14)">${cs(10, 10, 130, 16, 0.6)}<path d="M-102,0Q-96,-80 0,-86Q96,-80 102,0Z" fill="url(#qkDome)" ${OUT3}/><ellipse cx="0" cy="0" rx="102" ry="12" fill="#c8a050" ${OUT2}/><path d="M-60,-62Q-20,-80 30,-78" stroke="#fff" stroke-width="5" opacity=".35" fill="none"/><path d="M0,-86V-200" stroke="#2a2a2a" stroke-width="4"/></g>`;
    s += `</g>`;

    // the aftermath on the floor: shards glinting, plaster from the ceiling, books, the photo face down, a chair over (drawn above)
    if (A) {
      let d = "";
      for (let i = 0; i < 90; i++) { const X = -2.6 + r() * 5.2, Z = 4.6 + r() * 1.4, [x, y] = R(X, 0.01, Z), w = 8 + r() * 26; d += `<path d="M${f1(x)},${f1(y)}l${f1(w)},${f1(-w * 0.18)}l${f1(-w * 0.5)},${f1(w * 0.32)}Z" fill="#e8f8fc" opacity=".85" stroke="#8ab4c4" stroke-width="1.4"/>`; }
      for (let i = 0; i < 26; i++) { const X = -2 + r() * 4.4, Z = 3.4 + r() * 2.4, [x, y] = R(X, 0.01, Z); d += `<path d="M${f1(x)},${f1(y)}l${f1(8 + r() * 24)},${f1(-4 - r() * 8)}l${f1(6 + r() * 10)},${f1(10 + r() * 8)}l${f1(-20 - r() * 20)},${f1(4)}Z" fill="#e8e2d6" ${OUT2}/>`; }
      for (let i = 0; i < 12; i++) { const [x, y] = R(2.2 + r() * 1.6, 0.01, 4.4 + r() * 1.4); d += `<rect x="${f1(x)}" y="${f1(y - 10)}" width="${f1(40 + r() * 30)}" height="${f1(12 + r() * 8)}" transform="rotate(${f1(r() * 60 - 30)} ${f1(x)} ${f1(y)})" fill="${BOOKC[Math.floor(r() * BOOKC.length)]}" stroke="${INK}" stroke-width="1.6"/>`; }
      { const [x, y] = R(-3.4, 0.01, 5.2); d += `<g transform="translate(${f1(x)},${f1(y)}) rotate(-12)"><rect x="-56" y="-14" width="112" height="22" fill="#3a2a1c" ${OUT2}/><path d="M-40,-10l20,14l16,-10l24,12" stroke="#cfe8f2" stroke-width="2" fill="none"/></g>`; }
      // a ceiling panel down with the hole above
      { const [hx, hy] = R(0.9, HC, 3.5); d += `<path d="M${f1(hx - 70)},${f1(hy - 30)}l140,-6l10,40l-150,8z" fill="#2a2420" opacity=".75"/>`; const [px, py] = R(1.3, 0.02, 3.9); d += `<g transform="translate(${f1(px)},${f1(py)}) rotate(9)"><path d="M-120,-10L110,-24L130,6L-100,22Z" fill="#efe9de" ${OUT3}/><path d="M-120,-10L-100,22" stroke="#bfb4a2" stroke-width="3"/></g>`; }
      s += d;
    }
    // the far-left floor stays bare; a school bag and slippers in the near foreground
    if (!o.under) {
      const [bx, by] = R(-1.25, 0, 2.75), bs = FOC / 2.75;
      s += `${cs(bx, by + 4, 0.34 * bs, 0.05 * bs, 0.8)}<g transform="translate(${f1(bx)},${f1(by)}) rotate(${A ? -16 : -6})"><path d="M${f1(-0.17 * bs)},0V${f1(-0.3 * bs)}Q${f1(-0.17 * bs)},${f1(-0.4 * bs)} 0,${f1(-0.4 * bs)}Q${f1(0.17 * bs)},${f1(-0.4 * bs)} ${f1(0.17 * bs)},${f1(-0.3 * bs)}V0Z" fill="#8a6ac8" ${OUT3}/><rect x="${f1(-0.12 * bs)}" y="${f1(-0.2 * bs)}" width="${f1(0.24 * bs)}" height="${f1(0.15 * bs)}" rx="10" fill="#a88ae0" ${OUT2}/><path d="M${f1(-0.1 * bs)},${f1(-0.13 * bs)}h${f1(0.2 * bs)}" stroke="#f2c230" stroke-width="4"/><path d="M${f1(-0.1 * bs)},${f1(-0.36 * bs)}q${f1(0.1 * bs)},-30 ${f1(0.2 * bs)},0" stroke="#5a4a8a" stroke-width="8" fill="none"/></g>`;
      for (const [X, Z, rot] of [[1.15, 2.95, 12], [1.38, 3.0, -8]]) { const [x, y] = R(X, 0, Z), u = FOC / Z; s += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot})"><ellipse cx="0" cy="0" rx="${f1(0.06 * u)}" ry="${f1(0.025 * u)}" fill="#f4a0b4" ${OUT2}/><path d="M${f1(-0.05 * u)},${f1(-0.004 * u)}q${f1(0.05 * u)},${f1(-0.04 * u)} ${f1(0.1 * u)},0" stroke="#e8708a" stroke-width="6" fill="none"/></g>`; }
    }
    put(L.set, s);

    // the pendant lamp (swings around Qk.lampPivot) and its light
    if (!A && !o.under && !o.lampDown) {
      put(L.set, `<g id="${id}-lamp"><ellipse cx="1050" cy="103" rx="34" ry="9" fill="#2a2a2c" ${OUT2}/><rect x="1040" y="103" width="20" height="10" fill="#2a2a2c"/><g id="${id}-lampCord"><path d="M1050,110V936" stroke="#1e1e20" stroke-width="4"/><path d="M1052,110V936" stroke="#6a6e72" stroke-width="1.2" opacity=".6"/></g>
        <rect x="1040" y="922" width="20" height="16" rx="4" fill="#c8a050" ${OUT2}/>
        <path d="M948,1008Q950,940 1050,934Q1150,940 1152,1008Z" fill="url(#qkDome)" ${OUT3}/><path d="M972,990Q990,950 1040,946" stroke="#fff" stroke-width="5" opacity=".35" fill="none" stroke-linecap="round"/>
        <ellipse cx="1050" cy="1008" rx="102" ry="12" fill="${dark ? "#8a7a5a" : "#fff2c8"}" stroke="#c8a050" stroke-width="5"/></g>`);
      if (!dark) put(L.glow, `<g id="${id}-lampGlow"><path d="M952,1010L800,1330H1300L1148,1010Z" fill="url(#qkCone)" opacity=".7"/><ellipse cx="1050" cy="1318" rx="250" ry="38" fill="url(#qkPoolW)" opacity=".75"/><ellipse cx="1050" cy="1012" rx="120" ry="34" fill="#fff6d0" opacity=".45"/></g>`);
    }
    if (gl) put(L.glow, gl);
    // gas shimmer over the fallen canister (the aftermath), the canister itself on the floor
    if (A) {
      put(L.set, `<g id="${id}-can" transform="translate(-690,1520) rotate(-70)">${cs(0, 0, 40, 10, 0.6)}<rect x="-26" y="-130" width="52" height="130" rx="12" fill="url(#qkPotG)" ${OUT3}/><rect x="-26" y="-96" width="52" height="40" fill="#d8312a"/><path d="M-14,-80h28" stroke="#fff" stroke-width="3"/><path d="M-10,-130V-148H10V-130" fill="#9aa0a4" ${OUT3}/></g>`);
      put(L.glow, `<g id="${id}-gas" opacity="0">${[0, 1, 2, 3, 4].map((k) => `<path class="qkGas" d="M${-690 + k * 26},1470q-30,-60 0,-120t0,-120t0,-120" stroke="#cfe8d0" stroke-width="${18 - k * 2}" fill="none" opacity=".22" stroke-linecap="round"/>`).join("")}</g>`);
    }
    // the corridor wall with the door frame around the doorway (we look in from outside 2714)
    if (o.frame === "door") {
      const DX0 = 700, DX1 = 1400, DT = 330, DB = 1700;
      put(L.set, `<g>${[[-0.44, 3.95, -6, 1], [-0.27, 3.93, 8, -1]].map(([X, Z, rot, fl]) => { const [x, y] = R(X, 0, Z), u = FOC / Z / 400; return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${f4(fl * u)},${f4(u)})">${cs(0, 2, 40, 7, 0.7)}
        <path d="M-36,0H30Q42,0 40,-10Q38,-18 26,-20L4,-26Q-8,-36 -24,-34Q-38,-32 -38,-16Z" fill="#f48aa6" ${OUT2}/><path d="M-38,-4H40" stroke="#fff" stroke-width="7"/><path d="M-38,0H38" stroke="#d8d2c8" stroke-width="2"/>
        <path d="M-28,-30Q-18,-36 -8,-30" stroke="#5a2a3a" stroke-width="5" fill="none"/><path d="M-4,-24l8,8M4,-26l8,8M12,-24l6,6" stroke="#fff" stroke-width="2.4"/><path d="M22,-18Q34,-16 36,-8" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/></g>`; }).join("")}</g>`);
      put(L.glow, `<path d="M-1600,-600H2900V2900H-1600Z M${DX0},${DT}V${DB}H${DX1}V${DT}Z" fill="url(#qkCorrWall)" fill-rule="evenodd"/>
        <rect x="-1600" y="-600" width="4500" height="${DT - 40 + 600}" fill="url(#qkAOdn)" opacity=".5"/>
        ${poly([[DX0 - 34, DT - 34], [DX1 + 34, DT - 34], [DX1, DT], [DX0, DT]], `fill="#6a442a" ${OUT2}`)}${poly([[DX0 - 34, DT - 34], [DX0, DT], [DX0, DB], [DX0 - 34, DB + 20]], `fill="#8a5a38" ${OUT2}`)}${poly([[DX1 + 34, DT - 34], [DX1, DT], [DX1, DB], [DX1 + 34, DB + 20]], `fill="#5e3a22" ${OUT2}`)}
        <path d="M${DX0 - 60},${DT - 60}H${DX1 + 60}V${DB + 20}H${DX1 + 34}V${DT - 34}H${DX0 - 34}V${DB + 20}H${DX0 - 60}Z" fill="#7a5236" ${OUT3}/><path d="M${DX0 - 56},${DT - 56}H${DX1 + 56}" stroke="#a87a52" stroke-width="3"/>
        <rect x="1470" y="700" width="140" height="70" rx="8" fill="#2a2018" ${OUT3}/><rect x="1476" y="706" width="128" height="58" rx="5" fill="none" stroke="#c8a050" stroke-width="2"/><text x="1540" y="750" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#e8c46a">2714</text>
        <circle cx="1540" cy="840" r="16" fill="#e8e2d6" stroke="#9a9286" stroke-width="2"/><circle cx="1540" cy="840" r="6" fill="#c8312a"/>
        <path d="M-1600,${DB}H2900V2900H-1600Z" fill="url(#qkCarpet)"/><rect x="-1600" y="${DB}" width="4500" height="40" fill="url(#qkAOdn)"/>
        <path d="M${DX0},${DT}L540,${DT - 90}V${DB + 90}L${DX0},${DB}Z" fill="url(#qkDoorWood)" ${OUT3}/><path d="M${DX0 - 18},${DT + 40}L566,${DT - 34}V${DB + 40}L${DX0 - 18},${DB - 24}Z" fill="none" stroke="#4a2e1a" stroke-width="3" opacity=".6"/>
        <path d="M572,1060h40" stroke="#d8c070" stroke-width="12" stroke-linecap="round"/><circle cx="572" cy="1060" r="12" fill="#d8c070" ${OUT2}/>`);
    }
    // under the table: the table huge in the foreground (underside across the top, legs at the sides)
    if (o.under) {
      const u = o.under, cx = u.x ?? 1050, top = u.top ?? 1120, half = u.half ?? 560, G = u.G ?? 2050;
      const X0 = cx - half - 240, W = 2 * half + 480;
      let g = `<rect x="${X0}" y="${top - 1400}" width="${W}" height="1400" fill="#5a3820"/>`;
      for (let i = 0; i < 6; i++) g += `<rect x="${X0}" y="${top - 1400 + i * 233}" width="${W}" height="231" fill="${["#5e3a22", "#563420", "#62402a"][i % 3]}"/>`;
      g += grain(X0, top - 1400, W, 1400, 81, { col: "#2a1608", op: 0.3, gap: 22 });
      g += `<rect x="${cx - half + 30}" y="${top - 240}" width="${2 * half - 60}" height="60" fill="#4a2c18" ${OUT2}/><path d="M${cx - half + 30},${top - 236}H${cx + half - 30}" stroke="#7a5030" stroke-width="3"/>`;
      g += [cx - half + 120, cx + half - 120].map((x) => `<g fill="#9aa0a4" stroke="${INK}" stroke-width="2"><rect x="${x - 40}" y="${top - 120}" width="80" height="80" rx="6"/><circle cx="${x - 22}" cy="${top - 102}" r="5"/><circle cx="${x + 22}" cy="${top - 58}" r="5"/></g>`).join("");
      g += `<rect x="${X0}" y="${top - 74}" width="${W}" height="74" fill="url(#qkFrontW)" ${OUT}/><path d="M${X0},${top - 70}H${X0 + W}" stroke="#c8925e" stroke-width="4" opacity=".7"/><rect x="${X0}" y="${top - 140}" width="${W}" height="66" fill="url(#qkAOup)"/>`;
      g += `<rect x="${cx - half + 40}" y="${top}" width="${2 * half - 80}" height="40" fill="#5a3418" opacity=".85"/><rect x="${cx - half + 40}" y="${top}" width="${2 * half - 80}" height="70" fill="url(#qkAOdn)"/>`;
      for (const [x, w] of [[cx - half - 110, 110], [cx + half, 110]]) g += `<rect x="${x}" y="${top}" width="${w}" height="${G - top}" fill="url(#qkLegW)" ${OUT}/><path d="M${x + w * 0.3},${top + 30}V${G - 20}" stroke="#d8a878" stroke-width="7" opacity=".35"/>${grain(x + 4, top + 4, w - 8, G - top - 8, x, { col: "#3a2010", op: 0.25, dir: "v", gap: 18, knots: 1 })}`;
      put(L.glow, g);
    }
  }

  // the dining table (front legs at y 1640): back legs, the inner faces of the aprons, front legs, the front apron, the top
  const TX0 = -0.957, TX1 = 0.957, TZ0 = 4.0, TZ1 = 4.88, TH = 0.75, TT = 0.05, AY = 0.62, LW = 0.075, IN = 0.03;
  const legs = (z) => [TX0 + IN, TX1 - IN - LW].map((lx) => box3(lx, lx + LW, 0, AY, z, z + LW, { front: "url(#qkLegW)", side: "#5a3418", out: OUT2 })).join("");
  const tTop = () => {
    let s = hq(TX0, TX1, TZ0, TZ1, TH, `fill="url(#qkTopW)" ${OUT3}`);
    let g = "", q = mk(52);
    for (let X = TX0 + 0.05; X < TX1; X += 0.055 + q() * 0.05) g += ln(R(X + (q() - 0.5) * 0.02, TH, TZ1 - q() * 0.1), R(X, TH, TZ0 + q() * 0.3));
    s += `<path d="${g}" stroke="#7a4a24" stroke-width="1.6" opacity=".28" stroke-dasharray="90 14 40 20"/>`;
    s += poly([R(TX0 + 0.1, TH, TZ1 - 0.02), R(TX1 - 0.1, TH, TZ1 - 0.02), R(TX1 - 0.3, TH, TZ1 - 0.3), R(TX0 + 0.3, TH, TZ1 - 0.3)], `fill="#fff" opacity=".1"`);
    s += vq(TX0, TX1, TH - TT, TH, TZ0, `fill="url(#qkFrontW)" ${OUT3}`);
    const [a, y] = R(TX0, TH, TZ0), [b] = R(TX1, TH, TZ0);
    s += `<path d="M${f1(a + 4)},${f1(y + 2)}H${f1(b - 4)}" stroke="#e0aa72" stroke-width="3" opacity=".75"/>`;
    return s;
  };
  Qk.table = () => {
    let s = "";
    for (const [X, Z] of [[TX0 + 0.07, TZ0 + 0.07], [TX1 - 0.07, TZ0 + 0.07], [TX0 + 0.07, TZ1 - 0.07], [TX1 - 0.07, TZ1 - 0.07]]) { const [x, y] = R(X, 0, Z); s += cs(x, y + 2, 26, 7, 0.9); }
    { const [x, y] = R(0, 0, (TZ0 + TZ1) / 2); s += cs(x, y, 380, 40, 0.5); }
    s += legs(TZ1 - IN - LW);
    s += vq(TX0 + IN, TX1 - IN, AY, TH - TT, TZ1 - IN - 0.02, `fill="#6a3e22" ${OUT2}`);
    s += sq(TX0 + IN + 0.02, AY, TH - TT, TZ0 + IN, TZ1 - IN, `fill="#5a341c" ${OUT2}`) + sq(TX1 - IN - 0.02, AY, TH - TT, TZ0 + IN, TZ1 - IN, `fill="#5a341c" ${OUT2}`);
    s += legs(TZ0 + IN) + vq(TX0 + IN, TX1 - IN, AY, TH - TT, TZ0 + IN, `fill="url(#qkFrontW)" ${OUT2}`);
    return s + tTop();
  };
  // the parts of the table nearer than whoever is under it (front legs, the front apron, the top's front edge): redraw them in glow
  Qk.tableFront = () => {
    let s = legs(TZ0 + IN) + vq(TX0 + IN, TX1 - IN, AY, TH - TT, TZ0 + IN, `fill="url(#qkFrontW)" ${OUT2}`) + vq(TX0, TX1, TH - TT, TH, TZ0, `fill="url(#qkFrontW)" ${OUT3}`);
    const [a, y] = R(TX0, TH, TZ0), [b] = R(TX1, TH, TZ0);
    return s + `<path d="M${f1(a + 4)},${f1(y + 2)}H${f1(b - 4)}" stroke="#e0aa72" stroke-width="3" opacity=".75"/>`;
  };

  // the room answers the quake
  Qk.react = (tl, id, t0, dur, a = 1, o = {}) => {
    const $ = (s) => document.getElementById(`${id}-${s}`), org = (el) => el.dataset.o, n = (p) => Math.max(1, Math.ceil(dur / p));
    const sway = (s, amp, per, ph = 0) => { const el = $(s); if (!el) return; tl.fromTo(el, { rotation: -amp * a, svgOrigin: org(el) }, { rotation: amp * a, svgOrigin: org(el), duration: per, repeat: n(per), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + ph); };
    const jit = (s, ax, ay, per, ph = 0) => { const el = $(s); if (!el) return; tl.fromTo(el, { x: -ax * a, y: 0 }, { x: ax * a, y: -ay * a, duration: per, repeat: n(per), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + ph); };
    sway("curL", 2.2, 0.62); sway("curR", 2.2, 0.62, 0.15);
    sway("photo", 9, 0.42); sway("photo2", 8, 0.46, 0.1); sway("clock", 2.5, 0.3);
    sway("plant", 3.5, 0.5, 0.05); sway("flamp", 2.2, 0.38, 0.08); sway("bplants", 1.4, 0.55);
    jit("tprops", 3, 2, 0.07); jit("cup", 3, 2.5, 0.065, 0.03); jit("kprops", 2.5, 1.5, 0.08, 0.02); jit("chL", 5, 1, 0.11); jit("chR", 5, 1, 0.12, 0.04);
    const bks = document.querySelectorAll(`#${id}-books .qkBook`);
    bks.forEach((b, k) => tl.fromTo(b, { rotation: -3 * a, svgOrigin: `${b.dataset.x} ${b.dataset.y}` }, { rotation: 3 * a, svgOrigin: `${b.dataset.x} ${b.dataset.y}`, duration: 0.16 + (k % 3) * 0.03, repeat: n(0.18), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    (o.fall || []).forEach((t, k) => {
      const b = bks[(k * 3) % Math.max(1, bks.length)];
      if (!b) return;
      tl.to(b, { rotation: k % 2 ? 95 : -95, x: (k % 2 ? 1 : -1) * 40, y: 1400 - +b.dataset.y + 30, svgOrigin: `${b.dataset.x} ${b.dataset.y}`, duration: 0.45, ease: "power2.in" }, t0 + t);
    });
    if (o.dust) Pop2.particles(tl, o.dust.layer, { type: "dust", n: o.dust.n || 40, box: o.dust.box || [200, 120, 1700, 900], seed: o.dust.seed || 7, t0, dur });
  };

  // ---------------- the fridge door, close ----------------
  function qkFridge(L, o = {}) {
    const id = o.id || "fd";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#e6e8e8"/>`);
    let s = `<rect x="-400" y="-400" width="1880" height="2800" fill="url(#qkFridgeG)"/>${brushed(-400, -400, 1880, 2800, 17)}<path d="M-400,1500H1480" stroke="#c8ccce" stroke-width="10"/><path d="M960,300V1300" stroke="#b8bec2" stroke-width="40" stroke-linecap="round"/><path d="M948,320V1280" stroke="#fff" stroke-width="8" opacity=".7" stroke-linecap="round"/>
      <path d="M-400,-200L1480,600V700L-400,-100Z" fill="#fff" opacity=".18"/>`;
    // a child's drawing: แม่ in a nurse's cap holding มิว's hand under a sun
    s += `<g id="${id}-draw"><g transform="translate(250,1560) rotate(-6)"><rect x="-196" y="-152" width="400" height="300" fill="#000" opacity=".12"/><rect x="-200" y="-160" width="400" height="300" fill="#fbf8ee" ${OUT3}/>
      <circle cx="140" cy="-110" r="30" fill="#f6c935"/><path d="M140,-160v-10M190,-110h10M176,-146l8,-8" stroke="#f6c935" stroke-width="5"/>
      <circle cx="-60" cy="-50" r="26" fill="none" stroke="#e8682a" stroke-width="5"/><path d="M-80,-78h40l-6,-12h-28z" fill="#fff" stroke="#3a6ad8" stroke-width="4"/><path d="M-60,-24V60M-60,0L-20,20M-60,0L-96,24M-60,60L-80,110M-60,60L-40,110" stroke="#3a6ad8" stroke-width="6" fill="none"/>
      <circle cx="30" cy="0" r="20" fill="none" stroke="#e8682a" stroke-width="5"/><path d="M30,20V80M30,40L-20,22M30,40L64,60M30,80L14,120M30,80L46,120" stroke="#d8312a" stroke-width="6" fill="none"/>
      <text x="0" y="120" text-anchor="middle" font-family="Mali" font-weight="700" font-size="30" fill="#8a4ac8">แม่กับมิว</text></g>
      ${knob(240, 1406, 26, "#e8443a")}</g>`;
    // magnets and a photo strip
    s += `<g transform="translate(830,520) rotate(4)"><rect x="-56" y="-194" width="120" height="400" fill="#000" opacity=".12"/><rect x="-60" y="-200" width="120" height="400" fill="#fff" ${OUT3}/>${[0, 1, 2].map((k) => `<rect x="-48" y="${-186 + k * 128}" width="96" height="112" fill="${["#f2c8a8", "#c8e0f0", "#f6e2a0"][k]}"/><circle cx="-10" cy="${-136 + k * 128}" r="20" fill="#e8b88e"/><circle cx="16" cy="${-126 + k * 128}" r="14" fill="#c99068"/>`).join("")}</g>
      ${knob(830, 306, 24, "#3aa0e8")}${knob(120, 300, 20, "#4a8a5a")}${knob(640, 1180, 18, "#f2c230")}`;
    s += `<g id="${id}-note" transform="translate(370,820)"></g>`;
    put(L.set, s);
  }

  // ---------------- the glass of water, close ----------------
  function qkCup(L, o = {}) {
    const id = o.id || "cu";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#cfe6f0"/>`);
    // the room soft behind: the window's light, the lamp
    put(L.far, `<rect x="-600" y="-600" width="2300" height="1500" fill="#e8f4fa"/><rect x="-600" y="200" width="2300" height="700" fill="#bcdcee" opacity=".7"/>
      <circle cx="200" cy="300" r="90" fill="#fff" opacity=".6"/><circle cx="820" cy="180" r="140" fill="#fff6d0" opacity=".55"/><rect x="380" y="-600" width="30" height="1500" fill="#3c4248" opacity=".35"/><rect x="-200" y="-600" width="30" height="1500" fill="#3c4248" opacity=".3"/>
      <rect x="-600" y="560" width="2300" height="14" fill="#8a9298" opacity=".35"/>`);
    let s = `<path d="M-600,900H1700V2600H-600Z" fill="url(#qkTopW)"/><path d="M-600,900H1700" stroke="#e0aa72" stroke-width="10" opacity=".7"/>`;
    for (let k = 0; k < 9; k++) s += `<path d="M-600,${980 + k * 170}Q540,${960 + k * 170} 1700,${1000 + k * 170}" stroke="#7a4a24" stroke-width="4" fill="none" opacity=".25"/>`;
    s += grain(-600, 900, 2300, 1700, 23, { col: "#6a3e1c", op: 0.18, gap: 30 });
    s += `<path d="M-600,900H1700V1300Q540,1150 -600,1300Z" fill="#fff" opacity=".12"/>`;
    // มิว's phone lying face up: the time flips 13:19 → 13:20
    s += `<g transform="translate(330,1400) rotate(-8)">${cs(14, 30, 200, 300, 0.5)}<rect x="-124" y="-238" width="260" height="500" rx="34" fill="#0a0c10"/><rect x="-130" y="-250" width="260" height="500" rx="34" fill="#1e2228" ${OUT}/><rect x="-136" y="-244" width="8" height="60" rx="3" fill="#2a2e34"/><rect x="-112" y="-226" width="224" height="452" rx="22" fill="#3a5a8a"/>
      <rect x="-112" y="-226" width="224" height="452" rx="22" fill="url(#qkSheen)"/><rect x="-30" y="-216" width="60" height="12" rx="6" fill="#0e1014"/>
      <text id="${id}-t19" x="0" y="-80" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="84" fill="#fff">13:19</text>
      <text id="${id}-t20" x="0" y="-80" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="84" fill="#fff" opacity="0">13:20</text>
      <text x="0" y="-30" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="28" fill="#dfe8f4">วันศุกร์</text>
      <rect x="-90" y="40" width="180" height="66" rx="16" fill="#fff" opacity=".18"/><circle cx="-60" cy="73" r="16" fill="#2fa45a"/><rect x="-36" y="62" width="110" height="10" rx="5" fill="#fff" opacity=".7"/><rect x="-36" y="80" width="80" height="8" rx="4" fill="#fff" opacity=".45"/></g>`;
    for (const [x, y, rot, c] of [[230, 1760, 28, "#e8443a"], [330, 1850, 10, "#3a7ad8"], [170, 1880, 48, "#4ab85a"]]) s += `<g transform="translate(${x},${y}) rotate(${rot})">${cs(10, 14, 110, 14, 0.5)}<rect x="-90" y="-12" width="180" height="24" rx="6" fill="${c}" ${OUT3}/><path d="M90,-12l26,12l-26,12z" fill="${c}" ${OUT3}/><rect x="-60" y="-12" width="90" height="24" fill="#fff" opacity=".35"/><path d="M-84,-6H80" stroke="#fff" stroke-width="3" opacity=".5"/></g>`;
    // a rattan placemat under the glass
    s += `<ellipse cx="790" cy="1912" rx="330" ry="70" fill="#000" opacity=".12"/><ellipse cx="780" cy="1904" rx="330" ry="70" fill="#d8b878" stroke="#9a7a3a" stroke-width="4"/>${[0.78, 0.56, 0.34].map((k) => `<ellipse cx="780" cy="1904" rx="${330 * k}" ry="${70 * k}" fill="none" stroke="#b8945a" stroke-width="4"/>`).join("")}`;
    // the glass: water with rings (#id-rings) that pulse outward
    s += `<g transform="translate(780,1340)"><ellipse cx="0" cy="560" rx="230" ry="44" fill="#000" opacity=".12"/><ellipse cx="40" cy="580" rx="220" ry="36" fill="#9adcf0" opacity=".25"/>
      <path d="M-210,-40L-170,540Q0,580 170,540L210,-40Z" fill="#eaf8fc" opacity=".45" ${OUT}/>
      <path d="M-196,150L-170,540Q0,580 170,540L196,150Z" fill="#9adcf0" opacity=".55"/><path d="M-150,520Q0,550 150,520" stroke="#fff" stroke-width="8" fill="none" opacity=".5"/>
      <g id="${id}-surf"><ellipse cx="0" cy="150" rx="196" ry="40" fill="#c8eef8" ${OUT3}/>
        <g id="${id}-rings">${[0, 1, 2].map((k) => `<ellipse class="qkRing" cx="0" cy="150" rx="${60 + k * 50}" ry="${12 + k * 10}" fill="none" stroke="#f4fcff" stroke-width="5" opacity=".9"/>`).join("")}</g></g>
      <path d="M-150,-10L-120,500" stroke="#fff" stroke-width="16" opacity=".55" stroke-linecap="round"/><path d="M150,0L128,460" stroke="#fff" stroke-width="6" opacity=".35" stroke-linecap="round"/><ellipse cx="0" cy="-40" rx="210" ry="44" fill="none" ${OUT}/></g>`;
    put(L.set, s);
  }

  // ---------------- แม่'s plan of the room ----------------
  function qkPlan(L, o = {}) {
    const id = o.id || "pl";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#8a6a4a"/>${grain(-1000, -1000, 3100, 4000, 8, { col: "#4a2a12", op: 0.25, gap: 26 })}`);
    let s = `<g transform="rotate(-2 540 960)"><rect x="52" y="214" width="1000" height="1500" fill="#000" opacity=".25"/><rect x="40" y="200" width="1000" height="1500" fill="#fbfaf4" ${OUT}/><rect x="40" y="200" width="1000" height="1500" fill="url(#qkGrid)"/>
      <text x="540" y="290" text-anchor="middle" font-family="Mali" font-weight="700" font-size="56" fill="#2a4a8a">ห้องเรา 2714</text>
      <path d="M120,380H960V1560H120Z" fill="none" stroke="#2a2a2a" stroke-width="12"/>
      <path d="M220,380H860" stroke="#3aa0e8" stroke-width="22"/><path d="M220,380H860" stroke="#e8f6fc" stroke-width="6"/>
      <text x="540" y="356" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#2a7ac8">หน้าต่างกระจก</text>
      <path d="M120,1400V1540" stroke="#fbfaf4" stroke-width="16"/><path d="M120,1400Q230,1410 240,1540" stroke="#2a2a2a" stroke-width="4" fill="none" stroke-dasharray="10 8"/><text x="180" y="1600" text-anchor="middle" font-family="Mali" font-weight="700" font-size="30" fill="#2a2a2a">ประตู</text>
      <rect x="380" y="760" width="320" height="200" rx="8" fill="#e8c898" stroke="#6a4428" stroke-width="6"/><text x="540" y="872" text-anchor="middle" font-family="Mali" font-weight="700" font-size="36" fill="#6a4428">โต๊ะ</text>
      ${[[370, 750], [690, 750], [370, 950], [690, 950]].map(([x, y]) => `<rect x="${x}" y="${y}" width="20" height="20" fill="#6a4428"/>`).join("")}
      <circle cx="540" cy="860" r="70" fill="none" stroke="#c8a040" stroke-width="5" stroke-dasharray="12 8"/>
      <rect x="820" y="560" width="120" height="300" fill="#c8a07a" stroke="#6a4428" stroke-width="5"/><text x="880" y="720" text-anchor="middle" font-family="Mali" font-weight="700" font-size="28" fill="#6a4428" transform="rotate(90 880 720)">ชั้นหนังสือ</text>
      <rect x="820" y="920" width="120" height="200" fill="#9adcf0" stroke="#2a7ac8" stroke-width="5"/><text x="880" y="1030" text-anchor="middle" font-family="Mali" font-weight="700" font-size="28" fill="#2a7ac8" transform="rotate(90 880 1030)">ตู้ปลา</text>
      <rect x="140" y="460" width="130" height="160" fill="#f4f4f2" stroke="#5a5a5a" stroke-width="5"/><text x="205" y="550" text-anchor="middle" font-family="Mali" font-weight="700" font-size="28" fill="#5a5a5a">ตู้เย็น</text>
      <rect x="140" y="660" width="130" height="300" fill="#e8e2d6" stroke="#5a5a5a" stroke-width="5"/><circle cx="205" cy="770" r="34" fill="none" stroke="#2a2a2a" stroke-width="5"/><text x="205" y="900" text-anchor="middle" font-family="Mali" font-weight="700" font-size="26" fill="#5a5a5a">เตาแก๊ส</text>`;
    // danger zones (red, hatched) and labels; the safe zone under the table (green)
    const Z = [[220, 390, 640, 160, "กระจกแตก"], [800, 540, 160, 340, "ของล้มทับ"], [800, 900, 160, 240, "ตู้ปลาแตก"], [130, 650, 160, 320, "แก๊ส"]];
    Z.forEach(([x, y, w, h, t], k) => {
      s += `<g id="${id}-z${k}" opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="url(#qkHatch)" stroke="#e8443a" stroke-width="6" stroke-dasharray="16 10"/></g>`;
      const lx = x + w / 2, ly = k === 0 ? y + h / 2 + 14 : y + h + 46;
      s += `<g id="${id}-l${k}" opacity="0"><rect x="${lx - 92}" y="${ly - 36}" width="184" height="50" rx="25" fill="#e8443a"/><text x="${lx}" y="${ly}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="#fff">${t}</text></g>`;
    });
    s += `<g id="${id}-safe" opacity="0"><rect x="388" y="768" width="304" height="184" rx="10" fill="#3fd07a" opacity=".35" stroke="#1e9a50" stroke-width="7"/></g>
      <g id="${id}-you" opacity="0"><circle cx="490" cy="880" r="30" fill="#2fa45a" stroke="#fff" stroke-width="6"/><text x="490" y="892" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#fff">คุณ</text></g>
      <g id="${id}-mew" opacity="0"><circle cx="600" cy="890" r="26" fill="#f2c230" stroke="#fff" stroke-width="6"/><text x="600" y="900" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="24" fill="#2a2a2a">มิว</text></g>
      <g id="${id}-ok" opacity="0"><circle cx="700" cy="1040" r="54" fill="#1e9a50" stroke="#fff" stroke-width="7"/><path d="M674,1040l20,20l34,-40" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <text x="540" y="1660" text-anchor="middle" font-family="Mali" font-weight="700" font-size="40" fill="#d8312a">ตึกโยก → มุดใต้โต๊ะ ห่างกระจก ♥ แม่</text></g>`;
    put(L.set, s);
  }

  // ---------------- แม่'s plan as a pop-up: the paper on the table, the room's things rise out of it ----------------
  // Sets.qkPlan3d(L, o) draws the wooden table behind; Qk.plan3d(tl, L, sid, t0, o) draws everything else each frame from the shot clock
  // (a real camera that tilts down and drifts round): the paper with its grid and แม่'s handwriting lying on it, the walls, the window
  // glass, the furniture popping up (table on legs, shelf, tank, fridge, stove), the danger zones rising as red glass blocks with pills
  // (o.zAt [glass, shelf, tank, gas] seconds), the green safe space under the table (o.safeAt), คุณ and มิว as pawns under it (o.youAt),
  // the tick (o.okAt); o.dur the shot length.
  function qkPlan3d(L, o = {}) {
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#5a3c26"/><radialGradient id="plVig" cx=".5" cy=".45" r=".7"><stop offset="0" stop-color="#8a603e"/><stop offset="1" stop-color="#3a2416"/></radialGradient><rect x="-1000" y="-1000" width="3100" height="4000" fill="url(#plVig)"/>`);
  }
  Qk.plan3d = (tl, L, sid, t0, o = {}) => {
    const id = `${sid}-p3`, dur = o.dur ?? 3.8, zAt = o.zAt || [0.3, 1.75, 2.0, 2.25], safeAt = o.safeAt ?? 0.2, youAt = o.youAt ?? 0.35, okAt = o.okAt ?? dur - 1.0;
    put(L.set, `<g id="${id}"></g>`);
    const root = document.getElementById(id), cl = (v) => Math.max(0, Math.min(1, v));
    const back = (u, k = 1.7) => { u = cl(u); return 1 + (k + 1) * Math.pow(u - 1, 3) + k * Math.pow(u - 1, 2); };
    const eio = (u) => { u = cl(u); return u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; };
    const W = (px, py) => [(px - 540) / 1000, (py - 950) / 1000];
    const render = (t) => {
      // the camera: from nearly straight down to an oblique look, drifting round
      const tilt = (22 + 24 * eio(t / 2.0)) * Math.PI / 180, yaw = (-7 + 11 * (t / dur)) * Math.PI / 180, D = 3.15 - 0.25 * eio(t / dur), F = 2600;
      const st = Math.sin(tilt), ct = Math.cos(tilt), sy = Math.sin(yaw), cy = Math.cos(yaw), T = [0, 0, 0.1];
      const C = [T[0] + D * st * sy, T[1] + D * ct, T[2] + D * st * cy], Fw = [-st * sy, -ct, -st * cy], Rt = [cy, 0, -sy], Dn = [ct * sy, -st, ct * cy];
      const P = (X, Y, Z) => { const v = [X - C[0], Y - C[1], Z - C[2]], d = v[0] * Fw[0] + v[1] * Fw[1] + v[2] * Fw[2]; return [540 + (F * (v[0] * Rt[0] + v[2] * Rt[2])) / d, 850 + (F * (v[0] * Dn[0] + v[1] * Dn[1] + v[2] * Dn[2])) / d, d]; };
      const Pp = (px, py, h = 0) => { const [X, Z] = W(px, py); return P(X, h, Z); };
      const path = (pts) => `M${pts.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}Z`;
      const seen = (c, n) => (C[0] - c[0]) * n[0] + (C[1] - c[1]) * n[1] + (C[2] - c[2]) * n[2] > 0;
      // a box on the paper: x0…x1 × y0…y1 in paper px, from height h0 to h1; fills { top, side, front }, at: extra attributes
      const box = (x0, y0, x1, y1, h0, h1, f, at = OUT2) => {
        const [X0, Z0] = W(x0, y0), [X1, Z1] = W(x1, y1), cx = (X0 + X1) / 2, cz = (Z0 + Z1) / 2, hm = (h0 + h1) / 2;
        const v = (X, H, Z) => P(X, H, Z);
        const faces = [
          [[[X0, h0, Z1], [X1, h0, Z1], [X1, h1, Z1], [X0, h1, Z1]], [cx, hm, Z1], [0, 0, 1], f.front || f.side],
          [[[X1, h0, Z0], [X0, h0, Z0], [X0, h1, Z0], [X1, h1, Z0]], [cx, hm, Z0], [0, 0, -1], f.side],
          [[[X0, h0, Z0], [X0, h0, Z1], [X0, h1, Z1], [X0, h1, Z0]], [X0, hm, cz], [-1, 0, 0], f.side],
          [[[X1, h0, Z1], [X1, h0, Z0], [X1, h1, Z0], [X1, h1, Z1]], [X1, hm, cz], [1, 0, 0], f.side2 || f.side],
        ];
        let s = "";
        faces.filter((q) => seen(q[1], q[2])).forEach((q) => { s += `<path d="${path(q[0].map((p) => v(...p)))}" fill="${q[3]}" ${at}/>`; });
        s += `<path d="${path([[X0, h1, Z0], [X1, h1, Z0], [X1, h1, Z1], [X0, h1, Z1]].map((p) => v(...p)))}" fill="${f.top}" ${at}/>`;
        return { s, d: P(cx, hm, cz)[2] };
      };
      // ground text: an affine from the local projection
      const gtext = (px, py, str, size, col, anchor = "middle", rot = 0) => {
        const a = Pp(px, py), b = Pp(px + 100, py), c = Pp(px, py + 100), m = [(b[0] - a[0]) / 100, (b[1] - a[1]) / 100, (c[0] - a[0]) / 100, (c[1] - a[1]) / 100];
        return `<text transform="matrix(${m.map((v) => v.toFixed(4)).join(",")},${f1(a[0])},${f1(a[1])}) rotate(${rot})" text-anchor="${anchor}" font-family="Mali" font-weight="700" font-size="${size}" fill="${col}">${str}</text>`;
      };
      let s = "";
      // the table under the paper (grain), the paper's shadow, the paper, its grid, its handwriting
      const tb = Pp(-900, -400), tb2 = Pp(1980, -400), tb3 = Pp(1980, 2500), tb4 = Pp(-900, 2500);
      s += `<path d="${path([tb, tb2, tb3, tb4])}" fill="#8a5c38"/>`;
      let g = ""; for (let y = -400; y < 2500; y += 46) { g += `M${f1(Pp(-900, y)[0])},${f1(Pp(-900, y)[1])}L${f1(Pp(1980, y + 30)[0])},${f1(Pp(1980, y + 30)[1])}`; } s += `<path d="${g}" stroke="#5a3820" stroke-width="2" opacity=".35"/>`;
      s += `<path d="${path([Pp(52, 216), Pp(1056, 216), Pp(1056, 1716), Pp(52, 1716)])}" fill="#2a1408" opacity=".35"/>`;
      s += `<path d="${path([Pp(40, 200), Pp(1040, 200), Pp(1040, 1700), Pp(40, 1700)])}" fill="#fbfaf4" ${OUT3}/>`;
      g = ""; for (let x = 80; x < 1040; x += 40) g += `M${f1(Pp(x, 200)[0])},${f1(Pp(x, 200)[1])}L${f1(Pp(x, 1700)[0])},${f1(Pp(x, 1700)[1])}`; for (let y = 240; y < 1700; y += 40) g += `M${f1(Pp(40, y)[0])},${f1(Pp(40, y)[1])}L${f1(Pp(1040, y)[0])},${f1(Pp(1040, y)[1])}`;
      s += `<path d="${g}" stroke="#9cc4dc" stroke-width="1.4" opacity=".7"/>`;
      s += gtext(540, 300, "ห้องเรา 2714", 56, "#2a4a8a") + gtext(540, 352, "หน้าต่างกระจก", 32, "#2a7ac8") + gtext(205, 1610, "ประตู", 30, "#2a2a2a") + gtext(540, 1650, "ตึกโยก → มุดใต้โต๊ะ ห่างกระจก ♥ แม่", 38, "#d8312a");
      { const a = Pp(120, 1400), b = Pp(240, 1540); s += `<path d="M${f1(a[0])},${f1(a[1])}Q${f1(Pp(230, 1410)[0])},${f1(Pp(230, 1410)[1])} ${f1(b[0])},${f1(b[1])}" stroke="#2a2a2a" stroke-width="3" fill="none" stroke-dasharray="10 8"/>`; }
      // the safe space glows under the table, the circle of the lamp
      const sa = cl((t - safeAt) / 0.35);
      if (sa > 0) s += `<path d="${path([Pp(388, 768), Pp(692, 768), Pp(692, 952), Pp(388, 952)])}" fill="#3fd07a" opacity="${f1(0.45 * sa)}" stroke="#1e9a50" stroke-width="5"/>`;
      // things that stand on the paper, back to front
      const pop = back((t - 0.1) / 0.55), items = [];
      const add = (b) => items.push(b);
      const wall = (x0, y0, x1, y1, h = 0.045) => add(box(x0, y0, x1, y1, 0, h * pop, { top: "#3a3632", side: "#2a2622", front: "#4a4642" }));
      wall(108, 368, 220, 392); wall(860, 368, 972, 392); wall(108, 368, 132, 1400); wall(948, 368, 972, 1572); wall(108, 1540, 972, 1572);
      add(box(220, 372, 860, 388, 0, 0.085 * pop, { top: "#cfeefc", side: "rgba(90,180,230,.55)", front: "rgba(120,200,240,.5)" }, `stroke="#2a7ac8" stroke-width="2"`));
      const tH = 0.07 * pop;
      for (const [x, y] of [[392, 772], [676, 772], [392, 936], [676, 936]]) add(box(x, y, x + 14, y + 14, 0, tH, { top: "#6a4428", side: "#5a3418", front: "#7a4a2a" }));
      add(box(380, 760, 700, 960, tH - 0.012 * pop, tH, { top: "#e8c898", side: "#8a5a36", front: "#a8764a" }));
      for (const [x, y] of [[300, 830], [736, 830]]) add(box(x, y, x + 44, y + 60, 0, 0.04 * pop, { top: "#c8a070", side: "#8a5a36", front: "#a8764a" }));
      add(box(820, 560, 940, 860, 0, 0.2 * pop, { top: "#c8a07a", side: "#8a5a36", front: "#a8764a" }));
      add(box(820, 920, 940, 1120, 0, 0.11 * pop, { top: "#c8f0fa", side: "rgba(80,170,210,.75)", front: "rgba(110,200,230,.7)" }, `stroke="#2a7ac8" stroke-width="2"`));
      add(box(140, 460, 270, 620, 0, 0.17 * pop, { top: "#fbfbf8", side: "#c8ccce", front: "#e8eaea" }));
      add(box(140, 660, 270, 960, 0, 0.09 * pop, { top: "#e8e2d6", side: "#b8b0a2", front: "#d8d0c2" }));
      // the danger zones: red glass blocks rising around what can hurt
      const Z = [[220, 392, 860, 552, 0.11, "กระจกแตก"], [800, 540, 960, 880, 0.24, "ของล้มทับ"], [800, 900, 960, 1140, 0.14, "ตู้ปลาแตก"], [130, 650, 290, 970, 0.12, "แก๊ส"]];
      const pills = [];
      Z.forEach(([x0, y0, x1, y1, h, lab], k) => {
        const u = t - zAt[k];
        if (u < 0) return;
        const e = back(u / 0.45, 2.2), pulse = 0.55 + 0.15 * Math.sin(u * 7), hh = h * e;
        add(box(x0, y0, x1, y1, 0, Math.max(0.002, hh), { top: `rgba(232,68,58,${f1(0.45 * pulse + 0.1)})`, side: `rgba(216,49,42,${f1(0.35 * pulse)})`, front: `rgba(232,68,58,${f1(0.4 * pulse)})` }, `stroke="#ff5a46" stroke-width="3"`));
        const [X0, Z0] = W(x0, y0), [X1, Z1] = W(x1, y1), top = P(X0 + (X1 - X0) * (k === 0 ? 0.36 : 0.5), hh + 0.03, (Z0 + Z1) / 2);
        pills.push([top, lab, back((u - 0.08) / 0.4, 2.6), "#e8443a"]);
      });
      items.sort((a, b) => b.d - a.d).forEach((b) => { s += b.s; });
      // คุณ and มิว: pawns under the table
      [[490, 880, "#2fa45a", "คุณ", "#fff"], [600, 890, "#f2c230", "มิว", "#2a2a2a"]].forEach(([px, py, col, lab, tc], k) => {
        const e = back((t - youAt - k * 0.12) / 0.4, 2.6);
        if (e <= 0.01) return;
        const base = Pp(px, py), head = Pp(px, py, 0.05 * e), r = Math.max(6, 26 * (head[1] - Pp(px, py, 0.08)[1]) / 20);
        s += `<ellipse cx="${f1(base[0])}" cy="${f1(base[1])}" rx="${f1(r * 1.1)}" ry="${f1(r * 0.42)}" fill="#000" opacity=".25"/><path d="M${f1(base[0] - r * 0.8)},${f1(base[1])}Q${f1(base[0])},${f1(base[1] + r * 0.3)} ${f1(base[0] + r * 0.8)},${f1(base[1])}L${f1(head[0] + r * 0.4)},${f1(head[1])}H${f1(head[0] - r * 0.4)}Z" fill="${col}" ${OUT2}/>
          <circle cx="${f1(head[0])}" cy="${f1(head[1] - r * 0.7)}" r="${f1(r)}" fill="${col}" ${OUT2}/><circle cx="${f1(head[0] - r * 0.35)}" cy="${f1(head[1] - r * 1.05)}" r="${f1(r * 0.3)}" fill="#fff" opacity=".55"/>`;
        pills.push([[head[0] + (k ? 34 : -34), head[1] - r * 2.4], lab, e, col, tc]);
      });
      // pills (billboards) last
      pills.forEach(([p, lab, e, col, tc]) => {
        if (e <= 0.01) return;
        const w = 46 + lab.length * 27;
        s += `<g transform="translate(${f1(p[0])},${f1(p[1] - 24)}) scale(${f4(e)})"><rect x="${f1(-w / 2)}" y="-22" width="${f1(w)}" height="54" rx="27" fill="${Qk.tone(col.startsWith("#") ? col : "#e8443a", -0.45)}"/><rect x="${f1(-w / 2)}" y="-30" width="${f1(w)}" height="54" rx="27" fill="${col}" stroke="#140e0a" stroke-width="4"/><path d="M${f1(-w / 2 + 18)},-22H${f1(w / 2 - 18)}" stroke="#fff" stroke-width="3" opacity=".45" stroke-linecap="round"/>
          <text y="8" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="${tc || "#fff"}">${lab}</text></g>`;
      });
      const ok = back((t - okAt) / 0.35, 2.6);
      if (ok > 0.01) { const p = Pp(720, 1050, 0.03); s += `<g transform="translate(${f1(p[0])},${f1(p[1])}) scale(${f4(ok)})"><circle cy="8" r="54" fill="#0e6a34"/><circle r="54" fill="#1e9a50" stroke="#fff" stroke-width="7"/><path d="M-26,0l20,20l34,-40" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`; }
      root.innerHTML = s;
    };
    render(0);
    const c = { t: 0 };
    tl.fromTo(c, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => render(c.t) }, t0);
  };

  Object.assign(Sets, { qkRoom, qkFridge, qkCup, qkPlan, qkPlan3d });
})();
