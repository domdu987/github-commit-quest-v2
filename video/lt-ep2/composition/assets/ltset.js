// ช่างเชื่อมสายฟ้า (story 3) · sets in the channel look (layered depth, both frames). Ground for people: y 1400. Load after jkset.js + ltcast.js.
//   Sets.ltShop(L, o)  the narrow alley in ฝั่งธน with ร้านเหล็กดัดเจ๊หงส์ across the back (shutter, sign, stacked gates), the power pole + transformer at x 1650 (#id-tf),
//                      a street lamp on it; on the pavement: gas cylinders x 230, the welding machine x 420, the trestles with a gate x 760 (#id-gate), the bike x 1450 (o.bike),
//                      the money table x 1200 (o.table), the banana tree behind the shop corner x 1850 (o.banana → #id-tree .ltBan), a puddle x 980 (o.puddle)
//                      o.time: "day" | "storm" | "dusk" | "night" · o.rain · o.blackout (every light off) · #id-lamps = all the lights (toggle for the blackout)
//   Sets.ltRoof(L, o)  the rooftop of the 7-storey building: storm sky, the city far below, the giant billboard frame (#id-frame; weld at its left post x 760), water tank, stairwell box, the front parapet
//   Sets.ltWard(L, o)  the hospital ward: windows, curtains, beds at x 420 / 1080 / 1740 (mattress top y 1172), the ECG monitor x 1560 (#id-ecg, #id-ecgLine), IV stand
//                      o.nursery: three incubators instead of beds (#id-inc0..2 at x 420 / 900 / 1380) · o.night · o.blackout · o.drawing (the crayon picture on the door)
//   Sets.ltRoom(L, o)  the rental-house corridor at night: a door x 1000 (o.doorFront puts it in the set layer), the old fuse box on the wall x 1560 (#id-box, lid #id-box-lid), a bare bulb (#id-bulb)
//   Sets.ltSky(L, o)   the district seen from the alley mouth: the skyline with its windows (#id-lights), the hospital (red cross), the store sign, the temple, the transformer pole x 1500 (#id-tf);
//                      the wet street in front (puddle x 900) · o.storm · o.blackout
(function () {
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}${o.rot ? ` transform="rotate(${o.rot} ${f(x)} ${f(y)})"` : ""}>${text}</text>`;
  Sets.DEFS += `
    <linearGradient id="ltDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a8ad0"/><stop offset=".45" stop-color="#9cc4e8"/><stop offset=".8" stop-color="#e8e0cc"/><stop offset="1" stop-color="#f0e6d2"/></linearGradient>
    <linearGradient id="ltStorm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14181f"/><stop offset=".4" stop-color="#2c3340"/><stop offset=".75" stop-color="#4a5262"/><stop offset="1" stop-color="#6a7080"/></linearGradient>
    <linearGradient id="ltDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2e5a"/><stop offset=".4" stop-color="#6a4a7a"/><stop offset=".7" stop-color="#d87a60"/><stop offset="1" stop-color="#f0b880"/></linearGradient>
    <linearGradient id="ltNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06081a"/><stop offset=".5" stop-color="#121a3a"/><stop offset=".85" stop-color="#262e4e"/><stop offset="1" stop-color="#363c58"/></linearGradient>
    <linearGradient id="ltConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e8e8a"/><stop offset="1" stop-color="#6a6a68"/></linearGradient>
    <linearGradient id="ltWetConc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a5e66"/><stop offset="1" stop-color="#3a3e48"/></linearGradient>
    <linearGradient id="ltAwning" x1="0" y1="0" x2="1" y2="0">${[...Array(10)].map((_, k) => `<stop offset="${k / 10}" stop-color="${k % 2 ? "#b8342e" : "#e8e0d0"}"/><stop offset="${(k + 1) / 10}" stop-color="${k % 2 ? "#b8342e" : "#e8e0d0"}"/>`).join("")}</linearGradient>
    <linearGradient id="ltSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a5e66"/><stop offset=".5" stop-color="#8a8f98"/><stop offset="1" stop-color="#4a4e56"/></linearGradient>
    <linearGradient id="ltGlassW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe4f4"/><stop offset="1" stop-color="#8ab4d8"/></linearGradient>
    <radialGradient id="ltLamp"><stop offset="0" stop-color="#fff4c8" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd890" stop-opacity=".4"/><stop offset="1" stop-color="#ff9a30" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltFluor"><stop offset="0" stop-color="#e8f8ff" stop-opacity=".9"/><stop offset=".5" stop-color="#b8e0ff" stop-opacity=".3"/><stop offset="1" stop-color="#80b0ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="ltWinGlow"><stop offset="0" stop-color="#ffe8a0" stop-opacity=".9"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>`;
  const SKY = { day: "ltDay", storm: "ltStorm", dusk: "ltDusk", night: "ltNight" };
  const SKYTOP = { day: "#4a8ad0", storm: "#14181f", dusk: "#2a2e5a", night: "#06081a" };
  const dark = (time) => time === "night" || time === "storm";
  const clouds = (r, y0, c, n = 7, op = 0.9) => [...Array(n)].map((_, k) => { const x = -2200 + k * 900 + r() * 300, y = y0 + r() * 120, s = 0.8 + r() * 0.6; return `<g class="ltCloud" transform="translate(${f(x)},${f(y)}) scale(${f(s)})" opacity="${op}"><ellipse rx="420" ry="90" fill="${c}"/><ellipse cx="-160" cy="-50" rx="220" ry="110" fill="${c}"/><ellipse cx="140" cy="-70" rx="260" ry="130" fill="${c}"/></g>`; }).join("");
  const stars = (r, n = 40) => [...Array(n)].map(() => `<circle cx="${f(-1600 + r() * 4600)}" cy="${f(-400 + r() * 900)}" r="${f(0.8 + r() * 1.5)}" fill="#e8ecff" opacity="${f(0.3 + r() * 0.6)}"/>`).join("");
  // a row of shophouses for the far skyline: [x, w, h, colour]
  const skyline = (r, y, blocks, lit, cls = "ltWin") => blocks.map(([x, w, h, c]) => { let s = `<rect x="${x}" y="${y - h}" width="${w}" height="${h}" fill="${c}"/>`;
    for (let yy = y - h + 40; yy < y - 40; yy += 70) for (let xx = x + 24; xx < x + w - 40; xx += 60) if (r() > 0.45) s += `<rect class="${cls}" x="${xx}" y="${f(yy)}" width="26" height="36" fill="${lit ? (r() > 0.5 ? "#ffd890" : "#c8e8ff") : "#6a7a90"}" opacity="${lit ? f(0.6 + r() * 0.4) : 0.5}"/>`;
    return s; }).join("");
  const pole = (x, y, id, o = {}) => `<g id="${id}" transform="translate(${x},${y})"><rect x="-14" y="-820" width="28" height="820" fill="#5a5a60"/><rect x="-14" y="-820" width="10" height="820" fill="#7a7a80"/>
    <rect x="-110" y="-760" width="220" height="12" fill="#3a3a40"/><rect x="-110" y="-690" width="220" height="12" fill="#3a3a40"/>${[-90, -50, 50, 90].map((dx) => `<rect x="${dx - 5}" y="-782" width="10" height="24" fill="#8a9098"/>`).join("")}
    <g id="${id}-box"><rect x="22" y="-640" width="110" height="150" rx="8" fill="#5a6066"/><rect x="22" y="-640" width="110" height="150" rx="8" fill="url(#flV)"/>${[0, 1, 2, 3].map((k) => `<rect x="30" y="${-626 + k * 32}" width="94" height="8" fill="#3a3e44"/>`).join("")}<path d="M40,-640V-680M110,-640V-680" stroke="#3a3a40" stroke-width="5"/></g>
    ${o.lamp ? `<path d="M0,-560L-160,-600" stroke="#5a5a60" stroke-width="12" stroke-linecap="round"/><path d="M-176,-592Q-200,-612 -150,-620Q-120,-612 -140,-592Z" fill="#6a6a70"/><ellipse class="ltLampOn" cx="-162" cy="-590" rx="22" ry="8" fill="#fff4c8"/>` : ""}</g>`;
  const cables = (x0, x1, y, n = 4) => [...Array(n)].map((_, k) => `<path d="M${x0},${y + k * 18}Q${(x0 + x1) / 2},${y + k * 18 + 70 + k * 10} ${x1},${y + k * 18 + 6}" stroke="#2a2a30" stroke-width="${4 - k * 0.5}" fill="none"/>`).join("");
  const house = (x, w, h, c, o = {}) => `<g transform="translate(${x},1180)"><rect x="0" y="${-h}" width="${w}" height="${h}" fill="${c}"/><rect x="0" y="${-h}" width="${w}" height="${h}" fill="url(#flV)" opacity=".5"/>
    <rect x="-10" y="${-h - 18}" width="${w + 20}" height="22" fill="${o.roof || "#6a4a3a"}"/>${[...Array(Math.floor(w / 220))].map((_, k) => `<rect class="ltWin" x="${50 + k * 220}" y="${-h + 70}" width="110" height="130" fill="${o.lit ? "#ffd890" : "#8ab0cc"}" opacity="${o.lit ? 0.9 : 0.8}"/><rect x="${50 + k * 220}" y="${-h + 70}" width="110" height="130" fill="none" stroke="#f4f4f0" stroke-width="6"/><path d="M${105 + k * 220},${-h + 70}V${-h + 200}" stroke="#f4f4f0" stroke-width="4"/>`).join("")}
    <rect x="0" y="-360" width="${w}" height="14" fill="#4a3a30" opacity=".6"/>${o.plain ? "" : `<rect x="${w * 0.3}" y="-300" width="${w * 0.4}" height="300" fill="${o.lit ? "#ffe8b0" : "#3a3a44"}" opacity=".9"/><rect x="${w * 0.3}" y="-300" width="${w * 0.4}" height="300" fill="none" stroke="#7a7a80" stroke-width="8"/>`}</g>`;
  // the shop front: shutter raised, dark interior with stacked gates, the welding machine, the sign, the awning
  const shopFront = (id, lit, time) => `<g id="${id}-shop" transform="translate(360,1180)"><rect x="0" y="-760" width="1040" height="760" fill="#cdc2ae"/><rect x="0" y="-760" width="1040" height="760" fill="url(#flV)" opacity=".5"/>
    <rect x="-12" y="-782" width="1064" height="26" fill="#6a4a3a"/><rect x="60" y="-700" width="200" height="150" fill="${lit ? "#ffd890" : "#8ab0cc"}" opacity=".9"/><rect x="60" y="-700" width="200" height="150" fill="none" stroke="#f4f4f0" stroke-width="6"/><path d="M160,-700V-550" stroke="#f4f4f0" stroke-width="4"/>
    <rect x="740" y="-700" width="200" height="150" fill="${lit ? "#ffd890" : "#8ab0cc"}" opacity=".9"/><rect x="740" y="-700" width="200" height="150" fill="none" stroke="#f4f4f0" stroke-width="6"/><path d="M840,-700V-550" stroke="#f4f4f0" stroke-width="4"/>
    <rect x="80" y="-470" width="880" height="470" fill="${dark(time) ? "#14141c" : "#2a2a34"}"/>
    <g class="ltInterior">${[0, 1, 2].map((k) => `<g transform="translate(${160 + k * 60},0) skewX(-6)">${LT.GATE(240, 380)}</g>`).join("")}<g transform="translate(700,0)"><rect x="-80" y="-170" width="160" height="170" rx="8" fill="#c8a040"/><rect x="-80" y="-170" width="160" height="170" rx="8" fill="url(#flV)"/><circle cx="-30" cy="-120" r="16" fill="#1a1a1e"/><circle cx="30" cy="-120" r="16" fill="#1a1a1e"/><rect x="-60" y="-80" width="120" height="40" fill="#2a2a30"/><path d="M-80,-60q-60,40 -40,120" stroke="#1a1a1e" stroke-width="6" fill="none"/></g>
      <g transform="translate(880,0)">${[0, 1, 2, 3, 4].map((k) => `<rect x="${-40 + k * 14}" y="-420" width="8" height="420" fill="#6a6e76"/>`).join("")}</g></g>
    <g id="${id}-fluor"><rect x="300" y="-460" width="440" height="12" rx="6" fill="${lit ? "#f0fbff" : "#8a9098"}"/></g>
    <rect x="60" y="-500" width="920" height="40" fill="#8a8f98"/>${[...Array(23)].map((_, k) => `<path d="M${80 + k * 40},-500V-460" stroke="#6a6e76" stroke-width="3"/>`).join("")}
    <g id="${id}-sign"><rect x="130" y="-640" width="780" height="130" rx="10" fill="#1e3a7a"/><rect x="130" y="-640" width="780" height="130" rx="10" fill="url(#flV)" opacity=".6"/><rect x="140" y="-630" width="760" height="110" rx="8" fill="none" stroke="#f6d36a" stroke-width="4"/>
      ${T(520, -568, 62, "เหล็กดัด เจ๊หงส์", { fill: "#f6d36a", w: 900 })}${T(520, -527, 24, "ประตูรั้ว · เหล็กดัด · โครงหลังคา · รับงานด่วน", { fill: "#f4ecd8", w: 700 })}</g>
    <path d="M20,-500H1020L1060,-400H-20Z" fill="url(#ltAwning)"/><path d="M-20,-400H1060" stroke="#8a2a24" stroke-width="8"/>${[...Array(12)].map((_, k) => `<path d="M${-20 + k * 98},-400q24,30 48,0" stroke="#8a2a24" stroke-width="6" fill="none"/>`).join("")}</g>`;
  const workbench = (id, gate = true) => `<g id="${id}-bench" transform="translate(760,1400)"><path d="M-170,0L-130,-150H-110L-150,0ZM170,0L130,-150H110L150,0Z" fill="#4a4e56"/><rect x="-180" y="-160" width="360" height="16" rx="4" fill="#6a6e76"/>
    <path d="M-150,-100H-110M110,-100H150" stroke="#4a4e56" stroke-width="8"/>${gate ? `<g id="${id}-gate" transform="translate(0,-160) scale(1,0.98)">${LT.GATE(320, 400)}</g>` : ""}</g>`;
  const machine = (x) => `<g transform="translate(${x},1400)"><rect x="-70" y="-150" width="140" height="150" rx="8" fill="#c8a040"/><rect x="-70" y="-150" width="140" height="150" rx="8" fill="url(#flV)"/><rect x="-60" y="-140" width="120" height="50" rx="4" fill="#2a2a30"/><circle cx="-30" cy="-115" r="14" fill="#d8352a"/><circle cx="30" cy="-115" r="14" fill="#1a1a1e"/><rect x="-50" y="-70" width="100" height="40" fill="#3a3a40"/>
    <path d="M-70,-40Q-130,-20 -110,60Q-90,120 -30,90" stroke="#1a1a1e" stroke-width="6" fill="none"/><path d="M70,-40Q140,-30 120,60" stroke="#8a2a24" stroke-width="6" fill="none"/><rect x="-80" y="-10" width="160" height="12" fill="#3a3a40"/></g>`;
  const cylinders = (x) => `<g transform="translate(${x},1400)"><g transform="translate(-30,0)">${LT.CYL("#3a7ab8")}</g><g transform="translate(30,0) scale(.92)">${LT.CYL("#4a9a5a")}</g><path d="M-30,-180Q0,-230 30,-180" stroke="#2a2a30" stroke-width="5" fill="none"/><rect x="-66" y="-30" width="132" height="10" fill="#3a3a40"/></g>`;
  const table = (x, id) => `<g id="${id}-table" transform="translate(${x},1400)"><rect x="-150" y="-240" width="300" height="20" rx="4" fill="#e8e4dc"/><rect x="-150" y="-240" width="300" height="20" rx="4" fill="url(#flV)"/><path d="M-130,-220L-150,0M130,-220L150,0M-120,-120H120" stroke="#8a8f98" stroke-width="8"/>
    <g transform="translate(60,-240)"><rect x="-60" y="-50" width="120" height="50" rx="6" fill="#4a7a4a"/><rect x="-60" y="-50" width="120" height="50" rx="6" fill="url(#flV)"/><rect x="-50" y="-62" width="100" height="14" rx="3" fill="#3a6a3a"/><path d="M-20,-20h40" stroke="#1a2a1a" stroke-width="4"/></g>
    <g transform="translate(-70,-250)"><rect x="-50" y="-10" width="100" height="90" rx="6" fill="#f4ecd8"/>${T(0, 28, 26, "ชาร์จ", { fill: "#2e2a26", w: 900 })}${T(0, 62, 30, "20 ฿", { fill: "#d8352a", w: 900 })}</g></g>`;
  const puddle = (x, y, rx, ry, c = "#9ab8c8") => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${c}" opacity=".55"/><ellipse cx="${x}" cy="${y - 2}" rx="${rx * 0.7}" ry="${ry * 0.5}" fill="#e8f4fc" opacity=".35"/>`;
  const RAIN = (id, n = 160, seed = 3) => { const r = mk(seed); let d = ""; for (let i = 0; i < n; i++) { const x = r() * 1800 - 400, y = r() * 2600 - 400, l = 60 + r() * 80; d += `M${f(x)},${f(y)}l${f(-l * 0.16)},${f(l)}`; }
    return `<g id="${id}" class="ltRain"><path d="${d}" stroke="#c8dce8" stroke-width="3" opacity=".4" stroke-linecap="round"/><path d="${d}" transform="translate(0,-2600)" stroke="#c8dce8" stroke-width="3" opacity=".4" stroke-linecap="round"/></g>`; };
  window.LTS = { clouds, stars, skyline, pole, cables, house, puddle, RAIN, workbench, table };

  // ---------------- the alley and the shop ----------------
  Sets.ltShop = (L, o = {}) => {
    const id = o.id || "lts", r = mk(o.seed || 7), time = o.time || "day", night = dark(time), lit = night && !o.blackout, bike = o.bike !== false;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${SKYTOP[time]}"/><rect x="-3000" y="-1400" width="8000" height="2600" fill="url(#${SKY[time]})"/>
      ${time === "night" ? stars(r) : ""}${time === "storm" ? clouds(r, 200, "#1c2029", 7, 0.95) + clouds(r, 420, "#2e3542", 6, 0.8) : time === "day" ? clouds(r, 160, "#ffffff", 5, 0.8) : ""}`);
    let far = skyline(r, 1120, [[-2400, 700, 300, "#6a7490"], [-1650, 500, 420, "#7a8498"], [-1100, 600, 260, "#6a7490"], [-450, 420, 520, "#5a6480"], [50, 700, 300, "#7a8498"], [800, 540, 360, "#6a7490"], [1400, 400, 680, "#5a6480"], [1850, 600, 300, "#7a8498"], [2500, 520, 440, "#6a7490"], [3050, 800, 320, "#7a8498"]], lit);
    far += `<g transform="translate(1600,440)"><path d="M-170,0V-260M170,0V-260M-170,-260H170M-170,-130H170M-170,0L170,-260M170,0L-170,-260" stroke="#3a3e48" stroke-width="10" fill="none"/><rect x="-190" y="-290" width="380" height="36" fill="#3a3e48"/></g>`;   // the billboard frame on the tall building
    far += `<path d="M-760,1120L-700,860L-640,1120ZM-700,860L-700,790" stroke="#c8a040" stroke-width="10" fill="#e8c860"/>`;   // a temple spire
    far += `<rect x="-2400" y="900" width="6200" height="260" fill="url(#${night ? "brFog" : "jkHazeW"})" opacity="${night ? 0.35 : 0.7}"/>`;
    put(L.far, far);
    let mid = `${house(-900, 760, 620, "#b8a890", { lit, roof: "#5a4a40" })}${house(-120, 480, 560, "#a8b8a0", { lit })}${shopFront(id, lit, time)}${house(1400, 560, 600, "#c8b8a8", { lit, plain: true })}${house(1960, 900, 520, "#a8a8b0", { lit })}
      ${cables(-1000, 1650, 400)}${cables(1650, 3000, 400, 3)}${pole(1650, 1180, `${id}-tf`, { lamp: true })}<rect x="-2400" y="1180" width="7600" height="900" fill="${night ? "#2a2c36" : "#7a7a78"}"/>`;
    put(L.mid, mid);
    let s = `<rect x="-2400" y="1250" width="7600" height="1400" fill="url(#${o.rain || o.puddle ? "ltWetConc" : "ltConc"})"/><path d="M-2400,1262H5200" stroke="#9a9a98" stroke-width="4" opacity=".5"/><path d="M-2400,1400H5200" stroke="#5a5a58" stroke-width="3" opacity=".4"/>
      ${[...Array(16)].map((_, k) => `<path d="M${-2300 + k * 480},1400V1900" stroke="#5a5a58" stroke-width="2" opacity=".25"/>`).join("")}<rect x="-2400" y="1560" width="7600" height="26" fill="#4a4a48" opacity=".6"/>${[...Array(30)].map((_, k) => `<rect x="${-2380 + k * 260}" y="1562" width="40" height="22" fill="#2a2a28" opacity=".7"/>`).join("")}
      ${o.puddle ? puddle(980, 1480, 220, 30) + puddle(1700, 1520, 120, 16) : ""}${o.rain ? puddle(300, 1500, 140, 18) + puddle(1300, 1540, 180, 20) : ""}
      ${cylinders(230)}${machine(420)}${workbench(id, o.gate !== false)}${o.table ? table(o.tableX ?? 1200, id) : ""}
      ${bike ? `<g id="${id}-bike" transform="translate(1450,1400)">${LT.BIKE}</g>` : ""}
      ${o.banana ? `<g id="${id}-tree" transform="translate(1850,1400)">${LT.TREE}</g>` : ""}
      <g transform="translate(90,1400)"><path d="M-40,0Q-50,-60 -30,-70H30Q50,-60 40,0Z" fill="#a85a3a"/>${[-20, 0, 20].map((dx) => `<path d="M${dx},-70q${dx},-40 ${dx * 1.5},-80" stroke="#4a8a3a" stroke-width="6" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-120,0)"><rect x="-60" y="0" width="120" height="1980" fill="#5a4a40"/><rect x="-60" y="0" width="30" height="1980" fill="#7a6a60"/></g>${cables(-200, 1400, -40, 2)}${o.rain ? RAIN(`${id}-rain`, 180, o.seed || 3) : ""}`);
    put(L.glow, `<g id="${id}-lamps" style="mix-blend-mode:screen" opacity="${lit ? 1 : 0}"><circle cx="1488" cy="590" r="300" fill="url(#ltLamp)"/><ellipse cx="880" cy="760" rx="520" ry="200" fill="url(#ltFluor)" opacity=".6"/>
        ${[-700, 120, 480].map((x) => `<circle cx="${x}" cy="620" r="150" fill="url(#ltWinGlow)" opacity=".6"/>`).join("")}</g>
      ${time === "day" ? `<g style="mix-blend-mode:screen"><path d="M300,-200H600L1300,1500H-100Z" fill="url(#jkRay)" opacity=".16" style="filter:blur(22px)"/></g>` : ""}
      ${time === "dusk" ? `<g style="mix-blend-mode:screen"><circle cx="-300" cy="700" r="700" fill="url(#jkWarm)" opacity=".35"/></g>` : ""}`);
  };

  // ---------------- the rooftop ----------------
  Sets.ltRoof = (L, o = {}) => {
    const id = o.id || "ltr", r = mk(o.seed || 9), storm = o.storm !== false;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${storm ? "#14181f" : "#4a8ad0"}"/><rect x="-3000" y="-1400" width="8000" height="2800" fill="url(#${storm ? "ltStorm" : "ltDay"})"/>
      <g id="${id}-clouds">${storm ? clouds(r, 60, "#161a22", 8, 0.95) + clouds(r, 300, "#262c38", 7, 0.85) + clouds(r, 520, "#3a4150", 6, 0.6) : clouds(r, 200, "#ffffff", 6, 0.8)}</g>`);
    let far = `<path d="M-2400,1120H3800V1300H-2400Z" fill="${storm ? "#3a4252" : "#9ab0c8"}"/>` + skyline(r, 1200, [[-2400, 500, 160, "#4a5262"], [-1850, 400, 240, "#525a6a"], [-1400, 600, 140, "#4a5262"], [-750, 300, 300, "#3e4656"], [-400, 700, 180, "#525a6a"], [350, 450, 260, "#4a5262"], [850, 650, 150, "#525a6a"], [1550, 350, 340, "#3e4656"], [1950, 800, 170, "#4a5262"], [2800, 600, 220, "#525a6a"], [3450, 400, 150, "#4a5262"]], storm, "ltWin");
    far += `<path d="M-2400,1300Q-1000,1270 400,1300T3800,1290V1420H-2400Z" fill="${storm ? "#2a3240" : "#7a9ab8"}"/><path d="M-2000,1330Q-1200,1310 -400,1330" stroke="#8aa0b8" stroke-width="3" opacity=".4" fill="none"/>`;   // the river
    far += `<path d="M700,1200L760,920L820,1200Z" fill="#3a3e48"/><path d="M760,920V860" stroke="#3a3e48" stroke-width="8"/>`;
    far += `<rect x="-2400" y="1000" width="6200" height="420" fill="url(#${storm ? "brFog" : "jkHazeW"})" opacity="${storm ? 0.3 : 0.6}"/>`;
    put(L.far, far);
    let mid = `<g transform="translate(-400,1400)"><rect x="-160" y="-520" width="320" height="300" rx="20" fill="#6a7080"/><rect x="-160" y="-520" width="320" height="300" rx="20" fill="url(#flV)"/><path d="M-120,-220V0M120,-220V0M-120,-110H120" stroke="#4a4e56" stroke-width="14"/><ellipse cy="-520" rx="160" ry="30" fill="#8a8f98"/></g>
      <g transform="translate(2250,1400)"><rect x="-240" y="-420" width="480" height="420" fill="#8a8a88"/><rect x="-240" y="-420" width="480" height="420" fill="url(#flV)" opacity=".6"/><rect x="-260" y="-440" width="520" height="24" fill="#6a6a68"/><rect x="-70" y="-300" width="140" height="300" fill="#3a3a44"/><rect x="100" y="-360" width="90" height="90" fill="#6a7080"/></g>
      ${[1900, 2050].map((x) => `<g transform="translate(${x},1400)"><rect x="-50" y="-110" width="100" height="110" rx="8" fill="#c8c8c4"/><circle cy="-55" r="34" fill="#6a6a68"/><circle cy="-55" r="26" fill="none" stroke="#3a3a40" stroke-width="4"/></g>`).join("")}
      <rect x="-2400" y="1400" width="7600" height="800" fill="#6e6e6c"/>`;
    put(L.mid, mid);
    // the giant billboard frame (set layer so the welder can work at its post)
    const frame = `<g id="${id}-frame" transform="translate(760,1400)">
      ${[0, 1100].map((x) => `<rect x="${x - 26}" y="-1120" width="52" height="1120" fill="url(#ltSteel)"/><rect x="${x - 60}" y="-24" width="120" height="24" fill="#4a4e56"/>`).join("")}
      <rect x="-40" y="-1140" width="1180" height="40" fill="url(#ltSteel)"/><rect x="-40" y="-760" width="1180" height="34" fill="url(#ltSteel)"/><rect x="-40" y="-400" width="1180" height="30" fill="url(#ltSteel)"/>
      ${[0, 1].map((k) => `<path d="M26,${-1100 + k * 360}L1074,${-760 + k * 360}M1074,${-1100 + k * 360}L26,${-760 + k * 360}" stroke="#6a6e76" stroke-width="14"/>`).join("")}
      <path d="M26,-400L1074,-24M1074,-400L26,-24" stroke="#6a6e76" stroke-width="14"/>
      <g id="${id}-panel"><rect x="60" y="-1100" width="700" height="320" fill="#e8e4dc" opacity=".92"/><rect x="60" y="-1100" width="700" height="320" fill="url(#flV)" opacity=".5"/>${T(410, -960, 90, "เร็วๆ นี้", { fill: "#c8c4bc", w: 900 })}<rect x="760" y="-1100" width="300" height="320" fill="none" stroke="#8a8f98" stroke-width="6" stroke-dasharray="20 14"/></g>
      <g id="${id}-joint"><rect x="-40" y="-80" width="80" height="60" fill="#5a5e66"/><path d="M-40,-50H40" stroke="#8a8f98" stroke-width="4"/></g>
      <path d="M-200,0L-120,-1120" stroke="#8a8f98" stroke-width="16"/><path d="M-230,0L-150,-1120" stroke="#8a8f98" stroke-width="16"/>${[...Array(14)].map((_, k) => `<path d="M${-200 + k * 5.7},${-40 - k * 78}h32" stroke="#8a8f98" stroke-width="10"/>`).join("")}</g>`;   // the ladder
    let s = `<rect x="-2400" y="1400" width="7600" height="1400" fill="url(#${storm ? "ltWetConc" : "ltConc"})"/>${[...Array(18)].map((_, k) => `<path d="M${-2300 + k * 420},1400V1900" stroke="#4a4a48" stroke-width="2" opacity=".3"/>`).join("")}<path d="M-2400,1620H5200" stroke="#4a4a48" stroke-width="3" opacity=".4"/>
      ${storm ? puddle(400, 1520, 200, 24, "#8a9aa8") + puddle(1500, 1560, 260, 30, "#8a9aa8") : ""}
      <path d="M-2400,1420Q-800,1410 600,1430T3800,1420" stroke="#5a5a58" stroke-width="6" fill="none" opacity=".6"/>${frame}
      <g transform="translate(300,1400)"><rect x="-30" y="-16" width="60" height="16" fill="#3a3a40"/><path d="M-26,-16V-70Q0,-90 26,-70V-16" fill="#8a6a30"/></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<rect x="-600" y="1760" width="2400" height="400" fill="#5a5a58"/><rect x="-600" y="1740" width="2400" height="30" fill="#7a7a78"/>${o.rain !== false && storm ? RAIN(`${id}-rain`, 220, o.seed || 5) : ""}`);
    put(L.glow, `<g id="${id}-sheet" style="mix-blend-mode:screen" opacity="0"><rect x="-3000" y="-3000" width="8000" height="8000" fill="#dff4ff"/></g>${storm ? `<g style="mix-blend-mode:screen"><ellipse cx="-800" cy="300" rx="900" ry="400" fill="url(#ltBlue)" opacity=".12"/></g>` : ""}`);
  };

  // ---------------- the hospital ward / the nursery ----------------
  const bed = (x, id, k) => `<g id="${id}-bed${k}" transform="translate(${x},1400)"><rect x="-290" y="-300" width="580" height="40" rx="8" fill="#d8dde4"/><rect x="-290" y="-260" width="580" height="24" fill="#b8c0c8"/>
    <rect x="-280" y="-236" width="560" height="60" rx="10" fill="#f4f6f8"/><rect x="-280" y="-200" width="560" height="26" fill="#7ab8d8"/><rect x="-270" y="-250" width="130" height="34" rx="12" fill="#ffffff"/>
    <rect x="-300" y="-430" width="600" height="18" rx="6" fill="#a8b0b8"/><path d="M-290,-412V-300M290,-412V-300M-290,-176V0M290,-176V0" stroke="#8a9098" stroke-width="14"/><circle cx="-290" cy="0" r="14" fill="#3a3a40"/><circle cx="290" cy="0" r="14" fill="#3a3a40"/>
    <path d="M-300,-176H300" stroke="#8a9098" stroke-width="10"/></g>`;
  const ecg = (x, id, blackout) => `<g id="${id}-ecg" transform="translate(${x},1400)"><rect x="-12" y="-700" width="24" height="700" fill="#8a9098"/><path d="M-100,0H100M-70,0V-30M70,0V-30" stroke="#8a9098" stroke-width="12"/>
    <rect x="-150" y="-900" width="300" height="220" rx="14" fill="#d8dde4"/><rect x="-136" y="-886" width="272" height="170" rx="8" fill="${blackout ? "#101418" : "#0b1e1a"}"/>
    <polyline id="${id}-ecgLine" points="-126,-800 -90,-800 -80,-820 -70,-770 -60,-800 -20,-800 -10,-830 2,-760 14,-800 60,-800 70,-820 80,-780 90,-800 126,-800" fill="none" stroke="#3aff9a" stroke-width="4" stroke-linejoin="round" opacity="${blackout ? 0 : 1}"/>
    <text x="-126" y="-730" font-family="Kanit" font-weight="800" font-size="24" fill="#3aff9a" opacity="${blackout ? 0 : 1}">72 bpm</text><circle cx="110" cy="-736" r="7" fill="#d8352a" opacity="${blackout ? 0.2 : 1}"/></g>`;
  const iv = (x) => `<g transform="translate(${x},1400)"><rect x="-6" y="-760" width="12" height="760" fill="#8a9098"/><path d="M-60,0H60M-40,0V-24M40,0V-24" stroke="#8a9098" stroke-width="10"/><path d="M-40,-760H40" stroke="#8a9098" stroke-width="8"/><rect x="20" y="-760" width="40" height="110" rx="8" fill="#cfe4f0" opacity=".9"/><path d="M40,-650Q60,-500 20,-420" stroke="#9ab8c8" stroke-width="3" fill="none"/></g>`;
  Sets.ltWard = (L, o = {}) => {
    const id = o.id || "ltw", night = !!o.night, bo = !!o.blackout, r = mk(o.seed || 13);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${bo ? "#0a0c12" : night ? "#9ab4b8" : "#dfe8e8"}"/>`);
    let far = `<rect x="-2400" y="-1400" width="6200" height="2600" fill="${bo ? "#12141c" : "#e4ecec"}"/><rect x="-2400" y="640" width="6200" height="14" fill="${bo ? "#1a1c24" : "#9ab8a8"}"/><rect x="-2400" y="1150" width="6200" height="50" fill="${bo ? "#0e1016" : "#c8d4d0"}"/>`;
    [[560, 0], [1500, 1]].forEach(([x]) => { far += `<g transform="translate(${x},760)"><rect x="-220" y="-380" width="440" height="380" fill="${night ? "url(#ltNight)" : "url(#ltGlassW)"}"/>${night && !bo ? stars(r, 10) : ""}${night ? `<path d="${[...Array(14)].map((_, k) => `M${-200 + k * 32},${-360 + (k % 3) * 60}l-6,40`).join("")}" stroke="#9ab8d8" stroke-width="3" opacity=".5"/>` : ""}
      <path d="M0,-380V0M-220,-190H220" stroke="#f4f4f4" stroke-width="12"/><rect x="-236" y="-396" width="472" height="412" fill="none" stroke="#f4f4f4" stroke-width="18"/><rect x="-260" y="-420" width="50" height="460" fill="#dcd4c8" opacity=".9"/><rect x="210" y="-420" width="50" height="460" fill="#dcd4c8" opacity=".9"/></g>`; });
    far += `<g transform="translate(1050,520)"><circle r="70" fill="#f4f4f4" stroke="#6a7078" stroke-width="8"/><path d="M0,0V-50M0,0L34,20" stroke="#2a2a30" stroke-width="6" stroke-linecap="round"/></g>
      <g transform="translate(1050,340)"><rect x="-240" y="-50" width="480" height="100" rx="12" fill="#2a6a9a"/>${T(0, 18, 44, o.nursery ? "ห้องเด็กอ่อน" : "หอผู้ป่วยรวม", { fill: "#ffffff", w: 900 })}</g>`;
    put(L.far, far);
    let mid = `<rect x="-2400" y="1200" width="6200" height="900" fill="${bo ? "#101218" : "#cfd8d8"}"/><rect x="-2400" y="560" width="6200" height="16" fill="#8a9098"/>`;
    if (!o.nursery) mid += [[-20, 0], [760, 1], [1420, 2], [2060, 3]].map(([x]) => `<g transform="translate(${x},576)"><path d="M-70,0Q-90,300 -60,620Q-30,640 0,620Q40,300 40,0Z" fill="${bo ? "#1c2228" : "#9ad0b0"}"/><path d="M-50,40Q-70,320 -40,600" stroke="${bo ? "#242a30" : "#7ab890"}" stroke-width="6" fill="none"/>${[...Array(5)].map((_, k) => `<circle cx="${-56 + k * 22}" cy="-2" r="7" fill="#8a9098"/>`).join("")}</g>`).join("");
    mid += iv(-80) + (o.nursery ? `<g transform="translate(1950,1200)"><rect x="-150" y="-620" width="300" height="620" rx="6" fill="${bo ? "#161a22" : "#a8c8c0"}"/><rect x="-130" y="-600" width="260" height="580" fill="${bo ? "#1a1e28" : "#cfe0dc"}"/><circle cx="100" cy="-300" r="12" fill="#c8a040"/>
      ${o.drawing ? `<g id="${id}-drawing" transform="translate(-10,-420) rotate(-4)"><rect x="-100" y="-130" width="200" height="260" fill="#fff8e8" stroke="#d8c8a8" stroke-width="3"/><path d="M-40,-80h80" stroke="#f6c060" stroke-width="12" stroke-linecap="round"/>
        <circle cy="-20" r="32" fill="#f8c8a8" stroke="#8a4a2a" stroke-width="4"/><path d="M-26,-50L-34,-100L-14,-70L-6,-110L4,-70L14,-110L22,-70L36,-100L26,-50" fill="#2a2a30" stroke="#2a2a30" stroke-width="3" stroke-linejoin="round"/><path d="M-14,-24v4M14,-24v4" stroke="#2a2a30" stroke-width="5" stroke-linecap="round"/><path d="M-12,-6q12,12 24,0" stroke="#8a4a2a" stroke-width="4" fill="none"/>
        <rect x="-36" y="12" width="72" height="80" fill="#3a6aa0"/><path d="M-36,30L-70,70M36,30L70,70M-20,92V140M20,92V140" stroke="#8a4a2a" stroke-width="10" stroke-linecap="round"/><path d="M60,-60L52,-30L68,-36L58,-6" stroke="#f6c060" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-60,-40L-54,-18L-70,-24L-62,0" stroke="#f6c060" stroke-width="7" fill="none" stroke-linecap="round"/>${T(0, 112, 22, "ขอบคุณค่ะ", { fill: "#d8352a", w: 800 })}</g>` : ""}</g>` : "");
    put(L.mid, mid);
    let s = `<rect x="-2400" y="1240" width="6200" height="1400" fill="${bo ? "#141820" : "#e8ecea"}"/>${[...Array(14)].map((_, k) => `<path d="M-2400,${1300 + k * 60}H3800" stroke="${bo ? "#1c2028" : "#d4dcda"}" stroke-width="3"/>`).join("")}<rect x="-2400" y="1240" width="6200" height="10" fill="${bo ? "#0e1016" : "#c0c8c8"}"/>`;
    if (!o.nursery) s += bed(420, id, 0) + bed(1080, id, 1) + bed(1740, id, 2) + ecg(1560, id, bo) + `<g transform="translate(240,1400)"><rect x="-60" y="-440" width="120" height="440" rx="8" fill="#d8dde4"/><rect x="-50" y="-430" width="100" height="120" fill="#c0c8d0"/><path d="M-30,-370h60" stroke="#3a3a40" stroke-width="4"/><circle cx="40" cy="-220" r="8" fill="#c8a040"/></g>`;
    else { s += [420, 900, 1380].map((x, k) => `<g id="${id}-inc${k}" transform="translate(${x},1250)">${LT.INC(`${id}-incg${k}`)}</g>`).join(""); s += `<g transform="translate(60,1400)"><rect x="-60" y="-420" width="120" height="420" rx="8" fill="#d8dde4"/><rect x="-50" y="-410" width="100" height="100" rx="4" fill="#c0c8d0"/></g>`; }
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-60,0)"><path d="M-120,500Q-60,1100 -80,1980H40Q10,1200 60,500Z" fill="${bo ? "#161c22" : "#8ac0a0"}"/></g>`);
    put(L.glow, `<g id="${id}-lights" style="mix-blend-mode:screen" opacity="${bo ? 0 : 1}">${[400, 1100, 1800].map((x) => `<ellipse cx="${x}" cy="700" rx="360" ry="220" fill="url(#ltFluor)" opacity=".5"/>`).join("")}</g>
      ${night && !bo ? `<g style="mix-blend-mode:screen"><circle cx="560" cy="600" r="320" fill="url(#ltBlue)" opacity=".15"/></g>` : ""}`);
  };

  // ---------------- the rental house corridor at night ----------------
  const DOOR = (x = 1000, id = "") => `<g transform="translate(${x},1200)"><rect x="-150" y="-660" width="300" height="660" fill="#5a4a40"/><rect x="-130" y="-640" width="260" height="640" fill="#1a1a26"/>
    <g${id ? ` id="${id}-leaf"` : ""}><rect x="-130" y="-640" width="260" height="640" fill="#7a6250"/><rect x="-130" y="-640" width="260" height="640" fill="url(#flV)" opacity=".6"/><rect x="-100" y="-600" width="200" height="240" fill="none" stroke="#5a4a40" stroke-width="8"/><rect x="-100" y="-320" width="200" height="280" fill="none" stroke="#5a4a40" stroke-width="8"/><circle cx="96" cy="-330" r="12" fill="#c8a040"/></g>
    <rect x="-60" y="-700" width="120" height="44" rx="6" fill="#2a3a7a"/>${T(0, -668, 30, "ห้อง 7", { fill: "#f4ecd8", w: 900 })}</g>`;
  Sets.ltRoom = (L, o = {}) => {
    const id = o.id || "ltm", bo = !!o.blackout;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#0a0c14"/>`);
    put(L.far, `<rect x="-2400" y="-1400" width="6200" height="2600" fill="#262a38"/><rect x="-2400" y="1140" width="6200" height="60" fill="#1a1c28"/>
      <g transform="translate(300,1200)"><rect x="-200" y="-700" width="400" height="700" fill="#161a26"/><rect x="-180" y="-680" width="360" height="300" fill="url(#ltNight)"/><path d="M0,-680V-380M-180,-530H180" stroke="#4a5068" stroke-width="8"/></g>`);
    let mid = `<rect x="-2400" y="-1400" width="6200" height="2600" fill="#3a3e4e"/><rect x="-2400" y="-1400" width="6200" height="2600" fill="url(#flV)" opacity=".5"/><rect x="-2400" y="760" width="6200" height="18" fill="#2a2e3a"/>${[...Array(20)].map((_, k) => `<path d="M${-2300 + k * 320},780V1200" stroke="#343848" stroke-width="2" opacity=".6"/>`).join("")}
      <rect x="-2400" y="1200" width="6200" height="900" fill="#2a2a36"/>${o.doorFront ? "" : DOOR(1000)}${DOOR(1900)}${DOOR(100)}
      <g id="${id}-bulb" transform="translate(1300,560)"><path d="M0,-560V0" stroke="#1a1a22" stroke-width="4"/><path d="M-14,0h28v30h-28z" fill="#8a8f98"/><ellipse class="ltBulbOn" cy="60" rx="34" ry="42" fill="${bo ? "#5a5a60" : "#fff2c0"}"/></g>
      ${cables(-600, 1560, 700, 2)}`;
    put(L.mid, mid);
    let s = `<rect x="-2400" y="1240" width="6200" height="1400" fill="#5a5a66"/>${[...Array(12)].map((_, k) => `<path d="M-2400,${1300 + k * 70}H3800" stroke="#4a4a56" stroke-width="3"/>`).join("")}${[...Array(20)].map((_, k) => `<path d="M${-2300 + k * 330},1240V2200" stroke="#4a4a56" stroke-width="3" opacity=".7"/>`).join("")}
      ${o.doorFront ? DOOR(1000, id) : ""}<g id="${id}-boxg" transform="translate(1560,1000)">${LT.FUSEBOX(`${id}-box`)}</g>
      <g transform="translate(1800,1400)"><rect x="-70" y="-110" width="140" height="110" rx="6" fill="#4a7a4a"/><path d="M-50,-110V-170M50,-110V-170M-60,-170H60" stroke="#3a5a3a" stroke-width="6"/>${[-30, 0, 30].map((dx) => `<path d="M${dx},-170q${dx / 2},-40 ${dx},-90" stroke="#4a9a3a" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <g transform="translate(560,1400)"><rect x="-90" y="-40" width="180" height="40" rx="6" fill="#8a6a40"/><rect x="-40" y="-60" width="80" height="20" fill="#3a3a44"/><rect x="40" y="-62" width="50" height="22" fill="#c8302a"/></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `<g transform="translate(-200,0)"><rect x="-40" y="1100" width="2000" height="22" fill="#2a2a36"/><rect x="-40" y="1100" width="2000" height="8" fill="#5a5a68"/>${[0, 400, 800].map((x) => `<rect x="${x}" y="1100" width="20" height="900" fill="#2a2a36"/>`).join("")}</g>`);
    put(L.glow, `<g id="${id}-lamps" style="mix-blend-mode:screen" opacity="${bo ? 0 : 1}"><circle cx="1300" cy="620" r="520" fill="url(#ltLamp)" opacity=".55"/></g>`);
  };

  // ---------------- the district from the alley mouth ----------------
  Sets.ltSky = (L, o = {}) => {
    const id = o.id || "ltk", r = mk(o.seed || 17), storm = o.storm !== false, lit = !o.blackout;
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="${storm ? "#0e1118" : "#06081a"}"/><rect x="-3000" y="-1400" width="8000" height="2700" fill="url(#${storm ? "ltStorm" : "ltNight"})"/>
      <g id="${id}-clouds">${storm ? clouds(r, 80, "#141820", 8, 0.95) + clouds(r, 320, "#222834", 7, 0.85) : stars(r, 60)}</g>`);
    let far = skyline(r, 1080, [[-2400, 600, 260, "#262c3a"], [-1750, 420, 420, "#2e3444"], [-1300, 700, 220, "#262c3a"], [-550, 380, 560, "#1e2432"], [-150, 650, 300, "#2e3444"], [550, 500, 240, "#262c3a"], [1100, 460, 700, "#1e2432"], [1600, 800, 340, "#2e3444"], [2450, 600, 260, "#262c3a"], [3100, 700, 440, "#2e3444"]], lit, "ltWin");
    far += `<g id="${id}-hosp" transform="translate(1100,380)"><rect x="40" y="-60" width="380" height="110" rx="10" fill="${lit ? "#f4f4f4" : "#3a3e48"}"/><path d="M90,-5h50M115,-30v50" stroke="${lit ? "#d8352a" : "#5a2a2a"}" stroke-width="14"/>${T(290, 10, 44, "โรงพยาบาล", { fill: lit ? "#d8352a" : "#5a2a2a", w: 900 })}</g>
      <g id="${id}-store" transform="translate(-450,680)"><rect x="-150" y="-60" width="300" height="100" rx="10" fill="${lit ? "#f28a2a" : "#4a3020"}"/>${T(0, 6, 36, "สะดวกซื้อ 24 ชม.", { fill: lit ? "#ffffff" : "#8a7a70", w: 900 })}</g>
      <g id="${id}-temple" transform="translate(2200,1080)"><path d="M-160,0L-120,-240L0,-420L120,-240L160,0Z" fill="${lit ? "#c8a040" : "#3a3220"}"/><path d="M0,-420V-520" stroke="${lit ? "#f6d36a" : "#5a4a30"}" stroke-width="8"/><rect x="-200" y="-40" width="400" height="40" fill="#2a2a30"/></g>
      <rect x="-2400" y="900" width="6200" height="260" fill="url(#brFog)" opacity=".25"/>`;
    put(L.far, far);
    let mid = `${house(-1300, 900, 500, "#4a4a56", { lit })}${house(-300, 700, 620, "#54505c", { lit })}${house(500, 600, 480, "#4a4a56", { lit, plain: true })}${house(2000, 1200, 560, "#54505c", { lit })}
      ${cables(-1000, 1500, 360)}${cables(1500, 3200, 360, 3)}${pole(1500, 1180, `${id}-tf`, { lamp: true })}<rect x="-2400" y="1180" width="7600" height="900" fill="#262a34"/>`;
    put(L.mid, mid);
    let s = `<rect x="-2400" y="1260" width="7600" height="1400" fill="url(#ltWetConc)"/><path d="M-2400,1270H5200" stroke="#6a6e78" stroke-width="4" opacity=".5"/>${[...Array(16)].map((_, k) => `<path d="M${-2300 + k * 480},1400V1900" stroke="#2a2e38" stroke-width="2" opacity=".5"/>`).join("")}
      <path d="M-2400,1700H5200" stroke="#d8d8d0" stroke-width="10" stroke-dasharray="120 80" opacity=".35"/>${puddle(900, 1500, 260, 34, "#6a8aa8")}${puddle(-200, 1560, 180, 24, "#6a8aa8")}${puddle(1900, 1620, 300, 30, "#6a8aa8")}
      <g transform="translate(-150,1400)"><rect x="-60" y="-120" width="120" height="120" rx="10" fill="#3a6a3a"/><rect x="-66" y="-130" width="132" height="16" rx="4" fill="#2a4a2a"/></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.fg, `${storm ? RAIN(`${id}-rain`, 240, o.seed || 7) : ""}`);
    put(L.glow, `<g id="${id}-lights" style="mix-blend-mode:screen" opacity="${lit ? 1 : 0}"><circle cx="1338" cy="590" r="300" fill="url(#ltLamp)"/>${[-1100, -600, 200, 1300, 2400].map((x) => `<circle cx="${x}" cy="760" r="220" fill="url(#ltWinGlow)" opacity=".45"/>`).join("")}<circle cx="1330" cy="380" r="300" fill="url(#ltFluor)" opacity=".4"/><circle cx="-450" cy="680" r="260" fill="url(#ltWarm)" opacity=".5"/></g>
      <g id="${id}-sheet" style="mix-blend-mode:screen" opacity="0"><rect x="-3000" y="-3000" width="8000" height="8000" fill="#dff4ff"/></g>`);
  };
})();
