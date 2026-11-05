// ---------- นิวเคลียร์ลงกรุงเทพ · hook stills (lane A experiment, 2 Nov): a nuclear flash over Bangkok seen from a jammed expressway ----------
//   Sets.xway(L, o)      sunset expressway in one-point perspective toward a generic skyline (no landmarks): jammed cars seen from behind
//                        with brake lights, concrete barriers, light poles, a sign gantry. o.H horizon y · o.VX vanishing x · o.flash 0..1
//                        how much the blast light floods the sky · o.blast {stage, s, dy} drawn between the sky and the towers ·
//                        o.shadows long shadows toward the camera · o.skip [[lane, d]] gaps where people stand · o.tilt [[lane, d, deg]]
//                        cars swerving · o.honk [[lane, d]] horn marks
//   Sets.xwayBack(L, o)  the reverse view behind a close-up: glass towers mirroring the fireball many times, a hot white-orange sky
//   Nk.blastHTML(x, y, s, stage)  "flash" · "rise" · "mush": fireball, stem, condensation rings and the dust skirt
//   Nk.bloom(layer, x, y, r, op)  a screen-blended white-gold bloom (use on L.light)
//   Nk.birds(layer, box, n, seed) a fleeing flock
(function () {
  const INK = "#14181a", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const blob = Pop2.blob;
  const dk = (hex, k = 0.72) => { const n = parseInt(hex.slice(1), 16); return `rgb(${[n >> 16, (n >> 8) & 255, n & 255].map((v) => Math.round(v * k)).join(",")})`; };
  Sets.DEFS += `
    <linearGradient id="nkSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#262a58"/><stop offset=".42" stop-color="#9a5a74"/><stop offset=".72" stop-color="#f09a5a"/><stop offset="1" stop-color="#ffdf9a"/></linearGradient>
    <linearGradient id="nkSkyHot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a3e3e"/><stop offset=".45" stop-color="#ffa45a"/><stop offset="1" stop-color="#fff4cf"/></linearGradient>
    <radialGradient id="nkFire"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#fff6c8"/><stop offset=".6" stop-color="#ffc35a"/><stop offset=".85" stop-color="#ff7a2a"/><stop offset="1" stop-color="#c2381a"/></radialGradient>
    <radialGradient id="nkBloom"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset=".22" stop-color="#fff4cf" stop-opacity=".9"/><stop offset=".55" stop-color="#ffc878" stop-opacity=".4"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></radialGradient>
    <radialGradient id="nkCapGlow" cx=".5" cy=".8" r=".7"><stop offset="0" stop-color="#ffe9a8"/><stop offset=".35" stop-color="#ff9a4a"/><stop offset=".75" stop-color="#b4502e"/><stop offset="1" stop-color="#5a2e2a"/></radialGradient>
    <linearGradient id="nkStem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3428"/><stop offset=".42" stop-color="#e8884a"/><stop offset=".55" stop-color="#ffd08a"/><stop offset=".7" stop-color="#e8884a"/><stop offset="1" stop-color="#4a2a24"/></linearGradient>
    <linearGradient id="nkRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a08a84"/><stop offset=".35" stop-color="#6a5e60"/><stop offset="1" stop-color="#2e2a2e"/></linearGradient>
    <linearGradient id="nkWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2d6c8"/><stop offset="1" stop-color="#8a8078"/></linearGradient>
    <radialGradient id="nkTail"><stop offset="0" stop-color="#ff6a52" stop-opacity=".95"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
    <linearGradient id="nkTower" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a2e4e"/><stop offset="1" stop-color="#241e36"/></linearGradient>
    <linearGradient id="nkGlass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a7aa0"/><stop offset=".6" stop-color="#3a4668"/><stop offset="1" stop-color="#262c48"/></linearGradient>
    <radialGradient id="nkSun"><stop offset="0" stop-color="#fffbe8"/><stop offset=".45" stop-color="#ffd27a"/><stop offset="1" stop-color="#ff8a3a" stop-opacity="0"/></radialGradient>
    <linearGradient id="nkSkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f9ccb"/><stop offset=".55" stop-color="#bfd0dc"/><stop offset="1" stop-color="#f1e6cc"/></linearGradient>
    <radialGradient id="nkDust"><stop offset="0" stop-color="#c88a5a" stop-opacity=".95"/><stop offset="1" stop-color="#7a4a3a" stop-opacity="0"/></radialGradient>`;
  const Nk = {};
  const PAL = ["#eef0f2", "#c9ced4", "#2a2e34", "#b8262a", "#e8559a", "#9ccc3c", "#3a5a8a", "#d8c8a8", "#5a5e64", "#f2f2ee"];

  // a car seen from behind; (x, y) = where the tyres touch the road
  Nk.car = (x, y, s, col, o = {}) => {
    const roof = dk(col, 0.84), low = dk(col, 0.58);
    let g = `<g transform="translate(${f1(x)},${f1(y)}) rotate(${o.rot || 0}) scale(${s.toFixed(3)})">
      <rect x="-134" y="-16" width="46" height="24" rx="6" fill="#111"/><rect x="88" y="-16" width="46" height="24" rx="6" fill="#111"/>
      <path d="M-146,-22L-150,-98Q-146,-130 -112,-136H112Q146,-130 150,-98L146,-22Q144,-2 120,-2H-120Q-144,-2 -146,-22Z" fill="${col}" ${O(5)}/>
      <path d="M-108,-136L-90,-208Q-84,-224 -62,-226H62Q84,-224 90,-208L108,-136Z" fill="${roof}" ${O(5)}/>
      <path d="M-88,-142L-74,-202H74L88,-142Z" fill="#2a3442" ${O(4)}/><path d="M-58,-192L-32,-152M-30,-194L-14,-168" stroke="#c8d8e8" stroke-width="6" opacity=".45" stroke-linecap="round"/>
      <rect x="-144" y="-114" width="52" height="28" rx="7" fill="#e2322a" ${O(3)}/><rect x="92" y="-114" width="52" height="28" rx="7" fill="#e2322a" ${O(3)}/>
      <rect x="-40" y="-80" width="80" height="32" rx="4" fill="#f4f2ea" ${O(3)}/><path d="M-26,-64h52" stroke="${INK}" stroke-width="4"/>
      <rect x="-148" y="-42" width="296" height="24" rx="9" fill="${low}" ${O(3)}/>
      <path d="M-138,-100Q0,-114 138,-100" stroke="#fff6dc" stroke-width="6" opacity=".45" fill="none"/>
      <path d="M-100,-222Q0,-232 100,-222" stroke="#fff2c8" stroke-width="7" opacity=".7" fill="none"/>`;
    if (o.taxi) g += `<rect x="-48" y="-256" width="96" height="30" rx="8" fill="#f2d22a" ${O(3)}/><text x="0" y="-234" font-family="Kanit" font-weight="900" font-size="20" text-anchor="middle" fill="${INK}">TAXI</text>`;
    return g + `</g>`;
  };
  const tails = (x, y, s, rot = 0) => `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot}) scale(${s.toFixed(3)})"><circle cx="-118" cy="-100" r="80" fill="url(#nkTail)"/><circle cx="118" cy="-100" r="80" fill="url(#nkTail)"/></g>`;

  // the blast: stage "flash" (the first instant), "rise" (fireball lifting on its stem), "mush" (the full mushroom)
  Nk.blastHTML = (x, y, s, stage = "flash", seed = 11) => {
    const r = mk(seed); let g = `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">`;
    const smoke = (cx, cy, R, n, cols, op = 1) => { let h = ""; for (let k = 0; k < n; k++) { const a = r() * Math.PI * 2, d = R * (0.35 + r() * 0.65);
        h += `<path d="${blob(cx + Math.cos(a) * d, cy + Math.sin(a) * d * 0.55, R * (0.28 + r() * 0.3), r, 9)}" fill="${cols[k % cols.length]}" opacity="${op}"/>`; } return h; };
    if (stage === "flash") {
      g += `<circle cx="0" cy="-60" r="1100" fill="url(#nkBloom)"/>
        <ellipse cx="0" cy="-60" rx="1500" ry="34" fill="#ffffff" opacity=".85"/><ellipse cx="0" cy="-60" rx="900" ry="12" fill="#ffffff"/>
        <circle cx="0" cy="-60" r="190" fill="url(#nkFire)"/><circle cx="0" cy="-60" r="120" fill="#ffffff"/>
        <ellipse cx="0" cy="10" rx="620" ry="70" fill="url(#nkBloom)"/>`;
    } else if (stage === "rise") {
      g += `<circle cx="0" cy="-380" r="900" fill="url(#nkBloom)" opacity=".75"/>
        <path d="M-70,0Q-40,-160 -60,-300H60Q40,-160 70,0Z" fill="url(#nkStem)" ${O(4)}/>
        ${smoke(0, -10, 260, 14, ["#a86a4a", "#8a5440", "#c88a5a"])}
        <ellipse cx="0" cy="-250" rx="330" ry="44" fill="#fff4e0" opacity=".55"/>
        ${smoke(0, -400, 210, 16, ["#ff9a4a", "#ffc35a", "#e8703a"])}<circle cx="0" cy="-400" r="170" fill="url(#nkFire)"/>`;
    } else {
      // the mushroom: dust skirt, stem with turbulence, two condensation rings, the cap (dark smoke outside, glowing underneath)
      g += `<circle cx="0" cy="-700" r="1000" fill="url(#nkBloom)" opacity=".38"/>
        <ellipse cx="0" cy="-20" rx="1100" ry="120" fill="url(#nkDust)" opacity=".9"/>${smoke(0, -40, 520, 26, ["#9a6448", "#7a4c3a", "#b47a52", "#8a5a44"])}
        <path d="M-150,-40Q-90,-260 -96,-520Q-110,-660 -60,-760H60Q110,-660 96,-520Q90,-260 150,-40Z" fill="url(#nkStem)" ${O(5)}/>
        ${smoke(0, -420, 120, 12, ["#c87a4a", "#e8a05a", "#a85a3a"], 0.85)}
        <ellipse cx="0" cy="-470" rx="430" ry="58" fill="none" stroke="#fff4e6" stroke-width="26" opacity=".55"/>
        <ellipse cx="0" cy="-300" rx="620" ry="70" fill="none" stroke="#fff4e6" stroke-width="14" opacity=".3"/>
        ${smoke(0, -880, 470, 30, ["#4a2e2c", "#5e3a32", "#3a2426", "#6e4434"])}
        ${smoke(0, -830, 330, 22, ["#b4562e", "#d8743a", "#9a4a2e"])}
        <ellipse cx="0" cy="-790" rx="380" ry="190" fill="url(#nkCapGlow)"/><circle cx="0" cy="-740" r="120" fill="url(#nkFire)" opacity=".85"/>${smoke(0, -760, 190, 12, ["#ffb45a", "#ff8a3a", "#ffd27a"], 0.9)}
        <path d="M-420,-960Q-200,-1080 0,-1070Q220,-1080 420,-960" stroke="#ffdcb0" stroke-width="16" opacity=".35" fill="none"/>`;
    }
    return g + `</g>`;
  };
  Nk.bloom = (layer, x, y, R, op = 0.5) => put(layer, `<circle cx="${x}" cy="${y}" r="${R}" fill="url(#nkBloom)" opacity="${op}" style="mix-blend-mode:screen"/>`);
  Nk.birds = (layer, box, n = 12, seed = 5) => { const r = mk(seed), [bx, by, bw, bh] = box; let g = "";
    for (let k = 0; k < n; k++) { const x = bx + r() * bw, y = by + r() * bh, w = 14 + r() * 16;
      g += `<path d="M${f1(x - w)},${f1(y - w * 0.3)}Q${f1(x - w * 0.4)},${f1(y - w * 0.5)} ${f1(x)},${f1(y)}Q${f1(x + w * 0.4)},${f1(y - w * 0.5)} ${f1(x + w)},${f1(y - w * 0.3)}" stroke="#1e1620" stroke-width="${f1(3 + w * 0.12)}" fill="none" stroke-linecap="round"/>`; }
    put(layer, `<g>${g}</g>`); };
  const honk = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s.toFixed(3)})" stroke="#fff6dc" stroke-width="9" stroke-linecap="round" fill="none" opacity=".95"><path d="M-170,-250l-60,-50M-190,-190l-80,-10M170,-250l60,-50M190,-190l80,-10M0,-290v-70"/></g>`;

  // generic towers along the horizon; the faces that look at the blast catch its light
  const towers = (r, H, VX, hot, n = 26, reflect = false, gap = 0) => { let t = "";
    for (let k = 0; k < n; k++) { const x = -320 + k * 66 + r() * 40, w = 60 + r() * 110, near = 1 - Math.min(1, Math.abs(x + w / 2 - VX) / 760);
      const h = (120 + r() * 300 + near * 260 + (k % 7 === 3 ? 220 : 0)) * (1 - gap * near ** 2), y = H - h, lit = x + w / 2 < VX ? x + w - 10 : x;
      t += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h + 30)}" fill="url(#nkTower)"/>`;
      for (let j = 0; j < Math.floor(h / 34); j++) t += `<rect x="${f1(x + 8)}" y="${f1(y + 14 + j * 34)}" width="${f1(w - 16)}" height="6" fill="#ffcf8a" opacity="${f1(0.08 + r() * 0.22)}"/>`;
      t += `<rect x="${f1(lit)}" y="${f1(y)}" width="10" height="${f1(h + 30)}" fill="#ffe6b0" opacity="${f1(0.35 + hot * 0.55)}"/>`;
      if (reflect && r() < 0.5) t += `<circle cx="${f1(x + w / 2)}" cy="${f1(y + h * (0.2 + r() * 0.5))}" r="${f1(10 + r() * 14)}" fill="url(#nkSun)"/>`;
      if (k % 9 === 4) t += `<rect x="${f1(x + w / 2 - 3)}" y="${f1(y - 60)}" width="6" height="60" fill="#241e36"/><circle cx="${f1(x + w / 2)}" cy="${f1(y - 62)}" r="7" fill="#ff4a3a"/>`; }
    return t; };

  Sets.xway = (L, o = {}) => {
    const id = o.id || "xw", r = mk(o.seed || 7), H = o.H ?? 1000, VX = o.VX ?? 540, hot = o.flash ?? 0, Y = (d) => H + (1960 - H) * d;
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${o.day ? "nkSkyDay" : "nkSky"})"/>`;
    if (hot) sky += `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#nkSkyHot)" opacity="${hot}"/>`;
    for (let k = 0; k < 8; k++) { const y = 160 + k * 92 + r() * 30; sky += `<path d="${blob(-260 + r() * 1600, y, 150 + r() * 160, r, 9)}" fill="${o.day ? "#ffffff" : hot > 0.5 ? "#ffe0b0" : "#e8a07a"}" opacity="${o.day ? 0.45 : 0.3}"/>`; }
    put(L.sky, sky);
    let far = o.blast ? Nk.blastHTML(VX + (o.blast.dx ?? 0), H + (o.blast.dy ?? 0), o.blast.s ?? 1, o.blast.stage, o.blast.seed || 11) : "";
    far += towers(r, H + 20, VX, hot, 26, false, o.gap || 0) + `<rect x="-1300" y="${H}" width="3700" height="60" fill="#2a2236"/>`;
    put(L.far, far);
    // the deck: road, lane dashes, barriers, poles, a sign gantry
    const ex = (off, d) => VX + off * d;
    let s = `<path d="M${ex(-1000, 0.004)},${H}L${ex(1000, 0.004)},${H}L${ex(1000, 1.1)},${Y(1.1)}L${ex(-1000, 1.1)},${Y(1.1)}Z" fill="url(#nkRoad)"/>`;
    [-330, 330].forEach((off) => { for (let k = 0; k < 14; k++) { const d0 = 0.03 * 1.33 ** k, d1 = d0 * 1.14; if (d0 > 1.1) break;
      s += `<path d="M${f1(ex(off - 8, d0))},${f1(Y(d0))}L${f1(ex(off + 8, d0))},${f1(Y(d0))}L${f1(ex(off + 8, d1))},${f1(Y(d1))}L${f1(ex(off - 8, d1))},${f1(Y(d1))}Z" fill="#f4efe0" opacity=".8"/>`; } });
    [-1, 1].forEach((sd) => { const a = sd * 1000, b = sd * 1080;
      s += `<path d="M${ex(a, 0.004)},${H}L${ex(a, 1.1)},${Y(1.1)}L${ex(b, 1.1)},${Y(1.1) - 200 * 1.1}L${ex(b, 0.004)},${H - 1}Z" fill="url(#nkWall)" ${O(3)}/>`;
      for (let k = 0; k < 9; k++) { const d = 0.05 * 1.45 ** k; if (d > 1.1) break; const px = ex(sd * 1060, d), py = Y(d) - 190 * d;
        s += `<rect x="${f1(px - 7 * d)}" y="${f1(py - 820 * d)}" width="${f1(14 * d)}" height="${f1(820 * d)}" fill="#c8c0b8" ${O(2)}/><path d="M${f1(px)},${f1(py - 812 * d)}L${f1(px - sd * 140 * d)},${f1(py - 836 * d)}" stroke="#c8c0b8" stroke-width="${f1(12 * d)}"/><rect x="${f1(px - sd * 150 * d - 18 * d)}" y="${f1(py - 846 * d)}" width="${f1(36 * d)}" height="${f1(14 * d)}" fill="#fff2c8"/>`; } });
    const gd = o.gantry ?? 0.2; if (gd) { const gy = Y(gd) - 900 * gd;
      s += `<rect x="${f1(ex(-1060, gd))}" y="${f1(gy)}" width="${f1(2120 * gd)}" height="${f1(40 * gd)}" fill="#8a8480" ${O(2)}/>
        <rect x="${f1(ex(-560, gd))}" y="${f1(gy + 30 * gd)}" width="${f1(1120 * gd)}" height="${f1(230 * gd)}" rx="${f1(14 * gd)}" fill="#1e7a4a" stroke="#f4f2ea" stroke-width="${f1(10 * gd)}"/>
        <text x="${VX}" y="${f1(gy + 160 * gd)}" font-family="Kanit" font-weight="800" font-size="${f1(110 * gd)}" fill="#f4f2ea" text-anchor="middle">ทางพิเศษ ↑ ใจกลางเมือง</text>`; }
    // the jam: three lanes, far to near; gaps where people stand; some swerve, some honk
    const lanes = [-660, 0, 660], ds = [0.05, 0.065, 0.085, 0.11, 0.145, 0.19, 0.25, 0.33, 0.44, 0.58, 0.76, 0.98];
    const skip = o.skip || [], tilt = o.tilt || [], hk = o.honk || [];
    let shad = "", cars = "", glow = "", k = 0;
    ds.forEach((d) => lanes.forEach((off, li) => { k++;
      if (skip.some(([l, dd]) => l === li && Math.abs(dd - d) < 0.005) || d > (o.maxD ?? 0.98)) return;
      const tl = tilt.find(([l, dd]) => l === li && Math.abs(dd - d) < 0.005), rot = tl ? tl[2] : 0, jx = tl ? tl[3] || 0 : 0;
      const x = ex(off, d) + jx * d, y = Y(d), sc = d * 1.25, col = PAL[(k * 7 + li * 3) % PAL.length];
      if (o.shadows) { const vx = x - VX, vy = y - H, len = 0.55; shad += `<path d="M${f1(x - 150 * sc)},${f1(y)}L${f1(x + 150 * sc)},${f1(y)}L${f1(x + 150 * sc + vx * len)},${f1(y + vy * len)}L${f1(x - 150 * sc + vx * len)},${f1(y + vy * len)}Z" fill="#1a1020" opacity=".35"/>`; }
      cars += Nk.car(x, y, sc, col, { taxi: (k % 5) === 2, rot });
      glow += tails(x, y, sc, rot);
      if (hk.some(([l, dd]) => l === li && Math.abs(dd - d) < 0.005)) glow += honk(x, y, sc);
    }));
    put(L.set, s + shad + cars);
    put(L.glow, `<g opacity="${o.tailOp ?? 0.85}">${glow}</g>`);
  };

  // behind the close-up: tall glass towers that each mirror the fireball, the hot sky, a strip of barrier and car roofs
  Sets.xwayBack = (L, o = {}) => {
    const r = mk(o.seed || 19), H = o.H ?? 1500;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#nkSkyHot)"/><circle cx="540" cy="200" r="1300" fill="url(#nkBloom)" opacity=".6"/>`);
    let t = "";
    for (let k = 0; k < 12; k++) { const x = -300 + k * 150 + r() * 50, w = 140 + r() * 120, h = 700 + r() * 700, y = H - h;
      t += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h + 40)}" fill="url(#nkGlass)" ${O(3)}/>`;
      for (let j = 0; j < Math.floor(h / 70); j++) t += `<path d="M${f1(x)},${f1(y + 40 + j * 70)}h${f1(w)}" stroke="#1e2440" stroke-width="5"/>`;
      for (let j = 0; j < 3; j++) t += `<circle cx="${f1(x + w * (0.25 + r() * 0.5))}" cy="${f1(y + 100 + r() * (h - 200))}" r="${f1(16 + r() * 22)}" fill="url(#nkSun)"/>`;
      t += `<rect x="${f1(x + w - 12)}" y="${f1(y)}" width="12" height="${f1(h + 40)}" fill="#ffe6b0" opacity=".55"/>`; }
    put(L.far, t);
    let s = `<rect x="-1300" y="${H}" width="3700" height="700" fill="#5a4e50"/><path d="M-1300,${H}H2400" stroke="#e2d6c8" stroke-width="40"/>`;
    for (let k = 0; k < 6; k++) { const x = -200 + k * 300 + r() * 60; s += `<path d="M${f1(x)},${H + 140}Q${f1(x + 20)},${H + 40} ${f1(x + 120)},${H + 30}H${f1(x + 230)}Q${f1(x + 320)},${H + 40} ${f1(x + 340)},${H + 140}Z" fill="${PAL[k % PAL.length]}" ${O(4)}/>`; }
    put(L.set, s);
  };
  Nk.reflect = (layer, pts, s = 0.12) => put(layer, `<g opacity=".92">${pts.map(([x, y, k]) => Nk.blastHTML(x, y, s * (k || 1), "rise", 21)).join("")}</g>`);
  Rig.MODES.shield = (u, o) => ({ ...Rig.MODES.idle(u, o), uaF: -100, faF: -112, uaB: 26, faB: -28, torso: -7, head: -9, bodyY: 4 });
  window.Nk = Nk;
})();
