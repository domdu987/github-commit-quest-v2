// นิวเคลียร์ลงกรุงเทพ v6 · the nuke lands, played out big instead of a mushroom already standing.
//   Sets.nbJam(L, o)             the outbound jam seen from ahead at dusk: headlights toward the camera, the city behind the cars and
//                                the blast behind the city, people out on the road looking back at it. o.H horizon y · o.VX vanishing x ·
//                                o.flash hot sky 0..1 · o.bx, o.gap a dip in the skyline over the blast · o.maxD nearest car · o.id
//                                (the city rows are #id-B / #id-F, the deck #id-deck, the hot sky #id-hot: NkB.nuke drives them)
//   NkB.nuke(tl, L, t0, dur, o)  the detonation at (o.x, o.y) in L.far, scale o.s; o.at = seconds into it when the shot starts (<0: later):
//                                white-hot flash, the ball turning to fire, a shock dome and a ground ring racing out over the city, debris,
//                                the fireball climbing on its stem into a cap that rolls up and over, lit from the fire inside it, a
//                                condensation ring, the base surge pouring over the skyline, birds bursting off. o.jam = the nbJam id
//                                (silhouettes at the flash, the surge between the city rows, the sky heat); o.sx, o.sy = where ground zero
//                                sits on screen (the flash, the bloom and the lens streak live in screen space and climb with the fireball)
//   NkB.mushHTML(x, y, s, seed)  the grown mushroom in the same look, static (it also replaces the old beige "mush" stage everywhere)
//   NkB.blast / NkB.flood        the first v6 pass (kept)
// Every tween sits on the shot clock (tl, absolute seconds), so any frame can be seeked.
(function () {
  const NS = "http://www.w3.org/2000/svg", INK = "#14181a", f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const blob = Pop2.blob;
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const dk = (hex, k = 0.72) => { const n = parseInt(hex.slice(1), 16); return `rgb(${[n >> 16, (n >> 8) & 255, n & 255].map((v) => Math.round(v * k)).join(",")})`; };
  let seq = 0;
  const nid = (p) => `${p}${seq++}`;
  Sets.DEFS += `<radialGradient id="nbRing" cx=".5" cy=".5" r=".5"><stop offset=".72" stop-color="#fff4dc" stop-opacity="0"/><stop offset=".93" stop-color="#fff4dc" stop-opacity=".55"/><stop offset="1" stop-color="#fff4dc" stop-opacity="0"/></radialGradient>
    <radialGradient id="nbSkirt" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#b48a62" stop-opacity=".85"/><stop offset=".7" stop-color="#8a6448" stop-opacity=".5"/><stop offset="1" stop-color="#6a4a38" stop-opacity="0"/></radialGradient>
    <radialGradient id="nbWash"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#fff2d0"/><stop offset="1" stop-color="#ffc878" stop-opacity=".0"/></radialGradient>
    <radialGradient id="nbFire"><stop offset="0" stop-color="#ffffff"/><stop offset=".28" stop-color="#fffbe2"/><stop offset=".5" stop-color="#ffe07a"/><stop offset=".72" stop-color="#ffa03a"/><stop offset=".9" stop-color="#f05a22"/><stop offset="1" stop-color="#b8301a"/></radialGradient>
    <radialGradient id="nbCore" cx=".5" cy=".6" r=".5"><stop offset="0" stop-color="#fff6d0"/><stop offset=".25" stop-color="#ffd468"/><stop offset=".55" stop-color="#ff8a32"/><stop offset=".82" stop-color="#d84a22" stop-opacity=".9"/><stop offset="1" stop-color="#8a2a1c" stop-opacity="0"/></radialGradient>
    <linearGradient id="nbStemG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a1e22"/><stop offset=".22" stop-color="#8a3a26"/><stop offset=".42" stop-color="#f08a3a"/><stop offset=".5" stop-color="#ffd27a"/><stop offset=".58" stop-color="#f08a3a"/><stop offset=".78" stop-color="#8a3a26"/><stop offset="1" stop-color="#3a1e22"/></linearGradient>
    <radialGradient id="nbWil" cx=".5" cy=".5" r=".5"><stop offset=".5" stop-color="#ffffff" stop-opacity="0"/><stop offset=".78" stop-color="#ffffff" stop-opacity=".55"/><stop offset=".9" stop-color="#ffffff" stop-opacity=".85"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
    <radialGradient id="nbDome" cx=".5" cy="1" r="1"><stop offset=".7" stop-color="#fff2d8" stop-opacity="0"/><stop offset=".94" stop-color="#fff2d8" stop-opacity=".62"/><stop offset="1" stop-color="#fff2d8" stop-opacity="0"/></radialGradient>
    <radialGradient id="nbHL"><stop offset="0" stop-color="#ffffff"/><stop offset=".22" stop-color="#fff6d8" stop-opacity=".9"/><stop offset=".55" stop-color="#ffe2a0" stop-opacity=".28"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
    <linearGradient id="nbStreak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffb070" stop-opacity="0"/><stop offset=".35" stop-color="#ffd8a8" stop-opacity=".55"/><stop offset=".5" stop-color="#ffffff"/><stop offset=".65" stop-color="#ffd8a8" stop-opacity=".55"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></linearGradient>
    <linearGradient id="nbBeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2c8" stop-opacity=".5"/><stop offset="1" stop-color="#fff2c8" stop-opacity="0"/></linearGradient>
    <filter id="nbBlack" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 .06  0 0 0 0 .035  0 0 0 0 .07  0 0 0 1 0"/></filter>`;

  // ---------------------------------------------------------------- the smoke: flat two-tone billows (the lit face shifted toward the light)
  const TONE = {
    lit: ["#5e2620", "#d8602c", "#ffb04a"],   // the cap's underside, lit from the fire inside
    hot: ["#c84a22", "#ff9a3a", "#ffe08a"],   // the boiling core
    dk: ["#2c181e", "#4e2c2c", "#7a4a40"],    // smoke on top, a little sky light on its crown
    mid: ["#4a2222", "#8a3a2a", "#c8683a"],   // the rolling rim: half lit
    dust: ["#5a3a2c", "#a06a44", "#d89e66"],  // the base surge and the stem's skirt
  };
  function billow(x, y, R, r, tone, lx = 0, ly = 1) {
    const c = TONE[tone];
    return `<path d="${blob(x, y, R, r, 9)}" fill="${c[0]}"/><path d="${blob(x + lx * R * 0.22, y + ly * R * 0.24, R * 0.74, r, 8)}" fill="${c[1]}"/>`
      + `<path d="${blob(x + lx * R * 0.42, y + ly * R * 0.44, R * 0.34, r, 7)}" fill="${c[2]}" opacity=".9"/>`;
  }

  // the cap, centred on (0, 0) of its group: a torus of smoke rolling up the outside and in over the top, the fire showing underneath
  function capParts(r) {
    const P = { back: "", top: "", core: "", boil: [], front: "", rollL: [], rollR: [] };
    for (let k = 0; k <= 10; k++) { const a = Math.PI + ((k + (r() - 0.5) * 0.7) / 10) * Math.PI;   // the back of the ring, higher on screen
      P.back += billow(Math.cos(a) * (305 + r() * 55), -50 + Math.sin(a) * (58 + r() * 34), 108 + r() * 64, r, "dk", 0, -1); }
    for (let k = 0; k < 9; k++) { const x = -250 + k * 62 + (r() - 0.5) * 44;  // the crown
      P.top += billow(x, -170 - 46 * (1 - (x / 300) ** 2) + (r() - 0.5) * 40, 92 + r() * 58, r, "dk", -0.3, -1); }
    P.core = `<ellipse cx="0" cy="18" rx="330" ry="170" fill="url(#nbCore)"/>`;
    for (let k = 0; k < 6; k++) P.boil.push({ x: (k - 2.5) * 66 + (r() - 0.5) * 50, y: 22 + (r() - 0.5) * 80, R: 46 + r() * 52 });
    for (let k = 0; k <= 12; k++) { const a = ((k + (r() - 0.5) * 0.6) / 12) * Math.PI;              // the front of the ring, lit from below
      P.front += billow(Math.cos(a) * (318 + r() * 44), 60 + Math.sin(a) * (78 + r() * 28), 94 + r() * 58, r, "lit", 0, 1); }
    // the rim, rolling: billows on a circle round each side's cross-section (they turn up the outside and over the top)
    for (let k = 0; k < 6; k++) { const a = (k / 6) * Math.PI * 2;
      P.rollL.push({ x: -360 + Math.cos(a) * 112, y: 10 + Math.sin(a) * 112, R: 92 + r() * 30, tone: k % 2 ? "mid" : "dk" });
      P.rollR.push({ x: 360 + Math.cos(a) * 112, y: 10 + Math.sin(a) * 112, R: 92 + r() * 30, tone: k % 2 ? "dk" : "mid" }); }
    return P;
  }
  const rollHTML = (list, r) => list.map((b) => billow(b.x, b.y, b.R, r, b.tone, 0, 0.6)).join("");
  // the stem: a column of fire and dust that flares at the ground; height 700 from (0, 0) up
  function stemHTML(r) {
    let g = `<path d="M-160,0Q-80,-90 -76,-240Q-70,-470 -104,-700H104Q70,-470 76,-240Q80,-90 160,0Z" fill="url(#nbStemG)"/>
      <path d="M-26,-20Q-14,-300 -30,-690H30Q14,-300 26,-20Z" fill="#ffe3a0" opacity=".55"/>`;
    for (let k = 0; k < 11; k++) { const y = -60 - k * 60, side = k % 2 ? 1 : -1, w = 74 + 28 * Math.sin(k);
      g += billow(side * w, y, 42 + r() * 20, r, k > 7 ? "lit" : "mid", -side * 0.8, 0.2); }
    return g;
  }

  // the grown mushroom, static: same parts, no ids (replaces the old beige "mush" so every later shot matches)
  function mushHTML(x, y, s, seed = 11) {
    const r = mk(seed), P = capParts(r);
    let g = `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><circle cx="0" cy="-760" r="980" fill="url(#nkBloom)" opacity=".42"/>`;
    g += `<g>${surgeHTML(r, 0)}</g><g transform="translate(0,6)">${stemHTML(r)}</g>`;
    g += `<ellipse cx="0" cy="-470" rx="400" ry="54" fill="url(#nbWil)" opacity=".55"/>`;
    g += `<g transform="translate(0,-830)">${P.back}${P.top}${P.core}${P.boil.map((b) => billow(b.x, b.y, b.R, r, "hot", 0, 0.4)).join("")}${rollHTML(P.rollL, r)}${rollHTML(P.rollR, r)}${P.front}</g>`;
    return g + `</g>`;
  }
  // the base surge: a low wall of dust rolling out both ways (k = 0..1 how far it has spread)
  function surgeHTML(r, k = 1) {
    let g = "";
    for (let i = 0; i < 16; i++) { const side = i % 2 ? 1 : -1, d = (60 + (i >> 1) * 70) * (0.5 + 0.5 * k);
      g += billow(side * d, -30 - r() * 50, 70 + r() * 45, r, "dust", -side * 0.3, -0.6); }
    return g;
  }
  const oldBlast = Nk.blastHTML;
  Nk.blastHTML = (x, y, s, stage = "flash", seed = 11) => (stage === "mush" ? mushHTML(x, y, s, seed) : oldBlast(x, y, s, stage, seed));

  // ---------------------------------------------------------------- the set: the jam from ahead, the city and the sky behind it
  Sets.nbJam = (L, o = {}) => {
    const id = o.id || nid("nbj"), r = mk(o.seed || 23), H = o.H ?? 1120, VX = o.VX ?? 540, hot = o.flash ?? 0.25, Y = (d) => H + (1960 - H) * d;
    const bx = o.bx ?? 600, gap = o.gap ?? 0.55;
    put(L.sky, `<defs><linearGradient id="${id}-skyg" gradientUnits="userSpaceOnUse" x1="0" y1="${H - 1500}" x2="0" y2="${H + 40}">
        <stop offset="0" stop-color="#140f2a"/><stop offset=".32" stop-color="#3a1a3e"/><stop offset=".58" stop-color="#8e2e3a"/><stop offset=".8" stop-color="#e8662e"/><stop offset=".93" stop-color="#ffaa4e"/><stop offset="1" stop-color="#ffe0a0"/></linearGradient>
      <radialGradient id="${id}-hotg" gradientUnits="userSpaceOnUse" cx="${bx}" cy="${H - 260}" r="1450"><stop offset="0" stop-color="#fff6dc"/><stop offset=".18" stop-color="#ffd27a"/><stop offset=".45" stop-color="#f07a3a"/><stop offset="1" stop-color="#8a2a2a" stop-opacity="0"/></radialGradient></defs>
      <rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${id}-skyg)"/><rect id="${id}-hot" x="-1300" y="-900" width="3700" height="3900" fill="url(#${id}-hotg)" opacity="${hot}"/>`);
    let st = "";
    for (let k = 0; k < 9; k++) { const y = H - 980 + k * 104 + r() * 40, x = -200 + r() * 1500, w = 260 + r() * 300;
      st += `<path d="${blob(x, y, w, r, 11)}" transform="translate(${f1(x)},${f1(y)}) scale(1,.13) translate(${f1(-x)},${f1(-y)})" fill="${k > 5 ? "#ffb87a" : "#c8583e"}" opacity="${f1(0.18 + k * 0.04)}"/>`; }
    put(L.sky, `<g id="${id}-streaks">${st}</g>`);
    // the city: a hazy back row and a dark front row; every edge facing the blast catches its light, the faces toward us are in shadow
    const row = (n, x0, step, hmin, hvar, col, rimOp, win, seed) => { const rr = mk(seed); let t = "";
      for (let k = 0; k < n; k++) { const x = x0 + k * step + rr() * step * 0.5, w = step * (0.7 + rr() * 0.9), near = 1 - Math.min(1, Math.abs(x + w / 2 - bx) / 520);
        const h = (hmin + rr() * hvar + (k % 5 === 2 ? hvar * 0.6 : 0)) * (1 - gap * near ** 1.5), y = H - h;
        t += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h + 40)}" fill="${col}"/>`;
        if (k % 4 === 1) t += `<path d="M${f1(x + w * 0.2)},${f1(y)}L${f1(x + w * 0.5)},${f1(y - 40 - rr() * 50)}L${f1(x + w * 0.8)},${f1(y)}Z" fill="${col}"/>`;
        if (win) for (let j = 0; j < Math.floor(h / 30); j++) for (let i = 0; i < Math.floor(w / 26); i++) if (rr() < 0.42)
          t += `<rect x="${f1(x + 8 + i * 26)}" y="${f1(y + 14 + j * 30)}" width="12" height="9" fill="#ffcf7a" opacity="${f1(0.18 + rr() * 0.5)}"/>`;
        t += `<path d="M${f1(x)},${f1(y + h + 40)}V${f1(y)}H${f1(x + w)}V${f1(y + h + 40)}" fill="none" stroke="#ffd49a" stroke-width="5" opacity="${rimOp}"/>`;
        if (k % 6 === 3) t += `<rect x="${f1(x + w / 2 - 3)}" y="${f1(y - 70)}" width="6" height="70" fill="${col}"/><circle cx="${f1(x + w / 2)}" cy="${f1(y - 72)}" r="7" fill="#ff4a3a"/>`; }
      return t; };
    put(L.far, `<g id="${id}-B">${row(17, -300, 100, 190, 300, "#4a2a42", 0.5, false, 11)}</g>
      <g id="${id}-F">${row(15, -320, 112, 80, 210, "#1c1424", 0.65, true, 29)}<rect x="-1300" y="${H}" width="3700" height="90" fill="#140e1a"/></g>`);
    // the deck: road, lane lines, barriers, lamp posts; the jam three lanes wide, facing us; people out of their cars looking back
    const ex = (off, d) => VX + off * d;
    let s = `<defs><linearGradient id="${id}-road" gradientUnits="userSpaceOnUse" x1="0" y1="${H}" x2="0" y2="1960"><stop offset="0" stop-color="#b07a68"/><stop offset=".3" stop-color="#5a4450"/><stop offset="1" stop-color="#221c26"/></linearGradient>
      <linearGradient id="${id}-wall" gradientUnits="userSpaceOnUse" x1="0" y1="${H}" x2="0" y2="1960"><stop offset="0" stop-color="#7a5650"/><stop offset=".4" stop-color="#4a3440"/><stop offset="1" stop-color="#241c28"/></linearGradient></defs>
      <path d="M${ex(-1000, 0.004)},${H}L${ex(1000, 0.004)},${H}L${ex(1000, 1.1)},${Y(1.1)}L${ex(-1000, 1.1)},${Y(1.1)}Z" fill="url(#${id}-road)"/>`;
    [-330, 330].forEach((off) => { for (let k = 0; k < 14; k++) { const d0 = 0.03 * 1.33 ** k, d1 = d0 * 1.14; if (d0 > 1.1) break;
      s += `<path d="M${f1(ex(off - 8, d0))},${f1(Y(d0))}L${f1(ex(off + 8, d0))},${f1(Y(d0))}L${f1(ex(off + 8, d1))},${f1(Y(d1))}L${f1(ex(off - 8, d1))},${f1(Y(d1))}Z" fill="#f4e6d0" opacity=".55"/>`; } });
    [-1, 1].forEach((sd) => { const a = sd * 1000, b = sd * 1080;
      s += `<path d="M${ex(a, 0.004)},${H}L${ex(a, 1.1)},${Y(1.1)}L${ex(b, 1.1)},${Y(1.1) - 220}L${ex(b, 0.004)},${H - 1}Z" fill="url(#${id}-wall)" ${O(3)}/>
        <path d="M${ex(b, 0.004)},${H - 1}L${ex(b, 1.1)},${Y(1.1) - 220}" stroke="#ffd49a" stroke-width="6" opacity=".7"/>`;
      for (let k = 0; k < 9; k++) { const d = 0.05 * 1.45 ** k; if (d > 1.1) break; const px = ex(sd * 1060, d), py = Y(d) - 200 * d;
        s += `<rect x="${f1(px - 7 * d)}" y="${f1(py - 820 * d)}" width="${f1(14 * d)}" height="${f1(820 * d)}" fill="#3a3040" ${O(2)}/><path d="M${f1(px)},${f1(py - 812 * d)}L${f1(px - sd * 140 * d)},${f1(py - 836 * d)}" stroke="#3a3040" stroke-width="${f1(12 * d)}"/>
          <rect x="${f1(px - sd * 150 * d - 18 * d)}" y="${f1(py - 846 * d)}" width="${f1(36 * d)}" height="${f1(14 * d)}" fill="#fff2c8"/>`; } });
    const PAL = ["#eef0f2", "#c9ced4", "#2a2e34", "#b8262a", "#e8559a", "#9ccc3c", "#3a5a8a", "#d8c8a8", "#5a5e64", "#f2f2ee"];
    const lanes = [-660, 0, 660], ds = [0.05, 0.065, 0.085, 0.11, 0.145, 0.19, 0.25, 0.33, 0.44, 0.58, 0.76, 0.98];
    const people = o.people ?? [[0, 0.44, -1], [1, 0.33, 1], [0, 0.58, 1], [1, 0.25, -1], [0, 0.19, 1]];
    let shad = "", cars = "", glow = "", ppl = "", k = 0;
    ds.forEach((d) => lanes.forEach((off, li) => { k++;
      if (d > (o.maxD ?? 0.76)) return;
      const x = ex(off, d), y = Y(d), sc = d * 1.25, col = PAL[(k * 7 + li * 3) % PAL.length];
      const vx = x - VX, vy = y - H, len = 0.42;   // the blast is behind the city: every shadow runs toward the camera
      shad += `<path d="M${f1(x - 150 * sc)},${f1(y)}L${f1(x + 150 * sc)},${f1(y)}L${f1(x + 150 * sc + vx * len)},${f1(y + vy * len)}L${f1(x - 150 * sc + vx * len)},${f1(y + vy * len)}Z" fill="#120a14" opacity=".5"/>`;
      cars += carFront(x, y, sc, col, r);
      shad += `<path transform="translate(${f1(x)},${f1(y)}) scale(${sc.toFixed(3)})" d="M-150,-30L-300,190H-20L-90,-30ZM150,-30L300,190H20L90,-30Z" fill="url(#nbBeam)" opacity=".45"/>`;
      glow += `<g transform="translate(${f1(x)},${f1(y)}) scale(${sc.toFixed(3)})"><circle cx="-112" cy="-96" r="64" fill="url(#nbHL)"/><circle cx="112" cy="-96" r="64" fill="url(#nbHL)"/></g>`;
    }));
    people.forEach(([gapIdx, d, face], i) => { const x = ex(gapIdx ? 330 : -330, d) + (i % 2 ? 40 : -40) * d, y = Y(d) + 10 * d, sc = d * 1.4;
      const vx = x - VX, vy = y - H;
      shad += `<path d="M${f1(x - 22 * sc)},${f1(y)}L${f1(x + 22 * sc)},${f1(y)}L${f1(x + 22 * sc + vx * 0.5)},${f1(y + vy * 0.5)}L${f1(x - 22 * sc + vx * 0.5)},${f1(y + vy * 0.5)}Z" fill="#120a14" opacity=".55"/>`;
      ppl += personBack(x, y, sc, face, i, r); });
    put(L.set, `<g id="${id}-deck">${s}${shad}${cars}${ppl}</g>`);
    put(L.glow, `<g id="${id}-hl" opacity="${o.hlOp ?? 0.9}">${glow}</g>`);
    return id;
  };
  // a car seen from the front: headlights on, two heads behind the windscreen, the sky in the glass; (x, y) = where the tyres touch
  function carFront(x, y, s, col, r) {
    const roof = dk(col, 0.84), low = dk(col, 0.58);
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s.toFixed(3)})">
      <rect x="-136" y="-18" width="44" height="22" rx="6" fill="#0c0c10"/><rect x="92" y="-18" width="44" height="22" rx="6" fill="#0c0c10"/>
      <path d="M-150,-24L-154,-96Q-150,-128 -116,-134H116Q150,-128 154,-96L150,-24Q148,-4 124,-4H-124Q-148,-4 -150,-24Z" fill="${col}" ${O(5)}/>
      <path d="M-104,-134L-86,-206Q-80,-222 -58,-224H58Q80,-222 86,-206L104,-134Z" fill="${roof}" ${O(5)}/>
      <path d="M-88,-140L-72,-200H72L88,-140Z" fill="#241a26" ${O(4)}/>
      <circle cx="-40" cy="-178" r="15" fill="#0e0a12"/><path d="M-66,-140Q-66,-162 -40,-162Q-14,-162 -14,-140Z" fill="#0e0a12"/>
      <circle cx="40" cy="-178" r="15" fill="#0e0a12"/><path d="M14,-140Q14,-162 40,-162Q66,-162 66,-140Z" fill="#0e0a12"/>
      <path d="M-70,-148L-40,-196H-10L-46,-148Z" fill="#ffb878" opacity=".35"/>
      <rect x="-146" y="-112" width="58" height="26" rx="9" fill="#fff8e0" ${O(3)}/><rect x="88" y="-112" width="58" height="26" rx="9" fill="#fff8e0" ${O(3)}/>
      <rect x="-56" y="-108" width="112" height="30" rx="6" fill="#1c1e24" ${O(3)}/><rect x="-36" y="-62" width="72" height="24" rx="4" fill="#f4f2ea" ${O(3)}/>
      <rect x="-152" y="-44" width="304" height="22" rx="8" fill="${low}" ${O(3)}/>
      <ellipse cx="-164" cy="-128" rx="16" ry="11" fill="${roof}" ${O(3)}/><ellipse cx="164" cy="-128" rx="16" ry="11" fill="${roof}" ${O(3)}/>
      <path d="M-100,-222Q0,-232 100,-222" stroke="#ffd9a0" stroke-width="8" opacity=".85" fill="none"/>
      <path d="M-148,-100Q-146,-126 -116,-132M148,-100Q146,-126 116,-132" stroke="#ffd9a0" stroke-width="6" opacity=".7" fill="none"/></g>`;
  }
  // someone out on the road, back to us, looking at the blast (face = which way the head turns); a rim of light round the outline
  function personBack(x, y, s, face, i, r) {
    const shield = i % 2 === 0, col = ["#2a2e3a", "#3a2430", "#24302a"][i % 3];
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${(s * face).toFixed(3)},${s.toFixed(3)})">
      <path d="M-12,0L-10,-58H10L12,0Z" fill="#141018"/><path d="M-22,-56Q-24,-110 -12,-118H12Q24,-110 22,-56Z" fill="${col}"/>
      <circle cx="${face > 0 ? 2 : -2}" cy="-134" r="15" fill="#120e14"/>
      ${shield ? `<path d="M14,-112Q34,-128 18,-150" stroke="${col}" stroke-width="11" stroke-linecap="round" fill="none"/>` : `<path d="M18,-110Q26,-84 22,-62" stroke="${col}" stroke-width="11" stroke-linecap="round" fill="none"/>`}
      <path d="M-20,-62Q-26,-84 -18,-110" stroke="${col}" stroke-width="11" stroke-linecap="round" fill="none"/>
      <path d="M-22,-58Q-24,-110 -12,-118H12Q24,-110 22,-58M-15,-136Q-14,-150 0,-150Q14,-150 15,-136" stroke="#ffd49a" stroke-width="3.5" fill="none" opacity=".9"/></g>`;
  }

  // ---------------------------------------------------------------- the detonation
  function nuke(tl, L, t0, dur, o = {}) {
    const id = nid("nbn"), r = mk(o.seed || 37), x = o.x ?? 600, y = o.y ?? 1120, s = o.s ?? 0.8, at = o.at ?? 0, T = t0 - at, end = t0 + dur;
    const jam = o.jam, rise = o.rise ?? 2.6, up0 = -170, up1 = -790, up2 = -850, capBot = 110;
    const P = capParts(r);
    const g = document.createElementNS(NS, "g"); g.setAttribute("transform", `translate(${x},${y}) scale(${s})`);
    L.far.insertBefore(g, L.far.firstChild);
    const debris = Array.from({ length: o.debris ?? 14 }, () => { const a = (0.08 + r() * 0.84) * Math.PI, D = 420 + r() * 700;
      return { a, dx: Math.cos(a) * D, dy: -Math.sin(a) * D * 0.8, R: 3 + r() * 5, len: 1.1 + r() * 0.8 }; });
    const bh = (b, tone, i, ly = 0.4) => `<g id="${id}-${tone}${i}">${billow(b.x, b.y, b.R, r, tone, 0, ly)}</g>`;
    g.innerHTML = `<circle id="${id}-bl" cx="0" cy="-300" r="1300" fill="url(#nkBloom)"/>
      <path id="${id}-dome" d="M-100,0A100,82 0 0 1 100,0Z" fill="url(#nbDome)" stroke="#fff6e4" stroke-width="6" vector-effect="non-scaling-stroke"/>
      <g id="${id}-ring"><ellipse rx="100" ry="13" fill="url(#nbRing)"/><ellipse rx="100" ry="13" fill="none" stroke="#fff4dc" stroke-width="4" vector-effect="non-scaling-stroke"/></g>
      <g id="${id}-ring2"><ellipse rx="100" ry="13" fill="none" stroke="#ffd9a0" stroke-width="3" opacity=".7" vector-effect="non-scaling-stroke"/></g>
      <g id="${id}-sk">${surgeHTML(mk(91), 0.2)}</g>
      <g id="${id}-st" opacity="0">${stemHTML(r)}</g>
      <g id="${id}-up" transform="translate(0,${up0})">
        <ellipse id="${id}-wil" cx="0" cy="${capBot + 40}" rx="420" ry="66" fill="url(#nbWil)" opacity="0"/>
        <g id="${id}-cap" opacity="0">${P.back}${P.top}<g id="${id}-core">${P.core}</g>${P.boil.map((b, i) => bh(b, "hot", i)).join("")}
          <g id="${id}-rl">${rollHTML(P.rollL, r)}</g><g id="${id}-rr">${rollHTML(P.rollR, r)}</g>${P.front}</g>
        <g id="${id}-fb"><path d="${blob(0, 0, 205, r, 12)}" fill="#e8582a"/><circle r="196" fill="url(#nbFire)"/>
          ${Array.from({ length: 8 }, (_, i) => { const a = (i / 8 + r() * 0.09) * Math.PI * 2, d = 128 + r() * 52; return billow(Math.cos(a) * d, Math.sin(a) * d * 0.95, 38 + r() * 36, r, "hot", -Math.cos(a), -Math.sin(a)); }).join("")}
          ${billow(-70, -150, 56, r, "lit", 0.3, 0.8)}${billow(60, -160, 50, r, "lit", -0.3, 0.8)}
          <circle id="${id}-fbw" r="150" fill="#ffffff"/></g>
      </g>
      <g id="${id}-deb">${debris.map((d, i) => `<path id="${id}-d${i}" d="M${-d.R},0L0,${-d.R * 0.7}L${d.R},0L0,${d.R * 0.6}Z" fill="#241418"/>`).join("")}</g>`;
    const OR = (oy) => `0 ${oy}`;
    // the flash: a white sun on the ground, collapsing into the fireball
    tl.fromTo(`#${id}-bl`, { opacity: 1, scale: 1.15, svgOrigin: OR(-300) }, { opacity: 0.16, scale: 0.8, svgOrigin: OR(-300), duration: 1.2, ease: "power2.out" }, T);
    tl.to(`#${id}-bl`, { opacity: 0.1, duration: Math.max(0.2, end - T - 1.2), ease: "none" }, T + 1.2);
    tl.fromTo(`#${id}-fb`, { scale: 0.42, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.32, ease: "expo.out" }, T);
    tl.to(`#${id}-fb`, { scale: 1.22, svgOrigin: "0 0", duration: 0.9, ease: "power1.out" }, T + 0.32);
    tl.fromTo(`#${id}-fbw`, { opacity: 1 }, { opacity: 0, duration: 0.7, ease: "power2.in" }, T);
    tl.to(`#${id}-fb`, { opacity: 0, duration: 0.6, ease: "power1.in" }, T + 0.85);
    // up it goes: the fireball and then the cap ride the same climb; the stem stretches under it, pinned to the ground
    tl.fromTo(`#${id}-up`, { y: up0 }, { y: up1, duration: rise, ease: "power1.out" }, T);
    tl.to(`#${id}-up`, { y: up2, duration: Math.max(0.2, end - T - rise), ease: "none" }, T + rise);
    const k0 = (-up0 - capBot) / 700, k1 = (-up1 - capBot) / 700, k2 = (-up2 - capBot) / 700;
    tl.fromTo(`#${id}-st`, { scaleY: k0, scaleX: 0.7, svgOrigin: "0 0" }, { scaleY: k1, scaleX: 1, svgOrigin: "0 0", duration: rise, ease: "power1.out" }, T);
    tl.to(`#${id}-st`, { scaleY: k2, scaleX: 1.04, svgOrigin: "0 0", duration: Math.max(0.2, end - T - rise), ease: "none" }, T + rise);
    tl.fromTo(`#${id}-st`, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power1.out" }, T + 0.22);
    // the cap takes over from the fireball: it forms, swells and keeps rolling; the fire inside dims to embers
    tl.fromTo(`#${id}-cap`, { opacity: 0, scale: 0.5, svgOrigin: "0 0" }, { opacity: 1, scale: 0.9, svgOrigin: "0 0", duration: 1.3, ease: "power2.out" }, T + 0.45);
    tl.to(`#${id}-cap`, { scale: 0.9 + 0.05 * Math.max(0, end - T - 1.75), svgOrigin: "0 0", duration: Math.max(0.2, end - T - 1.75), ease: "none" }, T + 1.75);
    tl.fromTo(`#${id}-core`, { opacity: 1 }, { opacity: 0.72, duration: Math.max(0.4, end - T - 0.5), ease: "none" }, T + 0.5);
    tl.fromTo(`#${id}-rl`, { rotation: 0, svgOrigin: "-360 10" }, { rotation: -55 * Math.max(1, end - T), svgOrigin: "-360 10", duration: Math.max(1, end - T), ease: "none" }, T);
    tl.fromTo(`#${id}-rr`, { rotation: 0, svgOrigin: "360 10" }, { rotation: 55 * Math.max(1, end - T), svgOrigin: "360 10", duration: Math.max(1, end - T), ease: "none" }, T);
    P.boil.forEach((b, i) => tl.fromTo(`#${id}-hot${i}`, { scale: 0.86, svgOrigin: `${f1(b.x)} ${f1(b.y)}` }, { scale: 1.14, svgOrigin: `${f1(b.x)} ${f1(b.y)}`, duration: 0.3 + (i % 3) * 0.08,
      repeat: Math.max(1, Math.ceil((end - T) / 0.3)), yoyo: true, ease: "sine.inOut" }, T + 0.5 + (i % 4) * 0.07));
    // the condensation ring flashes round the column and is gone
    tl.fromTo(`#${id}-wil`, { opacity: 0, scale: 0.55, svgOrigin: OR(capBot + 40) }, { opacity: 0.9, scale: 1.05, svgOrigin: OR(capBot + 40), duration: 0.45, ease: "power2.out" }, T + 0.55);
    tl.to(`#${id}-wil`, { opacity: 0, scale: 1.45, svgOrigin: OR(capBot + 40), duration: 0.9, ease: "power1.in" }, T + 1.0);
    // the shock dome and the ground ring race out over the city
    tl.fromTo(`#${id}-dome`, { scale: 0.4, opacity: 0.95, svgOrigin: "0 0" }, { scale: 15, opacity: 0, svgOrigin: "0 0", duration: 1.15, ease: "power1.out" }, T + 0.04);
    tl.fromTo(`#${id}-ring`, { scale: 0.4, opacity: 1, svgOrigin: "0 0" }, { scale: 16, opacity: 0, svgOrigin: "0 0", duration: 1.8, ease: "power2.out" }, T + 0.06);
    tl.fromTo(`#${id}-ring2`, { scale: 0.4, opacity: 0.8, svgOrigin: "0 0" }, { scale: 11, opacity: 0, svgOrigin: "0 0", duration: 1.7, ease: "power2.out" }, T + 0.38);
    tl.fromTo(`#${id}-sk`, { scaleX: 0.3, scaleY: 0.5, svgOrigin: "0 0" }, { scaleX: 2.1, scaleY: 1.35, svgOrigin: "0 0", duration: 2.4, ease: "power2.out" }, T + 0.15);
    tl.to(`#${id}-sk`, { scaleX: 2.1 + 0.25 * Math.max(0, end - T - 2.55), svgOrigin: "0 0", duration: Math.max(0.2, end - T - 2.55), ease: "none" }, T + 2.55);
    // debris thrown out of the fire
    debris.forEach((d, i) => { tl.fromTo(`#${id}-d${i}`, { x: Math.cos(d.a) * 150, y: -60 - Math.sin(d.a) * 130, rotation: 0, opacity: 1 }, { x: d.dx, y: d.dy, rotation: 300, duration: d.len, ease: "power2.out" }, T + 0.12);
      tl.to(`#${id}-d${i}`, { opacity: 0, duration: 0.35 }, T + 0.12 + d.len - 0.35); });
    // the base surge pours over the skyline, between the two rows of towers
    if (jam && document.getElementById(`${jam}-F`)) {
      const F = document.getElementById(`${jam}-F`), sg = document.createElementNS(NS, "g");
      sg.innerHTML = `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}-sf">${surgeHTML(mk(93), 1)}${surgeHTML(mk(95), 1)}</g></g>`;
      F.parentNode.insertBefore(sg, F);
      tl.fromTo(`#${id}-sf`, { scaleX: 0.15, scaleY: 0.3, opacity: 0, svgOrigin: "0 0" }, { scaleX: 2.2, scaleY: 1.6, opacity: 1, svgOrigin: "0 0", duration: 2.6, ease: "power2.out" }, T + 0.35);
      tl.to(`#${id}-sf`, { scaleX: 2.2 + 0.3 * Math.max(0, end - T - 2.95), scaleY: 1.6 + 0.12 * Math.max(0, end - T - 2.95), svgOrigin: "0 0", duration: Math.max(0.2, end - T - 2.95), ease: "none" }, T + 2.95);
      // backlit: the set and the city go black in the flash, then settle into a dark rim-lit silhouette
      if (o.sil !== false) {
        const sil = (layer, ref, a, b, len) => { const u = document.createElementNS(NS, "use"); u.setAttribute("href", `#${ref}`); u.setAttribute("filter", "url(#nbBlack)"); u.id = `${id}-u${ref}`;
          const tgt = document.getElementById(ref); tgt.parentNode.insertBefore(u, tgt.nextSibling);
          tl.fromTo(u, { opacity: a }, { opacity: b, duration: len, ease: "power2.out" }, T); };
        sil(L.far, `${jam}-F`, 0.97, 0.5, 1.0); sil(L.far, `${jam}-B`, 0.88, 0.3, 1.0); sil(L.set, `${jam}-deck`, 0.94, 0.42, 0.9);
      }
      const hot = document.getElementById(`${jam}-hot`);
      if (hot) { tl.fromTo(hot, { opacity: 1 }, { opacity: o.heat ?? 0.28, duration: 1.3, ease: "power2.out" }, T); }
    }
    // screen space: the white wash, a bloom that climbs with the fireball, an anamorphic streak and ghosts across the lens
    if (o.sx !== undefined) {
      const sx = o.sx, sy = o.sy, ks = o.ks ?? s, w = document.createElementNS(NS, "g"); L.light.appendChild(w);
      const fy0 = sy + up0 * ks, fy1 = sy + up1 * ks;
      w.innerHTML = `<g id="${id}-wash" style="mix-blend-mode:screen"><rect x="-200" y="-200" width="1480" height="2320" fill="#ffe8c8" opacity=".07"/><circle cx="${sx}" cy="${fy0}" r="720" fill="url(#nbWash)"/></g>
        <g id="${id}-lens" style="mix-blend-mode:screen"><circle cx="${sx}" cy="0" r="520" fill="url(#nkBloom)" opacity=".75"/>
          <rect x="-400" y="-9" width="1880" height="18" fill="url(#nbStreak)"/><rect x="-400" y="-42" width="1880" height="84" fill="url(#nbStreak)" opacity=".28"/></g>
        <g id="${id}-ghost" style="mix-blend-mode:screen">${[[0.55, 46, "#8af0ff", 0.22], [0.95, 92, "#ffd27a", 0.16], [1.35, 30, "#ff8a6a", 0.22], [1.8, 140, "#a8ffc0", 0.1]].map(([k, R, c, op]) => {
          const gx = sx + (540 - sx) * k, gy = fy0 + (960 - fy0) * k; let hx = ""; for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2 + 0.3; hx += `${i ? "L" : "M"}${f1(gx + Math.cos(a) * R)},${f1(gy + Math.sin(a) * R)}`; }
          return `<path d="${hx}Z" fill="${c}" opacity="${op}"/>`; }).join("")}</g>`;
      tl.fromTo(`#${id}-wash`, { opacity: o.wash ?? 0.85 }, { opacity: 0, duration: 0.6, ease: "power2.out" }, T);
      tl.fromTo(`#${id}-lens`, { y: fy0, opacity: 1 }, { y: fy1, duration: rise, ease: "power1.out" }, T);
      tl.to(`#${id}-lens`, { opacity: o.lensRest ?? 0, duration: 1.4, ease: "power2.out" }, T);
      tl.fromTo(`#${id}-ghost`, { opacity: 1 }, { opacity: 0, duration: 0.9, ease: "power2.in" }, T);
    }
    // birds burst off the city
    if (o.birds) { const bg = document.createElementNS(NS, "g"); L.mid.appendChild(bg); const rb = mk(71);
      bg.innerHTML = Array.from({ length: o.birds }, (_, i) => { const w = 9 + rb() * 9;
        return `<g transform="translate(${f1(o.birdX ?? 540)},${f1(o.birdY ?? 1000)})"><g id="${id}-b${i}"><path id="${id}-bw${i}" d="M${-w},${-w * 0.3}Q${-w * 0.4},${-w * 0.6} 0,0Q${w * 0.4},${-w * 0.6} ${w},${-w * 0.3}" stroke="#140e14" stroke-width="${f1(2.5 + w * 0.12)}" fill="none" stroke-linecap="round"/></g></g>`; }).join("");
      for (let i = 0; i < o.birds; i++) { const a = -Math.PI * (0.1 + rb() * 0.8), D = 420 + rb() * 520;
        tl.fromTo(`#${id}-b${i}`, { x: (rb() - 0.5) * 300, y: (rb() - 0.5) * 80, scale: 0.6 }, { x: Math.cos(a) * D * 1.4, y: Math.sin(a) * D * 0.6 - 120, scale: 1.6, duration: 2.2, ease: "power1.out" }, T + 0.1 + rb() * 0.3);
        tl.fromTo(`#${id}-bw${i}`, { scaleY: 1, svgOrigin: "0 0" }, { scaleY: -0.6, svgOrigin: "0 0", duration: 0.09 + rb() * 0.05, repeat: 24, yoyo: true, ease: "sine.inOut" }, T + 0.1); }
    }
    return id;
  }

  // ---------------------------------------------------------------- the first v6 pass (kept for reference)
  function blast(tl, layer, t0, dur, o = {}) {
    const id = nid("nbb"), x = o.x ?? 600, y = o.y ?? 792, s = o.s ?? 0.4, at = o.at ?? 0, r0 = o.riseFrom ?? 1.05, m0 = o.mushFrom ?? 0.82, R = o.ring ?? 1100;
    const g = document.createElementNS(NS, "g");
    if (o.prepend) layer.insertBefore(g, layer.firstChild); else layer.appendChild(g);
    g.innerHTML = `<g id="${id}-sk"><ellipse cx="${x}" cy="${f1(y - 6 * s)}" rx="100" ry="22" fill="url(#nbSkirt)"/></g>
      <g id="${id}-ri"><ellipse cx="${x}" cy="${f1(y - 10 * s)}" rx="100" ry="20" fill="url(#nbRing)"/><ellipse id="${id}-re" cx="${x}" cy="${f1(y - 10 * s)}" rx="100" ry="20" fill="none" stroke="#fff6e0" stroke-width="5"/></g>
      <g id="${id}-ri2"><ellipse cx="${x}" cy="${f1(y - 10 * s)}" rx="100" ry="20" fill="none" stroke="#ffd9a0" stroke-width="3" opacity=".7"/></g>
      <g id="${id}-ris">${oldBlast(x, y, s * 0.92, "rise", 11)}</g>
      <g id="${id}-mu" opacity="0">${oldBlast(x, y, s, "mush", 11)}</g>
      <g id="${id}-fl" style="mix-blend-mode:screen">${oldBlast(x, y - 30 * s, s * 0.9, "flash", 11)}</g>`;
    const T = t0 + at, org = `${x} ${y}`;
    tl.fromTo(`#${id}-fl`, { opacity: 1, scale: 0.9, svgOrigin: org }, { opacity: 0, scale: 1.25, svgOrigin: org, duration: 0.75, ease: "power2.out" }, T);
    tl.fromTo(`#${id}-ris`, { scale: r0, opacity: 1, svgOrigin: org }, { scale: r0 + 0.4, svgOrigin: org, duration: 1.2, ease: "power1.out" }, T);
    tl.to(`#${id}-ris`, { opacity: 0, duration: 0.45, ease: "power1.in" }, T + 0.8);
    tl.fromTo(`#${id}-mu`, { opacity: 0, scale: m0, svgOrigin: org }, { opacity: 1, scale: m0 + 0.1, svgOrigin: org, duration: 0.5, ease: "power1.out" }, T + 0.75);
    tl.to(`#${id}-mu`, { scale: m0 + 0.1 + 0.06 * Math.max(0, dur - at - 1.25), svgOrigin: org, duration: Math.max(0.2, dur - at - 1.25), ease: "none" }, T + 1.25);
    const ring = (sel, d0, len, rx1) => { tl.fromTo(`${sel} ellipse`, { attr: { rx: 40, ry: 9 } }, { attr: { rx: rx1, ry: rx1 * 0.2 }, duration: len, ease: "power2.out" }, T + d0);
      tl.fromTo(sel, { opacity: 1 }, { opacity: 0, duration: len, ease: "power1.in" }, T + d0); };
    ring(`#${id}-ri`, 0.05, Math.min(2.4, dur - at), R); ring(`#${id}-ri2`, 0.35, Math.min(2.2, dur - at - 0.3), R * 0.8);
    tl.fromTo(`#${id}-sk ellipse`, { attr: { rx: 60, ry: 14 } }, { attr: { rx: R * 0.55, ry: R * 0.09 }, duration: Math.min(2.4, dur - at), ease: "power1.out" }, T + 0.15);
    return id;
  }
  function flood(tl, layer, t0, o = {}) {
    const id = nid("nbf"), g = document.createElementNS(NS, "g"); layer.appendChild(g);
    g.innerHTML = `<g id="${id}" style="mix-blend-mode:screen"><rect width="1080" height="1920" fill="#fff4dc"/><circle cx="${o.x ?? 600}" cy="${o.y ?? 520}" r="${o.r ?? 900}" fill="url(#nbWash)"/></g>`;
    tl.fromTo(`#${id}`, { opacity: o.peak ?? 0.5 }, { opacity: 0, duration: o.len ?? 0.7, ease: "power2.out" }, t0);
    return id;
  }

  window.NkB = { nuke, mushHTML, blast, flood };
})();
