// "เห็ดปอบ" v2 — ป่าโคก (dry dipterocarp forest) after the first rain, and the white mushrooms.
//   Sets.kok2(L, o)   o.time day | dusk | night · o.mound [x, s] (false = none) · o.mush n (0..5 by the mound) · o.trunks [[x, w], …] near trunks
//                     o.fgTrunk "left" | "right" | false · o.rays · o.seed · o.ground G
//                     ids: #id-mound, #id-m0.. (mushrooms), #id-rays
//   Pop2.mush2(x, y, s, o)  a white amanita: o.v "open" | "button" | "egg", o.tilt, o.id, o.dirt; origin at its foot
//   Pop2.mound2(x, G, s, o) the termite mound; Pop2.trunk2(x, base, h, w, pal, r, o)
(function () {
  const { mk, f1, put, blob, tuft } = Pop2;
  const LN = "#3a2a22";

  Sets.DEFS += `
    <linearGradient id="kSkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9cbcc0"/><stop offset=".5" stop-color="#d6dcc4"/><stop offset="1" stop-color="#f0e2b8"/></linearGradient>
    <linearGradient id="kSkyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3456"/><stop offset=".5" stop-color="#a0607a"/><stop offset="1" stop-color="#f4a668"/></linearGradient>
    <linearGradient id="kSkyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04060c"/><stop offset="1" stop-color="#121c2a"/></linearGradient>
    <linearGradient id="kGroundDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4a67a"/><stop offset=".25" stop-color="#b8784a"/><stop offset="1" stop-color="#8a4c2c"/></linearGradient>
    <linearGradient id="kGroundDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4806a"/><stop offset=".25" stop-color="#8a4a3a"/><stop offset="1" stop-color="#4a2822"/></linearGradient>
    <linearGradient id="kGroundNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2230"/><stop offset="1" stop-color="#0c0c10"/></linearGradient>
    <linearGradient id="kBarkDay" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a69684"/><stop offset=".18" stop-color="#7a6a5a"/><stop offset=".7" stop-color="#4e4036"/><stop offset="1" stop-color="#2e241e"/></linearGradient>
    <linearGradient id="kBarkDusk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d08a6a"/><stop offset=".18" stop-color="#6a4a46"/><stop offset=".7" stop-color="#3a2a30"/><stop offset="1" stop-color="#1e161c"/></linearGradient>
    <linearGradient id="kBarkNight" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a3446"/><stop offset=".3" stop-color="#141a24"/><stop offset="1" stop-color="#06080c"/></linearGradient>
    <linearGradient id="kMoundDay" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e09a62"/><stop offset=".45" stop-color="#b86a3c"/><stop offset="1" stop-color="#6e3a20"/></linearGradient>
    <linearGradient id="kMoundDusk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f0a070"/><stop offset=".45" stop-color="#8a4a36"/><stop offset="1" stop-color="#3a1e1a"/></linearGradient>
    <linearGradient id="kMoundNight" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a3a48"/><stop offset=".5" stop-color="#1c1a20"/><stop offset="1" stop-color="#0a0a0c"/></linearGradient>
    <linearGradient id="kRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4d2" stop-opacity=".6"/><stop offset=".7" stop-color="#fff4d2" stop-opacity=".18"/><stop offset="1" stop-color="#fff4d2" stop-opacity="0"/></linearGradient>
    <linearGradient id="kRayDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc890" stop-opacity=".6"/><stop offset="1" stop-color="#ffc890" stop-opacity="0"/></linearGradient>
    <linearGradient id="kHazeDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eee6c8" stop-opacity="0"/><stop offset=".55" stop-color="#eee6c8" stop-opacity=".7"/><stop offset="1" stop-color="#eee6c8" stop-opacity=".1"/></linearGradient>
    <linearGradient id="kHazeDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0a878" stop-opacity="0"/><stop offset=".55" stop-color="#f0a878" stop-opacity=".55"/><stop offset="1" stop-color="#f0a878" stop-opacity=".05"/></linearGradient>
    <linearGradient id="kHazeNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2a3e" stop-opacity="0"/><stop offset=".55" stop-color="#1e2a3e" stop-opacity=".6"/><stop offset="1" stop-color="#1e2a3e" stop-opacity="0"/></linearGradient>
    <linearGradient id="mCap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset=".55" stop-color="#fbf4e6"/><stop offset=".85" stop-color="#ecdfc8"/><stop offset="1" stop-color="#d8c8ac"/></linearGradient>
    <linearGradient id="mSide" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset=".7" stop-color="#6a5a4a" stop-opacity="0"/><stop offset="1" stop-color="#4a3a5a" stop-opacity=".38"/></linearGradient>
    <linearGradient id="mStem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fffef8"/><stop offset=".45" stop-color="#f6efe0"/><stop offset="1" stop-color="#c4b6a0"/></linearGradient>
    <linearGradient id="mVolva" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6f0e4"/><stop offset=".6" stop-color="#e2d6c2"/><stop offset="1" stop-color="#a88c6c"/></linearGradient>
    <radialGradient id="mGlow"><stop offset="0" stop-color="#fffbe8" stop-opacity=".55"/><stop offset="1" stop-color="#fffbe8" stop-opacity="0"/></radialGradient>`;

  const PAL = {
    day: { groundTop: "#d4a67a", sky: "kSkyDay", ground: "kGroundDay", bark: "kBarkDay", mound: "kMoundDay", ray: "kRay", haze: "kHazeDay", far: "#b4b2a0", mid: "#8a8274", leaf: ["p2LeafD", "p2LeafM", "p2LeafL"], litter: ["#c8925a", "#a8703e", "#e0b47a", "#8a5a34", "#b8a06a"], grass: ["#5e8a34", "#9ac05a"], shadow: "#3a1c0c", fissure: "#2a1e18" },
    dusk: { groundTop: "#c4806a", sky: "kSkyDusk", ground: "kGroundDusk", bark: "kBarkDusk", mound: "kMoundDusk", ray: "kRayDusk", haze: "kHazeDusk", far: "#a07888", mid: "#5a4250", leaf: ["p2LeafDd", "p2LeafMd", "p2LeafLd"], litter: ["#a8604a", "#7a4232", "#d08a5a", "#5a3028", "#9a6a4a"], grass: ["#4a5a2a", "#8a8a46"], shadow: "#1a0a10", fissure: "#120a0c" },
    night: { groundTop: "#1c2230", sky: "kSkyNight", ground: "kGroundNight", bark: "kBarkNight", mound: "kMoundNight", ray: null, haze: "kHazeNight", far: "#1e2838", mid: "#121822", leaf: ["p2LeafDn", "p2LeafMn", "p2LeafLn"], litter: ["#2a2620", "#1e1a16", "#36302a", "#16120e", "#2e2a22"], grass: ["#101a10", "#1c2a18"], shadow: "#000000", fissure: "#000000" },
  };

  // a dipterocarp trunk: near-straight with a slight lean, a flared base with roots, deep vertical fissures, lit on the left
  function trunk2(x, base, h, w, P, r, o = {}) {
    const lean = (r() - 0.5) * 0.05 * h, top = base - h, wb = w * 1.5, wt = w * 0.66;
    let g = "";
    if (o.cast !== false && P.shadow) g += `<path d="M${f1(x - w * 0.4)},${f1(base)}L${f1(x + w * 0.5)},${f1(base)}L${f1(x + w * 0.5 + w * 6)},${f1(base + w * 1.4)}L${f1(x - w * 0.1 + w * 5.6)},${f1(base + w * 1.5)}Z" fill="${P.shadow}" opacity="${o.castOp ?? 0.16}"/>`;
    g += `<ellipse cx="${f1(x + w * 0.2)}" cy="${f1(base + 2)}" rx="${f1(w * 1.4)}" ry="${f1(w * 0.22)}" fill="url(#p2AO)" opacity=".8"/>`;
    // roots
    g += `<path d="M${f1(x - wb / 2)},${f1(base)}Q${f1(x - wb)},${f1(base + 6)} ${f1(x - wb * 1.25)},${f1(base + 10)}Q${f1(x - wb * 0.7)},${f1(base - 4)} ${f1(x - w * 0.4)},${f1(base - w * 0.3)}Z
      M${f1(x + wb / 2)},${f1(base)}Q${f1(x + wb * 0.95)},${f1(base + 8)} ${f1(x + wb * 1.15)},${f1(base + 14)}Q${f1(x + wb * 0.6)},${f1(base - 4)} ${f1(x + w * 0.4)},${f1(base - w * 0.3)}Z" fill="url(#${P.bark})"/>`;
    const d = `M${f1(x - wb / 2)},${f1(base)}Q${f1(x - w / 2)},${f1(base - w * 0.3)} ${f1(x - w / 2)},${f1(base - w * 0.9)}L${f1(x - wt / 2 + lean)},${f1(top)}L${f1(x + wt / 2 + lean)},${f1(top)}L${f1(x + w / 2)},${f1(base - w * 0.9)}Q${f1(x + w / 2)},${f1(base - w * 0.3)} ${f1(x + wb / 2)},${f1(base)}Z`;
    g += `<path d="${d}" fill="url(#${P.bark})"/>`;
    // fissures: wavy vertical cracks, denser on the shadow side
    const n = Math.max(3, Math.round(w / 12));
    for (let k = 0; k < n; k++) {
      const u = (k + 0.5) / n, x0 = x - w / 2 + u * w;
      let p = `M${f1(x0 + (r() - 0.5) * 4)},${f1(base - 6)}`;
      for (let y = base - 46; y > top; y -= 34 + r() * 30) { const ku = (base - y) / h; p += `L${f1(x0 + lean * ku + (r() - 0.5) * w * 0.12)},${f1(y)}`; }
      g += `<path d="${p}" stroke="${P.fissure}" stroke-width="${f1(1.5 + w * 0.035)}" fill="none" opacity="${f1(0.25 + u * 0.45)}" stroke-linejoin="round"/>`;
    }
    // bark plates catching the light on the lit edge
    for (let k = 0; k < h / 60; k++) { const y = base - 40 - r() * (h - 60), ku = (base - y) / h; g += `<path d="M${f1(x - w * 0.42 + lean * ku)},${f1(y)}q${f1(w * 0.12)},-${f1(6 + r() * 10)} ${f1(w * 0.22)},-${f1(2 + r() * 6)}" stroke="#fff4dc" stroke-width="${f1(1 + w * 0.02)}" fill="none" opacity=".22"/>`; }
    return g;
  }
  function crownK(cx, cy, R, P, r) {
    let g = "";
    [[-0.6, 0.1, 0.55], [0.55, 0.05, 0.6], [0, -0.35, 0.65], [-0.25, 0.2, 0.5], [0.3, -0.1, 0.5]].forEach(([dx, dy, k]) => {
      g += `<path d="${blob(cx + dx * R + 10, cy + dy * R + 14, R * k * 1.05, r, 10)}" fill="url(#${P.leaf[0]})"/>`; });
    [[-0.55, 0.0, 0.42], [0.5, -0.05, 0.45], [0, -0.42, 0.5]].forEach(([dx, dy, k]) => {
      g += `<path d="${blob(cx + dx * R - 6, cy + dy * R - 6, R * k, r, 9)}" fill="url(#${P.leaf[1]})"/><path d="${blob(cx + dx * R - R * 0.18, cy + dy * R - R * 0.16, R * k * 0.5, r, 8)}" fill="url(#${P.leaf[2]})"/>`; });
    return g;
  }

  // the termite mound: a lumpy cone of red earth with three chimneys, rain-cut grooves, holes, a lit side, grass at the foot
  function mound2(x, G, s, P, r, o = {}) {
    const rr = mk(o.seed || 31), peaks = [[-40, 330, 70], [64, 262, 52], [-140, 176, 60], [150, 120, 70]];
    const prof = (px) => { let h = 0; peaks.forEach(([cx, ph, w]) => { const u = (px - cx) / (w * 2.3); h = Math.max(h, ph * Math.exp(-u * u * 1.6)); }); return Math.max(h, 110 * Math.max(0, 1 - Math.abs(px) / 230)); };
    const pts = [];
    for (let px = -230; px <= 230; px += 14) pts.push([px + (rr() - 0.5) * 6, -prof(px) * (0.96 + rr() * 0.08) + (Math.abs(px) > 220 ? 0 : 0)]);
    let d = `M-236,4L${pts.map(([a, b]) => `${f1(a)},${f1(Math.min(0, b))}`).join("L")}L236,4Z`;
    d = Pop2.smoothClosed([[-236, 4], ...pts.map(([a, b]) => [a, Math.min(0, b)]), [236, 4]]);
    let g = `<path d="M-140,0L240,0L560,74L60,90Z" fill="${P.shadow}" opacity=".16"/><ellipse cx="10" cy="4" rx="280" ry="32" fill="url(#p2AO)"/>`;
    g += `<path d="${d}" fill="url(#${P.mound})"/>`;
    // rain grooves follow the slope down from each chimney; crusty lumps catch the light
    peaks.forEach(([cx, ph]) => { for (let k = 0; k < 4; k++) { const x0 = cx + (rr() - 0.5) * 30, y0 = -ph * (0.75 + rr() * 0.2), x1 = x0 + (x0 - cx * 0.3) * (0.4 + rr() * 0.5) + (rr() - 0.5) * 40;
      g += `<path d="M${f1(x0)},${f1(y0)}Q${f1((x0 + x1) / 2 + (rr() - 0.5) * 30)},${f1(y0 * 0.5)} ${f1(x1)},${f1(-4 - rr() * 20)}" stroke="#4a2412" stroke-width="${f1(2 + rr() * 3)}" fill="none" opacity=".3" stroke-linecap="round"/>`; } });
    for (let k = 0; k < 26; k++) { const px = -200 + rr() * 400, py = -prof(px) * (0.1 + rr() * 0.75), R = 6 + rr() * 12;
      g += `<path d="${blob(px, py, R, rr, 6)}" fill="#e8a46a" opacity="${f1(0.18 + (px < 0 ? 0.2 : 0))}"/><path d="M${f1(px - R)},${f1(py + R * 0.5)}q${f1(R)},${f1(R * 0.5)} ${f1(R * 2)},0" stroke="#4a2412" stroke-width="2" fill="none" opacity=".25"/>`; }
    [[-60, -70, 13, 8], [40, -150, 9, 6], [-40, -250, 8, 6], [100, -60, 12, 8], [-130, -100, 9, 6], [70, -230, 6, 5]].forEach(([hx, hy, rx, ry]) => { g += `<ellipse cx="${hx}" cy="${hy}" rx="${rx}" ry="${ry}" fill="#2a1408"/><path d="M${hx - rx},${hy}q${rx},${-ry * 1.4} ${rx * 2},0" stroke="#f0b47a" stroke-width="2" fill="none" opacity=".5"/>`; });
    g += `<path d="M-170,-40Q-120,-140 -70,-260M-120,-24Q-90,-150 -54,-300" stroke="#fff0d0" stroke-width="6" fill="none" opacity=".16" stroke-linecap="round"/>`;
    for (let k = 0; k < 10; k++) g += tuft(-230 + k * 50 + rr() * 20, 6 + rr() * 10, 0.7 + rr() * 0.5, P.grass[0], P.grass[1], rr);
    return `<g ${o.id ? `id="${o.id}"` : ""}><g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g></g>`;
  }

  // a white amanita. Open: a warm-white dome with the gills seen from below, a drooping skirt ring, a tapered stem with
  // fibrils and the cap's shadow at its top, the torn membranous cup half buried in soil crumbs. Origin at its foot.
  function mush2(x, y, s, o = {}) {
    const v = o.v || "open", rr = mk(o.seed || Math.round(x * 7 + y * 3));
    const soil = (w) => { let g = `<ellipse cx="4" cy="2" rx="${w * 1.5}" ry="${w * 0.32}" fill="#5a2c14" opacity=".55"/>`;
      for (let k = 0; k < 14; k++) { const a = rr() * Math.PI, d = w * (0.7 + rr() * 0.9), cx = Math.cos(a) * d * (rr() < 0.5 ? -1 : 1), cy = -2 + rr() * 10, R = 3 + rr() * 7;
        g += `<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(R)}" ry="${f1(R * 0.7)}" fill="${rr() < 0.5 ? "#8a4a26" : "#6a3418"}"/><ellipse cx="${f1(cx - R * 0.2)}" cy="${f1(cy - R * 0.3)}" rx="${f1(R * 0.5)}" ry="${f1(R * 0.3)}" fill="#c48a5a" opacity=".6"/>`; }
      return g; };
    let g = `<ellipse cx="10" cy="6" rx="${v === "egg" ? 80 : 140}" ry="18" fill="url(#p2AO)"/>`;
    if (v === "egg") {
      const d = "M-50,0C-64,-44 -54,-118 0,-126C54,-118 64,-44 50,0Q0,10 -50,0Z";
      g += `<path d="${d}" fill="url(#mCap)" stroke="${LN}" stroke-width="2.4"/><path d="${d}" fill="url(#mSide)"/>
        <path d="M-44,-40Q-20,-30 6,-46Q24,-38 46,-50M-36,-84Q0,-74 36,-90" stroke="#cdbfa8" stroke-width="2" fill="none"/><path d="M-30,-104q16,-12 34,-10" stroke="#fff" stroke-width="6" fill="none" opacity=".8" stroke-linecap="round"/>
        <path d="M-52,0Q-34,-26 0,-18Q34,-28 52,0Z" fill="#9a6a44" opacity=".55"/>` + soil(44);
      return `<g ${o.id ? `id="${o.id}"` : ""}><g transform="translate(${f1(x)},${f1(y)}) scale(${s}) rotate(${o.tilt || 0})">${g}</g></g>`;
    }
    const H = v === "button" ? 190 : 250, cw = v === "button" ? 78 : 126, ch = v === "button" ? 124 : 96;
    // stem
    const stem = `M-21,-48C-25,-120 -17,-${H - 40} -12,-${H}L12,-${H}C17,-${H - 40} 25,-120 21,-48Z`;
    g += `<path d="${stem}" fill="url(#mStem)" stroke="${LN}" stroke-width="2.4"/>`;
    g += `<path d="M-13,-${H}L13,-${H}L17,-${H - 70}L-17,-${H - 70}Z" fill="#6a5440" opacity=".22"/>`;
    g += `<path d="M-10,-70q-4,-30 0,-60q3,-30 -1,-${H - 160}M7,-80q4,-30 0,-60q-3,-30 1,-${H - 170}M-2,-60q-2,-40 2,-${H - 120}" stroke="#d6ccb8" stroke-width="1.6" fill="none"/>`;
    // the skirt ring hanging under the cap
    const top = H - 26;
    g += `<path d="M-13,-${top}C-26,-${top - 6} -36,-${top - 22} -34,-${top - 34}Q-26,-${top - 28} -20,-${top - 34}Q-12,-${top - 26} -4,-${top - 32}Q4,-${top - 26} 12,-${top - 33}Q20,-${top - 27} 26,-${top - 34}Q32,-${top - 28} 35,-${top - 33}C36,-${top - 20} 26,-${top - 6} 13,-${top}Z" fill="#fbf8f0" stroke="${LN}" stroke-width="2" opacity=".97"/>
      <path d="M-24,-${top - 12}l-4,-14M-8,-${top - 8}l-2,-18M8,-${top - 8}l2,-18M24,-${top - 12}l4,-14" stroke="#d2c6b0" stroke-width="1.6"/>
      <path d="M-34,-${top - 34}Q0,-${top - 22} 35,-${top - 33}" stroke="#bfb29a" stroke-width="2" fill="none" opacity=".7"/>`;
    // the torn cup
    g += `<path d="M-44,0C-56,-24 -50,-56 -38,-66L-30,-54L-24,-70L-14,-58Q0,-62 14,-58L22,-70L30,-56L40,-66C52,-56 56,-24 44,0Q0,8 -44,0Z" fill="url(#mVolva)" stroke="${LN}" stroke-width="2.4" stroke-linejoin="round"/>
      <path d="M-30,-54Q0,-46 30,-56" stroke="#a8916e" stroke-width="2" fill="none" opacity=".6"/><path d="M-36,-30q-4,14 0,26M32,-36q6,14 2,30" stroke="#cdbea4" stroke-width="2" fill="none"/>`;
    g += soil(46);
    // gills seen from below, then the cap
    if (v === "open") {
      g += `<path d="M-${cw - 2},-${H}C-${cw * 0.62},-${H - 26} ${cw * 0.62},-${H - 26} ${cw - 2},-${H}C${cw * 0.6},-${H - 4} -${cw * 0.6},-${H - 4} -${cw - 2},-${H}Z" fill="#e6dccb" stroke="${LN}" stroke-width="2"/>`;
      for (let k = 0; k <= 16; k++) { const u = -1 + k / 8; g += `<path d="M${f1(u * (cw - 8))},-${f1(H + 1 - Math.abs(u) * 2)}Q${f1(u * cw * 0.4)},-${f1(H - 14)} ${f1(u * 11)},-${H - 18}" stroke="#bcae96" stroke-width="1.3" fill="none"/>`; }
      g += `<ellipse cx="0" cy="-${H - 16}" rx="16" ry="5" fill="#8a7458" opacity=".5"/>`;
    }
    const cap = v === "open" ? `M-${cw},-${H}C-${cw - 2},-${H + ch * 0.6} -${cw * 0.52},-${H + ch} 0,-${H + ch}C${cw * 0.52},-${H + ch} ${cw - 2},-${H + ch * 0.6} ${cw},-${H}C${cw * 0.62},-${H + 7} -${cw * 0.62},-${H + 7} -${cw},-${H}Z`
      : `M-${cw},-${H - 6}C-${cw + 4},-${H + ch * 0.7} -${cw * 0.52},-${H + ch} 0,-${H + ch}C${cw * 0.52},-${H + ch} ${cw + 4},-${H + ch * 0.7} ${cw},-${H - 6}Q0,-${H - 16} -${cw},-${H - 6}Z`;
    g += `<path d="${cap}" fill="url(#mCap)" stroke="${LN}" stroke-width="2.6"/><path d="${cap}" fill="url(#mSide)"/>`;
    g += `<path d="M-${cw - 6},-${H + 4}C-${cw * 0.6},-${H + 12} ${cw * 0.6},-${H + 12} ${cw - 6},-${H + 4}" stroke="#d4c8b2" stroke-width="3" fill="none" opacity=".8"/>`;
    g += `<path d="M-${f1(cw * 0.7)},-${f1(H + ch * 0.5)}Q-${f1(cw * 0.42)},-${f1(H + ch * 0.95)} ${f1(cw * 0.12)},-${f1(H + ch * 0.96)}" stroke="#fff" stroke-width="9" fill="none" opacity=".85" stroke-linecap="round"/>
      <path d="M-${f1(cw * 0.96)},-${f1(H + 6)}Q-${f1(cw * 0.94)},-${f1(H + ch * 0.55)} -${f1(cw * 0.6)},-${f1(H + ch * 0.85)}" stroke="#fffbe8" stroke-width="3" fill="none" opacity=".9"/>`;
    if (o.dirt !== false) g += `<path d="M-${f1(cw * 0.2)},-${f1(H + ch * 0.72)}l3,2M${f1(cw * 0.36)},-${f1(H + ch * 0.52)}l3,1M${f1(cw * 0.1)},-${f1(H + ch * 0.84)}l2,2" stroke="#a88c6c" stroke-width="3" stroke-linecap="round" opacity=".7"/>`;
    return `<g ${o.id ? `id="${o.id}"` : ""}><g transform="translate(${f1(x)},${f1(y)}) scale(${s}) rotate(${o.tilt || 0})">${g}</g></g>`;
  }

  function litter(x, y, s, c, r) {
    const a = r() * 180, L = (12 + r() * 10) * s, W = L * (0.38 + r() * 0.12);
    return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(a)}) scale(1,${f1(0.45 + r() * 0.3)})"><ellipse rx="${f1(L)}" ry="${f1(W)}" fill="${c}"/><path d="M${f1(-L)},0H${f1(L)}" stroke="#000" stroke-width="${f1(1 + s * 0.5)}" opacity=".18"/></g>`;
  }

  function kok2(L, o = {}) {
    const id = o.id || "k2", r = mk(o.seed || 77), G = o.ground ?? 1320, t = o.time || "day", P = PAL[t];
    // sky: a bright hazy afternoon behind a thin canopy
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${P.sky})"/>`;
    if (t !== "night") sky += `<circle cx="${o.sunX ?? 260}" cy="${o.sunY ?? 420}" r="560" fill="url(#p2Sun)"/>`;
    else for (let k = 0; k < 60; k++) sky += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-700 + r() * 1300)}" r="${f1(1 + r() * 1.8)}" fill="#e8ecff" opacity="${f1(0.2 + r() * 0.5)}"/>`;
    put(L.sky, sky);
    // far: rows of pale trunks fading into haze, crowns high up
    let far = "";
    for (let k = 0; k < 46; k++) { const x = -1100 + k * 74 + r() * 50, base = G - 150 + r() * 40, w = 8 + r() * 12; far += `<path d="M${f1(x - w / 2)},${f1(base)}L${f1(x - w * 0.35 + (r() - 0.5) * 20)},-600L${f1(x + w * 0.35)},-600L${f1(x + w / 2)},${f1(base)}Z" fill="${P.far}" opacity="${f1(0.45 + r() * 0.3)}"/>`; }
    for (let k = 0; k < 18; k++) far += `<path d="${blob(-1100 + k * 200 + r() * 80, -80 + r() * 220, 120 + r() * 90, r, 10)}" fill="${P.far}" opacity=".55"/>`;
    far += `<rect x="-1300" y="${G - 420}" width="3700" height="520" fill="url(#${P.haze})"/>`;
    put(L.far, far);
    // mid: trunks with some bark, saplings and shrubs, a canopy band
    let mid = "";
    for (let k = 0; k < 16; k++) { const x = -1000 + k * 210 + r() * 120, base = G - 80 + r() * 40, w = 22 + r() * 18; mid += trunk2(x, base, base + 700, w, { ...P, bark: P.bark }, r, { castOp: 0.08 }); }
    for (let k = 0; k < 12; k++) { const cx = -1100 + k * 300 + r() * 120, cy = -160 + r() * 200; mid += crownK(cx, cy, 170 + r() * 80, P, r); }
    for (let k = 0; k < 14; k++) { const x = -1000 + k * 240 + r() * 120, y = G - 60 + r() * 40; mid += `<path d="${blob(x, y - 40, 50 + r() * 40, r, 8)}" fill="url(#${P.leaf[0]})"/><path d="${blob(x - 14, y - 52, 30 + r() * 24, r, 7)}" fill="url(#${P.leaf[1]})"/>`; }
    mid += `<rect x="-1300" y="${G - 260}" width="3700" height="320" fill="url(#${P.haze})" opacity=".7"/>`;
    put(L.mid, mid);
    // set: the ground, litter, grass, near trunks, the mound and the mushrooms
    // the ground fades in under the haze instead of starting on a hard line
    let s = `<rect x="-1300" y="${G - 70}" width="3700" height="1700" fill="url(#${P.ground})"/><rect x="-1300" y="${G - 190}" width="3700" height="122" fill="url(#${id}-gfade)"/>`;
    s = `<defs><linearGradient id="${id}-gfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.groundTop}" stop-opacity="0"/><stop offset="1" stop-color="${P.groundTop}"/></linearGradient></defs>` + s;
    for (let k = 0; k < 22; k++) s += `<ellipse cx="${f1(-1100 + r() * 3300)}" cy="${f1(G - 60 + r() * 900)}" rx="${f1(120 + r() * 260)}" ry="${f1(14 + r() * 40)}" fill="${k % 3 ? P.grass[0] : "#000"}" opacity="${t === "night" ? 0.1 : k % 3 ? 0.22 : 0.08}"/>`;
    for (let k = 0; k < 520; k++) { const y = G - 90 + Math.pow(r(), 0.8) * 1200, x = -1200 + r() * 3500, sc = 0.5 + (y - G + 100) / 500; s += litter(x, y, sc, P.litter[Math.floor(r() * P.litter.length)], r); }
    for (let k = 0; k < 70; k++) { const y = G - 60 + r() * 1000; s += tuft(-1100 + r() * 3300, y, 0.4 + (y - G + 60) / 800, P.grass[0], P.grass[1], r); }
    const near = o.trunks || [[-140, 120], [1180, 100], [330, 46], [760, 60]];
    near.forEach(([x, w]) => { s += trunk2(x, G + w * 0.6, G + w * 0.6 + 900, w, P, r); });
    if (o.mound !== false) {
      const [mx, ms] = o.mound || [560, 1];
      s += mound2(mx, G + 40, ms, P, r, { id: `${id}-mound` });
      // real size: a 1.5 m mound, mushrooms a hand high (slightly generous so they read as white points)
      const M = [[-170, 18, 0.62, "open", -6], [-120, 30, 0.78, "open", 4], [-70, 24, 0.5, "button", -3], [120, 20, 0.36, "egg", 0], [-215, 14, 0.34, "egg", 0]], mk2 = o.mushK ?? 0.2;
      M.slice(0, o.mush ?? 4).forEach(([dx, dy, k, v, tilt], i) => { s += mush2(mx + dx * ms, G + 40 + dy * ms, k * ms * mk2, { v, tilt, id: `${id}-m${i}` }); });
    }
    put(L.set, s);
    // light: shafts through the canopy (in the world, above the darkness)
    if (P.ray && o.rays !== false) {
      let g = `<g id="${id}-rays" style="mix-blend-mode:screen">`;
      [[-200, 160, 0.5], [60, 110, 0.38], [380, 220, 0.45], [760, 120, 0.3]].forEach(([x0, w, op]) => { g += `<path d="M${x0},-600L${x0 + w},-600L${x0 + w + 900},${G + 600}L${x0 + 700},${G + 600}Z" fill="url(#${P.ray})" opacity="${op}"/>`; });
      put(L.glow, g + "</g>");
    }
    // foreground: a big trunk on one edge and a leafy branch hanging in
    let fg = "";
    if (o.fgTrunk !== false) { const left = (o.fgTrunk || "left") === "left"; fg += trunk2(left ? -80 : 1160, 2400, 3400, 220, P, r, { cast: false }); }
    if (o.fgLeaves !== false) for (let k = 0; k < 7; k++) { const x = 760 + k * 60 + r() * 40, y = -160 + r() * 140; fg += `<path d="M${f1(x)},${f1(y)}q${f1(-40 - r() * 40)},${f1(120 + r() * 60)} ${f1(-10 + r() * 20)},${f1(220 + r() * 80)}q${f1(30 + r() * 30)},${f1(-120)} ${f1(10)},${f1(-220)}z" fill="url(#${P.leaf[k % 2]})" opacity=".95"/>`; }
    put(L.fg, fg);
  }

  // a reaching hand, back of the hand up, fingers to -x, slightly curled; the wrist at (0, 0), the forearm tapering off to +x
  function reach(o = {}) {
    const sk = o.skin || "#c98e5e", sh = Rig2.shade(sk, 0.18), sh2 = Rig2.shade(sk, 0.3), dkS = Rig2.shade(sk, 0.42), L = o.len || 900;
    const finger = (pts, w, c) => { const d = `M${pts[0]}Q${pts[1]} ${pts[2]}`; return `<path d="${d}" stroke="${LN}" stroke-width="${w + 6}" fill="none" stroke-linecap="round"/><path d="${d}" stroke="${c}" stroke-width="${w}" fill="none" stroke-linecap="round"/>`; };
    let g = `<path d="M10,-40Q${L * 0.5},-62 ${L},-74V74Q${L * 0.5},62 10,42Z" fill="${o.sleeve || sk}" stroke="${LN}" stroke-width="3"/>
      <path d="M20,-30Q${L * 0.5},-50 ${L},-60V-30Q${L * 0.5},-24 20,-14Z" fill="#fff" opacity=".14"/><path d="M20,24Q${L * 0.5},40 ${L},48V74Q${L * 0.5},62 10,42Z" fill="#1c1030" opacity=".2"/>`;
    g += finger(["-100,30", "-142,44", "-170,62"], 20, sh2) + finger(["-112,12", "-170,20", "-206,40"], 24, sh) + finger(["-118,-8", "-186,-6", "-226,12"], 26, sh);
    g += `<path d="M20,-42C-30,-50 -90,-46 -122,-34C-132,-10 -128,18 -110,36C-70,48 -20,46 20,44Z" fill="${sk}" stroke="${LN}" stroke-width="3" stroke-linejoin="round"/>`;
    g += `<path d="M10,-38C-40,-44 -90,-40 -118,-30" stroke="#fff" stroke-width="5" fill="none" opacity=".22" stroke-linecap="round"/>`;
    g += finger(["-114,-28", "-178,-34", "-222,-18"], 26, sk);
    g += `<path d="M-160,-38q8,8 0,16M-172,-14q8,8 0,16M-160,8q7,7 0,14" stroke="${dkS}" stroke-width="2.4" fill="none" opacity=".6"/>`;
    g += `<ellipse cx="-226" cy="-21" rx="9" ry="6" fill="#f4dccc" transform="rotate(20 -226 -21)"/><ellipse cx="-230" cy="10" rx="8" ry="5.5" fill="#f0d4c2" opacity=".85" transform="rotate(35 -230 10)"/>`;
    g += `<path d="M-60,-40q14,-5 26,0M-96,-38q10,-4 20,0" stroke="${dkS}" stroke-width="2.4" fill="none" opacity=".45"/>`;
    g += finger(["-30,30", "-84,56", "-124,58"], 30, sk) + `<ellipse cx="-128" cy="56" rx="9" ry="6" fill="#f4dccc" transform="rotate(-10 -128 56)"/>`;
    return g;
  }

  // the money shot: the camera on the forest floor, the white amanitas big against the blurred mound and the sun through the leaves
  //   o.v "cluster" | "pair" · o.hand (a reaching hand #id-hand, parked off right) · o.time day | dusk | night
  function mushHero(L, o = {}) {
    const id = o.id || "mh", r = mk(o.seed || 91), t = o.time || "day", P = PAL[t], HZ = o.horizon ?? 1080, FY = o.foot ?? 1480;
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${P.sky})"/>`;
    if (t !== "night") { sky += `<circle cx="180" cy="300" r="700" fill="url(#p2Sun)"/>`;
      for (let k = 0; k < 26; k++) { const x = -200 + r() * 1500, y = -100 + r() * 1100, R = 20 + r() * 70; sky += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(R)}" fill="url(#mGlow)" opacity="${f1(0.4 + r() * 0.5)}"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(R * 0.7)}" fill="none" stroke="#fffbe8" stroke-width="2" opacity=".18"/>`; } }
    put(L.sky, sky);
    // far: soft trunks and the mound as a wall of red earth
    let far = "";
    [[-60, 140], [1020, 180], [300, 70]].forEach(([x, w]) => { far += `<rect x="${x - w / 2}" y="-900" width="${w}" height="${HZ + 1000}" fill="${P.mid}" opacity=".55"/>`; });
    if (o.mound !== false) far += `<g transform="translate(${o.moundX ?? 720},${HZ + 60}) scale(3.4)">${mound2(0, 0, 1, P, r).replace(/^<g [^>]*>/, "").replace(/<\/g>$/, "")}</g>`;
    far += `<rect x="-1300" y="${HZ - 300}" width="3700" height="400" fill="url(#${P.haze})" opacity=".55"/>`;
    put(L.far, far);
    // mid: the far forest floor, small litter and grass against the light
    let mid = `<rect x="-1300" y="${HZ - 40}" width="3700" height="400" fill="${P.groundTop}"/>`;
    for (let k = 0; k < 200; k++) { const y = HZ - 30 + r() * 220; mid += litter(-1200 + r() * 3500, y, 0.6 + (y - HZ) / 200, P.litter[Math.floor(r() * 5)], r); }
    for (let k = 0; k < 30; k++) mid += tuft(-1100 + r() * 3300, HZ - 10 + r() * 200, 0.8 + r() * 0.6, P.grass[0], P.grass[1], r);
    put(L.mid, mid);
    // set: the near floor and the mushrooms
    let s = `<rect x="-1300" y="${HZ + 120}" width="3700" height="1800" fill="url(#${P.ground})"/><rect x="-1300" y="${HZ + 60}" width="3700" height="64" fill="url(#${id}-gf)"/>
      <defs><linearGradient id="${id}-gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.groundTop}" stop-opacity="0"/><stop offset="1" stop-color="${P.groundTop}"/></linearGradient></defs>`;
    for (let k = 0; k < 260; k++) { const y = HZ + 100 + Math.pow(r(), 0.7) * 900; s += litter(-1200 + r() * 3500, y, 1 + (y - HZ) / 160, P.litter[Math.floor(r() * 5)], r); }
    for (let k = 0; k < 40; k++) { const x = -200 + r() * 1500, y = HZ + 120 + r() * 800; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(3 + r() * 6)}" ry="${f1(2 + r() * 4)}" fill="#5a2a14" opacity=".5"/>`; }
    for (let k = 0; k < 18; k++) s += tuft(-100 + r() * 1300, HZ + 160 + r() * 600, 1.4 + r(), P.grass[0], P.grass[1], r);
    const M = o.v === "pair" ? [[330, FY, 1.45, "open", -3], [760, FY, 1.45, "open", 3]]
      : [[200, FY - 70, 0.55, "egg", 0], [330, FY - 20, 0.95, "button", -4], [560, FY, 1.55, "open", 2], [790, FY - 40, 1.15, "open", 6], [930, FY - 80, 0.6, "egg", 0]];
    M.forEach(([x, y, k, v, tilt], i) => {
      s += `<ellipse cx="${x}" cy="${y - 240 * k}" rx="${f1(220 * k)}" ry="${f1(220 * k)}" fill="url(#mGlow)" opacity=".5"/>`;
      s += mush2(x, y, k, { v, tilt, id: `${id}-m${i}` });
      if (v === "open") for (let d = 0; d < 4; d++) { const dx = (r() - 0.5) * 140 * k, dy = -(250 + 60 + r() * 30) * k; s += `<g transform="translate(${f1(x + dx)},${f1(y + dy)})"><circle r="${f1(4 + r() * 4)}" fill="#e8f0f4" opacity=".75" stroke="#b8c4c8" stroke-width="1"/><circle cx="-1.5" cy="-1.5" r="1.6" fill="#fff"/></g>`; }
    });
    put(L.set, s);
    if (P.ray) put(L.glow, `<g id="${id}-rays" style="mix-blend-mode:screen"><path d="M-300,-700L-40,-700L${f1(860)},${FY}L${f1(380)},${FY}Z" fill="url(#${P.ray})" opacity=".55"/><path d="M200,-700L320,-700L1100,${FY}L860,${FY}Z" fill="url(#${P.ray})" opacity=".3"/></g>`);
    if (o.hand) put(L.set, `<g id="${id}-hand"><g transform="translate(1500,${FY - 260}) rotate(${o.handRot ?? 12}) scale(${o.handS ?? 1.6})">${reach({ skin: o.handSkin })}</g></g>`);
    // foreground: big out-of-focus leaves and blades
    let fg = "";
    for (let k = 0; k < 9; k++) fg += litter(-80 + k * 150 + r() * 60, 1880 + r() * 80, 7 + r() * 3, P.litter[k % 5], r);
    for (let k = 0; k < 5; k++) fg += tuft(k < 3 ? -40 + k * 60 : 1000 + k * 30, 2000, 5 + r() * 2, P.grass[0], P.grass[1], r);
    put(L.fg, fg);
  }

  Object.assign(Sets, { kok2, mushHero });
  Object.assign(Pop2, { mush2, mound2, trunk2, crownK, litter, reach, KPAL: PAL });
})();
