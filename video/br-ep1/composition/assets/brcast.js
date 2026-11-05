// บางระจัน แบต 3% (story 2) · the cast in the channel look (sig.js faces on flat.js bodies). Load after jkcast.js.
//   brKeng    เก่ง: a 2569 kid in a blue football shirt (number 10, phone in the chest pocket), navy shorts, flip-flops, bed-head hair
//             variants brKengPhone (phone in hand, screen lit), brKengTorch (phone held up as a torch), brKengTied (same body; rope is drawn by the shot)
//   brJuk     จุก: a small boy with a topknot, bare chest, a red waist cloth, a wooden sword · brJukSword
//   brTaeng   แตง: his big sister, hair bun, a mustard breast cloth, a dark red sarong, arms folded (mode fold)
//   brPhaeo   ยายแผ้ว: the camp cook: grey bun, a sabai across the chest, betel-dark mouth <g class="brBetel"> (opacity 0 → 1 for the grin)
//             variants brPhaeoLadle, brPhaeoTorch · brGranny: the same face in 2569 clothes (the ending)
//   brMan1..3, brWom1: villagers (ผ้าขาวม้า, sarongs, spears/dha) · brManSpear brManDha
//   BR.buffalo(o)  ไอ้ดำ, side on, facing right (scale(-1,1) to face left): <g class="brTongue"> to lick, <g class="brBufLeg"> to run
//   BR.enemy(x, y, s)  a torch-bearing silhouette for the fog · BR.PHONE BR.TORCH BR.LIME BR.limeRow BR.DRUM BR.CHICKEN BR.BANANA BR.POT BR.MORTAR
(function () {
  const { mix, dk, hi } = Rig2;
  const C = Rig.CAST, S = Flat.SPEC, faces = Sig.sigFaces;
  const f = (v) => (+v).toFixed(1);

  // ---------------- hair ----------------
  Flat.HAIR.bedhead = (c) => `<path d="M-43,-532C-50,-574 -28,-600 2,-600C30,-600 50,-586 46,-556Q38,-570 24,-572Q6,-574 -8,-572Q-22,-566 -30,-556Q-34,-546 -35,-532Z" fill="${c}"/>
    <path d="M-34,-588Q-50,-598 -48,-614Q-34,-606 -22,-598Z" fill="${c}"/><path d="M28,-590Q46,-598 50,-612Q38,-604 24,-597Z" fill="${c}"/><path d="M-6,-598Q-2,-614 8,-616Q6,-606 10,-600Z" fill="${c}"/>
    <path d="M-16,-586Q0,-592 16,-586" stroke="${hi(c, 0.3)}" stroke-width="4" stroke-linecap="round" opacity=".5"/>`;

  // ---------------- เก่ง ----------------
  const kit = () => `<path d="M-18,-492L0,-464L18,-492" stroke="#f4f4f4" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M-44,-470V-304M44,-470V-304" stroke="#f4f4f4" stroke-width="5" opacity=".85"/><rect x="-16" y="-452" width="32" height="7" rx="3" fill="#f4f4f4" opacity=".8"/>
    <text x="1" y="-386" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#f4f4f4" opacity=".95">10</text>
    <g class="brPocket"><rect x="16" y="-448" width="20" height="34" rx="3" fill="#1a1a22"/><rect x="18" y="-445" width="16" height="26" rx="2" fill="#243a66"/></g>`;
  S.brKeng = { hair: "bedhead", faces: faces({ browW: 4.6 }), acc: kit };
  C.brKeng = { v2: { skin: "#d8a878", hair: { c: "#1c1612" }, top: { kind: "tee", c: "#2a7ad8", sleeve: "short" }, bottom: { kind: "shorts", c: "#1c2a44" }, feet: { kind: "sandal", c: "#2a2a2a" }, w: 1.0 } };
  const PHONE = `<g transform="translate(0,112) rotate(-14)"><rect x="-22" y="-60" width="44" height="84" rx="7" fill="#1a1a22"/><rect x="-18" y="-54" width="36" height="66" rx="4" fill="#243a66" class="brScr"/>
    <rect x="-10" y="-48" width="20" height="8" rx="4" fill="#5ab0ff" class="brScr"/><rect x="-14" y="-34" width="28" height="4" rx="2" fill="#8ab8ff" opacity=".7" class="brScr"/><rect x="-14" y="-26" width="20" height="4" rx="2" fill="#8ab8ff" opacity=".5" class="brScr"/>
    <g class="brScrOff" opacity="0"><rect x="-18" y="-54" width="36" height="66" rx="4" fill="#101016"/></g></g>`;
  const PHONE_UP = `<g transform="translate(0,112) rotate(-150)"><rect x="-22" y="-60" width="44" height="84" rx="7" fill="#1a1a22"/><rect x="-18" y="-54" width="36" height="66" rx="4" fill="#101016"/><circle cx="-8" cy="-44" r="5" fill="#fff8d0" class="brLamp"/></g>`;
  C.brKengPhone = { v2: C.brKeng.v2, hand: PHONE, keep: "F" };
  C.brKengTorch = { v2: C.brKeng.v2, hand: PHONE_UP, keep: "F" };
  S.brKengPhone = S.brKeng; S.brKengTorch = S.brKeng;

  // ---------------- จุก and แตง ----------------
  const sash = () => `<path d="M-44,-330Q0,-318 44,-330L44,-300H-44Z" fill="#c8342a"/><path d="M30,-318L52,-270L40,-266L24,-306Z" fill="#a8241e"/>`;
  S.brJuk = { hair: "juk", faces: faces({ k: 1.3, browW: 4 }), headScale: 1.22, acc: sash, headTop: () => `<ellipse cx="31" cy="-529" rx="7" ry="4.4" fill="#e0705e" opacity=".3"/>` };
  C.brJuk = { v2: { skin: "#c8905e", hair: { c: "#1c1612" }, top: { kind: "tank", c: "#c8905e" }, bottom: { kind: "shorts", c: "#8a3a2a" }, feet: { kind: "bare" }, w: 1.06, limb: 0.9 } };
  const SWORDW = `<g transform="translate(0,112) rotate(-176)"><rect x="-5" y="-10" width="10" height="36" rx="3" fill="#6a4a2a"/><rect x="-18" y="24" width="36" height="8" rx="3" fill="#8a6a3a"/><path d="M-7,32L-5,170Q0,182 5,170L7,32Z" fill="#b89058"/><path d="M-2,36V160" stroke="#8a6a3a" stroke-width="2"/></g>`;
  C.brJukSword = { v2: C.brJuk.v2, hand: SWORDW, keep: "F" }; S.brJukSword = S.brJuk;
  S.brTaeng = { hair: "bun", faces: faces({ k: 1.12, browW: 3.6 }), headScale: 1.1, acc: () => `<path d="M-45,-470H45L43,-430H-43Z" fill="${dk("#c8a060", 0.12)}"/><circle cx="-28" cy="-452" r="4" fill="#d8443a"/>` };
  C.brTaeng = { v2: { skin: "#d0986a", hair: { c: "#1c1612" }, top: { kind: "tank", c: "#c8a060" }, bottom: { kind: "sarong", c: "#7a3a3a", band: "#d8b84a" }, feet: { kind: "bare" }, w: 0.94, limb: 0.94 } };

  // ---------------- ยายแผ้ว ----------------
  const sabai = () => `<path d="M-50,-492L-12,-492L52,-300L14,-300Z" fill="#a83848"/><path d="M-50,-492L-12,-492L52,-300L14,-300Z" fill="url(#flV)"/><path d="M-40,-470L30,-320" stroke="#d8b84a" stroke-width="2" opacity=".6"/>`;
  const betel = `<g class="brBetel" opacity="0"><path d="M-16,-521Q4,-500 24,-521Q4,-526 -16,-521Z" fill="#2a0e10"/><path d="M-10,-519Q4,-512 18,-519" stroke="#161014" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-8,-516Q4,-507 16,-516" stroke="#3a1a1a" stroke-width="2" fill="none"/></g>`;
  S.brPhaeo = { hair: "bun", faces: faces({ crinkle: true, k: 0.86, browW: 3.4 }), acc: sabai, headTop: () => betel };
  C.brPhaeo = { v2: { skin: "#c89a70", hair: { c: "#cfc6bc" }, top: { kind: "tank", c: "#e8dcc0" }, bottom: { kind: "sarong", c: "#4a3a5a", band: "#8a6a3a" }, feet: { kind: "bare" }, w: 1.12 } };
  const LADLE = `<g transform="translate(0,112) rotate(-40)"><rect x="-4" y="-120" width="8" height="140" rx="3" fill="#8a6a3a"/><ellipse cx="0" cy="24" rx="20" ry="12" fill="#6a4a2a"/><ellipse cx="0" cy="22" rx="14" ry="7" fill="#9a7a4a"/></g>`;
  const flame = (cls = "brFlame") => `<g class="${cls}"><path d="M0,0Q-22,-34 -6,-70Q0,-50 8,-62Q22,-30 0,0Z" fill="#ff9a3a"/><path d="M0,-6Q-10,-30 -2,-50Q4,-36 8,-44Q14,-24 0,-6Z" fill="#ffd860"/></g>`;
  const TORCH = `<g transform="translate(0,112) rotate(-160)"><rect x="-6" y="-10" width="12" height="150" rx="4" fill="#5a3a1c"/><path d="M-14,-10H14L10,-30H-10Z" fill="#8a6a3a"/><g transform="translate(0,-30)">${flame()}</g></g>`;
  C.brPhaeoLadle = { v2: C.brPhaeo.v2, hand: LADLE, keep: "F" }; S.brPhaeoLadle = S.brPhaeo;
  C.brPhaeoTorch = { v2: C.brPhaeo.v2, hand: TORCH, keep: "F" }; S.brPhaeoTorch = S.brPhaeo;
  S.brGranny = { hair: "bun", faces: faces({ crinkle: true, k: 0.86, browW: 3.4 }), glasses: "round", acc: () => `<circle cx="-18" cy="-440" r="7" fill="#f4ecd8" opacity=".9"/><circle cx="8" cy="-420" r="6" fill="#f4ecd8" opacity=".8"/><circle cx="22" cy="-452" r="5" fill="#f4ecd8" opacity=".8"/>` };
  C.brGranny = { v2: { skin: "#c89a70", hair: { c: "#cfc6bc" }, top: { kind: "tee", c: "#d88aa0", sleeve: "elbow" }, bottom: { kind: "trousers", c: "#4a4a5a" }, feet: { kind: "sandal", c: "#6a4a3a" }, w: 1.12 } };

  // ---------------- villagers ----------------
  const khaoma = (c1, c2) => () => `<path d="M-48,-490L-16,-490L30,-300L-2,-300Z" fill="${c1}"/>${[-36, -24, -12, 0].map((d) => `<path d="M${-48 + d * 0.3},${-490 + d * 4}L${-16 - 0},-490" stroke="${c2}" stroke-width="2" opacity=".5"/>`).join("")}<path d="M-42,-470L18,-320M-30,-480L26,-340" stroke="${c2}" stroke-width="3" opacity=".6"/>`;
  const SPEAR = `<g transform="translate(0,112) rotate(-6)"><rect x="-4" y="-300" width="8" height="380" rx="3" fill="#6a4a2a"/><path d="M-12,-300L0,-350L12,-300Z" fill="#c4ccd4"/></g>`;
  const DHA = `<g transform="translate(0,112) rotate(-130)"><rect x="-5" y="-6" width="10" height="40" rx="4" fill="#5a3a24"/><rect x="-14" y="30" width="28" height="8" rx="4" fill="#8a6a3a"/><path d="M-7,38L-9,190Q2,206 10,188L7,38Z" fill="#c4ccd4"/><path d="M-1,44V180" stroke="#9aa2aa" stroke-width="2"/></g>`;
  [["brMan1", "buzz", "#2a2420", "#c8905e", "#6a3a2a", "#b88660", 1.14, khaoma("#c84a3a", "#f4ecd8")], ["brMan2", "short", "#3a2a24", "#8a6a4a", "#3a4a6a", "#d4a07a", 1.0, khaoma("#3a6aa8", "#f4ecd8")],
   ["brMan3", "horseshoe", "#8a8680", "#a8a090", "#5a3a3a", "#c08a62", 1.2, () => ""], ["brWom1", "bun", "#2a2420", "#d88a6a", "#3a5a4a", "#d8a47c", 0.98, () => ""]].forEach(([n, hair, hc, tc, bc, sk, w, acc]) => {
    S[n] = { hair, faces: faces({ k: 0.9 }), acc, tache: n === "brMan3" ? "#8a8680" : undefined };
    C[n] = { v2: { skin: sk, hair: { c: hc }, top: { kind: "tank", c: tc }, bottom: { kind: "sarong", c: bc, band: "#8a6a3a" }, feet: { kind: "bare" }, w } };
  });
  C.brManSpear = { v2: C.brMan1.v2, hand: SPEAR, keep: "F" }; S.brManSpear = S.brMan1;
  C.brManDha = { v2: C.brMan2.v2, hand: DHA, keep: "F" }; S.brManDha = S.brMan2;

  // ---------------- poses for this story ----------------
  const M = Rig.MODES, Z = (u, o) => M.idle(u, o);
  M.tied = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.4); return { ...Z(u, o), uaF: 6, faF: 4, uaB: 6, faB: 4, head: 6 + 2 * b, torso: 2, bodyY: 0 }; };   // arms straight down, pinned by the rope
  M.tiedStruggle = (u, o) => { const j = Math.sin(u * 29) * 2; return { ...Z(u, o), uaF: 8 + j, faF: 6, uaB: 8 - j, faB: 6, head: -4 + j, torso: 3 - j, bodyY: 0 }; };
  M.chin = (u, o) => ({ ...M.tied(u, o), head: 26 + 3 * Math.sin(u * 7), torso: 9 });           // chin pushing the phone out of the pocket
  M.listen = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 0.9); return { ...Z(u, o), uaF: -118, faF: -156, uaB: 10, faB: -8, head: 6 + 4 * b, torso: 2 }; };   // phone to the ear, nodding
  M.chew = (u, o) => ({ ...Z(u, o), uaF: -96, faF: -150, head: 4 + 3 * Math.sin(u * 2 * Math.PI / 0.4), torso: 3 });
  M.hugKnees = (u, o) => { const b = Math.sin(u * 1.2); return { ...Z(u, o), thF: -150, shF: 150, thB: -146, shB: 148, uaF: -82, faF: -112, uaB: 72, faB: 112, torso: 14 + b * 0.5, head: 18 + b, bodyY: 288 }; };   // on the ground, knees up at the chest, arms around them
  M.kneelBow = (u, o) => ({ ...Z(u, o), thF: 4, shF: 112, thB: 8, shB: 114, uaF: -64, faF: -6, uaB: 60, faB: 6, torso: 52, head: 24, bodyY: 150 });   // knees on the ground, shins folded back, bowed to the floor
  M.torchRun = (u, o) => { const w = M.run ? M.run(u, o) : M.walk(u, o); return { ...w, uaF: -160, faF: -20, head: -6, torso: -8 }; };
  M.pointSword = (u, o) => { const j = Math.sin(u * 33) * 2.5; return { ...Z(u, o), uaF: -92 + j, faF: 6, uaB: 30, faB: 40, head: -2 + j, torso: -4, bodyY: 0 }; };
  M.foldX = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 3.0); return { ...Z(u, o), uaF: -26, faF: 128 + 2 * b, uaB: 30, faB: -128, head: -3 + b, torso: -3, bodyY: -1 }; };
  M.whistle = (u, o) => ({ ...Z(u, o), head: -14 + 2 * Math.sin(u * 1.3), torso: -2, uaF: -8, faF: -24, uaB: 8, faB: 24 });
  M.patHead = (u, o) => ({ ...Z(u, o), uaF: -126, faF: -40 + 6 * Math.sin(u * 2 * Math.PI / 0.8), head: 8, torso: 6 });

  // ---------------- props and creatures ----------------
  const LIME = (x, y, s = 1) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})"><circle r="22" fill="#9ac83a"/><circle cx="-7" cy="-7" r="8" fill="#b8e05a" opacity=".6"/><circle cx="6" cy="8" r="12" fill="#86b42e" opacity=".5"/><rect x="-3" y="-38" width="6" height="24" rx="1" fill="#7a7a80"/><rect x="-6" y="-40" width="12" height="4" fill="#5a5a60"/></g>`;
  const limeRow = (x0, y, n, gap = 56, s = 1) => { let h = ""; for (let k = 0; k < n; k++) { const x = x0 + k * gap; if (k) h += `<path d="M${f(x - gap + 6)},${f(y - 38 * s)}Q${f(x - gap / 2)},${f(y - 70 * s)} ${f(x - 6)},${f(y - 38 * s)}" stroke="${k % 2 ? "#d84a3a" : "#2a2a30"}" stroke-width="3" fill="none"/>`; h += LIME(x, y, s); } return h; };
  const DRUM = `<g><path d="M-30,-150H30L22,70H-22Z" fill="#8a5a32"/><path d="M-30,-150H30L22,70H-22Z" fill="url(#flV)"/><ellipse cy="-150" rx="30" ry="10" fill="#e8d8b0"/><ellipse cy="-150" rx="24" ry="7" fill="#f4ecd8"/>${[-120, -90, -60, -30, 0, 30].map((y) => `<path d="M-30,${y}H30" stroke="#5a3a1c" stroke-width="2" opacity=".6"/>`).join("")}</g>`;
  const CHICKEN = `<g transform="translate(0,112) rotate(-70)"><rect x="-3" y="0" width="6" height="150" fill="#b89058"/><path d="M-26,0Q-36,-50 -10,-66Q20,-74 34,-44Q42,-14 20,4Z" fill="#c87a3a"/><path d="M-20,-10Q-26,-44 -6,-56" stroke="#8a4a1a" stroke-width="3" fill="none"/><path d="M-30,2Q-50,20 -46,36" stroke="#f4ecd8" stroke-width="5" stroke-linecap="round"/></g>`;
  const BANANA = `<g>${[0, 1, 2, 3, 4].map((k) => `<path d="M${-30 + k * 14},-10Q${-30 + k * 14 + 4},-60 ${-16 + k * 14},-90" stroke="#e8c84a" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M${-30 + k * 14},-10Q${-30 + k * 14 + 4},-60 ${-16 + k * 14},-90" stroke="#c8a830" stroke-width="4" fill="none" stroke-linecap="round" opacity=".5"/>`).join("")}<path d="M-34,-92Q0,-110 34,-92" stroke="#6a5a2a" stroke-width="10" stroke-linecap="round" fill="none"/></g>`;
  const STICKY = `<g><path d="M-40,0Q-44,-70 0,-70Q44,-70 40,0Z" fill="#c8a860"/><path d="M-36,-18H36M-40,-36H40M-38,-54H38" stroke="#a8884a" stroke-width="3"/><ellipse cy="-70" rx="30" ry="8" fill="#e8d8b0"/></g>`;
  const POT = `<g><path d="M-120,0Q-130,-30 -100,-40H100Q130,-30 120,0Z" fill="#6a4a30"/><g class="brFire"><path d="M-30,-40Q-40,-80 -10,-100Q-4,-76 10,-90Q26,-60 6,-42Z" fill="#ff9a3a"/><path d="M-14,-42Q-18,-66 -2,-80Q2,-66 10,-72Q14,-56 2,-44Z" fill="#ffd860"/></g>
    <path d="M-110,-40Q-120,-120 -80,-170Q0,-200 80,-170Q120,-120 110,-40Z" fill="#9a6a44"/><path d="M-110,-40Q-120,-120 -80,-170Q0,-200 80,-170Q120,-120 110,-40Z" fill="url(#flV)"/><ellipse cy="-172" rx="84" ry="16" fill="#5a3a24"/><ellipse cy="-176" rx="70" ry="11" fill="#b89a6a"/>
    <g class="brSteam" opacity=".55">${[-40, 0, 40].map((x, k) => `<path d="M${x},-190q-14,-30 0,-60q12,-26 -2,-56" stroke="#fff" stroke-width="${8 - k}" fill="none" stroke-linecap="round" opacity=".6"/>`).join("")}</g></g>`;
  const MORTAR = `<g><path d="M-44,-70H44L34,10H-34Z" fill="#5a4a44"/><path d="M-44,-70H44L34,10H-34Z" fill="url(#flV)"/><ellipse cy="-70" rx="44" ry="12" fill="#3a2e2a"/><g class="brPestle" transform="translate(16,-70) rotate(20)"><rect x="-8" y="-120" width="16" height="130" rx="7" fill="#8a6a3a"/></g></g>`;
  const buffalo = (o = {}) => `<g class="brBuf"><ellipse cx="0" cy="-150" rx="150" ry="92" fill="#2a2624"/><ellipse cx="-30" cy="-120" rx="120" ry="60" fill="#221d1b"/><path d="M-110,-200Q0,-250 120,-200" stroke="#3a3430" stroke-width="14" fill="none" stroke-linecap="round" opacity=".7"/>
    <path d="M-150,-150Q-200,-150 -210,-100" stroke="#2a2624" stroke-width="18" fill="none" stroke-linecap="round"/><circle cx="-212" cy="-96" r="15" fill="#1a1614"/>
    <g class="brBufLeg">${[-100, -46, 50, 104].map((x) => `<rect x="${x - 17}" y="-92" width="34" height="92" rx="10" fill="#241f1d"/><rect x="${x - 20}" y="-10" width="40" height="12" rx="4" fill="#121010"/>`).join("")}</g>
    <g class="brBufHead" transform="translate(150,-176)"><path d="M-30,-34Q60,-64 94,-12Q104,30 70,52Q30,62 -14,42Z" fill="#2a2624"/>
      <path d="M16,-36Q-40,-74 -76,-136Q-30,-88 28,-48Z" fill="#3e3834"/><path d="M-4,-30Q-70,-44 -124,-112Q-84,-56 -2,-46Z" fill="#5a5450"/><path d="M-4,-30Q-70,-44 -124,-112" stroke="#2a2624" stroke-width="3" fill="none"/><ellipse cx="-20" cy="-22" rx="20" ry="11" fill="#2a2624" transform="rotate(-20 -20 -22)"/>
      <circle cx="40" cy="-6" r="8" fill="#f4ecd8"/><circle cx="43" cy="-5" r="4.5" fill="#111"/><circle cx="44" cy="-7" r="1.5" fill="#fff"/><circle cx="86" cy="34" r="6" fill="#111"/>
      <g class="brTongue" transform="translate(70,46)"><path d="M-10,0Q0,44 22,34Q34,22 18,-4Z" fill="#e87a8a"/><path d="M4,6Q8,24 16,26" stroke="#c85a6a" stroke-width="3" fill="none"/></g></g></g>`;
  const enemy = (x, y, s = 1, k = 0) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})" opacity=".9"><path d="M-26,0Q-34,-120 -10,-200Q0,-230 10,-200Q34,-120 26,0Z" fill="#161218"/><circle cy="-224" r="22" fill="#161218"/><path d="M-30,-180L-60,-120M30,-180L52,-150" stroke="#161218" stroke-width="12" stroke-linecap="round"/>
    <rect x="46" y="-320" width="7" height="170" fill="#2a2018"/><g transform="translate(50,-320)">${flame("brFlame brFlame" + k)}</g></g>`;
  // hand props for EP.2: the cook's chicken leg, the offerings (a bunch of bananas, a bowl of sticky rice)
  const BOWL = `<g transform="translate(0,112)"><path d="M-30,-6Q-34,24 0,26Q34,24 30,-6Z" fill="#6a4a30"/><ellipse cy="-6" rx="30" ry="9" fill="#e8d8b0"/><ellipse cy="-9" rx="22" ry="6" fill="#f4ecd8"/></g>`;
  const BANANA_H = `<g transform="translate(0,112) scale(.7) rotate(20)">${BANANA}</g>`;
  const LIME_H = `<g transform="translate(0,112)">${LIME(0, 0, 0.9)}</g>`;
  C.brKengLime = { v2: C.brKeng.v2, hand: LIME_H, keep: "F" }; S.brKengLime = S.brKeng;
  C.brPhaeoChicken = { v2: C.brPhaeo.v2, hand: CHICKEN, keep: "F" }; S.brPhaeoChicken = S.brPhaeo;
  C.brMan2Banana = { v2: C.brMan2.v2, hand: BANANA_H, keep: "F" }; S.brMan2Banana = S.brMan2;
  C.brWom1Bowl = { v2: C.brWom1.v2, hand: BOWL, keep: "F" }; S.brWom1Bowl = S.brWom1;
  window.BR = { PHONE, PHONE_UP, SWORDW, LADLE, TORCH, SPEAR, DHA, LIME, limeRow, DRUM, CHICKEN, BANANA, STICKY, POT, MORTAR, BOWL, buffalo, enemy, flame };
})();
