// "เห็ดปอบ" v2 — EP.2/EP.3 sets: the night road and ลุงทองดี's pickup, the cab in dashboard light, the district hospital's
// emergency entrance, the ward (night / dawn / day), and knowledge laid out on a surface.
//   Sets.nightRoad2(L, o)  dark paddies under the moon, a dirt road, roadside posts #id-posts (scroll x), the pickup #id-truck at o.x
//                          (o.s scale ≈ 2.25 × the characters' scale, o.flip faces left, o.driver "sil"|false, headlights in the glow
//                          layer, o.bedFront / o.doorFront redraw the bed wall / cab door over actors in #id-truckF)
//   Sets.cab2(L, o)        the driver through the windshield at night: wheel, hands, dashboard glow, rear window with the passengers
//   Sets.erFront2(L, o)    the emergency entrance: canopy, the red sign, glass doors lit, a wheelchair, moths round the lamp
//   Sets.ward2(L, o)       o.time night | dawn | day · o.bed x · o.window x · o.print (a long-fingered handprint on the glass #id-print)
//                          o.eyes (green eyes outside #id-eyes) · the monitor's trace #id-ecg · the curtain #id-curtain
//   Sets.benchTop(L, o)    items on the bamboo bench seen from above: o.items [[x, y, label, icon], …] → #id-t0.., stamps #id-x0..,
//                          o.verdict text #id-verdict (o.verdictY), o.ok [i…] items that get a green tick instead of a red ring
//   Pop2.truck(o)          the pickup, side view facing right, wheels on y 0; o.part door|bed for overlays (see below)
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
    <linearGradient id="trBody" gradientUnits="userSpaceOnUse" x1="0" y1="-310" x2="0" y2="0"><stop offset="0" stop-color="#e2e4e6"/><stop offset=".35" stop-color="#c4c8cc"/><stop offset=".55" stop-color="#9a9ea2"/><stop offset="1" stop-color="#5e6266"/></linearGradient>
    <radialGradient id="trRim" cx=".4" cy=".35"><stop offset="0" stop-color="#e8eaec"/><stop offset="1" stop-color="#8a8e92"/></radialGradient>
    <linearGradient id="trGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a3a4e"/><stop offset=".5" stop-color="#121a24"/><stop offset="1" stop-color="#0a0e14"/></linearGradient>
    <linearGradient id="trBodyFront" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22252a"/><stop offset=".12" stop-color="#4a4e56"/><stop offset=".5" stop-color="#2a2d32"/><stop offset=".88" stop-color="#4a4e56"/><stop offset="1" stop-color="#1e2024"/></linearGradient>
    <linearGradient id="trBonnet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a5e66"/><stop offset=".25" stop-color="#3a3e44"/><stop offset="1" stop-color="#121418"/></linearGradient>
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

  // ---------------- the pickup: a Thai single-cab seen from its right (driver's) side, facing right, wheels on y 0 ----------------
  //   1 unit ≈ 6 mm at s 1 (5.3 m long, 1.85 m to the roof); a 1.65 m rig character at scale c stands beside a truck at s ≈ 2.25·c.
  //   o.driver "sil" draws a hatted silhouette behind the side glass; o.part "door" | "bed" returns only that near panel, to be
  //   drawn again over actors so a driver sits behind the door and passengers sit inside the bed.
  const TR = { xF: 290, xR: -228, sill: -80, belt: -206 };
  function truck(o = {}) {
    const c = o.color || "url(#trBody)", { xF, xR, sill, belt } = TR;
    const wheel = (x) => `<path d="M${x + 78},${sill}A80,80 0 0 0 ${x - 78},${sill}Z" fill="#08080a"/><circle cx="${x}" cy="-64" r="64" fill="#161618" stroke="${LN}" stroke-width="4"/>
      <circle cx="${x}" cy="-64" r="52" fill="none" stroke="#242428" stroke-width="5"/><circle cx="${x}" cy="-64" r="36" fill="url(#trRim)" stroke="#3a3c40" stroke-width="2"/>
      ${[0, 72, 144, 216, 288].map((a) => `<path d="M${x},-72V-94" stroke="#5a5c60" stroke-width="8" stroke-linecap="round" transform="rotate(${a} ${x} -64)"/>`).join("")}<circle cx="${x}" cy="-64" r="11" fill="#3a3c40"/>
      <path d="M${x + 88},${sill}A88,88 0 0 0 ${x - 88},${sill}" stroke="#2a2c30" stroke-width="12" fill="none"/>`;
    const mud = (x0, x1) => `<g fill="#4a3a2c" opacity=".55">${Array.from({ length: 7 }, (_, k) => `<ellipse cx="${f1(x0 + ((x1 - x0) * (k + 0.5)) / 7)}" cy="${sill - 6 - (k % 3) * 7}" rx="${9 + (k % 2) * 6}" ry="4"/>`).join("")}</g>`;
    const bed = `<path d="M-444,${sill}V-204H-30V${sill}H${xR + 78}A80,80 0 0 0 ${xR - 78},${sill}Z" fill="${c}" stroke="${LN}" stroke-width="4"/>
      <path d="M-444,-204H-30V-192H-444Z" fill="#eef0f2" opacity=".8"/><path d="M-432,-192V-90" stroke="${LN}" stroke-width="2.5" opacity=".45"/>
      <path d="M-444,-152H-30" stroke="#fff" stroke-width="3" opacity=".2"/><path d="M-444,-147H-30" stroke="#4a4e52" stroke-width="2" opacity=".45"/>
      <rect x="-448" y="-190" width="16" height="58" rx="4" fill="#d8281e" stroke="${LN}" stroke-width="3"/><rect x="-448" y="-132" width="16" height="16" rx="3" fill="#ece4d4" stroke="${LN}" stroke-width="2"/>
      <path d="M-454,-102H-398V${sill + 4}H-454Z" fill="#34363a" stroke="${LN}" stroke-width="3"/>${mud(-430, xR - 90)}${mud(xR + 90, -40)}${wheel(xR)}`;
    const doorLines = `<path d="M-6,${belt + 4}V-88M252,${belt + 2}Q246,-150 224,-104" stroke="${LN}" stroke-width="3" fill="none" opacity=".7"/>
      <rect x="14" y="-190" width="32" height="9" rx="4" fill="#4a4e52" stroke="${LN}" stroke-width="2"/>
      <path d="M-20,-152H254" stroke="#fff" stroke-width="3" opacity=".2"/><path d="M-20,-147H254" stroke="#4a4e52" stroke-width="2" opacity=".45"/>
      <path d="M-20,-98H${xF - 80}V${sill}H-20Z" fill="#2c2e32" opacity=".55"/>${mud(-10, xF - 90)}`;
    if (o.part === "bed") return bed;
    if (o.part === "door") return `<path d="M-20,${sill}V${belt}H254L262,-150L${xF - 78},${sill}Z" fill="${c}"/>${doorLines}
      <path d="M-20,${belt}H250" stroke="#1e2024" stroke-width="7"/><path d="M-20,${belt}V${sill}H${xF - 78}" stroke="${LN}" stroke-width="4" fill="none"/>`;
    let g = `<ellipse cx="0" cy="6" rx="470" ry="26" fill="#000" opacity=".55"/><path d="M-436,-86H444V-6H-436Z" fill="#060608" opacity=".92"/>
      <circle cx="${xR + 22}" cy="-60" r="58" fill="#0c0c0e"/><circle cx="${xF + 22}" cy="-60" r="58" fill="#0c0c0e"/>` + bed;
    g += `<path d="M-20,${sill}V-286Q-20,-302 -4,-303L138,-308Q152,-308 160,-300L270,-210L420,-196Q448,-192 448,-162V-104L442,${sill}H${xF + 78}A80,80 0 0 0 ${xF - 78},${sill}Z" fill="${c}" stroke="${LN}" stroke-width="4"/>`;
    g += `<path d="M2,${belt}V-284Q2,-292 10,-292L136,-297Q145,-297 151,-290L244,${belt}Z" fill="url(#trGlass)" stroke="${LN}" stroke-width="3"/>`;
    if (o.driver === "sil" || o.driver === true) g += `<g fill="#07090c"><path d="M44,${belt}Q48,-226 80,-228Q112,-226 116,${belt}Z"/><ellipse cx="80" cy="-240" rx="26" ry="30"/>
      <path d="M58,-258Q60,-286 80,-288Q100,-286 102,-258Z"/><path d="M30,-258Q80,-274 130,-258Q80,-248 30,-258Z"/></g><path d="M104,-262Q108,-240 98,-216" stroke="#7ae8ff" stroke-width="3" fill="none" opacity=".35"/>`;
    g += `<path d="M24,-212L62,-288M44,-212L74,-270" stroke="#fff" stroke-width="7" opacity=".1"/><path d="M-20,${belt}H250" stroke="#1e2024" stroke-width="7"/>`;
    g += doorLines;
    g += `<path d="M0,-301L136,-306" stroke="#fff" stroke-width="5" opacity=".35"/><path d="M262,-214L298,-332" stroke="#1e2024" stroke-width="2.5"/>`;
    g += `<path d="M246,-206l10,-6h28q9,0 9,9v20q0,9 -9,9h-26q-8,0 -10,-8z" fill="#1e2024" stroke="${LN}" stroke-width="3"/>`;
    g += `<path d="M410,-194L446,-189Q451,-172 445,-161L408,-167Z" fill="#fff6c8" stroke="${LN}" stroke-width="3"/><rect x="434" y="-158" width="13" height="12" rx="2" fill="#f0a030" stroke="${LN}" stroke-width="2"/>
      <path d="M446,-146V-114" stroke="${LN}" stroke-width="5"/><path d="M368,-114H452V-90Q452,${sill} 442,${sill}H368Z" fill="#34363a" stroke="${LN}" stroke-width="3"/>`;
    g += wheel(xF);
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
    const sc = o.s ?? 1, dd = o.flip ? -1 : 1, GT = G + 110, TT = `translate(${X},${GT}) scale(${dd * sc},${sc})`;
    if (o.truck !== false) s += `<g id="${id}-truck"><g transform="${TT}">${truck({ driver: o.driver ?? "sil" })}</g></g>`;
    s += `<rect x="-2000" y="${G + 120}" width="6000" height="900" fill="#080a08"/>`;
    for (let k = 0; k < 60; k++) s += Pop2.tuft(-1800 + r() * 5600, G + 140 + r() * 400, 1 + r(), "#0a120a", "#16221a", r);
    put(L.set, s);
    // the bed's near wall / the cab door drawn again over the actors, so passengers sit inside the bed and the driver behind the door
    if (o.truck !== false && (o.bedFront || o.doorFront)) put(L.glow, `<g id="${id}-truckF"><g transform="${TT}">${o.bedFront ? truck({ part: "bed" }) : ""}${o.doorFront ? truck({ part: "door" }) : ""}</g></g>`);
    // headlights and tail-lights, world-anchored
    if (o.truck !== false) {
      const d = dd, hx = X + d * 448 * sc, hy = GT - 178 * sc;
      put(L.glow, `<g id="${id}-lights" style="mix-blend-mode:screen"><path d="M${hx},${hy - 24}L${hx + d * 1700},${hy - 300}L${hx + d * 1700},${hy + 320}L${hx},${hy + 24}Z" fill="url(#${d > 0 ? "nrBeam" : "nrBeamL"})"/>
        <path d="M${hx},${hy - 12}L${hx + d * 1200},${hy - 120}L${hx + d * 1200},${hy + 160}L${hx},${hy + 12}Z" fill="url(#${d > 0 ? "nrBeam" : "nrBeamL"})"/>
        <ellipse cx="${hx + d * 700}" cy="${G + 60}" rx="700" ry="60" fill="#fff4d0" opacity=".25"/>
        <circle cx="${hx}" cy="${hy}" r="140" fill="url(#erLamp)"/><circle cx="${X - d * 446 * sc}" cy="${GT - 160 * sc}" r="${f1(60 + 50 * sc)}" fill="url(#nrTail)"/></g>
        <g id="${id}-dust" opacity=".5">${Array.from({ length: 10 }, (_, k) => `<circle cx="${f1(X - d * (480 + k * 60) * sc)}" cy="${f1(GT - 20 * sc - k * 6 - (k % 3) * 10)}" r="${f1((30 + k * 8) * sc)}" fill="#6a5a50" opacity="${f1(0.4 - k * 0.03)}"/>`).join("")}</g>`);
    }
  }

  // ---------------- inside the cab, seen through the windshield from the bonnet ----------------
  //   right-hand drive, so the driver is on the left of the frame; behind him the rear window shows the passengers in the bed.
  //   The steering wheel, his forearms and hands, the dashboard and the truck's body are in the fg layer (in front of the rig);
  //   the rig's own arms hang down behind the dashboard.
  //   ids: #id-refl (windshield reflections, slide in x), #id-garland (marigold garland on the mirror, swing about 560 584),
  //        #id-bed (the passengers through the rear window, bob in y)
  //   o.wheelX (driver / wheel centre, default 340), o.skin, o.sleeve (his hands and sleeves)
  function cab2(L, o = {}) {
    const id = o.id || "cb", r = mk(o.seed || 35), WX = o.wheelX ?? 340, sk = o.skin || "#a87048", sl = o.sleeve || "#7c6c52";
    const WS = "M160,470L920,470L1046,1392L34,1392Z";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#nrSky)"/><circle cx="700" cy="560" r="230" fill="url(#kiMoon)"/><circle cx="700" cy="560" r="22" fill="#f4f6ff"/>
      ${Array.from({ length: 30 }, () => `<circle cx="${f1(200 + r() * 700)}" cy="${f1(500 + r() * 300)}" r="${f1(1 + r() * 1.5)}" fill="#e8ecff" opacity="${f1(0.3 + r() * 0.5)}"/>`).join("")}`);
    // through the rear window: the dark road behind, the bed, and the two passengers in moonlight (Yai's bun, Mint's hair in the wind)
    const rim = `stroke="#9ab4e0" stroke-width="3" stroke-opacity=".55"`;
    put(L.far, `<g id="${id}-bed"><path d="M240,800H860V1000H240Z" fill="#0a0e14"/><path d="M300,860L780,860L860,960L220,960Z" fill="#3a3e44"/><path d="M300,860L780,860" stroke="#c8ccd0" stroke-width="5" opacity=".5"/>
      <circle cx="540" cy="808" r="40" fill="url(#nrTail)" opacity=".5"/>
      ${[[610, 1, "#7a6a9a", "#1a1418"], [730, 0.92, "#a8a49c", "#c8c4bc"]].map(([x, k, shirt, hair], n) => `<g transform="translate(${x},866) scale(${k})"><path d="M-40,10Q-44,-34 -26,-48Q0,-58 26,-48Q44,-34 40,10Z" fill="${shirt}" opacity=".85"/>
        <circle cy="-74" r="24" fill="#a88068"/><circle cx="-8" cy="-76" r="2.6" fill="#1a1210"/><circle cx="8" cy="-76" r="2.6" fill="#1a1210"/>
        ${n === 0 ? `<path d="M-26,-70Q-30,-104 0,-102Q30,-104 26,-70L30,-40Q22,-62 20,-84Q0,-94 -20,-84Q-22,-62 -30,-40Z" fill="${hair}"/><path d="M24,-90Q50,-96 70,-84Q50,-80 30,-74Z" fill="${hair}"/>`
          : `<path d="M-24,-80Q0,-104 24,-80Q14,-92 0,-92Q-14,-92 -24,-80Z" fill="${hair}"/><circle cy="-102" r="10" fill="${hair}"/>`}
        <path d="M-26,-90Q0,-108 26,-90" stroke="#9ab4e0" stroke-width="3" fill="none" opacity=".5"/></g>`).join("")}</g>`);
    // the cab: back wall with the rear window, headliner, seat backs and headrests
    put(L.set, `<path d="M-1300,-900H2400V2900H-1300Z M300,640H780Q800,640 800,660V880Q800,900 780,900H300Q280,900 280,880V660Q280,640 300,640Z" fill="#101216" fill-rule="evenodd"/>
      <path d="M300,640H780Q800,640 800,660V880Q800,900 780,900H300Q280,900 280,880V660Q280,640 300,640Z" fill="none" stroke="#24272c" stroke-width="16"/>
      <path d="M100,470H980V560Q540,590 100,560Z" fill="#2a2c30"/><path d="M120,556Q540,586 960,556" stroke="#3a3c42" stroke-width="4" fill="none"/>
      <g fill="#1a1c22" stroke="#26282e" stroke-width="4"><rect x="${WX - 190}" y="930" width="380" height="600" rx="40"/><rect x="${WX - 80}" y="822" width="160" height="120" rx="34"/>
        <rect x="${WX + 410}" y="930" width="360" height="600" rx="40"/><rect x="${WX + 510}" y="822" width="160" height="120" rx="34"/></g>
      <path d="M${WX + 430},980V1500M${WX + 750},980V1500" stroke="#24262c" stroke-width="5"/>`);
    // in front of him: the wheel, his forearms and hands on it, the dashboard, the windshield frame, the bonnet, the mirror and garland
    const ang = 48, R = 236, CY = 1478, gx = R * Math.sin((ang * Math.PI) / 180), gy = CY - R * Math.cos((ang * Math.PI) / 180);
    const skS = Rig2.shade(sk, 0.25), slS = Rig2.shade(sl, 0.3);
    // forearms rise from behind the dashboard (the elbows are below it) to the fists on the rim
    const arm = (sx, hx) => `<path d="M${sx},1520Q${(sx + hx) / 2 - (hx < WX ? 30 : -30)},1420 ${hx},${f1(gy + 10)}" stroke="${slS}" stroke-width="76" fill="none" stroke-linecap="round"/><path d="M${sx},1520Q${(sx + hx) / 2 - (hx < WX ? 30 : -30)},1420 ${hx},${f1(gy + 10)}" stroke="${sl}" stroke-width="62" fill="none" stroke-linecap="round"/>
      <path d="M${sx + (hx < WX ? 14 : -14)},1500Q${(sx + hx) / 2},1430 ${hx + (hx < WX ? 10 : -10)},${f1(gy + 30)}" stroke="#fff" stroke-width="8" fill="none" opacity=".12"/>`;
    const fist = (hx, flip) => `<g transform="translate(${f1(hx)},${f1(gy)}) scale(${flip ? -1 : 1},1)"><path d="M-34,-6Q-38,-34 -10,-38L22,-36Q40,-30 38,-8L36,22Q30,38 8,38H-20Q-38,32 -36,12Z" fill="${sk}" stroke="${LN}" stroke-width="4"/>
      <path d="M-30,6H30M-28,20H28" stroke="${skS}" stroke-width="4" stroke-linecap="round"/><path d="M-12,-36Q6,-50 26,-40" stroke="${skS}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M-34,-6Q-38,-34 -10,-38L22,-36Q40,-30 38,-8L36,22Q30,38 8,38H-20Q-38,32 -36,12Z" fill="url(#r2Cyl)" opacity=".6"/></g>`;
    let fg = `<circle cx="${WX}" cy="${CY}" r="${R}" fill="none" stroke="#0c0c0e" stroke-width="40"/><circle cx="${WX}" cy="${CY}" r="${R + 18}" fill="none" stroke="#7ae8ff" stroke-width="3" opacity=".25"/>`;
    fg += arm(WX - 190, WX - gx) + arm(WX + 190, WX + gx) + fist(WX - gx, false) + fist(WX + gx, true);
    fg += `<path d="M20,1392Q540,1360 1060,1392V1460H20Z" fill="#141518"/><path d="M${WX - 170},1392Q${WX},1320 ${WX + 170},1392Z" fill="#0e0f12"/><path d="M${WX - 150},1388Q${WX},1330 ${WX + 150},1388" stroke="#7ae8ff" stroke-width="4" fill="none" opacity=".5"/>`;
    const OUT = "M60,380Q540,350 1020,380L1150,1392V2900H-70V1392Z";
    fg += `<path d="M-1300,-900H2400V2900H-1300Z ${OUT}" fill="url(#nrSky)" fill-rule="evenodd"/>${Array.from({ length: 24 }, () => `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(-300 + r() * 640)}" r="${f1(1 + r() * 1.5)}" fill="#e8ecff" opacity="${f1(0.3 + r() * 0.5)}"/>`).join("")}
      <path d="${OUT} ${WS}" fill="url(#trBodyFront)" fill-rule="evenodd"/><path d="${WS}" fill="none" stroke="#14161a" stroke-width="22"/><path d="M70,384Q540,354 1010,384" stroke="#c8d0dc" stroke-width="5" fill="none" opacity=".35"/>
      <path d="M-1300,1392H2400V2900H-1300Z" fill="url(#trBonnet)"/><path d="M0,1440Q540,1404 1080,1440" stroke="#fff" stroke-width="5" opacity=".18" fill="none"/>
      <path d="M200,1384L520,1340M600,1384L900,1342" stroke="#0c0c0e" stroke-width="10" stroke-linecap="round"/>
      <path d="M150,470L-120,1392M930,470L1200,1392" stroke="#c8ccd0" stroke-width="4" opacity=".25"/>
      <g transform="translate(950,1300)"><circle r="44" fill="#f4f0e4" stroke="#2a6ad8" stroke-width="6"/><circle r="30" fill="none" stroke="#e8302a" stroke-width="4"/><path d="M-14,-6H14M-12,6H12" stroke="#2a2a2a" stroke-width="4"/></g>
      <path d="M560,470V528" stroke="#1a1c20" stroke-width="12"/><rect x="470" y="524" width="180" height="56" rx="16" fill="#1a1c20" stroke="#2a2c30" stroke-width="4"/><path d="M482,536H638" stroke="#7a8a9a" stroke-width="5" opacity=".5"/>
      <g id="${id}-garland"><path d="M548,580V640M572,580V640" stroke="#e8e0d0" stroke-width="2"/>
        ${Array.from({ length: 14 }, (_, k) => { const a = (k / 14) * 2 * Math.PI; return `<circle cx="${f1(560 + 34 * Math.sin(a))}" cy="${f1(676 + 30 * Math.cos(a))}" r="11" fill="${k % 2 ? "#f0a020" : "#f8c030"}" stroke="#a8601a" stroke-width="2"/>`; }).join("")}
        <path d="M552,708L540,770M568,708L582,766" stroke="#e8302a" stroke-width="7" stroke-linecap="round"/><circle cx="560" cy="712" r="12" fill="#f4f0e8" stroke="#a8601a" stroke-width="2"/></g>`;
    put(L.glow, fg);
    put(L.glow, `<clipPath id="${id}-ws"><path d="${WS}"/></clipPath><circle cx="${WX}" cy="1380" r="420" fill="url(#cbDash)" opacity=".55" style="mix-blend-mode:screen"/>
      <g clip-path="url(#${id}-ws)"><g id="${id}-refl" opacity=".9">${[0, 1, 2].map((k) => `<path d="M${-200 + k * 520},1400L${100 + k * 520},440L${170 + k * 520},440L${-130 + k * 520},1400Z" fill="#dfe8ff" opacity="${[0.07, 0.05, 0.06][k]}"/>`).join("")}</g></g>`);
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
