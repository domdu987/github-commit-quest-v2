// ช่างเชื่อมสายฟ้า (story 3) · the cast in the channel look (sig.js faces on flat.js bodies). Load after jkcast.js.
//   ltYou      คุณ the welder: dark-blue tee, leather apron, jeans, boots · hair "short" before the strike, "bolt" (standing straight up, <g class="ltSpark"> sparks) after
//              ltYouWeld (torch in hand, mask up on the forehead) · ltYouWeldOn (mask down over the face) · ltYouBolt · ltYouBoltWeld · ltYouGown (hospital gown, hair bolt)
//   ltHong     เจ๊หงส์ the shop owner: perm, magenta blouse, gold chain · ltHongCalc (calculator) · ltHongCash (banknotes)
//   ltKim      เฮียกิม the old electrician: grey bolt hair, round glasses, singlet · ltKimDriver (screwdriver)
//   ltNurse    the nurse: white dress and cap · ltNurseBolt (her hair stands up too)
//   ltMan1..2 ltWom1..2 (+Phone): the alley
//   LT: PHONE TORCH_W CASH CALC BIKE GATE CYL INC BABY TREE FUSEBOX bolt(x0,y0,x1,y1,seed) sparks(n,r,seed) glowRing
(function () {
  const { mix, dk, hi } = Rig2;
  const C = Rig.CAST, S = Flat.SPEC, faces = Sig.sigFaces;
  const f = (v) => (+v).toFixed(1);
  // hair standing straight up after the strike (with sparks to switch on)
  Flat.HAIR.bolt = (c) => `<path d="M-42,-532C-46,-560 -40,-580 -34,-590L-46,-648L-22,-606L-12,-664L2,-612L14,-670L24,-610L48,-652L40,-592Q46,-566 44,-556Q34,-572 22,-574Q4,-570 -10,-576Q-22,-566 -30,-556Q-34,-546 -36,-532Z" fill="${c}"/>
    <path d="M-16,-608L-10,-646M8,-612L12,-654M30,-606L40,-640" stroke="${hi(c, 0.35)}" stroke-width="4" stroke-linecap="round" opacity=".6"/>
    <g class="ltSpark" opacity="0"><path d="M-62,-636l10,-6l-6,-10l10,-6M56,-622l-10,-8l8,-6l-8,-10M-2,-694l6,-8l-4,-10l8,-6M-40,-676l6,-6l-4,-8" stroke="#ffe24a" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;

  // ---------------- คุณ the welder ----------------
  const apron = () => `<path d="M-34,-472H34L40,-308H-40Z" fill="#6a4a30"/><path d="M-34,-472H34L40,-308H-40Z" fill="url(#flV)"/><path d="M-24,-472V-494M24,-472V-494" stroke="#4a3020" stroke-width="5"/><rect x="-26" y="-400" width="52" height="34" rx="4" fill="#5a3c26"/><path d="M-26,-383H26" stroke="#4a3020" stroke-width="2"/>`;
  S.ltYou = { hair: "short", faces: faces({ browW: 4.6 }), acc: apron };
  C.ltYou = { v2: { skin: "#c88a60", hair: { c: "#1c1612" }, top: { kind: "tee", c: "#2f4a66", sleeve: "short" }, bottom: { kind: "jeans", c: "#2a3450" }, feet: { kind: "boot", c: "#3a2a20" }, w: 1.02 } };
  const maskUp = () => `<g class="ltMaskUp" transform="translate(4,-602) rotate(-24)"><path d="M-40,0Q-44,-70 0,-78Q44,-70 40,0Z" fill="#2a2e34"/><path d="M-40,0Q-44,-70 0,-78Q44,-70 40,0Z" fill="url(#flV)"/><rect x="-26" y="-52" width="52" height="16" rx="4" fill="#3a8a4a" opacity=".9"/></g>`;
  const maskDown = () => `<g class="ltMaskDown"><path d="M-48,-596Q-52,-476 0,-456Q52,-476 48,-596Q0,-618 -48,-596Z" fill="#2a2e34"/><path d="M-48,-596Q-52,-476 0,-456Q52,-476 48,-596Q0,-618 -48,-596Z" fill="url(#flV)"/><rect x="-30" y="-566" width="60" height="24" rx="4" fill="#3a9a4a" opacity=".95"/><path d="M-30,-554H30" stroke="#8ad88a" stroke-width="3" opacity=".6"/></g>`;
  const TORCH_W = `<g transform="translate(0,112) rotate(-100)"><rect x="-7" y="-10" width="14" height="80" rx="5" fill="#3a3a44"/><rect x="-5" y="-50" width="10" height="44" rx="3" fill="#8a8f98"/><path d="M-4,-50L0,-72L4,-50Z" fill="#c8ccd4"/><path d="M4,62q34,30 24,96" stroke="#1a1a1e" stroke-width="5" fill="none"/><g class="ltArc" opacity="0"><circle cy="-74" r="14" fill="#fff8d0"/><circle cy="-74" r="28" fill="#9ad8ff" opacity=".45"/></g></g>`;
  S.ltYouWeld = { ...S.ltYou, headTop: maskUp }; C.ltYouWeld = { v2: C.ltYou.v2, hand: TORCH_W, keep: "F" };
  S.ltYouWeldOn = { ...S.ltYou, headTop: maskDown }; C.ltYouWeldOn = { v2: C.ltYou.v2, hand: TORCH_W, keep: "F" };
  S.ltYouBolt = { ...S.ltYou, hair: "bolt" }; C.ltYouBolt = { v2: C.ltYou.v2 };
  S.ltYouBoltWeld = { ...S.ltYou, hair: "bolt" }; C.ltYouBoltWeld = { v2: C.ltYou.v2, hand: TORCH_W, keep: "F" };
  S.ltYouGown = { hair: "bolt", faces: faces({ browW: 4.6 }) };
  C.ltYouGown = { v2: { ...C.ltYou.v2, top: { kind: "tee", c: "#9ad0e0", sleeve: "short" }, bottom: { kind: "trousers", c: "#9ad0e0" }, feet: { kind: "bare" } } };

  // ---------------- เจ๊หงส์ ----------------
  const bling = () => `<path d="M-30,-490Q0,-458 30,-490" stroke="#f2c55c" stroke-width="5" fill="none"/><circle cy="-464" r="7" fill="#f2c55c"/>${[[-28, -436], [-6, -416], [18, -440], [30, -400], [-20, -380], [8, -360]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="9" fill="#ff9ac0" opacity=".8"/><circle cx="${x}" cy="${y}" r="4" fill="#ffd0a0" opacity=".9"/>`).join("")}`;
  S.ltHong = { hair: "perm", faces: faces({ crinkle: true, k: 0.9, browW: 3.4 }), acc: bling };
  C.ltHong = { v2: { skin: "#e0b08a", hair: { c: "#3a2a2a" }, top: { kind: "tee", c: "#c8386a", sleeve: "elbow" }, bottom: { kind: "trousers", c: "#3a3a4a" }, feet: { kind: "sandal", c: "#c8a040" }, w: 1.18 } };
  const CALC = `<g transform="translate(0,112) rotate(-20)"><rect x="-20" y="-32" width="40" height="64" rx="5" fill="#dcdcdc"/><rect x="-14" y="-26" width="28" height="14" fill="#9ab8a0"/>${[-12, 0, 12].map((x) => [-4, 8, 20].map((y) => `<rect x="${x - 4}" y="${y - 4}" width="8" height="7" rx="2" fill="#4a4a4a"/>`).join("")).join("")}</g>`;
  const CASH = `<g transform="translate(0,112) rotate(-30)"><rect x="-30" y="-14" width="60" height="28" rx="3" fill="#9ac8a0"/><rect x="-30" y="-10" width="60" height="28" rx="3" fill="#8ab890" transform="rotate(-8)"/><circle r="9" fill="#e8e8e8" stroke="#6a8a70" stroke-width="2"/></g>`;
  C.ltHongCalc = { v2: C.ltHong.v2, hand: CALC, keep: "F" }; S.ltHongCalc = S.ltHong;
  C.ltHongCash = { v2: C.ltHong.v2, hand: CASH, keep: "F" }; S.ltHongCash = S.ltHong;

  // ---------------- เฮียกิม ----------------
  S.ltKim = { hair: "bolt", faces: faces({ crinkle: true, k: 0.86, browW: 3.2 }), glasses: "round", tache: "#b8b4ac" };
  C.ltKim = { v2: { skin: "#d8b090", hair: { c: "#c8c4bc" }, top: { kind: "singlet", c: "#f0ece4" }, bottom: { kind: "shorts", c: "#7a6a4a" }, feet: { kind: "sandal", c: "#4a3a2a" }, w: 0.9 } };
  const DRIVER = `<g transform="translate(0,112) rotate(-40)"><rect x="-6" y="-70" width="12" height="40" rx="4" fill="#d8352a"/><rect x="-2.5" y="-30" width="5" height="60" fill="#9aa0a6"/></g>`;
  C.ltKimDriver = { v2: C.ltKim.v2, hand: DRIVER, keep: "F" }; S.ltKimDriver = S.ltKim;

  // ---------------- the nurse ----------------
  const cap = () => `<path d="M-30,-598Q0,-612 30,-598L26,-576H-26Z" fill="#ffffff"/><path d="M-8,-596h16M0,-604v16" stroke="#d8352a" stroke-width="3"/>`;
  S.ltNurse = { hair: "bun", faces: faces({ k: 1.0, browW: 3.4 }), headTop: cap };
  C.ltNurse = { v2: { skin: "#e8c0a0", hair: { c: "#2a2220" }, top: { kind: "tee", c: "#ffffff", sleeve: "short" }, bottom: { kind: "sarong", c: "#f4f4f8", band: "#e0e0e8" }, feet: { kind: "sneaker", c: "#ffffff" }, w: 0.98 } };
  S.ltNurseBolt = { ...S.ltNurse, hair: "bolt" }; C.ltNurseBolt = { v2: C.ltNurse.v2 };
  S.ltPatient = { hair: "horseshoe", faces: faces({ crinkle: true, k: 0.88 }) };
  C.ltPatient = { v2: { skin: "#d8a888", hair: { c: "#9a948c" }, top: { kind: "tee", c: "#9ad0e0", sleeve: "short" }, bottom: { kind: "trousers", c: "#9ad0e0" }, feet: { kind: "bare" }, w: 1.0 } };

  // ---------------- the alley ----------------
  [["ltMan1", "buzz", "#2a2420", "#e8e0c8", "#3a3a4a", "#c89060", 1.1, "short"], ["ltMan2", "side", "#3a2a24", "#4a7ac8", "#2a2a30", "#d4a07a", 1.0, "long"],
   ["ltWom1", "bob", "#2a2420", "#f0d060", "#5a4a6a", "#e8c0a0", 0.96, "short"], ["ltWom2", "pony", "#1c1612", "#e86a8a", "#3a3a4a", "#d8a888", 0.94, "short"]].forEach(([n, hair, hc, tc, bc, sk, w, sl]) => {
    S[n] = { hair, faces: faces({ k: 0.9 }) };
    C[n] = { v2: { skin: sk, hair: { c: hc }, top: { kind: "tee", c: tc, sleeve: sl }, bottom: { kind: "trousers", c: bc }, feet: { kind: "sandal", c: "#3a3a3a" }, w } };
  });
  const PHONE = `<g transform="translate(0,112) rotate(-14)"><rect x="-20" y="-54" width="40" height="76" rx="7" fill="#1a1a22"/><rect x="-16" y="-48" width="32" height="60" rx="4" fill="#243a66" class="ltScr"/><rect x="-7" y="-34" width="14" height="30" rx="3" fill="none" stroke="#f4ecd8" stroke-width="2"/><rect class="ltBat" x="-5" y="-10" width="10" height="4" fill="#ff5a4a"/></g>`;
  ["ltMan1", "ltMan2", "ltWom1", "ltWom2"].forEach((n) => { C[n + "Phone"] = { v2: C[n].v2, hand: PHONE, keep: "F" }; S[n + "Phone"] = S[n]; });

  // ---------------- poses for this story ----------------
  const M = Rig.MODES, Z = (u, o) => M.idle(u, o);
  M.weld = (u, o) => ({ ...M.crouch(u, o), uaF: -30 + 2 * Math.sin(u * 9), faF: -12, uaB: -40, faB: -60, head: 22, torso: 18 });   // the torch tip lands ~(+130, -90) from the feet            // crouched over the work, the torch down
  M.weldStand = (u, o) => ({ ...Z(u, o), uaF: -72 + 2 * Math.sin(u * 9), faF: -30, uaB: 10, faB: -12, head: 12, torso: 8 });
  M.zap = (u, o) => { const j = Math.sin(u * 47) * 3 + Math.sin(u * 31) * 2; return { ...Z(u, o), uaF: -120 + j, faF: -40, uaB: -120 - j, faB: -40, thF: -20, shF: 10, thB: 20, shB: -6, torso: -6 + j, head: -10 + j, bodyY: -8 }; };   // struck: arms flung up, legs apart, shaking
  M.sneeze = (u, o) => { const k = Math.sin(u * 2 * Math.PI / 0.7); return { ...Z(u, o), head: 6 + 20 * k, torso: 2 + 8 * k, uaF: -40, faF: -120, uaB: 20, faB: 10 }; };
  M.pointZap = (u, o) => { const j = Math.sin(u * 41) * 1.5; return { ...Z(u, o), uaF: -92 + j, faF: 4, uaB: 24, faB: 30, head: -2, torso: -4 }; };
  M.hugTree = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.4); return { ...Z(u, o), uaF: -90 + 2 * b, faF: -100, uaB: -90 - 2 * b, faB: -100, head: 6, torso: 4 }; };   // both arms forward around the trunk
  M.floatGlow = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.2); return { ...Z(u, o), uaF: -44 + 6 * b, faF: -30, uaB: -44 - 6 * b, faB: -30, thF: 12, shF: 20, thB: -8, shB: 26, head: -16, torso: -4, bodyY: -40 + 10 * b }; };
  M.grabCable = (u, o) => { const j = Math.sin(u * 37) * 2; return { ...Z(u, o), uaF: -124 + j, faF: -20, uaB: -112 - j, faB: -24, head: -14, torso: -8 }; };   // both hands up on the cable
  M.shout = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 0.5); return { ...Z(u, o), uaF: -150, faF: -24, uaB: 8, faB: -20, head: -12 + 3 * b, torso: -8 }; };
  M.sitWet = (u, o) => ({ ...M.sit(u, o), uaF: 20, faF: -10, uaB: 20, faB: -10, head: 12 + 3 * Math.sin(u * 2), torso: 6 });
  M.comb = (u, o) => ({ ...Z(u, o), uaF: -150 + 10 * Math.sin(u * 2 * Math.PI / 0.6), faF: -140, head: 4, torso: 2 });
  M.proud = (u, o) => ({ ...Z(u, o), uaF: -26, faF: 128, uaB: 30, faB: -128, head: -6, torso: -4 });
  M.knock = (u, o) => ({ ...Z(u, o), uaF: -96, faF: -40 + 24 * Math.max(0, Math.sin(u * 2 * Math.PI / 0.45)), head: 2, torso: 2 });
  M.payUp = (u, o) => ({ ...Z(u, o), uaF: -80, faF: -20, uaB: 10, faB: -10, head: 4, torso: 2 });   // one arm out to collect

  // ---------------- props ----------------
  const BIKE = `<g><ellipse cx="0" cy="8" rx="190" ry="14" fill="#000" opacity=".2"/><circle cx="-120" cy="-50" r="50" fill="#1a1a1e"/><circle cx="-120" cy="-50" r="30" fill="#5a5a60"/><circle cx="120" cy="-50" r="50" fill="#1a1a1e"/><circle cx="120" cy="-50" r="30" fill="#5a5a60"/>
    <path d="M-120,-50L-50,-120H60L120,-50" stroke="#4a4a50" stroke-width="10" fill="none"/><path d="M-70,-120Q-10,-170 70,-150L90,-128L-10,-110Z" fill="#c8302a"/><path d="M-90,-128Q-60,-150 -20,-146" stroke="#1a1a1e" stroke-width="8" fill="none"/>
    <path d="M60,-150L80,-200L110,-205" stroke="#4a4a50" stroke-width="8" fill="none"/><rect x="-100" y="-150" width="60" height="26" rx="8" fill="#2a2a30"/><path d="M-10,-110L10,-70" stroke="#4a4a50" stroke-width="8"/><ellipse cx="124" cy="-186" rx="14" ry="10" fill="#ffe8a0"/></g>`;
  const GATE = (w = 300, h = 400) => `<g class="ltGate"><rect x="${-w / 2}" y="${-h}" width="${w}" height="${h}" fill="none" stroke="#3a3a44" stroke-width="12"/>${[...Array(Math.floor(w / 44))].map((_, k) => `<path d="M${-w / 2 + 22 + k * 44},${-h}V0" stroke="#3a3a44" stroke-width="7"/>`).join("")}<path d="M${-w / 2},${-h * 0.5}H${w / 2}" stroke="#3a3a44" stroke-width="9"/>
    ${[...Array(Math.floor(w / 88))].map((_, k) => `<path d="M${-w / 2 + 44 + k * 88},${-h * 0.5 - 60}q30,30 0,60q-30,-30 0,-60" stroke="#3a3a44" stroke-width="5" fill="none"/>`).join("")}</g>`;
  const CYL = (c = "#4a8ab8") => `<g><rect x="-26" y="-180" width="52" height="180" rx="14" fill="${c}"/><rect x="-26" y="-180" width="52" height="180" rx="14" fill="url(#flV)"/><rect x="-10" y="-200" width="20" height="24" rx="4" fill="#8a8f98"/><rect x="-26" y="-120" width="52" height="14" fill="#2a2a30" opacity=".5"/></g>`;
  const BABY = `<g><ellipse cy="-14" rx="42" ry="22" fill="#ffd8c0"/><circle cx="-34" cy="-22" r="18" fill="#f8c8a8"/><path d="M-40,-24q6,4 12,0M-38,-28q2,-3 4,0M-30,-28q2,-3 4,0" stroke="#5a3a30" stroke-width="2" fill="none"/><path d="M-44,-36q10,-8 20,0" stroke="#2a2220" stroke-width="3" fill="none"/></g>`;
  const INC = (id = "") => `<g class="ltInc"><rect x="-90" y="-10" width="180" height="60" rx="8" fill="#d8dde4"/><rect x="-80" y="50" width="12" height="90" fill="#9aa0a8"/><rect x="68" y="50" width="12" height="90" fill="#9aa0a8"/><rect x="-92" y="140" width="184" height="10" rx="4" fill="#8a9098"/>
    <path d="M-86,-10V-110Q-86,-130 -66,-130H66Q86,-130 86,-110V-10Z" fill="#cfe8f8" opacity=".55"/><path d="M-86,-10V-110Q-86,-130 -66,-130H66Q86,-130 86,-110V-10" stroke="#eaf4fb" stroke-width="4" fill="none"/>
    <g transform="translate(0,-26)">${BABY}</g><rect class="ltIncLamp" x="-40" y="-128" width="80" height="8" rx="4" fill="#ffe8a0" opacity="0"/><circle class="ltIncLed" cx="70" cy="10" r="5" fill="#3a9c66" opacity="0"/></g>`;
  const TREE = `<g><path d="M-18,0Q-22,-200 -10,-400" stroke="#6a9a3a" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M-18,0Q-22,-200 -10,-400" stroke="#8ab84a" stroke-width="12" fill="none" stroke-linecap="round" opacity=".6"/>
    ${[-150, -100, -40, 20, 80, 140].map((a, k) => `<path d="M-10,-400q${Math.cos(a * Math.PI / 180) * 120},${Math.sin(a * Math.PI / 180) * 90 - 40} ${Math.cos(a * Math.PI / 180) * 260},${Math.sin(a * Math.PI / 180) * 160 + 60}" stroke="#4a9a3a" stroke-width="${44 - k * 2}" fill="none" stroke-linecap="round"/>`).join("")}
    <g class="ltBunch" transform="translate(40,-330)">${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path class="ltBan" d="M${-36 + k * 12},0q-8,40 ${-30 + k * 4},70" stroke="#6aa040" stroke-width="13" fill="none" stroke-linecap="round"/>`).join("")}<path d="M-40,-10L50,-4" stroke="#4a6a2a" stroke-width="8" stroke-linecap="round"/><ellipse cx="-4" cy="90" rx="12" ry="18" fill="#8a3a5a"/></g></g>`;
  const FUSEBOX = (id = "fb") => `<g id="${id}"><rect x="-120" y="-170" width="240" height="340" rx="8" fill="#6a6e76"/><rect x="-108" y="-158" width="216" height="316" rx="6" fill="#4a4e56"/>
    <g class="ltSecret" opacity="0"><rect x="-96" y="-146" width="192" height="292" rx="6" fill="#2a2a30"/><rect x="-70" y="-100" width="140" height="190" fill="#f4ecd8" transform="rotate(-3)"/><path d="M-50,-60h100M-50,-30h100M-50,0h70M-50,30h100M-50,60h40" stroke="#c8302a" stroke-width="5" stroke-linecap="round" transform="rotate(-3)" opacity=".8"/></g>
    <g class="ltInner"><rect x="-100" y="-150" width="200" height="300" rx="6" fill="#4a4e56"/>${[0, 1, 2, 3].map((k) => `<rect x="-80" y="${-130 + k * 60}" width="160" height="40" rx="4" fill="#2a2a30"/><rect x="${-30 + (k % 2) * 30}" y="${-124 + k * 60}" width="30" height="28" rx="3" fill="${k % 2 ? "#d8352a" : "#3a9c66"}"/>`).join("")}<circle cx="-88" cy="-138" r="5" fill="#8a8f98"/><circle cx="88" cy="-138" r="5" fill="#8a8f98"/><circle cx="-88" cy="138" r="5" fill="#8a8f98"/><circle cx="88" cy="138" r="5" fill="#8a8f98"/></g>
    <g id="${id}-lid" transform="rotate(0)"><g class="ltLidFront"><rect x="-120" y="-170" width="240" height="340" rx="8" fill="#8a8e96"/><rect x="-120" y="-170" width="240" height="340" rx="8" fill="url(#flV)"/><rect x="-30" y="-20" width="60" height="40" rx="6" fill="#3a3a40"/><text x="0" y="-100" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#2a2a30">ไฟฟ้า</text><path d="M-8,60L-22,96H-2L-10,130L18,88H0Z" fill="#d8352a"/></g>
    <g class="ltLidBack" opacity="0" transform="scale(-1,1)"><rect x="-120" y="-170" width="240" height="340" rx="8" fill="#b8b4a8"/><rect x="-108" y="-158" width="216" height="316" rx="6" fill="#d8d4c8"/>${[-120, -60, 0, 60, 100].map((y, k) => `<path d="M-90,${y}h${k === 4 ? 60 : 170}" stroke="#4a4e56" stroke-width="5" stroke-linecap="round" opacity=".7"/>`).join("")}<text x="-90" y="-136" font-family="Kanit" font-weight="800" font-size="22" fill="#c8302a">กฎ ๓ ข้อ</text></g></g></g>`;
  // a lightning bolt between two points: a jagged polyline with a glow, seeded so every frame of a shot agrees
  const bolt = (x0, y0, x1, y1, seed = 1, w = 14) => { let s = seed; const r = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
    const n = 9, pts = [[x0, y0]]; for (let k = 1; k < n; k++) { const t = k / n, dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L, off = (r() - 0.5) * L * 0.16; pts.push([x0 + dx * t + nx * off, y0 + dy * t + ny * off]); } pts.push([x1, y1]);
    const d = "M" + pts.map((p) => `${f(p[0])},${f(p[1])}`).join("L");
    return `<g class="ltBolt"><path d="${d}" stroke="#9ad8ff" stroke-width="${w * 2.6}" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".35"/><path d="${d}" stroke="#dff4ff" stroke-width="${w}" fill="none" stroke-linejoin="round" stroke-linecap="round"/><path d="${d}" stroke="#ffffff" stroke-width="${w * 0.4}" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>`; };
  const sparks = (n = 10, r = 60, seed = 3, c = "#ffe24a") => { let s = seed; const rr = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
    return `<g class="ltSparks">${[...Array(n)].map(() => { const a = rr() * Math.PI * 2, l = r * (0.5 + rr()); return `<path d="M0,0L${f(Math.cos(a) * l)},${f(Math.sin(a) * l)}" stroke="${c}" stroke-width="${f(2 + rr() * 3)}" stroke-linecap="round"/>`; }).join("")}</g>`; };
  const glowRing = (r = 300, c = "#9ad8ff") => `<g class="ltGlow" style="mix-blend-mode:screen"><circle r="${r}" fill="url(#ltAura)"/><circle r="${r * 0.35}" fill="${c}" opacity=".12"/></g>`;
  window.LT = { PHONE, TORCH_W, CASH, CALC, BIKE, GATE, CYL, INC, BABY, TREE, FUSEBOX, bolt, sparks, glowRing };
})();
