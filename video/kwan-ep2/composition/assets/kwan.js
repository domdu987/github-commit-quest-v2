// Sets and figures for "ควันหลง": an old eight-storey women's dormitory in the city, 2 a.m., a fire on the seventh floor.
// Most of the story is seen through your own eyes (pov.js): room 714 is one wide panorama, so turning your head is a
// camera pan across a single room — door wall (x 0–1100), แพร's bed (x 1100–2200), the window (x 2200–3300); the ceiling
// is above y 500, the floor below y 1520. Also the dorm from outside, the peephole, the drop from the window, your phone,
// and the key-tag end card. Same layer contract as sets.js; seeded RNG only.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const CEIL = 500, FLOOR = 1520;
  let uid = 0; // clip-path ids must be unique per shot even when shots share a set id (element ids may repeat: fx tweens them together)

  Sets.DEFS += `
    <linearGradient id="kwWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b4746"/><stop offset=".55" stop-color="#34403f"/><stop offset="1" stop-color="#263030"/></linearGradient>
    <linearGradient id="kwCeil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d2222"/><stop offset="1" stop-color="#2c3333"/></linearGradient>
    <linearGradient id="kwFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d342d"/><stop offset="1" stop-color="#211c18"/></linearGradient>
    <linearGradient id="kwWood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3c28"/><stop offset=".5" stop-color="#6e4a32"/><stop offset="1" stop-color="#4c3221"/></linearGradient>
    <linearGradient id="kwWoodV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6e4a32"/><stop offset="1" stop-color="#3e2a1c"/></linearGradient>
    <linearGradient id="kwGap" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff9a3a" stop-opacity=".95"/><stop offset=".35" stop-color="#ff7a2a" stop-opacity=".4"/><stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></linearGradient>
    <radialGradient id="kwGapPool"><stop offset="0" stop-color="#ffb04a" stop-opacity=".7"/><stop offset=".4" stop-color="#ff8a2a" stop-opacity=".28"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="kwLed"><stop offset="0" stop-color="#ff5a4a" stop-opacity="1"/><stop offset=".3" stop-color="#ff3a2a" stop-opacity=".5"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <linearGradient id="kwMoonShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ec3ff" stop-opacity=".22"/><stop offset="1" stop-color="#9ec3ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="kwNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070a12"/><stop offset=".55" stop-color="#121a2a"/><stop offset="1" stop-color="#2a2a38"/></linearGradient>
    <linearGradient id="kwGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1420" stop-opacity=".2"/><stop offset=".5" stop-color="#3a4a66" stop-opacity=".18"/><stop offset="1" stop-color="#0d1420" stop-opacity=".25"/></linearGradient>
    <linearGradient id="kwFacade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a4d52"/><stop offset=".5" stop-color="#5c6066"/><stop offset="1" stop-color="#3c3f44"/></linearGradient>
    <radialGradient id="kwFireWin"><stop offset="0" stop-color="#fff0b0"/><stop offset=".35" stop-color="#ffb04a"/><stop offset=".7" stop-color="#ff6a1a"/><stop offset="1" stop-color="#9a2a0a"/></radialGradient>
    <radialGradient id="kwFireGlow"><stop offset="0" stop-color="#ff9a3a" stop-opacity=".55"/><stop offset=".45" stop-color="#ff7a2a" stop-opacity=".2"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="kwStreet"><stop offset="0" stop-color="#ffd58a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd58a" stop-opacity="0"/></radialGradient>
    <radialGradient id="kwSiren"><stop offset="0" stop-color="#ff3a3a" stop-opacity=".9"/><stop offset="1" stop-color="#ff3a3a" stop-opacity="0"/></radialGradient>
    <radialGradient id="kwSirenB"><stop offset="0" stop-color="#3a7aff" stop-opacity=".9"/><stop offset="1" stop-color="#3a7aff" stop-opacity="0"/></radialGradient>
    <radialGradient id="kwPeep" cx=".5" cy=".5" r=".5"><stop offset=".78" stop-color="#000" stop-opacity="0"/><stop offset=".95" stop-color="#000" stop-opacity=".85"/><stop offset="1" stop-color="#000"/></radialGradient>
    <linearGradient id="kwPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9dfc4"/><stop offset="1" stop-color="#cbbd98"/></linearGradient>
    <linearGradient id="kwScreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2a44"/><stop offset=".6" stop-color="#2a1e3a"/><stop offset="1" stop-color="#10121c"/></linearGradient>`;

  // ---------------- figures ----------------
  // ดาว sitting up in a bed (designed for this story, not borrowed from another): a girl who burned — charcoal skin cracked
  // like cooling embers, the cracks glowing orange; her face is only cracks: two ember slits for eyes and a split for a mouth;
  // her student blouse scorched through; frizzled burnt hair that still smokes. Origin = her hips on the mattress; parts by id:
  // #id-up (upper body, rotate from lying), #id-head, #id-arm (reaching), #id-eyes
  function daoSit(id, s = 1) {
    const CH = "#1b1512", RIM = `stroke="#3a2a22" stroke-width="3" stroke-linejoin="round"`, LAVA = "#ff6a1a";
    const crack = (d, w = 3.5) => `<path class="flk" d="${d}" stroke="${LAVA}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>`;
    const frizz = [-50, -36, -22, -8, 6, 20, 34, 48].map((x, k) => `<path d="M${x},-52q${k % 2 ? 8 : -8},-16 ${k % 2 ? -2 : 4},-30q${k % 2 ? -6 : 6},-10 ${k % 2 ? 4 : -2},-20" stroke="#120d0b" stroke-width="9" fill="none" stroke-linecap="round"/>`).join("");
    return `<g id="${id}" transform="scale(${s})">
      <g id="${id}-up" transform="rotate(0)">
        <path d="M-52,0C-62,-80 -58,-170 -40,-236C-30,-270 30,-272 42,-238C58,-170 62,-80 52,0Z" fill="#cfc8b8" ${RIM}/>
        <path d="M-52,-30C-40,-90 -10,-60 -4,-120C2,-170 40,-150 50,-200L46,-110C30,-90 10,-60 -10,-40Z" fill="#2a221d"/>
        ${[[-30, -150, 16], [26, -70, 20], [-14, -200, 12], [34, -190, 10]].map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 0.8}" fill="${CH}"/><ellipse cx="${x}" cy="${y}" rx="${r * 0.55}" ry="${r * 0.4}" fill="${LAVA}" opacity=".5" class="flk"/>`).join("")}
        <path d="M-34,-238Q0,-214 34,-238L26,-224Q0,-206 -26,-224Z" fill="#2a221d"/><rect x="-16" y="-206" width="32" height="15" rx="2" fill="#8a8478" opacity=".6"/><text x="0" y="-194" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="11" fill="#1a1612">714</text>
        <g id="${id}-head" transform="translate(0,-262) rotate(0)">
          <path d="M-14,40V20M14,40V20" stroke="${CH}" stroke-width="16"/>
          <ellipse cx="0" cy="-4" rx="50" ry="58" fill="${CH}" ${RIM}/>${frizz}
          ${crack("M-40,-30l14,10l-6,16l12,12M30,-40l-8,16l10,10M-6,30l6,12l-8,8M40,10l-10,4", 3)}
          <g id="${id}-eyes"><path d="M-30,-6Q-18,-14 -6,-6Q-18,0 -30,-6Z" fill="#ffd27a"/><path d="M8,-4Q20,-12 32,-4Q20,2 8,-4Z" fill="#ffd27a"/>
            <ellipse cx="-18" cy="-6" rx="20" ry="11" fill="${LAVA}" opacity=".35"/><ellipse cx="20" cy="-4" rx="20" ry="11" fill="${LAVA}" opacity=".35"/></g>
          ${crack("M-18,24l6,-4l6,6l6,-6l6,4l6,-4", 4)}
          <g class="smk" data-d="6">${[0, 1, 2].map((k) => `<path d="M${-30 + k * 26},-80C${-40 + k * 26},-120 ${-10 + k * 26},-150 ${-24 + k * 26},-200" stroke="#5a5550" stroke-width="${8 - k * 2}" fill="none" opacity="${0.45 - k * 0.1}" stroke-linecap="round"/>`).join("")}</g></g>
        <g id="${id}-arm" transform="translate(56,-200) rotate(0)">
          <path d="M0,0C14,60 30,130 40,200" stroke="${CH}" stroke-width="18" fill="none" stroke-linecap="round"/>${crack("M6,40l8,20l-4,18M24,120l6,22", 3)}
          ${[[-4, 54], [6, 60], [16, 56], [26, 48]].map(([dx, l]) => `<path d="M${40 + dx * 0.3},202l${dx * 0.4},${l}" stroke="${CH}" stroke-width="7" stroke-linecap="round"/><circle cx="${40 + dx * 0.3 + dx * 0.4}" cy="${202 + l}" r="3" fill="${LAVA}" class="flk"/>`).join("")}</g>
      </g></g>`;
  }
  // a charred hand dangling over the edge of the mattress (fingers down), wrist at the origin
  const burntHand = (id, s = 1) => `<g id="${id}" transform="scale(${s})"><path d="M-14,-40V20" stroke="${INK}" stroke-width="34" stroke-linecap="round"/><path d="M-14,-40V20" stroke="#3e3530" stroke-width="26" stroke-linecap="round"/>
      <g transform="translate(-14,46)"><ellipse rx="24" ry="30" fill="#3a302a" ${OUT}/>${[-14, -5, 4, 13].map((x, k) => `<path d="M${x},18v${30 + (k % 2) * 8}" stroke="${INK}" stroke-width="11" stroke-linecap="round"/><path d="M${x},18v${30 + (k % 2) * 8}" stroke="#3a302a" stroke-width="6" stroke-linecap="round"/>`).join("")}
      <path d="M-10,-6q8,-6 18,0" stroke="#5a4a40" stroke-width="3" fill="none"/></g></g>`;
  // แพร close behind the peephole: wet eyes, a cloth pressed over her mouth, hair in a messy bun, pyjamas
  const praeFace = (id) => `<g id="${id}">
      <path d="M-260,520C-250,300 -150,230 0,230C150,230 250,300 260,520Z" fill="#e7a8b8" ${OUT}/><path d="M-60,240Q0,280 60,240" stroke="#c98898" stroke-width="10" fill="none"/>
      <ellipse cx="0" cy="40" rx="150" ry="175" fill="#efc4a0" ${OUT}/>
      <path d="M-150,30C-170,-130 170,-130 150,30C140,-50 90,-80 0,-80C-90,-80 -140,-50 -150,30Z" fill="#2a1d18"/><circle cx="40" cy="-150" r="56" fill="#2a1d18"/>
      <path d="M-70,20q22,-16 44,0M26,20q22,-16 44,0" stroke="${INK}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <ellipse cx="-48" cy="34" rx="15" ry="12" fill="#fff"/><ellipse cx="48" cy="34" rx="15" ry="12" fill="#fff"/><circle cx="-46" cy="36" r="8" fill="${INK}"/><circle cx="50" cy="36" r="8" fill="${INK}"/>
      <path d="M-60,52q-6,30 -2,50M62,52q4,26 0,44" stroke="#9fd0ff" stroke-width="6" fill="none" opacity=".8" stroke-linecap="round"/>
      <path d="M-100,70C-60,60 60,60 100,70L110,160C60,190 -60,190 -110,160Z" fill="#f2efe6" ${OUT}/><path d="M-80,100h160M-90,130h180" stroke="#cfc8b8" stroke-width="4"/>
      <g transform="translate(-130,170) rotate(-20)">${Hands.fist({ r: 52 })}</g><g transform="translate(130,170) rotate(20)">${Hands.fist({ r: 52 })}</g></g>`;

  // flames licking up out of a window (top centre at x, y): three tongues, flickering (class flk)
  const flames = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})">${[[-34, 70, 0.9], [0, 110, 1], [36, 80, 0.85]].map(([dx, h, o], k) =>
    `<path class="flk" d="M${dx - 26},0C${dx - 30},${-h * 0.4} ${dx - 8},${-h * 0.6} ${dx},${-h}C${dx + 10},${-h * 0.6} ${dx + 30},${-h * 0.4} ${dx + 26},0Z" fill="url(#kwFireWin)" opacity="${o}"/>`).join("")}
    <path class="flk" d="M-20,0C-18,-30 -6,-50 0,-70C6,-50 18,-30 20,0Z" fill="#fff4c0" opacity=".9"/></g>`;

  // ---------------- the dorm from outside ----------------
  // eight floors, the seventh (from the ground) on fire: room 714 glows orange and pours smoke; o.truck adds the fire engine
  function dormExt(L, o = {}) {
    const id = o.id || "dx", r = mk(o.seed || 714);
    const X0 = 150, X1 = 930, G = 1720, FH = 150, top = G - 8 * FH;
    put(L.sky, `<rect x="-1400" y="-3200" width="3900" height="6000" fill="url(#kwNight)"/>`);
    // far city: blocks with a few lit windows, a radio mast blinking
    let far = "";
    for (let k = 0; k < 16; k++) {
      const x = -800 + k * 190 + r() * 60, w = 120 + r() * 140, h = 380 + r() * 700, y = G - 80 - h * 0.6;
      far += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="${k % 2 ? "#151b28" : "#121722"}"/>`;
      for (let j = 0; j < 9; j++) if (r() < 0.32) far += `<rect x="${f1(x + 12 + r() * (w - 30))}" y="${f1(y + 20 + r() * (h * 0.5))}" width="10" height="14" fill="#ffd58a" opacity="${(0.25 + r() * 0.5).toFixed(2)}"/>`;
    }
    far += `<path d="M1500,${G - 900}V${G - 300}M1470,${G - 300}L1500,${G - 900}L1530,${G - 300}" stroke="#1a2030" stroke-width="8" fill="none"/><circle class="led" cx="1500" cy="${G - 904}" r="7" fill="#ff4a3a"/>`;
    put(L.far, far);
    // the dorm
    let s = `<rect x="${X0 - 30}" y="${top - 40}" width="${X1 - X0 + 60}" height="${8 * FH + 40}" fill="url(#kwFacade)" ${OUT}/>`;
    s += `<rect x="${X0 + 220}" y="${top - 170}" width="340" height="110" rx="10" fill="#1d2228" ${OUT}/><text x="${X0 + 390}" y="${top - 100}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#ff7aa8" opacity=".9">หอพักสตรี ศรีเพ็ญ</text>`;
    s += `<g class="flk" opacity=".35"><text x="${X0 + 390}" y="${top - 100}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#ff9ac0" filter="url(#pvSoft)">หอพักสตรี ศรีเพ็ญ</text></g>`;
    const wins = [];
    for (let f = 0; f < 8; f++) {
      const y = G - (f + 1) * FH;
      s += `<path d="M${X0 - 30},${y + FH}H${X1 + 30}" stroke="#2a2d32" stroke-width="10"/>`;
      for (let c = 0; c < 5; c++) {
        const x = X0 + 20 + c * 152, fire = f === 6 && c === 3, smoky = f === 6 || (f === 7 && c > 1);
        const lit = !fire && r() < 0.25;
        s += `<rect x="${x}" y="${y + 26}" width="112" height="92" fill="${fire ? "url(#kwFireWin)" : lit ? "#e6c88a" : "#151a22"}" ${OUT}/>`;
        if (!fire) s += `<path d="M${x + 56},${y + 26}V${y + 118}" stroke="#3a3f46" stroke-width="5"/>${lit ? `<rect x="${x + 6}" y="${y + 32}" width="44" height="80" fill="#c99a5a" opacity=".5"/>` : ""}`;
        s += `<rect x="${x - 8}" y="${y + 116}" width="128" height="18" fill="#3a3e44" ${OUT}/>`; // balcony ledge
        if (r() < 0.3 && !fire) s += `<rect x="${x + 70}" y="${y + 70}" width="44" height="34" fill="#9aa0a6" ${OUT}/>`; // AC unit
        if (r() < 0.3 && !fire) s += `<path d="M${x + 4},${y + 40}Q${x + 56},${y + 54} ${x + 108},${y + 40}" stroke="#d8d0c0" stroke-width="3" fill="none"/>${[18, 40, 70].map((dx) => `<rect x="${x + dx}" y="${y + 44}" width="16" height="26" fill="${["#e07a8a", "#8ab0e0", "#f0e0a0"][dx % 3]}" opacity=".8"/>`).join("")}`;
        if (fire) { wins.push([x + 56, y + 72]); s += flames(x + 56, y + 30, 1.3); }
        if (smoky && !fire) s += `<rect class="flk" x="${x}" y="${y + 26}" width="112" height="92" fill="#ff7a2a" opacity="${f === 6 ? 0.35 : 0.12}"/>`;
      }
    }
    s += `<rect x="${X0 + 300}" y="${G - 130}" width="180" height="130" fill="#0e1218" ${OUT}/><rect x="${X0 + 290}" y="${G - 150}" width="200" height="24" fill="#3a3e44" ${OUT}/>`;
    // the street
    s += `<rect x="-1400" y="${G}" width="3900" height="1400" fill="#1a1c20"/><path d="M-1400,${G + 6}H2500" stroke="#3a3c40" stroke-width="10"/><path d="M-1400,${G + 220}H2500" stroke="#d8d4c0" stroke-width="6" stroke-dasharray="70 60" opacity=".4"/>`;
    [-120, 1150].forEach((x) => (s += `<path d="M${x},${G}V${G - 520}Q${x},${G - 560} ${x + 60},${G - 560}" stroke="#2a2d32" stroke-width="14" fill="none"/><ellipse cx="${x + 70}" cy="${G - 556}" rx="22" ry="9" fill="#ffe2a0"/>`));
    [[-40, G - 380], [1060, G - 360]].forEach(([x, y]) => (s += `<g>${[0, 1, 2, 3].map((k) => `<circle cx="${x + (k % 2) * 90 - 20}" cy="${y + Math.floor(k / 2) * 70}" r="${80 + k * 6}" fill="#0f1714"/>`).join("")}<rect x="${x + 16}" y="${y + 60}" width="22" height="${G - y - 60}" fill="#0f1714"/></g>`));
    put(L.set, s);
    // smoke pouring out of the seventh floor and up the face of the building
    let sm = "";
    wins.forEach(([x, y]) => {
      for (let k = 0; k < 16; k++) {
        const u = k / 16, cx = x + (r() - 0.5) * 140 + u * 180, cy = y - 60 - u * 1200, rx = 90 + u * 300;
        sm += `<g class="smk" data-d="${f1(10 + r() * 30)}"><ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(rx)}" ry="${f1(rx * 0.62)}" fill="url(#${u < 0.25 ? "pvPuffLit" : "pvPuff"})" opacity="${Math.min(1, 1.1 - u * 0.35).toFixed(2)}"/></g>`;
      }
    });
    put(L.set, sm + Pov.embers(r, { n: 26, x0: X0 + 400, x1: X0 + 760, y0: G - 7 * FH, y1: G - 6 * FH + 40, big: 7 }));
    put(L.glow, wins.map(([x, y]) => `<circle class="flk" cx="${x}" cy="${y}" r="300" fill="url(#kwFireGlow)" opacity=".9"/><rect class="flk" x="${x - 56}" y="${y - 46}" width="112" height="92" fill="#ffd27a" opacity=".55"/>`).join("") +
      [-120, 1150].map((x) => `<circle cx="${x + 70}" cy="${G - 540}" r="240" fill="url(#kwStreet)"/>`).join(""));
    if (o.truck) {
      put(L.set, `<g transform="translate(${o.truck},${G + 120})"><rect x="-260" y="-150" width="520" height="150" rx="16" fill="#c8261c" ${OUT}/><rect x="120" y="-210" width="140" height="80" rx="10" fill="#c8261c" ${OUT}/><rect x="140" y="-196" width="100" height="50" fill="#2a3644"/>
        <circle cx="-170" cy="0" r="40" fill="#1a1a1a" ${OUT}/><circle cx="170" cy="0" r="40" fill="#1a1a1a" ${OUT}/><path d="M-240,-120H90" stroke="#e8e8e8" stroke-width="10"/><rect x="-200" y="-200" width="300" height="20" fill="#9aa0a6" ${OUT}/>
        <circle class="siren" cx="150" cy="-218" r="14" fill="#ff3a3a"/><circle class="sirenb" cx="220" cy="-218" r="14" fill="#3a7aff"/></g>`);
      put(L.glow, `<circle class="siren" cx="${o.truck + 150}" cy="${G - 98}" r="260" fill="url(#kwSiren)" opacity=".7"/><circle class="sirenb" cx="${o.truck + 220}" cy="${G - 98}" r="260" fill="url(#kwSirenB)" opacity=".7"/>`);
    }
  }

  // ---------------- room 714 (the panorama) ----------------
  // o: smokeY (lower edge of the smoke, world y), gap (fire light under the door), towel (on its hook: true / in the gap: "gap"),
  // lump (someone under แพร's blanket: true), hand (a burnt hand hanging off แพร's bed), dao (ดาว sitting up, for the reveal),
  // reflect (the window glass reflects แพร's bed; "sit" shows the blanket risen), myBed (your own blanket in the foreground)
  function room(L, o = {}) {
    const id = o.id || "rm", r = mk(o.seed || 77), W0 = -400, W1 = 3700, n = ++uid;
    put(L.sky, `<rect x="-2000" y="-2000" width="7000" height="6000" fill="#0b0d0e"/>`);
    // outside the window (set layer, clipped to the glass): the block across the street, the city glow
    let city = `<rect x="2400" y="600" width="700" height="800" fill="#0c1422"/><rect x="2400" y="1150" width="700" height="250" fill="#2a2030" opacity=".8"/>`;
    for (let k = 0; k < 5; k++) { const x = 2380 + k * 150, h = 300 + r() * 400; city += `<rect x="${x}" y="${1400 - h}" width="130" height="${h}" fill="#141c2a"/>`; for (let j = 0; j < 10; j++) if (r() < 0.4) city += `<rect x="${f1(x + 10 + r() * 100)}" y="${f1(1400 - h + 20 + r() * (h - 40))}" width="12" height="16" fill="#ffd58a" opacity="${(0.3 + r() * 0.5).toFixed(2)}"/>`; }
    city += `<g class="flk" opacity=".4"><rect x="2400" y="1250" width="700" height="150" fill="#ff7a2a" opacity=".25"/></g>`;
    let s = `<defs><clipPath id="${id}-win${n}"><rect x="2440" y="660" width="600" height="680"/></clipPath></defs>`;
    // walls, ceiling, floor
    s += `<rect x="${W0}" y="${CEIL}" width="${W1 - W0}" height="${FLOOR - CEIL}" fill="url(#kwWall)"/>`;
    s += `<rect x="${W0}" y="-900" width="${W1 - W0}" height="${CEIL + 900}" fill="url(#kwCeil)"/><path d="M${W0},${CEIL}H${W1}" stroke="#151a1a" stroke-width="16"/>`;
    s += `<rect x="${W0}" y="${FLOOR}" width="${W1 - W0}" height="1400" fill="url(#kwFloor)"/>`;
    for (let x = W0; x < W1; x += 160) s += `<path d="M${x},${FLOOR}L${x + (x - 1650) * 0.9},${FLOOR + 1400}" stroke="#2a231e" stroke-width="3" opacity=".7"/>`;
    for (let k = 1; k < 9; k++) { const y = FLOOR + Math.pow(k / 9, 1.6) * 1400; s += `<path d="M${W0},${f1(y)}H${W1}" stroke="#2a231e" stroke-width="3" opacity=".7"/>`; }
    s += `<path d="M${W0},${FLOOR}H${W1}" stroke="#1a1512" stroke-width="22"/><rect x="${W0}" y="${FLOOR - 40}" width="${W1 - W0}" height="40" fill="#283231"/>`; // skirting
    s += `<rect x="${W0}" y="1080" width="${W1 - W0}" height="16" fill="#2c3736"/>`; // dado rail
    [1100, 2200].forEach((x) => (s += `<rect x="${x - 60}" y="${CEIL}" width="120" height="${FLOOR - CEIL}" fill="#000" opacity=".22"/><path d="M${x},${CEIL}V${FLOOR}" stroke="#1c2322" stroke-width="6"/>
      <path d="M${x},${CEIL}L${x + (x - 1650) * 0.25},-900M${x},${FLOOR}L${x + (x - 1650) * 0.6},${FLOOR + 1400}" stroke="#151a1a" stroke-width="6"/>`));
    // ceiling: smoke alarm (red LED), dead fluorescent tube, the fan
    s += `<g><ellipse cx="1250" cy="400" rx="70" ry="22" fill="#d8d8d0" ${OUT}/><ellipse cx="1250" cy="392" rx="52" ry="12" fill="#ecece4"/><circle class="led" cx="1276" cy="398" r="6" fill="#ff3a2a"/></g>`;
    s += `<rect x="980" y="250" width="420" height="34" rx="16" fill="#cfd4d2" ${OUT}/><rect x="980" y="244" width="420" height="12" fill="#9aa3a1"/>`;
    s += `<g transform="translate(1650,200)"><rect x="-8" y="-200" width="16" height="170" fill="#a8adaa"/><ellipse cx="0" cy="-20" rx="44" ry="20" fill="#b8bdb9" ${OUT}/>
      ${[0, 1, 2].map((k) => `<path transform="rotate(${k * 120 + 20})" d="M30,-10C150,-36 280,-30 300,0C280,30 150,30 30,10Z" fill="#c9cecb" ${OUT}/>`).join("")}<circle r="26" fill="#9aa09d" ${OUT}/></g>`;
    // ---- door wall ----
    s += `<g id="${id}-door" transform="translate(0,0)"><rect x="290" y="580" width="500" height="${FLOOR - 580}" fill="#2a1d14" ${OUT}/><rect x="306" y="596" width="468" height="${FLOOR - 600}" fill="url(#kwWood)"/>`;
    [[330, 640, 420, 360], [330, 1040, 420, 420]].forEach(([x, y, w, h]) => (s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="none" stroke="#3e2a1c" stroke-width="10"/><path d="M${x + 8},${y + 8}H${x + w - 8}" stroke="#8a6040" stroke-width="3" opacity=".5"/>`));
    s += `<circle cx="540" cy="800" r="14" fill="#1a1410" stroke="#b8a070" stroke-width="5"/><circle cx="537" cy="797" r="4" fill="#5a6070" opacity=".8"/>`; // peephole
    s += `<g id="${id}-knob"><circle cx="730" cy="1110" r="40" fill="#8a6a2a" ${OUT}/><circle cx="730" cy="1110" r="28" fill="#c9a24a" ${OUT}/><ellipse cx="720" cy="1100" rx="10" ry="7" fill="#fff4c0" opacity=".7"/></g>`;
    s += `<g><path d="M650,980L760,990" stroke="#9a9a90" stroke-width="7" stroke-dasharray="10 6"/><rect x="752" y="970" width="24" height="40" rx="4" fill="#9a9a90" ${OUT}/></g>`;
    // the old fire notice taped to the door (printed + the handwritten lines; fx can write them in: #id-hw0..2, #id-sign)
    s += noticeSvg(id, 420, 850, n) + `</g>`;
    // the towel on its hook
    if (o.towel !== "gap" && o.towel !== false) s += `<g id="${id}-towel"><circle cx="960" cy="880" r="10" fill="#9aa09d" ${OUT}/><path d="M920,890C900,1000 910,1120 930,1200H1000C1010,1120 1010,1000 1000,890Z" fill="#e8d8b8" ${OUT}/><path d="M926,1150H1004" stroke="#c9b48a" stroke-width="8"/></g>`;
    s += `<rect x="830" y="1040" width="56" height="86" rx="8" fill="#d8d8d0" ${OUT}/><rect x="846" y="1062" width="24" height="40" rx="4" fill="#b8b8b0"/>`; // light switch
    s += `<g>${[0, 1, 2].map((k) => `<path d="M${880 + k * 70},${FLOOR - 6}q30,-24 60,0z" fill="${["#e07a8a", "#8ab0e0", "#f0c060"][k]}" ${OUT}/>`).join("")}</g>`; // slippers
    if (o.towel === "gap") s += `<path id="${id}-gapcloth" d="M300,${FLOOR - 40}Q540,${FLOOR - 70} 790,${FLOOR - 40}L800,${FLOOR + 30}Q540,${FLOOR + 50} 290,${FLOOR + 30}Z" fill="#e8d8b8" ${OUT}/>`;
    // ---- แพร's wall ----
    s += `<rect x="1380" y="700" width="250" height="330" fill="#2a3a5a" ${OUT}/><circle cx="1505" cy="820" r="70" fill="#e8b8c8" opacity=".8"/><path d="M1420,1000L1500,880L1580,1000Z" fill="#f0e0a0" opacity=".6"/><text x="1505" y="980" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#fff">STAR</text>`;
    s += `<path d="M1150,640Q1650,700 2150,640" stroke="#4a4a40" stroke-width="3" fill="none"/>${Array.from({ length: 14 }, (_, k) => { const x = 1180 + k * 70, y = 640 + 60 * Math.sin((k / 13) * Math.PI); return `<circle cx="${x}" cy="${f1(y + 10)}" r="8" fill="#7a6a40"/>`; }).join("")}`;
    s += `<rect x="1720" y="860" width="360" height="20" fill="#5a4230" ${OUT}/><g transform="translate(1800,860)"><circle cy="-50" r="36" fill="#b8865a" ${OUT}/><circle cy="-100" r="28" fill="#b8865a" ${OUT}/><circle cx="-22" cy="-122" r="12" fill="#b8865a" ${OUT}/><circle cx="22" cy="-122" r="12" fill="#b8865a" ${OUT}/><circle cx="-9" cy="-104" r="3.5" fill="${INK}"/><circle cx="9" cy="-104" r="3.5" fill="${INK}"/></g>`;
    s += `${[1890, 1930, 1965, 2010].map((x, k) => `<rect x="${x}" y="${790 + k * 6}" width="${30 + k * 4}" height="${70 - k * 6}" fill="${["#c84a3a", "#3a6ac8", "#e0b040", "#4a9a6a"][k]}" ${OUT}/>`).join("")}`;
    // bed: headboard, frame, mattress, pillow, blanket (the lump), the dark under it
    s += `<rect x="1150" y="1060" width="50" height="${FLOOR - 1060}" fill="url(#kwWoodV)" ${OUT}/><rect x="1180" y="1330" width="960" height="70" fill="#5a3e2a" ${OUT}/><rect x="1190" y="1400" width="940" height="${FLOOR - 1400}" fill="#0a0806"/>`;
    s += `<rect x="1190" y="1250" width="940" height="90" rx="20" fill="#d9d4c8" ${OUT}/><ellipse cx="1300" cy="1240" rx="110" ry="40" fill="#f0ece0" ${OUT}/>`;
    s += `<g id="${id}-blanket"><path d="M1340,1330C1330,${o.lump === false ? 1300 : 1220} 1420,${o.lump === false ? 1290 : 1180} 1560,${o.lump === false ? 1290 : 1190}C1700,${o.lump === false ? 1290 : 1200} 1820,${o.lump === false ? 1300 : 1230} 2000,1260C2080,1270 2120,1300 2130,1340Z" fill="#a8586a" ${OUT}/>
      <path d="M1420,1250Q1560,1210 1700,1240M1760,1270Q1900,1250 2040,1290" stroke="#8a4456" stroke-width="6" fill="none"/></g>`;
    if (o.hand) s += `<g id="${id}-hand" transform="translate(1600,1350) rotate(0)"><g transform="scale(1.5)">${burntHand(`${id}-bh`, 1)}</g></g>`;
    if (o.dao) s += `<g id="${id}-daoat" transform="translate(1330,1300)">${daoSit(`${id}-dao`, 1.05)}</g>
      <path id="${id}-lap" d="M1250,1330C1260,1260 1400,1240 1560,1250C1700,1260 1820,1280 2000,1290C2080,1300 2120,1310 2130,1340Z" fill="#a8586a" ${OUT}/>`;
    // ---- window wall ----
    s += `<rect x="2540" y="520" width="380" height="100" rx="14" fill="#d8dcd8" ${OUT}/><path d="M2560,600H2900" stroke="#9aa09d" stroke-width="6"/>`; // AC
    if (o.sirens) city += `<rect class="siren" x="2400" y="1000" width="700" height="400" fill="url(#kwSiren)" opacity=".5"/><rect class="sirenb" x="2400" y="1000" width="700" height="400" fill="url(#kwSirenB)" opacity=".5"/>`;
    s += `<g clip-path="url(#${id}-win${n})">${city}<g id="${id}-refl" opacity="${o.reflect === false ? 0 : 0.22}">${reflection(id)}</g></g>`;
    s += `<rect x="2440" y="660" width="600" height="680" fill="url(#kwGlass)"/><path d="M2480,700L2600,660M2470,820L2700,670" stroke="#fff" stroke-width="8" opacity=".06"/>`;
    s += `<rect x="2420" y="640" width="640" height="720" fill="none" stroke="#8a9296" stroke-width="22"/><path d="M2740,650V1350" stroke="#8a9296" stroke-width="14"/><path d="M2420,640H3060" stroke="${INK}" stroke-width="4"/>`;
    s += `<path d="M2300,600H3180" stroke="#6a6a60" stroke-width="10"/>${[[2310, 2470, 1], [3010, 3170, -1]].map(([a, b, d]) => `<path d="M${a},604H${b}C${b - d * 10},900 ${b + d * 20},1200 ${b},1430H${a}C${a + d * 14},1200 ${a - d * 10},900 ${a},604Z" fill="#3a5a8a" ${OUT}/>${[0.25, 0.5, 0.75].map((u) => `<path d="M${f1(a + (b - a) * u)},610C${f1(a + (b - a) * u + 10)},900 ${f1(a + (b - a) * u - 10)},1200 ${f1(a + (b - a) * u)},1425" stroke="#2a4470" stroke-width="6" fill="none"/>`).join("")}`).join("")}`;
    s += `<rect x="2440" y="1250" width="600" height="26" fill="#6a4a32" ${OUT}/><path d="M2470,1276V${FLOOR}M3010,1276V${FLOOR}" stroke="#4a3222" stroke-width="20"/>
      <g transform="translate(2560,1250)"><rect x="-80" y="-14" width="200" height="14" rx="4" fill="#8a929a" ${OUT}/><path d="M-70,-14L-50,-130H110L130,-14Z" fill="#3a4048" ${OUT}/><circle cx="30" cy="-74" r="16" fill="#e07a8a" opacity=".7"/></g>
      <rect x="2820" y="1190" width="40" height="60" rx="6" fill="#e8e0d0" ${OUT}/><g transform="translate(2940,1250)"><path d="M-30,0L-24,-50H24L30,0Z" fill="#c86a3a" ${OUT}/><ellipse cy="-70" rx="18" ry="28" fill="#5a9a5a" ${OUT}/></g>`;
    put(L.set, s);
    // light: city/moon shaft from the window onto the floor, fire under the door, the alarm's LED
    let g = `<path d="M2440,660H3040L3500,${FLOOR + 900}H2100Z" fill="url(#kwMoonShaft)" opacity=".6"/>`;
    if (o.gap !== false) g += `<rect class="flk" x="306" y="${FLOOR - 10}" width="468" height="12" fill="#ffc06a" opacity=".95"/><rect class="flk" x="250" y="${FLOOR - 260}" width="580" height="260" fill="url(#kwGap)" opacity=".55"/>
      <ellipse class="flk" cx="540" cy="${FLOOR + 40}" rx="520" ry="120" fill="url(#kwGapPool)" opacity=".9"/>
      <g id="${id}-feet" opacity="0"><rect x="430" y="${FLOOR - 10}" width="60" height="12" fill="#1a0e08"/><rect x="560" y="${FLOOR - 10}" width="60" height="12" fill="#1a0e08"/></g>`;
    g += `<circle class="led" cx="1276" cy="398" r="40" fill="url(#kwLed)"/>`;
    put(L.glow, g);
    // smoke: the ceiling layer (its lower edge at smokeY) and wisps creeping under the door
    let sm = Pov.smoke(r, { x0: W0, x1: W1, y0: -900, y1: o.smokeY ?? 300, n: 34, lit: o.gap !== false });
    if (o.gap !== false) for (let k = 0; k < 7; k++) sm += `<g class="smk" data-d="${f1(8 + r() * 14)}"><ellipse cx="${f1(320 + r() * 440)}" cy="${f1(FLOOR - 40 - r() * 260)}" rx="${f1(80 + r() * 120)}" ry="${f1(30 + r() * 40)}" fill="url(#pvPuffLit)" opacity="${(0.35 + r() * 0.3).toFixed(2)}"/></g>`;
    put(L.set, sm);
    // foreground clutter for depth (fg layer: it slides faster than the room when the head turns, and the engine blurs it)
    put(L.fg, `<g opacity=".95"><path d="M1040,2050V1640H1180V2050M1030,1640H1190V1600H1030Z" fill="#0d0f10"/><path d="M1060,1600V1380Q1110,1350 1160,1380V1600" stroke="#0d0f10" stroke-width="22" fill="none"/>
      <path d="M2180,2100L2220,1740H2420L2460,2100Z" fill="#0d0f10"/>${[0, 1, 2].map((k) => `<path d="M${2230 + k * 70},1740Q${2250 + k * 70},1660 ${2290 + k * 70},1700" stroke="#0d0f10" stroke-width="16" fill="none"/>`).join("")}
      <path d="M-120,2100L-60,1700H120L160,2100Z" fill="#0d0f10"/></g>`);
    if (o.myBed) put(L.fg, `<path d="M-300,1760C100,1700 600,1730 1400,1690V2700H-300Z" fill="#4a6a9a" ${OUT}/><path d="M-200,1800C200,1760 700,1780 1300,1750" stroke="#3a5a88" stroke-width="12" fill="none"/>`);
  }
  // the reflection of แพร's bed in the window glass (mirrored, so the bed sits to the right): #id-rlie (the blanket lump)
  // and #id-rsit (someone sitting up under it, two ember slits for eyes; opacity 0 until fx fades it in)
  function reflection(id) {
    return `<g transform="translate(5480,0) scale(-1,1)"><rect x="2500" y="1200" width="520" height="60" fill="#d9d4c8"/>
      <path id="${id}-rlie" d="M2560,1260C2560,1200 2620,1170 2700,1170C2800,1170 2900,1190 2990,1230V1260Z" fill="#e8e0e0"/>
      <g id="${id}-rsit" opacity="0"><path d="M2560,1260C2560,1020 2620,940 2680,940C2740,940 2770,1020 2760,1180L2980,1210L2990,1260Z" fill="#e8e0e0"/>
        <ellipse cx="2680" cy="960" rx="44" ry="50" fill="#000" opacity=".75"/><path d="M2654,956q8,-5 16,0M2690,958q8,-5 16,0" stroke="#ff8a3a" stroke-width="5" stroke-linecap="round"/></g></g>`;
  }
  // the fire notice: printed rules, a floor plan, and three handwritten red lines + a signature
  function noticeSvg(id, x, y, n) {
    let p = `<g id="${id}-notice" transform="translate(${x},${y}) rotate(-1.5)"><rect x="-6" y="-6" width="262" height="362" fill="#000" opacity=".25"/><rect width="250" height="350" fill="url(#kwPaper)" ${OUT}/>
      <rect x="0" y="0" width="250" height="40" fill="#b8261c"/><text x="125" y="27" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="#fff">ข้อปฏิบัติเมื่อเกิดเพลิงไหม้</text>
      <text x="125" y="58" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="11" fill="#5a4a3a">หอพักสตรี ศรีเพ็ญ · ชั้น 7</text>`;
    ["1. ตั้งสติ อย่าตื่นตกใจ", "2. แจ้งเหตุ 199", "3. หนีไฟทางบันได", "4. ไปที่จุดรวมพล"].forEach((t, k) => (p += `<text x="16" y="${86 + k * 20}" font-family="Kanit" font-weight="400" font-size="12" fill="#3a2e24">${t}</text>`));
    p += `<g transform="translate(140,74)"><rect width="96" height="80" fill="none" stroke="#5a4a3a" stroke-width="2"/><path d="M0,40H96M48,0V80" stroke="#5a4a3a" stroke-width="1.5"/><circle cx="70" cy="60" r="5" fill="#b8261c"/><path d="M70,60L90,74" stroke="#2a8a3a" stroke-width="3"/></g>`;
    p += `<path d="M10,170H240" stroke="#8a7a60" stroke-width="1.5" stroke-dasharray="4 4"/>`;
    p += `<defs>${[0, 1, 2, 3].map((k) => `<clipPath id="${id}-hwc${k}-${n}"><rect id="${id}-hwr${k}" x="0" y="${180 + k * 42}" width="0" height="44"/></clipPath>`).join("")}</defs>`;
    ["ประตูร้อน ห้ามเปิด", "ลิฟต์มารับ ห้ามขึ้น", "ออกมาแล้ว… ห้ามกลับ"].forEach((t, k) => (p += `<g clip-path="url(#${id}-hwc${k}-${n})"><text id="${id}-hw${k}" x="${14 + k * 3}" y="${210 + k * 42}" transform="rotate(${[-2, 1.5, -1][k]} 120 ${200 + k * 42})" font-family="Kanit" font-weight="700" font-size="25" fill="#a8140c" letter-spacing="-.5">${t}</text></g>`));
    p += `<g clip-path="url(#${id}-hwc3-${n})"><text x="96" y="330" font-family="Kanit" font-weight="700" font-size="17" fill="#a8140c" transform="rotate(-4 160 325)">— ดาว 714 / 2539</text></g>`;
    p += `<path d="M-4,-4l30,8M226,-2l28,10M-2,340l26,-6" stroke="#d8d0b0" stroke-width="12" opacity=".8"/></g>`;
    return p;
  }

  // ---------------- through the peephole ----------------
  // a fisheye of the corridor: smoke, an orange glow at the far end, the green exit sign, แพร right against the door
  function peephole(L, o = {}) {
    const id = o.id || "pp", r = mk(o.seed || 31);
    put(L.sky, `<rect x="-2000" y="-2000" width="5000" height="6000" fill="#000"/>`);
    let s = `<defs><clipPath id="${id}-c"><circle cx="540" cy="900" r="430"/></clipPath></defs><g clip-path="url(#${id}-c)">
      <rect x="0" y="400" width="1080" height="1000" fill="#2a2420"/><path d="M110,470L470,820H610L970,470Z" fill="#1e1a17"/><path d="M110,1330L470,980H610L970,1330Z" fill="#3a2e24"/>
      <path d="M110,470L470,820V980L110,1330ZM970,470L610,820V980L970,1330Z" fill="#332b25"/><rect x="470" y="820" width="140" height="160" fill="#ff8a3a" class="flk" opacity=".9"/>
      ${[0, 1, 2].map((k) => `<rect x="${130 + k * 110}" y="${560 + k * 80}" width="${60 - k * 14}" height="${330 - k * 90}" fill="#4a3424" opacity=".8"/><rect x="${870 - k * 110}" y="${560 + k * 80}" width="${60 - k * 14}" height="${330 - k * 90}" fill="#4a3424" opacity=".8"/>`).join("")}
      <rect x="500" y="770" width="80" height="30" fill="#2aaa4a"/><text x="540" y="792" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="18" fill="#eaffea">EXIT</text>
      ${Pov.smoke(r, { x0: 100, x1: 980, y0: 420, y1: 860, n: 14, lit: true })}
      <g id="${id}-prae" transform="translate(540,960) scale(1.15)">${praeFace(`${id}-pf`)}</g>
      ${Array.from({ length: 6 }, () => `<g class="smk" data-d="${f1(10 + r() * 20)}"><ellipse cx="${f1(200 + r() * 680)}" cy="${f1(600 + r() * 700)}" rx="${f1(140 + r() * 140)}" ry="${f1(60 + r() * 50)}" fill="url(#pvPuff)" opacity=".45"/></g>`).join("")}
      <circle cx="540" cy="900" r="430" fill="url(#kwPeep)"/></g>
      <circle cx="540" cy="900" r="432" fill="none" stroke="#1a1612" stroke-width="18"/><circle cx="540" cy="900" r="452" fill="none" stroke="#b8a070" stroke-width="10" opacity=".35"/>
      <path d="M330,640A300,300 0 0 1 540,560" stroke="#fff" stroke-width="10" fill="none" opacity=".12" stroke-linecap="round"/>`;
    put(L.set, s);
    put(L.glow, `<circle class="flk" cx="540" cy="900" r="460" fill="url(#kwFireGlow)" opacity=".35"/>`);
  }

  // ---------------- looking down from the window ----------------
  // the face of the building drops away to the street; the fire engine pulls up, its lights wash the road; a torch answers
  function windowDown(L, o = {}) {
    const id = o.id || "wd", r = mk(o.seed || 9);
    put(L.sky, `<rect x="-2000" y="-2000" width="5000" height="6000" fill="#0a0d14"/>`);
    let s = `<path d="M-200,-200H1280L760,1500H320Z" fill="#3c4046"/>`;
    for (let k = 0; k < 7; k++) { const u = k / 7, y = -200 + Math.pow(u, 0.7) * 1700, w = 1480 - (1480 - 440) * Math.pow(u, 0.7); s += `<path d="M${f1(540 - w / 2)},${f1(y)}H${f1(540 + w / 2)}" stroke="#2a2d32" stroke-width="${f1(14 - k)}"/>`; }
    s += `<path d="M-200,-200L320,1500M1280,-200L760,1500" stroke="${INK}" stroke-width="6"/>`;
    s += `<rect x="-600" y="1500" width="2280" height="900" fill="#1a1c20"/><path d="M-600,1640H1680" stroke="#d8d4c0" stroke-width="5" stroke-dasharray="40 40" opacity=".4"/>`;
    s += `<g transform="translate(${o.truckX ?? 540},1700) scale(.42)"><rect x="-260" y="-150" width="520" height="150" rx="16" fill="#c8261c" ${OUT}/><rect x="120" y="-210" width="140" height="80" rx="10" fill="#c8261c" ${OUT}/><path d="M-240,-120H90" stroke="#e8e8e8" stroke-width="10"/><rect x="-200" y="-200" width="300" height="20" fill="#9aa0a6" ${OUT}/>
      <circle class="siren" cx="150" cy="-218" r="16" fill="#ff3a3a"/><circle class="sirenb" cx="220" cy="-218" r="16" fill="#3a7aff"/></g>`;
    [[380, 1600], [470, 1640], [640, 1610]].forEach(([x, y]) => (s += `<g transform="translate(${x},${y}) scale(.3)"><path d="M-30,0L-24,-110Q0,-130 24,-110L30,0Z" fill="#2a2a2a"/><circle cy="-140" r="24" fill="#e0c040" ${OUT}/><path d="M-28,-60H28" stroke="#e8e050" stroke-width="10"/></g>`));
    put(L.set, s + `<g id="${id}-answer" opacity="0"><circle cx="470" cy="1585" r="60" fill="url(#pvEmber)" opacity=".0"/><circle cx="470" cy="1585" r="14" fill="#fffbe8"/><circle cx="470" cy="1585" r="70" fill="#fff6dc" opacity=".25"/></g>`);
    put(L.glow, `<ellipse class="siren" cx="${(o.truckX ?? 540) + 60}" cy="1620" rx="420" ry="160" fill="url(#kwSiren)" opacity=".55"/><ellipse class="sirenb" cx="${(o.truckX ?? 540) + 90}" cy="1620" rx="420" ry="160" fill="url(#kwSirenB)" opacity=".55"/>`);
    put(L.fg, `<rect x="-300" y="-300" width="1680" height="300" fill="#8a9296"/><path d="M-300,0H1380" stroke="${INK}" stroke-width="6"/>` + Pov.smoke(r, { x0: -400, x1: 1500, y0: -600, y1: 260, n: 10 }));
  }

  // ---------------- your phone ----------------
  // o.mode: "lock" (02:03, battery 8%), "dial" (keys typed by fx: #id-d0..2), "call" (ดับเพลิง 199, a running call timer #id-ct)
  function phoneClose(L, o = {}) {
    const id = o.id || "pc", mode = o.mode || "lock";
    put(L.sky, `<rect x="-2000" y="-2000" width="5000" height="6000" fill="#0c0b0a"/>`);
    put(L.far, `<g filter="url(#pvSoft)" opacity=".7"><rect x="-200" y="200" width="1500" height="1300" fill="#2a3332"/><rect x="100" y="400" width="420" height="1100" fill="#4a3222"/><rect class="flk" x="80" y="1460" width="480" height="40" fill="#ff8a3a" opacity=".6"/><ellipse cx="900" cy="300" rx="600" ry="260" fill="#1a1816"/></g>`);
    const X = 300, Y = 360, W = 480, H = 980;
    let scr = "";
    if (mode === "lock") {
      scr = `<text x="${X + W / 2}" y="${Y + 290}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="150" fill="#f4f4f8" letter-spacing="-4">02:03</text>
        <text x="${X + W / 2}" y="${Y + 345}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="30" fill="#c8c8d8">วันเสาร์ 25 ตุลาคม</text>
        <g transform="translate(${X + 70},${Y + 470})"><rect width="${W - 140}" height="120" rx="26" fill="#ffffff" opacity=".14"/><circle cx="48" cy="60" r="24" fill="#ff5a4a"/><text x="48" y="70" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#fff">!</text>
          <text x="88" y="50" font-family="Kanit" font-weight="700" font-size="24" fill="#fff">แพร</text><text x="88" y="86" font-family="Kanit" font-weight="400" font-size="22" fill="#e8e8f0">พี่ ตื่นยัง ได้กลิ่นไหม้มั้ย</text></g>`;
    } else if (mode === "dial") {
      scr = `<text id="${id}-num" x="${X + W / 2}" y="${Y + 230}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="96" fill="#fff" letter-spacing="10"><tspan id="${id}-d0" opacity="0">1</tspan><tspan id="${id}-d1" opacity="0">9</tspan><tspan id="${id}-d2" opacity="0">9</tspan></text>`;
      const keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"];
      keys.forEach((k, i) => { const cx = X + 100 + (i % 3) * 140, cy = Y + 380 + Math.floor(i / 3) * 130; scr += `<circle id="${id}-k${k === "*" ? "s" : k === "#" ? "h" : k}" cx="${cx}" cy="${cy}" r="52" fill="#fff" opacity=".14"/><text x="${cx}" y="${cy + 16}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="46" fill="#fff">${k}</text>`; });
      scr += `<circle cx="${X + W / 2}" cy="${Y + 900}" r="52" fill="#3ac85a"/><path d="M${X + W / 2 - 20},${Y + 885}q8,30 40,32l8,-12l-14,-10l-8,6q-12,-6 -16,-18l6,-8l-10,-14z" fill="#fff"/>`;
    } else {
      scr = `<circle cx="${X + W / 2}" cy="${Y + 250}" r="90" fill="#b8261c"/><path d="M${X + W / 2},${Y + 196}c-30,40 -40,60 -40,80a40,40 0 0 0 80,0c0,-20 -10,-40 -40,-80z" fill="#ffb04a"/>
        <text x="${X + W / 2}" y="${Y + 410}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="54" fill="#fff">ดับเพลิง 199</text>
        <text id="${id}-ct" x="${X + W / 2}" y="${Y + 470}" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="34" fill="#c8f0d0">กำลังโทร…</text>
        <circle cx="${X + W / 2}" cy="${Y + 860}" r="56" fill="#e0362c"/><path d="M${X + W / 2 - 28},${Y + 860}h56" stroke="#fff" stroke-width="10" stroke-linecap="round"/>`;
    }
    put(L.set, `<g id="${id}-phone"><rect x="${X - 22}" y="${Y - 22}" width="${W + 44}" height="${H + 44}" rx="70" fill="#15171c" ${OUT}/><rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="54" fill="url(#kwScreen)"/>
      <rect x="${X + W / 2 - 60}" y="${Y + 18}" width="120" height="30" rx="15" fill="#05060a"/>
      <text x="${X + 40}" y="${Y + 46}" font-family="Kanit" font-weight="700" font-size="24" fill="#fff">02:03</text>
      <g transform="translate(${X + W - 110},${Y + 26})"><rect width="58" height="26" rx="7" fill="none" stroke="#fff" stroke-width="3"/><rect x="61" y="8" width="5" height="10" rx="2" fill="#fff"/><rect x="4" y="4" width="8" height="18" rx="3" fill="#ff4a3a"/><text x="-14" y="21" text-anchor="end" font-family="Kanit" font-weight="700" font-size="22" fill="#ff6a5a">8%</text></g>
      ${scr}<rect x="${X}" y="${Y}" width="${W}" height="${H}" rx="54" fill="none" stroke="#fff" stroke-width="2" opacity=".08"/></g>`);
    // the hand that holds it: the palm behind, four fingertips over the right edge, the thumb over the left (round, house style)
    const cap = (x, y, w, h, a) => `<g transform="translate(${x},${y}) rotate(${a})"><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="${w / 2}" fill="${Hands.SKIN}" ${OUT}/><path d="M${-w / 4},${h / 2 - 16}q${w / 4},8 ${w / 2},0" stroke="#cc9a74" stroke-width="3" fill="none"/></g>`;
    L.set.insertAdjacentHTML("afterbegin", `<path d="M${X + 40},${Y + H + 40}L${X - 140},2300H${X + 420}L${X + 320},${Y + H + 40}Z" fill="${Pov.SLEEVE}" ${OUT}/><path d="M${X + 20},${Y + H + 90}H${X + 340}" stroke="${Pov.CUFF}" stroke-width="30"/>
      <ellipse cx="${X + W / 2}" cy="${Y + H - 30}" rx="250" ry="150" fill="${Hands.SKIN}" ${OUT}/>`);
    put(L.set, [0, 1, 2, 3].map((k) => cap(X + W + 14, Y + H - 470 + k * 96, 58, 96, -8)).join("") + cap(X - 4, Y + H - 300, 62, 150, 28));
    put(L.glow, `<ellipse cx="${X + W / 2}" cy="${Y + H / 2}" rx="520" ry="760" fill="#6a8aff" opacity=".07"/>`);
  }

  // ---------------- end card: the room key tag ----------------
  function keyTag(L, o = {}) {
    const id = o.id || "kt", r = mk(o.seed || 3);
    put(L.sky, `<rect x="-2000" y="-2000" width="5000" height="6000" fill="#0d0c0b"/>`);
    put(L.far, `<rect x="-400" y="1000" width="1900" height="1400" fill="#2a1d14"/>${Array.from({ length: 8 }, (_, k) => `<path d="M-400,${1060 + k * 90}Q540,${1040 + k * 90} 1500,${1070 + k * 90}" stroke="#20160f" stroke-width="5" fill="none"/>`).join("")}`);
    put(L.set, `<g id="${id}-tag" transform="translate(540,900) rotate(-8)"><circle cx="0" cy="-330" r="70" fill="none" stroke="#b8b8b0" stroke-width="16"/><path d="M0,-260V-200" stroke="#b8b8b0" stroke-width="10"/>
        <path d="M0,-210L190,0L0,320L-190,0Z" fill="#c8261c" ${OUT}/><path d="M0,-180L160,0L0,280L-160,0Z" fill="none" stroke="#ff8a7a" stroke-width="4" opacity=".6"/><circle cx="0" cy="-170" r="14" fill="#2a1d14"/>
        <text x="0" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="120" fill="#fff4ea">714</text>
        <path d="M-120,60L-40,140M90,-40L140,30" stroke="#2a1d14" stroke-width="10" opacity=".35"/><g transform="translate(-30,-60)"><path d="M0,0q20,-30 40,0t40,0" stroke="#1a1410" stroke-width="18" fill="none" opacity=".3"/></g></g>
      <g transform="translate(540,1460) rotate(2)"><rect x="-330" y="-110" width="660" height="230" fill="url(#kwPaper)" ${OUT}/><path d="M-330,-110l40,20M330,110l-40,-16" stroke="#d8d0b0" stroke-width="14" opacity=".8"/>
        <text x="0" y="-26" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#a8140c">${o.ep || "ตอนที่ 2"}</text>
        <text x="0" y="62" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="78" fill="#a8140c">${o.title || "ลิฟต์มารับ"}</text></g>`);
    put(L.set, Pov.smoke(r, { x0: -400, x1: 1500, y0: -600, y1: 500, n: 10 }) + Pov.embers(r, { n: 18, y0: 1100, y1: 2000 }));
    put(L.glow, `<circle class="flk" cx="540" cy="1100" r="700" fill="url(#kwFireGlow)" opacity=".5"/>`);
  }

  Object.assign(Sets, { dormExt, room, peephole, windowDown, phoneClose, keyTag });
  window.Kwan = { daoSit, burntHand, praeFace, CEIL, FLOOR };
})();
