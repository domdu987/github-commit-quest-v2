// "เห็ดปอบ" v2 — the professional set kit: painted in layers with atmospheric depth, light from a named side,
// soft ambient occlusion under things, cast shadows, foreground framing, and living particles (rain, dust in light, fireflies, steam).
// Same layer contract as sets.js (sky / far / mid / set / act / fg; glow above the darkness; light = screen space). Seeded RNG only.
//   Sets.village2    the Isan village after the first rain: monsoon clouds with sun breaking through, a tree line, flooded paddies
//                    with sugar palms, the stilt house in detail (stairs, hammock, water jar, firewood), the tamarind, a red road with puddles
//                    o.time day | dusk | night · o.house [x, s] · o.tree x · o.road x · o.rain · o.rays · o.fg false
//   Sets.kok2        ป่าโคก after rain: dipterocarp trunks with bark, a high thin canopy, light shafts, red laterite, leaf litter,
//                    the termite mound with white mushrooms (o.mound [x, s], o.mush n), saplings · o.time day | dusk
//   Sets.kitchen2    the kitchen under the house at night: the clay stove's fire (#id-fire flickers), the curry pot's steam,
//                    a hanging lamp (o.lamp x), floorboards overhead leaking light, the platform with bowls and the rice basket, the water jar
//   Sets.mushHero    a hero close-up of the two white mushrooms on a banana leaf (o.v "pair" | "one"), dew, a shaft of light
//   Pop2.particles(tl, layer, o)  dust | rain | firefly | ember | steam, deterministic in timeline time
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);

  Sets.DEFS += `
    <linearGradient id="p2SkyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f7190"/><stop offset=".45" stop-color="#93adbd"/><stop offset=".8" stop-color="#d8d6c4"/><stop offset="1" stop-color="#eadcbc"/></linearGradient>
    <linearGradient id="p2SkyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2f55"/><stop offset=".45" stop-color="#7c5878"/><stop offset=".8" stop-color="#e2906a"/><stop offset="1" stop-color="#f6c48a"/></linearGradient>
    <linearGradient id="p2SkyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070e"/><stop offset=".6" stop-color="#101a2c"/><stop offset="1" stop-color="#1e2a3a"/></linearGradient>
    <linearGradient id="p2Haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8e2cf" stop-opacity="0"/><stop offset=".6" stop-color="#e8e2cf" stop-opacity=".55"/><stop offset="1" stop-color="#e8e2cf" stop-opacity="0"/></linearGradient>
    <linearGradient id="p2Ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2d0" stop-opacity=".55"/><stop offset="1" stop-color="#fff2d0" stop-opacity="0"/></linearGradient>
    <linearGradient id="p2Paddy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfd9d2"/><stop offset="1" stop-color="#8fa9a2"/></linearGradient>
    <linearGradient id="p2Earth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8744a"/><stop offset="1" stop-color="#8a4e2e"/></linearGradient>
    <linearGradient id="p2Wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6a4630"/><stop offset=".5" stop-color="#8a5e3e"/><stop offset="1" stop-color="#5e3e2a"/></linearGradient>
    <linearGradient id="p2Zinc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8c0c2"/><stop offset="1" stop-color="#7f898e"/></linearGradient>
    <radialGradient id="p2AO"><stop offset="0" stop-color="#1a120c" stop-opacity=".7"/><stop offset=".7" stop-color="#1a120c" stop-opacity=".25"/><stop offset="1" stop-color="#1a120c" stop-opacity="0"/></radialGradient>
    <radialGradient id="p2Sun"><stop offset="0" stop-color="#fff6dc" stop-opacity=".9"/><stop offset=".4" stop-color="#ffe4a8" stop-opacity=".35"/><stop offset="1" stop-color="#ffe4a8" stop-opacity="0"/></radialGradient>
    <filter id="p2Soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="12"/></filter>
    <linearGradient id="p2PudDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2f0"/><stop offset=".55" stop-color="#b4c6cc"/><stop offset="1" stop-color="#6e8a9a"/></linearGradient>
    <linearGradient id="p2PudD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd8a8"/><stop offset=".55" stop-color="#d89a8a"/><stop offset="1" stop-color="#6a4a6a"/></linearGradient>
    <linearGradient id="p2PudN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a6a"/><stop offset="1" stop-color="#101828"/></linearGradient>
    <radialGradient id="p2Puddle" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#dfe6e2"/><stop offset=".8" stop-color="#9fb2b4"/><stop offset="1" stop-color="#6f8486"/></radialGradient>
    <radialGradient id="p2Fire"><stop offset="0" stop-color="#fff0b8" stop-opacity="1"/><stop offset=".25" stop-color="#ffb04a" stop-opacity=".7"/><stop offset=".6" stop-color="#ff6a1a" stop-opacity=".22"/><stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="p2Lamp"><stop offset="0" stop-color="#fff0c8" stop-opacity=".95"/><stop offset=".3" stop-color="#ffd890" stop-opacity=".45"/><stop offset="1" stop-color="#ffc870" stop-opacity="0"/></radialGradient>
    <linearGradient id="p2Cap" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#f2efe4"/><stop offset="1" stop-color="#cfc8b4"/></linearGradient>
    <linearGradient id="p2Stem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8d2c0"/><stop offset=".4" stop-color="#fbfaf2"/><stop offset="1" stop-color="#c8c0aa"/></linearGradient>
    <linearGradient id="p2Mound" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c8804c"/><stop offset=".55" stop-color="#a8623a"/><stop offset="1" stop-color="#7a4226"/></linearGradient>
    <linearGradient id="p2CloudDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset=".45" stop-color="#e4e6e2"/><stop offset="1" stop-color="#8e9caa"/></linearGradient>
    <linearGradient id="p2CloudDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd2a0"/><stop offset=".5" stop-color="#c08a8a"/><stop offset="1" stop-color="#5e4466"/></linearGradient>
    <linearGradient id="p2CloudNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4866"/><stop offset=".5" stop-color="#202c44"/><stop offset="1" stop-color="#121a2c"/></linearGradient>
    <radialGradient id="p2LeafD" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#3e5e2c"/><stop offset="1" stop-color="#1e3418"/></radialGradient>
    <radialGradient id="p2LeafM" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#6a9440"/><stop offset="1" stop-color="#3a5a26"/></radialGradient>
    <radialGradient id="p2LeafL" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#b4d070"/><stop offset="1" stop-color="#6a9440"/></radialGradient>
    <radialGradient id="p2LeafDn" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#1a2a1e"/><stop offset="1" stop-color="#0a120c"/></radialGradient>
    <radialGradient id="p2LeafMn" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#22362a"/><stop offset="1" stop-color="#101c14"/></radialGradient>
    <radialGradient id="p2LeafLn" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#34503e"/><stop offset="1" stop-color="#1a2a20"/></radialGradient>
    <radialGradient id="p2LeafDd" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#4a4a30"/><stop offset="1" stop-color="#262418"/></radialGradient>
    <radialGradient id="p2LeafMd" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#7a6e44"/><stop offset="1" stop-color="#46402a"/></radialGradient>
    <radialGradient id="p2LeafLd" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#e0b070"/><stop offset="1" stop-color="#8a7448"/></radialGradient>
    <linearGradient id="p2GrassDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8b878"/><stop offset=".35" stop-color="#7a9a48"/><stop offset="1" stop-color="#3e5e24"/></linearGradient>
    <linearGradient id="p2GrassDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a8a6a"/><stop offset=".35" stop-color="#5e6a3a"/><stop offset="1" stop-color="#2e3a1e"/></linearGradient>
    <linearGradient id="p2GrassNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2c22"/><stop offset="1" stop-color="#0a120a"/></linearGradient>
    <linearGradient id="p2Trunk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a7a66"/><stop offset=".35" stop-color="#6a5a48"/><stop offset="1" stop-color="#3e342a"/></linearGradient>`;

  // ---------------- painting helpers ----------------
  // a scalloped blob (leaf cluster, bush): bumps round a circle of radius R
  function blob(cx, cy, R, r, n = 9) {
    const pts = Array.from({ length: n }, (_, k) => { const a = (k / n) * Math.PI * 2 + r() * 0.3, rr = R * (0.82 + r() * 0.22); return [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.86]; });
    let d = `M${f1(pts[0][0])},${f1(pts[0][1])}`;
    for (let k = 0; k < n; k++) { const [x0, y0] = pts[k], [x1, y1] = pts[(k + 1) % n], mx = (x0 + x1) / 2, my = (y0 + y1) / 2, ox = mx - cx, oy = my - cy, L = Math.hypot(ox, oy) || 1, bump = R * 0.32;
      d += `Q${f1(mx + (ox / L) * bump)},${f1(my + (oy / L) * bump)} ${f1(x1)},${f1(y1)}`; }
    return d + "Z";
  }
  // a cumulus as one soft shape: a bumpy top that swells in the middle, a flatter base; gradient lit from above; a few lit bumps on the sun side
  // a cumulus silhouette: round puffs (arcs) riding a dome envelope, bigger puffs at the crown, a soft flat base
  function cloudD(x, y, w, h, r) {
    const env = (u) => Math.pow(Math.max(0, Math.sin(Math.PI * u)), 0.8), U = [];
    for (let u = 0; u < 0.97; u += 0.07 + 0.1 * env(u) + r() * 0.05) U.push(u);
    U.push(1);
    const P = U.map((u) => [x - w / 2 + u * w, y - h * 0.62 * env(u)]);
    let d = `M${f1(P[0][0])},${f1(y)}`;
    for (let i = 1; i < P.length; i++) { const [x0, y0] = P[i - 1], [x1, y1] = P[i], R = Math.hypot(x1 - x0, y1 - y0) * (0.56 + r() * 0.2); d += `A${f1(R)},${f1(R)} 0 0 1 ${f1(x1)},${f1(y1)}`; }
    return d + `Q${f1(x + w * 0.25)},${f1(y + h * 0.07)} ${f1(x)},${f1(y + h * 0.05)}T${f1(x - w / 2)},${f1(y)}Z`;
  }
  function cloud2(x, y, w, h, r, grad, lit, base) {
    return `<path d="${cloudD(x, y, w, h, r)}" fill="url(#${grad})"/>` +
      `<path d="${cloudD(x - w * 0.06, y - h * 0.2, w * 0.7, h * 0.78, r)}" fill="${lit}" opacity=".42"/>` +
      `<path d="${cloudD(x - w * 0.12, y - h * 0.38, w * 0.38, h * 0.55, r)}" fill="${lit}" opacity=".32"/>` +
      `<ellipse cx="${f1(x + w * 0.04)}" cy="${f1(y - h * 0.02)}" rx="${f1(w * 0.4)}" ry="${f1(h * 0.07)}" fill="${base}" opacity=".28"/>`;
  }
  // a rain puddle: an irregular, perspective-flattened pool that mirrors the sky, a dark wet rim, a glint
  function smoothClosed(P) {
    const n = P.length, q = (k) => P[(k + n) % n];
    let d = `M${f1(P[0][0])},${f1(P[0][1])}`;
    for (let k = 0; k < n; k++) { const p0 = q(k - 1), p1 = q(k), p2 = q(k + 1), p3 = q(k + 2);
      d += `C${f1(p1[0] + (p2[0] - p0[0]) / 6)},${f1(p1[1] + (p2[1] - p0[1]) / 6)} ${f1(p2[0] - (p3[0] - p1[0]) / 6)},${f1(p2[1] - (p3[1] - p1[1]) / 6)} ${f1(p2[0])},${f1(p2[1])}`; }
    return d + "Z";
  }
  function puddle(px, py, rx, ry, r, t) {
    const P = Array.from({ length: 11 }, (_, k) => { const a = (k / 11) * Math.PI * 2, j = 0.72 + r() * 0.38; return [px + Math.cos(a) * rx * j, py + Math.sin(a) * ry * j]; });
    const d = smoothClosed(P), g = t === "night" ? "p2PudN" : t === "dusk" ? "p2PudD" : "p2PudDay";
    return `<path d="${d}" fill="none" stroke="${t === "night" ? "#0c0806" : "#5a3018"}" stroke-width="${f1(ry * 0.5)}" opacity=".35" stroke-linejoin="round"/>
      <path d="${d}" fill="url(#${g})"/><path d="${d}" fill="none" stroke="#2a1a10" stroke-width="2" opacity=".35"/>
      <path d="M${f1(px - rx * 0.5)},${f1(py - ry * 0.25)}h${f1(rx * 0.38)}M${f1(px + rx * 0.05)},${f1(py + ry * 0.1)}h${f1(rx * 0.22)}" stroke="#fff" stroke-width="${f1(Math.max(2, ry * 0.12))}" stroke-linecap="round" opacity="${t === "night" ? 0.25 : 0.6}"/>`;
  }
  // a broadleaf tree: a tapered trunk that forks into limbs (filled shapes, lit on the left), clusters of leaves in three depths
  function tree2(x, G, s, r, pal, o = {}) {
    const [LD, LM, LL] = pal.leaf, bark = pal.bark, barkS = pal.barkS;
    let g = `<ellipse cx="60" cy="8" rx="320" ry="44" fill="url(#p2AO)"/>`;
    g += `<path d="M-48,0Q-30,-200 -24,-430Q-120,-520 -230,-560L-214,-584Q-110,-540 -10,-470Q10,-560 70,-660L96,-646Q46,-540 30,-450Q120,-500 210,-520L214,-494Q110,-470 32,-400Q30,-200 50,0Z" fill="${bark}" ${OUT3}/>`;
    g += `<path d="M14,0Q8,-200 16,-430Q60,-480 96,-520L110,-510Q60,-460 34,-400Q34,-200 50,0Z" fill="${barkS}" opacity=".8"/>`;
    g += `<path d="M-20,-40Q-14,-200 -10,-380M8,-60Q4,-220 10,-360" stroke="${barkS}" stroke-width="4" opacity=".5" fill="none"/>`;
    const C = [[-200, -640, 190], [200, -620, 200], [0, -760, 230], [-110, -860, 170], [130, -880, 180], [-300, -540, 130], [300, -520, 120]];
    C.forEach(([cx, cy, R]) => { g += `<path d="${blob(cx + 20, cy + 30, R * 1.05, r, 10)}" fill="url(#${LD})"/>`; });
    C.forEach(([cx, cy, R]) => { g += `<path d="${blob(cx - 10, cy - 6, R * 0.85, r, 9)}" fill="url(#${LM})"/>`; });
    C.slice(0, 5).forEach(([cx, cy, R]) => { g += `<path d="${blob(cx - R * 0.35, cy - R * 0.3, R * 0.45, r, 8)}" fill="url(#${LL})"/>`; });
    for (let k = 0; k < 60; k++) { const a = r() * Math.PI * 2, d = r() * 300, lx = Math.cos(a) * d, ly = -720 + Math.sin(a) * d * 0.7; g += `<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="7" ry="3.5" transform="rotate(${f1(r() * 180)} ${f1(lx)} ${f1(ly)})" fill="${pal.fleck}" opacity=".7"/>`; }
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }
  // a cumulus: a dark base, the body, sunlit tops (light from the upper left)
  function cumulus(x, y, w, r, P) {
    let g = "";
    const n = 9;
    for (let k = 0; k < n; k++) { const px = x + (k / (n - 1) - 0.5) * w, rr = w * (0.13 + r() * 0.09); g += `<circle cx="${f1(px)}" cy="${f1(y + 20)}" r="${f1(rr)}" fill="${P[0]}"/>`; }
    for (let k = 0; k < n; k++) { const px = x + (k / (n - 1) - 0.5) * w * 0.85, rr = w * (0.12 + r() * 0.1), py = y - Math.sin((k / (n - 1)) * Math.PI) * w * 0.18; g += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(rr)}" fill="${P[1]}"/>`; }
    for (let k = 0; k < n - 2; k++) { const px = x + (k / (n - 1) - 0.55) * w * 0.8, rr = w * (0.07 + r() * 0.06), py = y - Math.sin(((k + 0.5) / (n - 1)) * Math.PI) * w * 0.22 - rr * 0.4; g += `<circle cx="${f1(px - rr * 0.25)}" cy="${f1(py - rr * 0.3)}" r="${f1(rr)}" fill="${P[2]}"/>`; }
    return g;
  }
  // a tree crown made of leaf clusters: shadow mass, mid, lit edges (light from the left), a few leaf flecks
  function crown(cx, cy, R, r, C, n = 14) {
    let g = "";
    for (let k = 0; k < n; k++) { const a = r() * Math.PI * 2, d = Math.sqrt(r()) * R * 0.75, rr = R * (0.28 + r() * 0.18); g += `<circle cx="${f1(cx + Math.cos(a) * d)}" cy="${f1(cy + Math.sin(a) * d * 0.8 + R * 0.08)}" r="${f1(rr)}" fill="${C[0]}"/>`; }
    for (let k = 0; k < n; k++) { const a = r() * Math.PI * 2, d = Math.sqrt(r()) * R * 0.7, rr = R * (0.24 + r() * 0.16); g += `<circle cx="${f1(cx + Math.cos(a) * d - R * 0.06)}" cy="${f1(cy + Math.sin(a) * d * 0.8 - R * 0.06)}" r="${f1(rr)}" fill="${C[1]}"/>`; }
    for (let k = 0; k < Math.floor(n * 0.7); k++) { const a = Math.PI * (0.85 + r() * 0.9), d = R * (0.45 + r() * 0.35), rr = R * (0.12 + r() * 0.1); g += `<circle cx="${f1(cx + Math.cos(a) * d)}" cy="${f1(cy + Math.sin(a) * d * 0.75)}" r="${f1(rr)}" fill="${C[2]}"/>`; }
    for (let k = 0; k < n * 2; k++) { const a = r() * Math.PI * 2, d = r() * R, lx = cx + Math.cos(a) * d, ly = cy + Math.sin(a) * d * 0.8; g += `<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="${f1(R * 0.035)}" ry="${f1(R * 0.018)}" transform="rotate(${f1(r() * 180)} ${f1(lx)} ${f1(ly)})" fill="${C[3] || C[2]}" opacity=".8"/>`; }
    return g;
  }
  // a sugar palm (ตาลโตนด): a tall bare trunk with leaf-scar rings, a round crown of fan leaves
  function palm(x, G, s, c, hi) {
    let g = `<path d="M-9,0Q-14,-420 -6,-820H6Q14,-420 9,0Z" fill="${c}"/>`;
    for (let k = 0; k < 14; k++) { const a = -Math.PI + (k / 13) * Math.PI, ex = Math.cos(a) * 150, ey = -820 + Math.sin(a) * 120 + 30; g += `<path d="M0,-830L${f1(ex - 30)},${f1(ey)}Q${f1(ex)},${f1(ey - 34)} ${f1(ex + 30)},${f1(ey + 6)}Z" fill="${c}"/>`; }
    for (let k = 0; k < 6; k++) { const a = -Math.PI * 0.85 + k * 0.22, ex = Math.cos(a) * 130, ey = -830 + Math.sin(a) * 100; g += `<path d="M0,-840L${f1(ex)},${f1(ey)}" stroke="${hi || c}" stroke-width="6" opacity=".5"/>`; }
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }
  // a banana plant: a pseudo-stem, broad tattered leaves with a midrib, lit on one side
  function banana(x, G, s, C) {
    let g = `<path d="M-16,0Q-20,-200 -8,-330H8Q20,-200 16,0Z" fill="${C[0]}"/>`;
    [[-150, -420, -30], [160, -440, 25], [-60, -520, -10], [90, -540, 12], [-200, -300, -55], [210, -320, 55]].forEach(([ex, ey, rot], k) => {
      const c = k % 2 ? C[1] : C[2];
      g += `<g transform="translate(0,-320) rotate(${rot})"><path d="M0,0Q${ex * 0.3},${ey * 0.2 - 60} ${ex * 0.1},${ey * 0.5}Q${ex * 0.8},${ey * 0.25 - 40} 0,0Z" fill="${c}"/><path d="M0,0Q${ex * 0.25},${ey * 0.15 - 40} ${ex * 0.1},${ey * 0.5}" stroke="${C[3]}" stroke-width="5" fill="none"/>
        ${[0.2, 0.32, 0.44].map((u) => `<path d="M${f1(ex * 0.12 * u * 4)},${f1(ey * 0.5 * u * 1.6)}l${f1(ex * 0.08)},${f1(8)}" stroke="${C[3]}" stroke-width="4" opacity=".6"/>`).join("")}</g>`;
    });
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }
  const tuft = (x, y, s, c1, c2, r) => { let g = ""; for (let k = 0; k < 7; k++) { const a = -0.9 + k * 0.3 + (r() - 0.5) * 0.2, h = (40 + r() * 40) * s; g += `<path d="M${f1(x)},${f1(y)}Q${f1(x + Math.sin(a) * h * 0.4)},${f1(y - h * 0.6)} ${f1(x + Math.sin(a) * h)},${f1(y - h * Math.cos(a))}" stroke="${k % 2 ? c1 : c2}" stroke-width="${f1(5 * s)}" fill="none" stroke-linecap="round"/>`; } return g; };

  // ---------------- the stilt house in detail; origin = ground under the middle; o.lit windows; o.under false hides the clutter ----------------
  function house2(x, G, s, o = {}) {
    const lit = !!o.lit, night = o.time === "night";
    let g = `<ellipse cx="40" cy="10" rx="440" ry="60" fill="url(#p2AO)"/>`;
    // the space under the floor, darker towards the back
    g += `<rect x="-300" y="-440" width="560" height="440" fill="#000" opacity=".22"/>`;
    // posts with grain
    [-280, -120, 40, 200].forEach((px) => { g += `<rect x="${px}" y="-450" width="30" height="450" fill="url(#p2Wood)" ${OUT3}/><path d="M${px + 9},-440V-10M${px + 19},-400V-40" stroke="#4a3020" stroke-width="2" opacity=".5"/>`; });
    if (o.under !== false) {
      // the hammock slung between two posts, the bamboo platform, the water jar, the firewood stack
      g += `<path d="M-252,-330Q-180,-210 -110,-330" stroke="#c8a868" stroke-width="10" fill="none"/><path d="M-250,-326Q-180,-190 -112,-326" stroke="#e8c27a" stroke-width="24" fill="none" opacity=".85"/>`;
      g += `<g transform="translate(110,-120)"><rect x="-120" y="0" width="240" height="22" fill="#c8a868" ${OUT3}/>${Array.from({ length: 9 }, (_, k) => `<path d="M${-110 + k * 28},2V20" stroke="#9a7a48" stroke-width="3"/>`).join("")}<path d="M-110,22V120M110,22V120" stroke="#8a6a3a" stroke-width="12"/></g>`;
      g += `<g transform="translate(330,0)"><path d="M-60,0Q-80,-80 -54,-130H54Q80,-80 60,0Z" fill="#7a4a2e" ${OUT3}/><ellipse cx="0" cy="-130" rx="58" ry="14" fill="#5a3420" ${OUT3}/><path d="M-50,-90Q0,-80 50,-90" stroke="#9a6a44" stroke-width="5" fill="none"/><path d="M-30,-118Q-20,-60 -30,-10" stroke="#ffffff" stroke-width="6" opacity=".18"/></g>`;
      g += `<g transform="translate(-200,0)">${Array.from({ length: 5 }, (_, k) => `<rect x="${-60 + (k % 2) * 8}" y="${-26 - k * 22}" width="140" height="20" rx="9" fill="${k % 2 ? "#8a6440" : "#7a5434"}" ${OUT3}/><circle cx="${84 + (k % 2) * 8}" cy="${-16 - k * 22}" r="9" fill="#c8a070" stroke="${INK}" stroke-width="2"/>`).join("")}</g>`;
    }
    // floor beam and joists
    g += `<rect x="-320" y="-470" width="600" height="34" fill="#5a3c28" ${OUT3}/>${Array.from({ length: 12 }, (_, k) => `<rect x="${-310 + k * 50}" y="-440" width="14" height="22" fill="#4a3020"/>`).join("")}`;
    // walls: vertical planks in two tones, a doorway and two windows with shutters swung open
    g += `<path d="M-300,-470V-800H260V-470Z" fill="#8a5e3e" ${OUT}/>`;
    for (let k = 0; k < 14; k++) g += `<rect x="${-300 + k * 40}" y="-800" width="40" height="330" fill="${k % 3 === 0 ? "#7e5436" : k % 3 === 1 ? "#946646" : "#875a3a"}"/><path d="M${-300 + k * 40},-800V-470" stroke="#5a3a24" stroke-width="3"/>`;
    const win = (wx) => `<rect x="${wx}" y="-720" width="110" height="140" fill="${lit ? "#ffd890" : night ? "#0a0806" : "#2a1e16"}" ${OUT3}/>${lit ? "" : `<rect x="${wx}" y="-720" width="110" height="40" fill="#000" opacity=".3"/>`}
      <path d="M${wx},-720L${wx - 60},-706V-594L${wx},-580Z" fill="#7a4e30" ${OUT3}/><path d="M${wx + 110},-720L${wx + 170},-706V-594L${wx + 110},-580Z" fill="#6a4228" ${OUT3}/>`;
    g += win(-230) + win(80);
    // gable roof: corrugated zinc with rust streaks, a deep eave shadow on the wall
    g += `<path d="M-300,-800H260V-760H-300Z" fill="#000" opacity=".3"/>`;
    g += `<path d="M-370,-790L-20,-1020L330,-790Z" fill="url(#p2Zinc)" ${OUT}/>`;
    for (let k = 0; k < 18; k++) { const u = k / 17, bx = -370 + u * 700; g += `<path d="M${f1(bx)},-790L-20,-1020" stroke="#6f797e" stroke-width="2" opacity=".6"/>`; }
    [-260, -120, 120, 230].forEach((rx) => { g += `<path d="M${rx},-790q6,-40 -4,-80" stroke="#a8643a" stroke-width="8" opacity=".55" fill="none"/>`; });
    g += `<path d="M-20,-1020L330,-790" stroke="#e8eef0" stroke-width="5" opacity=".6"/><path d="M-386,-786H346" stroke="${INK}" stroke-width="6"/>`;
    // the gable end: a wooden triangle with a vent
    g += `<path d="M-230,-800L-20,-950L190,-800Z" fill="#7a5034" ${OUT3}/><path d="M-60,-860h80" stroke="#4a3020" stroke-width="6"/>`;
    // stairs with a handrail
    g += `<path d="M262,-470L400,0" stroke="#5a3c28" stroke-width="14"/><path d="M300,-470L438,0" stroke="#5a3c28" stroke-width="14"/>${[1, 2, 3, 4, 5, 6].map((k) => `<path d="M${262 + k * 20},${-470 + k * 67}h40" stroke="#6a4630" stroke-width="10"/>`).join("")}<path d="M300,-560L460,-60" stroke="#4a3020" stroke-width="6"/>`;
    return `<g transform="translate(${f1(x)},${f1(G)}) scale(${s})">${g}</g>`;
  }

  // ---------------- Sets.village2 ----------------
  function village2(L, o = {}) {
    const id = o.id || "v2", r = mk(o.seed || 401), G = o.ground ?? 1320, t = o.time || "day", night = t === "night", dusk = t === "dusk";
    const SK = night ? "p2SkyNight" : dusk ? "p2SkyDusk" : "p2SkyDay";
    const CL = night ? ["#151c2a", "#1c2638", "#2a3448"] : dusk ? ["#6a4a64", "#b07a7c", "#f6c08e"] : ["#8696a2", "#d6dcda", "#fbf6e8"];
    let sk = `<rect x="-1300" y="-900" width="3700" height="3800" fill="url(#${SK})"/>`;
    if (!night) sk += `<circle cx="${o.sunX ?? 330}" cy="${o.sunY ?? 380}" r="520" fill="url(#p2Sun)"/>`;
    else for (let k = 0; k < 80; k++) sk += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-700 + r() * 1300)}" r="${f1(1 + r() * 2)}" fill="#e8ecff" opacity="${f1(0.25 + r() * 0.6)}"/>`;
    const CG = night ? "p2CloudNight" : dusk ? "p2CloudDusk" : "p2CloudDay";
    sk += cloud2(1500, 640, 900, 260, r, CG, CL[2], CL[0]) + cloud2(-340, 420, 1000, 300, r, CG, CL[2], CL[0]) + cloud2(1020, 300, 1200, 380, r, CG, CL[2], CL[0]) + cloud2(330, 760, 760, 220, r, CG, CL[2], CL[0]);
    if (!night && o.rays !== false) sk += Array.from({ length: 6 }, (_, k) => { const x0 = (o.sunX ?? 330) - 60 + k * 30, a = -0.45 + k * 0.16; return `<path d="M${x0},${(o.sunY ?? 380) + 60}L${f1(x0 + Math.sin(a) * 2400 - 70)},2600L${f1(x0 + Math.sin(a) * 2400 + 70)},2600Z" fill="url(#p2Ray)" opacity="${f1(0.35 + (k % 2) * 0.2)}"/>`; }).join("");
    put(L.sky, sk);
    // far: the tree line and palms, bluer and paler with distance; haze at their feet
    const FT = night ? ["#0c1218", "#111a22", "#16202a"] : dusk ? ["#5a4a62", "#6a566e", "#7a6478"] : ["#7f9698", "#8ea4a4", "#a4b6b2"];
    let f = "";
    for (let k = 0; k < 26; k++) f += crown(-1200 + k * 140 + r() * 60, G - 300 - r() * 40, 90 + r() * 50, r, [FT[0], FT[1], FT[2], FT[2]], 6);
    for (let k = 0; k < 7; k++) f += palm(-900 + k * 420 + r() * 120, G - 270, 0.45 + r() * 0.15, FT[0]);
    f += `<rect x="-1300" y="${G - 420}" width="3700" height="260" fill="url(#p2Haze)"/>`;
    put(L.far, f);
    // mid: flooded paddies holding the sky, bunds with grass, young rice; palms and a bamboo clump nearer
    const water = night ? "#162230" : dusk ? "#c69a8a" : "url(#p2Paddy)";
    let m = `<rect x="-1300" y="${G - 180}" width="3700" height="1400" fill="${water}"/>`;
    for (let k = 0; k < 7; k++) { const y = G - 170 + k * k * 14 + k * 20; m += `<path d="M-1300,${y}H2400" stroke="${night ? "#10180e" : dusk ? "#6a4a3a" : "#7a6a46"}" stroke-width="${6 + k * 2.4}"/><path d="M-1300,${y - 3 - k}H2400" stroke="${night ? "#16240f" : "#6f8f48"}" stroke-width="${3 + k}" opacity=".9"/>`; }
    for (let k = 0; k < 120; k++) { const ry = G - 160 + r() * 330, sc = 0.5 + (ry - G + 160) / 330; m += `<path d="M${f1(-1200 + r() * 3400)},${f1(ry)}l${f1(-3 * sc)},${f1(-14 * sc)}M${f1(-1195 + r() * 3400)},${f1(ry)}l${f1(3 * sc)},${f1(-16 * sc)}" stroke="${night ? "#1e3024" : "#5f9a4a"}" stroke-width="${f1(3 * sc)}" stroke-linecap="round"/>`; }
    for (let k = 0; k < 18; k++) m += `<path d="M${f1(-1200 + r() * 3400)},${f1(G - 150 + r() * 300)}h${f1(30 + r() * 80)}" stroke="#ffffff" stroke-width="2" opacity="${night ? 0.1 : 0.35}"/>`;
    [[-520, 0.8], [1360, 0.9], [1760, 0.75]].forEach(([px, ps]) => { m += palm(px, G - 120, ps, night ? "#0a1010" : dusk ? "#3a2e40" : "#4a5a48", night ? null : "#8a9a7a"); });
    put(L.mid, m);
    // set: the road, puddles, the house, the tamarind, bananas, fence, grass
    const earth = night ? "#2a1a12" : dusk ? "#8a4e36" : "url(#p2Earth)";
    let s = `<rect x="-1300" y="${G}" width="3700" height="1300" fill="url(#${night ? "p2GrassNight" : dusk ? "p2GrassDusk" : "p2GrassDay"})"/>`;
    for (let k = 0; k < 16; k++) s += `<ellipse cx="${f1(-1200 + r() * 3400)}" cy="${f1(G + 60 + r() * 800)}" rx="${f1(120 + r() * 260)}" ry="${f1(20 + r() * 50)}" fill="${k % 2 ? "#000" : "#fff"}" opacity="${night ? 0.06 : k % 2 ? 0.08 : 0.06}"/>`;
    for (let k = 0; k < 140; k++) { const gx = -1200 + r() * 3400, gy = G + 10 + r() * 900; s += tuft(gx, gy, 0.5 + (gy - G) / 700, night ? "#0e1a0a" : "#5a7a34", night ? "#1a2a12" : "#8aaa52", r); }
    const RX = o.road ?? 600;
    if (o.road !== false) {
      s += `<path d="M${RX - 380},${G + 1000}Q${RX - 80},${G + 300} ${RX - 64},${G}H${RX + 64}Q${RX + 140},${G + 300} ${RX + 520},${G + 1000}Z" fill="${earth}" opacity=".35"/>`;
      s += `<path d="M${RX - 330},${G + 1000}Q${RX - 60},${G + 300} ${RX - 50},${G}H${RX + 50}Q${RX + 120},${G + 300} ${RX + 470},${G + 1000}Z" fill="${earth}"/>`;
      for (let k = 0; k < 14; k++) { const u = r(), py = G + 40 + u * 900, px = RX + (r() < 0.5 ? -1 : 1) * (60 + u * 380) + (r() - 0.5) * 60; const sr = 6 + u * 14; s += `<ellipse cx="${f1(px + 2)}" cy="${f1(py + sr * 0.35)}" rx="${f1(sr * 1.1)}" ry="${f1(sr * 0.45)}" fill="#2a1408" opacity=".35"/><ellipse cx="${f1(px)}" cy="${f1(py)}" rx="${f1(sr)}" ry="${f1(sr * 0.6)}" fill="${night ? "#2a2420" : "#a8927c"}"/><ellipse cx="${f1(px - sr * 0.25)}" cy="${f1(py - sr * 0.22)}" rx="${f1(sr * 0.5)}" ry="${f1(sr * 0.25)}" fill="${night ? "#3a342e" : "#d8cab8"}"/>`; }
      s += `<path d="M${RX - 200},${G + 1000}Q${RX - 30},${G + 300} ${RX - 18},${G}M${RX + 300},${G + 1000}Q${RX + 70},${G + 300} ${RX + 20},${G}" stroke="${night ? "#1a100a" : "#7a4026"}" stroke-width="14" fill="none" opacity=".6"/>`;
      [[RX + 30, G + 420, 130, 22], [RX - 60, G + 230, 70, 11], [RX + 150, G + 720, 190, 36]].forEach(([px, py, rx, ry]) => { s += puddle(px, py, rx, ry, r, t); });
    }
    const [hx, hs] = o.house || [-60, 0.95];
    if (o.house !== false) s += house2(hx, G, hs, { lit: night, time: t });
    if (o.tree !== false) {
      const tx = o.tree ?? 860, sfx = night ? "n" : dusk ? "d" : "";
      s += tree2(tx, G, 1.15, r, { leaf: [`p2LeafD${sfx}`, `p2LeafM${sfx}`, `p2LeafL${sfx}`], bark: night ? "#0e0a08" : "#6a4a32", barkS: night ? "#060404" : "#3e2a1c", fleck: night ? "#2a3e30" : dusk ? "#e8c080" : "#c8dc8a" });
    }
    if (o.banana !== false) s += banana(o.bananaX ?? 300, G + 40, 0.9, night ? ["#0e180e", "#16241a", "#1e301e", "#0a1008"] : ["#5a7a3a", "#6e9a3e", "#88b44e", "#4a6a2a"]);
    if (o.fence) s += `<g>${Array.from({ length: 18 }, (_, k) => `<rect x="${o.fence[0] + k * 66}" y="${G - 230 + (k % 3) * 9}" width="18" height="${240 - (k % 3) * 9}" rx="6" fill="${night ? "#1a1410" : "#b89a62"}" stroke="${INK}" stroke-width="2"/><path d="M${o.fence[0] + k * 66 + 4},${G - 190}v30" stroke="#8a7044" stroke-width="3"/>`).join("")}
      <path d="M${o.fence[0] - 20},${G - 180}H${o.fence[0] + 1200}M${o.fence[0] - 20},${G - 80}H${o.fence[0] + 1200}" stroke="${night ? "#1a1410" : "#8a6e44"}" stroke-width="10"/></g>`;
    put(L.set, s);
    if (night) put(L.glow, `<g id="${id}-lamps"><circle cx="${hx - 175 * hs}" cy="${G - 650 * hs}" r="${240 * hs}" fill="url(#p2Lamp)" class="pglow"/><circle cx="${hx + 135 * hs}" cy="${G - 650 * hs}" r="${240 * hs}" fill="url(#p2Lamp)" class="pglow"/></g>`);
    // foreground: grass and a banana leaf edge framing the bottom corners (blur them with blur.fg)
    if (o.fg !== false) {
      const FC = night ? ["#050a04", "#0a1408"] : dusk ? ["#2a3a1a", "#3e5226"] : ["#3e5a24", "#5a7e30"];
      let fg = "";
      for (let k = 0; k < 10; k++) fg += tuft(-60 + k * 30, 2100, 3.2, FC[0], FC[1], r) + tuft(1140 - k * 30, 2120, 3.4, FC[0], FC[1], r);
      fg += `<path d="M1300,1500Q1000,1580 860,1820Q1040,1700 1300,1720Z" fill="${FC[1]}"/><path d="M1300,1610Q1060,1660 880,1810" stroke="${FC[0]}" stroke-width="10" fill="none"/>`;
      put(L.fg, fg);
    }
  }

  // ---------------- particles: deterministic in timeline time ----------------
  // o.type dust | rain | firefly | ember | steam; o.n; o.box [x, y, w, h]; o.t0, o.dur; o.seed; o.layer is any SVG group
  function particles(tl, layer, o) {
    const r = mk(o.seed || 9), n = o.n || 40, [bx, by, bw, bh] = o.box || [0, 0, 1080, 1920], T = o.type || "dust";
    const P = Array.from({ length: n }, () => ({ x: bx + r() * bw, y: by + r() * bh, ph: r() * 10, sp: 0.5 + r(), sz: r() }));
    const id = `pt${Math.floor(r() * 1e9)}`;
    const shape = (p, k) => T === "rain" ? `<path id="${id}-${k}" d="M0,0l-6,${f1(40 + p.sz * 30)}" stroke="#d8e4f0" stroke-width="${f1(2 + p.sz * 2)}" opacity="${f1(0.25 + p.sz * 0.35)}"/>`
      : T === "firefly" ? `<g id="${id}-${k}"><circle r="${f1(14 + p.sz * 10)}" fill="#e8ff9a" opacity=".18"/><circle r="${f1(3 + p.sz * 2)}" fill="#f4ffc8"/></g>`
      : T === "ember" ? `<circle id="${id}-${k}" r="${f1(2 + p.sz * 3)}" fill="#ffc86a"/>`
      : T === "steam" ? `<circle id="${id}-${k}" r="${f1(30 + p.sz * 40)}" fill="#f4f2ea" opacity=".12"/>`
      : T === "wisp" ? `<path id="${id}-${k}" d="M0,0C${f1(30 + p.sz * 20)},-60 ${f1(-30 - p.sz * 20)},-120 0,-180C${f1(24 + p.sz * 20)},-230 ${f1(-10)},-270 ${f1(10 + p.sz * 10)},-320" stroke="${o.color || "#f6f2ea"}" stroke-width="${f1(18 + p.sz * 22)}" fill="none" stroke-linecap="round" opacity="0"/>`
      : `<circle id="${id}-${k}" r="${f1(1.5 + p.sz * 2.5)}" fill="#fff6dc" opacity="${f1(0.3 + p.sz * 0.5)}"/>`;
    put(layer, `<g class="ptcl"${T === "wisp" || T === "steam" ? ` filter="url(#p2Soft)"` : ""}>${P.map(shape).join("")}</g>`);
    const els = P.map((_, k) => document.getElementById(`${id}-${k}`)), c = { t: 0 };
    const place = (t) => P.forEach((p, k) => {
      let x, y, op = null;
      if (T === "rain") { const yy = (p.y + t * 1900 * p.sp) % bh; x = p.x - yy * 0.12; y = by + yy; }
      else if (T === "firefly") { x = p.x + Math.sin(t * 0.7 * p.sp + p.ph) * 60; y = p.y + Math.cos(t * 0.5 * p.sp + p.ph * 2) * 40; op = 0.35 + 0.65 * Math.max(0, Math.sin(t * 2.2 * p.sp + p.ph)); }
      else if (T === "ember") { const yy = (p.y - by - t * 160 * p.sp + bh * 10) % bh; x = p.x + Math.sin(t * 2 + p.ph) * 18; y = by + yy; op = yy / bh; }
      else if (T === "wisp") { const u = ((t * 0.28 * p.sp + p.ph) % 1); x = p.x + Math.sin(u * 5 + p.ph) * 30; y = by + bh - u * bh * 0.7; op = Math.sin(u * Math.PI) * (o.op ?? 0.32);
        els[k].setAttribute("transform", `translate(${f1(x)},${f1(y)}) scale(${(0.7 + u * 0.8).toFixed(3)},${(0.8 + u * 0.6).toFixed(3)})`); els[k].setAttribute("opacity", f1(op)); return; }
      else if (T === "steam") { const u = ((t * 0.35 * p.sp + p.ph) % 1); x = p.x + Math.sin(u * 6 + p.ph) * 40; y = by + bh - u * bh; op = Math.sin(u * Math.PI) * 0.22; }
      else { x = p.x + Math.sin(t * 0.3 * p.sp + p.ph) * 30; y = p.y + Math.sin(t * 0.22 * p.sp + p.ph * 1.7) * 26 - t * 6 * p.sp; op = 0.25 + 0.5 * Math.max(0, Math.sin(t * 0.8 + p.ph)); }
      els[k].setAttribute("transform", `translate(${f1(x)},${f1(y)})`);
      if (op !== null) els[k].setAttribute("opacity", f1(op));
    });
    place(0);
    tl.to(c, { t: o.dur, duration: o.dur, ease: "none", immediateRender: false, onUpdate: () => place(c.t) }, o.t0);
  }

  Object.assign(Sets, { village2 });
  window.Pop2 = { cumulus, crown, palm, banana, tuft, house2, particles, blob, cloudD, cloud2, tree2, smoothClosed, puddle, mk, f1, put };
})();
