// "ต่อหัวเสือ" cast drawn with rig v2: school holidays at ยาย's house in the village, the cool season.
// Built on the channel's v2 bodies (tidecast / popcast) with this story's own hair, clothes and props, so each reads at a glance:
//   phum     ภูมิ 10 (draw ~0.76 of an adult): spiky hair under a red cap worn backwards, a lime tee with a slingshot print,
//            khaki shorts, sandals · phumSling (the slingshot in the front fist)
//   toey     เตย 15: long black hair in a high ponytail, white earbuds, a black tee with a pastel-pink heart, light jeans, white sneakers
//            · toeyPhone (phone in the hand)
//   yaiBua   ยายบัว 68: grey bun with a jasmine garland, a lilac lace blouse, a dark-green pha sin, a ผ้าขาวม้า on the shoulder
//   lungSing ลุงสิงห์ 55 (the neighbour the kids call crazy): a wide straw hat, a long-sleeved faded blue work shirt buttoned to the wrist,
//            a towel round the neck, loose dark trousers, rubber boots — dressed against stings even on a hot day (the clue in EP.1)
// Poses: swat (both forearms flailing in front of the face) · cover (both arms over the head, hunched) · runCover (running with an arm over the head)
//   · aim (slingshot drawn back) · scratch (rubbing the forearm) · beckon (waving someone in through a door)
(function () {
  const { LINE, dk } = Rig2;
  const C = Rig.CAST, M = Rig.MODES;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const base = (k) => (C[k] && C[k].v2) || {};

  // ---------------- props ----------------
  const sling = () => `<g transform="translate(0,118)"><path d="M0,10v36" stroke="#7a4a26" stroke-width="9" stroke-linecap="round"/><path d="M0,12L-16,-26M0,12L16,-26" stroke="#7a4a26" stroke-width="8" stroke-linecap="round"/>
    <path d="M-16,-26Q0,4 16,-26" stroke="#d8382a" stroke-width="3" fill="none"/></g>`;
  const phone = () => `<g transform="translate(0,118) rotate(-10)"><rect x="-13" y="-26" width="26" height="46" rx="5" fill="#2a2a32" ${ln(2)}/><rect x="-10" y="-22" width="20" height="36" rx="2" fill="#8ac8f0"/></g>`;

  // ---------------- ภูมิ ----------------
  const cap = `<g><path d="M-50,-586C-50,-628 50,-630 52,-586Z" fill="#d8302a" ${ln()}/><path d="M-52,-586Q-80,-584 -96,-574Q-74,-566 -48,-576Z" fill="#b8241e" ${ln(2.2)}/>
    <path d="M-20,-622Q4,-630 30,-620" stroke="#ff7a6a" stroke-width="5" fill="none" stroke-linecap="round" opacity=".6"/><circle cx="2" cy="-628" r="4" fill="#b8241e"/></g>`;
  const slingPrint = `<g transform="translate(0,-400)"><path d="M0,14v18M0,14L-12,-12M0,14L12,-12" stroke="#2e5a1a" stroke-width="5" stroke-linecap="round" fill="none"/><path d="M-12,-12Q0,6 12,-12" stroke="#d8302a" stroke-width="2.6" fill="none"/><circle cx="20" cy="-20" r="5" fill="#2e5a1a"/></g>`;
  C.phum = { v2: { ...base("tang"), face: "", faceTop: cap, top: { kind: "tee", c: "#a6d84a", sleeve: "short" }, print: slingPrint,
    bottom: { kind: "shorts", c: "#a8946a" }, feet: { kind: "sandal", c: "#2a5a9a" } } };
  C.phumSling = { ...C.phum, hand: sling(), keep: "F" };

  // ---------------- เตย ----------------
  const pony = `<path d="M30,-628C60,-640 82,-610 74,-560C70,-520 80,-490 92,-470Q60,-480 56,-530Q54,-580 30,-606Z" fill="#1a1412" ${ln()}/><circle cx="34" cy="-626" r="9" fill="#ec5e9e" ${ln(1.8)}/>`;
  const buds = `<g><circle cx="-50" cy="-528" r="6" fill="#fff" ${ln(1.6)}/><circle cx="52" cy="-528" r="6" fill="#fff" ${ln(1.6)}/><path d="M-50,-522q-4,60 10,110M52,-522q6,60 -10,110" stroke="#f4f4f4" stroke-width="2.4" fill="none"/></g>`;
  const heart = `<g transform="translate(0,-404)"><path d="M0,16C-30,-4 -22,-28 -8,-26C-2,-25 0,-20 0,-16C0,-20 2,-25 8,-26C22,-28 30,-4 0,16Z" fill="#ffb4c8" ${ln(2)}/></g>`;
  const mintV = base("mint");
  C.toey = { v2: { ...mintV, hair: { ...(mintV.hair || {}), c: "#1a1412", back: (x) => pony }, faceTop: buds, top: { kind: "tee", c: "#2a2a30", sleeve: "short" }, print: heart,
    bottom: { kind: "jeans", c: "#9ec0e0" }, feet: { kind: "sneaker", c: "#f6f4ee", mark: "#ec5e9e" } } };
  C.toeyPhone = { ...C.toey, hand: phone(), keep: "F" };

  // ---------------- ยายบัว ----------------
  const yv = base("yaiTide");
  const jasmine = `<g>${Array.from({ length: 7 }, (_, k) => `<circle cx="${-58 + k * 6}" cy="${-640 + Math.sin(k) * 6 + k * 4}" r="5" fill="#fffef4" stroke="#c8c4a8" stroke-width="1.2"/>`).join("")}</g>`;
  const pakama = `<path d="M-46,-470Q-20,-420 30,-330L46,-330Q10,-420 -30,-478Z" fill="#c8402a" ${ln(2)}/><path d="M-40,-460l14,24M-28,-440l14,24M-16,-418l14,24M-4,-396l14,24" stroke="#2a6ac8" stroke-width="4"/>`;
  C.yaiBua = { v2: { ...yv, faceTop: jasmine, top: { kind: "blouse", c: "#c8a8e0", sleeve: "elbow", lace: true, trim: "#a888c8" }, print: pakama,
    bottom: { kind: "sarong", c: "#1e5a3a", band: "#d8a83a", band2: "#14402a" }, extra: "" } };

  // ---------------- ลุงสิงห์ ----------------
  const tj = base("taJun");
  const hat = `<g><ellipse cx="0" cy="-596" rx="104" ry="20" fill="#e2c27a" ${ln()}/><path d="M-50,-598C-48,-650 48,-652 50,-598Z" fill="#d8b46a" ${ln()}/>
    <path d="M-50,-604h100" stroke="#7a4a26" stroke-width="7"/><path d="M-90,-596q90,16 180,0" stroke="#b89a5a" stroke-width="2" fill="none"/></g>`;
  const towel = `<path d="M-40,-470Q0,-440 40,-470L44,-440Q0,-414 -44,-440Z" fill="#f4f0e4" ${ln(2)}/><path d="M30,-454l6,70l18,-4l-8,-70" fill="#f4f0e4" ${ln(2)}/>`;
  C.lungSing = { v2: { ...tj, faceTop: hat, top: { kind: "shirt", c: "#6a8aa8", sleeve: "long", neck: "collar", collar: "#5a7a98", button: "#e8e4d8" }, print: towel,
    bottom: { kind: "trousers", c: "#3a3a40" }, legs: undefined, extra: "", skirt: undefined, feet: { kind: "boot", c: "#2a2a2e" } } };


  // ---------------- v2 cast (31 ต.ค. ค่ำ: lane A keeps sister+brother+grandma+uncle, so this story changes its set) ----------------
  //   tan      พี่แทน 16: spiky hair, white earbuds, a cobalt tee with two white stripes, black shorts, white sneakers · tanPhone (phone in hand)
  //   bai      ใบข้าว 9 (draw ~0.72): two short pigtails with yellow bobbles, a sunflower-yellow tee with a tamarind print, green shorts, sandals
  //            · baiSling (the slingshot in the front fist)
  //   taPerm   ตาเพิ่ม 70: grey stubble hair, a white singlet with a checked ผ้าขาวม้า over the shoulder, navy fisherman trousers, sandals
  //   paNuan   ป้านวล 52 (the neighbour the kids call crazy): a wide straw hat, a long-sleeved faded blue work shirt to the wrist, a towel
  //            round the neck, dark trousers, rubber boots, old scars on the backs of her hands
  const tg = base("tang");
  const num = `<path d="M-58,-430H58M-58,-414H58" stroke="#ffffff" stroke-width="7" opacity=".9"/>`;
  C.tan = { v2: { ...tg, headScale: 1.06, w: 1, limb: 1, face: "", faceTop: buds, top: { kind: "tee", c: "#2f62c8", sleeve: "short" }, print: num,
    bottom: { kind: "shorts", c: "#22252c" }, feet: { kind: "sneaker", c: "#f6f4ee", mark: "#2f62c8" } } };
  C.tanPhone = { ...C.tan, hand: phone(), keep: "F" };
  const pig = (h) => `<g><path d="M-52,-560C-78,-560 -92,-536 -86,-510Q-70,-524 -50,-540Z" fill="${h.c}" ${ln()}/><path d="M54,-560C80,-560 94,-536 88,-510Q72,-524 52,-540Z" fill="${h.c}" ${ln()}/>
    <circle cx="-56" cy="-556" r="9" fill="#ffd23a" ${ln(1.8)}/><circle cx="58" cy="-556" r="9" fill="#ffd23a" ${ln(1.8)}/></g>`;
  const tama = `<g transform="translate(0,-404) rotate(-20)"><path d="M-30,0C-20,-14 20,-14 30,0C20,10 -20,10 -30,0Z" fill="#8a5a30" ${ln(2)}/><path d="M-10,-6v12M6,-7v13" stroke="#5a3418" stroke-width="2"/></g>`;
  C.bai = { v2: { ...mintV, headScale: 1.2, w: 0.92, limb: 0.9, hair: { ...(mintV.hair || {}), c: "#1a1412", back: pig }, faceTop: "", top: { kind: "tee", c: "#ffc83a", sleeve: "short" }, print: tama,
    bottom: { kind: "shorts", c: "#4a9a5a" }, feet: { kind: "sandal", c: "#ec5e9e" } } };
  C.baiSling = { ...C.bai, hand: sling(), keep: "F" };
  const th = base("thong");
  C.taPerm = { v2: { ...th, hair: { c: "#d8d4cc", s: "#a8a49c", sh: "#f4f2ee", front: (x) => `<path d="M-46,-552C-50,-604 -18,-622 4,-622C30,-621 53,-604 49,-552Q46,-570 41,-578L-41,-578Q-45,-566 -46,-552Z" fill="${x.hair.c}" ${ln()}/>
      <g fill="${x.hair.s}" opacity=".5">${[[-30, -600], [-14, -608], [2, -610], [18, -606], [32, -598]].map(([x0, y0]) => `<circle cx="${x0}" cy="${y0}" r="2.4"/>`).join("")}</g>` },
    top: { kind: "singlet", c: "#f2ede2", sleeve: "none" }, print: pakama, bottom: { kind: "trousers", c: "#24365a" }, feet: { kind: "sandal", c: "#3a2a1e" } } };
  const ch = base("chan");
  C.paNuan = { v2: { ...ch, extra: "", faceTop: hat, top: { kind: "shirt", c: "#6a8aa8", sleeve: "long", neck: "collar", collar: "#5a7a98", button: "#e8e4d8" }, print: towel,
    bottom: { kind: "trousers", c: "#3a3a40" }, skirt: undefined, feet: { kind: "boot", c: "#2a2a2e" } } };

  // ---------------- poses ----------------
  // flailing both forearms in front of the face: the wrong instinct
  M.swat = (u, o) => { const a = Math.sin(u * 2 * Math.PI / 0.32), b = Math.sin(u * 2 * Math.PI / 0.27 + 1); return { ...M.idle(u, o), uaF: -100 + 30 * a, faF: -60 + 40 * b, uaB: 96 - 30 * b, faB: 56 - 40 * a, torso: -4 + 3 * a, head: -6 + 4 * b, bodyY: -2 }; };
  // both arms wrapped over the head, hunched (protect the face and head)
  M.cover = (u, o) => { const j = Math.sin(u * 31) * 1.2; return { ...M.idle(u, o), uaF: -150 + j, faF: -120, uaB: 150 - j, faB: 120, torso: 14, head: 14, bodyY: 14 }; };
  // running with the front arm over the head
  M.runCover = (u, o) => { const r = M.run(u, o); return { ...r, uaF: -150, faF: -110, torso: (r.torso || 0) + 6, head: 10 }; };
  // the slingshot drawn back: the front fist out, the back hand pulling to the cheek
  M.aim = (u, o) => ({ ...M.idle(u, o), uaF: -88, faF: -6, uaB: 80, faB: 120, torso: -2, head: -4 });
  // rubbing the forearm (a sting)
  M.scratch = (u, o) => { const a = Math.sin(u * 2 * Math.PI / 0.4); return { ...M.idle(u, o), uaF: -20, faF: -96, uaB: -30 + 6 * a, faB: -70, torso: 6, head: 10 }; };
  // waving someone in (through a door)
  M.beckon = (u, o) => { const a = Math.sin(u * 2 * Math.PI / 0.45); return { ...M.idle(u, o), uaF: -110, faF: -60 + 40 * a, uaB: 6, faB: -14, torso: -3, head: -4 }; };
})();
