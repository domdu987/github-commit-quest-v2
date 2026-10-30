// "ติดเกาะ" — ท่าเรือเกาะหลังเต่า (a fictional fishing village on an island in the Gulf of Thailand) on the morning the family sets out.
// Same layer contract as tide.js (sky / far / mid / set / act / fg; glow above the darkness; light = screen space). Seeded RNG only, no filters.
// Everything that moves is redrawn from the timeline clock by one proxy tween per call (Isl.pier), so any seek gives the same frame.
// Needs pop2.js, qkmat.js and tide.js (Tide.longtail, Tide.coco, Tide.fig) loaded first. Ink #2e2a26; the morning sun is on the right.
//
//   Sets.islPier(L, o)   o.view:
//     "pier"      (default) standing at the landward end of the wooden pier looking along it out to sea: the deck narrows to the
//                 vanishing point (600, 720) where ตาเวียง's stilt hut sits at the pier's end; moored longtails along the right side
//                 (the nearest is ลุงเจี๊ยบ's yellow-and-blue "เจี๊ยบทัวร์", #id-boat), the village beach and palms on the left with the
//                 ทช. vinegar post (#id-vpost, small), the home island's hills far left, เกาะผี a low hump on the right horizon.
//                 Actors stand on the deck: Isl.PIER.spots → near / mid / far {x, y, s} and Isl.PIER.deck(y) → [xL, xR] the deck's
//                 edges at a screen y (feet must sit between them); Isl.PIER.at(d) → {y, s} for a point d metres down the pier.
//     "hut"       at the pier's end in front of ตาเวียง's hut: the raised plank floor, weathered wall, thatch, nets, floats, the lantern,
//                 the shell string, the old paddle hanging on the front post with the three rules carved into its blade (#id-paddle),
//                 the deck planks running toward the camera. Actor spots: Isl.PIER.hutSpots.wiang (700, 1900, 1.0) / kids (380, 1900).
//     "sea"       from the pier's end looking out to sea: the last planks and a bollard at the bottom, open water to the horizon,
//                 เกาะผี on the right, the uncle's boat (#id-boat) close by the pier at first; Isl.pier o.boatGo [a, b] drives it out
//                 toward the horizon (shrinking, with a wake #id-wake) between a and b seconds into the call.
//     "beachpost" on the village beach by the water's edge: the ทช. vinegar post close on the left (#id-vpost: the blue sign
//                 "น้ำส้มสายชู", the jellyfish pictogram, the white box with the bottle), the swash at the bottom, the uncle's boat
//                 passing on the water behind (#id-boat, Isl.pier o.boatGo moves it right and away), the pier and the hut far left.
//     o.time "morning" (default; the only palette drawn here) · o.seed · o.people n small figures on the beach (pier view)
//     ids (redrawn): #id-rip0… ripples, #id-swash, #id-mb0…2 moored boats (bob), #id-flag (the hut's / the boat's pennant), #id-boat,
//                 #id-wake, #id-palm0/1 (data-o = crown), #id-birds
//   Isl.pier(tl, id, t0, dur, o)   runs the view: ripples, swash, the moored boats bob, the pennant, palms, birds; o.boatGo [a, b]
//                 (sea / beachpost views) the boat leaves; o.boatEase
//   Isl.PIER      { VP: [600, 720], HZ: 720, spots, hutSpots, deck(y), at(d) }
//   Isl.vinegarPost(x, y, s, id)   the ทช. post as an SVG string (foot at x, y) for other sets
//   Isl.hut(id, x, G, s, o)        ตาเวียง's hut as an SVG string (ground under the front middle; ~700 wide, 560 tall at s 1)
//   Isl.paddle(x, y, s, o)         the carved paddle (blade up), o.rot, o.id; the three rules in Mali, carved look
(function () {
  const { mk, f1, put, blob, cloud2, crown } = Pop2;
  const Isl = (window.Isl = window.Isl || {});
  const ST = (Isl._st = Isl._st || {});
  const INK = "#2e2a26", OUT2 = `stroke="${INK}" stroke-width="2.5" stroke-linejoin="round"`, OUT3 = `stroke="${INK}" stroke-width="3.5" stroke-linejoin="round"`;
  const T = Qk.tone, CS = Qk.cs, el = (id) => document.getElementById(id);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), lerp = (a, b, k) => a + (b - a) * k, sm = (a, b, x) => { const k = clamp((x - a) / (b - a), 0, 1); return k * k * (3 - 2 * k); };
  const P2 = (p) => `${f1(p[0])},${f1(p[1])}`;
  const PAL = { sky: ["#3a8fd8", "#7fc0ea", "#bfe3f2", "#eaf6f4"], sea: ["#1f8fb0", "#2a9fb8", "#5cc9c4", "#a6ecdf"], sand: ["#f6ead0", "#eedcb4", "#d9c196"], wet: "#c9b08a",
    leaf: ["#2f7a3c", "#4f9a44", "#8cc55a"], green: ["#2c6a3a", "#4c904a", "#8cc268"], wood: ["#b98a52", "#8a6238", "#5e4126"], haze: "#e4f0ee" };
  Sets.DEFS += `
    <linearGradient id="isSkyM" gradientUnits="userSpaceOnUse" x1="0" y1="-1200" x2="0" y2="760"><stop offset="0" stop-color="#2f7fd0"/><stop offset=".55" stop-color="#7fc0ea"/><stop offset=".86" stop-color="#bfe3f2"/><stop offset="1" stop-color="#eaf6f4"/></linearGradient>
    <linearGradient id="isSeaM" gradientUnits="userSpaceOnUse" x1="0" y1="720" x2="0" y2="1900"><stop offset="0" stop-color="#b9dfe6"/><stop offset=".06" stop-color="#2a9fb8"/><stop offset=".4" stop-color="#2fb0bf"/><stop offset=".75" stop-color="#5cc9c4"/><stop offset="1" stop-color="#a6ecdf"/></linearGradient>
    <linearGradient id="isPlank" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c49a62"/><stop offset=".5" stop-color="#b98a52"/><stop offset="1" stop-color="#a0733f"/></linearGradient>
    <linearGradient id="isPlankD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6238"/><stop offset="1" stop-color="#4e3620"/></linearGradient>
    <linearGradient id="isThatch" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9b872"/><stop offset=".5" stop-color="#b8924c"/><stop offset="1" stop-color="#7e5e2e"/></linearGradient>
    <linearGradient id="isHutWall" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8f8470"/><stop offset=".5" stop-color="#a99d86"/><stop offset="1" stop-color="#7a6f5c"/></linearGradient>
    <linearGradient id="isPaddle" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a6a3a"/><stop offset=".45" stop-color="#c18b4c"/><stop offset="1" stop-color="#6d4722"/></linearGradient>
    <linearGradient id="isSignB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b8ae0"/><stop offset="1" stop-color="#1e4e94"/></linearGradient>
    <linearGradient id="isSandB" gradientUnits="userSpaceOnUse" x1="0" y1="1300" x2="0" y2="1950"><stop offset="0" stop-color="#f6ead0"/><stop offset=".7" stop-color="#eedcb4"/><stop offset="1" stop-color="#c9b08a"/></linearGradient>
    <radialGradient id="isGlint" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>`;

  // ---------------- props ----------------
  // the ทช. vinegar post: a wooden post, the blue sign with a jellyfish, the white box with the bottle; foot at (x, y)
  Isl.vinegarPost = (x, y, s = 1, id = "") => {
    let g = CS(0, 6, 70, 12, 0.7) + `<path d="M-13,0V-300H13V0Z" fill="url(#isPlank)" ${OUT2}/><path d="M-13,-300H13L0,-318Z" fill="#7a5a34" ${OUT2}/><path d="M-5,-10V-290" stroke="#fff" stroke-width="3" opacity=".25"/>`;
    g += `<rect x="-92" y="-296" width="184" height="118" rx="10" fill="#000" opacity=".2" transform="translate(5,7)"/><rect x="-92" y="-296" width="184" height="118" rx="10" fill="url(#isSignB)" stroke="#f4f6f8" stroke-width="5"/>`;
    g += `<g transform="translate(-64,-250) scale(.8)"><path d="M-26,0Q-26,-30 0,-30Q26,-30 26,0Z" fill="#fff"/>${[-18, -8, 2, 12].map((tx) => `<path d="M${tx},2q-4,16 2,30" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}<circle cx="0" cy="-12" r="4" fill="#3b8ae0"/></g>`;
    g += `<text x="22" y="-252" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="24" fill="#fff">น้ำส้มสายชู</text><text x="14" y="-222" text-anchor="middle" font-family="Kanit" font-weight="500" font-size="16" fill="#e8f0fa">ปฐมพยาบาลแมงกะพรุน</text><text x="0" y="-194" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="14" fill="#ffd23a">ราดต่อเนื่อง 30 วินาที</text>`;
    g += `<rect x="-60" y="-164" width="120" height="86" rx="8" fill="#000" opacity=".18" transform="translate(4,6)"/><rect x="-60" y="-164" width="120" height="86" rx="8" fill="#f4f6f4" ${OUT2}/><rect x="-60" y="-164" width="120" height="16" rx="6" fill="#d8dcdc"/><path d="M-48,-118h22v-22h14v22h22v14h-22v22h-14v-22h-22z" fill="#d8302a"/>`;
    g += `<g transform="translate(26,-92)"><rect x="-14" y="-56" width="28" height="56" rx="5" fill="#f3e9c8" ${OUT2}/><rect x="-7" y="-70" width="14" height="16" rx="3" fill="#d84a36" ${OUT2}/><rect x="-11" y="-44" width="22" height="22" fill="#2a8ad0"/><path d="M-9,-40h8" stroke="#fff" stroke-width="3"/><path d="M-10,-52v38" stroke="#fff" stroke-width="3" opacity=".6"/></g>`;
    return `<g${id ? ` id="${id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`;
  };
  // the old paddle, blade up, carved with the three rules (o.rot, o.id, o.lit 0…1 brightens the first line)
  Isl.paddle = (x, y, s = 1, o = {}) => {
    const rules = [["กระหายแค่ไหน", "อย่าหมายน้ำเค็ม"], ["พิษไหม้", "อย่าใช้น้ำจืด"], ["เห็นเรือไกล", "อย่าว่ายตาม"]];
    let g = `<path d="M-14,120Q-16,330 -12,520L12,520Q16,330 14,120Z" fill="url(#isPaddle)" ${OUT3}/><path d="M-4,130V505" stroke="#fff" stroke-width="3" opacity=".22"/>`;
    g += `<path d="M-76,-150C-76,-240 -36,-272 0,-272C36,-272 76,-240 76,-150C76,-40 44,60 14,124L-14,124C-44,60 -76,-40 -76,-150Z" fill="url(#isPaddle)" ${OUT3}/>`;
    g += `<path d="M-62,-150C-62,-226 -30,-254 0,-254C10,-254 16,-250 20,-244C-6,-240 -40,-204 -44,-150C-46,-60 -26,40 -6,110L-16,110C-40,40 -62,-60 -62,-150Z" fill="#fff" opacity=".12"/>`;
    g += `<path d="M40,-200C62,-150 56,-40 30,70" stroke="#5a3a1a" stroke-width="2" fill="none" opacity=".5"/><path d="M-38,-120C-30,-20 -14,40 2,96" stroke="#5a3a1a" stroke-width="1.5" fill="none" opacity=".4"/>`;
    g += `<circle cx="0" cy="104" r="5" fill="#3a2a16"/><path d="M0,104Q-40,80 -70,110" stroke="#c8b48a" stroke-width="4" fill="none" stroke-linecap="round"/>`;
    rules.forEach((pair, i) => pair.forEach((r, j) => { const yy = -214 + i * 74 + j * 30, lit = i === 0 ? (o.lit ?? 0) : 0, fs = i ? 15 : 17; g += `<text x="1.5" y="${yy + 2}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fs}" fill="#f7e6c6" opacity=".4">${r}</text><text x="0" y="${yy}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fs}" fill="${lit ? "#ffe9a8" : "#3a2412"}" opacity="${i ? 0.75 : 1}">${r}</text>`; }));
    for (let k = 0; k < 3; k++) g += `<path d="M-52,${-176 + k * 74 + 32}Q0,${-176 + k * 74 + 36} 52,${-176 + k * 74 + 32}" stroke="#3a2412" stroke-width="1.5" fill="none" opacity=".35"/>`;
    return `<g${o.id ? ` id="${o.id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s}) rotate(${o.rot ?? 0})">${g}</g>`;
  };
  // ตาเวียง's stilt hut at the pier's end: posts into the water, a plank floor, weathered teak-grey walls, a thatched roof,
  // nets and floats on the front, a lantern, a shell string, the paddle on the front post (o.paddle false = none, o.paddleId)
  Isl.hut = (id, x, G, s, o = {}) => {
    const r = mk(o.seed || 5);
    let g = `<rect x="-330" y="-50" width="660" height="50" fill="#000" opacity=".22"/>`;
    [-300, -150, 0, 150, 300].forEach((px) => { g += `<rect x="${px - 12}" y="-60" width="24" height="62" fill="#6e5a44" ${OUT2}/><path d="M${px - 6},-58V0" stroke="#fff" stroke-width="2" opacity=".2"/>`; });
    // floor edge and the plank floor's front face
    g += `<rect x="-340" y="-86" width="680" height="28" fill="#8a6238" ${OUT2}/><rect x="-340" y="-96" width="680" height="12" fill="#c49a62"/>${Array.from({ length: 13 }, (_, k) => `<path d="M${-330 + k * 55},-86v26" stroke="#5e4126" stroke-width="2"/>`).join("")}`;
    // back wall of weathered planks, the shaded left wall
    g += `<path d="M-300,-420L-360,-392V-96H-300Z" fill="#6e6454" ${OUT3}/>`;
    g += `<rect x="-300" y="-420" width="600" height="324" fill="url(#isHutWall)" ${OUT3}/>`;
    for (let k = 0; k < 14; k++) g += `<path d="M${-290 + k * 44},-420V-96" stroke="#6b6050" stroke-width="2.4" opacity=".7"/><rect x="${-286 + k * 44}" y="${-400 + (k % 5) * 50}" width="${6 + (k % 3) * 6}" height="${30 + (k % 4) * 16}" fill="#d6cfbf" opacity=".22"/>`;
    g += Qk.grain(-300, -420, 600, 324, 11, { col: "#4a4034", op: 0.28, dir: "v" });
    // the window with its propped shutter, the doorway with a net curtain
    g += `<rect x="-230" y="-350" width="140" height="110" fill="#2a2e30" ${OUT2}/><path d="M-234,-350L-246,-404H-82L-94,-350Z" fill="#8a7e68" ${OUT2}/><path d="M-160,-350V-240M-230,-296H-90" stroke="#5a5244" stroke-width="5"/><path d="M-224,-344h40v30h-40z" fill="#5a8a9a" opacity=".5"/>`;
    g += `<rect x="60" y="-380" width="150" height="284" fill="#1e2224" ${OUT2}/><path d="${Array.from({ length: 9 }, (_, k) => `M${66 + k * 17},-380V-150`).join("")}" stroke="#6a8a5a" stroke-width="2" opacity=".7"/><path d="${Array.from({ length: 10 }, (_, k) => `M60,${-372 + k * 24}H210`).join("")}" stroke="#6a8a5a" stroke-width="1.6" opacity=".5"/>`;
    // the thatched roof: two layers, a ridge, loose ends
    g += `<path d="M-410,-412L-360,-560L380,-560L430,-412Z" fill="url(#isThatch)" ${OUT3}/><path d="M-392,-470L-350,-560L370,-560L410,-470Z" fill="#c9a258" opacity=".5"/>`;
    for (let k = 0; k < 44; k++) { const px = -400 + k * 19 + r() * 6; g += `<path d="M${f1(px)},-412q${f1(-3 + r() * 6)},14 ${f1(-6 + r() * 12)},${f1(22 + r() * 20)}" stroke="#8d6a30" stroke-width="2.2" fill="none" stroke-linecap="round"/>`; }
    for (let k = 0; k < 60; k++) { const px = -380 + r() * 760, py = -550 + r() * 120; g += `<path d="M${f1(px)},${f1(py)}l${f1(-4 + r() * 8)},${f1(10 + r() * 14)}" stroke="${r() < 0.5 ? "#e2c37c" : "#946f32"}" stroke-width="1.8" opacity=".6"/>`; }
    g += `<path d="M-370,-564H390" stroke="#5e4126" stroke-width="8"/><path d="M-370,-568H390" stroke="#f0d49a" stroke-width="2" opacity=".6"/>`;
    // the front posts holding the roof, floats and net on the right post, the lantern and the shell string under the eave
    [-320, 320].forEach((px) => { g += `<rect x="${px - 11}" y="-430" width="22" height="340" fill="#7a5a34" ${OUT2}/><path d="M${px - 4},-425V-100" stroke="#fff" stroke-width="2.5" opacity=".2"/>`; });
    g += `<path d="M300,-404q-70,80 -30,160q30,60 -10,110" stroke="#5a7a4a" stroke-width="3" fill="none" opacity=".9"/>${[[286, -300, "#ff8a3a"], [318, -250, "#f4f0e8"], [296, -196, "#ff8a3a"], [322, -150, "#2a8ad0"]].map(([bx, by, c]) => `<circle cx="${bx}" cy="${by}" r="16" fill="${c}" ${OUT2}/><circle cx="${bx - 5}" cy="${by - 6}" r="5" fill="#fff" opacity=".5"/>`).join("")}`;
    g += `<g transform="translate(-20,-412)"><path d="M0,0V36" stroke="#4a4038" stroke-width="3"/><rect x="-14" y="36" width="28" height="44" rx="6" fill="#d8b24a" ${OUT2}/><rect x="-9" y="44" width="18" height="26" fill="#fff4c0" opacity=".9"/><path d="M-14,80h28" stroke="#4a4038" stroke-width="3"/></g>`;
    g += `${[-120, -100, -80, -60].map((sx, i) => `<path d="M${sx},-412V${-360 - (i % 2) * 14}" stroke="#8a7a6a" stroke-width="1.5"/><circle cx="${sx}" cy="${-356 - (i % 2) * 14}" r="5.5" fill="${i % 2 ? "#f8d8d0" : "#f4e8d8"}" ${OUT2}/>`).join("")}`;
    // a fish trap (ไซ) and a coil of rope by the door, a conch on the floor edge
    g += `<g transform="translate(-60,-100)"><path d="M-40,0Q-50,-90 0,-96Q50,-90 40,0Z" fill="#c8a870" ${OUT2}/>${[-24, -12, 0, 12, 24].map((tx) => `<path d="M${tx},-4q${-tx * 0.1},-44 ${tx * 0.3},-88" stroke="#7a5a2a" stroke-width="2" fill="none"/>`).join("")}${[-70, -52, -34, -18].map((ty) => `<path d="M-38,${ty}Q0,${ty - 8} 38,${ty}" stroke="#7a5a2a" stroke-width="2" fill="none"/>`).join("")}</g>`;
    g += `<ellipse cx="250" cy="-104" rx="40" ry="16" fill="none" stroke="#e8d8a8" stroke-width="7"/><ellipse cx="250" cy="-104" rx="24" ry="9" fill="none" stroke="#d8c898" stroke-width="5"/>`;
    g += `<g transform="translate(170,-108) rotate(-20)"><path d="M-30,10Q-38,-14 -12,-26Q20,-40 36,-14Q46,8 24,16Q0,24 -30,10Z" fill="#f2dcc0" ${OUT2}/><path d="M-26,6Q-6,-6 20,6" stroke="#d8a8a0" stroke-width="3" fill="none"/><path d="M36,-14L48,-22" stroke="#f2dcc0" stroke-width="6" stroke-linecap="round"/></g>`;
    if (o.paddle !== false) g += Isl.paddle(-320, -250, 0.78, { rot: 8, id: o.paddleId });
    return `<g id="${id}-hut" transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  };

  // ---------------- the sky, the far island, the sea ----------------
  function sky(L, id, hz, o = {}) {
    const r = mk(o.seed || 31);
    let g = `<rect x="-3000" y="${f1(hz - 4200)}" width="8000" height="${f1(4200 + hz)}" fill="url(#isSkyM)"/>`;
    g += `<circle cx="${o.sunX ?? 1400}" cy="${f1(hz - 1150)}" r="760" fill="url(#qkSun)" opacity=".7"/>`;
    for (let k = 0; k < 8; k++) { const cx = -900 + r() * 3000, cy = hz - 1700 + r() * 900, w = 360 + r() * 560; g += `<path d="M${f1(cx)},${f1(cy)}q${f1(w * 0.5)},${f1(-12 - r() * 16)} ${f1(w)},${f1(-4 + r() * 10)}" stroke="#ffffff" stroke-width="${f1(6 + r() * 8)}" opacity="${f1(0.12 + r() * 0.12)}" stroke-linecap="round" fill="none"/>`; }
    for (let k = 0; k < 6; k++) g += cloud2(-760 + k * 640 + r() * 220, hz - 760 - r() * 640, 300 + r() * 320, 90 + r() * 60, r, "tdCloudM", "#ffffff", "#9fb8ca");
    g += `<g id="${id}-birds">${[0, 1, 2, 3, 4].map((k) => `<path d="M${f1(300 + k * 70 + r() * 40)},${f1(hz - 560 - k * 24 - r() * 60)}q10,-14 20,0q10,-14 20,0" stroke="#3a4a5a" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>`).join("")}</g>`;
    put(L.sky, g);
  }
  const islandHump = (x, y, w, h, c, c2) => `<path d="M${f1(x - w / 2)},${f1(y)}C${f1(x - w * 0.3)},${f1(y - h * 0.9)} ${f1(x - w * 0.05)},${f1(y - h * 1.25)} ${f1(x + w * 0.12)},${f1(y - h)}C${f1(x + w * 0.3)},${f1(y - h * 0.7)} ${f1(x + w * 0.45)},${f1(y - h * 0.3)} ${f1(x + w / 2)},${f1(y)}Z" fill="${c}"/><path d="M${f1(x - w * 0.42)},${f1(y)}C${f1(x - w * 0.2)},${f1(y - h * 0.8)} ${f1(x)},${f1(y - h * 0.95)} ${f1(x + w * 0.12)},${f1(y - h)}L${f1(x + w * 0.1)},${f1(y)}Z" fill="${c2}" opacity=".5"/>`;

  // ---------------- the pier geometry ----------------
  const VP = [600, 720], HZ = 720, NEAR = 1960, XL0 = 150, XR0 = 1010;
  const tOf = (y) => clamp((NEAR - y) / (NEAR - HZ), 0, 1);
  const deck = (y) => { const t = tOf(y); return [lerp(XL0, VP[0], t), lerp(XR0, VP[0], t)]; };
  // d metres down the pier from the camera (2.6 m up): screen y = HZ + 2500 / d
  const at = (d) => { const y = HZ + 2500 / d; return { y, s: clamp(3.4 / d, 0.1, 1.1) }; };
  const PIER = { VP, HZ, deck, at, spots: { near: { x: 520, y: 1900, s: 0.95 }, near2: { x: 340, y: 1880, s: 0.92 }, mid: { x: 600, y: 1560, s: 0.62 }, far: { x: 600, y: 1340, s: 0.45 } },
    hutSpots: { wiang: { x: 700, y: 1900, s: 1.0 }, fa: { x: 360, y: 1900, s: 0.9 }, phum: { x: 230, y: 1910, s: 0.68 } } };
  Isl.PIER = PIER;

  function pierView(L, o) {
    const id = o.id || "ip", r = mk(o.seed || 9);
    sky(L, id, HZ, { seed: (o.seed || 9) + 1 });
    // far: the sea to the horizon, the home island's hills left, เกาะผี right, far longtails
    let f = `<rect x="-3000" y="${HZ}" width="8000" height="1400" fill="url(#isSeaM)"/>`;
    f += islandHump(-420, HZ + 2, 1500, 230, "#5f8a7a", "#86a98f") + islandHump(-700, HZ + 2, 900, 150, "#7fa48e", "#9ab8a0");
    f += islandHump(1510, HZ + 2, 420, 64, "#6f8e86", "#8aa8a0") + `<path d="M1440,${HZ - 40}q30,-34 70,-6" stroke="#5f7e76" stroke-width="4" fill="none"/>`;
    f += `<rect x="-3000" y="${HZ - 16}" width="8000" height="26" fill="${PAL.haze}" opacity=".55"/>`;
    for (let k = 0; k < 70; k++) { const y = HZ + 8 + Math.pow(r(), 1.8) * 700, x = -600 + r() * 2300, len = 12 + (y - HZ) * 0.25 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1 + (y - HZ) / 260)}" opacity="${f1(0.2 + r() * 0.3)}" stroke-linecap="round"/>`; }
    f += `<g id="${id}-glint">${Array.from({ length: 18 }, () => { const y = HZ + 30 + Math.pow(r(), 1.6) * 420, x = 700 + r() * 900; return `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(14 + (y - HZ) * 0.06)}" ry="${f1(2 + (y - HZ) * 0.008)}" fill="url(#isGlint)"/>`; }).join("")}</g>`;
    [[1180, HZ + 150, 0.07, "#2f6fa0"], [-180, HZ + 230, 0.09, "#2e8a5a"]].forEach(([bx, by, bs, c], k) => { f += `<g id="${id}-fb${k}" transform="translate(${bx},${by}) scale(${bs})">${Tide.longtail({ hull: c, band: "#f2c02a", no: false, flip: !k, water: PAL.sea[1], seed: 20 + k, k: 30 + k })}</g>`; });
    put(L.far, f);
    // mid: the village beach on the left: sand, palms, casuarina, stilt houses, the vinegar post, small people
    let m = `<path d="M-1400,${HZ + 60}Q-300,${HZ + 30} 230,${HZ + 150}Q330,${HZ + 220} 300,${HZ + 420}Q260,${HZ + 700} 120,${HZ + 1100}L-1400,${HZ + 1100}Z" fill="url(#isSandB)"/>`;
    m += `<path d="M230,${HZ + 150}Q330,${HZ + 220} 300,${HZ + 420}Q260,${HZ + 700} 120,${HZ + 1100}" stroke="#fff" stroke-width="5" fill="none" opacity=".7"/><path d="M250,${HZ + 170}Q340,${HZ + 240} 316,${HZ + 420}Q280,${HZ + 690} 150,${HZ + 1080}" stroke="#bfe8e0" stroke-width="9" fill="none" opacity=".45"/>`;
    for (let k = 0; k < 7; k++) { const hx = -900 + k * 190 + r() * 60, hy = HZ + 110 + r() * 40, hs = 0.42 + r() * 0.12; m += `<g transform="translate(${f1(hx)},${f1(hy)}) scale(${f1(hs)})">${CS(0, 4, 160, 20, 0.6)}${[-60, 60].map((px) => `<rect x="${px - 7}" y="-90" width="14" height="90" fill="#7a5a34" ${OUT2}/>`).join("")}<rect x="-90" y="-190" width="180" height="100" fill="${["#a99d86", "#c8b89a", "#8fa0a8"][k % 3]}" ${OUT2}/><rect x="-40" y="-170" width="36" height="46" fill="#2a2e30"/><path d="M-110,-190L-80,-250H80L110,-190Z" fill="${k % 2 ? "url(#tdTin)" : "url(#isThatch)"}" ${OUT2}/></g>`; }
    for (let k = 0; k < 7; k++) { const px = -860 + k * 170 + r() * 80, ps = 0.5 + r() * 0.16, pl = (r() - 0.5) * 0.5; m += Tide.coco(px, HZ + 150 + r() * 60, ps, pl, (o.seed || 9) + 60 + k, { q: 0.5, pal: PAL.leaf, id: k < 2 ? `${id}-palm${k}` : undefined }); }
    m += Isl.vinegarPost(170, HZ + 330, 0.42, `${id}-vpost`);
    for (let k = 0; k < (o.people ?? 5); k++) { const px = -520 + r() * 640, py = HZ + 200 + r() * 160, s2 = (py - HZ) / 300 * 0.9; const pal = [["#e85a4a", "#2a3a5a", "#c88a5a", 0], ["#3a8ac8", "#e8dcc8", "#a8784a", "#f0d050"], ["#f0c040", "#4a4a4a", "#d8a070", 0], ["#58b088", "#2a3a5a", "#b88058", 0]][k % 4]; m += `<g transform="translate(${f1(px)},${f1(py)}) scale(${f1(s2)})">${Tide.fig(`${id}-p${k}`, pal)}</g>`; }
    put(L.mid, m);
    // set: the water near the pier (shallows over sand near the beach), the moored boats, the deck, the posts, the hut at the far end
    let s = "";
    for (let k = 0; k < 12; k++) s += `<path id="${id}-rip${k}" d="" stroke="#ffffff" stroke-width="${f1(1.5 + k * 0.3)}" fill="none" opacity="${f1(0.18 + (k % 3) * 0.1)}" stroke-linecap="round"/>`;
    // moored boats along the right side (drawn before the deck so their near ends tuck behind the planks)
    const MB = [{ x: 1040, y: 1720, s: 0.36, hull: "#f2c030", band: "#1e4e94", no: "เจี๊ยบทัวร์", seed: 3 }, { x: 900, y: 1330, s: 0.2, hull: "#2e8a5a", band: "#f2c02a", no: false, seed: 4 }, { x: 790, y: 1110, s: 0.12, hull: "#2f6fa0", band: "#d8423a", no: false, seed: 5 }];
    MB.forEach((b, k) => { s += `<g id="${id}-mb${k}" transform="translate(${b.x},${b.y}) scale(${b.s})">${CS(-60, 50, 620, 60, 0.7)}${Tide.longtail({ hull: b.hull, band: b.band, no: b.no, flip: false, water: PAL.sea[2], wid: `${id}-mb${k}-w`, seed: b.seed, k: 40 + k })}</g>`; if (k === 0) s += `<g id="${id}-boat"></g>`; });
    // the pier's shadow on the water, the posts under the deck's right edge
    const steps = 28, ys = Array.from({ length: steps + 1 }, (_, k) => HZ + (NEAR - HZ) / (1 + k * 0.17));
    const yEnd = ys[steps];
    s += `<path d="M${f1(XL0 + 40)},${NEAR}L${f1(deck(yEnd)[0] + 10)},${f1(yEnd + 10)}L${f1(deck(yEnd)[1] + 40)},${f1(yEnd + 10)}L${f1(XR0 + 120)},${NEAR}Z" fill="#0b3a44" opacity=".28"/>`;
    for (let k = 1; k < steps; k += 2) { const y = ys[k], [, xr] = deck(y), t = tOf(y), w = lerp(30, 3, t), h = lerp(170, 12, t); s += `<rect x="${f1(xr - w * 0.2)}" y="${f1(y - 6)}" width="${f1(w)}" height="${f1(h)}" fill="url(#isPlankD)" ${t < 0.7 ? OUT2 : ""}/><path d="M${f1(xr + w * 0.2)},${f1(y)}v${f1(h * 0.9)}" stroke="#fff" stroke-width="${f1(w * 0.12)}" opacity=".18"/>`; }
    // the deck: planks across, perspective-spaced, a dark gap between each
    for (let k = steps - 1; k >= 0; k--) {
      const y0 = ys[k + 1], y1 = ys[k], [l0, r0] = deck(y0), [l1, r1] = deck(y1), c = k % 2 ? "#c49a62" : "#b98a52";
      s += `<path d="M${f1(l0)},${f1(y0)}L${f1(r0)},${f1(y0)}L${f1(r1)},${f1(y1)}L${f1(l1)},${f1(y1)}Z" fill="${T(c, -0.06 * (k % 3))}" stroke="#5e4126" stroke-width="${f1(clamp((y1 - y0) * 0.07, 0.8, 3.5))}"/>`;
      if (k < 9) s += `<path d="M${f1(lerp(l1, r1, 0.08))},${f1(y1 - (y1 - y0) * 0.5)}L${f1(lerp(l1, r1, 0.9))},${f1(y1 - (y1 - y0) * 0.5)}" stroke="#fff" stroke-width="${f1(1.5 + (8 - k) * 0.3)}" opacity=".16"/>`;
    }
    for (let k = 0; k < 9; k++) { const y = ys[k] - (ys[k] - ys[k + 1]) * 0.5, [l, rr] = deck(y), nx = lerp(l, rr, 0.12 + k * 0.03); s += `<circle cx="${f1(nx)}" cy="${f1(y)}" r="${f1(clamp(3 - k * 0.3, 1, 3))}" fill="#3a2a16"/><circle cx="${f1(lerp(l, rr, 0.88 - k * 0.03))}" cy="${f1(y)}" r="${f1(clamp(3 - k * 0.3, 1, 3))}" fill="#3a2a16"/>`; }
    // bollards and a rope on the right edge, a tyre fender, a crate of floats on the left
    [[1860, 1.0], [1560, 0.62], [1360, 0.42]].forEach(([y, sc]) => { const [, xr] = deck(y); s += `<g transform="translate(${f1(xr - 26 * sc)},${f1(y)}) scale(${sc})">${CS(0, 4, 30, 8, 0.6)}<rect x="-14" y="-80" width="28" height="80" rx="6" fill="#6e5a44" ${OUT2}/><rect x="-18" y="-90" width="36" height="14" rx="5" fill="#8a7a62" ${OUT2}/><path d="M-6,-76V-6" stroke="#fff" stroke-width="3" opacity=".2"/></g>`; });
    s += `<path d="M${f1(deck(1860)[1] - 26)},1790Q${f1(deck(1700)[1] + 10)},1760 ${f1(deck(1560)[1] - 16)},1500" stroke="#c8b48a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M${f1(deck(1860)[1] - 26)},1790Q${f1(deck(1700)[1] + 10)},1760 ${f1(deck(1560)[1] - 16)},1500" stroke="#8a7a52" stroke-width="2" fill="none" stroke-dasharray="6 5"/>`;
    s += `<g transform="translate(${f1(deck(1760)[1] + 12)},1740)"><ellipse rx="18" ry="46" fill="#2a2a2a" ${OUT2}/><ellipse rx="8" ry="24" fill="#1a1a1a"/><path d="M0,-46V-74" stroke="#c8b48a" stroke-width="4"/></g>`;
    s += `<g transform="translate(${f1(deck(1800)[0] + 70)},1790)">${CS(0, 6, 70, 14, 0.6)}<rect x="-52" y="-56" width="104" height="56" rx="4" fill="#9fb0b8" ${OUT2}/><path d="M-52,-28H52M-20,-56V0M20,-56V0" stroke="#6a7a82" stroke-width="3"/>${[[-30, -66, "#ff8a3a"], [0, -70, "#f4f0e8"], [30, -64, "#2a8ad0"]].map(([bx, by, c]) => `<circle cx="${bx}" cy="${by}" r="15" fill="${c}" ${OUT2}/>`).join("")}</g>`;
    // the hut at the pier's end, a pennant on a pole beside it
    const hutS = (deck(yEnd)[1] - deck(yEnd)[0]) / 700;
    s += Isl.hut(id, VP[0] - 2, yEnd + 2, hutS, { seed: 5, paddle: false });
    s += `<path d="M${f1(VP[0] + 380 * hutS)},${f1(yEnd)}V${f1(yEnd - 720 * hutS)}" stroke="#d8dcdc" stroke-width="${f1(14 * hutS)}"/><path id="${id}-flag" d="" fill="#e8302a"/>`;
    put(L.set, s);
    put(L.fg, `<g transform="translate(1210,-70) rotate(-28)">${Tide.coco(0, 0, 1.25, 0, 77, { trunk: false, pal: [T(PAL.leaf[0], -0.3), T(PAL.leaf[1], -0.2), PAL.leaf[1]] })}</g>`);
    ST[id] = { kind: "pier", MB, flag: { px: VP[0] + 380 * hutS, py: yEnd - 720 * hutS, s: 1.6 * hutS }, rip: 12, hz: HZ };
    draw(id, 0);
  }

  function hutView(L, o) {
    const id = o.id || "ih", r = mk(o.seed || 13);
    sky(L, id, 1000, { seed: (o.seed || 13) + 1, sunX: 1500 });
    let f = `<rect x="-3000" y="1000" width="8000" height="1400" fill="url(#isSeaM)"/>`;
    f += islandHump(1500, 1002, 500, 70, "#6f8e86", "#8aa8a0") + `<rect x="-3000" y="986" width="8000" height="24" fill="${PAL.haze}" opacity=".55"/>`;
    for (let k = 0; k < 40; k++) { const y = 1010 + Math.pow(r(), 1.6) * 500, x = -600 + r() * 2300, len = 14 + (y - 1000) * 0.3 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1 + (y - 1000) / 260)}" opacity="${f1(0.2 + r() * 0.3)}" stroke-linecap="round"/>`; }
    f += `<g transform="translate(1250,1230) scale(.16)">${Tide.longtail({ hull: "#2e8a5a", band: "#f2c02a", no: false, flip: true, water: PAL.sea[2], seed: 8, k: 50 })}</g>`;
    put(L.far, f);
    // set: the deck planks running toward the camera (vanishing point far left-up), the hut on the right half, the water under the deck's edge
    let s = `<rect x="-1300" y="1540" width="3700" height="500" fill="url(#isSeaM)"/>`;
    for (let k = 0; k < 8; k++) s += `<path id="${id}-rip${k}" d="" stroke="#ffffff" stroke-width="${f1(2 + k * 0.4)}" fill="none" opacity="${f1(0.2 + (k % 3) * 0.1)}" stroke-linecap="round"/>`;
    s += Isl.hut(id, 760, 1570, 1.0, { seed: 5, paddleId: `${id}-paddle` });
    const rows = 14;
    for (let k = rows; k >= 0; k--) { const y0 = 1560 + (k / rows) * 420, y1 = 1560 + ((k + 1) / rows) * 420, sk = 0.5 + (k / rows) * 0.5; s += `<path d="M${f1(-1300)},${f1(y0)}H2400V${f1(y1)}H-1300Z" fill="${k % 2 ? "#c49a62" : "#b98a52"}" stroke="#5e4126" stroke-width="${f1(2 + sk * 2)}"/>`; if (k > 9) s += `<path d="M-900,${f1((y0 + y1) / 2)}H2000" stroke="#fff" stroke-width="2" opacity=".14"/>`; }
    s += `<path d="M-1300,1556H2400" stroke="#5e4126" stroke-width="6"/><path d="M-1300,1550H2400" stroke="#e8c68a" stroke-width="3" opacity=".6"/>`;
    for (let k = 0; k < 14; k++) { const x = -1200 + k * 260; s += `<path d="M${x},1560V1990" stroke="#5e4126" stroke-width="2.5" opacity=".8"/><circle cx="${x + 130}" cy="${1600 + (k % 3) * 120}" r="3.5" fill="#3a2a16"/>`; }
    s += `<g transform="translate(1160,1560)">${CS(0, 4, 40, 10, 0.6)}<rect x="-16" y="-96" width="32" height="96" rx="7" fill="#6e5a44" ${OUT2}/><rect x="-21" y="-108" width="42" height="16" rx="6" fill="#8a7a62" ${OUT2}/><path d="M-7,-92V-8" stroke="#fff" stroke-width="3" opacity=".2"/></g>`;
    s += `<path d="M1176,-96Q1240,1500 1300,1480" stroke="#c8b48a" stroke-width="8" fill="none" stroke-linecap="round" transform="translate(0,1560)"/>`;
    put(L.set, s);
    // glow: the paddle is also re-drawn here so it stays crisp over the darkness (nothing stands in front of it)
    put(L.fg, `<g transform="translate(-120,-40) rotate(18)">${Tide.coco(0, 0, 1.2, 0, 71, { trunk: false, pal: [T(PAL.leaf[0], -0.3), T(PAL.leaf[1], -0.25), PAL.leaf[1]] })}</g>`);
    ST[id] = { kind: "hut", rip: 8, hz: 1000, ripY: [1580, 1900], MB: [] };
    draw(id, 0);
  }

  function seaView(L, o) {
    const id = o.id || "is", r = mk(o.seed || 17), hz = 760;
    sky(L, id, hz, { seed: (o.seed || 17) + 1, sunX: 1350 });
    let f = `<rect x="-3000" y="${hz}" width="8000" height="1400" fill="url(#isSeaM)" transform="translate(0,${hz - 720})"/>`;
    f += islandHump(1560, hz + 2, 560, 90, "#5f7e76", "#7a9a90") + `<path d="M1470,${hz - 52}q40,-40 90,-10" stroke="#4e6e66" stroke-width="5" fill="none"/>` + `<rect x="-3000" y="${hz - 16}" width="8000" height="26" fill="${PAL.haze}" opacity=".55"/>`;
    for (let k = 0; k < 90; k++) { const y = hz + 8 + Math.pow(r(), 1.7) * 900, x = -800 + r() * 2700, len = 12 + (y - hz) * 0.25 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1 + (y - hz) / 260)}" opacity="${f1(0.18 + r() * 0.3)}" stroke-linecap="round"/>`; }
    f += `<g id="${id}-glint">${Array.from({ length: 22 }, () => { const y = hz + 30 + Math.pow(r(), 1.5) * 520, x = 600 + r() * 1000; return `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(14 + (y - hz) * 0.06)}" ry="${f1(2 + (y - hz) * 0.008)}" fill="url(#isGlint)"/>`; }).join("")}</g>`;
    put(L.far, f);
    let s = "";
    for (let k = 0; k < 12; k++) s += `<path id="${id}-rip${k}" d="" stroke="#ffffff" stroke-width="${f1(1.5 + k * 0.35)}" fill="none" opacity="${f1(0.18 + (k % 3) * 0.1)}" stroke-linecap="round"/>`;
    s += `<path id="${id}-wake" d="" fill="#ffffff" opacity=".55"/>`;
    s += `<g id="${id}-boatP"><g id="${id}-boat">${CS(-60, 50, 620, 60, 0.6)}${Tide.longtail({ hull: "#f2c030", band: "#1e4e94", no: "เจี๊ยบทัวร์", flip: true, water: PAL.sea[2], wid: `${id}-boat-w`, seed: 3, k: 60 })}</g></g>`;
    // the pier's end at the bottom: the last planks, the right-edge posts, a bollard with a rope, the pennant pole
    const rows = 7;
    for (let k = rows; k >= 0; k--) { const y0 = 1560 + (k / rows) * 420, y1 = 1560 + ((k + 1) / rows) * 420; s += `<path d="M-1300,${f1(y0)}H2400V${f1(y1)}H-1300Z" fill="${k % 2 ? "#c49a62" : "#b98a52"}" stroke="#5e4126" stroke-width="${f1(2 + k * 0.3)}"/>`; }
    s += `<path d="M-1300,1556H2400" stroke="#5e4126" stroke-width="7"/><path d="M-1300,1549H2400" stroke="#e8c68a" stroke-width="3" opacity=".6"/>`;
    for (let k = 0; k < 14; k++) { const x = -1200 + k * 260; s += `<path d="M${x},1560V1990" stroke="#5e4126" stroke-width="2.5" opacity=".8"/>`; }
    s += `<g transform="translate(900,1600)">${CS(0, 4, 44, 10, 0.6)}<rect x="-18" y="-110" width="36" height="110" rx="7" fill="#6e5a44" ${OUT2}/><rect x="-24" y="-124" width="48" height="18" rx="7" fill="#8a7a62" ${OUT2}/><path d="M-8,-106V-8" stroke="#fff" stroke-width="3" opacity=".2"/><path d="M-20,-96Q-70,-70 -110,-20" stroke="#c8b48a" stroke-width="8" fill="none" stroke-linecap="round"/></g>`;
    s += `<g transform="translate(760,1640)">${CS(0, 4, 70, 14, 0.5)}<ellipse rx="60" ry="22" fill="none" stroke="#e8d8a8" stroke-width="10"/><ellipse rx="34" ry="12" fill="none" stroke="#d8c898" stroke-width="7"/><path d="M-60,0q20,-20 60,-12" stroke="#c8b488" stroke-width="5" fill="none"/></g>`;
    s += `<path d="M150,1560V1100" stroke="#d8dcdc" stroke-width="5"/><circle cx="150" cy="1096" r="7" fill="#e8c040"/><path id="${id}-flag" d="" fill="#e8302a"/>`;
    put(L.set, s);
    ST[id] = { kind: "sea", rip: 12, hz, ripY: [hz + 40, 1540], MB: [], flag: { px: 150, py: 1100, s: 0.45 }, boat: { from: { x: 640, y: 1430, s: 0.5 }, to: { x: 1180, y: hz + 60, s: 0.07 } } };
    draw(id, 0);
  }

  function beachpostView(L, o) {
    const id = o.id || "ib", r = mk(o.seed || 21), hz = 700;
    sky(L, id, hz, { seed: (o.seed || 21) + 1, sunX: 1400 });
    let f = `<rect x="-3000" y="${hz}" width="8000" height="1400" fill="url(#isSeaM)" transform="translate(0,${hz - 720})"/>`;
    f += islandHump(1560, hz + 2, 420, 64, "#6f8e86", "#8aa8a0") + `<rect x="-3000" y="${hz - 16}" width="8000" height="26" fill="${PAL.haze}" opacity=".55"/>`;
    for (let k = 0; k < 70; k++) { const y = hz + 8 + Math.pow(r(), 1.7) * 700, x = -800 + r() * 2700, len = 12 + (y - hz) * 0.25 * r(); f += `<path d="M${f1(x)},${f1(y)}h${f1(len)}" stroke="#fff" stroke-width="${f1(1 + (y - hz) / 260)}" opacity="${f1(0.18 + r() * 0.3)}" stroke-linecap="round"/>`; }
    // the pier far left with the hut at its end, a moored boat
    f += `<path d="M-1300,${hz + 230}L-100,${hz + 170}L-90,${hz + 200}L-1300,${hz + 300}Z" fill="#8a6238" ${OUT2}/>${Array.from({ length: 9 }, (_, k) => `<rect x="${-1200 + k * 140}" y="${hz + 190 + k * 6}" width="8" height="${40 + k * 4}" fill="#5e4126"/>`).join("")}`;
    f += Isl.hut(id, -60, hz + 182, 0.11, { seed: 5, paddle: false });
    f += `<g transform="translate(-700,${hz + 330}) scale(.17)">${Tide.longtail({ hull: "#2e8a5a", band: "#f2c02a", no: false, flip: false, water: PAL.sea[2], seed: 8, k: 70 })}</g>`;
    put(L.far, f);
    let m = `<path id="${id}-wake" d="" fill="#ffffff" opacity=".55"/><g id="${id}-boatP"><g id="${id}-boat">${CS(-60, 50, 620, 60, 0.6)}${Tide.longtail({ hull: "#f2c030", band: "#1e4e94", no: "เจี๊ยบทัวร์", flip: false, water: PAL.sea[2], wid: `${id}-boat-w`, seed: 3, k: 80 })}</g></g>`;
    put(L.mid, m);
    // set: the beach, the swash, the post, shells, a palm on the right
    let s = `<path d="M-1300,1480Q540,1450 2400,1490V2400H-1300Z" fill="url(#isSandB)"/>`;
    for (let k = 0; k < 20; k++) { const y = 1520 + Math.pow(r(), 1.2) * 420, x = -900 + r() * 2900, w = 60 + r() * 200; s += `<path d="M${f1(x)},${f1(y)}q${f1(w / 2)},-6 ${f1(w)},0" stroke="#fff" stroke-width="3" fill="none" opacity=".35"/>`; }
    for (let k = 0; k < 14; k++) { const x = -200 + r() * 1400, y = 1700 + r() * 220, sz = 7 + r() * 9; s += `<path d="M${f1(x - sz)},${f1(y)}a${f1(sz)},${f1(sz * 0.7)} 0 0 1 ${f1(sz * 2)},0l${f1(-sz)},${f1(sz * 0.5)}z" fill="${["#f8f2ea", "#f4d8cc", "#e8dcc0"][k % 3]}" stroke="#9a8a72" stroke-width="1.2"/>`; }
    s += `<path id="${id}-swashW" d="" fill="${PAL.wet}" opacity=".55"/><path id="${id}-swashS" d="" fill="${PAL.sea[3]}" opacity=".7"/><path id="${id}-swash" d="" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".95"/><path id="${id}-swash2" d="" stroke="#fff" stroke-width="5" fill="none" opacity=".5"/>`;
    s += Isl.vinegarPost(300, 1850, 1.0, `${id}-vpost`);
    s += Tide.coco(1380, 2000, 2.2, -0.08, (o.seed || 21) + 71, { id: `${id}-palm0`, pal: PAL.leaf, fl: 0.6 });
    put(L.set, s);
    ST[id] = { kind: "beachpost", rip: 0, hz, MB: [], swashY: 1520, shore: true, boat: { from: { x: 300, y: hz + 330, s: 0.3 }, to: { x: 1500, y: hz + 120, s: 0.12 } } };
    draw(id, 0);
  }

  // ---------------- redraw from the clock ----------------
  function draw(id, t, o = {}) {
    const S = ST[id];
    if (!S) return;
    for (let k = 0; k < S.rip; k++) {
      const e = el(`${id}-rip${k}`); if (!e) continue;
      const [ya, yb] = S.ripY || [S.hz + 60, 1900], y = ya + ((k + 0.5) / S.rip) * (yb - ya) + 6 * Math.sin(t * 0.9 + k), d0 = (y - S.hz) / (1900 - S.hz), x0 = -900 + 400 * Math.sin(k * 2.1) + 40 * Math.sin(t * 0.5 + k), len = 500 + 900 * d0;
      let d = ""; for (let x = x0; x <= x0 + len; x += 30) d += `${d ? "L" : "M"}${f1(x)},${f1(y + (1 + 6 * d0) * Math.sin(x * 0.02 + t * 1.6 + k) + (0.5 + 3 * d0) * Math.sin(x * 0.051 - t * 2.2))}`;
      e.setAttribute("d", d);
    }
    S.MB.forEach((b, k) => { const g = el(`${id}-mb${k}`); if (!g) return; g.setAttribute("transform", `translate(${f1(b.x)},${f1(b.y + 2.5 * b.s * 3 * Math.sin(t * 1.5 + k))}) rotate(${f1(1.6 * Math.sin(t * 1.1 + k * 2))}) scale(${b.s})`); });
    if (S.flag) { const a = el(`${id}-flag`); if (a) { const { px, py, s } = S.flag, W = 110 * s, H = 60 * s; let d = ""; for (let k = 0; k <= 10; k++) { const u = k / 10, x = px + u * W, w = Math.sin(u * 5 - t * 6) * 6 * s * u; d += `${k ? "L" : "M"}${f1(x)},${f1(py + w)}`; } for (let k = 10; k >= 0; k--) { const u = k / 10, x = px + u * W, w = Math.sin(u * 5 - t * 6) * 6 * s * u; d += `L${f1(x)},${f1(py + H * (1 - u * 0.7) + w)}`; } a.setAttribute("d", d + "Z"); } }
    const sw = el(`${id}-swash`);
    if (sw && S.swashY) {
      const yb = S.swashY + 30 * Math.sin(t * 1.3), pts = []; for (let x = -1300; x <= 2400; x += 40) pts.push(`${x},${f1(yb + 12 * Math.sin(x * 0.006 + t * 1.2) + 6 * Math.sin(x * 0.021 - t * 2))}`);
      sw.setAttribute("d", `M${pts.join("L")}`); el(`${id}-swash2`).setAttribute("d", `M${pts.map((p) => { const [x, y] = p.split(","); return `${x},${f1(+y - 22)}`; }).join("L")}`);
      // on the shore the sea lies above the swash line (the sand runs down to the camera): a sheet of water from the sand's edge to the foam, the wet sand it leaves below
      if (S.shore) { el(`${id}-swashS`).setAttribute("d", `M-1300,1470L2400,1470L${pts.slice().reverse().join("L")}Z`); el(`${id}-swashW`).setAttribute("d", `M${pts.join("L")}L2400,${f1(S.swashY + 70)}L-1300,${f1(S.swashY + 70)}Z`); }
      else el(`${id}-swashW`).setAttribute("d", `M${pts.join("L")}L2400,2400L-1300,2400Z`);
    }
    [0, 1].forEach((k) => { const p = el(`${id}-palm${k}`); if (p && p.getAttribute("data-o")) { const [px, py] = p.getAttribute("data-o").split(" "); p.setAttribute("transform", `rotate(${f1(1.8 * Math.sin(t * 1.1 + k * 2))} ${px} ${py})`); } });
    const bd = el(`${id}-birds`); if (bd) bd.setAttribute("transform", `translate(${f1(-t * 9)},${f1(-t * 3 + 3 * Math.sin(t * 2))})`);
    const gl = el(`${id}-glint`); if (gl) gl.setAttribute("opacity", f1(0.7 + 0.3 * Math.sin(t * 5)));
    // the boat going out (sea / beachpost): position and scale between from and to, a wake fanning out behind it
    const bp = el(`${id}-boatP`);
    if (bp && S.boat) {
      const k = clamp(o.go ?? 0, 0, 1), E = k * k * (3 - 2 * k), F = S.boat.from, Tt = S.boat.to, x = lerp(F.x, Tt.x, E), y = lerp(F.y, Tt.y, E), s = lerp(F.s, Tt.s, E);
      bp.setAttribute("transform", `translate(${f1(x)},${f1(y + 2 * Math.sin(t * 1.7))}) rotate(${f1(1.2 * Math.sin(t * 1.3))}) scale(${f1(s)})`);
      const wk = el(`${id}-wake`), dir = S.kind === "sea" ? -1 : 1, L2 = 900 * s * (0.4 + k), ww = 60 * s;
      if (wk) wk.setAttribute("d", k > 0.02 ? `M${f1(x + dir * 380 * s)},${f1(y + 30 * s)}Q${f1(x + dir * 380 * s - dir * L2 * 0.5)},${f1(y + 30 * s - ww)} ${f1(x + dir * 380 * s - dir * L2)},${f1(y + 36 * s - ww * 0.6)}L${f1(x + dir * 380 * s - dir * L2)},${f1(y + 36 * s + ww * 0.6)}Q${f1(x + dir * 380 * s - dir * L2 * 0.5)},${f1(y + 30 * s + ww)} ${f1(x + dir * 380 * s)},${f1(y + 40 * s)}Z` : "");
    }
  }
  Isl.pier = (tl, id, t0, dur, o = {}) => {
    const c = { t: 0 }, [a, b] = o.boatGo || [99, 100], E = gsap.parseEase(o.boatEase || "power1.in");
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => draw(id, t0 + c.t, { go: o.boatGo ? E(clamp((c.t - a) / Math.max(0.01, b - a), 0, 1)) : 0 }) }, t0);
  };
  function islPier(L, o = {}) { const v = o.view || "pier"; return v === "hut" ? hutView(L, o) : v === "sea" ? seaView(L, o) : v === "beachpost" ? beachpostView(L, o) : pierView(L, o); }
  Object.assign(Sets, { islPier });
})();
