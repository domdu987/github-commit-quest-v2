// ---------- ทางกลับบ้าน · V11 pass (load after war.js): a lit, layered golden-hour world and heavy effects ----------
//   Sets.border(L, o)   golden-hour border field: low sun with a bloom, 4 haze ridges with fog bands between (the 2nd ridge carries
//                       the binocular glint #id-glint: a small 4-point star, no streak), a tree line, a leafy notched tree (o.tree, o.notch),
//                       crossed bamboo (o.bamboo), animal bones (o.bones), sandbags (o.bags), barbed wire (o.wire), layered grass blades
//                       in fg (o.fgH) and a grass band at the actors' feet in L.glow (o.band = [x0, x1, y])
//   Sets.hedge(L, o)    the same field with an earth bank (o.bank), a big tree; the leafy bush is drawn by War.bush (in front of actors)
//   War.bush(layer, x, y, s, id, o)   a bush of many small leaf clusters, 3 tones + lit edges, twigs, gaps you can see through (o.gaps)
//   War.tree(x, G, s, r, o)          a leafy tree: blob canopy of clusters, branches and bark, o.notch draws the X cut in the bark
//   War.blast(tl, L, x, y, t, o)     the mine: 3-frame white-out, dirt fountain jets, clods + grass flung (some past the lens),
//                                    fine dust spray, a ground shockwave, grass bent away, debris raining back, dust drifting past the
//                                    camera · o.world (the shot's world id) → tinnitus: 0.5 s blur + washed colour
//   War.bulletSlow(tl, L, o)         one bullet in slow motion (0.3×) through the bush just over the helmet, leaves bursting along its line,
//                                    twigs snapping, then real-speed bullets · o.y the line, o.x0/o.x1 the slow stretch, o.t
//   War.glint(tl, id, t0, dur, o)    2–3 blinks of the glint (o.at = times into the shot)
//   War.spot(tl, layer, x, y, t0, dur, o)  highlight a sign in the field: rings, a turning dashed ring, sparkles, a label pill with a coin
//   War.sway(tl, root, t0, dur)      every .wrSway group under root sways in the wind (grass, canopies)
//   War.jiggle(tl, aid, t0, dur, o)  the helmet strap and the dog tag of an actor bounce
//   WarUI.tag(...)   the squad's dog tag: notched, embossed letters, a beaded chain, big coins
//   WarUI.cover(...) the cross-section card: a bullet through a bush reaches the man (✗), a bullet stopped by a trunk / bank (✓)
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  let seq = 0; const nid = () => "wy" + (seq++);
  const blob = Pop2.blob;
  Sets.DEFS += `
    <linearGradient id="wySky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f6f98"/><stop offset=".42" stop-color="#9aa6b4"/><stop offset=".72" stop-color="#e2bf96"/><stop offset="1" stop-color="#f6cf8e"/></linearGradient>
    <linearGradient id="wySkyK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e3460"/><stop offset=".45" stop-color="#8a5a72"/><stop offset=".78" stop-color="#e48a5e"/><stop offset="1" stop-color="#f6b46e"/></linearGradient>
    <radialGradient id="wySun"><stop offset="0" stop-color="#fffbe6"/><stop offset=".12" stop-color="#fff1c0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd890" stop-opacity=".35"/><stop offset="1" stop-color="#ffc070" stop-opacity="0"/></radialGradient>
    <linearGradient id="wyHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6e2c4" stop-opacity="0"/><stop offset=".55" stop-color="#f6e2c4" stop-opacity=".55"/><stop offset="1" stop-color="#f6e2c4" stop-opacity="0"/></linearGradient>
    <linearGradient id="wyField" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8b46a"/><stop offset=".35" stop-color="#9aa04e"/><stop offset="1" stop-color="#5e7030"/></linearGradient>
    <linearGradient id="wyGround" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a9a50"/><stop offset=".5" stop-color="#7a8440"/><stop offset="1" stop-color="#4e5a26"/></linearGradient>
    <linearGradient id="wyLeafD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3e6a2c"/><stop offset="1" stop-color="#1e3a1a"/></linearGradient>
    <linearGradient id="wyLeafM" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7aa244"/><stop offset="1" stop-color="#4a7a30"/></linearGradient>
    <linearGradient id="wyLeafL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8e07a"/><stop offset="1" stop-color="#8ab448"/></linearGradient>
    <linearGradient id="wyBark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6644"/><stop offset=".5" stop-color="#5e4430"/><stop offset="1" stop-color="#3a2a1e"/></linearGradient>
    <linearGradient id="wyBag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8c08e"/><stop offset="1" stop-color="#9a8256"/></linearGradient>
    <linearGradient id="wyJet" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#5a4028"/><stop offset=".6" stop-color="#8a6a44"/><stop offset="1" stop-color="#b89a70" stop-opacity=".2"/></linearGradient>
    <radialGradient id="wyPuff"><stop offset="0" stop-color="#c4a87e" stop-opacity=".95"/><stop offset=".55" stop-color="#a8885e" stop-opacity=".7"/><stop offset="1" stop-color="#8a6e4c" stop-opacity="0"/></radialGradient>
    <radialGradient id="wyPuffL"><stop offset="0" stop-color="#e8d4b0" stop-opacity=".8"/><stop offset="1" stop-color="#d8c09a" stop-opacity="0"/></radialGradient>
    <radialGradient id="wyCore"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#fff2c0" stop-opacity=".9"/><stop offset="1" stop-color="#ffc060" stop-opacity="0"/></radialGradient>
    <radialGradient id="wyStar"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#fff8d0" stop-opacity=".7"/><stop offset="1" stop-color="#fff8d0" stop-opacity="0"/></radialGradient>
    <linearGradient id="wyTrail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff6d0" stop-opacity="1"/><stop offset=".25" stop-color="#ffd27a" stop-opacity=".7"/><stop offset="1" stop-color="#ffb040" stop-opacity="0"/></linearGradient>
    <linearGradient id="wyTag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f4f6"/><stop offset=".3" stop-color="#c2c8ce"/><stop offset=".55" stop-color="#e8ebee"/><stop offset=".8" stop-color="#a8b0b8"/><stop offset="1" stop-color="#d0d4d8"/></linearGradient>
    <linearGradient id="wyTagE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a7480"/><stop offset="1" stop-color="#3e464e"/></linearGradient>
    <radialGradient id="wyBead" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#b8c0c8"/><stop offset="1" stop-color="#5a6470"/></radialGradient>
    <linearGradient id="wyPanelR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf0ea"/><stop offset="1" stop-color="#f4d6cc"/></linearGradient>
    <linearGradient id="wyPanelG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef8ee"/><stop offset="1" stop-color="#cfe8d2"/></linearGradient>`;

  // ---------------- grass: filled curved blades in 3 tones with a lit edge ----------------
  const TONES = { day: ["#4e6a26", "#7a9a3a", "#a8b85a", "#e2dc8a"], dusk: ["#3a3a1e", "#6a5e2e", "#9a7e44", "#f0b878"] };
  const blade = (x, y, h, w, lean, c, hi) => {
    const tx = x + lean * h, ty = y - h, cx = x + lean * h * 0.35;
    return `<path d="M${f1(x - w)},${y}Q${f1(cx - w * 0.4)},${f1(y - h * 0.55)} ${f1(tx)},${f1(ty)}Q${f1(cx + w * 0.5)},${f1(y - h * 0.5)} ${f1(x + w)},${y}Z" fill="${c}"/>` +
      (hi ? `<path d="M${f1(x - w * 0.5)},${f1(y - 4)}Q${f1(cx - w * 0.3)},${f1(y - h * 0.55)} ${f1(tx)},${f1(ty)}" stroke="${hi}" stroke-width="${f1(Math.max(1.2, w * 0.25))}" fill="none" opacity=".7"/>` : "");
  };
  // a clump: o.n blades, heights h·(0.5..1.1); sway group per clump
  const clump = (x, y, h, r, T, o = {}) => {
    let g = "";
    const n = o.n ?? 9, w = o.w ?? Math.max(4, h * 0.035);
    for (let k = 0; k < n; k++) { const lean = (k - n / 2) / n * 0.9 + (r() - 0.5) * 0.3, hh = h * (0.5 + r() * 0.6), tone = k % 3;
      g += blade(x + (k - n / 2) * w * 0.9 + (r() - 0.5) * w, y, hh, w * (0.8 + r() * 0.5), lean, T[tone], tone === 2 ? T[3] : null); }
    return `<g transform="translate(0,0)"><g class="wrSway" data-amp="${o.amp ?? 3}">${g}</g></g>`;
  };
  War.grass = (x0, x1, y, h, r, T, o = {}) => { let g = ""; const step = o.step ?? h * 0.22; for (let x = x0; x < x1; x += step * (0.7 + r() * 0.6)) g += clump(x, y + (r() - 0.5) * (o.jit ?? 10), h * (0.7 + r() * 0.5), r, T, o); return g; };

  // ---------------- a leafy tree / a bush ----------------
  const leafSpray = (cx, cy, R, r, n, c) => { let g = ""; for (let k = 0; k < n; k++) { const a = r() * Math.PI * 2, d = R * (0.85 + r() * 0.25), lx = cx + Math.cos(a) * d, ly = cy + Math.sin(a) * d * 0.86;
    g += `<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="${f1(R * 0.09)}" ry="${f1(R * 0.045)}" transform="rotate(${f1((a * 180) / Math.PI + 90)} ${f1(lx)} ${f1(ly)})" fill="${c}"/>`; } return g; };
  const cluster = (cx, cy, R, r, dusk) => {
    const D = dusk ? "#2a3a1c" : "url(#wyLeafD)", M = dusk ? "#5a5a2a" : "url(#wyLeafM)", Lc = dusk ? "#c89a5a" : "url(#wyLeafL)";
    return `<path d="${blob(cx + R * 0.08, cy + R * 0.1, R, r, 11)}" fill="${D}"/>${leafSpray(cx + R * 0.08, cy + R * 0.1, R, r, 14, dusk ? "#2a3a1c" : "#2a4a20")}
      <path d="${blob(cx - R * 0.06, cy - R * 0.06, R * 0.8, r, 10)}" fill="${M}"/>${leafSpray(cx - R * 0.06, cy - R * 0.06, R * 0.8, r, 10, dusk ? "#6a6430" : "#5e8a36")}
      <path d="${blob(cx - R * 0.3, cy - R * 0.3, R * 0.42, r, 8)}" fill="${Lc}" opacity=".9"/>
      <path d="${blob(cx - R * 0.06, cy - R * 0.06, R * 0.8, r, 10)}" fill="none" stroke="${dusk ? "#f0b070" : "#e8ec9a"}" stroke-width="3" stroke-dasharray="${f1(R * 0.9)} ${f1(R * 4)}" stroke-dashoffset="${f1(R * 2.6)}" opacity=".75"/>`;
  };
  War.tree = (x, G, s, r, o = {}) => {
    const dusk = o.time === "dusk";
    let g = `<ellipse cx="${o.shadowX ?? 260}" cy="6" rx="420" ry="40" fill="#1a1a10" opacity=".28"/>`;
    g += `<path d="M-44,0Q-30,-180 -26,-400Q-110,-500 -220,-560L-206,-584Q-100,-536 -12,-470Q4,-560 60,-680L88,-668Q40,-560 28,-450Q110,-510 220,-540L226,-514Q110,-480 32,-396Q30,-190 46,0Z" fill="url(#wyBark)" ${O(3)}/>`;
    g += `<path d="M-18,-40Q-12,-200 -8,-380M10,-60Q6,-220 12,-360M-30,-120q10,-20 4,-46M24,-200q-8,-24 0,-44" stroke="#2a1e14" stroke-width="3.5" opacity=".55" fill="none"/>
      <path d="M-40,-10Q-30,-200 -24,-390" stroke="#c8a070" stroke-width="5" opacity=".45" fill="none"/>`;
    if (o.notch) g += `<g transform="translate(0,-210)"><path d="M-20,-20L20,20M20,-20L-20,20" stroke="#f2e2c0" stroke-width="12" stroke-linecap="round"/><path d="M-20,-20L20,20M20,-20L-20,20" stroke="#6a4a2a" stroke-width="3" stroke-linecap="round"/></g>`;
    const C = [[-210, -640, 170], [200, -630, 180], [0, -770, 210], [-120, -880, 160], [130, -890, 170], [-320, -560, 120], [320, -540, 110], [10, -620, 150]];
    g += `<g transform="translate(0,-560)"><g class="wrSway" data-amp="1.4" data-oy="1">${C.map(([cx, cy, R]) => cluster(cx, cy + 560, R, r, dusk)).join("")}</g></g>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  };
  War.bushHTML = (x, y, id, s = 1, o = {}) => {
    const r = mk(o.seed || 41), dusk = o.time === "dusk";
    // twigs
    let g = `<path d="M-30,0Q-50,-60 -120,-110M20,0Q50,-70 120,-120" stroke="#4a3624" stroke-width="9" stroke-linecap="round" fill="none"/><path d="M-30,0Q-50,-60 -120,-110" stroke="#8a6a48" stroke-width="3" fill="none" transform="translate(-2,-3)"/>`;
    const C = o.gaps ? [[-200, -170, 90], [-230, -60, 75], [-130, -270, 70], [190, -190, 88], [230, -70, 72], [130, -280, 66], [-80, -40, 60], [80, -40, 60]]
      : [[-150, -110, 100], [0, -170, 130], [150, -110, 100], [-70, -60, 90], [80, -60, 90], [-200, -50, 70], [210, -50, 70]];
    C.forEach(([cx, cy, R]) => { g += `<g transform="translate(${cx},${cy})"><g class="wrSway" data-amp="2.2">${cluster(0, 0, R, r, dusk)}</g></g>`; });
    // a few loose sprigs that let you see through
    for (let k = 0; k < (o.gaps ? 14 : 10); k++) { const a = -Math.PI * (0.1 + r() * 0.8), d = 160 + r() * 90; const ex = Math.cos(a) * d, ey = -140 + Math.sin(a) * d * 0.6, sx = ex * 0.7, sy = ey + 40; g += `<g transform="translate(0,0)"><g class="wrSway" data-amp="3"><path d="M${f1(sx)},${f1(sy)}Q${f1((sx + ex) / 2 + 10)},${f1((sy + ey) / 2 - 14)} ${f1(ex)},${f1(ey)}" stroke="#5a4430" stroke-width="2.6" fill="none"/>${leafSpray(ex, ey, 22, r, 7, k % 2 ? "#7aa244" : "#4a7a30")}${leafSpray((sx + ex) / 2, (sy + ey) / 2, 14, r, 4, "#5e8a36")}</g></g>`; }
    return `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}><ellipse cx="40" cy="4" rx="260" ry="26" fill="#1a1a10" opacity=".3"/>${g}</g></g>`;
  };
  War.bush = (layer, x, y, s, id, o) => put(layer, War.bushHTML(x, y, id, s, o));

  // ---------------- sandbags, barbed wire, bones ----------------
  const bags = (x, y, s, n = 5) => { let g = ""; for (let row = 0; row < 3; row++) for (let k = 0; k < n - row; k++) { const bx = (k - (n - row) / 2) * 150 + 75, by = -row * 70;
    g += `<g transform="translate(${bx},${by})"><path d="M-76,0Q-82,-40 -66,-62Q0,-74 66,-62Q82,-40 76,0Q0,10 -76,0Z" fill="url(#wyBag)" ${O(3)}/><path d="M-60,-30Q0,-22 60,-30" stroke="#8a7248" stroke-width="3" fill="none" opacity=".7"/>
      <path d="M-50,-60q-10,8 -6,20M50,-60q10,8 6,20" stroke="#8a7248" stroke-width="3" fill="none"/><path d="M-64,-56Q0,-68 60,-58" stroke="#f2e2b8" stroke-width="4" fill="none" opacity=".6"/></g>`; }
    return `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="40" cy="6" rx="${n * 90}" ry="24" fill="#1a1a10" opacity=".3"/>${g}</g>`; };
  const wire = (x0, x1, y, s = 1) => { let g = ""; for (let x = x0; x <= x1; x += 300) g += `<path d="M${x},${y + 20}L${x + 10},${y - 170 * s}" stroke="#5a4430" stroke-width="${12 * s}" stroke-linecap="round"/>`;
    let d = `M${x0},${y - 110 * s}`; for (let x = x0; x <= x1; x += 40) d += `Q${x + 20},${f1(y - 150 * s + Math.sin(x * 0.07) * 20)} ${x + 40},${f1(y - 100 * s)}`;
    let d2 = `M${x0},${y - 60 * s}`; for (let x = x0; x <= x1; x += 40) d2 += `Q${x + 20},${f1(y - 20 * s)} ${x + 40},${f1(y - 70 * s)}`;
    g += `<path d="${d}" stroke="#3a3a3a" stroke-width="${3 * s}" fill="none"/><path d="${d2}" stroke="#3a3a3a" stroke-width="${3 * s}" fill="none"/>`;
    for (let x = x0 + 20; x <= x1; x += 60) g += `<path d="M${x - 8},${f1(y - 128 * s)}l16,12M${x + 8},${f1(y - 128 * s)}l-16,12" stroke="#2a2a2a" stroke-width="${2.4 * s}"/>`;
    return g; };
  const bones = (x, y, s) => `<g transform="translate(${x},${y}) scale(${s})"><g transform="rotate(-14)"><rect x="-60" y="-8" width="120" height="16" rx="8" fill="#efe8d8" ${O(3)}/>${[[-60, -6], [-60, 8], [60, -6], [60, 8]].map(([a, b]) => `<circle cx="${a}" cy="${b}" r="11" fill="#efe8d8" ${O(3)}/>`).join("")}</g>
    <path d="M-30,24Q0,0 40,22Q30,40 0,40Q-24,40 -30,24Z" fill="#e2dac6" ${O(3)}/><path d="M-10,24h6M8,24h6" stroke="${INK}" stroke-width="4"/></g>`;

  // ---------------- the border field ----------------
  const ridgeY = (k, x, G, seed, lift = 0) => G - 430 - lift * (1 - k / 4) + k * 85 - Math.sin(x * 0.0032 + k * 1.7 + seed) * 70 - Math.sin(x * 0.011 + k) * 22;
  Sets.border = (L, o = {}) => {
    const id = o.id || "bd", r = mk(o.seed || 31), dusk = o.time === "dusk", G = o.ground ?? 1360, T = dusk ? TONES.dusk : TONES.day, sd = o.seed || 3;
    const sunX = o.sunX ?? 140, lift = o.lift ?? 0, sunY = o.sunY ?? G - 470 - lift * 0.6;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${dusk ? "wySkyK" : "wySky"})"/>
      <circle cx="${sunX}" cy="${sunY}" r="520" fill="url(#wySun)"/><circle cx="${sunX}" cy="${sunY}" r="54" fill="#fff8e0"/>
      ${[[300, 300, 1.3], [1100, 430, 1], [-400, 200, 1.1], [700, 140, 0.8]].map(([x, y, s]) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse rx="380" ry="26" fill="#fff4e4" opacity=".45"/><ellipse cx="-60" cy="-14" rx="240" ry="20" fill="#fffaf0" opacity=".5"/><ellipse cx="90" cy="10" rx="300" ry="14" fill="#e8b890" opacity=".35"/></g>`).join("")}`);
    // 4 ridges, lighter and warmer with distance, fog bands between; the 2nd carries the glint; the 3rd a tree line
    const RC = dusk ? ["#b88a8a", "#8a6a74", "#5e4e52", "#3e3a32"] : ["#c8bcb0", "#a2a49e", "#7e8c78", "#5e7046"];
    let far = "";
    for (let k = 0; k < 4; k++) {
      let d = `M-1300,${f1(ridgeY(k, -1300, G, sd, lift))}`; for (let x = -1300; x <= 2400; x += 60) d += `L${x},${f1(ridgeY(k, x, G, sd, lift))}`;
      far += `<path d="${d}L2400,${G + 300}H-1300Z" fill="${RC[k]}"/>`;
      if (k === 2) for (let x = -1300; x < 2400; x += 34 + r() * 30) { const y = ridgeY(k, x, G, sd, lift); far += `<path d="${blob(x, y - 10, 22 + r() * 18, r, 7)}" fill="${dusk ? "#4a3e3e" : "#6a7a56"}"/>`; }
      if (k < 3) far += `<rect x="-1300" y="${f1(G - 420 - lift * (1 - k / 4) + k * 85 + 10)}" width="3700" height="120" fill="url(#wyHaze)"/>`;
    }
    const gx = o.glintX ?? 760, gy = ridgeY(1, gx, G, sd, lift) + 10;
    put(L.far, far + (o.glint !== false ? `<g transform="translate(${gx},${f1(gy)})"><g id="${id}-glint" opacity=".6"><circle r="26" fill="url(#wyStar)"/><path d="M0,-22L3,-3L22,0L3,3L0,22L-3,3L-22,0L-3,-3Z" fill="#fff"/><circle r="4" fill="#fff"/></g></g>` : ""));
    // mid: the field plane with far bushes and a small tree
    let mid = `<path d="M-1300,${G - 120}Q500,${G - 150} 2400,${G - 110}V${G + 700}H-1300Z" fill="${dusk ? "#7a6a3a" : "url(#wyField)"}"/>`;
    for (let k = 0; k < 16; k++) { const x = -1200 + r() * 3500, y = G - 110 + r() * 50; mid += `<path d="${blob(x, y, 30 + r() * 40, r, 8)}" fill="${dusk ? "#4a4224" : "#5e7032"}"/><path d="${blob(x - 8, y - 8, 18 + r() * 20, r, 7)}" fill="${dusk ? "#8a7040" : "#8aa04a"}" opacity=".7"/>`; }
    mid += War.grass(-1300, 2400, G - 100, 40, r, T, { n: 5, step: 50, amp: 0 });
    put(L.mid, mid);
    // set: ground, path, the leafy tree, sandbags, bamboo, bones
    let s = `<rect x="-1300" y="${G - 60}" width="3700" height="1700" fill="${dusk ? "#5e5430" : "url(#wyGround)"}"/>`;
    for (let k = 0; k < 60; k++) { const x = -1200 + r() * 3400, y = G - 40 + r() * 900; s += `<path d="M${f1(x)},${f1(y)}q${f1(10 + r() * 20)},-6 ${f1(30 + r() * 30)},0" stroke="${k % 2 ? "#6a7034" : "#b0a860"}" stroke-width="3" fill="none" opacity=".5"/>`; }
    for (let k = 0; k < 40; k++) { const x = -1200 + r() * 3400, y = G + r() * 700, sc = 0.4 + (y - G) / 700; s += War.grass(x, x + 60 * sc, y, 60 * sc, r, T, { n: 6, step: 30 * sc, amp: 0 }); if (k % 3 === 0) s += `<ellipse cx="${f1(x + 50)}" cy="${f1(y)}" rx="${f1(10 * sc)}" ry="${f1(6 * sc)}" fill="#8a826a" ${O(1.6)}/>`; }
    if (o.path !== false) { const px = o.pathX ?? 420; s += `<path d="M${px - 160},${G + 1000}C${px - 40},${G + 500} ${px - 80},${G + 120} ${px + 60},${G - 50}L${px + 110},${G - 50}C${px + 40},${G + 120} ${px + 160},${G + 500} ${px + 300},${G + 1000}Z" fill="${dusk ? "#7a5a3a" : "#b8925e"}" opacity=".85"/>
      <path d="M${px - 100},${G + 900}C${px},${G + 500} ${px - 40},${G + 150} ${px + 80},${G - 40}" stroke="#d8b888" stroke-width="5" fill="none" opacity=".5"/>`; }
    if (o.tree !== false) s += War.tree(o.tree ?? 900, G + 20, o.treeS ?? 0.9, r, { notch: o.notch, time: o.time });
    if (o.bamboo !== false && o.bamboo !== undefined) { const bx = o.bamboo; s += `<g transform="translate(${bx},${G + 70})"><g id="${id}-bamboo"><ellipse cx="60" cy="6" rx="110" ry="12" fill="#1a1a10" opacity=".3"/>
      <path d="M-60,0L50,-160M60,0L-50,-160" stroke="#d8b860" stroke-width="16" stroke-linecap="round"/><path d="M-60,0L50,-160M60,0L-50,-160" stroke="#7a5a24" stroke-width="2.6" fill="none"/>
      <path d="M-56,-4L46,-156" stroke="#f6e2a0" stroke-width="4" opacity=".6"/>${[[-32, -40], [30, -40], [-8, -112], [8, -112]].map(([x, y]) => `<path d="M${x - 9},${y}h18" stroke="#7a5a24" stroke-width="3.5"/>`).join("")}
      <path d="M-20,-80q20,-10 40,0" stroke="#8a6a2a" stroke-width="4" fill="none"/></g></g>`; }
    if (o.bones) s += bones(o.bones[0], o.bones[1], o.bones[2] ?? 1);
    if (o.bags) s += bags(o.bags[0], o.bags[1], o.bags[2] ?? 1, o.bags[3] ?? 5);
    put(L.set, s);
    // feet band in L.glow (over the actors) and the near grass + wire in fg
    if (o.band) put(L.glow, `<g>${War.grass(o.band[0], o.band[1], o.band[2], o.band[3] ?? 110, mk(sd + 5), T, { step: 26, n: 8 })}</g>`);
    let fg = War.grass(-500, 1700, 2060, 420 * (o.fgH ?? 1), mk(sd + 9), T, { step: 70, n: 11, amp: 4 });
    if (o.wire) fg = wire(o.wire[0], o.wire[1], o.wire[2], o.wire[3] ?? 1) + fg;
    if (o.fgBags) fg = bags(o.fgBags[0], o.fgBags[1], o.fgBags[2] ?? 1.6, o.fgBags[3] ?? 4) + fg;
    put(L.fg, fg);
  };
  Sets.hedge = (L, o = {}) => {
    const id = o.id || "hg", G = o.ground ?? 1400, r = mk(o.seed || 7);
    Sets.border(L, { ...o, id: id + "b", time: o.time || "day", bamboo: undefined, path: false, glint: false, notch: false, tree: o.tree ?? 900, ground: G });
    put(L.set, `<g transform="translate(${o.bank ?? 140},${G + 150})"><g id="${id}-bank"><ellipse cx="60" cy="10" rx="330" ry="30" fill="#1a1a10" opacity=".3"/><path d="M-280,0Q-220,-170 0,-190Q220,-170 280,0Z" fill="#8a6440" ${O(4)}/>
      <path d="M-220,-60Q0,-150 220,-60" stroke="#b08a5a" stroke-width="12" fill="none" opacity=".6"/><path d="M-120,-30q20,-10 40,0M60,-50q16,-8 32,0" stroke="#5a3e24" stroke-width="5" fill="none"/>
      ${War.grass(-200, 200, -165, 60, r, TONES.day, { n: 6, step: 30 })}</g></g>`);
    if (!o.bushFront) War.bush(L.set, o.bush ?? 540, G + 170, 1, id + "-bush", { gaps: o.gaps });
  };

  // ---------------- motion helpers ----------------
  War.sway = (tl, root, t0, dur) => {
    if (!root) return;
    root.querySelectorAll(".wrSway").forEach((e, k) => { const amp = +(e.dataset.amp || 3); if (!amp) return; const P = 1.6 + (k % 5) * 0.27;
      tl.fromTo(e, { rotation: -amp * 0.5, transformOrigin: e.dataset.oy ? "50% 100%" : "50% 100%" }, { rotation: amp * 0.5, transformOrigin: "50% 100%", duration: P / 2, repeat: Math.ceil(dur / (P / 2)) + 1, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 - (k % 7) * 0.13 > 0 ? t0 - (k % 7) * 0.13 : t0); });
  };
  War.jiggle = (tl, aid, t0, dur, o = {}) => {
    const P = o.period ?? 0.32, n = Math.ceil(dur / P) + 1;
    tl.fromTo(`#${aid}-strap`, { rotation: -(o.amp ?? 12), transformOrigin: "50% 0%" }, { rotation: o.amp ?? 12, transformOrigin: "50% 0%", duration: P / 2, repeat: n * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
    tl.fromTo(`#${aid}-tagj`, { rotation: -(o.amp ?? 12) * 1.3, transformOrigin: "50% 0%" }, { rotation: (o.amp ?? 12) * 1.3, transformOrigin: "50% 0%", duration: P * 0.55, repeat: n * 2, yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.05);
  };
  War.glint = (tl, id, t0, dur, o = {}) => {
    const sel = `#${id}-glint`;
    (o.at || [0.15, 1.1, 2.2]).forEach((a) => tl.fromTo(sel, { opacity: 0.6, scale: 0.7, rotation: 0, transformOrigin: "50% 50%" }, { keyframes: [{ opacity: 1, scale: 1.25, rotation: 45, duration: 0.12, ease: "power2.out" }, { opacity: 0.6, scale: 0.7, rotation: 90, duration: 0.3, ease: "power2.in" }], immediateRender: false }, t0 + a));
  };

  // ---------------- the mine ----------------
  War.blast = (tl, L, x, y, t, o = {}) => {
    const id = o.id || nid(), s = o.s ?? 1, r = mk(o.seed || 17);
    // white-out (3 frames) then a warm afterglow
    tl.fromTo("#flashw", { opacity: 0, backgroundColor: "#ffffff" }, { keyframes: [{ opacity: 1, duration: 0.01 }, { opacity: 1, duration: 0.04 }, { opacity: 0, duration: 0.22, ease: "power2.out" }], immediateRender: false }, t);
    let jets = "", clods = "", spray = "", blades = "", puffs = "";
    for (let k = 0; k < 9; k++) { const a = (k - 4) * 9 + (r() - 0.5) * 6, h = 380 + r() * 260, w = 26 + r() * 22;
      jets += `<g transform="rotate(${f1(a)})"><g id="${id}-j${k}" opacity="0"><path d="M${-w},0Q${f1(-w * 0.6)},${f1(-h * 0.6)} 0,${f1(-h)}Q${f1(w * 0.6)},${f1(-h * 0.6)} ${w},0Z" fill="url(#wyJet)"/></g></g>`; }
    for (let k = 0; k < 30; k++) { const big = k % 4 === 0, sz = big ? 1.8 : 0.8 + r() * 0.6;
      clods += `<g id="${id}-c${k}" opacity="0"><path d="M${f1(-10 * sz)},${f1(-4 * sz)}Q${f1(-2 * sz)},${f1(-14 * sz)} ${f1(11 * sz)},${f1(-7 * sz)}Q${f1(15 * sz)},${f1(6 * sz)} ${f1(4 * sz)},${f1(11 * sz)}Q${f1(-11 * sz)},${f1(13 * sz)} ${f1(-12 * sz)},${f1(2 * sz)}Z" fill="${k % 3 ? "#5a4028" : "#7a5a38"}" ${O(1.6)}/><path d="M${f1(-6 * sz)},${f1(-6 * sz)}q${f1(6 * sz)},${f1(-4 * sz)} ${f1(12 * sz)},0" stroke="#a8865a" stroke-width="2" fill="none"/></g>`; }
    for (let k = 0; k < 14; k++) blades += `<g id="${id}-b${k}" opacity="0"><path d="M-3,22Q-6,0 2,-26Q6,0 3,22Z" fill="${k % 2 ? "#8aa040" : "#c8c070"}"/></g>`;
    for (let k = 0; k < 50; k++) spray += `<circle id="${id}-p${k}" r="${f1(2 + r() * 3)}" fill="${k % 2 ? "#8a6a44" : "#c4a47a"}" opacity="0"/>`;
    for (let k = 0; k < 7; k++) { const px = (r() - 0.5) * 140, py = -50 - k * 50, pr = 60 + r() * 40; puffs += `<g transform="translate(${f1(px)},${f1(py)})"><g id="${id}-u${k}" opacity="0"><path d="${blob(8, 10, pr, r, 9)}" fill="#7a5e40"/><path d="${blob(0, 0, pr * 0.92, r, 9)}" fill="#b0906a"/><path d="${blob(-pr * 0.25, -pr * 0.25, pr * 0.5, r, 8)}" fill="#dcc4a0" opacity=".85"/></g></g>`; }
    put(L.set, `<g transform="translate(${x},${y - 30}) scale(${s})">${puffs}${jets}</g>`);
    put(L.glow, `<g transform="translate(${x},${y}) scale(${s})">
      <g id="${id}-sw" opacity="0"><ellipse rx="80" ry="16" fill="none" stroke="#f6ead0" stroke-width="8" opacity=".7"/><ellipse rx="64" ry="12" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/></g>
      <g id="${id}-core" opacity="0"><circle cy="-40" r="170" fill="url(#wyCore)"/></g>${spray}${clods}${blades}</g>`);
    tl.fromTo(`#${id}-core`, { opacity: 1, scale: 0.4, transformOrigin: "50% 75%" }, { opacity: 0, scale: 1.5, transformOrigin: "50% 75%", duration: 0.25, ease: "power2.out", immediateRender: false }, t);
    tl.fromTo(`#${id}-sw`, { opacity: 1, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 0, scale: 9, transformOrigin: "50% 50%", duration: 0.55, ease: "power2.out", immediateRender: false }, t + 0.02);
    for (let k = 0; k < 9; k++) {
      tl.fromTo(`#${id}-j${k}`, { opacity: 1, scaleY: 0.05, scaleX: 0.6, transformOrigin: "50% 100%" }, { scaleY: 1, scaleX: 1, transformOrigin: "50% 100%", duration: 0.2 + (k % 3) * 0.04, ease: "power3.out", immediateRender: false }, t + 0.01);
      tl.to(`#${id}-j${k}`, { opacity: 0, scaleX: 1.8, y: -60, duration: 0.7, ease: "power1.in" }, t + 0.32);
    }
    for (let k = 0; k < 7; k++) {
      tl.fromTo(`#${id}-u${k}`, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "power2.out", immediateRender: false }, t + 0.05 + k * 0.025);
      tl.to(`#${id}-u${k}`, { scale: 1.35, x: (o.drift ?? -1) * (40 + k * 16), y: -60 - k * 10, opacity: o.linger ? 0.4 : 0, duration: 2.6, ease: "sine.out" }, t + 0.4 + k * 0.025);
    }
    const fall = (sel, a, v, up, tt, land) => tl.fromTo(sel, { x: 0, y: 0, rotation: 0, opacity: 1 }, { keyframes: [
      { x: Math.cos(a) * v * 0.5, y: -up, rotation: 220, duration: tt * 0.45, ease: "power2.out" },
      { x: Math.cos(a) * v, y: land, rotation: 480, duration: tt * 0.55, ease: "power2.in" }, { opacity: 0, duration: 0.25 }], immediateRender: false }, t);
    for (let k = 0; k < 30; k++) { const a = -Math.PI / 2 + (r() - 0.5) * 2.4; fall(`#${id}-c${k}`, a, 260 + r() * 520, 260 + r() * 520, 0.9 + r() * 0.6, 10 + r() * 40); }
    for (let k = 0; k < 14; k++) { const a = -Math.PI / 2 + (r() - 0.5) * 2.0; fall(`#${id}-b${k}`, a, 200 + r() * 400, 300 + r() * 400, 1.4 + r() * 0.8, 60 + r() * 120); }
    for (let k = 0; k < 50; k++) { const a = -Math.PI / 2 + (r() - 0.5) * 2.6, v = 200 + r() * 600;
      tl.fromTo(`#${id}-p${k}`, { x: 0, y: -20, opacity: 1 }, { x: Math.cos(a) * v, y: Math.sin(a) * v * 0.8, opacity: 0, duration: 0.5 + r() * 0.5, ease: "power3.out", immediateRender: false }, t); }
    // clods that fly past the lens (fg, big and blurred)
    if (L.fg) { let near = ""; for (let k = 0; k < 4; k++) near += `<g transform="translate(${f1(250 + r() * 600)},${f1(1450 + r() * 300)})"><g id="${id}-n${k}" opacity="0"><path d="M-16,-6Q-4,-22 16,-10Q24,8 6,16Q-18,18 -16,-6Z" fill="#4a3420"/></g></g>`;
      for (let k = 0; k < 5; k++) near += `<g transform="translate(${f1(-300 + k * 180)},${f1(900 + r() * 700)})"><g id="${id}-d${k}" opacity="0"><circle r="${f1(260 + r() * 160)}" fill="url(#wyPuffL)"/></g></g>`;
      put(L.fg, near);
      for (let k = 0; k < 4; k++) tl.fromTo(`#${id}-n${k}`, { opacity: 0, scale: 0.4, x: 0, y: 0, transformOrigin: "50% 50%" }, { keyframes: [{ opacity: 1, duration: 0.01 }, { scale: 2.2, x: (k - 3) * 160, y: 500, rotation: 200, duration: 0.45, ease: "power2.in" }, { opacity: 0, duration: 0.01 }], immediateRender: false }, t + 0.08 + k * 0.06);
      for (let k = 0; k < 5; k++) tl.fromTo(`#${id}-d${k}`, { opacity: 0, x: -200 }, { keyframes: [{ opacity: 0.5, x: 0, duration: 0.8, ease: "power1.out" }, { opacity: 0, x: 500, duration: 2.4, ease: "none" }], immediateRender: false }, t + 0.5 + k * 0.18);
    }
    // grass bent away by the wave, then springing back
    if (o.bend) document.querySelectorAll(o.bend).forEach((e, k) => tl.fromTo(e, { skewX: 0 }, { keyframes: [{ skewX: (e.getBBox().x > x ? 1 : -1) * 22, duration: 0.08, ease: "power3.out" }, { skewX: 0, duration: 0.9, ease: "elastic.out(1.1,0.3)" }], immediateRender: false }, t + 0.03 + k * 0.004));
    // tinnitus: 0.5 s soft focus and washed colour
    if (o.world) tl.fromTo(`#${o.world}`, { filter: "blur(0px) saturate(1) brightness(1)" }, { keyframes: [{ filter: "blur(2.5px) saturate(0.45) brightness(1.1)", duration: 0.12 }, { filter: "blur(2.5px) saturate(0.45) brightness(1.1)", duration: 0.5 }, { filter: "blur(0px) saturate(1) brightness(1)", duration: 0.45, ease: "power2.inOut" }], immediateRender: false }, t + 0.12);
  };

  // ---------------- a bullet in slow motion through the bush ----------------
  War.bulletSlow = (tl, L, o = {}) => {
    const id = nid(), r = mk(o.seed || 29), y = o.y, x0 = o.x0 ?? 900, x1 = o.x1 ?? 250, T = o.t, slow = o.slow ?? 0.4;
    const bullet = (k) => `<g transform="translate(0,${y + (k ? (r() - 0.5) * 120 : 0)})"><g id="${id}-k${k}" opacity="0"><path d="M0,-7L360,-2L360,2L0,7Z" fill="url(#wyTrail)"/><ellipse rx="22" ry="9" fill="#fff6d0" opacity=".6"/><ellipse rx="11" ry="4.5" fill="#fff"/></g></g>`;
    let g = ""; for (let k = 0; k < 4; k++) g += bullet(k);
    // leaf bursts along the slow stretch
    const NB = 7; let leaves = "";
    for (let b = 0; b < NB; b++) { const bx = x0 + ((x1 - x0) * (b + 0.5)) / NB; for (let j = 0; j < 7; j++) leaves += `<g transform="translate(${f1(bx)},${f1(y + (r() - 0.5) * 30)})"><g id="${id}-l${b}-${j}" opacity="0">${j === 6 ? `<path d="M-14,0H14" stroke="#4a3624" stroke-width="5" stroke-linecap="round"/>` : `<path d="M0,-14Q14,0 0,16Q-14,0 0,-14Z" fill="${j % 3 === 0 ? "#d8e07a" : j % 3 === 1 ? "#7aa244" : "#3e6a2c"}" ${O(1.4)}/><path d="M0,-12V14" stroke="#2a4a1e" stroke-width="1.4"/>`}</g></g>`; }
    put(L.glow, `<g>${leaves}${g}</g>`);
    // the slow one: in fast, through the bush at 0.3×, out fast
    tl.fromTo(`#${id}-k0`, { x: 1500, opacity: 1 }, { keyframes: [{ x: x0, duration: 0.05, ease: "none" }, { x: x1, duration: slow, ease: "none" }, { x: -500, duration: 0.05, ease: "none" }, { opacity: 0, duration: 0.01 }], immediateRender: false }, T);
    for (let b = 0; b < NB; b++) { const tb = T + 0.05 + (slow * (b + 0.5)) / NB, sl = 2.6;
      for (let j = 0; j < 7; j++) { const a = Math.PI + (r() - 0.5) * 1.6, v = 60 + r() * 120;
        tl.fromTo(`#${id}-l${b}-${j}`, { x: 0, y: 0, rotation: 0, opacity: 1 }, { x: Math.cos(a) * v * 1.4, y: Math.sin(a) * v + 30, rotation: (r() > 0.5 ? 1 : -1) * 300, opacity: 0, duration: 1.2 * sl * 0.5, ease: "power2.out", immediateRender: false }, tb); } }
    // real speed after
    for (let k = 1; k < 4; k++) { const tk = T + 0.05 + slow + 0.15 + k * 0.17; tl.fromTo(`#${id}-k${k}`, { x: 1500, opacity: 1 }, { keyframes: [{ x: -500, duration: 0.12, ease: "none" }, { opacity: 0, duration: 0.01 }], immediateRender: false }, tk); }
    return { slowFrom: T + 0.05, slowTo: T + 0.05 + slow };
  };

  // ---------------- highlight a sign in the field ----------------
  War.spot = (tl, layer, x, y, t0, dur, o = {}) => {
    const id = nid(), R = o.r ?? 120, r = mk(o.seed || 5);
    let sp = ""; for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2; sp += `<g transform="translate(${f1(Math.cos(a) * R * 1.15)},${f1(Math.sin(a) * R * 0.75)})"><g id="${id}-s${k}" opacity="0"><path d="M0,-12L3,-3L12,0L3,3L0,12L-3,3L-12,0L-3,-3Z" fill="#fff6c0"/></g></g>`; }
    const ly = -R * 0.75 - 150;
    put(layer, `<g transform="translate(${x},${y})">
      <g id="${id}-w1" opacity="0"><ellipse rx="${R}" ry="${f1(R * 0.62)}" fill="none" stroke="#ffd23a" stroke-width="10"/></g>
      <g id="${id}-w2" opacity="0"><ellipse rx="${R}" ry="${f1(R * 0.62)}" fill="none" stroke="#fff4b0" stroke-width="5"/></g>
      <g id="${id}-ring" opacity="0"><ellipse rx="${R}" ry="${f1(R * 0.62)}" fill="#ffd23a" fill-opacity=".12" stroke="#ffd23a" stroke-width="7"/>
        <g id="${id}-dash"><ellipse rx="${f1(R * 1.12)}" ry="${f1(R * 0.72)}" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="18 14" opacity=".9"/></g></g>${sp}
      <path id="${id}-stem" d="M0,${f1(-R * 0.62)}V${f1(ly + 60)}" stroke="#fff" stroke-width="5" opacity="0"/>
      <g transform="translate(0,${f1(ly)})"><g id="${id}-pill" opacity="0">
        <rect x="-${o.w ?? 210}" y="-56" width="${(o.w ?? 210) * 2}" height="112" rx="56" fill="#3a2a1a" opacity=".35" transform="translate(6,10)"/>
        <rect x="-${o.w ?? 210}" y="-56" width="${(o.w ?? 210) * 2}" height="112" rx="56" fill="#fffaf0" ${O(5)}/><rect x="-${(o.w ?? 210) - 8}" y="-48" width="${(o.w ?? 210) * 2 - 16}" height="30" rx="15" fill="#fff" opacity=".8"/>
        <g transform="translate(${-(o.w ?? 210) + 6},-62) scale(1.03)"><g id="${id}-coin">${War.coin(o.icon || "bamboo", 0, 0, 1)}</g></g>
        <text x="${(o.tx ?? 50)}" y="16" font-family="Kanit" font-weight="900" font-size="46" fill="#8a1a12" text-anchor="middle">${o.label || ""}</text></g></g></g>`);
    ["ring", "w1", "w2", "stem", "pill"].forEach((n) => tl.set(`#${id}-${n}`, { opacity: 0 }, 0));
    tl.fromTo(`#${id}-ring`, { opacity: 0, scale: 2.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-dash`, { rotation: 0, transformOrigin: "50% 50%" }, { rotation: 360, transformOrigin: "50% 50%", duration: 4, repeat: Math.ceil(dur / 4), ease: "none", immediateRender: false }, t0);
    [["w1", 0.1], ["w2", 0.3], ["w1", 1.1], ["w2", 1.3]].forEach(([n, d]) => tl.fromTo(`#${id}-${n}`, { opacity: 0.9, scale: 1, transformOrigin: "50% 50%" }, { opacity: 0, scale: 1.9, transformOrigin: "50% 50%", duration: 0.8, ease: "power2.out", immediateRender: false }, t0 + d));
    for (let k = 0; k < 8; k++) tl.fromTo(`#${id}-s${k}`, { opacity: 0, scale: 0, transformOrigin: "50% 50%" }, { keyframes: [{ opacity: 1, scale: 1.3, rotation: 90, duration: 0.2 }, { opacity: 0, scale: 0.3, rotation: 180, duration: 0.35 }], immediateRender: false }, t0 + 0.25 + k * 0.05 + r() * 0.1);
    tl.fromTo(`#${id}-stem`, { opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, transformOrigin: "50% 100%", duration: 0.2, immediateRender: false }, t0 + 0.3);
    tl.fromTo(`#${id}-pill`, { opacity: 0, scale: 0.3, y: 40, transformOrigin: "50% 100%" }, { opacity: 1, scale: 1, y: 0, transformOrigin: "50% 100%", duration: 0.5, ease: "back.out(2.4)", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-pill`, { y: 0 }, { y: -10, duration: 0.7, repeat: Math.ceil(dur / 0.7), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.9);
    const ce = document.getElementById(`${id}-coin`); QkUI.iconPop(tl, ce, t0 + 0.55); RabFX.life(tl, ce, t0 + 1.0, dur);
    if (o.out) tl.to([`#${id}-ring`, `#${id}-stem`, `#${id}-pill`], { opacity: 0, duration: 0.2 }, t0 + dur - 0.2);
  };

  // ---------------- poses ----------------
  const M = Rig.MODES;
  M.surge = (u, o) => { const s = Math.sin(u * 2 * Math.PI / 0.55), c = Math.cos(u * 2 * Math.PI / 0.55);
    return { ...M.idle(u, o), torso: 20 + 7 * s, head: 10 + 4 * c, uaF: -105 + 14 * s, faF: -12 + 8 * c, uaB: -80 - 12 * s, faB: -20, thF: 26 + 18 * s, shF: 30 + 20 * Math.max(0, -s), thB: -24 - 10 * s, shB: 20, bodyY: 14 + 6 * Math.abs(s) }; };
  M.drag = (u, o) => { const s = Math.sin(u * 2 * Math.PI / 0.55 + 0.8), j = Math.sin(u * 23) * 1.5;
    return { ...M.idle(u, o), torso: -16 + 5 * s + j, head: -6 + 3 * s, uaF: -72 + 8 * s, faF: -48 - 6 * s, uaB: -58 - 8 * s, faB: -56, thF: 30, shF: 10, thB: -30 + 6 * s, shB: 26, bodyY: 22 + 5 * s }; };
  M.reachUp = (u, o) => { const s = Math.sin(u * 2 * Math.PI / 0.9), lift = Math.max(0, s);
    return { ...M.lie(u, o), uaF: -150 + 24 * s, faF: -30 + 20 * s, uaB: -20 - 30 * lift, faB: -40, head: -16 - 22 * lift, torso: -6 * lift, thF: 8 * s, shF: 14 + 10 * lift, thB: -6 * s }; };
  M.duckLow = (u, o) => { const j = Math.sin(u * 19) * 1.6, b = Math.sin(u * 2 * Math.PI / 0.9);
    return { ...M.crouch(u, o), uaF: -150 + j, faF: -116, uaB: 150 - j, faB: 112, torso: 34 + j * 0.4 + 2 * b, head: -26 + j, bodyY: 175 + 4 * b }; };
  M.startle = (u, o) => { const k = Math.min(1, u / 0.15), j = Math.sin(u * 31) * 2; return { ...M.idle(u, o), uaF: -60 * k + j, faF: -100 * k, uaB: -50 * k, faB: -90 * k, torso: -10 * k, head: -12 * k + j, bodyY: 6 * k }; };
  M.pointAt = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 1.8); return { ...M.idle(u, o), uaF: -82 + 3 * b, faF: -4, uaB: 6, faB: -16, torso: 4, head: 2 + b, bodyY: -1 }; };

  // the helmet strap (moves with the head) and the dog tag on its chain (#aid-tagj) for the war cast
  const strap = (ctx) => `<g id="${ctx.id}-strap"><path d="M-56,-548Q-58,-500 -36,-462M56,-548Q58,-500 40,-466" stroke="#4a4234" stroke-width="3.6" fill="none" stroke-linecap="round"/><rect x="-44" y="-472" width="12" height="10" rx="2" fill="#b8a878" stroke="#3a3428" stroke-width="2"/></g>`;
  const tagJ = (ctx) => `<g id="${ctx.id}-tagj"><path d="M-22,-494Q-6,-446 0,-446Q6,-446 22,-494" stroke="#c8ccd0" stroke-width="3" fill="none" stroke-dasharray="1 3.4" stroke-linecap="round"/>
    <rect x="-9" y="-450" width="18" height="26" rx="5" fill="url(#wyTag)" stroke="#3a2622" stroke-width="1.6"/><path d="M-5,-442h10M-5,-436h7" stroke="#6a7480" stroke-width="1.6"/></g>`;
  ["tao", "joe", "mem", "enemy", "taoBare"].forEach((n) => { const v = Rig.CAST[n].v2, f = v.hair.front, bare = n === "taoBare";
    v.hair = { ...v.hair, front: (ctx) => (typeof f === "function" ? f(ctx) : f || "") + (bare ? "" : strap(ctx)) };
    v.extra = n === "enemy" ? "" : (ctx) => tagJ(ctx); });

  // ---------------- the dog tag card ----------------
  const tagPath = (w, h) => { const x = -w / 2, y = -h / 2, R = 60, n = h * 0.18; // notched on the left edge
    return `M${x + R},${y}H${w / 2 - R}Q${w / 2},${y} ${w / 2},${y + R}V${h / 2 - R}Q${w / 2},${h / 2} ${w / 2 - R},${h / 2}H${x + R}Q${x},${h / 2} ${x},${h / 2 - R}V${n + 30}L${x + 34},${n}V${-n + 20}L${x},${-n}V${y + R}Q${x},${y} ${x + R},${y}Z`; };
  const emboss = (x, y, txt, size, fill, anchor = "start") => `<text x="${x + 2}" y="${y + 2.5}" font-family="Kanit" font-weight="900" font-size="${size}" fill="#3a4048" opacity=".45" text-anchor="${anchor}">${txt}</text>
    <text x="${x - 1.5}" y="${y - 1.5}" font-family="Kanit" font-weight="900" font-size="${size}" fill="#ffffff" opacity=".85" text-anchor="${anchor}">${txt}</text>
    <text x="${x}" y="${y}" font-family="Kanit" font-weight="900" font-size="${size}" fill="${fill}" text-anchor="${anchor}">${txt}</text>`;
  WarUI.tag = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), act = o.active ?? 0, done = o.done ?? [], Y = o.y ?? 760, RULES = WarUI.RULES, W = 940, H = 560;
    let chain = ""; for (let k = 0; k <= 26; k++) { const u = k / 26, cx = -W / 2 + 110 + u * 200 - 60, cy = -H / 2 + 70 - Math.sin(u * Math.PI) * 0 - (1 - u) * 0 - u * 0; chain += ""; }
    // the chain: two strands from the hole up and out of the frame
    const strand = (x1, y1, x2, y2, sag) => { let s = ""; for (let k = 0; k <= 22; k++) { const u = k / 22, x = x1 + (x2 - x1) * u, y = y1 + (y2 - y1) * u + Math.sin(u * Math.PI) * sag; s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="7" fill="url(#wyBead)"/>`; } return s; };
    const hx = -W / 2 + 120, hy = -H / 2 + 74;
    chain = strand(hx, hy, hx - 160, -900, -40) + strand(hx, hy, hx + 260, -900, 40);
    const rows = RULES.map((rr, k) => { const on = k === act, d = done.includes(k), yy = -40 + k * 190;
      return `<g opacity="${on || d ? 1 : 0.42}"><g transform="translate(${-W / 2 + 70},${yy - 92})">${War.coin(k ? "bush" : "norush", 0, 0, 1.25, `${id}-c${k}`)}</g>
        ${emboss(-W / 2 + 240, yy + 14, rr, 42, on ? "#7a1a14" : "#4a525a")}
        ${d ? `<g transform="translate(${W / 2 - 60},${yy})"><circle id="${id}-g${k}" r="44" fill="url(#rbOkGlow)" opacity="0"/><g id="${id}-t${k}"><circle r="32" fill="#2fb864" stroke="#fff" stroke-width="5"/><path d="M-14,0l9,10l18,-20" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g></g>` : ""}</g>`; }).join("");
    put(layer, `<g id="${id}" opacity="0"><g transform="translate(540,${Y})"><g id="${id}-sw">${chain}
      <path d="${tagPath(W, H)}" fill="url(#wyTagE)" transform="translate(12,18)"/>
      <path d="${tagPath(W, H)}" fill="url(#wyTag)" ${O(5, "#3a4048")}/>
      <path d="${tagPath(W - 34, H - 34)}" fill="none" stroke="#8a949e" stroke-width="4" opacity=".7"/><path d="${tagPath(W - 40, H - 40)}" fill="none" stroke="#fff" stroke-width="2" opacity=".6" transform="translate(-2,-2)"/>
      <circle cx="${hx}" cy="${hy}" r="20" fill="#4a525a" ${O(3, "#2a3038")}/><circle cx="${hx}" cy="${hy}" r="20" fill="none" stroke="#fff" stroke-width="2" opacity=".5" transform="translate(-2,-2)"/>
      <g clip-path="url(#${id}-cl)"><rect id="${id}-sh" x="-${W}" y="-${H}" width="160" height="${H * 2}" fill="#fff" opacity=".4" transform="skewX(-22)"/></g>
      <defs><clipPath id="${id}-cl"><path d="${tagPath(W, H)}"/></clipPath></defs>
      ${emboss(60, -H / 2 + 92, "กฎของจ่าเม่น", 50, "#2a3038", "middle")}
      <path d="M-300,${-H / 2 + 120}H420" stroke="#8a949e" stroke-width="3" opacity=".6"/>${rows}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { y: -1100, rotation: -16, transformOrigin: "15% 0%" }, { y: 0, rotation: 0, transformOrigin: "15% 0%", duration: 0.8, ease: "back.out(1.5)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: -3, transformOrigin: "15% 0%" }, { rotation: 3, transformOrigin: "15% 0%", duration: 1.2, repeat: Math.ceil(dur / 1.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.8);
    tl.fromTo(`#${id}-sh`, { x: 0 }, { x: W * 2.4, duration: 0.9, repeat: Math.ceil(dur / 2.3), repeatDelay: 1.4, ease: "power1.inOut", immediateRender: false }, t0 + 0.7);
    RULES.forEach((_, k) => { const el = document.getElementById(`${id}-c${k}`); QkUI.iconPop(tl, el, t0 + 0.35 + k * 0.15); RabFX.life(tl, el, t0 + 1.0, dur); });
    done.forEach((k) => { const t = t0 + (o.tickAt ?? 0.9); tl.fromTo(`#${id}-t${k}`, { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t);
      tl.fromTo(`#${id}-g${k}`, { scale: 0.4, opacity: 1, transformOrigin: "50% 50%" }, { scale: 2.2, opacity: 0, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.out", immediateRender: false }, t + 0.1); });
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- the cross-section card: concealment vs cover ----------------
  const man = (fill) => `<g><circle cx="0" cy="-118" r="30" fill="${fill}" ${O(4)}/><path d="M-34,-150Q0,-176 34,-150L36,-128H-36Z" fill="#5a6a3a" ${O(4)}/>
    <path d="M-26,-86Q-40,-40 -30,0H34Q40,-50 24,-86Q0,-96 -26,-86Z" fill="#6a7a46" ${O(4)}/><path d="M-30,0L-60,34L-20,40M30,0L50,40" stroke="${INK}" stroke-width="16" stroke-linecap="round" fill="none"/>
    <path d="M-30,0L-60,34L-20,40M30,0L50,40" stroke="#5e6e3e" stroke-width="10" stroke-linecap="round" fill="none"/><path d="M-20,-70Q-50,-80 -40,-120" stroke="#6a7a46" stroke-width="16" stroke-linecap="round" fill="none"/></g>`;
  WarUI.cover = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), Y = o.y ?? 470, r = mk(13), PW = 940, PH = 470;
    const panel = (py, good) => {
      const gid = `${id}-${good ? "g" : "b"}`;
      let leaves = ""; if (!good) for (let j = 0; j < 8; j++) leaves += `<g transform="translate(${f1(560 + (r() - 0.5) * 60)},${f1(210 + (r() - 0.5) * 40)})"><g id="${gid}-l${j}" opacity="0"><path d="M0,-12Q12,0 0,14Q-12,0 0,-12Z" fill="${j % 2 ? "#7aa244" : "#4a7a30"}" ${O(1.4)}/></g></g>`;
      let chips = ""; if (good) for (let j = 0; j < 7; j++) chips += `<g transform="translate(600,210)"><g id="${gid}-p${j}" opacity="0"><path d="M-6,-4L6,-6L8,4L-4,6Z" fill="${j % 2 ? "#c8a070" : "#8a6644"}" ${O(1.2)}/></g></g>`;
      return `<g transform="translate(70,${py})">
        <rect width="${PW}" height="${PH}" rx="34" fill="${good ? "url(#wyPanelG)" : "url(#wyPanelR)"}" ${O(5)}/>
        <path d="M30,380Q470,360 910,382V440Q470,452 30,440Z" fill="#9a7a4a" opacity=".9"/><path d="M30,380Q470,360 910,382" stroke="${INK}" stroke-width="4" fill="none"/>
        ${War.grass(40, 900, 384, 40, mk(good ? 3 : 4), TONES.day, { n: 5, step: 40, amp: 0 })}
        <g transform="translate(330,382) scale(1.05)">${man("#c8946a")}</g>
        ${good ? `<g transform="translate(600,382)"><path d="M-70,0Q-60,-180 -52,-330H52Q60,-180 70,0Z" fill="url(#wyBark)" ${O(4)}/><path d="M-30,-40Q-24,-180 -20,-300M20,-60Q16,-200 24,-300" stroke="#2a1e14" stroke-width="4" opacity=".5" fill="none"/>
            <path d="M-52,-330Q0,-350 52,-330" stroke="${INK}" stroke-width="4" fill="#6a4a30"/><g id="${gid}-imp" opacity="0"><circle cx="72" cy="-172" r="40" fill="url(#wyPuff)"/><path d="M70,-172l-14,-8l4,8l-8,6z" fill="#fff6c0"/></g></g>`
          : War.bushHTML(560, 382, "", 0.62, { seed: 9 })}
        <g transform="translate(0,210)"><g id="${gid}-bl" opacity="0"><path d="M0,-6L240,-2L240,2L0,6Z" fill="url(#wyTrail)"/><ellipse rx="16" ry="6" fill="#fff"/></g></g>${leaves}${chips}
        <g transform="translate(${PW / 2},0)"><g id="${gid}-hd"><rect x="-150" y="-36" width="300" height="72" rx="36" fill="${good ? "#2fa864" : "#e2382e"}" ${O(4)}/><text y="16" font-family="Kanit" font-weight="900" font-size="44" fill="#fff" text-anchor="middle">${good ? "กันกระสุน" : "บังตา"}</text></g></g>
        <g transform="translate(${PW - 90},110)"><circle id="${gid}-glow" r="60" fill="url(#rbOkGlow)" opacity="0"/><g id="${gid}-mk" opacity="0"><circle r="54" fill="${good ? "#2fb864" : "#e2382e"}" stroke="#fff" stroke-width="7"/>
          ${good ? `<path d="M-24,0l15,17l32,-36" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/>` : `<path d="M-20,-20L20,20M20,-20L-20,20" stroke="#fff" stroke-width="12" stroke-linecap="round"/>`}</g></g></g>`;
    };
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-in"><g transform="translate(0,${Y})">${panel(0, false)}${panel(PH + 40, true)}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.12, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { scaleX: 0.7, scaleY: 1.2, y: 140, transformOrigin: "50% 50%" }, { scaleX: 1, scaleY: 1, y: 0, transformOrigin: "50% 50%", duration: 0.7, ease: "elastic.out(1,0.55)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { y: 0 }, { y: -8, duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.7);
    ["b", "g"].forEach((p, k) => { const pid = `${id}-${p}`, tb = t0 + 0.6 + k * 0.9;
      tl.fromTo(`#${pid}-hd`, { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, transformOrigin: "50% 50%", duration: 0.4, ease: "back.out(2.5)", immediateRender: false }, t0 + 0.25 + k * 0.12);
      // the bullet from the right edge to the man (bush) or to the trunk (cover)
      tl.fromTo(`#${pid}-bl`, { x: 960, opacity: 1 }, { keyframes: [{ x: p === "b" ? 380 : 660, duration: 0.28, ease: "none" }, { opacity: 0, duration: 0.05 }], immediateRender: false }, tb);
      if (p === "b") { for (let j = 0; j < 8; j++) { const a = Math.PI + (r() - 0.5) * 1.8, v = 50 + r() * 90; tl.fromTo(`#${pid}-l${j}`, { x: 0, y: 0, rotation: 0, opacity: 1 }, { x: Math.cos(a) * v, y: Math.sin(a) * v + 40, rotation: 260, opacity: 0, duration: 0.9, ease: "power2.out", immediateRender: false }, tb + 0.14); }
        RabFX.flash(tl, tb + 0.3, "#ff2a1a", 0.25); RabFX.shakeSel(tl, `#${id}-in`, tb + 0.3, 12); }
      else { tl.fromTo(`#${pid}-imp`, { opacity: 1, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 0, scale: 1.6, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.out", immediateRender: false }, tb + 0.28);
        for (let j = 0; j < 7; j++) { const a = (r() - 0.5) * 1.6, v = 40 + r() * 70; tl.fromTo(`#${pid}-p${j}`, { x: 0, y: 0, rotation: 0, opacity: 1 }, { x: Math.cos(a) * v, y: Math.sin(a) * v + 50, rotation: 300, opacity: 0, duration: 0.7, ease: "power2.out", immediateRender: false }, tb + 0.28); } }
      tl.fromTo(`#${pid}-mk`, { scale: 2.6, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, tb + 0.34);
      if (p === "g") tl.fromTo(`#${pid}-glow`, { scale: 0.4, opacity: 1, transformOrigin: "50% 50%" }, { scale: 2.4, opacity: 0, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.out", immediateRender: false }, tb + 0.42);
      if (p === "b") tl.fromTo(`#${pid}-mk`, { rotation: -14, transformOrigin: "50% 50%" }, { rotation: 0, transformOrigin: "50% 50%", duration: 0.5, ease: "elastic.out(1.4,0.3)", immediateRender: false }, tb + 0.6);
    });
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };
})();
