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
    <linearGradient id="nkConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a8a86"/><stop offset="1" stop-color="#5a5a56"/></linearGradient>`;

  const tower = (x, w, h, G, r, lit = 0.5) => {
    let s = `<rect x="${x}" y="${G - h}" width="${w}" height="${h}" fill="url(#nkTower)" ${O(3)}/>`;
    for (let yy = G - h + 20; yy < G - 20; yy += 26) for (let xx = x + 10; xx < x + w - 14; xx += 22) if (r() < lit) s += `<rect x="${xx}" y="${yy}" width="12" height="14" fill="${r() < 0.7 ? "#ffd88a" : "#bfe0ff"}" opacity="${f1(0.5 + r() * 0.5)}"/>`;
    if (r() < 0.5) s += `<path d="M${x + w / 2},${G - h}V${G - h - 60}" stroke="#2a2a40" stroke-width="5"/><circle cx="${x + w / 2}" cy="${G - h - 60}" r="5" fill="#ff4a4a"/>`;
    return s;
  };
  // a generic prang (temple tower) with smaller spires: reads "Bangkok riverside" without being one real temple
  const prang = (x, G, s) => `<g transform="translate(${x},${G}) scale(${s})" fill="#3a2a3a" ${O(3)}>
    <path d="M-120,0L-100,-80H100L120,0Z"/><path d="M-80,-80L-70,-180H70L80,-80Z"/><path d="M-56,-180Q-60,-300 0,-420Q60,-300 56,-180Z"/>
    ${[-40, 0, 40].map((dx) => `<path d="M${dx - 4},-200v-${dx ? 30 : 40}" stroke="#ffd88a" stroke-width="3" opacity=".5"/>`).join("")}<path d="M0,-420V-500" stroke-width="5"/>
    ${[-200, 200].map((dx) => `<path d="M${dx - 40},0L${dx - 34},-60H${dx + 34}L${dx + 40},0ZM${dx - 26},-60Q${dx - 26},-150 ${dx},-220Q${dx + 26},-150 ${dx + 26},-60Z"/>`).join("")}</g>`;
  const cloudG = (id) => `<g id="${id}"><path d="M-70,0Q-60,-300 -50,-560H50Q60,-300 70,0Z" fill="url(#nkStem)" opacity=".95"/>
      <ellipse cx="0" cy="-20" rx="420" ry="60" fill="#8a6a5a" opacity=".55"/>
      <g id="${id}-cap"><ellipse cx="0" cy="-620" rx="300" ry="130" fill="url(#nkCap)" ${O(4)}/>
        ${[[-200, -640, 120], [200, -640, 120], [-90, -720, 130], [100, -730, 120], [0, -770, 110], [-260, -590, 80], [260, -590, 80]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="url(#nkCap)" opacity=".95"/>`).join("")}
        <ellipse cx="0" cy="-560" rx="320" ry="50" fill="#3a2020" opacity=".6"/><ellipse cx="0" cy="-650" rx="150" ry="60" fill="#ffd27a" opacity=".55"/></g>
      <ellipse cx="0" cy="-360" rx="160" ry="30" fill="none" stroke="#e8b080" stroke-width="10" opacity=".5"/></g>`;

  function bkk(L, o = {}) {
    const id = o.id || "bk", r = mk(o.seed || 31), G = o.g ?? 1180, view = o.view || "skywalk";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="${G + 900}" fill="url(#nkSky)"/><circle cx="${o.sun ?? 1500}" cy="${G - 120}" r="70" fill="#ffd8a0" opacity=".85"/>
      ${[[-800, 300], [-100, 200], [700, 340], [1500, 240]].map(([x, y]) => `<path d="M${x - 300},${y}q90,-50 200,-20q90,-60 220,-10q110,-30 160,30Z" fill="#c86a6a" opacity=".45"/>`).join("")}`);
    // the event in the far layer: the fireball / whiteout core and the mushroom cloud
    if (o.cloud) { const [cx, cy, cs] = o.cloud; put(L.far, `<g transform="translate(${cx},${cy}) scale(${cs})">${cloudG(`${id}-cl`)}</g>`); }
    let far = "";
    for (let k = 0; k < 34; k++) { const x = -1400 + k * 115 + r() * 40, w = 70 + r() * 90, h = 160 + r() * 420; far += tower(x, w, h, G - 40, r, 0.25); }
    put(L.far, `<g opacity=".75">${far}</g>`);
    let mid = `<rect x="-1400" y="${G - 40}" width="3900" height="200" fill="url(#nkRiver)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M${-1300 + k * 380},${G + 20 + (k % 3) * 30}h${120 + (k % 4) * 40}" stroke="#ffc890" stroke-width="4" opacity=".4"/>`).join("")}
      ${prang(o.prang ?? 150, G - 30, 1.15)}`;
    for (let k = 0; k < 14; k++) { const x = -1300 + k * 290 + r() * 60; if (Math.abs(x - (o.prang ?? 150)) < 330) continue; mid += tower(x, 110 + r() * 120, 380 + r() * 620, G - 30, r, 0.45); }
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
    } else if (view === "street") {
      put(L.set, `<path d="M-1400,${G + 200}H2500V${G + 1100}H-1400Z" fill="#3a3a40"/><path d="M-1400,${G + 200}H2500" stroke="#c8c8c0" stroke-width="12"/>${Array.from({ length: 8 }, (_, k) => `<path d="M${-1200 + k * 480},${G + 520}h200" stroke="#e8e0a0" stroke-width="12"/>`).join("")}
        ${Array.from({ length: 7 }, (_, k) => { const x = -1200 + k * 520, c = ["#c84a3a", "#e8e4dc", "#3a5a8a", "#e8c84a", "#2a2a2a", "#8a8a90", "#4a8a5a"][k]; return `<g transform="translate(${x},${G + 420})"><rect x="-150" y="-110" width="300" height="110" rx="30" fill="${c}" ${O(4)}/><path d="M-100,-110L-70,-180H80L110,-110Z" fill="${c}" ${O(4)}/><path d="M-80,-114L-58,-168H70L92,-114Z" fill="#5a7a9a"/><circle cx="-90" cy="0" r="30" fill="#1a1a1a"/><circle cx="90" cy="0" r="30" fill="#1a1a1a"/><circle cx="140" cy="-70" r="12" fill="#ff5a3a"/></g>`; }).join("")}
        <g transform="translate(900,${G + 300})"><rect x="-90" y="-70" width="180" height="70" rx="10" fill="#2a8a8a" ${O(3)}/><path d="M-90,-70Q0,-150 90,-70" fill="#e8c84a" ${O(3)}/><circle cx="-50" cy="0" r="20" fill="#1a1a1a"/><circle cx="60" cy="0" r="20" fill="#1a1a1a"/></g>`);
    } else if (view === "window") {
      put(L.set, `<path fill-rule="evenodd" d="M-1600,-1000H2700V3000H-1600Z M-60,${G - 760}H1140V${G + 160}H-60Z" fill="#d8cfc0"/><g transform="translate(1500,${G + 600})"><rect x="-170" y="-1000" width="340" height="1000" fill="#8a5a34" ${O(5)}/><rect x="-150" y="-980" width="300" height="980" fill="#a8784a" ${O(3)}/><circle cx="110" cy="-480" r="18" fill="#d8c060" ${O(3)}/><rect x="96" y="-430" width="28" height="44" rx="4" fill="#9a9a9a" ${O(2)}/></g><rect x="-60" y="${G - 760}" width="1200" height="920" fill="none" stroke="#6a6a70" stroke-width="30"/><path d="M540,${G - 760}V${G + 160}" stroke="#6a6a70" stroke-width="22"/>
        <path d="M-1600,${G + 160}H2700V3000H-1600Z" fill="#b8a888"/><rect x="-1600" y="${G + 160}" width="4300" height="40" fill="#8a7a62"/>`);
    }
    if (o.flash) { const [fx, fy] = o.flash; put(L.mid, `<g id="${id}-fl" style="mix-blend-mode:screen"><circle cx="${fx}" cy="${fy}" r="520" fill="url(#nkFl)"/><circle cx="${fx}" cy="${fy}" r="110" fill="#fff"/></g>`); }
    put(L.glow, `<rect id="${id}-white" x="-2000" y="-1400" width="5200" height="4400" fill="#fffdf4" opacity="${o.white ?? 0}"/>`);
  }

  function shelter(L, o = {}) {
    const id = o.id || "sh", G = 1500;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#3a3a38"/>`);
    let s = `<path d="M-1400,-900H2500V${G}H-1400Z" fill="url(#nkConc)"/><path d="M-1400,${G}H2500V2600H-1400Z" fill="#6a6a64"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-1200 + k * 420},${G}l-180,900" stroke="#e8e0a0" stroke-width="10" opacity=".6"/>`).join("")}
      <path d="M-1400,${G - 900}H2500" stroke="#4a4a46" stroke-width="40"/>${Array.from({ length: 6 }, (_, k) => `<rect x="${-1300 + k * 700}" y="${G - 880}" width="120" height="880" fill="#9a9a94" ${O(4)}/><path d="M${-1300 + k * 700},${G - 600}h120" stroke="#e8c84a" stroke-width="30"/><path d="M${-1300 + k * 700},${G - 600}h120" stroke="#2a2a2a" stroke-width="30" stroke-dasharray="20 20"/>`).join("")}
      ${[-900, 400, 1700].map((x) => `<g transform="translate(${x},${G - 840})"><rect x="-70" y="-26" width="140" height="40" rx="6" fill="#2a2a2a"/><rect x="-60" y="-20" width="120" height="28" rx="4" fill="#fffbe0"/></g>`).join("")}
      <g transform="translate(1900,${G - 300})"><path d="M-200,300L-100,-400H400L500,300Z" fill="${o.dust ? "#e8c8a0" : "#c8c8b8"}" opacity=".85"/><text x="150" y="-430" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="60" fill="#2fa864">ทางขึ้น</text></g>`;
    put(L.set, s);
    put(L.glow, `<radialGradient id="${id}-lg"><stop offset="0" stop-color="#fffbe0" stop-opacity=".35"/><stop offset="1" stop-color="#fffbe0" stop-opacity="0"/></radialGradient>
      ${[-900, 400].map((x) => `<ellipse cx="${x}" cy="${G - 500}" rx="700" ry="600" fill="url(#${id}-lg)"/>`).join("")}
      <rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0c14" opacity=".35"/>${o.dust ? `<ellipse cx="2000" cy="${G}" rx="500" ry="300" fill="#e8c8a0" opacity=".35"/>` : ""}`);
  }
  Object.assign(Sets, { bkk, shelter });

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
  const M = Rig.MODES;
  M.shield = (u) => { const j = Math.sin(u * 31) * 2; return { ...M.idle(u, {}), uaF: -150 + j, faF: -100, uaB: -120, faB: -110, torso: -14 + j * 0.4, head: -22 + j, bodyY: 8 }; };
  M.look = (u) => ({ ...M.idle(u, {}), head: -8 + 2 * Math.sin(u * 1.7), uaF: -20, faF: -60, torso: -3 });
  M.reachDoor = (u) => { const j = Math.sin(u * 19) * 2; return { ...M.idle(u, {}), uaF: -88 + j, faF: -4, uaB: 10, faB: -30, torso: 10, head: 4 + j, thF: -20, shF: 20, thB: 16, shB: 10 }; };
})();
