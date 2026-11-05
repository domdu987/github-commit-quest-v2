// ---------- ถูกหวยทั้งบ้าน: the house (load after lotcast.js) ----------
// Same layer contract as the other kits (sky / far / mid / set / act / fg; glow over the darkness; light = screen space).
//   Sets.lotBed(L, o)    your room in the morning: peach wall, a thin plywood partition at the left (seams, a knot hole),
//                        the window at the right with sun shafts across the bed, a fan, a football poster, the clock (o.clock "7:12")
//                        bed: mattress top y 1200, pillow at x 130…430 (#id-pillow), blanket from x 380
//   Sets.lotHouse(L, o)  the whole house cut open like a doll's house: two floors × three rooms, thin inner walls.
//                        rooms (x0, x1, floor y): up A 50–380, B 380–710, C 710–1030 on y 1030 · down A, B, C on y 1550
//                        A↑ your room · B↑ grandma's mattress and shrine · C↑ ป้าศรี's window · A↓ kitchen (calendar + sign, small)
//                        B↓ the dining table and ลุงหมาน's boxes · C↓ the stairs and the front door
//   Sets.lotTable(L, o)  the dining table front on, the kitchen wall behind it with the sign (x 300, y 430) and the calendar
//                        (x 790, y 560); table top y 1270, its front edge in fg; o.time "morning" | "night"
(function () {
  const { T, at, INK } = Lot;
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const put = (el, h) => el.insertAdjacentHTML("beforeend", h);
  const f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => () => ((seed = (seed * 9301 + 49297) % 233280) / 233280);

  // ---------------- small furniture ----------------
  const fan = (x, y, s) => at(x, y, s, `<rect x="-8" y="0" width="16" height="200" fill="#d8dce0" ${O(3)}/><ellipse cx="0" cy="206" rx="60" ry="14" fill="#c8ccd2" ${O(3)}/>
    <circle cx="0" cy="-40" r="78" fill="#e8f0f4" fill-opacity=".55" ${O(4)}/><circle cx="0" cy="-40" r="16" fill="#5a8ac0" ${O(3)}/>
    <path d="M0,-40L-50,-90M0,-40L60,-60M0,-40L-10,24" stroke="#9ab8d8" stroke-width="16" stroke-linecap="round" opacity=".7"/>`);
  const poster = (x, y, s) => at(x, y, s, `<rect x="-110" y="-150" width="220" height="300" fill="#2a5a9a" ${O(4)}/><circle cx="0" cy="-30" r="56" fill="#f4f0e6" ${O(3)}/>
    <path d="M0,-86l18,34l-18,26l-18,-26zM-50,-50l30,14M50,-50l-30,14M-34,20l18,-20M34,20l-18,-20" stroke="${INK}" stroke-width="5" fill="#2e2a26"/>
    ${T(0, 92, 44, "สู้ๆ", { fill: "#f2c55c" })}<path d="M-110,-150l20,14M110,-150l-20,14" stroke="#d8d0b8" stroke-width="6"/>`);
  const clock = (x, y, s, txt = "7:12") => at(x, y, s, `<rect x="-70" y="-40" width="140" height="80" rx="14" fill="#2a2e34" ${O(4)}/>
    <rect x="-58" y="-28" width="116" height="56" rx="8" fill="#141a14"/>${T(0, 16, 44, txt, { fill: "#7cff9a", font: "Kanit", w: 700 })}`);
  const windowM = (x, y, w, h, o = {}) => {
    const day = o.time !== "night";
    return `<g transform="translate(${x},${y})"><rect x="-14" y="-14" width="${w + 28}" height="${h + 28}" rx="6" fill="#e8dcc4" ${O(4)}/>
      <rect x="0" y="0" width="${w}" height="${h}" fill="${day ? "url(#lotSkyW)" : "#1a2440"}"/>
      ${day ? `<path d="M0,${h * 0.72}Q${w * 0.3},${h * 0.6} ${w * 0.55},${h * 0.7}T${w},${h * 0.62}V${h}H0Z" fill="#8ab878"/>
        <rect x="${w * 0.12}" y="${h * 0.46}" width="${w * 0.22}" height="${h * 0.3}" fill="#e8d8c0"/><path d="M${w * 0.1},${h * 0.48}L${w * 0.23},${h * 0.36}L${w * 0.36},${h * 0.48}Z" fill="#c8603e"/>
        <rect x="${w * 0.58}" y="${h * 0.4}" width="${w * 0.26}" height="${h * 0.36}" fill="#d8e0e8"/>` : `<circle cx="${w * 0.75}" cy="${h * 0.25}" r="${w * 0.07}" fill="#f4ecc8"/>`}
      <path d="M${w / 2},0V${h}M0,${h / 2}H${w}" stroke="#e8dcc4" stroke-width="12"/>
      <path d="M-20,-24Q${w * 0.12},${h * 0.4} -10,${h + 20}H-40V-24Z" fill="${o.curtain || "#d8604e"}" ${O(3)}/>
      <path d="M${w + 20},-24Q${w * 0.88},${h * 0.4} ${w + 10},${h + 20}H${w + 40}V-24Z" fill="${o.curtain || "#d8604e"}" ${O(3)}/></g>`;
  };
  const DEFS = `<defs><linearGradient id="lotSkyW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8cc6ec"/><stop offset="1" stop-color="#f4e8c8"/></linearGradient>
    <linearGradient id="lotSun" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff2c8" stop-opacity=".75"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></linearGradient>
    <linearGradient id="lotWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b4804e"/><stop offset="1" stop-color="#8a5a32"/></linearGradient>
    <radialGradient id="lotLamp" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".85"/><stop offset="1" stop-color="#ffe2a0" stop-opacity="0"/></radialGradient></defs>`;
  const planks = (x0, x1, y0, y1, c = "#b98a5a") => {
    let s = `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="${c}"/>`;
    for (let y = y0 + 34; y < y1; y += 34 + ((y * 7) % 9)) s += `<path d="M${x0},${y}H${x1}" stroke="#8a5e36" stroke-width="3" opacity=".55"/>`;
    return s;
  };

  // ---------------- your room ----------------
  Sets.lotBed = (L, o = {}) => {
    const id = o.id || "bd";
    put(L.sky, `${DEFS}<rect x="-1200" y="-900" width="3500" height="4000" fill="#efc9a6"/>`);
    let s = `<rect x="-600" y="-400" width="2300" height="1920" fill="#f2cfae"/><path d="M-600,1100H1700" stroke="#e2b894" stroke-width="10" opacity=".5"/>
      <rect x="-600" y="1490" width="2300" height="30" fill="#d0a37a"/>${planks(-600, 1700, 1520, 2600)}`;
    // the thin plywood partition at the left: seams and a knot hole
    s += `<rect x="-600" y="-400" width="660" height="1920" fill="#d8b688"/>`;
    for (let x = -560; x < 60; x += 120) s += `<path d="M${x},-400V1520" stroke="#b8925e" stroke-width="5"/>`;
    s += `<path d="M60,-400V1520" stroke="${INK}" stroke-width="6" opacity=".35"/><ellipse cx="-20" cy="760" rx="14" ry="10" fill="#4a3420"/>
      ${windowM(640, 360, 360, 470, o)}${poster(330, 560, 0.95)}${fan(-160, 1250, 1.0)}
      <g transform="translate(980,1200)"><rect x="-80" y="0" width="160" height="300" fill="#a8743e" ${O(4)}/><rect x="-80" y="-20" width="160" height="26" fill="#c8945a" ${O(4)}/></g>
      ${clock(980, 1150, 0.9, o.clock || "7:12")}`;
    // the bed
    s += `<rect x="40" y="1190" width="980" height="230" rx="18" fill="#f4f0e8" ${O(5)}/><rect x="40" y="1380" width="980" height="120" fill="#8a5a32" ${O(5)}/>
      <path d="M40,1300H1020" stroke="#d8d4c8" stroke-width="5"/>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    // the pillow: in front of the sleeper by default; o.pillow "back" puts it behind the actors (a head can rest on it), "none" leaves it out (in hand)
    const pillow = `<g id="${id}-pillow"><path d="M120,1150Q110,1110 160,1104H400Q446,1110 436,1150Q446,1196 400,1204H160Q110,1198 120,1150Z" fill="#fbfaf6" ${O(5)}/>
      <path d="M150,1150Q280,1132 410,1150" stroke="#e0dcd2" stroke-width="5" fill="none"/></g>`;
    if (o.pillow === "back") put(L.set, pillow);
    // the blanket: flat over the legs by default; o.blanket "up" is a mound over someone lying down
    const bp = o.blanket === "up" ? "M372,1094Q470,1036 640,1056Q900,1084 1030,1166V1430H352Q326,1250 372,1094Z" : "M380,1180Q600,1150 1030,1190V1430H360Q340,1300 380,1180Z";
    put(o.blanket === "back" ? L.set : L.fg, `${o.pillow === "back" || o.pillow === "none" ? "" : pillow}<g id="${id}-blanket"><defs><clipPath id="${id}-bcl"><path d="${bp}"/></clipPath></defs><path d="${bp}" fill="#4f86c2" ${O(5)}/>
      <g clip-path="url(#${id}-bcl)">${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${430 + k * 100},1000V1430" stroke="#3a6aa0" stroke-width="8" opacity=".6"/>`).join("")}
      ${[0, 1, 2, 3].map((k) => `<path d="M352,${1100 + k * 70}Q700,${1070 + k * 70} 1030,${1160 + k * 70}" stroke="#3a6aa0" stroke-width="8" fill="none" opacity=".6"/>`).join("")}</g>
      <path d="${bp}" fill="none" ${O(5)}/></g>`);
    if (o.time !== "night") put(L.glow, `<path d="M640,360L1000,360L560,1500L-80,1500Z" fill="url(#lotSun)" opacity=".55" style="mix-blend-mode:screen"/>`);
  };

  // ---------------- the doll's house ----------------
  Sets.lotHouse = (L, o = {}) => {
    const id = o.id || "hs", r = mk(o.seed || 17), night = o.time === "night";
    put(L.sky, `${DEFS}<defs><linearGradient id="${id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${night ? "#141a34" : "#7cb8e6"}"/>
      <stop offset="1" stop-color="${night ? "#3a3048" : "#f6e2b8"}"/></linearGradient></defs><rect x="-1400" y="-1000" width="3900" height="4200" fill="url(#${id}-sky)"/>`);
    let far = "";
    for (let k = 0; k < 9; k++) { const x = -500 + k * 260 + r() * 60, h = 380 + r() * 260;
      far += `<rect x="${f1(x)}" y="${f1(1560 - h)}" width="230" height="${f1(h)}" fill="${night ? "#2a2a3e" : "#c8b8a8"}" opacity=".85"/>
        <path d="M${f1(x - 14)},${f1(1560 - h)}L${f1(x + 115)},${f1(1500 - h)}L${f1(x + 244)},${f1(1560 - h)}Z" fill="${night ? "#22223a" : "#b07a62"}" opacity=".85"/>`; }
    far += `<path d="M-600,300Q540,360 1700,290M-600,330Q540,400 1700,320" stroke="#2e2a26" stroke-width="3" fill="none" opacity=".5"/>`;
    put(L.far, far);
    // shell
    let s = `<rect x="-700" y="1550" width="2500" height="900" fill="${night ? "#3a3a40" : "#9a948a"}"/><path d="M-700,1556H1800" stroke="#c8c0b0" stroke-width="10"/>
      <path d="M10,520L540,190L1070,520Z" fill="#b8503a" ${O(6)}/><path d="M80,500L540,222L1000,500" stroke="#8a3626" stroke-width="10" fill="none"/>
      <rect x="30" y="510" width="1020" height="1050" fill="#f2d6b4" ${O(6)}/>`;
    const room = (x0, x1, y0, y1, wall, floor = "#c8955e") => `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="${wall}"/>
      <rect x="${x0}" y="${y1 - 26}" width="${x1 - x0}" height="26" fill="${floor}"/><path d="M${x0},${y1 - 26}H${x1}" stroke="#8a5e36" stroke-width="3"/>`;
    s += room(50, 380, 530, 1030, "#bfe0e8") + room(380, 710, 530, 1030, "#f0e2c0") + room(710, 1030, 530, 1030, "#f4cdd8");
    s += room(50, 380, 1040, 1550, "#e8f0dc", "#bca07a") + room(380, 710, 1040, 1550, "#f6e6c8") + room(710, 1030, 1040, 1550, "#e6dccc");
    // floors and thin walls (the joke: plywood a finger thick)
    s += `<rect x="30" y="1026" width="1020" height="20" fill="#8a5e36" ${O(4)}/>
      ${[380, 710].map((x) => `<rect x="${x - 4}" y="530" width="8" height="500" fill="#c8a878" ${O(2)}/><rect x="${x - 4}" y="1046" width="8" height="504" fill="#c8a878" ${O(2)}/>`).join("")}`;
    // A↑ your room: bed, poster, the window
    s += `<rect x="70" y="900" width="250" height="110" rx="10" fill="#f4f0e8" ${O(3)}/><rect x="70" y="990" width="250" height="20" fill="#8a5a32"/>
      <path d="M80,898Q76,876 100,874H170Q190,880 186,900Z" fill="#fff" ${O(3)}/>${poster(250, 680, 0.45)}${windowM(80, 590, 100, 120, o)}`;
    // B↑ grandma: a floor mattress, the shrine shelf, a folded net
    s += `<rect x="410" y="960" width="230" height="50" rx="10" fill="#e8d8b0" ${O(3)}/><path d="M410,975H640" stroke="#c8b888" stroke-width="4"/>
      <g transform="translate(560,700)"><rect x="-70" y="0" width="140" height="16" fill="#8a5a32" ${O(3)}/><path d="M-20,0V-46Q0,-70 20,-46V0Z" fill="#e8c860" ${O(3)}/>
        <circle cx="0" cy="-58" r="10" fill="#e8c860" ${O(3)}/><rect x="40" y="-30" width="10" height="30" fill="#f4f0e8"/><path d="M45,-30v-14" stroke="#ff9a3a" stroke-width="4"/></g>
      <path d="M400,560Q520,600 690,560" stroke="#e8e8f0" stroke-width="14" fill="none" opacity=".8"/>`;
    // C↑ ป้าศรี: the big window on the soi, a mirror, a fan
    s += `${windowM(820, 600, 160, 210, { ...o, curtain: "#e6bf3e" })}<rect x="740" y="740" width="60" height="110" rx="20" fill="#cfe4ec" ${O(3)}/>${fan(760, 900, 0.45)}`;
    // A↓ kitchen: stove, pots, fridge, the calendar and the sign (small at this scale)
    s += `<rect x="70" y="1330" width="180" height="200" fill="#e8e8e0" ${O(3)}/><rect x="70" y="1310" width="180" height="26" fill="#a8a8a0" ${O(3)}/>
      <ellipse cx="120" cy="1300" rx="34" ry="12" fill="#5a5a5a" ${O(3)}/><rect x="270" y="1180" width="100" height="350" rx="10" fill="#f4f6f8" ${O(3)}/><path d="M280,1300H360" stroke="#b8c0c8" stroke-width="4"/>
      ${Lot.calendar(300, 1150, 0.17, { id: `${id}-cal` })}${Lot.sign(150, 1070, 0.22, { id: `${id}-sg` })}`;
    // B↓ dining: the table, the TV, ลุงหมาน's boxes of past businesses
    s += `<rect x="420" y="1400" width="240" height="22" fill="#a8743e" ${O(3)}/><path d="M440,1422V1530M640,1422V1530" stroke="#8a5a32" stroke-width="12"/>
      ${[0, 1, 2].map((k) => `<ellipse cx="${470 + k * 70}" cy="1394" rx="22" ry="9" fill="#f4f0e8" ${O(2)}/>`).join("")}
      <rect x="560" y="1110" width="130" height="80" rx="6" fill="#2a2e34" ${O(3)}/>
      ${[[388, 1470, "ครีม"], [468, 1470, "ปลากัด"], [416, 1406, "คริปโต"]].map(([x, y, t]) => `<g transform="translate(${x},${y})"><rect x="0" y="0" width="${t.length * 12 + 26}" height="62" fill="#c8a06a" ${O(3)}/>${T(t.length * 6 + 13, 40, 22, t, { fill: "#5a3a1a", w: 700 })}</g>`).join("")}`;
    // C↓ the stairs and the front door
    s += `<path d="M720,1550L1000,1046" stroke="#8a5a32" stroke-width="20"/>${[...Array(8)].map((_, k) => `<path d="M${734 + k * 35},${1525 - k * 63}h40" stroke="#a8743e" stroke-width="14"/>`).join("")}
      <rect x="930" y="1290" width="90" height="250" fill="#7a4a2a" ${O(3)}/><circle cx="946" cy="1420" r="6" fill="#e8c860"/>
      <g>${[0, 1, 2].map((k) => `<ellipse cx="${760 + k * 40}" cy="1540" rx="18" ry="7" fill="#3a3a40"/>`).join("")}</g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    if (!night) put(L.glow, `<path d="M1030,600L1030,1000L740,1030L760,700Z" fill="url(#lotSun)" opacity=".35" style="mix-blend-mode:screen"/>`);
    else put(L.glow, `<circle cx="540" cy="1250" r="260" fill="url(#lotLamp)" opacity=".7"/>`);
  };

  // ---------------- the dining table ----------------
  Sets.lotTable = (L, o = {}) => {
    const id = o.id || "tb", night = o.time === "night";
    put(L.sky, `${DEFS}<rect x="-1200" y="-900" width="3500" height="4000" fill="${night ? "#3a2e2a" : "#f0e2c4"}"/>`);
    let s = `<rect x="-700" y="-400" width="2500" height="1300" fill="${night ? "#8a7a62" : "#f4e6c8"}"/>
      <rect x="-700" y="900" width="2500" height="420" fill="${night ? "#7a8a86" : "#cfe2dc"}"/>`;
    for (let x = -700; x < 1800; x += 60) s += `<path d="M${x},900V1320" stroke="${night ? "#5a6a66" : "#a8c4bc"}" stroke-width="3"/>`;
    for (let y = 960; y < 1320; y += 60) s += `<path d="M-700,${y}H1800" stroke="${night ? "#5a6a66" : "#a8c4bc"}" stroke-width="3"/>`;
    s += `<path d="M-700,900H1800" stroke="#a88a5a" stroke-width="12"/>
      <g transform="translate(-60,640)"><rect x="-160" y="0" width="320" height="18" fill="#8a5a32" ${O(3)}/>
        ${[-120, -50, 20, 90].map((x, k) => `<rect x="${x}" y="${-70 - (k % 2) * 16}" width="50" height="${70 + (k % 2) * 16}" rx="8" fill="${["#e8c860", "#c8603e", "#9ac8a8", "#e8dcc4"][k]}" ${O(3)}/>`).join("")}</g>
      <g transform="translate(1060,300)"><rect x="-150" y="0" width="300" height="1020" rx="16" fill="#e8eef2" ${O(5)}/><path d="M-150,380H150" stroke="#b8c4cc" stroke-width="5"/>
        <rect x="-90" y="440" width="60" height="44" rx="6" fill="#d8443a"/><rect x="10" y="120" width="70" height="50" rx="6" fill="#3a9c66"/></g>
      ${Lot.sign(300, 330, 0.95, { id: `${id}-sg` })}${Lot.calendar(790, 560, 0.86, { id: `${id}-cal` })}
      <g transform="translate(560,180)"><circle r="62" fill="#fbfaf6" ${O(5)}/><path d="M0,0V-40M0,0L28,14" stroke="${INK}" stroke-width="6" stroke-linecap="round"/></g>
      <rect x="-700" y="1320" width="2500" height="1300" fill="${night ? "#5a4636" : "#b98a5a"}"/>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    // the table: its top and front edge sit over the seated family
    const bowls = [-560, -330, 150, 360, 560, 760, 960, 1300, 1520].map((x, k) => `<ellipse cx="${x}" cy="1262" rx="52" ry="16" fill="#f4f2ec" ${O(3)}/><path d="M${x - 46},1262Q${x},1300 ${x + 46},1262" fill="#e8e4da" ${O(3)}/>
      <path d="M${x - 30},1258Q${x},1246 ${x + 30},1258" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("");
    put(L.fg, `<g id="${id}-table"><rect x="-900" y="1270" width="2900" height="30" fill="#c8945a" ${O(5)}/><rect x="-900" y="1298" width="2900" height="560" fill="url(#lotWood)" ${O(5)}/>
      <path d="M-900,1340H2000" stroke="#7a4a2a" stroke-width="4" opacity=".5"/>${bowls}
      <g transform="translate(470,1250)"><path d="M-70,0Q-70,-70 0,-74Q70,-70 70,0Z" fill="#c8c8c0" ${O(4)}/><rect x="-80" y="-6" width="160" height="14" rx="6" fill="#a8a8a0" ${O(3)}/></g>
      <g transform="translate(700,1250)"><ellipse rx="80" ry="20" fill="#fff" ${O(3)}/><ellipse cx="-20" cy="-6" rx="24" ry="12" fill="#f4f0e6"/><circle cx="-20" cy="-8" r="8" fill="#f2b632"/>
        <ellipse cx="26" cy="-4" rx="24" ry="12" fill="#f4f0e6"/><circle cx="26" cy="-6" r="8" fill="#f2b632"/></g></g>`);
    if (night) put(L.glow, `<path d="M540,-80V120" stroke="#2e2a26" stroke-width="6"/><path d="M440,120H640L600,60H480Z" fill="#e8c878" ${O(4)}/>
      <circle cx="540" cy="160" r="560" fill="url(#lotLamp)" opacity=".55" style="mix-blend-mode:screen"/>`);
    else put(L.glow, `<path d="M-300,-200L500,-200L1300,1500L300,1500Z" fill="url(#lotSun)" opacity=".28" style="mix-blend-mode:screen"/>`);
  };
  // ---------------- under the dining table (EP.3): six laps, the knees, the shins, the feet; o.people = [{ x, pants, skin, shoes, kind }] ----------------
  Sets.lotUnder = (L, o = {}) => {
    const id = o.id || "ud";
    put(L.sky, `${DEFS}<rect x="-1200" y="-900" width="3500" height="4000" fill="#17120e"/>`);
    const fy = o.floor ?? 1500;   // the floor line; the feet sit on it
    let s = `<rect x="-700" y="${fy}" width="2500" height="1400" fill="#3e3a40"/>`;
    for (let x = -700; x < 1800; x += 140) s += `<path d="M${x},${fy}L${x - 260},${fy + 900}" stroke="#2e2a30" stroke-width="4"/>`;
    s += `<path d="M-700,${fy}H1800" stroke="#5a5560" stroke-width="6"/>`;
    (o.people || []).forEach((p) => {
      const x = p.x, legs = (dx) => `<rect x="${x + dx - 34}" y="${p.kind === "shorts" ? 380 : 300}" width="68" height="${fy - 40 - (p.kind === "shorts" ? 380 : 300)}" rx="30" fill="${p.kind === "pants" ? p.pants : p.skin}" ${O(5)}/>`;
      s += legs(-44) + legs(44);
      if (p.kind === "shorts") s += `<path d="M${x - 92},250H${x + 92}L${x + 88},420H${x - 88}Z" fill="${p.pants}" ${O(5)}/>`;
      if (p.kind === "sarong") s += `<path d="M${x - 100},250H${x + 100}L${x + 96},${p.long ? fy - 80 : 250 + (fy - 250) * 0.66}H${x - 96}Z" fill="${p.pants}" ${O(5)}/>
        ${[0, 1, 2, 3, 4, 5, 6, 7].filter((k) => 330 + k * 120 < (p.long ? fy - 80 : 250 + (fy - 250) * 0.66)).map((k) => `<path d="M${x - 92},${330 + k * 120}H${x + 92}" stroke="${p.band || "#e8d8a8"}" stroke-width="7" opacity=".55"/>`).join("")}`;
      if (p.kind === "pants") s += `<path d="M${x - 92},250H${x + 92}L${x + 88},360H${x - 88}Z" fill="${p.pants}" ${O(5)}/>`;
      s += [-44, 44].map((dx) => `<ellipse cx="${x + dx + (dx < 0 ? -10 : 10)}" cy="${fy - 28}" rx="58" ry="26" fill="${p.shoes || "#3a3a40"}" ${O(5)}/>`).join("");
    });
    put(L.set, `<g id="${id}-world">${s}</g>`);
    // the underside of the table top, a rail, the chair seats' edges: over the knees (fg)
    put(L.fg, `<rect x="-700" y="-500" width="2500" height="640" fill="#4a2f1c" ${O(6)}/>${[0, 1, 2, 3].map((k) => `<path d="M-700,${-380 + k * 120}H1800" stroke="#3a2414" stroke-width="5"/>`).join("")}
      <rect x="-700" y="140" width="2500" height="60" fill="#6a4428" ${O(6)}/>`);
    put(L.glow, `<rect x="-700" y="200" width="2500" height="300" fill="#ffd9a0" opacity=".08"/>`);
  };
})();
