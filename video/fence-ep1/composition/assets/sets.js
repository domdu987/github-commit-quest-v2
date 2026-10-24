// Layered set builders for the haunted-house episode. Each builder fills named layer groups
// (sky, far, mid, set, fg) so a scene can parallax them independently. Deterministic: seeded RNG only.
(function () {
  const OUT = 'stroke="#2e2a26" stroke-width="4" stroke-linejoin="round"';
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => { el.insertAdjacentHTML("beforeend", html); };

  const DEFS = `
    <linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1820"/><stop offset=".6" stop-color="#1b2f3a"/><stop offset="1" stop-color="#2a4350"/></linearGradient>
    <linearGradient id="duskSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a5e"/><stop offset=".55" stop-color="#c8786a"/><stop offset="1" stop-color="#f2b37a"/></linearGradient>
    <linearGradient id="daySky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc3d9"/><stop offset="1" stop-color="#e8efe6"/></linearGradient>
    <radialGradient id="sunhalo"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".7"/><stop offset="1" stop-color="#ffe2a8" stop-opacity="0"/></radialGradient>
    <radialGradient id="beacon"><stop offset="0" stop-color="#ff9a3c" stop-opacity=".9"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="moonhalo"><stop offset="0" stop-color="#f4ecd8" stop-opacity=".35"/><stop offset="1" stop-color="#f4ecd8" stop-opacity="0"/></radialGradient>
    <radialGradient id="lampglow"><stop offset="0" stop-color="#ffd58a" stop-opacity=".8"/><stop offset=".4" stop-color="#ffb35c" stop-opacity=".25"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient>
    <linearGradient id="beamg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe7b0" stop-opacity=".7"/><stop offset="1" stop-color="#ffe7b0" stop-opacity="0"/></linearGradient>
    <linearGradient id="fogg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9fb8bf" stop-opacity="0"/><stop offset=".5" stop-color="#9fb8bf" stop-opacity=".2"/><stop offset="1" stop-color="#9fb8bf" stop-opacity="0"/></linearGradient>
    <pattern id="planks" width="60" height="400" patternUnits="userSpaceOnUse"><rect width="60" height="400" fill="#5a4030"/><path d="M0,0V400" stroke="#2e2a26" stroke-width="4"/><path d="M14,40q8,30 0,70M38,210q6,26 0,60" stroke="#4a3426" stroke-width="3" fill="none"/></pattern>
    <pattern id="floorb" width="400" height="40" patternUnits="userSpaceOnUse"><rect width="400" height="40" fill="#4a3426"/><path d="M0,40H400" stroke="#2e2a26" stroke-width="3"/><path d="M130,0V40M330,0V40" stroke="#2e2a26" stroke-width="2" opacity=".6"/></pattern>
    <pattern id="netp" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M0,0H10M0,0V10" stroke="#e8e2d4" stroke-width="1" opacity=".55"/></pattern>
    <radialGradient id="cogas" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#c9c3b6" stop-opacity=".0"/><stop offset=".7" stop-color="#c9c3b6" stop-opacity=".0"/><stop offset="1" stop-color="#c9c3b6" stop-opacity="0"/></radialGradient>`;

  function trees(r, x0, x1, base, hMin, hMax, col, shade) {
    let s = "";
    for (let x = x0; x < x1; x += 60 + r() * 70) {
      const h = hMin + r() * (hMax - hMin), w = h * 0.42;
      s += `<path d="M${x},${base}V${base - h * 0.35}" stroke="${shade}" stroke-width="${w * 0.08}"/>`;
      s += `<ellipse cx="${x}" cy="${base - h * 0.62}" rx="${w * 0.55}" ry="${h * 0.38}" fill="${col}"/>`;
      s += `<ellipse cx="${x + w * 0.18}" cy="${base - h * 0.55}" rx="${w * 0.3}" ry="${h * 0.3}" fill="${shade}" opacity=".6"/>`;
    }
    return s;
  }
  function palms(r, x0, x1, base, col) {
    let s = "";
    for (let x = x0; x < x1; x += 260 + r() * 300) {
      const h = 420 + r() * 220, lean = -30 + r() * 60;
      s += `<path d="M${x},${base}Q${x + lean * 0.5},${base - h * 0.5} ${x + lean},${base - h}" stroke="${col}" stroke-width="18" fill="none"/>`;
      for (let k = 0; k < 7; k++) {
        const a = (k / 7) * Math.PI * 2, L = 150;
        s += `<path d="M${x + lean},${base - h}q${Math.cos(a) * L * 0.5},${-40} ${Math.cos(a) * L},${Math.sin(a) * L * 0.4 + 40}" stroke="${col}" stroke-width="14" fill="none" stroke-linecap="round"/>`;
      }
    }
    return s;
  }
  function stars(r, n) {
    let s = "";
    for (let i = 0; i < n; i++) s += `<circle cx="${r() * 1400 - 160}" cy="${r() * 900}" r="${0.8 + r() * 1.8}" fill="#f4ecd8" opacity="${0.3 + r() * 0.6}"/>`;
    return s;
  }

  // ---------------- exterior: old wooden house on stilts ----------------
  function houseExterior(L, opts = {}) {
    const r = mk(opts.seed || 11);
    put(L.sky, `<rect x="-200" y="0" width="1480" height="1920" fill="url(#nightsky)"/>${stars(r, 120)}
      <circle cx="${opts.moonX || 820}" cy="320" r="260" fill="url(#moonhalo)"/><circle cx="${opts.moonX || 820}" cy="320" r="62" fill="#f4ecd8"/>`);
    put(L.far, `<path d="M-300,1180Q0,980 300,1100T900,1060T1500,1120V1300H-300Z" fill="#1d3039"/>` + trees(r, -300, 1700, 1250, 160, 300, "#1a2c34", "#15242b"));
    put(L.mid, palms(r, -200, 1700, 1420, "#121f25") + trees(r, -260, 1700, 1440, 220, 420, "#142229", "#0f1b20"));
    // the house (stilts, stairs, verandah, gable roof); lit window can be toggled via #houseWin
    put(L.set, `
      <rect x="-200" y="1400" width="1480" height="520" fill="#14211a"/>
      <path d="M-200,1520Q400,1480 1280,1530V1920H-200Z" fill="#101a15"/>
      <g id="house" transform="translate(${opts.houseX || 140},0)">
        ${[0, 1, 2, 3, 4].map((i) => `<rect x="${20 + i * 160}" y="1060" width="26" height="380" fill="#3a2a20" ${OUT}/>`).join("")}
        <rect x="-20" y="740" width="760" height="330" fill="url(#planks)" ${OUT}/>
        <rect x="-40" y="1060" width="800" height="26" fill="#2e2219" ${OUT}/>
        <path d="M-90,760L350,470L790,760Z" fill="#3b2c22" ${OUT}/>
        <path d="M-90,760L350,470L790,760" fill="none" stroke="#5c4433" stroke-width="10"/>
        <path d="M330,520l20,-60l20,60" fill="#3b2c22" ${OUT}/>
        <g id="houseWin"><rect x="80" y="820" width="150" height="170" fill="#ffd58a" ${OUT}/><path d="M155,820V990M80,905H230" stroke="#2e2a26" stroke-width="6"/>
          <circle cx="155" cy="905" r="200" fill="url(#lampglow)" opacity=".6"/></g>
        <rect id="houseDoor" x="420" y="830" width="130" height="230" fill="#2a1e17" ${OUT}/>
        <rect x="600" y="830" width="110" height="140" fill="#1b2328" ${OUT}/>
        <path d="M560,1086L700,1440" stroke="#2e2219" stroke-width="22"/><path d="M620,1086L760,1440" stroke="#2e2219" stroke-width="22"/>
        ${[0, 1, 2, 3, 4, 5].map((i) => `<path d="M${572 + i * 23},${1120 + i * 52}h62" stroke="#3a2a20" stroke-width="12"/>`).join("")}
      </g>`);
    put(L.fg, `<path d="M-200,1920V1640Q-60,1560 60,1660Q120,1540 240,1620Q300,1700 360,1920Z" fill="#070d0a"/>
      <path d="M760,1920Q820,1640 960,1600Q1040,1580 1280,1640V1920Z" fill="#070d0a"/>
      <path d="M1280,-40C1120,90 980,140 820,150" stroke="#060b08" stroke-width="34" fill="none" stroke-linecap="round"/>` +
      [0, 1, 2, 3, 4, 5].map((i) => `<ellipse cx="${900 + i * 64}" cy="${150 - i * 16 + (i % 2) * 26}" rx="64" ry="24" fill="#08100c" transform="rotate(${-18 + i * 6} ${900 + i * 64} ${150 - i * 16})"/>`).join(""));
    return { ground: 1500 };
  }

  // ---------------- interior: bedroom with mosquito net ----------------
  function bedroom(L, opts = {}) {
    put(L.sky, `<rect x="-200" y="0" width="1480" height="1920" fill="#2a1f19"/>`);
    put(L.far, `<rect x="-200" y="0" width="1480" height="1500" fill="url(#planks)" opacity=".85"/>
      <g id="bedWin"><rect x="620" y="360" width="300" height="380" fill="#16252e" ${OUT}/><circle cx="830" cy="460" r="40" fill="#f4ecd8" opacity=".9"/>
      <path d="M770,360V740M620,550H920" stroke="#2e2a26" stroke-width="8"/>
      <path id="moonbeam" d="M620,360L920,360L760,1500L120,1500Z" fill="#cfe2e6" opacity=".08"/></g>
      <rect x="-200" y="1480" width="1480" height="440" fill="url(#floorb)"/>`);
    put(L.mid, `<g id="lamp"><rect x="110" y="1300" width="60" height="70" rx="8" fill="#6b5a4a" ${OUT}/><path d="M118,1300q22,-60 44,0z" fill="#ffd58a" ${OUT}/>
        <circle id="lampHalo" cx="140" cy="1280" r="320" fill="url(#lampglow)" opacity=".7"/></g>
      <rect x="-60" y="1370" width="320" height="40" fill="#4a3426" ${OUT}/>`);
    put(L.set, `<g id="net"><path d="M300,560H1040L1080,1500H260Z" fill="url(#netp)" stroke="#e8e2d4" stroke-width="3" opacity=".75"/>
        <path d="M300,560L260,1500M1040,560L1080,1500" stroke="#e8e2d4" stroke-width="4" opacity=".6"/></g>
      <rect x="280" y="1440" width="780" height="70" rx="10" fill="#c9b98f" ${OUT}/>
      <rect x="320" y="1410" width="160" height="50" rx="18" fill="#e6d9bd" ${OUT}/>`);
    put(L.fg, `<rect x="-200" y="1780" width="1480" height="200" fill="#120c09"/><path d="M-200,-20H1280V60H-200Z" fill="#120c09"/>
      <rect x="-30" y="-20" width="80" height="1960" fill="#120c09"/>`);
    return { ground: 1500 };
  }

  // ---------------- interior: back room / kitchen with the generator ----------------
  function backroom(L, opts = {}) {
    put(L.sky, `<rect x="-200" y="0" width="1480" height="1920" fill="#241b16"/>`);
    put(L.far, `<rect x="-200" y="0" width="1480" height="1500" fill="url(#planks)" opacity=".75"/>
      <rect x="760" y="520" width="200" height="160" fill="#16252e" ${OUT}/><path id="shutter" d="M760,520h200v160h-200z" fill="#3b2c22" ${OUT}/>
      <rect x="-200" y="1480" width="1480" height="440" fill="url(#floorb)"/>`);
    put(L.mid, `<rect x="40" y="1120" width="420" height="380" fill="#3b2c22" ${OUT}/><rect x="70" y="1150" width="160" height="110" fill="#2a1e17" ${OUT}/><rect x="270" y="1150" width="160" height="110" fill="#2a1e17" ${OUT}/>
      <g id="pots"><ellipse cx="160" cy="1110" rx="70" ry="18" fill="#6b5a4a" ${OUT}/><rect x="96" y="1050" width="130" height="62" rx="12" fill="#7a6a58" ${OUT}/></g>`);
    put(L.set, `<g id="generator"><rect x="560" y="1290" width="300" height="200" rx="18" fill="#c0603e" ${OUT}/>
        <rect x="590" y="1320" width="150" height="90" rx="8" fill="#2e2a26"/><circle cx="790" cy="1350" r="22" fill="#e6d9bd" ${OUT}/>
        <rect x="770" y="1400" width="70" height="30" rx="6" fill="#e6d9bd" ${OUT}/><path d="M860,1330h40v-60" stroke="#2e2a26" stroke-width="12" fill="none" stroke-linecap="round"/>
        <g id="exhaust">${[0, 1, 2, 3, 4].map((i) => `<circle class="puff" cx="${900 + i * 18}" cy="${1250 - i * 70}" r="${26 + i * 10}" fill="#bdb5a6" opacity="${0.35 - i * 0.05}"/>`).join("")}</g></g>`);
    put(L.fg, `<rect x="-200" y="1780" width="1480" height="200" fill="#100b08"/><rect x="1000" y="-20" width="120" height="1960" fill="#100b08"/>`);
    return { ground: 1500 };
  }

  // ---------------- verandah / doorway at night ----------------
  function verandah(L, opts = {}) {
    const r = mk(opts.seed || 5);
    put(L.sky, `<rect x="-200" y="0" width="1480" height="1920" fill="url(#nightsky)"/>${stars(r, 90)}<circle cx="240" cy="300" r="50" fill="#f4ecd8"/><circle cx="240" cy="300" r="200" fill="url(#moonhalo)"/>`);
    put(L.far, trees(r, -300, 1600, 1250, 200, 420, "#15252d", "#101d23") + palms(r, -100, 1600, 1300, "#0f1a1f"));
    put(L.mid, `<rect x="-200" y="1300" width="1480" height="210" fill="#0f191e"/><rect x="-200" y="1250" width="1480" height="60" fill="#2e2219" ${OUT}/>
      ${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<rect x="${-120 + i * 170}" y="1020" width="20" height="240" fill="#3a2a20" ${OUT}/>`).join("")}
      <path d="M-200,1060H1280" stroke="#3a2a20" stroke-width="16"/>`);
    put(L.set, `<rect x="-200" y="1500" width="1480" height="420" fill="url(#floorb)"/><rect x="-200" y="1490" width="1480" height="16" fill="#2e2219"/>
      <rect id="vDoor" x="720" y="380" width="300" height="1120" fill="#1a1310" ${OUT}/><rect id="vDoorLeaf" x="720" y="380" width="300" height="1120" fill="#3a2a20" ${OUT}/>
      <rect x="690" y="350" width="360" height="40" fill="#2e2219" ${OUT}/>`);
    put(L.fg, `<rect x="-60" y="-20" width="110" height="1960" fill="#0d0907"/><path d="M-200,1840H1280V1960H-200Z" fill="#0d0907"/>`);
    return { ground: 1500 };
  }


  // ---------------- exterior: big old two-storey teak mansion ("gingerbread" house) ----------------
  function fret(x0, x1, y, r, col) { // scalloped fretwork under the eaves
    let d = "";
    for (let x = x0; x < x1; x += r * 2) d += `M${x},${y}a${r},${r} 0 0 0 ${r * 2},0`;
    return `<path d="${d}" fill="none" stroke="${col}" stroke-width="5"/>` +
      `<path d="M${x0},${y}H${x1}" stroke="${col}" stroke-width="8"/>`;
  }
  function shutterWin(x, y, w, h, lit, id) {
    const glass = lit ? "#ffd58a" : "#1b2328";
    return `<g${id ? ` id="${id}"` : ""}><rect x="${x - 6}" y="${y - 26}" width="${w + 12}" height="22" fill="#3b2c22" ${OUT}/>
      <path d="M${x - 6},${y - 26}l${(w + 12) / 2},-22l${(w + 12) / 2},22z" fill="#3b2c22" ${OUT}/>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${glass}" ${OUT}/>
      <path d="M${x + w / 2},${y}V${y + h}" stroke="#2e2a26" stroke-width="5"/>
      ${lit ? `<circle cx="${x + w / 2}" cy="${y + h / 2}" r="${h}" fill="url(#lampglow)" opacity=".55"/>` : ""}
      <rect x="${x - w * 0.42}" y="${y}" width="${w * 0.4}" height="${h}" fill="#5a4030" ${OUT}/>
      <rect x="${x + w * 1.02}" y="${y}" width="${w * 0.4}" height="${h}" fill="#5a4030" ${OUT} transform="rotate(4 ${x + w} ${y})"/>
      ${[0.2, 0.4, 0.6, 0.8].map((k) => `<path d="M${x - w * 0.4},${y + h * k}h${w * 0.36}M${x + w * 1.04},${y + h * k}h${w * 0.36}" stroke="#3b2c22" stroke-width="3"/>`).join("")}</g>`;
  }
  function balusters(x0, x1, y, h, col) {
    let s = `<path d="M${x0},${y}H${x1}M${x0},${y + h}H${x1}" stroke="${col}" stroke-width="10"/>`;
    for (let x = x0 + 10; x < x1; x += 26) s += `<rect x="${x}" y="${y}" width="10" height="${h}" fill="${col}"/>`;
    return s;
  }
  function banyan(x, base) {
    let s = `<path d="M${x - 60},${base}C${x - 40},${base - 300} ${x - 70},${base - 520} ${x - 10},${base - 700}L${x + 40},${base - 700}C${x + 60},${base - 500} ${x + 40},${base - 300} ${x + 70},${base}Z" fill="#0f1a16"/>`;
    for (let i = 0; i < 6; i++) s += `<ellipse cx="${x - 260 + i * 110}" cy="${base - 760 - (i % 2) * 70}" rx="190" ry="120" fill="${i % 2 ? "#0c1612" : "#101d18"}"/>`;
    for (let i = 0; i < 14; i++) { const rx = x - 300 + i * 46; s += `<path d="M${rx},${base - 700}q${(i % 3) * 6 - 6},${200 + (i % 4) * 60} ${(i % 2 ? 8 : -8)},${360 + (i % 5) * 50}" stroke="#0f1a16" stroke-width="5" fill="none"/>`; }
    return s;
  }
  function mansionExterior(L, opts = {}) {
    const r = mk(opts.seed || 21);
    const T = "#5a4030", D = "#3b2c22", W = "#4a3426";
    const tod = opts.time || "night";
    const SKY = { night: "url(#nightsky)", dusk: "url(#duskSky)", day: "url(#daySky)" }[tod];
    const HILL = { night: "#1b2d36", dusk: "#6a4a52", day: "#7fa58a" }[tod];
    const TREE = { night: ["#18282f", "#132127"], dusk: ["#4a3440", "#3a2834"], day: ["#5f8a6a", "#4e7558"] }[tod];
    const PALM = { night: "#111d22", dusk: "#2e2026", day: "#3f5e47" }[tod];
    put(L.sky, `<rect x="-400" y="0" width="1880" height="1920" fill="${SKY}"/>` + (tod === "night" ? `${stars(r, 140)}
      <circle cx="${opts.moonX || 880}" cy="250" r="240" fill="url(#moonhalo)"/><circle cx="${opts.moonX || 880}" cy="250" r="56" fill="#f4ecd8"/>` :
      tod === "dusk" ? `<circle cx="820" cy="980" r="320" fill="url(#sunhalo)"/><circle cx="820" cy="980" r="90" fill="#ffcf8a"/>` :
      `<circle cx="860" cy="260" r="280" fill="url(#sunhalo)" opacity=".6"/><ellipse cx="300" cy="300" rx="180" ry="50" fill="#f4f1e6" opacity=".8"/><ellipse cx="760" cy="420" rx="140" ry="40" fill="#f4f1e6" opacity=".7"/>`));
    put(L.far, `<path d="M-400,1160Q0,1000 360,1090T1000,1050T1700,1100V1320H-400Z" fill="${HILL}"/>` + trees(r, -400, 1800, 1260, 180, 320, TREE[0], TREE[1]));
    put(L.mid, palms(r, -300, 1800, 1430, PALM));
    const X = opts.houseX ?? -60; // the house is wider than the frame; scenes pan across it
    put(L.set, `
      <rect x="-400" y="1440" width="1880" height="480" fill="${{ night: "#121d17", dusk: "#3b3a2a", day: "#6f8f4f" }[tod]}"/>
      <path d="M-400,1530Q300,1490 1480,1540V1920H-400Z" fill="${{ night: "#0e1712", dusk: "#2e2c20", day: "#5e7c42" }[tod]}"/>
      <g id="house" transform="translate(${X},${opts.houseY || 0}) scale(${opts.houseScale || 1})">
        <!-- brick base with arches -->
        <rect x="0" y="1360" width="1200" height="110" fill="#6b4a3a" ${OUT}/>
        ${[0, 1, 2, 3, 4, 5].map((i) => `<path d="M${40 + i * 200},1470v-60a40,40 0 0 1 80,0v60z" fill="#1a1310" ${OUT}/>`).join("")}
        <!-- ground floor -->
        <rect x="20" y="1040" width="1160" height="330" fill="url(#planks)" ${OUT}/>
        <rect x="0" y="1340" width="1200" height="26" fill="${D}" ${OUT}/>
        ${shutterWin(110, 1110, 90, 170, false)}${shutterWin(330, 1110, 90, 170, false)}${shutterWin(870, 1110, 90, 170, false)}${shutterWin(1050, 1110, 70, 170, false)}
        <rect id="houseDoor" x="530" y="1080" width="160" height="270" fill="#2a1e17" ${OUT}/><path d="M530,1080a80,80 0 0 1 160,0" fill="${D}" ${OUT}/>
        <!-- ground-floor verandah posts + railing -->
        ${[0, 1, 2, 3, 4, 5, 6].map((i) => `<rect x="${10 + i * 196}" y="1020" width="22" height="330" fill="${D}" ${OUT}/>`).join("")}
        ${balusters(0, 470, 1270, 70, D)}${balusters(750, 1200, 1270, 70, D)}
        <!-- first-floor eave + fretwork -->
        <path d="M-50,1040H1250L1210,990H-10Z" fill="${D}" ${OUT}/>${fret(-40, 1240, 1046, 16, "#c9b98f")}
        <!-- upper floor -->
        <rect x="60" y="720" width="1080" height="290" fill="url(#planks)" ${OUT}/>
        ${shutterWin(150, 780, 80, 170, false)}${shutterWin(340, 780, 80, 170, true, "winLit")}${shutterWin(780, 780, 80, 170, false, "winDark")}${shutterWin(970, 780, 80, 170, false)}
        <!-- central balcony -->
        <rect x="500" y="760" width="220" height="250" fill="#2a1e17" ${OUT}/>${balusters(470, 750, 930, 80, D)}<rect x="460" y="1006" width="300" height="20" fill="${D}" ${OUT}/>
        <!-- roofs: two side gables and a tall central gable -->
        <path d="M20,730L250,470L480,730Z" fill="${D}" ${OUT}/><path d="M720,730L950,470L1180,730Z" fill="${D}" ${OUT}/>
        <path d="M-40,740H1240L1180,700H20Z" fill="${W}" ${OUT}/>${fret(-30, 1230, 744, 14, "#c9b98f")}
        <path d="M400,720L610,330L820,720Z" fill="#33251c" ${OUT}/><path d="M440,700L610,390L780,700" fill="none" stroke="#c9b98f" stroke-width="6"/>
        <circle cx="610" cy="560" r="44" fill="#1b2328" ${OUT}/><path d="M610,516V604M566,560H654" stroke="#2e2a26" stroke-width="5"/>
        <path d="M600,330l10,-50l10,50" fill="${D}" ${OUT}/>
        <!-- grand front stairs -->
        <path d="M520,1366H700L780,1500H440Z" fill="#4a3426" ${OUT}/>
        ${[0, 1, 2, 3].map((i) => `<path d="M${508 - i * 20},${1394 + i * 30}H${712 + i * 20}" stroke="#2e2a26" stroke-width="5"/>`).join("")}
      </g>
      ${banyan(opts.banyanX ?? 1320, 1470)}`);
    put(L.fg, `<g id="gate"><rect x="-80" y="1180" width="40" height="740" fill="#0a0f0c"/><rect x="250" y="1180" width="40" height="740" fill="#0a0f0c"/>
        <path d="M-40,1260H250M-40,1420H250" stroke="#0a0f0c" stroke-width="12"/>${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<path d="M${-30 + i * 36},1240V1720" stroke="#0a0f0c" stroke-width="8"/><path d="M${-30 + i * 36},1240l-8,-26h16z" fill="#0a0f0c"/>`).join("")}</g>
      <path d="M700,1920Q760,1660 920,1640Q1060,1620 1480,1700V1920Z" fill="#060b08"/>
      <path d="M1480,-40C1300,90 1150,140 960,150" stroke="#060b08" stroke-width="34" fill="none" stroke-linecap="round"/>` +
      [0, 1, 2, 3, 4, 5].map((i) => `<ellipse cx="${1040 + i * 64}" cy="${150 - i * 16 + (i % 2) * 26}" rx="64" ry="24" fill="#08100c" transform="rotate(${-18 + i * 6} ${1040 + i * 64} ${150 - i * 16})"/>`).join(""));
    return { ground: 1500 };
  }

  // ---------------- interior: grand hall with staircase ----------------
  function hall(L, opts = {}) {
    put(L.sky, `<rect x="-400" y="0" width="1880" height="1920" fill="#20170f"/>`);
    put(L.far, `<rect x="-400" y="0" width="1880" height="1500" fill="url(#planks)" opacity=".8"/>
      ${[0, 1, 2].map((i) => `<g><rect x="${-200 + i * 520}" y="380" width="200" height="260" fill="#6b4a3a" ${OUT}/><rect x="${-180 + i * 520}" y="400" width="160" height="220" fill="#2a1e17"/>
        <ellipse cx="${-100 + i * 520}" cy="480" rx="40" ry="50" fill="#3b2c22"/><path d="M${-160 + i * 520},620q60,-90 120,0" fill="#3b2c22"/></g>`).join("")}
      <rect x="-400" y="1480" width="1880" height="440" fill="url(#floorb)"/>`);
    put(L.mid, `<g id="stairs"><path d="M700,1500L1300,700H1480V1500Z" fill="#3b2c22" ${OUT}/>
        ${Array.from({ length: 14 }, (_, i) => `<path d="M${700 + i * 43},${1500 - i * 57}h60v57" fill="none" stroke="#2e2a26" stroke-width="5"/>`).join("")}
        <path d="M660,1380L1260,580" stroke="#2e2a26" stroke-width="16"/>
        ${Array.from({ length: 12 }, (_, i) => `<path d="M${690 + i * 48},${1350 - i * 64}v120" stroke="#3b2c22" stroke-width="10"/>`).join("")}</g>`);
    put(L.set, `<g id="chandelier"><path d="M300,0V180" stroke="#2e2a26" stroke-width="6"/><path d="M200,200q100,80 200,0" fill="none" stroke="#2e2a26" stroke-width="10"/>
        ${[0, 1, 2, 3, 4].map((i) => `<rect x="${206 + i * 46}" y="${180 + (i % 2) * 10}" width="8" height="26" fill="#e6d9bd"/>`).join("")}</g>
      <rect x="-60" y="1300" width="300" height="200" fill="#4a3426" ${OUT}/><rect x="-40" y="1320" width="260" height="20" fill="#3b2c22"/>`);
    put(L.fg, `<rect x="-400" y="1800" width="1880" height="200" fill="#0f0a07"/><rect x="-60" y="-20" width="120" height="1960" fill="#0f0a07"/>`);
    return { ground: 1500 };
  }


  // ---------------- props ----------------
  const props = {
    generator(id, x, y, s = 1, running = true) {
      return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-180,0V-250q0,-30 30,-30h300q30,0 30,30V0" fill="none" stroke="#3a3f45" stroke-width="16" stroke-linejoin="round"/><path d="M-180,-120h360" stroke="#3a3f45" stroke-width="12"/>
        <rect x="-150" y="-200" width="300" height="200" rx="18" fill="#c0603e" ${OUT}/><rect x="-150" y="-200" width="300" height="34" rx="10" fill="#8a3f2a" ${OUT}/><rect x="-40" y="-236" width="80" height="40" rx="8" fill="#2e2a26" ${OUT}/><circle cx="0" cy="-216" r="12" fill="#5b6066"/>
        <rect x="-120" y="-170" width="150" height="90" rx="8" fill="#2e2a26"/><rect x="-108" y="-158" width="60" height="30" rx="4" fill="#1a1512"/><circle cx="80" cy="-140" r="22" fill="#e6d9bd" ${OUT}/><circle cx="80" cy="-140" r="12" fill="#2e2a26"/><path d="M80,-140l8,-10" stroke="#c8392b" stroke-width="3"/>
        <path d="M150,-170h30v-40q0,-14 14,-14h20" fill="none" stroke="#5b6066" stroke-width="12" stroke-linecap="round"/><rect x="100" y="-60" width="46" height="26" rx="6" fill="#5b6066" ${OUT}/>
        <rect x="60" y="-90" width="70" height="30" rx="6" fill="#e6d9bd" ${OUT}/><path d="M150,-160h40v-60" stroke="#2e2a26" stroke-width="12" fill="none" stroke-linecap="round"/>
        <rect x="-130" y="-8" width="40" height="16" rx="6" fill="#2e2a26"/><rect x="90" y="-8" width="40" height="16" rx="6" fill="#2e2a26"/>
        <g id="${id}-shim" opacity="${running ? 0.35 : 0}">${[0, 1, 2].map((i) => `<path d="M${180 + i * 14},-230q-12,-30 0,-60t0,-60" stroke="#e8efe6" stroke-width="3" fill="none" opacity=".5"/>`).join("")}</g></g>`;
    },
    landlady(id, x, y, s = 1, umbrella = false) {
      return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-55,0C-62,-150 -50,-300 -30,-360H30C50,-300 62,-150 55,0Z" fill="#1a1512"/>
        <ellipse cx="0" cy="-400" rx="36" ry="42" fill="#1a1512"/><ellipse cx="0" cy="-444" rx="26" ry="16" fill="#1a1512"/>
        <g id="${id}-arm"><path d="M30,-330Q90,-300 130,-340" stroke="#1a1512" stroke-width="26" fill="none" stroke-linecap="round"/></g>
        ${umbrella ? `<path d="M-160,-470Q0,-600 160,-470Z" fill="#2a2420"/><path d="M0,-560V-330" stroke="#2a2420" stroke-width="8"/>` : ""}</g>`;
    },
    ghostSeated(id, x, y, s = 1) {
      return `<g id="${id}" transform="translate(${x},${y}) scale(${s})" opacity="0">
        <path d="M-80,0Q-90,-120 -50,-220Q0,-250 50,-220Q90,-120 80,0Z" fill="#0b0f12" opacity=".9" stroke="#cfdcd8" stroke-width="3" stroke-opacity=".35"/>
        <ellipse cx="0" cy="-280" rx="44" ry="52" fill="#0b0f12" opacity=".95" stroke="#cfdcd8" stroke-width="3" stroke-opacity=".35"/>
        <path d="M-46,-300Q-70,-160 -40,-90M46,-300Q70,-160 40,-90M-30,-320Q-50,-150 -10,-70M30,-320Q50,-150 10,-70" stroke="#0b0f12" stroke-width="22" fill="none" opacity=".85" stroke-linecap="round"/>
        <g id="${id}-face" opacity="0"><ellipse cx="-14" cy="-284" rx="6" ry="3" fill="#dfe7e4"/><ellipse cx="14" cy="-284" rx="6" ry="3" fill="#dfe7e4"/></g></g>`;
    },
    bench(x, y, s = 1) {
      return `<g transform="translate(${x},${y}) scale(${s})"><rect x="-260" y="-130" width="520" height="34" rx="8" fill="#6b4a3a" ${OUT}/><rect x="-240" y="-96" width="24" height="96" fill="#4a3426" ${OUT}/><rect x="216" y="-96" width="24" height="96" fill="#4a3426" ${OUT}/></g>`;
    },
    mat(x, y, w = 420) {
      return `<rect x="${x}" y="${y - 24}" width="${w}" height="30" rx="8" fill="#9c7a52" ${OUT}/><path d="M${x + 20},${y - 9}h${w - 40}" stroke="#7a5c3c" stroke-width="4"/>`;
    },
    rain(id, n = 140, seed = 3) {
      const r = mk(seed);
      let d = "";
      for (let i = 0; i < n; i++) { const x = r() * 1600 - 260, y = r() * 2400 - 300, l = 50 + r() * 70; d += `M${x},${y}l${-l * 0.18},${l}`; }
      return `<g id="${id}"><path d="${d}" stroke="#b9cdd3" stroke-width="3" opacity=".45" stroke-linecap="round"/><path d="${d}" transform="translate(0,-2400)" stroke="#b9cdd3" stroke-width="3" opacity=".45" stroke-linecap="round"/></g>`;
    },
    beacon(id, x, y) {
      return `<g id="${id}" transform="translate(${x},${y})"><rect x="-140" y="-90" width="280" height="90" rx="14" fill="#e6d9bd" ${OUT}/><rect x="-120" y="-150" width="160" height="70" rx="10" fill="#e6d9bd" ${OUT}/>
        <rect x="-110" y="-140" width="60" height="44" fill="#1b2328"/><circle cx="-80" cy="10" r="30" fill="#2e2a26"/><circle cx="90" cy="10" r="30" fill="#2e2a26"/>
        <rect x="-60" y="-170" width="70" height="18" rx="6" fill="#ff9a3c" ${OUT}/><circle id="${id}-glow" cx="-25" cy="-160" r="260" fill="url(#beacon)" opacity=".8"/></g>`;
    },
    shadowSweep(id) {
      return `<ellipse id="${id}" cx="-300" cy="900" rx="170" ry="520" fill="#05080a" opacity="0"/>`;
    },
  };

  window.Sets = { DEFS, houseExterior, mansionExterior, hall, bedroom, backroom, verandah, props };
})();
