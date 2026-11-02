// Sets, props and UI for "รูพญานาค" (a sinkhole opens in a rice field of a fictional Isan village on the Mekong at harvest time;
// the village calls it the naga's hole and comes at night for lottery numbers).
//   Sets.rupField(L, o)   the field world: morning (or o.time "dusk" | "night") sky, the Mekong and the Lao hills, sugar palms and
//                         bamboo, stilt houses with a rice granary and the sim's roof, golden paddies with bunds in perspective,
//                         and THE HOLE at o.hole = { x, y, rx, ry } (o.hole false = the field before it opened) with layered walls,
//                         roots, rice leaning in, rim cracks (#id-ck0…, grow them with Rup.cracks), offerings and the headman's sign
//                         (o.sign: the title "รูพญานาค" + o.ep). o.crowd: villagers' incense, garlands, phone lights.
//   Sets.rupCut(L, o)     the cross-section: a block of ground cut open like a museum model — field and well on top, soil, then
//                         limestone with joints, groundwater in the cracks, a cave under the field, the well pipe and pump.
//                         Animate with Rup.cutLife (water table drops, the cave roof ravels, the ground sinks).
//   Rup.cracks(tl, id, t0, dur)  draw the rim cracks out (stroke-dash) · Rup.life(tl, id, t0, dur) incense smoke, rice sway, crumbs
//   RupUI.palm(...)       the rules card: ยาย's palm-leaf manuscript (ใบลาน) on its string, three rhymed lines, ticks
//   Rup.mural(L, o)       the ฮูปแต้ม wall of the village sim: the naga coiled under the earth, Isan folk style (ochre, indigo, white)
(function () {
  const Rup = (window.Rup = window.Rup || {});
  const RupUI = (window.RupUI = window.RupUI || {});
  const f = (v) => (+v).toFixed(1);
  const LINE = "#2a1c16";
  const ln = (w = 3) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const rng = (seed) => { let s = seed % 2147483647; if (s <= 0) s += 2147483646; return () => (s = (s * 16807) % 2147483647) / 2147483647; };
  const rgb = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.substr(i, 2), 16)); };
  const hex = (a) => "#" + a.map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
  const mix = (a, b, k) => { const A = rgb(a), B = rgb(b); return hex(A.map((v, i) => v + (B[i] - v) * k)); };
  Rup.mix = mix; Rup.rng = rng;

  Sets.DEFS += `
    <linearGradient id="rpSkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f9fe0"/><stop offset=".55" stop-color="#9fd2f2"/><stop offset="1" stop-color="#f6ead0"/></linearGradient>
    <linearGradient id="rpSkyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3266"/><stop offset=".5" stop-color="#b8607a"/><stop offset="1" stop-color="#f6b070"/></linearGradient>
    <linearGradient id="rpSkyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b1e"/><stop offset=".6" stop-color="#16224a"/><stop offset="1" stop-color="#2c3a5e"/></linearGradient>
    <linearGradient id="rpRiver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8c8c4"/><stop offset="1" stop-color="#8a9a8a"/></linearGradient>
    <linearGradient id="rpPaddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8b44a"/><stop offset=".5" stop-color="#e8c25a"/><stop offset="1" stop-color="#c89a32"/></linearGradient>
    <linearGradient id="rpPaddyN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e3446"/><stop offset="1" stop-color="#3a3a3a"/></linearGradient>
    <radialGradient id="rpHoleDark" cx=".5" cy=".62" r=".6"><stop offset="0" stop-color="#050302"/><stop offset=".6" stop-color="#140c08"/><stop offset="1" stop-color="#2a1a10"/></radialGradient>
    <linearGradient id="rpWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3a24"/><stop offset=".22" stop-color="#8a4a2a"/><stop offset=".45" stop-color="#b0623a"/>
      <stop offset=".62" stop-color="#7a6a5a"/><stop offset=".8" stop-color="#3a2c22"/><stop offset="1" stop-color="#0a0604"/></linearGradient>
    <linearGradient id="rpLime" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8d2c2"/><stop offset="1" stop-color="#b4ac9a"/></linearGradient>
    <linearGradient id="rpWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6ab8d8" stop-opacity=".85"/><stop offset="1" stop-color="#2a6a98" stop-opacity=".9"/></linearGradient>
    <radialGradient id="rpCandle"><stop offset="0" stop-color="#fff2c0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffb84a" stop-opacity=".45"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="rpPhone"><stop offset="0" stop-color="#eef6ff" stop-opacity=".85"/><stop offset=".4" stop-color="#b8d8ff" stop-opacity=".3"/><stop offset="1" stop-color="#b8d8ff" stop-opacity="0"/></radialGradient>
    <filter id="rpBlur3" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
    <filter id="rpBlur8" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
    <filter id="rpBlur16" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>`;

  // ---------------- small pieces ----------------
  // a sugar palm (ตาลโตนด): a tall bare trunk with ring scars and a ball of fan leaves — the Isan skyline, never a broccoli
  Rup.palm = (x, y, h, s = 1, c = "#3a5a3a", r = rng(7)) => {
    let g = `<g transform="translate(${f(x)},${f(y)}) scale(${s})"><path d="M-7,0Q-4,${-h * 0.5} -5,${-h}L5,${-h}Q4,${-h * 0.5} 8,0Z" fill="${mix(c, "#5a4a3a", 0.6)}"/>`;
    for (let k = 1; k < 8; k++) g += `<path d="M-6,${f(-h * k / 8)}h12" stroke="${mix(c, "#2a1a10", 0.5)}" stroke-width="1.6" opacity=".5"/>`;
    const n = 15;
    for (let k = 0; k < n; k++) { const a = -Math.PI * (0.05 + 0.9 * k / (n - 1)) + (r() - 0.5) * 0.15, L = 46 + r() * 22, ex = Math.cos(a) * L, ey = -h + Math.sin(a) * L * 0.9;
      const w = 0.5; let fan = `M0,${-h}`;
      for (let j = -3; j <= 3; j++) { const b = a + j * 0.09 * w; fan += `L${f(Math.cos(b) * L)},${f(-h + Math.sin(b) * L * 0.9)}`; }
      g += `<path d="${fan}Z" fill="${k % 3 ? c : mix(c, "#9ac87a", 0.35)}" opacity=".95"/><path d="M0,${-h}L${f(ex)},${f(ey)}" stroke="${mix(c, "#1a2a1a", 0.4)}" stroke-width="1.4" opacity=".6"/>`; }
    g += `<ellipse cx="0" cy="${-h + 4}" rx="9" ry="7" fill="${mix(c, "#2a1a10", 0.5)}"/></g>`;
    return g;
  };
  // a broad village tree (mango / tamarind): a forked trunk and an uneven crown built from many pointed leaf clusters, lit from the
  // upper right, dark underside — irregular, never a round broccoli head
  Rup.tree = (x, y, h, c = "#3e6a34", r = rng(19)) => {
    let g = `<g transform="translate(${f(x)},${f(y)})"><path d="M-10,0Q-6,${-h * 0.4} -30,${-h * 0.7}M8,0Q4,${-h * 0.45} 34,${-h * 0.72}M0,0V${-h * 0.6}" stroke="${mix(c, "#4a3424", 0.7)}" stroke-width="12" fill="none" stroke-linecap="round"/>`;
    const lobes = 7 + Math.floor(r() * 4);
    for (let k = 0; k < lobes; k++) { const lx = (r() - 0.5) * h * 0.95, ly = -h * 0.62 - r() * h * 0.42 + Math.abs(lx) * 0.25, R = h * (0.14 + r() * 0.1);
      for (let j = 0; j < 14; j++) { const a = r() * Math.PI * 2, d = r() * R, px = lx + Math.cos(a) * d, py = ly + Math.sin(a) * d * 0.8, rot = r() * 180, lit = (px - lx) - (py - ly);
        g += `<path d="M${f(px - 12)},${f(py)}q12,-9 24,0q-12,9 -24,0Z" fill="${lit > 6 ? mix(c, "#b8d87a", 0.35) : lit < -10 ? mix(c, "#142a14", 0.45) : c}" transform="rotate(${f(rot)} ${f(px)} ${f(py)})"/>`; } }
    return g + "</g>";
  };
  // a clump of bamboo: thin culms arching out, nodes, feathery leaf sprays
  Rup.bamboo = (x, y, h, s = 1, c = "#5a8a3a", r = rng(11)) => {
    let g = `<g transform="translate(${f(x)},${f(y)}) scale(${s})">`;
    for (let k = 0; k < 9; k++) { const lean = (k - 4) * 0.13 + (r() - 0.5) * 0.08, H = h * (0.75 + r() * 0.3), ex = Math.sin(lean) * H, ey = -Math.cos(lean) * H;
      g += `<path d="M${(k - 4) * 5},0Q${f(ex * 0.3)},${f(ey * 0.6)} ${f(ex)},${f(ey)}" stroke="${mix(c, "#a8b05a", 0.3)}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
      for (let j = 1; j < 5; j++) { const t = j / 5; g += `<circle cx="${f(ex * t * t * 0.9 + (k - 4) * 5 * (1 - t))}" cy="${f(ey * t)}" r="2.6" fill="${mix(c, "#3a4a1a", 0.4)}"/>`; }
      for (let j = 0; j < 7; j++) { const t = 0.45 + j * 0.08, px = ex * t * t + (k - 4) * 5 * (1 - t), py = ey * t, d = (r() > 0.5 ? 1 : -1);
        g += `<path d="M${f(px)},${f(py)}q${f(d * 18)},${f(-4 + r() * 10)} ${f(d * 34)},${f(6 + r() * 10)}q${f(-d * 14)},${f(-6)} ${f(-d * 34)},${f(-6 - r() * 10)}Z" fill="${j % 2 ? c : mix(c, "#b8d88a", 0.3)}" opacity=".92"/>`; } }
    return g + "</g>";
  };
  // an Isan stilt house: a high floor on posts, a steep gable roof (corrugated), a ladder, cloth on the rail; o.granary adds a เล้าข้าว
  Rup.house = (x, y, s = 1, o = {}) => {
    const wd = o.w ?? 300, wall = o.wall ?? "#8a5a3a", roof = o.roof ?? "#7a8a96";
    let g = `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
      <ellipse cx="0" cy="6" rx="${wd * 0.62}" ry="16" fill="#2a1a10" opacity=".25"/>
      ${[-0.46, -0.16, 0.16, 0.46].map((t) => `<rect x="${f(t * wd - 7)}" y="-150" width="14" height="150" fill="#5a3a24" ${ln(2.4)}/>`).join("")}
      <rect x="${-wd / 2}" y="-176" width="${wd}" height="28" fill="#6a4228" ${ln(2.4)}/>
      <rect x="${-wd / 2 + 10}" y="-300" width="${wd - 20}" height="126" fill="${wall}" ${ln(2.4)}/>
      ${Array.from({ length: Math.floor((wd - 20) / 22) }, (_, k) => `<path d="M${-wd / 2 + 21 + k * 22},-298V-176" stroke="${mix(wall, "#2a1a10", 0.35)}" stroke-width="2"/>`).join("")}
      <rect x="${-wd * 0.12}" y="-276" width="${wd * 0.18}" height="90" fill="#2a1a12" ${ln(2.4)}/><rect x="${wd * 0.2}" y="-270" width="${wd * 0.14}" height="54" fill="#1a1410" ${ln(2.4)}/>
      <path d="M${-wd / 2 - 30},-292L0,-400L${wd / 2 + 30},-292Z" fill="${roof}" ${ln(2.6)}/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${f(-wd / 2 - 24 + k * (wd + 48) / 11)},-293L${f((k - 5.5) * 3)},-396" stroke="${mix(roof, "#2a3038", 0.3)}" stroke-width="2" opacity=".6"/>`).join("")}
      <path d="M-14,-400L0,-430L14,-400" stroke="#4a3426" stroke-width="5" fill="none"/>
      <g transform="translate(${-wd / 2 - 40},0) rotate(-24)"><path d="M0,0V-170M30,0V-170" stroke="#6a4228" stroke-width="7"/>${[1, 2, 3, 4, 5].map((k) => `<path d="M0,${-k * 30}H30" stroke="#6a4228" stroke-width="6"/>`).join("")}</g>
      <path d="M${-wd / 2 + 20},-182q30,30 60,0" fill="${o.cloth ?? "#c8403a"}" opacity=".9"/>`;
    if (o.granary) g += `<g transform="translate(${wd / 2 + 120},0)"><rect x="-56" y="-90" width="10" height="90" fill="#5a3a24"/><rect x="46" y="-90" width="10" height="90" fill="#5a3a24"/>
      <rect x="-64" y="-200" width="128" height="112" fill="#a06a3a" ${ln(2.4)}/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-64,${-190 + k * 22}H64" stroke="#7a4a28" stroke-width="2"/>`).join("")}
      <path d="M-88,-196L0,-266L88,-196Z" fill="#8a8a7a" ${ln(2.4)}/></g>`;
    return g + "</g>";
  };
  // the village sim (สิม, an Isan ordination hall): white walls, a two-tier roof with chofa and naga barge-boards
  Rup.sim = (x, y, s = 1) => `<g transform="translate(${f(x)},${f(y)}) scale(${s})">
    <rect x="-170" y="-150" width="340" height="150" fill="#f2ead8" ${ln(2.6)}/><rect x="-200" y="-12" width="400" height="20" fill="#d8ccb4" ${ln(2.4)}/>
    ${[-120, -60, 0, 60, 120].map((x) => `<rect x="${x - 12}" y="-110" width="24" height="60" rx="12" fill="#3a2a22"/>`).join("")}
    <path d="M-220,-150L0,-280L220,-150Z" fill="#c8402a" ${ln(2.6)}/><path d="M-160,-206L0,-330L160,-206Z" fill="#d85a32" ${ln(2.6)}/>
    <path d="M-220,-150Q-200,-140 -178,-152L0,-280L178,-152Q200,-140 220,-150" stroke="#f0c040" stroke-width="7" fill="none"/>
    <path d="M0,-330Q6,-352 -2,-370Q14,-362 12,-348" stroke="#f0c040" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M-220,-150q-16,-6 -18,-24M220,-150q16,-6 18,-24" stroke="#f0c040" stroke-width="7" fill="none" stroke-linecap="round"/></g>`;

  // ---------------- the field world ----------------
  Sets.rupField = (L, o = {}) => {
    const id = o.id || "rf", tm = o.time || "day", night = tm === "night", dusk = tm === "dusk", r = rng(o.seed || 23);
    const HZ = o.horizon ?? 820;   // horizon: the far bank of the Mekong
    const tint = (c) => night ? mix(c, "#1a2448", 0.62) : dusk ? mix(c, "#c8705a", 0.18) : c;
    // sky: gradient, sun or moon, soft layered cloud banks (flat bellies, lit tops)
    let sky = `<rect x="-1600" y="-900" width="4300" height="${HZ + 1000}" fill="url(#${night ? "rpSkyNight" : dusk ? "rpSkyDusk" : "rpSkyDay"})"/>`;
    if (night) { for (let k = 0; k < 90; k++) sky += `<circle cx="${f(-1200 + r() * 3500)}" cy="${f(-800 + r() * (HZ + 600))}" r="${f(0.8 + r() * 1.8)}" fill="#f4f0ff" opacity="${f(0.3 + r() * 0.6)}"/>`;
      sky += `<circle cx="820" cy="260" r="46" fill="#f8f2dc"/><circle cx="806" cy="250" r="9" fill="#e4dcc0"/><circle cx="832" cy="276" r="6" fill="#e4dcc0"/>`; }
    else sky += `<circle cx="${dusk ? 300 : 980}" cy="${dusk ? HZ - 120 : 150}" r="${dusk ? 70 : 54}" fill="${dusk ? "#ffd89a" : "#fffbe8"}"/>`;
    for (let k = 0; k < 8; k++) { const cx = -900 + k * 460 + r() * 160, cy = 120 + (k % 3) * 120 + r() * 60, w = 260 + r() * 220;
      let c = ""; for (let j = 0; j < 7; j++) c += `<ellipse cx="${f(cx + (j - 3) * w * 0.14)}" cy="${f(cy - Math.sin((j / 6) * Math.PI) * 36 - r() * 16)}" rx="${f(w * 0.16 + r() * 30)}" ry="${f(34 + r() * 18)}"/>`;
      sky += `<g opacity="${night ? 0.25 : 0.95}"><g fill="${night ? "#3a4a6a" : dusk ? "#f4c8b8" : "#ffffff"}">${c}</g><ellipse cx="${f(cx)}" cy="${f(cy + 18)}" rx="${f(w * 0.5)}" ry="20" fill="${night ? "#2a3454" : dusk ? "#c88aa0" : "#dceaf6"}"/></g>`; }
    put(L.sky, sky);
    // far: the Lao hills in three blue layers, the Mekong's wide pale band, a longtail, sugar palms on our bank
    let far = "";
    [["#8aa0c0", 0], ["#7088a8", 30], ["#5a7090", 60]].forEach(([c, dy], k) => { let d = `M-1500,${HZ - 40 + dy}`;
      for (let x = -1500; x <= 2700; x += 60) d += `L${x},${f(HZ - 70 + dy - Math.abs(Math.sin(x * 0.0021 + k * 1.7)) * (90 - k * 18) - Math.sin(x * 0.011 + k) * 12)}`;
      far += `<path d="${d}L2700,${HZ + 40}L-1500,${HZ + 40}Z" fill="${tint(c)}"/>`; });
    far += `<rect x="-1500" y="${HZ}" width="4200" height="70" fill="${tint("#b4c2bc")}"/>${Array.from({ length: 14 }, (_, k) => `<path d="M${-1200 + k * 280},${HZ + 20 + (k % 3) * 14}h${80 + (k % 4) * 30}" stroke="${tint("#e8f0ea")}" stroke-width="3" opacity=".6"/>`).join("")}
      <g transform="translate(260,${HZ + 36})"><path d="M-46,0Q-10,10 40,0L46,-6H-50Z" fill="${tint("#5a3a24")}"/><path d="M30,-6L58,-18" stroke="${tint("#3a2a1a")}" stroke-width="3"/></g>`;
    far += `<rect x="-1500" y="${HZ + 66}" width="4200" height="70" fill="${tint("#6a8a4a")}"/>`;
    for (let k = 0; k < 16; k++) far += Rup.palm(-1100 + k * 230 + r() * 80, HZ + 110 + r() * 14, 150 + r() * 70, 0.7 + r() * 0.2, tint("#3e5e3a"), r);
    put(L.far, far);
    // mid: the village tree line — bamboo, palms, stilt houses, the sim, power poles
    let mid = `<rect x="-1500" y="${HZ + 120}" width="4200" height="140" fill="${tint("#7a9a4a")}"/>`;
    for (let k = 0; k < 9; k++) mid += Rup.bamboo(-1100 + k * 420 + r() * 120, HZ + 200, 170 + r() * 60, 0.9, tint("#5a8a3a"), r);
    mid += Rup.sim(o.simX ?? -260, HZ + 214, 0.62);
    (o.houses || [[120, 0.55, true], [760, 0.6, false], [1260, 0.5, false]]).forEach(([hx, hs, gr], k) => { mid += Rup.house(hx, HZ + 222, hs, { granary: gr, wall: tint(["#8a5a3a", "#9a6a42", "#7a5236"][k % 3]), roof: tint(["#7a8a96", "#8a6a5a", "#6a7a86"][k % 3]), cloth: ["#c8403a", "#3a6ac8", "#e8b030"][k % 3] }); });
    for (let k = 0; k < 10; k++) mid += Rup.tree(-1000 + k * 330 + r() * 120, HZ + 232, 150 + r() * 70, tint(["#3e6a34", "#4a7a3a", "#36602e"][k % 3]), r);
    for (let k = 0; k < 6; k++) mid += Rup.palm(-900 + k * 520 + r() * 100, HZ + 230, 220 + r() * 60, 0.95, tint("#3a5a34"), r);
    mid += Array.from({ length: 6 }, (_, k) => `<path d="M${-800 + k * 520},${HZ + 230}V${HZ + 30}M${-830 + k * 520},${HZ + 50}h60" stroke="${tint("#5a4a3a")}" stroke-width="6"/>`).join("") +
      `<path d="M-800,${HZ + 52}${Array.from({ length: 5 }, (_, k) => `Q${-540 + k * 520},${HZ + 90} ${-280 + k * 520},${HZ + 52}`).join("")}" stroke="${tint("#3a3028")}" stroke-width="2" fill="none"/>`;
    put(L.mid, mid);
    // set: the paddies in perspective (rows of ripe heads), bunds, and the hole
    const GY = HZ + 250, FIELD = night ? "url(#rpPaddyN)" : "url(#rpPaddy)";
    let s = `<rect x="-1600" y="${GY}" width="4400" height="${2300 - GY}" fill="${FIELD}"/>`;
    for (let row = 0; row < 90; row++) { const t = row / 89, yy = GY + 6 + Math.pow(t, 1.6) * (1990 - GY), sz = 4 + t * 17, step = 18 + t * 30;
      const sh = row % 2 ? 0.06 : 0;
      s += `<path d="M-1600,${f(yy + sz * 0.15)}H2700" stroke="${tint(mix("#a87a22", "#7a5a1a", sh * 4))}" stroke-width="${f(1 + t * 5)}" opacity=".5"/>`;
      for (let x = -1500 + (row * 41) % step; x < 2600; x += step * (0.7 + r() * 0.6)) { const xx = x + (r() - 0.5) * step * 0.5, lit = r();
        const c1 = tint(lit > 0.6 ? "#f8da7a" : lit > 0.25 ? "#e8bc4a" : "#b8862a"), c2 = tint("#9a6a1e");
        s += `<g transform="translate(${f(xx)},${f(yy + (r() - 0.5) * sz * 0.4)}) rotate(${f((r() - 0.5) * 24)}) scale(${f(0.75 + r() * 0.5)})"><path d="M0,0q${f(-sz * 0.1)},${f(-sz * 0.8)} ${f(-sz * 0.5)},${f(-sz * 1.1)}M0,0q${f(sz * 0.05)},${f(-sz * 0.9)} ${f(sz * 0.4)},${f(-sz * 1.25)}M0,0q0,${f(-sz)} ${f(sz * 0.05)},${f(-sz * 1.35)}" stroke="${c2}" stroke-width="${f(0.8 + t * 2.6)}" fill="none" stroke-linecap="round"/>
          <path d="M${f(-sz * 0.5)},${f(-sz * 1.1)}q${f(-sz * 0.2)},${f(sz * 0.2)} ${f(-sz * 0.25)},${f(sz * 0.55)}M${f(sz * 0.4)},${f(-sz * 1.25)}q${f(sz * 0.25)},${f(sz * 0.2)} ${f(sz * 0.3)},${f(sz * 0.6)}M${f(sz * 0.05)},${f(-sz * 1.35)}q${f(sz * 0.18)},${f(sz * 0.1)} ${f(sz * 0.24)},${f(sz * 0.5)}" stroke="${c1}" stroke-width="${f(1.6 + t * 4.4)}" fill="none" stroke-linecap="round"/></g>`; } }
    // bunds (คันนา): raised strips running off toward the horizon, a few across
    [[-700, -260], [-120, 60], [520, 330], [1200, 620]].forEach(([x0, x1]) => { s += `<path d="M${x0},2300L${x1},${GY}" stroke="${tint("#a88a5a")}" stroke-width="26" opacity=".85"/><path d="M${x0 - 8},2300L${x1 - 4},${GY}" stroke="${tint("#6a8a3a")}" stroke-width="5" opacity=".7"/>`; });
    [GY + 90, GY + 300, GY + 680].forEach((yy) => { s += `<path d="M-1600,${yy}Q540,${yy - 18} 2700,${yy}" stroke="${tint("#a88a5a")}" stroke-width="${f(10 + (yy - GY) * 0.03)}" opacity=".8"/>`; });
    put(L.set, s);
    if (o.hole !== false) Rup.hole(L, { id, night, tint, ...(o.hole || {}) , crowd: o.crowd, sign: o.sign, ep: o.ep, cracks: o.cracks });
    if (o.fgRice !== false) { let fg = ""; const r2 = rng(91);
      for (let k = 0; k < 60; k++) { const x = -300 + k * 30 + r2() * 20, h = 160 + r2() * 160;
        fg += `<path d="M${f(x)},2000Q${f(x + 10)},${f(2000 - h * 0.6)} ${f(x + 30 + r2() * 30)},${f(2000 - h)}" stroke="${tint(k % 3 ? "#c89a3a" : "#e8c060")}" stroke-width="7" fill="none" stroke-linecap="round"/>
          <ellipse cx="${f(x + 34)}" cy="${f(2000 - h + 10)}" rx="8" ry="22" fill="${tint("#e8c060")}" transform="rotate(30 ${f(x + 34)} ${f(2000 - h + 10)})"/>`; }
      put(L.fg, `<g id="${id}-fgr" filter="url(#rpBlur8)" opacity=".9">${fg}</g>`); }
  };

  // the hole: a near-round collapse, the far wall lit and layered (topsoil, red laterite, grey clay, white limestone blocks at the
  // bottom of the light), the near lip dark; roots and rice hang over; cracks ring the rim (#id-ck0…)
  Rup.hole = (L, o) => {
    const id = o.id, x = o.x ?? 540, y = o.y ?? 1300, rx = o.rx ?? 300, ry = o.ry ?? 92, tint = o.tint || ((c) => c), r = rng(37);
    let g = `<g id="${id}-hole" transform="translate(${x},${y})">`;
    // rim cracks (arcs at 1.25–1.7 radii, the clock of the story: they grow toward whoever stands too close)
    const nc = o.cracks ?? 7;
    for (let k = 0; k < nc; k++) { const R = 1.22 + (k % 3) * 0.17 + r() * 0.06, a0 = (r() * 2 - 1) * Math.PI, a1 = a0 + 0.5 + r() * 0.9;
      let d = ""; for (let j = 0; j <= 14; j++) { const a = a0 + (a1 - a0) * j / 14, jit = (r() - 0.5) * 0.04; d += `${j ? "L" : "M"}${f(Math.cos(a) * rx * (R + jit))},${f(Math.sin(a) * ry * (R + jit) * 1.05)}`; }
      g += `<path id="${id}-ck${k}" class="${id}-ck" d="${d}" stroke="${tint("#2a1a10")}" stroke-width="${f(3 + r() * 2)}" fill="none" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="${o.crackDraw ? 100 : 0}"/>`; }
    // slumped ring of broken ground around the lip
    g += `<ellipse cx="0" cy="${f(ry * 0.12)}" rx="${f(rx * 1.16)}" ry="${f(ry * 1.3)}" fill="${tint("#8a6a3a")}"/>`;
    for (let k = 0; k < 22; k++) { const a = (k / 22) * Math.PI * 2, R = 1.08 + r() * 0.06;
      g += `<path d="M${f(Math.cos(a) * rx * R - 16)},${f(Math.sin(a) * ry * R)}l${f(14 + r() * 10)},${f(-8 - r() * 6)}l${f(16 + r() * 10)},${f(6 + r() * 6)}Z" fill="${tint(k % 2 ? "#6a4a2a" : "#9a7a4a")}"/>`; }
    // the pit: far wall (lit, banded) then the dark throat
    g += `<clipPath id="${id}-hc"><ellipse cx="0" cy="0" rx="${rx}" ry="${ry}"/></clipPath><g clip-path="url(#${id}-hc)">
      <rect x="${-rx}" y="${-ry}" width="${rx * 2}" height="${ry * 2}" fill="url(#rpWall)"/>`;
    for (let k = 0; k < 9; k++) g += `<path d="M${-rx},${f(-ry + k * ry * 0.22)}Q0,${f(-ry + k * ry * 0.22 + 10 + r() * 8)} ${rx},${f(-ry + k * ry * 0.22)}" stroke="${tint(["#4a2a18", "#a04a26", "#c87a4a", "#8a8274", "#6a5a4a"][k % 5])}" stroke-width="${f(4 + r() * 4)}" fill="none" opacity=".7"/>`;
    for (let k = 0; k < 10; k++) { const bx = (r() - 0.5) * rx * 1.4, by = -ry * 0.05 + r() * ry * 0.35; g += `<path d="M${f(bx)},${f(by)}l${f(18 + r() * 14)},-6l10,${f(14 + r() * 10)}l-24,6Z" fill="${tint("#d0c8b6")}" opacity=".75"/>`; }
    g += `<ellipse cx="0" cy="${f(ry * 0.78)}" rx="${f(rx * 0.95)}" ry="${f(ry * 0.98)}" fill="url(#rpHoleDark)"/>`;
    for (let k = 0; k < 14; k++) { const rxk = (r() - 0.5) * rx * 1.6, len = 30 + r() * 70;
      g += `<path d="M${f(rxk)},${f(-ry * 0.96)}q${f((r() - 0.5) * 20)},${f(len * 0.5)} ${f((r() - 0.5) * 30)},${f(len)}" stroke="${tint("#3a2618")}" stroke-width="${f(1.6 + r() * 2)}" fill="none" stroke-linecap="round"/>`; }
    // the near lip: a lip of topsoil seen edge-on, undercut (the overhang that will drop), grass and rice roots dangling
    g += `</g><path d="M${-rx},0A${rx},${ry} 0 0 0 ${rx},0L${f(rx * 0.97)},${f(ry * 0.16)}A${f(rx * 0.97)},${f(ry * 1.02)} 0 0 1 ${f(-rx * 0.97)},${f(ry * 0.16)}Z" fill="${tint("#4a2c18")}"/>
      <path d="M${-rx},0A${rx},${ry} 0 0 0 ${rx},0" fill="none" stroke="${tint("#c89a5a")}" stroke-width="5"/>
      ${Array.from({ length: 18 }, (_, k) => { const a = (k + 0.5) / 18 * Math.PI, px = -Math.cos(a) * rx * 0.98, py = Math.sin(a) * ry; return `<path d="M${f(px)},${f(py + 6)}q${f((r() - 0.5) * 8)},18 ${f((r() - 0.5) * 14)},${f(26 + r() * 22)}" stroke="${tint("#2a1a10")}" stroke-width="2.4" fill="none"/>`; }).join("")}
      <ellipse cx="0" cy="0" rx="${rx}" ry="${ry}" fill="none" stroke="${tint("#3a2414")}" stroke-width="4"/>`;
    // rice at the far lip leaning in, a broken bund crossing the hole
    for (let k = 0; k < 36; k++) { const a = Math.PI + (k / 35) * Math.PI, px = Math.cos(a) * rx * 1.02, py = Math.sin(a) * ry * 1.02;
      g += `<path d="M${f(px)},${f(py)}q${f(-px * 0.04)},-26 ${f(-px * 0.12)},-38" stroke="${tint(k % 2 ? "#e8c060" : "#b88a2a")}" stroke-width="4" fill="none" stroke-linecap="round"/>`; }
    g += `<path d="M${f(-rx * 1.3)},${f(-ry * 0.2)}L${f(-rx * 0.92)},${f(-ry * 0.32)}M${f(rx * 0.9)},${f(-ry * 0.42)}L${f(rx * 1.35)},${f(-ry * 0.5)}" stroke="${tint("#a88a5a")}" stroke-width="18"/>`;
    g += `</g>`;
    put(L.set, g);
    // crumbs falling into the dark (class for life)
    put(L.set, `<g transform="translate(${x},${y})">${Array.from({ length: 10 }, (_, k) => `<circle class="${id}-crumb" cx="${f((r() - 0.5) * rx * 1.4)}" cy="${f(-ry * 0.6 + r() * 20)}" r="${f(2 + r() * 3)}" fill="${tint("#6a4a2a")}" opacity="0"/>`).join("")}</g>`);
    if (o.sign !== false) Rup.sign(L, { x: x + (o.signX ?? rx * 0.62), y: y + (o.signY ?? ry * 2.6), ep: o.ep ?? "EP.1", night: o.night, id });
    if (o.crowd) Rup.offerings(L, { x, y, rx, ry, night: o.night, id });
  };
  // the headman's hand-painted sign stuck in the bund: the title of the story, in the world (S2 · H1)
  Rup.sign = (L, o) => put(L.set, `<g transform="translate(${f(o.x)},${f(o.y)}) rotate(-4)"><g id="${o.id}-sign">
    <path d="M-10,0V-150M10,0V-150" stroke="#4a2c1a" stroke-width="12"/><ellipse cx="0" cy="4" rx="40" ry="8" fill="#2a1a10" opacity=".35"/>
    <rect x="-150" y="-300" width="300" height="160" rx="10" fill="#e8d2a8" ${ln(4)}/><rect x="-150" y="-300" width="300" height="160" rx="10" fill="none" stroke="#b8945a" stroke-width="3" transform="translate(6,6)" opacity=".5"/>
    ${[0, 1, 2, 3].map((k) => `<path d="M-146,${-290 + k * 40}h292" stroke="#c8ae7a" stroke-width="2"/>`).join("")}
    <text x="0" y="-222" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#b8241e" transform="rotate(-2 0 -222)">รูพญานาค</text>
    <path d="M-116,-204q40,-8 80,0t80,0t80,0" stroke="#2a6a4a" stroke-width="7" fill="none" stroke-linecap="round"/>
    <text x="0" y="-160" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="34" fill="#2a1c16">${o.ep}</text>
    <path d="M60,-182l10,-10M70,-182l10,-10" stroke="#b8241e" stroke-width="4"/></g></g>`);
  // the offerings at the lip: incense in a banana-stem pot, marigold garlands, a small altar with candles and fruit; phone lights
  Rup.offerings = (L, o) => {
    const r = rng(53), { x, y, rx, ry, night } = o;
    let g = `<g transform="translate(${x},${y})">`;
    [[-1.32, -0.2], [-0.62, -1.6], [0.4, -1.65], [1.3, -0.35]].forEach(([u, v], k) => { const px = u * rx, py = v * ry;
      g += `<g transform="translate(${f(px)},${f(py)})"><rect x="-26" y="-34" width="52" height="34" rx="6" fill="#7aa04a" ${ln(2)}/>
        ${[-14, -4, 6, 16].map((dx) => `<path d="M${dx},-34L${dx + (r() - 0.5) * 6},-98" stroke="#c8402a" stroke-width="3"/><circle cx="${dx}" cy="-99" r="3" fill="#ffcf6a"/>`).join("")}
        <g class="${o.id}-smk" data-k="${k}">${[0, 1, 2].map((j) => `<path d="M${f(-6 + j * 6)},-104q-14,-40 6,-80t-4,-80" stroke="#e8e4dc" stroke-width="${f(5 - j)}" fill="none" opacity=".35" filter="url(#rpBlur3)"/>`).join("")}</g>
        <path d="M-34,6q34,22 68,0" stroke="#f0a020" stroke-width="12" fill="none" stroke-dasharray="2 9" stroke-linecap="round"/></g>`; });
    g += `<g transform="translate(${f(-rx * 0.05)},${f(-ry * 1.75)}) scale(.8)"><rect x="-90" y="-50" width="180" height="16" fill="#8a5a3a" ${ln(2)}/><path d="M-80,-34V0M80,-34V0" stroke="#6a4228" stroke-width="7"/>
      <ellipse cx="-44" cy="-62" rx="30" ry="12" fill="#e8c840" ${ln(2)}/><path d="M-60,-66q16,-20 32,0" fill="#f0d850" ${ln(1.6)}/>
      <rect x="2" y="-90" width="10" height="40" fill="#fff8e8" ${ln(1.6)}/><rect x="30" y="-84" width="10" height="34" fill="#fff8e8" ${ln(1.6)}/>
      <circle class="${o.id}-fl" cx="7" cy="-96" r="6" fill="#ffd060"/><circle class="${o.id}-fl" cx="35" cy="-90" r="6" fill="#ffd060"/>
      <circle cx="7" cy="-96" r="${night ? 60 : 30}" fill="url(#rpCandle)" opacity="${night ? 1 : 0.5}"/><circle cx="35" cy="-90" r="${night ? 60 : 30}" fill="url(#rpCandle)" opacity="${night ? 1 : 0.5}"/>
      <path d="M58,-62q14,-22 28,0" fill="#e8402a" ${ln(1.6)}/></g>`;
    put(L.set, g + `</g>`);
  };
  // life: incense curls, candle flicker, crumbs dropping into the hole, rice sway in the foreground
  Rup.life = (tl, id, t0, dur) => {
    document.querySelectorAll(`.${id}-smk`).forEach((el, k) => tl.fromTo(el, { x: 0, skewX: 0 }, { x: 10, skewX: -8, duration: 1.6 + k * 0.3, yoyo: true, repeat: Math.ceil(dur / 1.6), ease: "sine.inOut", immediateRender: false }, t0));
    document.querySelectorAll(`.${id}-fl`).forEach((el, k) => tl.fromTo(el, { scale: 0.8, svgOrigin: `${el.getAttribute("cx")} ${el.getAttribute("cy")}` }, { scale: 1.15, svgOrigin: `${el.getAttribute("cx")} ${el.getAttribute("cy")}`, duration: 0.12 + k * 0.03, yoyo: true, repeat: Math.ceil(dur / 0.12), ease: "sine.inOut", immediateRender: false }, t0));
    document.querySelectorAll(`.${id}-crumb`).forEach((el, k) => { const per = 0.9 + (k % 4) * 0.25;
      tl.fromTo(el, { y: 0, opacity: 1 }, { y: 60 + (k % 3) * 30, opacity: 0, duration: per, ease: "power2.in", repeat: Math.ceil(dur / per), immediateRender: false }, t0 + (k * 0.37) % per); });
    const fg = document.getElementById(`${id}-fgr`); if (fg) tl.fromTo(fg, { x: -6 }, { x: 6, duration: 1.8, yoyo: true, repeat: Math.ceil(dur / 1.8), ease: "sine.inOut", immediateRender: false }, t0);
  };
  Rup.cracks = (tl, id, t0, dur, o = {}) => document.querySelectorAll(`.${id}-ck`).forEach((el, k) =>
    tl.fromTo(el, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: dur * (0.6 + (k % 3) * 0.2), ease: o.ease || "power2.out", immediateRender: false }, t0 + (k % 4) * dur * 0.08));

  // ---------------- the cross-section (a block of the village's ground cut open) ----------------
  // o.wt0 / o.wt1: the water table before / after pumping (y) · o.stage: 0 cave full of water · 1 water drained · 2 roof raveling ·
  // 3 collapsed (the hole on top) · o.pump: the well and pump at the house · ids: #id-wt (water body), #id-cave, #id-plug (the soil
  // over the cave that drops), #id-surf (the field skin over it), #id-arrow0… (pumping arrows), .id-sand (raveling grains)
  Sets.rupCut = (L, o = {}) => {
    const id = o.id || "rc", r = rng(71), top = 560, face = 700, bot = 1760, x0 = 40, x1 = 1000, dx = 70, dy = -60;
    const wt = o.wt0 ?? 940, cx = 470, cy = 1130;
    put(L.sky, `<rect x="-1500" y="-900" width="4200" height="3200" fill="url(#rpSkyDay)"/><rect x="-1500" y="1700" width="4200" height="600" fill="#e8dcc0"/>`);
    let g = `<g id="${id}-block">`;
    // the top: the field skin in perspective with a bund and the house + well at the right
    g += `<path d="M${x0},${face}L${x0 + dx},${face + dy}L${x1 + dx},${face + dy}L${x1},${face}Z" fill="#d8b44a" ${ln(3)}/>`;
    for (let k = 0; k < 120; k++) { const px = x0 + 20 + r() * (x1 - x0), py = face - 4 - r() * 54; g += `<path d="M${f(px)},${f(py)}q2,-8 7,-11" stroke="${r() > 0.5 ? "#f2d070" : "#a8781e"}" stroke-width="2.4" fill="none" stroke-linecap="round"/>`; }
    // the right side face (darker, for depth)
    g += `<path d="M${x1},${face}L${x1 + dx},${face + dy}L${x1 + dx},${bot + dy}L${x1},${bot}Z" fill="#8a7a64" ${ln(3)}/>`;
    // the front face: layers
    const layers = [[face, 740, "#4a2e1a", "ดินนา"], [740, 820, "#a84a26", "ศิลาแลง"], [820, 930, "#c8a070", "ดินเหนียวปนทราย"], [930, bot, "url(#rpLime)", "หินปูน"]];
    layers.forEach(([a, b, c]) => { g += `<rect x="${x0}" y="${a}" width="${x1 - x0}" height="${b - a}" fill="${c}"/>`; });
    for (let k = 0; k < 90; k++) g += `<circle cx="${f(x0 + r() * (x1 - x0))}" cy="${f(820 + r() * 110)}" r="${f(1.5 + r() * 2.5)}" fill="#8a6a4a" opacity=".5"/>`;
    for (let k = 0; k < 9; k++) g += `<path d="M${x0},${1000 + k * 85}Q${(x0 + x1) / 2},${1000 + k * 85 + (r() - 0.5) * 20} ${x1},${1000 + k * 85}" stroke="#9a9282" stroke-width="2.4" fill="none" opacity=".7"/>`;
    for (let k = 0; k < 26; k++) { const jx = x0 + 20 + r() * (x1 - x0 - 40), jy = 940 + r() * 760; g += `<path d="M${f(jx)},${f(jy)}l${f((r() - 0.5) * 10)},${f(40 + r() * 50)}" stroke="#8a8274" stroke-width="2.2"/>`; }
    // groundwater: blue in the limestone's cracks below the water table (clipped), a wavy table line
    g += `<clipPath id="${id}-lc"><rect x="${x0}" y="930" width="${x1 - x0}" height="${bot - 930}"/></clipPath>
      <g clip-path="url(#${id}-lc)"><g id="${id}-wt"><rect x="${x0}" y="${wt}" width="${x1 - x0}" height="${bot - wt + 400}" fill="#4a9ad0" opacity=".32"/>
      <path d="M${x0},${wt}${Array.from({ length: 20 }, (_, k) => `q${(x1 - x0) / 40},-8 ${(x1 - x0) / 20},0`).join("")}" stroke="#2a7ab8" stroke-width="4" fill="none"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${f(x0 + 20 + r() * (x1 - x0 - 40))},${f(wt + 30 + r() * 700)}l${f((r() - 0.5) * 8)},${f(30 + r() * 30)}" stroke="#2a7ab8" stroke-width="3" opacity=".6"/>`).join("")}</g></g>`;
    // the cave: a dissolved void with stalactites; water fills it at stage 0
    const cave = `M${cx - 260},${cy}Q${cx - 250},${cy - 120} ${cx - 120},${cy - 140}Q${cx},${cy - 170} ${cx + 140},${cy - 130}Q${cx + 270},${cy - 100} ${cx + 250},${cy + 10}Q${cx + 230},${cy + 120} ${cx + 60},${cy + 130}Q${cx - 120},${cy + 150} ${cx - 220},${cy + 90}Z`;
    g += `<path id="${id}-cave" d="${cave}" fill="#2e2620" ${ln(3)}/><clipPath id="${id}-cc"><path d="${cave}"/></clipPath>
      <g clip-path="url(#${id}-cc)"><rect id="${id}-cw" x="${cx - 300}" y="${cy - 180}" width="600" height="340" fill="#3a8ac0" opacity="${(o.stage ?? 0) === 0 ? 0.85 : 0}"/>
      <path d="${cave}" fill="none" stroke="#5a4a3a" stroke-width="22" opacity=".5"/>
      ${[[-150, 0.7], [-60, 1], [40, 0.6], [130, 0.9]].map(([dx, q]) => `<path d="M${cx + dx - 7},${cy - 150}q7,${f(30 * q)} 2,${f(42 * q)}q-5,${f(-12 * q)} -2,${f(-42 * q)}Z" fill="#a89a84" opacity=".8"/>`).join("")}
      ${Array.from({ length: 9 }, (_, k) => `<ellipse cx="${cx - 230 + k * 56}" cy="${cy + 112 - Math.abs(k - 4) * 8}" rx="${18 + (k % 3) * 8}" ry="${10 + (k % 2) * 4}" fill="#6a5a48" opacity=".85"/>`).join("")}</g>`;
    // the plug: the soil and rice skin over the cave, the piece that drops (stage 3)
    g += `<g id="${id}-plug"><path d="M${cx - 150},${face - 40}L${cx + 150},${face - 40}L${cx + 120},${cy - 140}L${cx - 120},${cy - 150}Z" fill="none"/></g>`;
    // raveling sand from the clay into the cave (stage 2)
    g += `<g>${Array.from({ length: 40 }, (_, k) => `<circle class="${id}-sand" cx="${f(cx - 40 + r() * 80)}" cy="${f(930 + r() * 40)}" r="${f(2 + r() * 2.5)}" fill="#c8a070" opacity="0"/>`).join("")}</g>`;
    // the well and pump at the house: a casing down through the layers to below the water table, the pump at the bottom
    if (o.pump !== false) { const px = 820;
      g += `<g transform="translate(${px},${face - 30})">${Rup.house(-30, -6, 0.42, { w: 260, granary: false }).replace(/^<g transform="translate\([^)]*\) scale\([^)]*\)">/, '<g transform="translate(-60,-10) scale(.42)">')}</g>
        <rect x="${px - 9}" y="${face - 40}" width="18" height="${(o.pumpY ?? 1500) - face + 40}" fill="#9aa6ae" ${ln(2.4)}/><rect x="${px - 20}" y="${(o.pumpY ?? 1500)}" width="40" height="70" rx="8" fill="#5a6a78" ${ln(2.4)}/>
        <path d="M${px - 30},${face - 40}h60v-40h-60Z" fill="#3a8ad8" ${ln(2.4)}/><path d="M${px + 30},${face - 70}h70" stroke="#2a2a2a" stroke-width="8"/>
        ${[0, 1, 2, 3, 4].map((k) => `<path id="${id}-arrow${k}" d="M${px},${(o.pumpY ?? 1500) - 40 - k * 150}l-14,22h28Z" fill="#2a7ab8" opacity="0"/>`).join("")}`; }
    // labels carved into the face like a museum model (in-world, no HUD numbers)
    layers.forEach(([a, b, c, t]) => { g += `<text x="${x0 + 22}" y="${f(Math.min(b - 14, a + 44))}" font-family="Kanit" font-weight="800" font-size="30" fill="${a >= 930 ? "#5a5246" : "#f4ead8"}" opacity=".9">${t}</text>`; });
    g += `<text x="${x0 + 22}" y="${wt - 14}" font-family="Kanit" font-weight="800" font-size="28" fill="#1e5a8a" id="${id}-wtl">น้ำใต้ดิน</text>`;
    g += `<rect x="${x0}" y="${face}" width="${x1 - x0}" height="${bot - face}" fill="none" ${ln(4)}/></g>`;
    put(L.set, g);
    // the hole that opens on top (stage 3), hidden until then
    put(L.set, `<g id="${id}-surf" opacity="${(o.stage ?? 0) >= 3 ? 1 : 0}"><ellipse cx="${cx + dx * 0.4}" cy="${face + dy * 0.45}" rx="150" ry="22" fill="#140c08" ${ln(3)}/></g>`);
  };
  // the mechanism, step by step: the pump runs (arrows climb the casing), the water table sinks, the cave drains, sand ravels from the
  // clay into the void, the roof gives and the plug drops, a hole opens in the field
  Rup.cutLife = (tl, id, t0, dur, o = {}) => {
    const wt0 = o.wt0 ?? 940, wt1 = o.wt1 ?? 1260, a = o.at || { pump: 0, drop: 0.4, drain: 1.0, ravel: 1.8, fall: dur - 1.2 };
    for (let k = 0; k < 5; k++) tl.fromTo(`#${id}-arrow${k}`, { opacity: 0, y: 30 }, { opacity: 1, y: -30, duration: 0.5, repeat: Math.ceil(dur / 0.5), ease: "none", immediateRender: false }, t0 + a.pump + k * 0.1);
    tl.fromTo(`#${id}-wt`, { y: 0 }, { y: wt1 - wt0, duration: Math.max(0.8, a.ravel - a.drop), ease: "power1.inOut", immediateRender: false }, t0 + a.drop);
    tl.fromTo(`#${id}-wtl`, { y: 0 }, { y: wt1 - wt0, duration: Math.max(0.8, a.ravel - a.drop), ease: "power1.inOut", immediateRender: false }, t0 + a.drop);
    tl.fromTo(`#${id}-cw`, { opacity: 0.85 }, { opacity: 0, duration: 0.8, ease: "power1.in", immediateRender: false }, t0 + a.drain);
    document.querySelectorAll(`.${id}-sand`).forEach((el, k) => { const per = 0.6 + (k % 4) * 0.15;
      tl.fromTo(el, { y: 0, opacity: 1 }, { y: 70 + (k % 5) * 12, opacity: 0, duration: per, ease: "power2.in", repeat: Math.ceil((dur - a.ravel) / per), immediateRender: false }, t0 + a.ravel + (k * 0.11) % per); });
    tl.fromTo(`#${id}-surf`, { opacity: 0, scale: 0.2, svgOrigin: "498 673" }, { opacity: 1, scale: 1, svgOrigin: "498 673", duration: 0.35, ease: "back.out(2)", immediateRender: false }, t0 + a.fall);
  };

  // ---------------- ยาย's yard: the stilt house and granary behind, a concrete ring well in front, banana plants, a clothesline;
  // cracks ring the house (#id-yk0…, grow with Rup.cracks(tl, id + "y", …)), the well water clear → muddy (o.muddy 0..1) ----------------
  Sets.rupYard = (L, o = {}) => {
    const id = o.id || "ry", r = rng(83), tm = o.time || "day", night = tm === "night";
    Sets.rupField(L, { ...o, id, hole: false, fgRice: false, houses: [[-700, 0.5, false], [1500, 0.5, false]] });
    const tint = (c) => night ? mix(c, "#1a2448", 0.62) : c;
    let g = `<rect x="-1600" y="1180" width="4400" height="1200" fill="${tint("#b89a6a")}"/>`;
    for (let k = 0; k < 160; k++) g += `<ellipse cx="${f(-400 + r() * 1900)}" cy="${f(1200 + r() * 800)}" rx="${f(4 + r() * 10)}" ry="${f(2 + r() * 4)}" fill="${tint(r() > 0.5 ? "#a88a5a" : "#cab088")}" opacity=".7"/>`;
    g += Rup.house(560, 1240, 1.25, { w: 330, granary: true, wall: tint("#8a5a3a"), roof: tint("#7a8a96") });
    g += [[-120, 1300], [120, 1260], [1080, 1290]].map(([bx, by]) => `<g transform="translate(${bx},${by})"><path d="M0,0V-180" stroke="${tint("#6a8a3a")}" stroke-width="18"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M0,${-170 + k * 8}q${(k % 2 ? 1 : -1) * 70},${-40 + k * 6} ${(k % 2 ? 1 : -1) * 150},${10 + k * 10}q${(k % 2 ? -1 : 1) * 70},-20 ${(k % 2 ? -1 : 1) * 150},${-10 - k * 10}Z" fill="${tint(k % 3 ? "#4a8a3a" : "#6aa84a")}" ${ln(2)}/>`).join("")}</g>`).join("");
    g += `<path d="M-200,1060Q240,1100 680,1062" stroke="${tint("#3a3028")}" stroke-width="2.4" fill="none"/>${[[-120, "#e8483a"], [20, "#3a8ad8"], [160, "#f0c040"], [320, "#fff"]].map(([x, c]) => `<path d="M${x},1074l-14,64h60l-14,-62" fill="${tint(c)}" ${ln(2)}/>`).join("")}`;
    // the cracks ring the house's posts
    for (let k = 0; k < 9; k++) { const R = 1 + (k % 3) * 0.16, a0 = r() * Math.PI * 2, a1 = a0 + 0.6 + r() * 1.0;
      let d = ""; for (let j = 0; j <= 14; j++) { const a = a0 + (a1 - a0) * j / 14; d += `${j ? "L" : "M"}${f(560 + Math.cos(a) * 340 * R + (r() - 0.5) * 8)},${f(1270 + Math.sin(a) * 60 * R + (r() - 0.5) * 6)}`; }
      g += `<path id="${id}y-ck${k}" class="${id}y-ck" d="${d}" stroke="${tint("#3a2414")}" stroke-width="${f(3 + r() * 2.5)}" fill="none" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="${o.crackDraw ? 100 : 0}"/>`; }
    // the well: a concrete ring with a wooden pulley frame, the water inside (clear → muddy), a bucket on the rim
    const wc = mix("#3a8ab8", "#9a6a3a", o.muddy ?? 0);
    g += `<g transform="translate(${o.wellX ?? 250},${o.wellY ?? 1560})"><ellipse cx="0" cy="70" rx="170" ry="30" fill="#2a1a10" opacity=".3"/>
      <rect x="-140" y="-40" width="280" height="110" fill="${tint("#c8c4b8")}" ${ln(3)}/><path d="M-140,-10H140M-140,30H140" stroke="${tint("#a8a498")}" stroke-width="3"/>
      <ellipse cx="0" cy="-40" rx="140" ry="34" fill="${tint("#d8d4c8")}" ${ln(3)}/><ellipse id="${id}-wellw" cx="0" cy="-36" rx="118" ry="26" fill="${tint(wc)}"/>
      <ellipse cx="-30" cy="-42" rx="40" ry="6" fill="#fff" opacity=".25"/>
      <path d="M-120,-40V-260M120,-40V-260M-140,-250H140" stroke="${tint("#6a4228")}" stroke-width="12"/><circle cx="0" cy="-250" r="18" fill="${tint("#8a6a4a")}" ${ln(2)}/><path d="M0,-232V-120" stroke="#e8e0c8" stroke-width="3"/>
      <g transform="translate(150,-46)"><path d="M-34,-40H34L26,20H-26Z" fill="${tint("#e8d050")}" ${ln(2.4)}/><ellipse cx="0" cy="-40" rx="34" ry="9" fill="${tint(wc)}" ${ln(2)}/></g>`;
    // the water-level notches พ่อใหญ่สิน cuts on the well post each night, each one lower (o.notches = how many; the last is fresh)
    if (o.notches) for (let k = 0; k < o.notches; k++) { const yy = -236 + k * 26, fresh = k === o.notches - 1;
      g += `<path id="${id}-n${k}" d="M-130,${yy}l20,4" stroke="${fresh ? "#f0e0c0" : tint("#2a160a")}" stroke-width="${fresh ? 5 : 4}" stroke-linecap="round"/>${fresh ? `<path d="M-130,${yy + 3}l20,4" stroke="#3a200e" stroke-width="2"/>` : ""}`; }
    g += `</g>`;
    // the door that will not shut: a skewed frame, the panel swings open on its own (#id-door)
    g += `<g transform="translate(510,895)"><path d="M-6,-4L80,4L78,118L-8,112Z" fill="#140c08" ${ln(3)}/>
      <g id="${id}-door"><path d="M0,0L74,6L72,112L-2,108Z" fill="${tint("#7a4a2a")}" ${ln(2.6)}/><path d="M10,16L64,20M8,56L62,60M6,94L60,98" stroke="${tint("#5a3418")}" stroke-width="3"/><circle cx="62" cy="62" r="4" fill="${tint("#c8a040")}"/></g>
      <path d="M-8,112L80,118" stroke="${tint("#3a2414")}" stroke-width="5"/><path d="M80,4L84,-10" stroke="${tint("#3a2414")}" stroke-width="3"/></g>`;
    if (o.leanPost) g += `<path id="${id}-lp" d="M370,1052L352,1240" stroke="#3a2414" stroke-width="22"/><path d="M370,1052L352,1240" stroke="${tint("#6a4228")}" stroke-width="16"/>`;
    if (night) {
      // a bulb under the house, its light pooled flat on the ground; the window lit with the family inside
      g += `<path d="M560,1010V1050" stroke="#2a2a2a" stroke-width="2"/><ellipse cx="560" cy="1060" rx="8" ry="11" fill="#fff0b8" stroke="#8a7a40" stroke-width="1.6"/>
        ${Rup2 && Rup2.pool ? Rup2.pool(560, 1236, 300, 70) : ""}<path d="M560,1066L380,1236H740Z" fill="#ffd890" opacity=".1" style="mix-blend-mode:screen"/>
        <rect x="642" y="902" width="58" height="68" fill="#f8c870"/>
        <rect x="642" y="902" width="58" height="68" fill="none" ${ln(2.4)}/>`;
      for (let k = 0; k < 14; k++) g += `<circle class="${id}-dust" cx="${f(400 + r() * 320)}" cy="${f(1070 + r() * 40)}" r="${f(1.6 + r() * 2.4)}" fill="#c8a878" opacity="0"/>`;
    }
    put(L.set, g);
  };
  Rup.yardLife = (tl, id, t0, dur, o = {}) => {
    if (o.door != null) tl.fromTo(`#${id}-door`, { scaleX: 1, transformOrigin: "0% 50%" }, { scaleX: 0.35, skewY: -4, transformOrigin: "0% 50%", duration: o.doorDur ?? 1.6, ease: "power1.inOut", immediateRender: false }, t0 + o.door);
    if (o.notch != null) { const el = document.querySelector(`#${id}-n${o.last}`); if (el) tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out", immediateRender: false }, t0 + o.notch); }
    document.querySelectorAll(`.${id}-dust`).forEach((el, k) => { const per = 1.1 + (k % 4) * 0.25; if (!o.dust) return;
      tl.fromTo(el, { y: 0, opacity: 0.9 }, { y: 120 + (k % 3) * 30, opacity: 0, duration: per, ease: "power1.in", repeat: Math.ceil(dur / per), immediateRender: false }, t0 + (k * 0.23) % per); });
    if (o.lean != null) tl.fromTo(`#${id}-lp`, { rotation: 0, svgOrigin: "352 1240" }, { rotation: -5, svgOrigin: "352 1240", duration: 1.6, ease: "power2.inOut", immediateRender: false }, t0 + o.lean);
  };

  // ---------------- the rules: ยาย's palm-leaf manuscript (ใบลาน) on its string ----------------
  // lines: [text…] · o.active (index of this episode's rule) · o.done [indexes ticked] · screen space (L.light)
  RupUI.palm = (tl, layer, t0, dur, o = {}) => {
    const id = `rpl${Math.round(t0 * 100)}`, lines = o.lines || ["ดินแยกเป็นวง อย่าหลงเข้าใกล้", "น้ำบ่อขุ่นแดง แจ้งแล้วถอย", "รูยังกว้างได้ ไหว้ไกลร้อยเมตร"], y = o.y ?? 760;
    let g = `<g transform="translate(540,${y})"><g id="${id}">
      <path d="M-470,-20Q-480,-200 -440,-220L440,-232Q478,-210 470,-20L462,190Q470,214 440,222L-436,232Q-472,214 -462,190Z" fill="#000" opacity=".28" transform="translate(10,16)"/>
      <path d="M-470,-20Q-480,-200 -440,-220L440,-232Q478,-210 470,-20L462,190Q470,214 440,222L-436,232Q-472,214 -462,190Z" fill="#d8b878" ${ln(4)}/>
      <path d="M-450,-200L450,-212M-454,-140L452,-150M-458,-80L456,-88" stroke="#c4a060" stroke-width="2" opacity=".6"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-450 + k * 30},-214v436" stroke="#b8945a" stroke-width="1.2" opacity=".35"/>`).join("")}
      <circle cx="-380" cy="0" r="16" fill="#3a2a1a"/><circle cx="380" cy="0" r="16" fill="#3a2a1a"/>
      <path d="M-380,0Q-420,140 -470,320" stroke="#c8302a" stroke-width="7" fill="none"/><path d="M-470,320l-16,40M-470,320l14,38" stroke="#c8302a" stroke-width="6"/>
      <text x="0" y="-150" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#3a2414">กฎของยายคำ</text>`;
    lines.forEach((t, k) => { const yy = -60 + k * 92, st = (o.done || []).includes(k) ? "done" : k === o.active ? "on" : "off";
      g += `<g id="${id}-l${k}" opacity="${st === "off" ? 0.35 : 1}"><rect x="-330" y="${yy - 44}" width="660" height="72" rx="14" fill="${st === "on" ? "#fff2c8" : "none"}" ${st === "on" ? ln(3) : ""}/>
        <text x="-290" y="${yy + 6}" font-family="Kanit" font-weight="800" font-size="44" fill="${st === "on" ? "#8a1c14" : "#3a2414"}">${k + 1}. ${t}</text>
        ${st === "done" ? `<g transform="translate(300,${yy - 10})"><circle r="26" fill="#2fa864" ${ln(3)}/><path d="M-12,0l8,10l16,-18" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g>` : ""}</g>`; });
    put(layer, g + `</g></g>`);
    const el = document.getElementById(id);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0, y: 120, rotation: -6, svgOrigin: "0 -220" }, { opacity: 1, y: 0, rotation: 0, svgOrigin: "0 -220", duration: 0.55, ease: "back.out(2.2)", immediateRender: false }, t0);
    tl.fromTo(el, { rotation: -1.2, svgOrigin: "0 -220" }, { rotation: 1.2, svgOrigin: "0 -220", duration: 1.4, yoyo: true, repeat: Math.ceil(dur / 1.4), ease: "sine.inOut", immediateRender: false }, t0 + 0.55);
    if (o.active != null) tl.fromTo(`#${id}-l${o.active}`, { scale: 0.92, svgOrigin: "0 " + (-60 + o.active * 92) }, { scale: 1.04, svgOrigin: "0 " + (-60 + o.active * 92), duration: 0.5, yoyo: true, repeat: Math.ceil(dur / 0.5), ease: "sine.inOut", immediateRender: false }, t0 + 0.6);
    tl.to(el, { opacity: 0, duration: 0.25, immediateRender: false }, t0 + dur - 0.25);
  };
})();
