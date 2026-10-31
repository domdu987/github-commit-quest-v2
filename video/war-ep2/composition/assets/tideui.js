// "ทะเลลด" on-screen graphics (screen space: put them in L.light unless noted). The beach world's own materials: driftwood painted
// with boat paint, rope, fishing floats, a lifebuoy, sea foam. Same 2.5D rules as ตึกโยก (V10): slabs with a darker body under a lit
// face, one shade + one highlight, soft shadows under what floats; entries squash & stretch with back/elastic overshoot, staggered,
// then a secondary motion keeps running until the shot ends; exits lift and fade.
//   TideUI.rule(tl, layer, t0, dur, o)     ยาย's driftwood board on two ropes: 3 painted rhyming rules, each with a fishing-float coin.
//                                          o.active (0..2) is brushed on (paint write-on, yellow brush swipe, rhyme syllables pulse,
//                                          its coin pops and moves), o.done [i…] get a painted green tick, the rest are bleached and faint
//                                          · o.y (board top, default 300) · o.at [s…] when each row lands · o.out (s after t0) to lift away
//   TideUI.live(tl, layer, t0, dur, o)     จูน's livestream over the shot (the shot behind is her phone's view): avatar ring + name,
//                                          LIVE badge, viewers counting o.viewers [from, to], the side buttons, hearts rising, comments
//                                          o.comments [[t, name, text]…] sliding in and pushing the older ones up · o.name, o.title, o.out
//                                          · o.cy the bottom row's y (1500; 1310 keeps the whole stack above the caption band)
//                                          · o.typing [[t, name, until?]…] a "name กำลังพิมพ์ •••" row joins the stack; it stops at `until`,
//                                          at that name's next comment or pin, else 2.5 s on (stopping with no comment = they went quiet)
//                                          · o.pin [t, name, text] the pinned comment: pops in bigger than it stays (flash, a ring bursts
//                                          off it), gold rim, breathing glow, a "ปักหมุด" chip; sits above the stack (which keeps 3 rows), stays
//                                          · o.likes [from, to] the heart counter climbs (default a fixed 12.4K)
//                                          · a comment, typing row or pin with t < 0 was already there: it stands in place from t0 with no
//                                          entry (the live seen again after a cutaway keeps ยายพร❤️'s pin and the last comments)
//                                          · o.end t (s after t0): the stream cuts — a glitch tear, the picture and the UI dim, LIVE turns
//                                          grey, counts and hearts stop, no comments after it, a "ไลฟ์สิ้นสุดแล้ว · สัญญาณขาดหาย" panel with
//                                          a lost-signal icon (bars searching, a red X) floats at o.endY (820). Keep the set still after it
//                                          (no camera drift, nothing moving) so the picture reads frozen.
//   TideUI.choice(tl, layer, t0, dur, o)   the choice on driftwood boards: o.q, o.a / o.b { text, icon } (icon: a coin name or raw SVG),
//                                          a lifebuoy countdown (o.secs); the frame hovers (o.hover [[t, k]…]); o.pull "a" | "b": at o.at
//                                          a wave surges up the screen and drags the frame onto that card, then drains, leaving it wet ·
//                                          o.out
//   TideUI.endCard(tl, layer, t0, dur, o)  the blue tsunami evacuation sign on its pole at dusk, a paper note taped below it flapping in
//                                          the wind: o.l1 "ตอนที่ 2", o.l2 "คลื่นแรกไป" · o.final → "ตอนจบ" · o.tag true | "text": a red
//                                          sticker ("ตอนจบ") stamped on the note's top corner at o.tagAt (1.0 s), then pulsing — announces
//                                          the next episode as the finale while l1/l2 stay short ("ตอนที่ 3" / "หนีไม่ทัน")
//   TideUI.series(tl, layer, t0, dur, o)   the waves come as a series, painted in a rope-framed window on a driftwood board hung on two
//                                          ropes (x 40–1040, y o.y 230 … ~1434, above the caption band), its title painted above the window
//     o.phase "train"    a cross-section, deep sea → coast (hotel, palms, hill): three crests — turbulent bores, not surf curls —
//                        roll in one after another, the one nearest the coast first, each bigger; at o.at[3] brackets with spinning
//                        clocks open between them under one label o.gap ("ห่างกัน <u>5 นาที – 2 ชั่วโมง</u>", <u> = red).
//                        o.at [c0, c1, c2, gaps] (0.3, 0.9, 1.5, 2.2) · title "สึนามิไม่ได้มาลูกเดียว"
//     o.phase "heights"  one fixed scale (ruler 0–15 ม., 50 px a metre): a person (1.7 m), a one-storey house, the 5-storey hotel
//                        (3 m a storey, "ชั้น 1…5" badges kept above the water). Each crest comes in from the sea side (left) as a
//                        muddy bore, its foaming front racing across, holds, then drains before the next, leaving a dashed mark and
//                        its tag o.tags[k] ("09:38 · 2–3 ม.", "09:43 · 6–7 ม.", "10:03 · เกิน 10 ม.") at o.h[k] metres (2.5, 6.5,
//                        11: the third tops the 3rd floor and stays). o.at [w0, w1, w2] when each front comes in (0.6, 2.4, 4.2);
//                        its mark and tag land 0.6 s later · title "ปี 2547 · ชายหาดแห่งหนึ่ง"
//                        both: o.title, o.y (board top), o.out (s after t0: lifts away and fades)
//   TideUI.pa(tl, layer, t0, dur, o)       the warning tower's loudspeaker announcement on a note slab with a crawling yellow/black
//                                          hazard band and a "หอเตือนภัย" tab: the horn cluster shudders, sound rings pulse out; o.l1
//                                          ("โปรดทราบ โปรดทราบ…") is written on with the voice, o.l2 ("ขณะนี้เกิดคลื่นสึนามิ", red) slams
//                                          in, gets underlined and shakes. o.at [panel, l1, l2] (0, 0.35, 1.4) · o.y (centre, 470) · o.out
//   TideUI.source(tl, layer, t0, dur, o)   the source chip (a foam-white slab with a wave badge): o.text, o.y (default 1790)
//   TideUI.ICON.<name>() / TideUI.icon(name, x, y, s, id) / TideUI.iconPop(tl, root, t) / TideUI.iconLife(tl, root, t, dur)
//                                          the rule coins (120-unit box): recede (the sea draws back, a runner goes up the hill),
//                                          waves (a small wave, a big one rising behind it), floor (a strong 6-storey building, water
//                                          rising at its foot, a figure on the roof, an arrow up) · TideUI.RULES the rule lines
//                                          (<u>…</u> = rhyme syllables)
//   Sets.tideLegend(L, o) + TideUI.legendAnim(tl, id, t0, dur, o)
//                                          the Moken legend ละบูน (คลื่นยักษ์เจ็ดชั้น) on the channel's shadow screen: a thatched eave,
//                                          a pandanus-weave valance with a fringe, a sea-scallop border, the cloth screen hot-lit
//                                          (#id-hot), the banana trunk the rods stand in; puppets cut as woven-pandanus shapes:
//                                          #id-hill, #id-hut, #id-sand (stranded fish #id-fishA/B), #id-sea, #id-boat (the kabang
//                                          houseboat; #id-boatIn is left tilted on the sand, then tossed by the wave),
//                                          #id-elder (#id-arm points with the paddle), #id-v0 #id-v1 (children), #id-v2 (a grandmother
//                                          with a child), #id-wave (seven stacked crests #id-wc0..6). o.id, o.title (optional banner)
//                                          legendAnim o: recede [a, b], point [a, b], run [a, b], wave (a), elderGo (false keeps the
//                                          elder in place) — seconds after t0
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  let seq = 0;
  const nid = () => `tu${++seq}`;
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mkR = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const hex = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  const tone = (h, k) => { const c = hex(h), t = k >= 0 ? 255 : 0, a = Math.abs(k); return "#" + c.map((v) => Math.round(v + (t - v) * a).toString(16).padStart(2, "0")).join(""); };
  const wobble = (n = 4) => (p) => Math.sin(p * Math.PI * 2 * n) * (1 - p);
  const plain = (s) => s.replace(/<[^>]+>/g, "");
  // text width in em of Kanit 900 (calibrated on the real fonts: Thai marks take no width; Kanit 700 ≈ 0.97, Sriracha ≈ 0.95)
  const emW = (t) => { let w = 0; for (const c of plain(t)) {
    if (/[\u0E31\u0E34-\u0E3A\u0E47-\u0E4E\uFE0F]/.test(c)) continue;
    w += c === " " ? 0.2 : /[0-9]/.test(c) ? 0.56 : /[.:·,]/.test(c) ? 0.22 : c === "–" ? 0.54 : c === "…" ? 0.75 : /[“”]/.test(c) ? 0.38
      : c === "เ" ? 0.36 : /[โใไ]/.test(c) ? 0.42 : c === "แ" ? 0.62 : c === "ะ" ? 0.44 : c === "า" ? 0.55 : /[\u0E00-\u0E7F]/.test(c) ? 0.64 : c.codePointAt(0) > 0x2000 ? 1 : 0.58; }
    return w; };

  // coin palettes: face, face highlight, rim, rim shade
  const PAL = {
    recede: ["#c4efe8", "#f4fffc", "#2a9ca6", "#1a6a74"],
    waves: ["#d2e6fb", "#f6fbff", "#3a6cc8", "#22468a"],
    floor: ["#fde0bc", "#fff7ee", "#e8823a", "#b4561a"],
    far: ["#dff2cf", "#fbfff4", "#5aa83a", "#2e6a1a"],
    foot: ["#f8dcd8", "#fff6f4", "#d8453a", "#8a1e18"],
  };
  let coinDefs = "";
  for (const [n, [b, l, r, rd]] of Object.entries(PAL)) coinDefs += `<radialGradient id="tuF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${l}"/><stop offset=".5" stop-color="${b}"/><stop offset="1" stop-color="${tone(b, -0.2)}"/></radialGradient>
    <linearGradient id="tuR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset=".55" stop-color="${tone(r, -0.12)}"/><stop offset="1" stop-color="${rd}"/></linearGradient>`;

  Sets.DEFS += `${coinDefs}
    <radialGradient id="tuCoinSh"><stop offset="0" stop-color="#000" stop-opacity=".42"/><stop offset=".6" stop-color="#000" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="tuSoftSh"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset=".55" stop-color="#000" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <linearGradient id="tuBev" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/><stop offset=".58" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
    <clipPath id="tuPicClip" clipPathUnits="userSpaceOnUse"><circle cx="60" cy="60" r="51"/></clipPath>
    <linearGradient id="tuSeaG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3ec2d0"/><stop offset="1" stop-color="#1a7a9c"/></linearGradient>
    <linearGradient id="tuDeepG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a7ad8"/><stop offset=".6" stop-color="#1e4ea0"/><stop offset="1" stop-color="#142e6a"/></linearGradient>
    <linearGradient id="tuHillG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ad072"/><stop offset="1" stop-color="#3e8a44"/></linearGradient>
    <linearGradient id="tuSandG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8e2a8"/><stop offset="1" stop-color="#e2bc78"/></linearGradient>
    <linearGradient id="tuWallG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f4f0e8"/><stop offset=".6" stop-color="#e2dcd0"/><stop offset="1" stop-color="#c2baae"/></linearGradient>
    <linearGradient id="tuOrA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb070"/><stop offset="1" stop-color="#e2641a"/></linearGradient>
    <radialGradient id="tuHead" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6a5a4c"/><stop offset="1" stop-color="#241a14"/></radialGradient>
    <linearGradient id="tuGrn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#52c87a"/><stop offset="1" stop-color="#1f8246"/></linearGradient>
    <linearGradient id="tuWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2d2b2"/><stop offset=".45" stop-color="#cfb994"/><stop offset="1" stop-color="#b49a74"/></linearGradient>
    <linearGradient id="tuWoodL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2e4c6"/><stop offset=".5" stop-color="#e2cca4"/><stop offset="1" stop-color="#c8ac82"/></linearGradient>
    <linearGradient id="tuWoodSide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6e4c"/><stop offset="1" stop-color="#5a4430"/></linearGradient>
    <linearGradient id="tuRope" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a7a4a"/><stop offset=".4" stop-color="#d8bc84"/><stop offset="1" stop-color="#8a6a3a"/></linearGradient>
    <linearGradient id="tuBrush" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffe14a" stop-opacity=".85"/><stop offset=".85" stop-color="#ffd23a" stop-opacity=".75"/><stop offset="1" stop-color="#ffd23a" stop-opacity=".3"/></linearGradient>
    <radialGradient id="tuFloatO" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffd2a0"/><stop offset=".45" stop-color="#f88a34"/><stop offset="1" stop-color="#c25810"/></radialGradient>
    <radialGradient id="tuFloatW" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#eef2f4"/><stop offset="1" stop-color="#b8c4cc"/></radialGradient>
    <linearGradient id="tuLiveR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a6a"/><stop offset="1" stop-color="#d8243a"/></linearGradient>
    <linearGradient id="tuStory" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd23a"/><stop offset=".5" stop-color="#ff5a8a"/><stop offset="1" stop-color="#8a4aff"/></linearGradient>
    <linearGradient id="tuWaveWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5ad2e0" stop-opacity=".95"/><stop offset=".25" stop-color="#1e8ab0" stop-opacity=".95"/><stop offset="1" stop-color="#0a3a5a" stop-opacity=".97"/></linearGradient>
    <linearGradient id="tuSignB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f74d8"/><stop offset=".55" stop-color="#1e5ab8"/><stop offset="1" stop-color="#143e86"/></linearGradient>
    <linearGradient id="tuPole" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a747c"/><stop offset=".3" stop-color="#d8e0e6"/><stop offset=".55" stop-color="#9aa4ac"/><stop offset="1" stop-color="#4a545c"/></linearGradient>
    <linearGradient id="tuDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1a3a"/><stop offset=".38" stop-color="#5a3a6a"/><stop offset=".62" stop-color="#d8705a"/><stop offset=".72" stop-color="#ffb46a"/><stop offset="1" stop-color="#ffd890"/></linearGradient>
    <linearGradient id="tuDuskSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a4a5e"/><stop offset=".3" stop-color="#2e3a5e"/><stop offset="1" stop-color="#0e1a2e"/></linearGradient>
    <linearGradient id="tuNote" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbef"/><stop offset="1" stop-color="#ecdcb8"/></linearGradient>
    <linearGradient id="tuChip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbfffe"/><stop offset="1" stop-color="#dcefee"/></linearGradient>
    <radialGradient id="tuBuoy" cx=".5" cy=".5" r=".5"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset=".72" stop-color="#fff" stop-opacity=".35"/><stop offset=".9" stop-color="#000" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="tuScreen" cx=".5" cy=".42" r=".62"><stop offset="0" stop-color="#fffbe8"/><stop offset=".3" stop-color="#ffeec0"/><stop offset=".7" stop-color="#e8b878"/><stop offset="1" stop-color="#9a6434"/></radialGradient>
    <radialGradient id="tuHot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".25" stop-color="#fff6d0" stop-opacity=".6"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
    <radialGradient id="tuSpill" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".4"/><stop offset="1" stop-color="#ffcf7a" stop-opacity="0"/></radialGradient>
    <linearGradient id="tuBanana" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f2c8"/><stop offset=".4" stop-color="#b8d488"/><stop offset="1" stop-color="#6a8a44"/></linearGradient>
    <pattern id="tuBorder" width="64" height="64" patternUnits="userSpaceOnUse"><rect width="64" height="64" fill="#145a66"/><path d="M0,22q16,-18 32,0t32,0M0,46q16,-18 32,0t32,0" stroke="#f2d48a" stroke-width="5" fill="none"/>
      <path d="M0,34q16,-18 32,0t32,0" stroke="#5ac2c8" stroke-width="3" fill="none" opacity=".7"/><circle cx="16" cy="8" r="3" fill="#f2d48a"/><circle cx="48" cy="58" r="3" fill="#f2d48a"/><path d="M0,2H64M0,62H64" stroke="#0a3a44" stroke-width="4"/></pattern>
    <pattern id="tuValance" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#c8a050"/><path d="M0,20L20,0L40,20L20,40Z" fill="#a87a30"/><path d="M0,0L40,40M40,0L0,40" stroke="#e8c87a" stroke-width="5" opacity=".8"/><path d="M20,0V40M0,20H40" stroke="#7a5418" stroke-width="2" opacity=".5"/></pattern>
    <pattern id="tuWeave" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M9,2L16,9L9,16L2,9Z" fill="#fff4d0" opacity=".5"/></pattern>`;

  // ---------------- the rule coins ----------------
  const PICT = {
    // ทะเลถอย อย่าคอยดู: the sea draws back off the sand (a fish left flapping), a runner goes up the hill, the arrow says up
    recede: () => [`<path d="M-6,124V64Q12,36 34,42Q52,48 58,78L62,124Z" fill="url(#tuHillG)" ${OUT(3)}/><path d="M6,58Q18,44 30,46" stroke="#c8f0b0" stroke-width="3" fill="none" opacity=".8" stroke-linecap="round"/>
      <path d="M10,52l-4,-12M20,46l-1,-14" stroke="#2a6a30" stroke-width="3" stroke-linecap="round"/><circle cx="6" cy="38" r="6" fill="#3e8a44"/><circle cx="19" cy="30" r="7" fill="#4e9a50"/>
      <path d="M40,124V90Q72,80 130,86V124Z" fill="url(#tuSandG)" ${OUT(3)}/><path d="M56,100Q80,94 104,100" stroke="#c89a5a" stroke-width="2.4" fill="none" opacity=".6"/>
      <g class="tuSea"><path d="M84,92Q96,84 108,92T132,90V130H84Z" fill="url(#tuSeaG)" ${OUT(3)}/><path d="M84,92Q96,84 108,92T132,90" stroke="#e8fbff" stroke-width="4" fill="none" stroke-linecap="round"/>
        <path d="M92,106h14M110,114h12" stroke="#bff2ff" stroke-width="2.4" opacity=".7" stroke-linecap="round"/></g>
      <g transform="translate(70,96)"><g class="tuFish"><path d="M-8,0Q0,-7 8,0Q0,7 -8,0Z" fill="#8ab4d0" stroke="${INK}" stroke-width="2"/><path d="M8,0l6,-5v10z" fill="#8ab4d0" stroke="${INK}" stroke-width="2"/><circle cx="-4" cy="-1" r="1.3" fill="${INK}"/></g></g>`,
    `<g class="tuRun"><g transform="translate(44,58)"><path d="M0,-12L-4,4" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M0,-12L-4,4" stroke="#ff8a3a" stroke-width="4.5" stroke-linecap="round"/>
        <path d="M-4,4L2,14M-4,4L-12,10M-1,-8L8,-4M-1,-8L-10,-6" stroke="${INK}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="1" cy="-19" r="5.4" fill="url(#tuHead)" stroke="${INK}" stroke-width="2"/></g></g>
      <g class="tuUp"><path d="M18,30L30,12L42,30H35V44H25V30Z" fill="#0e4a2a" transform="translate(2,3)"/><path d="M18,30L30,12L42,30H35V44H25V30Z" fill="url(#tuGrn)" ${OUT(2.6)}/><path d="M29,16V38" stroke="#c8f5d8" stroke-width="2.4" opacity=".8" stroke-linecap="round"/></g>`],
    // คลื่นแรกไป คลื่นใหญ่ตาม: a small wave runs ahead, the big one rises behind it
    waves: () => [`<g class="tuBig"><path d="M34,124Q38,74 70,48Q96,30 112,40Q118,44 116,50Q104,44 94,56Q110,54 120,66L126,124Z" fill="url(#tuDeepG)" ${OUT(3)}/>
        <path d="M70,48Q96,30 112,40Q118,44 116,50Q104,44 94,56Q88,62 92,72Q80,62 82,52Z" fill="#eaf8ff" ${OUT(2.4)}/><path d="M60,70Q56,92 60,116M84,78Q80,98 84,118" stroke="#6aa2f0" stroke-width="3" fill="none" opacity=".6"/></g>
      <g class="tuSmall"><path d="M-6,124Q4,100 22,94Q36,90 44,98Q34,98 32,106Q42,106 48,116L50,124Z" fill="url(#tuSeaG)" ${OUT(3)}/><path d="M22,94Q36,90 44,98Q34,98 32,106" stroke="#effcff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
      <path d="M-6,118Q40,112 130,118V130H-6Z" fill="url(#tuSandG)" ${OUT(2.6)}/>`,
    `<g transform="translate(26,82)"><circle r="10" fill="#fff" ${OUT(2.4)}/><text y="5" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="15" fill="${INK}">1</text></g>
      <g transform="translate(96,24)"><circle r="12" fill="#e2392c" ${OUT(2.6)}/><text y="6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="17" fill="#fff">2</text></g>`],
    // หนีไม่ทัน ขึ้นชั้นสูง: water rising round a strong 6-storey concrete building, a figure waving from the roof, the arrow up
    floor: () => [`<rect x="34" y="22" width="48" height="108" fill="url(#tuWallG)" ${OUT(3)}/><path d="M30,22H86V15H30Z" fill="#c2baae" ${OUT(2.4)}/>
      <path d="M82,22L92,16V124L82,130Z" fill="#a8a094" ${OUT(2.2)}/>
      ${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M34,${40 + k * 17}H82" stroke="${INK}" stroke-width="${k < 5 ? 2 : 0}"/>${[40, 56, 70].map((x) => `<rect x="${x}" y="${26 + k * 17}" width="7" height="9" fill="#7ab4e0" stroke="${INK}" stroke-width="1.4"/>`).join("")}`).join("")}
      <path d="M36,22V130M80,22V130" stroke="#8a8276" stroke-width="3" opacity=".55"/>
      <g class="tuWater"><path d="M-6,102Q10,96 26,102T58,102T90,102T126,100V136H-6Z" fill="url(#tuSeaG)" ${OUT(2.8)} opacity=".95"/><path d="M-6,102Q10,96 26,102T58,102T90,102T126,100" stroke="#e8fbff" stroke-width="3.4" fill="none" stroke-linecap="round"/></g>`,
    `<g transform="translate(58,12)"><circle cx="0" cy="-8" r="5" fill="url(#tuHead)" stroke="${INK}" stroke-width="2"/><path d="M0,-4V5" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><path d="M0,-4V5" stroke="#ff8a3a" stroke-width="4" stroke-linecap="round"/>
        <g class="tuWave"><path d="M0,-2L9,-12" stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/></g><path d="M0,-2L-8,4" stroke="${INK}" stroke-width="3.4" stroke-linecap="round"/></g>
      <g class="tuArr2"><path d="M98,56L110,38L122,56H115V80H105V56Z" fill="#7a2e08" transform="translate(2,3)"/><path d="M98,56L110,38L122,56H115V80H105V56Z" fill="url(#tuOrA)" ${OUT(2.6)}/><path d="M109,42V74" stroke="#ffe0c0" stroke-width="2.4" opacity=".8" stroke-linecap="round"/></g>`],
  };
  // ที่ราบ ห่างฝั่ง 3 กม.: the sea at the left edge, a runner heading inland along a dashed arrow, the distance tag
  PICT.far = () => [`<path d="M-6,124Q4,96 18,92Q30,90 34,100L38,130H-6Z" fill="url(#tuSeaG)" ${OUT(3)}/><path d="M18,92Q30,90 34,100" stroke="#effcff" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M30,118Q70,112 130,116V130H30Z" fill="url(#tuSandG)" ${OUT(2.6)}/>
      <path d="M44,96H100" stroke="${INK}" stroke-width="9" stroke-linecap="round"/><path d="M44,96H100" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="7 6"/>
      <path d="M96,84L114,96L96,108Z" fill="url(#tuGrn)" ${OUT(2.6)}/><g class="tuRun"><g transform="translate(70,78)"><path d="M0,-12L-4,4" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M0,-12L-4,4" stroke="#ff8a3a" stroke-width="4.5" stroke-linecap="round"/><path d="M-4,4L2,14M-4,4L-12,10M-1,-8L8,-4M-1,-8L-10,-6" stroke="${INK}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="1" cy="-19" r="5.4" fill="url(#tuHead)" stroke="${INK}" stroke-width="2"/></g></g>`,
    `<g transform="translate(64,30)"><rect x="-30" y="-15" width="60" height="28" rx="10" fill="#fff" ${OUT(2.4)}/><text y="6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="17" fill="${INK}">3 กม.</text></g>`];
  // หนีด้วยเท้า ไม่ใช่รถ: a runner with a green tick, a car crossed out in red
  PICT.foot = () => [`<path d="M-6,118Q40,112 130,118V130H-6Z" fill="url(#tuSandG)" ${OUT(2.6)}/>
      <g transform="translate(78,106)"><path d="M-34,0V-14Q-32,-24 -20,-26L-11,-38H16L27,-26Q36,-24 36,-12V0Z" fill="#c3c9cf" ${OUT(2.4)}/><path d="M-7,-35H13L21,-26H-14Z" fill="#3f4e5e" ${OUT(1.6)}/>
        <circle cx="-18" cy="2" r="8" fill="#15181c" ${OUT(2)}/><circle cx="20" cy="2" r="8" fill="#15181c" ${OUT(2)}/></g>
      <g class="tuRun"><g transform="translate(30,62)"><path d="M0,-12L-4,4" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M0,-12L-4,4" stroke="#ff8a3a" stroke-width="4.5" stroke-linecap="round"/><path d="M-4,4L2,14M-4,4L-12,10M-1,-8L8,-4M-1,-8L-10,-6" stroke="${INK}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="1" cy="-19" r="5.4" fill="url(#tuHead)" stroke="${INK}" stroke-width="2"/></g></g>`,
    `<path d="M52,74L104,124M104,74L52,124" stroke="#fff" stroke-width="15" stroke-linecap="round"/><path d="M52,74L104,124M104,74L52,124" stroke="#e2392c" stroke-width="9" stroke-linecap="round"/>
      <path d="M16,26l9,10l18,-22" stroke="#fff" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M16,26l9,10l18,-22" stroke="#1e9a50" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`];
  const coin = (name) => {
    const [inside, top] = PICT[name]();
    return `<ellipse class="tuSh" cx="60" cy="120" rx="50" ry="9" fill="url(#tuCoinSh)"/>
      <g class="tuBob"><g class="tuSq">
        <circle cx="60" cy="66" r="52" fill="url(#tuR-${name})" ${OUT(4)}/><path d="M12,66A48,48 0 0 0 108,66" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
        <circle cx="60" cy="57" r="52" fill="url(#tuF-${name})" ${OUT(4)}/>
        <circle cx="60" cy="57" r="45.5" fill="none" stroke="url(#tuBev)" stroke-width="4"/>
        <g transform="translate(60,57) scale(.9) translate(-60,-60)"><g clip-path="url(#tuPicClip)">${inside}</g>${top}</g>
        <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle cx="53.5" cy="15.5" r="2.8" fill="#fff" opacity=".7"/>
      </g></g>`;
  };
  const ICON = Object.fromEntries(Object.keys(PICT).map((n) => [n, () => coin(n)]));
  const icon = (name, x, y, s = 1, id = "") => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>${ICON[name]()}</g></g>`;
  function iconPop(tl, root, t) {
    if (!root) return;
    root.querySelectorAll(".tuSq").forEach((e) => tl.fromTo(e, { scaleX: 0.3, scaleY: 1.5, svgOrigin: "60 117" }, { scaleX: 1, scaleY: 1, svgOrigin: "60 117", duration: 0.75, ease: "elastic.out(1, 0.42)", immediateRender: false }, t));
  }
  function iconLife(tl, root, t, dur) {
    if (!root || dur <= 0) return;
    const q = (s) => root.querySelectorAll(s), R = (p) => Math.ceil(dur / p) + 1;
    q(".tuBob").forEach((e) => tl.fromTo(e, { y: 0 }, { y: -5, duration: 0.85, repeat: R(0.85), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".tuSh").forEach((e) => tl.fromTo(e, { scaleX: 1, opacity: 1, svgOrigin: "60 120" }, { scaleX: 0.8, opacity: 0.55, svgOrigin: "60 120", duration: 0.85, repeat: R(0.85), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    // the sea slides out and back, the stranded fish flaps, the runner climbs, the arrow nudges up
    q(".tuSea").forEach((e) => tl.fromTo(e, { x: -16 }, { x: 18, duration: 1.1, repeat: R(1.1), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".tuFish").forEach((e) => tl.fromTo(e, { rotation: -22, svgOrigin: "0 0" }, { rotation: 22, svgOrigin: "0 0", duration: 0.16, repeat: R(0.16), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".tuRun").forEach((e) => tl.fromTo(e, { x: 10, y: 10 }, { x: -6, y: -8, duration: 0.9, repeat: R(0.9), ease: "none", immediateRender: false }, t));
    q(".tuUp").forEach((e) => tl.fromTo(e, { y: 4 }, { y: -6, duration: 0.32, repeat: R(0.32), yoyo: true, ease: "power2.out", immediateRender: false }, t));
    // the big wave rises, overshoots and settles, again and again; the small one runs ahead
    q(".tuBig").forEach((e) => tl.fromTo(e, { scaleY: 0.55, svgOrigin: "80 124" }, { scaleY: 1.06, svgOrigin: "80 124", duration: 0.9, repeat: R(0.9), yoyo: true, ease: "back.out(2)", immediateRender: false }, t));
    q(".tuSmall").forEach((e) => tl.fromTo(e, { x: 4 }, { x: -10, duration: 0.9, repeat: R(0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    // the water rises up the building, the figure waves, the arrow bounces up
    q(".tuWater").forEach((e) => tl.fromTo(e, { y: 16 }, { y: -6, duration: 1.2, repeat: R(1.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".tuWave").forEach((e) => tl.fromTo(e, { rotation: -20, svgOrigin: "0 -2" }, { rotation: 26, svgOrigin: "0 -2", duration: 0.22, repeat: R(0.22), yoyo: true, ease: "sine.inOut", immediateRender: false }, t));
    q(".tuArr2").forEach((e) => tl.fromTo(e, { y: 4 }, { y: -8, duration: 0.34, repeat: R(0.34), yoyo: true, ease: "power2.out", immediateRender: false }, t));
  }

  // ---------------- shared pieces ----------------
  const slab = (x, y, w, h, r, o = {}) => `<rect x="${x}" y="${y + (o.d ?? 10)}" width="${w}" height="${h}" rx="${r}" fill="${o.body || "#3a2a1a"}" stroke="${o.bodyStroke || INK}" stroke-width="${o.sw ?? 4}"/>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${o.face || "url(#tuWoodL)"}" stroke="${o.stroke || INK}" stroke-width="${o.sw ?? 4}"/>
    ${o.gloss === false ? "" : `<rect x="${x + r * 0.5}" y="${y + 5}" width="${w - r}" height="${Math.min(h * 0.4, 50)}" rx="${Math.min(r, h * 0.2)}" fill="#fff" opacity=".14"/>`}`;
  // driftwood grain, knots, nail holes and salt stains inside a box (seeded)
  function grain(x, y, w, h, seed, o = {}) {
    const r = mkR(seed);
    let s = "";
    for (let k = 0; k < (o.lines ?? Math.round(h / 22)); k++) {
      const yy = y + 12 + (k + r() * 0.6) * (h - 24) / (o.lines ?? Math.round(h / 22)), a = 6 + r() * 10, ph = r() * 6;
      let d = `M${x + 10},${f1(yy)}`;
      for (let xx = x + 10; xx <= x + w - 10; xx += 40) d += ` L${xx},${f1(yy + a * Math.sin(xx / 90 + ph) * 0.4)}`;
      s += `<path d="${d}" stroke="${o.c || "#8a7052"}" stroke-width="${f1(1.4 + r() * 1.6)}" fill="none" opacity="${f1(0.18 + r() * 0.2)}"/>`;
    }
    for (let k = 0; k < (o.knots ?? 2); k++) { const kx = x + 60 + r() * (w - 120), ky = y + 30 + r() * (h - 60);
      s += `<ellipse cx="${f1(kx)}" cy="${f1(ky)}" rx="16" ry="7" fill="#8a6a46" opacity=".5"/><ellipse cx="${f1(kx)}" cy="${f1(ky)}" rx="26" ry="12" fill="none" stroke="#8a6a46" stroke-width="2" opacity=".35"/><ellipse cx="${f1(kx)}" cy="${f1(ky)}" rx="36" ry="16" fill="none" stroke="#8a6a46" stroke-width="1.6" opacity=".22"/>`; }
    for (let k = 0; k < (o.stains ?? 3); k++) s += `<ellipse cx="${f1(x + r() * w)}" cy="${f1(y + r() * h)}" rx="${f1(30 + r() * 50)}" ry="${f1(10 + r() * 16)}" fill="#fffaf0" opacity="${f1(0.08 + r() * 0.1)}"/>`;
    return s;
  }
  // a hanging rope from (x, y0) down to (x, y1): twisted, with its shadow
  const rope = (x, y0, y1) => `<path d="M${x + 5},${y0}V${y1}" stroke="#000" stroke-width="12" opacity=".2"/><path d="M${x},${y0}V${y1}" stroke="${INK}" stroke-width="15"/><path d="M${x},${y0}V${y1}" stroke="url(#tuRope)" stroke-width="10"/>
    <path d="${Array.from({ length: Math.ceil((y1 - y0) / 14) }, (_, k) => `M${x - 5},${y0 + k * 14}L${x + 5},${y0 + k * 14 + 9}`).join("")}" stroke="#7a5a2a" stroke-width="2.6" opacity=".7"/>`;
  // a fishing float (A/B badge)
  const float = (x, y, r, letter, c = "O") => `<ellipse cx="${x + 4}" cy="${y + r + 6}" rx="${r}" ry="${r * 0.28}" fill="url(#tuSoftSh)" opacity=".6"/>
    <circle cx="${x}" cy="${y}" r="${r}" fill="url(#tuFloat${c})" ${OUT(3.4)}/><path d="M${x - r},${y}A${r},${r * 0.35} 0 0 0 ${x + r},${y}" stroke="${c === "O" ? "#a84a10" : "#8a98a2"}" stroke-width="3" fill="none" opacity=".7"/>
    <ellipse cx="${x - r * 0.35}" cy="${y - r * 0.45}" rx="${r * 0.32}" ry="${r * 0.2}" fill="#fff" opacity=".75" transform="rotate(-30 ${x - r * 0.35} ${y - r * 0.45})"/>
    <text x="${x}" y="${y + r * 0.36}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="${r * 1.05}" fill="${c === "O" ? "#fff" : INK}" stroke="${c === "O" ? "#7a3008" : "none"}" stroke-width="3" paint-order="stroke">${letter}</text>`;

  // ---------------- ยาย's driftwood board ----------------
  const RULES = [
    ["recede", "ทะเล<u>ถอย</u> อย่า<u>คอย</u>ดู"],
    ["waves", "คลื่นแรก<u>ไป</u> อย่าไว้<u>ใจ</u>"],
    ["floor", "หนีไม่<u>ทัน</u> ขึ้น<u>ชั้น</u>สูง"],
  ];
  function boardPath(x, y, w, h, seed) {
    const r = mkR(seed), pts = [];
    const n = 14;
    for (let k = 0; k <= n; k++) pts.push([x + (w * k) / n, y + (r() - 0.5) * 12 + (k === 0 || k === n ? 14 : 0)]);
    const right = [[x + w + 4, y + h * 0.3], [x + w - 4, y + h * 0.7]];
    const bot = [];
    for (let k = n; k >= 0; k--) bot.push([x + (w * k) / n, y + h + (r() - 0.5) * 16 - (k === 0 || k === n ? 14 : 0)]);
    const left = [[x - 6, y + h * 0.66], [x + 4, y + h * 0.28]];
    const all = [...pts, ...right, ...bot, ...left];
    return `M${all.map(([a, b]) => `${f1(a)},${f1(b)}`).join(" L")}Z`;
  }
  function rule(tl, layer, t0, dur, o = {}) {
    const id = nid(), act = o.active ?? 0, done = o.done || [], at = o.at || [0.55, 0.7, 0.85], Y0 = o.y ?? 300;
    const RR = o.rules || RULES, n = RR.length, GAP = o.gap ?? 190, isAct = (k) => (o.seq ? true : k === act), TITLE = o.title || "กฎของยาย";
    const X = 70, W = 940, H = o.h ?? 250 + n * GAP - 60, rowY = (k) => Y0 + 250 + k * GAP;
    const outline = boardPath(X, Y0, W, H, 7);
    let rows = "";
    RR.forEach(([ic, txt], k) => {
      const st = isAct(k) ? "act" : done.includes(k) ? "done" : "later", y = rowY(k), len = plain(txt).length;
      const col = st === "later" ? "#8a7f70" : "#1e2a3a", rc = st === "later" ? "#9a8e7e" : "#d8312a";
      const t = txt.replace(/<u>(.*?)<\/u>/g, `<tspan class="tuU" fill="${rc}">$1</tspan>`);
      const tw = Math.min(700, len * 36 + 30);
      rows += `<g id="${id}-r${k}" opacity="${st === "later" ? 0.5 : 0}">
        ${st === "act" ? `<path id="${id}-hl${k}" d="M246,${y - 50}Q420,${y - 66} ${246 + tw},${y - 52}L${250 + tw},${y + 40}Q440,${y + 54} 240,${y + 36}Z" fill="url(#tuBrush)"/>
          <path d="M${250 + tw - 30},${y - 46}l26,6M${250 + tw - 40},${y + 38}l30,-4" stroke="#ffd23a" stroke-width="4" opacity=".6" stroke-linecap="round"/>` : ""}
        <g transform="translate(36,${y - 84})"><g id="${id}-s${k}"${st === "act" ? ` opacity="0"` : ""}>${icon(ic, 0, 0, 1.45, `${id}-ic${k}`)}</g></g>
        ${st === "act" ? `<defs><clipPath id="${id}-cp${k}"><rect id="${id}-cr${k}" x="230" y="${y - 70}" width="0" height="120"/></clipPath></defs>` : ""}
        <g${st === "act" ? ` clip-path="url(#${id}-cp${k})"` : ""}>
          <text x="262" y="${y + 26}" font-family="Sriracha" font-size="72" fill="#fffaf0" stroke="#fffaf0" stroke-width="10" stroke-linejoin="round" opacity="${st === "later" ? 0.4 : 0.85}">${plain(txt)}</text>
          <text x="262" y="${y + 26}" font-family="Sriracha" font-size="72" fill="${col}">${t}</text></g>
        ${st === "done" ? `<path id="${id}-tk${k}" d="M${270 + tw},${y - 6}l22,26l46,-58" stroke="#1e9a50" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>` : ""}
        ${st === "later" ? `<path d="M240,${y - 10}H${260 + tw}" stroke="#fff" stroke-width="40" opacity=".18"/>` : ""}</g>`;
    });
    // decor: a scrap of fishing net and a float on the top-right corner, barnacles and a starfish low left, a shell chime under it
    const net = `<g opacity=".9">${Array.from({ length: 9 }, (_, k) => `<path d="M${X + W - 210 + k * 26},${Y0 - 6}Q${X + W - 170 + k * 24},${Y0 + 60} ${X + W + 6},${Y0 + 40 + k * 22}" stroke="#2e4a5a" stroke-width="2.4" fill="none" opacity=".55"/>`).join("")}
      ${Array.from({ length: 7 }, (_, k) => `<path d="M${X + W - 200 + k * 30},${Y0 - 4}Q${X + W - 120},${Y0 + 30 + k * 20} ${X + W + 4},${Y0 + 160 - k * 18}" stroke="#2e4a5a" stroke-width="2.4" fill="none" opacity=".45"/>`).join("")}
      ${float(X + W - 40, Y0 + 120, 26, "", "O")}</g>`;
    const barn = Array.from({ length: 7 }, (_, k) => { const bx = X + 40 + (k % 4) * 22 + (k > 3 ? 10 : 0), by = Y0 + H - 50 + (k > 3 ? 18 : 0); return `<path d="M${bx - 9},${by + 6}L${bx - 5},${by - 8}H${bx + 5}L${bx + 9},${by + 6}Z" fill="#e8e2d2" ${OUT(1.8)}/><ellipse cx="${bx}" cy="${by - 8}" rx="4" ry="2" fill="#5a5248"/>`; }).join("");
    const star = `<g transform="translate(${X + 170},${Y0 + H - 30}) rotate(14)"><path d="M0,-30L8,-9L30,-8L13,6L19,28L0,15L-19,28L-13,6L-30,-8L-8,-9Z" fill="#f08a4a" ${OUT(2.6)}/>${[[0, -16], [10, -4], [6, 10], [-6, 10], [-10, -4]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="2.2" fill="#ffd0a0"/>`).join("")}</g>`;
    const chime = `<g transform="translate(540,${Y0 + H + 4})"><g id="${id}-ch">${[-60, 0, 60].map((dx, k) => `<path d="M${dx},0V${70 + k * 18}" stroke="#d8c8a4" stroke-width="2.4"/>
      <g transform="translate(${dx},${76 + k * 18})"><path d="M0,-12Q-16,-4 -10,12Q0,20 10,12Q16,-4 0,-12Z" fill="${["#f6e2d0", "#fff4ec", "#f2d0c8"][k]}" ${OUT(2)}/><path d="M0,-12V14M-6,-6Q-8,6 -4,12M6,-6Q8,6 4,12" stroke="#c8a088" stroke-width="1.4" fill="none"/></g>`).join("")}</g></g>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">
      ${rope(X + 120, -40, Y0 + 24)}${rope(X + W - 120, -40, Y0 + 24)}
      <path d="${outline}" fill="url(#tuWoodSide)" stroke="${INK}" stroke-width="5" transform="translate(0,16)"/>
      <path d="${outline}" fill="url(#tuWood)" stroke="${INK}" stroke-width="5"/>
      <defs><clipPath id="${id}-bc"><path d="${outline}"/></clipPath></defs>
      <g clip-path="url(#${id}-bc)">${grain(X, Y0, W, H, 11, { knots: 3, stains: 5 })}<rect x="${X}" y="${Y0}" width="${W}" height="40" fill="#fff" opacity=".12"/></g>
      ${[[X + 120, Y0 + 26], [X + W - 120, Y0 + 26]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="12" fill="#5a3a22" ${OUT(2)}/><circle cx="${a}" cy="${b}" r="6" fill="#2a1a10"/>`).join("")}
      ${[[X + 30, Y0 + 60], [X + W - 34, Y0 + H - 40], [X + W - 30, Y0 + 300]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="6" fill="#7a4a22" opacity=".8"/><path d="M${a - 2},${b + 4}q-2,14 2,26" stroke="#9a5a2a" stroke-width="3" opacity=".35" fill="none"/>`).join("")}
      <g transform="translate(540,${Y0 + 122})"><path d="M-330,-14q20,-14 40,0t40,0M290,-14q20,-14 40,0t40,0" stroke="#2a9ca6" stroke-width="7" fill="none" stroke-linecap="round"/>
        <text y="18" text-anchor="middle" font-family="Sriracha" font-size="96" fill="#fffaf0" stroke="#fffaf0" stroke-width="16" stroke-linejoin="round">${TITLE}</text>
        <text y="18" text-anchor="middle" font-family="Sriracha" font-size="96" fill="#d8312a">${TITLE}</text>
        <path d="M-200,38Q0,52 200,38" stroke="#d8312a" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/></g>
      ${rows}${net}${barn}${star}${chime}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0);
    // in: dropped on its ropes, swings and settles, then sways in the breeze; the shell chime lags behind
    tl.fromTo(`#${id}-m`, { y: -1100 }, { y: 0, duration: 0.55, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 5, svgOrigin: `540 ${Y0 - 900}` }, { rotation: 0, svgOrigin: `540 ${Y0 - 900}`, duration: 1.6, ease: "elastic.out(1, 0.32)", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-sw`, { rotation: 0, svgOrigin: `540 ${Y0 - 900}` }, { rotation: 0.6, svgOrigin: `540 ${Y0 - 900}`, duration: 1.3, repeat: Math.ceil(dur / 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 2);
    tl.fromTo(`#${id}-ch`, { rotation: -14, svgOrigin: "0 0" }, { rotation: 10, svgOrigin: "0 0", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.5);
    // rows land; the active one is brushed on
    RR.forEach((_, k) => { if (isAct(k) || done.includes(k)) tl.fromTo(`#${id}-r${k}`, { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + at[k]); });
    (o.seq ? RR.map((_, k) => k) : act >= 0 && act < n ? [act] : []).forEach((act) => {
      const ta = t0 + at[act];
      tl.fromTo(`#${id}-cr${act}`, { attr: { width: 0 } }, { attr: { width: 780 }, duration: 0.7, ease: "power1.inOut", immediateRender: false }, ta + 0.1);
      tl.fromTo(`#${id}-hl${act}`, { scaleX: 0, svgOrigin: `240 ${rowY(act)}` }, { scaleX: 1, svgOrigin: `240 ${rowY(act)}`, duration: 0.5, ease: "power2.inOut", immediateRender: false }, ta + 0.6);
      tl.fromTo(`#${id}-s${act}`, { scale: 0, rotation: -40, opacity: 1, svgOrigin: "87 87" }, { scale: 1, rotation: 0, opacity: 1, svgOrigin: "87 87", duration: 0.5, ease: "back.out(2.6)", immediateRender: false }, ta);
      iconPop(tl, document.getElementById(`${id}-ic${act}`), ta);
      iconLife(tl, document.getElementById(`${id}-ic${act}`), ta + 0.6, dur - at[act] - 0.6);
      document.getElementById(`${id}-r${act}`).querySelectorAll(".tuU").forEach((u, j) => { u.setAttribute("font-size", 72); tl.fromTo(u, { attr: { "font-size": 72 } }, { attr: { "font-size": 86 }, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, ta + 1.0 + j * 0.25); });
    });
    done.forEach((d) => { const el = document.getElementById(`${id}-tk${d}`); if (el) tl.fromTo(el, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + at[d] + 0.35); });
    if (o.out !== undefined) { tl.to(`#${id}-m`, { y: -200, duration: 0.3, ease: "power2.in" }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + o.out); }
    return id;
  }

  // ---------------- จูน's livestream ----------------
  const NAMECOL = ["#ffd23a", "#7ae0ff", "#ff9ac0", "#a8f08a", "#ffb070", "#c8a8ff"];
  const hashN = (s) => { let h = 7; for (const ch of s) h = (h * 31 + ch.codePointAt(0)) % 9973; return h; };
  function live(tl, layer, t0, dur, o = {}) {
    const id = nid(), V = o.viewers || [120, 4800], name = o.name || "จูน ทะเลใส", R = mkR(5);
    const run = o.end !== undefined ? Math.min(dur, o.end) : dur;   // the stream is live until o.end
    const comments = (o.comments || []).filter(([t]) => t < run), pin = o.pin && o.pin[0] < run ? o.pin : null;
    const CY = o.cy ?? 1500, ROW = 104, fmt = (v) => (v >= 10000 ? `${(v / 1000).toFixed(1)}K` : v >= 1000 ? `${(v / 1000).toFixed(2)}K` : String(Math.round(v)));
    // a little portrait of จูน in the avatar (black hair, pink ends, the shell clip)
    const avatar = `<g transform="translate(96,146)"><circle r="50" fill="url(#tuStory)"/><circle r="44" fill="#1a1418"/><circle r="40" fill="#bfe8f4"/>
      <defs><clipPath id="${id}-av"><circle r="40"/></clipPath></defs><g clip-path="url(#${id}-av)">
        <path d="M-34,44Q-36,4 -20,-6Q0,-14 20,-6Q36,4 34,44Z" fill="#b8a4ea"/><path d="M-26,22Q-30,-24 0,-30Q30,-24 26,22Q24,0 18,-6Q0,-2 -18,-6Q-24,0 -26,22Z" fill="#1d1418"/>
        <circle cx="0" cy="-6" r="16" fill="#ebc19c"/><path d="M-16,-10Q-14,-30 4,-28Q18,-26 18,-12Q8,-20 -4,-16Z" fill="#1d1418"/><path d="M-22,10Q-24,22 -18,30M22,10Q24,22 18,30" stroke="#ff8cbc" stroke-width="5"/>
        <circle cx="-6" cy="-6" r="2" fill="#2a1a12"/><circle cx="7" cy="-6" r="2" fill="#2a1a12"/><path d="M-3,3q4,3 7,0" stroke="#c8506a" stroke-width="2" fill="none"/></g></g>`;
    const eye = `<path d="M-16,0Q0,-12 16,0Q0,12 -16,0Z" fill="none" stroke="#fff" stroke-width="3.4"/><circle r="4.6" fill="#fff"/>`;
    const btn = (y, art, count, k) => `<g transform="translate(990,${y})"><g id="${id}-b${k}"><circle r="46" fill="#000" opacity=".28"/><circle r="40" fill="#1a1e24" opacity=".55"/>${art}
      <text id="${id}-n${k}" y="74" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="26" fill="#fff" stroke="#000" stroke-width="5" paint-order="stroke" opacity=".95">${count}</text></g></g>`;
    const heartD = "M0,14C-26,-4 -28,-22 -16,-28C-8,-32 -2,-28 0,-20C2,-28 8,-32 16,-28C28,-22 26,-4 0,14Z";
    const heartBtn = `<path d="${heartD}" transform="translate(0,4) scale(1.15)" fill="#ff3a5a" stroke="#fff" stroke-width="3"/>`;
    const talkBtn = `<path d="M-20,-16H20Q26,-16 26,-10V8Q26,14 20,14H0L-12,24V14H-20Q-26,14 -26,8V-10Q-26,-16 -20,-16Z" fill="#fff"/><circle cx="-10" cy="-1" r="3" fill="#1a1e24"/><circle cx="0" cy="-1" r="3" fill="#1a1e24"/><circle cx="10" cy="-1" r="3" fill="#1a1e24"/>`;
    const shareBtn = `<path d="M-18,16V2Q-18,-10 -2,-10H6V-22L26,-2L6,18V6H0Q-12,6 -18,16Z" fill="#fff"/>`;
    const top = `<g id="${id}-top">${avatar}
        <text x="160" y="140" font-family="Kanit" font-weight="700" font-size="38" fill="#fff" stroke="#000" stroke-width="6" paint-order="stroke">${name}</text>
        <g transform="translate(160,158)"><rect width="150" height="40" rx="20" fill="#ff3a5a"/><text x="75" y="29" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="24" fill="#fff">+ ติดตาม</text></g>
        <g transform="translate(560,104)"><g id="${id}-live"><rect width="132" height="58" rx="14" fill="#7a0e1c" transform="translate(0,6)"/><rect width="132" height="58" rx="14" fill="url(#tuLiveR)" stroke="#fff" stroke-width="3"/>
          <circle id="${id}-dot" cx="28" cy="29" r="9" fill="#fff"/><text x="84" y="41" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#fff">LIVE</text></g>
          ${o.end !== undefined ? `<g id="${id}-off" opacity="0"><rect width="132" height="58" rx="14" fill="#1a1e24" transform="translate(0,6)"/><rect width="132" height="58" rx="14" fill="#4a5058" stroke="#9aa4ae" stroke-width="3"/>
            <circle cx="28" cy="29" r="9" fill="#7a848e"/><text x="84" y="41" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="#9aa4ae">LIVE</text></g>` : ""}</g>
        <g transform="translate(710,104)"><rect width="200" height="58" rx="29" fill="#000" opacity=".45"/><g transform="translate(40,29)">${eye}</g>
          <text id="${id}-v" x="72" y="41" font-family="Kanit" font-weight="700" font-size="32" fill="#fff">${fmt(V[0])}</text></g>
        <g transform="translate(990,132)"><circle r="30" fill="#000" opacity=".35"/><path d="M-12,-12L12,12M12,-12L-12,12" stroke="#fff" stroke-width="5" stroke-linecap="round"/></g>
        ${o.title ? `<g transform="translate(40,212)"><rect width="${plain(o.title).length * 24 + 60}" height="52" rx="26" fill="#000" opacity=".4"/><path d="M24,26q8,-12 16,0t16,0" stroke="#7ae0ff" stroke-width="5" fill="none" stroke-linecap="round" transform="translate(-4,0)"/>
          <text x="62" y="36" font-family="Kanit" font-weight="700" font-size="28" fill="#fff">${o.title}</text></g>` : ""}</g>`;
    let g = `<rect width="1080" height="260" fill="url(#${id}-tg)"/><rect y="1300" width="1080" height="620" fill="url(#${id}-bg)"/>
      <defs><linearGradient id="${id}-tg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
        <linearGradient id="${id}-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></linearGradient></defs>`;
    g += btn(1080, heartBtn, o.likes ? fmt(o.likes[0]) : "12.4K", 0) + btn(1230, talkBtn, "856", 1) + btn(1380, shareBtn, "แชร์", 2);
    // hearts rising from the heart button
    const HN = Math.max(6, Math.round(run / 0.28)), HC = ["#ff3a5a", "#ff8ab8", "#ffd23a", "#8a6aff", "#ff6a3a"];
    for (let k = 0; k < HN; k++) g += `<g id="${id}-h${k}" opacity="0" transform="translate(990,1070)"><g transform="scale(${f1(0.7 + R() * 0.6)})"><path d="${heartD}" fill="${HC[k % HC.length]}" stroke="#fff" stroke-width="3"/></g></g>`;
    // the stack: comments and "… กำลังพิมพ์" rows, a pill each, newest at the bottom (y = CY); new ones push the old up
    const rows = [...comments.map(([t, who, text]) => ({ t, who, text })), ...(o.typing || []).filter(([t]) => t < run).map(([t, who, until]) => ({ t, who, until, typing: true }))];
    rows.sort((a, b) => a.t - b.t);
    rows.forEach((r) => {   // a typing row stops at its own `until`, at that name's next comment or pin, at the end of the stream, or 2.5 s on
      if (!r.typing) return;
      const next = [...rows.filter((q) => !q.typing && q.who === r.who && q.t > r.t).map((q) => q.t), ...(pin && pin[1] === r.who && pin[0] > r.t ? [pin[0]] : [])];
      r.end = Math.min(r.until ?? (next.length ? Infinity : r.t + 2.5), ...next, run);
    });
    rows.forEach((r, k) => {
      const c = NAMECOL[hashN(r.who) % NAMECOL.length];
      const w = r.typing ? Math.round(118 + Math.max(emW(r.who) * 27, emW("กำลังพิมพ์") * 28 + 76)) : Math.min(860, 120 + Math.max(plain(r.who).length * 18, plain(r.text).length * 22));
      g += `<g id="${id}-c${k}" opacity="0" transform="translate(36,${CY})"><g id="${id}-cm${k}">
        <rect width="${w}" height="88" rx="44" fill="#000" opacity="${r.typing ? 0.38 : 0.5}"/><circle cx="44" cy="44" r="31" fill="${c}" stroke="#fff" stroke-width="3"/><text x="44" y="56" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="32" fill="#1a1418">${plain(r.who).slice(0, 1)}</text>
        <text x="90" y="37" font-family="Kanit" font-weight="700" font-size="28" fill="${c}">${r.who}</text>${r.typing
          ? `<text x="90" y="72" font-family="Kanit" font-weight="400" font-size="28" fill="#fff" opacity=".8">กำลังพิมพ์</text>${[0, 1, 2].map((j) => `<circle class="tuDot" cx="${f1(90 + emW("กำลังพิมพ์") * 28 + 22 + j * 20)}" cy="62" r="6.5" fill="#fff"/>`).join("")}`
          : `<text x="90" y="72" font-family="Kanit" font-weight="500" font-size="32" fill="#fff">${r.text}</text>`}</g></g>`;
    });
    // the pinned comment: bigger, gold-rimmed, glowing, above the stack (which then keeps 3 rows)
    const PH = 132, pinY = CY - 2 * ROW - 34 - PH;
    let pw = 0;
    if (pin) {
      const [, pwho, ptext] = pin, c = NAMECOL[hashN(pwho) % NAMECOL.length];
      pw = Math.round(Math.min(900, 150 + Math.max(emW(pwho) * 34, emW(ptext) * 48)));
      const pushpin = `<g transform="rotate(32)"><path d="M-10,-24H10L7,-8Q17,-2 15,6H-15Q-17,-2 -7,-8Z" fill="#e8392c" ${OUT(2.6)}/><path d="M0,6V24" stroke="#c8d0d8" stroke-width="3.6" stroke-linecap="round"/><path d="M-4,-20H3" stroke="#fff" stroke-width="2.6" opacity=".7" stroke-linecap="round"/></g>`;
      g += `<g transform="translate(36,${pinY})"><g id="${id}-pin" opacity="0"><g id="${id}-pS">
        <g id="${id}-pg">${[[24, 0.12], [15, 0.2], [8, 0.34]].map(([e, op]) => `<rect x="${-e}" y="${-e}" width="${pw + 2 * e}" height="${PH + 2 * e}" rx="${PH / 2 + e}" fill="#ffd23a" opacity="${op}"/>`).join("")}</g>
        <rect y="9" width="${pw}" height="${PH}" rx="${PH / 2}" fill="#6a4a08" stroke="${INK}" stroke-width="3"/>
        <rect width="${pw}" height="${PH}" rx="${PH / 2}" fill="#1a1418" opacity=".9"/><rect width="${pw}" height="${PH}" rx="${PH / 2}" fill="none" stroke="#ffd23a" stroke-width="5"/>
        <rect x="${PH / 4}" y="8" width="${pw - PH / 2}" height="30" rx="15" fill="#fff" opacity=".08"/>
        <circle cx="66" cy="66" r="47" fill="${c}" stroke="#ffd23a" stroke-width="5"/><text x="66" y="84" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="#1a1418">${plain(pwho).slice(0, 1)}</text>
        <text x="134" y="54" font-family="Kanit" font-weight="700" font-size="34" fill="${c}">${pwho}</text>
        <text x="134" y="110" font-family="Kanit" font-weight="700" font-size="48" fill="#fff">${ptext}</text>
        <rect id="${id}-pf" width="${pw}" height="${PH}" rx="${PH / 2}" fill="#fff" opacity="0"/>
        <rect id="${id}-pr" x="-4" y="-4" width="${pw + 8}" height="${PH + 8}" rx="${PH / 2 + 4}" fill="none" stroke="#ffd23a" stroke-width="6" opacity="0"/>
        <g transform="translate(${pw - 150},-12)"><g id="${id}-pc" opacity="0">${slab(0, -24, 150, 48, 24, { face: "url(#tuNote)", body: "#8a6e4c", d: 6, sw: 3 })}
          <g transform="translate(28,-2)"><g id="${id}-pp">${pushpin}</g></g><text x="92" y="9" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#1e2a3a">ปักหมุด</text></g></g></g></g></g>`;
    }
    g += `<g transform="translate(36,1618)"><rect width="760" height="76" rx="38" fill="#000" opacity=".42"/><text x="40" y="49" font-family="Kanit" font-weight="400" font-size="30" fill="#fff" opacity=".7">แสดงความคิดเห็น…</text></g>
      <g transform="translate(870,1656)"><rect x="-34" y="-30" width="68" height="60" rx="10" fill="#ff8a3a" stroke="#fff" stroke-width="3"/><path d="M-34,-10H34M0,-30V30" stroke="#fff" stroke-width="5"/><path d="M0,-30Q-20,-50 -26,-34Q-20,-26 0,-30Q20,-50 26,-34Q20,-26 0,-30" fill="#ffd23a" stroke="#fff" stroke-width="3"/></g>
      <g transform="translate(990,1656)"><circle r="38" fill="#000" opacity=".4"/>${shareBtn}</g>`;
    // the end of the stream: a glitch, the picture dims, "ไลฟ์สิ้นสุดแล้ว" with a lost-signal icon (above the caption band)
    const EY = o.endY ?? 820;
    const endPanel = o.end === undefined ? "" : `<rect id="${id}-dim" width="1080" height="1920" fill="#05070a" opacity="0"/>
      <g id="${id}-gl" opacity="0">${[[300, 56, "#fff", 0.5], [760, 22, "#7ae0ff", 0.6], [1120, 40, "#ff5a8a", 0.45], [1460, 16, "#fff", 0.6], [520, 10, "#ffd23a", 0.5]].map(([y, h, c, op], k) => `<rect class="tuGb" data-k="${k}" x="-40" y="${y}" width="1160" height="${h}" fill="${c}" opacity="${op}"/>`).join("")}</g>
      <g transform="translate(540,${EY})"><g id="${id}-ep" opacity="0">
        <ellipse cx="0" cy="236" rx="280" ry="24" fill="url(#tuSoftSh)" opacity=".7"/>
        ${slab(-300, -200, 600, 400, 44, { face: "#262b33", body: "#0a0c10", bodyStroke: "#000", stroke: "#4a525c", d: 14, sw: 4, gloss: false })}
        <g transform="translate(0,-74)"><circle r="92" fill="#1a1e24" stroke="#4a525c" stroke-width="4"/>
          ${[0, 1, 2, 3].map((k) => `<rect class="tuBar" data-k="${k}" x="${-52 + k * 28}" y="${34 - (24 + k * 20)}" width="20" height="${24 + k * 20}" rx="4" fill="${k ? "#5a646e" : "#e8ecee"}"/>`).join("")}
          <g transform="translate(52,-50)"><g id="${id}-x"><circle r="27" fill="#e8392c" stroke="#fff" stroke-width="4"/><path d="M-10,-10L10,10M10,-10L-10,10" stroke="#fff" stroke-width="6" stroke-linecap="round"/></g></g></g>
        <text y="92" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#fff">ไลฟ์สิ้นสุดแล้ว</text>
        <text y="148" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#9aa4ae">สัญญาณขาดหาย</text></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-ui">${g}</g>${endPanel}${top}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t0);
    tl.fromTo(`#${id}-top`, { y: -60 }, { y: 0, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-live`, { scale: 1, svgOrigin: "66 29" }, { scale: 1.08, svgOrigin: "66 29", duration: 0.5, repeat: Math.ceil(run / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-dot`, { opacity: 1 }, { opacity: 0.2, duration: 0.45, repeat: Math.ceil(run / 0.45), yoyo: true, ease: "none", immediateRender: false }, t0);
    // the viewer count climbs (faster as the sea gets stranger); the likes too, if given
    const vEl = document.getElementById(`${id}-v`), vc = { v: V[0] };
    tl.fromTo(vc, { v: V[0] }, { v: V[1], duration: run, ease: "power2.in", immediateRender: false, onUpdate: () => (vEl.textContent = fmt(vc.v)) }, t0);
    if (o.likes) { const nEl = document.getElementById(`${id}-n0`), lc = { v: o.likes[0] }; tl.fromTo(lc, { v: o.likes[0] }, { v: o.likes[1], duration: run, ease: "power1.in", immediateRender: false, onUpdate: () => (nEl.textContent = fmt(lc.v)) }, t0); }
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-b${k}`, { x: 120 }, { x: 0, duration: 0.45, ease: "back.out(2)", immediateRender: false }, t0 + 0.15 + k * 0.08));
    for (let k = 0; k < HN; k++) {
      const tk = t0 + 0.3 + k * 0.28 + R() * 0.1, dx = (R() - 0.5) * 140, len = 1.5 + R() * 0.5;
      if (tk > t0 + run - 0.3) continue;
      tl.fromTo(`#${id}-h${k}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, tk);
      tl.fromTo(`#${id}-h${k}`, { x: 990, y: 1070 }, { keyframes: [{ x: 990 + dx * 0.4, y: 920, duration: len * 0.35, ease: "sine.out" }, { x: 990 - dx * 0.3, y: 780, duration: len * 0.35, ease: "sine.inOut" }, { x: 990 + dx, y: 620, duration: len * 0.3, ease: "sine.in" }], immediateRender: false }, tk);
      tl.to(`#${id}-h${k}`, { opacity: 0, duration: 0.35 }, tk + len - 0.35);
      if (o.end !== undefined && tk + len > t0 + run) tl.to(`#${id}-h${k}`, { opacity: 0, duration: 0.12 }, t0 + run);
    }
    if (rows.length) tl.fromTo(`#${id}-b0`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.18, svgOrigin: "0 0", duration: 0.14, repeat: Math.ceil(run / 0.28), yoyo: true, ease: "power2.out", immediateRender: false }, t0 + 0.4);
    // lay the stack out at every arrival / stop: newest first, a row higher and fainter each; 4 rows show (3 under a pin)
    // (rows and a pin with t < 0 were already there before the shot: they stand in place from t0, no entry)
    const evts = [...new Set([...rows.map((r) => Math.max(0, r.t)), ...rows.filter((r) => r.typing && r.end > 0).map((r) => r.end), ...(pin ? [Math.max(0, pin[0])] : [])])].filter((t) => t < run).sort((a, b) => a - b);
    const cur = rows.map(() => null);
    evts.forEach((te) => {
      const T = t0 + te, cap = pin && pin[0] <= te ? 3 : 4;
      rows.forEach((r, k) => { if (r.typing && r.end === te && cur[k]) { tl.fromTo(`#${id}-c${k}`, { opacity: cur[k][1] }, { opacity: 0, duration: 0.2, immediateRender: false }, T); cur[k] = null; } });
      const act = rows.map((_, k) => k).filter((k) => rows[k].t <= te && !(rows[k].typing && rows[k].end <= te)).sort((a, b) => rows[b].t - rows[a].t || b - a);
      act.forEach((k, slot) => {
        const y = CY - slot * ROW, op = slot >= cap ? 0 : +(1 - slot * 0.15).toFixed(2);
        if (rows[k].t === te) {
          tl.fromTo(`#${id}-c${k}`, { opacity: 0, y: CY + 70 }, { opacity: op, y, duration: 0.28, ease: "back.out(1.6)", immediateRender: false }, T);
          tl.fromTo(`#${id}-cm${k}`, { scale: 0.7, svgOrigin: "0 40" }, { scale: 1, svgOrigin: "0 40", duration: 0.35, ease: "back.out(2.2)", immediateRender: false }, T);
        } else if (!cur[k]) {
          tl.set(`#${id}-c${k}`, { y, opacity: op }, T);
        } else if (cur[k][0] !== y || cur[k][1] !== op) {
          tl.fromTo(`#${id}-c${k}`, { y: cur[k][0], opacity: cur[k][1] }, { y, opacity: op, duration: 0.25, ease: "power2.out", immediateRender: false }, T);
        }
        cur[k] = [y, op];
      });
    });
    // the typing dots hop in turn while the row shows
    rows.forEach((r, k) => { if (!r.typing) return;
      document.getElementById(`${id}-c${k}`).querySelectorAll(".tuDot").forEach((d, j) => tl.fromTo(d, { y: 0 }, { y: -10, duration: 0.2, repeat: Math.ceil((r.end - r.t) / 0.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + Math.max(0, r.t) + j * 0.1)); });
    if (pin && pin[0] <= 0) {
      tl.set([`#${id}-pin`, `#${id}-pc`], { opacity: 1 }, t0);
      tl.fromTo(`#${id}-pg`, { opacity: 1, scale: 1, svgOrigin: `${pw / 2} ${PH / 2}` }, { opacity: 0.45, scale: 1.035, svgOrigin: `${pw / 2} ${PH / 2}`, duration: 0.6, repeat: Math.ceil(dur / 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
      tl.fromTo(`#${id}-pp`, { rotation: -10, svgOrigin: "0 20" }, { rotation: 10, svgOrigin: "0 20", duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    } else if (pin) {
      const tp = t0 + pin[0], O = `0 ${PH / 2}`;
      // it pops in bigger than it stays, flashes, a ring bursts off it; the glow keeps breathing and the pin chip lands on it
      tl.fromTo(`#${id}-pin`, { opacity: 0 }, { opacity: 1, duration: 0.1, immediateRender: false }, tp);
      tl.fromTo(`#${id}-pS`, { scale: 0.35, svgOrigin: O }, { scale: 1.14, svgOrigin: O, duration: 0.26, ease: "power2.out", immediateRender: false }, tp);
      tl.fromTo(`#${id}-pS`, { scale: 1.14, svgOrigin: O }, { scale: 1, svgOrigin: O, duration: 0.6, ease: "elastic.out(1, 0.45)", immediateRender: false }, tp + 0.26);
      tl.fromTo(`#${id}-pf`, { opacity: 0.85 }, { opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, tp + 0.05);
      tl.fromTo(`#${id}-pr`, { opacity: 1, scale: 1, svgOrigin: `${pw / 2} ${PH / 2}` }, { opacity: 0, scale: 1.18, svgOrigin: `${pw / 2} ${PH / 2}`, duration: 0.6, ease: "power2.out", immediateRender: false }, tp + 0.12);
      tl.fromTo(`#${id}-pg`, { opacity: 1, scale: 1, svgOrigin: `${pw / 2} ${PH / 2}` }, { opacity: 0.45, scale: 1.035, svgOrigin: `${pw / 2} ${PH / 2}`, duration: 0.6, repeat: Math.ceil(dur / 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, tp + 0.3);
      tl.fromTo(`#${id}-pc`, { opacity: 0, scale: 0, rotation: -25, svgOrigin: "75 0" }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: "75 0", duration: 0.5, ease: "back.out(3)", immediateRender: false }, tp + 0.3);
      tl.fromTo(`#${id}-pp`, { rotation: -10, svgOrigin: "0 20" }, { rotation: 10, svgOrigin: "0 20", duration: 0.5, repeat: Math.ceil(dur / 0.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, tp + 0.8);
    }
    if (o.end !== undefined) {
      const tE = t0 + run;
      // the picture tears for a few frames, then the stream is gone: grey LIVE, counts frozen, everything dims under the panel
      tl.set(`#${id}-gl`, { opacity: 1 }, tE);
      document.getElementById(`${id}-gl`).querySelectorAll(".tuGb").forEach((b, k) => tl.fromTo(b, { x: 0 }, { keyframes: [{ x: (k % 2 ? 1 : -1) * (60 + k * 30), duration: 0.05 }, { x: (k % 2 ? -1 : 1) * (30 + k * 12), duration: 0.05 }, { x: 0, duration: 0.05 }], ease: "none", immediateRender: false }, tE));
      tl.set(`#${id}-gl`, { opacity: 0 }, tE + 0.18);
      tl.fromTo(`#${id}-ui`, { x: 0 }, { keyframes: [{ x: -14, duration: 0.04 }, { x: 10, duration: 0.04 }, { x: -6, duration: 0.04 }, { x: 0, duration: 0.04 }], ease: "none", immediateRender: false }, tE);
      tl.fromTo(`#${id}-dim`, { opacity: 0 }, { opacity: 0.74, duration: 0.4, ease: "power2.out", immediateRender: false }, tE + 0.06);
      tl.set(`#${id}-live`, { opacity: 0 }, tE);
      tl.set(`#${id}-off`, { opacity: 1 }, tE);
      tl.fromTo(`#${id}-ep`, { opacity: 0, y: 50, scale: 0.7, svgOrigin: "0 0" }, { opacity: 1, y: 0, scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "back.out(2)", immediateRender: false }, tE + 0.35);
      tl.fromTo(`#${id}-x`, { scale: 0, rotation: -40, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.55, ease: "elastic.out(1, 0.45)", immediateRender: false }, tE + 0.7);
      // searching: the bars light up one by one and drop out again; the panel floats
      const rest = Math.max(0.6, dur - run);
      document.getElementById(`${id}-ep`).querySelectorAll(".tuBar").forEach((b, k) => { if (k) tl.fromTo(b, { fill: "#5a646e" }, { fill: "#e8ecee", duration: 0.12, repeat: Math.ceil(rest / 0.9), repeatDelay: 0.78, yoyo: true, ease: "none", immediateRender: false }, tE + 0.9 + k * 0.18); });
      tl.fromTo(`#${id}-ep`, { y: 0 }, { y: -8, duration: 1.1, repeat: Math.ceil(rest / 1.1), yoyo: true, ease: "sine.inOut", immediateRender: false }, tE + 0.95);
    }
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.2 }, t0 + o.out);
    return id;
  }

  // ---------------- the choice on driftwood, with the undertow ----------------
  function choice(tl, layer, t0, dur, o = {}) {
    const id = nid(), secs = o.secs ?? 3, A = o.a || { text: "วิ่งไปดึงน้อง" }, B = o.b || { text: "วิ่งขึ้นเขา" }, Y = [o.yA ?? 900, o.yB ?? 1210];
    const art = (c, k) => !c.icon ? "" : ICON[c.icon] ? icon(c.icon, -380, -92, 1.5, `${id}-i${k}`) : `<g transform="translate(-300,0)">${c.icon}</g>`;
    const card = (k, c) => {
      const tx = c.icon ? -180 : -300;
      return `<g transform="translate(540,${Y[k]})"><g id="${id}-e${k}" opacity="0"><g id="${id}-q${k}"><g id="${id}-c${k}">
        <rect id="${id}-sh${k}" x="-430" y="-100" width="860" height="270" rx="60" fill="url(#tuSoftSh)" opacity=".8"/>
        <g id="${id}-l${k}">
          <path d="${boardPath(-430, -125, 860, 250, 21 + k)}" fill="url(#tuWoodSide)" stroke="${INK}" stroke-width="5" transform="translate(0,14)"/>
          <path d="${boardPath(-430, -125, 860, 250, 21 + k)}" fill="url(#tuWoodL)" stroke="${INK}" stroke-width="5"/>
          <g opacity=".9">${grain(-430, -125, 860, 250, 30 + k, { knots: 1, stains: 2, lines: 9 })}</g>
          <g id="${id}-wet${k}" opacity="0"><path d="${boardPath(-430, -125, 860, 250, 21 + k)}" fill="#4a3a2a" opacity=".35"/>${[-300, -120, 80, 260].map((x, j) => `<path d="M${x},${125 + j % 2 * 6}q4,30 0,${40 + j * 8}" stroke="#6ad0e8" stroke-width="7" stroke-linecap="round" opacity=".7"/>`).join("")}</g>
          <g id="${id}-f${k}" opacity="0"><rect x="-448" y="-142" width="896" height="284" rx="46" fill="none" stroke="#ffd23a" stroke-width="24" opacity=".22"/><rect x="-442" y="-136" width="884" height="272" rx="40" fill="none" stroke="#ffd23a" stroke-width="10"/></g>
          ${float(-386, -88, 34, k ? "B" : "A", k ? "W" : "O")}
          ${art(c, k)}
          <text x="${tx}" y="32" font-family="Kanit" font-weight="900" font-size="${plain(c.text).length > 12 ? 70 : 82}" fill="#fffaf0" stroke="#fffaf0" stroke-width="12" stroke-linejoin="round" opacity=".7">${c.text}</text>
          <text x="${tx}" y="32" font-family="Kanit" font-weight="900" font-size="${plain(c.text).length > 12 ? 70 : 82}" fill="#1e2a3a">${c.text}</text>
          <g id="${id}-red${k}" opacity="0"><rect x="-436" y="-130" width="872" height="260" rx="38" fill="none" stroke="#ff3a2a" stroke-width="12"/></g></g></g></g></g></g>`;
    };
    // the lifebuoy countdown
    const buoy = `<g transform="translate(300,0)"><circle cy="6" r="66" fill="#000" opacity=".3"/>
      ${[0, 1, 2, 3, 4, 5, 6, 7].map((k) => { const a0 = (k * 45 - 90) * Math.PI / 180, a1 = ((k + 1) * 45 - 90) * Math.PI / 180, R1 = 64, R0 = 38;
        return `<path d="M${f1(R1 * Math.cos(a0))},${f1(R1 * Math.sin(a0))}A${R1},${R1} 0 0 1 ${f1(R1 * Math.cos(a1))},${f1(R1 * Math.sin(a1))}L${f1(R0 * Math.cos(a1))},${f1(R0 * Math.sin(a1))}A${R0},${R0} 0 0 0 ${f1(R0 * Math.cos(a0))},${f1(R0 * Math.sin(a0))}Z" fill="${k % 2 ? "#fff" : "#e8392c"}"/>`; }).join("")}
      <circle r="64" fill="none" ${OUT(4)}/><circle r="38" fill="#16120f" ${OUT(3)}/><circle r="64" fill="url(#tuBuoy)"/>
      <circle id="${id}-ring" r="30" fill="none" stroke="#ffd23a" stroke-width="8" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0" transform="rotate(-90)"/>
      <text id="${id}-n" y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="#fff">${secs}</text>
      <path d="M-46,-38A60,60 0 0 1 -12,-60" stroke="#fff" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/></g>`;
    // the surge: a wall of water with a curling foam lip, spray and bubbles (screen space)
    const R = mkR(13);
    let lip = "M-60,60";
    for (let x = -60; x <= 1140; x += 60) lip += ` Q${x + 30},${f1(-24 - R() * 26)} ${x + 60},${f1(8 + R() * 12)}`;
    const surge = `<g id="${id}-sg" transform="translate(0,2200)" opacity="0"><g id="${id}-sgw">
      <path d="${lip} V1100 H-60 Z" fill="url(#tuWaveWall)"/>
      <path d="${lip}" stroke="#effcff" stroke-width="26" fill="none" stroke-linecap="round" opacity=".95"/><path d="${lip}" stroke="#bff2ff" stroke-width="8" fill="none" transform="translate(0,26)" opacity=".7"/>
      ${Array.from({ length: 26 }, () => `<circle cx="${f1(R() * 1080)}" cy="${f1(-40 - R() * 90)}" r="${f1(5 + R() * 12)}" fill="#effcff" opacity="${f1(0.6 + R() * 0.4)}"/>`).join("")}
      ${Array.from({ length: 30 }, () => `<circle cx="${f1(R() * 1080)}" cy="${f1(60 + R() * 600)}" r="${f1(3 + R() * 8)}" fill="none" stroke="#bff2ff" stroke-width="2.4" opacity=".55"/>`).join("")}
      ${Array.from({ length: 8 }, (_, k) => `<path d="M${-40 + k * 150},${140 + (k % 3) * 40}q60,-30 120,0" stroke="#7ad8ec" stroke-width="6" fill="none" opacity=".5" stroke-linecap="round"/>`).join("")}</g></g>`;
    put(layer, `<g id="${id}" opacity="0"><rect id="${id}-dim" width="1080" height="1920" fill="#06121a" opacity=".45"/>
      <g transform="translate(540,580)"><g id="${id}-qe"><g id="${id}-qs">
        <ellipse cx="0" cy="96" rx="400" ry="34" fill="url(#tuSoftSh)" opacity=".6"/>
        <path d="${boardPath(-420, -78, 840, 156, 9)}" fill="url(#tuWoodSide)" stroke="${INK}" stroke-width="5" transform="translate(0,12)"/>
        <path d="${boardPath(-420, -78, 840, 156, 9)}" fill="url(#tuWood)" stroke="${INK}" stroke-width="5"/>
        <g opacity=".9">${grain(-420, -78, 840, 156, 44, { knots: 1, stains: 2, lines: 6 })}</g>
        <text x="-60" y="26" text-anchor="middle" font-family="Sriracha" font-size="78" fill="#fffaf0" stroke="#fffaf0" stroke-width="12" stroke-linejoin="round">${o.q || "จะทำยังไง?"}</text>
        <text x="-60" y="26" text-anchor="middle" font-family="Sriracha" font-size="78" fill="#d8312a">${o.q || "จะทำยังไง?"}</text>
        ${buoy}</g></g></g>
      ${card(0, A)}${card(1, B)}${surge}</g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.18, immediateRender: false }, t0);
    tl.fromTo(`#${id}-qe`, { y: -80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.32, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-qs`, { scaleX: 0.5, scaleY: 1.35, svgOrigin: "0 78" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 78", duration: 0.7, ease: "elastic.out(1, 0.45)", immediateRender: false }, t0);
    [0, 1].forEach((k) => {
      const t = t0 + 0.12 + k * 0.14;
      tl.fromTo(`#${id}-e${k}`, { y: 160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.32, ease: "power3.out", immediateRender: false }, t);
      tl.fromTo(`#${id}-q${k}`, { scaleX: 0.72, scaleY: 1.22, svgOrigin: "0 125" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 125", duration: 0.85, ease: "elastic.out(1, 0.5)", immediateRender: false }, t);
      iconPop(tl, document.getElementById(`${id}-i${k}`), t);
      iconLife(tl, document.getElementById(`${id}-i${k}`), t0 + 0.9, dur);
    });
    const pk = o.pull === "b" ? 1 : o.pull === "a" ? 0 : -1, PT = o.at ?? Math.min(secs, dur - 1.2);
    const ring = { k: 0 }, n = document.getElementById(`${id}-n`), ringEl = document.getElementById(`${id}-ring`), T = pk >= 0 ? PT : secs;
    tl.fromTo(ring, { k: 0 }, { k: T / secs, duration: T, ease: "none", immediateRender: false, onUpdate: () => { ringEl.setAttribute("stroke-dashoffset", f1(ring.k)); n.textContent = String(Math.max(0, Math.ceil(secs * (1 - ring.k) - 0.001))); } }, t0);
    for (let m = secs - 1; m >= 1; m--) { const tm = t0 + secs * (1 - m / secs); if (tm > t0 + 0.05 && tm < t0 + T) tl.fromTo(n, { scale: 1.45, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.3, ease: "back.out(3)", immediateRender: false }, tm); }
    tl.fromTo(`#${id}-qs`, { rotation: 0, svgOrigin: "0 78" }, { rotation: 1.2, svgOrigin: "0 78", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.8);
    // the frame hovers A, B, A… (cards lift off their shadows)
    const up = [0, 0];
    const focus = (t, k) => {
      tl.set(`#${id}-f${k}`, { opacity: 1 }, t); tl.set(`#${id}-f${1 - k}`, { opacity: 0 }, t);
      if (!up[k]) { tl.fromTo(`#${id}-l${k}`, { y: 0 }, { y: -16, duration: 0.22, ease: "back.out(3)", immediateRender: false }, t); up[k] = 1; }
      if (up[1 - k]) { tl.fromTo(`#${id}-l${1 - k}`, { y: -16 }, { y: 0, duration: 0.18, ease: "power2.out", immediateRender: false }, t); up[1 - k] = 0; }
    };
    const hov = o.hover || [[0.5, 1 - Math.max(0, pk)], [1.1, Math.max(0, pk)], [1.6, 1 - Math.max(0, pk)]];
    hov.filter(([t]) => t < T).forEach(([t, k]) => focus(t0 + t, k));
    if (pk >= 0) {
      const tp = t0 + PT, other = 1 - pk, topY = Math.min(Y[0], Y[1]) - 170, lift = 1980 - (pk === 0 ? Y[1] - 60 : Y[1] + 40);
      // the surge comes up the screen fast, rolls, and its foam lip catches the frame and carries it onto the pulled card
      tl.set(`#${id}-sg`, { opacity: 1 }, tp - 0.15);
      tl.fromTo(`#${id}-sg`, { y: 2200 }, { y: 1980 - lift, duration: 0.45, ease: "power3.out", immediateRender: false }, tp - 0.15);
      tl.fromTo(`#${id}-sgw`, { x: 0 }, { x: -60, duration: 1.4, ease: "sine.inOut", immediateRender: false }, tp - 0.15);
      tl.fromTo(`#${id}-sg`, { y: 1980 - lift }, { y: Math.max(topY, 1980 - lift - 160), duration: 0.35, ease: "sine.inOut", immediateRender: false }, tp + 0.3);
      focus(tp + 0.2, pk);
      tl.fromTo(`#${id}-c${other}`, { rotation: 0, svgOrigin: "0 0" }, { rotation: pk === 0 ? 4 : -4, svgOrigin: "0 0", duration: 0.5, ease: "power2.out", immediateRender: false }, tp + 0.1);
      tl.fromTo(`#${id}-c${other}`, { opacity: 1 }, { opacity: 0.45, duration: 0.4, immediateRender: false }, tp + 0.2);
      tl.fromTo(`#${id}-l${pk}`, { x: 0 }, { x: 16, duration: 0.5, ease: wobble(5), immediateRender: false }, tp + 0.35);
      tl.fromTo(`#${id}-red${pk}`, { opacity: 0 }, { opacity: 1, duration: 0.12, repeat: 5, yoyo: true, immediateRender: false }, tp + 0.4);
      // then it drains back down, leaving both boards wet and dripping
      tl.to(`#${id}-sg`, { y: 2200, duration: 0.8, ease: "power2.in" }, tp + 0.75);
      [0, 1].forEach((k) => tl.fromTo(`#${id}-wet${k}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, tp + 0.35));
      tl.fromTo(`#${id}-dim`, { opacity: 0.45 }, { opacity: 0.6, duration: 0.4, immediateRender: false }, tp);
      tl.set(n, { textContent: "!" }, tp);
    }
    if (o.out !== undefined) tl.to(`#${id}`, { opacity: 0, duration: 0.12 }, t0 + o.out);
    return id;
  }

  // ---------------- the end card: the evacuation sign at dusk ----------------
  // the sign's pictogram: a breaking wave, a figure running up a slope away from it, an arrow
  const signArt = `<path d="M-240,70Q-236,-10 -186,-46Q-146,-74 -116,-52Q-104,-42 -110,-30Q-128,-44 -146,-30Q-120,-32 -104,-12L-96,70Z" fill="#fff"/>
    <path d="M-176,10Q-160,-14 -136,-16" stroke="#1e5ab8" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M-94,70L60,-30V70Z" fill="#fff" opacity=".35"/>
    <g transform="translate(-6,-4)"><circle cx="0" cy="-48" r="15" fill="#fff"/><path d="M-6,-32L-18,8L4,30L-4,62M-18,8L-46,40M-8,-26L22,-6L40,-24M-8,-26L-34,-16L-44,-36" stroke="#fff" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
    <path d="M70,-6L150,-60M118,-64L152,-62L146,-28" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
  function endCard(tl, layer, t0, dur, o = {}) {
    const id = nid(), R = mkR(17), fin = !!o.final, l1 = o.l1 || (fin ? "ทะเลลด" : "ตอนที่ 2"), l2 = o.l2 || (fin ? "ตอนจบ" : "คลื่นแรกไป");
    // the lines shrink to stay on the 400-wide paper (Thai vowel and tone marks take no width of their own)
    const cells = (t) => [...plain(t)].filter((c) => !/[\u0E31\u0E34-\u0E3A\u0E47-\u0E4E]/.test(c)).length;
    const fit = (t, max) => Math.min(max, Math.floor(340 / (0.6 * Math.max(1, cells(t)))));
    let bg = `<rect width="1080" height="1920" fill="url(#tuDusk)"/>
      <circle cx="760" cy="1180" r="120" fill="#ffe6a8" opacity=".9"/><circle cx="760" cy="1180" r="260" fill="#ffd890" opacity=".18"/>
      ${Array.from({ length: 6 }, (_, k) => `<path d="M${-40 + k * 200},${300 + (k % 3) * 120}q90,-40 180,0q-60,24 -180,0Z" fill="#ffb4a0" opacity=".22"/>`).join("")}
      <path d="M-20,1250L120,1110L190,1150L260,1060L340,1250Z" fill="#3a2a4a" opacity=".75"/><path d="M820,1250L880,1170L930,1200L980,1120L1100,1250Z" fill="#3a2a4a" opacity=".7"/>
      <rect y="1250" width="1080" height="670" fill="url(#tuDuskSea)"/>`;
    for (let k = 0; k < 18; k++) bg += `<rect id="${id}-gl${k}" x="${f1(700 + (R() - 0.5) * 260)}" y="${f1(1262 + k * 22 + R() * 10)}" width="${f1(40 + R() * 90)}" height="4" rx="2" fill="#ffe6a8" opacity=".55"/>`;
    // the hill the sign stands on, palms against the sky
    bg += `<path d="M-40,1920V1380Q160,1300 380,1340Q600,1390 760,1520Q900,1640 1120,1640V1920Z" fill="#1a1426"/>
      ${[[120, 1330, 1], [300, 1350, 0.8]].map(([x, y, s]) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M0,0Q10,-160 -20,-300" stroke="#1a1426" stroke-width="14" fill="none"/>
        ${[-150, -100, -40, 20, 70, 130].map((a) => `<path d="M-20,-300q${f1(80 * Math.cos(a * Math.PI / 180))},${f1(80 * Math.sin(a * Math.PI / 180) - 30)} ${f1(160 * Math.cos(a * Math.PI / 180))},${f1(160 * Math.sin(a * Math.PI / 180) + 30)}" stroke="#1a1426" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("")}</g>`).join("")}`;
    for (let k = 0; k < 3; k++) bg += `<g id="${id}-bd${k}" transform="translate(${-80 - k * 70},${420 + k * 60})"><path d="M-14,0Q-7,-8 0,0Q7,-8 14,0" stroke="#2a1e30" stroke-width="4" fill="none" stroke-linecap="round"/></g>`;
    const sign = `<g transform="translate(540,620)"><g id="${id}-sg">
      <rect x="-16" y="120" width="32" height="1300" fill="url(#tuPole)" ${OUT(4)}/>
      <rect x="-330" y="-226" width="660" height="430" rx="28" fill="#0a1a3a" transform="translate(10,14)" opacity=".55"/>
      <rect x="-330" y="-226" width="660" height="430" rx="28" fill="#0e2e6a" ${OUT(5)} transform="translate(0,12)"/>
      <rect x="-330" y="-226" width="660" height="430" rx="28" fill="url(#tuSignB)" ${OUT(5)}/>
      <rect x="-312" y="-208" width="624" height="394" rx="18" fill="none" stroke="#fff" stroke-width="8"/>
      <g transform="translate(0,-50) scale(1.05)">${signArt}</g>
      <text y="104" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="56" fill="#fff">เส้นทางหนีคลื่นยักษ์</text>
      <text y="152" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#fff" letter-spacing="2">TSUNAMI EVACUATION ROUTE</text>
      ${[[-300, -196], [300, -196], [-300, 174], [300, 174]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="9" fill="#c8d0d8" ${OUT(2)}/><path d="M${a - 5},${b}h10" stroke="#5a646c" stroke-width="2"/>`).join("")}
      <path d="M-330,-226L-100,-226L-330,40Z" fill="#fff" opacity=".1"/><path d="M180,-210l40,30M-250,150l30,20M120,170l50,-6" stroke="#fff" stroke-width="3" opacity=".25"/>
      <circle cx="248" cy="-150" r="14" fill="#a85a2a" opacity=".35"/><circle cx="-268" cy="120" r="9" fill="#a85a2a" opacity=".3"/></g></g>`;
    // o.tag: a red sticker slapped on the note's top-right corner ("ตอนจบ" when true), so the next episode can be announced as the finale
    const tag = o.tag === true ? "ตอนจบ" : o.tag || "", tgW = Math.round(emW(tag) * 40 + 48);
    const tagMk = !tag ? "" : `<g transform="translate(${200 - tgW / 2 + 28},${fin ? 16 : 12}) rotate(-9)"><g id="${id}-tag" opacity="0">${slab(-tgW / 2, -31, tgW, 62, 16, { face: "url(#tuLiveR)", body: "#7a0e1c", d: 7, sw: 3.4 })}
        <rect x="${-tgW / 2 + 7}" y="-24" width="${tgW - 14}" height="48" rx="10" fill="none" stroke="#fff" stroke-width="2.4" stroke-dasharray="7 5" opacity=".75"/>
        <text y="14" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#fff">${tag}</text></g></g>`;
    const note = `<g transform="translate(540,${fin ? 1010 : 1000})"><g id="${id}-nt">
      <path d="M-200,0H200V${fin ? 300 : 280}H-200Z" fill="#000" opacity=".3" transform="translate(10,14)"/>
      <path d="M-200,0H200V${fin ? 300 : 280}H-200Z" fill="url(#tuNote)" stroke="#a8946a" stroke-width="3"/>
      <path d="M-200,${fin ? 300 : 280}L-176,${fin ? 276 : 256}V${fin ? 300 : 280}Z" fill="#d8c8a4"/>
      <g transform="rotate(-6)"><rect x="-80" y="-24" width="160" height="44" fill="#f2e6b8" opacity=".85" stroke="#d8c890" stroke-width="2"/><path d="M-70,-8H70" stroke="#fff" stroke-width="5" opacity=".4"/></g>
      ${fin ? `<text y="150" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fit(l1, 58)}" fill="#5a4a3a">${l1}</text>
        <text y="248" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fit(l2, 92)}" fill="#c8281e">${l2}</text>`
      : `<text y="112" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fit(l1, 54)}" fill="#5a4a3a">${l1}</text>
        <text y="214" text-anchor="middle" font-family="Mali" font-weight="700" font-size="${fit(l2, 84)}" fill="#c8281e">${l2}</text>`}
      <path d="M-170,${fin ? 270 : 252}q60,-8 120,0" stroke="#c8281e" stroke-width="4" fill="none" opacity=".5"/>${tagMk}</g></g>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-all">${bg}${sign}${note}</g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0);
    tl.fromTo(`#${id}-all`, { scale: 1, svgOrigin: "540 960" }, { scale: 1.05, svgOrigin: "540 960", duration: dur, ease: "none", immediateRender: false }, t0);
    // the sign shakes a little on its pole in the wind; the note pops on and flaps from its tape
    tl.fromTo(`#${id}-sg`, { rotation: -1.6, svgOrigin: "0 1400" }, { rotation: 1.2, svgOrigin: "0 1400", duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${id}-nt`, { scale: 0.2, rotation: -20, svgOrigin: "0 0" }, { scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.6, ease: "back.out(2.2)", immediateRender: false }, t0 + 0.25);
    tl.fromTo(`#${id}-nt`, { rotation: -3, svgOrigin: "0 0" }, { rotation: 4, svgOrigin: "0 0", duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.85);
    tl.fromTo(`#${id}-nt`, { skewY: 0 }, { skewY: 3, duration: 0.33, repeat: Math.ceil(dur / 0.33), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.85);
    if (tag) {
      const ts = t0 + (o.tagAt ?? 1.0);
      tl.fromTo(`#${id}-tag`, { opacity: 0, scale: 2.4, rotation: -16, svgOrigin: "0 0" }, { opacity: 1, scale: 1, rotation: 0, svgOrigin: "0 0", duration: 0.42, ease: "back.out(2.2)", immediateRender: false }, ts);
      tl.fromTo(`#${id}-tag`, { scale: 1, svgOrigin: "0 0" }, { scale: 1.07, svgOrigin: "0 0", duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, ts + 0.42);
    }
    for (let k = 0; k < 3; k++) {
      tl.fromTo(`#${id}-bd${k}`, { x: -80 - k * 70, y: 420 + k * 60 }, { x: 1180, y: 300 + k * 40, duration: dur + 1, ease: "none", immediateRender: false }, t0);
      tl.fromTo(`#${id}-bd${k} path`, { scaleY: 1, svgOrigin: "0 0" }, { scaleY: -0.6, svgOrigin: "0 0", duration: 0.2, repeat: Math.ceil(dur / 0.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + k * 0.07);
    }
    for (let k = 0; k < 18; k++) tl.fromTo(`#${id}-gl${k}`, { opacity: 0.15 }, { opacity: 0.8, duration: 0.3 + (k % 5) * 0.08, repeat: Math.ceil(dur / 0.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (k % 7) * 0.05);
    return id;
  }

  // ---------------- the source chip ----------------
  function source(tl, layer, t0, dur, o = {}) {
    const id = nid(), text = o.text || "", w = Math.round(plain(text).length * 14.5 + 104), y = o.y ?? 1790;
    put(layer, `<g transform="translate(540,${y})"><g id="${id}" opacity="0">
      <rect x="${-w / 2}" y="-26" width="${w}" height="58" rx="29" fill="#1a6a74" stroke="${INK}" stroke-width="3" transform="translate(0,7)"/>
      <rect x="${-w / 2}" y="-30" width="${w}" height="58" rx="29" fill="url(#tuChip)" stroke="${INK}" stroke-width="3"/>
      <circle cx="${-w / 2 + 31}" cy="-1" r="20" fill="#2a9ca6" stroke="${INK}" stroke-width="2.4"/><path d="M${-w / 2 + 19},1q6,-8 12,0t12,0" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>
      <text x="${-w / 2 + 62}" y="9" font-family="Kanit" font-weight="500" font-size="26" fill="#1e2a3a">${text}</text></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 30, scale: 0.85, svgOrigin: "0 0" }, { opacity: 1, y: 0, scale: 1, svgOrigin: "0 0", duration: 0.45, ease: "back.out(2)", immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
    return id;
  }

  // ---------------- the legend: ละบูน, told on the channel's shadow screen ----------------
  // the Moken legend of ละบูน, คลื่นยักษ์เจ็ดชั้น: when the sea drops strangely, the elders lead the children and everyone up the hill.
  // Puppets are cut, dyed leather with Moken motifs: pandanus weave (a diamond lattice punched through), wave scallops; a kabang
  // houseboat with its forked "mouth" bow and arched pandanus roof, a stilt hut, Moken elders and children, the wave as seven crests.
  const LEA = "#2a1408";
  const rod = (x, y, len = 300) => `<path d="M${x},${y}L${x + 6},${y + len}" stroke="#3a1e0e" stroke-width="7" stroke-linecap="round" opacity=".85"/>`;
  const weave = (d, c, op = 0.85) => `<path d="${d}" fill="${c}" opacity="${op}"/><path d="${d}" fill="url(#tuWeave)"/>`;
  function hillPuppet() {
    const body = "M-250,150Q-240,20 -160,-60Q-90,-130 -10,-120Q70,-110 130,-30Q180,50 220,150Z";
    const inner = "M-214,134Q-202,30 -136,-36Q-74,-98 -8,-92Q58,-86 108,-20Q150,46 180,134Z";
    let s = `<path d="${body}" fill="${LEA}"/>${weave(inner, "#3e8a3a")}`;
    // jungle on the slope: palms and round trees cut out of the leather
    [[-150, -36, 0.8], [-90, -96, 1], [10, -104, 0.9], [80, -40, 0.75]].forEach(([x, y, k]) => {
      s += `<g transform="translate(${x},${y}) scale(${k})"><path d="M0,10Q-4,-50 4,-96" stroke="${LEA}" stroke-width="12" fill="none"/>
        ${[-160, -120, -70, -30, 20].map((a) => { const c = Math.cos(a * Math.PI / 180), sn = Math.sin(a * Math.PI / 180); return `<path d="M4,-96q${f1(44 * c)},${f1(44 * sn - 14)} ${f1(90 * c)},${f1(90 * sn + 14)}" stroke="${LEA}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M4,-96q${f1(44 * c)},${f1(44 * sn - 14)} ${f1(90 * c)},${f1(90 * sn + 14)}" stroke="#6ab85a" stroke-width="6" fill="none" stroke-linecap="round" opacity=".85"/>`; }).join("")}</g>`;
    });
    // the path up, a dashed line of light
    s += `<path d="M120,140Q40,110 -10,70Q-60,30 -30,-20Q0,-60 -40,-104" stroke="#f8e2a8" stroke-width="7" fill="none" stroke-dasharray="12 12" opacity=".75"/>`;
    return s;
  }
  // a Moken stilt hut on the beach at the foot of the hill: bamboo legs, a woven wall, a palm-thatch roof, a ladder
  const hutPuppet = () => `<path d="M-70,-30L0,-90L70,-30Z" fill="${LEA}"/>${weave("M-58,-34L0,-80L58,-34Z", "#d8b05a")}
    <rect x="-56" y="-34" width="112" height="56" fill="${LEA}"/>${weave("M-46,-26H46V14H-46Z", "#c8844a")}<rect x="-12" y="-20" width="24" height="34" fill="#fff4d0" opacity=".8"/>
    ${[-50, -18, 18, 50].map((x) => `<path d="M${x},22V110" stroke="${LEA}" stroke-width="9"/>`).join("")}<path d="M-60,60H60" stroke="${LEA}" stroke-width="6"/>
    <path d="M66,22L96,110M80,22L110,110" stroke="${LEA}" stroke-width="5"/>${[40, 60, 80].map((y) => `<path d="M${70 + (y - 22) * 0.34},${y}h18" stroke="${LEA}" stroke-width="4"/>`).join("")}`;
  // the kabang: a long dugout hull with the forked bow ("mouth") and stern, an arched pandanus roof amidships
  const kabang = () => `<path d="M-150,0Q-170,-6 -186,-26L-170,-10L-188,6Q-160,12 -140,20H150Q170,12 188,6L170,-10L186,-26Q170,-6 150,0Z" fill="${LEA}"/>
    ${weave("M-136,4H136L128,14H-128Z", "#8a5a2a", 0.9)}
    <path d="M-80,2Q-80,-70 0,-76Q80,-70 80,2Z" fill="${LEA}"/>${weave("M-68,0Q-68,-60 0,-66Q68,-60 68,0Z", "#d8b05a")}
    <path d="M-60,-30Q0,-44 60,-30M-64,-12Q0,-24 64,-12" stroke="${LEA}" stroke-width="3" fill="none" opacity=".6"/>
    <path d="M110,0L150,-60M150,-60l10,-10" stroke="${LEA}" stroke-width="5"/>`;
  function seaPuppet() {
    let s = `<path d="M-300,40Q-260,-20 -210,10Q-170,-30 -120,6Q-76,-34 -30,4Q10,-34 60,6Q104,-30 150,8Q194,-26 240,10L300,160H-310Z" fill="${LEA}"/>
      <path d="M-282,52Q-246,4 -210,30Q-170,-6 -120,28Q-78,-10 -30,26Q10,-10 60,28Q100,-6 150,30Q190,-2 230,32L284,148H-292Z" fill="#2a8ab8" opacity=".86"/>`;
    for (let row = 0; row < 3; row++) s += `<path d="M${-270 + row * 20},${74 + row * 26}${Array.from({ length: 11 }, () => " q12,-16 24,0 t24,0").join("")}" stroke="#bfe8f8" stroke-width="5" fill="none" opacity=".75"/>`;
    s += `<g transform="translate(-140,96)"><path d="M-26,0Q0,-18 26,0Q0,18 -26,0Z" fill="${LEA}"/><path d="M-20,0Q0,-12 20,0Q0,12 -20,0Z" fill="#f2c84a" opacity=".9"/><path d="M26,0l14,-12v24z" fill="${LEA}"/></g>
`;
    return s;
  }
  function sandPuppet() {
    return `<path d="M-320,30Q-140,0 40,14T420,10V110H-320Z" fill="${LEA}"/>${weave("M-310,40Q-140,12 40,24T410,20V100H-310Z", "#e8b860")}
      ${[[-220, 52], [-100, 46], [20, 54], [140, 46], [270, 52]].map(([x, y]) => `<path d="M${x - 8},${y}q8,-10 16,0q-8,6 -16,0z" fill="#fff4d0" opacity=".75"/>`).join("")}`;
  }
  const fishPuppet = (c) => `<path d="M-30,0Q0,-20 30,0Q0,20 -30,0Z" fill="${LEA}"/><path d="M-24,0Q0,-14 24,0Q0,14 -24,0Z" fill="${c}" opacity=".9"/><path d="M30,0l16,-14v28z" fill="${LEA}"/><circle cx="-14" cy="-2" r="4" fill="#fff4d0"/>`;
  // a Moken elder in profile facing the hill (left): a cloth headband, short white beard, bare chest, a woven sarong, a paddle;
  // the front arm (#id-arm, pivot at the shoulder) hangs, then swings up to point at the hilltop
  function elderPuppet() {
    return `<path d="M-30,-196Q-34,-236 -2,-244Q32,-246 38,-214Q40,-190 26,-176L30,-150Q44,-120 38,-30L46,110L40,196H-34L-40,110L-38,-30Q-50,-110 -30,-150L-30,-176Q-50,-176 -46,-190L-58,-196Z" fill="${LEA}"/>
      ${weave("M-24,-200Q-26,-230 -2,-236Q26,-238 30,-212Q32,-194 20,-182L-20,-182Q-34,-186 -34,-192Z", "#c8844a")}
      <path d="M-36,-226Q0,-246 38,-224L36,-212Q0,-232 -34,-214Z" fill="#c8402e"/><path d="M36,-222l18,10l-14,8Z" fill="#c8402e"/>
      <path d="M-32,-184Q-24,-160 -6,-156Q-2,-172 -12,-182Z" fill="#f4ead8" opacity=".9"/><circle cx="-16" cy="-206" r="4" fill="#fff4d0"/>
      ${weave("M-28,-140Q0,-152 30,-138L32,-34H-30Z", "#c8844a", 0.8)}
      ${weave("M-38,-30H40L44,110H-42Z", "#2e7a8a")}<path d="M-38,-30H40" stroke="#f2c84a" stroke-width="8"/>
      <path d="M-40,110L-46,200M38,110L44,200" stroke="${LEA}" stroke-width="16" stroke-linecap="round"/>
      <path d="M24,-136Q60,-60 52,20" stroke="${LEA}" stroke-width="16" fill="none" stroke-linecap="round"/>
      <path d="M64,-70L46,150" stroke="#5a3418" stroke-width="9" stroke-linecap="round"/><path d="M46,140Q22,170 34,214Q46,236 58,214Q70,170 46,140Z" fill="${LEA}"/><path d="M46,154Q32,176 40,206" stroke="#c8a050" stroke-width="4" fill="none" opacity=".8"/>`;
  }
  const elderArm = `<path d="M0,0Q-14,44 -10,104" stroke="${LEA}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M0,0Q-14,44 -10,104" stroke="#c8844a" stroke-width="8" fill="none" stroke-linecap="round" opacity=".85"/>
    <path d="M-10,104L-12,132" stroke="${LEA}" stroke-width="9" stroke-linecap="round"/><circle cx="-10" cy="104" r="9" fill="${LEA}"/>`;
  // the grandmother leading a child by the hand (facing left), her headcloth and sarong woven
  const grandma = () => `<circle cx="0" cy="-150" r="24" fill="${LEA}"/><path d="M-30,-160Q-4,-196 26,-160L24,-136Q0,-150 -26,-138Z" fill="#d8a02e" opacity=".9"/>
    <path d="M-22,-126Q0,-134 22,-126L28,-40H-28Z" fill="${LEA}"/>${weave("M-16,-120Q0,-126 16,-120L21,-46H-21Z", "#c8402e")}
    <path d="M-30,-40H30L36,80H-36Z" fill="${LEA}"/>${weave("M-24,-34H24L28,72H-28Z", "#d8a02e")}
    <path d="M-28,80L-40,130M28,80L36,130" stroke="${LEA}" stroke-width="12" stroke-linecap="round"/>
    <path d="M-16,-110L-56,-80M18,-110L58,-60" stroke="${LEA}" stroke-width="11" stroke-linecap="round"/>
    <g transform="translate(76,-30)">${childShape("#2a8ab8", 0.62)}</g>`;
  function childShape(c, k = 1) {
    return `<g transform="scale(${k})"><circle cx="0" cy="-118" r="20" fill="${LEA}"/><circle cx="-2" cy="-118" r="12" fill="#c8844a" opacity=".85"/>
      <path d="M-18,-96Q0,-104 18,-96L22,-30H-22Z" fill="${LEA}"/>${weave("M-12,-90Q0,-96 12,-90L15,-36H-15Z", c)}
      <path d="M-16,-30L-34,10L-24,40M14,-30L30,4L46,30" stroke="${LEA}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M-14,-86L-44,-100M14,-86L40,-60" stroke="${LEA}" stroke-width="10" stroke-linecap="round"/></g>`;
  }
  // ละบูน: one wave built of seven stacked crests, each curling forward (left) over the one below
  function wavePuppet() {
    let s = `<path d="M-170,270Q-196,120 -150,0Q-104,-150 -24,-262Q36,-318 112,-296L156,-240Q176,-60 176,270Z" fill="${LEA}"/>
      ${weave("M-148,260Q-172,120 -128,6Q-86,-132 -12,-240Q40,-288 104,-276L136,-232Q156,-60 156,260Z", "#1e5a8a", 0.88)}`;
    for (let k = 0; k < 7; k++) {
      const y = 236 - k * 74, w = 262 - k * 18, x = 70 - k * 24;
      const d = `M${f1(x + w * 0.42)},${f1(y + 20)}Q${f1(x)},${f1(y - 70)} ${f1(x - w * 0.56)},${f1(y - 34)}Q${f1(x - w * 0.78)},${f1(y - 16)} ${f1(x - w * 0.64)},${f1(y + 10)}Q${f1(x - w * 0.54)},${f1(y - 14)} ${f1(x - w * 0.36)},${f1(y - 6)}Q${f1(x - w * 0.08)},${f1(y + 6)} ${f1(x + w * 0.42)},${f1(y + 34)}Z`;
      s += `<g id="__CREST${k}__"><path d="${d}" fill="#eaf8ff" stroke="${LEA}" stroke-width="12" stroke-linejoin="round"/>
        <path d="M${f1(x - w * 0.5)},${f1(y - 20)}Q${f1(x - w * 0.2)},${f1(y - 44)} ${f1(x + w * 0.2)},${f1(y - 20)}" stroke="#5ab8e0" stroke-width="5" fill="none" opacity=".75"/>
        ${[0.05, 0.22, 0.4].map((q) => `<circle cx="${f1(x - w * q)}" cy="${f1(y - 8 - q * 30)}" r="5" fill="${LEA}" opacity=".55"/>`).join("")}</g>`;
    }
    s += `${[[-120, -300], [-80, -330], [-30, -340], [20, -328]].map(([x, y], k) => `<circle cx="${x}" cy="${y}" r="${10 - k}" fill="#eaf8ff" stroke="${LEA}" stroke-width="5"/>`).join("")}`;
    return s;
  }
  function tideLegend(L, o = {}) {
    const id = o.id || "tlg", R = mkR(o.seed || 23), CX = 540, top = 300, bot = 1460, W = 940, x0 = CX - W / 2, x1 = CX + W / 2;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#0a0604"/>`);
    put(L.far, `<rect x="-1300" y="1500" width="3700" height="1200" fill="#140c06"/>`);
    let s = "";
    // the stage: a thatched eave, a woven pandanus valance with its fringe, the cloth screen in a sea-patterned border
    s += `<path d="M${x0 - 120},${top - 200}H${x1 + 120}L${x1 + 60},${top - 90}H${x0 - 60}Z" fill="#2a1a0e" stroke="#120a04" stroke-width="5"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${x0 - 100 + k * 90},${top - 200}L${x0 - 60 + k * 90},${top - 92}" stroke="#4a301a" stroke-width="6"/>`).join("")}
      <rect x="${x0 - 60}" y="${top - 90}" width="${W + 120}" height="76" fill="url(#tuValance)" stroke="#5a3a12" stroke-width="4"/>
      ${Array.from({ length: 36 }, (_, k) => `<path d="M${x0 - 54 + k * 30},${top - 14}l6,${18 + (k % 3) * 5}" stroke="#c8a050" stroke-width="5" stroke-linecap="round"/>`).join("")}
      <rect x="${x0 - 40}" y="${top - 40}" width="${W + 80}" height="${bot - top + 80}" fill="url(#tuBorder)" stroke="#0a2a34" stroke-width="5"/>
      <g id="${id}-scr"><rect x="${x0}" y="${top}" width="${W}" height="${bot - top}" fill="url(#tuScreen)"/></g>
      <g id="${id}-hot"><ellipse cx="${CX}" cy="${top + 520}" rx="300" ry="360" fill="url(#tuHot)"/></g>`;
    for (let k = 0; k < 8; k++) s += `<path d="M${x0 + 60 + k * 118 + (R() - 0.5) * 20},${top}Q${x0 + 66 + k * 118},${(top + bot) / 2} ${x0 + 54 + k * 118},${bot}" stroke="#a8743a" stroke-width="3" fill="none" opacity=".18"/>`;
    // the puppets pressed to the cloth (clipped to it): back to front
    const wave = wavePuppet().replace(/__CREST(\d)__/g, (_, k) => `${id}-wc${k}`);
    s += `<defs><clipPath id="${id}-clip"><rect x="${x0}" y="${top}" width="${W}" height="${bot - top}"/></clipPath></defs><g clip-path="url(#${id}-clip)" opacity=".94"><g transform="translate(${CX},${bot}) scale(1.2) translate(${-CX},${-bot})">
      <g transform="translate(${CX + 250},${bot - 330})"><g id="${id}-wave" opacity="0">${wave}${rod(0, 260, 160)}</g></g>
      <g transform="translate(${CX + 90},${bot - 250})"><g id="${id}-sand">${sandPuppet()}
        <g transform="translate(70,44)"><g id="${id}-fishA">${fishPuppet("#8ac8e8")}</g></g><g transform="translate(260,48) scale(-1,1)"><g id="${id}-fishB">${fishPuppet("#f2c84a")}</g></g></g></g>
      <g transform="translate(${CX + 290},${bot - 300})"><g id="${id}-sea">${seaPuppet()}${rod(0, 160, 160)}</g></g>
      <g transform="translate(${CX + 330},${bot - 318})"><g id="${id}-boat"><g id="${id}-boatIn"><g transform="scale(.62)">${kabang()}</g></g>${rod(0, 14, 300)}</g></g>
      <g transform="translate(${CX - 200},${bot - 430})"><g id="${id}-hill">${hillPuppet()}${rod(-30, 150, 290)}</g></g>
      <g transform="translate(${CX - 120},${bot - 300})"><g id="${id}-hut">${hutPuppet()}${rod(0, 110, 200)}</g></g>
      ${[["#c8402e", 0], ["#d8a02e", 1]].map(([c, k]) => `<g transform="translate(${CX - 40 + k * 70},${bot - 236})"><g id="${id}-v${k}"><g class="tuVb">${childShape(c, k ? 0.66 : 0.72)}</g>${rod(0, 40, 260)}</g></g>`).join("")}
      <g transform="translate(${CX + 100},${bot - 250})"><g id="${id}-v2"><g class="tuVb"><g transform="scale(.82)">${grandma()}</g></g>${rod(0, 107, 200)}</g></g>
      <g transform="translate(${CX + 210},${bot - 286})"><g id="${id}-elder"><g transform="scale(.8)">${elderPuppet()}<g transform="translate(-26,-136)"><g id="${id}-arm">${elderArm}</g></g></g>${rod(0, 157, 200)}<path d="M-10,83L-90,330" stroke="#3a1e0e" stroke-width="5" opacity=".8"/></g></g></g></g>`;
    // the banana trunk the rods stand in, under the screen
    s += `<g transform="translate(${CX},${bot + 44})"><rect x="${-W / 2 - 60}" y="-34" width="${W + 120}" height="72" rx="36" fill="url(#tuBanana)" stroke="#2a3a14" stroke-width="5"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-W / 2 + k * (W / 8)},-32V36" stroke="#5a7a34" stroke-width="3" opacity=".5"/>`).join("")}
      <path d="M${-W / 2 - 40},-18H${W / 2 + 40}" stroke="#f4fadc" stroke-width="5" opacity=".55"/></g>`;
    if (o.title) { const bw = Math.max(170, plain(o.title).length * 15 + 50), fs = plain(o.title).length > 12 ? 42 : 56, ban = `M${-bw},-38H${bw}L${bw - 16},40Q0,56 ${-bw + 16},40Z`;
      s += `<g transform="translate(${CX},${top - 50})"><path d="${ban}" fill="#000" opacity=".3" transform="translate(6,8)"/><path d="${ban}" fill="#f2e2c0" stroke="#5a3a12" stroke-width="4"/>
        <path d="M${-bw + 20},-26H${bw - 20}" stroke="#c8a050" stroke-width="3" stroke-dasharray="8 6"/>
        <text y="20" text-anchor="middle" font-family="Sriracha" font-size="${fs}" fill="#1e3a5a">${o.title}</text></g>`; }
    put(L.set, s);
    // the warm light spilling round the screen, moths circling the bulb
    let gl = `<ellipse cx="${CX}" cy="${top + 560}" rx="760" ry="860" fill="url(#tuSpill)" style="mix-blend-mode:screen"/>`;
    for (let k = 0; k < 6; k++) gl += `<g id="${id}-mo${k}" transform="translate(${f1(CX + (R() - 0.5) * 500)},${f1(top + 200 + R() * 500)})"><path d="M0,0q-8,-6 -12,2q6,4 12,-2q8,-6 12,2q-6,4 -12,-2" fill="#2a1a10" opacity=".55"/></g>`;
    put(L.glow, gl);
  }
  function legendAnim(tl, id, t0, dur, o = {}) {
    const [ra, rb] = o.recede || [0.6, 2.4], [pa, pb] = o.point || [1.6, 2.4], [va, vb] = o.run || [2.6, dur - 0.4];
    // every puppet trembles a little on its rod (held by hand behind the screen)
    [["hill", 0.9, 0.8], ["sea", 0.7, 1.4], ["boat", 0.8, 1.6], ["elder", 0.6, 1.6], ["sand", 1.1, 0.5], ["hut", 1.3, 0.6]].forEach(([n, per, a], k) => tl.fromTo(`#${id}-${n}`, { rotation: -a, svgOrigin: "0 140" }, { rotation: a, svgOrigin: "0 140", duration: per, repeat: Math.ceil(dur / per), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + k * 0.1));
    tl.fromTo(`#${id}-hot`, { opacity: 0.85, scale: 1, svgOrigin: "540 820" }, { opacity: 1, scale: 1.04, svgOrigin: "540 820", duration: 0.13, repeat: Math.ceil(dur / 0.13), yoyo: true, ease: "none", immediateRender: false }, t0);
    // the sea drops away off the sand and leaves the kabang lying tilted on it, the stranded fish flap
    tl.fromTo(`#${id}-sea`, { x: 0, y: 0 }, { x: 330, y: 70, duration: rb - ra, ease: "power2.inOut", immediateRender: false }, t0 + ra);
    tl.fromTo(`#${id}-boatIn`, { y: 0, rotation: 0, svgOrigin: "0 10" }, { y: 54, rotation: 9, svgOrigin: "0 10", duration: (rb - ra) * 0.8, ease: "bounce.out", immediateRender: false }, t0 + ra + 0.2);
    ["fishA", "fishB"].forEach((f, k) => tl.fromTo(`#${id}-${f}`, { rotation: -16, svgOrigin: "0 0" }, { rotation: 16, svgOrigin: "0 0", duration: 0.18 + k * 0.05, repeat: Math.ceil(dur / 0.18), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + ra + 0.4));
    // the elder's arm swings up to point at the hilltop, and jabs
    tl.fromTo(`#${id}-arm`, { rotation: 0, svgOrigin: "0 0" }, { rotation: 140, svgOrigin: "0 0", duration: pb - pa, ease: "back.out(1.6)", immediateRender: false }, t0 + pa);
    tl.fromTo(`#${id}-arm`, { rotation: 140, svgOrigin: "0 0" }, { rotation: 128, svgOrigin: "0 0", duration: 0.22, repeat: Math.ceil(Math.max(0.3, dur - pb) / 0.22), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + pb);
    // the grandmother leads the children up the hill path; the elder follows last
    [[0, -360, -330], [1, -390, -300], [2, -450, -320]].forEach(([k, dx, dy]) => {
      tl.fromTo(`#${id}-v${k}`, { x: 0, y: 0 }, { x: dx, y: dy, duration: vb - va, ease: "power1.in", immediateRender: false }, t0 + va + (2 - k) * 0.15);
      document.getElementById(`${id}-v${k}`)?.querySelectorAll(".tuVb").forEach((e) => tl.fromTo(e, { y: 0, rotation: -6, svgOrigin: "0 40" }, { y: -14, rotation: 6, svgOrigin: "0 40", duration: 0.17, repeat: Math.ceil(dur / 0.17), yoyo: true, ease: "power1.out", immediateRender: false }, t0 + va));
    });
    if (o.elderGo !== false) tl.fromTo(`#${id}-elder`, { x: 0, y: 0 }, { x: -150, y: -170, duration: Math.max(0.6, vb - va - 1.2), ease: "power1.in", immediateRender: false }, t0 + va + 1.2);
    // ละบูน: the seven crests stack up one on another, then the whole wave leans in
    if (o.wave !== undefined) {
      const tw = t0 + o.wave;
      tl.set(`#${id}-wave`, { opacity: 1 }, tw);
      for (let k = 0; k < 7; k++) {
        tl.set(`#${id}-wc${k}`, { opacity: 0 }, t0);
        tl.fromTo(`#${id}-wc${k}`, { opacity: 0, scaleY: 0.1, svgOrigin: `${70 - k * 24} ${256 - k * 74}` }, { opacity: 1, scaleY: 1, svgOrigin: `${70 - k * 24} ${256 - k * 74}`, duration: 0.4, ease: "back.out(2.4)", immediateRender: false }, tw + k * 0.14);
      }
      tl.fromTo(`#${id}-wave`, { y: 160 }, { y: 0, duration: 0.9, ease: "power2.out", immediateRender: false }, tw);
      tl.fromTo(`#${id}-boatIn`, { x: 0, y: 54, rotation: 9, svgOrigin: "0 10" }, { x: -70, y: -60, rotation: -24, svgOrigin: "0 10", duration: 0.7, ease: "back.out(2)", immediateRender: false }, tw + 0.5);
      tl.fromTo(`#${id}-wave`, { rotation: 0, svgOrigin: "0 260" }, { rotation: -7, svgOrigin: "0 260", duration: 0.75, repeat: Math.ceil(dur / 0.75), yoyo: true, ease: "sine.inOut", immediateRender: false }, tw + 1);
    }
    for (let k = 0; k < 6; k++) tl.fromTo(`#${id}-mo${k}`, { rotation: 0, svgOrigin: "540 820" }, { rotation: k % 2 ? -360 : 360, svgOrigin: "540 820", duration: 3 + k * 0.6, repeat: Math.ceil(dur / 3), ease: "none", immediateRender: false }, t0);
  }


  // ---------------- the waves come as a series (EP.2): the train, then the heights at one beach in 2547 ----------------
  // painted on a driftwood board hung on two ropes (the rule board's language), the scene inside a rope-framed window.
  // A crest is drawn as a turbulent bore: a ragged churned top, a steep front with foam rolling down it and spray thrown forward,
  // never a surf curl (NOAA: "Tsunamis rarely become great towering breaking waves").
  const crest = (w, h, seed) => {
    const r = mkR(seed), n = Math.max(7, Math.round(w / 26)), top = [];
    for (let k = 0; k <= n; k++) { const u = k / n; top.push([-w + w * u, -h * Math.pow(Math.sin(Math.min(1, u * 1.08) * Math.PI / 2), 1.6) + (k && k < n ? (r() - 0.5) * h * 0.16 : 0)]); }
    const front = [[6, -h * 0.72], [16, -h * 0.4], [w * 0.1 + 14, 0]];
    // the hump is the sea itself lifted: no outline along its foot, its fill runs a little under the surface line
    const edge = `M${-w},0 ` + top.map(([a, b]) => `L${f1(a)},${f1(b)}`).join(" ") + " " + front.map(([a, b]) => `L${f1(a)},${f1(b)}`).join(" "), body = `${edge} L${f1(w * 0.1 + 14)},8 L${-w},8 Z`;
    let foam = "";
    for (let k = 1; k < n; k++) { const [a, b] = top[k]; if (a > -w * 0.55) foam += `<circle cx="${f1(a)}" cy="${f1(b + 3)}" r="${f1(5 + r() * 7 + h * 0.05)}" fill="#f4fbff"/>`; }
    for (let k = 0; k < 4; k++) foam += `<circle cx="${f1(8 + k * 7 + r() * 6)}" cy="${f1(-h * (0.68 - k * 0.17))}" r="${f1(5 + r() * 5)}" fill="#f4fbff"/>`;
    const spray = Array.from({ length: 7 }, () => `<circle cx="${f1(14 + r() * 34)}" cy="${f1(-h * (0.5 + r() * 0.55))}" r="${f1(2 + r() * 3.2)}" fill="#e8f8ff" opacity="${f1(0.55 + r() * 0.4)}"/>`).join("");
    const churn = Array.from({ length: 4 }, (_, k) => { const x = -w * (0.78 - k * 0.17); return `<path d="M${f1(x)},${f1(-h * 0.06)}Q${f1(x + w * 0.06)},${f1(-h * 0.3)} ${f1(x + w * 0.16)},${f1(-h * (0.42 + k * 0.08))}" stroke="${k % 2 ? "#d8f0ff" : "#1e4ea0"}" stroke-width="${k % 2 ? 3 : 4}" fill="none" opacity="${k % 2 ? 0.55 : 0.4}" stroke-linecap="round"/>`; }).join("");
    return `<path d="${body}" fill="url(#tuBoreG)"/><path d="${edge}" stroke="${INK}" stroke-width="4" stroke-linejoin="round" fill="none"/>${churn}<g class="tuFoam">${foam}</g>${spray}`;
  };
  Sets.DEFS += `<linearGradient id="tuBoreG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ac4f4"/><stop offset=".4" stop-color="#5a9ae6"/><stop offset="1" stop-color="#3a7ad8"/></linearGradient>
    <linearGradient id="tuFloodG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a9a90" stop-opacity=".8"/><stop offset=".5" stop-color="#4a7470" stop-opacity=".82"/><stop offset="1" stop-color="#2e4a4c" stop-opacity=".88"/></linearGradient>
    <linearGradient id="tuSkyP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe4f4"/><stop offset="1" stop-color="#f4f8ee"/></linearGradient>
    <linearGradient id="tuGroundP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8d2a0"/><stop offset="1" stop-color="#c8a870"/></linearGradient>
    <linearGradient id="tuHotelF" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fbf8f0"/><stop offset=".7" stop-color="#ece6d8"/><stop offset="1" stop-color="#d2cab8"/></linearGradient>
    <pattern id="tuHaz" width="56" height="56" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="56" height="56" fill="#ffd23a"/><rect width="28" height="56" fill="#1e1a16"/></pattern>`;
  function seriesBoard(id, X, Y0, W, H, title) {
    const outline = boardPath(X, Y0, W, H, 31), ts = Math.min(80, Math.floor((W - 170) / (emW(title) * 0.95))), uw = Math.min(400, emW(title) * 0.95 * ts / 2);
    return `${rope(X + 130, -40, Y0 + 24)}${rope(X + W - 130, -40, Y0 + 24)}
      <path d="${outline}" fill="url(#tuWoodSide)" stroke="${INK}" stroke-width="5" transform="translate(0,16)"/>
      <path d="${outline}" fill="url(#tuWood)" stroke="${INK}" stroke-width="5"/>
      <defs><clipPath id="${id}-bc"><path d="${outline}"/></clipPath></defs>
      <g clip-path="url(#${id}-bc)">${grain(X, Y0, W, H, 41, { knots: 3, stains: 4 })}<rect x="${X}" y="${Y0}" width="${W}" height="40" fill="#fff" opacity=".12"/></g>
      ${[[X + 130, Y0 + 26], [X + W - 130, Y0 + 26]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="12" fill="#5a3a22" ${OUT(2)}/><circle cx="${a}" cy="${b}" r="6" fill="#2a1a10"/>`).join("")}
      <g transform="translate(540,${Y0 + 104})"><g id="${id}-ti">
        <text y="18" text-anchor="middle" font-family="Sriracha" font-size="${ts}" fill="#fffaf0" stroke="#fffaf0" stroke-width="16" stroke-linejoin="round">${title}</text>
        <text y="18" text-anchor="middle" font-family="Sriracha" font-size="${ts}" fill="#d8312a">${title}</text>
        <path d="M${f1(-uw)},42Q0,56 ${f1(uw)},42" stroke="#d8312a" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/></g></g>`;
  }
  // the painted window inside the board: a rope frame around a rounded scene
  const windowFrame = (x, y, w, h) => `<rect x="${x - 10}" y="${y - 10}" width="${w + 20}" height="${h + 20}" rx="30" fill="none" stroke="${INK}" stroke-width="14"/><rect x="${x - 10}" y="${y - 10}" width="${w + 20}" height="${h + 20}" rx="30" fill="none" stroke="url(#tuRope)" stroke-width="9"/>
    <path d="${Array.from({ length: Math.ceil((w + 20) / 18) }, (_, k) => `M${x - 6 + k * 18},${y - 14}l9,8`).join("")}" stroke="#7a5a2a" stroke-width="2.4" opacity=".6"/>`;
  function series(tl, layer, t0, dur, o = {}) {
    const id = nid(), phase = o.phase || "train", Y0 = o.y ?? 230, X = 54, W = 972, H = 1180;   // the board spans x 48–1030 (±8 swaying)
    const wx = 80, wy = Y0 + 186, ww = 920, wh = H - 228;   // the painted window (y 416 … 1368 at the default o.y)
    const title = o.title || (phase === "heights" ? "ปี 2547 · ชายหาดแห่งหนึ่ง" : "สึนามิไม่ได้มาลูกเดียว");
    let scene = "";
    const R = mkR(phase === "heights" ? 61 : 53);
    const mount = () => {
      put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">${seriesBoard(id, X, Y0, W, H, title)}
        <defs><clipPath id="${id}-wc"><rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" rx="22"/></clipPath></defs>
        <g clip-path="url(#${id}-wc)"><g id="${id}-sc">${scene}</g></g>${windowFrame(wx, wy, ww, wh)}</g></g></g>`);
      boardIn(tl, id, t0, dur, Y0);
    };
    if (phase === "train") {
      const SL = wy + 560, at = o.at || [0.3, 0.9, 1.5, 2.2], shoreX = wx + 740;
      // sky with two clouds, the sea, the seabed rising to the shore, the coast: a beach, palms, the hotel, the hill
      scene += `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="url(#tuSkyP)"/>
        ${[[wx + 150, wy + 96, 0.9], [wx + 640, wy + 70, 0.7]].map(([cx, cy, s]) => `<g transform="translate(${cx},${cy}) scale(${s})"><path d="M-90,20Q-90,-14 -54,-16Q-44,-46 -6,-42Q26,-60 54,-30Q92,-30 92,6Q92,24 70,24H-74Q-90,24 -90,20Z" fill="#fff" stroke="#9ab8c8" stroke-width="3"/></g>`).join("")}
        <path d="M${wx},${SL}H${shoreX + 10}L${wx + ww},${SL - 60}V${wy + wh}H${wx}Z" fill="url(#tuDeepG)"/>
        <path d="M${wx},${wy + wh - 30}C${wx + 300},${wy + wh - 50} ${wx + 560},${SL + 210} ${shoreX - 60},${SL + 40}L${shoreX + 10},${SL}L${wx + ww},${SL - 60}V${wy + wh}H${wx}Z" fill="#c8a870" ${OUT(3)}/>
        <path d="M${wx},${wy + wh - 30}C${wx + 300},${wy + wh - 50} ${wx + 560},${SL + 210} ${shoreX - 60},${SL + 40}" stroke="#e8d2a0" stroke-width="5" fill="none" opacity=".6"/>
        <path d="M${shoreX - 30},${SL + 2}L${wx + ww},${SL - 62}V${SL + 40}L${shoreX + 40},${SL + 18}Z" fill="url(#tuGroundP)"/>
        <path d="M${wx + 820},${SL - 50}Q${wx + 860},${SL - 250} ${wx + 940},${SL - 300}Q${wx + 920},${SL - 160} ${wx + ww},${SL - 120}V${SL - 56}Z" fill="url(#tuHillG)" ${OUT(3)}/>
        <g transform="translate(${shoreX + 44},${SL - 16})"><rect x="-20" y="-96" width="44" height="96" fill="url(#tuHotelF)" ${OUT(2.6)}/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-20,${-19 * k}H24" stroke="${INK}" stroke-width="1.4"/><rect x="-12" y="${-17 - 19 * k}" width="8" height="9" fill="#7ab4e0"/><rect x="6" y="${-17 - 19 * k}" width="8" height="9" fill="#7ab4e0"/>`).join("")}</g>
        ${[[shoreX + 8, SL - 4, 0.7], [shoreX + 112, SL - 34, 0.8]].map(([px, py, s]) => `<g transform="translate(${px},${py}) scale(${s})"><path d="M0,0Q6,-50 -6,-96" stroke="#7a5a3a" stroke-width="7" fill="none"/>${[-150, -100, -50, 0, 40].map((a) => `<path d="M-6,-96q${f1(30 * Math.cos(a * Math.PI / 180))},${f1(30 * Math.sin(a * Math.PI / 180) - 10)} ${f1(56 * Math.cos(a * Math.PI / 180))},${f1(56 * Math.sin(a * Math.PI / 180) + 12)}" stroke="#3e8a44" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}</g>`).join("")}
        <path d="M${wx},${SL}H${shoreX}" stroke="#bff2ff" stroke-width="4" opacity=".8"/>
        ${Array.from({ length: 10 }, () => `<path d="M${f1(wx + 30 + R() * 640)},${f1(SL + 40 + R() * 160)}h${f1(30 + R() * 40)}" stroke="#7ab4f0" stroke-width="3" opacity=".45" stroke-linecap="round"/>`).join("")}
        <text x="${wx + 36}" y="${SL + 150}" font-family="Kanit" font-weight="700" font-size="32" fill="#e8f4ff" opacity=".9">ทะเลลึก</text>
        <g id="${id}-dir" opacity=".4">${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${wx + 60 + k * 96},${SL + 40}l22,22l-22,22" stroke="#e8f8ff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`).join("")}</g>
        <g transform="translate(${shoreX + 70},${SL + 70})"><path d="M-40,0H24M10,-14L26,0L10,14" stroke="#fffaf0" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><text x="34" y="11" font-family="Kanit" font-weight="800" font-size="32" fill="#fffaf0" stroke="${INK}" stroke-width="5" paint-order="stroke">ฝั่ง</text></g>`;
      // three crests, the one nearest the coast first; the later ones bigger (the first is often not the largest)
      const CR = [[shoreX - 60, 170, 70], [shoreX - 320, 220, 110], [shoreX - 580, 260, 150]];
      CR.forEach(([x, w, h], k) => { scene += `<g transform="translate(${x},${SL})"><g id="${id}-k${k}" opacity="0"><g id="${id}-kw${k}">${crest(w, h, 70 + k)}</g></g></g>`; });
      // the gaps: a bracket between each pair of crests with a clock on it, one label over both
      const by = SL - 214;
      const br = (x0, x1, k) => `<g id="${id}-g${k}" opacity="0"><path d="M${x0 + 10},${by}H${x1 - 10}" stroke="${INK}" stroke-width="10" stroke-linecap="round"/><path d="M${x0 + 10},${by}H${x1 - 10}" stroke="#ffd23a" stroke-width="5" stroke-linecap="round"/>
        <path d="M${x0 + 26},${by - 14}L${x0 + 8},${by}L${x0 + 26},${by + 14}M${x1 - 26},${by - 14}L${x1 - 8},${by}L${x1 - 26},${by + 14}" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <g transform="translate(${(x0 + x1) / 2},${by})"><circle r="26" fill="#fffaf0" ${OUT(4)}/><path d="M0,-14V0L10,7" stroke="${INK}" stroke-width="4" fill="none" stroke-linecap="round"/><g class="tuHand"><path d="M0,0V-17" stroke="#d8312a" stroke-width="3" stroke-linecap="round"/></g></g></g>`;
      scene += br(CR[2][0], CR[1][0], 0) + br(CR[1][0], CR[0][0], 1);
      const gap = o.gap || "ห่างกัน <u>5 นาที – 2 ชั่วโมง</u>", gw = Math.round(emW(gap) * 46 + 80), lx = (CR[2][0] + CR[0][0]) / 2, ly = by - 136;
      scene += `<g id="${id}-gl" opacity="0"><path d="M${lx - 40},${ly + 40}L${(CR[2][0] + CR[1][0]) / 2},${by - 28}M${lx + 40},${ly + 40}L${(CR[1][0] + CR[0][0]) / 2},${by - 28}" stroke="${INK}" stroke-width="4" stroke-dasharray="10 8" opacity=".7"/>
        <g transform="translate(${lx},${ly})"><g id="${id}-gp">${slab(-gw / 2, -42, gw, 84, 42, { face: "url(#tuNote)", body: "#8a6e4c", d: 9 })}
          <text y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#1e2a3a">${gap.replace(/<u>(.*?)<\/u>/g, `<tspan fill="#d8312a">$1</tspan>`)}</text></g></g></g>`;
      mount();
      CR.forEach((_, k) => {
        const ta = t0 + at[k];
        tl.fromTo(`#${id}-k${k}`, { opacity: 0, x: -620 }, { opacity: 1, x: 0, duration: 1.0, ease: "power2.out", immediateRender: false }, ta);
        tl.fromTo(`#${id}-kw${k}`, { scaleX: 0.8, scaleY: 0.6, svgOrigin: "0 0" }, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 1.1, ease: "back.out(1.6)", immediateRender: false }, ta);
        // keep rolling in: a slow drift toward the coast and a churning top
        tl.fromTo(`#${id}-k${k}`, { x: 0 }, { x: 26, duration: Math.max(0.5, dur - at[k] - 1.0), ease: "none", immediateRender: false }, ta + 1.0);
        tl.fromTo(`#${id}-kw${k}`, { scaleY: 1, svgOrigin: "0 0" }, { scaleY: 1.07, svgOrigin: "0 0", duration: 0.45, repeat: Math.ceil(dur / 0.45), yoyo: true, ease: "sine.inOut", immediateRender: false }, ta + 1.1);
      });
      tl.fromTo(`#${id}-dir`, { x: -40 }, { x: 56, duration: 0.9, repeat: Math.ceil(dur / 0.9), ease: "none", immediateRender: false }, t0);
      const tg = t0 + at[3];
      [0, 1].forEach((k) => {
        const ox = `${(CR[2 - k][0] + CR[1 - k][0]) / 2} ${by}`;
        tl.fromTo(`#${id}-g${k}`, { opacity: 0, scaleX: 0.2, svgOrigin: ox }, { opacity: 1, scaleX: 1, svgOrigin: ox, duration: 0.5, ease: "back.out(2.2)", immediateRender: false }, tg + k * 0.15);
        document.getElementById(`${id}-g${k}`).querySelectorAll(".tuHand").forEach((h) => tl.fromTo(h, { rotation: 0, svgOrigin: "0 0" }, { rotation: 360, svgOrigin: "0 0", duration: 1.2, repeat: Math.ceil(dur / 1.2), ease: "none", immediateRender: false }, tg));
      });
      tl.fromTo(`#${id}-gl`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, tg + 0.3);
      tl.fromTo(`#${id}-gp`, { scale: 0.3, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "elastic.out(1, 0.5)", immediateRender: false }, tg + 0.3);
      tl.fromTo(`#${id}-gp`, { y: 0 }, { y: -6, duration: 0.8, repeat: Math.ceil(dur / 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, tg + 0.9);
    } else {
      // heights: one fixed scale (1 m = K px) on the ground G; a person (1.7 m), a one-storey house, the 5-storey hotel (3 m a storey)
      const K = 50, G = wy + wh - 64, at = o.at || [0.6, 2.4, 4.2], HM = o.h || [2.5, 6.5, 11];
      const tags = o.tags || ["09:38 · 2–3 ม.", "09:43 · 6–7 ม.", "10:03 · เกิน 10 ม."], TC = ["#2a9ca6", "#e8823a", "#d8312a"];
      const yM = (m) => G - m * K, hx = wx + 300, hw = 210;
      scene += `<rect x="${wx}" y="${wy}" width="${ww}" height="${wh}" fill="url(#tuSkyP)"/>
        <g transform="translate(${wx + 740},${wy + 110}) scale(.8)"><path d="M-90,20Q-90,-14 -54,-16Q-44,-46 -6,-42Q26,-60 54,-30Q92,-30 92,6Q92,24 70,24H-74Q-90,24 -90,20Z" fill="#fff" stroke="#9ab8c8" stroke-width="3"/></g>
        <rect x="${wx}" y="${G}" width="${ww}" height="${wy + wh - G}" fill="url(#tuGroundP)"/><path d="M${wx},${G}H${wx + ww}" stroke="${INK}" stroke-width="4"/>`;
      // the hotel: 5 storeys with windows, the roof railing and the flag (its floor badges go on top of the water, below)
      let hotel = `<rect x="${hx + 8}" y="${yM(15)}" width="${hw}" height="${15 * K}" fill="#000" opacity=".15"/><rect x="${hx}" y="${yM(15)}" width="${hw}" height="${15 * K}" fill="url(#tuHotelF)" ${OUT(4)}/>`;
      for (let f = 0; f < 5; f++) {
        const yb = yM(3 * f);
        hotel += `<path d="M${hx},${f1(yb)}H${hx + hw}" stroke="${INK}" stroke-width="${f ? 3 : 0}"/>`;
        for (let j = 0; j < 2; j++) hotel += `<rect x="${hx + 96 + j * 56}" y="${f1(yb - 3 * K + 32)}" width="40" height="${f1(3 * K - 62)}" fill="#7ab4e0" stroke="${INK}" stroke-width="2.4"/><path d="M${hx + 102 + j * 56},${f1(yb - 3 * K + 38)}l12,20" stroke="#fff" stroke-width="3" opacity=".6"/>`;
      }
      hotel += `<path d="M${hx - 6},${yM(15)}H${hx + hw + 6}V${yM(15) - 12}H${hx - 6}Z" fill="#c2baae" ${OUT(2.4)}/>${Array.from({ length: 9 }, (_, k) => `<path d="M${f1(hx + k * hw / 8)},${yM(15) - 12}V${yM(15) - 38}" stroke="#8a929a" stroke-width="3"/>`).join("")}<path d="M${hx},${yM(15) - 38}H${hx + hw}" stroke="#8a929a" stroke-width="4"/>
        <path d="M${hx + hw - 30},${yM(15) - 38}V${yM(15) - 100}" stroke="#6a6a6a" stroke-width="4"/><path d="M${hx + hw - 30},${yM(15) - 100}h40v30h-40Z" fill="#e8392c"/><path d="M${hx + hw - 30},${yM(15) - 94}h40v18h-40Z" fill="#fff"/><path d="M${hx + hw - 30},${yM(15) - 89}h40v8h-40Z" fill="#2a4aa8"/>`;
      const badges = Array.from({ length: 5 }, (_, f) => `<g transform="translate(${hx + 44},${f1(yM(3 * f) - 1.5 * K)})"><circle r="30" fill="#fffaf0" ${OUT(3)}/><text y="-2" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="17" fill="#5a4a3a">ชั้น</text><text y="21" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="24" fill="#1e2a3a">${f + 1}</text></g>`).join("");
      // the house (x 240 … 350): a wall ~2.6 m, a tin roof to ~4.2 m · the person (1.7 m) between the scale and the house
      const house = `<rect x="${wx + 160}" y="${yM(2.6)}" width="110" height="${2.6 * K}" fill="#e2cca4" ${OUT(3)}/><rect x="${wx + 176}" y="${yM(2.0)}" width="34" height="${2.0 * K}" fill="#8a5a3a" ${OUT(2.4)}/><rect x="${wx + 224}" y="${yM(2.0)}" width="32" height="32" fill="#7ab4e0" ${OUT(2.4)}/>
        <path d="M${wx + 146},${yM(2.6)}L${wx + 215},${yM(4.2)}L${wx + 284},${yM(2.6)}Z" fill="#a8b4bc" ${OUT(3)}/><path d="M${wx + 170},${yM(3.0)}L${wx + 215},${yM(3.9)}M${wx + 196},${yM(2.8)}L${wx + 228},${yM(3.7)}" stroke="#d8e0e6" stroke-width="3" opacity=".7"/>`;
      const px = wx + 124, person = `<g transform="translate(${px},${G})"><circle cx="0" cy="${-1.7 * K + 9}" r="9" fill="url(#tuHead)" ${OUT(2)}/><path d="M-9,${-1.7 * K + 20}H9L7,${-0.85 * K}H-7Z" fill="#ff8a3a" ${OUT(2)}/><path d="M-5,${-0.85 * K}L-6,0M5,${-0.85 * K}L6,0" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><path d="M-9,${-1.7 * K + 24}L-14,${-1 * K}M9,${-1.7 * K + 24}L14,${-1 * K}" stroke="#ebc19c" stroke-width="5" stroke-linecap="round"/></g>`;
      // the scale on the left: a tick every metre, numbers at 5, 10, 15
      let rule = `<path d="M${wx + 26},${G}V${yM(15)}" stroke="${INK}" stroke-width="5"/>`;
      for (let m = 0; m <= 15; m++) rule += `<path d="M${wx + 26},${f1(yM(m))}h${m % 5 ? 12 : 24}" stroke="${INK}" stroke-width="${m % 5 ? 2.4 : 4}"/>${m && m % 5 === 0 ? `<text x="${wx + 56}" y="${f1(yM(m) + 10)}" font-family="Kanit" font-weight="800" font-size="28" fill="#1e2a3a" stroke="#fffaf0" stroke-width="6" paint-order="stroke">${m} ม.</text>` : ""}`;
      rule += `<text x="${wx + 40}" y="${G + 44}" font-family="Kanit" font-weight="700" font-size="26" fill="#5a4a3a">← ทะเล</text>`;
      // the mark each crest leaves and its tag: a dashed line at its height (under the floor badges), a slab with the time and the height
      let marks = "", tagMk = "";
      HM.forEach((m, k) => {
        const y = yM(m), [tm, hg] = tags[k].includes(" · ") ? tags[k].split(" · ") : ["", tags[k]], red = k === HM.length - 1;
        const tw = Math.round((tm ? emW(`${tm} · `) * 32 : 0) + emW(hg) * 46 + 56);
        marks += `<g id="${id}-mk${k}" opacity="0"><path d="M${wx + 36},${f1(y)}H${wx + 520}" stroke="${TC[k % 3]}" stroke-width="7" stroke-dasharray="20 12"/><path d="M${wx + 36},${f1(y)}H${wx + 520}" stroke="#fff" stroke-width="2" stroke-dasharray="20 12" opacity=".6"/></g>`;
        tagMk += `<g transform="translate(${wx + 530},${f1(y)})"><g id="${id}-tg${k}" opacity="0">${slab(0, -38, tw, 76, 38, { face: red ? "url(#tuLiveR)" : "url(#tuNote)", body: red ? "#7a0e1c" : "#8a6e4c", d: 8 })}
            <path d="M-2,0l-16,-12v24z" fill="${red ? "#d8243a" : "#f2e6c8"}" ${OUT(2.4)}/><circle cx="16" cy="0" r="7" fill="${TC[k % 3]}" stroke="${INK}" stroke-width="2"/>
            <text x="30" y="15" font-family="Kanit" font-weight="900">${tm ? `<tspan font-size="32" fill="${red ? "#ffe2e2" : "#6a5a4a"}">${tm} · </tspan>` : ""}<tspan font-size="46" fill="${red ? "#fff" : "#1e2a3a"}">${hg}</tspan></text></g></g>`;
      });
      scene += hotel + house + person + `<path id="${id}-fl" d="" fill="url(#tuFloodG)"/><g id="${id}-ff"></g>` + marks + badges + rule + tagMk;
      mount();
      // the water: each crest comes in from the sea side (left) as a bore, its front racing across, holds churning, then
      // drains away leaving its mark; the last one stays. One proxy tween redraws the flood, so any seek gives the right frame.
      const RISE = 0.75, DRAIN = 0.55, fl = document.getElementById(`${id}-fl`), ff = document.getElementById(`${id}-ff`), RF = mkR(88);
      const specks = Array.from({ length: 16 }, () => [RF(), RF(), RF()]), up = gsap.parseEase("power2.out"), dn = gsap.parseEase("power1.in");
      const state = (tt) => {   // → [level m, front 0..1]
        let L = 0, F = 1;
        HM.forEach((m, k) => {
          const a = at[k], b = k + 1 < HM.length ? at[k + 1] - 0.15 : 1e9;
          if (tt < a) return;
          const u = tt - a;
          if (u < RISE) { const e = up(u / RISE); L = Math.max(L, m * (0.55 + 0.45 * e)); F = e; }
          else if (tt < b - DRAIN || k + 1 === HM.length) { L = Math.max(L, m); F = 1; }
          else if (tt < b) L = Math.max(L, m * (1 - dn((tt - (b - DRAIN)) / DRAIN)));
        });
        return [L, F];
      };
      const draw = (tt) => {
        const [Lm, F] = state(tt);
        if (Lm < 0.02) { fl.setAttribute("d", ""); ff.innerHTML = ""; return; }
        const yTop = yM(Lm), x0 = wx - 10, xf = wx + 40 + (ww + 40) * F, pts = [];
        for (let x = x0; x <= xf; x += 24) pts.push([x, yTop + 7 * Math.sin(x * 0.045 + tt * 5.2) + 4 * Math.sin(x * 0.11 - tt * 7.3)]);
        const front = F < 1 ? `L${f1(xf + 26)},${f1(yTop + (G - yTop) * 0.35)} L${f1(xf + 70)},${G}` : `L${wx + ww + 20},${f1(yTop)} L${wx + ww + 20},${G}`;
        fl.setAttribute("d", `M${x0},${G + 30} L${pts.map(([a, b]) => `${f1(a)},${f1(b)}`).join(" L")} ${front} L${wx + ww + 20},${G + 30} Z`);
        let fo = `<path d="M${pts.map(([a, b]) => `${f1(a)},${f1(b)}`).join(" L")}" stroke="#f4fbff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
        specks.forEach(([a, b, c], j) => { const x = x0 + a * (xf - x0), y = yTop + 18 + b * Math.max(20, G - yTop - 30);
          fo += j % 3 ? `<circle cx="${f1(x + 10 * Math.sin(tt * 3 + j))}" cy="${f1(y)}" r="${f1(3 + c * 5)}" fill="none" stroke="#c8ecee" stroke-width="2.4" opacity=".6"/>`
            : `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(18 + c * 26)}" height="7" rx="2" fill="#6a4a2a" opacity=".85" transform="rotate(${f1(-20 + c * 40 + 12 * Math.sin(tt * 2 + j))} ${f1(x)} ${f1(y)})"/>`; });
        if (F < 1) fo += Array.from({ length: 6 }, (_, j) => `<circle cx="${f1(xf + 10 + j * 9)}" cy="${f1(yTop + (G - yTop) * (0.08 + j * 0.13))}" r="${f1(9 - j)}" fill="#f4fbff" opacity=".9"/>`).join("");
        ff.innerHTML = fo;
      };
      draw(0);
      const c = { t: 0 };
      tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => draw(c.t) }, t0);
      HM.forEach((_, k) => {
        const tm = t0 + at[k] + RISE * 0.8;
        tl.fromTo(`#${id}-mk${k}`, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, tm);
        tl.fromTo(`#${id}-tg${k}`, { opacity: 0, x: 40, scale: 0.5, svgOrigin: "0 0" }, { opacity: 1, x: 0, scale: 1, svgOrigin: "0 0", duration: 0.55, ease: "back.out(2.4)", immediateRender: false }, tm);
        tl.fromTo(`#${id}-tg${k}`, { y: 0 }, { y: -5, duration: 0.75, repeat: Math.ceil(dur / 0.75), yoyo: true, ease: "sine.inOut", immediateRender: false }, tm + 0.6);
      });
    }
    if (o.out !== undefined) { tl.to(`#${id}-m`, { y: -200, duration: 0.3, ease: "power2.in" }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + o.out); }
    return id;
  }
  // the board drops on its ropes, swings, settles, then sways until the shot ends
  function boardIn(tl, id, t0, dur, Y0) {
    tl.set(`#${id}`, { opacity: 1 }, t0);
    tl.fromTo(`#${id}-m`, { y: -1200 }, { y: 0, duration: 0.55, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 4, svgOrigin: `540 ${Y0 - 900}` }, { rotation: 0, svgOrigin: `540 ${Y0 - 900}`, duration: 1.5, ease: "elastic.out(1, 0.32)", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-sw`, { rotation: 0, svgOrigin: `540 ${Y0 - 900}` }, { rotation: 0.22, svgOrigin: `540 ${Y0 - 900}`, duration: 0.7, ease: "sine.out", immediateRender: false }, t0 + 1.9);
    tl.fromTo(`#${id}-sw`, { rotation: 0.22, svgOrigin: `540 ${Y0 - 900}` }, { rotation: -0.22, svgOrigin: `540 ${Y0 - 900}`, duration: 1.4, repeat: Math.ceil(dur / 1.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 2.6);
    tl.fromTo(`#${id}-ti`, { scale: 0.6, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.3);
  }

  // ---------------- the warning tower's loudspeakers: the real announcement ----------------
  // a slab with a hazard band, the horn cluster pulsing sound rings, the two quoted lines (Thai PBS: the tower's message M3).
  const hornCluster = () => `<path d="M-6,30V96" stroke="#5a646c" stroke-width="10"/><rect x="-26" y="-6" width="52" height="40" rx="8" fill="#8a949c" ${OUT(3)}/>
    ${[[-1, -18], [1, -18], [-1, 22], [1, 22]].map(([s, y]) => `<g transform="translate(${s * 24},${y}) scale(${s},1)"><path d="M0,-12L44,-30V30L0,12Z" fill="#e8ecee" ${OUT(3)}/><path d="M44,-30Q52,0 44,30" fill="#c8d0d4" ${OUT(2.6)}/><path d="M6,-8L40,-22" stroke="#fff" stroke-width="3" opacity=".7"/></g>`).join("")}
    <circle cx="0" cy="-36" r="9" fill="#e8392c" ${OUT(2.4)}/>`;
  function pa(tl, layer, t0, dur, o = {}) {
    const id = nid(), at = o.at || [0, 0.35, 1.4], Y = o.y ?? 470, l1 = o.l1 || "โปรดทราบ โปรดทราบ…", l2 = o.l2 || "ขณะนี้เกิดคลื่นสึนามิ";
    const W = 960, Hh = 330, x0 = -W / 2, y0 = -Hh / 2, TX = x0 + 300;
    // both lines shrink to fit the 620 px beside the horn (Kanit 800/900)
    const s1 = Math.min(52, Math.floor(620 / (emW(`“${l1}”`) * 0.96))), s2 = Math.min(64, Math.floor(620 / emW(`“${l2}”`)));
    const w2 = emW(`“${l2}”`) * s2;
    const rings = (s) => [1, 2, 3].map((k) => `<path class="tuRing" data-k="${k}" d="M${s * (66 + k * 16)},-${28 + k * 14}Q${s * (84 + k * 22)},0 ${s * (66 + k * 16)},${28 + k * 14}" stroke="#ffd23a" stroke-width="${8 - k}" fill="none" stroke-linecap="round" opacity="${f1(1 - k * 0.22)}"/>`).join("");
    put(layer, `<g transform="translate(540,${Y})"><g id="${id}" opacity="0"><g id="${id}-in">
      <ellipse cx="0" cy="${Hh / 2 + 30}" rx="${W / 2 - 40}" ry="26" fill="url(#tuSoftSh)" opacity=".7"/>
      <rect x="${x0}" y="${y0 + 14}" width="${W}" height="${Hh}" rx="40" fill="#3a2a1a" ${OUT(5)}/>
      <rect x="${x0}" y="${y0}" width="${W}" height="${Hh}" rx="40" fill="url(#tuNote)" ${OUT(5)}/>
      <defs><clipPath id="${id}-hc"><rect x="${x0}" y="${y0}" width="${W}" height="${Hh}" rx="40"/></clipPath></defs>
      <g clip-path="url(#${id}-hc)"><g id="${id}-hz"><rect x="${x0 - 112}" y="${y0}" width="${W + 224}" height="34" fill="url(#tuHaz)"/></g><path d="M${x0},${y0 + 34}H${-x0}" stroke="${INK}" stroke-width="4"/>
        <rect x="${x0}" y="${y0 + 34}" width="${W}" height="40" fill="#fff" opacity=".18"/></g>
      <g transform="translate(${x0 + 150},${y0 + 190})"><circle r="104" fill="#1e2a3a" ${OUT(4)}/><circle r="96" fill="none" stroke="#ffd23a" stroke-width="5" opacity=".5"/>
        <g id="${id}-hn">${hornCluster()}</g>${rings(-1)}${rings(1)}</g>
      <g transform="translate(${x0 + 30},${y0 - 34})"><g id="${id}-lb">${slab(0, -26, 250, 56, 28, { face: "url(#tuLiveR)", body: "#7a0e1c", d: 7 })}
        <path d="M30,18V-14M22,-14h16l-8,-10z" stroke="#fff" stroke-width="4" fill="#fff" stroke-linejoin="round"/><text x="140" y="11" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#fff">หอเตือนภัย</text></g></g>
      <defs><clipPath id="${id}-c1"><rect id="${id}-r1" x="${TX - 10}" y="${y0 + 60}" width="0" height="100"/></clipPath></defs>
      <g clip-path="url(#${id}-c1)"><text x="${TX}" y="${y0 + 136}" font-family="Kanit" font-weight="800" font-size="${s1}" fill="#1e2a3a">“${l1}”</text></g>
      <g transform="translate(${TX},${y0 + 240})"><g id="${id}-l2" opacity="0">
        <text font-family="Kanit" font-weight="900" font-size="${s2}" fill="#fffaf0" stroke="#fffaf0" stroke-width="10" stroke-linejoin="round">“${l2}”</text>
        <text font-family="Kanit" font-weight="900" font-size="${s2}" fill="#d8312a">“${l2}”</text>
        <path id="${id}-ul" d="M6,22Q${f1(w2 / 2)},34 ${f1(w2)},20" stroke="#d8312a" stroke-width="7" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></g></g>
    </g></g></g>`);
    const ta = t0 + at[0];
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, ta);
    tl.fromTo(`#${id}-in`, { y: -90, scaleX: 0.6, scaleY: 1.25, svgOrigin: `0 ${Hh / 2}` }, { y: 0, scaleX: 1, scaleY: 1, svgOrigin: `0 ${Hh / 2}`, duration: 0.7, ease: "elastic.out(1, 0.5)", immediateRender: false }, ta);
    tl.fromTo(`#${id}-lb`, { scale: 0, rotation: -12, svgOrigin: "0 0" }, { scale: 1, rotation: -4, svgOrigin: "0 0", duration: 0.5, ease: "back.out(2.6)", immediateRender: false }, ta + 0.2);
    // the horns shudder with the sound, the rings pulse outward, the hazard band crawls
    tl.fromTo(`#${id}-hn`, { rotation: -2, svgOrigin: "0 0" }, { rotation: 2, svgOrigin: "0 0", duration: 0.07, repeat: Math.ceil(dur / 0.07), yoyo: true, ease: "none", immediateRender: false }, ta);
    document.getElementById(id).querySelectorAll(".tuRing").forEach((r) => { const k = +r.dataset.k;
      tl.fromTo(r, { opacity: 0, scale: 0.7, svgOrigin: "0 0" }, { opacity: 0.95, scale: 1.08, svgOrigin: "0 0", duration: 0.55, repeat: Math.ceil(dur / 0.55), ease: "power1.out", immediateRender: false }, ta + k * 0.12); });
    tl.fromTo(`#${id}-hz`, { x: 0 }, { x: -79.2, duration: 0.6, repeat: Math.ceil(dur / 0.6), ease: "none", immediateRender: false }, ta);
    // line 1 is written on with the voice (it takes the time until line 2), line 2 slams in, gets underlined and shakes
    tl.fromTo(`#${id}-r1`, { attr: { width: 0 } }, { attr: { width: 640 }, duration: Math.min(1.2, Math.max(0.5, at[2] - at[1] - 0.1)), ease: "power1.inOut", immediateRender: false }, t0 + at[1]);
    tl.fromTo(`#${id}-l2`, { opacity: 0, scale: 0.4, svgOrigin: `${f1(w2 / 2)} -20` }, { opacity: 1, scale: 1, svgOrigin: `${f1(w2 / 2)} -20`, duration: 0.55, ease: "back.out(2.4)", immediateRender: false }, t0 + at[2]);
    tl.fromTo(`#${id}-ul`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.out", immediateRender: false }, t0 + at[2] + 0.35);
    tl.fromTo(`#${id}-l2`, { x: 0 }, { x: 4, duration: 0.09, repeat: 7, yoyo: true, ease: "none", immediateRender: false }, t0 + at[2] + 0.6);
    if (o.out !== undefined) { tl.to(`#${id}-in`, { y: -60, duration: 0.3, ease: "power2.in" }, t0 + o.out); tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + o.out); }
    return id;
  }

  window.TideUI = { rule, live, choice, endCard, source, legendAnim, series, pa, ICON, icon, iconPop, iconLife, RULES };
  Object.assign(Sets, { tideLegend });
})();
