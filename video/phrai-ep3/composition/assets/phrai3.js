// Sets for "มือพราย" EP.3 ให้นอนหงาย (load after phrai.js and phraiui.js):
//   Sets.riverTop    straight down on the black river at night: moon and stars reflected, krathongs drifting, แพรว swimming
//                    face down (o.pose "prone": strokes #id-stA / #id-stB, kick splashes #id-kick, moved by #id-swo) or
//                    floating on her back (o.pose "supine": arms #id-aL / #id-aR scull, chest #id-chest breathes); a pale hand on
//                    her ankle (#id-ph), the gallon (#id-gal), the bank across the top when o.bank (y of the water's edge)
//   Sets.moonPOV     on her back looking up: the full moon, stars, thin cloud, river water lapping over the bottom of the lens (#id-lap)
//   Sets.ankleGrab   under the river: her ankle and the hem of the navy track pants kicking, a pale hand closing on it (#id-hand)
//   Sets.ward        the hospital room at dawn: bed (mattress top at o.bed ?? G - 330) with a blanket (#id-blanket goes over
//                    whoever lies in it), drip stand, chair, a window onto the river at sunrise (#id-boat: a ferry far out)
//   Sets.mhemLegend  the shadow-puppet screen again (two screens, y 0 / 1600): S1 a child in the river, a young man diving off
//                    the pier bare-handed (#id-dive); S2 under water the child clinging to his neck, both going down (#id-pair),
//                    and an oar floating on the surface (#id-oar)
//   Sets.ankleP      แพรว's ankle close on the hospital sheet: five grey-green finger marks (#id-marks)
//   Phrai3.hosp(G)   the hospital landing for pierDeck props: a white building with lit windows, the green-cross sign
//   Phrai3.ktop      a krathong seen from above
// Card icons for EP.3: noswim, mouthup, floatback, paddle, toexit, holdfloat.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const P = window.Phrai;
  const C = { skin: "#e8b48a", skinS: "#c88f66", tee: "#f2f0ea", teeS: "#d3d1ca", pants: "#2b3d5e", pantsS: "#1f2d47", hair: "#1a1513" };

  Sets.DEFS += `
    <linearGradient id="p3Dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a6a9a"/><stop offset=".5" stop-color="#d99a8a"/><stop offset="1" stop-color="#f6cf96"/></linearGradient>
    <linearGradient id="p3Wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9cfc4"/><stop offset="1" stop-color="#9fb8ac"/></linearGradient>
    <linearGradient id="p3Fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#161b19" stop-opacity=".95"/><stop offset="1" stop-color="#0a0c0b" stop-opacity="0"/></linearGradient>
    <radialGradient id="p3Moon" cx=".5" cy=".5"><stop offset="0" stop-color="#f6efcf" stop-opacity=".55"/><stop offset=".4" stop-color="#9fb0d8" stop-opacity=".16"/><stop offset="1" stop-color="#9fb0d8" stop-opacity="0"/></radialGradient>
    <radialGradient id="p3Sun"><stop offset="0" stop-color="#ffe6b0" stop-opacity=".9"/><stop offset=".4" stop-color="#ffc98a" stop-opacity=".35"/><stop offset="1" stop-color="#ffc98a" stop-opacity="0"/></radialGradient>`;

  // a krathong from above: a ring of banana-leaf points, the green bowl, a ring of flowers, the candle in the middle
  function ktop(x, y, s, o = {}) {
    const pts = Array.from({ length: 12 }, (_, i) => { const a = (i / 12) * Math.PI * 2, b = a + Math.PI / 12;
      return `<path d="M${f1(Math.cos(a - 0.2) * 58)},${f1(Math.sin(a - 0.2) * 58)}L${f1(Math.cos(b) * 92)},${f1(Math.sin(b) * 92)}L${f1(Math.cos(a + 0.45) * 58)},${f1(Math.sin(a + 0.45) * 58)}Z" fill="${i % 2 ? "#4f8f45" : "#3f7a3a"}" stroke="#1f3a1c" stroke-width="3"/>`; }).join("");
    const fl = Array.from({ length: 8 }, (_, i) => { const a = (i / 8) * Math.PI * 2; return `<circle cx="${f1(Math.cos(a) * 34)}" cy="${f1(Math.sin(a) * 34)}" r="12" fill="${["#f2a33a", "#f7c04a", "#c45cc0"][i % 3]}" stroke="#7a4a12" stroke-width="2"/>`; }).join("");
    return `<g class="ktg" data-dx="${o.dx ?? 30}" data-ph="${o.ph ?? 0}"><g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${pts}<circle r="58" fill="#5c9a4a" stroke="#1f3a1c" stroke-width="3"/>${fl}
      <circle r="12" fill="#f4f0e6" stroke="#7a6a52" stroke-width="2"/>${o.lit === false ? "" : `<circle class="kflame" r="7" fill="#ffd36a"/>`}</g></g>`;
  }
  const kGlowTop = (x, y, s) => `<g class="kglw"><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(170 * s)}" fill="url(#phFlame)"/></g>`;
  // the gallon from above: a translucent white box, red cap, the handle
  const galTop = (s = 1) => `<g transform="scale(${s})"><rect x="-56" y="-80" width="112" height="160" rx="22" fill="#e9eef0" fill-opacity=".9" ${OUT}/><rect x="-46" y="-10" width="92" height="80" rx="14" fill="#7fb3c9" opacity=".6"/>
    <circle cx="-14" cy="-58" r="16" fill="#e04a3a" ${OUT3}/><path d="M18,-74q34,-4 34,30" stroke="${INK}" stroke-width="12" fill="none"/><path d="M18,-74q34,-4 34,30" stroke="#e9eef0" stroke-width="6" fill="none"/></g>`;

  // ---------------- straight down on the river ----------------
  function riverTop(L, o = {}) {
    const id = o.id || "rt", r = mk(o.seed || 131), sx = o.x ?? 540, sy = o.y ?? 1060, ss = o.s ?? 1, rot = o.rot ?? 0, mx = o.moonX ?? 780, my = o.moonY ?? 420;
    put(L.sky, `<rect x="-1200" y="-1200" width="3500" height="4600" fill="url(#phWater)"/>`);
    let m = `<circle cx="${mx}" cy="${my}" r="420" fill="url(#p3Moon)"/><ellipse class="mrefl" cx="${mx}" cy="${my}" rx="74" ry="70" fill="#f1ead0" opacity=".75"/>`;
    for (let k = 0; k < 70; k++) m += `<circle cx="${f1(-800 + r() * 2700)}" cy="${f1(-800 + r() * 3600)}" r="${f1(1.2 + r() * 2.2)}" fill="#e8ecff" opacity="${(0.15 + r() * 0.35).toFixed(2)}"/>`;
    for (let k = 0; k < 60; k++) m += `<path class="rip" d="M${f1(-800 + r() * 2700)},${f1(-800 + r() * 3600)}q${f1(30 + r() * 40)},-10 ${f1(70 + r() * 90)},0" stroke="#6c7fa8" stroke-width="3" fill="none" stroke-linecap="round" opacity=".3"/>`;
    put(L.mid, m);
    let s = "", g = "";
    if (o.bank !== undefined) { // the far edge of the river: trees from above, the road's string lights along the water
      const B = o.bank;
      s += `<rect x="-1200" y="-1600" width="3500" height="${B + 1600}" fill="#070c12"/>`;
      for (let k = 0; k < 26; k++) s += `<circle cx="${f1(-900 + k * 120 + r() * 60)}" cy="${f1(B - 120 - r() * 260)}" r="${f1(70 + r() * 70)}" fill="${k % 2 ? "#0c1a14" : "#10221a"}"/>`;
      s += `<path d="M-1200,${B}${Array.from({ length: 40 }, (_, k) => `L${-1200 + k * 90},${f1(B + (k % 2 ? 14 : -6))}`).join("")}L2300,${B}V${B - 40}H-1200Z" fill="#1a2420"/>`;
      for (let k = 0; k < 40; k++) s += `<circle class="slt" cx="${f1(-1000 + k * 82)}" cy="${f1(B - 30 + Math.sin(k) * 6)}" r="6" fill="${["#ffcf7a", "#ff8a6a", "#9fd8ff", "#ffe08a"][k % 4]}"/>`;
    }
    (o.kt || [[180, 520, 0.7], [960, 1500, 0.8], [120, 1720, 0.6]]).forEach(([x, y, k], i) => { s += ktop(x, y, k, { dx: 24 + i * 8, ph: i }); g += kGlowTop(x, y, k); });
    if (o.gal) s += `<g id="${id}-gal"><g transform="translate(${o.gal.x},${o.gal.y}) rotate(${o.gal.r ?? 20})">${galTop(o.gal.s ?? 1)}</g></g>`;
    put(L.set, s); put(L.glow, g);

    // แพรว (local: head toward -y, hips at 0, feet at +440)
    const leg = (x0, x1, y1) => `<path d="M${x0},40L${x1},${y1}" stroke="${INK}" stroke-width="92" stroke-linecap="round"/><path d="M${x0},40L${x1},${y1}" stroke="${C.pants}" stroke-width="80" stroke-linecap="round"/><path d="M${x0 + (x0 < 0 ? -30 : 30)},60L${x1 + (x0 < 0 ? -30 : 30)},${y1 - 20}" stroke="#f2f0ea" stroke-width="6" opacity=".8"/>`;
    const foot = (x, y) => `<ellipse cx="${x}" cy="${y + 40}" rx="34" ry="50" fill="${C.skin}" ${OUT}/>`;
    const tint = (d) => `<path d="${d}" fill="#14223f" opacity=".5"/>`;
    let b = "";
    if ((o.pose || "supine") === "supine") {
      // arms out to the sides (star float), each pivoting at its shoulder so the hands can scull
      const arm = (sd, aid) => `<g id="${id}-${aid}" transform="rotate(0 ${sd * 84} -200)"><path d="M${sd * 84},-200L${sd * 250},-150L${sd * 380},-60" stroke="${INK}" stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M${sd * 84},-200L${sd * 250},-150L${sd * 380},-60" stroke="${C.skin}" stroke-width="54" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M${sd * 84},-200L${sd * 170},-176" stroke="${C.tee}" stroke-width="64" stroke-linecap="round"/>
        <ellipse cx="${sd * 404}" cy="-46" rx="40" ry="34" fill="${C.skin}" ${OUT}/>${tint(`M${sd * 200},-196L${sd * 430},-90L${sd * 420},-10L${sd * 190},-130Z`)}</g>`;
      b += `<g class="phair">${Array.from({ length: 9 }, (_, i) => { const a = (-150 + i * 15) * Math.PI / 180; return `<path d="M0,-360Q${f1(Math.cos(a) * 90)},${f1(-360 + Math.sin(a) * 120)} ${f1(Math.cos(a) * 170 + (i % 2) * 16)},${f1(-360 + Math.sin(a) * 210)}" stroke="${C.hair}" stroke-width="${16 - (i % 3) * 3}" fill="none" stroke-linecap="round"/>`; }).join("")}</g>`;
      b += leg(-42, -110, 420) + leg(42, 110, 420) + foot(-110, 420) + foot(110, 420) + tint("M-170,120L170,120L200,520L-200,520Z");
      b += arm(-1, "aL") + arm(1, "aR");
      b += `<g id="${id}-chest"><path d="M-96,-250Q0,-280 96,-250L86,70Q0,92 -86,70Z" fill="${C.tee}" ${OUT}/>
        <path d="M-40,-150q14,-16 28,0t28,0t28,0" stroke="#2f7fbf" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M-36,-128q14,-14 28,0t28,0t28,0" stroke="#5fb0e0" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path d="M-34,-238Q0,-208 34,-238" stroke="${C.teeS}" stroke-width="5" fill="none"/></g>${tint("M-96,-60L96,-60L86,70Q0,92 -86,70Z")}`;
      const face = o.face || "calm";
      const eyes = face === "gasp" ? `<ellipse cx="-28" cy="-346" rx="12" ry="14" fill="#fff" ${OUT3}/><ellipse cx="28" cy="-346" rx="12" ry="14" fill="#fff" ${OUT3}/><circle cx="-28" cy="-346" r="5" fill="${INK}"/><circle cx="28" cy="-346" r="5" fill="${INK}"/>`
        : face === "open" ? `<circle cx="-28" cy="-346" r="7" fill="${INK}"/><circle cx="28" cy="-346" r="7" fill="${INK}"/>`
        : `<path d="M-40,-346q12,8 24,0M16,-346q12,8 24,0" stroke="${INK}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
      const mouth = face === "gasp" ? `<ellipse cx="0" cy="-292" rx="16" ry="20" fill="#5a1f1a" ${OUT3}/>` : `<ellipse id="${id}-mouth" cx="0" cy="-294" rx="9" ry="7" fill="#7a2f2a"/>`;
      b += `<rect x="-26" y="-300" width="52" height="60" fill="${C.skin}"/><g id="${id}-head"><ellipse cx="0" cy="-340" rx="80" ry="94" fill="${C.skin}" ${OUT}/>
        <path d="M-80,-360Q-74,-438 0,-440Q74,-438 80,-360Q60,-404 0,-410Q-60,-404 -80,-360Z" fill="${C.hair}" ${OUT3}/>${eyes}<path d="M-4,-326q4,10 0,14" stroke="${C.skinS}" stroke-width="4" fill="none"/>${mouth}
        <g fill="#e09a86" opacity=".5"><ellipse cx="-46" cy="-314" rx="11" ry="5"/><ellipse cx="46" cy="-314" rx="11" ry="5"/></g>
        ${[[-60, -300], [52, -380], [20, -270]].map(([dx, dy]) => `<path d="M${dx},${dy}c5,9 7,14 2,17c-5,-3 -5,-8 -2,-17z" fill="#cfe2e6" opacity=".85"/>`).join("")}</g>`;
      // the waterline around her: a bright rim where the face, chest and hands break the surface
      b += `<ellipse class="rip" cx="0" cy="-300" rx="120" ry="150" fill="none" stroke="#b9c6e8" stroke-width="5" opacity=".55"/><ellipse class="rip" cx="0" cy="-120" rx="190" ry="260" fill="none" stroke="#9fb0d8" stroke-width="3" opacity=".35"/>`;
    } else {
      // face down, freestyle: one arm reaching ahead, the other pulling back along the body (two key poses swapped)
      const armL = (x0, y0, x1, y1, x2, y2) => `<path d="M${x0},${y0}L${x1},${y1}L${x2},${y2}" stroke="${INK}" stroke-width="62" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M${x0},${y0}L${x1},${y1}L${x2},${y2}" stroke="${C.skin}" stroke-width="52" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M${x0},${y0}L${f1(x0 + (x1 - x0) * 0.45)},${f1(y0 + (y1 - y0) * 0.45)}" stroke="${C.tee}" stroke-width="62" stroke-linecap="round"/><ellipse cx="${x2}" cy="${y2}" rx="36" ry="40" fill="${C.skin}" ${OUT}/>`;
      const spl = (x, y, k) => `<g opacity=".95">${Array.from({ length: 9 }, (_, i) => { const a = (i / 9) * Math.PI * 2; return `<ellipse cx="${f1(x + Math.cos(a) * 60 * k)}" cy="${f1(y + Math.sin(a) * 50 * k)}" rx="${f1(12 * k)}" ry="${f1(16 * k)}" fill="#e3eeff"/>`; }).join("")}<ellipse cx="${x}" cy="${y}" rx="${70 * k}" ry="${56 * k}" fill="none" stroke="#e3eeff" stroke-width="8"/></g>`;
      b += `<g id="${id}-wake" opacity=".7">${[0, 1, 2, 3, 4, 5].map((k) => `<ellipse class="rip" cx="${(k % 2 ? 40 : -40)}" cy="${560 + k * 120}" rx="${60 + k * 22}" ry="${30 + k * 8}" fill="none" stroke="#dfeaff" stroke-width="${8 - k}" opacity="${(0.7 - k * 0.1).toFixed(2)}"/>`).join("")}</g>`;
      b += leg(-42, -70, 430) + leg(42, 70, 440) + foot(-70, 430) + foot(70, 440) + tint("M-140,120L140,120L150,520L-150,520Z");
      b += `<g id="${id}-kick">${spl(-70, 480, 0.8)}</g><g id="${id}-kick2" opacity="0">${spl(70, 490, 0.8)}</g>`;
      b += `<path d="M-96,-250Q0,-280 96,-250L86,70Q0,92 -86,70Z" fill="${C.tee}" ${OUT}/><path d="M-30,-250V60" stroke="${C.teeS}" stroke-width="4" opacity=".6"/>${tint("M-96,-120L96,-120L86,70Q0,92 -86,70Z")}`;
      b += `<g id="${id}-stA">${armL(80, -210, 120, -470, 90, -700)}${armL(-80, -210, -130, -40, -120, 120)}${spl(90, -720, 1)}</g>`;
      b += `<g id="${id}-stB" opacity="0">${armL(-80, -210, -120, -470, -90, -700)}${armL(80, -210, 130, -40, 120, 120)}${spl(-90, -720, 1)}</g>`;
      // back of the head: wet hair, the ponytail trailing down the back, goggle strap
      b += `<ellipse cx="0" cy="-330" rx="78" ry="90" fill="${C.hair}" ${OUT}/><path d="M0,-260Q30,-160 6,-60" stroke="${C.hair}" stroke-width="30" fill="none" stroke-linecap="round"/><circle cx="0" cy="-262" r="14" fill="#2f7fbf" ${OUT3}/>
        <path d="M-78,-330Q0,-300 78,-330" stroke="#4fb0e0" stroke-width="10" fill="none"/>${tint("M-80,-300Q0,-260 80,-300L80,-240H-80Z")}`;
      b += `<ellipse class="rip" cx="0" cy="-200" rx="150" ry="300" fill="none" stroke="#dfeaff" stroke-width="6" opacity=".5"/>`;
    }
    // the hand on her right ankle: a grey-green forearm coming up from the dark below, fingers round the ankle
    const ph = `<g id="${id}-ph" opacity="${o.ph ?? 0}"><g transform="translate(${o.pose === "prone" ? 70 : 110},${o.pose === "prone" ? 470 : 450})">
      <path d="M-30,40L40,330L120,330L60,20Z" fill="url(#p3Fade)"/><path d="M-30,40L40,330M60,20L120,330" stroke="${P.GRIM}" stroke-width="4" opacity=".7"/>
      ${[[-50, -20], [-48, 6], [-44, 30]].map(([x, y], k) => `<path d="M${x},${y}Q${-10},${y - 34} ${48},${y - 10 + k * 4}" stroke="${P.GRIM}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M${x},${y}Q${-10},${y - 34} ${48},${y - 10 + k * 4}" stroke="${P.GBL2}" stroke-width="13" fill="none" stroke-linecap="round"/><circle cx="${48}" cy="${y - 10 + k * 4}" r="5" fill="#000"/>`).join("")}
      <path d="M60,30Q70,0 54,-30" stroke="${P.GRIM}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M60,30Q70,0 54,-30" stroke="${P.GBL2}" stroke-width="15" fill="none" stroke-linecap="round"/></g></g>`;
    put(L.act, `<g id="${id}-swo"><g id="${id}-sw" transform="translate(${sx},${sy}) rotate(${rot}) scale(${ss})">${b}${ph}</g></g>`);
    put(L.glow, `<circle cx="${mx}" cy="${my}" r="200" fill="url(#p3Moon)" opacity=".6"/>`);
  }

  // ---------------- on her back, looking up at the moon ----------------
  function moonPOV(L, o = {}) {
    const id = o.id || "mp", r = mk(o.seed || 137), mx = o.moonX ?? 540, my = o.moonY ?? 760;
    let s = `<rect x="-900" y="-900" width="2900" height="3800" fill="url(#phSky)"/>`;
    for (let i = 0; i < 160; i++) s += `<circle cx="${f1(-700 + r() * 2500)}" cy="${f1(-700 + r() * 3000)}" r="${f1(1 + r() * 2.6)}" fill="#e8ecff" opacity="${(0.3 + r() * 0.6).toFixed(2)}"/>`;
    s += `<circle cx="${mx}" cy="${my}" r="900" fill="url(#phHalo)"/><circle cx="${mx}" cy="${my}" r="170" fill="url(#phMoon)"/>
      <circle cx="${mx - 50}" cy="${my - 20}" r="30" fill="#d9d0ae" opacity=".5"/><circle cx="${mx + 44}" cy="${my + 50}" r="22" fill="#d9d0ae" opacity=".45"/><circle cx="${mx + 20}" cy="${my - 70}" r="14" fill="#d9d0ae" opacity=".4"/>`;
    put(L.sky, s);
    put(L.mid, `<g opacity=".5">${[[-200, 400, 700], [700, 1100, 600], [-100, 1500, 800]].map(([x, y, w]) => `<path d="M${x},${y}q${w * 0.2},-40 ${w * 0.45},-10q${w * 0.2},-36 ${w * 0.55},10q-${w * 0.4},30 -${w},0z" fill="#3a4870"/>`).join("")}</g>`);
    // the river lapping over the bottom of the lens, and a thin film of water at the edges
    put(L.light, `<g id="${id}-lap"><path d="M-200,1760Q60,1700 300,1750T780,1740T1280,1760V2200H-200Z" fill="#14223f" opacity=".92"/><path d="M-200,1760Q60,1700 300,1750T780,1740T1280,1760" stroke="#b9c6e8" stroke-width="8" fill="none" opacity=".7"/>
      ${[0, 1, 2, 3].map((k) => `<path d="M${-100 + k * 320},${1800 + (k % 2) * 30}h120" stroke="#9fb0d8" stroke-width="5" stroke-linecap="round" opacity=".5"/>`).join("")}</g>
      <rect x="0" y="0" width="1080" height="1920" fill="none" stroke="#14223f" stroke-width="90" opacity=".45"/>`);
  }

  // ---------------- under the river: the ankle kicking, the hand closing on it ----------------
  function ankleGrab(L, o = {}) {
    const id = o.id || "ag";
    Sets.underRiver(L, { id: `${id}u`, surface: o.surface ?? 220, seed: 141 });
    const leg = `<g id="${id}-leg"><path d="M420,-400L470,700" stroke="${INK}" stroke-width="190" stroke-linecap="round"/><path d="M420,-400L470,700" stroke="${C.pants}" stroke-width="176" stroke-linecap="round"/><path d="M360,-400L404,700" stroke="#f2f0ea" stroke-width="10" opacity=".8"/>
      <path d="M470,700L480,960" stroke="${INK}" stroke-width="128" stroke-linecap="round"/><path d="M470,700L480,960" stroke="${C.skin}" stroke-width="116" stroke-linecap="round"/>
      <path d="M440,940C430,1080 470,1160 560,1170L760,1180C810,1180 830,1130 800,1100C760,1060 640,1030 540,960Z" fill="${C.skin}" ${OUT}/>
      <rect x="380" y="640" width="190" height="70" rx="16" fill="${C.pantsS}" ${OUT}/></g>`;
    // the hand: a tapered grey-green forearm rising from the dark (fading out below), four long fingers curled round the front of
    // the ankle with dark nails, the thumb round the back (#id-fing scales from open to shut about the palm)
    const fing = (k) => { const y = 880 + k * 44, x1 = 330 + k * 6; return `<path d="M640,${y + 20}C560,${y - 40} ${x1 + 60},${y - 50} ${x1},${y + 6}" stroke="${P.GRIM}" stroke-width="48" fill="none" stroke-linecap="round"/>
      <path d="M640,${y + 20}C560,${y - 40} ${x1 + 60},${y - 50} ${x1},${y + 6}" stroke="url(#phPale)" stroke-width="38" fill="none" stroke-linecap="round"/><ellipse cx="${x1 + 4}" cy="${y + 4}" rx="12" ry="9" fill="#000"/>
      <path d="M${520 - k * 4},${y - 28}q8,6 4,14" stroke="${P.GVEIN}" stroke-width="3" fill="none"/>`; };
    const hand = `<g id="${id}-hand"><path d="M620,1960C600,1560 610,1220 600,1010L760,1000C770,1230 790,1560 820,1960Z" fill="url(#phPale)" stroke="${P.GRIM}" stroke-width="4"/><path d="M620,1960C600,1560 610,1220 600,1010L760,1000C770,1230 790,1560 820,1960Z" fill="#0a1b1a" opacity=".35"/>
      <path d="M640,1400q20,-60 6,-130M720,1600q-14,-70 4,-150" stroke="${P.GVEIN}" stroke-width="4" fill="none"/>
      <path d="M590,1040C580,960 600,880 680,860C760,850 800,930 790,1010Z" fill="url(#phPale)" stroke="${P.GRIM}" stroke-width="4"/>
      <g id="${id}-fing">${[0, 1, 2, 3].map(fing).join("")}
        <path d="M780,980C820,930 790,860 740,840" stroke="${P.GRIM}" stroke-width="50" fill="none" stroke-linecap="round"/><path d="M780,980C820,930 790,860 740,840" stroke="url(#phPale)" stroke-width="40" fill="none" stroke-linecap="round"/><ellipse cx="742" cy="842" rx="12" ry="9" fill="#000"/></g>
      <rect x="560" y="1500" width="300" height="480" fill="url(#phUnder)" opacity=".8"/></g>`;
    put(L.act, leg + hand); // the arm fades into the deep: no loose head beside it (user: "มือกับหัวไม่ติดกันหรอ")
    put(L.light, `<rect x="-200" y="-200" width="1480" height="2320" fill="#0d2a28" opacity=".22"/>`);
  }

  // ---------------- hospital room at dawn ----------------
  function ward(L, o = {}) {
    const id = o.id || "wd", r = mk(o.seed || 149), G = o.ground ?? 1480, BT = o.bed ?? G - 330;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#1b2420"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="url(#p3Wall)"/><rect x="-900" y="${G - 220}" width="2900" height="220" fill="#8fa89c"/><path d="M-900,${G - 220}H2000" stroke="#6f8a7e" stroke-width="8"/>`;
    // the window onto the river at sunrise (+ a ferry far out, #id-boat)
    const WX = o.win ?? 760;
    s += `<g><rect x="${WX}" y="${G - 1180}" width="520" height="640" fill="url(#p3Dawn)"/><circle cx="${WX + 330}" cy="${G - 640}" r="60" fill="#ffe6b0"/><circle cx="${WX + 330}" cy="${G - 640}" r="220" fill="url(#p3Sun)"/>
      <path d="M${WX},${G - 640}${Array.from({ length: 14 }, (_, k) => `L${WX + k * 40},${G - 660 - (k % 3) * 16}`).join("")}L${WX + 520},${G - 640}V${G - 600}H${WX}Z" fill="#3a3040"/>
      <rect x="${WX}" y="${G - 600}" width="520" height="60" fill="#c98a6a"/><path d="M${WX + 260},${G - 590}h120M${WX + 300},${G - 570}h80" stroke="#ffe6b0" stroke-width="5" opacity=".8"/>
      <g id="${id}-boat"><path d="M${WX + 80},${G - 586}h90q-10,14 -24,16h-50q-12,-4 -16,-16z" fill="#2a2024"/><path d="M${WX + 104},${G - 586}v-30" stroke="#2a2024" stroke-width="6"/><circle cx="${WX + 104}" cy="${G - 626}" r="9" fill="#2a2024"/><circle cx="${WX + 160}" cy="${G - 596}" r="5" fill="#ffd38a"/></g>
      <rect x="${WX - 20}" y="${G - 1200}" width="560" height="680" fill="none" stroke="#e8ece6" stroke-width="28"/><path d="M${WX + 260},${G - 1200}V${G - 520}M${WX - 20},${G - 860}H${WX + 540}" stroke="#e8ece6" stroke-width="16"/>
      <rect x="${WX - 40}" y="${G - 530}" width="600" height="30" fill="#d9dfda" ${OUT3}/></g>`;
    // curtain rail + a pale blue curtain bunched at the left
    s += `<path d="M-700,${G - 1300}H${WX - 60}" stroke="#9aa6a0" stroke-width="10"/><path d="M-700,${G - 1300}Q-640,${G - 700} -700,${G - 120}H-520Q-560,${G - 700} -520,${G - 1300}Z" fill="#9fc4d8" ${OUT3}/>${[-660, -600].map((x) => `<path d="M${x},${G - 1290}Q${x + 20},${G - 700} ${x},${G - 130}" stroke="#7fa4b8" stroke-width="5" fill="none"/>`).join("")}`;
    // the floor
    s += `<rect x="-900" y="${G}" width="2900" height="1200" fill="#cfd8d2"/>${Array.from({ length: 30 }, (_, k) => `<path d="M${-900 + k * 120},${G}V${G + 1200}" stroke="#b9c4bd" stroke-width="3"/>`).join("")}${Array.from({ length: 10 }, (_, k) => `<path d="M-900,${G + 60 + k * 120}H2000" stroke="#b9c4bd" stroke-width="3"/>`).join("")}`;
    // the drip stand
    s += `<g><path d="M-40,${G}V${G - 1000}" stroke="#a8b0b4" stroke-width="12"/><path d="M-110,${G}h140" stroke="#a8b0b4" stroke-width="12"/><path d="M-90,${G - 1000}h100" stroke="#a8b0b4" stroke-width="8"/>
      <path d="M-80,${G - 990}h60v120q0,24 -30,24t-30,-24z" fill="#e6f2f6" fill-opacity=".85" ${OUT3}/><path d="M-50,${G - 846}Q-40,${G - 600} 120,${BT - 40}" stroke="#d9e6ea" stroke-width="5" fill="none"/></g>`;
    // the bed: head at the left, rails, white sheet, pillow
    const BX0 = o.bedX0 ?? 60, BX1 = o.bedX1 ?? 780;
    s += `<g><rect x="${BX0 - 30}" y="${BT - 260}" width="34" height="${G - BT + 260}" rx="8" fill="#c9d0d4" ${OUT3}/><rect x="${BX1}" y="${BT - 120}" width="30" height="${G - BT + 120}" rx="8" fill="#c9d0d4" ${OUT3}/>
      <rect x="${BX0}" y="${BT + 40}" width="${BX1 - BX0}" height="60" fill="#a8b0b4" ${OUT3}/>${[BX0 + 40, BX1 - 60].map((x) => `<rect x="${x}" y="${BT + 100}" width="20" height="${G - BT - 140}" fill="#8f979b"/><circle cx="${x + 10}" cy="${G - 24}" r="22" fill="#4a4f52"/>`).join("")}
      <rect x="${BX0}" y="${BT - 20}" width="${BX1 - BX0}" height="66" rx="18" fill="#f4f6f4" ${OUT3}/><ellipse cx="${BX0 + 110}" cy="${BT - 30}" rx="100" ry="36" fill="#ffffff" ${OUT3}/></g>`;
    // the chair by the bed
    if (o.chair !== false) s += `<g><rect x="${BX1 + 90}" y="${G - 300}" width="200" height="30" rx="8" fill="#6a7a8a" ${OUT3}/><rect x="${BX1 + 260}" y="${G - 560}" width="30" height="280" rx="8" fill="#6a7a8a" ${OUT3}/><path d="M${BX1 + 100},${G - 270}V${G}M${BX1 + 280},${G - 270}V${G}" stroke="#4a5562" stroke-width="12"/></g>`;
    put(L.set, s);
    // the blanket that goes over whoever is in the bed (the shot moves it to the top of the act layer)
    put(L.act, `<g id="${id}-blanket"><path d="M${BX0 + 250},${BT - 190}Q${(BX0 + BX1) / 2},${BT - 230} ${BX1 - 30},${BT - 150}Q${BX1 + 10},${BT - 60} ${BX1 + 14},${BT + 60}H${BX0 + 230}Z" fill="#cfe0ea" ${OUT}/><path d="M${BX0 + 250},${BT - 190}l-20,250" stroke="#a8c4d4" stroke-width="12"/>
      ${[0, 1, 2].map((k) => `<path d="M${BX0 + 330 + k * 130},${BT - 190 + k * 8}q24,110 0,230" stroke="#a8c4d4" stroke-width="5" fill="none"/>`).join("")}</g>`);
    put(L.light, `<path d="M${WX},${G - 1180}L${WX + 520},${G - 1180}L${WX + 300},${G + 600}L${WX - 700},${G + 600}Z" fill="#ffd9a0" opacity=".12"/>`);
    put(L.glow, `<circle cx="${WX + 330}" cy="${G - 640}" r="700" fill="url(#p3Sun)" opacity=".35"/>`);
  }

  // ---------------- the legend of ตาเหม, in shadow puppets ----------------
  function mhemLegend(L, o = {}) {
    const id = o.id || "ml", Pk = "#170d06", CUT = "#ffd9a0", ROD = "#3a2414", LGY = [0, 1600];
    put(L.sky, `<rect x="-900" y="-1200" width="2900" height="5200" fill="#1c1009"/>`);
    const screen = (y0, y1) => `<rect x="-40" y="${y0}" width="1160" height="${y1 - y0}" fill="#e9a457"/><circle class="lamp" cx="540" cy="${(y0 + y1) / 2}" r="${(y1 - y0) * 0.75}" fill="url(#clothglow)"/>
      ${Array.from({ length: 30 }, (_, k) => `<path d="M${-40 + k * 40},${y0}V${y1}" stroke="#c98a44" stroke-width="1.5" opacity=".25"/>`).join("")}
      <path d="M-40,${y0}H1120" stroke="${Pk}" stroke-width="18"/><path d="M-40,${y1}H1120" stroke="${Pk}" stroke-width="18"/>
      <path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y0 + 8}l21,26l21,-26`).join("")}" fill="${Pk}"/><path d="${Array.from({ length: 28 }, (_, k) => `M${-40 + k * 42},${y1 - 8}l21,-26l21,26`).join("")}" fill="${Pk}"/>`;
    const rod = (x, y, len = 220) => `<path d="M${x},${y}V${y + len}" stroke="${ROD}" stroke-width="6"/>`;
    const waves = (y, h = 460) => `<path d="M-40,${y}${Array.from({ length: 24 }, () => `q24,-22 48,0`).join("")}V${y + h}H-40Z" fill="${Pk}" opacity=".9"/>
      ${Array.from({ length: 6 }, (_, k) => `<path d="M${40 + k * 180},${y + 60 + (k % 2) * 40}q30,-14 60,0t60,0" stroke="${CUT}" stroke-width="5" fill="none" opacity=".55"/>`).join("")}`;
    // the young ferryman: งอบ hat, lean, a cut-out eye; the child: small, arms up
    const man = (s) => `<g transform="scale(${s})"><path d="M-70,-236Q0,-290 70,-236Z" fill="${Pk}"/><circle cx="0" cy="-206" r="30" fill="${Pk}"/><ellipse cx="10" cy="-210" rx="6" ry="4" fill="${CUT}"/><path d="M-40,-30L-30,-176H30L40,-30Z" fill="${Pk}"/>
      <path d="M-14,-30V40M14,-30V40" stroke="${Pk}" stroke-width="13"/><path d="M-28,-164L-70,-250M28,-164L70,-250" stroke="${Pk}" stroke-width="12" stroke-linecap="round"/><path d="M-30,-60h60" stroke="${CUT}" stroke-width="5" opacity=".7"/></g>`;
    const child = (s) => `<g transform="scale(${s})"><circle cx="0" cy="-150" r="24" fill="${Pk}"/><path d="M-26,-20L-20,-126H20L26,-20Z" fill="${Pk}"/><path d="M-18,-118L-52,-190M18,-118L52,-190" stroke="${Pk}" stroke-width="10" stroke-linecap="round"/></g>`;
    let s = LGY.map((y) => screen(y, y + 900)).join("");
    // S1: the pier on the left, the child in the waves, a krathong, the man in mid-dive (#id-dive, pivot at its centre)
    s += `<circle cx="860" cy="140" r="54" fill="${CUT}"/>` + waves(420);
    s += `<rect x="-40" y="330" width="380" height="36" fill="${Pk}"/>${[20, 160, 300].map((x) => `<rect x="${x}" y="366" width="20" height="400" fill="${Pk}"/>`).join("")}`;
    s += `<g id="${id}-kid">${rod(760, 520)}<g transform="translate(760,520) rotate(-8)">${child(0.9)}</g></g>`;
    s += `<g transform="translate(900,428)"><path d="M-46,0Q0,-28 46,0Z" fill="${Pk}"/><path d="M-18,-12Q0,-54 18,-12Z" fill="${Pk}"/><circle class="lamp" cx="0" cy="-66" r="9" fill="#fff2c8"/></g>`;
    s += `<g id="${id}-dive" transform="translate(300,250) rotate(0)">${rod(0, 0, 160)}<g transform="rotate(-70)">${man(0.85)}</g></g>`;
    // S2: under water — the child round his neck, both going down; bubbles; an oar left on the surface
    const Y = LGY[1];
    s += `<path d="M-40,${Y + 200}${Array.from({ length: 24 }, () => `q24,-18 48,0`).join("")}V${Y + 900}H-40Z" fill="#3a1e0c" opacity=".55"/>`;
    s += `<g id="${id}-oar"><path d="M300,${Y + 180}L760,${Y + 150}" stroke="${Pk}" stroke-width="14" stroke-linecap="round"/><path d="M760,${Y + 150}l90,-20l10,40l-92,-6z" fill="${Pk}"/></g>`;
    s += `<g id="${id}-pair">${rod(540, Y + 560)}<g transform="translate(540,${Y + 560}) rotate(12)">${man(0.9)}</g><g transform="translate(500,${Y + 380}) rotate(-30)">${child(0.75)}</g>
      <path d="M512,${Y + 330}Q560,${Y + 300} 588,${Y + 352}" stroke="${Pk}" stroke-width="12" fill="none" stroke-linecap="round"/></g>`;
    for (let k = 0; k < 8; k++) s += `<circle class="bub" data-i="${k}" cx="${520 + (k % 3) * 30}" cy="${Y + 300 - k * 22}" r="${6 + (k % 3) * 3}" fill="none" stroke="${CUT}" stroke-width="3"/>`;
    put(L.set, s);
  }

  // ---------------- แพรว's ankle on the hospital sheet: five finger marks ----------------
  function ankleP(L, o = {}) {
    const id = o.id || "ap", r = mk(o.seed || 151), sk = C.skin;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#e8eeea"/>`);
    let m = "";
    for (let k = 0; k < 9; k++) m += `<path d="M${-200 + k * 160},-600Q${-120 + k * 160},800 ${-220 + k * 170},2600" stroke="#cfd8d4" stroke-width="6" fill="none"/>`;
    put(L.mid, m + `<rect x="-900" y="-600" width="2900" height="3400" fill="#ffd9a0" opacity=".12"/>`);
    let a = `<path d="M150,-300C170,300 210,700 240,980L560,1020C540,700 520,300 520,-300Z" fill="${sk}" ${OUT}/>
      <path d="M240,980C220,1120 250,1240 370,1280L860,1300C930,1300 960,1240 920,1190C860,1130 700,1100 560,1020Z" fill="${sk}" ${OUT}/>
      ${[0, 1, 2, 3, 4].map((t) => `<ellipse cx="${940 - t * 3}" cy="${1210 + t * 18}" rx="${22 - t * 2}" ry="14" fill="${sk}" ${OUT}/>`).join("")}
      <path d="M120,-600L130,240Q340,290 560,240L560,-600Z" fill="${C.pants}" ${OUT}/><path d="M130,200Q340,250 560,200" stroke="${C.pantsS}" stroke-width="12" fill="none"/><path d="M200,-600L196,220" stroke="#f2f0ea" stroke-width="10"/>`;
    const fing = (x0, y0, x1, y1, w) => `<path d="M${x0},${y0}Q${(x0 + x1) / 2},${Math.min(y0, y1) - 26} ${x1},${y1}" stroke="#4f6a5c" stroke-width="${w + 14}" fill="none" stroke-linecap="round" opacity=".28"/>
      <path d="M${x0},${y0}Q${(x0 + x1) / 2},${Math.min(y0, y1) - 26} ${x1},${y1}" stroke="#3d5548" stroke-width="${w}" fill="none" stroke-linecap="round" opacity=".7"/><ellipse cx="${x1}" cy="${y1}" rx="${w * 0.55}" ry="${w * 0.45}" fill="#26362e" opacity=".85"/>`;
    a += `<g id="${id}-marks" opacity="${o.marks ?? 1}">${fing(204, 690, 460, 668, 30)}${fing(208, 752, 490, 738, 32)}${fing(214, 814, 496, 806, 31)}${fing(222, 870, 460, 872, 26)}
      <path d="M538,610C510,690 510,760 530,812" stroke="#3d5548" stroke-width="34" fill="none" stroke-linecap="round" opacity=".6"/><ellipse cx="530" cy="812" rx="16" ry="13" fill="#26362e" opacity=".8"/></g>`;
    for (let k = 0; k < 6; k++) a += `<path d="M${f1(240 + r() * 280)},${f1(600 + r() * 500)}c5,9 7,14 2,17c-5,-3 -5,-8 -2,-17z" fill="#cfe2e6" opacity=".7"/>`;
    put(L.set, a);
    put(L.glow, `<circle cx="700" cy="300" r="900" fill="url(#p3Sun)" opacity=".35"/>`);
  }

  // the hospital landing (props for Sets.pierDeck): a white two-storey block behind the deck, lit windows, the green cross sign
  const hosp = (G) => `<g><rect x="-900" y="${G - 1100}" width="1300" height="1100" fill="#d9dedb" ${OUT}/><rect x="-900" y="${G - 1130}" width="1340" height="40" fill="#9aa4a0" ${OUT3}/>
    ${[0, 1].map((row) => [0, 1, 2, 3].map((c) => `<rect x="${-820 + c * 300}" y="${G - 1020 + row * 440}" width="180" height="220" fill="${(row + c) % 3 ? "#ffe3a8" : "#3a4a52"}" ${OUT3}/>`).join("")).join("")}
    <g transform="translate(200,${G - 1260})"><rect x="-200" y="-70" width="400" height="140" rx="12" fill="#f4f6f4" ${OUT}/><path d="M-150,-28h28v-28h28v28h28v28h-28v28h-28v-28h-28z" fill="#2fa05a"/>
      <text x="40" y="20" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="46" fill="#2a5a3a">โรงพยาบาล</text></g>
    <rect x="-900" y="${G - 160}" width="1340" height="160" fill="#b9c0bc"/>${[0, 1, 2].map((k) => `<rect x="${440 + k * 60}" y="${G - 120 + k * 40}" width="${200 - k * 60}" height="40" fill="#c9d0cc" ${OUT3}/>`).join("")}</g>`;
  const hospGlow = (G) => [0, 1, 2, 3].map((c) => `<circle cx="${-730 + c * 300}" cy="${G - 910}" r="160" fill="url(#phBulb)" opacity=".45"/>`).join("") + `<circle cx="200" cy="${G - 1260}" r="260" fill="#2fa05a" opacity=".18"/>`;

  // ---------------- card icons ----------------
  if (window.GameUI) {
    const K = INK, O = `stroke="${K}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
    const WATER = `<path d="M8,78q13,-8 26,0t26,0t26,0t26,0V112H8Z" fill="#4f8fbf" ${O}/>`;
    const NO = `<g class="a-pulse"><circle cx="60" cy="60" r="50" fill="none" stroke="#e0362c" stroke-width="9"/><path d="M25,25L95,95" stroke="#e0362c" stroke-width="9" stroke-linecap="round"/></g>`;
    Object.assign(GameUI.ILL, {
      // a swimmer thrashing flat out, speed splashes — crossed out
      noswim: `${WATER}<g class="a-bob"><circle cx="38" cy="66" r="10" fill="#efc6a0" ${O}/><path d="M48,70L92,74" stroke="${K}" stroke-width="12" stroke-linecap="round"/><path d="M48,70L92,74" stroke="#f2f0ea" stroke-width="6" stroke-linecap="round"/>
        <path d="M44,62L60,36L78,44" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/></g>${[0, 1, 2].map((i) => `<path class="a-wave" data-i="${i}" d="M${96 + i * 6},${58 - i * 8}l10,-6" stroke="#dfeaff" stroke-width="5" stroke-linecap="round"/>`).join("")}${NO}`,
      // the face above the waterline, breath puffs
      mouthup: `${WATER}<g class="a-bob"><circle cx="60" cy="56" r="26" fill="#efc6a0" ${O}/><circle cx="52" cy="50" r="3.5" fill="${K}"/><circle cx="68" cy="50" r="3.5" fill="${K}"/><ellipse cx="60" cy="66" rx="6" ry="5" fill="#7a2f2a"/></g>
        ${[0, 1].map((i) => `<circle class="a-wave" data-i="${i}" cx="${84 + i * 12}" cy="${40 - i * 10}" r="${5 + i * 2}" fill="none" stroke="#dfeaff" stroke-width="4"/>`).join("")}<path d="M10,78q13,-8 26,0t26,0t26,0t26,0" stroke="#dfeaff" stroke-width="4" fill="none"/>`,
      // lying on her back on the water, arms out
      floatback: `${WATER}<g class="a-bob"><circle cx="24" cy="70" r="11" fill="#efc6a0" ${O}/><path d="M34,72L98,74" stroke="${K}" stroke-width="14" stroke-linecap="round"/><path d="M34,72L98,74" stroke="#f2f0ea" stroke-width="8" stroke-linecap="round"/>
        <path d="M48,72L40,50M56,72L66,52" stroke="${K}" stroke-width="7" stroke-linecap="round"/></g><path d="M10,80q13,-8 26,0t26,0t26,0t26,0" stroke="#dfeaff" stroke-width="4" fill="none"/>`,
      // a hand sculling: small arcs either side
      paddle: `${WATER}<g class="a-pulse"><path d="M60,92V60" stroke="${K}" stroke-width="16" stroke-linecap="round"/><path d="M60,92V60" stroke="#efc6a0" stroke-width="10" stroke-linecap="round"/><ellipse cx="60" cy="52" rx="16" ry="12" fill="#efc6a0" ${O}/></g>
        <path class="a-wave" data-i="0" d="M30,52q-12,10 0,20" stroke="#dfeaff" stroke-width="5" fill="none" stroke-linecap="round"/><path class="a-wave" data-i="1" d="M90,52q12,10 0,20" stroke="#dfeaff" stroke-width="5" fill="none" stroke-linecap="round"/>`,
      // a swimmer's head with an arrow to a ladder at the bank
      toexit: `${WATER}<path d="M84,20V96M108,20V96M84,40h24M84,62h24M84,84h24" stroke="#8a5f3c" stroke-width="6" stroke-linecap="round"/><circle cx="28" cy="72" r="10" fill="#efc6a0" ${O}/>
        <g class="a-wave" data-i="0"><path d="M44,60H72M64,52l9,8l-9,8" stroke="#3fb86a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`,
      // arms over the gallon, floating
      holdfloat: `${WATER}<g class="a-bob"><rect x="46" y="54" width="44" height="40" rx="8" fill="#e9eef0" ${O}/><rect x="56" y="46" width="14" height="10" fill="#e04a3a" ${O}/><circle cx="34" cy="60" r="12" fill="#efc6a0" ${O}/>
        <path d="M40,70L80,66" stroke="${K}" stroke-width="10" stroke-linecap="round"/><path d="M40,70L80,66" stroke="#efc6a0" stroke-width="5" stroke-linecap="round"/></g>`,
    });
  }

  Object.assign(Sets, { riverTop, moonPOV, ankleGrab, ward, mhemLegend, ankleP });
  window.Phrai3 = { ktop, galTop, hosp, hospGlow };
})();
