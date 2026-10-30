// "ติดเกาะ" — เกาะผี, a small uninhabited islet in the Gulf of Thailand: the beach the two children are stranded on, seen from the beach
// out to sea and from the shallows looking inland, the opener close-up of a girl's hand scooping seawater, the inserts (the foam box,
// the last water bottle, a green coconut on the stake) and the first night by a driftwood fire. Same layer contract as tide.js
// (sky / far / mid / set / act / glow / fg; glow above the darkness; light = screen space). Seeded RNG only, gradients only, no filters.
// Everything that moves is redrawn from the timeline clock by one proxy tween per call (Isl.beach / Isl.scoop), so any seek is right.
// Ink #2e2a26. Needs pop2.js, qkmat.js and tide.js loaded first (Tide.coco palms, Tide.fig small figures).
//
//   Sets.islBeach(L, o)   o.view "sea" (default) | "land" · o.time "morning" | "noon" | "dusk-rain" | "night" · o.seed
//     view "sea"   from the dry sand looking out over the lagoon: the sun-lit shallows (clear water over sand and coral, the lure)
//                  between the shore o.shore metres out (10) and the reef edge (30 m), then the open sea to the horizon o.hz (640);
//                  camera o.hc metres up (2.6). A ground point d metres away is at y = hz + 2400·hc/d (Isl.seaY(id, d)); an adult
//                  standing d metres away has rig scale Isl.seaS(d) (≈ 6.4/d). Two dark rock headlands close the bay left and right,
//                  เกาะหลังเต่า is a haze-blue shape on the horizon (left). o.light true: one lamp far out at sea (#id-farlight, blinks
//                  slowly, with its reflection #id-farref) · o.glow true: bioluminescence along the swash and in the shallows (night; #id-glow,
//                  brighter wherever the water moves) · o.box true: the boat's foam box washed up on the sand (#id-box) · o.fire true:
//                  a driftwood fire on the sand at o.fireAt ([330, 1660]; #id-fire flames redrawn, #id-firepool its light on the sand,
//                  #id-embers) · o.poncho true: ฟ้า's orange poncho rigged on two sticks to catch rain (#id-poncho; sags with water once
//                  o.rain has run) · o.palms false: no framing palms · o.mud false: no footprints
//                  ids (redrawn): #id-water #id-wclipP #id-shal #id-foam #id-foam2 #id-swash #id-caus (drifts) #id-glitter #id-birds
//                  #id-palm0/1 (fronds, data-o = crown)
//     view "land"  from the water's edge looking inland (the swash at the bottom, redrawn #id-swash/#id-swashW): the curve of the beach,
//                  the dune with beach grass, the coconut grove (#id-palm0…3 fronds sway; fallen green coconuts under them #id-coco0…,
//                  the old camp's sharpened stake planted beside the pile #id-stake), the jungle ridge behind with the islet's top of bare
//                  rock (#id-top) carrying three small stone fire rings (#id-ring0..2), the rock shelter on the right (#id-shelter: an
//                  overhanging boulder, its dark mouth, the bamboo bird-rattle #id-rattle hanging from a crossbar), the pool of shade under
//                  the big palm at (300, 1700) (#id-shade). Stand people on the sand y 1620–1960 at rig scale 0.8–1.0 (Isl.LAND.spots:
//                  fa [430, 1880, 0.95], phum [700, 1910, 0.72], shade [330, 1800, 0.95] (sitting under the palm), stake [880, 1700, 0.8]).
//                  o.rain [a, b] seconds into Isl.beach when the rain starts / is full (dusk-rain starts at 0) · o.camp false hides the old
//                  camp's things (stake, rattle, rings) for the arrival shots
//   Sets.islNight(L, o)   = islBeach view "sea" time "night" with o.light, o.fire, o.poncho on (the first night) — pass o.view "land"
//                  for the land side at night (fire at o.fireAt)
//   Isl.beach(tl, id, t0, dur, o)  runs either view: the swash, glitter and caustics, the palms' sway, the birds, the far lamp, the glow,
//                  the fire, the rain (o.rain [a, b] seconds into the call → #id-rain streaks fade in; o.rainOut t fades them out)
//   Sets.islHand(L, o)   the opener / hook: straight down into the shallows at the water's edge, ฟ้า's right hand (skin #ebbd95, the pink
//                  scrunchie on the wrist, the mint sleeve hem at the lower-right corner) cupping clear water, palm up, seen from over her
//                  shoulder — no face in the shot. o.from/o.to [x, y] the wrist deep in the water / lifted, o.shoulder the corner the forearm
//                  comes from ([1200, 2080]), o.rot the hand's turn (-32). The title o.title
//                  ("ติดเกาะ") and o.sub ("EP.1") scratched into the wet sand at the bottom with a stick (o.fs size, o.at [x, y]) · the
//                  water's caustics drift, glints wink · Isl.scoop(tl, id, t0, dur, o) dips the cupped hand (o.from 0, tinted under the
//                  water) and lifts it slowly toward the camera (o.to 1): the water runs out between the fingers in three streams
//                  (#id-st0..2) and drops (#id-drop0..7) that ring the surface below (#id-rip0..4), the pool in the palm drains
//                  (#id-poolG), and near the end the hand trembles, hesitating
//   Sets.islInsert(L, o)  o.kind "box": the boat's foam box washed up on the sand, lid open: the vinegar bottle (label น้ำส้มสายชู),
//                  a coil of rope, a stack of plastic cups, a sponge (#id-lid) · "bottle": the last PET bottle lying on the hot sand with a
//                  little water in it (#id-water the level; Isl.shake(tl, id, t0, dur) tips it and the water sloshes), heat shimmer lines
//                  (#id-shimmer) · "coco": a green coconut rammed onto the sharpened stake, the husk torn open, the water running into a
//                  plastic cup (#id-stream, #id-cup; Isl.pour(tl, id, t0, dur) runs the stream and fills the cup)
//   Isl.PAL  the palettes by time · Isl.cocoNut(x, y, s, o) a green coconut (o.open, o.husk) · Isl.rock(…) · Isl.fire(id, x, y, s)
(function () {
  const { mk, f1, put, blob, cloud2, crown, smoothClosed } = Pop2;
  const Isl = (window.Isl = window.Isl || {});
  const ST = (Isl._st = Isl._st || {});
  const INK = "#2e2a26";
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const OUT2 = `stroke="${INK}" stroke-width="2" stroke-linejoin="round"`;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const sm = (a, b, x) => { const k = clamp((x - a) / (b - a), 0, 1); return k * k * (3 - 2 * k); };
  const lerp = (a, b, k) => a + (b - a) * k;
  const hx = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  const mix = (a, b, k) => { const A = hx(a), B = hx(b); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const T = Qk.tone, CS = Qk.cs;
  const el = (id) => document.getElementById(id);
  const P2 = (p) => `${f1(p[0])},${f1(p[1])}`;
  const dRand = (r, a, b) => a * Math.pow(b / a, r());

  Sets.DEFS += `
    <linearGradient id="isTrunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6e6052"/><stop offset=".55" stop-color="#a09078"/><stop offset="1" stop-color="#d0c0a4"/></linearGradient>
    <radialGradient id="isGlint"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
    <radialGradient id="isLamp"><stop offset="0" stop-color="#fff2c8" stop-opacity="1"/><stop offset=".3" stop-color="#ffd27a" stop-opacity=".6"/><stop offset="1" stop-color="#ffb84a" stop-opacity="0"/></radialGradient>
    <radialGradient id="isFirePool"><stop offset="0" stop-color="#ffb860" stop-opacity=".85"/><stop offset=".35" stop-color="#ff9a3a" stop-opacity=".4"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="isGlowC"><stop offset="0" stop-color="#9ffcff" stop-opacity=".9"/><stop offset=".5" stop-color="#3ee8ff" stop-opacity=".45"/><stop offset="1" stop-color="#3ee8ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="isMoon"><stop offset="0" stop-color="#fff8e0" stop-opacity=".9"/><stop offset=".25" stop-color="#e8f0ff" stop-opacity=".25"/><stop offset="1" stop-color="#c8d8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="isFoam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e2e8e8"/></linearGradient>
    <linearGradient id="isPET" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfe6ea" stop-opacity=".55"/><stop offset=".35" stop-color="#ffffff" stop-opacity=".75"/><stop offset=".6" stop-color="#d8eef2" stop-opacity=".5"/><stop offset="1" stop-color="#9ccad2" stop-opacity=".65"/></linearGradient>
    <linearGradient id="isVinegar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8d070"/><stop offset=".4" stop-color="#fff4b0"/><stop offset="1" stop-color="#d8b850"/></linearGradient>
    <linearGradient id="isCocoG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8d85a"/><stop offset=".5" stop-color="#7fb03a"/><stop offset="1" stop-color="#4e7a24"/></linearGradient>
    <linearGradient id="isStake" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a3222"/><stop offset=".5" stop-color="#7a5636"/><stop offset="1" stop-color="#3a261a"/></linearGradient>
    <linearGradient id="isRockG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6e6a62"/><stop offset=".5" stop-color="#4a4844"/><stop offset="1" stop-color="#2c2a28"/></linearGradient>
    <linearGradient id="isPoncho" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffa050"/><stop offset="1" stop-color="#e8702a"/></linearGradient>
    <linearGradient id="isLipG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8907c"/><stop offset="1" stop-color="#b86a5a"/></linearGradient>`;

  // ---------------- palettes by time of day (STYLE.md 1) ----------------
  const PAL = {
    morning: { sky: ["#2b7fd2", "#5ea9e6", "#aed8f0", "#eef6ee"], cl: ["#ffffff", "#9fb8ca"], sun: 0.75, stars: 0,
      sea: ["#b8dce0", "#4aa0c8", "#2a9fb8", "#5cc9c4", "#a6ecdf", "#e8fbf6"], sand: ["#f6ead0", "#ecd9b2", "#d8c094"], wet: ["#c7ab80", "#d8c29c"],
      bed: ["#c8ae80", "#a8905e", "#8a7850"], haze: "#e4f0ee", rock: ["#6e6a62", "#4a4844", "#2c2a28"], green: ["#2c6a3a", "#4c904a", "#8cc268"], leaf: ["#2f6e3a", "#4f9a44", "#9ccc6a"], light: 1 },
    noon: { sky: ["#2f86d6", "#6fb6ec", "#c6e6f6", "#f4f9ff"], cl: ["#ffffff", "#b8d0e0"], sun: 1, stars: 0,
      sea: ["#c8e8f0", "#1e8fb0", "#2aa6c4", "#45c6c2", "#8fe0d8", "#ffffff"], sand: ["#fbf3dc", "#f1e3c2", "#dcc498"], wet: ["#c9ad84", "#dcc6a0"],
      bed: ["#d4bc8c", "#b49c68", "#948456"], haze: "#f4f9ff", rock: ["#7a766c", "#4e4c48", "#2e2c2a"], green: ["#2e7040", "#56a050", "#98d070"], leaf: ["#2f7a3c", "#58aa48", "#a8dc70"], light: 1.1 },
    "dusk-rain": { sky: ["#4e4460", "#8a6e80", "#c89878", "#e2a56a"], cl: ["#9a8a90", "#4a3e50"], sun: 0, stars: 0,
      sea: ["#8a9aa0", "#4e7a88", "#3a6a7a", "#5a8a8a", "#7aa89e", "#c0d8cc"], sand: ["#d8c4a0", "#c8b088", "#a8906a"], wet: ["#8e7c5e", "#a08c6a"],
      bed: ["#a8906a", "#8a7656", "#6e6046"], haze: "#c8a888", rock: ["#5a5650", "#3a3834", "#222020"], green: ["#243e2c", "#3a5c3c", "#6a8a56"], leaf: ["#2a4830", "#3e6a3a", "#7a9a5a"], light: 0.6 },
    night: { sky: ["#060e1e", "#0b1a33", "#16304f", "#243e5e"], cl: ["#2e3e5c", "#101a2c"], sun: 0, stars: 1,
      sea: ["#243e58", "#102a40", "#071a2a", "#0e2c3a", "#15404a", "#2a5a60"], sand: ["#50606e", "#3e4c5a", "#2e3a46"], wet: ["#2a3640", "#36424e"],
      bed: ["#3a4652", "#2e3a44", "#242e38"], haze: "#1e3048", rock: ["#2e3238", "#1c2024", "#0e1012"], green: ["#101e18", "#1a2e22", "#2a4232"], leaf: ["#122218", "#1e3426", "#2e4a34"], light: 0.3 },
  };
  Isl.PAL = PAL;

  // ---------------- the sky: a gradient, the sun or moon, stars at night, thin high cloud, cumulus over the horizon in L.far ----------------
  function sky(L, id, P, hz, o = {}) {
    const r = mk(o.seed || 31);
    let g = `<defs><linearGradient id="${id}-skyG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(hz - 1900)}" x2="0" y2="${f1(hz + 30)}"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset=".5" stop-color="${P.sky[1]}"/><stop offset=".84" stop-color="${P.sky[2]}"/><stop offset="1" stop-color="${P.sky[3]}"/></linearGradient></defs>`;
    g += `<rect x="-3000" y="${f1(hz - 4200)}" width="8000" height="${f1(4200 + 2200)}" fill="url(#${id}-skyG)"/>`;
    if (P.sun) g += `<circle cx="${o.sunX ?? 1380}" cy="${f1(o.sunY ?? hz - 1250)}" r="${o.sunR ?? 820}" fill="url(#qkSun)" opacity="${P.sun}"/>`;
    if (P.stars) {
      for (let k = 0; k < 160; k++) { const sx = -800 + r() * 2700, sy = hz - 1900 + r() * 1700, rr = 1 + r() * 2.2; g += `<circle cx="${f1(sx)}" cy="${f1(sy)}" r="${f1(rr)}" fill="#ffffff" opacity="${f1(0.35 + r() * 0.6)}"/>`; }
      g += `<circle cx="${o.moonX ?? 860}" cy="${f1(o.moonY ?? hz - 420)}" r="260" fill="url(#isMoon)"/><path d="M${o.moonX ?? 860},${f1((o.moonY ?? hz - 420) - 46)}a46,46 0 1 0 0,92a36,42 0 1 1 0,-92z" fill="#fff6dc" opacity=".95"/>`;
    }
    for (let k = 0; k < 8; k++) { const cx = -900 + r() * 3000, cy = hz - 1750 + r() * 900, w = 380 + r() * 620; g += `<path d="M${f1(cx)},${f1(cy)}q${f1(w * 0.5)},${f1(-14 - r() * 18)} ${f1(w)},${f1(-4 + r() * 10)}" stroke="${P.stars ? "#3a5070" : "#ffffff"}" stroke-width="${f1(6 + r() * 9)}" opacity="${f1(0.1 + r() * 0.14)}" stroke-linecap="round" fill="none"/>`; }
    const grad = P.stars ? "p2CloudNight" : P.sun ? "tdCloudM" : "tdCloudS";
    for (let k = 0; k < 6; k++) g += cloud2(-760 + k * 640 + r() * 220, hz - 820 - r() * 700, 300 + r() * 320, 96 + r() * 60, r, grad, P.cl[0], P.cl[1]);
    if (!P.sun && !P.stars) for (let k = 0; k < 7; k++) g += cloud2(-900 + k * 560 + r() * 200, hz - 1400 + r() * 900, 900 + r() * 500, 300 + r() * 160, r, "tdCloudS", "#8a7e88", "#2e2838");
    put(L.sky, g);
    let fr = "";
    for (let k = 0; k < (P.sun ? 4 : 7); k++) fr += cloud2(-1000 + k * 700 + r() * 220, hz - 150 - r() * 120, 360 + r() * 420, 150 + r() * 120, r, grad, P.cl[0], P.cl[1]);
    put(L.far, `<g opacity="${P.stars ? 0.5 : 1}">${fr}</g>`);
  }

  // ---------------- small pieces ----------------
  // a green drinking coconut (box ~90 wide at s 1), the stem end up-left; o.open: the top hacked off, o.husk: the husk torn, o.shade colour
  Isl.cocoNut = (x, y, s = 1, o = {}) => {
    let g = CS(0, 26, 44, 10, 0.7);
    g += `<path d="M-40,8C-44,-20 -28,-44 0,-46C28,-44 44,-20 40,8C36,30 18,42 0,42C-18,42 -36,30 -40,8Z" fill="url(#isCocoG)" ${OUT3}/>`;
    g += `<path d="M-6,-46L-12,-58q6,-4 10,0L0,-46" fill="#8a6a34" ${OUT2}/><path d="M-30,-18Q-20,-34 -4,-40" stroke="#dff2a0" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>`;
    g += `<path d="M-14,-30L8,34M10,-36L26,26" stroke="#5a8a2a" stroke-width="2" opacity=".5"/>`;
    if (o.open) g += `<path d="M-18,-40Q0,-30 18,-40L14,-28Q0,-22 -14,-28Z" fill="#f6ecd0" ${OUT2}/><ellipse cx="0" cy="-32" rx="8" ry="4" fill="#5a4a30"/>`;
    if (o.husk) g += `<path d="M-30,-20L-54,-38L-40,-2Z M28,-24L54,-30L38,0Z" fill="#c8a860" ${OUT2}/><path d="M-50,-34l-8,-10M50,-28l9,-8" stroke="#b89050" stroke-width="3"/>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})">${g}</g>`;
  };
  // a dark boulder with a lit top (the sun on the right), weathered cracks, barnacle flecks at the foot; w × h, origin the ground middle
  Isl.rock = (x, y, w, h, r, P, o = {}) => {
    const pts = [];
    const n = 12;
    for (let i = 0; i <= n; i++) { const u = i / n, a = Math.PI * (1 - u); pts.push([x + Math.cos(a) * w * 0.5 * (0.9 + r() * 0.2), y - Math.sin(a) * h * (0.8 + r() * 0.3) * Math.pow(Math.sin(Math.PI * u), 0.5)]); }
    pts.push([x + w * 0.5, y + 4], [x - w * 0.5, y + 4]);
    const d = smoothClosed(pts), rc = o.pal || P.rock;
    let g = CS(x + 6, y + 6, w * 0.6, h * 0.14, 0.8);
    g += `<defs><linearGradient id="${o.id || "isr"}${Math.round(x)}${Math.round(y)}" gradientUnits="userSpaceOnUse" x1="${f1(x - w / 2)}" y1="${f1(y - h)}" x2="${f1(x + w / 2)}" y2="${f1(y)}"><stop offset="0" stop-color="${rc[1]}"/><stop offset=".45" stop-color="${rc[0]}"/><stop offset="1" stop-color="${rc[2]}"/></linearGradient></defs>`;
    g += `<path d="${d}" fill="url(#${o.id || "isr"}${Math.round(x)}${Math.round(y)})" ${OUT3}/>`;
    for (let k = 0; k < 4; k++) { const cx = x - w * 0.3 + r() * w * 0.6, cy = y - h * (0.2 + r() * 0.6); g += `<path d="M${f1(cx)},${f1(cy)}l${f1((r() - 0.5) * w * 0.2)},${f1(h * 0.2)}l${f1((r() - 0.5) * w * 0.15)},${f1(h * 0.18)}" stroke="${rc[2]}" stroke-width="2.4" fill="none" opacity=".7"/>`; }
    g += `<path d="M${f1(x - w * 0.1)},${f1(y - h * 0.92)}Q${f1(x + w * 0.2)},${f1(y - h * 1.02)} ${f1(x + w * 0.4)},${f1(y - h * 0.7)}" stroke="#ffffff" stroke-width="${f1(Math.max(2, h * 0.04))}" fill="none" opacity=".3" stroke-linecap="round"/>`;
    for (let k = 0; k < 6; k++) g += `<circle cx="${f1(x - w * 0.4 + r() * w * 0.8)}" cy="${f1(y - r() * h * 0.18)}" r="${f1(2 + r() * 3)}" fill="#e8e0d0" opacity=".6"/>`;
    return g;
  };
  // the sharpened hardwood stake the old castaway planted for husking coconuts: leaning, its tip dark with old husk fibre
  Isl.stake = (x, y, s = 1, o = {}) => `<g${o.id ? ` id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})">${CS(4, 4, 30, 8, 0.7)}
    <path d="M-16,0L-10,-170L0,-250L10,-170L16,0Z" fill="url(#isStake)" ${OUT3}/><path d="M-6,-20Q-4,-120 0,-240" stroke="#a07850" stroke-width="2.5" opacity=".6"/>
    <path d="M-12,-150l24,-6M-13,-120l26,-5M-14,-90l28,-4" stroke="#2a1a10" stroke-width="2" opacity=".5"/><path d="M-9,-200L0,-250L9,-200Z" fill="#8a7a60" opacity=".8"/>
    <path d="M-10,-214q10,6 20,-2" stroke="#c8a860" stroke-width="3" fill="none"/></g>`;
  // a driftwood fire (flames redrawn by fireDraw): the ring of stones, the logs, the glow on the sand in L.glow (added by the set)
  Isl.fire = (id, x, y, s = 1) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})"><g id="${id}">
    ${[[-70, 10, 26, 14], [-30, 20, 22, 12], [20, 22, 24, 13], [62, 12, 26, 14], [-50, -6, 20, 10], [45, -4, 20, 10]].map(([sx, sy, rx, ry]) => `<ellipse cx="${sx}" cy="${sy}" rx="${rx}" ry="${ry}" fill="#4a4842" ${OUT2}/><ellipse cx="${sx - 4}" cy="${sy - 4}" rx="${rx * 0.6}" ry="${ry * 0.4}" fill="#8a8680" opacity=".6"/>`).join("")}
    <path d="M-60,-2L40,-30" stroke="#5a3a22" stroke-width="16" stroke-linecap="round"/><path d="M-60,-2L40,-30" stroke="#8a5a32" stroke-width="7" stroke-linecap="round"/><path d="M60,0L-30,-26" stroke="#4a2e1a" stroke-width="15" stroke-linecap="round"/><path d="M60,0L-30,-26" stroke="#7a4e2c" stroke-width="6" stroke-linecap="round"/>
    <path d="M-20,-10Q0,-20 22,-8" stroke="#ff6a2a" stroke-width="6" fill="none" opacity=".9"/>
    <path id="${id}-f0" d="" fill="#ff6a1a" opacity=".9"/><path id="${id}-f1" d="" fill="#ffb02a" opacity=".95"/><path id="${id}-f2" d="" fill="#fff2b0"/>
    <g id="${id}-embers">${Array.from({ length: 9 }, (_, k) => `<circle id="${id}-e${k}" r="3" fill="#ffc060" opacity="0"/>`).join("")}</g></g></g>`;
  function fireDraw(id, t, k = 1) {
    const flame = (h, w, ph, sp) => { const pts = []; const n = 9; for (let i = 0; i <= n; i++) { const u = i / n, a = Math.PI * u, yy = -Math.sin(a) * h * (1 + 0.18 * Math.sin(t * sp + ph + u * 3)), xx = Math.cos(a) * w * (1 - 0.6 * Math.pow(Math.sin(a), 2) * 0) + 8 * Math.sin(t * sp * 1.3 + ph + u * 5) * u; pts.push([xx, yy]); } return `M${f1(-w)},0L${pts.map(P2).join("L")}L${f1(w)},0Z`; };
    const e0 = el(`${id}-f0`); if (!e0) return;
    e0.setAttribute("d", flame(150 * k, 46, 0, 9)); el(`${id}-f1`).setAttribute("d", flame(104 * k, 32, 1.2, 11)); el(`${id}-f2`).setAttribute("d", flame(52 * k, 16, 2.3, 13));
    for (let i = 0; i < 9; i++) { const life = (t * 0.45 + i * 0.37) % 1, e = el(`${id}-e${i}`); e.setAttribute("cx", f1(Math.sin(t * 1.7 + i * 2) * 26 * life)); e.setAttribute("cy", f1(-40 - life * 260)); e.setAttribute("r", f1(3 - life * 2)); e.setAttribute("opacity", f1((1 - life) * 0.9 * k)); }
  }
  // rain: a tile of slanted streaks in L.glow, drifted by rainDraw
  const rainSVG = (id, r) => { let g = ""; for (let k = 0; k < 210; k++) { const x = -200 + r() * 1500, y = -400 + r() * 2600, len = 40 + r() * 70; g += `<path d="M${f1(x)},${f1(y)}l-8,${f1(len)}" stroke="#dff2ff" stroke-width="${f1(1.4 + r() * 1.6)}" opacity="${f1(0.2 + r() * 0.3)}" stroke-linecap="round"/>`; } return `<g id="${id}-rain" opacity="0"><g id="${id}-rainT">${g}</g></g>`; };
  function rainDraw(id, t, k) {
    const g = el(`${id}-rain`); if (!g) return;
    g.setAttribute("opacity", f1(clamp(k, 0, 1)));
    el(`${id}-rainT`).setAttribute("transform", `translate(${f1(-((t * 60) % 300))},${f1((t * 1900) % 760)})`);
  }
  // sand ripples (wind), shells, a crab hole with its balls, footprints to the water: the dry beach's texture between y0 and y1
  function beachBits(r, P, y0, y1, o = {}) {
    let s = "";
    for (let k = 0; k < 26; k++) { const y = y0 + Math.pow(r(), 1.3) * (y1 - y0), x = -900 + r() * 2900, w = 80 + r() * 260; s += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},${f1(-6 - r() * 6)} ${f1(w)},0" stroke="#fff" stroke-width="3" fill="none" opacity=".32"/><path d="M${f1(x)},${f1(y + 4)}q${f1(w / 2)},${f1(-6)} ${f1(w)},0" stroke="${T(P.sand[2], -0.15)}" stroke-width="2" fill="none" opacity=".35"/>`; }
    for (let k = 0; k < 22; k++) { const y = y0 + r() * (y1 - y0), x = -500 + r() * 2100, sz = 7 + r() * 9 * ((y - y0) / (y1 - y0) + 0.4); s += `<path d="M${f1(x - sz)},${f1(y)}a${f1(sz)},${f1(sz * 0.7)} 0 0 1 ${f1(sz * 2)},0z" fill="${["#f8f2ea", "#f4d8cc", "#e8dcc0"][k % 3]}" stroke="#9a8a72" stroke-width=".9"/>`; }
    for (let k = 0; k < 6; k++) { const y = y0 + 40 + r() * (y1 - y0 - 80), x = -200 + r() * 1500, sz = 5 + r() * 5; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(sz)}" ry="${f1(sz * 0.5)}" fill="#5a4a32"/>` + Array.from({ length: 7 }, () => { const a = r() * Math.PI * 2, rr = sz * (1.8 + r() * 2.4); return `<circle cx="${f1(x + Math.cos(a) * rr)}" cy="${f1(y + Math.sin(a) * rr * 0.5)}" r="${f1(sz * 0.32)}" fill="${T(P.sand[2], -0.08)}" stroke="${T(P.sand[2], -0.3)}" stroke-width=".8"/>`; }).join(""); }
    if (o.prints !== false) for (let k = 0; k < 14; k++) { const u = k / 13, y = lerp(y1 - 40, y0 + 60, u), sz = lerp(26, 12, u), x = (o.px ?? 520) + Math.sin(u * 5) * 50 + (k % 2 ? sz * 1.5 : -sz * 1.5); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(sz * 0.5)}" ry="${f1(sz * 0.26)}" fill="${T(P.sand[2], -0.24)}" opacity=".55"/>${[-0.3, -0.1, 0.1, 0.3].map((q) => `<circle cx="${f1(x + q * sz * 1.1)}" cy="${f1(y - sz * 0.3)}" r="${f1(sz * 0.08)}" fill="${T(P.sand[2], -0.24)}" opacity=".55"/>`).join("")}`; }
    return s;
  }
  // the beach's coral heads and seagrass tufts on the lagoon floor (under the water sheet), scaled by distance
  const coralHead = (r, x, y, sz) => { const c = ["#e08a7a", "#d4a060", "#f0a088", "#8ab0b8", "#c87ab0"][Math.floor(r() * 5)]; let d = ""; for (let k = 0; k < 7; k++) { const a = -Math.PI / 2 + (r() - 0.5) * 2, L = sz * (0.5 + r() * 0.6); d += `M${f1(x)},${f1(y)}q${f1(Math.cos(a) * L * 0.5)},${f1(Math.sin(a) * L * 0.6)} ${f1(Math.cos(a) * L)},${f1(Math.sin(a) * L)}`; } return `<ellipse cx="${f1(x)}" cy="${f1(y + sz * 0.1)}" rx="${f1(sz * 0.6)}" ry="${f1(sz * 0.16)}" fill="#8a9a80" opacity=".3"/><path d="${d}" stroke="${c}" stroke-width="${f1(Math.max(1, sz * 0.2))}" stroke-linecap="round" fill="none"/><path d="${d}" stroke="#fff" stroke-width="${f1(Math.max(0.5, sz * 0.06))}" stroke-linecap="round" fill="none" opacity=".35"/>`; };
  const grassTuft = (r, x, y, sz, c = "#5e7a3a") => { let d = ""; for (let k = 0; k < 7; k++) { const dx = (r() - 0.5) * sz * 0.8, h = sz * (0.8 + r() * 0.9); d += `M${f1(x + dx * 0.3)},${f1(y)}q${f1(dx)},${f1(-h * 0.5)} ${f1(dx * 1.6)},${f1(-h)}`; } return `<path d="${d}" stroke="${c}" stroke-width="${f1(Math.max(1, sz * 0.09))}" fill="none" stroke-linecap="round"/>`; };

  // ======================== the sea view: from the dry sand looking out over the lagoon ========================
  const SEA = { FX: 2400, DR: 30, DMAX: 320 };
  function seaView(L, o) {
    const id = o.id || "ib", P = PAL[o.time || "noon"], r = mk(o.seed || 7), HZ = o.hz ?? 640, HC = o.hc ?? 2.6, FY = SEA.FX * HC, SH = o.shore ?? 10;
    const yAt = (d) => HZ + FY / d, Y0 = yAt(SH), YR = yAt(SEA.DR), night = P.stars === 1;
    sky(L, id, P, HZ, { seed: (o.seed || 7) + 1, sunX: 1300, sunY: HZ - 1150 });
    // far: เกาะหลังเต่า, a haze-blue hump on the horizon to the left, its village a few specks
    put(L.far, `<g opacity="${night ? 0.6 : 0.9}"><path d="M60,${HZ + 2}C120,${HZ - 40} 230,${HZ - 70} 300,${HZ - 58}C380,${HZ - 46} 440,${HZ - 20} 470,${HZ + 2}Z" fill="${mix(P.sky[2], P.rock[0], night ? 0.6 : 0.42)}"/><path d="M110,${HZ - 6}C170,${HZ - 34} 220,${HZ - 48} 280,${HZ - 44}" stroke="${mix(P.sky[2], P.green[1], 0.5)}" stroke-width="8" fill="none" opacity=".6"/>${night ? `<circle cx="312" cy="${HZ - 12}" r="2.5" fill="#ffd27a"/><circle cx="338" cy="${HZ - 10}" r="2" fill="#ffd27a"/>` : ""}</g>`);
    // mid: seabirds
    let bd = `<g id="${id}-birds">`;
    for (let k = 0; k < (night ? 0 : 9); k++) { const bx = 80 + r() * 900, by = HZ - 160 - r() * 300, bs = 0.5 + r() * 0.7; bd += `<path d="M${f1(bx - 15 * bs)},${f1(by)}q${f1(7 * bs)},${f1(-9 * bs)} ${f1(15 * bs)},0q${f1(7 * bs)},${f1(-9 * bs)} ${f1(15 * bs)},0" stroke="#3a4048" stroke-width="${f1(2.6 * bs)}" fill="none" stroke-linecap="round"/>`; }
    put(L.mid, bd + `</g>`);
    let s = `<defs><linearGradient id="${id}-bedG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(YR)}" x2="0" y2="${f1(Y0)}"><stop offset="0" stop-color="${T(P.bed[2], -0.1)}"/><stop offset=".5" stop-color="${P.bed[1]}"/><stop offset="1" stop-color="${P.bed[0]}"/></linearGradient>
      <linearGradient id="${id}-deepG" gradientUnits="userSpaceOnUse" x1="0" y1="${HZ}" x2="0" y2="${f1(YR)}"><stop offset="0" stop-color="${P.sea[0]}"/><stop offset=".08" stop-color="${P.sea[1]}"/><stop offset=".6" stop-color="${P.sea[2]}"/><stop offset="1" stop-color="${P.sea[3]}"/></linearGradient>
      <linearGradient id="${id}-lagG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(YR)}" x2="0" y2="${f1(Y0)}"><stop offset="0" stop-color="${P.sea[3]}" stop-opacity=".82"/><stop offset=".45" stop-color="${P.sea[4]}" stop-opacity=".42"/><stop offset="1" stop-color="${P.sea[5]}" stop-opacity=".18"/></linearGradient>
      <linearGradient id="${id}-beachG" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(Y0 - 30)}" x2="0" y2="2100"><stop offset="0" stop-color="${P.wet[0]}"/><stop offset=".1" stop-color="${P.wet[1]}"/><stop offset=".18" stop-color="${P.sand[2]}"/><stop offset=".55" stop-color="${P.sand[1]}"/><stop offset="1" stop-color="${P.sand[0]}"/></linearGradient>
      <clipPath id="${id}-wclip"><path id="${id}-wclipP" d=""/></clipPath></defs>`;
    // the lagoon floor: sand in bands of ripple, coral heads, seagrass, a few dark rocks — everything smaller with distance
    s += `<rect x="-3000" y="${f1(YR - 4)}" width="8000" height="${f1(Y0 - YR + 60)}" fill="url(#${id}-bedG)"/>`;
    for (let d = SH * 1.03; d < SEA.DR; d *= 1.06) { const y = yAt(d), a = clamp(200 / d, 0.5, 8), w = clamp(60 / d, 0.6, 4.5), ph = r() * 6; let p = ""; for (let x = -1300; x <= 2400; x += 50) p += `${p ? "L" : "M"}${x},${f1(y + Math.sin(x * 0.007 + ph) * a + Math.sin(x * 0.023 + ph * 2) * a * 0.4)}`; s += `<path d="${p}" stroke="${T(P.bed[2], -0.28)}" stroke-width="${f1(w)}" fill="none" opacity=".4"/><path d="${p}" stroke="${T(P.bed[0], 0.35)}" stroke-width="${f1(w * 0.7)}" fill="none" opacity=".5" transform="translate(0,${f1(w * 1.3)})"/>`; }
    for (let k = 0; k < 34; k++) { const d = dRand(r, SH + 1.2, SEA.DR - 2), sz = SEA.FX * (0.16 + r() * 0.22) / d; s += coralHead(r, -1000 + r() * 3000, yAt(d), sz); }
    for (let k = 0; k < 30; k++) { const d = dRand(r, SH + 1, SEA.DR - 3), sz = SEA.FX * (0.3 + r() * 0.5) / d, x = -1000 + r() * 3100, y = yAt(d); s += `<path d="M${f1(x)},${f1(y)}c${f1(sz * 0.3)},${f1(-sz * 0.2)} ${f1(sz * 0.7)},${f1(sz * 0.1)} ${f1(sz)},${f1(-sz * 0.05)}M${f1(x + sz * 0.2)},${f1(y + 1)}c${f1(sz * 0.3)},${f1(-sz * 0.15)} ${f1(sz * 0.6)},${f1(sz * 0.12)} ${f1(sz * 0.9)},0" stroke="#4e6a30" stroke-width="${f1(Math.max(0.8, sz * 0.09))}" fill="none" opacity=".8"/>`; }
    for (let k = 0; k < 9; k++) { const d = dRand(r, SH + 3, SEA.DR - 4), w = SEA.FX * (0.35 + r() * 0.6) / d, x = -1100 + r() * 3300, y = yAt(d); s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(w)}" ry="${f1(w * 0.3)}" fill="${T(P.bed[2], -0.3)}" opacity=".5"/><ellipse cx="${f1(x - w * 0.2)}" cy="${f1(y - w * 0.08)}" rx="${f1(w * 0.5)}" ry="${f1(w * 0.12)}" fill="${T(P.bed[1], 0.25)}" opacity=".6"/>`; }
    for (let k = 0; k < 10; k++) { const d = dRand(r, SH + 1, 22), sz = SEA.FX * 0.2 / d, x = -400 + r() * 1900, y = yAt(d); s += `<path d="M${f1(x - sz)},${f1(y)}C${f1(x - sz * 0.6)},${f1(y - sz * 0.5)} ${f1(x + sz * 0.6)},${f1(y - sz * 0.5)} ${f1(x + sz)},${f1(y)}C${f1(x + sz * 0.6)},${f1(y + sz * 0.5)} ${f1(x - sz * 0.6)},${f1(y + sz * 0.5)} ${f1(x - sz)},${f1(y)}Z" fill="${o.time === "night" ? T(P.bed[2], -0.15) : "#3a8ad0"}" opacity="${o.time === "night" ? ".5" : ".9"}"/><path d="M${f1(x + sz * 0.9)},${f1(y)}l${f1(sz * 0.4)},${f1(-sz * 0.35)}v${f1(sz * 0.7)}z" fill="${o.time === "night" ? T(P.bed[2], -0.3) : "#2a6ab0"}" opacity="${o.time === "night" ? ".5" : ".9"}"/>`; }
    // the beach toward the camera: a wet band that mirrors the sky, the high-tide line, then dry sand
    s += `<rect x="-3000" y="${f1(Y0 - 30)}" width="8000" height="2200" fill="url(#${id}-beachG)"/>`;
    s += `<rect x="-3000" y="${f1(Y0 - 30)}" width="8000" height="${f1((yAt(SH * 0.8) - Y0) + 30)}" fill="${P.sky[2]}" opacity=".22"/>`;
    for (let k = 0; k < 30; k++) { const y = Y0 + r() * (yAt(SH * 0.8) - Y0), x = -900 + r() * 2900, w = 60 + r() * 240; s += `<path d="M${f1(x)},${f1(y)}h${f1(w)}" stroke="#fff" stroke-width="${f1(1.5 + r() * 2.5)}" opacity="${f1(0.18 + r() * 0.3)}" stroke-linecap="round"/>`; }
    const Yt = yAt(SH * 0.66);
    for (let k = 0; k < 90; k++) { const x = -1200 + r() * 3500, y = Yt + (r() - 0.5) * 26 + Math.sin(x * 0.004) * 14, w = 8 + r() * 26; s += `<path d="M${f1(x)},${f1(y)}l${f1(w)},${f1((r() - 0.5) * 6)}" stroke="${["#6a5a3a", "#3a3428", "#8a7a52", "#f2ece0"][k % 4]}" stroke-width="${f1(2 + r() * 3)}" stroke-linecap="round" opacity=".8"/>`; }
    s += beachBits(r, P, yAt(SH * 0.78), 2000, { prints: o.mud !== false, px: 480 });
    // the headlands: dark boulders closing the bay on both sides, down into the water with white water at their feet
    const hl = (x0, dir) => { let g = ""; const dd = [[34, 240, 170], [27, 300, 230], [21, 330, 290], [16, 300, 240], [12.5, 240, 170]]; dd.forEach(([d, w, h], i) => { const sc = SEA.FX / d / 60, x = x0 + dir * (i * 40) + (r() - 0.5) * 30; g += Isl.rock(x, yAt(d) + 6, w * sc * 0.8, h * sc * 0.8, r, P, { id: `isr${id}${i}${dir > 0 ? "r" : "l"}` }); }); return g; };
    put(L.set, s);
    // the water (redrawn): the open sea to the reef, the breakers on the reef, the translucent lagoon sheet with caustics, the swash foam
    let spark = "";
    const SPK = night ? 0.25 : P.sun ? 1 : 0.5;
    for (let k = 0; k < 140; k++) { const d = dRand(r, SEA.DR + 2, SEA.DMAX), y = yAt(d), x = -1200 + r() * 3500, len = SEA.FX * (0.4 + r() * 1.8) / d; spark += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(clamp(40 / d, 0.6, 3.4))}" opacity="${f1((0.25 + r() * 0.5) * SPK)}" stroke-linecap="round"/>`; }
    for (let k = 0; k < 60; k++) { const d = dRand(r, SEA.DR + 2, 200), y = yAt(d), x = -1200 + r() * 3500, len = SEA.FX * (0.8 + r() * 2.2) / d, hh = len * 0.12; spark += `<path d="M${f1(x)},${f1(y)}q${f1(len / 2)},${f1(-hh)} ${f1(len)},0" stroke="${T(P.sea[2], -0.25)}" stroke-width="${f1(clamp(50 / d, 0.6, 4))}" fill="none" opacity=".45"/><path d="M${f1(x + len * 0.2)},${f1(y - hh * 0.6)}q${f1(len * 0.3)},${f1(-hh * 0.4)} ${f1(len * 0.6)},0" stroke="#fff" stroke-width="${f1(clamp(30 / d, 0.5, 2.6))}" fill="none" opacity="${f1(0.55 * SPK)}"/>`; }
    let ca = "";
    for (let k = 0; k < 90; k++) { const d = dRand(r, SH + 0.5, SEA.DR), x = -1200 + r() * 3500, y = yAt(d), rr = SEA.FX * (0.6 + r() * 1.2) / d; ca += `<path d="M${f1(x - rr)},${f1(y)}q${f1(rr * 0.5)},${f1(-rr * 0.16)} ${f1(rr)},0t${f1(rr)},0" stroke="#f4fdff" stroke-width="${f1(clamp(60 / d, 1, 4))}" fill="none" opacity="${f1((0.18 + r() * 0.28) * (night ? 0.4 : 1))}"/>`; }
    let w = `<g id="${id}-sea"><rect x="-3000" y="${HZ - 2}" width="8000" height="${f1(YR - HZ + 4)}" fill="url(#${id}-deepG)"/><g clip-path="url(#${id}-wclip)">${spark}</g>`;
    w += `<g id="${id}-brk">${[0, 1, 2].map((k) => `<path id="${id}-brk${k}" d="" stroke="#ffffff" stroke-width="${f1(7 - k * 1.5)}" fill="none" opacity="${f1(0.9 - k * 0.25)}" stroke-linecap="round"/>`).join("")}</g>`;
    w += `<path id="${id}-water" d="" fill="url(#${id}-lagG)"/><g clip-path="url(#${id}-wclip)"><g id="${id}-caus">${ca}</g><g id="${id}-glitter">${Array.from({ length: 26 }, (_, k) => `<circle id="${id}-gl${k}" r="9" fill="url(#isGlint)" opacity="0"/>`).join("")}</g></g>`;
    w += `<path id="${id}-shal" d="" fill="${P.sea[5]}" opacity=".35"/><path id="${id}-foam2" d="" stroke="#ffffff" fill="none" opacity=".45" stroke-linecap="round"/><path id="${id}-foam" d="" stroke="#ffffff" fill="none" opacity=".92" stroke-linecap="round"/><path id="${id}-swash" d="" fill="#ffffff" opacity=".18"/></g>`;
    w += `<rect x="-3000" y="${HZ - 24}" width="8000" height="30" fill="${P.haze}" opacity="${night ? 0.15 : 0.4}"/>`;
    w += hl(-300, -1) + hl(1380, 1);
    put(L.set, w);
    // things on the sand: the foam box, the fire, the poncho
    let on = "";
    if (o.box) on += foamBox(id, 760, 1500, 0.9, r, { open: false, side: true });
    if (o.poncho) on += poncho(id, 790, 1600, 1);
    if (o.fire) { const [fx, fy] = o.fireAt || [330, 1660]; on += Isl.fire(`${id}-fire`, fx, fy, 1); }
    put(L.set, on);
    // glow: the far lamp with its reflection, the fire's light on the sand, the bioluminescence
    let gl = "";
    if (o.light) gl += `<g id="${id}-farlight" opacity="0"><circle cx="${o.lightX ?? 640}" cy="${f1(HZ - 14)}" r="70" fill="url(#isLamp)"/><circle cx="${o.lightX ?? 640}" cy="${f1(HZ - 14)}" r="5" fill="#fff6d8"/><g id="${id}-farref" opacity=".5"><path d="M${(o.lightX ?? 640) - 3},${HZ}L${(o.lightX ?? 640) + 3},${HZ}L${(o.lightX ?? 640) + 12},${HZ + 190}L${(o.lightX ?? 640) - 12},${HZ + 190}Z" fill="#ffd27a" opacity=".22"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${f1((o.lightX ?? 640) - 6 - k * 2.2)},${f1(HZ + 8 + k * 20 + (k % 2) * 7)}h${f1(12 + k * 4.4)}" stroke="#ffe3a0" stroke-width="${f1(2 + k * 0.3)}" stroke-linecap="round" opacity="${f1(0.8 - k * 0.07)}"/>`).join("")}</g></g>`;
    if (o.fire) { const [fx, fy] = o.fireAt || [330, 1660]; gl += `<ellipse id="${id}-firepool" cx="${fx}" cy="${fy + 10}" rx="360" ry="130" fill="url(#isFirePool)" opacity=".8"/>`; }
    if (o.glow) gl += `<g id="${id}-glow"><path id="${id}-glowB" d="" fill="#3ee8ff" opacity=".28"/><path id="${id}-glowL" d="" stroke="#9ffcff" stroke-width="14" fill="none" opacity=".75" stroke-linecap="round"/>${Array.from({ length: 18 }, (_, k) => `<circle id="${id}-gb${k}" r="30" fill="url(#isGlowC)" opacity="0"/>`).join("")}</g>`;
    gl += rainSVG(id, r);
    put(L.glow, gl);
    // foreground: a frond at each top corner, beach morning glory creeping in at the bottom
    let fg = "";
    if (o.palms !== false) { fg += `<g transform="translate(-120,-60) rotate(24)">${Tide.coco(0, 0, 1.3, 0, (o.seed || 7) + 77, { trunk: false, pal: [T(P.leaf[0], -0.3), T(P.leaf[1], -0.25), P.leaf[1]], id: `${id}-palm0` })}</g>`; fg += `<g transform="translate(1210,-30) rotate(-26) scale(-1,1)">${Tide.coco(0, 0, 1.15, 0, (o.seed || 7) + 78, { trunk: false, pal: [T(P.leaf[0], -0.3), T(P.leaf[1], -0.25), P.leaf[1]], id: `${id}-palm1` })}</g>`; }
    const vine = (x0, y0, dir, seed) => { const rr = mk(seed); let v = `<path d="M${x0},${y0}q${dir * 160},-60 ${dir * 340},-30t${dir * 300},10" stroke="#4a7a3a" stroke-width="7" fill="none"/>`; for (let k = 0; k < 8; k++) { const u = k / 7, vx = x0 + dir * (40 + u * 600), vy = y0 - 40 + Math.sin(u * 4) * 20; v += `<path d="M${f1(vx)},${f1(vy)}c-26,-28 -26,-58 0,-66c26,8 26,38 0,66z" fill="${rr() < 0.5 ? "#4f8a3e" : "#6aa84a"}" stroke="#2e5a2a" stroke-width="2"/>`; if (k % 3 === 1) v += `<g transform="translate(${f1(vx + dir * 20)},${f1(vy - 70)})"><path d="M0,0L-16,-34Q0,-44 16,-34Z" fill="#d86ab0" stroke="#8a2a6a" stroke-width="2"/><ellipse cx="0" cy="-36" rx="18" ry="6" fill="#f4a0d8" stroke="#8a2a6a" stroke-width="2"/></g>`; } return v; };
    fg += vine(-120, 1930, 1, 3) + vine(1220, 1950, -1, 4);
    put(L.fg, fg);
    ST[id] = { kind: "sea", P, HZ, yAt, FY, SH, night, light: !!o.light, glow: !!o.glow, fire: !!o.fire, rain: o.rain || null, ph: Array.from({ length: 40 }, () => [r(), r(), r()]) };
    seaDrawI(id, 0);
  }
  Isl.seaY = (id, d) => ST[id].yAt(d);
  Isl.seaS = (d) => 6.4 / d;
  function seaDrawI(id, t, o = {}) {
    const S = ST[id], { HZ, yAt, SH } = S, YR = yAt(SEA.DR);
    const dE = SH + 0.55 * Math.sin(t * 1.4) + 0.2 * Math.sin(t * 3.1);
    const edge = (x, dd) => yAt(dd + 0.26 * Math.sin(x * 0.0045 + t * 1.1) * (dd / 10) + 0.14 * Math.sin(x * 0.013 - t * 1.7) * (dd / 10));
    const line = (dd, rev) => { const pts = []; for (let x = -1300; x <= 2400; x += 40) pts.push(`${x},${f1(edge(x, dd))}`); if (rev) pts.reverse(); return pts; };
    const E = line(dE, true), top = `M-1300,${f1(YR - 2)}L2400,${f1(YR - 2)}`;
    const water = `${top}L${E.join("L")}Z`;
    el(`${id}-water`).setAttribute("d", water); el(`${id}-wclipP`).setAttribute("d", `M-1300,${HZ - 2}L2400,${HZ - 2}L${E.join("L")}Z`);
    el(`${id}-shal`).setAttribute("d", `M${line(dE * 1.25, false).join("L")}L${E.join("L")}Z`);
    const fw = clamp(5200 * (S.FY / 7200) / (dE * dE), 1.4, 10), foam = el(`${id}-foam`), foam2 = el(`${id}-foam2`);
    foam.setAttribute("d", `M${line(dE, false).join("L")}`); foam.setAttribute("stroke-width", f1(fw));
    foam2.setAttribute("d", `M${line(dE * 1.08, false).join("L")}`); foam2.setAttribute("stroke-width", f1(fw * 0.6));
    el(`${id}-swash`).setAttribute("d", `M${line(dE, false).join("L")}L${line(Math.max(SH * 0.86, dE * 0.82), true).join("L")}Z`);
    // the breakers on the reef: three white lines that run in and fade
    for (let k = 0; k < 3; k++) { const q = ((t * 0.22 + k * 0.33) % 1), dd = SEA.DR + 3 - q * 4, pts = []; for (let x = -1300; x <= 2400; x += 60) { const amp = Math.max(0, Math.sin(x * 0.0021 + k * 2.1 + t * 0.3)); pts.push(`${x},${f1(yAt(dd) + 2 * Math.sin(x * 0.02 + t))}`); } const e = el(`${id}-brk${k}`); e.setAttribute("d", `M${pts.join("L")}`); e.setAttribute("opacity", f1((0.85 - k * 0.2) * Math.sin(Math.PI * q) * (S.night ? 0.5 : 1))); e.setAttribute("stroke-dasharray", `${f1(120 + k * 40)} ${f1(60 + k * 30)}`); e.setAttribute("stroke-dashoffset", f1(-t * 30 - k * 50)); }
    el(`${id}-caus`).setAttribute("transform", `translate(${f1(Math.sin(t * 0.8) * 18)},${f1(Math.cos(t * 0.6) * 5)})`);
    for (let k = 0; k < 26; k++) { const [a, b, c] = S.ph[k], d = SH + 1 + a * (SEA.DR - SH - 2), g = el(`${id}-gl${k}`); g.setAttribute("cx", f1(-300 + b * 1700)); g.setAttribute("cy", f1(yAt(d))); g.setAttribute("r", f1(clamp(120 / d, 4, 14))); g.setAttribute("opacity", f1(Math.max(0, Math.sin(t * (3 + c * 4) + k * 1.7)) * (S.night ? 0.25 : 0.85))); }
    const birds = el(`${id}-birds`); if (birds) birds.setAttribute("transform", `translate(${f1(t * 26)},${f1(Math.sin(t * 0.7) * 6)})`);
    [0, 1].forEach((k) => { const p = el(`${id}-palm${k}`); if (p) { const [px, py] = p.getAttribute("data-o").split(" "); p.setAttribute("transform", `rotate(${f1(1.8 * Math.sin(t * 1.1 + k * 2))} ${px} ${py})`); } });
    if (S.light) { const g = el(`${id}-farlight`); g.setAttribute("opacity", f1((o.lightK ?? 1) * (0.55 + 0.45 * Math.max(0, Math.sin(t * 0.9)) ))); el(`${id}-farref`).setAttribute("opacity", f1(0.42 + 0.18 * Math.sin(t * 2.2))); }
    if (S.fire) { fireDraw(`${id}-fire`, t, o.fireK ?? 1); const fp = el(`${id}-firepool`); if (fp) fp.setAttribute("opacity", f1(0.7 + 0.14 * Math.sin(t * 9) + 0.08 * Math.sin(t * 23))); }
    if (S.glow) {
      const k = o.glowK ?? 1, Lw = line(dE, false), Lb = line(dE * 1.15, true);
      el(`${id}-glowB`).setAttribute("d", `M${Lw.join("L")}L${Lb.join("L")}Z`); el(`${id}-glowB`).setAttribute("opacity", f1(0.3 * k * (0.7 + 0.3 * Math.sin(t * 1.4))));
      el(`${id}-glowL`).setAttribute("d", `M${Lw.join("L")}`); el(`${id}-glowL`).setAttribute("opacity", f1(0.8 * k));
      for (let i = 0; i < 18; i++) { const [a, b, c] = S.ph[i + 20], d = SH + 0.5 + a * 10, e = el(`${id}-gb${i}`); e.setAttribute("cx", f1(-200 + b * 1500 + 30 * Math.sin(t + i))); e.setAttribute("cy", f1(yAt(d))); e.setAttribute("r", f1(20 + 40 * c)); e.setAttribute("opacity", f1(k * Math.max(0, Math.sin(t * (1 + c * 2) + i * 2.3)) * 0.8)); }
    }
    if (o.rainK !== undefined) rainDraw(id, t, o.rainK);
  }

  // ======================== the land view: from the water's edge looking inland ========================
  const LAND = { spots: { fa: [430, 1880, 0.95], phum: [700, 1910, 0.72], shade: [330, 1800, 0.95], stake: [880, 1700, 0.8], box: [760, 1560, 0.9] } };
  Isl.LAND = LAND;
  function landView(L, o) {
    const id = o.id || "il", P = PAL[o.time || "noon"], r = mk(o.seed || 9), night = P.stars === 1, camp = o.camp !== false;
    sky(L, id, P, 1150, { seed: (o.seed || 9) + 1, sunX: 1250, sunY: 160, sunR: 700 });
    // far: the jungle ridge rising to the islet's bare top, the three old fire rings on it
    let f = `<path d="M-1300,1300L-900,900C-600,760 -300,700 0,620C240,560 420,470 560,430C700,390 900,470 1080,560C1300,660 1700,860 2400,1300Z" fill="${T(P.green[0], -0.15)}"/>`;
    for (let k = 0; k < 90; k++) { const u = r(), x = -1200 + u * 3400, base = 1300 - 700 * Math.pow(Math.sin(Math.PI * clamp((x + 600) / 2200, 0, 1)), 0.8), y = base + r() * 420, R = 60 + r() * 120; f += crown(x, y, R, r, [T(P.green[0], -0.1), P.green[1], P.green[2], T(P.green[2], 0.2)], 8); }
    f += `<g id="${id}-top">${Isl.rock(640, 470, 300, 110, r, P, { id: `${id}-topr` })}${Isl.rock(760, 500, 180, 80, r, P, { id: `${id}-topr2` })}`;
    if (camp) [[560, 404], [650, 392], [740, 410]].forEach(([cx, cy], k) => { f += `<g id="${id}-ring${k}">${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => { const a = (i / 8) * Math.PI * 2; return `<ellipse cx="${f1(cx + Math.cos(a) * 22)}" cy="${f1(cy + Math.sin(a) * 9)}" rx="4.5" ry="3" fill="#6a6a62" stroke="#2e2a26" stroke-width="1"/>`; }).join("")}<ellipse cx="${cx}" cy="${cy}" rx="14" ry="5" fill="#1a1612" opacity=".8"/></g>`; });
    f += `</g>`;
    put(L.far, f);
    // mid: the beach curving away to the left with a row of smaller palms along it
    let m = `<path d="M-1300,1420Q-700,1250 -100,1300L-100,1500L-1300,1600Z" fill="${P.sand[1]}"/>`;
    for (let k = 0; k < 5; k++) m += Tide.coco(-1000 + k * 210 + r() * 60, 1290 + r() * 40, 0.75 + r() * 0.2, (r() - 0.5) * 0.3, (o.seed || 9) + 30 + k, { q: 0.5, pal: P.leaf });
    put(L.mid, m);
    // set: the dune and the beach down to the swash, the grove, the old camp's things, the rock shelter
    let s = `<defs><linearGradient id="${id}-sandG" gradientUnits="userSpaceOnUse" x1="0" y1="1120" x2="0" y2="1900"><stop offset="0" stop-color="${P.sand[1]}"/><stop offset=".5" stop-color="${P.sand[0]}"/><stop offset=".88" stop-color="${P.sand[2]}"/><stop offset="1" stop-color="${P.wet[0]}"/></linearGradient>
      <radialGradient id="${id}-shadeG"><stop offset="0" stop-color="#2a3020" stop-opacity=".5"/><stop offset="1" stop-color="#2a3020" stop-opacity="0"/></radialGradient></defs>`;
    s += `<path d="M-3000,1180Q-800,1120 100,1150Q700,1180 1400,1120Q2200,1080 4000,1160V2400H-3000Z" fill="url(#${id}-sandG)"/>`;
    for (let k = 0; k < 40; k++) s += grassTuft(r, -400 + r() * 1900, 1150 + Math.sin(r() * 6) * 20, 30 + r() * 40, k % 3 ? "#7a9a4a" : "#a8b860");
    s += `<ellipse id="${id}-shade" cx="330" cy="1760" rx="330" ry="110" fill="url(#${id}-shadeG)"/>`;
    s += beachBits(r, P, 1260, 1820, { prints: o.mud !== false, px: 470 });
    // the grove: four palms with their trunks in the sand, green nuts fallen under the big one
    const PM = [[110, 1380, 0.98, 0.07], [560, 1300, 1.12, -0.1], [930, 1360, 0.9, 0.11], [1260, 1290, 1.05, -0.05]];
    PM.forEach(([x, y, sc, ln], k) => { s += Tide.coco(x, y, sc, ln, (o.seed || 9) + 40 + k, { pal: P.leaf, id: `${id}-palm${k}`, fl: 0.7 }); });
    [[590, 1560, 0.95, -10], [660, 1600, 1.05, 20], [720, 1545, 0.9, 140], [630, 1640, 1.0, 70]].forEach(([x, y, sc, rot], k) => { s += `<g id="${id}-coco${k}" transform="translate(${x},${y}) rotate(${rot})">${Isl.cocoNut(0, 0, sc)}</g>`; });
    if (camp) s += Isl.stake(LAND.spots.stake[0], LAND.spots.stake[1], 1, { id: `${id}-stake` });
    // the rock shelter on the right: boulders, an overhang with a dark mouth, the bamboo rattle on a crossbar
    s += Isl.rock(1060, 1430, 480, 280, r, P, { id: `${id}-shr0` }) + Isl.rock(850, 1390, 260, 160, r, P, { id: `${id}-shr1` });
    s += `<g id="${id}-shelter"><path d="M880,1180C930,1100 1070,1080 1170,1120C1230,1150 1250,1230 1210,1300L910,1310C870,1270 860,1220 880,1180Z" fill="url(#isRockG)" ${OUT3}/><path d="M930,1220Q1030,1180 1160,1210L1170,1300L920,1306Z" fill="#141210"/><path d="M900,1160Q1010,1100 1160,1140" stroke="#ffffff" stroke-width="6" fill="none" opacity=".25" stroke-linecap="round"/>`;
    if (camp) s += `<g id="${id}-rattle"><path d="M956,1310V1210M1040,1310V1206" stroke="#8a6a3a" stroke-width="6"/><path d="M950,1216H1048" stroke="#a07a40" stroke-width="5"/>${[970, 990, 1010, 1030].map((x, i) => `<path d="M${x},1220v${28 + (i % 2) * 14}" stroke="#4a3a24" stroke-width="2"/><rect x="${x - 5}" y="${1246 + (i % 2) * 14}" width="10" height="40" rx="4" fill="#c8b070" ${OUT2}/>`).join("")}</g>`;
    s += `</g>`;
    if (o.box) s += foamBox(id, LAND.spots.box[0], LAND.spots.box[1], 0.9, r, { open: false, side: true });
    if (o.fire) { const [fx, fy] = o.fireAt || [330, 1700]; s += Isl.fire(`${id}-fire`, fx, fy, 1); }
    if (o.poncho) s += poncho(id, 880, 1560, 1);
    // the swash at the bottom (redrawn)
    s += `<path id="${id}-swashW" d="" fill="${P.sea[4]}" opacity=".78"/><path id="${id}-swash" d="" stroke="#fff" stroke-width="13" fill="none" stroke-linecap="round" opacity=".95"/><path id="${id}-swash2" d="" stroke="#fff" stroke-width="5" fill="none" opacity=".55"/>`;
    put(L.set, s);
    let gl = "";
    if (o.fire) { const [fx, fy] = o.fireAt || [330, 1700]; gl += `<ellipse id="${id}-firepool" cx="${fx}" cy="${fy + 10}" rx="360" ry="130" fill="url(#isFirePool)" opacity=".8"/>`; }
    gl += rainSVG(id, r);
    put(L.glow, gl);
    put(L.fg, `<g transform="translate(1180,-80) rotate(-30)">${Tide.coco(0, 0, 1.3, 0, (o.seed || 9) + 91, { trunk: false, pal: [T(P.leaf[0], -0.3), T(P.leaf[1], -0.2), P.leaf[1]] })}</g>`);
    ST[id] = { kind: "land", P, swashY: 1868, night, fire: !!o.fire, rain: o.rain || null };
    landDrawI(id, 0);
  }
  function landDrawI(id, t, o = {}) {
    const S = ST[id];
    const w = el(`${id}-swash`);
    if (w) { const yb = S.swashY + 30 * Math.sin(t * 1.4), pts = []; for (let x = -1300; x <= 2400; x += 40) pts.push(`${x},${f1(yb + 12 * Math.sin(x * 0.006 + t * 1.2) + 6 * Math.sin(x * 0.021 - t * 2))}`); w.setAttribute("d", `M${pts.join("L")}`); el(`${id}-swash2`).setAttribute("d", `M${pts.map((p) => { const [x, y] = p.split(","); return `${x},${f1(+y + 26)}`; }).join("L")}`); el(`${id}-swashW`).setAttribute("d", `M${pts.join("L")}L2400,2400L-1300,2400Z`); }
    [0, 1, 2, 3].forEach((k) => { const p = el(`${id}-palm${k}`); if (p) { const [px, py] = p.getAttribute("data-o").split(" "); p.setAttribute("transform", `rotate(${f1(1.6 * Math.sin(t * 1.1 + k * 1.7) * (1 + 2 * (o.rainK || 0)))} ${px} ${py})`); } });
    const rt = el(`${id}-rattle`); if (rt) rt.setAttribute("transform", `rotate(${f1(2.5 * Math.sin(t * 2.3) + 1.5 * Math.sin(t * 5.1))} 998 1216)`);
    if (S.fire) { fireDraw(`${id}-fire`, t, o.fireK ?? 1); const fp = el(`${id}-firepool`); if (fp) fp.setAttribute("opacity", f1(0.7 + 0.14 * Math.sin(t * 9) + 0.08 * Math.sin(t * 23))); }
    if (o.rainK !== undefined) rainDraw(id, t, o.rainK);
  }
  // run either view: o.rain [a, b] seconds into the call when the rain starts / is full, o.rainOut when it stops, o.lightAt when the far
  // lamp appears, o.glowK the bioluminescence strength, o.fireK the fire's size
  Isl.beach = (tl, id, t0, dur, o = {}) => {
    const S = ST[id], c = { t: 0 }, rain = o.rain || S.rain;
    const draw = (tt) => {
      const t = t0 + tt, rk = rain ? sm(rain[0], rain[1], tt) * (o.rainOut !== undefined ? 1 - sm(o.rainOut, o.rainOut + 1.5, tt) : 1) : 0;
      const q = { rainK: rk, fireK: o.fireK, glowK: o.glowK ?? 1, lightK: o.lightAt !== undefined ? sm(o.lightAt, o.lightAt + 1.2, tt) : 1 };
      if (S.kind === "sea") seaDrawI(id, t, q); else landDrawI(id, t, q);
    };
    draw(0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => draw(c.t) }, t0);
  };
  function islBeach(L, o = {}) { return (o.view || "sea") === "land" ? landView(L, o) : seaView(L, o); }
  function islNight(L, o = {}) { return islBeach(L, { time: "night", light: true, fire: true, poncho: true, ...o }); }

  // ---------------- things that stand on the sand ----------------
  // the boat's foam box washed up: white polystyrene with a blue strap, the lid ajar (o.open) showing the vinegar bottle, rope, cups
  function foamBox(id, x, y, s, r, o = {}) {
    let g = CS(0, 8, 150, 26, 0.85);
    g += `<path d="M-120,0L-112,-96L112,-96L120,0Z" fill="#f4f6f4" ${OUT3}/><path d="M112,-96L120,0L150,-18L142,-108Z" fill="#dfe6e8" ${OUT3}/>`;
    for (let k = 0; k < 40; k++) g += `<circle cx="${f1(-100 + r() * 200)}" cy="${f1(-90 + r() * 84)}" r="${f1(2 + r() * 3)}" fill="#e2e8e8" opacity=".7"/>`;
    g += `<path d="M-40,-96V0M40,-96V0" stroke="#2a8ad0" stroke-width="7" opacity=".9"/><path d="M-100,-60H100" stroke="#c8d0d2" stroke-width="2"/>`;
    g += `<g id="${id}-lid" transform="rotate(${o.open ? -58 : -8} -112 -96)"><path d="M-116,-96L-104,-122L120,-122L132,-96Z" fill="#ffffff" ${OUT3}/><path d="M-104,-122L120,-122L124,-128L-100,-128Z" fill="#dfe6e8" ${OUT2}/></g>`;
    g += `<text x="0" y="-24" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#2a6ab8" opacity=".85">เจี๊ยบทัวร์</text>`;
    return `<g id="${id}-box" transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})">${g}</g>`;
  }
  // ฟ้า's orange poncho rigged on two sticks as a rain catch (sags in the middle), a cup under its lowest point
  function poncho(id, x, y, s) {
    return `<g id="${id}-poncho" transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})">${CS(0, 6, 150, 20, 0.7)}<path d="M-150,0L-142,-210M150,0L142,-206" stroke="#7a5a32" stroke-width="7" stroke-linecap="round"/>
      <path d="M-146,-200Q0,-120 142,-196L146,-150Q0,-70 150,-146Z" fill="url(#isPoncho)" ${OUT3}/><path d="M-146,-200Q0,-120 142,-196" stroke="#ffd0a0" stroke-width="4" fill="none" opacity=".6"/>
      <path d="M-60,-150Q0,-96 60,-152" stroke="#c85a20" stroke-width="3" fill="none" opacity=".5"/><path d="M-6,-90q6,10 12,0" stroke="#bfefff" stroke-width="4" fill="none" opacity=".9"/>
      <g transform="translate(0,0)"><path d="M-26,-70L-22,0H22L26,-70Z" fill="#dff2f6" stroke="#5a7a84" stroke-width="2" opacity=".9"/><path d="M-20,-30L-18,0H18L20,-30Z" fill="#9fd4dc" opacity=".8"/></g></g>`;
  }

  // ======================== the opener / hook: straight down into the shallows, a girl's hand scooping water ========================
  function islHand(L, o) {
    const id = o.id || "ih", r = mk(o.seed || 23), title = o.title ?? "ติดเกาะ", sub = o.sub ?? "EP.1";
    put(L.sky, `<rect x="-600" y="-600" width="2300" height="3200" fill="#c9ad84"/>`);
    let s = `<defs><radialGradient id="${id}-sandG" gradientUnits="userSpaceOnUse" cx="500" cy="900" r="1500"><stop offset="0" stop-color="#e8cfa2"/><stop offset=".55" stop-color="#cfae7a"/><stop offset="1" stop-color="#9c7c4e"/></radialGradient>
      <linearGradient id="${id}-wG" gradientUnits="userSpaceOnUse" x1="0" y1="-300" x2="0" y2="2200"><stop offset="0" stop-color="#1e8fb0" stop-opacity=".78"/><stop offset=".5" stop-color="#45c6c2" stop-opacity=".55"/><stop offset="1" stop-color="#8fe0d8" stop-opacity=".42"/></linearGradient>
      <clipPath id="${id}-wclip"><path id="${id}-wclipP" d=""/></clipPath><clipPath id="${id}-palmC"><path id="${id}-palmCP" d=""/></clipPath></defs>`;
    s += `<rect x="-600" y="-600" width="2300" height="3200" fill="url(#${id}-sandG)"/>`;
    for (let k = 0; k < 40; k++) { const y0 = -300 + k * 60, ph = r() * 6; let p = ""; for (let x = -400; x <= 1500; x += 40) p += `${p ? "L" : "M"}${x},${f1(y0 + x * 0.1 + Math.sin(x * 0.009 + ph) * 16)}`; s += `<path d="${p}" stroke="#9a7e54" stroke-width="7" fill="none" opacity=".3"/><path d="${p}" stroke="#f2e4c4" stroke-width="4" fill="none" opacity=".45" transform="translate(-3,-6)"/>`; }
    for (let k = 0; k < 240; k++) s += `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(-200 + r() * 2400)}" r="${f1(0.8 + r() * 1.8)}" fill="${r() < 0.5 ? "#fff8e8" : "#7a6444"}" opacity="${f1(0.3 + r() * 0.5)}"/>`;
    for (let k = 0; k < 14; k++) s += coralHead(r, -100 + r() * 1300, -100 + r() * 1100, 30 + r() * 50);
    for (let k = 0; k < 12; k++) { const x = -40 + r() * 1160, y = -100 + r() * 1300, R = 8 + r() * 16; s += `<ellipse cx="${f1(x + 4)}" cy="${f1(y + 5)}" rx="${f1(R)}" ry="${f1(R * 0.75)}" fill="#000" opacity=".2"/><ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(R)}" ry="${f1(R * 0.75)}" fill="${["#6a6058", "#8a7e70", "#d8d0c4", "#4a4038"][k % 4]}" ${OUT2}/><ellipse cx="${f1(x - R * 0.3)}" cy="${f1(y - R * 0.3)}" rx="${f1(R * 0.35)}" ry="${f1(R * 0.22)}" fill="#fff" opacity=".4"/>`; }
    [[160, 1380, 34, -20, "#f6e4d8"], [920, 1270, 26, 30, "#f8d8c8"], [120, 1600, 24, 10, "#f2dcc8"], [760, 1860, 36, 64, "#f8eadc"]].forEach(([x, y, sz, rot, c]) => { s += `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M${f1(-sz + 5)},5a${f1(sz)},${f1(sz * 0.8)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="#000" opacity=".2"/><path d="M${f1(-sz)},0a${f1(sz)},${f1(sz * 0.8)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="${c}" ${OUT2}/>${Array.from({ length: 6 }, (_, i) => `<path d="M0,${f1(sz * 0.5)}L${f1(-sz + i * sz * 0.4)},${f1(-sz * 0.3 - Math.sin(i / 5 * Math.PI) * sz * 0.4)}" stroke="#8a6a5a" stroke-width="1.5" opacity=".6"/>`).join("")}</g>`; });
    // the title scratched into the wet sand with a stick: a thin dark groove, a lit lip below-right, sand crumbs along it
    const TX = o.at ? o.at[0] : 500, TY = o.at ? o.at[1] : 1600, FS = o.fs || 230, rot = -4;
    const tx = (txt, fill, dx, dy, fs, extra = "") => `<text x="${TX + dx}" y="${TY + dy}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${fs}" fill="${fill}" ${extra}>${txt}</text>`;
    s += `<defs><clipPath id="${id}-tclip"><text x="${TX}" y="${TY}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${FS}">${title}</text></clipPath></defs>`;
    s += `<g transform="rotate(${rot} ${TX} ${TY})">${tx(title, "#fbf0d6", 7, 8, FS)}${tx(title, "#f2dfb8", 3, 3, FS)}<g clip-path="url(#${id}-tclip)">${tx(title, "#4a3620", 0, 0, FS)}${tx(title, "#8a6a44", 9, 11, FS)}<path d="M${TX - 520},${TY - 40}L${TX + 520},${TY - 110}" stroke="#e8f2f4" stroke-width="10" opacity=".25"/></g>
      ${tx(sub, "#fbf0d6", 4, 150, 72)}${tx(sub, "#5a4228", 0, 146, 72)}</g>`;
    s += `<g transform="translate(900,1770) rotate(32)">${CS(8, 10, 120, 10, 0.8)}<path d="M-130,-6Q0,-16 130,-4L132,8Q0,0 -128,8Z" fill="#9a8466" ${OUT2}/><path d="M-110,-4Q0,-12 110,-2" stroke="#d8c8a8" stroke-width="3" fill="none"/></g>`;
    put(L.set, s);
    // the water: a translucent sheet over the upper two thirds of the frame with caustics, a lacy edge, glints
    let w = `<path id="${id}-water" d="" fill="url(#${id}-wG)"/>`;
    let ca = "";
    for (let k = 0; k < 70; k++) { const x = -300 + r() * 1700, y = -300 + r() * 2000, rr = 30 + r() * 70; ca += `<path d="M${f1(x - rr)},${f1(y)}q${f1(rr * 0.5)},${f1(-rr * 0.4)} ${f1(rr)},0t${f1(rr)},0" stroke="#e8fbff" stroke-width="${f1(2 + r() * 3)}" fill="none" opacity="${f1(0.18 + r() * 0.25)}"/>`; }
    w += `<g clip-path="url(#${id}-wclip)"><g id="${id}-caus">${ca}</g><path d="M-400,300L1500,-100V100L-400,500Z" fill="#fff" opacity=".1"/></g>`;
    w += `<path id="${id}-foamB" d="" stroke="#ffffff" stroke-width="30" fill="none" opacity=".5" stroke-linecap="round"/><path id="${id}-foam" d="" stroke="#ffffff" stroke-width="11" fill="none" stroke-linecap="round"/>`;
    put(L.set, w);
    // ---- the hand: ฟ้า's right hand, palm up and cupped, seen from above and a little behind her wrist (an over-the-shoulder look
    // straight down into the shallows). The forearm comes in short and wide from the lower-right corner under the hem of her mint
    // T-shirt sleeve; the thumb lies along the right side of the cup; the four fingers stand along the far edge, curled back over
    // the water so their pads face the camera; the water sits in the hollow of the palm. Local coordinates: wrist (0,0), the hand
    // runs toward -y; the group is rotated so the arm points up-left. Everything moving is redrawn by scoopDraw.
    const sk = "#ebbd95", skD = "#c8906a", skL = "#f6d8bc", skM = "#d9a77e";
    const PALM = "M-122,14C-152,-66 -142,-170 -100,-232C-58,-284 62,-288 112,-242C152,-200 160,-88 132,14C104,54 -92,54 -122,14Z";
    const THUMB = "M128,-30C158,-70 186,-130 194,-196C200,-230 176,-246 156,-226C136,-198 110,-150 78,-104C70,-80 90,-60 128,-30Z";
    let h = `<g id="${id}-hshd" opacity=".22"><path id="${id}-hsa" d="" fill="#3a2410"/><ellipse id="${id}-hsp" rx="190" ry="120" fill="#3a2410"/></g>`;
    h += `<g id="${id}-rips">${Array.from({ length: 5 }, (_, k) => `<ellipse id="${id}-rip${k}" rx="10" ry="6" fill="none" stroke="#f4ffff" stroke-width="3" opacity="0"/>`).join("")}</g>`;
    h += `<g id="${id}-arm"><path id="${id}-fa" d="" fill="${sk}" ${OUT3}/><path id="${id}-fas" d="" fill="${skD}" opacity=".28"/><path id="${id}-slv" d="" fill="#a9e4d4" ${OUT3}/><path id="${id}-slvH" d="" stroke="#d6f6ee" stroke-width="12" fill="none" opacity=".7"/><path id="${id}-fawet" d="" fill="#2aa8b8" opacity=".45"/></g>`;
    h += `<g id="${id}-hand"><g id="${id}-hs">`;
    h += `<path d="${PALM}" fill="${sk}" ${OUT3}/>`;
    // the outer (little-finger) edge turns away: a darker band; the heel of the palm and its creases
    h += `<path d="M-122,14C-152,-66 -142,-170 -100,-232L-78,-226C-116,-168 -124,-70 -96,10Z" fill="${skD}" opacity=".35"/>`;
    h += `<path d="M-70,-40Q-20,-70 40,-50M-60,-10Q0,-30 70,-14" stroke="${skD}" stroke-width="3" fill="none" opacity=".45" stroke-linecap="round"/><path d="M-40,20Q10,38 90,10" stroke="${skL}" stroke-width="8" fill="none" opacity=".45" stroke-linecap="round"/>`;
    // the water in the hollow of the palm: a clear cyan pool with a darker rim, two highlights and a wobbling glint
    h += `<g id="${id}-poolG"><path id="${id}-pool" d="M-94,-112C-108,-184 -72,-248 -8,-256C62,-264 120,-220 114,-160C110,-118 80,-90 10,-86C-50,-82 -84,-90 -94,-112Z" fill="#79dcd6" opacity=".72"/><path d="M-94,-112C-108,-184 -72,-248 -8,-256C62,-264 120,-220 114,-160" stroke="#3aa8b0" stroke-width="3" fill="none" opacity=".5"/>
      <path d="M-62,-176Q-10,-214 60,-184" stroke="#fff" stroke-width="7" fill="none" opacity=".8" stroke-linecap="round"/><ellipse cx="40" cy="-140" rx="30" ry="12" fill="#fff" opacity=".4"/><path id="${id}-poolW" d="M-70,-120Q0,-100 90,-128" stroke="#bff6f4" stroke-width="4" fill="none" opacity=".8" stroke-linecap="round"/></g>`;
    // four fingers standing along the far edge, folded back over the pool: the proximal part turns away (mid tone, short), the folded
    // part comes back toward the camera showing the pad, a crease at the fold and at the tip joint
    const fing = (x, y, a, l1, l2, w, i) => `<g transform="translate(${x},${y}) rotate(${a})"><rect x="${-w / 2}" y="${-l1 - 4}" width="${w}" height="${l1 + 14}" rx="${w / 2}" fill="${skM}" ${OUT3}/>
      <rect x="${-w * 0.48}" y="${-l1 - 6}" width="${w * 0.96}" height="${l2 + l1 * 0.3}" rx="${w * 0.48}" fill="${sk}" ${OUT3}/>
      <path d="M${-w * 0.36},${-l1 + 2}q${w * 0.36},8 ${w * 0.72},0" stroke="${skD}" stroke-width="2.6" fill="none" opacity=".8"/><path d="M${-w * 0.3},${-l1 + l2 * 0.45}q${w * 0.3},6 ${w * 0.6},0" stroke="${skD}" stroke-width="2" fill="none" opacity=".55"/>
      <ellipse cx="0" cy="${-l1 + l2 * 0.8}" rx="${w * 0.26}" ry="${w * 0.17}" fill="${skL}" opacity=".55"/><path d="M${-w * 0.3},${-l1 - 2}q${w * 0.3},-6 ${w * 0.6},0" stroke="${skL}" stroke-width="2" fill="none" opacity=".5"/>
      <rect id="${id}-wetf${i}" x="${-w / 2 - 2}" y="${-l1 - 8}" width="${w + 4}" height="${l2 + l1 * 0.3 + 6}" rx="${w / 2}" fill="#2aa8b8" opacity=".5"/></g>`;
    h += `<g id="${id}-fng">${fing(-86, -230, -10, 50, 112, 52, 0)}${fing(-32, -254, -4, 56, 122, 54, 1)}${fing(22, -256, 2, 54, 118, 52, 2)}${fing(72, -238, 8, 44, 100, 46, 3)}</g>`;
    // the thumb along the right side, its nail toward the camera
    h += `<path d="${THUMB}" fill="${sk}" ${OUT3}/><path d="M118,-96Q146,-150 170,-200" stroke="${skD}" stroke-width="3" fill="none" opacity=".5"/><path d="M90,-96C104,-78 118,-60 134,-40" stroke="${sk}" stroke-width="7" fill="none"/><g transform="translate(174,-212) rotate(-38)"><rect x="-13" y="-9" width="26" height="18" rx="8" fill="#f3d2b8" stroke="${skD}" stroke-width="1.6"/></g><path d="M140,-130q8,-6 16,-2" stroke="${skL}" stroke-width="3" fill="none" opacity=".7"/>`;
    // the pink scrunchie on the wrist
    h += `<path d="M-126,34Q0,68 136,34" stroke="#ff8cbc" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M-110,36Q0,60 110,36" stroke="#ffb8d6" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/><path d="M-80,58q-8,10 -2,20M-70,60q6,12 0,22" stroke="#ff8cbc" stroke-width="7" fill="none" stroke-linecap="round"/>`;
    // under water the whole hand takes the water's tint (clipped to its silhouette)
    h += `<defs><clipPath id="${id}-hclip"><path d="${PALM}"/><path d="${THUMB}"/></clipPath></defs><rect id="${id}-wet" x="-320" y="-380" width="640" height="520" fill="#2aa8b8" opacity=".5" clip-path="url(#${id}-hclip)"/>`;
    h += `</g></g>`;
    // the water running out between the fingers: three streams, their drops, and the rings they make on the surface below
    h += `<g id="${id}-str">${Array.from({ length: 3 }, (_, k) => `<path id="${id}-st${k}" d="" fill="#d2f6ff" opacity=".9"/>`).join("")}</g>`;
    h += `<g id="${id}-drops">${Array.from({ length: 8 }, (_, k) => `<path id="${id}-drop${k}" d="M0,-14C-8,-2 -9,6 0,12C9,6 8,-2 0,-14Z" fill="#bfefff" stroke="#5aa8c0" stroke-width="1.5" opacity="0"/>`).join("")}</g>`;
    put(L.act, h);
    put(L.glow, `<g id="${id}-glints">${Array.from({ length: 14 }, (_, k) => `<circle id="${id}-g${k}" r="18" fill="url(#isGlint)" opacity="0"/>`).join("")}</g>`);
    ST[id] = { kind: "hand", ph: Array.from({ length: 40 }, () => [r(), r(), r()]), from: o.from || [600, 1200], to: o.to || [540, 1000], sh: o.shoulder || [1190, 1300], rot: o.rot ?? -40 };
    scoopDraw(id, 0, 0);
  }
  function scoopDraw(id, t, p) {
    const S = ST[id], k = gsap.parseEase("power2.inOut")(clamp(p, 0, 1));
    // the water sheet: covers the frame from the top down to a lacy edge that swings across the lower third
    const yE = 1240 + 40 * Math.sin(t * 0.9), edge = (x) => yE + 26 * Math.sin(x * 0.008 + t * 1.5) + 12 * Math.sin(x * 0.025 - t * 2.2);
    const E = []; for (let x = -400; x <= 1500; x += 30) E.push([x, edge(x)]);
    const wd = `M-400,-700H1500V${f1(edge(1500))}L${E.slice().reverse().map(P2).join("L")}Z`;
    el(`${id}-water`).setAttribute("d", wd); el(`${id}-wclipP`).setAttribute("d", wd);
    el(`${id}-foam`).setAttribute("d", `M${E.map(P2).join("L")}`); el(`${id}-foamB`).setAttribute("d", `M${E.map(([x, y]) => [x, y - 12]).map(P2).join("L")}`);
    el(`${id}-caus`).setAttribute("transform", `translate(${f1(Math.sin(t * 0.8) * 20)},${f1(Math.cos(t * 0.6) * 16)})`);
    for (let i = 0; i < 14; i++) { const [a, b] = S.ph[i], g = el(`${id}-g${i}`); g.setAttribute("cx", f1(-100 + a * 1300)); g.setAttribute("cy", f1(-100 + b * 1300)); g.setAttribute("opacity", f1(Math.max(0, Math.sin(t * 5 + i * 1.7)) * 0.7)); }
    // the hand: deep in the water and small at k 0, lifted toward the camera (bigger) at k 1; it hesitates with a small tremble at the end
    const tr = sm(0.78, 0.95, k) * (1 - sm(0.985, 1, k)), wob = tr * 4 * Math.sin(t * 14), wob2 = tr * 3 * Math.sin(t * 17 + 1);
    const W = [lerp(S.from[0], S.to[0], k) + wob, lerp(S.from[1], S.to[1], k) + wob2], sc = 0.88 + 0.34 * k, rot = S.rot + 6 * k + tr * 1.5 * Math.sin(t * 12);
    el(`${id}-hs`).setAttribute("transform", `translate(${f1(W[0])},${f1(W[1])}) rotate(${f1(rot)}) scale(${f1(sc)})`);
    const ca = Math.cos(rot * Math.PI / 180), sa = Math.sin(rot * Math.PI / 180), L2W = (x, y) => [W[0] + (x * ca - y * sa) * sc, W[1] + (x * sa + y * ca) * sc];
    // the forearm: short and wide from the lower-right corner to the wrist, the mint sleeve hem over its top third
    const A = S.sh, wr = L2W(0, 40), limb = (P0, P1, wa, wb) => { const dx = P1[0] - P0[0], dy = P1[1] - P0[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l; return `M${f1(P0[0] + nx * wa)},${f1(P0[1] + ny * wa)}L${f1(P1[0] + nx * wb)},${f1(P1[1] + ny * wb)}L${f1(P1[0] - nx * wb)},${f1(P1[1] - ny * wb)}L${f1(P0[0] - nx * wa)},${f1(P0[1] - ny * wa)}Z`; };
    const EL = [lerp(wr[0], A[0], 0.55), lerp(wr[1], A[1], 0.55)], E2 = [lerp(EL[0], wr[0], 0.12), lerp(EL[1], wr[1], 0.12)], A2 = [A[0] + (A[0] - wr[0]) * 0.3, A[1] + (A[1] - wr[1]) * 0.3];
    el(`${id}-fa`).setAttribute("d", limb(EL, wr, 150, 122 * sc)); el(`${id}-fas`).setAttribute("d", limb([EL[0] + 10, EL[1] + 60], [wr[0] + 30 * sc, wr[1] + 50 * sc], 40, 28 * sc));
    el(`${id}-fawet`).setAttribute("d", limb(wr, [lerp(wr[0], EL[0], 0.5), lerp(wr[1], EL[1], 0.5)], 126 * sc, 140));
    el(`${id}-slv`).setAttribute("d", limb(A2, E2, 236, 206));
    { const dx = E2[0] - A2[0], dy = E2[1] - A2[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l; el(`${id}-slvH`).setAttribute("d", `M${f1(E2[0] + nx * 196 - dx / l * 16)},${f1(E2[1] + ny * 196 - dy / l * 16)}Q${f1(E2[0] - dx / l * 2)},${f1(E2[1] - dy / l * 2)} ${f1(E2[0] - nx * 196 - dx / l * 16)},${f1(E2[1] - ny * 196 - dy / l * 16)}`); }
    // the shadow on the sand bed slides away and softens as the hand comes up
    el(`${id}-hsa`).setAttribute("d", limb([EL[0] + 40, EL[1] + 90], [wr[0] + 70 + 60 * k, wr[1] + 130 + 110 * k], 150, 120));
    const hp = el(`${id}-hsp`); hp.setAttribute("cx", f1(W[0] + 70 + 70 * k)); hp.setAttribute("cy", f1(W[1] + 40 + 130 * k)); hp.setAttribute("rx", f1(210 * sc)); hp.setAttribute("ry", f1(130 * sc)); hp.setAttribute("transform", `rotate(${f1(rot)} ${f1(W[0] + 70 + 70 * k)} ${f1(W[1] + 40 + 130 * k)})`);
    el(`${id}-hshd`).setAttribute("opacity", f1(0.26 - 0.12 * k));
    // under water the hand is tinted; the tint goes as it breaks the surface
    const wetO = 0.5 * (1 - sm(0.08, 0.4, k)); el(`${id}-wet`).setAttribute("opacity", f1(wetO)); for (let i = 0; i < 4; i++) el(`${id}-wetf${i}`).setAttribute("opacity", f1(wetO)); el(`${id}-fawet`).setAttribute("opacity", f1(wetO * 0.9));
    // the water in the palm drains away as it leaks; its surface wobbles
    const drain = sm(0.3, 1, k), pool = el(`${id}-poolG`); pool.setAttribute("opacity", f1(0.95 - 0.55 * drain)); pool.setAttribute("transform", `translate(${f1(-10 * drain)},${f1(-18 * drain)}) scale(${f1(1 - 0.38 * drain)})`);
    el(`${id}-poolW`).setAttribute("d", `M-70,-120Q0,${f1(-100 + 6 * Math.sin(t * 7))} 90,-128`);
    // the streams from the finger gaps: on while the hand lifts, thinning out at the end; each ends in drops, each drop a ring on the surface
    const flow = sm(0.12, 0.42, k) * (1 - sm(0.7, 0.98, k)), GAPS = [[-62, -236], [-4, -242], [52, -232]];
    GAPS.forEach(([gx, gy], i) => { const [x0, y0] = L2W(gx, gy), len = (110 + i * 30) * sc * flow, w0 = 7 * sc * flow, wg = 3 * Math.sin(t * 9 + i); el(`${id}-st${i}`).setAttribute("d", flow < 0.02 ? "" : `M${f1(x0 - w0)},${f1(y0)}Q${f1(x0 - w0 * 0.6 + wg)},${f1(y0 + len * 0.5)} ${f1(x0 + wg * 0.5)},${f1(y0 + len)}Q${f1(x0 + w0 * 0.6 + wg)},${f1(y0 + len * 0.5)} ${f1(x0 + w0)},${f1(y0)}Z`); });
    for (let i = 0; i < 8; i++) { const [a, b, c] = S.ph[i + 20], g = GAPS[i % 3], [x0, y0] = L2W(g[0], g[1]), life = (b + t * (0.8 + c * 0.6)) % 1, len = (110 + (i % 3) * 30) * sc * flow, e = el(`${id}-drop${i}`); e.setAttribute("transform", `translate(${f1(x0 + (a - 0.5) * 24 * sc)},${f1(y0 + len + life * 90 * sc)}) scale(${f1((0.6 + c * 0.6) * sc * (1 - 0.5 * life))})`); e.setAttribute("opacity", f1(flow * (1 - life) * (life > 0.05 ? 1 : 0))); }
    for (let i = 0; i < 5; i++) { const [a, b, c] = S.ph[i + 30], g = GAPS[i % 3], [x0, y0] = L2W(g[0], g[1]), life = (b + t * (0.6 + c * 0.5)) % 1, e = el(`${id}-rip${i}`); e.setAttribute("cx", f1(x0 + (a - 0.5) * 90 - 20 * sc)); e.setAttribute("cy", f1(y0 + (40 + (i % 3) * 36) * sc + 60 * sc)); e.setAttribute("rx", f1(14 + life * 110)); e.setAttribute("ry", f1((14 + life * 110) * 0.55)); e.setAttribute("opacity", f1(flow * (1 - life) * 0.8)); }
  }
  // lift the cupped hand from the water (o.from 0) up toward the lips (o.to 1) over the call; the drops fall harder as it tips
  Isl.scoop = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, u0 = o.from ?? 0, u1 = o.to ?? 1;
    scoopDraw(id, t0, u0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => scoopDraw(id, t0 + c.t, lerp(u0, u1, c.t / dur)) }, t0);
  };

  // ======================== the inserts ========================
  function islInsert(L, o = {}) {
    const id = o.id || "ii", r = mk(o.seed || 5), kind = o.kind || "box", P = PAL[o.time || "noon"];
    put(L.sky, `<rect x="-600" y="-600" width="2300" height="3200" fill="${P.sand[1]}"/>`);
    let s = `<defs><radialGradient id="${id}-sandG" gradientUnits="userSpaceOnUse" cx="540" cy="700" r="1500"><stop offset="0" stop-color="${P.sand[0]}"/><stop offset=".6" stop-color="${P.sand[1]}"/><stop offset="1" stop-color="${P.sand[2]}"/></radialGradient></defs><rect x="-600" y="-600" width="2300" height="3200" fill="url(#${id}-sandG)"/>`;
    for (let k = 0; k < 26; k++) { const y = -200 + k * 90 + r() * 40, ph = r() * 6; let p = ""; for (let x = -400; x <= 1500; x += 40) p += `${p ? "L" : "M"}${x},${f1(y + Math.sin(x * 0.008 + ph) * 12)}`; s += `<path d="${p}" stroke="${T(P.sand[2], -0.2)}" stroke-width="5" fill="none" opacity=".25"/><path d="${p}" stroke="#fff" stroke-width="3" fill="none" opacity=".35" transform="translate(-2,-5)"/>`; }
    for (let k = 0; k < 200; k++) s += `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(-200 + r() * 2400)}" r="${f1(0.8 + r() * 2)}" fill="${r() < 0.5 ? "#fff8e8" : "#8a7050"}" opacity="${f1(0.3 + r() * 0.5)}"/>`;
    for (let k = 0; k < 8; k++) { const x = -40 + r() * 1160, y = r() * 1920, sz = 10 + r() * 16; s += `<path d="M${f1(x - sz + 4)},${f1(5)}a0,0 0 0 0 0,0"/><path d="M${f1(x - sz)},${f1(y)}a${f1(sz)},${f1(sz * 0.7)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="${["#f8f2ea", "#f4d8cc", "#e8dcc0"][k % 3]}" stroke="#9a8a72" stroke-width="1.2"/>`; }
    if (kind === "box") {
      s += `<g transform="translate(540,1180) scale(2.6)">${foamBox(id, 0, 0, 1, r, { open: true })}</g>`;
      // inside, seen over the front wall: the vinegar bottle, the rope coil, the cups, a sponge
      let inn = `<g transform="translate(540,1180) scale(2.6)"><path d="M-112,-96L112,-96L108,-52L-108,-52Z" fill="#cfd8da"/><path d="M-108,-52H108" stroke="#aab4b6" stroke-width="2"/>`;
      inn += `<g transform="translate(-50,-56) rotate(-12)"><path d="M-22,0V-70Q-22,-84 -12,-86H12Q22,-84 22,-70V0Z" fill="url(#isVinegar)" ${OUT2}/><rect x="-10" y="-104" width="20" height="20" rx="3" fill="#d8302a" ${OUT2}/><rect x="-20" y="-60" width="40" height="34" fill="#f8f4ea" ${OUT2}/><text x="0" y="-46" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="9" fill="#2a2420">น้ำส้ม</text><text x="0" y="-35" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="9" fill="#2a2420">สายชู</text><path d="M-14,-80V-10" stroke="#fff" stroke-width="4" opacity=".6"/></g>`;
      inn += `<g transform="translate(40,-50)">${[0, 1, 2, 3].map((i) => `<ellipse rx="${40 - i * 5}" ry="${18 - i * 2}" cy="${-i * 5}" fill="none" stroke="#c8a860" stroke-width="7"/><ellipse rx="${40 - i * 5}" ry="${18 - i * 2}" cy="${-i * 5}" fill="none" stroke="#8a6a34" stroke-width="2.5" stroke-dasharray="4 3"/>`).join("")}<path d="M-30,-20q20,-14 46,-8" stroke="#e8c880" stroke-width="3" fill="none"/></g>`;
      inn += `<g transform="translate(86,-66)">${[0, 1, 2].map((i) => `<path d="M-14,${-i * 6}L-11,${-i * 6 - 30}H11L14,${-i * 6}Z" fill="#dff2f6" stroke="#5a7a84" stroke-width="1.5" opacity=".9"/>`).join("")}</g>`;
      inn += `<rect x="-96" y="-70" width="34" height="22" rx="4" fill="#f2c030" ${OUT2}/></g>`;
      s += inn;
      
    }
    if (kind === "bottle") {
      s += `<g transform="translate(540,1050) rotate(-18)"><g id="${id}-bot">${CS(10, 150, 300, 40, 0.8)}<path d="M-240,-70Q-250,-110 -210,-110H-120Q-100,-110 -100,-90V-70H180Q230,-70 236,-30V60Q230,100 180,100H-100V120Q-100,140 -120,140H-210Q-250,140 -240,100Z" fill="url(#isPET)" ${OUT3}/>
        <path id="${id}-water" d="M-236,60Q-230,100 -180,100H-20Q-60,80 -80,40Q-120,0 -236,20Z" fill="#7fd0e0" opacity=".75"/><path d="M-236,40Q-150,20 -60,50" stroke="#bfefff" stroke-width="4" fill="none" opacity=".8"/>
        <rect x="-60" y="-66" width="150" height="130" fill="#2a8ad0" opacity=".85" ${OUT2}/><path d="M-50,-30h130M-50,0h110M-50,30h90" stroke="#fff" stroke-width="7" opacity=".7"/><path d="M90,-66L60,-20L90,64" fill="#1a5a90" opacity=".8"/>
        <rect x="236" y="-40" width="40" height="80" rx="6" fill="#2a6ab8" ${OUT2}/><path d="M244,-30v60M256,-30v60M268,-30v60" stroke="#1a4a8a" stroke-width="2"/>
        <path d="M-200,-80Q0,-96 200,-80" stroke="#fff" stroke-width="8" fill="none" opacity=".6"/><path d="M-200,120Q0,130 190,112" stroke="#6a9aa8" stroke-width="4" fill="none" opacity=".4"/>${[-180, -140, 120, 160].map((x) => `<path d="M${x},-66V98" stroke="#8ab8c4" stroke-width="2.5" opacity=".5"/>`).join("")}<rect x="206" y="-50" width="30" height="100" rx="4" fill="#bfe0ea" ${OUT2}/></g></g>`;
      s += `<g id="${id}-shimmer">${Array.from({ length: 12 }, (_, k) => `<path id="${id}-sh${k}" d="M${f1(80 + k * 90)},700q10,-40 0,-80q-10,-40 0,-80" stroke="#fff" stroke-width="3" fill="none" opacity=".25"/>`).join("")}</g>`;
      for (let k = 0; k < 7; k++) s += `<ellipse cx="${f1(260 + k * 90 + r() * 30)}" cy="${f1(1300 + r() * 60)}" rx="4" ry="2.5" fill="#2a2420" opacity=".8"/>`;
    }
    if (kind === "coco") {
      // the stake driven into the sand at a slant, its tip through a big green coconut; the husk torn back in fibrous flaps, the shell's
      // white flesh showing at a hole at the top right; the water runs out of it into the plastic cup on the sand
      s += `<g transform="translate(100,1920) rotate(22) scale(3.2)">${CS(0, 4, 40, 10, 0.8)}<path d="M-16,0L-11,-200L0,-290L11,-200L16,0Z" fill="url(#isStake)" ${OUT3}/><path d="M-6,-20Q-4,-140 0,-280" stroke="#a07850" stroke-width="2.5" opacity=".6"/><path d="M-12,-150l24,-6M-13,-110l26,-5M-14,-70l28,-4" stroke="#2a1a10" stroke-width="2" opacity=".5"/></g>`;
      s += `<g transform="translate(470,1020) scale(3.4)"><g id="${id}-nut">${CS(10, 60, 60, 14, 0.6)}<path d="M-48,10C-54,-24 -34,-54 0,-56C34,-54 54,-24 48,10C42,36 22,52 0,52C-22,52 -42,36 -48,10Z" fill="url(#isCocoG)" ${OUT3}/>
        <path d="M-36,-20Q-24,-40 -4,-48" stroke="#dff2a0" stroke-width="6" fill="none" opacity=".7" stroke-linecap="round"/><path d="M-16,-36L10,40M12,-42L30,30" stroke="#5a8a2a" stroke-width="2" opacity=".5"/>
        <path d="M-6,-56L-14,-70q7,-5 12,0L2,-56" fill="#8a6a34" ${OUT2}/>
        <path d="M14,-44C30,-60 60,-52 62,-30C64,-14 52,-6 40,-8L30,-26Z" fill="#c8a860" ${OUT2}/><path d="M22,-40q14,-12 30,-2M24,-30q12,-8 26,-2M28,-20q10,-6 20,0" stroke="#a88040" stroke-width="2" fill="none"/>
        <path d="M-6,40C-10,52 -2,60 8,56C14,52 12,44 8,38Z" fill="#c8a860" ${OUT2} opacity=".9"/>
        <path d="M14,-44C18,-30 26,-18 36,-10C28,-4 18,-6 12,-12C8,-22 10,-34 14,-44Z" fill="#f6ecd0" ${OUT2}/><ellipse cx="22" cy="-26" rx="5" ry="3.5" fill="#4a3a28"/>
        <path d="M-30,-6L30,-54" stroke="#3a2a1a" stroke-width="0" /></g></g>`;
      s += `<path id="${id}-stream" d="" fill="#dff8ff" opacity=".92" stroke="#9fd4e0" stroke-width="2"/>`;
      s += `<g transform="translate(790,1560) scale(2.4)">${CS(0, 4, 40, 8, 0.8)}<path d="M-30,-80L-26,0H26L30,-80Z" fill="#dff2f6" stroke="#5a7a84" stroke-width="2" opacity=".92"/><path id="${id}-cup" d="M-26,0H26L28,-20H-28Z" fill="#9fd4dc" opacity=".85"/><path d="M-22,-70V-10" stroke="#fff" stroke-width="4" opacity=".6"/><path d="M-30,-80H30" stroke="#8aaab4" stroke-width="2"/></g>`;
    }
    put(L.set, s);
    put(L.glow, `<g id="${id}-glints">${Array.from({ length: 10 }, (_, k) => `<circle id="${id}-g${k}" r="14" fill="url(#isGlint)" opacity="0"/>`).join("")}</g>`);
    ST[id] = { kind: "insert", what: kind, ph: Array.from({ length: 30 }, () => [r(), r(), r()]) };
    insertDraw(id, 0, 0);
  }
  function insertDraw(id, t, p) {
    const S = ST[id];
    for (let i = 0; i < 10; i++) { const [a, b] = S.ph[i], g = el(`${id}-g${i}`); g.setAttribute("cx", f1(100 + a * 880)); g.setAttribute("cy", f1(700 + b * 900)); g.setAttribute("opacity", f1(Math.max(0, Math.sin(t * 4 + i * 1.9)) * 0.5)); }
    if (S.what === "bottle") { for (let k = 0; k < 12; k++) { const e = el(`${id}-sh${k}`); e.setAttribute("transform", `translate(0,${f1(-((t * 60 + k * 30) % 200))})`); e.setAttribute("opacity", f1(0.25 * Math.max(0, Math.sin(t * 2 + k)))); }
      const b = el(`${id}-bot`); b.setAttribute("transform", `rotate(${f1(-22 * p + 3 * Math.sin(t * 15) * p)} 180 0)`); el(`${id}-water`).setAttribute("transform", `translate(${f1(60 * p)},${f1(-10 * p)}) rotate(${f1(12 * p + 4 * Math.sin(t * 14) * p)} -120 60)`); }
    if (S.what === "coco") {
      const k = clamp(p, 0, 1), x0 = 546, y0 = 932, x1 = 790, y1 = 1400 - 60 * k, yy = lerp(y0, y1, sm(0, 0.2, k)), wig = 4 * Math.sin(t * 20);
      el(`${id}-stream`).setAttribute("d", k < 0.02 ? "" : `M${x0 - 7},${y0}Q${f1(x0 + (x1 - x0) * 0.55)},${f1(y0 + 60)} ${f1(x1 - 6 + wig)},${f1(yy)}L${f1(x1 + 6 + wig)},${f1(yy)}Q${f1(x0 + (x1 - x0) * 0.6)},${f1(y0 + 48)} ${x0 + 7},${y0}Z`);
      const lvl = -20 - 54 * k; el(`${id}-cup`).setAttribute("d", `M-26,0H26L${f1(26 + lvl * 0.07)},${f1(lvl)}H${f1(-26 - lvl * 0.07)}Z`);
      el(`${id}-nut`).setAttribute("transform", `rotate(${f1(-4 * sm(0, 0.15, k) + 1.2 * Math.sin(t * 12) * (k > 0.02 && k < 0.95 ? 1 : 0))} 0 0)`);
    }
  }
  Isl.shake = (tl, id, t0, dur, o = {}) => { const c = { t: 0 }, u0 = o.from ?? 0, u1 = o.to ?? 1; insertDraw(id, t0, u0); tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => insertDraw(id, t0 + c.t, lerp(u0, u1, Math.sin(Math.PI * Math.min(1, c.t / dur)))) }, t0); };
  Isl.pour = (tl, id, t0, dur, o = {}) => { const c = { t: 0 }, u0 = o.from ?? 0, u1 = o.to ?? 1; insertDraw(id, t0, u0); tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => insertDraw(id, t0 + c.t, lerp(u0, u1, c.t / dur)) }, t0); };
  Isl.insertIdle = (tl, id, t0, dur) => { const c = { t: 0 }; tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => insertDraw(id, t0 + c.t, 0) }, t0); };

  Object.assign(Sets, { islBeach, islNight, islHand, islInsert });
})();
