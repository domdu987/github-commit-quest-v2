// Sets and props for เอาชีวิตรอด 99 วัน EP.8 "ยาตู้เย็น" (on top of estate.js + estate7.js): the estate's medicine fridge dead after
// the storm (seen from inside its open door, shelves of boxes, เจ๊หงส์'s insulin with her name on tape, the thermometer strip on the
// door), the same red-cross fridge in the canteen with its door open, คุณวิน's office from inside at night (the bar fridge still cold
// on his reserved power, the frosted door pane a guard's torch comes up behind), the dark field outside the fence, ปั้น's drawing of
// everyone wading through a flooded field, the storm damage in the yard (a cracked solar array, a fallen branch), hand props.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const O = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const T = (x, y, txt, size, col, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 900}" font-size="${size}" fill="${col}"${o.extra || ""}>${txt}</text>`;

  Sets.DEFS += `
    <linearGradient id="iLiner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#46505c"/><stop offset=".6" stop-color="#323a45"/><stop offset="1" stop-color="#242a33"/></linearGradient>
    <linearGradient id="iLinerSide" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a313a"/><stop offset="1" stop-color="#3a434e"/></linearGradient>
    <linearGradient id="iDoor" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9dcd8"/><stop offset="1" stop-color="#aeb3b0"/></linearGradient>
    <radialGradient id="iCold"><stop offset="0" stop-color="#e8f6ff" stop-opacity=".9"/><stop offset=".35" stop-color="#bfe2ff" stop-opacity=".35"/><stop offset="1" stop-color="#bfe2ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="iColdBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfeaff" stop-opacity=".42"/><stop offset="1" stop-color="#cfeaff" stop-opacity="0"/></linearGradient>
    <linearGradient id="iGlass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e9f3f6" stop-opacity=".9"/><stop offset=".45" stop-color="#cfe2e8" stop-opacity=".55"/><stop offset="1" stop-color="#9fb8c0" stop-opacity=".85"/></linearGradient>
    <radialGradient id="tSpot"><stop offset="0" stop-color="#fff6d8" stop-opacity=".95"/><stop offset=".3" stop-color="#ffe9a8" stop-opacity=".5"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
    <linearGradient id="tBeamH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff2c0" stop-opacity=".55"/><stop offset="1" stop-color="#fff2c0" stop-opacity="0"/></linearGradient>
    <radialGradient id="nMoon"><stop offset="0" stop-color="#f4f8ff" stop-opacity=".9"/><stop offset=".2" stop-color="#cfdcf0" stop-opacity=".35"/><stop offset="1" stop-color="#cfdcf0" stop-opacity="0"/></radialGradient>
    <linearGradient id="nWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26324a"/><stop offset="1" stop-color="#121a28"/></linearGradient>
    <linearGradient id="oWarmWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6e4e"/><stop offset=".55" stop-color="#6e5640"/><stop offset="1" stop-color="#4a3a2c"/></linearGradient>`;

  // ======================================================================================================
  // props
  // ======================================================================================================
  // a box of insulin vials: white carton, a blue band, "อินซูลิน · 10 มล.", a strip of tape with the owner's name in marker;
  // origin = bottom centre (~110 × 150 front face + a side going back)
  function INSULIN(id = "", o = {}) {
    const I = id ? ` id="${id}"` : "", name = o.name ?? "หงส์";
    return `<g${I}><path d="M55,0L80,-18V-168L55,-150Z" fill="#c9cfd2" ${O(3)}/><path d="M-55,-150L-30,-168H80L55,-150Z" fill="#eef1f2" ${O(3)}/>
      <rect x="-55" y="-150" width="110" height="150" fill="#f7f9f9" ${O(3)}/><rect x="-55" y="-118" width="110" height="34" fill="#2f6fb8"/>${T(0, -94, "อินซูลิน", 21, "#fff")}
      ${T(0, -58, "10 มล.", 18, "#2f4a8a", { w: 700 })}<path d="M-44,-36h88M-44,-26h60" stroke="#9aa0a6" stroke-width="2.5"/><path d="M30,-140l10,10l-10,10l-10,-10z" fill="#c8392b"/>
      ${name ? `<g transform="rotate(-6 0 -140)"><rect x="-46" y="-152" width="70" height="22" fill="#efe2a8" opacity=".95" ${O(1.5)}/>${T(-11, -135, name, 17, "#1e2a5a", { w: 700 })}</g>` : ""}</g>`;
  }
  // an insulin vial: a short clear glass bottle, the liquid, a white label with a blue band, an aluminium crimp and a coloured cap;
  // origin = bottom centre (~44 × 96)
  function VIAL(id = "", o = {}) {
    const I = id ? ` id="${id}"` : "", cap = o.cap || "#e08a2a";
    return `<g${I}><path d="M-20,-4Q-22,0 -16,0H16Q22,0 20,-4V-62Q20,-70 12,-72V-78H-12V-72Q-20,-70 -20,-62Z" fill="url(#iGlass)" ${O(2.5)}/><path d="M-17,-6V-56H17V-6Z" fill="#dcecf2" opacity=".55"/>
      <rect x="-20" y="-52" width="40" height="30" fill="#f7f9f9" ${O(1.5)}/><rect x="-20" y="-44" width="40" height="9" fill="#2f6fb8"/><rect x="-14" y="-90" width="28" height="13" rx="2" fill="#b9c0c6" ${O(2)}/><rect x="-16" y="-98" width="32" height="10" rx="3" fill="${cap}" ${O(2)}/>
      <path d="M-13,-62V-10" stroke="#fff" stroke-width="4" opacity=".7" stroke-linecap="round"/></g>`;
  }
  // a fridge thermometer strip: a white card, ticks 0–40 °C, a red column (#id-col: its height is set by the shot, 7 px per degree),
  // the 2–8 band in blue, above 30 in red; origin = bottom centre of the scale (0 °C), ~70 × 330
  function THERMO(id, o = {}) {
    const deg = o.deg ?? 6, P = 7;
    return `<g id="${id}"><rect x="-34" y="-318" width="68" height="350" rx="10" fill="#f4f2ea" ${O(3)}/><rect x="-6" y="${-14 * P}" width="12" height="${6 * P}" fill="#9fd0f0"/><rect x="-6" y="${-40 * P}" width="12" height="${10 * P}" fill="#f2b6a8"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M-6,${-k * 5 * P}h${k % 2 ? -8 : -14}" stroke="${INK}" stroke-width="2"/>${k % 2 ? "" : T(-30, -k * 5 * P + 6, k * 5, 15, INK, { anchor: "end", w: 700 })}`).join("")}
      <rect x="-6" y="-284" width="12" height="284" rx="6" fill="none" ${O(2.5)}/><rect id="${id}-col" x="-4" y="${-deg * P}" width="8" height="${deg * P}" fill="#d23b2e"/><circle cy="12" r="13" fill="#d23b2e" ${O(2.5)}/>${T(18, -294, "°C", 16, INK, { w: 700 })}</g>`;
  }
  // a walkie-talkie (ภู's, EP.4): olive body, stubby antenna, speaker grille, a red LED #id-led, the push-to-talk bar; origin = bottom centre
  function WALKIE(id, o = {}) {
    return `<g id="${id}"><rect x="-34" y="-150" width="68" height="150" rx="12" fill="#3d4636" ${O(3)}/><rect x="16" y="-232" width="12" height="86" rx="5" fill="#22261e" ${O(2.5)}/><rect x="-30" y="-130" width="46" height="18" rx="4" fill="#22261e"/>
      ${Array.from({ length: 5 }, (_, k) => `<path d="M-22,${-96 + k * 12}h44" stroke="#22261e" stroke-width="5" stroke-linecap="round"/>`).join("")}<circle id="${id}-led" cx="-18" cy="-140" r="6" fill="#ff3b30" opacity="${o.led ?? 0.25}"/><rect x="-40" y="-110" width="8" height="40" rx="3" fill="#22261e"/>
      <path d="M-26,-30h52" stroke="#5a6650" stroke-width="4"/></g>`;
  }
  // the red-cross medicine fridge of the canteen (EP.7's FRIDGE), tall, white; o.open swings the door out to the right and shows the
  // dark interior: wire shelves with medicine boxes and vials; o.light lights the interior (it never is in EP.8); origin = floor centre
  function FRIDGE8(id, x, y, s = 1, o = {}) {
    const lit = !!o.light, inner = lit ? "#dfe9ee" : "url(#iLiner)";
    let g = `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><ellipse cx="10" cy="6" rx="130" ry="16" fill="#000" opacity=".22"/>`;
    if (!o.open) return g + `<rect x="-95" y="-340" width="190" height="340" rx="14" fill="#e8ece6" ${OUT}/><path d="M-95,-216H95" stroke="#9aa0a6" stroke-width="4"/><path d="M70,-308v62M70,-188v84" stroke="#8d969d" stroke-width="8" stroke-linecap="round"/>
      <rect x="-56" y="-158" width="74" height="74" rx="6" fill="#f4f2ea" ${O(3)}/><path d="M-30,-148h22v22h22v22h-22v22h-22v-22h-22v-22h22z" fill="#d23b2e" transform="translate(5,4) scale(.68) translate(-12,-40)"/><rect x="-64" y="-296" width="96" height="36" rx="4" fill="#f4f2ea" ${O(2.5)}/>${T(-16, -270, "ยา", 26, "#2f6fb8")}</g>`;
    // the open body: outer shell, the dark liner, shelves and boxes
    g += `<rect x="-95" y="-340" width="190" height="340" rx="14" fill="#e8ece6" ${OUT}/><rect x="-78" y="-322" width="156" height="306" rx="8" fill="${inner}" ${O(3)}/>`;
    const r = mk(o.seed || 91), cols = ["#f7f9f9", "#cfe2f2", "#f2d6c4", "#e8e2c4"];
    [-236, -150, -66].forEach((sy, j) => {
      g += `<path d="M-76,${sy}H76" stroke="#8d969d" stroke-width="5"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-72 + k * 18},${sy - 2}v4" stroke="#6f7880" stroke-width="2"/>`).join("")}`;
      for (let k = 0, xx = -70; xx < 60; k++) { const w = 22 + r() * 22, h = 30 + r() * 36;
        g += `<rect x="${f1(xx)}" y="${f1(sy - h)}" width="${f1(w)}" height="${f1(h)}" fill="${cols[(j + k) % 4]}" ${O(2)} opacity="${lit ? 1 : 0.8}"/><rect x="${f1(xx)}" y="${f1(sy - h * 0.62)}" width="${f1(w)}" height="${f1(h * 0.16)}" fill="#2f6fb8" opacity=".7"/>`; xx += w + 4 + r() * 6; } });
    if (!lit) g += `<rect x="-78" y="-322" width="156" height="306" rx="8" fill="#0e1218" opacity=".42"/>`;
    // the door swung open toward us on the right (a narrow parallelogram), its bins, the red-cross sticker on the outside face
    g += `<path d="M95,-336L176,-372V-6L95,-2Z" fill="url(#iDoor)" ${OUT}/><path d="M104,-300L168,-326M104,-200L168,-222M104,-104L168,-122" stroke="#8d969d" stroke-width="5"/>
      ${[-300, -200, -104].map((by) => `<path d="M108,${by}l8,-34h10l8,30" fill="#c9cfd2" ${O(2)}/>`).join("")}<path d="M100,-330L172,-362" stroke="#5b6066" stroke-width="4" opacity=".5"/></g>`;
    return g;
  }
  // a ground-mounted solar array after the storm: a frame on four legs carrying a tilted row of panels, two panels cracked (white
  // crazing), one fallen out and leaning on the legs, mud splashed up the legs; origin = ground centre (~760 wide at s = 1)
  function SOLARRACK(x, y, s = 1, o = {}) {
    const P = (x0, y0, w, h, crack) => `<g><path d="M${x0},${y0}L${x0 + w},${y0}L${x0 + w + 40},${y0 - h}L${x0 + 40},${y0 - h}Z" fill="url(#eSolar)" ${O(3)}/><path d="M${x0},${y0}L${x0 + w},${y0}L${x0 + w + 40},${y0 - h}L${x0 + 40},${y0 - h}Z" fill="url(#eCell)"/>
      ${crack ? `<path d="M${x0 + w * 0.5},${y0 - h * 0.45}l-40,-30M${x0 + w * 0.5},${y0 - h * 0.45}l50,-20M${x0 + w * 0.5},${y0 - h * 0.45}l-20,40M${x0 + w * 0.5},${y0 - h * 0.45}l34,46M${x0 + w * 0.5 - 40},${y0 - h * 0.45 - 30}l-24,10M${x0 + w * 0.5 + 50},${y0 - h * 0.45 - 20}l20,-24" stroke="#f4f8ff" stroke-width="3" opacity=".85" fill="none"/><circle cx="${x0 + w * 0.5}" cy="${y0 - h * 0.45}" r="7" fill="#f4f8ff" opacity=".8"/>` : ""}</g>`;
    let g = `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="8" rx="420" ry="34" fill="#000" opacity=".2"/>`;
    g += `<path d="M-330,0V-150M-110,0V-190M110,0V-230M330,0V-270" stroke="#7d868c" stroke-width="16"/><path d="M-330,-150L330,-270" stroke="#6f7880" stroke-width="12"/>`;
    g += P(-380, -150, 200, 120, false) + P(-170, -186, 200, 120, true) + P(40, -224, 200, 120, !!o.crack2);
    g += `<g transform="translate(250,-20) rotate(-68)"><path d="M0,0L200,0L230,-110L30,-110Z" fill="url(#eSolar)" ${O(3)}/><path d="M0,0L200,0L230,-110L30,-110Z" fill="url(#eCell)"/><path d="M90,-50l-36,-26M90,-50l40,-12M90,-50l-10,40" stroke="#f4f8ff" stroke-width="3" opacity=".85"/></g>`;
    g += `${[-330, -110, 110, 330].map((lx) => `<path d="M${lx - 16},0q8,-30 4,-60q10,24 12,60z" fill="#5a4a36" opacity=".6"/>`).join("")}</g>`;
    return g;
  }
  // a fallen branch with its leaves (a mango-tree limb); origin = the broken end
  function BRANCH(x, y, s = 1, rot = 0) {
    const r = mk(Math.abs(Math.round(x + y)) + 5);
    let g = `<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><path d="M0,0Q160,-30 420,-10" stroke="#5a4028" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M180,-22Q260,-110 340,-140M280,-14Q360,40 440,60" stroke="#5a4028" stroke-width="14" fill="none" stroke-linecap="round"/>
      <path d="M-6,-14l12,6l-8,10l10,4" stroke="#e8d0a0" stroke-width="5" fill="none"/>`;
    for (let k = 0; k < 26; k++) { const t = r(), bx = 120 + t * 330, by = -20 - r() * 120 + t * 60, a = r() * 180;
      g += `<ellipse cx="${f1(bx)}" cy="${f1(by)}" rx="30" ry="12" fill="${["#3f6a32", "#4f7c3a", "#365c2c"][k % 3]}" transform="rotate(${f1(a)} ${f1(bx)} ${f1(by)})" ${O(2)}/>`; }
    return g + `</g>`;
  }
  // the estate's alarm bell on a bracket (a red fire bell with its striker); origin = the wall mount
  const BELL = (id, x, y, s = 1) => `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><rect x="-20" y="-30" width="40" height="60" rx="6" fill="#5b6066" ${O(3)}/><path d="M0,0H70" stroke="#5b6066" stroke-width="10"/>
    <g id="${id}-b" transform="translate(110,0)"><path d="M-46,30Q-50,-46 0,-50Q50,-46 46,30Z" fill="#c8392b" ${OUT}/><rect x="-52" y="26" width="104" height="14" rx="6" fill="#a52a20" ${O(3)}/><path d="M-24,-30q-10,24 -6,52" stroke="#fff" stroke-opacity=".35" stroke-width="8" fill="none"/><circle cy="-50" r="9" fill="#3a3f45"/></g></g>`;

  // ======================================================================================================
  // 1. inside the dead medicine fridge, close: the liner, three wire shelves of boxes and bottles, เจ๊หงส์'s insulin box (#id-box)
  //    on the middle shelf with vials beside it (#id-v0..#id-v2, #id-v1 is the one her hand takes), the open door edge on the
  //    right with its bins and the thermometer strip (#id-th), the unlit lamp; everything in the blue dark of a fridge without power
  // ======================================================================================================
  function fridgeIn(L, o = {}) {
    const id = o.id || "fi", r = mk(o.seed || 93);
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#0b0e13"/>`);
    // the liner (far): back wall with ribs, the side walls in perspective, condensation drops
    let w = `<rect x="-1400" y="-900" width="4000" height="3800" fill="#14181f"/><path d="M60,180L1020,180L900,320L180,320Z" fill="#2c333d"/><path d="M60,180L180,320V1620L60,1760Z" fill="url(#iLinerSide)"/><path d="M1020,180L900,320V1620L1020,1760Z" fill="#262d36"/>
      <rect x="180" y="320" width="720" height="1300" fill="url(#iLiner)" ${O(3)}/>${Array.from({ length: 12 }, (_, k) => `<path d="M${210 + k * 58},330V1610" stroke="#000" stroke-opacity=".12" stroke-width="5"/>`).join("")}
      ${Array.from({ length: 34 }, () => { const x = 200 + r() * 680, y = 360 + r() * 1220, rr = 2 + r() * 5; return `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rr)}" ry="${f1(rr * 1.4)}" fill="#a9c2d6" opacity="${f1(0.18 + r() * 0.25)}"/>`; }).join("")}
      <g transform="translate(540,340)"><rect x="-70" y="-14" width="140" height="40" rx="10" fill="#3a434e" ${O(3)}/><rect x="-50" y="-4" width="100" height="18" rx="6" fill="#5a6470"/></g>`;
    put(L.far, w);
    // shelves (set): front rails + rods, the boxes, the vials, เจ๊หงส์'s box
    let s = ``;
    const shelf = (y) => `<path d="M120,${y}H960" stroke="#9aa4ab" stroke-width="12"/><path d="M120,${y - 6}H960" stroke="#d3d9dd" stroke-width="3" opacity=".6"/>${Array.from({ length: 22 }, (_, k) => `<path d="M${140 + k * 38},${y - 2}L${160 + k * 34},${y - 60}" stroke="#7d868c" stroke-width="3" opacity=".7"/>`).join("")}`;
    const box = (x, y, w, h, col, band, label) => `<g><rect x="${x}" y="${y - h}" width="${w}" height="${h}" fill="${col}" ${O(3)}/><rect x="${x}" y="${f1(y - h * 0.62)}" width="${w}" height="${f1(h * 0.18)}" fill="${band}"/>${label ? T(x + w / 2, f1(y - h * 0.62 + h * 0.15), label, Math.min(22, w / 4), "#fff") : ""}<path d="M${x + w},${y - h}l18,-14V${y - 14}l-18,14z" fill="#000" opacity=".2"/></g>`;
    // top shelf y 700: liquid-antibiotic bottles (amber), a stack of small boxes
    s += `${[230, 300, 370].map((x) => `<g transform="translate(${x},700)"><path d="M-26,0V-110Q-26,-124 -12,-128V-146H12V-128Q26,-124 26,-110V0Z" fill="#b8742e" opacity=".9" ${O(3)}/><rect x="-26" y="-92" width="52" height="40" fill="#f4f2ea" ${O(2)}/>${T(0, -66, "ยาน้ำ", 15, "#c8392b")}<rect x="-14" y="-162" width="28" height="18" rx="3" fill="#f4f2ea" ${O(2)}/></g>`).join("")}`;
    s += box(450, 700, 150, 90, "#e8e2c4", "#6a8a3a", "") + box(470, 610, 120, 70, "#cfe2f2", "#2f6fb8", "") + box(640, 700, 220, 130, "#f2d6c4", "#c8762a", "วัคซีน");
    s += shelf(700);
    // middle shelf y 1080: three vials, เจ๊หงส์'s box, another box
    s += [0, 1, 2].map((k) => `<g transform="translate(${250 + k * 62},1080) scale(1.5)">${VIAL(`${id}-v${k}`, {})}</g>`).join("");
    s += `<g transform="translate(560,1080) scale(1.9)">${INSULIN(`${id}-box`, { name: "หงส์" })}</g>` + box(720, 1080, 170, 150, "#f7f9f9", "#9a5aa8", "");
    s += shelf(1080);
    // bottom shelf y 1440: the crisper, more boxes behind its front
    s += box(220, 1440, 200, 120, "#cfe2f2", "#2f6fb8", "") + box(450, 1440, 160, 160, "#e8e2c4", "#c8392b", "") + box(640, 1440, 230, 110, "#f7f9f9", "#6a8a3a", "");
    s += shelf(1440) + `<path d="M150,1470H930L910,1600H170Z" fill="#cfe2f2" opacity=".18" ${O(3)}/>`;
    // the dark over everything inside (no lamp)
    s += `<rect x="60" y="180" width="960" height="1580" fill="#0b1018" opacity="${o.lit ? 0 : 0.34}"/>`;
    put(L.set, s);
    // the open door on the right (fg): its inner face with bins and the thermometer strip; the fridge's outer edge on the left
    put(L.fg, `<g><path d="M950,-200L1400,-380V2300L950,2120Z" fill="url(#iDoor)" ${OUT}/><path d="M960,-160L1380,-330" stroke="#5b6066" stroke-width="6" opacity=".5"/>
      ${[520, 980, 1440].map((by) => `<path d="M970,${by}L1360,${by - 150}" stroke="#8d969d" stroke-width="10"/><path d="M990,${by - 6}L1010,${by - 110}L1100,${by - 145}L1120,${by - 44}Z" fill="#c9cfd2" ${O(2.5)}/>`).join("")}
      <g transform="translate(1100,420) rotate(-12) scale(1.2)">${THERMO(`${id}-th`, { deg: o.deg ?? 6 })}</g>
      <path d="M-1400,-900H60V2900H-1400Z" fill="#e8ece6"/><path d="M60,-900V2900" stroke="${INK}" stroke-width="6"/><path d="M30,-900V2900" stroke="#9aa0a6" stroke-width="10"/></g>`);
    put(L.glow, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#9ab8d0" opacity=".05"/><ellipse cx="360" cy="1100" rx="520" ry="420" fill="#ffd9a8" opacity=".06"/>`);
  }

  // ======================================================================================================
  // 2. คุณวิน's office from inside at night: the lamp-lit back wall with the team photo and the calendar, a dark window with blinds,
  //    the filing cabinet, his desk (lamp, notebook, the radio), the bar fridge at the right (#id-bf: door #id-bfdoor closed /
  //    #id-bfopen open, its cold light #id-bflight + #id-bfglow), the hallway door at the left with a frosted pane (#id-pane) and a
  //    torch spot behind it (#id-torch, the shot moves it); floor y = 1500
  // ======================================================================================================
  function officeIn(L, o = {}) {
    const id = o.id || "oi", F = 1500, r = mk(o.seed || 95);
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#141018"/>`);
    let w = `<rect x="-1400" y="-900" width="4000" height="${F + 900}" fill="url(#oWarmWall)"/><rect x="-1400" y="${F - 260}" width="4000" height="260" fill="#3e2e22"/><path d="M-1400,${F - 260}H2600" stroke="#2a2018" stroke-width="10"/>
      ${Estate7.teamPhoto(470, 760, 1.15)}
      <g transform="translate(130,740)"><rect x="-80" y="-104" width="160" height="196" fill="#f4f2ea" ${O(3)}/><rect x="-80" y="-104" width="160" height="38" fill="#c8392b"/>${T(0, -76, "ต.ค.", 24, "#f4f2ea")}
        ${Array.from({ length: 20 }, (_, k) => `<rect x="${-68 + (k % 5) * 28}" y="${-56 + Math.floor(k / 5) * 32}" width="20" height="20" fill="none" stroke="#9aa0a6" stroke-width="1.5"/>${k < 13 ? `<path d="M${-66 + (k % 5) * 28},${-54 + Math.floor(k / 5) * 32}l16,16M${-50 + (k % 5) * 28},${-54 + Math.floor(k / 5) * 32}l-16,16" stroke="#c8392b" stroke-width="2"/>` : ""}`).join("")}</g>
      <g transform="translate(860,700)"><rect x="-150" y="-170" width="300" height="300" fill="#141a26" ${OUT}/>${Array.from({ length: 9 }, (_, k) => `<path d="M-146,${-160 + k * 30}h292" stroke="#c9b48a" stroke-width="9" opacity="${k < 5 ? 0.9 : 0.25}"/>`).join("")}<circle cx="80" cy="60" r="5" fill="#fffbe8" opacity=".7"/><circle cx="-60" cy="80" r="3" fill="#fffbe8" opacity=".6"/></g>
      <g transform="translate(-260,${F})"><rect x="-90" y="-420" width="180" height="420" fill="#6f7880" ${OUT}/>${[0, 1, 2, 3].map((k) => `<rect x="-76" y="${-406 + k * 102}" width="152" height="88" fill="#7d868c" ${O(2.5)}/><rect x="-22" y="${-372 + k * 102}" width="44" height="10" rx="4" fill="#3a3f45"/>`).join("")}</g>`;
    put(L.far, w);
    // the hallway door at the left: frame, the panel, the frosted pane and the torch spot behind it
    let s = `<rect x="-1400" y="${F}" width="4000" height="1400" fill="#5a4030"/>${Array.from({ length: 14 }, (_, k) => `<path d="M-1400,${F + 30 + k * k * 9}H2600" stroke="#3e2c20" stroke-width="${2 + k * 0.6}"/>`).join("")}
      <g><rect x="-60" y="${F - 640}" width="300" height="640" fill="#2a2018" ${O(4)}/><rect x="-46" y="${F - 626}" width="272" height="626" fill="#7a5a3a" ${O(3)}/><clipPath id="${id}-pclip"><rect x="-10" y="${F - 580}" width="200" height="240"/></clipPath>
        <rect id="${id}-pane" x="-10" y="${F - 580}" width="200" height="240" fill="#2e3440" ${O(3)}/><g clip-path="url(#${id}-pclip)"><circle id="${id}-torch" cx="-140" cy="${F - 470}" r="120" fill="url(#tSpot)" opacity="0"/></g>
        <path d="M-10,${F - 580}l200,240M60,${F - 580}l130,160" stroke="#fff" stroke-opacity=".08" stroke-width="18"/><circle cx="196" cy="${F - 300}" r="12" fill="#c9a55a" ${O(2)}/></g>`;
    // the desk (its front panel is #id-deskf, so a rig can sit or kneel behind it); lamp, notebook, radio on top
    s += `<g><rect x="300" y="${F - 360}" width="560" height="26" fill="#5a3e24" ${O(3)}/>
      <g transform="translate(380,${F - 360})"><path d="M-40,0h80l-10,-14h-60z" fill="#3a3f45" ${O(2)}/><path d="M0,-14L-20,-120L30,-160" stroke="#3a3f45" stroke-width="8" fill="none"/><path d="M10,-180l64,12l-22,52z" fill="#c8a85a" ${O(3)}/></g>
      <g transform="translate(580,${F - 362}) rotate(-3)"><rect x="-90" y="-24" width="180" height="24" fill="#f4ecd8" ${O(2)}/><path d="M0,-24V0" stroke="#8a7a5a" stroke-width="3"/></g>
      <g transform="translate(770,${F - 360})"><rect x="-70" y="-84" width="140" height="84" rx="14" fill="#6b4a2e" ${OUT}/><rect x="-58" y="-70" width="70" height="40" rx="5" fill="#2a1a0a"/><g id="${id}-dialw"><rect x="-58" y="-70" width="70" height="40" rx="5" fill="#ffb35c" opacity=".75"/></g><path d="M60,-84L100,-170" stroke="#9aa0a6" stroke-width="4"/></g></g>`;
    put(L.set, s);
    // desk front (act, over a rig behind it) and the bar fridge (act, so ก้อง can kneel in front of it)
    put(L.act, `<g id="${id}-deskf"><rect x="300" y="${F - 336}" width="560" height="336" fill="#4e3620" ${OUT}/><rect x="324" y="${F - 310}" width="240" height="120" fill="#5a3e24" ${O(2.5)}/><rect x="596" y="${F - 310}" width="240" height="120" fill="#5a3e24" ${O(2.5)}/><rect x="424" y="${F - 256}" width="40" height="10" rx="4" fill="#c9a55a"/><rect x="696" y="${F - 256}" width="40" height="10" rx="4" fill="#c9a55a"/></g>`);
    put(L.act, `<g id="${id}-bf" transform="translate(${o.bfx ?? 1010},${F})"><ellipse cx="6" cy="4" rx="110" ry="12" fill="#000" opacity=".25"/><rect x="-90" y="-250" width="180" height="250" rx="12" fill="#e8ece6" ${OUT}/>
      <rect x="-76" y="-236" width="152" height="222" rx="8" fill="#dfeef6" ${O(3)}/><g id="${id}-bfin">${[-170, -100].map((sy) => `<path d="M-74,${sy}H74" stroke="#9aa4ab" stroke-width="5"/>`).join("")}
        ${[[-60, -170], [-28, -170], [4, -170]].map(([vx, vy]) => `<g transform="translate(${vx},${vy}) scale(.72)">${VIAL("", {})}</g>`).join("")}<g transform="translate(46,-170) scale(.5)">${INSULIN("", { name: "" })}</g><g transform="translate(-20,-100) scale(.6)">${INSULIN(`${id}-loot`, { name: "" })}</g><rect x="20" y="-160" width="44" height="58" fill="#f2d6c4" ${O(2)}/></g>
      <g id="${id}-bflight" opacity="${o.bfOpen ? 1 : 0}"><rect x="-76" y="-236" width="152" height="222" rx="8" fill="#eaf8ff" opacity=".45"/></g>
      <g id="${id}-bfdoor" opacity="${o.bfOpen ? 0 : 1}"><rect x="-90" y="-250" width="180" height="250" rx="12" fill="#e8ece6" ${OUT}/><path d="M66,-220v80" stroke="#8d969d" stroke-width="8" stroke-linecap="round"/></g>
      <g id="${id}-bfopen" opacity="${o.bfOpen ? 1 : 0}"><path d="M-90,-246L-200,-290V-10L-90,-4Z" fill="url(#iDoor)" ${OUT}/><path d="M-100,-200L-190,-232M-100,-110L-190,-136" stroke="#8d969d" stroke-width="5"/></g></g>`);
    put(L.glow, `<circle cx="420" cy="${F - 520}" r="560" fill="url(#oPool)"/><g id="${id}-dialg"><circle cx="760" cy="${F - 400}" r="200" fill="url(#fDial)" opacity=".7"/></g>
      <g id="${id}-bfglow" opacity="${o.bfOpen ? 1 : 0}"><circle cx="${(o.bfx ?? 1010) - 40}" cy="${F - 140}" r="380" fill="url(#iCold)"/><path d="M${(o.bfx ?? 1010) - 80},${F - 236}L${(o.bfx ?? 1010) - 620},${F - 520}V${F + 260}L${(o.bfx ?? 1010) - 80},${F - 20}Z" fill="url(#iColdBeam)" transform="scale(-1,1) translate(${-2 * ((o.bfx ?? 1010) - 80)},0)"/></g>`);
  }

  // ======================================================================================================
  // 3. the dark field outside the fence: a night sky with the moon, the estate on the horizon with its lamps still lit (it has power
  //    for the lamps), flooded paddies with the moon in them, a lone dead tree, the dirt embankment across the foreground (y 1500)
  //    the group crouches behind
  // ======================================================================================================
  function fieldNight(L, o = {}) {
    const id = o.id || "fn", r = mk(o.seed || 97);
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="url(#fNight)"/>${Array.from({ length: 90 }, () => `<circle cx="${f1(-1200 + r() * 3400)}" cy="${f1(-800 + r() * 1700)}" r="${f1(1 + r() * 2.2)}" fill="#e9eef5" opacity="${f1(0.3 + r() * 0.6)}"/>`).join("")}
      <circle cx="${o.moonX ?? 820}" cy="300" r="300" fill="url(#nMoon)"/><circle cx="${o.moonX ?? 820}" cy="300" r="62" fill="#f4f8ff"/><circle cx="${(o.moonX ?? 820) + 18}" cy="290" r="54" fill="#dfe8f6" opacity=".5"/>`);
    // the estate far off (left of centre) — the skyline of estate.js is not exported, so a low silhouette with its lamps
    const ex = o.estX ?? 260;
    put(L.far, `<rect x="-1400" y="1060" width="4000" height="900" fill="url(#nWater)"/>${Array.from({ length: 10 }, (_, k) => `<path d="M-1400,${1080 + k * k * 6}H2600" stroke="#3a4a66" stroke-width="${1 + k * 0.4}" opacity=".5"/>`).join("")}
      <ellipse cx="${o.moonX ?? 820}" cy="1180" rx="60" ry="200" fill="#cfdcf0" opacity=".18"/>
      <g transform="translate(${ex},1060)"><path d="M-420,0V-60L-380,-90V-60L-340,-90V-60L-300,-90V-60L-260,-90V-40H-200V-150H-160V-40H40V-110L80,-130L120,-110V-40H260V-70L300,-90V-40H420V0Z" fill="#0e1320"/>
        ${Array.from({ length: 14 }, (_, k) => `<circle cx="${-400 + k * 60}" cy="-8" r="4" fill="#fffbe8"/>`).join("")}<rect x="-190" y="-140" width="20" height="14" fill="#ffd58a" opacity=".8"/></g>`);
    put(L.glow, Array.from({ length: 14 }, (_, k) => `<circle cx="${ex - 400 + k * 60}" cy="1052" r="40" fill="url(#eFlood)" opacity=".7"/>`).join("") + `<ellipse cx="${ex}" cy="1040" rx="520" ry="60" fill="#ffd58a" opacity=".12"/>`);
    put(L.mid, `<g transform="translate(${o.treeX ?? 900},1230)"><path d="M0,0V-320M0,-200l-70,-90M0,-150l80,-110M0,-260l-30,-70M80,-260l30,-40" stroke="#0a0e16" stroke-width="16" fill="none" stroke-linecap="round"/></g>
      ${Array.from({ length: 18 }, () => { const x = -1200 + r() * 3300, y = 1200 + r() * 200; return `<path d="M${f1(x)},${f1(y)}l-6,-30M${f1(x + 8)},${f1(y)}l4,-36M${f1(x + 16)},${f1(y)}l10,-26" stroke="#1a2232" stroke-width="4"/>`; }).join("")}`);
    // the embankment (set): an earthen ridge, its top lit by the moon, tufts of grass
    let s = `<path d="M-1400,1560Q-200,1460 540,1490Q1300,1520 2600,1450V2900H-1400Z" fill="#2a2a2c"/><path d="M-1400,1560Q-200,1460 540,1490Q1300,1520 2600,1450" stroke="#5a5e6a" stroke-width="10" fill="none" opacity=".6"/>
      ${Array.from({ length: 60 }, () => { const x = -1300 + r() * 3800, y = 1500 + r() * 60 - (x > 1300 ? (x - 1300) * 0.05 : 0); return `<path d="M${f1(x)},${f1(y)}q-6,-40 -18,-60M${f1(x)},${f1(y)}q4,-50 0,-74M${f1(x)},${f1(y)}q10,-36 24,-52" stroke="#1e2a22" stroke-width="5" fill="none"/>`; }).join("")}
      <rect x="-1400" y="1700" width="4000" height="1200" fill="#1c1c1e"/>`;
    put(L.set, s);
  }

  // ======================================================================================================
  // 4. ปั้น's drawing that night under the lightning: rain, a grey sky with a bolt, a field under water, four people wading with the
  //    water at their knees (ครูพิม, ก้อง with his bandana, ภู with the red scarf, ปั้น small) — four, not five — and round dark heads
  //    in the water around them; "พรุ่งนี้", "ฝน", "ปั้น"
  // ======================================================================================================
  function drawing8(L, o = {}) {
    const id = o.id || "dw8";
    put(L.sky, `<rect x="-1200" y="-800" width="3500" height="3600" fill="#2e2c2c"/>`);
    const C = (d, col, w = 9) => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#fCrayon)"/>`;
    let s = `<g transform="rotate(-1.5 540 960)"><rect x="90" y="260" width="900" height="1400" fill="url(#fPaper)" ${OUT}/><circle cx="540" cy="290" r="16" fill="#c8392b" ${OUT}/>`;
    s += `<rect x="140" y="320" width="800" height="560" fill="#5a6270" opacity=".45" filter="url(#fCrayon)"/>` + C("M640,360L590,520L650,520L580,700", "#f4d84a", 12);
    s += C(Array.from({ length: 26 }, (_, k) => `M${160 + (k * 37) % 760},${340 + (k * 53) % 1200}l-22,60`).join(""), "#7aa6d8", 5);
    s += `<rect x="140" y="980" width="800" height="560" fill="#4a78b8" opacity=".55" filter="url(#fCrayon)"/>` + C("M140,980Q300,960 540,985Q780,1005 940,975", "#2f5a9a", 10);
    // four people, cut at the water line (y 1070)
    const kid = (x, top, sc, extra) => `<g transform="translate(${x},1070) scale(${sc})" filter="url(#fCrayon)"><path d="M-46,0q2,-120 46,-130q44,10 46,130z" fill="${top}"/><circle cx="0" cy="-170" r="44" fill="#e9b48a"/>${extra}<path d="M-46,-90l-46,-40M46,-90l46,-40" stroke="#e9b48a" stroke-width="18" stroke-linecap="round"/></g>`;
    s += kid(250, "#9fc5e8", 1.05, `<path d="M-46,-186q0,-50 46,-52q46,2 46,52q-14,-24 -46,-26q-32,2 -46,26z" fill="#3a2a22"/><path d="M30,-216l20,-30" stroke="#e8b830" stroke-width="6"/>`);
    s += kid(420, "#d8463a", 1.0, `<path d="M-48,-190q0,-46 48,-48q48,2 48,48z" fill="#2a2420"/><path d="M-50,-196h100" stroke="#c8392b" stroke-width="12"/>`);
    s += kid(610, "#7d8f78", 1.12, `<path d="M-44,-196q2,-36 44,-38q42,2 44,38q-14,-14 -44,-16q-30,2 -44,16z" fill="#1e1a18"/><path d="M-30,-128q30,14 60,0l-6,16q-24,10 -48,0z" fill="#c8392b"/>`);
    s += kid(770, "#f4f2ea", 0.72, `<path d="M-44,-190q0,-44 44,-46q44,2 44,46q-14,-20 -44,-22q-30,2 -44,22z" fill="#231a16"/><path d="M-46,-180q-24,6 -20,40M46,-180q20,6 16,40" stroke="#231a16" stroke-width="12" stroke-linecap="round" fill="none"/><path d="M-40,-40h80v40h-80z" fill="#c8392b"/>`);
    s += C("M150,1070H930", "#2f5a9a", 8);
    // the round dark heads in the water, eyes
    s += [[200, 1180, 1], [350, 1250, 0.8], [520, 1200, 1.1], [690, 1290, 0.9], [860, 1170, 1], [300, 1380, 0.7], [760, 1420, 0.8]].map(([x, y, k]) => `<g transform="translate(${x},${y}) scale(${k})" filter="url(#fCrayon)"><ellipse rx="40" ry="34" fill="#22242a"/><circle cx="-12" cy="-4" r="6" fill="#d23b2e"/><circle cx="12" cy="-4" r="6" fill="#d23b2e"/></g>`).join("");
    s += T(540, 430, "พรุ่งนี้", 72, "#f4ecd8", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(260, 560, "ฝน", 50, "#9fc5e8", { w: 700, extra: ' filter="url(#fCrayon)"' }) + T(880, 1620, "ปั้น", 34, "#c8392b", { w: 700, extra: ' filter="url(#fCrayon)"' });
    s += `</g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="540" cy="900" r="900" fill="url(#fLamp)" opacity=".3"/><g id="${id}-flash" opacity="0"><rect x="-1400" y="-900" width="4000" height="3800" fill="#eaf2ff" opacity=".55"/></g>`);
  }

  // small hand props (attached to the front hand by Camp.attach through the rig's `prop` option)
  if (window.Camp) Object.assign(Camp.hand, {
    insulin: `<g transform="translate(6,150) rotate(8) scale(.62)">${INSULIN("", { name: "หงส์" })}</g>`,
    vial: `<g transform="translate(4,136) scale(.62)">${VIAL("", {})}</g>`,
    torch: `<g transform="translate(0,124) rotate(-90)"><rect x="-14" y="-12" width="70" height="24" rx="8" fill="#2a2c2e" ${O(3)}/><path d="M56,-18h22v36h-22z" fill="#3a3f45" ${O(3)}/><rect x="76" y="-14" width="6" height="28" fill="#fff6d8"/></g>`,
    walkie: `<g transform="translate(0,170) scale(.5)">${WALKIE("", { led: 1 })}</g>`,
  });

  window.Estate8 = { INSULIN, VIAL, THERMO, WALKIE, FRIDGE8, SOLARRACK, BRANCH, BELL };
  Object.assign(Sets, { fridgeIn, officeIn, fieldNight, drawing8 });
})();
