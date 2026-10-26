// Flat-vector hands for the first-person shots (the same ink-outline family as the rigs, but drawn as real hands: a palm,
// four separate fingers with knuckle creases, a thumb with a nail, a wrist and a sleeve cuff). Every hand is a group in
// local coordinates (see each function) so shots place it with translate/scale/rotate; the origins and overall sizes are
// kept from the first version so existing shots still line up. Colours come from the character (skin, skinS, sleeve, sleeveS).
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
  const mix = (a, b, k) => { const p = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16)); const A = p(a), B = p(b); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const COL = (o = {}) => { const skin = o.skin || "#ecc29c", sleeve = o.sleeve || "#9fc5d8"; return { skin, skinS: o.skinS || mix(skin, "#5a3220", 0.28), skinH: mix(skin, "#ffffff", 0.35), sleeve, sleeveS: o.sleeveS || mix(sleeve, "#000000", 0.3) }; };
  // a finger: a rounded bar from (0,0) along +x of length len and width w, a rounder tip, two knuckle creases; rot about its root
  const finger = (c, x, y, len, w, rot = 0, nail = false) => `<g transform="translate(${x},${y}) rotate(${rot})">
      <rect x="${-w * 0.5}" y="${-w / 2}" width="${len + w * 0.5}" height="${w}" rx="${w / 2}" fill="${c.skin}" ${OUT}/>
      <path d="M${-w * 0.2},${w * 0.42}h${len * 0.9}" stroke="${c.skinS}" stroke-width="${w * 0.22}" stroke-linecap="round" opacity=".55"/>
      <path d="M${len * 0.38},${-w * 0.34}q${w * 0.12},${w * 0.34} 0,${w * 0.68}M${len * 0.7},${-w * 0.3}q${w * 0.1},${w * 0.3} 0,${w * 0.6}" stroke="${c.skinS}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>
      ${nail ? `<ellipse cx="${len - w * 0.05}" cy="${-w * 0.1}" rx="${w * 0.26}" ry="${w * 0.2}" fill="${c.skinH}" stroke="${INK}" stroke-width="2.5"/>` : ""}</g>`;
  // the sleeve cuff: a thick band of the sleeve colour with a fold, then the sleeve itself running off the frame
  const cuff = (c, pts, band) => `<path d="${pts}" fill="${c.sleeve}" ${OUT}/><path d="${band}" fill="${c.sleeveS}" opacity=".5"/>`;

  // ---- grip: a fist wrapped round something standing along +x of the origin (the handle, the edge of a can, the bar);
  // origin = the edge the fingers close over, mid-height; the forearm leaves toward (-x, +y). ~300 px wide at scale 1. ----
  function grip(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "";
    const sleeve = cuff(c, "M-250,20L-70,160L-330,840L-600,700Z", "M-250,20L-70,160L-110,214L-290,74Z") + `<path d="M-330,840L-600,700L-540,640L-260,760Z" fill="${c.sleeveS}" opacity=".3"/>`;
    const wrist = `<path d="M-230,-20Q-240,80 -150,150L-60,160Q-120,80 -120,-40Z" fill="${c.skin}" ${OUT}/>`;
    // the palm: a rounded block behind the fingers, the heel of the hand lower-left
    const palm = `<path d="M-215,-125Q-235,-10 -205,120Q-150,165 -60,150L-20,140L-20,-120Q-120,-160 -215,-125Z" fill="${c.skin}" ${OUT}/>
      <path d="M-205,120Q-150,165 -60,150L-20,140L-30,96Q-120,120 -190,70Z" fill="${c.skinS}" opacity=".45"/>`;
    // four fingers curling over the edge: each root at the palm's right side, bent so the tip wraps past x = 0
    const F = [[-105, 28], [-45, 32], [15, 31], [72, 27]].map(([y, w], i) => {
      const len = 118 - i * 6;
      return `<g transform="translate(-40,${y})">${finger(c, 0, 0, len, w * 2, -4)}<g transform="translate(${len - 2},${w * 0.1}) rotate(112)">${finger(c, 0, 0, w * 1.45, w * 1.8, 0, true)}</g></g>`;
    }).join("");
    // the thumb over the top, crossing the first finger, nail toward us
    const thumbT = `<g transform="translate(-160,-96) rotate(-26)">${finger(c, 0, 0, 120, 58, 0)}<g transform="translate(116,2) rotate(70)">${finger(c, 0, 0, 40, 54, 0, true)}</g></g>`;
    return `<g ${id}>${sleeve}${wrist}${palm}${F}${thumbT}</g>`;
  }

  // ---- point: a hand with the index finger out; origin = the fingertip, finger pointing -x, forearm to +x ----
  function point(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "";
    const sleeve = cuff(c, "M300,-120L760,-150L760,160L300,140Z", "M300,-120L360,-124L360,144L300,140Z");
    const palm = `<path d="M110,-96Q230,-130 300,-100L300,130Q230,150 130,120Q90,60 110,-96Z" fill="${c.skin}" ${OUT}/><path d="M130,120Q230,150 300,130L300,86Q230,106 150,80Z" fill="${c.skinS}" opacity=".45"/>`;
    // three curled fingers under the palm (seen as stacked knuckles), the index straight out to the fingertip at the origin
    const curl = [[196, 124, 44], [178, 86, 48], [160, 44, 52]].map(([x, y, w]) => `<g transform="translate(${x},${y}) rotate(-148)">${finger(c, 0, 0, 78, w, 0, false)}<g transform="translate(76,0) rotate(-96)">${finger(c, 0, 0, 34, w * 0.9, 0, true)}</g></g>`).join("");
    const index = `<g transform="translate(236,-60) rotate(180)">${finger(c, 0, 0, 232, 58, 0, true)}</g>`;
    const thumbT = `<g transform="translate(214,-30) rotate(-140)">${finger(c, 0, 0, 90, 52, 0, true)}</g>`;
    return `<g ${id}>${sleeve}${palm}${curl}${index}${thumbT}</g>`;
  }

  // ---- open: a hand reaching up, palm to us, fingers spread; origin = palm centre, forearm down. ~200 px wide at scale 1 ----
  function open(o = {}) {
    const c = COL(o), id = o.id ? `id="${o.id}"` : "";
    const sleeve = cuff(c, "M-56,70L56,70L80,470L-80,470Z", "M-56,70L56,70L58,112L-58,112Z");
    const wrist = `<path d="M-44,30Q-50,80 -40,110L40,110Q50,80 44,30Z" fill="${c.skin}" ${OUT}/>`;
    const palm = `<path d="M-82,-40Q-96,40 -60,86Q0,106 60,86Q96,40 82,-40Q40,-80 0,-80Q-40,-80 -82,-40Z" fill="${c.skin}" ${OUT}/>
      <path d="M-30,-6q30,22 60,0M-40,30q40,26 80,0M-20,56q20,10 40,0" stroke="${c.skinS}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".7"/>`;
    const F = [[-66, -34, 104, 44, -106], [-24, -66, 124, 46, -96], [20, -66, 124, 46, -84], [62, -34, 100, 42, -72]].map(([x, y, len, w, rot]) => finger(c, x, y, len, w, rot, true)).join("");
    const thumbT = `<g transform="translate(-74,20) rotate(-150)">${finger(c, 0, 0, 96, 46, 0, true)}</g>`;
    return `<g ${id}>${sleeve}${wrist}${F}${palm}${thumbT}</g>`;
  }

  // ---- holdCan: a hand round a small can (the can is part of the group); origin = can centre ----
  function holdCan(o = {}) {
    const c = COL(o), col = o.col || "#c8392b", id = o.id ? `id="${o.id}"` : "";
    const can = `<rect x="-46" y="-66" width="92" height="132" rx="8" fill="url(#fCan)" ${OUT}/><rect x="-46" y="-24" width="92" height="52" fill="${col}" opacity=".9"/><path d="M-46,-66q46,-16 92,0" fill="#dfe3e6" ${OUT}/>`;
    // the fingers of the grip wrap the can: draw the grip behind, the can, then the finger tips again in front
    const g = grip(o);
    const tips = [[-105, 28], [-45, 32], [15, 31], [72, 27]].map(([y, w], i) => { const len = 118 - i * 6; return `<g transform="translate(-40,${y})"><g transform="translate(${len - 2},${w * 0.1}) rotate(112)">${finger(c, 0, 0, w * 1.45, w * 1.8, 0, true)}</g></g>`; }).join("");
    return `<g ${id}><g transform="translate(-46,10) scale(0.5)">${g}</g>${can}<g transform="translate(-46,10) scale(0.5)">${tips}</g></g>`;
  }

  window.Hand = { grip, point, open, holdCan, COL, finger };
})();
