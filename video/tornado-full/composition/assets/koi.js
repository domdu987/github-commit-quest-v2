// Sets, creatures and close-ups for "เสียงกอย": a rain-soaked southern rainforest by day and night (misty
// depth layers, buttress trees, ferns, a stream that can turn muddy and rise), a watershed cross-section,
// a black palm-leaf manuscript (สมุดข่อย) for the legend, close-ups of a foot / leech / fingernail, mud
// footprints, aerial views and the one-legged kong koi. Same layer contract as sets.js; seeded RNG only.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);

  Sets.DEFS += `
    <linearGradient id="koiDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb2aa"/><stop offset=".55" stop-color="#c9d4cb"/><stop offset="1" stop-color="#dfe3d8"/></linearGradient>
    <linearGradient id="koiNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050b0e"/><stop offset=".6" stop-color="#0b1a20"/><stop offset="1" stop-color="#12262c"/></linearGradient>
    <linearGradient id="mistg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2ea" stop-opacity="0"/><stop offset=".5" stop-color="#eef2ea" stop-opacity=".7"/><stop offset="1" stop-color="#eef2ea" stop-opacity="0"/></linearGradient>
    <linearGradient id="mistn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5f7f86" stop-opacity="0"/><stop offset=".5" stop-color="#5f7f86" stop-opacity=".45"/><stop offset="1" stop-color="#5f7f86" stop-opacity="0"/></linearGradient>
    <linearGradient id="shaftg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6d8" stop-opacity=".34"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></linearGradient>
    <linearGradient id="waterg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5d8a86"/><stop offset=".5" stop-color="#8fb7ae"/><stop offset="1" stop-color="#6a958e"/></linearGradient>
    <linearGradient id="floodw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b5236"/><stop offset=".18" stop-color="#4a3824"/><stop offset="1" stop-color="#21180e"/></linearGradient>
    <linearGradient id="floodwF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4b3925"/><stop offset="1" stop-color="#1e160d"/></linearGradient>
    <linearGradient id="mudw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a6044"/><stop offset=".5" stop-color="#9c7d55"/><stop offset="1" stop-color="#806548"/></linearGradient>
    <radialGradient id="lantern"><stop offset="0" stop-color="#ffd07a" stop-opacity=".85"/><stop offset=".4" stop-color="#ffb35c" stop-opacity=".25"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient>
    <radialGradient id="clothglow"><stop offset="0" stop-color="#fff0c8" stop-opacity=".95"/><stop offset=".45" stop-color="#ffc77a" stop-opacity=".55"/><stop offset="1" stop-color="#7a3a12" stop-opacity="0"/></radialGradient>
    <radialGradient id="torchpool"><stop offset="0" stop-color="#fff3c8" stop-opacity=".6"/><stop offset=".55" stop-color="#fff3c8" stop-opacity=".16"/><stop offset="1" stop-color="#fff3c8" stop-opacity="0"/></radialGradient>
    <radialGradient id="skin3d" cx=".4" cy=".35"><stop offset="0" stop-color="#f3c9a2"/><stop offset=".7" stop-color="#dba57c"/><stop offset="1" stop-color="#b9845e"/></radialGradient>
    <radialGradient id="leechg" cx=".35" cy=".3"><stop offset="0" stop-color="#6d6a3a"/><stop offset=".6" stop-color="#3b3a22"/><stop offset="1" stop-color="#1c1c12"/></radialGradient>
    <linearGradient id="paperK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1714"/><stop offset="1" stop-color="#0f0d0b"/></linearGradient>
    <linearGradient id="diagBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16242a"/><stop offset="1" stop-color="#0d171b"/></linearGradient>`;

  const DAY = { sky: "url(#koiDay)", far: ["#a2b3aa", "#93a69c", "#b4c2b9"], mist: "url(#mistg)", mid: ["#6f877a", "#617a6c", "#52695d"], trunkM: "#5a685e",
    set: ["#36533f", "#2c4535", "#43704f"], trunk: "#41493f", bark: "#2b322b", moss: "#6f9150", ground: "#4a4233", litter: ["#5f5340", "#3a3329", "#6e6147", "#7a5a3a"],
    trail: "#7b6a4f", fg: ["#1d3127", "#274233", "#335a40"], hi: "#86ad78", rock: "#6b6f66" };
  const NIGHT = { sky: "url(#koiNight)", far: ["#13252b", "#102026", "#18303a"], mist: "url(#mistn)", mid: ["#0f1f24", "#0d1b20", "#0b171b"], trunkM: "#101c1d",
    set: ["#0e1d1b", "#0b1716", "#132824"], trunk: "#111916", bark: "#080d0c", moss: "#1a2b1c", ground: "#0f1513", litter: ["#151d19", "#0b100e", "#1a221d", "#1d1a14"],
    trail: "#1b201c", fg: ["#040908", "#071009", "#0b170f"], hi: "#29452f", rock: "#1c2220" };

  // ---------- vegetation builders ----------
  function clump(r, cx, cy, R, c1, c2, hi) {
    let s = "";
    for (let i = 0; i < 9; i++) {
      const a = r() * Math.PI * 2, d = r() * R * 0.55, rx = R * (0.32 + r() * 0.26), ry = rx * (0.55 + r() * 0.25);
      const x = cx + Math.cos(a) * d, y = cy + Math.sin(a) * d * 0.7;
      s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(rx)}" ry="${f1(ry)}" transform="rotate(${f1(r() * 180)} ${f1(x)} ${f1(y)})" fill="${i < 6 ? c1 : c2}"/>`;
    }
    if (hi) for (let i = 0; i < 3; i++) s += `<ellipse cx="${f1(cx - R * 0.3 + r() * R * 0.4)}" cy="${f1(cy - R * 0.35 + r() * R * 0.2)}" rx="${f1(R * 0.18)}" ry="${f1(R * 0.08)}" fill="${hi}" opacity=".45" transform="rotate(${f1(-20 + r() * 40)} ${f1(cx)} ${f1(cy)})"/>`;
    return s;
  }
  function trunk(x, base, top, w, col, bark, r) {
    const bend = (r() - 0.5) * w * 1.2;
    let s = `<path d="M${f1(x - w / 2)},${base}C${f1(x - w / 2 + bend)},${f1(base - (base - top) * 0.5)} ${f1(x - w * 0.4 + bend)},${f1(top + 60)} ${f1(x - w * 0.38 + bend)},${top}H${f1(x + w * 0.38 + bend)}C${f1(x + w * 0.4 + bend)},${f1(top + 60)} ${f1(x + w / 2 + bend)},${f1(base - (base - top) * 0.5)} ${f1(x + w / 2)},${base}Z" fill="${col}"/>`;
    if (bark) for (let k = 0; k < 3; k++) {
      const bx = x - w * 0.25 + k * w * 0.25 + bend * 0.5;
      s += `<path d="M${f1(bx)},${base - 10}Q${f1(bx + (r() - 0.5) * 14)},${f1((base + top) / 2)} ${f1(bx + bend * 0.4)},${top + 20}" stroke="${bark}" stroke-width="${f1(2 + w * 0.03)}" fill="none" opacity=".55"/>`;
    }
    return s;
  }
  // giant rainforest tree with flared buttress roots (พูพอน)
  function buttress(x, base, w, P, r, o = {}) {
    const top = o.top ?? -300, sh = P.bark;
    let s = `<g>`;
    const fin = (dir, reach, hgt, thick) => {
      const x0 = x + dir * w * 0.42, y0 = base - hgt;
      const xe = x + dir * reach;
      return `<path d="M${f1(x0)},${f1(y0)}C${f1(x0 + dir * reach * 0.25)},${f1(y0 + hgt * 0.35)} ${f1(xe - dir * reach * 0.25)},${f1(base - 30)} ${f1(xe)},${base + 6}L${f1(xe - dir * thick)},${base + 10}C${f1(x0 + dir * 10)},${base} ${f1(x0)},${f1(base - hgt * 0.4)} ${f1(x0 - dir * 10)},${f1(base - hgt * 0.3)}Z" fill="${P.trunk}"/>
        <path d="M${f1(x0)},${f1(y0 + 20)}C${f1(x0 + dir * reach * 0.25)},${f1(y0 + hgt * 0.4)} ${f1(xe - dir * reach * 0.3)},${f1(base - 20)} ${f1(xe - dir * 8)},${base}" stroke="${sh}" stroke-width="5" fill="none" opacity=".5"/>`;
    };
    s += fin(-1, w * 1.9, w * 1.25, 40) + fin(1, w * 1.6, w * 1.05, 34);
    s += `<path d="M${f1(x - w / 2)},${base}C${f1(x - w * 0.46)},${base - 500} ${f1(x - w * 0.4)},${top + 300} ${f1(x - w * 0.36)},${top}H${f1(x + w * 0.36)}C${f1(x + w * 0.4)},${top + 300} ${f1(x + w * 0.46)},${base - 500} ${f1(x + w / 2)},${base}Z" fill="${P.trunk}"/>`;
    s += `<path d="M${f1(x + w * 0.18)},${base}C${f1(x + w * 0.22)},${base - 500} ${f1(x + w * 0.2)},${top + 300} ${f1(x + w * 0.2)},${top}H${f1(x + w * 0.36)}C${f1(x + w * 0.4)},${top + 300} ${f1(x + w * 0.46)},${base - 500} ${f1(x + w / 2)},${base}Z" fill="${sh}" opacity=".45"/>`;
    s += fin(-1, w * 1.1, w * 0.7, 26) + fin(1, w * 0.95, w * 0.6, 22);
    for (let k = 0; k < 7; k++) { // bark ridges
      const bx = x - w * 0.36 + k * w * 0.11;
      s += `<path d="M${f1(bx)},${base - 40}C${f1(bx + (r() - 0.5) * 18)},${base - 600} ${f1(bx + (r() - 0.5) * 18)},${top + 400} ${f1(bx * 0.98 + x * 0.02)},${top}" stroke="${sh}" stroke-width="${f1(3 + r() * 4)}" fill="none" opacity=".4"/>`;
    }
    for (let k = 0; k < 6; k++) { // moss patches
      const my = base - 120 - r() * 900, mx = x - w * 0.45 + r() * w * 0.3;
      s += `<ellipse cx="${f1(mx)}" cy="${f1(my)}" rx="${f1(14 + r() * 30)}" ry="${f1(30 + r() * 60)}" fill="${P.moss}" opacity="${f1(0.45 + r() * 0.4)}"/>`;
    }
    if (o.vines !== false) for (let k = 0; k < 3; k++) s += liana(x - w * 0.3 + k * w * 0.35, top + 100 + r() * 300, 500 + r() * 500, P.set[2], r);
    return s + `</g>`;
  }
  function liana(x, y0, len, col, r) {
    let d = `M${f1(x)},${f1(y0)}`, y = y0, cx = x;
    const leaves = [];
    while (y < y0 + len) {
      const dy = 60 + r() * 50; cx += (r() - 0.5) * 30; y += dy;
      d += `Q${f1(cx + (r() - 0.5) * 40)},${f1(y - dy / 2)} ${f1(cx)},${f1(y)}`;
      if (r() < 0.6) leaves.push(`<ellipse cx="${f1(cx + (r() < 0.5 ? -12 : 12))}" cy="${f1(y)}" rx="14" ry="7" fill="${col}" transform="rotate(${f1(r() * 60 - 30)} ${f1(cx)} ${f1(y)})"/>`);
    }
    return `<path d="${d}" stroke="${col}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/>${leaves.join("")}`;
  }
  function frond(x, y, len, ang, curl, col, hi, w = 1) {
    const a = (ang * Math.PI) / 180;
    const ex = x + Math.sin(a) * len, ey = y - Math.cos(a) * len;
    const cx = x + Math.sin(a) * len * 0.55 + Math.cos(a) * curl, cy = y - Math.cos(a) * len * 0.55 + Math.sin(a) * curl;
    let s = `<path d="M${f1(x)},${f1(y)}Q${f1(cx)},${f1(cy)} ${f1(ex)},${f1(ey)}" stroke="${col}" stroke-width="${f1(5 * w)}" fill="none" stroke-linecap="round"/>`;
    const n = Math.round(len / 22);
    for (let k = 1; k < n; k++) {
      const t = k / n, it = 1 - t;
      const px = it * it * x + 2 * it * t * cx + t * t * ex, py = it * it * y + 2 * it * t * cy + t * t * ey;
      const tx = 2 * it * (cx - x) + 2 * t * (ex - cx), ty = 2 * it * (cy - y) + 2 * t * (ey - cy);
      const ln = Math.hypot(tx, ty) || 1, nx = -ty / ln, ny = tx / ln, L = (1 - t * 0.8) * 34 * w;
      const deg = (Math.atan2(ty, tx) * 180) / Math.PI;
      for (const sd of [-1, 1]) {
        const lx = px + nx * sd * L * 0.55, ly = py + ny * sd * L * 0.55;
        s += `<ellipse cx="${f1(lx)}" cy="${f1(ly)}" rx="${f1(L * 0.55)}" ry="${f1(L * 0.17)}" fill="${sd < 0 ? col : hi}" transform="rotate(${f1(deg + sd * 62)} ${f1(lx)} ${f1(ly)})"/>`;
      }
    }
    return s;
  }
  function fernBush(x, base, s, col, hi, r) {
    let o = "";
    for (let k = 0; k < 7; k++) o += frond(x, base, (150 + r() * 90) * s, -75 + k * 25 + (r() - 0.5) * 10, (k < 3 ? -1 : 1) * 40 * s, col, hi, s);
    return o;
  }
  function aloc(x, y, s, ang, col, vein) { // heart-shaped elephant-ear leaf on a stalk
    return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(ang)}) scale(${s})">
      <path d="M0,0V-60" stroke="${col}" stroke-width="10"/>
      <path d="M0,-60C-40,-80 -130,-90 -130,-170C-130,-250 -55,-300 0,-330C55,-300 130,-250 130,-170C130,-90 40,-80 0,-60Z" fill="${col}"/>
      <path d="M0,-66V-318M0,-120L-70,-180M0,-160L-60,-230M0,-120L70,-180M0,-160L60,-230M0,-210L-36,-270M0,-210L36,-270" stroke="${vein}" stroke-width="4" fill="none" opacity=".55"/></g>`;
  }
  function banana(x, y, s, ang, col, vein) {
    return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(ang)}) scale(${s})">
      <path d="M0,0C-60,-90 -70,-330 0,-460C70,-330 60,-90 0,0Z" fill="${col}"/>
      <path d="M0,-10V-450" stroke="${vein}" stroke-width="5" opacity=".6"/>
      <path d="M-46,-140L-10,-170M-52,-230L-8,-250M50,-180L8,-205M48,-290L6,-305" stroke="${vein}" stroke-width="5" opacity=".7"/></g>`;
  }
  function mist(y, h, fill, op = 1) { return `<rect x="-900" y="${y}" width="2900" height="${h}" fill="${fill}" opacity="${op}"/>`; }

  // ---------------- rainforest (day / night); trail, stream or a camp on the slope ----------------
  function rainforest(L, o = {}) {
    const r = mk(o.seed || 7);
    const night = o.time === "night", P = night ? NIGHT : DAY, G = o.ground ?? 1480;
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="${P.sky}"/>`);
    // far: misty giants
    let far = "";
    for (let i = 0; i < 16; i++) far += trunk(-700 + i * 170 + r() * 60, G - 220, -200, 26 + r() * 22, P.far[1], null, r);
    for (let x = -800; x < 1900; x += 110) far += clump(r, x, 120 + r() * 260, 150 + r() * 60, P.far[0], P.far[2]);
    for (let x = -800; x < 1900; x += 140) far += clump(r, x, G - 260 + r() * 60, 110, P.far[1], P.far[0]);
    put(L.far, far + mist(G - 700, 650, P.mist, night ? 0.9 : 1) + mist(-100, 600, P.mist, 0.6));
    // mid
    let mid = "";
    for (let i = 0; i < 10; i++) mid += trunk(-640 + i * 260 + r() * 90, G - 60, -300, 40 + r() * 30, P.trunkM, P.mid[2], r);
    for (let x = -800; x < 1900; x += 120) mid += clump(r, x, 40 + r() * 200, 170, P.mid[0], P.mid[1], night ? null : P.hi);
    for (let x = -800; x < 1900; x += 150) mid += fernBush(x, G - 30, 0.9, P.mid[1], P.mid[0], r);
    put(L.mid, mid + mist(G - 420, 420, P.mist, night ? 0.6 : 0.75));
    // set: ground, trail, stream, giant tree, ferns, camp
    let s = `<rect x="-900" y="${G - 40}" width="2900" height="1500" fill="${P.ground}"/>`;
    for (let i = 0; i < 260; i++) s += `<ellipse cx="${f1(-700 + r() * 2500)}" cy="${f1(G - 20 + r() * 700)}" rx="${f1(4 + r() * 10)}" ry="${f1(2 + r() * 4)}" fill="${P.litter[i % 4]}" opacity=".8"/>`;
    if (o.trail) s += `<path d="M380,2400C430,2000 520,1800 500,${G + 60}C490,${G} 520,${G - 30} 545,${G - 40}H585C600,${G - 20} 610,${G + 60} 640,1700C700,1900 780,2100 860,2400Z" fill="${P.trail}"/>
      ${[0, 1, 2, 3].map((k) => `<ellipse cx="${560 + (r() - 0.5) * 120}" cy="${G + 160 + k * 160}" rx="${40 + k * 18}" ry="${8 + k * 3}" fill="${night ? "#2a3a3e" : "#a9bcb8"}" opacity=".55"/>`).join("")}`;
    if (o.stream) s += stream(o.id || "rf", G, P, r, o.stream);
    s += buttress(o.treeX ?? 110, G + 30, o.treeW ?? 170, P, r, { top: -600 });
    if (o.tree2 !== false) s += buttress(o.tree2X ?? 1010, G + 10, 110, P, r, { top: -600, vines: false });
    for (let x = -600; x < 1800; x += 210) s += fernBush(x + r() * 80, G + 40 + r() * 40, 1.05, P.set[0], P.set[2], r);
    for (let k = 0; k < 8; k++) s += `<ellipse cx="${f1(-200 + r() * 1500)}" cy="${f1(G + 30 + r() * 120)}" rx="${f1(26 + r() * 30)}" ry="${f1(14 + r() * 12)}" fill="${P.rock}"/>`;
    if (o.camp) s += camp(o.id || "rf", G, P, o);
    put(L.set, s);
    // fg: framing leaves (blurred by the shot)
    if (o.fg !== false) {
      let fg = aloc(-40, 2100, 1.9, 18, P.fg[1], P.fg[2]) + aloc(150, 2150, 1.5, -12, P.fg[0], P.fg[2]) + banana(1150, 2150, 1.9, -28, P.fg[1], P.fg[2]) + banana(1010, 2200, 1.4, -8, P.fg[0], P.fg[2]);
      fg += frond(-120, -60, 520, 150, 80, P.fg[0], P.fg[1], 1.6) + frond(1220, -80, 560, -150, -90, P.fg[0], P.fg[1], 1.6);
      put(L.fg, fg);
    }
    if (o.shafts && !night) put(L.light, [0, 1, 2].map((k) => `<path class="shaft" d="M${180 + k * 260},-100L${330 + k * 260},-100L${620 + k * 200},2000L${420 + k * 200},2000Z" fill="url(#shaftg)" opacity="${0.8 - k * 0.2}"/>`).join(""));
    if (night && o.camp) put(L.glow, `<circle class="lglow" cx="${o.lanternX ?? 600}" cy="${G - 330}" r="420" fill="url(#lantern)"/>`);
  }

  // stream from the upper left into the bottom right; clear / muddy / flood layers for animation
  function stream(id, G, P, r, opt) {
    const pts = [[-200, G + 40], [200, G + 70], [420, G + 150], [520, G + 300], [720, G + 420], [1300, G + 520]];
    const width = (k) => 40 + k * 70;
    const band = (scale) => {
      let L1 = "", R1 = "";
      pts.forEach(([x, y], k) => { const w = width(k) * scale; L1 += `${k ? "L" : "M"}${x},${y - w / 2}`; R1 = `L${x},${y + w / 2}` + R1; });
      return L1 + R1 + "Z";
    };
    let s = `<path d="${band(1.5)}" fill="${P.litter[1]}" opacity=".6"/>`;
    s += `<path id="${id}-clear" d="${band(1)}" fill="url(#waterg)"/>`;
    s += `<path id="${id}-mud" d="${band(1)}" fill="url(#mudw)" opacity="0"/>`;
    s += `<path id="${id}-flood" d="${band(2.1)}" fill="url(#mudw)" opacity="0"/>`;
    for (let k = 0; k < 26; k++) {
      const seg = Math.floor(r() * (pts.length - 1)), t = r(), [x0, y0] = pts[seg], [x1, y1] = pts[seg + 1];
      const x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t + (r() - 0.5) * width(seg) * 0.6;
      s += `<path class="rip" d="M${f1(x - 18)},${f1(y)}q18,-7 36,0" stroke="#e8f2ec" stroke-width="3" fill="none" opacity=".6" stroke-linecap="round"/>`;
    }
    pts.forEach(([x, y], k) => { if (k) s += `<ellipse cx="${x - 30}" cy="${y - width(k) * 0.55}" rx="${30 + k * 6}" ry="${14 + k * 3}" fill="${P.rock}"/><ellipse cx="${x - 36}" cy="${y - width(k) * 0.55 - 6}" rx="${12 + k * 2}" ry="4" fill="#dfe8e2" opacity=".35"/>`; });
    return s;
  }

  // two dome tents, a hammock slung between trees, a lantern; optional single-foot prints
  function camp(id, G, P, o) {
    const night = P === NIGHT;
    const tent = (x, col, sh, door) => `<g transform="translate(${x},${G + 20})"><path d="M-190,0Q-170,-230 0,-250Q170,-230 190,0Z" fill="${col}" ${OUT}/>
      <path d="M0,-250Q70,-230 190,0H80Q60,-140 0,-250Z" fill="${sh}" opacity=".55"/><path d="M-120,-170Q0,-120 120,-170M-160,-80Q0,-30 160,-80" stroke="${sh}" stroke-width="4" fill="none" opacity=".6"/>
      <path d="M-62,0Q-44,-140 0,-160Q44,-140 62,0Z" fill="${door}" ${OUT}/><path d="M-190,0l-46,16M190,0l46,16" stroke="${INK}" stroke-width="3"/></g>`;
    let s = tent(o.tentA ?? 340, night ? "#5a3a2a" : "#d9733f", night ? "#3a2418" : "#a9542f", night ? "#160d09" : "#3a2418");
    s += tent(o.tentB ?? 760, night ? "#26364a" : "#4f7fb0", night ? "#172231" : "#365d86", night ? "#0b111a" : "#1d2f45");
    // hammock between the giant tree and a pole tree on the right
    const hx0 = o.hamX0 ?? 860, hx1 = o.hamX1 ?? 1220, hy = G - 360;
    s += trunk(hx1 + 30, G + 20, -400, 60, P.trunk, P.bark, mk(3));
    s += `<g id="${id}-ham" class="hammock"><path d="M${hx0},${hy}L${hx0 + 60},${hy + 70}M${hx1},${hy}L${hx1 - 60},${hy + 70}" stroke="#c9bfa8" stroke-width="4"/>
      <path d="M${hx0 + 60},${hy + 70}Q${(hx0 + hx1) / 2},${hy + 230} ${hx1 - 60},${hy + 70}Q${(hx0 + hx1) / 2},${hy + 150} ${hx0 + 60},${hy + 70}Z" fill="${night ? "#3d4a34" : "#6f8a4f"}" ${OUT}/>
      ${o.hammock === "occupied" ? `<path d="M${hx0 + 110},${hy + 110}Q${(hx0 + hx1) / 2},${hy + 120} ${hx1 - 110},${hy + 100}Q${(hx0 + hx1) / 2},${hy + 190} ${hx0 + 110},${hy + 110}Z" fill="${night ? "#2a3324" : "#566d3c"}"/><ellipse cx="${hx1 - 110}" cy="${hy + 96}" rx="26" ry="20" fill="${night ? "#efece2" : "#f0ece2"}" opacity=".85"/>` : ""}
      <path d="M${hx0 + 60},${hy + 70}Q${(hx0 + hx1) / 2},${hy + 150} ${hx1 - 60},${hy + 70}" stroke="${INK}" stroke-width="3" fill="none" opacity=".6"/></g>`;
    s += `<g transform="translate(${o.lanternX ?? 600},${G - 330})"><path d="M0,-80V-10" stroke="${INK}" stroke-width="3"/><rect x="-16" y="-12" width="32" height="44" rx="8" fill="${night ? "#ffcf7a" : "#e8dcc0"}" ${OUT}/></g>`;
    if (o.prints) s += prints(G, o.prints);
    return s;
  }
  function footPrint(x, y, ang, s, fill) { // human-ish, but the toes are too long and clawed (always the same foot)
    return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(ang)}) scale(${s})" fill="${fill}">
      <path d="M2,72C-20,72 -28,54 -24,30C-20,8 -30,-14 -26,-36C-20,-60 20,-64 30,-44C38,-26 26,-6 22,16C18,42 26,72 2,72Z"/>
      ${[[-20, -86, 10, 20, -10], [-2, -94, 8, 17, -3], [14, -90, 7, 15, 5], [27, -80, 6, 13, 13], [37, -66, 5, 11, 22]].map(([a, b, rx, ry, rot]) => `<ellipse cx="${a}" cy="${b}" rx="${rx}" ry="${ry}" transform="rotate(${rot} ${a} ${b})"/><path d="M${a + rot * 0.2},${b - ry + 2}l${f1(rot / 5)},-14" stroke="${fill}" stroke-width="3.5" stroke-linecap="round"/>`).join("")}</g>`;
  }
  function prints(G, opt) {
    let s = "";
    const n = opt.n || 9;
    for (let k = 0; k < n; k++) s += footPrint(opt.x0 + k * opt.dx, G + 80 + Math.sin(k * 0.9) * 26, opt.ang || 90, opt.s || 0.7, "#070b09");
    return s;
  }

  // ---------------- aerial canopy (day, top-down) with a winding trail and three hikers ----------------
  function canopyAerial(L, o = {}) {
    const r = mk(o.seed || 21);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#2b4436"/>`);
    let far = "";
    for (let i = 0; i < 160; i++) far += clump(r, -600 + r() * 2300, -400 + r() * 2800, 120 + r() * 80, ["#3e5f48", "#4a6e52", "#355540"][i % 3], "#2d4838", "#6e9668");
    put(L.far, far);
    const trail = `M380,-500C520,0 300,400 520,800S760,1300 560,1700S420,2200 600,2600`;
    let mid = `<path d="${trail}" stroke="#6b5c44" stroke-width="70" fill="none" stroke-linecap="round"/><path d="${trail}" stroke="#87745a" stroke-width="40" fill="none" stroke-linecap="round" opacity=".7"/>`;
    const hik = [["#e8b830", 0], ["#34506e", 70], ["#3e5a44", 140]];
    mid += hik.map(([c, dy], k) => `<g transform="translate(${505 + k * 10},${790 + dy})"><ellipse cx="0" cy="6" rx="16" ry="9" fill="#1c2a22" opacity=".5"/><circle r="14" fill="${c}" ${OUT}/><circle cy="-2" r="6" fill="${k === 2 ? "#f0ece2" : "#2b2522"}"/></g>`).join("");
    for (let i = 0; i < 70; i++) {
      const x = -600 + r() * 2300, y = -400 + r() * 2800;
      if (Math.abs(x - 520) < 160 && y > 500 && y < 1100) continue;
      mid += clump(r, x, y, 90 + r() * 70, ["#4f7653", "#5c855c", "#466b4b"][i % 3], "#3a5a40", "#8db37e");
    }
    put(L.mid, mid);
    put(L.fg, mist(-200, 900, "url(#mistg)", 0.9) + mist(1300, 900, "url(#mistg)", 0.8));
  }

  // ---------------- aerial camp (night, top-down): tents, hammock, single footprints all round ----------------
  function aerialCamp(L, o = {}) {
    const r = mk(o.seed || 41);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0e1513"/>`);
    let s = "";
    for (let i = 0; i < 500; i++) s += `<ellipse cx="${f1(-600 + r() * 2300)}" cy="${f1(-400 + r() * 2800)}" rx="${f1(5 + r() * 12)}" ry="${f1(3 + r() * 5)}" fill="${NIGHT.litter[i % 4]}"/>`;
    for (let i = 0; i < 16; i++) s += `<circle cx="${f1(-300 + r() * 1700)}" cy="${f1(-200 + r() * 2300)}" r="${f1(30 + r() * 50)}" fill="#0a100e" ${OUT}/>`;
    const tentTop = (x, y, c, sh) => `<g transform="translate(${x},${y})"><path d="M0,-150L60,-120H-60Z" fill="${sh}" ${OUT}/><path d="M-140,0C-140,-92 -92,-132 0,-132C92,-132 140,-92 140,0C140,92 92,132 0,132C-92,132 -140,92 -140,0Z" fill="${c}" ${OUT}/>
      <path d="M-98,-94C-30,-30 30,30 98,94M98,-94C30,-30 -30,30 -98,94" stroke="${sh}" stroke-width="7" fill="none"/><path d="M-140,0C-60,20 60,20 140,0" stroke="#000" stroke-width="3" fill="none" opacity=".3"/></g>`;
    s += tentTop(400, 900, "#5a3a26", "#3a2418") + tentTop(720, 1140, "#24364a", "#172231");
    s += `<g transform="translate(560,1420) rotate(-12)"><rect x="-210" y="-36" width="420" height="72" rx="36" fill="#2d3826" ${OUT}/><path d="M-260,0H-210M210,0H260" stroke="#c9bfa8" stroke-width="5"/></g>`;
    s += `<circle cx="300" cy="1420" r="44" fill="#121a17" ${OUT}/><circle cx="830" cy="1300" r="40" fill="#121a17" ${OUT}/>`;
    // hopping ring of single prints round the tents
    const n = 15;
    for (let k = 0; k < n; k++) {
      const a = (k / n) * Math.PI * 2, x = 560 + Math.cos(a) * 390, y = 1060 + Math.sin(a) * 560;
      s += `<g class="pr" data-i="${k}">${footPrint(x, y, (a * 180) / Math.PI + 180, 1.0, "#030504")}</g>`;
    }
    put(L.set, s);
    put(L.glow, `<circle cx="560" cy="1000" r="560" fill="url(#torchpool)" opacity=".7"/>`);
  }

  // ---------------- watershed cross-section (diagram) ----------------
  function xsection(L, o = {}) {
    const id = o.id || "xs";
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="url(#diagBg)"/>` +
      Array.from({ length: 16 }, (_, k) => `<path d="M-900,${k * 140}H2000" stroke="#22363d" stroke-width="2"/>`).join(""));
    const ridge = "M-300,2600L-300,620C-100,560 40,420 200,360C320,330 380,420 470,560C560,700 640,900 760,1080C840,1190 920,1300 1100,1330L1400,1340V2600Z";
    let s = `<path d="${ridge}" fill="#2b3f3a" stroke="#cfc4a8" stroke-width="5"/>`;
    s += [[-120, 560], [40, 440], [330, 400], [430, 520], [560, 700], [660, 860]].map(([x, y]) => `<path d="M${x},${y}l-18,0l18,-70l18,70z" fill="#4f6b5c" stroke="#cfc4a8" stroke-width="3"/>`).join("");
    s += [0, 1, 2].map((k) => `<path d="M-300,${1500 + k * 60}C200,${1380 + k * 70} 700,${1480 + k * 50} 1400,${1450 + k * 70}" stroke="#3f5650" stroke-width="18" fill="none" opacity=".6"/>`).join("");
    const ch = "M230,380C300,470 360,560 430,640C520,760 600,900 700,1040C780,1150 860,1250 960,1310";
    s += `<path d="${ch}" stroke="#7fb3ab" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    s += `<path id="${id}-wave" d="${ch}" stroke="#9c7d55" stroke-width="34" fill="none" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400"/>`;
    s += `<g transform="translate(960,1300)"><path d="M-60,0Q-52,-70 0,-76Q52,-70 60,0Z" fill="#d9733f" stroke="#cfc4a8" stroke-width="4"/><path d="M-18,0Q-12,-40 0,-46Q12,-40 18,0Z" fill="#3a2418"/></g>`;
    s += `<g id="${id}-cloud" transform="translate(240,250)"><path d="M-170,30a60,60 0 0 1 40,-100a90,90 0 0 1 160,-20a70,70 0 0 1 120,40a56,56 0 0 1 -10,110H-150a50,50 0 0 1 -20,-30z" fill="#7d8f96" stroke="#cfc4a8" stroke-width="5"/>
      <g id="${id}-rain">${Array.from({ length: 16 }, (_, k) => `<path d="M${-150 + k * 20},${100 + (k % 3) * 18}l-12,46" stroke="#9fc6d6" stroke-width="5" stroke-linecap="round"/>`).join("")}</g></g>`;
    s += `<g transform="translate(960,1100)"><circle r="36" fill="#f2c55c" opacity=".9"/>${Array.from({ length: 8 }, (_, k) => `<path d="M0,-50V-66" stroke="#f2c55c" stroke-width="6" stroke-linecap="round" transform="rotate(${k * 45})"/>`).join("")}</g>`;
    const tag = (x, y, t, c) => `<g transform="translate(${x},${y})"><rect x="${-t.length * 13}" y="-34" width="${t.length * 26}" height="56" rx="12" fill="#0d171b" stroke="${c}" stroke-width="4"/><text y="6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="34" fill="${c}">${t}</text></g>`;
    s += `<g id="${id}-tags">${tag(250, 150, "ฝนตกบนเขา", "#9fc6d6")}${tag(880, 1450, "ริมลำธาร", "#f2c55c")}${tag(960, 1000, "ไม่มีฝน", "#f2c55c")}</g>`;
    put(L.set, s);
  }

  // ---------------- สมุดข่อย legend panels (cream ink on black paper), stacked for camera cuts ----------------
  function legendInk(L, o = {}) {
    const r = mk(o.seed || 9), C = "#e9dcbd", G = "#c9a55a";
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="3400" fill="url(#paperK)"/>` +
      Array.from({ length: 9 }, (_, k) => `<path d="M-900,${-200 + k * 420}H2000" stroke="#000" stroke-width="10" opacity=".6"/><path d="M-900,${-194 + k * 420}H2000" stroke="#2b2620" stroke-width="2"/>`).join("") +
      Array.from({ length: 400 }, () => `<circle cx="${f1(-200 + r() * 1500)}" cy="${f1(-300 + r() * 3200)}" r="${f1(0.6 + r() * 1.6)}" fill="#3a332b" opacity=".6"/>`).join(""));
    const tree = (x, base, h, s) => `<g transform="translate(${x},${base}) scale(${s})" stroke="${C}" stroke-width="4" fill="none" stroke-linecap="round">
      <path d="M-14,0C-10,-${h * 0.5} -20,-${h * 0.8} 0,-${h}M14,0C10,-${h * 0.5} 20,-${h * 0.8} 0,-${h}"/>
      ${[0.35, 0.55, 0.75].map((k, i) => `<path d="M0,-${h * k}c${i % 2 ? 60 : -60},-30 ${i % 2 ? 110 : -110},-10 ${i % 2 ? 120 : -120},-60c0,-30 -30,-40 -40,-20" />`).join("")}
      <path d="M-40,0q-30,10 -50,-6M40,0q30,10 50,-6"/></g>`;
    let s = "";
    // panel 1 (y 0..900): forest at night, the one-legged figure mid-hop
    s += tree(140, 860, 620, 1) + tree(900, 880, 700, 1) + tree(560, 860, 420, 0.8);
    s += `<path d="M60,880H1020" stroke="${C}" stroke-width="3" stroke-dasharray="14 10"/>`;
    s += `<g transform="translate(560,860)">${creatureInk(C)}</g>`;
    s += `<g fill="none" stroke="${G}" stroke-width="3">${[0, 1, 2].map((k) => `<path d="M${520 - k * 50},${880 - k * 6}q-20,-30 -40,0" opacity="${0.9 - k * 0.25}"/>`).join("")}</g>`;
    // panel 2 (y 1000..1500): one leg beside a trunk it cannot climb (scratch marks at the base)
    s += `<g transform="translate(0,0)">${tree(640, 1500, 520, 1.2)}<path d="M560,1480l-10,-60M580,1484l-6,-70M600,1482l-2,-56" stroke="${G}" stroke-width="5" stroke-linecap="round"/>
      <g transform="translate(380,1500) scale(1.5)">${legInk(C)}</g></g>`;
    // panel 3 (y 1560..1960): a sleeper's feet and a long hand reaching for the toes
    s += `<g transform="translate(540,1840)" stroke="${C}" stroke-width="4" fill="none" stroke-linecap="round">
      <path d="M-300,40H260"/><path d="M-260,40c0,-60 40,-80 120,-80h200"/>
      <path d="M60,-40c20,-30 60,-36 80,-10c14,18 6,44 -6,50"/>${[0, 1, 2, 3].map((k) => `<circle cx="${144 + k * 4}" cy="${-30 + k * 14}" r="7"/>`).join("")}
      <path d="M420,-300C340,-240 300,-160 250,-80c-10,14 -6,30 6,34M250,-80l-30,10M250,-80l-8,-30" stroke="${G}" stroke-width="6"/></g>`;
    put(L.set, s);
  }
  function creatureInk(C) {
    return `<g stroke="${C}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M0,0L6,-120L-20,-230"/><path d="M-26,0H34" stroke-width="7"/>
      <path d="M-20,-230C-60,-300 -50,-420 0,-470C30,-440 40,-360 20,-300C10,-270 -4,-250 -20,-230Z" fill="#141210"/>
      <path d="M0,-470c-10,-40 10,-70 34,-70c26,0 36,30 26,60c-6,20 -30,30 -60,10z" fill="#141210"/>
      <path d="M50,-500c30,40 40,110 30,170M40,-490c20,50 20,120 6,180M20,-480c10,60 6,120 -10,170"/>
      <path d="M-30,-420C-90,-380 -110,-300 -100,-200l-10,30M-100,-200l10,26M-100,-200l20,12"/>
      <path d="M30,-400C80,-360 100,-280 90,-180l12,28M90,-180l-8,28M90,-180l-20,16"/>
      <circle cx="16" cy="-500" r="3" fill="${C}"/></g>`;
  }
  function legInk(C) {
    return `<g stroke="${C}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M-14,-300C-20,-200 -6,-120 -16,-40C-20,-10 -30,0 -60,4M14,-300C20,-200 30,-120 20,-40"/>
      <path d="M20,-40C40,-10 70,0 110,4"/><path d="M-60,4H110"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M${50 + k * 14},4l${8 + k},-6"/>`).join("")}</g>`;
  }

  // ---------------- EP.2: up the giant tree — a branch to sit on, the flood below, dawn after ----------------
  // the ground sits low (o.ground ~2350) so the branch (o.branchY) is well above it; flood water is id-flood
  function treeNight(L, o = {}) {
    const id = o.id || "tn", dawn = o.time === "dawn", P = dawn ? DAY : NIGHT, G = o.ground ?? 2350, by = o.branchY ?? 1400, r = mk(o.seed || 51);
    const tx = o.treeX ?? (o.flip ? 960 : 120), tw = 300, rimC = dawn ? "#a9bfae" : "#4f7470";
    rainforest(L, { seed: o.seed || 51, time: dawn ? "day" : "night", ground: G, treeX: tx, treeW: tw, tree2X: o.tree2X ?? (o.flip ? -200 : 1250), fg: false, id });
    if (dawn) put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="url(#dawnsky)" opacity=".55"/>`);
    // moonlight on the inner edge of the trunk so it reads against the dark forest
    const ex = o.flip ? tx - tw / 2 : tx + tw / 2, d = o.flip ? 1 : -1;
    const lit = dawn ? ["#3a4238", "#5d6a5c"] : ["#0b1210", "#2b3c36"], bark = dawn ? "#2b322b" : "#070b0a";
    let tr = `<linearGradient id="${id}-trg" x1="${o.flip ? 1 : 0}" x2="${o.flip ? 0 : 1}"><stop offset="0" stop-color="${lit[0]}"/><stop offset=".7" stop-color="${lit[1]}"/><stop offset="1" stop-color="${lit[0]}"/></linearGradient>
      <path d="M${tx - tw / 2},${G + 30}C${tx - tw * 0.46},${G - 470} ${tx - tw * 0.4},-300 ${tx - tw * 0.36},-600H${tx + tw * 0.36}C${tx + tw * 0.4},-300 ${tx + tw * 0.46},${G - 470} ${tx + tw / 2},${G + 30}Z" fill="url(#${id}-trg)"/>`;
    for (let k = 0; k < 9; k++) { const bx = tx - tw * 0.4 + k * tw * 0.1; tr += `<path d="M${f1(bx)},${G}C${f1(bx + (r() - 0.5) * 24)},${G - 700} ${f1(bx + (r() - 0.5) * 24)},400 ${f1(bx * 0.97 + tx * 0.03)},-600" stroke="${bark}" stroke-width="${f1(4 + r() * 5)}" fill="none" opacity=".55"/>`; }
    for (let k = 0; k < 8; k++) tr += `<ellipse cx="${f1(tx - tw * 0.3 + r() * tw * 0.6)}" cy="${f1(G - 200 - r() * 1700)}" rx="${f1(12 + r() * 22)}" ry="${f1(26 + r() * 50)}" fill="${P.moss}" opacity=".6"/>`;
    tr += `<path d="M${ex + d * 6},${G + 30}C${ex + d * 0.06 * tw},${G - 470} ${ex + d * 0.12 * tw},-300 ${ex + d * 0.16 * tw},-600" stroke="${rimC}" stroke-width="7" fill="none" opacity="${dawn ? 0.25 : 0.4}"/>`;
    put(L.set, tr);
    let b = `<g id="${id}-branch"${o.flip ? ' transform="translate(1080,0) scale(-1,1)"' : ""}><path d="M40,${by - 70}C320,${by - 96} 760,${by - 64} 1320,${by - 12}L1320,${by + 26}C760,${by + 12} 320,${by + 34} 40,${by + 80}Z" fill="${P.trunk}" ${OUT}/>`;
    b += `<path d="M60,${by - 66}C320,${by - 92} 760,${by - 60} 1320,${by - 8}" stroke="${rimC}" stroke-width="7" fill="none" opacity="${dawn ? 0.3 : 0.55}"/>`;
    for (let k = 0; k < 6; k++) b += `<path d="M${80 + k * 200},${by - 60 + k * 9}q90,${-6 + k} 180,4" stroke="${P.bark}" stroke-width="5" fill="none" opacity=".6"/>`;
    for (let k = 0; k < 7; k++) b += `<ellipse cx="${120 + r() * 1000}" cy="${by - 62 + r() * 20}" rx="${30 + r() * 40}" ry="10" fill="${P.moss}" opacity=".7"/>`;
    b += [[520, -1], [980, 1]].map(([x, d]) => `<path d="M${x},${by - 50}q${d * 60},-120 ${d * 150},-180" stroke="${P.trunk}" stroke-width="22" fill="none" stroke-linecap="round"/>${clump(r, x + d * 160, by - 250, 90, P.set[0], P.set[1], dawn ? P.hi : null)}`).join("");
    put(L.set, b + `</g>`);
    // flash flood: a muddy sheet with a foam crest at its leading (right) edge. Slide the group in with x
    // (-2900 → 0); ${id}-floodF is the same water in front of anything standing in it (append it to act last)
    const W = G - 260;
    let wave = `M-3000,${W}`;
    for (let x = -3000; x <= 2000; x += 60) wave += `L${x},${f1(W + 9 * Math.sin(x / 70) + 5 * Math.sin(x / 23))}`;
    const streaks = (n, y0, h, op) => Array.from({ length: n }, () => { const y = y0 + r() * h, x = -2900 + r() * 4800; return `<path class="foam" d="M${f1(x)},${f1(y)}h${f1(90 + r() * 260)}" stroke="#e8e2d2" stroke-width="${f1(3 + r() * 6)}" stroke-linecap="round" stroke-dasharray="${f1(40 + r() * 40)} 34" opacity="${op}"/>`; }).join("");
    let f = `<g id="${id}-flood" opacity="0"><rect x="-3000" y="${W}" width="5000" height="1200" fill="url(#floodw)"/>
      <path d="${wave}" stroke="#d9d2bf" stroke-width="10" fill="none" opacity=".7"/>${streaks(70, W + 20, 620, 0.55)}`;
    f += Array.from({ length: 10 }, (_, k) => `<g class="deb" transform="translate(${-2600 + k * 450},${W + 60 + (k % 3) * 150}) rotate(${(k % 2 ? 1 : -1) * (6 + k)})"><rect x="-110" y="-14" width="220" height="28" rx="14" fill="#2a1d12" ${OUT}/><path d="M60,-12l40,-34M-40,-10l-20,-30" stroke="#2a1d12" stroke-width="9" stroke-linecap="round"/></g>`).join("");
    f += `<g><path d="M1860,${W + 4}C1960,${W - 60} 2020,${W - 190} 2120,${W - 160}C2200,${W - 130} 2190,${W + 60} 2150,${W + 300}L2120,${W + 1200}H1860Z" fill="#e2dccb" opacity=".9"/>
      ${Array.from({ length: 16 }, () => `<circle cx="${f1(1900 + r() * 260)}" cy="${f1(W - 230 + r() * 260)}" r="${f1(6 + r() * 16)}" fill="#ece6d6" opacity="${f1(0.4 + r() * 0.4)}"/>`).join("")}</g>`;
    put(L.set, f + `</g>`);
    put(L.act, `<g id="${id}-floodF" opacity="0"><rect x="-3000" y="${G - 50}" width="5000" height="900" fill="url(#floodwF)"/>${streaks(24, G - 20, 300, 0.45)}</g>`);
    if (dawn) put(L.light, [0, 1].map((k) => `<path class="shaft" d="M${300 + k * 340},-100L${420 + k * 340},-100L${700 + k * 300},2000L${520 + k * 300},2000Z" fill="url(#shaftg)" opacity=".7"/>`).join(""));
  }
  // the kong koi perched on a branch: hunched, one leg dangling (origin = where it sits)
  function koiSit(id, x, y, s, o = {}) {
    const c = o.col || "#030504", rim = o.rim || "#22312d";
    const R = `stroke="${rim}" stroke-width="2.5" stroke-linejoin="round"`;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><g id="${id}-body">
      <path d="M-10,0C10,30 30,80 26,160C24,200 30,240 36,270L18,274C10,240 4,200 2,160C0,100 -20,40 -30,10Z" fill="${c}" ${R}/>
      <path d="M18,270C30,286 70,290 96,292C104,300 96,306 86,304L22,296Z" fill="${c}" ${R}/>
      <path d="M-46,10C-66,-60 -56,-150 -10,-206C20,-236 70,-226 78,-186C84,-146 54,-104 32,-52C22,-22 16,-4 12,8Z" fill="${c}" ${R}/>
      <path d="M52,-200C62,-242 102,-252 120,-224C132,-202 124,-168 102,-158C82,-150 58,-166 52,-200Z" fill="${c}" ${R}/>
      ${o.eyes ? `<g class="koieyes"><circle cx="94" cy="-198" r="11" fill="#e9ffc0" opacity=".3"/><circle cx="110" cy="-194" r="11" fill="#e9ffc0" opacity=".3"/><circle cx="94" cy="-198" r="4" fill="#f4ffe0"/><circle cx="110" cy="-194" r="4" fill="#f4ffe0"/></g>` : ""}
      <path d="M62,-226C52,-166 58,-90 50,-10M80,-236C78,-166 88,-90 82,0M100,-236C106,-176 116,-96 110,-20M118,-220C132,-166 136,-106 128,-36" stroke="${c}" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M34,-174C60,-120 76,-40 80,60M80,60l8,46M80,60l-2,50M80,60l-14,42" stroke="${c}" stroke-width="15" fill="none" stroke-linecap="round"/></g></g>`;
  }
  // yellow rain poncho pulled over two people sitting close: (x, y) = between them at neck height.
  // ponchoBack (the hood behind their heads) goes in the set layer, poncho (the front drape) over the actors.
  function ponchoBack(id, x, y, s) {
    return `<g id="${id}-bk" transform="translate(${x},${y}) scale(${s})"><path d="M-180,40C-200,-60 -160,-150 -70,-172C-25,-182 25,-182 70,-172C160,-150 200,-60 180,40Z" fill="#d8a828" ${OUT}/>
      <path d="M-150,10C-160,-60 -130,-120 -60,-140M150,10C160,-60 130,-120 60,-140" stroke="#a97f18" stroke-width="8" fill="none" opacity=".7"/></g>`;
  }
  function poncho(id, x, y, s) {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-182,12C-120,-14 -60,4 0,-4C60,4 120,-14 182,12L212,196C130,222 -130,222 -212,196Z" fill="#e8b830" ${OUT}/>
      <path d="M-150,40C-140,90 -160,140 -176,190M0,10C-6,80 6,140 0,210M140,40C150,100 150,150 176,192" stroke="#c4931c" stroke-width="8" fill="none" opacity=".75"/>
      <path d="M-170,20C-110,2 -60,14 -10,8" stroke="#ffe08a" stroke-width="6" fill="none" opacity=".6"/>
      ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${-180 + k * 60},${206 + (k % 2) * 6}l-4,${22 + (k % 3) * 12}" stroke="#d9e6e8" stroke-width="5" stroke-linecap="round" opacity=".7"/>`).join("")}</g>`;
  }

  // ---------------- หนังตะลุง: the legend told with shadow puppets on three lit screens ----------------
  // screens centred at y 450, 1340, 2020; puppets jiggle (class pup) and the lamps flicker (class lamp)
  function legendShadow(L, o = {}) {
    const P = "#170d06", CUT = "#ffd9a0", ROD = "#3a2414";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3600" fill="#1c1009"/>`);
    let s = "";
    const screen = (y0, y1, cy) => `<rect x="-40" y="${y0}" width="1160" height="${y1 - y0}" fill="#e9a457"/>
      <circle class="lamp" cx="540" cy="${cy}" r="${(y1 - y0) * 0.9}" fill="url(#clothglow)"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-40 + k * 40},${y0}V${y1}" stroke="#c98a44" stroke-width="1.5" opacity=".25"/>`).join("")}
      <path d="M-40,${y0}H1120" stroke="${P}" stroke-width="18"/><path d="M-40,${y1}H1120" stroke="${P}" stroke-width="18"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y0 + 8}l21,26l21,-26`).join("")}" fill="${P}"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y1 - 8}l21,-26l21,26`).join("")}" fill="${P}"/>`;
    s += screen(-20, 960, 450) + screen(1040, 1660, 1350) + screen(1740, 2360, 2050);
    const tree = (x, base, h, flip) => `<g class="pup" data-ox="${x}" data-oy="${base}"><path d="M${x},${base + 200}V${base}" stroke="${ROD}" stroke-width="6"/>
      <g transform="translate(${x},${base}) scale(${flip ? -1 : 1},1)"><path d="M0,0C-120,-${h * 0.2} -150,-${h * 0.55} -60,-${h * 0.8}C-30,-${h * 0.9} -10,-${h * 0.96} 0,-${h}C10,-${h * 0.96} 30,-${h * 0.9} 60,-${h * 0.8}C150,-${h * 0.55} 120,-${h * 0.2} 0,0Z" fill="${P}"/>
      ${[0.2, 0.36, 0.52, 0.68].map((k, i) => `<path d="M${i % 2 ? 10 : -10},-${h * k}c${i % 2 ? 40 : -40},-20 ${i % 2 ? 70 : -70},-50 ${i % 2 ? 50 : -50},-80c-14,-20 -36,-10 -30,8" stroke="${CUT}" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}
      ${[0.28, 0.44, 0.6, 0.76].map((k) => `<ellipse cx="0" cy="-${h * k}" rx="8" ry="14" fill="${CUT}"/>`).join("")}<path d="M0,-${h * 0.1}V-${h * 0.9}" stroke="${CUT}" stroke-width="3"/></g></g>`;
    // the kong koi puppet with lace cut-outs and hand rods
    const pup = (x, y, sc, rot, id) => `<g class="pup" data-ox="${x}" data-oy="${y}"><g transform="translate(${x},${y}) rotate(${rot}) scale(${sc})">
      <path d="M0,-300V260M106,-200L190,260" stroke="${ROD}" stroke-width="${5 / sc}"/>
      ${koi(id, 0, 0, 1, { col: P, rim: P, rimW: 0 })}
      <g fill="${CUT}">${[[-10, -470, 6, 11], [6, -440, 7, 12], [20, -404, 6, 11], [-14, -400, 5, 9], [0, -360, 6, 10], [-4, -250, 4, 8], [12, -200, 4, 8], [20, -150, 4, 8]].map(([a, b, rx, ry]) => `<ellipse cx="${a}" cy="${b}" rx="${rx}" ry="${ry}"/>`).join("")}
        <circle cx="104" cy="-498" r="5"/><circle cx="120" cy="-494" r="5"/></g>
      <path d="M-20,-470c20,-14 46,-10 60,4M-24,-330c20,10 40,10 56,0" stroke="${CUT}" stroke-width="4" fill="none"/></g></g>`;
    s += tree(170, 900, 760) + tree(930, 900, 820, true) + pup(560, 880, 1.25, 0, "lgk1");
    // screen 2: the one leg, and a trunk it cannot climb (claw marks at the base)
    s += `<g class="pup" data-ox="760" data-oy="1640"><path d="M690,1640V1080H830V1640Z" fill="${P}"/><path d="M700,1260C740,1240 790,1250 820,1270M700,1400C740,1380 790,1390 820,1410" stroke="${CUT}" stroke-width="5" fill="none"/>
      <path d="M716,1630l-8,-110M740,1634l-4,-130M764,1632l0,-116M788,1630l4,-104" stroke="${CUT}" stroke-width="7" stroke-linecap="round"/></g>`;
    s += `<g class="pup" data-ox="330" data-oy="1640"><g transform="translate(330,1640) scale(1.9)"><path d="M-26,-300C-34,-240 -10,-190 14,-150C26,-120 14,-70 6,-24L24,-20C36,-70 48,-130 36,-162C22,-200 16,-250 24,-300Z" fill="${P}"/>
      <path d="M-6,-30C-22,-10 -18,4 10,6L104,10C118,10 120,0 106,-6L72,-16C52,-22 32,-32 24,-38Z" fill="${P}"/><path d="M104,10l18,4M100,-2l20,-2M92,-10l16,-8" stroke="${P}" stroke-width="5" stroke-linecap="round"/>
      ${[[-4, -250], [10, -200], [18, -110], [12, -60]].map(([a, b]) => `<ellipse cx="${a}" cy="${b}" rx="4" ry="9" fill="${CUT}"/>`).join("")}<path d="M0,-300V-340" stroke="${ROD}" stroke-width="4"/></g></g>`;
    // screen 3: a sleeper's feet, and the koi bending over his toes
    s += `<g class="pup" data-ox="380" data-oy="2280"><path d="M60,2300C60,2240 120,2210 220,2210H560C600,2210 640,2230 650,2260L660,2300Z" fill="${P}"/>
      <path d="M560,2210C580,2160 620,2150 640,2170C660,2190 656,2230 640,2250" fill="${P}"/>${[0, 1, 2, 3, 4].map((k) => `<circle cx="${648 + k * 3}" cy="${2178 + k * 13}" r="${10 - k}" fill="${P}"/>`).join("")}
      <ellipse cx="110" cy="2200" rx="60" ry="46" fill="${P}"/><path d="M200,2260H520" stroke="${CUT}" stroke-width="4"/></g>`;
    s += pup(880, 2330, 1.0, -28, "lgk3");
    put(L.set, s);
  }

  // ---------------- stream close-up: clear → muddy → rising → the surge from upstream ----------------
  function streamClose(L, o = {}) {
    const id = o.id || "sc", r = mk(o.seed || 31), P = DAY;
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="${P.sky}"/>`);
    let far = "";
    for (let i = 0; i < 14; i++) far += trunk(-700 + i * 190 + r() * 60, 980, -300, 34 + r() * 26, P.far[1], null, r);
    for (let x = -800; x < 1900; x += 120) far += clump(r, x, 120 + r() * 300, 170, P.far[0], P.far[2]);
    put(L.far, far + mist(500, 600, P.mist, 1));
    let mid = `<path d="M-900,960C-300,930 300,990 900,950S1600,960 2000,950V1060H-900Z" fill="${P.ground}"/>`;
    for (let x = -800; x < 1900; x += 130) mid += fernBush(x + r() * 60, 990, 0.9, P.set[0], P.set[2], r);
    mid += `<path d="M-200,1000C-150,960 -60,980 0,1020M300,1000c40,-40 120,-30 160,10" stroke="#3a3127" stroke-width="16" fill="none" stroke-linecap="round"/>`;
    put(L.mid, mid);
    let s = `<rect x="-900" y="1000" width="2900" height="640" fill="url(#waterg)" id="${id}-clear"/>`;
    for (let i = 0; i < 70; i++) s += `<ellipse cx="${f1(-600 + r() * 2300)}" cy="${f1(1040 + r() * 560)}" rx="${f1(10 + r() * 22)}" ry="${f1(5 + r() * 9)}" fill="#c9d8cc" opacity=".35"/>`;
    s += `<rect x="-900" y="1000" width="2900" height="640" fill="url(#mudw)" id="${id}-mud" opacity="0"/>`;
    s += [[260, 1250, 90], [820, 1180, 70], [-80, 1330, 110]].map(([x, y, w]) => `<ellipse cx="${x}" cy="${y}" rx="${w}" ry="${w * 0.45}" fill="${P.rock}"/><ellipse cx="${x - w * 0.2}" cy="${y - w * 0.2}" rx="${w * 0.4}" ry="${w * 0.12}" fill="#dfe8e2" opacity=".35"/>`).join("");
    s += `<g id="${id}-pole"><rect x="622" y="820" width="36" height="820" rx="10" fill="#b9a46a" ${OUT}/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M622,${900 + k * 90}h36" stroke="${INK}" stroke-width="5"/><text x="672" y="${912 + k * 90}" font-family="Kanit" font-weight="900" font-size="30" fill="#f4ecd8" stroke="${INK}" stroke-width="5" paint-order="stroke">${5 - k}</text>`).join("")}</g>`;
    s += `<rect id="${id}-flood" x="-900" y="1000" width="2900" height="640" fill="url(#mudw)" opacity="0"/>`;
    s += `<g id="${id}-foam">${Array.from({ length: 26 }, () => { const y = 1030 + r() * 580, x = -600 + r() * 2100; return `<path class="foam" d="M${f1(x)},${f1(y)}h${f1(80 + r() * 160)}" stroke="#eef4ee" stroke-width="${f1(3 + r() * 4)}" stroke-linecap="round" stroke-dasharray="40 30" opacity=".55"/>`; }).join("")}</g>`;
    s += `<g id="${id}-deb">${Array.from({ length: 7 }, (_, k) => `<g class="deb" data-i="${k}" transform="translate(${-400 + k * 260},${1080 + (k % 3) * 120})"><path d="M0,0l60,-8" stroke="#5a4636" stroke-width="9" stroke-linecap="round"/><ellipse cx="20" cy="10" rx="18" ry="7" fill="#5f8f5a"/></g>`).join("")}</g>`;
    s += `<g id="${id}-surge" transform="translate(-1400,0)"><path d="M-1300,700H120C230,690 320,740 330,820C340,900 300,960 340,1040C380,1140 330,1260 360,1360C380,1460 340,1560 360,1660H-1300Z" fill="#4e3a26"/>
      <path d="M-1300,760H60C150,760 220,800 230,860C240,940 210,1010 240,1090C270,1180 230,1290 250,1390C270,1490 240,1580 250,1660H-1300Z" fill="#6b5236" opacity=".9"/>
      <path d="M120,700C230,690 320,740 330,820C340,900 300,960 340,1040C380,1140 330,1260 360,1360C380,1460 340,1560 360,1660" stroke="#f4f1e6" stroke-width="40" fill="none" stroke-linecap="round" stroke-dasharray="46 22"/>
      ${Array.from({ length: 22 }, () => `<circle cx="${f1(280 + r() * 160)}" cy="${f1(700 + r() * 960)}" r="${f1(10 + r() * 28)}" fill="#f4f1e6" opacity=".9"/>`).join("")}
      <g transform="translate(-160,980) rotate(-24)"><rect x="-220" y="-26" width="440" height="52" rx="26" fill="#3a2a1c" ${OUT}/><circle cx="220" cy="0" r="22" fill="#8a6a46" ${OUT}/></g>
      <g transform="translate(-420,1320) rotate(14)"><rect x="-160" y="-20" width="320" height="40" rx="20" fill="#3a2a1c" ${OUT}/></g></g>`;
    s += `<path d="M-900,1620C-300,1590 300,1660 900,1610S1600,1630 2000,1620V2400H-900Z" fill="${P.ground}"/>`;
    for (let i = 0; i < 120; i++) s += `<ellipse cx="${f1(-700 + r() * 2500)}" cy="${f1(1640 + r() * 500)}" rx="${f1(4 + r() * 12)}" ry="${f1(2 + r() * 5)}" fill="${P.litter[i % 4]}" opacity=".8"/>`;
    for (let x = -600; x < 1800; x += 230) s += fernBush(x + r() * 80, 1690 + r() * 40, 1.1, P.set[0], P.set[2], r);
    put(L.set, s);
    put(L.fg, aloc(-40, 2150, 1.8, 18, P.fg[1], P.fg[2]) + banana(1150, 2150, 1.8, -28, P.fg[1], P.fg[2]));
  }

  // ---------------- close-up: a foot on a sleeping mat; leech between the toes ----------------
  function footClose(L, o = {}) {
    const id = o.id || "fc", r = mk(o.seed || 5);
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="#17202a"/>`);
    let bg = `<rect x="-900" y="-400" width="2900" height="2800" fill="#1d2b3a"/>`;
    for (let k = 0; k < 9; k++) bg += `<path d="M-900,${120 + k * 230}C0,${80 + k * 230} 600,${170 + k * 230} 2000,${110 + k * 230}" stroke="#14202c" stroke-width="16" fill="none"/>`;
    for (let k = 0; k < 7; k++) bg += `<path d="M${-100 + k * 230},-400V2400" stroke="#18242f" stroke-width="6"/>`;
    put(L.far, bg);
    // foot seen from above, toes up the frame
    const toes = [[-150, -500, 64, 86, -10], [-40, -560, 46, 66, -2], [44, -556, 40, 58, 6], [118, -530, 36, 50, 14], [180, -490, 32, 42, 22]];
    let f = `<g id="${id}-foot" transform="translate(${o.x ?? 520},${o.y ?? 1500})">
      <path d="M-230,700C-250,300 -230,-260 -200,-380C-170,-470 -40,-480 60,-470C160,-460 230,-420 240,-330C260,-200 250,300 230,700Z" fill="url(#skin3d)" ${OUT}/>
      <path d="M150,-380C200,-200 210,200 200,700" stroke="#b9845e" stroke-width="22" fill="none" opacity=".5"/>`;
    toes.forEach(([x, y, rx, ry, rot]) => {
      const top = y - ry, bot = y + ry * 0.9;
      f += `<g transform="rotate(${rot} ${x} ${bot})"><path d="M${x - rx},${bot}V${f1(y - ry * 0.25)}Q${x - rx},${top} ${x},${top}Q${x + rx},${top} ${x + rx},${f1(y - ry * 0.25)}V${bot}Z" fill="url(#skin3d)" ${OUT}/>
        <path d="M${f1(x - rx * 0.62)},${f1(y - ry * 0.32)}Q${f1(x - rx * 0.62)},${f1(top + ry * 0.12)} ${x},${f1(top + ry * 0.1)}Q${f1(x + rx * 0.62)},${f1(top + ry * 0.12)} ${f1(x + rx * 0.62)},${f1(y - ry * 0.32)}Q${x},${f1(y - ry * 0.18)} ${f1(x - rx * 0.62)},${f1(y - ry * 0.32)}Z" fill="#f4d9c6" stroke="#b9845e" stroke-width="3"/>
        <path d="M${f1(x - rx * 0.5)},${f1(y + ry * 0.25)}q${f1(rx * 0.5)},6 ${f1(rx)},0" stroke="#b9845e" stroke-width="3" fill="none" opacity=".7"/></g>`;
    });
    // blood between the big and 2nd toe, drips
    f += `<g id="${id}-blood"><path d="M-104,-468C-112,-440 -100,-410 -96,-384" stroke="#8e1b1b" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/>
      <ellipse cx="-80" cy="-430" rx="34" ry="16" fill="#7a1414" opacity=".5"/><path d="M-96,-384c-4,14 -2,26 4,30" stroke="#a52222" stroke-width="10" fill="none" stroke-linecap="round"/></g>
      <g id="${id}-drip"><path d="M-92,-346c-10,16 -10,30 0,34c10,-4 10,-18 0,-34z" fill="#a52222"/></g>`;
    // the leech: segmented, glossy, arched between the toes
    f += `<g id="${id}-leech" transform="translate(-96,-468) scale(.62)"><path d="M-6,0C-40,-30 -40,-110 10,-150C50,-180 96,-160 96,-120C96,-90 70,-80 50,-90C30,-100 30,-60 24,-20C20,4 6,10 -6,0Z" fill="url(#leechg)" stroke="#0e0e08" stroke-width="4"/>
      ${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${-22 + k * 6},${-30 - k * 20}q20,-6 34,${4 + k}" stroke="#1a1a10" stroke-width="3" fill="none" opacity=".7"/>`).join("")}
      <path d="M-14,-40C-20,-80 0,-120 30,-140" stroke="#c8c48a" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>
      <path d="M70,-150q12,-4 20,6" stroke="#e8e2b0" stroke-width="3" fill="none" opacity=".6"/></g></g>`;
    put(L.set, f);
    // reaching hand, sized to the close-up: index finger and thumb about to pinch (screen space, under the POV darkness)
    put(L.light, `<g id="${id}-hand" transform="translate(-520,1260) rotate(-20)">
      <path d="M-560,-120L20,-96L30,104L-560,150Z" fill="#e8b830" ${OUT}/><path d="M-20,-100L-10,100" stroke="#c4931c" stroke-width="16"/>
      <path d="M10,-80C70,-104 170,-110 236,-96C260,-60 262,40 240,84C170,112 70,108 14,88Z" fill="#e2ad85" ${OUT}/>
      <path d="M236,-38C262,-40 270,-14 250,-4C266,6 262,30 240,30C258,40 252,66 230,66" stroke="${INK}" stroke-width="4" fill="#d89f78"/>
      <path d="M214,-96C300,-118 380,-128 430,-122C458,-118 462,-82 434,-76C380,-70 300,-60 236,-44Z" fill="#e2ad85" ${OUT}/>
      <path d="M404,-122C426,-124 446,-118 448,-102C436,-96 420,-96 404,-100Z" fill="#f4d9c6" stroke="#b9845e" stroke-width="3"/>
      <path d="M320,-110q4,16 0,30M270,-102q4,14 0,26" stroke="#b9845e" stroke-width="3.5" fill="none"/>
      <path d="M120,70C190,70 300,40 370,-20C392,-38 420,-20 404,4C360,64 250,116 140,118Z" fill="#e2ad85" ${OUT}/>
      <path d="M368,-20C384,-30 400,-28 404,-12C394,-4 380,-4 368,-10Z" fill="#f4d9c6" stroke="#b9845e" stroke-width="3"/>
      <path d="M60,-60Q120,-30 170,-56" stroke="#c48a64" stroke-width="4" fill="none" opacity=".7"/></g>`);
  }

  // ---------------- close-ups for removing a leech (stacked vignettes, camera cuts between them) ----------------
  function leechHowTo(L, o = {}) {
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="3600" fill="url(#diagBg)"/>`);
    const skin = (y) => `<rect x="-200" y="${y}" width="1480" height="70" fill="#e6b48d"/><rect x="-200" y="${y + 70}" width="1480" height="120" fill="#d08f74"/><rect x="-200" y="${y + 190}" width="1480" height="160" fill="#b56f5c"/>
      <path d="M-200,${y}H1280" stroke="${INK}" stroke-width="5"/>${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${k * 180},${y + 260}q40,-30 80,0t80,0" stroke="#8e4a3e" stroke-width="5" fill="none"/>`).join("")}`;
    let s = "";
    // 1 (y 300..900): pulled hard, the mouthparts stay in the wound
    s += skin(760) + `<g transform="translate(540,760)">
      <path d="M-30,0C-40,-120 -60,-300 -20,-420C0,-470 60,-470 70,-420C90,-300 60,-120 30,0Z" fill="url(#leechg)" stroke="#0e0e08" stroke-width="4"/>
      ${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-40,${-60 - k * 60}q50,-14 90,0" stroke="#1a1a10" stroke-width="3" fill="none" opacity=".7"/>`).join("")}
      <path d="M-140,-640C-90,-560 -50,-480 -26,-430M140,-640C90,-560 50,-490 34,-440" stroke="${INK}" stroke-width="58" fill="none" stroke-linecap="round"/>
      <path d="M-140,-640C-90,-560 -50,-480 -26,-430M140,-640C90,-560 50,-490 34,-440" stroke="#e2ad85" stroke-width="48" fill="none" stroke-linecap="round"/>
      <path d="M0,-560V-700M-26,-670l26,-34 26,34" stroke="#e8443a" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <g id="hw-jaw"><path d="M-30,10l12,40 18,-34 18,34 12,-40" fill="#3b3a22" stroke="#0e0e08" stroke-width="3"/><circle cx="0" cy="40" r="66" fill="none" stroke="#e8443a" stroke-width="8"/></g></g>`;
    // 2 (y 1100..1700): a fingernail slides under the small (mouth) end
    s += skin(1560) + `<g transform="translate(460,1560)">
      <path d="M-260,-6C-200,-60 -60,-70 60,-56C160,-44 240,-30 250,-6Z" fill="url(#leechg)" stroke="#0e0e08" stroke-width="4"/>
      ${[0, 1, 2, 3, 4, 5, 6].map((k) => `<path d="M${-200 + k * 60},-50q8,24 0,44" stroke="#1a1a10" stroke-width="3" fill="none" opacity=".7"/>`).join("")}
      <text x="-250" y="-90" font-family="Kanit" font-weight="900" font-size="34" fill="#f2c55c">ปลายเล็ก = ปาก</text>
      <g id="hw-nail" transform="translate(-520,-40)"><path d="M0,0C80,-70 200,-80 300,-40C330,-28 334,4 300,12C200,30 80,40 0,30Z" fill="#e2ad85" ${OUT}/><path d="M240,-36C280,-30 310,-14 316,2C290,6 260,0 236,-8Z" fill="#f6dccb" stroke="#b9845e" stroke-width="3"/></g>
      <path d="M-160,40H40" stroke="#7fd1b9" stroke-width="8" stroke-linecap="round"/><path d="M20,24l26,16 -26,16" fill="none" stroke="#7fd1b9" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>`;
    // 3 (y 2100..2600): salt and flame, both crossed out
    const no = (x) => `<circle cx="${x}" cy="2340" r="190" fill="none" stroke="#e8443a" stroke-width="16"/><path d="M${x - 134},${2474}L${x + 134},${2206}" stroke="#e8443a" stroke-width="16"/>`;
    s += `<g transform="translate(300,2340)"><rect x="-60" y="-80" width="120" height="170" rx="26" fill="#e8e2d4" ${OUT}/><path d="M-60,-30H60" stroke="${INK}" stroke-width="4"/><path d="M-40,-80c0,-40 80,-40 80,0" fill="#b9c2c6" ${OUT}/>${[-20, 0, 20].map((x) => `<circle cx="${x}" cy="-104" r="5" fill="${INK}"/>`).join("")}<text y="50" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="40" fill="${INK}">เกลือ</text></g>${no(300)}`;
    s += `<g transform="translate(780,2380)"><rect x="-40" y="-20" width="80" height="140" rx="14" fill="#c0603e" ${OUT}/><path d="M0,-30C-40,-80 -20,-140 0,-170C10,-130 50,-110 30,-50C24,-34 12,-28 0,-30Z" fill="#f2c55c" ${OUT}/><path d="M0,-50C-12,-70 -6,-100 2,-114C8,-94 18,-80 10,-58Z" fill="#fff1c4"/></g>${no(780)}`;
    put(L.set, s);
  }

  // ---------------- mud close-up lit by a torch: one print, then another, never a pair ----------------
  function mudPrint(L, o = {}) {
    const r = mk(o.seed || 13);
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="#0b0f0d"/>`);
    let s = `<rect x="-900" y="-400" width="2900" height="2800" fill="#2a241c"/>`;
    for (let i = 0; i < 420; i++) s += `<ellipse cx="${f1(-300 + r() * 1700)}" cy="${f1(-200 + r() * 2300)}" rx="${f1(4 + r() * 16)}" ry="${f1(2 + r() * 7)}" fill="${["#3a3125", "#1f1a14", "#4a3e2d", "#2f3a2a"][i % 4]}" opacity=".9"/>`;
    for (let i = 0; i < 30; i++) s += `<path d="M${f1(-200 + r() * 1500)},${f1(-100 + r() * 2100)}q${f1(10 + r() * 20)},-${f1(4 + r() * 8)} ${f1(30 + r() * 30)},0" stroke="#b9c8c0" stroke-width="2" fill="none" opacity=".25"/>`;
    s += `<g opacity=".95">${footPrint(560, 1150, 0, 3.2, "#120f0b")}${footPrint(600, 450, 6, 3.0, "#120f0b")}</g>`;
    s += `<ellipse cx="540" cy="1080" rx="80" ry="40" fill="#8fa9b1" opacity=".18"/>`;
    put(L.set, s);
    put(L.glow, `<circle cx="560" cy="1060" r="700" fill="url(#torchpool)"/>`);
  }

  // ---------------- the kong koi: tall, hunched, one leg, arms to the knee ----------------
  function koi(id, x, y, s, o = {}) {
    const c = o.col || "#040706", rim = o.rim || "#24332f", rw = o.rimW ?? 2.5;
    const R = `stroke="${rim}" stroke-width="${rw}" stroke-linejoin="round"`;
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><ellipse cx="20" cy="6" rx="80" ry="12" fill="#000" opacity=".45"/>
      <g id="${id}-body">
      <path d="M-6,-470C-30,-420 -50,-330 -30,-230L-44,-196M-30,-230L-24,-192M-30,-230L-10,-200" stroke="${c}" stroke-width="13" fill="none" stroke-linecap="round" opacity=".85"/>
      <path d="M-26,-300C-34,-240 -10,-190 14,-150C26,-120 14,-70 6,-24L24,-20C36,-70 48,-130 36,-162C22,-200 16,-250 24,-300Z" fill="${c}" ${R}/>
      <path d="M-6,-30C-22,-10 -18,4 10,6L104,10C118,10 120,0 106,-6L72,-16C52,-22 32,-32 24,-38Z" fill="${c}" ${R}/>
      <path d="M104,10l18,4M100,-2l20,-2M92,-10l16,-8" stroke="${c}" stroke-width="5" stroke-linecap="round"/>
      <path d="M-36,-290C-54,-360 -44,-450 0,-506C30,-538 80,-528 88,-486C94,-446 64,-404 42,-352C32,-322 26,-302 22,-290Z" fill="${c}" ${R}/>
      <path d="M62,-500C72,-542 112,-552 130,-524C142,-502 134,-468 112,-458C92,-450 68,-466 62,-500Z" fill="${c}" ${R}/>
      ${o.eyes ? `<g class="koieyes"><circle cx="102" cy="-498" r="12" fill="#e9ffc0" opacity=".28"/><circle cx="120" cy="-494" r="12" fill="#e9ffc0" opacity=".28"/><circle cx="102" cy="-498" r="4.5" fill="#f4ffe0"/><circle cx="120" cy="-494" r="4.5" fill="#f4ffe0"/></g>` : ""}
      <path d="M72,-526C62,-466 68,-386 60,-306M90,-536C88,-466 98,-386 92,-296M110,-536C116,-476 126,-396 120,-316M128,-520C142,-466 146,-406 138,-336" stroke="${c}" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M44,-474C76,-424 100,-334 106,-214" stroke="${c}" stroke-width="17" fill="none" stroke-linecap="round"/>
      <path d="M106,-214l10,50M106,-214l-2,54M106,-214l-15,46M106,-214l24,38" stroke="${c}" stroke-width="5.5" fill="none" stroke-linecap="round"/></g></g>`;
  }
  // hop between points with a squash on each landing
  function hop(tl, id, t0, dur, o) {
    const g = document.getElementById(id), b = document.getElementById(`${id}-body`);
    const c = { t: 0 }, n = o.hops || 3, H = o.h || 90;
    const go = () => {
      const u = Math.min(1, c.t / dur), k = u * n, ph = k - Math.floor(k);
      const x = o.x0 + (o.x1 - o.x0) * u, y = o.y - Math.sin(Math.PI * ph) * H;
      const sq = ph < 0.12 ? 1 - (0.12 - ph) * 1.6 : 1;
      g.setAttribute("transform", `translate(${f1(x)},${f1(y)}) scale(${(o.flip ? -1 : 1) * o.s},${o.s})`);
      b.setAttribute("transform", `scale(${(2 - sq).toFixed(3)},${sq.toFixed(3)})`);
    };
    tl.to(c, { t: dur, duration: dur, ease: "none", onUpdate: go, immediateRender: false }, t0);
  }

  // ---------------- rain: two depths of streaks falling in a loop (screen space, above the darkness) ----------------
  function rain(tl, L, id, t0, dur, o = {}) {
    const r = mk(o.seed || 77), H = 1920, layers = [];
    [[o.far ?? 110, 26, 0.18, 2.2], [o.near ?? 60, 54, 0.32, 4]].forEach(([n, len, op, w], li) => {
      let s = "";
      for (let rep = 0; rep < 2; rep++) for (let i = 0; i < n; i++) {
        const x = r() * 1300 - 100, y = r() * H + rep * H;
        s += `<path d="M${f1(x)},${f1(y)}l${f1(-len * 0.18)},${len}" stroke="${o.col || "#d9e6e8"}" stroke-width="${w}" stroke-linecap="round" opacity="${op}"/>`;
      }
      put(L.light, `<g id="${id}-rain${li}">${s}</g>`);
      layers.push([document.getElementById(`${id}-rain${li}`), li ? 2300 : 1500]);
    });
    const c = { t: 0 };
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => layers.forEach(([g, v]) => {
      const y = -H + ((c.t * v) % H);
      g.setAttribute("transform", `translate(${f1(-y * 0.18 - 0.18 * H)},${f1(y)})`);
    }) }, t0);
  }
  // drifting mist / ripples / swaying leaves
  function life(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".rip").forEach((el, i) => tl.fromTo(el, { opacity: 0.1, x: -8 }, { opacity: 0.7, x: 10, duration: 0.9 + (i % 4) * 0.2, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 5) * 0.15));
    q(".hammock").forEach((el) => tl.fromTo(el, { rotation: -1.6 }, { rotation: 1.6, svgOrigin: "1040 1120", duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".foam").forEach((el, i) => tl.fromTo(el, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -140 }, duration: 0.7 + (i % 3) * 0.2, repeat: Math.ceil(dur / 0.7), ease: "none", immediateRender: false }, t0));
    q(".deb").forEach((el, i) => tl.fromTo(el, { x: 0 }, { x: 520, duration: dur, ease: "none", immediateRender: false }, t0));
    q(".pup").forEach((el, i) => tl.fromTo(el, { rotation: -1.5 }, { rotation: 1.5, svgOrigin: `${el.dataset.ox} ${el.dataset.oy}`, duration: 0.9 + (i % 3) * 0.25, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + i * 0.1));
    q(".lamp").forEach((el, i) => tl.fromTo(el, { opacity: 0.85 }, { opacity: 1, duration: 0.13 + (i % 3) * 0.05, repeat: Math.ceil(dur / 0.13), yoyo: true, ease: "none", immediateRender: false }, t0));
    q(".shaft").forEach((el, i) => tl.fromTo(el, { opacity: 0.35 }, { opacity: 0.85, duration: 2.2 + i * 0.4, repeat: Math.ceil(dur / 2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
  }

  // ======================= EP.3: stream crossing, boiling water, signals, the hospital =======================
  Sets.DEFS += `
    <linearGradient id="streamg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c8762"/><stop offset=".5" stop-color="#94906a"/><stop offset="1" stop-color="#6b7454"/></linearGradient>
    <linearGradient id="underw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8d8a60" stop-opacity=".62"/><stop offset="1" stop-color="#4f553e" stop-opacity=".85"/></linearGradient>
    <linearGradient id="potg" x1="0" x2="1"><stop offset="0" stop-color="#4a5054"/><stop offset=".3" stop-color="#c3cbcf"/><stop offset=".55" stop-color="#8d969b"/><stop offset="1" stop-color="#3e4448"/></linearGradient>
    <radialGradient id="firepool"><stop offset="0" stop-color="#ffb35c" stop-opacity=".8"/><stop offset=".45" stop-color="#ff8a3c" stop-opacity=".25"/><stop offset="1" stop-color="#ff8a3c" stop-opacity="0"/></radialGradient>
    <linearGradient id="hospWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfeae4"/><stop offset="1" stop-color="#c6d6cd"/></linearGradient>
    <linearGradient id="sepia" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9dab5"/><stop offset="1" stop-color="#c9b48a"/></linearGradient>
    <linearGradient id="underdark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#020303"/><stop offset=".75" stop-color="#050707"/><stop offset="1" stop-color="#1a201e" stop-opacity="0"/></linearGradient>`;
  const foamLines = (r, n, x0, x1, y0, y1, op = 0.5, col = "#eef0e4") => Array.from({ length: n }, () => {
    const y = y0 + r() * (y1 - y0), x = x0 + r() * (x1 - x0);
    return `<path class="foam" d="M${f1(x)},${f1(y)}h${f1(60 + r() * 200)}" stroke="${col}" stroke-width="${f1(3 + r() * 6)}" stroke-linecap="round" stroke-dasharray="${f1(30 + r() * 40)} 26" opacity="${op}"/>`;
  }).join("");
  const pebbles = (r, n, x0, x1, y0, y1, cols) => Array.from({ length: n }, (_, i) => `<ellipse cx="${f1(x0 + r() * (x1 - x0))}" cy="${f1(y0 + r() * (y1 - y0))}" rx="${f1(6 + r() * 20)}" ry="${f1(4 + r() * 10)}" fill="${cols[i % cols.length]}"/>`).join("");

  // POV at the water's edge: your own shoes at the bottom, fast shallow water across the frame
  function bankPOV(L, o = {}) {
    const id = o.id || "bp", r = mk(o.seed || 61), P = DAY;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#3a3428"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="1190" fill="${P.ground}"/>` + pebbles(r, 160, -700, 1800, -500, 560, P.litter);
    for (let x = -600; x < 1700; x += 170) s += clump(r, x + r() * 60, 80 + r() * 300, 120, P.set[0], P.set[2], P.hi);
    s += `<g opacity=".8">${footPrint(800, 470, 6, 1.1, "#241d14")}</g>`;
    s += `<path d="M-900,560C-300,540 300,600 900,560S1700,580 2000,570V1300C1500,1320 900,1270 400,1310S-400,1290 -900,1300Z" fill="url(#${o.mud ? "mudw" : "streamg"})"/>`;
    s += foamLines(r, 70, -900, 1800, 590, 1290, 0.55);
    s += [[180, 780, 70], [660, 700, 50], [920, 990, 80], [320, 1130, 55]].map(([x, y, w]) => `<path class="foam" d="M${x + w * 0.6},${y - w * 0.3}l${w * 2.2},${-w * 0.6}M${x + w * 0.6},${y + w * 0.3}l${w * 2.2},${w * 0.6}" stroke="#f4f2e8" stroke-width="7" stroke-linecap="round" stroke-dasharray="24 14" opacity=".75"/>
      <ellipse cx="${x}" cy="${y}" rx="${w}" ry="${w * 0.7}" fill="${P.rock}" ${OUT}/><ellipse cx="${x - w * 0.25}" cy="${y - w * 0.25}" rx="${w * 0.4}" ry="${w * 0.18}" fill="#dfe8e2" opacity=".35"/>`).join("");
    s += `<path d="M-900,1300C-400,1290 400,1320 900,1300S1700,1310 2000,1310V2600H-900Z" fill="#4a3f30"/>` + pebbles(r, 160, -700, 1800, 1320, 2400, ["#5c5040", "#3a3125", "#6b5e4a", "#2f281e"]);
    s += `<path class="foam" d="M-900,1300C-400,1290 400,1320 900,1300S1700,1310 2000,1310" stroke="#eef0e4" stroke-width="10" fill="none" stroke-dasharray="40 22" opacity=".6"/>`;
    put(L.set, s);
    const shoe = (x, y, rot) => `<g transform="translate(${x},${y}) rotate(${rot})"><path d="M-64,40C-72,-60 -52,-172 0,-178C52,-172 72,-60 64,40C60,120 32,172 0,174C-32,172 -60,120 -64,40Z" fill="#f0ece2" ${OUT}/>
      <path d="M-50,-120C-30,-150 30,-150 50,-120" stroke="#c9c3b6" stroke-width="10" fill="none"/><path d="M-30,-70h60M-32,-40h64M-32,-10h64" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>
      <ellipse cx="-24" cy="-150" rx="18" ry="9" fill="#7a5a3a" opacity=".6"/><ellipse cx="30" cy="-20" rx="12" ry="6" fill="#7a5a3a" opacity=".5"/>
      <path d="M-70,10C-74,200 -80,500 -90,800H90C80,500 74,200 70,10C40,-4 -40,-4 -70,10Z" fill="#2f3438" ${OUT}/><path d="M-66,30C-30,16 30,16 66,30" stroke="#22272a" stroke-width="10" fill="none"/></g>`;
    if (o.feet !== false) put(L.act, `<g id="${id}-feet">${shoe(400, 1560, -6)}${shoe(680, 1580, 5)}</g>`);
  }

  // the stream seen at three-quarters: a channel running from the far trees toward the viewer, people on the left bank
  function streamBank(L, o = {}) {
    const id = o.id || "sb", r = mk(o.seed || 171), P = DAY, G = o.ground ?? 1480;
    rainforest(L, { seed: o.seed || 171, time: "day", ground: G, treeX: -420, tree2X: 1560, fg: false, shafts: true, id });
    const lb = (y) => 560 - (y - (G - 120)) * 0.12, rb = (y) => 820 + (y - (G - 120)) * 0.42;
    let s = `<path d="M${lb(G - 120)},${G - 120}L${lb(2600)},2600L${rb(2600)},2600L${rb(G - 120)},${G - 120}Z" fill="#5a4b38"/>`;
    s += `<path d="M${lb(G - 110) + 14},${G - 110}L${lb(2600) + 30},2600L${rb(2600) - 30},2600L${rb(G - 110) - 14},${G - 110}Z" fill="url(#${o.mud ? "mudw" : "streamg"})"/>`;
    for (let k = 0; k < 46; k++) { const y = G - 100 + r() * 1100, u = r(), x = lb(y) + 30 + u * (rb(y) - lb(y) - 60), len = 40 + r() * 140; s += `<path class="foam" d="M${f1(x)},${f1(y)}l${f1(u * 30 - 6)},${f1(len)}" stroke="#eef0e4" stroke-width="${f1(3 + r() * 5)}" stroke-linecap="round" stroke-dasharray="${f1(20 + r() * 30)} 18" opacity=".55"/>`; }
    s += [[700, G + 120, 40], [900, G + 420, 60], [640, G + 700, 50]].map(([x, y, w]) => `<ellipse cx="${x}" cy="${y}" rx="${w}" ry="${w * 0.55}" fill="${P.rock}" ${OUT}/><path class="foam" d="M${x - w},${y + w * 0.4}q${w},${w * 0.8} ${w * 2},0" stroke="#f4f2e8" stroke-width="7" fill="none" stroke-dasharray="20 12"/>`).join("");
    s += `<path d="M${lb(G - 120)},${G - 120}L${lb(2600)},2600" stroke="#3a3125" stroke-width="16"/><path d="M${rb(G - 120)},${G - 120}L${rb(2600)},2600" stroke="#3a3125" stroke-width="16"/>`;
    put(L.set, s);
  }

  // side close-up at ankle height: a shoe on the stream bed, water to the ankle, a depth ruler (15 cm = 250 px)
  function ankleClose(L, o = {}) {
    const id = o.id || "ac", r = mk(o.seed || 71), P = DAY, S = 1150, B = 1400, cm = 250 / 15;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#a7b8af"/>`);
    let far = "";
    for (let i = 0; i < 12; i++) far += trunk(-700 + i * 200 + r() * 60, 980, -300, 40 + r() * 26, P.far[1], null, r);
    for (let x = -800; x < 1900; x += 120) far += clump(r, x, 120 + r() * 300, 170, P.far[0], P.far[2]);
    far += `<path d="M-900,940C-300,910 300,980 900,930S1600,950 2000,940V1200H-900Z" fill="${P.ground}"/>`;
    for (let x = -800; x < 1900; x += 140) far += fernBush(x + r() * 60, 960, 0.9, P.set[0], P.set[2], r);
    put(L.far, far + mist(400, 600, P.mist, 0.9));
    let s = `<rect x="-900" y="${S - 20}" width="2900" height="1500" fill="#6b6a4e"/>`;
    s += `<rect x="-900" y="${B - 30}" width="2900" height="1200" fill="#4f4836"/>` + pebbles(r, 90, -700, 1800, B - 30, B + 40, ["#7a7058", "#5c5444", "#8a8270", "#4a4436"]);
    // depth ruler, stood on the bed (behind the water surface so its lower half is under water)
    s += `<g id="${id}-ruler"><rect x="830" y="${B - 31 * cm}" width="70" height="${31 * cm}" rx="8" fill="#f2e6c4" ${OUT}/>
      ${Array.from({ length: 31 }, (_, k) => `<path d="M830,${f1(B - k * cm)}h${k % 5 ? 18 : 34}" stroke="${INK}" stroke-width="${k % 5 ? 3 : 5}"/>`).join("")}
      ${[0, 5, 10, 15, 20, 25, 30].map((k) => `<text x="${k ? 922 : 922}" y="${f1(B - k * cm + 11)}" font-family="Kanit" font-weight="900" font-size="32" fill="#f4ecd8" stroke="${INK}" stroke-width="6" paint-order="stroke">${k}</text>`).join("")}</g>`;
    // leg + shoe, toe downstream
    s += `<g id="${id}-leg"><path d="M352,-300L516,-300L512,1080L356,1080Z" fill="#2f3438" ${OUT}/><path d="M352,1040H514" stroke="#22272a" stroke-width="14"/>
      <path d="M356,1066C352,1180 350,1290 346,1350C344,1384 366,${B} 404,${B}L650,${B}C686,${B} 700,1380 686,1356C670,1330 610,1316 568,1300C536,1290 520,1240 516,1066Z" fill="#f0ece2" ${OUT}/>
      <path d="M348,1378H690" stroke="#c9c3b6" stroke-width="16"/><path d="M500,1200l60,40M500,1240l56,30M520,1160l40,40" stroke="${INK}" stroke-width="5" stroke-linecap="round"/></g>`;
    // the water itself: piles up on the upstream side of the leg, a trough and foam behind it
    let surf = `M-900,${S}`;
    for (let x = -900; x <= 2000; x += 40) {
      const near = x > 250 && x < 360 ? -30 * Math.sin(((x - 250) / 110) * Math.PI) : 0, wake = x > 520 && x < 760 ? 18 * Math.sin(((x - 520) / 240) * Math.PI) : 0;
      surf += `L${x},${f1(S + 6 * Math.sin(x / 47) + 4 * Math.sin(x / 13) + near + wake)}`;
    }
    s += `<path id="${id}-water" d="${surf}V${B + 40}H-900Z" fill="url(#underw)"/>`;
    s += `<path class="foam" d="${surf}" stroke="#f4f2e8" stroke-width="9" fill="none" stroke-dasharray="36 16" opacity=".8"/>`;
    s += foamLines(r, 26, -900, 1800, S + 20, B - 30, 0.45);
    s += `<g>${Array.from({ length: 14 }, () => `<circle class="foam" cx="${f1(300 + r() * 420)}" cy="${f1(S - 26 + r() * 46)}" r="${f1(6 + r() * 14)}" fill="#f4f2e8" opacity=".75" stroke-dasharray="0"/>`).join("")}</g>`;
    s += Array.from({ length: 5 }, (_, k) => `<g class="flow" data-i="${k}"><path d="M-120,${S + 50 + k * 42}H120" stroke="#eef4ee" stroke-width="10" stroke-linecap="round" opacity=".7"/><path d="M120,${S + 50 + k * 42}l-28,-18M120,${S + 50 + k * 42}l-28,18" stroke="#eef4ee" stroke-width="10" stroke-linecap="round" opacity=".7"/></g>`).join("");
    s += `<g id="${id}-mark" opacity="0"><path d="M780,${S}H1000" stroke="#e8443a" stroke-width="8" stroke-dasharray="20 10"/><path d="M1000,${S}l-22,-14v28z" fill="#e8443a"/></g>`;
    s += `<g id="${id}-splash" opacity="0">${Array.from({ length: 16 }, (_, k) => `<circle cx="${f1(420 + Math.cos(k) * (60 + r() * 140))}" cy="${f1(S - 40 - r() * 180)}" r="${f1(8 + r() * 16)}" fill="#e6eee6" opacity=".85"/>`).join("")}</g>`;
    put(L.set, s);
  }

  // aerial map: the fast narrow section where they stand, a route down the bank to a wide shallow reach
  function streamMap(L, o = {}) {
    const id = o.id || "sm", r = mk(o.seed || 81);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#24402f"/>`);
    let s = "";
    for (let i = 0; i < 150; i++) s += clump(r, -600 + r() * 2300, -400 + r() * 2800, 110 + r() * 70, ["#3e5f48", "#4a6e52", "#355540"][i % 3], "#2d4838", "#6e9668");
    const top = "M300,-400C360,0 420,300 300,700C230,940 300,1060 420,1180", low = "M400,1160C520,1300 700,1400 690,1700C680,1960 600,2200 620,2600";
    s += `<path d="${top}" stroke="#5e5440" stroke-width="130" fill="none" stroke-linecap="round"/><path d="${top}" stroke="url(#streamg)" stroke-width="96" fill="none" stroke-linecap="round"/>`;
    s += `<path d="${low}" stroke="#5e5440" stroke-width="330" fill="none" stroke-linecap="round"/><path d="${low}" stroke="#8fa38a" stroke-width="290" fill="none" stroke-linecap="round"/>`;
    s += [[640, 1420, 90, 26], [560, 1560, 70, 20], [720, 1700, 80, 24], [640, 1850, 60, 18]].map(([x, y, a, b]) => `<ellipse cx="${x}" cy="${y}" rx="${a}" ry="${b}" fill="#d6c79c" transform="rotate(-30 ${x} ${y})"/>`).join("");
    s += `<g>${[[310, 300], [350, 500], [300, 700], [280, 860], [340, 1040]].map(([x, y]) => `<path class="foam" d="M${x - 20},${y}q20,-14 40,0" stroke="#f4f2e8" stroke-width="6" fill="none" stroke-dasharray="14 10"/>`).join("")}</g>`;
    for (let i = 0; i < 30; i++) { const x = -500 + r() * 2100, y = -300 + r() * 2600; if (Math.abs(x - 330) < 220 || (Math.abs(x - 620) < 260 && y > 1100)) continue; s += clump(r, x, y, 90 + r() * 50, ["#4f7653", "#5c855c", "#466b4b"][i % 3], "#3a5a40", "#8db37e"); }
    s += `<g id="${id}-us">${[["#e8b830", 0], ["#34506e", 26], ["#3e5a44", 52]].map(([c, d], k) => `<g transform="translate(${190 - k * 6},${660 + d})"><circle r="15" fill="${c}" ${OUT}/></g>`).join("")}</g>`;
    s += `<g id="${id}-no" opacity="0"><path d="M262,650l90,90M352,650l-90,90" stroke="#fff" stroke-width="30" stroke-linecap="round"/><path d="M262,650l90,90M352,650l-90,90" stroke="#e8443a" stroke-width="18" stroke-linecap="round"/></g>`;
    const pts = []; for (let k = 0; k <= 13; k++) { const u = k / 13, a = 1 - u; pts.push([a * a * a * 200 + 3 * a * a * u * 210 + 3 * a * u * u * 330 + u * u * u * 470, a * a * a * 760 + 3 * a * a * u * 980 + 3 * a * u * u * 1240 + u * u * u * 1440]); }
    s += `<g id="${id}-route">${pts.map(([x, y], k) => `<circle class="rd" data-i="${k}" cx="${f1(x)}" cy="${f1(y)}" r="12" fill="#f4ecd8" stroke="${INK}" stroke-width="3" opacity="0"/>`).join("")}</g>`;
    s += `<g id="${id}-ok" opacity="0" transform="translate(640,1560)"><circle r="62" fill="#3e9a6a" stroke="#fff" stroke-width="10"/><path d="M-28,2l20,22l38,-44" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
    put(L.set, s);
    put(L.fg, mist(-300, 700, "url(#mistg)", 0.55));
  }

  // a pot of muddy stream water on three stones over a small fire, close up at dusk
  function boilPot(L, o = {}) {
    const id = o.id || "bo", r = mk(o.seed || 91);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#16201d"/>`);
    let far = "";
    for (let i = 0; i < 12; i++) far += trunk(-700 + i * 210 + r() * 60, 1500, -300, 50 + r() * 30, "#1f2b27", null, r);
    for (let x = -800; x < 1900; x += 140) far += clump(r, x, 160 + r() * 300, 180, "#1b2824", "#22322d");
    put(L.far, far);
    let s = `<rect x="-900" y="1480" width="2900" height="1200" fill="#2b261d"/>` + pebbles(r, 120, -700, 1800, 1500, 2300, ["#3a3125", "#1f1a14", "#4a3e2d"]);
    s += `<g transform="translate(540,1520)"><path d="M-170,-10l340,-40M-170,-50l340,30" stroke="#3a2a1c" stroke-width="34" stroke-linecap="round"/>
      <path class="fl1" d="M-120,0C-140,-90 -90,-150 -60,-220C-40,-150 -10,-120 0,-60C10,-120 40,-170 70,-230C100,-150 140,-90 120,0Z" fill="#ff8a3c"/>
      <path class="fl2" d="M-80,0C-90,-70 -60,-110 -30,-160C-10,-110 10,-90 20,-50C40,-100 60,-120 80,-160C100,-100 110,-50 90,0Z" fill="#ffb35c"/>
      <path class="fl3" d="M-40,0C-46,-40 -20,-70 0,-100C20,-70 46,-40 40,0Z" fill="#fff0b0"/>
      ${[[-200, -10, 70, 50], [200, -6, 66, 48], [0, 30, 90, 40]].map(([x, y, a, b]) => `<ellipse cx="${x}" cy="${y}" rx="${a}" ry="${b}" fill="#5f5a50" ${OUT}/><ellipse cx="${x - a * 0.3}" cy="${y - b * 0.4}" rx="${a * 0.4}" ry="${b * 0.18}" fill="#8a8478" opacity=".6"/>`).join("")}</g>`;
    // the pot: water seen from a little above so the rolling boil reads
    s += `<g id="${id}-pot"><path d="M320,1080C320,1260 340,1380 380,1430H700C740,1380 760,1260 760,1080Z" fill="url(#potg)" ${OUT}/>
      <path d="M300,1080h-40q-20,0 -20,20v20q0,14 20,14h56M780,1080h40q20,0 20,20v20q0,14 -20,14h-56" fill="none" stroke="${INK}" stroke-width="10"/>
      <ellipse cx="540" cy="1080" rx="226" ry="54" fill="#3e4448" ${OUT}/><ellipse id="${id}-water" cx="540" cy="1088" rx="200" ry="40" fill="#8a7650"/>
      <g id="${id}-bub">${Array.from({ length: 22 }, (_, k) => { const a = r() * Math.PI * 2, d = Math.sqrt(r()); return `<circle class="bub" data-i="${k}" cx="${f1(540 + Math.cos(a) * d * 180)}" cy="${f1(1088 + Math.sin(a) * d * 32)}" r="${f1(8 + r() * 14)}" fill="#c9b893" stroke="#f4ecd8" stroke-width="3" opacity="0"/>`; }).join("")}</g>
      <path d="M340,1120C360,1300 380,1380 400,1420" stroke="#e6ecef" stroke-width="10" fill="none" opacity=".45"/></g>`;
    s += `<g id="${id}-steam">${[0, 1, 2, 3, 4].map((k) => `<path class="steam" data-i="${k}" d="M${400 + k * 70},1040c-30,-60 30,-100 0,-160s30,-100 0,-160" stroke="#e8eef0" stroke-width="${18 - k}" fill="none" stroke-linecap="round" opacity="0"/>`).join("")}</g>`;
    put(L.set, s);
    put(L.glow, `<circle class="fireglow" cx="540" cy="1450" r="620" fill="url(#firepool)"/>`);
  }

  // helicopter: side silhouette (rotor = a fast-flickering blade) and top-down (spinning blades)
  function heliSide(id, x, y, s, col = "#0d1211") {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M-120,-10C-120,-70 -60,-96 20,-96C90,-96 130,-60 130,-10C130,20 90,34 20,34H-80C-110,34 -120,20 -120,-10Z" fill="${col}"/>
      <path d="M110,-40L420,-56L420,-30L120,-6Z" fill="${col}"/><path d="M400,-56l26,-50l14,4l-14,70z" fill="${col}"/><circle class="trot" cx="420" cy="-44" r="34" fill="none" stroke="${col}" stroke-width="6" opacity=".6"/>
      <path d="M-80,34v30M70,34v30M-130,66H120" stroke="${col}" stroke-width="10" stroke-linecap="round"/><path d="M0,-96v-30" stroke="${col}" stroke-width="12"/>
      <path class="rotor" d="M-330,-128H330" stroke="${col}" stroke-width="10" stroke-linecap="round"/><path d="M-70,-60C-40,-84 10,-84 20,-60V-20H-70Z" fill="#9fb3b8" opacity=".35"/></g>`;
  }
  function heliTop(id, x, y, s, col = "#151b1a") {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})"><path d="M0,-130C40,-130 60,-80 60,-20C60,40 30,70 0,70C-30,70 -60,40 -60,-20C-60,-80 -40,-130 0,-130Z" fill="${col}"/>
      <path d="M-10,60L-14,330H14L10,60Z" fill="${col}"/><path d="M-50,320H50" stroke="${col}" stroke-width="12" stroke-linecap="round"/>
      <circle r="300" fill="${col}" opacity=".12"/><g class="blades"><path d="M-300,0H300M0,-300V300" stroke="${col}" stroke-width="16" stroke-linecap="round" opacity=".75"/></g></g>`;
  }

  // looking straight up from under the canopy: trunks converge, leaves close over, one small gap of sky
  function canopyUp(L, o = {}) {
    const id = o.id || "cu", r = mk(o.seed || 101), gx = o.gapX ?? 620, gy = o.gapY ?? 420;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#d6ded8"/>`);
    put(L.far, `<g id="${id}-heliw">${heliSide(`${id}-heli`, gx, gy, 0.42, "#1a2220")}</g>`);
    let mid = "";
    for (let k = 0; k < 9; k++) { const bx = -300 + k * 210 + r() * 60, tx = 540 + (bx - 540) * 0.18; mid += `<path d="M${f1(bx - 70)},2400L${f1(tx - 10)},300L${f1(tx + 10)},300L${f1(bx + 70)},2400Z" fill="${["#3c4a40", "#33413a", "#45534a"][k % 3]}"/>`; }
    put(L.mid, mid);
    let s = "";
    for (let i = 0; i < 220; i++) { const x = -600 + r() * 2300, y = -500 + r() * 2000, d = Math.hypot(x - gx, (y - gy) * 1.3); if (d < 210) continue; s += clump(r, x, y, 120 + r() * 80, ["#1f3427", "#284232", "#173023"][i % 3], "#11241a", d < 330 ? "#5e8a62" : null); }
    put(L.set, s);
    put(L.fg, frond(-160, 1600, 620, -60, 80, "#0c1a12", "#173023", 1.8) + frond(1240, 1700, 640, -120, -90, "#0c1a12", "#173023", 1.8));
  }

  // top-down: canopy all round a grassy clearing; V of yellow poncho + branches; one-foot prints; helicopter
  function aerialClearing(L, o = {}) {
    const id = o.id || "ac2", r = mk(o.seed || 111), open = o.clearing !== false, cx = 540, cy = 1000, rx = 380, ry = 520;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#20382a"/>`);
    let s = "";
    if (open) {
      s += `<ellipse cx="${cx}" cy="${cy}" rx="${rx + 40}" ry="${ry + 40}" fill="#2f4a33"/><ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="#7d9a5a"/>`;
      s += Array.from({ length: 260 }, () => { const a = r() * Math.PI * 2, d = Math.sqrt(r()) * 0.95, x = cx + Math.cos(a) * d * rx, y = cy + Math.sin(a) * d * ry; return `<path d="M${f1(x)},${f1(y)}l${f1(-6 + r() * 12)},-16" stroke="${["#5f7d44", "#93ad6a", "#6e8b4c"][Math.floor(r() * 3)]}" stroke-width="4" stroke-linecap="round"/>`; }).join("");
      s += `<g transform="translate(330,1300) rotate(-24)"><rect x="-120" y="-20" width="240" height="40" rx="20" fill="#5a4636" ${OUT}/></g>`;
      if (o.prints) s += `<g id="${id}-prints">${Array.from({ length: o.prints }, (_, k) => { let x, y; do { const a = r() * Math.PI * 2, d = 0.25 + r() * 0.65; x = cx + Math.cos(a) * d * rx; y = cy + Math.sin(a) * d * ry; } while (Math.abs(y - 760 - (Math.abs(x - 540) * 560 / 210)) < 50 && y < 1340); return `<g class="pr" data-i="${k}" opacity="0">${footPrint(x, y, r() * 360, 0.75, "#1a1610")}</g>`; }).join("")}</g>`;
      s += `<g id="${id}-v"><path d="M330,760L540,1320L750,760" stroke="#4a3a20" stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <path d="M330,760L540,1320L750,760" stroke="#f2c230" stroke-width="46" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></g>`;
      s += `<g id="${id}-us">${[["#e8b830", 0], ["#34506e", 30]].map(([c, d]) => `<g transform="translate(${880 + d},${1240 + d})"><circle r="14" fill="${c}" ${OUT}/></g>`).join("")}</g>`;
    }
    for (let i = 0; i < 190; i++) { const x = -600 + r() * 2300, y = -400 + r() * 2800; if (open && ((x - cx) / (rx + 60)) ** 2 + ((y - cy) / (ry + 60)) ** 2 < 1) continue; s += clump(r, x, y, 120 + r() * 70, ["#3e5f48", "#4a6e52", "#355540"][i % 3], "#2d4838", "#6e9668"); }
    s += `<g id="${id}-hs" opacity=".35" transform="translate(1600,400)">${heliTop(`${id}-hsh`, 0, 0, 1, "#000")}</g>`;
    put(L.set, s);
    put(L.fg, mist(-300, 600, "url(#mistg)", 0.35));
  }

  // side view of the clearing: open sky, forest walls left and right, grass; the dark gap Mad walks into on the right
  function clearingSide(L, o = {}) {
    const id = o.id || "cs", r = mk(o.seed || 121), P = DAY, G = o.ground ?? 1500;
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="url(#koiDay)"/>`);
    let far = "";
    for (let x = -800; x < 1900; x += 90) far += clump(r, x, G - 380 + r() * 120, 150, P.far[0], P.far[2]);
    put(L.far, far + mist(G - 600, 500, P.mist, 0.8));
    let mid = "";
    for (const side of [-1, 1]) {
      const x0 = side < 0 ? -500 : 920;
      for (let k = 0; k < 6; k++) mid += trunk(x0 + k * 90 + r() * 30, G + 10, -300, 50 + r() * 30, P.trunkM, P.mid[2], r);
      for (let k = 0; k < 14; k++) mid += clump(r, x0 + r() * 600, -100 + r() * 900, 190, P.mid[0], P.mid[1], P.hi);
    }
    mid += `<path d="M960,${G}C960,${G - 300} 1000,${G - 520} 1080,${G - 560}C1160,${G - 520} 1200,${G - 300} 1200,${G}Z" fill="#0d1612" opacity=".9"/>`;
    put(L.mid, mid);
    let s = `<path d="M-900,${G - 20}C-300,${G - 40} 400,${G} 1000,${G - 30}S1800,${G - 10} 2000,${G - 20}V2700H-900Z" fill="#6f8a4c"/>`;
    s += Array.from({ length: 220 }, () => `<path d="M${f1(-700 + r() * 2500)},${f1(G + r() * 900)}l${f1(-8 + r() * 16)},-22" stroke="${["#5a7440", "#86a35f", "#4e6838"][Math.floor(r() * 3)]}" stroke-width="5" stroke-linecap="round"/>`).join("");
    for (let x = -600; x < 1800; x += 300) if (x < 100 || x > 900) s += fernBush(x + r() * 60, G + 30, 1.1, P.set[0], P.set[2], r);
    put(L.set, s);
    put(L.light, [0, 1].map((k) => `<path class="shaft" d="M${360 + k * 260},-100L${480 + k * 260},-100L${640 + k * 220},2000L${480 + k * 220},2000Z" fill="url(#shaftg)" opacity=".7"/>`).join(""));
  }

  // mud from above: a line of prints that are all the same foot, each followed by the round hole of a stick
  function stickTracks(L, o = {}) {
    const id = o.id || "st", r = mk(o.seed || 131), fl = o.floor;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3600" fill="${fl ? "#c9cfcb" : "#2a241c"}"/>`);
    let s;
    if (fl) {
      s = `<rect x="-900" y="-600" width="2900" height="3600" fill="#d6dbd7"/>` + Array.from({ length: 16 }, (_, k) => `<path d="M${-500 + k * 160},-600V3000M-900,${-600 + k * 240}H2000" stroke="#bfc6c1" stroke-width="5"/>`).join("");
      s += `<rect x="-900" y="-600" width="2900" height="${fl - -600}" fill="#060808"/><rect x="-900" y="${fl - 40}" width="2900" height="40" fill="#8a949a"/>`;
    } else {
      s = `<rect x="-900" y="-600" width="2900" height="3600" fill="#4a3e2e"/>` + pebbles(r, 500, -400, 1500, -400, 2900, ["#5a4a36", "#3a3125", "#6b5a42", "#2f3a2a"]);
      for (let i = 0; i < 40; i++) s += `<path d="M${f1(-200 + r() * 1500)},${f1(-300 + r() * 3000)}q${f1(10 + r() * 20)},-${f1(4 + r() * 8)} ${f1(30 + r() * 30)},0" stroke="#c9d6cf" stroke-width="2" fill="none" opacity=".25"/>`;
    }
    const P = Array.from({ length: o.n || 9 }, (_, k) => [500 + Math.sin(k * 0.8) * 26, 2500 - k * 330]), ink = fl ? "#5a4228" : "#140f0a", hole = fl ? "#4a3420" : "#0e0b07";
    s += `<g id="${id}-hl" opacity="0">${P.map(([x, y]) => footPrint(x, y, -4, 1.75, "#ff3b2f")).join("")}</g>`;
    s += `<g id="${id}-prints">${P.map(([x, y], k) => `<g class="pr" data-i="${k}">${footPrint(x, y, -4, 1.5, ink)}<circle cx="${f1(x + 170)}" cy="${f1(y - 130)}" r="22" fill="${hole}"/><circle cx="${f1(x + 170)}" cy="${f1(y - 130)}" r="30" fill="none" stroke="${fl ? "#7a6448" : "#2a2218"}" stroke-width="6" opacity=".7"/></g>`).join("")}</g>`;
    put(L.set, s);
  }

  // hospital room, side view: bed (head left), IV pole, window with blinds; optional stick and mud prints
  function hospRoom(L, o = {}) {
    const id = o.id || "hr", G = 1640, r = mk(o.seed || 141);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#cfdcd5"/>`);
    let far = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="url(#hospWall)"/><rect x="-900" y="${G - 60}" width="2900" height="60" fill="#9fb5aa"/>`;
    far += `<g transform="translate(560,260)"><rect width="420" height="560" fill="#eaf6fb" stroke="#8fa39a" stroke-width="14"/><rect x="10" y="10" width="400" height="540" fill="#bfe0ef"/>
      ${Array.from({ length: 14 }, (_, k) => `<rect x="10" y="${16 + k * 38}" width="400" height="22" fill="#f4f8f4" opacity=".9"/>`).join("")}</g>`;
    far += `<g transform="translate(150,200)"><circle r="60" fill="#f4f4f0" stroke="#6b7a72" stroke-width="8"/><path d="M0,0V-38M0,0L26,14" stroke="${INK}" stroke-width="6" stroke-linecap="round"/></g>`;
    far += `<rect x="-200" y="1000" width="560" height="60" rx="10" fill="#b9cbc2" stroke="#8fa39a" stroke-width="4"/>${[0, 1, 2].map((k) => `<circle cx="${-100 + k * 140}" cy="1030" r="14" fill="#6b7a72"/>`).join("")}`;
    put(L.far, far);
    let s = `<rect x="-900" y="${G}" width="2900" height="1000" fill="#d8dcd8"/>${Array.from({ length: 18 }, (_, k) => `<path d="M${-900 + k * 160},${G}V2600" stroke="#c2c8c4" stroke-width="4"/>`).join("")}<path d="M-900,${G + 160}H2000M-900,${G + 360}H2000" stroke="#c2c8c4" stroke-width="4"/>`;
    s += `<path d="M300,1400H900V${G}H300Z" fill="#1b2422" opacity=".55"/>`;
    if (o.prints) s += `<g id="${id}-prints">${[[1400, 1800], [1210, 1720], [1030, 1680], [880, 1650]].map(([x, y], k) => `<g class="pr" data-i="${k}" transform="translate(${x},${y}) scale(1,0.32)">${footPrint(0, 0, -96, 0.95, "#4a3a26")}<circle cx="-40" cy="-150" r="18" fill="#3a2c1c"/></g>`).join("")}</g>`;
    s += `<g id="${id}-bed"><path d="M240,1100V${G - 40}M940,1220V${G - 40}" stroke="#9aa3a8" stroke-width="22" stroke-linecap="round"/>
      ${[300, 880].map((x) => `<circle cx="${x}" cy="${G - 26}" r="26" fill="#3e4448" ${OUT}/>`).join("")}<rect x="240" y="1380" width="700" height="34" rx="8" fill="#9aa3a8" ${OUT}/>
      <rect x="250" y="1290" width="680" height="96" rx="24" fill="#f4f6f2" ${OUT}/><path d="M250,1340H930" stroke="#dfe4e0" stroke-width="10"/>
      <rect x="226" y="1080" width="36" height="320" rx="14" fill="#c9d0d4" ${OUT}/></g>`;
    s += `<g transform="translate(130,0)"><path d="M0,${G}V700" stroke="#9aa3a8" stroke-width="12"/><path d="M-50,${G}h100" stroke="#9aa3a8" stroke-width="12" stroke-linecap="round"/><path d="M-40,700h80" stroke="#9aa3a8" stroke-width="10"/>
      <rect x="-34" y="710" width="68" height="110" rx="20" fill="#e8f2f6" stroke="#8fa39a" stroke-width="5" opacity=".95"/><path d="M0,820C10,900 60,1000 120,1260" stroke="#c9d6da" stroke-width="5" fill="none"/></g>`;
    s += `<g transform="translate(1000,${G})"><rect x="0" y="-300" width="200" height="300" rx="10" fill="#e6ebe7" ${OUT}/><path d="M20,-150h160" stroke="#b9c2bd" stroke-width="5"/><rect x="40" y="-360" width="56" height="60" rx="8" fill="#f2e6c4" ${OUT}/></g>`;
    if (o.stick) s += `<g id="${id}-stick" transform="translate(950,${G}) rotate(-9)"><rect x="-9" y="-560" width="18" height="560" rx="8" fill="#6a4a2e" ${OUT}/><path d="M-9,-560q9,-26 18,0" fill="#4a3426"/><path d="M-9,-90h18v90h-18z" fill="#3a2c1c" opacity=".85"/><path d="M-6,-120q4,20 -2,40M4,-140q-2,24 3,46" stroke="#3a2c1c" stroke-width="5" fill="none"/></g>`;
    put(L.set, s);
    put(L.light, `<path class="shaft" d="M560,260L980,260L1300,1700L700,1700Z" fill="url(#shaftg)" opacity=".5"/>`);
  }
  // a blanket over legs in bed, drawn over the actors (the shot moves it to the top of the act layer)
  function blanket(id, x0, x1, y) {
    return `<g id="${id}"><path d="M${x0},${y - 70}C${x0 + 120},${y - 96} ${x1 - 160},${y - 90} ${x1},${y - 60}L${x1 + 20},${y + 10}H${x0 - 10}Z" fill="#cfe3ec" ${OUT}/><path d="M${x0 + 40},${y - 70}C${x0 + 140},${y - 30} ${x1 - 140},${y - 40} ${x1 - 20},${y - 20}" stroke="#a9c6d4" stroke-width="7" fill="none"/></g>`;
  }

  // floor level, looking into the dark under the bed: sheet hanging at the top, two pale eyes, a hand
  function underBed(L, o = {}) {
    const id = o.id || "ub", r = mk(o.seed || 151);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0a0d0d"/>`);
    let s = `<rect x="-900" y="560" width="2900" height="760" fill="url(#underdark)"/>`;
    s += `<path d="M-900,1260L2000,1260V2600H-900Z" fill="#b9bfbb"/>${Array.from({ length: 16 }, (_, k) => `<path d="M${540 + (k - 8) * 70},1260L${540 + (k - 8) * 260},2600" stroke="#a3aaa6" stroke-width="5"/>`).join("")}${[1400, 1620, 1950].map((y) => `<path d="M-900,${y}H2000" stroke="#a3aaa6" stroke-width="5"/>`).join("")}`;
    s += `<rect x="-900" y="1240" width="2900" height="60" fill="#0a0d0d" opacity=".55"/>`;
    s += `<g opacity=".85">${footPrint(330, 1700, -12, 1.25, "#4a3a26")}<circle cx="520" cy="1560" r="26" fill="#3a2c1c"/></g>`;
    s += `<g id="${id}-hair" opacity="0">${Array.from({ length: 12 }, (_, k) => `<path d="M${500 + k * 12},700C${492 + k * 14},800 ${506 + k * 10},920 ${496 + k * 13},${1040 + (k % 3) * 40}" stroke="#151a19" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    s += `<g id="${id}-eyes" opacity="0"><circle cx="540" cy="860" r="22" fill="#e9ffc0" opacity=".25"/><circle cx="600" cy="866" r="22" fill="#e9ffc0" opacity=".25"/><circle cx="540" cy="860" r="7" fill="#f4ffe0"/><circle cx="600" cy="866" r="7" fill="#f4ffe0"/></g>`;
    s += `<g id="${id}-hand" opacity="0" transform="translate(300,1240)"><path d="M-160,-200C-100,-120 -40,-60 0,-20C20,0 40,10 60,8" stroke="#050707" stroke-width="40" fill="none" stroke-linecap="round"/>
      ${[[60, 8, 150, 60], [56, -6, 160, 20], [50, -18, 150, -16], [40, 20, 120, 90]].map(([a, b, c, d]) => `<path d="M${a},${b}Q${(a + c) / 2},${(b + d) / 2 - 20} ${c},${d}" stroke="#050707" stroke-width="13" fill="none" stroke-linecap="round"/>`).join("")}</g>`;
    s += `<path d="M-900,-600H2000V520C1700,560 1500,500 1200,548C900,600 700,520 400,560C100,600 -300,530 -900,560Z" fill="#e3e8e3"/><path d="M-900,520C-300,500 300,560 900,510S1700,530 2000,520" stroke="#b9c2bc" stroke-width="14" fill="none"/>
      <path d="M-200,-600C-180,-100 -220,300 -190,540M300,-600C320,-100 280,300 310,550M800,-600C780,-100 820,300 790,540" stroke="#c9d0cb" stroke-width="12" fill="none"/>`;
    put(L.set, s);
  }

  // a yellowed newspaper clipping pinned to a corkboard; the shot puts a sepia actor in the photo box
  function posterBoard(L, o = {}) {
    const id = o.id || "pb", r = mk(o.seed || 161);
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="url(#hospWall)"/>`);
    let s = `<rect x="80" y="300" width="920" height="1340" rx="16" fill="#b98c5a" stroke="#7a5a36" stroke-width="18"/>` + Array.from({ length: 500 }, () => `<circle cx="${f1(100 + r() * 880)}" cy="${f1(320 + r() * 1300)}" r="${f1(1 + r() * 2.5)}" fill="#8a6440" opacity=".5"/>`).join("");
    s += `<rect x="120" y="340" width="260" height="200" fill="#f4f4ee" transform="rotate(-4 250 440)"/><rect x="720" y="1380" width="240" height="220" fill="#e8f0f4" transform="rotate(5 840 1490)"/>`;
    s += `<g transform="rotate(-2 540 960)"><rect x="200" y="520" width="680" height="900" fill="url(#sepia)" stroke="#a8916a" stroke-width="4"/>
      <text x="540" y="620" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#2b241a">ไกด์ท้องถิ่น</text><text x="540" y="690" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="58" fill="#2b241a">หายตัวในป่า</text>
      <rect x="250" y="730" width="300" height="380" fill="#d9c8a0" stroke="#5a4a32" stroke-width="6"/>
      ${Array.from({ length: 11 }, (_, k) => `<rect x="580" y="${740 + k * 34}" width="${250 - (k % 4) * 30}" height="12" rx="6" fill="#8a7a5a" opacity=".55"/>`).join("")}
      ${Array.from({ length: 6 }, (_, k) => `<rect x="250" y="${1150 + k * 40}" width="${580 - (k % 3) * 60}" height="12" rx="6" fill="#8a7a5a" opacity=".55"/>`).join("")}</g>`;
    s += [[220, 540], [860, 560], [540, 500]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="16" fill="#c8392b" ${OUT}/>`).join("");
    s += `<g id="${id}-stamp" opacity="0" transform="translate(560,1250) rotate(-12)"><rect x="-190" y="-60" width="380" height="120" rx="14" fill="none" stroke="#c8392b" stroke-width="12"/><text y="26" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="74" fill="#c8392b">20 ปีก่อน</text></g>`;
    s += `<defs><clipPath id="${id}-clip"><rect x="256" y="736" width="288" height="368" transform="rotate(-2 540 960)"/></clipPath></defs>`;
    put(L.set, s);
  }

  // extra looping motion for the EP.3 sets
  function life3(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".flow").forEach((el, i) => tl.fromTo(el, { x: -300 + (i % 2) * 200 }, { x: 1300, duration: 1.1 + (i % 3) * 0.2, repeat: Math.ceil(dur / 1.1), ease: "none", immediateRender: false }, t0 + i * 0.15));
    q(".bub").forEach((el, i) => tl.fromTo(el, { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1.2, duration: 0.32 + (i % 4) * 0.06, repeat: Math.ceil(dur / 0.35), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + (i % 7) * 0.07));
    q(".steam").forEach((el, i) => tl.fromTo(el, { opacity: 0, y: 40 }, { opacity: 0.5, y: -160, duration: 1.4, repeat: Math.ceil(dur / 1.4), ease: "sine.out", immediateRender: false }, t0 + i * 0.25));
    q(".blades").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360 * Math.ceil(dur / 0.25), svgOrigin: "0 0", duration: dur, ease: "none", immediateRender: false }, t0));
    q(".rotor").forEach((el) => tl.fromTo(el, { scaleX: 1 }, { scaleX: 0.15, svgOrigin: "0 -128", duration: 0.05, repeat: Math.ceil(dur / 0.05), yoyo: true, ease: "none", immediateRender: false }, t0));
  }

  // walking stick for บังหมาด
  if (window.Camp) Camp.hand.stick = `<g transform="translate(0,118)"><rect x="-7" y="-150" width="14" height="420" rx="6" fill="#6a4a2e" ${OUT}/><path d="M-7,-150q7,-20 14,0" fill="#4a3426"/></g>`;

  Object.assign(Sets, { rainforest, canopyAerial, aerialCamp, xsection, legendInk, legendShadow, streamClose, treeNight, footClose, leechHowTo, mudPrint,
    bankPOV, streamBank, ankleClose, streamMap, boilPot, canopyUp, aerialClearing, clearingSide, stickTracks, hospRoom, underBed, posterBoard });
  Sets.props = Object.assign(Sets.props || {}, { koi });
  window.Koi = { koi, koiSit, poncho, ponchoBack, hop, rain, life, life3, footPrint, heliSide, heliTop, blanket, NIGHT, DAY };
})();
