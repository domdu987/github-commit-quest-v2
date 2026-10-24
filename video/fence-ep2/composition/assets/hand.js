// Round "mitten" hands in the channel's rig style (a ball with a thumb and finger bumps, ink outline), the same
// family as the flashlight hand in เสียงกอย. Every hand is a group in local coordinates (see each function) so shots
// place it with translate/scale/rotate; colours come from the character (skin, skinS, sleeve, sleeveS).
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mix = (a, b, k) => { const p = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16)); const A = p(a), B = p(b); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const COL = (o = {}) => { const skin = o.skin || "#ecc29c", sleeve = o.sleeve || "#9fc5d8"; return { skin, skinS: o.skinS || mix(skin, "#5a3220", 0.3), sleeve, sleeveS: o.sleeveS || mix(sleeve, "#000000", 0.3) }; };
  // a ball hand: the palm circle with a crescent of shade on the shade side (sx = -1 | 1) and a couple of finger creases on the grip side
  const ball = (c, r, sx = 1, creases = true) => `<circle r="${r}" fill="${c.skin}" ${OUT}/><path d="M${-sx * r * 0.2},${r * 0.95}A${r},${r} 0 0 ${sx > 0 ? 0 : 1} ${sx * r * 0.98},${r * 0.2}A${r * 1.3},${r * 1.3} 0 0 ${sx > 0 ? 1 : 0} ${-sx * r * 0.2},${r * 0.95}Z" fill="${c.skinS}" opacity=".45"/>
    ${creases ? [-0.25, 0.1, 0.45].map((k) => `<path d="M${sx * r * 0.55},${r * k - 10}q${sx * 14},10 0,20" stroke="${c.skinS}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".8"/>`).join("") : ""}`;
  const thumb = (c, x, y, r, rot = 0) => `<g transform="translate(${x},${y}) rotate(${rot})"><rect x="${-r}" y="${-r * 1.9}" width="${r * 2}" height="${r * 2.6}" rx="${r}" fill="${c.skin}" ${OUT}/><path d="M${-r * 0.6},${-r * 1.4}q${r * 0.6},-8 ${r * 1.2},0" stroke="${c.skinS}" stroke-width="3" fill="none" opacity=".7"/></g>`;

  // ---- grip: a round hand holding something to the +x side; origin = the edge the hand presses on, mid-height ----
  // the forearm leaves toward (-x, +y). Mirror with scale(-1,1) for the other hand. ~300 px wide at scale 1.
  function grip(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "";
    const sleeve = `<path d="M-220,40L-40,170L-330,840L-600,700Z" fill="${c.sleeve}" ${OUT}/><path d="M-330,840L-600,700L-540,640L-260,760Z" fill="${c.sleeveS}" opacity=".45"/>`;
    const fingers = [[-80, 40], [-5, 52], [70, 50], [140, 36]].map(([y, r]) => `<circle cx="${20 + r * 0.3}" cy="${y}" r="${r}" fill="${c.skin}" ${OUT}/>`).join("");   // four finger bumps curling over the edge
    return `<g ${id}>${sleeve}${fingers}<g transform="translate(-100,10)">${ball(c, 128, 1)}</g>${thumb(c, -10, -118, 36, 28)}</g>`;
  }

  // ---- point: a round fist with the index finger out; origin = the fingertip, finger pointing -x, forearm to +x ----
  function point(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "";
    const sleeve = `<path d="M300,-110L760,-140L760,150L300,130Z" fill="${c.sleeve}" ${OUT}/><path d="M300,-110L350,-114L350,134L300,130Z" fill="${c.sleeveS}" opacity=".5"/>`;
    const index = `<rect x="0" y="-30" width="230" height="60" rx="30" fill="${c.skin}" ${OUT}/><path d="M110,-18q-10,18 0,36" stroke="${c.skinS}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".8"/>`;
    const curl = [[150, 50, 34], [160, 110, 30]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c.skin}" ${OUT}/>`).join("");
    return `<g ${id}>${sleeve}<g transform="translate(240,10)">${ball(c, 108, -1, false)}</g>${curl}${index}${thumb(c, 150, -46, 30, -70)}</g>`;
  }

  // ---- open: a small round hand reaching up, finger bumps spread; origin = palm centre, forearm down ----
  function open(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "";
    const sleeve = `<path d="M-50,60L50,60L74,470L-74,470Z" fill="${c.sleeve}" ${OUT}/><path d="M-50,60L50,60L52,100L-52,100Z" fill="${c.sleeveS}" opacity=".5"/>`;
    const fingers = [[-62, -70, 26], [-22, -92, 28], [20, -92, 28], [60, -70, 25]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c.skin}" ${OUT}/>`).join("");
    return `<g ${id}>${sleeve}${fingers}${ball(c, 84, 1, false)}<path d="M-30,-10q30,20 60,0M-26,24q26,18 52,0" stroke="${c.skinS}" stroke-width="3" fill="none" opacity=".6"/>${thumb(c, -86, 20, 24, 50)}</g>`;
  }

  // ---- holdCan: a round hand around a small can (the can is part of the group); origin = can centre ----
  function holdCan(o = {}) {
    const c = COL(o), col = o.col || "#c8392b", id = o.id ? `id="${o.id}"` : "";
    const can = `<rect x="-46" y="-66" width="92" height="132" rx="8" fill="url(#fCan)" ${OUT}/><rect x="-46" y="-24" width="92" height="52" fill="${col}" opacity=".9"/><path d="M-46,-66q46,-16 92,0" fill="#dfe3e6" ${OUT}/>`;
    return `<g ${id}><g transform="translate(-46,10) scale(0.5)">${grip(o)}</g>${can}<g transform="translate(-46,10) scale(0.5)">${[[-80, 40], [-5, 52], [70, 50], [140, 36]].map(([y, r]) => `<circle cx="${20 + r * 0.3}" cy="${y}" r="${r}" fill="${c.skin}" ${OUT}/>`).join("")}</g></g>`;
  }

  window.Hand = { grip, point, open, holdCan, COL };
})();
