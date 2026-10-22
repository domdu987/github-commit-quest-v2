// Layered sets and creatures for "ค่ายคืนสุดท้าย": the volunteer camp clearing (dusk / night), the deep
// forest at night, the ranger hut, a wild elephant and a green pit viper. Same layer contract as sets.js
// (sky, far, mid, set, fg + glow for light sources). Deterministic: seeded RNG only.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);

  Sets.DEFS += `
    <radialGradient id="fireglow"><stop offset="0" stop-color="#ffb35c" stop-opacity=".75"/><stop offset=".35" stop-color="#ff8a3c" stop-opacity=".28"/><stop offset="1" stop-color="#ff8a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="winglow"><stop offset="0" stop-color="#ffd58a" stop-opacity=".6"/><stop offset="1" stop-color="#ffd58a" stop-opacity="0"/></radialGradient>
    <radialGradient id="phoneglow"><stop offset="0" stop-color="#cfe9f2" stop-opacity=".7"/><stop offset="1" stop-color="#cfe9f2" stop-opacity="0"/></radialGradient>
    <linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe2e6" stop-opacity=".16"/><stop offset="1" stop-color="#cfe2e6" stop-opacity="0"/></linearGradient>
    <radialGradient id="beaconBlue"><stop offset="0" stop-color="#5fa8ff" stop-opacity=".85"/><stop offset="1" stop-color="#5fa8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="dawnsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3e4d6e"/><stop offset=".55" stop-color="#b88a8a"/><stop offset="1" stop-color="#f2c08a"/></linearGradient>
    <linearGradient id="nightsky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c161d"/><stop offset=".6" stop-color="#1a2d38"/><stop offset="1" stop-color="#2b4552"/></linearGradient>`;

  // ---------- vegetation ----------
  function pine(x, base, h, w, col, shade) {
    let t = `<rect x="${x - w * 0.06}" y="${base - h * 0.3}" width="${w * 0.12}" height="${h * 0.3}" fill="${shade}"/>`;
    for (let i = 0; i < 4; i++) {
      const top = base - h + i * h * 0.18, bot = base - h * 0.22 - (3 - i) * h * 0.05, cw = w * (0.45 + i * 0.18);
      t += `<path d="M${x},${top}L${x + cw / 2},${bot}Q${x},${bot + h * 0.04} ${x - cw / 2},${bot}Z" fill="${col}"/>`;
      t += `<path d="M${x},${top}L${x + cw / 2},${bot}Q${x + cw * 0.2},${bot + h * 0.02} ${x + cw * 0.08},${bot}Z" fill="${shade}" opacity=".7"/>`;
    }
    return t;
  }
  function broad(x, base, h, col, shade, trunk) { // tropical tree: tall trunk, layered crown
    const w = h * 0.55;
    let t = `<path d="M${x - 14},${base}C${x - 8},${base - h * 0.4} ${x - 18},${base - h * 0.6} ${x},${base - h * 0.75}C${x + 18},${base - h * 0.6} ${x + 8},${base - h * 0.4} ${x + 14},${base}Z" fill="${trunk}"/>`;
    t += `<ellipse cx="${x}" cy="${base - h * 0.8}" rx="${w * 0.6}" ry="${h * 0.2}" fill="${col}"/>`;
    t += `<ellipse cx="${x - w * 0.35}" cy="${base - h * 0.72}" rx="${w * 0.38}" ry="${h * 0.14}" fill="${col}"/>`;
    t += `<ellipse cx="${x + w * 0.35}" cy="${base - h * 0.74}" rx="${w * 0.4}" ry="${h * 0.15}" fill="${shade}"/>`;
    t += `<ellipse cx="${x + w * 0.1}" cy="${base - h * 0.92}" rx="${w * 0.36}" ry="${h * 0.12}" fill="${col}"/>`;
    return t;
  }
  function tufts(r, x0, x1, base, col, n = 1) {
    let d = "";
    for (let x = x0; x < x1; x += 40 + r() * 70) {
      const h = (30 + r() * 50) * n;
      d += `M${x},${base}q${-6},${-h * 0.6} ${-14},${-h}M${x},${base}q2,${-h * 0.7} 4,${-h * 1.1}M${x},${base}q8,${-h * 0.6} ${18},${-h * 0.9}`;
    }
    return `<path d="${d}" stroke="${col}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  }
  function fern(x, base, s, col) {
    let t = "";
    for (let k = -3; k <= 3; k++) t += `<path d="M${x},${base}Q${x + k * 30 * s},${base - 120 * s} ${x + k * 70 * s},${base - (60 + (3 - Math.abs(k)) * 30) * s}" stroke="${col}" stroke-width="${10 * s}" fill="none" stroke-linecap="round"/>`;
    return t;
  }
  function stars(r, n) {
    let s = "";
    for (let i = 0; i < n; i++) s += `<circle cx="${r() * 2200 - 560}" cy="${r() * 900}" r="${0.8 + r() * 1.8}" fill="#f4ecd8" opacity="${0.3 + r() * 0.6}"/>`;
    return s;
  }

  // ---------- props ----------
  function tent(x, y, s, col, shade, lit) {
    return `<g transform="translate(${x},${y}) scale(${s})"><path d="M-170,0Q-150,-200 0,-220Q150,-200 170,0Z" fill="${col}" ${OUT}/>
      <path d="M0,-220Q60,-200 170,0H60Q50,-120 0,-220Z" fill="${shade}" opacity=".6"/>
      <path d="M-60,0Q-40,-130 0,-150Q40,-130 60,0Z" fill="${lit ? "#ffcf7a" : "#2a1f1a"}" ${OUT}/><path d="M0,-150V0" stroke="${INK}" stroke-width="3"/>
      <path d="M-170,0l-40,14M170,0l40,14" stroke="${INK}" stroke-width="3"/></g>`;
  }
  function van(id, x, y, s, hood, flip) {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${flip ? -s : s},${s})">
      <path d="M-330,-60V-250Q-330,-300 -270,-305H170Q230,-300 260,-230L320,-140Q340,-120 340,-90V-60Z" fill="#e8e0cc" ${OUT}/>
      <path d="M-300,-150H330" stroke="#b9cdd3" stroke-width="18"/><path d="M-330,-110H340" stroke="#c9bfa8" stroke-width="5"/>
      ${[-280, -150, -20].map((wx) => `<rect x="${wx}" y="-280" width="110" height="90" rx="10" fill="#22303a" ${OUT}/>`).join("")}
      <path d="M120,-280H190Q220,-278 240,-230L262,-190H120Z" fill="#22303a" ${OUT}/>
      ${hood ? `<path d="M262,-190L300,-330L350,-300L330,-150Z" fill="#d8cfb8" ${OUT}/>` : ""}
      <circle cx="-200" cy="-60" r="58" fill="#2a2420" ${OUT}/><circle cx="-200" cy="-60" r="24" fill="#8a8a84"/>
      <circle cx="220" cy="-60" r="58" fill="#2a2420" ${OUT}/><circle cx="220" cy="-60" r="24" fill="#8a8a84"/>
      <rect x="310" y="-150" width="30" height="22" rx="6" fill="#f2c55c" ${OUT}/>
      <text x="${flip ? 60 : -60}" y="-118" transform="scale(${flip ? -1 : 1},1)" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#4f8f86">ค่ายอาสา</text></g>`;
  }
  function campfire(id, x, y, s, lit) {
    return `<g transform="translate(${x},${y}) scale(${s})">
      ${[-80, -48, -10, 30, 66, 92].map((sx, i) => `<ellipse cx="${sx}" cy="${-6 + (i % 2) * 6}" rx="26" ry="16" fill="#6d6a62" ${OUT}/>`).join("")}
      <path d="M-70,-10L60,-40M-60,-40L70,-8" stroke="#4a3426" stroke-width="22" stroke-linecap="round"/>
      <g id="${id}" opacity="${lit ? 1 : 0}"><path class="fl1" d="M-50,-30Q-60,-110 -10,-170Q-20,-110 10,-90Q20,-140 50,-160Q40,-90 60,-30Z" fill="#f08a3c"/>
        <path class="fl2" d="M-30,-30Q-34,-90 0,-130Q4,-80 20,-70Q30,-100 40,-110Q46,-60 40,-30Z" fill="#f2c55c"/>
        <path class="fl3" d="M-14,-30Q-14,-66 4,-84Q14,-60 20,-30Z" fill="#fff1c4"/></g></g>`;
  }
  function bannerPoles(x0, x1, y, text, col) {
    return `<rect x="${x0 - 8}" y="${y - 420}" width="16" height="420" fill="#4a3426" ${OUT}/><rect x="${x1 - 8}" y="${y - 420}" width="16" height="420" fill="#4a3426" ${OUT}/>
      <path d="M${x0},${y - 400}Q${(x0 + x1) / 2},${y - 360} ${x1},${y - 400}V${y - 320}Q${(x0 + x1) / 2},${y - 280} ${x0},${y - 320}Z" fill="${col}" ${OUT}/>
      <text x="${(x0 + x1) / 2}" y="${y - 328}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#f4ecd8">${text}</text>`;
  }
  function stringLights(x0, x1, y, lit) {
    let s = `<path d="M${x0},${y}Q${(x0 + x1) / 2},${y + 80} ${x1},${y}" fill="none" stroke="${INK}" stroke-width="3"/>`;
    for (let k = 1; k < 10; k++) {
      const u = k / 10, bx = x0 + (x1 - x0) * u, by = y + 160 * u * (1 - u) * 1.0 + 6;
      s += `<circle class="bulb" data-i="${k - 1}" cx="${bx}" cy="${by}" r="9" fill="${lit ? "#ffd58a" : "#c9bfa8"}" ${OUT}/>`;
    }
    return s;
  }
  function signpost(x, y, text) {
    return `<g transform="translate(${x},${y})"><rect x="-8" y="-230" width="16" height="230" fill="#4a3426" ${OUT}/>
      <rect x="-110" y="-240" width="220" height="80" rx="8" fill="#5f7d5a" ${OUT}/><text x="0" y="-190" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#f4ecd8">${text}</text></g>`;
  }

  // ---------------- camp clearing (dusk or night) ----------------
  function camp(L, o = {}) {
    const r = mk(o.seed || 31);
    const night = o.time === "night";
    const C = night
      ? { ridge: ["#1d2d38", "#17242d"], tree: ["#18262c", "#132026", "#0f191e"], pine: ["#1a2a31", "#152228"], ground: "#17231b", dirt: "#2b2a22", grass: "#0f1913" }
      : { ridge: ["#6a5470", "#56465e"], tree: ["#4a4a48", "#3d3d3f", "#352c28"], pine: ["#4e4a55", "#433f4a"], ground: "#6f7a4a", dirt: "#9a8460", grass: "#56613a" };
    put(L.sky, `<rect x="-600" y="0" width="2280" height="1920" fill="${night ? "url(#nightsky2)" : "url(#duskSky)"}"/>` + (night
      ? `${stars(r, 160)}<circle cx="${o.moonX ?? 820}" cy="300" r="240" fill="url(#moonhalo)"/><circle cx="${o.moonX ?? 820}" cy="300" r="54" fill="#f4ecd8"/>`
      : `<circle cx="300" cy="1020" r="340" fill="url(#sunhalo)"/><circle cx="300" cy="1020" r="96" fill="#ffcf8a"/>`));
    put(L.far, `<path d="M-700,1180Q-300,880 100,1060T800,980T1700,1080V1320H-700Z" fill="${C.ridge[0]}"/>
      <path d="M-700,1250Q-200,1080 300,1180T1300,1140T1800,1200V1330H-700Z" fill="${C.ridge[1]}"/>` +
      Array.from({ length: 30 }, (_, i) => pine(-680 + i * 85 + r() * 40, 1280, 160 + r() * 120, 70 + r() * 30, C.pine[0], C.pine[1])).join(""));
    let mid = "";
    for (let x = -700; x < 1900; x += 150 + r() * 120) mid += broad(x, 1440, 520 + r() * 300, C.tree[0], C.tree[1], C.tree[2]);
    put(L.mid, mid + `<rect x="-700" y="1380" width="2600" height="80" fill="${C.tree[1]}"/>`);
    put(L.set, `<rect x="-700" y="1420" width="2600" height="520" fill="${C.ground}"/>
      <ellipse cx="560" cy="1600" rx="760" ry="140" fill="${C.dirt}" opacity=".7"/>
      ${tufts(r, -700, 1900, 1440, C.grass)}
      ${bannerPoles(-120, 300, 1460, "ค่ายอาสาสร้างฝาย", night ? "#7a3f2a" : "#c0603e")}
      ${stringLights(300, 980, 1060, night)}<rect x="972" y="1040" width="16" height="420" fill="#4a3426" ${OUT}/>
      ${tent(-60, 1520, 0.9, "#d9773f", "#a8552a", night)}${tent(230, 1500, 0.72, "#4f8f86", "#386b64", false)}
      ${van("van", o.vanX ?? 1180, 1560, 0.95, o.hood, true)}
      ${signpost(o.signX ?? -340, 1520, "เขตอุทยานฯ")}
      <g transform="translate(560,1610)"><rect x="-260" y="-40" width="120" height="40" rx="18" fill="#6b4a3a" ${OUT}/><rect x="150" y="-40" width="120" height="40" rx="18" fill="#6b4a3a" ${OUT}/></g>
      ${campfire("campfire", o.fireX ?? 560, 1630, 0.9, night)}`);
    if (night) {
      put(L.glow, `<circle class="fireglow" cx="${o.fireX ?? 560}" cy="1540" r="620" fill="url(#fireglow)"/>
        ${Array.from({ length: 9 }, (_, k) => { const u = (k + 1) / 10; return `<circle class="bulbglow" data-i="${k}" cx="${300 + 680 * u}" cy="${1066 + 160 * u * (1 - u)}" r="34" fill="url(#winglow)"/>`; }).join("")}
        <circle cx="-60" cy="1440" r="160" fill="url(#winglow)" opacity=".7"/>`);
    }
    put(L.fg, `${tufts(r, -700, 1900, 1940, "#0a120d", 2.4)}${fern(-80, 1960, 1.6, "#0b140f")}${fern(1180, 1960, 1.8, "#0b140f")}`);
    return { ground: 1560 };
  }

  // ---------------- deep forest at night (wide, for walks) ----------------
  function forest(L, o = {}) {
    const r = mk(o.seed || 7);
    const W = o.width || 4200;
    put(L.sky, `<rect x="-800" y="0" width="${W + 1600}" height="1920" fill="url(#nightsky2)"/>${stars(r, 90)}
      <circle cx="${o.moonX ?? 780}" cy="330" r="260" fill="url(#moonhalo)"/><circle cx="${o.moonX ?? 780}" cy="330" r="64" fill="#f4ecd8"/>`);
    let far = `<rect x="-800" y="1050" width="${W + 1600}" height="260" fill="url(#fogg)"/>`;
    for (let x = -800; x < W; x += 70 + r() * 60) far += pine(x, 1300, 380 + r() * 260, 150 + r() * 80, "#29434d", "#223943");
    for (let k = 0; k < 6; k++) { const sx = -400 + k * 700 + r() * 300; far += `<path d="M${sx},0L${sx + 140},0L${sx + 520},1500L${sx + 260},1500Z" fill="url(#shaft)"/>`; }
    put(L.far, far);
    let mid = "";
    for (let x = -800; x < W; x += 160 + r() * 140) mid += pine(x, 1470, 620 + r() * 360, 240 + r() * 120, "#1d323a", "#172930");
    mid += Array.from({ length: 26 }, (_, i) => `<circle class="ffly" cx="${-400 + r() * (W + 400)}" cy="${900 + r() * 520}" r="${3 + r() * 3}" fill="#e9f5b0"/>`).join("");
    put(L.mid, mid + `<rect x="-800" y="1380" width="${W + 1600}" height="200" fill="url(#fogg)" opacity=".8"/>`);
    let set = `<rect x="-800" y="1480" width="${W + 1600}" height="460" fill="#16252c"/>`;
    if (o.path !== false) set += `<path class="trail" d="M-800,1560Q700,1500 1400,1540T3000,1530T${W + 800},1540V1600Q3200,1640 2400,1610Q1600,1640 700,1600T-800,1620Z" fill="#3b4f52" opacity="${o.pathFade ?? 1}"/>`;
    for (let x = -800; x < W; x += 520 + r() * 300) {
      if (o.bigTree !== undefined && Math.abs(x - o.bigTree) < 500) continue;
      const w = 70 + r() * 40;
      set += `<path d="M${x},1560V0h${w}V1560Z" fill="#101c22"/><path d="M${x + w * 0.62},1560V0h${w * 0.38}V1560Z" fill="#0b151a"/><path d="M${x - 40},1560q${w / 2 + 40},-40 ${w + 80},0Z" fill="#101c22"/>`;
    }
    set += tufts(r, -800, W, 1500, "#203238");
    if (o.bigTree !== undefined) { // huge buttressed trunk to hide behind
      const x = o.bigTree;
      set += `<path d="M${x - 150},1600C${x - 120},1300 ${x - 110},600 ${x - 100},-50H${x + 110}C${x + 120},600 ${x + 130},1300 ${x + 160},1600Z" fill="#14232a" ${OUT}/>
        <path d="M${x + 30},-50C${x + 50},600 ${x + 70},1300 ${x + 100},1600H${x + 160}C${x + 130},1300 ${x + 120},600 ${x + 110},-50Z" fill="#0d181d"/>
        <path d="M${x - 150},1600Q${x - 260},1560 ${x - 330},1610L${x - 140},1460ZM${x + 160},1600Q${x + 280},1560 ${x + 350},1616L${x + 140},1450Z" fill="#14232a" ${OUT}/>
        <path d="M${x - 60},1200q20,-80 0,-160M${x + 40},900q-16,-60 4,-120M${x - 30},500q14,-40 -6,-90" stroke="#0a1418" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M${x - 100},200q-60,200 -40,480" stroke="#2a4a3a" stroke-width="7" fill="none"/>
        <path d="M${x + 104},-50C${x + 114},600 ${x + 124},1300 ${x + 154},1596" stroke="#55737b" stroke-width="7" fill="none" opacity=".8"/>`;
    }
    put(L.set, set);
    if (o.hut !== undefined) { // ranger station far down the trail, window lit
      const hx = o.hut;
      put(L.mid, `<g transform="translate(${hx},1400) scale(.55)"><rect x="-200" y="-260" width="400" height="260" fill="#3b2c22" ${OUT}/><path d="M-250,-250L0,-420L250,-250Z" fill="#2a1e17" ${OUT}/>
        <rect x="-150" y="-200" width="110" height="90" fill="#ffd58a" ${OUT}/><rect x="40" y="-200" width="90" height="200" fill="#2a1e17" ${OUT}/>
        <rect x="-220" y="-330" width="160" height="50" fill="#5f7d5a" ${OUT}/><text x="-140" y="-296" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#f4ecd8">พิทักษ์ป่า</text></g>`);
      L.mid.insertAdjacentHTML("beforeend", `<circle class="hutglow" cx="${hx - 52}" cy="${1400 - 85}" r="140" fill="url(#winglow)"/>`);
    }
    let fg = "";
    for (let x = -800; x < W + 800; x += 300 + r() * 260) {
      const y = 1700 + r() * 160, rr = 120 + r() * 100;
      fg += `<ellipse cx="${x}" cy="${y}" rx="${rr}" ry="${rr * 0.55}" fill="#081015"/><ellipse cx="${x + rr * 0.6}" cy="${y - rr * 0.3}" rx="${rr * 0.7}" ry="${rr * 0.4}" fill="#0a1419"/>`;
    }
    if (o.branch !== false) {
      fg += `<path d="M1300,-40C1150,120 1000,170 820,180" stroke="#081015" stroke-width="40" fill="none" stroke-linecap="round"/>`;
      for (let i = 0; i < 7; i++) fg += `<ellipse cx="${880 + i * 70}" cy="${170 - i * 18 + (i % 2) * 30}" rx="70" ry="28" fill="#0a1419" transform="rotate(${-20 + i * 6} ${880 + i * 70} ${170 - i * 18})"/>`;
    }
    put(L.fg, fg);
    return { ground: 1560 };
  }

  // ---------------- ranger hut interior ----------------
  function hut(L, o = {}) {
    const r = mk(o.seed || 41), uid = L.far.id;
    put(L.sky, `<rect x="-600" y="0" width="2280" height="1920" fill="#241b16"/>`);
    // window view (forest at night); the final shot puts a figure inside .winview
    let view = `<rect x="560" y="420" width="440" height="520" fill="#1a2d38"/><circle cx="900" cy="500" r="30" fill="#f4ecd8"/>`;
    for (let x = 520; x < 1060; x += 50 + r() * 40) view += pine(x, 900, 220 + r() * 140, 90 + r() * 40, "#203a44", "#1a313a");
    view += `<rect x="560" y="860" width="440" height="80" fill="#13222a"/>`;
    put(L.far, `<rect x="-600" y="0" width="2280" height="1500" fill="url(#planks)" opacity=".9"/>
      <clipPath id="${uid}-wclip"><rect x="560" y="420" width="440" height="520"/></clipPath>
      <g clip-path="url(#${uid}-wclip)"><g class="winview">${view}</g></g>
      <rect x="560" y="420" width="440" height="520" fill="none" ${OUT} stroke-width="14"/><path d="M780,420V940M560,680H1000" stroke="${INK}" stroke-width="10"/>
      <rect x="540" y="940" width="480" height="30" fill="#4a3426" ${OUT}/>
      <rect x="-120" y="380" width="420" height="300" fill="#e9dcc0" ${OUT}/><path d="M-90,440q80,40 140,-10t160,40M-60,560q100,-30 180,10t110,-20" stroke="#5f7d5a" stroke-width="6" fill="none"/>
      ${[[-40, 470], [90, 520], [200, 600]].map(([px, py]) => `<circle cx="${px}" cy="${py}" r="10" fill="#e8705a" ${OUT}/>`).join("")}
      <text x="90" y="660" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="${INK}">แผนที่เส้นทางเดินป่า</text>
      <rect x="-120" y="200" width="420" height="80" fill="#5f7d5a" ${OUT}/><text x="90" y="254" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#f4ecd8">หน่วยพิทักษ์ป่า</text>
      <rect x="-600" y="1480" width="2280" height="440" fill="url(#floorb)"/>`);
    put(L.mid, `<g><rect x="80" y="1210" width="560" height="30" fill="#6b4a3a" ${OUT}/><rect x="110" y="1240" width="26" height="260" fill="#4a3426" ${OUT}/><rect x="584" y="1240" width="26" height="260" fill="#4a3426" ${OUT}/>
      <g id="radio"><rect x="140" y="1100" width="220" height="110" rx="12" fill="#3d3833" ${OUT}/><rect x="160" y="1120" width="110" height="50" rx="6" fill="#7fd1b9" opacity=".8"/>
        <circle cx="315" cy="1145" r="22" fill="#2a2420" ${OUT}/><path d="M340,1100L380,960" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle class="led" cx="170" cy="1190" r="7" fill="#e8705a"/>
        <path d="M200,1210q-10,60 30,70t60,-40" stroke="${INK}" stroke-width="5" fill="none"/></g>
      <g transform="translate(470,1150)"><rect x="-50" y="-60" width="100" height="60" rx="8" fill="#f4ecd8" ${OUT}/><path d="M0,-52v44M-22,-30h44" stroke="#e8705a" stroke-width="10"/></g></g>
      <g id="lantern"><path d="M-160,0V300" stroke="${INK}" stroke-width="5"/><rect x="-196" y="300" width="72" height="100" rx="14" fill="#ffd58a" ${OUT}/><rect x="-206" y="290" width="92" height="18" rx="6" fill="#4a3426" ${OUT}/></g>`);
    put(L.glow, `<circle class="lampglow" cx="-160" cy="350" r="520" fill="url(#lampglow)" opacity=".55"/><circle cx="215" cy="1145" r="160" fill="url(#phoneglow)" opacity=".35"/>`);
    put(L.fg, `<rect x="-600" y="1800" width="2280" height="200" fill="#120c09"/><rect x="1060" y="-20" width="140" height="1960" fill="#120c09"/>`);
    return { ground: 1500 };
  }

  // ---------------- close on the hut window (final shot) ----------------
  function hutWindow(L, o = {}) {
    const r = mk(o.seed || 43), uid = L.far.id;
    put(L.sky, `<rect x="-600" y="0" width="2280" height="1920" fill="#241b16"/>`);
    put(L.far, `<rect x="-600" y="0" width="2280" height="1920" fill="url(#planks)" opacity=".9"/>`);
    let view = `<rect x="140" y="330" width="800" height="900" fill="#1a2d38"/><circle cx="800" cy="450" r="170" fill="url(#moonhalo)"/><circle cx="800" cy="450" r="40" fill="#f4ecd8"/>`;
    for (let x = 100; x < 1000; x += 60 + r() * 50) view += pine(x, 1090, 300 + r() * 220, 120 + r() * 50, "#203a44", "#1a313a");
    view += `<rect x="140" y="1070" width="800" height="200" fill="#13222a"/><rect x="100" y="980" width="900" height="140" fill="url(#fogg)"/>`;
    put(L.set, `<clipPath id="${uid}-bw"><rect x="140" y="330" width="800" height="900"/></clipPath>
      <g clip-path="url(#${uid}-bw)"><g class="winview">${view}</g></g>
      <rect x="140" y="330" width="800" height="900" fill="none" ${OUT} stroke-width="24"/><path d="M540,330V1230M140,780H940" stroke="#3b2c22" stroke-width="20"/>
      <rect x="100" y="1228" width="880" height="48" fill="#4a3426" ${OUT}/>`);
    put(L.glow, `<circle cx="-120" cy="900" r="700" fill="url(#lampglow)" opacity=".35"/>`);
    put(L.fg, `<path d="M-120,1960V1820Q-110,1700 40,1690Q60,1560 160,1550Q270,1545 290,1670Q420,1690 450,1820V1960Z" fill="#06090b"/>
      <path d="M700,1960V1830Q720,1720 840,1700Q830,1580 930,1560Q1050,1556 1066,1680Q1180,1700 1200,1830V1960Z" fill="#06090b"/>`);
    return { ground: 1500 };
  }

  // ---------------- aerial forest map (top-down) for the zoom-out route shots ----------------
  function forestMap(L, o = {}) {
    const r = mk(o.seed || 51), uid = L.far.id;
    const P = o.points || { camp: [300, 1520], lost: [520, 1060], you: [640, 900], post: [790, 380], zone: [720, 640], thing: [520, 1040] };
    let crowns = "";
    for (let i = 0; i < 520; i++) {
      const x = r() * 1500 - 210, y = r() * 2300 - 190;
      const near = (q, d) => Math.hypot(x - q[0], y - q[1]) < d;
      if (near(P.camp, 170) || near(P.post, 90)) continue;
      const rr = 34 + r() * 46, c = ["#2a4236", "#23392e", "#2f4a3c", "#1f3329"][Math.floor(r() * 4)];
      crowns += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${rr.toFixed(0)}" fill="${c}"/><circle cx="${(x - rr * 0.3).toFixed(0)}" cy="${(y - rr * 0.3).toFixed(0)}" r="${(rr * 0.45).toFixed(0)}" fill="#3a5a48" opacity=".55"/>`;
    }
    const lbl = (x, y, t, c = "#f4ecd8", sz = 30) => `<g class="mlabel"><rect x="${x - t.length * sz * 0.29 - 14}" y="${y - sz - 6}" width="${t.length * sz * 0.58 + 28}" height="${sz + 18}" rx="${(sz + 18) / 2}" fill="rgba(10,14,16,.78)" stroke="${c}" stroke-width="2.5"/>
      <text x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${sz}" fill="${c}">${t}</text></g>`;
    put(L.set, `<rect x="-400" y="-400" width="1880" height="2720" fill="#16241e"/>
      ${Array.from({ length: 7 }, (_, i) => `<path d="M-300,${300 + i * 260}q300,-90 700,10t900,-40" fill="none" stroke="#2b4034" stroke-width="3" opacity=".6"/>`).join("")}
      <path d="M1400,-200C1100,300 1000,560 1180,900S700,1500 860,2300" fill="none" stroke="#2a4656" stroke-width="70" stroke-linecap="round"/>
      <path d="M1400,-200C1100,300 1000,560 1180,900S700,1500 860,2300" fill="none" stroke="#3b6274" stroke-width="30" stroke-linecap="round" opacity=".6"/>
      ${crowns}
      <ellipse cx="${P.camp[0]}" cy="${P.camp[1]}" rx="150" ry="110" fill="#6b6a4a"/>${[[-50, -20, "#d9773f"], [30, 10, "#4f8f86"], [-10, 50, "#e8e0cc"]].map(([dx, dy, c]) => `<path d="M${P.camp[0] + dx - 26},${P.camp[1] + dy + 18}L${P.camp[0] + dx},${P.camp[1] + dy - 22}L${P.camp[0] + dx + 26},${P.camp[1] + dy + 18}Z" fill="${c}" stroke="#2e2a26" stroke-width="3"/>`).join("")}
      <path class="mtrail" d="M${P.camp[0]},${P.camp[1] - 80}C${P.camp[0] + 40},1340 ${P.lost[0] - 60},1200 ${P.lost[0]},${P.lost[1]}" fill="none" stroke="#e9dcc0" stroke-width="10" stroke-dasharray="4 16" stroke-linecap="round"/>
      <g transform="translate(${P.lost[0]},${P.lost[1]})"><path d="M-22,-22L22,22M22,-22L-22,22" stroke="#e8705a" stroke-width="10" stroke-linecap="round"/></g>
      <g class="mzone"><ellipse cx="${P.zone[0]}" cy="${P.zone[1]}" rx="190" ry="120" fill="rgba(240,160,112,.18)" stroke="#f0a070" stroke-width="5" stroke-dasharray="16 12"/>
        ${[[-60, -20], [10, 30], [70, -30], [-10, -60]].map(([dx, dy]) => `<g transform="translate(${P.zone[0] + dx},${P.zone[1] + dy})"><ellipse rx="14" ry="17" fill="#f0a070" opacity=".85"/>${[-10, 0, 10].map((tx) => `<circle cx="${tx}" cy="-19" r="4" fill="#f0a070"/>`).join("")}</g>`).join("")}</g>
      <g class="mpost" transform="translate(${P.post[0]},${P.post[1]})"><circle r="90" fill="url(#winglow)"/><rect x="-36" y="-26" width="72" height="44" fill="#6b4a3a" stroke="#2e2a26" stroke-width="4"/><path d="M-46,-24L0,-58L46,-24Z" fill="#3b2c22" stroke="#2e2a26" stroke-width="4"/><rect x="-24" y="-14" width="18" height="16" fill="#ffd58a"/></g>
      <path id="${uid}-route" class="mroute" d="M${P.you[0]},${P.you[1]}C${P.you[0] + 60},${P.you[1] - 120} ${P.zone[0] - 80},${P.zone[1] + 60} ${P.zone[0]},${P.zone[1]}S${P.post[0] - 40},${P.post[1] + 120} ${P.post[0]},${P.post[1] + 40}" fill="none" stroke="#f2c55c" stroke-width="12" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400"/>
      ${o.road ? `<path d="M1000,1960C960,1560 880,1140 ${P.post[0] + 90},${P.post[1] + 40}" fill="none" stroke="#5a5448" stroke-width="34" stroke-linecap="round"/>
        <path d="M1000,1960C960,1560 880,1140 ${P.post[0] + 90},${P.post[1] + 40}" fill="none" stroke="#8a8270" stroke-width="4" stroke-dasharray="20 18"/>
        <g class="mcut" transform="translate(858,1150)"><circle r="44" fill="rgba(232,112,90,.25)"/><path d="M-26,-26L26,26M26,-26L-26,26" stroke="#e8705a" stroke-width="12" stroke-linecap="round"/></g>
        <g class="mamb" transform="translate(945,1420)"><rect x="-34" y="-20" width="68" height="40" rx="8" fill="#f4ecd8" stroke="#2e2a26" stroke-width="4"/><path d="M-6,0h12M0,-6v12" stroke="#e8705a" stroke-width="6"/>
          <rect class="mlb" x="-20" y="-30" width="40" height="10" rx="4" fill="#e8705a"/></g>` : ""}
      <g class="mthing" transform="translate(${P.thing[0]},${P.thing[1]})"><circle r="60" fill="#d8ff9a" opacity=".12"/><ellipse cx="-12" cy="0" rx="9" ry="6" fill="#e9ffc0"/><ellipse cx="12" cy="0" rx="9" ry="6" fill="#e9ffc0"/></g>
      <g class="myou" transform="translate(${P.you[0]},${P.you[1]})"><circle class="mping" r="30" fill="none" stroke="#7fd1b9" stroke-width="6"/><circle cx="-14" r="15" fill="#9c4a3c" stroke="#f4ecd8" stroke-width="4"/><circle cx="14" r="15" fill="#4f8f86" stroke="#f4ecd8" stroke-width="4"/></g>
      ${lbl(P.camp[0], P.camp[1] + 170, "แคมป์")}${lbl(P.lost[0] - 10, P.lost[1] + 80, "หลงทางตรงนี้", "#e8705a", 26)}
      ${lbl(P.you[0] + 40, P.you[1] + 90, "คุณอยู่ที่นี่", "#7fd1b9")}${lbl(P.zone[0] + 30, P.zone[1] - 140, "เขตช้างป่า", "#f0a070")}
      ${lbl(P.post[0] - 20, P.post[1] - 90, "ป้อมพิทักษ์ป่า", "#f2c55c")}${o.road ? lbl(800, 1240, "ถนนขาด", "#e8705a") + lbl(770, 1500, "รถกู้ภัย · รอถึงเช้า", "#f4ecd8", 26) : ""}
      <g class="mdist">${lbl(P.zone[0] + 230, P.zone[1] + 120, "≈ 1 กม.", "#f2c55c", 34)}</g>
      <g transform="translate(960,160)"><circle r="56" fill="rgba(10,14,16,.7)" stroke="#f4ecd8" stroke-width="3"/><path d="M0,-44L12,0L0,44L-12,0Z" fill="#f4ecd8"/><path d="M0,-44L12,0H-12Z" fill="#e8705a"/><text y="-60" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="#f4ecd8">N</text></g>`);
    return { ground: 1500 };
  }
  // animate the map: route draws, zone and post pulse, "you" pings, the thing's eyes blink
  function animMap(tl, scope, t0, dur, o = {}) {
    const rt = document.querySelector(`${scope} .mroute`);
    tl.to(rt, { attr: { "stroke-dashoffset": 0 }, duration: o.draw || 1.6, ease: "power1.inOut" }, t0 + (o.drawAt ?? 2.0));
    tl.fromTo(`${scope} .mping`, { attr: { r: 20 }, opacity: 1 }, { attr: { r: 70 }, opacity: 0, duration: 0.9, repeat: Math.ceil(dur / 0.9), ease: "power2.out", immediateRender: false }, t0);
    tl.fromTo(`${scope} .mzone`, { opacity: 0.55 }, { opacity: 1, duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, immediateRender: false }, t0);
    tl.fromTo(`${scope} .mdist`, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(3)", immediateRender: false }, t0 + (o.drawAt ?? 2.0) + (o.draw || 1.6));
    document.querySelectorAll(`${scope} .mlabel`).forEach((g, i) => tl.fromTo(g, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }, t0 + 0.9 + i * 0.18));
    for (let k = 0.6; k < dur; k += 1.3) { tl.set(`${scope} .mthing`, { opacity: 0 }, t0 + k); tl.set(`${scope} .mthing`, { opacity: 1 }, t0 + k + 0.15); }
    if (o.circle) { // the eyes prowl round the post
      const th = document.querySelector(`${scope} .mthing`), c = { a: 0 };
      tl.to(c, { a: Math.PI * 2 * (dur / 4), duration: dur, ease: "none", onUpdate: () => th.setAttribute("transform", `translate(${(o.circle[0] + Math.cos(c.a) * 170).toFixed(1)},${(o.circle[1] + Math.sin(c.a) * 130).toFixed(1)})`) }, t0);
    }
    if (document.querySelector(`${scope} .mlb`)) tl.fromTo(`${scope} .mlb`, { attr: { fill: "#e8705a" } }, { attr: { fill: "#5fa8e8" }, duration: 0.25, repeat: Math.ceil(dur / 0.25), yoyo: true, immediateRender: false }, t0);
  }

  // ---------------- the ranger post, front view at night ----------------
  function hutFront(L, o = {}) {
    const r = mk(o.seed || 61);
    if (o.dawn) put(L.sky, `<rect x="-600" y="0" width="2280" height="1920" fill="url(#dawnsky)"/><circle cx="200" cy="1180" r="380" fill="url(#sunhalo)"/><circle cx="200" cy="1180" r="70" fill="#ffd9a0"/>`);
    else put(L.sky, `<rect x="-600" y="0" width="2280" height="1920" fill="url(#nightsky2)"/>${stars(r, 80)}<circle cx="860" cy="260" r="200" fill="url(#moonhalo)"/><circle cx="860" cy="260" r="48" fill="#f4ecd8"/>`);
    let far = `<rect x="-600" y="1000" width="2280" height="260" fill="url(#fogg)"/>`;
    for (let x = -600; x < 1700; x += 70 + r() * 60) far += pine(x, 1260, 360 + r() * 240, 150 + r() * 80, "#29434d", "#223943");
    put(L.far, far);
    let mid = "";
    for (let x = -600; x < 1700; x += 170 + r() * 140) if (x < 80 || x > 1000) mid += pine(x, 1440, 620 + r() * 300, 240 + r() * 110, "#1d323a", "#172930");
    put(L.mid, mid);
    put(L.set, `<rect x="-600" y="1440" width="2280" height="1100" fill="#16252c"/><path d="M340,2400L470,1500H610L740,2400Z" fill="#3b4f52" opacity=".8"/>
      <g id="hutf"><path d="M130,1470V860H950V1470Z" fill="url(#planks)" stroke="${INK}" stroke-width="6"/>
        <path d="M60,880L540,560L1020,880Z" fill="#33251c" stroke="${INK}" stroke-width="6"/><path d="M100,870L540,600L980,870" fill="none" stroke="#5c4433" stroke-width="10"/>
        <path d="M800,690V420M800,430l60,40" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><circle cx="800" cy="420" r="9" fill="#e8705a"/>
        <rect x="320" y="900" width="440" height="80" fill="#5f7d5a" stroke="${INK}" stroke-width="5"/><text x="540" y="954" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#f4ecd8">หน่วยพิทักษ์ป่า</text>
        <rect id="hutdoor" x="450" y="1040" width="180" height="420" fill="#2a1e17" stroke="${INK}" stroke-width="6"/><circle cx="605" cy="1260" r="10" fill="#c9bfa8"/>
        <rect x="190" y="1060" width="200" height="170" fill="#ffd58a" stroke="${INK}" stroke-width="6"/><path d="M290,1060V1230M190,1145H390" stroke="${INK}" stroke-width="7"/>
        <rect x="700" y="1060" width="200" height="170" fill="#1b2328" stroke="${INK}" stroke-width="6"/><path d="M800,1060V1230M700,1145H900" stroke="${INK}" stroke-width="7"/>
        <rect x="100" y="1460" width="880" height="34" fill="#4a3426" stroke="${INK}" stroke-width="5"/><rect x="420" y="1492" width="240" height="26" fill="#3b2c22" stroke="${INK}" stroke-width="4"/>
        <g id="hutlamp"><path d="M680,1000V1030" stroke="${INK}" stroke-width="4"/><rect x="664" y="1030" width="32" height="42" rx="7" fill="#ffd58a" stroke="${INK}" stroke-width="4"/></g></g>`);
    put(L.glow, `<circle class="hwglow" cx="290" cy="1145" r="260" fill="url(#winglow)"/><circle cx="680" cy="1052" r="120" fill="url(#winglow)" opacity=".7"/>`);
    put(L.fg, `${tufts(r, -600, 1700, 1930, "#0a120d", 2.2)}${fern(-60, 1960, 1.7, "#0b140f")}${fern(1150, 1960, 1.8, "#0b140f")}`);
    return { ground: 1500 };
  }

  // ---------------- hospital corridor, daytime ----------------
  function clinic(L, o = {}) {
    put(L.sky, `<rect x="-600" y="0" width="2280" height="1920" fill="#dfe8e2"/>`);
    put(L.far, `<rect x="-600" y="0" width="2280" height="1180" fill="#e8efe9"/><rect x="-600" y="1180" width="2280" height="320" fill="#b9d3c6"/><path d="M-600,1180H1680" stroke="#8fb3a2" stroke-width="10"/>
      <rect x="560" y="300" width="420" height="560" fill="#bfe0ef" stroke="${INK}" stroke-width="10"/><path d="M770,300V860M560,580H980" stroke="${INK}" stroke-width="8"/>
      ${[0, 1, 2].map((i) => `<path d="M${590 + i * 130},860q30,-160 70,-260q30,90 50,260z" fill="#7fae7a"/>`).join("")}<circle cx="900" cy="380" r="40" fill="#fff6d8"/>
      <rect x="-60" y="380" width="380" height="250" rx="10" fill="#f4ecd8" stroke="${INK}" stroke-width="5"/><text x="130" y="470" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#c8553d">1669</text>
      <text x="130" y="540" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="${INK}">เจ็บป่วยฉุกเฉิน</text>
      <rect x="-600" y="1480" width="2280" height="440" fill="#cfd8d4"/>${Array.from({ length: 12 }, (_, i) => `<path d="M${-600 + i * 200},1480V1920" stroke="#b9c4c0" stroke-width="4"/>`).join("")}`);
    put(L.set, `<g transform="translate(540,1620)"><rect x="-380" y="-120" width="760" height="40" rx="10" fill="#4f8f86" stroke="${INK}" stroke-width="5"/><rect x="-380" y="-260" width="760" height="40" rx="10" fill="#4f8f86" stroke="${INK}" stroke-width="5"/>
      <rect x="-350" y="-80" width="26" height="80" fill="#8a9499" stroke="${INK}" stroke-width="4"/><rect x="324" y="-80" width="26" height="80" fill="#8a9499" stroke="${INK}" stroke-width="4"/></g>`);
    put(L.fg, `<rect x="-600" y="-40" width="2280" height="90" fill="#c9d6d0"/>`);
    return { ground: 1620 };
  }
  // Thai ambulance van facing left (the way it drives in); origin = ground under the middle of the van
  function rescueTruck(id, x, y, s) {
    const wheel = (cx) => `<g transform="translate(${cx},-46)"><circle r="50" fill="#1f2326" stroke="${INK}" stroke-width="5"/><g class="spokes">
        <circle r="24" fill="#b9c2c6" stroke="${INK}" stroke-width="3"/>${[0, 60, 120].map((a) => `<rect x="-3" y="-22" width="6" height="44" fill="#6b7478" transform="rotate(${a})"/>`).join("")}</g></g>`;
    const checks = Array.from({ length: 28 }, (_, i) => `<rect x="${-268 + i * 20}" y="${-118 + (i % 2) * 10}" width="20" height="10" fill="#e8705a"/>`).join("");
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="4" rx="310" ry="24" fill="#060c10" opacity=".45"/>
      <circle class="lbglow lbgr" cx="-120" cy="-300" r="220" fill="url(#beacon)" opacity=".7"/>
      <path d="M-300,-96L-700,-40L-700,10L-300,-60Z" fill="#fff3c8" opacity=".18"/>
      <path d="M-278,-40V-150Q-278,-176 -256,-186L-196,-252Q-184,-264 -164,-264H252Q280,-264 280,-236V-40Z" fill="#f7f5ee" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M-250,-182L-196,-246H-150V-182Z" fill="#22303a" stroke="${INK}" stroke-width="4"/><path d="M-226,-196L-190,-238" stroke="#5f7d8a" stroke-width="6" opacity=".6"/>
      <rect x="-128" y="-246" width="92" height="60" rx="6" fill="#22303a" stroke="${INK}" stroke-width="4"/><rect x="150" y="-246" width="104" height="60" rx="6" fill="#22303a" stroke="${INK}" stroke-width="4"/>
      <rect x="-20" y="-250" width="150" height="206" rx="6" fill="none" stroke="#9aa3a5" stroke-width="4"/><rect x="104" y="-150" width="16" height="6" rx="3" fill="#6b7478"/>
      <rect x="-278" y="-128" width="558" height="30" fill="#f7f5ee"/>${checks}<path d="M-278,-128H280M-278,-98H280" stroke="#c8553d" stroke-width="3"/>
      <text x="-90" y="-148" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#c8553d">รถพยาบาล</text>
      <text x="55" y="-146" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#2f6fb8">1669</text>
      <g transform="translate(55,-212)"><circle r="28" fill="#2f6fb8" stroke="${INK}" stroke-width="3"/>${[0, 60, 120].map((a) => `<rect x="-6" y="-22" width="12" height="44" rx="2" fill="#f7f5ee" transform="rotate(${a})"/>`).join("")}<path d="M0,-16V16" stroke="#2f6fb8" stroke-width="3"/></g>
      <rect x="-292" y="-66" width="44" height="28" rx="8" fill="#8a9499" stroke="${INK}" stroke-width="4"/><rect x="270" y="-66" width="20" height="28" rx="6" fill="#8a9499" stroke="${INK}" stroke-width="4"/>
      <rect x="-284" y="-104" width="24" height="20" rx="5" fill="#ffd58a" stroke="${INK}" stroke-width="3"/><rect x="262" y="-104" width="16" height="20" rx="4" fill="#e8705a" stroke="${INK}" stroke-width="3"/>
      <rect x="-222" y="-196" width="16" height="22" rx="4" fill="#3d3833" stroke="${INK}" stroke-width="3"/>
      <path d="M-230,-40a62,62 0 0 1 124,0M110,-40a62,62 0 0 1 124,0" fill="#2a3135"/>
      ${wheel(-168)}${wheel(172)}
      <rect x="-160" y="-284" width="170" height="22" rx="8" fill="#3d3833" stroke="${INK}" stroke-width="4"/>
      <rect class="lbr" x="-154" y="-282" width="78" height="18" rx="6" fill="#ff4a3a"/><rect class="lbb" x="-70" y="-282" width="78" height="18" rx="6" fill="#3f8fff"/>
      <circle class="lbglow lbgb" cx="-30" cy="-300" r="200" fill="url(#beaconBlue)" opacity=".7"/></g>`;
  }

  // dark mimic silhouette with eyeshine (no rig: it should not move like a person)
  function shade(id, x, y, s) {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-46,0C-58,-160 -50,-330 -36,-430Q0,-470 36,-430C50,-330 58,-160 46,0Z" fill="#05090b" opacity=".95"/>
      <ellipse cx="0" cy="-500" rx="40" ry="50" fill="#05090b"/><path d="M-36,-420Q-90,-300 -84,-170M36,-420Q92,-300 88,-160" stroke="#05090b" stroke-width="22" fill="none" stroke-linecap="round"/>
      <g class="eyes"><circle cx="-14" cy="-506" r="16" fill="#d8ff9a" opacity=".25"/><circle cx="16" cy="-506" r="16" fill="#d8ff9a" opacity=".25"/><ellipse cx="-14" cy="-506" rx="8" ry="5" fill="#e9ffc0"/><ellipse cx="16" cy="-506" rx="8" ry="5" fill="#e9ffc0"/></g></g>`;
  }

  // ---------------- creatures ----------------
  // wild elephant, side view facing left; legs, trunk and ear are animated by animElephant
  function elephant(id, x, y, s) {
    const B = "#4d5c63", Sh = "#3b474e", Rim = "#b7cbd0";
    const leg = (n, lx, back) => `<g id="${id}-l${n}" transform="translate(${lx},-360)"><g><path d="M-48,0H48L44,350Q44,366 26,366H-26Q-44,366 -44,350Z" fill="${back ? Sh : B}" stroke="${Rim}" stroke-width="4"/>
      <path d="M-40,350h80" stroke="#7a8a8e" stroke-width="5" stroke-dasharray="6 12"/></g></g>`;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="6" rx="520" ry="40" fill="#05090b" opacity=".6"/>
      <g id="${id}-bob">${leg(1, 230, true)}${leg(2, -260, true)}
        <path d="M-420,-420C-440,-650 -260,-860 40,-860C300,-860 470,-760 450,-480C440,-380 380,-330 300,-330H-330C-400,-330 -415,-380 -420,-420Z" fill="${B}" stroke="${Rim}" stroke-width="5"/>
        <path d="M-330,-800Q0,-880 330,-790Q420,-740 440,-560" stroke="#dfe9ea" stroke-width="12" fill="none" opacity=".55" stroke-linecap="round"/>
        <path d="M430,-560q60,40 40,170" stroke="${B}" stroke-width="18" fill="none" stroke-linecap="round"/>
        ${leg(3, 180, false)}${leg(4, -300, false)}
        <g id="${id}-head" transform="translate(-380,-640)">
          <g id="${id}-trunk"><path d="M-170,40C-230,180 -220,360 -200,520Q-196,560 -170,560Q-150,556 -152,520C-160,380 -150,220 -90,100Z" fill="${B}" stroke="${Rim}" stroke-width="5"/></g>
          <path d="M-210,-20C-240,-160 -140,-240 -20,-230C80,-220 120,-140 110,-60C100,40 20,120 -90,120C-160,120 -196,60 -210,-20Z" fill="${B}" stroke="${Rim}" stroke-width="5"/>
          <path d="M-120,90Q-190,150 -260,130" stroke="#e8e0cc" stroke-width="22" fill="none" stroke-linecap="round"/>
          <g id="${id}-ear"><path d="M-40,-200C120,-260 220,-120 200,40C190,160 100,220 20,190C40,80 0,-60 -40,-200Z" fill="${Sh}" stroke="${Rim}" stroke-width="5"/></g>
          <circle id="${id}-eye" cx="-120" cy="-60" r="9" fill="#d7e2df"/></g></g></g>`;
  }
  function animElephant(tl, id, t0, dur, o = {}) {
    const c = { t: 0 }, el = (k) => document.getElementById(`${id}-${k}`);
    const step = o.period || 1.5;
    const go = () => {
      const t = c.t, ph = (2 * Math.PI * t) / step, walk = o.walk === false ? 0 : 1;
      [[1, 0], [2, Math.PI], [3, Math.PI], [4, 0]].forEach(([n, off]) => {
        const g = el(`l${n}`).firstElementChild;
        g.setAttribute("transform", `rotate(${(walk * 11 * Math.sin(ph + off)).toFixed(2)})`);
      });
      el("bob").setAttribute("transform", `translate(0 ${(walk * 8 * Math.abs(Math.sin(ph))).toFixed(2)})`);
      el("trunk").setAttribute("transform", `rotate(${(7 * Math.sin(t * 1.3) + (o.raise && t > o.raise ? -30 * Math.min(1, (t - o.raise) / 0.6) : 0)).toFixed(2)} -130 70)`);
      el("ear").setAttribute("transform", `rotate(${(6 * Math.sin(t * 3.1)).toFixed(2)} -20 -180)`);
    };
    tl.to(c, { t: dur, duration: dur, ease: "none", onUpdate: go }, t0);
    go();
  }

  // green pit viper (งูเขียวหางไหม้): body is re-pathed every frame; strike lunges the head at `strike`
  function snake(id, x, y, s) {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path id="${id}-b0" fill="none" stroke="${INK}" stroke-width="30" stroke-linecap="round"/>
      <path id="${id}-b1" fill="none" stroke="#7fae5a" stroke-width="20" stroke-linecap="round"/><path id="${id}-tail" fill="none" stroke="#c8553d" stroke-width="16" stroke-linecap="round"/>
      <g id="${id}-head"><path d="M0,-18C30,-22 52,-8 54,2C52,14 30,22 0,18Z" fill="#7fae5a" ${OUT}/><circle cx="30" cy="-6" r="5" fill="#f2c55c"/><circle cx="31" cy="-6" r="2" fill="${INK}"/>
        <path id="${id}-tongue" d="M54,2h22l8,-7M76,2l8,7" stroke="#c8553d" stroke-width="4" fill="none" stroke-linecap="round"/></g></g>`;
  }
  function animSnake(tl, id, t0, dur, o = {}) {
    const c = { t: 0 }, el = (k) => document.getElementById(`${id}-${k}`);
    const N = 24, len = 360;
    const go = () => {
      const t = c.t;
      const st = o.strike !== undefined ? Math.max(0, Math.min(1, (t - o.strike) / 0.12)) * (1 - Math.max(0, Math.min(1, (t - o.strike - 0.35) / 0.4))) : 0;
      const pts = [];
      for (let i = 0; i <= N; i++) {
        const u = i / N; // 0 = tail, 1 = head
        const amp = 26 * (1 - st * u);
        pts.push([-len + u * (len + st * 150 * u * u), Math.sin(u * 9 - t * 6) * amp * (0.4 + 0.6 * u) - st * 70 * u * u]);
      }
      const d = "M" + pts.map((p) => p.map((v) => v.toFixed(1)).join(",")).join("L");
      el("b0").setAttribute("d", d); el("b1").setAttribute("d", d);
      el("tail").setAttribute("d", "M" + pts.slice(0, 5).map((p) => p.map((v) => v.toFixed(1)).join(",")).join("L"));
      const [hx, hy] = pts[N], [px, py] = pts[N - 1];
      el("head").setAttribute("transform", `translate(${hx.toFixed(1)} ${hy.toFixed(1)}) rotate(${(Math.atan2(hy - py, hx - px) * 180 / Math.PI).toFixed(1)})`);
      el("tongue").setAttribute("opacity", Math.sin(t * 17) > 0.2 ? 1 : 0);
    };
    tl.to(c, { t: dur, duration: dur, ease: "none", onUpdate: go }, t0);
    go();
  }

  // small hand props, attached to a rig's front hand group
  const hand = {
    whistle: `<g transform="translate(0,-4) rotate(-90)"><path d="M-12,-8h22v-6h10a12,12 0 1 1 -12,16H-12z" fill="#e07a4f" ${OUT}/></g>`,
    phone: `<g><rect x="-14" y="-34" width="28" height="50" rx="5" fill="#3d3833" ${OUT}/><rect x="-10" y="-28" width="20" height="36" fill="#cfe9f2"/></g>`,
    camera: `<g><rect x="-30" y="-26" width="60" height="40" rx="7" fill="#3d3833" ${OUT}/><circle cx="4" cy="-6" r="12" fill="#22303a" stroke="#c9bfa8" stroke-width="3"/><rect x="-24" y="-34" width="16" height="8" fill="#3d3833"/></g>`,
    mic: `<g><rect x="-12" y="-30" width="24" height="40" rx="8" fill="#2a2420" ${OUT}/><path d="M0,10q-10,60 30,90" stroke="${INK}" stroke-width="5" fill="none"/></g>`,
  };
  function attach(aid, what) {
    const g = document.getElementById(`${aid}-handF`);
    if (g) g.insertAdjacentHTML("beforeend", hand[what]);
  }

  // looping flame flicker + glow breathing for a lit campfire / lamps inside a shot
  function flicker(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    const rep = (p) => Math.ceil(dur / p) + 1;
    q(".fl1").forEach((el) => tl.fromTo(el, { scaleY: 1, scaleX: 1 }, { scaleY: 1.14, scaleX: 0.92, transformOrigin: "50% 100%", duration: 0.23, repeat: rep(0.23), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".fl2").forEach((el) => tl.fromTo(el, { scaleY: 1.1, x: -3 }, { scaleY: 0.9, x: 4, transformOrigin: "50% 100%", duration: 0.17, repeat: rep(0.17), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".fl3").forEach((el) => tl.fromTo(el, { scaleY: 0.9 }, { scaleY: 1.2, transformOrigin: "50% 100%", duration: 0.13, repeat: rep(0.13), yoyo: true, immediateRender: false }, t0));
    q(".fireglow").forEach((el) => tl.fromTo(el, { opacity: 0.85 }, { opacity: 1, duration: 0.31, repeat: rep(0.31), yoyo: true, immediateRender: false }, t0));
    q(".ffly").forEach((el, i) => tl.fromTo(el, { opacity: 0.1 }, { opacity: 1, duration: 0.6 + (i % 5) * 0.17, repeat: rep(0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 7) * 0.13));
    q(".led").forEach((el) => tl.fromTo(el, { opacity: 1 }, { opacity: 0.2, duration: 0.3, repeat: rep(0.3), yoyo: true, immediateRender: false }, t0));
  }

  Object.assign(Sets, { camp, forest, hut, hutWindow, forestMap, hutFront, clinic });
  Sets.props = Object.assign(Sets.props || {}, { van, tent, campfire, elephant, snake, shade, rescueTruck });
  window.Camp = { animElephant, animSnake, animMap, attach, flicker, pine, hand };
})();
