// รูพญานาค stills v2 (owner 2 Nov 2569 via coordination: "ทำเป็นที่มองจากด้านบนสวยๆ วัดขนาด กว้าง ยาว แล้วทำมุมที่เห็นความลึก ใต้ดิน" ·
// "แก้เป็นภาพ มาให้ผมดูก่อน"). Static SVG stills, 1080×1920, one scene per ?s=…:
//   drone-dusk · drone-moon   top-down drone view of the hole in the paddies, the crowd with incense and lucky-number boards
//   measure · measure-note   officials measure width and length with a knotted rope and a tape; the red rope runs further out at the ends (G1 p.28)
//   depth-1 … depth-4        one continuous camera move: sky → rim → through the soil layers → into the limestone cave with groundwater
(() => {
  const NS = "http://www.w3.org/2000/svg";
  const f = (n) => (+n).toFixed(1);
  const rng = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const LINE = "#1e1712";
  let defs = "";
  const def = (s) => { defs += s; };
  // an irregular closed blob around (cx, cy)
  const blob = (r, cx, cy, rx, ry, n = 40, wob = 0.08, rot = 0) => {
    const pts = []; for (let k = 0; k < n; k++) { const a = (k / n) * Math.PI * 2, w = 1 + (r() - 0.5) * 2 * wob;
      const x = Math.cos(a) * rx * w, y = Math.sin(a) * ry * w, c = Math.cos(rot), s = Math.sin(rot); pts.push([cx + x * c - y * s, cy + x * s + y * c]); }
    let d = `M${f(pts[0][0])},${f(pts[0][1])}`;
    for (let k = 0; k < n; k++) { const p = pts[(k + 1) % n], q2 = pts[(k + 2) % n]; d += `Q${f(p[0])},${f(p[1])} ${f((p[0] + q2[0]) / 2)},${f((p[1] + q2[1]) / 2)}`; }
    return d + "Z"; };
  const grainDef = (id, op = 0.07) => { def(`<filter id="${id}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.4  0 0 0 ${op} 0"/></filter>`); return `<rect width="1080" height="1920" filter="url(#${id})"/>`; };

  // ------------------------------------------------------------------ top-down kit
  const PAL = {
    dusk: { gold: ["#d4a43e", "#b88628", "#f2cf6a"], straw: "#c8a46c", stub: "#9a7a48", bund: "#d8bc84", bundHi: "#f0dca8", grass: "#7a8a3a",
      sky0: "#ffd9a0", sky1: "#f4a878", sky2: "#8a9ac8", mud: "#8a6a48", mudHi: "#b08a5e", road: "#c8a878", shadow: "rgba(40,22,10,.45)",
      sun: [-0.86, -0.5], warm: "#ffcf86", warmOp: 0.42, tint: "#ffb060", tintOp: 0.12, water: "#2a4a52", waterHi: "#ffd9a0", glow: 0.0 },
    moon: { gold: ["#5a6a5e", "#46564e", "#7e8e84"], straw: "#5a6270", stub: "#3e4652", bund: "#6e7a86", bundHi: "#9aa8b8", grass: "#34483e",
      sky0: "#c8d8f4", sky1: "#6a84b4", sky2: "#22304e", mud: "#3e3a40", mudHi: "#5a5660", road: "#5a5c66", shadow: "rgba(6,10,26,.55)",
      sun: [0.7, -0.72], warm: "#a8c4ff", warmOp: 0.22, tint: "#1a2a5a", tintOp: 0.32, water: "#0e1a2a", waterHi: "#e8f0ff", glow: 1.0 },
  };

  function field(P, r, o = {}) {
    // paddy plots on a jittered lattice, rotated a little so the bunds do not run with the frame
    const cols = 10, rows = 16, cw = 172, rh = 168, ox = -380, oy = -330, J = 22; let g = "", sh = "", bund = "";
    const pt = []; for (let j = 0; j <= rows; j++) { pt.push([]); for (let i = 0; i <= cols; i++) pt[j].push([ox + i * cw + (r() - 0.5) * J, oy + j * rh + (r() - 0.5) * J]); }
    def(`<linearGradient id="flood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${P.sky0}"/><stop offset=".55" stop-color="${P.sky1}"/><stop offset="1" stop-color="${P.sky2}"/></linearGradient>
      <linearGradient id="goldg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${P.gold[2]}"/><stop offset=".5" stop-color="${P.gold[0]}"/><stop offset="1" stop-color="${P.gold[1]}"/></linearGradient>`);
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
      const a = pt[j][i], b = pt[j][i + 1], c = pt[j + 1][i + 1], d = pt[j + 1][i], poly = `M${f(a[0])},${f(a[1])}L${f(b[0])},${f(b[1])}L${f(c[0])},${f(c[1])}L${f(d[0])},${f(d[1])}Z`;
      const t = r(), kind = o.kind ? o.kind(i, j, t) : (t < 0.58 ? "gold" : t < 0.84 ? "flood" : "cut");
      const id = `p${i}_${j}`; def(`<clipPath id="${id}"><path d="${poly}"/></clipPath>`);
      let inner = "";
      if (kind === "gold") {
        inner += `<path d="${poly}" fill="url(#goldg)"/>`;
        const ang = (r() < 0.5 ? 0 : 90) + (r() - 0.5) * 8, cx = (a[0] + c[0]) / 2, cy = (a[1] + c[1]) / 2;
        let rows2 = ""; for (let k = -16; k <= 16; k++) rows2 += `<path d="M-160,${k * 9}H160" stroke="${P.gold[1]}" stroke-width="3.4" opacity=".55"/><path d="M-160,${k * 9 - 3}H160" stroke="${P.gold[2]}" stroke-width="1.6" opacity=".55"/>`;
        inner += `<g transform="translate(${f(cx)},${f(cy)}) rotate(${f(ang)})">${rows2}</g>`;
        for (let k = 0; k < 18; k++) inner += `<circle cx="${f(a[0] + r() * cw)}" cy="${f(a[1] + r() * rh)}" r="${f(2 + r() * 3)}" fill="${P.gold[2]}" opacity=".5"/>`;
      } else if (kind === "flood") {
        inner += `<path d="${poly}" fill="url(#flood)"/>`;
        inner += `<ellipse cx="${f(a[0] + cw * (0.3 + r() * 0.4))}" cy="${f(a[1] + rh * (0.3 + r() * 0.4))}" rx="${f(40 + r() * 40)}" ry="${f(16 + r() * 12)}" fill="#fff" opacity="${P === PAL.moon ? 0.12 : 0.22}"/>`;
        for (let k = 0; k < 7; k++) for (let m = 0; m < 9; m++) inner += `<circle cx="${f(a[0] + 18 + m * 21 + (r() - 0.5) * 4)}" cy="${f(a[1] + 20 + k * 25 + (r() - 0.5) * 4)}" r="2.2" fill="${P.grass}" opacity=".8"/>`;
        for (let k = 0; k < 4; k++) inner += `<path d="M${f(a[0] + r() * cw)},${f(a[1] + r() * rh)}h${f(10 + r() * 24)}" stroke="${P.waterHi}" stroke-width="2" opacity=".55" stroke-linecap="round"/>`;
      } else {
        inner += `<path d="${poly}" fill="${P.straw}"/>`;
        for (let k = 0; k < 9; k++) for (let m = 0; m < 10; m++) inner += `<circle cx="${f(a[0] + 12 + m * 19)}" cy="${f(a[1] + 14 + k * 21)}" r="2" fill="${P.stub}" opacity=".9"/>`;
        for (let k = 0; k < (r() < 0.5 ? 1 : 0); k++) { const x = a[0] + 30 + r() * (cw - 60), y = a[1] + 30 + r() * (rh - 60);
          inner += `<ellipse cx="${f(x + 14)}" cy="${f(y + 9)}" rx="22" ry="16" fill="${P.shadow}"/><ellipse cx="${f(x)}" cy="${f(y)}" rx="26" ry="15" fill="${P.gold[0]}" stroke="${P.stub}" stroke-width="2"/><path d="M${f(x - 20)},${f(y)}h40M${f(x - 16)},${f(y - 6)}h32M${f(x - 16)},${f(y + 6)}h32" stroke="${P.gold[2]}" stroke-width="2" opacity=".7"/>`; }
      }
      // the raised bund shades the plot's edge away from the light
      const sx = -P.sun[0] * 14, sy = -P.sun[1] * 14;
      inner += `<path d="${poly}" fill="none" stroke="${P.shadow}" stroke-width="22" transform="translate(${f(sx)},${f(sy)})"/>`;
      g += `<g clip-path="url(#${id})">${inner}</g>`;
      bund += `<path d="${poly}" fill="none" stroke="${P.bund}" stroke-width="13" stroke-linejoin="round"/>`;
      sh += `<path d="${poly}" fill="none" stroke="${P.bundHi}" stroke-width="3.5" stroke-linejoin="round" transform="translate(${f(P.sun[0] * 3)},${f(P.sun[1] * 3)})" opacity=".8"/>`;
    }
    let tufts = ""; for (let k = 0; k < 420; k++) { const j = Math.floor(r() * rows), i = Math.floor(r() * cols), a = pt[j][i], b = pt[j][i + 1], u = r();
      tufts += `<circle cx="${f(a[0] + (b[0] - a[0]) * u)}" cy="${f(a[1] + (b[1] - a[1]) * u)}" r="${f(3 + r() * 4)}" fill="${P.grass}" opacity=".85"/>`; }
    return `<g transform="rotate(-9 540 960)">${g}${bund}${sh}${tufts}</g>`;
  }

  // a person seen from straight above: shadow, shoulders, head (hair / cap / straw hat), arms; facing angle `face` (rad)
  function topPerson(P, x, y, o = {}) {
    const face = o.face ?? 0, s = o.s ?? 1, L = (o.kneel ? 34 : 74) * s, [sx, sy] = [-P.sun[0], -P.sun[1]];
    const shade = `<path d="M${f(x - 7 * s)},${f(y)}L${f(x + sx * L - 9 * s * sy)},${f(y + sy * L + 9 * s * sx)}Q${f(x + sx * (L + 14 * s))},${f(y + sy * (L + 14 * s))} ${f(x + sx * L + 9 * s * sy)},${f(y + sy * L - 9 * s * sx)}L${f(x + 7 * s)},${f(y)}Z" fill="${P.shadow}"/>`;
    const deg = (face * 180) / Math.PI, shirt = o.shirt || "#d8d4c8", hair = o.hair || "#2a2220";
    let body = `<g transform="translate(${f(x)},${f(y)}) rotate(${f(deg)}) scale(${s})">`;
    if (o.kneel) body += `<ellipse cx="-12" cy="0" rx="12" ry="14" fill="${o.sarong || "#2a3a6a"}" stroke="${LINE}" stroke-width="1.6"/>`;
    body += `<ellipse cx="0" cy="0" rx="10" ry="17" fill="${shirt}" stroke="${LINE}" stroke-width="1.8"/>`;
    if (o.kneel) body += `<path d="M2,-9L16,-2M2,9L16,2" stroke="${o.skin || "#8a5a3a"}" stroke-width="5" stroke-linecap="round"/><circle cx="17" cy="0" r="3.6" fill="${o.skin || "#8a5a3a"}"/>`;
    else body += `<ellipse cx="2" cy="-18" rx="6" ry="4.5" fill="${shirt}" stroke="${LINE}" stroke-width="1.4"/><ellipse cx="2" cy="18" rx="6" ry="4.5" fill="${shirt}" stroke="${LINE}" stroke-width="1.4"/>`;
    if (o.hat) body += `<circle cx="1" cy="0" r="15" fill="#e2c88a" stroke="${LINE}" stroke-width="1.6"/><circle cx="1" cy="0" r="7" fill="#cdb070"/>`;
    else body += `<circle cx="1" cy="0" r="8.5" fill="${hair}" stroke="${LINE}" stroke-width="1.6"/>`;
    if (o.incense) body += `<path d="M18,0h14" stroke="#c8402a" stroke-width="2"/><circle cx="32" cy="0" r="2.4" fill="#ffb04a"/>`;
    return shade + body + "</g>";
  }
  const smoke = (x, y, r, P, n = 3) => { let g = ""; for (let k = 0; k < n; k++) { const dx = -P.sun[0] * 0 + 22 + k * 8, len = 70 + r() * 50;
    g += `<path d="M${f(x)},${f(y)}q${f(dx * 0.5)},${f(-len * 0.35)} ${f(dx)},${f(-len * 0.5)}t${f(dx * 0.6)},${f(-len * 0.5)}" stroke="#f4eee4" stroke-width="${f(3 + k)}" fill="none" opacity="${f(0.22 - k * 0.05)}" stroke-linecap="round"/>`; } return g; };
  const glowDot = (x, y, rad, col, op) => `<circle cx="${f(x)}" cy="${f(y)}" r="${rad}" fill="url(#glw)" opacity="${op}"/><circle cx="${f(x)}" cy="${f(y)}" r="2.6" fill="${col}"/>`;
  // a lucky-number board on an easel, seen from above at an angle so the numbers read
  const numBoard = (x, y, num, rot, P) => `<g transform="translate(${f(x)},${f(y)}) rotate(${rot})"><rect x="-40" y="10" width="80" height="18" fill="${P.shadow}" transform="skewX(-30)"/>
    <rect x="-44" y="-30" width="88" height="44" rx="4" fill="#fbf6ea" stroke="${LINE}" stroke-width="2.4"/><text x="0" y="3" text-anchor="middle" dominant-baseline="middle" font-family="Kanit" font-weight="900" font-size="30" letter-spacing="3" fill="#c42a22">${num}</text>
    <rect x="-44" y="-30" width="88" height="8" fill="#e8c860"/></g>`;
  const umbrella = (x, y, rad, P, c1 = "#c8302a", c2 = "#f4ecd8") => { let g = `<ellipse cx="${f(x - P.sun[0] * 26)}" cy="${f(y - P.sun[1] * 26)}" rx="${rad}" ry="${rad * 0.9}" fill="${P.shadow}"/>`;
    for (let k = 0; k < 10; k++) { const a0 = (k / 10) * Math.PI * 2, a1 = ((k + 1) / 10) * Math.PI * 2;
      g += `<path d="M${f(x)},${f(y)}L${f(x + Math.cos(a0) * rad)},${f(y + Math.sin(a0) * rad)}A${rad},${rad} 0 0 1 ${f(x + Math.cos(a1) * rad)},${f(y + Math.sin(a1) * rad)}Z" fill="${k % 2 ? c1 : c2}" stroke="${LINE}" stroke-width="1.6"/>`; }
    return g + `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="#2a2220"/>`; };
  const moto = (x, y, rot, P, c = "#2a5ab0") => `<g transform="translate(${f(x)},${f(y)}) rotate(${rot})"><ellipse cx="${f(-P.sun[0] * 14)}" cy="${f(-P.sun[1] * 14)}" rx="44" ry="14" fill="${P.shadow}"/>
    <rect x="-44" y="-7" width="88" height="14" rx="7" fill="#2a2a2a" stroke="${LINE}" stroke-width="1.4"/><rect x="-24" y="-12" width="44" height="24" rx="10" fill="${c}" stroke="${LINE}" stroke-width="1.6"/><path d="M30,-20V20" stroke="#3a3a3a" stroke-width="4" stroke-linecap="round"/><ellipse cx="-10" cy="0" rx="12" ry="8" fill="#1a1a1a"/></g>`;

  // the sinkhole from above: a shaft whose walls show the layers, roots, a pool at the bottom; cracks ring the ground around it
  function holeTop(P, r, cx, cy, rx, ry, o = {}) {
    const rot = o.rot ?? 0, outer = blob(r, cx, cy, rx, ry, 44, 0.07, rot); let g = "";
    // trampled mud apron and the crack rings
    g += `<path d="${blob(r, cx, cy, rx * (o.apron ?? 1.75), ry * (o.apron ?? 1.75), 40, 0.12, rot)}" fill="${P.mud}"/>`;
    g += `<path d="${blob(r, cx, cy, rx * 1.55, ry * 1.55, 40, 0.1, rot)}" fill="${P.mudHi}" opacity=".35"/>`;
    for (const k of [1.25, 1.45, 1.8]) { const a0 = r() * 6.28, span = 2.4 + r() * 2.2; let d = "";
      for (let t = 0; t <= 24; t++) { const a = a0 + (t / 24) * span, w = k * (1 + (r() - 0.5) * 0.05), x = Math.cos(a) * rx * w, y = Math.sin(a) * ry * w, c = Math.cos(rot), s = Math.sin(rot);
        d += `${t ? "L" : "M"}${f(cx + x * c - y * s + (r() - 0.5) * 6)},${f(cy + x * s + y * c + (r() - 0.5) * 6)}`; }
      g += `<path d="${d}" stroke="#1a0e08" stroke-width="5" fill="none" stroke-linejoin="round"/><path d="${d}" stroke="${P.mudHi}" stroke-width="1.6" fill="none" transform="translate(${f(P.sun[0] * 3)},${f(P.sun[1] * 3)})" opacity=".7"/>`; }
    for (let k = 0; k < 14; k++) { const a = r() * 6.28, r0 = 1.02 + r() * 0.1, r1 = r0 + 0.25 + r() * 0.4; const c = Math.cos(rot), s = Math.sin(rot);
      const P0 = [Math.cos(a) * rx * r0, Math.sin(a) * ry * r0], P1 = [Math.cos(a + 0.08) * rx * r1, Math.sin(a + 0.08) * ry * r1];
      g += `<path d="M${f(cx + P0[0] * c - P0[1] * s)},${f(cy + P0[0] * s + P0[1] * c)}L${f(cx + P1[0] * c - P1[1] * s + (r() - 0.5) * 14)},${f(cy + P1[0] * s + P1[1] * c + (r() - 0.5) * 14)}" stroke="#1a0e08" stroke-width="${f(2.5 + r() * 2.5)}" stroke-linecap="round"/>`; }
    // the walls: bands shrinking toward the bottom, offset away from the light so the lit wall shows more
    def(`<clipPath id="hc"><path d="${outer}"/></clipPath><radialGradient id="pool" cx=".45" cy=".45" r=".6"><stop offset="0" stop-color="${P.waterHi}" stop-opacity=".55"/><stop offset=".35" stop-color="${P.water}"/><stop offset="1" stop-color="#05080a"/></radialGradient>
      <linearGradient id="hsh" x1="${P.sun[0] < 0 ? 0 : 1}" y1="0" x2="${P.sun[0] < 0 ? 1 : 0}" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".78"/><stop offset=".55" stop-color="#000" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>`);
    const bands = [[1.0, "#4a3020"], [0.95, "#b8502a"], [0.83, "#c8643a"], [0.76, "#c8a070"], [0.64, "#a88a62"], [0.58, "#8e8a82"], [0.48, "#6e6c68"]];
    let w = ""; const off = [P.sun[0] * 70, P.sun[1] * 70];
    bands.forEach(([k, col], i) => { const t = i / bands.length; w += `<path d="${blob(rng(400 + i), cx + off[0] * t * 1.4, cy + off[1] * t * 1.4, rx * k, ry * k, 44, 0.06, rot)}" fill="${col}"/>`;
      if (col === "#b8502a" || col === "#c8643a") for (let m = 0; m < 30; m++) { const a = r() * 6.28, kk = k - 0.02 - r() * 0.08; w += `<circle cx="${f(cx + off[0] * t + Math.cos(a) * rx * kk)}" cy="${f(cy + off[1] * t + Math.sin(a) * ry * kk)}" r="${f(2 + r() * 3)}" fill="#7a2e16" opacity=".8"/>`; }
      if (col === "#8e8a82") for (let m = 0; m < 16; m++) { const a = r() * 6.28; w += `<path d="M${f(cx + off[0] * t + Math.cos(a) * rx * k * 0.98)},${f(cy + off[1] * t + Math.sin(a) * ry * k * 0.98)}l${f(-Math.cos(a) * 18)},${f(-Math.sin(a) * 14)}" stroke="#4e4c48" stroke-width="2"/>`; } });
    w += `<path d="${blob(rng(499), cx + off[0] * 1.5, cy + off[1] * 1.5, rx * 0.4, ry * 0.4, 36, 0.06, rot)}" fill="url(#pool)"/>`;
    def(`<radialGradient id="hdeep" cx="${f(0.5 + off[0] * 1.5 / (rx * 2.4))}" cy="${f(0.5 + off[1] * 1.5 / (ry * 2.4))}" r=".55"><stop offset=".25" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>`);
    w += `<rect x="${cx - Math.max(rx, ry) * 1.2}" y="${cy - Math.max(rx, ry) * 1.2}" width="${Math.max(rx, ry) * 2.4}" height="${Math.max(rx, ry) * 2.4}" fill="url(#hdeep)"/>`;
    // straw and a lost sandal floating on the pool
    w += `<path d="M${f(cx + off[0] * 1.5 - 20)},${f(cy + off[1] * 1.5 + 6)}l26,-8M${f(cx + off[0] * 1.5 + 8)},${f(cy + off[1] * 1.5 + 18)}l20,4" stroke="${P.gold[2]}" stroke-width="2.4" opacity=".7"/>`;
    // roots hanging from the rim into the shaft
    for (let k = 0; k < 40; k++) { const a = r() * 6.28, c = Math.cos(rot), s = Math.sin(rot), px = Math.cos(a) * rx * 0.99, py = Math.sin(a) * ry * 0.99, x0 = cx + px * c - py * s, y0 = cy + px * s + py * c;
      const len = 18 + r() * 34, dx = (cx - x0) / Math.hypot(cx - x0, cy - y0), dy = (cy - y0) / Math.hypot(cx - x0, cy - y0);
      w += `<path d="M${f(x0)},${f(y0)}q${f(dx * len * 0.5 + (r() - 0.5) * 26)},${f(dy * len * 0.5 + (r() - 0.5) * 26)} ${f(dx * len + (r() - 0.5) * 16)},${f(dy * len + (r() - 0.5) * 16)}" stroke="#3a2416" stroke-width="${f(1.6 + r() * 2.4)}" fill="none" stroke-linecap="round"/>`; }
    def(`<mask id="litm"><rect x="-200" y="-200" width="1500" height="2400" fill="#fff"/><path d="${blob(rng(77), cx + off[0] * 0.9, cy + off[1] * 0.9, rx * 0.92, ry * 0.92, 40, 0.08, rot)}" fill="#000"/></mask>`);
    const R = Math.max(rx, ry) * 1.4; w += `<rect x="${cx - R}" y="${cy - R}" width="${2 * R}" height="${2 * R}" fill="#0a0604" opacity=".82" mask="url(#litm)"/>`;
    w += `<rect x="${cx - Math.max(rx, ry) * 1.2}" y="${cy - Math.max(rx, ry) * 1.2}" width="${Math.max(rx, ry) * 2.4}" height="${Math.max(rx, ry) * 2.4}" fill="url(#hsh)" opacity=".5"/>`;
    g += `<g clip-path="url(#hc)">${w}</g>`;
    // a torn grass lip overhanging the edge
    g += `<path d="${outer}" fill="none" stroke="${P.grass}" stroke-width="9" stroke-dasharray="3 7" stroke-linecap="round"/><path d="${outer}" fill="none" stroke="#2a1a10" stroke-width="2.4"/>`;
    return g;
  }

  function drone(P, moon) {
    const r = rng(moon ? 5 : 5); let g = "";
    def(`<radialGradient id="glw"><stop offset="0" stop-color="#ffc870" stop-opacity=".9"/><stop offset="1" stop-color="#ffc870" stop-opacity="0"/></radialGradient>`);
    g += field(P, r);
    // a dirt track along the left and a farm path to the hole
    g += `<path d="M-60,1500C200,1380 260,1180 330,980S460,620 520,-40" stroke="${P.shadow}" stroke-width="86" fill="none" transform="translate(${f(-P.sun[0] * 10)},${f(-P.sun[1] * 10)})"/>
      <path d="M-60,1500C200,1380 260,1180 330,980S460,620 520,-40" stroke="${P.road}" stroke-width="78" fill="none"/>
      <path d="M-60,1500C200,1380 260,1180 330,980S460,620 520,-40" stroke="${P.mudHi}" stroke-width="3" fill="none" stroke-dasharray="14 18" opacity=".6"/>`;
    const cx = 610, cy = 1010, rx = 200, ry = 168;
    g += holeTop(P, r, cx, cy, rx, ry);
    // the lure: offering mat, incense urns, candles, garlands, lucky-number boards, a stall, motorbikes
    g += `<g transform="translate(700,1290) rotate(-12)"><rect x="-120" y="-34" width="240" height="68" rx="6" fill="${P.shadow}" transform="translate(${f(-P.sun[0] * 12)},${f(-P.sun[1] * 12)})"/>
      <rect x="-120" y="-34" width="240" height="68" rx="6" fill="#c8302a" stroke="${LINE}" stroke-width="2"/><rect x="-112" y="-26" width="224" height="52" fill="none" stroke="#f0c040" stroke-width="3" stroke-dasharray="10 6"/>
      ${[-80, -30, 20, 70].map((x, k) => `<circle cx="${x}" cy="0" r="17" fill="${["#f2b632", "#f4ecd8", "#e8762a", "#f2b632"][k]}" stroke="${LINE}" stroke-width="1.6"/><circle cx="${x}" cy="0" r="8" fill="${["#e8762a", "#e8c860", "#f2b632", "#c8402a"][k]}"/>`).join("")}
      ${[-100, 100].map((x) => `<circle cx="${x}" cy="0" r="9" fill="#f4ecd8" stroke="${LINE}" stroke-width="1.4"/>`).join("")}</g>`;
    const urns = [[590, 1240], [800, 1205], [470, 1210]];
    urns.forEach(([x, y]) => { g += `<ellipse cx="${f(x - P.sun[0] * 10)}" cy="${f(y - P.sun[1] * 10)}" rx="20" ry="16" fill="${P.shadow}"/><circle cx="${x}" cy="${y}" r="17" fill="#a8823a" stroke="${LINE}" stroke-width="2"/><circle cx="${x}" cy="${y}" r="11" fill="#5a4a32"/>`;
      for (let k = 0; k < 7; k++) g += glowDot(x + (r() - 0.5) * 16, y + (r() - 0.5) * 16, 14, "#ffb04a", moon ? 0.9 : 0.5);
      g += smoke(x, y, r, P, 3); });
    // candles on the mat and at the rim: warm pools that read strongly at night
    [[640, 1278], [760, 1300], [520, 1185], [870, 1150], [900, 1060]].forEach(([x, y]) => { g += glowDot(x, y, moon ? 40 : 18, "#fff2c0", moon ? 0.85 : 0.5); });
    g += numBoard(860, 1340, "4 2 7", -8, P) + numBoard(420, 1300, "9 1 8", 10, P) + numBoard(930, 860, "7 7 3", -20, P);
    g += umbrella(960, 1500, 70, P) + umbrella(810, 1580, 58, P, "#2a6ab0", "#f4ecd8") + umbrella(160, 1180, 54, P, "#e8a020", "#f4ecd8");
    g += moto(230, 1420, -60, P, "#c8302a") + moto(290, 1500, -50, P) + moto(150, 1560, -70, P, "#4a4a4a") + moto(330, 860, -82, P, "#2a8a5a");
    // the crowd at the rim: kneeling with incense facing the hole, standing to look in, a child peering over the edge
    const crowd = [];
    for (let k = 0; k < 13; k++) { const a = 0.15 + (k / 13) * 2.6; const R = 1.18 + r() * 0.12; crowd.push([cx + Math.cos(a) * rx * R, cy + Math.sin(a) * ry * R, a, k % 3 === 0 ? "stand" : "kneel"]); }
    for (let k = 0; k < 6; k++) { const a = 3.4 + k * 0.38; const R = 1.3 + r() * 0.2; crowd.push([cx + Math.cos(a) * rx * R, cy + Math.sin(a) * ry * R, a, "stand"]); }
    const shirts = ["#e8e2d4", "#3a5a9a", "#c84a3a", "#e8c860", "#5a8a5a", "#f4f0e8", "#8a4a8a", "#2a2a2a", "#d87a3a"];
    crowd.forEach(([x, y, a, pose], k) => { g += topPerson(P, x, y, { face: a + Math.PI, kneel: pose === "kneel", shirt: shirts[k % shirts.length], hair: k % 5 === 0 ? "#e8e4dc" : "#2a2220", hat: k % 7 === 3, incense: pose === "kneel" && k % 2 === 0, s: 1.55 });
      if (pose === "kneel" && k % 2 === 0) g += smoke(x + Math.cos(a + Math.PI) * 38, y + Math.sin(a + Math.PI) * 38, r, P, 2); });
    g += topPerson(P, cx + rx * 0.88, cy - ry * 0.62, { face: 2.6, shirt: "#e84a3a", hair: "#2a2220", s: 1.2 }); // a child at the very lip
    // walking in along the track
    [[300, 1120, -1.2], [345, 1040, -1.25], [380, 700, -1.3]].forEach(([x, y, a], k) => { g += topPerson(P, x, y, { face: a, shirt: shirts[(k + 4) % 9], s: 1.5, hat: k === 1 }); });
    // light: low warm sun from the upper left (dusk) or a cold moon from the upper right (night) with warm candle pools
    def(`<radialGradient id="sunL" cx="${moon ? 1.05 : -0.05}" cy="-0.05" r="1.15"><stop offset="0" stop-color="${P.warm}" stop-opacity="${P.warmOp}"/><stop offset="1" stop-color="${P.warm}" stop-opacity="0"/></radialGradient>
      <radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="${moon ? 0.7 : 0.5}"/></radialGradient>`);
    g += `<rect width="1080" height="1920" fill="${P.tint}" opacity="${P.tintOp}" style="mix-blend-mode:multiply"/><rect width="1080" height="1920" fill="url(#sunL)" style="mix-blend-mode:screen"/>`;
    if (moon) [[640, 1278], [760, 1300], [520, 1185], [870, 1150], [900, 1060], [590, 1240], [800, 1205], [470, 1210], [960, 1500]].forEach(([x, y]) => { g += `<circle cx="${x}" cy="${y}" r="90" fill="url(#glw)" opacity=".35" style="mix-blend-mode:screen"/>`; });
    def(`<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.warm}" stop-opacity="${moon ? 0.25 : 0.4}"/><stop offset=".3" stop-color="${P.warm}" stop-opacity="0"/></linearGradient>`);
    g += `<rect width="1080" height="1920" fill="url(#haze)"/><rect width="1080" height="1920" fill="url(#vig)"/>` + grainDef("gr");
    return g;
  }

  // ------------------------------------------------------------------ measuring (G1 p.28: an elongated hole grows along its length, so the ends are cordoned further out)
  function measure(note, far100) {
    const P = PAL.dusk, r = rng(31); let g = "";
    def(`<radialGradient id="glw"><stop offset="0" stop-color="#ffc870" stop-opacity=".9"/><stop offset="1" stop-color="#ffc870" stop-opacity="0"/></radialGradient>`);
    g += field(P, r, { kind: (i, j, t) => (t < 0.7 ? "cut" : t < 0.9 ? "gold" : "flood") });
    // scale: 30 px = 1 m · hole 10.2 m long (axis tilted 12° off vertical) × 4.1 m wide · cordon 10 m off the sides, 18 m off the ends
    const cx = 540, cy = 980, rot = (86 * Math.PI) / 180, M = 32, L = 5.1 * M, W = 2.05 * M;
    g += holeTop(P, r, cx, cy, L, W, { rot, apron: 1.35 });
    const c = Math.cos(rot), s = Math.sin(rot), at = (u, v) => [cx + u * c - v * s, cy + u * s + v * c];
    // red rope: a stretched octagon, 18 m beyond each end along the axis, 10 m beyond each side
    const ue = L + 18 * M, ve = W + 10 * M, poly = [[ue, 0], [ue * 0.72, ve], [-ue * 0.72, ve], [-ue, 0], [-ue * 0.72, -ve], [ue * 0.72, -ve]].map(([u, v]) => at(u, v));
    g += `<path d="M${poly.map(([x, y]) => `${f(x + 6)},${f(y + 5)}`).join("L")}Z" stroke="rgba(40,22,10,.4)" stroke-width="7" fill="none"/><path d="M${poly.map(([x, y]) => `${f(x)},${f(y)}`).join("L")}Z" stroke="#d8241e" stroke-width="6" fill="none"/>`;
    poly.forEach(([x, y]) => { g += `<ellipse cx="${f(x + 12)}" cy="${f(y + 8)}" rx="12" ry="6" fill="${P.shadow}"/><circle cx="${f(x)}" cy="${f(y)}" r="8" fill="#6a4228" stroke="${LINE}" stroke-width="2"/>`; });
    // warning signs on the rope, four sides
    [[0, ve], [0, -ve], [ue * 0.86, ve * 0.4], [-ue * 0.86, -ve * 0.4]].forEach(([u, v], k) => { const [x, y] = at(u, v);
      g += `<g transform="translate(${f(x)},${f(y)})"><rect x="-34" y="-20" width="68" height="40" rx="4" fill="#ffd23a" stroke="${LINE}" stroke-width="2"/><text x="0" y="1" text-anchor="middle" dominant-baseline="middle" font-family="Kanit" font-weight="900" font-size="20" fill="#1e1712">ห้ามเข้า</text></g>`; });
    // the tape along the length (end stake to end stake) and the knotted rope across the width
    const e0 = at(-L - 14, 0), e1 = at(L + 14, 0), w0 = at(0, -W - 14), w1 = at(0, W + 14);
    g += `<path d="M${f(e0[0])},${f(e0[1])}L${f(e1[0])},${f(e1[1])}" stroke="#f2c820" stroke-width="7"/>`;
    for (let k = 0; k <= 10; k++) { const [x, y] = at(-L - 14 + k * ((2 * L + 28) / 10), 0); g += `<path d="M${f(x - s * 7)},${f(y + c * 7)}L${f(x + s * 7)},${f(y - c * 7)}" stroke="#1e1712" stroke-width="2"/>`; }
    g += `<path d="M${f(w0[0])},${f(w0[1])}L${f(w1[0])},${f(w1[1])}" stroke="#e8dcc0" stroke-width="5"/>`;
    for (let k = 0; k <= 4; k++) { const [x, y] = at(0, -W - 14 + k * ((2 * W + 28) / 4)); g += `<circle cx="${f(x)}" cy="${f(y)}" r="6" fill="#c8b890" stroke="${LINE}" stroke-width="1.6"/>`; }
    // wooden stakes with painted tags (numbers live only on stakes, the tape case and the notebook)
    const plank = (x, y, txt) => `<g transform="translate(${f(x)},${f(y)}) rotate(-7)"><rect x="-94" y="-24" width="196" height="58" rx="6" fill="rgba(40,22,10,.45)"/>
      <rect x="-100" y="-30" width="200" height="58" rx="6" fill="#9a6a3c" stroke="${LINE}" stroke-width="2.6"/>${[-14, 0, 14].map((d) => `<path d="M-92,${d}Q0,${d + 4} 92,${d - 2}" stroke="#7a4e2a" stroke-width="2" fill="none" opacity=".7"/>`).join("")}
      <circle cx="-86" cy="-16" r="3.5" fill="#3a2a1a"/><circle cx="86" cy="14" r="3.5" fill="#3a2a1a"/>
      <text x="0" y="2" text-anchor="middle" dominant-baseline="middle" font-family="Kanit" font-weight="900" font-size="30" fill="#fbf4e2">${txt}</text></g>`;
    const stake = (x, y, txt, dx, dy) => `<ellipse cx="${f(x + 10)}" cy="${f(y + 7)}" rx="10" ry="5" fill="${P.shadow}"/><rect x="${f(x - 7)}" y="${f(y - 7)}" width="14" height="14" fill="#8a5a32" stroke="${LINE}" stroke-width="2"/>${txt ? plank(x + dx * 0.42, y + dy * 0.42, txt) : ""}`;
    const ax = [c, s], pr = [-s, c], tg = (p0, v, d) => stake(p0[0], p0[1], v, d[0], d[1]);
    g += stake(e0[0], e0[1], "", 0, 0) + stake(e1[0], e1[1], "", 0, 0) + stake(w0[0], w0[1], "", 0, 0) + stake(w1[0], w1[1], "", 0, 0);
    g += plank(e0[0] + 10, e0[1] - 92, "ทิศเหนือ ↑") + plank(e1[0] + 20, e1[1] + 96, "ยาว 10.2 ม.") + plank(w0[0] - 196, w0[1] + 6, "กว้าง 4.1 ม.");
    // the officials (hard hats) holding the tape and the rope, one writing; villagers kept behind the rope
    const off = (x, y, face, k, o = {}) => topPerson(P, x, y, { face, shirt: "#e8822a", hair: "#f4f0e8", s: 1.3, ...o }) + `<circle cx="${f(x + 1)}" cy="${f(y)}" r="9" fill="#f4f0e8" stroke="${LINE}" stroke-width="1.4"/>`;
    const tE0 = at(-L - 40, 0), tE1 = at(L + 40, 0), tW0 = at(0, -W - 40), tW1 = at(0, W + 40);
    g += off(tE0[0], tE0[1], rot, 0) + off(tE1[0], tE1[1], rot + Math.PI, 1) + off(tW0[0], tW0[1], rot + Math.PI / 2, 2) + off(tW1[0], tW1[1], rot - Math.PI / 2, 3);
    const wr = at(-60, W + 120); g += off(wr[0], wr[1], rot - Math.PI / 2, 4);
    g += `<g transform="translate(${f(wr[0] + 26)},${f(wr[1] - 14)}) rotate(-20)"><rect x="-14" y="-10" width="28" height="20" fill="#f4f0e4" stroke="${LINE}" stroke-width="1.6"/><path d="M0,-10V10" stroke="${LINE}" stroke-width="1"/></g>`;
    // the tape case on the ground by the south stake
    g += `<g transform="translate(${f(e0[0] - 46)},${f(e0[1] + 34)})"><circle r="20" fill="#f2c820" stroke="${LINE}" stroke-width="2.4"/><circle r="7" fill="#2a2a2a"/></g>`;
    // villagers behind the rope, two still holding incense
    const shirts = ["#e8e2d4", "#3a5a9a", "#c84a3a", "#5a8a5a", "#f4f0e8", "#8a4a8a"];
    [[ue * 0.4, ve + 70], [ue * 0.2, ve + 80], [-ue * 0.1, ve + 74], [-ue * 0.45, ve + 64], [ue * 0.3, -ve - 70], [-ue * 0.3, -ve - 76]].forEach(([u, v], k) => { const [x, y] = at(u, v);
      g += topPerson(P, x, y, { face: Math.atan2(cy - y, cx - x), shirt: shirts[k], s: 1.2, incense: k < 2, hat: k === 3 }); });
    def(`<radialGradient id="sunL" cx="-0.05" cy="-0.05" r="1.15"><stop offset="0" stop-color="${P.warm}" stop-opacity=".38"/><stop offset="1" stop-color="${P.warm}" stop-opacity="0"/></radialGradient>
      <radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>`);
    g += `<rect width="1080" height="1920" fill="${P.tint}" opacity="${P.tintOp}" style="mix-blend-mode:multiply"/><rect width="1080" height="1920" fill="url(#sunL)" style="mix-blend-mode:screen"/><rect width="1080" height="1920" fill="url(#vig)"/>`;
    if (!note) return g + grainDef("gr");
    // insert: the official's notebook and the tape case, close on a clipboard in warm light
    let n = `<rect width="1080" height="1920" fill="#3a2a1c"/>`;
    for (let k = 0; k < 40; k++) n += `<path d="M0,${k * 52 + (k % 3) * 6}H1080" stroke="#4a3624" stroke-width="${f(8 + r() * 10)}" opacity=".6"/>`;
    n += `<g transform="translate(540,900) rotate(-6)"><rect x="-372" y="-552" width="760" height="1100" rx="18" fill="rgba(0,0,0,.45)"/><rect x="-380" y="-560" width="760" height="1100" rx="18" fill="#7a5232" stroke="${LINE}" stroke-width="4"/>
      <rect x="-330" y="-480" width="660" height="960" fill="#f8f2e2" stroke="${LINE}" stroke-width="3"/>${Array.from({ length: 15 }, (_, k) => `<path d="M-300,${-380 + k * 60}H300" stroke="#9ab8d8" stroke-width="2"/>`).join("")}
      <rect x="-110" y="-590" width="220" height="70" rx="12" fill="#b8bcc2" stroke="${LINE}" stroke-width="4"/>
      <g font-family="Mali" font-weight="700" fill="#1e2a5a">
        <text x="-290" y="-400" font-size="44">หลุมยุบ ทุ่งโนนนาค</text>
        <text x="-290" y="-280" font-size="48">ยาว 10.2 ม. (เหนือ–ใต้)</text>
        <text x="-290" y="-160" font-size="48">กว้าง 4.1 ม.</text>
        <text x="-290" y="-40" font-size="44">รูปร่าง: แนวยาว</text>
        <text x="-290" y="40" font-size="40">→ จะขยายไปตามแนวยาว</text>
        <text x="-290" y="160" font-size="44">กันข้าง 10 ม.</text>
        <text x="-290" y="280" font-size="44">กันปลาย 2 ข้าง 18 ม.</text>
      </g>
      <path d="M-300,190" /><ellipse cx="30" cy="330" rx="250" ry="26" fill="none" stroke="#c42a22" stroke-width="5" transform="rotate(-2 30 330)"/>
      ${far100 ? `<text x="-290" y="410" font-family="Mali" font-weight="700" font-size="46" fill="#c42a22">ห่างหลุมอย่างน้อย 100 ม.</text><path d="M-296,436q300,16 610,-4" stroke="#c42a22" stroke-width="5" fill="none" stroke-linecap="round"/>`
        : `<g transform="translate(150,420)"><ellipse cx="0" cy="0" rx="150" ry="40" fill="none" stroke="#1e2a5a" stroke-width="4"/><path d="M-150,0H-210M150,0H210" stroke="#1e2a5a" stroke-width="4"/><path d="M-210,0l16,-10v20zM210,0l-16,-10v20z" fill="#1e2a5a"/></g>`}</g>`;
    n += `<g transform="translate(860,1600) rotate(14)"><ellipse cx="14" cy="18" rx="150" ry="140" fill="rgba(0,0,0,.45)"/><circle r="140" fill="#f2c820" stroke="${LINE}" stroke-width="5"/><circle r="104" fill="#e0b414" stroke="${LINE}" stroke-width="3"/><circle r="30" fill="#2a2a2a"/>
      <path d="M-20,-140h-360v58h360z" fill="#f8e070" stroke="${LINE}" stroke-width="3"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-30 - k * 12},-140v${k % 5 ? 14 : 26}" stroke="${LINE}" stroke-width="2"/>`).join("")}
      <text x="-260" y="-96" font-family="Kanit" font-weight="900" font-size="30" fill="#c42a22">10</text></g>`;
    n += `<g transform="translate(260,1660) rotate(-38)"><rect x="-16" y="-220" width="32" height="400" rx="8" fill="#2a5ab0" stroke="${LINE}" stroke-width="3"/><path d="M-16,180l16,40l16,-40z" fill="#e8c8a0" stroke="${LINE}" stroke-width="3"/></g>`;
    def(`<radialGradient id="lamp" cx=".3" cy=".2" r=".9"><stop offset="0" stop-color="#ffd890" stop-opacity=".45"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>`);
    return n + `<rect width="1080" height="1920" fill="url(#lamp)" style="mix-blend-mode:screen"/><rect width="1080" height="1920" fill="url(#vig)"/>` + grainDef("gr", 0.09);
  }

  // ------------------------------------------------------------------ the depth move: one tall world (1080 × 7400), the camera travels down it
  function depthWorld() {
    const r = rng(77); let g = "";
    const SURF = 2300, H = 7400;
    def(`<linearGradient id="dsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a6a"/><stop offset=".45" stop-color="#d87a6a"/><stop offset=".8" stop-color="#ffc888"/><stop offset="1" stop-color="#ffe2a8"/></linearGradient>
      <radialGradient id="dsun" cx=".72" cy=".86" r=".35"><stop offset="0" stop-color="#fff2c8" stop-opacity="1"/><stop offset=".3" stop-color="#ffd890" stop-opacity=".6"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>`);
    g += `<rect y="0" width="1080" height="${SURF}" fill="url(#dsky)"/><rect y="0" width="1080" height="${SURF}" fill="url(#dsun)"/>`;
    // clouds lit from below, birds, a kite: the first frame is sky
    for (let k = 0; k < 9; k++) { const x = r() * 1200 - 60, y = 300 + r() * 1500, w = 160 + r() * 260;
      g += `<g opacity="${f(0.55 + r() * 0.35)}"><ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(w)}" ry="${f(w * 0.22)}" fill="#f4c8a8"/><ellipse cx="${f(x - w * 0.2)}" cy="${f(y - w * 0.12)}" rx="${f(w * 0.5)}" ry="${f(w * 0.2)}" fill="#ffe0c0"/><ellipse cx="${f(x)}" cy="${f(y + w * 0.12)}" rx="${f(w * 0.9)}" ry="${f(w * 0.08)}" fill="#c87a78" opacity=".6"/></g>`; }
    for (let k = 0; k < 7; k++) { const x = 200 + r() * 600, y = 700 + r() * 500; g += `<path d="M${f(x)},${f(y)}q10,-8 20,0q10,-8 20,0" stroke="#3a2a3a" stroke-width="3" fill="none"/>`; }
    g += `<g transform="translate(300,520) rotate(-14)"><path d="M0,-60L44,0L0,70L-44,0Z" fill="#c8302a" stroke="${LINE}" stroke-width="3"/><path d="M0,-60V70M-44,0H44" stroke="${LINE}" stroke-width="2"/><path d="M0,70q-30,120 30,240t-20,260" stroke="${LINE}" stroke-width="2" fill="none"/></g>`;
    // the horizon: karst hills, sugar palms, the village roofs
    g += `<path d="M0,${SURF - 260}Q120,${SURF - 420} 220,${SURF - 300}Q300,${SURF - 520} 420,${SURF - 330}Q540,${SURF - 380} 640,${SURF - 300}Q760,${SURF - 560} 880,${SURF - 320}Q980,${SURF - 400} 1080,${SURF - 290}V${SURF}H0Z" fill="#8a6a8a" opacity=".75"/>`;
    for (let k = 0; k < 10; k++) { const x = 40 + k * 110 + (r() - 0.5) * 40, y = SURF - 150; g += `<path d="M${f(x)},${y + 60}V${f(y - 60)}" stroke="#4a3a4a" stroke-width="6"/><circle cx="${f(x)}" cy="${f(y - 66)}" r="26" fill="#3a4a3a"/>`; }
    // the surface plane seen at a low angle: paddies receding toward the horizon, the hole's mouth, people on the rim
    def(`<linearGradient id="plane" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8924a"/><stop offset="1" stop-color="#d4a43e"/></linearGradient>`);
    g += `<path d="M0,${SURF - 150}H1080V${SURF}H0Z" fill="url(#plane)"/>`;
    for (let k = 0; k < 7; k++) { const y = SURF - 130 + k * k * 2.6 + k * 3; g += `<path d="M0,${f(y)}H1080" stroke="#e0c890" stroke-width="${f(1 + k * 0.6)}" opacity=".8"/>`; }
    for (let k = -8; k <= 8; k++) g += `<path d="M${540 + k * 30},${SURF - 130}L${540 + k * 200},${SURF}" stroke="#e0c890" stroke-width="2" opacity=".6"/>`;
    g += `<path d="M0,${SURF - 60}H1080" stroke="#ffe4a0" stroke-width="2" opacity=".4"/>`;
    // the hole's mouth on the plane and the shaft cut open in front
    const HX = 560, HW = 300; // mouth centre and width at the surface
    g += `<ellipse cx="${HX}" cy="${SURF - 18}" rx="${HW / 2 + 24}" ry="30" fill="#6a4a2e"/><ellipse cx="${HX}" cy="${SURF - 14}" rx="${HW / 2}" ry="24" fill="#120a06"/>`;
    // people on the rim (small, side view silhouettes against the sunset) with incense smoke
    for (let k = 0; k < 7; k++) { const x = HX - 330 + k * 92 + (k > 2 ? 180 : 0), y = SURF - 30 - (k % 2) * 8, kneel = k % 3 === 1;
      g += `<g transform="translate(${x},${y}) scale(1.7) translate(${-x},${-y})">` + (kneel ? `<path d="M${x - 10},${y}q0,-22 10,-26q12,-2 14,26z" fill="#2a1e22"/><circle cx="${x + 2}" cy="${y - 34}" r="7" fill="#2a1e22"/><path d="M${x + 12},${y - 22}l12,-4" stroke="#2a1e22" stroke-width="4"/><path d="M${x + 24},${y - 26}q8,-30 -4,-60" stroke="#f4eee4" stroke-width="2.5" fill="none" opacity=".4"/>`
        : `<path d="M${x - 8},${y}l3,-34h10l3,34z" fill="#2a1e22"/><path d="M${x - 9},${y - 34}q9,-20 18,0z" fill="#2a1e22"/><circle cx="${x}" cy="${y - 48}" r="7.5" fill="#2a1e22"/>`) + "</g>"; }
    // ---- the cut face: layers with texture, lit by the shaft of light from the mouth
    const L1 = SURF, L2 = SURF + 300, L3 = SURF + 900, L4 = SURF + 1700, CAVE0 = SURF + 2500, WT = SURF + 3900, CAVE1 = SURF + 4500;
    const shaft = (y) => { // half-width of the shaft at depth y (narrows, then opens into the cave roof)
      if (y < CAVE0) return HW / 2 - (y - SURF) * 0.04 + Math.sin(y / 90) * 10; return 0; };
    const layer = (y0, y1, base, dots, seed) => { const rr = rng(seed); let s = `<rect x="0" y="${y0}" width="1080" height="${y1 - y0}" fill="${base[0]}"/>`;
      s += `<rect x="0" y="${y0}" width="1080" height="${y1 - y0}" fill="url(#lgr${seed})"/>`; def(`<linearGradient id="lgr${seed}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${base[1]}" stop-opacity=".0"/><stop offset="1" stop-color="${base[1]}" stop-opacity=".55"/></linearGradient>`);
      for (let k = 0; k < dots.n; k++) { const x = rr() * 1080, y = y0 + rr() * (y1 - y0), sz = dots.r[0] + rr() * (dots.r[1] - dots.r[0]);
        s += dots.kind === "pebble" ? `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(sz)}" ry="${f(sz * 0.7)}" fill="${dots.c[k % dots.c.length]}" stroke="rgba(0,0,0,.35)" stroke-width="1.4"/>`
          : dots.kind === "nod" ? `<path d="${blob(rr, x, y, sz, sz * 0.8, 8, 0.25)}" fill="${dots.c[k % dots.c.length]}"/>`
          : `<path d="M${f(x)},${f(y)}l${f((rr() - 0.5) * sz * 4)},${f(sz)}" stroke="${dots.c[k % dots.c.length]}" stroke-width="2" opacity=".6"/>`; }
      // a wavy contact line on top of the layer
      let d = `M0,${y0}`; for (let x = 0; x <= 1080; x += 40) d += `L${x},${f(y0 + Math.sin(x / 70 + seed) * 8 + (rr() - 0.5) * 6)}`;
      s += `<path d="${d}" stroke="rgba(0,0,0,.35)" stroke-width="4" fill="none"/>`; return s; };
    g += layer(L1, L2, ["#5a3a24", "#2a1a10"], { kind: "streak", n: 260, r: [6, 14], c: ["#7a5236", "#3a2416", "#8a6a3a"] }, 1);    // paddy soil, roots
    g += layer(L2, L3, ["#b8502a", "#6a2410"], { kind: "nod", n: 420, r: [5, 16], c: ["#8a2e16", "#d8743a", "#6a2210"] }, 2);   // laterite (ศิลาแลง) nodules
    g += layer(L3, L4, ["#c8a070", "#7a5a38"], { kind: "pebble", n: 360, r: [3, 9], c: ["#e0c49a", "#a88458", "#f0dcb4"] }, 3);  // sandy clay
    g += layer(L4, H, ["#9a968c", "#3e3c38"], { kind: "streak", n: 300, r: [10, 26], c: ["#6e6a62", "#c8c4b8", "#5a5650"] }, 4);  // limestone
    // bedding planes and joints in the limestone
    for (let k = 0; k < 12; k++) { const y = L4 + 80 + k * 140 + (r() - 0.5) * 30; g += `<path d="M0,${f(y)}Q270,${f(y + 14)} 540,${f(y - 6)}T1080,${f(y + 8)}" stroke="rgba(30,28,24,.5)" stroke-width="3" fill="none"/>`; }
    for (let k = 0; k < 26; k++) { const x = r() * 1080, y = L4 + r() * (H - L4); g += `<path d="M${f(x)},${f(y)}l${f((r() - 0.5) * 30)},${f(60 + r() * 120)}" stroke="rgba(30,28,24,.45)" stroke-width="2.5"/>`; }
    // roots from the paddy above reaching down into the laterite
    for (let k = 0; k < 40; k++) { const x = r() * 1080, len = 120 + r() * 380; let d = `M${f(x)},${L1}`; let px = x;
      for (let y = L1; y < L1 + len; y += 30) { px += (r() - 0.5) * 22; d += `L${f(px)},${f(y)}`; } g += `<path d="${d}" stroke="#2e1c10" stroke-width="${f(1.4 + r() * 3)}" fill="none" opacity=".75"/>`; }
    // the shaft: the open hole cut in half, dark inside, its walls catching the light
    let sl = `M${HX - HW / 2},${SURF - 14}`, sr = `M${HX + HW / 2},${SURF - 14}`, pts = [];
    for (let y = SURF; y <= CAVE0; y += 40) pts.push([y, shaft(y)]);
    pts.forEach(([y, w]) => { sl += `L${f(HX - w)},${y}`; });
    pts.forEach(([y, w]) => { sr += `L${f(HX + w)},${y}`; });
    const shp = `${sl}L${HX + shaft(CAVE0 - 40)},${CAVE0}${pts.slice().reverse().map(([y, w]) => `L${f(HX + w)},${y}`).join("")}Z`;
    def(`<linearGradient id="shaftG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1008"/><stop offset="1" stop-color="#05040a"/></linearGradient>`);
    def(`<clipPath id="shc"><path d="${shp}"/></clipPath>
      <linearGradient id="cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".5" stop-color="#000" stop-opacity=".72"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>
      <linearGradient id="mouthL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffcf86" stop-opacity=".55"/><stop offset=".3" stop-color="#ffcf86" stop-opacity=".12"/><stop offset="1" stop-color="#ffcf86" stop-opacity="0"/></linearGradient>`);
    let bw = "";
    [[L1, L2, "#3a2618"], [L2, L3, "#7a3218"], [L3, L4, "#8a6a48"], [L4, CAVE0 + 40, "#5e5a54"]].forEach(([a, b, col]) => { bw += `<rect x="${HX - HW}" y="${a}" width="${HW * 2}" height="${b - a}" fill="${col}"/>`; });
    for (let k = 0; k < 140; k++) { const y = SURF + r() * (CAVE0 - SURF), x = HX + (r() - 0.5) * HW * 1.6; bw += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(3 + r() * 7)}" ry="${f(2 + r() * 4)}" fill="#000" opacity=".25"/>`; }
    for (let k = 0; k < 9; k++) { const y = SURF + 260 + k * 250; bw += `<path d="M${HX - HW},${y}Q${HX},${y + 40} ${HX + HW},${y}" stroke="#000" stroke-width="3" fill="none" opacity=".35"/>`; }
    bw += `<rect x="${HX - HW}" y="${SURF - 20}" width="${HW * 2}" height="${CAVE0 - SURF + 60}" fill="url(#cyl)"/><rect x="${HX - HW}" y="${SURF - 20}" width="${HW * 2}" height="${CAVE0 - SURF + 60}" fill="url(#mouthL)" style="mix-blend-mode:screen"/>`;
    g += `<g clip-path="url(#shc)">${bw}</g><path d="${sl}" stroke="#ffd890" stroke-width="3" fill="none" opacity=".35"/><path d="${sr}" stroke="#1a0e08" stroke-width="5" fill="none" opacity=".6"/>`;
    // hanging roots, a crumbling lip and falling clods inside the shaft
    for (let k = 0; k < 18; k++) { const side = k % 2 ? 1 : -1, y = SURF + 30 + r() * 900, x = HX + side * shaft(y); let d = `M${f(x)},${f(y)}`, px = x;
      for (let t = 0; t < 6; t++) { px += -side * (6 + r() * 10); d += `L${f(px)},${f(y + t * 26)}`; } g += `<path d="${d}" stroke="#2e1c10" stroke-width="${f(1.4 + r() * 2)}" fill="none"/>`; }
    for (let k = 0; k < 10; k++) { const y = SURF + 200 + r() * 2000, x = HX + (r() - 0.5) * shaft(y) * 1.2; g += `<path d="${blob(r, x, y, 6 + r() * 8, 5 + r() * 6, 7, 0.3)}" fill="#6a4228" stroke="rgba(0,0,0,.4)" stroke-width="1.2"/>`; }
    // ---- the cave: a wide chamber in the limestone, its roof hung with stalactites, the groundwater below
    const caveP = [[-60, CAVE0 + 300], [120, CAVE0 + 140], [330, CAVE0 + 60], [HX - 50, CAVE0], [HX + 60, CAVE0 + 4], [780, CAVE0 + 90], [1000, CAVE0 + 180], [1150, CAVE0 + 500], [1150, WT + 600], [880, CAVE1 + 80], [560, CAVE1 + 120], [240, CAVE1 + 60], [-70, WT + 500], [-80, CAVE0 + 900]];
    const rough = []; caveP.forEach((p, k) => { const q2 = caveP[(k + 1) % caveP.length]; for (let t = 0; t < 1; t += 0.2) rough.push([p[0] + (q2[0] - p[0]) * t + (r() - 0.5) * 50, p[1] + (q2[1] - p[1]) * t + (r() - 0.5) * 50]); });
    caveP.length = 0; rough.forEach((p) => caveP.push(p));
    let cd = `M${caveP[0][0]},${caveP[0][1]}`; for (let k = 1; k <= caveP.length; k++) { const p = caveP[k % caveP.length], q2 = caveP[(k + 1) % caveP.length]; cd += `Q${p[0]},${p[1]} ${f((p[0] + q2[0]) / 2)},${f((p[1] + q2[1]) / 2)}`; }
    def(`<clipPath id="cavec"><path d="${cd}Z"/></clipPath>
      <radialGradient id="caveL" cx="${HX / 1080}" cy="0" r="1"><stop offset="0" stop-color="#6a604c"/><stop offset=".45" stop-color="#2a261e"/><stop offset="1" stop-color="#0a0a0c"/></radialGradient>
      <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6a8" stop-opacity=".6"/><stop offset="1" stop-color="#ffe6a8" stop-opacity="0"/></linearGradient>
      <linearGradient id="gw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e5662"/><stop offset=".4" stop-color="#0c2a34"/><stop offset="1" stop-color="#03080c"/></linearGradient>`);
    g += `<path d="${cd}Z" fill="url(#caveL)" stroke="#2a2824" stroke-width="10"/>`;
    let cave = "";
    // the far wall: flowstone curtains catching the light
    for (let k = 0; k < 16; k++) { const x = 80 + k * 60 + (r() - 0.5) * 20, y = CAVE0 + 200 + r() * 400, h = 300 + r() * 600;
      cave += `<path d="M${f(x)},${f(y)}q${f(18 + r() * 10)},${f(h * 0.5)} 0,${f(h)}q${f(-12)},${f(-h * 0.5)} 0,${f(-h)}" fill="#4a4436" opacity="${f(0.4 + r() * 0.3)}"/>`; }
    // stalactites from the roof, stalagmites from the floor, drips
    for (let k = 0; k < 40; k++) { const x = 70 + r() * 940; if (Math.abs(x - HX) < 70) continue; const y = CAVE0 + 30 + Math.abs(x - HX) * 0.45 + r() * 60, h = 40 + r() * 200, w = 8 + r() * 18;
      cave += `<path d="M${f(x - w)},${f(y)}Q${f(x - w * 0.3)},${f(y + h * 0.7)} ${f(x)},${f(y + h)}Q${f(x + w * 0.3)},${f(y + h * 0.7)} ${f(x + w)},${f(y)}Z" fill="#8a8476" stroke="#3a3630" stroke-width="2"/><path d="M${f(x - w * 0.5)},${f(y)}Q${f(x - w * 0.2)},${f(y + h * 0.6)} ${f(x)},${f(y + h * 0.95)}" stroke="#d8d0bc" stroke-width="2" fill="none" opacity=".55"/>`;
      if (k % 4 === 0) cave += `<path d="M${f(x)},${f(y + h + 30)}q-4,10 0,14q4,-4 0,-14z" fill="#bfe6f0"/><path d="M${f(x)},${f(y + h + 70)}q-4,10 0,14q4,-4 0,-14z" fill="#bfe6f0" opacity=".7"/>`; }
    for (let k = 0; k < 14; k++) { const x = 100 + r() * 880, y = WT - 10, h = 40 + r() * 140, w = 14 + r() * 20;
      cave += `<path d="M${f(x - w)},${f(y)}Q${f(x - w * 0.3)},${f(y - h * 0.7)} ${f(x)},${f(y - h)}Q${f(x + w * 0.3)},${f(y - h * 0.7)} ${f(x + w)},${f(y)}Z" fill="#7a7466" stroke="#3a3630" stroke-width="2"/><path d="M${f(x - w * 0.4)},${f(y)}Q${f(x - w * 0.15)},${f(y - h * 0.6)} ${f(x)},${f(y - h * 0.95)}" stroke="#c8c0aa" stroke-width="2" fill="none" opacity=".5"/>`; }
    // the light falling through the mouth into the chamber, dust in it
    cave += `<path d="M${HX - 70},${CAVE0}L${HX + 70},${CAVE0}L${HX + 320},${WT + 40}L${HX - 260},${WT + 40}Z" fill="url(#beam)" style="mix-blend-mode:screen"/>`;
    for (let k = 0; k < 60; k++) { const t = r(), y = CAVE0 + t * (WT - CAVE0), x = HX - 60 - t * 200 + r() * (120 + t * 500); cave += `<circle cx="${f(x)}" cy="${f(y)}" r="${f(1.4 + r() * 2.4)}" fill="#fff4d0" opacity="${f(0.3 + r() * 0.5)}"/>`; }
    // the groundwater: a still pool across the floor, and a channel snaking away into the dark like a naga's body (the "hungry naga" is this water)
    cave += `<rect x="0" y="${WT}" width="1080" height="${CAVE1 - WT + 200}" fill="url(#gw)"/>`;
    for (let k = 0; k < 18; k++) { const x = 90 + r() * 900, h = 60 + r() * 160; cave += `<path d="M${f(x - 12)},${WT + 4}Q${f(x)},${f(WT + h * 0.8)} ${f(x + 2)},${f(WT + h)}Q${f(x + 6)},${f(WT + h * 0.6)} ${f(x + 12)},${WT + 4}Z" fill="#9ab4b8" opacity=".12"/>`; }
    cave += `<path d="M0,${WT}H1080" stroke="#bfe6f0" stroke-width="3" opacity=".7"/><ellipse cx="${HX + 30}" cy="${WT + 14}" rx="220" ry="10" fill="#fff2c8" opacity=".55"/>`;
    for (let k = 0; k < 6; k++) cave += `<ellipse cx="${HX + 20}" cy="${WT + 10}" rx="${30 + k * 34}" ry="${4 + k * 2}" fill="none" stroke="#d8f4ff" stroke-width="2" opacity="${f(0.5 - k * 0.07)}"/>`;
    // the channel: a sinuous ribbon with scale-like ripples and a glint along its back
    let cp = ""; const C = (t) => [140 + t * 820 + Math.sin(t * 7) * 60, WT + 130 + Math.sin(t * 9.5 + 1) * 70 + t * 160];
    for (let t = 0; t <= 1.001; t += 0.02) { const [x, y] = C(t); cp += `${t ? "L" : "M"}${f(x)},${f(y)}`; }
    cave += `<path d="${cp}" stroke="#0f3a44" stroke-width="70" fill="none" stroke-linecap="round" opacity=".45"/><path d="${cp}" stroke="#2a7a88" stroke-width="34" fill="none" stroke-linecap="round" opacity=".35"/><path d="${cp}" stroke="#7ac8d4" stroke-width="10" fill="none" stroke-linecap="round" opacity=".25"/>`;
    for (let t = 0.02; t < 1; t += 0.035) { const [x, y] = C(t), [x2, y2] = C(t + 0.01), a = Math.atan2(y2 - y, x2 - x) * 180 / Math.PI;
      if (false) cave += `<path d="M-8,-10Q3,0 -8,10" transform="translate(${f(x)},${f(y)}) rotate(${f(a)})" stroke="#8ad0dc" stroke-width="2" fill="none" opacity=".35"/>`; }
    cave += `<path d="${cp}" stroke="#e8fbff" stroke-width="2.4" fill="none" stroke-dasharray="40 30 10 30" opacity=".5" transform="translate(-3,-6)"/><path d="${cp}" stroke="#9ad8e4" stroke-width="1.6" fill="none" stroke-dasharray="16 50" opacity=".45" transform="translate(4,6)"/>`;
    // the old water levels: pale mineral rings on the cave wall where the water used to stand, each one lower
    // (the same story the notches on ยาย's well post tell): the water was up here, now it is far down
    for (let k = 0; k < 4; k++) { const y = WT - 140 - k * 120; let d = `M-60,${y}`; for (let x = -60; x <= 1140; x += 60) d += `${x > HX - 230 && x < HX + 300 ? "M" : "L"}${x},${f(y + Math.sin(x / 90 + k) * 6)}`;
      cave += `<path d="${d}" stroke="#2a2418" stroke-width="12" fill="none" opacity="${f(0.4 - k * 0.07)}" transform="translate(0,9)"/><path d="${d}" stroke="#e2d4ac" stroke-width="${7 - k}" fill="none" opacity="${f(0.62 - k * 0.1)}"/>`; }
    // the head of the channel disappearing into a dark side passage, two glints like eyes left ambiguous
    const [hx, hy] = C(1); cave += `<ellipse cx="${f(hx + 40)}" cy="${f(hy)}" rx="90" ry="120" fill="#05060a"/>`;
    g += `<g clip-path="url(#cavec)">${cave}</g>`;
    // the pump's pipe: from the pump on the paddy bund straight down through every layer into the groundwater, sucking it away
    { const PX = 880, top = SURF - 70, bot = WT + 170;
      def(`<linearGradient id="pipeG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a5e66"/><stop offset=".35" stop-color="#c8ccd4"/><stop offset=".6" stop-color="#8a8e96"/><stop offset="1" stop-color="#3a3e46"/></linearGradient>`);
      g += `<rect x="${PX - 13}" y="${top}" width="26" height="${bot - top}" fill="url(#pipeG)" stroke="#1e1712" stroke-width="3"/>`;
      for (let y = top + 380; y < bot - 40; y += 420) g += `<rect x="${PX - 18}" y="${y}" width="36" height="16" rx="3" fill="#7a7e86" stroke="#1e1712" stroke-width="2"/>`;
      g += `<g transform="translate(${PX},${bot})"><rect x="-24" y="0" width="48" height="56" rx="6" fill="#6a6e76" stroke="#1e1712" stroke-width="3"/>${[0, 1, 2, 3].map((k) => `<path d="M-24,${12 + k * 12}H24" stroke="#2a2c30" stroke-width="3"/>`).join("")}
        ${[0, 1, 2].map((k) => `<ellipse cx="0" cy="${34}" rx="${60 + k * 46}" ry="${12 + k * 8}" fill="none" stroke="#d8f4ff" stroke-width="2" opacity="${f(0.5 - k * 0.14)}"/>`).join("")}</g>`;
      g += `<g transform="translate(${PX},${top})"><rect x="-56" y="-62" width="112" height="62" rx="8" fill="#c8402e" stroke="#1e1712" stroke-width="3"/><circle cx="-22" cy="-30" r="16" fill="#3a3a3a"/><rect x="10" y="-50" width="34" height="18" fill="#e8e0c8"/><path d="M56,-30h70" stroke="#2a5ab0" stroke-width="14" stroke-linecap="round"/></g>`; }

    // a soft vignette on the cut face, darker away from the shaft's light; the surface glow fading with depth
    def(`<radialGradient id="faceL" cx="${HX / 1080}" cy="${SURF / H}" r=".55"><stop offset="0" stop-color="#ffcf86" stop-opacity=".22"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
      <linearGradient id="deep" x1="0" y1="0" x2="0" y2="1"><stop offset="${SURF / H}" stop-color="#000" stop-opacity="0"/><stop offset="${(SURF + 1500) / H}" stop-color="#000" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></linearGradient>`);
    g += `<rect width="1080" height="${H}" fill="url(#faceL)" style="mix-blend-mode:screen"/><rect width="1080" height="${H}" fill="url(#deep)"/>`;
    return { g, H, SURF, CAVE0, WT };
  }
  function depth(k) {
    const w = depthWorld();
    // camera keys along one continuous move (y of the frame top, zoom about the frame centre)
    const cams = { 1: { y: 0, s: 1 }, 2: { y: w.SURF - 1150, s: 1.15, x: 40 }, 3: { y: w.SURF + 300, s: 1.05, x: 20 }, 4: { y: w.CAVE0 - 120, s: 1.0, x: 0 } }, c = cams[k];
    def(`<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>`);
    return `<g transform="translate(540,960) scale(${c.s}) translate(${-540 - (c.x || 0)},${-960 - c.y})">${w.g}</g><rect width="1080" height="1920" fill="url(#vig)"/>` + grainDef("gr");
  }

  // library mode (coordinator 3 Nov 2569): the same scenes, returned as markup for the episode engine instead of drawn into #cv.
  // RupStill.scene(name) → { defs, body } for drone-dusk · drone-moon · measure · measure-note · measure-note-100 (the notebook with
  // the evacuation line "ห่างหลุมอย่างน้อย 100 ม." in red instead of the sketch, for EP.3's 100 m rope) (1080×1920, screen-sized);
  // RupStill.world() → { defs, body, H, SURF, CAVE0, WT }: the tall depth world for the dive (1080 × H), the camera travels down it.
  window.RupStill = {
    scene(name) { defs = ""; let body = "";
      if (name === "drone-dusk") body = drone(PAL.dusk, false); else if (name === "drone-moon") body = drone(PAL.moon, true);
      else if (name === "measure") body = measure(false); else if (name === "measure-note") body = measure(true);
      else if (name === "measure-note-100") body = measure(true, true);
      return { defs, body }; },
    world() { defs = ""; const w = depthWorld(); return { defs, body: w.g, H: w.H, SURF: w.SURF, CAVE0: w.CAVE0, WT: w.WT }; },
  };
})();
