// Sets and props for "วันที่ 100": a rural primary school turned camp, a hundred days after the plague ("ห่าลง").
// The yard with its concrete fence, sliding iron gate, wooden classroom block, flagpole and the tall water tank;
// the classroom with the big green blackboard; the abandoned fresh market; the dirt road through the paddies;
// close-ups of a bulging can, the gate bolt, the tank gauge and the old radio; น้องปั้น's crayon drawing;
// a top-down map of the compound. Same layer contract as sets.js / zom.js (sky far mid set act fg + glow/light).
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const G = 1500;

  Sets.DEFS += `
    <linearGradient id="fDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb6dc"/><stop offset=".7" stop-color="#d9e6ea"/><stop offset="1" stop-color="#f1e9d6"/></linearGradient>
    <linearGradient id="fNoon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc3ea"/><stop offset=".75" stop-color="#eef2ea"/><stop offset="1" stop-color="#fff3d6"/></linearGradient>
    <linearGradient id="fDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2f52"/><stop offset=".5" stop-color="#b9566a"/><stop offset=".85" stop-color="#f2a05a"/><stop offset="1" stop-color="#ffd37a"/></linearGradient>
    <linearGradient id="fNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070f"/><stop offset="1" stop-color="#162035"/></linearGradient>
    <linearGradient id="fMorn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9d4e6"/><stop offset=".8" stop-color="#f6e7cf"/><stop offset="1" stop-color="#ffdca8"/></linearGradient>
    <linearGradient id="fPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fae5a"/><stop offset="1" stop-color="#6d8f3e"/></linearGradient>
    <linearGradient id="fPaddyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a3e"/><stop offset="1" stop-color="#2f3328"/></linearGradient>
    <linearGradient id="fDirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8a06a"/><stop offset="1" stop-color="#a77f4e"/></linearGradient>
    <linearGradient id="fConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9d4c8"/><stop offset="1" stop-color="#b3ada0"/></linearGradient>
    <linearGradient id="fTin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d9299"/><stop offset=".5" stop-color="#b9bec4"/><stop offset="1" stop-color="#7f858c"/></linearGradient>
    <linearGradient id="fBoard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f5a46"/><stop offset="1" stop-color="#1f3f31"/></linearGradient>
    <linearGradient id="fCan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d9299"/><stop offset=".35" stop-color="#e3e6e8"/><stop offset=".7" stop-color="#aeb3b8"/><stop offset="1" stop-color="#6f757b"/></linearGradient>
    <radialGradient id="fSun"><stop offset="0" stop-color="#fff2c0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd37a" stop-opacity=".5"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>
    <radialGradient id="fLamp"><stop offset="0" stop-color="#ffd58a" stop-opacity=".3"/><stop offset=".4" stop-color="#ffb35c" stop-opacity=".07"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient>
    <radialGradient id="fDial"><stop offset="0" stop-color="#ffd27a" stop-opacity=".9"/><stop offset=".5" stop-color="#ff9a3c" stop-opacity=".3"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="fRing"><stop offset=".6" stop-color="#ff5a3a" stop-opacity="0"/><stop offset=".9" stop-color="#ff5a3a" stop-opacity=".5"/><stop offset="1" stop-color="#ff5a3a" stop-opacity="0"/></radialGradient>
    <pattern id="fPaper" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#f3ecd9"/><path d="M0,59.5H60" stroke="#cdbfa3" stroke-width="1.5"/></pattern>
    <pattern id="fGrid" width="48" height="48" patternUnits="userSpaceOnUse"><rect width="48" height="48" fill="#f7f1e2"/><path d="M0,47.5H48M47.5,0V48" stroke="#d8cbb2" stroke-width="1.4"/></pattern>
    <pattern id="fMesh" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M0,13L13,0L26,13L13,26Z" fill="none" stroke="#9aa0a6" stroke-width="2.2"/></pattern>
    <filter id="fChalk" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.2"/></filter>
    <filter id="fCrayon" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".6" numOctaves="2" seed="9" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="4"/></filter>`;

  const SKY = { day: "fDay", noon: "fNoon", dusk: "fDusk", night: "fNight", morning: "fMorn" };
  const sky = (L, time) => put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#${SKY[time] || "fDay"})"/>`);
  const sunMoon = (L, time, x = 820, y = 420) => {
    if (time === "night") put(L.sky, `<circle cx="${x}" cy="${y - 80}" r="150" fill="url(#moonhalo)"/><circle cx="${x}" cy="${y - 80}" r="46" fill="#e9eef5"/><circle cx="${x - 16}" cy="${y - 92}" r="9" fill="#cfd6e0"/><circle cx="${x + 14}" cy="${y - 66}" r="6" fill="#cfd6e0"/>`);
    else if (time === "dusk") put(L.sky, `<circle cx="${x}" cy="${y + 520}" r="420" fill="url(#fSun)"/><circle cx="${x}" cy="${y + 520}" r="120" fill="#ffd37a"/>`);
    else put(L.sky, `<circle cx="${x}" cy="${y - 200}" r="380" fill="url(#fSun)"/><circle cx="${x}" cy="${y - 200}" r="64" fill="#fff2c0"/>`);
  };
  // ---------------- far ground: rice paddies to the horizon, a treeline, low hills with the radio mast ----------------
  function paddies(r, time, y0, o = {}) {
    const night = time === "night", dusk = time === "dusk";
    let s = `<rect x="-1200" y="${y0 - 10}" width="3500" height="1400" fill="url(#${night ? "fPaddyD" : "fPaddy"})"/>`;
    s += `<path d="M-1200,${y0 + 30}Q-600,${y0 - 60} 0,${y0 + 10}T1200,${y0 - 20}T2400,${y0 + 20}V${y0 + 120}H-1200Z" fill="${night ? "#1b2238" : dusk ? "#5c4a63" : "#6f9a6a"}"/>`;
    // hills + the radio mast on the far ridge (planted for the finale)
    s += `<path d="M-1200,${y0 - 40}L-700,${y0 - 160}L-300,${y0 - 90}L200,${y0 - 210}L700,${y0 - 120}L1150,${y0 - 240}L1600,${y0 - 110}L2300,${y0 - 170}V${y0 + 40}H-1200Z" fill="${night ? "#121a2c" : dusk ? "#4c3a5a" : "#7ea0b6"}" opacity=".9"/>`;
    s += `<path d="M1150,${y0 - 240}V${y0 - 420}M1138,${y0 - 400}h24M1142,${y0 - 350}h16M1146,${y0 - 300}h8" stroke="${night ? "#3a4660" : "#5c6f82"}" stroke-width="3"/><circle class="beacon" cx="1150" cy="${y0 - 424}" r="5" fill="#ff3b30" opacity=".8"/>`;
    // paddy dykes in perspective + a few stubborn trees
    for (let k = 0; k < 7; k++) { const y = y0 + 30 + k * k * 9; s += `<path d="M-1200,${y}H2400" stroke="${night ? "#2a3024" : "#5d7a35"}" stroke-width="${2 + k}" opacity=".5"/>`; }
    for (let k = 0; k < 9; k++) { const x = -900 + k * 380 + r() * 200, h = 90 + r() * 70; s += `<path d="M${x},${y0 + 24}v-${h * 0.5}" stroke="${night ? "#1a2030" : "#5a4a34"}" stroke-width="8"/><ellipse cx="${x}" cy="${y0 + 24 - h * 0.7}" rx="${h * 0.55}" ry="${h * 0.42}" fill="${night ? "#1c2636" : dusk ? "#4a4452" : "#4f7a44"}"/>`; }
    // power poles along the road, wires sagging, one leaning
    for (let k = 0; k < 4; k++) { const x = -600 + k * 700 + (k === 2 ? 60 : 0); s += `<g transform="translate(${x},${y0 + 20}) rotate(${k === 2 ? -7 : 0})"><path d="M0,0V-260M-40,-230H40M-30,-200H30" stroke="${night ? "#2a3040" : "#6b5a44"}" stroke-width="7"/></g>`; }
    s += `<path d="M-640,${y0 - 210}Q-290,${y0 - 150} 60,${y0 - 210}T760,${y0 - 210}T1460,${y0 - 210}" stroke="${night ? "#283040" : "#5a4a34"}" stroke-width="2.5" fill="none"/>`;
    return s;
  }

  // ---------------- the school yard (seen from inside): fence across the back with the sliding gate, classroom block left, water tank right ----------------
  // ids: #id-gate (slides open along x), #id-bolt, #id-tank, #id-level (float in the gauge tube), #id-flag, #id-lamp (night lantern)
  function schoolYard(L, o = {}) {
    const id = o.id || "sy", t = o.time || "day", night = t === "night", r = mk(o.seed || 41), FY = 1180; // fence foot line
    sky(L, t); sunMoon(L, t, o.sunX ?? 760, 420);
    put(L.far, paddies(r, t, 1040));
    // fence: concrete plinth, square posts, iron bars between; a sliding gate of vertical bars in the middle-right
    let s = `<rect x="-1200" y="${FY}" width="3500" height="60" fill="url(#fConc)" ${OUT}/>`;
    for (let x = -1320; x < 2300; x += 220) {
      if (x > 420 && x < 900) continue; // the gate opening
      const brk = o.breakAt === x;   // this section can fall inward (#id-fseg): rotated about its foot on the yard side
      if (brk) s += `<g id="${id}-fseg" transform="rotate(${o.fallen ? -82 : 0} ${x + 230} ${FY + 4})">`;
      s += `<rect x="${x}" y="${FY - 330}" width="40" height="340" fill="#cfc9bb" ${OUT}/><rect x="${x + 36}" y="${FY - 316}" width="186" height="30" fill="#5b6066" ${OUT}/><rect x="${x + 36}" y="${FY - 120}" width="186" height="26" fill="#5b6066" ${OUT}/>`;
      for (let b = 0; b < 6; b++) s += `<rect x="${x + 50 + b * 30}" y="${FY - 300}" width="12" height="190" fill="#3f454b"/>`;
      if (brk) s += `<path d="M${x + 60},${FY - 310}l-10,30l14,20M${x + 150},${FY - 120}l12,-24" stroke="#2e2a26" stroke-width="3" fill="none"/></g>`;
      if (brk && o.fallen) s += `<path d="M${x + 180},${FY + 30}q60,-20 120,10M${x + 200},${FY + 50}q50,-10 90,20" stroke="#5a4630" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    }
    // the short run between the gate's right post (x 940) and the next post (x 1100)
    s += `<rect x="936" y="${FY - 316}" width="168" height="30" fill="#5b6066" ${OUT}/><rect x="936" y="${FY - 120}" width="168" height="26" fill="#5b6066" ${OUT}/>`;
    for (let b = 0; b < 5; b++) s += `<rect x="${956 + b * 30}" y="${FY - 300}" width="12" height="190" fill="#3f454b"/>`;
    s += `<rect x="400" y="${FY - 400}" width="44" height="410" fill="#cfc9bb" ${OUT}/><rect x="896" y="${FY - 400}" width="44" height="410" fill="#cfc9bb" ${OUT}/><rect x="400" y="${FY - 420}" width="540" height="30" fill="#c8302a" ${OUT}/>`;
    s += `<text x="670" y="${FY - 435}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#f4ecd8" stroke="${INK}" stroke-width="5" paint-order="stroke">โรงเรียนบ้านหนองน้ำใส</text>`;
    // the gate: a frame of iron bars on a rail, slides to the right (+x) to open
    const gx = 444 + (o.gate || 0) * 440;
    s += `<g id="${id}-gate" transform="translate(${gx},0)"><rect x="0" y="${FY - 380}" width="452" height="380" fill="none" stroke="#3a3f45" stroke-width="18"/>`;
    for (let b = 0; b < 14; b++) s += `<rect x="${12 + b * 32}" y="${FY - 372}" width="10" height="364" fill="#3f454b"/>`;
    s += `<rect x="0" y="${FY - 230}" width="452" height="18" fill="#3a3f45"/><g id="${id}-bolt"><rect x="-70" y="${FY - 210}" width="130" height="22" rx="8" fill="#8d9299" ${OUT}/><rect x="-78" y="${FY - 222}" width="30" height="46" rx="6" fill="#5b6066" ${OUT}/></g></g>`;
    s += `<rect x="400" y="${FY - 8}" width="540" height="12" fill="#3a3f45"/>`;
    // classroom block (left, behind a gravel apron): raised wooden building, tin roof, long veranda, shuttered windows
    s += `<g transform="translate(-620,${FY - 20})">
      <path d="M-40,0V-520H900V0Z" fill="#c9a06c" ${OUT}/>${Array.from({ length: 12 }, (_, k) => `<path d="M${30 + k * 72},-500V-30" stroke="#a5804f" stroke-width="3"/>`).join("")}
      <path d="M-90,-520L440,-680L990,-520Z" fill="url(#fTin)" ${OUT}/>${Array.from({ length: 11 }, (_, k) => `<path d="M${-40 + k * 96},-${520 + k * 0}L${440},-676" stroke="#6b7177" stroke-width="2" opacity=".6"/>`).join("")}
      <rect x="-40" y="-120" width="940" height="26" fill="#8a6a42" ${OUT}/>${[0, 180, 360, 540, 720].map((x) => `<rect x="${x + 20}" y="-96" width="18" height="96" fill="#7a5a3e"/>`).join("")}
      ${[60, 300, 540].map((x) => `<rect x="${x}" y="-440" width="150" height="190" fill="#1d2a2c" ${OUT}/><rect x="${x - 16}" y="-440" width="22" height="190" fill="#6f8f58" ${OUT}/><rect x="${x + 144}" y="-440" width="22" height="190" fill="#6f8f58" ${OUT}/>${Array.from({ length: 5 }, (_, j) => `<path d="M${x},-${420 - j * 40}H${x + 150}" stroke="#2f3d3f" stroke-width="3"/>`).join("")}`).join("")}
      <rect x="760" y="-440" width="110" height="320" fill="#4a3a2a" ${OUT}/><circle cx="848" cy="-280" r="7" fill="#c9b48a"/>
      <rect x="280" y="-600" width="320" height="56" rx="8" fill="#1f3f31" ${OUT}/><text x="440" y="-560" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#f4ecd8">โรงเรียนบ้านหนองน้ำใส</text>
      <path d="M-40,-520L-90,-560M900,-520L990,-560" stroke="${INK}" stroke-width="4"/></g>`;
    // flagpole with a faded, torn flag
    s += `<g id="${id}-flag" transform="translate(300,${FY + 60})"><rect x="-70" y="-30" width="140" height="30" fill="url(#fConc)" ${OUT}/><path d="M0,-30V-700" stroke="#9aa0a6" stroke-width="10"/><circle cy="-706" r="9" fill="#c9a55a" ${OUT}/>
      <path id="${id}-flagc" d="M6,-690h150l-10,30l8,30l-12,30h-136z" fill="#c8392b"/><path d="M6,-660h146v20h-146z" fill="#f4ecd8"/><path d="M6,-640h140v-14h-140z" fill="#2f4a8a"/></g>`;
    // water tank: a concrete tank on four legs with a ladder, a pipe down to a tap, and a clear gauge tube with marks (#id-level = the float)
    s += `<g id="${id}-tank" transform="translate(1260,${FY + 40})"><path d="M-130,0V-520M130,0V-520M-70,0V-520M70,0V-520" stroke="#8a857a" stroke-width="18"/><path d="M-130,-120L130,-260M130,-120L-130,-260M-130,-380L130,-500M130,-380L-130,-500" stroke="#8a857a" stroke-width="7"/>
      <rect x="-190" y="-540" width="380" height="40" fill="#9aa0a6" ${OUT}/><rect x="-170" y="-840" width="340" height="300" rx="20" fill="url(#fConc)" ${OUT}/><path d="M-170,-760H170M-170,-620H170" stroke="#9f9a8e" stroke-width="5"/>
      <ellipse cx="0" cy="-840" rx="170" ry="26" fill="#bdb7aa" ${OUT}/><rect x="-60" y="-868" width="120" height="30" rx="8" fill="#5b6066" ${OUT}/>
      <path d="M150,-860V-600M150,-860h44" stroke="#8a857a" stroke-width="10"/><rect x="170" y="-470" width="26" height="470" fill="#8a857a"/>${Array.from({ length: 9 }, (_, k) => `<path d="M146,${-500 + k * 56}h74" stroke="#8a857a" stroke-width="8"/>`).join("")}
      <rect x="-230" y="-820" width="26" height="270" rx="12" fill="#dfe9ee" ${OUT}/>${Array.from({ length: 6 }, (_, k) => `<path d="M-236,${-800 + k * 48}h-18" stroke="${INK}" stroke-width="3"/>`).join("")}
      <rect id="${id}-level" x="-226" y="${-820 + 270 * (1 - (o.level ?? 0.72))}" width="18" height="${270 * (o.level ?? 0.72)}" fill="#6fb3d6"/>
      <path d="M-100,-540V-40h-60" stroke="#8a857a" stroke-width="10" fill="none"/><rect x="-190" y="-60" width="40" height="30" rx="6" fill="#c9a55a" ${OUT}/><rect x="-250" y="0" width="160" height="14" fill="#8a857a"/><circle cx="-180" cy="-20" r="10" fill="#6fb3d6" opacity=".7"/></g>`;
    put(L.set, s);
    // the yard: packed dirt with grass, puddles and a drain, closer to us
    let g = `<rect x="-1200" y="${FY + 60}" width="3500" height="1300" fill="url(#fDirt)"/>`;
    for (let k = 0; k < 40; k++) { const x = -1100 + r() * 3400, y = FY + 90 + r() * 900; g += `<path d="M${f1(x)},${f1(y)}q6,-26 12,0q6,-22 12,0q6,-18 12,0" stroke="#6f8f3e" stroke-width="4" fill="none"/>`; }
    g += `<ellipse cx="500" cy="${FY + 400}" rx="220" ry="40" fill="#8f6f45" opacity=".35"/><ellipse cx="1500" cy="${FY + 600}" rx="300" ry="50" fill="#8f6f45" opacity=".35"/>`;
    put(L.set, g);
    if (o.hill) put(L.far, `<g id="${id}-hill"><path d="M1000,780Q1400,520 1800,620T2500,720V1100H1000Z" fill="${night ? "#121816" : "#5f7a4a"}"/><circle id="${id}-blinkg" cx="1640" cy="602" r="44" fill="url(#fLamp)" opacity="0"/><circle id="${id}-blink" cx="1640" cy="602" r="8" fill="#fff8d0" opacity="0"/></g>`);
    if (o.genX !== undefined) put(L.set, Sets.props.generator(`${id}-gen`, o.genX, FY + 320, 0.75, !!o.genOn));
    if (night || o.lamp) put(L.glow, `<g id="${id}-lamp"><circle cx="${o.lampX ?? -200}" cy="${FY - 260}" r="420" fill="url(#fLamp)" opacity=".7"/></g>`);
    if (night) put(L.glow, Array.from({ length: 26 }, (_, k) => `<circle class="mote" cx="${f1(-400 + r() * 1900)}" cy="${f1(700 + r() * 900)}" r="${f1(3 + r() * 4)}" fill="#d8f0a0" opacity="${(0.2 + r() * 0.5).toFixed(2)}"/>`).join(""));
    if (t === "noon") put(L.glow, `<rect x="-1200" y="900" width="3500" height="400" fill="url(#zHaze)" opacity=".8"/>`);
  }

  // ---------------- the classroom: green blackboard on the back wall, teacher's desk, little desks, shutters with light ----------------
  // ids: #id-board (chalk area 160..920 × 330..880), #id-desk, #id-cans (12 cans, #id-bulge = the swollen one), #id-radio, #id-lamp
  function classroom(L, o = {}) {
    const id = o.id || "cr", night = !!o.night, r = mk(o.seed || 17);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#1a1d1c"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${G + 800}" fill="${night ? "#5a5248" : "#e8dcc6"}"/><rect x="-1200" y="${G - 40}" width="3500" height="40" fill="#8a7a62"/>`;
    s += `<rect x="-1200" y="${G}" width="3500" height="1300" fill="#b98f62"/>${Array.from({ length: 24 }, (_, k) => `<path d="M${-1200 + k * 150},${G}V2800" stroke="#a37c52" stroke-width="4"/>`).join("")}`;
    // the blackboard with its chalk tray; faded old lessons in the corner
    s += `<rect x="130" y="300" width="820" height="610" rx="10" fill="#7a5a3e" ${OUT}/><rect x="160" y="330" width="760" height="550" fill="url(#fBoard)"/><rect x="130" y="910" width="820" height="26" fill="#5f442d" ${OUT}/>
      <rect x="700" y="915" width="60" height="12" rx="4" fill="#f4ecd8"/><rect x="780" y="915" width="44" height="12" rx="4" fill="#f4ecd8"/><rect x="200" y="912" width="120" height="18" rx="4" fill="#3a3330"/>
      <g id="${id}-board"></g>`;
    // Thai alphabet poster, a clock stopped at 6:40, the national flag strip, a shelf with the old radio
    s += `<rect x="-220" y="360" width="260" height="360" fill="#f4ecd8" ${OUT}/>${["ก ไก่", "ข ไข่", "ค ควาย", "ง งู"].map((t, k) => `<text x="-90" y="${430 + k * 80}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="${["#c8392b", "#2f4a8a", "#1f3f31", "#b07f2c"][k]}">${t}</text>`).join("")}
      <g transform="translate(1080,400)"><circle r="70" fill="#f4ecd8" ${OUT}/><circle r="60" fill="none" stroke="#2e2a26" stroke-width="2"/><path d="M0,0L0,-44M0,0L28,22" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle r="5" fill="${INK}"/></g>
      <rect x="1000" y="620" width="360" height="22" fill="#8a6a42" ${OUT}/><rect x="1000" y="642" width="12" height="90" fill="#8a6a42"/><rect x="1348" y="642" width="12" height="90" fill="#8a6a42"/>`;
    s += `<g id="${id}-radio" transform="translate(1180,620)"><rect x="-120" y="-150" width="240" height="150" rx="14" fill="#6b4a2e" ${OUT}/><rect x="-100" y="-130" width="110" height="70" rx="8" fill="#1a1512" ${OUT}/><rect x="-96" y="-126" width="102" height="62" rx="6" fill="#2a1a0a"/>
      <g id="${id}-dialw"><rect x="-96" y="-126" width="102" height="62" rx="6" fill="#ffb35c" opacity="0"/></g>${Array.from({ length: 7 }, (_, k) => `<path d="M${-86 + k * 15},-118v12" stroke="#c9a55a" stroke-width="2"/>`).join("")}<rect id="${id}-needle" x="-40" y="-124" width="3" height="58" fill="#ff3b30"/>
      <rect x="20" y="-130" width="90" height="110" rx="6" fill="#2a2420"/>${Array.from({ length: 6 }, (_, k) => `<path d="M${30 + k * 14},-125v100" stroke="#c9a55a" stroke-width="3" opacity=".5"/>`).join("")}
      <circle cx="-72" cy="-32" r="18" fill="#c9a55a" ${OUT}/><circle cx="-20" cy="-32" r="18" fill="#c9a55a" ${OUT}/><path d="M100,-150L190,-330" stroke="#9aa0a6" stroke-width="6"/></g>`;
    // window with wooden shutters on the left wall, slats of light
    s += `<rect x="-640" y="300" width="330" height="520" fill="${night ? "#0b1020" : "#dfeef5"}" ${OUT}/><rect x="-680" y="300" width="50" height="520" fill="#6f8f58" ${OUT}/><rect x="-320" y="300" width="50" height="520" fill="#6f8f58" ${OUT}/>${Array.from({ length: 9 }, (_, k) => `<path d="M-640,${340 + k * 54}h330" stroke="#5a7a44" stroke-width="7"/>`).join("")}`;
    // teacher's desk (right front) + chair, little desks in rows (left)
    s += `<g id="${id}-desk" transform="translate(760,${G})"><rect x="-260" y="-320" width="520" height="30" fill="#8a6a42" ${OUT}/><rect x="-240" y="-290" width="480" height="150" fill="#a07a4a" ${OUT}/><rect x="-200" y="-260" width="140" height="40" rx="4" fill="#6f4f2e"/><path d="M-230,-140V0M230,-140V0" stroke="#5f442d" stroke-width="14"/></g>`;
    for (let k = 0; k < 3; k++) s += `<g transform="translate(${-420 + k * 240},${G - k * 10})"><rect x="-90" y="-260" width="180" height="20" fill="#c9a06c" ${OUT}/><path d="M-70,-240V0M70,-240V0" stroke="#5b6066" stroke-width="10"/><rect x="-60" y="-140" width="120" height="14" fill="#5b6066"/></g>`;
    // children's drawings pinned by the door (น้องปั้น's gallery)
    s += `${[[1420, 340], [1560, 360], [1440, 540]].map(([x, y], k) => `<g transform="translate(${x},${y}) rotate(${-4 + k * 5})"><rect width="120" height="150" fill="#f4ecd8" ${OUT}/><circle cx="60" cy="8" r="7" fill="#c8392b"/><path d="M20,120l20,-40l20,30l20,-50l20,60" stroke="#${["c8392b", "2f4a8a", "6f8f3e"][k]}" stroke-width="5" fill="none"/><circle cx="90" cy="40" r="14" fill="none" stroke="#f2c55c" stroke-width="5"/></g>`).join("")}`;
    put(L.set, s);
    if (o.cans) { // the haul laid out on the desk: twelve cans, one of them swollen (#id-bulge), a candle lantern beside them
      let c = `<g id="${id}-cans">`;
      const n = typeof o.cans === "number" ? o.cans : 12, bi = o.bulge ?? (n > 8 ? 8 : n - 2);
      for (let k = 0; k < n; k++) { const x = 540 + (k % 6) * 72, y = G - 320 - Math.floor(k / 6) * 56, b = k === bi; c += `<g id="${b ? `${id}-bulge` : `${id}-c${k}`}" transform="translate(${x},${y})"><rect x="-26" y="-70" width="52" height="70" rx="6" fill="url(#fCan)" ${OUT}/><rect x="-26" y="-50" width="52" height="32" fill="${["#c8392b", "#2f6fb8", "#e8b830", "#4f8a55"][k % 4]}" opacity=".85"/><path d="M-26,-70q26,${b ? -26 : -8} 52,0" fill="#cfd3d6" ${OUT}/>${b ? `<path d="M-18,-78q18,-12 36,0" stroke="#8d9299" stroke-width="2" fill="none"/>` : ""}</g>`; }
      c += `</g>`;
      put(L.set, c);
    }
    if (o.gen) { const gx = o.genX ?? -300; put(L.set, Sets.props.generator(`${id}-gen`, gx, G, 0.8, !!o.genOn));
      put(L.act, `<g id="${id}-co" opacity="${o.genOn ? 1 : 0}">${[0, 1, 2, 3].map((k) => `<path class="cowisp" d="M${gx + 152 + k * 10},${G - 236}q-40,-70 10,-140t-10,-150" stroke="#d8dde2" stroke-width="${11 - k * 2}" fill="none" stroke-linecap="round" opacity=".16"/>`).join("")}</g>`); }
    if (o.fan) put(L.set, Fence.FAN(id, o.fanX ?? 540, o.fanY ?? 110));
    if (o.bulb) { put(L.set, Fence.BULB(id, o.bulbX ?? 760, 120)); put(L.glow, `<g id="${id}-bulb" opacity="${o.bulbOn ? 1 : 0}"><circle cx="${o.bulbX ?? 760}" cy="180" r="800" fill="url(#fLamp)"/></g>`); }
    if (night) { put(L.glow, `<circle id="${id}-lamp" cx="${o.lampX ?? 760}" cy="${o.lampY ?? 1120}" r="520" fill="url(#fLamp)" opacity=".85"/>`); put(L.set, `<g transform="translate(${o.lampX ?? 760},${G - 320})"><rect x="-24" y="-130" width="48" height="130" rx="8" fill="#3a3330" ${OUT}/><rect x="-14" y="-110" width="28" height="80" fill="#ffd58a"/><path d="M-30,-140h60l-8,-16h-44z" fill="#5b6066" ${OUT}/></g>`); }
    else { put(L.glow, [0, 1, 2, 3].map((k) => `<path d="M${-620 + k * 80},${340}l40,0L${-300 + k * 70},${G + 60}l-70,0Z" fill="url(#zRay)" opacity=".6"/>`).join("")); }
  }
  // chalk strokes on the board (set id of the classroom): text lines with a chalk filter, each wrapped for clip reveals
  function chalk(id, lines) {
    const el = document.getElementById(`${id}-board`);
    el.insertAdjacentHTML("beforeend", lines.map((ln, k) => `<g class="chalk" id="${id}-ch${k}" opacity="${ln.hide ? 0 : 1}"><text x="${ln.x}" y="${ln.y}" text-anchor="${ln.anchor || "start"}" font-family="Kanit" font-weight="${ln.w || 700}" font-size="${ln.size || 50}" fill="${ln.color || "#f4ecd8"}" opacity=".92" filter="url(#fChalk)" style="letter-spacing:2px">${ln.text}</text></g>`).join(""));
  }

  // ---------------- the abandoned fresh market: tin roof with holes, concrete stalls, metal shelves with the last cans, a vendor standing still in the gap ----------------
  // ids: #id-gap (where ha3 stands, x≈300), #id-cans (the cans on the near shelf), #id-fall (a can that drops)
  function market(L, o = {}) {
    const id = o.id || "mk", r = mk(o.seed || 53);
    sky(L, o.time || "day");
    put(L.far, paddies(r, o.time || "day", 980));
    // back: roof underside with holes, a long back wall of shuttered shophouses, hanging tarps
    let s = `<path d="M-1200,-800H2300V560H-1200Z" fill="#4a4f55"/>${Array.from({ length: 20 }, (_, k) => `<path d="M${-1200 + k * 180},-800V560" stroke="#3a3f45" stroke-width="6"/>`).join("")}`;
    s += `<path d="M-1200,560H2300V700H-1200Z" fill="#8d9299" ${OUT}/>`;
    s += `${[[-600, 90], [100, 140], [900, 70], [1500, 120]].map(([x, w]) => `<ellipse cx="${x}" cy="200" rx="${w}" ry="${w * 0.4}" fill="#f6ecd2"/>`).join("")}`;
    s += `<rect x="-1200" y="700" width="3500" height="${G - 700}" fill="#c8c0ae"/>${Array.from({ length: 12 }, (_, k) => `<rect x="${-1150 + k * 300}" y="760" width="220" height="${G - 760}" fill="#9aa0a6" ${OUT}/>${Array.from({ length: 9 }, (_, j) => `<path d="M${-1150 + k * 300},${790 + j * 60}h220" stroke="#7f858c" stroke-width="5"/>`).join("")}`).join("")}`;
    s += `${[[-400, "#2f6fb8"], [500, "#c8392b"], [1300, "#e8b830"]].map(([x, c]) => `<path d="M${x},700l-60,260l120,-40l40,220l80,-180l40,60V700Z" fill="${c}" opacity=".7"/>`).join("")}`;
    put(L.mid, s);
    // the floor and the stalls: concrete tables in two rows, overturned baskets, a puddle, the near shelf of cans
    let t = `<rect x="-1200" y="${G - 60}" width="3500" height="1400" fill="#8f8a7c"/><path d="M-1200,${G + 300}H2300" stroke="#6f6a5e" stroke-width="6"/><ellipse cx="900" cy="${G + 240}" rx="260" ry="40" fill="#5f6a70" opacity=".6"/>`;
    const stall = (x, y, w) => `<g transform="translate(${x},${y})"><rect x="0" y="-120" width="${w}" height="28" fill="#cfc9bb" ${OUT}/><rect x="10" y="-92" width="${w - 20}" height="92" fill="#b3ada0" ${OUT}/><path d="M${w * 0.5},-92V0" stroke="#9f9a8e" stroke-width="4"/></g>`;
    t += stall(-700, G - 80, 500) + stall(-100, G - 80, 300) + stall(1040, G - 80, 520);
    // a metal shelf unit left of centre with a gap beside it (the vendor stands in #id-gap), a few cans left on it
    t += `<g transform="translate(-560,${G})"><rect x="0" y="-620" width="420" height="620" fill="none" stroke="#5b6066" stroke-width="16"/>${[-520, -400, -280, -160].map((y) => `<rect x="0" y="${y}" width="420" height="14" fill="#5b6066"/>`).join("")}
      ${[[40, -530, "#c8392b"], [110, -530, "#2f6fb8"], [320, -410, "#e8b830"], [60, -290, "#4f8a55"], [240, -290, "#c8392b"], [300, -170, "#2f6fb8"]].map(([x, y, c]) => `<g><rect x="${x}" y="${y}" width="44" height="60" rx="5" fill="url(#fCan)" ${OUT}/><rect x="${x}" y="${y + 18}" width="44" height="26" fill="${c}" opacity=".85"/></g>`).join("")}</g>`;
    t += `<rect id="${id}-gap" x="-120" y="${G - 640}" width="240" height="640" fill="#2a2724"/>`;
    t += `<g transform="translate(240,${G})"><rect x="0" y="-620" width="420" height="620" fill="none" stroke="#5b6066" stroke-width="16"/>${[-520, -400, -280, -160].map((y) => `<rect x="0" y="${y}" width="420" height="14" fill="#5b6066"/>`).join("")}
      <g id="${id}-cans">${[[30, -290, "#c8392b"], [84, -290, "#e8b830"], [138, -290, "#2f6fb8"], [192, -290, "#4f8a55"], [246, -290, "#c8392b"], [300, -290, "#e8b830"], [40, -170, "#2f6fb8"], [100, -170, "#c8392b"], [160, -170, "#4f8a55"], [220, -170, "#e8b830"], [290, -170, "#2f6fb8"], [350, -170, "#c8392b"]].map(([x, y, c], k) => `<g id="${id}-sc${k}" transform="translate(${x},${y})"><rect x="0" y="0" width="44" height="60" rx="5" fill="url(#fCan)" ${OUT}/><rect x="0" y="18" width="44" height="26" fill="${c}" opacity=".85"/>${k === 8 ? `<path d="M0,0q22,-18 44,0" fill="#cfd3d6" ${OUT}/>` : ""}</g>`).join("")}</g></g>`;
    t += `<g id="${id}-fall" transform="translate(470,${G - 310})"><rect x="0" y="0" width="44" height="60" rx="5" fill="url(#fCan)" ${OUT}/><rect x="0" y="18" width="44" height="26" fill="#e8b830" opacity=".85"/></g>`;
    t += `<g transform="translate(1180,${G})"><ellipse cx="0" cy="-20" rx="90" ry="40" fill="#b07f2c" ${OUT}/><path d="M-80,-30q80,-60 160,0" fill="none" stroke="#8a6a42" stroke-width="6"/></g><path d="M1500,${G - 10}l60,-60l40,40" stroke="#5b6066" stroke-width="8" fill="none"/>`;
    put(L.set, t);
    put(L.glow, `${[[-600, 90], [100, 140], [900, 70], [1500, 120]].map(([x, w]) => `<path d="M${x - w},200L${x + w},200L${x + w * 2.4},${G + 100}L${x - w * 2.4},${G + 100}Z" fill="url(#zRay)" opacity=".5"/>`).join("")}`);
    put(L.glow, Array.from({ length: 30 }, () => `<circle class="zdust" cx="${f1(-900 + r() * 2800)}" cy="${f1(300 + r() * 1100)}" r="${f1(1.6 + r() * 3)}" fill="#fff2dc" opacity="${f1(0.3 + r() * 0.4)}"/>`).join(""));
  }

  // ---------------- close-up: two hands holding a can whose lid has domed (#id-lid); optional child's hand from below (#id-kid) ----------------
  function canClose(L, o = {}) {
    const id = o.id || "cc", t = o.time || "dusk";
    sky(L, t);
    put(L.far, `<rect x="-1200" y="900" width="3500" height="1600" fill="${t === "night" ? "#3a3026" : "#8a6a42"}"/><rect x="-1200" y="880" width="3500" height="40" fill="${t === "night" ? "#4a3e30" : "#a07a4a"}"/>`);
    if (t === "night") put(L.glow, `<circle cx="300" cy="700" r="600" fill="url(#fLamp)" opacity=".7"/>`);
    // the can: big, centred, label torn, rust at the seam, the lid domed up (bulge = o.bulge 0..1)
    const b = o.bulge ?? 1;
    put(L.set, `<g id="${id}-can" transform="translate(540,1180)"><rect x="-230" y="-300" width="460" height="560" rx="30" fill="url(#fCan)" ${OUT}/>
      <rect x="-230" y="-140" width="460" height="260" fill="#c8392b" opacity=".9"/><rect x="-230" y="-140" width="460" height="40" fill="#f2c55c"/><text x="0" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="88" fill="#fff4ea" stroke="${INK}" stroke-width="6" paint-order="stroke">อาหารกระป๋อง</text>
      <path d="M-230,-140l40,80l-40,60Z" fill="#b3ada0"/><path d="M-120,-300v20M60,-300v20" stroke="#8a4a1a" stroke-width="8"/>${[[-200, -200], [180, -60], [-170, 160]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="14" fill="#8a4a1a" opacity=".7"/>`).join("")}
      <ellipse cx="0" cy="260" rx="230" ry="40" fill="#8d9299" ${OUT}/>
      <g id="${id}-lid"><path d="M-230,-300q0,-40 40,-40h380q40,0 40,40q-230,${-150 * b} -460,0z" fill="#dfe3e6" ${OUT}/><path d="M-190,-340q190,${-110 * b} 380,0" stroke="#a9b0b6" stroke-width="3" fill="none"/><path d="M-150,-350q150,${-60 * b} 300,-10" stroke="#fff" stroke-width="5" fill="none" opacity=".5"/><path d="M-60,-370l20,-20M20,-380l24,-22" stroke="#8a4a1a" stroke-width="4"/></g></g>`);
    // our hands on the can (POV): real grips, fingers wrapping over the label, thumbs hooked at the rim, forearms into the bottom corners (Hand.grip)
    const HC = { skin: o.skin || "#ecc29c", skinS: o.skinS, sleeve: o.sleeve || "#9fc5d8", sleeveS: o.sleeveS };
    put(L.fg, `<g id="${id}-hl" transform="translate(310,1200)">${Hand.grip(HC)}</g><g id="${id}-hr" transform="translate(770,1200) scale(-1,1)">${Hand.grip(HC)}</g>`);
    // o.release: a second pair of open hands (palms to us, fingers spread) hidden at the bottom corners, for the moment we let go —
    // shots fade #id-hl/#id-hr out and #id-hlo/#id-hro in so the hands are never left as fists clenched round nothing
    if (o.release) put(L.fg, `<g id="${id}-hlo" opacity="0" transform="translate(250,1420) rotate(-16) scale(1.6)">${Hand.open(HC)}</g><g id="${id}-hro" opacity="0" transform="translate(830,1420) rotate(16) scale(-1.6,1.6)">${Hand.open(HC)}</g>`);
    L.fg.classList.remove("fgblur");
    if (o.kid) put(L.act, `<g id="${id}-kid" transform="translate(-300,1500)"><g transform="scale(0.62)">${Hand.open({ skin: "#efc6a0", sleeve: "#f6f6f2", sleeveS: "#d8d4c8" })}</g></g>`);
  }

  // ---------------- the dirt road through the paddies (actors walk on y=G): heat shimmer at noon (#id-shim), the sun low at dusk ----------------
  function fieldRoad(L, o = {}) {
    const id = o.id || "fr", t = o.time || "noon", r = mk(o.seed || 29);
    sky(L, t); sunMoon(L, t, o.sunX ?? 640, 500);
    put(L.far, paddies(r, t, 1020));
    // the road converging to the horizon, with ruts; paddies either side with stubble and a buffalo wallow
    let s = `<path d="M-200,${G + 900}L430,1030H650L1280,${G + 900}Z" fill="url(#fDirt)" ${OUT}/><path d="M80,${G + 900}L500,1040M1000,${G + 900}L580,1040" stroke="#8f6f45" stroke-width="10" fill="none" opacity=".6"/>`;
    s += `<rect x="-1200" y="1030" width="3500" height="60" fill="${t === "night" ? "#2a3024" : t === "dusk" ? "#5c5a3a" : "#7d9a4a"}"/>`;
    s += `<path d="M-1200,1090H420L-200,${G + 900}H-1200Z M1300,${G + 900}L660,1090H2300V${G + 900}Z" fill="${t === "night" ? "#1f261b" : t === "dusk" ? "#6b5a38" : "#9fb860"}"/>`;
    for (let k = 0; k < 60; k++) { const u = r(), x = u < 0.5 ? -1100 + r() * 1300 : 900 + r() * 1300, y = 1120 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}q5,-22 10,0q5,-18 10,0" stroke="${t === "night" ? "#2f3828" : "#6f8f3e"}" stroke-width="3" fill="none"/>`; }
    s += `<path d="M-1200,${G + 300}h1000M1300,${G + 500}h1100" stroke="${t === "night" ? "#2a3024" : "#5d7a35"}" stroke-width="6" opacity=".5"/>`;
    s += `<g transform="translate(-700,1180)"><ellipse rx="140" ry="40" fill="#6f6a4a" opacity=".6"/><path d="M-60,-10q20,-50 60,-50t60,50" fill="#3a3330" ${OUT}/><path d="M-20,-60q-20,-30 -40,-20M20,-60q20,-30 40,-20" stroke="${INK}" stroke-width="6" fill="none"/></g>`;
    put(L.set, s);
    if (t === "noon") put(L.glow, `<g id="${id}-shim">${Array.from({ length: 14 }, (_, k) => `<path d="M-1200,${1050 + k * 22}q200,8 400,0t400,0t400,0t400,0t400,0t400,0t400,0t400,0" stroke="#fff6dc" stroke-width="3" fill="none" opacity=".18"/>`).join("")}</g><rect x="-1200" y="980" width="3500" height="300" fill="url(#zHaze)" opacity=".9"/>`);
    if (t === "dusk") put(L.glow, `<rect x="-1200" y="900" width="3500" height="1300" fill="#ff9a3c" opacity=".12"/>`);
  }

  // ---------------- close-up of the gate from inside: bars, the cross rail, the bolt (#id-bolt slides x), arms through the bars (#id-arms) ----------------
  function gateClose(L, o = {}) {
    const id = o.id || "gc", t = o.time || "dusk", r = mk(o.seed || 61);
    sky(L, t); sunMoon(L, t, 300, 600);
    put(L.far, paddies(r, t, 1100));
    put(L.mid, `<path d="M-1200,1180L2300,1180V${G + 900}H-1200Z" fill="url(#fDirt)"/>`);
    // outside: the road up to the gate, dusk haze
    let s = `<g id="${id}-arms" opacity="${o.arms ? 1 : 0}">${[[260, 1120, -10], [520, 1060, 8], [760, 1140, -4]].map(([x, y, a]) => `<g transform="translate(${x},${y}) rotate(${a})"><path d="M0,0C-10,80 -6,160 0,240" stroke="${INK}" stroke-width="54" stroke-linecap="round" fill="none"/><path d="M0,0C-10,80 -6,160 0,240" stroke="#9dac92" stroke-width="44" stroke-linecap="round" fill="none"/><path d="M-30,250l-10,36M-8,256l-2,40M14,254l6,38M30,246l16,30" stroke="#9dac92" stroke-width="14" stroke-linecap="round"/><path d="M-40,286l-6,14M-10,296l0,14M20,292l4,14M46,276l8,12" stroke="#1b1612" stroke-width="7" stroke-linecap="round"/><circle cx="4" cy="60" r="12" fill="#7a1414" opacity=".8"/></g>`).join("")}</g>`;
    put(L.set, s);
    // the gate itself: thick bars, two rails, the bolt on our side
    let g = `<rect x="-1200" y="${G + 40}" width="3500" height="40" fill="#3a3f45"/><g id="${id}-bars">`;
    for (let b = -10; b < 12; b++) g += `<rect x="${-80 + b * 110}" y="-200" width="34" height="${G + 260}" fill="#3f454b" ${OUT}/>`;
    g += `<rect x="-1300" y="560" width="2580" height="60" fill="#3a3f45" ${OUT}/><rect x="-1300" y="1360" width="2580" height="60" fill="#3a3f45" ${OUT}/>`;
    g += `<rect x="-1300" y="-240" width="2580" height="60" fill="#3a3f45" ${OUT}/>`;
    g += `<g id="${id}-bolt" transform="translate(${o.bolt ?? 0},0)"><rect x="620" y="1180" width="560" height="60" rx="20" fill="#8d9299" ${OUT}/><rect x="560" y="1150" width="110" height="120" rx="14" fill="#5b6066" ${OUT}/><rect x="1150" y="1160" width="40" height="100" rx="8" fill="#5b6066" ${OUT}/></g>`;
    g += `</g><rect x="1180" y="-240" width="80" height="${G + 320}" fill="#5b6066" ${OUT}/><rect x="1260" y="-300" width="80" height="${G + 400}" fill="#cfc9bb" ${OUT}/><rect x="1160" y="1130" width="200" height="160" rx="10" fill="none" stroke="#5b6066" stroke-width="14"/>`;
    // beyond the gate pillar the fence goes on: rails and bars up close, another concrete post (so a drifting camera never finds open ground)
    g += `<rect x="1340" y="560" width="1100" height="60" fill="#3a3f45" ${OUT}/><rect x="1340" y="1360" width="1100" height="60" fill="#3a3f45" ${OUT}/>${Array.from({ length: 10 }, (_, b) => `<rect x="${1390 + b * 110}" y="420" width="34" height="${G - 300}" fill="#3f454b" ${OUT}/>`).join("")}<rect x="1900" y="300" width="110" height="${G - 120}" fill="#cfc9bb" ${OUT}/>`;
    put(L.fg, g);
    L.fg.classList.remove("fgblur");
    if (t === "dusk") put(L.glow, `<rect x="-1200" y="800" width="3500" height="1400" fill="#ff9a3c" opacity=".12"/>`);
  }

  // ---------------- morning close-up of the tank's gauge: a clear tube with marks, the float (#id-float) one notch lower; เจ๊หงส์'s finger (#id-finger) ----------------
  function tankClose(L, o = {}) {
    const id = o.id || "tk";
    sky(L, "morning");
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9d4c8"/><rect x="-1200" y="-800" width="1300" height="3600" fill="#cfc9bb"/><path d="M-1200,400H2300M-1200,1000H2300" stroke="#9f9a8e" stroke-width="6"/>`);
    put(L.mid, `<rect x="700" y="-800" width="90" height="3600" fill="#8a857a" ${OUT}/>${Array.from({ length: 10 }, (_, k) => `<path d="M640,${-700 + k * 300}h210" stroke="#8a857a" stroke-width="26"/>`).join("")}`);
    let s = `<rect x="300" y="200" width="150" height="1500" rx="60" fill="#e8f1f5" ${OUT}/>${Array.from({ length: 10 }, (_, k) => `<path d="M300,${320 + k * 140}h-70" stroke="${INK}" stroke-width="8"/><text x="200" y="${338 + k * 140}" text-anchor="end" font-family="Kanit" font-weight="700" font-size="52" fill="${INK}">${10 - k}</text>`).join("")}`;
    s += `<rect id="${id}-water" x="312" y="${320 + 140 * (10 - (o.level ?? 7))}" width="126" height="${1380 - 140 * (10 - (o.level ?? 7))}" rx="50" fill="#6fb3d6" opacity=".85"/>`;
    s += `<g id="${id}-float" transform="translate(375,${320 + 140 * (10 - (o.level ?? 7))})"><rect x="-56" y="-30" width="112" height="60" rx="16" fill="#c8392b" ${OUT}/><path d="M-70,0h140" stroke="#c8392b" stroke-width="8"/></g>`;
    s += `<path d="M375,1700v120h300" stroke="#8a857a" stroke-width="18" fill="none"/>${[[380, 1740], [400, 1790]].map(([x, y]) => `<path d="M${x},${y}c8,14 10,22 2,26c-8,-4 -8,-12 -2,-26z" fill="#6fb3d6"/>`).join("")}`;
    // a pencil mark from last night at the old level, now one notch above the float
    s += `<g id="${id}-mark"><path d="M240,${330 + 140 * (10 - (o.level ?? 7) - 1)}h130" stroke="#c8392b" stroke-width="6" stroke-dasharray="14 8"/><text x="470" y="${346 + 140 * (10 - (o.level ?? 7) - 1)}" font-family="Kanit" font-weight="700" font-size="40" fill="#c8392b">เมื่อคืน</text></g>`;
    put(L.set, s);
    put(L.fg, `<g id="${id}-finger" transform="translate(900,1500)"><g transform="scale(0.8)">${Hand.point({ skin: "#e6b48c", skinS: "#c48a62", sleeve: "#d96a8a", sleeveS: "#b04f6e" })}</g></g>`);
    L.fg.classList.remove("fgblur");
    put(L.glow, `<path d="M-300,-200L-100,-200L600,1900L300,1900Z" fill="url(#zRay)" opacity=".7"/>`);
  }

  // ---------------- night: the old radio on the shelf, its dial glowing when it wakes (#id-dialw), needle (#id-needle); the room dark ----------------
  function radioClose(L, o = {}) {
    const id = o.id || "rc";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#0b0d12"/>`);
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2620"/><rect x="-1200" y="1180" width="3500" height="40" fill="#5a4630"/><rect x="-1200" y="1220" width="3500" height="1200" fill="#3a2e20"/>`);
    let s = `<g transform="translate(540,1180)"><rect x="-420" y="-470" width="840" height="470" rx="40" fill="#6b4a2e" ${OUT}/><rect x="-400" y="-450" width="800" height="430" rx="30" fill="#7a5a3e"/>
      <rect x="-360" y="-410" width="400" height="220" rx="16" fill="#1a1512" ${OUT}/><rect x="-350" y="-400" width="380" height="200" rx="12" fill="#2a1a0a"/>
      <g id="${id}-dialw" opacity="0"><rect x="-350" y="-400" width="380" height="200" rx="12" fill="#ffb35c" opacity=".55"/></g>
      ${Array.from({ length: 13 }, (_, k) => `<path d="M${-330 + k * 30},${-380}v${k % 3 ? 16 : 30}" stroke="#e9d9a8" stroke-width="3"/>`).join("")}<text x="-160" y="-230" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#e9d9a8" opacity=".8">AM 530 · 700 · 900 · 1200 · 1600</text>
      <rect id="${id}-needle" x="-200" y="-396" width="5" height="190" fill="#ff3b30"/>
      <rect x="80" y="-410" width="280" height="330" rx="14" fill="#2a2420" ${OUT}/>${Array.from({ length: 11 }, (_, k) => `<path d="M${100 + k * 24},-400v310" stroke="#c9a55a" stroke-width="5" opacity=".55"/>`).join("")}
      <circle cx="-260" cy="-110" r="56" fill="#c9a55a" ${OUT}/><circle cx="-100" cy="-110" r="56" fill="#c9a55a" ${OUT}/><path d="M-260,-150v30M-100,-150v30" stroke="${INK}" stroke-width="6"/><text x="-180" y="-30" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#e9d9a8" opacity=".7">THANARAT · 1979</text>
      <path d="M360,-470L560,-900" stroke="#9aa0a6" stroke-width="10"/><circle cx="560" cy="-900" r="10" fill="#9aa0a6"/>
      <rect x="-440" y="0" width="880" height="26" fill="#5a4630" ${OUT}/></g>`;
    s += `<g transform="translate(-180,1180)"><rect x="-60" y="-220" width="120" height="220" rx="10" fill="#3a3330" ${OUT}/><rect x="-40" y="-190" width="80" height="140" fill="#2a2420"/></g>`;
    put(L.set, s);
    put(L.glow, `<g id="${id}-glow" opacity="0"><circle cx="380" cy="880" r="520" fill="url(#fDial)"/></g>`);
  }

  // ---------------- น้องปั้น's crayon drawing, full frame on a pinned sheet: the school, five figures by the building, a sixth (#id-six) on top of the tank ----------------
  function drawing(L, o = {}) {
    const id = o.id || "dw";
    if (!o.onPlate) put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = o.onPlate ? `<g transform="${o.onPlate}">` : `<g transform="rotate(-2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += C("M200,420q60,-60 120,0M160,480q100,-120 200,0", "#f2c55c", 12) + `<circle cx="260" cy="430" r="60" fill="#f2c55c" opacity=".8" filter="url(#fCrayon)"/>`;
    s += C("M150,1300H930", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M450,1300l0,-120M750,1300l0,-120M850,1300l0,-120M930,1300l0,-120M150,1180H930", "#5b6066", 8);
    s += C("M200,1140V820H640V1140M160,820L420,700L680,820M250,900h80v120h-80zM480,900h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="820" width="440" height="320" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    s += C("M760,1140V760M880,1140V760M740,760h160v-120h-160z", "#5b6066", 10) + `<rect x="740" y="640" width="160" height="120" fill="#9fc5d8" opacity=".7" filter="url(#fCrayon)"/>`;
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="-10" cy="-136" r="4" fill="${col}"/><circle cx="10" cy="-136" r="4" fill="${col}"/><path d="M-12,-118q12,10 24,0" stroke="${col}" stroke-width="4" fill="none"/></g>`;
    s += fig(280, 1420, "#2f4a8a") + fig(380, 1430, "#c8392b") + fig(470, 1420, "#6f8f3e") + fig(560, 1430, "#d96a8a") + fig(640, 1450, "#e8b830", 0.7);
    s += `<g id="${id}-six">${fig(820, 640, "#2e2a26", 0.6)}</g>`;
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 100 บ้านของปั้น</text>`;
    s += `<text x="300" y="1560" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครูพิม ก้อง ลุง เจ๊ ปั้น</text></g>`;
    put(L.set, s);
    if (!o.onPlate) put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ---------------- top-down map of the compound: fence, gate, classroom, tank, flagpole; the road, paddies and the market 1.2 km away ----------------
  // ids: #id-pin0..4 (pins the shot reveals), #id-path (dotted route to the market), #id-ring (sound ring at the market)
  function mapTop(L, o = {}) {
    const id = o.id || "mp";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2d27"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9d3c0"/>`;
    s += `${Array.from({ length: 12 }, (_, k) => `<rect x="${-1100 + (k % 4) * 560}" y="${-600 + Math.floor(k / 4) * 900}" width="520" height="860" fill="#b7bfa0" opacity=".7" stroke="#9aa48a" stroke-width="5"/>${Array.from({ length: 7 }, (_, j) => `<path d="M${-1100 + (k % 4) * 560 + 20},${-600 + Math.floor(k / 4) * 900 + 60 + j * 110}h480" stroke="#a3ad90" stroke-width="3"/>`).join("")}`).join("")}`;
    s += `<path d="M-200,-800L-200,2800" stroke="#e9e2cc" stroke-width="90"/><path d="M-200,1240H1600" stroke="#e9e2cc" stroke-width="70"/><path d="M-200,-800V2800M-200,1240H1600" stroke="#bfb79f" stroke-width="4" stroke-dasharray="40 40"/>`;
    if (o.rings) s += `<g id="${id}-rings">${[[400, "400 ม."], [800, "800 ม."], [1200, "1.2 กม."]].map(([R, t], k) => `<circle cx="540" cy="900" r="${R}" fill="none" stroke="#1e1d1b" stroke-width="${k === 2 ? 5 : 3}" stroke-dasharray="${k === 2 ? "18 14" : "10 12"}" opacity=".55"/><g transform="translate(${540 + R * 0.72},${900 - R * 0.7})"><rect x="-70" y="-26" width="140" height="52" rx="26" fill="#f3eee3" stroke="#1e1d1b" stroke-width="3"/><text y="12" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#1e1d1b">${t}</text></g>`).join("")}</g>`;
    s += `<rect x="120" y="420" width="840" height="760" fill="#efe9d8" stroke="#3a3f45" stroke-width="14"/><rect x="430" y="1172" width="220" height="24" fill="#d9342b"/>`;
    s += `<rect x="170" y="470" width="520" height="190" rx="10" fill="#c7b48e" ${OUT}/><text x="430" y="585" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="${INK}">อาคารเรียน</text>`;
    s += `<circle cx="860" cy="560" r="80" fill="#9fc5d8" ${OUT}/><text x="860" y="700" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="${INK}">แท็งก์น้ำ</text>`;
    s += `<circle cx="540" cy="900" r="18" fill="#9aa0a6" ${OUT}/><text x="540" y="970" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="${INK}">เสาธง</text>`;
    s += `<text x="540" y="1270" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="#c8392b">ประตู</text>`;
    s += `<g transform="translate(1500,1250)"><rect x="-150" y="-110" width="300" height="220" rx="14" fill="#9aa0a6" ${OUT}/>${[0, 1, 2].map((k) => `<rect x="${-120 + k * 90}" y="-80" width="60" height="160" fill="#7f858c"/>`).join("")}<text x="0" y="170" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${INK}">ตลาดร้าง</text></g>`;
    s += `<path id="${id}-path" d="M540,1200V1240H1350" stroke="#c8392b" stroke-width="10" fill="none" stroke-dasharray="26 22" pathLength="1" stroke-dashoffset="${o.path ? 0 : 1}" style="stroke-dasharray:${o.path ? "26 22" : "1"};stroke-dashoffset:${o.path ? 0 : 1}"/>`;
    s += `<text x="1000" y="1200" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="36" fill="#c8392b">1.2 กม.</text>`;
    s += `<g transform="translate(-900,-600)"><circle r="70" fill="#f6e7cf" ${OUT}/><path d="M0,-50L18,0L0,50L-18,0Z" fill="#c8392b"/><text y="110" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="${INK}">N</text></g>`;
    s += `<text x="-900" y="1900" font-family="Kanit" font-weight="700" font-size="36" fill="#5d7a35">ทุ่งนา</text><text x="1700" y="300" font-family="Kanit" font-weight="700" font-size="36" fill="#5d7a35">ทุ่งนา</text>`;
    if (o.ring) s += `<g id="${id}-ring">${[0, 1, 2].map((k) => `<circle class="fring" cx="1500" cy="1250" r="${120 + k * 120}" fill="none" stroke="#ff5a3a" stroke-width="10" opacity="${0.8 - k * 0.25}"/>`).join("")}</g>`;
    put(L.set, s);
    put(L.light, `<rect x="0" y="0" width="1080" height="1920" fill="url(#fGrid)" opacity="0"/>`);
  }
  // the compound's pins for the map (added by the shot): label + drop marker at world (x, y)
  function pin(L, id, x, y, label, col = "#c8392b") {
    put(L.act, `<g id="${id}" opacity="0"><g transform="translate(${x},${y})"><path d="M0,0C-40,-60 -60,-90 -60,-130a60,60 0 1 1 120,0c0,40 -20,70 -60,130z" fill="${col}" ${OUT}/><circle cy="-130" r="22" fill="#f4ecd8"/><rect x="-170" y="-250" width="340" height="70" rx="35" fill="#f3eee3" stroke="#1e1d1b" stroke-width="3"/><text y="-200" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="36" fill="#1e1d1b">${label}</text></g></g>`);
  }



  // ---------------- AI-painted plates (assets/art/<name>.png, 1080×1920 at world 0,0): the scene is a picture; only what must move is drawn on top ----------------
  // o.set = plate for the set layer (parallax 1), o.far = optional plate for the far layer, o.fg = keyed foreground piece {name, x, y, s, blur}
  function plate(L, o = {}) {
    const img = (name, x = 0, y = 0, w = 1080, h = 1920, extra = "") => `<image href="assets/art/${name}.png" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="none" ${extra}/>`;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="${o.bg || "#0b0d10"}"/>`);
    if (o.far) put(L.far, img(o.far, -200, -200, 1480, 2320));
    if (o.set) put(L.set, img(o.set, o.x ?? 0, o.y ?? 0, o.w ?? 1080, o.h ?? 1920));
    if (o.fg) { const f = o.fg; put(L.fg, `<g id="${o.id || "pl"}-fg" transform="translate(${f.x},${f.y}) scale(${f.s || 1})">${img(f.name)}</g>`); if (f.blur === false) L.fg.classList.remove("fgblur"); }
    if (o.fgOff) L.fg.classList.remove("fgblur");
  }
  // iron bars drawn over a region so rigs placed behind them read as "outside the fence": x0..x1 at y0..y1, bar pitch p
  function bars(L, id, x0, x1, y0, y1, p = 30, col = "#1a1d22") {
    let s = `<g id="${id}">`;
    for (let x = x0; x < x1; x += p) s += `<rect x="${x}" y="${y0}" width="${Math.round(p * 0.32)}" height="${y1 - y0}" fill="${col}"/>`;
    s += `<rect x="${x0}" y="${y0 + (y1 - y0) * 0.12}" width="${x1 - x0}" height="${Math.round(p * 0.4)}" fill="${col}"/><rect x="${x0}" y="${y1 - (y1 - y0) * 0.2}" width="${x1 - x0}" height="${Math.round(p * 0.4)}" fill="${col}"/></g>`;
    put(L.act, s);
  }
  // the gate panel for the dusk gate plate: a sliding section of bars with its bolt, x = left edge in world space
  function gatePanel(L, id, x, y0 = 150, h = 1200, w = 470) {
    put(L.act, `<g id="${id}" transform="translate(${x},0)"><rect x="0" y="${y0}" width="${w}" height="${h}" fill="none" stroke="#2a2d31" stroke-width="22"/>
      ${Array.from({ length: Math.floor(w / 34) }, (_, b) => `<rect x="${14 + b * 34}" y="${y0 + 8}" width="12" height="${h - 16}" fill="#2f3337"/><rect x="${14 + b * 34}" y="${y0 + 8}" width="4" height="${h - 16}" fill="#4a4f55" opacity=".7"/>`).join("")}
      <rect x="0" y="${y0 + h * 0.45}" width="${w}" height="24" fill="#2a2d31"/><rect x="0" y="${y0 + h * 0.82}" width="${w}" height="24" fill="#2a2d31"/>
      <g id="${id}-bolt"><rect x="-80" y="${y0 + h * 0.47 - 8}" width="150" height="26" rx="10" fill="#8d9299" ${OUT}/><rect x="-92" y="${y0 + h * 0.47 - 22}" width="36" height="54" rx="8" fill="#5b6066" ${OUT}/></g></g>`);
  }

  // ---------------- top-down of the gate: the road and the crowd outside (top), the yard inside (bottom); figures are seen from above ----------------
  // ids: #id-gate (slides along x), #id-z0.. (the crowd, arms toward the bars), #id-in0.. (people inside)
  function gateTop(L, o = {}) {
    const id = o.id || "gtop", FY = 960, r = mk(o.seed || 77);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2420"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="${FY + 800}" fill="#5c4a63"/><rect x="-1200" y="${FY - 480}" width="3500" height="420" fill="#8a6a42"/>`;   // dusk road
    s += `<path d="M-1200,${FY - 270}H2300" stroke="#a07a4a" stroke-width="14" stroke-dasharray="90 70"/>`;
    s += `<rect x="-1200" y="${FY}" width="3500" height="2000" fill="url(#fDirt)"/>`;
    for (let k = 0; k < 30; k++) { const x = -1100 + r() * 3400, y = FY + 60 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}q6,-18 12,0q6,-14 12,0" stroke="#6f8f3e" stroke-width="4" fill="none"/>`; }
    // the fence from above: a concrete strip with square posts, the gate opening in the middle
    s += `<rect x="-1200" y="${FY - 30}" width="1644" height="60" fill="#cfc9bb" ${OUT}/><rect x="896" y="${FY - 30}" width="1404" height="60" fill="#cfc9bb" ${OUT}/>`;
    for (let x = -1100; x < 2300; x += 220) { if (x > 420 && x < 900) continue; s += `<rect x="${x - 6}" y="${FY - 42}" width="52" height="84" fill="#b3ada0" ${OUT}/>`; }
    s += `<rect x="400" y="${FY - 46}" width="44" height="92" fill="#b3ada0" ${OUT}/><rect x="896" y="${FY - 46}" width="44" height="92" fill="#b3ada0" ${OUT}/>`;
    s += `<g id="${id}-gate" transform="translate(${444 + (o.gate || 0) * 440},0)"><rect x="0" y="${FY - 16}" width="452" height="32" fill="#3a3f45" ${OUT}/>${Array.from({ length: 14 }, (_, b) => `<rect x="${12 + b * 32}" y="${FY - 22}" width="10" height="44" fill="#5b6066"/>`).join("")}</g>`;
    s += `<rect x="440" y="${FY + 16}" width="456" height="8" fill="#3a3f45"/>`;
    put(L.set, s);
    // the horde from above: shoulders, head, two arms stretched at the bars (ids -z0..; each in a plain outer group so GSAP can move it)
    const fig = (x, y, top, skin, hair, dead) => `<g transform="translate(${x},${y})"><ellipse rx="78" ry="42" fill="${top}" ${OUT}/><path d="M-60,-20L-150,70M60,-20L150,70" stroke="${INK}" stroke-width="40" stroke-linecap="round"/><path d="M-60,-20L-150,70M60,-20L150,70" stroke="${skin}" stroke-width="30" stroke-linecap="round"/>
      ${dead ? `<path d="M-150,70l-10,30M-156,66l-30,18M150,70l10,30M156,66l30,18" stroke="#1b1612" stroke-width="10" stroke-linecap="round"/><ellipse cx="20" cy="10" rx="18" ry="12" fill="#7a1414" opacity=".8"/>` : ""}<circle r="38" fill="${hair}" ${OUT}/><circle cx="-10" cy="-14" r="10" fill="${skin}" opacity=".7"/></g>`;
    const Z = [[560, FY - 150, "#2c3e6b", "#a3ae8e", "#9a948c"], [700, FY - 120, "#e6e8e2", "#b0b9a2", "#1f1a18"], [850, FY - 170, "#4f6a7a", "#98a88f", "#dfe6e2"], [430, FY - 230, "#2c3e6b", "#a3ae8e", "#9a948c"], [1000, FY - 260, "#e6e8e2", "#b0b9a2", "#1f1a18"]];
    put(L.act, Z.map(([x, y, top, skin, hair], k) => `<g id="${id}-z${k}">${fig(x, y, top, skin, hair, true)}</g>`).join(""));
    // inside: ครูพิม and ลุงหมาน shoving the panel (arms up at the gate), ก้อง sprawled on the dirt
    put(L.act, `<g id="${id}-in0">${fig(520, FY + 150, "#9fc5d8", "#ecc29c", "#2b2522", false).replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110").replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110")}</g>
      <g id="${id}-in1">${fig(760, FY + 150, "#2c3e6b", "#b9805a", "#d9b86a", false).replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110").replace("L-150,70M60,-20L150,70", "L-110,-110M60,-20L110,-110")}</g>
      <g id="${id}-in2" transform="translate(300,${FY + 330}) rotate(-70)"><ellipse rx="78" ry="42" fill="#b8463a" ${OUT}/><path d="M-60,-20L-150,40M60,-20L150,40" stroke="${INK}" stroke-width="40" stroke-linecap="round"/><path d="M-60,-20L-150,40M60,-20L150,40" stroke="#d6a27c" stroke-width="30" stroke-linecap="round"/><rect x="-40" y="30" width="80" height="150" rx="30" fill="#4a4e3a" ${OUT}/><circle r="38" fill="#231a16" ${OUT}/><path d="M-30,-30h60" stroke="#e07a4f" stroke-width="10"/></g>`);
    put(L.glow, `<rect x="-1200" y="-800" width="3500" height="${FY}" fill="#ff9a3c" opacity=".1"/>`);
  }

  // looping motion for this story's sets
  function flife(tl, scope, t0, dur) {
    const root = document.querySelector(scope);
    if (!root || root.dataset.flife) return;
    root.dataset.flife = "1";
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q("[id$='-shim'] path").forEach((el, i) => tl.fromTo(el, { x: -30 + (i % 3) * 10 }, { x: 30, duration: 0.9 + (i % 4) * 0.2, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q("[id$='-flagc']").forEach((el) => tl.fromTo(el, { skewY: -3 }, { skewY: 3, svgOrigin: "6 -690", duration: 0.8, repeat: Math.ceil(dur / 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".fly").forEach((el, i) => tl.fromTo(el, { x: -8 - (i % 3) * 3, y: 6 }, { x: 10 + (i % 4) * 3, y: -12 - (i % 3) * 5, duration: 0.22 + (i % 5) * 0.05, repeat: Math.ceil(dur / 0.22), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 7) * 0.03));
    q(".lampf").forEach((el, i) => { const st = 0.16 + (i % 3) * 0.05; for (let t = 0; t < dur; t += st) { const v = 0.82 + Math.abs((Math.sin((t * 7.3 + i) * 13.1) * 43758.5) % 1) * 0.22; tl.to(el, { opacity: v, duration: st, ease: "sine.inOut" }, t0 + t); } });
    q(".mote").forEach((el, i) => { tl.fromTo(el, { x: 0, y: 0 }, { x: 40 + (i % 5) * 18, y: -60 - (i % 4) * 20, duration: 2.6 + (i % 5) * 0.5, repeat: Math.ceil(dur / 2.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 - (i % 7) * 0.4); tl.fromTo(el, { opacity: 0.05 }, { opacity: 0.7, duration: 0.9 + (i % 3) * 0.3, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 - (i % 5) * 0.3); });
    q(".fanspin").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360, duration: 0.9, repeat: Math.ceil(dur / 0.9), ease: "none", transformOrigin: "0px 0px", immediateRender: false }, t0));
    q(".raind").forEach((el) => tl.fromTo(el, { y: -160 }, { y: 160, duration: 0.42, repeat: Math.ceil(dur / 0.42), ease: "none", immediateRender: false }, t0));
    q(".raind2").forEach((el) => tl.fromTo(el, { y: -120 }, { y: 120, duration: 0.6, repeat: Math.ceil(dur / 0.6), ease: "none", immediateRender: false }, t0));
    q(".rsplash ellipse").forEach((el, i) => tl.fromTo(el, { opacity: 0.7, scale: 0.3 }, { opacity: 0, scale: 1.6, transformOrigin: "50% 50%", duration: 0.5, repeat: Math.ceil(dur / 0.5), ease: "power1.out", immediateRender: false }, t0 + (i % 9) * 0.06));
    q(".cowisp").forEach((el, i) => tl.fromTo(el, { y: 20, opacity: 0.16 }, { y: -120, opacity: 0, duration: 2.2 + (i % 3) * 0.4, repeat: Math.ceil(dur / 2.2), ease: "sine.out", immediateRender: false }, t0 + i * 0.5));
    q(".fring").forEach((el, i) => tl.fromTo(el, { scale: 0.3, opacity: 0.9 }, { scale: 2.2, opacity: 0, svgOrigin: "1500 1250", duration: 1.6, repeat: Math.ceil(dur / 1.6), ease: "power1.out", immediateRender: false }, t0 + i * 0.5));
  }

  // ---------------- depth and light (the v2 look): blurred foreground silhouettes, atmospheric haze between far and set, soft light sources ----------------
  // depth(L, kind): dark out-of-focus shapes in L.fg (parallax 1.5 + the fg blur) — grass | bars | post | desk | branch | shelf
  let DEPN = 0;
  function depth(L, kind, o = {}) {
    const col = o.col || "#06080a", op = o.op ?? 0.92, r = mk(o.seed || 7 + DEPN++);
    const D = {
      grass: () => { let g = ""; for (let k = 0; k < 26; k++) { const x = (k < 13 ? -120 : 760) + r() * 420, h = 160 + r() * 260, w = 18 + r() * 22; g += `<path d="M${f1(x)},2000q${f1(-w)},${f1(-h * 0.5)} ${f1(w * 0.3)},${f1(-h)}q${f1(w)},${f1(h * 0.45)} ${f1(w * 1.6)},${f1(h)}z" fill="${col}"/>`; } return g + `<path d="M-1800,1800q500,-60 1000,0t1000,0t1000,0t1000,0t1000,0V2600H-1800z" fill="${col}"/>`; },   // wide enough that a camera pulling back from the first key never finds its end
      bars: () => [-60, 110, 280].map((x, k) => `<rect x="${x}" y="-400" width="${70 + k * 10}" height="2800" rx="20" fill="${col}"/>`).join("") + `<rect x="-1200" y="700" width="1640" height="60" fill="${col}"/>`,
      post: () => `<rect x="${o.x ?? -80}" y="-400" width="${o.w ?? 220}" height="2800" fill="${col}"/>`,
      desk: () => `<path d="M-1800,1666L2900,1336V2700H-1800z" fill="${col}"/><path d="M-1800,1666L2900,1336l0,40L-1800,1706z" fill="#2a2420"/>`,
      branch: () => `<path d="M-200,-200C100,-60 380,40 560,0C400,160 120,220 -200,200z" fill="${col}"/>${[[60, 120], [200, 60], [380, 90], [300, 180]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="90" ry="40" transform="rotate(${-30 + x / 10} ${x} ${y})" fill="${col}"/>`).join("")}`,
      shelf: () => `<rect x="-300" y="-400" width="420" height="2800" fill="${col}"/><rect x="-300" y="900" width="700" height="50" fill="${col}"/><rect x="-300" y="1500" width="700" height="50" fill="${col}"/>`,
    };
    // shapes are drawn in screen coordinates for the shot's first camera key (o.cam = {x, y, s}): map them back through the fg parallax (1.5)
    const c = o.cam || { x: 0, y: 0, s: 1 }, ls = 1 + (c.s - 1) * 1.5;
    put(L.fg, `<g opacity="${op}" transform="translate(${f1(540 + c.x * 1.5)},${f1(960 + c.y * 1.5)}) scale(${(1 / ls).toFixed(4)}) translate(-540,-960)">${(D[kind] || D.grass)()}</g>`);
  }
  // haze(L, y, h, col, op): a soft band of atmosphere in the mid layer (parallax .6) so the far ground sits behind the set
  function haze(L, y = 1000, h = 500, col = "#cfd8d4", op = 0.3) {
    op *= 0.5;
    const id = `hz${DEPN++}`;
    put(L.mid, `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity="0"/><stop offset=".55" stop-color="${col}" stop-opacity="${op}"/><stop offset="1" stop-color="${col}" stop-opacity="${op * 0.3}"/></linearGradient><rect x="-1200" y="${y - h}" width="3500" height="${h + 200}" fill="url(#${id})"/>`);
  }
  // light(L, x, y, r, col, op): a soft light source above the darkness (glow layer): core + wide bloom; cls = "lampf" flickers (flife)
  // light(L, x, y, R, col, op, cls): a light SOURCE the professional way — a tight bright core with a short halo at the lamp itself,
  // never a frame-wide wash (the user: "แสงบังจนดูไม่รู้เรื่อง"); the floor gets its light from cone() instead
  function light(L, x, y, R = 500, col = "#ffd58a", op = 0.5, cls = "") {
    if (!Fence.GLOW) return;
    const id = `lt${DEPN++}`;
    put(L.glow, `<radialGradient id="${id}"><stop offset="0" stop-color="#fff6e0" stop-opacity="${Math.min(1, op * 1.1)}"/><stop offset=".12" stop-color="${col}" stop-opacity="${op * 0.55}"/><stop offset=".3" stop-color="${col}" stop-opacity="${op * 0.14}"/><stop offset=".6" stop-color="${col}" stop-opacity="${op * 0.03}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></radialGradient>
      <g class="${cls}"><circle cx="${x}" cy="${y}" r="${R * 0.5}" fill="url(#${id})"/></g>`);
  }
  // cone(L, x, y, w, h, col, op): the light a lamp at (x, y) throws — a faint narrow beam and a soft pool on the floor at y + h (the pool sits
  // under the actors in the set layer, so people stand IN the light instead of behind a glow)
  function cone(L, x, y, w = 600, h = 900, col = "#ffd58a", op = 0.35, cls = "lampf") {
    if (!Fence.GLOW) return;
    const id = `cn${DEPN++}`;
    put(L.glow, `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity="${op * 0.32}"/><stop offset=".5" stop-color="${col}" stop-opacity="${op * 0.08}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>
      <path class="${cls}" d="M${x - 26},${y}L${x + 26},${y}L${x + w * 0.42},${y + h}L${x - w * 0.42},${y + h}Z" fill="url(#${id})"/>`);
    put(L.set, `<radialGradient id="${id}p"><stop offset="0" stop-color="${col}" stop-opacity="${op * 0.5}"/><stop offset=".55" stop-color="${col}" stop-opacity="${op * 0.18}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></radialGradient>
      <ellipse class="${cls}" cx="${x}" cy="${y + h}" rx="${w * 0.62}" ry="${w * 0.15}" fill="url(#${id}p)"/>`);
  }
  // rays(L, x0, x1, y0, y1, n, col): slanted light shafts (glow layer)
  function rays(L, x0 = -600, x1 = 400, y0 = 300, y1 = 1500, n = 4, col = "#ffd8a0", op = 0.5) {
    if (!Fence.GLOW) return;   // thin, faint shafts: a hint of dust in the air, not a wall of yellow
    const id = `ry${DEPN++}`;
    put(L.glow, `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity="${op * 0.3}"/><stop offset=".7" stop-color="${col}" stop-opacity="${op * 0.06}"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>
      ${Array.from({ length: n }, (_, k) => { const w = (x1 - x0) / n, x = x0 + k * w; return `<path d="M${x},${y0}h${w * 0.2}L${x + w * 0.2 + (x1 - x0) * 0.6},${y1}h${-w * 0.42}Z" fill="url(#${id})"/>`; }).join("")}`);
  }

  // clouds(L, seed): soft cloud banks high above the set (mid layer, parallax .6) for a camera that starts in the sky and drops through them
  function clouds(L, seed = 5) {
    const r = mk(seed); let s = "";
    for (let k = 0; k < 14; k++) { const x = -900 + r() * 2900, y = -1500 + r() * 1300, w = 260 + r() * 420, op = (0.75 + r() * 0.25).toFixed(2);
      s += `<g opacity="${op}">${[[0, 0, 1], [-0.4, 0.15, 0.7], [0.42, 0.12, 0.75], [0.1, -0.22, 0.6]].map(([dx, dy, k2]) => `<ellipse cx="${f1(x + dx * w)}" cy="${f1(y + dy * w * 0.35)}" rx="${f1(w * 0.55 * k2)}" ry="${f1(w * 0.22 * k2)}" fill="#f1f4f6"/>`).join("")}<ellipse cx="${f1(x)}" cy="${f1(y + w * 0.12)}" rx="${f1(w * 0.6)}" ry="${f1(w * 0.14)}" fill="#c9d3da" opacity=".6"/></g>`; }
    put(L.mid, s);
    put(L.far, `<rect x="-1200" y="-2200" width="3500" height="1500" fill="#dfe8ee" opacity=".35"/>`);
  }

  Object.assign(Sets, { schoolYard, classroom, market, canClose, fieldRoad, gateClose, tankClose, radioClose, drawing, mapTop, gateTop, plate });
  window.Fence = { chalk, pin, flife, paddies, bars, gatePanel, depth, haze, light, cone, rays, clouds, GLOW: true };
  // ======================================================================================================
  // EP.2 "เครื่องปั่นไฟ": the temple fair at noon, the generator POV, the classroom with the generator / fan / bulb /
  // exhaust, the hill with the answering light, น้องปั้น's second drawing
  // ======================================================================================================
  const FAN = (id, x, y) => `<g id="${id}-fan" transform="translate(${x},${y})"><path d="M0,-260V-40" stroke="#5b6066" stroke-width="14"/><g class="fanspin" style="transform-origin:0px 0px">${[0, 1, 2].map((k) => `<path d="M0,0L-30,-26L-230,-18L-220,22L-26,26Z" fill="#dfe3e6" ${OUT} transform="rotate(${k * 120})"/>`).join("")}</g><circle r="34" fill="#9aa0a6" ${OUT}/><circle r="12" fill="#5b6066"/></g>`;
  const BULB = (id, x, y) => `<g id="${id}-bulbbody" transform="translate(${x},${y})"><path d="M0,-200V-70" stroke="#2a2420" stroke-width="5"/><rect x="-18" y="-70" width="36" height="30" rx="4" fill="#9aa0a6" ${OUT}/><circle r="40" cy="0" fill="#f4ecd8" ${OUT}/><path d="M-10,0q10,-24 20,0" stroke="#9aa0a6" stroke-width="3" fill="none"/></g>`;

  // ---------------- the abandoned temple fair at noon: a small ferris wheel (#id-wheel spins), torn striped tents, a stage with speakers, the generator on a cart (#id-cart) ----------------
  function fair(L, o = {}) {
    const id = o.id || "fa", r = mk(o.seed || 83), t = o.time || "noon", G = 1500;
    sky(L, t); sunMoon(L, t, 300, 420);
    put(L.far, paddies(r, t, 1040));
    const R = 330, cx = 1320, cy = 640;
    let w = `<g transform="translate(${cx},${cy})"><path d="M-220,${R + 340}L0,0L220,${R + 340}Z" fill="none" stroke="#5b6066" stroke-width="18"/><path d="M-300,${R + 340}h600" stroke="#5b6066" stroke-width="22"/></g>`;
    w += `<g id="${id}-wheel" transform="translate(${cx},${cy})"><circle r="${R}" fill="none" stroke="#c8392b" stroke-width="14"/><circle r="${R - 70}" fill="none" stroke="#c8392b" stroke-width="6" opacity=".7"/>`;
    for (let k = 0; k < 8; k++) { const a = (k * Math.PI) / 4; w += `<path d="M0,0L${f1(Math.cos(a) * R)},${f1(Math.sin(a) * R)}" stroke="#5b6066" stroke-width="8"/><g transform="translate(${f1(Math.cos(a) * R)},${f1(Math.sin(a) * R)})"><rect x="-44" y="-8" width="88" height="68" rx="12" fill="${["#f2c55c", "#9fc5d8", "#d96a8a", "#6f8f58"][k % 4]}" ${OUT}/></g>`; }
    w += `<circle r="26" fill="#f4ecd8" ${OUT}/></g>`;
    put(L.mid, w);
    let s = `<rect x="-1200" y="${G - 40}" width="3500" height="1400" fill="url(#fDirt)"/>`;
    const tent = (x, col) => `<g transform="translate(${x},${G})"><path d="M-40,0V-420M300,0V-420" stroke="#8a6a42" stroke-width="12"/><path d="M-130,-420L130,-570L390,-420Z" fill="${col}" ${OUT}/>${[0, 1, 2, 3].map((k) => `<path d="M${-110 + k * 130},-420L${-45 + k * 130},-560" stroke="#f4ecd8" stroke-width="24" opacity=".5"/>`).join("")}<path d="M-130,-420l40,70l30,-70l50,100l40,-100l60,80l30,-80l60,50l-20,-50" fill="none" stroke="${INK}" stroke-width="4"/><path d="M-110,-430q30,70 0,140q40,-40 25,-140z" fill="${col}" opacity=".85" ${OUT}/></g>`;
    s += tent(-760, "#d96a8a") + tent(-230, "#f2c55c") + tent(1760, "#6f8f58");
    s += `<g transform="translate(700,${G})"><path d="M-430,-120V-640M430,-120V-640" stroke="#8a6a42" stroke-width="14"/><rect x="-400" y="-120" width="800" height="120" fill="#6b4a2e" ${OUT}/><rect x="-360" y="-470" width="110" height="350" fill="#2a2420" ${OUT}/><circle cx="-305" cy="-390" r="30" fill="#1a1512" stroke="#8d9299" stroke-width="6"/><circle cx="-305" cy="-250" r="46" fill="#1a1512" stroke="#8d9299" stroke-width="6"/>
      <g transform="rotate(7 0 -560)"><rect x="-400" y="-620" width="800" height="120" fill="#c8392b" opacity=".85" ${OUT}/><text x="0" y="-532" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#f4ecd8">งานวัดประจำปี</text></g></g>`;
    for (let k = 0; k < 14; k++) { const x = -1100 + r() * 3300, y = G + 60 + r() * 700; s += `<path d="M${f1(x)},${f1(y)}l${f1(20 + r() * 30)},${f1(-6 + r() * 12)}" stroke="#d9d4c8" stroke-width="8" stroke-linecap="round" opacity=".6"/>`; }
    put(L.set, s);
    put(L.act, `<g id="${id}-cart" transform="translate(${o.cartX ?? 260},${G})"><rect x="-180" y="-150" width="360" height="30" fill="#5b6066" ${OUT}/><path d="M170,-150L330,-270" stroke="#5b6066" stroke-width="14" stroke-linecap="round"/><circle cx="-110" cy="-50" r="50" fill="#2a2420" stroke="#8d9299" stroke-width="10"/><circle cx="110" cy="-50" r="50" fill="#2a2420" stroke="#8d9299" stroke-width="10"/>${Sets.props.generator(`${id}-gen`, 0, -150, 0.72, false)}</g>`);
    if (t === "noon") put(L.glow, `<rect x="-1200" y="900" width="3500" height="400" fill="url(#zHaze)" opacity=".8"/>`);
    put(L.glow, `<g id="${id}-shim">${[0, 1, 2].map((i) => `<path d="M${-400 + i * 700},1380q200,-30 400,0t400,0" stroke="#fff6dc" stroke-width="6" fill="none" opacity=".25"/>`).join("")}</g>`);
  }

  // ---------------- first person at the generator: the red machine filling the frame, our hand on the starter handle (#id-hand, cord #id-cord), the bulb above (#id-bulb), the fan ----------------
  function genClose(L, o = {}) {
    const id = o.id || "gp";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#0e0f12"/>`);
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a2620"/><rect x="-1200" y="1150" width="3500" height="40" fill="#5a4630"/><rect x="-1200" y="1190" width="3500" height="1300" fill="#3a2e20"/>`);
    put(L.mid, `<rect x="-300" y="260" width="1680" height="620" rx="10" fill="#1f3f31" opacity=".85" ${OUT}/><rect x="-1000" y="300" width="300" height="520" fill="#0b1020" ${OUT}/>`);
    put(L.set, `${BULB(id, 540, 170)}${o.fan ? FAN(id, 540, 60) : ""}${Sets.props.generator(`${id}-gen`, 540, 1560, 1.55, false)}<path id="${id}-cord" d="M664,1343L760,1560" stroke="#1a1512" stroke-width="8" fill="none"/>`);
    put(L.fg, `<g id="${id}-hand" transform="translate(760,1560)"><g transform="rotate(-70) scale(0.75)">${Hand.grip({ skin: o.skin || "#b9805a", sleeve: o.sleeve || "#2c3e6b" })}</g><rect x="-44" y="-18" width="88" height="36" rx="12" fill="#2a2420" ${OUT}/></g>`);
    L.fg.classList.remove("fgblur");
    put(L.glow, `<g id="${id}-bulb" opacity="0"><circle cx="540" cy="200" r="900" fill="url(#fLamp)"/></g><circle id="${id}-pilot" cx="664" cy="1343" r="16" fill="#ff3b30" opacity="0"/>`);
  }

  // ---------------- น้องปั้น's drawing of day 101: the school at night, the light on the hill, five of them under the fan, a man lying at the gate ----------------
  function drawing2(L, o = {}) {
    const id = o.id || "dw";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = `<g transform="rotate(-2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="720" fill="#2f4a8a" opacity=".22" filter="url(#fCrayon)"/>`;   // the night sky, scribbled
    s += C("M240,520q40,-50 80,0", "#f4ecd8", 10) + `<circle cx="280" cy="520" r="44" fill="#f4ecd8" opacity=".8" filter="url(#fCrayon)"/>`;   // the moon
    s += C("M620,860Q740,700 880,760T930,860", "#5b6066", 14) + `<g id="${id}-hl"><circle cx="800" cy="720" r="22" fill="#f2c55c" filter="url(#fCrayon)"/>${C("M800,660v-40M760,680l-30,-30M840,680l30,-30M750,730h-50M850,730h50", "#f2c55c", 8)}</g>`;   // the hill and the light
    s += C("M150,1300H930", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M750,1300l0,-120M850,1300l0,-120M930,1300l0,-120M150,1180H930", "#5b6066", 8);
    s += C("M200,1140V860H640V1140M160,860L420,740L680,860M250,940h80v120h-80zM480,940h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="860" width="440" height="280" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    s += C("M420,780v60M380,820h80", "#2e2a26", 8);   // the fan on the roof line
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += fig(280, 1420, "#2f4a8a") + fig(380, 1430, "#c8392b") + fig(470, 1420, "#6f8f3e") + fig(560, 1430, "#d96a8a") + fig(640, 1450, "#e8b830", 0.7);
    s += `<g id="${id}-man" transform="translate(520,1240) rotate(-90)">${fig(0, 0, "#2e2a26", 0.65)}</g>`;   // the man lying across the gate
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 101 แสงบนเขา</text>`;
    s += `<text x="300" y="1560" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครูพิม ก้อง ลุง เจ๊ ปั้น</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ================= EP.3 "คนแปลกหน้า" =================
  // a kitchen knife in local coordinates: handle at the origin, blade along +x (so a Hand.grip at the origin holds it)
  const KNIFE = (id = "", s = 1) => `<g ${id ? `id="${id}"` : ""} transform="scale(${s})"><rect x="-150" y="-26" width="150" height="52" rx="12" fill="#3a2e22" ${OUT}/><path d="M-120,-26h30M-80,-26h30" stroke="#5a4a38" stroke-width="6"/><path d="M0,-30H330Q420,-30 460,-4L380,30H0Z" fill="#cfd4d8" ${OUT}/><path d="M0,0H370" stroke="#f4f6f8" stroke-width="6"/><path d="M10,-30H330Q400,-30 440,-8" stroke="#8d9299" stroke-width="4" fill="none"/></g>`;

  // ---------------- close-up of ภู's leg on the road: the cargo trouser, the gash with dirt in it (#id-gash, #id-dirt), the flap of cloth (#id-flap),
  // the pour of water (#id-pour), his own hand with a cloth (#id-hand), the bandage wrap (#id-wrap). o.time morning|day ----------------
  function woundClose(L, o = {}) {
    const id = o.id || "wd", t = o.time || "morning";
    sky(L, t);
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#fDirt)"/>${Array.from({ length: 40 }, (_, k) => { const r = mk(31 + k)(); return `<ellipse cx="${-1100 + ((k * 587) % 3400)}" cy="${-700 + ((k * 331) % 3300)}" rx="${18 + r * 30}" ry="${8 + r * 12}" fill="#8a6a42" opacity=".35"/>`; }).join("")}`);
    // the leg lies across the frame, lower-left to upper-right: a wide cargo trouser leg with a side pocket, the boot at the right
    let s = `<g transform="rotate(-18 540 1000)"><path d="M-400,700H1300V1300H-400Z" fill="#4a5560" ${OUT}/><path d="M-400,700H1300V760H-400Z" fill="#5c6974"/><path d="M-400,1240H1300V1300H-400Z" fill="#38424b"/>
      <path d="M-400,1000H1300" stroke="#3d4852" stroke-width="6" stroke-dasharray="40 30" opacity=".6"/><rect x="760" y="820" width="190" height="150" rx="10" fill="#5c6974" ${OUT}/><path d="M760,860h190" stroke="#2e2a26" stroke-width="4"/>
      <g transform="translate(1300,1000)"><path d="M0,-300Q160,-320 200,-140L240,300H0Z" fill="#1e1e1e" ${OUT}/><path d="M20,-240h140" stroke="#5b6066" stroke-width="10"/><path d="M30,-150h140M30,-70h140" stroke="#5b6066" stroke-width="10"/></g>`;
    // the gash: the cloth torn wide at the shin, the skin, a deep cut with dirt and rust-dark edges
    s += `<g id="${id}-flap"><path d="M180,780Q400,730 640,790Q560,1020 440,1230Q300,1150 160,1240Q130,1000 180,780Z" fill="#d39a6e" ${OUT}/>
      <path d="M180,780Q400,730 640,790" stroke="#2e2a26" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="30 14"/><path d="M640,790Q560,1020 440,1230" stroke="#2e2a26" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="30 14"/></g>
      <g id="${id}-skin"><path d="M200,790Q400,750 620,800Q550,1010 440,1210Q310,1140 180,1220Q150,1000 200,790Z" fill="#d39a6e"/><path d="M220,820q180,-30 360,10" stroke="#e8b48e" stroke-width="14" fill="none" opacity=".6"/></g>
      <g id="${id}-gash"><path d="M260,860Q400,960 560,1120" stroke="#5a0f0f" stroke-width="54" stroke-linecap="round" fill="none"/><path d="M260,860Q400,960 560,1120" stroke="#8f1b1b" stroke-width="28" stroke-linecap="round" fill="none"/><path d="M290,880Q400,960 540,1100" stroke="#c0392b" stroke-width="8" stroke-linecap="round" fill="none" opacity=".7"/>
      <path d="M280,910q-30,40 -16,90M520,1080q30,50 10,100M400,980q-40,30 -36,70" stroke="#8f1b1b" stroke-width="9" fill="none" opacity=".8" stroke-linecap="round"/></g>
      <g id="${id}-dirt">${[[300, 890], [340, 925], [390, 960], [430, 1000], [470, 1040], [510, 1082], [360, 905], [450, 985], [320, 950], [495, 1120]].map(([x, y], k) => `<circle cx="${x}" cy="${y}" r="${7 + (k % 3) * 3}" fill="#3a2a16"/>`).join("")}<path d="M330,870l10,-14M470,1010l14,-10M400,940l-12,-12" stroke="#6b4a2e" stroke-width="6" stroke-linecap="round"/><path d="M300,870q40,-12 80,0M440,1030q30,-14 60,0" stroke="#6b4a2e" stroke-width="4" fill="none" opacity=".8"/></g>
      <g id="${id}-pour" opacity="0"><path d="M400,420Q400,700 400,920" stroke="#9fd0ea" stroke-width="30" stroke-linecap="round" fill="none" opacity=".8"/><path d="M400,420Q400,700 400,920" stroke="#e8f6ff" stroke-width="10" stroke-linecap="round" fill="none"/>${[[340, 980], [460, 1010], [400, 1060], [520, 1100]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="30" ry="10" fill="#9fd0ea" opacity=".7"/>`).join("")}</g>
      <g id="${id}-wrap" opacity="0">${[0, 1, 2, 3, 4].map((k) => `<path d="M${120 + k * 95},${740 + k * 8}L${180 + k * 95},${1260 + k * 8}" stroke="#f4ecd8" stroke-width="70" stroke-linecap="butt"/>`).join("")}${[0, 1, 2, 3, 4].map((k) => `<path d="M${150 + k * 95},${740 + k * 8}L${210 + k * 95},${1260 + k * 8}" stroke="#d9d0bc" stroke-width="3"/>`).join("")}<path d="M560,800l40,-30M560,1180l40,30" stroke="#d9d0bc" stroke-width="6"/></g></g>`;
    put(L.set, s);
    // his own hand: a grip with a folded rag, coming in from the lower right (a rescue volunteer's hand)
    put(L.act, `<g id="${id}-hand" transform="translate(760,1300) rotate(-30) scale(0.7)" opacity="${o.hand ? 1 : 0}"><g transform="translate(-120,-40) rotate(20)"><rect x="-90" y="-60" width="180" height="120" rx="10" fill="#f4ecd8" ${OUT}/><path d="M-70,-30h140M-70,0h140M-70,30h140" stroke="#d9d0bc" stroke-width="3"/></g>${Hand.grip({ skin: "#d39a6e", sleeve: "#6b7a5a" })}</g>`);
    // the jerrycan of water above, tipped (its mouth where the pour starts)
    put(L.act, `<g id="${id}-can" transform="translate(440,300) rotate(55)" opacity="${o.can ? 1 : 0}"><rect x="-90" y="-130" width="180" height="260" rx="18" fill="#dfe6e2" ${OUT}/><rect x="-30" y="-170" width="60" height="50" rx="8" fill="#5b6066" ${OUT}/><path d="M-60,-60h120" stroke="#9fc5d8" stroke-width="10"/><text y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#2f4a8a" transform="rotate(-55)">น้ำ</text></g>`);
    if (t === "morning") put(L.glow, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#ffdca8" opacity=".08"/>`);
  }

  // ---------------- the drawing of day 102: six crayon figures inside the fence, ภู (grey-green) standing at the fence, and a black scribbled figure outside ----------------
  function drawing3(L, o = {}) {
    const id = o.id || "dw3";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = `<g transform="rotate(2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="720" fill="#2f4a8a" opacity=".22" filter="url(#fCrayon)"/>`;
    s += C("M240,520q40,-50 80,0", "#f4ecd8", 10) + `<circle cx="280" cy="520" r="44" fill="#f4ecd8" opacity=".8" filter="url(#fCrayon)"/>`;
    s += C("M200,1140V860H640V1140M160,860L420,740L680,860M250,940h80v120h-80zM480,940h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="860" width="440" height="280" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    // the fence: a long line with posts, running down the right side of the page
    s += C("M150,1300H930", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M750,1300l0,-120M850,1300l0,-120M930,1300l0,-120M150,1180H930", "#5b6066", 8);
    s += C("M700,1180V1560M760,1180V1560", "#5b6066", 8) + C("M700,1180h60M700,1320h60M700,1460h60", "#5b6066", 8);   // the gate bars, drawn tall
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += fig(230, 1440, "#2f4a8a") + fig(320, 1450, "#c8392b") + fig(410, 1440, "#6f8f3e") + fig(500, 1450, "#d96a8a") + fig(580, 1470, "#e8b830", 0.7);
    // ภู at the gate, inside, arm out through the bars; and the one outside, scribbled black, no face
    s += `<g id="${id}-phu">${fig(660, 1440, "#4e6a5a")}${C("M660,1360l80,-20", "#4e6a5a", 8)}</g>`;
    s += `<g id="${id}-dark"><g transform="translate(850,1430)" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="#2e2a26" stroke="#2e2a26" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="#2e2a26" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M-50,-170q30,-30 60,10q20,30 -10,60q-40,20 -70,-10q-20,-40 20,-60" stroke="#2e2a26" stroke-width="4" fill="none" opacity=".8"/><path d="M-30,-60q-30,30 -10,70M30,-60q30,30 10,70" stroke="#2e2a26" stroke-width="4" fill="none"/></g></g>`;
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 102 พี่ภู</text>`;
    s += `<text x="330" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครู ก้อง ลุง เจ๊ ปั้น พี่ภู</text><text id="${id}-who" x="850" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#2e2a26" filter="url(#fCrayon)">?</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  // ================= EP.4 "รั้วล้ม" =================
  // rain: a sheet of thin streaks in the foreground layer; flife drives .raind groups downward in a loop. o.n streaks, o.op opacity
  function rain(L, o = {}) {
    const n = o.n ?? 90, r = mk(o.seed || 17), op = o.op ?? 0.55;
    put(L.fg, `<g class="raind" opacity="${op}">${Array.from({ length: n }, () => { const x = -1200 + r() * 3500, y = -900 + r() * 2200, l = 60 + r() * 90; return `<path d="M${f1(x)},${f1(y)}l-14,${f1(l)}" stroke="#dfe8f0" stroke-width="${(2 + r() * 2).toFixed(1)}" stroke-linecap="round" opacity="${(0.35 + r() * 0.5).toFixed(2)}"/>`; }).join("")}</g>
      <g class="raind2" opacity="${op * 0.6}">${Array.from({ length: Math.floor(n * 0.6) }, () => { const x = -1200 + r() * 3500, y = -900 + r() * 2200, l = 40 + r() * 60; return `<path d="M${f1(x)},${f1(y)}l-10,${f1(l)}" stroke="#c9d6e0" stroke-width="1.6" stroke-linecap="round" opacity="${(0.3 + r() * 0.4).toFixed(2)}"/>`; }).join("")}</g>`);
    L.fg.classList.remove("fgblur");
    if (o.splash !== false) put(L.set, `<g class="rsplash">${Array.from({ length: 24 }, (_, k) => `<ellipse cx="${-1000 + ((k * 433) % 3200)}" cy="${1480 + ((k * 97) % 400)}" rx="${10 + (k % 3) * 6}" ry="4" fill="none" stroke="#dfe8f0" stroke-width="3" opacity="0"/>`).join("")}</g>`);
  }

  // ---------------- the back door of the school building, from inside the corridor at night: two wooden panels (#id-dl, #id-dr) that swing shut toward the middle,
  // the timber bar (#id-bar) that drops into its brackets, and through the opening the yard in the rain ----------------
  function backDoor(L, o = {}) {
    const id = o.id || "bd";
    sky(L, "night");
    // what is outside the door: the yard at night (dirt, the far fence line), rain
    put(L.far, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2c3a4c"/><circle cx="700" cy="300" r="90" fill="#dfe6e2" opacity=".8"/><circle cx="700" cy="300" r="300" fill="#9fb8d8" opacity=".16"/><rect x="-1200" y="1000" width="3500" height="1600" fill="#6b5a3e"/><path d="M-1200,1000H2300" stroke="#5b6066" stroke-width="30"/>`);
    put(L.mid, `<rect x="-1200" y="1180" width="3500" height="900" fill="#5a4630"/><ellipse cx="560" cy="1500" rx="700" ry="90" fill="#6b5a3e" opacity=".6"/>`);
    // the corridor wall around the door, the frame, the floor
    const W = 1080, DX = 300, DW = 480, DT = 420, DB = 1560;
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9cfb8" ${OUT}/><rect x="-1200" y="${DB}" width="3500" height="1200" fill="#8a6a42" ${OUT}/><path d="M-1200,${DB}H2300" stroke="#5a3d24" stroke-width="8"/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${-1200 + k * 300},${DB}L${-1300 + k * 300},2700" stroke="#5a3d24" stroke-width="4" opacity=".5"/>`).join("")}
      <rect x="-1200" y="${DT - 60}" width="3500" height="24" fill="#b3ada0"/><path d="M-1200,1300H${DX - 40}M${DX + DW + 40},1300H2300" stroke="#c4b99f" stroke-width="30"/>`;
    s = s.replace(`<rect x="-1200" y="-800" width="3500" height="3600" fill="#d9cfb8" ${OUT}/>`, `<path d="M-1200,-800H2300V2800H-1200Z M${DX - 40},${DT - 40}V${DB}H${DX + DW + 40}V${DT - 40}Z" fill="#d9cfb8" fill-rule="evenodd" ${OUT}/>`);
    put(L.set, s);
    // a hole in the wall: we see the night through it (the far/mid layers show through this rect because L.set is painted over them except here)
    // the panels: each a frame of planks with a cross brace; they hinge at the outer jambs and are drawn closed at translate(0)
    const panel = (pid, flip) => `<g id="${pid}" transform="translate(${flip ? DX + DW : DX},0) scale(${flip ? -1 : 1},1)"><g transform="translate(${flip ? -0 : 0},0)"><rect x="0" y="${DT}" width="${DW / 2}" height="${DB - DT}" fill="#6b4a2e" ${OUT}/>
      ${[0, 1, 2].map((k) => `<rect x="${12 + k * 76}" y="${DT + 12}" width="64" height="${DB - DT - 24}" fill="#7a5a3e" stroke="#4a3220" stroke-width="3"/>`).join("")}
      <path d="M14,${DT + 40}L${DW / 2 - 14},${DB - 40}" stroke="#4a3220" stroke-width="22"/><rect x="0" y="${(DT + DB) / 2 - 20}" width="${DW / 2}" height="40" fill="#5a3d24" ${OUT}/>
      <circle cx="${DW / 2 - 40}" cy="${(DT + DB) / 2 + 80}" r="18" fill="#3a3f45" ${OUT}/></g></g>`;
    put(L.act, `<g id="${id}-doors">${panel(`${id}-dl`, false)}${panel(`${id}-dr`, true)}</g>
      <g id="${id}-brk"><rect x="${DX - 70}" y="${(DT + DB) / 2 + 20}" width="60" height="110" rx="8" fill="#3a3f45" ${OUT}/><rect x="${DX + DW + 10}" y="${(DT + DB) / 2 + 20}" width="60" height="110" rx="8" fill="#3a3f45" ${OUT}/></g>
      <g id="${id}-bar" opacity="${o.barred ? 1 : 0}" transform="translate(0,${o.barred ? 0 : -500})"><rect x="${DX - 90}" y="${(DT + DB) / 2 + 36}" width="${DW + 180}" height="76" rx="10" fill="#8a6a42" ${OUT}/><path d="M${DX - 60},${(DT + DB) / 2 + 60}H${DX + DW + 60}" stroke="#5a3d24" stroke-width="6"/></g>`);
    // the open state: panels swung back (we animate them from open to closed with scaleX about their hinges)
    if (!o.closed) { const l = document.getElementById(`${id}-dl`), r = document.getElementById(`${id}-dr`); l.setAttribute("transform", `translate(${DX},0) scale(${o.open ?? 0.25},1)`); r.setAttribute("transform", `translate(${DX + DW},0) scale(${-(o.open ?? 0.25)},1)`); }
    put(L.glow, `<rect x="${DX - 40}" y="${DT - 40}" width="${DW + 80}" height="${DB - DT + 40}" fill="#9fb8d8" opacity=".14"/>`);
  }

  // ---------------- the drawing of day 103: the broken fence, five inside, ลุง standing beyond the fence; a small box with a face hanging on a post ----------------
  function drawing4(L, o = {}) {
    const id = o.id || "dw4";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#5a4630"/>`);
    let s = `<g transform="rotate(-1.5 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="720" fill="#2f4a8a" opacity=".3" filter="url(#fCrayon)"/>`;
    s += Array.from({ length: 30 }, (_, k) => C(`M${170 + (k * 97) % 760},${470 + (k * 53) % 600}l-8,40`, "#9fc5d8", 5)).join("");   // the rain, scribbled
    s += C("M200,1140V860H640V1140M160,860L420,740L680,860M250,940h80v120h-80zM480,940h80v120h-80z", "#c8392b", 10) + `<rect x="200" y="860" width="440" height="280" fill="#f6d6a0" opacity=".6" filter="url(#fCrayon)"/>`;
    s += C("M150,1300H700", "#6f8f3e", 14) + C("M150,1300l0,-120M250,1300l0,-120M350,1300l0,-120M450,1300l0,-120M150,1180H700", "#5b6066", 8);
    s += C("M700,1300l200,-60M720,1290l180,-120M760,1280l140,-20", "#5b6066", 8);   // the fence down, lying flat to the right
    const fig = (x, y, col, h = 1) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,-80l40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += fig(230, 1440, "#2f4a8a") + fig(320, 1450, "#c8392b") + fig(410, 1450, "#d96a8a") + fig(490, 1470, "#e8b830", 0.7) + fig(580, 1440, "#4e6a5a");
    s += `<g id="${id}-man">${fig(880, 1200, "#6f8f3e")}${C("M840,1080q40,-10 60,-40", "#6f8f3e", 8)}</g>`;   // ลุง beyond the fence, standing, his hat
    s += C("M860,1070q20,-30 40,0", "#e8b830", 8);
    s += `<g id="${id}-box"><rect x="640" y="1180" width="60" height="50" fill="#2e2a26" filter="url(#fCrayon)"/><path d="M652,1196h10M678,1196h10M655,1218q15,-12 30,0" stroke="#f4ecd8" stroke-width="4" fill="none"/>${C("M670,1180v-60", "#2e2a26", 5)}</g>`;   // the small box with a face, on a string
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 103 ฝนตก</text>`;
    s += `<text x="420" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#c8392b" filter="url(#fCrayon)">ครู ก้อง เจ๊ ปั้น พี่ภู</text><text x="880" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#6f8f3e" filter="url(#fCrayon)">ลุง</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }
  Object.assign(Sets, { backDoor, drawing4 });
  window.Fence.rain = rain;
  Object.assign(Sets, { woundClose, drawing3 });
  window.Fence.KNIFE = KNIFE;
  Object.assign(Sets, { fair, genClose, drawing2 });
  window.Fence.FAN = FAN; window.Fence.BULB = BULB;

})();
