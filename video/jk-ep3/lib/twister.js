// ---------- ลมงวงช้างกลางกรุง · hook stills (lane A, 1 Nov): a tornado coming down a Bangkok road, people running to hide under the expressway ----------
//   Sets.bkk(L, o)   green-black storm sky with a wall cloud, the city's towers (plain blocks, no real landmarks), the elevated expressway on
//                    round pillars across the frame (#id-xway), a six-lane road with taxis/tuk-tuk silhouettes, street lamps, a footbridge sign
//   Tw.funnel(layer, x, y, h, w, id)  the funnel: a ragged cone from the cloud base to the ground, banded, with a debris skirt at its foot
//   Tw.debris(layer, box, n, seed)    zinc sheets, signs, branches and leaves flying across
//   Tw.jets(layer, x0, x1, y)          wind-speed streaks squeezed under the deck (the venturi under the bridge)
(function () {
  const INK = "#14181a", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const blob = Pop2.blob;
  Sets.DEFS += `
    <linearGradient id="twSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1410"/><stop offset=".4" stop-color="#1e3426"/><stop offset=".7" stop-color="#4a6a3a"/><stop offset="1" stop-color="#8a9a5a"/></linearGradient>
    <linearGradient id="twCone" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a3428"/><stop offset=".35" stop-color="#5a6a52"/><stop offset=".55" stop-color="#7a8a6a"/><stop offset="1" stop-color="#1a2018"/></linearGradient>
    <linearGradient id="twDeck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a9088"/><stop offset="1" stop-color="#4a504a"/></linearGradient>
    <linearGradient id="twPillar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a605a"/><stop offset=".4" stop-color="#9aa098"/><stop offset="1" stop-color="#3a403a"/></linearGradient>
    <linearGradient id="twRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4040"/><stop offset="1" stop-color="#1a1e1e"/></linearGradient>
    <linearGradient id="twStreak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d8e8d0" stop-opacity="0"/><stop offset=".7" stop-color="#e8f2e0" stop-opacity=".7"/><stop offset="1" stop-color="#e8f2e0" stop-opacity="0"/></linearGradient>
    <radialGradient id="twDust"><stop offset="0" stop-color="#6a6a50" stop-opacity=".9"/><stop offset="1" stop-color="#4a4a38" stop-opacity="0"/></radialGradient>
    <radialGradient id="twBolt"><stop offset="0" stop-color="#eaffe8" stop-opacity=".9"/><stop offset="1" stop-color="#9affc0" stop-opacity="0"/></radialGradient>`;
  const Tw = {};
  Sets.bkk = (L, o = {}) => {
    const id = o.id || "bk", r = mk(o.seed || 5), G = o.ground ?? 1500, XY = o.xway ?? 1010;
    // sky + wall cloud
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#twSky)"/>`;
    for (let k = 0; k < 16; k++) { const x = -1200 + k * 230, y = 120 + (k % 3) * 60; sky += `<path d="${blob(x, y, 220 + r() * 120, r, 10)}" fill="${k % 2 ? "#18241c" : "#223228"}" opacity=".95"/>`; }
    for (let k = 0; k < 10; k++) { const x = -1000 + k * 360, y = 420 + r() * 80; sky += `<path d="${blob(x, y, 160 + r() * 80, r, 9)}" fill="#2e4232" opacity=".9"/><path d="M${x - 150},${y + 60}q150,30 300,0" stroke="#5a7a4a" stroke-width="6" opacity=".4" fill="none"/>`; }
    sky += `<g transform="translate(${o.boltX ?? 900},40)"><circle r="260" fill="url(#twBolt)" opacity=".35"/><path d="M0,0L-40,180L20,170L-30,360L60,150L0,160L40,0Z" fill="#eaffea" opacity=".85"/></g>`;
    put(L.sky, sky);
    // the city: towers in rain haze
    let far = "";
    for (let k = 0; k < 22; k++) { const x = -1200 + k * 170 + r() * 60, w = 90 + r() * 110, h = 260 + r() * 520;
      far += `<rect x="${f1(x)}" y="${f1(G - 340 - h)}" width="${f1(w)}" height="${f1(h + 40)}" fill="${k % 2 ? "#2a382e" : "#34443a"}"/>`;
      for (let j = 0; j < 8; j++) far += `<rect x="${f1(x + 10 + (j % 3) * w / 3.4)}" y="${f1(G - 320 - h + 30 + Math.floor(j / 3) * 60)}" width="10" height="16" fill="#c8d890" opacity="${f1(0.15 + r() * 0.35)}"/>`; }
    far += `<rect x="-1300" y="${G - 420}" width="3700" height="200" fill="#5a6a4a" opacity=".35"/>`;
    put(L.far, far);
    // mid: road side buildings (shophouses), lamp posts, billboard
    let mid = "";
    for (let k = 0; k < 14; k++) { const x = -1200 + k * 260; mid += `<rect x="${x}" y="${G - 360}" width="250" height="300" fill="#4a524a" ${O(3)}/><rect x="${x}" y="${G - 360}" width="250" height="40" fill="#5a2a22"/>`;
      for (let j = 0; j < 3; j++) mid += `<rect x="${x + 20 + j * 76}" y="${G - 300}" width="56" height="70" fill="#1a2420" ${O(2)}/>`; mid += `<rect x="${x + 10}" y="${G - 180}" width="230" height="120" fill="#2a302a"/>`; }
    put(L.mid, mid);
    // set: road + the expressway deck on pillars
    let s = `<rect x="-1300" y="${G - 70}" width="3700" height="1800" fill="url(#twRoad)"/>`;
    for (let k = 0; k < 6; k++) s += `<path d="M-1300,${G + k * 120}H2400" stroke="#e8e8e0" stroke-width="${3 + k * 1.5}" stroke-dasharray="${60 + k * 20} ${50 + k * 16}" opacity=".6"/>`;
    s += `<path d="M-1300,${G - 60}H2400" stroke="#e8c03a" stroke-width="8"/>`;
    // pillars + deck
    for (let k = 0; k < 7; k++) { const px = -800 + k * 480; s += `<rect x="${px - 50}" y="${XY}" width="100" height="${G + 60 - XY}" fill="url(#twPillar)" ${O(3)}/><rect x="${px - 90}" y="${XY - 10}" width="180" height="50" fill="#7a807a" ${O(3)}/>`; }
    s += `<g id="${id}-xway"><rect x="-1300" y="${XY - 140}" width="3700" height="130" fill="url(#twDeck)" ${O(4)}/><rect x="-1300" y="${XY - 170}" width="3700" height="34" fill="#a8aea8" ${O(3)}/>
      <path d="M-1300,${XY - 152}H2400" stroke="#d8dcd8" stroke-width="4"/>${Array.from({ length: 40 }, (_, k) => `<path d="M${-1300 + k * 95},${XY - 170}v-26" stroke="#8a908a" stroke-width="6"/>`).join("")}
      <rect x="-1300" y="${XY - 10}" width="3700" height="30" fill="#1a1e1a" opacity=".6"/></g>`;
    // shadow under the deck
    s += `<rect x="-1300" y="${XY + 20}" width="3700" height="${G - XY}" fill="#000" opacity=".28"/>`;
    put(L.set, s);
  };
  Tw.funnel = (layer, x, y, h, w, id = "tw", o = {}) => { const r = mk(o.seed || 3), bend = o.bend ?? 0.18;
    // a curving spine from the cloud base (0,0) to the ground (bend·h, h); the column is a chain of ragged blobs, widest at the top
    const N = 34; let back = "", body = "", bands = "";
    for (let k = 0; k <= N; k++) { const u = k / N, sx = Math.sin(u * Math.PI * 0.9) * bend * h * (1 - u * 0.3) + u * u * bend * h * 0.5, sy = u * h,
        rad = (w / 2) * (1 - u) ** (o.pow ?? 2.4) + w * 0.03 * (1 - u * 0.5) + 12;
      back += `<path d="${blob(sx + 12, sy, rad * 1.1, r, 9)}" fill="#1e2a20" opacity=".9"/>`;
      body += `<path d="${blob(sx, sy, rad, r, 10)}" fill="${k % 3 ? (o.c1 || "#7c8c72") : (o.c2 || "#93a286")}"/><path d="${blob(sx + rad * 0.35, sy, rad * 0.62, r, 8)}" fill="#3a4a38" opacity=".55"/>`;
      if (k % 2 === 0 && k < N - 2) bands += `<path d="M${f1(sx - rad * 0.95)},${f1(sy + 6)}Q${f1(sx)},${f1(sy + rad * 0.32)} ${f1(sx + rad * 0.95)},${f1(sy - rad * 0.12)}" stroke="${k % 4 ? "#7a8a6a" : "#222c22"}" stroke-width="${f1(3 + rad * 0.05)}" fill="none" opacity=".7"/>`; }
    const gx = Math.sin(0.9 * Math.PI) * bend * h * 0.7 + bend * h * 0.5;
    // the ground debris cloud: a wide churning skirt of dust and pieces
    let skirt = ""; for (let k = 0; k < 26; k++) { const a = r() * Math.PI * 2, d = 40 + r() * (o.skirt ?? 380); skirt += `<path d="${blob(gx + Math.cos(a) * d, h - 30 + Math.sin(a) * d * 0.3 - r() * 120, 60 + r() * 90, r, 8)}" fill="${k % 2 ? "#4a4a3a" : "#5e5c46"}" opacity=".85"/>`; }
    for (let k = 0; k < 40; k++) { const a = r() * Math.PI * 2, d = 80 + r() * 420; skirt += `<rect x="${f1(gx + Math.cos(a) * d)}" y="${f1(h - 80 + Math.sin(a) * d * 0.5 - r() * 300)}" width="${f1(6 + r() * 18)}" height="${f1(4 + r() * 8)}" fill="#1a1a14" transform="rotate(${f1(r() * 180)} ${f1(gx + Math.cos(a) * d)} ${f1(h - 80)})"/>`; }
    put(layer, `<g transform="translate(${x},${y})"><g id="${id}">${back}${body}${bands}${skirt}</g></g>`); };
  Tw.debris = (layer, box, n = 30, seed = 9) => { const r = mk(seed), [bx, by, bw, bh] = box; let g = "";
    for (let k = 0; k < n; k++) { const x = bx + r() * bw, y = by + r() * bh, a = r() * 360, t = k % 4, sc = 0.5 + r() * 1.2;
      g += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(a)}) scale(${f1(sc)})">${t === 0 ? `<path d="M-40,-14L40,-20L44,14L-36,20Z" fill="#8a9298" ${O(2)}/><path d="M-30,-10L-26,16M-10,-12L-6,18M10,-14L14,16" stroke="#5a646a" stroke-width="2"/>`
        : t === 1 ? `<rect x="-30" y="-20" width="60" height="40" fill="#d8342a" ${O(2)}/><text y="8" font-family="Kanit" font-weight="900" font-size="18" fill="#fff" text-anchor="middle">ลด</text>`
        : t === 2 ? `<path d="M-40,0Q0,-10 40,4M-10,-2l-10,-16M14,0l12,-14" stroke="#4a3a24" stroke-width="6" fill="none"/>` : `<path d="M0,-12Q12,0 0,14Q-12,0 0,-12Z" fill="#4a7a30"/>`}</g>`; }
    put(layer, `<g>${g}</g>`); };
  Tw.jets = (layer, x0, x1, y, n = 9) => { let g = ""; for (let k = 0; k < n; k++) { const yy = y + k * 34, len = 300 + (k % 3) * 160, xs = x0 + (k * 97) % (x1 - x0 - len);
      g += `<path d="M${xs},${yy}Q${xs + len * 0.5},${yy - 8} ${xs + len},${yy + 4}" stroke="url(#twStreak)" stroke-width="${3 + (k % 3) * 2}" stroke-linecap="round" fill="none"/>`; }
    put(layer, `<g>${g}</g>`); };
  window.Tw = Tw;
})();
