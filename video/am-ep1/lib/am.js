// Sets, props, cast and the ghost for "เต็นท์ผีอำ": a campsite high on a northern doi in the cold season, dome tents in the rain,
// the inside of a tent by lantern and by coal light, a หมูกระทะ charcoal stove, and a ผีอำ that sits on your chest.
// Same layer contract as sets.js (sky / far / mid / set / act / fg, glow above the darkness); seeded RNG only.
//   Rig.CAST: phum (ภูมิ 18, vlogger) · toey (ใบเตย 8, his sister; draw at ~0.72) · oat (โอ๊ต 18) · jaew (น้าแจ๋ว 45) · kaew (ลุงแก้ว 65)
//   Am.ghost(x, y, s, o)   the ผีอำ: a coal-black, gaunt old man in a shawl, all one shape, long thin arms, green eyes (o.sit: squatting)
//   Am.eyes(x, y, s, id)   the eyes alone · Am.stove(x, y, s, o) the หมูกระทะ bucket stove (o.lit coals, o.pan, o.smoke) · Am.tent(...)
//   Sets.doiCamp     the campsite: ridges in mist, pines, dome tents (o.tents [[x, s, {lit, col, id, shadow}]]), plot posts, o.time dusk | night, o.rain
//   Sets.tentIn      inside a dome tent: fabric walls, sleeping mats, o.lamp (lantern on), o.stove x (lit stove), #id-zip door, o.time night | dark
//   Sets.chestPOV    lying on your back: the sleeping bag down the frame, the tent roof, the stove glowing at the feet, o.ghost on the chest
//   Sets.stoveClose  close on the stove: the dome pan, pork, the broth moat, coals below; #id-chop chopsticks
//   Sets.coalDark    black, a few coals glowing on a grate, smoke (#id-smoke) — the opener
//   Sets.coSection   koi-style diagrams on night-blue slate: o.v 1 coal → CO · 2 can't see, can't smell · 3 a closed tent fills · 4 a flap open is not enough
//   Sets.shadowLegend the legend as a shadow play on tent fabric, three full-screen panels (y 0/2000/4000)
//   Sets.campSign    end card: the campsite sign with a note pinned to it
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const ABL = "#0a0c0b", ABL2 = "#171b19", AEYE = ["#7dff6a", "#bfff96", "#f2ffe4"];

  Sets.DEFS += `
    <linearGradient id="amDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a6a"/><stop offset=".5" stop-color="#b86a6a"/><stop offset="1" stop-color="#f2b07a"/></linearGradient>
    <linearGradient id="amNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04060c"/><stop offset=".6" stop-color="#0c1424"/><stop offset="1" stop-color="#16203a"/></linearGradient>
    <linearGradient id="amRain" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07090e"/><stop offset="1" stop-color="#1a2230"/></linearGradient>
    <linearGradient id="amSlate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2836"/><stop offset="1" stop-color="#141c28"/></linearGradient>
    <radialGradient id="amCoal"><stop offset="0" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".35" stop-color="#ff7a2a" stop-opacity=".5"/><stop offset="1" stop-color="#ff5a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="amLamp"><stop offset="0" stop-color="#fff0c0" stop-opacity=".9"/><stop offset=".4" stop-color="#ffd08a" stop-opacity=".25"/><stop offset="1" stop-color="#ffd08a" stop-opacity="0"/></radialGradient>
    <radialGradient id="amTent"><stop offset="0" stop-color="#ffb04a" stop-opacity=".75"/><stop offset=".5" stop-color="#ff8a2a" stop-opacity=".22"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="amGlow"><stop offset="0" stop-color="#7dff6a" stop-opacity=".5"/><stop offset=".4" stop-color="#3dbf5a" stop-opacity=".16"/><stop offset="1" stop-color="#3dbf5a" stop-opacity="0"/></radialGradient>
    <linearGradient id="amFabric" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e88a3a"/><stop offset="1" stop-color="#b85a22"/></linearGradient>
    <linearGradient id="amFabricD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3a26"/><stop offset="1" stop-color="#2e1e14"/></linearGradient>`;

  // ---------------- cast ----------------
  Object.assign(Rig.CAST, {
    phum: { // ภูมิ: 18, vlogger — dark-green hoodie, red knit beanie, jeans, white sneakers
      skin: "#e2b08a", skinS: "#c4906a", top: "#3e6a4e", topS: "#2e5240", sleeve: "#3e6a4e", sleeveS: "#2e5240", forearm: "#3e6a4e", forearmS: "#2e5240",
      pants: "#4a6a9a", pantsS: "#3a5680", shoe: "#f0f0ea", belt: "#3e6a4e",
      torsoExtra: `<path d="M-30,-476Q0,-440 30,-476" stroke="#2e5240" stroke-width="8" fill="none"/><path d="M-12,-460v40M12,-460v40" stroke="#e8e4d8" stroke-width="4"/><rect x="-40" y="-380" width="80" height="34" rx="8" fill="#2e5240" opacity=".8"/>`,
      hair: `<path d="M-48,-566Q-52,-640 0,-646Q52,-640 48,-566Q30,-574 0,-576Q-30,-574 -48,-566Z" fill="#c8342a" ${OUT}/><path d="M-50,-572Q0,-560 50,-572" stroke="#a82820" stroke-width="12" fill="none"/>
        <path d="M-30,-632V-584M-10,-640V-580M10,-640V-580M30,-632V-584" stroke="#a82820" stroke-width="3" opacity=".7"/><circle cx="0" cy="-650" r="14" fill="#e8e4d8" ${OUT3}/>`,
      face: "",
    },
    toey: { // ใบเตย: 8 — pink puffer jacket, two pigtails, white earmuffs, leggings
      skin: "#ecc29c", skinS: "#cfa078", top: "#f08ab0", topS: "#d06a92", sleeve: "#f08ab0", sleeveS: "#d06a92", forearm: "#f08ab0", forearmS: "#d06a92",
      pants: "#6a5a9a", pantsS: "#544880", shoe: "#f4d24a", belt: "#f08ab0",
      torsoExtra: `${[-430, -390, -350].map((y) => `<path d="M-52,${y}Q0,${y + 8} 52,${y}" stroke="#d06a92" stroke-width="4" fill="none"/>`).join("")}`,
      hair: `<path d="M-48,-552Q-52,-614 0,-616Q52,-614 48,-552Q40,-584 0,-588Q-40,-584 -48,-552Z" fill="#3a2418" ${OUT}/>
        <path d="M-50,-560q-40,10 -38,60q14,-20 30,-26z" fill="#3a2418" ${OUT3}/><path d="M50,-560q40,10 38,60q-14,-20 -30,-26z" fill="#3a2418" ${OUT3}/>
        <path d="M-50,-580Q0,-640 50,-580" stroke="#f4f0e8" stroke-width="7" fill="none"/><circle cx="-50" cy="-552" r="18" fill="#f4f0e8" ${OUT3}/><circle cx="50" cy="-552" r="18" fill="#f4f0e8" ${OUT3}/>`,
      face: `<g fill="#e88a8a" opacity=".55"><ellipse cx="-24" cy="-526" rx="8" ry="4"/><ellipse cx="30" cy="-526" rx="8" ry="4"/></g>`,
    },
    oat: { // โอ๊ต: 18 — orange puffer vest over a grey tee, cap on backwards, grey joggers
      skin: "#c98e5e", skinS: "#a87048", top: "#8a8e94", topS: "#6e7278", sleeve: "#8a8e94", sleeveS: "#6e7278", forearm: "#c98e5e", forearmS: "#a87048",
      pants: "#5a5e66", pantsS: "#46494f", shoe: "#2a2a2c", belt: "#5a5e66",
      torsoExtra: `<path d="M-54,-470H-12V-330H-58ZM54,-470H12V-330H58Z" fill="#f08a2a" ${OUT3}/>${[-430, -390, -350].map((y) => `<path d="M-56,${y}H-14M14,${y}H56" stroke="#c86a1a" stroke-width="4"/>`).join("")}`,
      hair: `<path d="M-48,-560Q-50,-616 0,-618Q50,-616 48,-560Q40,-590 0,-592Q-40,-590 -48,-560Z" fill="#2a3a5a" ${OUT}/><path d="M-48,-590q-30,4 -40,18q20,8 44,0z" fill="#2a3a5a" ${OUT3}/><circle cx="0" cy="-618" r="6" fill="#2a3a5a"/>`,
      face: `<path d="M-30,-560q8,-4 14,0M14,-560q8,-4 14,0" stroke="#3a2a20" stroke-width="5" fill="none"/>`,
    },
    jaew: { // น้าแจ๋ว: 45 — purple fleece, a long striped scarf, short bob, reading glasses pushed up
      skin: "#e2b28c", skinS: "#c29470", top: "#7a4a9a", topS: "#62387e", sleeve: "#7a4a9a", sleeveS: "#62387e", forearm: "#7a4a9a", forearmS: "#62387e",
      pants: "#3a3a44", pantsS: "#2c2c34", shoe: "#8a5a3a", belt: "#7a4a9a",
      torsoExtra: `<path d="M-36,-480Q0,-450 36,-480L30,-460Q0,-436 -30,-460Z" fill="#e8c84a" ${OUT3}/><path d="M24,-466L34,-330H14L10,-460Z" fill="#e8c84a" ${OUT3}/>${[-430, -390, -350].map((y) => `<path d="M14,${y}H34" stroke="#c8342a" stroke-width="8"/>`).join("")}`,
      hair: `<path d="M-50,-548Q-56,-618 0,-620Q56,-618 50,-548Q52,-508 40,-500Q42,-560 0,-584Q-42,-560 -40,-500Q-52,-508 -50,-548Z" fill="#4a2e22" ${OUT}/>
        <g fill="none" stroke="#2a2a2a" stroke-width="4"><rect x="-34" y="-606" width="26" height="16" rx="5"/><rect x="8" y="-606" width="26" height="16" rx="5"/></g>`,
      face: `<g fill="#e88a8a" opacity=".5"><ellipse cx="-24" cy="-526" rx="9" ry="5"/><ellipse cx="30" cy="-526" rx="9" ry="5"/></g>`,
    },
    kaew: { // ลุงแก้ว: 65, the campsite keeper — indigo ม่อฮ่อม shirt, a red-checked ผ้าขาวม้า round the neck, grey knit cap, grey stubble
      skin: "#b07a52", skinS: "#8e5e3a", top: "#2a3a5e", topS: "#1e2c48", sleeve: "#2a3a5e", sleeveS: "#1e2c48", forearm: "#2a3a5e", forearmS: "#1e2c48",
      pants: "#2a3a5e", pantsS: "#1e2c48", shoe: "#5a3a26", belt: "#c8342a",
      torsoExtra: `<path d="M-40,-478Q0,-446 40,-478L36,-458Q0,-430 -36,-458Z" fill="#c8342a" ${OUT3}/><path d="M-30,-466l60,0M-26,-456l52,0" stroke="#f4ecd8" stroke-width="3" stroke-dasharray="6 6"/>
        <path d="M-18,-462L-28,-380H-10L-4,-460Z" fill="#c8342a" ${OUT3}/><path d="M0,-470V-320" stroke="#1e2c48" stroke-width="4"/>`,
      hair: `<path d="M-48,-566Q-50,-628 0,-632Q50,-628 48,-566Q30,-574 0,-576Q-30,-574 -48,-566Z" fill="#6a6a70" ${OUT}/><path d="M-50,-572Q0,-560 50,-572" stroke="#55555a" stroke-width="10" fill="none"/>`,
      face: `<path d="M-30,-562q8,-3 14,0M14,-562q8,-3 14,0" stroke="#5a3a26" stroke-width="2.5" fill="none"/><g fill="#8a8a8a" opacity=".5">${Array.from({ length: 14 }, (_, k) => `<circle cx="${-26 + (k % 7) * 9}" cy="${-506 + Math.floor(k / 7) * 8}" r="1.6"/>`).join("")}</g>`,
    },
  });

  // ---------------- the ผีอำ ----------------
  const eyes = (x, y, s, id = "") => `<g ${id ? `id="${id}"` : ""} class="aeye" transform="translate(${f1(x)},${f1(y)}) scale(${s})">${[-22, 22].map((cx) => `<circle cx="${cx}" cy="0" r="22" fill="${AEYE[0]}" opacity=".3"/>
    <path d="M${cx - 13},0Q${cx},-10 ${cx + 13},0Q${cx},6 ${cx - 13},0Z" fill="${AEYE[0]}"/><ellipse cx="${cx}" cy="0" rx="4.5" ry="4" fill="${AEYE[2]}"/>`).join("")}</g>`;
  // a gaunt old man in a shawl, all one coal-black shape; origin at the feet. o.sit: squatting low (on a chest), hands forward
  function ghost(x, y, s, o = {}) {
    const fing = (hx, hy, dir) => [-14, -5, 4, 13].map((d) => `<path d="M${hx},${hy}l${d * 1.3},${30 + Math.abs(d)}l${d * 0.5 + dir * 4},20" stroke="${ABL}" stroke-width="6" fill="none" stroke-linecap="round"/>`).join("");
    const body = o.sit
      ? `<path d="M-120,0Q-140,-90 -90,-150Q-120,-210 -60,-250Q0,-290 60,-250Q120,-210 90,-150Q140,-90 120,0Z" fill="${ABL}"/>
         <path d="M-96,-150Q-60,-190 0,-196Q60,-190 96,-150Q60,-170 0,-172Q-60,-170 -96,-150Z" fill="${ABL2}"/>
         <path d="M-70,-200Q-150,-120 -110,-30" stroke="${ABL}" stroke-width="20" fill="none" stroke-linecap="round"/>${fing(-110, -30, -1)}
         <path d="M70,-200Q150,-120 110,-30" stroke="${ABL}" stroke-width="20" fill="none" stroke-linecap="round"/>${fing(110, -30, 1)}
         <ellipse cx="0" cy="-300" rx="50" ry="58" fill="${ABL}"/><path d="M-56,-300Q-60,-370 0,-372Q60,-370 56,-300Q40,-340 0,-342Q-40,-340 -56,-300Z" fill="${ABL2}"/>`
      : `<path d="M-60,0L-50,-300Q-80,-330 -70,-380Q0,-420 70,-380Q80,-330 50,-300L60,0Z" fill="${ABL}"/>
         <path d="M-90,-370Q0,-420 90,-370L70,-300Q0,-330 -70,-300Z" fill="${ABL2}"/>
         <path d="M-66,-360Q-110,-250 -90,-150" stroke="${ABL}" stroke-width="18" fill="none" stroke-linecap="round"/>${fing(-90, -150, -1)}
         <path d="M66,-360Q110,-250 90,-150" stroke="${ABL}" stroke-width="18" fill="none" stroke-linecap="round"/>${fing(90, -150, 1)}
         <ellipse cx="0" cy="-450" rx="48" ry="56" fill="${ABL}"/>`;
    return `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})" opacity="${o.op ?? 1}">${body}${eyes(0, o.sit ? -300 : -452, 1, o.id ? `${o.id}-eyes` : "")}</g>`;
  }

  // ---------------- props ----------------
  // the หมูกระทะ stove: a charcoal bucket stove (clay lining in a tin bucket) with the domed grill pan and its moat of broth. Origin at its foot.
  function stove(x, y, s, o = {}) {
    const id = o.id || "";
    const coal = o.lit !== false;
    return `<g ${id ? `id="${id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})">
      ${coal ? `<circle cx="0" cy="-120" r="260" fill="url(#amCoal)" opacity=".55"/>` : ""}
      <path d="M-100,-170L-80,0H80L100,-170Z" fill="#8a9298" ${OUT}/><path d="M-100,-170H100" stroke="#6a7278" stroke-width="10"/><path d="M-90,-90H90" stroke="#6a7278" stroke-width="4" opacity=".6"/>
      <path d="M-40,-60H40V-10H-40Z" fill="${coal ? "#2a0e04" : "#2a2422"}" ${OUT3}/>${coal ? `<g class="acoal">${[-24, 0, 24].map((dx, k) => `<ellipse cx="${dx}" cy="-30" rx="14" ry="10" fill="${["#ff7a2a", "#ffb04a", "#ff5a1a"][k]}"/>`).join("")}</g>` : ""}
      ${o.pan !== false ? `<ellipse cx="0" cy="-176" rx="122" ry="26" fill="#cfd4d8" ${OUT}/><ellipse cx="0" cy="-180" rx="96" ry="18" fill="#e6c88a" opacity=".85"/>
        <path d="M-70,-184Q0,-262 70,-184Z" fill="#d8dce0" ${OUT3}/>${Array.from({ length: 5 }, (_, k) => `<path d="M${-48 + k * 24},${-196 - (k % 2) * 14}q10,-8 20,0" stroke="#c8706a" stroke-width="8" fill="none" stroke-linecap="round"/>`).join("")}
        ${[-90, 70].map((dx) => `<path d="M${dx},-182q8,-6 16,0" stroke="#7aa84a" stroke-width="6" fill="none" stroke-linecap="round"/>`).join("")}` : ""}
      ${o.smoke !== false ? `<g class="asmoke" opacity=".55">${[-30, 10, 40].map((dx, k) => `<path d="M${dx},-230q-24,-60 6,-120q24,-50 -6,-110" stroke="#d8dce0" stroke-width="${10 - k * 2}" fill="none" stroke-linecap="round" opacity="${0.5 - k * 0.1}"/>`).join("")}</g>` : ""}
    </g>`;
  }
  const lantern = (x, y, s, o = {}) => `<g ${o.id ? `id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M0,-80V-40" stroke="${INK}" stroke-width="4"/><path d="M-22,-40h44v12h-44z" fill="#3a3a3a"/>
    <rect x="-18" y="-28" width="36" height="52" rx="8" fill="${o.on === false ? "#4a5054" : "#fff2c8"}" ${OUT3}/><path d="M-22,24h44v10h-44z" fill="#3a3a3a"/></g>`;
  const bottle = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-22,0V-90Q-22,-110 -10,-118V-150H10V-118Q22,-110 22,-90V0Z" fill="#e8f2f0" opacity=".9" ${OUT3}/><rect x="-22" y="-80" width="44" height="40" fill="#c8342a"/><rect x="-10" y="-158" width="20" height="10" fill="#3a3a3a"/></g>`;
  // a dome tent from the side; origin at the ground, centre. o.lit: lit from inside; o.door open | closed; o.shadow: a figure's shadow on the wall
  function tent(x, G, s, o = {}) {
    const id = o.id || "", col = o.col || "#e8823a", sh = o.colS || "#b85a22";
    const lit = o.lit;
    let t = `<g ${id ? `id="${id}"` : ""} transform="translate(${f1(x)},${f1(G)}) scale(${s})">
      <path d="M-300,0L-330,30M300,0L330,30M-200,-200L-380,10M200,-200L380,10" stroke="#9a9a8a" stroke-width="3" opacity=".7"/>
      <path d="M-270,0Q-262,-250 0,-300Q262,-250 270,0Z" fill="${lit ? "#ffb05a" : col}" ${OUT}/>
      <path d="M-270,0Q-150,-180 0,-300M270,0Q150,-180 0,-300" stroke="${lit ? "#e8823a" : sh}" stroke-width="10" fill="none"/>
      <path d="M-120,0Q-112,-190 0,-214Q112,-190 120,0Z" fill="${lit ? "#ffd08a" : sh}" ${OUT3}/>`;
    if (o.door === "open") t += `<path d="M-10,0Q-6,-150 0,-214Q-90,-180 -120,0Z" fill="${lit ? "#ff9a3a" : "#7a3a16"}" opacity=".9"/><path d="M0,-214V0" stroke="${INK}" stroke-width="3"/>`;
    else t += `<path d="M0,-214V0" stroke="#3a3a3a" stroke-width="4"/><circle cx="0" cy="-120" r="6" fill="#d8d8d0" ${OUT3}/>`;
    if (o.shadow) t += `<g ${id ? `id="${id}-shadow"` : ""} opacity="${o.shadowOp ?? 0.85}"><path d="M60,0Q40,-80 70,-130Q50,-170 90,-200Q140,-210 150,-160Q170,-110 150,-60Q160,-20 150,0Z" fill="#3a1a0a"/><ellipse cx="118" cy="-206" rx="30" ry="34" fill="#3a1a0a"/>
      <path d="M90,-150Q20,-150 -40,-110" stroke="#3a1a0a" stroke-width="12" fill="none" stroke-linecap="round"/>${[-8, 0, 8].map((d) => `<path d="M-40,-110l-${20 + Math.abs(d)},${d * 2}" stroke="#3a1a0a" stroke-width="5" stroke-linecap="round"/>`).join("")}</g>`;
    if (o.num) t += `<g transform="translate(330,0)"><rect x="-8" y="-120" width="16" height="120" fill="#6a4a30" ${OUT3}/><rect x="-40" y="-170" width="80" height="60" rx="6" fill="#e8d8b0" ${OUT3}/><text x="0" y="-126" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="44" fill="#c8342a">${o.num}</text></g>`;
    return t + "</g>";
  }
  const tentGlow = (x, G, s) => `<ellipse cx="${f1(x)}" cy="${f1(G - 140 * s)}" rx="${f1(420 * s)}" ry="${f1(300 * s)}" fill="url(#amTent)"/>`;
  function pine(x, G, s, c) {
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})" fill="${c}"><rect x="-10" y="-60" width="20" height="60"/>${[0, 1, 2, 3].map((k) => `<path d="M${-110 + k * 18},${-50 - k * 110}L0,${-200 - k * 110}L${110 - k * 18},${-50 - k * 110}Z"/>`).join("")}</g>`;
  }

  // ---------------- the campsite ----------------
  function sky(L, o, r) {
    const t = o.time || "dusk";
    let s = `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#${t === "night" ? (o.rain ? "amRain" : "amNight") : "amDusk"})"/>`;
    if (t === "night" && !o.rain) {
      for (let i = 0; i < 70; i++) s += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-600 + r() * 1300)}" r="${f1(1 + r() * 2.2)}" fill="#e8ecff" opacity="${(0.25 + r() * 0.6).toFixed(2)}"/>`;
    }
    if (t === "dusk") s += `<circle cx="${o.sunX ?? 760}" cy="760" r="90" fill="#ffe2a8" opacity=".85"/><circle cx="${o.sunX ?? 760}" cy="760" r="240" fill="#ffd08a" opacity=".15"/>`;
    put(L.sky, s);
  }
  function ridges(L, G, t) {
    const c = t === "night" ? ["#0e1626", "#0a101c", "#070b14"] : ["#7a6a8a", "#5a4a6e", "#3e3456"];
    put(L.far, `<path d="M-1200,${G - 520}Q-800,${G - 760} -400,${G - 600}T400,${G - 700}T1200,${G - 560}T2300,${G - 640}V${G}H-1200Z" fill="${c[0]}"/>
      <rect x="-1200" y="${G - 600}" width="3500" height="120" fill="${t === "night" ? "#2a3446" : "#e8c8c0"}" opacity=".25"/>
      <path d="M-1200,${G - 380}Q-700,${G - 560} -200,${G - 440}T800,${G - 500}T1800,${G - 400}T2400,${G - 450}V${G}H-1200Z" fill="${c[1]}"/>
      <rect x="-1200" y="${G - 430}" width="3500" height="90" fill="${t === "night" ? "#2a3446" : "#f0d8d0"}" opacity=".3"/>`);
    return c[2];
  }
  function doiCamp(L, o = {}) {
    const id = o.id || "dc", G = o.ground ?? 1400, t = o.time || "dusk", r = mk(o.seed || 211);
    sky(L, o, r);
    const pc = ridges(L, G, t);
    let m = "";
    for (let k = 0; k < 14; k++) m += pine(-1100 + k * 260 + r() * 80, G - 120 - r() * 60, 0.9 + r() * 0.6, pc);
    put(L.mid, m + `<rect x="-1200" y="${G - 160}" width="3500" height="200" fill="${t === "night" ? "#1e2a3a" : "#e0c0b8"}" opacity=".22" class="amist"/>`);
    let s = `<rect x="-1200" y="${G}" width="3500" height="1400" fill="${t === "night" ? "#1e2a1e" : "#5a7a4a"}"/>${Array.from({ length: 60 }, () => { const gx = -1200 + r() * 3500, gy = G + 10 + r() * 600; return `<path d="M${f1(gx)},${f1(gy)}l-6,-20M${f1(gx + 8)},${f1(gy)}l2,-24M${f1(gx + 14)},${f1(gy)}l8,-18" stroke="${t === "night" ? "#2e3e2a" : "#7a9a5a"}" stroke-width="4"/>`; }).join("")}`;
    let g = "";
    (o.tents || []).forEach(([x, sc, to = {}]) => { s += tent(x, G, sc, to); if (to.lit) g += tentGlow(x, G, sc); });
    if (o.sign) s += `<g transform="translate(${o.sign},${G})"><rect x="-10" y="-260" width="20" height="260" fill="#5a3a26" ${OUT3}/><rect x="190" y="-260" width="20" height="260" fill="#5a3a26" ${OUT3}/>
      <rect x="-40" y="-330" width="280" height="110" rx="10" fill="#c8a066" ${OUT}/><text x="100" y="-288" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#3a2414">ลานกางเต็นท์</text>
      <text x="100" y="-244" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#5a3a20">ดอยหมอกมุง</text></g>`;
    if (o.stoveOut != null) { s += stove(o.stoveOut, G + 20, 0.7, { id: `${id}-stove`, smoke: false }); }
    if (o.table != null) s += `<g transform="translate(${o.table},${G})"><rect x="-150" y="-150" width="300" height="20" fill="#8a6a44" ${OUT3}/><path d="M-130,-130L-150,0M130,-130L150,0" stroke="#6a4a30" stroke-width="10"/></g>`;
    put(L.set, s);
    if (g) put(L.glow, g);
    if (o.rain) put(L.fg, `<g class="arain" opacity=".55">${Array.from({ length: 90 }, () => { const rx = -300 + r() * 1700, ry = -900 + r() * 2900; return `<path d="M${f1(rx)},${f1(ry)}l-14,60" stroke="#a8c0d8" stroke-width="3"/>`; }).join("")}</g>`);
  }

  // ---------------- inside a dome tent ----------------
  function tentIn(L, o = {}) {
    const id = o.id || "ti", G = o.ground ?? 1480, dark = o.time === "dark";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="${dark ? "#0c0806" : "#2a160c"}"/>`);
    // the fabric: a dome seen from inside, seams converging overhead
    let s = `<path d="M-700,${G}Q-640,${G - 1500} 540,${G - 1620}Q1720,${G - 1500} 1780,${G}Z" fill="${dark ? "url(#amFabricD)" : "url(#amFabric)"}"/>
      ${[-300, 140, 540, 940, 1380].map((x) => `<path d="M${x},${G}Q${540 + (x - 540) * 0.4},${G - 1300} 540,${G - 1620}" stroke="${dark ? "#1e120a" : "#a84a18"}" stroke-width="8" fill="none"/>`).join("")}
      <path d="M-700,${G - 520}Q540,${G - 760} 1780,${G - 520}" stroke="${dark ? "#1e120a" : "#a84a18"}" stroke-width="6" fill="none" opacity=".6"/>
      <g id="${id}-zip"><path d="M1180,${G}Q1200,${G - 560} 1320,${G - 760}Q1450,${G - 560} 1470,${G}Z" fill="${dark ? "#2a1a10" : "#c8682a"}" ${OUT3}/><path d="M1325,${G - 760}V${G}" stroke="#3a3a3a" stroke-width="5" stroke-dasharray="6 4"/>
        <circle cx="1325" cy="${G - 420}" r="9" fill="#d8d8d0" ${OUT3}/></g>
      <rect x="-1200" y="${G}" width="3500" height="1200" fill="${dark ? "#1a120c" : "#5a3a24"}"/>`;
    // sleeping mats along the floor
    s += [[-160, "#3a6aa8"], [260, "#a83a5a"], [680, "#4a8a5a"], [1100, "#6a5a9a"]].map(([x, c]) => `<rect x="${x - 190}" y="${G - 30}" width="380" height="60" rx="26" fill="${dark ? "#2a2420" : c}" ${OUT3}/>`).join("");
    if (o.bottle) s += bottle(o.bottle, G - 20, 0.9);
    put(L.set, s);
    let g = "";
    if (o.lamp !== false && !dark) { put(L.set, lantern(540, G - 1120, 1.4, { id: `${id}-lamp` })); g += `<circle cx="540" cy="${G - 1110}" r="520" fill="url(#amLamp)" opacity=".65"/>`; }
    if (o.stove != null) { put(L.act, stove(o.stove, G + 10, o.stoveS ?? 1.0, { id: `${id}-stove`, pan: o.pan, smoke: o.smoke })); g += `<circle cx="${o.stove}" cy="${G - 120}" r="${dark ? 520 : 380}" fill="url(#amCoal)" opacity="${dark ? 0.7 : 0.4}" class="aglow"/>`; }
    if (g) put(L.glow, g);
  }

  // ---------------- POV: lying on your back ----------------
  function chestPOV(L, o = {}) {
    const id = o.id || "cp";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#0a0604"/>`);
    // the tent roof overhead, the seams converging to the top
    let s = `<path d="M-400,-200H1480V1300H-400Z" fill="url(#amFabricD)"/>${[-200, 180, 540, 900, 1280].map((x) => `<path d="M${x},1300Q${540 + (x - 540) * 0.3},400 540,-200" stroke="#1e120a" stroke-width="10" fill="none"/>`).join("")}`;
    // the stove at the feet, far end, glowing
    if (o.stove !== false) s += `<circle cx="${o.stoveX ?? 700}" cy="860" r="520" fill="url(#amCoal)" opacity=".9" class="aglow"/>` + stove(o.stoveX ?? 700, 940, 0.5, { id: `${id}-stove`, smoke: true });
    put(L.set, s);
    // the sleeping bag: your own body down the frame, the zip, your hands
    let b = `<path d="M-200,2100Q-120,1500 240,1260Q540,1150 840,1260Q1200,1500 1280,2100Z" fill="#2a3a6a" ${OUT}/><path d="M540,1180V2100" stroke="#1a2448" stroke-width="10"/>
      ${[1360, 1520, 1700].map((y) => `<path d="M${-60 + (y - 1260) * 0.2},${y}Q540,${y - 90} ${1140 - (y - 1260) * 0.2},${y}" stroke="#1a2448" stroke-width="6" fill="none"/>`).join("")}`;
    if (o.ghost !== false) b += `<g id="${id}-ghost" opacity="${o.ghostOp ?? 1}">${ghost(540, 1560, 2.2, { sit: true, id: `${id}-g` })}</g>`;
    put(L.act, b);
  }

  // ---------------- close on the stove ----------------
  function stoveClose(L, o = {}) {
    const id = o.id || "sc", G = 1500;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2a160c"/>`);
    put(L.set, `<rect x="-1200" y="${G}" width="3500" height="1200" fill="#5a3a24"/><path d="M-700,${G}Q540,${G - 2400} 1780,${G}" fill="url(#amFabric)" opacity=".5"/>${stove(540, G + 40, 3.2, { id: `${id}-stove` })}`);
    put(L.glow, `<circle cx="540" cy="${G - 300}" r="700" fill="url(#amCoal)" opacity=".35" class="aglow"/>`);
    put(L.act, `<g id="${id}-chop"><path d="M1300,${G - 1200}L560,${G - 700}M1330,${G - 1170}L590,${G - 680}" stroke="#d8b878" stroke-width="16" stroke-linecap="round"/><path d="M548,${G - 712}q20,-14 40,0" stroke="#c8706a" stroke-width="22" fill="none" stroke-linecap="round"/></g>`);
  }

  // ---------------- the opener: coals in the dark ----------------
  function coalDark(L, o = {}) {
    const id = o.id || "cd", G = 1500, r = mk(o.seed || 77);
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#050302"/>`);
    let s = `<path d="M60,${G - 40}H1020" stroke="#3a3a3a" stroke-width="12"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${100 + k * 110},${G - 60}V${G - 20}" stroke="#2a2a2a" stroke-width="8"/>`).join("")}`;
    let c = "";
    for (let k = 0; k < 14; k++) { const cx = 160 + r() * 760, cy = G - 30 - r() * 90; c += `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(40 + r() * 30)}" ry="${f1(24 + r() * 14)}" fill="${["#2a0e04", "#ff7a2a", "#ffb04a", "#ff5a1a"][k % 4]}" ${OUT3}/>`; }
    put(L.set, s + `<g class="acoal">${c}</g>`);
    put(L.glow, `<circle cx="540" cy="${G - 60}" r="620" fill="url(#amCoal)" opacity=".8" class="aglow"/>`);
    put(L.act, `<g id="${id}-smoke" class="asmoke" opacity=".6">${[300, 460, 620, 780].map((x, k) => `<path d="M${x},${G - 120}q-60,-200 20,-400q70,-200 -20,-420q-60,-160 20,-300" stroke="#c8ccd0" stroke-width="${26 - k * 4}" fill="none" stroke-linecap="round" opacity="${0.35 - k * 0.05}"/>`).join("")}</g>`);
  }

  // ---------------- diagrams ----------------
  function coSection(L, o = {}) {
    const id = o.id || "co", v = o.v || 1, F = 1300;
    const T = (x, y, t, c = "#f4ecd8", sz = 40, i = "") => `<text ${i ? `id="${i}"` : ""} x="${x}" y="${y}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="${sz}" fill="${c}" stroke="#141c28" stroke-width="8" paint-order="stroke" ${i ? 'opacity="0"' : ""}>${t}</text>`;
    const X = (x, y, i, r = 70) => `<g id="${i}" opacity="0" transform="translate(${x},${y})"><circle r="${r}" fill="none" stroke="#e0362c" stroke-width="12"/><path d="M${-r * 0.7},${-r * 0.7}L${r * 0.7},${r * 0.7}" stroke="#e0362c" stroke-width="12" stroke-linecap="round"/></g>`;
    const mol = (x, y, i) => `<g ${i ? `id="${i}"` : ""} transform="translate(${f1(x)},${f1(y)})"><circle cx="-16" cy="0" r="24" fill="#5a5a60" ${OUT3}/><circle cx="18" cy="0" r="20" fill="#e85a4a" ${OUT3}/>
      <text x="-16" y="9" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="24" fill="#fff">C</text><text x="18" y="8" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="22" fill="#fff">O</text></g>`;
    // the tent in cross-section: a dome, two sleepers, the stove
    const tentX = (fill = true, flap = false) => `<path d="M140,${F}Q150,${F - 620} 540,${F - 700}Q930,${F - 620} 940,${F}Z" fill="#2a3446" stroke="#e8823a" stroke-width="10"/>
      ${flap ? `<path d="M860,${F}Q890,${F - 220} 930,${F - 260}L990,${F - 140}Q960,${F - 60} 960,${F}Z" fill="#141c28" stroke="#e8823a" stroke-width="8"/>` : ""}
      ${[300, 440].map((x) => `<g transform="translate(${x},${F - 40})"><rect x="-70" y="-24" width="140" height="44" rx="20" fill="#3a6aa8" ${OUT3}/><circle cx="-60" cy="-26" r="24" fill="#e2b08a" ${OUT3}/></g>`).join("")}
      ${stove(700, F - 6, 0.6, { smoke: false })}`;
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="url(#amSlate)"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1100 + k * 100},-800V2800M-1200,${-700 + k * 100}H2300" stroke="#26324a" stroke-width="2"/>`).join("")}`);
    let s = `<path d="M-600,${F}H1700" stroke="#5a4a3a" stroke-width="14"/>`, a = "";
    if (v === 1) {
      // burning charcoal gives off CO: coals in a stove, molecules rising out of it
      a += `<g id="${id}-coal">${stove(540, F, 1.6, { pan: false, smoke: false })}${T(540, F + 80, "ถ่านที่ติดไฟ", "#ffb04a", 44)}</g>`;
      a += Array.from({ length: 6 }, (_, k) => mol(380 + (k % 3) * 160, F - 520 - Math.floor(k / 3) * 210 - (k % 2) * 40, `${id}-m${k}`)).join("");
      a += `<g id="${id}-lab" opacity="0">${T(540, 480, "คาร์บอนมอนอกไซด์", "#ff8a7a", 64)}${T(540, 400, "แก๊สพิษ", "#f4ecd8", 44)}</g>`;
    } else if (v === 2) {
      // can't see it, can't smell it: an eye and a nose, each crossed out; the gas drawn dotted, faint
      a += `<g id="${id}-gas" opacity=".35">${Array.from({ length: 40 }, (_, k) => `<circle cx="${140 + (k % 10) * 90}" cy="${F - 900 + Math.floor(k / 10) * 160 + (k % 3) * 20}" r="10" fill="#a8b0c0"/>`).join("")}</g>
        <g id="${id}-t0" transform="translate(300,${F - 420})"><path d="M-130,0Q0,-110 130,0Q0,110 -130,0Z" fill="#f4ecd8" ${OUT}/><circle r="44" fill="#2a3a4a"/><circle cx="12" cy="-12" r="12" fill="#fff"/></g>${T(300, F - 250, "มองไม่เห็น", "#f4ecd8", 44)}${X(300, F - 420, `${id}-x0`, 150)}
        <g id="${id}-t1" transform="translate(780,${F - 420})"><path d="M-20,-140Q-30,-40 -80,30Q-60,70 0,60Q60,70 80,30Q30,-40 20,-140Z" fill="#e2b08a" ${OUT}/><ellipse cx="-30" cy="44" rx="14" ry="9" fill="#8a5a3a"/><ellipse cx="30" cy="44" rx="14" ry="9" fill="#8a5a3a"/>
          ${[-40, 0, 40].map((d) => `<path d="M${d},120q-16,30 0,60q16,30 0,60" stroke="#a8b0c0" stroke-width="6" fill="none" opacity=".6"/>`).join("")}</g>${T(780, F - 250, "ไม่มีกลิ่น", "#f4ecd8", 44)}${X(780, F - 420, `${id}-x1`, 150)}`;
    } else if (v === 3 || v === 4) {
      // a closed tent fills with it from the floor up (#id-level grows); 4: the flap is open and it still fills
      a += `<defs><clipPath id="${id}-clip"><path d="M140,${F}Q150,${F - 620} 540,${F - 700}Q930,${F - 620} 940,${F}Z"/></clipPath></defs>${tentX(true, v === 4)}
        <g clip-path="url(#${id}-clip)"><rect id="${id}-level" x="100" y="${F - 700}" width="880" height="700" fill="#e85a4a" opacity=".38"/></g>
        ${Array.from({ length: 10 }, (_, k) => mol(220 + (k % 5) * 150, F - 140 - Math.floor(k / 5) * 200, `${id}-m${k}`)).join("")}
        ${T(540, F + 80, v === 3 ? "เต็นท์ที่ปิดอยู่" : "แง้มประตูไว้", "#f4ecd8", 44)}`;
      if (v === 4) a += `<g id="${id}-arrow" opacity="0"><path d="M980,${F - 200}q90,-40 120,-140" stroke="#9ae68a" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M1080,${F - 380}l26,40l-46,4z" fill="#9ae68a"/></g>
        ${T(540, 420, "ก็ไม่พอ", "#ff8a7a", 80, `${id}-no`)}`;
      else a += T(540, 420, "สะสมเร็วมาก", "#ff8a7a", 72, `${id}-no`);
    }
    put(L.set, s + a);
  }

  // ---------------- the legend: a shadow play on tent fabric, lit by a torch ----------------
  function shadowLegend(L, o = {}) {
    const P = "#1e0e04", H = 1920;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="6600" fill="#120a06"/>`);
    const screen = (y0) => `<rect x="-60" y="${y0}" width="1200" height="${H}" fill="#e88a3a"/><circle cx="540" cy="${y0 + 960}" r="760" fill="#ffd08a" opacity=".45"/>${Array.from({ length: 6 }, (_, k) => `<path d="M${-60 + k * 240},${y0}V${y0 + H}" stroke="#b85a22" stroke-width="6" opacity=".5"/>`).join("")}
      <path d="M-60,${y0 + 260}Q540,${y0 + 120} 1140,${y0 + 260}" stroke="#b85a22" stroke-width="6" fill="none" opacity=".5"/>`;
    const tentS = (x, y, sc) => `<path transform="translate(${x},${y}) scale(${sc})" d="M-270,0Q-262,-250 0,-300Q262,-250 270,0Z" fill="${P}"/>`;
    const sleeper = (x, y, sc) => `<g transform="translate(${x},${y}) scale(${sc})" fill="${P}"><rect x="-200" y="-40" width="400" height="44" rx="20"/><circle cx="-200" cy="-50" r="40"/></g>`;
    const ground = (y) => `<rect x="-60" y="${y}" width="1200" height="40" fill="${P}"/>`;
    let s = "";
    // 1: a tent at plot nine, smoke curling out of it
    s += screen(0) + ground(1300) + tentS(500, 1300, 1.5) + `<path d="M500,800q-40,-90 10,-180q40,-70 -10,-150" stroke="${P}" stroke-width="18" fill="none" stroke-linecap="round" opacity=".7"/>
      <rect x="850" y="1080" width="16" height="220" fill="${P}"/><rect x="796" y="1000" width="124" height="86" rx="6" fill="${P}"/><text x="858" y="1066" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="62" fill="#e88a3a">9</text>`;
    // 2: inside — sleepers, and something squatting on one of them
    s += screen(2000) + ground(3300) + sleeper(380, 3290, 1.4) + sleeper(780, 3290, 1.4) + `<g transform="translate(380,3250)">${ghost(0, 0, 1.2, { sit: true }).replace(/fill="#0a0c0b"|fill="#171b19"/g, `fill="${P}"`)}</g>`;
    // 3: morning — the tent zipped shut, a pair of feet that do not move, two candles
    s += screen(4000) + ground(5300) + tentS(540, 5300, 1.5) + `<path d="M470,5300q10,-60 30,-80q20,20 10,80zM570,5300q10,-60 30,-80q20,20 10,80z" fill="${P}"/>${[150, 930].map((x) => `<rect x="${x - 10}" y="5120" width="20" height="180" fill="${P}"/><path d="M${x},5120q-16,-30 0,-56q16,26 0,56z" fill="#fff3c8"/>`).join("")}`;
    put(L.set, s);
  }

  // ---------------- end card: the campsite sign ----------------
  function campSign(L, o = {}) {
    const id = o.id || "cs", r = mk(o.seed || 523);
    sky(L, { time: o.time || "dusk" }, r);
    ridges(L, 1500, o.time || "dusk");
    put(L.mid, `<rect x="-1200" y="1500" width="3500" height="1200" fill="#3a4a30"/>`);
    let s = `<rect x="250" y="900" width="40" height="1200" fill="#5a3a26" ${OUT}/><rect x="790" y="900" width="40" height="1200" fill="#5a3a26" ${OUT}/>`;
    s += `<g id="${id}-sign" transform="rotate(-2 540 900)"><rect x="150" y="560" width="780" height="560" rx="18" fill="#c8a066" ${OUT}/><rect x="180" y="590" width="720" height="500" rx="10" fill="none" stroke="#8a6438" stroke-width="8"/>
      <text x="540" y="680" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="56" fill="#3a2414">ลานกางเต็นท์ดอยหมอกมุง</text>
      <text x="540" y="750" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="38" fill="#5a3a20">หนาวแค่ไหน… ถ่านไฟอย่าเข้าเต็นท์</text>
      <g transform="translate(300,1010) scale(.5)">${tent(0, 0, 1, { col: "#e8823a" })}</g>
      <g transform="rotate(4 620 920)"><rect x="440" y="800" width="400" height="240" fill="#f4ecd8" ${OUT3}/><circle cx="640" cy="808" r="12" fill="#c8342a"/>
        <text x="640" y="880" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="36" fill="#c8342a">${o.ep || "ตอนที่ 2"}</text>
        <text x="640" y="950" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="${INK}">${o.title || ""}</text>
        <text x="780" y="1016" text-anchor="end" font-family="Kanit" font-weight="500" font-size="24" fill="#5a4a3a">— ลุงแก้ว</text></g></g>`;
    put(L.set, s);
  }

  // ---------------- motion ----------------
  function life(tl, scope, t0, dur) {
    const q = (c) => Array.from(document.querySelectorAll(`${scope} ${c}`));
    q(".asmoke").forEach((el, i) => tl.fromTo(el, { opacity: 0.35 }, { opacity: 0.7, duration: 1.4, repeat: Math.ceil(dur / 1.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.3));
    q(".acoal").forEach((el) => tl.fromTo(el, { opacity: 0.75 }, { opacity: 1, duration: 0.22, repeat: Math.ceil(dur / 0.22), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".aglow").forEach((el) => tl.fromTo(el, { opacity: 0.55 }, { opacity: 0.8, duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".arain").forEach((el) => tl.fromTo(el, { y: -120 }, { y: 0, duration: 0.3, repeat: Math.ceil(dur / 0.3), ease: "none", immediateRender: false }, t0));
    q(".amist").forEach((el) => tl.fromTo(el, { x: 0 }, { x: 80, duration: dur, ease: "none", immediateRender: false }, t0));
  }

  Object.assign(Sets, { doiCamp, tentIn, chestPOV, stoveClose, coalDark, coSection, shadowLegend, campSign });
  window.Am = { ghost, eyes, stove, tent, lantern, bottle, pine, life, ABL, AEYE };
})();
