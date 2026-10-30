// "ตึกโยก" cast drawn with rig v2 (rig2.js): a Bangkok condo on the Friday afternoon the tower sways.
//   rider    "คุณ" ~25, the food-delivery rider: green jacket with reflective bands and the app badge, black trousers, sneakers,
//            a full-face helmet with a dark visor (the face is never seen) · riderBag: the insulated delivery bag in the front hand
//   mew      มิว 10, room 2714: a bob with bangs and a yellow star clip, a yellow tee with a cat face, denim shorts, bare feet,
//            the orange whistle on a lanyard (draw at ~0.76 of an adult) · mewPhone (phone in hand) · mewCandle (candle + matches)
//   somsak   ลุงสมศักดิ์ 60, the condo guard: pale-blue uniform shirt with epaulettes, badge and a radio on the chest, navy trousers,
//            black boots, a peaked cap with a badge (brim at the brows), grey moustache
// Poses for this story (crouched under a table, hands over the head, holding a table leg) are declared here too.
(function () {
  const { LINE, dk, hi } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round"`;
  const Qk = (window.Qk = window.Qk || {});

  // ---------------- the rider ----------------
  // full-face helmet: the shell covers the hair and ears, the visor covers the eyes, the chin bar the mouth
  const helmet = (shell = "#2b3036", stripe = "#2fa45a") => `
    <path d="M-62,-556C-66,-628 -24,-656 4,-656C42,-656 72,-628 68,-556L66,-506Q62,-478 38,-472H-30Q-58,-478 -60,-506Z" fill="${shell}" ${ln(3)}/>
    <path d="M-50,-626Q4,-664 58,-626" stroke="${stripe}" stroke-width="12" fill="none" stroke-linecap="round"/>
    <path d="M-34,-640Q4,-656 40,-640" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".35"/>
    <path d="M-48,-584Q4,-604 56,-584L54,-528Q4,-512 -46,-528Z" fill="#141a20" ${ln(2.8)}/>
    <path d="M-36,-584Q4,-598 44,-584L42,-566Q4,-578 -34,-566Z" fill="#5a7488" opacity=".55"/>
    <path d="M30,-582L14,-530M42,-580L28,-532" stroke="#d8eef8" stroke-width="5" opacity=".35" stroke-linecap="round"/>
    <path d="M-30,-506H38M-24,-494H32" stroke="#14181c" stroke-width="3" opacity=".7"/>
    <ellipse cx="-58" cy="-556" rx="6" ry="10" fill="#1c2024"/><ellipse cx="64" cy="-556" rx="6" ry="10" fill="#1c2024"/>`;
  const riderPrint = `
    <path d="M0,-470V-300" stroke="#1e6e3c" stroke-width="3"/><path d="M-3,-470h6v8h-6z" fill="#c8c8c8"/>
    <path d="M-60,-400H-6M6,-400H60" stroke="#e8f0e8" stroke-width="9" opacity=".9"/><path d="M-60,-400H-6M6,-400H60" stroke="#9ab0a0" stroke-width="2" opacity=".6"/>
    <g transform="translate(-30,-444)"><circle r="15" fill="#fff4dc" ${ln(1.8)}/><path d="M-9,-1h18q-1,9 -9,10q-8,-1 -9,-10z" fill="#e2a92e" stroke="#2a2a2a" stroke-width="1.4"/><path d="M-4,-3l-2,-6M2,-3l1,-7" stroke="#2a2a2a" stroke-width="1.6"/></g>`;
  C.rider = { v2: {
    skin: "#c99068", iris: "#2a1a12", w: 1.04,
    hair: { c: "#1a1410", front: "" },
    top: { kind: "shirt", c: "#2fa45a", sleeve: "long", neck: "collar", collar: "#25874a", button: "#25874a" },
    print: riderPrint,
    bottom: { kind: "trousers", c: "#25282d" }, feet: { kind: "sneaker", c: "#2c2e33", sole: "#e8e6e0", lace: "#8a8e94" },
    faceTop: helmet(),
  } };
  // the insulated delivery bag carried in the front hand (palm at (0,118) of the hand group)
  Qk.deliveryBag = () => `<g transform="translate(0,118)"><path d="M-8,-4Q0,-26 8,-4" stroke="#1e1e1e" stroke-width="5" fill="none"/>
    <rect x="-46" y="0" width="92" height="96" rx="8" fill="#2fa45a" ${ln(2.6)}/><rect x="-46" y="0" width="92" height="22" rx="8" fill="#25874a"/>
    <circle cx="0" cy="54" r="18" fill="#fff4dc" ${ln(1.8)}/><path d="M-11,52h22q-1,11 -11,12q-10,-1 -11,-12z" fill="#e2a92e" stroke="#2a2a2a" stroke-width="1.4"/>
    <path d="M-36,90H36" stroke="#e8f0e8" stroke-width="5" opacity=".8"/></g>`;
  C.riderBag = { v2: C.rider.v2, hand: Qk.deliveryBag() };

  // ---------------- มิว ----------------
  // a bob: bangs over the brows in front, the rounded back of the bob behind (both follow the head)
  const bobFront = (h) => `
    <path d="M-50,-546C-58,-606 -20,-630 4,-630C34,-630 62,-606 54,-546Q50,-566 42,-572Q32,-562 20,-576Q8,-564 -4,-578Q-16,-564 -28,-576Q-38,-564 -46,-570Q-49,-560 -50,-546Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-618Q-36,-594 -28,-576M-2,-626Q-6,-600 -2,-580M26,-620Q32,-598 22,-578" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".75" stroke-linecap="round"/>
    <path d="M-34,-606Q-18,-620 2,-622M12,-622Q30,-618 40,-606" stroke="${h.sh}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>
    <path d="M-50,-546Q-56,-520 -52,-500Q-46,-506 -42,-520Z" fill="${h.c}" ${ln(2)}/><path d="M54,-546Q60,-520 56,-500Q50,-506 46,-520Z" fill="${h.c}" ${ln(2)}/>
    <g transform="translate(40,-600) rotate(18)"><path d="M0,-12L3.5,-4L12,-3.5L5.5,2L7.5,10.5L0,6L-7.5,10.5L-5.5,2L-12,-3.5L-3.5,-4Z" fill="#f6c935" stroke="#6a4a10" stroke-width="1.8"/></g>`;
  const bobBack = (h) => `<path d="M-62,-560C-70,-628 -24,-650 4,-650C36,-650 76,-628 66,-560L64,-500Q40,-488 4,-490Q-34,-488 -60,-500Z" fill="${dk(h.c, 0.12)}" ${ln()}/>`;
  const whistle = (y = -398) => `<path d="M-26,-488Q-30,-444 -14,${y - 8}M26,-488Q22,-444 6,${y - 8}" stroke="#e8682a" stroke-width="3.2" fill="none"/>
    <g transform="translate(-4,${y})"><path d="M-14,-6H10Q20,-6 20,6Q20,18 6,18Q-6,18 -8,8H-14Z" fill="#f47b20" ${ln(2)}/><rect x="-24" y="-6" width="12" height="9" rx="2" fill="#f47b20" ${ln(1.8)}/>
    <circle cx="6" cy="6" r="4" fill="#b8500e"/><path d="M-10,-2H8" stroke="#ffd0a8" stroke-width="2.4" opacity=".7"/></g>`;
  const catTee = `<g transform="translate(0,-400)"><path d="M-24,-14L-18,-30L-8,-18H8L18,-30L24,-14Q28,8 0,14Q-28,8 -24,-14Z" fill="#fff4e0" ${ln(2)}/>
    <circle cx="-9" cy="-6" r="3" fill="#2a1a12"/><circle cx="9" cy="-6" r="3" fill="#2a1a12"/><path d="M-3,1h6l-3,3z" fill="#e87a8a"/><path d="M-20,2h-10M-20,6h-9M20,2h10M20,6h9" stroke="#2a1a12" stroke-width="1.4"/></g>`;
  C.mew = { v2: {
    skin: "#e8b88e", iris: "#3a2216", lash: true, blush: 0.7, headScale: 1.2,
    hair: { c: "#24170f", s: "#0e0806", sh: "#6a4a38", front: (x) => bobFront(x.hair), back: (x) => bobBack(x.hair) },
    top: { kind: "tee", c: "#f2c230", sleeve: "short" },
    print: catTee,
    bottom: { kind: "shorts", c: "#4a6a9a" }, feet: { kind: "bare" },
    extra: whistle(),
  } };
  Qk.phone = () => `<g transform="translate(0,118) rotate(-8)"><rect x="-16" y="-30" width="32" height="58" rx="6" fill="#20242a" ${ln(2.2)}/><rect x="-12" y="-25" width="24" height="46" rx="3" fill="#7ac8f0"/><path d="M-8,-18h16M-8,-10h10" stroke="#fff" stroke-width="3" opacity=".7"/></g>`;
  Qk.candle = () => `<g transform="translate(0,118)"><rect x="-6" y="-58" width="12" height="62" rx="2" fill="#f4efe2" ${ln(2)}/><path d="M0,-58v-8" stroke="${LINE}" stroke-width="2"/>
    <rect x="10" y="-14" width="24" height="16" rx="2" fill="#c83a2a" ${ln(1.8)}/><path d="M12,-8h20" stroke="#f2d06a" stroke-width="3"/></g>`;
  C.mewPhone = { v2: C.mew.v2, hand: Qk.phone() };
  C.mewCandle = { v2: C.mew.v2, hand: Qk.candle() };

  // ---------------- ลุงสมศักดิ์ ----------------
  const cap = `<path d="M-54,-576C-58,-640 -20,-664 4,-664C32,-664 62,-642 58,-576Z" fill="#26324e" ${ln(2.8)}/>
    <path d="M-44,-640Q4,-660 50,-640" stroke="#3a4a6e" stroke-width="7" fill="none" opacity=".7"/>
    <path d="M-58,-582Q4,-560 64,-582L66,-570Q4,-544 -60,-570Z" fill="#141a2a" ${ln(2.6)}/>
    <g transform="translate(4,-616)"><path d="M0,-16L12,-8V6Q0,16 -12,6V-8Z" fill="#e2c25a" ${ln(1.8)}/><path d="M-5,-2h10M0,-8v12" stroke="#8a6a1a" stroke-width="2"/></g>`;
  C.somsak = { v2: {
    skin: "#b07a52", iris: "#2a1a12", blush: 0.2, bags: true, w: 1.1,
    hair: { c: "#a8a49c", s: "#6a665e", sh: "#d8d4cc", front: `<path d="M-50,-560Q-54,-576 -48,-582L-40,-560ZM52,-560Q56,-576 50,-582L42,-560Z" fill="#a8a49c" ${ln(1.6)}/>` },
    top: { kind: "shirt", c: "#a9c0d6", sleeve: "long", neck: "collar", collar: "#93abc4", button: "#e8eef4" },
    print: `<path d="M-64,-476L-40,-484L-38,-472L-62,-466ZM64,-476L40,-484L38,-472L62,-466Z" fill="#26324e" ${ln(1.6)}/>
      <g transform="translate(-30,-436)"><path d="M0,-12L10,-6V6Q0,14 -10,6V-6Z" fill="#e2c25a" ${ln(1.6)}/></g>
      <g transform="translate(34,-440)"><rect x="-10" y="-14" width="20" height="30" rx="3" fill="#1e1e22" ${ln(1.6)}/><path d="M6,-14V-34" stroke="#1e1e22" stroke-width="4" stroke-linecap="round"/><circle cx="0" cy="-4" r="3" fill="#e8443a"/></g>
      <path d="M-58,-310H58" stroke="#1e1e22" stroke-width="10"/><rect x="-8" y="-316" width="16" height="12" fill="#c8b06a"/>`,
    bottom: { kind: "trousers", c: "#26304a" }, feet: { kind: "boot", c: "#1c1c20" },
    face: `<path d="M-22,-512Q2,-498 26,-512Q2,-522 -22,-512Z" fill="#9a968e" ${ln(1.6)}/>`,
    faceTop: cap,
  } };

  // ---------------- poses ----------------
  // crouched under a table: knees up, body low, both hands over the head (ป้อง)
  Rig.MODES.duck = (u, o) => { const j = Math.sin(u * 31) * 0.8; return { ...Rig.MODES.crouch(u, o), uaF: -150 + j, faF: -112, uaB: 150 - j, faB: 112, torso: 26 + j * 0.3, head: -20, bodyY: 150 }; };
  // the same, the front hand reaching out to hold the table leg (เกาะ), the back hand still over the head
  Rig.MODES.duckHold = (u, o) => { const j = Math.sin(u * 31) * 0.8; return { ...Rig.MODES.crouch(u, o), uaF: -64 + j, faF: -18, uaB: 150 - j, faB: 112, torso: 24 + j * 0.3, head: -16, bodyY: 150 }; };
  // shaken: standing, arms out for balance, staggering
  Rig.MODES.stagger = (u, o) => { const s = Math.sin(u * 9), c = Math.sin(u * 5.3); return { ...Rig.MODES.idle(u, o), uaF: -62 + 10 * s, faF: -20, uaB: 58 - 10 * s, faB: 18, torso: 6 * c, head: -4 + 4 * s, thF: 8 * c, thB: -8 * c, rootR: 3 * c, bodyY: 6 }; };
  // pulling someone by the hand toward the camera's left (the front arm stretched out low)
  Rig.MODES.pullHand = (u, o) => { const s = Math.sin(u * 12); return { ...Rig.MODES.idle(u, o), uaF: -40 + 4 * s, faF: -6, uaB: 30, faB: -20, torso: -8, head: 6, thF: 14, shF: 10, thB: -12, bodyY: 4 }; };
  // the whistle blown with the front hand
  Rig.MODES.blow = (u, o) => ({ ...Rig.MODES.whistle(u, o), head: -8, torso: -3 });
})();

