// Sets and props for "ชั้น 23": a Bangkok condo during an outbreak. A studio living room with the front door,
// the corridor through the door's peephole (with a front-facing face for the jump scare), the bathroom sink
// close-up of a bitten forearm, a bathtub being filled, the building's water system as a cross-section,
// the dead lift panel in the lobby, the fire stairs (side landing and looking down the shaft) and the city at dusk. Same layer contract as sets.js.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);

  Sets.DEFS += `
    <linearGradient id="zWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8d1c6"/><stop offset="1" stop-color="#c4bcae"/></linearGradient>
    <linearGradient id="zTile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dfe7e4"/><stop offset="1" stop-color="#c9d4d0"/></linearGradient>
    <linearGradient id="zChrome" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#eef2f4"/><stop offset=".5" stop-color="#9aa6ad"/><stop offset="1" stop-color="#dfe5e8"/></linearGradient>
    <linearGradient id="zWater" x1="0" x2="1"><stop offset="0" stop-color="#cfe9f2" stop-opacity=".5"/><stop offset=".5" stop-color="#f4fbff" stop-opacity=".9"/><stop offset="1" stop-color="#cfe9f2" stop-opacity=".5"/></linearGradient>
    <linearGradient id="zTub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc3d6" stop-opacity=".75"/><stop offset="1" stop-color="#5f9fb8" stop-opacity=".85"/></linearGradient>
    <linearGradient id="zDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f52"/><stop offset=".55" stop-color="#b8566a"/><stop offset="1" stop-color="#f0a26a"/></linearGradient>
    <linearGradient id="zDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fc7e0"/><stop offset="1" stop-color="#e8eef0"/></linearGradient>
    <linearGradient id="zNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070d"/><stop offset="1" stop-color="#141a2a"/></linearGradient>
    <radialGradient id="zExit"><stop offset="0" stop-color="#4dff9a" stop-opacity=".55"/><stop offset=".5" stop-color="#1fbf6a" stop-opacity=".18"/><stop offset="1" stop-color="#1fbf6a" stop-opacity="0"/></radialGradient>
    <radialGradient id="zPhone"><stop offset="0" stop-color="#cfe6ff" stop-opacity=".7"/><stop offset=".5" stop-color="#9cc4ff" stop-opacity=".2"/><stop offset="1" stop-color="#9cc4ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="zLens" cx=".5" cy=".5" r=".5"><stop offset=".78" stop-color="#000" stop-opacity="0"/><stop offset=".97" stop-color="#000" stop-opacity=".85"/><stop offset="1" stop-color="#000"/></radialGradient>
    <linearGradient id="zRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd8a0" stop-opacity=".42"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></linearGradient>
    <linearGradient id="zRayN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9c4ff" stop-opacity=".22"/><stop offset="1" stop-color="#a9c4ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="zHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfd8d4" stop-opacity="0"/><stop offset=".6" stop-color="#cfd8d4" stop-opacity=".16"/><stop offset="1" stop-color="#cfd8d4" stop-opacity=".05"/></linearGradient>
    <linearGradient id="zCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef6ff" stop-opacity=".28"/><stop offset="1" stop-color="#eef6ff" stop-opacity="0"/></linearGradient>
    <radialGradient id="zGlowW"><stop offset="0" stop-color="#eef6ff" stop-opacity=".9"/><stop offset=".45" stop-color="#dfeaf5" stop-opacity=".3"/><stop offset="1" stop-color="#dfeaf5" stop-opacity="0"/></radialGradient>
    <radialGradient id="zRed"><stop offset="0" stop-color="#ff2a1a" stop-opacity=".55"/><stop offset=".5" stop-color="#c81a10" stop-opacity=".18"/><stop offset="1" stop-color="#c81a10" stop-opacity="0"/></radialGradient>
    <pattern id="zWire" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M0,0L40,40M40,0L0,40" stroke="#c9ccd0" stroke-width="2.5"/></pattern>
    <radialGradient id="zSkinF" cx=".45" cy=".4"><stop offset="0" stop-color="#c6d3bd"/><stop offset=".7" stop-color="#9fb197"/><stop offset="1" stop-color="#7c8d75"/></radialGradient>`;

  // ---------------- city skyline (window view): day / dusk / night, smoke, a hospital with its lights ----------------
  function city(r, time, y0, o = {}) {
    const night = time === "night", dusk = time === "dusk";
    let s = `<rect x="-900" y="-600" width="2900" height="${y0 + 1000}" fill="url(#${night ? "zNight" : dusk ? "zDusk" : "zDay"})"/>`;
    const col = night ? ["#0b0f19", "#111827", "#0d1320"] : dusk ? ["#3a2f45", "#45364f", "#2f2a3c"] : ["#9fb0bc", "#8a9cab", "#b2c0ca"];
    for (let layer = 0; layer < 2; layer++) for (let x = -800; x < 1900; x += 70 + r() * 80) {
      const w = 60 + r() * 90, h = (layer ? 200 : 380) + r() * (layer ? 260 : 520), top = y0 - h;
      s += `<rect x="${f1(x)}" y="${f1(top)}" width="${f1(w)}" height="${h + 600}" fill="${col[layer + (r() > 0.6 ? 1 : 0)]}"/>`;
      if (night || dusk) for (let k = 0; k < 10; k++) if (r() > 0.55) s += `<rect x="${f1(x + 8 + r() * (w - 20))}" y="${f1(top + 14 + r() * (h - 30))}" width="7" height="9" fill="${r() > 0.5 ? "#ffd58a" : "#bcd6ff"}" opacity="${f1(0.4 + r() * 0.5)}"/>`;
    }
    if (o.smoke) s += [[180, 0.9], [760, 1.2], [1180, 0.8]].map(([x, k]) => `<path class="smoke" d="M${x},${y0 - 300}c-60,-120 80,-220 0,-360c-60,-110 70,-200 10,-330" stroke="${night ? "#3b3f4a" : "#5a5560"}" stroke-width="${70 * k}" fill="none" stroke-linecap="round" opacity=".55"/>`).join("");
    if (o.hospital) {
      const hx = o.hospital;
      s += `<g transform="translate(${hx},${y0 - 470}) scale(1.25)"><rect x="-120" y="0" width="240" height="900" fill="${night ? "#1b2333" : "#5a5f78"}" ${OUT}/>
        ${Array.from({ length: 24 }, (_, k) => `<rect x="${-100 + (k % 6) * 36}" y="${60 + Math.floor(k / 6) * 60}" width="22" height="30" fill="#ffeab0" opacity="${0.4 + (k % 3) * 0.2}"/>`).join("")}
        <rect x="-44" y="-96" width="88" height="88" rx="10" fill="#f4f4f0" ${OUT}/><path d="M0,-82V-22M-30,-52H30" stroke="#d8322a" stroke-width="20"/>
        <circle class="beacon" cx="-150" cy="320" r="90" fill="#ff3b30" opacity=".35"/><circle class="beacon2" cx="160" cy="300" r="90" fill="#2f7bff" opacity=".35"/></g>`;
    }
    return s;
  }

  // ---------------- atmosphere: light shafts, floating dust (class zdust, drifted by zlife), haze ----------------
  // shafts fall from a window rectangle [x0..x1, y0..y1] down-left onto the floor at y G
  const rays = (L, x0, x1, y0, y1, G, night) => put(L.glow, [0, 1, 2, 3].map((k) => {
    const a = x0 + ((x1 - x0) * k) / 4 + 20, b = a + (x1 - x0) / 6;
    return `<path d="M${f1(a)},${y0}L${f1(b)},${y0}L${f1(b - 420)},${G}L${f1(a - 560)},${G}Z" fill="url(#${night ? "zRayN" : "zRay"})" opacity="${(0.55 + 0.15 * (k % 2)).toFixed(2)}"/>`;
  }).join(""));
  const dust = (L, x0, x1, y0, y1, n = 26, seed = 5, col = "#fff2dc") => {
    const r = mk(seed);
    put(L.glow, Array.from({ length: n }, () => `<circle class="zdust" cx="${f1(x0 + r() * (x1 - x0))}" cy="${f1(y0 + r() * (y1 - y0))}" r="${f1(1.6 + r() * 3.2)}" fill="${col}" opacity="${f1(0.25 + r() * 0.45)}"/>`).join(""));
  };
  const haze = (L, y, h = 360) => put(L.glow, `<rect x="-1200" y="${y - h}" width="3500" height="${h + 80}" fill="url(#zHaze)"/>`);
  const cone = (L, x, y, w = 260, len = 900) => put(L.glow, `<path d="M${x - w / 2},${y}L${x + w / 2},${y}L${x + w * 1.6},${y + len}L${x - w * 1.6},${y + len}Z" fill="url(#zCone)" class="zflickg"/>`);

  // ---------------- the studio: front door (left), desk, sofa, big window on the city (right) ----------------
  function condo(L, o = {}) {
    const id = o.id || "cd", r = mk(o.seed || 23), G = 1500, t = o.time || "day", night = t === "night";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#1a1d22"/>`);
    put(L.far, `<svg x="200" y="-100" width="1300" height="1500" viewBox="200 -100 1300 1500" overflow="hidden">${city(r, t, 1150, { smoke: o.smoke, hospital: o.hospital })}</svg>`);
    let s = `<path d="M-900,-600H2000V${G}H-900Z M600,300H1100V1160H600Z" fill="url(#zWall)" fill-rule="evenodd"/>`;
    s += `<rect x="586" y="286" width="528" height="888" fill="none" stroke="#e9e4da" stroke-width="28"/><path d="M850,300V1160M600,730H1100" stroke="#e9e4da" stroke-width="16"/>
      <path d="M560,280h580v30h-580z" fill="#b9b2a6"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${590 + k * 8},300v850" stroke="#efe9dc" stroke-width="5" opacity=".5"/>`).join("")}`;
    s += `<rect x="-900" y="${G - 24}" width="2900" height="24" fill="#9b9183"/><rect x="-900" y="${G}" width="2900" height="1200" fill="#b98f62"/>${Array.from({ length: 22 }, (_, k) => `<path d="M${-900 + k * 140},${G}V2700" stroke="#a37c52" stroke-width="4"/>`).join("")}`;
    // front door with peephole, chain and a little shoe rack
    s += `<g id="${id}-doorf"><rect x="40" y="740" width="260" height="${G - 740}" fill="#e3ddd2" ${OUT}/><g id="${id}-door"><rect x="56" y="756" width="228" height="${G - 756}" fill="#7a5a3e" ${OUT}/>
      <rect x="80" y="790" width="180" height="300" rx="6" fill="none" stroke="#5f442d" stroke-width="6"/><rect x="80" y="1130" width="180" height="300" rx="6" fill="none" stroke="#5f442d" stroke-width="6"/>
      <circle cx="170" cy="980" r="9" fill="#2a2420" stroke="#c9b48a" stroke-width="4"/><rect x="246" y="1120" width="22" height="60" rx="6" fill="url(#zChrome)" ${OUT}/>
      <path d="M262,1060q-30,20 -4,44q-26,20 2,44" stroke="#c9ccd0" stroke-width="5" fill="none"/></g></g>`;
    s += `<rect x="20" y="${G - 70}" width="300" height="20" fill="#5f442d"/><path d="M40,${G - 50}h70l10,-24h-80z M140,${G - 50}h70l10,-24h-80z" fill="#e8e2d4" ${OUT}/>`;
    // desk + laptop + lamp
    s += `<g transform="translate(390,${G})"><rect x="-80" y="-300" width="300" height="24" fill="#d9cdb8" ${OUT}/><path d="M-66,-276V0M206,-276V0" stroke="#8a7a62" stroke-width="12"/>
      <path d="M-10,-302l10,-120h130l10,120z" fill="#3d4148" ${OUT}/><rect x="6" y="-412" width="118" height="96" fill="${night ? "#9cc4ff" : "#c9e3ff"}"/><path d="M150,-300l40,-150l-30,-10" stroke="#3d3833" stroke-width="7" fill="none"/><path d="M140,-470h60l-14,-30h-32z" fill="#f2c55c" ${OUT}/>
      <rect x="-60" y="-340" width="40" height="38" rx="6" fill="#e07a3f" ${OUT}/></g>`;
    // sofa
    s += `<g transform="translate(780,${G})"><rect x="-260" y="-300" width="520" height="150" rx="40" fill="#5b6f7c" ${OUT}/><rect x="-280" y="-190" width="560" height="150" rx="30" fill="#6c8190" ${OUT}/>
      <rect x="-300" y="-240" width="70" height="200" rx="30" fill="#5b6f7c" ${OUT}/><rect x="230" y="-240" width="70" height="200" rx="30" fill="#5b6f7c" ${OUT}/>
      <rect x="-150" y="-260" width="110" height="70" rx="20" fill="#e2c46a" ${OUT}/><path d="M-250,-40v30M250,-40v30" stroke="#3a3f45" stroke-width="12"/></g>`;
    // ceiling lamp
    s += `<path d="M640,-600V120" stroke="#3a3f45" stroke-width="4"/><path d="M600,120h80l26,60h-132z" fill="#3a3f45"/>`;
    put(L.set, s);
    if (!night && o.lamp !== false) put(L.glow, `<circle cx="640" cy="200" r="380" fill="url(#lantern)" opacity=".35"/>`);  // lamp:false once the power is out
    if (o.rays !== false) { rays(L, 600, 1100, 300, 1160, G + 40, night); dust(L, 150, 1050, 350, 1450, 30, o.seed || 7, night ? "#cfdcff" : "#fff2dc"); }
  }

  // ---------------- the corridor through the peephole: fisheye lens over a long hall ----------------
  function peephole(L, o = {}) {
    const id = o.id || "ph", r = mk(o.seed || 31), vx = 540, vy = 880;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#1c1b19"/>`);
    let s = `<path d="M-400,-200L${vx - 70},${vy - 90}H${vx + 70}L1480,-200Z" fill="#d9d3c4"/>`;
    s += `<path d="M-400,2200L${vx - 70},${vy + 90}H${vx + 70}L1480,2200Z" fill="#6b3a34"/>`;
    s += `<path d="M-400,-200L${vx - 70},${vy - 90}V${vy + 90}L-400,2200Z" fill="#cbc3b2"/><path d="M1480,-200L${vx + 70},${vy - 90}V${vy + 90}L1480,2200Z" fill="#bfb7a6"/>`;
    s += `<rect x="${vx - 70}" y="${vy - 90}" width="140" height="180" fill="#9e9686"/><rect x="${vx - 34}" y="${vy - 70}" width="68" height="22" fill="#1fbf6a"/><circle cx="${vx}" cy="${vy - 59}" r="70" fill="url(#zExit)"/>`;
    for (let k = 0; k < 4; k++) { // doors in perspective on both walls
      const u0 = 0.12 + k * 0.2, u1 = u0 + 0.1, lerp = (a, b, u) => a + (b - a) * u;
      for (const side of [-1, 1]) {
        const xa = lerp(side < 0 ? -400 : 1480, vx + side * 70, u0), xb = lerp(side < 0 ? -400 : 1480, vx + side * 70, u1);
        const ya = lerp(-200, vy - 90, u0) + (lerp(2200, vy + 90, u0) - lerp(-200, vy - 90, u0)) * 0.3, yb = lerp(-200, vy - 90, u1) + (lerp(2200, vy + 90, u1) - lerp(-200, vy - 90, u1)) * 0.3;
        const fa = lerp(2200, vy + 90, u0), fb = lerp(2200, vy + 90, u1);
        s += `<path d="M${f1(xa)},${f1(ya)}L${f1(xb)},${f1(yb)}L${f1(xb)},${f1(fb)}L${f1(xa)},${f1(fa)}Z" fill="#7a5a3e" ${OUT}/>`;
      }
    }
    if (!o.night) for (let k = 0; k < 5; k++) { const u = 0.08 + k * 0.19, y = -200 + (vy - 90 + 200) * u; s += `<rect x="${f1(vx - 40 - (1 - u) * 300)}" y="${f1(y)}" width="${f1(80 + (1 - u) * 600)}" height="${f1(6 + (1 - u) * 20)}" fill="#fff8e0" opacity=".8"/>`; }
    s += `<path d="M300,1700c40,-30 120,-20 160,10c-30,30 -120,40 -160,-10z" fill="#5a1010" opacity=".8"/>`;
    put(L.set, s);
    put(L.light, `<path d="M-200,-200H1280V2120H-200Z M540,960m-480,0a480,480 0 1,0 960,0a480,480 0 1,0 -960,0Z" fill="#050505" fill-rule="evenodd"/>
      <circle cx="540" cy="960" r="484" fill="url(#zLens)"/><circle cx="540" cy="960" r="482" fill="none" stroke="#2a2826" stroke-width="10"/>
      <path d="M330,700q90,-110 230,-120" stroke="#fff" stroke-width="16" fill="none" opacity=".12" stroke-linecap="round"/>`);
    if (o.night) put(L.glow, `<circle cx="${vx}" cy="${vy - 59}" r="260" fill="url(#zExit)"/><circle cx="${vx}" cy="${vy + 200}" r="420" fill="url(#zExit)" opacity=".5"/>`);
    if (o.face) put(L.act, zFace(`${id}-face`, 540, 960, 1));
  }
  // a front-facing infected face (peephole jump scare): sunken sockets, milky bloodshot eyes with pin pupils, black veins,
  // the jaw hanging open with a torn cheek, broken teeth, blood down the chin, wet hair across the face
  function zFace(id, x, y, s) {
    const r = mk(97);
    let veins = "";
    [[-170, -90, -1], [-60, -100, 1], [60, -100, -1], [170, -90, 1], [-250, -200, 1], [240, -230, -1], [-210, 60, 1], [220, 40, -1], [-90, 120, -1], [90, 120, 1], [0, -260, 1], [-120, -300, -1]].forEach(([x0, y0, d]) => {
      let px = x0, py = y0, path = `M${px},${py}`;
      for (let k = 0; k < 4; k++) { px += d * (14 + r() * 26); py += (r() - 0.45) * 70; path += `L${f1(px)},${f1(py)}`; }
      veins += `<path d="${path}" stroke="#2c3a30" stroke-width="${f1(3 + r() * 4)}" fill="none" stroke-linecap="round" opacity=".8"/>`;
      veins += `<path d="M${f1(px - d * 20)},${f1(py)}l${f1(d * (10 + r() * 20))},${f1(-20 - r() * 30)}" stroke="#2c3a30" stroke-width="2.5" fill="none" opacity=".7"/>`;
    });
    let teeth = "";
    for (let k = 0; k < 11; k++) { // upper row, a few missing
      if (k === 3 || k === 8) continue;
      const tx = -120 + k * 24, h = 18 + r() * 26, w = 18 + r() * 6;
      teeth += `<path d="M${f1(tx)},${f1(150 - Math.abs(tx) * 0.12)}l${f1(w * 0.5)},${f1(h)}l${f1(w * 0.5)},${f1(-h * 0.8)}z" fill="${r() > 0.5 ? "#e4dcc4" : "#cfc39e"}" stroke="#2e2a26" stroke-width="3"/>`;
    }
    for (let k = 0; k < 9; k++) { // lower row
      if (k === 5) continue;
      const tx = -96 + k * 24, h = 16 + r() * 22;
      teeth += `<path d="M${f1(tx)},${f1(310 - Math.abs(tx) * 0.15)}l${f1(10)},${f1(-h)}l${f1(10)},${f1(h * 0.9)}z" fill="#d9cfb2" stroke="#2e2a26" stroke-width="3"/>`;
    }
    const eye = (d, ry, px) => `<ellipse cx="${d * 110}" cy="-60" rx="92" ry="70" fill="#161b16" opacity=".55"/><ellipse cx="${d * 110}" cy="-58" rx="74" ry="56" fill="#0f130f" opacity=".7"/>
      <ellipse cx="${d * 110}" cy="-60" rx="52" ry="${ry}" fill="#e3e9da" ${OUT}/>
      ${[0, 1, 2, 3, 4].map((k) => `<path d="M${d * 110 + d * (30 + k * 4)},${-80 + k * 10}q${d * -14},${-4 + k * 3} ${d * -26},${2 - k}" stroke="#b02424" stroke-width="2.6" fill="none"/>`).join("")}
      ${[0, 1, 2].map((k) => `<path d="M${d * 110 - d * (34 + k * 4)},${-72 + k * 14}q${d * 12},2 ${d * 22},-6" stroke="#b02424" stroke-width="2.2" fill="none"/>`).join("")}
      <circle cx="${d * 110 + px}" cy="-58" r="10" fill="#c9cfbf"/><circle cx="${d * 110 + px}" cy="-58" r="5.5" fill="#5a0a0a"/>
      <path d="M${d * 110 - 50},-42q50,${ry * 0.55} 100,0" stroke="#8e2a2a" stroke-width="7" fill="none" opacity=".85"/>`;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})" opacity="0"><g id="${id}-in">
      <path d="M-150,300L-180,620H180L150,300Z" fill="#8a9a82" ${OUT}/><path d="M60,360q40,30 30,90q-30,-10 -40,-40z" fill="#5a0c0c" opacity=".9"/>${[0, 1, 2, 3].map((k) => `<ellipse cx="${70 + k * 8}" cy="${380 + k * 18}" rx="6" ry="9" fill="#2a0606"/>`).join("")}
      <path d="M-300,-60C-300,-330 -170,-430 0,-430C170,-430 300,-330 300,-60C300,120 230,260 150,330C100,380 60,400 0,404C-60,400 -100,380 -150,330C-230,260 -300,120 -300,-60Z" fill="url(#zSkinF)" ${OUT}/>
      <ellipse cx="-200" cy="110" rx="70" ry="110" fill="#5d6c55" opacity=".45"/><ellipse cx="205" cy="110" rx="62" ry="104" fill="#5d6c55" opacity=".4"/>
      <ellipse cx="-150" cy="-250" rx="60" ry="40" fill="#6c5a78" opacity=".25"/><ellipse cx="190" cy="200" rx="50" ry="40" fill="#6c5a78" opacity=".25"/>
      ${veins}
      ${eye(-1, 38, 6)}${eye(1, 33, -4)}
      <path d="M-200,-150q70,-10 130,40M200,-160q-70,-6 -130,44" stroke="#1d1a17" stroke-width="20" fill="none" stroke-linecap="round"/>
      <path d="M-14,30q-14,30 -4,44M18,30q14,30 4,44" stroke="#2b3328" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-30,70q30,14 60,0" stroke="#4c5a46" stroke-width="6" fill="none"/>
      <path d="M-150,140Q0,96 150,140Q140,330 0,348Q-140,330 -150,140Z" fill="#1c0404" ${OUT}/>
      <path d="M-150,140L-222,112Q-232,170 -196,186L-150,214Z" fill="#1c0404" ${OUT}/><path d="M-214,128l10,18l8,-14l8,16l8,-12" stroke="#d9cfb2" stroke-width="6" fill="none"/>
      <path d="M-140,150Q0,112 140,150" stroke="#6e1212" stroke-width="16" fill="none"/>
      ${teeth}
      <path d="M-60,180q-6,60 -2,110M40,176q10,50 2,120" stroke="#d8d0c0" stroke-width="3" fill="none" opacity=".45"/>
      <path d="M-120,250q-20,90 -16,190M-150,290q-14,60 -8,130M110,280q10,80 4,170M20,346q4,60 -6,130" stroke="#6e0c0c" stroke-width="16" fill="none" stroke-linecap="round" opacity=".92"/>
      ${[[-60, -330, 14], [140, -300, 10], [-240, 0, 12], [230, -10, 9], [-30, 380, 16], [80, 370, 12]].map(([bx, by, br]) => `<circle cx="${bx}" cy="${by}" r="${br}" fill="#6e0c0c" opacity=".85"/>`).join("")}
      <path d="M-300,-120C-320,-380 -120,-470 20,-460C180,-450 330,-360 300,-140C260,-260 160,-330 30,-330C-120,-330 -230,-260 -300,-120Z" fill="#1d1916" ${OUT}/>
      ${[[-250, -260, -262, 160, 18], [-205, -300, -236, 60, 13], [235, -250, 262, 140, 16], [190, -300, 214, 30, 11], [-60, -330, -150, -150, 12]].map(([x0, y0, x1, y1, w]) =>
        `<path d="M${x0 - w / 2},${y0}C${x0 - 20},${(y0 + y1) / 2} ${x1 + 16},${(y0 + y1) / 2} ${x1},${y1}C${x1 + 10},${(y0 + y1) / 2 + 10} ${x0 + 30},${(y0 + y1) / 2} ${x0 + w / 2},${y0}Z" fill="#1d1916"/>`).join("")}
    </g></g>`;
  }
  // the same infected seen from the front, lunging at the camera: shoulders in striped pyjamas, both clawed hands reaching
  function zLunge(id, x, y, s) {
    const hand = (d) => `<g transform="translate(${d * 270},360) scale(${d * 1.5},1.5) rotate(-24)"><path d="M0,40C-60,20 -90,-40 -60,-90C-30,-120 30,-110 50,-70C70,-30 60,20 0,40Z" fill="#a9b8a0" ${OUT}/>
      ${[[-66, -66, -150, -150], [-36, -98, -80, -226], [2, -104, 20, -232], [38, -86, 104, -196], [56, -30, 140, -40]].map(([x0, y0, x1, y1]) => `<path d="M${x0},${y0}Q${(x0 + x1) / 2 - 10},${(y0 + y1) / 2 - 20} ${x1},${y1}" stroke="#2e2a26" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M${x0},${y0}Q${(x0 + x1) / 2 - 10},${(y0 + y1) / 2 - 20} ${x1},${y1}" stroke="#a9b8a0" stroke-width="22" fill="none" stroke-linecap="round"/>
        <path d="M${x1},${y1}l${(x1 - x0) * 0.22},${(y1 - y0) * 0.22 - 6}l${8},${14}z" fill="#141010" stroke="#141010" stroke-width="4" stroke-linejoin="round"/>`).join("")}
      <path d="M-30,-50q24,-14 50,4M-40,-10q30,-6 56,8" stroke="#435541" stroke-width="5" fill="none"/></g>`;
    const arm = (d) => `<path d="M${d * 230},380C${d * 280},400 ${d * 300},390 ${d * 280},370" stroke="#2e2a26" stroke-width="150" fill="none" stroke-linecap="round"/><path d="M${d * 230},380C${d * 280},400 ${d * 300},390 ${d * 280},370" stroke="#b9c4d6" stroke-width="136" fill="none" stroke-linecap="round"/>
      <path d="M${d * 200},300l${d * 60},-30" stroke="#7b8aa6" stroke-width="12"/>`;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})" opacity="0">
      <path d="M-290,420Q-310,300 -170,290H170Q310,300 290,420L250,1200H-250Z" fill="#b9c4d6" ${OUT}/>${[-180, -100, -20, 60, 140, 220].map((sx) => `<path d="M${sx},300V1200" stroke="#7b8aa6" stroke-width="14"/>`).join("")}
      <path d="M-60,300Q0,340 60,300" stroke="#97a3b8" stroke-width="14" fill="none"/><ellipse cx="40" cy="560" rx="70" ry="60" fill="#6e0c0c" opacity=".85"/><ellipse cx="-90" cy="680" rx="40" ry="34" fill="#6e0c0c" opacity=".8"/>
      <path d="M-80,230L-90,330H90L80,230Z" fill="#8a9a82" ${OUT}/>
      <g transform="translate(0,-40) rotate(-11) scale(.62)">${zFace(`${id}-f`, 0, 0, 1).replace('opacity="0"', "")}</g>
      ${arm(-1)}${arm(1)}${hand(-1)}${hand(1)}</g>`;
  }

  // ---------------- close-up: a forearm under poured water (bite with soap, or an old healed scar) ----------------
  // the taps are dry once the pump stops, so the water comes from the stored tub: her other hand tips a plastic ขัน
  // (dipper) whose lip sits on the top of the stream at (690, 566)
  const DIPPER = (skin, sleeve) => `<g transform="translate(584,492) rotate(35)">
      <path d="M-940,-74L-300,-46L-300,46L-940,92Z" fill="${sleeve}" ${OUT}/><path d="M-900,40L-320,30" stroke="${INK}" stroke-width="3" opacity=".3"/>
      <rect x="-312" y="-54" width="34" height="108" rx="14" fill="${sleeve}" ${OUT}/>
      <rect x="-320" y="-14" width="230" height="30" rx="14" fill="#c24f7c" ${OUT}/>
      <path d="M-130,0C-130,96 -78,140 0,140C78,140 130,96 130,0Z" fill="#e86f9b" ${OUT}/><path d="M-96,40C-90,96 -50,120 -10,124" stroke="#fff" stroke-width="10" fill="none" opacity=".28" stroke-linecap="round"/>
      <ellipse cx="0" cy="0" rx="130" ry="34" fill="#c24f7c" ${OUT}/><ellipse cx="6" cy="4" rx="112" ry="24" fill="#bfe3ef"/><path d="M60,-6q30,6 56,4" stroke="#fff" stroke-width="5" opacity=".7" fill="none"/>
      <path d="M118,6q14,10 10,30" stroke="#dff3fa" stroke-width="26" fill="none" stroke-linecap="round" opacity=".9"/>
      <rect x="-286" y="-40" width="84" height="80" rx="30" fill="${skin}" ${OUT}/><path d="M-270,-14h52M-270,6h52M-270,24h48" stroke="${INK}" stroke-width="3" opacity=".45"/>
      <ellipse cx="-214" cy="-30" rx="26" ry="14" fill="${skin}" ${OUT}/></g>`;
  function armClose(L, o = {}) {
    const id = o.id || "ac", r = mk(o.seed || 41), skin = o.skin || "#ecc29c", sleeve = o.sleeve || "#e07a3f", night = !!o.night;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="${night ? "#0c0f14" : "#cfd8d5"}"/>`);
    let far = `<rect x="-900" y="-600" width="2900" height="3200" fill="${night ? "#141a22" : "url(#zTile)"}"/>`;
    for (let k = 0; k < 24; k++) far += `<path d="M${-900 + k * 130},-600V2600" stroke="${night ? "#1b222c" : "#b9c6c1"}" stroke-width="4"/><path d="M-900,${-600 + k * 130}H2000" stroke="${night ? "#1b222c" : "#b9c6c1"}" stroke-width="4"/>`;
    put(L.far, far);
    let s = "";
    if (o.water !== false) {
      s += `<path d="M-200,1280Q540,1180 1300,1280V2400H-200Z" fill="#f4f6f4" ${OUT}/><ellipse cx="540" cy="1360" rx="520" ry="80" fill="#dfe6e4"/><ellipse cx="560" cy="1380" rx="60" ry="16" fill="#9aa6ad"/>
        <g id="${id}-stream" transform="translate(200,0)"><rect x="468" y="566" width="44" height="760" fill="url(#zWater)"/>${Array.from({ length: 8 }, (_, k) => `<path class="foam" d="M${478 + (k % 3) * 10},${580 + k * 90}v60" stroke="#ffffff" stroke-width="4" stroke-dasharray="20 30" opacity=".8"/>`).join("")}</g>
        <g id="${id}-dipper">${DIPPER(skin, sleeve)}</g>`;
    }
    // forearm from the right edge, hand palm-down on the left
    const arm = `<g id="${id}-arm"><path d="M1300,1000L640,1010C600,1010 560,1000 520,1006L500,1110C540,1116 600,1110 640,1110L1300,1130Z" fill="${skin}" ${OUT}/>
      <path d="M530,1010C470,990 400,1000 360,1030C330,1050 300,1060 268,1062C250,1064 248,1080 266,1084L360,1090C380,1110 420,1124 470,1118L506,1110Z" fill="${skin}" ${OUT}/>
      <path d="M362,1040l-60,-6M372,1056l-70,4M380,1074l-64,12" stroke="${INK}" stroke-width="3" opacity=".5"/>
      <path d="M640,1100C780,1108 1000,1112 1300,1122" stroke="${INK}" stroke-width="3" opacity=".25" fill="none"/><path d="M560,1026C760,1028 1000,1032 1300,1040" stroke="#fff" stroke-width="12" opacity=".22" fill="none" stroke-linecap="round"/>
      ${o.mark === "scar" ? `<g id="${id}-scar"><path d="M626,1030q74,-40 156,0M632,1092q70,22 140,0" stroke="#f3c9b8" stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/>${[...Array(7)].map((_, k) => `<ellipse cx="${640 + k * 22}" cy="${1032 + Math.sin(k / 6 * Math.PI) * -10}" rx="6" ry="9" fill="#f0c4b4" stroke="#d49e8c" stroke-width="2"/>`).join("")}${[...Array(6)].map((_, k) => `<ellipse cx="${650 + k * 22}" cy="${1086 - Math.sin(k / 5 * Math.PI) * -8}" rx="6" ry="8" fill="#f0c4b4" stroke="#d49e8c" stroke-width="2"/>`).join("")}</g>`
        : `<g id="${id}-bite"><path d="M624,1040q70,-34 150,0" stroke="#b04040" stroke-width="5" fill="none" opacity=".6"/>${[...Array(7)].map((_, k) => `<ellipse cx="${630 + k * 22}" cy="${1034 + Math.sin(k / 6 * Math.PI) * -10}" rx="7" ry="10" fill="#8e1414"/>`).join("")}${[...Array(6)].map((_, k) => `<ellipse cx="${640 + k * 22}" cy="${1086 - Math.sin(k / 5 * Math.PI) * -8}" rx="7" ry="9" fill="#8e1414"/>`).join("")}
          <path id="${id}-drip" d="M700,1100c-6,30 -2,50 -8,70" stroke="#9e1414" stroke-width="9" fill="none" stroke-linecap="round"/></g>`}
      ${o.veins ? `<g id="${id}-veins">${[["M480,1032C450,1022 432,1046 400,1036C378,1030 360,1044 330,1034", 6], ["M480,1084C452,1094 430,1072 402,1088C384,1096 366,1086 344,1094", 5], ["M440,1030C430,1010 410,1004 392,1010", 4], ["M420,1090C412,1106 394,1112 376,1108", 4], ["M480,1058C456,1060 440,1052 418,1060", 4]]
        .map(([d, w]) => `<path class="vein" d="${d}" stroke="#4a2a4a" stroke-width="${w * 3.4}" fill="none" opacity=".4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><path class="vein" d="${d}" stroke="#120c12" stroke-width="${w * 1.7}" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>`).join("")}</g>` : ""}
      <g id="${id}-foam" opacity="0">${Array.from({ length: 26 }, () => `<circle cx="${f1(600 + r() * 220)}" cy="${f1(1000 + r() * 110)}" r="${f1(6 + r() * 16)}" fill="#ffffff" stroke="#d8e4ea" stroke-width="2" opacity=".9"/>`).join("")}</g>
      ${o.watch ? `<g id="${id}-watch"><rect x="546" y="986" width="58" height="146" rx="14" fill="#20262b" ${OUT}/><rect x="514" y="954" width="122" height="92" rx="20" fill="#2c3338" ${OUT}/>
        <rect x="526" y="966" width="98" height="68" rx="10" fill="#0c1512"/><text id="${id}-wtx" x="575" y="1014" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#9ff0c0">${o.watch}</text>
        <circle id="${id}-wdot" cx="614" cy="976" r="4" fill="#ff4a3a" opacity="0"/><path d="M528,972h30" stroke="#fff" stroke-width="4" opacity=".2"/></g>` : ""}
      <rect x="860" y="980" width="460" height="170" rx="30" fill="${sleeve}" ${OUT}/><path d="M870,990v150" stroke="${INK}" stroke-width="3" opacity=".4"/>
      <g id="${id}-cuff" transform="translate(400,0)"><rect x="470" y="976" width="420" height="178" rx="30" fill="${sleeve}" ${OUT}/><path d="M480,986v154" stroke="${INK}" stroke-width="3" opacity=".4"/></g></g>`;
    s += arm;
    if (o.water !== false) s += `<g id="${id}-splash">${Array.from({ length: 12 }, () => `<circle class="foam" cx="${f1(640 + r() * 110)}" cy="${f1(960 + r() * 60)}" r="${f1(5 + r() * 9)}" fill="#e8f6fb" opacity=".85"/>`).join("")}</g>`;
    put(L.set, s);
    if (night) put(L.glow, o.veins ? `<circle cx="760" cy="1000" r="520" fill="url(#zBeamHot)" opacity=".35"/>` : `<circle cx="760" cy="900" r="700" fill="url(#zPhone)"/>`);
  }

  // the water maths, written in marker on the bathroom mirror (diegetic instead of a floating card):
  // pieces #id-mw0..4 are wiped in by clip rects #id-mc0..4 (attr width), doodles .mdraw are drawn by stroke-dashoffset
  function mirrorMath(id, done) {
    const INKM = "#1b2a52", RED = "#c62a1f";
    const fig = (x, y, k) => `<g class="mdraw"><circle cx="${x}" cy="${y - 62}" r="15" fill="none" stroke="${INKM}" stroke-width="7" pathLength="1"/><path d="M${x},${y - 46}V${y - 8}M${x - 20},${y - 34}L${x + 20},${y - 34}M${x},${y - 8}L${x - 15},${y + 16}M${x},${y - 8}L${x + 15},${y + 16}" stroke="${INKM}" stroke-width="7" fill="none" stroke-linecap="round" pathLength="1"/></g>`;
    const bottle = (x, y) => `<path class="mdraw" d="M${x - 6},${y - 52}h12v10q12,6 12,18v40q0,6 -6,6h-24q-6,0 -6,-6v-40q0,-12 12,-18z" stroke="${INKM}" stroke-width="5" fill="none" stroke-linejoin="round" pathLength="1"/>`;
    const piece = (k, x, y, w, body) => `<clipPath id="${id}-mc${k}"><rect id="${id}-mr${k}" x="${x}" y="${y - 90}" width="${done ? w : 0}" height="130"/></clipPath><g id="${id}-mw${k}" clip-path="url(#${id}-mc${k})">${body}</g>`;
    const T = (x, y, txt, size = 60, col = INKM) => `<text x="${x}" y="${y}" font-family="Kanit" font-weight="700" font-size="${size}" fill="${col}">${txt}</text>`;
    let s = `<rect x="150" y="250" width="780" height="530" rx="18" fill="url(#zChrome)" ${OUT}/><rect x="168" y="268" width="744" height="494" rx="10" fill="#cfe0e4"/>
      <path d="M200,740L420,280M300,760L520,300" stroke="#fff" stroke-width="26" opacity=".35"/>`;
    s += `<g transform="rotate(-2 540 520)" style="${done ? "" : ""}">`;
    s += `<g id="${id}-mf0">${fig(220, 430, 0)}</g>`;
    s += piece(0, 262, 420, 470, T(262, 420, "1 คน · 1 วัน"));
    s += piece(1, 545, 420, 300, T(545, 420, "≈ 4 ลิตร", 60));
    s += `<g id="${id}-mb">${[585, 645, 705, 765].map((x) => bottle(x, 530)).join("")}</g>`;
    s += `<g id="${id}-mf1">${[200, 250, 300].map((x, k) => fig(x, 680, k)).join("")}</g>`;
    s += piece(2, 340, 668, 300, T(340, 668, "× 3 วัน ="));
    s += piece(3, 610, 676, 140, T(610, 676, "36", 92, RED));
    s += piece(4, 762, 668, 170, T(762, 668, "ลิตร", 60, RED));
    s += `<ellipse id="${id}-mo" class="mdraw" cx="660" cy="642" rx="76" ry="60" stroke="${RED}" stroke-width="7" fill="none" pathLength="1" transform="rotate(-8 664 642)"/></g>`;
    if (!done) s = s.replace(/class="mdraw"/g, 'class="mdraw" stroke-dasharray="1" stroke-dashoffset="1"');
    return s;
  }

  // ---------------- bathroom: tub filling, buckets and pots on the floor ----------------
  function bathroom(L, o = {}) {
    const id = o.id || "bt", G = 1520;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#cfd8d5"/>`);
    let far = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="url(#zTile)"/>`;
    for (let k = 0; k < 24; k++) far += `<path d="M${-900 + k * 120},-600V${G}" stroke="#b9c6c1" stroke-width="4"/><path d="M-900,${-600 + k * 120}H2000" stroke="#b9c6c1" stroke-width="4"/>`;
    put(L.far, far);
    let s = `<rect x="-900" y="${G}" width="2900" height="1200" fill="#a9b2b0"/>`;
    if (o.mirror) s += mirrorMath(id, o.mirror === "done");
    s += `<g><path d="M300,820h120q30,0 30,30v40h-40v-30h-110z" fill="url(#zChrome)" ${OUT}/></g>`;
    s += `<rect id="${id}-stream" x="400" y="890" width="30" height="${1440 - 890}" fill="url(#zWater)"/>`;
    s += `<defs><clipPath id="${id}-tc"><path d="M120,1200H780V1420Q780,1480 720,1480H180Q120,1480 120,1420Z"/></clipPath></defs>
      <path d="M100,1180H800V1430Q800,1500 730,1500H170Q100,1500 100,1430Z" fill="#f4f6f4" ${OUT}/>
      <g clip-path="url(#${id}-tc)"><rect id="${id}-water" x="100" y="1480" width="700" height="300" fill="url(#zTub)"/></g>
      <path d="M100,1180H800" stroke="${INK}" stroke-width="10"/><path d="M180,1500v30M720,1500v30" stroke="#9aa6ad" stroke-width="16"/>`;
    if (o.door) s += `<g transform="translate(860,0)"><rect x="0" y="700" width="230" height="${G - 700}" fill="#e8e2d8" ${OUT}/><rect x="14" y="714" width="202" height="${G - 724}" fill="#a88a68" ${OUT}/>
      <rect x="30" y="1080" width="24" height="56" rx="8" fill="url(#zChrome)" ${OUT}/><rect x="0" y="${G - 10}" width="230" height="10" fill="#fff4cf"/>
      <g id="${id}-feet" opacity="0"><ellipse cx="80" cy="${G - 4}" rx="34" ry="6" fill="#1a1612"/><ellipse cx="150" cy="${G - 4}" rx="34" ry="6" fill="#1a1612"/></g></g>`;
    if (!o.door) s += [[880, "#4f8fbf", 120], [1010, "#e07a3f", 100]].map(([x, c, w], k) => `<g transform="translate(${x},${G})"><path d="M${-w / 2},-160L${-w / 2 + 12},0H${w / 2 - 12}L${w / 2},-160Z" fill="${c}" ${OUT}/>
      <defs><clipPath id="${id}-bc${k}"><path d="M${-w / 2 + 6},-154L${-w / 2 + 16},-6H${w / 2 - 16}L${w / 2 - 6},-154Z"/></clipPath></defs><g clip-path="url(#${id}-bc${k})"><rect class="blevel" id="${id}-b${k}" x="${-w}" y="0" width="${w * 2}" height="200" fill="#8fc3d6" opacity=".9"/></g>
      <path d="M${-w / 2 + 6},-160q${w / 2 - 6},-60 ${w - 12},0" stroke="#3a3f45" stroke-width="5" fill="none"/></g>`).join("");
    put(L.set, s);
  }

  // ---------------- the building's water: pump in the basement → roof tank → taps (cross-section diagram) ----------------
  function tower(L, o = {}) {
    const id = o.id || "tw";
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="url(#diagBg)"/>` + Array.from({ length: 18 }, (_, k) => `<path d="M-900,${k * 130}H2000" stroke="#22363d" stroke-width="2"/>`).join(""));
    let s = `<rect x="300" y="300" width="480" height="1400" fill="#22343b" stroke="#cfc4a8" stroke-width="5"/>`;
    for (let k = 0; k <= 23; k++) s += `<path d="M300,${1640 - k * 56}H780" stroke="#3f5650" stroke-width="3"/>`;
    s += `<rect x="300" y="1700" width="480" height="140" fill="#1b282d" stroke="#cfc4a8" stroke-width="5"/>`;
    s += `<g transform="translate(420,1772)"><rect x="-60" y="-40" width="120" height="80" rx="12" fill="#5f6b70" stroke="#cfc4a8" stroke-width="4"/><circle cx="0" cy="0" r="26" fill="#2e3a3f" stroke="#cfc4a8" stroke-width="4"/><path class="spin" d="M0,-20V20M-20,0H20" stroke="#cfc4a8" stroke-width="5"/></g>`;
    s += `<g transform="translate(640,210)"><rect x="-90" y="-60" width="180" height="120" rx="14" fill="#4f7f96" stroke="#cfc4a8" stroke-width="5"/><rect id="${id}-tank" x="-80" y="-20" width="160" height="70" fill="#8fc3d6"/></g>`;
    s += `<path d="M480,1772H560V270" stroke="#3f5650" stroke-width="18" fill="none"/><path id="${id}-up" d="M480,1772H560V270" stroke="#8fc3d6" stroke-width="10" fill="none" stroke-dasharray="30 24"/>`;
    s += `<path d="M700,270V1640" stroke="#3f5650" stroke-width="14"/><path id="${id}-down" d="M700,270V1640" stroke="#8fc3d6" stroke-width="7" fill="none" stroke-dasharray="24 22"/>`;
    s += `<g transform="translate(740,352)"><circle r="18" fill="#e8705a"/><circle r="34" fill="none" stroke="#e8705a" stroke-width="4"/></g>`;
    s += `<g id="${id}-bolt" transform="translate(230,1700)"><path d="M10,-80L-30,10H0L-10,80L40,-20H8L22,-80Z" fill="#f2c55c" stroke="#2e2a26" stroke-width="4"/></g>`;
    s += `<g id="${id}-x" opacity="0"><path d="M150,1610l160,160M310,1610l-160,160" stroke="#fff" stroke-width="30" stroke-linecap="round"/><path d="M150,1610l160,160M310,1610l-160,160" stroke="#e8443a" stroke-width="18" stroke-linecap="round"/>
      <path d="M380,1700l90,140M470,1700l-90,140" stroke="#e8443a" stroke-width="14" stroke-linecap="round"/></g>`;
    const tag = (x, y, t, c) => `<g transform="translate(${x},${y})"><rect x="${-t.length * 15}" y="-36" width="${t.length * 30}" height="60" rx="12" fill="#0d171b" stroke="${c}" stroke-width="4"/><text y="7" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="${c}">${t}</text></g>`;
    s += `<g id="${id}-tags">${tag(560, 1920, "ปั๊มน้ำ", "#8fc3d6")}${tag(170, 1560, "ไฟดับ", "#f2c55c")}</g>`;
    put(L.set, s);
  }

  // a wall cabinet with a fire extinguisher ("full"), or its glass door swung open and the hook empty ("open")
  const extBox = (x, y, state) => `<g transform="translate(${x},${y})"><rect x="-56" y="-110" width="112" height="220" rx="8" fill="#b8302a" ${OUT}/><rect x="-44" y="-98" width="88" height="196" fill="#2a1414"/>
    ${state === "open" ? `<path d="M-44,-98L-120,-80V116L-44,98Z" fill="#cfe6f2" opacity=".35" ${OUT}/>` : `<g transform="translate(0,-10)">${EXT}</g><rect x="-44" y="-98" width="88" height="196" fill="#cfe6f2" opacity=".2"/>`}
    <path d="M-30,-98l-14,30" stroke="#fff" stroke-width="4" opacity=".4"/></g>`;
  // a 6 kg extinguisher, ~55 cm: red body, chrome valve and handle at the top, black hose; centred on its own middle
  const EXT = `<rect x="-26" y="-70" width="52" height="160" rx="18" fill="#c8302a" ${OUT}/><rect x="-26" y="-20" width="52" height="40" fill="#f4ecd8" opacity=".85"/><rect x="14" y="-62" width="7" height="140" rx="3" fill="#fff" opacity=".25"/>
    <rect x="-12" y="-92" width="24" height="24" rx="4" fill="url(#zChrome)" ${OUT}/><path d="M-10,-92L-34,-104M10,-92L30,-110" stroke="#2e2a26" stroke-width="7" stroke-linecap="round"/><path d="M12,-82q36,20 26,90" stroke="#1b1816" stroke-width="10" fill="none" stroke-linecap="round"/>`;
  // a flickering fluorescent tube (class zflick, driven by zlife) with its glow in the glow layer
  const tube = (L, x, y, w = 260) => { put(L.glow, `<ellipse class="zflickg" cx="${x}" cy="${y + 160}" rx="${w * 1.6}" ry="460" fill="url(#zGlowW)" opacity=".35"/>`); return `<rect x="${x - w / 2 - 10}" y="${y - 16}" width="${w + 20}" height="22" rx="6" fill="#3a3f45"/><rect class="zflick" x="${x - w / 2}" y="${y + 4}" width="${w}" height="14" rx="7" fill="#f4fbff"/>`; };

  // ---------------- the lift lobby with the power out: dead call panel (unlit ▼, blank display), lift doors on the left,
  // the fire-stair door on the right under a battery-lit green ทางหนีไฟ sign. #id-hand is บอส's finger jabbing the button
  // (fingertip at the local origin; the shot tweens its transform attribute).
  function liftCall(L, o = {}) {
    const id = o.id || "lc", G = 1500, skin = "#d39a6e";
    const SIGN = `<g transform="translate(1110,560)"><rect x="-170" y="-66" width="340" height="132" rx="10" fill="#1fbf6a" ${OUT}/><rect x="-158" y="-54" width="316" height="108" rx="6" fill="none" stroke="#dfffe9" stroke-width="3" opacity=".6"/>
        <g transform="translate(-112,-6)" fill="#fff"><circle cx="8" cy="-34" r="11"/><path d="M-6,-20l22,4l10,22l14,6l-4,8l-18,-6l-6,-8l-6,18l14,16l-4,28h-12l2,-22l-16,-14l-10,22l-20,6l-2,-10l14,-6l12,-30l4,-18l-10,6l-6,16l-10,-2l8,-22z"/></g>
        <text x="40" y="-6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#fff">ทางหนีไฟ</text><text x="40" y="38" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="28" fill="#fff" letter-spacing="3">FIRE EXIT</text></g>`;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0b0d0e"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="#6a6e6c"/>`;
    for (let k = 0; k < 9; k++) s += `<path d="M-900,${-600 + k * 260}H2000" stroke="#5f6361" stroke-width="3"/>`;
    // lift doors (left) with the hall lantern above them, blank
    s += `<rect x="-300" y="420" width="700" height="${G - 420}" fill="#3b4044" ${OUT}/><rect x="-270" y="460" width="320" height="${G - 460}" fill="url(#zChrome)" opacity=".5"/>
      <rect x="54" y="460" width="320" height="${G - 460}" fill="url(#zChrome)" opacity=".45"/><path d="M52,460V${G}" stroke="#16191b" stroke-width="8"/>
      <rect x="-40" y="300" width="200" height="80" rx="10" fill="#060504" ${OUT}/><text x="60" y="364" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="66" fill="#241413">88</text>`;
    // the call panel: brushed steel plate, a small floor display (dark, ghost segments only), one ▼ button that never lights
    s += `<g transform="translate(640,1000)"><rect x="-80" y="-180" width="160" height="340" rx="16" fill="url(#zChrome)" ${OUT}/><rect x="-66" y="-166" width="132" height="312" rx="10" fill="none" stroke="#fff" stroke-width="3" opacity=".35"/>
      <rect x="-56" y="-140" width="112" height="70" rx="8" fill="#08090a" ${OUT}/><text x="0" y="-86" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#1f1414">88</text><path d="M-46,-132h40" stroke="#fff" stroke-width="3" opacity=".18"/>
      <circle cx="0" cy="0" r="46" fill="#9aa6ad" ${OUT}/><circle cx="0" cy="0" r="34" fill="#2a3034"/><path d="M-14,-8H14L0,12Z" fill="#59636a"/><path d="M-22,-22a32,32 0 0 1 18,-10" stroke="#fff" stroke-width="4" opacity=".25" fill="none"/>
      <text x="0" y="110" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#4a5258">ชั้น 23</text></g>`;
    // the fire-stair door and its sign
    s += `<rect x="900" y="700" width="420" height="${G - 700}" fill="#4b5652" ${OUT}/><rect x="930" y="730" width="360" height="${G - 730}" fill="#5f6d67" ${OUT}/>
      <rect x="1010" y="820" width="120" height="180" fill="url(#zWire)" stroke="${INK}" stroke-width="4"/><rect x="1010" y="820" width="120" height="180" fill="#1b2421" opacity=".7"/>
      <rect x="950" y="1130" width="320" height="34" rx="12" fill="url(#zChrome)" ${OUT}/>`;
    s += `<rect x="-900" y="${G - 20}" width="2900" height="20" fill="#2f3331"/><rect x="-900" y="${G}" width="2900" height="1200" fill="#4a4a44"/>`;
    put(L.set, s);
    put(L.glow, `<circle cx="1110" cy="560" r="560" fill="url(#zExit)"/>${SIGN}`);  // battery-lit, so above the darkness
    // บอส's hand: index finger up, other fingers curled, red wristband, bare forearm (tank top)
    put(L.act, `<g id="${id}-hand" transform="translate(560,1260) scale(1.15) rotate(24)"><g transform="translate(34,0)">
      <path d="M-62,250L-74,980H70L50,250Z" fill="${skin}" ${OUT}/><path d="M30,280L44,960" stroke="${INK}" stroke-width="3" opacity=".25"/>
      <rect x="-60" y="222" width="114" height="46" rx="12" fill="#e05a3a" ${OUT}/><path d="M-56,236h106" stroke="#fff" stroke-width="4" opacity=".35"/>
      <rect x="-66" y="96" width="122" height="140" rx="40" fill="${skin}" ${OUT}/>
      <path d="M-6,140q14,-10 28,0M26,148q12,-8 22,2" stroke="${INK}" stroke-width="3" fill="none" opacity=".45"/>
      <ellipse cx="-66" cy="166" rx="20" ry="38" transform="rotate(-24 -66 166)" fill="${skin}" ${OUT}/></g>
      <rect x="-15" y="0" width="30" height="134" rx="15" fill="${skin}" ${OUT}/><path d="M-8,12q8,-6 16,0" stroke="#f3d2b6" stroke-width="5" fill="none"/><path d="M-10,60h20M-10,90h18" stroke="${INK}" stroke-width="2.5" opacity=".4"/></g>`);
  }

  // ---------------- fire stairs: a landing seen from the side, the floor number painted on the wall ----------------
  // o.up adds the flight going up on the left; o.ext puts an extinguisher cabinet on the wall; o.red a pulsing red emergency light
  function stairwell(L, o = {}) {
    const id = o.id || "sw", G = 1500, fl = o.floor ?? 23, X0 = o.up ? -100 : -900;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0d1110"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="#5d6460"/><rect x="-900" y="700" width="2900" height="40" fill="#4e5551"/>`;
    for (let k = 0; k < 12; k++) s += `<path d="M${-900 + k * 260},-600V${G}" stroke="#555c58" stroke-width="3"/>`;
    s += `<path d="M260,1300q120,-40 260,20q-120,50 -260,-20z" fill="#3b403d" opacity=".5"/><path d="M-200,820q40,120 10,260M900,780q-30,160 10,300" stroke="#454b47" stroke-width="5" fill="none" opacity=".7"/>`;
    s += `<text id="${id}-num" x="520" y="1180" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="420" fill="#e8e2cf" opacity=".9">${fl}</text>`;
    s += `<g transform="translate(150,520)"><rect x="-70" y="-30" width="140" height="60" rx="6" fill="#1fbf6a" ${OUT}/><path d="M-40,0h40M10,-12l14,12l-14,12" stroke="#fff" stroke-width="7" fill="none"/></g>`;
    s += tube(L, 520, 330);
    cone(L, 520, 350, 280, 1150); haze(L, G - 40, 420); dust(L, 260, 820, 420, 1420, 22, 11, "#e8f0ff");
    if (o.ext) s += extBox(880, 1110, o.ext);
    s += `<rect x="${X0}" y="${G}" width="${800 - X0}" height="40" fill="#8a8f8a"/><rect x="${X0}" y="${G + 40}" width="${800 - X0}" height="1200" fill="#3f4542"/>`;
    for (let k = 0; k < 10; k++) s += `<path d="M${800 + k * 90},${G + k * 70}h90v70" fill="none" stroke="#8a8f8a" stroke-width="16"/>`;
    s += `<path d="M800,${G}L1700,${G + 700}V2700H800Z" fill="#3f4542"/>`;
    if (o.up) {
      for (let k = 0; k < 12; k++) s += `<path d="M${-100 - k * 90},${G - k * 70}v-70h-90" fill="none" stroke="#8a8f8a" stroke-width="16"/>`;
      s += `<path d="M-100,${G}L-1180,${G - 840}V2700H-100Z" fill="#3f4542"/>`;
      s += `<path d="M-100,${G - 190}L-1180,${G - 1030}" stroke="#c9ccd0" stroke-width="12" fill="none"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-160 - k * 120},${G - 190 - (60 + k * 120) * 0.778}V${G - (60 + k * 120) * 0.778}" stroke="#c9ccd0" stroke-width="6"/>`).join("")}`;
    }
    s += `<path d="M${X0},${G - 190}H800L1700,${G + 510}" stroke="#c9ccd0" stroke-width="12" fill="none"/>${Array.from({ length: 14 }, (_, k) => -800 + k * 120).filter((x) => x > X0).map((x) => `<path d="M${x},${G - 190}V${G}" stroke="#c9ccd0" stroke-width="6"/>`).join("")}`;
    put(L.set, s);
    put(L.glow, `<circle cx="150" cy="520" r="520" fill="url(#zExit)"/>`);
    if (o.red) put(L.glow, `<circle class="zred" cx="${o.red}" cy="420" r="700" fill="url(#zRed)" opacity=".5"/>`);
  }
  // one long flight across the whole frame (the chase back up): nosing line y = 1500 + (x - 540) * 0.778
  const FLIGHT = (x) => 1500 + (x - 540) * 0.778;
  function stairFlight(L, o = {}) {
    const id = o.id || "sf";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0d1110"/>`);
    let s = `<rect x="-2000" y="-1400" width="5200" height="5200" fill="#5d6460"/>`;
    for (let k = 0; k < 20; k++) s += `<path d="M${-2000 + k * 260},-1400V3800" stroke="#555c58" stroke-width="3"/>`;
    (o.nums || [[1500, 21], [-500, 22]]).forEach(([x, n]) => (s += `<text x="${x}" y="${FLIGHT(x) - 260}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="380" fill="#e8e2cf" opacity=".75">${n}</text>`));
    s += tube(L, 900, FLIGHT(900) - 900) + tube(L, -300, FLIGHT(-300) - 900);
    cone(L, 900, FLIGHT(900) - 880, 260, 1100); cone(L, -300, FLIGHT(-300) - 880, 260, 1100); dust(L, -700, 1500, 700, 2100, 34, 13, "#e8f0ff");
    let st = "";
    for (let x = -1800; x < 2800; x += 90) st += `h90v70`;
    s += `<path d="M-1800,${FLIGHT(-1800)}${st}V4200H-1800Z" fill="#3f4542"/><path d="M-1800,${FLIGHT(-1800)}${st}" fill="none" stroke="#8a8f8a" stroke-width="16"/>`;
    s += `<path d="M-1800,${FLIGHT(-1800) - 190}L2800,${FLIGHT(2800) - 190}" stroke="#c9ccd0" stroke-width="12"/>${Array.from({ length: 40 }, (_, k) => -1760 + k * 120).map((x) => `<path d="M${x},${FLIGHT(x) - 190}V${FLIGHT(x)}" stroke="#c9ccd0" stroke-width="6"/>`).join("")}`;
    put(L.set, s);
    put(L.glow, `<circle class="zred" cx="400" cy="600" r="900" fill="url(#zRed)" opacity=".5"/>`);
  }
  // close-up from the corridor side: the steel fire door being shoved shut on an infected arm reaching through the gap;
  // a second face pressed to the wired glass. #id-door slides (x), #id-zarm flails from the gap, #id-hands push.
  function doorJam(L, o = {}) {
    const id = o.id || "dj", E = 760;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#120606"/>`);
    put(L.far, `<rect x="600" y="-600" width="500" height="3200" fill="#2a0c0c"/><circle class="zred" cx="820" cy="700" r="380" fill="url(#zRed)" opacity=".8"/>`);
    let s = `<g id="${id}-door"><rect x="-500" y="-200" width="${E + 500}" height="2400" fill="#6b7672" ${OUT}/><rect x="${E - 30}" y="-200" width="30" height="2400" fill="#4f5956"/>
      <rect x="-420" y="-120" width="${E + 340}" height="2240" fill="none" stroke="#5c6662" stroke-width="10"/>
      <g transform="translate(330,520)"><defs><clipPath id="${id}-win"><rect x="-150" y="-210" width="300" height="420"/></clipPath></defs><rect x="-150" y="-210" width="300" height="420" fill="#3a1010" ${OUT}/>
        <g clip-path="url(#${id}-win)"><g id="${id}-face" opacity="0" transform="scale(.42)">${zFace(`${id}-pf`, 0, 40, 1).replace('opacity="0"', "")}</g></g><rect x="-150" y="-210" width="300" height="420" fill="url(#zWire)" opacity=".55"/><rect x="-150" y="-210" width="300" height="420" fill="#cfe6f2" opacity=".14"/><path d="M-120,-180l60,-20" stroke="#fff" stroke-width="8" opacity=".3"/></g>
      <rect x="-300" y="1120" width="${E - 120 + 300}" height="50" rx="20" fill="url(#zChrome)" ${OUT}/><rect x="${E - 140}" y="1080" width="70" height="130" rx="12" fill="#3a3f45" ${OUT}/>
      <text x="200" y="1500" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="120" fill="#e8e2cf" opacity=".5">23</text></g>`;
    s += `<g id="${id}-zarm"><g transform="translate(${E + 20},900)"><g id="${id}-zarm-in">
      <path d="M40,-40L-300,-20L-310,70L40,60Z" fill="#e6e8e2" ${OUT}/><path d="M-120,-30l-20,40l30,10M-220,-26l14,30" stroke="#8a8f88" stroke-width="4" fill="none"/><ellipse cx="-80" cy="20" rx="40" ry="26" fill="#7a1414" opacity=".8"/>
      <path d="M-290,-14L-520,-4L-524,64L-296,64Z" fill="#b0b9a2" ${OUT}/><path d="M-330,0q-60,30 -150,10" stroke="#435541" stroke-width="5" fill="none"/>
      <path d="M-520,-30C-600,-40 -640,10 -620,60C-600,100 -540,96 -516,70Z" fill="#b0b9a2" ${OUT}/>
      ${[[-560, -26, -650, -110], [-600, -6, -720, -60], [-614, 30, -740, 20], [-600, 62, -710, 110], [-550, 82, -600, 170]].map(([x0, y0, x1, y1]) => `<path d="M${x0},${y0}Q${(x0 + x1) / 2},${(y0 + y1) / 2 - 30} ${x1},${y1}" stroke="#2e2a26" stroke-width="24" fill="none" stroke-linecap="round"/><path d="M${x0},${y0}Q${(x0 + x1) / 2},${(y0 + y1) / 2 - 30} ${x1},${y1}" stroke="#b0b9a2" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M${x1},${y1}l${(x1 - x0) * 0.25},${(y1 - y0) * 0.25 - 4}l6,12z" fill="#141010" stroke="#141010" stroke-width="3" stroke-linejoin="round"/>`).join("")}
    </g></g></g>`;
    s += `<rect x="${E}" y="-600" width="1400" height="3200" fill="#cfc6b6"/><rect x="${E}" y="-600" width="110" height="3200" fill="#8f978f" ${OUT}/><rect x="${E + 24}" y="-600" width="18" height="3200" fill="#6b7370"/>
      <rect x="${E + 150}" y="1100" width="40" height="80" rx="6" fill="#3a3f45"/>`;
    s += `<g id="${id}-dust" opacity="0">${Array.from({ length: 16 }, (_, k) => `<circle cx="${E + 20 + (k % 4) * 14}" cy="${200 + k * 110}" r="${8 + (k % 3) * 6}" fill="#d9d3c4" opacity=".6"/>`).join("")}</g>`;
    put(L.set, s);
    // บอส's forearms in the foreground, palms on the door (they move with it)
    put(L.fg, `<g id="${id}-hands">${[[300, 980, 18], [560, 1300, -8]].map(([hx, hy, rot]) => `<g transform="translate(${hx},${hy}) rotate(${rot})"><path d="M-70,0L-340,520L-200,600L40,90Z" fill="#d39a6e" ${OUT}/><path d="M-300,470l110,64" stroke="#e05a3a" stroke-width="40"/>
      <path d="M-80,-40C-90,-120 -20,-150 40,-140L90,-130C120,-120 120,-90 96,-84L60,-80L100,-60C126,-50 120,-20 96,-20L60,-24L90,0C110,20 90,44 66,36L20,24C0,60 -40,70 -70,40Z" fill="#d39a6e" ${OUT}/>
      <path d="M40,-112L88,-106M44,-74L96,-42M40,-30L80,8" stroke="#a9744c" stroke-width="5" stroke-linecap="round"/><path d="M-60,20Q-30,40 0,10" stroke="#b27c52" stroke-width="8" fill="none" opacity=".6"/><path d="M-200,520L-30,120" stroke="#b27c52" stroke-width="18" opacity=".35"/></g>`).join("")}</g>`);
    L.fg.classList.remove("fgblur");
  }
  // first-person run down the 23rd-floor corridor: a true perspective box (eye 1.6 m, f = 935 px, vanishing point 540,960),
  // doors on both walls with their numbers; #id-d2307 bursts open (closed panel hides, open panel shows); #id-z lunges out
  function corridorRun(L, o = {}) {
    const id = o.id || "cr", f = 935, vx = 540, vy = 960, W = 1.1, H = 2.6, E = 1.6;
    const P = (X, Y, Z) => `${f1(vx + (f * X) / Z)},${f1(vy + (f * (E - Y)) / Z)}`;
    const quad = (a, b, c, d, fill, extra = "") => `<path d="M${a}L${b}L${c}L${d}Z" fill="${fill}" ${extra}/>`;
    const Z0 = 0.35, Z1 = 30;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0b0b0a"/>`);
    let s = quad(P(-W, H, Z0), P(W, H, Z0), P(W, H, Z1), P(-W, H, Z1), "#cfc8b8");
    s += quad(P(-W, 0, Z0), P(W, 0, Z0), P(W, 0, Z1), P(-W, 0, Z1), "#5b2a2a");
    s += quad(P(-W, 0, Z0), P(-W, H, Z0), P(-W, H, Z1), P(-W, 0, Z1), "#d6cfbf");
    s += quad(P(W, 0, Z0), P(W, H, Z0), P(W, H, Z1), P(W, 0, Z1), "#c8c0ae");
    s += quad(P(-W, 0, Z1), P(-W, H, Z1), P(W, H, Z1), P(W, 0, Z1), "#9e9686");
    s += `<rect x="${vx - 18}" y="${vy - 44}" width="36" height="12" fill="#1fbf6a"/>`;
    for (let z = 1.2; z < Z1; z *= 1.33) s += `<path d="M${P(-W * 0.98, 0, z)}L${P(W * 0.98, 0, z)}" stroke="#4a2222" stroke-width="${f1(40 / z)}"/>`;
    // ceiling lights
    [2.4, 5, 8.5, 13, 19].forEach((z, k) => (s += quad(P(-0.3, H - 0.01, z), P(0.3, H - 0.01, z), P(0.3, H - 0.01, z + 0.5), P(-0.3, H - 0.01, z + 0.5), "#f4fbff", `class="${k === 1 ? "zflick" : ""}"`)));
    // doors: [side, z0, number]
    const doors = o.doors || [[1, 2.2, "2309"], [-1, 2.9, "2310"], [1, 4.6, "2307"], [-1, 5.6, "2308"], [1, 8.0, "2305"], [-1, 9.4, "2306"], [1, 12.5, "2303"], [-1, 14.5, "2304"]];
    doors.forEach(([sd, z, n]) => {
      const X = sd * W, z1 = z + 0.95;
      const frame = quad(P(X, 0, z - 0.06), P(X, 2.15, z - 0.06), P(X, 2.15, z1 + 0.06), P(X, 0, z1 + 0.06), "#e9e4da");
      const panel = quad(P(X, 0, z), P(X, 2.05, z), P(X, 2.05, z1), P(X, 0, z1), n === "2306" ? "#8a5a3a" : "#7a5a3e", OUT);
      const plate = `<text x="${f1(vx + (f * X) / (z + 0.47))}" y="${f1(vy + (f * (E - 2.32)) / (z + 0.47))}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${f1(120 / (z + 0.47))}" fill="#2e2a26">${n}</text>`;
      if (n === "2307") {
        const hinge = z1, ox = X - sd * 0.85, oz = z1 - 0.3; // open: the panel swung out into the corridor around the far jamb
        s += frame + quad(P(X, 0, z), P(X, 2.05, z), P(X, 2.05, z1), P(X, 0, z1), "#140606");
        s += `<g id="${id}-d2307">${panel}</g><g id="${id}-d2307o" opacity="0">${quad(P(X, 0, hinge), P(X, 2.05, hinge), P(ox, 2.05, oz), P(ox, 0, oz), "#7a5a3e", OUT)}</g>${plate}`;
      } else s += frame + panel + plate;
    });
    put(L.set, s);
    if (o.night) { put(L.glow, `<circle cx="${vx}" cy="${vy - 38}" r="120" fill="url(#zExit)"/>`); put(L.act, zLunge(`${id}-z`, 0, 0, 1)); return; }
    put(L.glow, `<ellipse class="zflickg" cx="${vx}" cy="${vy - 260}" rx="760" ry="560" fill="url(#zGlowW)" opacity=".35"/>`);
    put(L.glow, `<radialGradient id="${id}-fog"><stop offset="0" stop-color="#d9d3c4" stop-opacity=".75"/><stop offset="1" stop-color="#d9d3c4" stop-opacity="0"/></radialGradient><ellipse cx="${vx}" cy="${vy}" rx="260" ry="300" fill="url(#${id}-fog)"/>`);
    dust(L, 200, 900, 500, 1500, 24, 17, "#fff6e6");
    put(L.act, zLunge(`${id}-z`, 0, 0, 1));
  }
  // looking straight down the stairwell from the floor-19 landing: a real switchback stair in one-point perspective
  // (eye 1.6 m above the landing, f = 600 px). Each floor: flight A down the left side (−Y → +Y), a landing at the far end,
  // flight B back up the right side, the next landing at the near end; a well between the flights shows the floors below.
  // Drawn deepest first with depth fog. #id-up = the infected one floor down, looking up; #id-hand = its hand on the rail.
  function stairShaft(L, o = {}) {
    const id = o.id || "ss", f = 600, cx = 540, cy = 960, WX = 1.6, WY = 2.6, GAP = 0.42, LD = 1.25, RISE = 3, N = 7, TREADS = 10;
    const P = (X, Y, Z) => `${f1(cx + (f * X) / Z)},${f1(cy + (f * Y) / Z)}`;
    const mix = (hex, Z) => {
      const k = Math.min(0.94, 1 - Math.exp(-(Z - 1.4) / 6.5)), c = parseInt(hex.slice(1), 16);
      const ch = (sh) => Math.round(((c >> sh) & 255) * (1 - k) + 7 * k);
      return `rgb(${ch(16)},${ch(8)},${ch(0)})`;
    };
    const quad = (pts, fill, extra = "") => `<path d="M${pts.join("L")}Z" fill="${fill}" ${extra}/>`;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#050606"/>`);
    let s = "";
    // shaft walls, banded per half floor so they darken with depth
    for (let z = 0.75; z < 1.6 + RISE * N; z += 1.5) {
      const z2 = z + 1.5;
      s += quad([P(-WX, -WY, z), P(WX, -WY, z), P(WX, -WY, z2), P(-WX, -WY, z2)], mix("#545b57", z));
      s += quad([P(-WX, WY, z), P(WX, WY, z), P(WX, WY, z2), P(-WX, WY, z2)], mix("#4e5551", z));
      s += quad([P(-WX, -WY, z), P(-WX, WY, z), P(-WX, WY, z2), P(-WX, -WY, z2)], mix("#5d6460", z));
      s += quad([P(WX, -WY, z), P(WX, WY, z), P(WX, WY, z2), P(WX, -WY, z2)], mix("#575e5a", z));
    }
    const flight = (x0, x1, yFrom, yTo, zTop) => { // treads deepest first; each tread a horizontal slab, its nosing drawn light
      let t = "";
      for (let k = TREADS - 1; k >= 0; k--) {
        const ya = yFrom + ((yTo - yFrom) * k) / TREADS, yb = yFrom + ((yTo - yFrom) * (k + 1)) / TREADS, z = zTop + ((k + 1) * (RISE / 2)) / TREADS;
        t += quad([P(x0, ya, z), P(x1, ya, z), P(x1, yb, z), P(x0, yb, z)], mix(k % 2 ? "#8f948f" : "#868b86", z));
        t += `<path d="M${P(x0, ya, z)}L${P(x1, ya, z)}" stroke="${mix("#c9ccc4", z)}" stroke-width="${f1(Math.max(1, 26 / z))}"/>`;
        t += quad([P(x0, ya, z - RISE / 2 / TREADS), P(x1, ya, z - RISE / 2 / TREADS), P(x1, ya, z), P(x0, ya, z)], mix("#5f645f", z));
      }
      return t;
    };
    const rail = (x, yA, zA, yB, zB) => { // sloped handrail 0.9 m above the nosings, with balusters
      let t = "";
      for (let k = 0; k <= 6; k++) { const y = yA + ((yB - yA) * k) / 6, z = zA + ((zB - zA) * k) / 6; t += `<path d="M${P(x, y, z - 0.9)}L${P(x, y, z)}" stroke="${mix("#9aa0a2", z)}" stroke-width="${f1(Math.max(1, 20 / z))}"/>`; }
      return t + `<path d="M${P(x, yA, zA - 0.9)}L${P(x, yB, zB - 0.9)}" stroke="${mix("#d6d9dc", zA)}" stroke-width="${f1(Math.max(1.5, 46 / zA))}" stroke-linecap="round"/>`;
    };
    for (let n = N - 1; n >= 0; n--) {
      const Z = 1.6 + RISE * n, fl = 19 - n;
      // near landing of this floor (where the flight down starts)
      s += quad([P(-WX, -WY, Z), P(WX, -WY, Z), P(WX, -WY + LD, Z), P(-WX, -WY + LD, Z)], mix("#7d827e", Z));
      // flight B (right side) arrives here from the far landing below... drawn as part of the floor above it; this floor's own pieces:
      s += flight(GAP, WX, WY - LD, -WY + LD, Z + RISE / 2);                         // B: far landing → next floor's near landing
      s += quad([P(-WX, WY - LD, Z + RISE / 2), P(WX, WY - LD, Z + RISE / 2), P(WX, WY, Z + RISE / 2), P(-WX, WY, Z + RISE / 2)], mix("#7a7f7b", Z + RISE / 2));
      s += rail(GAP, WY - LD, Z + RISE / 2, -WY + LD, Z + RISE);
      s += `<path d="M${P(-GAP, WY - LD, Z + RISE / 2 - 0.9)}L${P(GAP, WY - LD, Z + RISE / 2 - 0.9)}" stroke="${mix("#d6d9dc", Z + 1.5)}" stroke-width="${f1(Math.max(1.5, 46 / (Z + 1.5)))}"/>`;
      s += flight(-WX, -GAP, -WY + LD, WY - LD, Z);                                   // A: this landing → far landing
      s += rail(-GAP, -WY + LD, Z, WY - LD, Z + RISE / 2);
      if (n > 0) { // stencilled floor number on the landing, and the green exit sign glow on the near wall
        s += `<text x="${f1(cx + (f * -0.9) / Z)}" y="${f1(cy + (f * (-WY + LD * 0.62)) / Z)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${f1((f * 0.5) / Z)}" fill="${mix("#e8e2cf", Z)}" opacity=".8">${fl}</text>`;
        s += `<circle cx="${f1(cx + (f * 1.2) / Z)}" cy="${f1(cy + (f * -WY) / Z)}" r="${f1((f * 0.9) / Z)}" fill="url(#zExit)" opacity="${f1(Math.max(0.15, 1 - n * 0.12))}"/>`;
      }
      if (n === 1) { // the infected (the office worker), one floor down in the well, face turned up, arms reaching up at her
        const Zh = Z + 0.2, px = cx + (f * 0.05) / Zh, py = cy + (f * 0.9) / Zh, k = (0.62 / Zh) * 1.45;
        const sk = "#b0b9a2", shirt = "#e6e8e2";
        const claw = (d) => `<g transform="translate(${d * 470},-330) scale(${d * 1.9},1.9) rotate(-8)"><path d="M0,40C-60,20 -90,-40 -60,-90C-30,-120 30,-110 50,-70C70,-30 60,20 0,40Z" fill="${sk}" ${OUT}/>
          ${[[-66, -66, -150, -150], [-36, -98, -80, -226], [2, -104, 20, -232], [38, -86, 104, -196], [56, -30, 140, -40]].map(([x0, y0, x1, y1]) => `<path d="M${x0},${y0}Q${(x0 + x1) / 2 - 10},${(y0 + y1) / 2 - 20} ${x1},${y1}" stroke="#2e2a26" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M${x0},${y0}Q${(x0 + x1) / 2 - 10},${(y0 + y1) / 2 - 20} ${x1},${y1}" stroke="${sk}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M${x1},${y1}l${(x1 - x0) * 0.22},${(y1 - y0) * 0.22 - 6}l8,14z" fill="#141010" stroke="#141010" stroke-width="4" stroke-linejoin="round"/>`).join("")}</g>`;
        const arm = (d) => `<path d="M${d * 380},520C${d * 500},300 ${d * 520},0 ${d * 470},-260" stroke="#2e2a26" stroke-width="170" fill="none" stroke-linecap="round"/><path d="M${d * 380},520C${d * 500},300 ${d * 520},0 ${d * 470},-260" stroke="${shirt}" stroke-width="150" fill="none" stroke-linecap="round"/>
          <path d="M${d * 360},300l${d * 60},-30l${d * -10},50" stroke="#8a8f88" stroke-width="10" fill="none"/>`;
        s += `<g id="${id}-up" opacity="0"><circle cx="${f1(px)}" cy="${f1(py)}" r="170" fill="url(#zRed)" opacity=".9"/><g transform="translate(${f1(px)},${f1(py)}) scale(${f1(k)})">
          <path d="M-600,900C-640,620 -520,460 -330,420Q0,380 330,420C520,460 640,620 600,900Z" fill="${shirt}" ${OUT}/>
          <path d="M0,430L-46,620L0,780L46,620Z" fill="#3a4a7a" ${OUT}/><ellipse cx="-230" cy="600" rx="90" ry="70" fill="#7a1414" opacity=".85"/><ellipse cx="260" cy="700" rx="70" ry="54" fill="#7a1414" opacity=".8"/>
          <path d="M-430,520l60,40l-20,60M380,480l-50,30" stroke="#8a8f88" stroke-width="8" fill="none"/>
          ${arm(-1)}${arm(1)}
          ${zFace(`${id}-uf`, 0, -20, 1).replace('opacity="0"', "").replace(/<path d="M-150,300L-180,620H180L150,300Z"[^>]*\/>/, "")}
          ${claw(-1)}${claw(1)}</g></g>`;
        s += `<g id="${id}-hand" opacity="0"></g>`;
      }
    }
    put(L.set, s);
    // ข้าว's own hands on the rail in the foreground: this is her looking down
    const fist = (x, d) => `<g transform="translate(${x},1722) scale(${d},1)">
        <path d="M-78,40C-92,150 -84,300 -66,420H118C112,300 104,150 92,40Z" fill="#e07a3f" ${OUT}/><path d="M-70,40H96" stroke="#bb5f2a" stroke-width="10"/>
        <path d="M-74,30C-80,-6 -66,-40 -34,-46L70,-50C96,-50 106,-30 104,0L100,34C70,52 -40,52 -74,30Z" fill="#ecc29c" ${OUT}/>
        ${[-50, -18, 14, 46].map((fx, k) => `<path d="M${fx - 15},-44C${fx - 17},-70 ${fx + 17},-72 ${fx + 15},-44" fill="#ecc29c" ${OUT}/><path d="M${fx - 7},-58q7,-6 14,0" stroke="#cc9a74" stroke-width="3" fill="none"/>`).join("")}
        <path d="M100,-6C126,-14 136,8 120,22L98,30" fill="#ecc29c" ${OUT}/><path d="M-40,8q30,10 80,0" stroke="#cc9a74" stroke-width="4" fill="none" opacity=".7"/></g>`;
    put(L.fg, `<g id="${id}-me"><rect x="-200" y="1690" width="1480" height="40" rx="20" fill="url(#zChrome)" ${OUT}/>${fist(300, -1)}${fist(780, 1)}</g>`);
    L.fg.classList.remove("fgblur");
  }

  // ---------------- cutaway: a noise on floor 19 spreads through the building; the infected on nearby floors turn to it ----------------
  // #id-ring0..2 expand from the landing; #id-z<k> (dots on other floors) slide to the stairwell; #id-us = ข้าว + บอส
  const NOISE_FL = [23, 22, 21, 20, 19, 18, 17, 16, 15];
  function noiseMap(L, o = {}) {
    const id = o.id || "nz", top = 330, H = 150, X0 = 230, X1 = 850, SX = 740, fy = (f) => top + (23 - f) * H;
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="url(#diagBg)"/>` + Array.from({ length: 18 }, (_, k) => `<path d="M-900,${k * 130}H2000" stroke="#22363d" stroke-width="2"/>`).join(""));
    let s = `<rect x="${X0}" y="${top - 20}" width="${X1 - X0}" height="${H * 9 + 20}" fill="#1a2a30" stroke="#cfc4a8" stroke-width="5"/>`;
    NOISE_FL.forEach((f) => {
      const y = fy(f) + H;
      s += `<path d="M${X0},${y}H${X1}" stroke="#3f5650" stroke-width="4"/><text x="${X0 - 24}" y="${y - 50}" text-anchor="end" font-family="Kanit" font-weight="900" font-size="44" fill="${f === 19 ? "#f2c55c" : "#7f9aa0"}">${f}</text>`;
      for (let d = 0; d < 3; d++) s += `<rect x="${X0 + 40 + d * 150}" y="${y - 110}" width="90" height="100" fill="none" stroke="#33494f" stroke-width="3"/>`;
    });
    s += `<rect x="${SX - 60}" y="${top - 20}" width="120" height="${H * 9 + 20}" fill="#22363d" stroke="#5c7a80" stroke-width="3"/>`;
    for (let k = 0; k < 18; k++) s += `<path d="M${SX - 50 + (k % 2) * 100},${top + k * (H / 2)}L${SX + 50 - (k % 2) * 100},${top + (k + 1) * (H / 2)}" stroke="#5c7a80" stroke-width="5"/>`;
    const oy = fy(19) + H - 60;
    s += [0, 1, 2].map((k) => `<circle id="${id}-ring${k}" cx="${SX}" cy="${oy}" r="80" fill="none" stroke="#f2c55c" stroke-width="10" opacity="0"/>`).join("");
    s += `<g id="${id}-bang" transform="translate(${SX},${oy})"><path d="M0,-46L12,-14L46,-18L20,6L34,38L0,20L-34,38L-20,6L-46,-18L-12,-14Z" fill="#f2c55c" stroke="#2e2a26" stroke-width="4"/></g>`;
    s += `<g id="${id}-us"><circle cx="${SX - 26}" cy="${oy + 24}" r="13" fill="#e07a3f" stroke="#fff" stroke-width="4"/><circle cx="${SX + 6}" cy="${oy + 24}" r="13" fill="#3a3f45" stroke="#fff" stroke-width="4"/></g>`;
    (o.dots || [[22, 380], [21, 520], [20, 300], [20, 560], [18, 420], [18, 300], [17, 560], [16, 380]]).forEach(([f, x], k) => {
      s += `<g id="${id}-z${k}" data-tx="${SX - x}" transform="translate(${x},${fy(f) + H - 40})"><circle r="20" fill="#d8322a" stroke="#2e2a26" stroke-width="4"/><circle class="zeye" cx="-6" cy="-4" r="3.5" fill="#fff"/><circle class="zeye" cx="7" cy="-4" r="3.5" fill="#fff"/></g>`;
    });
    put(L.set, s);
  }

  // ================= EP.2 (the night with no power): torchlight, the kitchen, the gym on floor 20, close-ups =================
  Sets.DEFS += `
    <linearGradient id="zBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff6dc" stop-opacity=".6"/><stop offset=".7" stop-color="#fff2d0" stop-opacity=".22"/><stop offset="1" stop-color="#fff2d0" stop-opacity="0"/></linearGradient>
    <radialGradient id="zBeamHot"><stop offset="0" stop-color="#fff8e6" stop-opacity=".5"/><stop offset="1" stop-color="#fff8e6" stop-opacity="0"/></radialGradient>
    <linearGradient id="zMirror" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#26323a"/><stop offset=".5" stop-color="#121a1f"/><stop offset="1" stop-color="#1d272d"/></linearGradient>
    <linearGradient id="zFridge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#dfe3e4"/><stop offset=".55" stop-color="#f4f6f6"/><stop offset="1" stop-color="#c9cfd1"/></linearGradient>`;
  // a flashlight beam from (x, y) at angle a (degrees, 0 = pointing right), drawn in the glow layer so it lights through the darkness;
  // rotate it by tweening the transform attribute of #id
  const beam = (id, x, y, a, len = 900, w = 240) => `<g id="${id}" transform="translate(${x},${y}) rotate(${a})"><path d="M0,-12L${len},-${w}L${len},${w}L0,12Z" fill="url(#zBeam)"/>
    <ellipse cx="${f1(len * 0.86)}" cy="0" rx="${f1(w * 0.55)}" ry="${f1(w * 0.95)}" fill="url(#zBeamHot)"/></g>`;

  // ---------------- the condo kitchen at night: a two-door fridge (freezer on top), counter and sink, the dark city in the window ----------------
  // #id-fd = fridge door (hinged on its right edge: tween attr transform "translate(680,0) scale(k,1) translate(-680,0)"), #id-mist = cold air,
  // o.note: the outage times in marker on the doors ("write": pieces #id-nr0..3 wipe in by attr width, #id-no circle draws; "done": all shown;
  // piece 2 is the freezer line, on the freezer door)
  function fridgeNote(id, done) {
    const INKM = "#1b2a52", RED = "#c62a1f";
    const piece = (k, x, y, w, body) => `<clipPath id="${id}-nc${k}"><rect id="${id}-nr${k}" x="${x - 6}" y="${y - 46}" width="${done || k === 0 ? w : 0}" height="64"/></clipPath><g clip-path="url(#${id}-nc${k})">${body}</g>`;
    const T = (x, y, txt, size = 34, col = INKM) => `<text x="${x}" y="${y}" font-family="Kanit" font-weight="700" font-size="${size}" fill="${col}">${txt}</text>`;
    let s = `<g transform="rotate(-3 530 1200)">`;
    s += piece(0, 404, 1146, 250, T(404, 1146, "ไฟดับ 17:30"));
    s += piece(1, 404, 1212, 260, T(404, 1212, "ตู้เย็น ≈ 4 ชม."));
    s += piece(3, 420, 1300, 230, T(420, 1300, "ห้ามเปิด!", 50, RED));
    s += `<ellipse id="${id}-no" class="mdraw" cx="530" cy="1284" rx="132" ry="46" stroke="${RED}" stroke-width="6" fill="none" pathLength="1" ${done ? "" : 'stroke-dasharray="1" stroke-dashoffset="1"'}/></g>`;
    return s;
  }
  function kitchen(L, o = {}) {
    const id = o.id || "kt", G = 1500, r = mk(o.seed || 61);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0b0d11"/>`);
    put(L.far, `<svg x="-60" y="300" width="380" height="800" viewBox="-60 300 380 800" overflow="hidden">${city(r, "night", 1050)}</svg>`);
    let s = `<path d="M-900,-600H2000V${G}H-900Z M-40,320H300V1080H-40Z" fill="url(#zWall)" fill-rule="evenodd"/>
      <rect x="-54" y="306" width="368" height="788" fill="none" stroke="#e9e4da" stroke-width="26"/><path d="M130,320V1080" stroke="#e9e4da" stroke-width="14"/>`;
    s += `<rect x="-900" y="${G}" width="2900" height="1200" fill="#8f8170"/>${Array.from({ length: 16 }, (_, k) => `<path d="M${-900 + k * 180},${G}V2700" stroke="#7d705f" stroke-width="4"/>`).join("")}`;
    // backsplash, upper cabinets, counter with a sink, a kettle and a pot
    s += `<rect x="700" y="960" width="900" height="200" fill="#dcd8cf"/>${Array.from({ length: 30 }, (_, k) => `<rect x="${704 + (k % 15) * 60}" y="${964 + Math.floor(k / 15) * 100}" width="54" height="94" fill="none" stroke="#c4bfb4" stroke-width="3"/>`).join("")}
      <rect x="720" y="420" width="760" height="340" fill="#b9a083" ${OUT}/><path d="M970,420V760M1220,420V760" stroke="${INK}" stroke-width="4"/><path d="M940,580v40M990,580v40M1190,580v40" stroke="#5f4b36" stroke-width="8" stroke-linecap="round"/>
      <rect x="700" y="1150" width="900" height="34" fill="#e8e4dc" ${OUT}/><rect x="716" y="1184" width="880" height="${G - 1184}" fill="#b9a083" ${OUT}/><path d="M980,1184V${G}M1240,1184V${G}" stroke="${INK}" stroke-width="4"/>
      <path d="M1040,1150q0,-90 50,-90" stroke="url(#zChrome)" stroke-width="16" fill="none"/><rect x="1030" y="1146" width="200" height="12" fill="#9aa6ad"/>
      <path d="M820,1150h90l-8,-70h-74z" fill="#3a3f45" ${OUT}/><path d="M902,1100q30,0 26,24" stroke="${INK}" stroke-width="6" fill="none"/>`;
    // the fridge: freezer door on top, fridge door below, handles on the left, magnets and a calendar
    s += `<rect x="372" y="882" width="316" height="${G - 882}" rx="18" fill="#9aa1a3" ${OUT}/>
      <g id="${id}-in"><rect x="384" y="1092" width="292" height="${G - 1100}" fill="#14191d"/><path d="M392,1200H668M392,1300H668M392,1400H668" stroke="#2c353b" stroke-width="8"/>
        <rect x="420" y="1240" width="60" height="58" rx="8" fill="#3e5a40"/><rect x="520" y="1350" width="90" height="48" rx="10" fill="#6a3c34"/><rect x="600" y="1230" width="40" height="70" rx="6" fill="#8fa8b8"/></g>
      <g id="${id}-fd"><rect x="380" y="1092" width="300" height="${G - 1100}" rx="12" fill="url(#zFridge)" ${OUT}/><rect x="398" y="1120" width="16" height="200" rx="8" fill="url(#zChrome)" ${OUT}/>
        <rect x="600" y="1360" width="56" height="70" fill="#f2efe6" ${OUT}/><path d="M606,1376h44M606,1392h44M606,1408h30" stroke="#9aa1a3" stroke-width="3"/><circle cx="628" cy="1360" r="9" fill="#d8322a"/>
        ${o.note ? fridgeNote(id, o.note === "done") : ""}</g>
      <g id="${id}-zd"><rect x="380" y="890" width="300" height="196" rx="12" fill="url(#zFridge)" ${OUT}/><rect x="398" y="920" width="16" height="140" rx="8" fill="url(#zChrome)" ${OUT}/>
        <circle cx="640" cy="930" r="11" fill="#f2c55c" ${OUT}/><circle cx="600" cy="950" r="9" fill="#4f8fbf" ${OUT}/>
        ${o.note ? `<clipPath id="${id}-nc2"><rect id="${id}-nr2" x="398" y="962" width="${o.note === "done" ? 270 : 0}" height="64"/></clipPath><g clip-path="url(#${id}-nc2)" transform="rotate(-3 530 1200)"><text x="404" y="1008" font-family="Kanit" font-weight="700" font-size="34" fill="#1b2a52">ช่องแข็ง ≈ 48 ชม.</text></g>` : ""}</g>
      <g id="${id}-mist" opacity="0">${Array.from({ length: 14 }, () => `<circle cx="${f1(400 + r() * 260)}" cy="${f1(1120 + r() * 340)}" r="${f1(30 + r() * 50)}" fill="#e8f4f8" opacity=".35"/>`).join("")}</g>`;
    put(L.set, s);
    put(L.glow, `<rect x="-40" y="320" width="340" height="760" fill="#3a4a7a" opacity=".18"/>`);   // a little moonlight from the window
  }

  // ---------------- the condo gym on floor 20, dark: a mirror wall (#id-refl holds whatever the mirror shows, clipped and tinted),
  // a dumbbell rack, a bench, a treadmill, the first-aid box on the pillar (#id-kit), cracks (#id-crack) and shards (#id-shards) ----------------
  function gym(L, o = {}) {
    const id = o.id || "gm", G = 1500, MT = 360, MB = 1330, cx = o.crackX ?? 760, cy = o.crackY ?? 900, r = mk(o.seed || 71);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#07090a"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="#3a3e40"/><rect x="-900" y="${MT - 70}" width="2900" height="40" fill="#2c3032"/>
      <text x="200" y="${MT - 100}" font-family="Kanit" font-weight="900" font-size="60" fill="#c9ccd0" opacity=".55" letter-spacing="6">FITNESS · ชั้น 20</text>`;
    s += `<defs><clipPath id="${id}-mclip"><rect x="-500" y="${MT}" width="2200" height="${MB - MT}"/></clipPath></defs>
      <rect x="-500" y="${MT}" width="2200" height="${MB - MT}" fill="url(#zMirror)"/>
      <g clip-path="url(#${id}-mclip)"><g id="${id}-refl"><rect x="-500" y="${MB - 120}" width="2200" height="160" fill="#1a1f22"/>
        ${[100, 420, 900, 1300].map((x) => `<rect x="${x}" y="${MB - 330}" width="${120 + (x % 3) * 40}" height="230" fill="#11161a" opacity=".9"/>`).join("")}</g>
        <rect x="-500" y="${MT}" width="2200" height="${MB - MT}" fill="#0d2230" opacity=".28"/>
        ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${-400 + k * 330},${MT}l-160,${MB - MT}" stroke="#fff" stroke-width="${10 + (k % 3) * 8}" opacity=".05"/>`).join("")}</g>
      ${[-200, 130, 460, 790, 1120].map((x) => `<path d="M${x},${MT}V${MB}" stroke="#0a0d0f" stroke-width="6"/>`).join("")}
      <rect x="-500" y="${MB}" width="2200" height="24" fill="#5c6366"/>`;
    // cracks radiating from (cx, cy), and the shards that fly
    s += `<g id="${id}-crack" opacity="0">${Array.from({ length: 11 }, (_, k) => { const a = (k / 11) * Math.PI * 2 + r() * 0.3, L1 = 160 + r() * 260, L2 = L1 + 120 + r() * 200, b = a + (r() - 0.5) * 0.5;
      return `<path d="M${cx},${cy}L${f1(cx + Math.cos(a) * L1)},${f1(cy + Math.sin(a) * L1)}L${f1(cx + Math.cos(b) * L2)},${f1(cy + Math.sin(b) * L2)}" stroke="#e8f4f8" stroke-width="${3 + (k % 3) * 2}" fill="none" opacity=".8"/>`; }).join("")}
      ${[60, 120, 200].map((R) => `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#e8f4f8" stroke-width="3" stroke-dasharray="${f1(R * 0.5)} ${f1(R * 0.35)}" opacity=".7"/>`).join("")}</g>`;
    s += `<g id="${id}-shards" opacity="0">${Array.from({ length: 16 }, (_, k) => { const a = (k / 16) * Math.PI * 2, d = 40 + r() * 90, x = cx + Math.cos(a) * d, y = cy + Math.sin(a) * d, z = 18 + r() * 30;
      return `<path class="shard" data-a="${f1(a)}" d="M${f1(x)},${f1(y - z)}L${f1(x + z * 0.8)},${f1(y + z * 0.4)}L${f1(x - z * 0.6)},${f1(y + z * 0.7)}Z" fill="#cfe6f2" stroke="#fff" stroke-width="2" opacity=".85"/>`; }).join("")}</g>`;
    // the floor, a treadmill (left), a bench, a dumbbell rack (right), the pillar with the first-aid box
    s += `<rect x="-900" y="${G - 170}" width="2900" height="1370" fill="#202426"/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-900 + k * 260},${G - 170}V2700" stroke="#191c1e" stroke-width="5"/>`).join("")}
      <g transform="translate(-60,${G})"><path d="M-160,0L-120,-90H260L300,0Z" fill="#2b3033" ${OUT}/><path d="M220,-90L300,-420" stroke="#3a3f43" stroke-width="22"/><rect x="250" y="-470" width="130" height="60" rx="10" fill="#2b3033" ${OUT}/></g>
      <g transform="translate(330,${G})"><rect x="-150" y="-150" width="300" height="40" rx="12" fill="#3b2f2a" ${OUT}/><path d="M-110,-110V0M110,-110V0" stroke="#2b3033" stroke-width="16"/></g>
      <g transform="translate(980,${G})"><rect x="-260" y="-230" width="520" height="24" fill="#2b3033" ${OUT}/><rect x="-260" y="-110" width="520" height="24" fill="#2b3033" ${OUT}/><path d="M-240,-206V0M240,-206V0" stroke="#2b3033" stroke-width="18"/>
        ${[-200, -110, -20, 70, 160].map((x, k) => `<g transform="translate(${x},${k % 2 ? -250 : -130})"><rect x="-6" y="-8" width="62" height="16" rx="6" fill="#9aa6ad"/><rect x="-18" y="-24" width="22" height="48" rx="8" fill="#1b1d1f" ${OUT}/><rect x="46" y="-24" width="22" height="48" rx="8" fill="#1b1d1f" ${OUT}/></g>`).join("")}</g>
      <rect x="1290" y="-600" width="240" height="${G + 600}" fill="#454a4c" ${OUT}/>
      <g id="${id}-kit" transform="translate(1410,860)"><rect x="-85" y="-70" width="170" height="140" rx="14" fill="#f2f2ee" ${OUT}/><path d="M0,-42V42M-42,0H42" stroke="#1f9a5a" stroke-width="24"/><rect x="-30" y="-92" width="60" height="22" rx="8" fill="#c9ccd0" ${OUT}/></g>`;
    put(L.set, s);
    put(L.glow, `<rect x="-900" y="-600" width="2900" height="60" fill="#000" opacity="0"/>`);
  }

  // ---------------- close-up: บอส's forearm cut by glass, ข้าว's hands pressing a towel on it (direct pressure), her watch ----------------
  // #id-spurt pulses (scaleY), #id-towel + #id-hands appear when she presses, #id-blot = blood soaking through, #id-wtx/#id-wdot the watch
  function pressClose(L, o = {}) {
    const id = o.id || "pc", skin = "#d39a6e", ks = "#ecc29c", sleeve = "#e07a3f";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0c0f12"/>`);
    put(L.far, `<rect x="-900" y="-600" width="2900" height="3200" fill="#3d2e22"/>${Array.from({ length: 16 }, (_, k) => `<path d="M-900,${-600 + k * 220}H2000" stroke="#33261c" stroke-width="6"/>`).join("")}`);
    let s = `<ellipse cx="560" cy="1180" rx="420" ry="120" fill="#5a0c0a" opacity=".85"/><ellipse id="${id}-pool" cx="620" cy="1210" rx="260" ry="70" fill="#7a1010" opacity=".9"/>`;
    // his forearm across the frame (from the right), hand open on the left, wristband
    s += `<g id="${id}-arm"><path d="M1300,960L620,990C560,992 520,986 480,994L470,1120C520,1126 580,1120 640,1120L1300,1140Z" fill="${skin}" ${OUT}/>
      <path d="M490,1000C420,980 340,990 290,1024C250,1050 220,1064 190,1066C168,1068 166,1086 188,1090L290,1098C312,1120 360,1132 420,1126L478,1116Z" fill="${skin}" ${OUT}/>
      <rect x="1000" y="958" width="70" height="186" rx="14" fill="#e05a3a" ${OUT}/>
      <path d="M640,1020L860,1060" stroke="#4a0606" stroke-width="22" stroke-linecap="round"/><path d="M640,1020L860,1060" stroke="#b01616" stroke-width="12" stroke-linecap="round"/>
      <g id="${id}-spurt"><path d="M740,1040C700,960 760,880 700,780C800,840 820,960 800,1046Z" fill="#c41a14" opacity=".92"/><path d="M780,1040C800,980 840,940 860,880C870,960 830,1010 810,1048Z" fill="#a51410" opacity=".85"/>
        <circle cx="690" cy="750" r="16" fill="#c41a14"/><circle cx="740" cy="720" r="10" fill="#c41a14"/><circle cx="870" cy="850" r="11" fill="#c41a14"/></g>
      <path d="M700,1110c-4,40 2,60 -6,90M800,1120c0,30 6,50 0,74" stroke="#9e1414" stroke-width="12" fill="none" stroke-linecap="round"/></g>`;
    // the towel and her two hands on top of it (heel of the hand on the wound), her watch on the left wrist
    s += `<g id="${id}-press" opacity="0"><path d="M560,940Q750,900 940,950L960,1110Q760,1150 560,1120Z" fill="#9cc4d6" ${OUT}/><path d="M600,960Q760,930 920,970" stroke="#7ea6ba" stroke-width="6" fill="none"/>
      <ellipse id="${id}-blot" cx="750" cy="1040" rx="60" ry="34" fill="#8e1414" opacity=".0"/>
      <g transform="translate(700,930) rotate(-8)"><path d="M-120,-40C-130,-110 -60,-140 20,-130L110,-120C150,-110 150,-40 120,-10L-80,10C-110,4 -118,-14 -120,-40Z" fill="${ks}" ${OUT}/>
        ${[-70, -20, 30, 80].map((x) => `<path d="M${x},-128C${x - 4},-170 ${x + 34},-176 ${x + 32},-126" fill="${ks}" ${OUT}/>`).join("")}<path d="M-140,-60L-420,-300L-300,-380L-60,-120Z" fill="${sleeve}" ${OUT}/></g>
      <g transform="translate(800,900) rotate(6)"><path d="M-110,-30C-120,-100 -50,-130 30,-120L110,-110C150,-100 150,-30 120,0L-70,20C-100,14 -108,-4 -110,-30Z" fill="${ks}" ${OUT}/>
        ${[-60, -10, 40, 90].map((x) => `<path d="M${x},-118C${x - 4},-160 ${x + 34},-166 ${x + 32},-116" fill="${ks}" ${OUT}/>`).join("")}<path d="M120,-60L420,-320L520,-220L160,10Z" fill="${sleeve}" ${OUT}/>
        <g transform="translate(150,-60) rotate(-40)"><rect x="-30" y="-74" width="60" height="148" rx="14" fill="#20262b" ${OUT}/><rect x="-62" y="-46" width="124" height="92" rx="20" fill="#2c3338" ${OUT}/>
          <rect x="-50" y="-34" width="100" height="68" rx="10" fill="#0c1512"/><text id="${id}-wtx" x="0" y="14" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#9ff0c0">5:00</text>
          <circle id="${id}-wdot" cx="40" cy="-24" r="4" fill="#ff4a3a" opacity="0"/></g></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="700" cy="1000" r="560" fill="url(#zBeamHot)"/>`);
  }

  // ---------------- close-up: the front door of 2306 from inside: peephole, chain, lever handle (#id-knob), a fist (#id-fist), dust (#id-dust) ----------------
  function doorClose(L, o = {}) {
    const id = o.id || "dc", skin = o.skin || "#d39a6e";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0b0c0d"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="3200" fill="#c9c1b2"/><rect x="120" y="-200" width="840" height="2400" fill="#e3ddd2" ${OUT}/>
      <g id="${id}-door"><rect x="150" y="-170" width="780" height="2340" fill="#7a5a3e" ${OUT}/><rect x="220" y="-80" width="640" height="800" rx="10" fill="none" stroke="#5f442d" stroke-width="12"/><rect x="220" y="880" width="640" height="1100" rx="10" fill="none" stroke="#5f442d" stroke-width="12"/>
        <circle cx="540" cy="560" r="20" fill="#1a1612" stroke="#c9b48a" stroke-width="8"/>
        <rect x="760" y="760" width="60" height="26" rx="6" fill="url(#zChrome)" ${OUT}/><path d="M790,786q-50,70 -10,150q-30,60 0,110" stroke="#c9ccd0" stroke-width="10" fill="none" id="${id}-chain"/>
        <rect x="720" y="1020" width="150" height="190" rx="14" fill="url(#zChrome)" ${OUT}/><g id="${id}-knob" transform="translate(760,1100)"><rect x="-200" y="-24" width="220" height="48" rx="22" fill="url(#zChrome)" ${OUT}/><circle r="30" fill="#c9ccd0" ${OUT}/></g></g>
      <g id="${id}-dust" opacity="0">${Array.from({ length: 14 }, (_, k) => `<circle cx="${200 + (k * 53) % 700}" cy="${-60 + (k * 37) % 120}" r="${4 + (k % 3) * 3}" fill="#e8e2cf" opacity=".7"/>`).join("")}</g>`;
    put(L.set, s);
    if (o.fist) put(L.fg, `<g id="${id}-fist" transform="translate(470,980)"><path d="M60,40L380,520L520,440L170,-20Z" fill="${skin}" ${OUT}/><rect x="330" y="400" width="140" height="60" rx="14" transform="rotate(-34 400 430)" fill="#e05a3a" ${OUT}/>
      <path d="M-70,-40C-80,-110 -10,-130 60,-120L120,-100C160,-80 160,10 120,40L-30,60C-70,56 -70,20 -70,-40Z" fill="${skin}" ${OUT}/>
      ${[-46, 0, 46].map((y) => `<path d="M-70,${y}q-20,-20 0,-40" stroke="${INK}" stroke-width="4" fill="none" opacity=".6"/>`).join("")}<path d="M60,-110q30,40 20,90" stroke="#b27c52" stroke-width="6" fill="none"/></g>`);
    L.fg.classList.remove("fgblur");
  }

  // looping motion for these sets
  function zlife(tl, scope, t0, dur) {
    const root = document.querySelector(scope);
    if (!root || root.dataset.zlife) return;
    root.dataset.zlife = "1";
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".zdust").forEach((el, i) => tl.fromTo(el, { x: -6 - (i % 5) * 3, y: 8 }, { x: 10 + (i % 4) * 4, y: -22 - (i % 3) * 8, duration: 2.6 + (i % 7) * 0.35, repeat: Math.ceil(dur / 2.6) + 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, t0 - (i % 9) * 0.3)));
    q(".smoke").forEach((el, i) => tl.fromTo(el, { x: -10, opacity: 0.4 }, { x: 14, opacity: 0.6, duration: 2.4 + i * 0.4, repeat: Math.ceil(dur / 2.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".beacon").forEach((el) => tl.fromTo(el, { opacity: 0.1 }, { opacity: 0.6, duration: 0.25, repeat: Math.ceil(dur / 0.25), yoyo: true, immediateRender: false }, t0));
    q(".beacon2").forEach((el) => tl.fromTo(el, { opacity: 0.6 }, { opacity: 0.1, duration: 0.25, repeat: Math.ceil(dur / 0.25), yoyo: true, immediateRender: false }, t0));
    q(".zred").forEach((el) => tl.fromTo(el, { opacity: 0.15 }, { opacity: 0.7, duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    const r = mk(Math.round(t0 * 100) + 7); // fluorescent tubes: mostly on, with seeded drop-outs
    for (let t = 0; t < dur; t += 0.06 + r() * 0.25) {
      const on = r() > 0.28 ? 1 : 0.15 + r() * 0.3;
      q(".zflick").forEach((el) => tl.set(el, { opacity: on }, t0 + t));
      q(".zflickg").forEach((el) => tl.set(el, { opacity: on * 0.35 }, t0 + t));
    }
    q(".spin").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360 * Math.ceil(dur), svgOrigin: "0 0", duration: dur, ease: "none", immediateRender: false }, t0));
  }

  Object.assign(Sets, { condo, peephole, armClose, bathroom, tower, liftCall, stairwell, stairShaft, stairFlight, doorJam, corridorRun, noiseMap, kitchen, gym, pressClose, doorClose });
  if (window.Camp) Camp.hand.extinguisher = `<g transform="translate(0,${118 + 96}) rotate(180)">${EXT}</g>`; // held by the valve, swung like a club
  window.Zom = { zFace, zLunge, zlife, city, FLIGHT, beam };
})();
