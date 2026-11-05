// ---------- ข้าวต้มตีสอง: the sets (load after kdcast.js) ----------
// Same layer contract as the other kits (sky / far / mid / set / act / fg; glow over the darkness; light = screen space).
//   Sets.kdRoom(L, o)  your rented room at 2 a.m.: dark blue wall, the window on the city, drawings pinned to a cork board,
//                      the desk (top y 1180, x 380…1100) with the laptop (screen #id-scr at 610…910 × 860…1060), the clock (o.clock "2:00");
//                      o.dawn: morning light through the window instead of the screen's glow
//   Sets.kdSoi(L, o)   the soi at night: shophouses, one streetlight (lamp at 760,330), ยายจันทร์'s porridge cart under it
//                      (cart x 300…720, wheels on y 1320), red stools at x 140/250, the chalkboard at x 930 (o.board rows, o.noBoard)
//   Sets.kdCart(L, o)  at the cart, from the stool: the pot and its steam (#id-steam), the glass case, a hanging bulb,
//                      the chalkboard at the right (#id-board…), the counter edge in fg at y 1300; o.back: the board turned round
(function () {
  const INK = "#2e2a26", DEFS = Sets.DEFS;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => { let s = seed; return () => ((s = (s * 16807) % 2147483647) / 2147483647); };
  Sets.DEFS += `<radialGradient id="kdLamp"><stop offset="0" stop-color="#ffe7a8" stop-opacity=".9"/><stop offset=".5" stop-color="#ffd27a" stop-opacity=".35"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
    <radialGradient id="kdScreen"><stop offset="0" stop-color="#bfe6ff" stop-opacity=".75"/><stop offset=".6" stop-color="#7ab8e8" stop-opacity=".22"/><stop offset="1" stop-color="#7ab8e8" stop-opacity="0"/></radialGradient>
    <linearGradient id="kdCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe7a8" stop-opacity=".55"/><stop offset="1" stop-color="#ffe7a8" stop-opacity="0"/></linearGradient>`;

  // ---------------- your room, 2 a.m. ----------------
  Sets.kdRoom = (L, o = {}) => {
    const id = o.id || "kr", r = mk(7), dawn = !!o.dawn;
    put(L.sky, `${DEFS}<rect x="-1200" y="-900" width="3500" height="4000" fill="${dawn ? "#c8b8a8" : "#141726"}"/>`);
    let s = `<rect x="-700" y="-400" width="2500" height="1920" fill="${dawn ? "#8a96b0" : "#262c44"}"/><rect x="-700" y="1500" width="2500" height="900" fill="${dawn ? "#6a5040" : "#2e2420"}"/>
      <path d="M-700,1500H1800" stroke="#1a1410" stroke-width="10"/>`;
    // the window on the city
    s += `<rect x="100" y="280" width="340" height="500" rx="6" fill="${dawn ? "#f6c8a0" : "#0c1430"}" ${O(6)}/>`;
    if (!dawn) for (let k = 0; k < 7; k++) { const bx = 120 + k * 46, bh = 120 + r() * 220;
      s += `<rect x="${f1(bx)}" y="${f1(780 - bh)}" width="40" height="${f1(bh)}" fill="#1c2440"/>`;
      for (let w = 0; w < 6; w++) if (r() > 0.55) s += `<rect x="${f1(bx + 8 + (w % 2) * 16)}" y="${f1(800 - bh + 20 + Math.floor(w / 2) * 34)}" width="8" height="12" fill="#f6d36a" opacity=".85"/>`; }
    else s += `<circle cx="300" cy="700" r="90" fill="#ffe0a0" opacity=".8"/>`;
    s += `<path d="M270,280V780M100,530H440" stroke="${INK}" stroke-width="8"/><path d="M80,270Q120,520 90,800L60,800Q80,520 40,270Z" fill="#4a3a6a" ${O(4)}/>`;
    // the cork board with drawings pinned
    s += `<rect x="540" y="280" width="420" height="330" rx="8" fill="#b88a5a" ${O(5)}/>`;
    [[580, 310, -4], [700, 300, 3], [820, 316, -2], [600, 450, 2], [730, 446, -5], [860, 460, 4]].forEach(([x, y, a], k) => {
      s += `<g transform="translate(${x},${y}) rotate(${a})"><rect x="0" y="0" width="100" height="120" fill="#fbf8f0" ${O(3)}/><circle cx="50" cy="44" r="20" fill="none" stroke="#3a5a9a" stroke-width="4"/>
        <path d="M24,96q26,-18 52,0" stroke="#3a5a9a" stroke-width="4" fill="none"/><circle cx="50" cy="-2" r="6" fill="#d8443a"/></g>`; });
    // the clock
    const hh = o.clock || "2:00", [h, m] = hh.split(":").map(Number), ah = ((h % 12) + m / 60) * 30, am = m * 6;
    s += `<g transform="translate(1000,300)"><circle r="54" fill="#e8eef4" ${O(5)}/><path d="M0,0L${f1(26 * Math.sin(ah * Math.PI / 180))},${f1(-26 * Math.cos(ah * Math.PI / 180))}M0,0L${f1(40 * Math.sin(am * Math.PI / 180))},${f1(-40 * Math.cos(am * Math.PI / 180))}" stroke="${INK}" stroke-width="6" stroke-linecap="round"/></g>`;
    // the desk, the laptop, sketchbooks, a mug
    const desk = `<rect x="380" y="1180" width="720" height="34" fill="#6a4a32" ${O(5)}/><rect x="300" y="1212" width="880" height="900" fill="#4e3624" ${O(5)}/><path d="M300,1260H1180" stroke="#3a2818" stroke-width="5"/><rect x="760" y="1300" width="300" height="160" rx="6" fill="none" stroke="#3a2818" stroke-width="5"/><circle cx="910" cy="1380" r="9" fill="#c8a060"/>
      <g transform="translate(760,1180)"><path d="M-170,0L-150,-14H150L170,0Z" fill="#9aa2ac" ${O(4)}/><rect x="-150" y="-330" width="300" height="316" rx="10" fill="#2a2e34" ${O(5)}/>
        <rect id="${id}-scr" x="-136" y="-316" width="272" height="288" rx="4" fill="${dawn ? "#2a3040" : "#a8d8f4"}"/></g>
      <g transform="translate(980,1180)"><rect x="-60" y="-26" width="120" height="26" fill="#d8443a" ${O(3)}/><rect x="-54" y="-50" width="112" height="24" fill="#3a6aa0" ${O(3)}/><rect x="-58" y="-72" width="116" height="22" fill="#f6c83a" ${O(3)}/></g>
      <g transform="translate(520,1180)"><rect x="-26" y="-62" width="52" height="62" rx="8" fill="#fbf8f0" ${O(4)}/><path d="M26,-48q22,4 0,30" stroke="${INK}" stroke-width="5" fill="none"/></g>`;
    // o.bed: a floor mattress under the window (a sleeper lies on it, the blanket over them in fg; "bare" → no blanket) · o.noDesk: no desk in front
    if (o.bed) s += `<rect x="30" y="1420" width="480" height="80" rx="14" fill="#e8e0d0" ${O(5)}/><rect x="30" y="1470" width="480" height="30" fill="#b8a888"/>
      <path d="M50,1420Q44,1384 90,1380H200Q236,1384 230,1420Z" fill="#fbf8f0" ${O(4)}/>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    if (!o.noDesk) put(L.fg, `<g id="${id}-desk">${desk}</g>`);
    if (o.bed && o.bed !== "bare") put(L.fg, `<path d="M190,1396Q300,1350 470,1380Q520,1392 516,1440H180Q166,1416 190,1396Z" fill="#6a7aa8" ${O(5)}/><path d="M220,1400Q340,1372 480,1396" stroke="#55648e" stroke-width="5" fill="none"/>`);
    if (!dawn) put(L.glow, `<ellipse cx="760" cy="980" rx="520" ry="420" fill="url(#kdScreen)" style="mix-blend-mode:screen"/>`);
    else put(L.glow, `<path d="M100,280L440,280L900,1500L-200,1500Z" fill="#ffd9a0" opacity=".25" style="mix-blend-mode:screen"/>`);
  };

  // ---------------- the soi at night, the cart under the one streetlight ----------------
  const cart = (x, y, sc = 1) => `<g transform="translate(${x},${y}) scale(${sc})">
    <circle cx="-150" cy="-30" r="34" fill="#2a2a2e" ${O(5)}/><circle cx="150" cy="-30" r="34" fill="#2a2a2e" ${O(5)}/>
    <rect x="-210" y="-300" width="420" height="250" rx="10" fill="#b8c4cc" ${O(6)}/><rect x="-200" y="-290" width="400" height="30" fill="#8a96a0"/>
    <rect x="-196" y="-250" width="392" height="120" rx="6" fill="#f4ecd8" ${O(4)}/>
    <text x="0" y="-198" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#c8302a">ข้าวต้มยายจันทร์</text>
    <text x="0" y="-148" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="26" fill="#2e2a26">เปิดตีหนึ่ง – ตีสี่</text>
    <rect x="-200" y="-470" width="400" height="170" fill="#cfe4ec" opacity=".55" ${O(4)}/><path d="M-200,-470H200" stroke="${INK}" stroke-width="6"/>
    <path d="M-120,-300Q-128,-400 -40,-404H60Q130,-400 120,-300Z" fill="#c8ccd2" ${O(5)}/><rect x="-130" y="-410" width="260" height="20" rx="8" fill="#a8acb2" ${O(4)}/>
    ${[100, 150].map((bx) => `<path d="M${bx - 22},-300Q${bx},-276 ${bx + 22},-300Z" fill="#fbf8f0" ${O(3)}/>`).join("")}</g>`;
  const stool = (x, y, sc = 1) => `<g transform="translate(${x},${y}) scale(${sc})"><path d="M-46,-110H46L36,0H-36Z" fill="#d8443a" ${O(4)}/><ellipse cx="0" cy="-110" rx="50" ry="12" fill="#e8584a" ${O(4)}/></g>`;
  Sets.kdSoi = (L, o = {}) => {
    const id = o.id || "ks", r = mk(13);
    put(L.sky, `${DEFS}<defs><linearGradient id="${id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1024"/><stop offset="1" stop-color="#2a2440"/></linearGradient></defs>
      <rect x="-1400" y="-1000" width="3900" height="4200" fill="url(#${id}-sky)"/>`);
    let far = "";
    for (let k = 0; k < 9; k++) { const x = -600 + k * 280, h = 700 + r() * 240;
      far += `<rect x="${f1(x)}" y="${f1(1320 - h)}" width="260" height="${f1(h)}" fill="#1a1c2c"/><rect x="${f1(x + 20)}" y="${f1(1320 - 260)}" width="220" height="240" fill="#2a2c3c"/>
        ${[0, 1, 2, 3, 4, 5, 6, 7].map((w) => `<path d="M${f1(x + 24)},${f1(1320 - 250 + w * 30)}H${f1(x + 236)}" stroke="#20222e" stroke-width="5"/>`).join("")}`;
      if (r() > 0.5) far += `<rect x="${f1(x + 70)}" y="${f1(1320 - h + 80)}" width="40" height="50" fill="#f6d36a" opacity=".5"/>`; }
    far += `<path d="M-700,420Q540,480 1800,400M-700,450Q540,520 1800,430" stroke="#0a0a14" stroke-width="4" fill="none"/>`;
    put(L.far, far);
    let s = `<rect x="-800" y="1320" width="2700" height="1000" fill="#2a2a32"/><rect x="-800" y="1300" width="2700" height="26" fill="#4a4a52"/>
      <path d="M-800,1700H1900" stroke="#f4ecd8" stroke-width="10" stroke-dasharray="70 60" opacity=".35"/>
      <rect x="852" y="300" width="16" height="1020" fill="#3a3a44" ${O(3)}/><path d="M860,310Q860,290 780,300" stroke="#3a3a44" stroke-width="14" fill="none"/>
      <path d="M720,296H800L790,330H730Z" fill="#e8e0c0" ${O(3)}/>`;
    s += cart(510, 1320) + stool(140, 1320) + stool(260, 1320);
    if (!o.noBoard) s += `<g transform="translate(930,1320)"><g transform="translate(0,-330) scale(0.62)">${KD.board(0, 0, 1, { id: `${id}-bd`, rows: o.board || ["กินให้อิ่มก่อน แล้วค่อยคิด", "ห้ามตัดสินใจตอนตีสอง", "นับสิ่งที่ทำได้แล้ว"] })}</g></g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.glow, `<path d="M730,330L790,330L1160,1330L260,1330Z" fill="url(#kdCone)" style="mix-blend-mode:screen"/><circle cx="760" cy="330" r="160" fill="url(#kdLamp)"/>`);
    put(L.mid, `<g id="${id}-steam">${KD.steam(500, 900, 1.0, `${id}-st`)}</g>`);
  };

  // ---------------- at the cart, from the stool ----------------
  Sets.kdCart = (L, o = {}) => {
    const id = o.id || "kc";
    put(L.sky, `${DEFS}<rect x="-1200" y="-900" width="3500" height="4000" fill="#100e18"/>`);
    let s = `<rect x="-700" y="-400" width="2500" height="1300" fill="#1a1828"/>
      <path d="M540,-400V200" stroke="#2e2a26" stroke-width="6"/><path d="M500,200H580L570,250H510Z" fill="#e8e0c0" ${O(4)}/>
      <rect x="-60" y="560" width="1200" height="380" fill="#cfe4ec" opacity=".35" ${O(5)}/>
      <path d="M420,940Q410,700 560,690H760Q910,700 900,940Z" fill="#c8ccd2" ${O(6)}/><rect x="396" y="672" width="528" height="40" rx="16" fill="#a8acb2" ${O(5)}/>
      <rect x="-60" y="940" width="1200" height="360" fill="#b8c4cc" ${O(6)}/>`;
    s += `<g transform="translate(1060,820)">${o.back ? KD.board(0, 0, 0.9, { id: `${id}-board`, back: true }) : KD.board(0, 0, 0.9, { id: `${id}-board`, rows: o.board || ["กินให้อิ่มก่อน แล้วค่อยคิด", "ห้ามตัดสินใจตอนตีสอง", "นับสิ่งที่ทำได้แล้ว"] })}</g>`;
    put(L.set, `<g id="${id}-world">${s}</g>`);
    put(L.mid, `<g id="${id}-steam">${KD.steam(660, 660, 1.4, `${id}-st`)}</g>`);
    put(L.fg, `<rect x="-900" y="1300" width="2900" height="700" fill="#8a96a0" ${O(6)}/><rect x="-900" y="1290" width="2900" height="26" fill="#b8c4cc" ${O(5)}/>`);
    put(L.glow, `<circle cx="540" cy="250" r="700" fill="url(#kdLamp)" opacity=".7" style="mix-blend-mode:screen"/>`);
  };
})();
