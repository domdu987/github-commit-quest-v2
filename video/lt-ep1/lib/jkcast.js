// สกิลจอมโกหก (story 1) · the cast in the channel look (sig.js faces on flat.js bodies). Load after sig.js.
//   jkYou      คุณ: the channel avatar (messy hair, one cowlick, round glasses) in a cheap navy suit, white shirt, mustard tie
//              ears: every jk character with lie-ears carries <g class="jkEar"> (red, glowing) at opacity 0 — show it with
//              tl.to(`#${aid} .jkEar`, { opacity: 1 }) when you lie · variants jkYouBook (the book "พูดให้คนเชื่อ ใน 7 วัน"),
//              jkYouBag (briefcase), jkYouCard (the grey card)
//   jkKen      the SSR boy: spiky hair, red scarf, a white tunic · jkKenSword (the light sword, glowing)
//   jkGod      the goddess behind the gacha counter: long lilac hair, a gold halo, a toga; <g class="jkGum"> a pink bubble
//   jkAunt     a customer in a café (story 1 opening) · jkSoul1/2/3 the dead in the queue on the clouds (pale, a ticket)
(function () {
  const { mix, dk, hi } = Rig2;
  const C = Rig.CAST, S = Flat.SPEC, PROP = Sig.PROP, faces = Sig.sigFaces;
  const ear = `<g class="jkEar" opacity="0"><ellipse cx="-33" cy="-540" rx="13" ry="16" fill="#ff5a3a" opacity=".35"/><ellipse cx="-33" cy="-540" rx="8" ry="10.5" fill="#e8402e"/><ellipse cx="-33" cy="-539" rx="3.8" ry="5.8" fill="#b82418"/></g>`;
  const suit = (tie) => (x) => `<path d="M-20,-490L0,-430L20,-490Z" fill="#f4f1ea"/><path d="M-5,-488H5L7,-474L0,-466L-7,-474Z" fill="${tie}"/><g class="jkTie"><path d="M-6,-472L-9,-372L0,-358L9,-372L6,-472Z" fill="${tie}"/><path d="M-6,-472L-9,-372L0,-358L9,-372L6,-472Z" fill="url(#flV)"/><path d="M-3,-468L-5,-380" stroke="#fff" stroke-width="1.6" opacity=".25"/></g>
    <path d="M-20,-490L0,-430L-8,-400L-34,-470Z" fill="${dk(x.top, 0.16)}"/><path d="M20,-490L0,-430L8,-400L34,-470Z" fill="${dk(x.top, 0.1)}"/>
    <circle cx="5" cy="-330" r="4" fill="${dk(x.top, 0.3)}"/><circle cx="5" cy="-296" r="4" fill="${dk(x.top, 0.3)}"/><rect x="22" y="-430" width="16" height="4" fill="#f4f1ea" opacity=".8"/>`;
  S.jkYou = { hair: "messy", glasses: "round", faces: faces({ browW: 4.8 }), acc: suit("#d9a43a"), headTop: () => ear };
  C.jkYou = { v2: { skin: "#c68b60", hair: { c: "#1f1813" }, top: { kind: "coat", c: "#2c3a5e", sleeve: "long" }, bottom: { kind: "trousers", c: "#28324e" },
    feet: { kind: "boot", c: "#1c1a1a" }, w: 1.02 } };
  const BOOK = `<g transform="translate(0,112) rotate(-8)"><rect x="-30" y="-56" width="56" height="74" rx="4" fill="#d8352a"/><rect x="-30" y="-56" width="8" height="74" fill="#a8241c"/>
    <rect x="-18" y="-44" width="38" height="10" fill="#f6d36a"/><rect x="-18" y="-28" width="30" height="5" fill="#f4ecd8"/><rect x="-18" y="-20" width="24" height="5" fill="#f4ecd8"/><text x="5" y="10" font-family="Kanit" font-weight="900" font-size="20" fill="#f6d36a" text-anchor="middle">7</text></g>`;
  const BAG = `<g transform="translate(0,112)"><rect x="-38" y="6" width="76" height="54" rx="6" fill="#4a3426"/><rect x="-38" y="6" width="76" height="12" fill="#3a281c"/><path d="M-12,6v-12h24v12" stroke="#3a281c" stroke-width="5" fill="none"/><rect x="-5" y="22" width="10" height="8" fill="#c8a040"/></g>`;
  const CARD = `<g transform="translate(0,112) rotate(-10)"><rect x="-26" y="-74" width="52" height="74" rx="6" fill="#9aa0a6"/><rect x="-21" y="-69" width="42" height="64" rx="4" fill="#b8bdc2"/><text x="0" y="-26" font-family="Kanit" font-weight="900" font-size="30" fill="#5a5f66" text-anchor="middle">F</text></g>`;
  C.jkYouBook = { v2: C.jkYou.v2, hand: BOOK, keep: "F" };
  C.jkYouBag = { v2: C.jkYou.v2, hand: BAG, keep: "F" };
  C.jkYouCard = { v2: C.jkYou.v2, hand: CARD, keep: "F" };

  Flat.HAIR.spiky = (c) => `<path d="M-42,-532C-48,-566 -40,-584 -30,-592L-40,-622L-14,-604L-6,-640L12,-608L32,-634L34,-598L58,-606L46,-574Q48,-562 46,-556Q36,-574 22,-574Q4,-570 -10,-576Q-22,-566 -30,-556Q-33,-546 -34,-532Z" fill="${c}"/>
    <path d="M-20,-600L-6,-636M14,-604L30,-628" stroke="${hi(c, 0.3)}" stroke-width="4" stroke-linecap="round" opacity=".55"/>`;
  S.jkKen = { hair: "spiky", faces: faces({ browW: 5.2 }),
    acc: () => `<path d="M-46,-490Q0,-454 46,-490L50,-468Q0,-436 -50,-468Z" fill="#c8302a"/><g class="jkScarf"><path d="M30,-470L58,-400L42,-396Z" fill="#a8241e"/></g>
      <rect x="-45" y="-330" width="90" height="16" fill="#8a5a32"/><rect x="-8" y="-334" width="16" height="24" rx="3" fill="#d8b84a"/>` };
  C.jkKen = { v2: { skin: "#d4a07a", hair: { c: "#e8c46a" }, top: { kind: "tee", c: "#efe8dc", sleeve: "long" }, bottom: { kind: "trousers", c: "#4a4a5a" },
    feet: { kind: "boot", c: "#5a3a24" }, w: 0.98 } };
  const SWORD = `<g transform="translate(0,112) rotate(-150)"><rect x="-5" y="-6" width="10" height="34" rx="4" fill="#5a3a24"/><rect x="-22" y="26" width="44" height="9" rx="4" fill="#d8b84a"/>
    <path d="M-9,34L-9,200L0,226L9,200L9,34Z" fill="#fff6c8"/><path d="M-26,34L-26,206L0,246L26,206L26,34Z" fill="#ffd85a" opacity=".35"/><path d="M-50,34L-50,214L0,270L50,214L50,34Z" fill="#ffd85a" opacity=".12"/></g>`;
  C.jkKenSword = { v2: C.jkKen.v2, hand: SWORD, keep: "F" };

  S.jkGod = { hair: "long", hairB: "longB", faces: faces({ k: 0.72, browW: 3.4 }),
    acc: () => `<path d="M-44,-470L44,-490L45,-296H-45Z" fill="#f6f0ff" opacity=".0"/><path d="M-46,-480Q-10,-440 46,-488L46,-460Q0,-420 -46,-452Z" fill="#d8c8f0"/>
      <rect x="-45" y="-330" width="90" height="12" fill="#d8b84a"/>`,
    headTop: () => `<ellipse cx="4" cy="-640" rx="40" ry="9" fill="none" stroke="#ffd85a" stroke-width="6"/><ellipse cx="4" cy="-640" rx="48" ry="14" fill="none" stroke="#ffd85a" stroke-width="3" opacity=".35"/>
      <g class="jkGum" opacity="0"><circle cx="30" cy="-512" r="22" fill="#ff8ab8"/><circle cx="24" cy="-520" r="6" fill="#ffd0e4"/></g>
      <path d="M2,-523q7,3 14,0" stroke="#c84a6a" stroke-width="3.4" fill="none" stroke-linecap="round"/>` };
  C.jkGod = { v2: { skin: "#e2b48e", hair: { c: "#b8a0e0" }, top: { kind: "tank", c: "#f6f0ff" }, bottom: { kind: "sarong", c: "#e8e0f8", band: "#d8b84a" },
    feet: { kind: "sandal", c: "#d8b84a" }, w: 1.0 } };

  S.jkAunt = { hair: "perm", faces: faces({ crinkle: true, k: 0.85, browW: 3.6 }),
    acc: () => `<path d="M-15,-490Q0,-450 15,-490" stroke="#e8d8a0" stroke-width="3" fill="none"/><circle cx="0" cy="-458" r="5" fill="#e8d8a0"/>` };
  C.jkAunt = { v2: { skin: "#d8a47c", hair: { c: "#2a2220" }, top: { kind: "tee", c: "#c86a8a", sleeve: "elbow" }, bottom: { kind: "trousers", c: "#3a3a4a" },
    feet: { kind: "sandal", c: "#c8a080" }, w: 1.12 } };
  const ticket = (n) => `<g transform="translate(14,-420) rotate(6)"><rect x="-20" y="-14" width="40" height="28" rx="4" fill="#f4ecd8"/><text x="0" y="7" font-family="Kanit" font-weight="900" font-size="17" fill="#3a3a44" text-anchor="middle">${n}</text></g>`;
  [["jkSoul1", "short", "#2a2420", "#6a8aa8", "#3a3e4a", "#c8946a", 4], ["jkSoul2", "bob", "#3a2a24", "#a86a6a", "#2e3242", "#e0b088", 7], ["jkSoul3", "buzz", "#5a5a5a", "#7a9a6a", "#4a4a3a", "#b07850", 9]].forEach(([n, hair, hc, tc, bc, sk, num]) => {
    S[n] = { hair, faces: faces({ k: 0.9 }), acc: () => ticket(num) };
    C[n] = { v2: { skin: sk, hair: { c: hc }, top: { kind: "tee", c: tc, sleeve: "short" }, bottom: { kind: "trousers", c: bc }, feet: { kind: "sandal", c: "#3a3030" } } };
  });
  window.JK = { BOOK, BAG, CARD, SWORD };
  // ---------------- EP.2+ ----------------
  // ถั่วงอก: a small kid with a topknot (จุก), an oversized faded tee, shorts, barefoot · jkKidLizard holds the knocked-out gecko up
  Flat.HAIR.juk = (c) => `<path d="M-41,-532C-46,-580 -18,-596 4,-596C30,-596 48,-584 45,-562Q30,-574 6,-574Q-16,-574 -28,-560Q-32,-550 -33,-532Z" fill="${c}"/>
    <circle cx="6" cy="-612" r="17" fill="${c}"/><path d="M-6,-598Q6,-592 18,-598" stroke="#d8443a" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  S.jkKid = { hair: "juk", faces: faces({ k: 1.3, browW: 4 }), headScale: 1.22,
    headTop: () => `<ellipse cx="31" cy="-529" rx="7" ry="4.4" fill="#e0705e" opacity=".3"/>` };
  C.jkKid = { v2: { skin: "#c8905e", hair: { c: "#1c1612" }, top: { kind: "tee", c: "#7aa8c8", sleeve: "short" }, bottom: { kind: "shorts", c: "#c8a46a" }, feet: { kind: "bare" }, w: 1.08, limb: 0.92 } };
  const GECKO = `<g transform="translate(0,112) rotate(-160)"><g transform="translate(0,-60)"><path d="M-30,0Q0,-14 30,0Q0,12 -30,0Z" fill="#8ab06a"/><circle cx="34" cy="0" r="11" fill="#8ab06a"/>
    <path d="M-30,0Q-56,6 -62,-10" stroke="#8ab06a" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-12,-8l-8,-12M12,-8l8,-12M-12,8l-8,12M12,8l8,12" stroke="#7a9a5a" stroke-width="5" stroke-linecap="round"/>
    <path d="M30,-4l4,4l4,-4M30,4" stroke="#2a2220" stroke-width="2" fill="none"/><circle cx="40" cy="-14" r="5" fill="#d8a080"/></g></g>`;
  C.jkKidLizard = { v2: C.jkKid.v2, hand: GECKO, keep: "F" };
  // มะปราง: elf at the guild/tavern counter: pointed ears, long dark-green hair, a guild vest
  S.jkMap = { hair: "long", hairB: "longB", faces: faces({ k: 0.8, browW: 3.8 }), noEar: true,
    acc: (x) => `<path d="M-44,-470L-12,-470L0,-420L12,-470L44,-470L45,-300H-45Z" fill="#7a3a3a" opacity=".92"/><circle cx="-24" cy="-420" r="6" fill="#d8b84a"/>`,
    headTop: (x) => `<path d="M-38,-552L-74,-578L-36,-528Z" fill="${x.skin}"/><path d="M-40,-548L-62,-566L-38,-534Z" fill="${x.skinS}"/>` };
  C.jkMap = { v2: { skin: "#e8c4a0", hair: { c: "#2e5a4a" }, top: { kind: "tee", c: "#f4ecd8", sleeve: "long" }, bottom: { kind: "trousers", c: "#3a3040" }, feet: { kind: "boot", c: "#4a3020" } } };
  // tavern regulars
  [["jkMan1", "buzz", "#2a2420", "#8a6a4a", "#3a3e4a", "#b88660", 1.14], ["jkMan2", "side", "#5a4030", "#5a7a8a", "#2e3242", "#d4a07a", 1.0], ["jkMan3", "horseshoe", "#8a8680", "#a8584a", "#4a4a3a", "#c08a62", 1.2],
   ["jkWom1", "bun", "#3a2a24", "#c8a050", "#5a3a4a", "#d8a47c", 1.0]].forEach(([n, hair, hc, tc, bc, sk, w]) => {
    S[n] = { hair, faces: faces({ k: 0.9 }), tache: n === "jkMan3" ? "#8a8680" : undefined };
    C[n] = { v2: { skin: sk, hair: { c: hc }, top: { kind: "tee", c: tc, sleeve: n === "jkMan1" ? "none" : "elbow" }, bottom: { kind: "trousers", c: bc }, feet: { kind: "boot", c: "#4a3020" }, w } };
  });
  // you with the wooden bucket over your head (the ears hidden): a band of planks, two iron hoops
  const bucket = `<g transform="translate(4,-560)"><path d="M-58,-62L58,-62L66,46L-66,46Z" fill="#a8743e"/>${[-40, -14, 12, 38].map((x) => `<path d="M${x},-62L${x * 1.12},46" stroke="#8a5a2c" stroke-width="3"/>`).join("")}
    <rect x="-62" y="-40" width="124" height="9" fill="#5a5e66"/><rect x="-66" y="20" width="132" height="9" fill="#5a5e66"/><path d="M-66,46H66" stroke="#6a4424" stroke-width="7"/>
    <path d="M-30,-40v30M30,-40v30" stroke="#5a3a1a" stroke-width="2" opacity=".5"/><ellipse cx="-14" cy="0" rx="9" ry="5" fill="#2a1a10"/><ellipse cx="24" cy="0" rx="9" ry="5" fill="#2a1a10"/></g>`;
  S.jkYouBucket = { ...S.jkYou, headTop: () => bucket };
  C.jkYouBucket = { v2: C.jkYou.v2 };
  window.JK.GECKO = GECKO;

  // the dragon, side on, facing right, about 640 wide (x −310…350, y −300…166), feet on y 146: a fierce one — bat wings, a spined back,
  // a thick tail with a spade, and a wedge skull with the jaws open, fangs out, yellow slit eye and two swept-back horns
  // JK.dragon(fill, o) → svg · o.stroke (outline only: chalk) · o.detail:false (plain silhouette) · o.ko (out cold: eyes X, mouth shut, tongue out)
  // · three heads (the lie said so): o.heads: ids prefix → <g id="<prefix>h0..2"> main, top, bottom neck+head (so a shot can wag them)
  const f1 = (v) => (+v).toFixed(1);
  const dragon = (fill, o = {}) => {
    const st = o.stroke ? `fill="none" stroke="${o.stroke}" stroke-width="${o.sw || 8}" stroke-dasharray="${o.dash || "none"}" stroke-linejoin="round"` : `fill="${fill}"`;
    const det = !o.stroke && o.detail !== false, H = (k, inner) => `<g${o.heads ? ` id="${o.heads}h${k}"` : ""}>${inner}</g>`;
    const tri = (x, y, h) => `<path d="M${f1(x - h * 0.45)},${f1(y + h * 0.3)}L${f1(x)},${f1(y - h)}L${f1(x + h * 0.45)},${f1(y + h * 0.3)}Z" ${st}/>`;
    const tail = `<path d="M-112,8Q-226,36 -258,-28Q-276,-68 -256,-100L-240,-86Q-238,-52 -212,-24Q-176,10 -104,54Z" ${st}/><path d="M-256,-100L-306,-128L-296,-76L-242,-80Z" ${st}/>`;
    const spines = [[-226, -12, 16], [-196, 0, 16], [-166, 8, 14], [-100, -58, 22], [-60, -72, 24], [-20, -78, 24], [20, -76, 22], [60, -66, 20], [92, -108, 16], [126, -144, 16], [162, -166, 14]].map(([x, y, h]) => tri(x, y, h)).join("");
    const body = `<path d="M-130,40Q-150,-30 -90,-56Q-20,-84 70,-60Q130,-44 128,10Q120,70 60,88Q-30,104 -100,84Q-134,70 -130,40Z" ${st}/>`;
    const legs = `<path d="M-96,56Q-122,100 -98,146H-40Q-56,110 -30,70Z" ${st}/><path d="M-98,146L-120,158L-94,150L-104,166L-78,150L-74,166L-60,146Z" ${st}/>
      <path d="M44,70Q34,110 56,146H108Q96,110 112,76Z" ${st}/><path d="M56,146L34,158L60,150L52,166L76,150L82,166L96,146Z" ${st}/>`;
    const wing = (dx, dy, op) => `<g transform="translate(${dx},${dy})${o.ko ? " rotate(78 -30 -60)" : ""}"${op ? ` opacity="${op}"` : ""}>
      <path d="M-30,-60L-60,-240L-180,-220Q-125,-262 -120,-320Q-72,-300 -30,-340Q-10,-290 60,-290Q30,-210 90,-110Q30,-80 -30,-60Z" ${st}/>
      ${o.stroke ? "" : `<path d="M-30,-60L-60,-240" stroke="${fill}" stroke-width="24" stroke-linecap="round"/><path d="M-60,-240L-180,-220M-60,-240L-120,-320M-60,-240L-30,-340M-60,-240L60,-290" stroke="#000" stroke-opacity=".22" stroke-width="6" fill="none" stroke-linecap="round"/>`}</g>`;
    const jaw = `<path d="M210,-116L286,-128Q318,-112 332,-84L318,-76Q290,-100 262,-92L226,-80Q206,-96 210,-116Z" ${st}/>${det && !o.ko ? `<path d="M290,-120L298,-146L306,-118ZM312,-102L320,-130L328,-100Z" fill="#fff"/>` : ""}`;
    // the skull (absolute coords, neck joint at (205,-140)) placed on each of the three necks: top (behind), main, bottom (in front)
    const skullAt = (k, jx, jy, a, sc, neck, tongue) => H(k, `${neck}<g transform="translate(${jx},${jy}) rotate(${a}) scale(${sc}) translate(-205,140)">
      <path d="M190,-200Q250,-222 330,-182L344,-168Q300,-150 276,-132L206,-120Q186,-160 190,-200Z" ${st}/>
      ${o.ko ? `<g transform="rotate(-17 212 -116)">${jaw}</g>` : jaw}
      <path d="M208,-202L158,-292L182,-284L224,-212ZM232,-208L218,-302L242,-288L252,-210Z" ${st}/>
      ${det ? (o.ko ? `<path d="M226,-194l18,14M244,-194l-18,14" stroke="#1a0e08" stroke-width="5" stroke-linecap="round" fill="none"/>${tongue ? `<path d="M318,-104Q336,-96 332,-78Q320,-84 316,-98Z" fill="#e87a8a"/>` : ""}`
        : `<path d="M294,-148L300,-122L308,-150ZM316,-160L322,-136L330,-162Z" fill="#fff"/><path d="M214,-186Q236,-204 262,-184Q238,-174 214,-186Z" fill="#ffd040"/><path d="M238,-198L242,-178" stroke="#1a0e08" stroke-width="3.5" stroke-linecap="round"/>
          <path d="M212,-196Q240,-214 268,-194" stroke="#000" stroke-opacity=".3" stroke-width="5" fill="none" stroke-linecap="round"/>${tongue ? `<path d="M338,-186q10,-14 2,-26q12,-10 4,-22" stroke="#fff" stroke-opacity=".5" stroke-width="4" fill="none" stroke-linecap="round"/>` : ""}`) : ""}</g>`);
    const heads = skullAt(1, 128, -262, -40, 0.78, `<path d="M40,-60Q50,-160 112,-272L146,-252Q106,-160 96,-40Z" ${st}/>`, false)
      + skullAt(0, 205, -140, -4, 1.06, `<path d="M60,-30Q60,-90 110,-130Q150,-172 200,-162L210,-110Q160,-100 130,-60Q110,-30 120,20Z" ${st}/>`, true)
      + skullAt(2, 252, -12, 28, 0.78, `<path d="M96,-16Q170,-50 240,-28L258,6Q176,10 118,44Z" ${st}/>`, false);
    const belly = det ? `<path d="M-116,34Q-16,72 86,52" stroke="#fff" stroke-opacity=".16" stroke-width="22" fill="none" stroke-linecap="round"/>` : "";
    const legsPlain = `<path${legs.split("<path")[1]}<path${legs.split("<path")[3]}`;
    if (o.stroke) return `${tail}${body}${legsPlain}${wing(0, 0)}${heads}`;
    return `${o.ko ? "" : wing(-34, 12, 0.72)}${tail}${body}${spines}${legs}${wing(0, 0)}${heads}${belly}`;
  };
  window.JK.dragon = dragon;

  // ---------------- EP.4 ----------------
  // horns pushing up through the hair: <g class="jkHorn"> (grow with scale from the scalp, svgOrigin "4 -590" in head space)
  const horns = `<g class="jkHorn"><path d="M-26,-588Q-44,-640 -20,-676Q-30,-636 -6,-596Z" fill="#7a1e24"/><path d="M30,-590Q50,-640 28,-680Q40,-636 14,-598Z" fill="#7a1e24"/>
    <path d="M-24,-600Q-34,-630 -22,-654" stroke="#a8343a" stroke-width="3" fill="none"/><path d="M28,-602Q38,-630 28,-656" stroke="#a8343a" stroke-width="3" fill="none"/></g>`;
  S.jkYouHorn = { ...S.jkYou, headTop: () => ear + horns };
  C.jkYouHorn = { v2: C.jkYou.v2 };
  S.jkYouHornBucket = { ...S.jkYou, headTop: () => horns + bucket };
  C.jkYouHornBucket = { v2: C.jkYou.v2 };
  // royal guards: a steel cap with a red plume, a red tabard over mail, a spear in the near hand
  Flat.HAIR.helm = (c) => `<path d="M-46,-540C-50,-600 -16,-612 6,-612C36,-612 54,-598 50,-540L40,-536Q4,-546 -36,-536Z" fill="#9aa2aa"/><path d="M-46,-546H50" stroke="#6a727a" stroke-width="7"/>
    <path d="M2,-612Q-10,-650 18,-668Q12,-640 22,-614Z" fill="#c8302a"/><path d="M4,-606V-546" stroke="#c4ccd4" stroke-width="5"/>`;
  S.jkGuard = { hair: "helm", faces: faces({ k: 0.8, browW: 5 }), noEar: true,
    acc: () => `<path d="M-30,-488H30L36,-300H-36Z" fill="#b82e2a"/><path d="M-30,-488H30L28,-470H-28Z" fill="#d8b84a"/><circle cx="0" cy="-400" r="16" fill="#d8b84a"/>` };
  C.jkGuard = { v2: { skin: "#c08a62", hair: { c: "#2a2420" }, top: { kind: "tee", c: "#8a929a", sleeve: "long" }, bottom: { kind: "trousers", c: "#4a4a52" }, feet: { kind: "boot", c: "#3a2a20" }, w: 1.1 } };
  const SPEAR = `<g transform="translate(0,112) rotate(-6)"><rect x="-4" y="-300" width="8" height="380" rx="3" fill="#6a4a2a"/><path d="M-12,-300L0,-350L12,-300Z" fill="#c4ccd4"/></g>`;
  C.jkGuardSpear = { v2: C.jkGuard.v2, hand: SPEAR, keep: "F" };
  S.jkGuardSpear = S.jkGuard;

  // ---------------- acting poses for the series (v2b): the body says it before the narrator does ----------------
  //   shrug · facepalm · cheer · cower · think · coverEars · despair · relief · pray · fold (arms crossed) · nod · no (head shake)
  const M = Rig.MODES, Z = (u, o) => M.idle(u, o);
  M.shrug = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.2); return { ...Z(u, o), uaF: -62 + b, faF: -92, uaB: 62 - b, faB: 92, head: -5 + 2 * b, torso: -2, bodyY: -5 - b }; };
  M.facepalm = (u, o) => { const b = Math.sin(u * 1.6); return { ...Z(u, o), uaF: -118, faF: -138, uaB: 8, faB: -14, head: 15 + b, torso: 7, bodyY: 3 }; };
  M.cheer = (u, o) => { const h = Math.abs(Math.sin(u * 2 * Math.PI / (o.period || 0.7))); return { ...Z(u, o), uaF: -162 + 6 * h, faF: -14, uaB: 162 - 6 * h, faB: 14, head: -9, torso: -4, bodyY: -22 * h }; };
  M.cower = (u, o) => { const j = Math.sin(u * 41) * 1.2 + Math.sin(u * 27) * 0.8; return { ...Z(u, o), thF: -30, shF: 48, thB: -18, shB: 38, torso: 20 + j * 0.4, head: 16 + j, uaF: -122 + j, faF: -150, uaB: 118 - j, faB: 148, bodyY: 54 }; };
  M.think = (u, o) => { const b = Math.sin(u * 1.9); return { ...Z(u, o), uaF: -84, faF: -152, uaB: 24, faB: -34, head: 5 + 2.5 * b, torso: 3, bodyY: -1 }; };
  M.coverEars = (u, o) => { const j = Math.sin(u * 37) * 0.9; return { ...Z(u, o), uaF: -138 + j, faF: -118, uaB: 138 - j, faB: 118, head: 4 + j * 0.6, torso: 5, bodyY: 2 }; };
  M.despair = (u, o) => { const b = Math.sin(u * 1.1); return { ...Z(u, o), uaF: 12, faF: -2, uaB: -12, faB: 2, torso: 11 + 0.6 * b, head: 24 + b, bodyY: 9 }; };
  M.relief = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.6); return { ...Z(u, o), uaF: -98, faF: -128, uaB: 6, faB: -12, head: -9 + 1.5 * b, torso: -5, bodyY: -3 + 2 * b }; };
  M.pray = (u, o) => { const j = Math.sin(u * 19) * 0.7; return { ...Z(u, o), uaF: -58 + j, faF: -136, uaB: 58 - j, faB: 136, head: 7, torso: 5, bodyY: 2 }; };
  M.fold = (u, o) => ({ ...Z(u, o), uaF: -42, faF: -132, uaB: 42, faB: 132, head: -3, torso: -3, bodyY: -1 });
  M.nod = (u, o) => ({ ...Z(u, o), head: 7 * Math.sin(u * 2 * Math.PI / (o.period || 0.55)) + 4 });
  M.no = (u, o) => ({ ...Z(u, o), head: 5 * Math.sin(u * 2 * Math.PI / 0.3), hair: -5 * Math.sin(u * 2 * Math.PI / 0.3) });
  M.sitCheer = (u, o) => { const h = Math.abs(Math.sin(u * 2 * Math.PI / 0.7)); return { ...M.sitChair(u, o), uaF: -160 + 6 * h, faF: -14, uaB: 160 - 6 * h, faB: 14, head: -8, torso: -6, bodyY: 150 - 10 * h }; };
  M.sitPray = (u, o) => { const j = Math.sin(u * 19) * 0.7; return { ...M.sitChair(u, o), uaF: -58 + j, faF: -136, uaB: 58 - j, faB: 136, head: 8, torso: 6 }; };
  M.sitCower = (u, o) => { const j = Math.sin(u * 41) * 1.2; return { ...M.sitChair(u, o), uaF: -122 + j, faF: -150, uaB: 118 - j, faB: 148, head: 16 + j, torso: 14 }; };
  M.sitDespair = (u, o) => { const b = Math.sin(u * 1.1); return { ...M.sitChair(u, o), uaF: 8, faF: -4, uaB: -8, faB: 4, head: 24 + b, torso: 12 }; };
  M.sitCoverEars = (u, o) => { const j = Math.sin(u * 37) * 0.9; return { ...M.sitChair(u, o), uaF: -138 + j, faF: -118, uaB: 138 - j, faB: 118, head: 4, torso: 5 }; };
  M.sitHoldHead = (u, o) => { const sw = Math.sin(u * 2.2) * 3; return { ...M.sitChair(u, o), uaF: -150, faF: -106, uaB: 150, faB: 106, head: 8 + sw, torso: 4 }; };
  M.sitFacepalm = (u, o) => ({ ...M.sitChair(u, o), uaF: -118, faF: -138, uaB: 8, faB: -14, head: 15, torso: 8 });
})();
