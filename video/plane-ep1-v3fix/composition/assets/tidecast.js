// "ทะเลลด" cast drawn with rig v2 (rig2.js): a family New Year at grandma's beach shop in บ้านแหลมหอย on the Andaman coast.
//   june       จูน 16: long black hair with pink-dyed ends (a shell clip on the right), an oversized lilac tee with a sun-and-wave
//              print, denim shorts, pink sandals, a pink scrunchie on the wrist
//              · juneStick (phone on a selfie stick in the hand; pose "film") · junePhone (phone in the hand; poses phoneLook / selfie)
//   tang       ตังค์ 10 (draw at ~0.76 of an adult): spiky hair, a plaster on the cheek, a yellow tank top with a blue fish, red swim
//              shorts, bare feet · tangRing (the yellow duck swim ring round the waist; pose "ringArms") · tangBucket (the blue bucket
//              of fish in the hand) · tangRingBucket (both)
//   yaiTide    ยาย 65: grey hair pulled back into a bun with a gold pin, gold earrings, a cream blouse with hibiscus, a work apron,
//              a blue batik sarong, sandals · yaiTidePhoto (holding the framed old photo)
//   taJun      ตาจุ่น 68: weathered dark skin, a balding head with white hair and stubble, a faded orange life vest over a rolled-up
//              teal shirt, a checked ผ้าขาวม้า round the neck, loose fisherman's trousers rolled to the calf, bare feet
//              · taJunConch (the conch hanging in the fist; poses pointUp / idle) · taJunBlow (the conch at the lips; pose blowConch)
// Poses: film (selfie stick held up and out) · pointUp (to the hill) · blowConch (the front hand at the lips, elbow up) · ringArms (arms resting
//   on the swim ring) · cheer (both arms up, bouncing) · shadeEyes (a hand over the brows, looking out to sea) · wagFinger (a warning)
//   · scoop (bent forward, reaching down to the sand) · holdPhoto (the framed photo shown in front of the apron, the front forearm across the body; use yaiTidePhoto, oneHand the back)
// Props (TideCast.PROP, also Tide.PROP): phoneStick() phone() bucket() conch(rot, skin, mirror) photo(rot) — hand props at the palm
//   (0,118); rig v2 puts a cast's hand prop in both fists, so every prop variant here sets keep: "F" | "B" (the fist that holds it;
//   taJunConch keeps it in the back fist so the front one can point)
// Spec hooks added to rig v2 here: v2.skirt (SVG over both legs under the pelvis: ยาย's batik sarong) and v2.legs(side) ->
//   { thigh, shin } laid over each leg (ตาจุ่น's rolled trousers)
// Scene pieces (return SVG; place them anywhere):
//   TideCast.duckRing(x, y, s, o)  the duck ring on its own (floating: o.water adds the waterline, o.id wraps it for tweening)
//   TideCast.photo(x, y, s, o)     the clue: an old framed photo of two young fishermen on a longtail boat, ตาจุ่น in a headband
//                                  and ตา in a cap (o.id, o.glass, o.year default ๒๕๒๕, o.rot)
//   TideCast.clipping(x, y, s, o)  the clue: a yellowed clipping of ๒๗ ธ.ค. ๔๗, a fisherman carrying a young woman out of the water
//                                  (o.title, o.date, o.caption, o.id, o.rot)
(function () {
  const { LINE, dk, hi, shade } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const Tide = (window.Tide = window.Tide || {});
  const TC = (window.TideCast = window.TideCast || {});

  Sets.DEFS += `
    <linearGradient id="tdJuneHair" gradientUnits="userSpaceOnUse" x1="0" y1="-540" x2="0" y2="-424"><stop offset="0" stop-color="#1d1418"/><stop offset=".48" stop-color="#2c1822"/><stop offset=".7" stop-color="#b8407a"/><stop offset="1" stop-color="#ff8cbc"/></linearGradient>
    <linearGradient id="tdJuneHairB" gradientUnits="userSpaceOnUse" x1="0" y1="-520" x2="0" y2="-392"><stop offset="0" stop-color="#170f13"/><stop offset=".45" stop-color="#22131b"/><stop offset=".72" stop-color="#a83a6c"/><stop offset="1" stop-color="#f27aae"/></linearGradient>
    <linearGradient id="tdVest" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f0a058"/><stop offset=".5" stop-color="#e8863c"/><stop offset="1" stop-color="#c2652a"/></linearGradient>
    <linearGradient id="tdRing" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2a0"/><stop offset=".45" stop-color="#ffd23a"/><stop offset="1" stop-color="#d89a12"/></linearGradient>
    <linearGradient id="tdRingBack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8b420"/><stop offset="1" stop-color="#b47c0c"/></linearGradient>
    <linearGradient id="tdBucket" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a86d8"/><stop offset=".4" stop-color="#5aa8f0"/><stop offset="1" stop-color="#2a62b0"/></linearGradient>
    <linearGradient id="tdConch" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff4e4"/><stop offset=".55" stop-color="#f2d6b4"/><stop offset="1" stop-color="#c89a72"/></linearGradient>
    <radialGradient id="tdConchIn" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#ffd2d8"/><stop offset=".7" stop-color="#f08a9a"/><stop offset="1" stop-color="#c8566a"/></radialGradient>
    <linearGradient id="tdSepia" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8d2a8"/><stop offset=".55" stop-color="#c8a878"/><stop offset="1" stop-color="#a88458"/></linearGradient>
    <linearGradient id="tdFrame" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a8723e"/><stop offset=".5" stop-color="#7a4a22"/><stop offset="1" stop-color="#4e2c12"/></linearGradient>
    <linearGradient id="tdNews" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2e6c4"/><stop offset="1" stop-color="#d8c494"/></linearGradient>
    <linearGradient id="tdGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".35" stop-color="#fff" stop-opacity=".06"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset=".72" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <pattern id="tdBatik" width="44" height="44" patternUnits="userSpaceOnUse"><rect width="44" height="44" fill="#1f5576"/>
      <path d="M-2,30Q10,22 22,30T46,30" stroke="#3a9a8a" stroke-width="2.4" fill="none"/><path d="M6,28q-7,-8 0,-13q7,5 0,13z" fill="#3a9a8a"/><path d="M30,30q9,-3 10,-12q-9,1 -10,12z" fill="#3a9a8a"/>
      <g transform="translate(14,13)">${[0, 72, 144, 216, 288].map((a) => `<ellipse cy="-5" rx="3.8" ry="5.4" fill="#f29a3a" transform="rotate(${a})"/>`).join("")}<circle r="3" fill="#ffe08a" stroke="#8a3a1a" stroke-width="1"/></g>
      <g transform="translate(33,37)">${[0, 90, 180, 270].map((a) => `<ellipse cy="-3.4" rx="2.4" ry="3.6" fill="#f2e2c0" transform="rotate(${a})"/>`).join("")}<circle r="1.8" fill="#d8503a"/></g>
      <g fill="#cfe6e0" opacity=".7"><circle cx="4" cy="5" r="1.1"/><circle cx="28" cy="6" r="1.1"/><circle cx="40" cy="14" r="1.1"/><circle cx="22" cy="41" r="1.1"/><circle cx="5" cy="40" r="1.1"/><circle cx="26" cy="20" r=".9"/></g></pattern>
    <clipPath id="tdSarongClip"><path d="M-57,-336Q-62,-250 -55,-150L-50,-38Q-26,-31 0,-34Q26,-31 50,-38L55,-150Q62,-250 57,-336Z"/></clipPath>
    <linearGradient id="tdSkirt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a1a2a" stop-opacity=".38"/><stop offset=".28" stop-color="#0a1a2a" stop-opacity="0"/><stop offset=".72" stop-color="#fff" stop-opacity="0"/><stop offset=".9" stop-color="#fff" stop-opacity=".14"/><stop offset="1" stop-color="#0a1a2a" stop-opacity=".22"/></linearGradient>
    <pattern id="tdCheck" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="#c8402e"/><rect width="12" height="24" fill="#2e5a9a" opacity=".55"/><rect width="24" height="12" fill="#2e5a9a" opacity=".45"/><path d="M0,6H24M6,0V24" stroke="#f4e6c8" stroke-width="1.6" opacity=".55"/></pattern>`;

  // rig2 has no long skirt and no rolled trousers: a spec may add V.skirt (SVG laid over both legs, under the pelvis and the
  // torso, so the feet step out under the hem) and V.legs(side) -> { thigh, shin } (SVG laid over each thigh / shin after the build).
  // P.keep "F" | "B" leaves the hand prop in that fist only
  const build0 = Rig.build;
  Rig.build = (parent, id, P) => {
    const el = build0(parent, id, P), V = P && P.v2, other = P && P.keep && document.getElementById(`${id}-hand${P.keep === "F" ? "B" : "F"}`);
    if (other) [...other.children].forEach((c) => { if (!c.id) c.remove(); });
    if (V && V.legs) ["B", "F"].forEach((s) => {
      const o = V.legs(s), th = document.querySelector(`#${id}-th${s} > g`), sh = document.getElementById(`${id}-sh${s}`);
      if (th && o.thigh) th.insertAdjacentHTML("beforeend", o.thigh);
      if (sh && o.shin) sh.insertAdjacentHTML("beforeend", o.shin);
    });
    const thF = V && V.skirt && document.getElementById(`${id}-thF`);
    if (thF) thF.parentNode.insertAdjacentHTML("afterend", typeof V.skirt === "function" ? V.skirt() : V.skirt);
    return el;
  };

  // ---------------- จูน ----------------
  // bangs swept to her right, side locks to the shoulders; the dyed ends come from the gradient (same coordinates as the head)
  const juneFront = (h) => `
    <path d="M-50,-560C-62,-524 -66,-480 -60,-432Q-50,-440 -44,-466C-41,-500 -41,-540 -41,-566Z" fill="url(#tdJuneHair)" ${ln()}/>
    <path d="M50,-566C61,-530 65,-488 62,-446Q60,-428 67,-412Q47,-416 46,-450C43,-488 43,-530 42,-566Z" fill="url(#tdJuneHair)" ${ln()}/>
    <path d="M-50,-546C-60,-612 -20,-632 4,-630C36,-629 62,-606 53,-546C50,-560 46,-568 40,-568Q24,-574 6,-596Q-4,-574 -18,-580Q-30,-570 -40,-576Q-47,-564 -50,-546Z" fill="${h.c}" ${ln()}/>
    <path d="M6,-596Q22,-572 40,-568Q50,-564 52,-552Q44,-560 30,-560Q14,-566 6,-596Z" fill="${dk(h.c, 0.2)}" opacity=".6"/>
    <path d="M-34,-618Q-44,-592 -38,-576M-8,-626Q-18,-600 -14,-580M22,-622Q14,-604 8,-598M55,-534Q59,-490 58,-452M-51,-530Q-56,-490 -54,-450" stroke="${h.s}" stroke-width="2.4" fill="none" opacity=".7" stroke-linecap="round"/>
    <path d="M-36,-602Q-26,-614 -12,-620M2,-622Q14,-624 26,-618" stroke="#8a6a8a" stroke-width="5" fill="none" stroke-linecap="round" opacity=".55"/>
    <path d="M-28,-608Q-22,-614 -14,-617" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".35"/>
    <g transform="translate(-44,-596) rotate(-30)"><path d="M0,10L-14,-4Q-12,-16 0,-18Q12,-16 14,-4Z" fill="#fff0f2" ${ln(2)}/><path d="M0,10L-9,-12M0,10L-3,-17M0,10L3,-17M0,10L9,-12" stroke="#f08aa8" stroke-width="2" stroke-linecap="round"/><path d="M-5,10h10" stroke="#f08aa8" stroke-width="3"/></g>`;
  const juneBack = () => `
    <path d="M-58,-584C-72,-532 -84,-468 -80,-398Q-66,-386 -52,-398Q-36,-388 -18,-396L18,-396Q36,-388 52,-398Q68,-386 82,-398C86,-468 74,-532 62,-584C52,-634 -48,-634 -58,-584Z" fill="url(#tdJuneHairB)" ${ln()}/>
    <path d="M-66,-540Q-74,-476 -70,-408M68,-540Q76,-476 72,-408M-34,-560Q-40,-480 -34,-404M34,-560Q40,-480 34,-404" stroke="#0e080b" stroke-width="2.6" fill="none" opacity=".6"/>`;
  const sunWave = `<g transform="translate(0,-404)"><path d="M-30,6A30,30 0 0 1 30,6Z" fill="#ffb84a" ${ln(2.2)}/><path d="M-22,-10l-8,-10M0,-26v-12M22,-10l8,-10" stroke="#ff9a3a" stroke-width="3.4" stroke-linecap="round"/>
    <path d="M-40,8q10,-8 20,0t20,0t20,0t20,0" stroke="#2fa0b8" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M-34,20q10,-8 20,0t20,0t20,0" stroke="#2fa0b8" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/></g>`;
  C.june = { v2: {
    skin: "#ebc19c", iris: "#3a2016", lash: true, blush: 0.75, lip: "#d0606a", w: 1.06,
    hair: { c: "#1d1418", s: "#0c070a", sh: "#7a5a72", front: (x) => juneFront(x.hair), back: () => juneBack() },
    top: { kind: "tee", c: "#b8a4ea", sleeve: "elbow", trim: "#a08ad8" },
    print: sunWave,
    bottom: { kind: "shorts", c: "#6e94c9" }, feet: { kind: "sandal", c: "#ec6aa0" },
    wristband: "#ff7eb0",
  } };

  // ---------------- ตังค์ ----------------
  const spiky = (h) => `
    <path d="M-47,-552C-52,-598 -28,-620 2,-620C30,-620 54,-600 49,-552Q46,-570 40,-576L46,-606L30,-590L28,-628L13,-598L2,-636L-9,-600L-24,-630L-28,-594L-44,-610L-40,-578Q-45,-568 -47,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-44,-556v18M48,-556v16" stroke="${h.c}" stroke-width="6" stroke-linecap="round"/>
    <path d="M-22,-612L-26,-592M2,-626L-1,-600M26,-618L22,-594" stroke="${h.sh}" stroke-width="3" opacity=".6" stroke-linecap="round"/>
    <path d="M-30,-596Q2,-612 34,-596" stroke="${h.sh}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".45"/>`;
  const fishTank = `<g transform="translate(-4,-392)"><path d="M-26,0Q-6,-20 18,0Q-6,20 -26,0Z" fill="#3a8ad8" ${ln(2.2)}/><path d="M18,0L32,-12V12Z" fill="#3a8ad8" ${ln(2.2)}/>
    <circle cx="-14" cy="-3" r="4" fill="#fff" stroke="${LINE}" stroke-width="1.4"/><circle cx="-13" cy="-3" r="1.8" fill="${LINE}"/><path d="M-2,-8q4,8 0,16M6,-8q4,8 0,16" stroke="#a8d8ff" stroke-width="2" fill="none"/>
    <circle cx="-34" cy="-14" r="3" fill="none" stroke="#a8d8ff" stroke-width="2"/><circle cx="-40" cy="-24" r="2" fill="none" stroke="#a8d8ff" stroke-width="1.6"/></g>`;
  const plaster = `<g transform="translate(-30,-526) rotate(-24)"><rect x="-13" y="-6" width="26" height="12" rx="5" fill="#f4d2a8" ${ln(1.6)}/><rect x="-5" y="-4" width="10" height="8" rx="2" fill="#e8b88a"/>
    <circle cx="-9" cy="-2" r=".9" fill="#c89a6a"/><circle cx="9" cy="2" r=".9" fill="#c89a6a"/></g>`;
  const tangV2 = {
    skin: "#d49c6c", iris: "#2e1c12", blush: 0.65, headScale: 1.2, w: 0.92, limb: 0.92,
    hair: { c: "#16100c", s: "#060404", sh: "#5a4a40", front: (x) => spiky(x.hair) },
    top: { kind: "tank", c: "#f6c832", sleeve: "none" },
    print: fishTank,
    bottom: { kind: "shorts", c: "#e2483c" }, feet: { kind: "bare" },
    face: plaster,
  };
  C.tang = { v2: tangV2 };
  // the duck swim ring round the waist: the back of the ring shows beside the hips, the front crosses the belly, the duck head on the front
  const ringWaist = `
    <path d="M-104,-334Q-104,-370 -62,-376L-60,-344Q-84,-342 -86,-330Z" fill="url(#tdRingBack)" ${ln(2.4)}/><path d="M104,-334Q104,-370 62,-376L60,-344Q84,-342 86,-330Z" fill="url(#tdRingBack)" ${ln(2.4)}/>
    <path d="M-106,-336Q-106,-292 0,-284Q106,-292 106,-336Q104,-310 60,-318Q0,-326 -60,-318Q-104,-310 -106,-336Z" fill="#d89a12" ${ln(2.4)}/>
    <path d="M-106,-336Q-108,-300 -60,-290Q0,-280 60,-290Q108,-300 106,-336Q108,-360 60,-352Q0,-344 -60,-352Q-108,-360 -106,-336Z" fill="url(#tdRing)" ${ln(2.8)}/>
    <path d="M-86,-342Q-40,-334 0,-334M30,-334Q70,-336 92,-344" stroke="#fffbe0" stroke-width="5" fill="none" opacity=".8" stroke-linecap="round"/>
    <path d="M-70,-300Q0,-288 70,-300" stroke="#b47c0c" stroke-width="3" fill="none" opacity=".5"/>
    <g transform="translate(40,-332)"><path d="M-14,4Q-22,-28 -2,-44Q20,-56 30,-36Q36,-22 26,-12Q20,0 14,6Z" fill="url(#tdRing)" ${ln(2.6)}/>
      <path d="M26,-30Q46,-34 50,-26Q46,-18 28,-20Z" fill="#ff8a2a" ${ln(2.2)}/><path d="M28,-25H48" stroke="#c8561a" stroke-width="1.8"/>
      <circle cx="16" cy="-36" r="4.6" fill="#fff" stroke="${LINE}" stroke-width="1.6"/><circle cx="17.5" cy="-36" r="2.4" fill="${LINE}"/><circle cx="16" cy="-37.6" r=".9" fill="#fff"/>
      <path d="M-8,-30Q0,-44 12,-46" stroke="#fffbe0" stroke-width="3.4" fill="none" opacity=".75" stroke-linecap="round"/>
      <ellipse cx="6" cy="-24" rx="5" ry="3" fill="#ff9aa0" opacity=".55"/></g>`;
  C.tangRing = { v2: { ...tangV2, extra: ringWaist } };

  // ---------------- ยาย ----------------
  const yaiFront = (h) => `
    <path d="M-47,-550C-51,-606 -16,-624 4,-624C30,-623 54,-604 49,-550Q46,-572 34,-586Q18,-594 4,-588Q-12,-596 -28,-588Q-42,-576 -47,-550Z" fill="${h.c}" ${ln()}/>
    <path d="M4,-622Q2,-606 4,-590M-12,-618Q-22,-600 -34,-584M18,-618Q30,-602 40,-584M-26,-610Q-36,-596 -42,-576M32,-612Q42,-598 46,-578" stroke="${h.s}" stroke-width="2.2" fill="none" opacity=".7"/>
    <path d="M-30,-610Q4,-626 36,-608" stroke="${h.sh}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".55"/>`;
  const yaiBun = (h) => `<circle cx="26" cy="-626" r="25" fill="${dk(h.c, 0.06)}" ${ln()}/><path d="M10,-634q14,-12 30,-4M8,-620q18,-6 36,0M14,-608q12,6 26,0" stroke="${h.s}" stroke-width="2.4" fill="none"/>
    <path d="M52,-650L-4,-604" stroke="#d8a83a" stroke-width="5" stroke-linecap="round"/><circle cx="52" cy="-650" r="6" fill="#f2c84a" ${ln(1.8)}/><circle cx="50" cy="-652" r="2" fill="#fff" opacity=".7"/>`;
  const hibiscus = (x, y, s = 1, c = "#e2483c") => `<g transform="translate(${x},${y}) scale(${s})">${[0, 72, 144, 216, 288].map((a) => `<ellipse cx="0" cy="-7" rx="5.4" ry="7.6" fill="${c}" transform="rotate(${a})"/>`).join("")}<circle r="3" fill="#ffd23a"/></g>`;
  const blouseFlowers = `${[[-36, -450, 1], [20, -428, 0.9], [-12, -380, 1], [40, -360, 0.85], [-44, -330, 0.8], [8, -322, 0.9]].map(([x, y, s], k) => `<path d="M${x - 10},${y + 6}q-8,4 -12,12M${x + 9},${y + 8}q8,2 12,10" stroke="#2f8a6a" stroke-width="3" fill="none" stroke-linecap="round"/>` + hibiscus(x, y, s, k % 2 ? "#e2483c" : "#f07a4a")).join("")}`;
  const apron = `<path d="M-60,-346Q0,-338 60,-346L64,-170Q0,-160 -64,-170Z" fill="#ece2cf" ${ln(2.6)}/><path d="M-60,-346Q0,-338 60,-346L61,-330Q0,-322 -61,-330Z" fill="#d8ccb2"/>
    <path d="M-36,-262H34L32,-212Q0,-206 -34,-212Z" fill="#e2d6be" ${ln(2)}/><path d="M-2,-262V-210" stroke="#b8aa8e" stroke-width="2"/>
    <path d="M-54,-300q10,30 4,60M48,-296q-8,40 0,70" stroke="#c8bba0" stroke-width="2.4" fill="none" opacity=".7"/><circle cx="22" cy="-200" r="7" fill="#c8a878" opacity=".35"/><circle cx="-30" cy="-280" r="5" fill="#c8a878" opacity=".3"/>
    <path d="M-62,-340Q-80,-324 -84,-300M62,-340Q78,-326 80,-306" stroke="#d8ccb2" stroke-width="7" fill="none" stroke-linecap="round"/>`;
  const tumpal = Array.from({ length: 9 }, (_, k) => `<path d="M${-54 + k * 12},-52L${-48 + k * 12},-69L${-42 + k * 12},-52Z" fill="#c4442a"/>`).join("");
  const yaiSarong = `<g><path d="M-57,-336Q-62,-250 -55,-150L-50,-38Q-26,-31 0,-34Q26,-31 50,-38L55,-150Q62,-250 57,-336Z" fill="url(#tdBatik)" ${ln(2.6)}/>
    <g clip-path="url(#tdSarongClip)"><rect x="-64" y="-72" width="128" height="20" fill="#e8b84a"/>${tumpal}<path d="M-64,-72H64M-64,-52H64" stroke="#c4442a" stroke-width="3"/>
      <rect x="-64" y="-52" width="128" height="20" fill="#173f58"/><path d="M-60,-44h120" stroke="#cfe6e0" stroke-width="2" stroke-dasharray="2 6" opacity=".7"/>
      <path d="M16,-336L24,-30H34L24,-336Z" fill="#06121c" opacity=".22"/><path d="M16,-336L24,-30" stroke="${LINE}" stroke-width="2.2"/>
      <path d="M-34,-150q-4,50 2,108M40,-160q4,60 -2,118" stroke="#0a2436" stroke-width="2.2" fill="none" opacity=".45"/></g>
    <path d="M-57,-336Q-62,-250 -55,-150L-50,-38Q-26,-31 0,-34Q26,-31 50,-38L55,-150Q62,-250 57,-336Z" fill="url(#tdSkirt)"/></g>`;
  const earrings = `<g fill="none" stroke="#e8b830" stroke-width="3"><circle cx="-50" cy="-526" r="6"/><circle cx="54" cy="-526" r="6"/></g><circle cx="-53" cy="-530" r="1.6" fill="#fff"/><circle cx="51" cy="-530" r="1.6" fill="#fff"/>`;
  const yaiV2 = {
    skin: "#c8946a", iris: "#3e2a1e", blush: 0.4, lip: "#a8443a",
    hair: { c: "#c9c4bc", s: "#8f8a84", sh: "#f2eee6", front: (x) => yaiFront(x.hair), back: (x) => yaiBun(x.hair) },
    top: { kind: "blouse", c: "#f4e6cc", sleeve: "elbow", lace: true, trim: "#d8c8a4" },
    print: blouseFlowers,
    bottom: { kind: "sarong", c: "#1f5576", band: "#173f58", band2: "#173f58" }, feet: { kind: "sandal", c: "#5a3a22" },
    skirt: yaiSarong, extra: apron,
    face: `<path d="M-22,-596q10,-3 20,0M-16,-588q8,-2 16,0M-34,-552l-7,-3M-34,-546l-7,1M38,-552l7,-3M38,-546l7,1M-14,-532q-7,10 -3,19M24,-532q7,10 3,19" stroke="#8a6448" stroke-width="2" fill="none" stroke-linecap="round" opacity=".8"/>${earrings}`,
  };
  C.yaiTide = { v2: yaiV2 };

  // ---------------- ตาจุ่น ----------------
  const junHair = (h) => `
    <path d="M-47,-556C-50,-580 -46,-596 -38,-604Q-44,-584 -42,-562ZM49,-556C52,-580 48,-596 40,-604Q46,-584 44,-562Z" fill="${h.c}" ${ln(2)}/>
    <path d="M-44,-572q-4,10 -2,20M46,-572q4,10 2,20" stroke="${h.s}" stroke-width="2" fill="none"/>
    <path d="M-30,-608Q2,-620 32,-608" stroke="#fff" stroke-width="5" fill="none" opacity=".18" stroke-linecap="round"/>
    <path d="M-26,-598q12,-4 22,0M6,-600q12,-4 22,0" stroke="#5a3418" stroke-width="2" fill="none" opacity=".45" stroke-linecap="round"/>`;
  const stubble = `<g fill="#ece8de" opacity=".85">${[[-34, -520], [-28, -511], [-20, -505], [-11, -500], [0, -498], [11, -499], [21, -503], [30, -509], [37, -517], [-24, -518], [-14, -512], [-4, -508], [8, -508], [18, -512], [28, -518], [-8, -524], [4, -523], [16, -524], [-30, -530], [36, -528]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.7"/>`).join("")}</g>
    <path d="M-14,-534q-8,12 -4,22M24,-534q8,12 4,22M-38,-552l-8,-3M-38,-545l-8,1M42,-552l8,-3M42,-545l8,1M-24,-590q12,-4 24,0" stroke="#4e2c14" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".75"/>
    <path d="M30,-584q6,6 4,14" stroke="#c89a72" stroke-width="2" fill="none" opacity=".6"/>`;
  const vest = `
    <path d="M-52,-488L-22,-484L-14,-430L-18,-306Q-44,-300 -70,-306L-68,-448Q-66,-476 -52,-488Z" fill="url(#tdVest)" ${ln(2.8)}/>
    <path d="M52,-488L22,-484L14,-430L18,-306Q44,-300 70,-306L68,-448Q66,-476 52,-488Z" fill="url(#tdVest)" ${ln(2.8)}/>
    <path d="M-68,-420H-16M16,-420H68M-70,-350H-17M17,-350H70" stroke="#d8d4c8" stroke-width="9" opacity=".75"/><path d="M-68,-420H-16M16,-420H68M-70,-350H-17M17,-350H70" stroke="#9a968a" stroke-width="2" opacity=".5"/>
    <path d="M-17,-404H17M-17,-334H17" stroke="#1e2228" stroke-width="6"/><rect x="-8" y="-411" width="16" height="14" rx="3" fill="#2a2e34" stroke="${LINE}" stroke-width="1.8"/><rect x="-8" y="-341" width="16" height="14" rx="3" fill="#2a2e34" stroke="${LINE}" stroke-width="1.8"/>
    <path d="M-60,-460Q-54,-400 -60,-330M58,-460Q54,-400 60,-330" stroke="#a8541c" stroke-width="2.6" fill="none" opacity=".55"/>
    <path d="M-50,-470Q-40,-474 -30,-470" stroke="#ffd0a0" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/>
    <path d="M-62,-320l6,-4M44,-386l8,-2M-46,-380l5,3" stroke="#f4e2c8" stroke-width="3" opacity=".5" stroke-linecap="round"/>`;
  const pakama = `<path d="M-42,-492Q0,-466 44,-492L48,-478Q0,-446 -46,-478Z" fill="url(#tdCheck)" ${ln(2.2)}/><path d="M30,-484Q40,-440 34,-396L52,-396Q56,-444 46,-486Z" fill="url(#tdCheck)" ${ln(2.2)}/>
    <path d="M34,-396h18" stroke="#f4e6c8" stroke-width="3" stroke-dasharray="3 3"/>`;
  const rolled = (c, k = 1) => (side) => {
    const cc = side === "B" ? dk(c, 0.1) : c, cf = hi(cc, 0.16), a = 46 * k / 2, b = 36 * k / 2, s0 = 35 * k / 2;
    return {
      thigh: Rig2.paint(Rig2.limbD(152, 2 * a + 12, 2 * b + 14), cc, { ao: true }) +
        `<path d="M${-a + 8},26q8,44 2,96M${a - 6},54q-6,34 -2,80" stroke="${dk(cc, 0.3)}" stroke-width="2.2" fill="none" opacity=".55"/>`,
      shin: Rig2.paint(`M${-s0 - 6},-8Q0,-14 ${s0 + 6},-8L${s0 + 9},66H${-s0 - 9}Z`, cc) +
        `<path d="M${-s0 - 11},60Q0,53 ${s0 + 11},60L${s0 + 10},80Q0,87 ${-s0 - 10},80Z" fill="${cf}" ${ln(2.4)}/>` +
        `<path d="M${-s0 - 9},70Q0,65 ${s0 + 9},70" stroke="${dk(cf, 0.28)}" stroke-width="2" fill="none"/><path d="M${-s0 - 6},62Q-4,58 ${s0 - 2},60" stroke="#fff" stroke-width="2" fill="none" opacity=".25"/>`,
    };
  };
  const junV2 = {
    skin: "#8a5a3a", iris: "#2a1a12", blush: 0.12, bags: true, w: 0.96, limb: 0.9, brow: "#ece8de",
    hair: { c: "#ece8de", s: "#a8a49c", sh: "#ffffff", front: (x) => junHair(x.hair) },
    top: { kind: "shirt", c: "#6f8e90", sleeve: "elbow", neck: "collar", collar: "#5e7c7e", button: "#d8d4c8", trim: "#5e7c7e" },
    bottom: { kind: "shorts", c: "#3c404c" }, feet: { kind: "bare" }, legs: rolled("#3c404c", 0.9),
    extra: vest + pakama,
    face: stubble,
  };
  C.taJun = { v2: junV2 };

  // ---------------- props (in the hand: the palm is at (0,118) of the hand group) ----------------
  // the selfie stick runs on along the forearm past the fist, the phone (its pink back to us) clamped at the end
  const phoneStick = () => `<g transform="translate(0,118)">
    <path d="M0,10V250" stroke="${LINE}" stroke-width="11" stroke-linecap="round"/><path d="M0,10V250" stroke="#b8c2ca" stroke-width="6" stroke-linecap="round"/>
    <path d="M0,70V74M0,140V144M0,200V204" stroke="#6a747c" stroke-width="7"/><path d="M-1.5,20V240" stroke="#fff" stroke-width="1.6" opacity=".6"/>
    <rect x="-9" y="-14" width="18" height="40" rx="6" fill="#2a2a30" ${ln(2.2)}/><circle cx="0" cy="-2" r="3" fill="#ec6aa0"/>
    <g transform="translate(0,262)"><rect x="-14" y="-10" width="28" height="18" rx="4" fill="#3a3e44" ${ln(2)}/>
      <rect x="-30" y="2" width="60" height="104" rx="11" fill="#ff8ab8" ${ln(2.6)}/><rect x="-30" y="2" width="60" height="104" rx="11" fill="url(#r2Cyl)"/>
      <rect x="-20" y="12" width="22" height="30" rx="7" fill="#2a2a30" ${ln(1.8)}/><circle cx="-13" cy="20" r="4.4" fill="#4a6a8a" stroke="#111" stroke-width="1.4"/><circle cx="-13" cy="34" r="4.4" fill="#4a6a8a" stroke="#111" stroke-width="1.4"/>
      <circle cx="-3" cy="27" r="2.6" fill="#fff6c8"/><path d="M14,70q6,-8 0,-14q-6,6 0,14z" fill="#fff" opacity=".7"/></g></g>`;
  const phone = () => `<g transform="translate(0,118) rotate(-8)"><rect x="-17" y="-32" width="34" height="62" rx="7" fill="#ff8ab8" ${ln(2.2)}/><rect x="-13" y="-27" width="26" height="50" rx="4" fill="#26303a"/>
    <path d="M-9,-20h18M-9,-12h12" stroke="#7ac8f0" stroke-width="3" opacity=".8"/><circle cx="20" cy="22" r="5" fill="#fff2f4" ${ln(1.4)}/></g>`;
  const bucket = () => `<g transform="translate(0,118)"><path d="M-30,30Q0,-34 30,30" stroke="${LINE}" stroke-width="5" fill="none"/><path d="M-30,30Q0,-34 30,30" stroke="#e8eef4" stroke-width="2.4" fill="none"/>
    <g transform="translate(0,34)"><path d="M-34,0H34L28,70Q0,78 -28,70Z" fill="url(#tdBucket)" ${ln(2.6)}/><ellipse cx="0" cy="0" rx="34" ry="8" fill="#1e4a8a" ${ln(2.4)}/>
      <path d="M-14,-2Q-24,-26 -12,-34L-6,-20Z" fill="#9ab8c8" ${ln(1.8)}/><path d="M8,-2Q20,-30 10,-38L2,-22Z" fill="#c8b45a" ${ln(1.8)}/>
      <path d="M-34,0H34" stroke="#fff" stroke-width="3" opacity=".5"/><path d="M-22,14Q-20,40 -18,62" stroke="#a8d8ff" stroke-width="4" fill="none" opacity=".55" stroke-linecap="round"/>
      <path d="M-30,40H30" stroke="#fff" stroke-width="5" opacity=".75"/></g></g>`;
  // the conch (หอยสังข์) lying across the fist: spire and knobs out to the side, the pink flared lip below, the fingers over the shell.
  // rot turns it in the hand (0 = across a hanging forearm), mirror puts the spire on the other side (taJunBlow: conch(-92, skin, true))
  const conch = (rot = 0, skin = "#8a5a3a", mirror = false) => `<g transform="translate(0,122) rotate(${rot}) scale(${mirror ? -1 : 1},1)">
    <path d="M-58,6Q-40,-6 -18,-22Q2,-36 24,-28L56,-12Q62,-7 57,-1L26,10Q20,28 -2,31Q-32,30 -58,6Z" fill="url(#tdConch)" ${ln(2.6)}/>
    <path d="M-30,12Q-16,46 14,38Q32,33 25,11Q4,22 -30,12Z" fill="#f6d8c4" ${ln(2.4)}/><path d="M-24,15Q-10,34 12,32Q2,22 -24,15Z" fill="url(#tdConchIn)"/>
    <path d="M-12,-27l3,-12l6,9M2,-32l4,-13l6,11M16,-31l5,-11l4,10M30,-24l5,-9l3,8" fill="#fbeedc" ${ln(2)}/>
    <path d="M28,-26Q33,-12 28,8M39,-20Q43,-9 39,5M49,-15Q52,-7 49,2" stroke="#b88a62" stroke-width="2.2" fill="none"/>
    <path d="M-48,4Q-24,-10 -2,-4Q14,0 24,-6M-40,12Q-16,4 8,10" stroke="#c89a72" stroke-width="2" fill="none" opacity=".7"/>
    <path d="M-36,-6Q-14,-24 14,-26" stroke="#fff" stroke-width="3.4" fill="none" opacity=".7" stroke-linecap="round"/>
    <ellipse cx="57" cy="-6" rx="2.6" ry="3.6" fill="#3a2a20"/>
    <g fill="${skin}" stroke="${LINE}" stroke-width="2.2">${[-14, -3, 8].map((x) => `<rect x="${x}" y="-12" width="11" height="24" rx="5.5"/>`).join("")}</g></g>`;
  // the old photo in a frame (a hand prop variant and a free-standing piece)
  function photoArt(o = {}) {
    // two young fishermen on a longtail boat, sepia; the one on the left wears a headband (ตาจุ่น), the other a cap (ตา)
    return `<rect x="-90" y="-66" width="180" height="132" fill="url(#tdSepia)"/>
      <path d="M-90,6Q-40,0 0,4T90,2V66H-90Z" fill="#a88458"/><path d="M-90,14Q-50,10 -10,14T90,12" stroke="#d8c09a" stroke-width="2" fill="none" opacity=".7"/>
      <path d="M-74,-30L-60,-52L-44,-26ZM40,-40L58,-62L76,-34Z" fill="#b8996c" opacity=".7"/>
      <path d="M-80,22Q-10,36 76,18L66,36Q-6,46 -70,36Z" fill="#5a3e22"/><path d="M-80,22L-92,8" stroke="#5a3e22" stroke-width="5"/><path d="M-88,8l-6,-12" stroke="#8a2e1e" stroke-width="3"/>
      <g fill="#4a3018"><circle cx="-30" cy="-10" r="9"/><path d="M-44,26Q-44,0 -30,-1Q-16,0 -16,26Z"/><path d="M-40,-14H-20" stroke="#e8d8b0" stroke-width="3"/>
        <circle cx="16" cy="-12" r="9"/><path d="M2,26Q2,-2 16,-3Q30,-2 30,26Z"/><path d="M6,-20Q16,-28 28,-20L32,-16H4Z"/></g>
      <path d="M-18,8Q-6,0 4,8" stroke="#4a3018" stroke-width="6" stroke-linecap="round" fill="none"/>
      <rect x="-90" y="-66" width="180" height="132" fill="#fff8e0" opacity=".08"/>
      <path d="M-60,-66l10,40M30,-66l-6,30M70,10l10,30" stroke="#fff4dc" stroke-width="1.4" opacity=".35"/>
      <text x="62" y="58" text-anchor="end" font-family="Mali" font-weight="700" font-size="12" fill="#4a3018" opacity=".7">${o.year || "๒๕๒๕"}</text>`;
  }
  const photoFramed = (o = {}) => `<path d="M-112,-88H112V88H-112Z" fill="#2a1a0c" transform="translate(6,8)" opacity=".5"/>
    <path d="M-112,-88H112V88H-112Z" fill="url(#tdFrame)" ${ln(3)}/><path d="M-112,-88L-98,-74H98L112,-88ZM-112,88L-98,74H98L112,88Z" fill="#000" opacity=".16"/>
    <path d="M-112,-88L-98,-74V74L-112,88ZM112,-88L98,-74V74L112,88Z" fill="#fff" opacity=".1"/>
    <rect x="-98" y="-74" width="196" height="148" fill="#efe2c4" stroke="#3a240e" stroke-width="2"/>${photoArt(o)}
    ${o.glass === false ? "" : `<rect x="-98" y="-74" width="196" height="148" fill="url(#tdGlass)"/>`}
    <path d="M-104,-84H104" stroke="#d8a868" stroke-width="2" opacity=".5"/>`;
  const photoHand = (rot = -22) => `<g transform="translate(0,124) rotate(${rot}) translate(0,-40) scale(.6)">${photoFramed()}</g>`;
  TC.PROP = { phoneStick, phone, bucket, conch, photo: photoHand };
  Tide.PROP = Object.assign(Tide.PROP || {}, TC.PROP);
  // keep: the fist that holds the prop (rig v2 puts a cast's hand prop in both; the build hook below clears the other one)
  C.juneStick = { v2: C.june.v2, hand: phoneStick(), keep: "F" };
  C.junePhone = { v2: C.june.v2, hand: phone(), keep: "F" };
  C.tangBucket = { v2: tangV2, hand: bucket(), keep: "F" };
  C.tangRingBucket = { v2: C.tangRing.v2, hand: bucket(), keep: "F" };
  C.taJunConch = { v2: junV2, hand: conch(), keep: "B" };
  C.taJunBlow = { v2: junV2, hand: conch(-92, junV2.skin, true), keep: "F" };
  C.yaiTidePhoto = { v2: yaiV2, hand: photoHand(), keep: "F" };

  // ---------------- scene pieces ----------------
  TC.photo = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s}) rotate(${o.rot ?? 0})"><g${o.id ? ` id="${o.id}"` : ""}>${photoFramed(o)}</g></g>`;
  TC.clipping = (x, y, s = 1, o = {}) => {
    const t = o.title || "คลื่นยักษ์ถล่มชายฝั่งอันดามัน", d = o.date || "๒๗ ธ.ค. ๔๗", cap = o.caption || "ชาวประมงอุ้มหญิงสาวหนีคลื่น";
    const torn = "M-150,-120L-138,-124L-126,-118L-110,-125L-92,-119L-74,-126L-52,-120L-30,-125L-8,-118L14,-124L36,-119L58,-126L80,-120L102,-125L124,-119L150,-123L148,-96L152,-60L147,-20L151,20L146,60L150,96L147,124L124,120L100,126L76,119L52,125L28,118L4,124L-20,119L-44,125L-68,118L-92,124L-116,119L-140,125L-150,120L-146,80L-151,40L-147,0L-152,-40L-147,-80Z";
    return `<g transform="translate(${x},${y}) scale(${s}) rotate(${o.rot ?? -4})"><g${o.id ? ` id="${o.id}"` : ""}>
      <path d="${torn}" fill="#000" opacity=".25" transform="translate(6,8)"/><path d="${torn}" fill="url(#tdNews)" stroke="#a8946a" stroke-width="2"/>
      <text x="-134" y="-92" font-family="Kanit" font-weight="900" font-size="25" fill="#2a2420">${t}</text>
      <path d="M-134,-80H134" stroke="#2a2420" stroke-width="2"/><text x="134" y="-66" text-anchor="end" font-family="Kanit" font-weight="400" font-size="13" fill="#5a5048">${d}</text>
      <rect x="-134" y="-58" width="150" height="112" fill="#8a8274"/>
      <g opacity=".85"><path d="M-134,30Q-90,16 -50,26T16,22V54H-134Z" fill="#5a544a"/><path d="M-124,24Q-90,8 -60,20" stroke="#c8c0b0" stroke-width="3" fill="none"/>
        <circle cx="-58" cy="-26" r="10" fill="#2e2a24"/><path d="M-74,34Q-74,-10 -58,-12Q-40,-10 -38,10L-30,26L-44,36Z" fill="#2e2a24"/>
        <path d="M-52,-8Q-30,-18 -12,-6Q0,4 -6,16Q-26,20 -50,8Z" fill="#3e3a32"/><circle cx="-12" cy="-18" r="8.5" fill="#3e3a32"/><path d="M-6,-24Q6,-16 2,2Q-4,-6 -8,-12Z" fill="#2e2a24"/>
        <path d="M-8,14L4,40M-14,16L-6,42" stroke="#3e3a32" stroke-width="5" stroke-linecap="round"/></g>
      ${Array.from({ length: 64 }, (_, k) => `<circle cx="${-130 + (k % 8) * 18}" cy="${-52 + Math.floor(k / 8) * 13}" r="1.3" fill="#2e2a24" opacity=".22"/>`).join("")}
      <text x="-134" y="74" font-family="Kanit" font-weight="400" font-size="13" fill="#3a342c">${cap}</text>
      ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M30,${-50 + k * 15}H${k === 6 ? 96 : 134}" stroke="#6a6258" stroke-width="5" opacity=".55"/>`).join("")}
      ${[0, 1, 2].map((k) => `<path d="M-134,${92 + k * 13}H${k === 2 ? 40 : 134}" stroke="#6a6258" stroke-width="5" opacity=".5"/>`).join("")}
      <path d="M-150,-30Q0,-24 150,-36" stroke="#a8946a" stroke-width="2" opacity=".5"/></g></g>`;
  };
  TC.duckRing = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})"><g${o.id ? ` id="${o.id}"` : ""}>
    ${o.water ? `<ellipse cx="0" cy="18" rx="150" ry="26" fill="#0e5a7a" opacity=".35"/>` : `<ellipse cx="0" cy="40" rx="130" ry="20" fill="#000" opacity=".22"/>`}
    <path d="M-120,0Q-120,-58 0,-58Q120,-58 120,0Q120,58 0,58Q-120,58 -120,0Z" fill="url(#tdRing)" ${ln(4)}/>
    <ellipse cx="0" cy="-6" rx="60" ry="22" fill="${o.water ? "#1a7a9a" : "#e8d8b0"}" ${ln(3)}/><path d="M-58,-2Q0,22 58,-2" stroke="#b47c0c" stroke-width="3" fill="none" opacity=".6"/>
    <path d="M-100,-20Q-60,-50 0,-50" stroke="#fffbe0" stroke-width="9" fill="none" opacity=".8" stroke-linecap="round"/><path d="M40,46Q90,38 110,10" stroke="#b47c0c" stroke-width="5" fill="none" opacity=".5"/>
    ${o.water ? `<path d="M-124,8Q-80,24 -40,12T40,14T124,6" stroke="#bfefff" stroke-width="5" fill="none" opacity=".75"/>` : ""}
    <g transform="translate(76,-30)"><path d="M-20,10Q-30,-40 -2,-62Q28,-80 42,-52Q50,-34 36,-20Q28,-4 20,12Z" fill="url(#tdRing)" ${ln(3.4)}/>
      <path d="M36,-46Q64,-52 70,-40Q64,-28 38,-30Z" fill="#ff8a2a" ${ln(3)}/><path d="M40,-38H66" stroke="#c8561a" stroke-width="2.4"/>
      <circle cx="22" cy="-52" r="6.4" fill="#fff" stroke="${LINE}" stroke-width="2"/><circle cx="24" cy="-52" r="3.4" fill="${LINE}"/><circle cx="22" cy="-54" r="1.2" fill="#fff"/>
      <path d="M-10,-42Q0,-62 18,-66" stroke="#fffbe0" stroke-width="5" fill="none" opacity=".75" stroke-linecap="round"/><ellipse cx="10" cy="-34" rx="7" ry="4" fill="#ff9aa0" opacity=".55"/></g>
    <path d="M-112,-6Q-130,-20 -126,-34Q-112,-30 -106,-14Z" fill="url(#tdRing)" ${ln(3)}/></g></g>`;

  // ---------------- poses ----------------
  const M = Rig.MODES;
  // the selfie stick held up and out to the front, the free hand making a V
  M.film = (u, o) => { const s = Math.sin(u * 1.6), j = Math.sin(u * 7) * 0.6; return { ...M.idle(u, o), uaF: -142 + 3 * s + j, faF: -14 + 2 * s, uaB: 26, faB: -96 + 3 * Math.sin(u * 2.4), torso: -3, head: -10 + 2 * Math.sin(u * 1.2), bodyY: -2 }; };
  // pointing up toward the hill behind, the head turned up with the arm
  M.pointUp = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.4); return { ...M.idle(u, o), uaF: -138 + 3 * b, faF: -4, uaB: 10, faB: -16, torso: -4, head: -14, bodyY: -2 }; };
  // the conch blown with both hands at the mouth, the chest heaving
  M.blowConch = (u, o) => { const h = Math.sin(u * 2 * Math.PI / 1.6); return { ...M.idle(u, o), uaF: -108 + h, faF: -158, uaB: 14 + h, faB: -34, torso: -5 - 2 * h, head: -12 - 2 * h, bodyY: -2 - 2 * h }; };
  // forearms resting on the swim ring round the waist
  M.ringArms = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.6); return { ...M.idle(u, o), uaF: -26 + b, faF: -64, uaB: 26 - b, faB: 64, torso: b * 0.6 }; };
  // both arms up, bouncing on the toes (free fish!)
  M.cheer = (u, o) => { const b = Math.abs(Math.sin(u * 2 * Math.PI / 0.5)); return { ...M.idle(u, o), uaF: -156 + 6 * b, faF: -24, uaB: 156 - 6 * b, faB: 24, torso: -4, head: -10 - 4 * b, bodyY: -18 * b }; };
  // a hand over the brows, looking out to sea
  M.shadeEyes = (u, o) => ({ ...M.idle(u, o), uaF: -118, faF: -136, uaB: 4, faB: -12, torso: -3, head: -6 + Math.sin(u * 0.7) * 2 });
  // a raised finger wagging: a warning
  M.wagFinger = (u, o) => ({ ...M.idle(u, o), uaF: -34, faF: -132 + 12 * Math.sin(u * 2 * Math.PI / 0.45), uaB: 4, faB: -12, torso: 2, head: 4 + 2 * Math.sin(u * 3) });
  // the old photo held up in the front hand, looked at (the frame stays upright at this pose)
  M.holdPhoto = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 3); return { ...M.idle(u, o), uaF: 2 + b, faF: 20 - b, uaB: 6, faB: -14, torso: 2, head: 6 + b }; };
  // bent forward, reaching down to the sand (picking up a fish)
  M.scoop = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.1); return { ...M.crouch(u, o), uaF: -30 + 8 * b, faF: -12, uaB: -10 - 6 * b, faB: -20, torso: 34, head: 14 }; };
})();

