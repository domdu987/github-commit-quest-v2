// สกิลจอมโกหก · sets in the channel look (layered depth, haze, practical lights, both frames). Ground for people: y 1400.
//   Sets.jkCity(L, o)   Earth at dusk: office towers, a road of cars whose tail lights glow (#id-brake, for the red-ears gag),
//                       the sidewalk with a café table under an umbrella (x 520…760), the insurance office front (x 860…1260),
//                       a street lamp at x 380 · o.manhole: the open manhole at x 1180 (#id-hole) · o.dark: later in the evening
//   Sets.jkCloud(L, o)  the queue on the clouds: a pastel sky, cloud banks, a gold gate far off, velvet ropes (x 100…560),
//                       the giant gacha machine (dome at 820,860 r 170, crank #id-crank on the left at 650,1170, chute mouth 820,1290),
//                       the goddess's counter (x 1080…1440, top 1180, in FRONT of whoever stands behind it), sign over it,
//                       rays from above · #id-hole: the floor hole under x 440 (scale it open)
//   Sets.jkTown(L, o)   the starting town, late afternoon: mountains, a castle on the hill, timber houses, a cobbled plaza,
//                       the guild hall (x 620…1380) with the ranking board (x 760…1240, rows #id-r0… at y 760 + 70k)
//                       o.rows: [[rank, name, hilite]] · lanterns lit when o.dusk
(function () {
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}>${text}</text>`;
  Sets.DEFS += `
    <linearGradient id="jkDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2a5a"/><stop offset=".35" stop-color="#6a4a7a"/><stop offset=".62" stop-color="#e88a6a"/><stop offset=".8" stop-color="#f6c47a"/><stop offset="1" stop-color="#f6d8a0"/></linearGradient>
    <linearGradient id="jkHeaven" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ab8e8"/><stop offset=".45" stop-color="#cfe0f4"/><stop offset=".75" stop-color="#f8e6d8"/><stop offset="1" stop-color="#fdf0dc"/></linearGradient>
    <linearGradient id="jkNoon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6aa0d8"/><stop offset=".55" stop-color="#b8d4e8"/><stop offset=".85" stop-color="#f4dcb0"/><stop offset="1" stop-color="#f8e4c0"/></linearGradient>
    <linearGradient id="jkHazeW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4e0" stop-opacity="0"/><stop offset="1" stop-color="#fff4e0" stop-opacity=".6"/></linearGradient>
    <linearGradient id="jkHazeD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6b880" stop-opacity="0"/><stop offset="1" stop-color="#f6b880" stop-opacity=".55"/></linearGradient>
    <linearGradient id="jkRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff8e0" stop-opacity=".75"/><stop offset="1" stop-color="#fff8e0" stop-opacity="0"/></linearGradient>
    <radialGradient id="jkSun"><stop offset="0" stop-color="#fffbe8"/><stop offset=".25" stop-color="#ffe8b0" stop-opacity=".8"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkRed"><stop offset="0" stop-color="#ff5a3a" stop-opacity=".9"/><stop offset=".4" stop-color="#ff3a2a" stop-opacity=".35"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkWarm"><stop offset="0" stop-color="#ffe0a0" stop-opacity=".9"/><stop offset=".45" stop-color="#ffc070" stop-opacity=".3"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkGold"><stop offset="0" stop-color="#fffbe0"/><stop offset=".3" stop-color="#ffe070" stop-opacity=".8"/><stop offset="1" stop-color="#ffc840" stop-opacity="0"/></radialGradient>
    <linearGradient id="jkGlassD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset=".45" stop-color="#e8f4ff" stop-opacity=".12"/><stop offset="1" stop-color="#ffffff" stop-opacity=".3"/></linearGradient>
    <pattern id="jkCobble" width="60" height="30" patternUnits="userSpaceOnUse"><rect width="60" height="30" fill="#b8a488"/><path d="M0,15h60M30,0v15M0,15v15M60,15v15" stroke="#9a8668" stroke-width="3"/><rect x="4" y="3" width="22" height="9" rx="3" fill="#c4b094" opacity=".6"/></pattern>`;

  // ---------------- Earth at dusk ----------------
  function car(x, y, c, id) {
    return `<g transform="translate(${x},${y})"><path d="M-110,-10Q-112,-50 -84,-56L-50,-90H46L84,-56Q112,-52 110,-10Z" fill="${c}"/><path d="M-44,-84H-4V-58H-70ZM4,-84H42L72,-58H4Z" fill="#2a3448" opacity=".8"/>
      <circle cx="-62" cy="-8" r="20" fill="#1c1c22"/><circle cx="62" cy="-8" r="20" fill="#1c1c22"/><circle cx="-62" cy="-8" r="8" fill="#6a6e76"/><circle cx="62" cy="-8" r="8" fill="#6a6e76"/>
      <rect x="-112" y="-46" width="14" height="14" rx="3" fill="#ff4a3a" class="${id}-tail"/></g>`;
  }
  Sets.jkCity = (L, o = {}) => {
    const id = o.id || "jkc", r = mk(o.seed || 3);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#f6d8a0"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#jkDusk)"/>
      <circle cx="1500" cy="980" r="240" fill="url(#jkSun)"/><circle cx="1500" cy="980" r="70" fill="#fff2d0"/>`);
    let fr = "";
    for (let x = -1800; x < 3000; ) { const w = 140 + r() * 160, h = 380 + r() * 560, c = ["#4a3a5e", "#523e62", "#45385a"][Math.floor(r() * 3)];
      fr += `<rect x="${f(x)}" y="${f(1180 - h)}" width="${f(w)}" height="${f(h + 600)}" fill="${c}"/>`;
      for (let yy = 1210 - h; yy < 1150; yy += 34) for (let xx = x + 12; xx < x + w - 16; xx += 24) if (r() < (o.dark ? 0.3 : 0.12)) fr += `<rect x="${f(xx)}" y="${f(yy)}" width="13" height="18" fill="#ffd890" opacity="${f(0.45 + r() * 0.4)}"/>`;
      x += w + 8 + r() * 40; }
    put(L.far, fr + `<rect x="-2400" y="760" width="6200" height="560" fill="url(#jkHazeD)"/>`);
    // the road with traffic (their tail lights are the brake lights of the gag)
    let mid = `<rect x="-2400" y="1150" width="6200" height="200" fill="#4a4250"/><path d="M-2400,1250H3800" stroke="#e8d8a8" stroke-width="5" stroke-dasharray="70 70" opacity=".55"/>`;
    [[-700, "#c8c8cc"], [-300, "#3a6aa8"], [140, "#d8443a"], [560, "#e8e2d6"], [980, "#5a5e66"], [1420, "#c8a040"], [1860, "#3a7a5a"]].forEach(([x, c]) => (mid += car(x, 1236, c, id)));
    mid += `<rect x="-2400" y="1300" width="6200" height="40" fill="#8a8090"/><rect x="-2400" y="1336" width="6200" height="900" fill="#6a6272"/>`;
    put(L.mid, mid);
    // sidewalk, café, office, lamp, manhole
    let s = `<rect x="-2400" y="1360" width="6200" height="1400" fill="#b8aca0"/><path d="M-2400,1360H3800" stroke="#9a8e84" stroke-width="6"/>
      ${[...Array(40)].map((_, i) => `<path d="M${-2400 + i * 160},1360l-60,1300" stroke="#a89c90" stroke-width="3"/>`).join("")}
      <g transform="translate(640,1400)"><path d="M-12,-300V0" stroke="#6a6a72" stroke-width="8"/><path d="M-210,-300Q0,-380 210,-300Z" fill="#e8d8b8"/><path d="M-210,-300Q-100,-330 0,-336V-300Z" fill="#d8443a"/><path d="M0,-336Q100,-330 210,-300H0Z" fill="#e8d8b8"/>
        <rect x="-120" y="-150" width="240" height="14" rx="4" fill="#f4ecd8"/><path d="M-100,-136L-110,0M100,-136L110,0" stroke="#8a8a92" stroke-width="6"/>
        <g transform="translate(-60,-150)"><rect x="-14" y="-30" width="28" height="30" rx="4" fill="#f4f1ea"/><path d="M14,-22q12,2 0,14" stroke="#f4f1ea" stroke-width="4" fill="none"/></g>
        <g transform="translate(40,-150)"><rect x="-40" y="-8" width="80" height="8" fill="#e8e2d6"/><rect x="-34" y="-56" width="54" height="48" rx="3" fill="#d8443a" transform="rotate(-6)"/></g></g>
      <g transform="translate(1060,1360)"><rect x="-220" y="-560" width="440" height="560" fill="#e8e2d6"/><rect x="-200" y="-420" width="400" height="400" fill="#9ac0d8" opacity=".85"/><path d="M0,-420V-20" stroke="#e8e2d6" stroke-width="10"/>
        <rect x="-220" y="-540" width="440" height="100" fill="#2a4a8a"/>${T(0, -478, 46, "ประกันชีวิต มั่นใจ", { fill: "#f6d36a", w: 900 })}${T(0, -448, 20, "สาขา 112 · เปิดทุกวัน", { fill: "#f4ecd8", w: 700, op: 0.85 })}
        <rect x="-180" y="-260" width="120" height="150" fill="#f4ecd8" opacity=".85"/>${T(-120, -200, 22, "ยอดขาย", { fill: "#2a4a8a", w: 900 })}${T(-120, -150, 40, "0", { fill: "#d8443a", w: 900 })}</g>
      <g transform="translate(380,1400)"><rect x="-10" y="-760" width="20" height="760" fill="#4a4a54"/><path d="M0,-740Q0,-780 60,-780H120" stroke="#4a4a54" stroke-width="12" fill="none"/><path d="M96,-784H156L148,-764H104Z" fill="#5a5a66"/></g>`;
    if (o.manhole) s += `<g transform="translate(1180,1520)"><ellipse rx="110" ry="24" fill="#3a3a40"/><ellipse id="${id}-hole" rx="92" ry="18" fill="#08080c"/><ellipse cx="160" cy="-6" rx="104" ry="20" fill="#7a7a82"/><ellipse cx="160" cy="-8" rx="86" ry="14" fill="#8a8a92"/>${[-50, -20, 10, 40].map((d) => `<path d="M${160 + d},-18v20" stroke="#6a6a72" stroke-width="4"/>`).join("")}
      <path d="M-140,-10L-140,-80M-60,-26L-60,-90" stroke="#e8a030" stroke-width="7"/><path d="M-170,-80H-30" stroke="#e8a030" stroke-width="10" stroke-dasharray="20 14"/></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-180,1900)"><path d="M0,0Q-40,-300 40,-520Q120,-300 80,0Z" fill="#2e4a34"/><path d="M60,0Q140,-260 260,-360Q200,-160 130,0Z" fill="#3a5a3e"/><rect x="-60" y="-10" width="220" height="220" rx="20" fill="#5a3a2a"/></g>`);
    put(L.glow, `<g style="mix-blend-mode:screen"><circle cx="506" cy="626" r="180" fill="url(#jkWarm)" opacity="${o.dark ? 0.7 : 0.45}"/>
      <g id="${id}-brake" opacity=".35">${[-700, -300, 140, 560, 980, 1420, 1860].map((x) => `<circle cx="${x - 105}" cy="1197" r="60" fill="url(#jkRed)"/>`).join("")}</g></g>`);
  };

  // ---------------- the queue on the clouds ----------------
  const puff = (x, y, w, h, c = "#ffffff", sh = "#e4e8f4") => `<g transform="translate(${x},${y})"><ellipse cx="0" cy="${f(h * 0.15)}" rx="${f(w * 0.55)}" ry="${f(h * 0.45)}" fill="${sh}"/>
    ${[[-0.32, 0.02, 0.3], [0, -0.22, 0.38], [0.3, -0.04, 0.3], [-0.14, -0.1, 0.3], [0.16, -0.18, 0.28]].map(([dx, dy, rr]) => `<circle cx="${f(dx * w)}" cy="${f(dy * h)}" r="${f(rr * w * 0.6)}" fill="${c}"/>`).join("")}</g>`;
  Sets.jkCloud = (L, o = {}) => {
    const id = o.id || "jkq", r = mk(o.seed || 9);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#fdf0dc"/><rect x="-3000" y="-1400" width="8000" height="2700" fill="url(#jkHeaven)"/>
      <circle cx="780" cy="200" r="420" fill="url(#jkSun)" opacity=".8"/>`);
    let fr = "";
    for (let i = 0; i < 16; i++) fr += puff(-1800 + i * 330 + r() * 90, 1000 + r() * 160, 420 + r() * 260, 260 + r() * 120, "#fbf6f0", "#e8e0e8");
    fr += `<g transform="translate(1600,820)" opacity=".75"><rect x="-90" y="-240" width="26" height="250" fill="#e8c86a"/><rect x="64" y="-240" width="26" height="250" fill="#e8c86a"/><path d="M-100,-240Q0,-320 100,-240" stroke="#e8c86a" stroke-width="22" fill="none"/>
      <path d="M-64,-220Q0,-270 64,-220V10H-64Z" fill="#fff8e0" opacity=".7"/></g>`;
    put(L.far, fr + `<rect x="-2400" y="700" width="6200" height="600" fill="url(#jkHazeW)"/>`);
    let mid = "";
    for (let i = 0; i < 14; i++) mid += puff(-1600 + i * 360 + r() * 80, 1290 + r() * 60, 520, 260, "#ffffff", "#e6eaf4");
    put(L.mid, mid + `<rect x="-2400" y="1330" width="6200" height="900" fill="#f4f2f6"/>`);
    // cloud floor, ropes, the machine, the counter
    let s = `<rect x="-2400" y="1360" width="6200" height="1400" fill="#f8f6fa"/>${[...Array(24)].map((_, i) => puff(-1800 + i * 230, 1400 + (i % 3) * 30, 300, 120, "#ffffff", "#e8ecf6")).join("")}
      <ellipse id="${id}-hole" cx="440" cy="1420" rx="0" ry="0" fill="#7ab0e8"/>
      ${[100, 280, 460].map((x) => `<g transform="translate(${x},1400)"><rect x="-7" y="-150" width="14" height="150" fill="#d8b84a"/><circle cy="-156" r="12" fill="#e8c86a"/><rect x="-26" y="-6" width="52" height="10" rx="4" fill="#c8a43a"/></g>`).join("")}
      <path d="M100,-0" /><path d="M100,1260Q190,1300 280,1260Q370,1300 460,1260" stroke="#a8243a" stroke-width="12" fill="none" transform="translate(0,0)"/>
      <g transform="translate(820,1400)">
        <rect x="-150" y="-330" width="300" height="330" rx="24" fill="#d8443a"/><rect x="-150" y="-330" width="60" height="330" rx="20" fill="#b82e2a"/><rect x="-130" y="-40" width="260" height="22" rx="8" fill="#a82420"/>
        <rect x="-60" y="-150" width="120" height="70" rx="14" fill="#2a1a1a"/><rect id="${id}-chute" x="-46" y="-140" width="92" height="50" rx="10" fill="#1a1010"/>
        ${T(0, -250, 44, "สุ่มสกิล", { fill: "#fff2c8", w: 900 })}<circle cx="-90" cy="-200" r="14" fill="#f6d36a"/><rect x="66" y="-216" width="44" height="30" rx="5" fill="#2a1a1a"/><rect x="74" y="-208" width="28" height="6" rx="3" fill="#f6d36a"/>
        <circle cx="0" cy="-540" r="190" fill="#e8f2fa" opacity=".55"/>
        ${[...Array(34)].map(() => { const a = r() * 6.28, d = Math.sqrt(r()) * 150; const cc = ["#f6d36a", "#d8443a", "#3a8ac8", "#6ac87a", "#c87ac8", "#f4ecd8", "#9aa0a6"][Math.floor(r() * 7)]; const x = Math.cos(a) * d, y = -480 + Math.abs(Math.sin(a)) * 120 + r() * 40;
          return `<g transform="translate(${f(x)},${f(y)})"><circle r="22" fill="${cc}"/><path d="M-22,0A22,22 0 0,0 22,0Z" fill="#f4f1ea" opacity=".85"/><circle cx="-7" cy="-9" r="5" fill="#fff" opacity=".7"/></g>`; }).join("")}
        <circle cx="0" cy="-540" r="190" fill="url(#jkGlassD)"/><circle cx="0" cy="-540" r="190" fill="none" stroke="#f4f8fc" stroke-width="10"/><path d="M-120,-640Q-60,-700 20,-704" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/>
        <rect x="-170" y="-360" width="340" height="40" rx="16" fill="#b82e2a"/>
        <g id="${id}-crank" transform="translate(-170,-230) scale(-1,1)"><circle r="26" fill="#d8b84a"/><rect x="-8" y="-8" width="90" height="16" rx="8" fill="#c8a43a"/><circle cx="84" cy="0" r="16" fill="#f4ecd8"/></g></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.set, `<g class="act-front"><g transform="translate(1260,1400)"><rect x="-190" y="-230" width="380" height="230" rx="10" fill="#f4ecd8"/><rect x="-200" y="-244" width="400" height="22" rx="8" fill="#d8b84a"/>
        <rect x="-170" y="-200" width="340" height="170" rx="8" fill="#ebe2cf"/>${T(0, -130, 30, "ไม่รับคืน", { fill: "#a8243a", w: 900 })}${T(0, -88, 30, "ไม่รับเปลี่ยน", { fill: "#a8243a", w: 900 })}
        <g transform="translate(120,-250)"><rect x="-24" y="-40" width="48" height="40" rx="5" fill="#f6a8c8"/>${T(0, -12, 15, "หมากฝรั่ง", { fill: "#fff", w: 800 })}</g>
        <g transform="translate(-120,-250)"><rect x="-6" y="-60" width="12" height="60" fill="#c8a43a"/><circle cy="-66" r="16" fill="#e8c86a"/></g></g></g>`);
    put(L.fg, `${puff(-260, 1880, 900, 360)}${puff(1500, 1900, 900, 380)}`);
    put(L.glow, `<g style="mix-blend-mode:screen"><path d="M560,-200H760L1100,1500H400Z" fill="url(#jkRay)" opacity=".26" style="filter:blur(18px)"/><path d="M880,-200H980L1260,1500H980Z" fill="url(#jkRay)" opacity=".18" style="filter:blur(18px)"/>
      <circle id="${id}-burst" cx="820" cy="1300" r="0" fill="url(#jkGold)"/></g>`);
  };

  // ---------------- the starting town ----------------
  function house(x, w, h, c, roof, r) {
    let s = `<g transform="translate(${x},1180)"><rect x="0" y="${-h}" width="${w}" height="${h}" fill="${c}"/><path d="M-20,${-h}L${w / 2},${-h - w * 0.55}L${w + 20},${-h}Z" fill="${roof}"/>`;
    for (let k = 0; k < 4; k++) s += `<path d="M0,${-h + k * h / 4}H${w}" stroke="#6a4a32" stroke-width="7"/>`;
    s += `<path d="M0,${-h}V0M${w},${-h}V0M${w / 2},${-h}V${-h * 0.25}" stroke="#6a4a32" stroke-width="8"/><path d="M0,${-h}L${w / 2},${-h / 2}L${w},${-h}" stroke="#6a4a32" stroke-width="5" fill="none"/>`;
    s += `<rect x="${w * 0.18}" y="${-h * 0.72}" width="${w * 0.22}" height="${h * 0.2}" fill="${r() < 0.5 ? "#ffd890" : "#4a5a6a"}"/><rect x="${w * 0.6}" y="${-h * 0.72}" width="${w * 0.22}" height="${h * 0.2}" fill="#4a5a6a"/>
      <rect x="${w * 0.38}" y="${-h * 0.3}" width="${w * 0.24}" height="${h * 0.3}" rx="${w * 0.12}" fill="#5a3a24"/></g>`;
    return s;
  }
  Sets.jkTown = (L, o = {}) => {
    const id = o.id || "jkt", r = mk(o.seed || 17), dusk = !!o.dusk;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#f8e4c0"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#${dusk ? "jkDusk" : "jkNoon"})"/><circle cx="-200" cy="500" r="300" fill="url(#jkSun)" opacity=".8"/>`);
    put(L.far, `<path d="M-2400,1100L-1800,620L-1300,880L-700,520L-100,860L400,600L1000,900L1600,560L2300,880L3000,640L3800,1000V1500H-2400Z" fill="#8aa0c0" opacity=".8"/>
      <path d="M-2400,1150L-1500,880L-800,1040L0,860L900,1060L1700,880L2600,1060L3800,920V1500H-2400Z" fill="#7a9a8a"/>
      <g transform="translate(1500,880)"><rect x="-120" y="-200" width="240" height="200" fill="#c8c0b8"/><rect x="-160" y="-300" width="70" height="300" fill="#d4ccc4"/><rect x="90" y="-280" width="70" height="280" fill="#d4ccc4"/>
        <path d="M-170,-300L-125,-380L-80,-300ZM80,-280L125,-360L170,-280Z" fill="#a8484a"/><rect x="-40" y="-260" width="80" height="60" fill="#c8c0b8"/><path d="M-50,-260L0,-330L50,-260Z" fill="#a8484a"/><path d="M125,-360V-410" stroke="#5a4a3a" stroke-width="4"/><path d="M125,-410h40l-10,10l10,10h-40z" fill="#d8443a"/></g>
      <rect x="-2400" y="760" width="6200" height="520" fill="url(#jkHazeW)" opacity=".8"/>`);
    let mid = "";
    const roofs = ["#a8484a", "#8a5a3a", "#6a5a7a", "#b86a3a"], walls = ["#efe2c8", "#e8d8b8", "#f2e8d4", "#e4d4bc"];
    for (let x = -1800; x < 3000; ) { const w = 180 + r() * 90, h = 260 + r() * 140; if (x < 520 || x > 1460) mid += house(x, w, h, walls[Math.floor(r() * 4)], roofs[Math.floor(r() * 4)], r); x += w + 30 + r() * 40; }
    put(L.mid, mid + `<rect x="-2400" y="1176" width="6200" height="900" fill="#c4b094"/>`);
    // the plaza and the guild hall
    const rows = o.rows || [[1, "เซอร์อาเธอร์ผู้ไม่เคยแพ้", 0], [2, "แม่มดดอกไม้เหล็ก", 0], [3, "ยักษ์ใจดีแห่งภูเขา", 0], [10, "เคน · ดาบแสง (SSR)", 1], [9999, "คุณ · จอมโกหก (F)", 2]];
    let s = `<rect x="-2400" y="1180" width="6200" height="1500" fill="url(#jkCobble)"/><rect x="-2400" y="1180" width="6200" height="1500" fill="#8a6a4a" opacity=".12"/>
      <g transform="translate(1000,1180)"><rect x="-380" y="-760" width="760" height="760" fill="#e8d8b8"/><path d="M-430,-760L0,-1040L430,-760Z" fill="#7a3a3a"/><path d="M-380,-760H380M-380,-380H380" stroke="#6a4a32" stroke-width="10"/>
        <rect x="-300" y="-1020" width="600" height="1" fill="none"/><rect x="-190" y="-930" width="380" height="110" rx="12" fill="#5a3a24"/>${T(0, -858, 56, "กิลด์ผู้กล้า", { fill: "#f6d36a", w: 900 })}
        <rect x="-110" y="-250" width="220" height="250" rx="110" fill="#4a2e1c"/><path d="M0,-250V0" stroke="#3a2214" stroke-width="6"/>
        ${[-330, 330].map((x) => `<g transform="translate(${x},-300)"><rect x="-26" y="-60" width="52" height="70" rx="8" fill="#3a2a20"/><rect x="-18" y="-50" width="36" height="50" rx="5" fill="${dusk ? "#ffd890" : "#f4e4c0"}"/></g>`).join("")}
        <path d="M-380,-760V0M380,-760V0" stroke="#6a4a32" stroke-width="12"/></g>
      <g id="${id}-board" transform="translate(1000,1180)"><path d="M-250,0V-140M250,0V-140" stroke="#5a3a24" stroke-width="22"/>
        <rect x="-270" y="-560" width="540" height="430" rx="14" fill="#7a4e2c"/><rect x="-250" y="-540" width="500" height="390" rx="8" fill="#e8d4a8"/>
        <rect x="-200" y="-600" width="400" height="60" rx="10" fill="#5a3a24"/>${T(0, -558, 36, "อันดับผู้กล้า", { fill: "#f6d36a", w: 900 })}
        ${rows.map(([n, name, hl], k) => { const y = -500 + k * 70 + (k === rows.length - 1 ? 20 : 0); const bg = hl === 1 ? "#f6d36a" : hl === 2 ? "#c8c8cc" : "#f4e8cc";
          return `<g id="${id}-r${k}"><rect x="-230" y="${y}" width="460" height="56" rx="8" fill="${bg}"/>${T(-205, y + 40, 30, n.toLocaleString("en-US"), { anchor: "start", fill: "#5a3a24", w: 900 })}${T(-95, y + 39, 27, name, { anchor: "start", fill: "#3a2a20", w: 800 })}</g>`; }).join("")}
        ${T(0, -196, 26, "⋮", { fill: "#8a6a4a", w: 900 })}</g>`;
    // a fountain and stalls on the left, banners
    s += `<g transform="translate(240,1300)"><ellipse rx="200" ry="40" fill="#9aa4ac"/><ellipse cy="-10" rx="180" ry="30" fill="#8ac0d8"/><rect x="-24" y="-180" width="48" height="170" fill="#a8b0b8"/><ellipse cy="-180" rx="70" ry="16" fill="#a8b0b8"/>
      <path d="M0,-190q-60,-40 -90,40M0,-190q60,-40 90,40" stroke="#bfe4f4" stroke-width="8" fill="none" opacity=".8"/></g>
      ${[500, 1500].map((x) => `<g transform="translate(${x},1180)"><rect x="-6" y="-420" width="12" height="420" fill="#5a3a24"/><path d="M6,-410h80v150l-40,-26l-40,26z" fill="#d8443a"/><circle cx="46" cy="-340" r="16" fill="#f6d36a"/></g>`).join("")}`;
    // o.dragon: the dragon from EP.3 still out cold across the plaza, in front of the guild (drawn in front of the cast at the back)
    if (o.dragon) s += `<g transform="translate(${o.dragon.x ?? 1150},${o.dragon.y ?? 1640}) scale(${o.dragon.flip ? -(o.dragon.s ?? 3.1) : (o.dragon.s ?? 3.1)},${o.dragon.s ?? 3.1}) rotate(-3)">${JK.dragon("#4f8a5e", { ko: true })}</g>`;   // flat out across the plaza (o.dragon.flip: heads to the left)
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-260,1880)"><path d="M0,0Q80,-420 200,-640Q260,-380 240,0Z" fill="#3a5a3a"/><path d="M160,0Q300,-280 460,-380Q380,-120 320,0Z" fill="#4a6a44"/></g>
      <g transform="translate(1700,1900)"><rect x="-120" y="-200" width="240" height="200" rx="10" fill="#6a4a32"/><path d="M-140,-200H140L120,-240H-120Z" fill="#8a5a3a"/>${[-70, 0, 70].map((x) => `<circle cx="${x}" cy="-250" r="34" fill="${["#d8443a", "#f6a830", "#6ac87a"][(x + 70) / 70]}"/>`).join("")}</g>`);
    put(L.glow, `<g style="mix-blend-mode:screen"><circle cx="-200" cy="500" r="700" fill="url(#jkSun)" opacity=".35"/>
      ${dusk ? [-330, 330].map((x) => `<circle cx="${1000 + x}" cy="880" r="140" fill="url(#jkWarm)"/>`).join("") : ""}
      <path d="M-600,-100H-300L700,1500H100Z" fill="url(#jkRay)" opacity=".25" style="filter:blur(20px)"/></g>`);
  };

  // ---------------- EP.2: the alley behind the guild (night) and the tavern ----------------
  //   Sets.jkAlley(L, o)   brick back wall of the guild (y 380…1400), a back door with a lamp (lamp at 860,720), crates (seat top 1252 at
  //                        x 520), barrels, a moon over the roofs · ground 1400
  //   Sets.jkTavern(L, o)  warm interior: beams, lanterns (#id-lamp…), a bar counter (x 1000…1500, top 1160, act-front) where มะปราง
  //                        stands, tables (x 160…420 and 560…820, top 1180), stools/benches, the fireplace (x -380), a window
  //                        (x 1640…1900, #id-win: what grows outside), the plain lit wall (x 200…900, y 420…1000) for hand shadows
  Sets.jkAlley = (L, o = {}) => {
    const id = o.id || "jka", r = mk(o.seed || 5);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#1a2040"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#sgNight)"/>
      <circle cx="260" cy="260" r="60" fill="#f4f0dc"/><circle cx="260" cy="260" r="160" fill="#f4f0dc" opacity=".08"/>
      ${[...Array(50)].map(() => `<circle cx="${f(-1600 + r() * 4600)}" cy="${f(-300 + r() * 700)}" r="${f(0.8 + r() * 1.5)}" fill="#e8ecff" opacity="${f(0.3 + r() * 0.5)}"/>`).join("")}`);
    put(L.far, `${[...Array(14)].map((_, i) => { const x = -1800 + i * 360, h = 200 + r() * 160; return `<path d="M${x},${560 - h}L${x + 180},${470 - h}L${x + 360},${560 - h}V900H${x}Z" fill="#1c2238"/>`; }).join("")}`);
    let s = `<rect x="-2400" y="300" width="6200" height="1100" fill="#5a3e3a"/>`;
    for (let y = 320; y < 1400; y += 40) for (let x = -2400 + ((y / 40) % 2) * 50; x < 3800; x += 100) s += `<rect x="${x + 3}" y="${y + 3}" width="94" height="34" rx="3" fill="${["#6a4842", "#62443e", "#704c44"][Math.floor(r() * 3)]}"/>`;
    s += `<rect x="-2400" y="1360" width="6200" height="40" fill="#3a2a28"/><rect x="-2400" y="1400" width="6200" height="1400" fill="#3a3640"/>
      ${[...Array(30)].map((_, i) => `<path d="M${-2400 + i * 220},1400l-80,1300" stroke="#33303a" stroke-width="3"/>`).join("")}
      <g transform="translate(860,1400)"><rect x="-110" y="-460" width="220" height="460" fill="#3a2418"/><rect x="-96" y="-446" width="192" height="446" fill="#5a3a24"/><path d="M0,-446V0" stroke="#3a2418" stroke-width="5"/><circle cx="70" cy="-220" r="9" fill="#d8b84a"/>
        <g transform="translate(150,-560)"><path d="M-10,0H20V30" stroke="#2a2a2e" stroke-width="6" fill="none"/><rect x="6" y="30" width="30" height="40" rx="6" fill="#2a2a2e"/><rect x="11" y="36" width="20" height="28" rx="4" fill="#ffd890"/></g></g>
      <g transform="translate(520,1400)"><rect x="-90" y="-150" width="180" height="150" fill="#8a6a42"/><path d="M-90,-150L90,0M90,-150L-90,0" stroke="#6a4a2a" stroke-width="10"/><rect x="-90" y="-150" width="180" height="150" fill="none" stroke="#5a3a1e" stroke-width="10"/></g>
      <g transform="translate(310,1400)"><rect x="-70" y="-110" width="140" height="110" fill="#7a5a36"/><rect x="-70" y="-110" width="140" height="110" fill="none" stroke="#5a3a1e" stroke-width="8"/></g>
      ${[1160, 1290].map((x) => `<g transform="translate(${x},1400)"><path d="M-60,-200Q-74,-100 -60,0H60Q74,-100 60,-200Z" fill="#7a4e2a"/><path d="M-66,-160H66M-70,-40H70" stroke="#4a4a52" stroke-width="10"/><ellipse cy="-200" rx="60" ry="14" fill="#5a3a20"/></g>`).join("")}`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(1500,1900)"><path d="M-120,-300Q-60,-420 40,-300L60,0H-120Z" fill="#14161e"/><circle cx="-50" cy="-340" r="70" fill="#1a1c24"/></g><path d="M-900,180Q400,330 2200,140" stroke="#0a0b10" stroke-width="7" fill="none"/>`);
    put(L.glow, `<g style="mix-blend-mode:screen"><circle cx="1031" cy="890" r="300" fill="url(#jkWarm)" opacity=".65"/><ellipse cx="1000" cy="1420" rx="460" ry="80" fill="url(#jkWarm)" opacity=".35"/><circle cx="260" cy="260" r="260" fill="#c8d8ff" opacity=".06"/></g>`);
  };

  Sets.jkTavern = (L, o = {}) => {
    const id = o.id || "jkv", r = mk(o.seed || 21);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#2a1a14"/>`);
    put(L.far, `<rect x="-2400" y="-600" width="6200" height="2600" fill="#3a2418"/>`);
    let mid = `<rect x="-2400" y="-200" width="6200" height="1600" fill="#6a4a32"/>`;
    for (let x = -2400; x < 3800; x += 120) mid += `<rect x="${x}" y="-200" width="116" height="1600" fill="${["#6e4c34", "#664630", "#72503a"][Math.floor(r() * 3)]}"/>`;
    mid += `<rect x="-2400" y="220" width="6200" height="60" fill="#3a2418"/>${[-1600, -800, 0, 800, 1600, 2400].map((x) => `<rect x="${x}" y="-200" width="70" height="1600" fill="#3a2418"/>`).join("")}`;
    mid += `<g id="${id}-win" transform="translate(1770,700)"><rect x="-150" y="-220" width="300" height="360" rx="140" fill="#1a2440"/><rect x="-150" y="-220" width="300" height="360" rx="140" fill="none" stroke="#3a2418" stroke-width="26"/><path d="M0,-220V140M-150,-20H150" stroke="#3a2418" stroke-width="14"/>
      <circle cx="70" cy="-120" r="20" fill="#f4f0dc" opacity=".8"/></g>
      <g transform="translate(-380,1180)"><rect x="-220" y="-560" width="440" height="560" fill="#7a6a5a"/>${[...Array(8)].map((_, i) => `<rect x="${-220 + (i % 4) * 110}" y="${-560 + Math.floor(i / 4) * 70}" width="106" height="66" fill="#8a7a6a"/>`).join("")}
        <path d="M-140,0V-260Q0,-360 140,-260V0Z" fill="#1a1010"/><path d="M-90,0Q-70,-110 -10,-150Q-30,-70 40,-120Q30,-40 90,0Z" fill="#ff9a3a"/><path d="M-50,0Q-40,-60 0,-90Q10,-40 50,0Z" fill="#ffd060"/></g>
      ${[[400, "#3a6a4a"], [1240, "#6a3a3a"]].map(([x, c]) => `<g transform="translate(${x},420)"><rect x="-70" y="-40" width="140" height="90" rx="6" fill="${c}"/><rect x="-60" y="-30" width="120" height="70" rx="4" fill="#d8c8a0" opacity=".25"/></g>`).join("")}
      <rect x="-2400" y="1180" width="6200" height="1400" fill="#4a3020"/>`;
    put(L.mid, mid);
    let s = `<rect x="-2400" y="1240" width="6200" height="1400" fill="#5a3a26"/>${[...Array(26)].map((_, i) => `<path d="M-2400,${1260 + i * 50}H3800" stroke="#4a2e1c" stroke-width="3"/>`).join("")}
      <rect id="${id}-wall" x="200" y="420" width="700" height="580" fill="#c8a478" opacity=".22"/>
      ${[[290, 1400], [690, 1400]].map(([x, gy]) => `<g transform="translate(${x},${gy})"><path d="M-130,-220V0M130,-220V0" stroke="#4a2e1a" stroke-width="16"/><rect x="-150" y="-236" width="300" height="24" rx="6" fill="#7a5030"/>
        <g transform="translate(-60,-236)"><path d="M-16,0L-12,-40H12L16,0Z" fill="#c8a050"/><ellipse cy="-40" rx="12" ry="4" fill="#f4e4b0"/></g><g transform="translate(60,-236)"><ellipse rx="30" ry="8" fill="#e8e2d6"/><ellipse cy="-4" rx="22" ry="5" fill="#a86a3a"/></g></g>`).join("")}
      ${[[150, 1400], [440, 1400], [560, 1400], [840, 1400]].map(([x, gy]) => `<g transform="translate(${x},${gy})"><rect x="-34" y="-120" width="68" height="16" rx="5" fill="#7a5030"/><path d="M-26,-104L-30,0M26,-104L30,0" stroke="#4a2e1a" stroke-width="10"/></g>`).join("")}`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.set, `<g class="act-front"><g transform="translate(1250,1400)"><rect x="-260" y="-240" width="520" height="240" fill="#6a4228"/>${[...Array(5)].map((_, i) => `<rect x="${-250 + i * 102}" y="-220" width="94" height="200" rx="6" fill="#7a5032"/>`).join("")}
        <rect x="-280" y="-262" width="560" height="30" rx="6" fill="#8a5a34"/><g transform="translate(160,-262)"><rect x="-26" y="-50" width="52" height="50" rx="8" fill="#5a3a24"/><rect x="-30" y="-40" width="60" height="8" fill="#3a3a40"/></g>
        <g transform="translate(-170,-262)"><path d="M-14,0L-10,-36H10L14,0Z" fill="#c8a050"/><ellipse cy="-36" rx="10" ry="4" fill="#f4e4b0"/></g></g></g>`);
    put(L.fg, `<g transform="translate(-200,1950)"><rect x="-160" y="-300" width="320" height="40" rx="10" fill="#3a2214"/><path d="M-120,-260V0M120,-260V0" stroke="#2a180e" stroke-width="20"/></g>
      <g transform="translate(1600,1980)"><path d="M-80,-200Q-90,-100 -80,0H80Q90,-100 80,-200Z" fill="#3a2214"/><ellipse cy="-200" rx="80" ry="20" fill="#2a180e"/></g>`);
    const lamps = [[-900, 360], [100, 330], [1000, 360], [1900, 330]];
    put(L.set, lamps.map(([x, y], k) => `<g id="${id}-lamp${k}" transform="translate(${x},${y})"><path d="M0,-140V-20" stroke="#2a1a10" stroke-width="5"/><rect x="-26" y="-24" width="52" height="64" rx="10" fill="#3a2a1c"/><rect x="-18" y="-16" width="36" height="46" rx="6" fill="#ffd890"/></g>`).join(""));
    put(L.glow, `<g style="mix-blend-mode:screen">${lamps.map(([x, y]) => `<circle cx="${x}" cy="${y + 10}" r="300" fill="url(#jkWarm)" opacity=".55"/>`).join("")}
      <circle cx="-380" cy="1080" r="420" fill="url(#jkWarm)" opacity=".6"/><ellipse cx="500" cy="1420" rx="900" ry="140" fill="url(#jkWarm)" opacity=".22"/></g>`);
  };
})();
