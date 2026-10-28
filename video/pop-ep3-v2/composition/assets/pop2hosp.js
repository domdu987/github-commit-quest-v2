// "เห็ดปอบ" v2 — EP.2/EP.3 sets: the night road and ลุงทองดี's pickup, the cab in dashboard light, the district hospital's
// emergency entrance, the ward (night / dawn / day), and knowledge laid out on a surface.
//   Sets.nightRoad2(L, o)  dark paddies under the moon, a dirt road, roadside posts #id-posts (scroll x), the pickup #id-truck at o.x
//                          (o.flip faces left; headlights in the glow layer; o.bed true leaves room for actors in the bed)
//   Sets.cab2(L, o)        inside the cab at night: windshield with the headlights on the road ahead (#id-road scrolls), dashboard glow
//   Sets.erFront2(L, o)    the emergency entrance: canopy, the red sign, glass doors lit, a wheelchair, moths round the lamp
//   Sets.ward2(L, o)       o.time night | dawn | day · o.bed x · o.window x · o.print (a long-fingered handprint on the glass #id-print)
//                          o.eyes (green eyes outside #id-eyes) · the monitor's trace #id-ecg · the curtain #id-curtain
//   Sets.benchTop(L, o)    items on the bamboo bench seen from above: o.items [[x, y, label, icon], …] → #id-t0.., stamps #id-x0..,
//                          o.verdict text #id-verdict (o.verdictY), o.ok [i…] items that get a green tick instead of a red ring
//   Pop2.truck(o)          the pickup, side view, origin between the wheels on the ground
//   Pop2.PROP.{basin, saltGlass, bag, torchBeam}
(function () {
  const { mk, f1, put, blob } = Pop2;
  const LN = "#2a1e1a";

  Sets.DEFS += `
    <linearGradient id="nrSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050a"/><stop offset=".7" stop-color="#0c1426"/><stop offset="1" stop-color="#18223a"/></linearGradient>
    <linearGradient id="nrPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2638"/><stop offset="1" stop-color="#0a0e16"/></linearGradient>
    <linearGradient id="nrRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2420"/><stop offset="1" stop-color="#3a2e26"/></linearGradient>
    <linearGradient id="nrBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff4d0" stop-opacity=".75"/><stop offset="1" stop-color="#fff4d0" stop-opacity="0"/></linearGradient>
    <linearGradient id="nrBeamL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#fff4d0" stop-opacity=".75"/><stop offset="1" stop-color="#fff4d0" stop-opacity="0"/></linearGradient>
    <linearGradient id="nrBeamUp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff4d0" stop-opacity=".6"/><stop offset="1" stop-color="#fff4d0" stop-opacity="0"/></linearGradient>
    <radialGradient id="nrTail"><stop offset="0" stop-color="#ff4030" stop-opacity=".8"/><stop offset="1" stop-color="#ff4030" stop-opacity="0"/></radialGradient>
    <linearGradient id="trBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8dadc"/><stop offset=".5" stop-color="#a8acb0"/><stop offset="1" stop-color="#6a6e72"/></linearGradient>
    <radialGradient id="cbDash"><stop offset="0" stop-color="#7ae8ff" stop-opacity=".55"/><stop offset="1" stop-color="#7ae8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="erWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8dcd4"/><stop offset="1" stop-color="#a8aca4"/></linearGradient>
    <radialGradient id="erLamp"><stop offset="0" stop-color="#f0fff8" stop-opacity=".8"/><stop offset=".3" stop-color="#c8f0e8" stop-opacity=".25"/><stop offset="1" stop-color="#c8f0e8" stop-opacity="0"/></radialGradient>
    <linearGradient id="wdWallN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a5450"/><stop offset="1" stop-color="#22322e"/></linearGradient>
    <linearGradient id="wdWallD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ab8ae"/><stop offset="1" stop-color="#6a8a80"/></linearGradient>
    <linearGradient id="wdFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a9690"/><stop offset="1" stop-color="#5a6662"/></linearGradient>
    <linearGradient id="wdNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04070e"/><stop offset="1" stop-color="#122038"/></linearGradient>
    <linearGradient id="wdDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a6a"/><stop offset=".6" stop-color="#d88a7a"/><stop offset="1" stop-color="#f6c08a"/></linearGradient>
    <linearGradient id="wdDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ab4d0"/><stop offset="1" stop-color="#e0ecf0"/></linearGradient>
    <linearGradient id="wdCurtain" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7aa8c8"/><stop offset=".5" stop-color="#9ac4e0"/><stop offset="1" stop-color="#6a98b8"/></linearGradient>
    <radialGradient id="wdTube"><stop offset="0" stop-color="#f4fffa" stop-opacity=".6"/><stop offset="1" stop-color="#f4fffa" stop-opacity="0"/></radialGradient>`;

  // ---------------- the pickup ----------------
  function truck(o = {}) {
    const c = o.color || "url(#trBody)";
    let g = `<ellipse cx="0" cy="8" rx="460" ry="30" fill="#000" opacity=".55"/>`;
    // bed and tailgate (left), cab (right), bonnet; wheels
    g += `<path d="M-430,-60V-200H-40V-60Z" fill="${c}" stroke="${LN}" stroke-width="4"/><path d="M-430,-200H-40V-186H-430Z" fill="#e8eaec"/><path d="M-410,-180V-80M-300,-180V-80M-190,-180V-80" stroke="#7a7e82" stroke-width="3" opacity=".6"/>`;
    g += `<path d="M-40,-60V-210L10,-330H190L250,-210H400Q430,-206 432,-170V-60Z" fill="${c}" stroke="${LN}" stroke-width="4"/>`;
    g += `<path d="M20,-215L54,-310H120V-215Z" fill="#1a2430" stroke="${LN}" stroke-width="3"/><path d="M136,-215V-310H182L232,-215Z" fill="#1a2430" stroke="${LN}" stroke-width="3"/>`;
    if (o.driver) g += `<g transform="translate(170,-232)"><ellipse cx="0" cy="-30" rx="26" ry="30" fill="#0e0c0a"/><path d="M-50,-50Q0,-80 50,-50Z" fill="#0e0c0a"/><path d="M-30,0Q0,-10 30,0V20H-30Z" fill="#0e0c0a"/></g>`;
    g += `<path d="M30,-205L58,-290" stroke="#fff" stroke-width="6" opacity=".25"/><path d="M128,-215V-60" stroke="${LN}" stroke-width="3"/><path d="M104,-160h20" stroke="${LN}" stroke-width="4"/>`;
    g += `<rect x="402" y="-170" width="30" height="40" rx="6" fill="#fff6c8" stroke="${LN}" stroke-width="3"/><rect x="-436" y="-170" width="16" height="40" rx="4" fill="#e8302a" stroke="${LN}" stroke-width="3"/>`;
    g += `<path d="M-440,-60H440V-40H-440Z" fill="#3a3c40" stroke="${LN}" stroke-width="3"/>`;
    [-280, 280].forEach((wx) => { g += `<path d="M${wx - 110},-60A110,110 0 0 1 ${wx + 110},-60" fill="#1a1c1e"/><circle cx="${wx}" cy="-30" r="80" fill="#1a1a1c" stroke="${LN}" stroke-width="4"/><circle cx="${wx}" cy="-30" r="40" fill="#8a8c90"/><circle cx="${wx}" cy="-30" r="12" fill="#4a4c50"/>`; });
    g += `<path d="M-430,-150H430" stroke="#fff" stroke-width="4" opacity=".2"/><path d="M-60,-120H430" stroke="#7a2a22" stroke-width="10" opacity=".5"/>`;
    return g;
  }

  // ---------------- the night road ----------------
  function nightRoad2(L, o = {}) {
    const id = o.id || "nr", r = mk(o.seed || 33), G = o.ground ?? 1400, X = o.x ?? 300;
    let sky = `<rect x="-2000" y="-900" width="6000" height="3900" fill="url(#nrSky)"/><circle cx="${o.moonX ?? 820}" cy="420" r="420" fill="url(#kiMoon)"/><circle cx="${o.moonX ?? 820}" cy="420" r="36" fill="#f4f6ff"/>`;
    for (let k = 0; k < 90; k++) sky += `<circle cx="${f1(-1500 + r() * 5000)}" cy="${f1(-600 + r() * 1500)}" r="${f1(1 + r() * 1.8)}" fill="#e8ecff" opacity="${f1(0.2 + r() * 0.6)}"/>`;
    put(L.sky, sky);
    let far = `<g id="${id}-far">`;
    for (let k = 0; k < 26; k++) far += `<path d="${blob(-1600 + k * 220 + r() * 90, G - 260 - r() * 80, 110 + r() * 80, r, 9)}" fill="#070a10"/>`;
    for (let k = 0; k < 8; k++) { const px = -1500 + k * 640 + r() * 200; far += `<path d="M${px},${G - 250}L${px + 6},${G - 640}" stroke="#070a10" stroke-width="10"/>${Array.from({ length: 9 }, (_, j) => `<path d="M${px + 6},${G - 640}q${(j - 4) * 22},${-20 + Math.abs(j - 4) * 10} ${(j - 4) * 48},${10 + Math.abs(j - 4) * 14}" stroke="#070a10" stroke-width="8" fill="none"/>`).join("")}`; }
    put(L.far, far + `</g>`);
    // mid: flooded paddies catching the moon, bunds
    let mid = `<g id="${id}-scroll"><rect x="-2000" y="${G - 260}" width="6000" height="400" fill="url(#nrPaddy)"/>`;
    for (let k = 0; k < 12; k++) mid += `<path d="M-2000,${G - 240 + k * 30}H4000" stroke="#2a3a54" stroke-width="2" opacity=".5"/>`;
    for (let k = 0; k < 30; k++) mid += `<path d="M${f1(-1800 + r() * 5600)},${f1(G - 230 + r() * 160)}h${f1(30 + r() * 120)}" stroke="#a8c0e8" stroke-width="3" opacity="${f1(0.2 + r() * 0.3)}"/>`;
    put(L.mid, mid + `</g>`);
    // set: the dirt road and verge; posts scroll past
    let s = `<rect x="-2000" y="${G - 100}" width="6000" height="900" fill="#0e120e"/><path d="M-2000,${G - 40}H4000V${G + 120}H-2000Z" fill="url(#nrRoad)"/>`;
    for (let k = 0; k < 40; k++) s += `<ellipse cx="${f1(-1800 + r() * 5600)}" cy="${f1(G - 20 + r() * 120)}" rx="${f1(10 + r() * 30)}" ry="${f1(3 + r() * 6)}" fill="#4a3a30" opacity=".6"/>`;
    s += `<g id="${id}-posts">${Array.from({ length: 18 }, (_, k) => `<rect x="${-1800 + k * 360}" y="${G - 210}" width="16" height="170" fill="#2a2420"/><path d="M${-1800 + k * 360},${G - 190}H${-1440 + k * 360}" stroke="#3a3430" stroke-width="2"/>`).join("")}</g>`;
    if (o.truck !== false) s += `<g id="${id}-truck"><g transform="translate(${X},${G + 70}) scale(${o.flip ? -1 : 1},1) scale(${o.s ?? 1})">${truck({ driver: o.driver !== false })}</g></g>`;
    s += `<rect x="-2000" y="${G + 120}" width="6000" height="900" fill="#080a08"/>`;
    for (let k = 0; k < 60; k++) s += Pop2.tuft(-1800 + r() * 5600, G + 140 + r() * 400, 1 + r(), "#0a120a", "#16221a", r);
    put(L.set, s);
    // the bed's near wall drawn again over the actors, so passengers sit inside it
    if (o.truck !== false && o.bedFront) put(L.glow, `<g transform="translate(${X},${G + 70}) scale(${o.flip ? -1 : 1},1) scale(${o.s ?? 1})"><path d="M-430,-60V-200H-40V-60Z" fill="#9a9ea2" stroke="${LN}" stroke-width="4"/><path d="M-430,-200H-40V-186H-430Z" fill="#e8eaec"/>
      <path d="M-410,-180V-80M-300,-180V-80M-190,-180V-80" stroke="#7a7e82" stroke-width="3" opacity=".6"/><path d="M-430,-150H-40" stroke="#fff" stroke-width="4" opacity=".2"/><path d="M-440,-60H-40V-40H-440Z" fill="#3a3c40"/>
      <path d="M-390,-60A110,110 0 0 1 -170,-60" fill="#1a1c1e"/><circle cx="-280" cy="-30" r="80" fill="#1a1a1c" stroke="${LN}" stroke-width="4"/><circle cx="-280" cy="-30" r="40" fill="#8a8c90"/><circle cx="-280" cy="-30" r="12" fill="#4a4c50"/>
      <rect x="-436" y="-170" width="16" height="40" rx="4" fill="#e8302a" stroke="${LN}" stroke-width="3"/></g>`);
    // headlights and tail-lights, world-anchored
    if (o.truck !== false) {
      const d = o.flip ? -1 : 1, hx = X + d * 432 * (o.s ?? 1), hy = G + 70 - 150 * (o.s ?? 1);
      const sc = o.s ?? 1;
      put(L.glow, `<g id="${id}-lights" style="mix-blend-mode:screen"><path d="M${hx},${hy - 24}L${hx + d * 1700},${hy - 300}L${hx + d * 1700},${hy + 320}L${hx},${hy + 24}Z" fill="url(#${d > 0 ? "nrBeam" : "nrBeamL"})"/>
        <path d="M${hx},${hy - 12}L${hx + d * 1200},${hy - 120}L${hx + d * 1200},${hy + 160}L${hx},${hy + 12}Z" fill="url(#${d > 0 ? "nrBeam" : "nrBeamL"})"/>
        <ellipse cx="${hx + d * 700}" cy="${G + 60}" rx="700" ry="60" fill="#fff4d0" opacity=".25"/>
        <circle cx="${hx}" cy="${hy}" r="140" fill="url(#erLamp)"/><circle cx="${X - d * 432 * sc}" cy="${hy}" r="120" fill="url(#nrTail)"/></g>
        <g id="${id}-dust" opacity=".5">${Array.from({ length: 10 }, (_, k) => `<circle cx="${f1(X - d * (460 + k * 60) * sc)}" cy="${f1(G + 40 - k * 6 - (k % 3) * 10)}" r="${f1((30 + k * 8) * sc)}" fill="#6a5a50" opacity="${f1(0.4 - k * 0.03)}"/>`).join("")}</g>`);
    }
  }

  // ---------------- inside the cab ----------------
  function cab2(L, o = {}) {
    const id = o.id || "cb", r = mk(o.seed || 35);
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#03050a"/>`);
    // through the windshield: the road in the headlights
    let far = `<g id="${id}-road"><rect x="-1300" y="780" width="3700" height="900" fill="#0a0e0a"/><path d="M500,780L580,780L1300,1300L-220,1300Z" fill="#4a3e32"/><path d="M540,790V1300" stroke="#c8b890" stroke-width="6" stroke-dasharray="30 40" opacity=".5"/>`;
    for (let k = 0; k < 14; k++) far += `<path d="${blob(-200 + k * 120 + r() * 40, 760 - r() * 30, 40 + r() * 30, r, 8)}" fill="#05080a"/>`;
    far += `</g><path d="M480,780L600,780L1400,1300L-320,1300Z" fill="url(#nrBeamUp)" opacity=".8" style="mix-blend-mode:screen"/>`;
    put(L.far, far);
    // the cab: windshield frame, roof, dashboard with gauges, the wheel
    let s = `<path d="M-1300,-900H2400V600H-1300Z M120,620L960,620L1040,1080L40,1080Z" fill="#14161a" fill-rule="evenodd"/>`;
    s += `<path d="M120,620L960,620L1040,1080L40,1080Z" fill="none" stroke="#2a2c30" stroke-width="30"/><path d="M160,640L360,640L240,1060" fill="#fff" opacity=".05"/>`;
    s += `<path d="M-1300,1060H2400V2900H-1300Z" fill="#1c1e22"/><path d="M-1300,1060Q540,1010 2400,1060V1180Q540,1130 -1300,1180Z" fill="#26282c"/>`;
    s += `<g transform="translate(760,1140)"><rect x="-150" y="-60" width="300" height="110" rx="20" fill="#0a0c0e"/>${[-80, 0, 80].map((gx) => `<circle cx="${gx}" cy="0" r="36" fill="#0e1a1e" stroke="#4adfff" stroke-width="3"/><path d="M${gx},0l${gx === 0 ? 20 : -14},-24" stroke="#ff8a3a" stroke-width="4"/>`).join("")}</g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="760" cy="1140" r="520" fill="url(#cbDash)" style="mix-blend-mode:screen"/>
      <g transform="translate(${o.wheelX ?? 300},1560)"><circle r="300" fill="none" stroke="#08080a" stroke-width="50"/><path d="M-300,0H300M0,0V300" stroke="#08080a" stroke-width="46"/><circle r="60" fill="#121416"/><path d="M-200,-220Q0,-310 200,-220" stroke="#7ae8ff" stroke-width="4" fill="none" opacity=".35"/></g>`);
  }

  // ---------------- the emergency entrance ----------------
  function erFront2(L, o = {}) {
    const id = o.id || "er", r = mk(o.seed || 37), G = o.ground ?? 1500;
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#nrSky)"/>`;
    for (let k = 0; k < 50; k++) sky += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-600 + r() * 1100)}" r="${f1(1 + r() * 1.5)}" fill="#e8ecff" opacity="${f1(0.2 + r() * 0.5)}"/>`;
    put(L.sky, sky);
    put(L.far, Array.from({ length: 10 }, (_, k) => `<path d="${blob(-1000 + k * 380, G - 620 - r() * 100, 160 + r() * 80, r, 9)}" fill="#060a0e"/>`).join(""));
    // the building: two floors of windows, the canopy over the bay, the sign
    let s = `<rect x="-600" y="${G - 1100}" width="2300" height="1100" fill="url(#erWall)"/><rect x="-600" y="${G - 1100}" width="2300" height="40" fill="#2a6aa8"/>`;
    for (let k = 0; k < 9; k++) s += `<rect x="${-560 + k * 250}" y="${G - 1020}" width="150" height="180" fill="${k % 3 === 1 ? "#f4f0c8" : "#1a2430"}" stroke="#7a7e78" stroke-width="6"/>`;
    s += `<rect x="-600" y="${G - 760}" width="2300" height="24" fill="#2a6aa8"/>`;
    s += `<path d="M120,${G - 560}H1180L1240,${G - 500}H60Z" fill="#e8ece6" stroke="#6a6e68" stroke-width="5"/><path d="M60,${G - 500}H1240V${G - 470}H60Z" fill="#c8ccc4"/>`;
    s += `<rect x="90" y="${G - 470}" width="22" height="470" fill="#b8bcb6"/><rect x="1190" y="${G - 470}" width="22" height="470" fill="#b8bcb6"/>`;
    s += `<g transform="translate(650,${G - 660})"><rect x="-330" y="-70" width="660" height="140" rx="14" fill="#c8202a" stroke="#fff" stroke-width="6"/><text y="10" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="#fff">ห้องฉุกเฉิน</text><text y="54" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" letter-spacing="6" fill="#ffe0e0">EMERGENCY</text></g>`;
    // glass doors, lit from inside
    s += `<rect x="380" y="${G - 400}" width="540" height="400" fill="#e8fff8"/><path d="M650,${G - 400}V${G}" stroke="#6a6e68" stroke-width="10"/><rect x="380" y="${G - 400}" width="540" height="400" fill="none" stroke="#6a6e68" stroke-width="12"/>
      <path d="M420,${G - 380}L520,${G - 30}" stroke="#fff" stroke-width="20" opacity=".4"/><rect x="430" y="${G - 300}" width="120" height="200" fill="#c8e0d8" opacity=".6"/>`;
    s += `<rect x="-1300" y="${G}" width="3700" height="1600" fill="#3a3e42"/><path d="M-1300,${G + 40}H2400" stroke="#e8d84a" stroke-width="8" stroke-dasharray="60 40"/><path d="M200,${G + 200}H1100" stroke="#f4f4f0" stroke-width="10"/>`;
    // a wheelchair by the door
    s += `<g transform="translate(1040,${G})"><circle cx="0" cy="-60" r="60" fill="none" stroke="#3a3a3a" stroke-width="8"/><path d="M-40,-150H40V-90H-40ZM40,-150V-230" stroke="#3a3a3a" stroke-width="8" fill="#5a7aa8"/></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="650" cy="${G - 200}" r="700" fill="url(#erLamp)" style="mix-blend-mode:screen"/><circle cx="650" cy="${G - 530}" r="300" fill="url(#erLamp)" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- the ward ----------------
  function ward2(L, o = {}) {
    const id = o.id || "wd", r = mk(o.seed || 39), G = o.ground ?? 1500, t = o.time || "night", BX = o.bed ?? 560, WX = o.window ?? 800;
    const SKY = t === "dawn" ? "wdDawn" : t === "day" ? "wdDay" : "wdNight";
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${SKY})"/>`;
    if (t === "night") for (let k = 0; k < 40; k++) sky += `<circle cx="${f1(WX - 300 + r() * 600)}" cy="${f1(100 + r() * 600)}" r="${f1(1 + r() * 1.5)}" fill="#e8ecff" opacity="${f1(0.3 + r() * 0.5)}"/>`;
    sky += Array.from({ length: 6 }, (_, k) => `<path d="${blob(WX - 400 + k * 160, 760 + r() * 60, 90 + r() * 40, r, 8)}" fill="${t === "day" ? "#5a7a5a" : "#05080c"}"/>`).join("");
    put(L.sky, sky);
    // the outside eyes sit behind the glass
    const eyesG = o.eyes ? Pop2.eyePair(WX + 20, 600, 1.6, `${id}-eyes`) : "";
    // the wall with the window cut out, the window frame with blinds half up
    let s = `<defs><mask id="${id}-wm"><rect x="-1300" y="-900" width="3700" height="3900" fill="#fff"/><rect x="${WX - 210}" y="260" width="420" height="560" fill="#000"/></mask></defs>
      <rect x="-1300" y="-900" width="3700" height="${G + 900}" fill="url(#${t === "night" ? "wdWallN" : "wdWallD"})" mask="url(#${id}-wm)"/>`;
    s += `<rect x="-1300" y="${G - 300}" width="3700" height="20" fill="${t === "night" ? "#1a2624" : "#5a7a70"}"/>`;
    s += `<rect x="${WX - 222}" y="248" width="444" height="584" fill="none" stroke="#e8ece8" stroke-width="22"/><path d="M${WX},260V820" stroke="#e8ece8" stroke-width="12"/>`;
    s += `<g opacity=".95">${Array.from({ length: 7 }, (_, k) => `<rect x="${WX - 210}" y="${260 + k * 26}" width="420" height="20" fill="${t === "night" ? "#4a5a58" : "#d8dcd4"}"/>`).join("")}<path d="M${WX - 180},260V440M${WX + 180},260V440" stroke="#9a9e98" stroke-width="2"/></g>`;
    if (o.print) s += `<g id="${id}-print" opacity=".85"><g transform="translate(${WX + 40},600) rotate(-8)"><path d="M-40,60Q-56,0 -40,-40Q-10,-60 30,-50Q56,-30 50,20Q44,70 10,84Q-30,90 -40,60Z" fill="#c8d8d0" opacity=".55"/>
      ${[[-34, -36, -58, -170], [-12, -52, -16, -200], [10, -54, 18, -196], [30, -44, 50, -166], [48, -2, 110, -60]].map(([x0, y0, x1, y1]) => `<path d="M${x0},${y0}L${x1},${y1}" stroke="#c8d8d0" stroke-width="14" stroke-linecap="round" opacity=".55"/>`).join("")}</g></g>`;
    // floor
    s += `<rect x="-1300" y="${G - 280}" width="3700" height="1800" fill="url(#wdFloor)"/>${Array.from({ length: 12 }, (_, k) => `<path d="M-1300,${G - 280 + Math.pow(k / 11, 1.5) * 900}H2400" stroke="#4a5652" stroke-width="2" opacity=".5"/>`).join("")}`;
    // the monitor on its arm, the IV pole
    s += `<g transform="translate(${WX + 360},${G - 700})"><rect x="-90" y="-70" width="180" height="140" rx="12" fill="#1a1e22" stroke="#3a3e42" stroke-width="6"/><rect x="-76" y="-56" width="152" height="100" fill="#06100c"/>
      <g id="${id}-ecg"><path d="M-76,0h30l8,-24l8,44l8,-30l6,10h40l8,-24l8,44l8,-30l6,10h22" stroke="#4aff7a" stroke-width="3" fill="none"/></g><text x="50" y="-30" font-family="Kanit" font-weight="700" font-size="24" fill="#4aff7a">88</text><path d="M0,70V300" stroke="#8a8e92" stroke-width="10"/></g>`;
    s += `<g id="${id}-iv"><g transform="translate(${BX - 330},${G})"><path d="M0,0V-900" stroke="#b8bcc0" stroke-width="10"/><path d="M-40,-900H40" stroke="#b8bcc0" stroke-width="8"/><path d="M-34,-890Q-40,-760 0,-740Q40,-760 34,-890Z" fill="#e8f4f8" opacity=".8" stroke="#8a9a9e" stroke-width="3"/>
      <path d="M0,-740Q30,-500 ${o.lineTo ?? 220},-460" stroke="#d8e8ec" stroke-width="4" fill="none"/><path d="M-60,0h120" stroke="#8a8e92" stroke-width="10"/></g></g>`;
    // the bed: frame, mattress, pillow, sheet; rails
    s += `<g transform="translate(${BX},${G})"><ellipse cx="0" cy="10" rx="440" ry="40" fill="#000" opacity=".4"/><path d="M-400,0V-200M400,0V-200" stroke="#8a8e92" stroke-width="16"/><path d="M-420,-200H420V-250H-420Z" fill="#c8ccd0" stroke="#6a6e72" stroke-width="5"/>
      <path d="M-410,-250H410V-300H-410Z" fill="#f2f4f2"/><path d="M-400,-330Q-400,-300 -300,-300H-220Q-200,-330 -240,-350H-380Z" fill="#fbfbf8" stroke="#c8ccc8" stroke-width="3"/>
      <path d="M-420,-200V-420M420,-200V-380" stroke="#c8ccd0" stroke-width="16"/><path d="M-160,-262H320" stroke="#9ab8d0" stroke-width="16" opacity=".7"/>${[-360, -320, -280].map((wy) => `<circle cx="${wy}" cy="-20" r="20" fill="#3a3e42"/>`).join("")}</g>`;
    if (o.clock) { const [cx, cy, hh, mm] = o.clock; s += `<g transform="translate(${cx},${cy})"><circle r="62" fill="#f6f6f2" stroke="#3a3e42" stroke-width="8"/>${Array.from({ length: 12 }, (_, k) => `<path d="M0,-50v8" stroke="#3a3e42" stroke-width="4" transform="rotate(${k * 30})"/>`).join("")}<path d="M0,6V-30" stroke="#1a1e22" stroke-width="7" stroke-linecap="round" transform="rotate(${hh})"/><path d="M0,8V-46" stroke="#1a1e22" stroke-width="4" stroke-linecap="round" transform="rotate(${mm})"/><circle r="5" fill="#c8202a"/></g>`; }
    // the curtain at the left on its rail
    s += `<path d="M-1300,140H${BX - 380}" stroke="#c8ccd0" stroke-width="10"/><g id="${id}-curtain">${Array.from({ length: 6 }, (_, k) => `<path d="M${-900 + k * 90},150Q${-860 + k * 90},${G - 200} ${-900 + k * 90 + (k % 2 ? 30 : -20)},${G - 120}L${-810 + k * 90},${G - 120}Q${-830 + k * 90},${G - 200} ${-810 + k * 90},150Z" fill="url(#wdCurtain)" opacity=".95"/>`).join("")}</g>`;
    put(L.set, s);
    let gl = `<circle cx="${BX}" cy="120" r="900" fill="url(#wdTube)" opacity="${t === "night" ? 0.55 : 0.9}" style="mix-blend-mode:screen"/><rect x="${BX - 260}" y="110" width="520" height="24" rx="12" fill="#f4fffa" opacity=".9"/>`;
    if (t === "dawn") gl += `<path d="M${WX - 210},260L${WX + 210},260L${WX - 300},${G + 400}L${WX - 900},${G + 400}Z" fill="#ffb878" opacity=".12" style="mix-blend-mode:screen"/>`;
    put(L.glow, gl + eyesG);
  }

  // ---------------- knowledge laid out on the bench, from above ----------------
  function benchTop(L, o = {}) {
    const id = o.id || "bt", r = mk(o.seed || 71), UI = PopUI.ICON, ok = o.ok || [];
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#2a1a0e"/>`);
    let s = "";
    for (let k = 0; k < 40; k++) s += `<rect x="-1300" y="${-900 + k * 96}" width="3700" height="90" fill="url(#bnSlat)"/><path d="M-1300,${-900 + k * 96 + 90}H2400" stroke="#5a3a1a" stroke-width="6"/>`;
    for (let k = 0; k < 30; k++) s += `<path d="M${f1(-200 + r() * 1500)},${f1(r() * 2000)}h${f1(60 + r() * 200)}" stroke="#8a6a3a" stroke-width="2" opacity=".5"/>`;
    (o.items || []).forEach(([x, y, label, kind], i) => {
      s += `<g id="${id}-t${i}"><g transform="translate(${x},${y})"><ellipse cx="14" cy="22" rx="210" ry="170" fill="#000" opacity=".3"/><path d="M-200,-150Q0,-180 200,-150L190,160Q0,190 -200,160Z" fill="url(#bnLeaf)" stroke="#2a5a1a" stroke-width="4"/><path d="M-196,0H196" stroke="#2a5a1a" stroke-width="5" opacity=".6"/>
        ${UI[kind](0, -10, 2.4)}<text x="0" y="230" text-anchor="middle" font-family="Mali" font-weight="700" font-size="50" fill="#fff6e0" stroke="#3a2210" stroke-width="10" paint-order="stroke">${label}</text></g></g>`;
      s += ok.includes(i) ? `<g id="${id}-x${i}" opacity="0"><g transform="translate(${x + 130},${y - 120})"><circle r="64" fill="#3aa84a" stroke="#fff" stroke-width="8"/><path d="M-28,0l18,20l36,-40" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>`
        : `<g id="${id}-x${i}" opacity="0"><g transform="translate(${x},${y - 10})"><circle r="150" fill="none" stroke="#e8302a" stroke-width="16" opacity=".9"/><path d="M-100,-100L100,100" stroke="#e8302a" stroke-width="18" stroke-linecap="round"/></g></g>`;
    });
    if (o.verdict) s += `<g id="${id}-verdict" opacity="0"><g transform="translate(540,${o.verdictY ?? 1400}) rotate(-4)"><rect x="-${o.verdictW ?? 340}" y="-90" width="${(o.verdictW ?? 340) * 2}" height="150" rx="20" fill="${o.verdictC || "#e8302a"}"/><text x="0" y="22" text-anchor="middle" font-family="Mali" font-weight="700" font-size="78" fill="#fff">${o.verdict}</text></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="300" cy="200" r="1100" fill="url(#kiLampGlow)" opacity=".35" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- props ----------------
  Object.assign(Pop2.PROP, {
    saltGlass: () => `<g transform="translate(0,104)"><path d="M-22,-40L-18,30H18L22,-40Z" fill="#dff0f8" opacity=".85" stroke="${LN}" stroke-width="2.4"/><path d="M-20,-14H20" stroke="#fff" stroke-width="2" opacity=".7"/><path d="M-19,-10L-17,28H17L19,-10Z" fill="#c8e4f0" opacity=".7"/></g>`,
    bag: () => `<g transform="translate(0,120)"><path d="M-40,-20H40L44,70Q0,80 -44,70Z" fill="#e8f4f8" opacity=".85" stroke="${LN}" stroke-width="2.4"/><path d="M-40,-20H40" stroke="#4a8ad8" stroke-width="6"/><g transform="translate(-8,40) scale(.16)">${Pop2.mush2(0, 0, 1, { v: "open", dirt: false })}</g><g transform="translate(18,52) scale(.12)">${Pop2.mush2(0, 0, 1, { v: "button", dirt: false })}</g></g>`,
  });
  const BASIN = `<g><ellipse cx="0" cy="0" rx="110" ry="26" fill="#3a6a9a" stroke="${LN}" stroke-width="3"/><path d="M-110,0L-90,60H90L110,0" fill="#4a7aaa" stroke="${LN}" stroke-width="3"/><ellipse cx="0" cy="2" rx="96" ry="18" fill="#2a4a6a"/></g>`;

  // ---------------- icons for EP.2/EP.3 knowledge ----------------
  const ICON = PopUI.ICON, INK = "#3a2a22", O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const at = (x, y, s, g) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`;
  Object.assign(ICON, {
    throat: (x, y, s = 1) => at(x, y, s, `<path d="M-30,-40Q-10,-46 6,-36Q20,-24 14,-6Q30,4 26,20Q20,40 -6,42Q-30,40 -34,10Z" fill="#f2c8a8" ${O()}/><path d="M-4,8q10,-4 16,4" ${O(3)} fill="none"/><path d="M28,-30L6,-4" stroke="${INK}" stroke-width="9" stroke-linecap="round"/><path d="M28,-30L6,-4" stroke="#f2c8a8" stroke-width="4" stroke-linecap="round"/>`),
    saltglass: (x, y, s = 1) => at(x, y, s, `<path d="M-24,-36L-18,40H18L24,-36Z" fill="#dff0f8" ${O()}/><path d="M-22,-10H22" stroke="#9ac8e0" stroke-width="3"/><path d="M-20,-6L-17,38H17L20,-6Z" fill="#b8dcec"/>${[[-8, 10], [6, 20], [-2, 28], [10, 4]].map(([a, b]) => `<rect x="${a}" y="${b}" width="5" height="5" fill="#fff"/>`).join("")}`),
    lungs: (x, y, s = 1) => at(x, y, s, `<path d="M-6,-40V-10M6,-40V-10" ${O(5)}/><path d="M-8,-12Q-40,-30 -40,10Q-40,40 -10,36Q-6,10 -8,-12Z" fill="#f4a0a8" ${O()}/><path d="M8,-12Q40,-30 40,10Q40,40 10,36Q6,10 8,-12Z" fill="#f4a0a8" ${O()}/><path d="M26,-40l18,32h-36z" fill="#ffd84a" ${O(3)}/><path d="M26,-30v10M26,-14v1" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`),
    vomit: (x, y, s = 1) => at(x, y, s, `<circle cx="-6" cy="-6" r="32" fill="#c8e0a0" ${O()}/><circle cx="-16" cy="-14" r="4" fill="${INK}"/><circle cx="6" cy="-14" r="4" fill="${INK}"/><path d="M-14,8q8,-8 16,0" ${O(4)} fill="none"/><path d="M16,10q18,4 26,24q-14,6 -26,-6z" fill="#a8c860" ${O(3)}/>`),
    bag: (x, y, s = 1) => at(x, y, s, `<path d="M-30,-30H30L34,40Q0,48 -34,40Z" fill="#e8f4f8" ${O()}/><path d="M-30,-30H30" stroke="#4a8ad8" stroke-width="7"/>${ICON.mush(0, 10, 0.5)}`),
    photo: (x, y, s = 1) => at(x, y, s, `<rect x="-26" y="-42" width="52" height="84" rx="9" fill="#22262c" ${O()}/><rect x="-21" y="-34" width="42" height="64" rx="4" fill="#cfe4ff"/>${ICON.mush(0, -2, 0.4)}`),
    people: (x, y, s = 1) => at(x, y, s, `<circle cx="-16" cy="-18" r="14" fill="#f2c8a8" ${O(3)}/><path d="M-38,30Q-38,-2 -16,-2Q6,-2 6,30Z" fill="#8ab4d8" ${O(3)}/><circle cx="18" cy="-12" r="12" fill="#c99a74" ${O(3)}/><path d="M0,34Q0,6 18,6Q36,6 36,34Z" fill="#c8a4d8" ${O(3)}/>`),
    form: (x, y, s = 1) => at(x, y, s, `<rect x="-30" y="-40" width="60" height="80" rx="6" fill="#fffaf0" ${O()}/><rect x="-14" y="-46" width="28" height="12" rx="4" fill="#b8bcc0" ${O(3)}/><path d="M-18,-16h36M-18,0h36M-18,16h24" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`),
    liver: (x, y, s = 1) => at(x, y, s, `<path d="M-40,-6Q-36,-34 0,-30Q40,-30 40,-10Q34,20 -6,26Q-40,26 -40,-6Z" fill="#a84a3a" ${O()}/><path d="M-20,-16q14,6 30,0" stroke="#d8806a" stroke-width="4" fill="none"/>`),
    doctor: (x, y, s = 1) => at(x, y, s, `<circle cy="-18" r="18" fill="#e2b28c" ${O(3)}/><path d="M-32,38Q-32,4 0,4Q32,4 32,38Z" fill="#f6f6f2" ${O(3)}/><path d="M-14,8Q-18,30 0,32Q18,30 14,8" stroke="#3a3a3a" stroke-width="3" fill="none"/>`),
    bowl: (x, y, s = 1) => at(x, y, s, `<path d="M-40,-6Q-40,34 0,36Q40,34 40,-6Z" fill="#f2ece0" ${O()}/><path d="M-38,8h76" stroke="#3a6a9a" stroke-width="5"/><ellipse cx="0" cy="-6" rx="40" ry="10" fill="#c8902e" ${O(3)}/><ellipse cx="-12" cy="-8" rx="10" ry="4" fill="#f2e8d4"/><path d="M-6,-24q6,-10 0,-18M10,-24q6,-10 0,-18" stroke="#9aa0a6" stroke-width="3" fill="none"/>`),
    trend: (x, y, s = 1) => at(x, y, s, `<rect x="-40" y="-36" width="80" height="72" rx="8" fill="#fffaf0" ${O(3)}/><path d="M-30,10L-14,-14L0,-4L14,-20L30,24" stroke="#e8302a" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`),
  });

  Object.assign(Sets, { nightRoad2, cab2, erFront2, ward2, benchTop });
  Object.assign(Pop2, { truck, BASIN });
})();
