// Sets, props and the ghost for "แสงกระสือ": a village by the rice fields in the flood season, at night, the power still on —
// stilt houses with lit windows, concrete power poles standing in the water, a transformer by the temple, green lights over the
// flood. Same layer contract as sets.js (sky / far / mid / set / act / fg, glow above the darkness); seeded RNG only.
//   Krasue.ghost(x, y, s, o)  the กระสือ, one piece: a woman's black head with green eyes and long wet hair, and under the neck her
//                             heart glowing red (user: "หัวใจสีแดง"), lungs and guts glowing green, hanging and dripping (class kbob bobs it, kdrip drips, khair sways)
//   Krasue.glow(x, y, s)      its green light for the glow layer (shows through the darkness)
//   Krasue.lurk(x, y, s, o)   the head as a black shape in the dark, only the green eyes clear (o.bun, o.heart dim red); Krasue.lensFace(id) the
//                             face at the lens for a split second (screen space) — the koi-style scare: show almost nothing, hold, then one quick hit and cut
//   Sets.floodVillage  wide: houses on stilts, poles and sagging lines in the water, the transformer lamp; o.lights green orbs
//                      (#id-l0…), o.fallen = a broken line with its end in the water (#id-arc sparks, #id-wire); #id-wfront over waders
//   Sets.houseIn       inside a low house at night: the outlets near the floor, a fan, the fridge (o.fridgeX; lower handle #id-fh), the door (o.doorX, #id-door),
//                      the window (o.windowX, o.day = daylight), o.mud = the morning after (tide line, mud), the main switch (สะพานไฟ) on
//                      the wall with its lever (#id-lever, pivot at #id-pivot), the water (#id-water) that rises over the floor,
//                      stairs by the door up to the sleeping floor (step k top at G - 90(k+1), x 700 + 110k)
//   Sets.floodSection  koi-style diagram: the house cut open, outlet low, cut-out by the stairs, the flood rising (#id-water #id-zap #id-lever #id-ok #id-wet)
//   Sets.porchFlood    the front of the house: steps into the flood, the meter box, a lamp, a pole close by (o.dark: power cut)
//   Sets.meterCard     chapter card: the electric meter, its disc and number wheels running backwards (#id-disc, #id-digits)
//   Sets.comicLegend   an old one-baht horror comic, printed black and green on yellowed paper, four panels (y 0/1000/2000/3000)
//   Sets.switchClose   the main switch close up: porcelain base, copper blades, a hand on the lever (#id-hand, #id-lever)
//   Sets.poleSign      end card: the warning sign on a power pole with a note pinned to it
//   Sets.latchClose    close up: ฝน's hand on the door bolt (#id-bolt, #id-hand), green light through the plank gaps (#id-gaps)
//   Sets.outletClose   close up: the outlet behind the fridge burnt black (#id-soot), a tester screwdriver (#id-tester, its neon #id-neon)
//   Sets.chaemTop      top-down: ป้าแช่ม asleep on a mat, blanket to the chin, eyes #id-shut / #id-open / #id-eyes (green glow), rag #id-rag
//   Sets.cprFloor      top-down on the upstairs boards: เต้ย on his back (#id-chest, #id-lips, eyes #id-shut / #id-open), ฝน's hands (#id-hands),
//                      her phone calling 1669
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  // the ghost's palette (the channel's ghosts: coal-black with green eyes, like the กองกอย)
  const KBL = "#0a0c0b", KBL2 = "#161b19", KRIM = "#3d6a52", KEYE = ["#7dff6a", "#bfff96", "#f2ffe4"];

  Sets.DEFS += `
    <linearGradient id="ksSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070f"/><stop offset=".6" stop-color="#0d1426"/><stop offset="1" stop-color="#1a2338"/></linearGradient>
    <linearGradient id="ksDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2448"/><stop offset=".5" stop-color="#6b4a74"/><stop offset=".85" stop-color="#d9826a"/><stop offset="1" stop-color="#f2b47a"/></linearGradient>
    <linearGradient id="ksWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2a33"/><stop offset=".4" stop-color="#121c22"/><stop offset="1" stop-color="#070c10"/></linearGradient>
    <linearGradient id="ksMud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a5238" stop-opacity=".88"/><stop offset="1" stop-color="#2e2a1c" stop-opacity=".95"/></linearGradient>
    <radialGradient id="ksGut" cx=".45" cy=".4"><stop offset="0" stop-color="#e6ffc8"/><stop offset=".45" stop-color="#7dff6a"/><stop offset="1" stop-color="#2a8a46"/></radialGradient>
    <radialGradient id="ksHeart" cx=".42" cy=".35"><stop offset="0" stop-color="#ffd0c4"/><stop offset=".4" stop-color="#ff3a2a"/><stop offset="1" stop-color="#9a0c0c"/></radialGradient>
    <radialGradient id="ksHeartGlow"><stop offset="0" stop-color="#ff3a2a" stop-opacity=".7"/><stop offset=".5" stop-color="#d8201a" stop-opacity=".22"/><stop offset="1" stop-color="#d8201a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ksGlow"><stop offset="0" stop-color="#7dff6a" stop-opacity=".55"/><stop offset=".4" stop-color="#3dbf5a" stop-opacity=".18"/><stop offset="1" stop-color="#3dbf5a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ksArc"><stop offset="0" stop-color="#eafcff" stop-opacity=".95"/><stop offset=".3" stop-color="#8fe6ff" stop-opacity=".45"/><stop offset="1" stop-color="#5ab8ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="ksLamp"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".85"/><stop offset=".4" stop-color="#ffc06a" stop-opacity=".22"/><stop offset="1" stop-color="#ffc06a" stop-opacity="0"/></radialGradient>
    <radialGradient id="ksTube"><stop offset="0" stop-color="#e8f6ff" stop-opacity=".7"/><stop offset=".5" stop-color="#bfe0ff" stop-opacity=".18"/><stop offset="1" stop-color="#bfe0ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="ksWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfc5a8"/><stop offset="1" stop-color="#b3a98c"/></linearGradient>
    <pattern id="ksDots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.6" fill="#2a2a20" opacity=".18"/></pattern>
    <pattern id="ksDotsG" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="3" fill="#3daa5a" opacity=".55"/></pattern>`;

  // ---------------- the กระสือ ----------------
  function ghost(x, y, s, o = {}) {
    const hair = Array.from({ length: 13 }, (_, i) => { const dx = -64 + i * 10.6, len = 230 + (i % 4) * 46, sw = (i % 2 ? 1 : -1) * (10 + (i % 3) * 8);
      return `<path class="khair" data-i="${i}" d="M${f1(dx * 0.7)},-60C${f1(dx * 1.25)},${f1(len * 0.25)} ${f1(dx * 1.3 + sw)},${f1(len * 0.65)} ${f1(dx * 1.1 + sw * 1.6)},${f1(len)}" stroke="#050706" stroke-width="${14 - (i % 3) * 3}" fill="none" stroke-linecap="round"/>`; }).join("");
    const eye = (cx) => `<g class="keye"><circle cx="${cx}" cy="-6" r="30" fill="${KEYE[0]}" opacity=".3"/><path d="M${cx - 17},-6Q${cx},-20 ${cx + 17},-6Q${cx},6 ${cx - 17},-6Z" fill="${KEYE[0]}"/><ellipse cx="${cx}" cy="-6" rx="6" ry="5" fill="${KEYE[2]}"/></g>`;
    // the guts: trachea and spine, two lungs, the heart, a coil of intestine hanging down, all lit green from inside
    const gut = (d, w) => `<path d="${d}" stroke="#1d5a32" stroke-width="${w + 8}" fill="none" stroke-linecap="round"/><path d="${d}" stroke="url(#ksGut)" stroke-width="${w}" fill="none" stroke-linecap="round"/>`;
    const guts = `<g class="kguts">
      ${gut("M-6,70C-8,110 -4,150 0,180", 16)}
      <path d="M-14,100C-70,96 -84,170 -60,230C-40,250 -18,226 -14,190Z" fill="url(#ksGut)" stroke="#1d5a32" stroke-width="4"/>
      <path d="M14,100C70,96 84,170 60,230C40,250 18,226 14,190Z" fill="url(#ksGut)" stroke="#1d5a32" stroke-width="4"/>
      <circle cx="0" cy="186" r="62" fill="url(#ksHeartGlow)"/>
      <path d="M-22,196C-40,176 -40,150 -16,150C-6,150 0,160 0,166C0,160 6,150 16,150C40,150 40,176 22,196L0,226Z" fill="url(#ksHeart)" stroke="#5a0d0d" stroke-width="4" class="kheart"/>
      ${gut("M0,226C-60,250 -70,300 -20,316C40,334 60,290 20,276C-20,262 -50,300 -30,350C-14,390 30,380 26,420C22,460 -10,470 -14,520", 18)}
      ${gut("M10,236C50,260 70,320 40,360C20,384 34,420 54,450", 12)}
      ${[[-14, 520], [54, 450], [-60, 232], [60, 232]].map(([dx, dy], k) => `<path class="kdrip" data-i="${k}" d="M${dx},${dy}c-6,12 -6,20 0,22c6,-2 6,-10 0,-22z" fill="#9fff8a"/>`).join("")}</g>`;
    const face = `<path d="M-64,-30Q-62,-110 0,-114Q62,-110 64,-30Q66,40 30,66Q0,82 -30,66Q-66,40 -64,-30Z" fill="${KBL}" stroke="${KRIM}" stroke-width="4"/>
      <path d="M-40,-40Q-20,-30 -6,-36M6,-36Q20,-30 40,-40" stroke="${KRIM}" stroke-width="3" fill="none"/>${eye(-24)}${eye(24)}
      <path d="M-16,40Q0,30 16,40Q8,54 0,56Q-8,54 -16,40Z" fill="#020303" stroke="${KRIM}" stroke-width="2"/><path d="M-8,46l3,7l3,-7M2,46l3,7l3,-7" stroke="#c8ff9a" stroke-width="2" fill="none"/>
      <path d="M-66,-36Q-60,-118 0,-122Q60,-118 66,-36Q40,-84 0,-86Q-40,-84 -66,-36Z" fill="#050706"/>
      ${[-46, -30, 30, 46].map((dx, i) => `<path d="M${dx * 0.8},-80C${dx},-30 ${dx + (i % 2 ? 4 : -4)},20 ${dx * 1.1},${80 + (i % 2) * 20}" stroke="#050706" stroke-width="${9 - (i % 2) * 2}" fill="none" stroke-linecap="round"/>`).join("")}`;
    const bun = o.bun ? `<circle cx="0" cy="-128" r="30" fill="#050706" stroke="${KRIM}" stroke-width="3"/>` : "";  // ป้าแช่ม's bun (EP.2 clue)
    return `<g class="kbob" ${o.id ? `id="${o.id}"` : ""} opacity="${o.op ?? 1}"><g transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})">${hair}${guts}${bun}${face}</g></g>`;
  }
  // the green glow is centred on the guts, under the heart, and the heart keeps its own red glow on top (so it reads red in the dark)
  const glow = (x, y, s, r = 1) => `<g class="kglow"><circle cx="${f1(x)}" cy="${f1(y + 300 * s)}" r="${f1(420 * s * r)}" fill="url(#ksGlow)"/><circle cx="${f1(x)}" cy="${f1(y + 190 * s)}" r="${f1(120 * s)}" fill="url(#ksHeartGlow)"/></g>`;
  // koi-style scares (user 25 ต.ค.: "ฉากจั้มสแกร์ไม่ค่อยดี ดูกองกอย EP.3 ตอนจบเป็นตัวอย่าง"): show almost nothing. lurk = the head as a
  // black shape in the dark, hair hanging, only the two green eyes clear (class keye flickers), o.bun, o.heart = a dim red glow
  // under the neck where the heart is (no lit guts); lensFace = the face right at the lens for a split second (#id, opacity 0)
  function lurk(x, y, s, o = {}) {
    const hair = Array.from({ length: 11 }, (_, i) => { const dx = -56 + i * 11.2, len = 200 + (i % 4) * 50, sw = (i % 2 ? 1 : -1) * (8 + (i % 3) * 6);
      return `<path class="khair" data-i="${i}" d="M${f1(dx * 0.7)},-60C${f1(dx * 1.2)},${f1(len * 0.25)} ${f1(dx * 1.25 + sw)},${f1(len * 0.65)} ${f1(dx * 1.05 + sw * 1.5)},${f1(len)}" stroke="#030404" stroke-width="${13 - (i % 3) * 3}" fill="none" stroke-linecap="round"/>`; }).join("");
    const eye = (cx) => `<g class="keye"><circle cx="${cx}" cy="-6" r="22" fill="${KEYE[0]}" opacity=".22"/><path d="M${cx - 14},-6Q${cx},-16 ${cx + 14},-6Q${cx},4 ${cx - 14},-6Z" fill="${KEYE[0]}"/><ellipse cx="${cx}" cy="-6" rx="4" ry="3.5" fill="${KEYE[2]}"/></g>`;
    return `<g ${o.id ? `id="${o.id}"` : ""} opacity="${o.op ?? 1}"><g transform="translate(${f1(x)},${f1(y)}) scale(${s})">
      ${o.heart ? `<circle cx="0" cy="190" r="${o.heart * 90}" fill="url(#ksHeartGlow)" opacity=".55"/>` : ""}${hair}
      ${o.bun ? `<circle cx="0" cy="-128" r="30" fill="#030404"/>` : ""}
      <path d="M-64,-30Q-62,-110 0,-114Q62,-110 64,-30Q66,40 30,66Q0,82 -30,66Q-66,40 -64,-30Z" fill="#030404"/>
      <path d="M-66,-36Q-60,-118 0,-122Q60,-118 66,-36Q40,-84 0,-86Q-40,-84 -66,-36Z" fill="#020303"/>${eye(-24)}${eye(24)}
      ${[-46, -30, 30, 46].map((dx, i) => `<path d="M${dx * 0.8},-80C${dx},-30 ${dx + (i % 2 ? 4 : -4)},20 ${dx * 1.1},${80 + (i % 2) * 20}" stroke="#020303" stroke-width="${9 - (i % 2) * 2}" fill="none" stroke-linecap="round"/>`).join("")}</g></g>`;
  }
  const lensFace = (id) => `<g id="${id}" opacity="0"><rect x="-100" y="-100" width="1280" height="2120" fill="#020303"/>
      <g transform="translate(540,900) scale(8.5)">
        <path d="M-64,-30Q-62,-110 0,-114Q62,-110 64,-30Q66,40 30,66Q0,82 -30,66Q-66,40 -64,-30Z" fill="#070908" stroke="${KRIM}" stroke-width="1.2" opacity=".9"/>
        ${[-24, 24].map((cx) => `<circle cx="${cx}" cy="-6" r="20" fill="${KEYE[0]}" opacity=".35"/><path d="M${cx - 15},-6Q${cx},-19 ${cx + 15},-6Q${cx},5 ${cx - 15},-6Z" fill="${KEYE[0]}"/><ellipse cx="${cx}" cy="-6" rx="4" ry="4" fill="${KEYE[2]}"/>`).join("")}
        <path d="M-14,40Q0,32 14,40Q8,52 0,54Q-8,52 -14,40Z" fill="#000"/>
        ${[-50, -36, -20, 14, 30, 48].map((dx, i) => `<path d="M${dx},-120C${dx + (i % 2 ? 6 : -6)},-40 ${dx + (i % 2 ? -4 : 4)},20 ${dx * 1.2},120" stroke="#010202" stroke-width="${7 - (i % 3)}" fill="none" stroke-linecap="round"/>`).join("")}</g></g>`;
  // a floating green light seen from far away (what the villagers call แสงกระสือ)
  const orb = (x, y, s, id) => `<g class="korb" ${id ? `id="${id}"` : ""}><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(16 * s)}" fill="#d8ffc0"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(38 * s)}" fill="#7dff6a" opacity=".45"/>
    <path d="M${f1(x - 5 * s)},${f1(y + 14 * s)}q${f1(-6 * s)},${f1(40 * s)} ${f1(4 * s)},${f1(80 * s)}M${f1(x + 6 * s)},${f1(y + 14 * s)}q${f1(8 * s)},${f1(30 * s)} ${f1(-2 * s)},${f1(60 * s)}" stroke="#7dff6a" stroke-width="${f1(4 * s)}" fill="none" opacity=".7"/></g>`;
  const orbGlow = (x, y, s) => `<g class="kglow"><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(200 * s)}" fill="url(#ksGlow)"/></g>`;

  // a small rowing boat (เรือพาย), side view, bow to the right; o.flip = bow left
  const boat = (x, y, s, o = {}) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})"><path d="M-260,-30H220Q290,-34 320,-80Q316,-16 250,14Q220,30 180,30H-220Q-266,24 -280,-6Q-284,-26 -260,-30Z" fill="#6a4a2e" ${OUT}/>
    <path d="M-260,-30H220Q290,-34 320,-80" stroke="#9a6a3c" stroke-width="10" fill="none"/>${[-150, 20].map((bx) => `<rect x="${bx}" y="-44" width="70" height="14" rx="4" fill="#8a5f3c" ${OUT3}/>`).join("")}</g>`;
  const boatFront = (x, y, s, o = {}) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})"><path d="M-260,-30H220Q290,-34 320,-80Q316,-16 250,14Q220,30 180,30H-220Q-266,24 -280,-6Q-284,-26 -260,-30Z" fill="#6a4a2e" ${OUT}/><path d="M-250,4H200" stroke="#4a3220" stroke-width="5"/></g>`;

  // ---------------- shared pieces ----------------
  function sky(L, o, r) {
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#${o.dusk ? "ksDusk" : "ksSky"})"/>`;
    if (!o.dusk) for (let i = 0; i < 60; i++) s += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-600 + r() * 1300)}" r="${f1(1 + r() * 2)}" fill="#e8ecff" opacity="${(0.25 + r() * 0.5).toFixed(2)}"/>`;
    const m = o.moon ?? { x: 820, y: 240, r: 52 };
    if (m) s += `<circle cx="${m.x}" cy="${m.y}" r="${m.r * 5}" fill="#9fb0d8" opacity=".08"/><circle cx="${m.x}" cy="${m.y}" r="${m.r}" fill="#e8e2c0"/>`;
    s += `<g class="kcloud">${[[-300, 180, 520], [500, 120, 640], [1200, 260, 560], [200, 400, 700]].map(([x, y, w]) => `<path d="M${x},${y}q${w * 0.2},-60 ${w * 0.45},-20q${w * 0.25},-70 ${w * 0.55},10q-${w * 0.4},50 -${w},10z" fill="#1c2438" opacity=".85"/>`).join("")}</g>`;
    put(L.sky, s);
  }
  function farLine(L, y, r, o = {}) {
    let s = `<path d="M-1200,${y}`;
    for (let x = -1200; x <= 2300; x += 70) s += `L${x},${f1(y - 50 - r() * 110)}`;
    s += `L2300,${y + 30}H-1200Z" fill="#05080c"/>`;
    const tx = o.temple ?? 1050;
    if (tx !== false) s += `<g fill="#070b12"><rect x="${tx - 110}" y="${y - 170}" width="220" height="120"/><path d="M${tx - 150},${y - 170}L${tx},${y - 290}L${tx + 150},${y - 170}Z"/><path d="M${tx},${y - 290}q12,-26 2,-46" stroke="#070b12" stroke-width="6" fill="none"/></g>`;
    if (!o.dark) for (let k = 0; k < 14; k++) s += `<circle class="slt" cx="${f1(-900 + r() * 2900)}" cy="${f1(y - 30 - r() * 60)}" r="4" fill="#ffd38a" opacity=".7"/>`;
    put(L.far, s);
  }
  function water(L, W, r, o = {}) {
    let s = `<rect x="-1200" y="${W}" width="3500" height="${3000 - W}" fill="url(#ksWater)"/>`;
    for (let k = 0; k < 50; k++) s += `<path class="rip" d="M${f1(-900 + r() * 2900)},${f1(W + 20 + r() * 1300)}h${f1(30 + r() * 110)}" stroke="#6c7f9a" stroke-width="3" stroke-linecap="round" opacity=".3"/>`;
    // flotsam: a sandal, a bottle, a plastic chair half sunk
    s += `<g opacity=".8"><rect x="${o.chair ?? 140}" y="${W + 40}" width="80" height="34" rx="6" fill="#3f6fa0" transform="rotate(-12 ${(o.chair ?? 140) + 40} ${W + 57})"/><ellipse cx="760" cy="${W + 120}" rx="30" ry="9" fill="#a83a2a"/><rect x="420" y="${W + 220}" width="16" height="44" rx="5" fill="#cfe6ee" transform="rotate(70 428 ${W + 242})"/></g>`;
    put(L.mid, s);
  }
  // a concrete power pole from the water up, cross-arm, insulators; returns the top wire points
  function pole(x, W, h, o = {}) {
    const top = W - h;
    let s = `<g><rect x="${x - 16}" y="${top}" width="32" height="${h + 260}" fill="#8a8e8c" ${OUT3}/><path d="M${x - 6},${top + 40}V${W}" stroke="#6f7472" stroke-width="5"/>
      <rect x="${x - 120}" y="${top + 40}" width="240" height="18" rx="3" fill="#6a6058" ${OUT3}/>${[-100, -36, 36, 100].map((dx) => `<rect x="${x + dx - 7}" y="${top + 18}" width="14" height="24" rx="5" fill="#d8dcd8" ${OUT3}/>`).join("")}`;
    if (o.transformer) s += `<rect x="${x - 70}" y="${top + 120}" width="140" height="170" rx="14" fill="#7f8a86" ${OUT}/><path d="M${x - 70},${top + 160}h140M${x - 70},${top + 200}h140M${x - 70},${top + 240}h140" stroke="#5f6866" stroke-width="5"/>
      <g transform="translate(${x},${top + 330})"><path d="M-46,0L0,-40L46,0Z" fill="#f2c94a" ${OUT3}/><path d="M-2,-26l-6,14h8l-4,10" stroke="${INK}" stroke-width="4" fill="none"/></g>`;
    if (o.lamp) s += `<path d="M${x},${top + 90}h70v20" stroke="#4a4f52" stroke-width="7" fill="none"/><path d="M${x + 52},${top + 110}h36l-6,16h-24z" fill="#30353a"/>`;
    s += `<ellipse class="rip" cx="${x}" cy="${W + 6}" rx="44" ry="9" fill="none" stroke="#9fb0c8" stroke-width="4" opacity=".5"/></g>`;
    return { s, wires: [-100, -36, 36, 100].map((dx) => [x + dx, top + 18]) };
  }
  const sag = (a, b, d = 70) => `M${a[0]},${a[1]}Q${(a[0] + b[0]) / 2},${(a[1] + b[1]) / 2 + d} ${b[0]},${b[1]}`;
  function stilt(x, W, s, o = {}) {
    const lit = o.lit !== false;
    return `<g transform="translate(${x},${W}) scale(${s})">
      ${[-220, -90, 40, 170].map((px) => `<rect x="${px}" y="-300" width="24" height="420" fill="#2a1d14" ${OUT3}/>`).join("")}
      <rect x="-260" y="-330" width="480" height="40" fill="#3b2a1c" ${OUT3}/><path d="M-250,-330V-600H210V-330Z" fill="#4a3424" ${OUT}/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${-250 + k * 38},-600V-330" stroke="#2a1c12" stroke-width="4"/>`).join("")}
      <rect x="-190" y="-540" width="110" height="130" fill="${lit ? "#ffd38a" : "#1a1f26"}" ${OUT3}/><path d="M-135,-540v130" stroke="${INK}" stroke-width="5"/>
      <rect x="40" y="-540" width="110" height="130" fill="${lit && o.both !== false ? "#ffcf7a" : "#1a1f26"}" ${OUT3}/><path d="M95,-540v130" stroke="${INK}" stroke-width="5"/>
      <path d="M-300,-600L-20,-800L260,-600Z" fill="#2a1c12" ${OUT}/></g>`;
  }
  const stiltGlow = (x, W, s, both = true) => `<circle cx="${f1(x - 135 * s)}" cy="${f1(W - 475 * s)}" r="${f1(220 * s)}" fill="url(#ksLamp)"/>${both ? `<circle cx="${f1(x + 95 * s)}" cy="${f1(W - 475 * s)}" r="${f1(200 * s)}" fill="url(#ksLamp)"/>` : ""}
    <path d="M${f1(x - 135 * s)},${W + 10}v${f1(260 * s)}" stroke="#ffd38a" stroke-width="${f1(26 * s)}" opacity=".18"/>`;

  // ---------------- wide: the flooded village at night ----------------
  function floodVillage(L, o = {}) {
    const id = o.id || "fv", r = mk(o.seed || 211), W = o.water ?? 1250;
    sky(L, o, r);
    farLine(L, W - 20, r, o);  // o.dark: every light in the village is out
    water(L, W, r, o);
    let s = "", g = "";
    (o.houses || [[-150, 1.0], [980, 0.8]]).forEach(([x, k, ho], i) => { const lit = !o.dark && !(ho && ho.dark); s += stilt(x, W, k, { both: i % 2 === 0, lit }); if (lit) g += stiltGlow(x, W, k, i % 2 === 0); });
    const poles = (o.poles || [[260, 760], [700, 700, { transformer: true, lamp: true }], [1180, 640]]).map(([x, h, po]) => pole(x, W, h, po || {}));
    poles.forEach((p) => (s += p.s));
    let w = "";
    for (let k = 0; k < poles.length - 1; k++) for (let j = 0; j < 4; j++) {
      if (o.fallen && k === o.fallen.span && j === o.fallen.wire) continue;
      w += `<path d="${sag(poles[k].wires[j], poles[k + 1].wires[j], 60 + j * 6)}" stroke="#1a1d20" stroke-width="4" fill="none"/>`;
    }
    // the broken line: from its insulator down into the water, its end arcing
    if (o.fallen) {
      const a = poles[o.fallen.span].wires[o.fallen.wire], e = o.fallen.end || [a[0] + 220, W + 30];
      const wd = `M${a[0]},${a[1]}C${a[0] + 60},${a[1] + 200} ${e[0] - 80},${e[1] - 260} ${e[0]},${e[1]}`;
      w += `<path id="${id}-wire" d="${wd}" stroke="#1a1d20" stroke-width="5" fill="none"/>`;
      g += `<path d="${wd}" stroke="#8fe6ff" stroke-width="3" fill="none" opacity=".4"/>`;  // a sheen so the line reads at night
      s += `<g id="${id}-arc" opacity="0">${[0, 1, 2, 3, 4].map((k) => `<path d="M${e[0]},${e[1]}l${(k - 2) * 18},${-20 - k * 6}l${(k % 2 ? 14 : -14)},-16l${(k - 2) * 10},-14" stroke="#eafcff" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
      g += `<g id="${id}-arcg" opacity="0"><circle cx="${e[0]}" cy="${e[1]}" r="200" fill="url(#ksArc)"/><ellipse cx="${e[0]}" cy="${e[1] + 20}" rx="260" ry="50" fill="url(#ksArc)" opacity=".7"/></g>`;
    }
    s += w;
    put(L.set, s);
    poles.forEach((p, i) => { if (!o.dark && ((o.poles || [])[i]?.[2]?.lamp || (!o.poles && i === 1))) g += `<circle class="lamp" cx="${(o.poles ? o.poles[i][0] : 700) + 70}" cy="${W - (o.poles ? o.poles[i][1] : 700) + 130}" r="210" fill="url(#ksLamp)"/>`; });
    let a = "";
    (o.lights || []).forEach(([x, y, k], i) => { a += orb(x, y, k, `${id}-l${i}`); g += `<g id="${id}-lg${i}">${orbGlow(x, y, k)}</g>`; });
    put(L.set, a);
    put(L.glow, g);
    put(L.act, `<g id="${id}-wfront"><path d="M-1200,${W}Q-400,${W - 10} 400,${W}T2000,${W}V3000H-1200Z" fill="#14202a" opacity=".82"/><path class="rip" d="M-1200,${W}Q-400,${W - 10} 400,${W}T2000,${W}" stroke="#9fb0c8" stroke-width="5" fill="none" opacity=".6"/></g>`);
  }

  // ---------------- inside the house: the water creeping up to the outlets ----------------
  function houseIn(L, o = {}) {
    const id = o.id || "hi", r = mk(o.seed || 223), G = o.ground ?? 1480, WL = o.level ?? G - 60;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#141210"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${G + 800}" fill="url(#ksWall)"/><rect x="-1200" y="${G - 300}" width="3500" height="300" fill="#9f9478"/><path d="M-1200,${G - 300}H2300" stroke="#7d7358" stroke-width="8"/>`;
    // old water stains from past floods
    s += `<path d="M-1200,${G - 520}Q-600,${G - 540} 0,${G - 515}T1200,${G - 525}T2300,${G - 520}" stroke="#8a7f62" stroke-width="10" fill="none" opacity=".55"/>`;
    // window on the night (rain streaks), door, Buddha shelf, calendar, clock
    const WX = o.windowX ?? -640;
    s += `<g id="${id}-window"><rect x="${WX}" y="${G - 1150}" width="360" height="420" fill="${o.day ? "#bcd6e8" : "#0b1220"}" ${OUT}/>${o.day ? `<circle cx="${WX + 270}" cy="${G - 1060}" r="40" fill="#fff3c8" opacity=".8"/>` : [0, 1, 2, 3, 4, 5].map((k) => `<path d="M${WX + 20 + k * 60},${G - 1130}l-20,90" stroke="#5a6a8a" stroke-width="3" opacity=".5"/>`).join("")}<path id="${id}-wframe" d="M${WX + 180},${G - 1150}v420M${WX},${G - 940}h360" stroke="#5a4a3a" stroke-width="10"/></g>
      <g id="${id}-door"><rect x="${o.doorX ?? 1120}" y="${G - 1260}" width="380" height="1260" fill="#5a3f2a" ${OUT}/>${[0, 1].map((k) => `<rect x="${(o.doorX ?? 1120) + 50}" y="${G - 1200 + k * 600}" width="280" height="520" rx="8" fill="none" stroke="#3b2a1c" stroke-width="6"/>`).join("")}<circle id="${id}-knob" cx="${(o.doorX ?? 1120) + 30}" cy="${G - 620}" r="14" fill="#c9a55a" ${OUT3}/></g>
      <rect x="-160" y="${G - 1420}" width="300" height="24" fill="#6a4a32" ${OUT3}/><path d="M-30,${G - 1420}v-80h60v80" fill="#c9a55a" ${OUT3}/>
      <rect x="260" y="${G - 1260}" width="170" height="220" fill="#f4ecd8" ${OUT3}/><rect x="260" y="${G - 1260}" width="170" height="50" fill="#c8392b"/>
      <circle cx="680" cy="${G - 1240}" r="56" fill="#f4ecd8" ${OUT}/><path d="M680,${G - 1240}v-36M680,${G - 1240}l26,14" stroke="${INK}" stroke-width="5"/>`;
    // the main switch (สะพานไฟ) by the door: porcelain base, fuses, the lever (#id-lever turns about #id-pivot)
    const SX = o.switchX ?? 940, SY = G - 1120;
    s += `<g id="${id}-panel"><rect x="${SX - 70}" y="${SY - 120}" width="140" height="240" rx="10" fill="#efe9dc" ${OUT}/><rect x="${SX - 52}" y="${SY - 100}" width="104" height="40" rx="6" fill="#d8d0c0" ${OUT3}/>
      <rect x="${SX - 52}" y="${SY + 60}" width="104" height="40" rx="6" fill="#d8d0c0" ${OUT3}/><path d="M${SX - 30},${SY - 80}h60M${SX - 30},${SY + 80}h60" stroke="#c9873a" stroke-width="5"/>
      <path d="M${SX},${SY + 120}V${G - 320}" stroke="#2a2a2a" stroke-width="10"/><path d="M${SX},${SY - 120}V${SY - 420}" stroke="#2a2a2a" stroke-width="10"/>
      <circle id="${id}-pivot" cx="${SX}" cy="${SY + 40}" r="9" fill="${INK}"/>
      <g id="${id}-lever" transform="rotate(0 ${SX} ${SY + 40})"><rect x="${SX - 40}" y="${SY - 70}" width="80" height="14" rx="5" fill="#c9873a" ${OUT3}/><rect x="${SX - 8}" y="${SY - 70}" width="16" height="110" fill="#c9873a" ${OUT3}/><rect x="${SX - 26}" y="${SY - 104}" width="52" height="40" rx="10" fill="#1d1d1d" ${OUT3}/></g></g>`;
    // the outlets near the floor, a power strip, the fan, the fridge, the TV
    const outlet = (x, y) => `<g><rect x="${x - 50}" y="${y - 34}" width="100" height="68" rx="8" fill="#f4f0e6" ${OUT3}/>${[-20, 20].map((d) => `<g><rect x="${x + d - 10}" y="${y - 12}" width="6" height="14" fill="${INK}"/><rect x="${x + d + 4}" y="${y - 12}" width="6" height="14" fill="${INK}"/></g>`).join("")}</g>`;
    s += outlet(240, G - 230) + outlet(-420, G - 230);
    s += `<path d="M240,${G - 220}C260,${G - 120} 340,${G - 60} 420,${G - 40}" stroke="#2a2a2a" stroke-width="7" fill="none"/><rect x="400" y="${G - 60}" width="160" height="40" rx="8" fill="#f4f0e6" ${OUT3}/><circle id="${id}-led" cx="420" cy="${G - 40}" r="6" fill="#ff4a3a"/>`;
    const FX = o.fridgeX ?? 1520;
    s += `<g id="${id}-fridge"><rect x="${FX}" y="${G - 760}" width="300" height="760" rx="16" fill="#d8e4e8" ${OUT}/><path d="M${FX},${G - 520}h300" stroke="${INK}" stroke-width="4"/><rect x="${FX + 268}" y="${G - 700}" width="12" height="90" rx="4" fill="#9aa4a8"/>
      <rect id="${id}-fh" x="${FX + 266}" y="${G - 480}" width="14" height="100" rx="5" fill="#9aa4a8" ${OUT3}/><path d="M${FX + 220},${G - 300}V${G - 360}h-30" stroke="#6a7478" stroke-width="5" fill="none"/></g>`;
    s += `<g><rect x="-1060" y="${G - 420}" width="380" height="420" fill="#6a4a32" ${OUT}/><rect x="-1040" y="${G - 700}" width="340" height="250" rx="14" fill="#1a1f24" ${OUT}/><rect x="-1020" y="${G - 680}" width="300" height="210" rx="8" fill="#2a3a4a"/></g>`;
    s += `<g transform="translate(560,${G})"><path d="M0,0V-560" stroke="#d8dcd8" stroke-width="16"/><ellipse cx="0" cy="-12" rx="90" ry="16" fill="#d8dcd8" ${OUT3}/><circle cx="0" cy="-620" r="110" fill="none" stroke="#9aa4a8" stroke-width="10"/>
      <g class="kfan">${[0, 120, 240].map((a) => `<path d="M0,-620L${f1(Math.cos(a * Math.PI / 180) * 96)},${f1(-620 + Math.sin(a * Math.PI / 180) * 96)}" stroke="#7fb3c9" stroke-width="40" stroke-linecap="round" opacity=".85"/>`).join("")}</g><circle cx="0" cy="-620" r="22" fill="#d8dcd8" ${OUT3}/></g>`;
    // the stairs up to the sleeping floor, by the door under the switch (each step 90 high, 110 deep; the 3rd top is at G - 270)
    if (o.stairs !== false) s += `<g>${[0, 1, 2, 3, 4, 5, 6].map((k) => `<rect x="${700 + k * 110}" y="${G - 90 * (k + 1)}" width="${560 - k * 110 + 400}" height="${90 * (k + 1)}" fill="${k % 2 ? "#7a5a3c" : "#6a4a32"}" ${OUT3}/>`).join("")}</g>`;
    // the floor (tiles) and the flood water over it (#id-water: a group to move up; drawn in the act layer over the people)
    s += `<rect x="-1200" y="${G}" width="3500" height="1200" fill="#8a8270"/>${Array.from({ length: 12 }, (_, k) => `<path d="M-1200,${G + 40 + k * 90}H2300" stroke="#6f6858" stroke-width="3"/>`).join("")}`;
    // after the flood: a brown tide line on the walls at the night's level, mud over the floor and up the bottom of everything
    if (o.mud) s += `<path d="M-1200,${G - 170}Q-600,${G - 186} 0,${G - 168}T1200,${G - 176}T2300,${G - 170}V${G}H-1200Z" fill="#6a5a3a" opacity=".35"/><path d="M-1200,${G - 170}Q-600,${G - 186} 0,${G - 168}T1200,${G - 176}T2300,${G - 170}" stroke="#5a4a2a" stroke-width="8" fill="none" opacity=".7"/>
      ${Array.from({ length: 16 }, (_, k) => `<ellipse cx="${f1(-1100 + r() * 3300)}" cy="${f1(G + 30 + r() * 500)}" rx="${f1(60 + r() * 160)}" ry="${f1(10 + r() * 22)}" fill="#5a4a2a" opacity=".55"/>`).join("")}`;
    put(L.set, s);
    put(L.act, `<g id="${id}-water" transform="translate(0,0)"><rect x="-1200" y="${WL}" width="3500" height="1600" fill="url(#ksMud)"/><path class="rip" d="M-1200,${WL}Q-600,${WL - 10} 0,${WL}T1200,${WL}T2300,${WL}" stroke="#d8d0a8" stroke-width="6" fill="none" opacity=".6"/>
      ${Array.from({ length: 14 }, (_, k) => `<path class="rip" d="M${f1(-900 + r() * 2900)},${f1(WL + 30 + r() * 300)}h${f1(40 + r() * 120)}" stroke="#a89f78" stroke-width="4" stroke-linecap="round" opacity=".5"/>`).join("")}</g>`);
    put(L.light, `<g id="${id}-tube"><rect x="380" y="-200" width="420" height="10" fill="#e8f6ff" opacity="0"/></g>`);
    put(L.glow, `<g class="ktube" id="${id}-tubeg"><rect x="300" y="${G - 1480}" width="580" height="30" rx="14" fill="#f4fbff"/><ellipse cx="590" cy="${G - 1300}" rx="1200" ry="900" fill="url(#ksTube)"/></g>`);
  }

  // ---------------- the front of the house: steps into the flood, the meter, a lamp, the pole ----------------
  function porchFlood(L, o = {}) {
    const id = o.id || "pf", r = mk(o.seed || 227), G = o.ground ?? 1480, W = o.water ?? G + 160;
    sky(L, { moon: false, dusk: o.dusk }, r);
    farLine(L, 1080, r, { temple: 980, dark: o.dark });  // o.dark: the power is cut — no window, no lamp, no lights across the fields
    water(L, 1080, r, {});
    let s = `<path d="M-1200,-800H560V${G}H-1200Z" fill="#cfc5a8"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1180 + k * 60},-800V${G}" stroke="#b3a98c" stroke-width="3"/>`).join("")}
      <rect x="-380" y="${G - 900}" width="320" height="380" fill="${o.dark ? "#1a1f26" : "#ffd38a"}" opacity=".9" ${OUT}/><path d="M-220,${G - 900}v380M-380,${G - 710}h320" stroke="${INK}" stroke-width="7"/>
      <rect x="140" y="${G - 1100}" width="300" height="1100" fill="#5a3f2a" ${OUT}/>`;
    // the meter box on the wall
    s += `<g><rect x="-760" y="${G - 1180}" width="200" height="260" rx="10" fill="#d8d0c0" ${OUT}/><circle cx="-660" cy="${G - 1080}" r="64" fill="#e8f0f2" stroke="${INK}" stroke-width="4" opacity=".9"/>
      <rect x="-700" y="${G - 1110}" width="80" height="22" fill="${INK}"/><ellipse cx="-660" cy="${G - 1050}" rx="40" ry="8" fill="#b8c0c4" ${OUT3}/><path d="M-660,${G - 920}V-800" stroke="#2a2a2a" stroke-width="10"/></g>`;
    s += `<rect x="-1200" y="${G}" width="1800" height="40" fill="#8a8270" ${OUT}/>${[0, 1, 2, 3].map((k) => `<rect x="${560 + k * 70}" y="${G + 40 + k * 60}" width="140" height="20" rx="4" fill="#9a9070" ${OUT3}/>`).join("")}`;
    s += `<rect x="560" y="${W}" width="2000" height="1400" fill="url(#ksWater)"/>${Array.from({ length: 14 }, (_, k) => `<path class="rip" d="M${f1(600 + r() * 1100)},${f1(W + 20 + r() * 600)}h${f1(40 + r() * 100)}" stroke="#6c7f9a" stroke-width="4" stroke-linecap="round" opacity=".45"/>`).join("")}`;
    const p = pole(o.poleX ?? 1240, W, 1400, { lamp: true });
    s += p.s + `<path d="M${p.wires[0][0]},${p.wires[0][1]}Q900,${p.wires[0][1] + 140} 420,${G - 1300}" stroke="#1a1d20" stroke-width="5" fill="none"/>`;
    put(L.set, s);
    if (!o.dark) put(L.glow, `<circle class="lamp" cx="${(o.poleX ?? 1240) + 70}" cy="${W - 1400 + 130}" r="300" fill="url(#ksLamp)"/><circle cx="-220" cy="${G - 710}" r="420" fill="url(#ksLamp)" opacity=".7"/>`);
    put(L.act, `<g id="${id}-wfront"><rect x="560" y="${W}" width="2000" height="1400" fill="#14202a" opacity=".8"/><path class="rip" d="M560,${W}H2560" stroke="#9fb0c8" stroke-width="5" opacity=".6"/></g>`);
  }

  // ---------------- chapter card: the electric meter running backwards ----------------
  function meterCard(L, o = {}) {
    const id = o.id || "mc", X = 540, Y = 900;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#3b2a1c"/>`);
    let m = "";
    for (let k = 0; k < 24; k++) m += `<path d="M${-1100 + k * 120},-800V2800" stroke="#2a1d14" stroke-width="8"/>`;
    put(L.mid, m);
    let s = `<rect x="${X - 300}" y="${Y - 520}" width="600" height="1040" rx="40" fill="#1d1f22" ${OUT}/><path d="M${X - 240},${Y - 460}Q${X},${Y - 600} ${X + 240},${Y - 460}V${Y + 300}H${X - 240}Z" fill="#dfe9ee" fill-opacity=".9" ${OUT}/>
      <rect x="${X - 200}" y="${Y - 380}" width="400" height="260" rx="10" fill="#f4f0e6" ${OUT3}/>
      <text x="${X}" y="${Y - 330}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="40" fill="${INK}">kWh</text>
      <g><rect x="${X - 170}" y="${Y - 300}" width="340" height="80" rx="6" fill="#1d1f22"/><g id="${id}-digits">${[0, 1, 2, 3, 4].map((k) => `<text x="${X - 136 + k * 68}" y="${Y - 238}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="${k === 4 ? "#ff6a5a" : "#f4f0e6"}" class="kdg" data-k="${k}">${[0, 4, 2, 7, 1][k]}</text>`).join("")}</g></g>
      <text x="${X}" y="${Y - 150}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#6a6a6a">220V 5(15)A 50Hz</text>
      <rect x="${X - 220}" y="${Y - 40}" width="440" height="60" fill="#c9cfd2" ${OUT3}/><g id="${id}-disc"><ellipse cx="${X}" cy="${Y - 10}" rx="200" ry="22" fill="#d8dee2" ${OUT3}/><rect id="${id}-mark" x="${X - 10}" y="${Y - 30}" width="20" height="40" fill="${INK}"/></g>
      <rect x="${X - 140}" y="${Y + 360}" width="280" height="120" rx="10" fill="#2a2c30" ${OUT3}/>${[-80, 0, 80].map((d) => `<circle cx="${X + d}" cy="${Y + 420}" r="22" fill="#8a8e90" ${OUT3}/>`).join("")}`;
    // the paper tag hung on the meter
    s += `<g id="${id}-tag" transform="rotate(-6 ${X + 210} ${Y + 210})"><path d="M${X + 210},${Y + 150}l40,-90" stroke="#c9a86a" stroke-width="5"/><rect x="${X + 40}" y="${Y + 150}" width="380" height="150" rx="10" fill="#f4ecd8" ${OUT3}/>
      <text x="${X + 230}" y="${Y + 248}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#b8261c">${o.text || "6 ชั่วโมงก่อน"}</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="${X}" cy="${Y - 200}" r="700" fill="url(#ksLamp)" opacity=".5"/>`);
  }

  // ---------------- the old one-baht comic: four panels in black and green on yellowed newsprint ----------------
  function comicLegend(L, o = {}) {
    const id = o.id || "cl", PY = [0, 1000, 2000, 3000], P = "#1a1a14", GR = "#3daa5a";
    put(L.sky, `<rect x="-1200" y="-1800" width="3500" height="6600" fill="#d8c79a"/><rect x="-1200" y="-1800" width="3500" height="6600" fill="url(#ksDots)"/>`);
    const frame = (y, inner) => `<g><rect x="60" y="${y + 60}" width="960" height="880" fill="#efe2bd" stroke="${P}" stroke-width="10"/>${inner}<rect x="60" y="${y + 60}" width="960" height="880" fill="none" stroke="${P}" stroke-width="10"/></g>`;
    const woman = (x, y, s, o2 = {}) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-70,0L-50,-300Q0,-330 50,-300L70,0Z" fill="${o2.fill || "#efe2bd"}" stroke="${P}" stroke-width="7"/>
      ${o2.head === false ? `<path d="M-24,-310h48" stroke="${P}" stroke-width="7"/>` : `<circle cx="0" cy="-360" r="46" fill="#efe2bd" stroke="${P}" stroke-width="7"/><path d="M-46,-370Q-40,-420 0,-420Q40,-420 46,-370Q30,-390 0,-392Q-30,-390 -46,-370Z" fill="${P}"/><path d="M-16,-350q6,6 12,0M8,-350q6,6 12,0M-10,-326q10,8 20,0" stroke="${P}" stroke-width="5" fill="none"/>`}
      <path d="M-56,-260L-110,-120M56,-260L110,-120" stroke="${P}" stroke-width="12" stroke-linecap="round"/></g>`;
    const head = (x, y, s) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-50,-10Q-50,-90 0,-92Q50,-90 50,-10Q46,50 0,58Q-46,50 -50,-10Z" fill="${P}"/>
      <path d="M-26,-14q10,-10 20,0M6,-14q10,-10 20,0" stroke="${GR}" stroke-width="9"/>
      <path d="M-6,58C-10,120 0,160 -30,210C-50,250 -10,290 10,330M10,60C40,120 50,170 30,230" stroke="${GR}" stroke-width="14" fill="none" stroke-linecap="round"/>
      <path d="M-30,80Q-70,90 -60,150Q-40,170 -20,130ZM30,80Q70,90 60,150Q40,170 20,130Z" fill="${GR}" stroke="${P}" stroke-width="5"/>
      ${Array.from({ length: 9 }, (_, i) => `<path d="M${-40 + i * 10},-70Q${-80 + i * 20},${20 + (i % 3) * 10} ${-70 + i * 18},${110 + (i % 2) * 30}" stroke="${P}" stroke-width="6" fill="none"/>`).join("")}</g>`;
    // the cover (y -1000): the title in green, the price, the head with its guts glowing over a field
    let s = `<g><rect x="60" y="-940" width="960" height="880" fill="#efe2bd" stroke="${P}" stroke-width="10"/><rect x="60" y="-940" width="960" height="200" fill="${P}"/>
      <text x="540" y="-790" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="150" fill="${GR}" stroke="#efe2bd" stroke-width="4">กระสือ</text>
      <g transform="translate(900,-680) rotate(-12)"><circle r="70" fill="#e04a3a" stroke="${P}" stroke-width="6"/><text x="0" y="-6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#efe2bd">1</text><text x="0" y="40" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#efe2bd">บาท</text></g>
      <rect x="60" y="-740" width="960" height="680" fill="${P}" opacity=".85"/><path d="M60,-200H1020" stroke="${GR}" stroke-width="6"/>${head(540, -560, 1.7)}
      <text x="540" y="-100" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#efe2bd">ผีหัวลอย ไส้เรืองแสง!</text></g>`;
    // 1. by day: a kind village woman with a basket, sun, chickens
    s += frame(PY[0], `<circle cx="860" cy="200" r="70" fill="none" stroke="${P}" stroke-width="7"/>${[0, 1, 2, 3, 4, 5, 6, 7].map((k) => `<path d="M${860 + Math.cos(k * 0.785) * 90},${200 + Math.sin(k * 0.785) * 90}l${Math.cos(k * 0.785) * 30},${Math.sin(k * 0.785) * 30}" stroke="${P}" stroke-width="6"/>`).join("")}
      <path d="M60,${PY[0] + 760}H1020" stroke="${P}" stroke-width="6"/>${woman(420, PY[0] + 760, 1.2)}<path d="M540,${PY[0] + 470}q50,10 60,60h-120q10,-50 60,-60z" fill="#efe2bd" stroke="${P}" stroke-width="6"/>`);
    // 2. at night: her body asleep on the mat, the head pulling free, the guts coming with it
    s += frame(PY[1], `<rect x="60" y="${PY[1] + 60}" width="960" height="880" fill="${P}" opacity=".88"/><rect x="160" y="${PY[1] + 700}" width="760" height="40" fill="#5a5a40"/>
      <path d="M220,${PY[1] + 690}Q500,${PY[1] + 640} 820,${PY[1] + 690}" stroke="#efe2bd" stroke-width="8" fill="none"/><g id="${id}-h2">${head(560, PY[1] + 420, 1.4)}</g>
      <g fill="#c8ff9a">${[0, 1, 2, 3, 4].map((k) => `<circle cx="${380 + k * 90}" cy="${PY[1] + 240 + (k % 2) * 30}" r="5"/>`).join("")}</g>`);
    // 3. it floats over the fields toward the lights (a lamp on a pole, a lit window)
    s += frame(PY[2], `<rect x="60" y="${PY[2] + 60}" width="960" height="880" fill="${P}" opacity=".9"/><path d="M60,${PY[2] + 700}H1020" stroke="${GR}" stroke-width="6"/>
      ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${100 + k * 140},${PY[2] + 700}l20,-40l20,40" stroke="${GR}" stroke-width="5" fill="none"/>`).join("")}
      <path d="M860,${PY[2] + 700}V${PY[2] + 260}" stroke="#efe2bd" stroke-width="16"/><circle cx="900" cy="${PY[2] + 290}" r="28" fill="#efe2bd"/><circle cx="900" cy="${PY[2] + 290}" r="70" fill="#efe2bd" opacity=".25"/>
      <g id="${id}-h3">${head(420, PY[2] + 360, 0.9)}</g><path d="M300,${PY[2] + 470}Q360,${PY[2] + 420} 420,${PY[2] + 440}" stroke="${GR}" stroke-width="5" stroke-dasharray="12 12" fill="none"/>`);
    // 4. it calls a name from the dark: a child at a window, the balloon full of dots
    s += frame(PY[3], `<rect x="60" y="${PY[3] + 60}" width="960" height="880" fill="${P}" opacity=".92"/><rect x="640" y="${PY[3] + 340}" width="300" height="360" fill="#efe2bd" stroke="#efe2bd" stroke-width="6"/>
      <circle cx="790" cy="${PY[3] + 500}" r="50" fill="${P}"/><path d="M730,${PY[3] + 700}Q790,${PY[3] + 560} 850,${PY[3] + 700}Z" fill="${P}"/>
      <g id="${id}-h4">${head(280, PY[3] + 520, 1.0)}</g><g><path d="M140,${PY[3] + 140}H560Q600,${PY[3] + 140} 600,${PY[3] + 180}V${PY[3] + 280}Q600,${PY[3] + 320} 560,${PY[3] + 320}H360L300,${PY[3] + 380}L310,${PY[3] + 320}H140Q100,${PY[3] + 320} 100,${PY[3] + 280}V${PY[3] + 180}Q100,${PY[3] + 140} 140,${PY[3] + 140}Z" fill="#efe2bd" stroke="${P}" stroke-width="6"/>
      ${[0, 1, 2].map((k) => `<circle cx="${290 + k * 60}" cy="${PY[3] + 230}" r="12" fill="${P}"/>`).join("")}</g>`);
    put(L.set, s + `<rect x="-1200" y="-800" width="3500" height="5600" fill="url(#ksDotsG)" opacity=".12"/>`);
  }

  // ---------------- the main switch close up ----------------
  function switchClose(L, o = {}) {
    const id = o.id || "sc", X = 540, Y = 900;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#ksWall)"/>`);
    put(L.mid, `<path d="M${X},${Y - 1600}V${Y - 360}M${X},${Y + 380}V${Y + 1700}" stroke="#2a2a2a" stroke-width="26"/><path d="M-1200,${Y + 700}H2300" stroke="#9f9478" stroke-width="600" opacity=".5"/>`);
    let s = `<rect x="${X - 260}" y="${Y - 380}" width="520" height="760" rx="30" fill="#efe9dc" ${OUT}/><rect x="${X - 200}" y="${Y - 320}" width="400" height="130" rx="16" fill="#d8d0c0" ${OUT3}/>
      <rect x="${X - 200}" y="${Y + 190}" width="400" height="130" rx="16" fill="#d8d0c0" ${OUT3}/><path d="M${X - 120},${Y - 255}h240M${X - 120},${Y + 255}h240" stroke="#c9873a" stroke-width="10"/>
      ${[-80, 80].map((d) => `<rect x="${X + d - 22}" y="${Y - 190}" width="44" height="80" fill="#c9873a" ${OUT3}/><rect x="${X + d - 22}" y="${Y + 110}" width="44" height="80" fill="#c9873a" ${OUT3}/>`).join("")}
      <circle cx="${X}" cy="${Y + 150}" r="20" fill="${INK}"/>
      <g id="${id}-lever" transform="rotate(0 ${X} ${Y + 150})">${[-80, 80].map((d) => `<rect x="${X + d - 14}" y="${Y - 150}" width="28" height="300" fill="#d8a04a" ${OUT3}/>`).join("")}<rect x="${X - 130}" y="${Y - 200}" width="260" height="60" rx="12" fill="#1d1d1d" ${OUT}/></g>`;
    put(L.set, s);
    if (o.hand !== false) put(L.act, `<g id="${id}-hand" transform="translate(0,0)"><path d="M${X + 260},${Y + 1200}L${X + 60},${Y - 120}" stroke="${INK}" stroke-width="150" stroke-linecap="round"/><path d="M${X + 260},${Y + 1200}L${X + 60},${Y - 120}" stroke="${o.sleeve || "#e8a33a"}" stroke-width="136" stroke-linecap="round"/>
      <path d="M${X + 60},${Y - 60}L${X + 20},${Y - 170}" stroke="${INK}" stroke-width="110" stroke-linecap="round"/><path d="M${X + 60},${Y - 60}L${X + 20},${Y - 170}" stroke="${o.skin || "#e8b48a"}" stroke-width="96" stroke-linecap="round"/>
      ${[-36, -12, 12, 36].map((d) => `<path d="M${X + 20 + d},${Y - 200}q-30,-20 -40,10" stroke="${INK}" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M${X + 20 + d},${Y - 200}q-30,-20 -40,10" stroke="${o.skin || "#e8b48a"}" stroke-width="22" fill="none" stroke-linecap="round"/>`).join("")}</g>`);
    put(L.glow, `<g id="${id}-spark" opacity="0"><circle cx="${X}" cy="${Y - 120}" r="260" fill="url(#ksArc)"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${X},${Y - 120}l${Math.cos(k) * 120},${Math.sin(k) * 120}" stroke="#eafcff" stroke-width="5"/>`).join("")}</g>`);
  }

  // ---------------- end card: the danger sign on a power pole, a note pinned to it ----------------
  function poleSign(L, o = {}) {
    const id = o.id || "ps", r = mk(o.seed || 233);
    sky(L, { moon: { x: 860, y: 260, r: 50 } }, r);
    water(L, 1350, r, {});
    let s = `<rect x="440" y="-800" width="200" height="3400" fill="#8a8e8c" ${OUT}/><path d="M470,-800V2600" stroke="#6f7472" stroke-width="8"/>`;
    s += `<g id="${id}-sign" transform="rotate(-2 540 900)"><rect x="200" y="560" width="680" height="560" rx="20" fill="#f2c94a" ${OUT}/><rect x="230" y="590" width="620" height="500" rx="12" fill="none" stroke="${INK}" stroke-width="8"/>
      <path d="M540,640L640,800H440Z" fill="${INK}"/><path d="M548,670l-26,60h30l-20,52" stroke="#f2c94a" stroke-width="10" fill="none"/>
      <text x="540" y="880" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="${INK}">อันตราย</text>
      <text x="540" y="950" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="46" fill="${INK}">ไฟฟ้าแรงสูง</text>
      <g transform="rotate(5 560 1050)"><rect x="300" y="960" width="500" height="230" fill="#f2ecdc" stroke="${INK}" stroke-width="3"/><circle cx="550" cy="976" r="10" fill="#b8261c"/>
        <text x="550" y="1036" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="42" fill="#a8140c">${o.ep || "ตอนที่ 2"}</text>
        <text x="550" y="1110" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#a8140c">${o.title || "อย่าจับตัว"}</text>
        <text x="760" y="1170" text-anchor="end" font-family="Kanit" font-weight="700" font-size="28" fill="#5a4a3a">— ลุงเปี๊ยก ช่างไฟ</text></g></g>`;
    for (let k = 0; k < 6; k++) s += `<g class="drip" data-i="${k}"><path d="M${f1(240 + k * 110 + r() * 30)},1118c-7,12 -7,20 0,22c7,-2 7,-10 0,-22z" fill="#9fc3d8" opacity=".85"/></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="760" r="760" fill="url(#ksLamp)" opacity=".4"/>`);
  }

  // ---------------- top-down on the upstairs floor: เต้ย on his back, ฝน's hands on his chest, her phone on the boards calling 1669 ----------------
  function cprFloor(L, o = {}) {
    const id = o.id || "cf", r = mk(o.seed || 239), X = 540, sk = "#d9a074", sh = "#3faa6a", shS = "#2f8a54";
    let m = `<rect x="-900" y="-600" width="2900" height="3400" fill="#5a3f2a"/>`;
    for (let x = -880; x < 2000; x += 130) m += `<path d="M${x},-600V2800" stroke="#3b2a1c" stroke-width="7"/>${[0, 1, 2].map((k) => `<path d="M${x + 6},${f1(-200 + k * 1000 + r() * 400)}h118" stroke="#3b2a1c" stroke-width="5"/>`).join("")}`;
    for (let k = 0; k < 18; k++) m += `<ellipse cx="${f1(-200 + r() * 1500)}" cy="${f1(r() * 2200)}" rx="${f1(20 + r() * 60)}" ry="${f1(6 + r() * 14)}" fill="#3b2a1c" opacity=".5"/>`;
    // water dripping off him onto the boards
    m += `<ellipse cx="${X}" cy="1250" rx="420" ry="760" fill="#1d2a33" opacity=".35"/>`;
    put(L.mid, m);
    // her phone on the floor, on a call to 1669 (the screen lights the boards)
    put(L.set, `<g transform="translate(180,520) rotate(-18)"><rect x="-70" y="-130" width="140" height="260" rx="20" fill="#1d1f22" ${OUT}/><rect x="-58" y="-112" width="116" height="200" rx="8" fill="#e8f0f2"/>
      <text x="0" y="-60" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#e0362c">1669</text><text x="0" y="-20" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#2e2a26">กำลังโทร…</text>
      <circle cx="0" cy="50" r="24" fill="#e0362c"/><path d="M-12,50h24" stroke="#fff" stroke-width="6" stroke-linecap="round"/></g>`);
    const shoe = (x) => `<ellipse cx="${x}" cy="1900" rx="36" ry="24" fill="${sk}" ${OUT}/>`;
    let b = `<g id="${id}-body" transform="rotate(-5 ${X} 1100)">
      <path d="M${X - 80},1380L${X - 100},1840Q${X - 96},1880 ${X - 60},1880L${X - 34},1390Z" fill="${sk}" ${OUT}/><path d="M${X + 80},1380L${X + 100},1840Q${X + 96},1880 ${X + 60},1880L${X + 34},1390Z" fill="${sk}" ${OUT}/>${shoe(X - 80)}${shoe(X + 80)}
      <path d="M${X - 130},1300L${X - 120},1560H${X + 120}L${X + 130},1300Z" fill="#3f6fb0" ${OUT}/>
      <path d="M${X - 140},880L${X - 210},1290Q${X - 210},1330 ${X - 180},1334L${X - 146},1330L${X - 118},960Z" fill="${sh}" ${OUT}/><path d="M${X + 140},880L${X + 210},1290Q${X + 210},1330 ${X + 180},1334L${X + 146},1330L${X + 118},960Z" fill="${sh}" ${OUT}/>
      <ellipse cx="${X - 192}" cy="1352" rx="28" ry="34" fill="${sk}" ${OUT}/><ellipse cx="${X + 192}" cy="1352" rx="28" ry="34" fill="${sk}" ${OUT}/>
      <g id="${id}-chest"><path d="M${X - 146},870Q${X},830 ${X + 146},870L${X + 124},1320H${X - 124}Z" fill="${sh}" ${OUT}/><path d="M${X - 146},870Q${X},830 ${X + 146},870" stroke="${shS}" stroke-width="10" fill="none"/>
        <text x="${X}" y="1150" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="150" fill="#f4ecd8">9</text></g>
      <rect x="${X - 32}" y="800" width="64" height="70" fill="${sk}" ${OUT}/>
      <g id="${id}-head"><ellipse cx="${X}" cy="700" rx="116" ry="126" fill="${sk}" ${OUT}/><path d="M${X - 118},660Q${X - 116},556 ${X},546Q${X + 116},556 ${X + 118},660Q${X + 86},602 ${X},598Q${X - 86},602 ${X - 118},660Z" fill="#221a16" ${OUT}/>
        <g id="${id}-shut"><path d="M${X - 62},700q22,10 44,0M${X + 18},700q22,10 44,0" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/></g>
        <g id="${id}-open" opacity="0"><ellipse cx="${X - 40}" cy="700" rx="16" ry="20" fill="#fff" ${OUT3}/><ellipse cx="${X + 40}" cy="700" rx="16" ry="20" fill="#fff" ${OUT3}/><circle cx="${X - 40}" cy="704" r="9" fill="#2a1d16"/><circle cx="${X + 40}" cy="704" r="9" fill="#2a1d16"/></g>
        <ellipse id="${id}-lips" cx="${X}" cy="772" rx="24" ry="10" fill="#6f8fb0" stroke="#3a2a22" stroke-width="4"/></g></g>`;
    // her hands, stacked on the middle of his chest; mustard hoodie sleeves from the left
    const hand = (x, y, rot) => `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M-300,-34H-56V34H-300Z" fill="#e8a33a" ${OUT}/><ellipse cx="0" cy="0" rx="68" ry="52" fill="#e2ad85" ${OUT}/>${[-30, -10, 10, 30].map((d) => `<path d="M30,${d}h40" stroke="${INK}" stroke-width="20" stroke-linecap="round"/><path d="M30,${d}h40" stroke="#e2ad85" stroke-width="13" stroke-linecap="round"/>`).join("")}</g>`;
    b += `<g id="${id}-hands" opacity="${o.hands ?? 1}">${hand(X - 10, 1060, 0)}${hand(X + 4, 1046, -8)}</g>`;
    put(L.act, b);
    put(L.glow, `<circle cx="180" cy="520" r="520" fill="url(#ksTube)" opacity=".8"/>`);
  }

  // ---------------- close up: ฝน's hand on the door bolt, green light coming through the gaps between the planks ----------------
  function latchClose(L, o = {}) {
    const id = o.id || "lc";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#1a120c"/>`);
    let s = "";
    for (let k = 0; k < 7; k++) s += `<rect x="${-120 + k * 200}" y="-400" width="190" height="2800" fill="${k % 2 ? "#5a3f2a" : "#523a26"}" ${OUT3}/>${[0, 1, 2].map((j) => `<path d="M${-100 + k * 200},${f1(100 + j * 700 + (k % 3) * 60)}q60,-14 150,6" stroke="#3b2a1c" stroke-width="5" fill="none"/>`).join("")}`;
    // the bolt: a plate on the door, the sliding bar, the keeper on the frame
    s += `<rect x="260" y="900" width="420" height="120" rx="10" fill="#8a8e90" ${OUT}/><rect x="760" y="890" width="160" height="140" rx="10" fill="#8a8e90" ${OUT}/>
      <g id="${id}-bolt"><rect x="300" y="935" width="560" height="50" rx="25" fill="#c9cfd2" ${OUT}/><path d="M520,935V870" stroke="${INK}" stroke-width="34" stroke-linecap="round"/><path d="M520,935V870" stroke="#c9cfd2" stroke-width="22" stroke-linecap="round"/></g>`;
    put(L.set, s);
    put(L.act, `<g id="${id}-hand"><path d="M-200,1500L380,980" stroke="${INK}" stroke-width="190" stroke-linecap="round"/><path d="M-200,1500L380,980" stroke="#e8a33a" stroke-width="172" stroke-linecap="round"/>
      <ellipse cx="470" cy="900" rx="96" ry="74" fill="#e2ad85" ${OUT}/>${[-40, -14, 12, 38].map((d) => `<path d="M${500 + d},860q20,-30 40,-6" stroke="${INK}" stroke-width="36" fill="none" stroke-linecap="round"/><path d="M${500 + d},860q20,-30 40,-6" stroke="#e2ad85" stroke-width="24" fill="none" stroke-linecap="round"/>`).join("")}</g>`);
    // the gaps between the planks glow green (#id-gaps)
    put(L.glow, `<g id="${id}-gaps">${[0, 1, 2, 3, 4, 5].map((k) => `<rect x="${66 + k * 200}" y="-400" width="10" height="2800" fill="#9fff8a" opacity=".55"/>`).join("")}<ellipse cx="540" cy="1900" rx="900" ry="300" fill="url(#ksGlow)"/></g>`);
  }

  // ---------------- close up: the outlet behind the fridge, burnt black; a tester screwdriver held to it ----------------
  function outletClose(L, o = {}) {
    const id = o.id || "oc", X = 540, Y = 960;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#ksWall)"/>`);
    put(L.mid, `<path d="M-1200,${Y + 260}Q-600,${Y + 244} 0,${Y + 262}T1200,${Y + 254}T2300,${Y + 260}V2800H-1200Z" fill="#6a5a3a" opacity=".45"/><path d="M-1200,${Y + 260}Q-600,${Y + 244} 0,${Y + 262}T1200,${Y + 254}T2300,${Y + 260}" stroke="#5a4a2a" stroke-width="10" fill="none" opacity=".7"/>
      <rect x="760" y="-800" width="600" height="3600" fill="#c8d4d8" ${OUT}/><path d="M760,-800V2800" stroke="#9aa4a8" stroke-width="10"/>`);
    let s = `<rect x="${X - 230}" y="${Y - 160}" width="460" height="320" rx="30" fill="#f4f0e6" ${OUT}/>
      <g id="${id}-soot"><ellipse cx="${X - 30}" cy="${Y - 60}" rx="200" ry="150" fill="#1d1a16" opacity=".75"/><ellipse cx="${X - 60}" cy="${Y - 160}" rx="90" ry="120" fill="#1d1a16" opacity=".5"/><path d="M${X - 120},${Y - 120}q-30,-90 10,-200M${X - 20},${Y - 150}q20,-80 -10,-160" stroke="#1d1a16" stroke-width="22" fill="none" opacity=".45" stroke-linecap="round"/></g>
      ${[-90, 90].map((d) => `<g><rect x="${X + d - 22}" y="${Y - 40}" width="12" height="50" fill="${INK}"/><rect x="${X + d + 10}" y="${Y - 40}" width="12" height="50" fill="${INK}"/></g>`).join("")}
      <g transform="translate(${X - 90},${Y - 10}) rotate(18)"><path d="M-60,-40Q-70,40 -30,70H40Q70,30 60,-40Z" fill="#2a2622" ${OUT}/><path d="M-30,70Q-40,140 10,220" stroke="#2a2622" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M-50,-20q30,-30 70,0" stroke="#5a3a1a" stroke-width="10" fill="none"/></g>`;
    put(L.set, s);
    // ลุงเปี๊ยก's hand with the tester screwdriver; its neon (#id-neon) stays dark (no power)
    put(L.act, `<g id="${id}-tester"><path d="M1400,1700L${X + 230},${Y + 80}" stroke="${INK}" stroke-width="170" stroke-linecap="round"/><path d="M1400,1700L${X + 230},${Y + 80}" stroke="#7c8a8e" stroke-width="152" stroke-linecap="round"/>
      <ellipse cx="${X + 200}" cy="${Y + 60}" rx="90" ry="70" fill="#b67d55" ${OUT}/><path d="M${X + 190},${Y + 40}L${X + 80},${Y - 30}" stroke="${INK}" stroke-width="42" stroke-linecap="round"/><path d="M${X + 190},${Y + 40}L${X + 80},${Y - 30}" stroke="#e04a3a" stroke-width="30" stroke-linecap="round"/>
      <ellipse id="${id}-neon" cx="${X + 136}" cy="${Y + 6}" rx="10" ry="8" fill="#5a4a3a"/><path d="M${X + 80},${Y - 30}L${X + 40},${Y - 54}" stroke="#c9cfd2" stroke-width="12" stroke-linecap="round"/></g>`);
  }

  // ---------------- top-down: ป้าแช่ม asleep on a mat, a blanket up to her neck, the curry pot, a rag smeared green by the pillow ----------------
  function chaemTop(L, o = {}) {
    const id = o.id || "ct", r = mk(o.seed || 241), X = 540, sk = "#e6d2bc";
    let m = `<rect x="-900" y="-600" width="2900" height="3400" fill="#6a4a32"/>`;
    for (let x = -880; x < 2000; x += 140) m += `<path d="M${x},-600V2800" stroke="#4a3424" stroke-width="7"/>`;
    put(L.mid, m);
    // the mat (เสื่อ): woven stripes
    let s = `<rect x="${X - 380}" y="380" width="760" height="1500" rx="20" fill="#d8b878" ${OUT}/>${Array.from({ length: 30 }, (_, k) => `<path d="M${X - 380},${400 + k * 50}H${X + 380}" stroke="${k % 3 ? "#c4a060" : "#a8402a"}" stroke-width="${k % 3 ? 4 : 10}"/>`).join("")}`;
    // the pillow, the head (her bun on the pillow), the blanket to the chin
    s += `<rect x="${X - 170}" y="420" width="340" height="190" rx="60" fill="#f4ecd8" ${OUT}/>
      <g id="${id}-head"><circle cx="${X}" cy="470" r="44" fill="#3a3330" ${OUT}/><ellipse cx="${X}" cy="600" rx="112" ry="124" fill="${sk}" ${OUT}/><path d="M${X - 114},560Q${X - 110},468 ${X},460Q${X + 110},468 ${X + 114},560Q${X + 80},508 ${X},504Q${X - 80},508 ${X - 114},560Z" fill="#3a3330" ${OUT}/>
        <g id="${id}-shut"><path d="M${X - 60},610q22,10 44,0M${X + 16},610q22,10 44,0" stroke="#5a4a3a" stroke-width="7" fill="none" stroke-linecap="round"/></g>
        <g id="${id}-open" opacity="0"><ellipse cx="${X - 38}" cy="608" rx="16" ry="12" fill="#fff" ${OUT3}/><ellipse cx="${X + 38}" cy="608" rx="16" ry="12" fill="#fff" ${OUT3}/><circle cx="${X - 38}" cy="610" r="8" fill="#2a1d16"/><circle cx="${X + 38}" cy="610" r="8" fill="#2a1d16"/></g>
        <g id="${id}-smile"><path d="M${X - 28},668q28,${o.smile ? 18 : 4} 56,0" stroke="#8a5a4a" stroke-width="6" fill="none" stroke-linecap="round"/></g></g>
      <path d="M${X - 300},700Q${X},660 ${X + 300},700L${X + 320},1700Q${X},1740 ${X - 320},1700Z" fill="#2f5a46" ${OUT}/>${Array.from({ length: 8 }, (_, k) => `<path d="M${X - 300},${780 + k * 120}Q${X},${750 + k * 120} ${X + 300},${780 + k * 120}" stroke="#d89aa8" stroke-width="10" fill="none" opacity=".6"/>`).join("")}`;
    // the pot (from EP.1) beside her, and the rag by the pillow, smeared with green slime
    s += `<g transform="translate(${X + 400},900) scale(1.4)"><ellipse cx="0" cy="0" rx="110" ry="110" fill="#9aa4a8" ${OUT}/><ellipse cx="0" cy="0" rx="86" ry="86" fill="#b8c0c4" ${OUT3}/><path d="M-120,0h-30M120,0h30" stroke="${INK}" stroke-width="12" stroke-linecap="round"/></g>
      <g id="${id}-rag" transform="translate(${X - 330},560) rotate(-14)"><path d="M-90,-60Q-20,-90 80,-50Q110,20 70,70Q-10,100 -90,60Q-120,0 -90,-60Z" fill="#e8e2d0" ${OUT}/>
        <path d="M-60,-20Q-10,-40 40,-10Q60,20 20,40Q-30,50 -50,20Z" fill="#7dff6a" opacity=".85"/><path d="M-20,30q-6,40 6,70" stroke="#7dff6a" stroke-width="10" fill="none" stroke-linecap="round"/></g>`;
    put(L.set, s);
    put(L.glow, `<g id="${id}-eyes" opacity="0"><circle cx="${X - 38}" cy="608" r="40" fill="url(#ksGlow)"/><circle cx="${X + 38}" cy="608" r="40" fill="url(#ksGlow)"/><ellipse cx="${X - 38}" cy="608" rx="14" ry="10" fill="#bfff96"/><ellipse cx="${X + 38}" cy="608" rx="14" ry="10" fill="#bfff96"/></g>
      <circle cx="${X - 330}" cy="560" r="160" fill="url(#ksGlow)" opacity=".5"/><circle cx="${X + 300}" cy="-200" r="900" fill="url(#ksLamp)" opacity=".35"/>`);
  }

  // looping motion: the ghost bobs and drips, hair sways, orbs float, the fan turns, the tube light buzzes, sparks spit
  function life(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".kbob").forEach((el, i) => tl.fromTo(el, { y: -10 }, { y: 16, duration: 1.4 + (i % 3) * 0.3, repeat: Math.ceil(dur / 1.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".khair").forEach((el, i) => tl.fromTo(el, { rotation: -3 }, { rotation: 4, svgOrigin: "0 -60", duration: 1.2 + (i % 3) * 0.3, repeat: Math.ceil(dur / 1.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.07));
    q(".kdrip").forEach((el, i) => tl.fromTo(el, { y: 0, opacity: 0.95 }, { y: 120, opacity: 0, duration: 0.9 + (i % 3) * 0.2, repeat: Math.ceil(dur / 0.9), ease: "power2.in", immediateRender: false }, t0 + i * 0.23));
    q(".keye").forEach((el, i) => tl.fromTo(el, { opacity: 1 }, { opacity: 0.55, duration: 0.45 + (i % 2) * 0.1, repeat: Math.ceil(dur / 0.45), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".kheart").forEach((el) => { for (let t = 0; t < dur; t += 0.9) { tl.to(el, { scale: 1.12, svgOrigin: "0 190", duration: 0.08 }, t0 + t); tl.to(el, { scale: 1, svgOrigin: "0 190", duration: 0.25 }, t0 + t + 0.08); } });
    q(".kglow").forEach((el, i) => tl.fromTo(el, { opacity: 0.75 }, { opacity: 1, duration: 0.6 + (i % 3) * 0.2, repeat: Math.ceil(dur / 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".korb").forEach((el, i) => tl.fromTo(el, { y: -14, x: -8 }, { y: 14, x: 8, duration: 1.6 + (i % 3) * 0.4, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.3));
    q(".kfan").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360 * dur * 2, svgOrigin: "0 -620", duration: dur, ease: "none", immediateRender: false }, t0));
    q(".ktube").forEach((el) => { for (let t = 0.3; t < dur; t += 1.7) { tl.set(el, { opacity: 0.4 }, t0 + t); tl.set(el, { opacity: 1 }, t0 + t + 0.06); } });
    q(".rip").forEach((el, i) => tl.fromTo(el, { x: -10, opacity: 0.2 }, { x: 12, opacity: 0.55, duration: 1 + (i % 4) * 0.25, repeat: Math.ceil(dur / 1), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 5) * 0.12));
    q(".slt").forEach((el, i) => tl.fromTo(el, { opacity: 0.4 }, { opacity: 0.9, duration: 0.5 + (i % 5) * 0.12, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "none", immediateRender: false }, t0 + (i % 7) * 0.07));
    q(".lamp").forEach((el, i) => tl.fromTo(el, { opacity: 0.85 }, { opacity: 1, duration: 0.13 + (i % 3) * 0.05, repeat: Math.ceil(dur / 0.13), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".drip").forEach((el, i) => tl.fromTo(el, { y: 0, opacity: 0.9 }, { y: 140, opacity: 0, duration: 0.9 + (i % 3) * 0.2, repeat: Math.ceil(dur / 0.9), ease: "power2.in", immediateRender: false }, t0 + (i % 5) * 0.17));
    q(".kcloud").forEach((el) => tl.fromTo(el, { x: 0 }, { x: 60, duration: dur, ease: "none", immediateRender: false }, t0));
  }
  // the broken line spitting sparks at random (seeded) between t0 and t0 + dur
  function arcs(tl, sel, gsel, t0, dur, seed = 5) {
    const r = mk(seed);
    for (let t = 0; t < dur; t += 0.12 + r() * 0.5) { const k = 0.4 + r() * 0.6; tl.set([sel, gsel], { opacity: k }, t0 + t); tl.set([sel, gsel], { opacity: 0 }, t0 + t + 0.05 + r() * 0.06); }
  }

  // ---------------- cast ----------------
  Object.assign(Rig.CAST, {
    fon: { // ฝน: 17, oversized mustard hoodie, black shorts over leggings, long hair loose with a clip, phone on a strap round her neck
      skin: "#e2ad85", skinS: "#c28c63", top: "#e8a33a", topS: "#c4842a", sleeve: "#e8a33a", sleeveS: "#c4842a", forearm: "#e8a33a", forearmS: "#c4842a",
      pants: "#24262a", pantsS: "#17181b", shoe: "#d8dcd8", belt: "#24262a",
      torsoExtra: `<path d="M-36,-470Q0,-430 36,-470" stroke="#c4842a" stroke-width="6" fill="none"/><path d="M-10,-470v40M10,-470v40" stroke="#f4ecd8" stroke-width="4"/>
        <path d="M-30,-470L-6,-380L18,-470" stroke="#2a2a2a" stroke-width="4" fill="none"/><rect x="-24" y="-400" width="36" height="60" rx="6" fill="#1d1f22" ${OUT}/><rect x="-18" y="-394" width="24" height="44" rx="3" fill="#7fb3c9"/>`,
      hair: `<path d="M-50,-560Q-56,-616 0,-618Q56,-616 50,-560Q60,-500 56,-430Q40,-470 40,-540Q20,-588 0,-588Q-30,-588 -40,-540Q-40,-470 -56,-430Q-62,-500 -50,-560Z" fill="#1b1614" ${OUT}/><rect x="22" y="-596" width="26" height="10" rx="4" fill="#e04a6a"/>`,
      face: `<g fill="#e0907a" opacity=".55"><ellipse cx="-24" cy="-526" rx="7" ry="3.5"/><ellipse cx="30" cy="-526" rx="7" ry="3.5"/></g>`,
    },
    toey: { // เต้ย: 9, green football shirt with number 9, blue shorts, flip-flops, a little cowlick
      skin: "#d9a074", skinS: "#b98059", top: "#3faa6a", topS: "#2f8a54", sleeve: "#3faa6a", sleeveS: "#2f8a54", forearm: "#d9a074", forearmS: "#b98059",
      pants: "#3f6fb0", pantsS: "#2f5690", shoe: "#e04a3a", belt: "#3f6fb0",
      torsoExtra: `<text x="0" y="-372" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#f4ecd8">9</text>`,
      hair: `<path d="M-48,-552Q-50,-610 0,-612Q50,-610 48,-554Q42,-578 0,-582Q-42,-578 -48,-552Z" fill="#221a16" ${OUT}/><path d="M6,-612q14,-26 -2,-40" stroke="#221a16" stroke-width="10" fill="none" stroke-linecap="round"/>`,
      face: `<g fill="#e0907a" opacity=".5"><ellipse cx="-24" cy="-526" rx="7" ry="3.5"/><ellipse cx="30" cy="-526" rx="7" ry="3.5"/></g>`,
    },
    piak: { // ลุงเปี๊ยก: 55, the village electrician — grey work shirt with a pocket of screwdrivers, tool belt, cap, rubber boots, moustache
      skin: "#b67d55", skinS: "#94603e", top: "#7c8a8e", topS: "#626f73", sleeve: "#7c8a8e", sleeveS: "#626f73", forearm: "#b67d55", forearmS: "#94603e",
      pants: "#3a3530", pantsS: "#2a2622", shoe: "#1d1d1d", belt: "#6a4a2a",
      torsoExtra: `<rect x="10" y="-450" width="44" height="50" fill="#626f73" ${OUT}/><path d="M18,-450v-26M30,-450v-34M42,-450v-22" stroke="#e04a3a" stroke-width="6"/>
        <rect x="-62" y="-318" width="124" height="34" fill="#6a4a2a" ${OUT}/><rect x="-50" y="-300" width="30" height="50" rx="4" fill="#8a6a4a" ${OUT}/><path d="M24,-290v50" stroke="#f2c94a" stroke-width="10"/>`,
      hair: `<path d="M-56,-560Q-50,-630 0,-632Q54,-630 58,-560Z" fill="#2f4a6a" ${OUT}/><path d="M-10,-574H96Q80,-552 30,-554Z" fill="#2f4a6a" ${OUT}/><path d="M-46,-560q-5,14 2,26M46,-560q5,14 -2,26" stroke="#8a8278" stroke-width="8" fill="none" stroke-linecap="round"/>`,
      face: `<path d="M-22,-510Q4,-498 30,-510Q22,-494 4,-494Q-14,-494 -22,-510Z" fill="#3a3530"/><path d="M-30,-560q8,-3 14,0M14,-560q8,-3 14,0" stroke="#5a4a32" stroke-width="3" fill="none"/>`,
    },
    chaem: { // ป้าแช่ม: 60, the kind neighbour — pale (too pale), faded pink blouse, dark green sarong, hair in a tight bun, a cloth over her shoulder
      skin: "#e6d2bc", skinS: "#c9b29a", top: "#d89aa8", topS: "#b97f8c", sleeve: "#d89aa8", sleeveS: "#b97f8c", forearm: "#e6d2bc", forearmS: "#c9b29a",
      pants: "#2f5a46", pantsS: "#234638", shoe: "#3a2a20", belt: "#2f5a46",
      torsoExtra: `<path d="M-54,-470L40,-300" stroke="#efe6d6" stroke-width="20"/><path d="M-30,-470Q0,-440 30,-470" stroke="#b97f8c" stroke-width="5" fill="none"/>`,
      hair: `<circle cx="0" cy="-618" r="26" fill="#3a3330" ${OUT}/><path d="M-48,-546Q-52,-610 0,-612Q50,-610 48,-548Q40,-582 0,-586Q-38,-582 -48,-546Z" fill="#3a3330" ${OUT}/>`,
      face: `<path d="M-30,-560q8,-3 14,0M14,-560q8,-3 14,0" stroke="#7a6a5a" stroke-width="2.5" fill="none"/><path d="M-26,-508q4,4 0,8M30,-508q-4,4 0,8" stroke="#c9b29a" stroke-width="2" fill="none"/>`,
    },
  });

  // ---------------- the rule card skin (ลุงเปี๊ยก's rules on a steel switch-box with a hazard stripe) + card icons ----------------
  if (typeof document !== "undefined" && !document.getElementById("ks-css")) document.head.insertAdjacentHTML("beforeend", `<style id="ks-css">
    .krule.elec { background: linear-gradient(180deg, #3a4044, #24292c); border: 4px solid #f2c94a; box-shadow: 0 0 0 10px rgba(20,22,24,.92), 0 0 0 13px #1d1d1d, 0 26px 60px rgba(0,0,0,.65); padding-top: 50px; }
    .krule.elec::before { inset: 0 0 auto 0; height: 26px; background: repeating-linear-gradient(-45deg, #f2c94a 0 26px, #1d1d1d 26px 52px); }
    .krule.elec .cn { border: 0; width: 24px; height: 24px; border-radius: 50%; background: radial-gradient(circle at 40% 35%, #e8ece8, #7a7e7c); }
    .krule.elec .cn::after { width: 16px; height: 4px; border-radius: 2px; background: #4a4e4c; left: 4px; top: 10px; }
    .krule.elec .cn.tl, .krule.elec .cn.tr { top: 36px; }
    .krule.elec .kr-h span { background: #f2c94a; color: #1d1d1d; border: 3px solid #1d1d1d; }
    .krule.elec .kr-i { background: radial-gradient(circle at 40% 35%, #fffbe0, #f2c94a); border-color: #1d1d1d; }
    .krule.elec .kr-t strong { color: #f2c94a; }
    .krule.elec .kr-t u::after { background: #f2c94a; box-shadow: 0 0 14px #f2c94a; }
    .krule.elec .kr-r + .kr-r { border-top: 2px dashed rgba(242,201,74,.35); }</style>`);
  if (window.GameUI) {
    const K = INK, O = `stroke="${K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
    const NO = `<g class="a-pulse"><circle cx="60" cy="60" r="50" fill="none" stroke="#e0362c" stroke-width="9"/><path d="M25,25L95,95" stroke="#e0362c" stroke-width="9" stroke-linecap="round"/></g>`;
    const BOLT = (x, y, k = 1) => `<path d="M${x + 4 * k},${y}l${-12 * k},${22 * k}h${12 * k}l${-8 * k},${20 * k}" stroke="#f2c94a" stroke-width="${5 * k}" fill="none" stroke-linejoin="round"/>`;
    const WATER = `<path d="M8,84q13,-8 26,0t26,0t26,0t26,0V112H8Z" fill="#4f8fbf" ${O}/>`;
    Object.assign(GameUI.ILL, {
      // the main switch, its lever coming down
      cutmain: `<rect x="34" y="14" width="52" height="92" rx="8" fill="#efe9dc" ${O}/><circle cx="60" cy="74" r="5" fill="${K}"/><g class="a-bob"><path d="M60,74L60,30" stroke="#c9873a" stroke-width="10" stroke-linecap="round"/><rect x="44" y="20" width="32" height="16" rx="6" fill="#1d1d1d"/></g>
        <path d="M96,40v34M88,64l8,12l8,-12" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
      // water rising to an outlet
      wetplug: `${WATER}<rect x="36" y="44" width="48" height="34" rx="6" fill="#f4f0e6" ${O}/><path d="M50,54v12M70,54v12" stroke="${K}" stroke-width="5"/><g class="a-bob"><path d="M14,96V70M8,78l6,-10l6,10" stroke="#4fb0e0" stroke-width="5" fill="none"/></g>`,
      // dry feet on a dry step
      drystand: `<rect x="20" y="78" width="80" height="16" rx="4" fill="#c9a86a" ${O}/><path d="M42,78V50M74,78V50" stroke="#24262a" stroke-width="14" stroke-linecap="round"/><ellipse cx="38" cy="78" rx="12" ry="6" fill="#e2ad85" ${O}/><ellipse cx="78" cy="78" rx="12" ry="6" fill="#e2ad85" ${O}/>
        <g class="a-pulse"><path d="M88,22l6,6l12,-14" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round"/></g>`,
      // a wet hand toward a fan — crossed out
      nowettouch: `<path d="M20,98V50Q20,40 30,40H50" stroke="#e2ad85" stroke-width="18" stroke-linecap="round" fill="none"/>${[0, 1, 2].map((k) => `<path d="M${26 + k * 10},${66 + k * 8}c-4,7 -4,11 0,13c4,-2 4,-6 0,-13z" fill="#4fb0e0"/>`).join("")}
        <circle cx="80" cy="46" r="22" fill="none" stroke="#7fb3c9" stroke-width="6"/><path d="M80,68V100" stroke="#9aa4a8" stroke-width="6"/>${NO}`,
      // someone wading toward a pole in the water — crossed out
      nowade: `${WATER}<path d="M92,18V96" stroke="#8a8e8c" stroke-width="10"/>${BOLT(84, 30)}<circle cx="40" cy="48" r="10" fill="#e2ad85" ${O}/><path d="M40,58V84M40,66l14,8" stroke="${K}" stroke-width="8" stroke-linecap="round"/>${NO}`,
      // a broken line down in the water, keep away
      awayline: `${WATER}<path d="M20,14L60,40Q80,60 70,86" stroke="#1d1d1d" stroke-width="6" fill="none"/><g class="a-pulse">${BOLT(64, 70, 0.8)}</g>
        <g class="a-wave" data-i="0"><path d="M98,48H76M84,40l-8,8l8,8" stroke="#3fb86a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
      // water up to the switch box: don't wade in, call the electrician
      panelwater: `${WATER.replace("M8,84", "M8,64").replace("V112H8Z", "V112H8Z")}<rect x="40" y="18" width="40" height="62" rx="6" fill="#efe9dc" ${O}/><path d="M60,58V30" stroke="#c9873a" stroke-width="7" stroke-linecap="round"/>${NO}`,
      // a broken line down in the water, the water around it charged (bolts in the ripples)
      livewater: `${WATER}<path d="M24,10L54,36Q66,52 60,80" stroke="#1d1d1d" stroke-width="6" fill="none"/><g class="a-pulse"><ellipse cx="60" cy="92" rx="26" ry="7" fill="none" stroke="#f2c94a" stroke-width="4"/><ellipse cx="60" cy="96" rx="46" ry="12" fill="none" stroke="#f2c94a" stroke-width="3" opacity=".6"/></g>${BOLT(30, 88, 0.6)}${BOLT(92, 88, 0.6)}`,
      // a fallen line with a warning sign: always treat it as live
      assumelive: `<path d="M14,16L54,44Q70,62 58,98" stroke="#1d1d1d" stroke-width="7" fill="none"/><g class="a-pulse"><path d="M80,30L108,82H52Z" fill="#f2c94a" ${O}/><path d="M80,46v18" stroke="${K}" stroke-width="7" stroke-linecap="round"/><circle cx="80" cy="74" r="4" fill="${K}"/></g>${BOLT(62, 92, 0.7)}`,
      // a hand reaching for someone being shocked — crossed out
      notouch: `<circle cx="78" cy="30" r="12" fill="#e2ad85" ${O}/><path d="M78,42V74M78,52l-14,-10M78,52l14,-12M78,74l-8,22M78,74l8,22" stroke="${K}" stroke-width="7" stroke-linecap="round"/>${BOLT(96, 50, 0.7)}
        <path d="M8,72H46" stroke="#e2ad85" stroke-width="16" stroke-linecap="round"/>${NO}`,
      // a dry wooden pole, held from a dry step
      drystick: `<rect x="10" y="88" width="44" height="14" rx="4" fill="#c9a86a" ${O}/><path d="M30,88V60" stroke="#24262a" stroke-width="12" stroke-linecap="round"/><g class="a-bob"><path d="M34,70L106,24" stroke="#6a4a2e" stroke-width="11" stroke-linecap="round"/><path d="M34,70L106,24" stroke="#c9a86a" stroke-width="5" stroke-linecap="round"/></g>`,
      // phone 1669
      call1669: `<rect x="34" y="12" width="52" height="96" rx="10" fill="#1d1f22" ${O}/><rect x="40" y="22" width="40" height="66" rx="4" fill="#e8f0f2"/><text x="60" y="64" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="#e0362c">1669</text><g class="a-wave" data-i="1"><path d="M96,30q10,10 0,20M104,24q16,16 0,32" stroke="#e0362c" stroke-width="5" fill="none" stroke-linecap="round"/></g>`,
      // two hands pressing the middle of a chest
      cpr: `<ellipse cx="60" cy="78" rx="44" ry="30" fill="#3faa6a" ${O}/><g class="a-bob"><ellipse cx="60" cy="58" rx="20" ry="15" fill="#e2ad85" ${O}/><path d="M60,44V14" stroke="#e8a33a" stroke-width="18" stroke-linecap="round"/></g><path d="M90,30v28M84,50l6,10l6,-10" stroke="#e0362c" stroke-width="5" fill="none" stroke-linecap="round"/>`,
      // the lever up crossed out; an electrician checks first
      callelec: `<rect x="14" y="16" width="44" height="76" rx="6" fill="#efe9dc" ${O}/><path d="M36,62V30" stroke="#c9873a" stroke-width="8" stroke-linecap="round"/>${NO.replace(/60/g, "36").replace("r=\"50\"", "r=\"34\"").replace("M25,25L95,95", "M12,12L60,60")}
        <circle cx="88" cy="40" r="14" fill="#b67d55" ${O}/><path d="M74,34h28" stroke="#2f4a6a" stroke-width="10"/><path d="M88,54V96M88,66l-16,10M88,66l14,-6" stroke="#7c8a8e" stroke-width="10" stroke-linecap="round"/><g class="a-bob"><path d="M104,58l10,-16" stroke="#e04a3a" stroke-width="6" stroke-linecap="round"/></g>`,
      // an appliance drying in the sun before it is used again
      drydevice: `<g class="a-pulse"><circle cx="92" cy="26" r="14" fill="#f2c94a" ${O}/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${92 + Math.cos(k * 1.05) * 20},${26 + Math.sin(k * 1.05) * 20}l${Math.cos(k * 1.05) * 8},${Math.sin(k * 1.05) * 8}" stroke="#f2c94a" stroke-width="4"/>`).join("")}</g>
        <rect x="20" y="40" width="54" height="66" rx="8" fill="#d8e4e8" ${O}/><path d="M20,64h54" stroke="${K}" stroke-width="3"/>${[0, 1].map((k) => `<path d="M${36 + k * 22},${34 - k * 4}q-6,-8 0,-16" stroke="#9fb0c8" stroke-width="4" fill="none" opacity=".8"/>`).join("")}`,
      // sparks or a burning smell when the power comes back: switch it off at once
      smelloff: `<g class="a-pulse"><path d="M30,20l6,14l14,-8l-6,14l14,4l-14,6l6,14l-14,-8l-6,14l-4,-14l-14,6l8,-12l-14,-6l14,-4l-8,-12l14,6z" fill="#f2c94a" ${O}/></g>
        <path d="M70,24q-10,10 0,20t0,20" stroke="#8a8a8a" stroke-width="5" fill="none" opacity=".8"/><rect x="66" y="66" width="40" height="44" rx="6" fill="#efe9dc" ${O}/><g class="a-bob"><path d="M86,78V102" stroke="#c9873a" stroke-width="7" stroke-linecap="round"/></g><path d="M74,100l12,10l12,-10" stroke="#3fb86a" stroke-width="4" fill="none"/>`,
      // call the power company / 1669 on the phone
      callpea: `<rect x="34" y="12" width="52" height="96" rx="10" fill="#1d1f22" ${O}/><rect x="40" y="22" width="40" height="66" rx="4" fill="#7fb3c9"/>${BOLT(62, 32, 1.1)}<g class="a-wave" data-i="1"><path d="M96,30q10,10 0,20M104,24q16,16 0,32" stroke="#e0362c" stroke-width="5" fill="none" stroke-linecap="round"/></g>`,
    });
  }

  // ---------------- koi-style knowledge diagram: the house in cross-section (like the koi flash-flood mountain) ----------------
  // flat teal ground, the room cut open: the outlet low on the wall (#id-plug), the cut-out high by the stairs (#id-lever, pivot at
  // its hinge), a stick figure on the stairs; the flood (#id-water, move it up with y) with sparks off the outlet (#id-zap);
  // #id-ok (green tick by the switch), #id-wet (a dripping hand with a red cross); small labels like the koi diagrams
  function floodSection(L, o = {}) {
    const id = o.id || "fs", F = 1360, T = (x, y, t, c = "#f4ecd8", sz = 34) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${sz}" fill="${c}">${t}</text>`;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#1f3338"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1100 + k * 100},-800V2800M-1200,${-700 + k * 100}H2300" stroke="#26404a" stroke-width="2"/>`).join("")}`);
    let s = `<path d="M120,${F}V720L540,420L960,720V${F}Z" fill="#e9e1cc" ${OUT}/><path d="M160,${F}V740L540,470L920,740V${F}Z" fill="#d8ceb4"/>
      <path d="M80,730L540,380L1000,730" fill="none" stroke="#7a4a2e" stroke-width="22" stroke-linecap="round"/>
      <rect x="60" y="${F}" width="960" height="40" fill="#8a7a60" ${OUT}/>${[0, 1, 2, 3, 4].map((k) => `<rect x="${100 + k * 200}" y="${F + 40}" width="34" height="300" fill="#6a5a44" ${OUT3}/>`).join("")}
      <path d="M-600,${F + 260}H1700" stroke="#5a4a36" stroke-width="10"/>`;
    // the stairs up to the sleeping floor on the right, the sleeping floor
    s += `<path d="M560,940H920" stroke="#7a6a50" stroke-width="18"/>${[0, 1, 2, 3, 4, 5].map((k) => `<rect x="${600 + k * 54}" y="${F - 70 - k * 70}" width="${330 - k * 54}" height="18" fill="#9a8a6a" ${OUT3}/>`).join("")}`;
    // the outlet, low on the left wall
    s += `<g id="${id}-plug"><rect x="200" y="${F - 170}" width="80" height="110" rx="10" fill="#f4f0e6" ${OUT3}/><path d="M228,${F - 140}v26M252,${F - 140}v26" stroke="${INK}" stroke-width="7"/></g>${T(240, F - 196, "ปลั๊ก")}`;
    // the cut-out by the stairs, its lever
    s += `<g><rect x="640" y="760" width="120" height="170" rx="10" fill="#efe9dc" ${OUT}/><rect x="676" y="790" width="48" height="110" rx="6" fill="#b8b0a0" ${OUT3}/>
        <g id="${id}-lever" transform="rotate(0 700 845)"><rect x="692" y="800" width="16" height="48" rx="4" fill="#c9873a" ${OUT3}/><circle cx="700" cy="800" r="12" fill="#2e2a26"/></g>
        <path d="M700,930V${F}" stroke="#2a2a2a" stroke-width="6"/><path d="M290,${F - 120}H600V${F}" stroke="#2a2a2a" stroke-width="5" fill="none" opacity=".6"/></g>${T(700, 742, "คัตเอาต์")}`;
    // the stick figure on the stairs
    s += `<g transform="translate(830,${F - 345})"><circle cx="0" cy="-118" r="26" fill="#e9bc93" ${OUT3}/><path d="M0,-92V-24M0,-70l-32,26M0,-70l40,-28M0,-24l-22,48M0,-24l18,48" stroke="${INK}" stroke-width="12" stroke-linecap="round" fill="none"/></g>`;
    put(L.set, s);
    // the water (rises with y), sparks off the outlet into it
    put(L.act, `<g id="${id}-water" transform="translate(0,0)"><path d="M-600,${F + 120}q60,-16 120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0V${F + 900}H-600Z" fill="#3f7fae" opacity=".72"/>
        <path d="M-600,${F + 120}q60,-16 120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0t120,0" stroke="#bfe6ff" stroke-width="5" fill="none"/></g>
      <g id="${id}-zap" opacity="0">${[[240, F - 60, 140, 120], [240, F - 60, 20, 160], [240, F - 60, 340, 110]].map(([x, y, x2, y2]) => `<path d="M${x},${y}L${(x + x2) / 2 + 20},${y + y2 * 0.4}L${(x + x2) / 2 - 16},${y + y2 * 0.6}L${x2},${y + y2}" stroke="#ffe24a" stroke-width="9" fill="none" stroke-linejoin="round"/>`).join("")}</g>
      <g id="${id}-ok" opacity="0" transform="translate(830,700)"><circle r="54" fill="#3fb86a" ${OUT}/><path d="M-24,0l16,18l30,-36" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <g id="${id}-wet" opacity="0" transform="translate(520,860)"><path d="M-40,40V-30q0,-14 14,-14t14,14V-60q0,-14 14,-14t14,14V-30q0,-14 14,-14t14,14V40q0,40 -40,40h-10q-30,0 -44,-40Z" fill="#e9bc93" ${OUT}/>
        ${[[-30, 70], [0, 92], [26, 70]].map(([x, y]) => `<path d="M${x},${y}q-8,14 0,20q8,-6 0,-20Z" fill="#4fb0e0" ${OUT3}/>`).join("")}
        <circle cx="0" cy="10" r="96" fill="none" stroke="#e0362c" stroke-width="12"/><path d="M-68,-58L68,78" stroke="#e0362c" stroke-width="12" stroke-linecap="round"/></g>`);
    put(L.glow, `<circle id="${id}-zapg" cx="240" cy="${F - 60}" r="160" fill="url(#ksArc)" opacity="0"/>`);
  }
  // a flip-flop floating on the water (เต้ย's, in EP.1)
  const slipper = (x, y, s = 1, id = "") => `<g ${id ? `id="${id}"` : ""} transform="translate(${x},${y}) scale(${s})"><ellipse rx="54" ry="20" fill="#3fa0d8" ${OUT3}/><path d="M-10,-6q20,-24 40,0" stroke="#f4f0e6" stroke-width="7" fill="none"/></g>`;

  Object.assign(Sets, { floodSection, floodVillage, houseIn, porchFlood, meterCard, comicLegend, switchClose, poleSign, cprFloor, latchClose, outletClose, chaemTop });
  window.Krasue = { ghost, lurk, lensFace, slipper, glow, orb, orbGlow, boat, boatFront, life, arcs, KBL, KBL2, KRIM, KEYE };
})();
