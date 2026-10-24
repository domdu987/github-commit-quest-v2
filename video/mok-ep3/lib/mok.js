// Sets, props and cast for "หมอกลง": a mountain road in Loei at 3 a.m. in the cold season, fog thick enough to
// swallow the headlights. Driver's POV through the windscreen, the car seen from outside on a foggy road and from
// the front through the windscreen (three people inside), a tiny village petrol station with a convex mirror, a green
// road sign, a top-down diagram of two cars, the license plate. Same layer contract as sets.js; seeded RNG only.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);

  Sets.DEFS += `
    <linearGradient id="mkSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1018"/><stop offset=".6" stop-color="#1b2430"/><stop offset="1" stop-color="#3a4452"/></linearGradient>
    <linearGradient id="mkDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2742"/><stop offset=".5" stop-color="#4f4a68"/><stop offset=".85" stop-color="#b9806a"/><stop offset="1" stop-color="#e0a27a"/></linearGradient>
    <linearGradient id="mkRoad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f47"/><stop offset="1" stop-color="#1f2329"/></linearGradient>
    <radialGradient id="mkFogGlow"><stop offset="0" stop-color="#f4f2ea" stop-opacity=".95"/><stop offset=".35" stop-color="#d9dbd8" stop-opacity=".55"/><stop offset="1" stop-color="#c3c7cc" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkPuff"><stop offset="0" stop-color="#d3d7dc" stop-opacity=".85"/><stop offset=".6" stop-color="#c9ced6" stop-opacity=".45"/><stop offset="1" stop-color="#c3c7cc" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkLow"><stop offset="0" stop-color="#fff3d2" stop-opacity=".8"/><stop offset=".5" stop-color="#e9e2c8" stop-opacity=".3"/><stop offset="1" stop-color="#e9e2c8" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkHaz"><stop offset="0" stop-color="#ffb04a" stop-opacity=".95"/><stop offset=".4" stop-color="#ff8a2a" stop-opacity=".35"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkTail"><stop offset="0" stop-color="#ff4a3a" stop-opacity=".95"/><stop offset=".4" stop-color="#d8261a" stop-opacity=".35"/><stop offset="1" stop-color="#d8261a" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkTube"><stop offset="0" stop-color="#e8fbff" stop-opacity=".85"/><stop offset=".4" stop-color="#bfe6f2" stop-opacity=".25"/><stop offset="1" stop-color="#bfe6f2" stop-opacity="0"/></radialGradient>
    <linearGradient id="mkBeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6dc" stop-opacity=".75"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></linearGradient>
    <linearGradient id="mkFogBand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9ced6" stop-opacity="0"/><stop offset=".5" stop-color="#c9ced6" stop-opacity=".75"/><stop offset="1" stop-color="#c9ced6" stop-opacity="0"/></linearGradient>
    <linearGradient id="mkDash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2d33"/><stop offset="1" stop-color="#121418"/></linearGradient>
    <linearGradient id="mkBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9ecef"/><stop offset=".6" stop-color="#c3c9cf"/><stop offset="1" stop-color="#9aa2aa"/></linearGradient>
    <linearGradient id="mkGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a3644"/><stop offset=".5" stop-color="#3f4e5e"/><stop offset="1" stop-color="#1e2732"/></linearGradient>
    <linearGradient id="mkWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e4634"/><stop offset="1" stop-color="#3a2a1f"/></linearGradient>
    <linearGradient id="mkRoof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a423c"/><stop offset="1" stop-color="#211c19"/></linearGradient>
    <linearGradient id="mkShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb35a" stop-opacity=".42"/><stop offset="1" stop-color="#ffb35a" stop-opacity="0"/></linearGradient>
    <linearGradient id="mkMoonShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcd6ff" stop-opacity=".28"/><stop offset="1" stop-color="#bcd6ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="mkShaftUp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffb35a" stop-opacity=".38"/><stop offset="1" stop-color="#ffb35a" stop-opacity="0"/></linearGradient>
    <radialGradient id="mkMoon"><stop offset="0" stop-color="#dfe8f2" stop-opacity=".55"/><stop offset=".3" stop-color="#b9c6d6" stop-opacity=".25"/><stop offset="1" stop-color="#9aa8b8" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkFire"><stop offset="0" stop-color="#ff9a4a" stop-opacity=".42"/><stop offset=".45" stop-color="#ff8a3a" stop-opacity=".16"/><stop offset="1" stop-color="#ff8a3a" stop-opacity="0"/></radialGradient>
    <radialGradient id="mkMirror" cx=".45" cy=".4"><stop offset="0" stop-color="#4a5a66"/><stop offset=".8" stop-color="#26313a"/><stop offset="1" stop-color="#0e1418"/></radialGradient>`;

  // drifting fog: wide soft bands (class fogb drifts sideways) over a base tint
  const fogBands = (r, y0, y1, n, op = 0.7, col = "url(#mkFogBand)") => Array.from({ length: n }, (_, k) => {
    const y = y0 + (y1 - y0) * (k / Math.max(1, n - 1)) + (r() - 0.5) * 80, h = 160 + r() * 260;
    return `<g class="fogb" data-d="${f1(30 + r() * 70)}"><rect x="-1100" y="${f1(y)}" width="3300" height="${f1(h)}" fill="${col}" opacity="${(op * (0.6 + r() * 0.4)).toFixed(2)}"/></g>`;
  }).join("");
  const fogBlobs = (r, n, x0, x1, y0, y1, op = 0.5) => Array.from({ length: n }, () => `<g class="fogb" data-d="${f1(20 + r() * 60)}"><ellipse cx="${f1(x0 + r() * (x1 - x0))}" cy="${f1(y0 + r() * (y1 - y0))}" rx="${f1(220 + r() * 300)}" ry="${f1(70 + r() * 90)}" fill="url(#mkPuff)" opacity="${(op * (0.6 + r() * 0.4)).toFixed(2)}"/></g>`).join("");

  // foreground silhouettes for depth: grass clumps along the bottom, an overhanging branch from a corner (fg layer is blurred)
  const fgGrass = (r, y, n = 9, col = "#0b0e10") => Array.from({ length: n }, (_, k) => {
    const x = -300 + k * (1700 / n) + r() * 80;
    return `<g transform="translate(${f1(x)},${f1(y + r() * 40)}) scale(${(0.8 + r() * 0.7).toFixed(2)})">${Array.from({ length: 7 }, (_, b) => `<path d="M${b * 14 - 42},0Q${b * 14 - 40 + (b - 3) * 10},-${f1(120 + r() * 120)} ${b * 14 - 30 + (b - 3) * 26},-${f1(160 + r() * 140)}" stroke="${col}" stroke-width="${f1(10 + r() * 6)}" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
  }).join("");
  const fgBranch = (x, y, flip = 1, col = "#0b0e10") => `<g transform="translate(${x},${y}) scale(${flip},1)"><path d="M-200,-40Q120,10 420,140" stroke="${col}" stroke-width="34" fill="none" stroke-linecap="round"/>
      <path d="M140,40Q220,0 300,10M260,90Q330,80 380,120M60,0Q90,-60 160,-80" stroke="${col}" stroke-width="14" fill="none" stroke-linecap="round"/>
      ${[[300, 10], [160, -80], [380, 120], [420, 140], [220, 40]].map(([lx, ly]) => `<ellipse cx="${lx}" cy="${ly}" rx="46" ry="18" fill="${col}" transform="rotate(${(lx % 50) - 25} ${lx} ${ly})"/>`).join("")}</g>`;

  // the villager in the fog: a pale figure with a blanket round the shoulders; an arm that waves (class wave, pivot at the shoulder)
  function villager(x, y, s, o = {}) {
    const arm = o.wave === false ? `<path d="M-46,-300Q-60,-200 -50,-120" stroke="#1c2228" stroke-width="30" stroke-linecap="round" fill="none"/>`
      : `<g class="wave" data-ox="${x + 50 * s}" data-oy="${y - 300 * s}"><path d="M50,-300Q90,-380 100,-470" stroke="#1c2228" stroke-width="28" stroke-linecap="round" fill="none"/><g transform="translate(100,-480)"><ellipse rx="22" ry="28" fill="#c9d3cf"/>${[-14, -4, 6, 15].map((fx) => `<path d="M${fx},-18v-30" stroke="#c9d3cf" stroke-width="9" stroke-linecap="round"/>`).join("")}</g></g>`;
    return `<g class="vlg" opacity="${o.op ?? 1}"><g transform="translate(${f1(x)},${f1(y)}) scale(${s})">
      <path d="M-70,0L-60,-280Q-62,-330 -20,-344H20Q62,-330 60,-280L70,0Z" fill="#1c2228"/>
      <path d="M-84,-250Q-90,-340 -30,-352H30Q90,-340 84,-250Q60,-280 0,-284Q-60,-280 -84,-250Z" fill="#5a4a3e"/>${arm}
      <ellipse cx="0" cy="-392" rx="40" ry="48" fill="#c9d3cf"/><path d="M-42,-400Q-46,-450 0,-452Q46,-450 42,-400Q30,-430 0,-430Q-30,-430 -42,-400Z" fill="#1c2228"/>
      <ellipse cx="${-14 + (o.look || 0)}" cy="-392" rx="7" ry="9" fill="#0b0f12"/><ellipse cx="${14 + (o.look || 0)}" cy="-392" rx="7" ry="9" fill="#0b0f12"/></g></g>`;
  }

  // a small white hatchback seen from the side, nose to the right. Light groups by id so a shot can switch them:
  // ${id}-head (headlights), ${id}-tail (tail/brake lights), ${id}-haz (hazards, blink with class haz), ${id}-cab (cabin glow)
  function car(id, x, y, s, o = {}) {
    const P = o.plate || "xxx xxxx";
    return `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})">
      <ellipse cx="0" cy="8" rx="330" ry="22" fill="#05080b" opacity=".55"/>
      <path d="M-320,-40Q-330,-120 -290,-140L-200,-150Q-150,-250 -40,-262H120Q190,-258 250,-170L320,-150Q348,-140 344,-80V-40Q344,-10 316,-10H-300Q-322,-12 -320,-40Z" fill="url(#mkBody)" ${OUT}/>
      <path d="M-180,-152Q-140,-236 -40,-244H40V-152Z" fill="url(#mkGlass)" ${OUT}/><path d="M58,-244H118Q176,-240 226,-160L230,-152H58Z" fill="url(#mkGlass)" ${OUT}/>
      <path d="M48,-246V-20M-190,-150V-30" stroke="${INK}" stroke-width="4"/><path d="M-60,-130h40M110,-130h40" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
      ${[-200, 210].map((wx) => `<g><circle cx="${wx}" cy="-20" r="64" fill="#15181c" ${OUT}/><circle cx="${wx}" cy="-20" r="34" fill="#8a929a" ${OUT}/><circle cx="${wx}" cy="-20" r="8" fill="${INK}"/></g>`).join("")}
      <rect x="318" y="-130" width="26" height="30" rx="8" fill="#f4f0d8" ${OUT}/><rect x="-326" y="-128" width="20" height="40" rx="6" fill="#a8261c" ${OUT}/>
      <rect x="-338" y="-86" width="20" height="40" rx="4" fill="#f4f2ea" ${OUT}/><text x="-328" y="-60" font-family="Kanit" font-weight="900" font-size="9" text-anchor="middle" fill="${INK}" transform="rotate(-90 -328 -66)">${P}</text>
      <g id="${id}-cab" opacity="${o.cab ?? 0}"><path d="M-180,-152Q-140,-236 -40,-244H40V-152Z" fill="#ffd38a" opacity=".35"/><path d="M58,-244H118Q176,-240 226,-160L230,-152H58Z" fill="#ffd38a" opacity=".35"/></g></g>`;
  }
  // the matching lights for the glow layer (positions follow car(x, y, s); right-facing only)
  function carLights(id, x, y, s, o = {}) {
    const hx = x + 332 * s, hy = y - 115 * s, tx = x - 318 * s, ty = y - 108 * s;
    const beam = o.high ? `<path d="M${hx},${hy - 10 * s}L${hx + 1400},${hy - 300}L${hx + 1400},${hy + 260}L${hx},${hy + 10 * s}Z" fill="url(#mkLow)" opacity=".9"/><circle cx="${hx + 300}" cy="${hy}" r="${600 * s}" fill="url(#mkFogGlow)"/>`
      : `<path d="M${hx},${hy}L${hx + 900},${hy + 120}L${hx + 900},${hy + 300}L${hx},${hy + 14 * s}Z" fill="url(#mkLow)" opacity=".75"/>`;
    return `<g id="${id}-head" opacity="${o.head === false ? 0 : 1}">${beam}<circle cx="${hx}" cy="${hy}" r="${90 * s}" fill="url(#mkFogGlow)"/></g>
      <g id="${id}-tail" opacity="${o.tail === false ? 0 : 1}"><circle cx="${tx}" cy="${ty}" r="${120 * s}" fill="url(#mkTail)"/></g>
      <g id="${id}-haz" opacity="${o.haz ? 1 : 0}"><g class="haz"><circle cx="${tx}" cy="${ty + 40 * s}" r="${140 * s}" fill="url(#mkHaz)"/><circle cx="${hx}" cy="${hy + 20 * s}" r="${140 * s}" fill="url(#mkHaz)"/></g></g>`;
  }

  // ---------------- sets ----------------
  // driver's POV at 3 a.m.: windscreen full of fog, dashboard and wheel, the light stalk on the right of the column (#id-stalk),
  // a hand (#id-hand) that can reach for it; low beams (#id-low) or a white wall of high-beam glare (#id-high); road lines (#id-lines);
  // a waving villager somewhere in the fog (#id-fig, opacity by o.fig)
  function carPOV(L, o = {}) {
    const id = o.id || "cp", r = mk(o.seed || 83);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#5e646c"/>`);
    let far = `<rect x="-900" y="600" width="2900" height="1400" fill="#4a4f57"/>`;
    const mv = o.moving !== false, flow = (from, to, p, k, n, body) => {   // stopped: the copies sit spread along the road instead
      const A = from.split(",").map(Number), B = to.split(",").map(Number), f = mv ? 0 : ((k + 0.5) / n) ** 2, P = A.map((v, j) => v + (B[j] - v) * f);
      return `<g class="flow" data-from="${from}" data-to="${to}" data-p="${p}" data-o="${(k / n).toFixed(3)}"${mv ? "" : ' data-still="1"'} transform="translate(${f1(P[0])},${f1(P[1])}) scale(${P[2].toFixed(3)})">${body}</g>`;
    };
    let ln = `<path d="M160,1420L470,940M900,1420L610,940" stroke="#e9e4cf" stroke-width="8" opacity=".5"/>`;
    for (let k = 0; k < 6; k++) ln += flow("540,945,0.05", "510,1480,1.6", 1.2, k, 6, `<path d="M-7,-60L7,-60L11,60L-11,60Z" fill="#e9e4cf" opacity=".85"/>`);
    const post = `<rect x="-9" y="-110" width="18" height="110" rx="4" fill="#d9dde2"/><rect x="-9" y="-96" width="18" height="16" fill="#ff9a3a"/>`;
    for (let k = 0; k < 4; k++) ln += flow("470,948,0.05", "-180,1560,1.7", 1.6, k, 4, post) + flow("610,948,0.05", "1260,1560,1.7", 1.6, k + 0.5, 4, post);
    far += `<g id="${id}-lines" opacity="${o.lines ?? 0.8}">${ln}</g>`;
    far += fogBands(r, 420, 1100, 6, 0.75) + fogBlobs(r, 8, -300, 1400, 500, 1100, 0.55);
    put(L.far, far);
    // the villager sits in front of the far fog so it reads; a light veil keeps it ghostly
    put(L.mid, `<g id="${id}-fig" opacity="${o.fig ?? 0}">${villager(o.figX ?? 640, o.figY ?? 1040, o.figS ?? 0.55, { wave: o.wave !== false })}</g>
      <g id="${id}-low" opacity="${o.high ? 0 : 1}"><path d="M120,1460L470,980H610L960,1460Z" fill="url(#mkBeam)" opacity=".5"/><ellipse cx="540" cy="1060" rx="520" ry="200" fill="url(#mkPuff)" opacity=".7"/></g>
      <g id="${id}-high" opacity="${o.high ? 1 : 0}"><rect x="-900" y="300" width="2900" height="1300" fill="#e9ebe6" opacity=".9"/><ellipse cx="540" cy="900" rx="900" ry="600" fill="url(#mkFogGlow)"/></g>
      ${fogBlobs(r, 6, -200, 1300, 700, 1250, 0.35)}`);
    // the cabin: roof liner, A-pillars, mirror, dashboard
    let s = `<path d="M-900,-600H2000V300Q1500,250 1150,250L1000,330Q540,280 80,330L-70,250Q-420,250 -900,300Z" fill="#14171b"/>
      <path d="M-70,250L80,330L-60,1500H-900V300Q-420,250 -70,250Z" fill="#1b1e23"/><path d="M1150,250L1000,330L1140,1500H2000V300Q1500,250 1150,250Z" fill="#1b1e23"/>
      <rect x="420" y="290" width="240" height="64" rx="16" fill="#202328" ${OUT}/><path d="M540,354v24" stroke="#202328" stroke-width="12"/>`;
    s += `<path d="M-900,1440Q540,1350 2000,1440V2600H-900Z" fill="url(#mkDash)"/><path d="M-900,1440Q540,1350 2000,1440" stroke="#3a3e46" stroke-width="10" fill="none"/>`;
    s += `<g id="${id}-hazbtn"><rect x="492" y="1452" width="96" height="66" rx="12" fill="#202328" stroke="#3a3e46" stroke-width="6"/><path d="M514,1500l26,-38l26,38z" fill="none" stroke="#d8443a" stroke-width="7"/></g>`;
    s += `<g><rect x="60" y="1466" width="160" height="60" rx="12" fill="#0b0d10" ${OUT}/><text x="140" y="1509" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="36" fill="#7fd1ff">${o.clock || "03:00"}</text></g>`;
    put(L.set, s);
    // right-hand drive: the wheel sits right of centre, the light stalk sticks out right of the column (#id-stalk), her hand (#id-hand)
    let w = `<g transform="translate(700,1800)"><circle r="330" fill="none" stroke="#0e1013" stroke-width="64"/><circle r="330" fill="none" stroke="#2a2d33" stroke-width="48"/><path d="M-310,40Q0,120 310,40M0,110V330" stroke="#1a1c20" stroke-width="70" fill="none"/><circle r="96" fill="#1a1c20" ${OUT}/><circle r="34" fill="#2a2d33"/></g>`;
    // her hands on the rim: the left always (10 o'clock), the right too (2 o'clock) unless it's off reaching for the stalk / hazard button
    const SLV = "#d9a12c", CUF = "#efc256";
    const grip = (x, y, side) => {   // side -1 = left hand at 10 o'clock, 1 = right at 2: a round fist on the rim, the sleeve to the bottom corner
      const ex = side < 0 ? -60 : 1140, ey = 2300, d = Math.hypot(ex - x, ey - y), ux = (ex - x) / d, uy = (ey - y) / d;
      return `<path d="M${x},${y}L${ex},${ey}" stroke="${INK}" stroke-width="134" stroke-linecap="round"/><path d="M${x},${y}L${ex},${ey}" stroke="${SLV}" stroke-width="124" stroke-linecap="round"/>
        <path d="M${f1(x + ux * 70)},${f1(y + uy * 70)}L${f1(x + ux * 115)},${f1(y + uy * 115)}" stroke="${INK}" stroke-width="134"/><path d="M${f1(x + ux * 74)},${f1(y + uy * 74)}L${f1(x + ux * 111)},${f1(y + uy * 111)}" stroke="${CUF}" stroke-width="124"/>
        <g transform="translate(${x},${y}) rotate(${side < 0 ? -25 : 25})">${Hands.fist({ r: 85 })}</g>`;
    };
    w += `<g id="${id}-gripL">${grip(414, 1635, -1)}</g>`;
    if (o.grip !== "left") w += `<g id="${id}-gripR">${grip(986, 1635, 1)}</g>`;
    w += `<g id="${id}-stalk"><g transform="translate(780,1560)"><g class="stk"><rect x="0" y="-16" width="180" height="32" rx="16" fill="#1d2025" ${OUT}/><rect x="146" y="-24" width="64" height="48" rx="14" fill="#2b2f35" ${OUT}/><circle cx="178" cy="0" r="9" fill="#7fd1ff" opacity=".7"/></g></g></g>`;
    // the reaching hand: index finger out, the tip at the group's origin (shots move it with translate(x,y)); arm comes from the bottom right
    if (o.grip === "left") w += `<g id="${id}-hand" transform="translate(${o.handX ?? 1300},${o.handY ?? 2300})"><g transform="rotate(${o.handRot ?? 55})">${Hands.poke({ r: 78, sleeve: SLV, cuff: CUF, sleeveLen: 1100 })}</g></g>`;
    put(L.act, w);  // same depth as the dashboard so the fingertip lands on the button / stalk at every zoom

    put(L.glow, `<g id="${id}-dashglow"><circle cx="140" cy="1496" r="120" fill="#7fd1ff" opacity=".1"/></g><g id="${id}-hazglow" opacity="${o.haz ? 1 : 0}"><g class="haz"><rect x="-900" y="-600" width="2900" height="3400" fill="#ff9a3a" opacity=".16"/><circle cx="540" cy="1486" r="90" fill="url(#mkHaz)"/></g></g>`);
  }

  // a green road sign in the fog lit by passing headlights: "บ้านหมอก 3 กม." and under it the episode plate
  function roadSign(L, o = {}) {
    const id = o.id || "rs", r = mk(o.seed || 89);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#mkSky)"/>`);
    let far = "";
    for (let k = 0; k < 9; k++) far += `<path d="M${-800 + k * 340},1200L${-660 + k * 340},${700 + r() * 200}L${-520 + k * 340},1200Z" fill="#141a20"/>`;
    put(L.far, far + fogBands(r, 600, 1300, 5, 0.75));
    let s = `<path d="M-900,1420H2000V2600H-900Z" fill="url(#mkRoad)"/><path d="M-900,1440H2000" stroke="#d9d4bc" stroke-width="10" stroke-dasharray="80 90" opacity=".6"/>`;
    s += `<rect x="520" y="560" width="26" height="900" fill="#8a929a" ${OUT}/><rect x="760" y="560" width="26" height="900" fill="#8a929a" ${OUT}/>`;
    s += `<g id="${id}-sign"><rect x="300" y="380" width="700" height="330" rx="26" fill="#1f7a4a" ${OUT}/><rect x="318" y="398" width="664" height="294" rx="18" fill="none" stroke="#f4f2ea" stroke-width="7"/>
      <text x="650" y="520" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="104" fill="#f4f2ea">บ้านหมอก</text>
      <text x="650" y="640" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="76" fill="#f4f2ea">${o.km ?? "3"} กม. ➜</text></g>`;
    if (o.ep) s += `<g id="${id}-ep"><rect x="380" y="740" width="540" height="150" rx="16" fill="#f2c23a" ${OUT}/><text x="650" y="808" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="${INK}">${o.ep}</text><text x="650" y="868" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="54" fill="${INK}">${o.title}</text></g>`;
    put(L.set, s);
    put(L.fg, fogBands(r, 300, 1800, 4, 0.55));
    put(L.glow, `<g id="${id}-sweep"><ellipse cx="650" cy="560" rx="560" ry="420" fill="url(#mkLow)"/></g>`);
  }

  // wide: a mountain road in the hills at night, mist in the valleys, one car's lights climbing (#id-car)
  function mountainRoad(L, o = {}) {
    const id = o.id || "mr", r = mk(o.seed || 97);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#${o.dusk ? "mkDusk" : "mkSky"})"/>` + Array.from({ length: 70 }, () => `<circle cx="${f1(-700 + r() * 2500)}" cy="${f1(-500 + r() * 1100)}" r="${f1(1 + r() * 2)}" fill="#e8ecff" opacity="${(0.2 + r() * 0.6).toFixed(2)}"/>`).join(""));
    let far = "";
    [[700, "#1a2230"], [900, "#141b26"], [1100, "#10161f"]].forEach(([y, c], k) => {
      let d = `M-900,${y + 400}`;
      for (let x = -900; x <= 2000; x += 120) d += `L${x},${f1(y - 160 * Math.abs(Math.sin(x / 360 + k)) - r() * 80)}`;
      far += `<path d="${d}L2000,${y + 600}H-900Z" fill="${c}"/>` + fogBands(r, y - 40, y + 120, 2, 0.6);
    });
    put(L.far, far);
    let s = `<path d="M-900,1300C-300,1200 300,1500 700,1380S1500,1180 2000,1260V2600H-900Z" fill="#0c1118"/>`;
    s += `<path id="${id}-road" d="M-400,2400C-100,2000 600,1900 500,1640S100,1420 420,1300S1100,1180 1500,1120" stroke="#2f343c" stroke-width="64" fill="none" stroke-linecap="round"/><path d="M-400,2400C-100,2000 600,1900 500,1640S100,1420 420,1300S1100,1180 1500,1120" stroke="#d9d4bc" stroke-width="5" stroke-dasharray="26 30" fill="none" opacity=".6"/>`;
    for (let k = 0; k < 18; k++) s += `<path d="M${f1(-800 + r() * 2700)},${f1(1500 + r() * 900)}l${f1(30 + r() * 30)},-${f1(140 + r() * 120)}l${f1(30 + r() * 30)},${f1(140 + r() * 120)}z" fill="#070b10"/>`;
    put(L.set, s + fogBands(r, 1250, 1700, 3, 0.55));
    put(L.glow, `<g id="${id}-car"><circle cx="0" cy="0" r="40" fill="url(#mkFogGlow)"/><circle cx="0" cy="0" r="9" fill="#fff6dc"/></g>`);
  }

  // a village petrol station at night: one pump under a tin roof, fluorescent tubes, a little shop with a counter,
  // the convex mirror on a pole (#id-mirror), the car at the pump, room for ยายแสง and the three
  function gasStation(L, o = {}) {
    const id = o.id || "gs", r = mk(o.seed || 101), G = o.ground ?? 1480;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#mkSky)"/>`);
    let far = "";
    for (let k = 0; k < 8; k++) far += `<path d="M${-800 + k * 360},${G - 200}L${-640 + k * 360},${G - 620 - r() * 160}L${-480 + k * 360},${G - 200}Z" fill="#121820"/>`;
    put(L.far, far + fogBands(r, G - 700, G - 150, 3, 0.45));
    let s = `<rect x="-900" y="${G - 20}" width="2900" height="1200" fill="#2a2e34"/><path d="M-900,${G - 20}H2000" stroke="#4a4f57" stroke-width="6"/>`;
    for (let k = 0; k < 30; k++) s += `<ellipse cx="${f1(-700 + r() * 2500)}" cy="${f1(G + 40 + r() * 800)}" rx="${f1(20 + r() * 60)}" ry="${f1(6 + r() * 12)}" fill="#1c1f24" opacity=".7"/>`;
    // shop
    s += `<rect x="-760" y="${G - 620}" width="560" height="600" fill="#5a5048" ${OUT}/><rect x="-720" y="${G - 520}" width="320" height="260" fill="#e9e2b8" opacity=".85" ${OUT}/><rect x="-720" y="${G - 360}" width="320" height="100" fill="#8a6a46" ${OUT}/>
      <path d="M-800,${G - 620}L-480,${G - 760}L-160,${G - 620}Z" fill="#6b7178" ${OUT}/><rect x="-700" y="${G - 600}" width="280" height="60" rx="8" fill="#c8392b" ${OUT}/><text x="-560" y="${G - 556}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="#fff">ปั๊มยายแสง</text>`;
    // canopy + pump
    s += `<rect x="-120" y="${G - 900}" width="760" height="60" fill="#d9dde2" ${OUT}/><rect x="-80" y="${G - 840}" width="24" height="820" fill="#8a929a" ${OUT}/><rect x="560" y="${G - 840}" width="24" height="820" fill="#8a929a" ${OUT}/>
      <g transform="translate(120,${G})"><rect x="0" y="-360" width="150" height="360" rx="14" fill="#c8392b" ${OUT}/><rect x="20" y="-330" width="110" height="80" rx="8" fill="#0b0d10"/><text x="75" y="-276" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="#7fd1ff">500</text>
        <path d="M150,-240q60,0 60,80v120" stroke="${INK}" stroke-width="12" fill="none"/></g>`;
    // the convex mirror on its pole
    s += `<g id="${id}-mirror"><rect x="1040" y="${G - 900}" width="20" height="900" fill="#d8443a" ${OUT}/><circle cx="1050" cy="${G - 980}" r="130" fill="url(#mkMirror)" stroke="#d8443a" stroke-width="22"/><path d="M970,${G - 1040}q40,-40 100,-30" stroke="#c9d6dc" stroke-width="8" fill="none" opacity=".45"/></g>`;
    if (o.car !== false) s += car(`${id}-car`, o.carX ?? 560, G + 40, o.carS ?? 0.85, { plate: o.plate, cab: 0.6 });
    put(L.set, s);
    put(L.glow, `${[60, 360].map((x) => `<rect class="tube" x="${x}" y="${G - 840}" width="200" height="18" rx="9" fill="#e8fbff"/><circle cx="${x + 100}" cy="${G - 830}" r="420" fill="url(#mkTube)"/>`).join("")}
      <circle cx="-560" cy="${G - 400}" r="300" fill="#ffe7a0" opacity=".14"/>`);
    put(L.fg, fogBands(r, G - 400, G + 300, 2, 0.35));
  }

  // close-up of the convex mirror: the car fish-eyed in it, and behind the car a figure wrapped in a blanket (#id-who)
  function mirrorClose(L, o = {}) {
    const id = o.id || "mc", r = mk(o.seed || 103);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#11161c"/>` + fogBands(r, -200, 2400, 7, 0.4));
    let s = `<defs><clipPath id="${id}-clip"><circle cx="540" cy="900" r="430"/></clipPath></defs>
      <circle cx="540" cy="900" r="430" fill="url(#mkMirror)"/>
      <g clip-path="url(#${id}-clip)">
        <path d="M100,1200Q540,1060 980,1200V1400H100Z" fill="#2a2e34"/>
        <g transform="translate(540,1130) scale(0.9,0.8)"><path d="M-320,-40Q-330,-120 -290,-140L-200,-150Q-150,-250 -40,-262H120Q190,-258 250,-170L320,-150Q348,-140 344,-80V-40Q344,-10 316,-10H-300Q-322,-12 -320,-40Z" fill="#c3c9cf" ${OUT}/><path d="M-180,-152Q-140,-236 -40,-244H40V-152Z" fill="#3a4654"/><path d="M58,-244H118Q176,-240 226,-160L230,-152H58Z" fill="#3a4654"/></g>
        <g id="${id}-who" opacity="${o.who ?? 1}">${villager(250, 1120, 0.85, { wave: false })}</g>
        ${fogBands(r, 600, 1300, 3, 0.35)}
        <rect x="100" y="460" width="900" height="880" fill="#c9e0ea" opacity=".07"/>
      </g>
      <circle cx="540" cy="900" r="430" fill="none" stroke="#d8443a" stroke-width="56"/><circle cx="540" cy="900" r="458" fill="none" stroke="${INK}" stroke-width="6"/>
      <path d="M260,700q80,-120 230,-130" stroke="#e9f4f8" stroke-width="16" fill="none" opacity=".35" stroke-linecap="round"/>
      <rect x="520" y="1380" width="40" height="1200" fill="#d8443a" ${OUT}/>`;
    put(L.set, s);
  }

  // the car on a foggy mountain road, side view: shoulder on the near side, rails, the car (#id-car) and its lights in the glow layer
  function roadFog(L, o = {}) {
    const id = o.id || "rfg", r = mk(o.seed || 107), G = o.ground ?? 1400;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#3e444c"/>`);
    put(L.far, `<rect x="-900" y="${G - 500}" width="2900" height="600" fill="#30353c"/>` + fogBands(r, G - 700, G, 5, 0.85));
    const sc = o.scroll ? ` class="scroll" data-v="${o.scroll}"` : "";
    let s = `<rect x="-900" y="${G - 40}" width="2900" height="260" fill="url(#mkRoad)"/><g${sc} data-w="190"><path d="M-900,${G + 60}H2400" stroke="#e9e4cf" stroke-width="10" stroke-dasharray="90 100" opacity=".55"/></g>
      <rect x="-900" y="${G + 220}" width="2900" height="1200" fill="#3a3a30"/><g${sc} data-w="240">`;
    for (let x = -880; x < 2400; x += 240) s += `<rect x="${x}" y="${G + 120}" width="16" height="110" fill="#c9cdd2" ${OUT}/>`;
    s += `</g>`;
    s += `<path d="M-900,${G + 150}H2000" stroke="#c9cdd2" stroke-width="22"/>`;
    if (o.villager) s += `<g id="${id}-v">${villager(o.villager.x, G + 30, o.villager.s || 0.9, { wave: o.villager.wave !== false })}</g>`;
    if (o.car !== false) s += car(`${id}-car`, o.carX ?? 540, o.carY ?? G + 40, o.carS ?? 1, { plate: o.plate });
    if (o.car2) s += car(`${id}-car2`, o.car2.x, o.car2.y ?? G + 40, o.car2.s ?? 1, { plate: o.plate });
    put(L.set, s);
    let g = o.car !== false ? carLights(`${id}-car`, o.carX ?? 540, o.carY ?? G + 40, o.carS ?? 1, o) : "";
    if (o.car2) g += carLights(`${id}-car2`, o.car2.x, o.car2.y ?? G + 40, o.car2.s ?? 1, o.car2);
    put(L.glow, g);
    put(L.fg, fogBands(r, G - 600, G + 400, 4, 0.75) + (o.weeds === false ? "" : `<g${sc} data-w="1700">${fgGrass(r, 1960, 8)}</g>`));
  }

  // a steering wheel seen from the front of the car (the rim as an ellipse in front of the driver's chest), its column into the dash,
  // and a round hand over the rim at each grip point (the rig's own hand circle at actor scale 1.15) so she reads as holding it
  function wheelGrip(w, grips, skin) {
    let g = `<path d="M${w.x - 16},${w.y}L${w.x - 26},${w.y + 200}H${w.x + 26}L${w.x + 16},${w.y}Z" fill="#16181c" ${OUT}/>
      <ellipse cx="${w.x}" cy="${w.y}" rx="${w.rx}" ry="${w.ry}" fill="none" stroke="#0e1013" stroke-width="30"/><ellipse cx="${w.x}" cy="${w.y}" rx="${w.rx}" ry="${w.ry}" fill="none" stroke="#2f3238" stroke-width="18"/>
      <path d="M${w.x - w.rx},${w.y}Q${w.x},${w.y + 26} ${w.x + w.rx},${w.y}M${w.x},${w.y + 14}V${w.y + w.ry}" stroke="#1a1c20" stroke-width="16" fill="none"/><ellipse cx="${w.x}" cy="${w.y + 6}" rx="26" ry="20" fill="#1a1c20" ${OUT}/>`;
    grips.forEach(([x, y]) => {
      g += `<circle cx="${x}" cy="${y}" r="17.5" fill="${skin}" ${OUT}/>`;
    });
    return g;
  }

  // through the windscreen from the bonnet: three people inside (rigs go in the act layer at the seat positions),
  // the dashboard edge drawn on top (#id-dash, moved over the actors with TOP), fog behind them through the rear window
  function carInterior(L, o = {}) {
    const id = o.id || "ci", r = mk(o.seed || 109);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#5e646c"/>` + fogBands(r, 200, 1200, 4, 0.6));
    let s = `<path d="M-900,-600H2000V2600H-900Z" fill="#14171b"/><path d="M60,240Q540,170 1020,240L1080,1000H0Z" fill="#9aa2aa" opacity=".55"/>
      <path d="M200,330Q540,290 880,330L900,640H180Z" fill="#6c747d"/>` + fogBands(r, 300, 650, 2, 0.5);
    s += `<rect x="70" y="620" width="380" height="640" rx="70" fill="#2a2e34" ${OUT}/><rect x="630" y="620" width="380" height="640" rx="70" fill="#2a2e34" ${OUT}/>
      <rect x="150" y="560" width="220" height="110" rx="40" fill="#30353c" ${OUT}/><rect x="710" y="560" width="220" height="110" rx="40" fill="#30353c" ${OUT}/>`;
    put(L.set, s);
    put(L.act, `<g id="${id}-dash"><path d="M-900,1230Q540,1150 2000,1230V2600H-900Z" fill="url(#mkDash)"/><path d="M-900,1230Q540,1150 2000,1230" stroke="#3a3e46" stroke-width="10" fill="none"/>
      ${wheelGrip(o.wheel || { x: 270, y: 1158, rx: 100, ry: 86 }, o.grips || [[340, 1097], [200, 1097]], o.skin || "#ecbf98")}
      <path d="M-900,-600H2000V150Q540,90 -900,150Z" fill="#0e1013"/><path d="M-60,-600L60,1230M1140,-600L1020,1230" stroke="#0e1013" stroke-width="120"/>
      <rect x="-900" y="-600" width="2900" height="3200" fill="#9fb3c4" opacity=".08"/></g>`);
    put(L.glow, `<g id="${id}-hazglow" opacity="${o.haz ? 1 : 0}"><g class="haz"><rect x="-900" y="-600" width="2900" height="3400" fill="#ff9a3a" opacity=".2"/></g></g>`);
  }

  // side window from the back seat: the glass, the fog, a pale villager bending to the window (#id-face), a knuckle knocking (#id-knock);
  // the window glass can slide down (#id-glass)
  function carWindow(L, o = {}) {
    const id = o.id || "cw", r = mk(o.seed || 113);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#4b5159"/>` + fogBands(r, -200, 2400, 8, 0.7));
    put(L.far, `<g id="${id}-face" opacity="${o.face ?? 1}">${villager(560, 1700, 1.9, { wave: false })}</g><g id="${id}-knock" opacity="${o.knock ?? 0}"><g transform="translate(760,880)"><ellipse rx="56" ry="64" fill="#c9d3cf" ${OUT}/>${[-30, -10, 10, 30].map((fx) => `<ellipse cx="${fx}" cy="-46" rx="13" ry="16" fill="#b8c4bf" ${OUT}/>`).join("")}</g></g>`);
    put(L.mid, `<g id="${id}-glass"><rect x="80" y="380" width="920" height="900" rx="40" fill="#9fb3c4" opacity=".22"/><path d="M160,460L420,420M180,560L300,540" stroke="#e9f4f8" stroke-width="10" opacity=".25" stroke-linecap="round"/>
      ${Array.from({ length: 30 }, () => `<circle cx="${f1(120 + r() * 860)}" cy="${f1(420 + r() * 820)}" r="${f1(3 + r() * 6)}" fill="#e9f4f8" opacity=".3"/>`).join("")}</g>`);
    put(L.set, `<path d="M-900,-600H2000V2600H-900ZM80,420Q80,380 120,380H960Q1000,380 1000,420V1280H80Z" fill="#1b1e23" fill-rule="evenodd"/>
      <rect x="-900" y="1280" width="2900" height="1400" fill="#24272c"/><rect x="100" y="1330" width="880" height="80" rx="20" fill="#30353c" ${OUT}/><rect x="760" y="1350" width="120" height="40" rx="10" fill="#14171b" ${OUT}/>`);
  }

  // looking back through the rear window from the back seat: headlights of a car in the fog coming up behind (#id-lights, scale them up)
  function rearWindow(L, o = {}) {
    const id = o.id || "rw", r = mk(o.seed || 127);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#3c4148"/>` + fogBands(r, -200, 2400, 7, 0.75));
    put(L.far, `<g id="${id}-lights" opacity="${o.lights ?? 1}"><g transform="translate(540,1000)"><circle cx="-130" cy="0" r="40" fill="#fff6dc"/><circle cx="130" cy="0" r="40" fill="#fff6dc"/><circle cx="-130" cy="0" r="260" fill="url(#mkFogGlow)"/><circle cx="130" cy="0" r="260" fill="url(#mkFogGlow)"/>
      <rect x="-70" y="60" width="140" height="44" rx="6" fill="#f4f2ea" opacity="${o.plateOn ? 0.9 : 0}"/></g></g>`);
    put(L.set, `<path d="M-900,-600H2000V2600H-900ZM140,520Q540,440 940,520L1000,1260H80Z" fill="#1b1e23" fill-rule="evenodd"/>
      <path d="M140,600H940M150,700H930M160,800H920" stroke="#5a2a20" stroke-width="5" opacity=".7"/><rect x="-900" y="1260" width="2900" height="1400" fill="#24272c"/>
      <rect x="120" y="1290" width="360" height="300" rx="50" fill="#2a2e34" ${OUT}/><rect x="600" y="1290" width="360" height="300" rx="50" fill="#2a2e34" ${OUT}/>`);
    // the back-seat cushion in front of whoever sits there (moved over the actors with TOP)
    put(L.act, `<g id="${id}-seat"><path d="M-900,1640Q540,1600 2000,1640V2600H-900Z" fill="#2a2e34" ${OUT}/><path d="M-900,1700Q540,1662 2000,1700" stroke="#34383e" stroke-width="10" fill="none"/></g>`);
    put(L.glow, `<g id="${id}-hazglow" opacity="${o.haz ? 1 : 0}"><g class="haz"><rect x="-900" y="-600" width="2900" height="3400" fill="#ff9a3a" opacity=".2"/></g></g>`);
  }

  // a Thai license plate close-up, white with black letters and the province, on a bumper in fog (#id-plate)
  function plateClose(L, o = {}) {
    const id = o.id || "pc", r = mk(o.seed || 131), P = o.plate || "xxx xxxx";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#30353c"/>`);
    put(L.set, `<rect x="-900" y="600" width="2900" height="900" fill="${o.body || "#c3c9cf"}" ${OUT}/><rect x="-900" y="1500" width="2900" height="300" fill="#15181c"/>
      <g id="${id}-plate"><rect x="160" y="760" width="760" height="380" rx="26" fill="#f4f2ea" ${OUT}/><rect x="180" y="780" width="720" height="340" rx="18" fill="none" stroke="${INK}" stroke-width="6"/>
      <text x="540" y="960" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="170" fill="#1b1e23" textLength="620" lengthAdjust="spacingAndGlyphs">${P}</text><text x="540" y="1078" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="76" fill="#1b1e23">เลย</text></g>
      <rect x="-200" y="640" width="300" height="100" rx="20" fill="#a8261c" ${OUT}/><rect x="980" y="640" width="300" height="100" rx="20" fill="#a8261c" ${OUT}/>`);
    put(L.glow, `<g id="${id}-glow" opacity="${o.lit ?? 1}"><circle cx="-50" cy="690" r="260" fill="url(#mkTail)"/><circle cx="1130" cy="690" r="260" fill="url(#mkTail)"/></g>`);
    put(L.fg, fogBands(r, 200, 1800, 4, 0.45));
  }

  // top-down diagram: two lanes in fog, our car stopped on the shoulder (#id-a) with brake lights (#id-brake) or only hazards,
  // the car behind (#id-b) driving up following the red lights
  function topRoad(L, o = {}) {
    const id = o.id || "tr", r = mk(o.seed || 137);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#3a3a30"/>`);
    let s = `<rect x="200" y="-600" width="680" height="3400" fill="#2f343c"/><path d="M540,-600V2800" stroke="#e9e4cf" stroke-width="12" stroke-dasharray="80 90" opacity=".7"/><path d="M210,-600V2800M870,-600V2800" stroke="#e9e4cf" stroke-width="8" opacity=".6"/>`;
    const topCar = (cid, x, y, col) => `<g id="${cid}"><g transform="translate(${x},${y})"><rect x="-80" y="-150" width="160" height="300" rx="50" fill="${col}" ${OUT}/><rect x="-62" y="-90" width="124" height="70" rx="16" fill="#3f4e5e"/><rect x="-62" y="60" width="124" height="50" rx="14" fill="#3f4e5e"/></g></g>`;
    s += topCar(`${id}-a`, 120, 700, "#e9ecef") + topCar(`${id}-b`, 380, 1900, "#8a929a");
    put(L.set, s + fogBands(r, -200, 2400, 6, 0.55));
    put(L.glow, `<g id="${id}-brake" opacity="${o.brake ? 1 : 0}"><circle cx="70" cy="845" r="90" fill="url(#mkTail)"/><circle cx="170" cy="845" r="90" fill="url(#mkTail)"/></g>
      <g id="${id}-haz" opacity="${o.haz ? 1 : 0}"><g class="haz"><circle cx="50" cy="560" r="80" fill="url(#mkHaz)"/><circle cx="190" cy="560" r="80" fill="url(#mkHaz)"/><circle cx="50" cy="845" r="80" fill="url(#mkHaz)"/><circle cx="190" cy="845" r="80" fill="url(#mkHaz)"/></g></g>
      <g id="${id}-bhead"><path d="M320,1750L280,1300H480L440,1750Z" fill="url(#mkBeam)" transform="rotate(180 380 1750)" opacity=".0"/><circle cx="330" cy="1755" r="70" fill="url(#mkFogGlow)"/><circle cx="430" cy="1755" r="70" fill="url(#mkFogGlow)"/></g>`);
  }

  // looping motion: fog drifts, hazards blink, the villager waves, tubes flicker
  function life(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".fogb").forEach((el, i) => tl.fromTo(el, { x: 0 }, { x: (i % 2 ? -1 : 1) * (+(el.dataset.d) || 40) * dur, duration: dur, ease: "none", immediateRender: false }, t0));
    q(".haz").forEach((el) => { for (let k = 0; k < dur; k += 0.8) { tl.set(el, { opacity: 1 }, t0 + k); tl.set(el, { opacity: 0.08 }, t0 + k + 0.4); } });
    // rotate about the shoulder in the figure's own units (svgOrigin would use the root SVG's space and miss inside the camera layers)
    q(".wave").forEach((el, i) => tl.fromTo(el, { attr: { transform: "rotate(-14 50 -300)" } }, { attr: { transform: "rotate(18 50 -300)" }, duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.1));
    q(".flow").forEach((el) => {
      if (el.dataset.still) return;
      const [x0, y0, s0] = el.dataset.from.split(",").map(Number), [x1, y1, s1] = el.dataset.to.split(",").map(Number), p = +el.dataset.p;
      tl.fromTo(el, { attr: { transform: `translate(${x0},${y0}) scale(${s0})` } }, { attr: { transform: `translate(${x1},${y1}) scale(${s1})` }, duration: p, ease: "power2.in", repeat: Math.ceil(dur / p) + 1, immediateRender: false }, t0 + (+el.dataset.o) * p);
    });
    q(".scroll").forEach((el) => { const w = +el.dataset.w, v = +el.dataset.v; tl.fromTo(el, { x: 0 }, { x: -w, duration: w / v, ease: "none", repeat: Math.ceil(dur * v / w) + 1, immediateRender: false }, t0); });
    q(".glint").forEach((el, i) => tl.fromTo(el, { opacity: 0.35 }, { opacity: 0.95, duration: 0.6, repeat: Math.ceil(dur / 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.2));
    q(".flick").forEach((el, i) => { for (let k = 0.15 * i; k < dur; k += 0.23) tl.set(el, { opacity: 0.78 + 0.22 * Math.abs(Math.sin(k * 7.3 + i)) }, t0 + k); });
    q(".tube").forEach((el, i) => { for (let k = 0.7 + i * 0.9; k < dur; k += 2.3) { tl.set(el, { opacity: 0.2 }, t0 + k); tl.set(el, { opacity: 1 }, t0 + k + 0.06); tl.set(el, { opacity: 0.4 }, t0 + k + 0.11); tl.set(el, { opacity: 1 }, t0 + k + 0.16); } });
  }


  // ================= EP.2 (อย่าหลับใน): the abandoned village, the house with the charcoal stove =================
  const PALE = "#c9d3cf", BLK = "#5a4a3e";
  // one of the village dead sitting on the floor: blanket mound, pale face, dark eyes (same head as the standing villager)
  const ghostSit = (x, y, s, op = 1) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})" opacity="${op}">
      <path d="M-96,0Q-104,-150 -52,-204Q0,-232 52,-204Q104,-150 96,0Z" fill="${BLK}"/><path d="M-60,-40Q0,-20 60,-40" stroke="#463a30" stroke-width="8" fill="none"/>
      <ellipse cx="0" cy="-252" rx="40" ry="48" fill="${PALE}"/><path d="M-42,-260Q-46,-310 0,-312Q46,-310 42,-260Q30,-290 0,-290Q-30,-290 -42,-260Z" fill="#1c2228"/>
      <ellipse cx="-14" cy="-252" rx="7" ry="9" fill="#0b0f12"/><ellipse cx="14" cy="-252" rx="7" ry="9" fill="#0b0f12"/></g>`;
  // someone sitting slumped, wrapped head to foot in the villagers' brown blanket (face hidden in the hood)
  const wrapped = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path d="M-110,0Q-122,-170 -64,-236Q0,-276 64,-236Q122,-170 110,0Z" fill="${BLK}" ${OUT}/>
      <path d="M-64,-236Q0,-300 64,-236Q54,-196 0,-190Q-54,-196 -64,-236Z" fill="#4e4036" ${OUT}/><ellipse cx="0" cy="-222" rx="36" ry="24" fill="#0b0d10"/><path d="M-80,-60Q0,-30 80,-60" stroke="#463a30" stroke-width="8" fill="none"/></g>`;
  // the clay charcoal stove (อั้งโล่): a tapered bucket with a metal band, an arched air vent at the front, coals on the grate (#id-coals glow)
  const stove = (id, x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})">
      <ellipse cx="0" cy="6" rx="110" ry="18" fill="#000" opacity=".4"/>
      <path d="M-84,-170L-62,0H62L84,-170Z" fill="#b0563a" ${OUT}/><path d="M-84,-170H84" stroke="${INK}" stroke-width="5"/>
      <path d="M-80,-140L80,-140L78,-122H-78Z" fill="#6b7178" ${OUT}/><path d="M-26,0V-52Q0,-78 26,-52V0Z" fill="#2a1a12" ${OUT}/>
      <path d="M-90,-176H90V-164H-90Z" fill="#7a3a26" ${OUT}/>
      <g id="${id}-coals">${[-50, -20, 12, 44, -34, 0, 30].map((cx, k) => `<ellipse cx="${cx}" cy="${k < 4 ? -184 : -198}" rx="22" ry="13" fill="#1b1714" ${OUT}/>`).join("")}</g></g>`;
  const basket = (x, y) => `<g transform="translate(${x},${y})"><path d="M-80,-110L-64,0H64L80,-110Z" fill="#8a6a40" ${OUT}/>
      ${[-80, -50, -20].map((yy) => `<path d="M-78,${yy}H78" stroke="#6b5030" stroke-width="5"/>`).join("")}
      ${[-56, -24, 8, 40, -40, -8, 26].map((cx, k) => `<ellipse cx="${cx}" cy="${k < 4 ? -116 : -136}" rx="22" ry="15" fill="#151210" ${OUT}/>`).join("")}</g>`;
  const blankets = (x, y) => `<g transform="translate(${x},${y})">${[["#7a4a3a", 0], ["#4a5a6a", -44], ["#8a7a4a", -88]].map(([c, yy]) => `<rect x="-110" y="${yy - 44}" width="220" height="48" rx="16" fill="${c}" ${OUT}/>`).join("")}</g>`;

  // inside a house in บ้านหมอก: plank walls, a window with shutters (#id-open / #id-shut), the door (#id-dooropen),
  // a calendar from 2529, the stove in the middle (#id-fire glow, class flick), charcoal and blankets, the dead seated round
  // the stove (#id-ghosts), the gas (#id-gas, a diagram haze that fills from the ceiling) and steam (#id-steam)
  function houseRoom(L, o = {}) {
    const id = o.id || "hr", r = mk(o.seed || 139), G = o.ground ?? 1540, SX = o.stoveX ?? 540;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#0d0f12"/>`);
    let w = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="#3a2c22"/>`;
    for (let x = -880; x < 2000; x += 74) w += `<path d="M${x},-600V${G}" stroke="#271d16" stroke-width="5"/><path d="M${x + 30},${f1(200 + r() * 900)}v${f1(40 + r() * 120)}" stroke="#2f241b" stroke-width="3" opacity=".7"/>`;
    w += `<rect x="-900" y="300" width="2900" height="40" fill="#2a1f17" ${OUT}/><rect x="-900" y="${G - 30}" width="2900" height="34" fill="#2a1f17"/>`;
    // window (right): fog outside; open leaves at the sides, or closed leaves over the opening
    const WX = o.winX ?? 720, WY = 560, WW = 260, WH = 400;
    w += `<rect x="${WX}" y="${WY}" width="${WW}" height="${WH}" fill="#6c747d"/>` + `<g clip-path="url(#${id}-wclip)">${fogBands(r, WY, WY + WH, 3, 0.8)}</g>
      <defs><clipPath id="${id}-wclip"><rect x="${WX}" y="${WY}" width="${WW}" height="${WH}"/></clipPath></defs>
      <rect x="${WX - 14}" y="${WY - 14}" width="${WW + 28}" height="${WH + 28}" fill="none" stroke="#2a1f17" stroke-width="22"/>
      <g id="${id}-open" opacity="${o.shut ? 0 : 1}"><path d="M${WX - 14},${WY}L${WX - 90},${WY - 30}V${WY + WH + 30}L${WX - 14},${WY + WH}Z" fill="#4a3828" ${OUT}/><path d="M${WX + WW + 14},${WY}L${WX + WW + 90},${WY - 30}V${WY + WH + 30}L${WX + WW + 14},${WY + WH}Z" fill="#4a3828" ${OUT}/></g>
      <g id="${id}-shut" opacity="${o.shut ? 1 : 0}"><rect x="${WX}" y="${WY}" width="${WW / 2}" height="${WH}" fill="#4a3828" ${OUT}/><rect x="${WX + WW / 2}" y="${WY}" width="${WW / 2}" height="${WH}" fill="#4a3828" ${OUT}/>
        ${[0.25, 0.5, 0.75].map((k) => `<path d="M${WX + 10},${WY + WH * k}H${WX + WW - 10}" stroke="#33261b" stroke-width="5"/>`).join("")}<rect x="${WX + WW / 2 - 40}" y="${WY + WH / 2 - 8}" width="80" height="16" rx="4" fill="#2a1f17"/></g>`;
    // door (left)
    const DX = o.doorX ?? 60;
    w += `<rect x="${DX}" y="${G - 760}" width="250" height="760" fill="#2a1f17"/><g id="${id}-dooropen" opacity="${o.door ? 1 : 0}"><rect x="${DX + 14}" y="${G - 746}" width="222" height="746" fill="#6c747d"/>${fogBands(r, G - 700, G - 100, 2, 0.6).replace(/x="-1100"/g, `x="${DX + 14}"`).replace(/width="3300"/g, 'width="222"')}</g>
      <g id="${id}-doorshut" opacity="${o.door ? 0 : 1}"><rect x="${DX + 14}" y="${G - 746}" width="222" height="746" fill="#4a3828" ${OUT}/>${[0.3, 0.6].map((k) => `<path d="M${DX + 24},${f1(G - 746 + 746 * k)}H${DX + 226}" stroke="#33261b" stroke-width="5"/>`).join("")}<circle cx="${DX + 200}" cy="${G - 380}" r="10" fill="#1b1714"/></g>`;
    // calendar from forty years ago
    w += `<g transform="translate(${o.calX ?? 470},470) rotate(3)"><rect x="-70" y="0" width="140" height="170" fill="#e9e0c8" ${OUT}/><rect x="-70" y="0" width="140" height="44" fill="#a8261c" ${OUT}/>
      <text x="0" y="32" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="26" fill="#fff">ธ.ค. 2529</text>
      ${Array.from({ length: 16 }, (_, k) => `<rect x="${-56 + (k % 4) * 30}" y="${58 + Math.floor(k / 4) * 26}" width="20" height="16" fill="#b9ae94"/>`).join("")}<circle cx="0" cy="-12" r="6" fill="${INK}"/></g>`;
    put(L.far, w);
    // the dead seated round the stove (behind the living)
    let gh = "";
    (o.ghostPos || [[SX - 330, G + 30, 0.8], [SX + 330, G + 30, 0.8], [SX - 190, G - 10, 0.66], [SX + 190, G - 10, 0.66], [SX - 470, G + 60, 0.9], [SX + 470, G + 60, 0.9], [SX, G - 40, 0.58]])
      .forEach(([x, y, sc]) => (gh += ghostSit(x, y, sc)));
    let st = `<rect x="-900" y="${G}" width="2900" height="1300" fill="#4a3628"/>`;
    for (let y = G + 50; y < 2600; y += 70) st += `<path d="M-900,${y}H2000" stroke="#3a2a1f" stroke-width="5"/>`;
    st += `<g id="${id}-ghosts" opacity="${o.ghosts ?? 0}">${gh}</g>`;
    st += blankets(o.blankX ?? 210, G + 70) + basket(SX + 200, G + 60) + `<g id="${id}-stove">${stove(id, SX, G + 70)}</g>`;
    put(L.set, st);
    put(L.glow, `<g id="${id}-moon" opacity="${o.shut ? 0.55 : 1}">${o.shut ? [0.25, 0.5, 0.75].map((k) => `<path d="M${WX + 10},${WY + WH * k - 3}H${WX + WW - 10}L${WX + WW - 260},${G + 90}H${WX - 380}Z" fill="url(#mkMoonShaft)" opacity=".5"/>`).join("")
        : `<path d="M${WX},${WY}H${WX + WW}L${WX + WW - 240},${G + 90}H${WX - 400}Z" fill="url(#mkMoonShaft)"/>`}</g>`);
    put(L.glow, `<g id="${id}-fire" opacity="${o.fire ?? 0}"><g class="flick"><circle cx="${SX}" cy="${G - 140}" r="760" fill="url(#mkFire)"/>
        <path d="M${SX - 80},${G - 110}H${SX + 80}L${SX + 260},${G - 1000}H${SX - 260}Z" fill="url(#mkShaftUp)"/><path d="M${SX - 40},${G - 110}H${SX + 40}L${SX + 120},${G - 1000}H${SX - 120}Z" fill="url(#mkShaftUp)" opacity=".7"/><circle cx="${SX}" cy="${G - 110}" r="200" fill="url(#mkHaz)"/></g>
        ${[-50, -20, 12, 44, -34, 0, 30].map((cx, k) => `<ellipse cx="${SX + cx}" cy="${G + 70 + (k < 4 ? -184 : -198)}" rx="18" ry="9" fill="#ff7a2a" opacity=".85"/>`).join("")}</g>
      <g id="${id}-steam" opacity="0">${[-40, 10, 50, -10, 30].map((dx, k) => `<ellipse cx="${SX + dx}" cy="${G - 200 - k * 60}" rx="${70 + k * 20}" ry="${40 + k * 12}" fill="#e9ecef" opacity=".55"/>`).join("")}</g>
      <g id="${id}-gas" opacity="${o.gas ?? 0}"><rect x="-900" y="300" width="2900" height="${G - 300}" fill="#a79cc8" opacity=".3"/>
        ${Array.from({ length: 80 }, () => `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(320 + r() * (G - 340))}" r="${f1(5 + r() * 9)}" fill="#d6cff2" opacity=".55"/>`).join("")}</g>`);
  }

  // the abandoned village in the fog: stilt houses fading into the white, a leaning wooden sign "บ้านหมอก" (#id-sign),
  // the near house (o.house) with steps, a door (#id-door, orange inside when o.glow) and a window (#id-win),
  // villagers standing round it (o.vill: [{x, y, s, op}]) and fog in front
  const K = INK;
  function fogVillage(L, o = {}) {
    const id = o.id || "fv", r = mk(o.seed || 149), G = o.ground ?? 1500;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#4b5159"/><circle cx="${o.moonX ?? 860}" cy="260" r="760" fill="url(#mkMoon)"/>`);
    const hut = (x, y, sc, c) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${sc})"><path d="M-200,-300L0,-470L200,-300Z" fill="${c}"/><rect x="-170" y="-300" width="340" height="200" fill="${c}"/>
        ${[-150, -50, 50, 150].map((px) => `<rect x="${px - 8}" y="-100" width="16" height="100" fill="${c}"/>`).join("")}</g>`;
    let far = "";
    for (let k = 0; k < 6; k++) far += hut(-600 + k * 450 + r() * 120, G - 260, 0.55 + r() * 0.2, "#3a4048");
    put(L.far, far + fogBands(r, G - 700, G - 100, 5, 0.85));
    let mid = "";
    [[-260, 0.8], [1320, 0.85]].forEach(([x, sc]) => (mid += hut(x, G - 60, sc, "#2c3138")));
    put(L.mid, mid + fogBands(r, G - 500, G, 3, 0.7));
    let s = `<rect x="-900" y="${G}" width="2900" height="1300" fill="#3a382f"/><path d="M200,2600Q420,${G + 300} 520,${G}H600Q560,${G + 300} 900,2600Z" fill="#4a463a"/>`;
    for (let k = 0; k < 40; k++) s += `<path d="M${f1(-800 + r() * 2700)},${f1(G + 20 + r() * 900)}l-8,-26M${f1(-800 + r() * 2700)},${f1(G + 20 + r() * 900)}l6,-22" stroke="#2c2a22" stroke-width="5"/>`;
    // the house: a big Thai stilt house seen from the gable end — posts and bracing, a hammock, a water jar and firewood
    // underneath, plank walls, a deep gable roof with a moonlit edge, a railing, the door at the top of the stairs (#id-door,
    // #id-doorshut), two windows (#id-win) and a lantern; light from inside spills out as shafts through the fog (#id-wglow)
    if (o.house) {
      const h = o.house, hx = h.x ?? 540, hs = h.s ?? 1, lit = !!o.glow, WIN = lit ? "#f0a050" : "#14100d";
      const plank = (x0, x1, y0, y1, step, c) => Array.from({ length: Math.floor((x1 - x0) / step) }, (_, k) => `<path d="M${x0 + (k + 1) * step},${y0}V${y1}" stroke="${c}" stroke-width="${k % 3 ? 3 : 5}"/>`).join("");
      s += `<g transform="translate(${hx},${G}) scale(${hs})">
        <ellipse cx="0" cy="6" rx="560" ry="40" fill="#000" opacity=".35"/>
        ${[-430, -260, -90, 90, 260, 430].map((px) => `<rect x="${px - 16}" y="-214" width="32" height="214" fill="#2e241c" ${OUT}/>`).join("")}
        <path d="M-430,-180L-260,-40M-260,-180L-430,-40M260,-180L430,-40M430,-180L260,-40" stroke="#2a2018" stroke-width="12"/>
        <path d="M-90,-150Q0,-60 90,-150" stroke="#8a3a30" stroke-width="16" fill="none"/><path d="M-90,-150Q0,-60 90,-150" stroke="#2a2018" stroke-width="3" fill="none"/>
        <g transform="translate(170,0)"><path d="M-48,0Q-62,-58 -38,-88H38Q62,-58 48,0Z" fill="#6b3a26" ${OUT}/><ellipse cx="0" cy="-88" rx="38" ry="9" fill="#2a1610" ${OUT}/><path d="M-30,-50q30,10 60,0" stroke="#8a5a40" stroke-width="5" fill="none"/></g>
        <g transform="translate(340,0)">${[[-40, -20], [0, -20], [40, -20], [-20, -54], [20, -54], [0, -88]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="20" fill="#5a4030" ${OUT}/><circle cx="${x}" cy="${y}" r="8" fill="#8a6a4a"/>`).join("")}</g>
        <rect x="-480" y="-232" width="960" height="34" fill="#3a2c22" ${OUT}/>
        <rect x="-450" y="-580" width="900" height="350" fill="url(#mkWall)" ${OUT}/>${plank(-450, 450, -578, -232, 50, "#33261b")}<path d="M-450,-410H450" stroke="#2a1f17" stroke-width="10"/>
        <g id="${id}-door"><rect x="-250" y="-520" width="170" height="300" fill="${lit ? "#e8893e" : "#14100d"}" ${OUT}/><rect id="${id}-doorshut" x="-250" y="-520" width="170" height="300" fill="#1b1410" opacity="${o.doorShut ? 1 : 0}" ${OUT}/></g>
        <path d="M-250,-520L-300,-505V-235L-250,-220Z" fill="#4a3828" ${OUT}/>
        ${Array.from({ length: 6 }, (_, k) => `<rect x="${-276 - k * 16}" y="${-214 + k * 36}" width="${200}" height="18" fill="#3a2c22" ${OUT}/>`).join("")}<path d="M-270,-300L-380,0" stroke="#2e241c" stroke-width="12"/>
        <g id="${id}-win"><rect x="60" y="-500" width="200" height="190" fill="${WIN}" ${OUT}/><path d="M160,-500V-310M60,-405H260" stroke="#2a1f17" stroke-width="10"/></g>
        <path d="M60,-500L20,-515V-295L60,-310ZM260,-500L300,-515V-295L260,-310Z" fill="#4a3828" ${OUT}/>
        <rect x="330" y="-500" width="90" height="150" fill="${WIN}" ${OUT}/><path d="M375,-500V-350" stroke="#2a1f17" stroke-width="8"/>
        <path d="M-60,-300H450" stroke="#3a2c22" stroke-width="12"/>${Array.from({ length: 9 }, (_, k) => `<rect x="${-56 + k * 62}" y="-300" width="12" height="80" fill="#3a2c22"/>`).join("")}
        <path d="M-520,-580L0,-930L520,-580Z" fill="url(#mkWall)" ${OUT}/>${Array.from({ length: 15 }, (_, k) => { const x = -420 + k * 60; return `<path d="M${x},${f1(-580 - 350 * (1 - Math.abs(x) / 520) + 8)}V-584" stroke="#2a1f17" stroke-width="${k % 3 ? 3 : 5}"/>`; }).join("")}
        <path d="M-520,-580L0,-930L520,-580Z" fill="none" ${OUT}/><path d="M0,-860l30,40l-30,40l-30,-40z" fill="${lit ? "#c8702e" : "#14100d"}" ${OUT}/>
        <path d="M-590,-556L0,-980L590,-556L560,-534L0,-940L-560,-534Z" fill="url(#mkRoof)" ${OUT}/>
        <path d="M-590,-556L0,-980" stroke="#b9c9dc" stroke-width="6" opacity=".55"/><path d="M0,-980L590,-556" stroke="#b9c9dc" stroke-width="4" opacity=".25"/>
        <path d="M-40,-556V-480" stroke="#1b1714" stroke-width="4"/><g transform="translate(-40,-450)"><rect x="-16" y="-30" width="32" height="44" rx="6" fill="${lit ? "#ffd27a" : "#2a2420"}" ${OUT}/><path d="M-20,-30H20M-20,14H20" stroke="${K}" stroke-width="6"/></g></g>`;
    }
    if (o.sign !== false) s += `<g id="${id}-sign" transform="translate(${o.signX ?? 860},${G + 40}) rotate(-6)"><rect x="-12" y="-420" width="24" height="420" fill="#4a3828" ${OUT}/>
        <rect x="-170" y="-470" width="340" height="120" rx="8" fill="#6b5236" ${OUT}/><path d="M-150,-440L-90,-400M120,-460L140,-380" stroke="#4a3828" stroke-width="4"/>
        <text x="0" y="-388" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="62" fill="#e9e0c8" opacity=".85">บ้านหมอก</text></g>`;
    (o.vill || []).forEach((v) => (s += `<g opacity="${v.op ?? 0.85}">${villager(v.x, v.y ?? G + 20, v.s ?? 0.7, { wave: false, look: v.look })}</g>`));
    put(L.set, s);
    if (o.house && o.glow) {
      const h = o.house, hx = h.x ?? 540, hs = h.s ?? 1;
      put(L.glow, `<g id="${id}-wglow"><g transform="translate(${hx},${G}) scale(${hs})"><g class="flick">
        <path d="M-250,-220H-80L60,40H-470Z" fill="url(#mkShaft)"/><path d="M60,-310H260L420,40H-60Z" fill="url(#mkShaft)" opacity=".7"/><path d="M330,-350H420L520,40H300Z" fill="url(#mkShaft)" opacity=".5"/>
        <circle cx="-165" cy="-370" r="240" fill="url(#mkHaz)" opacity=".45"/><circle cx="160" cy="-405" r="220" fill="url(#mkHaz)" opacity=".4"/><circle cx="-40" cy="-450" r="90" fill="url(#mkHaz)" opacity=".6"/>
        <ellipse cx="-200" cy="30" rx="300" ry="40" fill="#ffb35a" opacity=".16"/><ellipse cx="180" cy="30" rx="260" ry="34" fill="#ffb35a" opacity=".12"/></g></g></g>`);
    }
    put(L.fg, fogBands(r, G - 500, G + 500, 4, o.fogFg ?? 0.6) + (o.grass === false ? "" : fgGrass(r, 2010, 8)) + (o.branch ? fgBranch(o.branch.x ?? -260, o.branch.y ?? 90, o.branch.flip ?? 1) : ""));
  }

  // from outside, looking in through the window: the room lit by the stove; actors go in the act layer,
  // the wall with the window hole (#id-frame) is moved over them with TOP
  function windowLook(L, o = {}) {
    const id = o.id || "wl", r = mk(o.seed || 151), G = 1330;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#3a2c22"/>`);
    let f = "";
    for (let x = -880; x < 2000; x += 74) f += `<path d="M${x},-600V${G}" stroke="#2a1f17" stroke-width="5"/>`;
    put(L.far, f + `<rect x="-900" y="${G}" width="2900" height="1200" fill="#4a3628"/>`);
    put(L.set, stove(id, o.stoveX ?? 700, G + 60, 1.1));
    put(L.act, `<g id="${id}-frame"><path d="M-900,-600H2000V2600H-900ZM160,560H920V1500H160Z" fill="#4a3828" fill-rule="evenodd"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-880 + k * 100},-600V560M${-880 + k * 100},1500V2600" stroke="#33261b" stroke-width="6"/>`).join("")}
      <rect x="140" y="540" width="800" height="980" fill="none" stroke="#2a1f17" stroke-width="40"/><path d="M540,560V1500M160,1030H920" stroke="#2a1f17" stroke-width="22"/>
      <path d="M140,540L20,500V1560L140,1520Z" fill="#3a2c22" ${OUT}/><path d="M940,540L1060,500V1560L940,1520Z" fill="#3a2c22" ${OUT}/>
      <rect x="160" y="560" width="760" height="940" fill="#9fb3c4" opacity=".08"/></g>`);
    put(L.glow, `<g class="flick"><circle cx="${o.stoveX ?? 700}" cy="${G - 160}" r="700" fill="url(#mkFire)"/><circle cx="${o.stoveX ?? 700}" cy="${G - 140}" r="180" fill="url(#mkHaz)"/></g>`);
    put(L.fg, fogBands(r, 300, 1900, 4, 0.5));
  }

  // the back of เจ's camera held in two round fists: the photo on the screen (the three at the stove, and the dead
  // filling the room behind them, #id-ghosts)
  function photoLCD(L, o = {}) {
    const id = o.id || "pl", r = mk(o.seed || 157);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#1a1410"/><circle cx="540" cy="1500" r="1000" fill="url(#mkFire)"/>`);
    let sc = `<rect x="150" y="690" width="780" height="520" fill="#3a2c22"/>`;
    for (let x = 150; x < 930; x += 40) sc += `<path d="M${x},690V1010" stroke="#2a1f17" stroke-width="3"/>`;
    sc += `<rect x="150" y="1010" width="780" height="200" fill="#4a3628"/>`;
    let gh = "";
    [[230, 1040, 0.42], [850, 1040, 0.42], [330, 990, 0.34], [760, 990, 0.34], [420, 960, 0.3], [660, 960, 0.3], [540, 945, 0.28], [180, 1110, 0.5], [900, 1110, 0.5]]
      .filter(([x]) => !(o.mother && x === 330)).forEach(([x, y, k]) => (gh += ghostSit(x, y, k)));
    sc += `<g id="${id}-ghosts" opacity="${o.ghosts ?? 1}">${gh}</g>`;
    if (o.mother) sc += `<g id="${id}-mother">${womanSit(330, 1000, 0.4)}</g>`;
    const kid = (x, y, top, hair) => `<g transform="translate(${x},${y})"><path d="M-44,0Q-50,-80 -26,-100H26Q50,-80 44,0Z" fill="${top}" ${OUT}/><circle cx="0" cy="-126" r="30" fill="#ecbf98" ${OUT}/>${hair}
        <path d="M-12,-122q4,-4 8,0M6,-122q4,-4 8,0" stroke="${INK}" stroke-width="3" fill="none"/><path d="M-10,-110q10,8 20,0" stroke="${INK}" stroke-width="3" fill="none"/></g>`;
    sc += kid(430, 1150, "#d9a12c", `<path d="M-32,-132Q-30,-168 0,-168Q30,-168 32,-132Z" fill="#1b1d20"/>`) + kid(650, 1150, "#a99ad0", `<path d="M-36,-120Q-38,-172 0,-172Q38,-172 36,-120Q30,-150 0,-152Q-30,-150 -36,-120Z" fill="#a99ad0" ${OUT}/>`);
    sc += stove(id, 540, 1200, 0.42) + `<circle cx="540" cy="1110" r="320" fill="url(#mkFire)"/><rect x="150" y="690" width="780" height="520" fill="#fff" opacity=".06"/>`;
    put(L.set, `<rect x="40" y="560" width="1000" height="800" rx="60" fill="#1b1d20" ${OUT}/><rect x="70" y="590" width="940" height="740" rx="44" fill="#24272c"/>
      <defs><clipPath id="${id}-clip"><rect x="150" y="690" width="780" height="520" rx="10"/></clipPath></defs>
      <g clip-path="url(#${id}-clip)">${sc}</g><rect x="150" y="690" width="780" height="520" rx="10" fill="none" stroke="#0b0d10" stroke-width="10"/>
      <text x="170" y="732" font-family="Kanit" font-weight="700" font-size="28" fill="#f4f2ea">1/1</text><text x="910" y="732" text-anchor="end" font-family="Kanit" font-weight="700" font-size="28" fill="#f4f2ea">ISO 3200</text>
      <circle cx="540" cy="1272" r="34" fill="#30353c" ${OUT}/>${[380, 700].map((x) => `<rect x="${x - 40}" y="1256" width="80" height="32" rx="10" fill="#30353c" ${OUT}/>`).join("")}`);
    const fistArm = (x, y, side) => `<path d="M${x},${y}L${x + side * 260},2300" stroke="${INK}" stroke-width="150" stroke-linecap="round"/><path d="M${x},${y}L${x + side * 260},2300" stroke="#5f6b4a" stroke-width="140" stroke-linecap="round"/>
        <g transform="translate(${x},${y}) rotate(${side * 30})">${Hands.fist({ r: 90, skin: "#dca57c", shade: "#bb8560" })}</g>`;
    put(L.act, fistArm(70, 1250, -1) + fistArm(1010, 1250, 1));
    put(L.glow, `<rect x="150" y="690" width="780" height="520" fill="#ffe7c0" opacity=".05"/>`);
  }

  // the bundle they dragged out: a figure wrapped head to foot in the villagers' brown blanket, slumped by the steps;
  // a pale hand comes out of it (#id-hand) and the hood lifts (#id-hood)
  function bundleClose(L, o = {}) {
    const id = o.id || "bc", r = mk(o.seed || 163), G = 1640;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#4b5159"/>` + fogBands(r, -200, 1600, 6, 0.7));
    put(L.far, `<rect x="-900" y="${G}" width="2900" height="1200" fill="#3a382f"/>${Array.from({ length: 5 }, (_, k) => `<rect x="${-200 + k * 10}" y="${G - 600 + k * 120}" width="${520 - k * 20}" height="40" fill="#3a2c22" ${OUT}/>`).join("")}`);
    put(L.set, `<g transform="translate(560,${G + 40})"><path d="M-330,0Q-360,-420 -170,-640Q0,-760 170,-640Q360,-420 330,0Z" fill="${BLK}" ${OUT}/>
        <path d="M-220,-120Q0,-60 220,-120M-260,-300Q-60,-240 120,-330" stroke="#463a30" stroke-width="12" fill="none"/>
        <g id="${id}-hood"><path d="M-170,-640Q0,-780 170,-640Q140,-520 0,-500Q-140,-520 -170,-640Z" fill="#4e4036" ${OUT}/><ellipse cx="0" cy="-590" rx="96" ry="70" fill="#0b0d10"/>
          <g id="${id}-eyes" opacity="${o.eyes ?? 0}"><ellipse cx="-30" cy="-590" rx="10" ry="12" fill="${PALE}"/><ellipse cx="30" cy="-590" rx="10" ry="12" fill="${PALE}"/></g></g>
        <g id="${id}-hand" opacity="${o.hand ?? 0}"><g transform="translate(150,-470) rotate(-20)">${Hands.fist({ r: 78, skin: PALE, shade: "#9aa6a2" })}</g></g></g>`);
    put(L.fg, fogBands(r, 900, 2000, 3, 0.45));
  }


  // ================= EP.3 (อย่ากลับเข้าไป): the pickup in the fog, its driver, the morning at the pump =================
  const RED = "#8a2f2a", SCARF = "#5a6b7a";
  // the woman in the red cardigan and headscarf, seated (in the photo): the face pale, smiling at the camera
  const womanSit = (x, y, s) => `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">
      <path d="M-96,0Q-104,-150 -52,-204Q0,-232 52,-204Q104,-150 96,0Z" fill="${RED}"/><path d="M-20,-200L0,-150L20,-200" fill="#efe6d6"/>
      <ellipse cx="0" cy="-252" rx="40" ry="48" fill="#d9c7b8"/><path d="M-50,-250Q-56,-316 0,-318Q56,-316 50,-250Q40,-290 0,-292Q-40,-290 -50,-250Z" fill="${SCARF}"/>
      <path d="M-22,-256q8,-6 14,0M8,-256q8,-6 14,0" stroke="#2e2a26" stroke-width="5" fill="none"/><path d="M-16,-226q16,12 32,0" stroke="#2e2a26" stroke-width="5" fill="none"/></g>`;

  // a small Thai pickup seen from the side, nose to the right, the same length as car() so carLights() fits it.
  // o.dusty (thick dust, rust), o.flat (flat tyres), o.mud (fresh wet mud on the wheels and sills)
  function pickup(id, x, y, s, o = {}) {
    const body = o.dusty ? "#9a6a5a" : "#8a3a30", tyreR = o.flat ? 52 : 64, ty = o.flat ? -8 : -20;
    const mud = o.mud ? `<g id="${id}-mud">${[-200, 210].map((wx) => `<path d="M${wx - 70},${ty - 10}Q${wx - 40},${ty + 40} ${wx},${ty + 46}Q${wx + 50},${ty + 40} ${wx + 72},${ty}" stroke="#3a2416" stroke-width="22" fill="none" stroke-linecap="round"/>
        <ellipse cx="${wx - 30}" cy="${ty + 30}" rx="18" ry="9" fill="#5a3a22"/><circle cx="${wx + 20}" cy="${ty + 36}" r="5" fill="#c9a77a" opacity=".7"/>`).join("")}
        <path d="M-320,-30h640" stroke="#3a2416" stroke-width="16" stroke-dasharray="40 20 70 30" opacity=".85"/></g>` : "";
    return `<g id="${id}" transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})">
      <ellipse cx="0" cy="8" rx="330" ry="22" fill="#05080b" opacity=".55"/>
      <path d="M-330,-40V-150H-20V-40Z" fill="${body}" ${OUT}/><path d="M-330,-150H-20" stroke="#5a2420" stroke-width="10"/>
      <path d="M-20,-40V-150Q-10,-250 60,-262H150Q200,-258 236,-170L322,-150Q348,-140 344,-80V-40Z" fill="${body}" ${OUT}/>
      <path d="M10,-160Q20,-240 70,-246H140Q176,-240 210,-170L214,-160Z" fill="url(#mkGlass)" ${OUT}/>
      <path d="M-330,-40H344V-14Q344,-4 330,-4H-316Q-330,-6 -330,-20Z" fill="#3a3a3a" ${OUT}/>
      ${[-200, 210].map((wx) => `<g><circle cx="${wx}" cy="${ty}" r="${tyreR}" fill="#15181c" ${OUT}/><circle cx="${wx}" cy="${ty}" r="30" fill="${o.dusty ? "#8a6a4a" : "#8a929a"}" ${OUT}/><circle cx="${wx}" cy="${ty}" r="8" fill="${INK}"/></g>`).join("")}
      <rect x="318" y="-130" width="26" height="30" rx="8" fill="#f4f0d8" ${OUT}/><rect x="-336" y="-128" width="18" height="40" rx="6" fill="#a8261c" ${OUT}/>
      ${o.dusty ? `<g fill="#c9b89a" opacity=".4"><path d="M-330,-40V-150H-20V-40Z"/><path d="M-20,-40V-150Q-10,-250 60,-262H150Q200,-258 236,-170L322,-150Q348,-140 344,-80V-40Z"/></g>
        ${[-300, -250, -120, -60, 260].map((vx, k) => `<path d="M${vx},-40q${k % 2 ? 12 : -10},-40 ${k % 2 ? -4 : 6},-${70 + (k % 3) * 20}" stroke="#4a6a3a" stroke-width="8" fill="none" opacity=".8"/><circle cx="${vx + 4}" cy="${-110 - (k % 3) * 20}" r="7" fill="#4a6a3a" opacity=".8"/>`).join("")}` : ""}
      ${mud}</g>`;
  }

  // the pickup's driver window at night from outside: the door, the dark cab, the driver in a red cardigan and a headscarf
  // with the face in shadow, two pale round hands on the wheel (#id-driver); dash glow (#id-dash)
  function pickupWindow(L, o = {}) {
    const id = o.id || "pw", r = mk(o.seed || 167);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#4b5159"/>` + fogBands(r, -200, 2400, 7, 0.7));
    put(L.far, `<rect x="-900" y="600" width="2900" height="900" fill="#0d0f12"/><g id="${id}-driver"><g transform="translate(600,1330) scale(0.92)">
        <path d="M-230,0Q-250,-300 -150,-380Q0,-430 150,-380Q250,-300 230,0Z" fill="${RED}"/><path d="M-40,-390L0,-320L40,-390" fill="#efe6d6" opacity=".6"/>
        <path d="M-120,-430Q-130,-640 0,-650Q130,-640 120,-430Q100,-470 0,-470Q-100,-470 -120,-430Z" fill="${SCARF}"/><ellipse cx="0" cy="-520" rx="88" ry="104" fill="#07090b"/>
        <path d="M118,-450q40,30 30,90" stroke="${SCARF}" stroke-width="26" fill="none" stroke-linecap="round"/></g></g>
      <g id="${id}-dash"><rect x="-900" y="1120" width="2900" height="380" fill="#141618"/><rect x="200" y="1120" width="240" height="40" rx="8" fill="#7fd1ff" opacity=".12"/></g>
      <g><ellipse cx="600" cy="1080" rx="260" ry="60" fill="none" stroke="#2a2d33" stroke-width="30"/>
        ${[[380, 1080, -1], [820, 1080, 1]].map(([hx, hy, sd]) => `<g transform="translate(${hx},${hy}) rotate(${sd * 20})">${Hands.fist({ r: 44, skin: "#d6dcd8", shade: "#a6b0ac" })}</g>`).join("")}</g>`);
    put(L.set, `<path d="M-900,-600H2000V2600H-900ZM130,560Q150,460 300,440H920Q990,450 1000,560V1180H130Z" fill="#8a3a30" fill-rule="evenodd" ${OUT}/>
      <path d="M130,560Q150,460 300,440H920Q990,450 1000,560V1180H130Z" fill="none" stroke="#1b1d20" stroke-width="26"/>
      <rect x="-900" y="1180" width="2900" height="40" fill="#5a2420"/><rect x="700" y="1300" width="160" height="34" rx="12" fill="#3a2a26" ${OUT}/>
      <path d="M-900,1600H2000" stroke="#5a2420" stroke-width="8"/><rect x="130" y="560" width="870" height="620" fill="#9fb3c4" opacity=".06"/>`);
    put(L.fg, fogBands(r, 200, 2000, 3, 0.45));
  }

  // the pump in the morning: pale sky, thin fog, tubes off; the old pickup behind the pump (o.oldTruck {x})
  function gasMorning(L, o = {}) {
    gasStation(L, { ...o, car: o.car ?? false });
    L.sky.innerHTML = `<rect x="-900" y="-600" width="2900" height="3400" fill="#b9c3cc"/><circle cx="1200" cy="420" r="260" fill="#fff6dc" opacity=".35"/>`;
    L.glow.innerHTML = "";
    L.far.querySelectorAll("path").forEach((p) => p.setAttribute("fill", "#7d8a96"));
    if (o.oldTruck) put(L.set, pickup(`${o.id || "gm"}-old`, o.oldTruck.x, (o.ground ?? 1480) + 40, o.oldTruck.s ?? 0.9, { dusty: true, flat: true, mud: o.oldTruck.mud }));
  }

  // close-up of the old pickup's front wheel: rust, dust, vines, and fresh wet mud on the tyre (#id-mud glints)
  function wheelClose(L, o = {}) {
    const id = o.id || "wc", r = mk(o.seed || 173);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#a9b3bc"/>`);
    put(L.far, `<rect x="-900" y="1500" width="2900" height="1200" fill="#9a8a6a"/>${Array.from({ length: 30 }, () => `<circle cx="${f1(-600 + r() * 2200)}" cy="${f1(1520 + r() * 800)}" r="${f1(3 + r() * 8)}" fill="#7a6a4a" opacity=".6"/>`).join("")}`);
    let s = `<path d="M-900,300H2000V1180Q1500,1180 1200,1000Q900,800 540,800Q180,800 -120,1000Q-420,1180 -900,1180Z" fill="#9a6a5a" ${OUT}/>
      <path d="M-900,300H2000V1180Q1500,1180 1200,1000Q900,800 540,800Q180,800 -120,1000Q-420,1180 -900,1180Z" fill="#b9a68a" opacity=".45"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-200 + k * 160},300q30,200 -20,420" stroke="#4a6a3a" stroke-width="12" fill="none" opacity=".75"/>`).join("")}
      <g transform="translate(540,1250)"><circle r="430" fill="#15181c" ${OUT}/><circle r="200" fill="#8a6a4a" ${OUT}/><circle r="60" fill="#5a4a3a" ${OUT}/>
        ${Array.from({ length: 6 }, (_, k) => `<circle cx="${f1(120 * Math.cos(k * Math.PI / 3))}" cy="${f1(120 * Math.sin(k * Math.PI / 3))}" r="16" fill="#3a2a1f"/>`).join("")}
        ${Array.from({ length: 24 }, (_, k) => `<path d="M${f1(330 * Math.cos(k * Math.PI / 12))},${f1(330 * Math.sin(k * Math.PI / 12))}L${f1(420 * Math.cos(k * Math.PI / 12))},${f1(420 * Math.sin(k * Math.PI / 12))}" stroke="#2a2d33" stroke-width="16"/>`).join("")}
        <g id="${id}-mud"><path d="M-420,60Q-380,300 -150,400Q100,450 300,330Q400,250 425,120L330,90Q300,250 140,320Q-60,370 -230,280Q-330,200 -340,60Z" fill="#3a2416"/>
          <path d="M-300,240Q-150,360 60,360" stroke="#6a4a2e" stroke-width="10" fill="none" opacity=".8"/>
          ${[[-260, 300, 34], [-80, 380, 26], [180, 350, 30], [340, 200, 22]].map(([cx, cy, rr]) => `<ellipse cx="${cx}" cy="${cy}" rx="${rr}" ry="${rr * 0.6}" fill="#4a2e1a"/><ellipse cx="${cx - rr * 0.3}" cy="${cy - rr * 0.25}" rx="${rr * 0.35}" ry="${rr * 0.18}" fill="#e9d8c0" opacity=".75" class="glint"/>`).join("")}
          ${Array.from({ length: 10 }, () => `<circle cx="${f1(-400 + r() * 800)}" cy="${f1(-200 + r() * 300)}" r="${f1(6 + r() * 12)}" fill="#3a2416"/>`).join("")}</g></g>`;
    put(L.set, s);
  }

  // ---------------- cast ----------------
  Object.assign(Rig.CAST, {
    mintFake: { // the thing by the stove in มิ้นท์'s jacket and beanie: the villagers' grey skin
      skin: "#c9d3cf", skinS: "#9aa6a2", top: "#d9a12c", topS: "#b5841c", sleeve: "#d9a12c", sleeveS: "#b5841c",
      pants: "#2f3438", pantsS: "#22272a", shoe: "#ece6da", belt: "#b5841c",
      torsoExtra: `${[-430, -390, -350].map((y) => `<path d="M-56,${y}H56" stroke="#b5841c" stroke-width="5"/>`).join("")}<path d="M0,-484V-306" stroke="#8a6414" stroke-width="5"/>`,
      hair: `<path d="M-50,-540Q-56,-606 0,-610Q56,-606 50,-540L54,-492Q42,-484 34,-494L32,-556Q0,-566 -32,-556L-34,-494Q-42,-484 -54,-492Z" fill="#231a16" ${OUT}/>
        <path d="M-50,-566Q-48,-626 0,-628Q48,-626 50,-566Z" fill="#1b1d20" ${OUT}/><path d="M-50,-566H50" stroke="#34383c" stroke-width="10"/>`,
    },
    mother: { // ยายแสง's mother, forty years ago: the same red cardigan, a headscarf, black hair
      skin: "#d6a982", skinS: "#b5876a", top: "#8a2f2a", topS: "#6b2420", sleeve: "#8a2f2a", sleeveS: "#6b2420",
      pants: "#3a3530", pantsS: "#2a2622", shoe: "#2a2420", belt: "#6b2420",
      torsoExtra: `<path d="M-24,-484L0,-420L24,-484" fill="#efe6d6" ${OUT}/><path d="M-30,-420V-306M30,-420V-306" stroke="#6b2420" stroke-width="6"/>`,
      hair: `<path d="M-48,-544Q-52,-610 0,-612Q50,-610 48,-546Q40,-580 0,-584Q-38,-580 -48,-544Z" fill="#231a16" ${OUT}/>
        <path d="M-56,-560Q-50,-626 0,-628Q50,-626 56,-560Q30,-590 0,-592Q-30,-590 -56,-560Z" fill="#5a6b7a" ${OUT}/><path d="M50,-560q20,20 10,50" stroke="#5a6b7a" stroke-width="12" fill="none" stroke-linecap="round"/>`,
    },
    girl: { // ยายแสง as a little girl: a faded blue dress, two short pigtails (scale her ~0.55)
      skin: "#d6a982", skinS: "#b5876a", top: "#6a8aa8", topS: "#557390", sleeve: "#6a8aa8", sleeveS: "#557390",
      pants: "#6a8aa8", pantsS: "#557390", shoe: "#3a2f26", belt: "#557390",
      hair: `<path d="M-48,-546Q-52,-606 0,-610Q50,-606 48,-548Q40,-580 0,-584Q-38,-580 -48,-546Z" fill="#231a16" ${OUT}/><circle cx="-56" cy="-540" r="16" fill="#231a16"/><circle cx="56" cy="-540" r="16" fill="#231a16"/>`,
    },
    mint: { // มิ้นท์: driver, mustard puffer jacket, black beanie, shoulder-length hair
      skin: "#ecbf98", skinS: "#cc9a74", top: "#d9a12c", topS: "#b5841c", sleeve: "#d9a12c", sleeveS: "#b5841c",
      pants: "#2f3438", pantsS: "#22272a", shoe: "#ece6da", belt: "#b5841c",
      torsoExtra: `${[-430, -390, -350].map((y) => `<path d="M-56,${y}H56" stroke="#b5841c" stroke-width="5"/>`).join("")}<path d="M0,-484V-306" stroke="#8a6414" stroke-width="5"/><path d="M-40,-490Q0,-470 40,-490V-470Q0,-452 -40,-470Z" fill="#b5841c" ${OUT}/>`,
      hair: `<path d="M-50,-540Q-56,-606 0,-610Q56,-606 50,-540L54,-492Q42,-484 34,-494L32,-556Q0,-566 -32,-556L-34,-494Q-42,-484 -54,-492Z" fill="#231a16" ${OUT}/>
        <path d="M-50,-566Q-48,-626 0,-628Q48,-626 50,-566Z" fill="#1b1d20" ${OUT}/><path d="M-50,-566H50" stroke="#34383c" stroke-width="10"/>`,
      face: `<g fill="#e09a86" opacity=".5"><ellipse cx="-24" cy="-526" rx="7" ry="3.5"/><ellipse cx="30" cy="-526" rx="7" ry="3.5"/></g>`,
    },
    jay: { // เจ: photographer, olive field jacket, camera strap across the chest, short messy hair
      skin: "#dca57c", skinS: "#bb8560", top: "#5f6b4a", topS: "#4a5539", sleeve: "#5f6b4a", sleeveS: "#4a5539",
      pants: "#3b4a63", pantsS: "#2c3850", shoe: "#3a2f26", belt: "#4a5539",
      torsoExtra: `<path d="M-46,-484L40,-330" stroke="#1b1d20" stroke-width="10"/><g transform="translate(14,-380)"><rect x="-34" y="-22" width="68" height="46" rx="8" fill="#1b1d20" ${OUT}/><circle cx="6" cy="2" r="15" fill="#3a4654" stroke="#9aa2aa" stroke-width="4"/></g>
        <rect x="-50" y="-450" width="34" height="30" rx="4" fill="#4a5539" ${OUT}/>`,
      hair: `<path d="M-48,-552Q-52,-612 -4,-614Q44,-614 48,-556L38,-576L26,-562L12,-580L-4,-564L-18,-580L-32,-562Z" fill="#231c18" ${OUT}/>`,
      face: `<path d="M-10,-506q12,6 24,0" stroke="#7a5a44" stroke-width="3" fill="none" opacity=".5"/>`,
    },
    wan: { // หวาน: eighteen, oversized lilac hoodie with the hood up, two braids
      skin: "#efc6a0", skinS: "#cf9d79", top: "#a99ad0", topS: "#8a7ab4", sleeve: "#a99ad0", sleeveS: "#8a7ab4",
      pants: "#3a3f45", pantsS: "#2b2f34", shoe: "#ece6da", belt: "#8a7ab4",
      torsoExtra: `<rect x="-30" y="-380" width="60" height="40" rx="10" fill="#8a7ab4" ${OUT}/><path d="M-10,-470v40M10,-470v36" stroke="#f4ecd8" stroke-width="4" stroke-linecap="round"/>`,
      hair: `<path d="M-40,-540Q-60,-470 -48,-430M40,-540Q60,-470 48,-430" stroke="#231a16" stroke-width="16" stroke-linecap="round" fill="none"/>
        <path d="M-48,-546Q-54,-606 0,-610Q52,-606 48,-548Q40,-580 0,-584Q-38,-580 -48,-546Z" fill="#231a16" ${OUT}/>
        <path d="M-62,-520Q-70,-628 0,-634Q70,-628 62,-520Q56,-590 0,-596Q-56,-590 -62,-520Z" fill="#a99ad0" ${OUT}/>`,
      face: `<g fill="#e09a86" opacity=".55"><ellipse cx="-24" cy="-526" rx="7" ry="3.5"/><ellipse cx="30" cy="-526" rx="7" ry="3.5"/></g>`,
    },
    saeng: { // ยายแสง: petrol-station owner, faded red cardigan over a white blouse, grey hair in a low bun, headscarf
      skin: "#c99a74", skinS: "#a87a56", top: "#8a2f2a", topS: "#6b2420", sleeve: "#8a2f2a", sleeveS: "#6b2420",
      pants: "#3a3530", pantsS: "#2a2622", shoe: "#2a2420", belt: "#6b2420",
      torsoExtra: `<path d="M-24,-484L0,-420L24,-484" fill="#efe6d6" ${OUT}/><path d="M-30,-420V-306M30,-420V-306" stroke="#6b2420" stroke-width="6"/>`,
      hair: `<path d="M-48,-544Q-52,-610 0,-612Q50,-610 48,-546Q40,-580 0,-584Q-38,-580 -48,-544Z" fill="#b8b0a6" ${OUT}/>
        <path d="M-56,-560Q-50,-626 0,-628Q50,-626 56,-560Q30,-590 0,-592Q-30,-590 -56,-560Z" fill="#5a6b7a" ${OUT}/><path d="M50,-560q20,20 10,50" stroke="#5a6b7a" stroke-width="12" fill="none" stroke-linecap="round"/>`,
      face: `<path d="M-30,-560q8,-3 14,0M14,-560q8,-3 14,0" stroke="#7a5a44" stroke-width="2.5" fill="none"/><path d="M-26,-512q4,4 0,8M30,-512q-4,4 0,8" stroke="#a87a56" stroke-width="2" fill="none"/>`,
    },
  });

  Object.assign(Sets, { carPOV, roadSign, mountainRoad, gasStation, mirrorClose, roadFog, carInterior, carWindow, rearWindow, plateClose, topRoad, houseRoom, fogVillage, windowLook, photoLCD, bundleClose, pickupWindow, gasMorning, wheelClose });
  window.Mok = { villager, car, carLights, fogBands, fogBlobs, life, ghostSit, stove, wrapped, pickup, womanSit };
})();
