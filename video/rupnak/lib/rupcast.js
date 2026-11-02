// "รูพญานาค" cast drawn with rig v2: a family back at ยาย's village on the Mekong for the rice harvest.
//   mook      มุก 16: a high ponytail with a side fringe, a cobalt zip jacket over a white tee, jeans, white sneakers · mookPhone (phone)
//   tonkao    ต้นข้าว 10 (draw at ~0.76): a buzz cut, a red football shirt with a white 9, black shorts, rubber sandals
//             · tonkaoPhone (phone held out to film) · tonkaoNote (a scrap of paper with numbers)
//   yaiKham   ยายคำ 72: grey hair in a bun with a small white flower, a white lace blouse, an indigo mudmee ผ้าซิ่น, sandals
//             · yaiKhamLeaf (her palm-leaf manuscript on its string)
//   phoSin    พ่อใหญ่สิน 76: a thin white fringe round a bald crown, white stubble, an indigo ม่อฮ่อม shirt, a checked ผ้าขาวม้า over
//             the shoulder, rolled black trousers, sandals · phoSinBar (a long iron well-driller's bar, his old trade)
(function () {
  const { LINE, dk, hi } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  // ---------------- มุก ----------------
  const mookFront = (h) => `
    <path d="M-50,-546C-60,-612 -20,-632 4,-630C36,-629 62,-606 53,-546C48,-566 40,-574 26,-578Q8,-584 -6,-600Q-22,-578 -40,-574Q-48,-562 -50,-546Z" fill="${h.c}" ${ln()}/>
    <path d="M-6,-600Q-16,-574 -40,-562Q-50,-556 -52,-536Q-44,-552 -30,-556Q-12,-566 -6,-600Z" fill="${dk(h.c, 0.25)}" opacity=".7"/>
    <path d="M-30,-614Q-38,-596 -36,-580M-6,-624Q-14,-606 -10,-592M22,-622Q14,-604 10,-596" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".7" stroke-linecap="round"/>
    <path d="M-28,-610Q-18,-620 -4,-623M8,-624Q20,-624 32,-616" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".3"/>
    <rect x="40" y="-616" width="16" height="12" rx="5" fill="#3a6ad8" ${ln(1.8)} transform="rotate(30 48 -610)"/>`;
  const mookBack = () => `
    <path d="M44,-612Q96,-618 104,-560Q110,-500 88,-454Q96,-506 80,-548Q70,-576 44,-588Z" fill="#20161a" ${ln()}/>
    <path d="M58,-600Q90,-590 92,-548M66,-590Q84,-560 82,-520" stroke="#0e080b" stroke-width="2.4" fill="none" opacity=".6"/>`;
  C.mook = { v2: { fingers: true,
    skin: "#e2b48c", iris: "#2e1c12", lash: true, blush: 0.55, lip: "#c45a5e", w: 1.04,
    hair: { c: "#20161a", s: "#0c070a", sh: "#6a5a62", front: (x) => mookFront(x.hair), back: () => mookBack() },
    top: { kind: "coat", c: "#2f5fc8", sleeve: "long", trim: "#f2f0ea" },
    bottom: { kind: "jeans", c: "#34405a" }, feet: { kind: "sneaker", c: "#f4f2ee" },
  } };

  // ---------------- ต้นข้าว ----------------
  const buzz = (h) => `
    <path d="M-48,-548C-54,-604 -24,-622 2,-622C30,-622 54,-604 49,-548Q44,-574 30,-584Q2,-594 -26,-584Q-42,-574 -48,-548Z" fill="${h.c}" ${ln()}/>
    <path d="M-36,-596Q2,-614 38,-596" stroke="${h.sh}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".35"/>
    ${Array.from({ length: 12 }, (_, k) => `<circle cx="${-34 + k * 6}" cy="${-604 + Math.abs(k - 6) * 1.8}" r="1.2" fill="${h.s}" opacity=".6"/>`).join("")}`;
  const nine = `<g transform="translate(0,-400)"><rect x="-40" y="-30" width="80" height="10" fill="#f4f2ee" opacity=".9"/><text x="0" y="28" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#f4f2ee" stroke="${LINE}" stroke-width="1.6">9</text></g>`;
  C.tonkao = { v2: { fingers: true,
    skin: "#c88c5c", iris: "#2a1a10", blush: 0.6, headScale: 1.2, w: 0.92, limb: 0.92,
    hair: { c: "#17110d", s: "#060404", sh: "#5a4a40", front: (x) => buzz(x.hair) },
    top: { kind: "tee", c: "#d8302a", sleeve: "elbow", trim: "#f4f2ee" },
    print: nine,
    bottom: { kind: "shorts", c: "#22242a" }, feet: { kind: "sandal", c: "#2a8ad8" },
  } };

  // ---------------- ยายคำ ----------------
  const yaiCap = (h) => `
    <path d="M-47,-550C-51,-606 -16,-624 4,-624C30,-623 54,-604 49,-550Q46,-572 34,-586Q18,-594 4,-588Q-12,-596 -28,-588Q-42,-576 -47,-550Z" fill="${h.c}" ${ln()}/>
    <path d="M4,-622Q2,-606 4,-590M-12,-618Q-22,-600 -34,-584M18,-618Q30,-602 40,-584" stroke="${h.s}" stroke-width="2.2" fill="none" opacity=".7"/>
    <path d="M-30,-610Q4,-626 36,-608" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5"/>`;
  // the bun sits at the back of the head (drawn behind it), a small white flower pinned in
  const yaiKnot = (h) => `<ellipse cx="34" cy="-612" rx="22" ry="20" fill="${dk(h.c, 0.06)}" ${ln()}/><path d="M18,-618q14,-10 30,-2M20,-604q14,6 28,0" stroke="${h.s}" stroke-width="2.2" fill="none"/>
    <g transform="translate(46,-628)"><circle r="6" fill="#fff" ${ln(1.4)}/>${[0, 72, 144, 216, 288].map((a) => `<ellipse cx="0" cy="-7" rx="3.4" ry="5" fill="#fff" ${ln(1)} transform="rotate(${a})"/>`).join("")}<circle r="2.6" fill="#f0c040"/></g>`;
  // the ผ้าซิ่น: indigo with white mudmee hooks, a red-and-gold ตีนซิ่น hem
  const sin = `<g><path d="M-57,-336Q-62,-250 -55,-150L-50,-38Q-26,-31 0,-34Q26,-31 50,-38L55,-150Q62,-250 57,-336Z" fill="#26346e" ${ln(2.6)}/>
    ${Array.from({ length: 5 }, (_, k) => `<path d="M-50,${-310 + k * 50}l8,-8l8,8l8,-8l8,8l8,-8l8,8l8,-8l8,8l8,-8l8,8l8,-8l8,8" stroke="#e8e2d0" stroke-width="2.6" fill="none" opacity=".8"/>`).join("")}
    ${Array.from({ length: 4 }, (_, k) => `<path d="M${-36 + k * 24},${-286 + (k % 2) * 50}m-6,0a6,6 0 1 0 12,0a6,6 0 1 0 -12,0" fill="none" stroke="#e8e2d0" stroke-width="2"/>`).join("")}
    <path d="M-52,-70Q0,-62 52,-70L50,-38Q0,-30 -50,-38Z" fill="#b8302a" ${ln(2)}/><path d="M-51,-62Q0,-54 51,-62" stroke="#f0c040" stroke-width="4" fill="none"/>
    <path d="M14,-336L22,-36" stroke="${LINE}" stroke-width="2" opacity=".6"/></g>`;
  C.yaiKham = { v2: { fingers: true,
    skin: "#b88058", iris: "#2a1a12", blush: 0.25, bags: true, w: 0.98, limb: 0.94, brow: "#d8d4cc", lip: "#9a4a3a",
    hair: { c: "#d8d4cc", s: "#9a968e", sh: "#ffffff", front: (x) => yaiCap(x.hair), back: (x) => yaiKnot(x.hair) },
    top: { kind: "blouse", c: "#f6f2ea", sleeve: "elbow", lace: true, trim: "#d8d0c0" },
    bottom: { kind: "sarong", c: "#26346e", band: "#b8302a", band2: "#f0c040" }, feet: { kind: "sandal", c: "#6a4a32" },
    skirt: sin,
  } };

  // ---------------- พ่อใหญ่สิน ----------------
  const fringe = (h) => `
    <path d="M-52,-560C-56,-590 -46,-600 -38,-602Q-46,-582 -44,-552Z" fill="${h.c}" ${ln()}/><path d="M52,-560C56,-590 46,-600 38,-602Q46,-582 44,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-616Q4,-628 34,-614" stroke="#e8c8a0" stroke-width="5" fill="none" stroke-linecap="round" opacity=".35"/>`;
  const stubble = `<g opacity=".55">${Array.from({ length: 26 }, (_, k) => `<circle cx="${-30 + (k % 13) * 5}" cy="${-466 + Math.floor(k / 13) * 7 + (k % 2) * 2}" r="1.2" fill="#e8e4dc"/>`).join("")}</g>`;
  const pakama = `<path d="M-40,-452Q0,-430 40,-452L30,-330Q0,-318 -30,-330Z" fill="none"/><path d="M-44,-454L46,-388" stroke="#c84a3a" stroke-width="20" stroke-linecap="round"/>
    <path d="M-44,-454L46,-388" stroke="#f0e0c8" stroke-width="20" stroke-dasharray="6 6"/><path d="M-36,-460L52,-394" stroke="${LINE}" stroke-width="1.6" fill="none" opacity=".6"/>`;
  C.phoSin = { v2: { fingers: true,
    skin: "#8e5e3c", iris: "#2a1a12", blush: 0.1, bags: true, w: 0.94, limb: 0.9, brow: "#ece8de",
    hair: { c: "#ece8de", s: "#a8a49c", sh: "#ffffff", front: (x) => fringe(x.hair) },
    top: { kind: "coat", c: "#24305a", sleeve: "long", trim: "#1a2244" },
    bottom: { kind: "shorts", c: "#1e1e22" }, feet: { kind: "sandal", c: "#4a3424" },
    extra: pakama, face: stubble,
  } };

  // ---------------- ผู้ใหญ่ทอง: the headman, comic, sells incense by the hole: khaki-ish shirt with pockets, a cap, a whistle on a cord ----------------
  const cap = (h) => `<path d="M-50,-560C-54,-616 -20,-632 4,-632C32,-632 56,-614 50,-560Q40,-584 4,-590Q-34,-586 -50,-560Z" fill="${h.c}" ${ln()}/>
    <path d="M-56,-590Q2,-650 58,-592L64,-576Q2,-604 -60,-574Z" fill="#c8a040" ${ln()}/><path d="M40,-584Q90,-580 104,-566Q70,-562 44,-570Z" fill="#a88030" ${ln()}/>`;
  C.thong = { v2: { fingers: true,
    skin: "#a8724a", iris: "#2a1a12", blush: 0.2, bags: true, w: 1.12, limb: 1.0, brow: "#2a1a12",
    hair: { c: "#2a2420", s: "#100c0a", sh: "#6a5a50", front: (x) => cap(x.hair) },
    top: { kind: "shirt", c: "#b8a070", sleeve: "short", trim: "#8a7448" },
    bottom: { kind: "jeans", c: "#3a3a40" }, feet: { kind: "sandal", c: "#3a2a1a" },
    face: `<path d="M-22,-470q22,10 44,0" stroke="#2a1a12" stroke-width="5" fill="none" stroke-linecap="round"/>`,
    extra: `<path d="M-20,-452Q0,-400 18,-452" stroke="#e8302a" stroke-width="3" fill="none"/><rect x="-6" y="-410" width="12" height="20" rx="3" fill="#d8d4c8" ${ln(1.6)}/>
      <rect x="10" y="-420" width="30" height="34" fill="#a8905e" ${ln(1.8)}/><rect x="-40" y="-420" width="30" height="34" fill="#a8905e" ${ln(1.8)}/>`,
  } };

  // ---------------- poses with weight, elbows and talking hands ----------------
  const M = Rig.MODES, Z = () => M.idle(0, {});
  M.talk = (u, o) => { const s = Math.sin(u * 2.3), s2 = Math.sin(u * 4.7 + 1), w = Math.sin(u * 0.9);
    return { ...M.idle(u, o), uaF: -34 + 9 * s, faF: -78 + 16 * s2, uaB: 10 + 3 * w, faB: -26, torso: 1.5 * w, head: 3 * s - 2, thF: 6 + 3 * w, shF: 6, thB: -4 - 2 * w, shB: 3, rootR: 1.2 * w }; };
  M.talk2 = (u, o) => { const s = Math.sin(u * 2.1 + 2), s2 = Math.sin(u * 5.1);
    return { ...M.idle(u, o), uaF: -58 + 10 * s, faF: -54 + 18 * s2, uaB: -40 - 8 * s, faB: -62 + 10 * s2, torso: 2, head: -3 + 3 * s, thF: 10, shF: 8, thB: -6 }; };
  M.leanFilm = (u, o) => { const j = Math.sin(u * 1.4);
    return { ...Z(), thF: -46, shF: 74, thB: -14, shB: 46, torso: 46 + 2 * j, head: 34, uaF: -74 + 3 * j, faF: -34, uaB: 34 + 4 * j, faB: -36, bodyY: 66 }; };
  M.wai = (u, o) => { const b = Math.sin(u * 1.6);
    return { ...Z(), uaF: -38, faF: -122 + 2 * b, uaB: -36, faB: -120 + 2 * b, torso: 8 + b, head: 10, thF: 4, thB: -4, bodyY: 2 }; };
  M.stopArm = (u, o) => { const b = Math.sin(u * 3.1);
    return { ...Z(), uaF: -84 + 3 * b, faF: -16, uaB: -14, faB: -64, torso: -5, head: -6, thF: 12, shF: 6, thB: -10, shB: 4, rootR: -1.5 }; };
  M.kneelWai = (u, o) => { const b = Math.sin(u * 1.4); return { ...M.crouch(u, o), uaF: -38, faF: -122 + 2 * b, uaB: -36, faB: -120 + 2 * b, torso: 14 + b, head: 12 }; };
  M.handsHip = (u, o) => { const b = Math.sin(u * 1.2);
    return { ...M.idle(u, o), uaF: -30, faF: 100, uaB: 30, faB: -100, torso: -2 + b, head: 2 * b, thF: 6, thB: -6 }; };
})();
