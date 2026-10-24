// Hands that really hold things, drawn like the reference clips: no black outline, forms separated by tone,
// long tapered fingers with a shaded underside, faint nails, a soft gradient on the back of the hand.
// grip (two-hand hold, POV), point (fist + index), open (a child's hand reaching), holdCan (a hand around a small can).
// Every hand is a group in local coordinates (see each function) so shots place it with translate/scale/rotate;
// colours come from the character (skin, skinS, sleeve, sleeveS).
(function () {
  const f1 = (v) => v.toFixed(1);
  const mix = (a, b, k) => { const p = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16)); const A = p(a), B = p(b); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  let N = 0;
  const COL = (o = {}) => { const skin = o.skin || "#ecc29c", sleeve = o.sleeve || "#9fc5d8";
    return { skin, skinS: o.skinS || mix(skin, "#5a3220", 0.3), skinD: mix(skin, "#3a2014", 0.5), nail: mix(skin, "#fff6ee", 0.3), sleeve, sleeveS: o.sleeveS || mix(sleeve, "#000000", 0.3), line: mix(skin, "#2a1a10", 0.55) }; };
  const LW = 2.2;   // the thin tonal outline

  // a tapered finger along a quadratic curve from knuckle (x0, y0) to tip (x1, y1); width w at the base, 0.72 w at the tip
  // bend > 0 bows the finger toward its shade side (the +normal); returns the silhouette, the shaded underside, a joint crease, the nail
  function finger(x0, y0, x1, y1, w, c, bend = 0.18, shadeSide = 1) {
    const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = (-dy / L) * shadeSide, ny = (dx / L) * shadeSide;
    const cx = x0 + dx * 0.55 + nx * L * bend, cy = y0 + dy * 0.55 + ny * L * bend;
    const P = (t) => [(1 - t) * (1 - t) * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) * (1 - t) * y0 + 2 * (1 - t) * t * cy + t * t * y1];
    const T = (t) => { const tx = 2 * (1 - t) * (cx - x0) + 2 * t * (x1 - cx), ty = 2 * (1 - t) * (cy - y0) + 2 * t * (y1 - cy), l = Math.hypot(tx, ty) || 1; return [tx / l, ty / l]; };
    const n = 10, up = [], dn = [];
    for (let i = 0; i <= n; i++) { const t = i / n, [px, py] = P(t), [tx, ty] = T(t), hw = (w / 2) * (1 - 0.28 * t); up.push([px - ty * hw, py + tx * hw]); dn.push([px + ty * hw, py - tx * hw]); }
    const [ex, ey] = P(1), [tx, ty] = T(1), r = (w / 2) * 0.72;
    const tip = `A${f1(r)},${f1(r)} 0 0 0 ${f1(dn[n][0])},${f1(dn[n][1])}`, r0 = w / 2;   // rounded tip, rounded base (hidden under the hand)
    const sil = `M${up.map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}${tip}L${dn.slice().reverse().map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}A${f1(r0)},${f1(r0)} 0 0 0 ${f1(up[0][0])},${f1(up[0][1])}Z`;
    // underside shade: the half of the finger on the shade side
    const mid = up.map((p, i) => [(p[0] + dn[i][0]) / 2 + nx * 2, (p[1] + dn[i][1]) / 2 + ny * 2]);
    const shadePts = shadeSide > 0 ? [up, mid] : [dn, mid];
    const shade = `M${shadePts[0].map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}L${shadePts[1].slice().reverse().map((p) => `${f1(p[0])},${f1(p[1])}`).join("L")}Z`;
    const [jx, jy] = P(0.55), [jtx, jty] = T(0.55), hwj = (w / 2) * 0.85;
    const nailC = [ex - tx * w * 0.5, ey - ty * w * 0.5], ang = (Math.atan2(ty, tx) * 180) / Math.PI;
    return `<path d="${sil}" fill="${c.skin}" stroke="${c.line}" stroke-width="${LW}" stroke-linejoin="round"/>
      <path d="${shade}" fill="${c.skinS}" opacity=".55"/>
      <path d="M${f1(jx - jty * hwj * 0.9)},${f1(jy + jtx * hwj * 0.9)}Q${f1(jx + jtx * 5)},${f1(jy + jty * 5)} ${f1(jx + jty * hwj * 0.6)},${f1(jy - jtx * hwj * 0.6)}" stroke="${c.skinS}" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".75"/>
      <ellipse cx="${f1(nailC[0])}" cy="${f1(nailC[1])}" rx="${f1(w * 0.24)}" ry="${f1(w * 0.17)}" fill="${c.nail}" opacity=".75" transform="rotate(${f1(ang)} ${f1(nailC[0])} ${f1(nailC[1])})"/>`;
  }
  const grad = (id, c, x1, y1, x2, y2) => `<linearGradient id="${id}" gradientUnits="userSpaceOnUse" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"><stop offset="0" stop-color="${c.skin}"/><stop offset="1" stop-color="${c.skinS}"/></linearGradient>`;

  // ---- grip: a hand seen from above, fingers wrapping around something to the +x side; origin = the edge the fingers wrap over, mid-height ----
  // the forearm leaves toward (-x, +y). Mirror with scale(-1,1) for the other hand. ~330 px wide at scale 1.
  function grip(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "", g = `hg${N++}`;
    const sleeve = `<path d="M-236,-10L-60,150L-330,840L-600,700Z" fill="${c.sleeve}"/><path d="M-330,840L-600,700L-540,640L-260,760Z" fill="${c.sleeveS}" opacity=".45"/><path d="M-236,-10L-60,150L-84,190L-262,30Z" fill="${c.sleeveS}" opacity=".5"/>`;
    const wrist = `<path d="M-230,-60C-250,30 -200,130 -120,160L-40,150L-30,-80Z" fill="${c.skin}"/>`;
    // little finger to index (index drawn last so it overlaps), knuckles at x≈-20, tips curling down over the front
    const F = [[-30, 118, 112, 150, 44], [-24, 44, 148, 86, 52], [-20, -30, 164, 12, 56], [-18, -104, 154, -68, 58]];
    const fingers = F.map(([x0, y0, x1, y1, w]) => finger(x0, y0, x1, y1, w, c, 0.2, 1)).join("");
    const back = `${grad(g, c, -200, -150, 20, 150)}<path d="M-215,-150C-150,-205 -30,-195 10,-150C30,-80 26,70 8,145C-40,190 -150,195 -215,150C-240,60 -240,-60 -215,-150Z" fill="url(#${g})" stroke="${c.line}" stroke-width="${LW}"/>
      ${[-104, -30, 44, 118].map((y) => `<path d="M-8,${y - 16}q12,16 0,32" stroke="${c.skinS}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>`).join("")}
      <path d="M-160,-96q50,-34 110,-26M-176,34q40,-12 86,-2" stroke="${c.skinS}" stroke-width="2.4" fill="none" opacity=".45"/>`;
    const thumb = finger(-120, -130, 62, -262, 58, c, -0.22, -1);
    return `<g ${id}>${sleeve}${wrist}${fingers}${back}${thumb}</g>`;
  }

  // ---- point: a fist with the index finger out; origin = the fingertip, finger pointing -x, forearm to +x ----
  function point(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "", g = `hp${N++}`;
    const sleeve = `<path d="M330,-120L760,-150L760,160L330,140Z" fill="${c.sleeve}"/><path d="M330,-120L380,-124L380,144L330,140Z" fill="${c.sleeveS}" opacity=".5"/>`;
    const fist = `${grad(g, c, 200, -100, 300, 130)}<path d="M170,-90C230,-130 330,-120 350,-60C372,20 360,100 320,122C250,150 160,140 140,100C120,50 120,-40 170,-90Z" fill="url(#${g})" stroke="${c.line}" stroke-width="${LW}"/>`;
    // curled middle, ring and little finger under the index, seen end-on
    const curl = [[150, 54, 46, 30], [152, 104, 42, 27], [160, 146, 36, 22]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${c.skin}" stroke="${c.line}" stroke-width="${LW}"/><path d="M${x - rx},${y}a${rx},${ry} 0 0 0 ${rx * 2},0a${rx},${ry * 0.55} 0 0 1 ${-rx * 2},0z" fill="${c.skinS}" opacity=".5"/>`).join("");
    const index = finger(172, 0, 0, 0, 58, c, 0.05, 1);
    const thumb = finger(322, -70, 150, -30, 54, c, 0.3, -1);
    return `<g ${id}>${sleeve}${fist}${curl}${index}${thumb}</g>`;
  }

  // ---- open: a small open hand reaching up, palm to the viewer, fingers spread; origin = palm centre, forearm down ----
  function open(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "", g = `ho${N++}`;
    const sleeve = `<path d="M-50,70L50,70L74,470L-74,470Z" fill="${c.sleeve}"/><path d="M-50,70L50,70L52,110L-52,110Z" fill="${c.sleeveS}" opacity=".5"/>`;
    const F = [[-52, -40, -112, -156, 32], [-20, -60, -46, -196, 34], [16, -62, 26, -198, 34], [50, -46, 98, -160, 30]];
    const fingers = F.map(([x0, y0, x1, y1, w]) => finger(x0, y0, x1, y1, w, c, 0.08, 1)).join("");
    const palm = `${grad(g, c, 0, -80, 0, 90)}<path d="M-70,-40C-60,-80 60,-80 70,-40C84,20 60,80 0,86C-60,80 -84,20 -70,-40Z" fill="url(#${g})" stroke="${c.line}" stroke-width="${LW}"/>
      <path d="M-50,-10q50,30 100,-4M-44,24q44,28 88,0M-20,-50q20,70 40,0" stroke="${c.skinS}" stroke-width="2.6" fill="none" opacity=".7"/>`;
    const thumb = finger(-56, 10, -130, -62, 38, c, -0.15, -1);
    return `<g ${id}>${sleeve}${fingers}${palm}${thumb}</g>`;
  }

  // ---- holdCan: a hand around a small can (the can is part of the group); origin = can centre ----
  function holdCan(o = {}) {
    const c = COL(o), col = o.col || "#c8392b", id = o.id ? `id="${o.id}"` : "";
    const can = `<rect x="-46" y="-66" width="92" height="132" rx="8" fill="url(#fCan)" stroke="#2e2a26" stroke-width="3"/><rect x="-46" y="-24" width="92" height="52" fill="${col}" opacity=".9"/><path d="M-46,-66q46,-16 92,0" fill="#dfe3e6" stroke="#2e2a26" stroke-width="3"/>`;
    return `<g ${id}>${can}<g transform="translate(-46,10) scale(0.52)">${grip(o)}</g></g>`;
  }

  window.Hand = { grip, point, open, holdCan, finger, COL };
})();
