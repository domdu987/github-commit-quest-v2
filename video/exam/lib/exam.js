// "ห้องสอบ" world (lane C): a Thai secondary-school classroom (ม.3/4) on a midterm-exam morning when the dead come up the corridor.
// House style (ทะเลลด / เห็ดปอบ): layered depth, light from the corridor windows on the left, contact shadows, dust in the light.
//   Sets.examRoom(L, o)   the classroom from the front corner: rows of wooden desks with exam papers, the whiteboard ("สอบกลางภาค
//                         คณิตศาสตร์ ม.3/4"), the wall clock (#id-min / #id-hr hands), the side door with its narrow glass panel
//                         (#id-door, glass #id-glass), the back door (#id-bdoor, latch #id-latch hanging loose), the steel cabinet
//                         at the back with a pair of EXTRA student shoes under it (the planted clue, #id-shoes), windows, fans,
//                         the roll list on the teacher's desk ("30 คน"). o.dark 0..1 = lights off · o.desk "front" | "door"
//                         (teacher's desk pushed against the back door) · o.cab "shut" | "open" (empty, a misted handprint inside)
//   Sets.examDoor(L, o)   inside, close on the side door: the glass panel at eye level (#id-face = a zombie face pressed to it,
//                         o.face true), the door's lock knob (#id-knob), the light switch on the wall (#id-sw). o.dark
//   Sets.examHall(L, o)   the corridor outside: room signs 3/1 3/2 3/3 3/4 (#id-sign0..3), lockers, windows, notice board,
//                         o.time day · o.dark 0..1
//   Sets.examCab(L, o)    insert at floor level: the cabinet's base and the extra pair of shoes (o.shoes), o.open, o.print
//   Exam.phone(x, y, s, o)  a phone in a hand (screen: o.screen "cam" | "mom" | "off")
//   Exam.clock(x, y, s, id) the wall clock (#id-min #id-hr) · Exam.life(tl, id, t0, dur) fans, dust, the clock ticking
(function () {
  const { mk, f1, put, tuft } = Pop2;
  const INK = "#2a2420";
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const E = (window.Exam = window.Exam || {});
  Sets.DEFS += `
    <linearGradient id="exWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4ecd6"/><stop offset="1" stop-color="#e2d4b2"/></linearGradient>
    <linearGradient id="exFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8b898"/><stop offset="1" stop-color="#9a8a6a"/></linearGradient>
    <linearGradient id="exBoard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#eef2f4"/><stop offset="1" stop-color="#d8dee2"/></linearGradient>
    <linearGradient id="exDesk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8a868"/><stop offset="1" stop-color="#b07e44"/></linearGradient>
    <linearGradient id="exSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a9aa4"/><stop offset=".45" stop-color="#c8d4da"/><stop offset="1" stop-color="#7a8a94"/></linearGradient>
    <linearGradient id="exGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfe6f0" stop-opacity=".85"/><stop offset=".5" stop-color="#a8c8d8" stop-opacity=".7"/><stop offset="1" stop-color="#e8f4fa" stop-opacity=".85"/></linearGradient>
    <linearGradient id="exRay" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff4d8" stop-opacity=".5"/><stop offset="1" stop-color="#fff4d8" stop-opacity="0"/></linearGradient>
    <radialGradient id="exAO"><stop offset="0" stop-color="#1a120c" stop-opacity=".55"/><stop offset=".7" stop-color="#1a120c" stop-opacity=".18"/><stop offset="1" stop-color="#1a120c" stop-opacity="0"/></radialGradient>
    <radialGradient id="exPhone"><stop offset="0" stop-color="#d8ecff" stop-opacity=".9"/><stop offset=".4" stop-color="#9cc4ff" stop-opacity=".35"/><stop offset="1" stop-color="#9cc4ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="exEye"><stop offset="0" stop-color="#f4ffe8"/><stop offset=".4" stop-color="#c8f0b0" stop-opacity=".8"/><stop offset="1" stop-color="#9ae080" stop-opacity="0"/></radialGradient>
    <radialGradient id="exZskin" cx=".45" cy=".4"><stop offset="0" stop-color="#b8c6ae"/><stop offset=".7" stop-color="#8fa088"/><stop offset="1" stop-color="#6e7e68"/></radialGradient>`;

  // ---------------- props ----------------
  E.clock = (x, y, s, id) => `<g transform="translate(${x},${y}) scale(${s})"><circle r="78" fill="#2a2a30" ${O(4)}/><circle r="66" fill="#fbfaf4"/>
    ${Array.from({ length: 12 }, (_, k) => `<path d="M0,-60V${k % 3 ? -54 : -48}" stroke="${INK}" stroke-width="${k % 3 ? 3 : 6}" transform="rotate(${k * 30})"/>`).join("")}
    <g id="${id}-hr"><path d="M0,6V-34" stroke="${INK}" stroke-width="8" stroke-linecap="round" transform="rotate(${10 * 30 + 40 * 0.5})"/></g>
    <g id="${id}-min"><path d="M0,8V-52" stroke="${INK}" stroke-width="5" stroke-linecap="round" transform="rotate(${40 * 6})"/></g>
    <g id="${id}-sec"><path d="M0,10V-56" stroke="#d8392e" stroke-width="2.5" stroke-linecap="round"/></g><circle r="6" fill="#d8392e"/><path d="M-40,-48Q0,-70 40,-48" stroke="#fff" stroke-width="6" fill="none" opacity=".6"/></g>`;
  E.phone = (x, y, s, o = {}) => {
    const sc = o.screen || "cam";
    const scr = sc === "mom" ? `<rect x="-44" y="-86" width="88" height="172" rx="10" fill="#1e3a5a"/><circle cy="-30" r="22" fill="#f2c8a8"/><path d="M-26,8q26,-20 52,0v12h-52Z" fill="#f2c8a8"/><text y="44" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#fff">แม่</text>
      <circle cx="-22" cy="70" r="12" fill="#e2382e"/><circle cx="22" cy="70" r="12" fill="#2fa864"/>`
      : sc === "cam" ? `<rect x="-44" y="-86" width="88" height="172" rx="10" fill="#26303a"/><rect x="-36" y="-70" width="72" height="120" fill="#5a7080"/><circle cy="70" r="11" fill="#fff" stroke="#e2382e" stroke-width="4"/><text x="-30" y="-74" font-family="Kanit" font-weight="800" font-size="13" fill="#e2382e">● REC</text>`
      : `<rect x="-44" y="-86" width="88" height="172" rx="10" fill="#0e1014"/>`;
    return `<g transform="translate(${x},${y}) scale(${s}) rotate(${o.rot || 0})">${sc !== "off" ? `<circle r="260" fill="url(#exPhone)" opacity=".6"/>` : ""}<rect x="-52" y="-96" width="104" height="192" rx="16" fill="#1a1c22" ${O(4)}/>${scr}<rect x="-14" y="-92" width="28" height="5" rx="2" fill="#3a3c44"/></g>`;
  };
  // a zombie face pressed to glass: grey-green, milky glowing eyes, mouth open, no blood
  E.face = (x, y, s, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>
    <path d="M-90,-40Q-96,-150 0,-160Q96,-150 90,-40Q86,60 40,100Q0,118 -40,100Q-86,60 -90,-40Z" fill="url(#exZskin)" ${O(4)}/>
    <path d="M-96,-90Q-60,-176 10,-170Q80,-170 98,-96Q70,-140 20,-140Q-40,-150 -96,-90Z" fill="#1e1a18" ${O(3)}/>
    <path d="M-50,-60q20,-12 40,0M10,-60q20,-12 40,0" stroke="#3a4030" stroke-width="5" fill="none"/>
    <ellipse cx="-30" cy="-34" rx="22" ry="16" fill="#e8f0dc" ${O(3)}/><ellipse cx="30" cy="-34" rx="22" ry="16" fill="#e8f0dc" ${O(3)}/>
    <circle cx="-30" cy="-34" r="26" fill="url(#exEye)" opacity=".7"/><circle cx="30" cy="-34" r="26" fill="url(#exEye)" opacity=".7"/>
    <path d="M-36,40Q0,20 36,40Q30,86 0,88Q-30,86 -36,40Z" fill="#2a1a1a" ${O(3)}/><path d="M-26,40h52" stroke="#d8d4c0" stroke-width="7"/>
    <path d="M-70,10q10,24 4,40M66,0q-8,30 2,48M-10,-120q-6,20 4,30" stroke="#5a6a50" stroke-width="3" fill="none" opacity=".6"/>
    <ellipse cx="0" cy="40" rx="110" ry="140" fill="#fff" opacity=".07"/></g></g>`;
  const desk = (x, y, s, paper = true, chair = true) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cy="8" rx="150" ry="18" fill="url(#exAO)"/>
    ${chair ? `<g transform="translate(0,90)"><path d="M-60,0V-110M60,0V-110" stroke="#5a6a7a" stroke-width="8"/><rect x="-70" y="-120" width="140" height="18" rx="4" fill="#d8a868" ${O(2.5)}/></g>` : ""}
    <path d="M-120,0V-150M120,0V-150" stroke="#5a6a7a" stroke-width="9"/><path d="M-110,-60H110" stroke="#5a6a7a" stroke-width="6"/>
    <path d="M-134,-176H134L126,-150H-126Z" fill="url(#exDesk)" ${O(3)}/><rect x="-134" y="-190" width="268" height="16" rx="3" fill="#e8b878" ${O(3)}/>
    ${paper ? `<g transform="translate(-10,-194) skewX(-20)"><rect x="-50" y="-10" width="100" height="10" fill="#fbfaf4" ${O(1.5)}/></g><path d="M50,-196l40,-6" stroke="#2a5ab8" stroke-width="5" stroke-linecap="round"/>` : ""}</g>`;
  const shoes = (x, y, s, id) => `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}">${[-34, 34].map((dx) => `<g transform="translate(${dx},0)"><path d="M-28,0Q-30,-26 -10,-30H16Q34,-26 34,-8V0Z" fill="#1a1a1e" ${O(3)}/><path d="M-26,-4H32" stroke="#f4f4f4" stroke-width="5"/><path d="M-10,-24q10,-6 20,0" stroke="#f4f4f4" stroke-width="3" fill="none"/><path d="M-20,-22q6,-4 12,0" stroke="#fff" stroke-width="3" opacity=".5"/></g>`).join("")}</g></g>`;
  // the steel cabinet at the back: double doors; o.open shows it empty with a misted handprint on the inside of the door
  const cabinet = (x, G, s, id, o = {}) => `<g transform="translate(${x},${G}) scale(${s})"><ellipse cy="6" rx="190" ry="20" fill="url(#exAO)"/>
    <rect x="-160" y="-520" width="320" height="490" rx="6" fill="url(#exSteel)" ${O(4)}/><rect x="-160" y="-30" width="320" height="30" fill="#5a6a74" ${O(3)}/>
    ${o.open ? `<rect x="-150" y="-510" width="300" height="470" fill="#1a1e24"/><path d="M-150,-300H150" stroke="#3a4048" stroke-width="6"/>
      <path d="M-160,-520L-300,-500V-50L-160,-30Z" fill="#a8b8c0" ${O(4)}/><g opacity=".5" fill="#fff"><ellipse cx="-236" cy="-300" rx="26" ry="32"/>${[-26, -12, 2, 16].map((dx, k) => `<ellipse cx="${-236 + dx}" cy="${-346 - (k % 2) * 6}" rx="6" ry="14"/>`).join("")}</g>`
    : `<path d="M0,-520V-30" stroke="${INK}" stroke-width="3"/><rect x="-18" y="-300" width="10" height="40" rx="3" fill="#5a6a74"/><rect x="8" y="-300" width="10" height="40" rx="3" fill="#5a6a74"/>${o.ajar ? `<path d="M0,-520L22,-516V-34L0,-30Z" fill="#0e1014"/>` : ""}
      ${Array.from({ length: 6 }, (_, k) => `<path d="M-140,${-480 + k * 14}H-30M30,${-480 + k * 14}H140" stroke="#7a8a94" stroke-width="3"/>`).join("")}`}
    <path d="M-150,-516V-40" stroke="#fff" stroke-width="6" opacity=".35"/></g>`;
  const door = (x, G, s, id, o = {}) => `<g transform="translate(${x},${G}) scale(${s})"><rect x="-130" y="-560" width="260" height="560" fill="#6a4a30" ${O(4)}/>
    <g id="${id}-door"><rect x="-116" y="-546" width="232" height="546" fill="#a8784a" ${O(3)}/><path d="M-100,-530V-16M100,-530V-16" stroke="#8a6040" stroke-width="3" opacity=".6"/>
      <g id="${id}-glass"><rect x="-40" y="-470" width="80" height="210" fill="url(#exGlass)" ${O(3)}/><path d="M-30,-460l30,-0M-34,-440l50,0" stroke="#fff" stroke-width="4" opacity=".6"/></g>
      ${o.face ? `<g clip-path="url(#${id}-gclip)">${E.face(0, -350, 0.42, `${id}-face`)}</g>` : ""}
      <g id="${id}-knob"><circle cx="90" cy="-270" r="16" fill="#d8c060" ${O(3)}/></g><rect x="78" y="-246" width="24" height="16" rx="3" fill="#8a8a8a" ${O(2)}/></g>
    <text y="-590" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#2c5a8a">${o.sign || "ม.3/4"}</text></g>`;

  // ---------------- Sets.examRoom ----------------
  function examRoom(L, o = {}) {
    const id = o.id || "er", r = mk(o.seed || 11), G = 1500, dark = o.dark || 0;
    put(L.mid, `<rect x="-1400" y="200" width="3900" height="900" fill="#bcd8ec"/><path d="M-1400,900Q0,860 2500,900V1100H-1400Z" fill="#7aa86a"/>`);
    let s = `<rect x="-1400" y="-900" width="3900" height="${G + 900}" fill="url(#exWall)"/>`;
    // windows on the left wall (with the sky in L.mid showing through holes)
    s = `<path d="M-1400,-900H2500V${G}H-1400Z M-1240,330H-640V1000H-1240Z M-520,330H80V1000H-520Z" fill="url(#exWall)" fill-rule="evenodd"/>`;
    s += [[-1240], [-520]].map(([x]) => `<rect x="${x}" y="330" width="600" height="670" fill="none" stroke="#3d78a8" stroke-width="18"/><path d="M${x + 300},330V1000M${x},660H${x + 600}" stroke="#3d78a8" stroke-width="10"/>`).join("");
    s += `<rect x="-1400" y="${G - 300}" width="3900" height="300" fill="#c8b48a" opacity=".55"/><path d="M-1400,${G - 300}H2500" stroke="#3d78a8" stroke-width="10"/>`;
    s += `<rect x="-1400" y="${G}" width="3900" height="1400" fill="url(#exFloor)"/>` + Array.from({ length: 16 }, (_, k) => `<path d="M-1400,${G + 10 + k * k * 5}H2500" stroke="#8a7a5a" stroke-width="2" opacity=".45"/>`).join("") +
      Array.from({ length: 24 }, (_, k) => `<path d="M${-1400 + k * 170},${G}L${-1400 + k * 170 + (k * 170 - 1950) * 0.6},${G + 1400}" stroke="#8a7a5a" stroke-width="2" opacity=".3"/>`).join("") + `<path d="M-1400,${G}H2500" stroke="#6a5a40" stroke-width="6"/>`;
    // whiteboard + exam title, the clock above it
    s += `<g transform="translate(560,620)"><rect x="-520" y="-240" width="1040" height="480" rx="10" fill="#9aa4aa" ${O(5)}/><rect x="-500" y="-220" width="1000" height="440" fill="url(#exBoard)"/>
      <text x="-460" y="-120" font-family="Mali" font-weight="700" font-size="70" fill="#2a4a9a">สอบกลางภาค</text><text x="-460" y="-20" font-family="Mali" font-weight="700" font-size="60" fill="#d8392e">คณิตศาสตร์ ม.3/4</text>
      <text x="-460" y="80" font-family="Mali" font-weight="700" font-size="48" fill="#2a2a2a">10:00 – 11:30 น. · ห้ามคุยกัน</text><rect x="-500" y="220" width="1000" height="22" fill="#7a848a"/></g>`;
    s += E.clock(1230, 330, 1.0, id);
    // the side door (front right) with its glass panel, the back door far left at the back wall, the cabinet
    s += `<clipPath id="${id}-gclip"><rect x="-40" y="-470" width="80" height="210"/></clipPath>`;
    s += door(1300, G - 40, 1.05, id, { face: o.face });
    s += `<g id="${id}-bdoorg">${door(-1100, G - 40, 0.9, `${id}b`, { sign: "ทางออก" })}</g><g id="${id}-latch" transform="translate(-1030,${G - 330})"><rect x="-6" y="-4" width="40" height="10" fill="#9a9a9a" ${O(2)} transform="rotate(30)"/></g>`;
    s += cabinet(-640, G - 20, 0.95, id, { open: o.cab === "open", ajar: o.cab === "ajar" });
    if (o.shoes !== false && o.cab !== "open") s += shoes(-640, G - 20, 0.9, `${id}-shoes`);
    // rows of desks receding (3 rows), exam papers, bags hanging, the teacher's desk + roll list
    const rows = [[1620, 1.0], [1760, 1.08], [1920, 1.18]];
    rows.forEach(([y, sc], k) => { for (let c = 0; c < 4; c++) s += desk(-560 + c * 430 + (k % 2) * 40, y, sc); });
    const tdx = o.desk === "door" ? -1080 : 1060, tdy = o.desk === "door" ? G - 20 : 1480;
    s += `<g id="${id}-tdesk" transform="translate(${tdx},${tdy})"><ellipse cy="8" rx="240" ry="24" fill="url(#exAO)"/><rect x="-220" y="-230" width="440" height="230" fill="#8a5a34" ${O(4)}/><rect x="-236" y="-256" width="472" height="30" fill="#b07e44" ${O(4)}/>
      <g transform="translate(-120,-262)"><rect x="-60" y="-14" width="120" height="14" fill="#fbfaf4" ${O(2)}/><text x="-50" y="-18" font-family="Kanit" font-weight="800" font-size="20" fill="#2a2a2a">รายชื่อ 30 คน</text></g>
      <path d="M60,-262l50,-10" stroke="#d8392e" stroke-width="7" stroke-linecap="round"/></g>`;
    // ceiling fans, fluorescent tubes (on/off)
    s += [-200, 900].map((x) => `<g transform="translate(${x},40)"><path d="M0,-200V-20" stroke="#5a5a5a" stroke-width="8"/><ellipse rx="30" ry="14" fill="#d8d4c8" ${O(3)}/><g class="exfan"><path d="M-20,0L-240,22L-240,6Z M20,0L240,-6L240,14Z" fill="#c8c4b8" ${O(3)}/></g></g>`).join("");
    s += [-500, 400, 1300].map((x) => `<g transform="translate(${x},-120)"><rect x="-150" y="-12" width="300" height="24" rx="10" fill="${dark ? "#8a8a8a" : "#fbfff8"}" ${O(3)}/></g>`).join("");
    put(L.set, s);
    put(L.glow, `<path d="M-1240,330H-640L-200,${G + 300}H-1300Z M-520,330H80L520,${G + 300}H-420Z" fill="url(#exRay)" opacity="${f1(0.55 * (1 - dark))}"/>`);
    if (dark) put(L.glow, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0e1c" opacity="${f1(dark * 0.55)}"/>`);
  }

  // ---------------- Sets.examDoor: close on the side door from inside ----------------
  function examDoor(L, o = {}) {
    const id = o.id || "ed", G = 1700, dark = o.dark || 0;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="url(#exWall)"/>`);
    let s = `<rect x="-1400" y="${G}" width="3900" height="700" fill="url(#exFloor)"/><path d="M-1400,${G - 280}H2500" stroke="#3d78a8" stroke-width="12"/><rect x="-1400" y="${G - 280}" width="3900" height="280" fill="#c8b48a" opacity=".5"/>`;
    s += `<clipPath id="${id}-gclip"><rect x="-40" y="-470" width="80" height="210"/></clipPath>`;
    s += `<g transform="translate(540,0)">${door(0, G, 2.2, id, { face: o.face })}</g>`;
    s += `<g transform="translate(980,${G - 820})"><g id="${id}-sw"><rect x="-40" y="-60" width="80" height="120" rx="10" fill="#f4f2ea" ${O(3)}/><rect x="-14" y="-34" width="28" height="40" rx="5" fill="${dark ? "#c8c4b8" : "#e8e4d8"}" ${O(2)}/></g></g>`;
    put(L.set, s);
    if (dark) put(L.glow, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0e1c" opacity="${f1(dark * 0.6)}"/>`);
  }

  // ---------------- Sets.examHall: the corridor ----------------
  function examHall(L, o = {}) {
    const id = o.id || "eh", r = mk(o.seed || 21), G = 1450, dark = o.dark || 0;
    put(L.mid, `<rect x="-1400" y="0" width="3900" height="1100" fill="#bcd8ec"/><path d="M-1400,800Q500,760 2500,800V1100H-1400Z" fill="#7aa86a"/>`);
    let s = `<path d="M-1400,-900H2500V${G}H-1400Z M-1300,250H-900V800H-1300Z M-500,250H-100V800H-500Z M300,250H700V800H300Z M1100,250H1500V800H1100Z M1900,250H2300V800H1900Z" fill="#e8dcbc" fill-rule="evenodd"/>`;
    s += `<rect x="-1400" y="${G}" width="3900" height="700" fill="#b8a88a"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-1400 + k * 140},${G}L${-1400 + k * 140 - 200},${G + 700}" stroke="#a8987a" stroke-width="3"/>`).join("")}`;
    s += `<rect x="-1400" y="${G - 260}" width="3900" height="260" fill="#c8b48a" opacity=".6"/>`;
    ["3/1", "3/2", "3/3", "3/4"].forEach((t, k) => {
      const x = -1100 + k * 800;
      s += `<g transform="translate(${x},${G})"><rect x="-120" y="-540" width="240" height="540" fill="#a8784a" ${O(4)}/><rect x="-36" y="-460" width="72" height="190" fill="url(#exGlass)" ${O(3)}/>
        <g id="${id}-sign${k}"><rect x="-90" y="-640" width="180" height="70" rx="8" fill="#2c5a8a" ${O(3)}/><text y="-590" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#fff">ม.${t}</text></g></g>`;
    });
    s += `<g transform="translate(-700,${G - 600})"><rect x="-130" y="-100" width="260" height="200" fill="#c86a3a" ${O(3)}/><rect x="-110" y="-80" width="70" height="90" fill="#fbf4e2" transform="rotate(-4)"/><rect x="-20" y="-70" width="60" height="70" fill="#e8f0ff" transform="rotate(5)"/><rect x="50" y="-60" width="50" height="100" fill="#fff0a0"/></g>`;
    put(L.set, s);
    put(L.glow, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0e1c" opacity="${f1(dark * 0.55)}"/>`);
  }

  // ---------------- Sets.examCab: floor-level insert ----------------
  function examCab(L, o = {}) {
    const id = o.id || "ec";
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="2900" fill="url(#exWall)"/>`);
    let s = `<rect x="-1400" y="1300" width="3900" height="900" fill="url(#exFloor)"/>`;
    s += cabinet(540, 1320, 2.6, id, { open: o.open, ajar: !o.open });
    if (o.shoes !== false && !o.open) s += shoes(540, 1316, 2.4, `${id}-shoes`);
    put(L.set, s);
    put(L.glow, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0e1c" opacity="${f1((o.dark || 0) * 0.55)}"/>`);
  }

  E.life = (tl, id, t0, dur) => {
    document.querySelectorAll(".exfan").forEach((f) => tl.fromTo(f, { rotation: 0 }, { rotation: 360 * dur * 0.6, svgOrigin: "0 0", duration: dur, ease: "none", immediateRender: false }, t0));
    const sec = document.getElementById(`${id}-sec`);
    if (sec) for (let k = 0; k < Math.ceil(dur); k++) tl.to(sec, { rotation: (k + 1) * 6, svgOrigin: "0 0", duration: 0.12, ease: "back.out(3)", immediateRender: false }, t0 + k);
  };
  Object.assign(Sets, { examRoom, examDoor, examHall, examCab });
})();
