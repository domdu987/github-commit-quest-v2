// ต้นตะเคียนกลางนา (เลน B · 2 พ.ย. 2569): sets, props and cast.
//   Sets.tkField(L, o)  a rain-season rice field late in the afternoon, one giant ตะเคียน in the middle of it.
//     o.mood "storm" | "calm" | "clear" (sky + light) · o.dark 0..1 how black the storm is · o.rain 0..1 · o.flash 0..1 (sky lit by lightning)
//     o.tree {x, y, s} the tree (base of the trunk at x,y) · o.hut {x, y, s} the เถียงนา · o.buf {x, y, s, flip} the buffalo tied to its stake
//     o.bolt 0..1 a strike on the tree top (+ o.side [[x,y],…] side-flash arcs from the trunk) · o.horizon y of the horizon (default 980)
//     o.far false hides the far treeline · o.fgRice true adds out-of-focus rice in front
//   Sets.tkHut(L, o)    inside-out: under the เถียงนา roof looking out at the tree across the paddies (o.tree, o.rain, o.dark, o.flash)
//   Sets.tkCPR(L, o)    top-down on the muddy bund: ลุงเปี๊ยก on his back, rain, the rescuer's stacked hands (o.hands), the phone on the grass (o.phone)
//   Tk.tree / Tk.hut / Tk.buffalo / Tk.dog / Tk.bolt / Tk.shrine  (strings, world coords)
//   cast: ploy (พลอย 17, the granddaughter home to help plant rice) · yaiHom (ยายหอม 72) · lungPiak (ลุงเปี๊ยก 55, the neighbour) · ton (ต้น 9)
(function () {
  const INK = "#1e1a16";
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Tk = (window.Tk = window.Tk || {});

  Sets.DEFS += `
    <linearGradient id="tkSkyS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1e2c"/><stop offset=".55" stop-color="#3a3c4e"/><stop offset="1" stop-color="#7a7a6e"/></linearGradient>
    <linearGradient id="tkSkyC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a8ac8"/><stop offset=".6" stop-color="#a8c4d8"/><stop offset="1" stop-color="#f2d8a0"/></linearGradient>
    <linearGradient id="tkSkyA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a9ad8"/><stop offset=".6" stop-color="#b8d4e8"/><stop offset="1" stop-color="#e8eef0"/></linearGradient>
    <linearGradient id="tkCloud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4c60"/><stop offset="1" stop-color="#1e2030"/></linearGradient>
    <linearGradient id="tkCloudC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c8d0e0"/></linearGradient>
    <linearGradient id="tkPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a8a4a"/><stop offset="1" stop-color="#3a6a2a"/></linearGradient>
    <linearGradient id="tkPaddyS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5e3e"/><stop offset="1" stop-color="#22382a"/></linearGradient>
    <linearGradient id="tkWaterS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a6c7a"/><stop offset="1" stop-color="#3a3e4a"/></linearGradient>
    <linearGradient id="tkWaterC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8d8e8"/><stop offset="1" stop-color="#7aa0c0"/></linearGradient>
    <linearGradient id="tkBark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1c14"/><stop offset=".35" stop-color="#6a4a32"/><stop offset=".6" stop-color="#4a3222"/><stop offset="1" stop-color="#1e140e"/></linearGradient>
    <radialGradient id="tkLeaf" cx=".4" cy=".3"><stop offset="0" stop-color="#4a7a3a"/><stop offset=".7" stop-color="#24482a"/><stop offset="1" stop-color="#14281a"/></radialGradient>
    <radialGradient id="tkLeafS" cx=".4" cy=".3"><stop offset="0" stop-color="#2e4a32"/><stop offset=".7" stop-color="#18301e"/><stop offset="1" stop-color="#0c1810"/></radialGradient>
    <radialGradient id="tkFlash" cx=".5" cy=".2" r=".8"><stop offset="0" stop-color="#eef4ff" stop-opacity=".95"/><stop offset=".5" stop-color="#b8c8ff" stop-opacity=".35"/><stop offset="1" stop-color="#8aa0ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="tkBoltG"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".4" stop-color="#cfe0ff" stop-opacity=".5"/><stop offset="1" stop-color="#8aa8ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="tkSun"><stop offset="0" stop-color="#fff2c0" stop-opacity=".9"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
    <linearGradient id="tkMud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a5a42"/><stop offset="1" stop-color="#4a3e2e"/></linearGradient>`;

  const STORM = (m) => m === "storm";
  // ---------------------------------------------------------------- props
  const CLOTH = ["#d8302a", "#f2c230", "#3aa04a", "#e86aa8", "#2a6ad0", "#8a3ab8", "#f07a1a"];
  Tk.shrine = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})">
    <path d="M-8,0V-170M8,0V-170" stroke="${INK}" stroke-width="20"/><path d="M-8,0V-170M8,0V-170" stroke="#8a6a4a" stroke-width="12"/>
    <rect x="-70" y="-250" width="140" height="90" fill="#e8d8b0" ${OUT(4)}/><rect x="-28" y="-228" width="56" height="68" fill="#3a2a1e"/>
    <path d="M-96,-246L0,-320L96,-246Z" fill="#c83a2a" ${OUT(4)}/><path d="M0,-320l-10,-28l10,-12l10,12z" fill="#f2c230" ${OUT(2)}/>
    <rect x="-84" y="-164" width="168" height="16" fill="#8a6a4a" ${OUT(3)}/>
    ${[-50, -24, 24, 50].map((dx, k) => `<g transform="translate(${dx},-176)"><circle r="9" fill="${["#f2f0ea", "#e86aa8", "#f2c230", "#f2f0ea"][k]}" ${OUT(2)}/><path d="M0,9v12" stroke="${INK}" stroke-width="3"/></g>`).join("")}
    <path d="M-60,-160q20,30 40,0q20,30 40,0q20,30 40,0" stroke="#f2c230" stroke-width="7" fill="none"/></g>`;
  Tk.tree = (x, y, s = 1, o = {}) => {
    const r = mk(o.seed || 77), storm = o.storm, leaf = storm ? "tkLeafS" : "tkLeaf", rim = storm ? "#9ab0e8" : "#ffe2a0";
    let g = `<g transform="translate(${x},${y}) scale(${s})">`;
    g += `<ellipse cx="0" cy="10" rx="520" ry="60" fill="#000" opacity=".3"/>`;
    // buttress roots and trunk
    g += `<path d="M-260,10Q-170,-10 -120,-120L-110,-780Q-60,-840 0,-840Q70,-840 110,-780L120,-120Q170,-10 270,10Z" fill="url(#tkBark)" ${OUT(6)}/>`;
    g += [-190, -70, 80, 200].map((dx) => `<path d="M${dx},10Q${dx * 0.6},-60 ${dx * 0.4},-160" stroke="#1e140e" stroke-width="10" fill="none"/>`).join("");
    for (let k = 0; k < 9; k++) g += `<path d="M${f1(-90 + r() * 180)},${f1(-200 - r() * 560)}q${f1(-10 + r() * 20)},-60 ${f1(-6 + r() * 12)},-120" stroke="#2a1c14" stroke-width="6" fill="none" opacity=".7"/>`;
    // the seven-colour cloths wound round the trunk + a garland
    CLOTH.forEach((c, k) => { const yy = -300 - k * 26; g += `<path d="M-116,${yy}Q0,${yy + 22} 116,${yy}V${yy + 24}Q0,${yy + 46} -116,${yy + 24}Z" fill="${c}" ${OUT(3)}/>`; });
    g += `<path d="M60,-292q30,60 10,150" stroke="#d8302a" stroke-width="18" fill="none"/><path d="M80,-290q40,70 30,160" stroke="#f2c230" stroke-width="14" fill="none"/><path d="M40,-286q10,60 -10,120" stroke="#3aa04a" stroke-width="12" fill="none"/>`;
    g += `<path d="M-110,-150Q0,-90 110,-150" stroke="#f2f0ea" stroke-width="12" fill="none" stroke-dasharray="14 8"/>`;
    // big limbs
    g += `<path d="M-60,-760Q-260,-880 -430,-900" stroke="${INK}" stroke-width="54" fill="none" stroke-linecap="round"/><path d="M-60,-760Q-260,-880 -430,-900" stroke="#4a3222" stroke-width="42" fill="none" stroke-linecap="round"/>
      <path d="M60,-770Q260,-900 450,-930" stroke="${INK}" stroke-width="54" fill="none" stroke-linecap="round"/><path d="M60,-770Q260,-900 450,-930" stroke="#4a3222" stroke-width="42" fill="none" stroke-linecap="round"/>
      <path d="M0,-830Q10,-1000 -20,-1120" stroke="${INK}" stroke-width="46" fill="none" stroke-linecap="round"/><path d="M0,-830Q10,-1000 -20,-1120" stroke="#4a3222" stroke-width="34" fill="none" stroke-linecap="round"/>`;
    // the crown: overlapping leaf masses, dark below, a rim on top
    const blobs = [[-420, -960, 230], [-220, -1080, 270], [0, -1200, 300], [230, -1090, 280], [440, -980, 230], [-300, -880, 200], [300, -880, 210], [0, -960, 280], [-120, -1300, 200], [140, -1290, 200]];
    g += blobs.map(([bx, by, br]) => `<ellipse cx="${bx}" cy="${by}" rx="${br}" ry="${br * 0.72}" fill="url(#${leaf})" ${OUT(5)}/>`).join("");
    g += blobs.slice(0, 5).concat(blobs.slice(8)).map(([bx, by, br]) => `<path d="M${bx - br * 0.7},${by - br * 0.4}Q${bx},${by - br * 0.85} ${bx + br * 0.7},${by - br * 0.4}" stroke="${rim}" stroke-width="8" fill="none" opacity=".45" stroke-linecap="round"/>`).join("");
    for (let k = 0; k < 60; k++) { const a = r() * Math.PI * 2, d = r(); g += `<ellipse cx="${f1(Math.cos(a) * 480 * d)}" cy="${f1(-1080 + Math.sin(a) * 260 * d)}" rx="${f1(10 + r() * 14)}" ry="${f1(5 + r() * 6)}" fill="${storm ? "#3a5a3e" : "#6a9a4a"}" opacity=".6" transform="rotate(${f1(r() * 180)} ${f1(Math.cos(a) * 480 * d)} ${f1(-1080 + Math.sin(a) * 260 * d)})"/>`; }
    // the shrine at the foot
    if (o.shrine !== false) g += Tk.shrine(-250, 0, 0.9);
    // scorch + split after the strike
    if (o.burnt) g += `<path d="M10,-840L-20,-640L20,-500L-10,-300L16,-120" stroke="#ff9a3a" stroke-width="10" fill="none" opacity="${f1(o.burnt)}"/><path d="M10,-840L-20,-640L20,-500L-10,-300L16,-120" stroke="#fff2b0" stroke-width="4" fill="none" opacity="${f1(o.burnt)}"/>`;
    return g + `</g>`;
  };
  Tk.hut = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})">
    <ellipse cx="0" cy="8" rx="300" ry="30" fill="#000" opacity=".25"/>
    ${[-230, -80, 80, 230].map((dx) => `<rect x="${dx - 12}" y="-340" width="24" height="340" fill="#6a4a32" ${OUT(4)}/>`).join("")}
    <rect x="-270" y="-250" width="540" height="40" fill="#8a6a4a" ${OUT(4)}/>${[-200, -100, 0, 100, 200].map((dx) => `<path d="M${dx},-250v40" stroke="#5a4030" stroke-width="5"/>`).join("")}
    <path d="M-250,-250V-330M250,-250V-330" stroke="#6a4a32" stroke-width="10"/><path d="M-250,-300H250" stroke="#6a4a32" stroke-width="8"/>
    <path d="M-340,-440L-200,-560H200L340,-440Z" fill="#c8a058" ${OUT(5)}/>${Array.from({ length: 14 }, (_, k) => `<path d="M${-320 + k * 48},-442l${18},${-110 + Math.abs(k - 6.5) * 0}" stroke="#a07a3a" stroke-width="5" opacity=".8"/>`).join("")}
    <path d="M-340,-440Q0,-420 340,-440" stroke="#8a6a2a" stroke-width="8" fill="none"/>
    <path d="M-200,-560V-440M200,-560V-440" stroke="#5a4030" stroke-width="10"/>
    <g transform="translate(-140,-250)"><path d="M0,0L30,250M60,0L90,250" stroke="#6a4a32" stroke-width="8"/>${[50, 110, 170, 230].map((yy) => `<path d="M${yy * 0.12},${yy}H${60 + yy * 0.12}" stroke="#6a4a32" stroke-width="7"/>`).join("")}</g>
    ${o.items !== false ? `<g transform="translate(120,-290)"><ellipse rx="40" ry="14" fill="#c84a2a" ${OUT(3)}/><path d="M-40,0q40,-40 80,0" fill="#a83a1a" ${OUT(3)}/></g><g transform="translate(40,-270)"><path d="M-30,0L-20,-60H20L30,0Z" fill="#e8e0c8" ${OUT(3)}/></g>` : ""}</g>`;
  Tk.buffalo = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${o.flip ? -s : s},${s})">
    <ellipse cx="0" cy="6" rx="220" ry="26" fill="#000" opacity=".3"/>
    ${[-130, -70, 90, 150].map((dx) => `<path d="M${dx},-60V0" stroke="${INK}" stroke-width="34" stroke-linecap="round"/><path d="M${dx},-60V0" stroke="#3a3a40" stroke-width="24" stroke-linecap="round"/>`).join("")}
    <path d="M-180,-110Q-190,-230 -60,-240Q120,-250 180,-200Q210,-160 190,-90Q170,-50 80,-50H-130Q-180,-60 -180,-110Z" fill="#4a4a52" ${OUT(5)}/>
    <path d="M-150,-200Q-40,-236 140,-210" stroke="#6a6a74" stroke-width="10" fill="none" opacity=".7"/>
    <g transform="translate(220,-170)"><path d="M-50,-30Q0,-60 40,-30Q70,10 50,50Q30,70 0,64Q-40,60 -54,20Z" fill="#4a4a52" ${OUT(5)}/><ellipse cx="30" cy="50" rx="30" ry="20" fill="#5a5a62" ${OUT(3)}/>
      <circle cx="14" cy="0" r="7" fill="${INK}"/><circle cx="16" cy="-2" r="2.5" fill="#fff"/>
      <path d="M-30,-36Q-120,-70 -110,-10Q-80,-50 -24,-24Z" fill="#a89a80" ${OUT(4)}/><path d="M20,-44Q90,-110 120,-40Q90,-70 30,-30Z" fill="#a89a80" ${OUT(4)}/></g>
    <path d="M-180,-120q-30,40 -16,100" stroke="#3a3a40" stroke-width="10" fill="none"/>
    ${o.rope ? `<path d="M260,-130Q${o.rope[0] / s},${-60} ${o.rope[0] / s},${o.rope[1] / s}" stroke="#c8a870" stroke-width="5" fill="none"/>` : ""}</g>`;
  Tk.dog = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${o.flip ? -s : s},${s})">
    <ellipse cx="0" cy="4" rx="90" ry="14" fill="#000" opacity=".3"/>
    ${[-50, -24, 30, 56].map((dx) => `<path d="M${dx},-40V0" stroke="${INK}" stroke-width="18" stroke-linecap="round"/><path d="M${dx},-40V0" stroke="#c8925a" stroke-width="11" stroke-linecap="round"/>`).join("")}
    <ellipse cx="0" cy="-60" rx="80" ry="38" fill="#c8925a" ${OUT(4)}/><ellipse cx="10" cy="-44" rx="40" ry="16" fill="#f2e2c8"/>
    <path d="M-76,-70q-34,-30 -30,-70" stroke="${INK}" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M-76,-70q-34,-30 -30,-70" stroke="#c8925a" stroke-width="9" fill="none" stroke-linecap="round"/>
    <g transform="translate(78,-96)"><circle r="36" fill="#c8925a" ${OUT(4)}/><path d="M-26,-24Q-46,0 -30,30Q-18,10 -12,-20Z" fill="#7a4a2a" ${OUT(3)}/><path d="M18,-30Q40,-10 34,20Q22,4 12,-24Z" fill="#7a4a2a" ${OUT(3)}/>
      <ellipse cx="30" cy="14" rx="20" ry="14" fill="#f2e2c8" ${OUT(3)}/><circle cx="44" cy="8" r="6" fill="${INK}"/><circle cx="8" cy="-6" r="5" fill="${INK}"/><circle cx="26" cy="-8" r="5" fill="${INK}"/>
      ${o.bark ? `<path d="M30,26q10,14 20,0" fill="#c84a5a" ${OUT(2)}/>` : ""}</g>
    <path d="M60,-74q16,6 30,-2" stroke="#d8302a" stroke-width="7" fill="none"/></g>`;
  // the bolt: jagged main channel from (x0,y0) to (x1,y1) + branches + glow
  Tk.bolt = (x0, y0, x1, y1, seed = 5, w = 1) => {
    const r = mk(seed), n = 12; let pts = [[x0, y0]];
    for (let k = 1; k < n; k++) { const t = k / n; pts.push([x0 + (x1 - x0) * t + (r() - 0.5) * 120, y0 + (y1 - y0) * t]); }
    pts.push([x1, y1]);
    const d = "M" + pts.map((p) => p.map(f1).join(",")).join("L");
    let br = "";
    [3, 6, 8].forEach((k) => { const [bx, by] = pts[k]; let q = [[bx, by]]; for (let j = 1; j < 5; j++) q.push([bx + (r() - 0.3) * 60 * j * (k % 2 ? 1 : -1), by + j * 50]); br += `<path d="M${q.map((p) => p.map(f1).join(",")).join("L")}" stroke="#e8f0ff" stroke-width="${f1(5 * w)}" fill="none" opacity=".8"/>`; });
    return `<g><path d="${d}" stroke="#8aa8ff" stroke-width="${f1(40 * w)}" fill="none" opacity=".35" stroke-linejoin="round"/><path d="${d}" stroke="#dfe8ff" stroke-width="${f1(16 * w)}" fill="none" stroke-linejoin="round"/><path d="${d}" stroke="#ffffff" stroke-width="${f1(7 * w)}" fill="none" stroke-linejoin="round"/>${br}</g>`;
  };
  // ลุงเปี๊ยก fallen on his back, side view (x,y = his hips on the ground); o.smoke: wisps off his shirt
  Tk.lying = (x, y, s = 1, o = {}) => { const sk = "#b0805a"; return `<g transform="translate(${x},${y}) scale(${o.flip ? -s : s},${s})">
    <ellipse cx="40" cy="8" rx="380" ry="26" fill="#000" opacity=".35"/>
    <path d="M0,-30L-150,-40L-300,-20" stroke="${INK}" stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M0,-30L-150,-40L-300,-20" stroke="${sk}" stroke-width="52" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M-10,-40H-150" stroke="${INK}" stroke-width="80" stroke-linecap="round"/><path d="M-10,-40H-150" stroke="#a8946a" stroke-width="68" stroke-linecap="round"/>
    <ellipse cx="-318" cy="-34" rx="24" ry="34" fill="${sk}" ${OUT(4)}/>
    <path d="M-20,-90Q120,-120 250,-80L250,0H-20Z" fill="#d8582a" ${OUT(5)}/>
    ${[[30, -60], [100, -80], [170, -50], [210, -84], [60, -24], [140, -20]].map(([fx, fy]) => `<g transform="translate(${fx},${fy})">${[0, 72, 144, 216, 288].map((a) => `<ellipse rx="9" ry="4.5" fill="#f2c230" transform="rotate(${a}) translate(8,0)"/>`).join("")}<circle r="3.5" fill="#fff"/></g>`).join("")}
    <path d="M200,-40L120,20L20,30" stroke="${INK}" stroke-width="44" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M200,-40L120,20L20,30" stroke="${sk}" stroke-width="34" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="248" y="-60" width="40" height="40" fill="${sk}" ${OUT(4)}/>
    <g transform="translate(350,-56)"><ellipse rx="72" ry="66" fill="${sk}" ${OUT(5)}/><path d="M-20,-66Q40,-80 70,-20L50,-10Q30,-60 -20,-50Z" fill="#e8e4d8" ${OUT(3)}/><path d="M0,-60Q40,-70 62,-24" stroke="#c83a2a" stroke-width="6" fill="none" stroke-dasharray="10 8"/>
      <path d="M10,-6q14,6 28,0" stroke="#3a2a22" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M-30,30q16,4 30,-2" stroke="#3a2a22" stroke-width="5" fill="none" stroke-linecap="round"/><ellipse cx="62" cy="10" rx="10" ry="12" fill="${sk}" ${OUT(3)}/></g>
    ${o.smoke ? [0, 1, 2].map((k) => `<path d="M${60 + k * 70},-110q-20,-40 0,-80t0,-80" stroke="#cfd4d8" stroke-width="10" fill="none" opacity="${f1(0.5 - k * 0.1)}" stroke-linecap="round"/>`).join("") : ""}</g>`; };
  const arc = (x0, y0, x1, y1, seed) => { const r = mk(seed); let p = `M${x0},${y0}`; for (let k = 1; k <= 6; k++) { const t = k / 6; p += `L${f1(x0 + (x1 - x0) * t + (r() - 0.5) * 40)},${f1(y0 + (y1 - y0) * t + (r() - 0.5) * 30)}`; } return `<path d="${p}" stroke="#9ab8ff" stroke-width="16" fill="none" opacity=".4"/><path d="${p}" stroke="#ffffff" stroke-width="5" fill="none"/>`; };

  const sky = (L, o, hz) => {
    const m = o.mood || "storm", r = mk(o.seed || 9), dark = o.dark ?? 0.7;
    put(L.sky, `<rect x="-900" y="-800" width="2900" height="${hz + 800 + 40}" fill="url(#${STORM(m) ? "tkSkyS" : m === "clear" ? "tkSkyA" : "tkSkyC"})"/>`);
    let c = "";
    if (STORM(m)) {
      // the anvil: a dark wall of cloud, lighter churning underside, and a ragged rain curtain at the horizon
      c += `<path d="M-900,-800H2000V${f1(380 + 200 * (1 - dark))}Q1600,${f1(520 - 120 * dark)} 1200,${f1(450 - 60 * dark)}Q800,${f1(600 - 120 * dark)} 400,${f1(470 - 60 * dark)}Q0,${f1(580 - 100 * dark)} -900,${f1(430 - 60 * dark)}Z" fill="url(#tkCloud)" opacity="${f1(0.75 + 0.25 * dark)}"/>`;
      for (let k = 0; k < 22; k++) c += `<ellipse cx="${f1(-700 + r() * 2400)}" cy="${f1(300 + r() * 260)}" rx="${f1(120 + r() * 220)}" ry="${f1(50 + r() * 60)}" fill="#55586c" opacity="${f1(0.25 + r() * 0.3)}"/>`;
      for (let k = 0; k < 18; k++) { const x = -800 + r() * 2600; c += `<path d="M${f1(x)},${f1(500 + r() * 100)}L${f1(x - 60)},${hz}" stroke="#5a5e70" stroke-width="${f1(30 + r() * 60)}" opacity=".18"/>`; }
      if (o.flash) c += `<rect x="-900" y="-800" width="2900" height="${hz + 840}" fill="url(#tkFlash)" opacity="${f1(o.flash)}"/>`;
      if (o.distBolt) c += `<g opacity=".85">${Tk.bolt(o.distBolt[0], 420, o.distBolt[1], hz - 10, 41, 0.45)}</g>`;
    } else {
      c += `<circle cx="${m === "clear" ? 820 : 900}" cy="${m === "clear" ? 300 : 760}" r="300" fill="url(#tkSun)"/>`;
      for (let k = 0; k < 7; k++) { const cx = -500 + r() * 2000, cy = 150 + r() * 400; c += `<g opacity="${m === "clear" ? 0.9 : 0.75}">${[0, 1, 2, 3].map((j) => `<ellipse cx="${f1(cx + j * 70 - 100)}" cy="${f1(cy - (j % 2) * 30)}" rx="${f1(90 + r() * 60)}" ry="${f1(50 + r() * 20)}" fill="url(#tkCloudC)"/>`).join("")}</g>`; }
      if (m === "clear") c += `<path d="M-200,${hz}A700,700 0 0 1 1300,${hz}" stroke="#ff8a8a" stroke-width="24" fill="none" opacity=".18"/><path d="M-170,${hz}A670,670 0 0 1 1270,${hz}" stroke="#ffe08a" stroke-width="24" fill="none" opacity=".18"/><path d="M-140,${hz}A640,640 0 0 1 1240,${hz}" stroke="#8ae0a8" stroke-width="24" fill="none" opacity=".18"/>`;
      // far storm still grumbling on the horizon in "clear": the danger cue
      if (m === "clear" && o.farStorm) c += `<path d="M-900,${hz - 20}Q-500,${hz - 260} -200,${hz - 200}Q0,${hz - 300} 200,${hz - 120}V${hz}H-900Z" fill="#4a4c60" opacity=".85"/>${o.farBolt ? `<g opacity=".9">${Tk.bolt(-120, hz - 230, -60, hz - 10, 13, 0.35)}</g>` : ""}`;
    }
    put(L.sky, c);
  };
  const paddies = (L, o, hz) => {
    const m = o.mood || "storm", r = mk((o.seed || 9) + 3), S = STORM(m), d = o.dark ?? 0.7;
    if (o.far !== false) {
      let f = `<path d="M-900,${hz}Q-600,${hz - 70} -300,${hz - 40}Q0,${hz - 90} 300,${hz - 50}Q600,${hz - 80} 900,${hz - 40}Q1300,${hz - 70} 2000,${hz - 30}V${hz + 10}H-900Z" fill="${S ? "#2a3430" : "#5a7a6a"}"/>`;
      for (let k = 0; k < 30; k++) { const x = -800 + r() * 2700; f += `<ellipse cx="${f1(x)}" cy="${f1(hz - 30 - r() * 30)}" rx="${f1(30 + r() * 50)}" ry="${f1(20 + r() * 30)}" fill="${S ? "#222c28" : "#4a6a52"}"/>`; }
      // a village: roofs and a wat spire far left, a line of power poles
      f += `<g opacity=".9">${[-560, -480, -400, 1360, 1440].map((x) => `<path d="M${x},${hz - 6}V${hz - 30}L${x + 30},${hz - 50}L${x + 60},${hz - 30}V${hz - 6}Z" fill="${S ? "#1e2624" : "#7a6a5a"}"/>`).join("")}<path d="M-300,${hz - 4}V${hz - 80}L-290,${hz - 120}L-280,${hz - 80}V${hz - 4}Z" fill="${S ? "#1e2624" : "#c8a868"}"/></g>`;
      put(L.far, f);
    }
    // the paddies in perspective: bands of planted rice, water between, bunds in lighter mud
    let p = `<rect x="-1400" y="${hz}" width="3900" height="${5000 - hz}" fill="url(#${S ? "tkPaddyS" : "tkPaddy"})"/>`;
    const rows = 26;
    for (let k = 0; k < rows; k++) {
      const t = k / rows, y = hz + Math.pow(t, 1.8) * (4200 - hz), h = 4 + 60 * Math.pow(t, 1.6);
      if (k % 5 === 2) p += `<path d="M-1400,${f1(y)}H2500V${f1(y + h * 1.4)}H-900Z" fill="url(#${S ? "tkWaterS" : "tkWaterC"})" opacity=".8"/>`;
      else if (k % 5 === 4) p += `<path d="M-1400,${f1(y)}H2500V${f1(y + h * 0.7)}H-900Z" fill="url(#tkMud)" opacity="${S ? 0.75 : 0.95}"/>`;
      else { const step = 10 + 50 * t; let tufts = ""; for (let x = -1400; x < 2500; x += step) tufts += `M${f1(x + r() * step * 0.4)},${f1(y + h)}l${f1(-3 - 6 * t)},${f1(-h)}M${f1(x + step * 0.3)},${f1(y + h)}l${f1(4 + 6 * t)},${f1(-h * 1.1)}`; p += `<path d="${tufts}" stroke="${S ? "#5a7a4a" : "#9ac85a"}" stroke-width="${f1(1.5 + 4 * t)}" opacity=".75"/>`; }
    }
    // a bund running from the foreground toward the tree (where the family runs)
    if (o.bund !== false) { const bx = o.bundX ?? 540; p += `<path d="M${bx - 30},${hz + 40}L${bx + 30},${hz + 40}L${bx + 700},4400L${bx - 700},4400Z" fill="url(#tkMud)" opacity="${S ? 0.85 : 1}"/><path d="M${bx - 30},${hz + 40}L${bx - 700},4400" stroke="#3a3022" stroke-width="6" opacity=".6"/>`; }
    put(L.mid, p);
    if (S) put(L.mid, `<rect x="-900" y="${hz - 200}" width="2900" height="400" fill="#7a7e8a" opacity="${f1(0.15 + 0.15 * d)}"/>`);
  };
  const rain = (L, o) => {
    const k = o.rain ?? 0; if (!k) return; const r = mk(321);
    let g = `<g opacity="${f1(0.5 + 0.4 * k)}">`;
    for (let i = 0; i < Math.round(160 * k); i++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, l = 40 + r() * 70; g += `<path d="M${f1(x)},${f1(y)}l${f1(-l * 0.22)},${f1(l)}" stroke="#cfd8ea" stroke-width="${f1(1.6 + r() * 2)}" opacity="${f1(0.35 + r() * 0.4)}" stroke-linecap="round"/>`; }
    for (let i = 0; i < Math.round(30 * k); i++) g += `<ellipse cx="${f1(-100 + r() * 1300)}" cy="${f1(1300 + r() * 700)}" rx="${f1(10 + r() * 16)}" ry="${f1(3 + r() * 4)}" fill="none" stroke="#cfd8ea" stroke-width="2" opacity=".45"/>`;
    put(L.light, g + `</g>`);
  };

  Sets.tkField = function (L, o = {}) {
    const hz = o.horizon ?? 980, m = o.mood || "storm", S = STORM(m);
    sky(L, o, hz);
    paddies(L, o, hz);
    let s = "";
    if (o.hut) s += Tk.hut(o.hut.x, o.hut.y, o.hut.s || 1, o.hut);
    if (o.buf) s += `<path d="M${o.buf.stake[0]},${o.buf.stake[1]}v-50" stroke="${INK}" stroke-width="12"/><path d="M${o.buf.stake[0]},${o.buf.stake[1]}v-50" stroke="#8a6a4a" stroke-width="7"/>` + Tk.buffalo(o.buf.x, o.buf.y, o.buf.s || 1, { ...o.buf, rope: [(o.buf.stake[0] - o.buf.x) * (o.buf.flip ? -1 : 1), o.buf.stake[1] - 40 - o.buf.y] });
    if (o.tree) s += Tk.tree(o.tree.x, o.tree.y, o.tree.s || 1, { storm: S, ...o.tree });
    put(L.set, s);
    if (o.dog) put(L.act || L.set, Tk.dog(o.dog.x, o.dog.y, o.dog.s || 1, o.dog));
    if (o.fgRice) { const r = mk(55); let f = ""; for (let k = 0; k < 14; k++) { const x = -100 + k * 95 + r() * 40, h = 220 + r() * 160; f += `<path d="M${f1(x)},2000q-20,-${f1(h * 0.6)} -50,-${f1(h)}M${f1(x + 10)},2000q10,-${f1(h * 0.7)} 30,-${f1(h * 1.05)}M${f1(x + 20)},2000q30,-${f1(h * 0.5)} 70,-${f1(h * 0.9)}" stroke="${S ? "#2e4a2a" : "#5a9a3a"}" stroke-width="16" fill="none" stroke-linecap="round"/>`; } put(L.fg, `<g opacity=".95">${f}</g>`); }
    // the strike
    if (o.bolt && o.tree) {
      const t = o.tree, ts = t.s || 1, topX = t.x - 20 * ts, topY = t.y - 1250 * ts;
      put(L.glow, `<g opacity="${f1(o.bolt)}"><circle cx="${topX}" cy="${topY}" r="${f1(500 * ts)}" fill="url(#tkBoltG)"/>${Tk.bolt(topX + 120, -700, topX, topY, 7, 1.2)}
        <path d="M${t.x + 10 * ts},${t.y - 840 * ts}L${t.x - 20 * ts},${t.y - 640 * ts}L${t.x + 20 * ts},${t.y - 500 * ts}L${t.x - 10 * ts},${t.y - 300 * ts}L${t.x + 16 * ts},${t.y - 120 * ts}" stroke="#ffffff" stroke-width="${f1(10 * ts)}" fill="none"/>
        ${(o.side || []).map(([sx, sy], k) => arc(t.x + (sx > t.x ? 110 : -110) * ts, t.y - 360 * ts, sx, sy, 90 + k)).join("")}
        ${o.ground ? [1, 2, 3].map((k) => `<ellipse cx="${t.x}" cy="${t.y}" rx="${f1(k * 220 * ts)}" ry="${f1(k * 50 * ts)}" fill="none" stroke="#cfe0ff" stroke-width="${f1(8 - k * 2)}" opacity="${f1(0.7 - k * 0.18)}"/>`).join("") : ""}</g>`);
    }
    rain(L, o);
  };

  // under the hut roof looking out across the paddies at the tree
  Sets.tkHut = function (L, o = {}) {
    Sets.tkField(L, { ...o, hut: null, bund: false });
    let f = `<path d="M-900,-800H2000V260L1300,180Q540,120 -220,180L-900,260Z" fill="#a8803e" ${OUT(6)}/>`;
    for (let k = 0; k < 40; k++) f += `<path d="M${-900 + k * 75},${200 - Math.abs(k - 19) * 2}l${-8},${80}" stroke="#7a5a2a" stroke-width="7"/>`;
    f += `<path d="M-900,240Q540,140 2000,240" stroke="#6a4a22" stroke-width="20" fill="none"/>`;
    f += `<rect x="-120" y="140" width="70" height="2000" fill="#5a4030" ${OUT(5)}/><rect x="1130" y="140" width="70" height="2000" fill="#5a4030" ${OUT(5)}/>`;
    f += `<rect x="-900" y="1640" width="2900" height="60" fill="#7a5a3a" ${OUT(5)}/><rect x="-900" y="1700" width="2900" height="500" fill="#5a4030"/>${Array.from({ length: 14 }, (_, k) => `<path d="M${-900 + k * 220},1700v500" stroke="#3a2a1e" stroke-width="6"/>`).join("")}`;
    put(L.fg, f);
  };

  // top-down on the bund: the man on his back, rain, the rescuer's stacked hands, the phone with 1669 on the grass
  Sets.tkCPR = function (L, o = {}) {
    const r = mk(o.seed || 61), X = 540, sk = "#b0805a";
    put(L.sky, `<rect x="-900" y="-800" width="2900" height="3600" fill="#4a5a3a"/>`);
    let m = `<rect x="-900" y="-800" width="2900" height="3600" fill="url(#tkMud)"/>`;
    m += `<path d="M-900,-800H120Q60,960 140,2800H-900Z" fill="#3a4a3a"/><path d="M2000,-800H960Q1020,960 940,2800H2000Z" fill="#3a4a3a"/>`;
    for (let k = 0; k < 160; k++) { const left = r() < 0.5, x = left ? -200 + r() * 300 : 980 + r() * 300, y = -200 + r() * 2400; m += `<path d="M${f1(x)},${f1(y)}l${f1(-10 + r() * 20)},-26M${f1(x + 8)},${f1(y)}l${f1(6 + r() * 10)},-30" stroke="#6a9a4a" stroke-width="5" opacity=".8"/>`; }
    for (let k = 0; k < 40; k++) m += `<ellipse cx="${f1(160 + r() * 760)}" cy="${f1(r() * 2000)}" rx="${f1(14 + r() * 30)}" ry="${f1(8 + r() * 14)}" fill="#8a9aaa" opacity=".35"/>`;
    put(L.mid, m);
    // his body: floral shirt, khaki shorts, bare feet; head at top; the headband ผ้าขาวม้า
    let b = `<g transform="rotate(-4 ${X} 1100)">
      ${[-1, 1].map((sd) => `<path d="M${X + sd * 70},1380L${X + sd * 90},1840" stroke="${INK}" stroke-width="96" stroke-linecap="round"/><path d="M${X + sd * 70},1380L${X + sd * 90},1840" stroke="${sk}" stroke-width="84" stroke-linecap="round"/><path d="M${X + sd * 60},1370L${X + sd * 76},1560" stroke="${INK}" stroke-width="112"/><path d="M${X + sd * 60},1370L${X + sd * 76},1560" stroke="#a8946a" stroke-width="100"/>`).join("")}
      ${[-1, 1].map((sd) => `<path d="M${X + sd * 150},880L${X + sd * 220},1320" stroke="${INK}" stroke-width="72" stroke-linecap="round"/><path d="M${X + sd * 150},880L${X + sd * 220},1320" stroke="${sk}" stroke-width="60" stroke-linecap="round"/>`).join("")}
      <path d="M${X - 160},860Q${X},820 ${X + 160},860L${X + 130},1400H${X - 130}Z" fill="#d8582a" ${OUT(5)}/>
      ${Array.from({ length: 12 }, () => { const fx = X - 110 + r() * 220, fy = 900 + r() * 460; return `<g transform="translate(${f1(fx)},${f1(fy)})">${[0, 72, 144, 216, 288].map((a) => `<ellipse rx="14" ry="7" fill="#f2c230" transform="rotate(${a}) translate(12,0)"/>`).join("")}<circle r="6" fill="#fff"/></g>`; }).join("")}
      <rect x="${X - 34}" y="790" width="68" height="70" fill="${sk}" ${OUT(4)}/>
      <ellipse cx="${X}" cy="690" rx="120" ry="130" fill="${sk}" ${OUT(5)}/><path d="M${X - 122},640Q${X},560 ${X + 122},640L${X + 120},600Q${X},520 ${X - 120},600Z" fill="#e8e4d8" ${OUT(4)}/><path d="M${X - 122},630Q${X},556 ${X + 122},630" stroke="#c83a2a" stroke-width="10" fill="none" stroke-dasharray="16 12"/>
      <path d="M${X - 64},690q22,10 44,0M${X + 20},690q22,10 44,0" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M${X - 30},760q30,10 60,0" stroke="#3a2a22" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M${X - 90},620l10,24" stroke="#5a4a40" stroke-width="5"/></g>`;
    // the rescuer's hands, stacked mid-chest, arms coming from the left (her pink long sleeves)
    const hand = (x, y, rot) => `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M-300,-34H-60V34H-300Z" fill="#e86a8a" ${OUT(4)}/><path d="M-70,-30H-50V30H-70Z" fill="#fff"/><ellipse cx="0" cy="0" rx="72" ry="56" fill="#d8a47a" ${OUT(4)}/>${[-32, -11, 10, 31].map((fy) => `<path d="M44,${fy}h44" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="M44,${fy}h44" stroke="#d8a47a" stroke-width="15" stroke-linecap="round"/>`).join("")}<path d="M-10,-50q30,-20 50,0" stroke="${INK}" stroke-width="20" stroke-linecap="round" fill="none"/><path d="M-10,-50q30,-20 50,0" stroke="#d8a47a" stroke-width="13" stroke-linecap="round" fill="none"/></g>`;
    if (o.hands) b += `<g>${hand(X - 20, 1080, -4)}${hand(X - 6, 1064, -12)}<circle cx="${X}" cy="1076" r="150" fill="none" stroke="#fff2b0" stroke-width="6" opacity=".35"/></g>`;
    // the phone on the grass, speaker on, 1669 calling
    if (o.phone) b += `<g transform="translate(900,560) rotate(14)"><rect x="-70" y="-130" width="140" height="260" rx="22" fill="#1e1e24" ${OUT(4)}/><rect x="-58" y="-112" width="116" height="220" rx="10" fill="#2a6a4a"/><text x="0" y="-40" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="40" fill="#fff">1669</text><circle cx="0" cy="40" r="26" fill="#3ad06a"/><path d="M-10,30q10,20 20,20" stroke="#fff" stroke-width="6" fill="none"/>${[1, 2, 3].map((k) => `<path d="M${50 + k * 16},-20q10,20 0,40" stroke="#f2f0ea" stroke-width="5" fill="none" opacity="${f1(1 - k * 0.25)}"/>`).join("")}</g>`;
    put(L.set, b);
    rain(L, { rain: o.rain ?? 0.6 });
  };

  // ---------------------------------------------------------------- cast
  const { LINE } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const base = (k) => (C[k] && C[k].v2) || {};
  // พลอย: a long braid over the shoulder, side fringe, pink long-sleeve farm shirt, jeans rolled to the knee, bare feet in the mud
  const fringe = (h) => `<path d="M-56,-520C-66,-604 -30,-632 4,-632C40,-631 68,-604 58,-520Q50,-560 30,-574Q-6,-560 -40,-574Q-50,-556 -56,-520Z" fill="${h.c}" ${ln()}/><path d="M-30,-606Q4,-620 40,-600" stroke="${h.sh}" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>`;
  const braid = (h) => `<g>${Array.from({ length: 7 }, (_, k) => `<ellipse cx="${f1(52 + k * 2)}" cy="${-560 + k * 26}" rx="15" ry="17" fill="${h.c}" ${ln(2)}/>`).join("")}<circle cx="64" cy="-372" r="8" fill="#e83a6a" ${ln(2)}/></g>`;
  C.ploy = { v2: { ...base("june"), hair: { c: "#1a120e", s: "#000", sh: "#6a5a50", front: (x) => fringe(x.hair), back: (x) => braid(x.hair) }, top: { kind: "shirt", c: "#e86a8a", sleeve: "long", neck: "collar", collar: "#d05a7a", button: "#fff" }, print: "", bottom: { kind: "jeans", c: "#3a5a8a" }, feet: { kind: "bare" } } };
  // ยายหอม: งอบ (palm-leaf farmer hat) over a white bun, indigo ม่อฮ่อม shirt, checked sarong
  const ngob = `<g transform="translate(0,26)"><path d="M-120,-588Q0,-700 120,-588Q0,-604 -120,-588Z" fill="#c8a868" ${ln()}/><path d="M-90,-610Q0,-680 90,-610" stroke="#a88a4a" stroke-width="4" fill="none"/><path d="M-60,-630Q0,-676 60,-630" stroke="#a88a4a" stroke-width="4" fill="none"/><path d="M-120,-588Q0,-570 120,-588" stroke="#8a6a3a" stroke-width="5" fill="none"/></g>`;
  C.yaiHom = { v2: { ...base("yaiTide"), faceTop: ngob, top: { kind: "blouse", c: "#2a3a6a", sleeve: "long", trim: "#1e2a4e" }, print: `<path d="M-40,-470V-330" stroke="#e8e4d8" stroke-width="3" stroke-dasharray="6 6" opacity=".6"/>`, bottom: { kind: "sarong", c: "#7a3a2a" }, extra: "" } };
  // ลุงเปี๊ยก: ผ้าขาวม้า tied round the head, loud orange floral shirt, khaki shorts
  const headband = `<g><path d="M-58,-566Q0,-590 58,-566L56,-546Q0,-570 -56,-546Z" fill="#e8e4d8" ${ln()}/><path d="M-56,-556Q0,-580 56,-556" stroke="#c83a2a" stroke-width="7" fill="none" stroke-dasharray="10 8"/><path d="M56,-560l26,-14l-4,30Z" fill="#e8e4d8" ${ln(2)}/></g>`;
  const flowers = `<g>${[[-40, -440], [30, -420], [-20, -380], [40, -360], [-36, -340], [10, -470]].map(([x, y]) => `<g transform="translate(${x},${y})">${[0, 72, 144, 216, 288].map((a) => `<ellipse rx="7" ry="3.6" fill="#f2c230" transform="rotate(${a}) translate(6,0)"/>`).join("")}<circle r="3" fill="#fff"/></g>`).join("")}</g>`;
  C.lungPiak = { v2: { ...base("taJun"), faceTop: headband, top: { kind: "shirt", c: "#d8582a", sleeve: "short", neck: "collar", collar: "#b8481e", button: "#f2e8d8" }, print: flowers, bottom: { kind: "shorts", c: "#a8946a" }, feet: { kind: "bare" }, extra: "" } };
  // ต้น: green tee with a big 9, blue shorts, a slingshot in the back pocket
  C.ton = { v2: { ...base("tang"), top: { kind: "tee", c: "#3a9a5a", sleeve: "short" }, print: `<text x="0" y="-380" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="56" fill="#f2f0ea" opacity=".9">9</text>`, bottom: { kind: "shorts", c: "#2a4a8a" }, feet: { kind: "bare" } } };
})();
