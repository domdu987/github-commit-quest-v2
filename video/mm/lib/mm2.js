// "ผีแม่ม่าย" sets, part 2 — the rest of the village. Same layer contract as pop2.js (sky / far / mid / set / act / fg; glow above the
// darkness; light = screen space). Seeded RNG only. Coordinates are laid out for a camera at fr(540, 960, 1, 540, 960) unless noted.
//   Sets.shirtOpen(L, o)  opener: one red shirt on a bamboo pole in the dark, lit by a cold shaft of moonlight; a plank nailed to the
//                         pole carries the title in red paint (#id-wipe = the mask rect that paints it in, width 0 → 760; drips #id-d0..3
//                         grow from their tops) · ids #id-shirt (sways round its hook, svgOrigin "0 0"), #id-beam · o.ep "EP.1"
//   Sets.gate2(L, o)      dusk at the village entrance: the main road across the foreground, the concrete gate with the village name,
//                         a red shirt hung on each pillar (#id-gs0, #id-gs1), the laterite road into the village past houses with shirts,
//                         the songthaew pulling away on the left (#id-bus, o.bus false to leave it out) · o.name "บ้านโนนคำ"
//   Sets.tower2(L, o)     low angle under the loudspeaker tower at dusk: horns #id-horns, sound rings #id-ring0..2 (scale from their
//                         centres), the office veranda corner, the table with the amplifier (VU #id-vu) and an iced coffee in a bag
//   Sets.legend3(L, o)    หนังประโมทัย screen lit from behind: the widow puppet #id-widow, the sleeping man #id-man, the red shirt puppet
//                         #id-rshirt (translucent red, glows through the cloth), the lamp #id-lamp; audience heads in fg
//   Sets.yard2(L, o)      ลุงเปี๊ยก's place under his stilt house: the bamboo platform (seat top at y G-170 for c 1, x o.seat),
//                         the scarecrow in a red shirt, sarong and a string wig (#id-crow), his motorbike, the shirt pole · o.time day | dusk
//   Sets.house3(L, o)     inside the family house at supper: plank walls, the shrine shelf, father's portrait with a black ribbon
//                         (#id-photo, x o.photo), calendar, a wall clock (#id-hh #id-mm hands only), the fluorescent tube (#id-tube glow),
//                         a fan, the doorway with a red shirt on a hanger (#id-dsh), the woven mat and the khantoke tray of food
//                         (x o.tray, y o.trayY; drawn over the actors so whoever sits behind it has their legs hidden; o.trayFront false)
//   Sets.flip2(L, o)      the อสม. flipchart at the sala. o.close: the page fills the frame. Hearts #id-h0 (squeezes: scale from its
//                         centre) and #id-h1 (quivers), ECG traces #id-e0 #id-e1 (stroke-dash draw-on), arrows #id-a0, cross #id-x1
//   Sets.sleep2(L, o)     3 a.m. in the sleeping room: plank wall with moonlight slits (#id-moon), shuttered window (#id-win),
//                         the doorway with the red shirt on its hanger (#id-dsh sways), floor mattresses under mosquito nets: Keng's
//                         (x o.bed, front panel in L.glow #id-net), Fon's (#id-net2); o.ghost seats the widow at the foot of Keng's
//                         mattress (#id-ghost, eyes #id-ghost-eyes) · o.lamp true = the night bulb is on (#id-bulb)
//   Mm.songthaew(o)       the village songthaew: Pop2.truck with a roofed bed, benches, posts and a rear step (same units, faces right)
//   Mm.scarecrow(x, G, s, o)  straw man dressed as a woman (red shirt, sarong, string wig, painted lips) · origin at its foot
//   Mm.moto(x, G, s)      an underbone motorbike side-on, facing right, wheels on y 0 (1 unit ≈ 2.7 mm at s 1: 1.9 m long)
//   Mm.PROP.{mic, polish, bag, hanger}  props for the hand group (the palm at (0, 118))
(function () {
  const { mk, f1, put, blob, cloud2, crown, palm, tuft, house2 } = Pop2;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const Mm = (window.Mm = window.Mm || {});

  Sets.DEFS += `
    <linearGradient id="mmPillar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff0d2"/><stop offset=".6" stop-color="#e2cca4"/><stop offset="1" stop-color="#a8906c"/></linearGradient>
    <linearGradient id="mmPanel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a2218"/><stop offset="1" stop-color="#5e0e0a"/></linearGradient>
    <linearGradient id="mmGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe49a"/><stop offset="1" stop-color="#c8902a"/></linearGradient>
    <linearGradient id="mmAsphalt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3e48"/><stop offset="1" stop-color="#2e2830"/></linearGradient>
    <linearGradient id="mmLaterite" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a5a44"/><stop offset="1" stop-color="#b8683e"/></linearGradient>
    <linearGradient id="mmBeam" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity=".0"/><stop offset=".35" stop-color="#cfe0ff" stop-opacity=".22"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>
    <radialGradient id="mmSpot" cx=".5" cy=".45" r=".55"><stop offset="0" stop-color="#bcd2ff" stop-opacity=".4"/><stop offset="1" stop-color="#bcd2ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="mmPlank" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a3a"/><stop offset=".5" stop-color="#9c6a46"/><stop offset="1" stop-color="#84563a"/></linearGradient>
    <linearGradient id="mmPlankN" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c1620"/><stop offset=".5" stop-color="#221a24"/><stop offset="1" stop-color="#1a141c"/></linearGradient>
    <linearGradient id="mmFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a4630"/><stop offset="1" stop-color="#8a5e40"/></linearGradient>
    <linearGradient id="mmFloorN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16121a"/><stop offset="1" stop-color="#2a2028"/></linearGradient>
    <linearGradient id="mmMat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8b878"/><stop offset="1" stop-color="#b8945a"/></linearGradient>
    <linearGradient id="mmMattress" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2d8ec"/><stop offset="1" stop-color="#b8acc8"/></linearGradient>
    <radialGradient id="mmTubeW"><stop offset="0" stop-color="#f4fff8" stop-opacity=".7"/><stop offset=".3" stop-color="#d8f4ec" stop-opacity=".22"/><stop offset="1" stop-color="#d8f4ec" stop-opacity="0"/></radialGradient>
    <radialGradient id="mmBulb"><stop offset="0" stop-color="#ffe0a0" stop-opacity=".75"/><stop offset=".3" stop-color="#ffb860" stop-opacity=".22"/><stop offset="1" stop-color="#ffb860" stop-opacity="0"/></radialGradient>
    <linearGradient id="mmPaper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fdfbf4"/><stop offset="1" stop-color="#ebe4d2"/></linearGradient>
    <radialGradient id="mmScreen" cx=".5" cy=".55" r=".72"><stop offset="0" stop-color="#fff4d8"/><stop offset=".5" stop-color="#f2be78"/><stop offset="1" stop-color="#8a4420"/></radialGradient>
    <radialGradient id="mmVu"><stop offset="0" stop-color="#ffd27a" stop-opacity=".9"/><stop offset="1" stop-color="#ff9a2a" stop-opacity="0"/></radialGradient>
    <linearGradient id="mmSlit" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8c4ff" stop-opacity=".3"/><stop offset="1" stop-color="#a8c4ff" stop-opacity="0"/></linearGradient>
    <filter id="mmSoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
    <pattern id="mmMesh" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0,0H6M0,0V6" stroke="#e6eef8" stroke-width=".8" opacity=".5"/></pattern>
    <pattern id="mmWeave" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M0,6H12M12,18H24" stroke="#9a7440" stroke-width="5" opacity=".45"/><path d="M6,12V24M18,0V12" stroke="#e8cc8a" stroke-width="4" opacity=".4"/></pattern>`;

  // ---------------- props in hand (palm at (0, 118)) ----------------
  Mm.PROP = {
    mic: () => `<g transform="translate(2,104) rotate(-12)"><rect x="-8" y="-6" width="16" height="70" rx="6" fill="#2a2a2e" stroke="${INK}" stroke-width="2.4"/><ellipse cx="0" cy="-14" rx="17" ry="20" fill="#9aa0a6" stroke="${INK}" stroke-width="2.4"/>
      <path d="M-12,-20h24M-13,-12h26M-11,-4h22" stroke="#5a5e64" stroke-width="2"/><path d="M0,64q-10,40 18,60t-6,70" stroke="#1a1a1e" stroke-width="4" fill="none"/></g>`,
    polish: () => `<g transform="translate(4,100) rotate(10)"><rect x="-11" y="-14" width="22" height="26" rx="6" fill="#d8202a" stroke="${INK}" stroke-width="2.2"/><rect x="-6" y="-36" width="12" height="22" rx="2" fill="#1a1a1e" stroke="${INK}" stroke-width="2"/>
      <path d="M-6,-10q4,-2 6,8" stroke="#fff" stroke-width="2.4" opacity=".6" fill="none"/></g>`,
    bag: () => `<g transform="translate(0,116)"><path d="M-14,0Q0,-16 14,0" stroke="#1e2a3a" stroke-width="7" fill="none"/><path d="M-70,8Q-74,60 -64,96H64Q74,60 70,8Q0,-4 -70,8Z" fill="#2e4a6e" stroke="${INK}" stroke-width="3"/>
      <path d="M-70,30H70" stroke="#c8a040" stroke-width="6"/><path d="M-50,8V96M50,8V96" stroke="#1e3450" stroke-width="3" opacity=".6"/><ellipse cx="-70" cy="52" rx="10" ry="30" fill="#24405e" stroke="${INK}" stroke-width="2.4"/></g>`,
    hanger: () => `<g transform="translate(0,96)"><path d="M0,0q10,-12 2,-20t-8,4" stroke="#8a8a90" stroke-width="3" fill="none"/>${Mm.shirt(0, 6, 0.5, {})}</g>`,
  };

  // ---------------- the songthaew ----------------
  // Pop2.truck facing right; the bed gets a roof on posts, a far bench, a grab rail and a rear step. Units as Pop2.truck (1 ≈ 6 mm).
  Mm.songthaew = (o = {}) => {
    let g = Pop2.truck({ driver: o.driver ?? "sil" });
    const pax = o.pax ?? [[-330, "#2a2420"], [-150, "#3a2a24"]];
    let b = `<path d="M-440,-204V-330H-34V-204Z" fill="#141210" opacity=".9"/>`;
    // the far bench back and its padding, passengers' silhouettes sitting along it
    b += `<path d="M-430,-262H-40V-226H-430Z" fill="#4a5a7a" ${OUT3}/><path d="M-430,-250H-40" stroke="#6a7a9a" stroke-width="3"/>`;
    pax.forEach(([px, c]) => { b += `<g fill="${c}"><ellipse cx="${px}" cy="-286" rx="24" ry="28"/><path d="M${px - 40},-204Q${px - 40},-256 ${px},-260Q${px + 40},-256 ${px + 40},-204Z"/></g>`; });
    // posts, the grab rail, the roof with its luggage rail and a little route board above the cab
    [-448, -240, -34].forEach((px) => { b += `<rect x="${px - 6}" y="-372" width="12" height="170" fill="#d8dce0" ${OUT3}/>`; });
    b += `<path d="M-448,-300H-34" stroke="#c8ccd0" stroke-width="7"/><path d="M-448,-300H-34" stroke="${INK}" stroke-width="9" opacity=".25"/>`;
    b += `<path d="M-470,-372Q-470,-392 -450,-394H150Q172,-392 172,-378L168,-366H-470Z" fill="#eef2f4" ${OUT}/><path d="M-470,-376H168" stroke="${o.stripe || "#2a7ab8"}" stroke-width="8"/>`;
    b += `<path d="M-440,-394V-414H-60V-394" stroke="#9aa0a6" stroke-width="5" fill="none"/>${[-380, -300, -220, -140].map((px) => `<path d="M${px},-414V-394" stroke="#9aa0a6" stroke-width="4"/>`).join("")}`;
    b += `<rect x="-10" y="-430" width="160" height="34" rx="4" fill="#f4e8b0" ${OUT3}/><path d="M6,-418h70M6,-408h110" stroke="#3a6a9a" stroke-width="4"/>`;
    // the rear step and the hand grip by the step
    b += `<path d="M-500,-64H-440V-48H-500Z" fill="#8a8e92" ${OUT3}/><path d="M-470,-64V-90" stroke="#5a5e62" stroke-width="5"/><path d="M-452,-360V-120" stroke="#e8ecee" stroke-width="5"/>`;
    return g.replace(/(<path d="M-444,-80V-204)/, `${b}$1`);
  };

  // ---------------- the motorbike (underbone) ----------------
  Mm.moto = (x, G, s = 1, o = {}) => {
    const wh = (wx) => `<circle cx="${wx}" cy="-110" r="110" fill="#141416" ${OUT3}/><circle cx="${wx}" cy="-110" r="74" fill="#3a3c40"/><circle cx="${wx}" cy="-110" r="64" fill="#9aa0a6"/>
      ${[0, 60, 120].map((a) => `<path d="M${wx - 60},-110H${wx + 60}" stroke="#5a5e62" stroke-width="7" transform="rotate(${a} ${wx} -110)"/>`).join("")}<circle cx="${wx}" cy="-110" r="18" fill="#2a2c30"/>`;
    const c = o.color || "#c8282a";
    let g = `<ellipse cx="0" cy="6" rx="380" ry="22" fill="#000" opacity=".4"/>` + wh(-250) + wh(270);
    g += `<path d="M-250,-110L-80,-180L120,-170L270,-110" stroke="#2a2c30" stroke-width="16" fill="none"/>`;
    g += `<path d="M-300,-250Q-320,-330 -200,-340H40Q70,-336 60,-300L-10,-240Q-120,-200 -300,-250Z" fill="${c}" ${OUT}/>`;
    g += `<path d="M-280,-330Q-180,-372 20,-350L30,-330Q-140,-346 -280,-318Z" fill="#1a1a1e" ${OUT3}/>`;
    g += `<path d="M60,-300L180,-420L210,-410L100,-280Z" fill="${c}" ${OUT3}/><path d="M200,-420L280,-110" stroke="#9aa0a6" stroke-width="16"/><path d="M200,-420L280,-110" stroke="${INK}" stroke-width="18" opacity=".2"/>`;
    g += `<path d="M150,-470L260,-470" stroke="#2a2a2e" stroke-width="12" stroke-linecap="round"/><path d="M200,-430Q240,-470 260,-470" stroke="${INK}" stroke-width="6" fill="none"/>`;
    g += `<rect x="230" y="-470" width="80" height="60" rx="6" fill="none" stroke="#3a3a3a" stroke-width="5"/>${[0, 1, 2].map((k) => `<path d="M${240 + k * 24},-466V-414" stroke="#3a3a3a" stroke-width="3"/>`).join("")}`;
    g += `<path d="M268,-430l30,6l-4,22l-30,-4z" fill="#fff6c8" ${OUT3}/>`;
    g += `<path d="M-300,-250L-360,-240L-350,-210L-290,-220Z" fill="#d8302a" ${OUT3}/><path d="M-120,-170L-40,-120" stroke="#9aa0a6" stroke-width="10"/>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  };

  // ---------------- the scarecrow dressed as a woman ----------------
  Mm.scarecrow = (x, G, s = 1, o = {}) => {
    const r = mk(o.seed || 5);
    let g = `<ellipse cx="0" cy="4" rx="110" ry="16" fill="#000" opacity=".3"/><path d="M0,0V-640" stroke="#8a6a3a" stroke-width="14"/><path d="M-200,-470H200" stroke="#8a6a3a" stroke-width="12" stroke-linecap="round"/>`;
    // the sarong, the red shirt over the cross, straw poking out of the cuffs and the collar
    g += `<path d="M-70,-300L-90,-30H90L70,-300Z" fill="#5a2a6a" ${OUT3}/><path d="M-84,-80H84M-80,-130H80" stroke="#e8c050" stroke-width="5"/><path d="M-76,-200H76" stroke="#3a1a4a" stroke-width="4"/>`;
    g += `<g transform="translate(0,-494) scale(1.05)">${Mm.shirt(0, 0, 1, {}).replace(/<path d="M-6,0V14"[^>]*\/><path d="M-120,14H120"[^>]*\/>/, "")}</g>`;
    for (let k = 0; k < 7; k++) g += `<path d="M${-204 + r() * 10},${-480 + k * 4}l${-20 - r() * 20},${-10 + r() * 20}M${204 - r() * 10},${-480 + k * 4}l${20 + r() * 20},${-10 + r() * 20}" stroke="#e8c870" stroke-width="3"/>`;
    // the head: a straw bundle with a painted face and lips, a black string wig
    g += `<ellipse cx="0" cy="-560" rx="62" ry="70" fill="#e2c27a" ${OUT3}/>`;
    for (let k = 0; k < 14; k++) g += `<path d="M${-50 + k * 8},-600q${(r() - 0.5) * 8},40 ${(r() - 0.5) * 10},80" stroke="#c8a050" stroke-width="2" fill="none"/>`;
    g += `<path d="M-30,-570q10,-8 20,0M10,-570q10,-8 20,0" stroke="${INK}" stroke-width="4" fill="none"/><path d="M-16,-532Q0,-520 16,-532Q0,-540 -16,-532Z" fill="#d82a3a"/><circle cx="-30" cy="-546" r="9" fill="#ff7a8a" opacity=".6"/><circle cx="30" cy="-546" r="9" fill="#ff7a8a" opacity=".6"/>`;
    g += `<path d="M-66,-580C-84,-664 84,-664 66,-580Q40,-606 0,-604Q-40,-606 -66,-580Z" fill="#121014"/>`;
    for (let k = 0; k < 7; k++) { const sx = -70 + k * 5; g += `<path d="M${sx},-600Q${sx - 10 + r() * 6},-500 ${sx - 6 + r() * 8},${-400 - r() * 40}" stroke="#121014" stroke-width="5" fill="none"/><path d="M${-sx},-600Q${-sx + 10 - r() * 6},-500 ${-sx + 6 - r() * 8},${-400 - r() * 40}" stroke="#121014" stroke-width="5" fill="none"/>`; }
    g += `<circle cx="40" cy="-620" r="10" fill="#e83a6a" ${OUT3}/>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})"><g ${o.id ? `id="${o.id}"` : ""}>${g}</g></g>`;
  };

  // ---------------- the opener: one shirt in the dark ----------------
  function shirtOpen(L, o = {}) {
    const id = o.id || "so", r = mk(o.seed || 77), G = o.ground ?? 1760, HX = o.x ?? 540, HY = o.hookY ?? 330, S = o.s ?? 2.1;
    let sk = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#p2SkyNight)"/><rect x="-1300" y="-900" width="3700" height="3900" fill="#04050a" opacity=".6"/>`;
    for (let k = 0; k < 70; k++) sk += `<circle cx="${f1(-600 + r() * 2300)}" cy="${f1(-500 + r() * 1300)}" r="${f1(1 + r() * 1.6)}" fill="#e8ecff" opacity="${f1(0.15 + r() * 0.5)}"/>`;
    sk += `<circle cx="820" cy="250" r="460" fill="url(#kiMoon)" opacity=".75"/><circle cx="820" cy="250" r="36" fill="#eef2ff"/>`;
    sk += cloud2(980, 200, 620, 100, r, "p2CloudNight", "#2a3448", "#0c1018");
    put(L.sky, sk);
    // far: the village asleep — roofs, palms, the tower, one more shirt on a pole far off
    let f = "";
    for (let k = 0; k < 18; k++) f += crown(-900 + k * 170 + r() * 50, G - 520 - r() * 40, 70 + r() * 30, r, ["#06080c", "#080a10", "#0a0c12", "#0a0c12"], 6);
    for (let k = 0; k < 4; k++) f += palm(-500 + k * 560 + r() * 80, G - 480, 0.5 + r() * 0.1, "#05070a");
    [[-160, 0.5], [1180, 0.46]].forEach(([hx, hs]) => { f += `<g opacity=".95" filter="brightness(.2)">${house2(hx, G - 420, hs, { time: "night", under: false })}</g>`; });
    f += `<rect x="-1300" y="${G - 560}" width="3700" height="1600" fill="#05060a" opacity=".35"/><rect x="-1300" y="${G - 760}" width="3700" height="300" fill="url(#p2Haze)" opacity=".35"/>`;
    put(L.far, f);
    let m = Mm.shirtPole(-80, G - 300, 0.55, { night: true, id: `${id}-far0` }) + Mm.shirtPole(1240, G - 320, 0.5, { night: true, id: `${id}-far1` });
    m += `<rect x="-1300" y="${G - 420}" width="3700" height="300" fill="url(#p2Haze)" opacity=".35"/>`;
    put(L.mid, m);
    // the pole, the plank, the shirt
    let s = `<rect x="-1300" y="${G - 140}" width="3700" height="1200" fill="url(#p2GrassNight)"/><rect x="-1300" y="${G - 140}" width="3700" height="1200" fill="#05070a" opacity=".45"/>`;
    for (let k = 0; k < 40; k++) { const gx = -600 + r() * 2300, gy = G - 120 + r() * 300; s += tuft(gx, gy, 0.8 + (gy - G) / 300, "#0a120c", "#142018", r); }
    s += `<ellipse cx="${HX}" cy="${G + 40}" rx="120" ry="20" fill="#000" opacity=".5"/>`;
    s += `<path d="M${HX - 6},${G + 40}L${HX - 2},${HY + 8}" stroke="#7a6038" stroke-width="20" stroke-linecap="round"/><path d="M${HX + 2},${G + 40}L${HX + 4},${HY + 8}" stroke="#c8a868" stroke-width="5" opacity=".5"/>
      ${[0.2, 0.42, 0.66, 0.86].map((u) => `<path d="M${HX - 12},${f1(HY + (G - HY) * u)}h22" stroke="#4a3418" stroke-width="5"/>`).join("")}`;
    const PY = o.plankY ?? 1250, PW = 760, PH = 240;
    s += `<g transform="translate(${HX},${PY}) rotate(-3)"><rect x="${-PW / 2 + 10}" y="${-PH / 2 + 14}" width="${PW}" height="${PH}" rx="8" fill="#000" opacity=".45"/>
      <rect x="${-PW / 2}" y="${-PH / 2}" width="${PW}" height="${PH}" rx="8" fill="url(#mmBoard)" ${OUT}/>
      <path d="M${-PW / 2 + 10},-50H${PW / 2 - 10}M${-PW / 2 + 10},10H${PW / 2 - 10}M${-PW / 2 + 10},66H${PW / 2 - 10}" stroke="#8a6a3e" stroke-width="2.4" opacity=".5"/>
      ${[[-PW / 2 + 24, -PH / 2 + 22], [PW / 2 - 24, -PH / 2 + 22], [-PW / 2 + 24, PH / 2 - 22], [PW / 2 - 24, PH / 2 - 22]].map(([nx, ny]) => `<circle cx="${nx}" cy="${ny}" r="7" fill="#4a3a2a"/>`).join("")}
      <defs><mask id="${id}-mask"><rect id="${id}-wipe" x="${-PW / 2}" y="${-PH / 2 - 60}" width="${PW}" height="${PH + 200}" fill="#fff"/></mask></defs>
      <g mask="url(#${id}-mask)"><text x="-10" y="44" text-anchor="middle" font-family="Mali" font-weight="700" font-size="148" fill="#c41e16" stroke="#6a0a08" stroke-width="3" paint-order="stroke" letter-spacing="4">ผีแม่ม่าย</text>
</g>
      ${[[-236, 44, 46], [-74, 50, 70], [118, 46, 36], [250, 52, 58]].map(([dx, dy, dl], k) => `<g id="${id}-d${k}"><path d="M${dx - 7},${dy}C${dx - 6},${dy + dl * 0.5} ${dx - 4},${dy + dl * 0.8} ${dx - 6},${dy + dl}A7,8 0 1 0 ${dx + 6},${dy + dl}C${dx + 4},${dy + dl * 0.8} ${dx + 3},${dy + dl * 0.4} ${dx + 3},${dy}Z" fill="#c41e16" stroke="#6a0a08" stroke-width="1.5"/></g>`).join("")}
      <text x="${PW / 2 - 40}" y="${PH / 2 - 26}" text-anchor="end" font-family="Kanit" font-weight="800" font-size="40" fill="#f4ecd8" opacity=".9">${o.ep || "EP.1"}</text></g>`;
    s += `<g transform="translate(${HX},${HY}) scale(${S})"><g id="${id}-shirt">${Mm.shirt(0, 0, 1, { shade: true }).replace(/^<g transform="[^"]*">/, "").replace(/<\/g>$/, "")}</g></g>`;
    put(L.set, s);
    // the shaft of moonlight that picks out the shirt and the plank
    put(L.glow, `<g id="${id}-beam"><path d="M1200,-200L1700,40L${HX - 40},${PY + 300}L${HX - 520},${PY + 60}Z" fill="url(#mmBeam)" opacity=".7" filter="url(#mmSoft)" style="mix-blend-mode:screen"/></g>`);
    let fg = "";
    for (let k = 0; k < 8; k++) fg += tuft(-40 + k * 40, 2080, 3.4, "#020403", "#05080a", r) + tuft(1120 - k * 40, 2100, 3.2, "#020403", "#05080a", r);
    put(L.fg, fg);
  }

  // ---------------- the village gate at dusk ----------------
  function gate2(L, o = {}) {
    const id = o.id || "gt", r = mk(o.seed || 303), HZ = o.horizon ?? 900, VX = o.vx ?? 700;
    let sk = `<rect x="-1300" y="-900" width="3700" height="3800" fill="url(#p2SkyDusk)"/><circle cx="${o.sunX ?? 160}" cy="${HZ - 40}" r="620" fill="url(#p2Sun)"/>`;
    sk += cloud2(1300, 380, 1100, 300, r, "p2CloudDusk", "#f2b88a", "#5a3a54") + cloud2(-200, 200, 1000, 260, r, "p2CloudDusk", "#f2b88a", "#5a3a54");
    put(L.sky, sk);
    // far: tree line, palms, the temple roof at the end of the village road
    const FT = ["#4a3450", "#5a4060", "#6a4c6e"];
    let f = "";
    for (let k = 0; k < 26; k++) f += crown(-1200 + k * 140 + r() * 60, HZ - 10 - r() * 30, 70 + r() * 40, r, [FT[0], FT[1], FT[2], FT[2]], 6);
    for (let k = 0; k < 7; k++) f += palm(-1000 + k * 480 + r() * 120, HZ + 10, 0.4 + r() * 0.12, FT[0]);
    f += `<g transform="translate(${VX},${HZ - 20}) scale(.55)" fill="${FT[0]}"><path d="M-170,0V-90H170V0Z"/><path d="M-210,-90L-120,-170L120,-170L210,-90Z"/><path d="M-150,-170L-60,-250L60,-250L150,-170Z"/><path d="M0,-250V-380" stroke="${FT[0]}" stroke-width="10"/></g>`;
    f += `<rect x="-1300" y="${HZ - 140}" width="3700" height="220" fill="url(#p2Haze)"/>`;
    put(L.far, f);
    // mid: paddies either side, the first houses of the village with their shirts
    let m = `<rect x="-1300" y="${HZ}" width="3700" height="700" fill="url(#p2GrassDusk)"/>`;
    for (let k = 0; k < 10; k++) m += `<path d="M-1300,${HZ + 20 + k * k * 6}H2400" stroke="#6a7a3a" stroke-width="2" opacity=".35"/>`;
    [[VX - 330, HZ + 40, 0.24, false], [VX + 300, HZ + 46, 0.24, true], [VX - 520, HZ + 110, 0.34, false], [VX + 520, HZ + 120, 0.34, true]].forEach(([hx, hy, hs, flip], k) => {
      m += `<g transform="translate(${hx},${hy}) scale(${flip ? -1 : 1},1) translate(${-hx},${-hy})">${house2(hx, hy, hs, { time: "dusk", under: false })}</g>`;
      m += Mm.shirtPole(hx + (flip ? -1 : 1) * 200 * hs, hy, hs * 0.8, { id: `${id}-hs${k}` });
    });
    m += `<rect x="-1300" y="${HZ - 20}" width="3700" height="160" fill="url(#p2Haze)" opacity=".5"/>`;
    put(L.mid, m);
    // set: the village road into the distance, the gate, the main road in front with its verge
    const GB = o.gateY ?? 1330, GW = 300, GH = 520;
    let s = `<path d="M${VX - 16},${HZ}H${VX + 16}L${VX + 330},${GB + 60}H${VX - 330}Z" fill="url(#mmLaterite)"/>`;
    s += `<path d="M${VX - 6},${HZ + 4}L${VX - 120},${GB + 50}M${VX + 6},${HZ + 4}L${VX + 120},${GB + 50}" stroke="#7a3e24" stroke-width="7" opacity=".45"/>`;
    for (let k = 0; k < 16; k++) { const u = r(), py = HZ + 10 + u * (GB - HZ); s += `<ellipse cx="${f1(VX + (r() - 0.5) * (40 + u * 520))}" cy="${f1(py)}" rx="${f1(3 + u * 9)}" ry="${f1(1.5 + u * 3)}" fill="#6a3420" opacity=".55"/>`; }
    // the gate: plinths, pillars, capitals, the beam with the name panel, the pediment with curled finials
    const pillar = (px) => `<rect x="${px - 34}" y="${GB - 30}" width="68" height="40" fill="#c8b08c" ${OUT3}/><rect x="${px - 26}" y="${GB - GH}" width="52" height="${GH - 30}" fill="url(#mmPillar)" ${OUT3}/>
      <path d="M${px - 26},${GB - 120}H${px + 26}M${px - 26},${GB - 400}H${px + 26}" stroke="#c8902a" stroke-width="6"/><rect x="${px - 36}" y="${GB - GH - 20}" width="72" height="26" fill="#e8d4a8" ${OUT3}/>`;
    s += `<ellipse cx="${VX}" cy="${GB + 6}" rx="${GW + 80}" ry="24" fill="#000" opacity=".22"/>` + pillar(VX - GW) + pillar(VX + GW);
    s += `<rect x="${VX - GW - 50}" y="${GB - GH - 110}" width="${2 * GW + 100}" height="96" rx="6" fill="url(#mmPillar)" ${OUT3}/><rect x="${VX - GW + 10}" y="${GB - GH - 98}" width="${2 * GW - 20}" height="72" rx="4" fill="url(#mmPanel)" stroke="#c8902a" stroke-width="4"/>
      <text x="${VX}" y="${GB - GH - 46}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="50" fill="url(#mmGold)" stroke="#5a2a08" stroke-width="1.5" paint-order="stroke">${o.name || "บ้านโนนคำ"}</text>`;
    s += `<path d="M${VX - GW - 40},${GB - GH - 110}L${VX},${GB - GH - 230}L${VX + GW + 40},${GB - GH - 110}Z" fill="#e8d4a8" ${OUT3}/><path d="M${VX - GW + 20},${GB - GH - 116}L${VX},${GB - GH - 206}L${VX + GW - 20},${GB - GH - 116}Z" fill="#b8282a" ${OUT3}/>
      <text x="${VX}" y="${GB - GH - 132}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="24" fill="#ffe49a">ยินดีต้อนรับ</text>
      <path d="M${VX - GW - 40},${GB - GH - 110}q-30,-10 -26,-50q10,24 30,22M${VX + GW + 40},${GB - GH - 110}q30,-10 26,-50q-10,24 -30,22M${VX},${GB - GH - 230}q-8,-40 10,-60q-2,30 8,40" stroke="#c8902a" stroke-width="9" fill="none" stroke-linecap="round"/>`;
    // a shirt on a hanger hooked to each pillar
    s += `<g transform="translate(${VX - GW + 32},${GB - 330})"><path d="M0,0q14,-14 0,-26" stroke="#8a8a90" stroke-width="4" fill="none"/>${Mm.shirt(0, 0, 0.42, { id: `${id}-gs0` })}</g>`;
    s += `<g transform="translate(${VX + GW - 32},${GB - 330})"><path d="M0,0q-14,-14 0,-26" stroke="#8a8a90" stroke-width="4" fill="none"/>${Mm.shirt(0, 0, 0.42, { id: `${id}-gs1` })}</g>`;
    // the main road across the front: asphalt with a dashed centre line, a gravel shoulder and the grass verge
    const RY = o.roadY ?? 1400;
    s += `<path d="M-1300,${RY}H2400V${RY + 260}H-1300Z" fill="url(#mmAsphalt)"/><path d="M-1300,${RY}H2400" stroke="#8a7a6a" stroke-width="10"/><path d="M-1300,${RY + 260}H2400" stroke="#9a8a7a" stroke-width="12"/>`;
    for (let k = 0; k < 20; k++) s += `<path d="M${-1300 + k * 200},${RY + 128}h110" stroke="#f4f0e0" stroke-width="9" opacity=".85"/>`;
    for (let k = 0; k < 40; k++) s += `<ellipse cx="${f1(-1200 + r() * 3400)}" cy="${f1(RY + 10 + r() * 240)}" rx="${f1(10 + r() * 30)}" ry="${f1(2 + r() * 4)}" fill="#1e1a20" opacity=".4"/>`;
    s += `<rect x="-1300" y="${RY + 266}" width="3700" height="900" fill="url(#p2GrassDusk)"/>`;
    for (let k = 0; k < 50; k++) { const gx = -1200 + r() * 3400, gy = RY + 280 + r() * 500; s += tuft(gx, gy, 0.6 + (gy - RY) / 600, "#3a4a24", "#5a6a34", r); }
    // the long evening shadows of the gate across the road
    s += `<path d="M${VX - GW - 26},${GB}L${VX - GW + 400},${RY + 240}L${VX - GW + 460},${RY + 240}L${VX - GW + 26},${GB}Z" fill="#1a0e1a" opacity=".25"/><path d="M${VX + GW - 26},${GB}L${VX + GW + 400},${RY + 240}L${VX + GW + 460},${RY + 240}L${VX + GW + 26},${GB}Z" fill="#1a0e1a" opacity=".25"/>`;
    put(L.set, s);
    // the songthaew pulling away on the main road, and its dust
    if (o.bus !== false) {
      // facing left (driving off), so its rear and the step are on the right, where the passenger just got down
      const [bx, bs] = o.bus || [90, 0.95];
      put(L.set, `<g id="${id}-bus"><g transform="translate(${bx},${RY + 110}) scale(${-bs},${bs})">${Mm.songthaew()}</g></g>`);
      put(L.glow, `<g opacity=".45">${Array.from({ length: 5 }, (_, k) => `<circle cx="${f1(bx + 500 * bs + 30 + k * 46)}" cy="${f1(RY + 70 - k * 14)}" r="${f1(16 + k * 12)}" fill="#c8c0c8" opacity="${f1(0.3 - k * 0.05)}"/>`).join("")}</g>`);
    }
    put(L.glow, `<circle cx="${o.sunX ?? 160}" cy="${HZ - 40}" r="900" fill="url(#kiLampGlow)" opacity=".35" style="mix-blend-mode:screen"/>`);
    if (o.fg !== false) { let fg = ""; for (let k = 0; k < 9; k++) fg += tuft(-60 + k * 36, 2100, 3.4, "#2a3218", "#3a4622", r) + tuft(1140 - k * 36, 2120, 3.4, "#2a3218", "#3a4622", r); put(L.fg, fg); }
  }

  // ---------------- under the loudspeaker tower ----------------
  function tower2(L, o = {}) {
    const id = o.id || "tw", r = mk(o.seed || 515), TX = o.x ?? 640;
    let sk = `<rect x="-1300" y="-900" width="3700" height="3800" fill="url(#p2SkyDusk)"/><circle cx="160" cy="1100" r="700" fill="url(#p2Sun)"/>`;
    sk += cloud2(1200, 260, 1000, 260, r, "p2CloudDusk", "#f2b88a", "#5a3a54") + cloud2(-100, 520, 900, 220, r, "p2CloudDusk", "#f2b88a", "#5a3a54");
    put(L.sky, sk);
    // the tower seen from below: the pole converges upwards, the horns against the sky, the crossbar, the junction box
    let m = `<path d="M${TX - 18},2200L${TX - 9},180H${TX + 9}L${TX + 18},2200Z" fill="#8a8a84"/><path d="M${TX + 4},2200L${TX + 2},180" stroke="#c8c8c0" stroke-width="4" opacity=".6"/>`;
    m += `<path d="M${TX - 150},250H${TX + 150}" stroke="#6a6a66" stroke-width="12"/>`;
    const side = (dir) => `<g transform="translate(${TX + dir * 60},250) scale(${dir},1)"><rect x="-40" y="-26" width="44" height="52" rx="6" fill="#9a9e9a" ${OUT3}/><path d="M0,-18L170,-80V80L0,18Z" fill="#d8dcd8" ${OUT}/>
      <ellipse cx="170" cy="0" rx="20" ry="80" fill="#2a2e2c" ${OUT3}/><path d="M20,-14L150,-62" stroke="#fff" stroke-width="5" opacity=".45"/></g>`;
    m += `<g id="${id}-horns">${side(-1)}${side(1)}<g transform="translate(${TX},170)"><circle r="96" fill="#d8dcd8" ${OUT}/><circle r="80" fill="#2a2e2c"/><circle r="30" fill="#4a4e4c"/><circle r="12" fill="#1a1c1a"/><path d="M-70,-40A84,84 0 0 1 -20,-84" stroke="#fff" stroke-width="6" fill="none" opacity=".4"/></g></g>`;
    m += `<rect x="${TX - 50}" y="560" width="100" height="120" rx="8" fill="#8a9a8a" ${OUT3}/><path d="M${TX - 36},590h72M${TX - 36},616h72" stroke="#5a6a5a" stroke-width="5"/><path d="M${TX},680Q${TX + 60},900 ${TX + 10},1200" stroke="#1a1a1a" stroke-width="5" fill="none"/>`;
    for (let k = 0; k < 3; k++) m += `<g id="${id}-ring${k}" opacity="${o.rings ? 0.55 - k * 0.15 : 0}"><circle cx="${TX}" cy="170" r="${130 + k * 90}" stroke="#fff4d8" stroke-width="${7 - k * 1.5}" fill="none" stroke-dasharray="46 30"/></g>`;
    put(L.mid, m);
    // the office veranda: roof edge top left, a post, a bougainvillea; the table at the bottom with the amplifier
    let s = `<path d="M-400,-200L520,-200L380,120H-400Z" fill="#7a4a30" ${OUT}/><path d="M-400,120H380" stroke="#4a2a18" stroke-width="16"/>${Array.from({ length: 10 }, (_, k) => `<path d="M${-380 + k * 90},-200L${-360 + k * 76},120" stroke="#5a3420" stroke-width="5"/>`).join("")}`;
    s += `<rect x="40" y="110" width="44" height="1900" fill="url(#p2Wood)" ${OUT3}/>`;
    for (let k = 0; k < 26; k++) { const a = r() * 6.28, d = r() * 160; s += `<circle cx="${f1(-60 + Math.cos(a) * d)}" cy="${f1(240 + Math.sin(a) * d * 0.7)}" r="${f1(14 + r() * 14)}" fill="${["#d83a7a", "#e85a8a", "#b82a6a"][k % 3]}" ${OUT3}/>`; }
    for (let k = 0; k < 12; k++) s += `<path d="${blob(-60 + (r() - 0.5) * 300, 260 + (r() - 0.5) * 200, 22, r, 6)}" fill="#3a6a2a"/>`;
    const TY = o.tableY ?? 1560;
    s += `<path d="M-400,${TY}H1500V2400H-400Z" fill="#6a4630"/><path d="M-400,${TY}H1500" stroke="#3a2418" stroke-width="10"/><path d="M-400,${TY + 18}H1500" stroke="#9a6e4a" stroke-width="5" opacity=".6"/>`;
    s += `<g transform="translate(${o.ampX ?? 760},${TY})"><rect x="-150" y="-120" width="300" height="120" rx="8" fill="#1e1e22" ${OUT}/><rect x="-130" y="-100" width="120" height="56" rx="4" fill="#2a2a20" ${OUT3}/><g id="${id}-vu"><rect x="-124" y="-94" width="108" height="44" fill="#ffcf6a" opacity=".85"/><path d="M-110,-56L-80,-86" stroke="#2a1a0a" stroke-width="3"/></g>
      ${[20, 70, 120].map((kx) => `<circle cx="${kx}" cy="-74" r="16" fill="#c8ccd0" ${OUT3}/><path d="M${kx},-74l6,-12" stroke="#2a2a2e" stroke-width="3"/>`).join("")}<path d="M-130,-20H130" stroke="#3a3a40" stroke-width="4"/></g>`;
    s += `<g transform="translate(${o.cupX ?? 260},${TY - 6})"><path d="M-40,-150Q-46,-60 -36,0H36Q46,-60 40,-150Z" fill="#c8e4f4" opacity=".7" ${OUT3}/><path d="M-36,-110Q-40,-50 -32,0H32Q40,-50 36,-110Z" fill="#7a4a24" opacity=".85"/><path d="M-40,-150q-20,-30 6,-50M40,-150q20,-30 -6,-50" stroke="#e8f0f4" stroke-width="5" fill="none"/>
      <path d="M8,-200V-110" stroke="#e83a3a" stroke-width="7"/>${[-20, 0, 18].map((dx) => `<rect x="${dx - 10}" y="-96" width="18" height="18" rx="3" fill="#e8f4ff" opacity=".7"/>`).join("")}</g>`;
    put(L.set, s.slice(0, s.indexOf(`<path d="M-400,${TY}H1500`)));
    put(L.glow, s.slice(s.indexOf(`<path d="M-400,${TY}H1500`)));
    put(L.glow, `<circle cx="${(o.ampX ?? 760) - 70}" cy="${TY - 72}" r="120" fill="url(#mmVu)" opacity=".5" style="mix-blend-mode:screen"/><circle cx="160" cy="1100" r="900" fill="url(#kiLampGlow)" opacity=".3" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- the shadow-puppet legend ----------------
  const holes = (pts) => pts.map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="url(#mmScreen)"/>`).join("");
  function widowPuppet() { // the widow in profile facing right: tall and thin, hair to her knees, sarong, a long arm with long nails on a stick
    return `<path d="M-30,-640Q-50,-690 -6,-700Q30,-698 36,-664L50,-652L36,-642Q34,-616 16,-606L14,-580H-28Q-46,-600 -30,-640Z" fill="#120a08"/>
      <path d="M-28,-680C-70,-640 -84,-420 -70,-160Q-60,-120 -40,-150C-40,-300 -36,-500 -10,-610Z" fill="#120a08"/>
      <path d="M-34,-580Q-50,-480 -34,-360H38Q50,-480 30,-580Z" fill="#120a08"/>
      <path d="M-34,-360L-58,-20L-40,0H56L44,-360Z" fill="#120a08"/>${holes([[14, -650, 6], [-10, -300, 5], [10, -300, 5], [-14, -230, 5], [8, -230, 5], [26, -230, 5], [-18, -160, 5], [4, -160, 5], [24, -160, 5], [-20, -90, 5], [2, -90, 5], [24, -90, 5]])}
      <path d="M-40,-260H48M-48,-120H52" stroke="url(#mmScreen)" stroke-width="4"/>
      <path d="M20,-640l14,-4l-8,10z" fill="#7aff6a"/>
      <path d="M30,-560L150,-500L230,-520" stroke="#120a08" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>${[-18, -6, 6, 18].map((d) => `<path d="M230,-520l${46 + d * 0.5},${d * 1.2}" stroke="#120a08" stroke-width="5" stroke-linecap="round"/>`).join("")}
      <path d="M230,-520L230,60" stroke="#2a1a10" stroke-width="5"/><path d="M0,0V440" stroke="#2a1a10" stroke-width="7"/>`;
  }
  function sleeperPuppet() { // a young man asleep on a mat, in profile, head on a pillow at the right
    return `<path d="M-300,0H300V24H-300Z" fill="#120a08"/>${holes([[-260, 12, 5], [-200, 12, 5], [-140, 12, 5], [-80, 12, 5], [-20, 12, 5], [40, 12, 5], [100, 12, 5], [160, 12, 5], [220, 12, 5]])}
      <path d="M180,-10Q170,-50 230,-54Q290,-50 286,-10Z" fill="#120a08"/>
      <path d="M-270,-6Q-280,-60 -220,-66L60,-80Q140,-96 180,-60Q200,-30 180,-6Z" fill="#120a08"/>
      <path d="M150,-70Q150,-120 200,-124Q246,-120 248,-86Q250,-60 224,-52Q190,-48 150,-70Z" fill="#120a08"/>
      <path d="M206,-100q10,6 20,0" stroke="url(#mmScreen)" stroke-width="3" fill="none"/>${holes([[-120, -40, 5], [-60, -44, 5], [0, -48, 5], [60, -52, 5]])}
      <path d="M0,24V460" stroke="#2a1a10" stroke-width="7"/>`;
  }
  function shirtPuppet() { // the red shirt: translucent dyed hide, it glows red through the screen
    return `<path d="M-60,-300Q0,-282 60,-300L114,-276L96,-220L68,-232L70,-60Q0,-48 -68,-60L-66,-232L-96,-220L-114,-276Z" fill="#e8281e" opacity=".88"/>
      <path d="M-60,-300Q0,-282 60,-300L114,-276L96,-220L68,-232L70,-60Q0,-48 -68,-60L-66,-232L-96,-220L-114,-276Z" fill="none" stroke="#5a0806" stroke-width="7"/>
      <path d="M-24,-296Q0,-276 24,-296M-40,-200Q-30,-140 -44,-80M30,-196Q40,-140 28,-80" stroke="#8a100c" stroke-width="5" fill="none"/>${holes([[-30, -160, 4], [0, -160, 4], [30, -160, 4], [-15, -120, 4], [15, -120, 4]])}
      <path d="M-120,-300H120" stroke="#2a1a10" stroke-width="7"/><path d="M0,-300V140" stroke="#2a1a10" stroke-width="7"/>`;
  }
  function legend3(L, o = {}) {
    const id = o.id || "lg", r = mk(o.seed || 43), CX = 540, CY = o.cy ?? 820, W = 920, H = 1120;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#07060a"/>`);
    let s = `<rect x="-1300" y="${CY + H / 2 + 40}" width="3700" height="1600" fill="#0e0a08"/>`;
    s += `<g id="${id}-lamp"><rect x="${CX - W / 2}" y="${CY - H / 2}" width="${W}" height="${H}" fill="url(#mmScreen)"/></g>`;
    for (let k = 0; k < 9; k++) s += `<path d="M${CX - W / 2 + 60 + k * 100 + (r() - 0.5) * 20},${CY - H / 2}Q${CX - W / 2 + 70 + k * 100},${CY} ${CX - W / 2 + 56 + k * 100},${CY + H / 2}" stroke="#a8743a" stroke-width="3" fill="none" opacity=".22"/>`;
    s += `<rect x="${CX - W / 2 - 30}" y="${CY - H / 2 - 30}" width="${W + 60}" height="30" rx="12" fill="#5a3a1e"/><rect x="${CX - W / 2 - 30}" y="${CY + H / 2}" width="${W + 60}" height="30" rx="12" fill="#5a3a1e"/>
      <rect x="${CX - W / 2 - 30}" y="${CY - H / 2 - 200}" width="30" height="${H + 600}" rx="12" fill="#4a2e18"/><rect x="${CX + W / 2}" y="${CY - H / 2 - 200}" width="30" height="${H + 600}" rx="12" fill="#4a2e18"/>`;
    // a strip of red cloth tied along the top of the frame, like at a village fair
    s += `<path d="M${CX - W / 2 - 40},${CY - H / 2 - 30}Q${CX - W / 4},${CY - H / 2 + 10} ${CX},${CY - H / 2 - 30}T${CX + W / 2 + 40},${CY - H / 2 - 30}" stroke="#b8201a" stroke-width="18" fill="none"/>`;
    s += `<rect x="${CX - W / 2 - 40}" y="${CY + H / 2 + 30}" width="${W + 80}" height="400" fill="#1a1008"/><path d="M${CX - W / 2 - 40},${CY + H / 2 + 60}H${CX + W / 2 + 40}" stroke="#3a2412" stroke-width="6"/>`;
    s += `<defs><clipPath id="${id}-clip"><rect x="${CX - W / 2}" y="${CY - H / 2}" width="${W}" height="${H}"/></clipPath></defs><g clip-path="url(#${id}-clip)">
      <g transform="translate(${CX + 150},${CY + 330})"><g id="${id}-man">${sleeperPuppet()}</g></g>
      <g transform="translate(${CX - 300},${CY + 400})"><g id="${id}-widow">${widowPuppet()}</g></g>
      <g transform="translate(${CX + 300},${CY - 60})"><g id="${id}-rshirt" opacity="${o.shirt === false ? 0 : 1}">${shirtPuppet()}</g></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="${CX}" cy="${CY + H / 2 + 120}" r="700" fill="url(#lgSpill)" style="mix-blend-mode:screen"/>`);
    let fg = "";
    for (let k = 0; k < 7; k++) { const x = -60 + k * 190 + r() * 40, y = 1820 + r() * 60, s2 = 1 + r() * 0.3;
      fg += `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s2)})"><path d="M-110,200Q-110,40 -40,20Q0,10 40,20Q110,40 110,200Z" fill="#050404"/><ellipse cx="0" cy="-30" rx="56" ry="64" fill="#050404"/>${k % 3 === 1 ? `<path d="M-30,-80q30,-40 60,0" stroke="#050404" stroke-width="20"/>` : ""}</g>`; }
    put(L.fg, fg);
  }

  // ---------------- ลุงเปี๊ยก's place ----------------
  function yard2(L, o = {}) {
    const id = o.id || "yd", r = mk(o.seed || 616), G = o.ground ?? 1500, t = o.time || "day", dusk = t === "dusk";
    const SK = dusk ? "p2SkyDusk" : "p2SkyDay";
    let sk = `<rect x="-1300" y="-900" width="3700" height="3800" fill="url(#${SK})"/>` + cloud2(1100, 300, 1000, 280, r, dusk ? "p2CloudDusk" : "p2CloudDay", dusk ? "#f2b88a" : "#fbf6e8", dusk ? "#5a3a54" : "#8696a2");
    put(L.sky, sk);
    const FT = dusk ? ["#4a3450", "#5a4060", "#6a4c6e"] : ["#3a5a3a", "#4a6a42", "#5a7a4a"];
    let f = "";
    for (let k = 0; k < 20; k++) f += crown(-1000 + k * 170 + r() * 60, G - 420 - r() * 60, 90 + r() * 40, r, [FT[0], FT[1], FT[2], FT[2]], 6);
    f += `<rect x="-1300" y="${G - 560}" width="3700" height="300" fill="url(#p2Haze)" opacity=".7"/>`;
    put(L.far, f);
    // the house: big, so its underside is a room; the platform under it, the stairs on the right
    const HX = o.house ?? 420, HS = o.hs ?? 1.9;
    let s = `<rect x="-1300" y="${G - 300}" width="3700" height="1600" fill="url(#${dusk ? "p2GrassDusk" : "p2GrassDay"})"/><path d="M-1300,${G - 60}H2400V${G + 900}H-1300Z" fill="url(#p2Earth)" opacity=".9"/>`;
    s += house2(HX, G, HS, { time: t, under: false });
    // the bamboo platform (แคร่) under the house: top at G-170 for a sitter of scale 1
    const PX = o.seat ?? 470;
    s += `<g transform="translate(${PX},${G})"><ellipse cx="0" cy="8" rx="330" ry="30" fill="#000" opacity=".3"/><path d="M-300,-170H300V-140H-300Z" fill="#d8b878" ${OUT3}/>${Array.from({ length: 15 }, (_, k) => `<path d="M${-290 + k * 41},-168V-142" stroke="#a8884e" stroke-width="3"/>`).join("")}
      <path d="M-280,-140V0M280,-140V0M-200,-140V0M200,-140V0" stroke="#9a7a48" stroke-width="16"/><path d="M-280,-60H280" stroke="#9a7a48" stroke-width="8"/></g>`;
    // things on the platform: a fan-shaped basket, a radio
    s += `<g transform="translate(${PX + 210},${G - 176})"><rect x="-40" y="-50" width="80" height="50" rx="8" fill="#3a6a9a" ${OUT3}/><circle cx="-12" cy="-25" r="14" fill="#1e2a3a"/><rect x="10" y="-40" width="22" height="10" fill="#cfe0e8"/><path d="M30,-50l20,-50" stroke="#8a8a90" stroke-width="3"/></g>`;
    // the motorbike parked under the house, the scarecrow by the stairs, the shirt pole by the road
    s += Mm.moto(o.moto ?? -150, G + 20, 0.62, { color: "#2a5ab8" });
    put(L.set, s);
    put(L.set, Mm.scarecrow(o.crow ?? 980, G + 40, 0.92, { id: `${id}-crow` }) + Mm.shirtPole(o.pole ?? 1210, G + 60, 0.95, { id: `${id}-sh` }));
    if (dusk) put(L.glow, `<circle cx="-200" cy="${G - 600}" r="900" fill="url(#kiLampGlow)" opacity=".35" style="mix-blend-mode:screen"/>`);
    if (o.fg !== false) { let fg = ""; for (let k = 0; k < 8; k++) fg += tuft(-60 + k * 36, 2100, 3.2, "#2a3a18", "#3a5222", r) + tuft(1140 - k * 36, 2120, 3.2, "#2a3a18", "#3a5222", r); put(L.fg, fg); }
  }

  // ---------------- inside the house at supper ----------------
  function house3(L, o = {}) {
    const id = o.id || "hs", r = mk(o.seed || 717), G = o.ground ?? 1420, night = o.time === "night", PH = o.photo ?? 380;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="${night ? "#0a0e1a" : "#3a2a4a"}"/>`);
    // the window: dusk (or night) outside, the neighbour's roof and a shirt on its pole
    const WX = o.window ?? 900;
    let m = `<rect x="${WX - 150}" y="420" width="300" height="380" fill="url(#${night ? "p2SkyNight" : "p2SkyDusk"})"/>`;
    m += `<g transform="translate(${WX - 40},790) scale(.3)">${house2(0, 0, 1, { time: night ? "night" : "dusk", under: false, lit: true })}</g>${Mm.shirtPole(WX + 80, 800, 0.32, { night })}`;
    put(L.mid, m);
    // the plank wall with the window cut out, the doorway at the left
    const DX = o.door ?? 90;
    let w = `<defs><mask id="${id}-wm"><rect x="-1300" y="-900" width="3700" height="3900" fill="#fff"/><rect x="${WX - 150}" y="420" width="300" height="380" fill="#000"/><rect x="${DX - 170}" y="${G - 760}" width="340" height="760" fill="#000"/></mask></defs><g mask="url(#${id}-wm)">`;
    for (let k = 0; k < 60; k++) { const px = -1300 + k * 62; w += `<rect x="${px}" y="-900" width="60" height="${G + 900}" fill="${night ? ["#1c1620", "#201a24", "#18141c"][k % 3] : ["#8a5a3a", "#9c6a46", "#84563a"][k % 3]}"/><path d="M${px + 60},-900V${G}" stroke="${night ? "#08060a" : "#4a2e1c"}" stroke-width="3"/>`; }
    w += `<path d="M-1300,${G - 900}H2400" stroke="${night ? "#100c12" : "#5a3a24"}" stroke-width="22"/></g>`;
    w += `<rect x="${WX - 160}" y="410" width="320" height="400" fill="none" stroke="#4a2e1c" stroke-width="20"/><path d="M${WX},420V800M${WX - 150},610H${WX + 150}" stroke="#4a2e1c" stroke-width="10"/>`;
    // the doorway: dark beyond, the frame, a red shirt on a hanger hooked to the lintel
    w += `<rect x="${DX - 170}" y="${G - 760}" width="340" height="760" fill="${night ? "#04050a" : "#1a1420"}"/><path d="M${DX - 180},${G}V${G - 770}H${DX + 180}V${G}" stroke="#5a3a24" stroke-width="22" fill="none"/>`;
    w += `<circle cx="${DX + 200}" cy="${G - 600}" r="5" fill="#2a2a2a"/><g transform="translate(${DX + 200},${G - 596})"><path d="M0,0q12,-10 0,-24" stroke="#8a8a90" stroke-width="4" fill="none"/>${Mm.shirt(0, 2, 0.52, { id: `${id}-dsh`, night })}</g>`;
    // the shrine shelf high on the wall: the Buddha images, garlands, a vase of flowers
    const SX = o.shrine ?? 380;
    w += `<g transform="translate(${SX},300)"><path d="M-180,0H180L160,30H-160Z" fill="#c8902a" ${OUT3}/><path d="M-170,30L-120,90M170,30L120,90" stroke="#9a6a1a" stroke-width="10"/>
      ${[-80, 0, 80].map((bx, k) => `<g transform="translate(${bx},0) scale(${k === 1 ? 1.15 : 0.9})"><path d="M-30,0Q-34,-40 -16,-56Q0,-62 16,-56Q34,-40 30,0Z" fill="#e8c050" ${OUT3}/><circle cx="0" cy="-70" r="16" fill="#e8c050" ${OUT3}/><path d="M0,-86l-6,-14h12z" fill="#e8c050"/></g>`).join("")}
      <path d="M-150,-10q-10,-50 10,-70M150,-10q10,-50 -10,-70" stroke="#3a8a3a" stroke-width="6" fill="none"/><circle cx="-146" cy="-84" r="12" fill="#f4e8a8"/><circle cx="146" cy="-84" r="12" fill="#f4e8a8"/></g>`;
    // father's portrait: black-and-white, a young man smiling, the black ribbon draped over the frame's top corners
    w += `<g id="${id}-photo" transform="translate(${PH},${o.photoY ?? 560})"><rect x="-120" y="-150" width="240" height="300" fill="#000" opacity=".35" transform="translate(8,10)"/><rect x="-120" y="-150" width="240" height="300" fill="#c8a050" ${OUT}/><rect x="-100" y="-130" width="200" height="260" fill="#c8c4bc"/>
      <path d="M-100,130V40Q-90,-10 -40,-14Q0,-6 40,-14Q90,-10 100,40V130Z" fill="#4a4a4a"/><path d="M-20,-14L0,30L20,-14" fill="#e8e8e4"/>
      <path d="M-42,-60C-44,-110 -18,-122 2,-122C24,-122 44,-110 42,-60C40,-34 30,-20 2,-16C-26,-20 -40,-34 -42,-60Z" fill="#8a8680"/>
      <path d="M-44,-80C-50,-130 -10,-136 4,-136C30,-136 50,-120 44,-80Q30,-100 2,-100Q-26,-100 -44,-80Z" fill="#2a2a2a"/>
      <path d="M-24,-70q8,-6 14,0M10,-70q8,-6 14,0" stroke="#2a2a2a" stroke-width="4" fill="none"/><path d="M-14,-40Q2,-28 18,-40" stroke="#2a2a2a" stroke-width="4" fill="none"/>
      <path d="M-120,-150L-60,-150L-120,-90Z M120,-150L60,-150L120,-90Z" fill="#0a0a0a"/><path d="M-30,-160Q0,-140 30,-160L20,-176Q0,-166 -20,-176Z" fill="#0a0a0a"/><circle cx="0" cy="-160" r="12" fill="#0a0a0a"/>
      <path d="M-8,-160L-30,-110M8,-160L30,-110" stroke="#0a0a0a" stroke-width="12"/></g>`;
    // the calendar, the wall clock, the fluorescent tube, the fan
    // a woven fan on a nail, the ผ้าขาวม้า on a cord under the window, a mirror
    w += `<g transform="translate(560,760) rotate(-8)"><path d="M0,0V-30" stroke="#5a4a3a" stroke-width="3"/><path d="M0,0L-60,90Q0,120 60,90Z" fill="#d8b878" ${OUT3}/><path d="M0,0L-30,100M0,0V108M0,0L30,100" stroke="#a8884e" stroke-width="3"/><path d="M0,0V60" stroke="#8a5a2a" stroke-width="8"/></g>`;
    w += `<path d="M${WX - 200},${G - 380}H${WX + 200}" stroke="#4a3a2a" stroke-width="3"/><path d="M${WX - 120},${G - 380}v210h90v-210" fill="#2a7a5a" opacity=".95"/><path d="M${WX - 120},${G - 340}h90M${WX - 120},${G - 280}h90M${WX - 120},${G - 220}h90" stroke="#e8c840" stroke-width="10"/><path d="M${WX - 90},${G - 380}v210M${WX - 60},${G - 380}v210" stroke="#1e5a3e" stroke-width="6"/>`;
    w += `<g transform="translate(${o.calendar ?? 640},640)"><rect x="-80" y="-110" width="160" height="210" fill="#f4ecd8" ${OUT3}/><rect x="-80" y="-110" width="160" height="40" fill="#c8342a"/><text x="0" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="84" fill="#3a2a22">13</text></g>`;
    w += `<g transform="translate(${o.clock ?? 640},330)"><circle r="70" fill="#5a3a24" ${OUT3}/><circle r="58" fill="#f4eedc"/>${Array.from({ length: 12 }, (_, k) => `<path d="M0,-52V-44" stroke="#3a2a22" stroke-width="4" transform="rotate(${k * 30})"/>`).join("")}
      <g id="${id}-hh" transform="rotate(${o.hh ?? 195})"><path d="M-4,8V-30" stroke="#2a1e1a" stroke-width="7" stroke-linecap="round"/></g><g id="${id}-mm" transform="rotate(${o.mm ?? 180})"><path d="M-3,10V-46" stroke="#2a1e1a" stroke-width="4" stroke-linecap="round"/></g><circle r="5" fill="#c8a040"/></g>`;
    w += `<g transform="translate(${o.tube ?? 560},170)"><rect x="-190" y="-12" width="380" height="24" rx="12" fill="#e8f4ee" ${OUT3}/><rect x="-200" y="-18" width="22" height="36" rx="4" fill="#d8d8d0" ${OUT3}/><rect x="178" y="-18" width="22" height="36" rx="4" fill="#d8d8d0" ${OUT3}/></g>`;
    put(L.mid, w);
    // the floor: planks in perspective, the woven mat, the khantoke tray with supper
    let s = `<rect x="-1300" y="${G}" width="3700" height="1400" fill="url(#${night ? "mmFloorN" : "mmFloor"})"/>`;
    for (let k = 0; k < 12; k++) { const y = G + Math.pow(k / 11, 1.5) * 900; s += `<path d="M-1300,${f1(y)}H2400" stroke="#2a1a10" stroke-width="${f1(2 + k * 0.5)}" opacity=".6"/>`; }
    const TX = o.tray ?? 640, TY = o.trayY ?? 1640;
    s += `<path d="M${TX - 560},${TY - 170}H${TX + 560}L${TX + 700},${TY + 260}H${TX - 700}Z" fill="url(#mmMat)" ${OUT3}/><path d="M${TX - 560},${TY - 170}H${TX + 560}L${TX + 700},${TY + 260}H${TX - 700}Z" fill="url(#mmWeave)"/>`;
    let tray = `<g transform="translate(${TX},${TY})"><ellipse cx="0" cy="40" rx="300" ry="60" fill="#000" opacity=".3"/><ellipse cx="0" cy="0" rx="290" ry="80" fill="#a8401e" ${OUT}/><ellipse cx="0" cy="-8" rx="262" ry="66" fill="#c8602e"/>
      <path d="M-290,0V40Q0,110 290,40V0" fill="#8a3418" ${OUT3}/>
      <g transform="translate(-150,-22)"><path d="M-40,-60Q-44,-10 -34,10H34Q44,-10 40,-60Z" fill="#d8b878" ${OUT3}/><ellipse cx="0" cy="-60" rx="42" ry="12" fill="#c8a868" ${OUT3}/><path d="M-36,-40H36M-38,-20H38" stroke="#a8884e" stroke-width="3"/></g>
      <g transform="translate(20,-20)"><ellipse cx="0" cy="0" rx="70" ry="22" fill="#f4f0e6" ${OUT3}/><ellipse cx="0" cy="-4" rx="58" ry="15" fill="#e8a040"/>${[[-20, -6], [10, -2], [26, -8]].map(([x, y]) => `<path d="M${x},${y}l10,-4" stroke="#3a8a2a" stroke-width="4"/>`).join("")}<circle cx="-30" cy="-4" r="5" fill="#d82a1e"/></g>
      <g transform="translate(160,-26)"><path d="M-70,0Q0,-30 70,0Q0,20 -70,0Z" fill="#b87a3a" ${OUT3}/><path d="M60,-2l26,-10l-6,14z" fill="#b87a3a" ${OUT3}/><path d="M-40,-6l10,8M-10,-10l10,8M20,-10l10,8" stroke="#6a3a18" stroke-width="3"/></g>
      ${[[-60, 30], [100, 30]].map(([gx, gy]) => `<g transform="translate(${gx},${gy})"><path d="M-14,-40H14L11,0H-11Z" fill="#cfe4f4" opacity=".75" ${OUT3}/></g>`).join("")}</g>`;
    if (o.trayFront === false) s += tray;
    s += `<g transform="translate(${o.fan ?? 1080},${G + 60})"><ellipse cx="0" cy="6" rx="80" ry="16" fill="#000" opacity=".3"/><path d="M-70,0Q0,-20 70,0" stroke="#d8d8d0" stroke-width="16" fill="none"/><path d="M0,-6V-420" stroke="#e8e8e0" stroke-width="14"/>
      <circle cy="-520" r="110" fill="#cfe4f4" opacity=".5" ${OUT3}/>${[0, 1, 2, 3, 4, 5, 6, 7].map((k) => `<path d="M0,-520L${f1(Math.cos(k * 0.785) * 104)},${f1(-520 + Math.sin(k * 0.785) * 104)}" stroke="#9ab4c8" stroke-width="2"/>`).join("")}<circle cy="-520" r="26" fill="#2a8ac8" ${OUT3}/></g>`;
    put(L.set, s);
    if (o.trayFront !== false) put(L.glow, tray);
    put(L.glow, `<g id="${id}-tube"><ellipse cx="${o.tube ?? 560}" cy="190" rx="900" ry="700" fill="url(#mmTubeW)" style="mix-blend-mode:screen" opacity="${night ? 0.8 : 0.55}"/></g>`);
  }

  // ---------------- the อสม. flipchart ----------------
  // the page in local units: 800 wide, 1000 tall, its top-left at (0,0)
  function page(id) {
    let p = `<rect x="0" y="0" width="800" height="1000" fill="url(#mmPaper)" ${OUT3}/>`;
    p += `<text x="400" y="110" text-anchor="middle" font-family="Mali" font-weight="700" font-size="84" fill="#c8241e">ใหลตาย</text><path d="M230,132Q400,150 570,128" stroke="#c8241e" stroke-width="7" fill="none" stroke-linecap="round"/>
      <text x="400" y="196" text-anchor="middle" font-family="Mali" font-weight="700" font-size="44" fill="#1e4a9a">หัวใจ ไม่ใช่ผี</text>`;
    const heart = (cx, cy, s) => `<path d="M${cx},${cy + 120 * s}C${cx - 150 * s},${cy + 20 * s} ${cx - 140 * s},${cy - 110 * s} ${cx - 60 * s},${cy - 110 * s}C${cx - 20 * s},${cy - 110 * s} ${cx},${cy - 80 * s} ${cx},${cy - 60 * s}C${cx},${cy - 80 * s} ${cx + 20 * s},${cy - 110 * s} ${cx + 60 * s},${cy - 110 * s}C${cx + 140 * s},${cy - 110 * s} ${cx + 150 * s},${cy + 20 * s} ${cx},${cy + 120 * s}Z" fill="#f4a0a0" stroke="#c8241e" stroke-width="8" stroke-linejoin="round"/>`;
    // left: the normal heart squeezing blood out (arrows), a regular trace
    p += `<path d="M400,240V900" stroke="#9a9a9a" stroke-width="3" stroke-dasharray="14 10"/>`;
    p += `<text x="200" y="300" text-anchor="middle" font-family="Mali" font-weight="700" font-size="46" fill="#2a2a2a">ปกติ</text>`;
    p += `<g id="${id}-h0">${heart(200, 470, 1)}</g>`;
    const arrows = (cx, col) => [-1, 1].map((d) => `<path d="M${cx + d * 96},${400}q${d * 40},-26 ${d * 78},-24" stroke="${col}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M${cx + d * 174},${376}l${-d * 22},${-16}M${cx + d * 174},${376}l${-d * 18},${20}" stroke="${col}" stroke-width="9" stroke-linecap="round"/>`).join("");
    p += `<g id="${id}-a0">${arrows(200, "#1e4a9a")}</g>`;
    p += `<text x="200" y="680" text-anchor="middle" font-family="Mali" font-weight="700" font-size="42" fill="#1e4a9a">บีบเลือด ✓</text>`;
    p += `<path id="${id}-e0" d="M40,800H90L104,780L118,800H140L152,700L166,860L180,800H230L244,780L258,800H280L292,700L306,860L320,800H370" stroke="#2a8a3a" stroke-width="7" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`;
    // right: the quivering heart (scribbles inside), the crossed-out arrows, a chaotic trace
    p += `<text x="600" y="300" text-anchor="middle" font-family="Mali" font-weight="700" font-size="46" fill="#c8241e">ใหลตาย</text>`;
    p += `<g id="${id}-h1">${heart(600, 470, 1)}<path d="M540,420l20,-20l10,30l20,-30l14,36l18,-30l12,30l16,-24M530,470l22,-16l8,28l24,-30l10,34l22,-28l12,30l20,-20M560,520l18,-16l12,26l20,-24l12,22l16,-18" stroke="#8a1010" stroke-width="5" fill="none" stroke-linejoin="round"/></g>`;
    p += `<g id="${id}-x1"><g opacity=".5">${arrows(600, "#1e4a9a")}</g>${[-1, 1].map((d) => `<path d="M${600 + d * 150 - 20},${356}l40,40M${600 + d * 150 + 20},${356}l-40,40" stroke="#c8241e" stroke-width="9" stroke-linecap="round"/>`).join("")}</g>`;
    p += `<text x="600" y="730" text-anchor="middle" font-family="Mali" font-weight="700" font-size="40" fill="#c8241e">เต้นระริก ไม่บีบ ✗</text>`;
    p += `<path id="${id}-e1" d="M440,800L452,770L462,826L474,778L482,818L494,764L506,834L516,786L528,812L538,772L550,830L562,780L574,816L584,770L596,828L608,784L620,812L632,768L644,832L656,788L668,810L680,776L692,826L704,790L716,808L730,780L742,820L760,800" stroke="#c8241e" stroke-width="7" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`;
    p += `<text x="400" y="960" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#5a5a5a">อสม.บ้านโนนคำ</text>`;
    return p;
  }
  function flip2(L, o = {}) {
    const id = o.id || "fp", r = mk(o.seed || 818), close = !!o.close;
    // the sala in daylight behind: posts, the roof edge, villagers on plastic chairs (soft, it is all behind the chart)
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#e8dcc0"/><rect x="-1300" y="900" width="3700" height="2000" fill="#cbb48c"/>`);
    let f = `<path d="M-1300,-900H2400V120H-1300Z" fill="#8a5a3a"/><path d="M-1300,120H2400" stroke="#5a3420" stroke-width="30"/>`;
    for (let k = 0; k < 8; k++) f += `<rect x="${-900 + k * 420}" y="120" width="60" height="1300" fill="url(#p2Wood)"/>`;
    f += `<rect x="-1300" y="420" width="3700" height="500" fill="#bfe0f4" opacity=".55"/>`;
    for (let k = 0; k < 10; k++) { const x = -800 + k * 300 + r() * 80, y = 1300 + (k % 2) * 80; f += `<g transform="translate(${f1(x)},${y})"><rect x="-70" y="-10" width="140" height="120" rx="12" fill="${["#d83a3a", "#3a6ad8", "#e8b030"][k % 3]}" opacity=".85"/><ellipse cx="0" cy="-130" rx="56" ry="64" fill="#4a3a30"/><path d="M-90,-10Q-90,-80 0,-80Q90,-80 90,-10Z" fill="${["#f4f0e6", "#5a8a6a", "#c88a5a"][k % 3]}"/></g>`; }
    put(L.far, f);
    let s = "";
    if (close) {
      // the page fills the frame: 800×1000 scaled to 1.2, top at y 300; the spiral binding along the top edge
      s += `<g transform="translate(60,330) scale(1.2)"><rect x="12" y="16" width="800" height="1000" fill="#000" opacity=".25"/>${page(id)}${Array.from({ length: 16 }, (_, k) => `<path d="M${30 + k * 50},-14q-10,20 0,34" stroke="#5a5e64" stroke-width="6" fill="none"/>`).join("")}<rect x="0" y="-30" width="800" height="22" fill="#3a3e44"/></g>`;
    } else {
      // the easel with the pad, seen whole at the side of the frame
      s += `<g transform="translate(${o.x ?? 600},${o.y ?? 560}) scale(${o.s ?? 0.62})"><path d="M60,1000L-60,1900M740,1000L860,1900M400,1000L400,1800" stroke="#7a5a3a" stroke-width="22" stroke-linecap="round"/>
        <rect x="-10" y="-40" width="820" height="40" fill="#3a3e44"/>${page(id)}</g>`;
    }
    put(L.set, s);
    put(L.glow, `<circle cx="300" cy="200" r="1100" fill="url(#kiLampGlow)" opacity=".18" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- 3 a.m. ----------------
  // a floor mattress in perspective, centred at (cx, cy): w wide, d deep; the pillow at the left end, a folded blanket at the right
  const mattress = (cx, cy, w, d) => `<g transform="translate(${cx},${cy})"><ellipse cx="0" cy="${d * 0.62}" rx="${w * 0.6}" ry="${d * 0.28}" fill="#000" opacity=".5"/>
    <path d="M${-w * 0.47},${-d / 2}H${w * 0.47}L${w * 0.53},${d / 2}H${-w * 0.53}Z" fill="url(#mmMattress)" ${OUT3}/><path d="M${-w * 0.53},${d / 2}H${w * 0.53}V${d / 2 + 24}H${-w * 0.53}Z" fill="#8a7aa0" ${OUT3}/>
    <path d="M${-w * 0.5},0H${w * 0.5}" stroke="#a89ab8" stroke-width="2" opacity=".5"/>
    <path d="M${-w * 0.46},${-d * 0.36}Q${-w * 0.47},${-d * 0.5} ${-w * 0.37},${-d * 0.48}H${-w * 0.26}Q${-w * 0.21},${d * 0.1} ${-w * 0.27},${d * 0.38}H${-w * 0.43}Q${-w * 0.51},${d * 0.3} ${-w * 0.46},${-d * 0.36}Z" fill="#f2eef6" ${OUT3}/>
    <path d="M${w * 0.3},${-d / 2}H${w * 0.47}L${w * 0.53},${d / 2}H${w * 0.33}Z" fill="#5a7aa8" ${OUT3}/><path d="M${w * 0.31},${-d * 0.1}H${w * 0.5}M${w * 0.32},${d * 0.2}H${w * 0.52}" stroke="#3a5a88" stroke-width="3"/></g>`;
  // a mosquito net hung over a mattress: back panel, sides and top in L.set, the front panel in L.glow (it veils the sleeper)
  const netBox = (cx, top, w, h, d, nid) => {
    const bL = cx - w / 2, bR = cx + w / 2, fL = cx - w / 2 - d * 0.35, fR = cx + w / 2 + d * 0.35, bTop = top, fTop = top + d * 0.5, bBot = top + h, fBot = top + h + d;
    const mesh = (pts, op) => `<path d="${pts}" fill="#e8eef8" opacity="${op * 0.45}"/><path d="${pts}" fill="url(#mmMesh)" opacity="${op * 0.7}"/>`;
    const back = mesh(`M${bL},${bTop}H${bR}V${bBot}H${bL}Z`, 0.16) + mesh(`M${bL},${bTop}L${fL},${fTop}V${fBot}L${bL},${bBot}Z`, 0.2) + mesh(`M${bR},${bTop}L${fR},${fTop}V${fBot}L${bR},${bBot}Z`, 0.2) + mesh(`M${bL},${bTop}H${bR}L${fR},${fTop}H${fL}Z`, 0.24);
    const front = `<g id="${nid}">${mesh(`M${fL},${fTop}H${fR}V${fBot}Q${cx},${fBot + 16} ${fL},${fBot}Z`, 0.26)}
      <path d="M${fL},${fTop}V${fBot}M${fR},${fTop}V${fBot}M${fL},${fTop}H${fR}" stroke="#e8eef8" stroke-width="2.4" opacity=".4"/>
      ${[0.18, 0.43, 0.71].map((u, k) => `<path d="M${f1(fL + (fR - fL) * u)},${fTop}Q${f1(fL + (fR - fL) * (u + 0.02 * (k % 2 ? 1 : -1)))},${f1((fTop + fBot) / 2)} ${f1(fL + (fR - fL) * (u - 0.015))},${fBot}" stroke="#f4f8ff" stroke-width="16" opacity=".07" fill="none"/>`).join("")}</g>`;
    const strings = `<path d="M${bL},${bTop}L${bL - 40},-900M${bR},${bTop}L${bR + 40},-900M${fL},${fTop}L${fL - 140},-900M${fR},${fTop}L${fR + 140},-900" stroke="#c8c8d0" stroke-width="2" opacity=".4"/>`;
    return { back: strings + back, front };
  };
  function sleep2(L, o = {}) {
    const id = o.id || "sl", r = mk(o.seed || 919), G = o.ground ?? 1180, BX = o.bed ?? 560, lamp = !!o.lamp, WX = o.window ?? 1080, DX = o.door ?? 60;
    const KY = G + 470, KW = 640, KD = 200;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#brNight)"/><circle cx="${WX + 40}" cy="560" r="300" fill="url(#kiMoon)"/><circle cx="${WX + 40}" cy="560" r="26" fill="#f4f6ff"/>`);
    // the back wall: planks with moonlit gaps, the shuttered window (closed but for a crack), the doorway with the red shirt
    let w = `<defs><mask id="${id}-wm"><rect x="-1300" y="-900" width="3700" height="3900" fill="#fff"/><rect x="${WX - 130}" y="430" width="260" height="330" fill="#000"/><rect x="${DX - 150}" y="${G - 700}" width="300" height="700" fill="#000"/></mask></defs><g mask="url(#${id}-wm)">`;
    for (let k = 0; k < 60; k++) { const px = -1300 + k * 62; w += `<rect x="${px}" y="-900" width="60" height="${G + 900}" fill="${["#1c1620", "#201a24", "#18141c"][k % 3]}"/><path d="M${px + 60},-900V${G}" stroke="#9ab4ff" stroke-width="2.4" opacity="${f1(0.08 + r() * 0.2)}"/>`; }
    w += `<path d="M-1300,${G - 840}H2400" stroke="#0e0a10" stroke-width="20"/></g>`;
    w += `<rect x="${WX - 140}" y="420" width="280" height="350" fill="none" stroke="#2a201c" stroke-width="18"/>`;
    w += `<g id="${id}-winL"><path d="M${WX - 130},430H${WX - 4}V760H${WX - 130}Z" fill="#241c18" stroke="#120c0a" stroke-width="3"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${WX - 120},${462 + k * 64}H${WX - 14}" stroke="#3a2e26" stroke-width="5"/>`).join("")}</g>`;
    w += `<g id="${id}-winR"><path d="M${WX + 10},430H${WX + 130}V760H${WX + 10}Z" fill="#241c18" stroke="#120c0a" stroke-width="3"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${WX + 20},${462 + k * 64}H${WX + 120}" stroke="#3a2e26" stroke-width="5"/>`).join("")}</g>`;
    w += `<rect x="${DX - 150}" y="${G - 700}" width="300" height="700" fill="#050407"/><path d="M${DX - 160},${G}V${G - 710}H${DX + 160}V${G}" stroke="#2a1e18" stroke-width="20" fill="none"/>`;
    w += `<g transform="translate(${DX + 40},${G - 700})"><path d="M0,0q12,-10 0,-24" stroke="#5a5a60" stroke-width="4" fill="none"/>${Mm.shirt(0, 2, 0.5, { id: `${id}-dsh`, night: true })}</g>`;
    if (lamp) w += `<g transform="translate(560,120)"><path d="M0,-200V0" stroke="#2a2a2a" stroke-width="3"/><circle cx="0" cy="18" r="20" fill="#ffe8b0"/></g>`;
    put(L.mid, w);
    // the floor, the moon through the crack, Fon's mattress at the back, Keng's at the front, the mosquito coil
    let s = `<rect x="-1300" y="${G}" width="3700" height="1600" fill="url(#mmFloorN)"/>`;
    for (let k = 0; k < 13; k++) { const y = G + Math.pow(k / 12, 1.6) * 1100; s += `<path d="M-1300,${f1(y)}H2400" stroke="#06040a" stroke-width="${f1(2 + k * 0.6)}" opacity=".85"/><path d="M-1300,${f1(y + 3 + k * 0.4)}H2400" stroke="#4a3a44" stroke-width="1.4" opacity=".35"/>`; }
    const MX = o.moonX ?? BX + 470, MY = KY - 40;
    s += `<g id="${id}-moonF"><path d="M${WX - 4},440L${WX + 10},440L${MX + 150},${MY + 40}L${MX - 230},${MY + 40}Z" fill="#a8c4ff" opacity=".07"/>
      <ellipse cx="${MX - 40}" cy="${MY + 10}" rx="240" ry="90" fill="#a8c4ff" opacity=".16"/>${[-120, -40, 40].map((dx) => `<path d="M${MX + dx - 70},${MY - 50}L${MX + dx + 10},${MY - 50}L${MX + dx - 30},${MY + 60}L${MX + dx - 110},${MY + 60}Z" fill="#c8dcff" opacity=".12"/>`).join("")}</g>`;
    const FX = o.bed2 ?? 120, FY = G + 150;
    s += mattress(FX, FY, 480, 110);
    const nF = netBox(FX, G - 280, 460, 360, 110, `${id}-net2`), nK = netBox(BX, G - 210, KW + 40, 520, KD + 40, `${id}-net`);
    s += nF.back;
    put(L.set, s);
    put(L.set, nK.back + mattress(BX, KY, KW, KD));
    // the coil smouldering on its tin lid by Keng's head, its smoke (#id-smoke) a thin line
    put(L.set, `<g transform="translate(${BX - KW / 2 - 80},${KY + 60})"><ellipse cx="0" cy="6" rx="46" ry="14" fill="#5a5e62"/><path d="M-30,0a30,10 0 1 0 60,0a22,7 0 1 0 -44,0a14,5 0 1 0 28,0" stroke="#3a5a2a" stroke-width="5" fill="none"/></g>`);
    // the widow at the foot of Keng's mattress, outside his net; her eyes go in the glow
    const GX = o.ghostX ?? BX + KW / 2 + 190, GY = o.ghostY ?? KY + 70, GS = o.ghostS ?? 0.9;
    let gl = nF.front + nK.front;
    gl += `<g id="${id}-smoke"><circle cx="${BX - KW / 2 - 50}" cy="${KY + 60}" r="4" fill="#ff6a2a"/><path d="M${BX - KW / 2 - 50},${KY + 56}c-10,-40 14,-70 0,-110s14,-70 -6,-120" stroke="#c8ccd8" stroke-width="3" fill="none" opacity=".35"/></g>`;
    gl += `<g id="${id}-moon"><path d="M${WX - 4},440L${WX + 10},440L${MX + 150},${MY + 40}L${MX - 230},${MY + 40}Z" fill="url(#mmSlit)" opacity=".8" filter="url(#mmSoft)" style="mix-blend-mode:screen"/></g>`;
    if (o.ghost) gl += Mm.ghost(GX, GY, GS, { id: `${id}-ghost`, pose: "sit", rim: true, eyes: false }) + Mm.ghostEyes(GX, GY, GS, { pose: "sit", id: `${id}-ghost-eyes` });
    if (lamp) gl += `<g id="${id}-bulb"><circle cx="560" cy="138" r="560" fill="url(#mmBulb)" style="mix-blend-mode:screen"/></g>`;
    put(L.glow, gl);
  }

  Object.assign(Sets, { shirtOpen, gate2, tower2, legend3, yard2, house3, flip2, sleep2 });
})();
