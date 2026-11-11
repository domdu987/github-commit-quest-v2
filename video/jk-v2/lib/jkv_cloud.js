// สกิลจอมโกหก · look V detail pass for Sets.jkCloud (owner 11 Nov: "เขียนให้ละเอียด ฉากให้ละเอียดกว่านี้ … ห้ามใช้ fal.ai เจนภาพ").
// Everything here is hand-drawn SVG, no raster, no external assets: materials as vertical gradients (lit from above, warm key light from
// the upper left), chrome and brass bevels, edge highlights, contact shadows as radial gradients (no blur filters at all), textures as
// patterns (cloud wisps, cream wood grain, cloth weave, marble veins), small believable props, layered depth (far things paler).
// It wraps JKD.dress.jkCloud so it runs after the set and its depth dressing, before the cast. Loads after jkdepth.js.
//   sky   high cirrus streaks, a halo ring round the sun, faint stars
//   far   the gold gate rebuilt (marble steps, fluted pillars with capitals, arch with filigree beads and a star finial, pennants, a glow),
//         shaded cloud banks, haze strata, tiny far lanterns, sparkle stars
//   mid   shaded cloud puffs with rim light, the deco lanterns dressed (paper ribs, brass caps, tassel), two more lanterns that bob,
//         a gold harp left on a small cloud floating in the sky (right of the dome), drifting feathers
//   set   floor: radial shading, wisp texture, a lilac runner with gold edges along the queue, the "ยืนตรงนี้" ring under the hero,
//         two rows of shaded floor puffs, wisps, stars, petals, feathers (all inserted UNDER #id-hole so the hole still opens over them) ·
//         the machine: marble plinth with a step, cabinet material (lit red, side shading), chrome edge strips, corner bolts, speaker grille,
//         enamel title plate "สุ่มสกิล", bevelled coin button, chrome coin-slot plate with the "1 ชีวิต" price tag, chrome frame round the chute
//         and the "รับสกิลตรงนี้" plate, chrome base strip, chrome dome collar with marquee bulbs, capsules shaded with glints (under the glass),
//         the dome's fresnel rim, curved reflections, refraction band and a chrome cap with a gold knob, a chrome hub plate behind the crank ·
//         brass stanchions (gradient posts, collars, finial balls, hook rings, base discs), the velvet rope (core, sheen, dark underside, twist)
//         with tassels, the deco queue sign given a brass post, finial and gold plate frames, a floating "ต่อคิวสุ่มสกิล" arrow sign on a
//         small cloud with wings (bobs) · an act-front group on the counter: brass top strip, wood-grained frame, engraved nameplate
//         "เทพีประจำเคาน์เตอร์", an open ledger with a pen, inkpad and stamp (left), the bell shaded, the gum box shaded, a glass jar of gum (right)
//   fg    the two near puffs shaded, pastel bokeh discs (few), two soft feathers
//   glow  halos on the marquee bulbs that breathe (screen blend)
// Nothing is drawn over the goddess (x 1180…1340, y 880…1180), the queue's faces, #id-hole, #id-crank, #id-chute, #id-burst or the counter's sign.
(function () {
  window.JKV = window.JKV || {};
  if (JKV.cloud) return;   // idempotent
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const NS = "http://www.w3.org/2000/svg";
  const G = (layer, html) => { const g = document.createElementNS(NS, "g"); layer.appendChild(g); if (html) g.innerHTML = html; return g; };
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}${o.tf ? ` transform="${o.tf}"` : ""}>${text}</text>`;
  const Q = new URLSearchParams(location.search);   // ?nojkv=1 turns this pass off

  // ---------------- materials (ids prefixed jkv_c), added once ----------------
  Sets.DEFS += `
    <linearGradient id="jkv_cRedV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a74"/><stop offset=".16" stop-color="#e65044"/><stop offset=".6" stop-color="#d4403a"/><stop offset="1" stop-color="#9c1e1a"/></linearGradient>
    <linearGradient id="jkv_cRedH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset=".14" stop-color="#000" stop-opacity=".04"/><stop offset=".32" stop-color="#fff" stop-opacity=".2"/><stop offset=".52" stop-color="#fff" stop-opacity="0"/><stop offset=".82" stop-color="#000" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></linearGradient>
    <linearGradient id="jkv_cLitV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".3"/><stop offset=".3" stop-color="#fff" stop-opacity=".2"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
    <linearGradient id="jkv_cLit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>
    <linearGradient id="jkv_cChromeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".22" stop-color="#d4dbe2"/><stop offset=".48" stop-color="#7d8894"/><stop offset=".56" stop-color="#f2f5f8"/><stop offset=".8" stop-color="#a7b0ba"/><stop offset="1" stop-color="#58626e"/></linearGradient>
    <linearGradient id="jkv_cChromeH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#58626e"/><stop offset=".18" stop-color="#eaeff3"/><stop offset=".42" stop-color="#8a94a0"/><stop offset=".6" stop-color="#ffffff"/><stop offset=".82" stop-color="#a7b0ba"/><stop offset="1" stop-color="#4c5661"/></linearGradient>
    <linearGradient id="jkv_cGoldV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6c8"/><stop offset=".35" stop-color="#f2d270"/><stop offset=".72" stop-color="#c89a2c"/><stop offset="1" stop-color="#86601a"/></linearGradient>
    <linearGradient id="jkv_cGoldH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#86601a"/><stop offset=".22" stop-color="#fff2b4"/><stop offset=".5" stop-color="#e2be52"/><stop offset=".78" stop-color="#a47c22"/><stop offset="1" stop-color="#6a4c10"/></linearGradient>
    <radialGradient id="jkv_cBall" cx=".36" cy=".3" r=".74"><stop offset="0" stop-color="#fff" stop-opacity=".7"/><stop offset=".32" stop-color="#fff" stop-opacity=".12"/><stop offset=".72" stop-color="#000" stop-opacity=".04"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></radialGradient>
    <radialGradient id="jkv_cGlassHi" cx=".3" cy=".26" r=".72"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".28" stop-color="#fff" stop-opacity=".16"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cFresnel" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".8" stop-color="#dcecfa" stop-opacity="0"/><stop offset=".93" stop-color="#d2e6f8" stop-opacity=".3"/><stop offset="1" stop-color="#ffffff" stop-opacity=".6"/></radialGradient>
    <radialGradient id="jkv_cShadow"><stop offset="0" stop-color="#3c3a5a" stop-opacity=".42"/><stop offset=".5" stop-color="#3c3a5a" stop-opacity=".2"/><stop offset="1" stop-color="#3c3a5a" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cPuff" cx=".42" cy=".3" r=".74"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#fcfcff"/><stop offset=".82" stop-color="#eaedf8"/><stop offset="1" stop-color="#d6dcef"/></radialGradient>
    <radialGradient id="jkv_cPuffFar" cx=".42" cy=".3" r=".74"><stop offset="0" stop-color="#fffdfb"/><stop offset=".6" stop-color="#f8f3f5"/><stop offset="1" stop-color="#e6dee9"/></radialGradient>
    <radialGradient id="jkv_cGlow"><stop offset="0" stop-color="#fff9e4" stop-opacity=".9"/><stop offset=".4" stop-color="#ffe9ac" stop-opacity=".4"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cLamp"><stop offset="0" stop-color="#fff4d0" stop-opacity=".95"/><stop offset=".32" stop-color="#ffc070" stop-opacity=".5"/><stop offset="1" stop-color="#ff9a40" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cBokP"><stop offset="0" stop-color="#ffd2e4" stop-opacity=".6"/><stop offset=".72" stop-color="#ffd2e4" stop-opacity=".38"/><stop offset=".9" stop-color="#ffd2e4" stop-opacity=".08"/><stop offset="1" stop-color="#ffd2e4" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cBokG"><stop offset="0" stop-color="#fff0b8" stop-opacity=".6"/><stop offset=".72" stop-color="#fff0b8" stop-opacity=".38"/><stop offset=".9" stop-color="#fff0b8" stop-opacity=".08"/><stop offset="1" stop-color="#fff0b8" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cBokB"><stop offset="0" stop-color="#d4e8ff" stop-opacity=".6"/><stop offset=".72" stop-color="#d4e8ff" stop-opacity=".38"/><stop offset=".9" stop-color="#d4e8ff" stop-opacity=".08"/><stop offset="1" stop-color="#d4e8ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cBokL"><stop offset="0" stop-color="#e6dcff" stop-opacity=".6"/><stop offset=".72" stop-color="#e6dcff" stop-opacity=".38"/><stop offset=".9" stop-color="#e6dcff" stop-opacity=".08"/><stop offset="1" stop-color="#e6dcff" stop-opacity="0"/></radialGradient>
    <radialGradient id="jkv_cFloor" gradientUnits="userSpaceOnUse" cx="700" cy="1480" r="1300"><stop offset="0" stop-color="#ffffff" stop-opacity=".5"/><stop offset=".45" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#c4c8e2" stop-opacity=".55"/></radialGradient>
    <linearGradient id="jkv_cRunner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8bef0"/><stop offset=".55" stop-color="#a89cdc"/><stop offset="1" stop-color="#8678c4"/></linearGradient>
    <linearGradient id="jkv_cMarble" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdfa"/><stop offset=".55" stop-color="#e9e3dd"/><stop offset="1" stop-color="#b6aea8"/></linearGradient>
    <linearGradient id="jkv_cCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset=".6" stop-color="#f4ecd8"/><stop offset="1" stop-color="#d9ceb4"/></linearGradient>
    <linearGradient id="jkv_cShadeDown" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".36"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
    <linearGradient id="jkv_cShadeUp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".36"/></linearGradient>
    <linearGradient id="jkv_cHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6ea" stop-opacity="0"/><stop offset="1" stop-color="#fff6ea" stop-opacity=".75"/></linearGradient>
    <linearGradient id="jkv_cGate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff8d8"/><stop offset=".5" stop-color="#f2dc98"/><stop offset="1" stop-color="#d4b060"/></linearGradient>
    <linearGradient id="jkv_cGateH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c8a450"/><stop offset=".3" stop-color="#fff4c8"/><stop offset=".62" stop-color="#ecd088"/><stop offset="1" stop-color="#b89440"/></linearGradient>
    <radialGradient id="jkv_cGateGlow"><stop offset="0" stop-color="#fff9e2" stop-opacity=".9"/><stop offset=".35" stop-color="#ffeaa8" stop-opacity=".42"/><stop offset="1" stop-color="#ffe2a0" stop-opacity="0"/></radialGradient>
    <linearGradient id="jkv_cPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2b0"/><stop offset=".45" stop-color="#ffb866"/><stop offset="1" stop-color="#e08a40"/></linearGradient>
    <linearGradient id="jkv_cJar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".3" stop-color="#fff" stop-opacity=".08"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient>
    <pattern id="jkv_cWoodC" width="72" height="18" patternUnits="userSpaceOnUse"><path d="M0,4q18,-3 36,0t36,0" stroke="#c9b48c" stroke-width="1.4" fill="none" opacity=".55"/><path d="M0,10q18,3 36,0t36,0" stroke="#fff" stroke-width="1.2" fill="none" opacity=".5"/><path d="M0,15q18,-2 36,0t36,0" stroke="#c9b48c" stroke-width="1" fill="none" opacity=".4"/><ellipse cx="54" cy="8" rx="5" ry="2.6" fill="#b89c70" opacity=".25"/></pattern>
    <pattern id="jkv_cWeave" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0,2.5H5M2.5,0V5" stroke="#000" stroke-width=".7" opacity=".09"/></pattern>
    <pattern id="jkv_cCloudTex" width="220" height="110" patternUnits="userSpaceOnUse"><path d="M10,40q30,-22 60,0t60,0t60,0" stroke="#fff" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/><path d="M-20,95q36,-24 72,0t72,0t72,0" stroke="#dde2f3" stroke-width="4" fill="none" opacity=".55" stroke-linecap="round"/><ellipse cx="150" cy="20" rx="26" ry="8" fill="#fff" opacity=".5"/><ellipse cx="60" cy="72" rx="20" ry="6" fill="#e4e8f6" opacity=".5"/></pattern>
    <pattern id="jkv_cVein" width="140" height="70" patternUnits="userSpaceOnUse"><path d="M-10,20q40,-18 70,6t70,-10" stroke="#9c948e" stroke-width="1.6" fill="none" opacity=".22"/><path d="M20,60q30,-12 60,2t50,-14" stroke="#b8b0a8" stroke-width="1.2" fill="none" opacity=".2"/></pattern>`;

  // ---------------- building blocks ----------------
  const star4 = (x, y, r, c = "#fff6d0", op = 0.8) => `<path d="M${f(x)},${f(y - r)}Q${f(x)},${f(y)} ${f(x + r)},${f(y)}Q${f(x)},${f(y)} ${f(x)},${f(y + r)}Q${f(x)},${f(y)} ${f(x - r)},${f(y)}Q${f(x)},${f(y)} ${f(x)},${f(y - r)}Z" fill="${c}" opacity="${op}"/>`;
  const bolt = (x, y, r = 6) => `<circle cx="${f(x)}" cy="${f(y)}" r="${r}" fill="url(#jkv_cChromeV)"/><circle cx="${f(x)}" cy="${f(y)}" r="${f(r * 0.55)}" fill="#6a7480"/><circle cx="${f(x - r * 0.25)}" cy="${f(y - r * 0.3)}" r="${f(r * 0.22)}" fill="#fff" opacity=".8"/>`;
  const feather = (x, y, s, rot, op = 0.9) => `<g transform="translate(${f(x)},${f(y)}) rotate(${rot}) scale(${s})" opacity="${op}"><path d="M0,0C-16,-28 -12,-72 0,-104C12,-72 16,-28 0,0Z" fill="#fff"/><path d="M0,0C-16,-28 -12,-72 0,-104" stroke="#d8def0" stroke-width="2" fill="none"/><path d="M0,-6V-98" stroke="#c4cbe4" stroke-width="1.6"/>${[-86, -70, -54, -38, -22].map((yy) => `<path d="M0,${yy}l-7,7M0,${yy}l7,7" stroke="#d8def0" stroke-width="1.1" fill="none"/>`).join("")}<path d="M-2,-30C-8,-48 -6,-70 0,-88" stroke="#fff" stroke-width="3" opacity=".8" fill="none"/></g>`;
  // a shaded cloud puff: a lavender belly, a soft shadow below, lit spheres, a rim of light along the top-left of the big lobes
  const PARTS = [[-0.32, 0.02, 0.3], [0, -0.22, 0.38], [0.3, -0.04, 0.3], [-0.14, -0.1, 0.3], [0.16, -0.18, 0.28]];
  const puffG = (x, y, w, h, g = "jkv_cPuff", op = 1) => `<g transform="translate(${f(x)},${f(y)})" opacity="${op}"><ellipse cx="0" cy="${f(h * 0.18)}" rx="${f(w * 0.56)}" ry="${f(h * 0.46)}" fill="#d8dcee"/><ellipse cx="${f(w * 0.04)}" cy="${f(h * 0.34)}" rx="${f(w * 0.5)}" ry="${f(h * 0.3)}" fill="url(#jkv_cShadow)" opacity=".45"/>
      ${PARTS.map(([dx, dy, rr]) => `<circle cx="${f(dx * w)}" cy="${f(dy * h)}" r="${f(rr * w * 0.6)}" fill="url(#${g})"/>`).join("")}
      ${PARTS.slice(0, 3).map(([dx, dy, rr]) => { const R = rr * w * 0.6, cx = dx * w, cy = dy * h; return `<path d="M${f(cx - R * 0.78)},${f(cy - R * 0.2)}A${f(R)},${f(R)} 0 0,1 ${f(cx + R * 0.1)},${f(cy - R * 0.96)}" stroke="#fff" stroke-width="${f(Math.max(2, R * 0.08))}" fill="none" opacity=".85" stroke-linecap="round"/>`; }).join("")}</g>`;
  // a paper lantern: brass caps, paper body with ribs and side shading, a red tassel; halo as a radial disc (no filter)
  const lanternBody = (s = 1, halo = true) => `<g transform="scale(${s})">${halo ? `<circle r="84" fill="url(#jkv_cLamp)" opacity=".55"/>` : ""}<path d="M0,-60V-94" stroke="#8a6414" stroke-width="2.5"/><rect x="-20" y="-62" width="40" height="14" rx="5" fill="url(#jkv_cGoldV)"/>
    <path d="M-34,-48Q-48,0 -34,48H34Q48,0 34,-48Z" fill="url(#jkv_cPaper)"/>${[-22, -9, 4, 17].map((x) => `<path d="M${x},-48Q${x - 7},0 ${x},48" stroke="#c87a30" stroke-width="1.6" fill="none" opacity=".4"/>`).join("")}
    <path d="M-34,-48Q-48,0 -34,48H34Q48,0 34,-48Z" fill="url(#jkv_cLitV)" opacity=".55"/><ellipse cx="-14" cy="-20" rx="9" ry="18" fill="#fff" opacity=".28"/>
    <rect x="-20" y="46" width="40" height="14" rx="5" fill="url(#jkv_cGoldV)"/><path d="M0,60v16" stroke="#a8243a" stroke-width="3"/><path d="M-7,76h14l-3,22h-8z" fill="#d8443a"/><path d="M-5,80v16M0,80v18M5,80v16" stroke="#f08070" stroke-width="1.2"/></g>`;
  const lantern = (x, y, s) => `<g transform="translate(${f(x)},${f(y)})">${lanternBody(s)}</g>`;
  // a gold harp lying on a cloud
  const harp = (x, y, s) => { const qp = (a, c, b, t) => [(1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]];
    const box0 = [0, 0], boxC = [-34, -84], box1 = [-16, -164], neckC = [44, -200], neck1 = [96, -150];
    let st = ""; for (let k = 1; k <= 9; k++) { const t = k / 10, a = qp(box1, neckC, neck1, t), b = qp(box0, boxC, box1, 1 - t * 0.92); st += `<path d="M${f(a[0])},${f(a[1])}L${f(b[0])},${f(b[1])}" stroke="#fff8e0" stroke-width="1.4" opacity=".9"/>`; }
    return `<g transform="translate(${f(x)},${f(y)}) scale(${s}) rotate(-6)"><ellipse cx="40" cy="6" rx="76" ry="12" fill="url(#jkv_cShadow)"/>${st}
      <path d="M0,0Q-34,-84 -16,-164" stroke="url(#jkv_cGoldH)" stroke-width="18" fill="none" stroke-linecap="round"/><path d="M-16,-164Q44,-200 96,-150" stroke="url(#jkv_cGoldV)" stroke-width="12" fill="none" stroke-linecap="round"/>
      <path d="M96,-150L72,0" stroke="url(#jkv_cGoldH)" stroke-width="9" stroke-linecap="round"/><path d="M-6,0H80" stroke="url(#jkv_cGoldV)" stroke-width="10" stroke-linecap="round"/>
      <path d="M-4,-10Q-30,-84 -14,-150" stroke="#fff6c8" stroke-width="3" fill="none" opacity=".7"/><circle cx="96" cy="-152" r="9" fill="url(#jkv_cGoldV)"/><circle cx="96" cy="-152" r="9" fill="url(#jkv_cBall)"/><circle cx="-16" cy="-166" r="8" fill="url(#jkv_cGoldV)"/><circle cx="-16" cy="-166" r="8" fill="url(#jkv_cBall)"/></g>`; };
  // the far gate of heaven, rebuilt bigger round the one jkset draws at (1600,820): pale gold, lit from above
  const gate = () => { const archY = (x) => { const t = (x + 110) / 220; return (1 - t) * (1 - t) * -330 + 2 * (1 - t) * t * -440 + t * t * -330; };
    return `<g transform="translate(1600,820)"><circle cy="-170" r="300" fill="url(#jkv_cGateGlow)" opacity=".85"/>
    ${puffG(-200, 30, 300, 130, "jkv_cPuffFar")}${puffG(210, 40, 320, 140, "jkv_cPuffFar")}
    <rect x="-200" y="-14" width="400" height="30" rx="8" fill="url(#jkv_cMarble)"/><rect x="-200" y="-14" width="400" height="30" rx="8" fill="url(#jkv_cVein)"/><rect x="-160" y="-40" width="320" height="30" rx="8" fill="url(#jkv_cMarble)"/><rect x="-160" y="-40" width="320" height="30" rx="8" fill="url(#jkv_cVein)"/>
    <path d="M-110,-330Q0,-440 110,-330V-40H-110Z" fill="#fff9ea" opacity=".92"/><path d="M-110,-330Q0,-440 110,-330V-40H-110Z" fill="url(#jkv_cLit)" opacity=".5"/>
    ${[-70, -35, 0, 35, 70].map((x) => `<path d="M${x},${f(archY(x) + 6)}V-40" stroke="#e6c874" stroke-width="5" opacity=".8"/>`).join("")}<path d="M-110,-200H110M-110,-120H110" stroke="#e6c874" stroke-width="6" opacity=".8"/>
    ${[-150, 104].map((x) => `<rect x="${x}" y="-320" width="46" height="280" fill="url(#jkv_cGateH)"/><rect x="${x - 10}" y="-336" width="66" height="18" rx="4" fill="url(#jkv_cGate)"/><rect x="${x - 10}" y="-54" width="66" height="16" rx="4" fill="url(#jkv_cGate)"/><rect x="${x + 8}" y="-300" width="7" height="240" fill="#fff" opacity=".35"/>`).join("")}
    <path d="M-160,-330Q0,-470 160,-330" stroke="url(#jkv_cGateH)" stroke-width="34" fill="none" stroke-linecap="round"/><path d="M-160,-330Q0,-470 160,-330" stroke="#fff8e0" stroke-width="6" fill="none" opacity=".6"/>
    ${[0.12, 0.26, 0.4, 0.5, 0.6, 0.74, 0.88].map((t) => { const x = -160 + 320 * t, y = (1 - t) * (1 - t) * -330 + 2 * (1 - t) * t * -470 + t * t * -330; return `<circle cx="${f(x)}" cy="${f(y - 30)}" r="9" fill="url(#jkv_cGoldV)"/><circle cx="${f(x)}" cy="${f(y - 30)}" r="4" fill="#fff8e0"/>`; }).join("")}
    ${star4(0, -452, 26, "#fff2b0", 0.95)}${star4(0, -452, 12, "#fff", 1)}
    ${[-127, 127].map((x) => `<path d="M${x},-336V-396" stroke="#a88438" stroke-width="3"/><path d="M${x},-396h36l-10,10l10,10h-36z" fill="#e8c86a"/>`).join("")}</g>`; };
  // the floating queue sign: a gold-framed cream arrow plate on a small cloud, with little wings
  const floatSign = (x, y) => `<g transform="translate(${x},${y})">${puffG(0, 72, 360, 110)}<ellipse cy="58" rx="190" ry="12" fill="url(#jkv_cShadow)"/>
    <path d="M-214,-10q-40,-30 -70,-6q30,8 40,30q10,-20 30,-24z" fill="#fff" opacity=".92"/><path d="M-214,-10q-40,-30 -70,-6" stroke="#dfe3f2" stroke-width="2" fill="none"/>
    <path d="M232,-10q40,-30 70,-6q-30,8 -40,30q-10,-20 -30,-24z" fill="#fff" opacity=".92"/><path d="M232,-10q40,-30 70,-6" stroke="#dfe3f2" stroke-width="2" fill="none"/>
    <path d="M-210,-40H190L232,0L190,40H-210Z" fill="url(#jkv_cGoldV)"/><path d="M-200,-32H184L220,0L184,32H-200Z" fill="url(#jkv_cCream)"/><path d="M-200,-32H184L220,0L184,32H-200Z" fill="url(#jkv_cWeave)"/>
    <path d="M-196,-27H180" stroke="#fff" stroke-width="3" opacity=".7"/>${[[-192, -22], [-192, 22], [176, -22], [176, 22]].map(([bx, by]) => bolt(bx, by, 5)).join("")}
    ${T(-8, 16, 44, "ต่อคิวสุ่มสกิล", { fill: "#5a3a24", w: 900 })}</g>`;

  JKV.cloud = (L, tl, sh, id, o) => {
    if (Q.get("nojkv")) return;
    const sid = o.id || "jkq", r = mk((o.seed || 9) + 23);
    const reps = (p) => Math.ceil(sh.dur / p) + 1;
    const world = L.set.querySelector(`#${sid}-world`);
    const hole = world && world.querySelector(`#${sid}-hole`);
    const machine = world && world.lastElementChild;   // the gacha group, translate(820,1400), as jkset builds it

    // ---- sky: cirrus streaks, a halo round the sun, faint stars ----
    L.sky.insertAdjacentHTML("beforeend", `<g>${[[-300, 120, 520, 16], [300, 60, 420, 12], [1000, 150, 620, 18], [1700, 90, 460, 14], [200, 420, 380, 10], [1300, 480, 520, 14]].map(([x, y, w, h]) => `<ellipse cx="${x}" cy="${y}" rx="${w}" ry="${h}" fill="#fff" opacity=".28"/><ellipse cx="${x + 40}" cy="${y - 4}" rx="${w * 0.6}" ry="${h * 0.5}" fill="#fff" opacity=".3"/>`).join("")}
      <circle cx="780" cy="200" r="300" fill="none" stroke="#fff" stroke-width="7" opacity=".16"/><circle cx="780" cy="200" r="360" fill="none" stroke="#fff" stroke-width="3" opacity=".1"/>
      ${[...Array(12)].map(() => star4(-400 + r() * 2200, -420 + r() * 820, 5 + r() * 7, "#fff", 0.3 + r() * 0.3)).join("")}</g>`);

    // ---- far: the gate, shaded cloud banks, haze strata, tiny lanterns, sparkle stars ----
    { let h = gate();
      for (let i = 0; i < 10; i++) h += puffG(-1700 + i * 520 + r() * 120, 1060 + r() * 70, 560 + r() * 200, 240 + r() * 60, "jkv_cPuffFar", 0.95);
      h += `<rect x="-2400" y="960" width="6200" height="360" fill="url(#jkv_cHaze)" opacity=".5"/><rect x="-2400" y="820" width="6200" height="60" fill="#fff6ea" opacity=".2"/>
        ${[[-250, 560, 0.42], [920, 400, 0.4], [1250, 640, 0.46], [2200, 520, 0.5]].map(([x, y, s]) => `<g opacity=".7">${lantern(x, y, s)}</g>`).join("")}
        ${[...Array(18)].map(() => star4(-300 + r() * 1800, 160 + r() * 640, 6 + r() * 8, "#fff2c0", 0.4 + r() * 0.4)).join("")}`;
      L.far.insertAdjacentHTML("beforeend", h); }

    // ---- mid: shaded puffs with rim light, the deco lanterns dressed, two more lanterns, a harp on a cloud, feathers ----
    { let h = "";
      for (let i = 0; i < 9; i++) h += puffG(-1400 + i * 470 + r() * 100, 1272 + r() * 46, 480 + r() * 140, 220 + r() * 40, "jkv_cPuff", 0.96);
      h += puffG(1000, 792, 230, 90, "jkv_cPuff", 0.98) + harp(978, 772, 0.8) + feather(520, 540, 0.5, 28, 0.8) + feather(1180, 760, 0.42, -40, 0.75) + feather(-160, 980, 0.55, 110, 0.7);
      L.mid.insertAdjacentHTML("beforeend", h);
      L.mid.querySelectorAll(".lan > g").forEach((inner) => inner.insertAdjacentHTML("beforeend", lanternBody(1.08, false)));
      const g = G(L.mid, `<g>${lantern(760, 300, 0.8)}</g><g>${lantern(1100, 520, 0.7)}</g>`);   // each in a wrapper: gsap's y tween must not touch the translate
      [...g.children].forEach((el, k) => { const p = 4.6 + k * 0.9; tl.fromTo(el, { y: 0 }, { y: -22, duration: p / 2, repeat: reps(p) * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, sh.start - k * 1.3)); }); }

    // ---- set: the cloud floor (under the hole), the plinth (under the machine), then everything on top ----
    if (world && hole) {
      let fl = `<rect x="-2400" y="1360" width="6200" height="1400" fill="url(#jkv_cFloor)"/><rect x="-2400" y="1360" width="6200" height="1400" fill="url(#jkv_cCloudTex)" opacity=".55"/>
        <path d="M-760,1396H602V1456H-760Z" fill="url(#jkv_cRunner)"/><path d="M-760,1396H602V1456H-760Z" fill="url(#jkv_cWeave)"/><path d="M-760,1400H602M-760,1452H602" stroke="#f2d270" stroke-width="3"/><path d="M-760,1407H602" stroke="#fff" stroke-width="2" opacity=".25"/>
        ${[...Array(12)].map((_, k) => `<path d="M${-740 + k * 112},1402v50" stroke="#fff" stroke-width="1.5" opacity=".12"/>`).join("")}
        <ellipse cx="440" cy="1434" rx="118" ry="28" fill="#fff8e0" opacity=".3"/><ellipse cx="440" cy="1434" rx="118" ry="28" fill="none" stroke="#f2d270" stroke-width="5" stroke-dasharray="18 10"/>${T(440, 1486, 22, "ยืนตรงนี้", { fill: "#86601a", w: 900 })}`;
      for (let i = 0; i < 12; i++) fl += puffG(-1000 + i * 290 + r() * 60, 1500 + r() * 30, 240 + r() * 90, 90 + r() * 24, "jkv_cPuff", 0.96);
      for (let i = 0; i < 8; i++) fl += puffG(-900 + i * 420 + r() * 120, 1640 + r() * 50, 360 + r() * 120, 120 + r() * 40, "jkv_cPuff", 0.97);
      for (let i = 0; i < 4; i++) fl += puffG(-600 + i * 640 + r() * 200, 1820 + r() * 60, 520 + r() * 160, 170 + r() * 50, "jkv_cPuff", 1);
      for (let i = 0; i < 12; i++) { const x = -900 + r() * 2600, y = 1480 + r() * 420, w = 80 + r() * 140; fl += `<path d="M${f(x)},${f(y)}q${f(w * 0.25)},${f(-10 - r() * 10)} ${f(w * 0.5)},0t${f(w * 0.5)},0" stroke="#fff" stroke-width="${f(3 + r() * 4)}" fill="none" opacity=".6" stroke-linecap="round"/>`; }
      for (let i = 0; i < 9; i++) { const x = -700 + r() * 2300, y = 1480 + r() * 360; if (Math.abs(x - 440) < 200 && y < 1500) continue; fl += star4(x, y, 5 + r() * 7, "#f2d270", 0.5 + r() * 0.3); }
      fl += feather(120, 1590, 0.55, 78, 0.85) + feather(1180, 1700, 0.6, -96, 0.85) + feather(760, 1760, 0.5, 100, 0.8);
      fl += [[-240, 1540], [300, 1620], [980, 1560], [1340, 1660], [640, 1700]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="9" ry="5" fill="#ffd2e4" opacity=".7" transform="rotate(${f(r() * 60 - 30)} ${x} ${y})"/>`).join("");
      hole.insertAdjacentHTML("beforebegin", fl);
    }
    if (machine) {
      // the marble plinth with a step, under the cabinet
      machine.insertAdjacentHTML("beforebegin", `<g transform="translate(820,1400)"><ellipse cy="50" rx="250" ry="22" fill="url(#jkv_cShadow)"/>
        <path d="M-210,30L-196,18H196L210,30Z" fill="#fbf8f4"/><rect x="-210" y="30" width="420" height="24" rx="6" fill="url(#jkv_cMarble)"/><rect x="-210" y="30" width="420" height="24" rx="6" fill="url(#jkv_cVein)"/><rect x="-210" y="30" width="420" height="24" rx="6" fill="url(#jkv_cLitV)" opacity=".35"/>
        <path d="M-186,-2L-176,-12H176L186,-2Z" fill="#fdfbf8"/><rect x="-186" y="-2" width="372" height="22" rx="5" fill="url(#jkv_cMarble)"/><rect x="-186" y="-2" width="372" height="22" rx="5" fill="url(#jkv_cVein)"/><rect x="-186" y="-2" width="372" height="22" rx="5" fill="url(#jkv_cLitV)" opacity=".4"/>
        <path d="M-150,0H150" stroke="#000" stroke-width="4" opacity=".18"/><path d="M-184,0H184" stroke="#fff" stroke-width="2" opacity=".5"/></g>`);
      // a chrome hub plate behind the crank (the crank itself is left alone)
      const crank = machine.querySelector(`#${sid}-crank`);
      if (crank) crank.insertAdjacentHTML("beforebegin", `<g transform="translate(-170,-230)"><circle r="42" fill="url(#jkv_cChromeV)"/><circle r="33" fill="#8a1e1a"/><circle r="33" fill="url(#jkv_cBall)"/>${[45, 135, 225, 315].map((a) => bolt(36 * Math.cos(a * Math.PI / 180), 36 * Math.sin(a * Math.PI / 180), 4)).join("")}</g>`);
      // capsules: shading and glints, slipped in under the glass
      const glass = machine.querySelector('circle[fill="url(#jkGlassD)"]');
      const caps = [...machine.children].filter((e) => e.tagName === "g" && !e.id && /^translate\(/.test(e.getAttribute("transform") || "") && e.querySelector('circle[r="22"]'));
      const capHtml = caps.map((e) => { const m = /translate\(([-\d.]+),([-\d.]+)\)/.exec(e.getAttribute("transform")); return `<g transform="translate(${m[1]},${m[2]})"><circle r="22" fill="url(#jkv_cBall)"/><path d="M-22,0A22,22 0 0,0 22,0Z" fill="#fff" opacity=".16"/><path d="M-21,0H21" stroke="#000" stroke-width="1.2" opacity=".22"/><ellipse cx="-8" cy="-11" rx="6" ry="3.4" fill="#fff" opacity=".9" transform="rotate(-35 -8 -11)"/><circle cx="9" cy="10" r="2.6" fill="#fff" opacity=".35"/></g>`; }).join("");
      if (glass) glass.insertAdjacentHTML("beforebegin", capHtml); else machine.insertAdjacentHTML("beforeend", capHtml);
    }
    // the machine's outer dressing (on top of the cabinet and the depth shading): materials, chrome, plates, the dome's glass
    const bulbs = [-150, -105, -55, 0, 55, 105, 150].map((x) => [x, -350 + 18 * Math.sqrt(1 - (x / 200) ** 2)]);
    L.set.insertAdjacentHTML("beforeend", `<g transform="translate(820,1400)">
      <rect x="-150" y="-330" width="300" height="330" rx="24" fill="url(#jkv_cRedV)" opacity=".5"/><rect x="-150" y="-330" width="300" height="330" rx="24" fill="url(#jkv_cRedH)" opacity=".85"/>
      <path d="M-124,-325H124" stroke="#ffb8a8" stroke-width="3" opacity=".7"/><rect x="-160" y="-326" width="12" height="326" rx="5" fill="url(#jkv_cChromeH)"/><rect x="148" y="-326" width="12" height="326" rx="5" fill="url(#jkv_cChromeH)"/>
      ${[[-134, -306], [134, -306], [-134, -14], [134, -14]].map(([x, y]) => bolt(x, y, 6)).join("")}
      ${[...Array(8)].map((_, k) => `<rect x="-138" y="${-302 + k * 11}" width="36" height="4" rx="2" fill="#000" opacity=".28"/>`).join("")}
      <rect x="-118" y="-292" width="236" height="74" rx="12" fill="url(#jkv_cGoldV)"/><rect x="-110" y="-284" width="220" height="58" rx="8" fill="url(#jkv_cCream)"/><rect x="-110" y="-284" width="220" height="58" rx="8" fill="url(#jkv_cLit)" opacity=".6"/>${T(0, -239, 42, "สุ่มสกิล", { fill: "#b82e2a", w: 900 })}
      <circle cx="-90" cy="-200" r="19" fill="url(#jkv_cGoldV)"/><circle cx="-90" cy="-200" r="13" fill="#f6d36a"/><circle cx="-90" cy="-200" r="13" fill="url(#jkv_cBall)"/>
      <rect x="58" y="-228" width="60" height="52" rx="7" fill="url(#jkv_cChromeV)"/><rect x="70" y="-215" width="36" height="26" rx="4" fill="#1a1010"/><rect x="76" y="-205" width="24" height="5" rx="2" fill="#f6d36a"/><path d="M88,-234l-7,-9h14z" fill="#fff" opacity=".85"/>
      
      <rect x="-66" y="-156" width="132" height="82" rx="16" fill="none" stroke="url(#jkv_cChromeV)" stroke-width="7"/><rect x="-44" y="-70" width="88" height="22" rx="5" fill="url(#jkv_cCream)"/>${T(0, -54, 13, "รับสกิลตรงนี้", { fill: "#5a3a24", w: 800 })}
      <rect x="-150" y="-20" width="300" height="20" rx="6" fill="url(#jkv_cChromeV)" opacity=".9"/>
      <ellipse cx="0" cy="-350" rx="202" ry="27" fill="url(#jkv_cChromeH)"/><ellipse cx="0" cy="-356" rx="196" ry="20" fill="url(#jkv_cChromeV)"/><ellipse cx="0" cy="-359" rx="150" ry="7" fill="#fff" opacity=".5"/>
      ${bulbs.map(([x, y]) => `<circle cx="${x}" cy="${f(y)}" r="7" fill="#fff4c0"/><circle cx="${x}" cy="${f(y)}" r="7" fill="url(#jkv_cBall)"/>`).join("")}
      <circle cx="0" cy="-540" r="190" fill="url(#jkv_cFresnel)"/><circle cx="0" cy="-540" r="190" fill="url(#jkv_cGlassHi)" opacity=".7"/>
      <path d="M-150,-600Q-120,-690 -20,-716" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" opacity=".55"/><path d="M-168,-540Q-160,-610 -120,-660" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".5"/>
      <path d="M120,-660Q160,-600 162,-520" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".35"/><path d="M-120,-410Q0,-372 120,-410" stroke="#cfe6fa" stroke-width="5" fill="none" opacity=".45"/>
      <ellipse cx="60" cy="-470" rx="50" ry="22" fill="#fff" opacity=".1" transform="rotate(-20 60 -470)"/><circle cx="0" cy="-540" r="190" fill="none" stroke="#fff" stroke-width="3" opacity=".55"/>
      <ellipse cx="0" cy="-728" rx="44" ry="13" fill="url(#jkv_cChromeH)"/><rect x="-30" y="-750" width="60" height="24" rx="8" fill="url(#jkv_cChromeV)"/><circle cx="0" cy="-762" r="14" fill="url(#jkv_cGoldV)"/><circle cx="0" cy="-762" r="14" fill="url(#jkv_cBall)"/></g>`);
    // brass stanchions and the velvet rope with tassels
    L.set.insertAdjacentHTML("beforeend", `${[100, 280, 460].map((x) => `<g transform="translate(${x},1400)"><ellipse cy="2" rx="34" ry="10" fill="url(#jkv_cShadow)"/><ellipse cy="-2" rx="28" ry="8" fill="url(#jkv_cGoldH)"/><ellipse cy="-6" rx="24" ry="6" fill="url(#jkv_cGoldV)"/>
        <rect x="-8" y="-150" width="16" height="146" rx="3" fill="url(#jkv_cGoldH)"/><path d="M-4,-146V-8" stroke="#fff8e0" stroke-width="2" opacity=".6"/><rect x="-13" y="-154" width="26" height="8" rx="3" fill="url(#jkv_cGoldV)"/><rect x="-11" y="-136" width="22" height="5" rx="2" fill="url(#jkv_cGoldV)"/>
        <circle cy="-161" r="13" fill="url(#jkv_cGoldV)"/><circle cy="-161" r="13" fill="url(#jkv_cBall)"/><circle cx="-5" cy="-166" r="3" fill="#fff" opacity=".85"/><circle cy="-140" r="6" fill="url(#jkv_cGoldV)"/><circle cy="-140" r="6" fill="url(#jkv_cBall)"/></g>`).join("")}
      <path d="M100,1260Q190,1300 280,1260Q370,1300 460,1260" stroke="#58101e" stroke-width="15" fill="none" stroke-linecap="round" opacity=".55" transform="translate(0,3)"/>
      <path d="M100,1260Q190,1300 280,1260Q370,1300 460,1260" stroke="#b82e44" stroke-width="14" fill="none" stroke-linecap="round"/>
      <path d="M100,1260Q190,1300 280,1260Q370,1300 460,1260" stroke="#e87088" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7" transform="translate(0,-4)"/>
      <path d="M100,1260Q190,1300 280,1260Q370,1300 460,1260" stroke="#f0a0b0" stroke-width="2" fill="none" stroke-dasharray="9 11" opacity=".5"/>
      ${[190, 370].map((x) => `<g transform="translate(${x},1280)"><circle r="7" fill="url(#jkv_cGoldV)"/><circle r="7" fill="url(#jkv_cBall)"/><path d="M0,6v10" stroke="#a8243a" stroke-width="3"/><path d="M-9,16h18l-4,26h-10z" fill="#b82e44"/><path d="M-6,20v18M0,20v20M6,20v18" stroke="#f0a0b0" stroke-width="1.2" opacity=".7"/></g>`).join("")}`);
    // the deco queue sign at x 330 gets a brass post, a finial and gold frames round its plates
    if (L.set.querySelector('g[transform="translate(330,1400)"]')) L.set.insertAdjacentHTML("beforeend", `<g transform="translate(330,1400)"><ellipse cy="2" rx="30" ry="9" fill="url(#jkv_cShadow)"/><ellipse cy="-2" rx="26" ry="7" fill="url(#jkv_cGoldH)"/><rect x="-9" y="-204" width="18" height="200" rx="3" fill="url(#jkv_cGoldH)"/><rect x="-9" y="-272" width="18" height="18" fill="url(#jkv_cGoldH)"/>
      <circle cy="-340" r="10" fill="url(#jkv_cGoldV)"/><circle cy="-340" r="10" fill="url(#jkv_cBall)"/><g transform="translate(0,-300)"><path d="M-110,-30H90L120,0L90,30H-110Z" fill="none" stroke="url(#jkv_cGoldV)" stroke-width="4"/></g><g transform="translate(0,-230)"><path d="M-100,-26H70L96,0L70,26H-100Z" fill="none" stroke="url(#jkv_cGoldV)" stroke-width="3"/></g></g>`);
    // the floating queue sign (bobs a little)
    if (false) { const g = G(L.set, floatSign(360, 700)); tl.fromTo(g, { y: 0 }, { y: -14, duration: 2.6, repeat: reps(5.2) * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, Math.max(0, sh.start - 0.7)); }
    // on the counter (an act-front group of its own, in front of whoever stands behind the counter): brass strip, grain, nameplate, ledger, stamp, inkpad, bell, jar of gum
    L.set.insertAdjacentHTML("beforeend", `<g class="act-front"><g transform="translate(1260,1400)">
      <rect x="-190" y="-222" width="20" height="222" fill="url(#jkv_cWoodC)" opacity=".8"/><rect x="170" y="-222" width="20" height="222" fill="url(#jkv_cWoodC)" opacity=".8"/><rect x="-190" y="-30" width="380" height="30" fill="url(#jkv_cWoodC)" opacity=".8"/><rect x="-190" y="-222" width="380" height="22" fill="url(#jkv_cWoodC)" opacity=".8"/>
      <rect x="-190" y="-230" width="380" height="230" rx="10" fill="url(#jkv_cLitV)" opacity=".3"/><rect x="-190" y="-30" width="380" height="30" fill="url(#jkv_cShadeUp)" opacity=".5"/>
      <rect x="-170" y="-200" width="340" height="170" rx="8" fill="none" stroke="#c9b48c" stroke-width="3" opacity=".7"/><rect x="-170" y="-200" width="340" height="8" fill="url(#jkv_cShadeDown)" opacity=".5"/>
      <rect x="-200" y="-244" width="400" height="22" rx="8" fill="url(#jkv_cGoldV)" opacity=".85"/><path d="M-196,-240H196" stroke="#fff8e0" stroke-width="2" opacity=".7"/><rect x="-190" y="-222" width="380" height="7" fill="url(#jkv_cShadeDown)" opacity=".7"/>
      
      <g transform="translate(-140,-246)"><ellipse cx="0" cy="4" rx="50" ry="5" fill="url(#jkv_cShadow)"/><path d="M-46,0L-42,-12H-2L0,0Z" fill="#e8dcc0"/><path d="M0,0L2,-12H42L46,0Z" fill="#f6efdc"/><path d="M-46,0H46V6H-46Z" fill="#8a6a44"/><path d="M-46,6H46" stroke="#5a3a24" stroke-width="1.5"/><path d="M-38,-9H-6M-36,-5H-8M8,-9H38M10,-5H36" stroke="#b8a888" stroke-width="1.2"/><path d="M0,-12V0" stroke="#c8b898" stroke-width="1.5"/>
        <path d="M8,-6l24,-18" stroke="#2a2440" stroke-width="3" stroke-linecap="round"/><path d="M30,-22l5,-4" stroke="#d8b84a" stroke-width="3" stroke-linecap="round"/>
        <rect x="10" y="-22" width="24" height="10" rx="2" fill="#2a2440"/><rect x="12" y="-20" width="20" height="4" rx="1" fill="#4a4470"/>
        <rect x="-36" y="-28" width="22" height="12" rx="2" fill="#d8443a"/><rect x="-38" y="-18" width="26" height="6" rx="1" fill="#3a2a20"/><rect x="-32" y="-52" width="14" height="26" rx="5" fill="#a86a3a"/><rect x="-32" y="-52" width="14" height="26" rx="5" fill="url(#jkv_cLitV)" opacity=".6"/><ellipse cx="-25" cy="-52" rx="7" ry="3" fill="#c8884a"/></g>
      <rect x="-126" y="-310" width="12" height="60" fill="url(#jkv_cGoldH)"/><circle cx="-120" cy="-316" r="16" fill="url(#jkv_cBall)"/><circle cx="-126" cy="-322" r="4" fill="#fff" opacity=".9"/><ellipse cx="-120" cy="-249" rx="14" ry="4" fill="url(#jkv_cShadow)"/>
      <rect x="96" y="-290" width="48" height="40" rx="5" fill="url(#jkv_cLit)" opacity=".7"/><path d="M98,-279H142" stroke="#fff" stroke-width="2" opacity=".55"/><ellipse cx="120" cy="-249" rx="26" ry="4" fill="url(#jkv_cShadow)"/>
      <g transform="translate(164,-246)"><ellipse cy="2" rx="24" ry="5" fill="url(#jkv_cShadow)"/><path d="M-20,-4V-46Q-20,-52 -14,-52H14Q20,-52 20,-46V-4Q20,0 14,0H-14Q-20,0 -20,-4Z" fill="#e6f2fa" opacity=".5"/>
        ${[[-10, -12, "#d8443a"], [2, -14, "#3a8ac8"], [11, -10, "#f6d36a"], [-6, -24, "#6ac87a"], [6, -26, "#c87ac8"], [-11, -36, "#f6d36a"], [4, -38, "#d8443a"], [12, -30, "#6ac87a"], [-3, -44, "#3a8ac8"]].map(([x, y, c]) => `<circle cx="${x}" cy="${y}" r="6" fill="${c}"/><circle cx="${x}" cy="${y}" r="6" fill="url(#jkv_cBall)"/>`).join("")}
        <path d="M-20,-4V-46Q-20,-52 -14,-52H14Q20,-52 20,-46V-4Q20,0 14,0H-14Q-20,0 -20,-4Z" fill="url(#jkv_cJar)"/><rect x="-16" y="-62" width="32" height="12" rx="4" fill="url(#jkv_cGoldV)"/><path d="M-14,-44V-10" stroke="#fff" stroke-width="3" opacity=".6"/></g></g></g>`);

    // ---- fg: the two near puffs shaded, pastel bokeh (few), two soft feathers ----
    L.fg.insertAdjacentHTML("beforeend", `${puffG(-260, 1880, 900, 360, "jkv_cPuff", 0.9)}${puffG(1500, 1900, 900, 380, "jkv_cPuff", 0.9)}
      ${[[120, 300, 56, "jkv_cBokP"], [1180, 250, 70, "jkv_cBokG"], [1350, 600, 48, "jkv_cBokB"], [900, 1750, 64, "jkv_cBokL"], [-20, 1500, 52, "jkv_cBokG"]].map(([x, y, rr, g]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="url(#${g})"/>`).join("")}
      ${feather(200, 1720, 0.8, 30, 0.75)}${feather(1340, 1600, 0.7, -50, 0.7)}`);

    // ---- glow: halos on the marquee bulbs, breathing ----
    { const g = G(L.glow, `<g style="mix-blend-mode:screen">${bulbs.map(([x, y]) => `<circle cx="${820 + x}" cy="${f(1400 + y)}" r="18" fill="url(#jkv_cGlow)" opacity=".6"/>`).join("")}</g>`);
      tl.fromTo(g.firstChild, { opacity: 1 }, { opacity: 0.45, duration: 0.9, repeat: reps(1.8) * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, sh.start); }
  };

  // ---- hook: run after the set and its depth dressing (before the cast) ----
  if (window.JKD && JKD.dress && JKD.dress.jkCloud && !JKD.dress.jkCloud.__jkv) {
    const prev = JKD.dress.jkCloud;
    JKD.dress.jkCloud = (L, tl, sh, id, o) => { prev(L, tl, sh, id, o); window.JKV = window.JKV || {}; JKV.cloud(L, tl, sh, id, o); };
    JKD.dress.jkCloud.__jkv = true;
  }
})();
