// ---------- ถูกหวยทั้งบ้าน (lane A, storytelling): the family, their props and the inserts ----------
// Load after rig2.js, mmcast.js and rabcast.js (the family is dressed from those bodies).
//   Rig.CAST.lotYou   "คุณ" ~24: undercut, navy tee, grey shorts · lotYouMask (surgical mask) · lotYouPhone / lotYouTicket (hand F)
//   Rig.CAST.lotMom   แม่ 50: low bun, rose blouse, sarong · lotMomPhone · lotMomMask
//   Rig.CAST.lotSri   ป้าศรี 56: curls, yellow blouse · lotSriPhone (the gossip line is always open)
//   Rig.CAST.lotMan   ลุงหมาน 60: balding, teal "business" shirt, glasses on the forehead · lotManSun (dark glasses indoors)
//   Rig.CAST.lotBeer  เบียร์ 25: bowl cut, red football shirt no. 10 · lotBeerTicket (a ticket edge in the back hand, EP.1 clue)
//   Rig.CAST.lotBoon  ยายบุญ 72: grey bun, lace blouse, ผ้าขาวม้า
//   Lot.ticket(x, y, s, o)      the lottery ticket (generic: no emblem), o.num "386521", o.ids → #id-d0..d5 per digit
//   Lot.result(o)              phone screen content (272×540): the draw result, digits #id-r0..r5
//   Lot.call(o)                phone screen content: the incoming call from ป้าแจ๋ว
//   Lot.calendar(x, y, s, o)   the kitchen wall calendar, grandma's six red digits across the top (o.id → #id-red)
//   Lot.sign(x, y, s, o)       the old wooden sign on a string: "ถูกเลขยาย แบ่งยายครึ่ง" (o.id → #id-swing, origin at the nail)
//   Lot.think(x, y, s, inner)  a thought cloud with three trailing puffs (origin at the last puff)
//   Lot.tag(x, y, text, o)     a name tag: a tape strip with the name in marker
//   Lot.NUM                    the winning number
(function () {
  const C = Rig.CAST, LINE = Rig2.LINE, INK = "#2e2a26";
  const f1 = (v) => (+v).toFixed(1);
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const T = (x, y, size, text, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 900}" font-size="${size}" fill="${o.fill || INK}"${o.ls ? ` letter-spacing="${o.ls}"` : ""}${o.op ? ` opacity="${o.op}"` : ""}>${text}</text>`;
  const at = (x, y, s, svg, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s})">${svg}</g>`;
  const NUM = "386521";

  // ---------------- faces ----------------
  const MASK = `<path d="M-41,-536Q3,-548 47,-536L43,-507Q3,-488 -37,-507Z" fill="#d6e8f2" stroke="${LINE}" stroke-width="2.4" stroke-linejoin="round"/>
    <path d="M-33,-527Q3,-535 39,-527M-31,-517Q3,-523 37,-517" stroke="#a2bed0" stroke-width="2.2" fill="none"/>
    <path d="M-41,-533Q-52,-548 -45,-562M47,-533Q56,-548 50,-562" stroke="#eef4f6" stroke-width="2.6" fill="none" stroke-linecap="round"/>`;
  const SUN = `<g><path d="M-34,-557H-3Q-1,-540 -16,-536Q-33,-537 -34,-557ZM5,-557H36Q35,-537 19,-536Q4,-540 5,-557Z" fill="#14161a" stroke="${LINE}" stroke-width="2.4"/>
    <path d="M-3,-552h8M-34,-555l-12,-3M36,-555l12,-3" stroke="#14161a" stroke-width="3.4" fill="none"/>
    <path d="M-28,-552l8,-2M11,-552l8,-2" stroke="#fff" stroke-width="2.2" opacity=".5"/></g>`;

  // ---------------- hand props (hand group at the wrist, palm at +118) ----------------
  const PHONE_H = `<g transform="translate(4,146) rotate(-12)"><rect x="-21" y="-38" width="42" height="76" rx="8" fill="#1c2026" stroke="${LINE}" stroke-width="2.6"/>
    <rect x="-17" y="-32" width="34" height="62" rx="5" fill="#a8d8f4"/><path d="M-12,-22h24M-12,-12h18" stroke="#fff" stroke-width="3" opacity=".7"/></g>`;
  const TICKET_H = `<g transform="translate(6,146) rotate(-14)"><rect x="-38" y="-22" width="76" height="44" rx="3" fill="#f4cfdc" stroke="${LINE}" stroke-width="2.4"/>
    <rect x="-32" y="-16" width="64" height="12" rx="2" fill="#d8708e"/><path d="M-30,6h40M-30,14h28" stroke="#b8506e" stroke-width="3"/></g>`;
  const TICKET_EDGE = `<g transform="translate(10,150) rotate(-30)"><rect x="-10" y="-22" width="62" height="40" rx="3" fill="#f4cfdc" stroke="${LINE}" stroke-width="2.4"/>
    <rect x="-6" y="-16" width="52" height="10" rx="2" fill="#d8708e"/></g>`;

  // ---------------- the family ----------------
  C.lotYou = { v2: { ...C.keng.v2, extra: "", top: { kind: "tee", c: "#34619e", sleeve: "short" },
    print: `<path d="M-18,-410h36" stroke="#e8eef4" stroke-width="5" stroke-linecap="round" opacity=".75"/><path d="M-10,-398h20" stroke="#e8eef4" stroke-width="5" stroke-linecap="round" opacity=".5"/>`,
    bottom: { kind: "shorts", c: "#4a4c54" } } };
  C.lotYouMask = { v2: { ...C.lotYou.v2, faceTop: MASK } };
  C.lotYouPhone = { v2: C.lotYou.v2, hand: PHONE_H, keep: "F" };
  C.lotYouTicket = { v2: C.lotYou.v2, hand: TICKET_H, keep: "F" };
  C.lotYouMaskTicket = { v2: C.lotYouMask.v2, hand: TICKET_H, keep: "F" };

  C.lotMom = { v2: { ...C.chan.v2, extra: "", top: { kind: "blouse", c: "#c45f7c", sleeve: "elbow", trim: "#9a4460" } } };
  C.lotMomPhone = { v2: C.lotMom.v2, hand: PHONE_H, keep: "F" };
  C.lotMomMask = { v2: { ...C.lotMom.v2, faceTop: MASK } };
  C.lotMomMaskTicket = { v2: C.lotMomMask.v2, hand: TICKET_H, keep: "F" };

  // ป้าศรี: lipstick, gold earrings, a red flower clip in the perm, a pearl string (so she reads as the auntie up close)
  const SRI_FACE = `<g fill="#e8c048" stroke="${LINE}" stroke-width="1.6"><circle cx="-50" cy="-527" r="5.5"/><circle cx="55" cy="-527" r="5.5"/></g>`;
  const SRI_TOP = `<g transform="translate(-38,-596)"><circle r="12" fill="#d8443a" stroke="${LINE}" stroke-width="2"/><circle r="4.5" fill="#f6d36a"/></g>`;
  C.lotSri = { v2: { ...C.bua.v2, blush: 0.85, lip: "#c43a48", face: (C.bua.v2.face || "") + SRI_FACE, faceTop: SRI_TOP,
    extra: `<path d="M-24,-486Q0,-458 24,-486" stroke="#f4f0e6" stroke-width="6" stroke-dasharray="0.1 9" stroke-linecap="round" fill="none"/>`,
    top: { kind: "blouse", c: "#e6bf3e", sleeve: "elbow", trim: "#bf9624" } } };
  C.lotSriPhone = { v2: C.lotSri.v2, hand: PHONE_H, keep: "F" };
  C.lotSriTicket = { v2: C.lotSri.v2, hand: TICKET_H, keep: "F" };

  C.lotMan = { v2: { ...C.samarn.v2, top: { kind: "shirt", c: "#2f8a78", sleeve: "long", neck: "collar", collar: "#25705f", button: "#e8f0e8" },
    print: `<g fill="#f2d24a" opacity=".85"><circle cx="-26" cy="-430" r="7"/><circle cx="22" cy="-400" r="6"/><circle cx="-8" cy="-360" r="7"/><circle cx="30" cy="-340" r="5"/></g>` } };
  C.lotManSun = { v2: { ...C.lotMan.v2, faceTop: SUN } };
  C.lotManSunTicket = { v2: C.lotManSun.v2, hand: TICKET_H, keep: "F" };

  C.lotBeer = { v2: { ...C.keng.v2, extra: "", skin: "#c48e60", hair: C.piak.v2.hair, top: { kind: "tee", c: "#d6443a", sleeve: "short" },
    print: `<text x="0" y="-372" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#f4f0e6">10</text><path d="M-40,-470h80" stroke="#f4f0e6" stroke-width="5" opacity=".8"/>`,
    bottom: { kind: "shorts", c: "#1f2c48" } } };
  C.lotBeerTicket = { v2: C.lotBeer.v2, hand: TICKET_EDGE, keep: "B" };
  C.lotBeerFull = { v2: C.lotBeer.v2, hand: TICKET_H, keep: "F" };

  C.lotBoon = { v2: C.yaiBua.v2 };

  // ---------------- the ticket ----------------
  // generic: no emblem, no real layout; pastel pink with the number in big print
  const ticket = (x, y, s, o = {}) => {
    const n = o.num || NUM, id = o.id || "tk";
    const digits = [...n].map((d, i) => `<g id="${id}-d${i}"><rect x="${-246 + i * 82}" y="-46" width="70" height="96" rx="10" fill="#fffaf2" ${O(3)}/>
      ${T(-211 + i * 82, 32, 84, d, { fill: "#a8305a" })}</g>`).join("");
    return at(x, y, s, `<rect x="-300" y="-170" width="600" height="340" rx="16" fill="#f6d2de" ${O(5)}/>
      <rect x="-280" y="-150" width="560" height="62" rx="10" fill="#d8708e"/>${T(0, -105, 40, o.head || "สลากกินแบ่ง · งวด 16 พ.ย.", { fill: "#fff6f0" })}
      <path d="M-280,80H280" stroke="#d8708e" stroke-width="3" stroke-dasharray="10 8"/>
      ${T(-240, 128, 30, "ชุด 21 · 80 บาท", { anchor: "start", fill: "#a8305a", w: 700 })}${T(240, 128, 30, "งวดนี้งวดเดียว", { anchor: "end", fill: "#a8305a", w: 700, op: 0.7 })}
      ${digits}`, o.rot || 0);
  };
  // the phone screen with the draw result (inside NkE.phone's 272×540 screen box)
  const result = (o = {}) => {
    const n = o.num || NUM, id = o.id || "rs";
    return `<rect width="272" height="540" fill="#f4f0e8"/><rect width="272" height="84" fill="#2f6aa8"/>${T(136, 52, 26, "ผลสลาก งวด 16 พ.ย.", { fill: "#fff" })}
      ${T(136, 150, 30, "รางวัลที่ 1", { fill: "#c8304a" })}
      <rect x="18" y="176" width="236" height="96" rx="14" fill="#fff" stroke="#c8304a" stroke-width="4"/>
      ${[...n].map((d, i) => `<g id="${id}-r${i}">${T(42 + i * 38, 248, 66, d, { fill: "#2e2a26" })}</g>`).join("")}
      ${T(136, 316, 22, "รางวัลละ 6,000,000 บาท", { fill: "#5a5650", w: 700 })}
      <path d="M24,360H248M24,410H248M24,460H248" stroke="#d8d0c0" stroke-width="10" stroke-linecap="round"/>`;
  };
  const call = () => `<rect width="272" height="540" fill="#1e2a3a"/>${T(136, 70, 22, "สายเรียกเข้า", { fill: "#c8d4e0", w: 700 })}
    <circle cx="136" cy="170" r="62" fill="#e6bf3e" stroke="#fff" stroke-width="5"/><circle cx="136" cy="150" r="24" fill="#c48c62"/><path d="M92,214Q136,170 180,214" fill="#c48c62"/>
    <path d="M104,134Q136,96 168,134Q160,118 136,114Q112,118 104,134Z" fill="#2a2420"/>
    ${T(136, 278, 34, "ป้าแจ๋ว", { fill: "#fff" })}${T(136, 314, 22, "แผงหวยหน้าตลาด", { fill: "#c8d4e0", w: 700 })}
    <circle cx="70" cy="452" r="34" fill="#d8443a"/><circle cx="202" cy="452" r="34" fill="#3aa86a"/>
    <path d="M56,452h28M188,448q14,-14 28,0" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"/>`;

  // ---------------- the kitchen wall ----------------
  const calendar = (x, y, s, o = {}) => {
    const id = o.id || "cal";
    let grid = "";
    for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) {
      const d = r * 7 + c - 5;
      if (d >= 1 && d <= 30) grid += T(-150 + c * 50, 120 + r * 46, 26, String(d), { fill: d === 16 ? "#c8302a" : "#5a544c", w: d === 16 ? 900 : 700 });
    }
    // the month's picture (hills, a sala, the sun) · grandma's six digits are a small red scribble in the empty cells of the first row,
    // easy to walk past every morning (EP.3 zooms in on #id-red) · the draw date (16) circled
    const pic = `<rect x="-172" y="-96" width="344" height="168" fill="#bfe0ee"/><circle cx="112" cy="-52" r="22" fill="#f6d36a"/>
      <path d="M-172,40Q-90,-30 0,20Q80,-20 172,30V72H-172Z" fill="#8cc08a"/><path d="M-172,72V56Q-60,22 60,50Q120,38 172,54V72Z" fill="#6aa86e"/>
      <g transform="translate(-70,12)"><path d="M-36,0L0,-30L36,0Z" fill="#c8603e"/><rect x="-24" y="0" width="48" height="26" fill="#f4e6c8"/></g>
      <rect x="-172" y="-96" width="344" height="168" fill="none" stroke="#5a544c" stroke-width="3"/>`;
    return at(x, y, s, `<path d="M0,-226L-22,-196H22Z" fill="#8a6a4a"/><circle cx="0" cy="-226" r="7" fill="#5a4a3a"/>
      <rect x="-190" y="-200" width="380" height="460" rx="8" fill="#fbf7ee" ${O(4)}/><rect x="-190" y="-200" width="380" height="96" rx="8" fill="#c8402e"/>
      ${T(0, -138, 44, "พฤศจิกายน", { fill: "#fff6ea" })}${pic}
      <g id="${id}-red" transform="rotate(-3 -52 120)">${T(-52, 128, 34, (o.num || NUM).split("").join(" "), { fill: "#d8202a", font: "Sriracha", w: 400 })}
        <path d="M-138,138Q-52,146 34,136" stroke="#d8202a" stroke-width="3" fill="none" stroke-linecap="round"/></g>
      ${grid}<circle id="${id}-ring" cx="-150" cy="249" r="22" fill="none" stroke="#d8202a" stroke-width="3.5"/>`);
  };
  const sign = (x, y, s, o = {}) => at(x, y, s, `<circle cx="0" cy="0" r="8" fill="#5a4a3a"/>
    <g id="${o.id || "sg"}-swing"><path d="M0,0L-140,90M0,0L140,90" stroke="#7a6a52" stroke-width="4" fill="none"/>
      <path d="M-210,86H210L204,250H-204Z" fill="#a8743e" ${O(5)}/>
      <path d="M-196,120H198M-200,170H200M-198,218H196" stroke="#8a5a2a" stroke-width="3" opacity=".55"/>
      <circle cx="-140" cy="98" r="6" fill="#4a3a2a"/><circle cx="140" cy="98" r="6" fill="#4a3a2a"/>
      ${T(0, 158, 50, "ถูกเลขยาย", { fill: "#3a2414", font: "Sriracha", w: 400 })}${T(0, 222, 50, "แบ่งยายครึ่ง", { fill: "#3a2414", font: "Sriracha", w: 400 })}</g>`, o.rot || 0);

  // ---------------- cards ----------------
  const think = (x, y, s, inner = "") => at(x, y, s, `<circle cx="0" cy="0" r="12" fill="#fff" ${O(4)}/><circle cx="34" cy="-40" r="20" fill="#fff" ${O(4)}/>
    <path d="M10,-120C-30,-130 -40,-190 4,-206C10,-250 80,-262 104,-226C140,-260 214,-236 210,-186C254,-172 250,-110 206,-100C200,-60 132,-52 112,-80C86,-50 28,-62 10,-120Z" fill="#fff" ${O(5)}/>
    <g transform="translate(106,-160)">${inner}</g>`);
  const tag = (x, y, text, o = {}) => at(x, y, o.s || 1, `<path d="M-14,-34H${f1(text.length * 23 + 28)}L${f1(text.length * 23 + 22)},26H-20Z" fill="${o.bg || "#f4e7b8"}" ${O(3)} opacity=".96"/>
    ${T(text.length * 11.5 + 4, 10, 44, text, { fill: o.fill || "#2e2a26", font: "Sriracha", w: 400 })}`, o.rot ?? -4);

  // ---------------- poses for this story ----------------
  const M = Rig.MODES;
  M.liePhone = (u, o) => ({ ...M.lie(u, o), uaF: (o.ua ?? -112) + 2 * Math.sin(u * 1.1), faF: o.fa ?? -36, head: 6 });   // on the back in bed, the phone held up over the face
  M.sitHug = (u, o) => { const j = Math.sin(u * 40) * 1.2; return { ...M.sit(u, o), uaF: 14 + j, faF: 110, uaB: -14 - j, faB: -110, torso: 4 + j * 0.4, head: 3 + j }; };  // sitting up in bed, squeezing the pillow, trembling
  M.nod = (u, o) => ({ ...M.sitChair(u, o), head: 3 + 10 * (0.5 - 0.5 * Math.cos(u * 2 * Math.PI / (o.period || 1.0))), ...(o.hold ? { uaB: -34, faB: -62 } : {}) });  // a slow nod at the table
  M.sitHold = (u, o) => ({ ...M.sitChair(u, o), uaB: -34, faB: -62 });  // at the table, the back hand up near the table edge

  // ---------------- EP.2: props, inserts and a few more people ----------------
  const ZIP = `<g><path d="M-26,-506H32" stroke="#6a6e74" stroke-width="8" stroke-linecap="round"/>
    ${[-20, -12, -4, 4, 12, 20].map((x) => `<path d="M${x},-511v10" stroke="#b8bcc2" stroke-width="3"/>`).join("")}
    <rect x="28" y="-514" width="10" height="16" rx="3" fill="#c8ccd2" stroke="${LINE}" stroke-width="1.8"/></g>`;
  const SPOON_H = `<g transform="translate(4,146) rotate(-20)"><ellipse cx="0" cy="-36" rx="12" ry="16" fill="#dfe3e6" stroke="${LINE}" stroke-width="2.2"/>
    <rect x="-3.5" y="-22" width="7" height="58" rx="3" fill="#c8ccd0" stroke="${LINE}" stroke-width="2"/></g>`;
  C.lotSriZip = { v2: { ...C.lotSri.v2, faceTop: SRI_TOP + ZIP } };
  const spoon = (c) => ({ v2: c.v2, hand: SPOON_H, keep: "F" });
  Object.assign(C, { lotYouMaskSpoon: spoon(C.lotYouMask), lotMomMaskSpoon: spoon(C.lotMomMask), lotManSunSpoon: spoon(C.lotManSun),
    lotBeerSpoon: spoon(C.lotBeer), lotSriZipSpoon: spoon(C.lotSriZip), lotBoonSpoon: spoon(C.lotBoon) });
  M.touch = (u, o) => ({ ...M.idle(u, o), uaF: -96 + 2 * Math.sin(u * 2), faF: -8, torso: 4, head: 7 });   // standing, a hand out to a forehead
  M.eat = (u, o) => { const k = 0.5 - 0.5 * Math.cos((2 * Math.PI * u) / (o.period || 1.7)); return { ...M.sitChair(u, o), uaF: -30 - 12 * k, faF: -50 - 92 * k, head: 3 - 5 * k }; };
  M.sitStill = (u, o) => ({ ...M.sitChair(0, o), head: o.head ?? 0 });   // frozen mid-chew
  const cooker = (x, y, s, o = {}) => at(x, y, s, `<ellipse cx="0" cy="92" rx="150" ry="22" fill="#000" opacity=".18"/>
    <path d="M-130,-20Q-140,80 -110,90H110Q140,80 130,-20Z" fill="#f4f2ec" ${O(5)}/><path d="M-134,18H134" stroke="#e05a6a" stroke-width="10"/>
    ${[-90, -30, 30, 90].map((cx) => `<circle cx="${cx}" cy="18" r="9" fill="#f6d36a" ${O(2)}/>`).join("")}
    <rect x="-30" y="44" width="60" height="26" rx="6" fill="#d8d4c8" ${O(3)}/><circle cx="16" cy="57" r="6" fill="#e8443a"/>
    <g id="${o.id || "ck"}-lid"><path d="M-136,-20Q-130,-96 0,-100Q130,-96 136,-20Z" fill="#fbfaf6" ${O(5)}/><rect x="-30" y="-118" width="60" height="22" rx="10" fill="#b8b4aa" ${O(4)}/></g>`);
  const amulet = (x, y, s, o = {}) => at(x, y, s, `<rect x="-120" y="-20" width="240" height="112" rx="8" fill="#8a5a32" ${O(5)}/><rect x="-104" y="-6" width="208" height="22" fill="#5a3a1a"/>
    <g transform="translate(-50,42)"><path d="M-24,30V-8Q-24,-38 0,-42Q24,-38 24,-8V30Z" fill="#e8c860" ${O(4)}/><circle cx="0" cy="-16" r="8" fill="#c8a040"/><path d="M-11,22Q0,2 11,22Z" fill="#c8a040"/></g>
    <g transform="translate(50,42)"><path d="M-24,30V-8Q-24,-38 0,-42Q24,-38 24,-8V30Z" fill="#e8c860" ${O(4)}/><circle cx="0" cy="-16" r="8" fill="#c8a040"/><path d="M-11,22Q0,2 11,22Z" fill="#c8a040"/></g>
    <g id="${o.id || "am"}-lid"><rect x="-124" y="-62" width="248" height="44" rx="8" fill="#a8743e" ${O(5)}/><path d="M-100,-40H100" stroke="#e8c860" stroke-width="5"/></g>`);
  const sock = (x, y, s, o = {}) => at(x, y, s, `<path d="M-40,-120H40V40Q40,70 70,80Q120,96 110,130Q100,160 40,150H-20Q-50,146 -46,100Z" fill="#f4f0e6" ${O(5)}/>
    <path d="M-40,-96H40M-40,-72H40" stroke="#e05a6a" stroke-width="10"/><path d="M-46,120Q-10,150 40,150" stroke="#c8c0b0" stroke-width="5" fill="none"/>`, o.rot || 0);
  const mattress = (x, y, s, o = {}) => at(x, y, s, `<rect x="-300" y="0" width="600" height="64" rx="10" fill="#8a5a32" ${O(5)}/>
    <g id="${o.id || "mt"}-top"><rect x="-300" y="-112" width="600" height="112" rx="18" fill="#f4f0e8" ${O(5)}/><path d="M-280,-56H280" stroke="#d8d4c8" stroke-width="5"/></g>`);
  const tmini = (x, y, s, o = {}) => at(x, y, s, `<rect x="-62" y="-38" width="124" height="76" rx="6" fill="#f6d2de" ${O(4)}/><rect x="-54" y="-30" width="108" height="18" rx="3" fill="#d8708e"/>
    ${T(0, 28, 30, o.num || NUM, { fill: "#a8305a", ls: 2 })}`, o.rot || 0);
  const snakes = (x, y, s) => at(x, y, s, `<ellipse rx="200" ry="128" fill="#fff" ${O(5)}/>${[0, 1, 2, 3, 4, 5].map((i) => {
      const cx = -120 + (i % 3) * 120, cy = -40 + Math.floor(i / 3) * 82;
      return `<g transform="translate(${cx},${cy})"><path d="M-44,8q14,-18 28,0t28,0t22,-4" stroke="${INK}" stroke-width="19" fill="none" stroke-linecap="round"/>
        <path d="M-44,8q14,-18 28,0t28,0t22,-4" stroke="#fbfbf6" stroke-width="12" fill="none" stroke-linecap="round"/>
        <path d="M50,0l14,-3m-14,3l14,4" stroke="#d8202a" stroke-width="3" stroke-linecap="round"/>
        <ellipse cx="38" cy="2" rx="15" ry="11" fill="#fbfbf6" stroke="${INK}" stroke-width="3"/><circle cx="42" cy="-1" r="2.6" fill="${INK}"/></g>`; }).join("")}`);
  const bulb = (x, y, s) => at(x, y, s, `${[0, 1, 2, 3, 4, 5, 6].map((k) => { const a = (-150 + k * 20) * Math.PI / 180;
      return `<path d="M${f1(Math.cos(a) * 92)},${f1(Math.sin(a) * 92)}L${f1(Math.cos(a) * 124)},${f1(Math.sin(a) * 124)}" stroke="#f6c83a" stroke-width="9" stroke-linecap="round"/>`; }).join("")}
    <path d="M-50,-10Q-56,-76 0,-80Q56,-76 50,-10Q40,14 26,30V44H-26V30Q-40,14 -50,-10Z" fill="#fff3a8" ${O(5)}/><rect x="-26" y="44" width="52" height="30" rx="6" fill="#b8bcc2" ${O(4)}/>`);

  // ---------------- EP.3: the pickups, the money, a few more poses ----------------
  M.hideBehind = (u, o) => ({ ...M.idle(u, o), uaF: 34 + 2 * Math.sin(u * 3), faF: 30, torso: -3, head: -4 + 2 * Math.sin(u * 2.2) });   // the phone behind the back
  M.sitLaugh = (u, o) => { const b = Math.abs(Math.sin(u * 8)); return { ...M.sitChair(u, o), torso: -4 - 3 * b, head: -10 - 4 * b, uaF: -20, faF: -100, bodyY: 150 - 3 * b }; };
  M.wave2 = (u, o) => ({ ...M.idle(u, o), uaF: -150, faF: -20 + 24 * Math.sin(u * 2 * Math.PI / 1.1), head: 4 });
  const pickup = (x, y, s, o = {}) => at(x, y, s, `<ellipse cx="0" cy="8" rx="300" ry="26" fill="#000" opacity=".3"/>
    <path d="M-290,-40V-120H-40L20,-210H190Q236,-206 250,-150L290,-120Q300,-80 296,-40Z" fill="${o.c || "#c8d0d8"}" ${O(6)}/>
    <path d="M40,-196H180Q210,-192 222,-150H10Z" fill="#9ad0ec" ${O(4)}/><path d="M-40,-120V-40" stroke="${INK}" stroke-width="5"/>
    <rect x="-280" y="-150" width="236" height="30" rx="4" fill="${o.c2 || "#a8b0b8"}" ${O(4)}/>
    ${[-190, 190].map((wx) => `<circle cx="${wx}" cy="-36" r="52" fill="#2a2a2e" ${O(5)}/><circle cx="${wx}" cy="-36" r="22" fill="#b8bcc2"/>`).join("")}
    <ellipse id="${o.id || "pk"}-hl" cx="292" cy="-96" rx="10" ry="16" fill="#fff6c0" ${O(3)}/>`, o.rot || 0);
  const money = (x, y, s) => at(x, y, s, [0, 1, 2, 3, 4, 5].map((k) => `<g transform="translate(${(k % 3) * 8 - 8},${-k * 26})"><rect x="-120" y="-30" width="240" height="60" rx="6" fill="#b8a88a" ${O(4)}/>
    <rect x="-104" y="-18" width="208" height="36" rx="4" fill="none" stroke="#7a6a4a" stroke-width="3"/>${T(0, 12, 28, "1000", { fill: "#5a4a2a" })}</g>`).join(""));
  const tears = (x, y, s) => at(x, y, s, `<path d="M-30,0q-6,14 0,22q6,-8 0,-22Z" fill="#7ac8f4" stroke="${INK}" stroke-width="1.6"/><path d="M30,0q-6,14 0,22q6,-8 0,-22Z" fill="#7ac8f4" stroke="${INK}" stroke-width="1.6"/>`);

  window.Lot = { NUM, ticket, result, call, calendar, sign, think, tag, MASK, SUN, T, at, O, INK, cooker, amulet, sock, mattress, tmini, snakes, bulb, pickup, money, tears };
})();
