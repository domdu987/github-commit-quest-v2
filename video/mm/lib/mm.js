// "ผีแม่ม่าย" sets — an Isan village where young men die in their sleep and every house hangs a red shirt.
// Same layer contract as pop2.js (sky / far / mid / set / act / fg; glow above the darkness; light = screen space). Seeded RNG only.
//   Sets.redStreet(L, o)  the village street receding to a temple roof: stilt houses both sides, a red shirt on a bamboo pole by
//                         every house (#id-sh0.. sway), the hand-painted sign "บ้านนี้ไม่มีผู้ชาย" (#id-sign), the loudspeaker tower
//                         (#id-horns), a street lamp; o.time dusk | night · o.seed · o.ground G · ids #id-lamp (lamp glow)
//   Mm.shirt(x, y, s, o)  a red T-shirt hanging from a bamboo crossbar; origin at the hook; o.id wraps it for swaying
//   Mm.sign(x, y, s, o)   the wooden board with the red brush letters; o.text
//   Mm.ghost(x, y, s, o)  ผีแม่ม่าย: coal-black, long hair over the face, thin, a torn sarong, long fingers, green eyes;
//                         o.pose "stand" | "sit" (at the foot of a mat) | "peek" (head and a hand round a door frame); origin at the feet;
//                         ids from o.id: #id (outer, no transform), #id-eyes
(function () {
  const { mk, f1, put, blob, cloud2, crown, palm, tuft, house2, puddle } = Pop2;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const Mm = (window.Mm = window.Mm || {});

  Sets.DEFS += `
    <linearGradient id="mmShirt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8443a"/><stop offset=".55" stop-color="#c8281e"/><stop offset="1" stop-color="#8a1410"/></linearGradient>
    <linearGradient id="mmShirtN" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a8302a"/><stop offset=".55" stop-color="#7a1a16"/><stop offset="1" stop-color="#4a0c0a"/></linearGradient>
    <linearGradient id="mmBoard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8a878"/><stop offset="1" stop-color="#9a7a4e"/></linearGradient>
    <linearGradient id="mmRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a3a24"/><stop offset="1" stop-color="#9a5634"/></linearGradient>
    <linearGradient id="mmRoadN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e120c"/><stop offset="1" stop-color="#3a2216"/></linearGradient>
    <radialGradient id="mmTube"><stop offset="0" stop-color="#e8fff4" stop-opacity=".75"/><stop offset=".25" stop-color="#b8f0e0" stop-opacity=".3"/><stop offset="1" stop-color="#b8f0e0" stop-opacity="0"/></radialGradient>
    <radialGradient id="mmGhostRim" cx=".5" cy=".3" r=".7"><stop offset=".7" stop-color="#0a0c0b" stop-opacity="0"/><stop offset="1" stop-color="#3a5a7a" stop-opacity=".5"/></radialGradient>`;

  // ---------------- props ----------------
  // a red tee on a bamboo crossbar, hook at (0,0), about 0.7 m tall at s 1 for a character of scale 1
  Mm.shirt = (x, y, s, o = {}) => {
    const fill = o.night ? "url(#mmShirtN)" : "url(#mmShirt)", dk = o.night ? "#3a0806" : "#7a1410";
    const tee = `<path d="M-6,0V14" stroke="#5a4a3a" stroke-width="4"/><path d="M-120,14H120" stroke="#b89a62" stroke-width="10" stroke-linecap="round"/>
      <path d="M-58,16Q0,34 58,16L112,40L94,96L66,84L68,250Q0,262 -66,250L-64,84L-94,96L-112,40Z" fill="${fill}" ${OUT3}/>
      <path d="M-24,18Q0,40 24,18" stroke="${dk}" stroke-width="5" fill="none"/>
      <path d="M-30,90Q-20,170 -36,240M22,96Q34,170 20,244M-64,84Q-60,120 -58,150" stroke="${dk}" stroke-width="4" fill="none" opacity=".55"/>
      <path d="M-46,40Q-40,80 -48,120" stroke="#ff9a8a" stroke-width="6" fill="none" opacity="${o.night ? 0.15 : 0.35}" stroke-linecap="round"/>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g ${o.id ? `id="${o.id}"` : ""}>${tee}</g></g>`;
  };
  // a pole stuck in the ground with the crossbar, the shirt hanging from it; origin at the foot of the pole
  Mm.shirtPole = (x, G, s, o = {}) => `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})"><path d="M0,0V-560" stroke="#a8884e" stroke-width="12" stroke-linecap="round"/><path d="M0,0V-560" stroke="${INK}" stroke-width="14" opacity=".25"/>
    ${[-120, -260, -400].map((k) => `<path d="M-6,${k}h12" stroke="#7a5a2a" stroke-width="4"/>`).join("")}</g>` + Mm.shirt(x + 4 * s, G - 552 * s, s, o);
  Mm.sign = (x, y, s, o = {}) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s}) rotate(${o.rot ?? -3})"><g ${o.id ? `id="${o.id}"` : ""}>
    <path d="M-40,-150V-60M40,-150V-60" stroke="#6a5030" stroke-width="5"/><rect x="-240" y="-60" width="480" height="130" rx="8" fill="url(#mmBoard)" ${OUT}/>
    <path d="M-230,-30H230M-230,10H230M-230,46H230" stroke="#8a6a3e" stroke-width="2" opacity=".5"/><circle cx="-210" cy="-36" r="5" fill="#5a4a3a"/><circle cx="210" cy="-36" r="5" fill="#5a4a3a"/>
    <text x="0" y="28" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${o.size ?? 54}" fill="#b81e18" stroke="#6a0a08" stroke-width="1.5" paint-order="stroke">${o.text || "บ้านนี้ไม่มีผู้ชาย"}</text>
    <path d="M-150,40q4,16 0,30M90,42q3,12 0,22M150,40q4,20 -2,34" stroke="#b81e18" stroke-width="4" fill="none" stroke-linecap="round" opacity=".85"/></g></g>`;

  // ---------------- the ghost ----------------
  // coal-black so it disappears in the dark; only a cold rim and the green eyes give it away
  Mm.ghost = (x, y, s, o = {}) => {
    const id = o.id || "mmg", pose = o.pose || "stand", BL = "#07090a", BL2 = "#0e1112", RIM = "#4a6a8a";
    const hair = (hx, hy, len) => `<path d="M${hx - 52},${hy - 10}C${hx - 70},${hy + len * 0.4} ${hx - 64},${hy + len * 0.8} ${hx - 40},${hy + len}Q${hx - 20},${hy + len - 30} ${hx - 6},${hy + len + 10}Q${hx + 14},${hy + len - 24} ${hx + 30},${hy + len + 6}Q${hx + 52},${hy + len - 30} ${hx + 60},${hy + len * 0.6}C${hx + 70},${hy + len * 0.3} ${hx + 60},${hy - 40} ${hx},${hy - 52}C${hx - 40},${hy - 50} ${hx - 52},${hy - 30} ${hx - 52},${hy - 10}Z" fill="${BL}"/>
      <path d="M${hx - 34},${hy}Q${hx - 40},${hy + len * 0.5} ${hx - 30},${hy + len * 0.9}M${hx + 22},${hy}Q${hx + 36},${hy + len * 0.5} ${hx + 26},${hy + len * 0.9}" stroke="${BL2}" stroke-width="5" fill="none"/>`;
    const fingers = (fx, fy, dir) => [-14, -5, 4, 13].map((d, i) => `<path d="M${fx + d},${fy}q${dir * (6 + i * 3)},${40 + i * 6} ${dir * (4 + i * 4)},${84 + i * 8}" stroke="${BL}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("");
    let g = "";
    if (pose === "sit") {
      // kneeling, sitting back on its heels at the foot of a mat, hair hanging forward over the face
      g += `<path d="M-120,0Q-130,-120 -60,-180Q0,-210 60,-180Q130,-120 120,0Z" fill="${BL}"/>`;
      g += `<path d="M-60,-180Q-70,-300 -40,-360Q0,-380 40,-360Q70,-300 60,-180Z" fill="${BL}"/>`;
      g += hair(0, -400, 330);
      g += `<path d="M-50,-330Q-90,-240 -70,-120" stroke="${BL}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M50,-330Q90,-240 74,-120" stroke="${BL}" stroke-width="22" fill="none" stroke-linecap="round"/>`;
      g += fingers(-70, -122, -1) + fingers(74, -122, 1);
      g += Pop2.eyePair(0, -384, 0.62, `${id}-eyes`);
    } else if (pose === "peek") {
      // only the head and one hand round a door frame (frame edge at x 0)
      g += hair(-20, -560, 300) + `<path d="M0,-470Q-20,-430 0,-390" stroke="${BL}" stroke-width="18" fill="none"/>`;
      g += `<path d="M10,-440q-30,-6 -44,4" stroke="${BL}" stroke-width="14" stroke-linecap="round"/>` + fingers(-36, -438, -1).replace(/q/g, "q").slice(0);
      g += Pop2.eyePair(-24, -548, 0.62, `${id}-eyes`);
    } else {
      // standing: too thin, too tall, the sarong torn into strips at the hem, arms hanging past the knees
      g += `<path d="M-64,0L-52,-120Q-60,-260 -40,-330L40,-330Q60,-260 52,-120L64,0L40,-18L22,6L4,-22L-16,4L-36,-20Z" fill="${BL}"/>`;
      g += `<path d="M-40,-330Q-50,-460 -34,-540Q0,-560 34,-540Q50,-460 40,-330Z" fill="${BL}"/>`;
      g += `<path d="M-36,-520Q-74,-380 -78,-150" stroke="${BL}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M36,-520Q74,-380 80,-150" stroke="${BL}" stroke-width="20" fill="none" stroke-linecap="round"/>`;
      g += fingers(-78, -150, -1) + fingers(80, -150, 1);
      g += hair(0, -600, 330);
      g += `<path d="M-60,-120Q0,-100 60,-120" stroke="${BL2}" stroke-width="4" fill="none"/>`;
      g += Pop2.eyePair(0, -590, 0.62, `${id}-eyes`);
    }
    if (o.rim !== false) g += `<g opacity=".55">${pose === "stand" ? `<path d="M40,-540Q52,-460 42,-330Q60,-260 52,-120" stroke="${RIM}" stroke-width="3" fill="none"/>` : `<path d="M60,-180Q130,-120 120,0" stroke="${RIM}" stroke-width="3" fill="none"/>`}</g>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}">${g}</g></g>`;
  };

  // ---------------- the loudspeaker tower (หอกระจายข่าว) ----------------
  const horns = (x, G, s, id) => `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">
    <path d="M-10,0V-1100" stroke="#8a8a84" stroke-width="22"/><path d="M-10,0V-1100" stroke="${INK}" stroke-width="24" opacity=".2"/>
    ${[-200, -420, -640, -860].map((k) => `<path d="M-24,${k}h28" stroke="#5a5a56" stroke-width="6"/>`).join("")}
    <path d="M-120,-1080H100" stroke="#6a6a66" stroke-width="12"/>
    <g id="${id}">${[[-110, -1110, -18], [-10, -1140, 0], [90, -1110, 18]].map(([hx, hy, a]) => `<g transform="translate(${hx},${hy}) rotate(${a})"><path d="M-20,-20L-60,-70H60L20,-20Z" fill="#c8ccc8" ${OUT3}/><ellipse cx="0" cy="-70" rx="60" ry="14" fill="#2a2e2c" ${OUT3}/><rect x="-20" y="-24" width="40" height="22" fill="#9a9e9a" ${OUT3}/></g>`).join("")}</g>
    <rect x="-40" y="-760" width="60" height="70" rx="6" fill="#8a9a8a" ${OUT3}/><path d="M-30,-740h40M-30,-722h40" stroke="#5a6a5a" stroke-width="4"/></g>`;

  // ---------------- Sets.redStreet ----------------
  function redStreet(L, o = {}) {
    const id = o.id || "rs", r = mk(o.seed || 909), G = o.ground ?? 1400, t = o.time || "night", night = t === "night";
    // sky: deep night with a hazy moon, or a bruised dusk; slow heavy clouds
    const SK = night ? "p2SkyNight" : "p2SkyDusk", CL = night ? ["#121826", "#1a2232", "#283246"] : ["#5a3a54", "#9a6070", "#e8a07a"];
    let sk = `<rect x="-1300" y="-900" width="3700" height="3800" fill="url(#${SK})"/>`;
    if (night) {
      for (let k = 0; k < 90; k++) sk += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-700 + r() * 1500)}" r="${f1(1 + r() * 1.8)}" fill="#e8ecff" opacity="${f1(0.2 + r() * 0.6)}"/>`;
      sk += `<circle cx="${o.moonX ?? 820}" cy="${o.moonY ?? 380}" r="380" fill="url(#kiMoon)"/><circle cx="${o.moonX ?? 820}" cy="${o.moonY ?? 380}" r="40" fill="#f2f4ff"/>`;
    } else sk += `<circle cx="${o.sunX ?? 300}" cy="${o.sunY ?? 980}" r="560" fill="url(#p2Sun)"/>`;
    sk += cloud2(1400, 520, 1000, 280, r, night ? "p2CloudNight" : "p2CloudDusk", CL[2], CL[0]) + cloud2(-300, 300, 1100, 320, r, night ? "p2CloudNight" : "p2CloudDusk", CL[2], CL[0]);
    put(L.sky, sk);
    // far: tree line, sugar palms and the temple roof with its chofa on the horizon at the end of the street
    const FT = night ? ["#0a0f15", "#0e141c", "#121a24"] : ["#4a3a52", "#5a4862", "#6a5672"];
    let f = "";
    for (let k = 0; k < 24; k++) f += crown(-1200 + k * 150 + r() * 60, G - 220 - r() * 40, 80 + r() * 40, r, [FT[0], FT[1], FT[2], FT[2]], 6);
    for (let k = 0; k < 6; k++) f += palm(-900 + k * 520 + r() * 100, G - 200, 0.42 + r() * 0.12, FT[0]);
    const tx = o.temple ?? 560, ty = G - 210;
    f += `<g transform="translate(${tx},${ty})" fill="${FT[0]}"><path d="M-170,0V-90H170V0Z"/><path d="M-210,-90L-120,-170L120,-170L210,-90Z"/><path d="M-150,-170L-60,-250L60,-250L150,-170Z"/>
      <path d="M-60,-250Q-62,-286 -40,-300M60,-250Q62,-286 40,-300" stroke="${FT[0]}" stroke-width="8" fill="none"/><path d="M0,-250V-380" stroke="${FT[0]}" stroke-width="10"/><path d="M-212,-90q-14,-30 4,-48M212,-90q14,-30 -4,-48" stroke="${FT[0]}" stroke-width="7" fill="none"/></g>`;
    f += `<rect x="-1300" y="${G - 360}" width="3700" height="260" fill="url(#p2Haze)" opacity="${night ? 0.6 : 1}"/>`;
    put(L.far, f);
    // mid: the far houses down the street, smaller and hazier, each with its shirt
    let m = "";
    [[200, G - 120, 0.34, false], [900, G - 120, 0.32, true], [60, G - 70, 0.48, false], [1040, G - 70, 0.46, true]].forEach(([hx, hy, hs, flip], k) => {
      m += `<g transform="translate(${hx},${hy}) scale(${flip ? -1 : 1},1) translate(${-hx},${-hy})" opacity=".85">${house2(hx, hy, hs, { lit: night && k % 2 === 0, time: t, under: false })}</g>`;
      m += Mm.shirtPole(hx + (flip ? -1 : 1) * 210 * hs, hy, hs * 0.75, { night, id: `${id}-shm${k}` });
    });
    m += `<rect x="-1300" y="${G - 200}" width="3700" height="200" fill="url(#p2Haze)" opacity=".5"/>`;
    put(L.mid, m);
    // set: the laterite street narrowing to the temple, verges, the near houses, shirts, the sign, the tower, the lamp
    const earth = night ? "url(#mmRoadN)" : "url(#mmRoad)";
    let s = `<rect x="-1300" y="${G - 80}" width="3700" height="1400" fill="url(#${night ? "p2GrassNight" : "p2GrassDusk"})"/>`;
    s += `<path d="M${tx - 70},${G - 80}H${tx + 70}L${tx + 760},${G + 900}H${tx - 760}Z" fill="${earth}"/>`;
    s += `<path d="M${tx - 30},${G - 70}L${tx - 300},${G + 900}M${tx + 30},${G - 70}L${tx + 300},${G + 900}" stroke="${night ? "#120a06" : "#7a3e22"}" stroke-width="16" opacity=".5"/>`;
    for (let k = 0; k < 18; k++) { const u = r(), py = G - 60 + u * 940, w = 70 + u * 700; s += `<ellipse cx="${f1(tx + (r() - 0.5) * w)}" cy="${f1(py)}" rx="${f1(4 + u * 12)}" ry="${f1(2 + u * 4)}" fill="${night ? "#0a0604" : "#5a2a16"}" opacity=".5"/>`; }
    [[tx - 120, G + 360, 120, 20], [tx + 210, G + 620, 170, 30]].forEach(([px, py, rx, ry]) => { s += puddle(px, py, rx, ry, r, night ? "night" : "dusk"); });
    for (let k = 0; k < 80; k++) { const gx = -1200 + r() * 3400, gy = G - 60 + r() * 900; if (Math.abs(gx - tx) < 120 + (gy - G + 80) * 0.78) continue; s += tuft(gx, gy, 0.45 + (gy - G) / 800, night ? "#0c160a" : "#3a4a24", night ? "#16241a" : "#5a6a34", r); }
    // near houses: left one faces right, right one is mirrored so its stairs come down to the street
    const NL = o.left ?? [-330, G + 60, 0.95], NR = o.right ?? [1420, G + 80, 0.95];
    s += house2(NL[0], NL[1], NL[2], { lit: night, time: t });
    s += `<g transform="translate(${NR[0]},${NR[1]}) scale(-1,1) translate(${-NR[0]},${-NR[1]})">${house2(NR[0], NR[1], NR[2], { lit: false, time: t })}</g>`;
    // bamboo fences along the verges
    const fence = (x0, y0, n, dx, dy, sc) => Array.from({ length: n }, (_, k) => `<rect x="${f1(x0 + k * dx)}" y="${f1(y0 + k * dy - 150 * sc)}" width="${f1(12 * sc)}" height="${f1(150 * sc)}" rx="4" fill="${night ? "#1a1410" : "#8a6e44"}" stroke="${INK}" stroke-width="2"/>`).join("") +
      `<path d="M${x0},${f1(y0 - 110 * sc)}L${f1(x0 + n * dx)},${f1(y0 + n * dy - 110 * sc)}M${x0},${f1(y0 - 50 * sc)}L${f1(x0 + n * dx)},${f1(y0 + n * dy - 50 * sc)}" stroke="${night ? "#1a1410" : "#6a5034"}" stroke-width="${f1(7 * sc)}"/>`;
    s += fence(tx - 230, G - 40, 7, -40, 36, 0.8) + fence(tx + 210, G - 40, 7, 40, 36, 0.8);
    // the shirts of the near houses and the sign on the left gate
    s += Mm.shirtPole(NL[0] + 520 * NL[2], NL[1] + 10, 0.92, { night, id: `${id}-sh0` });
    s += Mm.shirtPole(NR[0] - 560 * NR[2], NR[1] + 10, 0.92, { night, id: `${id}-sh1` });
    s += Mm.sign(NL[0] + 640 * NL[2], NL[1] - 150, 0.62, { id: `${id}-sign`, rot: -4 });
    // the tower and the lamp post on the right verge
    s += horns(o.horns ?? 900, G - 30, 0.62, `${id}-horns`);
    const LX = o.lampX ?? 240;
    s += `<g transform="translate(${LX},${G - 20})"><path d="M0,0V-760" stroke="#5a4a3a" stroke-width="16"/><path d="M0,-740H120" stroke="#5a4a3a" stroke-width="8"/><rect x="60" y="-736" width="110" height="16" rx="8" fill="${night ? "#f4fff8" : "#d8e0dc"}" ${OUT3}/></g>`;
    put(L.set, s);
    if (night) put(L.glow, `<g id="${id}-lamp"><circle cx="${LX + 115}" cy="${G - 748}" r="420" fill="url(#mmTube)" style="mix-blend-mode:screen"/><ellipse cx="${LX + 120}" cy="${G + 20}" rx="380" ry="70" fill="#d8fff0" opacity=".12"/></g>`);
    if (o.fg !== false) {
      const FC = night ? ["#040804", "#08100a"] : ["#2a3218", "#3a4622"];
      let fg = "";
      for (let k = 0; k < 9; k++) fg += tuft(-60 + k * 34, 2110, 3.2, FC[0], FC[1], r) + tuft(1140 - k * 34, 2130, 3.4, FC[0], FC[1], r);
      put(L.fg, fg);
    }
  }

  Object.assign(Sets, { redStreet });
})();
