// สกิลจอมโกหก v2 · long cut · the top-three heroes and the new props (load after jkcast.js / jkv_cast.js)
//   jkGiant   ยักษ์ใจดีแห่งภูเขา: bald with side tufts, a big brown beard, a fur vest over a moss tunic, a rope belt · draw at scale ~1.9
//             jkGiantClub: the stone club (as tall as a house at his scale) in the near hand
//   jkWitch   แม่มดดอกไม้เหล็ก: a tall steel-grey witch hat with an iron flower, long plum hair, a violet gown, a silver-thorn sash
//             jkWitchWand: a wand topped with an iron flower
//   jkArthur  เซอร์อาเธอร์ผู้ไม่เคยแพ้: swept gold hair, a gold circlet, silver plate with gold trim, a red cape; lie-ears both sides (.jkEar)
//             jkArthurSword: the holy gold sword (raised: rot 180)
//   jkYouPaper: you holding the old insurance paper "ประกันชีวิต มั่นใจ สาขา 112" · jkYouPaperGold: the same paper turned gold
//   jkYouMark: horns + the demon-king mark on the forehead · jkKenHilt: Ken holding the hilt only
(function () {
  const { mix, dk, hi } = Rig2;
  const C = Rig.CAST, S = Flat.SPEC, faces = Sig.sigFaces;
  const earL = `<g class="jkEar" opacity="0"><ellipse cx="-33" cy="-540" rx="13" ry="16" fill="#ff5a3a" opacity=".35"/><ellipse cx="-33" cy="-540" rx="8" ry="10.5" fill="#e8402e"/><ellipse cx="-33" cy="-539" rx="3.8" ry="5.8" fill="#b82418"/></g>`;
  const earR = earL.replace(/cx="-33"/g, 'cx="41"');
  // ---- the giant
  Flat.HAIR.giantTuft = (c) => `<path d="M-44,-520C-50,-548 -46,-566 -36,-574Q-30,-552 -32,-520Z" fill="${c}"/><path d="M44,-520C50,-548 46,-566 38,-574Q32,-552 34,-520Z" fill="${c}"/>
    <path d="M-30,-590Q4,-606 36,-590" stroke="${hi(c, 0.2)}" stroke-width="3" fill="none" opacity=".35"/>`;
  const beard = `<path d="M-40,-530Q-44,-480 -20,-458Q4,-446 26,-458Q48,-480 44,-530Q34,-504 4,-502Q-24,-504 -40,-530Z" fill="#6a4026"/>
    <path d="M-20,-512Q4,-520 26,-512Q4,-500 -20,-512Z" fill="#5a3420"/><path d="M-10,-488Q4,-478 18,-488" stroke="#4a2a18" stroke-width="3" fill="none"/>
    <path d="M-26,-478Q-14,-466 -4,-470M12,-470Q24,-466 32,-478" stroke="#8a5a36" stroke-width="2.4" fill="none" opacity=".7"/>`;
  S.jkGiant = { hair: "giantTuft", faces: faces({ k: 1.05, browW: 7 }), headTop: () => beard,
    acc: (x) => `<path d="M-50,-490L-20,-490L-10,-300H-52Z" fill="#7a5232"/><path d="M50,-490L20,-490L10,-300H52Z" fill="#6e4a2c"/>
      ${[-44, -38, -32, 30, 36, 42].map((xx, i) => `<path d="M${xx},${-470 + (i % 3) * 50}l6,10l6,-10" stroke="#5a3a20" stroke-width="2" fill="none"/>`).join("")}
      <path d="M-50,-330Q0,-318 50,-330L50,-314Q0,-302 -50,-314Z" fill="#c8a46a"/><path d="M-8,-326q8,22 16,0" stroke="#a8844a" stroke-width="5" fill="none"/>` };
  C.jkGiant = { v2: { skin: "#c49068", hair: { c: "#6a4026" }, top: { kind: "tee", c: "#6a8a52", sleeve: "none" }, bottom: { kind: "trousers", c: "#5a4a3a" }, feet: { kind: "boot", c: "#4a3020" }, w: 1.35 } };
  const CLUB = `<g transform="translate(0,112) rotate(-160)"><rect x="-10" y="-10" width="20" height="120" rx="8" fill="#6a4a2a"/><path d="M-10,90L10,90L10,110L-10,110Z" fill="#4a3018"/>
    <path d="M-34,100Q-52,180 -38,300Q0,336 38,300Q54,180 34,100Z" fill="#8a8680"/><path d="M-30,140Q-40,220 -28,290" stroke="#6e6a64" stroke-width="8" fill="none"/>
    <circle cx="10" cy="170" r="9" fill="#6e6a64"/><circle cx="-8" cy="240" r="11" fill="#6e6a64"/><circle cx="16" cy="270" r="7" fill="#6e6a64"/><path d="M20,120Q34,200 24,290" stroke="#a8a49c" stroke-width="5" fill="none" opacity=".6"/></g>`;
  C.jkGiantClub = { v2: C.jkGiant.v2, hand: CLUB, keep: "F" }; S.jkGiantClub = S.jkGiant;
  // ---- the witch
  const hat = `<g><path d="M-62,-574Q4,-560 70,-576L66,-560Q4,-544 -58,-558Z" fill="#4a4a5a"/><path d="M-34,-570Q-10,-660 30,-730Q24,-690 40,-660Q38,-610 42,-570Z" fill="#5a5a6c"/>
    <path d="M-30,-588Q4,-578 40,-588L42,-572Q4,-562 -32,-572Z" fill="#8a2a4a"/>
    <g transform="translate(26,-596)"><circle r="7" fill="#c8ccd4"/>${[0, 60, 120, 180, 240, 300].map((a) => `<path d="M0,0Q-6,-16 0,-24Q6,-16 0,0Z" fill="#9aa0ac" stroke="#6a707c" stroke-width="1.5" transform="rotate(${a})"/>`).join("")}<circle r="5" fill="#e8d070"/></g>
    <path d="M30,-730l14,6" stroke="#5a5a6c" stroke-width="6" stroke-linecap="round"/></g>`;
  S.jkWitch = { hair: "long", hairB: "longB", faces: faces({ k: 0.78, browW: 3.4 }), headTop: () => hat,
    acc: () => `<path d="M-46,-488Q0,-460 46,-488L46,-470Q0,-444 -46,-470Z" fill="#3a2a4a"/><path d="M-46,-340L46,-360L46,-344L-46,-324Z" fill="#9aa0ac"/>
      ${[-36, -18, 0, 18, 36].map((xx) => `<path d="M${xx},${-336 - xx * 0.2}l4,-8l4,8" fill="#c8ccd4"/>`).join("")}<circle cx="0" cy="-440" r="7" fill="#c8ccd4"/>` };
  C.jkWitch = { v2: { skin: "#e8c8b4", hair: { c: "#5a2a5a" }, top: { kind: "tee", c: "#5a3a7a", sleeve: "long" }, bottom: { kind: "sarong", c: "#4a2e6a", band: "#9aa0ac" }, feet: { kind: "boot", c: "#2a2030" }, w: 0.94 } };
  const WAND = `<g transform="translate(0,112) rotate(-170)"><rect x="-4" y="-6" width="8" height="150" rx="3" fill="#3a2a30"/><g transform="translate(0,150)"><circle r="9" fill="#c8ccd4"/>${[0, 72, 144, 216, 288].map((a) => `<path d="M0,0Q-8,18 0,30Q8,18 0,0Z" fill="#9aa0ac" stroke="#6a707c" stroke-width="1.5" transform="rotate(${a})"/>`).join("")}<circle r="6" fill="#e8d070"/></g></g>`;
  C.jkWitchWand = { v2: C.jkWitch.v2, hand: WAND, keep: "F" }; S.jkWitchWand = S.jkWitch;
  // ---- Sir Arthur
  Flat.HAIR.swept = (c) => `<path d="M-44,-530C-50,-584 -18,-604 8,-604C40,-604 58,-584 52,-552Q46,-566 30,-574Q60,-560 60,-536Q46,-560 20,-566Q-8,-570 -26,-560Q-34,-548 -36,-530Z" fill="${c}"/>
    <path d="M-14,-596Q20,-606 44,-588" stroke="${hi(c, 0.32)}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>`;
  Flat.HAIR.capeB = (c) => `<path d="M-50,-492Q-70,-300 -64,-130Q0,-110 64,-130Q70,-300 50,-492Z" fill="#b82a2a"/><path d="M-30,-480Q-40,-300 -36,-140" stroke="#8e1e1e" stroke-width="6" fill="none"/><path d="M24,-480Q34,-300 30,-140" stroke="#8e1e1e" stroke-width="6" fill="none"/>`;
  const circlet = `<path d="M-40,-578Q4,-590 48,-578" stroke="#e8c048" stroke-width="6" fill="none"/><path d="M0,-588l6,-12l6,12z" fill="#e8c048"/><circle cx="6" cy="-584" r="4" fill="#3a8ad0"/>`;
  S.jkArthur = { hair: "swept", hairB: "capeB", faces: faces({ k: 0.92, browW: 5 }), headTop: () => circlet + earL + earR,
    acc: () => `<path d="M-48,-494Q0,-470 48,-494L50,-456Q0,-430 -50,-456Z" fill="#c4ccd4"/><path d="M-48,-494Q0,-470 48,-494" stroke="#e8c048" stroke-width="4" fill="none"/>
      <path d="M-40,-450H40L36,-330H-36Z" fill="#b4bcc6" opacity=".9"/><path d="M0,-446V-334" stroke="#e8c048" stroke-width="5"/><path d="M-22,-410h44" stroke="#e8c048" stroke-width="4"/>
      <path d="M-46,-330H46V-312H-46Z" fill="#6a4a2a"/><rect x="-9" y="-334" width="18" height="24" rx="3" fill="#e8c048"/>` };
  C.jkArthur = { v2: { skin: "#e0b08a", hair: { c: "#f0d070" }, top: { kind: "coat", c: "#9aa4b4", sleeve: "long" }, bottom: { kind: "trousers", c: "#5a6474" }, feet: { kind: "boot", c: "#6a6e78" }, w: 1.05 } };
  const GSWORD = (rot) => `<g transform="translate(0,112) rotate(${rot})"><rect x="-6" y="-10" width="12" height="44" rx="5" fill="#6a3a24"/><rect x="-30" y="32" width="60" height="12" rx="5" fill="#e8c048"/><circle cy="-12" r="8" fill="#e8c048"/>
    <path d="M-11,44L-11,350L0,396L11,350L11,44Z" fill="#fff4c0"/><path d="M-26,44L-26,356L0,420L26,356L26,44Z" fill="#ffd040" opacity=".45"/><path d="M-52,44L-52,366L0,462L52,366L52,44Z" fill="#ffd040" opacity=".16"/><path d="M-3,52V340" stroke="#fff" stroke-width="3" opacity=".9"/></g>`;
  C.jkArthurSword = { v2: C.jkArthur.v2, hand: GSWORD(-30), keep: "F" }; S.jkArthurSword = S.jkArthur;
  C.jkArthurSwordUp = { v2: C.jkArthur.v2, hand: GSWORD(180), keep: "F" }; S.jkArthurSwordUp = S.jkArthur;
  // ---- props for you and Ken
  const PAPER = (gold) => `<g transform="translate(0,112) rotate(-12)"><rect x="-34" y="-96" width="68" height="92" rx="3" fill="${gold ? "#ffe07a" : "#f8f4ea"}" stroke="${gold ? "#c89a20" : "#c8c0b0"}" stroke-width="2"/>
    <rect x="-34" y="-96" width="68" height="20" fill="${gold ? "#e8a820" : "#2a4a8a"}"/><text x="0" y="-81" font-family="Kanit" font-weight="900" font-size="11" fill="#fff" text-anchor="middle">ประกันชีวิต</text>
    <path d="M-24,-62h48M-24,-50h40M-24,-38h44M-24,-26h30" stroke="${gold ? "#b08020" : "#9a9aa4"}" stroke-width="4"/><circle cx="18" cy="-18" r="9" fill="none" stroke="${gold ? "#c82020" : "#c84040"}" stroke-width="3"/>
    <text x="-10" y="-12" font-family="Kanit" font-weight="900" font-size="10" fill="${gold ? "#8a5a10" : "#5a5a66"}" text-anchor="middle">112</text></g>`;
  C.jkYouPaper = { v2: C.jkYou.v2, hand: PAPER(false), keep: "F" }; S.jkYouPaper = S.jkYou;
  C.jkYouPaperGold = { v2: C.jkYou.v2, hand: PAPER(true), keep: "F" }; S.jkYouPaperGold = S.jkYou;
  const mark = `<g class="jkMark"><path d="M4,-578l7,12h-14z" fill="#d82a3a"/><circle cx="4" cy="-566" r="9" fill="none" stroke="#d82a3a" stroke-width="3"/><path d="M4,-575v14M-3,-568h14" stroke="#ff8a8a" stroke-width="1.6"/></g>`;
  const horns = `<g class="jkHorn"><path d="M-26,-588Q-44,-640 -20,-676Q-30,-636 -6,-596Z" fill="#3a1a24"/><path d="M30,-590Q50,-640 28,-680Q40,-636 14,-598Z" fill="#3a1a24"/>
    <path d="M-24,-600Q-34,-630 -22,-654" stroke="#6a3a44" stroke-width="3" fill="none"/><path d="M28,-602Q38,-630 28,-656" stroke="#6a3a44" stroke-width="3" fill="none"/></g>`;
  const youEar = S.jkYou.headTop;
  S.jkYouMark = { ...S.jkYou, headTop: () => youEar() + horns + mark }; C.jkYouMark = { v2: C.jkYou.v2 };
  S.jkYouMarkPaper = S.jkYouMark; C.jkYouMarkPaper = { v2: C.jkYou.v2, hand: PAPER(false), keep: "F" };
  S.jkYouMarkPaperGold = S.jkYouMark; C.jkYouMarkPaperGold = { v2: C.jkYou.v2, hand: PAPER(true), keep: "F" };
  const HILT = `<g transform="translate(0,112) rotate(-20)"><rect x="-6" y="-8" width="12" height="40" rx="5" fill="#5a3a24"/><rect x="-26" y="30" width="52" height="10" rx="4" fill="#d8b84a"/><path d="M-8,40L-6,58L0,52L4,62L8,40Z" fill="#c8e8ff"/></g>`;
  C.jkKenHilt = { v2: C.jkKen.v2, hand: HILT, keep: "F" }; S.jkKenHilt = S.jkKen;
  window.JK.PAPER = PAPER; window.JK.GSWORD = GSWORD; window.JK.CLUB = CLUB;
})();
