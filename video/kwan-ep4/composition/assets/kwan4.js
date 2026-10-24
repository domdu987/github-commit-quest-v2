// Sets and people for "ควันหลง" EP.4 ห้ามกลับ (the finale; loaded after kwan3.js):
//   Sets.kwanLegend   2539 told in shadow puppets on four cloth screens (y 0 / 1600 / 3200 / 4800, each 900 tall): the dorm
//                     burning; ดาว outside hearing her roommate call from the seventh floor; ดาว going back in; the roommate
//                     coming down the far stairs while ดาว stays in the window (#id-flames, #id-call, #id-go, #id-win)
//   Kwan.residents    a huddle of residents in blankets at the assembly point (silhouettes against the siren light)
//   Kwan.assembly     the green "จุดรวมพล" sign on its post
//   Kwan.daoWindow    ดาว in 714's window: a burnt silhouette, ember eyes, a waving arm (#id-arm)
//   Rig.CAST.ff (a firefighter in turnout gear), Rig.CAST.sri (ป้าศรี, the housekeeper, sixty, grey bun)
// Card icons: assembly, staythere, tellff.
(function () {
  const INK = "#2e2a26";
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const f1 = (v) => (+v).toFixed(1);
  const LAVA = "#ff6a1a", CH = "#1b1512";

  if (window.Rig) {
    Rig.CAST.ff = { // firefighter: khaki turnout coat with reflective bands, yellow helmet, breathing set on the back
      skin: "#d6a27c", skinS: "#b5825e", top: "#c9b27a", topS: "#a8925e", sleeve: "#c9b27a", sleeveS: "#a8925e", forearm: "#c9b27a", forearmS: "#a8925e",
      pants: "#c9b27a", pantsS: "#a8925e", shoe: "#1e1b19", belt: "#2e2a26",
      torsoExtra: `<rect x="-58" y="-380" width="116" height="16" fill="#e8f0d0"/><rect x="-58" y="-350" width="116" height="10" fill="#c8d04a"/><rect x="-58" y="-460" width="116" height="12" fill="#e8f0d0"/>
        <path d="M-10,-482V-330" stroke="#2e2a26" stroke-width="5"/><rect x="18" y="-450" width="30" height="40" rx="6" fill="#2a2c2a" ${OUT3}/>`,
      hair: `<path d="M-60,-556Q-62,-626 0,-630Q62,-626 60,-556Z" fill="#f2c230" ${OUT3}/><path d="M-76,-556H76L70,-540H-70Z" fill="#d8a820" ${OUT3}/><rect x="-14" y="-622" width="28" height="40" rx="4" fill="#c8392b"/>
        <path d="M-40,-610Q0,-640 40,-610" stroke="#fff6c8" stroke-width="5" fill="none" opacity=".6"/>`,
      face: `<path d="M-44,-540L-50,-500M44,-540L50,-500" stroke="#2e2a26" stroke-width="5"/>`,
    };
    Rig.CAST.sri = { // ป้าศรี: sixty, the dorm's housekeeper — pale blue uniform, an apron, grey hair in a low bun, reading glasses
      skin: "#d9a982", skinS: "#b98a64", top: "#9ab4c8", topS: "#7a94a8", sleeve: "#9ab4c8", sleeveS: "#7a94a8", forearm: "#d9a982", forearmS: "#b98a64",
      pants: "#4a5560", pantsS: "#3a444e", shoe: "#2a2420", belt: "#e8e4d8",
      torsoExtra: `<path d="M-40,-440H40L48,-300H-48Z" fill="#f2efe6" ${OUT3}/><path d="M-30,-484L0,-458L30,-484" fill="#e8e4d8" ${OUT3}/>`,
      hair: `<path d="M-50,-548Q-56,-612 0,-614Q56,-612 50,-548Q44,-578 0,-584Q-44,-578 -50,-548Z" fill="#b8b4ac" ${OUT3}/><circle cx="0" cy="-616" r="22" fill="#a8a49c" ${OUT3}/>
        <path d="M-40,-596q20,-12 40,-8" stroke="#d8d4cc" stroke-width="4" fill="none"/>`,
      face: `<g fill="none" stroke="#5a4a3a" stroke-width="3"><circle cx="-14" cy="-546" r="12"/><circle cx="18" cy="-546" r="12"/><path d="M-2,-546h8"/></g>
        <path d="M-30,-512q8,6 16,2M14,-512q8,4 16,-2" stroke="#b98a64" stroke-width="3" fill="none"/>`,
    };
  }

  // a huddle of residents wrapped in blankets (back-lit silhouettes), n figures from x0 spaced by gap
  function residents(x0, y, s, n = 6, gap = 120) {
    const col = ["#4a5a78", "#6a5a7a", "#5a6a5a", "#7a6a5a", "#5a5a6a", "#6a7a8a"];
    let g = "";
    for (let k = 0; k < n; k++) {
      const x = x0 + k * gap + (k % 2) * 18, h = 300 + (k % 3) * 30, sc = s * (0.9 + (k % 3) * 0.07);
      g += `<g transform="translate(${f1(x)},${f1(y + (k % 2) * 14)}) scale(${f1(sc)})"><path d="M-60,0C-70,-${h * 0.6} -50,-${h * 0.9} 0,-${h * 0.92}C50,-${h * 0.9} 70,-${h * 0.6} 60,0Z" fill="${col[k % col.length]}" ${OUT3}/>
        <circle cx="0" cy="-${h}" r="30" fill="#2a2420"/><path d="M-50,-${h * 0.5}Q0,-${h * 0.42} 50,-${h * 0.5}" stroke="#2e2a26" stroke-width="4" fill="none" opacity=".5"/></g>`;
    }
    return g;
  }
  // the assembly-point sign
  const assembly = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M0,0V-420" stroke="#8a9096" stroke-width="14"/><rect x="-150" y="-620" width="300" height="220" rx="16" fill="#2f8a52" stroke="#eaffe8" stroke-width="8"/>
      ${[-60, 0, 60].map((dx) => `<circle cx="${dx}" cy="-570" r="16" fill="#eaffe8"/><path d="M${dx - 22},-490q0,-50 22,-54t22,54z" fill="#eaffe8"/>`).join("")}
      <path d="M-100,-520l-20,20l20,20M100,-520l20,20l-20,20" stroke="#eaffe8" stroke-width="8" fill="none"/><rect x="-150" y="-390" width="300" height="70" rx="10" fill="#f2efe6"/>
      <text x="0" y="-342" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#2f8a52">จุดรวมพล</text></g>`;
  // ดาว in 714's window: a burnt silhouette with ember eyes, one arm waving (pivot at the shoulder)
  const daoWindow = (id, x, y, s = 1) => `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-26,0C-28,-34 -22,-50 0,-52C22,-50 28,-34 26,0Z" fill="${CH}"/><circle cx="0" cy="-64" r="15" fill="${CH}"/>
      ${[-13, -8, -3, 2, 7, 12].map((dx, k) => `<path d="M${dx},-75q${k % 2 ? 2 : -2},-4 ${k % 2 ? -1 : 1},-7" stroke="${CH}" stroke-width="3.5" fill="none" stroke-linecap="round"/>`).join("")}
      <path d="M-8,-66q3,-2 6,0M3,-66q3,-2 6,0" stroke="#ffd27a" stroke-width="2.4" stroke-linecap="round"/><circle cx="0" cy="-66" r="14" fill="${LAVA}" opacity=".25" class="flk"/>
      <g id="${id}-arm" transform="rotate(0 16 -40)"><path d="M16,-40L34,-80" stroke="${CH}" stroke-width="8" stroke-linecap="round"/></g></g>`;

  // ---------------- 2539 in shadow puppets ----------------
  Sets.kwanLegend = function (L, o) {
    const id = o.id || "kl", P = "#170d06", CUT = "#ffd9a0", ROD = "#3a2414", LGY = [0, 1600, 3200, 4800];
    put(L.sky, `<rect x="-900" y="-1200" width="2900" height="8400" fill="#1c1009"/>`);
    const screen = (y0, y1) => `<rect x="-40" y="${y0}" width="1160" height="${y1 - y0}" fill="#e9a457"/>
      <circle class="lamp" cx="540" cy="${(y0 + y1) / 2}" r="${(y1 - y0) * 0.75}" fill="url(#clothglow)"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-40 + k * 40},${y0}V${y1}" stroke="#c98a44" stroke-width="1.5" opacity=".25"/>`).join("")}
      <path d="M-40,${y0}H1120" stroke="${P}" stroke-width="18"/><path d="M-40,${y1}H1120" stroke="${P}" stroke-width="18"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y0 + 8}l21,26l21,-26`).join("")}" fill="${P}"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y1 - 8}l21,-26l21,26`).join("")}" fill="${P}"/>`;
    const rod = (x, y, len = 240) => `<path d="M${x},${y}V${y + len}" stroke="${ROD}" stroke-width="6"/>`;
    const pup = (x, y, inner, rot = 0, pid = "") => `<g class="pup" data-ox="${x}" data-oy="${y}"${pid ? ` id="${pid}"` : ""}>${rod(x, y)}<g transform="translate(${x},${y}) rotate(${rot})">${inner}</g></g>`;
    // the dorm as a puppet: eight floors of lace windows, the seventh floor glowing
    const dorm = (s, fire) => {
      let w = `<rect x="-170" y="-720" width="340" height="720" fill="${P}"/><rect x="-190" y="-740" width="380" height="30" fill="${P}"/>`;
      for (let f = 0; f < 8; f++) for (let c = 0; c < 4; c++) {
        const x = -150 + c * 80, y = -90 - f * 82, lit = f === 6;
        w += `<rect x="${x}" y="${y - 50}" width="50" height="50" fill="${lit && fire ? "#ff9a3a" : CUT}" opacity="${lit && fire ? 1 : 0.85}"/><path d="M${x + 25},${y - 50}V${y}" stroke="${P}" stroke-width="5"/>`;
      }
      return `<g transform="scale(${s})">${w}<rect x="-40" y="-80" width="80" height="80" fill="${CUT}"/><path d="M0,-80V0" stroke="${P}" stroke-width="5"/></g>`;
    };
    const girl = (s, arm = 0) => `<g transform="scale(${s})"><circle cx="0" cy="-200" r="30" fill="${P}"/>${[-22, -8, 6, 20].map((dx, k) => `<path d="M${dx},-226q${k % 2 ? 6 : -6},-14 ${k % 2 ? -2 : 3},-24" stroke="${P}" stroke-width="6" fill="none"/>`).join("")}
      <path d="M-40,-30L-30,-170H30L40,-30Z" fill="${P}"/><path d="M-30,-30L-50,0H50L30,-30Z" fill="${P}"/><ellipse cx="0" cy="-130" rx="8" ry="14" fill="${CUT}"/>
      <path d="M-14,0V30M14,0V30" stroke="${P}" stroke-width="10"/><path d="M28,-160L${60 + arm * 0.2},${-210 - arm}" stroke="${P}" stroke-width="12" stroke-linecap="round"/></g>`;
    const flame = (x, y, s) => `<path class="kfl" d="M${x},${y}c${12 * s},-${20 * s} ${4 * s},-${40 * s} ${16 * s},-${60 * s}c${4 * s},${20 * s} ${18 * s},${30 * s} ${10 * s},${60 * s}z" fill="${P}"/>`;
    let s = LGY.map((y) => screen(y, y + 900)).join("");
    // S1: 2539, the dorm burns
    s += `<text x="540" y="96" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="${P}" opacity=".85">พ.ศ. 2539</text>`;
    s += pup(540, 840, dorm(0.85, true)) + `<g id="${id}-flames">${[-130, -60, 20, 100].map((dx, k) => flame(540 + dx * 0.9, 236 - (k % 2) * 16, 1.4 + (k % 2) * 0.4)).join("")}</g>`;
    // S2: ดาว outside, looking up; the roommate calling from the seventh floor
    const Y2 = LGY[1];
    s += pup(760, Y2 + 820, dorm(0.95, true)) + pup(240, Y2 + 820, girl(1.25, 40)) +
      `<g id="${id}-call">${[0, 1, 2].map((k) => `<path d="M${620 - k * 40},${Y2 + 240 - k * 10}q-30,30 0,60" stroke="${P}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    // S3: ดาว runs back in through the door; the flames rise
    const Y3 = LGY[2];
    s += pup(560, Y3 + 820, dorm(1.0, true)) + `<g id="${id}-go">${pup(300, Y3 + 820, girl(1.15, -40), 18)}</g>` + [-140, -40, 60, 140].map((dx, k) => flame(560 + dx, Y3 + 240 - (k % 2) * 20, 2 + (k % 2) * 0.5)).join("");
    // S4: the roommate escapes down the far stairs; ดาว in the window, still
    const Y4 = LGY[3], WX = 540 - 150 + 80, WY = Y4 + 820 - 90 - 6 * 82 - 50;
    s += pup(540, Y4 + 820, dorm(1.0, false)) + `<g id="${id}-win"><rect x="${WX}" y="${WY}" width="50" height="50" fill="#ff9a3a"/><path d="M${WX + 8},${WY + 50}C${WX + 8},${WY + 30} ${WX + 14},${WY + 26} ${WX + 25},${WY + 26}C${WX + 36},${WY + 26} ${WX + 42},${WY + 30} ${WX + 42},${WY + 50}Z" fill="${P}"/>
      <circle cx="${WX + 25}" cy="${WY + 18}" r="11" fill="${P}"/><ellipse cx="${WX + 21}" cy="${WY + 18}" rx="3" ry="1.6" fill="#ffe6a0"/><ellipse cx="${WX + 29}" cy="${WY + 18}" rx="3" ry="1.6" fill="#ffe6a0"/></g>` +
      pup(880, Y4 + 840, girl(1.1, 0)) + `<path d="M760,${Y4 + 620}L1000,${Y4 + 860}" stroke="${P}" stroke-width="10" stroke-dasharray="30 18"/>`;
    put(L.set, s);
  };


  // ---------------- the street in front of the dorm (1 m ≈ 400 px; a storey is 3 m) ----------------
  // the dorm's face sits on the set layer so people line up with its door: ground-floor door (o.door x, lit from inside), the
  // shop-house windows above, smoke from the top; then the pavement and the road. o.truck: a fire engine (x of its middle);
  // o.sign: the assembly-point sign (x); o.crowd: residents in blankets from x; o.dawn: the sky already going pale
  Sets.street = function (L, o) {
    const id = o.id || "st", r = (() => { let q = o.seed || 41; return () => ((q = (q * 1664525 + 1013904223) % 4294967296) / 4294967296); })(), G = 1500, FL = 1200, D = o.door ?? 380;
    put(L.sky, `<rect x="-2400" y="-5000" width="6000" height="9000" fill="url(#kwNight)"/>`);
    let far = "";
    for (let k = 0; k < 12; k++) { const x = -1600 + k * 380, h = 1400 + r() * 1600; far += `<rect x="${f1(x)}" y="${f1(G - 100 - h)}" width="${f1(260 + r() * 120)}" height="${f1(h)}" fill="#141a26"/>`; }
    put(L.far, far);
    // the building
    let s = `<rect x="-1100" y="${G - 4 * FL - 200}" width="3000" height="${4 * FL + 200}" fill="url(#kwFacade)"/>`;
    for (let f = 0; f < 4; f++) {
      s += `<rect x="-1100" y="${G - f * FL - 40}" width="3000" height="40" fill="#3a3e44"/>`;
      for (let c = 0; c < 7; c++) {
        const x = -900 + c * 420, y = G - f * FL - 820;
        if (f === 0 && Math.abs(x + 130 - D) < 420) continue;
        const lit = r() < 0.3;
        s += `<rect x="${x}" y="${y}" width="260" height="440" fill="${lit ? "#e6c88a" : "#151a22"}" stroke="#2e2a26" stroke-width="6"/><path d="M${x + 130},${y}V${y + 440}" stroke="#3a3f46" stroke-width="10"/><rect x="${x - 16}" y="${y + 430}" width="292" height="26" fill="#3a3e44"/>`;
      }
    }
    // the ground-floor door and the dorm's name above it
    s += `<rect x="${D - 230}" y="${G - 900}" width="460" height="900" fill="#2a2d32"/><rect x="${D - 200}" y="${G - 870}" width="400" height="870" fill="${o.door !== undefined ? "#ffd38a" : "#0e1218"}" opacity="${o.door !== undefined ? 0.8 : 1}"/>
      <path d="M${D},${G - 870}V${G}" stroke="#2a2d32" stroke-width="12"/><rect x="${D - 300}" y="${G - 1100}" width="600" height="140" rx="12" fill="#1d2228"/>
      <text x="${D}" y="${G - 1010}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="72" fill="#ff7aa8" opacity=".9">หอพักสตรี ศรีเพ็ญ</text>`;
    if (o.door !== undefined) s += `<g opacity=".55">${Pov.smoke(r, { x0: D - 200, x1: D + 200, y0: G - 870, y1: G - 300, n: 4, op: 0.5 })}</g>`;
    // smoke rolling off the top floors
    for (let k = 0; k < 12; k++) s += `<g class="smk" data-d="${f1(8 + r() * 20)}"><ellipse cx="${f1(-500 + r() * 2200)}" cy="${f1(G - 4 * FL - 300 + r() * 900)}" rx="${f1(320 + r() * 380)}" ry="${f1(180 + r() * 160)}" fill="url(#pvPuff)" opacity=".9"/></g>`;
    for (let k = 0; k < 7; k++) s += `<g class="smk" data-d="${f1(6 + r() * 14)}"><ellipse cx="${f1(-700 + r() * 2400)}" cy="${f1(G - 2 * FL - 600 + r() * FL)}" rx="${f1(260 + r() * 300)}" ry="${f1(140 + r() * 120)}" fill="url(#pvPuff)" opacity=".45"/></g>`;
    // the pavement, the kerb, the road (wet: the siren light streaks in it)
    s += `<rect x="-2400" y="${G}" width="6000" height="220" fill="#2c2e33"/><rect x="-2400" y="${G + 220}" width="6000" height="30" fill="#4a4c52"/><rect x="-2400" y="${G + 250}" width="6000" height="2600" fill="#1a1c20"/>
      <path d="M-2400,${G + 1100}H3600" stroke="#d8d4c0" stroke-width="18" stroke-dasharray="240 160" opacity=".3"/>`;
    for (let k = 0; k < 10; k++) s += `<ellipse cx="${f1(-900 + r() * 2900)}" cy="${f1(G + 400 + r() * 1400)}" rx="${f1(260 + r() * 300)}" ry="${f1(18 + r() * 16)}" fill="${k % 2 ? "#5a8aff" : "#ff5a4a"}" opacity=".12"/>`;
    s += `<path d="M-1200,${G + 520}C-400,${G + 440} 300,${G + 700} 1100,${G + 560}S2200,${G + 660} 2800,${G + 480}" stroke="#d8a820" stroke-width="34" fill="none"/><path d="M-1200,${G + 980}C-200,${G + 900} 700,${G + 1160} 2000,${G + 1020}" stroke="#c8392b" stroke-width="30" fill="none"/>`;
    if (o.truck !== undefined) s += `<g transform="translate(${o.truck},${G + 760}) scale(4)"><rect x="-260" y="-150" width="520" height="150" rx="16" fill="#c8261c" stroke="#2e2a26" stroke-width="2"/><rect x="120" y="-210" width="140" height="80" rx="10" fill="#c8261c" stroke="#2e2a26" stroke-width="2"/><rect x="140" y="-196" width="100" height="50" fill="#2a3644"/>
      <circle cx="-170" cy="0" r="40" fill="#1a1a1a"/><circle cx="170" cy="0" r="40" fill="#1a1a1a"/><circle cx="-170" cy="0" r="16" fill="#6a6e74"/><circle cx="170" cy="0" r="16" fill="#6a6e74"/><path d="M-240,-120H90" stroke="#e8e8e8" stroke-width="10"/><rect x="-200" y="-200" width="300" height="20" fill="#9aa0a6"/>
      <path d="M-250,-70H110" stroke="#f2c230" stroke-width="6"/><circle class="siren" cx="150" cy="-218" r="14" fill="#ff3a3a"/><circle class="sirenb" cx="220" cy="-218" r="14" fill="#3a7aff"/></g>`;
    if (o.sign !== undefined) s += assembly(o.sign, G + 1500, 2.2);
    if (o.crowd !== undefined) s += residents(o.crowd, G + 1560, 2.0, 5, 250);
    put(L.set, s);
    let gl = "";
    if (o.door !== undefined) gl += `<ellipse cx="${D}" cy="${G + 40}" rx="520" ry="120" fill="#ffd38a" opacity=".25"/>`;
    if (o.truck !== undefined) gl += `<g class="siren"><circle cx="${o.truck + 600}" cy="${G - 120}" r="1500" fill="url(#kwSiren)" opacity=".45"/></g><g class="sirenb"><circle cx="${o.truck + 880}" cy="${G - 120}" r="1500" fill="url(#kwSirenB)" opacity=".45"/></g>`;
    else gl += `<g class="siren"><circle cx="1900" cy="${G}" r="1700" fill="url(#kwSiren)" opacity=".35"/></g><g class="sirenb"><circle cx="2100" cy="${G}" r="1700" fill="url(#kwSirenB)" opacity=".35"/></g>`;
    put(L.glow, gl);
  };
  // ---------------- card icons ----------------
  if (window.GameUI) {
    const K = INK, O = `stroke="${K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`, SH = `<ellipse cx="60" cy="108" rx="34" ry="6" fill="#000" opacity=".18"/>`;
    Object.assign(GameUI.ILL, {
      assembly: `${SH}<path d="M60,104V54" stroke="#8a9096" stroke-width="7"/><rect x="18" y="12" width="84" height="52" rx="8" fill="#2f8a52" ${O}/><g class="a-bob">${[-20, 0, 20].map((dx) => `<circle cx="${60 + dx}" cy="28" r="6" fill="#eaffe8"/><path d="M${52 + dx},52q0,-14 8,-16t8,16z" fill="#eaffe8"/>`).join("")}</g>`,
      staythere: `${SH}<g class="a-pulse"><circle cx="60" cy="56" r="40" fill="#f2c55c" ${O}/></g><path d="M60,30V58L78,70" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M40,100h40" stroke="#3fb86a" stroke-width="7" stroke-linecap="round"/>`,
      tellff: `${SH}<path d="M14,64Q16,30 46,28Q76,30 78,64Z" fill="#f2c230" ${O}/><path d="M6,64H86L80,74H12Z" fill="#d8a820" ${O}/>
        <g class="a-bob"><path d="M84,20h28v26h-14l-8,10v-10h-6z" fill="#fff" ${O}/><text x="98" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="16" fill="#c8392b">714</text></g>`,
    });
  }

  function put(el, html) { el.insertAdjacentHTML("beforeend", html); }
  Object.assign(window.Kwan, { residents, assembly, daoWindow });
})();
