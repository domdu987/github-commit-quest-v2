// Sets, props, cast and the life of the sea for ติดเกาะร้าง EP.1 "ผีอำ" (a fishing village on the Gulf, ยาย's porch by the water,
// the longtail boat, the rocky island with the shrine on its headland, the tide pool with the puffer fish, the campfire night, the
// paralysed first-person view from the sand, the dawn). Same layer contract as sets.js / fence.js (sky far mid set act fg + glow);
// load after estate7.js. Everything that moves (waves, foam, glitter, plankton, stars, clouds, lightning, fire, smoke, the fish's
// fins) carries a class and is driven by Isle.life(tl, scope, t0, dur, o).
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const O = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);
  const T = (x, y, txt, size, col, o = {}) => `<text x="${x}" y="${y}" text-anchor="${o.anchor || "middle"}" font-family="Kanit" font-weight="${o.w || 900}" font-size="${size}" fill="${col}"${o.extra || ""}>${txt}</text>`;

  Sets.DEFS += `
    <linearGradient id="iMorn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb3d6"/><stop offset=".55" stop-color="#bfe0ea"/><stop offset="1" stop-color="#f6e6cf"/></linearGradient>
    <linearGradient id="iDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2446"/><stop offset=".42" stop-color="#7a3f66"/><stop offset=".72" stop-color="#e07a4c"/><stop offset="1" stop-color="#ffc28a"/></linearGradient>
    <linearGradient id="iNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#040812"/><stop offset=".6" stop-color="#0d1a33"/><stop offset="1" stop-color="#1a2d4e"/></linearGradient>
    <linearGradient id="iDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2a4f"/><stop offset=".5" stop-color="#6a6a9a"/><stop offset=".78" stop-color="#f0a070"/><stop offset="1" stop-color="#ffd9a0"/></linearGradient>
    <linearGradient id="iSeaMorn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb8cc"/><stop offset="1" stop-color="#3f8aa6"/></linearGradient>
    <linearGradient id="iSeaDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e59a6a"/><stop offset=".3" stop-color="#8a5a7a"/><stop offset="1" stop-color="#2d3a5c"/></linearGradient>
    <linearGradient id="iSeaNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16274a"/><stop offset="1" stop-color="#0a1428"/></linearGradient>
    <linearGradient id="iSeaDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0b080"/><stop offset=".35" stop-color="#7a7aa0"/><stop offset="1" stop-color="#2a3a5c"/></linearGradient>
    <linearGradient id="iSandDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9d9b4"/><stop offset="1" stop-color="#d2bf94"/></linearGradient>
    <linearGradient id="iSandDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9a37e"/><stop offset="1" stop-color="#9c7a5e"/></linearGradient>
    <linearGradient id="iSandNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4256"/><stop offset="1" stop-color="#262c3c"/></linearGradient>
    <linearGradient id="iSandDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7a7a"/><stop offset="1" stop-color="#5a5260"/></linearGradient>
    <linearGradient id="iRock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8d8a84"/><stop offset="1" stop-color="#4e4a46"/></linearGradient>
    <linearGradient id="iRockN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c4252"/><stop offset="1" stop-color="#1c2030"/></linearGradient>
    <linearGradient id="iRockD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a5a66"/><stop offset="1" stop-color="#342c3a"/></linearGradient>
    <radialGradient id="iPoolW" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#8fd8e0"/><stop offset=".6" stop-color="#3f9fb0"/><stop offset="1" stop-color="#1f6a7a"/></radialGradient>
    <radialGradient id="iPoolD" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#5aa8b8"/><stop offset=".6" stop-color="#2a6a7c"/><stop offset="1" stop-color="#143a46"/></radialGradient>
    <radialGradient id="iMoonG"><stop offset="0" stop-color="#f6f9ff" stop-opacity=".95"/><stop offset=".18" stop-color="#cfdcf4" stop-opacity=".35"/><stop offset="1" stop-color="#cfdcf4" stop-opacity="0"/></radialGradient>
    <radialGradient id="iSunG"><stop offset="0" stop-color="#fff2c8" stop-opacity=".95"/><stop offset=".25" stop-color="#ffb060" stop-opacity=".45"/><stop offset="1" stop-color="#ff9040" stop-opacity="0"/></radialGradient>
    <radialGradient id="iFireG"><stop offset="0" stop-color="#ffd27a" stop-opacity=".55"/><stop offset=".45" stop-color="#ff8a3c" stop-opacity=".16"/><stop offset="1" stop-color="#ff8a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="iLampG"><stop offset="0" stop-color="#fff0c0" stop-opacity=".8"/><stop offset=".35" stop-color="#ffc050" stop-opacity=".22"/><stop offset="1" stop-color="#ffc050" stop-opacity="0"/></radialGradient>
    <radialGradient id="iBioG"><stop offset="0" stop-color="#9cf5ff" stop-opacity=".9"/><stop offset="1" stop-color="#2ad0e8" stop-opacity="0"/></radialGradient>
    <radialGradient id="iEye"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset=".8" stop-color="#000" stop-opacity=".75"/><stop offset="1" stop-color="#000" stop-opacity="1"/></radialGradient>
    <linearGradient id="iHull" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f6aa8"/><stop offset=".55" stop-color="#2d4f82"/><stop offset=".56" stop-color="#c8392b"/><stop offset="1" stop-color="#8f2a20"/></linearGradient>
    <linearGradient id="iPlank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8865a"/><stop offset="1" stop-color="#6e5433"/></linearGradient>
    <linearGradient id="iPuff" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a8a4e"/><stop offset=".55" stop-color="#b9b073"/><stop offset=".6" stop-color="#f4f0dc"/><stop offset="1" stop-color="#e3dcc2"/></linearGradient>
    <pattern id="iCaust" width="90" height="70" patternUnits="userSpaceOnUse"><path d="M0,35q22,-30 45,0t45,0M0,0q22,30 45,0t45,0M0,70q22,-30 45,0t45,0" fill="none" stroke="#dffcff" stroke-width="3" stroke-opacity=".5"/></pattern>
    <pattern id="iGrain" width="40" height="40" patternUnits="userSpaceOnUse"><circle cx="6" cy="8" r="1.4" fill="#000" opacity=".12"/><circle cx="22" cy="30" r="1.1" fill="#fff" opacity=".18"/><circle cx="33" cy="12" r="1.2" fill="#000" opacity=".1"/><circle cx="12" cy="24" r=".9" fill="#fff" opacity=".14"/></pattern>
    <filter id="iSoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="iSoft6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>`;

  const SKY = { morning: "iMorn", day: "iMorn", dusk: "iDusk", night: "iNight", dawn: "iDawn" };
  const SEA = { morning: "iSeaMorn", day: "iSeaMorn", dusk: "iSeaDusk", night: "iSeaNight", dawn: "iSeaDawn" };
  const SAND = { morning: "iSandDay", day: "iSandDay", dusk: "iSandDusk", night: "iSandNight", dawn: "iSandDawn" };
  const ROCK = { morning: "iRock", day: "iRock", dusk: "iRockD", night: "iRockN", dawn: "iRockD" };
  const WAVEC = { morning: "#dff2f6", day: "#dff2f6", dusk: "#ffd0a0", night: "#6a86b8", dawn: "#ffd0a8" };

  // ======================================================================================================
  // sky, sea, sand — the pieces every set shares
  // ======================================================================================================
  const sky = (L, t, o = {}) => put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="url(#${SKY[t]})"/>`);
  function stars(L, seed, n = 110, o = {}) {
    const r = mk(seed); let s = "";
    for (let k = 0; k < n; k++) { const x = -1200 + r() * 3400, y = -800 + r() * (o.h || 1600), rr = 0.9 + r() * 2.2, op = 0.3 + r() * 0.65;
      s += `<circle class="${k % 4 === 0 ? "star" : ""}" cx="${f1(x)}" cy="${f1(y)}" r="${f1(rr)}" fill="#e9f0ff" opacity="${f1(op)}"/>`; }
    // the milky band
    s += `<ellipse cx="300" cy="200" rx="1500" ry="260" fill="#9fb0e0" opacity=".06" transform="rotate(-28 300 200)" filter="url(#iSoft)"/>`;
    put(L.sky, s);
  }
  const moon = (L, x, y, r = 70, id = "moon") => put(L.sky, `<g id="${id}"><circle cx="${x}" cy="${y}" r="${r * 5}" fill="url(#iMoonG)"/><circle cx="${x}" cy="${y}" r="${r}" fill="#f4f7ff"/><circle cx="${x + r * 0.3}" cy="${y - r * 0.2}" r="${r * 0.85}" fill="#e3e9f7" opacity=".55"/><circle cx="${x - r * 0.25}" cy="${y + r * 0.3}" r="${r * 0.14}" fill="#cfd8ea" opacity=".6"/><circle cx="${x + r * 0.35}" cy="${y + r * 0.45}" r="${r * 0.1}" fill="#cfd8ea" opacity=".5"/></g>`);
  // clouds that drift (class cld): soft stacked ellipses, lit from the time's horizon colour; storm = low, dark, heavy on the right
  function clouds(L, seed, t, o = {}) {
    const r = mk(seed), night = t === "night", storm = o.storm, base = night ? "#1b2538" : t === "dusk" ? "#4a3458" : t === "dawn" ? "#5a5a84" : "#f3f6f8", lit = night ? "#2c3a54" : t === "dusk" ? "#ffb07a" : t === "dawn" ? "#ffc8a0" : "#ffffff";
    let s = "";
    for (let k = 0; k < (o.n || 9); k++) { const x = -900 + r() * 2900, y = (o.y0 ?? -500) + r() * (o.h || 900), w = 280 + r() * 460, op = storm ? 0.9 : 0.6 + r() * 0.35;
      s += `<g class="cld" opacity="${f1(op)}" data-sp="${f1(0.4 + r() * 0.8)}">${[[0, 0, 1], [-0.42, 0.14, 0.72], [0.4, 0.12, 0.78], [0.08, -0.2, 0.62], [-0.15, -0.12, 0.5]].map(([dx, dy, k2]) => `<ellipse cx="${f1(x + dx * w)}" cy="${f1(y + dy * w * 0.36)}" rx="${f1(w * 0.52 * k2)}" ry="${f1(w * 0.2 * k2)}" fill="${base}"/>`).join("")}<ellipse cx="${f1(x + 0.1 * w)}" cy="${f1(y + 0.1 * w * 0.3)}" rx="${f1(w * 0.44)}" ry="${f1(w * 0.09)}" fill="${lit}" opacity=".55"/></g>`; }
    if (storm) { // the wall of the squall: a dark bank low on the right with rain hanging under it
      s += `<g class="cld" data-sp=".3"><path d="M700,260Q1000,120 1400,200T2200,260L2300,620H700Z" fill="#241c34" opacity=".92"/><path d="M820,300Q1100,210 1500,250T2200,300" stroke="#5a4668" stroke-width="40" fill="none" opacity=".5" stroke-linecap="round"/>
        ${Array.from({ length: 26 }, (_, k) => `<path d="M${900 + k * 50},${600 + (k % 3) * 20}l-30,${260 + (k % 4) * 40}" stroke="#4a4a6a" stroke-width="6" opacity=".35"/>`).join("")}</g>`; }
    put(L.far, s);
  }
  // the open sea from the horizon y0 down to y1: a graded band with wave rows (class wv, further rows thinner and slower), the
  // horizon haze, optional moon or sun glitter (class glit) under x = gx, optional far islands
  function sea(L, t, y0, y1, o = {}) {
    const r = mk(o.seed || 11), col = WAVEC[t]; let s = `<rect x="-1500" y="${y0}" width="4200" height="${y1 - y0}" fill="url(#${SEA[t]})"/>`;
    s += `<rect x="-1500" y="${y0 - 6}" width="4200" height="60" fill="${t === "night" ? "#3a5080" : t === "dusk" ? "#ffc8a0" : t === "dawn" ? "#ffd8b0" : "#ffffff"}" opacity="${t === "night" ? 0.25 : 0.35}" filter="url(#iSoft6)"/>`;
    const rows = o.rows || 11;
    for (let k = 0; k < rows; k++) { const a = k / rows, y = y0 + 18 + a * a * (y1 - y0 - 40), amp = 2 + a * a * 22, len = 90 + a * 260, op = 0.14 + a * 0.5, w = 1.5 + a * 3.5; let d = `M-1500,${f1(y)}`;
      for (let x = -1500; x < 2700; x += len) d += `q${f1(len * 0.25)},${f1(-amp)} ${f1(len * 0.5)},0t${f1(len * 0.5)},0`;
      s += `<g class="wv" data-sp="${f1(0.5 + a * 1.2)}" data-amp="${f1(20 + a * 50)}"><path d="${d}" stroke="${col}" stroke-width="${f1(w)}" fill="none" opacity="${f1(op)}" stroke-linecap="round"/>${a > 0.55 ? `<path d="${d}" stroke="#ffffff" stroke-width="${f1(w * 2.6)}" fill="none" opacity="${f1(op * 0.22)}" stroke-dasharray="${f1(len * 0.3)} ${f1(len * 0.7)}" stroke-dashoffset="${f1(r() * len)}" class="foam"/>` : ""}</g>`; }
    if (o.glitter !== undefined) { const gx = o.glitter, gc = t === "night" ? "#dfe8ff" : "#ffe6b0";
      for (let k = 0; k < 70; k++) { const a = k / 70, y = y0 + 30 + a * a * (y1 - y0 - 60), sp = 40 + a * 320, x = gx + (r() - 0.5) * sp, w = 14 + a * 70;
        s += `<path class="glit" d="M${f1(x - w / 2)},${f1(y)}h${f1(w)}" stroke="${gc}" stroke-width="${f1(2 + a * 5)}" opacity="${f1(0.2 + r() * 0.6)}" stroke-linecap="round"/>`; } }
    put(L.far, s);
  }
  // sand from y0 down: a graded slab, grain, a scatter of shells and bits of weed, the dark wet band near the water at y = wet
  function sand(L, t, y0, o = {}) {
    const r = mk(o.seed || 13); let s = `<rect x="-1500" y="${y0}" width="4200" height="2200" fill="url(#${SAND[t]})"/><rect x="-1500" y="${y0}" width="4200" height="2200" fill="url(#iGrain)"/>`;
    for (let k = 0; k < (o.bits ?? 40); k++) { const x = -1300 + r() * 3800, y = y0 + 60 + r() * 900, q = r();
      s += q < 0.35 ? `<path d="M${f1(x)},${f1(y)}q6,-9 14,0q-4,6 -14,0z" fill="${t === "night" ? "#6a6f80" : "#f3ebdc"}" ${O(1.5)}/>` : q < 0.6 ? `<path d="M${f1(x)},${f1(y)}q14,-6 30,4" stroke="${t === "night" ? "#2a3a30" : "#5a6a3a"}" stroke-width="4" fill="none" stroke-linecap="round"/>` : `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(2 + r() * 3)}" fill="#000" opacity=".12"/>`; }
    put(L.set, s);
  }
  // the water's edge lapping across the lower frame (group #id-wash is slid up and down by life): a translucent wedge of sea with its
  // foam line, wet sheen above it, and at night the plankton that lights where the water moves (class bio)
  function wash(L, id, t, o = {}) {
    const r = mk(o.seed || 17), y = o.y ?? 1760, night = t === "night";
    let d = `M-1500,${y + 120}`; for (let x = -1500; x < 2700; x += 160) d += `q40,-28 80,0t80,0`; d += `L2700,3000H-1500Z`;
    let foam = `M-1500,${y + 120}`; for (let x = -1500; x < 2700; x += 160) foam += `q40,-28 80,0t80,0`;
    let s = `<g id="${id}-wash"><path d="${d.replace(y + 120, y + 60)}" fill="${night ? "#1c2c4a" : t === "dusk" ? "#4a3a5c" : "#6fb0c4"}" opacity=".35"/><path d="${d}" fill="url(#${SEA[t]})" opacity=".92"/>
      <path d="${foam}" stroke="#ffffff" stroke-width="12" fill="none" opacity="${night ? 0.5 : 0.85}" class="foam" stroke-linecap="round"/><path d="${foam.replace(y + 120, y + 150)}" stroke="#ffffff" stroke-width="5" fill="none" opacity=".35" class="foam" stroke-dasharray="40 70"/>`;
    if (night) for (let k = 0; k < 60; k++) { const x = -1200 + r() * 3600, yy = y + 100 + r() * 70; s += `<circle class="bio" cx="${f1(x)}" cy="${f1(yy)}" r="${f1(3 + r() * 7)}" fill="url(#iBioG)" opacity="${f1(r() * 0.8)}"/>`; }
    s += `</g>`;
    put(o.layer || L.set, s);
  }

  // ======================================================================================================
  // props
  // ======================================================================================================
  // a coconut palm: a curved tapering trunk with ring scars from (x, y) up to the crown, leaning `lean` px to the right at the top,
  // nine fronds that droop from the crown with leaflets along them, a cluster of nuts; origin = foot of the trunk
  function PALM(x, y, s = 1, lean = 120, seed = 3, o = {}) {
    const r = mk(seed), H = o.h || 820, night = o.night, dark = night ? "#0e1a1a" : "#2f5d34", mid = night ? "#15262a" : "#3f7a44", lite = night ? "#1c3034" : "#5a9a58", bark = night ? "#2a2420" : "#6b4a2e", barkL = night ? "#3a3028" : "#8a6a44";
    const cx = x + lean, cy = y - H;
    let g = `<g transform="translate(0,0)"><path d="M${x - 26},${y}Q${x - 10 + lean * 0.45},${y - H * 0.5} ${cx - 12},${cy}L${cx + 12},${cy}Q${x + 16 + lean * 0.45},${y - H * 0.5} ${x + 30},${y}Z" fill="${bark}" ${O(3)}/>`;
    for (let k = 1; k < 14; k++) { const a = k / 14, px = x + lean * a * a * 0.95 + (lean * a * (1 - a)) * 0.2, py = y - H * a, w = 30 - a * 12; g += `<path d="M${f1(px - w)},${f1(py)}q${f1(w)},${f1(-6)} ${f1(w * 2)},0" stroke="${barkL}" stroke-width="3" fill="none" opacity=".6"/>`; }
    const frond = (ang, len, curl) => { const a = ang * Math.PI / 180, ex = cx + Math.cos(a) * len, ey = cy + Math.sin(a) * len + curl, mx = cx + Math.cos(a) * len * 0.55, my = cy + Math.sin(a) * len * 0.55 - 30;
      let f = `<path d="M${cx},${cy}Q${f1(mx)},${f1(my)} ${f1(ex)},${f1(ey)}" stroke="${mid}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
      for (let i = 1; i <= 9; i++) { const t = i / 10, bx = (1 - t) * (1 - t) * cx + 2 * (1 - t) * t * mx + t * t * ex, by = (1 - t) * (1 - t) * cy + 2 * (1 - t) * t * my + t * t * ey, ll = 70 * (1 - t * 0.5), nx = -Math.sin(a), ny = Math.cos(a);
        f += `<path d="M${f1(bx)},${f1(by)}l${f1(nx * ll * 0.5 + Math.cos(a) * 14)},${f1(ny * ll * 0.5 + 24)}M${f1(bx)},${f1(by)}l${f1(-nx * ll * 0.5 + Math.cos(a) * 14)},${f1(-ny * ll * 0.5 + 24)}" stroke="${i % 2 ? dark : lite}" stroke-width="5" fill="none" stroke-linecap="round"/>`; }
      return f; };
    const fr = [-172, -150, -122, -95, -70, -45, -18, 8, 30].map((ang, i) => frond(ang + (r() - 0.5) * 10, 240 + r() * 90, 60 + i * 6)).join("");
    g += `<g class="frnd" style="transform-origin:${cx}px ${cy}px">${fr}${[[-18, 22], [6, 30], [26, 18]].map(([dx, dy]) => `<circle cx="${cx + dx}" cy="${cy + dy}" r="16" fill="${night ? "#2a2a1a" : "#8a7a3a"}" ${O(2.5)}/>`).join("")}</g></g>`;
    return `<g transform="scale(${s})" style="transform-origin:${x}px ${y}px">${g}</g>`;
  }
  // a boulder: a faceted rough shape w × h, origin = bottom centre; t picks the palette; barnacles near the foot when wet
  function BOULDER(x, y, w, h, seed, t = "day", o = {}) {
    const r = mk(seed), n = 9; let pts = [];
    for (let k = 0; k < n; k++) { const a = Math.PI + (k / (n - 1)) * Math.PI, rr = 0.82 + r() * 0.24; pts.push([x + Math.cos(a) * w * 0.5 * rr, y + Math.sin(a) * h * rr * (k === 0 || k === n - 1 ? 1 : 1)]); }
    const d = `M${f1(pts[0][0])},${y}` + pts.map(([px, py]) => `L${f1(px)},${f1(Math.min(y, py))}`).join("") + `L${f1(pts[n - 1][0])},${y}Z`;
    let g = `<path d="${d}" fill="url(#${ROCK[t]})" ${OUT}/><path d="${d}" fill="url(#iGrain)" opacity=".7"/>`;
    g += `<path d="M${f1(pts[2][0])},${f1(pts[2][1] + 10)}L${f1(x + w * 0.1)},${f1(y - h * 0.35)}L${f1(pts[6][0])},${f1(pts[6][1] + 12)}" stroke="#fff" stroke-opacity="${t === "night" ? 0.08 : 0.2}" stroke-width="10" fill="none" stroke-linejoin="round"/>`;
    g += `<path d="M${f1(x + w * 0.05)},${f1(y - h * 0.35)}L${f1(x + w * 0.3)},${f1(y - 10)}" stroke="#000" stroke-opacity=".18" stroke-width="14" fill="none"/>`;
    if (o.wet) for (let k = 0; k < 10; k++) g += `<circle cx="${f1(x - w * 0.4 + r() * w * 0.8)}" cy="${f1(y - 6 - r() * h * 0.3)}" r="${f1(3 + r() * 3)}" fill="#d9d2c0" opacity=".5"/>`;
    return g;
  }
  // the spirit shrine on the headland (ศาลเพียงตา): a post, a little gabled house with a red cloth, incense cups, the oil lamp on its
  // ledge (#id-lamp, lit = flame on, a thread of smoke .smk when o.smoke); origin = foot of the post
  function SHRINE(id, x, y, s = 1, o = {}) {
    const night = o.night, wood = night ? "#2a2420" : "#6b4a2e", roof = night ? "#3a2228" : "#8f2a20";
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-10,0V-180H10V0Z" fill="${wood}" ${O(3)}/><path d="M-70,-180H70V-200H-70Z" fill="${wood}" ${O(3)}/>
      <path d="M-56,-200V-300H56V-200Z" fill="${night ? "#3a3028" : "#9a7a4a"}" ${O(3)}/><path d="M-78,-300L0,-370L78,-300Z" fill="${roof}" ${O(3)}/><path d="M-4,-370L0,-400L4,-370Z" fill="${roof}"/><path d="M-86,-300H86" stroke="${INK}" stroke-width="4"/>
      <path d="M-30,-300V-230H30V-300" fill="#1a1412" opacity=".6"/><path d="M-60,-250h120v-10H-60z" fill="#c8392b" opacity=".85"/><path d="M-20,-200l-6,24M20,-200l6,24" stroke="#c8392b" stroke-width="4"/>
      <path d="M-40,-200v-18M-34,-200v-26M-46,-200v-22" stroke="#8a8a7a" stroke-width="2"/><circle cx="-40" cy="-226" r="3" fill="#ff6a30"/>
      ${LAMP(`${id}-lamp`, 36, -200, 0.55, { lit: o.lit !== false, smoke: o.smoke })}</g>`;
  }
  // a hurricane lamp: base, the glass with the flame inside (.fl1/.fl2 for Camp.flicker), the wire handle; origin = bottom centre
  function LAMP(id, x, y, s = 1, o = {}) {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-36,0h72l-8,-18h-56z" fill="#4a4a44" ${O(3)}/><rect x="-20" y="-52" width="40" height="34" rx="4" fill="#3d3833" ${O(3)}/>
      <path d="M-30,-52h60l-6,-110h-48z" fill="#f4f4ee" fill-opacity=".35" ${O(3)}/><path d="M-26,-60h52" stroke="#fff" stroke-opacity=".3" stroke-width="4"/>
      <g opacity="${o.lit === false ? 0 : 1}"><path class="fl1" d="M-12,-66q-8,-40 12,-66q16,30 8,66z" fill="#ffb347"/><path class="fl2" d="M-5,-66q-3,-26 5,-40q7,16 4,40z" fill="#fff3c0"/></g>
      <rect x="-34" y="-176" width="68" height="14" rx="4" fill="#3d3833" ${O(3)}/><path d="M-26,-176Q0,-260 26,-176" stroke="#5b5550" stroke-width="6" fill="none"/>
      ${o.smoke ? `<g class="smk"><path d="M0,-176q-10,-30 4,-60q14,-30 -2,-60" stroke="#cfcfcf" stroke-width="6" fill="none" opacity=".5" stroke-linecap="round"/></g>` : ""}</g>`;
  }
  // the campfire: a ring of stones, crossed logs, three flames (.fl1 .fl2 .fl3) and rising embers (.ffly); origin = ground centre
  function FIRE(id, x, y, s = 1, o = {}) {
    const r = mk(o.seed || 19);
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="6" rx="150" ry="30" fill="#000" opacity=".25"/>
      ${[-110, -70, -24, 24, 70, 110].map((sx, i) => `<ellipse cx="${sx}" cy="${-4 + (i % 2) * 8}" rx="30" ry="18" fill="${o.night ? "#5a5a60" : "#8a8680"}" ${O(3)}/>`).join("")}
      <path d="M-80,-8L70,-44M-66,-46L80,-6" stroke="#4a3426" stroke-width="24" stroke-linecap="round"/><path d="M-80,-8L70,-44M-66,-46L80,-6" stroke="#2a1a10" stroke-width="24" stroke-linecap="round" stroke-dasharray="6 30" opacity=".5"/>
      <g id="${id}-fl" opacity="${o.lit === false ? 0 : 1}"><path class="fl1" d="M-56,-30Q-70,-120 -14,-190Q-24,-120 8,-100Q20,-160 56,-180Q44,-100 66,-30Z" fill="#f07a2c"/>
        <path class="fl2" d="M-34,-30Q-40,-100 0,-146Q6,-90 24,-78Q34,-112 44,-124Q50,-66 44,-30Z" fill="#f6c24c"/><path class="fl3" d="M-16,-30Q-16,-74 6,-96Q16,-66 22,-30Z" fill="#fff4c8"/>
        ${Array.from({ length: 8 }, (_, k) => `<circle class="ffly" cx="${f1(-40 + r() * 80)}" cy="${f1(-120 - r() * 160)}" r="${f1(2 + r() * 3)}" fill="#ffd27a" opacity=".8"/>`).join("")}</g></g>`;
  }
  // the longtail boat seen from the side (bow to the left): the hull with its paint stripes, the raised prow with a cloth and
  // garland, thwarts, the engine on its pivot at the stern with the long shaft into the water; origin = waterline at mid-hull
  function LONGTAIL(id, x, y, s = 1, o = {}) {
    const flip = o.flip ? -1 : 1;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${flip * s},${s})"><path d="M-420,0L-470,-120Q-480,-150 -450,-150L-300,-110L300,-100Q380,-96 420,-60L440,0Z" fill="url(#iHull)" ${OUT}/>
      <path d="M-300,-110L300,-100" stroke="#f4ecd8" stroke-width="6"/><path d="M-440,-150Q-400,-80 -300,-110" fill="#1f3a66" ${O(3)}/><path d="M-462,-150q-6,-40 10,-70" stroke="#c8392b" stroke-width="8" stroke-linecap="round"/>
      ${[-120, 40, 200].map((tx) => `<path d="M${tx},-100v-16h70v16" fill="#a8865a" ${O(3)}/>`).join("")}<path d="M-200,-104Q0,-70 300,-100" stroke="#6e5433" stroke-width="6" fill="none"/>
      <g id="${id}-eng" transform="translate(360,-110)"><rect x="-40" y="-70" width="80" height="60" rx="8" fill="#3a3f45" ${O(3)}/><rect x="-12" y="-100" width="24" height="30" fill="#5b6066" ${O(2.5)}/><path d="M-40,-30L-200,60" stroke="#5b6066" stroke-width="12" stroke-linecap="round"/>
        <path d="M-200,60l-24,14M-200,60l10,24" stroke="#8d969d" stroke-width="8" stroke-linecap="round"/><path d="M40,-40L140,-90" stroke="#6b4a2e" stroke-width="10" stroke-linecap="round"/></g>
      ${o.canopy !== false ? `<path d="M-160,-116V-260H200V-116" fill="none" stroke="#5b6066" stroke-width="8"/><path d="M-180,-260Q20,-290 220,-260L200,-230Q20,-250 -160,-230Z" fill="#2f6fb8" ${O(3)}/>` : ""}
      <path d="M-420,0H440" stroke="#ffffff" stroke-width="6" opacity=".5"/></g>`;
  }
  // the puffer fish, side view facing left: a plump body on url(#iPuff), dark spots, the big eye, a beak mouth, fins (class pfin flutter),
  // a fan tail. #id-body is scaled by Isle.puff(id, k): 0 = swimming, 1 = blown up into a ball with its spines out (#id-spines)
  function PUFFER(id, o = {}) {
    const r = mk(o.seed || 23), k = o.puff ?? 0, sc = 1 + 0.55 * k;
    let spots = ""; for (let i = 0; i < 12; i++) { const a = -1.1 + r() * 2.2, rr = 0.25 + r() * 0.55, sx = Math.cos(a) * rr * 74, sy = -Math.sin(a) * rr * 50 - 10; spots += `<circle cx="${f1(sx)}" cy="${f1(sy)}" r="${f1(5 + r() * 6)}" fill="#5e5a2e" opacity=".75"/>`; }
    let spines = ""; for (let i = 0; i < 26; i++) { const a = (i / 26) * Math.PI * 2, bx = Math.cos(a) * 78, by = Math.sin(a) * 60; spines += `<path d="M${f1(bx * 0.92)},${f1(by * 0.92)}L${f1(bx * 1.16)},${f1(by * 1.16)}" stroke="#4a4624" stroke-width="4" stroke-linecap="round"/>`; }
    return `<g id="${id}"><g id="${id}-body" transform="scale(${f1(sc)})" style="transform-origin:0px 0px">
      <g id="${id}-spines" opacity="${k}">${spines}</g>
      <g class="pfin" style="transform-origin:-10px 36px"><path d="M-10,36q-30,30 -4,56q22,-16 30,-48z" fill="#c9bf86" ${O(2.5)}/></g>
      <path d="M-82,-6Q-80,-56 -24,-62Q40,-66 76,-22Q92,4 72,32Q40,62 -20,58Q-80,52 -82,-6Z" fill="url(#iPuff)" ${OUT}/>${spots}
      <path d="M-60,-40q24,-14 50,-16" stroke="#fff" stroke-opacity=".35" stroke-width="5" fill="none" stroke-linecap="round"/>
      <g class="pfin" style="transform-origin:-24px 22px"><path d="M-24,22q-26,8 -34,32q26,0 44,-18z" fill="#d9d0a0" ${O(2.5)}/></g>
      <g class="pfin" style="transform-origin:30px -56px"><path d="M30,-56q6,-26 24,-34q6,22 -8,38z" fill="#c9bf86" ${O(2.5)}/></g>
      <path d="M76,-10q30,-24 36,-44q10,26 2,52q6,30 -4,46q-14,-22 -34,-36z" fill="#d9d0a0" ${O(3)}/>
      <circle cx="-44" cy="-16" r="16" fill="#fbf7ee" ${O(3)}/><circle cx="-47" cy="-15" r="8" fill="#1d130c"/><circle cx="-50" cy="-19" r="3" fill="#fff"/>
      <path d="M-84,10q8,-6 14,0" fill="#4a3a2a" ${O(2.5)}/><path d="M-80,6h8" stroke="#f4ecd8" stroke-width="3"/></g></g>`;
  }
  // a coconut (husked, green) with the top cut open and a straw of palm stem; origin = bottom centre
  const COCONUT = (x, y, s = 1, open = true) => `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="0" cy="6" rx="60" ry="12" fill="#000" opacity=".2"/><path d="M-54,-10Q-62,-80 -20,-120Q0,-134 22,-120Q64,-80 54,-10Q40,10 0,10Q-40,10 -54,-10Z" fill="#7aa84a" ${OUT}/><path d="M-30,-100q10,-20 30,-22" stroke="#fff" stroke-opacity=".25" stroke-width="6" fill="none" stroke-linecap="round"/>${open ? `<ellipse cx="4" cy="-118" rx="22" ry="8" fill="#f4ecd8" ${O(2.5)}/><ellipse cx="4" cy="-118" rx="9" ry="3.5" fill="#2a1a10"/><path d="M8,-120L30,-200" stroke="#9a7a3a" stroke-width="6" stroke-linecap="round"/>` : `<circle cx="0" cy="-124" r="6" fill="#4a6a2a"/>`}</g>`;
  // a grilled fish on a stick: the puffer skinned, charred, on a split stick; origin = the stick's held end
  const STICKFISH = (x, y, s = 1, rot = -60) => `<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><rect x="-5" y="-250" width="10" height="250" rx="4" fill="#8a6a44" ${O(2.5)}/><path d="M-30,-250Q-44,-320 -10,-380Q30,-400 48,-350Q60,-300 30,-250Z" fill="#c9924c" ${O(3)}/><path d="M-24,-300q20,-30 46,-24M-16,-340q16,-18 40,-12" stroke="#5a3a1a" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M-20,-370q10,-10 26,-6" stroke="#2a1a10" stroke-width="8" fill="none" stroke-linecap="round" opacity=".8"/><circle cx="4" cy="-262" r="4" fill="#2a1a10"/></g>`;
  // the phone with no bars: a dark screen, "ไม่มีสัญญาณ", a crossed signal icon; origin = centre
  const PHONE = (id, x, y, s = 1, rot = 0) => `<g id="${id}" transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><rect x="-70" y="-140" width="140" height="280" rx="18" fill="#1a1a1e" ${OUT}/><rect x="-62" y="-128" width="124" height="256" rx="12" fill="#0c0f16"/>
    <g transform="translate(0,-60)"><path d="M-22,10v-6M-12,10v-12M-2,10v-18M8,10v-24M18,10v-30" stroke="#5b6066" stroke-width="6" stroke-linecap="round"/><path d="M-30,-30L30,20" stroke="#c8392b" stroke-width="6" stroke-linecap="round"/></g>
    ${T(0, 20, "ไม่มีสัญญาณ", 18, "#c9d0d4", { w: 700 })}${T(0, 48, "ไม่มีเน็ต", 15, "#6f7880", { w: 500 })}<rect x="-30" y="110" width="60" height="6" rx="3" fill="#5b6066"/></g>`;
  // the island far off at sea: a low rock with a hump, palms, the shrine's roof on the headland; origin = waterline centre, ~900 wide
  function ISLAND(x, y, s = 1, t = "day", o = {}) {
    const night = t === "night", rock = night ? "#0f1626" : t === "dusk" ? "#3a2a44" : t === "dawn" ? "#3a3450" : "#5a6a58", lite = night ? "#1a2238" : t === "dusk" ? "#5a4060" : t === "dawn" ? "#5a5070" : "#7f9a74";
    return `<g transform="translate(${x},${y}) scale(${s})"><path d="M-460,0Q-420,-60 -300,-80Q-200,-110 -80,-150Q40,-230 160,-200Q260,-180 330,-110Q400,-60 460,0Z" fill="${rock}"/><path d="M-80,-150Q40,-230 160,-200Q200,-190 230,-170Q140,-190 40,-170Q-40,-150 -80,-150Z" fill="${lite}" opacity=".7"/>
      ${PALM(-250, -82, 0.26, 40, 31, { night: night || t === "dusk" })}${PALM(-150, -110, 0.3, -30, 33, { night: night || t === "dusk" })}${PALM(40, -170, 0.28, 30, 35, { night: night || t === "dusk" })}
      <g transform="translate(200,-200) scale(.32)"><path d="M-10,0V-180H10Z" fill="${night ? "#1a2238" : "#5a4030"}"/><path d="M-78,-180L0,-250L78,-180Z" fill="${night ? "#2a2238" : "#8f2a20"}"/></g>
      ${o.lamp ? `<circle cx="214" cy="-258" r="6" fill="#ffd27a"/>` : ""}<path d="M-470,0H470" stroke="#fff" stroke-width="4" opacity="${night ? 0.15 : 0.4}"/></g>`;
  }

  // ======================================================================================================
  // 1. ยาย's porch at the water's edge, morning: the deck of a stilt house in the foreground, the rail, the sea beyond with the
  //    longtail moored, the island far off, palms; coconuts and the cleaver on the deck
  // ======================================================================================================
  function porch(L, o = {}) {
    const id = o.id || "pc", r = mk(o.seed || 41), t = "morning";
    sky(L, t); put(L.sky, `<circle cx="820" cy="420" r="400" fill="url(#iSunG)" opacity=".5"/>`);
    clouds(L, 43, t, { n: 7, y0: -300, h: 700 });
    sea(L, t, 860, 1180, { seed: 45, rows: 9 });
    put(L.far, ISLAND(1420, 880, 0.62, t));
    // mid: the beach below the house, the moored boat, the posts of the pier, palms either side
    put(L.mid, `<path d="M-1500,1140Q-200,1100 540,1130Q1300,1160 2700,1120V1400H-1500Z" fill="#e3d2ac"/>${LONGTAIL(`${id}-boat`, 760, 1150, 0.5, { canopy: false })}
      <path d="M-120,1120V1000M-40,1130V1000M40,1140V1000" stroke="#6b4a2e" stroke-width="10"/><path d="M-140,1000H60" stroke="#8a6a44" stroke-width="14"/>
      ${PALM(-240, 1150, 1.0, 180, 47)}${PALM(1180, 1140, 0.9, -140, 49)}`);
    // set: the deck (planks running toward us), the rail along the back edge, a post with a hanging lamp, coconut pile, cleaver, a water jar
    let s = `<rect x="-1500" y="1300" width="4200" height="1600" fill="url(#iPlank)"/>${Array.from({ length: 18 }, (_, k) => `<path d="M${-1500 + k * 240},1300L${-1700 + k * 300},2900" stroke="#4e3a20" stroke-width="5" opacity=".7"/>`).join("")}<path d="M-1500,1300H2700" stroke="#3e2c16" stroke-width="10"/>
      <path d="M-1500,1300V1120M-1500,1130H2700M-1500,1220H2700" stroke="#8a6a44" stroke-width="14"/>${Array.from({ length: 12 }, (_, k) => `<path d="M${-1300 + k * 330},1300V1120" stroke="#8a6a44" stroke-width="14"/>`).join("")}
      <path d="M880,1300V560" stroke="#6b4a2e" stroke-width="30"/><path d="M880,620h120" stroke="#6b4a2e" stroke-width="14"/>${LAMP(`${id}-lamp`, 1000, 760, 0.7, { lit: false })}
      ${[[180, 1600, 0.9], [120, 1660, 0.85], [250, 1680, 0.95], [190, 1720, 0.8]].map(([x, y, k]) => COCONUT(x, y, k, false)).join("")}<path d="M330,1700l80,-30" stroke="#8d969d" stroke-width="14" stroke-linecap="round"/><path d="M330,1700l-30,10" stroke="#6b4a2e" stroke-width="14" stroke-linecap="round"/>
      <g transform="translate(1150,1680)"><path d="M-70,0Q-90,-90 -50,-150H50Q90,-90 70,0Z" fill="#8a5a3a" ${OUT}/><ellipse cx="0" cy="-150" rx="50" ry="14" fill="#3a2a1a" ${O(3)}/><path d="M-60,-90q60,14 120,0" stroke="#fff" stroke-opacity=".2" stroke-width="8" fill="none"/></g>`;
    put(L.set, s);
    put(L.glow, `<rect x="-1400" y="300" width="4000" height="1600" fill="#ffd8a0" opacity=".08"/>`);
  }

  // ======================================================================================================
  // 2. inside the longtail, looking aft: the stern with the engine on its pivot (ลุงนวล stands there), the thwart the kids sit on,
  //    the gunwales running past the camera, the sea and sky behind (time, storm); o.island = the island far behind on the left
  // ======================================================================================================
  function boatIn(L, o = {}) {
    const id = o.id || "bi", t = o.time || "morning", r = mk(o.seed || 51), night = t === "night";
    sky(L, t); if (night) stars(L, 53);
    if (t === "dawn") put(L.sky, `<circle cx="300" cy="900" r="520" fill="url(#iSunG)" opacity=".8"/>`);
    clouds(L, 55, t, { n: 8, y0: -200, h: 700, storm: o.storm });
    sea(L, t, 900, 1500, { seed: 57, rows: 12, glitter: t === "dawn" ? 300 : undefined });
    if (o.island) put(L.far, ISLAND(o.islandX ?? 180, 912, o.islandS ?? 0.5, t, { lamp: o.lamp }));
    // the hull interior: gunwales converging aft, ribs, the stern board with the engine
    let s = `<path d="M-1500,2900L-700,1120Q0,1090 700,1120L2600,2900Z" fill="url(#iPlank)"/><path d="M-1500,2900L-700,1120Q0,1090 700,1120L2600,2900" stroke="#3e2c16" stroke-width="12" fill="none"/>
      ${Array.from({ length: 9 }, (_, k) => { const a = k / 8, y = 1120 + a * a * 1700, x0 = -700 - a * a * 800, x1 = 700 + a * a * 1900; return `<path d="M${f1(x0)},${f1(y)}Q0,${f1(y - 40 - a * 80)} ${f1(x1)},${f1(y)}" stroke="#4e3a20" stroke-width="${f1(4 + a * 8)}" fill="none"/>`; }).join("")}
      <path d="M-760,1140Q0,1040 760,1140L740,1180Q0,1090 -740,1180Z" fill="#2d4f82" ${O(3)}/><path d="M-700,1118Q0,1030 700,1118" stroke="#c8392b" stroke-width="12" fill="none"/>
      <path d="M-760,1140L-1500,1500M760,1140L2300,1500" stroke="#2d4f82" stroke-width="60"/><path d="M-760,1140L-1500,1500M760,1140L2300,1500" stroke="#c8392b" stroke-width="14"/>
      <g id="${id}-eng" transform="translate(300,1110)"><rect x="-70" y="-120" width="140" height="100" rx="12" fill="#3a3f45" ${OUT}/><rect x="-20" y="-170" width="40" height="50" fill="#5b6066" ${O(3)}/><path d="M-70,-60L-280,-10" stroke="#6b4a2e" stroke-width="16" stroke-linecap="round"/><path d="M60,-40L260,140" stroke="#5b6066" stroke-width="14" stroke-linecap="round"/><circle cx="-30" cy="-70" r="14" fill="#c8392b" ${O(2.5)}/></g>
      <path d="M-520,1500H520V1540H-520Z" fill="#a8865a" ${O(3)}/><path d="M-500,1540v60M500,1540v60" stroke="#6e5433" stroke-width="14"/>
      <g transform="translate(-520,1700)"><path d="M-60,0q-10,-60 10,-90h120q20,30 10,90z" fill="#3d4d45" ${O(3)}/><path d="M-40,-90q50,-40 100,0" stroke="#2e2a26" stroke-width="8" fill="none"/></g><path d="M-900,1800q100,-30 200,0" stroke="#6e5433" stroke-width="20" stroke-linecap="round"/>`;
    put(L.set, s);
    put(L.fg, `<path d="M-1500,2900L-1200,1640Q-300,1560 540,1600Q1400,1560 2300,1640L2600,2900Z" fill="none"/>`);
    if (night) put(L.glow, `<rect x="-1400" y="300" width="4000" height="1600" fill="#3a5a8c" opacity=".08"/>`);
    else if (t === "dawn") put(L.glow, `<rect x="-1400" y="300" width="4000" height="1600" fill="#ffb070" opacity=".1"/>`);
  }

  // ======================================================================================================
  // 2b. the open sea, morning, seen from another boat: the island big on the right with the shrine on its headland, the longtail
  //     (#id-boat, slid by the shot) crossing toward it on a sea that has started to heave; the squall building behind the island
  // ======================================================================================================
  function seaWide(L, o = {}) {
    const id = o.id || "sw", t = o.time || "morning";
    sky(L, t); put(L.sky, `<circle cx="300" cy="300" r="380" fill="url(#iSunG)" opacity=".45"/>`);
    clouds(L, 111, t, { n: 7, y0: -400, h: 800, storm: o.storm });
    sea(L, t, 1000, 2000, { seed: 113, rows: 14 });
    put(L.far, ISLAND(o.islandX ?? 820, 1012, o.islandS ?? 1.35, t));
    put(L.set, `<g id="${id}-boat">${LONGTAIL(`${id}-lt`, o.boatX ?? -200, o.boatY ?? 1480, 0.78, { canopy: false })}<path d="M${(o.boatX ?? -200) - 520},${(o.boatY ?? 1480) + 10}q60,-30 120,0t120,0" stroke="#ffffff" stroke-width="12" fill="none" opacity=".7" class="foam"/></g>`);
    wash(L, id, t, { y: 2000, seed: 115 });
    put(L.glow, `<rect x="-1400" y="300" width="4000" height="1600" fill="#ffd8a0" opacity=".07"/>`);
  }

  // ======================================================================================================
  // 3. the island's beach (time: dusk | night | dawn): the headland on the right with the shrine on top (#id-shrine, lamp lit at
  //    night when o.lamp), palms on the left, the sea beyond, sand across the lower frame with the water's edge lapping at the
  //    bottom (#id-wash); o.fire puts the campfire at (fireX, 1560) with its glow; o.shelter the frond lean-to against the rock;
  //    o.pool the tide pool among the rocks lower left; lightning in the far storm when life() is given o.bolts
  // ======================================================================================================
  function beach(L, o = {}) {
    const id = o.id || "bh", t = o.time || "dusk", r = mk(o.seed || 61), night = t === "night", dark = night || t === "dusk";
    sky(L, t);
    if (night) { stars(L, 63); moon(L, o.moonX ?? 760, o.moonY ?? 300, 64, `${id}-moon`); }
    if (t === "dawn") put(L.sky, `<circle cx="${o.sunX ?? 900}" cy="1010" r="560" fill="url(#iSunG)" opacity=".85"/><circle cx="${o.sunX ?? 900}" cy="1040" r="70" fill="#fff0c0"/>`);
    clouds(L, 65, t, { n: night ? 4 : 8, y0: -300, h: 900, storm: t === "dusk" });
    if (t === "dusk") put(L.far, `<g id="${id}-bolt" opacity="0"><path d="M1240,120l-60,170l50,-20l-80,210l40,-10l-90,230" stroke="#fff6ff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M1240,120l-60,170l50,-20l-80,210l40,-10l-90,230" stroke="#cfa0ff" stroke-width="22" fill="none" opacity=".4" filter="url(#iSoft6)"/></g>`);
    sea(L, t, 1000, 1420, { seed: 67, rows: 11, glitter: night ? (o.moonX ?? 760) : t === "dawn" ? (o.sunX ?? 900) : undefined });
    // mid: the headland (a stack of boulders) with the shrine, the palms, rocks at the waterline
    put(L.mid, `${BOULDER(1240, 1300, 900, 520, 71, t)}${BOULDER(960, 1320, 520, 300, 73, t)}${BOULDER(1500, 1330, 500, 260, 75, t, { wet: true })}
      ${SHRINE(`${id}-shrine`, 1180, 830, 0.9, { night: dark, lit: !!o.lamp, smoke: o.smoke })}
      ${PALM(-120, 1360, 1.05, 220, 77, { night: dark })}${PALM(120, 1380, 0.8, 120, 79, { night: dark })}${PALM(-380, 1340, 0.9, 260, 81, { night: dark })}`);
    if (o.lamp) put(L.glow, `<circle cx="1212" cy="750" r="150" fill="url(#iLampG)"/>`);
    // set: the sand, the rocks on the left with the pool, the shelter, driftwood, the fire
    sand(L, t, 1300, { seed: 83 });
    let s = `<path d="M-1500,1300Q-300,1270 540,1300Q1400,1330 2700,1290" stroke="#fff" stroke-opacity="${night ? 0.08 : 0.25}" stroke-width="30" fill="none" filter="url(#iSoft6)"/>`;
    if (o.pool) s += `${BOULDER(-200, 1760, 420, 170, 85, t, { wet: true })}${BOULDER(300, 1800, 300, 130, 87, t, { wet: true })}<g id="${id}-pool"><ellipse cx="80" cy="1700" rx="230" ry="80" fill="url(#${dark ? "iPoolD" : "iPoolW"})" ${O(3)}/><ellipse cx="80" cy="1700" rx="230" ry="80" fill="url(#iCaust)" opacity=".5" class="caust"/></g>`;
    if (o.shelter) s += `<g id="${id}-shelter">${BOULDER(900, 1540, 360, 230, 89, t)}${[-10, 30, 70, 110].map((dx, k) => `<path d="M${760 + dx},1540L${640 + dx},1330Q${600 + dx},1300 ${580 + dx},1340L${720 + dx},1540Z" fill="${dark ? "#1a2a22" : "#4f7a44"}" ${O(3)}/><path d="M${700 + dx},1540L${610 + dx},1340" stroke="${dark ? "#2a3a2a" : "#6a9a58"}" stroke-width="4"/>`).join("")}</g>`;
    s += `<path d="M1500,1640q120,-30 240,10q60,20 120,-10" stroke="#5a4a3a" stroke-width="18" stroke-linecap="round" fill="none"/><path d="M-700,1560q80,-20 160,8" stroke="#5a4a3a" stroke-width="14" stroke-linecap="round" fill="none"/>`;
    put(L.set, s);
    if (o.fire) { put(L.set, FIRE(`${id}-fire`, o.fireX ?? 560, o.fireY ?? 1580, o.fireS ?? 0.9, { night: dark, lit: o.fire !== "out" }));
      if (o.fire !== "out") put(L.glow, `<g class="fireglow"><circle cx="${o.fireX ?? 560}" cy="${(o.fireY ?? 1580) - 60}" r="560" fill="url(#iFireG)"/></g>`); }
    wash(L, id, t, { y: o.washY ?? 1840, seed: 91 });
    if (night) put(L.glow, `<rect x="-1400" y="-900" width="4000" height="3800" fill="#2a4a8c" opacity=".05"/>`);
    if (t === "dusk") put(L.glow, `<g id="${id}-flash" opacity="0"><rect x="-1400" y="-900" width="4000" height="3800" fill="#e8dcff"/></g>`);
  }

  // ======================================================================================================
  // 4. the tide pool from above (the first-person look down into it): rocks round a pool that fills the frame, clear water with
  //    caustics and rings (class ring), weed, a crab in the corner, small fish (class dart), and the puffer (#id-puff) — the shot's
  //    hands come in from the bottom; o.time dusk by default
  // ======================================================================================================
  function pool(L, o = {}) {
    const id = o.id || "tp", t = o.time || "dusk", r = mk(o.seed || 93), dark = t === "night";
    put(L.sky, `<rect x="-1400" y="-900" width="4000" height="3800" fill="${dark ? "#0b1220" : "#3a3238"}"/>`);
    // the rock rim (far = under the water surface edge; set = the rocks around)
    let rocks = ""; for (let k = 0; k < 14; k++) { const a = (k / 14) * Math.PI * 2, cx = 540 + Math.cos(a) * 640, cy = 980 + Math.sin(a) * 860; rocks += BOULDER(cx, cy + 120, 380 + r() * 200, 220 + r() * 120, 100 + k, t === "dusk" ? "dusk" : t, { wet: true }); }
    put(L.far, `<rect x="-1400" y="-900" width="4000" height="3800" fill="${dark ? "#1a2230" : "#6a5a58"}"/>${rocks}`);
    // the water: a big ellipse of graded water, sand and pebbles seen through it, caustics, rings, weed, fish
    let w = `<ellipse cx="540" cy="980" rx="520" ry="700" fill="url(#${dark ? "iPoolD" : "iPoolW"})"/><ellipse cx="540" cy="980" rx="520" ry="700" fill="none" ${O(5)}/>
      ${Array.from({ length: 40 }, () => `<circle cx="${f1(200 + r() * 680)}" cy="${f1(500 + r() * 950)}" r="${f1(4 + r() * 10)}" fill="#c9b48a" opacity=".35"/>`).join("")}
      <ellipse cx="540" cy="980" rx="520" ry="700" fill="url(#iCaust)" opacity="${dark ? 0.35 : 0.6}" class="caust"/>
      ${[[220, 760], [800, 1300], [360, 1500]].map(([x, y]) => `<path d="M${x},${y}q-20,-60 10,-110q20,-30 0,-70M${x + 24},${y}q10,-70 -16,-120" stroke="${dark ? "#1f4a3a" : "#2f7a4a"}" stroke-width="7" fill="none" stroke-linecap="round" class="weed"/>`).join("")}
      <g transform="translate(860,620)"><ellipse rx="36" ry="24" fill="#c8562e" ${O(3)}/><path d="M-36,-6l-24,-18M36,-6l24,-18M-30,10l-20,16M30,10l20,16M-10,-20l-6,-20M12,-20l6,-20" stroke="#c8562e" stroke-width="6" stroke-linecap="round"/><circle cx="-10" cy="-10" r="4" fill="#1d130c"/><circle cx="12" cy="-10" r="4" fill="#1d130c"/></g>
      ${[[300, 1000, 0.5], [700, 880, 0.45], [640, 1420, 0.55]].map(([x, y, k], i) => `<g class="dart" data-i="${i}" transform="translate(${x},${y})"><path d="M-30,0q16,-14 36,0q-20,14 -36,0z" fill="#d9e0e8" ${O(2)} transform="scale(${k * 2})"/><path d="M-30,0l-14,-8v16z" fill="#d9e0e8" transform="scale(${k * 2})"/></g>`).join("")}
      ${[[540, 980, 160], [420, 1200, 120], [700, 760, 90]].map(([x, y, rr], i) => `<ellipse class="ring" data-i="${i}" cx="${x}" cy="${y}" rx="${rr}" ry="${rr * 0.55}" fill="none" stroke="#ffffff" stroke-width="3" opacity="0"/>`).join("")}`;
    put(L.set, w);
    put(L.act, `<g id="${id}-puffg" transform="translate(${o.puffX ?? 560},${o.puffY ?? 1320}) scale(${o.puffS ?? 1.1})">${PUFFER(`${id}-puff`, { puff: o.puff ?? 0, seed: 95 })}</g>`);
    put(L.glow, `<ellipse cx="420" cy="760" rx="360" ry="260" fill="#ffffff" opacity="${dark ? 0.06 : 0.14}" filter="url(#iSoft)"/>`);
  }

  // ======================================================================================================
  // 5. lying on the sand, looking up (โต้ง's paralysed point of view): the night sky overhead, the fire's glow licking the lower
  //    right edge, the eyelids that cannot blink as a dark vignette with lashes (fg), room at the top for a face to lean in
  // ======================================================================================================
  function lieDown(L, o = {}) {
    const id = o.id || "ld", r = mk(o.seed || 97);
    sky(L, "night"); stars(L, 99, 160, { h: 2400 }); moon(L, o.moonX ?? 300, o.moonY ?? 1500, 58, `${id}-moon`);
    clouds(L, 101, "night", { n: 3, y0: 200, h: 1200 });
    put(L.mid, `${PALM(1500, 2400, 1.2, -400, 103, { night: true })}`);
    put(L.set, `<path d="M-1500,2900L-1500,2100Q-200,2000 1200,2200L2700,2000V2900Z" fill="#1c2232"/>`);
    put(L.glow, `<g class="fireglow"><ellipse cx="1180" cy="1900" rx="900" ry="500" fill="url(#iFireG)"/></g><g id="${id}-lampg" opacity="0"><circle cx="-200" cy="400" r="700" fill="url(#iLampG)"/></g>`);
    put(L.fg, `<g id="${id}-lids"><rect x="-1400" y="-900" width="4000" height="3800" fill="url(#iEye)"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${-60 + k * 90},-80q${(k % 2 ? 30 : -20)},80 ${(k % 2 ? 10 : -30)},140" stroke="#050408" stroke-width="${7 + (k % 3) * 2}" fill="none" stroke-linecap="round" opacity=".9"/>`).join("")}
      ${Array.from({ length: 14 }, (_, k) => `<path d="M${-40 + k * 90},2000q${(k % 2 ? 30 : -20)},-80 ${(k % 2 ? 10 : -30)},-140" stroke="#050408" stroke-width="${7 + (k % 3) * 2}" fill="none" stroke-linecap="round" opacity=".9"/>`).join("")}</g>
      <g id="${id}-blur" opacity="0"><rect x="-1400" y="-900" width="4000" height="3800" fill="#9fb8d8" opacity=".18"/></g>`);
  }

  // ======================================================================================================
  // 6. the shrine close, dawn: the headland rock under it, the sea and the rising sun behind; the lamp on its ledge still smoking
  // ======================================================================================================
  function shrineClose(L, o = {}) {
    const id = o.id || "sc", t = "dawn";
    sky(L, t); put(L.sky, `<circle cx="760" cy="1120" r="640" fill="url(#iSunG)" opacity=".9"/><circle cx="760" cy="1140" r="80" fill="#fff0c0"/>`);
    clouds(L, 105, t, { n: 6, y0: -200, h: 700 });
    sea(L, t, 1100, 1700, { seed: 107, rows: 10, glitter: 760 });
    put(L.mid, `${BOULDER(540, 1900, 1400, 700, 109, t)}`);
    put(L.set, `${BOULDER(540, 1500, 700, 260, 111, t)}${SHRINE(`${id}-shrine`, 540, 1270, 2.0, { night: false, lit: true, smoke: true })}`);
    put(L.glow, `<circle cx="612" cy="1100" r="260" fill="url(#iLampG)" opacity=".7"/><rect x="-1400" y="300" width="4000" height="1600" fill="#ffb070" opacity=".1"/>`);
  }

  // ======================================================================================================
  // the life of a shot: waves slide, foam breathes, glitter and plankton twinkle, stars wink, clouds drift, the far storm flashes
  // at o.bolts, fire and lamps flicker (Camp.flicker classes), smoke rises, the fish's fins flutter, the pool's rings spread
  // ======================================================================================================
  function life(tl, scope, t0, dur, o = {}) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`), rep = (p) => Math.ceil(dur / p) + 1;
    q(".wv").forEach((el, i) => { const sp = +el.dataset.sp || 1, amp = +el.dataset.amp || 30, p = 3.2 / sp; tl.fromTo(el, { x: -amp }, { x: amp, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 - (i % 5) * 0.4); });
    q(".foam").forEach((el, i) => { const p = 1.6 + (i % 3) * 0.5; tl.fromTo(el, { opacity: +el.getAttribute("opacity") * 0.6 }, { opacity: +el.getAttribute("opacity"), duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 4) * 0.3); });
    q(".glit").forEach((el, i) => { if (i % 2) return; const p = 0.5 + (i % 5) * 0.17; tl.fromTo(el, { opacity: 0.1 }, { opacity: +el.getAttribute("opacity") || 0.6, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 7) * 0.13); });
    q(".bio").forEach((el, i) => { const p = 0.7 + (i % 6) * 0.3; tl.fromTo(el, { opacity: 0 }, { opacity: 0.3 + (i % 4) * 0.2, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 9) * 0.21); });
    q(".star").forEach((el, i) => { const p = 1.1 + (i % 4) * 0.4; tl.fromTo(el, { opacity: 0.25 }, { opacity: 0.95, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 5) * 0.37); });
    q(".cld").forEach((el, i) => { const sp = +el.dataset.sp || 0.6; tl.fromTo(el, { x: 0 }, { x: -60 * sp * dur / 10, duration: dur, ease: "none", immediateRender: false }, t0); });
    q(".frnd").forEach((el, i) => { const p = 2.4 + (i % 3) * 0.6; tl.fromTo(el, { rotation: -1.5 }, { rotation: 1.5, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.5); });
    q(".smk").forEach((el) => { tl.fromTo(el, { y: 0, opacity: 0.6 }, { y: -60, opacity: 0, duration: 2.2, repeat: rep(2.2), ease: "none", immediateRender: false }, t0); });
    q(".pfin").forEach((el, i) => { const p = 0.22 + (i % 3) * 0.05; tl.fromTo(el, { rotation: -12 }, { rotation: 12, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.07); });
    q(".dart").forEach((el, i) => { const p = 3 + i; tl.fromTo(el, { x: 0 }, { x: i % 2 ? -140 : 160, duration: p, repeat: rep(p), yoyo: true, ease: "power1.inOut", immediateRender: false }, t0 + i * 0.8); });
    q(".ring").forEach((el, i) => { const p = 2.4; tl.fromTo(el, { opacity: 0.6, scale: 0.2 }, { opacity: 0, scale: 1.4, transformOrigin: "50% 50%", duration: p, repeat: rep(p), ease: "power1.out", immediateRender: false }, t0 + i * 0.8); });
    q(".caust").forEach((el) => { tl.fromTo(el, { x: 0, y: 0 }, { x: 44, y: 18, duration: 2.6, repeat: rep(2.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); });
    q(".weed").forEach((el, i) => { const p = 1.8 + (i % 2) * 0.4; tl.fromTo(el, { x: -6 }, { x: 6, duration: p, repeat: rep(p), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.3); });
    if (window.Camp) Camp.flicker(tl, scope, t0, dur);
    const wash = document.querySelector(`${scope} [id$="-wash"]`); if (wash) { const p = o.washP || 5.2; tl.fromTo(wash, { y: 0 }, { y: -(o.washAmp || 70), duration: p / 2, repeat: rep(p / 2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); }
    (o.bolts || []).forEach((bt) => { const bolt = document.querySelector(`${scope} [id$="-bolt"]`), flash = document.querySelector(`${scope} [id$="-flash"]`);
      [[0, 0.06], [0.1, 0.05], [0.22, 0.12]].forEach(([d, l]) => { if (bolt) { tl.set(bolt, { opacity: 1 }, t0 + bt + d); tl.set(bolt, { opacity: 0 }, t0 + bt + d + l); } if (flash) { tl.set(flash, { opacity: 0.35 }, t0 + bt + d); tl.to(flash, { opacity: 0, duration: l * 2, immediateRender: false }, t0 + bt + d); } }); });
  }
  // the puffer's blow-up: k 0 → 1 over d seconds from t (the spines come out with it)
  function puff(tl, id, t, d = 0.5, from = 0, to = 1) {
    const body = document.getElementById(`${id}-body`), sp = document.getElementById(`${id}-spines`), c = { k: from };
    const go = () => { body.setAttribute("transform", `scale(${(1 + 0.55 * c.k).toFixed(3)})`); sp.setAttribute("opacity", Math.max(0, Math.min(1, (c.k - 0.3) / 0.7)).toFixed(2)); };
    tl.to(c, { k: to, duration: d, ease: to > from ? "back.out(1.6)" : "power2.in", onUpdate: go, immediateRender: false }, t); go();
  }

  // ======================================================================================================
  // the cast (Rig.CAST): แพรว 14, โต้ง 10, ยาย, ลุงนวล, ตาเมฆ
  // ======================================================================================================
  Object.assign(Rig.CAST, {
    praew: { // แพรว: fourteen, long dark hair with a side fringe and a low side ponytail, oversized lilac tee, denim shorts, white sneakers, a hair tie on the wrist
      untuck: true,
      skin: "#ebc6a6", skinS: "#cf9f7c", top: "#a98fd1", topS: "#8570ad", sleeve: "#a98fd1", sleeveS: "#8570ad", forearm: "#ebc6a6", forearmS: "#cf9f7c",
      pants: "#3d5a80", pantsS: "#2c4360", shoe: "#f0ece4", belt: "#2c4360",
      torsoExtra: `<path d="M-14,-440l6,-14l6,14l14,2l-10,10l2,14l-12,-6l-12,6l2,-14l-10,-10z" fill="#f4ecd8" opacity=".85"/><path d="M-30,-486Q0,-470 30,-486" stroke="#8570ad" stroke-width="4" fill="none"/>`,
      hair: `<path d="M-50,-548Q-56,-612 0,-614Q54,-612 50,-548Q46,-586 10,-590Q-20,-592 -34,-572Q-44,-556 -50,-548Z" fill="#3a2418" ${OUT}/>
        <path d="M-50,-548Q-70,-500 -62,-440Q-60,-400 -52,-370Q-40,-380 -34,-420Q-30,-480 -40,-530Z" fill="#3a2418" ${OUT}/><path d="M-56,-460h16" stroke="#e07a8a" stroke-width="6" stroke-linecap="round"/>
        <path d="M-10,-590Q30,-600 48,-560" stroke="#5a3a28" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>`,
      face: `<g fill="#e88a86" opacity=".4"><ellipse cx="-26" cy="-524" rx="8" ry="4"/><ellipse cx="32" cy="-524" rx="8" ry="4"/></g>`,
    },
    tong: { // โต้ง: ten, bright yellow tee under an olive explorer's vest with pockets, khaki shorts, sandals, a khaki bucket hat, a whistle on a cord, freckles
      untuck: true,
      skin: "#dcae84", skinS: "#b98a62", top: "#f2c94c", topS: "#cfa636", sleeve: "#f2c94c", sleeveS: "#cfa636", forearm: "#dcae84", forearmS: "#b98a62",
      pants: "#c9b58a", pantsS: "#a8946c", shoe: "#5b4a3a", belt: "#8a7a5a",
      torsoExtra: `<path d="M-62,-470L-40,-486L-20,-440L-26,-300H-56Z" fill="#6b7a4a" ${OUT}/><path d="M62,-470L40,-486L20,-440L26,-300H56Z" fill="#6b7a4a" ${OUT}/>
        <rect x="-52" y="-380" width="24" height="26" rx="3" fill="#5a6a3a" ${O(2.5)}/><rect x="28" y="-380" width="24" height="26" rx="3" fill="#5a6a3a" ${O(2.5)}/><path d="M-52,-370h24M28,-370h24" stroke="${INK}" stroke-width="2"/>
        <path d="M-28,-486Q0,-470 28,-486L20,-420" stroke="#e07a4f" stroke-width="3" fill="none"/><path d="M14,-424h18v10h-12z" fill="#e07a4f" ${O(2)}/>`,
      hair: `<path d="M-46,-560Q-46,-606 0,-608Q46,-606 46,-560L30,-566L16,-554L0,-568L-16,-554L-30,-566Z" fill="#2a1c14" ${OUT}/>
        <path d="M-62,-566Q-70,-618 0,-622Q70,-618 62,-566Q40,-576 0,-578Q-40,-576 -62,-566Z" fill="#b8a67a" ${OUT}/><ellipse cx="0" cy="-566" rx="76" ry="14" fill="#a8946c" ${OUT}/><path d="M-50,-596Q0,-606 50,-596" stroke="#8a7a5a" stroke-width="5" fill="none"/>`,
      face: `<g fill="#b98a62" opacity=".6"><circle cx="-30" cy="-526" r="2"/><circle cx="-22" cy="-522" r="2"/><circle cx="-34" cy="-518" r="1.8"/><circle cx="30" cy="-526" r="2"/><circle cx="36" cy="-520" r="2"/><circle cx="26" cy="-518" r="1.8"/></g>`,
    },
    yai: { // ยาย: seventy, short grey hair in a low bun with a jasmine pin, a pale flowered blouse, a knee-length maroon sarong, sandals, laugh lines
      untuck: true,
      skin: "#c99a74", skinS: "#a97a56", top: "#cfe3ea", topS: "#a9c3cc", sleeve: "#cfe3ea", sleeveS: "#a9c3cc", forearm: "#c99a74", forearmS: "#a97a56",
      pants: "#7a2e3a", pantsS: "#5a1e2a", shoe: "#6a4a2e", belt: "#5a1e2a",
      torsoExtra: `${[[-34, -460], [10, -440], [-6, -400], [30, -380], [-38, -360]].map(([x, y]) => `<g transform="translate(${x},${y})"><circle r="4" fill="#e07a8a" opacity=".7"/><circle cx="-5" cy="-3" r="3" fill="#e07a8a" opacity=".7"/><circle cx="5" cy="-3" r="3" fill="#e07a8a" opacity=".7"/></g>`).join("")}<path d="M-26,-486Q0,-466 26,-486" stroke="#a9c3cc" stroke-width="4" fill="none"/>`,
      hemExtra: `<path d="M-60,-262Q-66,-200 -62,-120H62Q66,-200 60,-262Q30,-250 0,-254Q-30,-250 -60,-262Z" fill="#7a2e3a" ${OUT}/><path d="M-62,-150H62M-63,-136H63" stroke="#c9a55a" stroke-width="4"/><path d="M-30,-240q10,40 0,100M26,-242q-8,40 0,100" stroke="#5a1e2a" stroke-width="3" fill="none"/>`,
      hair: `<path d="M-48,-552Q-52,-608 0,-610Q52,-608 48,-552Q40,-580 0,-584Q-38,-580 -48,-552Z" fill="#b9b2a6" ${OUT}/><circle cx="-40" cy="-584" r="20" fill="#b9b2a6" ${OUT}/><circle cx="-52" cy="-596" r="7" fill="#f4f2ea" ${O(2)}/>`,
      face: `<path d="M-34,-520q10,-6 22,0M12,-520q10,-6 22,0M-40,-534l-6,2M46,-534l6,2" stroke="#8a6a4a" stroke-width="2.5" fill="none"/><path d="M-30,-508q8,8 0,16M30,-508q-8,8 0,16" stroke="#8a6a4a" stroke-width="2" fill="none" opacity=".7"/>`,
    },
    nuan: { // ลุงนวล: fifty-five, the fisherman: faded orange shirt with the sleeves rolled, grey shorts, a navy cap, a checked cloth round the neck, stubble, sun-dark skin
      untuck: true,
      skin: "#a9704a", skinS: "#875632", top: "#d98a4a", topS: "#b06a30", sleeve: "#d98a4a", sleeveS: "#b06a30", forearm: "#a9704a", forearmS: "#875632",
      pants: "#6b6f73", pantsS: "#4f5357", shoe: "#3a3330", belt: "#4f5357",
      torsoExtra: `<path d="M-40,-486Q-30,-440 -34,-380L-46,-370L-50,-486Z M40,-486Q30,-440 34,-380L46,-370L50,-486Z" fill="#c8392b" ${O(3)}/><path d="M-44,-470h12M-42,-440h12M-40,-410h12M32,-470h12M30,-440h12M28,-410h12" stroke="#2f4a8a" stroke-width="5"/><path d="M-30,-484Q0,-470 30,-484" stroke="#b06a30" stroke-width="4" fill="none"/>`,
      hair: `<path d="M-46,-562q-4,14 0,26M46,-562q4,14 0,26" stroke="#2a2420" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path d="M-50,-570Q-52,-618 0,-620Q52,-618 50,-570Z" fill="#2c3e6b" ${OUT}/><path d="M-54,-570Q0,-580 54,-570Q60,-562 54,-556Q0,-566 -54,-556Q-60,-562 -54,-570Z" fill="#2c3e6b" ${OUT}/><path d="M50,-564q36,6 30,30q-14,-16 -32,-20" fill="#2c3e6b" ${OUT}/>`,
      face: `<path d="M-30,-508q34,16 66,0" stroke="#5a4a3a" stroke-width="3" fill="none" stroke-dasharray="3 3"/><path d="M-34,-522q10,-5 22,0M12,-522q10,-5 22,0" stroke="#7a5a44" stroke-width="2.5" fill="none"/>`,
    },
    mek: { // ตาเมฆ: the old man of the island: long white hair tied back, a thin white beard, an old white shirt, dark fisherman's trousers wet to the thigh, bare feet, a cord with an amulet, cold pale skin
      untuck: true, noSheen: true,
      skin: "#cfc2b2", skinS: "#a8998a", top: "#e9e4d6", topS: "#c4bdad", sleeve: "#e9e4d6", sleeveS: "#c4bdad", forearm: "#cfc2b2", forearmS: "#a8998a",
      pants: "#1c2e4a", pantsS: "#12203a", shoe: "#cfc2b2", belt: "#12203a",
      torsoExtra: `<path d="M-24,-486Q0,-456 24,-486" stroke="#3a2a1a" stroke-width="3" fill="none"/><rect x="-7" y="-462" width="14" height="18" rx="3" fill="#8a7a3a" ${O(2)}/><path d="M-50,-380q10,20 0,60M48,-376q-8,22 0,56" stroke="#9a9488" stroke-width="3" fill="none" opacity=".6"/>`,
      hemExtra: `<path d="M-58,-262q6,-10 12,0q6,-10 12,0q6,-10 12,0q6,-10 12,0q6,-10 12,0q6,-10 12,0q6,-10 12,0q6,-10 12,0q6,-10 12,0" stroke="#cfe6ff" stroke-width="3" fill="none" opacity=".5"/>`,
      hair: `<path d="M-48,-552Q-52,-610 0,-612Q52,-610 48,-552Q40,-584 0,-586Q-40,-584 -48,-552Z" fill="#e8e4dc" ${OUT}/><path d="M-30,-580Q-60,-560 -56,-500Q-54,-470 -50,-440" stroke="#e8e4dc" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M-30,-580Q-60,-560 -56,-500Q-54,-470 -50,-440" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".5"/>
        <path d="M-14,-502Q0,-480 14,-502Q10,-470 0,-466Q-10,-470 -14,-502Z" fill="#e8e4dc" ${O(2.5)}/>`,
      face: `<path d="M-36,-522q12,-8 24,-2M12,-524q12,-6 24,2M-38,-506q10,10 22,8M16,-498q12,2 22,-8" stroke="#8a8078" stroke-width="2.5" fill="none"/><path d="M-6,-512h12" stroke="#9a8a84" stroke-width="2"/>`,
    },
  });

  // the kids' first-person hands (for Hand.open / Hand.grip): โต้ง's skin and the yellow cuff
  const TONGHAND = { skin: "#dcae84", skinS: "#b98a62", sleeve: "#f2c94c", sleeveS: "#cfa636" };
  if (window.Camp) Object.assign(Camp.hand, {
    lamp: `<g transform="translate(0,118) rotate(90) translate(0,-6) scale(.9)">${LAMP("", -176, 0, 1, { lit: true }).replace('transform="translate(-176,0) scale(1)"', 'transform="translate(0,0) rotate(-90) translate(-200,20)"')}</g>`,
    lighter: `<g transform="translate(0,118)"><rect x="-10" y="-30" width="20" height="40" rx="4" fill="#c8392b" ${O(2.5)}/><rect x="-8" y="-40" width="16" height="12" rx="2" fill="#9aa0a6" ${O(2)}/><g class="fl2"><path d="M-4,-40q-4,-20 4,-30q8,10 4,30z" fill="#ffb347"/></g></g>`,
    coconut: `<g transform="translate(12,150) scale(.55)">${COCONUT(0, 0, 1, true)}</g>`,
    stickfish: `<g transform="translate(0,118)">${STICKFISH(0, 0, 0.42, -80)}</g>`,
    puffball: `<g transform="translate(10,130) scale(.5)">${PUFFER("", { puff: 1, seed: 29 })}</g>`,
  });

  window.Isle = { PALM, BOULDER, SHRINE, LAMP, FIRE, LONGTAIL, PUFFER, COCONUT, STICKFISH, PHONE, ISLAND, sea, sand, wash, stars, moon, clouds, life, puff, TONGHAND };
  Object.assign(Sets, { porch, boatIn, seaWide, beach, pool, lieDown, shrineClose });
})();
