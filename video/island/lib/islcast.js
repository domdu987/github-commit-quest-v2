// "ติดเกาะ" cast drawn with rig v2 (rig2.js): a brother and sister stranded on a deserted islet off a fishing island in the Gulf.
//   fah        ฟ้า 15: a short brown bob with a yellow star clip, a mint tee with a blue whale, khaki shorts, pink strap sandals, a pink
//              wristband (the hand of the opener) · fahBag (the orange crossbody survival bag) · fahCup (a clear plastic cup in the
//              front fist, keep "F") · fahCoco (a young green coconut in the front fist) · fahBagCup (bag + cup)
//   phum       ภูมิ 9 (draw at ~0.74 of an adult): an upturned black fringe, an orange tank top with a green dinosaur, blue swim shorts,
//              bare feet, a snorkel mask hanging on the chest · phumSnack (a snack bag) · phumBottle (a plastic water bottle, level
//              Isl.PROP.bottle(level)) · phumCoco (a young coconut) · phumMirror (the folding mirror, open)
//   jeab       ลุงเจี๊ยบ 42: a red cap worn backwards, a yellow polo with "เจี๊ยบทัวร์" on the chest, olive shorts, black rubber boots,
//              sun-darkened skin
//   wiang      ตาเวียง 68: very dark weathered skin, white hair in a topknot, a thin white beard, an old grey singlet, blue fisherman's
//              trousers rolled to the calf, a red ผ้าขาวม้า round the waist, a shell necklace, bare feet
//              · wiangPaddle (the old carved paddle hanging from the back fist, keep "B")
//   villager   a pier villager: a wet grey tee, rolled jeans, a bucket of fish (bucket in the front fist)
// Poses (Rig.MODES): scoopDrink (crouched, the front hand lifting water to the mouth) · pour (the front hand tips a bottle into the cup
//   in the back hand) · catchRain (face up, mouth open, arms spread) · pullCord (a yanking starter pull, repeating) · holdPaddle (the
//   paddle in the back fist, the front hand on the hip) · pointTree (pointing high up at a palm, head up) · dizzy (swaying, a hand to the
//   brow, knees soft) · stab (lifting a coconut over the head and slamming it down on the stake, repeating) · shout (both hands cupped
//   at the mouth) · sitSand (sitting on the sand, knees up, slumped)
// Props (Isl.PROP, hand props at the palm (0,118)): cup(level) bottle(level) snackBag() coconut() paddle() mirror() · pieces placed
//   anywhere: bagOrange() (the bag with its strap, in body space) cap() (the red cap on its own, for floating) stake() (the sharpened
//   stake planted in sand, 100 units = 1 m) coconutFree(s) (a young coconut lying on the sand)
(function () {
  const { LINE, dk, hi, shade } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const Isl = (window.Isl = window.Isl || {});
  const IC = (window.IslCast = window.IslCast || {});

  Sets.DEFS += `
    <linearGradient id="isFahHair" gradientUnits="userSpaceOnUse" x1="0" y1="-630" x2="0" y2="-480"><stop offset="0" stop-color="#7a5236"/><stop offset=".5" stop-color="#5a3a26"/><stop offset="1" stop-color="#3e2618"/></linearGradient>
    <linearGradient id="isFahHairB" gradientUnits="userSpaceOnUse" x1="0" y1="-620" x2="0" y2="-470"><stop offset="0" stop-color="#4e3220"/><stop offset="1" stop-color="#2e1c10"/></linearGradient>
    <linearGradient id="isBag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffa050"/><stop offset=".5" stop-color="#ff8a3a"/><stop offset="1" stop-color="#d8641e"/></linearGradient>
    <linearGradient id="isCap" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f05a4a"/><stop offset=".55" stop-color="#d8302a"/><stop offset="1" stop-color="#9e1e1a"/></linearGradient>
    <linearGradient id="isPolo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd44a"/><stop offset="1" stop-color="#e8b020"/></linearGradient>
    <linearGradient id="isCoco" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8d868"/><stop offset=".45" stop-color="#7fb043"/><stop offset="1" stop-color="#4e7a2a"/></linearGradient>
    <linearGradient id="isCocoSh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
    <linearGradient id="isPaddle" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a7a52"/><stop offset=".4" stop-color="#c8a878"/><stop offset="1" stop-color="#7a5a3a"/></linearGradient>
    <linearGradient id="isPlastic" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset=".3" stop-color="#ffffff" stop-opacity=".1"/><stop offset=".7" stop-color="#ffffff" stop-opacity=".05"/><stop offset="1" stop-color="#ffffff" stop-opacity=".4"/></linearGradient>
    <linearGradient id="isWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfefff"/><stop offset="1" stop-color="#5ab8e8"/></linearGradient>
    <linearGradient id="isSnack" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a3a"/><stop offset=".5" stop-color="#ffb43a"/><stop offset="1" stop-color="#e8502a"/></linearGradient>
    <linearGradient id="isMirror" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#d8e8f4"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="#8ea6b8"/></linearGradient>
    <linearGradient id="isSingletOld" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b8b4aa"/><stop offset="1" stop-color="#8e8a80"/></linearGradient>
    <pattern id="isPakama" width="22" height="22" patternUnits="userSpaceOnUse"><rect width="22" height="22" fill="#c8302a"/><rect width="11" height="22" fill="#f2c84a" opacity=".55"/><rect width="22" height="11" fill="#f2c84a" opacity=".4"/><path d="M0,5.5H22M5.5,0V22" stroke="#7a1a16" stroke-width="1.6" opacity=".6"/></pattern>
    <pattern id="isCamo" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#6a7a4a"/><path d="M4,8q10,-8 18,2t14,-2q-6,12 -16,10t-12,8q-8,-6 -4,-18z" fill="#4e5c36"/><path d="M26,26q8,-4 12,4q-4,8 -12,6z" fill="#8a9a62"/><circle cx="8" cy="30" r="5" fill="#3a4428"/></pattern>`;

  // ---------------- ฟ้า ----------------
  // a chin-length bob: a full fringe cut straight across the brow with a slight part on her right, the sides falling to the jaw
  const fahFront = (h) => `
    <path d="M-52,-560C-56,-604 -30,-634 4,-634C40,-634 60,-608 54,-560L50,-500Q46,-488 38,-496L40,-556Q24,-572 4,-570Q-16,-572 -40,-556L-38,-500Q-44,-488 -50,-498Z" fill="url(#isFahHair)" ${ln()}/>
    <path d="M-40,-556Q-20,-580 10,-574Q30,-578 40,-556Q30,-588 2,-592Q-26,-590 -40,-556Z" fill="${dk(h.c, 0.22)}" opacity=".55"/>
    <path d="M-36,-606Q-20,-620 0,-618M14,-620Q30,-616 42,-600" stroke="${hi(h.c, 0.35)}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>
    <path d="M-14,-628Q-10,-600 -8,-574M20,-626Q18,-600 20,-574M-46,-560Q-50,-530 -46,-502M48,-560Q52,-530 46,-502" stroke="${h.s}" stroke-width="2.2" fill="none" opacity=".55" stroke-linecap="round"/>
    <g transform="translate(-40,-592) rotate(-18)"><path d="M0,-14L4,-4L15,-4L6,2L9,13L0,7L-9,13L-6,2L-15,-4L-4,-4Z" fill="#ffd23a" ${ln(2)}/><circle cx="-3" cy="-4" r="2" fill="#fff" opacity=".8"/></g>`;
  const fahBack = () => `
    <path d="M-60,-580C-70,-540 -72,-500 -66,-462Q-50,-452 -36,-464L36,-464Q50,-452 66,-462C72,-500 70,-540 60,-580C50,-626 -50,-626 -60,-580Z" fill="url(#isFahHairB)" ${ln()}/>
    <path d="M-50,-560Q-56,-510 -52,-470M50,-560Q56,-510 52,-470" stroke="#1e1208" stroke-width="2.4" fill="none" opacity=".5"/>`;
  const whale = `<g transform="translate(-2,-396)"><path d="M-34,0Q-26,-26 6,-24Q30,-22 36,-6L48,-18L46,2L48,20L36,8Q28,22 6,22Q-24,22 -34,0Z" fill="#2a6ac8" ${ln(2.2)}/>
    <path d="M-30,2Q-6,16 24,10" stroke="#9ad0ff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/><circle cx="-16" cy="-6" r="3.2" fill="#fff" ${ln(1.2)}/><circle cx="-15" cy="-6" r="1.5" fill="${LINE}"/>
    <path d="M-6,-24q-2,-10 4,-16M-6,-24q4,-8 10,-10" stroke="#9ad0ff" stroke-width="3" fill="none" stroke-linecap="round"/></g>`;
  const fahV2 = {
    skin: "#ebbd95", iris: "#3a2418", lash: true, blush: 0.7, lip: "#d0666e", w: 1.02,
    hair: { c: "#5a3a26", s: "#2e1c10", sh: "#9a7452", front: (x) => fahFront(x.hair), back: () => fahBack() },
    top: { kind: "tee", c: "#9fe0c8", sleeve: "short", trim: "#6ab8a0" },
    print: whale,
    bottom: { kind: "shorts", c: "#c8b48a" }, feet: { kind: "sandal", c: "#e87a8a" },
    wristband: "#ff7eb0",
  };
  C.fah = { v2: fahV2 };
  // the orange crossbody bag: the strap over the right shoulder, the bag on the left hip (body space, drawn in #id-acc)
  const bagOrange = () => `<g>
    <path d="M44,-486Q10,-420 -40,-330" stroke="${LINE}" stroke-width="16" stroke-linecap="round"/><path d="M44,-486Q10,-420 -40,-330" stroke="#c8521a" stroke-width="10" stroke-linecap="round"/><path d="M42,-480Q10,-420 -36,-336" stroke="#ffb070" stroke-width="3" fill="none" opacity=".6"/>
    <g transform="translate(-58,-330) rotate(8)"><rect x="-44" y="-10" width="88" height="70" rx="12" fill="#b84a12" ${ln(2.6)}/><rect x="-44" y="-30" width="88" height="40" rx="12" fill="url(#isBag)" ${ln(2.6)}/>
      <path d="M-44,10H44" stroke="#8a2e08" stroke-width="2"/><rect x="-10" y="4" width="20" height="14" rx="4" fill="#2a2a30" ${ln(1.6)}/><path d="M-30,-20h18M14,-20h18" stroke="#ffd0a0" stroke-width="3" opacity=".55" stroke-linecap="round"/>
      <path d="M-36,30q8,-4 16,0M18,34q8,-4 16,0" stroke="#7a2a08" stroke-width="2" fill="none" opacity=".5"/><circle cx="30" cy="-18" r="6" fill="#ffd23a" ${ln(1.4)}/></g></g>`;
  C.fahBag = { v2: { ...fahV2, extra: bagOrange() } };

  // ---------------- ภูมิ ----------------
  // a bowl of black hair with the fringe flicked up in three tufts; the hairline sits above the brows
  const phumFront = (h) => `
    <path d="M-48,-556C-52,-600 -28,-628 2,-628C32,-628 54,-600 50,-556Q48,-572 42,-578Q30,-566 20,-574Q10,-570 2,-576Q-8,-570 -18,-574Q-30,-566 -40,-578Q-46,-572 -48,-556Z" fill="${h.c}" ${ln()}/>
    <path d="M-34,-606Q-48,-640 -36,-662Q-24,-640 -14,-626Q-12,-656 4,-672Q18,-654 16,-626Q28,-642 44,-660Q50,-634 38,-606Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-610Q2,-624 36,-608" stroke="${h.sh}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".45"/>
    <path d="M-30,-630l-4,-16M2,-636l2,-18M34,-630l6,-14" stroke="${h.sh}" stroke-width="2.6" opacity=".6" stroke-linecap="round"/>
    <path d="M-46,-560v16M48,-560v14" stroke="${h.c}" stroke-width="6" stroke-linecap="round"/>`;
  const dino = `<g transform="translate(-6,-394)"><path d="M-30,10Q-30,-14 -8,-16L10,-30Q20,-34 24,-24L20,-14Q34,-12 36,0L30,4L26,0L22,8L14,8L12,14L4,14L4,8L-8,8L-10,14L-18,14L-18,6Q-30,8 -30,10Z" fill="#4caf50" ${ln(2.2)}/>
    <path d="M-8,-16l-4,-8l6,2l0,-8l6,4l2,-6l4,8" fill="#2e7d32" ${ln(1.4)}/><circle cx="14" cy="-24" r="2.6" fill="#fff" ${ln(1.2)}/><circle cx="15" cy="-24" r="1.2" fill="${LINE}"/>
    <path d="M-22,-2q10,10 22,6" stroke="#a5d6a7" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/><path d="M26,-20q6,2 8,-4" stroke="${LINE}" stroke-width="1.6" fill="none"/></g>`;
  // the snorkel mask hanging on the chest from its strap round the neck
  const mask = `<g><path d="M-26,-488Q-28,-456 -8,-430M26,-488Q28,-456 10,-430" stroke="${LINE}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-26,-488Q-28,-456 -8,-430M26,-488Q28,-456 10,-430" stroke="#2a2a30" stroke-width="4" fill="none" stroke-linecap="round"/>
    <g transform="translate(0,-404) rotate(-10)"><path d="M-40,-18Q-42,-36 -22,-36H22Q42,-36 40,-18L36,14Q30,26 12,24L4,12L-4,12L-12,24Q-30,26 -36,14Z" fill="#1e5aa8" ${ln(2.4)}/>
      <path d="M-34,-26H-6V12H-30ZM6,-26H34V12H10Z" fill="#bfe8f4" ${ln(1.8)}/><path d="M-30,-20l16,22M12,-20l16,22" stroke="#fff" stroke-width="4" opacity=".7" stroke-linecap="round"/>
      <path d="M-4,12q4,-6 8,0" stroke="${LINE}" stroke-width="2" fill="none"/><path d="M34,-30q12,-20 10,-46" stroke="#ff8a3a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M34,-30q12,-20 10,-46" stroke="#ffc08a" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/></g></g>`;
  const phumV2 = {
    skin: "#e0a878", iris: "#2e1c12", blush: 0.7, headScale: 1.2, w: 0.92, limb: 0.92,
    hair: { c: "#16100c", s: "#060404", sh: "#5a4a40", front: (x) => phumFront(x.hair) },
    top: { kind: "tank", c: "#ff9a4a", sleeve: "none" },
    print: dino,
    bottom: { kind: "shorts", c: "#2a5ab8" }, feet: { kind: "bare" },
    extra: mask,
  };
  C.phum = { v2: phumV2 };

  // ---------------- ลุงเจี๊ยบ ----------------
  // short dark hair under a red cap worn backwards: the bill sticks out behind on his left; the strap and the button face us
  const jeabHair = (h) => `<path d="M-46,-556C-50,-592 -28,-616 2,-616C30,-616 52,-594 48,-556Q44,-568 36,-574Q4,-586 -34,-574Q-44,-568 -46,-556Z" fill="${h.c}" ${ln()}/>`;
  const capBack = `<g transform="translate(0,-610)">
    <path d="M-30,10L-78,4Q-96,2 -94,-8L-84,-16Q-60,-12 -32,-8Z" fill="#9e1e1a" ${ln(2.4)}/>
    <path d="M-50,26C-56,-16 -30,-36 2,-36C34,-36 58,-14 54,26Q30,34 2,34Q-26,34 -50,26Z" fill="url(#isCap)" ${ln(2.6)}/>
    <path d="M-50,26Q2,40 54,26L52,36Q2,50 -48,36Z" fill="#7a1612" ${ln(2.2)}/><path d="M-10,36h22v8h-22z" fill="#3a3a3a" ${ln(1.6)}/>
    <path d="M-30,-20Q2,-30 36,-20M-40,0Q2,-10 46,0" stroke="#ff8a7a" stroke-width="2.6" fill="none" opacity=".45"/><path d="M2,-36V30" stroke="#8a1a16" stroke-width="2" opacity=".6"/><circle cx="2" cy="-36" r="5" fill="#b02420" ${ln(1.6)}/></g>`;
  const poloPrint = `<g transform="translate(-40,-424)"><text x="0" y="0" font-family="Kanit" font-weight="700" font-size="13" fill="#1e3a8a">เจี๊ยบทัวร์</text><path d="M0,6h58" stroke="#1e3a8a" stroke-width="1.6"/>
    <path d="M62,-14q6,-8 12,0t12,0" stroke="#1e3a8a" stroke-width="2.6" fill="none"/></g>`;
  const jeabV2 = {
    skin: "#c8906a", iris: "#2e1c12", blush: 0.25, w: 1.08, limb: 1.05,
    hair: { c: "#2a1c14", s: "#120a06", sh: "#4e3a2a", front: (x) => jeabHair(x.hair) },
    top: { kind: "tee", c: "#f2c030", sleeve: "short", neck: "collar", collar: "#e8b020", button: "#fff4d0", trim: "#d8a018" },
    print: poloPrint,
    bottom: { kind: "shorts", c: "#6a7a4a" }, feet: { kind: "boot", c: "#1e1e22" },
    faceTop: capBack,
    face: `<path d="M-14,-532q-6,8 -2,16M24,-532q6,8 2,16M-30,-594q12,-5 24,0M8,-594q12,-5 24,0" stroke="#8a5a3a" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/>`,
  };
  C.jeab = { v2: jeabV2 };

  // ---------------- ตาเวียง ----------------
  // thin white hair swept back into a topknot, a thin white beard and moustache, deep lines; the skin very dark from the sun
  const wiangFront = (h) => `
    <path d="M-46,-560C-48,-592 -30,-610 2,-612C32,-612 50,-594 48,-560Q44,-574 32,-580Q4,-590 -30,-580Q-44,-574 -46,-560Z" fill="${h.c}" ${ln(2)}/>
    <path d="M-30,-580Q2,-600 36,-580" stroke="${h.s}" stroke-width="2" fill="none" opacity=".6"/><path d="M-40,-570l-4,10M44,-570l4,10" stroke="${h.c}" stroke-width="4" stroke-linecap="round"/>`;
  const wiangKnot = (h) => `<g transform="translate(6,-626)"><path d="M-10,8Q-8,-26 14,-30Q34,-28 30,-4Q26,10 8,12Z" fill="${h.c}" ${ln(2)}/><path d="M-4,-6q12,-14 26,-8M-2,2q14,-6 26,-4" stroke="${h.s}" stroke-width="2" fill="none"/>
    <path d="M-16,12Q-2,-4 14,-4" stroke="#c8402e" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M-14,14l-12,10" stroke="#c8402e" stroke-width="4" stroke-linecap="round"/></g>`;
  const beard = `<g><path d="M-36,-530Q-30,-500 -8,-492Q4,-490 16,-492Q38,-500 44,-530Q42,-508 30,-498Q4,-484 -22,-498Q-34,-508 -36,-530Z" fill="#ece8de" ${ln(2)} opacity=".95"/>
    <path d="M-8,-522q12,-5 24,0q-6,6 -12,6q-6,0 -12,-6z" fill="#ece8de" ${ln(1.6)}/>
    <path d="M-30,-510q6,10 14,12M38,-510q-6,10 -14,12M-14,-496q18,6 36,0" stroke="#bcb8ae" stroke-width="1.8" fill="none"/>
    <path d="M-16,-534q-7,10 -3,19M24,-534q7,10 3,19M-40,-552l-8,-3M-40,-545l-8,1M44,-552l8,-3M44,-545l8,1M-26,-596q12,-4 24,0M8,-596q12,-4 22,0M-26,-586h22M10,-586h20" stroke="#5a3218" stroke-width="2" fill="none" stroke-linecap="round" opacity=".7"/></g>`;
  const pakamaW = `<path d="M-50,-336Q0,-322 52,-336L54,-306Q0,-292 -52,-306Z" fill="url(#isPakama)" ${ln(2.4)}/><path d="M32,-312Q44,-270 36,-220L56,-224Q62,-272 50,-316Z" fill="url(#isPakama)" ${ln(2.2)}/><path d="M36,-220h20" stroke="#f4e6c8" stroke-width="3" stroke-dasharray="3 3"/>`;
  const shells = `<path d="M-24,-486Q0,-452 26,-486" stroke="#8a6a4a" stroke-width="2.4" fill="none"/>${[[-20, -478], [-10, -466], [0, -461], [10, -466], [20, -478]].map(([x, y]) => `<path d="M${x},${y - 6}q-6,4 -4,10q4,4 8,0q2,-6 -4,-10z" fill="#f4e8d8" ${ln(1.4)}/>`).join("")}`;
  const singletHoles = `<g><circle cx="-18" cy="-380" r="4" fill="#8a5a3a" opacity=".8"/><circle cx="26" cy="-346" r="3" fill="#8a5a3a" opacity=".8"/><path d="M-40,-420q10,30 4,60M36,-410q-6,30 2,56" stroke="#7a766c" stroke-width="2.2" fill="none" opacity=".6"/><path d="M-30,-460q18,6 38,-2" stroke="#d8d4ca" stroke-width="3" fill="none" opacity=".4"/></g>`;
  const rolled = (c, k = 1) => (side) => {
    const cc = side === "B" ? dk(c, 0.1) : c, cf = hi(cc, 0.16), a = 46 * k / 2, b = 36 * k / 2, s0 = 35 * k / 2;
    return {
      thigh: Rig2.paint(Rig2.limbD(152, 2 * a + 12, 2 * b + 14), cc, { ao: true }) + `<path d="M${-a + 8},26q8,44 2,96M${a - 6},54q-6,34 -2,80" stroke="${dk(cc, 0.3)}" stroke-width="2.2" fill="none" opacity=".55"/>`,
      shin: Rig2.paint(`M${-s0 - 6},-8Q0,-14 ${s0 + 6},-8L${s0 + 9},66H${-s0 - 9}Z`, cc) + `<path d="M${-s0 - 11},60Q0,53 ${s0 + 11},60L${s0 + 10},80Q0,87 ${-s0 - 10},80Z" fill="${cf}" ${ln(2.4)}/><path d="M${-s0 - 9},70Q0,65 ${s0 + 9},70" stroke="${dk(cf, 0.28)}" stroke-width="2" fill="none"/>`,
    };
  };
  const wiangV2 = {
    skin: "#8a5a3a", iris: "#2a1a12", blush: 0.1, bags: true, w: 0.94, limb: 0.88, brow: "#ece8de",
    hair: { c: "#ece8de", s: "#a8a49c", sh: "#ffffff", front: (x) => wiangFront(x.hair), back: (x) => wiangKnot(x.hair) },
    top: { kind: "singlet", c: "#a8a49a", sleeve: "none" },
    print: singletHoles,
    bottom: { kind: "shorts", c: "#2a3a6a" }, feet: { kind: "bare" }, legs: rolled("#2a3a6a", 0.9),
    extra: pakamaW + shells,
    face: beard,
  };
  C.wiang = { v2: wiangV2 };

  // ---------------- a pier villager ----------------
  const villV2 = {
    skin: "#c49a74", iris: "#2e1c12", blush: 0.2, w: 1.0,
    hair: { c: "#1e1410", s: "#0a0604", sh: "#4a3a30", front: (x) => jeabHair(x.hair) },
    top: { kind: "tee", c: "#8a9298", sleeve: "short", trim: "#6a7278" },
    print: `<path d="M-30,-440q20,40 0,110M20,-430q-10,50 10,100" stroke="#5a6268" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>`,
    bottom: { kind: "jeans", c: "#4a5a7a" }, feet: { kind: "bare" },
  };
  C.villager = { v2: villV2 };

  // ---------------- props in the hand (the palm is at (0,118) of the hand group) ----------------
  const cup = (level = 0.5) => `<g transform="translate(0,118) rotate(-6)"><path d="M-22,-30H22L18,34Q0,40 -18,34Z" fill="#bfe4f0" opacity=".35" ${ln(2.2)}/>
    ${level > 0 ? `<path d="M${-22 + (1 - level) * 3},${34 - level * 62}H${22 - (1 - level) * 3}L18,34Q0,40 -18,34Z" fill="url(#isWater)" opacity=".85"/><path d="M${-20 + (1 - level) * 3},${34 - level * 62}H${20 - (1 - level) * 3}" stroke="#fff" stroke-width="2.4" opacity=".8"/>` : ""}
    <path d="M-22,-30H22L18,34Q0,40 -18,34Z" fill="url(#isPlastic)"/><path d="M-22,-30H22" stroke="#fff" stroke-width="3" opacity=".7"/></g>`;
  const bottle = (level = 0.5) => `<g transform="translate(0,118) rotate(-4)"><path d="M-16,-66H16V-56Q22,-50 22,-40V40Q22,52 10,52H-10Q-22,52 -22,40V-40Q-22,-50 -16,-56Z" fill="#dff2f8" opacity=".4" ${ln(2.2)}/>
    ${level > 0 ? `<path d="M-20,${52 - level * 92}H20V40Q20,50 10,50H-10Q-20,50 -20,40Z" fill="url(#isWater)" opacity=".9"/><path d="M-18,${52 - level * 92}H18" stroke="#fff" stroke-width="2.2" opacity=".8"/>` : ""}
    <rect x="-13" y="-78" width="26" height="14" rx="3" fill="#2a8ad0" ${ln(2)}/><path d="M-22,-10h44M-22,10h44" stroke="#8ad0e8" stroke-width="2" opacity=".5"/>
    <rect x="-18" y="-20" width="36" height="30" fill="#2a8ad0" opacity=".85"/><text x="0" y="0" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="11" fill="#fff">น้ำดื่ม</text>
    <path d="M-16,-66H16V-56Q22,-50 22,-40V40Q22,52 10,52H-10Q-22,52 -22,40V-40Q-22,-50 -16,-56Z" fill="url(#isPlastic)"/></g>`;
  const snackBag = () => `<g transform="translate(0,118) rotate(10)"><path d="M-24,-8Q-30,-18 -22,-22H22Q30,-18 24,-8L28,70Q0,82 -28,70Z" fill="url(#isSnack)" ${ln(2.4)}/>
    <path d="M-22,-22H22" stroke="#fff" stroke-width="4" opacity=".6"/><path d="M-24,-8H24" stroke="#c83a18" stroke-width="2" opacity=".6"/>
    <ellipse cx="0" cy="30" rx="16" ry="18" fill="#fff6c8" ${ln(1.6)}/><path d="M-8,22q8,-6 16,0q-4,10 -8,12q-6,-2 -8,-12z" fill="#e8582a"/><text x="0" y="52" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="10" fill="#fff">กรอบ!</text>
    <path d="M-18,-4q6,30 2,66M20,-2q-4,30 2,64" stroke="#fff" stroke-width="2" fill="none" opacity=".35"/></g>`;
  const coconutArt = (s = 1) => `<g transform="scale(${s})"><ellipse cx="0" cy="0" rx="44" ry="50" fill="url(#isCoco)" ${ln(2.8)}/><ellipse cx="0" cy="0" rx="44" ry="50" fill="url(#isCocoSh)"/>
    <path d="M-30,-20Q-10,-44 20,-36" stroke="#d8f0a0" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/><path d="M-6,-50q-10,-6 -14,-16q10,4 14,16z" fill="#7a5a2a" ${ln(1.8)}/>
    <path d="M-20,20Q0,8 22,22M-14,36Q0,28 14,38" stroke="#5a8a30" stroke-width="2.6" fill="none" opacity=".5"/></g>`;
  const coconut = () => `<g transform="translate(0,118)">${coconutArt(0.86)}</g>`;
  // the paddle: an old wooden paddle with a T-grip, hanging blade-down from the fist; the rules carved faintly along the blade
  const paddle = () => `<g transform="translate(0,118) rotate(6)"><path d="M-24,-40H24" stroke="${LINE}" stroke-width="18" stroke-linecap="round"/><path d="M-24,-40H24" stroke="#9a7a52" stroke-width="12" stroke-linecap="round"/>
    <path d="M0,-40V160" stroke="${LINE}" stroke-width="20" stroke-linecap="round"/><path d="M0,-40V160" stroke="url(#isPaddle)" stroke-width="14" stroke-linecap="round"/>
    <path d="M-24,150Q-36,230 -28,330Q0,350 28,330Q36,230 24,150Q0,140 -24,150Z" fill="url(#isPaddle)" ${ln(2.8)}/>
    <path d="M-16,170q-4,60 0,140M14,176q4,60 0,130" stroke="#7a5a3a" stroke-width="2" fill="none" opacity=".55"/>
    ${["กระหาย", "พิษไหม้", "เรือไกล"].map((t, k) => `<text x="0" y="${200 + k * 40}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="16" fill="#4a3018" opacity=".8">${t}</text>`).join("")}
    <path d="M-30,166q4,-10 10,-14" stroke="#fff" stroke-width="3" opacity=".3" stroke-linecap="round"/></g>`;
  const mirror = () => `<g transform="translate(0,118) rotate(-12)"><path d="M-30,-28Q-34,-74 0,-76Q34,-74 30,-28Z" fill="#ff8ab8" ${ln(2.2)}/><path d="M-26,-30Q-28,-66 0,-68Q28,-66 26,-30Z" fill="url(#isMirror)" ${ln(1.6)}/>
    <path d="M-14,-56L-2,-62" stroke="#fff" stroke-width="4" stroke-linecap="round"/><ellipse cx="0" cy="-10" rx="32" ry="12" fill="#ff8ab8" ${ln(2.2)}/><ellipse cx="0" cy="-12" rx="28" ry="8" fill="#ffc0d8"/></g>`;
  const bucketFish = () => `<g transform="translate(0,118)"><path d="M-30,30Q0,-34 30,30" stroke="${LINE}" stroke-width="5" fill="none"/><path d="M-30,30Q0,-34 30,30" stroke="#e8eef4" stroke-width="2.4" fill="none"/>
    <g transform="translate(0,34)"><path d="M-34,0H34L28,70Q0,78 -28,70Z" fill="#6a8a40" ${ln(2.6)}/><ellipse cx="0" cy="0" rx="34" ry="8" fill="#3e5a28" ${ln(2.4)}/><path d="M-14,-2Q-24,-26 -12,-34L-6,-20Z" fill="#9ab8c8" ${ln(1.8)}/><path d="M8,-2Q20,-30 10,-38L2,-22Z" fill="#c8b45a" ${ln(1.8)}/></g></g>`;
  // free-standing pieces
  const cap = (s = 1) => `<g transform="scale(${s})"><path d="M-54,10C-60,-32 -32,-52 2,-52C36,-52 60,-30 56,10Q30,20 2,20Q-26,20 -54,10Z" fill="url(#isCap)" ${ln(2.8)}/><path d="M54,8L104,0Q116,-2 112,8L104,16Q78,14 52,20Z" fill="#9e1e1a" ${ln(2.4)}/>
    <path d="M-54,10Q2,26 56,10L54,22Q2,36 -52,22Z" fill="#7a1612" ${ln(2.2)}/><path d="M2,-52V14" stroke="#8a1a16" stroke-width="2" opacity=".6"/><circle cx="2" cy="-52" r="5" fill="#b02420" ${ln(1.6)}/><path d="M-30,-34Q2,-44 36,-34" stroke="#ff8a7a" stroke-width="3" fill="none" opacity=".45"/></g>`;
  // the stake: a sharpened hardwood stake driven into the sand, point up, old and sun-bleached, 100 units = 1 m (point at (0,-100))
  const stake = (s = 1) => `<g transform="scale(${s})"><ellipse cx="6" cy="6" rx="34" ry="10" fill="#000" opacity=".25"/>
    <path d="M-13,0L-10,-250L0,-340L10,-250L13,0Z" fill="#b89a74" ${ln(2.8)}/><path d="M-10,-250L0,-340L10,-250Z" fill="#e8d8b8" ${ln(2.2)}/><path d="M-5,-20q-3,-100 0,-210M6,-24q3,-96 0,-200" stroke="#7a5a3a" stroke-width="2.2" fill="none" opacity=".6"/>
    <path d="M-12,-60q12,-5 24,0M-11,-130q11,-5 22,0M-10,-200q10,-4 20,0" stroke="#5a4028" stroke-width="2.4" fill="none" opacity=".5"/><ellipse cx="0" cy="0" rx="16" ry="6" fill="#8a6a44" opacity=".6"/></g>`;
  const coconutFree = (s = 1) => `<g transform="scale(${s})"><ellipse cx="6" cy="40" rx="48" ry="12" fill="#000" opacity=".22"/><g transform="rotate(-18)">${coconutArt(1)}</g></g>`;
  Isl.PROP = Object.assign(Isl.PROP || {}, { cup, bottle, snackBag, coconut, paddle, mirror, bagOrange, cap, stake, coconutFree, bucketFish });
  IC.PROP = Isl.PROP;

  // variants that hold things (keep: the fist that holds the prop; the build hook in tidecast.js clears the other one)
  C.fahCup = { v2: fahV2, hand: cup(0.6), keep: "F" };
  C.fahBagCup = { v2: C.fahBag.v2, hand: cup(0.6), keep: "F" };
  C.fahCoco = { v2: fahV2, hand: coconut(), keep: "F" };
  C.phumSnack = { v2: phumV2, hand: snackBag(), keep: "F" };
  C.phumBottle = { v2: phumV2, hand: bottle(0.5), keep: "F" };
  C.phumBottleEmpty = { v2: phumV2, hand: bottle(0), keep: "F" };
  C.phumCoco = { v2: phumV2, hand: coconut(), keep: "F" };
  C.phumMirror = { v2: phumV2, hand: mirror(), keep: "F" };
  C.wiangPaddle = { v2: wiangV2, hand: paddle(), keep: "B" };
  C.villagerBucket = { v2: villV2, hand: bucketFish(), keep: "F" };

  // ---------------- poses ----------------
  const M = Rig.MODES;
  // crouched at the water's edge, the front hand scooping and lifting to the mouth (a slow lift, a pause, a drop back)
  M.scoopDrink = (u, o) => { const p = (u % 2.6) / 2.6, lift = p < 0.35 ? p / 0.35 : p < 0.7 ? 1 : 1 - (p - 0.7) / 0.3, e = lift * lift * (3 - 2 * lift);
    return { ...M.crouch(u, o), uaF: -40 - 70 * e, faF: -70 - 86 * e, uaB: -20, faB: -40, torso: 26 - 8 * e, head: 10 - 14 * e }; };
  // standing, the front hand tipping a bottle into the cup held in the back hand
  M.pour = (u, o) => ({ ...M.idle(u, o), uaF: -34 + 2 * Math.sin(u * 1.4), faF: -62, uaB: -30, faB: -96, torso: 4, head: 14 });
  // face to the sky, mouth open, arms out wide
  M.catchRain = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.2); return { ...M.idle(u, o), uaF: -118 + 3 * b, faF: -22, uaB: 118 - 3 * b, faB: 22, torso: -8, head: -26 + 2 * b, bodyY: -2 }; };
  // the starter cord: a crouching lean, the front arm yanks back over and over
  M.pullCord = (u, o) => { const p = (u % 0.9) / 0.9, k = p < 0.3 ? p / 0.3 : 1 - (p - 0.3) / 0.7, e = k * k; return { ...M.idle(u, o), thF: -12, shF: 18, thB: 8, shB: 6, uaF: -20 - 70 * e, faF: -60 + 40 * e, uaB: -10, faB: -30, torso: 18 - 14 * e, head: -4 + 6 * e, bodyY: 10 - 6 * e }; };
  // the paddle hanging from the back fist, the front hand on the hip
  M.holdPaddle = (u, o) => ({ ...M.idle(u, o), uaF: 14 + Math.sin(u * 1.3), faF: -112, uaB: 12, faB: -8, torso: 1, head: 2 + 2 * Math.sin(u * 0.8) });
  // pointing high at the crown of a palm, head tipped back
  M.pointTree = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.6); return { ...M.idle(u, o), uaF: -150 + 3 * b, faF: -6, uaB: 10, faB: -14, torso: -5, head: -18, bodyY: -2 }; };
  // dizzy: a slow sway, knees soft, the front hand pressed to the brow
  M.dizzy = (u, o) => { const s = Math.sin(u * 1.9), s2 = Math.sin(u * 3.1); return { ...M.idle(u, o), thF: -6, shF: 14, thB: 4, shB: 10, uaF: -112 + 3 * s2, faF: -140, uaB: -8 + 6 * s, faB: -20, torso: 6 + 7 * s, head: 8 + 9 * s2, bodyY: 14 + 4 * s, rootR: 3 * s }; };
  // stab: the coconut goes up over the head in both hands, then slams down onto the stake; repeats every 1.4 s
  M.stab = (u, o) => { const p = (u % 1.4) / 1.4, k = p < 0.55 ? p / 0.55 : 1 - (p - 0.55) / 0.45, e = p < 0.55 ? k * k * (3 - 2 * k) : 1 - Math.pow(1 - k, 2);
    return { ...M.idle(u, o), uaF: -40 - 118 * e, faF: -30 + 10 * e, uaB: 40 + 118 * e, faB: 30 - 10 * e, torso: 22 - 30 * e, head: 10 - 20 * e, bodyY: 10 - 12 * e, thF: -4, shF: 8 }; };
  // both hands cupped at the mouth, calling out to sea
  M.shout = (u, o) => { const j = Math.sin(u * 7) * 1.2; return { ...M.idle(u, o), uaF: -95 + j, faF: -150, uaB: 95 - j, faB: 150, torso: -5, head: -8, bodyY: -2 }; };
  // sitting on the sand, knees up, slumped forward (fah in the shade)
  M.sitSand = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 3.4); return { ...M.idle(u, o), thF: -98, shF: 112, thB: -92, shB: 108, torso: 14 + 0.6 * b, head: 12, uaF: -24, faF: -30, uaB: -14, faB: -28, bodyY: 230 }; };
})();
