// "ตึกโยก" on-screen graphics (screen space: put them in L.light unless noted). 2.5D motion graphics (skill rule V10): every badge, card,
// pill and phone is a slab with depth (a darker body under a lit face), faces are lit from the upper left (gradient, bevel, gloss), what
// floats casts a soft shadow; entries squash & stretch with an elastic/back overshoot, staggered 0.1–0.15 s; a secondary motion keeps
// running until the shot ends; exits shrink and fade.
//   QkUI.title(tl, layer, t0, dur, o)    the EP.1 opener title: ROD MAI CLUB · "ตึกโยก" in extruded 3D letters that drop in, squash and sway
//                                        like the tower, over a glowing seismograph line · o.ep "EP.1 · หมอบ ป้อง เกาะ" on a 3D pill
//   QkUI.app(tl, layer, t0, dur, o)      your left hand holding the phone (with its side thickness and glass glare) with the rider app: the
//                                        route map to เดอะสกาย 32, the order (ห้อง 2714 · มิว · ก๋วยเตี๋ยวต้มยำ "ไม่ใส่ผัก!!"), the clock
//                                        (o.clock "13:18") and the countdown o.eta [from, to] seconds over the shot
//   QkUI.eta(tl, layer, t0, dur, o)      the HUD chip top-left (a slab): scooter coin, ห้อง 2714, the countdown o.eta [from, to] (00:00 → "ถึงแล้ว")
//   QkUI.choice(tl, layer, t0, dur, o)   the first-person choice: o.q, o.a / o.b { text, icon } on 3D cards, a 3-2-1 ring on a bezel (o.secs),
//                                        the hovered card lifts with its shadow, then o.pick at o.pickAt; o.mark { at, wrong } stamps ✗ / ✓
//   QkUI.rewind(tl, layer, t0, dur, o)   VHS rewind over the shot: tracking bars, colour fringes, ◀◀, a clock running back (o.from → o.to)
//   QkUI.note(tl, layer, t0, dur, o)     แม่'s note on the fridge = the rule card: textured paper with a curled corner, 3D magnets and tape,
//                                        3 rhyming rules with coin stickers; o.active (1–3) gets a highlighter swipe and its sticker animates,
//                                        o.done ticks, later rules are faint pencil; o.at [t…] (seconds into the shot) when each row lands · o.out
//   QkUI.labels(tl, layer, t0, o)        telestrator call-outs: o.items [{ x, y, lx, ly, text, icon, at, dur, end }] — a glowing bead on the
//                                        body, a line (with its shadow) that draws to a 3D pill with a moving coin
//   QkUI.seismo(tl, layer, t0, dur, o)   a seismograph screen in a bezel: the glowing trace draws itself (main shock, aftershocks), pills, "หลบซ้ำ"
//   QkUI.quakeMap(tl, L, sid, t0, o)     on Sets.mapTH (id o.map): an epicentre burst in Myanmar with rings that sweep over Bangkok, the
//                                        Bangkok pin with a swaying tower and a counter "โยกนานกว่า 20 วินาที" (o.count [start, end]), the date chip
//   QkUI.call(tl, layer, t0, dur, o)     a phone (3D) in a hand calling "แม่ ♥": rings, then "ไม่มีผู้รับสาย" (o.failAt)
//   QkUI.endCard(tl, layer, t0, dur, o)  the end card: มิว's orange whistle (3D) on its twisted lanyard with a paper tag (o.l1 "ตอนที่ 2", o.l2)
//   QkUI.ICON.<name>()                   2.5D coins in a 120-unit box (face centre 60,57 r 52, the rim below it, a soft shadow at y 120):
//                                        duck cover hold table lift stairs whistle candle torch · QkUI.icon(name, x, y, s, id) places one ·
//                                        QkUI.iconLife(tl, root, t, dur) its secondary motion · QkUI.iconPop(tl, root, t) its squash-and-stretch entry
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;
  const nid = () => `qu${++seq}`;
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mmss = (s) => { s = Math.max(0, Math.round(s)); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`; };
  const hex = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  const tone = (h, k) => { const c = hex(h), t = k >= 0 ? 255 : 0, a = Math.abs(k); return "#" + c.map((v) => Math.round(v + (t - v) * a).toString(16).padStart(2, "0")).join(""); };
  // a damped wobble as an ease: goes 0 → ±1 … → 0 (use with fromTo { x: 0 } → { x: amplitude })
  const wobble = (n = 4) => (p) => Math.sin(p * Math.PI * 2 * n) * (1 - p);

  // coin palettes: face, face highlight, rim, rim shade
  const PAL = {
    duck: ["#fde59a", "#fffbe8", "#e3a632", "#a8741a"],
    cover: ["#c4e4f6", "#f4fbff", "#4f9cc8", "#2e6e96"],
    hold: ["#f8d4c2", "#fff5ef", "#d8845e", "#a85a38"],
    table: ["#d8f0c8", "#f7fff2", "#6aaa52", "#44803a"],
    lift: ["#dfe5ea", "#ffffff", "#8a98a4", "#5c6a76"],
    stairs: ["#d8f0c8", "#f7fff2", "#6aaa52", "#44803a"],
    whistle: ["#fddcbc", "#fff6ee", "#e8823a", "#b4561a"],
    candle: ["#2c3858", "#56688e", "#e09a40", "#a86a1e"],
    torch: ["#2c3858", "#56688e", "#5a8ac8", "#345e96"],
  };
  let coinDefs = "";
  for (const [n, [b, l, r, rd]] of Object.entries(PAL)) coinDefs += `<radialGradient id="quF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${l}"/><stop offset=".5" stop-color="${b}"/><stop offset="1" stop-color="${tone(b, -0.2)}"/></radialGradient>
    <linearGradient id="quR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset=".55" stop-color="${tone(r, -0.12)}"/><stop offset="1" stop-color="${rd}"/></linearGradient>`;

  Sets.DEFS += `${coinDefs}
    <linearGradient id="quPanel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16201f" stop-opacity=".94"/><stop offset="1" stop-color="#0b1112" stop-opacity=".94"/></linearGradient>
    <linearGradient id="quNote" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf4"/><stop offset="1" stop-color="#f3ead4"/></linearGradient>
    <linearGradient id="quHi" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe45a" stop-opacity=".78"/><stop offset=".85" stop-color="#ffd23a" stop-opacity=".62"/><stop offset="1" stop-color="#ffd23a" stop-opacity=".35"/></linearGradient>
    <radialGradient id="quBurst"><stop offset="0" stop-color="#fff2b0"/><stop offset=".35" stop-color="#ff8a3a" stop-opacity=".85"/><stop offset="1" stop-color="#e8382a" stop-opacity="0"/></radialGradient>
    <linearGradient id="quTag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8f0dc"/><stop offset="1" stop-color="#e2d2ae"/></linearGradient>
    <filter id="quDrop" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="9"/><feOffset dy="12"/><feComponentTransfer><feFuncA type="linear" slope=".45"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <radialGradient id="quCoinSh"><stop offset="0" stop-color="#000" stop-opacity=".42"/><stop offset=".6" stop-color="#000" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="quSoftSh"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset=".55" stop-color="#000" stop-opacity=".28"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <linearGradient id="quBev" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/><stop offset=".58" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
    <clipPath id="quPicClip" clipPathUnits="userSpaceOnUse"><circle cx="60" cy="60" r="51"/></clipPath>
    <radialGradient id="quHead" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6a5a4c"/><stop offset="1" stop-color="#241a14"/></radialGradient>
    <radialGradient id="quSkin" cx=".35" cy=".3" r=".85"><stop offset="0" stop-color="#fadcbc"/><stop offset=".6" stop-color="#e8b88e"/><stop offset="1" stop-color="#c08660"/></radialGradient>
    <linearGradient id="quSkinL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d0aa"/><stop offset=".6" stop-color="#e2ad80"/><stop offset="1" stop-color="#b87e58"/></linearGradient>
    <linearGradient id="quGrn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#52c87a"/><stop offset="1" stop-color="#1f8246"/></linearGradient>
    <linearGradient id="quGrnS" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5cd286"/><stop offset="1" stop-color="#22884a"/></linearGradient>
    <linearGradient id="quWoodF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8925e"/><stop offset="1" stop-color="#8a5a36"/></linearGradient>
    <linearGradient id="quWoodV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c08a58"/><stop offset=".45" stop-color="#a87448"/><stop offset="1" stop-color="#6e4628"/></linearGradient>
    <linearGradient id="quSteelI" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8e979e"/><stop offset=".35" stop-color="#e8ecee"/><stop offset=".6" stop-color="#b4bbc0"/><stop offset="1" stop-color="#7e878e"/></linearGradient>
    <linearGradient id="quRedA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7e66"/><stop offset="1" stop-color="#cc261c"/></linearGradient>
    <radialGradient id="quOr" cx=".3" cy=".25" r=".9"><stop offset="0" stop-color="#ffd2a2"/><stop offset=".42" stop-color="#f88c34"/><stop offset="1" stop-color="#c25810"/></radialGradient>
    <linearGradient id="quOrM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb070"/><stop offset="1" stop-color="#d0641a"/></linearGradient>
    <radialGradient id="quHole" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#2a1004"/><stop offset=".7" stop-color="#6a2a08"/><stop offset="1" stop-color="#a84a12"/></radialGradient>
    <linearGradient id="quCylW" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="#faf3e2"/><stop offset="1" stop-color="#d2c2a2"/></linearGradient>
    <linearGradient id="quCylK" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a7078"/><stop offset=".3" stop-color="#a2aab0"/><stop offset=".55" stop-color="#3a4046"/><stop offset="1" stop-color="#1c2024"/></linearGradient>
    <linearGradient id="quYel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe680"/><stop offset=".5" stop-color="#f6c230"/><stop offset="1" stop-color="#c08a10"/></linearGradient>
    <linearGradient id="quBrass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f2d690"/><stop offset=".5" stop-color="#d4aa4a"/><stop offset="1" stop-color="#9a7224"/></linearGradient>
    <radialGradient id="quFlameG" cx=".5" cy=".72" r=".75"><stop offset="0" stop-color="#fffde6"/><stop offset=".38" stop-color="#ffd85a"/><stop offset="1" stop-color="#ff7a1a"/></radialGradient>
    <radialGradient id="quFlameGlow"><stop offset="0" stop-color="#ffe9a0" stop-opacity=".9"/><stop offset=".45" stop-color="#ffb43a" stop-opacity=".32"/><stop offset="1" stop-color="#ffb43a" stop-opacity="0"/></radialGradient>
    <linearGradient id="quBeamG" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff6c0" stop-opacity=".98"/><stop offset=".55" stop-color="#ffe680" stop-opacity=".55"/><stop offset="1" stop-color="#ffe680" stop-opacity="0"/></linearGradient>
    <linearGradient id="quCylS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9aa2aa"/><stop offset=".3" stop-color="#e8ecef"/><stop offset=".6" stop-color="#8a929a"/><stop offset="1" stop-color="#4a5258"/></linearGradient>
    <linearGradient id="quCardF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#253432"/><stop offset=".45" stop-color="#172221"/><stop offset="1" stop-color="#0d1514"/></linearGradient>
    <linearGradient id="quCardGloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="quGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe98a"/><stop offset=".55" stop-color="#ffd23a"/><stop offset="1" stop-color="#e2a812"/></linearGradient>
    <linearGradient id="quCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbf2"/><stop offset="1" stop-color="#ece0c4"/></linearGradient>
    <linearGradient id="quPillD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#352c24"/><stop offset="1" stop-color="#120d09"/></linearGradient>
    <radialGradient id="quBead" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fffbd0"/><stop offset=".45" stop-color="#ffd23a"/><stop offset="1" stop-color="#b8860e"/></radialGradient>
    <radialGradient id="quGlowGold"><stop offset="0" stop-color="#ffd23a" stop-opacity=".75"/><stop offset=".5" stop-color="#ffd23a" stop-opacity=".22"/><stop offset="1" stop-color="#ffd23a" stop-opacity="0"/></radialGradient>
    <radialGradient id="quRedC" cx=".35" cy=".3" r=".85"><stop offset="0" stop-color="#ff8a78"/><stop offset=".55" stop-color="#e2392c"/><stop offset="1" stop-color="#a81e16"/></radialGradient>
    <radialGradient id="quGrnC" cx=".35" cy=".3" r=".85"><stop offset="0" stop-color="#7ae49a"/><stop offset=".55" stop-color="#22a85a"/><stop offset="1" stop-color="#0f6a36"/></radialGradient>
    <linearGradient id="quBezel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2e6e8"/><stop offset=".35" stop-color="#7e8890"/><stop offset=".6" stop-color="#d8dde0"/><stop offset="1" stop-color="#4e585e"/></linearGradient>
    <linearGradient id="quBezelD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a5458"/><stop offset=".3" stop-color="#262e30"/><stop offset=".7" stop-color="#1a2022"/><stop offset="1" stop-color="#3a4346"/></linearGradient>
    <radialGradient id="quScreen" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="#1c2a28"/><stop offset="1" stop-color="#080e0d"/></radialGradient>
    <linearGradient id="quGlare" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="quPhoneB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a626a"/><stop offset=".08" stop-color="#262b31"/><stop offset=".92" stop-color="#1a1e22"/><stop offset="1" stop-color="#4a525a"/></linearGradient>
    <linearGradient id="quCallScr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a5a8e"/><stop offset="1" stop-color="#18284a"/></linearGradient>
    <radialGradient id="quHeart" cx=".35" cy=".3" r=".85"><stop offset="0" stop-color="#ff8a8a"/><stop offset=".55" stop-color="#e2302c"/><stop offset="1" stop-color="#a0161a"/></radialGradient>
    <linearGradient id="quHud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2a26"/><stop offset="1" stop-color="#0a120f"/></linearGradient>
    <linearGradient id="quTitleF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset=".55" stop-color="#f6ecd8"/><stop offset="1" stop-color="#e2c69a"/></linearGradient>
    <linearGradient id="quEpF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6a56"/><stop offset="1" stop-color="#c4221a"/></linearGradient>
    <linearGradient id="quLanyard" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8601e"/><stop offset=".35" stop-color="#ff9a52"/><stop offset="1" stop-color="#c4561a"/></linearGradient>
    <linearGradient id="quRing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f4f6"/><stop offset=".5" stop-color="#8a949c"/><stop offset="1" stop-color="#d8dde0"/></linearGradient>
    <pattern id="quPaper" width="90" height="90" patternUnits="userSpaceOnUse"><path d="M8,12l14,3M40,30l9,-4M66,58l16,2M18,70l7,6M58,8l5,9M80,30l-6,10M30,48l12,1" stroke="#9a8a62" stroke-width="1.2" opacity=".16"/>
      <circle cx="26" cy="22" r="1.2" fill="#8a7a52" opacity=".2"/><circle cx="72" cy="44" r="1" fill="#8a7a52" opacity=".2"/><circle cx="48" cy="80" r="1.3" fill="#8a7a52" opacity=".18"/><circle cx="10" cy="54" r=".9" fill="#8a7a52" opacity=".2"/></pattern>`;

  // ---------------- 2.5D coins (120-unit box; the pictogram lives in the old 0–120 disc space and is scaled into the face) ----------------
  const cube = (s = 1) => `<g transform="scale(${s})"><path d="M-7,-3.5L0,-7L7,-3.5L0,0Z" fill="#dccdb6"/><path d="M-7,-3.5L0,0V8L-7,4.5Z" fill="#a8947c"/><path d="M7,-3.5L0,0V8L7,4.5Z" fill="#7a6854"/>
    <path d="M-7,-3.5L0,-7L7,-3.5V4.5L0,8L-7,4.5Z" fill="none" stroke="${INK}" stroke-width="2" stroke-linejoin="round"/><path d="M-7,-3.5L0,0L7,-3.5M0,0V8" fill="none" stroke="${INK}" stroke-width="1.2" opacity=".6"/></g>`;
  const crouch = (o) => `<g class="quAn" data-a="duck"><g class="quAnS" data-o="${o}">`;
  // each icon: [clipped inside the face, drawn on top unclipped]
  const PICT = {
    // หมอบ: a figure dropping low, the arrow pushing it down
    duck: () => [`<ellipse cx="60" cy="97" rx="31" ry="5" fill="${INK}" opacity=".2"/>
      ${crouch("60 94")}<path d="M44,86L35,96M76,86L85,96" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>
        <path d="M60,61Q41,67 40,89H80Q79,67 60,61Z" fill="url(#quGrn)" ${OUT(3.5)}/><path d="M61,62Q75,68 77,87H67Q66,71 61,62Z" fill="#14582e" opacity=".35"/>
        <path d="M47,75Q50,68 57,65" stroke="#b4f5c8" stroke-width="3" fill="none" opacity=".75" stroke-linecap="round"/>
        <circle cx="60" cy="51" r="10" fill="url(#quHead)" ${OUT(3)}/><circle cx="56.5" cy="47.5" r="3" fill="#fff" opacity=".5"/></g></g>
      <path d="M24,100H96" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`,
    `<g class="quArr"><path d="M54,8H66V22H75L60,38L45,22H54Z" fill="#7a140e" transform="translate(2.5,3)"/><path d="M54,8H66V22H75L60,38L45,22H54Z" fill="url(#quRedA)" ${OUT(3)}/>
        <path d="M57.5,11.5V23" stroke="#ffd8d0" stroke-width="3" opacity=".85" stroke-linecap="round"/></g>`],
    // ป้อง: both arms over the head, bits bouncing off
    cover: () => [`<path d="M34,110Q36,91 60,89Q84,91 86,110Z" fill="url(#quGrn)" ${OUT(3.5)}/><path d="M62,90Q80,92 84,108H70Q70,96 62,90Z" fill="#14582e" opacity=".3"/>
      <circle cx="60" cy="72" r="17" fill="url(#quSkin)" ${OUT(4)}/>
      <path d="M33,84Q30,50 60,47Q90,50 87,84" fill="none" stroke="${INK}" stroke-width="17" stroke-linecap="round"/><path d="M33,84Q30,50 60,47Q90,50 87,84" fill="none" stroke="url(#quGrnS)" stroke-width="10" stroke-linecap="round"/>
      <path d="M37,70Q38,54 57,51" fill="none" stroke="#b4f5c8" stroke-width="3" opacity=".8" stroke-linecap="round"/>
      <circle cx="33" cy="86" r="6.5" fill="url(#quSkin)" ${OUT(2.5)}/><circle cx="87" cy="86" r="6.5" fill="url(#quSkin)" ${OUT(2.5)}/>`,
    `<g class="quBits"><g transform="translate(46,22)"><g class="quBitR">${cube(1.1)}</g></g><g transform="translate(75,27)"><g class="quBitR">${cube(0.85)}</g></g></g>`],
    // เกาะ: a hand gripping a table leg (the sleeve comes in from outside the coin)
    hold: () => [`<ellipse cx="60" cy="104" rx="40" ry="5" fill="${INK}" opacity=".18"/>
      <g class="quTbl"><rect x="27" y="44" width="11" height="58" fill="url(#quWoodV)" ${OUT(3)}/><rect x="81" y="44" width="11" height="58" fill="url(#quWoodV)" ${OUT(3)}/>
        <path d="M22,27H98L106,36H14Z" fill="#e8be8e" ${OUT(3)}/><rect x="14" y="36" width="92" height="10" fill="url(#quWoodF)" ${OUT(3)}/><path d="M26,31.5H74" stroke="#fff4e0" stroke-width="2.5" opacity=".8" stroke-linecap="round"/></g>
      <g class="quGrip"><path d="M95,65H124V93H95Z" fill="url(#quGrn)" ${OUT(3)}/><path d="M97,82H124" stroke="#e8f0e8" stroke-width="4" opacity=".85"/>
        <path d="M70,63Q93,55 99,71Q103,90 85,94L72,91Q66,78 70,63Z" fill="url(#quSkin)" ${OUT(3.5)}/><path d="M77,66V90M85,66V91M92,68V88" stroke="#a8704a" stroke-width="2.4"/>
        <path d="M74,67Q80,63 88,62" stroke="#fff" stroke-width="2.5" opacity=".55" fill="none" stroke-linecap="round"/></g>`, ""],
    // หมอบใต้โต๊ะ: the whole drill — crouched under a table, arms over the head, a bit falling on the top
    table: () => [`<ellipse cx="60" cy="102" rx="46" ry="5" fill="${INK}" opacity=".18"/>
      <g class="quTbl"><rect x="19" y="46" width="10" height="55" fill="url(#quWoodV)" ${OUT(3)}/><rect x="91" y="46" width="10" height="55" fill="url(#quWoodV)" ${OUT(3)}/>
        <path d="M18,28H102L110,37H10Z" fill="#e8be8e" ${OUT(3)}/><rect x="10" y="37" width="100" height="10" fill="url(#quWoodF)" ${OUT(3)}/><path d="M22,32.5H70" stroke="#fff4e0" stroke-width="2.5" opacity=".8" stroke-linecap="round"/></g>
      ${crouch("60 99")}<path d="M60,79Q43,83 41,99H79Q77,83 60,79Z" fill="url(#quGrn)" ${OUT(3)}/><path d="M61,80Q74,84 77,98H68Q67,87 61,80Z" fill="#14582e" opacity=".32"/>
        <circle cx="60" cy="71" r="8.5" fill="url(#quHead)" ${OUT(3)}/>
        <path d="M47,76Q47,60 60,59Q73,60 73,76" stroke="${INK}" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M47,76Q47,60 60,59Q73,60 73,76" stroke="#3cb868" stroke-width="5" fill="none" stroke-linecap="round"/></g></g>
      <path d="M12,101H108" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`,
    `<g class="quBits"><g transform="translate(62,14)"><g class="quBitR">${cube(1)}</g></g></g>`],
    // วิ่งไปลิฟต์: lift doors in a deep frame with the floor display, a running figure
    lift: () => [`<rect x="30" y="24" width="62" height="82" rx="3" fill="#56606a" ${OUT(4)}/><path d="M32,26H90L85,31H37Z" fill="#8a96a2"/>
      <rect x="36" y="31" width="50" height="75" fill="#262c32"/><rect x="37" y="32" width="24" height="74" fill="url(#quSteelI)"/><rect x="61" y="32" width="24" height="74" fill="url(#quSteelI)"/>
      <path d="M61,32V106" stroke="${INK}" stroke-width="2.5"/><path d="M43,37V100M67,37V100" stroke="#fff" stroke-width="3" opacity=".55"/>
      <path d="M22,106H100" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`,
    `<g class="quRun"><path d="M21,59L15,77" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><path d="M21,59L15,77" stroke="#3cb868" stroke-width="5.5" stroke-linecap="round"/>
        <path d="M15,77L23,91M15,77L6,87M20,63L30,69M20,63L10,67" stroke="${INK}" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="22" cy="50" r="7" fill="url(#quHead)" ${OUT(2.5)}/></g>
      <rect x="43" y="10" width="36" height="15" rx="4" fill="#0c0c0e" transform="translate(1.5,2.5)" opacity=".5"/><rect x="43" y="10" width="36" height="15" rx="4" fill="#161618" ${OUT(2.5)}/>
      <path d="M49.5,21.5l4.5,-7l4.5,7z" fill="#ff6a3a"/><path d="M63.5,14.5l4.5,7l4.5,-7z" fill="#ffb03a"/>`],
    // ลงบันได ไม่ใช่ลิฟต์: 3D steps going down to the right, a figure walking down them, a no-lift sticker
    stairs: () => [`<path d="M26,42H46V54H66V66H86V78H106V100H26Z" fill="#6e4628" ${OUT(2.5)}/>
      ${[[20, 40, 48], [40, 60, 60], [60, 80, 72], [80, 100, 84]].map(([a, b, y]) => `<path d="M${a},${y}H${b}L${b + 6},${y - 6}H${a + 6}Z" fill="#f0cc9e" ${OUT(2)}/>`).join("")}
      <path d="M100,84L106,78V100L100,104Z" fill="#8a5a36" ${OUT(2)}/>
      <path d="M20,48H40V60H60V72H80V84H100V104H20Z" fill="url(#quWoodF)" ${OUT(3)}/><path d="M23,51H37M43,63H57M63,75H77M83,87H97" stroke="#ffe6c4" stroke-width="2" opacity=".55"/>
      <g transform="translate(29,47)"><g class="quAn" data-a="walk"><g class="quStep"><path d="M0,-21V-9" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M0,-21V-9" stroke="#3cb868" stroke-width="4" stroke-linecap="round"/>
        <path d="M0,-9L-4,0M0,-9L5,-1M0,-18L6,-12M0,-18L-6,-13" stroke="${INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/><circle cx="0" cy="-27" r="5.5" fill="url(#quHead)" ${OUT(2)}/></g></g></g>`,
    `<g transform="translate(90,28)"><circle cy="3.5" r="16" fill="#8a140e"/><circle r="16" fill="#fff" stroke="#d8312a" stroke-width="5"/><rect x="-6.5" y="-9" width="13" height="18" fill="url(#quSteelI)" stroke="${INK}" stroke-width="1.5"/>
      <path d="M0,-9V9" stroke="${INK}" stroke-width="1.2"/><path d="M-11,11L11,-11" stroke="#d8312a" stroke-width="5"/><path d="M-9,-6A11,11 0 0 1 -2,-11" stroke="#fff" stroke-width="2" fill="none" opacity=".8"/></g>`],
    // ติดใต้ซาก: the whistle blowing, sound waves puffing out (rule 3)
    whistle: () => ["", `<g transform="translate(48,66) rotate(-10)"><path d="M-22,-10H12Q28,-10 28,8Q28,26 8,26Q-8,26 -10,12H-22Z" fill="#9a400c" transform="translate(2,5)"/>
        <path d="M-22,-10H12Q28,-10 28,8Q28,26 8,26Q-8,26 -10,12H-22Z" fill="url(#quOr)" ${OUT(4)}/>
        <rect x="-38" y="-10" width="18" height="13" rx="3" fill="url(#quOrM)" ${OUT(3)}/><ellipse cx="-38" cy="-3.5" rx="2.2" ry="4.6" fill="#5a2406"/>
        <circle cx="8" cy="8" r="7" fill="url(#quHole)" ${OUT(2.5)}/><path d="M-16,-5H10Q20,-5 22,4" stroke="#ffe6cc" stroke-width="4" fill="none" opacity=".85" stroke-linecap="round"/>
        <circle cx="-38" cy="-12" r="5" fill="none" stroke="url(#quRing)" stroke-width="3"/></g>
      <g class="quWave">${[0, 1, 2].map((k) => `<path class="quWv" d="M${83 + k * 9},${41 - k * 6}q${8},${16 + k * 6} 0,${32 + k * 12}" stroke="#d8312a" stroke-width="5.5" fill="none" stroke-linecap="round"/>`).join("")}</g>`],
    // จุดเทียน: a candle in a brass dish, the flame flickering in its glow
    candle: () => ["", `<circle class="quGlow" cx="60" cy="40" r="44" fill="url(#quFlameGlow)"/>
      <ellipse cx="60" cy="101" rx="25" ry="7" fill="#7a5a1a"/><ellipse cx="60" cy="98" rx="25" ry="7" fill="url(#quBrass)" ${OUT(3)}/>
      <rect x="49" y="47" width="22" height="52" rx="3" fill="url(#quCylW)" ${OUT(3.5)}/><ellipse cx="60" cy="47" rx="11" ry="3.6" fill="#fffef8" ${OUT(2.5)}/>
      <path d="M52.5,48v11q0,4 3,4q3,0 3,-4v-9" fill="#fffef8" stroke="${INK}" stroke-width="2"/><path d="M60,47V40" stroke="${INK}" stroke-width="2.5"/>
      <path class="quFlame" d="M60,14Q74,31 67,41Q60,48 53,41Q46,31 60,14Z" fill="url(#quFlameG)" ${OUT(3)}/><path class="quFlame2" d="M60,28Q65,35 62.5,40Q60,42 57.5,40Q55,35 60,28Z" fill="#fffbe6"/>`],
    // ใช้ไฟฉาย: a torch, its beam sweeping
    torch: () => ["", `<g transform="rotate(-30 60 60)"><path class="quBeam" d="M49,42L28,0H92L71,42Z" fill="url(#quBeamG)"/>
        <rect x="50" y="56" width="20" height="46" rx="5" fill="url(#quCylS)" ${OUT(3.5)}/><path d="M52,72H68M52,78H68M52,84H68M52,90H68" stroke="#3a4048" stroke-width="2" opacity=".6"/>
        <rect x="56" y="61" width="8" height="6" rx="2" fill="#d8312a" ${OUT(1.5)}/><path d="M46,42H74L70,57H50Z" fill="url(#quYel)" ${OUT(3)}/>
        <ellipse cx="60" cy="42" rx="14" ry="3.6" fill="#fffbe0" ${OUT(2.5)}/><path d="M54,60V97" stroke="#fff" stroke-width="2.5" opacity=".35"/></g>`],
  };
  const coin = (name) => {
    const [inside, top] = PICT[name]();
    return `<ellipse class="quSh" cx="60" cy="120" rx="50" ry="9" fill="url(#quCoinSh)"/>
      <g class="quBob"><g class="quSq">
        <circle cx="60" cy="66" r="52" fill="url(#quR-${name})" ${OUT(4)}/><path d="M12,66A48,48 0 0 0 108,66" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
        <circle cx="60" cy="57" r="52" fill="url(#quF-${name})" ${OUT(4)}/>
        <circle cx="60" cy="57" r="45.5" fill="none" stroke="url(#quBev)" stroke-width="4"/>
        <g transform="translate(60,57) scale(.9) translate(-60,-60)">${inside ? `<g clip-path="url(#quPicClip)">${inside}</g>` : ""}${top}</g>
        <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle cx="53.5" cy="15.5" r="2.8" fill="#fff" opacity=".7"/>
      </g></g>`;
  };
  const ICON = Object.fromEntries(Object.keys(PICT).map((n) => [n, () => coin(n)]));
  const icon = (name, x, y, s = 1, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>${ICON[name]()}</g></g>`;
  // squash-and-stretch entry of a coin (stretched tall → squashed wide → settles)
  function iconPop(tl, root, t) {
    if (!root) return;
    root.querySelectorAll(".quSq").forEach((e) => tl.fromTo(e, { scaleX: 0.3, scaleY: 1.5, svgOrigin: "60 117" }, { scaleX: 1, scaleY: 1, svgOrigin: "60 117", duration: 0.75, ease: "elastic.out(1, 0.42)", immediateRender: false }, t));
  }
  // secondary motion inside a coin, from t until t + dur
  function iconLife(tl, root, t, dur) {
    if (!root) return;
    const q = (s) => root.querySelectorAll(s), n = Math.max(1, Math.round(dur / 0.5)), R = (p) => Math.ceil(dur / p) + 1;
    // the coin floats, its shadow shrinks and fades as it rises
    q(".quBob").forEach((e) => tl.fromTo(e, { y: 0 }, { y: -5, duration: 0.85, repeat: R(0.85), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".quSh").forEach((e) => tl.fromTo(e, { scaleX: 1, opacity: 1, svgOrigin: "60 120" }, { scaleX: 0.8, opacity: 0.55, svgOrigin: "60 120", duration: 0.85, repeat: R(0.85), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    // the arrow shoves down (accelerating), springs back
    q(".quArr").forEach((e) => tl.fromTo(e, { y: -6 }, { y: 7, duration: 0.32, repeat: R(0.32), yoyo: true, ease: "power2.in", immediateRender: false }, t));
    // the figure drops: stretched while high, squashed when it lands
    q('.quAn[data-a="duck"]').forEach((e) => tl.fromTo(e, { y: -8 }, { y: 2, duration: 0.42, repeat: R(0.42), yoyo: true, ease: "power2.in", immediateRender: false }, t));
    q('.quAn[data-a="duck"] .quAnS').forEach((e) => { const o = e.dataset.o || "60 94"; tl.fromTo(e, { scaleX: 0.95, scaleY: 1.08, svgOrigin: o }, { scaleX: 1.12, scaleY: 0.86, svgOrigin: o, duration: 0.42, repeat: R(0.42), yoyo: true, ease: "power3.in", immediateRender: false }, t); });
    // debris drops, bounces off the arms / tabletop, tumbling
    q(".quBits").forEach((e) => tl.fromTo(e, { y: -18, opacity: 0 }, { y: 14, opacity: 1, duration: 0.6, repeat: n, ease: "bounce.out", immediateRender: false }, t));
    q(".quBitR").forEach((e, i) => tl.fromTo(e, { rotation: 0, svgOrigin: "0 0" }, { rotation: i % 2 ? -220 : 220, svgOrigin: "0 0", duration: 0.6, repeat: n, ease: "power2.out", immediateRender: false }, t));
    q(".quTbl").forEach((e) => tl.fromTo(e, { x: -3 }, { x: 3, duration: 0.08, repeat: R(0.08), yoyo: true, ease: "none", immediateRender: false }, t));
    q(".quGrip").forEach((e) => tl.fromTo(e, { x: 2.5 }, { x: -2.5, duration: 0.08, repeat: R(0.08), yoyo: true, ease: "none", immediateRender: false }, t));
    q(".quRun").forEach((e) => tl.fromTo(e, { x: -6 }, { x: 8, duration: 0.3, repeat: R(0.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    // walking down the stairs, a step bob on top
    q('.quAn[data-a="walk"]').forEach((e) => tl.fromTo(e, { x: 0, y: 0 }, { x: 44, y: 25, duration: 1.3, repeat: R(1.3), ease: "none", immediateRender: false }, t));
    q(".quStep").forEach((e) => tl.fromTo(e, { y: 0 }, { y: -3, duration: 0.16, repeat: R(0.16), yoyo: true, ease: "power1.out", immediateRender: false }, t));
    // the whistle's waves puff outward one after another
    q(".quWv").forEach((e, i) => tl.fromTo(e, { scale: 0.55, opacity: 1, svgOrigin: "74 58" }, { scale: 1.25, opacity: 0, svgOrigin: "74 58", duration: 0.6, repeat: R(0.6), ease: "power1.out", immediateRender: false }, t + i * 0.14));
    // the flame flickers inside its breathing glow
    q(".quFlame").forEach((e) => tl.fromTo(e, { scaleY: 0.86, scaleX: 1.06, svgOrigin: "60 44" }, { scaleY: 1.14, scaleX: 0.94, svgOrigin: "60 44", duration: 0.11, repeat: R(0.11), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".quFlame2").forEach((e) => tl.fromTo(e, { scale: 0.85, svgOrigin: "60 41" }, { scale: 1.12, svgOrigin: "60 41", duration: 0.17, repeat: R(0.17), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".quGlow").forEach((e) => tl.fromTo(e, { scale: 0.88, opacity: 0.75, svgOrigin: "60 40" }, { scale: 1.1, opacity: 1, svgOrigin: "60 40", duration: 0.26, repeat: R(0.26), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    // the torch beam sweeps
    q(".quBeam").forEach((e) => tl.fromTo(e, { rotation: -9, opacity: 0.8, svgOrigin: "60 42" }, { rotation: 9, opacity: 1, svgOrigin: "60 42", duration: 0.75, repeat: R(0.75), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
  }

  // ---------------- shared 3D pieces ----------------
  // a slab: a darker body `d` px under a lit face; o.face / o.body fills, o.stroke, o.sw, o.gloss
  const slab = (x, y, w, h, r, o = {}) => `<rect x="${x}" y="${y + (o.d ?? 10)}" width="${w}" height="${h}" rx="${r}" fill="${o.body || "#05090a"}" stroke="${o.bodyStroke || INK}" stroke-width="${o.sw ?? 4}"/>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${o.face || "url(#quCardF)"}" stroke="${o.stroke || INK}" stroke-width="${o.sw ?? 4}"${o.strokeOp ? ` stroke-opacity="${o.strokeOp}"` : ""}/>
    ${o.gloss === false ? "" : `<rect x="${x + r * 0.5}" y="${y + 5}" width="${w - r}" height="${Math.min(h * 0.42, 60)}" rx="${Math.min(r, h * 0.21)}" fill="url(#quCardGloss)"/>`}`;
  // a stamp coin (✗ / ✓) at cx, cy
  const stamp = (cx, cy, r, good) => `<circle cx="${cx}" cy="${cy + 10}" r="${r}" fill="${good ? "#0a4a26" : "#6a0e0a"}" stroke="#140e0a" stroke-width="5"/>
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#${good ? "quGrnC" : "quRedC"})" stroke="#fff" stroke-width="7"/>
    <path d="M${cx - r * 0.62},${cy - r * 0.2}A${r * 0.66},${r * 0.66} 0 0 1 ${cx - r * 0.12},${cy - r * 0.64}" stroke="#fff" stroke-width="6" fill="none" opacity=".55" stroke-linecap="round"/>
    ${good ? `<path d="M${cx - 32},${cy + 4}l22,24l40,-46" stroke="#05301a" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".5" transform="translate(0,5)"/><path d="M${cx - 32},${cy}l22,24l40,-46" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`
      : `<path d="M${cx - 26},${cy - 21}L${cx + 26},${cy + 31}M${cx + 26},${cy - 21}L${cx - 26},${cy + 31}" stroke="#4a0806" stroke-width="16" stroke-linecap="round" opacity=".5"/><path d="M${cx - 26},${cy - 26}L${cx + 26},${cy + 26}M${cx + 26},${cy - 26}L${cx - 26},${cy + 26}" stroke="#fff" stroke-width="14" stroke-linecap="round"/>`}`;

  // ---------------- the opener title ----------------
  function title(tl, layer, t0, dur, o = {}) {
    const id = nid(), DEP = 13;
    // a seismograph trace: flat, then the swing
    let tr = "M90,0";
    for (let x = 90; x <= 990; x += 6) { const k = (x - 90) / 900, a = k < 0.25 ? 3 : 70 * Math.sin(Math.PI * Math.min(1, (k - 0.25) / 0.6)) * (k < 0.85 ? 1 : 0.4); tr += `L${x},${f1(Math.sin(x * 0.23) * a + Math.sin(x * 0.61) * a * 0.35)}`; }
    const T = (attrs, tf = "") => `<text x="540" y="470" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="210"${tf ? ` transform="${tf}"` : ""} ${attrs}>ตึกโยก</text>`;
    let ext = "";
    for (let k = DEP; k >= 1; k--) ext += T(`fill="${tone("#a8341e", -0.75 * (k / DEP))}"${k === DEP ? ` stroke="#140e0a" stroke-width="12" stroke-linejoin="round" paint-order="stroke"` : ""}`, `translate(${f1(k * 0.55)},${f1(k * 1.35)})`);
    const dash = `pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"`;
    put(layer, `<g id="${id}" opacity="0"><rect x="0" y="120" width="1080" height="680" fill="url(#${id}g)"/>
      <defs><linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05090c" stop-opacity=".78"/><stop offset=".7" stop-color="#05090c" stop-opacity=".45"/><stop offset="1" stop-color="#05090c" stop-opacity="0"/></linearGradient></defs>
      <text x="540" y="268" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" letter-spacing="16" fill="#000" opacity=".5" transform="translate(0,3)">ROD MAI CLUB</text>
      <text x="540" y="268" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" letter-spacing="16" fill="#f4ecd8" opacity=".9">ROD MAI CLUB</text>
      <g transform="translate(0,${560 + 8})" opacity=".45"><path class="${id}-d" d="${tr}" stroke="#000" stroke-width="8" fill="none" stroke-linejoin="round" ${dash}/></g>
      <g transform="translate(0,560)"><path class="${id}-d" d="${tr}" stroke="#ff3a2a" stroke-width="20" fill="none" stroke-linejoin="round" opacity=".28" ${dash}/>
        <path class="${id}-d" d="${tr}" stroke="#ff4a3a" stroke-width="7" fill="none" stroke-linejoin="round" ${dash}/>
        <path class="${id}-d" d="${tr}" stroke="#ffd2c8" stroke-width="2" fill="none" stroke-linejoin="round" opacity=".85" ${dash}/></g>
      <g id="${id}-m"><g id="${id}-s"><g id="${id}-t">
        <ellipse cx="560" cy="520" rx="330" ry="26" fill="url(#quSoftSh)" opacity=".7"/>
        ${ext}
        ${T(`fill="url(#quTitleF)" stroke="#140e0a" stroke-width="12" stroke-linejoin="round" paint-order="stroke"`)}
        ${T(`fill="none" stroke="#fff" stroke-width="3" opacity=".55"`, "translate(-2,-3)")}
        <path d="M640,300l-20,60l26,22l-30,52l18,30" stroke="#140e0a" stroke-width="10" fill="none" stroke-linejoin="round"/><path d="M640,300l-20,60l26,22l-30,52l18,30" stroke="#ff6a3a" stroke-width="3.5" fill="none" stroke-linejoin="round"/></g></g></g>
      <g transform="translate(540,668)"><g id="${id}-ep" opacity="0"><g id="${id}-eps">${slab(-252, -46, 504, 82, 41, { face: "url(#quEpF)", body: "#6a120c", stroke: "#140e0a", sw: 6, d: 9 })}
        <text x="0" y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#5a0c08" opacity=".55" transform="translate(0,3)">${o.ep || "EP.1 · หมอบ ป้อง เกาะ"}</text>
        <text x="0" y="13" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#fff6ea">${o.ep || "EP.1 · หมอบ ป้อง เกาะ"}</text></g></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    // the letters drop in stretched, land squashed, spring back, then sway like the tower
    tl.fromTo(`#${id}-m`, { y: -340 }, { y: 0, duration: 0.38, ease: "power3.in", immediateRender: false }, t0);
    tl.fromTo(`#${id}-s`, { scaleX: 0.86, scaleY: 1.2, svgOrigin: "540 500" }, { scaleX: 0.9, scaleY: 1.14, svgOrigin: "540 500", duration: 0.38, ease: "none", immediateRender: false }, t0);
    tl.fromTo(`#${id}-s`, { scaleX: 1.22, scaleY: 0.74, svgOrigin: "540 500" }, { scaleX: 1, scaleY: 1, svgOrigin: "540 500", duration: 0.8, ease: "elastic.out(1, 0.38)", immediateRender: false }, t0 + 0.38);
    tl.fromTo(`#${id}-t`, { rotation: 0, svgOrigin: "540 500" }, { rotation: -3.5, svgOrigin: "540 500", duration: 0.45, ease: "sine.out", immediateRender: false }, t0 + 0.75);
    tl.fromTo(`#${id}-t`, { rotation: -3.5, svgOrigin: "540 500" }, { rotation: 3.5, svgOrigin: "540 500", duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.2);
    tl.fromTo(`.${id}-d`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.5, ease: "power1.inOut", immediateRender: false }, t0 + 0.3);
    tl.fromTo(`#${id}-ep`, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, t0 + 0.75);
    tl.fromTo(`#${id}-eps`, { scaleX: 0.4, scaleY: 1.5, svgOrigin: "0 40" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 40", duration: 0.75, ease: "elastic.out(1, 0.45)", immediateRender: false }, t0 + 0.75);
    tl.fromTo(`#${id}-s`, { scaleX: 1, scaleY: 1, svgOrigin: "540 500" }, { scaleX: 0.9, scaleY: 0.9, svgOrigin: "540 500", duration: 0.3, ease: "power2.in", immediateRender: false }, t0 + dur - 0.3);
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  // ---------------- the rider app in your hand ----------------
  function app(tl, layer, t0, dur, o = {}) {
    const id = nid(), X = 540, Y = o.y ?? 1180, W = 560, H = 1040, [e0, e1] = o.eta || [120, 110], x0 = -W / 2, y0 = -H / 2;
    // the city map in the app: blocks with a lit top and a shadow, a park, the river, roads with casings, the route with a glow,
    // the condo as a 3D block with the pin on it
    let map = `<rect x="-240" y="-160" width="480" height="300" rx="18" fill="#e9efe6"/>
      <path d="M-240,108C-150,96 -80,112 0,92S160,60 240,48V140H-240Z" fill="#a8d4ea"/><path d="M-240,108C-150,96 -80,112 0,92S160,60 240,48" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>
      <path d="M-200,124q14,-5 28,0M-60,118q14,-5 28,0M90,96q14,-5 28,0" stroke="#fff" stroke-width="2.5" fill="none" opacity=".6"/>
      <rect x="-228" y="-150" width="112" height="96" rx="12" fill="#bfe2a8"/>${[[-206, -126, 11], [-178, -104, 14], [-148, -132, 10], [-140, -84, 12], [-196, -76, 9]].map(([x, y, r]) => `<circle cx="${x + 2}" cy="${y + 4}" r="${r}" fill="#6aa85a" opacity=".5"/><circle cx="${x}" cy="${y}" r="${r}" fill="#8ec878"/>`).join("")}`;
    for (const [bx, by, bw, bh] of [[-86, -150, 92, 58], [14, -150, 92, 34], [-228, -26, 110, 56], [-86, -26, 92, 46], [14, -26, 92, 30], [130, -26, 98, 20]]) map += `<rect x="${bx + 4}" y="${by + 6}" width="${bw}" height="${bh}" rx="6" fill="#c8ccc4"/><rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="6" fill="#fbfbf6" stroke="#d8dcd2" stroke-width="2"/>`;
    map += `<path d="M-240,-40H240M-100,-160V140M120,-160V140M-240,80L240,10" stroke="#c8d0c4" stroke-width="18"/><path d="M-240,-40H240M-100,-160V140M120,-160V140M-240,80L240,10" stroke="#fff" stroke-width="13"/>
      <path d="M134,-96L140,-102H190L184,-96Z" fill="#b8d0e6" stroke="#5a7a98" stroke-width="2" stroke-linejoin="round"/><path d="M184,-96L190,-102V-66L184,-60Z" fill="#4a6a88" stroke="#5a7a98" stroke-width="2" stroke-linejoin="round"/>
      <rect x="134" y="-96" width="50" height="36" fill="#7a9ab8" stroke="#5a7a98" stroke-width="2"/><path d="M140,-88H178M140,-80H178M140,-72H178" stroke="#d8ecf8" stroke-width="2.5" opacity=".8"/>
      <path d="M-200,74L-100,59.5L-100,-40L120,-40L150,-60" stroke="#2fa45a" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".22"/>
      <path id="${id}-route" d="M-200,74L-100,59.5L-100,-40L120,-40L150,-60" stroke="#1f9a4e" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
      <circle id="${id}-me" cx="-200" cy="74" r="26" fill="#2a5cb8" opacity=".22"/><circle cx="-200" cy="74" r="13" fill="#2a5cb8" stroke="#fff" stroke-width="4"/>
      <ellipse cx="160" cy="-99" rx="13" ry="4" fill="#000" opacity=".3"/>
      <g transform="translate(160,-100)"><g id="${id}-pin" opacity="0"><path d="M0,0C-18,-20 -21,-33 -21,-41A21,21 0 0 1 21,-41C21,-33 18,-20 0,0Z" fill="url(#quRedC)" ${OUT(3)}/><circle cy="-41" r="7.5" fill="#fff"/><path d="M-13,-49A15,15 0 0 1 -3,-57" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/></g></g>
      <g transform="translate(36,-118)"><rect x="-88" y="-17" width="176" height="40" rx="20" fill="#000" opacity=".12"/><rect x="-88" y="-22" width="176" height="40" rx="20" fill="#fff" stroke="#c8d0c4" stroke-width="2"/><text y="7" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="25" fill="#2a3a2a">เดอะสกาย 32</text></g>`;
    // the noodle bowl icon for the order
    const bowl = `<g transform="translate(205,-12)"><path d="M-26,-6C-30,6 -24,18 0,22C24,18 30,6 26,-6Z" fill="#e8f0f4" ${OUT(2.5)}/><path d="M-26,-6H26" stroke="#d8312a" stroke-width="4"/>
      <path d="M-14,-10q3,-10 -2,-18M0,-10q3,-10 -2,-18M14,-10q3,-10 -2,-18" stroke="#c8ccce" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>`;
    put(layer, `<g id="${id}" transform="translate(${X},${Y})" opacity="0"><g id="${id}-in">
      <ellipse cx="40" cy="${H / 2 + 40}" rx="${W / 2}" ry="40" fill="url(#quSoftSh)" opacity=".5"/>
      <path d="M-330,520Q-362,300 -300,180L-250,120L-196,560Z" fill="url(#quGrn)" ${OUT(5)}/><path d="M-300,190Q-330,320 -318,500" stroke="#7ee0a2" stroke-width="7" fill="none" opacity=".5" stroke-linecap="round"/><path d="M-340,420H-210" stroke="#e8f0e8" stroke-width="16" opacity=".85"/>
      <rect x="${x0 + 12}" y="${y0 + 16}" width="${W}" height="${H}" rx="56" fill="#0a0c0e" ${OUT(5)}/>
      <rect x="${x0}" y="${y0}" width="${W}" height="${H}" rx="56" fill="url(#quPhoneB)" ${OUT(5)}/>
      <rect x="${x0 - 7}" y="${y0 + 170}" width="8" height="70" rx="3" fill="#3a4048" ${OUT(2)}/><rect x="${x0 - 7}" y="${y0 + 260}" width="8" height="110" rx="3" fill="#3a4048" ${OUT(2)}/>
      <rect x="${x0 + 18}" y="${y0 + 18}" width="${W - 36}" height="${H - 36}" rx="42" fill="#f4f6f4"/>
      <rect x="${x0 + 18}" y="${y0 + 18}" width="${W - 36}" height="150" rx="42" fill="#2fa45a"/><rect x="${x0 + 18}" y="${y0 + 120}" width="${W - 36}" height="48" fill="#2fa45a"/><rect x="${x0 + 18}" y="${y0 + 160}" width="${W - 36}" height="10" fill="#000" opacity=".08"/>
      <rect x="${-60}" y="${y0 + 30}" width="120" height="30" rx="15" fill="#06080a"/>
      <text x="${x0 + 60}" y="${y0 + 62}" font-family="Kanit" font-weight="700" font-size="28" fill="#e8f6ec">${o.clock || "13:18"}</text>
      <g transform="translate(${x0 + 96},${y0 + 118})"><circle cy="3" r="30" fill="#1a6a38"/><circle r="30" fill="#fff4dc" ${OUT(3)}/><path d="M-17,-2h34q-2,17 -17,19q-15,-2 -17,-19z" fill="#e2a92e" ${OUT(2)}/></g>
      <text x="${x0 + 140}" y="${y0 + 130}" font-family="Kanit" font-weight="800" font-size="40" fill="#fff">อิ่มด่วน · ไรเดอร์</text>
      <g transform="translate(0,${y0 + 334})">${map}</g>
      <g transform="translate(0,${y0 + 560})"><text x="-220" y="0" font-family="Kanit" font-weight="800" font-size="46" fill="#1e2228">ห้อง 2714 · มิว</text>
        <text x="-220" y="56" font-family="Kanit" font-weight="400" font-size="32" fill="#3a4a3a">ก๋วยเตี๋ยวต้มยำ x1</text>${bowl}
        <g id="${id}-noteg" opacity="0"><rect x="-226" y="84" width="452" height="64" rx="14" fill="#e2a92e"/><rect x="-226" y="78" width="452" height="64" rx="14" fill="#fff1c8" stroke="#e2a92e" stroke-width="3"/><text x="0" y="122" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#c8281e">"ไม่ใส่ผัก!! ไม่ใส่ผัก!!"</text></g></g>
      <g transform="translate(0,${H / 2 - 150})">${slab(-240, -60, 480, 120, 30, { face: "url(#quPillD)", body: "#000", sw: 0, d: 8 })}<text x="-200" y="14" font-family="Kanit" font-weight="700" font-size="32" fill="#cfe8d4">ส่งภายใน</text>
        <text id="${id}-eta" x="200" y="22" text-anchor="end" font-family="Kanit" font-weight="900" font-size="66" fill="#ffd23a">${mmss(e0)}</text></g>
      <path d="M${x0 + 18},${y0 + 60}L${x0 + 260},${y0 + 18}H${x0 + 420}L${x0 + 18},${y0 + 380}Z" fill="url(#quGlare)"/>
      <path d="M${x0 + 30},${y0 + 520}L${W / 2 - 18},${y0 + 230}V${y0 + 290}L${x0 + 30},${y0 + 590}Z" fill="#fff" opacity=".05"/>
      <path d="M${x0 + 8},${y0 + 90}V${H / 2 - 90}" stroke="#fff" stroke-width="3" opacity=".22" stroke-linecap="round"/>
      <path d="M${W / 2 - 20},-120Q${W / 2 + 40},-110 ${W / 2 + 46},-40Q${W / 2 + 48},0 ${W / 2 - 10},10" fill="url(#quSkinL)" ${OUT(4)}/><path d="M${W / 2 + 14},-100Q${W / 2 + 34},-80 ${W / 2 + 34},-50" stroke="#fff" stroke-width="3" opacity=".4" fill="none" stroke-linecap="round"/>
      <path d="M-${W / 2 + 10},-60Q-${W / 2 + 60},-40 -${W / 2 + 56},40Q-${W / 2 + 50},80 -${W / 2 - 14},80" fill="url(#quSkinL)" ${OUT(4)}/><path d="M-${W / 2 + 34},-40Q-${W / 2 + 46},0 -${W / 2 + 40},30" stroke="#fff" stroke-width="3" opacity=".4" fill="none" stroke-linecap="round"/></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { y: 700, rotation: 8, svgOrigin: "0 0" }, { y: 0, rotation: -3, svgOrigin: "0 0", duration: 0.55, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-route`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 1.2, ease: "power2.inOut", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-me`, { attr: { r: 14 }, opacity: 0.5 }, { attr: { r: 34 }, opacity: 0, duration: 0.9, repeat: Math.ceil(dur / 0.9), ease: "power1.out", immediateRender: false }, t0 + 0.3);
    tl.fromTo(`#${id}-pin`, { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "bounce.out", immediateRender: false }, t0 + 0.75);
    tl.fromTo(`#${id}-noteg`, { scaleX: 0.3, scaleY: 1.4, opacity: 1, svgOrigin: "0 110" }, { scaleX: 1, scaleY: 1, opacity: 1, svgOrigin: "0 110", duration: 0.6, ease: "elastic.out(1, 0.45)", immediateRender: false }, t0 + 0.9);
    const el = document.getElementById(`${id}-eta`), c = { v: e0 };
    tl.fromTo(c, { v: e0 }, { v: e1, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { el.textContent = mmss(c.v); } }, t0);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  }

  // ---------------- the HUD chip ----------------
  function eta(tl, layer, t0, dur, o = {}) {
    const id = nid(), [e0, e1] = o.eta || [100, 80], w = o.w ?? 400;
    put(layer, `<g transform="translate(${o.x ?? 40},${o.y ?? 150})"><g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-s">
      <rect y="7" width="${w}" height="96" rx="48" fill="#020605" opacity=".85"/><rect width="${w}" height="96" rx="48" fill="url(#quHud)" opacity=".94"/>
      <rect x="22" y="5" width="${w - 44}" height="34" rx="17" fill="url(#quCardGloss)"/><rect width="${w}" height="96" rx="48" fill="none" stroke="#2fa45a" stroke-width="4"/>
      <g transform="translate(52,48)"><circle cy="4" r="34" fill="#0d4a26"/><circle r="34" fill="url(#quGrnC)" stroke="#0a2a16" stroke-width="2.5"/><path d="M-22,-12A26,26 0 0 1 -6,-24" stroke="#fff" stroke-width="3.5" fill="none" opacity=".5" stroke-linecap="round"/>
        <path d="M-20,8L-6,-12H10L20,8M-6,-12L-10,-20" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="-20" cy="10" r="7" fill="#fff"/><circle cx="20" cy="10" r="7" fill="#fff"/></g>
      <text x="100" y="40" font-family="Kanit" font-weight="700" font-size="26" fill="#cfe8d4">ห้อง 2714</text>
      <text x="100" y="83" font-family="Kanit" font-weight="900" font-size="40" fill="#000" opacity=".45">${"ส่งภายใน " + mmss(e0)}</text>
      <text id="${id}-v" x="100" y="80" font-family="Kanit" font-weight="900" font-size="40" fill="#ffd23a">ส่งภายใน ${mmss(e0)}</text></g></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: o.pop === false ? 0.01 : 0.2, immediateRender: false }, t0);
    if (o.pop !== false) {
      tl.fromTo(`#${id}-m`, { x: -70 }, { x: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0);
      tl.fromTo(`#${id}-s`, { scaleX: 0.8, scaleY: 1.18, svgOrigin: "0 48" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 48", duration: 0.75, ease: "elastic.out(1, 0.5)", immediateRender: false }, t0);
    }
    const el = document.getElementById(`${id}-v`), sh = el.previousElementSibling, c = { v: e0 };
    tl.fromTo(c, { v: e0 }, { v: e1, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { const s = c.v <= 0.5 ? "ถึงแล้ว!" : `ส่งภายใน ${mmss(c.v)}`; el.textContent = s; sh.textContent = s; el.setAttribute("fill", c.v <= 10.5 ? "#ff6a4a" : "#ffd23a"); } }, t0);
    if (e1 <= 0.5) tl.fromTo(`#${id}-s`, { scale: 1, svgOrigin: "200 48" }, { scale: 1.12, svgOrigin: "200 48", duration: 0.15, repeat: 5, yoyo: true, immediateRender: false }, t0 + dur * (e0 / Math.max(0.01, e0 - e1)) - 0.1);
    if (o.out) { tl.fromTo(`#${id}-s`, { scale: 1, svgOrigin: "0 48" }, { scale: 0.85, svgOrigin: "0 48", duration: 0.2, ease: "power2.in", immediateRender: false }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + o.out); }
  }

  // ---------------- the first-person choice ----------------
  function choice(tl, layer, t0, dur, o = {}) {
    const id = nid(), secs = o.secs ?? 3, A = o.a, B = o.b, Y = [o.yA ?? 880, o.yB ?? 1190], SX = 352;
    const card = (k, c) => `<g transform="translate(540,${Y[k]})"><g id="${id}-e${k}" opacity="0"><g id="${id}-q${k}"><g id="${id}-c${k}">
        <rect id="${id}-sh${k}" x="-440" y="-112" width="880" height="290" rx="60" fill="url(#quSoftSh)" opacity=".85"/>
        <g id="${id}-l${k}">
          ${slab(-430, -130, 860, 260, 34, { face: "url(#quCardF)", body: "#020404", stroke: "#f4ecd8", strokeOp: 0.3, sw: 4, d: 12 })}
          <g id="${id}-f${k}" opacity="0"><rect x="-440" y="-140" width="880" height="280" rx="42" fill="none" stroke="#ffd23a" stroke-width="22" opacity=".22"/><rect x="-436" y="-136" width="872" height="272" rx="38" fill="none" stroke="#ffd23a" stroke-width="9"/></g>
          <g transform="translate(-388,-88)"><rect x="-25" y="-21" width="50" height="46" rx="12" fill="#7a5a08"/><rect x="-25" y="-27" width="50" height="46" rx="12" fill="url(#quGold)" stroke="#140e0a" stroke-width="3"/>
            <text y="7" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#140e0a">${k ? "B" : "A"}</text></g>
          ${icon(c.icon, -330, -100, 1.6, `${id}-i${k}`)}
          <text x="-110" y="29" font-family="Kanit" font-weight="900" font-size="74" fill="#000" opacity=".5">${c.text}</text><text x="-110" y="24" font-family="Kanit" font-weight="900" font-size="74" fill="#f6efe0">${c.text}</text>
          <g id="${id}-xr${k}" opacity="0"><circle cx="${SX}" cy="0" r="60" fill="none" stroke="#ff5a46" stroke-width="10"/></g>
          <g id="${id}-x${k}" opacity="0">${stamp(SX, 0, 60, false)}</g>
          <g id="${id}-vr${k}" opacity="0"><circle cx="${SX}" cy="0" r="60" fill="none" stroke="#5aef8a" stroke-width="10"/></g>
          <g id="${id}-v${k}" opacity="0">${stamp(SX, 0, 60, true)}</g></g></g></g></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#05090c" opacity=".42"/>
      <g transform="translate(540,560)"><g id="${id}-qe"><g id="${id}-qs">
        <ellipse cx="0" cy="88" rx="380" ry="34" fill="url(#quSoftSh)" opacity=".6"/>
        ${slab(-400, -70, 800, 140, 70, { face: "url(#quCream)", body: "#a8946a", stroke: "#140e0a", sw: 6, d: 10 })}
        <text x="-40" y="22" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#1e1a16">${o.q || "คุณจะทำยังไง?"}</text>
        <g transform="translate(300,0)"><circle cy="6" r="60" fill="#3a3e42"/><circle r="60" fill="url(#quBezel)" stroke="#140e0a" stroke-width="4"/><circle r="49" fill="#16120f"/>
          <circle id="${id}-ring" r="40" fill="none" stroke="#ffd23a" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0" transform="rotate(-90)"/>
          <path d="M-36,-14A38,38 0 0 1 -14,-36" stroke="#fff" stroke-width="3" fill="none" opacity=".25" stroke-linecap="round"/>
          <text id="${id}-n" y="20" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#fff">${secs}</text></g></g></g></g>
      ${card(0, A)}${card(1, B)}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.18, immediateRender: false }, t0);
    tl.fromTo(`#${id}-qe`, { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-qs`, { scaleX: 0.5, scaleY: 1.35, svgOrigin: "0 70" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 70", duration: 0.7, ease: "elastic.out(1, 0.45)", immediateRender: false }, t0);
    [0, 1].forEach((k) => {
      const t = t0 + 0.12 + k * 0.14;
      tl.fromTo(`#${id}-e${k}`, { y: 140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power3.out", immediateRender: false }, t);
      tl.fromTo(`#${id}-q${k}`, { scaleX: 0.72, scaleY: 1.22, svgOrigin: "0 130" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 130", duration: 0.85, ease: "elastic.out(1, 0.5)", immediateRender: false }, t);
      iconPop(tl, document.getElementById(`${id}-i${k}`), t);
      iconLife(tl, document.getElementById(`${id}-i${k}`), t0 + 0.9, dur);
    });
    const ring = { k: 0 }, n = document.getElementById(`${id}-n`), ringEl = document.getElementById(`${id}-ring`), T = o.pickAt ?? secs;
    tl.fromTo(ring, { k: 0 }, { k: 1, duration: T, ease: "none", immediateRender: false, onUpdate: () => { ringEl.setAttribute("stroke-dashoffset", f1(ring.k)); n.textContent = String(Math.max(0, Math.ceil(secs * (1 - ring.k) - 0.001))); } }, t0);
    // each second ticks: the number pops
    for (let m = secs - 1; m >= 1; m--) { const tm = t0 + T * (1 - m / secs); if (tm > t0 + 0.05) tl.fromTo(n, { scale: 1.4, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)", immediateRender: false }, tm); }
    // the cursor: hovers A, B, A… then lands on the pick; the hovered card lifts off its shadow
    const hov = o.hover || [[0.4, 0], [1.0, 1], [1.6, 0]], pick = o.pick === "b" ? 1 : 0, up = [0, 0];
    const focus = (t, k) => {
      tl.set(`#${id}-f${k}`, { opacity: 1 }, t); tl.set(`#${id}-f${1 - k}`, { opacity: 0 }, t);
      if (!up[k]) { tl.fromTo(`#${id}-l${k}`, { y: 0 }, { y: -16, duration: 0.22, ease: "back.out(3)", immediateRender: false }, t); tl.fromTo(`#${id}-sh${k}`, { scale: 1, opacity: 0.85, svgOrigin: "0 30" }, { scale: 1.05, opacity: 0.6, svgOrigin: "0 30", duration: 0.22, ease: "power2.out", immediateRender: false }, t); up[k] = 1; }
      if (up[1 - k]) { tl.fromTo(`#${id}-l${1 - k}`, { y: -16 }, { y: 0, duration: 0.18, ease: "power2.out", immediateRender: false }, t); tl.fromTo(`#${id}-sh${1 - k}`, { scale: 1.05, opacity: 0.6, svgOrigin: "0 30" }, { scale: 1, opacity: 0.85, svgOrigin: "0 30", duration: 0.18, ease: "power2.out", immediateRender: false }, t); up[1 - k] = 0; }
    };
    hov.forEach(([t, k]) => focus(t0 + t, k));
    focus(t0 + T, pick);
    // the pick: pressed in (squash), springs back, the other card dims
    tl.fromTo(`#${id}-c${pick}`, { scaleX: 1, scaleY: 1, svgOrigin: "0 0" }, { scaleX: 1.07, scaleY: 0.93, svgOrigin: "0 0", duration: 0.1, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + T);
    tl.fromTo(`#${id}-c${1 - pick}`, { opacity: 1 }, { opacity: 0.35, duration: 0.15, immediateRender: false }, t0 + T);
    if (o.mark) {
      const { at, wrong = "a" } = o.mark, w = wrong === "a" ? 0 : 1, ta = t0 + at, tb = t0 + at + 0.4;
      tl.fromTo(`#${id}-x${w}`, { opacity: 0, scale: 2.6, rotation: -25, svgOrigin: `${SX} 0` }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: `${SX} 0`, duration: 0.28, ease: "back.out(3)", immediateRender: false }, ta);
      tl.fromTo(`#${id}-xr${w}`, { opacity: 0.9, scale: 1, svgOrigin: `${SX} 0` }, { opacity: 0, scale: 2, svgOrigin: `${SX} 0`, duration: 0.45, ease: "power2.out", immediateRender: false }, ta + 0.2);
      tl.fromTo(`#${id}-l${w}`, { x: 0 }, { x: 14, duration: 0.4, ease: wobble(4), immediateRender: false }, ta + 0.2);
      tl.fromTo(`#${id}-c${w}`, { opacity: w === pick ? 1 : 0.35 }, { opacity: 0.45, duration: 0.2, immediateRender: false }, ta + 0.25);
      tl.fromTo(`#${id}-c${1 - w}`, { opacity: 1 - w === pick ? 1 : 0.35 }, { opacity: 1, duration: 0.1, immediateRender: false }, ta + 0.25);
      focus(ta + 0.25, 1 - w);
      tl.fromTo(`#${id}-v${1 - w}`, { opacity: 0, scale: 2.6, rotation: 25, svgOrigin: `${SX} 0` }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: `${SX} 0`, duration: 0.32, ease: "back.out(3)", immediateRender: false }, tb);
      tl.fromTo(`#${id}-vr${1 - w}`, { opacity: 0.9, scale: 1, svgOrigin: `${SX} 0` }, { opacity: 0, scale: 2, svgOrigin: `${SX} 0`, duration: 0.5, ease: "power2.out", immediateRender: false }, tb + 0.22);
      tl.fromTo(`#${id}-q${1 - w}`, { scaleX: 1, scaleY: 1, svgOrigin: "0 130" }, { scaleX: 1.06, scaleY: 0.94, svgOrigin: "0 130", duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, tb + 0.22);
    }
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.15 }, t0 + o.out);
    return id;
  }

  // ---------------- VHS rewind ----------------
  function rewind(tl, layer, t0, dur, o = {}) {
    const id = nid();
    const bars = [0, 1, 2].map((k) => `<rect id="${id}-b${k}" x="0" y="0" width="1080" height="${60 + k * 30}" fill="#fff" opacity=".2"/>`).join("");
    let lines = ""; for (let y = 0; y < 1920; y += 8) lines += `<path d="M0,${y}H1080" stroke="#000" stroke-width="3" opacity=".16"/>`;
    const fr = [[340, "#ff3a5a"], [780, "#3ae0ff"], [1220, "#ff3a5a"], [1530, "#3ae0ff"]].map(([y, c], k) => `<rect id="${id}-fr${k}" x="0" y="${y}" width="1080" height="${6 + k * 2}" fill="${c}" opacity=".35"/>`).join("");
    const rw = (dx, c) => `<g transform="translate(${dx},0)"><path d="M60,0L0,40L60,80ZM130,0L70,40L130,80Z" fill="${c}"/><text x="160" y="64" font-family="Kanit" font-weight="900" font-size="64" fill="${c}" letter-spacing="4">ย้อนกลับ</text></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#2a3a6a" opacity=".22"/>${lines}${bars}${fr}
      <g transform="translate(70,190)"><g opacity=".55">${rw(-4, "#ff3a5a")}${rw(4, "#3ae0ff")}</g><g transform="translate(0,6)" opacity=".45">${rw(0, "#000")}</g>${rw(0, "#fff")}</g>
      ${o.from ? `<g transform="translate(1010,254)"><rect x="-200" y="-58" width="214" height="78" rx="16" fill="#000" opacity=".35"/><text id="${id}-tc" x="0" y="0" text-anchor="end" font-family="Kanit" font-weight="700" font-size="56" fill="#fff">${o.from}</text></g>` : ""}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.08, immediateRender: false }, t0);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-b${k}`, { y: 1920 * (k / 3) }, { y: -400, duration: 0.45 + k * 0.1, repeat: Math.ceil(dur / 0.45), ease: "none", immediateRender: false }, t0));
    [0, 1, 2, 3].forEach((k) => tl.fromTo(`#${id}-fr${k}`, { x: -30, y: 0 }, { x: 30, y: k % 2 ? 60 : -60, duration: 0.07 + k * 0.02, repeat: Math.ceil(dur / 0.07), yoyo: true, ease: "none", immediateRender: false }, t0));
    if (o.from && o.to) { const tc = document.getElementById(`${id}-tc`), [h0, m0] = o.from.split(":").map(Number), [h1, m1] = o.to.split(":").map(Number), c = { v: h0 * 60 + m0 };
      tl.fromTo(c, { v: h0 * 60 + m0 }, { v: h1 * 60 + m1, duration: dur * 0.8, ease: "power2.inOut", immediateRender: false, onUpdate: () => { const v = Math.round(c.v); tc.textContent = `${Math.floor(v / 60)}:${String(v % 60).padStart(2, "0")}`; } }, t0); }
    tl.to(`#${id}`, { opacity: 0, duration: 0.12 }, t0 + dur - 0.12);
  }

  // ---------------- แม่'s note on the fridge: the rule card ----------------
  const RULES = [
    ["duck", "ตึกโยก อย่า<u>วิ่ง</u>", "หมอบ ป้อง เกาะ อย่า<u>ทิ้ง</u>"],
    ["stairs", "หยุดสั่นแล้ว<u>ไป</u>", "ลงบัน<u>ได</u> ไม่ใช่ลิฟต์"],
    ["whistle", "ติดใต้<u>ซาก</u> อย่าอ้า<u>ปาก</u>ตะโกน", "เคาะท่อ เป่านกหวีด"],
  ];
  // a 3D magnet: a glossy sphere and its shadow on the paper
  const magnet = (x, y, c) => `<ellipse cx="${x + 10}" cy="${y + 22}" rx="36" ry="24" fill="url(#quSoftSh)" opacity=".7"/>
    <circle cx="${x}" cy="${y}" r="34" fill="url(#${c})" stroke="${tone(c === "quMagB" ? "#1e5a8a" : "#8a6a10", 0)}" stroke-width="3"/>
    <ellipse cx="${x - 11}" cy="${y - 13}" rx="11" ry="7" fill="#fff" opacity=".75" transform="rotate(-30 ${x - 11} ${y - 13})"/><circle cx="${x + 12}" cy="${y + 14}" r="4" fill="#fff" opacity=".25"/>`;
  Sets.DEFS += `<radialGradient id="quMagB" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#9ad4ff"/><stop offset=".5" stop-color="#3aa0e8"/><stop offset="1" stop-color="#1a5a96"/></radialGradient>
    <radialGradient id="quMagY" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff2a8"/><stop offset=".5" stop-color="#f2c230"/><stop offset="1" stop-color="#a87a10"/></radialGradient>
    <linearGradient id="quCurl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8ccb0"/><stop offset=".5" stop-color="#fffaf0"/><stop offset="1" stop-color="#e4d8bc"/></linearGradient>
    <linearGradient id="quCurlSh" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".3"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>`;
  function note(tl, layer, t0, dur, o = {}) {
    const id = nid(), act = o.active ?? 1, done = o.done || [], at = o.at || [0.6, 1.4, 2.2], Y0 = o.y ?? 250;
    const row = (k) => {
      const [ic, l1, l2] = RULES[k], st = k + 1 === act ? "act" : done.includes(k + 1) ? "done" : "later", y = 300 + k * 300;
      const col = st === "later" ? "#8a8478" : "#2a2420", u = (s) => s.replace(/<u>(.*?)<\/u>/g, `<tspan class="quU" fill="${st === "later" ? "#8a8478" : "#c8281e"}">$1</tspan>`);
      return `<g id="${id}-r${k}" opacity="${st === "later" ? 0.38 : 0}">
        ${st === "act" ? `<path id="${id}-hl" opacity="0" d="M252,${y - 92}Q560,${y - 104} 862,${y - 90}L858,${y + 84}Q560,${y + 92} 250,${y + 80}Z" fill="url(#quHi)"/>` : ""}
        <g transform="translate(70,${y - 100})"><g id="${id}-s${k}"${st === "later" ? ` filter="url(#quGray)"` : st === "act" ? ` opacity="0"` : ""}>${icon(ic, 0, 0, 1.5, `${id}-ic${k}`)}</g></g>
        <text x="270" y="${y - 22}" font-family="Mali" font-weight="700" font-size="${l1.replace(/<[^>]+>/g, "").length > 20 ? 50 : 60}" fill="${col}">${u(l1)}</text>
        <text x="270" y="${y + 58}" font-family="Mali" font-weight="700" font-size="${l2.length > 22 ? 50 : 56}" fill="${col}">${u(l2)}</text>
        ${st === "done" ? `<g id="${id}-tk${k}" opacity="0"><path d="M74,${y - 10}l40,40l80,-90" stroke="#1e9a50" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>` : ""}
        ${k < 2 ? `<path d="M60,${y + 130}H960" stroke="#c8dce8" stroke-width="3" stroke-dasharray="4 10"/>` : ""}</g>`;
    };
    put(layer, `<defs><filter id="quGray"><feColorMatrix type="saturate" values="0"/></filter></defs>
      <g id="${id}" transform="translate(40,${Y0})" opacity="0"><g id="${id}-m"><g id="${id}-s"><g id="${id}-w"><g id="${id}-p" filter="url(#quDrop)">
      <path d="M0,20Q0,0 20,0H980Q1000,0 1000,20V1104L904,1200H20Q0,1200 0,1180Z" fill="url(#quNote)" stroke="#d8ccb0" stroke-width="3"/>
      <path d="M0,20Q0,0 20,0H980Q1000,0 1000,20V1104L904,1200H20Q0,1200 0,1180Z" fill="url(#quPaper)"/>
      <path d="M0,20Q0,0 20,0H980Q1000,0 1000,20V60H0Z" fill="#fff" opacity=".35"/>
      ${Array.from({ length: 11 }, (_, k) => `<path d="M40,${180 + k * 96}H${k > 9 ? 900 : 960}" stroke="#bcd4e6" stroke-width="2" opacity=".7"/>`).join("")}<path d="M150,40V1160" stroke="#f0a8a8" stroke-width="3"/>
      <text x="500" y="118" text-anchor="middle" font-family="Mali" font-weight="700" font-size="58" fill="#c8281e">ถ้าตึกโยก… จำไว้นะลูก</text>
      ${[0, 1, 2].map(row).join("")}
      <text x="880" y="1150" text-anchor="end" font-family="Mali" font-weight="700" font-size="48" fill="#c8281e">♥ แม่</text>
      <path d="M1000,1104L904,1200L960,1080Z" fill="url(#quCurlSh)" opacity=".8"/>
      <path d="M1000,1104L904,1200Q918,1128 1000,1104Z" fill="url(#quCurl)" stroke="#c8b890" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M990,1110Q930,1124 914,1184" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>
      <g transform="translate(60,1150) rotate(-38)"><path d="M-90,-26L-82,-18L-90,-10L-82,-2L-90,6L-82,14L-90,22H90L82,14L90,6L82,-2L90,-10L82,-18L90,-26Z" fill="#f2e6b8" opacity=".82" stroke="#d8c890" stroke-width="1.5"/>
        <path d="M-80,-16H80" stroke="#fff" stroke-width="5" opacity=".4"/></g>
      ${magnet(120, 30, "quMagB")}${magnet(880, 30, "quMagY")}</g></g></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    tl.fromTo(`#${id}-m`, { x: -120, y: 220 }, { x: 0, y: 0, duration: 0.6, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-s`, { scale: 0.35, rotation: -9, svgOrigin: "500 600" }, { scale: 1, rotation: -1.5, svgOrigin: "500 600", duration: 0.6, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-w`, { rotation: -1, svgOrigin: "500 0" }, { rotation: 1, svgOrigin: "500 0", duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.6);
    // the rows in ink land when they are read (later rows stay faint pencil from the start)
    [0, 1, 2].forEach((k) => { if (k + 1 === act || done.includes(k + 1)) tl.fromTo(`#${id}-r${k}`, { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + at[k]); });
    const a = act - 1;
    if (a >= 0 && a < 3) {
      tl.fromTo(`#${id}-hl`, { scaleX: 0, opacity: 1, svgOrigin: "250 0" }, { scaleX: 1, opacity: 1, svgOrigin: "250 0", duration: 0.5, ease: "power2.inOut", immediateRender: false }, t0 + at[a] + 0.2);
      tl.fromTo(`#${id}-s${a}`, { scale: 0, rotation: -40, opacity: 1, svgOrigin: "90 90" }, { scale: 1, rotation: 0, opacity: 1, svgOrigin: "90 90", duration: 0.5, ease: "back.out(2.6)", immediateRender: false }, t0 + at[a]);
      iconPop(tl, document.getElementById(`${id}-ic${a}`), t0 + at[a]);
      iconLife(tl, document.getElementById(`${id}-ic${a}`), t0 + at[a] + 0.6, dur);
      document.getElementById(`${id}-r${a}`).querySelectorAll(".quU").forEach((u, j) => { const fs = +u.parentNode.getAttribute("font-size"); u.setAttribute("font-size", fs); tl.fromTo(u, { attr: { "font-size": fs } }, { attr: { "font-size": Math.round(fs * 1.2) }, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + at[a] + 0.7 + j * 0.25); });
    }
    done.forEach((d) => { const el = document.getElementById(`${id}-tk${d - 1}`); if (el) tl.fromTo(el, { opacity: 0, scale: 2, svgOrigin: `130 ${300 + (d - 1) * 300}` }, { opacity: 1, scale: 1, svgOrigin: `130 ${300 + (d - 1) * 300}`, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t0 + at[d - 1] + 0.3); });
    if (o.out !== undefined) { tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + o.out); tl.to(`#${id}-m`, { y: -40, duration: 0.25 }, t0 + o.out); }
  }

  // ---------------- call-outs on the bodies ----------------
  function labels(tl, layer, t0, o = {}) {
    (o.items || []).forEach((it) => {
      const id = nid(), at = t0 + (it.at ?? 0), w = 90 + it.text.length * 42, cx = (w - 70) / 2;
      const dash = `pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"`;
      put(layer, `<g id="${id}" opacity="0">
        <path class="${id}-ln" d="M${it.x + 5},${it.y + 8}L${it.lx + 5},${it.ly + 8}" stroke="#000" stroke-opacity=".45" stroke-width="10" stroke-linecap="round" ${dash}/>
        <path class="${id}-ln" d="M${it.x},${it.y}L${it.lx},${it.ly}" stroke="#ffd23a" stroke-width="8" stroke-linecap="round" ${dash}/>
        <path class="${id}-ln" d="M${it.x},${it.y - 2}L${it.lx},${it.ly - 2}" stroke="#fff6c0" stroke-width="2.5" stroke-linecap="round" opacity=".8" ${dash}/>
        <circle cx="${it.x}" cy="${it.y}" r="40" fill="url(#quGlowGold)"/><circle id="${id}-pu" cx="${it.x}" cy="${it.y}" r="16" fill="none" stroke="#ffd23a" stroke-width="6"/>
        <circle cx="${it.x + 2}" cy="${it.y + 4}" r="16" fill="#000" opacity=".35"/><circle cx="${it.x}" cy="${it.y}" r="16" fill="url(#quBead)" stroke="#140e0a" stroke-width="4"/><circle cx="${it.x - 5}" cy="${it.y - 5}" r="4.5" fill="#fff" opacity=".85"/>
        <g transform="translate(${it.lx},${it.ly})"><g id="${id}-pl" opacity="0"><g id="${id}-pls">
          ${slab(-70, -62, w + 70, 124, 62, { face: "url(#quPillD)", body: "#6e5208", stroke: "#ffd23a", bodyStroke: "#140e0a", sw: 6, d: 12 })}
          ${icon(it.icon, -64, -60, 0.94, `${id}-ic`)}<text x="62" y="29" font-family="Kanit" font-weight="900" font-size="72" fill="#000" opacity=".55">${it.text}</text><text x="62" y="24" font-family="Kanit" font-weight="900" font-size="72" fill="#ffd23a">${it.text}</text></g></g></g></g>`);
      tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.1, immediateRender: false }, at);
      tl.fromTo(`.${id}-ln`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.25, ease: "power2.out", immediateRender: false }, at);
      tl.fromTo(`#${id}-pl`, { opacity: 0 }, { opacity: 1, duration: 0.08, immediateRender: false }, at + 0.15);
      tl.fromTo(`#${id}-pls`, { scaleX: 0.35, scaleY: 1.45, svgOrigin: `${cx} 0` }, { scaleX: 1, scaleY: 1, svgOrigin: `${cx} 0`, duration: 0.75, ease: "elastic.out(1, 0.45)", immediateRender: false }, at + 0.15);
      tl.fromTo(`#${id}-pu`, { attr: { r: 16 }, opacity: 1 }, { attr: { r: 60 }, opacity: 0, duration: 0.8, repeat: 4, ease: "power2.out", immediateRender: false }, at);
      iconPop(tl, document.getElementById(`${id}-ic`), at + 0.15);
      iconLife(tl, document.getElementById(`${id}-ic`), at + 0.9, it.dur ?? 3);
      if (it.end !== undefined) { tl.to(`#${id}-pls`, { scale: 0.6, svgOrigin: `${cx} 0`, duration: 0.2, ease: "power2.in" }, t0 + it.end); tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + it.end); }
    });
  }

  // ---------------- the seismogram ----------------
  function seismo(tl, layer, t0, dur, o = {}) {
    const id = nid(), X0 = 110, X1 = 970, Y = o.y ?? 860, draw = o.draw ?? 2.6;
    const amp = (k) => (k < 0.08 ? 4 : k < 0.42 ? 230 * Math.sin(Math.PI * (k - 0.08) / 0.34) : 0) + [[0.58, 0.05, 80], [0.72, 0.04, 60], [0.86, 0.035, 46]].reduce((s, [c, w, a]) => s + (Math.abs(k - c) < w ? a * Math.sin(Math.PI * (k - c + w) / (2 * w)) : 0), 0);
    let d = `M${X0},0`;
    for (let x = X0; x <= X1; x += 4) { const k = (x - X0) / (X1 - X0), a = amp(k); d += `L${x},${f1(Math.sin(x * 0.42) * a * (0.6 + 0.4 * Math.sin(x * 0.09)) + Math.sin(x * 1.3) * 3)}`; }
    const pill = (x, y, t, c, k) => `<g transform="translate(${x},${y})"><g id="${id}-p${k}" opacity="0">${slab(-(28 + t.length * 15), -30, 56 + t.length * 30, 60, 30, { face: c, body: tone(c, -0.55), stroke: "#140e0a", sw: 4, d: 7 })}<text y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#fff">${t}</text></g></g>`;
    const screw = (x, y) => `<circle cx="${x}" cy="${y}" r="9" fill="url(#quBezel)" stroke="#140e0a" stroke-width="2"/><path d="M${x - 5},${y - 5}L${x + 5},${y + 5}" stroke="#2a3034" stroke-width="2"/>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m">
      <ellipse cx="540" cy="${Y + 450}" rx="460" ry="40" fill="url(#quSoftSh)" opacity=".6"/>
      <rect x="60" y="${Y - 420 + 14}" width="960" height="840" rx="44" fill="#020404" stroke="#140e0a" stroke-width="4"/>
      <rect x="60" y="${Y - 420}" width="960" height="840" rx="44" fill="url(#quBezelD)" stroke="#140e0a" stroke-width="4"/>
      <rect x="66" y="${Y - 414}" width="948" height="828" rx="40" fill="none" stroke="#fff" stroke-width="2" opacity=".14"/>
      <rect x="86" y="${Y - 394}" width="908" height="788" rx="26" fill="url(#quScreen)" stroke="#05080a" stroke-width="4"/>
      ${screw(84, Y - 398)}${screw(996, Y - 398)}${screw(84, Y + 398)}${screw(996, Y + 398)}
      <circle id="${id}-led" cx="940" cy="${Y - 404}" r="6" fill="#ff4a3a"/>
      <text x="110" y="${Y - 336}" font-family="Kanit" font-weight="800" font-size="44" fill="#000" opacity=".5" transform="translate(0,3)">คลื่นแผ่นดินไหว</text>
      <text x="110" y="${Y - 336}" font-family="Kanit" font-weight="800" font-size="44" fill="#f4ecd8">คลื่นแผ่นดินไหว</text>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${X0},${Y - 260 + k * 65}H${X1}" stroke="#7ad8b0" stroke-width="1.5" opacity=".1"/>`).join("")}
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${X0 + k * 78},${Y - 290}V${Y + 300}" stroke="#7ad8b0" stroke-width="1.5" opacity=".07"/>`).join("")}
      <defs><clipPath id="${id}-cl"><rect id="${id}-cr" x="${X0 - 10}" y="${Y - 300}" width="0" height="600"/></clipPath></defs>
      <g clip-path="url(#${id}-cl)"><g transform="translate(0,${Y})"><path d="${d}" stroke="#ff3a2a" stroke-width="16" fill="none" stroke-linejoin="round" opacity=".22"/><path d="${d}" stroke="#ff5a46" stroke-width="5" fill="none" stroke-linejoin="round"/>
        <path d="${d}" stroke="#ffd8d0" stroke-width="1.6" fill="none" stroke-linejoin="round" opacity=".8"/></g></g>
      <g id="${id}-pen"><circle cx="0" cy="0" r="30" fill="url(#quBurst)" opacity=".7"/><circle cx="0" cy="0" r="12" fill="#fff" stroke="#ff5a46" stroke-width="5"/></g>
      <text x="${X1}" y="${Y + 360}" text-anchor="end" font-family="Kanit" font-weight="600" font-size="30" fill="#f4ecd8" opacity=".7">เวลา →</text>
      ${pill(X0 + (X1 - X0) * 0.25, Y + 262, "แผ่นดินไหวหลัก", "#d8312a", 0)}${pill(X0 + (X1 - X0) * 0.72, Y + 167, "อาฟเตอร์ช็อก", "#e8822a", 1)}
      <g transform="translate(${X1 - 110},${Y - 330})"><g id="${id}-dk" opacity="0">${icon("table", -64, -64, 1.07, `${id}-tb`)}</g></g>
      <g transform="translate(${X1 - 110},${Y - 170})"><g id="${id}-dl" opacity="0">${slab(-100, -30, 200, 60, 30, { face: "#1e9a50", body: "#0a4a24", stroke: "#140e0a", sw: 4, d: 7 })}<text y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#fff">หลบซ้ำ</text></g></g>
      <path d="M86,${Y - 394}H560L300,${Y + 394}H86Z" fill="url(#quGlare)" opacity=".7"/></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.fromTo(`#${id}-m`, { y: 60 }, { y: 0, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-led`, { opacity: 1 }, { opacity: 0.2, duration: 0.3, repeat: Math.ceil(dur / 0.3), yoyo: true, immediateRender: false }, t0);
    tl.fromTo(`#${id}-cr`, { attr: { width: 0 } }, { attr: { width: X1 - X0 + 20 }, duration: draw, ease: "none", immediateRender: false }, t0 + 0.25);
    const pen = document.getElementById(`${id}-pen`), c = { k: 0 };
    const placePen = () => { const x = X0 + (X1 - X0) * c.k, a = amp(c.k); pen.setAttribute("transform", `translate(${f1(x)},${f1(Y + Math.sin(x * 0.42) * a * (0.6 + 0.4 * Math.sin(x * 0.09)))})`); };
    placePen();
    tl.fromTo(c, { k: 0 }, { k: 1, duration: draw, ease: "none", immediateRender: false, onUpdate: placePen }, t0 + 0.25);
    [[0, 0.2], [1, 0.62]].forEach(([k, f]) => tl.fromTo(`#${id}-p${k}`, { scaleX: 0.3, scaleY: 1.5, opacity: 0, svgOrigin: "0 30" }, { scaleX: 1, scaleY: 1, opacity: 1, svgOrigin: "0 30", duration: 0.7, ease: "elastic.out(1, 0.45)", immediateRender: false }, t0 + 0.25 + draw * f));
    tl.fromTo([`#${id}-dk`, `#${id}-dl`], { scale: 0, opacity: 1, svgOrigin: "0 0" }, { scale: 1, opacity: 1, svgOrigin: "0 0", duration: 0.5, stagger: 0.12, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.25 + draw * 0.75);
    iconPop(tl, document.getElementById(`${id}-tb`), t0 + 0.25 + draw * 0.75);
    iconLife(tl, document.getElementById(`${id}-tb`), t0 + 0.9 + draw * 0.75, dur);
    if (o.out !== undefined) { tl.fromTo(`#${id}-m`, { y: 0 }, { y: 40, duration: 0.2, ease: "power2.in", immediateRender: false }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + o.out); }
  }

  // ---------------- the real quake on the map (draws into the map's set layer) ----------------
  function quakeMap(tl, L, sid, t0, o = {}) {
    const mp = o.map || "mq", X = o.x ?? 90, Y = o.y ?? 300, S = o.s ?? 1, W = (lon, lat) => { const [px, py] = Maps.P(lon, lat); return [X + px * S, Y + py * S]; };
    const [ex, ey] = W(95.9, 22.0), [bx, by] = W(100.5, 13.75), id = `${sid}-qm`;
    ["pin0", "pin1", "sh0", "sh1", "lab0", "lab1", "car", "rip"].forEach((p) => { if (document.getElementById(`${mp}-${p}`)) tl.set(`#${mp}-${p}`, { opacity: 0 }, t0); });
    if (document.getElementById(`${mp}-reveal`)) tl.set(`#${mp}-reveal`, { attr: { "stroke-dashoffset": 1 } }, t0);
    put(L.glow, `<g id="${id}">${[0, 1, 2, 3].map((k) => `<circle id="${id}-r${k}" cx="${f1(ex)}" cy="${f1(ey)}" r="10" fill="none" stroke="#e8382a" stroke-width="7" opacity="0"/>`).join("")}
      <g id="${id}-ep"><circle cx="${f1(ex)}" cy="${f1(ey)}" r="90" fill="url(#quBurst)"/><path d="M${f1(ex)},${f1(ey - 34)}l10,22l24,-6l-14,20l18,16l-24,2l-2,24l-12,-20l-12,20l-2,-24l-24,-2l18,-16l-14,-20l24,6z" fill="#ffd23a" stroke="#140e0a" stroke-width="4"/></g>
      <g transform="translate(${f1(ex + 40)},${f1(ey + 90)})"><g id="${id}-el"><rect x="-10" y="-40" width="330" height="80" rx="40" fill="#140e0a"/><text x="155" y="14" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="38" fill="#ffd23a">เมียนมา · ขนาด 8.2</text></g></g>
      <g transform="translate(${f1(bx)},${f1(by)})"><g id="${id}-bk"><path d="M0,0C-30,-34 -36,-56 -36,-70A36,36 0 0 1 36,-70C36,-56 30,-34 0,0Z" fill="#d8312a" stroke="#140e0a" stroke-width="4"/><circle cy="-70" r="14" fill="#fff"/></g></g>
      <g transform="translate(${f1(bx + 50)},${f1(by - 40)})"><g id="${id}-bl"><rect x="0" y="-40" width="230" height="80" rx="40" fill="#fffaf0" stroke="#140e0a" stroke-width="4"/><text x="115" y="14" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#140e0a">กรุงเทพฯ</text></g></g>
      <g transform="translate(${f1(bx - 150)},${f1(by + 210)})"><g id="${id}-tw" opacity="0"><g id="${id}-tws"><rect x="-30" y="-180" width="60" height="180" fill="#5f8fb0" stroke="#140e0a" stroke-width="4"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-22,${-160 + k * 28}H22" stroke="#cfe6f2" stroke-width="5"/>`).join("")}</g>
        <rect x="40" y="-120" width="360" height="110" rx="24" fill="#140e0a" stroke="#ffd23a" stroke-width="5"/><text x="220" y="-78" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#f4ecd8">ตึกสูงโยกนานกว่า</text>
        <text id="${id}-cnt" x="220" y="-26" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#ffd23a">0 วินาที</text></g></g></g>`);
    put(L.light, `<g id="${id}-chip" opacity="0" transform="translate(540,200)"><rect x="-420" y="-56" width="840" height="112" rx="56" fill="#140e0a" stroke="#ffd23a" stroke-width="5"/>
      <text y="16" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="#fff">28 มี.ค. 2568 · 13:20 น.</text></g>`);
    tl.fromTo(`#${id}-ep`, { scale: 0, svgOrigin: `${f1(ex)} ${f1(ey)}` }, { scale: 1, svgOrigin: `${f1(ex)} ${f1(ey)}`, duration: 0.5, ease: "back.out(3)", immediateRender: false }, t0 + 0.1);
    tl.fromTo(`#${id}-ep`, { rotation: -8, svgOrigin: `${f1(ex)} ${f1(ey)}` }, { rotation: 8, svgOrigin: `${f1(ex)} ${f1(ey)}`, duration: 0.12, repeat: 60, yoyo: true, immediateRender: false }, t0 + 0.6);
    const reach = Math.hypot(bx - ex, by - ey) + 160;
    [0, 1, 2, 3].forEach((k) => tl.fromTo(`#${id}-r${k}`, { attr: { r: 10 }, opacity: 0.9 }, { attr: { r: reach }, opacity: 0, duration: 2.2, repeat: 3, ease: "power1.out", immediateRender: false }, t0 + 0.3 + k * 0.55));
    tl.fromTo(`#${id}-el`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, t0 + (o.labelAt ?? 1.4));
    tl.fromTo(`#${id}-chip`, { opacity: 0, y: 160 }, { opacity: 1, y: 200, duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + (o.chipAt ?? 0.3));
    tl.fromTo(`#${id}-bk`, { y: -160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "bounce.out", immediateRender: false }, t0 + (o.bkkAt ?? 2.8));
    tl.fromTo(`#${id}-bl`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.4, ease: "back.out(2.6)", immediateRender: false }, t0 + (o.bkkAt ?? 2.8) + 0.4);
    const [c0, c1] = o.count || [5.9, 8.2], cnt = document.getElementById(`${id}-cnt`), cc = { v: 0 };
    tl.to(`#${id}-el`, { opacity: 0, duration: 0.3 }, t0 + c0 - 0.6);
    tl.fromTo(`#${id}-tw`, { opacity: 0, scale: 0.6, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0", duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + c0);
    tl.fromTo(`#${id}-tws`, { rotation: -4, svgOrigin: "0 0" }, { rotation: 4, svgOrigin: "0 0", duration: 0.6, repeat: Math.ceil((c1 - c0) / 0.6) + 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + c0);
    tl.fromTo(cc, { v: 0 }, { v: 20, duration: c1 - c0 - 0.3, ease: "power1.in", immediateRender: false, onUpdate: () => { cnt.textContent = `${Math.round(cc.v)}${cc.v >= 19.5 ? "+" : ""} วินาที`; } }, t0 + c0 + 0.2);
    if (o.out !== undefined) tl.to(`#${id}-chip`, { opacity: 0, duration: 0.2 }, t0 + o.out);
  }

  // ---------------- calling แม่ ----------------
  function call(tl, layer, t0, dur, o = {}) {
    const id = nid(), X = o.x ?? 640, Y = o.y ?? 1240;
    put(layer, `<g transform="translate(${X},${Y})"><g id="${id}" opacity="0"><g transform="rotate(${o.rot ?? 6})">
      <ellipse cx="30" cy="420" rx="230" ry="34" fill="url(#quSoftSh)" opacity=".6"/>
      <rect x="-186" y="-364" width="400" height="760" rx="48" fill="#06080a" ${OUT(5)}/>
      <rect x="-200" y="-380" width="400" height="760" rx="48" fill="url(#quPhoneB)" ${OUT(5)}/>
      <rect x="203" y="-250" width="7" height="90" rx="3" fill="#3a4048" ${OUT(2)}/>
      <rect x="-184" y="-364" width="368" height="728" rx="36" fill="url(#quCallScr)"/>
      <rect x="-48" y="-350" width="96" height="26" rx="13" fill="#05070a"/>
      ${[0, 1, 2].map((k) => `<circle id="${id}-w${k}" cy="-180" r="80" fill="none" stroke="#fff" stroke-width="4" opacity="0"/>`).join("")}
      <circle cy="-172" r="80" fill="#8a3a5a" opacity=".6"/><circle cy="-180" r="80" fill="#f8d0e0" ${OUT(4)}/><circle cy="-180" r="68" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>
      <g transform="translate(0,-176)"><path d="M0,26C-40,0 -44,-30 -24,-40C-12,-46 -2,-40 0,-30C2,-40 12,-46 24,-40C44,-30 40,0 0,26Z" fill="#7a0e10" transform="translate(2,5)"/>
        <path d="M0,26C-40,0 -44,-30 -24,-40C-12,-46 -2,-40 0,-30C2,-40 12,-46 24,-40C44,-30 40,0 0,26Z" fill="url(#quHeart)" stroke="#5a0a0c" stroke-width="3"/><ellipse cx="-18" cy="-28" rx="8" ry="5" fill="#fff" opacity=".7" transform="rotate(-30 -18 -28)"/></g>
      <text y="-37" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="60" fill="#000" opacity=".35">แม่</text><text y="-40" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="60" fill="#fff">แม่</text>
      <text id="${id}-s" y="20" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="36" fill="#cfd8e8">กำลังโทร…</text>
      <text id="${id}-f" y="20" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#ff8a7a" opacity="0">ไม่มีผู้รับสาย</text>
      <circle cy="258" r="56" fill="#7a140e"/><circle cy="250" r="56" fill="url(#quRedC)" stroke="#5a0a08" stroke-width="3"/><path d="M-30,236A36,36 0 0 1 -6,218" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>
      <path d="M-26,250h52" stroke="#fff" stroke-width="12" stroke-linecap="round"/>
      <path d="M-184,-364L60,-364L-184,40Z" fill="url(#quGlare)"/>
      <path d="M-200,120Q-262,140 -252,262Q-242,382 -120,402" fill="url(#quSkinL)" ${OUT(4)}/><path d="M-230,170Q-246,250 -226,330" stroke="#fff" stroke-width="4" opacity=".4" fill="none" stroke-linecap="round"/></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)", immediateRender: false }, t0);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-w${k}`, { attr: { r: 80 }, opacity: 0.8 }, { attr: { r: 170 }, opacity: 0, duration: 1, repeat: 3, ease: "power1.out", immediateRender: false }, t0 + 0.3 + k * 0.33));
    const f = t0 + (o.failAt ?? dur - 1);
    tl.to(`#${id}-s`, { opacity: 0, duration: 0.1 }, f);
    tl.fromTo(`#${id}-f`, { opacity: 0, scale: 1.5, svgOrigin: "0 10" }, { opacity: 1, scale: 1, svgOrigin: "0 10", duration: 0.3, ease: "back.out(3)", immediateRender: false }, f);
    [0, 1, 2].forEach((k) => tl.set(`#${id}-w${k}`, { opacity: 0 }, f));
  }

  // ---------------- the end card: the orange whistle and its tag ----------------
  function endCard(tl, layer, t0, dur, o = {}) {
    const id = nid();
    const body = "M-110,-60H70Q150,-60 150,30Q150,120 50,120Q-30,120 -40,50H-110Z";
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#120e0c"/><rect width="1080" height="1920" fill="url(#${id}v)"/>
      <defs><radialGradient id="${id}v" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#3a2a22"/><stop offset="1" stop-color="#0a0706"/></radialGradient>
        <linearGradient id="${id}cord" gradientUnits="userSpaceOnUse" x1="534" y1="0" x2="546" y2="0"><stop offset="0" stop-color="#d8601e"/><stop offset=".35" stop-color="#ff9a52"/><stop offset="1" stop-color="#b8501a"/></linearGradient>
        <radialGradient id="${id}sp" cx=".5" cy=".4" r=".5"><stop offset="0" stop-color="#ffb070" stop-opacity=".22"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></radialGradient></defs>
      <ellipse cx="540" cy="760" rx="520" ry="560" fill="url(#${id}sp)"/>
      <g transform="translate(540,0) scale(1.3) translate(-540,0)"><g id="${id}-sw">
        <path d="M540,-20V550" stroke="#140e0a" stroke-width="17"/><path d="M540,-20V550" stroke="url(#${id}cord)" stroke-width="12"/>
        <path d="${Array.from({ length: 42 }, (_, k) => `M534.5,${-20 + k * 14}L545.5,${-12 + k * 14}`).join("")}" stroke="#a8420e" stroke-width="3" opacity=".75"/>
        <path d="${Array.from({ length: 42 }, (_, k) => `M535,${-15 + k * 14}L541,${-11 + k * 14}`).join("")}" stroke="#ffd2b0" stroke-width="2" opacity=".7"/>
        <circle cx="540" cy="560" r="15" fill="none" stroke="#2a2420" stroke-width="9"/><circle cx="540" cy="560" r="15" fill="none" stroke="url(#quRing)" stroke-width="5"/>
        <g transform="translate(540,640) rotate(-8)"><g id="${id}-wt">
          <path d="${body}" fill="#8a3a0c" transform="translate(8,12)" stroke="#140e0a" stroke-width="8" stroke-linejoin="round"/>
          <path d="${body}" fill="url(#quOr)" stroke="#140e0a" stroke-width="8" stroke-linejoin="round"/>
          <rect x="-196" y="-60" width="96" height="72" rx="14" fill="#a8480e" transform="translate(6,10)"/><rect x="-196" y="-60" width="96" height="72" rx="14" fill="url(#quOrM)" stroke="#140e0a" stroke-width="7"/>
          <ellipse cx="-196" cy="-24" rx="9" ry="24" fill="#5a2406" stroke="#140e0a" stroke-width="4"/>
          <circle cx="50" cy="30" r="36" fill="url(#quHole)" stroke="#140e0a" stroke-width="6"/><path d="M26,14A30,30 0 0 1 60,2" stroke="#ffd2a8" stroke-width="4" fill="none" opacity=".5"/>
          <path d="M-96,-42H66Q120,-40 132,-6" stroke="#ffe8d0" stroke-width="12" fill="none" opacity=".75" stroke-linecap="round"/>
          <path d="M-90,98Q-20,108 60,104" stroke="#000" stroke-width="10" fill="none" opacity=".12" stroke-linecap="round"/>
          <circle cx="-172" cy="-66" r="20" fill="none" stroke="#3a3e42" stroke-width="10"/><circle cx="-172" cy="-66" r="20" fill="none" stroke="url(#quRing)" stroke-width="6"/></g></g>
        <g transform="translate(540,900) rotate(4)"><g id="${id}-tg">
          <path d="M0,-170V-60" stroke="#c8b08a" stroke-width="5"/><path d="M5,-166V-58" stroke="#000" stroke-width="4" opacity=".25"/>
          <g filter="url(#quDrop)"><path d="M-230,-60H230V210H-230Z" fill="url(#quTag)" stroke="#8a7a5a" stroke-width="4"/><path d="M-230,-60H230V210H-230Z" fill="url(#quPaper)"/>
            <path d="M-230,-60H230V-40H-230Z" fill="#fff" opacity=".25"/><path d="M200,210L230,180V210Z" fill="#c8b48a"/>
            <circle cy="-30" r="20" fill="#d8ccb0" stroke="#a8987a" stroke-width="3"/><circle cy="-30" r="12" fill="#120e0c"/>
            <text y="60" text-anchor="middle" font-family="Mali" font-weight="700" font-size="54" fill="#8a6a3a">${o.l1 || "ตอนที่ 2"}</text>
            <text y="153" text-anchor="middle" font-family="Mali" font-weight="700" font-size="76" fill="#5a0c08" opacity=".3">${o.l2 || "ลงบันได"}</text>
            <text y="150" text-anchor="middle" font-family="Mali" font-weight="700" font-size="76" fill="#c8281e">${o.l2 || "ลงบันได"}</text></g></g></g></g></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 7, svgOrigin: "540 -20" }, { rotation: -4, svgOrigin: "540 -20", duration: 1.1, ease: "elastic.out(1, 0.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: -4, svgOrigin: "540 -20" }, { rotation: 2, svgOrigin: "540 -20", duration: 1.4, repeat: 3, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.1);
    // the whistle turns a little on its cord (a 3D twist), the tag lags behind the swing
    tl.fromTo(`#${id}-wt`, { scaleX: 1, svgOrigin: "0 -60" }, { scaleX: 0.9, svgOrigin: "0 -60", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.2);
    tl.fromTo(`#${id}-tg`, { rotation: -6, svgOrigin: "0 -170" }, { rotation: 5, svgOrigin: "0 -170", duration: 1.2, repeat: Math.ceil(dur / 1.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.25);
  }

  window.QkUI = { title, app, eta, choice, rewind, note, labels, seismo, quakeMap, call, endCard, ICON, icon, iconLife, iconPop, RULES, mmss };
})();
