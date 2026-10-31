// Rig v2: the same skeleton, joints and ids as rig.js (so every pose mode, track and shot keeps working), drawn as
// illustrated characters instead of capsule puppets: tapered limbs with form shading, a shaped skull and jaw, eyes with
// iris and catch-lights, hair in two layers (#id-hairB behind the torso follows the head), clothes with folds and hems,
// shaped hands and shoes, a soft contact shadow. Thin warm line instead of the heavy black outline.
// A cast entry opts in with v2: { ... } (see the spec below); Rig.build falls back to the old builder otherwise.
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const LINE = "#3a2622";
  const f = (v) => (+v).toFixed(1);
  const rgb = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.substr(i, 2), 16)); };
  const hex = (a) => "#" + a.map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
  const mix = (a, b, k) => { const A = rgb(a), B = rgb(b); return hex(A.map((v, i) => v + (B[i] - v) * k)); };
  const dk = (c, k) => mix(c, "#000000", k);
  // shadows lean cool and violet, never plain grey
  const shade = (c, k = 0.24) => mix(dk(c, k), "#3b2a5c", 0.14);
  const hi = (c, k = 0.25) => mix(c, "#fff6e6", k);

  Sets.DEFS += `
    <linearGradient id="r2Cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c1030" stop-opacity=".26"/><stop offset=".28" stop-color="#1c1030" stop-opacity="0"/>
      <stop offset=".66" stop-color="#1c1030" stop-opacity="0"/><stop offset="1" stop-color="#1c1030" stop-opacity=".3"/></linearGradient>
    <linearGradient id="r2AO" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1030" stop-opacity=".22"/><stop offset=".22" stop-color="#1c1030" stop-opacity="0"/>
      <stop offset=".8" stop-color="#1c1030" stop-opacity="0"/><stop offset="1" stop-color="#1c1030" stop-opacity=".28"/></linearGradient>
    <radialGradient id="r2Head" cx=".42" cy=".38" r=".66"><stop offset=".55" stop-color="#3a1424" stop-opacity="0"/><stop offset="1" stop-color="#3a1424" stop-opacity=".3"/></radialGradient>
    <radialGradient id="r2Blush"><stop offset="0" stop-color="#ff6a7a" stop-opacity=".42"/><stop offset="1" stop-color="#ff6a7a" stop-opacity="0"/></radialGradient>
    <radialGradient id="r2Contact"><stop offset="0" stop-color="#0a0608" stop-opacity=".55"/><stop offset=".6" stop-color="#0a0608" stop-opacity=".25"/><stop offset="1" stop-color="#0a0608" stop-opacity="0"/></radialGradient>
    <radialGradient id="r2EyeGlow"><stop offset="0" stop-color="#d8ff9a" stop-opacity=".75"/><stop offset=".45" stop-color="#7dff6a" stop-opacity=".25"/><stop offset="1" stop-color="#7dff6a" stop-opacity="0"/></radialGradient>`;

  // a tapered limb from (0,0) to (0,len): rounded ends overlap the joints, a slight swell at the top third
  const limbD = (len, w0, w1, sw = 2) => {
    const a = w0 / 2, b = w1 / 2;
    return `M${f(-a)},0C${f(-a)},${f(-a * 1.3)} ${f(a)},${f(-a * 1.3)} ${f(a)},0Q${f(a + sw)},${f(len * 0.38)} ${f(b)},${f(len)}` +
      `C${f(b)},${f(len + b * 1.3)} ${f(-b)},${f(len + b * 1.3)} ${f(-b)},${f(len)}Q${f(-a - sw * 0.6)},${f(len * 0.38)} ${f(-a)},0Z`;
  };
  const paint = (d, fill, o = {}) => `<path d="${d}" fill="${fill}" stroke="${o.line || LINE}" stroke-width="${o.sw ?? 2.6}" stroke-linejoin="round"/>` +
    (o.cyl === false ? "" : `<path d="${d}" fill="url(#r2Cyl)"/>`) + (o.ao ? `<path d="${d}" fill="url(#r2AO)"/>` : "");

  // ---------------- face ----------------
  const EX = [-17, 19], EY = -548;
  function eyeSet(P) {
    const iris = P.iris || "#4a2e20", brow = P.brow || P.hair.c, lid = LINE, lash = P.lash;
    const sclera = (rx, ry, dy = 0) => EX.map((x) => `<ellipse cx="${x}" cy="${EY + dy}" rx="${rx}" ry="${ry}" fill="#fbf7f0" stroke="${lid}" stroke-width="1.6"/>`).join("");
    const pupil = (r, dx = 1.5, dy = 1) => EX.map((x) => `<circle cx="${x + dx}" cy="${EY + dy}" r="${r}" fill="${iris}"/><circle cx="${x + dx}" cy="${EY + dy}" r="${f(r * 0.55)}" fill="#160e0c"/>
      <circle cx="${f(x + dx - r * 0.38)}" cy="${f(EY + dy - r * 0.45)}" r="${f(Math.max(1.6, r * 0.32))}" fill="#fff"/><circle cx="${f(x + dx + r * 0.35)}" cy="${f(EY + dy + r * 0.42)}" r="1" fill="#fff" opacity=".8"/>`).join("");
    const lids = (lift = 0) => EX.map((x, i) => `<path d="M${x - 10},${EY - 3 - lift}Q${x},${EY - 15 - lift} ${x + 10},${EY - 4 - lift}" stroke="${lid}" stroke-width="3.4" fill="none" stroke-linecap="round"/>` +
      (lash ? `<path d="M${x + (i ? 10 : -10)},${EY - 4 - lift}l${i ? 4 : -4},-4" stroke="${lid}" stroke-width="2.6" stroke-linecap="round"/>` : "")).join("");
    const brows = (ty = 0, tilt = 0) => EX.map((x, i) => { const s = i ? 1 : -1, inner = -tilt * 1, outer = tilt * 0.6;
      return `<path d="M${x - 11},${EY - 20 + ty + (s < 0 ? outer : inner)}Q${x},${EY - 26 + ty} ${x + 11},${EY - 20 + ty + (s < 0 ? inner : outer)}" stroke="${brow}" stroke-width="4.6" fill="none" stroke-linecap="round"/>`; }).join("");
    const bags = P.bags ? EX.map((x) => `<path d="M${x - 9},${EY + 9}q9,7 18,0" stroke="${shade(P.skin, 0.3)}" stroke-width="3" fill="none" opacity=".8"/>`).join("") : "";
    return {
      normal: sclera(8.6, 10.4) + pupil(6.8) + lids() + brows() + bags,
      side: sclera(8.6, 9.6) + pupil(6.4, 4.2, 1.5) + EX.map((x) => `<path d="M${x - 10},${EY - 2}Q${x},${EY - 12} ${x + 10},${EY - 3}L${x + 10},${EY - 10}H${x - 10}Z" fill="${P.skin}"/>`).join("") +
        EX.map((x) => `<path d="M${x - 10},${EY - 2}Q${x},${EY - 10} ${x + 10},${EY - 3}" stroke="${lid}" stroke-width="3.4" fill="none" stroke-linecap="round"/>`).join("") + brows(2, -2) + bags,
      wide: sclera(10, 12.4, -1) + pupil(4.6, 0.5, -1) + lids(3) + brows(-7, -2) + bags,
      closed: EX.map((x) => `<path d="M${x - 9},${EY + 1}Q${x},${EY + 7} ${x + 9},${EY + 1}" stroke="${lid}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`).join("") + brows(2) + bags,
      pain: EX.map((x, i) => { const s = i ? -1 : 1; return `<path d="M${x - 9 * s},${EY - 5}L${x + 6 * s},${EY}L${x - 9 * s},${EY + 5}" stroke="${lid}" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`; }).join("") + brows(4, 6),
      glow: EX.map((x) => `<circle cx="${x}" cy="${EY}" r="22" fill="url(#r2EyeGlow)"/><ellipse cx="${x}" cy="${EY}" rx="9" ry="10" fill="#c8ff9a"/><ellipse cx="${x}" cy="${EY}" rx="4" ry="5" fill="#f4ffe8"/>`).join("") + brows(4, 7),
      dead: EX.map((x) => `<ellipse cx="${x}" cy="${EY}" rx="11" ry="10" fill="#22201c" opacity=".55"/><ellipse cx="${x}" cy="${EY}" rx="8.6" ry="9.6" fill="#e6eadc" stroke="${lid}" stroke-width="1.6"/><circle cx="${x + 2}" cy="${EY + 1}" r="2" fill="#5a1010"/>`).join("") + brows(3, 5),
      worry: sclera(8.6, 10.4) + pupil(6.2, 1, 1.5) + lids() + brows(-3, -6) + bags,
      angry: sclera(8.6, 8.8, 1) + pupil(6, 1.5, 2) + lids(-2) + brows(5, 7) + bags,
    };
  }
  function mouthSet(P) {
    const lip = P.lip || shade(P.skin, 0.32), inner = "#5a1e1e", tongue = "#d86a6a";
    return {
      smile: `<path d="M-5,-519Q4,-510 14,-519" stroke="${LINE}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M-1,-512q5,2 10,0" stroke="${lip}" stroke-width="2" fill="none" opacity=".6"/>`,
      flat: `<path d="M-4,-516Q4,-514 12,-516" stroke="${LINE}" stroke-width="3" fill="none" stroke-linecap="round"/>`,
      o: `<path d="M-1,-522Q4,-525 9,-522Q12,-512 4,-507Q-4,-512 -1,-522Z" fill="${inner}" stroke="${LINE}" stroke-width="2.4"/><path d="M0,-511q4,-3 8,0" fill="${tongue}"/>`,
      frown: `<path d="M-5,-511Q4,-519 14,-511" stroke="${LINE}" stroke-width="3" fill="none" stroke-linecap="round"/>`,
      scream: `<path d="M-9,-524Q4,-528 17,-524Q16,-500 4,-497Q-8,-500 -9,-524Z" fill="${inner}" stroke="${LINE}" stroke-width="2.6"/>
        <path d="M-7,-523Q4,-526 15,-523L14,-519Q4,-521 -6,-519Z" fill="#f4eee2"/><path d="M-3,-503q7,-6 14,0q-7,4 -14,0z" fill="${tongue}"/>`,
      snarl: `<path d="M-15,-526Q4,-534 23,-526L20,-506Q4,-498 -12,-506Z" fill="#220505" stroke="${LINE}" stroke-width="2.6"/>
        <path d="M-12,-525l3,6l3,-6l3,6l3,-6l3,6l3,-6l3,6l3,-6l3,6" stroke="#ece4cf" stroke-width="2.4" fill="none" stroke-linejoin="round"/>`,
      laugh: `<path d="M-7,-522Q4,-524 16,-522Q14,-506 4,-505Q-6,-506 -7,-522Z" fill="${inner}" stroke="${LINE}" stroke-width="2.6"/><path d="M-5,-521Q4,-523 14,-521L13,-518Q4,-519 -4,-518Z" fill="#f4eee2"/>`,
    };
  }

  // ---------------- clothes ----------------
  // torso outlines by cut; all share the neck at y -488 and the hem near -296
  function torsoD(kind, w = 1) {
    const X = (x) => f(x * w);
    if (kind === "tank") return `M${X(-20)},-488Q0,-472 ${X(20)},-488L${X(32)},-488Q${X(36)},-460 ${X(56)},-450L${X(57)},-424Q${X(55)},-360 ${X(58)},-298Q0,-288 ${X(-58)},-298Q${X(-55)},-360 ${X(-57)},-424L${X(-56)},-450Q${X(-36)},-460 ${X(-32)},-488Z`;
    if (kind === "coat") return `M${X(-22)},-492Q0,-480 ${X(22)},-492L${X(46)},-486Q${X(64)},-480 ${X(64)},-456L${X(62)},-420Q${X(64)},-330 ${X(72)},-230Q0,-218 ${X(-72)},-230Q${X(-64)},-330 ${X(-62)},-420L${X(-64)},-456Q${X(-64)},-480 ${X(-46)},-486Z`;
    // tee / shirt / blouse / singlet base: rounded shoulders, a slight waist, a soft hem
    return `M${X(-22)},-490Q0,-478 ${X(22)},-490L${X(46)},-485Q${X(64)},-479 ${X(64)},-456L${X(61)},-424Q${X(56)},-370 ${X(62)},-296Q${X(30)},-288 0,-290Q${X(-30)},-288 ${X(-62)},-296Q${X(-56)},-370 ${X(-61)},-424L${X(-64)},-456Q${X(-64)},-479 ${X(-46)},-485Z`;
  }

  function build2(parent, id, P) {
    const V = P.v2, skin = V.skin, skinS = shade(skin, 0.2), skinD = shade(skin, 0.34), top = V.top.c, w = V.w || 1, k = V.limb || 1;
    const hair = { c: V.hair.c, s: V.hair.s || shade(V.hair.c, 0.35), sh: V.hair.sh || hi(V.hair.c, 0.35) };
    const ctx = { skin, skinS, skinD, hair, top, topS: shade(top), LINE, id };
    const back = (c) => dk(c, 0.1);

    // ---- legs ----
    const bt = V.bottom, pc = bt.c;
    const leg = (side) => {
      const B = side === "B", c = B ? back(pc) : pc, sk = B ? back(skin) : skin;
      let thigh, shin;
      const tw0 = 46 * k, tw1 = 36 * k, sw0 = 35 * k, sw1 = 26 * k;
      if (bt.kind === "shorts") {
        thigh = paint(limbD(150, tw0 - 6, tw1 - 6), sk) + paint(`M${f(-tw0 / 2 - 3)},-24H${f(tw0 / 2 + 3)}L${f(tw0 / 2 + 5)},92Q0,98 ${f(-tw0 / 2 - 5)},92Z`, c, { ao: true }) +
          `<path d="M${f(-tw0 / 2 - 4)},84Q0,90 ${f(tw0 / 2 + 4)},84" stroke="${shade(c, 0.3)}" stroke-width="3" fill="none"/>`;
        shin = paint(limbD(138, sw0 - 6, sw1 - 4), sk);
      } else {
        const flare = bt.kind === "sarong" ? 10 : 0;
        thigh = paint(limbD(150, tw0 + flare, tw1 + flare), c) + (bt.kind === "jeans" ? `<path d="M${f(tw0 / 2 - 7)},-8Q${f(tw0 / 2 - 4)},80 ${f(tw1 / 2 - 6)},150" stroke="${shade(c, 0.3)}" stroke-width="2" fill="none" opacity=".6"/>` : "") +
          `<path d="M${f(-tw0 / 2 + 8)},40q8,14 18,12" stroke="${shade(c, 0.32)}" stroke-width="2.4" fill="none" opacity=".55"/>`;
        shin = paint(limbD(132, sw0 + flare, sw1 + flare + 2), c) +
          (bt.kind === "jeans" ? `<path d="M${f(-sw1 / 2 - 2)},112H${f(sw1 / 2 + 2)}L${f(sw1 / 2 + 3)},128H${f(-sw1 / 2 - 3)}Z" fill="${hi(c, 0.22)}" stroke="${LINE}" stroke-width="2.2"/>` : "") +
          (bt.kind === "sarong" ? `<path d="M${f(-sw1 / 2 - flare / 2 - 1)},104H${f(sw1 / 2 + flare / 2 + 1)}" stroke="${bt.band || "#d8a83a"}" stroke-width="7"/><path d="M${f(-sw1 / 2 - flare / 2)},116H${f(sw1 / 2 + flare / 2)}" stroke="${bt.band2 || "#a8342a"}" stroke-width="4"/>` : "") +
          `<path d="M${f(-sw0 / 2 + 6)},30q6,30 2,60" stroke="${shade(c, 0.3)}" stroke-width="2.2" fill="none" opacity=".45"/>`;
      }
      const ft = V.feet || { kind: "bare" };
      let foot;
      if (ft.kind === "sneaker") {
        const sc = B ? back(ft.c || "#f4f2ec") : ft.c || "#f4f2ec";
        foot = `<path d="M-17,120Q-18,108 -6,108H10Q18,110 22,122Q40,126 42,140V146H-19Q-21,134 -17,120Z" fill="${sc}" stroke="${LINE}" stroke-width="2.6" stroke-linejoin="round"/>
          <path d="M-19,140H42" stroke="${ft.sole || "#d8d2c4"}" stroke-width="6"/><path d="M-19,146H42" stroke="${LINE}" stroke-width="2.6"/>
          <path d="M8,116l8,8M14,114l8,8" stroke="${ft.lace || "#b8b2a6"}" stroke-width="2.4" stroke-linecap="round"/>${ft.mark ? `<path d="M-8,132q14,-10 30,0" stroke="${ft.mark}" stroke-width="3.5" fill="none"/>` : ""}`;
      } else if (ft.kind === "boot") {
        const bc = B ? back(ft.c) : ft.c;
        foot = `<path d="M-19,50H19L20,124Q38,128 40,142V148H-20Z" fill="${bc}" stroke="${LINE}" stroke-width="2.6" stroke-linejoin="round"/><path d="M-19,50H19L20,124Q38,128 40,142V148H-20Z" fill="url(#r2Cyl)"/>
          <path d="M-21,50H21V60H-21Z" fill="${hi(bc, 0.2)}" stroke="${LINE}" stroke-width="2.2"/><path d="M-20,142H40" stroke="${dk(bc, 0.35)}" stroke-width="5"/>`;
      } else { // bare feet, optionally a sandal strap
        const sk2 = B ? back(skin) : skin;
        foot = `<path d="M-13,118Q-14,110 -4,110H8Q14,114 18,124Q34,128 36,138Q36,144 28,144H-14Q-17,132 -13,118Z" fill="${sk2}" stroke="${LINE}" stroke-width="2.4" stroke-linejoin="round"/>
          <path d="M22,136v6M28,136v6" stroke="${skinD}" stroke-width="1.6"/>${ft.kind === "sandal" ? `<path d="M-15,144H38" stroke="${ft.c || "#6a4a2a"}" stroke-width="5"/><path d="M6,118q6,10 16,8" stroke="${ft.c || "#6a4a2a"}" stroke-width="4" fill="none"/>` : ""}`;
      }
      return `<g id="${id}-th${side}"><g>${thigh}</g><g transform="translate(0,150)"><g id="${id}-sh${side}">${shin}${foot}</g></g></g>`;
    };

    // ---- arms ----
    const tp = V.top;
    const arm = (side, extra = "") => {
      const B = side === "B", tc = B ? back(top) : top, sk = B ? back(skin) : skin;
      const sl = tp.sleeve || "short";
      const uw0 = 31 * k, uw1 = 25 * k, fw0 = 25 * k, fw1 = 19 * k;
      let upper = paint(limbD(122, uw0, uw1), sl === "none" ? sk : (sl === "long" || sl === "elbow") ? tc : sk);
      if (sl === "short") upper += paint(`M${f(-uw0 / 2 - 4)},-10Q${f(-uw0 / 2 - 2)},-34 0,-34Q${f(uw0 / 2 + 2)},-34 ${f(uw0 / 2 + 4)},-10L${f(uw0 / 2 + 7)},58Q0,66 ${f(-uw0 / 2 - 7)},58Z`, tc, { ao: true }) +
        `<path d="M${f(-uw0 / 2 - 5)},52Q0,60 ${f(uw0 / 2 + 5)},52" stroke="${shade(tc, 0.28)}" stroke-width="2.6" fill="none"/>`;
      if (sl === "elbow") upper += `<path d="M${f(-uw1 / 2 - 4)},110Q0,120 ${f(uw1 / 2 + 4)},110" stroke="${tp.trim || shade(tc, 0.25)}" stroke-width="5" fill="none" stroke-dasharray="${tp.lace ? "5 3" : "none"}"/>`;
      const fc = sl === "long" ? tc : sk;
      let fore = paint(limbD(106, fw0, fw1), fc);
      if (sl === "long") fore += `<path d="M${f(-fw1 / 2 - 3)},92H${f(fw1 / 2 + 3)}L${f(fw1 / 2 + 2)},104H${f(-fw1 / 2 - 2)}Z" fill="${shade(tc, 0.12)}" stroke="${LINE}" stroke-width="2.2"/>`;
      if (sl === "elbow" || sl === "short" || sl === "none") fore += `<path d="M-6,30q4,20 0,40" stroke="${skinS}" stroke-width="2" fill="none" opacity=".5"/>`;
      // the hand: a palm with the thumb folded forward, fingers suggested
      const hc = sk;
      const hand = `<path d="M-11,104Q-14,118 -10,128Q-2,138 8,132Q14,124 12,108Z" fill="${hc}" stroke="${LINE}" stroke-width="2.4" stroke-linejoin="round"/>
        <path d="M9,108Q19,112 16,122Q13,126 9,122" fill="${hc}" stroke="${LINE}" stroke-width="2.2" stroke-linejoin="round"/>
        <path d="M-6,124q4,4 9,3" stroke="${skinD}" stroke-width="1.6" fill="none"/>${V.wristband && !B ? `<path d="M-11,98H11V106H-11Z" fill="${V.wristband}" stroke="${LINE}" stroke-width="2"/>` : ""}`;
      const tor = `<g id="${id}-torch" display="none" transform="translate(0,118)"><rect x="-9" y="-6" width="18" height="44" rx="4" fill="#3d3833" stroke="${LINE}" stroke-width="2.6"/>
          <path id="${id}-beam" d="M-8,38L-230,900H230L8,38Z" fill="url(#beamg)"/></g>`;
      return `<g id="${id}-ua${side}">${upper}<g transform="translate(0,122)"><g id="${id}-fa${side}">${fore}${hand}<g id="${id}-hand${side}">${side === "F" ? tor : ""}${extra}</g></g></g></g>`;
    };

    // ---- torso ----
    const tD = torsoD(tp.kind, w);
    let torso = "";
    if (tp.kind === "tank" || tp.kind === "singlet") // bare shoulders under the straps
      torso += paint(`M${f(-22 * w)},-492Q0,-482 ${f(22 * w)},-492L${f(48 * w)},-482Q${f(62 * w)},-474 ${f(60 * w)},-440L${f(-60 * w)},-440Q${f(-62 * w)},-474 ${f(-48 * w)},-482Z`, skin);
    torso += paint(tD, top, { ao: true });
    // folds: under the chest, the waist pull, the hem
    torso += `<path d="M${f(-40 * w)},-404q10,26 4,52M${f(36 * w)},-396q-6,30 2,56M${f(-20 * w)},-318q16,6 34,-2" stroke="${shade(top, 0.3)}" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".55"/>`;
    torso += typeof V.print === "function" ? V.print(ctx) : V.print || "";
    if (tp.neck === "collar") torso += `<path d="M${f(-24 * w)},-494L-2,-466L${f(-8 * w)},-500ZM${f(24 * w)},-494L2,-466L${f(8 * w)},-500Z" fill="${tp.collar || hi(top, 0.15)}" stroke="${LINE}" stroke-width="2.4" stroke-linejoin="round"/>
      <path d="M0,-466V-300" stroke="${shade(top, 0.3)}" stroke-width="2.4"/>${[-440, -400, -360, -322].map((y) => `<circle cx="4" cy="${y}" r="3.2" fill="${tp.button || hi(top, 0.4)}" stroke="${LINE}" stroke-width="1.4"/>`).join("")}`;
    else if (tp.kind !== "coat") torso += `<path d="M${f(-22 * w)},-490Q0,-478 ${f(22 * w)},-490" stroke="${shade(top, 0.22)}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
    if (tp.kind === "coat") torso += `<path d="M${f(-24 * w)},-492L-4,-420V-226M${f(24 * w)},-492L4,-420" stroke="${LINE}" stroke-width="2.4" fill="none"/>
      <path d="M${f(-22 * w)},-492L-4,-420L${f(-30 * w)},-446L${f(-34 * w)},-480Z M${f(22 * w)},-492L4,-420L${f(30 * w)},-446L${f(34 * w)},-480Z" fill="${hi(top, 0.3)}" stroke="${LINE}" stroke-width="2.2" stroke-linejoin="round"/>
      <rect x="${f(26 * w)}" y="-380" width="26" height="30" rx="3" fill="${shade(top, 0.08)}" stroke="${LINE}" stroke-width="2"/>`;
    // the pelvis joins the thighs under the hem (shorts / trousers / sarong)
    const pelvis = paint(`M${f(-46 * k)},-336H${f(46 * k)}L${f(45 * k)},-296Q${f(24 * k)},-276 0,-286Q${f(-24 * k)},-276 ${f(-45 * k)},-296Z`, pc, { cyl: false });

    // ---- head ----
    const headD = "M-45,-556C-47,-606 -20,-616 3,-616C28,-616 50,-604 49,-556C48,-526 37,-503 12,-496C3,-494 -6,-494 -14,-497C-36,-505 -45,-527 -45,-556Z";
    const ear = (x, s) => `<path d="M${x},-560q${s * 14},-6 ${s * 14},10q0,16 ${-s * 13},16" fill="${skin}" stroke="${LINE}" stroke-width="2.4"/><path d="M${x + s * 3},-552q${s * 7},2 ${s * 5},10" stroke="${skinD}" stroke-width="2" fill="none"/>`;
    const eyes = eyeSet({ ...V, skin, hair }), mouths = mouthSet({ ...V, skin });
    const eyeG = Object.entries(eyes).map(([n, v]) => `<g class="eye-${n}" display="${n === "normal" ? "inline" : "none"}">${v}</g>`).join("");
    const mouthG = Object.entries(mouths).map(([n, v]) => `<g class="mouth-${n}" display="${n === "smile" ? "inline" : "none"}">${v}</g>`).join("");
    const head = `${ear(-43, -1)}${ear(47, 1)}
      <path d="${headD}" fill="${skin}" stroke="${LINE}" stroke-width="2.6"/><path d="${headD}" fill="url(#r2Head)"/>
      <path d="M-40,-528Q-30,-500 -6,-496" stroke="${skinS}" stroke-width="5" fill="none" opacity=".35" stroke-linecap="round"/>
      <ellipse cx="-27" cy="-525" rx="11" ry="7" fill="url(#r2Blush)" opacity="${V.blush ?? 1}"/><ellipse cx="33" cy="-525" rx="11" ry="7" fill="url(#r2Blush)" opacity="${V.blush ?? 1}"/>
      <path d="M7,-538Q12,-530 9,-525Q4,-523 1,-526Q6,-528 7,-538Z" fill="${skinD}" opacity=".55"/><circle cx="4" cy="-531" r="1.6" fill="#fff" opacity=".35"/>
      ${V.face || ""}
      <g id="${id}-eyes">${eyeG}</g><g id="${id}-mouth">${mouthG}</g>
      <g id="${id}-hair">${typeof V.hair.front === "function" ? V.hair.front(ctx) : V.hair.front || ""}</g>${V.faceTop || ""}
      <g id="${id}-sweat" display="none"><path d="M44,-584c6,10 8,16 2,19c-6,-3 -6,-9 -2,-19z" fill="#cfe2e6" stroke="${LINE}" stroke-width="2"/></g>`;
    const neck = `<path d="M-14,-516L-15,-484Q0,-476 15,-484L14,-516Z" fill="${skinS}" stroke="${LINE}" stroke-width="2.4"/><path d="M-14,-506Q0,-494 14,-506" stroke="${skinD}" stroke-width="5" fill="none" opacity=".4"/>`;
    const hairB = typeof V.hair.back === "function" ? V.hair.back(ctx) : V.hair.back || "";

    const html = `<g id="${id}">
      <ellipse id="${id}-shadow" cx="0" cy="3" rx="${f(86 * w)}" ry="15" fill="url(#r2Contact)"/>
      <g id="${id}-root"><g id="${id}-body">
        <g transform="translate(-20,-300)">${leg("B")}</g>
        <g transform="translate(20,-300)">${leg("F")}</g>
        ${pelvis}
        <g transform="translate(-46,-455)">${arm("B", P.hand || "")}</g>
        <g id="${id}-torso">
          <g id="${id}-hairB"><g transform="translate(0,-500) scale(${V.headScale ?? 1.12}) translate(0,500)">${hairB}</g></g>
          ${neck}${torso}
          <g id="${id}-acc">${V.extra ? (typeof V.extra === "function" ? V.extra(ctx) : V.extra) : ""}</g>
          <g id="${id}-head"><g transform="translate(0,-500) scale(${V.headScale ?? 1.12}) translate(0,500)">${head}</g></g>
        </g>
        <g transform="translate(46,-455)">${arm("F", P.hand || "")}</g>
      </g></g></g>`;
    const g = document.createElementNS(NS, "g");
    g.innerHTML = html;
    parent.appendChild(g.firstElementChild);
    return document.getElementById(id);
  }

  const old = Rig.build;
  Rig.build = (parent, id, P) => (P && P.v2 ? build2(parent, id, P) : old(parent, id, P));
  window.Rig2 = { build2, mix, dk, hi, shade, LINE, limbD, paint };
})();
