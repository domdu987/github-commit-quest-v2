// Sets and props for "เอาชีวิตรอด 99 วัน" part 2 "ถนน" (EP.5–8): the four-lane highway at noon (side, first-person,
// top-down), the inside of ลุงหมาน's pickup, the shade under an overpass, a close-up for first aid on the ground,
// the abandoned petrol station with its guard on the canopy roof, and ปั้น's crayon drawing of the estate.
// Same layer contract as sets.js / fence.js (sky far mid set act fg + glow/light); load after fence.js.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const G = 1500;

  Sets.DEFS += `
    <linearGradient id="rAsph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6d7073"/><stop offset="1" stop-color="#55585b"/></linearGradient>
    <linearGradient id="rAsphD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3c3f"/><stop offset="1" stop-color="#2a2c2e"/></linearGradient>
    <linearGradient id="rHeat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c8" stop-opacity="0"/><stop offset=".5" stop-color="#fff2c8" stop-opacity=".55"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></linearGradient>
    <linearGradient id="rShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1c1f"/><stop offset="1" stop-color="#2e3134"/></linearGradient>
    <linearGradient id="rGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9fc0cc"/><stop offset=".55" stop-color="#6f8f9c"/><stop offset="1" stop-color="#4a6470"/></linearGradient>
    <linearGradient id="rFridge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f6ff"/><stop offset="1" stop-color="#9fd0ea"/></linearGradient>
    <radialGradient id="rGlare"><stop offset="0" stop-color="#fffbe6" stop-opacity=".95"/><stop offset=".25" stop-color="#fff0b8" stop-opacity=".45"/><stop offset="1" stop-color="#ffd37a" stop-opacity="0"/></radialGradient>`;

  const SKYG = { noon: "fNoon", day: "fDay", dusk: "fDusk", night: "fNight", morning: "fMorn" };
  const sky = (L, t) => put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#${SKYG[t] || "fNoon"})"/>`);
  const sun = (L, t, x = 760, y = 260) => {
    if (t === "night") put(L.sky, `<circle cx="${x}" cy="${y}" r="150" fill="url(#moonhalo)"/><circle cx="${x}" cy="${y}" r="46" fill="#e9eef5"/>`);
    else if (t === "dusk") put(L.sky, `<circle cx="${x}" cy="${y + 700}" r="460" fill="url(#fSun)"/><circle cx="${x}" cy="${y + 700}" r="120" fill="#ffd37a"/>`);
    else put(L.sky, `<circle cx="${x}" cy="${y}" r="520" fill="url(#rGlare)"/><circle cx="${x}" cy="${y}" r="70" fill="#fffbe6"/>`);
  };

  // ---------------- props ----------------
  // ลุงหมาน's pickup from the side, facing +x; origin = the ground under the middle of the wheelbase.
  // A steel stock cage on the bed (the farmer's คอก), faded blue paint with rust; wheels #id-w0 (rear) #id-w1 (front), each spinning group .spin
  function TRUCK(id, o = {}) {
    const c = o.col || "#7fa0ae", cS = "#5f7f8c";
    const wheel = (k, x) => `<g id="${id}-w${k}" transform="translate(${x},-62)"><circle r="64" fill="#1f1d1a" ${OUT}/><g class="spin"><circle r="34" fill="#8d9299" ${OUT}/>${[0, 72, 144, 216, 288].map((a) => `<path d="M0,0L${f1(Math.cos(a * Math.PI / 180) * 30)},${f1(Math.sin(a * Math.PI / 180) * 30)}" stroke="#5b6066" stroke-width="7"/>`).join("")}<circle r="9" fill="#5b6066"/></g></g>`;
    let s = `<g id="${id}">`;
    s += `<ellipse cx="0" cy="0" rx="420" ry="26" fill="#000" opacity=".22"/>`;
    // bed + cage (rear, -x)
    s += `<g id="${id}-bed"></g>`;   // riders in the bed go here (behind the side panel)
    s += `<path d="M-400,-80V-210H40V-80Z" fill="${c}" ${OUT}/><path d="M-400,-150H40" stroke="${cS}" stroke-width="5"/><path d="M-386,-200h30v100h-30z" fill="#c8392b" opacity=".85"/>`;
    s += `<g id="${id}-cage"><path d="M-396,-210V-360H30V-210" fill="none" stroke="#3f454b" stroke-width="10" stroke-linejoin="round"/>${[-330, -250, -170, -90, -10].map((x) => `<path d="M${x},-212V-360" stroke="#3f454b" stroke-width="6"/>`).join("")}<path d="M-396,-290H30" stroke="#3f454b" stroke-width="6"/></g>`;
    // cab (front, +x)
    s += `<path d="M40,-80V-300Q40,-330 70,-330H230Q262,-330 280,-300L330,-210H400Q420,-210 420,-190V-80Z" fill="${c}" ${OUT}/>`;
    s += `<path d="M70,-300H222L262,-216H70Z" fill="url(#rGlass)" ${OUT}/><path d="M150,-300V-216" stroke="${c}" stroke-width="12"/><path d="M90,-290l40,-0" stroke="#fff" stroke-width="5" opacity=".5"/>`;
    s += `<path d="M60,-190h40M170,-190h40" stroke="${cS}" stroke-width="6" stroke-linecap="round"/><rect x="390" y="-196" width="30" height="34" rx="6" fill="#fff6d8" ${OUT}/><rect x="-410" y="-196" width="22" height="40" rx="4" fill="#c8392b" ${OUT}/>`;
    s += `<path d="M-400,-80H420" stroke="#3a3f45" stroke-width="18"/>`;
    s += [[-120, -120, 26], [250, -110, 20], [-330, -120, 18]].map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 0.6}" fill="#8a4a1a" opacity=".55"/>`).join("");
    s += wheel(0, -250) + wheel(1, 280);
    s += `<g id="${id}-puff" opacity="0">${[0, 1, 2].map((k) => `<circle cx="${-440 - k * 40}" cy="${-70 - k * 18}" r="${22 + k * 10}" fill="#8a857a" opacity="${0.5 - k * 0.12}"/>`).join("")}</g>`;
    return s + `</g>`;
  }
  // the same pickup from behind (receding up the road): tailgate, cage, tail lights, two wheels; origin = ground centre
  function TRUCKR(id, o = {}) {
    const c = o.col || "#7fa0ae";
    let s = `<g id="${id}"><ellipse cx="0" cy="0" rx="230" ry="22" fill="#000" opacity=".25"/>`;
    s += `<rect x="-230" y="-110" width="70" height="110" rx="18" fill="#1f1d1a" ${OUT}/><rect x="160" y="-110" width="70" height="110" rx="18" fill="#1f1d1a" ${OUT}/>`;
    s += `<path d="M-210,-300Q-210,-470 -120,-470H120Q210,-470 210,-300Z" fill="${c}" ${OUT}/><path d="M-150,-440H150L180,-330H-180Z" fill="url(#rGlass)" ${OUT}/>`;
    s += `<g id="${id}-bed"></g>`;   // riders in the bed go here (behind the tailgate)
    s += `<rect x="-230" y="-300" width="460" height="200" rx="10" fill="${c}" ${OUT}/><rect x="-200" y="-270" width="400" height="120" rx="8" fill="#6f8f9c" opacity=".35"/>`;
    s += `<rect x="-226" y="-292" width="30" height="70" rx="6" fill="#c8392b" ${OUT}/><rect x="196" y="-292" width="30" height="70" rx="6" fill="#c8392b" ${OUT}/><rect x="-70" y="-150" width="140" height="34" rx="4" fill="#f4ecd8" ${OUT}/><text x="0" y="-124" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="${INK}">บพ 4521</text>`;
    s += `<path d="M-226,-300V-470M226,-300V-470M-226,-470H226M-226,-385H226" fill="none" stroke="#3f454b" stroke-width="10"/>${[-150, -75, 0, 75, 150].map((x) => `<path d="M${x},-300V-470" stroke="#3f454b" stroke-width="6"/>`).join("")}`;
    s += `<rect x="-240" y="-108" width="480" height="20" fill="#3a3f45"/>`;
    return s + `</g>`;
  }
  // an abandoned car from the side (facing +x unless flip): sedan or van, doors open, a window smashed, a flat tyre
  function CAR(x, y, s, col, o = {}) {
    const fl = o.flip ? -1 : 1, van = o.van;
    let g = `<g transform="translate(${x},${y}) scale(${fl * s},${s})"><ellipse cx="0" cy="0" rx="330" ry="22" fill="#000" opacity=".2"/>`;
    g += van ? `<path d="M-320,-70V-290Q-320,-320 -290,-320H210Q250,-320 280,-270L320,-190V-70Z" fill="${col}" ${OUT}/><path d="M-290,-296H120V-200H-290Z" fill="url(#rGlass)" ${OUT}/><path d="M140,-296H200Q232,-296 252,-262L286,-200H140Z" fill="url(#rGlass)" ${OUT}/>`
      : `<path d="M-320,-70V-160Q-320,-180 -290,-186L-200,-196L-120,-270Q-100,-286 -70,-286H110Q140,-286 160,-266L230,-196L300,-180Q320,-176 320,-150V-70Z" fill="${col}" ${OUT}/><path d="M-176,-200L-110,-262H10V-200Z" fill="url(#rGlass)" ${OUT}/><path d="M30,-262H100Q124,-262 140,-246L190,-200H30Z" fill="url(#rGlass)" ${OUT}/>`;
    if (o.smash) g += `<path d="M-150,-230l30,-14l10,20l24,-8M-130,-210l18,-24" stroke="#f4ecd8" stroke-width="3" fill="none"/>`;
    if (o.door) g += `<path d="M30,-200L-30,-120L-20,-70L40,-90Z" fill="${col}" ${OUT} opacity=".95"/>`;
    g += `<path d="M-320,-70H320" stroke="#3a3f45" stroke-width="14"/><rect x="290" y="-150" width="26" height="24" rx="5" fill="#f4ecd8" ${OUT}/><rect x="-318" y="-150" width="18" height="26" rx="4" fill="#c8392b" ${OUT}/>`;
    g += [-200, 210].map((wx, k) => `<g transform="translate(${wx},${k === 0 && o.flat ? -40 : -52})"><ellipse rx="54" ry="${k === 0 && o.flat ? 40 : 54}" fill="#1f1d1a" ${OUT}/><circle r="22" fill="#8d9299" ${OUT}/></g>`).join("");
    g += `<ellipse cx="-60" cy="-120" rx="40" ry="16" fill="#8a4a1a" opacity=".4"/><path d="M-300,-176q200,-20 560,-8" stroke="#fff" stroke-width="4" opacity=".3" fill="none"/>`;
    return g + `</g>`;
  }
  // a car from above (for the top-down shot): body, windscreen, roof; a = rotation in degrees
  const CARTOP = (x, y, a, col, w = 190, h = 420) => `<g transform="translate(${x},${y}) rotate(${a})"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="40" fill="${col}" ${OUT}/><rect x="${-w / 2 + 18}" y="${-h / 2 + 70}" width="${w - 36}" height="70" rx="14" fill="url(#rGlass)" ${OUT}/><rect x="${-w / 2 + 22}" y="${-h / 2 + 150}" width="${w - 44}" height="${h * 0.34}" rx="16" fill="${col}" opacity=".8" stroke="${INK}" stroke-width="3"/><rect x="${-w / 2 + 18}" y="${h / 2 - 90}" width="${w - 36}" height="56" rx="12" fill="url(#rGlass)" ${OUT}/></g>`;
  // a straw hat (ลุงหมาน's) — hung on a post or lying on the ground
  const HAT = (id, x, y, s = 1, rot = 0) => `<g id="${id}" transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><ellipse cx="0" cy="0" rx="86" ry="16" fill="#c9a55a" ${OUT}/><path d="M-44,-2Q-40,-50 2,-52Q44,-50 48,-2Z" fill="#d9b86a" ${OUT}/><path d="M-44,-10H48" stroke="#8a6a2a" stroke-width="7"/></g>`;
  // a clear plastic water bottle: level 0..1 (#id-water inside); origin = bottle centre, ~70 × 230
  const BOTTLE = (id, level = 0.6, cap = "#2f6fb8") => `<g id="${id}"><rect x="-36" y="-96" width="72" height="196" rx="22" fill="#dfeff5" fill-opacity=".55" ${OUT}/><rect id="${id}-water" x="-30" y="${f1(-90 + 184 * (1 - level))}" width="60" height="${f1(184 * level)}" rx="16" fill="#6fb3d6" opacity=".75"/><rect x="-20" y="-124" width="40" height="30" rx="6" fill="${cap}" ${OUT}/><path d="M-36,-40H36M-36,30H36" stroke="#9fc0cc" stroke-width="4"/><path d="M-20,-80v120" stroke="#fff" stroke-width="7" opacity=".55" stroke-linecap="round"/></g>`;
  window.Road = { TRUCK, TRUCKR, CAR, CARTOP, HAT, BOTTLE };

  // heat shimmer bands (class "shim" drift in flife) and a hot haze at the horizon
  const shimmer = (L, y0, y1, n = 12, op = 0.16) => {
    put(L.glow, `<g class="rshim">${Array.from({ length: n }, (_, k) => { const y = y0 + (y1 - y0) * k / (n - 1); return `<path d="M-1300,${f1(y)}q150,9 300,0t300,0t300,0t300,0t300,0t300,0t300,0t300,0t300,0t300,0t300,0t300,0" stroke="#fff6dc" stroke-width="3" fill="none" opacity="${op}"/>`; }).join("")}</g>`);
    put(L.glow, `<rect x="-1300" y="${y0 - 60}" width="3800" height="${y1 - y0 + 120}" fill="url(#rHeat)" opacity=".7"/>`);
  };

  // ---------------- the highway from the side: far carriageway beyond the median barrier, the near one we walk on ----------------
  // opts: time (noon/dusk), cars [[x, y, s, col, {flip, van, smash, door, flat}]] near lane, farCars, sign (overhead "ปั๊ม 4 กม."), billboard, bridge
  function highway(L, o = {}) {
    const id = o.id || "hw", t = o.time || "noon", r = mk(o.seed || 91), dusk = t === "dusk";
    sky(L, t); sun(L, t, o.sunX ?? 760, o.sunY ?? 230);
    put(L.far, Fence.paddies(r, t === "noon" ? "day" : t, 1000));
    // mid (parallax): the far carriageway, its cars, the median barrier, power poles, the overhead sign
    let m = `<rect x="-1400" y="1040" width="4000" height="120" fill="url(#rAsph)"/><path d="M-1400,1098H2600" stroke="#f4ecd8" stroke-width="6" stroke-dasharray="70 60" opacity=".7"/>`;
    m += (o.farCars || [[-700, 1150, 0.45, "#c8c2b4"], [400, 1150, 0.42, "#8a3a2e", { flip: true }], [1500, 1150, 0.45, "#e8e2d4", { van: true }]]).map(([x, y, s, col, oo]) => CAR(x, y, s, col, oo || {})).join("");
    m += `<path d="M-1400,1160H2600V1230H-1400Z" fill="#cfc9bb" ${OUT}/><path d="M-1400,1172H2600" stroke="#e8e2d4" stroke-width="6"/>${Array.from({ length: 24 }, (_, k) => `<path d="M${-1400 + k * 180},1160v70" stroke="#a9a397" stroke-width="3"/>`).join("")}`;
    for (let k = 0; k < 6; k++) { const x = -1100 + k * 700; m += `<path d="M${x},1170V820M${x - 46},850H${x + 46}" stroke="${dusk ? "#3a3044" : "#6b5a44"}" stroke-width="9" fill="none"/>`; }
    m += `<path d="M-1100,850Q-750,880 -400,850T300,850T1000,850T1700,850T2400,850" stroke="#5a4a34" stroke-width="2.5" fill="none" opacity=".7"/>`;
    if (o.billboard !== false) m += `<g transform="translate(${o.billboardX ?? 1500},1160)"><path d="M-10,0V-300M110,0V-300" stroke="#5b6066" stroke-width="14"/><rect x="-160" y="-520" width="420" height="230" fill="#e8e2d4" ${OUT}/><rect x="-140" y="-500" width="380" height="110" fill="#c8392b" opacity=".55"/><text x="50" y="-420" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="#f4ecd8" stroke="${INK}" stroke-width="5" paint-order="stroke">ที่ดินขาย</text><path d="M-150,-330h400" stroke="#9f9a8e" stroke-width="6"/><path d="M40,-520l30,90l-20,70" stroke="#8a857a" stroke-width="4" fill="none"/></g>`;
    if (o.sign) m += `<g id="${id}-sign" transform="translate(${o.signX ?? 300},1230)"><path d="M-360,0V-560M360,0V-560M-360,-540H360" stroke="#8d9299" stroke-width="16" fill="none"/><rect x="-300" y="-700" width="600" height="190" rx="14" fill="#1f6b46" ${OUT}/><rect x="-286" y="-686" width="572" height="162" rx="10" fill="none" stroke="#f4ecd8" stroke-width="5"/>
      <text x="-30" y="-618" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#f4ecd8">ปั๊มน้ำมัน</text><text x="-30" y="-550" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="46" fill="#f4ecd8">${o.sign} กม.</text>
      <g transform="translate(200,-606)"><rect x="-34" y="-50" width="60" height="100" rx="8" fill="#f4ecd8"/><rect x="-24" y="-38" width="40" height="30" fill="#1f6b46"/><path d="M26,-20q26,0 26,30v30" stroke="#f4ecd8" stroke-width="10" fill="none"/></g></g>`;
    put(L.mid, m);
    // set: the near carriageway we walk on (actors at y 1500), lane marks, cracks, our side's cars
    let s = `<rect x="-1400" y="1230" width="4000" height="1500" fill="url(#rAsph)"/><path d="M-1400,1250H2600" stroke="#e8b830" stroke-width="8"/><path d="M-1400,1660H2600" stroke="#f4ecd8" stroke-width="10" stroke-dasharray="120 90"/><path d="M-1400,2060H2600" stroke="#f4ecd8" stroke-width="10"/>`;
    for (let k = 0; k < 18; k++) { const x = -1300 + r() * 3800, y = 1300 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}l${f1(30 + r() * 40)},${f1(6 - r() * 12)}l${f1(20 + r() * 30)},${f1(10 - r() * 20)}" stroke="#4a4d50" stroke-width="3" fill="none"/>`; }
    s += `<path d="M-900,1560q400,-14 900,0" stroke="#3a3c3f" stroke-width="22" fill="none" opacity=".35"/><path d="M200,1780q500,10 1100,-6" stroke="#3a3c3f" stroke-width="22" fill="none" opacity=".3"/>`;
    s += (o.cars || [[-700, 1420, 1.42, "#e8e2d4", { smash: true }], [1600, 1430, 1.45, "#3f5a8a", { door: true, flat: true }]]).map(([x, y, sc, col, oo]) => CAR(x, y, sc, col, oo || {})).join("");
    if (o.bridge) s += `<g>${Array.from({ length: 40 }, (_, k) => `<rect x="${-1400 + k * 100}" y="1990" width="40" height="120" fill="#cfc9bb" ${OUT}/>`).join("")}<rect x="-1400" y="1960" width="4000" height="40" fill="#e8e2d4" ${OUT}/></g>`;
    put(L.set, s);
    if (o.truck) put(L.set, `<g transform="translate(${o.truck.x},${o.truck.y ?? 1520}) scale(${o.truck.flip ? -(o.truck.s ?? 0.9) : (o.truck.s ?? 0.9)},${o.truck.s ?? 0.9})">${TRUCK(`${id}-truck`, o.truck)}</g>`);
    if (t === "noon") shimmer(L, 1040, 1250, 10, 0.18);
    if (dusk) put(L.glow, `<rect x="-1300" y="700" width="3800" height="1400" fill="#ff9a3c" opacity=".12"/>`);
  }

  // ---------------- first person down the highway: lanes converging to a vanishing point, a mirage on the asphalt ----------------
  // opts: vx/vy (vanishing point), cars [[depth 0..1, lane -2..2, col]], overpass (a bridge across the horizon), bridge (railings both sides), time
  function highwayPov(L, o = {}) {
    const id = o.id || "hp", t = o.time || "noon", r = mk(o.seed || 17), VX = o.vx ?? 540, VY = o.vy ?? 1000;
    sky(L, t); sun(L, t, o.sunX ?? 700, o.sunY ?? 330);
    put(L.far, Fence.paddies(r, t === "noon" ? "day" : t, VY));
    const P = (d, lane) => { const k = 1 / (1 + d * 9); return [VX + lane * 760 * k, VY + (2300 - VY) * k, k]; };   // depth d: 0 = at our feet, 1 = far; lane in half-widths
    let s = `<path d="M${VX - 6},${VY}L${VX + 6},${VY}L${VX + 2600},2700L${VX - 2600},2700Z" fill="url(#rAsph)"/>`;
    s += `<path d="M${VX - 4},${VY}L${VX - 1300},2700M${VX + 4},${VY}L${VX + 1300},2700" stroke="#e8e2d4" stroke-width="8" fill="none"/>`;
    for (let k = 0; k < 14; k++) { const d0 = k / 14, d1 = d0 + 0.035, [x0, y0] = P(d0 ** 1.0, 0), [x1, y1] = P(d1, 0); s += `<path d="M${f1(x0)},${f1(y0)}L${f1(x1)},${f1(y1)}" stroke="#f4ecd8" stroke-width="${f1(22 * P(d0, 0)[2])}" fill="none"/>`; }
    // the median barrier running away on the left, the far carriageway beyond it
    s += `<path d="M${VX - 20},${VY}L${VX - 1900},2700L${VX - 2600},2700L${VX - 30},${VY}Z" fill="#cfc9bb" ${OUT}/><path d="M${VX - 30},${VY}L${VX - 2600},2700V${VY}Z" fill="url(#rAsphD)" opacity=".35"/>`;
    if (o.bridge) s += `<path d="M${VX + 10},${VY - 4}L${VX + 2000},2300M${VX + 10},${VY - 24}L${VX + 2000},2050" stroke="#e8e2d4" stroke-width="18" fill="none"/>${Array.from({ length: 16 }, (_, k) => { const [x, y, kk] = P(k / 16, 2.3); return `<rect x="${f1(x)}" y="${f1(y - 320 * kk)}" width="${f1(40 * kk)}" height="${f1(320 * kk)}" fill="#cfc9bb" stroke="${INK}" stroke-width="2"/>`; }).join("")}`;
    put(L.set, s);
    // cars at depth, smaller and paler with distance; an overpass across the horizon
    let c = "";
    if (o.overpass !== false) c += `<g opacity=".85"><rect x="-1300" y="${VY - 120}" width="3800" height="60" fill="#b3ada0" ${OUT}/>${[-300, 300, 900, 1500].map((x) => `<rect x="${x}" y="${VY - 60}" width="40" height="62" fill="#9f9a8e"/>`).join("")}</g>`;
    (o.cars || [[0.12, -1.2, "#e8e2d4"], [0.3, 0.9, "#3f5a8a"], [0.55, -0.4, "#8a3a2e"], [0.8, 0.6, "#c8c2b4"]]).forEach(([d, lane, col]) => { const [x, y, k] = P(d, lane); c += `<g opacity="${f1(0.55 + 0.45 * (1 - d))}">${CAR(x, y, 1.5 * k, col, { flip: lane < 0 })}</g>`; });
    put(L.set, c);
    // the mirage: a bright, wobbling band just short of the horizon
    put(L.glow, `<g class="rshim"><ellipse cx="${VX}" cy="${VY + 40}" rx="900" ry="30" fill="#e8f2f6" opacity=".55"/><ellipse cx="${VX}" cy="${VY + 60}" rx="600" ry="18" fill="#fff" opacity=".35"/></g>`);
    shimmer(L, VY - 30, VY + 200, 9, 0.2);
  }

  // ---------------- the highway from above: two carriageways, the median, cars at angles, the overpass shadow ----------------
  // the pickup (#id-truck, pointing up) drives up the page between the cars; figures from above (#id-z0..) are the slow dead
  function highwayTop(L, o = {}) {
    const id = o.id || "ht", r = mk(o.seed || 33);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#8fae5a"/>`);
    let s = `${Array.from({ length: 14 }, (_, k) => `<path d="M-1200,${-700 + k * 260}H2300" stroke="#6d8f3e" stroke-width="6" opacity=".6"/>`).join("")}`;
    s += `<rect x="-300" y="-800" width="560" height="3600" fill="url(#rAsph)"/><rect x="320" y="-800" width="560" height="3600" fill="url(#rAsph)"/><rect x="260" y="-800" width="60" height="3600" fill="#cfc9bb" ${OUT}/>`;
    s += `<path d="M-20,-800V2800M600,-800V2800" stroke="#f4ecd8" stroke-width="10" stroke-dasharray="110 90"/><path d="M-290,-800V2800M870,-800V2800" stroke="#f4ecd8" stroke-width="8"/><path d="M250,-800V2800M330,-800V2800" stroke="#e8b830" stroke-width="7"/>`;
    s += `<rect x="-1200" y="${o.bridgeY ?? 200}" width="3500" height="230" fill="#b3ada0" ${OUT}/><rect x="-1200" y="${(o.bridgeY ?? 200) + 230}" width="3500" height="120" fill="#000" opacity=".25"/>`;
    put(L.set, s);
    put(L.set, (o.cars || [[-250, 1500, 8, "#e8e2d4"], [460, 640, 186, "#c8c2b4"], [730, 1000, 172, "#e8b830"], [480, 1380, 196, "#2f6fb8"], [760, 1760, 168, "#8a3a2e"], [470, 2160, 182, "#3f5a8a"], [740, 2520, 190, "#e8e2d4"]]).map(([x, y, a, col]) => CARTOP(x, y, a, col)).join(""));
    const fig = (x, y, top, skin, hair) => `<g transform="translate(${x},${y}) scale(0.42)"><ellipse rx="56" ry="30" fill="${top}" ${OUT}/><path d="M-44,-10L-90,60M44,-10L90,60" stroke="${INK}" stroke-width="28" stroke-linecap="round"/><path d="M-44,-10L-90,60M44,-10L90,60" stroke="${skin}" stroke-width="20" stroke-linecap="round"/><circle r="27" fill="${hair}" ${OUT}/></g>`;
    put(L.act, (o.dead || [[-262, 1180, "#2c3e6b"], [610, 1190, "#e6e8e2"], [620, 1580, "#4f6a7a"], [600, 1990, "#2c3e6b"], [-270, 2050, "#e6e8e2"], [880, 1400, "#4f6a7a"]]).map(([x, y, top], k) => `<g id="${id}-z${k}">${fig(x, y, top, "#a3ae8e", "#3a3330")}</g>`).join(""));
    // the pickup from above: cab ahead (up), cage over the bed, ปั้น a dot of red in the back
    put(L.act, `<g id="${id}-truck" transform="translate(${o.truckX ?? 20},${o.truckY ?? 2400})"><g id="${id}-truckr"><rect x="-110" y="-260" width="220" height="520" rx="40" fill="#7fa0ae" ${OUT}/><rect x="-92" y="-230" width="184" height="80" rx="16" fill="url(#rGlass)" ${OUT}/><rect x="-96" y="-140" width="192" height="90" rx="12" fill="#6f8f9c" ${OUT}/>
      <rect x="-100" y="-30" width="200" height="270" fill="#5f7f8c" ${OUT}/>${[0, 1, 2, 3].map((k) => `<path d="M-100,${10 + k * 60}H100" stroke="#3f454b" stroke-width="6"/>`).join("")}<circle cx="-40" cy="120" r="24" fill="#8e2a2a" ${OUT}/><circle cx="40" cy="60" r="26" fill="#b8463a" ${OUT}/><circle cx="20" cy="180" r="26" fill="#d96a8a" ${OUT}/></g></g>`);
    put(L.glow, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#fff2c8" opacity=".12"/>`);
  }

  // ---------------- inside the pickup's cab (first person from the driver's seat) ----------------
  // the windscreen shows the highway (highwayPov drawn behind); dashboard with the fuel gauge (#id-needle, rotate about its pivot),
  // the warning lamp (#id-warn), the steering wheel with ครูพิม's two hands (#id-wheel rotates a little), the rear-view mirror
  function cab(L, o = {}) {
    const id = o.id || "cb";
    highwayPov(L, { ...o, id: `${id}-v`, vy: 900, vx: 600, sunY: 260, cars: o.cars || [[0.12, -2.3, "#e8e2d4"], [0.35, -1.7, "#3f5a8a"], [0.6, 2.3, "#8a3a2e"], [0.85, -1.5, "#c8c2b4"]] });
    // the cab frame and dashboard in the fg layer (sharp, near)
    let f = `<path d="M-1300,-900H2400V2900H-1300ZM-60,150Q540,90 1160,150L1240,1180H-140Z" fill="#2a2c2e" fill-rule="evenodd"/>`;
    f += `<path d="M-60,150Q540,90 1160,150" stroke="#3f454b" stroke-width="24" fill="none"/><path d="M-60,150L-140,1180M1160,150L1240,1180" stroke="#3f454b" stroke-width="40" fill="none"/>`;
    f += `<rect x="460" y="170" width="200" height="70" rx="14" fill="#1f1d1a" ${OUT}/><rect x="470" y="178" width="180" height="54" rx="10" fill="url(#rGlass)" opacity=".8"/>`;
    f += `<path d="M-300,1150Q540,1060 1400,1150V2600H-300Z" fill="#3a3632" ${OUT}/><path d="M-300,1150Q540,1060 1400,1150" stroke="#55504a" stroke-width="10" fill="none"/>`;
    // the gauge cluster: a fuel dial E–F
    f += `<g transform="translate(300,1330)"><circle r="120" fill="#141210" ${OUT}/><path d="M-90,30A95,95 0 0 1 90,30" stroke="#f4ecd8" stroke-width="6" fill="none"/>${[-60, -30, 0, 30, 60].map((a) => `<path d="M${f1(Math.sin(a * Math.PI / 180) * 80)},${f1(-Math.cos(a * Math.PI / 180) * 80 + 30)}L${f1(Math.sin(a * Math.PI / 180) * 96)},${f1(-Math.cos(a * Math.PI / 180) * 96 + 30)}" stroke="#f4ecd8" stroke-width="5"/>`).join("")}
      <text x="-92" y="70" font-family="Kanit" font-weight="900" font-size="34" fill="#ff6a4a">E</text><text x="70" y="70" font-family="Kanit" font-weight="900" font-size="34" fill="#f4ecd8">F</text>
      <g id="${id}-needle" transform="translate(0,30) rotate(${o.fuel ?? -40})"><path d="M0,6L-5,0L0,-88L5,0Z" fill="#ff5a3a" stroke="${INK}" stroke-width="2"/></g><circle cy="30" r="12" fill="#5b6066"/>
      <g id="${id}-warn" opacity="0.15"><rect x="-26" y="-70" width="52" height="40" rx="6" fill="#ffb020"/><rect x="-14" y="-62" width="20" height="26" fill="#141210"/><path d="M8,-56q10,0 10,12v10" stroke="#141210" stroke-width="5" fill="none"/></g></g>`;
    f += `<g transform="translate(760,1330)"><circle r="110" fill="#141210" ${OUT}/>${Array.from({ length: 9 }, (_, k) => { const a = (-120 + k * 30) * Math.PI / 180; return `<path d="M${f1(Math.sin(a) * 76)},${f1(-Math.cos(a) * 76)}L${f1(Math.sin(a) * 92)},${f1(-Math.cos(a) * 92)}" stroke="#f4ecd8" stroke-width="5"/>`; }).join("")}<g id="${id}-speed" transform="rotate(${o.speed ?? -40})"><path d="M0,6L-5,0L0,-86L5,0Z" fill="#ff5a3a" stroke="${INK}" stroke-width="2"/></g><circle r="10" fill="#5b6066"/></g>`;
    put(L.fg, f);
    // the wheel with two hands (rotates about its hub)
    const PIM = Rig.CAST.pim;
    put(L.fg, `<g id="${id}-wheel" transform="translate(520,1560)"><circle r="380" fill="none" stroke="#1b1a18" stroke-width="64"/><circle r="380" fill="none" stroke="#3a3632" stroke-width="40"/><path d="M-360,40L-90,60M360,40L90,60M0,90V360" stroke="#1b1a18" stroke-width="56" fill="none"/><circle r="100" fill="#2a2724" ${OUT}/>
      <g transform="translate(-330,-170) rotate(-30) scale(0.7)">${Hand.grip({ skin: PIM.skin, sleeve: PIM.sleeve })}</g><g transform="translate(330,-170) rotate(30) scale(-0.7,0.7)">${Hand.grip({ skin: PIM.skin, sleeve: PIM.sleeve })}</g></g>`);
    L.fg.classList.remove("fgblur");
  }

  // ---------------- the shade under an overpass: the concrete deck overhead, pillars, the white-hot road beyond ----------------
  // ids: #id-car (a car parked in the shade), #id-under (the dark gap under it — the dead crawl out of it)
  function underpass(L, o = {}) {
    const id = o.id || "up", r = mk(o.seed || 47);
    sky(L, "noon");
    put(L.far, Fence.paddies(r, "day", 1060));
    // the sunlit world beyond the shade: bleached
    put(L.mid, `<rect x="-1400" y="1080" width="4000" height="200" fill="url(#rAsph)"/><rect x="-1400" y="-800" width="4000" height="2100" fill="#fffbe6" opacity=".35"/>`);
    // the deck overhead (a dark slab with beams), two fat pillars, the ground in shadow
    let s = `<rect x="-1400" y="-900" width="4000" height="1260" fill="url(#rShade)"/>${Array.from({ length: 12 }, (_, k) => `<rect x="${-1400 + k * 360}" y="-900" width="60" height="1260" fill="#24272a"/>`).join("")}<rect x="-1400" y="300" width="4000" height="70" fill="#3a3d40" ${OUT}/>`;
    s += `<path d="M-1400,370H2600" stroke="#5b6066" stroke-width="6"/>`;
    s += (o.pillars || [40, 1180]).map((x) => `<g><rect x="${x - 110}" y="370" width="220" height="1160" fill="#5a5d60" ${OUT}/><rect x="${x - 110}" y="370" width="60" height="1160" fill="#46494c"/><path d="M${x - 80},700l40,30l-10,40M${x + 40},1100l30,-20" stroke="#3a3d40" stroke-width="4" fill="none"/></g>`).join("");
    s += `<rect x="-1400" y="1280" width="4000" height="1500" fill="#3c3f42"/><path d="M-1400,1280H2600" stroke="#2a2c2e" stroke-width="8"/>`;
    for (let k = 0; k < 14; k++) { const x = -1200 + r() * 3400, y = 1330 + r() * 700; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(20 + r() * 40)}" ry="${f1(5 + r() * 8)}" fill="#2a2c2e" opacity=".6"/>`; }
    s += `<path d="M700,1320q60,-20 120,6l40,-10" stroke="#8a857a" stroke-width="5" fill="none"/><rect x="980" y="1330" width="70" height="40" rx="6" fill="#b3ada0" ${OUT}/>`;
    put(L.set, s);
    if (o.car !== false) put(L.set, `<g id="${id}-car">${CAR(o.carX ?? 1250, 1440, 1.45, "#8a3a2e", { smash: true, flat: true, flip: true })}<ellipse id="${id}-under" cx="${o.carX ?? 1250}" cy="1430" rx="470" ry="34" fill="#0d0e0f" opacity=".75"/></g>`);
    // light: the bright opening beyond the shade, a hard edge on the ground where the sun starts
    put(L.glow, `<rect x="-1400" y="1240" width="4000" height="50" fill="#fff6d8" opacity=".25"/><rect x="-1400" y="-900" width="4000" height="1300" fill="#000" opacity=".3"/><rect x="-1400" y="1290" width="4000" height="1500" fill="#000" opacity=".18"/>`);
    put(L.fg, `<rect x="-1400" y="2050" width="4000" height="900" fill="#fff2c8" opacity=".12"/>`);
  }

  // ---------------- first aid on the ground, close-up from above: a body lying in the shade, cloths, a bottle pouring ----------------
  // the rig of the patient is placed by the shot (act layer); this set gives the ground, the shade edge and the props:
  // #id-cl0..3 (wet cloths, hidden), #id-pour (a bottle tilted, hidden) with #id-stream, #id-fan (a flap of cardboard, hidden)
  function aidClose(L, o = {}) {
    const id = o.id || "ac", r = mk(o.seed || 23);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#3c3f42"/>`);
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="#46494c"/>`;
    for (let k = 0; k < 40; k++) { const x = -900 + r() * 2900, y = -500 + r() * 2900; s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(2 + r() * 5)}" fill="#3a3d40"/>`; }
    s += `<path d="M-1200,${o.edge ?? 1800}L2300,${(o.edge ?? 1800) - 300}V2800H-1200Z" fill="#fff2c8" opacity=".22"/>`;   // where the sun starts
    s += `<path d="M330,700L760,690L790,1780L300,1790Z" fill="#c9a06c" opacity=".95" ${OUT}/><path d="M330,1000L770,990M320,1400L780,1390" stroke="#a5804f" stroke-width="6" fill="none"/>`;   // a flattened cardboard box under him
    put(L.set, s);
    const CLOTH = (k, x, y, a, w = 190) => `<g id="${id}-cl${k}" opacity="0" transform="translate(${x},${y}) rotate(${a})"><path d="M${-w / 2},-34Q0,-50 ${w / 2},-34L${w / 2 + 10},34Q0,50 ${-w / 2 - 10},34Z" fill="#c9d8e0" ${OUT}/><path d="M${-w / 2 + 20},-10q${w / 2},14 ${w - 40},0M${-w / 2 + 20},14q${w / 2},10 ${w - 40},0" stroke="#9fb6c2" stroke-width="4" fill="none"/>${[0, 1, 2].map((j) => `<circle cx="${-w / 3 + j * w / 3}" cy="40" r="5" fill="#6fb3d6" opacity=".8"/>`).join("")}</g>`;
    put(L.act, (o.cloths || [[540, 806, -6, 150], [540, 968, 0, 110], [452, 1012, 32, 84], [628, 1012, -32, 84]]).map(([x, y, a, w], k) => CLOTH(k, x, y, a, w)).join(""));
    put(L.fg, `<g id="${id}-pour" opacity="0" transform="translate(760,560) rotate(-120)">${BOTTLE(`${id}-pb`, 0.45)}</g><path id="${id}-stream" d="M690,600Q650,690 600,790" stroke="#9fd0ea" stroke-width="16" stroke-linecap="round" fill="none" opacity="0"/>`);
    put(L.fg, `<g id="${id}-fan" opacity="0" transform="translate(900,900)"><path d="M-140,-180L140,-200L160,160L-120,180Z" fill="#c9a06c" ${OUT}/><path d="M-100,-120l220,-14M-90,0l230,-10M-80,110l220,-12" stroke="#a5804f" stroke-width="6" fill="none"/><text x="10" y="-40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#8a6a42" transform="rotate(-4)">น้ำดื่ม</text></g>`);
    L.fg.classList.remove("fgblur");
  }

  // ---------------- the abandoned petrol station: canopy on four pillars, two pump islands, the minimart with its fridges ----------------
  // ids: #id-fridge (glow behind the glass), #id-chain (the lock on the door), #id-roof (the canopy top line — a guard stands at y = 760),
  // #id-lamp (a hurricane lamp under the canopy at night). opts: time (dusk/night), sign
  function station(L, o = {}) {
    const id = o.id || "st", t = o.time || "dusk", r = mk(o.seed || 71), night = t === "night";
    sky(L, t); sun(L, t, o.sunX ?? 900, 300);
    put(L.far, Fence.paddies(r, t, 1040));
    // the minimart behind (mid): concrete box, a glass front with shelves and glowing fridges, the chained door, a painted warning
    let m = `<g transform="translate(-200,1240)"><rect x="-500" y="-560" width="1500" height="560" fill="#d9d4c8" ${OUT}/><rect x="-500" y="-600" width="1500" height="60" fill="#c8392b" ${OUT}/><path d="M-500,-580H1000" stroke="#f4ecd8" stroke-width="8"/>
      <rect x="-440" y="-480" width="900" height="420" fill="url(#rGlass)" ${OUT}/>${[-260, -80, 100, 280].map((x) => `<path d="M${x},-480V-60" stroke="#5b6066" stroke-width="10"/>`).join("")}
      <g id="${id}-fridge"><rect x="-420" y="-460" width="300" height="390" fill="url(#rFridge)" opacity="${night ? 0.25 : 0.55}"/>${Array.from({ length: 4 }, (_, j) => `<path d="M-420,${-430 + j * 90}h300" stroke="#9fc0cc" stroke-width="5"/>${Array.from({ length: 7 }, (_, i) => `<rect x="${-410 + i * 40}" y="${-418 + j * 90}" width="24" height="60" rx="8" fill="#dfeff5" stroke="#6f8f9c" stroke-width="2"/><rect x="${-406 + i * 40}" y="${-428 + j * 90}" width="16" height="12" fill="#2f6fb8"/>`).join("")}`).join("")}</g>
      <rect x="560" y="-420" width="260" height="420" fill="#5b6066" ${OUT}/><rect x="580" y="-400" width="220" height="380" fill="url(#rGlass)" opacity=".7"/><g id="${id}-chain"><path d="M620,-230q70,-30 140,0q-70,30 -140,0" stroke="#8d9299" stroke-width="10" fill="none" stroke-dasharray="14 8"/><rect x="672" y="-226" width="36" height="44" rx="6" fill="#c9a55a" ${OUT}/></g>
      <text x="690" y="-300" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#c8392b" transform="rotate(-6 690 -300)" opacity=".95">ห้ามเข้า</text></g>`;
    m += `<g transform="translate(1600,1240)"><path d="M0,0V-820" stroke="#8d9299" stroke-width="30"/><rect x="-160" y="-1080" width="320" height="300" rx="18" fill="#e8e2d4" ${OUT}/><rect x="-140" y="-1060" width="280" height="110" rx="10" fill="#c8392b"/><text x="0" y="-985" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#f4ecd8">ปั๊ม</text>${[0, 1].map((k) => `<rect x="-130" y="${-930 + k * 66}" width="260" height="52" rx="6" fill="#1f1d1a"/><text x="110" y="${-893 + k * 66}" text-anchor="end" font-family="Kanit" font-weight="900" font-size="38" fill="#3a3f45">--.--</text>`).join("")}</g>`;
    put(L.mid, m);
    // the canopy (set): a deep slab on four square pillars; its top at y = 760 is where the guard stands
    let s = `<rect x="-1400" y="1240" width="4000" height="1500" fill="url(#fConc)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M${-1400 + k * 420},1240L${-1700 + k * 560},2700" stroke="#a9a397" stroke-width="4"/>`).join("")}`;
    s += `<g id="${id}-roof"><rect x="-700" y="760" width="2100" height="150" fill="#f4ecd8" ${OUT}/><rect x="-700" y="830" width="2100" height="50" fill="#c8392b"/><path d="M-700,910H1400" stroke="${INK}" stroke-width="5"/><rect x="-700" y="910" width="2100" height="40" fill="#3a3d40" opacity=".5"/>
      ${[[-200, 760], [-80, 760], [1100, 760]].map(([x, y]) => `<rect x="${x}" y="${y - 60}" width="110" height="64" rx="18" fill="#a5895a" ${OUT}/>`).join("")}<path d="M1300,760V1240M1340,760V1240${Array.from({ length: 10 }, (_, k) => `M1300,${800 + k * 46}h40`).join("")}" stroke="#8d9299" stroke-width="8" fill="none"/></g>`;
    s += [-520, 120, 760, 1240].map((x) => `<rect x="${x - 40}" y="950" width="80" height="300" fill="#cfc9bb" ${OUT}/>`).join("");
    const PUMP = (x) => `<g transform="translate(${x},1300)"><rect x="-220" y="-30" width="440" height="40" fill="#b3ada0" ${OUT}/><rect x="-90" y="-330" width="180" height="300" rx="14" fill="#e8e2d4" ${OUT}/><rect x="-70" y="-300" width="140" height="70" fill="#1f1d1a"/><rect x="-90" y="-200" width="180" height="40" fill="#c8392b"/><path d="M90,-180q60,0 60,90v70" stroke="#1f1d1a" stroke-width="12" fill="none"/><rect x="130" y="-30" width="40" height="30" rx="6" fill="#3a3f45"/></g>`;
    s += PUMP(-180) + PUMP(980);
    put(L.set, s);
    if (night) { put(L.glow, `<g id="${id}-lamp"><circle cx="${o.lampX ?? 420}" cy="1150" r="520" fill="url(#fLamp)" opacity=".9"/></g>`); put(L.set, `<g transform="translate(${o.lampX ?? 420},1240)"><rect x="-26" y="-80" width="52" height="80" rx="10" fill="#c9a55a" ${OUT}/><rect x="-16" y="-70" width="32" height="54" fill="#ffd58a"/></g>`); }
    else put(L.glow, `<rect x="-1400" y="700" width="4000" height="1400" fill="#ff9a3c" opacity=".14"/>`);
  }

  // ---------------- ปั้น's drawing that night: the estate (a factory with a chimney and a tall lit fence), ภู shaking hands with a man in a tie ----------------
  function drawing5(L, o = {}) {
    const id = o.id || "dw5";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#3a3330"/>`);
    let s = `<g transform="rotate(1.2 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    s += `<rect x="140" y="440" width="800" height="560" fill="#2f2a4a" opacity=".35" filter="url(#fCrayon)"/>`;   // night sky scribble
    s += C("M200,1080V760H760V1080M200,760L330,660L460,760L590,660L720,760M640,760V560H700V760", "#5b6066", 10) + `<rect x="200" y="760" width="560" height="320" fill="#b3ada0" opacity=".55" filter="url(#fCrayon)"/>`;   // saw-tooth factory roof + chimney
    s += C("M650,540q-20,-40 10,-70q-30,-30 0,-60", "#8a857a", 7);
    s += [[260, 860], [380, 860], [500, 860], [620, 860]].map(([x, y]) => `<rect x="${x}" y="${y}" width="60" height="60" fill="#ffd25a" filter="url(#fCrayon)"/>`).join("");   // lit windows
    s += C("M150,1180H940M150,1180V1040M250,1180V1040M350,1180V1040M450,1180V1040M550,1180V1040M650,1180V1040M750,1180V1040M850,1180V1040M940,1180V1040M150,1060H940", "#3f454b", 7);   // the tall fence
    s += [190, 400, 610, 820].map((x) => `<circle cx="${x}" cy="1030" r="14" fill="#ffd25a" filter="url(#fCrayon)"/>`).join("");   // lamps on the fence
    const fig = (x, y, col, h = 1, tie) => `<g transform="translate(${x},${y}) scale(${h})" filter="url(#fCrayon)"><circle cy="-130" r="30" fill="none" stroke="${col}" stroke-width="8"/><path d="M0,-100V0M0,-80l-40,40M0,0l-30,60M0,0l30,60" stroke="${col}" stroke-width="8" fill="none" stroke-linecap="round"/>${tie ? `<path d="M0,-98l-10,30l10,16l10,-16z" fill="#c8392b"/>` : ""}</g>`;
    s += `<g id="${id}-pair">${fig(470, 1430, "#6f8f3e")}${fig(600, 1430, "#5b6066", 1, true)}${C("M470,1350L600,1350", "#6f8f3e", 8)}${C("M600,1350l40,40", "#5b6066", 8)}</g>`;   // ภู and the man in the tie, hands joined
    s += fig(220, 1460, "#2f4a8a", 0.8) + fig(300, 1470, "#d96a8a", 0.8) + fig(360, 1480, "#e8b830", 0.55) + fig(840, 1450, "#c8392b", 0.8);
    s += `<text x="540" y="400" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="60" fill="#2f4a8a" filter="url(#fCrayon)">วันที่ 104 บ้านใหม่?</text>`;
    s += `<text x="540" y="1600" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#6f8f3e" filter="url(#fCrayon)">พี่ภู กับ คุณ...</text></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".35"/>`);
  }

  Object.assign(Sets, { highway, highwayPov, highwayTop, cab, underpass, aidClose, station, drawing5 });
})();
