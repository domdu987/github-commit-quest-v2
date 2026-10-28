// "ผีแม่ม่าย" cast drawn with rig v2 (rig2.js): a family in an Isan village where young men die in their sleep.
//   keng   เก่ง 24, construction worker home from Bangkok, the man the ghost is said to want (sleeps in a white singlet)
//   fon    ฝน 17, his sister, ponytail with a red scrunchie, round glasses, mustard school-club tee — learned CPR from ป้าบัว
//   chan   แม่จันทร์ 50, their mother, widowed when their father died in his sleep at 35
//   samarn ผู้ใหญ่สมาน 62, the village headman in khaki, glasses on his forehead, believes in red shirts
//   bua    ป้าบัว 56, village health volunteer (อสม.) in the blue vest, gives the rules
//   piak   ลุงเปี๊ยก 45, neighbour with a motorbike, fetches the AED
//   docm   หมอ 40, cardiologist at the provincial hospital
//   boss   บอส 10, a cousin (draw at ~0.72 of an adult)
// Variants for props are made in the episode body: { ...Rig.CAST.samarn, hand: Mm.PROP.mic() }.
(function () {
  const { LINE, dk, hi } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round"`;

  // ---------------- hair ----------------
  // an undercut, front view: the top grows from a hairline just above the brows and sweeps up and over; only the temples are
  // clippered, in an opaque stubble tone between skin and hair, so the hair always sits on the head (no skin band under it)
  const undercut = (h, skin) => {
    const stub = Rig2.mix(skin, h.c, 0.42);
    return `
    <path d="M-47,-590C-49,-578 -48,-566 -45,-556L-40,-558Q-40,-574 -37,-593Z" fill="${stub}"/><path d="M52,-592C51,-578 50,-566 48,-556L43,-558Q42,-574 40,-591Z" fill="${stub}"/>
    <g fill="${h.c}" opacity=".55">${[[-44, -584], [-42, -572], [-44, -563], [46, -584], [45, -572], [46, -563]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.4"/>`).join("")}</g>
    <path d="M-47,-590C-54,-630 -22,-656 8,-656C42,-656 64,-632 52,-592Q47,-584 41,-588Q30,-600 16,-596Q2,-606 -12,-597Q-28,-602 -47,-590Z" fill="${h.c}" ${ln()}/>
    <path d="M-32,-608Q0,-644 44,-618M-16,-602Q14,-632 48,-604M-40,-598Q-30,-626 -6,-640" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".7" stroke-linecap="round"/>
    <path d="M-22,-630Q6,-650 34,-638" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/>`;
  };
  // bangs over the forehead, hair tucked behind the ears (the ponytail itself is in back)
  const bangs = (h) => `
    <path d="M-50,-548C-56,-606 -18,-628 4,-628C34,-627 60,-604 52,-548Q48,-566 40,-570Q30,-560 20,-574Q10,-562 -2,-576Q-14,-562 -26,-574Q-36,-560 -44,-566Q-48,-558 -50,-548Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-616Q-36,-592 -28,-574M-2,-624Q-6,-598 -2,-578M26,-618Q32,-596 22,-576" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".75" stroke-linecap="round"/>
    <path d="M-34,-604Q-20,-618 0,-620M10,-620Q28,-618 38,-606" stroke="${h.sh}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>`;
  const ponytail = (h, tie) => `
    <path d="M30,-622C70,-640 92,-600 84,-546C78,-500 92,-468 104,-444Q76,-452 66,-490C58,-526 66,-572 40,-596Z" fill="${dk(h.c, 0.1)}" ${ln()}/>
    <path d="M60,-598Q80,-560 74,-512M70,-610Q92,-570 88,-520" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".7"/>
    <g transform="translate(46,-616) rotate(-28)"><rect x="-13" y="-9" width="26" height="18" rx="8" fill="${tie}" ${ln(2.2)}/><path d="M-8,-4q8,6 16,0" stroke="${dk(tie, 0.3)}" stroke-width="2" fill="none"/></g>`;
  const lowBun = (h) => `<ellipse cx="0" cy="-566" rx="30" ry="22" fill="${dk(h.c, 0.06)}" ${ln()}/><path d="M-20,-574q20,-10 40,0M-22,-562q22,-8 44,0" stroke="${h.s}" stroke-width="2.4" fill="none"/>`;
  const sideSwept = (h) => `
    <path d="M-48,-552C-52,-606 -16,-624 4,-624C30,-623 54,-604 49,-552Q46,-572 34,-584Q18,-592 4,-586Q-14,-594 -30,-584Q-44,-572 -48,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-604Q4,-622 38,-604M-12,-614Q-24,-598 -36,-580" stroke="${h.s}" stroke-width="2.2" fill="none" opacity=".7"/>
    <path d="M-26,-610Q4,-624 34,-608" stroke="${h.sh}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".5"/>`;
  // balding crown with a grey horseshoe of hair and a shine on the scalp
  const horseshoe = (h, skin) => `
    <path d="M-50,-552C-54,-598 -24,-622 2,-622C30,-621 56,-598 51,-552Q46,-572 40,-578Q36,-596 2,-600Q-32,-596 -38,-578Q-46,-572 -50,-552Z" fill="${skin}" ${ln()}/>
    <path d="M-50,-552Q-54,-580 -42,-596Q-40,-576 -36,-566Q-44,-560 -50,-552ZM51,-552Q55,-580 44,-596Q42,-576 38,-566Q46,-560 51,-552Z" fill="${h.c}" ${ln(2)}/>
    <path d="M-14,-612Q4,-620 20,-612" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".35"/>`;
  // short perm: a cap of curls
  const perm = (h) => `
    <path d="M-52,-552C-60,-610 -18,-632 4,-632C34,-631 64,-606 54,-552Q50,-570 42,-574Q32,-566 22,-578Q10,-568 -2,-580Q-14,-568 -26,-578Q-38,-568 -46,-574Q-50,-562 -52,-552Z" fill="${h.c}" ${ln()}/>
    <g fill="none" stroke="${h.s}" stroke-width="2.6" opacity=".75">${[[-36, -604], [-20, -616], [-2, -620], [16, -616], [32, -606], [44, -590], [-46, -588], [-28, -594], [-8, -600], [12, -598], [30, -590]].map(([x, y]) => `<path d="M${x - 6},${y}a6,6 0 1 1 12,0"/>`).join("")}</g>`;
  const bowl = (h) => `
    <path d="M-50,-552C-56,-610 -18,-628 4,-628C32,-627 60,-606 52,-552Q30,-566 2,-566Q-26,-566 -50,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-600Q2,-616 34,-600" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".45"/>`;

  // ---------------- small pieces ----------------
  const roundGlasses = `<g fill="none" stroke="#2a2a2a" stroke-width="3.2"><circle cx="-17" cy="-546" r="14"/><circle cx="19" cy="-546" r="14"/><path d="M-3,-548h8M-31,-550l-14,-4M33,-550l14,-4"/></g>
    <path d="M-24,-554l6,-2M12,-554l6,-2" stroke="#fff" stroke-width="2" opacity=".55"/>`;
  const rectGlasses = `<g fill="none" stroke="#3a3a3a" stroke-width="3.2"><rect x="-31" y="-556" width="27" height="18" rx="5"/><rect x="5" y="-556" width="27" height="18" rx="5"/><path d="M-4,-548h9M-31,-550l-14,-4M32,-550l14,-4"/></g>`;
  const foreheadGlasses = `<g fill="none" stroke="#5a4a3a" stroke-width="3"><rect x="-30" y="-600" width="25" height="14" rx="5" fill="#cfe0e8" fill-opacity=".35"/><rect x="5" y="-600" width="25" height="14" rx="5" fill="#cfe0e8" fill-opacity=".35"/><path d="M-5,-594h10"/></g>`;
  const chain = (c = "#d8d8d0") => `<path d="M-30,-486Q0,-440 30,-486" stroke="${c}" stroke-width="2.6" fill="none"/><rect x="-6" y="-458" width="12" height="16" rx="3" fill="#d8b84a" ${ln(1.6)}/>`;
  // ผ้าขาวม้า: the checked cloth over one shoulder
  const pakaoma = (a = "#c8342a", b = "#2a5a9a") => `<path d="M-50,-484Q-6,-470 36,-300" stroke="${a}" stroke-width="24" fill="none"/><path d="M-50,-484Q-6,-470 36,-300" stroke="${b}" stroke-width="24" fill="none" stroke-dasharray="12 12"/>
    <path d="M-50,-484Q-6,-470 36,-300" stroke="#efe6d6" stroke-width="3" fill="none" stroke-dasharray="4 20"/><path d="M-50,-484Q-6,-470 36,-300" stroke="${LINE}" stroke-width="26" fill="none" opacity=".16"/>`;

  // ---------------- cast ----------------
  C.keng = { v2: {
    skin: "#b47448", iris: "#2a1a12", blush: 0.2, w: 1.06,
    hair: { c: "#17110e", s: "#000", sh: "#5a4a40", front: (x) => undercut(x.hair, x.skin) },
    top: { kind: "tank", c: "#eef0f0", sleeve: "none" },
    print: `<path d="M-22,-404h44v20h-44z" fill="none" stroke="#c8a040" stroke-width="2.4" opacity=".6"/><path d="M-16,-394h32" stroke="#c8a040" stroke-width="3" opacity=".6"/>`,
    bottom: { kind: "shorts", c: "#2e3e5e" }, feet: { kind: "sandal", c: "#3a2a20" },
    extra: chain(),
  } };
  C.kengDay = { v2: { ...C.keng.v2, extra: chain() + pakaoma() } };
  C.fon = { v2: {
    skin: "#e6b48a", iris: "#3a2216", lash: true, blush: 0.5,
    hair: { c: "#2a1a14", s: "#140c08", sh: "#7a5444", front: (x) => bangs(x.hair), back: (x) => ponytail(x.hair, "#d8303a") },
    top: { kind: "tee", c: "#e2a92e", sleeve: "short" },
    print: `<g transform="translate(0,-414)"><circle r="20" fill="#fff4dc" stroke="#9a6a1a" stroke-width="2.4"/><path d="M-2,-12h4v8h8v4h-8v8h-4v-8h-8v-4h8z" fill="#d8303a"/></g>`,
    bottom: { kind: "shorts", c: "#3a5a7a" }, feet: { kind: "bare" },
    faceTop: roundGlasses,
  } };
  C.chan = { v2: {
    skin: "#c08a62", iris: "#2e1e14", blush: 0.3, lip: "#9a3a34", bags: true,
    hair: { c: "#3a3330", s: "#1a1614", sh: "#8a847c", front: (x) => sideSwept(x.hair), back: (x) => lowBun(x.hair) },
    top: { kind: "blouse", c: "#56677a", sleeve: "elbow", trim: "#3e4c5c" },
    bottom: { kind: "sarong", c: "#4a2a3e", band: "#c8a050", band2: "#2a1a26" }, feet: { kind: "sandal", c: "#4a3424" },
    extra: chain("#d8b84a"),
    face: `<path d="M-34,-552l-6,-3M38,-552l6,-3M-12,-530q-6,8 -2,16M22,-530q6,8 2,16" stroke="#8a5a3e" stroke-width="1.8" fill="none" opacity=".7"/>`,
  } };
  C.samarn = { v2: {
    skin: "#a87048", iris: "#2a1a12", blush: 0.25, bags: true, w: 1.12,
    hair: { c: "#a8a49c", s: "#6a665e", sh: "#d8d4cc", front: (x) => horseshoe(x.hair, "#a87048") },
    top: { kind: "shirt", c: "#b39a62", sleeve: "long", neck: "collar", collar: "#a08a54", button: "#e8dcb8" },
    print: `<g transform="translate(-26,-430)"><path d="M-12,-10h24v20h-24z" fill="#8a7444" ${ln(1.8)}/><path d="M-8,-4h16M-8,2h12" stroke="#e8dcb8" stroke-width="2"/></g>
      <g transform="translate(28,-436)"><circle r="12" fill="#d8b84a" ${ln(1.8)}/><path d="M-5,0h10M0,-5v10" stroke="#8a6a1a" stroke-width="2.4"/></g>`,
    bottom: { kind: "trousers", c: "#3a3a32" }, feet: { kind: "sandal", c: "#2a2018" },
    face: `<path d="M-22,-512Q2,-500 24,-512Q2,-520 -22,-512Z" fill="#c8c4bc" ${ln(1.8)}/>`,
    faceTop: foreheadGlasses,
  } };
  C.bua = { v2: {
    skin: "#c48c62", iris: "#2e1e14", blush: 0.45, lip: "#a8442e",
    hair: { c: "#2a2420", s: "#120e0c", sh: "#6a5a50", front: (x) => perm(x.hair) },
    top: { kind: "blouse", c: "#f4f0e6", sleeve: "elbow", trim: "#d8d0c0" },
    // the blue volunteer vest with its badge
    extra: `<path d="M-52,-480L-30,-488L-14,-420L-16,-300H-56Q-60,-400 -52,-480ZM52,-480L30,-488L14,-420L16,-300H56Q60,-400 52,-480Z" fill="#2a64b0" ${ln()}/>
      <path d="M-48,-470L-34,-420M48,-470L34,-420" stroke="#fff" stroke-width="2.4" opacity=".35"/>
      <g transform="translate(-36,-404)"><rect x="-14" y="-8" width="28" height="16" rx="3" fill="#f4f0e6" ${ln(1.6)}/><text x="0" y="5" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="11" fill="#2a64b0">อสม.</text></g>`,
    bottom: { kind: "sarong", c: "#2f6a4a", band: "#e8d8a8", band2: "#1e4a32" }, feet: { kind: "sandal", c: "#4a3a2a" },
    face: `<path d="M-30,-552l-6,-3M34,-552l6,-3" stroke="#8a5a3e" stroke-width="1.8" fill="none" opacity=".6"/>`,
  } };
  C.piak = { v2: {
    skin: "#9a6640", iris: "#2a1a12", blush: 0.2, w: 1.04,
    hair: { c: "#2a2622", sh: "#7a746c", front: (x) => bowl(x.hair) },
    top: { kind: "singlet", c: "#e8e2d4", sleeve: "none" },
    bottom: { kind: "shorts", c: "#8a7a5a" }, feet: { kind: "sandal", c: "#2a2018" },
    extra: pakaoma("#2a7a5a", "#e8c840"),
  } };
  C.docm = { v2: {
    skin: "#e0b088", iris: "#3a2418",
    hair: { c: "#1a1612", s: "#000", sh: "#5a4a40", front: (x) => sideSwept(x.hair) },
    top: { kind: "coat", c: "#f6f6f2", sleeve: "long" },
    bottom: { kind: "trousers", c: "#5a6470" }, feet: { kind: "sneaker", c: "#2a2a2e" },
    print: `<path d="M-14,-470V-420M14,-470V-420" stroke="#7a9ab8" stroke-width="16"/><path d="M-30,-462Q-40,-384 0,-374Q40,-384 30,-462" stroke="#3a3a3a" stroke-width="4.5" fill="none"/><circle cx="0" cy="-372" r="8" fill="#9aa4a8" ${ln(2)}/>
      <rect x="22" y="-430" width="26" height="14" rx="2" fill="#fff" ${ln(1.6)}/><path d="M26,-424h18" stroke="#2a64b0" stroke-width="2"/>`,
    faceTop: rectGlasses,
  } };
  C.boss = { v2: {
    skin: "#d8a078", iris: "#2a1a12", blush: 0.7, headScale: 1.2,
    hair: { c: "#1a1410", sh: "#5a4a40", front: (x) => bowl(x.hair) },
    top: { kind: "tee", c: "#4a9a5a", sleeve: "short" },
    print: `<path d="M-18,-404q6,-20 24,-16q14,4 10,18l8,4h-12l-4,8h-8l2,-8h-10z" fill="#2a6a3a"/><circle cx="12" cy="-412" r="2" fill="#fff"/>`,
    bottom: { kind: "shorts", c: "#c8a050" }, feet: { kind: "bare" },
  } };
})();
