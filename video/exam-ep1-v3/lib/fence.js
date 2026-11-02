// "รั้วสุดท้าย" world (lane C · zombie series): บ้านหนองน้ำใส, a rural primary school in the central plains on day 100 after ห่าลง.
// Painted in the house style of ทะเลลด / เห็ดปอบ: layered depth, a named light side, contact shadows, haze, living particles.
// Same layer contract as sets.js (sky / far / mid / set / act / fg · glow above the darkness · light = screen space). Seeded RNG only.
//
//   Sets.fenceYard(L, o)   inside the fence looking at the school: the two-storey cream building (orange tile roof, a blue-railed
//                          corridor, boarded windows), the water tower (แท็งก์น้ำ) on the right, the flagpole with a torn flag on the left,
//                          vegetable beds, banana clumps, rain barrels, the clothesline, sandbags. Ground G = 1420.
//                          o.time day | noon | dusk | night · o.lit (night: the classroom window upstairs glows) · o.gen (the generator on
//                          the ground at x o.gen, #id-gen shakes; o.genOn adds exhaust + lamp) · o.tower {fig: true} (a figure on top: the clue)
//   Sets.fenceGate(L, o)   from inside the yard looking out through the iron gate: the concrete fence both sides with planks nailed across,
//                          the gate (bars, chain, padlock), the road and the paddies beyond. Gate centre x 540, ground G 1420.
//                          o.lock "open" (shackle swung out, hanging: the planted mistake EP.1) | "locked" · o.nail "clean" | "blood" (the nail
//                          on the INNER face of the brace post, x 300 y 1150: EP.3) · o.horde n (ผีห่า silhouettes outside, eyes glow)
//                          · o.open 0..1 (gate leaves swing open, #id-gl / #id-gr) · o.window true (a classroom window frame in fg: the high view)
//                          · o.time · o.mud (footprints in the mud inside the gate: EP.1 end) · o.man (a man lying outside the gate: EP.3)
//   Sets.fenceOut(L, o)    outside on the road: the school name sign over the gate, the fence, the building and tower behind, the road
//                          and fields; o.pickup x (the abandoned pickup by the fence, its fuel flap open: EP.2) · o.hill (the hill on the left;
//                          o.blink true adds #id-blink, the torch on the hill) · o.time
//   Sets.fenceClass(L, o)  the upstairs classroom: chalkboard (o.chalk [line1, line2] in chalk; #id-chalk), wooden desks, the window
//                          on the right with the paddies (dusk/night), a dead ceiling fan, alphabet posters, drawings pinned up, mats and
//                          blankets, candles (night, #id-cand flicker), the old radio on the teacher's desk (#id-radio, #id-rled), o.time
//   Sets.fenceMarket(L, o) the abandoned market: rows of stalls under torn tarps, empty shelves, crates, cans scattered, light shafts
//                          through holes (dusk); o.time
//   Sets.fenceRoad(L, o)   the road back at sunset: the low sun, the paddies, power poles with slack wires, the school far off;
//                          o.horde n (a crowd behind), o.time dusk | noon
//   Sets.fenceCanIns(L, o) insert on a desk: the bulging can (#id-can, lid #id-lid swells), a can opener (#id-op), candle light, o.hand
//   Sets.fenceSiphon(L,o)  insert: the pickup's fuel filler, the hose in it (#id-hose), a jerrycan below (#id-jc), noon sun
//   Sets.fenceNail(L, o)   insert: the brace plank with the nail (#id-nail), o.blood, o.foot (a bare foot coming down on it, #id-foot)
//   Sets.fenceLock(L, o)   insert: the chain and padlock on the gate bars; o.lock open | locked (#id-shackle swings)
//   Sets.fenceRadio(L, o)  insert: the old transistor radio at night, dial glow (#id-glow), needle (#id-needle), candle
//   Fence.horde(x, y, s, n, r, o)   a crowd of ผีห่า silhouettes (back-lit, glowing eyes; class fzz for sway)
//   Fence.can(x, y, s, o)  the can (o.bulge 0..1) · Fence.radio(x, y, s, id) · Fence.padlock(x, y, s, open, id)
//   Fence.life(tl, id, t0, dur)     flag, clouds, grass, clothesline, horde sway, candles
(function () {
  const { mk, f1, put, tree2, cumulus, crown, palm, banana, tuft, blob } = Pop2;
  const INK = "#2a2420";
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const FC = { wall: "#efdcae", wallS: "#cdb487", wallL: "#fbedc8", trim: "#f6f1e4", roof: "#c4532f", roofS: "#8e3420", roofL: "#e2794a",
    rail: "#3d78a8", door: "#3f6f78", doorS: "#2a4c54", conc: "#d9d2c4", concS: "#a9a092", concL: "#f1ece2", iron: "#2f3a3a", ironL: "#5e6e6c",
    rust: "#9a5a32", grass: "#6c9a3e", grassD: "#4a7430", soil: "#8a6a48", soilD: "#5e4630", road: "#5a5650", plank: "#8a6440", plankS: "#5e4228" };
  Sets.DEFS += `
    <linearGradient id="fcSkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f86c8"/><stop offset=".55" stop-color="#8fc0e2"/><stop offset="1" stop-color="#e6eedc"/></linearGradient>
    <linearGradient id="fcSkyNoon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a9ad0"/><stop offset=".5" stop-color="#b6d6ea"/><stop offset="1" stop-color="#fbf2d4"/></linearGradient>
    <linearGradient id="fcSkyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2a5e"/><stop offset=".38" stop-color="#7a4a78"/><stop offset=".7" stop-color="#e2765a"/><stop offset="1" stop-color="#ffc06a"/></linearGradient>
    <linearGradient id="fcSkyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b22"/><stop offset=".5" stop-color="#16205a"/><stop offset="1" stop-color="#3a3270"/></linearGradient>
    <radialGradient id="fcSun"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset=".18" stop-color="#ffe9a8" stop-opacity=".75"/><stop offset=".5" stop-color="#ffc870" stop-opacity=".22"/><stop offset="1" stop-color="#ffc870" stop-opacity="0"/></radialGradient>
    <radialGradient id="fcSunD"><stop offset="0" stop-color="#fff2c0" stop-opacity="1"/><stop offset=".15" stop-color="#ffb860" stop-opacity=".8"/><stop offset=".5" stop-color="#ff7a4a" stop-opacity=".25"/><stop offset="1" stop-color="#ff7a4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="fcMoon"><stop offset="0" stop-color="#fff8e0" stop-opacity=".6"/><stop offset=".4" stop-color="#e8e8ff" stop-opacity=".16"/><stop offset="1" stop-color="#e8e8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="fcPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cc25a"/><stop offset="1" stop-color="#5e8a36"/></linearGradient>
    <linearGradient id="fcPaddyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8925a"/><stop offset="1" stop-color="#5a5a34"/></linearGradient>
    <linearGradient id="fcPaddyN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a4a"/><stop offset="1" stop-color="#141c26"/></linearGradient>
    <linearGradient id="fcGround" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b89a6c"/><stop offset="1" stop-color="#8a6c48"/></linearGradient>
    <linearGradient id="fcWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6e6bc"/><stop offset="1" stop-color="#dcc497"/></linearGradient>
    <linearGradient id="fcRoof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8643a"/><stop offset="1" stop-color="#a8442a"/></linearGradient>
    <linearGradient id="fcTank" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6e8a96"/><stop offset=".35" stop-color="#c8d8de"/><stop offset=".6" stop-color="#9ab2bc"/><stop offset="1" stop-color="#5a727e"/></linearGradient>
    <linearGradient id="fcConc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f1ece2"/><stop offset=".6" stop-color="#d9d2c4"/><stop offset="1" stop-color="#b4ab9c"/></linearGradient>
    <linearGradient id="fcIron" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4e5e5c"/><stop offset=".45" stop-color="#7a8c88"/><stop offset="1" stop-color="#2f3a3a"/></linearGradient>
    <linearGradient id="fcCan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a929a"/><stop offset=".3" stop-color="#eef2f4"/><stop offset=".55" stop-color="#b8c0c6"/><stop offset="1" stop-color="#6a727a"/></linearGradient>
    <linearGradient id="fcLabel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a8281e"/><stop offset=".35" stop-color="#e8483a"/><stop offset="1" stop-color="#8a1e16"/></linearGradient>
    <linearGradient id="fcBoard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e4a3e"/><stop offset="1" stop-color="#22382e"/></linearGradient>
    <linearGradient id="fcFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a7a58"/><stop offset="1" stop-color="#6a5038"/></linearGradient>
    <linearGradient id="fcCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c8" stop-opacity=".4"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></linearGradient>
    <linearGradient id="fcRayD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc888" stop-opacity=".5"/><stop offset="1" stop-color="#ffc888" stop-opacity="0"/></linearGradient>
    <radialGradient id="fcCandle"><stop offset="0" stop-color="#fff2c0" stop-opacity=".95"/><stop offset=".3" stop-color="#ffb860" stop-opacity=".45"/><stop offset="1" stop-color="#ff9a40" stop-opacity="0"/></radialGradient>
    <radialGradient id="fcEye"><stop offset="0" stop-color="#f4ffe0"/><stop offset=".35" stop-color="#b8f0a0" stop-opacity=".8"/><stop offset="1" stop-color="#8ae070" stop-opacity="0"/></radialGradient>
    <radialGradient id="fcAO"><stop offset="0" stop-color="#1a120c" stop-opacity=".6"/><stop offset=".7" stop-color="#1a120c" stop-opacity=".2"/><stop offset="1" stop-color="#1a120c" stop-opacity="0"/></radialGradient>
    <radialGradient id="fcDial"><stop offset="0" stop-color="#ffe9a0" stop-opacity=".95"/><stop offset=".5" stop-color="#ffb850" stop-opacity=".35"/><stop offset="1" stop-color="#ffb850" stop-opacity="0"/></radialGradient>
    <linearGradient id="fcHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4dc" stop-opacity="0"/><stop offset=".7" stop-color="#fff4dc" stop-opacity=".35"/><stop offset="1" stop-color="#fff4dc" stop-opacity="0"/></linearGradient>
    <linearGradient id="fcHazeD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb070" stop-opacity="0"/><stop offset=".7" stop-color="#ffb070" stop-opacity=".32"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></linearGradient>`;

  const SK = { day: "fcSkyDay", noon: "fcSkyNoon", dusk: "fcSkyDusk", night: "fcSkyNight" };
  const PAD = { day: "fcPaddy", noon: "fcPaddy", dusk: "fcPaddyD", night: "fcPaddyN" };
  const LEAF = (t) => (t === "night" ? "n" : t === "dusk" ? "d" : "");
  const tone = (t, day, dusk, night) => (t === "night" ? night : t === "dusk" ? dusk : day);
  const Fence = (window.Fence = window.Fence || {});

  // ---------------- sky: gradient, sun/moon, clouds ----------------
  function sky(L, t, r, o = {}) {
    let s = `<rect x="-1400" y="-900" width="3900" height="2900" fill="url(#${SK[t]})"/>`;
    if (t === "night") {
      for (let k = 0; k < 70; k++) s += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-400 + r() * 1300)}" r="${f1(1 + r() * 2.2)}" fill="#fff" opacity="${f1(0.3 + r() * 0.6)}"/>`;
      const mx = o.moonX ?? 760, my = o.moonY ?? 250;
      s += `<circle cx="${mx}" cy="${my}" r="300" fill="url(#fcMoon)"/><circle cx="${mx}" cy="${my}" r="70" fill="#fff6dc"/><circle cx="${mx - 18}" cy="${my - 10}" r="13" fill="#e8dcc0" opacity=".7"/><circle cx="${mx + 22}" cy="${my + 18}" r="9" fill="#e8dcc0" opacity=".6"/>`;
    } else if (t === "dusk") {
      const sx = o.sunX ?? 300, sy = o.sunY ?? 860;
      s += `<circle cx="${sx}" cy="${sy}" r="520" fill="url(#fcSunD)"/><circle cx="${sx}" cy="${sy}" r="74" fill="#fff0c0"/>`;
    } else {
      const sx = o.sunX ?? (t === "noon" ? 560 : 180), sy = o.sunY ?? (t === "noon" ? 120 : 260);
      s += `<circle cx="${sx}" cy="${sy}" r="${t === "noon" ? 460 : 360}" fill="url(#fcSun)"/><circle cx="${sx}" cy="${sy}" r="${t === "noon" ? 64 : 56}" fill="#fffbe8"/>`;
    }
    const CP = tone(t, ["#c4d6e6", "#eef4f8", "#ffffff"], ["#7a4a6a", "#d8826a", "#ffd0a0"], ["#1e2650", "#2c3466", "#3e4880"]);
    s += `<g class="fcloud">${[[-500, 300, 760], [500, 180, 620], [1500, 340, 700]].map(([x, y, w]) => cumulus(x, y, w, r, CP)).join("")}</g>`;
    put(L.sky, s);
  }
  // far tree line, paddies, sugar palms, a far village roof or two
  function land(L, t, r, y, o = {}) {
    const lineC = tone(t, "#5e8a5a", "#5a3e5a", "#141c2c"), lineC2 = tone(t, "#7aa46a", "#7a4e60", "#1c2638");
    let s = `<path d="M-1400,${y}` + Array.from({ length: 40 }, (_, k) => `Q${-1400 + k * 100 + 50},${f1(y - 50 - r() * 60)} ${-1400 + (k + 1) * 100},${f1(y - 10 - r() * 20)}`).join("") + `V${y + 300}H-1400Z" fill="${lineC2}"/>`;
    s += `<path d="M-1400,${y + 10}` + Array.from({ length: 50 }, (_, k) => `Q${-1400 + k * 80 + 40},${f1(y - 20 - r() * 40)} ${-1400 + (k + 1) * 80},${f1(y + 4 - r() * 12)}`).join("") + `V${y + 300}H-1400Z" fill="${lineC}"/>`;
    put(L.far, s);
    if (o.hill) put(L.sky, `<path d="M-300,${y - 40}Q20,${y - 520} 300,${y - 470}Q520,${y - 430} 760,${y - 40}Z" fill="${tone(t, "#6a8e72", "#5a3a5a", "#141c34")}"/><path d="M140,${y - 480}V${y - 640}M100,${y - 600}h80M110,${y - 550}h60" stroke="${tone(t, "#5a6a72", "#3a2a40", "#2a3048")}" stroke-width="6"/>${o.blink ? `<g id="${o.id}-blink" opacity="0"><circle cx="250" cy="${y - 380}" r="90" fill="url(#fcCandle)"/><circle cx="250" cy="${y - 380}" r="11" fill="#fff8e0"/></g>` : ""}`);
    // paddies with bunds and palms
    let m = `<rect x="-1400" y="${y}" width="3900" height="900" fill="url(#${PAD[t]})"/>`;
    for (let k = 0; k < 8; k++) m += `<path d="M-1400,${f1(y + 30 + k * k * 9)}Q500,${f1(y + 20 + k * k * 9)} 2500,${f1(y + 36 + k * k * 9)}" stroke="${tone(t, "#4e7a2e", "#6a4a2e", "#0c121a")}" stroke-width="${2 + k}" fill="none" opacity=".55"/>`;
    if (t !== "night") for (let k = 0; k < 9; k++) m += `<path d="M${f1(-1200 + r() * 3400)},${f1(y + 40 + r() * 140)}h${f1(60 + r() * 140)}" stroke="${tone(t, "#e8f2d8", "#ffd8a0", "#000")}" stroke-width="3" opacity=".35"/>`;
    [[-900, 0.55], [-300, 0.42], [1400, 0.5], [1900, 0.62]].forEach(([px, s]) => (m += palm(px, y + 30, s, tone(t, "#3e5a3a", "#3a2a3a", "#0a0e16"), tone(t, "#6a8a5a", "#6a4a5a", "#141a26"))));
    put(L.mid, m);
  }

  // ---------------- the school building ----------------
  // x = left end, G = ground, s = scale; 7 bays of 200 wide, ground floor 300 high, first floor 300, roof
  function school(x, G, s, t, o = {}) {
    const bays = o.bays || 7, BW = 200, W = bays * BW, F1 = 300, F2 = 300, night = t === "night";
    const wall = night ? "#3a3a52" : t === "dusk" ? "#e8b890" : "url(#fcWall)", wallS = night ? "#262640" : t === "dusk" ? "#b8806a" : FC.wallS;
    let g = `<ellipse cx="${W / 2}" cy="10" rx="${W * 0.6}" ry="50" fill="url(#fcAO)"/>`;
    // body
    g += `<rect x="0" y="${-F1 - F2}" width="${W}" height="${F1 + F2}" fill="${wall}" ${O()}/>`;
    // corridor floor slab and the deep corridor shadow on both floors
    [0, 1].forEach((fl) => {
      const top = -F1 * (fl + 1), y0 = top + 30;
      g += `<rect x="0" y="${y0}" width="${W}" height="${F1 - 30}" fill="${wallS}" opacity=".55"/>`;
      // doors and windows in the back wall of the corridor
      for (let b = 0; b < bays; b++) {
        const bx = b * BW + 30;
        if (b % 2 === 0) g += `<rect x="${bx + 20}" y="${y0 + 60}" width="70" height="${F1 - 90}" fill="${night ? "#1a2030" : FC.door}" ${O(3)}/><path d="M${bx + 55},${y0 + 60}v${F1 - 90}" stroke="${FC.doorS}" stroke-width="3"/>`;
        else g += `<rect x="${bx}" y="${y0 + 70}" width="140" height="110" fill="${night ? (o.lit && fl === 1 && b === 3 ? "#ffcf72" : "#141a28") : "#5a7a86"}" ${O(3)}/>` +
          (o.boards !== false ? [0, 1, 2].map((k) => `<path d="M${bx - 8},${y0 + 90 + k * 34}l156,${(k % 2 ? -1 : 1) * 10}" stroke="${FC.plank}" stroke-width="16"/><path d="M${bx - 8},${y0 + 90 + k * 34}l156,${(k % 2 ? -1 : 1) * 10}" stroke="${FC.plankS}" stroke-width="2" opacity=".6"/>`).join("") : "");
      }
      // columns and the corridor railing
      for (let b = 0; b <= bays; b++) g += `<rect x="${b * BW - 12}" y="${top}" width="24" height="${F1}" fill="${night ? "#4a4a62" : FC.trim}" ${O(3)}/>`;
      g += `<rect x="-10" y="${top - 6}" width="${W + 20}" height="36" fill="${night ? "#4a4a62" : FC.trim}" ${O(3)}/>`;
      if (fl === 1) g += `<path d="M0,${-F1 + 10}H${W}" stroke="${FC.rail}" stroke-width="12"/>${Array.from({ length: bays * 8 }, (_, k) => `<path d="M${k * 25 + 6},${-F1 + 10}v-90" stroke="${FC.rail}" stroke-width="5"/>`).join("")}<path d="M0,${-F1 - 80}H${W}" stroke="${FC.rail}" stroke-width="12"/><path d="M0,${-F1 - 84}H${W}" stroke="#7ab0d8" stroke-width="3" opacity=".7"/>`;
    });
    // ground step and the stair at the right end
    g += `<rect x="-20" y="-24" width="${W + 40}" height="24" fill="${FC.conc}" ${O(3)}/>`;
    g += `<path d="M${W - 40},0L${W + 120},0L${W + 120},${-F1}L${W - 40},${-F1 + 10}Z" fill="${night ? "#2a2a40" : FC.concS}" ${O(3)}/>` + Array.from({ length: 10 }, (_, k) => `<path d="M${W - 30 + k * 15},${-k * 30}h40" stroke="${INK}" stroke-width="2" opacity=".5"/>`).join("");
    // the roof: hip roof with tiles, a lit front edge
    const ry = -F1 - F2;
    g += `<path d="M-60,${ry + 10}L${W * 0.18},${ry - 170}H${W * 0.82}L${W + 60},${ry + 10}Z" fill="${night ? "#3a2230" : "url(#fcRoof)"}" ${O()}/>`;
    for (let k = 1; k < 7; k++) g += `<path d="M${f1(-60 + k * 7)},${f1(ry + 10 - k * 25)}H${f1(W + 60 - k * 7)}" stroke="${night ? "#22121c" : FC.roofS}" stroke-width="2.4" opacity=".55"/>`;
    g += `<path d="M-60,${ry + 10}H${W + 60}" stroke="${night ? "#5a3a48" : FC.roofL}" stroke-width="8"/><path d="M${W * 0.18},${ry - 170}H${W * 0.82}" stroke="${night ? "#5a3a48" : FC.roofL}" stroke-width="6"/>`;
    // name board on the gable band: อาคาร ๑
    g += `<rect x="${W / 2 - 150}" y="${ry - 6}" width="300" height="56" rx="8" fill="${night ? "#2a3048" : "#2c5a8a"}" ${O(3)}/><text x="${W / 2}" y="${ry + 36}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#fff" opacity="${night ? 0.5 : 1}">อาคารเรียน ๑</text>`;
    // grime streaks and a painted warning
    g += Array.from({ length: 10 }, (_, k) => `<path d="M${40 + k * W / 10},${ry + 30}v${60 + (k % 3) * 40}" stroke="#5a4a3a" stroke-width="10" opacity=".12"/>`).join("");
    if (o.paint !== false) g += `<text x="${BW * 0.5}" y="-60" font-family="Sriracha" font-size="48" fill="#b8281e" opacity=".85" transform="rotate(-3 ${BW * 0.5} -60)">มีคนอยู่ ห้ามยิง</text>`;
    if (night && o.lit) g += `<circle cx="${3 * BW + 100}" cy="${-F1 - 160}" r="200" fill="url(#fcCandle)" opacity=".7"/>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }

  // the water tower: four splayed legs with braces, a ladder, a cylindrical tank, o.fig = a dark figure crouched on top
  function tower(x, G, s, t, o = {}) {
    const night = t === "night", leg = night ? "#2a3040" : "#5a6a72", H = 900;
    let g = `<ellipse cx="0" cy="8" rx="220" ry="30" fill="url(#fcAO)"/>`;
    g += `<path d="M-150,0L-80,${-H}M150,0L80,${-H}M-60,0L-40,${-H}M60,0L40,${-H}" stroke="${leg}" stroke-width="14" stroke-linecap="round"/>`;
    for (let k = 1; k < 5; k++) { const y = -k * H / 5, w = 150 - k * 14; g += `<path d="M${-w},${y}H${w}M${-w},${y}L${w - 14},${y - H / 5}M${w},${y}L${-w + 14},${y - H / 5}" stroke="${leg}" stroke-width="5" opacity=".8"/>`; }
    g += `<path d="M20,0V${-H}M44,0V${-H}" stroke="${leg}" stroke-width="4"/>${Array.from({ length: 30 }, (_, k) => `<path d="M20,${-k * 30}h24" stroke="${leg}" stroke-width="3"/>`).join("")}`;
    g += `<rect x="-130" y="${-H - 20}" width="260" height="22" fill="${leg}" ${O(3)}/>`;
    g += `<path d="M-120,${-H - 20}V${-H - 250}Q0,${-H - 300} 120,${-H - 250}V${-H - 20}Q0,${-H + 10} -120,${-H - 20}Z" fill="${night ? "#30384a" : "url(#fcTank)"}" ${O()}/>`;
    g += `<path d="M-120,${-H - 250}Q0,${-H - 200} 120,${-H - 250}" fill="none" stroke="${INK}" stroke-width="3"/><path d="M-120,${-H - 130}Q0,${-H - 90} 120,${-H - 130}" fill="none" stroke="${night ? "#1a2030" : "#6a828c"}" stroke-width="4"/>`;
    g += `<path d="M-40,${-H - 260}Q0,${-H - 340} 40,${-H - 260}" fill="${night ? "#2a3040" : "#8aa0aa"}" ${O(3)}/><path d="M-90,${-H - 230}V${-H - 60}" stroke="#fff" stroke-width="6" opacity="${night ? 0.08 : 0.35}"/>`;
    g += `<text x="0" y="${-H - 140}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="44" fill="${night ? "#5a6a8a" : "#2c5a8a"}">บ.น.ส.</text>`;
    g += Array.from({ length: 6 }, (_, k) => `<path d="M${-100 + k * 40},${-H - 40}v${30 + (k % 2) * 30}" stroke="${FC.rust}" stroke-width="5" opacity=".5"/>`).join("");
    if (o.fig) g += `<g id="${o.id}-fig"><path d="M-20,${-H - 290}q-6,-40 14,-60q24,-6 30,18q8,30 -4,44Z" fill="#0a0c14"/><circle cx="6" cy="${-H - 362}" r="18" fill="#0a0c14"/></g>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }
  // the flagpole with a faded, torn flag (#id-flag waves)
  const flagpole = (x, G, s, id, t) => `<g transform="translate(${x},${G}) scale(${s})"><rect x="-40" y="-30" width="80" height="30" fill="${FC.conc}" ${O(3)}/><rect x="-6" y="-900" width="12" height="880" fill="#d8dce0" ${O(2.5)}/><circle cy="-906" r="12" fill="#e8c860" ${O(2.5)}/>
    <g id="${id}-flag"><path d="M6,-880H186Q176,-842 190,-806L170,-790Q186,-770 176,-760H6Z" fill="#c8303a" opacity="${t === "night" ? 0.5 : 0.9}" ${O(2.5)}/><path d="M6,-856H184M6,-788H178" stroke="#f4f0e8" stroke-width="14" opacity="${t === "night" ? 0.4 : 0.85}"/><path d="M6,-834H186V-810H6Z" fill="#2c3a8a" opacity="${t === "night" ? 0.4 : 0.85}"/></g></g>`;

  // ---------------- the fence: concrete posts, a low wall, steel bars, planks nailed across, broken glass on top ----------------
  function fenceRun(x0, x1, G, s, t, o = {}) {
    const night = t === "night", H = 300 * s, P = 160 * s;
    let g = "";
    const wallC = night ? "#3a3c50" : "url(#fcConc)";
    g += `<rect x="${x0}" y="${G - H * 0.42}" width="${x1 - x0}" height="${H * 0.42}" fill="${wallC}" ${O(3)}/>`;
    g += `<path d="M${x0},${G - H * 0.42 + 26 * s}H${x1}" stroke="${night ? "#2a3048" : "#3d78a8"}" stroke-width="${14 * s}"/>`;
    for (let x = x0; x < x1; x += 18 * s) g += `<path d="M${f1(x)},${f1(G - H * 0.42)}V${f1(G - H)}" stroke="${night ? "#1a1e28" : FC.iron}" stroke-width="${5 * s}"/>`;
    g += `<path d="M${x0},${f1(G - H + 14 * s)}H${x1}" stroke="${night ? "#1a1e28" : FC.iron}" stroke-width="${8 * s}"/>`;
    for (let x = x0; x <= x1; x += P) g += `<rect x="${f1(x - 16 * s)}" y="${f1(G - H - 20 * s)}" width="${f1(32 * s)}" height="${f1(H + 20 * s)}" fill="${night ? "#44465a" : FC.concL}" ${O(3)}/><rect x="${f1(x + 4 * s)}" y="${f1(G - H - 20 * s)}" width="${f1(12 * s)}" height="${f1(H + 20 * s)}" fill="${night ? "#2a2c3a" : FC.concS}" opacity=".6"/>`;
    // planks nailed across the bars, with nail heads
    if (o.planks !== false) for (let x = x0 + 40 * s; x < x1 - 60 * s; x += 260 * s) {
      const y = G - H * (0.6 + ((x / 97) % 1) * 0.25), rot = (((x / 53) % 1) - 0.5) * 10;
      g += `<g transform="rotate(${f1(rot)} ${f1(x + 90 * s)} ${f1(y)})"><rect x="${f1(x)}" y="${f1(y - 14 * s)}" width="${f1(190 * s)}" height="${f1(28 * s)}" fill="${night ? "#3a3028" : FC.plank}" ${O(2.5)}/><path d="M${f1(x + 6 * s)},${f1(y)}h${f1(170 * s)}" stroke="${FC.plankS}" stroke-width="2" opacity=".6"/><circle cx="${f1(x + 14 * s)}" cy="${f1(y)}" r="${f1(3.5 * s)}" fill="#c8ccd0"/><circle cx="${f1(x + 176 * s)}" cy="${f1(y)}" r="${f1(3.5 * s)}" fill="#c8ccd0"/></g>`;
    }
    // broken glass along the top of the wall line
    for (let x = x0; x < x1; x += 22 * s) g += `<path d="M${f1(x)},${f1(G - H * 0.42)}l${f1(6 * s)},${f1(-14 * s)}l${f1(6 * s)},${f1(14 * s)}" fill="${night ? "#4a6a6a" : "#8ad0b8"}" opacity=".7"/>`;
    if (o.sign) g += `<g transform="translate(${o.sign[0]},${G - H * 0.24})"><text text-anchor="middle" font-family="Sriracha" font-size="${46 * s}" fill="#b8281e" opacity=".9">${o.sign[1]}</text></g>`;
    return g;
  }
  // the padlock (open: the shackle swung out, the body hanging off the chain)
  Fence.padlock = (x, y, s, open, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>
    ${open ? `<g id="${id}-shackle"><path d="M-22,-30V-96Q-22,-124 0,-124Q22,-124 22,-96V-80" fill="none" stroke="#c8ccd0" stroke-width="11" stroke-linecap="round"/>
      <path d="M-22,-30V-96Q-22,-124 0,-124Q22,-124 22,-96V-80" fill="none" stroke="#7a8288" stroke-width="3"/></g>`
    : `<path id="${id}-shackle" d="M-22,-28V-62Q-22,-90 0,-90Q22,-90 22,-62V-28" fill="none" stroke="#c8ccd0" stroke-width="11" stroke-linecap="round"/><path d="M-22,-28V-62Q-22,-90 0,-90Q22,-90 22,-62V-28" fill="none" stroke="#7a8288" stroke-width="3"/>`}
    <rect x="-40" y="-34" width="80" height="78" rx="12" fill="#d8a83a" ${O(3.5)}/><rect x="-40" y="-34" width="22" height="78" rx="10" fill="#f2cc6a" opacity=".7"/>
    <path d="M18,-30v70" stroke="#a8781e" stroke-width="5" opacity=".6"/><circle cx="0" cy="6" r="9" fill="#3a2a10"/><path d="M0,10v16" stroke="#3a2a10" stroke-width="6"/></g></g>`;
  // the iron gate: two leaves of bars between concrete pillars, a chain, the padlock
  function gate(cx, G, s, t, o = {}) {
    const night = t === "night", W = 520, H = 360, iron = night ? "#1a2028" : "url(#fcIron)", ironS = night ? "#10141a" : FC.iron;
    const leaf = (side) => {
      const x0 = side < 0 ? -W / 2 : 0;
      let g = `<rect x="${x0 + 8}" y="${-H}" width="${W / 2 - 16}" height="${H - 10}" fill="none" stroke="${ironS}" stroke-width="12"/>`;
      for (let k = 1; k < 9; k++) g += `<path d="M${x0 + 8 + k * (W / 2 - 16) / 9},${-H}V-10" stroke="${ironS}" stroke-width="6"/>`;
      g += `<path d="M${x0 + 8},${-H * 0.55}H${x0 + W / 2 - 8}M${x0 + 8},${-H * 0.2}H${x0 + W / 2 - 8}" stroke="${ironS}" stroke-width="9"/>`;
      g += Array.from({ length: 9 }, (_, k) => `<path d="M${x0 + 8 + k * (W / 2 - 16) / 9 - 6},${-H}l6,-22l6,22" fill="${ironS}"/>`).join("");
      g += `<path d="M${x0 + 12},${-H + 4}V-14" stroke="${night ? "#3a4858" : FC.ironL}" stroke-width="3" opacity=".7"/>`;
      g += Array.from({ length: 5 }, (_, k) => `<path d="M${x0 + 30 + k * 50},${-H * 0.55 + 6}v${18 + k * 4}" stroke="${FC.rust}" stroke-width="4" opacity=".55"/>`).join("");
      return g;
    };
    const op = o.open || 0;
    let g = `<ellipse cx="0" cy="6" rx="${W * 0.7}" ry="22" fill="url(#fcAO)"/>`;
    g += `<g id="${o.id}-gl"><g transform="translate(${-W / 2},0) scale(${f1(1 - op * 0.75)},1) translate(${W / 2},0)">${leaf(-1)}</g></g>`;
    g += `<g id="${o.id}-gr"><g transform="translate(${W / 2},0) scale(${f1(1 - op * 0.75)},1) translate(${-W / 2},0)">${leaf(1)}</g></g>`;
    // the chain round the two middle bars, the padlock hanging
    if (!op) g += `<g id="${o.id}-chain"><path d="M-30,${-H * 0.5}q15,18 30,0q15,18 30,0M-30,${-H * 0.5 + 26}q15,-18 30,0q15,-18 30,0" fill="none" stroke="#c8ccd0" stroke-width="7"/>
      <path d="M-30,${-H * 0.5}q15,18 30,0q15,18 30,0" fill="none" stroke="#5a6268" stroke-width="2"/>${Fence.padlock(o.lock === "open" ? 28 : 0, -H * 0.5 + (o.lock === "open" ? 100 : 74), 0.8, o.lock === "open", `${o.id}-lock`)}</g>`;
    // pillars
    [-1, 1].forEach((sd) => {
      const px = sd * (W / 2 + 40);
      g += `<rect x="${px - 44}" y="${-H - 80}" width="88" height="${H + 80}" fill="${night ? "#44465a" : FC.concL}" ${O()}/><rect x="${px + (sd < 0 ? 10 : -44)}" y="${-H - 80}" width="34" height="${H + 80}" fill="${night ? "#2a2c3a" : FC.concS}" opacity=".55"/>
        <rect x="${px - 54}" y="${-H - 100}" width="108" height="26" fill="${night ? "#555770" : FC.trim}" ${O(3)}/>`;
    });
    return `<g transform="translate(${f1(cx)},${f1(G)}) scale(${s})">${g}</g>`;
  }

  // ---------------- props ----------------
  const barrel = (x, G, s, c = "#2c6aa8") => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cx="0" cy="4" rx="70" ry="14" fill="url(#fcAO)"/><path d="M-50,0V-150Q0,-160 50,-150V0Q0,8 -50,0Z" fill="${c}" ${O(3)}/><ellipse cx="0" cy="-150" rx="50" ry="10" fill="#1a3a5a" ${O(3)}/><path d="M-50,-50Q0,-40 50,-50M-50,-100Q0,-90 50,-100" stroke="${INK}" stroke-width="2.5" fill="none" opacity=".5"/><path d="M-34,-140V-10" stroke="#fff" stroke-width="7" opacity=".3"/></g>`;
  const sandbags = (x, G, s, n = 5) => `<g transform="translate(${x},${G}) scale(${s})">${Array.from({ length: n }, (_, k) => { const row = k < 3 ? 0 : 1, i = row ? k - 3 : k; return `<path d="M${-110 + i * 80 + row * 40},${-row * 46}q-6,-44 34,-46h20q40,2 34,46Z" fill="#c8b48a" ${O(3)}/><path d="M${-98 + i * 80 + row * 40},${-row * 46 - 22}h60" stroke="#8a7a5a" stroke-width="2.5" opacity=".7"/>`; }).join("")}</g>`;
  const bed = (x, G, s, t) => `<g transform="translate(${x},${G}) scale(${s})"><path d="M-160,0L-140,-36H140L160,0Z" fill="${FC.soilD}" ${O(3)}/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-120 + k * 30},-30q-10,-40 0,-60q10,20 0,60M${-120 + k * 30},-30q14,-30 24,-40" stroke="${tone(t, "#4e9a3a", "#6a8a3a", "#1a2a20")}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
  const line = (x0, x1, y, id, t) => `<g id="${id}-cl"><path d="M${x0},${y}Q${(x0 + x1) / 2},${y + 40} ${x1},${y}" stroke="#d8d4c8" stroke-width="3" fill="none"/>
    ${[[0.25, "#e85a4a"], [0.45, "#f6f2e8"], [0.65, "#3a7ac8"]].map(([u, c], k) => { const x = x0 + (x1 - x0) * u, yy = y + 40 * 4 * u * (1 - u); return `<g class="fcloth"><path d="M${f1(x - 30)},${f1(yy)}h60l-6,${70 + k * 10}h-48Z" fill="${c}" opacity="${t === "night" ? 0.4 : 1}" ${O(2.5)}/></g>`; }).join("")}</g>`;
  // the generator: a red open-frame genset (#id-gen), o.on = exhaust puffs + its work lamp
  Fence.gen = (x, G, s, id, on) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cx="0" cy="4" rx="130" ry="18" fill="url(#fcAO)"/><g id="${id}-gen">
    <path d="M-110,0V-120H110V0M-110,-120H110M-110,-60H110" stroke="#2a2a2a" stroke-width="9" fill="none"/>
    <rect x="-90" y="-112" width="120" height="90" rx="10" fill="#d8392e" ${O(3)}/><rect x="-80" y="-104" width="40" height="70" rx="6" fill="#f06a5a" opacity=".6"/><rect x="40" y="-100" width="60" height="70" rx="6" fill="#3a3a3a" ${O(3)}/>
    <circle cx="70" cy="-66" r="20" fill="#5a5a5a" stroke="#222" stroke-width="3"/><rect x="-60" y="-150" width="110" height="34" rx="12" fill="#e8483a" ${O(3)}/><circle cx="-50" cy="-133" r="8" fill="#222"/>
    <text x="-30" y="-50" font-family="Kanit" font-weight="800" font-size="20" fill="#fff">5.5 kW</text></g></g>`;
  // the can: o.bulge 0..1 swells the lid into a dome, o.label (red, a fish), o.dent
  Fence.can = (x, y, s, o = {}) => {
    const b = o.bulge ?? 0, id = o.id || "";
    return `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="8" rx="110" ry="22" fill="url(#fcAO)"/><g ${id ? `id="${id}"` : ""}>
      <path d="M-80,-180V0Q0,24 80,0V-180" fill="url(#fcCan)" ${O(4)}/><path d="M-80,-150Q0,-128 80,-150V-40Q0,-18 -80,-40Z" fill="url(#fcLabel)" ${O(3)}/>
      <path d="M-50,-92q30,-26 64,0q-34,26 -64,0zM14,-92l18,-14v28z" fill="#ffd8a0" ${O(2.5)}/><circle cx="-28" cy="-96" r="4" fill="${INK}"/>
      <text x="0" y="-52" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="22" fill="#fff">ปลาซาร์ดีน</text>
      <path d="M-80,-170Q0,-148 80,-170M-80,-12Q0,10 80,-12" stroke="${INK}" stroke-width="2.4" fill="none" opacity=".6"/>
      <path d="M-58,-176V-6" stroke="#fff" stroke-width="10" opacity=".55"/>
      <g ${id ? `id="${id}-lid"` : ""}><path d="M-80,-180Q-80,${f1(-202 - b * 70)} 0,${f1(-204 - b * 78)}Q80,${f1(-202 - b * 70)} 80,-180Q0,-160 -80,-180Z" fill="#dfe4e8" ${O(4)}/>
        <path d="M-50,${f1(-188 - b * 30)}Q0,${f1(-206 - b * 66)} 50,${f1(-188 - b * 30)}" stroke="#fff" stroke-width="6" fill="none" opacity=".8"/><ellipse cx="0" cy="${f1(-188 - b * 40)}" rx="${f1(26 - b * 6)}" ry="${f1(7 + b * 2)}" fill="none" stroke="#8a929a" stroke-width="3"/></g>
      ${o.leak ? `<path d="M64,-150q10,40 4,90" stroke="#c8a050" stroke-width="7" fill="none" stroke-linecap="round" opacity=".85"/><circle cx="68" cy="-54" r="7" fill="#c8a050"/>` : ""}</g></g>`;
  };
  // the old transistor radio: wood case, a speaker grille, the tuning dial lit amber (#id-glow), a needle (#id-needle), an aerial
  Fence.radio = (x, y, s, id) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="6" rx="260" ry="30" fill="url(#fcAO)"/>
    <path d="M150,-170L260,-470" stroke="#c8ccd0" stroke-width="7" stroke-linecap="round"/><circle cx="260" cy="-470" r="8" fill="#e8ecf0" ${O(2)}/>
    <rect x="-220" y="-190" width="440" height="190" rx="26" fill="#7a4a2a" ${O(4)}/><rect x="-220" y="-190" width="440" height="34" rx="16" fill="#9a6a42" opacity=".7"/>
    <rect x="-196" y="-160" width="200" height="140" rx="16" fill="#3a2a1e" ${O(3)}/>${Array.from({ length: 9 }, (_, k) => `<path d="M-186,${-148 + k * 14}h180" stroke="#6a5038" stroke-width="5"/>`).join("")}
    <g id="${id}-glow" opacity=".4"><rect x="20" y="-160" width="180" height="70" rx="10" fill="url(#fcDial)"/><circle cx="110" cy="-125" r="120" fill="url(#fcDial)" opacity=".5"/></g>
    <rect x="20" y="-160" width="180" height="70" rx="10" fill="#f2e2b0" opacity=".5" ${O(3)}/>${Array.from({ length: 12 }, (_, k) => `<path d="M${34 + k * 14},-150v${k % 3 ? 10 : 18}" stroke="#5a4020" stroke-width="2.5"/>`).join("")}
    <text x="110" y="-100" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="16" fill="#5a4020">AM  540 · 1600</text>
    <path id="${id}-needle" d="M80,-160V-92" stroke="#d8281e" stroke-width="4"/>
    <circle cx="60" cy="-46" r="28" fill="#c8a878" ${O(3)}/><circle cx="160" cy="-46" r="28" fill="#c8a878" ${O(3)}/><path d="M60,-70v14M160,-70v14" stroke="${INK}" stroke-width="4"/>
    <path id="${id}-rled" d="M-200,-176h12" stroke="#ff4a3a" stroke-width="7" stroke-linecap="round" opacity=".3"/></g>`;
  // a crowd of ผีห่า: hunched silhouettes with glowing eyes, darker at the back; class fzz sways
  Fence.horde = (x, y, s, n, r, o = {}) => {
    let g = "";
    const col = o.col || "#141820", rim = o.rim || "#8ab0a0";
    for (let k = 0; k < n; k++) {
      const px = (r() - 0.5) * (o.w || 700), py = r() * (o.d || 120), sc = 0.7 + (py / (o.d || 120)) * 0.5, lean = (r() - 0.5) * 18, arm = r() > 0.5;
      g += `<g class="fzz" transform="translate(${f1(px)},${f1(py)}) scale(${f1(sc)})"><g transform="rotate(${f1(lean)})">
        <path d="M-26,0L-18,-120Q-40,-200 -10,-250Q20,-262 34,-232Q50,-190 26,-120L32,0Z" fill="${col}"/><circle cx="6" cy="-272" r="26" fill="${col}"/>
        ${arm ? `<path d="M-20,-220Q-70,-200 -96,-170" stroke="${col}" stroke-width="18" stroke-linecap="round" fill="none"/>` : `<path d="M28,-214Q60,-170 52,-120" stroke="${col}" stroke-width="16" stroke-linecap="round" fill="none"/>`}
        <path d="M-30,-250Q-8,-266 18,-262" stroke="${rim}" stroke-width="3" fill="none" opacity=".5"/>
        <circle cx="-4" cy="-274" r="10" fill="url(#fcEye)"/><circle cx="16" cy="-274" r="10" fill="url(#fcEye)"/><circle cx="-4" cy="-274" r="3" fill="#f4ffe0"/><circle cx="16" cy="-274" r="3" fill="#f4ffe0"/></g></g>`;
    }
    return `<g transform="translate(${x},${y}) scale(${s})">${g}</g>`;
  };
  // footprints in mud: a line of bare human prints (left / right, toes), getting smaller with distance
  Fence.prints = (x0, y0, x1, y1, n) => Array.from({ length: n }, (_, k) => {
    const u = k / (n - 1), x = x0 + (x1 - x0) * u + (k % 2 ? 22 : -22) * (1 - u * 0.5), y = y0 + (y1 - y0) * u, sc = 1 - u * 0.55, fl = k % 2 ? -1 : 1;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(sc * fl)},${f1(sc * 0.55)})"><path d="M-14,30q-6,-40 4,-58q16,-12 22,6q4,30 -4,52q-10,8 -22,0z" fill="#3a2a1a" opacity=".75"/>${[[-10, -42], [-1, -46], [8, -44], [15, -38], [20, -30]].map(([a, b], i) => `<circle cx="${a}" cy="${b}" r="${4.4 - i * 0.5}" fill="#3a2a1a" opacity=".75"/>`).join("")}</g>`;
  }).join("");

  // camp life props for the yard (V10 detail): water jars, a bicycle, stacked chairs, a playground slide, a cooking corner, firewood, hopscotch
  const jar = (x, G, s, t) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="4" rx="80" ry="14" fill="url(#fcAO)"/><path d="M-40,-150Q-80,-120 -70,-60Q-60,0 0,0Q60,0 70,-60Q80,-120 40,-150Z" fill="${tone(t, "#8a4a2a", "#7a3a2a", "#2a1a18")}" ${O(3)}/><ellipse cy="-150" rx="42" ry="10" fill="#3a2418" ${O(3)}/><path d="M-60,-100Q0,-86 60,-100" stroke="#e8c860" stroke-width="5" fill="none" opacity=".7"/><path d="M-50,-130Q-62,-80 -46,-30" stroke="#fff" stroke-width="7" opacity=".25" fill="none"/></g>`;
  const bike = (x, G, s, t) => { const c = tone(t, "#2c6aa8", "#3a4a7a", "#1a2030"); return `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="4" rx="150" ry="14" fill="url(#fcAO)"/>${[-90, 90].map((wx) => `<circle cx="${wx}" cy="-60" r="58" fill="none" stroke="${INK}" stroke-width="7"/><circle cx="${wx}" cy="-60" r="6" fill="${INK}"/>`).join("")}<path d="M-90,-60L-20,-60L40,-140L-50,-140ZM-20,-60L-56,-170M90,-60L46,-170M40,-140L46,-170" stroke="${c}" stroke-width="9" fill="none" stroke-linejoin="round"/><path d="M-76,-174h40M30,-178l34,-4" stroke="${INK}" stroke-width="9" stroke-linecap="round"/><rect x="-40" y="-120" width="70" height="40" fill="#c8945a" ${O(3)}/></g>`; };
  const chairs = (x, G, s, t) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="4" rx="70" ry="12" fill="url(#fcAO)"/>${[0, 1, 2, 3].map((k) => `<path d="M-50,${-k * 14}L-46,${-100 - k * 14}H46L50,${-k * 14}M-50,${-60 - k * 14}H50M-40,${-100 - k * 14}V${-170 - k * 14}H40V${-100 - k * 14}" fill="none" stroke="${tone(t, ["#e8483a", "#2fa864", "#2f6fd0", "#f2c83a"][k], "#8a5a5a", "#2a2a38")}" stroke-width="9" stroke-linejoin="round"/>`).join("")}</g>`;
  const slide = (x, G, s, t) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="4" rx="220" ry="20" fill="url(#fcAO)"/><path d="M-140,0V-260M-90,0V-260" stroke="${tone(t, "#d8392e", "#8a3a3a", "#2a1a1e")}" stroke-width="10"/>${Array.from({ length: 6 }, (_, k) => `<path d="M-140,${-40 - k * 40}H-90" stroke="${INK}" stroke-width="5"/>`).join("")}<path d="M-90,-260L180,-10L200,0L210,-14L-70,-280Z" fill="${tone(t, "#f2c83a", "#a88a4a", "#2a2820")}" ${O(3)}/><path d="M-80,-266L190,-16" stroke="#fff" stroke-width="5" opacity=".5"/><rect x="-150" y="-280" width="80" height="22" fill="#3a8ad0" ${O(3)}/></g>`;
  const cook = (x, G, s, t, id) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="4" rx="140" ry="18" fill="url(#fcAO)"/>${[-50, 0, 50].map((k, i) => `<rect x="${k - 22}" y="-40" width="44" height="40" fill="#8a8478" ${O(2.5)}/>`).join("")}<path d="M-60,-40Q0,-30 60,-40V-110Q0,-124 -60,-110Z" fill="#3a3a3e" ${O(3)}/><ellipse cy="-112" rx="62" ry="12" fill="#22222a" ${O(3)}/><path d="M-62,-90Q0,-80 62,-90" stroke="#5a5a62" stroke-width="4" fill="none"/>
    <g fill="${tone(t, "#e86a2a", "#ff8a3a", "#ff9a40")}"><path d="M-30,-40q-6,-20 6,-34q4,18 14,6q4,16 -6,28Z"/><path d="M10,-40q-4,-16 8,-26q2,14 10,6q2,12 -6,20Z"/></g>${[-120, -100, 100, 120].map((wx, i) => `<path d="M${wx},0l${i < 2 ? 50 : -50},-14" stroke="#6a4630" stroke-width="12" stroke-linecap="round"/>`).join("")}</g>`;
  const firewood = (x, G, s) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="4" rx="110" ry="12" fill="url(#fcAO)"/>${Array.from({ length: 7 }, (_, k) => `<g transform="translate(${-70 + (k % 4) * 46 + Math.floor(k / 4) * 23},${-18 - Math.floor(k / 4) * 32})"><circle r="18" fill="#a8784a" ${O(2.5)}/><circle r="9" fill="none" stroke="#7a5034" stroke-width="2"/></g>`).join("")}</g>`;
  const hop = (x, G, t) => `<g opacity=".7" stroke="${tone(t, "#f4f0e4", "#f0d8c0", "#5a5a6a")}" stroke-width="5" fill="none">${[0, 1, 2].map((k) => `<path d="M${x - 60 + k * 30},${G - k * 60}h120v-60h-120z"/>`).join("")}<text x="${x}" y="${G - 200}" text-anchor="middle" font-family="Mali" font-size="40" fill="${tone(t, "#f4f0e4", "#f0d8c0", "#5a5a6a")}" stroke="none">บ้าน</text></g>`;
  // ---------------- Sets.fenceYard ----------------
  function fenceYard(L, o = {}) {
    const id = o.id || "fy", t = o.time || "day", r = mk(o.seed || 31), G = 1420;
    sky(L, t, r, o); land(L, t, r, 1060, { hill: false });
    // the back fence beyond the school, a few roofs of the village
    put(L.mid, `<g opacity=".95">${fenceRun(-1400, 2500, 1110, 0.6, t, { planks: false })}</g>`);
    let s = "";
    s += `<rect x="-1400" y="${G - 300}" width="3900" height="1200" fill="${tone(t, "url(#fcGround)", "#a8785a", "#2a2a38")}"/>`;
    // the yard: worn dirt with grass tufts, a football goal, puddles
    for (let k = 0; k < 40; k++) s += `<path d="M${f1(-1200 + r() * 3400)},${f1(G - 280 + r() * 600)}q6,-24 12,0q6,-18 12,0" stroke="${tone(t, FC.grass, "#7a6a3a", "#1a2a24")}" stroke-width="4" fill="none"/>`;
    s += school(-760, G - 250, 0.95, t, { lit: o.lit });
    s += tower(1180, G - 230, 0.62, t, { fig: o.tower && o.tower.fig, id });
    s += flagpole(-930, G - 120, 0.9, id, t);
    s += tree2(1620, G - 180, 0.9, r, { leaf: [`p2LeafD${LEAF(t)}`, `p2LeafM${LEAF(t)}`, `p2LeafL${LEAF(t)}`], bark: tone(t, "#6a4a32", "#5a3a2a", "#0e0a08"), barkS: tone(t, "#3e2a1c", "#3a2418", "#060404"), fleck: tone(t, "#c8dc8a", "#e8c080", "#2a3e30") });
    s += line(-1180, -520, G - 260, id, t);
    s += bed(-120, G + 60, 1, t) + bed(240, G + 70, 1, t);
    s += barrel(620, G + 40, 1.0) + barrel(740, G + 70, 0.95, "#3a8a5a") + sandbags(1000, G + 120, 1.1);
    s += hop(380, G + 260, t) + slide(1400, G - 120, 0.75, t) + jar(-420, G + 30, 0.9, t) + jar(-330, G + 50, 0.8, t) + chairs(860, G - 60, 0.8, t)
      + bike(-700, G + 40, 0.95, t) + cook(160, G - 70, 0.85, t, id) + firewood(320, G - 50, 0.8);
    s += banana(-1180, G + 120, 1.1, tone(t, ["#4a6a3a", "#3e7a3a", "#5a9a44"], ["#5a4a3a", "#6a5a3a", "#8a6a44"], ["#0e1610", "#121c14", "#16221a"]));
    if (o.gen !== undefined) s += Fence.gen(o.gen, G + 140, 1.1, id, o.genOn);
    put(L.set, s);
    put(L.set, `<rect x="-1400" y="${G - 500}" width="3900" height="300" fill="url(#${t === "dusk" ? "fcHazeD" : "fcHaze"})" opacity="${t === "night" ? 0.15 : 0.6}"/>`);
    if (t === "night") put(L.glow, `<g id="${id}-cand"><circle cx="${-760 + (3 * 200 + 100) * 0.95}" cy="${G - 250 - 460 * 0.95}" r="${o.lit ? 260 : 0}" fill="url(#fcCandle)" opacity=".5"/></g>`);
    if (o.genOn) put(L.glow, `<g id="${id}-lamp"><circle cx="${o.gen}" cy="${G - 60}" r="360" fill="url(#fcCandle)" opacity=".8"/></g>`);
    put(L.fg, tuft ? `<g>${[-300, 1300].map((x) => `<path d="M${x},2000q30,-200 60,-260q10,120 40,250Z" fill="${tone(t, FC.grassD, "#5a4a2a", "#0a100c")}"/>`).join("")}</g>` : "");
  }

  // ---------------- Sets.fenceGate ----------------
  function fenceGate(L, o = {}) {
    const id = o.id || "fg", t = o.time || "day", r = mk(o.seed || 41), G = 1420;
    sky(L, t, r, { sunX: 700, ...o }); land(L, t, r, 1000, {});
    // the road beyond the gate, receding
    put(L.mid, `<path d="M380,1000L700,1000L1500,1700H-400Z" fill="${tone(t, "#8a8478", "#7a5a5a", "#1e2230")}"/><path d="M540,1004L540,1700" stroke="${tone(t, "#f2ead0", "#e8c090", "#3a3e50")}" stroke-width="8" stroke-dasharray="40 50" opacity=".7"/>
      ${[[-200, 0.6], [1260, 0.7], [1700, 0.85]].map(([x, s]) => `<g transform="translate(${x},1010) scale(${s})"><path d="M-6,0V-520" stroke="${tone(t, "#6a5a4a", "#4a3a3a", "#141820")}" stroke-width="16"/><path d="M-60,-490H60" stroke="${tone(t, "#6a5a4a", "#4a3a3a", "#141820")}" stroke-width="10"/></g>`).join("")}
      <path d="M-300,700Q540,780 2400,640" stroke="${tone(t, "#3a3a3a", "#2a2028", "#0a0c12")}" stroke-width="3" fill="none"/>`);
    let s = `<rect x="-1400" y="${G - 60}" width="3900" height="900" fill="${tone(t, "url(#fcGround)", "#8a6050", "#22222e")}"/>`;
    if (o.horde) s += `<g id="${id}-horde">${Fence.horde(560, G - 120, 0.9, o.horde, r, { w: 1500, d: 90, col: tone(t, "#2a3030", "#1a1418", "#06080c"), rim: tone(t, "#c8d8c8", "#ffb880", "#8ab0d0") })}</g>`;
    if (o.mud) s += `<path d="M260,${G + 40}Q540,${G - 10} 840,${G + 50}Q860,${G + 260} 540,${G + 300}Q220,${G + 260} 260,${G + 40}Z" fill="${tone(t, "#6a5038", "#5a3a2a", "#141420")}"/>` + Fence.prints(560, G + 260, 520, G - 30, 7);
    if (o.man) s += `<g transform="translate(600,1330) scale(.85)"><ellipse cx="0" cy="10" rx="200" ry="24" fill="url(#fcAO)"/><path d="M-170,0Q-120,-46 -40,-40L120,-30Q170,-26 180,0Z" fill="#e8823a" ${O(4)}/><circle cx="-180" cy="-24" r="30" fill="#b8865a" ${O(4)}/><path d="M120,-6H200" stroke="#f2f2f2" stroke-width="22"/></g>`;
    // fence runs both sides of the gate, gate in the middle
    s += fenceRun(-1400, 230, G, 1.25, t, { sign: [-500, "ห้ามเข้า มีคน"] }) + fenceRun(850, 2500, G, 1.25, t, {});
    s += gate(540, G, 1.0, t, { id, lock: o.lock || "locked", open: o.open || 0 });
    // the brace post leaning inside, with its nail (EP.3)
    s += `<g transform="translate(300,${G})"><path d="M-30,0L40,-460L80,-450L10,0Z" fill="${tone(t, FC.plank, "#7a5040", "#2a221c")}" ${O(3)}/><path d="M-10,-10L52,-440" stroke="${FC.plankS}" stroke-width="3" opacity=".6"/>
      <g id="${id}-nail"><path d="M18,-250l40,-9" stroke="#9aa0a6" stroke-width="7" stroke-linecap="round"/><circle cx="18" cy="-249" r="8" fill="#c8ccd0" stroke="#2a2420" stroke-width="2"/>${o.nail === "blood" ? `<path d="M34,-256l22,-5" stroke="#b81a12" stroke-width="8" stroke-linecap="round"/><path d="M30,-246q-4,24 4,44M44,-250q2,14 -2,26" stroke="#9a1810" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="33" cy="-198" r="5" fill="#9a1810"/>` : ""}</g></g>`;
    s += sandbags(900, G + 110, 1.1, 5) + barrel(-160, G + 80, 1.0);
    put(L.set, s);
    if (o.window) put(L.fg, `<g><rect x="-1400" y="-900" width="3900" height="560" fill="#5a4630"/><rect x="-1400" y="1700" width="3900" height="900" fill="#5a4630"/><rect x="-1400" y="-900" width="1440" height="3600" fill="#5a4630"/><rect x="1040" y="-900" width="1400" height="3600" fill="#5a4630"/>
      <path d="M40,-340H1040V1700H40Z" fill="none" stroke="#3a2a1a" stroke-width="40"/><path d="M540,-340V1700M40,700H1040" stroke="#6a5038" stroke-width="22"/></g>`);
  }

  // ---------------- Sets.fenceOut ----------------
  function fenceOut(L, o = {}) {
    const id = o.id || "fo", t = o.time || "day", r = mk(o.seed || 51), G = 1460;
    sky(L, t, r, o); land(L, t, r, 1020, { hill: !!o.hill, blink: o.blink, id });
    let m = school(-560, 1150, 0.62, t, { lit: o.lit, paint: false }) + tower(1020, 1150, 0.42, t, { id });
    put(L.mid, m);
    let s = `<rect x="-1400" y="1180" width="3900" height="200" fill="${tone(t, "#9a8a64", "#8a6050", "#1e1e2a")}"/>`;
    s += fenceRun(-1400, 260, 1330, 1.0, t, { sign: [-420, "ห้ามเข้า มีคน"] }) + fenceRun(820, 2500, 1330, 1.0, t, {});
    s += gate(540, 1330, 0.95, t, { id, lock: o.lock || "locked" });
    // the name arch over the gate
    s += `<g transform="translate(540,960)"><rect x="-330" y="-70" width="660" height="110" rx="14" fill="${tone(t, "#2c5a8a", "#3a4a7a", "#1a2238")}" ${O()}/><rect x="-310" y="-52" width="620" height="74" rx="8" fill="none" stroke="#f2e2a8" stroke-width="3" opacity=".7"/>
      <text x="0" y="8" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#fff" opacity="${t === "night" ? 0.6 : 1}">โรงเรียนบ้านหนองน้ำใส</text></g>`;
    // the road in front
    s += `<rect x="-1400" y="1360" width="3900" height="1400" fill="${tone(t, "#6e6a62", "#6a4a4a", "#181a24")}"/><path d="M-1400,1520H2500" stroke="${tone(t, "#f2e2a0", "#e8b880", "#3a3a48")}" stroke-width="10" stroke-dasharray="70 60" opacity=".8"/>
      <path d="M-1400,1362H2500" stroke="${tone(t, "#a8a090", "#8a6a5a", "#2a2a38")}" stroke-width="10"/>`;
    for (let k = 0; k < 14; k++) s += `<path d="M${f1(-1200 + r() * 3400)},${f1(1400 + r() * 500)}l${f1(20 + r() * 40)},${f1(4 - r() * 8)}" stroke="#4a4640" stroke-width="3" opacity=".5"/>`;
    if (o.pickup !== undefined) s += pickup(o.pickup, 1420, 0.92, t, id);
    put(L.set, s);
    put(L.set, `<rect x="-1400" y="960" width="3900" height="300" fill="url(#${t === "dusk" ? "fcHazeD" : "fcHaze"})" opacity="${t === "night" ? 0.1 : 0.55}"/>`);
  }
  // the abandoned pickup (side view, nose right): flat tyre, dust, the fuel flap open on the rear quarter (#id-flap)
  function pickup(x, G, s, t, id) {
    const body = tone(t, "#e8e4da", "#d8b8a0", "#3a3a4a"), dk = tone(t, "#b8b2a4", "#a88878", "#24242e");
    return `<g transform="translate(${x},${G}) scale(${s})"><ellipse cx="0" cy="8" rx="460" ry="36" fill="url(#fcAO)"/>
      <path d="M-420,-70V-180Q-420,-200 -400,-204L-60,-210L-40,-330Q-34,-350 -10,-352H210Q250,-350 270,-320L340,-214L400,-206Q430,-200 430,-170V-70Z" fill="${body}" ${O(5)}/>
      <path d="M-30,-320H90V-224H-46ZM110,-320H210Q236,-318 248,-296L300,-224H110Z" fill="${tone(t, "#7a98a8", "#8a6a7a", "#141828")}" ${O(3.5)}/>
      <path d="M-420,-130H430" stroke="${dk}" stroke-width="5"/><path d="M-60,-210V-80M110,-224V-80" stroke="${INK}" stroke-width="3"/>
      <path d="M-410,-196H-80" stroke="#fff" stroke-width="5" opacity=".4"/>
      <g id="${id}-flap"><rect x="-300" y="-178" width="46" height="40" rx="6" fill="${dk}" ${O(3)}/><rect x="-342" y="-180" width="40" height="44" rx="6" fill="${body}" ${O(3)} transform="rotate(-8 -302 -158)"/><circle cx="-277" cy="-158" r="10" fill="#2a2a2a"/></g>
      ${[-260, 260].map((wx) => `<circle cx="${wx}" cy="-62" r="78" fill="#2a2a2e" ${O(4)}/><circle cx="${wx}" cy="-62" r="40" fill="#8a8a90" ${O(3)}/><circle cx="${wx}" cy="-62" r="14" fill="#4a4a50"/>`).join("")}
      <path d="M-338,4Q-260,-10 -182,4" fill="#2a2a2e"/>
      <rect x="400" y="-170" width="30" height="40" rx="6" fill="#ffd36a" opacity=".6" ${O(2.5)}/><path d="M-60,-276h-40" stroke="${INK}" stroke-width="5"/>
      ${Array.from({ length: 8 }, (_, k) => `<circle cx="${-380 + k * 100}" cy="${-110 - (k % 3) * 20}" r="${6 + (k % 2) * 4}" fill="#8a7a5a" opacity=".35"/>`).join("")}</g>`;
  }
  Fence.pickup = pickup;

  // ---------------- Sets.fenceClass: the upstairs classroom ----------------
  function fenceClass(L, o = {}) {
    const id = o.id || "fc", t = o.time || "dusk", r = mk(o.seed || 61), night = t === "night", G = 1500;
    const wallC = tone(t, "#e8dcc0", "#d8b090", "#2a2838"), wallS = tone(t, "#c8b898", "#a8806a", "#1a1a28");
    // the view through the window (right): paddies at dusk, the gate below
    put(L.mid, `<rect x="560" y="300" width="1400" height="900" fill="url(#${SK[t]})"/>${t === "dusk" ? `<circle cx="900" cy="840" r="300" fill="url(#fcSunD)"/><circle cx="900" cy="840" r="46" fill="#fff0c0"/>` : `<circle cx="1000" cy="460" r="200" fill="url(#fcMoon)"/><circle cx="1000" cy="460" r="40" fill="#fff6dc"/>`}
      <rect x="560" y="900" width="1400" height="300" fill="url(#${PAD[t]})"/><path d="M560,900` + Array.from({ length: 16 }, (_, k) => `Q${600 + k * 90},${f1(860 - r() * 40)} ${650 + k * 90},${f1(890 - r() * 10)}`).join("") + `V920H560Z" fill="${tone(t, "#5e8a5a", "#5a3e5a", "#141c2c")}"/>`);
    let s = `<rect x="-1400" y="-900" width="3900" height="${G + 900}" fill="${wallC}"/>`;
    // window cut-out on the right (wall drawn as four rects around it)
    s = `<rect x="-1400" y="-900" width="1960" height="${G + 900}" fill="${wallC}"/><rect x="1440" y="-900" width="1100" height="${G + 900}" fill="${wallC}"/><rect x="560" y="-900" width="880" height="1200" fill="${wallC}"/><rect x="560" y="1200" width="880" height="${G - 1200}" fill="${wallC}"/>`;
    s += `<path d="M560,300H1440V1200H560Z" fill="none" stroke="#5a3a24" stroke-width="30"/><path d="M1000,300V1200M560,750H1440" stroke="#6a4a30" stroke-width="16"/><path d="M560,1200H1440" stroke="#8a6a4a" stroke-width="40"/>`;
    s += `<rect x="560" y="300" width="880" height="900" fill="${night ? "#000" : "#fff"}" opacity=".05"/>`;
    // the lower wall band (painted), the floor
    s += `<rect x="-1400" y="${G - 330}" width="1960" height="330" fill="${wallS}"/><path d="M-1400,${G - 330}H560M1440,${G - 330}H2500" stroke="${tone(t, "#3d78a8", "#5a5a8a", "#1a2238")}" stroke-width="12"/>`;
    s += `<rect x="-1400" y="${G}" width="3900" height="800" fill="${tone(t, "url(#fcFloor)", "#6a4a3a", "#1a1620")}"/>` + Array.from({ length: 14 }, (_, k) => `<path d="M-1400,${G + 20 + k * k * 4}H2500" stroke="${INK}" stroke-width="2" opacity=".25"/>`).join("");
    // the chalkboard with chalk text
    const ch = o.chalk || ["", ""];
    s += `<g transform="translate(-80,480)"><rect x="-470" y="-250" width="940" height="500" rx="14" fill="#6a4a2a" ${O(5)}/><rect x="-440" y="-222" width="880" height="444" fill="url(#fcBoard)"/>
      ${Array.from({ length: 6 }, (_, k) => `<path d="M${-420 + r() * 700},${-180 + r() * 380}q${f1(60 + r() * 120)},${f1(-10 + r() * 20)} ${f1(160 + r() * 160)},${f1(-4 + r() * 8)}" stroke="#e8ece8" stroke-width="16" opacity=".06" fill="none"/>`).join("")}
      <g id="${id}-chalk"><text x="0" y="-40" text-anchor="middle" font-family="Mali" font-weight="700" font-size="104" fill="#f4f6f0" opacity=".92">${ch[0]}</text>
      <text x="0" y="90" text-anchor="middle" font-family="Mali" font-weight="700" font-size="66" fill="#ffe08a" opacity=".9">${ch[1]}</text>
      ${o.tally ? `<g transform="translate(250,170)" stroke="#f4f6f0" stroke-width="6" opacity=".85">${Array.from({ length: 4 }, (_, k) => `<path d="M${k * 18},-30v54"/>`).join("")}<path d="M-8,10L72,-24"/></g>` : ""}</g>
      <rect x="-470" y="230" width="940" height="22" fill="#8a6a4a" ${O(3)}/><rect x="-300" y="216" width="40" height="14" fill="#f4f6f0"/><rect x="-200" y="218" width="30" height="12" fill="#f2c8d8"/></g>`;
    // posters: Thai alphabet chart and the kids' drawings (EP clue drawings pinned)
    s += `<g transform="translate(-860,420)"><rect x="-150" y="-200" width="300" height="400" fill="#fbf4e2" ${O(4)}/>${Array.from({ length: 30 }, (_, k) => `<text x="${-118 + (k % 5) * 58}" y="${-140 + Math.floor(k / 5) * 60}" font-family="Kanit" font-weight="800" font-size="40" fill="${["#d8392e", "#2c6aa8", "#2f9a5a"][k % 3]}">${"กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพ"[k]}</text>`).join("")}</g>`;
    s += [[-580, 260, -6, "#ffe6a0"], [-470, 520, 5, "#d8f0ff"]].map(([x, y, rot, c]) => `<g transform="translate(${x},${y}) rotate(${rot})"><rect x="-80" y="-60" width="160" height="120" fill="${c}" ${O(3)}/><circle cx="-30" cy="-10" r="20" fill="#f2a83a"/><path d="M-60,40q30,-40 60,-10t60,-20" stroke="#2f9a5a" stroke-width="7" fill="none"/><circle cx="0" cy="-66" r="6" fill="#d8392e"/></g>`).join("");
    // the dead ceiling fan
    s += `<g transform="translate(-80,-120)"><path d="M0,-200V-20" stroke="#5a5a5a" stroke-width="10"/><ellipse cx="0" cy="0" rx="40" ry="20" fill="#d8d4c8" ${O(3)}/><path d="M-30,0L-300,30L-300,10Z M30,0L300,-10L300,14Z" fill="#c8c4b8" ${O(3)}/></g>`;
    // desks (wooden, children's): back row in set
    const desk = (x, y, sc) => `<g transform="translate(${x},${y}) scale(${sc})"><ellipse cx="0" cy="6" rx="170" ry="20" fill="url(#fcAO)"/><path d="M-130,0V-150M130,0V-150M-120,0V-150" stroke="#5a3a24" stroke-width="12"/>
      <path d="M-150,-170H150L140,-150H-140Z" fill="#a8784a" ${O(3)}/><rect x="-150" y="-186" width="300" height="20" fill="#c8945a" ${O(3)}/><path d="M-140,-180H140" stroke="#e8b880" stroke-width="3" opacity=".7"/></g>`;
    s += desk(-640, G + 40, 0.9) + desk(-260, G + 60, 0.95) + desk(-450, G + 230, 1.15);
    s += `<g transform="translate(-200,${G + 40})">${Fence.can(0, 0, 0.3, {})}${Fence.can(60, 10, 0.3, {})}</g><g transform="translate(-620,${G - 140})"><rect x="-60" y="-20" width="120" height="20" fill="#e8e0c8" ${O(2)}/><rect x="-50" y="-36" width="100" height="16" fill="#3a7ac8" ${O(2)}/></g>`;
    // the teacher's desk with the radio (right, under the window)
    s += `<g transform="translate(1000,${G + 120})"><ellipse cx="0" cy="6" rx="300" ry="30" fill="url(#fcAO)"/><rect x="-270" y="-300" width="540" height="300" fill="#7a5034" ${O(4)}/><rect x="-290" y="-330" width="580" height="34" fill="#a06c44" ${O(4)}/><path d="M-260,-200H260M0,-296V0" stroke="#5a3a24" stroke-width="4"/><circle cx="-130" cy="-150" r="8" fill="#e8c860"/><circle cx="130" cy="-150" r="8" fill="#e8c860"/></g>`;
    s += `<g id="${id}-radio">${Fence.radio(1060, G - 210, 0.62, `${id}-r`)}</g>`;
    // mats and blankets on the floor, a lantern
    s += `<path d="M-1100,${G + 260}L-200,${G + 240}L-160,${G + 360}L-1160,${G + 380}Z" fill="#3a6aa8" ${O(3)}/><path d="M-1100,${G + 290}L-180,${G + 270}" stroke="#f2d84a" stroke-width="8" opacity=".6"/>`;
    // candles (night): on the desk and the floor
    if (night) s += [[760, G - 220], [-440, G - 210]].map(([x, y], k) => `<g transform="translate(${x},${y})"><rect x="-10" y="-50" width="20" height="50" fill="#f4eee0" ${O(2)}/><path id="${id}-fl${k}" d="M0,-52q-10,-18 0,-34q10,16 0,34z" fill="#ffd060"/></g>`).join("");
    put(L.set, s);
    put(L.fg, `<g transform="translate(-700,${G + 520}) scale(1.9)"><path d="M-150,-170H150L140,-150H-140Z" fill="#a8784a" ${O(3)}/><rect x="-150" y="-186" width="300" height="20" fill="#c8945a" ${O(3)}/><path d="M-130,0V-150M130,0V-150" stroke="#5a3a24" stroke-width="12"/></g>`);
    if (night) put(L.glow, `<g id="${id}-cand">${[[760, G - 270], [-440, G - 260]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="420" fill="url(#fcCandle)" opacity=".75"/>`).join("")}</g>`);
    else put(L.glow, `<path d="M560,300L1440,300L700,1700L-600,1700Z" fill="url(#fcRayD)" opacity="${t === "dusk" ? 0.55 : 0.25}"/>`);
  }

  // ---------------- Sets.fenceMarket ----------------
  function fenceMarket(L, o = {}) {
    const id = o.id || "fm", t = o.time || "dusk", r = mk(o.seed || 71), G = 1460;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="${tone(t, "#5a4a3a", "#3a2a2a", "#0a0a10")}"/>`);
    // the market roof: steel trusses with holes letting light shafts in
    let f = `<rect x="-1400" y="-900" width="3900" height="1100" fill="${tone(t, "#3a3432", "#2a2224", "#0c0c12")}"/>`;
    for (let x = -1300; x < 2500; x += 260) f += `<path d="M${x},200L${x + 130},-100L${x + 260},200M${x + 130},-100V200" stroke="${tone(t, "#5a5450", "#4a3a3a", "#1a1a22")}" stroke-width="12" fill="none"/>`;
    [[180, 120], [820, 80], [-380, 60]].forEach(([x, w]) => (f += `<rect x="${x}" y="-60" width="${w}" height="60" fill="${tone(t, "#ffe8b0", "#ffb070", "#5a6a9a")}"/>`));
    put(L.far, f);
    let s = `<rect x="-1400" y="200" width="3900" height="${G - 200}" fill="${tone(t, "#9a8a74", "#8a6a5a", "#14141c")}"/><rect x="-1400" y="${G}" width="3900" height="800" fill="${tone(t, "#a8987e", "#9a7a62", "#1a1a22")}"/>`;
    s += `<g transform="translate(560,330)"><rect x="-300" y="-50" width="600" height="100" rx="10" fill="#d8392e" ${O()}/><text y="20" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#fff">ตลาดสดหนองน้ำใส</text><path d="M-200,-50L-180,-120M200,-50L180,-120" stroke="#4a3a2a" stroke-width="5"/></g>`;
    s += Array.from({ length: 6 }, (_, k) => `<g transform="translate(${-1100 + k * 520},${G - 20})"><path d="M-60,0Q-70,-90 -30,-110H30Q70,-90 60,0Z" fill="#d8c8a0" ${O(3)}/><path d="M-30,-110q30,-14 60,0" stroke="#8a7a5a" stroke-width="4" fill="none"/><text y="-40" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="22" fill="#8a3a2a">ข้าวสาร</text></g>`).join("");
    // rows of stalls: wooden tables with torn tarps and empty shelves, crates, scattered cans
    const stall = (x, sc, c) => `<g transform="translate(${x},${G}) scale(${sc})"><ellipse cx="0" cy="6" rx="300" ry="30" fill="url(#fcAO)"/><path d="M-250,0V-460M250,0V-460" stroke="#4a3a2a" stroke-width="14"/>
      <path d="M-290,-470Q0,-430 290,-470L270,-380Q120,-330 30,-400Q-60,-330 -150,-390L-270,-370Z" fill="${c}" ${O(4)}/><path d="M-240,-440q120,24 240,0" stroke="#fff" stroke-width="6" opacity=".3" fill="none"/>
      <rect x="-260" y="-200" width="520" height="40" fill="#8a6440" ${O(3)}/><rect x="-240" y="-160" width="480" height="160" fill="#6a4a30" ${O(3)}/>
      <rect x="-230" y="-330" width="460" height="16" fill="#8a6440" ${O(2.5)}/>${Array.from({ length: 4 }, (_, k) => `<rect x="${-200 + k * 110}" y="${-380}" width="60" height="50" fill="${["#c8a050", "#a8c0d0", "#d86a4a", "#e8e4da"][k]}" opacity="${0.4 + (k % 2) * 0.5}" ${O(2)}/>`).join("")}</g>`;
    s += stall(-700, 0.9, tone(t, "#2f7ac8", "#3a5a9a", "#1a2238")) + stall(1500, 0.95, tone(t, "#e85a3a", "#a83a3a", "#2a1a1e"));
    s += stall(420, 0.62, tone(t, "#3a9a5a", "#3a6a4a", "#14221a"));
    for (let k = 0; k < 9; k++) s += Fence.can(-500 + r() * 1700, G + 120 + r() * 260, 0.32 + r() * 0.12, {});
    s += `<g transform="translate(240,${G + 60})"><path d="M-110,0V-150H110V0Z" fill="#a8784a" ${O(3)}/><path d="M-110,-75H110M-110,-150L110,0" stroke="#7a5034" stroke-width="5"/></g>`;
    put(L.set, s);
    put(L.glow, [[180, 120], [820, 80], [-380, 60]].map(([x, w]) => `<path d="M${x},0H${x + w}L${x + w + 300},${G + 200}H${x + 200}Z" fill="url(#fcCone)" opacity="${t === "night" ? 0.2 : 0.7}"/>`).join(""));
  }

  // ---------------- Sets.fenceRoad: the road back at sunset ----------------
  function fenceRoad(L, o = {}) {
    const id = o.id || "fr", t = o.time || "dusk", r = mk(o.seed || 81), G = 1200;
    sky(L, t, r, { sunX: 760, sunY: 900, ...o }); land(L, t, r, 1000, {});
    let s = `<path d="M440,1000L640,1000L2100,2400H-1000Z" fill="${tone(t, "#8a847a", "#6a4a4a", "#1a1c26")}"/><path d="M540,1004L560,2400" stroke="${tone(t, "#f2ead0", "#ffd090", "#3a3e50")}" stroke-width="10" stroke-dasharray="60 60" opacity=".8"/>`;
    [[-60, 0.35], [-460, 0.6], [-1100, 1.0], [1160, 0.6], [1800, 1.0]].forEach(([x, sc]) => (s += `<g transform="translate(${x},${f1(1000 + sc * 320)}) scale(${sc})"><path d="M-8,0V-760" stroke="${tone(t, "#4a3a2a", "#3a2a2a", "#0e1016")}" stroke-width="20"/><path d="M-80,-720H80" stroke="${tone(t, "#4a3a2a", "#3a2a2a", "#0e1016")}" stroke-width="12"/></g>`));
    s += `<path d="M-1400,520Q-500,620 -40,660Q300,680 520,700Q900,720 2500,600" stroke="#1a1416" stroke-width="3" fill="none"/>`;
    // the school far off at the end of the road (its tower and roof)
    s += `<g transform="translate(560,1000) scale(.12)">${school(-600, 0, 1, t, { paint: false })}${tower(900, 0, 0.8, t, {})}</g>`;
    put(L.mid, s);
    if (o.horde) put(L.set, `<g id="${id}-horde">${Fence.horde(560, 1300, 0.9, o.horde, r, { w: 1400, d: 260, col: tone(t, "#2a2a30", "#1a1218", "#06080c"), rim: "#ffb880" })}</g>`);
    put(L.set, `<rect x="-1400" y="1900" width="3900" height="400" fill="${tone(t, "#6a6460", "#4a3438", "#14141c")}"/>`);
  }

  // ---------------- inserts ----------------
  function fenceCanIns(L, o = {}) {
    const id = o.id || "fci", t = o.time || "dusk";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="${t === "night" ? "#14101a" : "#3a2a24"}"/>`);
    let s = `<rect x="-1400" y="900" width="3900" height="1400" fill="#a06c44"/>` + Array.from({ length: 9 }, (_, k) => `<path d="M-1400,${940 + k * 70}Q540,${930 + k * 70} 2500,${950 + k * 70}" stroke="#7a5034" stroke-width="4" opacity=".45" fill="none"/>`).join("");
    s += `<rect x="-1400" y="880" width="3900" height="30" fill="#c8945a"/>`;
    // the chalkboard far behind (out of focus)
    put(L.far, `<rect x="-300" y="80" width="1500" height="700" fill="#22382e"/><text x="460" y="420" text-anchor="middle" font-family="Mali" font-weight="700" font-size="150" fill="#f4f6f0" opacity=".85">${o.chalk || ""}</text><text x="460" y="600" text-anchor="middle" font-family="Mali" font-weight="700" font-size="90" fill="#ffe08a" opacity=".8">${o.chalk2 || ""}</text>`);
    s += `<g id="${id}-can">${Fence.can(540, 1360, 2.4, { bulge: o.bulge ?? 0.8, id: `${id}-c`, leak: o.leak })}</g>`;
    // the can opener (key type) lying by it
    s += `<g id="${id}-op" transform="translate(880,1500) rotate(-20)"><rect x="-150" y="-16" width="240" height="32" rx="14" fill="#c8ccd0" ${O(3)}/><path d="M90,-30L170,-10L160,26L90,20Z" fill="#9aa0a6" ${O(3)}/><path d="M-140,-6H70" stroke="#fff" stroke-width="5" opacity=".5"/></g>`;
    // a crayon drawing beside it: a can with a skull (ปั้น already knew)
    if (o.drawing) s += `<g transform="translate(220,1640) rotate(-8)"><rect x="-170" y="-120" width="340" height="240" fill="#fbf6e8" ${O(3)}/><path d="M-60,60V-50Q0,-80 60,-50V60Q0,80 -60,60Z" fill="none" stroke="#d8392e" stroke-width="7"/><circle cx="0" cy="0" r="22" fill="none" stroke="#2a2a2a" stroke-width="6"/><path d="M-10,-4h4M6,-4h4M-8,12h16" stroke="#2a2a2a" stroke-width="5"/><path d="M-110,-90L110,90M110,-90L-110,90" stroke="#2a2a2a" stroke-width="6" opacity=".7"/></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="${t === "night" ? 900 : 200}" cy="${t === "night" ? 1000 : 400}" r="900" fill="url(#${t === "night" ? "fcCandle" : "fcSunD"})" opacity="${t === "night" ? 0.6 : 0.35}"/>`);
  }
  function fenceSiphon(L, o = {}) {
    const id = o.id || "fsi";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="url(#fcSkyNoon)"/><circle cx="900" cy="140" r="500" fill="url(#fcSun)"/>`);
    put(L.far, `<rect x="-1400" y="1100" width="3900" height="1200" fill="#9a8a64"/>${fenceRun(-1400, 2500, 1120, 0.9, "noon", { planks: false })}`);
    // the pickup's rear quarter filling the frame, the fuel door open, the hose going in, a yellow jerrycan below
    let s = `<path d="M-1400,300H2500V1500H-1400Z" fill="#e8e4da" ${O(6)}/><path d="M-1400,640H2500" stroke="#b8b2a4" stroke-width="10"/><path d="M-1400,360H2500" stroke="#fff" stroke-width="12" opacity=".5"/>
      <circle cx="1500" cy="1500" r="420" fill="#2a2a2e" ${O(6)}/><path d="M900,1500Q1500,900 2100,1500" fill="#e8e4da" ${O(6)}/>`;
    s += `<rect x="380" y="700" width="260" height="230" rx="30" fill="#b8b2a4" ${O(5)}/><circle cx="510" cy="815" r="62" fill="#2a2a2a" ${O(4)}/><circle cx="510" cy="815" r="30" fill="#141414"/>
      <rect x="100" y="690" width="240" height="250" rx="30" fill="#e8e4da" ${O(5)} transform="rotate(-14 340 815)"/>`;
    s += `<g id="${id}-hose"><path d="M510,815C520,980 380,1120 260,1260C160,1380 140,1600 180,1900" stroke="#3aa86a" stroke-width="34" fill="none" stroke-linecap="round" opacity=".85"/><path d="M510,815C520,980 380,1120 260,1260C160,1380 140,1600 180,1900" stroke="#c8f0d8" stroke-width="8" fill="none" opacity=".55"/></g>`;
    s += `<g id="${id}-jc" transform="translate(760,1640)"><ellipse cx="0" cy="250" rx="240" ry="30" fill="url(#fcAO)"/><path d="M-200,240V-120Q-200,-160 -160,-170H120L200,-90V240Z" fill="#e8b42a" ${O(5)}/><path d="M-140,-200H40V-150H-140Z" fill="#d89a1a" ${O(4)}/><path d="M-160,-40H160M-160,80H160" stroke="#b8861a" stroke-width="8"/><path d="M-170,-140V220" stroke="#fff" stroke-width="12" opacity=".4"/></g>`;
    put(L.set, s);
  }
  function fenceNail(L, o = {}) {
    const id = o.id || "fn", t = o.time || "day";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="${tone(t, "#c8b48a", "#8a6a5a", "#1a1a24")}"/>`);
    put(L.far, `<rect x="-1400" y="-900" width="3900" height="1600" fill="${tone(t, "#d9d2c4", "#b89a8a", "#2a2c3a")}"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1400 + k * 140},-900V700" stroke="${tone(t, FC.iron, "#3a3030", "#10141a")}" stroke-width="40"/>`).join("")}<rect x="-1400" y="680" width="3900" height="60" fill="#3d78a8"/>`);
    let s = `<rect x="-1400" y="1300" width="3900" height="1000" fill="${tone(t, "#8a6c48", "#6a4a3a", "#1e1e28")}"/>`;
    s += `<g transform="translate(540,1100) rotate(-12)"><rect x="-900" y="-90" width="1800" height="180" fill="${tone(t, FC.plank, "#7a5040", "#2a221c")}" ${O(6)}/><path d="M-880,-40H880M-880,30H880" stroke="${FC.plankS}" stroke-width="5" opacity=".55"/>
      <g id="${id}-nail"><path d="M-40,-90L-34,-250" stroke="#8a9096" stroke-width="16" stroke-linecap="round"/><path d="M-44,-110L-40,-240" stroke="#d8dce0" stroke-width="5" opacity=".7"/><ellipse cx="-40" cy="-90" rx="30" ry="10" fill="#9aa0a6" ${O(3)}/>
      <path d="M-46,-200l4,-20M-36,-160l6,-14" stroke="${FC.rust}" stroke-width="7" stroke-linecap="round" opacity=".7"/>${o.blood ? `<path d="M-40,-250L-36,-180" stroke="#a81a12" stroke-width="12" stroke-linecap="round"/><path d="M-30,-96q20,30 10,70" stroke="#8a1810" stroke-width="10" fill="none" stroke-linecap="round"/>` : ""}</g></g>`;
    if (o.foot) s += `<g id="${id}-foot"><path d="M380,-500Q360,300 420,560Q440,700 560,760Q720,800 760,700Q780,600 700,560Q600,520 620,300L640,-500Z" fill="#c8946a" ${O(5)}/><path d="M560,760q-20,30 0,50M610,770q-10,34 10,46M660,770q0,30 16,40M700,740q10,26 26,30" stroke="${INK}" stroke-width="5" fill="none"/><path d="M420,-400Q410,200 450,500" stroke="#e8b48a" stroke-width="14" opacity=".6" fill="none"/></g>`;
    put(L.set, s);
  }
  function fenceLock(L, o = {}) {
    const id = o.id || "fl", t = o.time || "dusk";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="url(#${SK[t]})"/>`);
    put(L.far, `<rect x="-1400" y="1100" width="3900" height="1200" fill="url(#${PAD[t]})"/>${Fence.horde(560, 1180, 0.8, o.horde || 0, mk(5), { w: 1600, d: 120, col: "#14141a", rim: "#ffb880" })}`);
    let s = Array.from({ length: 7 }, (_, k) => `<rect x="${-260 + k * 190}" y="-900" width="56" height="3200" fill="url(#fcIron)" ${O(5)}/>`).join("");
    s += `<rect x="-1400" y="760" width="3900" height="60" fill="${FC.iron}" ${O(4)}/>`;
    s += `<path d="M310,700q60,70 130,0q60,70 130,0q60,70 130,0M310,830q60,-70 130,0q60,-70 130,0q60,-70 130,0" fill="none" stroke="#c8ccd0" stroke-width="26"/><path d="M310,700q60,70 130,0q60,70 130,0" fill="none" stroke="#5a6268" stroke-width="6"/>`;
    s += `<g id="${id}-lk">${Fence.padlock(560, 1100, 3.4, o.lock === "open", `${id}-p`)}</g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="300" cy="900" r="900" fill="url(#fcSunD)" opacity=".3"/>`);
  }
  function fenceRadio(L, o = {}) {
    const id = o.id || "fra";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="#0e0c14"/>`);
    put(L.far, `<rect x="-1400" y="-900" width="3900" height="2000" fill="#1e1a26"/><rect x="200" y="-200" width="700" height="800" fill="#141a30" stroke="#2a2030" stroke-width="30"/><circle cx="600" cy="100" r="40" fill="#fff6dc" opacity=".7"/>`);
    let s = `<rect x="-1400" y="1350" width="3900" height="1000" fill="#4a3020"/><rect x="-1400" y="1330" width="3900" height="30" fill="#6a4630"/>`;
    s += Fence.radio(500, 1500, 2.2, id);
    s += `<g transform="translate(-60,1460)"><rect x="-22" y="-120" width="44" height="120" fill="#f4eee0" ${O(3)}/><path id="${id}-fl" d="M0,-124q-22,-40 0,-76q22,36 0,76z" fill="#ffd060"/></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="-60" cy="1300" r="700" fill="url(#fcCandle)" opacity=".55"/><g id="${id}-halo" opacity=".5"><circle cx="700" cy="1200" r="600" fill="url(#fcDial)"/></g>`);
  }

  // ---------------- life: flag, clouds, laundry, horde sway, candles ----------------
  Fence.life = (tl, id, t0, dur) => {
    const sw = (sel, a, p) => { if (document.querySelector(sel)) tl.fromTo(sel, { rotation: -a }, { rotation: a, duration: p, yoyo: true, repeat: Math.ceil(dur / p), ease: "sine.inOut", immediateRender: false }, t0); };
    const flag = document.getElementById(`${id}-flag`);
    if (flag) tl.fromTo(flag, { scaleX: 1 }, { scaleX: 0.9, svgOrigin: "6 -820", duration: 0.5, yoyo: true, repeat: Math.ceil(dur / 0.5), ease: "sine.inOut", immediateRender: false }, t0);
    document.querySelectorAll(".fcloud").forEach((c) => tl.fromTo(c, { x: 0 }, { x: 40 * dur, duration: dur, ease: "none", immediateRender: false }, t0));
    document.querySelectorAll(`#${id}-horde .fzz`).forEach((z, k) => tl.fromTo(z, { y: 0 }, { y: -8, duration: 0.5 + (k % 4) * 0.12, yoyo: true, repeat: Math.ceil(dur / 0.5), ease: "sine.inOut", immediateRender: false }, t0 + (k % 5) * 0.07));
    const h = document.getElementById(`${id}-horde`);
    if (h) tl.fromTo(h, { x: 0 }, { x: 30, duration: dur, ease: "none", immediateRender: false }, t0);
    [0, 1].forEach((k) => { const f = document.getElementById(`${id}-fl${k}`); if (f) tl.fromTo(f, { scaleY: 1 }, { scaleY: 0.82, transformOrigin: "50% 100%", duration: 0.13 + k * 0.03, yoyo: true, repeat: Math.ceil(dur / 0.13), ease: "sine.inOut", immediateRender: false }, t0); });
    const fl = document.getElementById(`${id}-fl`);
    if (fl) tl.fromTo(fl, { scaleY: 1 }, { scaleY: 0.82, transformOrigin: "50% 100%", duration: 0.14, yoyo: true, repeat: Math.ceil(dur / 0.14), ease: "sine.inOut", immediateRender: false }, t0);
    const cand = document.getElementById(`${id}-cand`);
    if (cand) tl.fromTo(cand, { opacity: 1 }, { opacity: 0.85, duration: 0.17, yoyo: true, repeat: Math.ceil(dur / 0.17), ease: "sine.inOut", immediateRender: false }, t0);
    sw(`#${id}-cl`, 0, 1);
  };

  Object.assign(Sets, { fenceYard, fenceGate, fenceOut, fenceClass, fenceMarket, fenceRoad, fenceCanIns, fenceSiphon, fenceNail, fenceLock, fenceRadio });
})();
