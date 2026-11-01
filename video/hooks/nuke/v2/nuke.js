// "ระเบิดนิวเคลียร์ลงกรุงเทพ" pre-production stills (lane C, 1 Nov). Generic Bangkok, no real logos, station names or flags.
//   Sets.bkk(L, o)      dusk over the city: towers with lit windows, a temple prang and spires by the river, the elevated rail
//                       viaduct, tangled power lines, street food stalls. o.view: "skywalk" (on an elevated walkway, railing in
//                       front) | "street" (a jammed road, a car door close) | "window" (inside a condo looking out).
//                       The event: o.flash [x, y] (#id-fl core, #id-white whiteout), o.cloud [x, y, s] (#id-cl mushroom cloud)
//   Sets.shelter(L, o)  the basement car park of a concrete office tower: columns, painted bays, emergency lamps, people
//                       sitting in the middle away from the ramp; o.dust (the ramp mouth glowing, dust drifting in)
//   cast: ploy (พลอย 24, office blouse, lanyard) · phum (ภูมิ 14, her brother, school shirt) · uncle (ลุงชัย 60, security guard)
(function () {
  const { f1, put, mk } = Pop2;
  const INK = "#1e2228";
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  Sets.DEFS += `
    <linearGradient id="nkSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1e3a"/><stop offset=".45" stop-color="#6a3a5a"/><stop offset=".8" stop-color="#e8784a"/><stop offset="1" stop-color="#ffb070"/></linearGradient>
    <linearGradient id="nkTower" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a2a40"/><stop offset=".6" stop-color="#3a3a58"/><stop offset="1" stop-color="#22223a"/></linearGradient>
    <linearGradient id="nkRiver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c86a4a"/><stop offset="1" stop-color="#2a2238"/></linearGradient>
    <radialGradient id="nkFl"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="#fffbe8"/><stop offset=".5" stop-color="#ffe8a8" stop-opacity=".7"/><stop offset="1" stop-color="#ffd080" stop-opacity="0"/></radialGradient>
    <radialGradient id="nkCap" cx=".5" cy=".7" r=".7"><stop offset="0" stop-color="#ffb84a"/><stop offset=".45" stop-color="#c8582a"/><stop offset="1" stop-color="#4a2a2a"/></radialGradient>
    <linearGradient id="nkStem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3a3a"/><stop offset=".5" stop-color="#c8783a"/><stop offset="1" stop-color="#4a3030"/></linearGradient>
    <linearGradient id="nkConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8b8b2"/><stop offset="1" stop-color="#8a8a84"/></linearGradient>`;

  const tower = (x, w, h, G, r, lit = 0.5, kind = -1) => {
    const k = kind >= 0 ? kind : Math.floor(r() * 6), top = G - h, c = ["#2a2a40", "#33304a", "#2a3444", "#3a2e3e", "#283040", "#30344a"][k];
    let outline;
    if (k === 0) outline = `M${x},${G}V${top + 60}H${x + w * 0.15}V${top + 20}H${x + w * 0.85}V${top + 60}H${x + w}V${G}Z`;            // stepped
    else if (k === 1) outline = `M${x},${G}V${top}L${x + w / 2},${top - 90}L${x + w},${top}V${G}Z`;                                    // spire roof
    else if (k === 2) outline = `M${x},${G}V${top + w * 0.4}Q${x},${top} ${x + w / 2},${top}Q${x + w},${top} ${x + w},${top + w * 0.4}V${G}Z`; // round top
    else if (k === 3) outline = `M${x},${G}V${top + 40}L${x + w},${top - 50}V${G}Z`;                                                 // slanted crown
    else if (k === 4) outline = `M${x},${G}V${top}H${x + w * 0.42}V${top + 80}H${x + w * 0.58}V${top - 30}H${x + w}V${G}Z`;           // twin
    else outline = `M${x},${G}V${top + 120}H${x + w * 0.1}V${top + 60}H${x + w * 0.2}V${top}H${x + w * 0.8}V${top + 60}H${x + w * 0.9}V${top + 120}H${x + w}V${G}Z`; // terraced
    let s = `<path d="${outline}" fill="${c}" ${O(3)}/><path d="M${x + w * 0.62},${G}V${top + 60}" stroke="#000" stroke-width="${f1(w * 0.3)}" opacity=".18"/>`;
    const cw = k === 2 ? 16 : 22, rh = k === 4 ? 20 : 26;
    for (let yy = top + 70; yy < G - 20; yy += rh) { const floorLit = r() < lit * 0.6; for (let xx = x + 10; xx < x + w - 14; xx += cw) if (floorLit ? r() < 0.85 : r() < lit * 0.5) s += `<rect x="${xx}" y="${yy}" width="${cw - 8}" height="${rh - 10}" fill="${r() < 0.75 ? "#ffd88a" : "#bfe0ff"}" opacity="${f1(0.5 + r() * 0.5)}"/>`; }
    if (k === 3 || k === 0) s += `<path d="M${x + 6},${top + 70}H${x + w - 6}" stroke="#8a9ab8" stroke-width="3" opacity=".5"/>`;
    if (r() < 0.45) s += `<path d="M${x + w / 2},${top - (k === 1 ? 90 : 0)}V${top - (k === 1 ? 160 : 70)}" stroke="#2a2a40" stroke-width="5"/><circle cx="${x + w / 2}" cy="${top - (k === 1 ? 160 : 70)}" r="6" fill="#ff4a4a"/>`;
    if (k === 5 && r() < 0.6) s += `<path d="M${x + w * 0.2},${top + 2}h${w * 0.6}" stroke="#4a8a5a" stroke-width="10" opacity=".7"/>`;
    return s;
  };
  // a generic prang (temple tower) with smaller spires: reads "Bangkok riverside" without being one real temple
  const prang = (x, G, s) => `<g transform="translate(${x},${G}) scale(${s})" fill="#3a2a3a" ${O(3)}>
    <path d="M-120,0L-100,-80H100L120,0Z"/><path d="M-80,-80L-70,-180H70L80,-80Z"/><path d="M-56,-180Q-60,-300 0,-420Q60,-300 56,-180Z"/>
    ${[-40, 0, 40].map((dx) => `<path d="M${dx - 4},-200v-${dx ? 30 : 40}" stroke="#ffd88a" stroke-width="3" opacity=".5"/>`).join("")}<path d="M0,-420V-500" stroke-width="5"/>
    ${[-200, 200].map((dx) => `<path d="M${dx - 40},0L${dx - 34},-60H${dx + 34}L${dx + 40},0ZM${dx - 26},-60Q${dx - 26},-150 ${dx},-220Q${dx + 26},-150 ${dx + 26},-60Z"/>`).join("")}</g>`;
  const cloudG = (id) => {
    const r = mk(77), puff = (cx, cy, rr, n, fillA, fillB) => Array.from({ length: n }, (_, k) => { const a = (k / n) * Math.PI * 2, d = rr * (0.35 + r() * 0.5), pr = rr * (0.3 + r() * 0.25);
      return `<circle cx="${f1(cx + Math.cos(a) * d * 1.4)}" cy="${f1(cy + Math.sin(a) * d * 0.55)}" r="${f1(pr)}" fill="${r() < 0.5 ? fillA : fillB}"/>`; }).join("");
    return `<g id="${id}">
      <ellipse cx="0" cy="-10" rx="620" ry="90" fill="#8a6a5a" opacity=".55"/>${puff(0, -40, 420, 26, "#9a7a68", "#7a5a4e")}
      <path d="M-90,0C-80,-200 -70,-420 -56,-560H56C70,-420 80,-200 90,0Z" fill="url(#nkStem)"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-70 + (k % 2) * 20},${-40 - k * 58}q60,-26 120,0" stroke="${k % 2 ? "#e8a868" : "#6a4040"}" stroke-width="10" fill="none" opacity=".45"/>`).join("")}
      <ellipse cx="0" cy="-330" rx="230" ry="34" fill="none" stroke="#f4e8e0" stroke-width="16" opacity=".55"/><ellipse cx="0" cy="-326" rx="260" ry="42" fill="none" stroke="#f4e8e0" stroke-width="6" opacity=".3"/>
      <g id="${id}-cap">
        <ellipse cx="0" cy="-560" rx="360" ry="70" fill="#3a2020" opacity=".7"/>
        ${puff(0, -660, 300, 34, "#c8683a", "#a8482a")}${puff(0, -720, 240, 26, "#e8904a", "#c86a3a")}${puff(0, -780, 170, 18, "#f4b86a", "#e8984a")}
        <ellipse cx="0" cy="-600" rx="250" ry="70" fill="#ffd27a" opacity=".55" filter="url(#p2Soft)"/><ellipse cx="0" cy="-610" rx="120" ry="40" fill="#fff0c0" opacity=".7" filter="url(#p2Soft)"/>
        ${puff(0, -840, 140, 14, "#8a4a3a", "#6a3a30")}<path d="M-330,-600Q-360,-700 -280,-760M330,-600Q360,-700 280,-760" stroke="#f4c890" stroke-width="10" opacity=".5" fill="none"/></g>
      <ellipse cx="0" cy="-470" rx="300" ry="40" fill="#f4e8e0" opacity=".22"/></g>`;
  };
  // the flash: a white core, a hot halo, long lens streaks and rays
  const flashG = (id, fx, fy) => `<g id="${id}" style="mix-blend-mode:screen"><circle cx="${fx}" cy="${fy}" r="700" fill="url(#nkFl)" opacity=".8"/><circle cx="${fx}" cy="${fy}" r="320" fill="url(#nkFl)"/>
      ${Array.from({ length: 16 }, (_, k) => `<path d="M${fx},${fy}L${f1(fx + Math.cos((k / 16) * 6.283) * 1600)},${f1(fy + Math.sin((k / 16) * 6.283) * 1600)}" stroke="#fffbe8" stroke-width="${k % 2 ? 6 : 14}" opacity="${k % 2 ? 0.25 : 0.4}"/>`).join("")}
      <ellipse cx="${fx}" cy="${fy}" rx="1800" ry="22" fill="#fffbe8" opacity=".7"/><ellipse cx="${fx}" cy="${fy}" rx="900" ry="8" fill="#fff" opacity=".9"/><circle cx="${fx}" cy="${fy}" r="120" fill="#fff"/>
      ${[[0.4, 30, "#bfe0ff"], [0.7, 50, "#ffd0a0"], [1.25, 80, "#c0ffd0"]].map(([d, rr, c]) => `<circle cx="${f1(fx + (540 - fx) * d * 1.6)}" cy="${f1(fy + (1100 - fy) * d * 1.6)}" r="${rr}" fill="none" stroke="${c}" stroke-width="6" opacity=".4"/>`).join("")}</g>`;

  function bkk(L, o = {}) {
    const id = o.id || "bk", r = mk(o.seed || 31), G = o.g ?? 1180, view = o.view || "skywalk";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="${G + 900}" fill="url(#nkSky)"/><circle cx="${o.sun ?? 1500}" cy="${G - 120}" r="70" fill="#ffd8a0" opacity=".85"/>
      ${[[-800, 300], [-100, 200], [700, 340], [1500, 240]].map(([x, y]) => `<path d="M${x - 300},${y}q90,-50 200,-20q90,-60 220,-10q110,-30 160,30Z" fill="#c86a6a" opacity=".45"/>`).join("")}`);
    // the event in the far layer: the fireball / whiteout core and the mushroom cloud
    if (o.cloud) { const [cx, cy, cs] = o.cloud; put(L.far, `<g transform="translate(${cx},${cy}) scale(${cs})">${cloudG(`${id}-cl`)}</g>`); }
    let far = "";
    for (let k = 0; k < 34; k++) { const x = -1400 + k * 115 + r() * 40, w = 70 + r() * 90, h = 160 + r() * 420; far += tower(x, w, h, G - 40, r, 0.25, k % 6); }
    put(L.far, `<g opacity=".75">${far}</g>`);
    let mid = `<rect x="-1400" y="${G - 40}" width="3900" height="200" fill="url(#nkRiver)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M${-1300 + k * 380},${G + 20 + (k % 3) * 30}h${120 + (k % 4) * 40}" stroke="#ffc890" stroke-width="4" opacity=".4"/>`).join("")}
      ${prang(o.prang ?? 150, G - 30, 1.15)}`;
    for (let k = 0; k < 14; k++) { const x = -1300 + k * 290 + r() * 60; if (Math.abs(x - (o.prang ?? 150)) < 330) continue; mid += tower(x, 110 + r() * 120, 380 + r() * 620, G - 30, r, 0.45, (k * 5 + 2) % 6); }
    put(L.mid, mid);
    // the elevated rail viaduct and power lines
    let s = `<path d="M-1400,${G + 40}H2500V${G + 76}H-1400Z" fill="#6a6a70" ${O(4)}/>${Array.from({ length: 9 }, (_, k) => `<rect x="${-1300 + k * 450}" y="${G + 76}" width="54" height="600" fill="#7a7a80" ${O(3)}/>`).join("")}
      <g transform="translate(${o.train ?? 300},${G + 40})"><rect x="0" y="-80" width="760" height="80" rx="16" fill="#d8dce0" ${O(4)}/>${Array.from({ length: 12 }, (_, k) => `<rect x="${24 + k * 60}" y="-66" width="40" height="34" rx="4" fill="#3a4a5a"/>`).join("")}<path d="M0,-20H760" stroke="#2a8a5a" stroke-width="10"/></g>`;
    s += `<path d="M-1400,${G - 140}Q-600,${G - 80} 200,${G - 150}T2500,${G - 120}M-1400,${G - 120}Q-500,${G - 50} 400,${G - 130}T2500,${G - 100}M-1400,${G - 100}Q-800,${G - 30} 0,${G - 110}T2500,${G - 80}" stroke="#1a1a24" stroke-width="3" fill="none"/>`;
    put(L.set, s);
    if (view === "skywalk") {
      put(L.set, `<path d="M-1400,${G + 320}H2500V${G + 900}H-1400Z" fill="#4a4a52"/><path d="M-1400,${G + 320}H2500" stroke="#8a8a92" stroke-width="10"/>
        ${Array.from({ length: 30 }, (_, k) => `<path d="M${-1400 + k * 140},${G + 330}l-80,570" stroke="#5a5a62" stroke-width="4"/>`).join("")}`);
      put(L.fg, `<g>${Array.from({ length: 26 }, (_, k) => `<path d="M${-1500 + k * 170},${G + 140}V${G + 330}" stroke="#b8bcc0" stroke-width="10"/>`).join("")}<path d="M-1600,${G + 140}H2700" stroke="#d8dce0" stroke-width="22" stroke-linecap="round"/><path d="M-1600,${G + 150}H2700" stroke="#7a7e84" stroke-width="6"/></g>`);
    } else if (view === "parking") {
      put(L.set, `<path d="M-1400,${G + 200}H2500V${G + 1200}H-1400Z" fill="#5a5a60"/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-1300 + k * 330},${G + 230}l-140,900" stroke="#e8e8d8" stroke-width="10" opacity=".8"/>`).join("")}<path d="M-1400,${G + 200}H2500" stroke="#a8a8a0" stroke-width="16"/>
        ${Array.from({ length: 6 }, (_, k) => { const x = -1150 + k * 660, c = ["#c84a3a", "#e8e4dc", "#3a5a8a", "#2a2a2a", "#8a8a90", "#e8c84a"][k]; return `<g transform="translate(${x},${G + 560})"><rect x="-200" y="-150" width="400" height="150" rx="40" fill="${c}" ${O(5)}/><path d="M-130,-150L-90,-250H110L150,-150Z" fill="${c}" ${O(5)}/><path d="M-106,-156L-74,-232H96L126,-156Z" fill="#5a7a9a"/><circle cx="-120" cy="0" r="42" fill="#1a1a1a"/><circle cx="120" cy="0" r="42" fill="#1a1a1a"/><circle cx="186" cy="-100" r="14" fill="#ffd060"/></g>`; }).join("")}`);
    } else if (view === "street") {
      put(L.set, `<path d="M-1400,${G + 200}H2500V${G + 1100}H-1400Z" fill="#3a3a40"/><path d="M-1400,${G + 200}H2500" stroke="#c8c8c0" stroke-width="12"/>${Array.from({ length: 8 }, (_, k) => `<path d="M${-1200 + k * 480},${G + 520}h200" stroke="#e8e0a0" stroke-width="12"/>`).join("")}
        ${Array.from({ length: 7 }, (_, k) => { const x = -1200 + k * 520, c = ["#c84a3a", "#e8e4dc", "#3a5a8a", "#e8c84a", "#2a2a2a", "#8a8a90", "#4a8a5a"][k]; return `<g transform="translate(${x},${G + 420})"><rect x="-150" y="-110" width="300" height="110" rx="30" fill="${c}" ${O(4)}/><path d="M-100,-110L-70,-180H80L110,-110Z" fill="${c}" ${O(4)}/><path d="M-80,-114L-58,-168H70L92,-114Z" fill="#5a7a9a"/><circle cx="-90" cy="0" r="30" fill="#1a1a1a"/><circle cx="90" cy="0" r="30" fill="#1a1a1a"/><circle cx="140" cy="-70" r="12" fill="#ff5a3a"/></g>`; }).join("")}
        <g transform="translate(900,${G + 300})"><rect x="-90" y="-70" width="180" height="70" rx="10" fill="#2a8a8a" ${O(3)}/><path d="M-90,-70Q0,-150 90,-70" fill="#e8c84a" ${O(3)}/><circle cx="-50" cy="0" r="20" fill="#1a1a1a"/><circle cx="60" cy="0" r="20" fill="#1a1a1a"/></g>`);
    } else if (view === "window") {
      put(L.set, `<path fill-rule="evenodd" d="M-1600,-1000H2700V3000H-1600Z M-60,${G - 760}H1140V${G + 160}H-60Z" fill="#d8cfc0"/><g transform="translate(1500,${G + 600})"><rect x="-170" y="-1000" width="340" height="1000" fill="#8a5a34" ${O(5)}/><rect x="-150" y="-980" width="300" height="980" fill="#a8784a" ${O(3)}/><circle cx="110" cy="-480" r="18" fill="#d8c060" ${O(3)}/><rect x="96" y="-430" width="28" height="44" rx="4" fill="#9a9a9a" ${O(2)}/></g><rect x="-60" y="${G - 760}" width="1200" height="920" fill="none" stroke="#6a6a70" stroke-width="30"/><path d="M540,${G - 760}V${G + 160}" stroke="#6a6a70" stroke-width="22"/>
        <path d="M-1600,${G + 160}H2700V3000H-1600Z" fill="#b8a888"/><rect x="-1600" y="${G + 160}" width="4300" height="40" fill="#8a7a62"/>`);
    }
    if (o.flash) { const [fx, fy] = o.flash; put(L.mid, flashG(`${id}-fl`, fx, fy)); }
    put(L.glow, `<rect id="${id}-white" x="-2000" y="-1400" width="5200" height="4400" fill="#fffdf4" opacity="${o.white ?? 0}"/>`);
  }

  function shelter(L, o = {}) {
    const id = o.id || "sh", G = 1500;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#3a3a38"/>`);
    let s = `<path d="M-1400,-900H2500V${G}H-1400Z" fill="url(#nkConc)"/><path d="M-1400,${G}H2500V2600H-1400Z" fill="#9a9a92"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-1200 + k * 420},${G}l-180,900" stroke="#e8e0a0" stroke-width="10" opacity=".6"/>`).join("")}
      <path d="M-1400,${G - 900}H2500" stroke="#4a4a46" stroke-width="40"/>${Array.from({ length: 6 }, (_, k) => `<rect x="${-1300 + k * 700}" y="${G - 880}" width="120" height="880" fill="#9a9a94" ${O(4)}/><path d="M${-1300 + k * 700},${G - 600}h120" stroke="#e8c84a" stroke-width="30"/><path d="M${-1300 + k * 700},${G - 600}h120" stroke="#2a2a2a" stroke-width="30" stroke-dasharray="20 20"/>`).join("")}
      ${[-900, 400, 1700].map((x) => `<g transform="translate(${x},${G - 840})"><rect x="-70" y="-26" width="140" height="40" rx="6" fill="#2a2a2a"/><rect x="-60" y="-20" width="120" height="28" rx="4" fill="#fffbe0"/></g>`).join("")}
      <g transform="translate(1900,${G - 300})"><path d="M-200,300L-100,-400H400L500,300Z" fill="${o.dust ? "#e8c8a0" : "#c8c8b8"}" opacity=".85"/><text x="150" y="-430" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="60" fill="#2fa864">ทางขึ้น</text></g>`;
    put(L.set, s);
    put(L.glow, `<radialGradient id="${id}-lg"><stop offset="0" stop-color="#fffbe0" stop-opacity=".55"/><stop offset="1" stop-color="#fffbe0" stop-opacity="0"/></radialGradient>
      ${[-900, 400].map((x) => `<ellipse cx="${x}" cy="${G - 500}" rx="700" ry="600" fill="url(#${id}-lg)"/>`).join("")}
      <rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0c14" opacity=".12"/>${o.dust ? `<ellipse cx="2000" cy="${G}" rx="500" ry="300" fill="#e8c8a0" opacity=".35"/>` : ""}`);
  }

  // the old wooden shophouse where ยายทวด lives: folding wooden doors, a family shrine shelf, old photos, a TV, a calendar, a tin box
  function shophouse(L, o = {}) {
    const id = o.id || "sp", G = 1560;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#3a2a20"/>`);
    let s = `<rect x="-1400" y="-900" width="3900" height="${G + 900}" fill="#d8c4a0"/><rect x="-1400" y="${G - 300}" width="3900" height="300" fill="#b89a70"/><path d="M-1400,${G}H2500V2600H-1400Z" fill="#8a6a4a"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${-1400 + k * 300},${G}l-120,1000" stroke="#6a4a30" stroke-width="5"/>`).join("")}
      <g transform="translate(-700,${G})">${Array.from({ length: 6 }, (_, k) => `<rect x="${k * 120}" y="-1300" width="114" height="1300" fill="#8a5a34" ${O(3)}/><rect x="${k * 120 + 16}" y="-1240" width="82" height="300" fill="#a8784a" ${O(2)}/>`).join("")}<rect x="0" y="-1340" width="720" height="50" fill="#5a3a20" ${O(3)}/></g>
      <g transform="translate(500,${G - 980})"><rect x="-200" y="0" width="400" height="30" fill="#7a3a20" ${O(3)}/><rect x="-120" y="-160" width="240" height="160" fill="#c8302a" ${O(3)}/><circle cx="0" cy="-90" r="40" fill="#e8c060" ${O(2)}/><path d="M-180,0v-60M180,0v-60" stroke="#e8c060" stroke-width="10"/><circle cx="-140" cy="-20" r="10" fill="#ffd060"/><circle cx="140" cy="-20" r="10" fill="#ffd060"/></g>
      ${[[200, G - 640, 0], [380, G - 680, 1], [820, G - 640, 2]].map(([x, y, k]) => `<g transform="translate(${x},${y}) rotate(${k - 1})"><rect x="-70" y="-90" width="140" height="180" fill="#5a3a20" ${O(3)}/><rect x="-56" y="-76" width="112" height="152" fill="${["#c8b898", "#b8a888", "#d8c8a8"][k]}"/><path d="M-40,40q20,-60 40,-20q20,-60 40,20" fill="#6a5a48" opacity=".6"/></g>`).join("")}
      <g transform="translate(1100,${G - 760})"><rect x="-80" y="0" width="160" height="200" fill="#fbfaf4" ${O(3)}/><rect x="-80" y="0" width="160" height="50" fill="#c8302a"/><text y="140" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="80" fill="#2a2a2a">2</text></g>
      <g transform="translate(1250,${G - 180})"><rect x="-200" y="-30" width="400" height="200" fill="#7a5030" ${O(4)}/><rect x="-150" y="-260" width="300" height="220" rx="16" fill="#2a2a30" ${O(4)}/><rect x="-130" y="-240" width="260" height="180" rx="8" fill="#5a8aa8"/></g>
      <path d="M-1400,${G - 1500}H2500" stroke="#5a3a20" stroke-width="40"/>`;
    put(L.set, s);
    put(L.glow, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#e8784a" opacity=".08"/><radialGradient id="${id}-lg"><stop offset="0" stop-color="#fff0c8" stop-opacity=".5"/><stop offset="1" stop-color="#fff0c8" stop-opacity="0"/></radialGradient><ellipse cx="500" cy="${G - 700}" rx="900" ry="700" fill="url(#${id}-lg)"/>`);
  }
  // props that the hands grab
  const NP = (window.NukeProp = {});
  NP.gold = `<g><path d="M-60,0Q0,60 60,0" stroke="#e8c040" stroke-width="10" fill="none"/>${Array.from({ length: 7 }, (_, k) => `<circle cx="${-60 + k * 20}" cy="${Math.round(Math.sin((k / 6) * 3.14) * 28)}" r="7" fill="#ffd860" stroke="#a8801a" stroke-width="2"/>`).join("")}<rect x="-14" y="30" width="28" height="30" rx="6" fill="#ffd860" stroke="#a8801a" stroke-width="3"/></g>`;
  NP.cat = `<g><ellipse cx="0" cy="0" rx="70" ry="44" fill="#e8a858" ${O(3)}/><circle cx="60" cy="-30" r="36" fill="#e8a858" ${O(3)}/><path d="M38,-58l6,-30l20,22M70,-62l18,-26l6,30" fill="#e8a858" ${O(3)}/><circle cx="52" cy="-32" r="6" fill="#2a2a2a"/><circle cx="74" cy="-32" r="6" fill="#2a2a2a"/><path d="M-66,0q-50,-40 -30,-90" stroke="#e8a858" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-30,-30l10,30M0,-40l10,30" stroke="#c87a30" stroke-width="6"/></g>`;
  NP.remote = `<g><rect x="-20" y="-60" width="40" height="120" rx="12" fill="#2a2a30" ${O(3)}/><circle cy="-36" r="8" fill="#e8382e"/>${[0, 1, 2].map((k) => `<rect x="-12" y="${-12 + k * 20}" width="24" height="12" rx="3" fill="#8a8a90"/>`).join("")}</g>`;
  NP.water = `<g><rect x="-26" y="-70" width="52" height="140" rx="14" fill="#bfe0ff" opacity=".85" ${O(3)}/><rect x="-14" y="-90" width="28" height="22" rx="4" fill="#2a6ac8" ${O(2)}/><path d="M-26,-10H26" stroke="#fff" stroke-width="5" opacity=".6"/></g>`;
  NP.radio = `<g><rect x="-60" y="-40" width="120" height="80" rx="12" fill="#c8302a" ${O(3)}/><circle cx="-24" cy="0" r="24" fill="#2a2a2a"/><rect x="10" y="-20" width="38" height="16" rx="4" fill="#ffe8a0"/><path d="M40,-40l20,-50" stroke="#8a8a8a" stroke-width="5"/></g>`;
  NP.meds = `<g><rect x="-30" y="-40" width="60" height="80" rx="8" fill="#fbfaf4" ${O(3)}/><rect x="-30" y="-40" width="60" height="22" rx="6" fill="#2fa864"/><path d="M-8,10h16M0,2v16" stroke="#e2382e" stroke-width="6"/></g>`;
  NP.tin = `<g><rect x="-70" y="-46" width="140" height="92" rx="10" fill="#4a6a8a" ${O(3)}/><rect x="-70" y="-46" width="140" height="24" rx="8" fill="#6a8aa8" ${O(3)}/><circle r="16" fill="#c8a040" ${O(2)}/></g>`;
  Object.assign(Sets, { bkk, shelter, shophouse });

  // ---------------- cast ----------------
  const { LINE, dk } = Rig2;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const bob = (h) => `<path d="M-52,-548C-62,-616 -16,-634 6,-632C38,-630 62,-608 54,-548Q50,-584 26,-596Q4,-604 -20,-592Q-42,-580 -52,-548Z" fill="${h.c}" ${ln()}/><path d="M-56,-560Q-66,-500 -50,-468Q-40,-500 -46,-540Z M56,-560Q66,-500 50,-468Q40,-500 46,-540Z" fill="${h.c}" ${ln()}/>`;
  const lan = `<path d="M-22,-488L-6,-410M22,-488L6,-410" stroke="#c83a3a" stroke-width="5"/><rect x="-16" y="-412" width="32" height="40" rx="4" fill="#fbfaf4" ${ln(2)}/>`;
  const ploy = { skin: "#e0a87e", iris: "#2a1a10", lash: true, blush: 0.5, lip: "#c8584a", hair: { c: "#1a1210", s: "#000", sh: "#5a4034", front: (x) => bob(x.hair) },
    top: { kind: "blouse", c: "#e8e4f4", sleeve: "elbow", trim: "#c8c0e0" }, print: lan, bottom: { kind: "jeans", c: "#2a2a3a" }, feet: { kind: "sneaker", c: "#e8e8e8", sole: "#aaa" } };
  const phum = { ...Rig.CAST.beam.v2, skin: "#d8a070" };
  const uncle = { skin: "#9a6a44", iris: "#2a1a10", blush: 0.2, hair: { c: "#8a8a8a", s: "#5a5a5a", sh: "#c8c8c8", front: (x) => `<path d="M-50,-556C-56,-610 -10,-622 6,-620C34,-618 56,-600 50,-556Q40,-580 10,-584Q-30,-584 -50,-556Z" fill="${x.hair.c}" ${ln()}/>` },
    top: { kind: "shirt", c: "#4a5a7a", sleeve: "short", neck: "collar", collar: "#4a5a7a", button: "#d8c060", trim: "#3a4a6a" }, print: `<rect x="-50" y="-470" width="30" height="20" fill="#d8c060"/>`, bottom: { kind: "jeans", c: "#2a3a5a" }, feet: { kind: "boot", c: "#1a1a1a" } };
  Object.assign(Rig.CAST, { ploy: { v2: ploy }, phum: { v2: phum }, uncle: { v2: uncle }, ployPhone: { v2: ploy, hand: `<g transform="translate(0,118) rotate(-10)"><rect x="-20" y="-40" width="40" height="76" rx="7" fill="#1a1c22" ${ln(2.2)}/><rect x="-15" y="-34" width="30" height="62" rx="4" fill="#3a8a5a"/></g>`, keep: "F" } });

  const tuad = { skin: "#c89a7a", iris: "#3a2418", lash: true, blush: 0.25, lip: "#a8645a",
    hair: { c: "#eeeae4", s: "#a8a49c", sh: "#fff", front: (x) => `<path d="M-48,-552C-54,-610 -16,-626 4,-626C30,-624 52,-606 48,-552Q42,-578 26,-588Q8,-596 -12,-588Q-34,-580 -48,-552Z" fill="#eeeae4" ${ln()}/><path d="M-30,-540q8,6 16,2M14,-538q8,4 16,-2" stroke="#8a7a6a" stroke-width="2" fill="none"/>`, back: (x) => `<circle cx="34" cy="-594" r="24" fill="#e0dcd4" ${ln()}/>` },
    top: { kind: "blouse", c: "#e8e0f0", sleeve: "elbow", trim: "#c8b8d8" }, bottom: { kind: "sarong", c: "#4a5a3a", band: "#c8a040", band2: "#c8a040" }, feet: { kind: "sandal", c: "#5a3a2a" },
    face: `<g fill="none" stroke="#3a2a2a" stroke-width="3"><circle cx="-22" cy="-552" r="15"/><circle cx="22" cy="-552" r="15"/><path d="M-7,-552h14"/></g>` };
  Object.assign(Rig.CAST, { tuad: { v2: tuad }, tuadTin: { v2: tuad, hand: `<g transform="translate(0,128) scale(.8)">${NP.tin}</g>`, keep: "F" },
    phumCat: { v2: phum, hand: `<g transform="translate(10,120) scale(.9)">${NP.cat}</g>`, keep: "F" }, chaiRemote: { v2: uncle, hand: `<g transform="translate(0,120) rotate(-20) scale(.8)">${NP.remote}</g>`, keep: "F" },
    ployGold: { v2: ploy, hand: `<g transform="translate(0,124) scale(.8)">${NP.gold}</g>`, keep: "F" } });
  Rig.MODES.grabUp = (u) => { const j = Math.sin(u * 17) * 3; return { ...Rig.MODES.idle(u, {}), uaF: -150 + j, faF: -30, uaB: -40, faB: -60, torso: -8 + j * 0.3, head: -10, thF: -20, shF: 30, bodyY: 6 }; };
  Rig.MODES.hugCat = (u) => { const j = Math.sin(u * 13) * 2; return { ...Rig.MODES.idle(u, {}), uaF: -70 + j, faF: -100, uaB: -60, faB: -110, torso: 4, head: 6 + j }; };
  const M = Rig.MODES;
  M.shield = (u) => { const j = Math.sin(u * 31) * 2; return { ...M.idle(u, {}), uaF: -150 + j, faF: -100, uaB: -120, faB: -110, torso: -14 + j * 0.4, head: -22 + j, bodyY: 8 }; };
  M.look = (u) => ({ ...M.idle(u, {}), head: -8 + 2 * Math.sin(u * 1.7), uaF: -20, faF: -60, torso: -3 });
  M.reachDoor = (u) => { const j = Math.sin(u * 19) * 2; return { ...M.idle(u, {}), uaF: -88 + j, faF: -4, uaB: 10, faB: -30, torso: 10, head: 4 + j, thF: -20, shF: 20, thB: 16, shB: 10 }; };
})();