// ---------------- crouched under the table, in profile (the rig is front-on and too tall to fit under a 0.75 m table) ----------------
// Qk.duck(who, x, y, s, o): kneeling, bent forward, the head down, origin on the floor under the hips, facing left (o.flip faces right).
//   who "rider" | "mew" · o.arms "cover" (both hands over the back of the head) | "hold" (the front hand grips a table leg o.reach units ahead)
//   ids from o.id: #id (outer: move it), #id-b (body: tremble it), #id-arm (the reaching arm), #id-head
// About 230 units tall and 380 long at s 1 (0.6 m × 1 m): it fits under the table's 282-unit top.
(function () {
  const { LINE, dk, hi, shade } = Rig2;
  const Qk = window.Qk;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const P = {
    rider: { skin: "#c99068", top: "#2fa45a", band: "#e8f0e8", pants: "#25282d", shoe: "#2c2e33", head: (s) => `<path d="M-58,-6C-62,-62 -22,-82 10,-80C46,-78 66,-50 62,-6Q58,24 30,30H-34Q-58,22 -58,-6Z" fill="#2b3036" ${ln(3)}/>
        <path d="M-58,-6Q-58,26 -30,30L-26,4Q-44,-2 -50,-24Z" fill="#141a20" ${ln(2.4)}/><path d="M-44,-60Q4,-92 50,-56" stroke="#2fa45a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-30,-66Q0,-80 30,-70" stroke="#fff" stroke-width="5" fill="none" opacity=".3" stroke-linecap="round"/>` },
    mew: { skin: "#e8b88e", top: "#f2c230", band: null, pants: "#4a6a9a", shoe: null, head: (s) => `<path d="M-50,-4C-54,-56 -18,-74 8,-72C40,-70 60,-46 56,-4Q50,24 24,28H-28Q-50,22 -50,-4Z" fill="#24170f" ${ln(2.6)}/>
        <path d="M-50,-4Q-50,20 -30,26Q-34,4 -24,-6Q-40,-6 -50,-4Z" fill="#e8b88e" ${ln(2)}/><circle cx="-36" cy="6" r="3" fill="#2a1a12"/><g transform="translate(30,-50) rotate(18)"><path d="M0,-10L3,-3L10,-3L4,2L6,9L0,5L-6,9L-4,2L-10,-3L-3,-3Z" fill="#f6c935" stroke="#6a4a10" stroke-width="1.6"/></g>` },
  };
  Qk.duck = (who, x, y, s = 1, o = {}) => {
    const p = P[who], id = o.id || `dk${Math.floor(x)}`, fl = o.flip ? -1 : 1, reach = o.reach ?? 160;
    const skinS = shade(p.skin, 0.2);
    // back leg (behind), torso, head, arms; facing left: the head is at negative x
    const shin = `<path d="M-30,-8Q40,-16 120,-12L126,8Q40,10 -34,10Z" fill="${dk(p.pants, 0.08)}" ${ln()}/>` + (p.shoe ? `<path d="M110,-16Q146,-18 148,6L112,8Z" fill="${p.shoe}" ${ln(2.2)}/>` : `<path d="M112,-12Q140,-14 142,6L114,8Z" fill="${p.skin}" ${ln(2.2)}/>`);
    const thigh = `<path d="M-42,-4Q-46,-60 4,-118L58,-108Q34,-60 20,-6Z" fill="${p.pants}" ${ln()}/>`;
    const torso = `<path d="M70,-112C70,-170 30,-214 -40,-214C-98,-212 -136,-188 -142,-150C-132,-122 -96,-112 -60,-108C-20,-104 30,-90 70,-112Z" fill="${p.top}" ${ln()}/>
      <path d="M50,-120C20,-104 -20,-106 -60,-110" stroke="${shade(p.top, 0.3)}" stroke-width="4" fill="none" opacity=".6"/>${p.band ? `<path d="M10,-206Q-10,-150 0,-110" stroke="${p.band}" stroke-width="10" opacity=".85"/>` : ""}
      ${who === "mew" ? `<path d="M-120,-140Q-120,-96 -100,-84" stroke="#e8682a" stroke-width="3" fill="none"/><g transform="translate(-98,-78) rotate(60)"><path d="M-10,-5H8Q16,-5 16,4Q16,13 4,13Q-4,13 -6,6H-10Z" fill="#f47b20" ${ln(1.8)}/></g>` : ""}`;
    const head = `<g id="${id}-head" transform="translate(-170,-112) rotate(-28)">${p.head()}</g>`;
    const coverArm = (dx) => `<path d="M${-96 + dx},-196Q${-150 + dx},-226 ${-196 + dx},-196" stroke="${p.top}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M${-96 + dx},-196Q${-150 + dx},-226 ${-196 + dx},-196" stroke="${LINE}" stroke-width="34" fill="none" stroke-linecap="round" opacity=".18"/>
      <ellipse cx="${-204 + dx}" cy="-186" rx="20" ry="16" fill="${p.skin}" ${ln(2.2)}/>`;
    const holdArm = `<g id="${id}-arm"><path d="M-110,-160Q-180,-150 ${-150 - reach},-110" stroke="${p.top}" stroke-width="28" fill="none" stroke-linecap="round"/><path d="M-110,-160Q-180,-150 ${-150 - reach},-110" stroke="${LINE}" stroke-width="32" fill="none" stroke-linecap="round" opacity=".18"/>
      <ellipse cx="${-160 - reach}" cy="-106" rx="18" ry="22" fill="${p.skin}" ${ln(2.2)}/><path d="M${-170 - reach},-118v22M${-160 - reach},-122v26" stroke="${skinS}" stroke-width="2"/></g>`;
    const arms = o.arms === "hold" ? coverArm(0) + holdArm : coverArm(0) + coverArm(-18);
    const g = `<g id="${id}-b"><ellipse cx="0" cy="6" rx="170" ry="16" fill="#1a1010" opacity=".25"/>${shin}${thigh}${torso}${head}${arms}</g>`;
    return `<g transform="translate(${x},${y}) scale(${fl * s},${s})"><g id="${id}">${g}</g></g>`;
  };
  // the table seen from its long side, in the same room scale (front legs at G): for the side shots under the table
  Qk.povGrip = (o = {}) => `<g transform="rotate(${o.rot ?? -20})"><path d="M-70,90L-60,900H150L130,80Z" fill="#2fa45a" stroke="#2e2a26" stroke-width="4" stroke-linejoin="round"/>
    <path d="M-62,280H140M-58,500H144" stroke="#e8f0e8" stroke-width="14" opacity=".85"/><path d="M-66,110H134" stroke="#25874a" stroke-width="22"/>
    <path d="M-60,96Q-80,10 -20,-24Q30,-44 80,-24Q130,0 124,70Q118,110 70,112L-40,114Z" fill="#c99068" stroke="#2e2a26" stroke-width="4" stroke-linejoin="round"/>
    <path d="M-30,-18Q-40,30 -24,70M10,-30Q2,20 14,72M50,-26Q46,24 56,70" stroke="#9a6a48" stroke-width="3" fill="none"/></g>`;
})();

