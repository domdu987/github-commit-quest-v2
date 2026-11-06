// "หนวดใส" sets, cast and props — a fictional beach village on the Gulf of Thailand (no karsts: a flat bright horizon, two low green
// islands, casuarinas and coconut palms), late-year holiday morning. Built on tide.js's beach (Sets.tideBeach, same layer contract,
// seeded RNG, gradients only) and tidecast.js's rigs. Load after tide.js, tidecast.js.
//
//   Sets.jellyBeach(L, o)  the Gulf beach from the sand looking out · o = tideBeach's sea view + o.isles (true) low islands instead of
//                          karsts · o.tower [x, y, s] the lifeguard tower · o.post [x, y, s, full] the vinegar post (full 0…1: bottles
//                          in its rack) · o.rock [x, y, s] "หินโน้น" out in the bay · o.jellies [[x, y, s, deep], …] box jellyfish in
//                          the shallows (deep 0…1 under the surface) · o.umbrellas [[x, y, s, colour], …] · o.ring [x, y, s] the duck
//                          ring floating empty
//   Sets.jellyPorch(L, o)  ยายลออ's wooden house at dawn: plank wall, door, window to the sea, the basket of vinegar bottles at the door,
//                          the sundial on the house post (o.dial), the shelf with the photo face down
//   Sets.jellyHook(L, o)   frame 0: the wet sand close, ภูมิ's calf with the clear tentacles wrapped round it and the red welts, the uncapped
//                          bottle over it in ต้น's hand, the title written in the wet sand (o.title, o.sub)
//   Jelly.box(x, y, s, o)  a box jellyfish (pale, nearly clear cube bell, four corners each trailing a bundle of long tentacles)
//   Jelly.bottle(x, y, s, o) a PET water bottle · o.cap false = uncapped · o.tilt degrees
//   Jelly.post(x, y, s, o) · Jelly.tower(x, y, s, o) · Jelly.basket(x, y, s, o)
//   cast: jTon (ต้น 40) · jTonBottle · jTonPhone · jPhum (ภูมิ 11) · jWan (น้ำหวาน 7, duck ring) · jLaor (ยายลออ 70) · jLaorBasket ·
//         jGuard (ไลฟ์การ์ด) · jWoman (ผู้หญิงบนหาด)
(function () {
  const INK = "#2e2a26";
  const f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el && el.insertAdjacentHTML("beforeend", html);
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  let uid = 0; const nid = (p) => `${p}${++uid}`;
  const J = (window.Jelly = window.Jelly || {});

  // ------------------------------------------------------------------ props
  // box jellyfish: a rounded cube bell (nearly clear, a cool rim light, faint inner organs), four pedalia at the corners, each with a
  // bundle of long thin tentacles (beaded with stinging cells). (x, y) = the bell's lower rim; ~110 wide, tentacles ~ o.len (360)
  J.box = (x, y, s = 1, o = {}) => { const r = mk(o.seed || 7), g = nid("jb"), len = o.len ?? 360, sw = o.sway ?? 0, lit = o.lit ?? 1;
    // four corners: two front (±56, 4) and two back (±30, -14); each trails a bundle of o.per (5) tentacles beaded with stinging cells (o.per 1: the single-tentacle kind)
    let t = "";
    [[-56, 4, 1], [-30, -12, 0.75], [30, -12, 0.75], [56, 4, 1]].forEach(([cx, cy, fr], c) => { for (let k = 0; k < (o.per ?? 5); k++) { let d = `M${cx},${cy}`, xx = cx + (k - 2) * 3; const L0 = len * fr * (0.75 + 0.25 * r());
      for (let j = 1; j <= 9; j++) { const yy = cy + (L0 * j) / 9; xx += (r() - 0.5) * 18 + sw * j * 2.4 + (cx < 0 ? -1.2 : 1.2); d += `Q${f1(xx + (j % 2 ? 10 : -10))},${f1(yy - L0 / 18)} ${f1(xx)},${f1(yy)}`; }
      t += `<path d="${d}" stroke="#ffffff" stroke-width="${f1(4.2 - k * 0.5)}" fill="none" opacity="${f1((0.75 - k * 0.08) * fr * lit)}" stroke-linecap="round"/>`;
      t += `<path d="${d}" stroke="#a88ae8" stroke-width="2" fill="none" opacity="${f1(0.6 * lit)}" stroke-dasharray="3 8" stroke-linecap="round"/>`; } });
    return `<g transform="translate(${x},${y}) scale(${s})"${o.id ? ` id="${o.id}"` : ""} opacity="${o.op ?? 1}"><defs><linearGradient id="${g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="${f1(0.75 * lit)}"/><stop offset=".5" stop-color="#bfeaf8" stop-opacity=".35"/><stop offset="1" stop-color="#7ac4e4" stop-opacity=".3"/></linearGradient></defs>
      ${o.glow ? `<ellipse cx="0" cy="-40" rx="110" ry="90" fill="#dff8ff" opacity=".22"/>` : ""}${t}
      <path d="M-30,-12L-36,-84Q-34,-96 -20,-98H20Q34,-96 36,-84L30,-12Z" fill="#cfeef8" opacity=".25"/>
      <path d="M-56,4L-62,-76Q-62,-94 -44,-96L44,-96Q62,-94 62,-76L56,4Q0,16 -56,4Z" fill="url(#${g})" stroke="#f2fcff" stroke-width="4"/>
      <path d="M-30,-10L-34,-88M30,-10L34,-88" stroke="#ffffff" stroke-width="2.4" opacity="${f1(0.7 * lit)}"/><path d="M-56,4L-30,-12L30,-12L56,4" stroke="#ffffff" stroke-width="2.4" fill="none" opacity="${f1(0.6 * lit)}"/>
      <path d="M-50,-70Q-46,-88 -24,-90" stroke="#fff" stroke-width="7" fill="none" opacity="${f1(0.85 * lit)}" stroke-linecap="round"/>
      <path d="M-14,-60Q0,-72 14,-60Q12,-34 0,-26Q-12,-34 -14,-60Z" fill="#c8a8f0" opacity=".35"/>
      ${[-56, -30, 30, 56].map((cx, k) => `<path d="M${cx - 5},${k % 3 ? -12 : 4}L${cx},${(k % 3 ? -12 : 4) + 12}L${cx + 5},${k % 3 ? -12 : 4}" fill="#ffffff" opacity=".75"/>`).join("")}</g>`; };

  // PET water bottle (clear, blue label, blue cap) · (x, y) = the bottom centre; ~200 tall · o.cap false: no cap, o.tilt degrees,
  // o.label text on the label (default none, a wave mark only)
  J.bottle = (x, y, s = 1, o = {}) => { const g = nid("jw");
    return `<g transform="translate(${x},${y}) scale(${s}) rotate(${o.tilt ?? 0})"><defs><linearGradient id="${g}" x1="0" x2="1"><stop offset="0" stop-color="#d8f0fc" stop-opacity=".75"/><stop offset=".35" stop-color="#ffffff" stop-opacity=".45"/><stop offset="1" stop-color="#a8d8f0" stop-opacity=".7"/></linearGradient></defs>
      <path d="M-34,0Q-38,-4 -38,-14V-120Q-38,-140 -22,-152Q-14,-160 -14,-174V-186H14V-174Q14,-160 22,-152Q38,-140 38,-120V-14Q38,-4 34,0Z" fill="url(#${g})" ${OUT(3)}/>
      <path d="M-38,-60H38M-38,-104H38" stroke="#8ac8e8" stroke-width="2" opacity=".6"/><rect x="-38" y="-100" width="76" height="40" fill="#2a7ad0" stroke="${INK}" stroke-width="2.4"/>
      <path d="M-28,-80q10,-8 20,0t20,0t20,0" stroke="#fff" stroke-width="3.4" fill="none"/>${o.label ? `<text x="0" y="-66" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="15" fill="#fff">${o.label}</text>` : ""}
      <path d="M-26,-130Q-28,-50 -24,-10" stroke="#fff" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>
      <path d="M-36,-40Q0,-34 36,-40" stroke="#bfe6f8" stroke-width="3" fill="none" opacity=".8"/>
      <path d="M-15,-186H15" stroke="${INK}" stroke-width="3"/>${o.cap === false ? `<ellipse cx="0" cy="-187" rx="13" ry="4" fill="#d8f0fc" stroke="${INK}" stroke-width="2"/>` : `<rect x="-17" y="-206" width="34" height="22" rx="4" fill="#2a6ad0" ${OUT(2.6)}/><path d="M-12,-202v14M-4,-202v14M4,-202v14M12,-202v14" stroke="#1a4aa0" stroke-width="2"/>`}</g>`; };

  // the vinegar post (เสาน้ำส้มสายชู): a white post with red bands, a little roofed rack on top with slots for 4 bottles (o.full 0…1),
  // the sign "น้ำส้มสายชู · สำหรับแมงกะพรุน" with a jellyfish icon · (x, y) = the foot; ~560 tall
  J.post = (x, y, s = 1, o = {}) => { const n = Math.round((o.full ?? 1) * 4);
    let b = "";
    for (let k = 0; k < 4; k++) { const bx = -63 + k * 42;
      // the painted outline of a bottle on the back panel + the spring clip that holds it
      b += `<g transform="translate(${bx},-392)"><path d="M-13,0V-56Q-13,-64 -6,-70V-80H6V-70Q13,-64 13,-56V0Z" fill="none" stroke="#9a8a6a" stroke-width="2.6" stroke-dasharray="5 4"/>
        <path d="M-16,-36Q-16,-48 -4,-48M16,-36Q16,-48 4,-48" stroke="#8a929a" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="-16" cy="-34" r="3" fill="#8a929a"/><circle cx="16" cy="-34" r="3" fill="#8a929a"/></g>`;
      if (k < n) b += `<g transform="translate(${bx},-392)"><path d="M-13,0V-56Q-13,-64 -6,-70V-80H6V-70Q13,-64 13,-56V0Z" fill="#f6efe0" fill-opacity=".92" ${OUT(2.2)}/><rect x="-13" y="-46" width="26" height="22" fill="#e8b830" stroke="${INK}" stroke-width="1.6"/><rect x="-7" y="-88" width="14" height="10" rx="2" fill="#d8302a" stroke="${INK}" stroke-width="1.6"/><path d="M-8,-58V-8" stroke="#fff" stroke-width="3" opacity=".7"/></g>`; }
    return `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="6" rx="70" ry="14" fill="#5a4a30" opacity=".25"/>
      <rect x="-14" y="-370" width="28" height="372" fill="#f4f2ec" ${OUT(3)}/>${[-60, -150, -240].map((yy) => `<rect x="-14" y="${yy}" width="28" height="22" fill="#d8312a"/>`).join("")}<path d="M-6,-366V-2" stroke="#fff" stroke-width="4" opacity=".7"/>
      <path d="M-96,-378H96V-486H-96Z" fill="#6a5a44" ${OUT(3.4)}/><path d="M-86,-384H86V-480H-86Z" fill="#efe6d2"/><path d="M-86,-480L-70,-470H70L86,-480" fill="#d8ccb0"/>
      <path d="M-96,-378H96" stroke="${INK}" stroke-width="7"/><path d="M-90,-384H90" stroke="#8a7a5a" stroke-width="4"/>${b}
      <path d="M-96,-486V-378M96,-486V-378" stroke="${INK}" stroke-width="6"/>
      <path d="M-112,-486L0,-528L112,-486Z" fill="#d8312a" ${OUT(3.4)}/><path d="M-84,-492L0,-520" stroke="#ff8a7a" stroke-width="4" opacity=".7"/>
      <g transform="translate(0,-290)"><rect x="-104" y="-62" width="208" height="124" rx="12" fill="#fff" ${OUT(3)}/><rect x="-96" y="-54" width="192" height="38" rx="6" fill="#2a7ad0"/>
        <text x="0" y="-26" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="26" fill="#fff">น้ำส้มสายชู</text>
        <circle cx="-58" cy="20" r="34" fill="#e8f6fc" stroke="${INK}" stroke-width="2.4"/><g transform="translate(-58,30) scale(.42)">${J.box(0, 0, 1, { len: 70, seed: 3, lit: 1.4 })}</g>
        <text x="30" y="14" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="17" fill="#1e2a3a">สำหรับแมงกะพรุน</text><text x="30" y="42" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="15" fill="#d8312a" textLength="128" lengthAdjust="spacingAndGlyphs">ราดอย่างน้อย 30 วินาที</text></g></g>`; };

  // the lifeguard tower: a red-and-yellow hut on four stilts with a ladder, a red-yellow flag, a rescue tube and the board "หอกู้ภัย"
  // · (x, y) = the foot of the front stilts; ~900 tall
  J.tower = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="8" rx="230" ry="28" fill="#5a4a30" opacity=".22"/>
    ${[[-150, 0], [150, 0], [-110, -40], [110, -40]].map(([xx, yy], k) => `<path d="M${xx},${yy}L${xx * 0.72},-470" stroke="${INK}" stroke-width="${k < 2 ? 26 : 18}" stroke-linecap="round"/><path d="M${xx},${yy}L${xx * 0.72},-470" stroke="${k < 2 ? "#e8d8b8" : "#c8b898"}" stroke-width="${k < 2 ? 18 : 12}" stroke-linecap="round"/>`).join("")}
    <path d="M-130,-160L130,-300M130,-160L-130,-300" stroke="#a8987a" stroke-width="10"/>
    <g>${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M60,${-60 * k}H140" stroke="#c8b898" stroke-width="10"/>`).join("")}<path d="M60,0V-420M140,0V-420" stroke="${INK}" stroke-width="14"/><path d="M60,0V-420M140,0V-420" stroke="#f0e0c0" stroke-width="8"/></g>
    <path d="M-150,-470H150V-500H-150Z" fill="#8a6a4a" ${OUT(3.4)}/><path d="M-130,-500V-690H130V-500Z" fill="#f2c230" ${OUT(4)}/><path d="M-130,-560H130V-610H-130Z" fill="#d8312a"/>
    <rect x="-96" y="-676" width="192" height="64" fill="#2a3a4a" ${OUT(3)}/><path d="M-90,-670L-40,-618" stroke="#8ac8e8" stroke-width="8" opacity=".5"/>
    <path d="M-170,-690L0,-760L170,-690Z" fill="#d8312a" ${OUT(4)}/><path d="M-140,-700L0,-752" stroke="#ff8a7a" stroke-width="6" opacity=".7"/>
    <rect x="-112" y="-552" width="224" height="46" rx="6" fill="#fff" ${OUT(3)}/><text x="0" y="-518" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="#d8312a">หอกู้ภัย</text>
    <path d="M0,-760V-900" stroke="${INK}" stroke-width="8"/><g ${o.flagId ? `id="${o.flagId}"` : ""}><path d="M4,-900L110,-884L4,-860Z" fill="#d8312a" ${OUT(2.4)}/><path d="M4,-880L110,-884L4,-860Z" fill="#f2c230"/></g>
    <g transform="translate(-150,-420) rotate(8)"><rect x="-14" y="0" width="28" height="200" rx="14" fill="#e8482a" ${OUT(2.6)}/><path d="M0,0V-40" stroke="${INK}" stroke-width="3"/><path d="M-8,20V180" stroke="#ff9a7a" stroke-width="5" opacity=".7"/></g></g>`;

  // ยายลออ's basket of vinegar bottles (a woven bamboo basket, 6 bottles of น้ำส้มสายชู) · (x, y) = the bottom centre; ~180 wide
  J.basket = (x, y, s = 1, o = {}) => { let b = ""; for (let k = 0; k < (o.n ?? 6); k++) { const bx = -66 + k * 26, by = -78 - (k % 2) * 8;
      b += `<g transform="translate(${bx},${by}) rotate(${(k - 2.5) * 4})"><path d="M-11,0V-56Q-11,-62 -5,-68V-78H5V-68Q11,-62 11,-56V0Z" fill="#f6efe0" fill-opacity=".92" ${OUT(2)}/><rect x="-11" y="-44" width="22" height="18" fill="#e8b830" stroke="${INK}" stroke-width="1.4"/><rect x="-6" y="-86" width="12" height="9" rx="2" fill="#d8302a" stroke="${INK}" stroke-width="1.4"/></g>`; }
    let w = ""; for (let k = 0; k < 7; k++) w += `<path d="M${-92 + k * 4},${-74 + k * 11}Q0,${-64 + k * 11} ${92 - k * 4},${-74 + k * 11}" stroke="#8a5a2a" stroke-width="4" fill="none" opacity=".8"/>`;
    return `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="4" rx="110" ry="16" fill="#3a2a1a" opacity=".3"/>${b}
      <path d="M-96,-76Q-90,-6 -64,0H64Q90,-6 96,-76Z" fill="#c8924a" ${OUT(3.4)}/>${w}${[-60, -30, 0, 30, 60].map((xx) => `<path d="M${xx},-74V-2" stroke="#9a6a32" stroke-width="3" opacity=".6"/>`).join("")}
      <path d="M-96,-76Q0,-62 96,-76" stroke="${INK}" stroke-width="5" fill="none"/><path d="M-70,-76Q0,-200 70,-76" stroke="${INK}" stroke-width="10" fill="none"/><path d="M-70,-76Q0,-200 70,-76" stroke="#c8924a" stroke-width="5" fill="none"/></g>`; };

  // tentacles laid over a calf, with the whip-mark welts they leave (red, raised, ladder-like) · pts = the tentacle's path over the skin
  J.welts = (pts, o = {}) => { const d = "M" + pts.map((p) => p.join(",")).join("L");
    return `<g><path d="${d}" stroke="#e85a6a" stroke-width="${o.w ?? 26}" fill="none" opacity=".55" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="#ff8a8a" stroke-width="${(o.w ?? 26) * 0.5}" fill="none" opacity=".6" stroke-linecap="round" stroke-dasharray="4 7"/>
      <path d="${d}" stroke="#eafcff" stroke-width="${(o.w ?? 26) * 0.32}" fill="none" opacity=".75" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="#b49ae8" stroke-width="2.4" fill="none" opacity=".6" stroke-dasharray="2 8"/></g>`; };

  J.ladder = (pts, o = {}) => { const w = o.w ?? 14; let bars = "", d = "M" + pts.map((p) => p.join(",")).join("L");
    for (let k = 0; k < pts.length - 1; k++) { const [x0, y0] = pts[k], [x1, y1] = pts[k + 1], n = Math.max(2, Math.round(Math.hypot(x1 - x0, y1 - y0) / (w * 0.9))), nx = -(y1 - y0), ny = x1 - x0, l = Math.hypot(nx, ny) || 1;
      for (let j = 0; j < n; j++) { const t = (j + 0.5) / n, cx = x0 + (x1 - x0) * t, cy = y0 + (y1 - y0) * t, ux = (nx / l) * w, uy = (ny / l) * w;
        bars += `<path d="M${f1(cx - ux)},${f1(cy - uy)}L${f1(cx + ux)},${f1(cy + uy)}" stroke="#b0306a" stroke-width="${f1(w * 0.32)}" stroke-linecap="round" opacity=".85"/>`; } }
    return `<g><path d="${d}" stroke="#e84a6a" stroke-width="${f1(w * 2.3)}" fill="none" opacity=".45" stroke-linecap="round" stroke-linejoin="round"/>${bars}<path d="${d}" stroke="#d83a7a" stroke-width="${f1(w * 0.9)}" fill="none" opacity=".55" stroke-linecap="round"/>
      <path d="${d}" stroke="#f2feff" stroke-width="${f1(w * 0.42)}" fill="none" opacity=".95" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="#ffffff" stroke-width="${f1(w * 0.14)}" fill="none" stroke-linecap="round" transform="translate(-1,-1.5)"/><path d="${d}" stroke="#a88ae8" stroke-width="${f1(w * 0.12)}" fill="none" stroke-dasharray="2 6"/></g>`; };

  // ------------------------------------------------------------------ sets
  const SETS = (window.Sets = window.Sets || {});
  SETS.jellyBeach = (L, o = {}) => {
    const id = o.id || "jb";
    SETS.tideBeach(L, { boats: 0, fish: 0, sea: 0, near: false, vines: false, islands: [], ...o, view: "sea", time: o.time || "morning" });
    const k = document.getElementById(`${id}-karsts`); if (k) k.setAttribute("display", "none");
    [0, 1].forEach((n) => { const w = document.getElementById(`${id}-boat${n}-w`); if (w) w.setAttribute("display", "none"); });
    // Gulf boats: a Prachuap registration instead of the Andaman one tide.js paints
    [L.set, L.mid, L.far].forEach((ly) => ly && ly.querySelectorAll("text").forEach((t) => { if (/^พง/.test(t.textContent)) t.textContent = t.textContent.replace(/^พง/, "ปข"); }));
    const hz = o.hz ?? 640, r = mk(o.seed || 21);
    // the Gulf: two low green islands far out, a fishing boat's silhouette, the haze line
    if (o.isles !== false) put(L.far, `<g opacity=".9"><path d="M-260,${hz}Q-170,${hz - 46} -60,${hz - 40}Q40,${hz - 30} 120,${hz}Z" fill="#7aa49a"/><path d="M-200,${hz - 30}Q-120,${hz - 42} -40,${hz - 34}" stroke="#a8ccc0" stroke-width="5" fill="none" opacity=".6"/>
      <path d="M900,${hz}Q980,${hz - 28} 1080,${hz - 24}Q1150,${hz - 16} 1220,${hz}Z" fill="#8aaea4"/><rect x="-3000" y="${hz - 14}" width="8000" height="18" fill="#e8f4f2" opacity=".5"/></g>`);
    if (o.rock) { const [x, y, s] = o.rock; put(L.mid, `<g transform="translate(${x},${y}) scale(${s})"><path d="M-120,0Q-110,-70 -40,-96Q20,-110 70,-76Q120,-40 126,0Z" fill="#6a6258" ${OUT(3)}/><path d="M-80,-50Q-30,-86 30,-84" stroke="#9a9288" stroke-width="10" fill="none" opacity=".7"/><path d="M-140,4H150" stroke="#fff" stroke-width="8" opacity=".7"/></g>`); }
    (o.umbrellas || []).forEach(([x, y, s, c]) => put(L.set, `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="4" rx="150" ry="20" fill="#5a4a30" opacity=".2"/><path d="M0,0V-300" stroke="${INK}" stroke-width="9"/><path d="M0,0V-300" stroke="#e8e0d0" stroke-width="5"/>
      <path d="M-170,-290Q0,-420 170,-290Q120,-310 85,-290Q40,-320 0,-292Q-40,-320 -85,-290Q-120,-310 -170,-290Z" fill="${c}" ${OUT(3)}/><path d="M-85,-290Q-40,-360 0,-378M85,-290Q40,-360 0,-378" stroke="#fff" stroke-width="6" fill="none" opacity=".6"/></g>`));
    // beach life: mats and towels, a cooler, a sandcastle with a bucket and spade, flip-flops (o.life [[kind, x, y, s], …])
    const LIFE = {
      mat: (c) => `<path d="M-150,0L-120,-60H150L130,0Z" fill="${c}" ${OUT(3)}/><path d="M-130,-20H140M-125,-40H145" stroke="#fff" stroke-width="7" opacity=".7"/>`,
      towel: (c) => `<path d="M-90,0L-70,-40H100L80,0Z" fill="${c}" ${OUT(3)}/><path d="M-80,-12H90" stroke="#f2c230" stroke-width="8"/>`,
      cooler: () => `<ellipse cx="0" cy="4" rx="70" ry="12" fill="#5a4a30" opacity=".25"/><path d="M-60,0V-80H60V0Z" fill="#2a8ad0" ${OUT(3)}/><path d="M-64,-80H64V-104H-64Z" fill="#f4f2ec" ${OUT(3)}/><path d="M-20,-104q20,-20 40,0" stroke="${INK}" stroke-width="6" fill="none"/><path d="M-50,-60V-10" stroke="#8ac8ec" stroke-width="6" opacity=".7"/>`,
      castle: () => `<path d="M-80,0L-70,-60H-40V-80H-20V-60H20V-80H40V-60H70L80,0Z" fill="#d8c08a" ${OUT(3)}/><path d="M-10,-80V-130L20,-118L-10,-108" fill="#d8312a" stroke="${INK}" stroke-width="2.4"/><g transform="translate(110,0)"><path d="M-28,-60L-22,0H22L28,-60Z" fill="#f06a9a" ${OUT(2.6)}/><ellipse cx="0" cy="-60" rx="28" ry="8" fill="#c84a7a" ${OUT(2.4)}/></g>`,
      flops: () => `<ellipse cx="-20" cy="0" rx="16" ry="34" fill="#f2c230" ${OUT(2.4)}/><ellipse cx="22" cy="6" rx="16" ry="34" fill="#f2c230" ${OUT(2.4)}/><path d="M-20,-18l-8,14M-20,-18l8,14M22,-12l-8,14M22,-12l8,14" stroke="#d8312a" stroke-width="4"/>`,
    };
    (o.life || []).forEach(([kind, x, y, s, c]) => put(L.set, `<g transform="translate(${x},${y}) scale(${s})">${LIFE[kind](c || "#3a9ad8")}</g>`));
    if (o.tower) put(L.set, J.tower(o.tower[0], o.tower[1], o.tower[2], { flagId: `${id}-flag` }));
    if (o.post) put(L.set, J.post(o.post[0], o.post[1], o.post[2], { full: o.post[3] ?? 0 }));
    (o.jellies || []).forEach(([x, y, s, deep], k) => put(L.set, `<g id="${id}-jl${k}" opacity="${f1(1 - 0.55 * (deep ?? 0.5))}">${J.box(x, y, s, { seed: 11 + k, len: 300 + 60 * (k % 3), sway: 0.6 })}</g>`));
    (o.under || []).forEach(([x, y, s], k) => put(L.fg, `<g opacity=".7">${J.box(x, y, s, { seed: 31 + k, len: 220 + 40 * (k % 3), sway: 0.8 })}</g>`));
    if (o.wade) { const [wy, dp] = o.wade, gid = `${id}-wd`; put(L.fg, `<defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3ab0c8" stop-opacity=".55"/><stop offset="1" stop-color="#1a7a9a" stop-opacity=".8"/></linearGradient></defs>
      <path d="M-1300,${wy}Q-400,${wy - 10} 540,${wy}T2400,${wy}V${wy + dp}H-1300Z" fill="url(#${gid})"/><path d="M-1300,${wy}Q-400,${wy - 10} 540,${wy}T2400,${wy}" stroke="#eafcff" stroke-width="7" fill="none" opacity=".85"/>
      ${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${-100 + k * 240},${wy + 24 + (k % 3) * 30}q40,-8 80,0" stroke="#bfeaf2" stroke-width="4" fill="none" opacity=".6"/>`).join("")}`); }
    if (o.ring) put(L.set, `<g id="${id}-ring">${TideCast.duckRing(o.ring[0], o.ring[1], o.ring[2], { water: true })}</g>`);
  };

  SETS.jellyPorch = (L, o = {}) => { const id = o.id || "jp", r = mk(o.seed || 5);
    put(L.sky, `<defs><linearGradient id="${id}-dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a7ab8"/><stop offset=".55" stop-color="#f2a87a"/><stop offset="1" stop-color="#ffe2a8"/></linearGradient>
      <linearGradient id="${id}-pl" x1="0" x2="1"><stop offset="0" stop-color="#8a5a34"/><stop offset=".5" stop-color="#a8703e"/><stop offset="1" stop-color="#7a4a2a"/></linearGradient></defs>
      <rect x="-900" y="-800" width="2900" height="3600" fill="url(#${id}-dawn)"/>`);
    // the window: the sea at dawn, the sun just up, the post on the beach far away
    let win = `<g><rect x="560" y="420" width="420" height="520" fill="url(#${id}-dawn)"/><circle cx="820" cy="760" r="54" fill="#fff2c8"/><circle cx="820" cy="760" r="120" fill="#ffe8a8" opacity=".35"/>
      <rect x="560" y="800" width="420" height="140" fill="#5a8aa8"/><path d="M560,812H980" stroke="#ffe8b8" stroke-width="6" opacity=".8"/>${[0, 1, 2, 3].map((k) => `<path d="M${640 + k * 80},${860 + (k % 2) * 30}h40" stroke="#ffe8b8" stroke-width="4" opacity=".6"/>`).join("")}
      <path d="M560,930Q770,900 980,930V940H560Z" fill="#f0d8a8"/><g transform="translate(640,936) scale(.12)">${J.post(0, 0, 1, { full: 1 })}</g></g>`;
    // plank wall with the window frame and the open door to the right (the window drawn after the planks so none cross the glass)
    let w = `<path d="M-900,-200H2000V1560H-900Z M560,420H980V940H560Z M1080,380H1500V1560H1080Z" fill="url(#${id}-pl)" fill-rule="evenodd"/>`;
    for (let k = 0; k < 32; k++) w += `<path d="M${-880 + k * 90},-200V1560" stroke="#5a3a1e" stroke-width="5" opacity=".55"/><path d="M${-846 + k * 90},${200 + r() * 800}q4,40 0,80" stroke="#6a4224" stroke-width="3" opacity=".5"/>`;
    w += win + `<rect x="540" y="400" width="460" height="560" fill="none" stroke="#4a2a14" stroke-width="40"/><path d="M770,420V940M560,680H980" stroke="#4a2a14" stroke-width="16"/>
      <rect x="1060" y="360" width="460" height="1200" fill="none" stroke="#3a2210" stroke-width="40"/><rect x="1080" y="380" width="420" height="1180" fill="#ffd8a0" opacity=".55"/>`;
    // the shelf with the photo face down (a clue), a gecko
    w += `<rect x="-140" y="620" width="460" height="26" fill="#5a3a1e" ${OUT(3)}/><path d="M-100,646l30,40M280,646l-30,40" stroke="#5a3a1e" stroke-width="10"/>
      <g transform="translate(110,618)"><path d="M-74,0L-70,-14H70L74,0Z" fill="#5a3a20" ${OUT(2.6)}/><path d="M-62,-14H62" stroke="#c8a870" stroke-width="4"/><path d="M10,-14L-22,-66" stroke="#3a2412" stroke-width="9" stroke-linecap="round"/><path d="M10,-14L-22,-66" stroke="#7a5432" stroke-width="4" stroke-linecap="round"/><rect x="-40" y="-14" width="46" height="5" fill="#e8dcc0"/></g>
      <g transform="translate(-60,618)"><path d="M-22,0V-60H22V0Z" fill="#e8dcc0" ${OUT(2.4)}/><path d="M-14,-52h28M-14,-40h20" stroke="#8a7a5a" stroke-width="3"/></g>`;
    // the house post with the sundial (a nail and a painted arc, the shadow at seven)
    if (o.dial !== false) w += `<rect x="-420" y="-200" width="120" height="1760" fill="#6a4224" ${OUT(4)}/><g transform="translate(-360,520)"><path d="M-46,0A46,46 0 0 1 46,0" fill="#f2e2b8" ${OUT(2.4)}/>${[-60, -30, 0, 30, 60].map((a) => `<path d="M0,0L${f1(40 * Math.sin(a * Math.PI / 180))},${f1(-40 * Math.cos(a * Math.PI / 180))}" stroke="#8a5a2a" stroke-width="2"/>`).join("")}<path id="${id}-gnomon" d="M0,0L-30,-26" stroke="#2a1a0e" stroke-width="5" stroke-linecap="round"/><circle r="6" fill="#2a1a0e"/></g>`;
    // a lived-in Thai house: the Buddha shelf with a garland and incense, the calendar, the radio, the fishing net hung on the wall
    w += `<g transform="translate(160,170)"><rect x="-150" y="70" width="300" height="20" fill="#5a3a1e" ${OUT(3)}/><path d="M-120,90l20,30M120,90l-20,30" stroke="#5a3a1e" stroke-width="8"/>
      <path d="M-26,70Q-30,30 0,20Q30,30 26,70Z" fill="#e8b830" ${OUT(2.4)}/><circle cy="10" r="13" fill="#e8b830" ${OUT(2.4)}/><path d="M0,-8l-4,-10h8z" fill="#e8b830"/>
      <path d="M-70,70v-30M-60,70v-36" stroke="#d8312a" stroke-width="4"/><circle cx="-70" cy="38" r="3" fill="#ffb84a"/><circle cx="-60" cy="32" r="3" fill="#ffb84a"/>
      <path d="M50,40q20,40 40,0" stroke="#f2f0ea" stroke-width="9" fill="none"/>${[0, 1, 2, 3, 4].map((k) => `<circle cx="${52 + k * 9}" cy="${42 + Math.sin(k / 4 * Math.PI) * 18}" r="6" fill="${k % 2 ? "#f2c230" : "#f2f0ea"}" stroke="${INK}" stroke-width="1.4"/>`).join("")}<circle cx="70" cy="72" r="7" fill="#d8312a"/></g>
      <g transform="translate(430,700)"><rect x="-70" y="0" width="140" height="190" fill="#fbf7ee" ${OUT(3)}/><rect x="-70" y="0" width="140" height="40" fill="#d8312a"/><text x="0" y="30" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="20" fill="#fff" textLength="128" lengthAdjust="spacingAndGlyphs">พฤศจิกายน</text>
        ${Array.from({ length: 20 }, (_, k) => `<rect x="${-60 + (k % 5) * 25}" y="${56 + Math.floor(k / 5) * 30}" width="18" height="20" fill="${k === 6 ? "#f2c230" : "#e8e0d0"}"/>`).join("")}<path d="M0,0V-14" stroke="${INK}" stroke-width="3"/></g>
      <g transform="translate(240,620)"><rect x="-56" y="-44" width="112" height="44" rx="10" fill="#8a2a2a" ${OUT(2.6)}/><circle cx="-26" cy="-22" r="14" fill="#2a2a2a"/><rect x="6" y="-36" width="38" height="16" fill="#e8dcb0"/><path d="M30,-44L60,-110" stroke="${INK}" stroke-width="3"/></g>
      <g transform="translate(40,780) scale(.75)" opacity=".9"><path d="M0,0L-180,560H180Z" fill="#c8b890" opacity=".35"/>${Array.from({ length: 12 }, (_, k) => `<path d="M0,0L${-180 + k * 33},560" stroke="#8a7a5a" stroke-width="2.4"/>`).join("")}${Array.from({ length: 9 }, (_, k) => `<path d="M${-(k + 1) * 19},${(k + 1) * 60}H${(k + 1) * 19}" stroke="#8a7a5a" stroke-width="2.4"/>`).join("")}<path d="M-180,560H180" stroke="#5a4a30" stroke-width="10"/>${[-150, -90, -30, 30, 90, 150].map((x) => `<circle cx="${x}" cy="566" r="7" fill="#8a8a8a" stroke="${INK}" stroke-width="1.6"/>`).join("")}<circle r="10" fill="#5a3a1e"/></g>`;
    put(L.far, w);
    // the floor boards and the basket at the door
    put(L.set, `<path d="M-900,1540H2000V2400H-900Z" fill="#7a4a24"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-900,${1560 + k * 70}H2000" stroke="#5a341a" stroke-width="5"/>`).join("")}<path d="M1080,1560L1500,1560L1700,2000L900,2000Z" fill="#ffd8a0" opacity=".28"/>
      <path d="M-520,1700L180,1700L240,1900L-580,1900Z" fill="#d8b878" ${OUT(3)}/>${[0, 1, 2, 3, 4, 5, 6, 7, 8].map((k) => `<path d="M${-520 + k * 78},1700L${-580 + k * 91},1900" stroke="#a8884a" stroke-width="4"/>`).join("")}<path d="M-540,1760H200M-560,1830H220" stroke="#c84a3a" stroke-width="8" opacity=".7"/>
      <g transform="translate(380,1640)"><ellipse cx="0" cy="8" rx="130" ry="18" fill="#2a1a0a" opacity=".35"/><path d="M-80,0Q-130,-90 -100,-180Q-90,-220 -60,-230H60Q90,-220 100,-180Q130,-90 80,0Z" fill="#6a3a1e" ${OUT(4)}/><path d="M-110,-130Q0,-110 110,-130" stroke="#d8a040" stroke-width="10" fill="none"/><path d="M-70,-200Q-80,-120 -60,-40" stroke="#a8683a" stroke-width="10" fill="none" opacity=".6"/>
        <ellipse cx="0" cy="-232" rx="70" ry="16" fill="#3a2412" ${OUT(3)}/><g transform="translate(10,-248)"><path d="M-40,0Q-36,26 0,28Q36,26 40,0Z" fill="#d8dce0" ${OUT(2.6)}/><path d="M-28,8Q0,18 28,8" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/></g></g>` + (o.basket !== false ? J.basket(1180, 1640, 1.3) : ""));
  };

  // frame 0: on the wet sand, close: ภูมิ's calf across the frame with the tentacles round it, the uncapped bottle tipping over it
  SETS.jellyHook = (L, o = {}) => { const id = o.id || "jh";
    put(L.sky, `<defs><linearGradient id="${id}-sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cdbb94"/><stop offset=".5" stop-color="#d8c69e"/><stop offset="1" stop-color="#bfa97e"/></linearGradient>
      <linearGradient id="${id}-skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2a878"/><stop offset=".55" stop-color="#cf9262"/><stop offset="1" stop-color="#a86e44"/></linearGradient>
      <linearGradient id="${id}-foam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ac8d8" stop-opacity=".9"/><stop offset=".7" stop-color="#bfe8ec" stop-opacity=".6"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>
      <rect x="-900" y="-800" width="2900" height="3600" fill="url(#${id}-sand)"/>`);
    const r = mk(o.seed || 9); let g = `<path d="M-900,-200H2000V420Q1500,470 1000,440Q540,410 0,460Q-500,500 -900,470Z" fill="url(#${id}-foam)"/><path id="${id}-swash" d="M-900,470Q-500,500 0,460Q540,410 1000,440Q1500,470 2000,420" stroke="#fff" stroke-width="10" fill="none" opacity=".85"/>`;
    for (let k = 0; k < 70; k++) g += `<ellipse cx="${f1(-200 + r() * 1500)}" cy="${f1(500 + r() * 1500)}" rx="${f1(3 + r() * 6)}" ry="${f1(2 + r() * 3)}" fill="#a8946a" opacity=".5"/>`;
    // the title, written with a finger in the wet sand (grooves with a lit lip), the foam about to reach it
    g += `<g transform="translate(540,${o.titleY ?? 1660}) rotate(-4)"><text x="0" y="0" text-anchor="middle" font-family="Sriracha" font-size="150" fill="#8a7650" opacity=".75">${o.title ?? "หนวดใส"}</text><text x="3" y="-4" text-anchor="middle" font-family="Sriracha" font-size="150" fill="none" stroke="#f4ead0" stroke-width="3" opacity=".7">${o.title ?? "หนวดใส"}</text>
      <text x="0" y="96" text-anchor="middle" font-family="Sriracha" font-size="74" fill="#8a7650" opacity=".75">${o.sub ?? "EP.1"}</text></g>`;
    put(L.far, g);
    // the calf (knee at the left edge, foot at the right), swim shorts' hem, the tentacles and welts, sand grains stuck to it
    const leg = `<path d="M-120,980Q140,930 420,960Q640,984 790,1040Q860,1062 900,1030Q950,990 1000,1010Q1060,1040 1040,1110Q1010,1180 900,1170Q760,1150 600,1150Q360,1150 120,1180Q-60,1200 -120,1200Z" fill="url(#${id}-skin)" ${OUT(5)}/>
      <path d="M200,1160Q420,1132 620,1140" stroke="#9a643a" stroke-width="8" fill="none" opacity=".35"/><path d="M140,990Q400,960 640,990" stroke="#f2c49a" stroke-width="12" fill="none" opacity=".6" stroke-linecap="round"/>
      <path d="M-160,960Q-60,940 20,950L40,1220Q-60,1230 -160,1230Z" fill="#f08a1a" ${OUT(5)}/><path d="M20,950L40,1220" stroke="#c86a0a" stroke-width="8"/>`;
    put(L.set, leg + `<g id="${id}-ten">${J.welts([[90, 1000], [180, 1100], [260, 1170]])}${J.welts([[300, 960], [380, 1060], [470, 1150]])}${J.welts([[520, 990], [600, 1080], [650, 1150]], { w: 20 })}${J.welts([[160, 1180], [340, 1000], [560, 1040], [760, 1160]], { w: 18 })}
      <path d="M760,1160Q860,1260 820,1400Q790,1500 900,1600" stroke="#eafcff" stroke-width="7" fill="none" opacity=".7" stroke-linecap="round"/><path d="M650,1150Q700,1300 640,1420" stroke="#eafcff" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/></g>
      <g transform="translate(900,1300) scale(.55) rotate(18)" opacity=".9">${J.box(0, 0, 1, { seed: 4, len: 160 })}</g>`);
    // ต้น's hand from the top holding the uncapped bottle, tipped toward the leg; the cap falling; a first drop at the mouth
    put(L.act, `<g id="${id}-bt"><g transform="translate(470,700) rotate(-128)">${J.bottle(0, 0, 1.25, { cap: false })}</g>
      <g transform="translate(330,520)"><path d="M-40,-60Q20,-90 70,-40Q100,-10 80,30Q50,70 0,60Q-50,50 -60,10Z" fill="#c08a5e" ${OUT(4)}/><path d="M30,-40Q60,-20 60,10M0,-40Q34,-14 30,24M-30,-30Q0,-6 -4,28" stroke="#8a5a3a" stroke-width="4" fill="none"/>
        <path d="M-60,-40L-260,-360L-150,-400L20,-90Z" fill="#5aa8d8" ${OUT(4)}/><path d="M-150,-400L-120,-340" stroke="#4a90c0" stroke-width="8"/></g>
      <g id="${id}-drop"><path d="M600,690Q594,710 600,720Q606,710 600,690Z" fill="#dff4fc" stroke="#7ab8d8" stroke-width="2"/></g>
      <g transform="translate(660,560) rotate(30)"><rect x="-17" y="-11" width="34" height="22" rx="4" fill="#2a6ad0" ${OUT(2.6)}/></g></g>`);
  };

  // the camera half in the sea: above the line the sky, the horizon, the beach far behind with the tower and small people; below it
  // the water lit by the sun — caustic light, shafts, motes, the rippled sand floor. o.surf the surface y (900) · o.shore true
  SETS.jellySplit = (L, o = {}) => { const id = o.id || "js", sy = o.surf ?? 900, r = mk(o.seed || 17);
    put(L.sky, `<defs><linearGradient id="${id}-sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5ab8ec"/><stop offset="1" stop-color="#cfeefa"/></linearGradient>
      <linearGradient id="${id}-uw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5ad0dc"/><stop offset=".45" stop-color="#2aa0bc"/><stop offset="1" stop-color="#16708e"/></linearGradient>
      <linearGradient id="${id}-ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".35"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>
      <rect x="-900" y="-800" width="2900" height="${sy + 800}" fill="url(#${id}-sk)"/>${[[-200, 180, 1.2], [420, 120, 0.9], [900, 220, 1.1], [1500, 160, 1]].map(([x, y, s]) => `<g transform="translate(${x},${y}) scale(${s})">${[0, 1, 2, 3].map((j) => `<ellipse cx="${j * 70 - 100}" cy="${-(j % 2) * 30}" rx="${90 + j * 10}" ry="${50 + (j % 2) * 14}" fill="#ffffff" opacity=".92"/>`).join("")}</g>`).join("")}`);
    // far shore behind: the sand strip, palms, the tower, tiny people (o.shore false: open sea only)
    let f = `<rect x="-900" y="${sy - 34}" width="2900" height="34" fill="#3ab0c8"/>`;
    if (o.shore !== false) { f += `<path d="M-900,${sy - 34}Q540,${sy - 60} 2000,${sy - 34}Z" fill="#e8d6a8"/><path d="M-900,${sy - 46}H2000" stroke="#f4ead0" stroke-width="5" opacity=".7"/>`;
      for (let k = 0; k < 9; k++) { const x = -400 + k * 260 + r() * 80; f += `<g transform="translate(${f1(x)},${sy - 50}) scale(.16)"><path d="M0,0Q-10,-200 20,-420" stroke="#6a5a3a" stroke-width="22" fill="none"/>${[0, 1, 2, 3, 4, 5].map((j) => `<path d="M20,-420q${-140 + j * 56},${-40 + (j % 2) * 30} ${-200 + j * 80},${80 + (j % 3) * 30}" stroke="#2a7a4a" stroke-width="26" fill="none" stroke-linecap="round"/>`).join("")}</g>`; }
      f += `<g transform="translate(${o.towerX ?? 760},${sy - 40}) scale(.15)">${J.tower(0, 0, 1)}</g>`;
      [[300, 0.07], [330, 0.065], [980, 0.07], [520, 0.06]].forEach(([x, s], k) => { f += `<g transform="translate(${x},${sy - 42}) scale(${s})"><circle cy="-560" r="60" fill="${["#3a2a1e", "#2a1a10", "#4a3a2a", "#2a2018"][k]}"/><path d="M-60,-500H60L50,-200H-50Z" fill="${["#d8312a", "#2a7ad0", "#f2c230", "#3aa86a"][k]}"/><path d="M-40,-200V0M40,-200V0" stroke="#8a5a3a" stroke-width="30"/></g>`; }); }
    put(L.far, f);
    // under the surface
    let u = `<rect x="-900" y="${sy}" width="2900" height="${2200 - sy}" fill="url(#${id}-uw)"/>`;
    for (let k = 0; k < 7; k++) { const x = -200 + k * 230 + r() * 60; u += `<path d="M${f1(x)},${sy}L${f1(x + 80)},${sy}L${f1(x + 260)},1920L${f1(x + 100)},1920Z" fill="url(#${id}-ray)" opacity="${f1(0.4 + r() * 0.4)}"/>`; }
    // caustics: a net of bright wavy cells, strongest just under the surface and on the floor
    for (let row = 0; row < 14; row++) { const y = sy + 40 + row * 72; let d = ""; for (let x = -400; x < 1500; x += 90) d += `M${x},${f1(y + r() * 20)}q${f1(30 + r() * 20)},${f1(-18 - r() * 10)} ${f1(70 + r() * 20)},0`; u += `<path d="${d}" stroke="#e8fcff" stroke-width="${f1(3 - row * 0.12)}" fill="none" opacity="${f1(0.42 - row * 0.022)}"/>`; }
    const FL = o.floor ?? 1720; u += `<path d="M-900,${FL}Q-300,${FL - 40} 300,${FL - 10}T1500,${FL - 20}T2600,${FL}V2400H-900Z" fill="#d8c08a"/><path d="M-900,${FL}Q-300,${FL - 40} 300,${FL - 10}T1500,${FL - 20}T2600,${FL}" stroke="#f0dcaa" stroke-width="6" fill="none"/>`;
    for (let k = 0; k < 10; k++) u += `<path d="M${-300 + k * 180},${FL + 40 + (k % 3) * 40}q40,-12 80,0t80,0" stroke="#b8a070" stroke-width="5" fill="none" opacity=".7"/>`;
    for (let k = 0; k < 60; k++) u += `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(sy + 40 + r() * (FL - 20 - sy))}" r="${f1(1.5 + r() * 3)}" fill="#ffffff" opacity="${f1(0.25 + r() * 0.4)}"/>`;
    put(L.mid, u);
    // the surface: a bright meniscus line, the underside sheen, little wavelets above
    put(L.glow, `<path d="M-900,${sy}Q-500,${sy - 8} -100,${sy}T700,${sy}T1500,${sy}T2300,${sy}" stroke="#ffffff" stroke-width="8" fill="none" opacity=".95"/>
      <path d="M-900,${sy + 12}Q-500,${sy + 4} -100,${sy + 12}T700,${sy + 12}T1500,${sy + 12}T2300,${sy + 12}" stroke="#bff4fa" stroke-width="18" fill="none" opacity=".45"/>
      ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${-200 + k * 220},${sy - 10 - (k % 2) * 8}q30,-10 60,0" stroke="#ffffff" stroke-width="4" fill="none" opacity=".8"/>`).join("")}`);
  };
  // swimmers far out: heads, shoulders and a splash at the water line (groups of ≤ 3) · [[x, y, s], …]
  J.swimmers = (list) => list.map(([x, y, s], k) => `<g transform="translate(${x},${y}) scale(${s})">${[[-26, 0, "#2a1a10", "#d8312a"], [10, 4, "#3a2a1e", "#2a7ad0"], [42, -2, "#1a120a", "#f2c230"]].slice(0, k % 2 ? 2 : 3).map(([dx, dy, h, c]) => `<g transform="translate(${dx},${dy})"><path d="M-12,4Q0,-6 12,4" fill="${c}"/><circle cy="-12" r="10" fill="#c08a5e"/><path d="M-10,-16Q0,-26 10,-16" fill="${h}"/><path d="M-18,6h36" stroke="#ffffff" stroke-width="3" opacity=".8"/></g>`).join("")}</g>`).join("");

  // ยายลออ's rule board (in-world, screen space): a hand-painted driftwood plank hung by rope from the vinegar post's crossbar,
  // her three rhyming lines with a painted icon each · o.active 0…2 the rule of this episode (yellow, bigger), done ones ticked,
  // later ones faded · (x, y) the board's top centre; ~760 wide
  J.ruleBoard = (x, y, o = {}) => { const A = o.active ?? 0, rr = mk(5), L3 = [["หนวดใสพันขา", "อย่าราดน้ำท่า"], ["น้ำส้มราดไว้", "นับสามสิบไป"], ["อยู่นิ่งอย่าถู", "เรียกหมอมาดู"]];
    const icon = (k) => k === 0 ? `<g transform="translate(0,6) scale(.34)">${J.box(0, 0, 1, { len: 90, seed: 2, lit: 1.3 })}</g><g transform="translate(26,-6) rotate(-35) scale(.22)">${J.bottle(0, 0, 1, { cap: false })}</g><circle r="44" fill="none" stroke="#d8312a" stroke-width="8"/><path d="M-31,31L31,-31" stroke="#d8312a" stroke-width="8"/>`
      : k === 1 ? `<g transform="translate(-12,40) scale(.42)"><path d="M-13,0V-56Q-13,-64 -6,-70V-80H6V-70Q13,-64 13,-56V0Z" fill="#f6efe0" stroke="${INK}" stroke-width="3"/><rect x="-13" y="-46" width="26" height="22" fill="#e8b830"/></g><circle cx="20" cy="4" r="22" fill="#fff" stroke="${INK}" stroke-width="3"/><path d="M20,4V-12M20,4l10,6" stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/><text x="20" y="44" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="18" fill="#d8312a">30 วิ</text>`
      : `<path d="M-30,30Q-30,-6 0,-10Q30,-6 30,30Z" fill="#2a7ad0" stroke="${INK}" stroke-width="3"/><circle cy="-24" r="14" fill="#c08a5e" stroke="${INK}" stroke-width="3"/><rect x="14" y="-40" width="26" height="42" rx="5" fill="#2a2a32" stroke="${INK}" stroke-width="2.4"/><text x="27" y="-12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="11" fill="#7ae08a">1669</text>`;
    let g = `<g transform="translate(${x},${y})" ${o.gid ? `id="${o.gid}"` : ""}><path d="M-240,-120L-300,0M240,-120L300,0" stroke="#8a6a3a" stroke-width="7"/><circle cx="-240" cy="-122" r="9" fill="#5a4a30"/><circle cx="240" cy="-122" r="9" fill="#5a4a30"/>
      <path d="M-380,0Q-390,-8 -370,-12L370,-16Q392,-8 384,8L378,560Q380,580 360,584L-362,590Q-386,586 -382,566Z" fill="#a88454" stroke="${INK}" stroke-width="6"/>`;
    for (let k = 0; k < 9; k++) g += `<path d="M-370,${30 + k * 62}Q0,${20 + k * 62 + rr() * 16} 372,${32 + k * 62}" stroke="#8a6a3e" stroke-width="3" fill="none" opacity=".6"/>`;
    g += `<text x="0" y="66" text-anchor="middle" font-family="Sriracha" font-size="44" fill="#3a2410">${o.title || "กลอนยายลออ"}</text><path d="M-150,84q150,-12 300,0" stroke="#3a2410" stroke-width="3" fill="none"/>`;
    L3.forEach(([a, b], k) => { const yy = 136 + k * 146, on = k === A, done = k < A, op = k > A ? 0.38 : 1;
      g += `<g opacity="${op}" transform="translate(0,${yy})">${on ? `<rect x="-350" y="-10" width="700" height="132" rx="16" fill="#f2c230" opacity=".85" stroke="${INK}" stroke-width="4"/>` : ""}
        <g transform="translate(-282,56)"><circle r="52" fill="#fbf4e2" stroke="${INK}" stroke-width="4"/>${icon(k)}</g>
        <text x="-200" y="48" font-family="Sriracha" font-size="${on ? 46 : 40}" fill="#2a1a0a">${a}</text><text x="-200" y="102" font-family="Sriracha" font-size="${on ? 46 : 40}" fill="${on ? "#b8241e" : "#2a1a0a"}">${b}</text>
        ${done ? `<g transform="translate(300,56)"><circle r="30" fill="#3aa86a" stroke="${INK}" stroke-width="4"/><path d="M-14,0l9,10l18,-20" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>` : ""}</g>`; });
    return g + `</g>`; };
  // HG7: the subscribe card in the same driftwood family, hung by one rope, a brass bell (o.gid)
  J.subCard = (x, y, o = {}) => `<g transform="translate(${x},${y})" ${o.gid ? `id="${o.gid}"` : ""}><path d="M0,-150V-20" stroke="#8a6a3a" stroke-width="7"/><circle cy="-152" r="9" fill="#5a4a30"/>
    <path d="M-330,-20Q-340,-28 -318,-30L320,-34Q342,-26 336,-8L330,250Q330,268 312,270L-316,276Q-338,272 -334,254Z" fill="#a88454" stroke="${INK}" stroke-width="6"/>
    ${[0, 1, 2, 3].map((k) => `<path d="M-320,${20 + k * 62}Q0,${10 + k * 62} 324,${22 + k * 62}" stroke="#8a6a3e" stroke-width="3" fill="none" opacity=".6"/>`).join("")}
    <g transform="translate(-232,120)"><circle r="76" fill="#d8312a" stroke="${INK}" stroke-width="5"/><path d="M-30,24Q-34,-30 0,-40Q34,-30 30,24L40,34H-40Z" fill="#f2c230" stroke="${INK}" stroke-width="4"/><circle cy="44" r="9" fill="#f2c230" stroke="${INK}" stroke-width="3"/><path d="M-50,-20q-10,20 0,40M50,-20q10,20 0,40" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g>
    <text x="54" y="92" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#b8241e" stroke="#fbf4e2" stroke-width="3" paint-order="stroke">กดติดตาม</text>
    <text x="54" y="156" text-anchor="middle" font-family="Sriracha" font-size="38" fill="#2a1a0a">ไว้ดูกฎข้อต่อไป</text><text x="54" y="210" text-anchor="middle" font-family="Sriracha" font-size="38" fill="#2a1a0a">ก่อนวันที่ต้องใช้</text></g>`;

  // ------------------------------------------------------------------ cast (rig v2 over existing bases)
  const C = window.Rig && Rig.CAST; if (!C) return;
  const b = (k) => (C[k] && C[k].v2) || {};
  const LN = (window.Rig2 && Rig2.LINE) || INK, ln = (w = 2.6) => `stroke="${LN}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const leaves = `<g opacity=".85">${[[-34, -440], [20, -412], [-10, -360], [36, -350]].map(([x, y], k) => `<path transform="translate(${x},${y}) rotate(${k * 50})" d="M0,0q10,-14 22,0q-10,14 -22,0z" fill="#2a8a6a"/>`).join("")}</g>`;
  C.jTon = { v2: { ...b("keng"), skin: "#c08a5e", top: { kind: "shirt", c: "#5aa8d8", sleeve: "short", neck: "collar", collar: "#4a90c0", button: "#fff" }, print: leaves,
    bottom: { kind: "shorts", c: "#e4d6b4" }, feet: { kind: "sandal", c: "#2a2a2a" }, extra: "" } };
  C.jTonBottle = { v2: C.jTon.v2, hand: `<g transform="translate(0,104) rotate(170)">${J.bottle(0, 0, 0.5, { cap: false })}</g>`, keep: "F" };
  C.jTonPhone = { v2: C.jTon.v2, hand: `<g transform="translate(0,118) rotate(-8)"><rect x="-18" y="-32" width="36" height="64" rx="7" fill="#2a2a32" ${ln(2.2)}/><rect x="-14" y="-27" width="28" height="52" rx="4" fill="#5ab8e8"/></g>`, keep: "F" };
  C.jPhum = { v2: { ...b("tang"), top: { kind: "tee", c: "#2a7ad0", sleeve: "short" }, print: `<path d="M-30,-420h60" stroke="#f2c230" stroke-width="8"/>`, bottom: { kind: "shorts", c: "#f08a1a" }, feet: { kind: "bare" }, face: "" } };
  C.jWan = { v2: { ...b("mint"), headScale: 1.28, w: 0.88, limb: 0.84, top: { kind: "tank", c: "#f06a9a", sleeve: "none" },
    print: `<g fill="#fff" opacity=".85">${[[-24, -440], [10, -420], [-10, -390], [26, -380]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5"/>`).join("")}</g>`,
    bottom: { kind: "shorts", c: "#f06a9a" }, feet: { kind: "bare" }, extra: (C.tangRing && C.tangRing.v2.extra) || "" } };
  C.jLaor = { v2: { ...b("yai"), top: { kind: "blouse", c: "#f4e2a8", sleeve: "elbow", trim: "#d8c080" }, print: `<path d="M-22,-488q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0" stroke="#c8a860" stroke-width="2.4" fill="none"/>`,
    bottom: { kind: "sarong", c: "#2a5a7a", band: "#e8c050", band2: "#d8312a" }, extra: "" } };
  C.jLaorBasket = { v2: C.jLaor.v2, hand: `<g transform="translate(0,112)">${J.basket(0, 110, 0.55)}</g>`, keep: "F" };
  C.jGuard = { v2: { ...b("boon"), top: { kind: "tank", c: "#d8312a", sleeve: "none" }, print: `<path d="M-14,-420h28M0,-434v28" stroke="#fff" stroke-width="8"/>`, bottom: { kind: "shorts", c: "#f2c230" }, feet: { kind: "bare" }, extra: "" } };
  C.jWoman = { v2: { ...b("fon"), top: { kind: "tee", c: "#f2f0e8", sleeve: "short" }, print: "", bottom: { kind: "shorts", c: "#3a8a7a" } } };
})();
