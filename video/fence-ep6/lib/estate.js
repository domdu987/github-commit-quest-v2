// Sets and props for "เอาชีวิตรอด 99 วัน" EP.6 "นิคม": คุณวิน's industrial estate — seen from the access road at dawn
// (a three-metre fence whose lamps are still lit, saw-tooth factory roofs covered in solar panels, a water tower, a
// chimney), the sliding gate with its guard tower and the banner "ทุกคนต้องมีประโยชน์", the yard inside (washroom block,
// two-storey office, factory with its roller door, laundry, vegetable beds), the workshop bench in the first person, the
// communal washroom where the chlorine gas pools along the floor, the canteen at night, the dormitory with the radio,
// คุณวิน's notebook, the first-person hook over the bucket, and ปั้น's drawing of ยายจันทร์ outside the fence.
// Same layer contract as sets.js / fence.js / road.js (sky far mid set act fg + glow/light); load after road.js.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const O = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const dressed = (o) => o.dress !== false && !!window.Dress;
  const T = (x, y, txt, size, col, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 900}" font-size="${size}" fill="${col}"${o.extra || ""}>${txt}</text>`;

  Sets.DEFS += `
    <linearGradient id="eSolar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#46679c"/><stop offset=".5" stop-color="#26406a"/><stop offset="1" stop-color="#182844"/></linearGradient>
    <pattern id="eCell" width="26" height="18" patternUnits="userSpaceOnUse"><path d="M0,1H26M1,0V18" stroke="#a9c2e2" stroke-opacity=".42" stroke-width="1.6"/></pattern>
    <linearGradient id="eZinc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9d0d4"/><stop offset="1" stop-color="#a1aab0"/></linearGradient>
    <linearGradient id="eZincN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c4656"/><stop offset="1" stop-color="#2a3240"/></linearGradient>
    <pattern id="eRib" width="22" height="40" patternUnits="userSpaceOnUse"><path d="M1,0V40" stroke="#000" stroke-opacity=".14" stroke-width="3"/><path d="M8,0V40" stroke="#fff" stroke-opacity=".16" stroke-width="2"/></pattern>
    <pattern id="eTileW" width="64" height="64" patternUnits="userSpaceOnUse"><rect width="64" height="64" fill="#dfe5de"/><path d="M0,1H64M1,0V64" stroke="#98a298" stroke-width="2.5"/><path d="M6,7H58" stroke="#fff" stroke-opacity=".55" stroke-width="2"/></pattern>
    <pattern id="eTileF" width="110" height="110" patternUnits="userSpaceOnUse"><rect width="110" height="110" fill="#b7b6ab"/><path d="M0,1H110M1,0V110" stroke="#6c6b63" stroke-width="3"/><rect x="55" y="55" width="54" height="54" fill="#000" opacity=".05"/></pattern>
    <pattern id="ePeg" width="44" height="44" patternUnits="userSpaceOnUse"><rect width="44" height="44" fill="#9a7a52"/><circle cx="22" cy="22" r="4.5" fill="#3a2a1a"/><circle cx="21" cy="21" r="4.5" fill="#5a4026" opacity=".5"/></pattern>
    <linearGradient id="eGasV" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#b4c43c" stop-opacity=".72"/><stop offset=".5" stop-color="#c4d25a" stop-opacity=".38"/><stop offset="1" stop-color="#d6e282" stop-opacity="0"/></linearGradient>
    <radialGradient id="eGasR"><stop offset="0" stop-color="#b0c038" stop-opacity=".7"/><stop offset=".6" stop-color="#c2d058" stop-opacity=".3"/><stop offset="1" stop-color="#d6e282" stop-opacity="0"/></radialGradient>
    <linearGradient id="eWarm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6a8"/><stop offset="1" stop-color="#f2a94a"/></linearGradient>
    <radialGradient id="eFluo"><stop offset="0" stop-color="#f4fbff" stop-opacity=".85"/><stop offset=".25" stop-color="#d8ecf6" stop-opacity=".3"/><stop offset="1" stop-color="#d8ecf6" stop-opacity="0"/></radialGradient>
    <radialGradient id="eFlood"><stop offset="0" stop-color="#fffbe8" stop-opacity=".9"/><stop offset=".2" stop-color="#fff2c8" stop-opacity=".35"/><stop offset="1" stop-color="#ffe2a0" stop-opacity="0"/></radialGradient>
    <linearGradient id="eBeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6d8" stop-opacity=".34"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></linearGradient>
    <linearGradient id="ePaintG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fbfa8"/><stop offset="1" stop-color="#84a68e"/></linearGradient>
    <linearGradient id="eCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ece4cf"/><stop offset="1" stop-color="#d6ccb2"/></linearGradient>
    <linearGradient id="eDesk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6e4e30"/><stop offset="1" stop-color="#3e2a1a"/></linearGradient>
    <linearGradient id="eBench" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6a44"/><stop offset="1" stop-color="#5e4428"/></linearGradient>
    <linearGradient id="eSteel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d3d9dd"/><stop offset=".45" stop-color="#a7b0b6"/><stop offset="1" stop-color="#7d868c"/></linearGradient>
    <linearGradient id="eDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d7395"/><stop offset=".45" stop-color="#c99aa0"/><stop offset=".78" stop-color="#f4c49a"/><stop offset="1" stop-color="#ffe0a8"/></linearGradient>
    <linearGradient id="eNightIn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3446"/><stop offset="1" stop-color="#1c2432"/></linearGradient>`;

  const SKYG = { morning: "eDawn", day: "fDay", noon: "fNoon", dusk: "fDusk", night: "fNight" };
  const sky = (L, t) => put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="url(#${SKYG[t] || "eDawn"})"/>`);
  const stars = (L, seed, n = 80) => { const q = mk(seed); put(L.sky, Array.from({ length: n }, () => `<circle cx="${f1(-1200 + q() * 3400)}" cy="${f1(-800 + q() * 1700)}" r="${f1(1 + q() * 2.2)}" fill="#e9eef5" opacity="${f1(0.3 + q() * 0.6)}"/>`).join("")); };

  // ======================================================================================================
  // props
  // ======================================================================================================
  // a jug of household bleach: white HDPE, a hollow handle at the shoulder, red cap, blue label; origin = bottom centre (~130 × 240)
  function BLEACH(id = "", o = {}) {
    const I = id ? ` id="${id}"` : "";
    return `<g${I}><path d="M-60,-10Q-62,0 -50,0H50Q62,0 62,-10V-152Q62,-180 40,-194L22,-202V-214H-22V-202L-40,-194Q-62,-180 -60,-152Z" fill="#f4f4ee" ${OUT}/>
      <path d="M22,-196Q58,-190 58,-150Q58,-120 40,-112" fill="none" stroke="${INK}" stroke-width="4"/><ellipse cx="34" cy="-152" rx="11" ry="26" fill="#4a4a44" opacity=".55" ${O(3)}/>
      <rect x="-24" y="-234" width="48" height="24" rx="5" fill="#c8392b" ${O(3)}/><path d="M-18,-226h36" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>
      <rect x="-54" y="-132" width="76" height="104" rx="8" fill="#2f6fb8" ${O(3)}/>${T(-16, -96, "ฟอก", 25, "#fff")}${T(-16, -68, "ขาว", 25, "#fff")}
      <path d="M-16,-56l10,10l-10,10l-10,-10z" fill="#fff" stroke="#c8392b" stroke-width="2.5"/><path d="M-46,-160V-20" stroke="#fff" stroke-width="8" opacity=".6" stroke-linecap="round"/></g>`;
  }
  // a bottle of toilet-bowl cleaner (WA DOH lists toilet bowl cleaners among the products that contain acids): squat purple bottle,
  // an angled nozzle, white label "ล้างห้องน้ำ" with a red warning strip; origin = bottom centre (~110 × 300)
  function ACID(id = "", o = {}) {
    const I = id ? ` id="${id}"` : "";
    return `<g${I}><path d="M-50,-8Q-50,0 -42,0H42Q50,0 50,-8V-168Q50,-196 24,-206V-224H-16V-206Q-50,-196 -50,-168Z" fill="#6a58b8" ${OUT}/>
      <path d="M-16,-224L-10,-244L52,-292Q60,-298 66,-290L70,-284Q74,-276 66,-270L14,-230L12,-222Z" fill="#7d6cc8" ${OUT}/><path d="M56,-292l14,-12l10,10l-12,12z" fill="#c8392b" ${O(3)}/>
      <rect x="-42" y="-160" width="84" height="120" rx="8" fill="#f4f2ee" ${O(3)}/>${T(0, -118, "ล้าง", 24, "#4a3a98")}${T(0, -90, "ห้องน้ำ", 22, "#4a3a98")}
      <rect x="-42" y="-74" width="84" height="22" fill="#c8392b"/>${T(0, -57, "อันตราย", 17, "#fff")}<path d="M-38,-186V-16" stroke="#fff" stroke-width="7" opacity=".35" stroke-linecap="round"/></g>`;
  }
  // the red plastic bucket of every Thai washroom with water and a floating blue scoop (ขัน); origin = bottom centre (~200 × 170)
  function BUCKETR(id = "", o = {}) {
    const I = id ? ` id="${id}"` : "";
    return `<g${I}><ellipse cx="8" cy="2" rx="104" ry="16" fill="#000" opacity=".24"/><path d="M-92,-150L-74,0H74L92,-150Z" fill="#c8392b" ${OUT}/>
      <path d="M-87,-112H87M-83,-78H83" stroke="#a52a20" stroke-width="5"/><ellipse cx="0" cy="-150" rx="92" ry="22" fill="#a52a20" ${OUT}/>
      <ellipse ${id ? `id="${id}-w"` : ""} cx="0" cy="-146" rx="80" ry="15" fill="${o.water || "#9cbcc6"}"/><path d="M-50,-150q30,-6 60,0" stroke="#fff" stroke-width="3" opacity=".5" fill="none"/>
      ${o.scoop === false ? "" : `<g transform="translate(-24,-150)"><ellipse rx="30" ry="9" fill="#2f6fb8" ${O(3)}/><path d="M26,-2l42,-16" stroke="#2f6fb8" stroke-width="10" stroke-linecap="round"/></g>`}
      <path d="M-88,-150Q0,-262 88,-150" stroke="#5b6066" stroke-width="5" fill="none"/><path d="M-80,-140L-66,-12" stroke="#fff" stroke-opacity=".3" stroke-width="8"/></g>`;
  }
  // chlorine gas: heavier than air (CDC), so it lies along the floor and climbs slowly — a soft yellow-green band from the floor
  // y up h, and blobs (class "egb") the shots drift; origin-free, the shot scales #id from its bottom edge
  function GAS(id, x0, x1, y, h, op = 1) {
    const r = mk(Math.abs(Math.round(x0 * 7 + y)) + 3); let s = `<g id="${id}" opacity="${op}"><rect x="${x0}" y="${y - h}" width="${x1 - x0}" height="${h + 40}" fill="url(#eGasV)"/>`;
    for (let k = 0; k < 14; k++) { const x = x0 + r() * (x1 - x0), w = 140 + r() * 240, yy = y - r() * h * 0.7; s += `<ellipse class="egb" cx="${f1(x)}" cy="${f1(yy)}" rx="${f1(w)}" ry="${f1(w * 0.32)}" fill="url(#eGasR)"/>`; }
    return s + `</g>`;
  }
  // a row of solar panels on a slope from p0 → p1 (the eaves) with depth (dx, dy): a parallelogram of cells and a sky glint
  const SOLAR = (x0, y0, x1, y1, dx, dy) => `<path d="M${x0},${y0}L${x1},${y1}L${x1 + dx},${y1 + dy}L${x0 + dx},${y0 + dy}Z" fill="url(#eSolar)" ${O(3)}/><path d="M${x0},${y0}L${x1},${y1}L${x1 + dx},${y1 + dy}L${x0 + dx},${y0 + dy}Z" fill="url(#eCell)"/>
    <path d="M${f1(x0 + (x1 - x0) * 0.15 + dx * 0.3)},${f1(y0 + (y1 - y0) * 0.15 + dy * 0.3)}L${f1(x0 + (x1 - x0) * 0.55 + dx * 0.3)},${f1(y0 + (y1 - y0) * 0.55 + dy * 0.3)}" stroke="#d8e8ff" stroke-width="4" opacity=".55"/>`;
  // a saw-tooth factory seen three-quarter: wall x..x+w from the ground y up h, n teeth whose slopes carry solar panels and whose
  // upright faces are the clerestory glass (lit = lamps still on inside); dark = night palette
  function SAW(x, y, w, h, n, o = {}) {
    const tw = w / n, th = o.th ?? Math.min(130, tw * 0.6), dx = o.dx ?? 60, dy = o.dy ?? -46, top = y - h, lit = o.lit, dark = o.dark;
    let s = `<g><rect x="${x}" y="${top}" width="${w}" height="${h}" fill="url(#${dark ? "eZincN" : "eZinc"})" ${OUT}/><rect x="${x}" y="${top}" width="${w}" height="${h}" fill="url(#eRib)"/>`;
    s += `<path d="M${x + w},${top}L${x + w + dx},${top + dy}V${y + dy}L${x + w},${y}Z" fill="${dark ? "#222a36" : "#8f989e"}" ${OUT}/>`;   // the side wall going back
    for (let k = n - 1; k >= 0; k--) { const a = x + k * tw;
      s += `<path d="M${a + tw},${top}V${top - th}L${a + tw + dx},${top - th + dy}V${top + dy}Z" fill="${lit ? "#ffd58a" : dark ? "#3a4a5a" : "#9fc0cc"}" ${O(3)}/>${lit ? `<path d="M${a + tw + 6},${top - th + 8}V${top - 6}" stroke="#fff6d8" stroke-width="4" opacity=".7"/>` : ""}`;
      s += SOLAR(a, top - th, a + tw, top, dx, dy);
      s += `<path d="M${a},${top}V${top - th}L${a + tw},${top}Z" fill="url(#${dark ? "eZincN" : "eZinc"})" ${O(3)}/>`; }
    if (o.windows !== false) { const wy = top + h * 0.28; s += `<rect x="${x + 20}" y="${f1(wy)}" width="${w - 40}" height="${f1(h * 0.12)}" fill="${lit ? "url(#eWarm)" : dark ? "#2a3646" : "#7f9aa6"}" ${O(3)}/>` + Array.from({ length: Math.floor((w - 40) / 70) }, (_, k) => `<path d="M${x + 20 + (k + 1) * 70},${f1(wy)}v${f1(h * 0.12)}" stroke="${INK}" stroke-width="3"/>`).join(""); }
    return s + `</g>`;
  }
  // the water tower: four splayed legs with braces, a cylindrical tank with a ladder; origin = ground centre
  const WTOWER = (x, y, s = 1, dark) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-70,0L-40,-520M70,0L40,-520M-60,-150H60M-48,-330H48M-62,-150L48,-330M62,-150L-48,-330" stroke="${dark ? "#2a3240" : "#6f7880"}" stroke-width="12" fill="none"/>
    <path d="M-110,-520V-690Q-110,-712 0,-712Q110,-712 110,-690V-520Q110,-500 0,-500Q-110,-500 -110,-520Z" fill="${dark ? "#3a4656" : "#c9d0d4"}" ${OUT}/><path d="M-110,-610Q0,-590 110,-610" stroke="${dark ? "#2a3240" : "#9aa4ab"}" stroke-width="6" fill="none"/><path d="M-80,-700V-510" stroke="#fff" stroke-width="10" opacity="${dark ? 0.1 : 0.35}"/>
    <path d="M86,-520V-130M100,-520V-130${Array.from({ length: 9 }, (_, k) => `M86,${-500 + k * 42}h14`).join("")}" stroke="${dark ? "#2a3240" : "#5b6066"}" stroke-width="4" fill="none"/></g>`;
  // the chimney with red and white bands; origin = ground centre
  const CHIMNEY = (x, y, h, s = 1, dark) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-46,0L-30,${-h}H30L46,0Z" fill="${dark ? "#4a3a3a" : "#d9d4c8"}" ${OUT}/>${[0.12, 0.3].map((k) => `<path d="M${f1(-30 - 16 * k)},${f1(-h + h * k)}H${f1(30 + 16 * k)}V${f1(-h + h * k + 50)}H${f1(-30 - 16 * k)}Z" fill="${dark ? "#5a2424" : "#c8392b"}" opacity=".9"/>`).join("")}<rect x="-38" y="${-h - 18}" width="76" height="22" rx="4" fill="${dark ? "#2a2a2a" : "#5b6066"}" ${O(3)}/></g>`;
  // a lamp post with a floodlight head (lit draws the lamp face; the glow goes in the glow layer from the set); origin = ground
  const LAMPPOST = (x, y, h, lit, dark) => `<g transform="translate(${x},${y})"><path d="M0,0V${-h}" stroke="${dark ? "#2a3040" : "#7d868c"}" stroke-width="16"/><path d="M0,${-h + 10}q50,-30 90,-10" stroke="${dark ? "#2a3040" : "#7d868c"}" stroke-width="10" fill="none"/>
    <rect x="74" y="${-h - 16}" width="70" height="30" rx="8" fill="${dark ? "#1e2430" : "#5b6066"}" ${O(3)}/><rect x="80" y="${-h + 6}" width="58" height="10" rx="4" fill="${lit ? "#fffbe8" : "#c9d0d4"}"/><rect x="-22" y="-14" width="44" height="14" rx="4" fill="${dark ? "#1e2430" : "#5b6066"}"/></g>`;
  // the estate's three-metre fence: concrete posts every gap px with cranked tops carrying barbed strands, chain-link between, coil on
  // top; lamps on every third post (lamp tops listed in L._fenceLamps for the glow)
  function FENCE3(x0, x1, y, h, o = {}) {
    const gap = o.gap ?? 240, lamps = [], dark = o.dark; let posts = "", mesh = `<rect x="${x0}" y="${y - h}" width="${x1 - x0}" height="${h}" fill="url(#fMesh)" opacity="${dark ? 0.55 : 0.9}"/>`;
    for (let x = x0, k = 0; x <= x1; x += gap, k++) {
      posts += `<rect x="${x - 14}" y="${y - h - 10}" width="28" height="${h + 10}" fill="${dark ? "#4a525e" : "#d4cfc2"}" ${O(3)}/><path d="M${x},${y - h - 8}l38,-46" stroke="${dark ? "#4a525e" : "#9aa0a6"}" stroke-width="9"/>`;
      if (o.lamps && k % 3 === 1) { lamps.push([x + 6, y - h - 40]); posts += `<rect x="${x - 26}" y="${y - h - 54}" width="52" height="24" rx="6" fill="${dark ? "#1e2430" : "#5b6066"}" ${O(2.5)}/><rect x="${x - 20}" y="${y - h - 34}" width="40" height="8" rx="3" fill="#fffbe8"/>`; }
    }
    const strands = [0, 1, 2].map((j) => `<path d="M${x0 + 16 + j * 13},${y - h - 18 - j * 15}H${x1 + 16 + j * 13}" stroke="${dark ? "#5a626e" : "#7d868c"}" stroke-width="2.4"/>`).join("");
    const coil = window.Dress ? Dress.barbed(x0, x1, y - h - 4, o.coil ?? 22, Math.abs(x0 | 0) + 89) : "";
    return { svg: `<g>${mesh}<path d="M${x0},${y - h}H${x1}M${x0},${y - 10}H${x1}" stroke="${dark ? "#4a525e" : "#9aa0a6"}" stroke-width="6"/>${posts}${strands}${coil}</g>`, lamps };
  }
  // the guard tower: four legs, a sandbagged platform at height h (its floor y - h is where the guard stands), a tin roof, a floodlight
  const GTOWER = (x, y, h, dark, lit) => `<g transform="translate(${x},${y})"><path d="M-110,0L-90,${-h}M110,0L90,${-h}M-104,${-h * 0.35}H104M-96,${-h * 0.7}H96M-104,${-h * 0.35}L96,${-h * 0.7}M104,${-h * 0.35}L-96,${-h * 0.7}" stroke="${dark ? "#2a3040" : "#6b5a44"}" stroke-width="14" fill="none"/>
    <rect x="-140" y="${-h - 12}" width="280" height="24" fill="${dark ? "#2a3040" : "#8a6a44"}" ${O(3)}/>
    ${Array.from({ length: 6 }, (_, k) => `<rect x="${-136 + k * 46}" y="${-h - 70}" width="48" height="30" rx="12" fill="${dark ? "#3a3a32" : "#b49a6a"}" ${O(3)}/><rect x="${-130 + k * 46 + (k % 2) * 10}" y="${-h - 42}" width="48" height="30" rx="12" fill="${dark ? "#34342c" : "#a88e60"}" ${O(3)}/>`).join("")}
    <path d="M-96,${-h - 70}V${-h - 300}M96,${-h - 70}V${-h - 300}" stroke="${dark ? "#2a3040" : "#6b5a44"}" stroke-width="10"/><path d="M-170,${-h - 290}L0,${-h - 360}L170,${-h - 290}Z" fill="${dark ? "#3a4252" : "#9aa4ab"}" ${OUT}/>
    <g transform="translate(120,${-h - 300}) rotate(28)"><rect x="-30" y="-20" width="60" height="40" rx="8" fill="${dark ? "#1e2430" : "#3a3f45"}" ${O(3)}/><rect x="28" y="-16" width="8" height="32" fill="${lit ? "#fffbe8" : "#c9d0d4"}"/></g></g>`;
  // the tower's sandbag parapet alone, to lay over a guard standing on the platform (same geometry as GTOWER)
  const PARAPET = (x, y, h, dark) => `<g transform="translate(${x},${y})">${Array.from({ length: 6 }, (_, k) => `<rect x="${-136 + k * 46}" y="${-h - 70}" width="48" height="30" rx="12" fill="${dark ? "#3a3a32" : "#b49a6a"}" ${O(3)}/><rect x="${-130 + k * 46 + (k % 2) * 10}" y="${-h - 42}" width="48" height="30" rx="12" fill="${dark ? "#34342c" : "#a88e60"}" ${O(3)}/>`).join("")}<rect x="-140" y="${-h - 12}" width="280" height="24" fill="${dark ? "#2a3040" : "#8a6a44"}" ${O(3)}/></g>`;
  // an enamel/painted sign: a rounded plate with one or two lines of text
  const PLATE = (x, y, w, h, lines, o = {}) => `<g transform="translate(${x},${y}) rotate(${o.rot || 0})"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="${o.rx ?? 10}" fill="${o.bg || "#f4f2ea"}" ${O(3)}/><rect x="${-w / 2 + 8}" y="${-h / 2 + 8}" width="${w - 16}" height="${h - 16}" rx="${(o.rx ?? 10) * 0.6}" fill="none" stroke="${o.fg || "#c8392b"}" stroke-width="4"/>
    ${lines.map((t, k) => T(0, f1(-h / 2 + (k + 1) * h / (lines.length + 1) + (o.size || 34) * 0.36), t, o.size || 34, o.fg || "#c8392b")).join("")}${o.rust ? `<path d="M${-w / 2 + 10},${h / 2 - 8}h${w * 0.3}l-10,-${h * 0.3}z" fill="url(#dRust)"/>` : ""}</g>`;
  // the canteen table seen from the front at y (top edge), x0 → x1: steel trays of rice and curry, cups, a jug — goes over seated rigs
  function TABLEF(x0, x1, y, o = {}) {
    const r = mk(o.seed || 31), n = Math.floor((x1 - x0) / 240);
    let s = `<g><path d="M${x0 - 20},${y}L${x0 + 30},${y - 60}H${x1 - 30}L${x1 + 20},${y}Z" fill="#c9cfd2" ${OUT}/><path d="M${x0 - 20},${y}H${x1 + 20}V${y + 36}H${x0 - 20}Z" fill="#8d969d" ${OUT}/>`;
    for (let k = 0; k < n; k++) { const cx = x0 + 120 + k * 240 + (r() - 0.5) * 30;
      s += `<g transform="translate(${f1(cx)},${y - 28})"><path d="M-70,0L-60,-22H60L70,0Z" fill="#b9c0c6" ${O(3)}/><ellipse cx="-22" cy="-16" rx="28" ry="8" fill="#f4f0e2"/><ellipse cx="26" cy="-16" rx="24" ry="7" fill="${["#c8762a", "#6a8a3a", "#b8463a"][k % 3]}"/></g>`;
      if (r() < 0.6) s += `<g transform="translate(${f1(cx + 90)},${y - 30})"><path d="M-14,0L-16,-40H16L14,0Z" fill="url(#eSteel)" ${O(2.5)}/></g>`; }
    s += `<path d="M${x0 + 10},${y + 36}V${y + 230}M${x1 - 10},${y + 36}V${y + 230}" stroke="#5b6066" stroke-width="14"/></g>`;
    return s;
  }
  // the registration table outside the office: folding table, the register (open), a rubber stamp and ink pad, name tags; origin = floor centre
  const REGTABLE = (id, x, y, s = 1) => `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><ellipse cx="10" cy="4" rx="320" ry="24" fill="#000" opacity=".2"/><path d="M-260,-6L-240,-200M260,-6L240,-200M-240,-160L240,-110M240,-160L-240,-110" stroke="#5b6066" stroke-width="10"/>
    <path d="M-300,-230L-270,-262H270L300,-230Z" fill="#e8e2d4" ${OUT}/><rect x="-300" y="-232" width="600" height="28" fill="#c9c2b2" ${OUT}/>
    <g transform="translate(-60,-246)"><path d="M-110,0L-96,-24H0L4,0Z" fill="#f7f1e2" ${O(2.5)}/><path d="M4,0L8,-24H104L118,0Z" fill="#f4ecd8" ${O(2.5)}/><path d="M-90,-14h80M-86,-8h70M14,-14h84M18,-8h70" stroke="#5b6066" stroke-width="2"/></g>
    <g transform="translate(150,-250)"><rect x="-26" y="-8" width="52" height="12" rx="3" fill="#c8392b" ${O(2)}/><rect x="-10" y="-40" width="20" height="34" rx="6" fill="#6b4a2e" ${O(2)}/></g><rect x="200" y="-256" width="60" height="14" rx="3" fill="#2f4a8a" ${O(2)}/>
    ${[0, 1, 2].map((k) => `<rect x="${-250 + k * 26}" y="${-258 - k * 3}" width="44" height="28" rx="3" fill="#f4f2ea" ${O(2)}/><rect x="${-250 + k * 26}" y="${-258 - k * 3}" width="44" height="8" fill="#c8392b"/>`).join("")}
    <path d="M-300,-204H300" stroke="${INK}" stroke-width="3"/></g>`;
  window.Estate = { BLEACH, ACID, BUCKETR, GAS, SAW, WTOWER, CHIMNEY, LAMPPOST, FENCE3, GTOWER, PARAPET, PLATE, TABLEF, REGTABLE };

  // the estate on the horizon in local coordinates (fence foot y = 0, gate at x = 0, ±1700 wide): factories with panels and lit
  // clerestories, the office, water tower, chimney, the fence with its lamps, the corner towers, the gate pillars and floodlights
  function skyline(r, o = {}) {
    const dark = o.dark, lit = true;
    let s = CHIMNEY(-260, -40, 760, 1, dark) + WTOWER(820, -40, 0.95, dark);
    s += SAW(-1560, -40, 820, 270, 5, { lit, dark }) + SAW(-640, -40, 820, 320, 6, { lit, dark }) + SAW(300, -40, 980, 290, 7, { lit, dark });
    s += `<rect x="1330" y="-270" width="330" height="230" fill="url(#${dark ? "eZincN" : "eZinc"})" ${OUT}/><path d="M1320,-270H1670" stroke="${INK}" stroke-width="8"/>`;
    s += `<g><rect x="-420" y="-300" width="400" height="260" fill="${dark ? "#3a4252" : "#e8e2d4"}" ${OUT}/>${[0, 1].map((j) => [0, 1, 2, 3].map((i) => `<rect x="${-396 + i * 96}" y="${-280 + j * 120}" width="70" height="70" fill="url(#eWarm)" ${O(3)}/>`).join("")).join("")}</g>`;
    const F = FENCE3(-1720, 1720, 0, 170, { gap: 150, lamps: true, dark, coil: 14 });
    s += F.svg + GTOWER(-1640, 0, 260, dark, true) + GTOWER(1640, 0, 260, dark, true);
    s += `<rect x="-130" y="-300" width="60" height="300" fill="${dark ? "#4a525e" : "#d4cfc2"}" ${O(3)}/><rect x="70" y="-300" width="60" height="300" fill="${dark ? "#4a525e" : "#d4cfc2"}" ${O(3)}/><rect x="-140" y="-350" width="280" height="56" fill="#2f4a8a" ${O(3)}/>${T(0, -312, "นิคมอุตสาหกรรม", 28, "#f4ecd8")}`;
    s += `<path d="M-70,-6H70" stroke="#5b6066" stroke-width="8"/>${Array.from({ length: 8 }, (_, k) => `<path d="M${-64 + k * 18},-10V-210" stroke="#5b6066" stroke-width="5"/>`).join("")}`;
    s += [-1100, -400, 420, 1100].map((x) => LAMPPOST(x, 0, 380, true, dark)).join("");
    return { svg: s, lamps: F.lamps.concat([[-1100 + 110, -370], [-400 + 110, -370], [420 + 110, -370], [1100 + 110, -370], [-1640 + 140, -580], [1640 + 140, -580]]) };
  }

  // ======================================================================================================
  // 1. the hook, first person: a filthy washroom, a squat toilet, the red bucket, a bottle in each hand (ยายจันทร์'s hands)
  // ids: #id-hl / #id-hr (the hands with their bottles), #id-sl / #id-sr (the pour, hidden), #id-gas (the cloud, hidden)
  // ======================================================================================================
  function washroomPov(L, o = {}) {
    const id = o.id || "wp", r = mk(o.seed || 61), skin = o.skin || "#c99a74", sleeve = o.sleeve || "#9a6aa8";
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#2a2c28"/>`);
    let w = `<rect x="-1400" y="-900" width="4000" height="1920" fill="url(#eTileW)"/><rect x="-1400" y="-900" width="4000" height="1920" fill="url(#dGrime)"/>`;
    w += `<g transform="translate(780,150)"><rect x="-160" y="-110" width="320" height="220" fill="#fff6dc" ${OUT}/>${Array.from({ length: 6 }, (_, k) => `<path d="M-150,${-88 + k * 36}h300" stroke="#c9cfc8" stroke-width="15"/><path d="M-150,${-82 + k * 36}h300" stroke="#fff" stroke-width="3" opacity=".6"/>`).join("")}<rect x="-160" y="-110" width="320" height="220" fill="none" stroke="#8d969d" stroke-width="12"/></g>`;
    w += `<path d="M-1400,520H2600" stroke="#8d969d" stroke-width="24"/><path d="M-1400,512H2600" stroke="#d3d9dd" stroke-width="5"/>${[-200, 600, 1500].map((x) => `<rect x="${x}" y="500" width="24" height="44" fill="#6f7880"/>`).join("")}`;
    w += `<g transform="translate(330,640)"><rect x="-110" y="-80" width="220" height="150" rx="12" fill="#e8ece6" ${OUT}/><rect x="56" y="-102" width="44" height="24" rx="6" fill="#c9d0d5" ${O(3)}/><path d="M-60,70V380" stroke="#c9d0d5" stroke-width="18"/><path d="M-90,20h180" stroke="#c9cfc8" stroke-width="4"/>${Dress ? Dress.streak(-90, 70, 50, 300, 0.7) : ""}</g>`;
    w += `<rect x="-1400" y="930" width="4000" height="90" fill="#9aa39a" opacity=".55"/><path d="M-1400,1020H2600" stroke="#4a4a40" stroke-width="10"/>`;
    if (dressed(o)) w += [[-300, 0.8], [140, 0.6], [560, 0.7], [1180, 0.8], [1600, 0.6]].map(([x, op]) => Dress.streak(x, 560, 70 + r() * 60, 460, op)).join("") + Array.from({ length: 40 }, () => `<circle cx="${f1(-900 + r() * 2600)}" cy="${f1(900 + r() * 110)}" r="${f1(3 + r() * 8)}" fill="#3a4a2a" opacity="${f1(0.25 + r() * 0.35)}"/>`).join("");
    put(L.far, w);
    // the floor: tiles in perspective toward a vanishing point high above, wet patches, a drain, the toilet pan, the bucket
    const vx = 540, vy = -1500; let s = `<path d="M-1400,1020H2600V2800H-1400Z" fill="#b8b7ad"/>`;
    for (let j = -16; j <= 22; j++) { const xb = -1400 + j * 150, t = (2800 - vy) / (1020 - vy), xe = vx + (xb - vx) * t; s += `<path d="M${f1(xb)},1020L${f1(xe)},2800" stroke="#6c6b63" stroke-width="3"/>`; }
    for (let k = 1; k < 16; k++) { const y = 1020 + 40 * k + 5 * k * k; s += `<path d="M-1400,${f1(y)}H2600" stroke="#6c6b63" stroke-width="${f1(2 + k * 0.25)}"/>`; }
    s += `<rect x="-1400" y="1020" width="4000" height="1800" fill="url(#dGrime)" opacity=".8"/>`;
    s += [[160, 1420, 210, 40], [880, 1760, 260, 50], [-120, 1900, 200, 44], [640, 1290, 150, 26]].map(([x, y, a, b]) => `<ellipse cx="${x}" cy="${y}" rx="${a}" ry="${b}" fill="#d9dfe0" opacity=".35"/><ellipse cx="${x - a * 0.3}" cy="${y - b * 0.3}" rx="${a * 0.3}" ry="${b * 0.18}" fill="#fff" opacity=".35"/>`).join("");
    s += `<g transform="translate(200,1640)"><ellipse rx="90" ry="34" fill="#8d969d" ${O(3)}/>${Array.from({ length: 6 }, (_, k) => `<path d="M${-62 + k * 25},-22v44" stroke="#4a4f55" stroke-width="5"/>`).join("")}<ellipse rx="90" ry="34" fill="none" stroke="#3a3f45" stroke-width="3"/></g>`;
    // the squat pan, in the floor: ceramic surround, ridged foot pads, the bowl, water in the trap, a brown ring
    s += `<g transform="translate(470,1200)"><ellipse rx="230" ry="96" fill="#eef1ee" ${OUT}/><path d="M-200,-10q-10,-40 30,-56h70q-20,30 -16,66zM200,-10q10,-40 -30,-56h-70q20,30 16,66z" fill="#dfe4e1" ${O(3)}/>
      ${[0, 1, 2, 3].map((k) => `<path d="M${-176 + k * 18},-46l10,40M${176 - k * 18},-46l-10,40" stroke="#b9c2bf" stroke-width="5"/>`).join("")}
      <ellipse cx="0" cy="10" rx="120" ry="58" fill="#cdd5d3" ${O(3)}/><ellipse cx="0" cy="12" rx="104" ry="46" fill="none" stroke="#a5824a" stroke-width="9" opacity=".45"/><ellipse cx="30" cy="26" rx="46" ry="22" fill="#3c4c4e"/><ellipse cx="30" cy="26" rx="46" ry="22" fill="#86a8b0" opacity=".45"/><path d="M-80,-20q40,-16 90,-8" stroke="#fff" stroke-width="5" opacity=".6" fill="none"/></g>`;
    if (dressed(o)) s += Array.from({ length: 26 }, () => `<circle cx="${f1(-700 + r() * 2400)}" cy="${f1(1060 + r() * 1600)}" r="${f1(2 + r() * 6)}" fill="#4a3a20" opacity="${f1(0.15 + r() * 0.25)}"/>`).join("") + `<path d="M760,1100q60,30 40,90" stroke="#5a4a2a" stroke-width="10" opacity=".25" fill="none"/>`;
    s += `<g transform="translate(560,1900) scale(2.1)">${BUCKETR(`${id}-bk`, { scoop: true })}</g>`;
    put(L.set, s);
    // our hands, on the shoulders of the bottles so the labels read; each group's origin is the hand (the pour pivots there)
    const grip = Hand.grip({ skin, sleeve, skinS: "#a57a56", sleeveS: "#7a4a88" });
    put(L.act, `<g id="${id}-hl" transform="translate(330,1150) rotate(-6)"><g transform="scale(1.45)"><g transform="translate(62,175)">${BLEACH(`${id}-jug`)}</g><g transform="scale(0.55)">${grip}</g></g></g>
      <g id="${id}-hr" transform="translate(750,1100) rotate(6)"><g transform="scale(1.45)"><g transform="translate(-50,190)">${ACID(`${id}-acid`)}</g><g transform="scale(-0.55,0.55)">${grip}</g></g></g>`);
    put(L.glow, `<g id="${id}-gas" opacity="0">${[[560, 1500, 260], [470, 1380, 200], [660, 1340, 220], [560, 1220, 260], [420, 1120, 200], [700, 1080, 240]].map(([x, y, rr]) => `<ellipse class="egb" cx="${x}" cy="${y}" rx="${rr}" ry="${rr * 0.55}" fill="url(#eGasR)"/>`).join("")}</g>
      <circle cx="780" cy="150" r="420" fill="url(#eFlood)" opacity=".35"/>`);
  }

  // ======================================================================================================
  // 2. the estate from the access road at dawn: paddies, the road straight to the gate, the estate on the horizon with every lamp lit
  // ======================================================================================================
  function estateFar(L, o = {}) {
    const id = o.id || "ef", t = o.time || "morning", r = mk(o.seed || 63), night = t === "night";
    sky(L, t);
    if (night) stars(L, 7); else put(L.sky, `<circle cx="${o.sunX ?? 1180}" cy="1060" r="560" fill="url(#fSun)" opacity=".9"/><circle cx="${o.sunX ?? 1180}" cy="1080" r="90" fill="#fff2c0" opacity=".95"/>`
      + Array.from({ length: 8 }, () => { const x = -900 + r() * 2800, y = 100 + r() * 700, w = 260 + r() * 520; return `<g opacity="${f1(0.45 + r() * 0.35)}"><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(16 + r() * 18)}" fill="#8a7a9a"/><ellipse cx="${f1(x + w * 0.12)}" cy="${f1(y + 8)}" rx="${f1(w * 0.75)}" ry="${f1(7 + r() * 6)}" fill="#ffc89a" opacity=".75"/></g>`; }).join(""));
    put(L.far, Fence.paddies(r, night ? "night" : "morning", 1150));
    const SK = skyline(r, { dark: night });
    put(L.mid, `<g transform="translate(540,1150) scale(0.5)">${SK.svg}</g>`);
    put(L.glow, SK.lamps.map(([x, y]) => `<circle cx="${f1(540 + x * 0.5 * 0.6)}" cy="${f1(1150 + y * 0.5 * 0.6)}" r="34" fill="url(#eFlood)" opacity=".8"/>`).join(""));
    // the access road (set): straight to the gate, a broken centre line, cracked edges, grass verges and paddies, poles converging
    const vx = 540, vy = 1150; let s = `<rect x="-1400" y="1150" width="4000" height="1700" fill="#7f9c50"/>`;
    for (let k = 0; k < 9; k++) { const y = 1160 + k * k * 16 + k * 20; s += `<path d="M-1400,${y}H2600" stroke="#cfe0ea" stroke-width="${2 + k}" opacity=".5"/>`; }
    s += `<path d="M${vx - 40},${vy}L${vx + 40},${vy}L1500,2800L-420,2800Z" fill="url(#rAsph)" ${O(3)}/>`;
    for (let k = 0; k < 9; k++) { const a = k / 9, b = (k + 0.5) / 9, y0 = vy + (2800 - vy) * a * a, y1 = vy + (2800 - vy) * b * b; s += `<path d="M${vx},${f1(y0)}L${vx + (y1 - vy) * 0.03},${f1(y1)}" stroke="#f4ecd8" stroke-width="${f1(3 + 30 * b)}" opacity=".8"/>`; }
    s += `<path d="M${vx - 40},${vy}L-420,2800M${vx + 40},${vy}L1500,2800" stroke="#e8b830" stroke-width="10" opacity=".75"/>`;
    for (let k = 0; k < 6; k++) { const a = (k + 1) / 7, y = vy + (2800 - vy) * a * a, h = 40 + 900 * a * a, xl = vx - 120 - (y - vy) * 1.3, xr = vx + 120 + (y - vy) * 1.3;
      s += `<path d="M${f1(xl)},${f1(y)}V${f1(y - h)}M${f1(xl - h * 0.12)},${f1(y - h * 0.92)}H${f1(xl + h * 0.12)}" stroke="#6b5a44" stroke-width="${f1(2 + 10 * a)}" fill="none"/><path d="M${f1(xr)},${f1(y)}V${f1(y - h)}M${f1(xr - h * 0.12)},${f1(y - h * 0.92)}H${f1(xr + h * 0.12)}" stroke="#6b5a44" stroke-width="${f1(2 + 10 * a)}" fill="none"/>`; }
    if (dressed(o)) s += Dress.tufts(-1300, 300, 1700, 2700, 26, 501, 70) + Dress.tufts(900, 2500, 1700, 2700, 26, 503, 70) + `<g transform="translate(1320,1720) rotate(8)">${Road.CAR(0, 0, 1.1, "#c8c2b4", { smash: true })}</g>`
      + PLATE(-60, 1560, 300, 120, ["นิคมฯ 1 กม."], { bg: "#1f6b46", fg: "#f4ecd8", size: 40, rot: -3 }) + `<path d="M-120,1620V1800M0,1620V1800" stroke="#8d9299" stroke-width="12"/>`;
    put(L.set, s);
    if (!night) put(L.glow, `<rect x="-1400" y="700" width="4000" height="1000" fill="#ffb070" opacity=".1"/>`);
  }

  // ======================================================================================================
  // 3. the gate: a sliding steel gate between concrete pillars, the arch "นิคมอุตสาหกรรม", a cloth banner "ทุกคนต้องมีประโยชน์",
  // the three-metre fence with coil on top, the guard tower on the left (platform floor at y = 1500 - th), sandbags, floodlights.
  // o.open 0..1 slides #id-gate right behind the right-hand fence; o.inside = we stand inside at night looking out at the dark road.
  // ======================================================================================================
  function estateGate(L, o = {}) {
    const id = o.id || "eg", t = o.time || "morning", r = mk(o.seed || 65), night = t === "night", G = 1500, th = o.towerH ?? 760;
    sky(L, t); if (night) stars(L, 9);
    if (o.inside) {   // beyond the bars: the dark road away from the estate, dead trees, the shapes that wait
      put(L.far, `${Fence.paddies(r, "night", 1180)}<path d="M470,1180L610,1180L900,1560L180,1560Z" fill="#20242a"/>`);
      put(L.mid, `<g opacity=".9">${[[-260, 1210, 0.9], [130, 1236, 1.1], [820, 1222, 1], [1180, 1250, 1.2], [1500, 1214, 0.8]].map(([x, y, s2]) => `<g transform="translate(${x},${y}) scale(${s2})"><path d="M0,0V-180M0,-120l-40,-50M0,-90l50,-60M0,-150l-20,-40" stroke="#141820" stroke-width="10" fill="none" stroke-linecap="round"/></g>`).join("")}</g>`);
    } else {
      put(L.far, `${Fence.paddies(r, night ? "night" : "morning", 1060)}<g transform="translate(540,1080) scale(0.42)">${skyline(r, { dark: night }).svg}</g>`);
      // the yard inside, seen through the bars (mid): a factory front, lamp posts, a parked forklift
      put(L.mid, `<rect x="-1400" y="1200" width="4000" height="400" fill="url(#fConc)"/>${SAW(-700, 1220, 1500, 360, 6, { lit: true, dark: night, windows: true })}${LAMPPOST(-200, 1260, 420, true, night)}${LAMPPOST(1300, 1260, 420, true, night)}<path d="M-1400,1300H2600" stroke="#e8b830" stroke-width="8" opacity=".7"/>`);
    }
    // the set: asphalt apron, a speed bump, the fences, the pillars + arch + banner, the gate, the tower
    let s = `<rect x="-1400" y="${G - 10}" width="4000" height="1400" fill="url(#rAsph)"/><path d="M-1400,${G + 120}H2600" stroke="#e8b830" stroke-width="10" stroke-dasharray="90 60"/><rect x="60" y="${G + 240}" width="960" height="34" rx="14" fill="#e8b830" ${O(3)}/>${Array.from({ length: 8 }, (_, k) => `<path d="M${90 + k * 120},${G + 244}l40,26" stroke="#2e2a26" stroke-width="12"/>`).join("")}`;
    const FL = FENCE3(-1400, -60, G, 980, { gap: 260, lamps: true, dark: night, coil: 26 }), FR = FENCE3(1140, 2600, G, 980, { gap: 260, lamps: true, dark: night, coil: 26 });
    s += FL.svg;
    // the gate (slides right, behind the right fence): frame, bars, a diagonal, a wheel track
    s += `<path d="M60,${G + 6}H2000" stroke="#4a4f55" stroke-width="10"/><g id="${id}-gate" transform="translate(${(o.open || 0) * 960},0)"><rect x="80" y="${G - 900}" width="920" height="900" fill="none" stroke="${night ? "#3a4250" : "#5b6066"}" stroke-width="22"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${120 + k * 64},${G - 890}V${G - 10}" stroke="${night ? "#3a4250" : "#6f7880"}" stroke-width="12"/><path d="M${116 + k * 64},${G - 890}V${G - 10}" stroke="${night ? "#5a6270" : "#a7b0b6"}" stroke-width="3"/>`).join("")}
      <path d="M80,${G - 450}H1000M80,${G - 840}H1000" stroke="${night ? "#3a4250" : "#5b6066"}" stroke-width="16"/><path d="M90,${G - 20}L990,${G - 440}" stroke="${night ? "#3a4250" : "#5b6066"}" stroke-width="12"/>
      ${[160, 900].map((x) => `<circle cx="${x}" cy="${G - 4}" r="22" fill="#2a2c2e" ${O(3)}/>`).join("")}<rect x="120" y="${G - 520}" width="140" height="60" rx="6" fill="#c8392b" ${O(3)}/>${T(190, G - 478, "หยุด", 36, "#fff")}${dressed(o) ? Dress.rust(180, G - 880, 30, 300) + Dress.rust(720, G - 430, 26, 260) : ""}</g>`;
    s += FR.svg;
    // pillars + arch + banner
    const pil = (x) => `<rect x="${x - 70}" y="${G - 1120}" width="140" height="1120" fill="${night ? "#4a525e" : "#d4cfc2"}" ${OUT}/><rect x="${x - 70}" y="${G - 1120}" width="140" height="1120" fill="url(#dConc)" opacity=".8"/><rect x="${x - 84}" y="${G - 1140}" width="168" height="34" fill="${night ? "#3a4250" : "#b9b2a2"}" ${O(3)}/><path d="M${x - 60},${G - 300}h120" stroke="#000" stroke-opacity=".15" stroke-width="40"/>`;
    s += pil(40) + pil(1040);
    s += `<rect x="-20" y="${G - 1260}" width="1120" height="130" fill="#2f4a8a" ${OUT}/><rect x="-6" y="${G - 1246}" width="1092" height="102" fill="none" stroke="#f4ecd8" stroke-width="4"/>${T(540, G - 1172, "นิคมอุตสาหกรรม", 70, "#f4ecd8")}`;
    s += `<g class="laundry"><path d="M110,${G - 1110}Q540,${G - 1060} 970,${G - 1110}L960,${G - 980}Q540,${G - 930} 120,${G - 980}Z" fill="#f2efe6" ${O(3)}/><path d="M960,${G - 980}l-14,18l-6,-16M120,${G - 980}l18,16l4,-14" stroke="${INK}" stroke-width="3" fill="none"/>
      ${T(540, G - 1012, "ทุกคนต้องมีประโยชน์", 60, "#c8392b", { extra: ' transform="rotate(-1 540 ' + (G - 1012) + ')"' })}<path d="M220,${G - 1000}q80,-10 120,4M700,${G - 1004}q60,8 110,-4" stroke="#c8392b" stroke-width="4" opacity=".5" fill="none"/></g>`;
    // the floodlights on the pillars
    s += [40, 1040].map((x) => `<g transform="translate(${x},${G - 1150})"><rect x="-30" y="-50" width="60" height="40" rx="8" fill="#3a3f45" ${O(3)}/><rect x="-24" y="-14" width="48" height="10" rx="4" fill="#fffbe8"/></g>`).join("");
    // sandbags at the pillar feet; the guard tower on the left
    if (window.Dress) s += Dress.sandbags(-170, G + 10, 0.9, 3, 2, 71) + Dress.sandbags(1240, G + 10, 0.9, 3, 2, 73);
    s += GTOWER(-380, G, th, night, true);
    if (dressed(o)) s += `<g opacity=".9">${Dress.weeds(-1400, 2600, G + 4, 509, 40)}</g>` + Dress.crack(300, G + 60, 120, 10, 0.45) + Dress.crack(1400, G + 140, 140, -20, 0.4);
    put(L.set, s);
    const lamps = FL.lamps.concat(FR.lamps).concat([[40, G - 1150], [1040, G - 1150], [-380 + 120, G - th - 300]]);
    put(L.glow, lamps.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="${night ? 220 : 90}" fill="url(#eFlood)" opacity="${night ? 0.95 : 0.6}"/>`).join("") + (night ? `<path d="M40,${G - 1140}L-160,${G}H360Z M1040,${G - 1140}L760,${G}H1280Z" fill="url(#eBeam)"/>` : `<rect x="-1400" y="600" width="4000" height="1200" fill="#ffb070" opacity=".08"/>`));
    if (night) put(L.set, `<ellipse cx="540" cy="${G + 120}" rx="760" ry="120" fill="#fff2c8" opacity=".14"/>`);
  }

  // ======================================================================================================
  // 4. the yard inside: washroom block (left, door #id-wdoor), office (centre, คุณวิน's window #id-winw on the first floor),
  // factory (right, roller door open), lamp posts, laundry, vegetable beds; ground line of the buildings y = 1240, actors ~1520
  // ======================================================================================================
  function estateYard(L, o = {}) {
    const id = o.id || "ey", t = o.time || "day", r = mk(o.seed || 67), night = t === "night", B = 1240;
    sky(L, t === "morning" ? "morning" : t); if (night) stars(L, 11);
    put(L.far, `${Fence.paddies(r, night ? "night" : t === "morning" ? "morning" : "day", 1000)}`);
    // mid: the rest of the estate behind — roofs with panels, the water tower, the chimney, the perimeter fence and its lamps
    const F = FENCE3(-1400, 2600, 1090, 120, { gap: 160, lamps: true, dark: night, coil: 12 });
    put(L.mid, `${CHIMNEY(140, 1080, 620, 0.8, night)}${WTOWER(1500, 1080, 0.7, night)}${SAW(-1300, 1080, 900, 200, 5, { lit: night, dark: night, windows: false })}${SAW(1800, 1080, 800, 210, 5, { lit: night, dark: night, windows: false })}${F.svg}${GTOWER(2300, 1090, 300, night, true)}`);
    if (night) put(L.glow, F.lamps.map(([x, y]) => `<circle cx="${f1(x * 0.6 + 216)}" cy="${f1(y * 0.6 + 384)}" r="60" fill="url(#eFlood)" opacity=".8"/>`).join(""));
    const wall = night ? "#4a4e58" : "url(#eCream)", glass = night ? "url(#eWarm)" : "#7f9aa6";
    let s = `<rect x="-1400" y="${B}" width="4000" height="1600" fill="${night ? "#3a3e46" : "url(#fConc)"}"/>${Array.from({ length: 11 }, (_, k) => `<path d="M${-1400 + k * 400},${B}L${-1700 + k * 520},2800" stroke="${night ? "#2a2e36" : "#a9a397"}" stroke-width="4"/>`).join("")}<path d="M-1400,1800H2600M-1400,2300H2600" stroke="${night ? "#2a2e36" : "#a9a397"}" stroke-width="4"/>`;
    s += `<path d="M-1400,${B + 70}H2600M-1400,${B + 112}H2600" stroke="#e8b830" stroke-width="9" opacity="${night ? 0.4 : 0.85}"/><rect x="-1400" y="${B}" width="4000" height="26" fill="#6f7880" opacity=".7"/>${Array.from({ length: 40 }, (_, k) => `<path d="M${-1400 + k * 100},${B + 4}v18" stroke="#3a3f45" stroke-width="5"/>`).join("")}`;
    // washroom block
    s += `<g><rect x="-1400" y="${B - 420}" width="1020" height="420" fill="${wall}" ${OUT}/><rect x="-1410" y="${B - 440}" width="1040" height="30" fill="${night ? "#3a3e46" : "#9aa4ab"}" ${O(3)}/>
      ${[-1300, -1150, -640, -490].map((x) => `<rect x="${x}" y="${B - 360}" width="110" height="70" fill="${night ? "#2a3040" : "#9fb8c0"}" ${O(3)}/>${[0, 1, 2, 3].map((k) => `<path d="M${x + 4},${B - 352 + k * 17}h102" stroke="${night ? "#4a5260" : "#e8ece6"}" stroke-width="7"/>`).join("")}`).join("")}
      <rect x="-900" y="${B - 320}" width="170" height="320" fill="#3a3530" ${O(3)}/><g id="${id}-wdoor"><rect x="-900" y="${B - 320}" width="170" height="320" fill="${night ? "#5a5248" : "#8a6a44"}" ${O(3)}/><rect x="-880" y="${B - 300}" width="130" height="120" fill="#000" opacity=".12"/><circle cx="-748" cy="${B - 160}" r="8" fill="#c9a55a"/></g>
      ${PLATE(-815, B - 372, 230, 52, ["ห้องน้ำรวม"], { bg: "#2f4a8a", fg: "#f4ecd8", size: 32, rx: 6 })}
      <g transform="translate(-560,${B})"><rect x="-60" y="-110" width="120" height="110" fill="#b3ada0" ${O(3)}/><path d="M-30,-200V-130h40" stroke="#8d969d" stroke-width="10" fill="none"/><rect x="2" y="-140" width="20" height="16" rx="4" fill="#c9a55a"/></g>${window.Dress ? Dress.broom(-1050, B, 1, -10) + Dress.bucket(-980, B + 10, 0.9, "#c8392b") : ""}</g>`;
    // office: two storeys, glass door, first-floor windows with blinds; #id-winw = คุณวิน's
    s += `<g><rect x="-320" y="${B - 760}" width="1240" height="760" fill="${wall}" ${OUT}/><rect x="-340" y="${B - 790}" width="1280" height="40" fill="${night ? "#3a3e46" : "#b3ada0"}" ${O(3)}/><path d="M-320,${B - 380}H920" stroke="${night ? "#3a3e46" : "#c9c2b2"}" stroke-width="16"/>
      ${[-260, 520].map((x) => `<rect x="${x}" y="${B - 300}" width="300" height="160" fill="${glass}" ${O(3)}/><path d="M${x + 150},${B - 300}v160" stroke="${INK}" stroke-width="4"/>`).join("")}
      <rect x="200" y="${B - 300}" width="200" height="300" fill="${night ? "#3a3530" : "#5b7a86"}" ${O(3)}/><path d="M300,${B - 300}V${B}" stroke="${INK}" stroke-width="4"/><path d="M220,${B - 280}l40,240M320,${B - 280}l40,240" stroke="#fff" stroke-opacity=".25" stroke-width="6"/>${PLATE(300, B - 336, 200, 46, ["สำนักงาน"], { bg: "#f4f2ea", fg: "#2f4a8a", size: 28, rx: 6 })}
      ${[[-260, 0], [120, 1], [560, 0]].map(([x, me]) => `<g ${me ? `id="${id}-winw"` : ""}><rect x="${x}" y="${B - 680}" width="${me ? 260 : 300}" height="180" fill="${me && night ? "url(#eWarm)" : glass}" ${O(3)}/>${Array.from({ length: 6 }, (_, k) => `<path d="M${x + 4},${B - 668 + k * 28}h${me ? 252 : 292}" stroke="${night ? (me ? "#c98a3a" : "#c99a4a") : "#c9d0d4"}" stroke-width="6" opacity=".8"/>`).join("")}</g>`).join("")}
      <rect x="760" y="${B - 470}" width="110" height="70" fill="#d9d6cc" ${O(3)}/><path d="M770,${B - 455}h90M770,${B - 440}h90M770,${B - 425}h90" stroke="#8d969d" stroke-width="3"/>
      <g transform="translate(-200,${B - 440})"><rect x="-100" y="-50" width="200" height="110" fill="#6b4a2e" ${O(3)}/><rect x="-90" y="-40" width="180" height="90" fill="#d9cfb8"/>${[0, 1, 2, 3, 4].map((k) => `<rect x="${-80 + (k % 3) * 58}" y="${-32 + Math.floor(k / 3) * 44}" width="48" height="36" fill="#f4f2ea" stroke="#8d969d" stroke-width="1.5" transform="rotate(${(k % 2 ? 4 : -3)} ${-56 + (k % 3) * 58} ${-14 + Math.floor(k / 3) * 44})"/>`).join("")}</g></g>`;
    // factory: saw-tooth with panels, roller door open onto the machines, banner, a strip of windows
    s += `<g>${SAW(980, B, 1620, 640, 7, { lit: night, dark: night, th: 150 })}<rect x="1300" y="${B - 380}" width="460" height="380" fill="${night ? "#141820" : "#2e3236"}" ${O(3)}/>
      <g opacity=".85">${[[1360, 0.9], [1520, 1.1], [1660, 0.8]].map(([x, k]) => `<rect x="${x}" y="${B - 200 * k}" width="100" height="${200 * k}" fill="${night ? "#2a2e36" : "#4a5056"}" ${O(2)}/><circle cx="${x + 50}" cy="${B - 150 * k}" r="22" fill="none" stroke="${night ? "#3a3e46" : "#6f7880"}" stroke-width="6"/>`).join("")}</g>
      <rect x="1290" y="${B - 410}" width="480" height="40" fill="${night ? "#3a3e46" : "#9aa4ab"}" ${O(3)}/>${Array.from({ length: 4 }, (_, k) => `<path d="M1300,${B - 402 + k * 8}h460" stroke="${INK}" stroke-width="2" opacity=".4"/>`).join("")}
      <rect x="1880" y="${B - 560}" width="560" height="90" fill="#1f6b46" ${O(3)}/>${T(2160, B - 500, "ความปลอดภัยต้องมาก่อน", 40, "#f4ecd8")}</g>`;
    s += [-430, 950, 2120].map((x) => LAMPPOST(x, B + 20, 760, night, night)).join("");
    s += `<g transform="translate(950,${B - 650})"><path d="M-6,0l-60,-20v40z M6,0l60,-20v40z" fill="${night ? "#3a3e46" : "#c9d0d4"}" ${O(3)}/></g>`;
    if (window.Dress) s += Dress.laundry(2180, 2560, B - 300, 77) + (dressed(o) ? Dress.garden(1980, B + 300, 380, 79) + Dress.crate(1820, B + 40, 0.9) + Dress.crate(1880, B - 50, 0.8) + Dress.drum(1150, B + 30, 0.9, "#2f5f8a") + Dress.puddle(400, B + 400, 160, 28, night) + Dress.crack(-200, B + 300, 140, 20, 0.4) : "");
    put(L.set, s);
    if (night) { put(L.glow, [-430, 950, 2120].map((x) => `<circle cx="${x + 110}" cy="${B + 20 - 750}" r="200" fill="url(#eFlood)" opacity=".9"/>`).join("") + `<g id="${id}-winwg"><rect x="70" y="${B - 730}" width="360" height="280" rx="60" fill="#ffd58a" opacity=".25"/></g>`); [-430, 950, 2120].forEach((x) => Fence.cone(L, x + 110, B - 730, 700, 1250, "#fff2c8", 0.4, "")); }
    else put(L.glow, `<rect x="-1400" y="400" width="4000" height="1400" fill="${t === "morning" ? "#ffb070" : "#fff2d8"}" opacity=".07"/>`);
  }

  // ======================================================================================================
  // 5. the workshop, first person: the bench, the pegboard of tools, a vise, the grinder, the spear laid across (#id-spear) with its
  // upgrade parts hidden: #id-collar (steel sleeve over the blade joint) and #id-wrap (rubber strips round the grip, revealed by the shot)
  // ======================================================================================================
  function workshopPov(L, o = {}) {
    const id = o.id || "wk", r = mk(o.seed || 69);
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#1e1c1a"/>`);
    let w = `<rect x="-1400" y="-900" width="4000" height="1700" fill="url(#ePeg)"/><rect x="-1400" y="-900" width="4000" height="1700" fill="url(#dGrime)" opacity=".7"/>`;
    const tool = (x, y, rot, body) => `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M0,-6v-30" stroke="#3a2a1a" stroke-width="5"/>${body}</g>`;
    w += tool(-120, 120, 8, `<rect x="-14" y="0" width="28" height="200" rx="8" fill="#c8392b" ${O(3)}/><rect x="-60" y="-30" width="120" height="44" rx="6" fill="#8d969d" ${O(3)}/>`);
    w += [0, 1, 2, 3, 4].map((k) => tool(80 + k * 60, 100, 0, `<rect x="-9" y="0" width="18" height="${150 + k * 24}" rx="6" fill="#a7b0b6" ${O(2.5)}/><circle cx="0" cy="0" r="20" fill="none" stroke="#a7b0b6" stroke-width="10"/>`)).join("");
    w += tool(520, 90, -4, `<path d="M-30,0H300L280,90H-10Z" fill="#c9d0d4" ${O(3)}/><rect x="-80" y="-6" width="60" height="100" rx="18" fill="#6b4a2e" ${O(3)}/>${Array.from({ length: 14 }, (_, k) => `<path d="M${k * 20},90l10,14l10,-14" stroke="${INK}" stroke-width="2" fill="none"/>`).join("")}`);
    w += tool(980, 140, 12, `<path d="M-20,0L-30,160M20,0L30,160" stroke="#2f4a8a" stroke-width="22" stroke-linecap="round"/><path d="M-14,-10L14,-10L6,-80H-6Z" fill="#8d969d" ${O(3)}/>`);
    w += [0, 1, 2].map((k) => tool(1180 + k * 50, 110, 0, `<rect x="-8" y="0" width="16" height="70" rx="4" fill="${["#e8b830", "#2f6fb8", "#c8392b"][k]}" ${O(2)}/><rect x="-3" y="70" width="6" height="90" fill="#a7b0b6"/>`)).join("");
    w += `<g transform="translate(-480,140)"><circle r="90" fill="none" stroke="#c8392b" stroke-width="22"/><circle r="90" fill="none" stroke="#2e2a26" stroke-width="3"/><circle r="64" fill="none" stroke="#a52a20" stroke-width="10"/></g>`;
    w += `<g transform="translate(760,-200)"><path d="M0,-700V0" stroke="#2a2a2a" stroke-width="5"/><path d="M-110,60L-70,0H70L110,60Z" fill="#3a3f45" ${OUT}/><ellipse cx="0" cy="62" rx="70" ry="16" fill="#fff6d8"/></g>`;
    w += `<rect x="-1400" y="700" width="4000" height="100" fill="#3a2a1a" opacity=".6"/>`;
    put(L.far, w);
    let s = `<rect x="-1400" y="760" width="4000" height="2100" fill="url(#eBench)"/>${Array.from({ length: 12 }, (_, k) => `<path d="M-1400,${800 + k * 170}H2600" stroke="#4a321c" stroke-width="5" opacity=".7"/><path d="M-1400,${804 + k * 170}H2600" stroke="#a5804f" stroke-width="2" opacity=".4"/>`).join("")}<rect x="-1400" y="760" width="4000" height="40" fill="url(#eSteel)" ${O(3)}/>`;
    s += [[200, 1100, 160], [820, 1700, 200], [-200, 1800, 140], [1000, 1000, 120]].map(([x, y, a]) => `<ellipse cx="${x}" cy="${y}" rx="${a}" ry="${a * 0.4}" fill="#1e140a" opacity=".3"/>`).join("");
    s += `<g transform="translate(930,960)"><rect x="-130" y="-40" width="260" height="120" rx="10" fill="#3f5a7a" ${OUT}/><rect x="-150" y="-100" width="110" height="70" fill="#4f6a8a" ${O(3)}/><rect x="40" y="-100" width="110" height="70" fill="#4f6a8a" ${O(3)}/><path d="M150,-60H330" stroke="#a7b0b6" stroke-width="18"/><circle cx="330" cy="-60" r="18" fill="#3a3f45"/></g>`;
    s += `<g transform="translate(140,950)"><circle r="110" fill="#5b6066" ${OUT}/><circle r="80" fill="#8d969d" ${O(3)}/><circle r="20" fill="#3a3f45"/><rect x="100" y="-50" width="200" height="100" rx="20" fill="#2f6f6a" ${OUT}/><path d="M-130,-100q60,-60 120,-40" stroke="#5b6066" stroke-width="18" fill="none"/></g>`;
    s += Array.from({ length: 18 }, () => { const x = -600 + r() * 2300, y = 1500 + r() * 900; return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(r() * 360)})"><path d="M-14,-8l14,-8l14,8v16l-14,8l-14,-8z" fill="#a7b0b6" ${O(2)}/><circle r="6" fill="#5b6066"/></g>`; }).join("");
    s += `<g transform="translate(-260,1240) rotate(-12)"><path d="M-80,0q40,-60 120,-30q60,30 20,90q-80,30 -140,-60z" fill="#c9b89a" ${O(3)}/><path d="M-50,-10q40,-20 90,10" stroke="#8a7a5a" stroke-width="4" fill="none"/></g>`;
    s += `<g transform="translate(1280,1520)"><ellipse rx="110" ry="40" fill="#1f1d1a" ${O(3)}/><ellipse rx="70" ry="24" fill="#2e2a26"/><path d="M60,-20l160,-60l10,30l-160,50z" fill="#1f1d1a" ${O(3)}/></g>`;
    // the spear, butt lower-left to blade upper-right: steel shaft (the +1), black tape bands, ลุงหมาน's knife
    const L0 = -80, L1 = 1180, Y0 = 1560, Y1 = 1200, ang = Math.atan2(Y1 - Y0, L1 - L0) * 180 / Math.PI, len = Math.hypot(L1 - L0, Y1 - Y0);
    s += `<g id="${id}-spear" transform="translate(${L0},${Y0}) rotate(${f1(ang)})"><ellipse cx="${len / 2}" cy="26" rx="${len / 2}" ry="18" fill="#000" opacity=".25"/>
      <rect x="0" y="-22" width="${len - 230}" height="44" rx="14" fill="url(#eSteel)" ${O(4)}/><path d="M20,-10H${len - 250}" stroke="#fff" stroke-width="4" opacity=".55"/>
      <rect x="0" y="-24" width="60" height="48" rx="8" fill="#1f1d1a" ${O(3)}/>${[len - 330, len - 290, len - 250].map((x) => `<rect x="${x}" y="-28" width="30" height="56" rx="5" fill="#1f1d1a" ${O(3)}/>`).join("")}
      <g transform="translate(${len - 230},0)"><path d="M0,-26H40L250,-8Q262,0 250,8L40,26H0Z" fill="#d6dbdf" ${O(4)}/><path d="M40,-12L240,-2" stroke="#fff" stroke-width="5" opacity=".7"/><path d="M40,14L230,4" stroke="#8d969d" stroke-width="3"/></g>
      <g id="${id}-wrap">${Array.from({ length: 12 }, (_, k) => `<g class="ewrap"><path d="M${140 + k * 30},-28l26,56" stroke="#1f1d1a" stroke-width="30" stroke-linecap="round"/><path d="M${136 + k * 30},-22l20,40" stroke="#4a4642" stroke-width="5" stroke-linecap="round"/></g>`).join("")}</g>
      <g id="${id}-collar" opacity="0"><rect x="${len - 340}" y="-34" width="140" height="68" rx="12" fill="url(#eSteel)" ${O(4)}/>${[0, 1, 2].map((k) => `<path d="M${len - 320 + k * 44},-34v68" stroke="#6f7880" stroke-width="4"/>`).join("")}<circle cx="${len - 220}" cy="0" r="8" fill="#5b6066"/><path d="M${len - 330},-22h120" stroke="#fff" stroke-width="5" opacity=".7"/></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="760" cy="-140" r="900" fill="url(#eFlood)" opacity=".45"/><g id="${id}-sparks" opacity="0">${Array.from({ length: 22 }, (_, k) => { const a = -Math.PI * (0.15 + 0.7 * r()), d = 60 + r() * 220; return `<path d="M0,0L${f1(Math.cos(a) * d)},${f1(Math.sin(a) * d)}" stroke="${k % 3 ? "#ffd25a" : "#fff6d8"}" stroke-width="${f1(3 + r() * 4)}" stroke-linecap="round"/>`; }).join("")}</g>`);
  }

  // ======================================================================================================
  // 6. the communal washroom: tiled walls, the long mirror over three sinks, the high louvred window (light in), the stalls on the
  // right, the door on the left (#id-door swings; daylight behind), wet floor and drain. Gas: Estate.GAS put on top by the shot.
  // ======================================================================================================
  function washroom(L, o = {}) {
    const id = o.id || "wr", r = mk(o.seed || 71), F = 1300;
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#1e2220"/>`);
    let w = `<rect x="-1400" y="-900" width="4000" height="${F + 900}" fill="url(#eTileW)"/><rect x="-1400" y="-900" width="4000" height="${F + 900}" fill="url(#dGrime)"/><rect x="-1400" y="${F - 260}" width="4000" height="260" fill="#9aa39a" opacity=".45"/>`;
    // the door to the yard: frame, the bright day behind, the leaf
    w += `<rect x="-640" y="${F - 560}" width="320" height="560" fill="#fff6dc"/><rect x="-640" y="${F - 560}" width="320" height="560" fill="#c9dfe8" opacity=".5"/><rect x="-660" y="${F - 580}" width="360" height="580" fill="none" stroke="#6f7880" stroke-width="22"/>
      <g id="${id}-door" transform="translate(-640,0) scale(${o.door ?? 1},1) translate(640,0)"><rect x="-640" y="${F - 560}" width="320" height="560" fill="#8a6a44" ${OUT}/><rect x="-610" y="${F - 520}" width="260" height="200" fill="#000" opacity=".1"/><circle cx="-350" cy="${F - 280}" r="10" fill="#c9a55a"/></g>`;
    // mirror + sinks
    w += `<rect x="40" y="${F - 660}" width="780" height="300" fill="#8fa8b0" ${OUT}/><path d="M60,${F - 640}L300,${F - 380}M420,${F - 650}l90,120l-60,40l120,110" stroke="#e8f0f2" stroke-width="5" fill="none" opacity=".7"/><path d="M40,${F - 660}h780v300h-780z" fill="url(#dGrime)" opacity=".7"/>`;
    w += [140, 430, 720].map((x) => `<g transform="translate(${x},${F - 240})"><path d="M-110,0H110L90,60Q0,90 -90,60Z" fill="#eef1ee" ${OUT}/><rect x="-14" y="60" width="28" height="180" fill="#c9d0d5" ${O(3)}/><path d="M0,-60v40q0,10 20,10" stroke="#a7b0b6" stroke-width="10" fill="none"/><ellipse cx="0" cy="10" rx="80" ry="14" fill="#cdd5d3"/></g>`).join("");
    // the high louvred window
    w += `<g transform="translate(1040,${F - 940})"><rect x="-150" y="-100" width="300" height="200" fill="#fff6dc" ${OUT}/>${Array.from({ length: 5 }, (_, k) => `<path d="M-140,${-80 + k * 38}h280" stroke="#c9cfc8" stroke-width="15"/>`).join("")}<rect x="-150" y="-100" width="300" height="200" fill="none" stroke="#8d969d" stroke-width="12"/></g>`;
    // stalls
    w += `<g>${[1240, 1600, 1960, 2320].map((x, k) => `<rect x="${x - 10}" y="${F - 760}" width="22" height="760" fill="#84a68e" ${O(3)}/>${k < 3 ? `<rect x="${x + 22}" y="${F - 700}" width="330" height="660" fill="${k === 1 ? "#5a6a5e" : "url(#ePaintG)"}" ${O(3)}/>${k === 1 ? `<path d="M${x + 22},${F - 700}L${x + 120},${F - 680}V${F - 60}L${x + 22},${F - 40}Z" fill="url(#ePaintG)" ${O(3)}/>` : `<circle cx="${x + 320}" cy="${F - 380}" r="8" fill="#5b6066"/>`}` : ""}`).join("")}</g>`;
    if (dressed(o)) w += [[-200, 0.7], [600, 0.6], [1100, 0.7], [1800, 0.6]].map(([x, op]) => Dress.streak(x, F - 820, 80 + r() * 60, 600, op)).join("") + Array.from({ length: 50 }, () => `<circle cx="${f1(-1200 + r() * 3600)}" cy="${f1(F - 260 + r() * 250)}" r="${f1(3 + r() * 9)}" fill="#3a4a2a" opacity="${f1(0.2 + r() * 0.35)}"/>`).join("");
    put(L.far, w);
    let s = `<rect x="-1400" y="${F}" width="4000" height="1600" fill="url(#eTileF)"/><rect x="-1400" y="${F}" width="4000" height="1600" fill="url(#dGrime)" opacity=".6"/><path d="M-1400,${F}H2600" stroke="#4a4a40" stroke-width="10"/>`;
    s += [[200, F + 300, 260, 34], [900, F + 460, 300, 40], [-300, F + 600, 220, 30], [1500, F + 380, 240, 32]].map(([x, y, a, b]) => `<ellipse cx="${x}" cy="${y}" rx="${a}" ry="${b}" fill="#dfe6e6" opacity=".32"/><ellipse cx="${x - a * 0.3}" cy="${y - b * 0.3}" rx="${a * 0.25}" ry="${b * 0.2}" fill="#fff" opacity=".4"/>`).join("");
    s += `<g transform="translate(640,${F + 300})"><ellipse rx="80" ry="22" fill="#8d969d" ${O(3)}/>${Array.from({ length: 5 }, (_, k) => `<path d="M${-48 + k * 24},-14v28" stroke="#4a4f55" stroke-width="4"/>`).join("")}</g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="1040" cy="${F - 940}" r="380" fill="url(#eFlood)" opacity=".5"/>`);
    Fence.rays(L, 900, 1200, F - 1000, F + 200, 3, "#fff6dc", 0.5);
    if (o.doorLight !== false) put(L.glow, `<path d="M-640,${F - 560}L-320,${F - 560}L60,${F + 400}L-700,${F + 400}Z" fill="#fff6dc" opacity="${f1(0.18 * (1 - (o.door ?? 1)))}" id="${id}-spill"/>`);
  }

  // ======================================================================================================
  // 7. the canteen at night: pale-green wainscot, cream wall, barred windows on the dark, fluorescent tubes, a clock, the duty board,
  // a poster "ทุกคนต้องมีประโยชน์", a water cooler; the near table is Estate.TABLEF put over the seated rigs by the shot
  // ======================================================================================================
  function canteen(L, o = {}) {
    const id = o.id || "cn", r = mk(o.seed || 73), F = 1300;
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#141820"/>`);
    let w = `<rect x="-1400" y="-900" width="4000" height="${F - 400 + 900}" fill="url(#eCream)"/><rect x="-1400" y="${F - 400}" width="4000" height="400" fill="url(#ePaintG)"/><path d="M-1400,${F - 400}H2600" stroke="#6a8a72" stroke-width="10"/>`;
    w += [-500, 360, 1220, 2080].map((x) => `<g transform="translate(${x},${F - 760})"><rect x="-200" y="-180" width="400" height="300" fill="url(#eNightIn)" ${OUT}/>${Array.from({ length: 7 }, (_, k) => `<path d="M${-170 + k * 56},-180v300" stroke="#5b6066" stroke-width="8"/>`).join("")}<circle cx="120" cy="-110" r="10" fill="#e9eef5" opacity=".6"/><path d="M-200,-30H200" stroke="#5b6066" stroke-width="10"/></g>`).join("");
    w += `<g transform="translate(800,${F - 1060})"><circle r="64" fill="#f4f2ea" ${OUT}/><path d="M0,0V-44M0,0L36,12" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle r="6" fill="${INK}"/></g>`;
    w += `<g transform="translate(1650,${F - 560})"><rect x="-200" y="-150" width="400" height="250" fill="#6b4a2e" ${OUT}/><rect x="-186" y="-136" width="372" height="222" fill="#d9cfb8"/>${T(0, -96, "ตารางงาน", 36, "#2f4a8a")}${Array.from({ length: 6 }, (_, k) => `<path d="M-160,${-60 + k * 26}h${200 + (k % 3) * 40}" stroke="#5b6066" stroke-width="4"/>`).join("")}<rect x="100" y="-40" width="70" height="90" fill="#f4f2ea" stroke="#8d969d" stroke-width="2" transform="rotate(4 135 5)"/></g>`;
    w += PLATE(-40, F - 560, 380, 150, ["ทุกคน", "ต้องมีประโยชน์"], { size: 40, rust: true });
    w += `<g transform="translate(2300,${F})"><rect x="-70" y="-300" width="140" height="300" fill="#e8ece6" ${OUT}/><path d="M-50,-420h100l-10,120h-80z" fill="#cfe6ee" fill-opacity=".7" ${O(3)}/><rect x="-20" y="-200" width="40" height="20" fill="#2f6fb8"/></g>`;
    w += [-700, 300, 1300, 2300].map((x) => `<g transform="translate(${x},-120)"><rect x="-240" y="-14" width="480" height="28" rx="10" fill="#d9d6cc" ${O(3)}/><rect x="-224" y="10" width="448" height="12" rx="6" fill="#f4fbff"/></g>`).join("");
    if (dressed(o)) w += [[-900, 0.5], [500, 0.4], [1900, 0.5]].map(([x, op]) => Dress.streak(x, F - 380, 90, 380, op)).join("");
    put(L.far, w);
    let s = `<rect x="-1400" y="${F}" width="4000" height="1600" fill="url(#eTileF)"/><rect x="-1400" y="${F}" width="4000" height="1600" fill="#000" opacity=".18"/><path d="M-1400,${F}H2600" stroke="#4a4a40" stroke-width="10"/>`;
    s += `<g opacity=".9">${TABLEF(-1100, 2400, F + 40, { seed: 37 }).replace(/<path d="M[-\d.]+,[-\d.]+V[-\d.]+M[-\d.]+,[-\d.]+V[-\d.]+" stroke="#5b6066" stroke-width="14"\/>/, "")}</g>`;
    put(L.set, s);
    put(L.glow, [-700, 300, 1300, 2300].map((x) => `<ellipse cx="${x}" cy="-80" rx="620" ry="260" fill="url(#eFluo)" opacity=".7"/>`).join(""));
  }

  // ======================================================================================================
  // 8. the dormitory at night: blue-grey wall, a barred window onto the floodlit yard and the far gate (#id-gatewin), bunk beds with
  // a mosquito net, ปั้น asleep on the lower bunk (o.pun), the crate with ลุงหมาน's radio (#id-dial glow), the group's bags
  // ======================================================================================================
  function dormNight(L, o = {}) {
    const id = o.id || "dm", r = mk(o.seed || 75), F = 1300;
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#0e1218"/>`);
    let w = `<rect x="-1400" y="-900" width="4000" height="${F + 900}" fill="#3e4a5a"/><rect x="-1400" y="${F - 200}" width="4000" height="200" fill="#323c4a"/>`;
    // the window: the yard under floodlights, the fence, the gate far off with its two lamps
    w += `<g transform="translate(780,${F - 640})"><rect x="-240" y="-260" width="480" height="420" fill="#0e1420"/><g><rect x="-240" y="40" width="480" height="120" fill="#2a3038"/>${[-170, -40, 90, 200].map((x) => `<rect x="${x}" y="-20" width="12" height="60" fill="#1a1e26"/>`).join("")}<path d="M-240,30H240" stroke="#3a4250" stroke-width="6"/>
      <g id="${id}-gatewin"><rect x="-30" y="-10" width="70" height="44" fill="none" stroke="#5a6270" stroke-width="3"/>${[0, 1, 2, 3].map((k) => `<path d="M${-24 + k * 18},-8v40" stroke="#5a6270" stroke-width="2"/>`).join("")}</g>
      <circle cx="-40" cy="-30" r="4" fill="#fffbe8"/><circle cx="50" cy="-30" r="4" fill="#fffbe8"/>${[-200, -120, 120, 200].map((x) => `<circle cx="${x}" cy="-40" r="3" fill="#fffbe8"/>`).join("")}</g>
      ${Array.from({ length: 7 }, (_, k) => `<path d="M${-200 + k * 66},-260v420" stroke="#5b6066" stroke-width="12"/>`).join("")}<rect x="-250" y="-270" width="500" height="440" fill="none" stroke="#6f7880" stroke-width="20"/><rect x="-270" y="170" width="540" height="24" fill="#6f7880" ${O(3)}/></g>`;
    w += `<g transform="translate(-660,${F - 900})"><circle r="70" fill="none" stroke="#5b6066" stroke-width="8"/>${[0, 120, 240].map((a) => `<path d="M0,0L${f1(Math.cos(a * Math.PI / 180) * 60)},${f1(Math.sin(a * Math.PI / 180) * 60)}" stroke="#7d868c" stroke-width="18" stroke-linecap="round"/>`).join("")}<circle r="14" fill="#3a3f45"/></g>`;
    w += `<path d="M1200,${F - 820}Q1500,${F - 780} 1800,${F - 820}" stroke="#8d969d" stroke-width="3" fill="none"/>${[[1300, "#c9a06c"], [1480, "#d96a8a"], [1650, "#9fc5d8"]].map(([x, c]) => `<path d="M${x},${F - 806}h90v150h-90z" fill="${c}" opacity=".7" ${O(2.5)}/>`).join("")}`;
    put(L.far, w);
    // floor, the bunk (x -560..300), the crate + radio (x 980), bags, the spear against the bunk
    let s = `<rect x="-1400" y="${F}" width="4000" height="1600" fill="#2e333a"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-1400 + k * 500},${F}L${-1700 + k * 650},2800" stroke="#252a30" stroke-width="4"/>`).join("")}`;
    s += `<g transform="translate(780,${F + 160})"><path d="M-260,-200L260,-200L420,320L-420,320Z" fill="#cfe0f0" opacity=".1"/>${Array.from({ length: 7 }, (_, k) => `<path d="M${-200 + k * 66},-200L${-320 + k * 106},320" stroke="#0e1218" stroke-width="16" opacity=".35"/>`).join("")}</g>`;
    const bunk = `<g transform="translate(-130,${F + 220})"><path d="M-430,0V-900M430,0V-900" stroke="#6f7880" stroke-width="22"/><path d="M-430,-220H430M-430,-720H430" stroke="#6f7880" stroke-width="18"/>
      <rect x="-420" y="-300" width="840" height="80" rx="20" fill="#9a8a6a" ${OUT}/><rect x="-420" y="-800" width="840" height="80" rx="20" fill="#8a7a5a" ${OUT}/><rect x="-400" y="-330" width="160" height="40" rx="18" fill="#e8e2d4" ${O(3)}/>
      ${o.pun !== false ? `<g><circle cx="-320" cy="-344" r="40" fill="#efc6a0" ${O(3)}/><path d="M-360,-350Q-360,-392 -320,-392Q-280,-392 -282,-352Q-300,-372 -320,-372Q-342,-372 -360,-350Z" fill="#231a16" ${O(3)}/><path d="M-358,-360q-30,10 -26,40M-282,-360q24,10 20,40" stroke="#231a16" stroke-width="12" stroke-linecap="round" fill="none"/><path d="M-336,-342q6,4 12,0M-312,-342q6,4 12,0" stroke="${INK}" stroke-width="3" fill="none"/><path d="M-290,-330Q-40,-420 300,-330V-300H-290Z" fill="#c8392b" opacity=".9" ${O(3)}/><path d="M-200,-350q100,-30 220,-14" stroke="#a52a20" stroke-width="4" fill="none"/></g>` : ""}
      <path d="M-430,-900Q-300,-500 -440,-230M430,-900Q300,-500 440,-230" stroke="#e8ece6" stroke-width="6" fill="none" opacity=".35"/><path d="M-440,-900Q0,-860 440,-900" stroke="#e8ece6" stroke-width="20" fill="none" opacity=".25"/>
      ${Array.from({ length: 5 }, (_, k) => `<path d="M330,${-700 + k * 100}h100" stroke="#6f7880" stroke-width="8"/>`).join("")}</g>`;
    s += bunk;
    s += `<g transform="translate(980,${F + 240})"><path d="M-130,0L-120,-160H120L130,0Z" fill="#8a6a44" ${OUT}/><path d="M-124,-80H124" stroke="#6b4a2e" stroke-width="5"/>
      <g transform="translate(0,-160)"><rect x="-110" y="-120" width="220" height="120" rx="14" fill="#6b4a2e" ${OUT}/><rect x="-96" y="-104" width="110" height="58" rx="6" fill="#2a1a0a" ${O(2)}/><g id="${id}-dialw" opacity="${o.radioOn ? 1 : 0}"><rect x="-96" y="-104" width="110" height="58" rx="6" fill="#ffb35c" opacity=".7"/></g><rect x="-60" y="-100" width="3" height="50" fill="#ff3b30"/>
        <rect x="26" y="-104" width="72" height="88" rx="6" fill="#2a2420" ${O(2)}/>${Array.from({ length: 5 }, (_, k) => `<path d="M${32 + k * 14},-100v80" stroke="#c9a55a" stroke-width="3" opacity=".55"/>`).join("")}<circle cx="-70" cy="-26" r="14" fill="#c9a55a" ${O(2)}/><circle cx="-20" cy="-26" r="14" fill="#c9a55a" ${O(2)}/><path d="M100,-120L170,-260" stroke="#9aa0a6" stroke-width="5"/></g></g>`;
    s += `<g transform="translate(330,${F + 260})"><path d="M-80,0q-10,-70 10,-110h120q20,40 10,110z" fill="#3d4d45" ${O(3)}/><path d="M-50,-110q40,-40 80,0" stroke="#2e2a26" stroke-width="8" fill="none"/></g><g transform="translate(470,${F + 270})"><path d="M-70,0q-6,-60 8,-90h110q14,30 8,90z" fill="#d96a8a" opacity=".85" ${O(3)}/></g>`;
    s += `<g transform="translate(280,${F + 230}) rotate(-14)"><rect x="-12" y="-900" width="24" height="900" rx="8" fill="url(#eSteel)" ${O(3)}/>${Array.from({ length: 8 }, (_, k) => `<path d="M-14,${-520 + k * 22}l28,14" stroke="#1f1d1a" stroke-width="12"/>`).join("")}<path d="M-14,-900L0,-1060L14,-900Z" fill="#d6dbdf" ${O(3)}/></g>`;
    put(L.set, s);
    put(L.glow, `<g id="${id}-glow" opacity="${o.radioOn ? 1 : 0}"><circle cx="960" cy="${F + 20}" r="420" fill="url(#fDial)"/></g><rect x="540" y="${F - 900}" width="480" height="420" fill="#cfe0f0" opacity=".08"/>`);
  }

  // ======================================================================================================
  // 9. คุณวิน's notebook, from above on his desk: the register (page "chan": ยายจันทร์'s job struck out, "ทำงานไม่ได้" in red —
  // #id-strike, #id-red; ปั้น "รอดู") or the count (page "count": the radio numbers 99 … 94 and #id-n93 being written, the radio's glow)
  // ======================================================================================================
  function notebook(L, o = {}) {
    const id = o.id || "nb", page = o.page || "chan", night = page === "count";
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#1a120a"/>`);
    let s = `<rect x="-1400" y="-900" width="4000" height="3800" fill="url(#eDesk)"/>${Array.from({ length: 30 }, (_, k) => `<path d="M-1400,${-900 + k * 130}q1000,${(k % 3) * 20 - 20} 4000,0" stroke="#2e1e10" stroke-width="3" opacity=".5" fill="none"/>`).join("")}`;
    s += `<g transform="rotate(-4 540 1000)"><rect x="110" y="480" width="860" height="1080" rx="14" fill="#2f2a4a" ${OUT}/><rect x="126" y="494" width="410" height="1052" fill="#f7f1e2" ${O(2)}/><rect x="544" y="494" width="410" height="1052" fill="#f4ecd8" ${O(2)}/><path d="M540,494V1546" stroke="#8a7a5a" stroke-width="8"/>
      ${Array.from({ length: 20 }, (_, k) => `<path d="M140,${560 + k * 48}H526M558,${560 + k * 48}H944" stroke="#b9c8d8" stroke-width="2"/>`).join("")}<path d="M190,500V1540M608,500V1540" stroke="#e8a0a0" stroke-width="2"/>`;
    const H = (x, y, txt, size = 34, col = "#2f4a8a", extra = "") => `<text x="${x}" y="${y}" font-family="Kanit" font-weight="500" font-size="${size}" fill="${col}"${extra}>${txt}</text>`;
    s += H(200, 548, "ทะเบียนนิคม", 40, "#2f4a8a") + [["ประเสริฐ · รปภ.", 0], ["บุญมี · ครัว", 1], ["สมศรี · ซักผ้า", 2], ["วีระ · ช่าง", 3], ["จันทร์ · 71 · ทำความสะอาด", 4], ["ภู · หมอ", 6], ["พิม · ครัว", 7], ["ก้อง · หาของ", 8], ["หงส์ · โกดัง", 9], ["ปั้น · 7 · รอดู", 10]].map(([t, k]) => H(200, 606 + k * 48, `${k + 1 > 5 ? k : k + 1}. ${t}`, 30)).join("");
    s += `<clipPath id="${id}-cs"><rect id="${id}-csr" x="330" y="${606 + 4 * 48 - 40}" width="${o.struck ? 220 : 0}" height="60"/></clipPath><clipPath id="${id}-cr"><rect id="${id}-crr" x="230" y="${606 + 5 * 48 - 60}" width="${o.struck ? 320 : 0}" height="90"/></clipPath>
      <g id="${id}-strike" clip-path="url(#${id}-cs)"><path d="M340,${606 + 4 * 48 - 10}h190" stroke="#c8392b" stroke-width="5"/></g><g id="${id}-red" clip-path="url(#${id}-cr)">${H(240, 606 + 5 * 48 - 6, "→ ทำงานไม่ได้", 34, "#c8392b", ' transform="rotate(-3 240 840)"')}</g>`;
    s += `<ellipse cx="370" cy="${606 + 10 * 48 - 12}" rx="100" ry="30" fill="none" stroke="#c8392b" stroke-width="4" opacity=".8"/>`;
    if (night) {
      s += H(620, 548, "วิทยุ · ทุกคืน", 38, "#2f4a8a") + [99, 98, 97, 96, 95, 94].map((n, k) => H(640, 606 + k * 48, `${n}`, 34) + `<path d="M700,${598 + k * 48}h${60 + (k % 2) * 20}" stroke="#2f4a8a" stroke-width="3" opacity=".6"/>`).join("");
      s += `<clipPath id="${id}-cn"><rect id="${id}-cnr" x="630" y="${606 + 6 * 48 - 44}" width="${o.n93 ? 90 : 0}" height="60"/></clipPath><g id="${id}-n93" clip-path="url(#${id}-cn)">${H(640, 606 + 6 * 48, "93", 38, "#c8392b")}</g>`;
    } else s += H(620, 548, "งานวันนี้", 38, "#2f4a8a") + ["ซ่อมรั้ว ด้านเหนือ", "ขนข้าวสาร 12 กระสอบ", "ล้างห้องน้ำรวม", "เปลี่ยนแผงโซลาร์ 3 แผง"].map((t, k) => H(620, 606 + k * 48, `- ${t}`, 30)).join("");
    s += `</g>`;
    s += `<g transform="translate(940,1700) rotate(30)"><rect x="-10" y="-200" width="20" height="200" rx="6" fill="#1f1d1a" ${O(3)}/><path d="M-10,0L0,30L10,0Z" fill="#c9a55a" ${O(2)}/></g>`;
    s += `<g transform="translate(-60,1500) rotate(-8)"><rect x="-120" y="-60" width="240" height="120" rx="10" fill="#f4f2ea" ${OUT}/><rect x="-120" y="-60" width="240" height="30" fill="#c8392b"/>${T(0, 20, "วิน", 46, "#2e2a26")}</g>`;
    if (night) s += `<g transform="translate(1000,360)"><rect x="-200" y="-140" width="400" height="280" rx="24" fill="#6b4a2e" ${OUT}/><rect x="-170" y="-110" width="200" height="110" rx="8" fill="#2a1a0a"/><g id="${id}-dialw"><rect x="-170" y="-110" width="200" height="110" rx="8" fill="#ffb35c" opacity=".7"/></g><rect x="-80" y="-104" width="4" height="96" fill="#ff3b30"/></g>`;
    else s += `<g transform="translate(-40,520)"><ellipse rx="110" ry="100" fill="#f4f2ea" ${OUT}/><ellipse rx="86" ry="78" fill="#5a3a22"/></g>`;
    put(L.set, s);
    if (night) put(L.glow, `<circle cx="960" cy="360" r="700" fill="url(#fDial)"/><rect x="-1400" y="-900" width="4000" height="3800" fill="#0a0e18" opacity=".25"/>`);
    else put(L.glow, `<circle cx="300" cy="200" r="900" fill="url(#eFlood)" opacity=".35"/>`);
  }

  // ======================================================================================================
  // 10. ปั้น's drawing that night: the estate fence with its lamps, the factory; outside, a small old woman with a white bun among
  // black scribbled shapes (#id-shadows), the moon, "คืนนี้", "ยายจันทร์"
  // ======================================================================================================
  function drawing6(L, o = {}) {
    const id = o.id || "dw6";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#3a3330"/>`);
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    let s = `<g transform="rotate(-1.5 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    s += `<rect x="140" y="320" width="800" height="760" fill="#1f2a4a" opacity=".45" filter="url(#fCrayon)"/><circle cx="800" cy="440" r="56" fill="#f2e27a" filter="url(#fCrayon)"/>`;
    s += C("M180,900V700H500V900M180,700L280,620L380,700L480,620M540,900V660H880V900M540,660L640,580L740,660L840,580", "#5b6066", 9) + `<rect x="180" y="700" width="320" height="200" fill="#b3ada0" opacity=".5" filter="url(#fCrayon)"/><rect x="540" y="660" width="340" height="240" fill="#b3ada0" opacity=".5" filter="url(#fCrayon)"/>`;
    s += [[220, 760], [320, 760], [420, 760], [590, 720], [700, 720], [810, 720]].map(([x, y]) => `<rect x="${x}" y="${y}" width="44" height="44" fill="#ffd25a" filter="url(#fCrayon)"/>`).join("");
    s += C("M140,1100H950M140,960H950" + Array.from({ length: 10 }, (_, k) => `M${150 + k * 88},1100V950`).join(""), "#3f454b", 7);
    s += [190, 410, 630, 850].map((x) => `<circle cx="${x}" cy="940" r="14" fill="#ffd25a" filter="url(#fCrayon)"/>`).join("");
    // outside: ยายจันทร์ (white bun, purple blouse, the sarong) alone
    s += `<g transform="translate(540,1420)" filter="url(#fCrayon)"><circle cy="-150" r="30" fill="none" stroke="#8a6a4a" stroke-width="8"/><circle cx="18" cy="-182" r="16" fill="#f4f2ea" stroke="#9aa0a6" stroke-width="5"/><path d="M-26,-160Q0,-190 26,-160" stroke="#e8e6e0" stroke-width="10" fill="none"/>
      <path d="M-30,-118H30L36,-40H-36Z" fill="#9a6aa8"/><path d="M-36,-40H36L30,40H-30Z" fill="#4a5a3a"/><path d="M-30,-110l-30,60M30,-110l26,60" stroke="#8a6a4a" stroke-width="8" stroke-linecap="round"/><path d="M-20,-150q4,4 8,0M8,-150q4,4 8,0M-10,-134q10,-6 20,0" stroke="#5a4a3a" stroke-width="4" fill="none"/></g>`;
    s += `<g id="${id}-shadows">${[[250, 1380, 1.1], [360, 1500, 0.9], [760, 1370, 1.05], [860, 1490, 1], [180, 1560, 0.95], [920, 1580, 1.1], [650, 1560, 0.8], [430, 1300, 0.75]].map(([x, y, k]) => `<g transform="translate(${x},${y}) scale(${k})"><g class="shm" filter="url(#fCrayon)"><path d="M-30,40L-20,-110Q0,-150 20,-110L30,40Z" fill="#1a1612"/><circle cy="-140" r="26" fill="#1a1612"/><path d="M-20,-90l-60,-30M20,-90l60,-24" stroke="#1a1612" stroke-width="16" stroke-linecap="round"/><circle class="sheye" cx="-8" cy="-144" r="4" fill="#d8ff9a"/><circle class="sheye" cx="8" cy="-144" r="4" fill="#d8ff9a"/></g></g>`).join("")}</g>`;
    s += T(540, 1640, "ยายจันทร์", 52, "#9a6aa8", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(300, 400, "คืนนี้", 64, "#f4ecd8", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(880, 1640, "ปั้น", 34, "#c8392b", { w: 700, extra: ' filter="url(#fCrayon)"' });
    s += `</g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ======================================================================================================
  // the people of the estate: ยายจันทร์, three workers, two guards (the rig's own outline weight)
  // ======================================================================================================
  const OR = 'stroke="#2e2a26" stroke-width="3.5" stroke-linejoin="round"';
  const TAG = (col = "#c8392b") => `<rect x="12" y="-452" width="38" height="22" rx="3" fill="#f4f2ea" ${OR}/><rect x="12" y="-452" width="38" height="6" fill="${col}"/><path d="M18,-440h26M18,-434h18" stroke="#5b6066" stroke-width="2"/>`;
  const SCARF = `<path d="M-40,-486Q0,-456 40,-486Q30,-460 0,-450Q-30,-460 -40,-486Z" fill="#c8392b" stroke="#2e2a26" stroke-width="3"/>`;
  Object.assign(Rig.CAST, {
    yai: { // ยายจันทร์: seventy, the estate's only old woman: lilac blouse with a scalloped lace collar, a faded blue cleaner's apron, batik sarong, white bun with a pin
      skin: "#d6a37c", skinS: "#b3805a", top: "#b89ac8", topS: "#9478a8", sleeve: "#b89ac8", sleeveS: "#9478a8", forearm: "#d6a37c", forearmS: "#b3805a",
      pants: "#4c5a3c", pantsS: "#3a462c", shoe: "#7a5a3a", belt: "#3a462c",
      torsoExtra: `<path d="M-34,-488q8,12 17,0q8,12 17,0q8,12 17,0q8,12 17,0" fill="#f4f2ea" stroke="#2e2a26" stroke-width="2.5"/>${[-446, -420].map((y) => `<circle cx="0" cy="${y}" r="4" fill="#f4f2ea" stroke="#2e2a26" stroke-width="1.5"/>`).join("")}
        <path d="M-44,-404H44L50,-306H-50Z" fill="#6f95aa" ${OR}/><path d="M-40,-404Q0,-430 40,-404" stroke="#6f95aa" stroke-width="5" fill="none"/><rect x="-18" y="-372" width="36" height="28" rx="4" fill="#5f8598" ${OR}/>
        <path d="M-56,-318H56" stroke="#3a462c" stroke-width="10"/>${[-40, -14, 12, 38].map((x) => `<circle cx="${x}" cy="-316" r="4" fill="#c9a55a"/>`).join("")}${TAG("#2f6fb8")}`,
      hair: `<path d="M-48,-548Q-54,-606 0,-610Q52,-606 48,-548Q42,-582 2,-586Q-40,-582 -48,-548Z" fill="#e8e5de" ${OR}/><circle cx="34" cy="-598" r="22" fill="#e8e5de" ${OR}/><path d="M-30,-596q20,-10 46,-6M-36,-576q24,-14 54,-10" stroke="#bdb8ad" stroke-width="3" fill="none"/><path d="M26,-616l22,30" stroke="#c9a55a" stroke-width="5" stroke-linecap="round"/>`,
      face: `<path d="M-34,-532q9,5 16,0M12,-532q9,5 16,0" stroke="#8a5a3a" stroke-width="2.5" fill="none" opacity=".6"/><path d="M-30,-504q4,10 -2,16M34,-504q-4,10 2,16" stroke="#8a5a3a" stroke-width="2.5" fill="none" opacity=".55"/><path d="M-6,-588q12,-4 24,0" stroke="#a5805a" stroke-width="2" fill="none" opacity=".5"/><g fill="#d98a7a" opacity=".32"><ellipse cx="-26" cy="-520" rx="8" ry="4"/><ellipse cx="30" cy="-520" rx="8" ry="4"/></g>`,
    },
    wk1: { // a factory hand: pale-blue work shirt, the estate's red-topped tag, navy trousers, navy cap
      skin: "#c99064", skinS: "#a87248", top: "#9cbcd6", topS: "#7c9cb6", sleeve: "#9cbcd6", sleeveS: "#7c9cb6", forearm: "#c99064", forearmS: "#a87248",
      pants: "#2f3a52", pantsS: "#232c40", shoe: "#1e1e1e", belt: "#232c40",
      torsoExtra: `<path d="M-26,-486L0,-462L26,-486" stroke="#7c9cb6" stroke-width="5" fill="none"/><rect x="-46" y="-470" width="30" height="28" rx="3" fill="none" stroke="#7c9cb6" stroke-width="3"/>${TAG()}`,
      hair: `<path d="M-48,-560Q-48,-612 0,-614Q48,-612 48,-560Z" fill="#2f3a52" ${OR}/><path d="M10,-566h70q8,0 4,10h-74z" fill="#2f3a52" ${OR}/><circle cx="0" cy="-596" r="6" fill="#c8392b"/>`,
      face: `<path d="M-28,-560q8,-5 16,-2M14,-562q8,-4 16,2" stroke="#3a2a1e" stroke-width="3" fill="none"/>`,
    },
    wk2: { // a factory hand: pink work smock, black trousers, hair in a net
      skin: "#e2b28a", skinS: "#c08e66", top: "#e09aa8", topS: "#c07a8a", sleeve: "#e09aa8", sleeveS: "#c07a8a", forearm: "#e2b28a", forearmS: "#c08e66",
      pants: "#2a2a2e", pantsS: "#1e1e22", shoe: "#3a3a3e", belt: "#1e1e22",
      torsoExtra: `<path d="M-30,-486Q0,-460 30,-486" stroke="#c07a8a" stroke-width="5" fill="none"/>${TAG()}<path d="M-40,-350H40" stroke="#c07a8a" stroke-width="4"/>`,
      hair: `<path d="M-50,-548Q-56,-612 0,-614Q56,-612 50,-548Q46,-584 2,-588Q-42,-584 -50,-548Z" fill="#231a16" ${OR}/><circle cx="40" cy="-584" r="20" fill="#231a16" ${OR}/><path d="M-50,-556Q-58,-622 0,-626Q58,-622 52,-556" fill="#8d969d" opacity=".3" stroke="#5b6066" stroke-width="2" stroke-dasharray="4 3"/>`,
      face: `<g fill="#e09a86" opacity=".4"><ellipse cx="-24" cy="-524" rx="7" ry="3.5"/><ellipse cx="30" cy="-524" rx="7" ry="3.5"/></g>`,
    },
    wk3: { // the estate's mechanic: grey-blue overalls with grease, a towel round the neck, a red cap backwards
      untuck: true, skin: "#b9805a", skinS: "#98653f", top: "#5f7386", topS: "#4a5a6a", sleeve: "#5f7386", sleeveS: "#4a5a6a", forearm: "#b9805a", forearmS: "#98653f",
      pants: "#5f7386", pantsS: "#4a5a6a", shoe: "#2a2420", belt: "#4a5a6a",
      torsoExtra: `<path d="M-40,-470V-310M40,-470V-310" stroke="#4a5a6a" stroke-width="10"/><rect x="-30" y="-440" width="60" height="58" rx="6" fill="#55687a" ${OR}/><path d="M-50,-488Q0,-460 50,-488L44,-468Q0,-446 -44,-468Z" fill="#f4f2ea" ${OR}/>${[[18, -400, 14], [-30, -350, 10], [30, -330, 8]].map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 0.6}" fill="#2a2420" opacity=".45"/>`).join("")}`,
      hair: `<path d="M-48,-560Q-48,-612 0,-614Q48,-612 48,-560Z" fill="#c8392b" ${OR}/><path d="M-10,-566h-70q-8,0 -4,10h74z" fill="#c8392b" ${OR}/>`,
      face: `<path d="M-30,-508q34,14 64,0" stroke="#5a4636" stroke-width="3" fill="none" stroke-dasharray="3 3" opacity=".6"/>`,
    },
    eg1: { // an estate guard: khaki shirt, the red scarf of คุณวิน's men (like the station guard), black beret with a brass badge
      skin: "#b47a50", skinS: "#94603a", top: "#b9a77a", topS: "#97875e", sleeve: "#b9a77a", sleeveS: "#97875e", forearm: "#b47a50", forearmS: "#94603a",
      pants: "#3f4a3a", pantsS: "#2f382b", shoe: "#1e1e1e", belt: "#2e2a26",
      torsoExtra: `<path d="M-56,-420H56" stroke="#2e2a26" stroke-width="4"/><rect x="14" y="-472" width="30" height="20" rx="3" fill="#2e2a26"/>${SCARF}<rect x="-52" y="-470" width="20" height="12" fill="#c8392b"/>`,
      hair: `<path d="M-50,-566Q-40,-620 12,-618Q58,-612 50,-568Q20,-582 -50,-566Z" fill="#1e1e1e" ${OR}/><circle cx="-28" cy="-590" r="7" fill="#c9a55a"/>`,
      face: `<path d="M-30,-560q8,-6 16,-2M14,-562q8,-4 16,2" stroke="#3a2a1e" stroke-width="4" fill="none"/>`,
    },
    eg2: { // an estate guard: khaki shirt, red scarf, crew cut and a moustache
      skin: "#c48a5e", skinS: "#a36e46", top: "#b9a77a", topS: "#97875e", sleeve: "#b9a77a", sleeveS: "#97875e", forearm: "#c48a5e", forearmS: "#a36e46",
      pants: "#3f4a3a", pantsS: "#2f382b", shoe: "#1e1e1e", belt: "#2e2a26",
      torsoExtra: `<path d="M-56,-420H56" stroke="#2e2a26" stroke-width="4"/>${SCARF}<rect x="14" y="-470" width="30" height="18" rx="3" fill="#2e2a26"/>`,
      hair: `<path d="M-46,-560Q-46,-606 0,-608Q46,-606 46,-560Q30,-574 0,-576Q-30,-574 -46,-560Z" fill="#1c1816" ${OR}/>`,
      face: `<path d="M-14,-516q14,-8 30,0" stroke="#1c1816" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-30,-562q8,-6 16,-2M14,-564q8,-4 16,2" stroke="#1c1816" stroke-width="4" fill="none"/>`,
    },
  });

  Object.assign(Sets, { washroomPov, estateFar, estateGate, estateYard, workshopPov, washroom, canteen, dormNight, notebook, drawing6 });
})();
