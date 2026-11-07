// คนเดินดิน (story 4) · the cast in the channel look (sig.js faces on flat.js bodies). Load after ltcast.js.
//   flYou      คุณ the boy who cannot fly: side-parted hair, round glasses, grey school shirt + navy shorts, sneakers, a small backpack (acc) · flYouBag (no backpack) · flYouScope (telescope eyepiece hand)
//   flGran     ยายแย้ม: grey bun, welding goggles on the forehead, a flowered blouse under a leather apron · flGranWeld (torch in hand) · flGranMask (goggles down)
//   flFa       ฟ้า: long blue-black hair, sky-blue hoodie, shorts, sneakers · flFaTea (a bubble tea in hand)
//   flMom      the laser-eyed neighbour (perm, apron) · <g class="flLaser"> red beams from the eyes at opacity 0 · flUncle: the elephant-strong uncle (horseshoe, singlet, huge) · flUncleJar (a jar in hand)
//   flDad flMum flTot: the family on the nest (the toddler s 0.55) · flTeacher: bun, rectangle glasses, purple blazer, <g class="flLaser"> · flKid1..3: classmates
//   flCaptain  กัปตันสุริยา: gold helmet (HAIR.helm), gold armour, a red cape (<g class="flCape">), a sun emblem; he never stands on the ground (place him 14 px up, see FL.hover)
//   modes: fly (horizontal, arms forward, head to the facing side) · hover (upright, legs dangling) · hang (upside down) · pulley (hanging in a harness)
//   FL: DOG(id) a small dog (tail .flTail, mouth .flBark) · TEA JAR TOAST SPRAY NOTEBOOK · trail(x,y,len,c) a speed trail
(function () {
  const { mix, dk, hi } = Rig2;
  const C = Rig.CAST, S = Flat.SPEC, faces = Sig.sigFaces;
  const f = (v) => (+v).toFixed(1);
  Flat.HAIR.messy = Flat.HAIR.messy || Flat.HAIR.short;
  // ---------------- คุณ ----------------
  const backpack = () => `<g class="flPack"><rect x="-56" y="-470" width="30" height="120" rx="12" fill="#3a6a8a"/><rect x="-56" y="-470" width="30" height="120" rx="12" fill="url(#flV)"/><path d="M-30,-470Q-10,-462 -8,-440M-30,-360Q-10,-368 -8,-392" stroke="#2a4a60" stroke-width="5" fill="none"/></g>
    <rect x="18" y="-440" width="14" height="30" rx="2" fill="#f4ecd8"/><rect x="20" y="-452" width="6" height="14" rx="2" fill="#d8352a"/>`;
  S.flYou = { hair: "side", glasses: "round", faces: faces({ browW: 4.6 }), acc: backpack, headScale: 1.04 };
  C.flYou = { v2: { skin: "#d2a07a", hair: { c: "#1c1612" }, top: { kind: "tee", c: "#d8dce4", sleeve: "short", neck: "collar" }, bottom: { kind: "shorts", c: "#2a3a6a" }, feet: { kind: "sneaker", c: "#f4f4f0" }, w: 0.94, limb: 0.98 } };
  S.flYouBag = { ...S.flYou, acc: () => `<rect x="18" y="-440" width="14" height="30" rx="2" fill="#f4ecd8"/><rect x="20" y="-452" width="6" height="14" rx="2" fill="#d8352a"/>` }; C.flYouBag = { v2: C.flYou.v2 };
  const NOTEBOOK = `<g transform="translate(0,112) rotate(-14)"><rect x="-26" y="-36" width="52" height="68" rx="4" fill="#3a6a4a"/><rect x="-26" y="-36" width="10" height="68" fill="#2a4a34"/><path d="M-8,-20h24M-8,-6h24M-8,8h20" stroke="#cfe0c8" stroke-width="3"/></g>`;
  C.flYouBook = { v2: C.flYou.v2, hand: NOTEBOOK, keep: "F" }; S.flYouBook = S.flYou;
  // ---------------- ยายแย้ม ----------------
  const goggles = () => `<g class="flGog" transform="translate(0,-586)"><rect x="-40" y="-14" width="80" height="26" rx="12" fill="#3a3e44"/><circle cx="-18" cy="-1" r="12" fill="#5a8a6a"/><circle cx="18" cy="-1" r="12" fill="#5a8a6a"/><circle cx="-20" cy="-4" r="4" fill="#cfe8d8" opacity=".7"/><circle cx="16" cy="-4" r="4" fill="#cfe8d8" opacity=".7"/></g>`;
  const gogglesDown = () => `<g class="flGog" transform="translate(2,-556)"><rect x="-44" y="-14" width="88" height="28" rx="13" fill="#3a3e44"/><circle cx="-18" cy="0" r="13" fill="#2a4a3a"/><circle cx="18" cy="0" r="13" fill="#2a4a3a"/></g>`;
  const apronG = () => `<path d="M-36,-470H36L42,-312H-42Z" fill="#7a5638"/><path d="M-36,-470H36L42,-312H-42Z" fill="url(#flV)"/><path d="M-24,-470V-492M24,-470V-492" stroke="#5a3a24" stroke-width="5"/><rect x="-24" y="-400" width="48" height="30" rx="4" fill="#6a4a30"/>
    ${[[-30, -450], [30, -452], [-20, -340], [26, -336]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="#e88aa8" opacity=".9"/>`).join("")}`;
  S.flGran = { hair: "bun", faces: faces({ crinkle: true, k: 0.82, browW: 3.2 }), acc: apronG, headTop: goggles };
  C.flGran = { v2: { skin: "#d8b08a", hair: { c: "#c8c8c8" }, top: { kind: "tee", c: "#c86a8a", sleeve: "elbow" }, bottom: { kind: "sarong", c: "#4a3a5a", band: "#2a2a3a" }, feet: { kind: "sandal", c: "#6a4a30" }, w: 1.12, limb: 0.92 } };
  C.flGranWeld = { v2: C.flGran.v2, hand: LT.TORCH_W, keep: "F" }; S.flGranWeld = { ...S.flGran, headTop: gogglesDown };
  // ---------------- ฟ้า ----------------
  const hoodie = () => `<path d="M-46,-492Q0,-470 46,-492L48,-470Q0,-446 -48,-470Z" fill="#3a90d0"/><path d="M-8,-470v40M8,-470v40" stroke="#f4f4f0" stroke-width="4" stroke-linecap="round"/>`;
  S.flFa = { hair: "long", hairB: "longB", faces: faces({ k: 0.95, browW: 3.6 }), acc: hoodie };
  C.flFa = { v2: { skin: "#e0b898", hair: { c: "#1e2848" }, top: { kind: "tee", c: "#4aa8e8", sleeve: "long" }, bottom: { kind: "shorts", c: "#f4f0e8" }, feet: { kind: "sneaker", c: "#ffffff" } } };
  const TEA = `<g transform="translate(0,112) rotate(-10)"><path d="M-16,-30H16L13,24H-13Z" fill="#e8d8c0" opacity=".9"/><path d="M-13,0H13L12,24H-12Z" fill="#8a6a4a"/>${[-8, -2, 5].map((x) => `<circle cx="${x}" cy="16" r="3.5" fill="#2a1a10"/>`).join("")}<rect x="-18" y="-34" width="36" height="6" rx="3" fill="#f4f4f0"/><path d="M4,-34V-70" stroke="#f4a0b8" stroke-width="6" stroke-linecap="round"/></g>`;
  C.flFaTea = { v2: C.flFa.v2, hand: TEA, keep: "F" }; S.flFaTea = S.flFa;
  // ---------------- neighbours ----------------
  const laser = (dir = 1) => `<g class="flLaser" opacity="0"><path d="M${-14 * dir},-548L${-14 * dir + 420 * dir},-440M${14 * dir},-548L${14 * dir + 420 * dir},-440" stroke="#ff3a2a" stroke-width="7" stroke-linecap="round" opacity=".9"/><path d="M${-14 * dir},-548L${-14 * dir + 420 * dir},-440M${14 * dir},-548L${14 * dir + 420 * dir},-440" stroke="#ffd0c0" stroke-width="2.5" stroke-linecap="round"/><circle cx="-14" cy="-548" r="7" fill="#ff6a5a"/><circle cx="14" cy="-548" r="7" fill="#ff6a5a"/></g>`;
  S.flMom = { hair: "perm", faces: faces({ k: 0.9, browW: 3.6 }), acc: () => `<path d="M-30,-470H30L34,-320H-34Z" fill="#f4e4c8"/><path d="M-30,-470H30L34,-320H-34Z" fill="url(#flV)"/>`, headTop: () => laser(1) };
  C.flMom = { v2: { skin: "#d8a47c", hair: { c: "#3a2a24" }, top: { kind: "tee", c: "#a85a8a", sleeve: "elbow" }, bottom: { kind: "trousers", c: "#3a3a4a" }, feet: { kind: "sandal", c: "#c8a080" }, w: 1.1 } };
  S.flUncle = { hair: "horseshoe", faces: faces({ crinkle: true, k: 0.86, browW: 5 }), tache: "#3a2a24" };
  C.flUncle = { v2: { skin: "#c89060", hair: { c: "#3a2a24" }, top: { kind: "singlet", c: "#f4f0e8" }, bottom: { kind: "shorts", c: "#5a4a3a" }, feet: { kind: "sandal", c: "#4a3a30" }, w: 1.42, limb: 1.08 } };
  const JAR = `<g class="flJar" transform="translate(0,112) rotate(-12)"><path d="M-22,-30H22V26Q22,34 14,34H-14Q-22,34 -22,26Z" fill="#cfe4ee" opacity=".85"/><rect x="-24" y="-40" width="48" height="14" rx="4" fill="#c8302a"/><path d="M-14,-20V20" stroke="#fff" stroke-width="4" opacity=".6"/>${[-8, 4].map((x) => `<circle cx="${x}" cy="${12 - x}" r="6" fill="#d8a040"/>`).join("")}</g>`;
  C.flUncleJar = { v2: C.flUncle.v2, hand: JAR, keep: "F" }; S.flUncleJar = S.flUncle;
  // ---------------- the family on the nest · the teacher · classmates ----------------
  S.flDad = { hair: "short", faces: faces({ browW: 4.4 }) }; C.flDad = { v2: { skin: "#d0a078", hair: { c: "#2a2220" }, top: { kind: "tee", c: "#6a8aa8", sleeve: "short" }, bottom: { kind: "trousers", c: "#3a3e4a" }, feet: { kind: "sneaker", c: "#e8e8e0" } } };
  S.flMum = { hair: "bob", faces: faces({ k: 0.95, browW: 3.6 }) }; C.flMum = { v2: { skin: "#e0b898", hair: { c: "#4a3028" }, top: { kind: "tee", c: "#e8c860", sleeve: "elbow" }, bottom: { kind: "sarong", c: "#8a4a5a", band: "#5a2a3a" }, feet: { kind: "sandal", c: "#c8a080" } } };
  S.flTot = { hair: "juk", faces: faces({ k: 1.35, browW: 3.6 }), headScale: 1.3 }; C.flTot = { v2: { skin: "#e0b898", hair: { c: "#1c1612" }, top: { kind: "tee", c: "#ff9a6a", sleeve: "short" }, bottom: { kind: "shorts", c: "#f4f0e8" }, feet: { kind: "bare" }, w: 1.1, limb: 0.8 } };
  S.flTeacher = { hair: "bun", glasses: "rect", faces: faces({ k: 0.9, browW: 4.2 }), headTop: () => laser(1) };
  C.flTeacher = { v2: { skin: "#d8b090", hair: { c: "#2a2220" }, top: { kind: "coat", c: "#6a4a8a", sleeve: "long" }, bottom: { kind: "trousers", c: "#2a2a3a" }, feet: { kind: "boot", c: "#2a2220" }, w: 1.04 } };
  [["flKid1", "bowl", "#2a2220", "#d8dce4", "#2a3a6a", "#d4a07a", 0.96], ["flKid2", "pony", "#3a2a24", "#d8dce4", "#2a3a6a", "#e0b898", 0.92], ["flKid3", "buzz", "#1c1612", "#d8dce4", "#2a3a6a", "#c89060", 1.0], ["flKid4", "bob", "#4a3028", "#d8dce4", "#2a3a6a", "#e8c8a8", 0.94]].forEach(([n, hair, hc, tc, bc, sk, w]) => {
    S[n] = { hair, hairB: hair === "pony" ? "ponyB" : undefined, faces: faces({ k: 1.0, browW: 4 }), headScale: 1.02 };
    C[n] = { v2: { skin: sk, hair: { c: hc }, top: { kind: "tee", c: tc, sleeve: "short", neck: "collar" }, bottom: { kind: hair === "pony" || hair === "bob" ? "sarong" : "shorts", c: bc, band: bc }, feet: { kind: "sneaker", c: "#f4f4f0" }, w, limb: 0.96 } };
  });
  // ---------------- กัปตันสุริยา ----------------
  const cape = () => `<g class="flCape"><path d="M-40,-488Q-70,-380 -56,-300Q-10,-330 40,-300Q60,-380 40,-488Z" fill="#c8302a"/><path d="M-40,-488Q-70,-380 -56,-300Q-10,-330 40,-300Q60,-380 40,-488Z" fill="url(#flV)" opacity=".6"/></g>`;
  const armour = () => `<path d="M-42,-490H42L38,-320H-38Z" fill="#e8b830"/><path d="M-42,-490H42L38,-320H-38Z" fill="url(#flV)"/><path d="M-46,-492Q-60,-470 -52,-440M46,-492Q60,-470 52,-440" stroke="#f6d36a" stroke-width="12" stroke-linecap="round"/>
    <circle cy="-420" r="22" fill="#f6d36a"/><circle cy="-420" r="22" fill="none" stroke="#a87820" stroke-width="3"/>${[0, 45, 90, 135, 180, 225, 270, 315].map((a) => `<path d="M0,-450v-10" stroke="#f6d36a" stroke-width="5" stroke-linecap="round" transform="rotate(${a} 0 -420)"/>`).join("")}<rect x="-40" y="-330" width="80" height="14" fill="#a87820"/>`;
  S.flCaptain = { hair: "helm", faces: faces({ browW: 5.2, k: 0.9 }), acc: armour, headTop: () => `<path d="M-44,-600Q0,-640 44,-600" stroke="#f6d36a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M0,-640V-676" stroke="#f6d36a" stroke-width="8" stroke-linecap="round"/>`, hairB: undefined };
  C.flCaptain = { v2: { skin: "#d8a878", hair: { c: "#e8b830" }, top: { kind: "coat", c: "#e8b830", sleeve: "long" }, bottom: { kind: "trousers", c: "#c89020" }, feet: { kind: "boot", c: "#a87820" }, w: 1.1, limb: 1.04 } };
  // cape is drawn behind the torso: hairB slot is behind the body in flat.js, so give him a "hair back" that is the cape
  Flat.HAIR.capeB = () => cape();
  S.flCaptain.hairB = "capeB";

  // ---------------- flight poses ----------------
  const M = Rig.MODES;
  M.fly = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.6); return { ...M.idle(u, o), uaF: -162 + 2 * b, faF: -8, uaB: -150 - 2 * b, faB: -10, thF: 6 + 2 * b, thB: -6 - 2 * b, shF: 6, shB: 4, torso: -4, head: 10, bodyY: 0, rootR: (o.ang ?? 74) + 2 * b, rootY: 4 * b }; };
  M.hover = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.2); return { ...M.idle(u, o), uaF: -40 + 3 * b, faF: -60, uaB: -30 - 3 * b, faB: -50, thF: 18 + 4 * b, shF: 30, thB: -14 - 4 * b, shB: 26, torso: -3, head: 2, bodyY: 0, rootY: 8 * b }; };
  M.hang = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.4); return { ...M.idle(u, o), uaF: -20 + 3 * b, faF: -40, uaB: -14 - 3 * b, faB: -30, thF: 10, shF: 10, thB: -8, shB: 8, torso: 0, head: -6 + 2 * b, bodyY: 0, rootR: 180 + 3 * b, rootY: 6 * b }; };
  M.pulley = (u, o) => { const j = Math.sin(u * 23) * 1.2; return { ...M.idle(u, o), uaF: -150 + j, faF: -20, uaB: -140 - j, faB: -18, thF: 30, shF: 60, thB: 26, shB: 56, torso: 4, head: -10, bodyY: 0 }; };
  M.dangle = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.4); return { ...M.idle(u, o), uaF: -160, faF: -6, uaB: -4, faB: -20, thF: 8 + 6 * b, shF: 16, thB: -8 - 6 * b, shB: 12, torso: 2 * b, head: -6, rootR: 6 * b }; };
  M.clap = (u, o) => { const b = Math.abs(Math.sin(u * 11)); return { ...M.idle(u, o), uaF: -70 - 20 * b, faF: -60 + 30 * b, uaB: -60 + 20 * b, faB: -70 - 30 * b, head: -4, torso: -2 }; };
  M.spray = (u, o) => ({ ...M.crouch(u, o), uaF: -20, faF: -30, head: 20 });
  M.scope = (u, o) => ({ ...M.idle(u, o), uaF: -92, faF: -70, uaB: -80, faB: -60, torso: 8, head: 12 + 1.5 * Math.sin(u * 1.1) });
  M.bark = (u, o) => M.idle(u, o);
  M.floatPoint = (u, o) => ({ ...M.point(u, o), bodyY: -16 + 6 * Math.sin(u * 2 * Math.PI / 1.3) });
  M.floatIdle = (u, o) => ({ ...M.idle(u, o), bodyY: -16 + 6 * Math.sin(u * 2 * Math.PI / 1.3) });

  // ---------------- props and bits ----------------
  const DOG = (id, c = "#c8a060") => `<g id="${id}" class="flDog"><ellipse cx="0" cy="-54" rx="54" ry="30" fill="${c}"/><ellipse cx="0" cy="-54" rx="54" ry="30" fill="url(#flV)" opacity=".5"/>
      <path class="flTail" d="M-50,-66Q-86,-96 -72,-120" stroke="${c}" stroke-width="12" fill="none" stroke-linecap="round"/>
      ${[-34, -14, 14, 34].map((x) => `<rect x="${x - 7}" y="-36" width="14" height="38" rx="6" fill="${dk(c, 0.1)}"/>`).join("")}
      <g class="flHead" transform="translate(52,-82)"><circle r="30" fill="${c}"/><path d="M-26,-14Q-34,-50 -10,-40Z" fill="${dk(c, 0.25)}"/><path d="M14,-18Q24,-52 36,-28Z" fill="${dk(c, 0.25)}"/><circle cx="10" cy="-6" r="3.5" fill="#1a1a1e"/><circle cx="24" cy="4" r="6" fill="#1a1a1e"/>
        <g class="flBark" opacity="0"><path d="M10,12Q24,24 34,12" stroke="#1a1a1e" stroke-width="3" fill="none"/><ellipse cx="22" cy="18" rx="8" ry="5" fill="#d84a4a"/></g></g></g>`;
  const TOAST = (x, y) => `<g transform="translate(${x},${y})"><rect x="-40" y="-30" width="80" height="60" rx="8" fill="#c8ccd4"/><rect x="-40" y="-30" width="80" height="60" rx="8" fill="url(#flV)"/><rect x="-30" y="-36" width="26" height="12" rx="3" fill="#1a1a1e"/><rect x="4" y="-36" width="26" height="12" rx="3" fill="#1a1a1e"/><g class="flToast"><path d="M-26,-36q10,-30 20,0M4,-36q10,-30 20,0" fill="#e8b860"/></g><g class="flSmoke" opacity="0"><path d="M-10,-50q-8,-20 0,-40M10,-50q8,-20 0,-40" stroke="#8a8a90" stroke-width="5" fill="none" stroke-linecap="round"/></g></g>`;
  const SPRAY = `<g transform="translate(0,112) rotate(-100)"><rect x="-10" y="-20" width="20" height="50" rx="5" fill="#d8352a"/><rect x="-10" y="-20" width="20" height="50" rx="5" fill="url(#flV)"/><rect x="-5" y="-30" width="10" height="12" rx="2" fill="#2a2a30"/><circle cx="0" cy="-30" r="3" fill="#1a1a1e"/></g>`;
  C.flYouSpray = { v2: C.flYou.v2, hand: SPRAY, keep: "F" }; S.flYouSpray = S.flYou;
  const trail = (len = 160, c = "#ffffff") => `<g class="flTrail" opacity=".55"><path d="M0,0H${-len}" stroke="${c}" stroke-width="10" stroke-linecap="round" opacity=".5"/><path d="M0,-14H${-len * 0.7}M0,14H${-len * 0.6}" stroke="${c}" stroke-width="6" stroke-linecap="round" opacity=".35"/></g>`;
  window.FL = { DOG, TOAST, SPRAY, TEA, JAR, NOTEBOOK, trail };
})();