// ---------------- EP.2 "คลื่นแรกไป อย่าไว้ใจ": the wrist grab, ยาย hugging the photo, the tourist on the cooler ----------------
// Extra faces on every v2 cast (injected after the build, chosen in a track entry like the others):
//   eyes "up" (looking up, brows raised and worried) · "upSide" (up and toward +x: up-left on screen when flipped) · "sideWorry" / "sideAngry"
//   (looking toward +x, brows raised / knit: to whoever stands on that side) · "strain" (narrowed,
//   brows knit: holding on with everything) · mouth "grit" (teeth clenched)
// Poses (Rig.MODES):
//   grabHold  ตาจุ่น reaching to his right and down, the front fist closed on someone's wrist, braced back (leaning away, knees bent,
//             the free arm out for balance); o.reachIn (s) shoots the arm out from hanging at the start of the segment
//   yanked    จูน (drawn flipped) leaning away toward the steps, the held front arm trailing back to the holder, the free arm reaching
//             forward, the back foot pushing off; o.flip false if the actor is not flipped
//             The two share one tug (TideCast.tug: the pair sways and jerks together), so a hand set on a wrist stays there
//   lookUp    head tilted back, hands a little raised and tense: use with eyes "up" / "upSide"
//   hugPhoto  ยาย clutching the framed photo flat against her chest, both forearms over it (use yaiTideHug); o.up 0…1 tips the head
//             back to look up (with eyes "up" / "upSide")
//   cling     arms draped over something floating in front of the chest, bobbing (the tourist on his cooler: Tide.raft)
// Cast: taJunGrip (ตาจุ่น with the front fist closed round a wrist) · juneYank (จูน with the held hand straining open) · yaiTideHug (ยาย with the photo for hugPhoto: the frame against her
//   chest, her front forearm and both hands over it) · tourist (นักท่องเที่ยว ~30: sunburnt, sunglasses pushed up on his head, a loud
//   blue floral shirt, orange board shorts)
// TideCast.armPoint(mode, side, along, u, opts) → [x, y] a point `along` units down the forearm (0 the elbow, 118 the palm) in the
//   actor's own units (feet at 0,0) for a pose at time u
// TideCast.gripPair(x, y, s, o) → { x, y, s, hand } where to stand จูน (flipped, "yanked") so ตาจุ่น's fist (taJunGrip at x, y, scale s,
//   unflipped, "grabHold") closes on her wrist: list จูน first and ตาจุ่น after her so his fist is drawn over her wrist.
//   o.wrist (80) how far down her forearm he holds (her pink band shows between his fist and her hand), o.hold / o.held other poses
// TideCast.headPoint(mode, u, opts) → [x, y] the middle of the face for a pose (actor units; mirror x for a flipped actor) to frame close shots
(function () {
  const { LINE, dk, hi, shade, paint, limbD } = Rig2;
  const C = Rig.CAST, M = Rig.MODES, TC = window.TideCast;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const backOut = (k) => { const c1 = 1.4, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };
  const f = (v) => (+v).toFixed(1);

  // ---------------- extra eyes and mouth (same geometry as rig2's eye set) ----------------
  const EX = [-17, 19], EY = -548;
  function extraFace(V) {
    const iris = V.iris || "#4a2e20", brow = V.brow || V.hair.c, lid = LINE, lash = V.lash;
    const sclera = (rx, ry, dy = 0) => EX.map((x) => `<ellipse cx="${x}" cy="${EY + dy}" rx="${rx}" ry="${ry}" fill="#fbf7f0" stroke="${lid}" stroke-width="1.6"/>`).join("");
    const pupil = (r, dx, dy) => EX.map((x) => `<circle cx="${x + dx}" cy="${EY + dy}" r="${r}" fill="${iris}"/><circle cx="${x + dx}" cy="${EY + dy}" r="${f(r * 0.55)}" fill="#160e0c"/>
      <circle cx="${f(x + dx - r * 0.38)}" cy="${f(EY + dy - r * 0.45)}" r="${f(Math.max(1.6, r * 0.32))}" fill="#fff"/>`).join("");
    const lids = (lift = 0) => EX.map((x, i) => `<path d="M${x - 10},${EY - 3 - lift}Q${x},${EY - 15 - lift} ${x + 10},${EY - 4 - lift}" stroke="${lid}" stroke-width="3.4" fill="none" stroke-linecap="round"/>` +
      (lash ? `<path d="M${x + (i ? 10 : -10)},${EY - 4 - lift}l${i ? 4 : -4},-4" stroke="${lid}" stroke-width="2.6" stroke-linecap="round"/>` : "")).join("");
    const brows = (ty = 0, tilt = 0) => EX.map((x, i) => { const s = i ? 1 : -1, inner = -tilt, outer = tilt * 0.6;
      return `<path d="M${x - 11},${EY - 20 + ty + (s < 0 ? outer : inner)}Q${x},${EY - 26 + ty} ${x + 11},${EY - 20 + ty + (s < 0 ? inner : outer)}" stroke="${brow}" stroke-width="4.6" fill="none" stroke-linecap="round"/>`; }).join("");
    const bags = V.bags ? EX.map((x) => `<path d="M${x - 9},${EY + 9}q9,7 18,0" stroke="${shade(V.skin, 0.3)}" stroke-width="3" fill="none" opacity=".8"/>`).join("") : "";
    // the lower lid squeezed up and the creases of a hard squint (strain)
    const squint = EX.map((x) => `<path d="M${x - 9},${EY + 5}Q${x},${EY + 1} ${x + 9},${EY + 5}" stroke="${lid}" stroke-width="2.4" fill="none" stroke-linecap="round"/>`).join("") +
      `<path d="M-2,-572l3,8M6,-572l-3,8" stroke="${shade(V.skin, 0.35)}" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>`;
    return {
      eyes: {
        up: sclera(8.6, 10.6) + pupil(6.2, 0.6, -4.8) + lids(2.5) + brows(-7, -5) + bags,
        upSide: sclera(8.6, 10.6) + pupil(6.0, 3.6, -4.4) + lids(2.5) + brows(-7, -5) + bags,
        strain: sclera(8.6, 8.2, 1) + pupil(5.8, 1.5, 1.5) + lids(-2) + squint + brows(6, 10) + bags,
        sideWorry: sclera(8.6, 10.4) + pupil(6.2, 4.2, 1) + lids(1) + brows(-5, -6) + bags,
        sideAngry: sclera(8.6, 8.8, 1) + pupil(6, 4.2, 2) + lids(-2) + brows(5, 8) + bags,
      },
      mouths: {
        grit: `<path d="M-12,-514Q-4,-522 4,-522Q12,-522 20,-514L17,-508Q4,-512 -9,-508Z" fill="#f4eee2" stroke="${LINE}" stroke-width="2.4" stroke-linejoin="round"/>
          <path d="M-9,-512Q4,-516 17,-512" stroke="#b8ae9c" stroke-width="1.4" fill="none"/><path d="M-2,-520v9M4,-521v10M10,-520v9" stroke="#b8ae9c" stroke-width="1.2"/>
          <path d="M-13,-514q-4,5 -3,11M21,-514q4,5 3,11M-4,-503q8,3 16,0" stroke="${shade(V.skin, 0.34)}" stroke-width="2" fill="none" stroke-linecap="round"/>`,
      },
    };
  }
  const build1 = Rig.build;
  Rig.build = (parent, id, P) => {
    const el = build1(parent, id, P);
    if (P && P.v2) {
      const x = extraFace(P.v2), eg = document.getElementById(`${id}-eyes`), mg = document.getElementById(`${id}-mouth`);
      if (eg) eg.insertAdjacentHTML("beforeend", Object.entries(x.eyes).map(([n, v]) => `<g class="eye-${n}" display="none">${v}</g>`).join(""));
      if (mg) mg.insertAdjacentHTML("beforeend", Object.entries(x.mouths).map(([n, v]) => `<g class="mouth-${n}" display="none">${v}</g>`).join(""));
      // V.sleevePrint: SVG laid on each upper arm's sleeve (the arm's own frame: the shoulder at 0, down the arm +y)
      if (P.v2.sleevePrint) ["F", "B"].forEach((sd) => { const ua = document.getElementById(`${id}-ua${sd}`); if (ua) ua.insertAdjacentHTML("beforeend", P.v2.sleevePrint); });
    }
    return el;
  };

  // ---------------- the tug the two share ----------------
  // the pair sways toward the steps and back and jerks: x in local units toward +x (the holder's side moves the same way on screen)
  const tugX = (u) => 5 * Math.sin((u * 2 * Math.PI) / 0.9) + 2.2 * Math.sin((u * 2 * Math.PI) / 0.37 + 1);
  const tugY = (u) => 3 * Math.abs(Math.sin((u * 2 * Math.PI) / 0.9));
  TC.tug = (u) => ({ x: tugX(u), y: tugY(u) });

  // ---------------- poses ----------------
  M.grabHold = (u, o) => {
    const k = o.reachIn ? backOut(clamp(u / o.reachIn, 0, 1)) : 1, j = Math.sin(u * 23) * 0.6;
    return { ...M.idle(u, o), uaF: lerp(6, -50, k), faF: lerp(-8, -28, k), uaB: 34 + 4 * Math.sin(u * 2.9), faB: 32 + 6 * Math.sin(u * 3.7), torso: -5 + j, head: 3 + 2 * Math.sin(u * 4.1),
      thF: -18, shF: 8, thB: 22, shB: -20, rootR: -5, rootX: tugX(u), rootY: 0, bodyY: 12 + tugY(u), hair: 0, acc: 0 };
  };
  M.yanked = (u, o) => {
    const s = o.flip === false ? -1 : 1, a = Math.sin(u * 7.3), b = Math.sin(u * 5.1 + 1);
    return { ...M.idle(u, o), uaF: -66, faF: -4, uaB: 70 + 12 * a, faB: 12 + 10 * b, torso: -8 + 1.5 * b, head: -8 + 3 * Math.sin(u * 6.2),
      thF: -24, shF: 32, thB: 26, shB: 6, rootR: -9, rootX: -s * tugX(u), rootY: 0, bodyY: 10 + tugY(u) };
  };
  M.lookUp = (u, o) => { const b = Math.sin((u * 2 * Math.PI) / 3); return { ...M.idle(u, o), uaF: 10 + b, faF: -28, uaB: -10 - b, faB: 28, torso: -3, head: -12 + 1.5 * b, bodyY: -2 }; };
  const HUG = { uaF: -8, faF: 156, uaB: 27, faB: -167 };
  M.hugPhoto = (u, o) => {
    const b = Math.sin((u * 2 * Math.PI) / 3.4), up = o.up || 0;
    return { ...M.idle(u, o), uaF: HUG.uaF + 0.6 * b, faF: HUG.faF, uaB: HUG.uaB - 0.6 * b, faB: HUG.faB, torso: 1 - 3 * up, head: 6 - 18 * up + b, bodyY: -1 - b };
  };
  M.cling = (u, o) => {
    const b = Math.sin((u * 2 * Math.PI) / 2.2), j = Math.sin(u * 3.3);
    return { ...M.idle(u, o), uaF: -74 + 1.5 * b, faF: 164 - 1.5 * b, uaB: 74 - 1.5 * b, faB: -164 + 1.5 * b, torso: 1.5 * j, head: -4 + 7 * Math.sin(u * 1.7) + 2 * j, bodyY: 0 };
  };

  // ---------------- where a point on an arm ends up ----------------
  const rot = (p, deg) => { const a = (deg * Math.PI) / 180, c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; };
  TC.armPoint = (mode, side = "F", along = 118, u = 0, opts = {}) => {
    const p = M[mode](u, opts), F = side === "F";
    let q = rot([0, along], F ? p.faF : p.faB);
    q = rot([q[0], q[1] + 122], F ? p.uaF : p.uaB);
    q = rot([q[0] + (F ? 46 : -46), q[1] - 455 + p.bodyY], p.rootR || 0);
    return [q[0] + (p.rootX || 0), q[1] + (p.rootY || 0)];
  };
  TC.gripPair = (x, y, s, o = {}) => {
    const a = TC.armPoint(o.hold || "grabHold", "F", 118), b = TC.armPoint(o.held || "yanked", "F", o.wrist ?? 80);
    return { x: Math.round(x + (a[0] + b[0]) * s), y: Math.round(y + (a[1] - b[1]) * s), s, hand: [Math.round(x + a[0] * s), Math.round(y + a[1] * s)] };
  };
  // the middle of the face (between the eyes) for a pose, in the actor's units → frame a close shot on it (x is mirrored when flipped)
  TC.headPoint = (mode, u = 0, opts = {}) => {
    const p = M[mode](u, opts), hs = 1.12;
    let q = rot([0, (-548 + 500) * hs], p.head || 0);
    q = rot([q[0], q[1] - 500 + 300], p.torso || 0);
    q = rot([q[0], q[1] - 300 + p.bodyY], p.rootR || 0);
    return [q[0] + (p.rootX || 0), q[1] + (p.rootY || 0)];
  };
  // a body point (in the actor's units, under the body's bob) seen from inside a forearm at a pose → [x, y] in that forearm's frame
  const toFore = (mode, side, P, u = 0, opts = {}) => {
    const p = M[mode](u, opts), F = side === "F";
    let q = rot([P[0] - (F ? 46 : -46), P[1] + 455], -(F ? p.uaF : p.uaB));
    return rot([q[0], q[1] - 122], -(F ? p.faF : p.faB));
  };

  // ---------------- ตาจุ่น's fist closed round a wrist (a hand prop at the palm; drawn over the default hand) ----------------
  const junSkin = C.taJun.v2.skin, junD = shade(junSkin, 0.3), junL = hi(junSkin, 0.22);
  const gripFist = () => `<g transform="translate(1,116) rotate(-34)">
    <path d="M-17,-14Q-21,4 -16,18Q-4,26 12,22Q24,16 23,0Q22,-16 10,-21Q-8,-24 -17,-14Z" fill="${junSkin}" ${ln(2.4)}/>
    <path d="M-12,-10Q-14,4 -10,14" stroke="${junD}" stroke-width="2" fill="none" opacity=".7"/>
    ${[[-6, -17], [3, -18], [12, -14], [19, -7]].map(([x, y]) => `<path d="M${x - 5},${y + 2}q5,-7 10,0" fill="${junSkin}" ${ln(2)}/><path d="M${x - 2},${y - 1}q2,-2 4,0" stroke="${junL}" stroke-width="1.6" fill="none"/>`).join("")}
    <path d="M-2,-10Q2,4 0,18M7,-10Q11,4 9,18M15,-6Q18,6 16,15" stroke="${junD}" stroke-width="1.8" fill="none" opacity=".75"/>
    <path d="M-17,0Q-26,6 -22,16Q-14,22 -6,16" fill="${junSkin}" ${ln(2.2)}/><path d="M-21,12q4,3 8,1" stroke="${junD}" stroke-width="1.4" fill="none"/>
    <path d="M-10,-14Q2,-20 14,-16" stroke="${junL}" stroke-width="2.4" fill="none" opacity=".55" stroke-linecap="round"/></g>`;
  C.taJunGrip = { v2: C.taJun.v2, hand: gripFist(), keep: "F" };
  // จูน's held hand straining open: the fingers splayed and bent back, the thumb out (drawn over the default hand)
  const juneSk = C.june.v2.skin, juneD = shade(juneSk, 0.3);
  const splay = () => `<g transform="translate(0,104)">
    <path d="M-12,0Q-15,14 -11,26Q-2,34 9,30Q15,20 13,2Z" fill="${juneSk}" ${ln(2.4)}/>
    ${[[-10, 26, 28, 22], [-3, 30, 34, 8], [5, 30, 32, -6], [11, 25, 25, -20]].map(([x, y, l, a]) => `<g transform="translate(${x},${y}) rotate(${a})"><rect x="-3.6" y="-3" width="7.2" height="${l}" rx="3.6" fill="${juneSk}" ${ln(2)}/><rect x="-2.2" y="${l - 7}" width="4.4" height="4.6" rx="2" fill="#f6dcd0"/></g>`).join("")}
    <path d="M12,6Q26,4 32,14Q30,19 24,16Q18,12 12,14" fill="${juneSk}" ${ln(2.2)}/>
    <path d="M-6,20q4,3 9,2" stroke="${juneD}" stroke-width="1.6" fill="none"/></g>`;
  C.juneYank = { v2: C.june.v2, hand: splay(), keep: "F" };

  // ---------------- ยาย hugging the photo: the frame flat on her chest, her front forearm and both hands over it ----------------
  {
    const V = C.yaiTide.v2, sk = V.skin, skS = shade(sk, 0.2), skD = shade(sk, 0.34), skB = dk(sk, 0.1), tot = HUG.uaF + HUG.faF;
    const [cx, cy] = toFore("hugPhoto", "F", [0, -404]), [bx, by] = toFore("hugPhoto", "F", [-64, -394]);
    const hand = (c, cd) => `<path d="M-11,104Q-14,118 -10,128Q-2,138 8,132Q14,124 12,108Z" fill="${c}" stroke="${LINE}" stroke-width="2.4" stroke-linejoin="round"/>
      <path d="M9,108Q19,112 16,122Q13,126 9,122" fill="${c}" stroke="${LINE}" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M-4,118Q-1,128 -3,134M3,118Q6,128 4,134" stroke="${cd}" stroke-width="1.6" fill="none" opacity=".8" stroke-linecap="round"/>
      <path d="M-6,124q4,4 9,3" stroke="${cd}" stroke-width="1.6" fill="none"/>`;
    // the frame, upright against the chest (its photo faces out), then the left hand gripping its far edge, then the front forearm and hand
    const hug = `${TC.photo(f(cx), f(cy), 0.6, { rot: f(-tot) })}
      <g transform="translate(${f(bx)},${f(by)}) rotate(71) translate(0,-118)"><g transform="translate(0,66)">${paint(limbD(40, 22, 19), skB)}</g>${hand(skB, shade(skB, 0.34))}</g>
      ${paint(limbD(106, 25, 19), sk)}<path d="M-6,30q4,20 0,40" stroke="${skS}" stroke-width="2" fill="none" opacity=".5"/>${hand(sk, skD)}`;
    C.yaiTideHug = { v2: V, hand: hug, keep: "F" };
  }

  // ---------------- นักท่องเที่ยว: ~30, sunburnt, sunglasses pushed up on his head, a loud floral shirt ----------------
  const touristHair = (h) => `
    <path d="M-47,-552C-51,-600 -24,-622 4,-622C33,-622 55,-602 50,-552Q47,-566 40,-574L37,-558L28,-579L19,-563L8,-584L-3,-565L-15,-582L-24,-563L-34,-577Q-43,-568 -47,-552Z" fill="${h.c}" ${ln()}/>
    <path d="M-30,-600Q-10,-614 14,-612M-38,-586q8,-10 18,-14M24,-604q14,4 22,16" stroke="${h.sh}" stroke-width="3" fill="none" opacity=".5" stroke-linecap="round"/>
    <path d="M-44,-560v14M47,-560v12" stroke="${h.c}" stroke-width="7" stroke-linecap="round"/>`;
  // aviators pushed up onto the hair: two dark teardrop lenses catching the sky, the bridge, the arms going back into the hair
  const shades = `<g transform="translate(2,-610) rotate(-3)">
    <path d="M-48,8L-38,2M48,8L38,2" stroke="#2a2420" stroke-width="3.4" stroke-linecap="round"/>
    ${[-1, 1].map((s) => `<path d="M${s * 4},-2Q${s * 6},-8 ${s * 18},-8Q${s * 38},-8 ${s * 40},2Q${s * 40},16 ${s * 26},18Q${s * 8},18 ${s * 5},6Z" fill="#26323c" stroke="#c8a040" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M${s * 12},-3Q${s * 22},-5 ${s * 32},0" stroke="#8ec4e0" stroke-width="3" fill="none" opacity=".75" stroke-linecap="round"/><path d="M${s * 10},8l${s * 8},-6" stroke="#fff" stroke-width="2" opacity=".5" stroke-linecap="round"/>`).join("")}
    <path d="M-5,-1Q0,-5 5,-1" stroke="#c8a040" stroke-width="2.6" fill="none"/></g>`;
  // sunburn: a red nose and cheeks, peeling on the nose, a tan line at the neck of the shirt
  const sunburn = `<ellipse cx="6" cy="-531" rx="11" ry="8" fill="#e8584a" opacity=".38"/><ellipse cx="-27" cy="-526" rx="13" ry="8" fill="#e8584a" opacity=".3"/><ellipse cx="33" cy="-526" rx="13" ry="8" fill="#e8584a" opacity=".3"/>
    <path d="M2,-540q3,-2 5,1M8,-536q2,-2 4,1" stroke="#fff4ec" stroke-width="1.4" fill="none" opacity=".8"/><path d="M-26,-584q12,-3 22,0" stroke="#e8584a" stroke-width="5" opacity=".25" stroke-linecap="round"/>`;
  // the print: big white and yellow hibiscus, monstera leaves and palm fronds on electric blue
  const flower = (x, y, s, c, cc) => `<g transform="translate(${x},${y}) scale(${s})">${[0, 72, 144, 216, 288].map((a) => `<path d="M0,0C-9,-6 -10,-20 0,-24C10,-20 9,-6 0,0Z" fill="${c}" transform="rotate(${a})"/>`).join("")}
    <circle r="5" fill="${cc}"/><path d="M0,0l9,-12" stroke="${cc}" stroke-width="2.4"/><circle cx="9" cy="-12" r="2.4" fill="#ffe14a"/></g>`;
  const leaf = (x, y, a, s) => `<g transform="translate(${x},${y}) rotate(${a}) scale(${s})"><path d="M0,0C-14,-10 -16,-34 0,-46C16,-34 14,-10 0,0Z" fill="#2fa860"/><path d="M0,-2V-44M0,-14l-9,-6M0,-24l-10,-6M0,-14l9,-6M0,-24l10,-6" stroke="#1e7a44" stroke-width="2"/></g>`;
  const floral = `<g opacity=".95">${leaf(-44, -430, -30, 1)}${leaf(36, -340, 40, 1.1)}${leaf(-20, -330, -150, 0.9)}${leaf(48, -462, 120, 0.8)}${leaf(-50, -476, -80, 0.7)}
    ${flower(-34, -462, 1, "#fff6ec", "#e8483a")}${flower(36, -446, 1.05, "#ffd43a", "#e8483a")}${flower(-38, -364, 0.95, "#ff8ab4", "#c8203a")}${flower(16, -318, 0.9, "#fff6ec", "#e8483a")}
    ${flower(2, -404, 0.85, "#ff8ab4", "#c8203a")}${flower(44, -348, 0.55, "#ffd43a", "#e8483a")}</g>`;
  const sleeveFlowers = `${leaf(-6, 34, 150, 0.6)}${flower(4, 14, 0.62, "#fff6ec", "#e8483a")}${flower(-8, 44, 0.45, "#ffd43a", "#e8483a")}`;
  C.tourist = { v2: {
    skin: "#e2946c", iris: "#2e1c12", blush: 1.0, lip: "#c45e52", w: 1.08, limb: 1.02,
    hair: { c: "#2c1e16", s: "#120c08", sh: "#7a5a44", front: (x) => touristHair(x.hair) },
    top: { kind: "shirt", c: "#1e8fd6", sleeve: "short", neck: "collar", collar: "#1a7cbc", button: "#f4f0e2" },
    print: floral, sleevePrint: sleeveFlowers, bottom: { kind: "shorts", c: "#f2963a" }, feet: { kind: "bare" },
    face: sunburn, faceTop: shades,
  } };
})();
