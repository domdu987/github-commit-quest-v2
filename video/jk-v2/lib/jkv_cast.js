// สกิลจอมโกหก · look V detail pass for the CAST (owner 11 Nov 2026: "เขียนให้ละเอียด … เสื้อผ้า … ห้ามใช้ fal.ai เจนภาพ").
// Hand-drawn SVG clothing and hair detail over the flat.js bodies, in the stylized-3D spirit: vertical cloth gradients (lit from above),
// a cylinder shade across the torso, bevelled edges, patterns for weave / pinstripe / embroidery, small believable props. No filters at all.
// It wraps Flat.SPEC.<name>.acc and .headTop (the originals still run first, so the animated classes jkTie, jkScarf, jkEar, jkGum stay),
// and must load right after jkcast.js: common.part and the shots copy these specs at load time.
//   jkYou    navy suit: pinstripe + cylinder shade, side and centre seams, a shoulder bevel, waist creases, a shirt collar band with the top
//            button and two collar wings, notched lapels with edge highlights, a striped tie with a dimpled knot, a chest pocket with a pocket
//            square, three buttons with highlights · hair: two highlight strands (the coat is buttoned to the hem, so no belt can show)
//   jkKen    tunic: weave + shade, a laced placket with eyelets, gold trim, an embroidered hem band, leather shoulder plates with gold rims and
//            rivets, a stitched leather belt with a bevelled gold buckle and a hip pouch, a pendant on a cord, the scarf redrawn with folds,
//            a knot and fringed tails (class jkScarf kept) · hair: two strands
//   jkGod    robe: four layered drape folds with highlight and shade edges, a jewelled gold sash (sapphire medallion, ruby and emerald side
//            gems, studs) with a hanging ribbon, a gold necklace with beads and a pink pendant, a drop earring · halo: a soft glow, a double
//            ring with a bevel and three sparkles · hair: two strands
//   jkSoul1/2/3  weave + shade, a rib collar, a hem band, a belt, a crumpled queue ticket (creases, perforation, a red strip, "คิว"), a round
//            number badge with a pin, a faint tee print each · hair: one strand
//   jkAunt   a floral blouse print, a round collar, a pearl necklace with a gold pendant, a handbag strap and bag, a thin belt, a hoop earring
//   jkMan1   leather work apron with straps, a bib pocket with a pencil, a tool loop, a patch · jkMan2 a green neckerchief with a knot and
//            tails, a round chest patch, a hip patch, a belt · jkMan3 a cream baker's apron with a neck strap, a waist tie with a bow, a
//            pocket with a spoon, flour smudges · jkWom1 a teal shawl with fringe, a wooden bead necklace, a red sash
//   also: Flat.SPEC.jkYouBag / jkYouBook / jkYouCard are aliased to jkYou, so jkYouBagB (defined by the shots as a copy of jkYouBag) gets
//         the hero's spec (suit, messy hair, glasses, the red ear) instead of an empty one.
(function () {
  if (window.JKV && JKV.cast) return;   // idempotent
  if (!window.Flat || !window.Rig || !window.Rig2 || !window.Sets) return;
  const { mix, dk, hi } = Rig2;
  const f = (v) => (+v).toFixed(1);
  const S = Flat.SPEC, C = Rig.CAST;
  const wOf = (n) => (((C[n] || {}).v2 || {}).w) || 1;
  const hairOf = (n) => ((((C[n] || {}).v2 || {}).hair || {}).c) || "#1a1410";

  // ---------------- materials (ids prefixed jkv_), added once ----------------
  Sets.DEFS += `
    <linearGradient id="jkv_cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset=".38" stop-color="#fff" stop-opacity=".11"/><stop offset=".64" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".16"/></linearGradient>
    <linearGradient id="jkv_lit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".26"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>
    <linearGradient id="jkv_neckShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".34"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
    <linearGradient id="jkv_shirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf9f4"/><stop offset="1" stop-color="#e2ddd0"/></linearGradient>
    <linearGradient id="jkv_tie" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecd28e"/><stop offset=".5" stop-color="#d9a43a"/><stop offset="1" stop-color="#a8781c"/></linearGradient>
    <pattern id="jkv_tieStripe" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(-40)"><rect width="10" height="10" fill="#d9a43a"/><rect width="10" height="3.2" fill="#c08c2a"/><rect y="5.6" width="10" height="1.4" fill="#f0c860"/></pattern>
    <pattern id="jkv_pin" width="8" height="8" patternUnits="userSpaceOnUse"><rect x="2" width="1.3" height="8" fill="#fff" opacity=".09"/></pattern>
    <pattern id="jkv_weave" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0,2.5h5M2.5,0v5" stroke="#000" stroke-width=".8" opacity=".07"/></pattern>
    <pattern id="jkv_embroid" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#b8322a"/><path d="M6,1.5L10.5,6L6,10.5L1.5,6Z" fill="#e8c86a"/><circle cx="6" cy="6" r="1.3" fill="#fbeab0"/></pattern>
    <radialGradient id="jkv_btn" cx=".36" cy=".3" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".6"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></radialGradient>
    <linearGradient id="jkv_gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2b0"/><stop offset=".45" stop-color="#f2c24a"/><stop offset=".78" stop-color="#c08a20"/><stop offset="1" stop-color="#8a5a10"/></linearGradient>
    <linearGradient id="jkv_leather" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ad7d52"/><stop offset=".5" stop-color="#7a5232"/><stop offset="1" stop-color="#4e3220"/></linearGradient>
    <linearGradient id="jkv_leatherD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7e5636"/><stop offset="1" stop-color="#3a2416"/></linearGradient>
    <linearGradient id="jkv_scarf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2543f"/><stop offset=".5" stop-color="#c8302a"/><stop offset="1" stop-color="#8e1e18"/></linearGradient>
    <linearGradient id="jkv_scarfG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa878"/><stop offset=".55" stop-color="#3a7a58"/><stop offset="1" stop-color="#245040"/></linearGradient>
    <linearGradient id="jkv_robe" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdfbff"/><stop offset=".6" stop-color="#ece4fa"/><stop offset="1" stop-color="#d2c6ec"/></linearGradient>
    <linearGradient id="jkv_cream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8f2e4"/><stop offset="1" stop-color="#e0d4ba"/></linearGradient>
    <linearGradient id="jkv_shawl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a9a98"/><stop offset=".55" stop-color="#3a6c6a"/><stop offset="1" stop-color="#244846"/></linearGradient>
    <radialGradient id="jkv_haloGlow"><stop offset="0" stop-color="#ffe27a" stop-opacity=".42"/><stop offset=".6" stop-color="#ffd85a" stop-opacity=".14"/><stop offset="1" stop-color="#ffd85a" stop-opacity="0"/></radialGradient>`;

  // ---------------- helpers (local coordinates of flat.js: feet y 0, shoulders y -490, +x = the facing side) ----------------
  const slabD = (w, b) => { const X = (v) => f(v * w); return `M${X(-44)},-462Q${X(-44)},-490 ${X(-20)},-490H${X(20)}Q${X(44)},-490 ${X(44)},-462L${X(45)},${b}H${X(-45)}Z`; };
  const panelD = (w, b) => { const X = (v) => f(v * w); return `M${X(-44)},-462Q${X(-44)},-490 ${X(-20)},-490H${X(-14)}Q${X(-22)},-474 ${X(-23)},-452L${X(-22)},${b}H${X(-45)}Z`; };
  const NECK = `<rect x="-11" y="-506" width="22" height="16" fill="url(#jkv_neckShade)"/>`;   // the chin's shadow on the neck
  const shade = (w, b, op = 1) => `<path d="${slabD(w, b)}" fill="url(#jkv_cyl)" opacity="${op}"/>`;   // the torso reads as a cylinder
  const button = (x, y, r, c) => `<circle cx="${f(x)}" cy="${f(y)}" r="${r}" fill="${c}"/><circle cx="${f(x)}" cy="${f(y)}" r="${r}" fill="url(#jkv_btn)"/>`;
  const gem = (x, y, r, c) => `<circle cx="${f(x)}" cy="${f(y)}" r="${r}" fill="${dk(c, 0.3)}"/><circle cx="${f(x)}" cy="${f(y)}" r="${f(r * 0.76)}" fill="${c}"/><circle cx="${f(x - r * 0.3)}" cy="${f(y - r * 0.34)}" r="${f(Math.max(0.9, r * 0.28))}" fill="#fff" opacity=".85"/>`;
  const star = (x, y, r, c = "#fff8d0") => `<path d="M${f(x)},${f(y - r)}Q${f(x + r * 0.16)},${f(y - r * 0.16)} ${f(x + r)},${f(y)}Q${f(x + r * 0.16)},${f(y + r * 0.16)} ${f(x)},${f(y + r)}Q${f(x - r * 0.16)},${f(y + r * 0.16)} ${f(x - r)},${f(y)}Q${f(x - r * 0.16)},${f(y - r * 0.16)} ${f(x)},${f(y - r)}Z" fill="${c}"/>`;
  const strand = (d, c, w = 3, op = 0.42) => `<path d="${d}" stroke="${hi(c, 0.45)}" stroke-width="${w}" fill="none" stroke-linecap="round" opacity="${op}"/>`;
  // points along a quadratic (a necklace curve)
  const qpt = (A, B, Cc, t) => [0, 1].map((i) => (1 - t) * (1 - t) * A[i] + 2 * (1 - t) * t * B[i] + t * t * Cc[i]);
  const beads = (A, B, Cc, n, r, c, hl = "#fff") => [...Array(n)].map((_, i) => { const t = (i + 1) / (n + 1), [px, py] = qpt(A, B, Cc, t);
    return `<circle cx="${f(px)}" cy="${f(py)}" r="${r}" fill="${c}"/><circle cx="${f(px - r * 0.3)}" cy="${f(py - r * 0.3)}" r="${f(r * 0.32)}" fill="${hl}" opacity=".8"/>`; }).join("");
  const wrapAcc = (n, extra) => { const sp = S[n]; if (!sp || sp._jkvAcc) return; const prev = sp.acc; sp.acc = (x) => (prev ? prev(x) : "") + extra(x); sp._jkvAcc = true; };
  const wrapHead = (n, extra, before) => { const sp = S[n]; if (!sp || sp._jkvHead) return; const prev = sp.headTop;
    sp.headTop = (x) => (before ? before(x) : "") + (prev ? prev(x) : "") + extra(x); sp._jkvHead = true; };

  // ---------------- คุณ: the cheap navy suit, now cut properly ----------------
  const TIE = "#d9a43a";
  const suitV = (w) => (x) => {
    const top = x.top, slab = slabD(w, -236), panel = panelD(w, -236), hiT = hi(top, 0.32), dkT = dk(top, 0.32);
    const lapel = (s, c) => { const X = (v) => f(v * s), d = `M${X(12)},-497L${X(32)},-481L${X(25)},-467L${X(38)},-455L${X(3)},-348Z`;
      return `<path d="${d}" fill="${c}"/><path d="${d}" fill="url(#jkv_lit)"/><path d="M${X(32)},-481L${X(25)},-467L${X(38)},-455L${X(3)},-348" stroke="${hiT}" stroke-width="2" fill="none" stroke-linejoin="round" opacity="${s > 0 ? 0.62 : 0.48}"/>`; };
    const wing = (s) => { const X = (v) => f(v * s); return `<path d="M${X(14)},-501L${X(22)},-492L${X(7)},-468L${X(3)},-488Z" fill="url(#jkv_shirt)"/><path d="M${X(14)},-501L${X(22)},-492L${X(7)},-468" stroke="#cfc7b8" stroke-width="1.4" fill="none"/>`; };
    return `<path d="${slab}" fill="${top}"/><path d="${panel}" fill="${x.topS}"/><path d="${slab}" fill="url(#jkv_pin)"/><path d="${slab}" fill="url(#jkv_cyl)"/><path d="${slab}" fill="url(#flV)"/>${NECK}
      <path d="M${f(-40 * w)},-470L${f(-41 * w)},-240M${f(40 * w)},-470L${f(41 * w)},-240" stroke="${dkT}" stroke-width="2" opacity=".32"/>
      <path d="M-3,-350V-236" stroke="${dkT}" stroke-width="2.4" opacity=".55"/><path d="M-0.8,-350V-236" stroke="${hiT}" stroke-width="1.2" opacity=".22"/>
      <path d="M${f(-39 * w)},-468Q${f(-40 * w)},-486 ${f(-20 * w)},-487H${f(20 * w)}Q${f(40 * w)},-486 ${f(39 * w)},-468" stroke="${hiT}" stroke-width="2.6" fill="none" opacity=".5"/>
      <path d="M-36,-286q14,-6 30,-2M-30,-262q12,-5 26,-1M18,-272q10,-4 22,0M14,-296q9,-3 20,1" stroke="${dkT}" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".45"/>
      <path d="M-36,-289q14,-6 30,-2M-30,-265q12,-5 26,-1M18,-275q10,-4 22,0" stroke="${hiT}" stroke-width="1.4" fill="none" stroke-linecap="round" opacity=".22"/>
      <rect x="${f(-45 * w)}" y="-248" width="${f(90 * w)}" height="12" fill="#000" opacity=".1"/>
      <path d="M-13,-497L-3,-356H3L13,-497Z" fill="url(#jkv_shirt)"/><path d="M-13,-497L-3,-356H-1L-9,-497ZM13,-497L3,-356H1L9,-497Z" fill="#000" opacity=".1"/>
      <path d="M-33,-481Q-22,-500 -12,-502H12Q22,-500 33,-481L28,-477Q20,-492 12,-494H-12Q-20,-492 -28,-477Z" fill="${dk(top, 0.22)}"/>
      <path d="M-14,-502Q0,-495 14,-502L14,-488Q0,-481 -14,-488Z" fill="url(#jkv_shirt)"/>${button(0, -493, 2.4, "#e4ded0")}
      ${wing(-1)}${wing(1)}
      ${lapel(-1, dk(top, 0.17))}${lapel(1, dk(top, 0.07))}
      <path d="M-12,-497L-3,-356M12,-497L3,-356" stroke="${dkT}" stroke-width="1.6" opacity=".4"/>
      <path d="M-6.5,-489H6.5L8.5,-476L0,-467L-8.5,-476Z" fill="url(#jkv_tie)"/><path d="M-1,-487q1,8 0,16" stroke="${dk(TIE, 0.4)}" stroke-width="1.6" fill="none" opacity=".7"/><path d="M-5.5,-486q-1,5 1,10" stroke="${hi(TIE, 0.5)}" stroke-width="1.4" fill="none" opacity=".6"/>
      <g class="jkTie"><path d="M-6,-471L-9.5,-372L0,-357L9.5,-372L6,-471Z" fill="url(#jkv_tieStripe)"/><path d="M-6,-471L-9.5,-372L0,-357L9.5,-372L6,-471Z" fill="url(#jkv_lit)"/>
        <path d="M-5,-470L-8.4,-373" stroke="${hi(TIE, 0.45)}" stroke-width="1.6" opacity=".5"/><path d="M5,-470L8.4,-373" stroke="${dk(TIE, 0.35)}" stroke-width="1.6" opacity=".5"/></g>
      <path d="M22,-437L25,-447L29,-440L33,-449L36,-437Z" fill="#f4f1ea"/><path d="M29,-440L29,-437" stroke="#c8c0b0" stroke-width="1"/>
      <rect x="20" y="-438" width="18" height="4.5" rx="1" fill="${dk(top, 0.32)}"/><path d="M20,-438H38" stroke="${hiT}" stroke-width="1.2" opacity=".5"/>
      ${[-346, -310, -274].map((y) => button(4, y, 4.6, dk(top, 0.42))).join("")}`;
  };
  const youHair = hairOf("jkYou");
  ["jkYou", "jkYouBucket", "jkYouHorn", "jkYouHornBucket"].forEach((n) => wrapAcc(n, suitV(wOf("jkYou"))));
  wrapHead("jkYou", () => strand("M-30,-574Q-8,-596 14,-590", youHair, 3.2, 0.38) + strand("M0,-612Q4,-626 8,-632", youHair, 2.4, 0.4));
  wrapHead("jkYouHorn", () => strand("M-30,-574Q-8,-596 14,-590", youHair, 3.2, 0.38));
  // the bag / book / card variants resolve to jkYou through flat.js's suffix rule; alias them so a later copy (jkYouBagB) finds a spec too
  ["jkYouBag", "jkYouBook", "jkYouCard"].forEach((n) => { if (!S[n]) S[n] = S.jkYou; });

  // ---------------- เคน: the tunic of a boy who thinks he's the hero ----------------
  const kenV = (w) => (x) => {
    const top = x.top, slab = slabD(w, -296), panel = panelD(w, -296), dkT = dk(top, 0.3), RED = "#c8302a", LEA = "#7a5232";
    const plate = (s, c) => { const X = (v) => f(v * s), d = `M${X(21)},-492Q${X(44)},-494 ${X(45)},-462L${X(39)},-458Q${X(37)},-477 ${X(19)},-482Z`;
      return `<path d="${d}" fill="${c}"/><path d="${d}" fill="url(#jkv_lit)"/><path d="M${X(21)},-492Q${X(44)},-494 ${X(45)},-462" stroke="#d8b84a" stroke-width="2.2" fill="none"/><circle cx="${X(30)}" cy="-486" r="2" fill="#f0dc98"/><circle cx="${X(41)}" cy="-471" r="2" fill="#f0dc98"/>`; };
    return `<path d="${slab}" fill="${top}"/><path d="${panel}" fill="${x.topS}"/><path d="${slab}" fill="url(#jkv_weave)"/><path d="${slab}" fill="url(#jkv_cyl)"/><path d="${slab}" fill="url(#flV)"/>${NECK}
      <path d="M${f(-40 * w)},-460L${f(-41 * w)},-300M${f(40 * w)},-460L${f(41 * w)},-300" stroke="${dkT}" stroke-width="2" opacity=".25"/>
      <path d="M-34,-352q12,-5 24,0M14,-346q10,-4 22,0" stroke="${dkT}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".35"/>
      <rect x="-9" y="-470" width="18" height="136" fill="${dk(top, 0.06)}"/><path d="M-9,-470V-334M9,-470V-334" stroke="#c8a43a" stroke-width="1.8" opacity=".9"/>
      ${[-412, -394, -376, -358].map((y) => `<circle cx="-5" cy="${y}" r="2.3" fill="${dk(top, 0.5)}"/><circle cx="5" cy="${y}" r="2.3" fill="${dk(top, 0.5)}"/>`).join("")}
      <path d="M-5,-412L5,-394L-5,-376L5,-358M5,-412L-5,-394L5,-376L-5,-358M-5,-358q-6,6 -2,12M5,-358q6,6 2,12" stroke="#8a5a32" stroke-width="2.2" fill="none" stroke-linecap="round"/>
      <rect x="${f(-45 * w)}" y="-314" width="${f(90 * w)}" height="17" fill="url(#jkv_embroid)"/><path d="M${f(-45 * w)},-314H${f(45 * w)}M${f(-45 * w)},-297H${f(45 * w)}" stroke="#c8a43a" stroke-width="1.6"/>
      ${plate(1, LEA)}${plate(-1, dk(LEA, 0.2))}
      <rect x="${f(-46 * w)}" y="-333" width="${f(92 * w)}" height="19" fill="url(#jkv_leather)"/><path d="M${f(-46 * w)},-333H${f(46 * w)}" stroke="${hi(LEA, 0.4)}" stroke-width="1.6" opacity=".7"/><path d="M${f(-46 * w)},-314H${f(46 * w)}" stroke="${dk(LEA, 0.4)}" stroke-width="1.6"/>
      <path d="M${f(-44 * w)},-329H${f(44 * w)}M${f(-44 * w)},-318H${f(44 * w)}" stroke="#e8d0a8" stroke-width="1" stroke-dasharray="3 4" opacity=".55"/>
      <rect x="-10" y="-337" width="20" height="27" rx="3" fill="url(#jkv_gold)"/><rect x="-6" y="-333" width="12" height="19" rx="1.5" fill="${dk(LEA, 0.3)}"/><path d="M0,-334V-316" stroke="#f2e0a0" stroke-width="2.2" stroke-linecap="round"/>
      <rect x="31" y="-336" width="6" height="16" rx="2" fill="${dk(LEA, 0.35)}"/>
      <path d="M24,-320H42V-293Q33,-286 24,-293Z" fill="url(#jkv_leatherD)"/><path d="M22,-322H44L42,-307H24Z" fill="${dk(LEA, 0.12)}"/><path d="M22,-322H44" stroke="${hi(LEA, 0.35)}" stroke-width="1.4" opacity=".6"/><circle cx="33" cy="-309" r="2.4" fill="#d8b84a"/>
      <path d="M-15,-448Q0,-424 15,-448" stroke="#5a3a24" stroke-width="2" fill="none"/><circle cx="0" cy="-427" r="7" fill="url(#jkv_gold)"/>${gem(0, -427, 3.4, "#d8403a")}
      <path d="M-46,-490Q0,-454 46,-490L50,-468Q0,-436 -50,-468Z" fill="url(#jkv_scarf)"/>
      <path d="M-44,-487Q0,-453 44,-487" stroke="${hi(RED, 0.4)}" stroke-width="2.2" fill="none" opacity=".55"/>
      <path d="M-30,-478Q-10,-458 10,-466M-14,-470Q8,-450 30,-460" stroke="${dk(RED, 0.3)}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".5"/>
      <path d="M-48,-469Q0,-437 48,-469" stroke="${dk(RED, 0.35)}" stroke-width="2" fill="none" opacity=".5"/>
      <g class="jkScarf"><path d="M28,-474L62,-404L52,-392L36,-398Z" fill="url(#jkv_scarf)"/><path d="M30,-473L50,-414L40,-404Z" fill="${dk(RED, 0.22)}"/>
        <path d="M33,-468L57,-410" stroke="${hi(RED, 0.4)}" stroke-width="1.6" opacity=".45"/>
        <path d="M38,-397l-2,10M45,-394l-1,10M52,-392l1,10M58,-397l2,9" stroke="${dk(RED, 0.15)}" stroke-width="2" stroke-linecap="round"/></g>
      <ellipse cx="31" cy="-471" rx="9.5" ry="7.5" fill="${dk(RED, 0.1)}"/><path d="M24,-474q7,-5 14,0M24,-468q7,5 14,0" stroke="${dk(RED, 0.35)}" stroke-width="1.8" fill="none"/><path d="M26,-476q4,-2 8,-1" stroke="${hi(RED, 0.45)}" stroke-width="1.6" fill="none" opacity=".6"/>`;
  };
  wrapAcc("jkKen", kenV(wOf("jkKen")));
  const kenHair = hairOf("jkKen");
  wrapHead("jkKen", () => strand("M-26,-580Q-8,-592 6,-586", kenHair, 3, 0.5) + strand("M26,-600L34,-622", kenHair, 2.6, 0.45));

  // ---------------- เทพี: a draped robe, a jewelled sash, the halo polished ----------------
  const godV = (w) => (x) => {
    const ROBE = "#ece4fa", slab = slabD(w, -296);
    const bands = [[-446, -418], [-418, -390], [-390, -362], [-362, null]];
    // each fold sweeps from the far shoulder down toward the near hip (a toga drape), with a soft lit edge and a shade under it
    const edge = (y) => `M-45,${y + 8}Q-12,${y + 44} 45,${y - 2}`;
    const fold = ([y0, y1]) => { const d = y1 === null ? `${edge(y0)}L45,-296H-45Z` : `${edge(y0)}L45,${y1 - 2}Q-12,${y1 + 44} -45,${y1 + 8}Z`;
      return `<path d="${d}" fill="url(#jkv_robe)"/><path d="${edge(y0)}" stroke="#fff" stroke-width="2.2" fill="none" opacity=".3"/><path d="${edge(y0 + 2.5)}" stroke="${dk(ROBE, 0.22)}" stroke-width="2" fill="none" opacity=".3"/>
        <path d="M-24,${y0 + 24}q2,10 -2,20M8,${y0 + 24}q2,9 -1,18M30,${y0 + 6}q2,9 -1,17" stroke="${dk(ROBE, 0.2)}" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".35"/>`; };
    const sashGems = [[-30, "#3aa868"], [-17, "#d8403a"], [17, "#d8403a"], [30, "#3aa868"]].map(([gx, c]) => gem(gx, -326.5, 3.4, c)).join("")
      + [-38, -24, -9, 9, 24, 38].map((gx) => `<circle cx="${gx}" cy="-326.5" r="1.6" fill="#fff0a8"/>`).join("");
    return `${bands.map(fold).join("")}<path d="${slab}" fill="url(#jkv_cyl)" opacity=".7"/>
      <rect x="-45" y="-337" width="90" height="21" fill="url(#jkv_gold)"/><path d="M-45,-336H45" stroke="#fff6c8" stroke-width="1.6" opacity=".8"/><path d="M-45,-317H45" stroke="#7a5210" stroke-width="1.8" opacity=".8"/>
      <path d="M30,-316L36,-282L24,-286Z" fill="url(#jkv_gold)"/><path d="M30,-282l-2,10M33,-281l0,10M36,-282l2,9" stroke="#e0a830" stroke-width="1.8" stroke-linecap="round"/>
      ${sashGems}<circle cx="0" cy="-326.5" r="10" fill="url(#jkv_gold)"/><circle cx="0" cy="-326.5" r="10" fill="none" stroke="#8a5a10" stroke-width="1"/>${gem(0, -326.5, 6, "#4a6ad8")}
      <path d="M-15,-494Q0,-468 15,-494" stroke="#f2c25a" stroke-width="2.2" fill="none"/>${beads([-15, -494], [0, -468], [15, -494], 6, 2.1, "#f6d888")}
      <circle cx="0" cy="-478" r="4.6" fill="url(#jkv_gold)"/>${gem(0, -478, 2.8, "#e86aa0")}`;
  };
  wrapAcc("jkGod", godV(wOf("jkGod")));
  const godHair = hairOf("jkGod");
  wrapHead("jkGod", () => `<path d="M-30,-647Q4,-655 38,-647" stroke="#fff8d0" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".85"/><path d="M-30,-634Q4,-628 38,-634" stroke="#c89a20" stroke-width="2" fill="none" stroke-linecap="round" opacity=".6"/>
      <ellipse cx="4" cy="-641" rx="54" ry="16" fill="none" stroke="#fff0a0" stroke-width="1.6" opacity=".45"/>
      ${star(52, -652, 9)}${star(-36, -630, 7)}${star(16, -662, 6)}<circle cx="52" cy="-652" r="2" fill="#f2c24a"/><circle cx="-36" cy="-630" r="1.6" fill="#f2c24a"/>
      <path d="M-33,-529V-519" stroke="#f2c25a" stroke-width="1.6"/><circle cx="-33" cy="-515" r="3.4" fill="url(#jkv_gold)"/>
      ${strand("M-28,-582Q-4,-598 22,-588", godHair, 3, 0.45)}${strand("M-36,-556Q-34,-584 -14,-596", godHair, 2.2, 0.35)}`,
    () => `<ellipse cx="4" cy="-640" rx="62" ry="24" fill="url(#jkv_haloGlow)"/>`);

  // ---------------- the dead in the queue: a crumpled ticket, a number badge, faint prints ----------------
  const ticket = (n) => `<g transform="translate(14,-420) rotate(6)"><path d="M-22,-15L-6,-17L8,-14L22,-16L23,-2L20,13L4,15L-10,13L-23,14L-21,0Z" fill="#f6efe0"/>
    <path d="M-22,-15L-6,-17L-10,13L-23,14Z" fill="#000" opacity=".07"/><path d="M-22,-15L-6,-17L8,-14L22,-16L22,-12L8,-10L-6,-13L-22,-11Z" fill="#d8443a" opacity=".75"/>
    <path d="M-14,-11L-9,10M10,-10L6,12" stroke="#b8b0a0" stroke-width="1" opacity=".6"/><path d="M-19,-9V11" stroke="#b8b0a0" stroke-width="1.2" stroke-dasharray="2 2"/>
    <text x="1" y="-2" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="7" fill="#8a7a5a">คิว</text><text x="1" y="12" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="17" fill="#3a3a44">${n}</text></g>`;
  const badge = (n) => `<g transform="translate(-23,-452)"><path d="M-10,-8L7,5" stroke="#9aa0a8" stroke-width="1.8"/><circle cx="-10" cy="-8" r="2.1" fill="#c8ccd0"/><circle r="9.5" fill="#e8e2d6"/><circle r="9.5" fill="url(#jkv_btn)"/><circle r="6.8" fill="#f8f4ec" stroke="#8a8a92" stroke-width="1"/><text y="3.6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="10" fill="#3a3e4a">${n}</text></g>`;
  const PRINTS = {
    jkSoul1: (x) => `<path d="M-20,-412l3.5,7.5l8,1l-6,5.5l1.5,8l-7,-4l-7,4l1.5,-8l-6,-5.5l8,-1z" fill="${hi(x.top, 0.5)}" opacity=".3"/>`,
    jkSoul2: () => `<rect x="-44" y="-432" width="88" height="6" fill="#fff" opacity=".16"/><rect x="-44" y="-414" width="88" height="6" fill="#fff" opacity=".16"/>`,
    jkSoul3: (x) => `<circle cx="-18" cy="-400" r="9" fill="none" stroke="${hi(x.top, 0.5)}" stroke-width="3" opacity=".3"/><circle cx="-18" cy="-400" r="2.5" fill="${hi(x.top, 0.5)}" opacity=".3"/>`,
  };
  const soulV = (n, num) => (x) => { const top = x.top, slab = slabD(1, -296), hiT = hi(top, 0.35), dkT = dk(top, 0.3);
    return `<path d="${slab}" fill="url(#jkv_weave)"/>${shade(1, -296, 0.85)}
      <path d="M-18,-490Q0,-472 18,-490L16,-487Q0,-467 -16,-487Z" fill="${dk(top, 0.14)}"/>
      <rect x="-45" y="-303" width="90" height="7" fill="${dk(top, 0.1)}"/><path d="M-43,-299H43" stroke="${hiT}" stroke-width="1" stroke-dasharray="2 3" opacity=".5"/>
      <path d="M-34,-340q12,-5 24,0M12,-330q10,-4 22,0" stroke="${dkT}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".3"/>
      ${PRINTS[n](x)}
      <rect x="-42" y="-298" width="84" height="9" fill="#3a2c24"/><rect x="-5" y="-300" width="10" height="12" rx="2" fill="url(#jkv_gold)"/>
      ${badge(num)}${ticket(num)}`; };
  const SOUL_HAIR = { jkSoul1: "M-24,-584Q0,-596 22,-588", jkSoul2: "M-26,-586Q0,-600 24,-590", jkSoul3: "M-22,-582Q0,-592 20,-586" };
  [["jkSoul1", 4], ["jkSoul2", 7], ["jkSoul3", 9]].forEach(([n, num]) => { wrapAcc(n, soulV(n, num)); const hc = hairOf(n); wrapHead(n, () => strand(SOUL_HAIR[n], hc, 2.8, 0.4)); });

  // ---------------- the customer in the café: a floral blouse, pearls, a handbag ----------------
  const flower = (px, py, r, c) => `<g fill="${c}" opacity=".45">${[0, 72, 144, 216, 288].map((a) => { const t = (a * Math.PI) / 180; return `<circle cx="${f(px + Math.cos(t) * r)}" cy="${f(py + Math.sin(t) * r)}" r="${f(r * 0.7)}"/>`; }).join("")}</g><circle cx="${f(px)}" cy="${f(py)}" r="${f(r * 0.5)}" fill="#f6d36a" opacity=".6"/>`;
  const auntV = (w) => (x) => { const top = x.top, slab = slabD(w, -296), dkT = dk(top, 0.3), X = (v) => f(v * w);
    return `<path d="${slab}" fill="url(#jkv_weave)"/>${shade(w, -296, 0.85)}
      ${[[-30, -440], [-10, -392], [-34, -358], [28, -452], [36, -398], [12, -344], [34, -330]].map(([px, py]) => flower(px, py, 4.5, hi(top, 0.4))).join("")}
      <path d="M-34,-320q12,-5 24,0M14,-312q10,-4 22,0" stroke="${dkT}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".35"/>
      <path d="M-20,-490Q-10,-474 0,-472Q10,-474 20,-490L25,-485Q12,-463 0,-461Q-12,-463 -25,-485Z" fill="${hi(top, 0.45)}"/><path d="M-25,-485Q-12,-463 0,-461Q12,-463 25,-485" stroke="${dk(top, 0.2)}" stroke-width="1.6" fill="none" opacity=".6"/>
      <rect x="${X(-45)}" y="-302" width="${X(90)}" height="8" fill="${dk(top, 0.35)}"/><rect x="-4" y="-303" width="8" height="10" rx="1.5" fill="url(#jkv_gold)"/>
      <path d="M${X(30)},-486L${X(-42)},-318" stroke="#5a3a24" stroke-width="6" stroke-linecap="round"/><path d="M${X(30)},-487L${X(-42)},-319" stroke="#a8784e" stroke-width="1.6" stroke-linecap="round" opacity=".5"/>
      <g transform="translate(${X(-44)},-316)"><rect x="-16" y="-14" width="34" height="28" rx="5" fill="#6a4228"/><rect x="-16" y="-14" width="34" height="28" rx="5" fill="url(#jkv_lit)"/><path d="M-16,-14H18L16,-2H-14Z" fill="#4e3220"/><rect x="-3" y="-6" width="8" height="6" rx="1" fill="#d8b84a"/></g>
      <path d="M-16,-490Q0,-452 16,-490" stroke="#e8d8a0" stroke-width="1.4" fill="none"/>${beads([-16, -490], [0, -452], [16, -490], 11, 2.6, "#f6f0e4")}
      <circle cx="0" cy="-458" r="5" fill="url(#jkv_gold)"/>${gem(0, -458, 2.8, "#e86aa0")}`; };
  wrapAcc("jkAunt", auntV(wOf("jkAunt")));
  const auntHair = hairOf("jkAunt");
  wrapHead("jkAunt", () => strand("M-16,-608q6,-9 16,-6", auntHair, 2.4, 0.5) + strand("M6,-610q7,-8 16,-4", auntHair, 2.4, 0.5) + strand("M26,-602q6,-6 14,-3", auntHair, 2.2, 0.45)
    + `<circle cx="-33" cy="-529" r="3.6" fill="none" stroke="#e8c86a" stroke-width="1.8"/>`);

  // ---------------- plaza bystanders ----------------
  const man1V = (w) => (x) => { const LEA = "#7a5232", X = (v) => f(v * w);
    return `${shade(w, -296, 0.85)}
      <path d="M${X(-22)},-470L${X(-31)},-492M${X(22)},-470L${X(31)},-492" stroke="#5a3a24" stroke-width="5" stroke-linecap="round"/>
      <path d="M${X(-22)},-470H${X(22)}L${X(24)},-340H${X(44)}L${X(46)},-296H${X(-46)}L${X(-44)},-340H${X(-24)}Z" fill="url(#jkv_leather)"/>
      <path d="M${X(-22)},-470H${X(22)}L${X(24)},-340H${X(44)}L${X(46)},-296H${X(-46)}L${X(-44)},-340H${X(-24)}Z" fill="url(#jkv_cyl)" opacity=".6"/>
      <path d="M${X(-20)},-468H${X(20)}" stroke="${hi(LEA, 0.4)}" stroke-width="1.6" opacity=".7"/><path d="M${X(-44)},-340H${X(44)}" stroke="#3a2418" stroke-width="3.5"/>
      <rect x="-12" y="-440" width="24" height="22" rx="2" fill="${dk(LEA, 0.18)}"/><path d="M-12,-440H12V-418H-12Z" stroke="#e8d0a8" stroke-width="1" stroke-dasharray="2 3" fill="none" opacity=".5"/>
      <rect x="-4" y="-454" width="4.5" height="16" fill="#f2c230"/><path d="M-4,-454l2.2,-5l2.3,5z" fill="#ead2ac"/>
      <rect x="${X(28)}" y="-336" width="10" height="26" rx="3" fill="${dk(LEA, 0.3)}"/><path d="M${X(33)},-362V-320" stroke="#5a5e66" stroke-width="4" stroke-linecap="round"/><rect x="${f(33 * w - 6)}" y="-368" width="12" height="8" rx="2" fill="#8a8e96"/>
      <rect x="${X(-40)}" y="-330" width="14" height="14" rx="1" fill="#9a7a58"/><rect x="${X(-40)}" y="-330" width="14" height="14" rx="1" fill="none" stroke="#e8d0a8" stroke-width="1" stroke-dasharray="2 2" opacity=".6"/>`; };
  wrapAcc("jkMan1", man1V(wOf("jkMan1")));
  const man2V = (w) => (x) => { const top = x.top, X = (v) => f(v * w), G = "#3a7a58";
    return `<path d="${slabD(w, -296)}" fill="url(#jkv_weave)"/>${shade(w, -296, 0.85)}
      <path d="M-34,-330q12,-5 24,0" stroke="${dk(top, 0.3)}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".35"/>
      <rect x="${X(-45)}" y="-301" width="${X(90)}" height="8" fill="#3a2a20"/><rect x="-4" y="-302" width="8" height="10" rx="1.5" fill="url(#jkv_gold)"/>
      <rect x="${X(-40)}" y="-330" width="16" height="14" rx="2" fill="${dk(top, 0.25)}"/><rect x="${X(-40)}" y="-330" width="16" height="14" rx="2" fill="none" stroke="${hi(top, 0.4)}" stroke-width="1" stroke-dasharray="2 2" opacity=".7"/>
      <circle cx="${X(24)}" cy="-420" r="9" fill="#c8a050"/><circle cx="${X(24)}" cy="-420" r="9" fill="none" stroke="#f0e0b0" stroke-width="1.2" stroke-dasharray="2 2"/><path d="M${f(24 * w - 4)},-420h8M${X(24)},-424v8" stroke="#6a4a2a" stroke-width="2" stroke-linecap="round"/>
      <path d="M-24,-490Q0,-462 24,-490L28,-480Q0,-446 -28,-480Z" fill="url(#jkv_scarfG)"/><path d="M-22,-488Q0,-462 22,-488" stroke="${hi(G, 0.4)}" stroke-width="1.8" fill="none" opacity=".6"/>
      <path d="M8,-462L2,-430L12,-436Z" fill="${dk(G, 0.1)}"/><path d="M12,-462L20,-432L24,-442Z" fill="${dk(G, 0.25)}"/><ellipse cx="10" cy="-466" rx="6.5" ry="5" fill="${G}"/><path d="M5,-469q5,-3 10,0" stroke="${hi(G, 0.45)}" stroke-width="1.6" fill="none" opacity=".7"/>`; };
  wrapAcc("jkMan2", man2V(wOf("jkMan2")));
  const man3V = (w) => (x) => { const X = (v) => f(v * w), CR = "#e0d4ba";
    return `${shade(w, -296, 0.85)}
      <path d="M${X(-26)},-466Q0,-502 ${X(26)},-466" stroke="#e8dcc4" stroke-width="5" fill="none"/>
      <path d="M${X(-26)},-466H${X(26)}L${X(28)},-348H${X(52)}L${X(52)},-296H${X(-52)}L${X(-52)},-348H${X(-28)}Z" fill="url(#jkv_cream)"/>
      <path d="M${X(-26)},-466H${X(26)}L${X(28)},-348H${X(52)}L${X(52)},-296H${X(-52)}L${X(-52)},-348H${X(-28)}Z" fill="url(#jkv_cyl)" opacity=".5"/>
      <path d="M${X(-52)},-348H${X(52)}" stroke="#e8dcc4" stroke-width="4"/><path d="M${X(-52)},-346H${X(52)}" stroke="${dk(CR, 0.25)}" stroke-width="1.4" opacity=".6"/>
      <ellipse cx="${X(46)}" cy="-352" rx="7" ry="4" fill="#e8dcc4" transform="rotate(-25 ${X(46)} -352)"/><ellipse cx="${X(50)}" cy="-344" rx="7" ry="4" fill="#dccfb4" transform="rotate(30 ${X(50)} -344)"/><path d="M${X(48)},-346l3,14M${X(50)},-346l6,12" stroke="#dccfb4" stroke-width="3" stroke-linecap="round"/>
      <rect x="-16" y="-404" width="32" height="24" rx="2" fill="${dk(CR, 0.08)}"/><path d="M-16,-404H16" stroke="${dk(CR, 0.25)}" stroke-width="1.6"/><rect x="2" y="-430" width="5" height="28" rx="2" fill="#a8784e"/><ellipse cx="4.5" cy="-432" rx="5" ry="3.5" fill="#b8886a"/>
      <ellipse cx="-24" cy="-380" rx="9" ry="5" fill="#fff" opacity=".5"/><ellipse cx="26" cy="-330" rx="7" ry="4" fill="#fff" opacity=".45"/><ellipse cx="-30" cy="-318" rx="6" ry="4" fill="${dk(CR, 0.2)}" opacity=".45"/>`; };
  wrapAcc("jkMan3", man3V(wOf("jkMan3")));
  const wom1V = (w) => (x) => { const X = (v) => f(v * w), T = "#3a6c6a";
    return `<path d="${slabD(w, -296)}" fill="url(#jkv_weave)"/>${shade(w, -296, 0.85)}
      <rect x="${X(-45)}" y="-304" width="${X(90)}" height="10" fill="#a8484a"/><path d="M${X(-45)},-304H${X(45)}" stroke="#c86a6a" stroke-width="1.6" opacity=".7"/><ellipse cx="${X(34)}" cy="-300" rx="6" ry="4.5" fill="#b85858"/><path d="M${X(36)},-298l4,12M${X(32)},-297l-2,12" stroke="#a8484a" stroke-width="3" stroke-linecap="round"/>
      <path d="M${X(-46)},-486Q${X(-30)},-500 ${X(-16)},-492L${X(-4)},-470L${X(-16)},-300H${X(-46)}Z" fill="url(#jkv_shawl)"/><path d="M${X(46)},-486Q${X(30)},-500 ${X(16)},-492L${X(4)},-470L${X(16)},-300H${X(46)}Z" fill="url(#jkv_shawl)"/>
      <path d="M${X(-4)},-470L${X(-16)},-300M${X(4)},-470L${X(16)},-300" stroke="${hi(T, 0.4)}" stroke-width="1.8" opacity=".6"/>
      ${[-42, -36, -30, -24, -18, 18, 24, 30, 36, 42].map((bx) => `<path d="M${X(bx)},-300v9" stroke="${T}" stroke-width="2" stroke-linecap="round"/>`).join("")}
      <path d="M-14,-490Q0,-456 14,-490" stroke="#8a5a32" stroke-width="1.4" fill="none"/>${beads([-14, -490], [0, -456], [14, -490], 9, 2.4, "#8a5a32", "#d8b088")}<circle cx="0" cy="-460" r="4" fill="url(#jkv_gold)"/>`; };
  wrapAcc("jkWom1", wom1V(wOf("jkWom1")));
  const BY_HAIR = { jkMan1: "M-22,-582Q0,-592 20,-586", jkMan2: "M-20,-588Q4,-598 26,-590" };
  Object.entries(BY_HAIR).forEach(([n, d]) => { const hc = hairOf(n); wrapHead(n, () => strand(d, hc, 2.8, 0.42)); });
  wrapHead("jkMan3", () => `<path d="M-14,-582Q4,-592 20,-584" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".22"/>`);   // a shine on the bald top
  const womHair = hairOf("jkWom1");
  wrapHead("jkWom1", () => strand("M-20,-586Q4,-594 26,-586", womHair, 2.8, 0.42) + strand("M-38,-606q8,-8 16,-4", womHair, 2.4, 0.42));   // a strand + the bun

  window.JKV = window.JKV || {};
  JKV.cast = { suitV, kenV, godV, soulV, auntV, ticket, badge };
})();
