// บางระจัน แบต 3% · sets in the channel look (layered depth, both frames). Ground for people: y 1400. Load after jkset.js.
//   Sets.brField(L, o)  the paddy field at dawn: mist, a low sun, palm trees, paddy rows, a dike path; two bushes (#id-bush1 at x 300, #id-bush2 at x 1300)
//   Sets.brCamp(L, o)   the camp: bamboo stockade across the back (gate x 1000…1200), huts on stilts, the granary (x 1450…1750, floor y 1000, room underneath),
//                       the kitchen left (stove + pot at 330, mortar at 520, baskets), the tying pole at x 760 (o.pole), torch posts at x 60 and 1300 (o.torches: lit),
//                       a long drum at 1100 (o.drum), a water jar at 1850 · o.night (moon, dark blue), o.fog (fog bands), o.limes (the lime battery ring around the plaza),
//                       o.offerings (bananas, sticky rice, bowls before the pole), o.enemy (n torch silhouettes beyond the stockade, #id-enemy)
//   Sets.brRoom(L, o)   2569: a bedroom (bed x 300…1000 top y 1300, window, poster, door x 1400…1640) · o.kitchen: the kitchen cupboard on legs with a basket of limes under it
(function () {
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}>${text}</text>`;
  Sets.DEFS += `
    <linearGradient id="brDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6aa8"/><stop offset=".3" stop-color="#c8a0b0"/><stop offset=".55" stop-color="#f6b88a"/><stop offset=".8" stop-color="#ffe2b0"/><stop offset="1" stop-color="#fff0d0"/></linearGradient>
    <linearGradient id="brDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a9ad8"/><stop offset=".5" stop-color="#a8ccec"/><stop offset=".85" stop-color="#ecdcb8"/><stop offset="1" stop-color="#f4e4c0"/></linearGradient>
    <linearGradient id="brNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#080c22"/><stop offset=".5" stop-color="#16204a"/><stop offset=".85" stop-color="#2a3860"/><stop offset="1" stop-color="#3a4668"/></linearGradient>
    <linearGradient id="brFog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8ecf0" stop-opacity="0"/><stop offset=".5" stop-color="#e8ecf0" stop-opacity=".55"/><stop offset="1" stop-color="#e8ecf0" stop-opacity="0"/></linearGradient>
    <linearGradient id="brThatch" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8a860"/><stop offset="1" stop-color="#8a6a34"/></linearGradient>
    <linearGradient id="brWater" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfe4ec" stop-opacity=".0"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#cfe4ec" stop-opacity="0"/></linearGradient>
    <radialGradient id="brMoon"><stop offset="0" stop-color="#fff8e0"/><stop offset=".3" stop-color="#e8f0ff" stop-opacity=".5"/><stop offset="1" stop-color="#c8d8ff" stop-opacity="0"/></radialGradient>
    <pattern id="brMesh" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0,6H12M6,0V12" stroke="#5a4a3a" stroke-width="1.2" opacity=".6"/></pattern>`;

  const palm = (x, y, s, c = "#2a4a30") => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-10,0Q-6,-180 10,-300" stroke="${c}" stroke-width="16" fill="none" stroke-linecap="round"/>
    ${[-150, -110, -70, -30, 10, 50].map((a) => `<path d="M10,-300q${Math.cos(a * Math.PI / 180) * 90},${Math.sin(a * Math.PI / 180) * 90 - 20} ${Math.cos(a * Math.PI / 180) * 170},${Math.sin(a * Math.PI / 180) * 170 + 40}" stroke="${c}" stroke-width="12" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
  const bamboo = (x, y, s, c = "#3a6a3a") => `<g transform="translate(${x},${y}) scale(${s})">${[-24, 0, 22].map((dx, k) => `<path d="M${dx},0Q${dx - 10},-200 ${dx + 14 - k * 10},-380" stroke="${c}" stroke-width="7" fill="none"/>${[-300, -220, -140].map((yy) => `<path d="M${dx - 4 + k * 2},${yy}q30,-30 70,-20M${dx - 4 + k * 2},${yy}q-30,-30 -70,-14" stroke="${c}" stroke-width="4" fill="none"/>`).join("")}`).join("")}</g>`;
  const bush = (x, y, s, c = "#4a8a3a", id = "") => `<g${id ? ` id="${id}"` : ""} transform="translate(${x},${y}) scale(${s})"><ellipse cy="-70" rx="150" ry="90" fill="${c}"/><ellipse cx="-70" cy="-110" rx="90" ry="70" fill="${c}"/><ellipse cx="60" cy="-130" rx="100" ry="80" fill="${c}"/><ellipse cx="-20" cy="-150" rx="70" ry="60" fill="#5a9a46"/><ellipse cx="80" cy="-90" rx="60" ry="40" fill="#3a7a30" opacity=".7"/></g>`;
  const grassTuft = (x, y, s, c = "#6a9a3a") => `<g transform="translate(${x},${y}) scale(${s})">${[-30, -15, 0, 15, 30].map((dx, k) => `<path d="M${dx * 0.3},0Q${dx},-40 ${dx * 1.6},-80" stroke="${c}" stroke-width="5" fill="none" stroke-linecap="round"/>`).join("")}</g>`;

  window.BRS = { palm, bamboo, bush, grassTuft };
  // ---------------- the paddy field at dawn ----------------
  Sets.brField = (L, o = {}) => {
    const id = o.id || "brf", r = mk(o.seed || 5);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#ffe2b0"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#brDawn)"/>
      <circle cx="1500" cy="760" r="340" fill="url(#jkSun)" opacity=".9"/><circle cx="1500" cy="760" r="70" fill="#fff6d8"/>`);
    let far = `<path d="M-2400,900L-1800,780L-1200,860L-600,760L0,840L600,740L1200,820L1800,760L2400,840L3000,780L3800,860V1100H-2400Z" fill="#9aa8c0" opacity=".8"/>
      <path d="M-2400,980L-1600,900L-900,960L-200,890L500,950L1200,900L1900,960L2700,900L3800,960V1150H-2400Z" fill="#8aa090" opacity=".85"/>`;
    [[-700, 1000, 0.8], [-300, 1010, 0.6], [1900, 1000, 0.9], [2300, 1010, 0.7], [3100, 1000, 0.8]].forEach(([x, y, s]) => (far += palm(x, y, s, "#4a6a50")));
    far += `<rect x="-2400" y="880" width="6200" height="300" fill="url(#jkHazeW)" opacity=".9"/>`;
    put(L.far, far);
    let mid = "";
    for (let k = 0; k < 7; k++) { const y = 1000 + k * 46, h = 46; mid += `<rect x="-2400" y="${y}" width="6200" height="${h}" fill="${k % 2 ? "#8ab85a" : "#9ec868"}"/><rect x="-2400" y="${y + h - 12}" width="6200" height="10" fill="#cfe4ec" opacity=".5"/><rect x="${-2000 + (k * 700) % 3000}" y="${y + h - 12}" width="900" height="10" fill="url(#brWater)"/>`; }
    mid += `<path d="M-2400,1330L3800,1330" stroke="#8a7a4a" stroke-width="12"/><path d="M400,1330L1000,1000M1700,1330L1300,1000" stroke="#9a8a5a" stroke-width="10" opacity=".7"/>`;
    mid += [...Array(40)].map(() => { const x = -2300 + r() * 6000, y = 1010 + r() * 300; return `<path d="M${f(x)},${f(y + 20)}q4,-18 0,-36M${f(x + 10)},${f(y + 22)}q6,-16 2,-32" stroke="#6a9a3a" stroke-width="3" fill="none" stroke-linecap="round"/>`; }).join("");
    put(L.mid, mid + `<rect x="-2400" y="1330" width="6200" height="900" fill="#b09a66"/>`);
    let s = `<rect x="-2400" y="1360" width="6200" height="1400" fill="#b89e6a"/><path d="M-2400,1372H3800" stroke="#d8c48a" stroke-width="4" opacity=".6"/><path d="M-2400,1420Q-1000,1400 400,1430T3800,1420" stroke="#9a8050" stroke-width="18" fill="none" opacity=".5"/>
      <ellipse cx="900" cy="1470" rx="140" ry="22" fill="#cfe4ec" opacity=".6"/><ellipse cx="900" cy="1468" rx="110" ry="14" fill="#e8f4fc" opacity=".5"/>
      ${bush(300, 1400, 1, "#4a8a3a", `${id}-bush1`)}${bush(1300, 1400, 0.9, "#3e7e34", `${id}-bush2`)}
      ${[80, 560, 1120, 1600, 2100].map((x) => grassTuft(x, 1400, 0.8 + r() * 0.5)).join("")}
      <circle cx="1700" cy="1410" r="14" fill="#8a7a62"/><circle cx="1740" cy="1416" r="9" fill="#9a8a70"/>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-120,1920)">${[0, 40, 80, 120, 160].map((dx) => `<path d="M${dx},0Q${dx + 30},-200 ${dx + 90},-420" stroke="#3a6a2a" stroke-width="14" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <g transform="translate(1800,1940)">${[0, 50, 100].map((dx) => `<path d="M${dx},0Q${dx - 30},-220 ${dx - 100},-380" stroke="#3a6a2a" stroke-width="14" fill="none" stroke-linecap="round"/>`).join("")}</g>`);
    put(L.glow, `<g style="mix-blend-mode:screen"><path d="M1300,500H1700L2600,1500H600Z" fill="url(#jkRay)" opacity=".22" style="filter:blur(22px)"/></g>
      <rect x="-2400" y="1040" width="6200" height="360" fill="url(#brFog)" opacity=".7"/>`);
  };

  // ---------------- the camp ----------------
  const hut = (x, y, w, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-${w / 2 - 20},0V-120M${w / 2 - 20},0V-120M0,0V-120" stroke="#5a3a1c" stroke-width="12"/>
    <rect x="-${w / 2}" y="-130" width="${w}" height="14" fill="#6a4a22"/><rect x="-${w / 2 + 6}" y="-290" width="${w - 12}" height="160" fill="#a8864a"/>${[-250, -210, -170].map((yy) => `<path d="M-${w / 2 + 6},${yy}H${w / 2 - 6}" stroke="#8a6a34" stroke-width="3" opacity=".7"/>`).join("")}
    <rect x="-24" y="-250" width="48" height="120" fill="#3a2410"/><path d="M-${w / 2 + 40},-290L0,-420L${w / 2 + 40},-290Z" fill="url(#brThatch)"/><path d="M-${w / 2 + 40},-290L0,-420L${w / 2 + 40},-290" stroke="#6a4a22" stroke-width="6" fill="none"/></g>`;
  const granary = (x, y, id) => `<g id="${id}-granary" transform="translate(${x},${y})"><g id="${id}-under"><rect x="-150" y="-400" width="300" height="400" fill="#4a3418" opacity=".55"/></g>
    ${[-130, -44, 44, 130].map((dx) => `<rect x="${dx - 9}" y="-400" width="18" height="400" fill="#5a3a1c"/><rect x="${dx - 12}" y="-12" width="24" height="12" fill="#3a2410"/>`).join("")}
    <rect x="-160" y="-414" width="320" height="18" fill="#6a4a22"/><rect x="-150" y="-600" width="300" height="186" fill="#b08a4a"/>${[-560, -520, -480, -440].map((yy) => `<path d="M-150,${yy}H150" stroke="#8a6a34" stroke-width="3" opacity=".7"/>`).join("")}
    <rect x="-30" y="-560" width="60" height="146" fill="#3a2410"/><path d="M-200,-600L0,-740L200,-600Z" fill="url(#brThatch)"/><path d="M-200,-600L0,-740L200,-600" stroke="#6a4a22" stroke-width="6" fill="none"/>
    <path d="M-210,-410L-150,-600" stroke="#8a6a34" stroke-width="8"/>${[-440, -480, -520, -560].map((yy, k) => `<path d="M${-196 + k * 14},${yy + 8}h30" stroke="#8a6a34" stroke-width="5"/>`).join("")}</g>`;
  const stockade = (x0, x1, y, gateX) => { let h = ""; for (let x = x0; x < x1; x += 46) { if (x > gateX && x < gateX + 200) continue; const hh = 400 + ((x / 46) % 3) * 24; h += `<path d="M${x - 16},${y}V${y - hh}L${x},${y - hh - 36}L${x + 16},${y - hh}V${y}Z" fill="${(x / 46) % 2 ? "#a08048" : "#8c6c3c"}"/>`; }
    h += `<path d="M${x0},${y - 300}H${x1}M${x0},${y - 140}H${x1}" stroke="#5a3a1c" stroke-width="10" opacity=".8"/>`;
    h += `<path d="M${gateX - 10},${y}V${y - 520}M${gateX + 210},${y}V${y - 520}" stroke="#5a3a1c" stroke-width="26"/><rect x="${gateX - 40}" y="${y - 540}" width="280" height="26" fill="#5a3a1c"/><path d="M${gateX + 10},${y}V${y - 440}H${gateX + 190}V${y}" fill="#3a2a1a" opacity=".5"/>`; return h; };
  Sets.brCamp = (L, o = {}) => {
    const id = o.id || "brc", r = mk(o.seed || 11), night = !!o.night;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${night ? "#080c22" : "#f4e4c0"}"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#${night ? "brNight" : "brDay"})"/>
      ${night ? `<circle cx="260" cy="420" r="260" fill="url(#brMoon)" opacity=".8"/><circle cx="260" cy="420" r="62" fill="#fff6e0"/>${[...Array(50)].map(() => `<circle cx="${f(-1600 + r() * 4600)}" cy="${f(-300 + r() * 800)}" r="${f(0.8 + r() * 1.6)}" fill="#e8ecff" opacity="${f(0.3 + r() * 0.6)}"/>`).join("")}` : `<circle cx="1700" cy="380" r="260" fill="url(#jkSun)" opacity=".55"/>`}`);
    let far = `<path d="M-2400,1000L-1800,940L-1200,990L-600,920L0,980L600,930L1200,990L1800,940L2400,1000L3000,950L3800,1000V1200H-2400Z" fill="${night ? "#121a34" : "#4a7a4a"}"/>`;
    [[-900, 1010, 1.1], [-500, 1000, 0.9], [2200, 1010, 1.0], [2700, 1000, 1.2], [3300, 1010, 0.9]].forEach(([x, y, s]) => (far += palm(x, y, s, night ? "#0e1428" : "#2e5a34")));
    [[-1300, 1010, 1], [600, 1010, 0.8], [3000, 1010, 1]].forEach(([x, y, s]) => (far += bamboo(x, y, s, night ? "#101830" : "#3a6a3a")));
    far += `<rect x="-2400" y="880" width="6200" height="330" fill="url(#${night ? "brFog" : "jkHazeW"})" opacity="${night ? 0.5 : 0.8}"/>`;
    // the enemy patrol: torch silhouettes beyond the fence. o.fenceFront puts them and the fence in the set layer (parallax 1) so the camera can frame them; o.noFence drops the fence (the enemy's own view)
    let enemyHTML = "";
    if (o.enemy) { enemyHTML = `<g id="${id}-enemy">`; for (let k = 0; k < o.enemy; k++) enemyHTML += BR.enemy(2300 + k * 180 + r() * 60, 1150, 1.3 + r() * 0.25, k); enemyHTML += "</g>"; if (!o.fenceFront) far += enemyHTML; }
    put(L.far, far);
    let mid = `${hut(-650, 1180, 340, 1)}${hut(2100, 1180, 300, 0.95)}${o.fenceFront || o.noFence ? "" : stockade(-2400, 3800, 1180, 1000)}`;
    put(L.mid, mid + `<rect x="-2400" y="1180" width="7600" height="900" fill="${night ? "#2a2a3a" : "#b89a6a"}"/>`);
    let s = `${o.fenceFront ? enemyHTML + stockade(-2400, 5200, 1180, 1000) : ""}<rect x="-2400" y="1240" width="7600" height="1400" fill="${night ? "#3a3448" : "#c0a470"}"/>${[...Array(30)].map(() => `<ellipse cx="${f(-2300 + r() * 6000)}" cy="${f(1300 + r() * 600)}" rx="${f(40 + r() * 90)}" ry="${f(8 + r() * 10)}" fill="${night ? "#2e2a3e" : "#ad9262"}" opacity=".7"/>`).join("")}
      ${granary(1600, 1400, id)}
      <g transform="translate(330,1400)">${BR.POT}</g><g transform="translate(520,1400)">${BR.MORTAR}</g>
      <g transform="translate(200,1400)"><path d="M-50,0Q-56,-60 -36,-80H36Q56,-60 50,0Z" fill="#a8864a"/><path d="M-44,-20H44M-48,-44H48" stroke="#8a6a34" stroke-width="3"/>${[-24, -4, 16, 0, -12, 10].map((dx, k) => `<circle cx="${dx}" cy="${-84 - (k > 2 ? 16 : 0)}" r="13" fill="#9ac83a"/>`).join("")}</g>
      <g transform="translate(440,1400)"><path d="M-40,0Q-46,-50 -30,-66H30Q46,-50 40,0Z" fill="#a8864a"/>${[-16, 0, 16].map((dx) => `<path d="M${dx},-70q4,-20 0,-36" stroke="#d8443a" stroke-width="6" stroke-linecap="round"/>`).join("")}</g>
      ${o.pole ? `<g id="${id}-pole" transform="translate(760,1400)"><rect x="-22" y="-520" width="44" height="520" fill="#6a4a22"/><rect x="-22" y="-520" width="14" height="520" fill="#8a6a34"/><rect x="-26" y="-540" width="52" height="22" rx="4" fill="#5a3a1c"/></g>` : ""}
      ${[60, 1300].map((x) => `<g transform="translate(${x},1400)"><rect x="-8" y="-300" width="16" height="300" fill="#5a3a1c"/><path d="M-20,-300H20L14,-330H-14Z" fill="#8a6a34"/>${o.torches ? `<g transform="translate(0,-330)">${BR.flame(`brFlame ${id}-tf`)}</g>` : ""}</g>`).join("")}
      ${o.drum ? `<g transform="translate(1100,1400) rotate(-8)">${BR.DRUM}</g>` : ""}
      <g transform="translate(1850,1400)"><path d="M-70,0Q-96,-90 -60,-150Q0,-180 60,-150Q96,-90 70,0Z" fill="#6a4a30"/><ellipse cy="-152" rx="52" ry="12" fill="#3a2a1a"/><path d="M-80,-60Q0,-40 80,-60" stroke="#8a6a44" stroke-width="4" fill="none"/></g>
      ${o.offerings ? `<g transform="translate(660,1440)">${BR.BANANA}</g><g transform="translate(760,1444) scale(.9)">${BR.STICKY}</g><g transform="translate(860,1440) scale(.8)">${BR.BANANA}</g><g transform="translate(600,1456)"><ellipse rx="30" ry="10" fill="#8a6a44"/><ellipse cy="-4" rx="24" ry="7" fill="#e8d8b0"/></g>` : ""}
      ${o.limes ? `<g id="${id}-limes">${BR.limeRow(100, 1470, 26, 56, 0.9)}</g>` : ""}`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-160,1960)"><path d="M0,0Q60,-260 220,-420Q120,-260 90,0Z" fill="#2e5a30"/><path d="M120,0Q220,-200 400,-300Q300,-120 240,0Z" fill="#3a6a3a"/></g>
      <g transform="translate(1960,1980)"><rect x="-14" y="-420" width="28" height="420" fill="#4a3018"/><path d="M-30,-420H30L16,-460H-16Z" fill="#6a4a22"/></g>`);
    put(L.glow, `<g style="mix-blend-mode:screen">${night ? `${o.torches ? [60, 1300].map((x) => `<circle cx="${x}" cy="1080" r="260" fill="url(#jkWarm)" opacity=".5"/>`).join("") : ""}<circle cx="260" cy="420" r="520" fill="url(#brMoon)" opacity=".25"/>` : `<path d="M1500,300H1800L2500,1500H900Z" fill="url(#jkRay)" opacity=".2" style="filter:blur(22px)"/>`}</g>
      ${o.fog ? `<rect x="-2400" y="1000" width="6200" height="380" fill="url(#brFog)" opacity=".75"/><rect x="-2400" y="1300" width="6200" height="300" fill="url(#brFog)" opacity=".5"/>` : ""}`);
  };

  // ---------------- 2569: the bedroom and the kitchen ----------------
  const DOOR = `<g transform="translate(1520,1200)"><rect x="-130" y="-640" width="260" height="640" fill="#8a6a4a"/><rect x="-110" y="-620" width="200" height="620" fill="#c8b8a0"/><rect x="-100" y="-610" width="180" height="600" fill="#e8dcc8"/><circle cx="70" cy="-320" r="10" fill="#c8a040"/></g>`;
  Sets.brRoom = (L, o = {}) => {   // o.doorFront: the door in the set layer (parallax 1) so someone can stand in the doorway
    const id = o.id || "brr";
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#dfe6ec"/>`);
    put(L.far, `<rect x="-2400" y="-1400" width="6200" height="2600" fill="#e4e9ee"/><rect x="-2400" y="1180" width="6200" height="40" fill="#cfd6dc"/>`);
    let mid = `<rect x="-2400" y="1200" width="6200" height="900" fill="#c8b090"/>${[...Array(14)].map((_, k) => `<path d="M-2400,${1240 + k * 50}H3800" stroke="#b89e7c" stroke-width="3" opacity=".6"/>`).join("")}`;
    if (!o.kitchen) {
      mid += `<g transform="translate(1100,900)"><rect x="-200" y="-400" width="400" height="400" fill="#8ab8e8"/><rect x="-200" y="-400" width="400" height="400" fill="url(#jkHazeW)" opacity=".6"/><path d="M0,-400V0M-200,-200H200" stroke="#f4f4f4" stroke-width="12"/><rect x="-216" y="-416" width="432" height="432" fill="none" stroke="#f4f4f4" stroke-width="16"/>
        <rect x="-240" y="-440" width="60" height="480" fill="#d8b890" opacity=".9"/><rect x="180" y="-440" width="60" height="480" fill="#d8b890" opacity=".9"/></g>
        <g transform="translate(400,760)"><rect x="-130" y="-180" width="260" height="360" rx="6" fill="#2a2a44"/><rect x="-120" y="-170" width="240" height="340" fill="#4a3a30"/><path d="M-120,30L-40,-60L20,0L120,-110V170H-120Z" fill="#8a5a30"/>${T(0, -110, 44, "บางระจัน", { fill: "#f6d36a", w: 900 })}${T(0, -70, 20, "ใน 60 วิ", { fill: "#f4ecd8", w: 700 })}</g>
${o.doorFront ? "" : DOOR}`;
    } else {
      mid += `<g transform="translate(900,1200)"><rect x="-200" y="-420" width="400" height="300" fill="#8a6a44"/><rect x="-190" y="-410" width="180" height="280" fill="url(#brMesh)" stroke="#5a4a3a" stroke-width="4"/><rect x="10" y="-410" width="180" height="280" fill="url(#brMesh)" stroke="#5a4a3a" stroke-width="4"/>
        <rect x="-210" y="-430" width="420" height="16" fill="#6a4a30"/><path d="M-180,-120V0M180,-120V0M-170,0h-20M170,0h20" stroke="#6a4a30" stroke-width="14"/><circle cx="-20" cy="-270" r="6" fill="#c8a040"/><circle cx="20" cy="-270" r="6" fill="#c8a040"/>
        <g transform="translate(-40,0)"><path d="M-70,0Q-76,-50 -50,-66H50Q76,-50 70,0Z" fill="#a8864a"/><path d="M-62,-24H62M-66,-46H66" stroke="#8a6a34" stroke-width="3"/>${[-40, -16, 8, 32, -28, -4, 20, -16, 8].map((dx, k) => `<circle cx="${dx}" cy="${-72 - (k > 3 ? 16 : 0) - (k > 7 ? 14 : 0)}" r="12" fill="#9ac83a"/>`).join("")}</g></g>
        <g transform="translate(300,1200)"><rect x="-120" y="-200" width="240" height="200" fill="#d8d8d8"/><rect x="-110" y="-190" width="220" height="60" fill="#c8c8cc"/><rect x="-110" y="-120" width="220" height="110" fill="#e8e8ea"/></g>`;
    }
    put(L.mid, mid);
    let s = `<rect x="-2400" y="1240" width="6200" height="1400" fill="#c8b090"/>${[...Array(14)].map((_, k) => `<path d="M-2400,${1280 + k * 50}H3800" stroke="#b89e7c" stroke-width="3" opacity=".6"/>`).join("")}`;
    if (!o.kitchen && o.doorFront) s += DOOR;
    if (!o.kitchen) s += `<g transform="translate(650,1400)"><rect x="-350" y="-170" width="700" height="60" rx="6" fill="#6a4a3a"/><rect x="-350" y="-110" width="24" height="110" fill="#5a3a2a"/><rect x="326" y="-110" width="24" height="110" fill="#5a3a2a"/>
        <rect x="-340" y="-230" width="680" height="70" rx="12" fill="#f4f0ea"/><rect x="-340" y="-196" width="680" height="40" fill="#6a8ac8"/><path d="M-340,-196Q-200,-230 -60,-196T220,-196T340,-196" fill="#7a9ad8"/><rect x="-330" y="-250" width="150" height="40" rx="14" fill="#fff"/>
        <rect x="-430" y="-240" width="80" height="140" fill="#8a6a4a"/><rect x="-440" y="-250" width="100" height="16" fill="#a8866a"/><path d="M-400,-250V-300" stroke="#2a2a2a" stroke-width="4"/><circle cx="-400" cy="-310" r="18" fill="#f6d36a"/></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, o.kitchen ? `` : `<g transform="translate(1900,1960)"><rect x="-120" y="-700" width="240" height="700" fill="#6a4a3a" opacity=".9"/></g>`);
    put(L.glow, `<g style="mix-blend-mode:screen"><path d="M900,500H1300L1700,1500H300Z" fill="url(#jkRay)" opacity=".28" style="filter:blur(22px)"/></g>`);
  };
})();
