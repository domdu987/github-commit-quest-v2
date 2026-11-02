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
    <filter id="tkSil"><feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0 0.05  0 0 0 1 0"/></filter>
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
  // the hundred-year ตะเคียน: a tall straight trunk on buttress roots, a tiered jagged crown with drooping leaf sprays,
  // old lightning scars (long charred streaks) from the crown to the roots. (x,y) = foot of the trunk. Crown top ≈ y − 1500·s.
  const cluster = (r, cx, cy, rx, ry, n = 26) => { let d = ""; for (let k = 0; k <= n; k++) { const a = Math.PI * 2 * k / n, j = 0.82 + r() * 0.3, tip = k % 2 ? 1.12 : 0.92; const px = cx + Math.cos(a) * rx * j * tip, py = cy + Math.sin(a) * ry * j * tip * (Math.sin(a) > 0 ? 0.7 : 1); d += (k ? "L" : "M") + f1(px) + "," + f1(py); } return d + "Z"; };
  Tk.tree = (x, y, s = 1, o = {}) => {
    const r = mk(o.seed || 77), storm = o.storm;
    const C0 = storm ? "#0e1a12" : "#1e3a20", C1 = storm ? "#1a2e1e" : "#2e5a2e", C2 = storm ? "#2a4430" : "#4a7e3a", C3 = storm ? "#3e5a48" : "#7aae4a", rim = storm ? "#a8b8f0" : "#ffe2a0";
    let g = `<g transform="translate(${x},${y}) scale(${s})">`;
    g += `<ellipse cx="0" cy="12" rx="560" ry="64" fill="#000" opacity=".3"/>`;
    // buttress roots (พูพอน): five thin fins flaring out
    [[-300, 14, -60, -260], [-170, 20, -40, -330], [180, 20, 40, -330], [310, 14, 60, -260], [0, 26, 0, -200]].forEach(([fx, fy, tx, ty]) => {
      g += `<path d="M${tx - 40},${ty}Q${fx * 0.55},${fy - 60} ${fx},${fy}L${fx + (fx < 0 ? 70 : -70)},${fy}Q${fx * 0.3},${fy - 40} ${tx + 40},${ty}Z" fill="${fx < 0 ? "#3a2618" : "#5a3e28"}" ${OUT(5)}/>`;
    });
    // trunk: tall and straight, slight taper, bark furrows
    g += `<path d="M-120,0L-96,-1180Q-60,-1230 0,-1232Q60,-1230 96,-1180L120,0Z" fill="url(#tkBark)" ${OUT(6)}/>`;
    for (let k = 0; k < 14; k++) { const bx = -90 + r() * 180, by = -60 - r() * 1080; g += `<path d="M${f1(bx)},${f1(by)}q${f1(-6 + r() * 12)},-80 ${f1(-4 + r() * 8)},-${f1(120 + r() * 120)}" stroke="#1e140e" stroke-width="5" fill="none" opacity=".75"/>`; }
    // old lightning scars: healed ridges, darker than the bark, pale callus edges (clue 1, visible from EP.1 frame 0)
    if (o.scar !== false) g += Tk.oldScars();
    // the seven-colour cloths + garland
    CLOTH.forEach((c, k) => { const yy = -330 - k * 24; g += `<path d="M-114,${yy}Q0,${yy + 20} 114,${yy}V${yy + 22}Q0,${yy + 42} -114,${yy + 22}Z" fill="${c}" ${OUT(3)}/>`; });
    g += `<path d="M60,-322q30,60 10,150" stroke="#d8302a" stroke-width="16" fill="none"/><path d="M80,-320q40,70 30,160" stroke="#f2c230" stroke-width="12" fill="none"/><path d="M40,-316q10,60 -10,120" stroke="#3aa04a" stroke-width="10" fill="none"/>`;
    g += `<path d="M-112,-170Q0,-110 112,-170" stroke="#f2f0ea" stroke-width="12" fill="none" stroke-dasharray="14 8"/>`;
    // limbs reaching out to the tiers
    const limb = (x0, y0, x1, y1, w) => `<path d="M${x0},${y0}Q${(x0 + x1) / 2},${y1 + 40} ${x1},${y1}" stroke="${INK}" stroke-width="${w + 12}" fill="none" stroke-linecap="round"/><path d="M${x0},${y0}Q${(x0 + x1) / 2},${y1 + 40} ${x1},${y1}" stroke="#4a3222" stroke-width="${w}" fill="none" stroke-linecap="round"/>`;
    g += limb(-40, -1080, -520, -1180, 34) + limb(40, -1060, 540, -1160, 34) + limb(-20, -1200, -300, -1400, 26) + limb(20, -1200, 320, -1420, 26) + limb(0, -1220, 0, -1560, 24);
    // the crown: three tiers of jagged leaf clusters (dark underside, mid, lit top) + drooping sprays
    // the crown: three tiers built from many small scalloped lobes (dark under-layer, mid, lit top), leaf flecks, sprays hanging
    const lobe = (cx, cy, rr, fill, k = 9) => { let d = ""; for (let j = 0; j <= k; j++) { const a0 = Math.PI * 2 * j / k, a1 = Math.PI * 2 * (j + 1) / k, rj = rr * (0.85 + r() * 0.25);
        const x0 = cx + Math.cos(a0) * rr, y0 = cy + Math.sin(a0) * rr * 0.72, x1 = cx + Math.cos(a1) * rr, y1 = cy + Math.sin(a1) * rr * 0.72, am = (a0 + a1) / 2, xm = cx + Math.cos(am) * rj * 1.25, ym = cy + Math.sin(am) * rj * 0.9;
        d += (j ? "" : `M${f1(x0)},${f1(y0)}`) + `Q${f1(xm)},${f1(ym)} ${f1(x1)},${f1(y1)}`; } return `<path d="${d}Z" fill="${fill}"/>`; };
    const tiers = [{ y: -1150, w: 640, n: 18, ry: 230 }, { y: -1380, w: 520, n: 15, ry: 220 }, { y: -1580, w: 340, n: 10, ry: 180 }];
    tiers.forEach((t) => {
      const pts = Array.from({ length: t.n }, (_, k) => { const u = (k + 0.5) / t.n, x = -t.w + 2 * t.w * u + (r() - 0.5) * 40; return [x, t.y - Math.sin(u * Math.PI) * t.ry * 0.45 + (r() - 0.5) * t.ry * 0.4]; });
      pts.forEach(([cx, cy]) => { if (r() < 0.5) { const sx = cx + (r() - 0.5) * 60, len = 30 + r() * 70; g += `<path d="M${f1(sx)},${f1(cy + 60)}q${f1(-8 + r() * 16)},${f1(len * 0.6)} ${f1(-6 + r() * 12)},${f1(len)}" stroke="${C1}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M${f1(sx)},${f1(cy + 60 + len * 0.5)}l-10,8M${f1(sx)},${f1(cy + 60 + len * 0.8)}l10,8" stroke="${C2}" stroke-width="5" stroke-linecap="round"/>`; } });
      g += `<path d="M${-t.w - 40},${t.y + 40}Q0,${t.y + t.ry * 1.1} ${t.w + 40},${t.y + 40}Q${t.w * 0.6},${t.y - t.ry * 0.4} 0,${t.y - t.ry * 0.5}Q${-t.w * 0.6},${t.y - t.ry * 0.4} ${-t.w - 40},${t.y + 40}Z" fill="${C0}"/>`;
      pts.forEach(([cx, cy]) => { g += lobe(cx, cy + 20, 70 + r() * 30, C0); });
      pts.forEach(([cx, cy]) => { g += lobe(cx + (r() - 0.5) * 30, cy - 6, 60 + r() * 26, C1); });
      pts.forEach(([cx, cy]) => { g += lobe(cx + (r() - 0.5) * 30, cy - 36, 38 + r() * 18, C2); });
      pts.filter(() => r() < 0.7).forEach(([cx, cy]) => { g += lobe(cx + (r() - 0.5) * 30, cy - 58, 20 + r() * 12, C3); g += `<path d="M${f1(cx - 40)},${f1(cy - 64)}Q${f1(cx)},${f1(cy - 100)} ${f1(cx + 40)},${f1(cy - 64)}" stroke="${rim}" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>`; });
      for (let k = 0; k < 70; k++) { const lx = -t.w + r() * 2 * t.w, ly = t.y - 70 + r() * 120; g += `<path d="M${f1(lx)},${f1(ly)}q6,-8 14,-4q-4,8 -14,4z" fill="${C3}" opacity=".75"/>`; }
    });
    if (o.shrine !== false) g += Tk.shrine(-300, 10, 0.9);
    // fresh strike: a glowing split down the trunk + smoke + bark chips
    if (o.burnt) {
      const b = f1(o.burnt);
      g += `<path d="M10,-1230L-20,-980L20,-760L-14,-520L18,-300L-4,-60" stroke="#ff7a1a" stroke-width="16" fill="none" opacity="${b}" stroke-linejoin="round"/><path d="M10,-1230L-20,-980L20,-760L-14,-520L18,-300L-4,-60" stroke="#fff2b0" stroke-width="6" fill="none" opacity="${b}"/>`;
      g += [0, 1, 2, 3].map((k) => `<path d="M${-20 + k * 14},${-700 - k * 140}q-30,-60 0,-120t0,-120" stroke="#9aa0a8" stroke-width="${22 - k * 3}" fill="none" opacity="${f1(0.45 * o.burnt)}" stroke-linecap="round"/>`).join("");
    }
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
  // the bolt: a jagged main channel that forks (recursive), a blinding white core, violet-blue glow
  Tk.bolt = (x0, y0, x1, y1, seed = 5, w = 1) => {
    const r = mk(seed), paths = [];
    const walk = (ax, ay, bx, by, depth, width) => {
      const n = Math.max(4, Math.round(Math.hypot(bx - ax, by - ay) / 70)), pts = [[ax, ay]];
      for (let k = 1; k < n; k++) { const t = k / n; pts.push([ax + (bx - ax) * t + (r() - 0.5) * 90 * (1 - t * 0.3), ay + (by - ay) * t + (r() - 0.5) * 30]); }
      pts.push([bx, by]);
      paths.push({ d: "M" + pts.map((p) => p.map(f1).join(",")).join("L"), width, depth });
      if (depth < 3) pts.slice(1, -1).forEach((p, k) => { if (r() < (depth ? 0.25 : 0.35)) { const len = (160 + r() * 260) / (depth + 1), ang = Math.atan2(by - ay, bx - ax) + (r() < 0.5 ? -1 : 1) * (0.5 + r() * 0.6); walk(p[0], p[1], p[0] + Math.cos(ang) * len, p[1] + Math.sin(ang) * len, depth + 1, width * 0.45); } });
    };
    walk(x0, y0, x1, y1, 0, 1);
    const glow = paths.map((p) => `<path d="${p.d}" stroke="#9a7aff" stroke-width="${f1(70 * w * p.width)}" fill="none" opacity=".22" stroke-linejoin="round" stroke-linecap="round"/>`).join("");
    const mid = paths.map((p) => `<path d="${p.d}" stroke="#b8d0ff" stroke-width="${f1(22 * w * p.width)}" fill="none" opacity=".75" stroke-linejoin="round" stroke-linecap="round"/>`).join("");
    const core = paths.map((p) => `<path d="${p.d}" stroke="#ffffff" stroke-width="${f1(8 * w * p.width + 1.5)}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`).join("");
    return `<g>${glow}${mid}${core}</g>`;
  };
  // ground current: branching cracks of light running out over the wet field from (x,y), squashed for perspective
  Tk.ground = (x, y, s = 1, seed = 31, reach = 1) => {
    const r = mk(seed); let g = "";
    const run = (ax, ay, ang, len, depth) => { let px = ax, py = ay, d = `M${f1(px)},${f1(py)}`; const n = 7; for (let k = 0; k < n; k++) { ang += (r() - 0.5) * 0.7; px += Math.cos(ang) * len / n; py += Math.sin(ang) * len / n * 0.32; d += `L${f1(px)},${f1(py)}`; if (depth < 2 && r() < 0.3) run(px, py, ang + (r() < 0.5 ? -0.8 : 0.8), len * 0.45, depth + 1); }
      g += `<path d="${d}" stroke="#a8c0ff" stroke-width="${f1((14 - depth * 4) * s)}" fill="none" opacity=".45" stroke-linecap="round"/><path d="${d}" stroke="#ffffff" stroke-width="${f1((4.5 - depth * 1.2) * s)}" fill="none" stroke-linecap="round"/>`; };
    for (let k = 0; k < 9; k++) run(x, y, Math.PI * 2 * k / 9 + r() * 0.3, (380 + r() * 300) * s * reach, 0);
    return `<g>${g}<ellipse cx="${x}" cy="${y}" rx="${f1(160 * s)}" ry="${f1(46 * s)}" fill="#e8f0ff" opacity=".55"/></g>`;
  };
  // bark chips and sparks flying off the trunk at (x,y)
  Tk.chips = (x, y, s = 1, seed = 17) => { const r = mk(seed); let g = ""; for (let k = 0; k < 22; k++) { const a = -Math.PI + r() * Math.PI * 2, d = (60 + r() * 300) * s, cx = x + Math.cos(a) * d, cy = y + Math.sin(a) * d * 0.8; g += k % 2 ? `<path d="M${f1(cx)},${f1(cy)}l${f1(10 * s)},${f1(-6 * s)}l${f1(6 * s)},${f1(12 * s)}l${f1(-12 * s)},${f1(4 * s)}z" fill="#5a3e28" stroke="${INK}" stroke-width="2" transform="rotate(${f1(r() * 360)} ${f1(cx)} ${f1(cy)})"/>` : `<path d="M${f1(x + Math.cos(a) * d * 0.5)},${f1(y + Math.sin(a) * d * 0.4)}L${f1(cx)},${f1(cy)}" stroke="#ffe08a" stroke-width="${f1(4 * s)}" stroke-linecap="round"/>`; } return `<g>${g}</g>`; };
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
      if (m === "clear" && o.farStorm) c += `<path d="M-900,${hz}Q-700,${hz - 420} -350,${hz - 380}Q-100,${hz - 520} 150,${hz - 360}Q380,${hz - 420} 520,${hz - 160}Q600,${hz - 60} 700,${hz}Z" fill="#3e4054" opacity=".92"/><path d="M-700,${hz - 360}Q-300,${hz - 470} 150,${hz - 380}" stroke="#6a6c80" stroke-width="20" fill="none" opacity=".6"/>${o.farBolt ? `<g opacity=".95">${Tk.bolt(120, hz - 380, 200, hz - 10, 13, 0.5)}<circle cx="140" cy="${hz - 300}" r="160" fill="url(#tkBoltG)" opacity=".6"/></g>` : ""}`;
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
    const k = o.rain ?? 0; if (!k) return; const r = mk(321), lit = (o.flash ?? 0) > 0.6;
    let g = `<g opacity="${f1(0.5 + 0.4 * k)}">`;
    for (let i = 0; i < Math.round(160 * k); i++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, l = 40 + r() * 70; g += `<path d="M${f1(x)},${f1(y)}l${f1(-l * 0.22)},${f1(l)}" stroke="${lit ? "#ffffff" : "#cfd8ea"}" stroke-width="${f1((lit ? 2.6 : 1.6) + r() * 2)}" opacity="${f1((lit ? 0.6 : 0.35) + r() * 0.4)}" stroke-linecap="round"/>`; }
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
      const t = o.tree, ts = t.s || 1, topX = t.x, topY = t.y - 1560 * ts;
      put(L.glow, `<g opacity="${f1(o.bolt)}"><circle cx="${topX}" cy="${topY}" r="${f1(620 * ts)}" fill="url(#tkBoltG)"/>${Tk.bolt(topX + 160, -900, topX, topY, o.boltSeed || 7, 1.3)}
        <path d="M${t.x + 10 * ts},${t.y - 1230 * ts}L${t.x - 20 * ts},${t.y - 980 * ts}L${t.x + 20 * ts},${t.y - 760 * ts}L${t.x - 14 * ts},${t.y - 520 * ts}L${t.x + 18 * ts},${t.y - 300 * ts}L${t.x - 4 * ts},${t.y - 60 * ts}" stroke="#ffffff" stroke-width="${f1(12 * ts)}" fill="none"/>
        ${Tk.chips(t.x, t.y - 900 * ts, ts * 1.2)}${Tk.chips(t.x, t.y - 400 * ts, ts, 23)}
        ${(o.side || []).map(([sx, sy], k) => arc(t.x + (sx > t.x ? 110 : -110) * ts, t.y - 360 * ts, sx, sy, 90 + k)).join("")}
        ${o.ground ? Tk.ground(t.x, t.y, ts, 31, o.ground) : ""}</g>`);
    }
    rain(L, o);
  };

  // under the hut roof looking out across the paddies at the tree
  Sets.tkHut = function (L, o = {}) {
    Sets.tkScape(L, { fgRice: false, ...o, hut: null, bund: null, reflect: false });
    let f = `<path d="M-900,-800H2000V260L1300,180Q540,120 -220,180L-900,260Z" fill="#a8803e" ${OUT(6)}/>`;
    for (let k = 0; k < 40; k++) f += `<path d="M${-900 + k * 75},${200 - Math.abs(k - 19) * 2}l${-8},${80}" stroke="#7a5a2a" stroke-width="7"/>`;
    f += `<path d="M-900,240Q540,140 2000,240" stroke="#6a4a22" stroke-width="20" fill="none"/>`;
    f += `<rect x="-120" y="140" width="70" height="2000" fill="#5a4030" ${OUT(5)}/><rect x="1130" y="140" width="70" height="2000" fill="#5a4030" ${OUT(5)}/>`;
    f += `<rect x="-900" y="1640" width="2900" height="60" fill="#7a5a3a" ${OUT(5)}/><rect x="-900" y="1700" width="2900" height="500" fill="#5a4030"/>${Array.from({ length: 14 }, (_, k) => `<path d="M${-900 + k * 220},1700v500" stroke="#3a2a1e" stroke-width="6"/>`).join("")}`;
    put(L.fg, f);
  };

  // top-down on the bund: ลุงเปี๊ยก on his back, the rain; the rescuer's head and shoulders seen from above at the left, her arms
  // straight down to the stacked hands (drawn by the shot with armSl, o.hands = false here); the phone on the grass (o.phone)
  Sets.tkCPR = function (L, o = {}) {
    const r = mk(o.seed || 61), X = o.X ?? 600, sk = "#b0805a", skD = "#8a5a3a";
    put(L.sky, `<rect x="-900" y="-800" width="2900" height="3600" fill="#4a5a3a"/>`);
    let m = `<rect x="-900" y="-800" width="2900" height="3600" fill="url(#tkMud)"/>`;
    m += `<path d="M-900,-800H40Q-20,960 60,2800H-900Z" fill="#3a5a3a"/><path d="M2000,-800H1060Q1120,960 1040,2800H2000Z" fill="#3a5a3a"/>`;
    for (let k = 0; k < 200; k++) { const left = r() < 0.5, x = left ? -200 + r() * 240 : 1060 + r() * 240, y = -200 + r() * 2400; m += `<path d="M${f1(x)},${f1(y)}l${f1(-10 + r() * 20)},-26M${f1(x + 8)},${f1(y)}l${f1(6 + r() * 10)},-30" stroke="#7aaa4a" stroke-width="5" opacity=".8"/>`; }
    for (let k = 0; k < 50; k++) m += `<ellipse cx="${f1(80 + r() * 960)}" cy="${f1(r() * 2000)}" rx="${f1(14 + r() * 30)}" ry="${f1(8 + r() * 14)}" fill="#8a9aaa" opacity=".3"/>`;
    for (let k = 0; k < 30; k++) m += `<path d="M${f1(100 + r() * 900)},${f1(r() * 2000)}q20,-6 40,0" stroke="#3a3022" stroke-width="5" fill="none" opacity=".5"/>`;
    put(L.mid, m);
    // his body, relaxed: rounded shoulders, arms resting slightly away, legs a little apart, feet turned out
    const limb = (x0, y0, x1, y1, w, c) => `<path d="M${x0},${y0}L${x1},${y1}" stroke="${INK}" stroke-width="${w + 10}" stroke-linecap="round"/><path d="M${x0},${y0}L${x1},${y1}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`;
    let b = `<g transform="rotate(-3 ${X} 1100)"><ellipse cx="${X}" cy="1180" rx="260" ry="760" fill="#000" opacity=".18"/>`;
    b += limb(X - 70, 1390, X - 120, 1640, 84, "#a8946a") + limb(X + 70, 1390, X + 110, 1640, 84, "#a8946a");
    b += limb(X - 120, 1660, X - 150, 1880, 64, sk) + limb(X + 110, 1660, X + 150, 1880, 64, sk);
    b += `<ellipse cx="${X - 180}" cy="1910" rx="30" ry="44" fill="${sk}" ${OUT(4)} transform="rotate(30 ${X - 180} 1910)"/><ellipse cx="${X + 180}" cy="1910" rx="30" ry="44" fill="${sk}" ${OUT(4)} transform="rotate(-30 ${X + 180} 1910)"/>`;
    b += limb(X - 160, 880, X - 230, 1100, 62, "#d8582a") + limb(X - 230, 1100, X - 250, 1320, 54, sk) + limb(X + 160, 880, X + 230, 1100, 62, "#d8582a") + limb(X + 230, 1100, X + 250, 1320, 54, sk);
    b += `<ellipse cx="${X - 256}" cy="1356" rx="34" ry="40" fill="${sk}" ${OUT(4)}/><ellipse cx="${X + 256}" cy="1356" rx="34" ry="40" fill="${sk}" ${OUT(4)}/>`;
    b += `<path d="M${X - 190},880Q${X - 200},840 ${X - 120},826Q${X},810 ${X + 120},826Q${X + 200},840 ${X + 190},880L${X + 150},1420Q${X},1440 ${X - 150},1420Z" fill="#d8582a" ${OUT(5)}/>`;
    b += Array.from({ length: 14 }, () => { const fx = X - 130 + r() * 260, fy = 880 + r() * 500; return `<g transform="translate(${f1(fx)},${f1(fy)})">${[0, 72, 144, 216, 288].map((a) => `<ellipse rx="14" ry="7" fill="#f2c230" transform="rotate(${a}) translate(12,0)"/>`).join("")}<circle r="6" fill="#fff"/></g>`; }).join("");
    b += `<path d="M${X - 50},830Q${X},870 ${X + 50},830" stroke="#a8401e" stroke-width="10" fill="none"/>${[920, 1020, 1120, 1220, 1320].map((yy) => `<circle cx="${X}" cy="${yy}" r="7" fill="#f2e8d8" ${OUT(2)}/>`).join("")}`;
    b += `<rect x="${X - 36}" y="770" width="72" height="70" fill="${sk}" ${OUT(4)}/>`;
    b += `<g><ellipse cx="${X}" cy="680" rx="118" ry="128" fill="${sk}" ${OUT(5)}/><path d="M${X - 116},640Q${X - 110},560 ${X},552Q${X + 110},560 ${X + 116},640Q${X + 60},600 ${X},598Q${X - 60},600 ${X - 116},640Z" fill="#3a3430" ${OUT(3)}/>
      <path d="M${X - 120},612Q${X},570 ${X + 120},612L${X + 118},640Q${X},600 ${X - 118},640Z" fill="#e8e4d8" ${OUT(3)}/><path d="M${X - 120},626Q${X},586 ${X + 120},626" stroke="#c83a2a" stroke-width="8" fill="none" stroke-dasharray="14 10"/>
      <path d="M${X - 66},690q22,9 44,0M${X + 22},690q22,9 44,0" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M${X - 24},730q24,-8 48,0" stroke="#2a2420" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M${X - 36},752q36,14 72,0" stroke="${skD}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M${X - 50},758Q${X},810 ${X + 50},758" fill="#2a1a10" opacity=".14"/></g></g>`;
    // the rescuer from above at his left: her head (braid, parting) and pink shoulders
    if (o.rescuer !== false) b += `<g transform="translate(${X - 330},1080) scale(.85)"><ellipse cx="-30" cy="0" rx="78" ry="200" fill="#e86a8a" stroke="${INK}" stroke-width="5"/><path d="M-30,-190Q10,-196 20,-150M-30,190Q10,196 20,150" stroke="#c04a6a" stroke-width="8" fill="none"/>
      <path d="M-120,10Q-170,30 -200,80Q-230,130 -220,190" stroke="#1a120e" stroke-width="30" fill="none" stroke-linecap="round"/>${Array.from({ length: 6 }, (_, k) => `<path d="M${-128 - k * 16},${20 + k * 26}q10,6 22,-2" stroke="#3a2a22" stroke-width="4" fill="none"/>`).join("")}<circle cx="-220" cy="196" r="10" fill="#e83a6a"/>
      <ellipse cx="40" cy="0" rx="82" ry="72" fill="#1e1410" stroke="${INK}" stroke-width="4"/><path d="M-36,0H110" stroke="#5a463c" stroke-width="5"/><path d="M-20,-46Q40,-60 100,-30M-20,46Q40,60 100,30" stroke="#4a3a30" stroke-width="5" fill="none" opacity=".8"/>
      <path d="M108,-28Q128,0 108,28" stroke="#e0a880" stroke-width="12" fill="none" stroke-linecap="round"/><ellipse cx="20" cy="-30" rx="26" ry="12" fill="#7a6458" opacity=".5"/></g>`;
    if (o.phone) b += `<g transform="translate(940,520) rotate(14)"><rect x="-70" y="-130" width="140" height="260" rx="22" fill="#1e1e24" ${OUT(4)}/><rect x="-58" y="-112" width="116" height="220" rx="10" fill="#2a6a4a"/><text x="0" y="-40" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="40" fill="#fff">1669</text><circle cx="0" cy="40" r="26" fill="#3ad06a"/><path d="M-10,30q10,20 20,20" stroke="#fff" stroke-width="6" fill="none"/>${[1, 2, 3].map((k) => `<path d="M${50 + k * 16},-20q10,20 0,40" stroke="#f2f0ea" stroke-width="5" fill="none" opacity="${f1(1 - k * 0.25)}"/>`).join("")}</g>`;
    put(L.set, b);
    rain(L, { rain: o.rain ?? 0.6 });
  };

  // ---------------------------------------------------------------- in-world cards
  // ยายหอม's rules: three split-bamboo slats tied with rope to the hut post, ink-brushed, rain-dark; drops in on its ropes and swings
  Tk.RULES = [["tree", "ฟ้าคำราม <u>อย่าตามต้นไม้</u>", "ต้นสูงกลางนา ฟ้าผ่าก่อนใคร"], ["touch", "คนโดนฟ้าผ่า <u>ไม่มีไฟค้าง</u>", "รีบจับรีบช่วย อย่ามัวยืนห่าง"], ["wait", "ฟ้าร้องครั้งท้าย <u>นับครึ่งชั่วโมง</u>", "ยังไม่ครบสามสิบ อย่าเพิ่งออกโล่ง"]];
  const icon = (k, x, y, s) => {
    const g = { tree: `<path d="M0,40V-6" stroke="#2a1a0c" stroke-width="10"/><ellipse cy="-24" rx="34" ry="26" fill="#2a1a0c"/><path d="M14,-80l-10,24h12l-12,26" stroke="#ffd84a" stroke-width="7" fill="none" stroke-linejoin="round"/><path d="M-44,-44L44,44M44,-44L-44,44" stroke="#c8281a" stroke-width="9" stroke-linecap="round" opacity=".9"/>`,
      touch: `<path d="M-34,20Q-30,-30 -10,-34Q0,-10 4,-34Q16,-30 14,0L30,-14Q44,-6 26,16Q10,40 -14,40Z" fill="#2a1a0c"/><path d="M-50,-50l10,10M50,-50l-10,10M0,-62v14" stroke="#3a8a3a" stroke-width="7" stroke-linecap="round"/>`,
      wait: `<circle r="40" fill="none" stroke="#2a1a0c" stroke-width="8"/><path d="M0,0V-28M0,0L18,12" stroke="#2a1a0c" stroke-width="8" stroke-linecap="round"/><path d="M0,-40A40,40 0 0 1 0,40" fill="#2a1a0c" opacity=".35"/>` }[k];
    return `<g transform="translate(${x},${y}) scale(${s})"><circle r="56" fill="#efe2bc" stroke="#2a1a0c" stroke-width="5"/>${g}</g>`;
  };
  let rseq = 0;
  Tk.rules = (tl, layer, t0, dur, o = {}) => {
    const id = `tkr${rseq++}`, act = o.active ?? -1, done = o.done || [], Y0 = o.y ?? 260, r = mk(91 + rseq);
    let g = `<path d="M540,-600V${Y0 - 40}" stroke="#6a4a2a" stroke-width="80"/><path d="M540,-600V${Y0 - 40}" stroke="#4a3220" stroke-width="80" stroke-dasharray="6 40" opacity=".5"/>`;
    // header plank
    g += `<g><rect x="190" y="${Y0 - 70}" width="700" height="96" rx="10" fill="#8a6a3e" stroke="#2a1a0c" stroke-width="5"/>${[0, 1, 2, 3].map((k) => `<path d="M206,${Y0 - 50 + k * 20}H874" stroke="#6a4a2a" stroke-width="3" opacity=".6"/>`).join("")}
      <text x="540" y="${Y0}" text-anchor="middle" font-family="Sriracha" font-size="58" fill="#fff6dc" stroke="#2a1a0c" stroke-width="8" paint-order="stroke">${o.title || "กฎของยายหอม"}</text></g>`;
    Tk.RULES.forEach(([ic, a, b], k) => {
      const y = Y0 + 70 + k * 210, st = k === act ? "act" : done.includes(k) ? "done" : "later";
      g += `<g id="${id}-r${k}" opacity="${st === "later" ? 0.42 : 1}">`;
      g += `<path d="M320,${y - 30}L330,${y}M760,${y - 30}L750,${y}" stroke="#c8a870" stroke-width="7"/>`;
      // the bamboo slat: cream split bamboo with nodes, rain-dark streaks
      g += `<rect x="70" y="${y}" width="940" height="180" rx="22" fill="#d8c08a" stroke="#2a1a0c" stroke-width="5"/><rect x="70" y="${y + 6}" width="940" height="26" rx="12" fill="#efe0b0" opacity=".8"/>`;
      g += [300, 640].map((nx) => `<path d="M${nx},${y + 4}V${y + 176}" stroke="#a88a52" stroke-width="10"/><path d="M${nx + 6},${y + 4}V${y + 176}" stroke="#efe0b0" stroke-width="3"/>`).join("");
      for (let j = 0; j < 7; j++) { const sx = 90 + r() * 900; g += `<path d="M${f1(sx)},${y + 8}q${f1(-4 + r() * 8)},60 ${f1(-4 + r() * 8)},${f1(80 + r() * 80)}" stroke="#8a6a3a" stroke-width="${f1(4 + r() * 6)}" opacity=".35" stroke-linecap="round"/>`; }
      if (st === "act") g += `<rect id="${id}-hl" x="70" y="${y}" width="940" height="180" rx="22" fill="#ffd84a" opacity=".28"/>`;
      g += icon(ic, 160, y + 90, 1);
      const hi = (s) => s.replace(/<u>(.*?)<\/u>/g, `<tspan fill="#a8281a">$1</tspan>`);
      g += `<text x="240" y="${y + 78}" font-family="Sriracha" font-size="54" fill="#2a1a0c">${hi(a)}</text><text x="240" y="${y + 148}" font-family="Sriracha" font-size="48" fill="#3a2a14">${b}</text>`;
      if (st === "done") g += `<path id="${id}-tk${k}" d="M930,${y + 70}l22,26l46,-58" stroke="#2a8a3a" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      if (st === "act") g += `<path id="${id}-tick" d="M930,${y + 70}l22,26l46,-58" stroke="#a8281a" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>`;
      g += `</g>`;
    });
    // rain running down the slats
    for (let j = 0; j < 30; j++) g += `<path d="M${f1(80 + r() * 920)},${f1(Y0 + r() * 640)}l-4,40" stroke="#ffffff" stroke-width="3" opacity=".35" stroke-linecap="round"/>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-m"><g id="${id}-sw">${g}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 1 }, t0); tl.set(`#${id}`, { opacity: 0 }, t0 + dur);
    const pv = "540 -600", N = (p) => Math.ceil(dur / p) + 1;
    tl.fromTo(`#${id}-m`, { y: -1500 }, { y: 0, duration: 0.45, ease: "power3.in", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: 5, svgOrigin: pv }, { rotation: 0, svgOrigin: pv, duration: 1.5, ease: "elastic.out(1, 0.3)", immediateRender: false }, t0 + 0.45);
    tl.fromTo(`#${id}-sw`, { rotation: -0.6, svgOrigin: pv }, { rotation: 0.6, svgOrigin: pv, duration: 1.3, repeat: N(1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.95);
    if (act >= 0) {
      tl.fromTo(`#${id}-r${act}`, { scale: 1, svgOrigin: `540 ${Y0 + 160 + act * 210}` }, { scale: 1.06, svgOrigin: `540 ${Y0 + 160 + act * 210}`, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, t0 + 0.7);
      tl.fromTo(`#${id}-hl`, { opacity: 0 }, { opacity: 0.32, duration: 0.3, immediateRender: false }, t0 + 0.7);
      if (o.tickAt != null) tl.fromTo(`#${id}-tick`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + o.tickAt);
    }
    return id;
  };

  // ผ้าพระบฏ: a long painted cloth hung behind the shrine — นางตะเคียน in the tree, mural style (flat earth colours, gold, red ground)
  Tk.cloth = (x, y, s = 1, o = {}) => {
    const r = mk(44); let g = `<g transform="translate(${x},${y}) scale(${s})">`;
    g += `<path d="M-420,-40H420" stroke="#5a3a1e" stroke-width="30" stroke-linecap="round"/><path d="M-380,-40V-120M380,-40V-120" stroke="#c8a870" stroke-width="6"/>`;
    g += `<path d="M-380,-20H380V1520Q300,1560 220,1520Q140,1560 60,1520Q-20,1560 -100,1520Q-180,1560 -260,1520Q-320,1560 -380,1520Z" fill="#8a2a1a" stroke="#2a1a0c" stroke-width="6"/>`;
    g += `<rect x="-340" y="20" width="680" height="1440" fill="#c8a868" stroke="#5a3a1e" stroke-width="5"/>`;
    // mural border: gold lotus band
    for (let k = 0; k < 14; k++) g += `<path d="M${-330 + k * 48},40q24,-30 48,0" fill="#e8c048" stroke="#5a3a1e" stroke-width="3"/>`;
    // painted sky: dark storm band with gold lightning
    g += `<path d="M-340,60H340V420Q200,380 0,430Q-200,380 -340,420Z" fill="#3a3a5a"/><path d="M120,80l-40,120h50l-60,140" stroke="#e8c048" stroke-width="12" fill="none" stroke-linejoin="round"/>`;
    // the tree: trunk with seven-colour cloths, a mural canopy of scalloped leaves
    g += `<path d="M-60,1440V600Q-40,560 0,560Q40,560 60,600V1440Z" fill="#5a3a22" stroke="#2a1a0c" stroke-width="5"/>`;
    CLOTH.forEach((c, k) => { g += `<rect x="-62" y="${980 + k * 18}" width="124" height="16" fill="${c}"/>`; });
    for (let k = 0; k < 26; k++) { const a = Math.PI * (1 + k / 25), rx = 300, cx = Math.cos(a) * rx * (0.6 + r() * 0.4), cy = 560 + Math.sin(a) * 200 * (0.6 + r() * 0.4); g += `<path d="M${f1(cx - 40)},${f1(cy)}q40,-50 80,0q-40,30 -80,0Z" fill="${k % 2 ? "#2a5a2a" : "#3a7a3a"}" stroke="#1a2a12" stroke-width="3"/>`; }
    // นางตะเคียน: long black hair to the roots, green สไบ, white skin, gold crown, one long arm beckoning toward the people
    g += `<g transform="translate(0,700)"><path d="M-70,0Q-120,300 -90,700Q0,760 90,700Q120,300 70,0Z" fill="#14100e"/>
      <path d="M-40,80Q-60,260 -40,420H40Q60,260 40,80Z" fill="#2a8a4a" stroke="#14100e" stroke-width="4"/><path d="M-40,90L40,200" stroke="#e8c048" stroke-width="10"/>
      <ellipse cx="0" cy="20" rx="44" ry="54" fill="#f2e8dc" stroke="#14100e" stroke-width="4"/><path d="M-30,10q10,-6 18,0M12,10q10,-6 18,0" stroke="#14100e" stroke-width="4" fill="none"/><path d="M-8,46q8,4 16,0" stroke="#a8281a" stroke-width="4" fill="none"/>
      <path d="M-34,-30L-20,-80L0,-40L20,-80L34,-30Z" fill="#e8c048" stroke="#14100e" stroke-width="3"/>
      <g id="${o.id || "tkc"}-arm"><path d="M40,120Q160,160 250,300" stroke="#f2e8dc" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M250,300q20,10 30,30M250,300q26,0 40,16" stroke="#f2e8dc" stroke-width="10" stroke-linecap="round"/></g></g>`;
    // tiny painted villagers sheltering under her shade
    [[-230, 1380], [-170, 1400], [190, 1390]].forEach(([px, py], k) => { g += `<g transform="translate(${px},${py})"><circle cy="-70" r="16" fill="#e8c8a0" stroke="#14100e" stroke-width="3"/><path d="M-18,-52L-22,0H22L18,-52Z" fill="${["#c84a2a", "#2a4a8a", "#e8c048"][k]}" stroke="#14100e" stroke-width="3"/></g>`; });
    g += `<path d="M-340,1440H340" stroke="#5a3a1e" stroke-width="6"/>`;
    // age: cracks, water stains, fold lines
    for (let k = 0; k < 10; k++) g += `<path d="M${f1(-330 + r() * 660)},${f1(40 + r() * 1400)}l${f1(-20 + r() * 40)},${f1(30 + r() * 50)}" stroke="#5a3a1e" stroke-width="2" opacity=".4"/>`;
    g += `<path d="M-340,500H340M-340,1000H340" stroke="#5a3a1e" stroke-width="3" opacity=".25"/><ellipse cx="200" cy="1200" rx="120" ry="60" fill="#5a3a1e" opacity=".15"/>`;
    return g + `</g>`;
  };

  // the pickup at the roadside, side view, facing left: hard steel roof, windows up; o.faces [{x,who}] heads behind glass
  Tk.pickup = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})">
    <ellipse cx="0" cy="14" rx="520" ry="34" fill="#000" opacity=".35"/>
    <path d="M-470,-60Q-480,-150 -440,-170L-300,-190L-200,-330Q-180,-350 -150,-350H40Q70,-350 80,-330L110,-200H480Q500,-200 500,-180V-60Z" fill="${o.c || "#c8ccd0"}" stroke="${INK}" stroke-width="6"/>
    <path d="M-180,-320L-110,-200H70L50,-320Z" fill="#2a3a4a" stroke="${INK}" stroke-width="5"/><path d="M-280,-200L-210,-320H-190L-260,-200Z" fill="#2a3a4a" stroke="${INK}" stroke-width="4"/>
    <path d="M-170,-310L-120,-220" stroke="#ffffff" stroke-width="8" opacity=".25"/><path d="M-60,-310L-20,-220" stroke="#ffffff" stroke-width="6" opacity=".2"/>
    ${(o.faces || []).map(([fx, col, hair]) => `<g transform="translate(${fx},-250)"><circle r="34" fill="${col}" opacity=".85"/><path d="M-34,-6Q-30,-44 0,-44Q30,-44 34,-6Q20,-24 0,-26Q-20,-24 -34,-6Z" fill="${hair}" opacity=".9"/></g>`).join("")}
    <path d="M-110,-200V-80M110,-200V-60" stroke="${INK}" stroke-width="4" opacity=".6"/><rect x="-60" y="-170" width="40" height="10" rx="4" fill="${INK}" opacity=".6"/>
    <path d="M120,-196H480V-120H120Z" fill="#9aa0a6" stroke="${INK}" stroke-width="4"/>
    ${[-300, 300].map((wx) => `<circle cx="${wx}" cy="-40" r="88" fill="#1a1a1e" stroke="${INK}" stroke-width="6"/><circle cx="${wx}" cy="-40" r="40" fill="#8a9096" stroke="${INK}" stroke-width="4"/>`).join("")}
    <rect x="-490" y="-140" width="40" height="30" rx="6" fill="#ffe8a0" stroke="${INK}" stroke-width="4"/><rect x="474" y="-150" width="30" height="40" rx="5" fill="#d8302a" stroke="${INK}" stroke-width="4"/>
    ${o.keys ? `<g transform="translate(-30,-150)"><circle r="10" fill="#e8c048" stroke="${INK}" stroke-width="3"/><path d="M0,10v30" stroke="#c8ccd0" stroke-width="5"/></g>` : ""}
    ${o.mud !== false ? `<path d="M-470,-70Q-300,-110 -100,-80Q100,-120 500,-80V-60H-470Z" fill="#6a5a3e" opacity=".55"/>` : ""}</g>`;
  // ต้น's toy stopwatch, close-up: o.mm o.ss on a green LCD
  Tk.watch = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-70,-260H70V260H-70Z" fill="#2a8a4a" stroke="${INK}" stroke-width="6"/>${[-200, -140, 140, 200].map((yy) => `<path d="M-70,${yy}H70" stroke="#1e6a3a" stroke-width="5"/>`).join("")}
    <rect x="-150" y="-140" width="300" height="280" rx="60" fill="#f2c230" stroke="${INK}" stroke-width="7"/><rect x="-110" y="-90" width="220" height="150" rx="16" fill="#a8c890" stroke="${INK}" stroke-width="5"/>
    <text x="0" y="12" text-anchor="middle" font-family="monospace" font-weight="700" font-size="76" fill="#1e2a14">${o.mm || "12"}:${o.ss || "04"}</text><text x="0" y="48" text-anchor="middle" font-family="sans-serif" font-weight="700" font-size="24" fill="#1e2a14">${o.label || "LAP"}</text>
    <circle cx="-160" cy="-60" r="16" fill="#d8302a" stroke="${INK}" stroke-width="4"/><circle cx="160" cy="-60" r="16" fill="#2a6ad0" stroke="${INK}" stroke-width="4"/>
    <path d="M-120,-120L-80,-128" stroke="#fff" stroke-width="8" opacity=".5" stroke-linecap="round"/></g>`;
  // the old black-and-white photo in the shrine: a young farmer in a งอบ, a crack across the glass
  Tk.photo = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-150" y="-200" width="300" height="400" fill="#8a5a2a" stroke="${INK}" stroke-width="7"/><rect x="-120" y="-170" width="240" height="340" fill="#d8d2c4"/>
    <rect x="-120" y="-170" width="240" height="340" fill="#7a7468" opacity=".25"/><path d="M-100,170Q-90,40 0,30Q90,40 100,170Z" fill="#4a4640"/><ellipse cx="0" cy="-30" rx="58" ry="70" fill="#a8a296"/><path d="M-110,-70Q0,-170 110,-70Q0,-96 -110,-70Z" fill="#5a564e"/>
    <path d="M-24,-30q10,-6 18,0M8,-30q10,-6 18,0" stroke="#2a2824" stroke-width="5" fill="none"/><path d="M-16,10q16,8 32,0" stroke="#2a2824" stroke-width="5" fill="none"/>
    <path d="M-120,-120L40,60L120,20" stroke="#ffffff" stroke-width="3" opacity=".6" fill="none"/><path d="M-60,-160L-20,-110" stroke="#fff" stroke-width="10" opacity=".25"/>
    ${[-40, 0, 40].map((dx) => `<g transform="translate(${dx},226)"><path d="M0,0V-30" stroke="#f2f0ea" stroke-width="8"/><ellipse cy="-36" rx="5" ry="9" fill="#ffb84a"/></g>`).join("")}
    <path d="M-150,206H150" stroke="#c83a2a" stroke-width="14"/><path d="M-130,200q30,-24 60,0q30,-24 60,0q30,-24 60,0q30,-24 60,0" stroke="#f2c230" stroke-width="7" fill="none"/></g>`;
  // the ambulance (no brand): white van, red stripe, cross, siren lights (o.lit 0..1)
  Tk.ambulance = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="12" rx="480" ry="30" fill="#000" opacity=".3"/>
    <path d="M-440,-60V-300Q-440,-330 -400,-330H200Q240,-330 270,-290L420,-160Q440,-140 440,-110V-60Z" fill="#f4f4f0" stroke="${INK}" stroke-width="6"/>
    <path d="M220,-300L350,-180H220Z" fill="#2a3a4a" stroke="${INK}" stroke-width="5"/><rect x="-440" y="-170" width="880" height="40" fill="#d8302a"/>
    <g transform="translate(-160,-240)"><rect x="-22" y="-60" width="44" height="120" fill="#d8302a"/><rect x="-60" y="-22" width="120" height="44" fill="#d8302a"/></g>
    <rect x="-100" y="-360" width="200" height="34" rx="8" fill="#2a6ad0" stroke="${INK}" stroke-width="4"/><circle cx="-60" cy="-343" r="${f1(14 + 40 * (o.lit ?? 0))}" fill="#4a8aff" opacity="${f1(0.3 + 0.5 * (o.lit ?? 0))}"/><circle cx="60" cy="-343" r="${f1(14 + 40 * (1 - (o.lit ?? 0)))}" fill="#ff4a3a" opacity="${f1(0.3 + 0.5 * (1 - (o.lit ?? 0)))}"/>
    ${[-260, 280].map((wx) => `<circle cx="${wx}" cy="-40" r="80" fill="#1a1a1e" stroke="${INK}" stroke-width="6"/><circle cx="${wx}" cy="-40" r="36" fill="#8a9096" stroke="${INK}" stroke-width="4"/>`).join("")}
    <text x="-60" y="-80" font-family="sans-serif" font-weight="800" font-size="56" fill="#d8302a">1669</text></g>`;
  // the wet paper note slapped on the truck window: "next time" line in felt-tip
  Tk.note = (x, y, s = 1, lines = []) => `<g transform="translate(${x},${y}) scale(${s}) rotate(-4)"><path d="M-400,-260H400V250Q300,280 200,250Q100,290 0,250Q-100,280 -200,250Q-300,290 -400,250Z" fill="#f2ecd8" stroke="${INK}" stroke-width="6"/>
    <rect x="-80" y="-290" width="160" height="60" fill="#e8d890" opacity=".85" transform="rotate(4)"/>${[-160, -60, 40, 140].map((yy) => `<path d="M-370,${yy}H370" stroke="#a8c0d8" stroke-width="3"/>`).join("")}
    ${lines.map((t, k) => `<text x="0" y="${-110 + k * 110}" text-anchor="middle" font-family="Sriracha" font-size="${k === 0 ? 64 : 76}" fill="${k === lines.length - 1 ? "#a8281a" : "#1e2a4a"}">${t}</text>`).join("")}
    <ellipse cx="200" cy="120" rx="90" ry="50" fill="#a8b0c0" opacity=".25"/><path d="M-300,200l20,40M-100,190l10,50M260,180l12,44" stroke="#a8c0d8" stroke-width="5" opacity=".6" stroke-linecap="round"/></g>`;
  // the strike FX for a shot: the white flash (2–3 frames), the silhouette beat, then the scene relit
  Tk.strikeFX = (tl, L, t, o = {}) => {
    tl.set("#flashw", { opacity: 1 }, t); tl.set("#flashw", { opacity: 0 }, t + 0.05);
    const els = [L.set, L.act, L.mid, L.far].filter(Boolean);
    els.forEach((e) => { tl.set(e, { attr: { filter: "url(#tkSil)" } }, t + 0.05); tl.set(e, { attr: { filter: "none" } }, t + 0.05 + (o.sil ?? 0.12)); });
    tl.set("#flashw", { opacity: 0.55 }, t + 0.05 + (o.sil ?? 0.12)); tl.to("#flashw", { opacity: 0, duration: 0.35 }, t + 0.08 + (o.sil ?? 0.12));
  };
  // ================================================================ film look (2 พ.ย. owner: "ทำภาพสวยๆหน่อยสิ")
  // Sets.tkScape(L, o): the rice field at three times of day, painted for depth —
  //   o.mood "gold" (late-afternoon gold, a black storm wall swallowing the sky from the left) | "storm" (teal → indigo, rain curtains) | "clear" (after rain: blue, low gold, rainbow)
  //   sky → far treeline layers with sugar palms, a village and a wat chedi in haze, mist bands → paddies (mirror water reflecting the sky,
  //   rice bands with wind waves, bunds) → the tree on its island with its reflection → fg blurred rice blades → rain in three depths
  //   o.horizon · o.tree {x,y,s} · o.buf · o.hut · o.bund (x of the bund running at the camera) · o.rain 0..1 · o.wind 0..1 · o.flash · o.bolt (temp FX) · o.ripples
  Sets.DEFS += `
    <linearGradient id="skGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a6a"/><stop offset=".45" stop-color="#d89a5a"/><stop offset=".8" stop-color="#ffd890"/><stop offset="1" stop-color="#fff0c0"/></linearGradient>
    <linearGradient id="skStorm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a121c"/><stop offset=".45" stop-color="#1c3442"/><stop offset=".85" stop-color="#3e6670"/><stop offset="1" stop-color="#6a8e8e"/></linearGradient>
    <linearGradient id="skClear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a6ab8"/><stop offset=".55" stop-color="#8cc0e4"/><stop offset=".9" stop-color="#f2e2b8"/><stop offset="1" stop-color="#ffe2a0"/></linearGradient>
    <linearGradient id="wGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0c0"/><stop offset=".5" stop-color="#e8a868"/><stop offset="1" stop-color="#5a5a6a"/></linearGradient>
    <linearGradient id="wStorm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a8e8e"/><stop offset=".5" stop-color="#2e4e58"/><stop offset="1" stop-color="#0e1a22"/></linearGradient>
    <linearGradient id="wClear" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe8b0"/><stop offset=".4" stop-color="#a8d0e8"/><stop offset="1" stop-color="#3a7ac0"/></linearGradient>
    <linearGradient id="stWall" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121a24"/><stop offset=".7" stop-color="#1e2a36"/><stop offset="1" stop-color="#2e3a44"/></linearGradient>
    <linearGradient id="rCurtain" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8aa8b0" stop-opacity="0"/><stop offset=".3" stop-color="#8aa8b0" stop-opacity=".45"/><stop offset="1" stop-color="#8aa8b0" stop-opacity=".15"/></linearGradient>
    <linearGradient id="mistB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset=".5" stop-color="#ffffff" stop-opacity=".9"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
    <radialGradient id="sunG"><stop offset="0" stop-color="#fff6d0"/><stop offset=".15" stop-color="#ffe8a0" stop-opacity=".9"/><stop offset=".5" stop-color="#ffc870" stop-opacity=".3"/><stop offset="1" stop-color="#ffb050" stop-opacity="0"/></radialGradient>
    <linearGradient id="rayG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c0" stop-opacity=".5"/><stop offset="1" stop-color="#fff2c0" stop-opacity="0"/></linearGradient>
    <filter id="skBlur4"><feGaussianBlur stdDeviation="4"/></filter><filter id="skBlur10"><feGaussianBlur stdDeviation="10"/></filter><filter id="skBlur24"><feGaussianBlur stdDeviation="24"/></filter>`;
  const PAL = {
    gold: { sky: "skGold", water: "wGold", far1: "#7a6a6a", far2: "#4a4048", far3: "#2a2630", mist: "#ffe0b0", rice: ["#4a6a2a", "#7a9a3a", "#c8c060"], bund: ["#6a4a2a", "#a8805a"], rain: "#e8e0d0" },
    storm: { sky: "skStorm", water: "wStorm", far1: "#3a5660", far2: "#22363e", far3: "#121e24", mist: "#9ab8bc", rice: ["#18301e", "#2e5034", "#5a8a5a"], bund: ["#2a2620", "#4a443a"], rain: "#c8dce4" },
    clear: { sky: "skClear", water: "wClear", far1: "#7aa0a8", far2: "#4a7468", far3: "#2a4a3a", mist: "#ffffff", rice: ["#2e6a2a", "#5aa03a", "#b8e070"], bund: ["#6a5032", "#a88a5a"], rain: "#ffffff" },
  };
  const clouds = (r, n, x0, x1, y0, y1, s0, s1, fill, rim, rimSide = 1, op = 1) => { let g = ""; for (let k = 0; k < n; k++) { const cx = x0 + r() * (x1 - x0), cy = y0 + r() * (y1 - y0), s = s0 + r() * (s1 - s0);
      g += `<g opacity="${f1(op)}">${[0, 1, 2, 3, 4].map((j) => { const ex = cx + (j - 2) * s * 0.55 + (r() - 0.5) * s * 0.3, ey = cy - Math.sin(j / 4 * Math.PI) * s * 0.45, er = s * (0.45 + r() * 0.35); return `<ellipse cx="${f1(ex)}" cy="${f1(ey)}" rx="${f1(er)}" ry="${f1(er * 0.78)}" fill="${fill}"/>${rim ? `<path d="M${f1(ex - er * 0.2 * rimSide)},${f1(ey - er * 0.75)}A${f1(er)},${f1(er * 0.78)} 0 0 ${rimSide > 0 ? 1 : 0} ${f1(ex + er * 0.95 * rimSide)},${f1(ey + er * 0.1)}" stroke="${rim}" stroke-width="${f1(er * 0.08)}" fill="none" opacity=".75"/>` : ""}`; }).join("")}<ellipse cx="${f1(cx)}" cy="${f1(cy + s * 0.15)}" rx="${f1(s * 1.5)}" ry="${f1(s * 0.32)}" fill="${fill}"/></g>`; } return g; };
  const palm = (x, y, s, c) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-4,0Q-8,-160 0,-300" stroke="${c}" stroke-width="10" fill="none"/>${Array.from({ length: 11 }, (_, k) => { const a = -Math.PI + k * Math.PI / 10; return `<path d="M0,-300q${f1(Math.cos(a) * 40)},${f1(Math.sin(a) * 30 - 10)} ${f1(Math.cos(a) * 80)},${f1(Math.sin(a) * 50 + 20)}" stroke="${c}" stroke-width="7" fill="none"/>`; }).join("")}<circle cy="-300" r="26" fill="${c}"/></g>`;
  const chedi = (x, y, s, c) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-60,0V-40H-40V-80Q-40,-130 0,-150Q40,-130 40,-80V-40H60V0Z" fill="${c}"/><path d="M-10,-150L0,-300L10,-150Z" fill="${c}"/><path d="M-26,-180H26M-20,-200H20M-14,-220H14" stroke="${c}" stroke-width="8"/></g>`;
  Sets.tkScape = function (L, o = {}) {
    const m = o.mood || "storm", P = PAL[m], hz = o.horizon ?? 1000, r = mk(o.seed || 17), wind = o.wind ?? (m === "storm" ? 1 : 0.3);
    // ---- sky
    let s = `<rect x="-1400" y="-1200" width="3900" height="${hz + 1300}" fill="url(#${P.sky})"/>`;
    if (m === "gold") {
      s += `<circle cx="${o.sunX ?? 860}" cy="${hz - 260}" r="520" fill="url(#sunG)"/>`;
      for (let k = 0; k < 7; k++) { const a = -0.9 - k * 0.12; s += `<path d="M${o.sunX ?? 860},${hz - 260}L${f1((o.sunX ?? 860) + Math.cos(a) * 2400 - 60)},${f1(hz - 260 + Math.sin(a) * 2400)}L${f1((o.sunX ?? 860) + Math.cos(a) * 2400 + 60)},${f1(hz - 260 + Math.sin(a) * 2400)}Z" fill="url(#rayG)" opacity=".35"/>`; }
      // the storm wall from the left: an anvil, its towering face, gold rim light on its sunward edges, rain shafts below
      s += `<path d="M-1400,-1200H${o.wallX ?? 520}Q${(o.wallX ?? 520) + 200},-600 ${(o.wallX ?? 520) - 80},-200Q${(o.wallX ?? 520) + 160},150 ${(o.wallX ?? 520) - 40},${hz - 380}Q${(o.wallX ?? 520) + 120},${hz - 200} ${(o.wallX ?? 520) - 200},${hz - 120}L-1400,${hz - 60}Z" fill="url(#stWall)"/>`;
      s += clouds(r, 9, -800, (o.wallX ?? 520) - 40, -500, hz - 300, 160, 300, "#1e2a36", "#ffcf80", 1, 1);
      for (let k = 0; k < 9; k++) { const x = -900 + k * 150 + r() * 60; s += `<path d="M${f1(x)},${hz - 220}L${f1(x - 60 + r() * 30)},${hz}L${f1(x + 50)},${hz}L${f1(x + 90)},${hz - 220}Z" fill="url(#rCurtain)" opacity=".7"/>`; }
      s += clouds(r, 4, (o.wallX ?? 520) + 100, 1600, 80, 400, 70, 120, "#f4d0a0", "#fff6d8", -1, 0.55);
    } else if (m === "storm") {
      s += clouds(r, 14, -900, 2000, -300, hz - 450, 160, 320, "#162430", "#4e6a76", 1, 1);
      s += clouds(r, 10, -900, 2000, hz - 520, hz - 260, 120, 220, "#22384a", "#6a8a94", 1, 0.9);
      // rain curtains: grey-teal shafts sweeping from the cloud base to the horizon
      for (let k = 0; k < 14; k++) { const x = -1000 + k * 230 + r() * 120, w = 80 + r() * 160; s += `<path d="M${f1(x)},${hz - 420}L${f1(x - 90)},${hz + 10}L${f1(x - 90 + w)},${hz + 10}L${f1(x + w)},${hz - 420}Z" fill="url(#rCurtain)" opacity="${f1(0.5 + r() * 0.4)}"/>`; }
      if (o.flash) s += `<rect x="-1400" y="-1200" width="3900" height="${hz + 1300}" fill="#dfe8ff" opacity="${f1(o.flash * 0.45)}"/><ellipse cx="${o.flashX ?? 700}" cy="${hz - 500}" rx="900" ry="500" fill="#eef4ff" opacity="${f1(o.flash * 0.5)}" filter="url(#skBlur24)"/>`;
      if (o.distBolt) s += `<g opacity=".9">${Tk.bolt(o.distBolt[0], hz - 520, o.distBolt[1], hz - 10, 41, 0.5)}</g>`;
    } else {
      s += `<circle cx="${o.sunX ?? 180}" cy="${hz - 180}" r="420" fill="url(#sunG)" opacity=".9"/>`;
      s += clouds(r, 6, -600, 1800, 100, hz - 500, 80, 150, "#ffffff", "#ffe8c0", -1, 0.85);
      const RB = ["#ff5a5a", "#ffa040", "#ffe060", "#60d070", "#4aa0ff", "#5a6aff", "#a060e0"];
      s += `<g opacity=".42" filter="url(#skBlur4)">${RB.map((c, k) => `<path d="M-500,${hz}A${1200 - k * 26},${1200 - k * 26} 0 0 1 ${1900 - k * 52},${hz}" stroke="${c}" stroke-width="26" fill="none" transform="translate(${k * 26},0)"/>`).join("")}</g>`;
      if (o.farStorm) { const fx = o.farStormX ?? 1500; s += `<g><path d="M${fx - 900},${hz}Q${fx - 800},${hz - 380} ${fx - 450},${hz - 420}Q${fx - 200},${hz - 600} ${fx + 100},${hz - 430}Q${fx + 400},${hz - 520} ${fx + 700},${hz - 300}V${hz}Z" fill="#2a3442"/>${clouds(r, 4, fx - 700, fx + 500, hz - 520, hz - 380, 120, 200, "#2a3442", "#ffd8a0", -1, 1)}<path d="M${fx - 500},${hz - 380}L${fx - 600},${hz}H${fx + 300}L${fx + 260},${hz - 380}Z" fill="url(#rCurtain)" opacity=".6"/>${o.farBolt ? `<g>${Tk.bolt(fx - 120, hz - 440, fx - 60, hz - 6, 13, 0.45)}<ellipse cx="${fx - 100}" cy="${hz - 420}" rx="260" ry="160" fill="#eef4ff" opacity=".45" filter="url(#skBlur24)"/></g>` : ""}</g>`; }
    }
    put(L.sky, s);
    // ---- far: three treeline layers with sugar palms, a village and a chedi, mist between
    let f = "";
    [[P.far1, -80, 0.7], [P.far2, -40, 0.85], [P.far3, -8, 1]].forEach(([c, dy, k], li) => {
      let d = `M-1400,${hz + 10}`; for (let x = -1400; x <= 2600; x += 60) d += `L${x},${f1(hz + dy - 20 - Math.abs(Math.sin(x * 0.011 + li)) * 40 * k - r() * 18)}`; f += `<path d="${d}L2600,${hz + 10}Z" fill="${c}"/>`;
      for (let j = 0; j < 7; j++) f += palm(-1200 + r() * 3600, hz + dy, (0.35 + r() * 0.25) * k, c);
      if (li === 0) f += chedi(o.chediX ?? -260, hz + dy - 10, 0.9, c);
      if (li === 1) for (let j = 0; j < 6; j++) { const x = 1200 + j * 70; f += `<path d="M${x},${hz + dy}V${hz + dy - 30}L${x + 30},${hz + dy - 54}L${x + 60},${hz + dy - 30}V${hz + dy}Z" fill="${c}"/>`; }
      f += `<rect x="-1400" y="${hz + dy - 60}" width="4000" height="70" fill="url(#mistB)" opacity="${m === "storm" ? 0.32 : 0.22}" style="fill:${P.mist}" filter="url(#skBlur10)"/>`;
    });
    put(L.far, f);
    // ---- mid: the paddies — mirror water and rice bands in perspective, wind waves, bunds
    let p = `<rect x="-1400" y="${hz}" width="4000" height="4400" fill="${P.rice[0]}"/>`;
    const rows = 22;
    for (let k = 0; k < rows; k++) {
      const t0 = k / rows, t1 = (k + 1) / rows, y0 = hz + Math.pow(t0, 1.9) * (4200 - hz), y1 = hz + Math.pow(t1, 1.9) * (4200 - hz), h = y1 - y0;
      if (k % 3 === 1) {   // water: the sky in it, a bright horizon streak, ripples when it rains
        p += `<rect x="-1400" y="${f1(y0)}" width="4000" height="${f1(h)}" fill="url(#${P.water})"/>`;
        p += `<path d="M-1400,${f1(y0 + 2)}H2600" stroke="${m === "storm" ? "#9ac0c4" : "#fff4d0"}" stroke-width="${f1(1 + h * 0.06)}" opacity=".6"/>`;
        if (o.rain) for (let j = 0; j < 10 + k * 2; j++) { const rx = -900 + r() * 2900, ry = y0 + r() * h, rr = 4 + t0 * 30; p += `<ellipse cx="${f1(rx)}" cy="${f1(ry)}" rx="${f1(rr)}" ry="${f1(rr * 0.28)}" fill="none" stroke="#e8f4f8" stroke-width="${f1(0.8 + t0 * 2)}" opacity=".5"/>`; }
        for (let j = 0; j < 6 + k; j++) { const x = -1200 + r() * 3600; p += `<path d="M${f1(x)},${f1(y0 + r() * h)}h${f1(30 + t0 * 200)}" stroke="#ffffff" stroke-width="${f1(1 + t0 * 3)}" opacity=".18"/>`; }
      } else if (k % 3 === 2) {   // bund
        p += `<rect x="-1400" y="${f1(y0)}" width="4000" height="${f1(h * 0.55)}" fill="${P.bund[0]}"/><path d="M-1400,${f1(y0 + 1)}H2600" stroke="${P.bund[1]}" stroke-width="${f1(1 + h * 0.05)}"/>`;
        p += `<rect x="-1400" y="${f1(y0 + h * 0.55)}" width="4000" height="${f1(h * 0.45)}" fill="${P.rice[0]}"/>`;
      } else {   // rice: dark base, blades, wind-wave highlight bands
        p += `<rect x="-1400" y="${f1(y0)}" width="4000" height="${f1(h)}" fill="${P.rice[0]}"/>`;
        const step = 6 + 40 * t0; let bl = "";
        for (let x = -1400; x < 2600; x += step) { const lean = wind * (8 + 20 * t0) * (0.6 + 0.4 * Math.sin(x * 0.004 + k)); bl += `M${f1(x + r() * step * 0.5)},${f1(y1)}q${f1(lean * 0.4)},${f1(-h * 0.6)} ${f1(lean)},${f1(-h * 1.15)}`; }
        p += `<path d="${bl}" stroke="${P.rice[1]}" stroke-width="${f1(1 + 4 * t0)}" fill="none" opacity=".9"/>`;
        for (let j = 0; j < 3; j++) { const ph = r() * 6; let d = `M-1400,${f1(y0 + h * 0.3)}`; for (let x = -1400; x <= 2600; x += 100) d += `L${x},${f1(y0 + h * (0.3 + 0.2 * Math.sin(x * 0.006 + ph)))}`; p += `<path d="${d}" stroke="${P.rice[2]}" stroke-width="${f1(2 + h * 0.18)}" fill="none" opacity="${f1(0.18 + 0.12 * wind)}" stroke-linecap="round"/>`; }
      }
    }
    const vx = o.vx ?? 540; for (let k = -6; k <= 6; k++) { if (!k) continue; const bx = vx + k * 520; p += `<path d="M${f1(vx + k * 22)},${hz + 6}L${f1(bx * 3 - vx * 2)},4400" stroke="${P.bund[0]}" stroke-width="${Math.abs(k) < 3 ? 46 : 34}" opacity=".9"/><path d="M${f1(vx + k * 22)},${hz + 6}L${f1(bx * 3 - vx * 2)},4400" stroke="${P.bund[1]}" stroke-width="4" opacity=".7" transform="translate(${k > 0 ? -10 : 10},0)"/>`; }
    if (o.bund != null && o.bund !== false) { const bx = o.bund; p += `<path d="M${bx - 26},${hz + 30}L${bx + 26},${hz + 30}L${bx + 760},4400L${bx - 760},4400Z" fill="${P.bund[0]}"/><path d="M${bx - 26},${hz + 30}L${bx - 760},4400" stroke="${P.bund[1]}" stroke-width="8"/><path d="M${bx + 26},${hz + 30}L${bx + 760},4400" stroke="#000" stroke-width="6" opacity=".25"/>`;
      if (o.rain) for (let j = 0; j < 40; j++) { const t = r(), y = hz + 40 + t * t * 3000, x = bx + (r() - 0.5) * (40 + t * t * 1300); p += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(6 + t * 40)}" ry="${f1((6 + t * 40) * 0.3)}" fill="#c8dce4" opacity=".35"/>`; } }
    put(L.mid, p);
    if (m === "storm") put(L.mid, `<rect x="-1400" y="${hz - 160}" width="4000" height="320" fill="${P.mist}" opacity=".22" filter="url(#skBlur24)"/>`);
    // ---- set: the tree on its island + its reflection, the hut, the buffalo
    let st = "";
    if (o.tree) { const t = o.tree, ts = t.s || 1;
      if (o.reflect !== false) { const pid = `pond${Math.round(t.x)}${Math.round(t.y)}`, py = t.y - 10 * ts, prx = 780 * ts, pry = 130 * ts;
        st += `<defs><clipPath id="${pid}"><ellipse cx="${t.x}" cy="${f1(py + pry)}" rx="${f1(prx)}" ry="${f1(pry)}"/></clipPath></defs><ellipse cx="${t.x}" cy="${f1(py + pry)}" rx="${f1(prx)}" ry="${f1(pry)}" fill="url(#${P.water})"/>`;
        st += `<g clip-path="url(#${pid})"><g opacity="${m === "storm" ? 0.3 : 0.45}" filter="url(#skBlur4)" transform="translate(0,${f1(2 * t.y + 40 * ts)}) scale(1,-1)">${Tk.tree(t.x, t.y, ts, { storm: m === "storm", shrine: false, ...t, burnt: 0 })}</g>${Array.from({ length: 10 }, (_, k) => `<path d="M${f1(t.x - prx + r() * 2 * prx)},${f1(py + 20 + r() * pry * 1.8)}h${f1(60 + r() * 160)}" stroke="#ffffff" stroke-width="3" opacity=".25"/>`).join("")}${o.rain ? Array.from({ length: 30 }, () => { const rx = t.x - prx + r() * 2 * prx, ry = py + 20 + r() * pry * 1.8, rr = 6 + r() * 16; return `<ellipse cx="${f1(rx)}" cy="${f1(ry)}" rx="${f1(rr)}" ry="${f1(rr * 0.3)}" fill="none" stroke="#e8f4f8" stroke-width="2" opacity=".5"/>`; }).join("") : ""}</g>`; }
      st += `<ellipse cx="${t.x}" cy="${t.y + 10 * ts}" rx="${f1(560 * ts)}" ry="${f1(64 * ts)}" fill="${P.bund[0]}"/><path d="M${f1(t.x - 560 * ts)},${t.y + 10 * ts}A${f1(560 * ts)},${f1(64 * ts)} 0 0 0 ${f1(t.x + 560 * ts)},${t.y + 10 * ts}" stroke="${P.bund[1]}" stroke-width="5" fill="none"/>`; }
    if (o.hut) st += Tk.hut(o.hut.x, o.hut.y, o.hut.s || 1, o.hut);
    if (o.buf) st += `<path d="M${o.buf.stake[0]},${o.buf.stake[1]}v-50" stroke="${INK}" stroke-width="12"/><path d="M${o.buf.stake[0]},${o.buf.stake[1]}v-50" stroke="#8a6a4a" stroke-width="7"/>` + Tk.buffalo(o.buf.x, o.buf.y, o.buf.s || 1, { ...o.buf, rope: [(o.buf.stake[0] - o.buf.x) * (o.buf.flip ? -1 : 1), o.buf.stake[1] - 40 - o.buf.y] });
    if (o.tree) { const t = o.tree, ts = t.s || 1; st += `<g class="tkSway">${Tk.tree(t.x, t.y, ts, { storm: m === "storm", ...t })}</g>`;
      // cloths streaming in the wind + incense smoke at the shrine
      st += `<g transform="translate(${t.x},${t.y}) scale(${ts})">${CLOTH.map((c, k) => `<path d="M110,${-322 - k * 24}q${f1(80 + 60 * wind)},${f1(-20 + 30 * Math.sin(k))} ${f1(160 + 140 * wind)},${f1(10 + k * 6)}q${f1(-40)},${f1(14)} ${f1(-160 - 140 * wind)},${f1(-4 - k * 6)}" fill="${c}" stroke="${INK}" stroke-width="2.5" opacity=".95"/>`).join("")}
        ${[0, 1, 2].map((k) => `<path d="M${-300 + k * 14},-170q${f1(20 + wind * 40)},-40 ${f1(10 + wind * 60)},-90t${f1(20 + wind * 80)},-90" stroke="#e8e4dc" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>`).join("")}</g>`; }
    put(L.set, st);
    // ---- fg: big blurred rice blades leaning with the wind
    if (o.fgRice !== false) { let g = ""; for (let k = 0; k < 12; k++) { const x = (k < 6 ? -160 + k * 45 : 900 + (k - 6) * 50) + r() * 30, h = 220 + r() * 300, lean = wind * (60 + r() * 80); g += `<path d="M${f1(x)},2050q${f1(lean * 0.3)},-${f1(h * 0.6)} ${f1(lean)},-${f1(h)}" stroke="${P.rice[k % 2 ? 1 : 0]}" stroke-width="${f1(12 + r() * 10)}" fill="none" stroke-linecap="round"/>`; } put(L.fg, `<g filter="url(#skBlur10)" opacity=".95">${g}</g>`); }
    // ---- rain in three depths (far fine, mid, near big blurred) + temp strike FX
    if (o.rain) { const rk = o.rain, lit = (o.flash ?? 0) > 0.6, c = lit ? "#ffffff" : P.rain; let far = "", mid = "", near = "";
      for (let i = 0; i < 260 * rk; i++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, l = 26 + r() * 30; far += `M${f1(x)},${f1(y)}l${f1(-l * 0.25)},${f1(l)}`; }
      for (let i = 0; i < 110 * rk; i++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, l = 60 + r() * 60; mid += `M${f1(x)},${f1(y)}l${f1(-l * 0.25)},${f1(l)}`; }
      for (let i = 0; i < 26 * rk; i++) { const x = -200 + r() * 1500, y = -200 + r() * 2300, l = 160 + r() * 140; near += `<path d="M${f1(x)},${f1(y)}l${f1(-l * 0.25)},${f1(l)}" stroke="${c}" stroke-width="${f1(5 + r() * 5)}" stroke-linecap="round" opacity=".35"/>`; }
      put(L.light, `<g class="rainF"><path d="${far}" stroke="${c}" stroke-width="1.4" opacity="${lit ? 0.55 : 0.3}"/></g><g class="rainM"><path d="${mid}" stroke="${c}" stroke-width="2.6" opacity="${lit ? 0.7 : 0.42}" stroke-linecap="round"/></g><g class="rainN" filter="url(#skBlur4)">${near}</g>`); }
    if (o.bolt && o.tree) { const t = o.tree, ts = t.s || 1, topX = t.x, topY = t.y - 1560 * ts;
      put(L.glow, `<g><circle cx="${topX}" cy="${topY}" r="${f1(700 * ts)}" fill="url(#tkBoltG)"/>${Tk.bolt(topX + 180, -900, topX, topY, o.boltSeed || 7, 1.4)}
        <path d="M${t.x + 10 * ts},${t.y - 1230 * ts}L${t.x - 20 * ts},${t.y - 980 * ts}L${t.x + 20 * ts},${t.y - 760 * ts}L${t.x - 14 * ts},${t.y - 520 * ts}L${t.x + 18 * ts},${t.y - 300 * ts}L${t.x - 4 * ts},${t.y - 60 * ts}" stroke="#ffffff" stroke-width="${f1(14 * ts)}" fill="none"/>
        ${Tk.chips(t.x, t.y - 900 * ts, ts * 1.3)}${Tk.chips(t.x, t.y - 450 * ts, ts * 1.1, 23)}${o.ground ? Tk.ground(t.x, t.y, ts, 31, o.ground) : ""}
        <ellipse cx="${t.x}" cy="${t.y + 60 * ts}" rx="${f1(700 * ts)}" ry="${f1(120 * ts)}" fill="#dfe8ff" opacity=".35" filter="url(#skBlur24)"/></g>`); }
  };
  // inside the pickup, looking out the side window: the dark cab, the glass with rain running down it (drops refract the light), the field outside
  Tk.cabWindow = (o = {}) => { const r = mk(o.seed || 88); let g = `<path d="M0,0H1080V1920H0Z M70,420Q70,360 130,360H980Q1040,360 1040,420V1300H70Z" fill="#14181c" fill-rule="evenodd"/>`;
    g += `<path d="M70,1300H1040" stroke="#2a3036" stroke-width="30"/><path d="M0,1330H1080V1920H0Z" fill="#1a1e22"/><path d="M0,1420Q540,1360 1080,1420" stroke="#2a3036" stroke-width="12" fill="none"/>`;
    g += `<path d="M0,1500H1080" stroke="#0e1114" stroke-width="80"/><rect x="760" y="1360" width="160" height="40" rx="10" fill="#2a3036"/>`;
    // the glass: rivulets and drops
    let gl = `<rect x="70" y="360" width="970" height="940" fill="#a8c0d0" opacity=".08"/>`;
    for (let k = 0; k < 16; k++) { const x = 100 + r() * 920; let d = `M${f1(x)},${f1(360 + r() * 200)}`; let y = 380; for (let j = 0; j < 8; j++) { y += 60 + r() * 60; d += `L${f1(x + (r() - 0.5) * 16)},${f1(y)}`; } gl += `<path d="${d}" stroke="#e8f4ff" stroke-width="${f1(3 + r() * 4)}" fill="none" opacity=".45" stroke-linecap="round"/>`; }
    for (let k = 0; k < 90; k++) { const x = 90 + r() * 930, y = 380 + r() * 900, rr = 3 + r() * 9; gl += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rr)}" ry="${f1(rr * 1.2)}" fill="#0e1820" opacity=".25"/><circle cx="${f1(x - rr * 0.3)}" cy="${f1(y - rr * 0.4)}" r="${f1(rr * 0.35)}" fill="#ffffff" opacity=".7"/>`; }
    // ต้น's head and shoulder silhouette at the window, his hand on the glass
    g += gl + `<g opacity=".95"><path d="M-40,1300Q-20,980 120,940Q230,920 260,1060Q290,1200 240,1300Z" fill="#0c0e10"/><ellipse cx="170" cy="880" rx="110" ry="125" fill="#0c0e10"/><path d="M80,800q20,-40 40,-10q20,-50 40,-10q20,-40 40,0" stroke="#0c0e10" stroke-width="18" fill="none"/>
      <path d="M200,880Q240,876 250,900" stroke="#4a6070" stroke-width="5" fill="none" opacity=".7"/></g>
      <g transform="translate(330,820) rotate(-10)" opacity=".9"><ellipse rx="50" ry="62" fill="#3a2c24"/>${[-30, -10, 10, 30].map((dx) => `<rect x="${dx - 8}" y="-120" width="16" height="70" rx="8" fill="#3a2c24"/>`).join("")}</g>`;
    return g; };
  // ================================================================ review fixes (2 พ.ย. gate review)
  // ผ้าพระบฏ, Thai mural on old cloth: gold + red ground, a kanok border, นางตะเคียน inside the trunk — pale face, almond eyes, red lips, a ชฎา crown,
  // a green สไบ with gold edging, black hair pouring down the trunk into the roots; mural villagers sheltering under the canopy.
  // ids: #<id>-eyesO (open eyes, opacity 0 → 1), #<id>-arm (the beckoning hand, rotate about its shoulder), #<id>-p0..p3 (the villagers, fade into the hair)
  Tk.cloth = (x, y, s = 1, o = {}) => {
    const r = mk(44), id = o.id || "tkc"; let g = `<g transform="translate(${x},${y}) scale(${s})">`;
    g += `<path d="M-430,-40H430" stroke="#4a2a14" stroke-width="34" stroke-linecap="round"/><circle cx="-430" cy="-40" r="24" fill="#c8a040" stroke="#2a1a0c" stroke-width="4"/><circle cx="430" cy="-40" r="24" fill="#c8a040" stroke="#2a1a0c" stroke-width="4"/>`;
    g += `<path d="M-400,-20H400V1560L340,1600L280,1560L220,1600L160,1560L100,1600L40,1560L-20,1600L-80,1560L-140,1600L-200,1560L-260,1600L-320,1560L-400,1600Z" fill="#7a1e14" stroke="#2a1a0c" stroke-width="6"/>`;
    // kanok border: gold flames on red
    g += `<rect x="-370" y="10" width="740" height="1520" fill="#e8c068" stroke="#5a3a14" stroke-width="5"/>`;
    for (let k = 0; k < 16; k++) { const bx = -350 + k * 46; g += `<path d="M${bx},34q14,-26 24,-6q8,-16 18,0q-10,16 -20,10q-10,10 -22,-4Z" fill="#a8281a" stroke="#5a3a14" stroke-width="2"/>`; g += `<path d="M${bx},1506q14,26 24,6q8,16 18,0q-10,-16 -20,-10q-10,-10 -22,4Z" fill="#a8281a" stroke="#5a3a14" stroke-width="2"/>`; }
    g += `<rect x="-340" y="60" width="680" height="1420" fill="#d8b878" stroke="#5a3a14" stroke-width="4"/>`;
    // night storm in the upper panel, gold lightning, painted clouds (mural swirls)
    g += `<path d="M-340,60H340V470Q160,430 0,470Q-160,430 -340,470Z" fill="#2a2a4a"/>`;
    for (let k = 0; k < 6; k++) { const cx = -280 + k * 110, cy = 120 + (k % 2) * 60; g += `<path d="M${cx},${cy}q30,-40 60,0q30,-30 50,10q-50,30 -110,-10Z" fill="#4a4a6a" stroke="#e8c068" stroke-width="3"/>`; }
    g += `<path d="M130,90l-40,130h50l-70,150" stroke="#f2d070" stroke-width="12" fill="none" stroke-linejoin="round"/>`;
    // the tree: trunk, seven cloths, a mural canopy of scalloped leaves
    g += `<path d="M-120,1480Q-90,1000 -80,640Q-40,600 0,600Q40,600 80,640Q90,1000 120,1480Z" fill="#5a3418" stroke="#2a1a0c" stroke-width="5"/>`;
    CLOTH.forEach((c, k) => { g += `<path d="M-100,${1060 + k * 18}Q0,${1070 + k * 18} 100,${1060 + k * 18}V${1074 + k * 18}Q0,${1084 + k * 18} -100,${1074 + k * 18}Z" fill="${c}"/>`; });
    for (let k = 0; k < 40; k++) { const a = Math.PI * (1.02 + 0.96 * k / 39), rr = 260 + r() * 70, cx = Math.cos(a) * rr * 1.1, cy = 600 + Math.sin(a) * rr * 0.75; g += `<path d="M${f1(cx - 34)},${f1(cy)}q34,-44 68,0q-34,26 -68,0Z" fill="${k % 3 ? "#2a5a2a" : "#3e7a3a"}" stroke="#1a2a12" stroke-width="2.5"/>`; }
    // her hair: pours from the head down the trunk and into the roots (black, with gold-line strands)
    g += `<path d="M-60,700Q-130,1000 -110,1300Q-160,1420 -250,1480H250Q160,1420 110,1300Q130,1000 60,700Z" fill="#120c0a"/>`;
    for (let k = 0; k < 9; k++) { const sx = -90 + k * 22; g += `<path d="M${sx},760Q${sx - 20 + k * 2},1100 ${sx * 2.2},1470" stroke="#3a2a22" stroke-width="3" fill="none"/>`; }
    // her body: green สไบ with gold, pale arms
    g += `<path d="M-56,820Q-80,960 -60,1060H60Q80,960 56,820Z" fill="#2a8a4a" stroke="#14100e" stroke-width="4"/><path d="M-56,840L56,980" stroke="#e8c048" stroke-width="12"/><path d="M-56,1040H60" stroke="#e8c048" stroke-width="8"/>`;
    // the beckoning arm (her left), pivot at the shoulder (50,860)
    g += `<g id="${id}-arm"><path d="M50,860Q150,880 230,980" stroke="#f4ece2" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M50,860Q150,880 230,980" stroke="#14100e" stroke-width="26" fill="none" opacity=".25"/>
      <g transform="translate(232,984) rotate(30)"><ellipse rx="16" ry="12" fill="#f4ece2" stroke="#14100e" stroke-width="3"/>${[-10, -3, 4, 11].map((dx) => `<path d="M${dx},-6q4,-26 -6,-34" stroke="#f4ece2" stroke-width="6" stroke-linecap="round" fill="none"/>`).join("")}</g></g>`;
    // the face: pale, almond eyes (closed lids → open), arched brows, red lips; ชฎา crown
    g += `<g transform="translate(0,770)"><path d="M-44,-10Q-46,46 0,62Q46,46 44,-10Q40,-56 0,-58Q-40,-56 -44,-10Z" fill="#f4ece2" stroke="#14100e" stroke-width="4"/>
      <path d="M-32,-14Q-20,-22 -8,-14M8,-14Q20,-22 32,-14" stroke="#14100e" stroke-width="3" fill="none"/>
      <g id="${id}-eyesC"><path d="M-30,0q10,6 20,0M10,0q10,6 20,0" stroke="#14100e" stroke-width="3.5" fill="none"/></g>
      <g id="${id}-eyesO" opacity="${o.open ? 1 : 0}"><path d="M-31,0Q-20,-9 -9,0Q-20,6 -31,0Z" fill="#fff" stroke="#14100e" stroke-width="2.5"/><circle cx="-19" cy="-1" r="4.5" fill="#14100e"/><path d="M9,0Q20,-9 31,0Q20,6 9,0Z" fill="#fff" stroke="#14100e" stroke-width="2.5"/><circle cx="21" cy="-1" r="4.5" fill="#14100e"/><circle cx="-18" cy="-2" r="1.5" fill="#d8302a"/><circle cx="22" cy="-2" r="1.5" fill="#d8302a"/></g>
      <path d="M-2,8q2,10 -4,14" stroke="#c8a890" stroke-width="2.5" fill="none"/><path d="M-10,32Q0,38 10,32Q0,28 -10,32Z" fill="#b8281a"/>
      <path d="M-46,-40Q-50,-80 -30,-96L-14,-150L0,-210L14,-150L30,-96Q50,-80 46,-40Q0,-64 -46,-40Z" fill="#e8c048" stroke="#5a3a14" stroke-width="4"/>${[-30, -14, 0, 14, 30].map((dx, k) => `<circle cx="${dx}" cy="${-60 - (2 - Math.abs(k - 2)) * 24}" r="5" fill="#a8281a"/>`).join("")}
      <path d="M-46,-40Q-60,-20 -56,20M46,-40Q60,-20 56,20" stroke="#e8c048" stroke-width="6" fill="none"/></g>`;
    // mural villagers sheltering under her shade (the ones she takes fade into the hair)
    [[-260, 1430, "#c84a2a"], [-200, 1450, "#2a4a8a"], [210, 1440, "#e8c048"], [270, 1430, "#3a7a3a"]].forEach(([px, py, c], k) => { g += `<g id="${id}-p${k}" transform="translate(${px},${py})"><circle cy="-74" r="15" fill="#e8c8a0" stroke="#14100e" stroke-width="3"/><path d="M-16,-90Q0,-104 16,-90" stroke="#14100e" stroke-width="6" fill="none"/><path d="M-18,-56L-24,0H24L18,-56Z" fill="${c}" stroke="#14100e" stroke-width="3"/><path d="M-12,0V22M12,0V22" stroke="#14100e" stroke-width="5"/></g>`; });
    // mural ground line, age: cracks, water stains, worn fold lines
    g += `<path d="M-340,1480H340" stroke="#5a3a14" stroke-width="6"/>`;
    for (let k = 0; k < 18; k++) g += `<path d="M${f1(-330 + r() * 660)},${f1(70 + r() * 1400)}l${f1(-20 + r() * 40)},${f1(20 + r() * 50)}l${f1(-10 + r() * 20)},${f1(10 + r() * 30)}" stroke="#4a2a10" stroke-width="2" fill="none" opacity=".45"/>`;
    g += `<path d="M-340,520H340M-340,1000H340" stroke="#5a3a14" stroke-width="3" opacity=".25"/><ellipse cx="220" cy="1250" rx="140" ry="70" fill="#5a3a14" opacity=".14"/><ellipse cx="-240" cy="330" rx="90" ry="50" fill="#5a3a14" opacity=".12"/>`;
    return g + `</g>`;
  };
  // old healed lightning scars (3–4 long dark ridges with paler callus edges) for the trunk, in tree units; drawn by Tk.tree when o.scar
  Tk.oldScars = () => [[18, -1220, 0], [-62, -1150, 1], [70, -1100, 2], [-20, -900, 3]].map(([x0, y0, k]) => { const pts = [[x0, y0]]; let x = x0; for (let j = 1; j < 7; j++) { x += (j % 2 ? -1 : 1) * (10 + k * 3); pts.push([x, y0 + j * (150 - k * 12)]); } const d = "M" + pts.map((p) => p.join(",")).join("L");
    return `<path d="${d}" stroke="#d8c0a0" stroke-width="${26 - k * 3}" fill="none" opacity=".55" stroke-linejoin="round"/><path d="${d}" stroke="#1a0e08" stroke-width="${16 - k * 2}" fill="none" stroke-linejoin="round"/><path d="${d}" stroke="#3a2618" stroke-width="${5}" fill="none" stroke-dasharray="20 14" opacity=".8"/>`; }).join("");
  // the old photo: a young farmer in a งอบ standing under THE SAME tree (its trunk with cloths behind him), black-and-white, a crack in the glass
  Tk.photo = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-160" y="-210" width="320" height="420" fill="#6a4020" stroke="${INK}" stroke-width="8"/><rect x="-130" y="-180" width="260" height="360" fill="#d6d0c2"/>
    <path d="M-130,-180H130V-40Q60,-80 0,-60Q-60,-80 -130,-40Z" fill="#8a867c"/>${[-90, -40, 10, 60, 100].map((cx) => `<ellipse cx="${cx}" cy="-120" rx="44" ry="30" fill="#6a665e"/>`).join("")}
    <path d="M-34,180V-60H34V180Z" fill="#7a7468"/>${[0, 1, 2, 3, 4, 5, 6].map((k) => `<rect x="-34" y="${20 + k * 10}" width="68" height="9" fill="${["#9a948a", "#5a564e", "#8a8478", "#4a4640", "#aaa49a", "#6a665e", "#7a7468"][k]}"/>`).join("")}
    <path d="M-130,150H130V180H-130Z" fill="#8a8478"/>
    <g transform="translate(-70,40)"><path d="M-36,140Q-40,40 0,30Q40,40 36,140Z" fill="#4a4640"/><ellipse cx="0" cy="0" rx="26" ry="30" fill="#b0aa9e"/><path d="M-50,-14Q0,-60 50,-14Q0,-24 -50,-14Z" fill="#5a564e"/>
      <path d="M-10,0q4,-3 8,0M4,0q4,-3 8,0" stroke="#2a2824" stroke-width="3" fill="none"/><path d="M-6,14q6,4 12,0" stroke="#2a2824" stroke-width="3" fill="none"/></g>
    <rect x="-130" y="-180" width="260" height="360" fill="#7a6a50" opacity=".18"/><path d="M-130,-110L30,70L130,40" stroke="#ffffff" stroke-width="3" opacity=".6" fill="none"/><path d="M-80,-170L-30,-110" stroke="#fff" stroke-width="12" opacity=".2"/>
    ${[-40, 0, 40].map((dx) => `<g transform="translate(${dx},236)"><path d="M0,0V-30" stroke="#f2f0ea" stroke-width="8"/><ellipse cy="-36" rx="5" ry="9" fill="#ffb84a"/></g>`).join("")}
    <path d="M-160,216H160" stroke="#c83a2a" stroke-width="14"/><path d="M-140,210q30,-24 60,0q30,-24 60,0q30,-24 60,0q30,-24 60,0" stroke="#f2c230" stroke-width="7" fill="none"/></g>`;
  // small cartoon faces for people seen through a car window: [x, skin, hair, kind] kind: "yai" (งอบ), "ploy" (braid), "ton"
  Tk.winFace = (x, y, s, skin, hair, kind, look = 0) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse rx="40" ry="46" fill="${skin}" stroke="${INK}" stroke-width="3"/>
    ${kind === "yai" ? `<path d="M-74,-30Q0,-110 74,-30Q0,-44 -74,-30Z" fill="#c8a868" stroke="${INK}" stroke-width="3"/>` : kind === "ploy" ? `<path d="M-42,-6C-46,-56 42,-60 42,-6Q30,-30 0,-34Q-30,-30 -42,-6Z" fill="${hair}"/><ellipse cx="${-44 * (look || 1)}" cy="20" rx="12" ry="26" fill="${hair}"/>` : `<path d="M-40,-14C-40,-54 40,-54 40,-14Q20,-30 0,-30Q-20,-30 -40,-14Z" fill="${hair}"/>${[-20, 0, 20].map((dx) => `<path d="M${dx},-44l-4,-14" stroke="${hair}" stroke-width="6"/>`).join("")}`}
    <ellipse cx="${-14 + look * 8}" cy="2" rx="6" ry="8" fill="#fff" stroke="${INK}" stroke-width="2"/><ellipse cx="${14 + look * 8}" cy="2" rx="6" ry="8" fill="#fff" stroke="${INK}" stroke-width="2"/><circle cx="${-14 + look * 10}" cy="3" r="3.5" fill="${INK}"/><circle cx="${14 + look * 10}" cy="3" r="3.5" fill="${INK}"/>
    <ellipse cx="${look * 6}" cy="26" rx="8" ry="${kind === "ton" ? 9 : 5}" fill="#5a1a1a"/></g>`;
  // the ambulance: white, a blue Star of Life (not the Red Cross emblem), 1669, a generic red-and-yellow stripe, light bar
  Tk.ambulance = (x, y, s = 1, o = {}) => { const star = `<g>${[0, 60, 120].map((a) => `<rect x="-14" y="-56" width="28" height="112" rx="4" fill="#2a6ad0" transform="rotate(${a})"/>`).join("")}<path d="M0,-34V36" stroke="#fff" stroke-width="6"/><path d="M-10,-26q20,10 0,20q-20,10 0,20q20,10 0,20" stroke="#fff" stroke-width="4" fill="none"/></g>`;
    return `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="12" rx="480" ry="30" fill="#000" opacity=".3"/>
    <path d="M-440,-60V-300Q-440,-330 -400,-330H200Q240,-330 270,-290L420,-160Q440,-140 440,-110V-60Z" fill="#f4f4f0" stroke="${INK}" stroke-width="6"/>
    <path d="M220,-300L350,-180H220Z" fill="#2a3a4a" stroke="${INK}" stroke-width="5"/><rect x="-440" y="-170" width="880" height="26" fill="#e8402a"/><rect x="-440" y="-144" width="880" height="14" fill="#f2c230"/>
    <g transform="translate(-170,-240)">${star}</g>
    <rect x="-100" y="-360" width="200" height="34" rx="8" fill="#e8e8e8" stroke="${INK}" stroke-width="4"/><circle cx="-60" cy="-343" r="${f1(14 + 40 * (o.lit ?? 0))}" fill="#4a8aff" opacity="${f1(0.3 + 0.5 * (o.lit ?? 0))}"/><circle cx="60" cy="-343" r="${f1(14 + 40 * (1 - (o.lit ?? 0)))}" fill="#ff4a3a" opacity="${f1(0.3 + 0.5 * (1 - (o.lit ?? 0)))}"/>
    ${[-260, 280].map((wx) => `<circle cx="${wx}" cy="-40" r="80" fill="#1a1a1e" stroke="${INK}" stroke-width="6"/><circle cx="${wx}" cy="-40" r="36" fill="#8a9096" stroke="${INK}" stroke-width="4"/>`).join("")}
    <text x="-20" y="-200" font-family="sans-serif" font-weight="800" font-size="60" fill="#2a6ad0">1669</text>${o.open ? `<path d="M-440,-300H-560V-60H-440Z" fill="#e8e8e4" stroke="${INK}" stroke-width="5"/><rect x="-430" y="-290" width="260" height="220" fill="#2a3036"/>` : ""}</g>`; };
  // a stretcher (side view) with a blanket: (x,y) = the middle of the mattress top
  Tk.stretcher = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-300,40H300" stroke="#8a929a" stroke-width="16"/><path d="M-260,40L-280,150M260,40L280,150M-200,40L-180,150M200,40L180,150" stroke="#6a727a" stroke-width="10"/>${[-280, -180, 180, 280].map((wx) => `<circle cx="${wx}" cy="160" r="16" fill="#1a1a1e"/>`).join("")}<rect x="-310" y="0" width="620" height="44" rx="12" fill="#e8ecf0" stroke="${INK}" stroke-width="4"/></g>`;
  // scorched ground at a strike (dark, cracked, with smoke wisps rising)
  Tk.scorch = (x, y, s = 1, smoke = 1) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse rx="260" ry="50" fill="#1a120c" opacity=".75"/><ellipse rx="160" ry="30" fill="#0a0806" opacity=".8"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${-180 + k * 90},-10q-20,-60 0,-120t0,-120" stroke="#b8bcc0" stroke-width="${14 - k}" fill="none" opacity="${f1(0.35 * smoke)}" stroke-linecap="round"/>`).join("")}</g>`;
  // the toy stopwatch, counting (o.label above the digits, o.ring 0..1 progress toward 30:00); returns html; Tk.watchRun animates the digits
  Tk.watch = (x, y, s = 1, o = {}) => `<g transform="translate(${x},${y}) scale(${s})"><path d="M-70,-280H70V280H-70Z" fill="#2a8a4a" stroke="${INK}" stroke-width="6"/>${[-220, -160, 160, 220].map((yy) => `<path d="M-70,${yy}H70" stroke="#1e6a3a" stroke-width="5"/>`).join("")}
    <rect x="-170" y="-170" width="340" height="340" rx="80" fill="#f2c230" stroke="${INK}" stroke-width="7"/>
    ${o.ring != null ? `<circle r="150" fill="none" stroke="#c89a20" stroke-width="16"/><circle id="${o.id}-ring" r="150" fill="none" stroke="#d8302a" stroke-width="16" pathLength="1" stroke-dasharray="${f1(o.ring)} 1" transform="rotate(-90)" stroke-linecap="round"/>` : ""}
    <rect x="-118" y="-84" width="236" height="150" rx="16" fill="#a8c890" stroke="${INK}" stroke-width="5"/>
    <text id="${o.id}-d" x="0" y="20" text-anchor="middle" font-family="monospace" font-weight="700" font-size="78" fill="#1e2a14">${o.mm || "10"}:${o.ss || "00"}</text>
    <text x="0" y="-104" text-anchor="middle" font-family="Sriracha" font-size="${o.labelSize || 30}" fill="#2a1a0c">${o.label || ""}</text>${o.sub ? `<text x="0" y="56" text-anchor="middle" font-family="sans-serif" font-weight="700" font-size="22" fill="#1e2a14">${o.sub}</text>` : ""}
    <circle cx="-180" cy="-60" r="16" fill="#d8302a" stroke="${INK}" stroke-width="4"/><circle cx="180" cy="-60" r="16" fill="#2a6ad0" stroke="${INK}" stroke-width="4"/>
    <path d="M-130,-140L-90,-148" stroke="#fff" stroke-width="8" opacity=".5" stroke-linecap="round"/></g>`;
  Tk.watchRun = (tl, id, t0, dur, from, o = {}) => { const el = () => document.getElementById(`${id}-d`), c = { v: from };
    tl.fromTo(c, { v: from }, { v: from + dur * (o.speed ?? 1), duration: dur, ease: "none", immediateRender: false, onUpdate: () => { const e = el(); if (e) { const v = Math.floor(c.v); e.textContent = `${String(Math.floor(v / 60)).padStart(2, "0")}:${String(v % 60).padStart(2, "0")}`; } } }, t0);
    if (o.ring) tl.fromTo(`#${id}-ring`, { attr: { "stroke-dasharray": `${f1(from / 1800)} 1` } }, { attr: { "stroke-dasharray": `${f1((from + dur * (o.speed ?? 1)) / 1800)} 1` }, duration: dur, ease: "none", immediateRender: false }, t0); };
  // inside the cab, looking out (o.view "side" | "windshield"): dark cab, the glass with rivulets and refracting drops; returns html (screen units)
  Tk.cab = (o = {}) => { const r = mk(o.seed || 88), ws = o.view === "windshield"; let g = "";
    const hole = ws ? "M60,520Q540,430 1020,520L1060,1340Q540,1300 20,1340Z" : "M70,420Q70,360 130,360H980Q1040,360 1040,420V1300H70Z";
    g += `<path d="M0,0H1080V1920H0Z ${hole}" fill="#1a2026" fill-rule="evenodd"/><path d="${hole}" fill="none" stroke="#0a0e12" stroke-width="22"/>`;
    if (ws) g += `<path d="M0,1320Q540,1270 1080,1320V1920H0Z" fill="#20262c"/><path d="M0,1420Q540,1370 1080,1420" stroke="#2e363e" stroke-width="10" fill="none"/><path d="M700,1520a140,140 0 1 1 1,0" fill="none" stroke="#0e1216" stroke-width="30"/><path d="M60,520L20,1340" stroke="#2a3036" stroke-width="40"/><path d="M1020,520L1060,1340" stroke="#2a3036" stroke-width="40"/><path d="M520,520V600" stroke="#0e1216" stroke-width="14"/><rect x="470" y="600" width="100" height="40" rx="8" fill="#0e1216"/>`;
    else g += `<path d="M70,1300H1040" stroke="#2a3036" stroke-width="30"/><path d="M0,1330H1080V1920H0Z" fill="#20262c"/><path d="M0,1420Q540,1360 1080,1420" stroke="#2e363e" stroke-width="12" fill="none"/><rect x="760" y="1360" width="160" height="40" rx="10" fill="#2e363e"/>`;
    let gl = `<path d="${hole}" fill="#a8c0d0" opacity=".07"/>`;
    for (let k = 0; k < 14; k++) { const x = 110 + r() * 860; let d = `M${f1(x)},${f1(400 + r() * 200)}`; let y = 420; for (let j = 0; j < 8; j++) { y += 60 + r() * 60; d += `L${f1(x + (r() - 0.5) * 18)},${f1(y)}`; } gl += `<path d="${d}" stroke="#e8f4ff" stroke-width="${f1(2.5 + r() * 3)}" fill="none" opacity=".3" stroke-linecap="round"/>`; }
    for (let k = 0; k < 110; k++) { const x = 90 + r() * 930, y = 440 + r() * 840, rr = 3 + r() * 9; gl += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rr)}" ry="${f1(rr * 1.2)}" fill="#0e1820" opacity=".22"/><circle cx="${f1(x - rr * 0.3)}" cy="${f1(y - rr * 0.4)}" r="${f1(rr * 0.35)}" fill="#ffffff" opacity=".65"/>`; }
    return { frame: g, glass: gl }; };
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
  C.lungPiak = { v2: { ...base("taJun"), hair: { ...base("taJun").hair, c: "#3a3430", s: "#1e1a18", sh: "#6a625a" }, brow: "#2a2420", face: `<path d="M-40,-528Q0,-486 40,-528Q36,-500 0,-492Q-36,-500 -40,-528Z" fill="#2a1a10" opacity=".16"/><path d="M-20,-531q10,-6 20,-2q10,-4 20,2" stroke="#2a2420" stroke-width="5" fill="none" stroke-linecap="round"/>`, faceTop: headband, top: { kind: "shirt", c: "#d8582a", sleeve: "short", neck: "collar", collar: "#b8481e", button: "#f2e8d8" }, print: flowers, bottom: { kind: "shorts", c: "#a8946a" }, feet: { kind: "bare" }, extra: "" } };
  // ต้น: green tee with a big 9, blue shorts, a slingshot in the back pocket
  const phoneP = `<g transform="translate(0,118) rotate(-10)"><rect x="-13" y="-26" width="26" height="46" rx="5" fill="#2a2a32" ${ln(2)}/><rect x="-10" y="-22" width="20" height="36" rx="2" fill="#3ad06a"/></g>`;
  C.ployPhone = { ...C.ploy, hand: phoneP, keep: "F" };
  C.medic = { v2: { ...base("keng"), top: { kind: "shirt", c: "#2a6ad0", sleeve: "short", neck: "collar", collar: "#1e5ab8", button: "#fff" }, print: `<path d="M-30,-440h20M-20,-450v20" stroke="#fff" stroke-width="6"/>`, bottom: { kind: "jeans", c: "#1e2a4a" }, feet: { kind: "boot", c: "#1a1a1a" }, extra: "" } };
  C.ton = { v2: { ...base("tang"), top: { kind: "tee", c: "#3a9a5a", sleeve: "short" }, print: `<text x="0" y="-380" text-anchor="middle" font-family="sans-serif" font-weight="800" font-size="56" fill="#f2f0ea" opacity=".9">9</text>`, bottom: { kind: "shorts", c: "#2a4a8a" }, feet: { kind: "bare" } } };
})();
