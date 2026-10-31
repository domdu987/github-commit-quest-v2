// "รั้วสุดท้าย" cast drawn with rig v2 (rig2.js). Load after tidecast.js (uses its Rig.build hook for v2.legs / v2.skirt / keep).
//   pim      ครูพิม 32: a high ponytail with a teal scrunchie, side-swept fringe, a pale-blue teacher's shirt with sleeves rolled to the
//            elbow, navy slacks, flat shoes, a whistle on a lanyard · pimLedger? no: hands free
//   kong     ก้อง 17: spiky hair, a red bandana round the neck, a sleeveless yellow PE shirt (school logo), dark jeans, sneakers,
//            backpack straps · kongBat (a taped baseball bat in the fist) · kongCrate (a crate of cans held in front: pose "carry")
//   man      ลุงหมาน 61: a woven farmer's hat, white moustache and stubble, an indigo ม่อฮ่อม shirt, a checked ผ้าขาวม้า at the waist,
//            rolled black trousers, bare feet · manHose (the green hose in the fist)
//   hong     เจ๊หงส์ 45: a short permed bob, glasses on a chain, red lipstick, a red flowered blouse, black trousers, sandals, a pen behind
//            the ear · hongBook (the ledger in the hand)
//   pan      น้องปั้น 7 (draw at ~0.62 of an adult): two pigtails with red bobbles, a white kindergarten blouse with a navy bow, navy
//            shorts, white socks + black shoes · panDraw (her drawing held up in the fist)
//   phu      ภู 28: messy hair, stubble, a faded orange rescue vest over a charcoal tee, cargo trousers, boots, a bandage on the head
//   hz1 hz2 hz3   ผีห่า: a farmer, a schoolboy, a market woman — grey-green skin, torn clothes, milky glowing eyes (eyes "glow"), stains
// Poses added: carry (both forearms forward and up holding something in front) · shamble2 (arms reaching forward, head down)
//   · cough (bent, a fist at the mouth) · siphon (crouched, the front hand at the mouth) · hold (front hand raised showing something)
//   · bat (the bat raised over the shoulder) · slam (both arms pushing forward)
(function () {
  const { LINE, dk, hi } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  // ---------------- hair ----------------
  const pimFront = (h) => `
    <path d="M-47,-548C-56,-610 -16,-630 6,-628C34,-628 58,-606 51,-548Q46,-570 36,-582Q10,-596 -14,-590Q-30,-580 -40,-566Q-46,-556 -47,-548Z" fill="${h.c}" ${ln()}/>
    <path d="M-40,-566Q-6,-604 40,-584Q20,-574 6,-578Q-20,-570 -40,-566Z" fill="${dk(h.c, 0.2)}" opacity=".5"/>
    <path d="M-30,-614Q-4,-626 26,-616" stroke="${h.sh}" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>
    <path d="M-20,-620Q-36,-596 -40,-568M8,-626Q30,-610 44,-584" stroke="${h.s}" stroke-width="2.2" fill="none" opacity=".7"/>`;
  const pimBack = (h) => `<path d="M10,-628Q60,-660 74,-610Q86,-560 70,-500Q62,-470 74,-440Q48,-450 46,-500Q50,-560 30,-610Z" fill="${h.c}" ${ln()}/>
    <path d="M56,-600q10,40 2,90" stroke="${h.s}" stroke-width="2.4" fill="none"/><circle cx="34" cy="-626" r="12" fill="#2aa59a" ${ln(2.2)}/>`;
  const kongFront = (h) => `
    <path d="M-48,-552C-58,-600 -40,-624 -22,-626L-30,-648L-8,-630L0,-656L14,-630L30,-650L32,-626Q56,-616 52,-552Q46,-574 34,-584Q16,-592 0,-586Q-20,-592 -36,-578Q-44,-566 -48,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-20,-620l-8,-20M10,-626l6,-22" stroke="${h.sh}" stroke-width="4" opacity=".5" stroke-linecap="round"/>`;
  const manHat = `<path d="M-108,-588Q-60,-604 0,-606Q60,-604 112,-588Q118,-578 100,-574Q0,-560 -96,-574Q-116,-578 -108,-588Z" fill="#d8b46a" ${ln()}/>
    <path d="M-50,-592Q-48,-660 2,-668Q50,-660 54,-592Q0,-584 -50,-592Z" fill="#e2c27a" ${ln()}/>
    ${Array.from({ length: 9 }, (_, k) => `<path d="M${-90 + k * 22},-582l10,-8" stroke="#a8843a" stroke-width="2" opacity=".7"/>`).join("")}
    ${Array.from({ length: 5 }, (_, k) => `<path d="M${-40 + k * 20},-596l8,-56" stroke="#b8944a" stroke-width="2" opacity=".6"/>`).join("")}
    <path d="M-48,-600Q0,-590 52,-600" stroke="#7a3a2a" stroke-width="7"/>`;
  const manFace = `<path d="M-20,-512Q4,-500 26,-512Q20,-522 4,-518Q-12,-522 -20,-512Z" fill="#ece8de" ${ln(1.8)}/>
    <g fill="#ece8de" opacity=".8">${[[-30, -505], [-22, -498], [-10, -494], [2, -493], [14, -495], [26, -500], [32, -508]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.8"/>`).join("")}</g>
    <path d="M-38,-552l-8,-3M-38,-545l-8,1M42,-552l8,-3M42,-545l8,1M-24,-592q12,-4 24,0M-14,-534q-8,12 -4,22M24,-534q8,12 4,22" stroke="#4e2c14" stroke-width="2" fill="none" stroke-linecap="round" opacity=".7"/>`;
  const hongFront = (h) => `<g fill="${h.c}" ${ln(2.2)}>${[[-44, -560, 16], [-46, -536, 14], [-34, -598, 18], [-12, -614, 19], [14, -616, 19], [36, -602, 18], [50, -572, 16], [52, -544, 14], [-46, -582, 15]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}"/>`).join("")}</g>
    <path d="M-30,-596Q0,-616 34,-598" stroke="${h.sh}" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>
    <path d="M54,-578l20,-34" stroke="#2a5ab8" stroke-width="6" stroke-linecap="round"/><path d="M72,-610l4,-6" stroke="#f2f2f2" stroke-width="5" stroke-linecap="round"/>`;
  const hongFace = `<g fill="none" stroke="#3a2a2a" stroke-width="3"><circle cx="-22" cy="-552" r="15"/><circle cx="26" cy="-552" r="15"/><path d="M-7,-554h18M-37,-556l-10,-4M41,-556l8,-4"/></g>
    <path d="M-46,-548Q-56,-500 -40,-470" stroke="#d8b84a" stroke-width="2" fill="none" stroke-dasharray="3 3"/><circle cx="-24" cy="-558" r="3" fill="#fff" opacity=".6"/><circle cx="24" cy="-558" r="3" fill="#fff" opacity=".6"/>`;
  const panFront = (h) => `
    <path d="M-47,-550C-54,-608 -18,-628 4,-628C32,-627 56,-606 51,-550Q48,-566 40,-576Q30,-570 22,-580Q14,-568 2,-576Q-10,-566 -20,-578Q-30,-568 -40,-576Q-46,-566 -47,-550Z" fill="${h.c}" ${ln()}/>
    <path d="M2,-628V-580" stroke="${h.s}" stroke-width="2.4" opacity=".7"/><path d="M-30,-614Q2,-628 34,-614" stroke="${h.sh}" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>`;
  const panBack = (h) => [-1, 1].map((sd) => `<path d="M${sd * 44},-590Q${sd * 84},-596 ${sd * 86},-560Q${sd * 88},-520 ${sd * 72},-500Q${sd * 64},-530 ${sd * 50},-560Z" fill="${h.c}" ${ln()}/><circle cx="${sd * 54}" cy="-588" r="9" fill="#e2382e" ${ln(2)}/>`).join("");
  const phuFront = (h) => `<path d="M-48,-552C-58,-606 -22,-630 6,-626C38,-624 58,-600 52,-552Q48,-570 40,-578L30,-568L24,-586L12,-570L4,-590L-8,-570L-18,-588L-28,-570L-38,-580Z" fill="${h.c}" ${ln()}/>
    <path d="M-50,-584Q0,-604 54,-586L54,-570Q0,-588 -50,-570Z" fill="#f4f2ec" ${ln(2)}/><path d="M30,-584l6,10" stroke="#c84a3a" stroke-width="4" opacity=".7"/>`;
  const stubble = (c = "#3a2a20") => `<g fill="${c}" opacity=".35">${Array.from({ length: 22 }, (_, k) => `<circle cx="${-34 + (k % 11) * 7}" cy="${-514 + Math.floor(k / 11) * 9 + ((k % 11) - 5) ** 2 * 0.3}" r="1.5"/>`).join("")}</g>`;

  // ---------------- clothes extras ----------------
  const whistle = `<path d="M-20,-490Q0,-430 20,-490" stroke="#e2382e" stroke-width="3" fill="none"/><g transform="translate(0,-436)"><rect x="-12" y="-6" width="26" height="14" rx="5" fill="#d8dce0" ${ln(2)}/><circle cx="10" cy="1" r="4" fill="#8a9096"/></g>`;
  const bandana = `<path d="M-30,-494Q0,-474 32,-494L26,-470Q0,-452 -24,-470Z" fill="#d8302a" ${ln(2.4)}/><path d="M-6,-470l-10,26l14,-6l10,8l-2,-26Z" fill="#c8282a" ${ln(2)}/><circle cx="-12" cy="-482" r="2.5" fill="#fff" opacity=".8"/><circle cx="12" cy="-480" r="2.5" fill="#fff" opacity=".8"/>`;
  const straps = `<path d="M-36,-486L-44,-330M36,-486L44,-330" stroke="#2a4a7a" stroke-width="11" stroke-linecap="round"/><path d="M-36,-486L-44,-330M36,-486L44,-330" stroke="#5a7ab0" stroke-width="3" opacity=".7"/>`;
  const peLogo = `<circle cx="-24" cy="-420" r="14" fill="#2c5a8a" ${ln(2)}/><text x="-24" y="-414" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="14" fill="#fff">น</text><path d="M-60,-372Q0,-362 60,-372" stroke="#2c5a8a" stroke-width="6" opacity=".7"/>`;
  const pakama = `<path d="M-58,-336Q0,-322 58,-336L60,-306Q0,-292 -60,-306Z" fill="url(#tdCheck)" ${ln(2.2)}/><path d="M30,-306l10,40l14,-4l-6,-40Z" fill="url(#tdCheck)" ${ln(2)}/>`;
  const flowersRed = `${[[-34, -450], [18, -432], [-12, -380], [36, -362], [-40, -330], [10, -326]].map(([x, y]) => `<g transform="translate(${x},${y})">${[0, 72, 144, 216, 288].map((a) => `<ellipse cy="-6" rx="4.4" ry="6.4" fill="#ffe0e0" transform="rotate(${a})"/>`).join("")}<circle r="2.6" fill="#ffd23a"/></g>`).join("")}`;
  const bow = `<path d="M0,-484l-22,-12v24ZM0,-484l22,-12v24Z" fill="#1e2a5a" ${ln(2)}/><circle cx="0" cy="-484" r="5" fill="#1e2a5a" ${ln(1.8)}/><circle cx="-14" cy="-418" r="5" fill="#2a3a7a"/>`;
  const vest = `<path d="M-54,-488L-22,-484L-14,-430L-18,-306Q-44,-300 -70,-306L-68,-448Q-66,-476 -54,-488Z" fill="url(#tdVest)" ${ln(2.6)}/><path d="M54,-488L22,-484L14,-430L18,-306Q44,-300 70,-306L68,-448Q66,-476 54,-488Z" fill="url(#tdVest)" ${ln(2.6)}/>
    <path d="M-68,-400H-16M16,-400H68" stroke="#e8ecf0" stroke-width="10" opacity=".8"/><path d="M-68,-400H-16M16,-400H68" stroke="#9aa0a6" stroke-width="2" opacity=".6"/>
    <rect x="22" y="-470" width="34" height="24" rx="3" fill="#2a2e34" ${ln(1.8)}/><text x="39" y="-453" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="12" fill="#ffd23a">กู้ภัย</text>
    <path d="M-60,-330q20,6 34,0" stroke="#7a3a1a" stroke-width="4" opacity=".4" fill="none"/>`;
  const rolled = (c) => (side) => {
    const cc = side === "B" ? dk(c, 0.1) : c, s0 = 17.5;
    return { shin: Rig2.paint(`M${-s0 - 6},-8Q0,-14 ${s0 + 6},-8L${s0 + 9},60H${-s0 - 9}Z`, cc) + `<path d="M${-s0 - 11},54Q0,48 ${s0 + 11},54L${s0 + 10},74Q0,80 ${-s0 - 10},74Z" fill="${hi(cc, 0.16)}" ${ln(2.2)}/>` };
  };
  // zombies: stains, tears, and the pale scar of a bite
  const rot = (c) => `<path d="M-40,-420q10,30 -4,60M30,-380q14,20 0,50" stroke="${dk(c, 0.4)}" stroke-width="10" opacity=".35" fill="none" stroke-linecap="round"/>
    <path d="M-60,-320l14,-20l10,24l12,-16l10,18" fill="none" stroke="${LINE}" stroke-width="2.2"/><circle cx="20" cy="-440" r="16" fill="#5a2a22" opacity=".45"/>`;
  const zFace = `<path d="M-40,-560q10,-6 22,-2M20,-562q12,-4 22,2" stroke="#2a3020" stroke-width="3" fill="none"/><path d="M-30,-520q6,8 0,18M30,-518q-4,10 2,18" stroke="#4a5a3a" stroke-width="3" fill="none" opacity=".6"/><path d="M-20,-600q-6,20 4,30" stroke="#3a4a30" stroke-width="2.4" fill="none" opacity=".6"/>`;
  const zHair = (h) => `<path d="M-48,-552C-58,-604 -24,-628 4,-626C36,-624 58,-600 52,-552Q44,-580 30,-590Q10,-598 -10,-592Q-34,-584 -48,-552Z" fill="${h.c}" ${ln()}/><path d="M-30,-590l-6,30M8,-596l2,26M30,-588l6,22" stroke="${h.s}" stroke-width="3"/>`;

  // ---------------- specs ----------------
  const pimV2 = { skin: "#d8a47a", iris: "#3a2418", lash: true, blush: 0.5, lip: "#c0564a",
    hair: { c: "#2a1a14", s: "#140c08", sh: "#6a4a3a", front: (x) => pimFront(x.hair), back: (x) => pimBack(x.hair) },
    top: { kind: "shirt", c: "#bcd8f0", sleeve: "elbow", neck: "collar", collar: "#d6e8f8", button: "#f4f8fc", trim: "#9abedc" },
    bottom: { kind: "trousers", c: "#2a3450" }, feet: { kind: "sneaker", c: "#3a3a44", sole: "#8a8a90" }, extra: whistle };
  const kongV2 = { skin: "#c88a5a", iris: "#2a1a10", blush: 0.4, w: 0.98,
    hair: { c: "#1a1410", s: "#000", sh: "#5a4a40", front: (x) => kongFront(x.hair) },
    top: { kind: "tank", c: "#f2c83a", sleeve: "none" }, print: peLogo,
    bottom: { kind: "jeans", c: "#3a4a6a" }, feet: { kind: "sneaker", c: "#f4f2ec", mark: "#d8302a" }, extra: straps + bandana,
    face: `<path d="M-30,-526l8,3" stroke="#8a4a2a" stroke-width="2" opacity=".6"/>` };
  const manV2 = { skin: "#9a6a44", iris: "#2a1a12", blush: 0.12, bags: true, w: 0.96, limb: 0.92, brow: "#ece8de",
    hair: { c: "#ece8de", s: "#a8a49c", sh: "#fff", front: () => "" }, faceTop: manHat,
    top: { kind: "shirt", c: "#2e3c62", sleeve: "long", neck: "collar", collar: "#26324f", button: "#1a2238", trim: "#26324f" },
    bottom: { kind: "shorts", c: "#262630" }, feet: { kind: "bare" }, legs: rolled("#262630"), extra: pakama, face: manFace };
  const hongV2 = { skin: "#e2b48a", iris: "#3a2418", lash: true, blush: 0.6, lip: "#c8202a",
    hair: { c: "#3a2420", s: "#1e100c", sh: "#7a5040", front: (x) => hongFront(x.hair) },
    top: { kind: "blouse", c: "#c8303a", sleeve: "short" }, print: flowersRed,
    bottom: { kind: "trousers", c: "#1e1e24" }, feet: { kind: "sandal", c: "#7a3a2a" }, face: hongFace };
  const panV2 = { skin: "#f0c4a0", iris: "#4a2a1a", lash: true, blush: 1, headScale: 1.3, w: 0.92,
    hair: { c: "#24160f", s: "#0e0806", sh: "#6a4a3a", front: (x) => panFront(x.hair), back: (x) => panBack(x.hair) },
    top: { kind: "blouse", c: "#f8f6f0", sleeve: "short" }, print: bow,
    bottom: { kind: "shorts", c: "#22306a" }, feet: { kind: "sneaker", c: "#1e1e24", sole: "#f4f4f4" } };
  const phuV2 = { skin: "#b88058", iris: "#241812", blush: 0.25, bags: true,
    hair: { c: "#1e1612", s: "#000", sh: "#5a4a40", front: (x) => phuFront(x.hair) },
    top: { kind: "tee", c: "#3a3e46", sleeve: "short" }, bottom: { kind: "trousers", c: "#5a5a44" }, feet: { kind: "boot", c: "#3a2e24" },
    extra: vest, face: stubble() };
  const zom = (top, bottom, hair, extra = {}) => ({ skin: "#8e9e80", iris: "#e8f0d8", blush: 0, bags: true, w: 0.95, limb: 0.9,
    hair: { c: hair, s: dk(hair, 0.4), sh: hi(hair, 0.2), front: (x) => zHair(x.hair) },
    top, bottom, feet: { kind: "bare" }, print: rot(top.c), face: zFace, ...extra });

  Object.assign(C, {
    pim: { v2: pimV2 }, kong: { v2: kongV2 }, man: { v2: manV2 }, hong: { v2: hongV2 }, pan: { v2: panV2 }, phu: { v2: phuV2 },
    hz1: { v2: zom({ kind: "shirt", c: "#4a5a7a", sleeve: "long", neck: "collar" }, { kind: "shorts", c: "#3a3028" }, "#2a2420", { faceTop: manHat }) },
    hz2: { v2: zom({ kind: "shirt", c: "#e8e8e0", sleeve: "short", neck: "collar" }, { kind: "shorts", c: "#2a3a6a" }, "#1a1410") },
    hz3: { v2: zom({ kind: "blouse", c: "#8a3a5a", sleeve: "short" }, { kind: "sarong", c: "#3a4a2a", band: "#6a5a2a", band2: "#4a2a2a" }, "#2a201c") },
  });

  // ---------------- hand props (palm at (0,118)) ----------------
  const P = (window.FenceCast = window.FenceCast || {});
  P.bat = () => `<g transform="translate(0,118) rotate(180)"><path d="M-7,-10L-14,-300Q0,-320 14,-300L7,-10Z" fill="#c8945a" ${ln(2.6)}/><path d="M-9,-60H9M-10,-90H10M-11,-120H11" stroke="#2a2a2a" stroke-width="6"/><path d="M-4,-20L-8,-290" stroke="#f2c890" stroke-width="3" opacity=".7"/></g>`;
  P.crateChest = () => `<g transform="translate(30,-262)"><rect x="-150" y="-90" width="240" height="120" fill="#c8945a" ${ln(3)}/><path d="M-150,-50H90M-150,-10H90" stroke="#8a6040" stroke-width="5"/>
    ${[-120, -60, 0, 60].map((x, k) => `<g transform="translate(${x + 10},-96) scale(.24)"><path d="M-80,-180V0Q0,24 80,0V-180" fill="url(#fcCan)" ${ln(8)}/><path d="M-80,-150Q0,-128 80,-150V-40Q0,-18 -80,-40Z" fill="url(#fcLabel)"/><path d="M-80,-180Q-80,${k === 2 ? -270 : -202} 0,${k === 2 ? -282 : -204}Q80,${k === 2 ? -270 : -202} 80,-180Z" fill="#dfe4e8" ${ln(8)}/></g>`).join("")}</g>`;
  P.hose = () => `<g transform="translate(0,118)"><path d="M0,-10C10,-60 -30,-120 -10,-200" stroke="#3aa86a" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M0,-10C10,-60 -30,-120 -10,-200" stroke="#c8f0d8" stroke-width="3" fill="none" opacity=".6"/></g>`;
  P.book = () => `<g transform="translate(0,118) rotate(-10)"><rect x="-44" y="-60" width="88" height="110" rx="6" fill="#2a5a3a" ${ln(2.6)}/><rect x="-36" y="-52" width="72" height="94" fill="#f4ecd8"/><path d="M-28,-36h50M-28,-20h44M-28,-4h50M-28,12h36" stroke="#5a4a3a" stroke-width="3"/></g>`;
  P.drawing = () => `<g transform="translate(0,118) rotate(-6)"><rect x="-70" y="-110" width="140" height="110" fill="#fbf6e8" ${ln(2.6)}/>${[-50, -30, -10, 10, 30].map((x) => `<g stroke="#2a2a2a" stroke-width="3" fill="none"><circle cx="${x}" cy="-60" r="6"/><path d="M${x},-54v18M${x - 6},-30l6,-6l6,6"/></g>`).join("")}<g stroke="#d8392e" stroke-width="3" fill="none"><path d="M50,-100v40M42,-100h16"/><circle cx="50" cy="-106" r="5"/></g></g>`;
  Object.assign(C, {
    kongBat: { v2: kongV2, hand: P.bat(), keep: "F" }, kongCrate: { v2: { ...kongV2, extra: straps + bandana + P.crateChest() } },
    manHose: { v2: manV2, hand: P.hose(), keep: "F" }, hongBook: { v2: hongV2, hand: P.book(), keep: "B" }, panDraw: { v2: panV2, hand: P.drawing(), keep: "F" },
  });

  // ---------------- poses ----------------
  const M = Rig.MODES, idle = (u, o) => M.idle(u, o);
  M.carry = (u, o) => ({ ...idle(u, o), uaF: -14, faF: -62, uaB: 14, faB: 62, torso: -4, head: -3 });
  M.shamble2 = (u, o) => M.lunge(u, o);
  M.cough = (u, o) => ({ ...idle(u, o), uaF: -110 + 3 * Math.sin(u * 20), faF: -150, uaB: 10, faB: -20, torso: 12 + 5 * Math.abs(Math.sin(u * 9)), head: 14 + 4 * Math.abs(Math.sin(u * 9)), bodyY: 8 });
  M.siphon = (u, o) => ({ ...M.crouch(u, o), uaF: -113, faF: -158, head: 6 });
  M.hold = (u, o) => ({ ...idle(u, o), uaF: -70, faF: -60, head: 4 });
  M.bat = (u, o) => ({ ...idle(u, o), uaF: -160, faF: -30, uaB: -150, faB: -30, torso: -4, head: -2 });
  M.slam = (u, o) => ({ ...idle(u, o), uaF: -86, faF: -8, uaB: -80, faB: -6, torso: 12, thF: 18, shF: 20, thB: -16, bodyY: 8 });
})();
