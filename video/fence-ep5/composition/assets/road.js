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
    <pattern id="rAgg" width="120" height="70" patternUnits="userSpaceOnUse"><circle cx="8" cy="10" r="1.6" fill="#fff" opacity=".22"/><circle cx="34" cy="26" r="1.2" fill="#000" opacity=".3"/><circle cx="58" cy="8" r="2" fill="#000" opacity=".2"/><circle cx="76" cy="44" r="1.4" fill="#fff" opacity=".2"/><circle cx="96" cy="18" r="1.1" fill="#fff" opacity=".26"/><circle cx="112" cy="58" r="1.8" fill="#000" opacity=".24"/><circle cx="20" cy="52" r="1.3" fill="#000" opacity=".26"/><circle cx="46" cy="62" r="1.5" fill="#fff" opacity=".16"/><circle cx="66" cy="30" r="1" fill="#fff" opacity=".24"/><circle cx="104" cy="36" r="1.2" fill="#000" opacity=".22"/><circle cx="88" cy="64" r="1" fill="#000" opacity=".3"/><circle cx="4" cy="34" r="1" fill="#fff" opacity=".2"/><path d="M24,40l6,2M80,12l5,-2" stroke="#000" stroke-opacity=".2" stroke-width="1.5"/></pattern>
    <linearGradient id="rShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c8" stop-opacity=".16"/><stop offset=".7" stop-color="#fff2c8" stop-opacity=".07"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></linearGradient>
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
    if (o.plain !== true && window.Dress) g += `<path d="M-318,-120H318V-74H-318Z" fill="#000" opacity=".12"/><path d="M-318,-150H318" stroke="#000" stroke-opacity=".14" stroke-width="3"/>${van ? `<path d="M130,-296V-74M-100,-296V-74" stroke="#000" stroke-opacity=".3" stroke-width="3"/>` : `<path d="M20,-262V-76M-176,-200L-170,-80" stroke="#000" stroke-opacity=".3" stroke-width="3"/>`}<rect x="-10" y="-176" width="34" height="9" rx="4" fill="#3a3f45" opacity=".7"/><rect x="${van ? 150 : 150}" y="-176" width="34" height="9" rx="4" fill="#3a3f45" opacity=".7"/>
      <path d="M${van ? 236 : 170},-208l22,-6v18h-22z" fill="${col}" stroke="${INK}" stroke-width="3"/>${[-200, 210].map((wx) => `<path d="M${wx - 72},-74A72,60 0 0 1 ${wx + 72},-74" fill="#1a1918" opacity=".55"/>`).join("")}<path d="M-318,-90H318" stroke="#b39d7a" stroke-width="16" opacity=".22"/>
      <path d="${van ? "M-280,-286L-200,-206" : "M-150,-250L-110,-206"}M${van ? "-200,-286L-150,-236" : "40,-256L80,-210"}" stroke="#fff" stroke-width="7" opacity=".28"/>${[-200, 210].map((wx, k) => `<g transform="translate(${wx},${k === 0 && o.flat ? -40 : -52})"><circle r="15" fill="none" stroke="#5b6066" stroke-width="3"/>${[0, 72, 144, 216, 288].map((a) => `<circle cx="${f1(Math.cos(a * Math.PI / 180) * 10)}" cy="${f1(Math.sin(a * Math.PI / 180) * 10)}" r="2" fill="#3a3f45"/>`).join("")}</g>`).join("")}`;
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
    if (dressed(o)) m += highwayMid(r, o);
    put(L.mid, m);
    // set: the near carriageway we walk on (actors at y 1500), lane marks, cracks, our side's cars
    let s = `<rect x="-1400" y="1230" width="4000" height="1500" fill="url(#rAsph)"/><path d="M-1400,1250H2600" stroke="#e8b830" stroke-width="8"/><path d="M-1400,1660H2600" stroke="#f4ecd8" stroke-width="10" stroke-dasharray="120 90"/><path d="M-1400,2060H2600" stroke="#f4ecd8" stroke-width="10"/>`;
    for (let k = 0; k < 18; k++) { const x = -1300 + r() * 3800, y = 1300 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}l${f1(30 + r() * 40)},${f1(6 - r() * 12)}l${f1(20 + r() * 30)},${f1(10 - r() * 20)}" stroke="#4a4d50" stroke-width="3" fill="none"/>`; }
    s += `<path d="M-900,1560q400,-14 900,0" stroke="#3a3c3f" stroke-width="22" fill="none" opacity=".35"/><path d="M200,1780q500,10 1100,-6" stroke="#3a3c3f" stroke-width="22" fill="none" opacity=".3"/>`;
    if (dressed(o)) s += highwayFloor(mk((o.seed || 91) + 401), o);
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
    if (dressed(o)) { const D = Dress, q = mk((o.seed || 17) + 441);
      s += `<path d="M${VX - 6},${VY}L${VX + 6},${VY}L${VX + 2600},2700L${VX - 2600},2700Z" fill="url(#rAgg)" opacity=".8"/>`;
      for (let k = 0; k < 6; k++) { const lane = -1.6 + q() * 3.6, d0 = 0.05 + q() * 0.5, [x0, y0] = P(d0, lane), [x1, y1] = P(d0 + 0.2, lane + (q() - 0.5) * 0.4); s += `<path d="M${f1(x0)},${f1(y0)}Q${f1((x0 + x1) / 2 + (q() - 0.5) * 60)},${f1((y0 + y1) / 2)} ${f1(x1)},${f1(y1)}" stroke="#1f2022" stroke-width="${f1(10 * P(d0, 0)[2] + 2)}" fill="none" opacity=".45"/>`; }
      s += [[0.02, 0.6], [0.08, -0.7], [0.15, 0.2]].map(([d, lane]) => { const [x, y, k] = P(d, lane); return `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(220 * k)}" ry="${f1(40 * k)}" fill="#1a1b1c" opacity=".22"/>`; }).join("");
      if (!o.bridge) s += Array.from({ length: 12 }, (_, k) => { const [x, y, kk] = P(k / 12, 2.6); return `<rect x="${f1(x)}" y="${f1(y - 150 * kk)}" width="${f1(22 * kk + 2)}" height="${f1(150 * kk)}" fill="#f4ecd8" stroke="${INK}" stroke-width="2"/><rect x="${f1(x)}" y="${f1(y - 120 * kk)}" width="${f1(22 * kk + 2)}" height="${f1(20 * kk)}" fill="#c8392b"/>`; }).join("");
      s += litter([[VX - 360, 2050, "paper", 1.5, -10], [VX + 420, 1880, "bottle", 1.3, 20]]); }
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
    if (dressed(o)) underpassDress(L, id, o, mk((o.seed || 47) + 409));
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
    if (dressed(o)) { const D = Dress; s += agg(-1200, -800, 3500, 3600, 0.9) + [[200, 400, 160], [980, 1300, 120], [80, 1500, 90], [900, 500, 70]].map(([x, y, w]) => `<ellipse cx="${x}" cy="${y}" rx="${w}" ry="${w * 0.4}" fill="#26282a" opacity=".3"/>`).join("") + tarLine(r, -200, 200, 900, 0.6) + tarLine(r, 800, 1900, 700, -0.3) + D.pebbles(-900, 2000, -500, 2400, 50, 291, 9) + D.leaves(-900, 2000, -500, 2400, 20, 293) + litter([[160, 1700, "bottle", 1.2, -30], [930, 1600, "cup", 1.2, 40]]); }
    s += `<path d="M330,700L760,690L790,1780L300,1790Z" fill="#c9a06c" opacity=".95" ${OUT}/>${dressed(o) ? `${Array.from({ length: 22 }, (_, k) => `<path d="M${336 + k * 20},700L${306 + k * 21.5},1788" stroke="#b8905c" stroke-width="3" opacity=".7"/>`).join("")}<text x="540" y="1560" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#8a6a42" opacity=".5" transform="rotate(-1 540 1560)">น้ำดื่ม</text><rect x="320" y="1180" width="460" height="36" fill="#d9c9a0" opacity=".6"/><path d="M300,1790L790,1780L792,1800L302,1810Z" fill="#000" opacity=".2"/>` : ""}<path d="M330,1000L770,990M320,1400L780,1390" stroke="#a5804f" stroke-width="6" fill="none"/>`;   // a flattened cardboard box under him
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
    if (dressed(o)) { const q = mk((o.seed || 71) + 431);   // dusk: long streaks of cloud lit from below, a few birds; night: stars
      put(L.sky, t === "dusk" ? Array.from({ length: 9 }, () => { const x = -900 + q() * 2700, y = -300 + q() * 1100, w = 300 + q() * 700; return `<g opacity="${f1(0.45 + q() * 0.4)}"><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(18 + q() * 22)}" fill="#7a3a5a"/><ellipse cx="${f1(x + w * 0.1)}" cy="${f1(y + 10)}" rx="${f1(w * 0.8)}" ry="${f1(8 + q() * 8)}" fill="#ffb07a" opacity=".7"/></g>`; }).join("") + Array.from({ length: 5 }, () => { const x = 100 + q() * 900, y = 200 + q() * 400, w = 14 + q() * 10; return `<path d="M${f1(x - w)},${f1(y)}q${f1(w / 2)},${f1(-w / 2)} ${f1(w)},0q${f1(w / 2)},${f1(-w / 2)} ${f1(w)},0" stroke="#2a1a24" stroke-width="3" fill="none"/>`; }).join("")
        : night ? Array.from({ length: 70 }, () => `<circle cx="${f1(-1100 + q() * 3300)}" cy="${f1(-700 + q() * 1600)}" r="${f1(1 + q() * 2.2)}" fill="#e9eef5" opacity="${f1(0.35 + q() * 0.6)}"/>`).join("") : ""); }
    put(L.far, Fence.paddies(r, t, 1040));
    // the minimart behind (mid): concrete box, a glass front with shelves and glowing fridges, the chained door, a painted warning
    let m = `<g transform="translate(-200,1240)"><rect x="-500" y="-560" width="1500" height="560" fill="#d9d4c8" ${OUT}/><rect x="-500" y="-600" width="1500" height="60" fill="#c8392b" ${OUT}/><path d="M-500,-580H1000" stroke="#f4ecd8" stroke-width="8"/>
      <rect x="-440" y="-480" width="900" height="420" fill="url(#rGlass)" ${OUT}/>${[-260, -80, 100, 280].map((x) => `<path d="M${x},-480V-60" stroke="#5b6066" stroke-width="10"/>`).join("")}
      <g id="${id}-fridge"><rect x="-420" y="-460" width="300" height="390" fill="url(#rFridge)" opacity="${night ? 0.25 : 0.55}"/>${Array.from({ length: 4 }, (_, j) => `<path d="M-420,${-430 + j * 90}h300" stroke="#9fc0cc" stroke-width="5"/>${Array.from({ length: 7 }, (_, i) => `<rect x="${-410 + i * 40}" y="${-418 + j * 90}" width="24" height="60" rx="8" fill="#dfeff5" stroke="#6f8f9c" stroke-width="2"/><rect x="${-406 + i * 40}" y="${-428 + j * 90}" width="16" height="12" fill="#2f6fb8"/>`).join("")}`).join("")}</g>
      <rect x="560" y="-420" width="260" height="420" fill="#5b6066" ${OUT}/><rect x="580" y="-400" width="220" height="380" fill="url(#rGlass)" opacity=".7"/><g id="${id}-chain"><path d="M620,-230q70,-30 140,0q-70,30 -140,0" stroke="#8d9299" stroke-width="10" fill="none" stroke-dasharray="14 8"/><rect x="672" y="-226" width="36" height="44" rx="6" fill="#c9a55a" ${OUT}/></g>
      <text x="690" y="-300" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#c8392b" transform="rotate(-6 690 -300)" opacity=".95">ห้ามเข้า</text></g>`;
    m += `<g transform="translate(1600,1240)"><path d="M0,0V-820" stroke="#8d9299" stroke-width="30"/><rect x="-160" y="-1080" width="320" height="300" rx="18" fill="#e8e2d4" ${OUT}/><rect x="-140" y="-1060" width="280" height="110" rx="10" fill="#c8392b"/><text x="0" y="-985" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#f4ecd8">ปั๊ม</text>${[0, 1].map((k) => `<rect x="-130" y="${-930 + k * 66}" width="260" height="52" rx="6" fill="#1f1d1a"/><text x="110" y="${-893 + k * 66}" text-anchor="end" font-family="Kanit" font-weight="900" font-size="38" fill="#3a3f45">--.--</text>`).join("")}</g>`;
    put(L.mid, m);
    const fore = dressed(o) ? stationDress(L, id, o, mk((o.seed || 71) + 419), night) : "";
    // the canopy (set): a deep slab on four square pillars; its top at y = 760 is where the guard stands
    let s = `<rect x="-1400" y="1240" width="4000" height="1500" fill="url(#fConc)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M${-1400 + k * 420},1240L${-1700 + k * 560},2700" stroke="#a9a397" stroke-width="4"/>`).join("")}${fore}`;
    s += `<g id="${id}-roof"><rect x="-700" y="760" width="2100" height="150" fill="#f4ecd8" ${OUT}/><rect x="-700" y="830" width="2100" height="50" fill="#c8392b"/><path d="M-700,910H1400" stroke="${INK}" stroke-width="5"/><rect x="-700" y="910" width="2100" height="40" fill="#3a3d40" opacity=".5"/>
      ${[[-200, 760], [-80, 760], [1100, 760]].map(([x, y]) => `<rect x="${x}" y="${y - 60}" width="110" height="64" rx="18" fill="#a5895a" ${OUT}/>`).join("")}<path d="M1300,760V1240M1340,760V1240${Array.from({ length: 10 }, (_, k) => `M1300,${800 + k * 46}h40`).join("")}" stroke="#8d9299" stroke-width="8" fill="none"/></g>`;
    s += [-520, 120, 760, 1240].map((x) => `<rect x="${x - 40}" y="950" width="80" height="300" fill="#cfc9bb" ${OUT}/>`).join("");
    const PUMP = (x) => `<g transform="translate(${x},1300)"><rect x="-220" y="-30" width="440" height="40" fill="#b3ada0" ${OUT}/><rect x="-90" y="-330" width="180" height="300" rx="14" fill="#e8e2d4" ${OUT}/><rect x="-70" y="-300" width="140" height="70" fill="#1f1d1a"/><rect x="-90" y="-200" width="180" height="40" fill="#c8392b"/><path d="M90,-180q60,0 60,90v70" stroke="#1f1d1a" stroke-width="12" fill="none"/><rect x="130" y="-30" width="40" height="30" rx="6" fill="#3a3f45"/></g>`;
    s += PUMP(-180) + PUMP(980);
    if (dressed(o)) s += stationTop(id, o, mk((o.seed || 71) + 421), night);
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


  // ---------------- set dressing for the road sets (EP.5): asphalt grain, sealed cracks, skid marks, road studs, litter from
  // the evacuation, a grimy median barrier with weeds; under the overpass: stained concrete, posters, graffiti, a drain pipe,
  // someone's cardboard bed, a light shaft through the deck joint; at the station: oil stains, hazard kerbs, pump nozzles and
  // hoses, dead canopy lights, an ice chest, crates, a fire extinguisher, long dusk shadows. o.dress === false skips all of it.
  const dressed = (o) => o.dress !== false && !!window.Dress;
  const agg = (x, y, w, h, op = 1) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#rAgg)" opacity="${op}"/>`;
  const tarLine = (r, x, y, len, ang) => { let d = `M${f1(x)},${f1(y)}`, cx = x, cy = y; for (let k = 0; k < 6; k++) { cx += Math.cos(ang) * len / 6 + (r() - 0.5) * 30; cy += Math.sin(ang) * len / 6 + (r() - 0.5) * 12; d += `L${f1(cx)},${f1(cy)}`; }
    return `<path d="${d}" stroke="#1f2022" stroke-width="7" fill="none" stroke-linejoin="round" opacity=".5"/><path d="${d}" stroke="#a9adb1" stroke-width="2" fill="none" opacity=".22" transform="translate(0,-3)"/>`; };
  const LIT = {
    bottle: `<ellipse cx="4" cy="4" rx="42" ry="8" fill="#0b0d08" opacity=".22"/><rect x="-40" y="-14" width="74" height="26" rx="12" fill="#dfeff5" fill-opacity=".7" stroke="${INK}" stroke-width="2"/><rect x="34" y="-8" width="14" height="14" rx="3" fill="#2f6fb8" stroke="${INK}" stroke-width="2"/><path d="M-30,-8h50" stroke="#fff" stroke-width="3" opacity=".7"/>`,
    sandal: `<ellipse cx="4" cy="3" rx="40" ry="8" fill="#0b0d08" opacity=".2"/><path d="M-40,0q0,-16 34,-16h20q24,0 26,12q0,8 -26,8z" fill="#c8392b" stroke="${INK}" stroke-width="2"/><path d="M-6,-14q8,10 22,10" stroke="#e8e4da" stroke-width="4" fill="none"/>`,
    bag: `<ellipse cx="4" cy="4" rx="46" ry="9" fill="#0b0d08" opacity=".18"/><path d="M-40,0q-6,-30 20,-34q10,-12 22,0q30,4 22,34q-30,8 -64,0z" fill="#f4f4ee" fill-opacity=".75" stroke="${INK}" stroke-width="2"/><path d="M-20,-20q10,8 24,2" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>`,
    paper: `<path d="M-30,-6l50,-10l12,22l-50,8z" fill="#f2ede0" stroke="${INK}" stroke-width="1.5"/><path d="M-20,-4l34,-6M-16,4l30,-6" stroke="#8a857a" stroke-width="2"/>`,
    cup: `<ellipse cx="6" cy="4" rx="34" ry="7" fill="#0b0d08" opacity=".2"/><path d="M-26,-10l52,-6l-4,22l-44,4z" fill="#f4f4ee" stroke="${INK}" stroke-width="2"/><ellipse cx="-26" cy="0" rx="5" ry="10" fill="#e8e4da" stroke="${INK}" stroke-width="2"/>`,
    helmet: `<ellipse cx="6" cy="4" rx="56" ry="10" fill="#0b0d08" opacity=".25"/><path d="M-50,0q0,-56 50,-56q50,0 50,56z" fill="#e8b830" stroke="${INK}" stroke-width="3"/><path d="M-30,-8q30,-20 70,-8" stroke="#1f1d1a" stroke-width="10" fill="none"/><path d="M-30,-40q14,-12 30,-12" stroke="#fff" stroke-width="5" opacity=".5" fill="none"/>`,
    tyre: `<path d="M-60,0q20,-16 60,-10t60,6" stroke="#0b0d08" stroke-opacity=".2" stroke-width="20" fill="none" transform="translate(4,5)"/><path d="M-60,0q20,-16 60,-10t60,6" stroke="#1f1d1a" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M-50,-4q20,-12 50,-8" stroke="#55504a" stroke-width="3" fill="none" stroke-dasharray="6 6"/>`,
    case: `<ellipse cx="20" cy="6" rx="150" ry="16" fill="#0b0d08" opacity=".26"/><path d="M-110,-40L-100,-118L110,-112L110,-40Z" fill="#3f5a7a" stroke="${INK}" stroke-width="3"/><rect x="-110" y="-44" width="220" height="44" rx="8" fill="#2f4a6a" stroke="${INK}" stroke-width="3"/>
      <path d="M-96,-40q30,-22 64,-6q24,12 52,-2l52,-6l14,16h-182z" fill="#d96a8a" stroke="${INK}" stroke-width="2"/><path d="M-20,-46q20,-14 50,-6" stroke="#e8dcc6" stroke-width="10" fill="none"/><path d="M96,-6q50,-10 104,4l-8,14q-48,4 -96,-4z" fill="#e8dcc6" stroke="${INK}" stroke-width="2"/><rect x="-14" y="-52" width="28" height="10" rx="4" fill="#1f1d1a"/>`,
    poster: `<rect x="-60" y="-80" width="120" height="160" fill="#f2ede0" stroke="${INK}" stroke-width="2"/><rect x="-50" y="-70" width="100" height="40" fill="#c8392b" opacity=".8"/><path d="M-44,-14h88M-44,4h70M-44,22h80M-44,40h50" stroke="#5b6066" stroke-width="5"/><path d="M40,80l20,-30v30z" fill="#d9d4c8" stroke="${INK}" stroke-width="1.5"/>`,
  };
  const litter = (list) => list.map(([x, y, k, s = 1, a = 0]) => Dress.at(x, y, s, LIT[k], a)).join("");

  // the near carriageway (set layer, under the cars) and the median + far carriageway (mid layer)
  function highwayFloor(r, o) {
    const D = Dress;
    let s = agg(-1400, 1240, 4000, 1500, 0.9);
    s += [[1330, 1470], [1740, 1890]].map(([a, b]) => `<rect x="-1400" y="${a}" width="4000" height="46" fill="#000" opacity=".07"/><rect x="-1400" y="${b}" width="4000" height="46" fill="#000" opacity=".07"/><rect x="-1400" y="${a + 46}" width="4000" height="8" fill="#fff" opacity=".05"/><rect x="-1400" y="${b + 46}" width="4000" height="8" fill="#fff" opacity=".05"/>`).join("");
    for (let k = 0; k < 7; k++) s += tarLine(r, -1300 + r() * 3600, 1290 + r() * 720, 260 + r() * 320, (r() - 0.5) * 0.5);
    for (let k = 0; k < 4; k++) s += tarLine(r, -1200 + r() * 3400, 1280 + r() * 300, 220 + r() * 160, 1.2 + r() * 0.5);
    s += [[-320, 1700, 260, 120], [880, 1320, 200, 90], [1700, 1880, 300, 110], [-1100, 1360, 180, 80]].map(([x, y, w, h]) => `<path d="M${x},${y + 6}L${x + w * 0.4},${y}L${x + w},${y + 8}L${x + w - 6},${y + h}L${x + w * 0.5},${y + h - 6}L${x + 4},${y + h}Z" fill="#505356" opacity=".4" stroke="#2a2c2e" stroke-opacity=".3" stroke-width="3"/>`).join("");
    for (let k = 0; k < 7; k++) { const x = -1200 + r() * 3400, y = 1300 + r() * 760, w = 40 + r() * 70; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.22)}" fill="#1a1b1c" opacity=".26"/><ellipse cx="${f1(x - w * 0.2)}" cy="${f1(y - 2)}" rx="${f1(w * 0.4)}" ry="${f1(w * 0.07)}" fill="#7a6a9a" opacity=".12"/>`; }
    s += [0, 64].map((dy) => `<path d="M-1200,${1860 + dy}C-600,${1846 + dy} -100,${1790 + dy} 420,${1720 + dy * 0.6}" stroke="#1a1b1c" stroke-width="16" opacity=".3" fill="none" stroke-linecap="round"/>`).join("");
    for (let x = -1400 + 165; x < 2600; x += 210) s += `<rect x="${x - 9}" y="1653" width="18" height="14" rx="3" fill="#e8e4da" stroke="${INK}" stroke-width="1.5"/><rect x="${x - 7}" y="1655" width="14" height="5" fill="#ffb84a"/>`;
    for (let x = -1300; x < 2600; x += 300) s += `<rect x="${x - 8}" y="1243" width="16" height="12" rx="3" fill="#e8b830" stroke="${INK}" stroke-width="1.5"/>`;
    for (let k = 0; k < 26; k++) { const x = -1350 + r() * 3900, y = r() < 0.5 ? 1660 : 2060; s += `<ellipse cx="${f1(x)}" cy="${f1(y + (r() - 0.5) * 6)}" rx="${f1(8 + r() * 22)}" ry="${f1(3 + r() * 3)}" fill="#606366" opacity=".55"/>`; }
    s += `<path d="M-1400,1256${Array.from({ length: 20 }, (_, k) => `Q${-1300 + k * 200},${1270 + (k % 3) * 6} ${-1200 + k * 200},1258`).join("")}V1252H-1400Z" fill="#b8a47a" opacity=".45"/>`;
    s += D.pebbles(-1400, 2600, 1262, 1300, 40, 211, 5);
    if (!o.bridge) {
      s += `<rect x="-1400" y="2072" width="4000" height="110" fill="#8f8a7e"/>${agg(-1400, 2072, 4000, 110, 0.7)}<rect x="-1400" y="2176" width="4000" height="700" fill="#7f8a52"/><path d="M-1400,2178${Array.from({ length: 30 }, (_, k) => `q${66},${(k % 2 ? 1 : -1) * 10} 134,0`).join("")}" stroke="#6a7444" stroke-width="10" fill="none"/>`;
      s += D.pebbles(-1400, 2600, 2080, 2170, 60, 213, 7) + D.tufts(-1400, 2600, 2180, 2600, 70, 215, 46, true) + D.weeds(-1400, 2600, 2182, 217, 54);
    }
    s += litter([[-160, 1440, "case", 1], [-260, 1600, "paper", 1, -10], [320, 1960, "bottle", 1, 14], [1060, 1580, "sandal", 1, 22], [620, 1370, "cup", 1], [-880, 1990, "bag", 1], [1440, 2020, "tyre", 1.2], [180, 1780, "paper", 1, 30], [1900, 1700, "bottle", 1, -40], [-560, 1820, "helmet", 0.9, -8]]);
    return s;
  }
  function highwayMid(r, o) {
    const D = Dress;
    let m = agg(-1400, 1040, 4000, 120, 0.7);
    m += `<rect x="-1400" y="1160" width="4000" height="70" fill="url(#dConc)" opacity=".85"/><rect x="-1400" y="1160" width="4000" height="70" fill="url(#dGrime)"/><path d="M-1400,1163H2600" stroke="#fff" stroke-opacity=".4" stroke-width="3"/>`;
    for (let x = -1300; x < 2600; x += 360) m += `<rect x="${x}" y="1184" width="16" height="11" rx="2" fill="#ff9a3c" stroke="${INK}" stroke-width="1.5"/>`;
    for (let k = 0; k < 16; k++) m += D.streak(-1400 + r() * 4000, 1172, 20 + r() * 30, 56, 0.7);
    m += D.weeds(-1400, 2600, 1232, 219, 30);
    if (o.billboard !== false) { const bx = o.billboardX ?? 1500; m += `<g transform="translate(${bx},1160)"><rect x="-160" y="-520" width="420" height="230" fill="url(#dGrime)"/>${D.streak(-130, -292, 40, 140, 0.8)}${D.streak(150, -292, 30, 120, 0.7)}${D.rust(-160, -520, 70, 120, 0.7)}<path d="M260,-520l-40,0l40,46z" fill="#cfc9bb" stroke="${INK}" stroke-width="2"/></g>`; }
    return m;
  }

  // under the overpass: concrete wear on deck and pillars, posters, graffiti, a drain pipe and its puddle, a cardboard bed
  function underpassDress(L, id, o, r) {
    const D = Dress, P = o.pillars || [40, 1180];
    let s = `<rect x="-1400" y="-900" width="4000" height="1270" fill="url(#dConc)" opacity=".45"/>${Array.from({ length: 12 }, (_, k) => `<rect x="${-1400 + k * 360 + 54}" y="-900" width="6" height="1200" fill="#fff" opacity=".06"/>`).join("")}`;
    s += `<rect x="-1400" y="300" width="4000" height="70" fill="url(#dGrime)"/>${Array.from({ length: 10 }, () => D.streak(-1400 + r() * 4000, 300, 30 + r() * 50, 70, 0.8)).join("")}`;
    s += Array.from({ length: 7 }, () => { const x = -1100 + r() * 3200; return `<path d="M${f1(x)},370q-16,0 -18,16q18,12 36,0q-2,-16 -18,-16z" fill="#8a6a42" stroke="${INK}" stroke-width="2"/>`; }).join("");
    s += P.map((x, j) => `<rect x="${x - 110}" y="370" width="220" height="1160" fill="url(#dConc)"/>${D.streak(x - 100, 370, 80, 420, 0.9)}${D.streak(x + 20, 370, 60, 300, 0.7)}<rect x="${x - 110}" y="1380" width="220" height="150" fill="url(#dGrime)"/>
      <path d="M${x - 110},372V1528M${x + 110},372V1528" stroke="#fff6d8" stroke-opacity=".28" stroke-width="5"/><path d="M${x + 108},${900 + j * 80}l-20,24l6,30l-16,20" stroke="#3a2a20" stroke-width="3" fill="none"/><path d="M${x + 96},${940 + j * 80}h14M${x + 94},${960 + j * 80}h16" stroke="#8a4a22" stroke-width="3"/>
      <text x="${x}" y="560" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="#e8e2d4" opacity=".6">P${12 + j}</text>
      ${D.at(x - 30, 820, 0.9, LIT.poster, -3)}${j === 0 ? D.at(x + 46, 880, 0.75, LIT.poster.replace("#c8392b", "#2f6fb8"), 5) : ""}
      <path d="M${x - 90},${1180 - j * 40}q30,-40 60,-6q20,24 50,-20q16,-24 36,4" stroke="${j ? "#c8392b" : "#2f6fb8"}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/><path d="M${x - 70},${1230 - j * 40}l40,-20l30,24l40,-30" stroke="#f4ecd8" stroke-width="6" fill="none" opacity=".55"/>`).join("");
    // the drain pipe down the left pillar, its stain and puddle
    const px = P[0] + 80;
    s += `<rect x="${px}" y="370" width="24" height="1150" fill="#7d858c" stroke="${INK}" stroke-width="3"/><rect x="${px + 4}" y="370" width="6" height="1150" fill="#fff" opacity=".25"/>${[600, 900, 1200].map((y) => `<rect x="${px - 6}" y="${y}" width="36" height="12" fill="#5b6066" stroke="${INK}" stroke-width="2"/>`).join("")}<path d="M${px - 4},1520h32l10,14h-52z" fill="#5b6066" stroke="${INK}" stroke-width="2"/>`;
    s += agg(-1400, 1280, 4000, 1500, 0.55) + `<rect x="-1400" y="1280" width="4000" height="80" fill="url(#dAO)"/>` + D.puddle(px + 70, 1560, 130, 22, true);
    s += D.tracks(-1300, 2400, -300, 1700, 400, 1300, 100, 0.14);
    // someone sheltered here: cardboard bed with a pillow and blanket by the right pillar, bottles, a plastic stool, rubble
    s += D.at(P[1] - 380, 1360, 1, `<ellipse cx="10" cy="10" rx="230" ry="20" fill="#0b0d08" opacity=".3"/><path d="M-210,0L190,-14L210,20L-190,30Z" fill="#c9a06c" stroke="${INK}" stroke-width="3"/><path d="M-60,-6l10,30M70,-10l6,28" stroke="#a5804f" stroke-width="4"/><path d="M110,-30q40,-18 80,0q10,20 -10,24h-64q-16,-6 -6,-24z" fill="#e8dcc6" stroke="${INK}" stroke-width="2"/><path d="M-180,-6q100,-40 200,-20q40,10 60,24l-260,20z" fill="#4f6a8a" stroke="${INK}" stroke-width="2"/><path d="M-150,-10q80,-24 170,-10" stroke="#fff" stroke-width="4" opacity=".25" fill="none"/>`);
    s += D.bottles(P[1] - 120, 1346, 0.8, 3) + D.at(-700, 1350, 1, `<ellipse cx="6" cy="4" rx="70" ry="10" fill="#0b0d08" opacity=".26"/><path d="M-50,0L-40,-70H40L50,0" fill="none" stroke="#2f6fb8" stroke-width="10"/><ellipse cx="0" cy="-72" rx="50" ry="12" fill="#2f6fb8" stroke="${INK}" stroke-width="3"/>`);
    s += D.at(-260, 1330, 1, `<ellipse cx="0" cy="6" rx="150" ry="16" fill="#0b0d08" opacity=".25"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-120 + k * 28},0l${10 + (k % 3) * 6},-${20 + (k * 7) % 26}l${18 + (k % 2) * 8},${12 + (k % 4) * 4}z" fill="${["#8d8a84", "#a9a397", "#76736d"][k % 3]}" stroke="${INK}" stroke-width="1.5"/>`).join("")}`);
    s += litter([[-500, 1500, "bag", 1.1], [300, 1720, "cup", 1.1, 20], [860, 1880, "paper", 1.2, -12], [-900, 1800, "bottle", 1.2, 30], [1500, 1700, "sandal", 1.1, -20]]) + D.leaves(-1300, 2400, 1300, 1900, 40, 223);
    put(L.set, s);
    // a shaft of sun through the joint between the two decks, lighting a band of floor; dust in it
    put(L.glow, `<path d="M570,370L630,370L860,1640L640,1640Z" fill="url(#rShaft)"/>${[[240, 50, 0.1], [180, 36, 0.12], [110, 22, 0.14]].map(([rx, ry, op]) => `<ellipse cx="750" cy="1640" rx="${rx}" ry="${ry}" fill="#fff2c8" opacity="${op}"/>`).join("")}${Array.from({ length: 10 }, () => `<circle class="mote" cx="${f1(600 + r() * 260)}" cy="${f1(200 + r() * 1300)}" r="${f1(2 + r() * 3)}" fill="#fff6dc" opacity=".55"/>`).join("")}`);
  }

  // the petrol station: forecourt wear, kerbs, pump detail, canopy lights, minimart clutter, long dusk shadows
  function stationDress(L, id, o, r, night) {
    const D = Dress;
    let m = `<g transform="translate(-200,1240)"><rect x="-500" y="-560" width="1500" height="560" fill="url(#dConc)" opacity=".7"/><rect x="-500" y="-160" width="1500" height="160" fill="url(#dGrime)"/>${D.streak(-480, -540, 60, 200, 0.8)}${D.streak(860, -540, 80, 260, 0.8)}${D.streak(420, -540, 40, 120, 0.6)}
      <path d="M-440,-480L-200,-60M-300,-480L-60,-60M200,-480L420,-90" stroke="#fff" stroke-opacity=".14" stroke-width="40"/><rect x="60" y="-300" width="120" height="150" fill="#f2ede0" stroke="${INK}" stroke-width="2" transform="rotate(-2 120 -225)"/><text x="120" y="-250" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#c8392b">ลดราคา</text><path d="M80,-210h80M80,-190h60" stroke="#5b6066" stroke-width="5"/>
      <rect x="840" y="-500" width="120" height="80" fill="#cfc9bb" stroke="${INK}" stroke-width="3"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${852 + k * 22},-490v60" stroke="#8d9299" stroke-width="4"/>`).join("")}${D.rust(840, -420, 50, 70, 0.8)}
      <g transform="translate(-380,0)"><ellipse cx="10" cy="4" rx="120" ry="14" fill="#0b0d08" opacity=".3"/><rect x="-100" y="-130" width="200" height="130" rx="10" fill="#2f6fb8" stroke="${INK}" stroke-width="3"/><rect x="-100" y="-150" width="200" height="28" rx="8" fill="#e8e4da" stroke="${INK}" stroke-width="3"/><text x="0" y="-60" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#f4ecd8">น้ำแข็ง</text><rect x="-100" y="-130" width="200" height="130" fill="url(#dGrime)"/></g>
      ${D.crate(-150, 0, 1, 110, 70, "#c8392b")}${D.crate(-150, -70, 1, 100, 60, "#e8b830")}${D.crate(-40, 0, 1, 110, 70, "#2f6f6a")}
      <g transform="translate(470,0)"><ellipse cx="4" cy="4" rx="34" ry="7" fill="#0b0d08" opacity=".3"/><rect x="-20" y="-90" width="40" height="90" rx="14" fill="#c8392b" stroke="${INK}" stroke-width="3"/><path d="M-10,-90v-14h20v14M10,-100q26,0 26,30" stroke="#1f1d1a" stroke-width="6" fill="none"/><rect x="-20" y="-60" width="40" height="22" fill="#f4ecd8" opacity=".85"/></g>
      <g transform="translate(1060,-20)"><rect x="-10" y="-380" width="160" height="70" rx="6" fill="#1f6b46" stroke="${INK}" stroke-width="3"/><text x="70" y="-332" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#f4ecd8">ห้องน้ำ →</text><path d="M60,-310V0" stroke="#8d9299" stroke-width="10"/></g></g>`;
    put(L.mid, m);
    // forecourt (set layer, before the canopy)
    let f = `<rect x="-1400" y="1240" width="4000" height="1500" fill="url(#dConc)"/><rect x="-1400" y="1240" width="4000" height="1500" fill="url(#rAgg)" opacity=".5"/><rect x="-1400" y="1240" width="4000" height="70" fill="url(#dAO)"/>${[1420, 1640, 1900, 2200].map((y) => `<path d="M-1400,${y}H2600" stroke="#8f897c" stroke-width="5"/><path d="M-1400,${y + 4}H2600" stroke="#fff" stroke-opacity=".25" stroke-width="2"/>`).join("")}`;
    for (let k = 0; k < 10; k++) { const x = -1200 + r() * 3300, y = 1300 + r() * 900; f += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(120 + r() * 200)}" ry="${f1(30 + r() * 40)}" fill="#7a6a58" opacity=".1"/>`; }
    for (let k = 0; k < 8; k++) { const x = -1100 + r() * 3200, y = 1330 + r() * 600, w = 50 + r() * 90; f += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.24)}" fill="#2a2420" opacity=".22"/>`; }
    f += [-180, 980].map((x) => `<ellipse cx="${x + 60}" cy="1340" rx="200" ry="34" fill="#1a1612" opacity=".3"/><ellipse cx="${x - 40}" cy="1360" rx="90" ry="16" fill="#3a2a5a" opacity=".12"/>`).join("");
    f += D.tracks(-1300, 2500, -300, 1700, 300, 1320, 110, 0.12) + D.tracks(2400, 2500, 1500, 1700, 900, 1320, 110, 0.1);
    for (let k = 0; k < 8; k++) f += D.crack(-1200 + r() * 3300, 1300 + r() * 800, 60 + r() * 80, r() * 80 - 40, 0.55);
    f += D.weeds(-1300, -760, 1252, 227, 34) + D.weeds(1500, 2400, 1252, 229, 40) + D.tufts(-1300, 2400, 1400, 2100, 20, 231, 32, true);
    f += `<g opacity=".55"><path d="M-760,1780l80,-60l80,60M-700,1720v120" stroke="#f4ecd8" stroke-width="16" fill="none" stroke-linecap="round"/><text x="-560" y="1830" font-family="Kanit" font-weight="900" font-size="60" fill="#f4ecd8" transform="rotate(-4 -560 1830)">เข้า</text></g><rect x="1460" y="1980" width="200" height="40" rx="6" fill="#3a3d40" stroke="${INK}" stroke-width="3" opacity=".7"/>${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${1476 + k * 26},1986v28" stroke="#1a1b1c" stroke-width="6"/>`).join("")}`;
    if (!night) f += [-520, 120, 760, 1240].map((x) => `<path d="M${x - 40},1250L${x + 40},1250L${x + 150},1900L${x - 10},1900Z" fill="#1a1612" opacity=".16"/>`).join("") + [-180, 980].map((x) => `<path d="M${x - 90},1300L${x + 90},1300L${x + 200},1700L${x + 20},1700Z" fill="#1a1612" opacity=".14"/>`).join("");
    f += litter([[-900, 1620, "bottle", 1.1, 20], [300, 1760, "paper", 1.2, -14], [1500, 1600, "cup", 1.1], [-300, 1950, "bag", 1.2]]) + D.leaves(-1300, 2400, 1300, 2000, 30, 233);
    return f;
  }
  // detail drawn over the canopy and pumps (set layer, after them)
  function stationTop(id, o, r, night) {
    const D = Dress;
    let s = `<rect x="-700" y="760" width="2100" height="150" fill="url(#dGrime)"/>${Array.from({ length: 8 }, () => D.streak(-680 + r() * 2000, 880, 30 + r() * 40, 70, 0.8)).join("")}${D.rust(-700, 760, 90, 120, 0.6)}${D.rust(1300, 790, 80, 110, 0.6)}`;
    s += `<rect x="-700" y="910" width="2100" height="40" fill="#cfc9bb"/><rect x="-700" y="910" width="2100" height="40" fill="url(#dConc)"/>${[-560, -260, 40, 340, 640, 940, 1240].map((x, k) => k === 3 ? `<g transform="rotate(14 ${x} 920)"><rect x="${x}" y="918" width="140" height="16" rx="4" fill="#e8e4da" stroke="${INK}" stroke-width="2"/></g><path d="M${x + 4},920l-6,40" stroke="#3a3330" stroke-width="2"/>` : `<rect x="${x}" y="918" width="140" height="16" rx="4" fill="${night ? "#8d9299" : "#e8e4da"}" stroke="${INK}" stroke-width="2"/>`).join("")}<rect x="-700" y="942" width="2100" height="10" fill="#000" opacity=".25"/>`;
    s += [-520, 120, 760, 1240].map((x) => `<rect x="${x - 40}" y="950" width="80" height="300" fill="url(#dConc)"/><rect x="${x - 40}" y="950" width="18" height="300" fill="#fff" opacity=".14"/><rect x="${x + 22}" y="950" width="18" height="300" fill="#000" opacity=".12"/><rect x="${x - 40}" y="1200" width="80" height="50" fill="url(#dGrime)"/><rect x="${x - 26}" y="1040" width="52" height="40" rx="4" fill="#f4ecd8" stroke="${INK}" stroke-width="1.5"/><circle cx="${x}" cy="1060" r="14" fill="none" stroke="#c8392b" stroke-width="4"/><path d="M${x - 10},1070l20,-20" stroke="#c8392b" stroke-width="4"/>`).join("");
    const pump = (x, g) => `<g transform="translate(${x},1300)"><path d="M-220,-30h440v40h-440z" fill="url(#dGrime)"/>${Array.from({ length: 11 }, (_, k) => `<path d="M${-220 + k * 40},10l20,-40h20l-20,40z" fill="${k % 2 ? "#1f1d1a" : "#e8b830"}" opacity=".85"/>`).join("")}<path d="M-220,-30h440" stroke="${INK}" stroke-width="3"/>
      <rect x="-70" y="-300" width="140" height="70" fill="#1f1d1a"/><text x="60" y="-252" text-anchor="end" font-family="Kanit" font-weight="900" font-size="34" fill="#3a3f45">00.00</text><rect x="-90" y="-200" width="180" height="40" fill="url(#dGrime)"/>${g.map((t, k) => `<rect x="${-80 + k * 56}" y="-150" width="50" height="34" rx="4" fill="${["#e8b830", "#c8392b", "#1f6b46"][k]}" stroke="${INK}" stroke-width="2"/><text x="${-55 + k * 56}" y="-125" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${t.length > 2 ? 16 : 22}" fill="#f4ecd8">${t}</text>`).join("")}
      <rect x="-90" y="-330" width="180" height="300" rx="14" fill="url(#dGrime)"/><path d="M-90,-326V-34" stroke="#fff" stroke-opacity=".3" stroke-width="6"/><g transform="translate(-112,-150)"><rect x="-14" y="-40" width="24" height="60" rx="6" fill="#1f1d1a" stroke="${INK}" stroke-width="2"/><path d="M-4,-36l-20,-10v-14l30,4z" fill="#3a3f45" stroke="${INK}" stroke-width="2"/><path d="M-2,20q-30,60 10,120q30,30 70,10" stroke="#1f1d1a" stroke-width="10" fill="none"/></g>
      ${D.bucket(150, -30, 0.7, "#2f6fb8")}<path d="M150,-120l30,-70" stroke="#8a6a42" stroke-width="5"/><path d="M168,-190h30" stroke="#1f1d1a" stroke-width="10"/></g>`;
    s += pump(-180, ["91", "95", "ดีเซล"]) + pump(980, ["91", "95", "ดีเซล"]);
    s += D.drum(1480, 1250, 0.8, "#c8392b") + D.tires(-760, 1250, 0.8, 3) + D.sandbags(330, 1252, 0.7, 4, 2, 241);
    return s;
  }

  Object.assign(Sets, { highway, highwayPov, highwayTop, cab, underpass, aidClose, station, drawing5 });
})();
