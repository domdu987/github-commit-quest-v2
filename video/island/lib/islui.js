// "ติดเกาะ" on-screen graphics (screen space: put them in L.light unless noted). The castaway world's own materials: an old carved
// paddle, young coconuts split in half, woven palm leaf, rope, a glass bottle with a note, a campfire. Same 2.5D rules as ตึกโยก /
// ทะเลลด (V8/V10): a darker body under a lit face, one shade + one highlight, soft shadows under what floats; entries squash &
// stretch with back/elastic overshoot, staggered, then a secondary motion keeps running until the shot ends; exits lift and fade.
// Nothing here looks like ทะเลลด's driftwood boards or fishing floats.
//   IslUI.rule(tl, layer, t0, dur, o)      ตาเวียง's old paddle hung on two ropes, the blade carved with the 3 rhyming rules.
//                                          o.active (0..2) is lit by a torch sweep: the carving fills with gold (write-on), the rhyme
//                                          syllables bounce, a coconut-shell coin pops beside the line (seawater / jelly / boat);
//                                          o.done [i…] get a green paint stroke and a tick, the rest stay faint carvings under moss
//                                          · o.y (blade top, default 300) · o.at [s…] when each row lands · o.glow true = a gold halo
//                                          behind the paddle (the rewind) · o.out (s after t0) to lift away
//   IslUI.hud(tl, layer, t0, dur, o)       the survival HUD, top-left under y 130 (x 40–370, y 130–360): a coconut-shell bottle
//                                          "น้ำในตัว" 0–100% whose level follows o.water [[t, pct]…] (seconds after t0; falling =
//                                          the water reddens and sweat drops run, rising = bubbles), a wooden day tag o.day (a number → "วันที่ n", or text), and
//                                          o.forks [done, total] coconut halves (filled = a fork already taken) · o.out
//   IslUI.fork(tl, layer, t0, dur, o)      the fork card of the "คุณคือคนติดเกาะ" format: o.q on a floating plank, A / B on two
//                                          coconut halves (o.a / o.b { text }), a campfire that burns down over o.secs with a count.
//                                          o.pick "a"|"b" at o.pickAt: the stamp "คนส่วนใหญ่เลือก" slams onto that half, it grows,
//                                          the other fades · o.vote true: no answer — when the fire is out the frame flicks between
//                                          the halves and the sign "คอมเมนต์เลือก A หรือ B" pops · o.out
//   IslUI.choice(...)                      = fork with vote: true
//   IslUI.dark(tl, layer, t0, dur, o)      the screen drains to blue-black from the edges, a pulse line beats slower and stops, the red
//                                          line o.text ("ทางนี้… คุณไม่ถึงเช้า") rises at o.textAt (a fraction of dur, default 0.5; > 1 = seconds)
//   IslUI.rewind(tl, layer, t0, dur, o)    ◀◀ the rewind: scan lines, a scrub bar running backward, sea rings running inward, then the
//                                          overlay lifts at o.ruleAt (1.0) and IslUI.rule glows up for rule o.rule (default 0); o.ruleOpts
//   IslUI.chip(tl, layer, t0, dur, o)      a small plank on a rope loop: o.text ("เช้าวันนั้น", "วันที่ 1 · บ่ายสอง"), o.x o.y (540, 190)
//   IslUI.source(tl, layer, t0, dur, o)    the source chip: a sand-coloured pill with a coconut badge, o.text, o.y (1790)
//   IslUI.symptom(tl, layer, t0, dur, o)   woven palm-leaf slats, one per o.items[] (ตัวร้อน วิงเวียน …), o.x o.y (640, 330), o.gap
//   IslUI.endCard(tl, layer, t0, dur, o)   a glass bottle washed up on wet sand at dusk, the note inside: o.l1 "ตอนที่ 2" o.l2 "พิษไหม้"
//                                          · o.final → "ติดเกาะ / ตอนจบ"
//   IslUI.ICON.<name>() / IslUI.icon(name, x, y, s, id) / iconPop / iconLife   the rule coins (120-unit box): seawater (a cup of
//                                          seawater under a red ban ring), jelly (a box jellyfish and a bottle of vinegar), boat (a far
//                                          boat, a figure waving from the sand, a swimmer banned) · IslUI.RULES the rule lines
//   Sets.islLegend(L, o) + IslUI.legendAnim(tl, id, t0, dur, o)
//                                          the legend "ไฟเกาะผี" on the channel's shadow screen; the puppets are woven coconut-leaf
//                                          cut-outs: an islet with a palm (#id-isle), three fires (#id-f0..2), the sea (#id-sea), a
//                                          longtail with a lamp passing far out (#id-boat), a swimmer leaving the islet (#id-swim) who
//                                          sinks (bubbles #id-bub0..2), the moon · legendAnim o: fires [a, b] (lit one by one), boat
//                                          [a, b] (crosses right → left), swim [a, b], sink (t) — seconds after t0
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;
  const nid = () => `iu${++seq}`;
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mkR = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const plain = (s) => String(s).replace(/<[^>]+>/g, "");
  const cells = (t) => [...plain(t)].filter((c) => !/[ัิ-ฺ็-๎]/.test(c)).length;
  const tone = (h, k) => { h = h.replace("#", ""); const c = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)), t = k >= 0 ? 255 : 0, a = Math.abs(k); return "#" + c.map((v) => Math.round(v + (t - v) * a).toString(16).padStart(2, "0")).join(""); };
  const FT = (tl, sel, from, to, dur, ease, t, extra = {}) => tl.fromTo(sel, from, { ...to, duration: dur, ease, immediateRender: false, ...extra }, t);

  // coin palettes: face, face highlight, rim, rim shade
  const PAL = {
    seawater: ["#cdeefb", "#f4fcff", "#2f8fc0", "#1c5a80"],
    jelly: ["#e6e2fb", "#fbf9ff", "#7a5ac8", "#4a3488"],
    boat: ["#ffe8c0", "#fff8ea", "#e89a3a", "#a8601a"],
  };
  let coinDefs = "";
  for (const [n, [b, l, r, rd]] of Object.entries(PAL)) coinDefs += `<radialGradient id="iuF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${l}"/><stop offset=".5" stop-color="${b}"/><stop offset="1" stop-color="${tone(b, -0.2)}"/></radialGradient>
    <linearGradient id="iuR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset=".55" stop-color="${tone(r, -0.12)}"/><stop offset="1" stop-color="${rd}"/></linearGradient>`;

  Sets.DEFS += `${coinDefs}
    <radialGradient id="iuCoinSh"><stop offset="0" stop-color="#000" stop-opacity=".42"/><stop offset=".6" stop-color="#000" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="iuSoftSh"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset=".55" stop-color="#000" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <linearGradient id="iuBev" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/><stop offset=".58" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
    <clipPath id="iuPicClip" clipPathUnits="userSpaceOnUse"><circle cx="60" cy="60" r="51"/></clipPath>
    <linearGradient id="iuSeaBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf8ff"/><stop offset=".55" stop-color="#bfe8f8"/><stop offset="1" stop-color="#4ab0d0"/></linearGradient>
    <linearGradient id="iuSalt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fdcf4"/><stop offset="1" stop-color="#2f8fc0"/></linearGradient>
    <linearGradient id="iuDeep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a7ad8"/><stop offset=".6" stop-color="#1e4ea0"/><stop offset="1" stop-color="#142e6a"/></linearGradient>
    <linearGradient id="iuSandG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8e2a8"/><stop offset="1" stop-color="#e2bc78"/></linearGradient>
    <linearGradient id="iuPaddle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0c494"/><stop offset=".5" stop-color="#c8a870"/><stop offset="1" stop-color="#a0825a"/></linearGradient>
    <linearGradient id="iuPaddleSide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5e3e"/><stop offset="1" stop-color="#4a3622"/></linearGradient>
    <linearGradient id="iuRope" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a7a4a"/><stop offset=".4" stop-color="#d8bc84"/><stop offset="1" stop-color="#8a6a3a"/></linearGradient>
    <linearGradient id="iuHusk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bfe070"/><stop offset=".45" stop-color="#86b84c"/><stop offset="1" stop-color="#4e7e2a"/></linearGradient>
    <linearGradient id="iuHuskB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a08050"/><stop offset=".5" stop-color="#6a4a28"/><stop offset="1" stop-color="#3e2a14"/></linearGradient>
    <radialGradient id="iuMeat" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#fffdf6"/><stop offset=".7" stop-color="#f6ecd8"/><stop offset="1" stop-color="#e0d0b0"/></radialGradient>
    <radialGradient id="iuPool" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#e6f8ff"/><stop offset="1" stop-color="#9ad4ea"/></radialGradient>
    <radialGradient id="iuGold"><stop offset="0" stop-color="#ffe9a0" stop-opacity=".95"/><stop offset=".45" stop-color="#ffcf4a" stop-opacity=".45"/><stop offset="1" stop-color="#ffcf4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="iuDarkEdge" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#050a14" stop-opacity="0"/><stop offset=".45" stop-color="#050a14" stop-opacity=".2"/><stop offset=".72" stop-color="#050a14" stop-opacity=".82"/><stop offset="1" stop-color="#050a14"/></radialGradient>
    <linearGradient id="iuGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".3" stop-color="#fff" stop-opacity=".06"/><stop offset=".58" stop-color="#fff" stop-opacity="0"/><stop offset=".72" stop-color="#fff" stop-opacity=".2"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="iuHudW" gradientUnits="userSpaceOnUse" x1="0" y1="10" x2="0" y2="172"><stop offset="0" stop-color="#8fdcf8"/><stop offset="1" stop-color="#1e86c8"/></linearGradient>
    <linearGradient id="iuHudR" gradientUnits="userSpaceOnUse" x1="0" y1="10" x2="0" y2="172"><stop offset="0" stop-color="#ff9a70"/><stop offset="1" stop-color="#c8301e"/></linearGradient>
    <linearGradient id="iuTag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecd8b0"/><stop offset=".5" stop-color="#d8bc8a"/><stop offset="1" stop-color="#b89a68"/></linearGradient>
    <linearGradient id="iuTagSide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5e3e"/><stop offset="1" stop-color="#4a3622"/></linearGradient>
    <radialGradient id="iuFire" cx=".5" cy=".85" r=".8"><stop offset="0" stop-color="#fff6b0"/><stop offset=".35" stop-color="#ffb23a"/><stop offset=".75" stop-color="#ff6a1a"/><stop offset="1" stop-color="#c8300a" stop-opacity=".9"/></radialGradient>
    <radialGradient id="iuFireGlow"><stop offset="0" stop-color="#ffb04a" stop-opacity=".55"/><stop offset="1" stop-color="#ffb04a" stop-opacity="0"/></radialGradient>
    <linearGradient id="iuDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1434"/><stop offset=".36" stop-color="#5a3a6e"/><stop offset=".6" stop-color="#d8705a"/><stop offset=".7" stop-color="#ffb46a"/><stop offset="1" stop-color="#ffd890"/></linearGradient>
    <linearGradient id="iuDuskSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a4a62"/><stop offset=".35" stop-color="#2e3a5e"/><stop offset="1" stop-color="#0e1a2e"/></linearGradient>
    <linearGradient id="iuWetSand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a6a58"/><stop offset=".3" stop-color="#9a8a70"/><stop offset="1" stop-color="#c8b088"/></linearGradient>
    <linearGradient id="iuNote" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbef"/><stop offset="1" stop-color="#ecdcb8"/></linearGradient>
    <linearGradient id="iuCork" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b08a5a"/><stop offset=".5" stop-color="#d8b07a"/><stop offset="1" stop-color="#8a6a40"/></linearGradient>
    <linearGradient id="iuSandPill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf6e4"/><stop offset="1" stop-color="#ecdcb8"/></linearGradient>
    <pattern id="iuLeafWeave" width="28" height="28" patternUnits="userSpaceOnUse"><rect width="28" height="28" fill="#9ab848"/><path d="M0,14L14,0H28L0,28ZM28,14L14,28" stroke="#c8dc70" stroke-width="7" fill="none"/><path d="M0,0L28,28" stroke="#5e8a2a" stroke-width="2.4" opacity=".8"/><path d="M14,0V28M0,14H28" stroke="#4e7a22" stroke-width="1.4" opacity=".5"/></pattern>
    <pattern id="iuLeafWeaveD" width="28" height="28" patternUnits="userSpaceOnUse"><rect width="28" height="28" fill="#c8a850"/><path d="M0,14L14,0H28L0,28ZM28,14L14,28" stroke="#e8cc78" stroke-width="7" fill="none"/><path d="M0,0L28,28" stroke="#8a6a28" stroke-width="2.4" opacity=".8"/></pattern>
    <pattern id="iuScan" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="3" fill="#000" opacity=".3"/></pattern>
    <pattern id="iuWeave" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M9,2L16,9L9,16L2,9Z" fill="#fff4d0" opacity=".5"/></pattern>`;

  // ---------------- the rule coins (120-unit box) ----------------
  const PICT = {
    // กระหายแค่ไหน อย่าหมายน้ำเค็ม: a clear cup of seawater on the shore, salt crystals in it, a red ban ring over it
    seawater: () => [`<rect x="-10" y="-10" width="140" height="140" fill="url(#iuSeaBg)"/>
      <g class="iuRip"><path d="M-30,84q15,-10 30,0t30,0t30,0t30,0t30,0t30,0V140H-30Z" fill="#3aa8c8" opacity=".85"/><path d="M-30,84q15,-10 30,0t30,0t30,0t30,0t30,0t30,0" stroke="#effcff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
      <path d="M-10,110Q60,100 130,112V140H-10Z" fill="url(#iuSandG)" ${OUT(2.6)}/>
      <g transform="translate(60,66)"><path d="M-30,-44H30L24,44Q0,50 -24,44Z" fill="#dff4ff" opacity=".45" ${OUT(3)}/>
        <path d="M-27,-12H27L24,44Q0,50 -24,44Z" fill="url(#iuSalt)" opacity=".92"/><path d="M-27,-12H27" stroke="#fff" stroke-width="3" opacity=".85"/>
        ${[[-14, 6], [6, 18], [16, 2], [-6, 30], [12, 34], [-18, 24]].map(([x, y]) => `<path d="M${x - 4},${y}l4,-4l4,4l-4,4z" fill="#fff" opacity=".9"/>`).join("")}
        <path d="M-22,-36l-3,70" stroke="#fff" stroke-width="3" opacity=".55" stroke-linecap="round"/><path d="M-30,-44H30" stroke="#fff" stroke-width="3" opacity=".7"/></g>`,
    `<g class="iuBan"><circle cx="60" cy="60" r="46" fill="none" stroke="#e02a1e" stroke-width="9"/><path d="M27,27L93,93" stroke="#e02a1e" stroke-width="9" stroke-linecap="round"/><circle cx="60" cy="60" r="46" fill="none" stroke="#fff" stroke-width="2" opacity=".5"/></g>`],
    // พิษไหม้ อย่าใช้น้ำจืด: a box jellyfish hangs in deep water, its tentacle bundles swaying; a bottle of vinegar tips in
    jelly: () => [`<rect x="-10" y="-10" width="140" height="140" fill="url(#iuDeep)"/>
      ${[[10, 20], [100, 30], [24, 100], [92, 104]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#8ac8ff" opacity=".5"/>`).join("")}
      <g transform="translate(56,38)"><path d="M-30,16Q-30,-24 0,-26Q30,-24 30,16Q18,24 0,22Q-18,24 -30,16Z" fill="#e4f8ff" opacity=".88" ${OUT(2.6)}/>
        <path d="M-22,10Q-20,-14 0,-16Q20,-14 22,10" stroke="#9adcf4" stroke-width="3" fill="none" opacity=".7"/><path d="M-16,-10q6,-6 14,-4" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>
        <g class="iuTent">${[-24, -8, 8, 24].map((x, k) => `<path d="M${x},18q${k % 2 ? 6 : -6},22 0,44t${k % 2 ? -5 : 5},40" stroke="#bfe8ff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".9"/><path d="M${x + 3},20q${k % 2 ? -5 : 5},20 0,42" stroke="#7ab8d8" stroke-width="2" fill="none" stroke-linecap="round" opacity=".8"/>`).join("")}</g></g>`,
    `<g class="iuBot"><g transform="translate(100,96) rotate(-34)"><rect x="-11" y="-30" width="22" height="48" rx="5" fill="#6a3a14" ${OUT(2.4)}/><rect x="-6" y="-42" width="12" height="14" rx="2" fill="#3a2410" ${OUT(2)}/>
        <rect x="-9" y="-12" width="18" height="18" fill="#fff8e8" stroke="#3a2410" stroke-width="1.4"/><path d="M-6,-6h12M-6,-1h12M-6,4h8" stroke="#c83a2a" stroke-width="2"/>
        <path d="M-3,-46q-6,-10 -2,-18" stroke="#fff8e8" stroke-width="3" fill="none" stroke-linecap="round" opacity=".9"/><circle cx="-8" cy="-66" r="3" fill="#fff8e8" opacity=".9"/></g></g>`],
    // เห็นเรือไกล อย่าว่ายตาม: a longtail far on the horizon, a figure on the sand waving, a swimmer heading out is banned
    boat: () => [`<rect x="-10" y="-10" width="140" height="140" fill="url(#iuSeaBg)"/>
      <path d="M-10,58H130V140H-10Z" fill="#3aa8c8"/><path d="M-10,58H130" stroke="#effcff" stroke-width="3" opacity=".8"/>
      ${[[0, 72], [40, 80], [84, 70]].map(([x, y]) => `<path d="M${x},${y}q8,-5 16,0" stroke="#bfe8f8" stroke-width="3" fill="none" stroke-linecap="round"/>`).join("")}
      <g class="iuBoat"><g transform="translate(96,54)"><path d="M-22,2Q-20,8 -14,8H14Q20,8 24,2L26,-2H-26Z" fill="#2a3a4a" ${OUT(1.6)}/><path d="M-10,-2V-14M-10,-14h10l-10,5" fill="#e84a3a" stroke="#2a3a4a" stroke-width="1.4"/><path d="M14,-2l10,-10" stroke="#2a3a4a" stroke-width="2.4"/></g></g>
      <path d="M-10,100Q60,86 130,102V140H-10Z" fill="url(#iuSandG)" ${OUT(2.6)}/>
      <g transform="translate(30,96)"><circle cx="0" cy="-30" r="7" fill="#e3ad84" ${OUT(2)}/><path d="M0,-22V0" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M0,-22V0" stroke="#ff8a3a" stroke-width="4.5" stroke-linecap="round"/>
        <path d="M0,0l-7,16M0,0l7,16M0,-16l-12,8" stroke="${INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/><g class="iuArm"><path d="M0,-16l12,-14" stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/></g></g>
      <g transform="translate(66,78)"><circle cx="0" cy="-6" r="5" fill="#e3ad84" ${OUT(1.6)}/><path d="M-10,0q10,-6 20,0" stroke="#e3ad84" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M-12,2q12,-4 24,0" stroke="#effcff" stroke-width="3" fill="none"/></g>`,
    `<g transform="translate(66,74)"><circle r="16" fill="none" stroke="#e02a1e" stroke-width="5"/><path d="M-11,-11L11,11" stroke="#e02a1e" stroke-width="5" stroke-linecap="round"/></g>`],
  };
  const coin = (name) => {
    const [inside, top] = PICT[name]();
    return `<ellipse class="iuSh" cx="60" cy="120" rx="50" ry="9" fill="url(#iuCoinSh)"/>
      <g class="iuBob"><g class="iuSq">
        <circle cx="60" cy="66" r="52" fill="url(#iuR-${name})" ${OUT(4)}/><path d="M12,66A48,48 0 0 0 108,66" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
        <circle cx="60" cy="57" r="52" fill="url(#iuF-${name})" ${OUT(4)}/>
        <circle cx="60" cy="57" r="45.5" fill="none" stroke="url(#iuBev)" stroke-width="4"/>
        <g transform="translate(60,57) scale(.9) translate(-60,-60)"><g clip-path="url(#iuPicClip)">${inside}</g>${top}</g>
        <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle cx="53.5" cy="15.5" r="2.8" fill="#fff" opacity=".7"/>
      </g></g>`;
  };
  const ICON = Object.fromEntries(Object.keys(PICT).map((n) => [n, () => coin(n)]));
  const icon = (name, x, y, s = 1, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>${ICON[name]()}</g></g>`;
  function iconPop(tl, root, t) {
    if (!root) return;
    root.querySelectorAll(".iuSq").forEach((e) => FT(tl, e, { scaleX: 0.3, scaleY: 1.5, svgOrigin: "60 117" }, { scaleX: 1, scaleY: 1, svgOrigin: "60 117" }, 0.75, "elastic.out(1, 0.42)", t));
  }
  function iconLife(tl, root, t, dur) {
    if (!root || dur <= 0) return;
    const q = (s) => root.querySelectorAll(s), R = (p) => Math.ceil(dur / p) + 1;
    q(".iuBob").forEach((e) => FT(tl, e, { y: 0 }, { y: -5 }, 0.85, "sine.inOut", t, { repeat: R(0.85), yoyo: true }));
    q(".iuSh").forEach((e) => FT(tl, e, { scaleX: 1, opacity: 1, svgOrigin: "60 120" }, { scaleX: 0.8, opacity: 0.55, svgOrigin: "60 120" }, 0.85, "sine.inOut", t, { repeat: R(0.85), yoyo: true }));
    q(".iuRip").forEach((e) => FT(tl, e, { x: -14 }, { x: 14 }, 1.1, "sine.inOut", t, { repeat: R(1.1), yoyo: true }));
    q(".iuBan").forEach((e) => FT(tl, e, { scale: 1, svgOrigin: "60 60" }, { scale: 1.08, svgOrigin: "60 60" }, 0.5, "sine.inOut", t, { repeat: R(0.5), yoyo: true }));
    q(".iuTent").forEach((e) => FT(tl, e, { skewX: -8, svgOrigin: "0 18" }, { skewX: 8, svgOrigin: "0 18" }, 0.9, "sine.inOut", t, { repeat: R(0.9), yoyo: true }));
    q(".iuBot").forEach((e) => FT(tl, e, { rotation: -6, svgOrigin: "100 96" }, { rotation: 6, svgOrigin: "100 96" }, 0.7, "sine.inOut", t, { repeat: R(0.7), yoyo: true }));
    q(".iuBoat").forEach((e) => FT(tl, e, { x: 6, y: 0 }, { x: -8, y: 2 }, 1.3, "sine.inOut", t, { repeat: R(1.3), yoyo: true }));
    q(".iuArm").forEach((e) => FT(tl, e, { rotation: -22, svgOrigin: "0 -16" }, { rotation: 24, svgOrigin: "0 -16" }, 0.22, "sine.inOut", t, { repeat: R(0.22), yoyo: true }));
  }

  // ---------------- shared pieces ----------------
  // a rope from (x, y0) down to (x, y1): twisted, with its shadow
  const rope = (x, y0, y1, w = 12) => `<path d="M${x + 4},${y0}V${y1}" stroke="#000" stroke-width="${w}" opacity=".2"/><path d="M${x},${y0}V${y1}" stroke="${INK}" stroke-width="${w + 4}"/><path d="M${x},${y0}V${y1}" stroke="url(#iuRope)" stroke-width="${w}"/>
    <path d="${Array.from({ length: Math.ceil((y1 - y0) / 14) }, (_, k) => `M${x - w * 0.4},${y0 + k * 14}L${x + w * 0.4},${y0 + k * 14 + 9}`).join("")}" stroke="#7a5a2a" stroke-width="${f1(w * 0.22)}" opacity=".7"/>`;
  // a small wooden tag / plank (x, y top-left) with its dark side
  const plank = (x, y, w, h, r = 12, o = {}) => `<rect x="${x}" y="${y + (o.d ?? 9)}" width="${w}" height="${h}" rx="${r}" fill="url(#iuTagSide)" ${OUT(o.sw ?? 3.4)}/>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="url(#iuTag)" ${OUT(o.sw ?? 3.4)}/>
    <path d="M${x + 16},${y + h * 0.3}q${w * 0.3},6 ${w * 0.6},0M${x + 24},${y + h * 0.66}q${w * 0.3},-5 ${w * 0.5},0" stroke="#9a7a4a" stroke-width="1.8" fill="none" opacity=".55"/>
    <rect x="${x + 8}" y="${y + 4}" width="${w - 16}" height="${Math.min(h * 0.35, 30)}" rx="8" fill="#fff" opacity=".16"/>`;
  // a young coconut split in half seen from above: the green husk ring, the pale meat, the water pool (r = outer radius)
  const halfCoco = (r, o = {}) => `<ellipse cx="${f1(r * 0.08)}" cy="${f1(r * 1.02)}" rx="${f1(r * 1.02)}" ry="${f1(r * 0.22)}" fill="url(#iuSoftSh)" opacity=".7"/>
    <circle r="${r}" cy="${f1(r * 0.08)}" fill="url(#iuHuskB)" ${OUT(4)}/>
    <circle r="${r}" fill="url(#iuHusk)" ${OUT(4)}/>
    ${Array.from({ length: 14 }, (_, k) => { const a = (k / 14) * Math.PI * 2; return `<path d="M${f1(Math.cos(a) * r * 0.86)},${f1(Math.sin(a) * r * 0.86)}L${f1(Math.cos(a) * r * 0.98)},${f1(Math.sin(a) * r * 0.98)}" stroke="#3e6a1e" stroke-width="2" opacity=".55"/>`; }).join("")}
    <circle r="${f1(r * 0.86)}" fill="#f0e2c4" ${OUT(3)}/><circle r="${f1(r * 0.82)}" fill="url(#iuMeat)"/>
    ${o.pool === false ? "" : `<ellipse cx="${f1(r * 0.04)}" cy="${f1(r * 0.12)}" rx="${f1(r * 0.52)}" ry="${f1(r * 0.42)}" fill="url(#iuPool)" opacity=".75"/><path d="M${f1(-r * 0.3)},${f1(-r * 0.08)}q${f1(r * 0.12)},${f1(-r * 0.12)} ${f1(r * 0.3)},${f1(-r * 0.06)}" stroke="#fff" stroke-width="${f1(Math.max(2, r * 0.03))}" fill="none" stroke-linecap="round" opacity=".85"/>`}
    <path d="M${f1(-r * 0.7)},${f1(-r * 0.46)}A${f1(r * 0.86)},${f1(r * 0.86)} 0 0 1 ${f1(-r * 0.2)},${f1(-r * 0.83)}" stroke="#fff" stroke-width="${f1(Math.max(2, r * 0.035))}" fill="none" opacity=".55" stroke-linecap="round"/>`;
  // a letter badge carved on the husk
  const badge = (x, y, r, letter) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#3e2a14" ${OUT(3)}/><circle cx="${x}" cy="${y}" r="${r - 6}" fill="#f6e8c8" stroke="#6a4a28" stroke-width="2"/>
    <text x="${x}" y="${y + r * 0.42}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${f1(r * 1.25)}" fill="#3e2a14">${letter}</text>`;
  // a little campfire (origin at the ground under it): logs, a glow, three flame tongues in #id-fl
  const campfire = (id, s = 1) => `<g transform="scale(${s})"><ellipse cx="0" cy="8" rx="80" ry="20" fill="url(#iuFireGlow)"/>
    <g id="${id}-fl"><path d="M-30,0Q-44,-40 -18,-70Q-20,-40 -2,-56Q4,-30 14,-50Q34,-24 20,0Z" fill="url(#iuFire)" stroke="#a82a08" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M-10,0Q-20,-24 -4,-42Q2,-22 10,-34Q18,-14 10,0Z" fill="#fff2a0" opacity=".85"/></g>
    <path d="M-52,10L28,-10" stroke="${INK}" stroke-width="14" stroke-linecap="round"/><path d="M-52,10L28,-10" stroke="#8a5a30" stroke-width="9" stroke-linecap="round"/>
    <path d="M-30,-8L50,14" stroke="${INK}" stroke-width="14" stroke-linecap="round"/><path d="M-30,-8L50,14" stroke="#a06a38" stroke-width="9" stroke-linecap="round"/>
    ${[-36, -10, 20, 40].map((x) => `<circle cx="${x}" cy="14" r="6" fill="#5a5a60" ${OUT(2)}/>`).join("")}</g>`;

  // ---------------- ตาเวียง's paddle ----------------
  const RULES = [
    ["seawater", "กระ<u>หาย</u>แค่ไหน อย่า<u>หมาย</u>น้ำเค็ม"],
    ["jelly", "พิษ<u>ไหม้</u> อย่า<u>ใช้</u>น้ำจืด"],
    ["boat", "เห็นเรือ<u>ไกล</u> อย่า<u>ว่าย</u>ตาม"],
  ];
  // the blade: a broad old blade seen flat, hung on two ropes; the shaft runs straight up out of the top edge
  const bladePath = (x, y, w, h) => `M${x + 150},${y}H${x + w - 150}Q${x + w},${y} ${x + w},${y + 150}V${y + h - 180}Q${x + w},${y + h} ${x + w - 180},${y + h}H${x + 180}Q${x},${y + h} ${x},${y + h - 180}V${y + 150}Q${x},${y} ${x + 150},${y}Z`;
  function rule(tl, layer, t0, dur, o = {}) {
    const id = nid(), act = o.active ?? 0, done = o.done || [], at = o.at || [0.55, 0.7, 0.85], Y0 = o.y ?? 300;
    const X = 90, W = 900, H = 560, rowY = (k) => Y0 + 150 + k * 150, FS = 46, TX = 140;
    const R = mkR(31);
    const outline = bladePath(X, Y0, W, H);
    let rows = "";
    RULES.forEach(([ic, txt], k) => {
      const st = k === act ? "act" : done.includes(k) ? "done" : "later", y = rowY(k), n = cells(txt), tw = n * 27;
      const t = txt.replace(/<u>(.*?)<\/u>/g, `<tspan class="iuU" fill="${st === "later" ? "#6a5a40" : "#c8281e"}">$1</tspan>`);
      const carve = (fill, op, dx = 0, dy = 0) => `<text x="${TX + dx}" y="${y + 22 + dy}" font-family="Mali" font-weight="700" font-size="${FS}" fill="${fill}" opacity="${op}">${st === "later" ? plain(txt) : t}</text>`;
      rows += `<g id="${id}-r${k}" opacity="${st === "later" ? 0.55 : 0}">
        ${st === "done" ? `<path id="${id}-gp${k}" d="M${TX - 10},${y + 4}Q${TX + tw * 0.3},${y - 14} ${TX + tw * 0.6},${y + 8}T${TX + 10 + tw},${y + 2}" stroke="#2f9a4e" stroke-width="42" fill="none" stroke-linecap="round" opacity=".55" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>` : ""}
        ${st === "act" ? `<g id="${id}-tch" opacity="0"><ellipse cx="${TX}" cy="${y}" rx="190" ry="90" fill="url(#iuGold)"/></g>` : ""}
        ${carve("#fff4dc", st === "later" ? 0.35 : 0.7, -2, -2)}${carve("#2a1a0a", st === "later" ? 0.5 : 0.92, 2, 2)}
        ${st === "act" ? `<defs><clipPath id="${id}-cp"><rect id="${id}-cr" x="${TX - 20}" y="${y - 60}" width="0" height="110"/></clipPath></defs>
          <g clip-path="url(#${id}-cp)"><text x="${TX}" y="${y + 22}" font-family="Mali" font-weight="700" font-size="${FS}" fill="#ffd23a" stroke="#ffd23a" stroke-width="9" stroke-linejoin="round" opacity=".5">${plain(txt)}</text>
          <text x="${TX}" y="${y + 22}" font-family="Mali" font-weight="700" font-size="${FS}" fill="#3a2410">${t}</text></g>` : ""}
        ${st === "done" ? `<path id="${id}-tk${k}" d="M${TX + 24 + tw},${y - 4}l20,24l42,-54" stroke="#1e8a46" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>` : ""}
        ${st === "later" ? Array.from({ length: 4 }, () => `<ellipse cx="${f1(TX + 30 + R() * tw)}" cy="${f1(y - 20 + R() * 40)}" rx="${f1(14 + R() * 22)}" ry="${f1(6 + R() * 8)}" fill="#6a8a3a" opacity=".3"/>`).join("") : ""}
        <g transform="translate(${905},${y - 62})"><g id="${id}-s${k}"${st === "act" ? ` opacity="0"` : ""}>${icon(ic, 0, 0, 1.0, `${id}-ic${k}`)}</g></g></g>`;
    });
    // decor: a crack and old nail holes, barnacle scars, a strip of rope lashing where the shaft meets the blade
    const nails = [[X + 80, Y0 + 90], [X + W - 90, Y0 + H - 110], [X + W - 60, Y0 + 140]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="6" fill="#5a3a1a" opacity=".8"/><path d="M${a - 2},${b + 4}q-2,14 2,26" stroke="#8a5a2a" stroke-width="3" opacity=".3" fill="none"/>`).join("");
    const crack = `<path d="M${X + 300},${Y0 + H - 8}q-10,-40 6,-80q-14,-30 -4,-70" stroke="#4a3418" stroke-width="2.6" fill="none" opacity=".6"/>`;
    const shaft = `<g><path d="M540,${Y0 + 30}V-300" stroke="${INK}" stroke-width="40" stroke-linecap="round"/><path d="M540,${Y0 + 30}V-300" stroke="url(#iuPaddle)" stroke-width="30" stroke-linecap="round"/><path d="M532,${Y0 + 10}V-300" stroke="#fff" stroke-width="5" opacity=".25" stroke-linecap="round"/>
      ${[0, 1, 2, 3, 4].map((k) => `<path d="M520,${Y0 + 50 - k * 11}l40,-7" stroke="#8a6a3a" stroke-width="6" stroke-linecap="round"/>`).join("")}</g>`;
    const tag = `<g transform="translate(${X + 250},${Y0 - 80}) rotate(-6)"><g id="${id}-tag">${plank(-180, -40, 360, 84, 14)}
      <text y="20" text-anchor="middle" font-family="Sriracha" font-size="52" fill="#fff8e8" stroke="#fff8e8" stroke-width="10" stroke-linejoin="round" opacity=".8">กฎของตาเวียง</text>
      <text y="20" text-anchor="middle" font-family="Sriracha" font-size="52" fill="#c8281e">กฎของตาเวียง</text></g></g>`;
    put(layer, `<g id="${id}" opacity="0">${o.glow ? `<g id="${id}-glow" opacity="0"><ellipse cx="540" cy="${Y0 + H / 2}" rx="700" ry="520" fill="url(#iuGold)"/></g>` : ""}<g id="${id}-m"><g id="${id}-sw">${o.glow ? `<path d="${outline}" fill="none" stroke="#ffe27a" stroke-width="34" opacity=".7" stroke-linejoin="round"/><path d="${outline}" fill="none" stroke="#ffd23a" stroke-width="80" opacity=".25" stroke-linejoin="round"/>` : ""}
      ${rope(X + 250, -40, Y0 + 6)}${rope(X + W - 160, -40, Y0 + 50)}
      ${shaft}
      <path d="${outline}" fill="url(#iuPaddleSide)" stroke="${INK}" stroke-width="5" transform="translate(0,16)"/>
      <path d="${outline}" fill="url(#iuPaddle)" stroke="${INK}" stroke-width="5"/>
      <defs><clipPath id="${id}-bc"><path d="${outline}"/></clipPath></defs>
      <g clip-path="url(#${id}-bc)">${Array.from({ length: 9 }, (_, k) => `<path d="M${X + 40},${Y0 + 60 + k * 56 + (k % 2) * 12}q${W * 0.3},${8 + k} ${W * 0.6},0t${W * 0.3},6" stroke="#8a6a3a" stroke-width="${f1(1.4 + (k % 3) * 0.6)}" fill="none" opacity=".35"/>`).join("")}
        <rect x="${X}" y="${Y0}" width="${W}" height="60" fill="#fff" opacity=".12"/>${crack}</g>
      ${[[X + 250, Y0 + 12], [X + W - 160, Y0 + 56]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="11" fill="#5a3a22" ${OUT(2)}/><circle cx="${a}" cy="${b}" r="5" fill="#2a1a10"/>`).join("")}
      ${nails}${rows}${tag}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    if (o.glow) { FT(tl, `#${id}-glow`, { opacity: 0, scale: 0.6, svgOrigin: `540 ${Y0 + H / 2}` }, { opacity: 1, scale: 1, svgOrigin: `540 ${Y0 + H / 2}` }, 0.8, "power2.out", t0); FT(tl, `#${id}-glow`, { scale: 1, svgOrigin: `540 ${Y0 + H / 2}` }, { scale: 1.08, svgOrigin: `540 ${Y0 + H / 2}` }, 1.1, "sine.inOut", t0 + 0.8, { repeat: Math.ceil(dur / 1.1), yoyo: true }); }
    // in: dropped on its ropes, swings and settles, then sways; the title tag lags behind
    FT(tl, `#${id}-m`, { y: -1100 }, { y: 0 }, 0.55, "power3.out", t0);
    FT(tl, `#${id}-sw`, { rotation: 4, svgOrigin: `540 ${Y0 - 900}` }, { rotation: 0, svgOrigin: `540 ${Y0 - 900}` }, 1.6, "elastic.out(1, 0.32)", t0 + 0.4);
    FT(tl, `#${id}-sw`, { rotation: 0, svgOrigin: `540 ${Y0 - 900}` }, { rotation: 0.5, svgOrigin: `540 ${Y0 - 900}` }, 1.3, "sine.inOut", t0 + 2, { repeat: Math.ceil(dur / 1.3), yoyo: true });
    FT(tl, `#${id}-tag`, { rotation: -10, svgOrigin: "0 -40" }, { rotation: 6, svgOrigin: "0 -40" }, 0.9, "sine.inOut", t0 + 0.5, { repeat: Math.ceil(dur / 0.9), yoyo: true });
    RULES.forEach((_, k) => { if (k === act || done.includes(k)) FT(tl, `#${id}-r${k}`, { x: -50, opacity: 0 }, { x: 0, opacity: 1 }, 0.35, "power2.out", t0 + at[k]); });
    if (act >= 0 && act < 3) {
      const ta = t0 + at[act];
      // the torch sweep crosses the line and the carving fills with gold behind it
      FT(tl, `#${id}-tch`, { opacity: 0 }, { opacity: 1 }, 0.2, "none", ta + 0.1);
      FT(tl, `#${id}-tch`, { x: 0 }, { x: 720 }, 1.1, "power1.inOut", ta + 0.1);
      tl.to(`#${id}-tch`, { opacity: 0.35, duration: 0.4 }, ta + 1.3);
      FT(tl, `#${id}-tch`, { x: 720 }, { x: 300 }, 1.6, "sine.inOut", ta + 1.7, { repeat: Math.ceil(dur / 1.6), yoyo: true });
      FT(tl, `#${id}-cr`, { attr: { width: 0 } }, { attr: { width: 780 } }, 1.0, "power1.inOut", ta + 0.15);
      FT(tl, `#${id}-s${act}`, { scale: 0, rotation: -40, opacity: 1, svgOrigin: "60 60" }, { scale: 1, rotation: 0, opacity: 1, svgOrigin: "60 60" }, 0.5, "back.out(2.6)", ta + 0.4);
      iconPop(tl, document.getElementById(`${id}-ic${act}`), ta + 0.4);
      iconLife(tl, document.getElementById(`${id}-ic${act}`), ta + 1.0, dur - at[act] - 1.0);
      document.getElementById(`${id}-r${act}`).querySelectorAll(".iuU").forEach((u, j) => FT(tl, u, { attr: { fill: "#c8281e" } }, { attr: { fill: "#ffd23a" } }, 0.16, "power2.out", ta + 1.2 + j * 0.25, { yoyo: true, repeat: 3 })); // the rhyme syllables flash gold in turn
    }
    done.forEach((d) => {
      const gp = document.getElementById(`${id}-gp${d}`), tk = document.getElementById(`${id}-tk${d}`);
      if (gp) FT(tl, gp, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 } }, 0.45, "power2.inOut", t0 + at[d] + 0.2);
      if (tk) FT(tl, tk, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 } }, 0.35, "power2.out", t0 + at[d] + 0.5);
    });
    if (o.out !== undefined) { tl.to(`#${id}-m`, { y: -220, duration: 0.3, ease: "power2.in" }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + o.out); }
    return id;
  }

  // ---------------- the survival HUD ----------------
  const BOTTLE = "M44,0H76V22Q110,28 114,74Q120,124 94,156Q60,172 26,156Q0,124 6,74Q10,28 44,22Z";
  function hud(tl, layer, t0, dur, o = {}) {
    const id = nid(), water = o.water && o.water.length ? o.water : [[0, 100]], forks = o.forks || [0, 3];
    const H = 172, lvl = (p) => H - 6 - (H - 14) * Math.max(0, Math.min(100, p)) / 100;
    let g = `<g transform="translate(40,130)"><g id="${id}" opacity="0">
      <g transform="translate(0,0)"><g id="${id}-bt">
        <ellipse cx="62" cy="178" rx="54" ry="10" fill="url(#iuSoftSh)" opacity=".6"/>
        <defs><clipPath id="${id}-bc"><path d="${BOTTLE}"/></clipPath></defs>
        <path d="${BOTTLE}" fill="#f2f7f9" opacity=".7" ${OUT(3.4)}/>
        <g clip-path="url(#${id}-bc)"><rect id="${id}-w" x="0" y="${f1(lvl(water[0][1]))}" width="120" height="200" fill="url(#iuHudW)"/><rect id="${id}-wr" x="0" y="${f1(lvl(water[0][1]))}" width="120" height="200" fill="url(#iuHudR)" opacity="0"/>
          <path id="${id}-ws" d="M-10,${f1(lvl(water[0][1]))}q15,-6 30,0t30,0t30,0t30,0t30,0" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/>
          <g id="${id}-bub" opacity="0">${[[30, 0], [62, 18], [88, 6]].map(([x, y]) => `<circle cx="${x}" cy="${150 + y}" r="4" fill="#fff" opacity=".8"/>`).join("")}</g></g>
        <path d="${BOTTLE}" fill="url(#iuGlass)"/><path d="M22,54Q14,90 22,130" stroke="#fff" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>
        <rect x="40" y="-14" width="40" height="22" rx="4" fill="url(#iuCork)" ${OUT(2.6)}/><path d="M46,-10v14M54,-11v16M62,-10v14M70,-11v15" stroke="#7a5a30" stroke-width="1.6" opacity=".6"/>
        <text x="60" y="66" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="22" fill="#1e2a3a" stroke="#fff" stroke-width="4" paint-order="stroke" opacity=".9">น้ำในตัว</text>
        <text id="${id}-pct" x="60" y="112" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#1e2a3a" stroke="#fff" stroke-width="5" paint-order="stroke">${Math.round(water[0][1])}%</text>
        <g id="${id}-dr" opacity="0">${[[118, 70], [112, 110]].map(([x, y]) => `<path d="M${x},${y}q-5,8 0,14q5,-6 0,-14z" fill="#bfe8ff" ${OUT(1.6)}/>`).join("")}</g>
      </g></g>
      <g transform="translate(140,6)"><g id="${id}-tag"><path d="M-8,-6V-26q8,-10 16,0V-6" stroke="${INK}" stroke-width="7" fill="none"/><path d="M-8,-6V-26q8,-10 16,0V-6" stroke="url(#iuRope)" stroke-width="4" fill="none"/>
        ${plank(-18, -6, 210, 56, 10, { d: 7 })}<text x="88" y="32" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="27" fill="#2a1a0a">${typeof o.day === "number" ? `วันที่ ${o.day}` : o.day || "วันที่ 1"}</text></g></g>
      <g transform="translate(140,90)"><g id="${id}-fk">${Array.from({ length: forks[1] }, (_, k) => `<g transform="translate(${30 + k * 66},28)"><g id="${id}-h${k}">${k < forks[0] ? halfCoco(26) : `<circle r="26" cy="2" fill="#2a1a0a" opacity=".5"/><circle r="26" fill="url(#iuHuskB)" ${OUT(3)}/><circle r="18" fill="#1a1008" stroke="#6a4a28" stroke-width="2" stroke-dasharray="4 4"/>`}</g></g>`).join("")}
        <text x="30" y="80" font-family="Kanit" font-weight="700" font-size="22" fill="#f4ecd8" stroke="#1e2a3a" stroke-width="4" paint-order="stroke" opacity=".9">ทางแยก ${forks[0]}/${forks[1]}</text></g></g>
    </g></g>`;
    put(layer, g);
    FT(tl, `#${id}`, { opacity: 0 }, { opacity: 1 }, 0.2, "none", t0);
    FT(tl, `#${id}-bt`, { scale: 0, svgOrigin: "60 160" }, { scale: 1, svgOrigin: "60 160" }, 0.55, "back.out(2.2)", t0);
    FT(tl, `#${id}-tag`, { x: -80, opacity: 0 }, { x: 0, opacity: 1 }, 0.4, "back.out(2)", t0 + 0.15);
    FT(tl, `#${id}-tag`, { rotation: -4, svgOrigin: "0 -26" }, { rotation: 3, svgOrigin: "0 -26" }, 1.1, "sine.inOut", t0 + 0.6, { repeat: Math.ceil(dur / 1.1), yoyo: true });
    for (let k = 0; k < forks[1]; k++) FT(tl, `#${id}-h${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0" }, 0.45, "back.out(2.6)", t0 + 0.3 + k * 0.12);
    FT(tl, `#${id}-ws`, { x: -30 }, { x: 0 }, 1.0, "none", t0, { repeat: Math.ceil(dur / 1.0) });
    // the level follows the keyframes; red creeps in as it falls, drops run while it is falling, bubbles when it rises
    const W = document.getElementById(`${id}-w`), WR = document.getElementById(`${id}-wr`), WS = document.getElementById(`${id}-ws`), P = document.getElementById(`${id}-pct`), c = { v: water[0][1] };
    const draw = () => { const y = lvl(c.v); W.setAttribute("y", f1(y)); WR.setAttribute("y", f1(y)); WR.setAttribute("opacity", f1(Math.max(0, Math.min(1, (38 - c.v) / 26)))); WS.setAttribute("transform", `translate(0,${f1(y - lvl(water[0][1]))})`); P.textContent = `${Math.round(c.v)}%`; };
    for (let k = 1; k < water.length; k++) {
      const [ta, pa] = water[k - 1], [tb, pb] = water[k], d = Math.max(0.05, tb - ta);
      tl.to(c, { v: pb, duration: d, ease: "none", immediateRender: false, onUpdate: draw }, t0 + ta);
      if (pb < pa) { FT(tl, `#${id}-dr`, { opacity: 0, y: 0 }, { opacity: 1, y: 40 }, Math.min(1.2, d), "power1.in", t0 + ta, { repeat: Math.max(0, Math.ceil(d / 1.2) - 1) }); tl.to(`#${id}-dr`, { opacity: 0, duration: 0.2 }, t0 + tb); }
      else if (pb > pa) { FT(tl, `#${id}-bub`, { opacity: 0, y: 0 }, { opacity: 1, y: -70 }, Math.min(0.9, d), "power1.out", t0 + ta, { repeat: Math.max(0, Math.ceil(d / 0.9) - 1) }); tl.to(`#${id}-bub`, { opacity: 0, duration: 0.2 }, t0 + tb); }
      if (pb <= 25 && pa > 25) FT(tl, P, { scale: 1, svgOrigin: "60 100" }, { scale: 1.3, svgOrigin: "60 100" }, 0.25, "power2.out", t0 + tb - 0.1, { yoyo: true, repeat: 3 });
    }
    if (o.out !== undefined) { tl.to(`#${id}-bt`, { scale: 0, svgOrigin: "60 160", duration: 0.3, ease: "back.in(2)" }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + o.out); }
    return id;
  }

  // ---------------- the fork card ----------------
  function fork(tl, layer, t0, dur, o = {}) {
    const id = nid(), secs = o.secs ?? 3, A = o.a || { text: "ดื่ม" }, B = o.b || { text: "ไม่ดื่ม" }, vote = !!o.vote, q = o.q || "คุณจะทำอะไร?";
    const CY = 940, CX = [300, 780], RR = 212;
    const half = (k, c) => {
      const lines = String(c.text).split("|"), fs = Math.max(42, Math.min(62, Math.floor(300 / (0.56 * Math.max(...lines.map(cells)))))), n = lines.length;
      return `<g transform="translate(${CX[k]},${CY})"><g id="${id}-e${k}" opacity="0"><g id="${id}-q${k}"><g id="${id}-c${k}">
        ${halfCoco(RR)}${badge(-150, -150, 36, k ? "B" : "A")}
        <g id="${id}-f${k}" opacity="0"><circle r="${RR + 16}" fill="none" stroke="#ffd23a" stroke-width="22" opacity=".3"/><circle r="${RR + 10}" fill="none" stroke="#ffd23a" stroke-width="9"/></g>
        ${lines.map((l, j) => `<text y="${f1(26 + (j - (n - 1) / 2) * (fs + 8))}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${fs}" fill="#fff8ec" stroke="#fff8ec" stroke-width="12" stroke-linejoin="round" opacity=".75">${l}</text>
          <text y="${f1(26 + (j - (n - 1) / 2) * (fs + 8))}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${fs}" fill="#1e2a3a">${l}</text>`).join("")}
        <g id="${id}-dim${k}" opacity="0"><circle r="${RR + 2}" fill="#06121a" opacity=".55"/></g>
        <g id="${id}-st${k}" opacity="0"><g transform="rotate(-12) translate(0,-124)"><g id="${id}-sts${k}">
          <rect x="-176" y="-48" width="352" height="96" rx="16" fill="#fff4ec" opacity=".9"/><rect x="-176" y="-48" width="352" height="96" rx="16" fill="none" stroke="#e02a1e" stroke-width="8"/><rect x="-165" y="-37" width="330" height="74" rx="10" fill="none" stroke="#e02a1e" stroke-width="3" stroke-dasharray="10 6"/>
          <text y="13" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#e02a1e">คนส่วนใหญ่เลือก</text></g></g></g>
      </g></g></g></g>`;
    };
    const Q = `<g transform="translate(540,470)"><g id="${id}-qe" opacity="0"><g id="${id}-qs">
      ${rope(-330, -470, -84, 11)}${rope(330, -470, -84, 11)}
      <ellipse cx="0" cy="100" rx="420" ry="32" fill="url(#iuSoftSh)" opacity=".55"/>
      ${plank(-430, -84, 860, 168, 20, { d: 14, sw: 5 })}
      <text y="26" text-anchor="middle" font-family="Sriracha" font-size="${cells(q) > 14 ? 60 : 74}" fill="#fff8e8" stroke="#fff8e8" stroke-width="12" stroke-linejoin="round" opacity=".8">${q}</text>
      <text y="26" text-anchor="middle" font-family="Sriracha" font-size="${cells(q) > 14 ? 60 : 74}" fill="#c8281e">${q}</text></g></g></g>`;
    const fire = `<g transform="translate(540,1310)"><g id="${id}-fe" opacity="0">${campfire(id, 1.6)}
      <text id="${id}-n" y="-150" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#fff" stroke="#1e2a3a" stroke-width="7" paint-order="stroke">${secs}</text>
      <g id="${id}-smk" opacity="0">${[[-10, -40], [8, -70], [-4, -100]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="14" fill="#c8c8c8" opacity=".55"/>`).join("")}</g></g></g>`;
    const voteSign = `<g transform="translate(540,1430)"><g id="${id}-vs" opacity="0"><g id="${id}-vss">${plank(-350, -50, 700, 100, 18, { d: 10, sw: 4 })}
      <g transform="translate(-290,0)"><path d="M-24,-20H24Q32,-20 32,-12V8Q32,16 24,16H0L-12,28V16H-24Q-32,16 -32,8V-12Q-32,-20 -24,-20Z" fill="#1e2a3a"/><circle cx="-12" cy="-2" r="3" fill="#fff"/><circle cx="0" cy="-2" r="3" fill="#fff"/><circle cx="12" cy="-2" r="3" fill="#fff"/></g>
      <text x="30" y="16" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#2a1a0a">คอมเมนต์เลือก A หรือ B</text></g></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect id="${id}-dimall" width="1080" height="1920" fill="#06121a" opacity=".5"/>${Q}${half(0, A)}${half(1, B)}${fire}${voteSign}</g>`);
    FT(tl, `#${id}`, { opacity: 0 }, { opacity: 1 }, 0.18, "none", t0);
    FT(tl, `#${id}-qe`, { y: -120, opacity: 0 }, { y: 0, opacity: 1 }, 0.4, "power3.out", t0);
    FT(tl, `#${id}-qs`, { rotation: -3, svgOrigin: "0 -470" }, { rotation: 0, svgOrigin: "0 -470" }, 1.4, "elastic.out(1, 0.35)", t0 + 0.2);
    FT(tl, `#${id}-qs`, { rotation: 0, svgOrigin: "0 -470" }, { rotation: 0.8, svgOrigin: "0 -470" }, 1.2, "sine.inOut", t0 + 1.6, { repeat: Math.ceil(dur / 1.2), yoyo: true });
    [0, 1].forEach((k) => {
      const t = t0 + 0.15 + k * 0.14;
      FT(tl, `#${id}-e${k}`, { y: 180, opacity: 0 }, { y: 0, opacity: 1 }, 0.35, "power3.out", t);
      FT(tl, `#${id}-q${k}`, { scaleX: 0.7, scaleY: 1.25, svgOrigin: "0 0" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 0" }, 0.85, "elastic.out(1, 0.5)", t);
      FT(tl, `#${id}-c${k}`, { rotation: k ? 2 : -2, svgOrigin: "0 0" }, { rotation: k ? -2 : 2, svgOrigin: "0 0" }, 1.5 + k * 0.2, "sine.inOut", t + 0.6, { repeat: Math.ceil(dur / 1.5), yoyo: true });
    });
    // the fire burns down over secs; the number counts
    FT(tl, `#${id}-fe`, { opacity: 0, scale: 0.4, svgOrigin: "0 0" }, { opacity: 1, scale: 1, svgOrigin: "0 0" }, 0.45, "back.out(2)", t0 + 0.3);
    const n = document.getElementById(`${id}-n`), cnt = { k: 0 }, T = Math.min(secs, dur - 0.8);
    FT(tl, `#${id}-fl`, { scaleY: 1, scaleX: 1, svgOrigin: "0 0" }, { scaleY: 0.12, scaleX: 0.6, svgOrigin: "0 0" }, T, "power1.in", t0 + 0.45);
    FT(tl, `#${id}-fl`, { skewX: -6 }, { skewX: 6 }, 0.14, "sine.inOut", t0, { repeat: Math.ceil(dur / 0.14), yoyo: true });
    tl.to(cnt, { k: 1, duration: T, ease: "none", immediateRender: false, onUpdate: () => { n.textContent = String(Math.max(0, Math.ceil(secs * (1 - cnt.k) - 0.001))); } }, t0 + 0.45);
    for (let m = secs - 1; m >= 0; m--) { const tm = t0 + 0.45 + secs * (1 - m / secs); if (tm < t0 + dur - 0.3) FT(tl, n, { scale: 1.5, svgOrigin: "0 -140" }, { scale: 1, svgOrigin: "0 -140" }, 0.3, "back.out(3)", tm); }
    FT(tl, `#${id}-smk`, { opacity: 0, y: 0 }, { opacity: 0.8, y: -60 }, 0.8, "power1.out", t0 + 0.45 + T);
    tl.to(`#${id}-smk`, { opacity: 0, duration: 0.4 }, t0 + 0.45 + T + 0.8);
    // the frame hovers between the halves while the fire burns
    const focus = (t, k) => { tl.set(`#${id}-f${k}`, { opacity: 1 }, t); tl.set(`#${id}-f${1 - k}`, { opacity: 0 }, t); };
    const pk = o.pick === "b" ? 1 : o.pick === "a" ? 0 : -1, PT = o.pickAt ?? Math.min(secs + 0.5, dur - 1.0);
    const hov = o.hover || [[0.6, 0], [1.2, 1], [1.8, 0], [2.4, 1]];
    hov.filter(([t]) => t < (pk >= 0 ? PT : T + 0.45)).forEach(([t, k]) => focus(t0 + t, k));
    if (pk >= 0 && !vote) {
      const tp = t0 + PT, other = 1 - pk;
      focus(tp, pk);
      FT(tl, `#${id}-st${pk}`, { opacity: 0 }, { opacity: 1 }, 0.05, "none", tp);
      FT(tl, `#${id}-sts${pk}`, { scale: 2.2, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0" }, 0.22, "power3.in", tp);
      FT(tl, `#${id}-q${pk}`, { x: 0 }, { x: 10 }, 0.08, "none", tp + 0.2, { yoyo: true, repeat: 5 });
      FT(tl, `#${id}-e${pk}`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.12, svgOrigin: "0 0" }, 0.5, "back.out(2)", tp + 0.25);
      FT(tl, `#${id}-dim${other}`, { opacity: 0 }, { opacity: 1 }, 0.4, "none", tp + 0.1);
      FT(tl, `#${id}-e${other}`, { scale: 1, svgOrigin: "0 0" }, { scale: 0.9, svgOrigin: "0 0" }, 0.5, "power2.out", tp + 0.1);
      tl.set(n, { textContent: "!" }, tp);
    }
    if (vote) {
      const tv = t0 + 0.45 + T;
      for (let k = 0; k < 10; k++) { const tk = tv + k * 0.28; if (tk < t0 + dur - 0.2) focus(tk, k % 2); }
      FT(tl, `#${id}-vs`, { opacity: 0, y: 80 }, { opacity: 1, y: 0 }, 0.4, "back.out(2.2)", tv + 0.2);
      FT(tl, `#${id}-vss`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.05, svgOrigin: "0 0" }, 0.5, "sine.inOut", tv + 0.7, { repeat: Math.ceil(dur / 0.5), yoyo: true });
      tl.set(n, { textContent: "?" }, tv);
    }
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.15 }, t0 + o.out);
    return id;
  }
  const choice = (tl, layer, t0, dur, o = {}) => fork(tl, layer, t0, dur, { ...o, vote: true });

  // ---------------- the dead end ----------------
  function dark(tl, layer, t0, dur, o = {}) {
    const id = nid(), text = o.text || "ทางนี้… คุณไม่ถึงเช้า", tA = o.textAt ?? 0.5, ta = t0 + (tA <= 1 ? tA * dur : tA); // textAt: a fraction of dur, or seconds when > 1
    let pulse = "M-300,0";
    for (let k = 0; k < 4; k++) pulse += ` h${40 - k * 6} l6,-${38 - k * 9} l10,${64 - k * 14} l8,-${30 - k * 6} h${36 + k * 10}`;
    pulse += " h200";
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-eg"><rect x="-540" y="-960" width="2160" height="3840" fill="url(#iuDarkEdge)"/></g><rect id="${id}-bk" width="1080" height="1920" fill="#050a14" opacity="0"/>
      <g transform="translate(540,1180)"><path id="${id}-pl" d="${pulse}" stroke="#e8382a" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" opacity=".9"/><path d="M-300,0H300" stroke="#e8382a" stroke-width="3" opacity=".25"/></g>
      <g transform="translate(540,900)"><g id="${id}-tx" opacity="0"><text y="0" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${cells(text) > 16 ? 64 : 78}" fill="#e8382a" stroke="#1a0608" stroke-width="10" paint-order="stroke" stroke-linejoin="round">${text}</text></g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    FT(tl, `#${id}-eg`, { scale: 2.6, svgOrigin: "540 960" }, { scale: 0.9, svgOrigin: "540 960" }, Math.max(0.6, dur * 0.55), "power2.inOut", t0);
    FT(tl, `#${id}-bk`, { opacity: 0 }, { opacity: 0.94 }, Math.max(0.5, dur * 0.4), "power2.in", t0 + dur * 0.45);
    FT(tl, `#${id}-pl`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 } }, Math.max(0.8, dur * 0.7), "power1.in", t0 + 0.1);
    FT(tl, `#${id}-pl`, { opacity: 0.9 }, { opacity: 0.25 }, 0.6, "power2.in", t0 + dur - 0.7);
    FT(tl, `#${id}-tx`, { opacity: 0, y: 40 }, { opacity: 1, y: 0 }, 0.6, "power2.out", ta);
    FT(tl, `#${id}-tx`, { x: 0 }, { x: 3 }, 0.07, "none", ta + 0.6, { repeat: Math.ceil((dur - (ta - t0) - 0.6) / 0.07), yoyo: true });
    return id;
  }

  // ---------------- the rewind ----------------
  function rewind(tl, layer, t0, dur, o = {}) {
    const id = nid(), ra = o.ruleAt ?? 1.0;
    put(layer, `<g id="${id}" opacity="0"><rect width="1080" height="1920" fill="#1a3a4a" opacity=".35"/><rect width="1080" height="1920" fill="url(#iuScan)"/>
      <g id="${id}-rg">${[0, 1, 2, 3, 4].map((k) => `<circle id="${id}-ring${k}" cx="540" cy="960" r="${120 + k * 170}" fill="none" stroke="#9ae8ff" stroke-width="6" opacity=".55"/>`).join("")}</g>
      <g transform="translate(140,220)"><g id="${id}-ch"><rect x="-70" y="-44" width="330" height="88" rx="20" fill="#06121a" opacity=".6"/><path d="M-40,0L-8,-26V26ZM-4,0L28,-26V26Z" fill="#9ae8ff"/>
        <text x="48" y="14" font-family="Kanit" font-weight="800" font-size="40" fill="#9ae8ff">ย้อนกลับ</text></g></g>
      <g transform="translate(540,1420)"><rect x="-440" y="-8" width="880" height="16" rx="8" fill="#06121a" opacity=".6"/><rect id="${id}-bar" x="-440" y="-8" width="880" height="16" rx="8" fill="#9ae8ff" opacity=".8"/><circle id="${id}-kn" cx="440" cy="0" r="22" fill="#fff" ${OUT(3)}/></g></g>`);
    FT(tl, `#${id}`, { opacity: 0 }, { opacity: 1 }, 0.12, "none", t0);
    [0, 1, 2, 3, 4].forEach((k) => FT(tl, `#${id}-ring${k}`, { scale: 2.2, opacity: 0, svgOrigin: "540 960" }, { scale: 0.05, opacity: 0.7, svgOrigin: "540 960" }, 0.9, "power1.in", t0 + k * 0.12, { repeat: Math.ceil(ra / 0.9) }));
    FT(tl, `#${id}-kn`, { attr: { cx: 440 } }, { attr: { cx: -440 } }, ra, "power1.inOut", t0);
    FT(tl, `#${id}-bar`, { attr: { width: 880 } }, { attr: { width: 0 } }, ra, "power1.inOut", t0);
    FT(tl, `#${id}-ch`, { opacity: 1 }, { opacity: 0.3 }, 0.18, "none", t0, { repeat: Math.ceil(ra / 0.18), yoyo: true });
    tl.to(`#${id}`, { opacity: 0, duration: 0.35 }, t0 + ra);
    rule(tl, layer, t0 + ra - 0.2, dur - ra + 0.2, { active: o.rule ?? 0, y: 300, glow: true, at: [0.4, 0.55, 0.7], ...(o.ruleOpts || {}) });
    return id;
  }

  // ---------------- chips ----------------
  function chip(tl, layer, t0, dur, o = {}) {
    const id = nid(), text = o.text || "", x = o.x ?? 540, y = o.y ?? 190, w = cells(text) * 21 + 90, h = 66;
    put(layer, `<g transform="translate(${x},${y})"><g id="${id}" opacity="0"><g id="${id}-s"><path d="M-14,-30V-60q14,-16 28,0V-30" stroke="${INK}" stroke-width="8" fill="none"/><path d="M-14,-30V-60q14,-16 28,0V-30" stroke="url(#iuRope)" stroke-width="4.5" fill="none"/>
      ${plank(-w / 2, -33, w, h, 12, { d: 8 })}<text y="12" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="#2a1a0a">${text}</text></g></g></g>`);
    FT(tl, `#${id}`, { opacity: 0, y: -90 }, { opacity: 1, y: 0 }, 0.45, "back.out(2.2)", t0);
    FT(tl, `#${id}-s`, { rotation: -7, svgOrigin: "0 -60" }, { rotation: 5, svgOrigin: "0 -60" }, 1.0, "sine.inOut", t0 + 0.3, { repeat: Math.ceil(dur / 1.0), yoyo: true });
    tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  }
  function source(tl, layer, t0, dur, o = {}) {
    const id = nid(), text = o.text || "", w = Math.round(cells(text) * 14.5 + 108), y = o.y ?? 1790;
    put(layer, `<g transform="translate(540,${y})"><g id="${id}" opacity="0">
      <rect x="${-w / 2}" y="-26" width="${w}" height="58" rx="29" fill="#6a4a28" stroke="${INK}" stroke-width="3" transform="translate(0,7)"/>
      <rect x="${-w / 2}" y="-30" width="${w}" height="58" rx="29" fill="url(#iuSandPill)" stroke="${INK}" stroke-width="3"/>
      <g transform="translate(${-w / 2 + 31},-1)"><circle r="20" fill="url(#iuHuskB)" stroke="${INK}" stroke-width="2.4"/><circle r="13" fill="#f6ecd8"/><circle cx="-4" cy="-3" r="2.4" fill="#5a3a1a"/><circle cx="4" cy="-3" r="2.4" fill="#5a3a1a"/><circle cx="0" cy="5" r="2.4" fill="#5a3a1a"/></g>
      <text x="${-w / 2 + 62}" y="9" font-family="Kanit" font-weight="500" font-size="26" fill="#1e2a3a">${text}</text></g></g>`);
    FT(tl, `#${id}`, { opacity: 0, y: 30, scale: 0.85, svgOrigin: "0 0" }, { opacity: 1, y: 0, scale: 1, svgOrigin: "0 0" }, 0.45, "back.out(2)", t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
    return id;
  }
  function symptom(tl, layer, t0, dur, o = {}) {
    const id = nid(), items = o.items || [], x = o.x ?? 640, y = o.y ?? 330, gap = o.gap ?? 0.3, w = 420, h = 74;
    put(layer, `<g transform="translate(${x},${y})"><g id="${id}">${items.map((t, k) => `<g transform="translate(0,${k * 90})"><g id="${id}-i${k}" opacity="0"><g id="${id}-s${k}">
      <rect x="${-w / 2}" y="${-h / 2 + 8}" width="${w}" height="${h}" rx="10" fill="#4e6a1e" ${OUT(3)}/><rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="10" fill="url(#iuLeafWeave)" ${OUT(3)}/>
      <rect x="${-w / 2 + 12}" y="${-h / 2 + 10}" width="${w - 24}" height="${h - 20}" rx="8" fill="#fffaf0" opacity=".82"/>
      <circle cx="${-w / 2 + 44}" cy="0" r="12" fill="#e02a1e" ${OUT(2.4)}/><text x="${-w / 2 + 74}" y="13" font-family="Mali" font-weight="700" font-size="36" fill="#8a1a10">${t}</text></g></g></g>`).join("")}</g></g>`);
    items.forEach((_, k) => {
      const t = t0 + k * gap;
      FT(tl, `#${id}-i${k}`, { opacity: 0, x: 120 }, { opacity: 1, x: 0 }, 0.35, "back.out(1.8)", t);
      FT(tl, `#${id}-s${k}`, { rotation: 6, svgOrigin: `${-w / 2} 0` }, { rotation: 0, svgOrigin: `${-w / 2} 0` }, 0.9, "elastic.out(1, 0.45)", t);
      FT(tl, `#${id}-s${k}`, { rotation: 0, svgOrigin: `${-w / 2} 0` }, { rotation: -1.2, svgOrigin: `${-w / 2} 0` }, 1.1 + k * 0.1, "sine.inOut", t + 1, { repeat: Math.ceil(dur / 1.1), yoyo: true });
    });
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + o.out);
    else tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
    return id;
  }

  // ---------------- the end card: a bottle on the wet sand at dusk ----------------
  function endCard(tl, layer, t0, dur, o = {}) {
    const id = nid(), R = mkR(17), fin = !!o.final, l1 = o.l1 || (fin ? "ติดเกาะ" : "ตอนที่ 2"), l2 = o.l2 || (fin ? "ตอนจบ" : "พิษไหม้");
    const fit = (t, max) => Math.min(max, Math.floor(300 / (0.6 * Math.max(1, cells(t)))));
    let bg = `<rect width="1080" height="1920" fill="url(#iuDusk)"/>
      <circle cx="300" cy="420" r="70" fill="#fff6d8" opacity=".95"/><circle cx="300" cy="420" r="150" fill="#fff6d8" opacity=".12"/>
      ${Array.from({ length: 5 }, (_, k) => `<path d="M${-60 + k * 240},${560 + (k % 3) * 90}q110,-36 220,0q-70,22 -220,0Z" fill="#ffb4a0" opacity=".22"/>`).join("")}
      <path d="M-20,1080L160,990L250,1030L330,960L470,1080Z" fill="#2a1a3a" opacity=".8"/>
      <rect y="1080" width="1080" height="400" fill="url(#iuDuskSea)"/>`;
    for (let k = 0; k < 14; k++) bg += `<rect id="${id}-gl${k}" x="${f1(140 + (R() - 0.5) * 360)}" y="${f1(1092 + k * 24 + R() * 10)}" width="${f1(40 + R() * 100)}" height="4" rx="2" fill="#ffe6a8" opacity=".5"/>`;
    bg += `<path id="${id}-sand" d="M-20,1500Q540,1440 1100,1490V1920H-20Z" fill="url(#iuWetSand)"/>
      <path id="${id}-wash" d="M-20,1480Q300,1440 540,1468T1100,1470V1560Q540,1520 -20,1560Z" fill="#8ab8c8" opacity=".55"/>
      <path id="${id}-foam" d="M-20,1478Q300,1438 540,1466T1100,1468" stroke="#fff" stroke-width="9" fill="none" opacity=".85" stroke-linecap="round"/>
      ${Array.from({ length: 12 }, () => `<ellipse cx="${f1(R() * 1080)}" cy="${f1(1560 + R() * 320)}" rx="${f1(10 + R() * 40)}" ry="${f1(3 + R() * 5)}" fill="#fff" opacity="${f1(0.08 + R() * 0.12)}"/>`).join("")}
      ${[[180, 1700], [860, 1760], [420, 1850]].map(([x, y]) => `<path d="M${x - 18},${y}a18,13 0 0 1 36,0l-18,9z" fill="#f4e8d8" stroke="#8a7a62" stroke-width="2"/>`).join("")}`;
    // the bottle lying tilted on the sand: its mouth to the upper-right, the note flat inside, the cork
    const bottle = `<g transform="translate(540,1450) rotate(-18)"><g id="${id}-bt">
      <ellipse cx="0" cy="190" rx="300" ry="34" fill="url(#iuSoftSh)" opacity=".55"/>
      <path d="M-270,-140Q-300,-140 -300,-100V120Q-300,160 -260,160H230Q300,160 300,100V-80Q300,-140 230,-140Z" fill="#9adcd8" opacity=".3" ${OUT(5)}/>
      <g transform="translate(300,-10)"><rect x="-10" y="-70" width="110" height="140" rx="30" fill="#9adcd8" opacity=".3" ${OUT(5)}/><rect x="60" y="-54" width="90" height="108" rx="22" fill="url(#iuCork)" ${OUT(4)}/><path d="M80,-40v80M104,-44v88M126,-40v80" stroke="#7a5a30" stroke-width="2.4" opacity=".6"/></g>
      <g id="${id}-nt"><path d="M-230,-104H200V124H-230Z" fill="url(#iuNote)" stroke="#a8946a" stroke-width="3"/><path d="M-230,-104V124" stroke="#d8c8a4" stroke-width="10" opacity=".7"/>
        <text x="-14" y="${fin ? -6 : -10}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fit(l1, fin ? 60 : 54)}" fill="#5a4a3a">${l1}</text>
        <text x="-14" y="${fin ? 96 : 92}" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fit(l2, 96)}" fill="#c8281e">${l2}</text>
        <path d="M-150,112q60,-8 120,0" stroke="#c8281e" stroke-width="4" fill="none" opacity=".5"/></g>
      <path d="M-270,-140Q-300,-140 -300,-100V120Q-300,160 -260,160H230Q300,160 300,100V-80Q300,-140 230,-140Z" fill="url(#iuGlass)"/>
      <path d="M-250,-110Q-50,-120 180,-116" stroke="#fff" stroke-width="12" opacity=".55" stroke-linecap="round"/><path d="M-250,130Q0,140 200,134" stroke="#fff" stroke-width="6" opacity=".3" stroke-linecap="round"/>
      <path d="M250,-100Q280,-40 270,80" stroke="#fff" stroke-width="7" opacity=".4" stroke-linecap="round"/>
      ${[[-180, 60], [-60, 100], [80, 40]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5" fill="#fff" opacity=".4"/>`).join("")}
      <path d="M-300,120Q-250,170 -170,166" stroke="#fff" stroke-width="4" opacity=".5" fill="none"/></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-all">${bg}${bottle}</g></g>`);
    FT(tl, `#${id}`, { opacity: 0 }, { opacity: 1 }, 0.25, "none", t0);
    FT(tl, `#${id}-all`, { scale: 1, svgOrigin: "540 1200" }, { scale: 1.05, svgOrigin: "540 1200" }, dur, "none", t0);
    // the bottle rolls in on a wash and settles; the wash runs up and back; the note is lit by the last light
    FT(tl, `#${id}-bt`, { x: 500, y: 60, rotation: 40, svgOrigin: "0 0" }, { x: 0, y: 0, rotation: 0, svgOrigin: "0 0" }, 0.9, "power3.out", t0 + 0.1);
    FT(tl, `#${id}-bt`, { rotation: 0, svgOrigin: "0 0" }, { rotation: -2, svgOrigin: "0 0" }, 0.6, "sine.inOut", t0 + 1.0, { repeat: Math.ceil(dur / 0.6), yoyo: true });
    FT(tl, `#${id}-wash`, { y: 0 }, { y: -70 }, 1.3, "sine.inOut", t0, { repeat: Math.ceil(dur / 1.3), yoyo: true });
    FT(tl, `#${id}-foam`, { y: 0, opacity: 0.85 }, { y: -70, opacity: 0.4 }, 1.3, "sine.inOut", t0, { repeat: Math.ceil(dur / 1.3), yoyo: true });
    for (let k = 0; k < 14; k++) FT(tl, `#${id}-gl${k}`, { opacity: 0.12 }, { opacity: 0.75 }, 0.3 + (k % 5) * 0.08, "sine.inOut", t0 + (k % 7) * 0.05, { repeat: Math.ceil(dur / 0.3), yoyo: true });
    return id;
  }

  // ---------------- the legend "ไฟเกาะผี" on the shadow screen ----------------
  const LEA = "#2a1408";
  const rod = (x, y, len = 300) => `<path d="M${x},${y}L${x + 6},${y + len}" stroke="#3a1e0e" stroke-width="7" stroke-linecap="round" opacity=".85"/>`;
  const weave = (d, pat = "iuLeafWeave", op = 0.88) => `<path d="${d}" fill="url(#${pat})" opacity="${op}"/><path d="${d}" fill="url(#iuWeave)" opacity=".5"/>`;
  function isletPuppet(id) {
    // a rock islet with a sand skirt and one leaning palm; three fire-rings on its top
    let s = `<path d="M-250,110Q-230,20 -150,-20Q-70,-70 20,-54Q110,-40 170,30Q220,80 240,110Z" fill="${LEA}"/>${weave("M-220,100Q-200,34 -130,-2Q-64,-50 20,-36Q100,-24 150,40Q190,78 210,100Z", "iuLeafWeaveD")}
      <path d="M-260,116Q0,96 250,116V150H-260Z" fill="${LEA}"/>${weave("M-250,122Q0,104 240,122V142H-250Z", "iuLeafWeaveD", 0.75)}
      <path d="M90,-30Q110,-120 80,-200" stroke="${LEA}" stroke-width="14" fill="none"/>`;
    [-160, -120, -70, -20, 30].forEach((a) => { const c = Math.cos(a * Math.PI / 180), sn = Math.sin(a * Math.PI / 180); s += `<path d="M80,-200q${f1(50 * c)},${f1(50 * sn - 16)} ${f1(100 * c)},${f1(100 * sn + 16)}" stroke="${LEA}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M80,-200q${f1(50 * c)},${f1(50 * sn - 16)} ${f1(100 * c)},${f1(100 * sn + 16)}" stroke="#8ac85a" stroke-width="6" fill="none" stroke-linecap="round" opacity=".85"/>`; });
    [[-120, -8], [-30, -30], [60, -4]].forEach(([x, y], k) => {
      s += `<g transform="translate(${x},${y})"><path d="M-30,0h60" stroke="${LEA}" stroke-width="10" stroke-linecap="round"/><g id="${id}-f${k}" opacity="0"><g id="${id}-fl${k}">
        <path d="M-22,0Q-30,-34 -10,-62Q-12,-36 2,-48Q8,-26 14,-44Q30,-20 16,0Z" fill="${LEA}"/><path d="M-14,0Q-20,-26 -6,-46Q-6,-26 4,-34Q10,-16 6,0Z" fill="#ffb23a" opacity=".92"/><path d="M-6,0Q-10,-14 -2,-26Q4,-12 2,0Z" fill="#fff2a0" opacity=".9"/></g></g></g>`;
    });
    return s;
  }
  function seaPuppet2() {
    let s = `<path d="M-320,40Q-280,-20 -230,10Q-190,-30 -140,6Q-96,-34 -50,4Q-10,-34 40,6Q84,-30 130,8Q174,-26 220,10Q260,-20 320,12L340,160H-330Z" fill="${LEA}"/>
      <path d="M-302,52Q-266,4 -230,30Q-190,-6 -140,28Q-98,-10 -50,26Q-10,-10 40,28Q80,-6 130,30Q170,-2 220,32Q256,4 300,30L318,148H-312Z" fill="#2a6a9a" opacity=".86"/>`;
    for (let row = 0; row < 3; row++) s += `<path d="M${-290 + row * 20},${74 + row * 26}${Array.from({ length: 12 }, () => " q12,-16 24,0 t24,0").join("")}" stroke="#bfe8f8" stroke-width="5" fill="none" opacity=".7"/>`;
    return s;
  }
  const boatPuppet = (id) => `<g><path d="M-120,0Q-134,-8 -150,-30L-134,-12L-152,4Q-120,14 -100,20H110Q130,14 150,4L134,-12L150,-30Q134,-8 120,0Z" fill="${LEA}"/>
    <path d="M-60,0Q-60,-52 0,-56Q60,-52 60,0Z" fill="${LEA}"/>${weave("M-48,-2Q-48,-42 0,-46Q48,-42 48,-2Z", "iuLeafWeaveD")}
    <path d="M70,0L100,-50" stroke="${LEA}" stroke-width="5"/><g id="${id}-lamp"><circle cx="100" cy="-56" r="12" fill="#fff6c0"/><circle cx="100" cy="-56" r="26" fill="#ffd27a" opacity=".3"/></g></g>`;
  const swimPuppet = (id) => `<g><circle cx="0" cy="-30" r="22" fill="${LEA}"/><circle cx="-2" cy="-30" r="12" fill="#c8844a" opacity=".85"/>
    <path d="M-30,-6Q0,-16 30,-6" stroke="${LEA}" stroke-width="16" stroke-linecap="round"/>
    <g id="${id}-armA"><path d="M-10,-14Q-40,-60 -70,-50" stroke="${LEA}" stroke-width="14" fill="none" stroke-linecap="round"/></g>
    <g id="${id}-armB"><path d="M10,-14Q50,-10 70,-30" stroke="${LEA}" stroke-width="14" fill="none" stroke-linecap="round"/></g>
    <path d="M-50,8q25,-10 50,0t50,0" stroke="#bfe8f8" stroke-width="6" fill="none" opacity=".8"/></g>`;
  function islLegend(L, o = {}) {
    const id = o.id || "ilg", R = mkR(o.seed || 29), CX = 540, top = 300, bot = 1460, W = 940, x0 = CX - W / 2, x1 = CX + W / 2;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#0a0604"/>`);
    put(L.far, `<rect x="-1300" y="1500" width="3700" height="1200" fill="#140c06"/>`);
    let s = `<path d="M${x0 - 120},${top - 200}H${x1 + 120}L${x1 + 60},${top - 90}H${x0 - 60}Z" fill="#2a1a0e" stroke="#120a04" stroke-width="5"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${x0 - 100 + k * 90},${top - 200}L${x0 - 60 + k * 90},${top - 92}" stroke="#4a301a" stroke-width="6"/>`).join("")}
      <rect x="${x0 - 60}" y="${top - 90}" width="${W + 120}" height="76" fill="url(#iuLeafWeaveD)" stroke="#5a3a12" stroke-width="4"/>
      ${Array.from({ length: 36 }, (_, k) => `<path d="M${x0 - 54 + k * 30},${top - 14}l6,${18 + (k % 3) * 5}" stroke="#c8a050" stroke-width="5" stroke-linecap="round"/>`).join("")}
      <rect x="${x0 - 40}" y="${top - 40}" width="${W + 80}" height="${bot - top + 80}" fill="url(#iuLeafWeave)" stroke="#2a3a14" stroke-width="5"/>
      <g id="${id}-scr"><rect x="${x0}" y="${top}" width="${W}" height="${bot - top}" fill="url(#tuScreen)"/></g>
      <g id="${id}-hot"><ellipse cx="${CX}" cy="${top + 520}" rx="300" ry="360" fill="url(#tuHot)"/></g>`;
    for (let k = 0; k < 8; k++) s += `<path d="M${x0 + 60 + k * 118 + (R() - 0.5) * 20},${top}Q${x0 + 66 + k * 118},${(top + bot) / 2} ${x0 + 54 + k * 118},${bot}" stroke="#a8743a" stroke-width="3" fill="none" opacity=".18"/>`;
    s += `<defs><clipPath id="${id}-clip"><rect x="${x0}" y="${top}" width="${W}" height="${bot - top}"/></clipPath></defs><g clip-path="url(#${id}-clip)" opacity=".94">
      <g transform="translate(${x0 + 150},${top + 170})"><g id="${id}-moon"><circle r="60" fill="#fff4d0" opacity=".9"/><circle cx="18" cy="-12" r="44" fill="url(#tuScreen)" opacity=".92"/></g></g>
      <g transform="translate(${CX + 150},${bot - 330})"><g id="${id}-sea">${seaPuppet2()}${rod(0, 160, 200)}</g></g>
      <g transform="translate(${x1 + 160},${bot - 348})"><g id="${id}-boat"><g transform="scale(.85)">${boatPuppet(id)}</g>${rod(0, 20, 300)}</g></g>
      <g transform="translate(${CX - 150},${bot - 290})"><g id="${id}-isle">${isletPuppet(id)}${rod(-40, 140, 260)}</g></g>
      <g transform="translate(${CX + 10},${bot - 200})"><g id="${id}-swim" opacity="0"><g transform="scale(.9)">${swimPuppet(id)}</g>${rod(0, 10, 260)}</g></g>
      ${[0, 1, 2].map((k) => `<g transform="translate(${CX + 80 + k * 30},${bot - 220})"><circle id="${id}-bub${k}" r="${10 - k * 2}" fill="#eaf8ff" stroke="${LEA}" stroke-width="5" opacity="0"/></g>`).join("")}</g>`;
    s += `<g transform="translate(${CX},${bot + 44})"><rect x="${-W / 2 - 60}" y="-34" width="${W + 120}" height="72" rx="36" fill="url(#tuBanana)" stroke="#2a3a14" stroke-width="5"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-W / 2 + k * (W / 8)},-32V36" stroke="#5a7a34" stroke-width="3" opacity=".5"/>`).join("")}
      <path d="M${-W / 2 - 40},-18H${W / 2 + 40}" stroke="#f4fadc" stroke-width="5" opacity=".55"/></g>`;
    if (o.title) { const bw = Math.max(170, cells(o.title) * 16 + 50), fs = cells(o.title) > 12 ? 42 : 56, ban = `M${-bw},-38H${bw}L${bw - 16},40Q0,56 ${-bw + 16},40Z`;
      s += `<g transform="translate(${CX},${top - 50})"><path d="${ban}" fill="#000" opacity=".3" transform="translate(6,8)"/><path d="${ban}" fill="#f2e2c0" stroke="#5a3a12" stroke-width="4"/>
        <path d="M${-bw + 20},-26H${bw - 20}" stroke="#c8a050" stroke-width="3" stroke-dasharray="8 6"/>
        <text y="20" text-anchor="middle" font-family="Sriracha" font-size="${fs}" fill="#1e3a5a">${o.title}</text></g>`; }
    put(L.set, s);
    let gl = `<ellipse cx="${CX}" cy="${top + 560}" rx="760" ry="860" fill="url(#tuSpill)" style="mix-blend-mode:screen"/>`;
    for (let k = 0; k < 6; k++) gl += `<g id="${id}-mo${k}" transform="translate(${f1(CX + (R() - 0.5) * 500)},${f1(top + 200 + R() * 500)})"><path d="M0,0q-8,-6 -12,2q6,4 12,-2q8,-6 12,2q-6,4 -12,-2" fill="#2a1a10" opacity=".55"/></g>`;
    put(L.glow, gl);
  }
  function legendAnim(tl, id, t0, dur, o = {}) {
    const [fa, fb] = o.fires || [0.4, 1.6], [ba, bb] = o.boat || [1.2, dur - 0.3], [sa, sb] = o.swim || [2.6, dur - 1.2], sink = o.sink ?? dur - 1.2;
    [["isle", 1.1, 0.5], ["sea", 0.7, 1.4], ["boat", 0.8, 1.2]].forEach(([n, per, a], k) => FT(tl, `#${id}-${n}`, { rotation: -a, svgOrigin: "0 140" }, { rotation: a, svgOrigin: "0 140" }, per, "sine.inOut", t0 + k * 0.1, { repeat: Math.ceil(dur / per), yoyo: true }));
    FT(tl, `#${id}-hot`, { opacity: 0.85, scale: 1, svgOrigin: "540 820" }, { opacity: 1, scale: 1.04, svgOrigin: "540 820" }, 0.13, "none", t0, { repeat: Math.ceil(dur / 0.13), yoyo: true });
    // the three fires light one by one and flicker
    [0, 1, 2].forEach((k) => { const tk = t0 + fa + (fb - fa) * k / 2; FT(tl, `#${id}-f${k}`, { opacity: 0, scaleY: 0.1, svgOrigin: "0 0" }, { opacity: 1, scaleY: 1, svgOrigin: "0 0" }, 0.4, "back.out(2)", tk); FT(tl, `#${id}-fl${k}`, { skewX: -8, scaleY: 0.92, svgOrigin: "0 0" }, { skewX: 8, scaleY: 1.08, svgOrigin: "0 0" }, 0.16 + k * 0.03, "sine.inOut", tk, { repeat: Math.ceil(dur / 0.16), yoyo: true }); });
    // the boat crosses far out, right to left, its lamp blinking
    FT(tl, `#${id}-boat`, { x: 0 }, { x: -1400 }, bb - ba, "none", t0 + ba);
    FT(tl, `#${id}-lamp`, { opacity: 1 }, { opacity: 0.3 }, 0.5, "sine.inOut", t0, { repeat: Math.ceil(dur / 0.5), yoyo: true });
    // the swimmer leaves the islet toward the boat, arms alternating, then sinks: three bubbles rise
    tl.set(`#${id}-swim`, { opacity: 1 }, t0 + sa);
    FT(tl, `#${id}-swim`, { x: 0 }, { x: 320 }, sb - sa, "power1.in", t0 + sa);
    FT(tl, `#${id}-armA`, { rotation: -30, svgOrigin: "-10 -14" }, { rotation: 40, svgOrigin: "-10 -14" }, 0.4, "sine.inOut", t0 + sa, { repeat: Math.ceil((sb - sa) / 0.4), yoyo: true });
    FT(tl, `#${id}-armB`, { rotation: 30, svgOrigin: "10 -14" }, { rotation: -40, svgOrigin: "10 -14" }, 0.4, "sine.inOut", t0 + sa, { repeat: Math.ceil((sb - sa) / 0.4), yoyo: true });
    FT(tl, `#${id}-swim`, { y: 0 }, { y: 90, opacity: 0 }, 0.8, "power2.in", t0 + sink);
    [0, 1, 2].forEach((k) => FT(tl, `#${id}-bub${k}`, { opacity: 0, y: 0 }, { opacity: 1, y: -70 - k * 20 }, 0.9, "power1.out", t0 + sink + 0.5 + k * 0.25, { repeat: 1 }));
    for (let k = 0; k < 6; k++) FT(tl, `#${id}-mo${k}`, { rotation: 0, svgOrigin: "540 820" }, { rotation: k % 2 ? -360 : 360, svgOrigin: "540 820" }, 3 + k * 0.6, "none", t0, { repeat: Math.ceil(dur / 3) });
  }

  window.IslUI = { rule, hud, fork, choice, dark, rewind, chip, source, symptom, endCard, legendAnim, ICON, icon, iconPop, iconLife, RULES };
  Object.assign(Sets, { islLegend });
})();
