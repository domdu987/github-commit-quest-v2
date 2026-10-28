// เห็ดปอบ cast drawn with rig v2 (rig2.js). Same names as pop.js, so every shot keeps working; the old puppets stay as <name>1.
(function () {
  const { LINE, dk, hi, shade } = Rig2;
  const C = Rig.CAST;
  for (const k of ["mint", "ton", "yai", "thong", "boon", "khem", "doc"]) C[k + "1"] = C[k];
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round"`;

  // ---------------- hair ----------------
  const longFront = (h, x) => `
    <path d="M-42,-566Q-34,-552 -24,-564Q-12,-552 -2,-566Q10,-554 20,-574Q32,-560 44,-558L46,-580L-46,-580Z" fill="${x.skinD}" opacity=".35"/>
    <path d="M-50,-562C-60,-532 -60,-498 -53,-466Q-46,-474 -42,-494C-40,-520 -40,-546 -40,-568Z" fill="${h.c}" ${ln()}/>
    <path d="M50,-568C59,-536 61,-500 57,-468C55,-448 57,-432 63,-418Q47,-422 45,-452C43,-490 43,-530 42,-568Z" fill="${h.c}" ${ln()}/>
    <path d="M-50,-546C-60,-612 -20,-632 4,-630C36,-629 62,-606 53,-546C50,-560 47,-568 42,-566Q32,-572 21,-586Q12,-568 -2,-574Q-12,-564 -24,-577Q-34,-566 -43,-572Q-47,-560 -50,-546Z" fill="${h.c}" ${ln()}/>
    <path d="M-32,-620Q-42,-594 -38,-576M0,-628Q-6,-602 -4,-578M30,-622Q36,-598 24,-588M52,-540Q54,-500 51,-470M-50,-530Q-52,-500 -50,-476" stroke="${h.s}" stroke-width="2.6" fill="none" opacity=".75" stroke-linecap="round"/>
    <path d="M-38,-598Q-30,-610 -18,-616M-6,-620Q6,-622 16,-619M26,-614Q36,-608 40,-598" stroke="${h.sh}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>
    <path d="M-30,-606Q-24,-612 -16,-615" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".3"/>`;
  const longBack = (h) => `
    <path d="M-54,-580C-66,-530 -72,-470 -66,-416Q-54,-404 -44,-416Q-32,-404 -18,-414L18,-414Q32,-404 44,-416Q56,-404 68,-416C74,-470 68,-530 58,-580C50,-630 -46,-630 -54,-580Z" fill="${dk(h.c, 0.12)}" ${ln()}/>
    <path d="M-60,-540Q-64,-480 -58,-424M62,-540Q66,-480 60,-424" stroke="${h.s}" stroke-width="2.6" fill="none" opacity=".7"/>`;
  const buzz = (h) => `
    <path d="M-46,-552C-50,-606 -18,-624 4,-622C30,-621 53,-604 49,-552Q46,-570 41,-578L33,-574L25,-584L13,-577L1,-586L-11,-577L-23,-584L-33,-574L-41,-578Q-45,-566 -46,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-44,-556v16M48,-556v14" stroke="${h.c}" stroke-width="5" stroke-linecap="round"/>
    <g fill="${h.sh}" opacity=".5">${[[-30, -606], [-16, -612], [0, -614], [16, -612], [30, -604], [-22, -596], [-6, -600], [10, -600], [24, -594], [38, -590], [-36, -590]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.6"/>`).join("")}</g>
    <path d="M-30,-608Q2,-624 34,-606" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".4"/>`;
  const pulledBack = (h) => `
    <path d="M-47,-550C-51,-606 -16,-624 4,-624C30,-623 54,-604 49,-550Q46,-572 34,-586Q18,-594 4,-588Q-12,-596 -28,-588Q-42,-576 -47,-550Z" fill="${h.c}" ${ln()}/>
    <path d="M4,-622Q2,-606 4,-590M-12,-618Q-22,-600 -34,-584M18,-618Q30,-602 40,-584M-26,-610Q-36,-596 -42,-576M32,-612Q42,-598 46,-578" stroke="${h.s}" stroke-width="2.2" fill="none" opacity=".7"/>
    <path d="M-30,-610Q4,-626 36,-608" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".55"/>`;
  const bun = (h, pin) => `<circle cx="-30" cy="-622" r="23" fill="${dk(h.c, 0.06)}" ${ln()}/><path d="M-44,-630q12,-12 28,-4M-48,-618q16,-6 34,0" stroke="${h.s}" stroke-width="2.4" fill="none"/>
    ${pin ? `<path d="M-62,-640L4,-610" stroke="${pin}" stroke-width="4.5" stroke-linecap="round"/><circle cx="-62" cy="-640" r="5" fill="${pin}" ${ln(1.8)}/>` : ""}`;

  // ---------------- cast ----------------
  C.mint = { v2: {
    skin: "#efc6a0", iris: "#5a3424", lash: true,
    hair: { c: "#3d241b", s: "#24140e", sh: "#8a5a44", front: (x) => longFront(x.hair, x) + `<g transform="translate(47,-604)"><circle r="10" fill="#ec5e7e" ${ln(2.2)}/><path d="M-6,-3q6,6 12,0M-6,4q6,-4 12,0" stroke="#b83a5a" stroke-width="2" fill="none"/></g>`, back: (x) => longBack(x.hair) },
    top: { kind: "tee", c: "#c9b6ea", sleeve: "short" },
    print: `<path d="M-6,-426c-10,-14 -28,-2 -15,13l15,13l15,-13c13,-15 -5,-27 -15,-13z" fill="#ec5e7e" stroke="#b83a5a" stroke-width="2"/><path d="M-16,-420q2,-6 7,-6" stroke="#fff" stroke-width="2.4" fill="none" opacity=".6" stroke-linecap="round"/>`,
    bottom: { kind: "jeans", c: "#8fb5dc" }, feet: { kind: "sneaker", c: "#f6f4ee", mark: "#ec5e7e" },
  } };
  C.ton = { v2: {
    skin: "#c98e5e", iris: "#3a2416", blush: 0.6,
    hair: { c: "#1b1512", sh: "#5a4a40", front: (x) => buzz(x.hair) },
    top: { kind: "tank", c: "#d8443a", sleeve: "none" },
    bottom: { kind: "shorts", c: "#a8946a" }, feet: { kind: "boot", c: "#2f6a44" },
    // the woven shoulder bag (ย่าม) across the chest, the bag at his hip
    extra: `<path d="M-44,-478L40,-326" stroke="#2c5a7a" stroke-width="11" stroke-linecap="round"/><path d="M-44,-478L40,-326" stroke="#e8d8a8" stroke-width="3" stroke-dasharray="7 7"/>
      <g transform="translate(46,-318) rotate(-8)"><path d="M-26,-10H26L22,40Q0,48 -22,40Z" fill="#2c5a7a" ${ln()}/><path d="M-24,4H24M-23,18H23M-22,30H22" stroke="#e8d8a8" stroke-width="3" stroke-dasharray="6 5"/><path d="M-26,-10H26" stroke="#c84a3a" stroke-width="5"/></g>`,
    face: `<rect x="22" y="-534" width="16" height="8" rx="3" fill="#f0dcb8" stroke="${LINE}" stroke-width="1.6" transform="rotate(-16 30 -530)"/>`,
  } };
  C.yai = { v2: {
    skin: "#c99a74", iris: "#3e2a1e", blush: 0.4, lip: "#a8342a",
    hair: { c: "#c2bdb4", s: "#8f8a84", sh: "#f2eee6", front: (x) => pulledBack(x.hair), back: (x) => bun(x.hair, "#d8a83a") },
    top: { kind: "blouse", c: "#f2ece0", sleeve: "elbow", lace: true, trim: "#d8cfbd" },
    print: `<path d="M-22,-488q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0q4,6 8,0" stroke="#d8cfbd" stroke-width="2.4" fill="none"/>${[-430, -396, -362].map((y) => `<circle cx="2" cy="${y}" r="3" fill="#d8cfbd"/>`).join("")}`,
    bottom: { kind: "sarong", c: "#6a2f62", band: "#d8a83a", band2: "#a8342a" }, feet: { kind: "sandal", c: "#6a4a2a" },
    // the sash (ผ้าเบี่ยง) over one shoulder
    extra: `<path d="M-54,-482Q-10,-420 44,-304" stroke="#d8a83a" stroke-width="22" fill="none"/><path d="M-54,-482Q-10,-420 44,-304" stroke="#a8342a" stroke-width="4" stroke-dasharray="9 9" fill="none"/>
      <path d="M-54,-482Q-10,-420 44,-304" stroke="${LINE}" stroke-width="24" fill="none" opacity=".18"/>`,
    face: `<path d="M-22,-596q10,-3 20,0M-16,-588q8,-2 16,0M-34,-552l-7,-3M-34,-546l-7,1M38,-552l7,-3M38,-546l7,1M-14,-532q-7,10 -3,19M24,-532q7,10 3,19" stroke="#8a6448" stroke-width="2" fill="none" stroke-linecap="round" opacity=".8"/>`,
  } };
  C.thong = { v2: {
    skin: "#a87048", iris: "#2a1a12", blush: 0.25, bags: true, w: 0.9, limb: 0.88,
    hair: { c: "#8a8580", s: "#5a5650", sh: "#c8c4bc", front: (x) => `
      <path d="M-46,-560q-4,18 2,34M48,-560q4,18 -2,32" stroke="${x.hair.c}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M-44,-570Q0,-552 46,-570V-584H-44Z" fill="#000" opacity=".22"/>
      <path d="M-50,-582C-52,-628 -16,-644 2,-644C24,-644 56,-630 54,-582Z" fill="#c8a868" ${ln()}/>
      <path d="M-50,-582C-52,-628 -16,-644 2,-644C24,-644 56,-630 54,-582Z" fill="url(#r2Cyl)"/>
      <path d="M-40,-626L46,-600M-46,-604L50,-628M-30,-640L54,-590M-50,-590L30,-642" stroke="#9a7a42" stroke-width="2" opacity=".5"/>
      <path d="M-52,-596Q2,-586 56,-596" stroke="#7a5a30" stroke-width="8" fill="none"/>
      <path d="M-108,-576Q-62,-600 2,-598Q66,-600 112,-576Q66,-562 2,-564Q-62,-562 -108,-576Z" fill="#d6b878" ${ln()}/>
      <path d="M-96,-576Q2,-592 100,-576" stroke="#a8884a" stroke-width="2.4" fill="none" opacity=".7"/>
      <path d="M-70,-570L-60,-592M-36,-566L-30,-596M0,-565V-598M36,-566L30,-596M70,-570L60,-592" stroke="#a8884a" stroke-width="2" opacity=".55"/>` },
    top: { kind: "shirt", c: "#7c6c52", sleeve: "long", neck: "collar", collar: "#8a7a5e", button: "#d8ccb4" },
    print: `<path d="M-60,-318H60V-296H-60Z" fill="#c8342a" ${ln(2.2)}/><path d="M-50,-318v22M-30,-318v22M-10,-318v22M10,-318v22M30,-318v22M50,-318v22M-60,-307H60" stroke="#efe6d6" stroke-width="3" opacity=".8"/>`,
    bottom: { kind: "trousers", c: "#2c2c30" }, feet: { kind: "bare" },
    face: `<g fill="${dk("#a87048", 0.35)}" opacity=".5">${[[-24, -508], [-14, -503], [-4, -500], [8, -500], [18, -503], [28, -508], [-18, -512], [24, -512]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.5"/>`).join("")}</g>
      <path d="M-36,-530q4,14 14,20M42,-530q-4,14 -14,20" stroke="#7a4a2c" stroke-width="2" fill="none" opacity=".6"/>`,
  } };
  C.boon = { v2: {
    skin: "#b88058", iris: "#2e1e14", blush: 0.5,
    hair: { c: "#2a2420", front: (x) => `<path d="M-48,-552C-52,-604 -16,-622 4,-622C30,-621 54,-604 50,-552Q44,-574 4,-580Q-36,-574 -48,-552Z" fill="${x.hair.c}" ${ln()}/>
      <path d="M-54,-588C-50,-636 54,-640 56,-588Q30,-574 2,-576Q-28,-574 -54,-588Z" fill="#c8342a" ${ln()}/><path d="M-50,-600Q2,-614 54,-600M-44,-614Q2,-628 48,-614" stroke="#efe6d6" stroke-width="3" stroke-dasharray="6 6" fill="none" opacity=".8"/>
      <path d="M54,-596q20,4 22,22q-12,-2 -20,-10z" fill="#a82a22" ${ln(2.2)}/>` },
    top: { kind: "blouse", c: "#e88a3a", sleeve: "short" },
    bottom: { kind: "sarong", c: "#3a5a8a", band: "#e8d8a8", band2: "#2a3a5a" }, feet: { kind: "sandal", c: "#4a3a2a" },
  } };
  C.khem = { v2: {
    skin: "#a87048", iris: "#2a1a12", blush: 0.25, bags: true,
    hair: { c: "#8a8680", sh: "#c8c4bc", front: (x) => buzz(x.hair) },
    top: { kind: "singlet", c: "#efe9dc", sleeve: "none" },
    bottom: { kind: "trousers", c: "#4a6a4a" }, feet: { kind: "sandal", c: "#3a2a1e" },
    extra: `<path d="M-46,-486Q0,-440 46,-486" stroke="#8ab4d8" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M38,-484L44,-410" stroke="#8ab4d8" stroke-width="14" stroke-linecap="round"/>
      <path d="M38,-484L44,-410M-46,-486Q0,-440 46,-486" stroke="${LINE}" stroke-width="16" fill="none" opacity=".15"/><path d="M36,-420h16" stroke="#e8f0f6" stroke-width="3"/>`,
  } };
  C.doc = { v2: {
    skin: "#e2b28c", iris: "#3a2418", lash: true,
    hair: { c: "#1e1814", front: (x) => pulledBack(x.hair), back: (x) => bun(x.hair) },
    top: { kind: "coat", c: "#f6f6f2", sleeve: "long" },
    bottom: { kind: "trousers", c: "#4a9a8a" }, feet: { kind: "sneaker", c: "#f4f4f0" },
    print: `<path d="M-14,-470V-420M14,-470V-420" stroke="#4a9a8a" stroke-width="16"/><path d="M-30,-462Q-40,-384 0,-374Q40,-384 30,-462" stroke="#3a3a3a" stroke-width="4.5" fill="none"/><circle cx="0" cy="-372" r="8" fill="#9aa4a8" ${ln(2)}/>`,
    faceTop: `<g fill="none" stroke="#2a2a2a" stroke-width="3.4"><rect x="-30" y="-559" width="26" height="21" rx="6"/><rect x="6" y="-559" width="26" height="21" rx="6"/><path d="M-4,-550h10M-30,-552l-14,-4"/></g>
      <path d="M-26,-556l8,-1" stroke="#fff" stroke-width="2" opacity=".5"/>`,
  } };
})();
