// ---------- นิวเคลียร์ลงกรุงเทพ EP.1 · storyboard sets and game-style UI (lane A experiment, 2 Nov; formula copied 1:1, our own designs) ----------
//   Sets.carFront(L, o)   the family seen through the windshield: rear window and back seat behind them; Nk2.cabinFront(layer, o) adds
//                         the dashboard, wheel, A-pillars and mirror over the actors (call it from fx so it covers their legs)
//   Sets.drivePOV(L, o)   the driver's view down the jammed expressway (Sets.xway) with the cabin around it · o.sign green sign text
//   Sets.xwaySide(L, o)   side view: the elevated expressway, its emergency stair, a tower with an underground-parking mouth, the mushroom far off
//   Sets.garage(L, o)     underground car park: beams, tubes, pillars, bays, parked cars, the ramp and its rolling shutter
//                         o.view "wide" | "shutter" | "pillar" · o.shutter 0..1 · o.chalk text on the pillar · o.dust under the shutter
//   Nk2.phone(x, y, s, screen)  a hand holding a phone · screen "black" | "alert" | "nosignal"
//   Nk2.radio(x, y, s) · Nk2.bag(x, y, s) · Nk2.dust(x, y, s) · Nk2.basket(x, y, s)
//   NkUI.title · miniMap · cityMap · rule · section · counter · chip · chain · notebook · endCard · logo   (screen-space; put in L.light)
(function () {
  const INK = "#14181a", INK2 = "#2e2a26", CREAM = "#f4ecd8", RED = "#d8443a", YEL = "#f2c55c", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const blob = Pop2.blob;
  const T = (x, y, s, txt, o = {}) => `<text x="${f1(x)}" y="${f1(y)}" font-family="Kanit" font-weight="${o.w || 800}" font-size="${s}" fill="${o.fill || INK2}" text-anchor="${o.anchor || "middle"}"${o.op ? ` opacity="${o.op}"` : ""}>${txt}</text>`;
  Sets.DEFS += `
    <linearGradient id="n2Sunset" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a6a"/><stop offset=".5" stop-color="#e08a5a"/><stop offset="1" stop-color="#ffd890"/></linearGradient>
    <linearGradient id="n2Dash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3e46"/><stop offset="1" stop-color="#15171b"/></linearGradient>
    <linearGradient id="n2Seat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a5e66"/><stop offset="1" stop-color="#34373e"/></linearGradient>
    <linearGradient id="n2Glare" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="n2Conc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a9a94"/><stop offset="1" stop-color="#6e6e6a"/></linearGradient>
    <linearGradient id="n2Floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e605e"/><stop offset="1" stop-color="#3a3c3c"/></linearGradient>
    <linearGradient id="n2Ceil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3e403e"/><stop offset="1" stop-color="#5a5c58"/></linearGradient>
    <radialGradient id="n2Tube"><stop offset="0" stop-color="#f4fff4" stop-opacity=".9"/><stop offset="1" stop-color="#d8f4e0" stop-opacity="0"/></radialGradient>
    <radialGradient id="n2Out"><stop offset="0" stop-color="#ffd08a" stop-opacity=".95"/><stop offset="1" stop-color="#ff8a3a" stop-opacity="0"/></radialGradient>
    <radialGradient id="n2MapBg" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#1c2a2c"/><stop offset="1" stop-color="#0a1012"/></radialGradient>
    <radialGradient id="n2Hot"><stop offset="0" stop-color="#ff5a3a" stop-opacity=".9"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="n2EndBg" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#1e2226"/><stop offset="1" stop-color="#08090b"/></radialGradient>
    <clipPath id="n2MiniClip"><circle cx="0" cy="0" r="1"/></clipPath>`;
  const Nk2 = {}, NkUI = {};

  // ---------- small icons (centre 0,0, ~60 px) ----------
  const ICON = {
    person: (c = INK2) => `<circle cx="0" cy="-16" r="11" fill="${c}"/><path d="M-18,22Q-18,-2 0,-2Q18,-2 18,22Z" fill="${c}"/>`,
    cat: (c = INK2) => `<path d="M-16,-10L-14,-26L-4,-16H4L14,-26L16,-10Q20,6 0,8Q-20,6 -16,-10Z" fill="${c}"/><path d="M-12,8Q-14,22 0,22Q14,22 12,8Z" fill="${c}"/>`,
    building: (c = INK2) => `<rect x="-16" y="-24" width="32" height="46" rx="3" fill="${c}"/>${[-14, -2, 10].map((y) => `<rect x="-10" y="${y}" width="7" height="6" fill="${CREAM}"/><rect x="3" y="${y}" width="7" height="6" fill="${CREAM}"/>`).join("")}`,
    car: (c = INK2) => `<path d="M-22,8V-2L-14,-14H14L22,-2V8Z" fill="${c}"/><circle cx="-12" cy="10" r="6" fill="${c}"/><circle cx="12" cy="10" r="6" fill="${c}"/><rect x="-10" y="-10" width="20" height="8" fill="${CREAM}"/>`,
    under: (c = INK2) => `<path d="M-24,-6H24" stroke="${c}" stroke-width="5"/><path d="M-18,0V20H18V0" fill="none" stroke="${c}" stroke-width="5"/><text x="0" y="16" font-family="Kanit" font-weight="900" font-size="18" text-anchor="middle" fill="${c}">P</text><path d="M-10,-12L0,-24L10,-12" fill="none" stroke="${c}" stroke-width="4"/>`,
    radio: (c = INK2) => `<rect x="-20" y="-10" width="40" height="28" rx="5" fill="${c}"/><path d="M-12,-10L10,-26" stroke="${c}" stroke-width="4"/><circle cx="-6" cy="4" r="7" fill="${CREAM}"/><rect x="6" y="-2" width="8" height="12" fill="${CREAM}"/>`,
    water: (c = INK2) => `<path d="M0,-24Q16,-2 14,8Q12,22 0,22Q-12,22 -14,8Q-16,-2 0,-24Z" fill="${c}"/>`,
    clock: (c = INK2) => `<circle r="18" fill="none" stroke="${c}" stroke-width="5"/><path d="M0,-10V0L8,6" stroke="${c}" stroke-width="5" fill="none" stroke-linecap="round"/>`,
    warn: (c = INK2) => `<path d="M0,-22L22,18H-22Z" fill="${c}"/><rect x="-3" y="-8" width="6" height="14" fill="${CREAM}"/><circle cy="12" r="3.5" fill="${CREAM}"/>`,
    info: (c = INK2) => `<circle r="16" fill="none" stroke="${c}" stroke-width="4"/><circle cy="-7" r="3" fill="${c}"/><rect x="-2.5" y="-2" width="5" height="12" fill="${c}"/>`,
    food: (c = INK2) => `<rect x="-18" y="-12" width="36" height="26" rx="5" fill="${c}"/><path d="M-12,-12V-20H12V-12" fill="none" stroke="${c}" stroke-width="4"/>`,
    torch: (c = INK2) => `<rect x="-6" y="-6" width="12" height="28" rx="3" fill="${c}"/><path d="M-12,-20H12L6,-6H-6Z" fill="${c}"/>`,
    pill: (c = INK2) => `<rect x="-20" y="-9" width="40" height="18" rx="9" fill="${c}"/><path d="M0,-9V9" stroke="${CREAM}" stroke-width="3"/>`,
    shirt: (c = INK2) => `<path d="M-20,-14L-8,-20H8L20,-14L26,0L16,4V22H-16V4L-26,0Z" fill="${c}"/>`,
  };
  NkUI.ICON = ICON;
  const badge = (x, y, ok) => `<g transform="translate(${x},${y})"><circle r="15" fill="${ok ? "#3aa86a" : RED}" stroke="${CREAM}" stroke-width="3"/>${ok ? `<path d="M-7,0L-2,5L7,-5" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>` : `<path d="M-6,-6L6,6M6,-6L-6,6" stroke="#fff" stroke-width="4" stroke-linecap="round"/>`}</g>`;
  const panel = (x, y, w, h, o = {}) => `<g filter="drop-shadow(0 8px 14px rgba(0,0,0,.45))"><rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" rx="${o.rx ?? 14}" fill="${o.fill || CREAM}" stroke="${o.stroke || "#c9bea6"}" stroke-width="3"/>${o.bar ? `<rect x="${f1(x)}" y="${f1(y)}" width="12" height="${f1(h)}" rx="6" fill="${RED}"/>` : ""}</g>`;

  // ---------- the car seen from the front ----------
  Sets.carFront = (L, o = {}) => {
    const r = mk(o.seed || 31);
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#n2Sunset)"/>`);
    // behind the car, seen through the rear window: the jam's headlights and towers
    // o.blast {id, x, y, s}: the mushroom over the city behind the car (the towers drop low so it reads at a glance)
    let far = o.blast ? `<g id="${o.blast.id}">${Nk.blastHTML(o.blast.x ?? 600, o.blast.y ?? 792, o.blast.s ?? 0.4, "mush", 11)}</g>` : "";
    const hk = o.blast || o.low ? 0.45 : 1;   // o.low: the same low skyline without the standing mushroom (a shot that stages its own)
    for (let k = 0; k < 9; k++) { const x = 160 + k * 100 + r() * 30, h = (120 + r() * 220) * hk; far += `<rect x="${f1(x)}" y="${f1(760 - h)}" width="${f1(70 + r() * 40)}" height="${f1(h)}" fill="#4a3a5a" opacity=".85"/>`; }
    for (let k = 0; k < 7; k++) { const x = 240 + k * 100, y = 740 + (k % 2) * 8; far += `<circle cx="${x - 16}" cy="${y}" r="9" fill="#fff4d0"/><circle cx="${x + 16}" cy="${y}" r="9" fill="#fff4d0"/><circle cx="${x}" cy="${y}" r="46" fill="url(#n2Out)" opacity=".5"/>`; }
    put(L.far, far);
    // cabin behind the family: headliner, rear window, back bench, front seat backs
    let s = `<path d="M-900,-600H2000V2600H-900ZM230,470Q240,420 300,416H780Q840,420 850,470L880,790H200Z" fill="#26282e" fill-rule="evenodd"/>
      <path d="M200,790H880" stroke="#15171b" stroke-width="10"/><path d="M230,470Q240,420 300,416H780Q840,420 850,470L880,790H200Z" fill="none" stroke="#15171b" stroke-width="10"/>
      <path d="M240,440L330,780M840,440L750,780" stroke="#fff" stroke-width="5" opacity=".08"/>
      <path d="M90,1060Q90,960 200,950H880Q990,960 990,1060V1300H90Z" fill="url(#n2Seat)" ${O(4)}/>
      <path d="M150,1000H930" stroke="#2a2c32" stroke-width="6" opacity=".6"/>`;
    [[300, 1], [780, 1]].forEach(([x]) => { s += `<path d="M${x - 170},1300V1010Q${x - 170},930 ${x - 90},920H${x + 90}Q${x + 170},930 ${x + 170},1010V1300Z" fill="url(#n2Seat)" ${O(4)}/>
        <rect x="${x - 70}" y="${o.headY ?? 830}" width="140" height="100" rx="34" fill="#4a4e56" ${O(4)}/><path d="M${x - 40},${(o.headY ?? 830) + 100}v24M${x + 40},${(o.headY ?? 830) + 100}v24" stroke="#8a8e96" stroke-width="8"/>`; });
    put(L.set, s);
  };
  // dashboard, wheel, pillars, mirror and windshield glare, drawn over the actors
  Nk2.cabinFront = (layer, o = {}) => {
    const wx = o.wheelX ?? 300, dy = (o.dashY ?? 1330) - 1330; // o.dashY raises the dash and wheel (hides seated legs)
    put(layer, `<g><g transform="translate(0,${dy})">
      <path d="M-900,1330Q540,1250 2000,1330V2600H-900Z" fill="url(#n2Dash)" ${O(5)}/><path d="M-900,1340Q540,1262 2000,1340" stroke="#5a5e66" stroke-width="8" fill="none"/>
      <rect x="430" y="1380" width="220" height="70" rx="14" fill="#0e1013" ${O(3)}/><text x="540" y="1428" font-family="Kanit" font-weight="800" font-size="34" fill="#7fd1ff" text-anchor="middle">${o.clock || "17:41"}</text>
      <g transform="translate(${wx},1420)"><ellipse rx="230" ry="200" fill="none" stroke="#0e1013" stroke-width="56"/><ellipse rx="230" ry="200" fill="none" stroke="#2c2f36" stroke-width="40"/>
        <path d="M-220,30Q0,90 220,30M0,90V200" stroke="#1c1e22" stroke-width="54" fill="none"/><ellipse rx="70" ry="56" fill="#1c1e22" ${O(3)}/></g></g>
      <path d="M-900,-600H2000V170Q540,110 -900,170Z" fill="#0e1013"/>
      <path d="M-120,-600L60,1330" stroke="#0e1013" stroke-width="150"/><path d="M1200,-600L1020,1330" stroke="#0e1013" stroke-width="150"/>
      <g transform="translate(540,250)"><path d="M0,-90V-30" stroke="#0e1013" stroke-width="16"/><rect x="-120" y="-34" width="240" height="70" rx="20" fill="#1c1e22" ${O(3)}/><rect x="-104" y="-22" width="208" height="46" rx="12" fill="#9fb3c4" opacity=".5"/></g>
      <path d="M140,180L420,180L120,1300L-160,1300Z" fill="url(#n2Glare)"/><path d="M700,180L860,180L640,1300L480,1300Z" fill="url(#n2Glare)" opacity=".7"/>
    </g>`);
  };

  // ---------- the driver's view ----------
  Sets.drivePOV = (L, o = {}) => {
    Sets.xway(L, { id: o.id || "dp", H: o.H ?? 1060, flash: o.flash ?? 0.15, day: o.day, maxD: 0.62, gantry: o.sign ? 0.3 : 0,
      blast: o.blast === false ? null : { stage: "mush", s: o.blastS ?? 0.2, dy: -6 }, skip: [[1, 0.58], [1, 0.44]], tailOp: 0.95 });
    if (o.sign) { const gd = 0.3, H = o.H ?? 1060, Y = H + (1960 - H) * gd, gy = Y - 900 * gd;
      put(L.set, `<rect x="${f1(540 - 330)}" y="${f1(gy + 6)}" width="660" height="${f1(84)}" rx="10" fill="#1e7a4a" stroke="#f4f2ea" stroke-width="5"/>${T(540, gy + 64, 46, o.sign, { fill: "#f4f2ea", w: 800 })}`); }
    put(L.act, `<g>
      <path d="M-900,-600H2000V230Q540,150 -900,230Z" fill="#0e1013"/>
      <path d="M-120,-600L80,1560" stroke="#0e1013" stroke-width="170"/><path d="M1200,-600L1000,1560" stroke="#0e1013" stroke-width="170"/>
      <g transform="translate(540,330)"><path d="M0,-110V-40" stroke="#0e1013" stroke-width="16"/><rect x="-140" y="-44" width="280" height="80" rx="22" fill="#1c1e22" ${O(3)}/><rect x="-122" y="-30" width="244" height="54" rx="14" fill="#c8a07a" opacity=".55"/></g>
      <path d="M-900,1560Q540,1470 2000,1560V2600H-900Z" fill="url(#n2Dash)" ${O(5)}/>
      <g transform="translate(560,1900)"><ellipse rx="420" ry="360" fill="none" stroke="#0e1013" stroke-width="70"/><ellipse rx="420" ry="360" fill="none" stroke="#2c2f36" stroke-width="50"/><ellipse rx="110" ry="90" cy="40" fill="#1c1e22"/></g>
      <path d="M160,240L470,240L160,1560L-150,1560Z" fill="url(#n2Glare)"/></g>`);
  };

  // ---------- a hand holding a phone ----------
  Nk2.phone = (x, y, s, screen = "black", o = {}) => {
    let scr = `<rect x="-128" y="-268" width="256" height="536" rx="30" fill="#0b0d10"/>`;
    if (screen === "black") scr += `<path d="M-100,-250L60,-250L-100,40Z" fill="#fff" opacity=".06"/>`;
    if (screen === "alert" || screen === "nosignal") scr += `<rect x="-128" y="-268" width="256" height="536" rx="30" fill="${screen === "alert" ? "#1a0e10" : "#14181c"}"/>
      ${T(-100, -232, 20, o.clock || "17:43", { fill: "#f4ecd8", anchor: "start", w: 700 })}${T(100, -232, 18, screen === "nosignal" ? "ไม่มีบริการ" : "●●●", { fill: "#f4ecd8", anchor: "end", w: 600 })}`;
    if (screen === "alert") scr += `<rect x="-112" y="-200" width="224" height="380" rx="22" fill="#c8302a" stroke="#ff8a7a" stroke-width="3"/>
      <g transform="translate(0,-130) scale(1.6)">${ICON.warn("#fff4ea")}</g>${T(0, -48, 22, "แจ้งเตือนฉุกเฉิน", { fill: "#ffe0d8", w: 700 })}
      ${T(0, 14, 54, "เข้าอาคาร", { fill: "#fff", w: 900 })}${T(0, 74, 54, "ทันที", { fill: "#fff", w: 900 })}${T(0, 132, 22, "อยู่ข้างใน · ฟังประกาศ", { fill: "#ffe0d8", w: 600 })}
      <rect x="-90" y="200" width="180" height="44" rx="22" fill="#3a1a1c"/>${T(0, 230, 22, "ตกลง", { fill: "#ffd0c8", w: 700 })}`;
    if (screen === "nosignal") scr += `<g transform="translate(0,-40)">${[0, 1, 2, 3].map((k) => `<rect x="${-54 + k * 30}" y="${30 - k * 26}" width="20" height="${30 + k * 26}" rx="4" fill="#5a6068"/>`).join("")}<path d="M-70,-70L70,70" stroke="${RED}" stroke-width="12" stroke-linecap="round"/></g>
      ${T(0, 120, 40, "ไม่มีสัญญาณ", { fill: "#f4ecd8", w: 900 })}${T(0, 160, 22, "โทรออกไม่ได้ · ไม่มีอินเทอร์เน็ต", { fill: "#9aa2aa", w: 600 })}`;
    const skin = o.skin || "#d8a070", skinS = o.skinS || "#b47e52";
    return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${o.rot ?? -8}) scale(${s})">
      <path d="M-60,240Q-40,520 60,700H330Q300,500 210,300Z" fill="${o.sleeve || "#f2f0ea"}" ${O(5)}/>
      <rect x="-142" y="-284" width="284" height="568" rx="40" fill="#1a1c20" ${O(5)}/>${scr}
      <path d="M-170,-40Q-190,-10 -176,20L-146,30Q-130,0 -142,-34Z" fill="${skin}" ${O(4)}/><path d="M-176,60Q-196,90 -180,120L-146,124Q-132,96 -142,66Z" fill="${skin}" ${O(4)}/>
      <path d="M150,-20Q196,-6 204,40L210,220Q200,300 120,330L-40,300Q-120,270 -150,190L-146,150Q-60,200 40,190Q120,170 140,90Z" fill="${skin}" ${O(5)}/>
      <path d="M126,120Q170,90 206,110" stroke="${skinS}" stroke-width="6" fill="none"/><path d="M150,-20Q120,10 136,60" stroke="${skinS}" stroke-width="5" fill="none"/></g>`;
  };
  Nk2.radio = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-60,-120L-30,-300" stroke="#9aa2aa" stroke-width="12" stroke-linecap="round"/><circle cx="-30" cy="-304" r="12" fill="#9aa2aa"/>
    <rect x="-150" y="-130" width="300" height="200" rx="26" fill="#c8302a" ${O(5)}/><rect x="-126" y="-104" width="250" height="148" rx="16" fill="#2a1c1c"/>
    ${Array.from({ length: 6 }, (_, k) => `<path d="M${-106},${-82 + k * 22}h110" stroke="#5a3a3a" stroke-width="8" stroke-linecap="round"/>`).join("")}<rect x="30" y="-90" width="80" height="40" rx="8" fill="#b9e8a8"/>${T(70, -62, 24, "FM", { w: 900 })}
    <circle cx="70" cy="10" r="26" fill="#e9e4cf" ${O(4)}/><path d="M70,-6v16" stroke="${INK}" stroke-width="5"/></g>`;
  Nk2.bag = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-70,0Q-90,-120 -40,-170L-10,-200L10,-200L40,-170Q90,-120 70,0Z" fill="#1c1e22" ${O(5)}/><path d="M-14,-200L-30,-236M14,-200L30,-236" stroke="#1c1e22" stroke-width="12" stroke-linecap="round"/><path d="M-40,-120Q-20,-80 -30,-30" stroke="#5a5e66" stroke-width="6" fill="none"/></g>`;
  Nk2.dust = (x, y, s, seed = 3) => { const r = mk(seed); let g = ""; for (let k = 0; k < 26; k++) g += `<circle cx="${f1((r() - 0.5) * 120)}" cy="${f1((r() - 0.5) * 40)}" r="${f1(3 + r() * 6)}" fill="#b8b4a8" opacity="${f1(0.6 + r() * 0.4)}"/>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`; };
  Nk2.basket = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-110,0L-96,-90H96L110,0Z" fill="#c8964e" ${O(5)}/>${[-60, -20, 20, 60].map((xx) => `<path d="M${xx},-88V-2" stroke="#9a6a32" stroke-width="6"/>`).join("")}<path d="M-96,-90Q0,-170 96,-90" stroke="#9a6a32" stroke-width="10" fill="none"/></g>`;

  // ---------- side view: the deck, its emergency stair, the tower with a parking mouth ----------
  Sets.xwaySide = (L, o = {}) => {
    const r = mk(o.seed || 41), G = o.ground ?? 1640, XY = o.xway ?? 860;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#nkSkyHot)"/><circle cx="${o.blastX ?? 200}" cy="300" r="900" fill="url(#nkBloom)" opacity=".35"/>`);
    let far = Nk.blastHTML(o.blastX ?? 200, G - 380, o.blastS ?? 0.55, "mush", 11);
    for (let k = 0; k < 18; k++) { const x = -400 + k * 110 + r() * 40, w = 80 + r() * 90, h = 260 + r() * 520; far += `<rect x="${f1(x)}" y="${f1(G - 300 - h)}" width="${f1(w)}" height="${f1(h + 40)}" fill="url(#nkTower)"/>`; }
    put(L.far, far);
    let s = `<rect x="-1300" y="${G - 40}" width="3700" height="900" fill="#5a5052"/><path d="M-1300,${G - 40}H2400" stroke="#e8c03a" stroke-width="8"/>`;
    // the tower on the right with the parking mouth
    s += `<rect x="640" y="${G - 1500}" width="700" height="1460" fill="#8a8a90" ${O(4)}/>`;
    for (let j = 0; j < 14; j++) s += `<path d="M640,${G - 1440 + j * 100}H1340" stroke="#6a6a70" stroke-width="6"/>`;
    s += `<path d="M700,${G - 40}V${G - 300}Q700,${G - 360} 760,${G - 360}H1000Q1060,${G - 360} 1060,${G - 300}V${G - 40}Z" fill="#14161a" ${O(5)}/>
      <path d="M720,${G - 40}L1040,${G - 40}L980,${G - 200}H780Z" fill="#2a2c30"/>
      <rect x="760" y="${G - 600}" width="240" height="80" rx="12" fill="#1e5aa8" stroke="#f4f2ea" stroke-width="5"/>${T(820, G - 544, 52, "P", { fill: "#f4f2ea", w: 900 })}${T(935, G - 544, 34, "ใต้ดิน", { fill: "#f4f2ea", w: 800 })}`;
    // the deck on pillars and its zig-zag emergency stair down to the street
    for (let k = 0; k < 5; k++) { const px = -500 + k * 380; if (px > 560) break; s += `<rect x="${px - 40}" y="${XY}" width="80" height="${G - XY}" fill="url(#twPillar)" ${O(3)}/>`; }
    s += `<rect x="-1300" y="${XY - 130}" width="1940" height="130" fill="url(#twDeck)" ${O(4)}/><rect x="-1300" y="${XY - 160}" width="1940" height="32" fill="#a8aea8" ${O(3)}/>`;
    const sx = 330; let st = "";
    for (let f = 0; f < 3; f++) { const y0 = XY + f * ((G - XY) / 3), y1 = y0 + (G - XY) / 3, dir = f % 2 ? -1 : 1, x0 = sx + (dir < 0 ? 240 : 0);
      st += `<path d="M${x0},${y0}L${x0 + dir * 240},${y1}" stroke="#d8d0c0" stroke-width="22"/><path d="M${x0},${y0 - 70}L${x0 + dir * 240},${y1 - 70}" stroke="#e8c03a" stroke-width="8"/>`;
      for (let k = 1; k < 10; k++) st += `<path d="M${x0 + dir * 24 * k},${y0 + ((y1 - y0) / 10) * k}v-70" stroke="#e8c03a" stroke-width="5"/>`; }
    s += st + `<rect x="${sx - 30}" y="${XY - 40}" width="300" height="40" fill="#d8d0c0" ${O(3)}/>`;
    put(L.set, s);
  };

  // ---------- the underground car park ----------
  Sets.garage = (L, o = {}) => {
    const r = mk(o.seed || 53), view = o.view || "wide", VX = o.VX ?? 600, VY = o.VY ?? 900, shut = o.shutter ?? 0;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#2a2c2c"/>`);
    let far = "";
    if (view === "wide") {
      // back wall with the ramp mouth up to daylight and its shutter
      far += `<rect x="-400" y="${VY - 260}" width="1900" height="520" fill="url(#n2Conc)"/><rect x="-400" y="${VY + 200}" width="1900" height="60" fill="#e8c03a"/>
        ${Array.from({ length: 24 }, (_, k) => `<path d="M${-400 + k * 80},${VY + 200}l40,60" stroke="#1c1e20" stroke-width="22"/>`).join("")}
        <path d="M${VX + 120},${VY + 200}L${VX + 420},${VY + 200}L${VX + 360},${VY - 200}H${VX + 180}Z" fill="#c8b8a0"/><rect x="${VX + 180}" y="${VY - 220}" width="180" height="${f1(130 + 0)}" fill="url(#n2Out)"/>
        <rect x="${VX + 176}" y="${VY - 224}" width="188" height="${f1(4 + 140 * shut)}" fill="#9a9ea4" ${O(3)}/>
        <g transform="translate(${VX - 260},${VY - 170})"><rect x="-70" y="-30" width="140" height="60" rx="8" fill="#1e8a4a" ${O(3)}/>${T(14, 14, 30, "ทางออก", { fill: "#e8ffe8", w: 800 })}<circle cx="-46" cy="-6" r="7" fill="#e8ffe8"/><path d="M-46,0l-8,18M-46,4l10,8" stroke="#e8ffe8" stroke-width="5"/></g>`;
      for (let k = 0; k < 5; k++) { const x = -260 + k * 300; far += Nk.car(x, VY + 196, 0.62, ["#c9ced4", "#3a5a8a", "#eef0f2", "#b8262a", "#5a5e64"][k], {}); }
      put(L.far, far);
      // ceiling beams and tubes in perspective, floor bays
      let s = `<path d="M-900,-600H2000V${VY - 260}H-900Z" fill="url(#n2Ceil)"/><path d="M-900,${VY + 260}H2000V2600H-900Z" fill="url(#n2Floor)"/>`;
      for (let k = 0; k < 7; k++) { const t = k / 6, y = VY - 260 - (VY - 260 + 300) * (1 - t) ** 1.6; s += `<rect x="-900" y="${f1(y - 40 * (1 - t) - 10)}" width="2900" height="${f1(70 * (1 - t) + 16)}" fill="#2e302e"/>`;
        s += `<rect x="${f1(VX - 360 * (1 - t) - 90)}" y="${f1(y + 40 * (1 - t) + 6)}" width="${f1(180 + 520 * (1 - t))}" height="${f1(8 + 18 * (1 - t))}" rx="8" fill="${k === 2 ? "#5a6058" : "#f4fff4"}"/>`;
        if (k !== 2) put(L.glow, `<ellipse cx="${VX}" cy="${f1(y + 60 * (1 - t))}" rx="${f1(300 + 700 * (1 - t))}" ry="${f1(60 + 160 * (1 - t))}" fill="url(#n2Tube)" opacity=".45"/>`); }
      for (let k = -4; k <= 4; k++) s += `<path d="M${VX + k * 90},${VY + 262}L${VX + k * 520},2000" stroke="#e9e4cf" stroke-width="7" opacity=".55"/>`;
      s += `<path d="M${VX - 40},${VY + 480}l40,-60l40,60M${VX},${VY + 420}v120" stroke="#e9e4cf" stroke-width="10" fill="none" opacity=".6"/>`;
      // pillars at the sides
      [[-150, 1.25], [1230, 1.25], [180, 0.7], [1010, 0.7]].forEach(([x, k]) => { const w = 150 * k, top = VY - 260 - 400 * (k - 0.6), bot = VY + 260 + 900 * (k - 0.6);
        s += `<rect x="${f1(x - w / 2)}" y="${f1(top)}" width="${f1(w)}" height="${f1(bot - top)}" fill="url(#n2Conc)" ${O(4)}/><rect x="${f1(x - w / 2)}" y="${f1(bot - 110 * k)}" width="${f1(w)}" height="${f1(110 * k)}" fill="#e8c03a"/>
          ${Array.from({ length: 4 }, (_, j) => `<path d="M${f1(x - w / 2 + j * w / 4)},${f1(bot - 110 * k)}l${f1(w / 8)},${f1(110 * k)}" stroke="#1c1e20" stroke-width="${f1(14 * k)}"/>`).join("")}
          ${T(x, top + 200 * k, 46 * k, "B1", { fill: "#2e302e", w: 900 })}`; });
      if (o.chalk) s += `<g transform="translate(${o.chalkX ?? 180},${o.chalkY ?? VY + 40}) rotate(-2)">${o.chalk.map((ln, k) => T(0, k * (o.chalkSize ?? 34) * 1.3, o.chalkSize ?? 34, ln, { fill: "#f4f2ea", w: 700, op: 0.92 })).join("")}</g>`;
      put(L.set, s);
    } else if (view === "shutter") {
      // close on the rolling shutter at the top of the ramp; light and dust under its gap
      const gapY = 1400 - 0 + (1 - shut) * 0, bottom = 1500 - 900 * (1 - shut);
      far += `<rect x="-400" y="300" width="1900" height="1300" fill="url(#n2Out)" opacity=".9"/>`;
      put(L.far, far);
      let s = `<rect x="-900" y="-600" width="2900" height="900" fill="#2e302e"/><rect x="-900" y="1500" width="2900" height="1200" fill="url(#n2Floor)"/>
        <rect x="-900" y="300" width="1040" height="1200" fill="url(#n2Conc)" ${O(4)}/><rect x="940" y="300" width="1100" height="1200" fill="url(#n2Conc)" ${O(4)}/>
        <rect x="140" y="300" width="800" height="${f1(bottom - 300)}" fill="#a8acb2" ${O(5)}/>`;
      for (let y = 330; y < bottom - 10; y += 36) s += `<path d="M146,${y}H934" stroke="#7a7e86" stroke-width="8"/><path d="M146,${y + 6}H934" stroke="#d4d8de" stroke-width="3"/>`;
      s += `<rect x="140" y="${f1(bottom - 30)}" width="800" height="30" fill="#6a6e76" ${O(4)}/><rect x="500" y="${f1(bottom - 70)}" width="80" height="44" rx="10" fill="#2e302e"/>`;
      if (o.dust) { for (let k = 0; k < 40; k++) s += `<circle cx="${f1(160 + r() * 760)}" cy="${f1(bottom + 10 + r() * 200)}" r="${f1(3 + r() * 7)}" fill="#c8c0b0" opacity="${f1(0.4 + r() * 0.5)}"/>`;
        s += `<path d="M300,${f1(bottom)}h480l-60,8h-360z" fill="#1a1a1a" opacity=".85"/>`; }
      put(L.set, s);
      if (o.dust) put(L.glow, `<rect x="140" y="${f1(bottom)}" width="800" height="26" fill="#ffd08a" opacity=".85"/><path d="M140,${f1(bottom + 26)}L-100,1920H1180L940,${f1(bottom + 26)}Z" fill="#ffd08a" opacity=".12"/>`);
    }
  };

  // ---------- game-style UI (screen space) ----------
  NkUI.title = (layer, o = {}) => put(layer, `<g transform="translate(540,${o.y ?? 230})">
      <rect x="-150" y="-112" width="300" height="56" rx="12" fill="${RED}"/>${T(0, -72, 32, o.tag || "นิวเคลียร์ลงกรุงเทพ", { fill: "#fff", w: 800 })}
      ${T(0, 76, 150, o.big || "วันที่ 1", { fill: "#fff", w: 900 })}
      <g transform="translate(0,132)"><rect x="-118" y="-28" width="236" height="56" rx="28" fill="${YEL}"/><g transform="translate(-78,0) scale(.8)">${ICON.clock(INK2)}</g>${T(18, 14, 34, o.time || "17:42 น.", { w: 800 })}</g>
      ${T(0, 214, 30, o.sub || "ทางด่วน · ตอนที่ 1", { fill: "#f4ecd8", w: 700, op: 0.9 })}</g>`);
  NkUI.miniMap = (layer, o = {}) => {
    const cx = o.cx ?? 540, cy = o.cy ?? 820, R = o.r ?? 400, r = mk(11);
    let m = `<rect x="-1" y="-1" width="2" height="2" fill="#9cb88a"/>`;
    // inside the unit circle: blocks, the expressway band, the shelter tower
    for (let k = 0; k < 26; k++) { const x = -0.95 + (k % 6) * 0.34 + r() * 0.05, y = -0.95 + Math.floor(k / 6) * 0.42 + r() * 0.05; m += `<rect x="${f1(x * 100) / 100}" y="${f1(y * 100) / 100}" width=".24" height=".28" rx=".03" fill="#d8d0bc" stroke="#7a7464" stroke-width=".01"/>`; }
    m += `<path d="M-1.2,.55L1.2,-.25" stroke="#7a7a80" stroke-width=".26"/><path d="M-1.2,.55L1.2,-.25" stroke="#e8e4d8" stroke-width=".012" stroke-dasharray=".05 .05"/>`;
    for (let k = 0; k < 18; k++) { const t = -1 + k * 0.12; m += `<rect x="${t.toFixed(2)}" y="${(0.55 - (t + 1.2) * 0.333 - 0.05).toFixed(3)}" width=".07" height=".04" rx=".01" fill="${["#b8262a", "#eef0f2", "#e8559a", "#9ccc3c"][k % 4]}" transform="rotate(-18 ${t.toFixed(2)} ${(0.55 - (t + 1.2) * 0.333).toFixed(3)})"/>`; }
    m += `<rect x=".2" y="-.62" width=".36" height=".42" rx=".03" fill="#f4ecd8" stroke="${RED}" stroke-width=".025"/><circle cx=".38" cy="-.41" r=".1" fill="#1e5aa8"/><text x=".38" y="-.37" font-family="Kanit" font-weight="900" font-size=".12" text-anchor="middle" fill="#fff">P</text>`;
    m += `<circle cx="-.28" cy=".27" r=".05" fill="#3aa86a" stroke="#fff" stroke-width=".015"/>`;
    const tok = (x, y, ic, lab) => `<g transform="translate(${x},${y})"><rect x="-96" y="-30" width="192" height="60" rx="30" fill="${CREAM}" stroke="#c9bea6" stroke-width="3"/><g transform="translate(-60,0) scale(.7)">${ICON[ic]()}</g>${T(16, 12, 30, lab, { w: 800 })}</g>`;
    put(layer, `<g><circle cx="${cx}" cy="${cy}" r="${R + 24}" fill="#e9e1c8" filter="drop-shadow(0 16px 30px rgba(0,0,0,.5))"/>
      <g transform="translate(${cx},${cy}) scale(${R})" clip-path="url(#n2MiniClip)">${m}</g><circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#7a6e54" stroke-width="6"/>
      ${tok(cx - 250, cy - R + 10, "building", "ตึก")}${tok(cx + 250, cy - R + 10, "under", "ลานจอดใต้ดิน")}${tok(cx - 250, cy + R - 10, "radio", "วิทยุ")}${tok(cx + 250, cy + R - 10, "water", "น้ำ")}</g>`);
  };
  NkUI.cityMap = (layer, o = {}) => {
    const cx = o.cx ?? 540, cy = o.cy ?? 760, r = mk(23);
    let g = `<rect x="0" y="0" width="1080" height="1920" fill="url(#n2MapBg)"/>`;
    for (let k = 0; k < 30; k++) g += `<path d="M${k * 40},0V1920M0,${k * 70}H1080" stroke="#1e3236" stroke-width="2"/>`;
    [260, 520].forEach((R) => (g += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#3a5458" stroke-width="10"/>`));
    const sp = 8; for (let k = 0; k < sp; k++) { const a = (k / sp) * Math.PI * 2 + 0.2, ex = cx + Math.cos(a) * 1300, ey = cy + Math.sin(a) * 1300;
      g += `<path d="M${cx},${cy}L${f1(ex)},${f1(ey)}" stroke="#3a5458" stroke-width="16"/>`;
      for (let j = 0; j < 46; j++) { const d = 120 + r() * 1000, px = cx + Math.cos(a) * d + (r() - 0.5) * 14, py = cy + Math.sin(a) * d + (r() - 0.5) * 14; g += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(3 + r() * 4)}" fill="#ff4a3a" opacity="${f1(0.6 + r() * 0.4)}"/>`; }
      for (let j = 1; j < 5; j++) { const d = 180 + j * 190, px = cx + Math.cos(a) * d, py = cy + Math.sin(a) * d, deg = (a * 180) / Math.PI;
        g += `<path d="M-14,-16L8,0L-14,16" transform="translate(${f1(px)},${f1(py)}) rotate(${f1(deg)})" stroke="#ff7a5a" stroke-width="7" fill="none" stroke-linecap="round"/>`; } }
    g += `<circle cx="${cx}" cy="${cy}" r="170" fill="url(#n2Hot)"/><g transform="translate(${cx},${cy + 10}) scale(.12)">${Nk.blastHTML(0, 0, 1, "mush", 5)}</g>
      <rect x="${cx - 110}" y="${cy + 60}" width="220" height="48" rx="24" fill="${RED}"/>${T(cx, cy + 96, 30, "จุดระเบิด", { fill: "#fff", w: 800 })}`;
    const px = cx - 360, py = cy + 300;
    g += `<path d="M${cx},${cy}L${px},${py}" stroke="#f4ecd8" stroke-width="4" stroke-dasharray="14 12" opacity=".8"/><rect x="${(cx + px) / 2 - 70}" y="${(cy + py) / 2 - 26}" width="140" height="52" rx="26" fill="${CREAM}"/>${T((cx + px) / 2, (cy + py) / 2 + 12, 30, "8 กม.", { w: 900 })}
      <g transform="translate(${px},${py})"><path d="M0,0C-40,-50 -40,-90 0,-96C40,-90 40,-50 0,0Z" fill="#3aa86a" stroke="#fff" stroke-width="5"/><circle cy="-62" r="14" fill="#fff"/><rect x="-60" y="12" width="120" height="44" rx="22" fill="${CREAM}"/>${T(0, 44, 28, "เก่ง", { w: 900 })}</g>`;
    g += [[40, 40, 1, 1], [1040, 40, -1, 1], [40, 1880, 1, -1], [1040, 1880, -1, -1]].map(([x, y, a, b]) => `<path d="M${x},${y + b * 70}V${y}H${x + a * 70}" stroke="#d8443a" stroke-width="6" fill="none"/>`).join("");
    put(layer, `<g>${g}</g>`);
  };
  NkUI.rule = (layer, o = {}) => { const x = o.x ?? 150, y = o.y ?? 230, w = o.w ?? 780, h = o.h ?? 250;
    put(layer, `<g>${panel(x, y, w, h, { bar: true })}<rect x="${x + w / 2 - 80}" y="${y + 24}" width="160" height="40" rx="20" fill="${INK2}"/>${T(x + w / 2, y + 54, 26, o.tag || "กฎข้อ 1", { fill: CREAM, w: 800 })}
      ${T(x + w / 2, y + 140, o.size || 64, o.text || "เข้าตึก · อยู่ในตึก · ฟังข่าว", { w: 900 })}
      <g transform="translate(${x + w / 2 - 40},${y + 205})"><circle r="16" fill="#e9e1c8" stroke="#c9bea6" stroke-width="3"/>${ICON.person().replace(/fill="[^"]*"/g, 'fill="#7a6e54"').replace("<circle", '<circle transform="scale(.5)"')}</g>
      <g transform="translate(${x + w / 2 + 40},${y + 205})"><circle r="16" fill="${RED}"/><path d="M-6,-6L6,6M6,-6L-6,6" stroke="#fff" stroke-width="4"/></g></g>`); };
  NkUI.section = (layer, o = {}) => { const r = mk(29);
    let g = `<rect x="0" y="0" width="1080" height="1920" fill="url(#n2MapBg)"/>`;
    const L0 = 260, R0 = 820, top = 360, ground = 1180;
    // fallout dust coming down and stopping at the concrete
    for (let k = 0; k < 120; k++) { const x = 60 + r() * 960, y = 120 + r() * (ground - 160); if (x > L0 - 10 && x < R0 + 10 && y > top - 20) continue; g += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(3 + r() * 4)}" fill="#d8e85a" opacity="${f1(0.4 + r() * 0.5)}"/>`; }
    g += `<rect x="40" y="${ground}" width="1000" height="560" fill="#3a3430"/><path d="M40,${ground}H1040" stroke="#7a6a5a" stroke-width="8"/>`;
    g += `<rect x="${L0}" y="${top}" width="${R0 - L0}" height="${ground - top}" fill="#8a8a8e" stroke="#e9e4d8" stroke-width="10"/>`;
    for (let k = 1; k < 7; k++) g += `<path d="M${L0},${top + k * ((ground - top) / 7)}H${R0}" stroke="#e9e4d8" stroke-width="6"/>`;
    g += `<rect x="${L0 + 40}" y="${top + 40}" width="${R0 - L0 - 80}" height="${ground - top - 60}" fill="#a8a8ac" opacity=".5"/>`;
    g += `<rect x="${L0}" y="${ground}" width="${R0 - L0}" height="380" fill="#6a6a6e" stroke="#e9e4d8" stroke-width="10"/><path d="M${L0},${ground + 190}H${R0}" stroke="#e9e4d8" stroke-width="6"/>`;
    for (let k = 0; k < 6; k++) g += `<g transform="translate(${L0 + 90 + k * 90},${ground + 165}) scale(.9)">${ICON.person("#7ae08a")}</g>`;
    g += `<g transform="translate(${L0 + 130},${ground + 345}) scale(.4)">${Nk.car(0, 0, 1, "#c9ced4", {})}</g><g transform="translate(${R0 - 130},${ground + 345}) scale(.4)">${Nk.car(0, 0, 1, "#3a5a8a", {})}</g>`;
    [[120, 250, "หลังคา", top - 4], [140, 700, "ผนังนอก", 700], [940, 760, "กลางตึก", 760], [940, ground + 120, "ใต้ดิน", ground + 120]].forEach(([x, y, lab]) => {
      g += `<rect x="${x - 90}" y="${y - 30}" width="180" height="56" rx="28" fill="${CREAM}"/>${T(x, y + 10, 30, lab, { w: 800 })}`; });
    g += badge(1030, ground + 90, true) + badge(1030, 730, true);
    put(layer, `<g>${g}</g>`); };
  NkUI.counter = (layer, items, o = {}) => { let g = "", y = o.y ?? 90;
    items.forEach((it) => { const w = 250; g += panel(40, y, w, 92, {}) + `<g transform="translate(92,${y + 46})"><circle r="30" fill="#e9e1c8" stroke="#c9bea6" stroke-width="3"/><g transform="scale(.8)">${ICON[it.icon]()}</g></g>${T(140, y + 62, 52, it.n, { anchor: "start", w: 900 })}${T(140 + 30 * String(it.n).length + 10, y + 62, 26, it.unit || "", { anchor: "start", w: 700, fill: "#7a6e54" })}`;
      y += 108; });
    put(layer, `<g>${g}</g>`); };
  NkUI.chip = (layer, lines, o = {}) => { const x = o.x ?? 40, y = o.y ?? 90, w = o.w ?? 640, h = 50 + lines.length * 46;
    put(layer, `<g>${panel(x, y, w, h, { rx: 16 })}<g transform="translate(${x + 44},${y + 50})">${ICON[o.icon || "info"]("#7a6e54")}</g>${lines.map((ln, k) => T(x + 86, y + 62 + k * 46, k ? 30 : 34, ln, { anchor: "start", w: k ? 600 : 800, fill: k ? "#5a5244" : INK2 })).join("")}</g>`); };
  NkUI.chain = (layer, items, o = {}) => { const y = o.y ?? 110, n = items.length, gap = 230, x0 = 540 - ((n - 1) * gap) / 2; let g = "";
    items.forEach((it, k) => { const x = x0 + k * gap; g += panel(x - 80, y, 160, 150, { rx: 18 }) + `<g transform="translate(${x},${y + 60}) scale(1.3)">${ICON[it.icon]()}</g>${T(x, y + 132, 26, it.label, { w: 700 })}` + badge(x + 70, y + 8, it.ok);
      if (k < n - 1) g += `<path d="M${x + 92},${y + 75}h46m-14,-12l14,12l-14,12" stroke="${CREAM}" stroke-width="7" fill="none" stroke-linecap="round"/>`; });
    put(layer, `<g>${g}</g>`); };
  NkUI.notebook = (layer, rows, o = {}) => { const x = o.x ?? 110, y = o.y ?? 160, w = o.w ?? 860, h = 120 + rows.length * 96;
    let g = panel(x, y, w, h, { rx: 18 }) + `<g transform="translate(${x + 60},${y + 64})"><circle r="26" fill="#e9e1c8" stroke="#c9bea6" stroke-width="3"/>${ICON.food("#7a6e54")}</g>${T(x + 108, y + 78, 44, o.title || "เสบียง · วันที่ 1 · 40 คน", { anchor: "start", w: 900 })}<path d="M${x + 30},${y + 110}H${x + w - 30}" stroke="#c9bea6" stroke-width="4"/>`;
    rows.forEach((rw, k) => { const ry = y + 150 + k * 96, bad = rw.bad;
      g += `<rect x="${x + 24}" y="${ry - 40}" width="${w - 48}" height="80" rx="14" fill="${bad ? "#fbe2dc" : "#efe6d0"}" stroke="${bad ? RED : "transparent"}" stroke-width="3"/>
        <g transform="translate(${x + 72},${ry})"><circle r="24" fill="#fff8ea" stroke="#c9bea6" stroke-width="3"/><g transform="scale(.7)">${ICON[rw.icon](bad ? RED : "#7a6e54")}</g></g>${T(x + 116, ry + 12, 32, rw.label, { anchor: "start", w: 800 })}`;
      for (let j = 0; j < 10; j++) g += `<rect x="${x + 300 + j * 34}" y="${ry - 8}" width="26" height="16" rx="4" fill="${j < rw.bar ? (bad ? RED : j > 6 ? "#e8c03a" : "#3aa8a0") : "#ddd2bc"}"/>`;
      g += T(x + w - 120, ry + 12, 34, rw.val, { anchor: "end", w: 900, fill: bad ? RED : INK2 }) + (bad ? "" : badge(x + w - 66, ry, true)); });
    put(layer, `<g>${g}</g>`); };
  NkUI.endCard = (layer, o = {}) => put(layer, `<g><rect x="0" y="0" width="1080" height="1920" fill="url(#n2EndBg)"/>
      <g transform="translate(540,640)"><rect x="-110" y="-30" width="220" height="56" rx="28" fill="none" stroke="#f4ecd8" stroke-width="3" opacity=".7"/><circle cx="-72" cy="-2" r="8" fill="${RED}"/>${T(14, 10, 28, "ตอนต่อไป", { fill: "#f4ecd8", w: 700 })}</g>
      ${T(540, 830, 130, o.big || "ตอนที่ 2", { fill: "#f4ecd8", w: 900 })}<rect x="390" y="880" width="300" height="8" rx="4" fill="${RED}"/>
      ${T(540, 970, 44, o.sub || "ใครบางคนเคาะประตูจากข้างนอก", { fill: "#ff5a4a", w: 800 })}${T(540, 1050, 32, o.foot || "กดติดตาม แล้วมารอดไปด้วยกัน", { fill: "#c8c0b0", w: 600 })}</g>`);
  NkUI.logo = (layer) => put(layer, `<g><rect x="0" y="0" width="1080" height="1920" fill="url(#n2EndBg)"/>
      <g transform="translate(540,780)"><circle r="120" fill="#1e2a2c" stroke="${YEL}" stroke-width="10"/>${T(0, 40, 120, "?", { fill: YEL, w: 900 })}</g>
      ${T(540, 1010, 96, "Rod Mai Club", { fill: "#f4ecd8", w: 900 })}${T(540, 1080, 40, "ถ้าวันหนึ่ง… คุณจะรอดไหม?", { fill: "#c8c0b0", w: 600 })}</g>`);
  window.Nk2 = Nk2; window.NkUI = NkUI;
})();
