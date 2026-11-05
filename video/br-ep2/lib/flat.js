// Flat look (lane A experiment, "สูตรทดลอง"): the cast redrawn in the reference series' line style, on the same skeleton,
// joints and ids as rig.js / rig2.js, so every pose mode, track and shot keeps working.
//   no outlines anywhere · a small round head, dot eyes with a catch-light, short brows, a tiny mouth · long thin stick limbs
//   with round hands · flat clothes with one shade panel on the far side · far-side limbs a shade darker · muted colours.
// Per-character hooks (SPEC): faces(x, browC, faces) → { eyes, mouths } · headTop(x) → svg over the face · V.top.pat → a printed top.
// Rig.FLAT = true switches Rig.build (every v2 cast entry) and Rig.buildCat to these builders. Load after every cast file.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const { mix, dk, hi } = Rig2;
  const f = (v) => (+v).toFixed(1);
  const INK = "#211714";
  const mute = (c, k = 0.14) => mix(c, "#8c8782", k); // take the edge off saturated cast colours
  const shd = (c, k = 0.15) => mix(dk(c, k), "#283050", 0.1); // the shade panel: darker, a touch cooler
  const far = (c) => mix(dk(c, 0.13), "#283050", 0.06); // far-side limbs

  Sets.DEFS += `
    <pattern id="flCheckRB" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#4a78a8"/><path d="M0,4h16M0,12h16" stroke="#c8483e" stroke-width="3" opacity=".85"/><path d="M4,0v16M12,0v16" stroke="#efe4d0" stroke-width="2" opacity=".55"/></pattern>
    <pattern id="flCheckGY" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#3a7a5a"/><path d="M0,4h16M0,12h16" stroke="#d8c050" stroke-width="3" opacity=".85"/><path d="M4,0v16M12,0v16" stroke="#efe4d0" stroke-width="2" opacity=".45"/></pattern>
    <pattern id="flCheckRW" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#efe6d8"/><path d="M0,3.5h14M0,10.5h14M3.5,0v14M10.5,0v14" stroke="#c8403a" stroke-width="3" opacity=".85"/></pattern>
    <linearGradient id="flV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient>
    <linearGradient id="flLimb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>
    <radialGradient id="flFace" cx=".36" cy=".3" r=".78"><stop offset="0" stop-color="#fff" stop-opacity=".17"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".15"/></radialGradient>
    <filter id="flSoft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3"/></filter>`;

  // rounded bar from (0,0) down to (0,len), w wide: the round ends hide every joint (there are no outlines to give a seam away)
  const bar = (len, w, fill) => `<rect x="${f(-w / 2)}" y="${f(-w / 2)}" width="${f(w)}" height="${f(len + w)}" rx="${f(w / 2)}" fill="${fill}"/><rect x="${f(-w / 2)}" y="${f(-w / 2)}" width="${f(w)}" height="${f(len + w)}" rx="${f(w / 2)}" fill="url(#flLimb)"/>`;

  // ---------------- hair (front: over the head, under the ear · back: behind the torso, follows the head) ----------------
  // head: ellipse centre (2,-546), rx 42, ry 45 · the face looks a little to +x (three-quarter view)
  const HAIR = {
    short: (c) => `<path d="M-41,-536C-46,-582 -18,-598 4,-598C30,-598 48,-584 46,-560Q38,-576 24,-578Q6,-572 -12,-578Q-24,-572 -28,-556Q-30,-546 -32,-534Z" fill="${c}"/>`,
    undercut: (c, x) => `<path d="M-41,-534C-44,-560 -40,-578 -30,-586L-26,-560Q-28,-546 -32,-532Z" fill="${mix(x.skin, c, 0.55)}"/>
      <path d="M-34,-566C-42,-600 -14,-614 10,-612C36,-610 54,-594 46,-566Q40,-582 28,-584Q14,-580 2,-586Q-12,-578 -22,-584Q-30,-578 -34,-566Z" fill="${c}"/>
      <path d="M-4,-606Q22,-614 40,-598" stroke="${hi(c, 0.22)}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".5"/>`,
    bowl: (c) => `<path d="M-42,-534C-48,-586 -16,-602 4,-602C34,-602 52,-588 47,-560Q24,-568 2,-566Q-18,-566 -28,-560Q-32,-550 -32,-534Z" fill="${c}"/>`,
    buzz: (c) => `<path d="M-41,-540C-44,-584 -16,-596 4,-596C30,-596 48,-584 45,-562Q30,-574 6,-574Q-16,-574 -28,-560Q-32,-552 -33,-540Z" fill="${c}"/>`,
    pony: (c) => `<path d="M-42,-532C-48,-586 -16,-600 4,-600C32,-600 52,-586 47,-556Q42,-566 34,-570Q20,-562 8,-570Q-4,-562 -14,-572Q-24,-566 -30,-552Q-32,-542 -33,-530Z" fill="${c}"/>`,
    ponyB: (c) => `<path d="M-26,-592C-60,-596 -76,-566 -72,-526C-70,-494 -78,-468 -88,-450Q-62,-454 -58,-490C-54,-522 -54,-556 -30,-580Z" fill="${c}"/>`,
    bob: (c) => `<path d="M-46,-508C-54,-560 -40,-602 4,-602C46,-602 56,-566 52,-512Q46,-504 40,-512L40,-562Q14,-570 -12,-566Q-26,-564 -32,-556L-32,-508Q-40,-500 -46,-508Z" fill="${c}"/>`,
    long: (c) => `<path d="M-44,-520C-50,-584 -16,-600 4,-600C34,-600 52,-586 48,-556Q40,-568 28,-570Q10,-564 -6,-570Q-20,-562 -30,-548L-32,-516Z" fill="${c}"/>`,
    longB: (c, x) => `<path d="M-50,-560C-60,-510 -62,-450 -56,-410Q-28,-398 0,-404Q30,-398 52,-412Q56,-470 50,-560Z" fill="${dk(c, 0.08)}"/>
      ${x.ends ? `<path d="M-58,-446Q-60,-424 -56,-410Q-28,-398 0,-404Q30,-398 52,-412Q55,-430 54,-446Q28,-436 0,-440Q-30,-436 -58,-446Z" fill="${x.ends}"/>` : ""}`,
    bun: (c) => `<path d="M-42,-534C-48,-586 -16,-598 4,-598C32,-598 50,-584 46,-558Q30,-572 8,-572Q-14,-572 -26,-560Q-32,-550 -33,-534Z" fill="${c}"/><circle cx="-28" cy="-596" r="17" fill="${dk(c, 0.06)}"/>`,
    perm: (c) => `<g fill="${c}"><path d="M-42,-530C-48,-584 -16,-598 4,-598C32,-598 50,-584 47,-560Q30,-570 6,-570Q-18,-570 -30,-556L-33,-530Z"/>
      ${[[-36, -572], [-24, -592], [-6, -602], [14, -602], [32, -592], [44, -574], [-42, -548]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="15"/>`).join("")}</g>`,
    side: (c) => `<path d="M-41,-536C-46,-584 -18,-600 6,-600C32,-600 50,-586 46,-560Q42,-570 34,-572Q20,-582 -2,-584Q-18,-578 -26,-560Q-30,-548 -32,-534Z" fill="${c}"/>`,
    horseshoe: (c) => `<path d="M-42,-528C-46,-552 -42,-570 -34,-580Q-28,-558 -30,-528Z" fill="${c}"/><path d="M38,-562Q44,-572 44,-560L46,-548Q40,-552 38,-562Z" fill="${c}"/>`,
    guardCap: (c, x) => `<path d="M-41,-534Q-44,-556 -40,-566L-28,-562Q-30,-546 -32,-534Z" fill="${x.hairC}"/>
      <path d="M-42,-562C-44,-600 -12,-610 6,-610C34,-610 50,-598 47,-562Z" fill="${c}"/>
      <rect x="-43" y="-570" width="91" height="10" fill="${dk(c, 0.25)}"/>
      <path d="M14,-562Q52,-568 74,-552Q52,-546 14,-552Z" fill="${dk(c, 0.35)}"/>
      <path d="M2,-598l6,-8l6,8l-6,10z" fill="#d8b84a"/>`,
    helmet: (c, x) => `<path d="M-50,-546C-52,-604 -16,-616 6,-616C40,-616 60,-596 58,-546L56,-506Q52,-490 34,-488H-26Q-46,-492 -48,-508Z" fill="${c}"/>
      <path d="M-44,-592Q4,-626 52,-592" stroke="${x.stripe || "#2fa45a"}" stroke-width="11" fill="none" stroke-linecap="round"/>
      <rect x="-14" y="-574" width="66" height="38" rx="16" fill="#151a1f"/><path d="M-2,-566Q20,-574 42,-566" stroke="#fff" stroke-width="3" fill="none" opacity=".25" stroke-linecap="round"/>`,
  };

  // ---------------- per-character flat specs (identity kept through hair, colours and one or two signature details) ----------------
  const chain = `<path d="M-15,-490Q0,-462 15,-490" stroke="#d8c890" stroke-width="2.4" fill="none"/><rect x="-4" y="-470" width="8" height="10" rx="2" fill="#d8b84a"/>`;
  const sash = (pat) => `<path d="M-46,-484L-28,-492L46,-336L44,-300L30,-300Z" fill="url(#${pat})"/>`;
  const SPEC = {
    keng: { hair: "undercut", acc: () => chain },
    kengDay: { hair: "undercut", acc: () => chain + sash("flCheckRB") },
    fon: { hair: "pony", tie: "#c8343c", glasses: "round",
      print: () => `<circle cx="10" cy="-420" r="15" fill="#f2e6cc"/><path d="M7.5,-429h5v6.5h6.5v5h-6.5v6.5h-5v-6.5h-6.5v-5h6.5z" fill="#c8343c"/>` },
    boss: { hair: "bowl", print: (x) => `<path d="M-16,-404q4,-17 21,-14q13,3 9,16l7,4h-11l-3,7h-8l2,-7h-17z" fill="${dk(x.top, 0.25)}"/>` },
    prae: { hair: "pony", tie: "#2a1a14", print: (x) => `<path d="M-30,-494Q0,-468 30,-494L38,-478Q0,-448 -38,-478Z" fill="${dk(x.top, 0.14)}"/><path d="M-8,-470v34M8,-470v30" stroke="#efe6d6" stroke-width="2.6" stroke-linecap="round"/>` },
    piak: { hair: "short", acc: () => sash("flCheckGY") },
    somsak: { hair: "guardCap", hatC: "#26324e", tache: "#c8c4bc",
      print: () => `<path d="M-46,-482L-24,-488V-476L-46,-470ZM46,-482L24,-488V-476L46,-470Z" fill="#26324e"/><path d="M20,-450l6,-6l6,6v8l-6,4l-6,-4z" fill="#d8b84a"/>
        <rect x="-36" y="-452" width="14" height="24" rx="3" fill="#2a2a2e"/><path d="M-29,-452v-12" stroke="#2a2a2e" stroke-width="3"/>` },
    june: { hair: "long", hairB: "longB", ends: "#d87aa8", print: () => `<circle cx="6" cy="-424" r="11" fill="#f2c55c"/><path d="M-12,-410q9,-8 18,0t18,0" stroke="#6e94c9" stroke-width="5" fill="none" stroke-linecap="round"/>` },
    yaiBua: { hair: "bun", acc: () => sash("flCheckRB") },
    bua: { hair: "perm",
      acc: () => `<path d="M-45,-462Q-45,-490 -24,-490L-12,-430V-296H-46ZM45,-462Q45,-490 24,-490L12,-430V-296H46Z" fill="#2c62a8"/><rect x="-40" y="-414" width="22" height="13" rx="3" fill="#efe8da"/>` },
    docm: { hair: "side", glasses: "rect",
      print: () => `<path d="M-14,-490L0,-462L14,-490V-236H-14Z" fill="#9ab4cc"/><path d="M-26,-470Q-34,-392 0,-384Q34,-392 26,-470" stroke="#3a3a3a" stroke-width="4" fill="none"/><circle cx="0" cy="-382" r="7" fill="#9aa4a8"/>` },
    mew: { hair: "bob", clip: "#f2c230", noEar: true,
      print: (x) => `<g transform="translate(6,-418)"><path d="M-14,-6L-12,-18L-4,-10H4L12,-18L14,-6Q14,10 0,10Q-14,10 -14,-6Z" fill="${dk(x.top, 0.35)}"/><circle cx="-5" cy="-3" r="2" fill="#f2e6cc"/><circle cx="5" cy="-3" r="2" fill="#f2e6cc"/></g>`,
      acc: () => `<path d="M-16,-490Q0,-450 16,-490" stroke="#2a64b0" stroke-width="2.6" fill="none"/><rect x="-6" y="-458" width="13" height="20" rx="5" fill="#e8702a"/>` },
    phum: { hair: "buzz" },
    rider: { hair: "helmet", hatC: "#2b3036", noEar: true,
      print: () => `<rect x="-45" y="-410" width="90" height="9" fill="#d8e0e0" opacity=".85"/><rect x="-45" y="-350" width="90" height="9" fill="#d8e0e0" opacity=".85"/>`,
      sleeve: `<rect x="-11" y="54" width="22" height="8" fill="#d8e0e0" opacity=".85"/>` },
    samarn: { hair: "horseshoe", tache: "#c8c4bc", glassesUp: true,
      print: () => `<rect x="-36" y="-446" width="22" height="20" rx="2" fill="#9a8458"/><circle cx="26" cy="-440" r="8" fill="#d8b84a"/>` },
  };
  const nameOf = (P) => Object.keys(Rig.CAST).find((k) => Rig.CAST[k] === P) || "";
  const specFor = (n) => SPEC[n] || SPEC[n.replace(/[A-Z][a-z]*$/, "")] || {};

  // ---------------- face ----------------
  const EX = [-8, 21], EY = -549;
  function faces(browC) {
    const dot = (x, y, rx = 4.8, ry = 6.2) => `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${rx}" ry="${ry}" fill="${INK}"/><circle cx="${f(x + 1.6)}" cy="${f(y - 2.3)}" r="1.5" fill="#fff" opacity=".9"/>`;
    const brows = (dy = 0, tilt = 0) => EX.map((x, i) => {
      const inner = x + (i ? -7 : 7), outer = x + (i ? 7 : -7);
      return `<path d="M${outer},${EY - 15 + dy}L${inner},${EY - 15 + dy + tilt}" stroke="${browC}" stroke-width="4.2" stroke-linecap="round"/>`;
    }).join("");
    const dots = (dx = 0, rx, ry) => EX.map((x) => dot(x + dx, EY, rx, ry)).join("");
    return {
      eyes: {
        normal: dots() + brows(),
        side: dots(4) + brows(1),
        wide: EX.map((x) => `<circle cx="${x}" cy="${EY}" r="7" fill="${INK}"/><circle cx="${x + 2}" cy="${EY - 2.6}" r="2.2" fill="#fff"/>`).join("") + brows(-7, -1),
        closed: EX.map((x) => `<path d="M${x - 6},${EY}q6,5 12,0" stroke="${INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`).join("") + brows(2),
        pain: EX.map((x, i) => { const s = i ? -1 : 1; return `<path d="M${x - 6 * s},${EY - 5}L${x + 5 * s},${EY}L${x - 6 * s},${EY + 5}" stroke="${INK}" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`; }).join("") + brows(3, -5),
        worry: dots() + brows(-3, -6),
        angry: dots(0, 4.8, 5.4) + brows(3, 6),
        glow: EX.map((x) => `<circle cx="${x}" cy="${EY}" r="16" fill="#c8ff9a" opacity=".3"/><circle cx="${x}" cy="${EY}" r="7" fill="#e9ffc0"/>`).join("") + brows(3, 6),
        dead: EX.map((x) => `<circle cx="${x}" cy="${EY}" r="7" fill="#e6e8dc"/>`).join("") + brows(3, 4),
        happy: EX.map((x) => `<path d="M${x - 7},${EY + 2}q7,-9 14,0" stroke="${INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>`).join("") + brows(-2),
        sad: dots() + brows(-2, 7),
        squint: EX.map((x) => `<ellipse cx="${x}" cy="${EY}" rx="5.2" ry="3" fill="${INK}"/>`).join("") + brows(1, 3),
      },
      mouths: {
        smile: `<path d="M3,-523q6,5 12,0" stroke="${INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`,
        flat: `<path d="M4,-521h10" stroke="${INK}" stroke-width="3.2" stroke-linecap="round"/>`,
        o: `<ellipse cx="9" cy="-520" rx="4.6" ry="6" fill="${INK}"/>`,
        frown: `<path d="M3,-517q6,-5 12,0" stroke="${INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`,
        scream: `<ellipse cx="9" cy="-517" rx="8" ry="11" fill="${INK}"/><path d="M4,-510q5,-4 10,0q-5,3 -10,0z" fill="#b8605a"/>`,
        snarl: `<path d="M-4,-526H22L19,-510Q9,-504 -1,-510Z" fill="${INK}"/><path d="M-1,-525l2.5,5l2.5,-5l2.5,5l2.5,-5l2.5,5l2.5,-5l2.5,5l2.5,-5" stroke="#efe6d6" stroke-width="2" fill="none"/>`,
        laugh: `<path d="M1,-525h16q0,14 -8,14q-8,0 -8,-14z" fill="${INK}"/>`,
        smirk: `<path d="M2,-521q7,2 13,-5" stroke="${INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`,
        grin: `<path d="M-1,-526h20q-2,12 -10,12q-8,0 -10,-12z" fill="${INK}"/><path d="M1,-524h16v4h-16z" fill="#f4ecd8"/>`,
        pout: `<ellipse cx="9" cy="-520" rx="3.2" ry="2.4" fill="${INK}"/>`,
        grit: `<path d="M0,-524h18v8h-18z" fill="${INK}"/><path d="M3,-524v8M7.5,-524v8M12,-524v8M15,-524v8" stroke="#f4ecd8" stroke-width="1.6"/>`,
      },
    };
  }

  function buildFlat(parent, id, P, name) {
    const V = P.v2, S = specFor(name), w = V.w || 1, k = V.limb || 1;
    const skin = mute(V.skin, 0.06), skinS = shd(skin, 0.13), skinB = far(skin);
    const tp = V.top || { kind: "tee", c: "#888" }, top = mute(tp.c), topS = shd(top), topB = far(top);
    const bt = V.bottom || { kind: "trousers", c: "#3a3a3a" }, pc = mute(bt.c), pcB = far(pc);
    const hairC = V.hair ? V.hair.c : "#1a1410";
    const ft = V.feet || { kind: "bare" };
    const hs = S.headScale ?? (V.headScale ? V.headScale * 1.06 : 1);
    const x = { skin, skinS, top, topS, hairC, ends: S.ends, stripe: S.stripe };
    const X = (v) => f(v * w);

    // ---- legs ----
    const leg = (side) => {
      const B = side === "B", c = B ? pcB : pc, sk = B ? skinB : skin;
      const tw = 27 * k, sw = 24 * k;
      let thigh, shin;
      if (bt.kind === "shorts") {
        thigh = bar(150, tw - 3, sk) + `<rect x="${f(-tw / 2 - 2)}" y="-16" width="${f(tw + 4)}" height="88" rx="7" fill="${c}"/>`;
        shin = bar(134, sw - 2, sk);
      } else if (bt.kind === "sarong") {
        thigh = bar(150, tw + 12, c);
        shin = bar(130, sw + 12, c) + `<rect x="${f(-(sw + 12) / 2)}" y="100" width="${f(sw + 12)}" height="8" fill="${mute(bt.band || "#c8963a")}"/>`;
      } else {
        thigh = bar(150, tw, c);
        shin = bar(132, sw, c) + (bt.kind === "jeans" ? `<rect x="${f(-sw / 2)}" y="118" width="${f(sw)}" height="10" fill="${hi(c, 0.18)}"/>` : "");
      }
      let foot;
      const fc = (c0) => (B ? far(mute(c0)) : mute(c0));
      if (ft.kind === "sneaker") foot = `<path d="M-13,124Q-14,114 -4,114H8Q16,116 20,124Q34,127 35,138V144H-14Z" fill="${fc(ft.c || "#f2f0ea")}"/><rect x="-14" y="140" width="49" height="6" rx="2" fill="${fc(ft.sole || "#d8d2c4")}"/>`;
      else if (ft.kind === "boot") foot = `<path d="M-14,96H13V122Q33,125 35,138V147H-14Z" fill="${fc(ft.c)}"/>`;
      else {
        foot = `<path d="M-11,122Q-12,113 -3,113H6Q12,117 16,125Q30,128 31,137Q31,142 25,142H-12Z" fill="${sk}"/>`;
        if (ft.kind === "sandal") foot += `<rect x="-13" y="141" width="45" height="6" rx="2" fill="${fc(ft.c || "#3a2a20")}"/>`;
      }
      return `<g id="${id}-th${side}">${thigh}<g transform="translate(0,150)"><g id="${id}-sh${side}">${shin}${foot}</g></g></g>`;
    };

    // ---- arms ----
    const torch = `<g id="${id}-torch" display="none" transform="translate(0,112)"><rect x="-7" y="-4" width="14" height="36" rx="3" fill="#3d3833"/><path id="${id}-beam" d="M-8,30L-230,900H230L8,30Z" fill="url(#beamg)"/></g>`;
    const arm = (side, extra = "") => {
      const B = side === "B", tc = B ? topB : top, sk = B ? skinB : skin, sl = tp.sleeve || "short";
      const tcF = tp.pat ? `url(#${tp.pat})` : tc, dim = (h) => (tp.pat && B ? h.replace(/fill="[^"]*"/, 'fill="#1c2030" opacity=".3"') : "");
      const uw = 18 * k, fw = 16 * k;
      let upper, fore;
      if (sl === "none") upper = bar(122, uw, sk);
      else if (sl === "short") { const r = `<rect x="${f(-uw / 2 - 5)}" y="${f(-uw / 2 - 6)}" width="${f(uw + 10)}" height="58" rx="${f(uw / 2 + 3)}" fill="${tcF}"/>`; upper = bar(122, uw, sk) + r + dim(r); }
      else { const r = bar(122, uw + 3, tcF); upper = r + dim(r); }
      if (sl === "elbow") upper += `<rect x="${f(-uw / 2 - 4)}" y="104" width="${f(uw + 8)}" height="12" rx="5" fill="${dk(tc, 0.1)}"/>`;
      if (S.sleeve && sl !== "none") upper += S.sleeve;
      if (sl === "long") fore = bar(98, fw + 3, tcF) + dim(bar(98, fw + 3, tcF)) + `<rect x="${f(-fw / 2 - 3)}" y="88" width="${f(fw + 6)}" height="12" rx="4" fill="${dk(tc, 0.12)}"/>`;
      else fore = bar(104, fw, sk);
      const hand = `<circle cx="0" cy="112" r="${f(10.5 * k)}" fill="${sk}"/>`;
      return `<g id="${id}-ua${side}">${upper}<g transform="translate(0,122)"><g id="${id}-fa${side}">${fore}${hand}<g id="${id}-hand${side}">${side === "F" ? torch : ""}${extra}</g></g></g></g>`;
    };

    // ---- torso: a plain slab with rounded shoulders, one shade panel on the far side ----
    const coat = tp.kind === "coat", bottomY = coat ? -236 : -296;
    const slab = `M${X(-44)},-462Q${X(-44)},-490 ${X(-20)},-490H${X(20)}Q${X(44)},-490 ${X(44)},-462L${X(45)},${bottomY}H${X(-45)}Z`;
    const panel = `M${X(-44)},-462Q${X(-44)},-490 ${X(-20)},-490H${X(-14)}Q${X(-22)},-474 ${X(-23)},-452L${X(-22)},${bottomY}H${X(-45)}Z`;
    let torso = "";
    if (tp.kind === "tank" || tp.kind === "singlet") {
      torso += `<path d="${slab}" fill="${skin}"/><path d="${panel}" fill="${skinS}" opacity=".7"/>`;
      const tank = `M${X(-30)},-490H${X(-20)}Q0,-464 ${X(20)},-490H${X(30)}Q${X(32)},-458 ${X(44)},-446L${X(45)},-296H${X(-45)}L${X(-44)},-446Q${X(-32)},-458 ${X(-30)},-490Z`;
      torso += `<path d="${tank}" fill="${top}"/><path d="M${X(-44)},-446Q${X(-32)},-458 ${X(-30)},-490H${X(-22)}Q${X(-24)},-470 ${X(-23)},-446L${X(-22)},-296H${X(-45)}Z" fill="${topS}" opacity=".8"/>`;
    } else {
      torso += tp.pat ? `<path d="${slab}" fill="url(#${tp.pat})"/><path d="${panel}" fill="#1c2030" opacity=".3"/>` : `<path d="${slab}" fill="${top}"/><path d="${panel}" fill="${topS}"/>`;
      if (tp.neck === "collar") torso += `<path d="M${X(-20)},-492L0,-466L${X(20)},-492L${X(10)},-498L0,-484L${X(-10)},-498Z" fill="${hi(top, 0.18)}"/>` +
        [-440, -404, -368, -332].map((y) => `<circle cx="3" cy="${y}" r="3" fill="${hi(top, 0.35)}"/>`).join("");
      else if (!coat) torso += `<path d="M${X(-17)},-490Q0,-474 ${X(17)},-490Z" fill="${skinS}"/>`;
      if (coat) torso += `<path d="M${X(-20)},-490L-3,-430V${bottomY}H3V-430L${X(20)},-490" fill="none" stroke="${topS}" stroke-width="3"/>`;
    }
    torso += `<path d="${slab}" fill="url(#flV)"/><ellipse cx="0" cy="-484" rx="27" ry="9" fill="#000" opacity=".16" filter="url(#flSoft)"/>`;
    torso += S.print ? S.print(x) : "";
    const pelvis = `<rect x="${f(-40 * k)}" y="-324" width="${f(80 * k)}" height="36" rx="8" fill="${pc}"/><rect x="${f(-40 * k)}" y="-324" width="${f(80 * k)}" height="36" rx="8" fill="url(#flV)"/>`;

    // ---- head ----
    const browC = dk(hairC === "#a8a49c" ? "#6a665e" : hairC, 0.05);
    const { eyes, mouths } = S.faces ? S.faces(x, browC, faces) : faces(browC);
    const eyeG = Object.entries(eyes).map(([n, v]) => `<g class="eye-${n}" display="${n === "normal" ? "inline" : "none"}">${v}</g>`).join("");
    const mouthG = Object.entries(mouths).map(([n, v]) => `<g class="mouth-${n}" display="${n === "smile" ? "inline" : "none"}">${v}</g>`).join("");
    const hk = S.hair || "short", hc = S.hatC || mute(hairC, 0.05);
    const hairF = (HAIR[hk] || HAIR.short)(hc, x);
    const hairBk = S.hairB ? HAIR[S.hairB](mute(hairC, 0.05), x) : hk === "pony" ? HAIR.ponyB(mute(hairC, 0.05)) : "";
    const tie = S.tie && hk === "pony" ? `<ellipse cx="-34" cy="-588" rx="8" ry="11" fill="${S.tie}" transform="rotate(-30 -34 -588)"/>` : "";
    const ear = S.noEar ? "" : `<ellipse cx="-33" cy="-540" rx="7.5" ry="10" fill="${skin}"/><ellipse cx="-33" cy="-539" rx="3.6" ry="5.6" fill="${skinS}"/>`;
    let faceTop = "";
    if (S.glasses === "round") faceTop += `<g fill="none" stroke="#2a2220" stroke-width="2.6">${EX.map((ex) => `<circle cx="${ex}" cy="${EY}" r="10.5"/>`).join("")}<path d="M${EX[0] + 10.5},${EY}H${EX[1] - 10.5}"/></g>`;
    if (S.glasses === "rect") faceTop += `<g fill="none" stroke="#2a2220" stroke-width="2.6">${EX.map((ex) => `<rect x="${ex - 11}" y="${EY - 8}" width="22" height="16" rx="4"/>`).join("")}<path d="M${EX[0] + 11},${EY}H${EX[1] - 11}"/></g>`;
    if (S.glassesUp) faceTop += `<g fill="none" stroke="#2a2220" stroke-width="2.6">${EX.map((ex) => `<rect x="${ex - 10}" y="-590" width="20" height="13" rx="4"/>`).join("")}<path d="M${EX[0] + 10},-584H${EX[1] - 10}"/></g>`;
    if (S.tache) faceTop += `<path d="M-3,-528Q9,-536 22,-528Q16,-522 9,-525Q2,-522 -3,-528Z" fill="${S.tache}"/>`;
    if (S.clip) faceTop += `<path d="M30,-584l3,-7l3,7l7,1l-5,5l1,7l-6,-4l-6,4l1,-7l-5,-5z" fill="${S.clip}"/>`;
    if (S.headTop) faceTop += S.headTop(x);
    const head = `<ellipse cx="2" cy="-546" rx="42" ry="45" fill="${skinS}"/><ellipse cx="5" cy="-547" rx="39.5" ry="43.6" fill="${skin}"/><ellipse cx="5" cy="-547" rx="39.5" ry="43.6" fill="url(#flFace)"/>
      <ellipse cx="-11" cy="-531" rx="7.5" ry="4.2" fill="#e8705a" opacity="${S.blush ?? 0.15}"/><ellipse cx="27" cy="-531" rx="7.5" ry="4.2" fill="#e8705a" opacity="${S.blush ?? 0.15}"/>
      <path d="M16,-541Q23,-533 20,-527Q15,-525 12,-528Q17,-532 16,-541Z" fill="${skinS}" opacity=".55"/>
      <g id="${id}-eyes">${eyeG}</g><g id="${id}-mouth">${mouthG}</g>
      <g id="${id}-hair"><g class="flHs">${hairF}${tie}${S.noShine ? "" : `<path d="M-16,-588Q2,-600 20,-591" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".14"/>`}</g></g>${ear}${faceTop}
      <g id="${id}-sweat" display="none"><path d="M44,-584c6,10 8,16 2,19c-6,-3 -6,-9 -2,-19z" fill="#cfe2e6"/></g>`;
    const neck = `<rect x="-11" y="-508" width="22" height="26" fill="${skinS}"/>`;
    const HS = (inner) => `<g transform="translate(0,-500) scale(${hs}) translate(0,500)">${inner}</g>`;

    const html = `<g id="${id}">
      <ellipse id="${id}-shadow" cx="0" cy="3" rx="${f(66 * w)}" ry="10" fill="#000" opacity=".22"/>
      <g class="flSq"><g id="${id}-root"><g id="${id}-body">
        <g transform="translate(-20,-300)">${leg("B")}</g>
        <g transform="translate(20,-300)">${leg("F")}</g>
        ${pelvis}
        <g transform="translate(-46,-455)">${arm("B", P.keep === "F" ? "" : P.hand || "")}</g>
        <g id="${id}-torso">
          <g id="${id}-hairB">${HS(hairBk)}</g>
          <g class="flBr">${neck}${torso}
          <g id="${id}-acc">${S.acc ? S.acc(x) : ""}</g>
          <g id="${id}-head"><g class="flHb">${HS(head)}</g></g></g>
        </g>
        <g transform="translate(46,-455)">${arm("F", P.keep === "B" ? "" : P.hand || "")}</g>
      </g></g></g></g>`;
    const g = document.createElementNS(NS, "g");
    g.innerHTML = html;
    parent.appendChild(g.firstElementChild);
    return document.getElementById(id);
  }

  // ---------------- ส้มโอ the cat, flat: same ids and groups as Rig.buildCat ----------------
  function buildCatFlat(parent, id) {
    const O = "#cf8448", OS = "#a8642e", CR = "#efe2c8";
    const html = `<g id="${id}"><ellipse cx="0" cy="4" rx="60" ry="9" fill="#000" opacity=".2"/>
      <g id="${id}-root"><g id="${id}-tail"><path d="M36,-14C84,-16 92,-62 72,-92" fill="none" stroke="${OS}" stroke-width="15" stroke-linecap="round"/></g>
      <g id="${id}-body"><path d="M-38,0C-46,-40 -28,-80 0,-80C28,-80 46,-40 38,0Z" fill="${O}"/>
        <path d="M-38,0C-46,-40 -28,-80 0,-80C-14,-70 -22,-40 -20,0Z" fill="${OS}" opacity=".6"/>
        <path d="M-14,0C-18,-28 -9,-52 0,-52C9,-52 18,-28 14,0Z" fill="${CR}"/>
        <ellipse cx="-15" cy="-2" rx="11" ry="6" fill="${CR}"/><ellipse cx="15" cy="-2" rx="11" ry="6" fill="${CR}"/></g>
      <g id="${id}-head"><path d="M-38,-120L-35,-162L-8,-140ZM38,-120L35,-162L8,-140Z" fill="${O}"/>
        <path d="M-31,-130L-30,-152L-16,-140ZM31,-130L30,-152L16,-140Z" fill="#e2a084"/>
        <ellipse cx="0" cy="-112" rx="44" ry="36" fill="${O}"/>
        <path d="M-44,-112C-44,-132 -30,-148 -8,-148C-26,-136 -32,-120 -26,-84C-38,-90 -44,-100 -44,-112Z" fill="${OS}" opacity=".55"/>
        <path d="M-8,-147l4,14l4,-14M-20,-142l6,11M20,-142l-6,11" stroke="${OS}" stroke-width="4" fill="none" stroke-linecap="round"/>
        <ellipse cx="0" cy="-99" rx="15" ry="10" fill="${CR}"/>
        <g class="ce-open"><ellipse cx="-16" cy="-116" rx="4.8" ry="6.2" fill="${INK}"/><ellipse cx="16" cy="-116" rx="4.8" ry="6.2" fill="${INK}"/>
          <circle cx="-14.4" cy="-118.3" r="1.5" fill="#fff"/><circle cx="17.6" cy="-118.3" r="1.5" fill="#fff"/></g>
        <g class="ce-closed" display="none"><path d="M-22,-115q6,5 12,0M10,-115q6,5 12,0" stroke="${INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/></g>
        <path d="M-3.5,-104h7l-3.5,4z" fill="#a85848"/></g></g></g>`;
    parent.insertAdjacentHTML("beforeend", html);
    return document.getElementById(id);
  }


  // ---------------- ส้มโอ in profile (a still prop, facing +x): "hiss" arched back, fur on end, ears flat, fangs · "sit" ----------------
  function catSide(x, y, s, mode = "hiss", flip = false) {
    const O = "#cf8448", OS = "#a8642e", CR = "#efe2c8";
    const sx = flip ? -s : s;
    let g = "";
    if (mode === "hiss") {
      // the arched back, sampled so the raised fur can run along it as a zigzag
      const P0 = [-92, -100], P1 = [-100, -172], P2 = [-48, -226], P3 = [8, -226], Q1 = [62, -226], Q2 = [106, -182], Q3 = [100, -118];
      const bez = (a, b, c, d, t) => [0, 1].map((i) => (1 - t) ** 3 * a[i] + 3 * (1 - t) ** 2 * t * b[i] + 3 * (1 - t) * t * t * c[i] + t ** 3 * d[i]);
      const pts = [];
      for (let k = 0; k <= 16; k++) { const t = k / 16; pts.push(t < 0.5 ? bez(P0, P1, P2, P3, t * 2) : bez(P3, Q1, Q2, Q3, t * 2 - 1)); }
      let fur = "";
      for (let k = 2; k < 15; k++) { const [x0, y0] = pts[k - 1], [x1, y1] = pts[k], [x2, y2] = pts[k + 1], nx = y2 - y0, ny = -(x2 - x0), n = Math.hypot(nx, ny) || 1;
        fur += `<path d="M${f(x0 - (nx / n) * 6)},${f(y0 - (ny / n) * 6)}L${f(x1 + (nx / n) * 16)},${f(y1 + (ny / n) * 16)}L${f(x2 - (nx / n) * 6)},${f(y2 - (ny / n) * 6)}Z" fill="${O}"/>`; }
      g += `<ellipse cx="10" cy="4" rx="130" ry="11" fill="#000" opacity=".22"/>
        <path d="M-84,-112C-128,-150 -138,-226 -112,-270C-100,-292 -80,-296 -72,-282" fill="none" stroke="${OS}" stroke-width="38" stroke-linecap="round"/>
        <path d="M-118,-200l-18,-6M-122,-236l-20,-2M-112,-268l-16,-12" stroke="${OS}" stroke-width="10" stroke-linecap="round"/>
        <rect x="-78" y="-112" width="17" height="114" rx="8.5" fill="${OS}"/><rect x="62" y="-110" width="17" height="112" rx="8.5" fill="${OS}"/>
        ${fur}
        <path d="M-92,-100C-100,-172 -48,-226 8,-226C62,-226 106,-182 100,-118Q102,-96 86,-90Q24,-152 -62,-88Q-86,-84 -92,-100Z" fill="${O}"/>
        <path d="M-62,-88Q24,-152 86,-90Q64,-124 12,-132Q-36,-128 -62,-88Z" fill="${OS}" opacity=".55"/>
        <path d="M-40,-206l10,26M-8,-220l5,28M26,-218l-2,28M58,-202l-8,26" stroke="${OS}" stroke-width="7" stroke-linecap="round"/>
        <rect x="-58" y="-104" width="17" height="106" rx="8.5" fill="${O}"/><rect x="82" y="-104" width="17" height="106" rx="8.5" fill="${O}"/>
        <ellipse cx="-46" cy="0" rx="14" ry="6.5" fill="${CR}"/><ellipse cx="94" cy="0" rx="14" ry="6.5" fill="${CR}"/>
        <path d="M84,-150Q100,-176 118,-176L104,-104Q88,-110 84,-150Z" fill="${CR}"/>
        <path d="M104,-168L70,-176L98,-150ZM118,-174L96,-196L126,-170Z" fill="${OS}"/>
        <ellipse cx="122" cy="-142" rx="38" ry="34" fill="${O}"/>
        <path d="M86,-150Q90,-172 112,-176Q98,-160 100,-120Q88,-128 86,-150Z" fill="${OS}" opacity=".5"/>
        <ellipse cx="150" cy="-128" rx="16" ry="12" fill="${CR}"/>
        <path d="M142,-128L166,-124L156,-108Q146,-110 142,-128Z" fill="${INK}"/>
        <path d="M147,-127l2.5,7l2.5,-6.5M156,-125.5l2,6l2.5,-5.5" fill="#f4ecd8"/>
        <path d="M157,-142l7,1l-4,5z" fill="#a85848"/>
        <ellipse cx="136" cy="-152" rx="6" ry="5.4" fill="${INK}"/><circle cx="137.6" cy="-154" r="1.8" fill="#fff"/>
        <path d="M124,-166L148,-158" stroke="${INK}" stroke-width="4.6" stroke-linecap="round"/>
        <path d="M160,-132L206,-142M160,-126L206,-124M158,-120L200,-106" stroke="${CR}" stroke-width="2.4" stroke-linecap="round" opacity=".85"/>`;
    } else {
      g += `<ellipse cx="0" cy="4" rx="90" ry="10" fill="#000" opacity=".22"/>
        <path d="M-60,-10C-100,-12 -110,20 -60,8C-20,0 30,4 60,-2" stroke="${OS}" stroke-width="16" fill="none" stroke-linecap="round"/>
        <path d="M-70,0C-84,-80 -40,-150 20,-150C64,-150 70,-90 56,0Z" fill="${O}"/>
        <path d="M-70,0C-84,-80 -40,-150 20,-150C-20,-120 -40,-70 -34,0Z" fill="${OS}" opacity=".55"/>
        <path d="M30,-130Q60,-120 56,0H24Q40,-60 30,-130Z" fill="${CR}"/>
        <path d="M14,-196L24,-236L44,-200ZM52,-198L70,-232L78,-192Z" fill="${O}"/>
        <ellipse cx="44" cy="-176" rx="44" ry="36" fill="${O}"/>
        <path d="M70,-160Q92,-160 92,-150Q90,-140 70,-142Z" fill="${CR}"/>
        <circle cx="66" cy="-182" r="6" fill="${INK}"/><circle cx="67.8" cy="-184" r="1.8" fill="#fff"/>
        <path d="M88,-158l4,-3l1,5z" fill="#a85848"/>`;
    }
    return `<g transform="translate(${f(x)},${f(y)}) scale(${f(sx)},${f(s)})">${g}</g>`;
  }

  // ---------------- v2 life: breathing, a swaying tuft, ties and scarves that lag, eyes that glance, squash on a landing ----------------
  const hash = (str) => { let h = 7; for (const ch of str) h = (h * 31 + ch.charCodeAt(0)) % 1000003; return h; };
  const loopTo = (tl, sel, from, to, period, t0, dur, ph = 0) => { if (dur <= 0.3) return; const n = Math.max(1, Math.ceil(dur / period) * 2);
    tl.fromTo(sel, from, { ...to, duration: period / 2, repeat: n, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, t0 - ph)); };
  function life(tl, id, t0, dur, track) {
    const root = document.getElementById(id); if (!root || !root.querySelector(".flBr")) return;
    const h = hash(id), walking = JSON.stringify(track || "").includes('"walk"') || JSON.stringify(track || "").includes("\"run\"");
    const amp = walking ? 2.2 : 1;
    loopTo(tl, `#${id} .flBr`, { scaleY: 1, svgOrigin: "0 -296" }, { scaleY: 1.013, svgOrigin: "0 -296" }, 3.4 + (h % 7) * 0.1, t0, dur, (h % 11) * 0.2);
    loopTo(tl, `#${id} .flHb`, { rotation: -0.6, svgOrigin: "0 -500" }, { rotation: 0.6, svgOrigin: "0 -500" }, 2.9 + (h % 5) * 0.15, t0, dur, (h % 13) * 0.17);
    loopTo(tl, `#${id} .flHs`, { rotation: -1.4 * amp, svgOrigin: "0 -560" }, { rotation: 1.4 * amp, svgOrigin: "0 -560" }, walking ? 0.55 : 1.9 + (h % 4) * 0.2, t0, dur, (h % 7) * 0.11);
    if (root.querySelector(".jkTie")) loopTo(tl, `#${id} .jkTie`, { rotation: -2.2 * amp, svgOrigin: "0 -472" }, { rotation: 2.2 * amp, svgOrigin: "0 -472" }, walking ? 0.6 : 1.6, t0, dur, (h % 9) * 0.1);
    if (root.querySelector(".jkScarf")) loopTo(tl, `#${id} .jkScarf`, { rotation: -5 * amp, svgOrigin: "30 -470" }, { rotation: 5 * amp, svgOrigin: "30 -470" }, walking ? 0.5 : 1.2, t0, dur, (h % 5) * 0.1);
    if (root.querySelector(".flSway")) loopTo(tl, `#${id} .flSway`, { rotation: -2 * amp, svgOrigin: "0 -480" }, { rotation: 2 * amp, svgOrigin: "0 -480" }, walking ? 0.6 : 1.8, t0, dur, (h % 6) * 0.1);
    // glances: every few seconds the eyes slide a touch and come back
    let t = 1.1 + (h % 10) * 0.23; const eyes = `#${id}-eyes`;
    while (t + 0.9 < dur) { const dx = (h + Math.round(t * 10)) % 2 ? 2.6 : -2.4;
      tl.to(eyes, { x: dx, duration: 0.14, ease: "power2.out" }, t0 + t); tl.to(eyes, { x: 0, duration: 0.18, ease: "power2.inOut" }, t0 + t + 0.6 + (h % 3) * 0.15); t += 2.6 + ((h >> 3) % 5) * 0.4; }
  }
  const squash = (tl, id, at, amt = 0.16, dur = 0.42) => { const sel = `#${id} > .flSq`;
    tl.fromTo(sel, { scaleY: 1, scaleX: 1, svgOrigin: "0 0" }, { scaleY: 1 - amt, scaleX: 1 + amt * 0.7, svgOrigin: "0 0", duration: 0.08, ease: "power2.out", immediateRender: false }, at);
    tl.to(sel, { scaleY: 1, scaleX: 1, svgOrigin: "0 0", duration: dur, ease: "elastic.out(1, 0.45)" }, at + 0.08); };
  const prevDrive = Rig.drive;
  Rig.drive = (tl, id, t0, dur, track, blinks) => { prevDrive(tl, id, t0, dur, track, blinks); if (Rig.FLAT) life(tl, id, t0, dur, track); };
  Rig.squash = squash;

  const prevBuild = Rig.build, prevCat = Rig.buildCat;
  Rig.build = (parent, id, P) => (Rig.FLAT && P && P.v2 ? buildFlat(parent, id, P, nameOf(P)) : prevBuild(parent, id, P));
  Rig.buildCat = (parent, id) => (Rig.FLAT ? buildCatFlat(parent, id) : prevCat(parent, id));
  window.Flat = { buildFlat, buildCatFlat, catSide, SPEC, HAIR, mute, shd, far, INK, life, squash };
})();