// your hand holding the delivery bag by its strap, from the bottom-right corner (first person); the fist is at (0,0)
(function () {
  const Qk = window.Qk, INK = "#2e2a26";
  Qk.povBag = (o = {}) => `<g transform="rotate(${o.rot ?? -10})">
    <path d="M-150,40Q-150,-30 -80,-36H80Q150,-30 150,40" stroke="#1e1e1e" stroke-width="22" fill="none" stroke-linecap="round"/>
    <g transform="translate(0,40)"><rect x="-210" y="0" width="420" height="420" rx="30" fill="#2fa45a" stroke="${INK}" stroke-width="6"/><rect x="-210" y="0" width="420" height="90" rx="30" fill="#25874a"/>
      <circle cx="0" cy="230" r="78" fill="#fff4dc" stroke="${INK}" stroke-width="5"/><path d="M-46,222h92q-4,46 -46,50q-42,-4 -46,-50z" fill="#e2a92e" stroke="#2a2a2a" stroke-width="3"/>
      <path d="M-22,214l-8,-24M8,214l4,-28" stroke="#2a2a2a" stroke-width="5"/><path d="M-170,380H170" stroke="#e8f0e8" stroke-width="16" opacity=".8"/></g>
    <path d="M60,-30L420,700H760L320,-60Z" fill="#2fa45a" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/><path d="M170,160L560,140M250,340L640,320" stroke="#e8f0e8" stroke-width="20" opacity=".85"/>
    <path d="M90,-20L330,-70" stroke="#25874a" stroke-width="40"/>
    <path d="M-60,-60Q-70,-120 -10,-130Q60,-140 110,-110Q150,-80 130,-30Q110,0 60,0L-40,0Q-70,-10 -60,-60Z" fill="#c99068" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
    <path d="M-30,-100Q-34,-60 -24,-14M14,-110Q8,-60 20,-10M56,-104Q54,-60 64,-14" stroke="#9a6a48" stroke-width="4" fill="none"/><path d="M-40,-36Q-62,-40 -66,-64" stroke="#9a6a48" stroke-width="4" fill="none"/></g>`;
})();
