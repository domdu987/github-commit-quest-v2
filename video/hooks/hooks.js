// Hook stills (lane C, 1 Nov): two new worlds for the "movie" hooks.
//   Sets.caveFlood(L, o)  a cave chamber after the rain: black rock, dripping stalactites, a muddy flood up to the chest,
//                         the way out (an arch at the back) drowned under the water, a jet of water pouring in from a crack,
//                         a high dry ledge on the right. Headlamps are the only light: o.beams [[x, y, deg, len]] cut cones
//                         out of the dark (#id-dark). o.wl = water level (world y), o.rise = how much the water climbs (tween #id-wtr)
//   Sets.sharkSea(L, o)   a split-level view at dusk: the sky and swell above the line o.sl, the deep blue below with sun
//                         shafts; a surfboard at the surface; a big shark below (#id-shark at o.shark = [x, y, s, deg]) and a
//                         dorsal fin cutting the surface (#id-fin at o.fin = [x, s]) with its wake
//   cast: cav1 (บอส, 16, headlamp helmet) cav2 (มิ้น, 17) cav3 (โค้ชเจต, 30) · surf (ปลายฟ้า, 19, rash guard)
(function () {
  const { f1, put } = Pop2;
  const INK = "#1e2228";
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  Sets.DEFS += `
    <linearGradient id="cvRock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a6a58"/><stop offset="1" stop-color="#3a3028"/></linearGradient>
    <linearGradient id="cvRock2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a4e42"/><stop offset=".5" stop-color="#8a7a66"/><stop offset="1" stop-color="#4a3e34"/></linearGradient>
    <linearGradient id="cvWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a6a48" stop-opacity=".82"/><stop offset=".3" stop-color="#4a4a32" stop-opacity=".92"/><stop offset="1" stop-color="#1e1e14" stop-opacity=".98"/></linearGradient>
    <radialGradient id="cvBeam" cx="0" cy=".5" r="1"><stop offset="0" stop-color="#fff6d8" stop-opacity=".55"/><stop offset=".6" stop-color="#ffe8a8" stop-opacity=".18"/><stop offset="1" stop-color="#ffe8a8" stop-opacity="0"/></radialGradient>
    <radialGradient id="cvLamp"><stop offset="0" stop-color="#fffbe8"/><stop offset=".3" stop-color="#fff0b0" stop-opacity=".8"/><stop offset="1" stop-color="#ffe080" stop-opacity="0"/></radialGradient>
    <linearGradient id="skSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a6a"/><stop offset=".55" stop-color="#d8785a"/><stop offset="1" stop-color="#ffc07a"/></linearGradient>
    <linearGradient id="skDeep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a8aa8"/><stop offset=".35" stop-color="#145a7a"/><stop offset="1" stop-color="#03141e"/></linearGradient>
    <linearGradient id="skShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8fbff" stop-opacity=".45"/><stop offset="1" stop-color="#e8fbff" stop-opacity="0"/></linearGradient>
    <linearGradient id="skShark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a58"/><stop offset=".55" stop-color="#5a6a78"/><stop offset=".6" stop-color="#c8d0d4"/><stop offset="1" stop-color="#e8ecec"/></linearGradient>
    <linearGradient id="skSwell" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a6a8a"/><stop offset="1" stop-color="#1a4a6a"/></linearGradient>`;

  // ---------------- the flooded cave ----------------
  function caveFlood(L, o = {}) {
    const id = o.id || "cf", WL = o.wl ?? 1300;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="3200" fill="#0a0806"/>`);
    // far: the back wall with the drowned way out (an arch whose top is now under the water), the inflow jet from a crack
    let far = `<path d="M-1400,-900H2500V2400H-1400Z" fill="#1e1814"/>
      <path d="M220,${WL - 40}Q240,${WL - 380} 540,${WL - 420}Q840,${WL - 380} 860,${WL - 40}" fill="#0a0806" stroke="#3a3028" stroke-width="10"/>
      <path d="M280,${WL - 40}Q300,${WL - 330} 540,${WL - 360}Q780,${WL - 330} 800,${WL - 40}" fill="#050403"/>`;
    put(L.far, far);
    // mid: rock masses with wet highlights and stalactites
    const stal = (x, y, h, w) => `<path d="M${x - w},${y}Q${x - w * 0.3},${y + h * 0.6} ${x},${y + h}Q${x + w * 0.3},${y + h * 0.6} ${x + w},${y}Z" fill="url(#cvRock2)" ${O(3)}/><path d="M${x - w * 0.4},${y + 10}Q${x - w * 0.1},${y + h * 0.5} ${x},${y + h - 6}" stroke="#a89878" stroke-width="3" opacity=".35" fill="none"/>`;
    let mid = `<path d="M-1400,-900H2500V${WL - 700}Q1900,${WL - 820} 1500,${WL - 760}Q1100,${WL - 700} 900,${WL - 780}Q540,${WL - 900} 160,${WL - 780}Q-200,${WL - 680} -600,${WL - 760}Q-1000,${WL - 840} -1400,${WL - 700}Z" fill="url(#cvRock)" ${O(5)}/>
      ${[[-300, WL - 760, 220, 40], [-60, WL - 720, 160, 26], [380, WL - 860, 260, 46], [700, WL - 840, 190, 30], [1180, WL - 740, 240, 40], [1420, WL - 770, 150, 24], [-720, WL - 750, 200, 34]].map(([x, y, h, w]) => stal(x, y, h, w)).join("")}
      <path d="M-1400,${WL - 700}Q-900,${WL - 500} -700,${WL - 200}L-640,${WL + 600}H-1400Z" fill="url(#cvRock)" ${O(5)}/>
      <path d="M2500,${WL - 700}Q1900,${WL - 560} 1700,${WL - 260}L1640,${WL + 600}H2500Z" fill="url(#cvRock)" ${O(5)}/>
      <path d="M-860,${WL - 520}q60,40 40,120M1880,${WL - 480}q-50,50 -20,140" stroke="#a89878" stroke-width="5" opacity=".3" fill="none"/>`;
    put(L.mid, mid);
    // set: the high dry ledge (right) and the crack with the inflow jet (left)
    let s = `<path d="M1180,${WL - 300}Q1300,${WL - 360} 1500,${WL - 340}L1700,${WL - 300}L1700,${WL + 200}H1150Z" fill="url(#cvRock2)" ${O(5)}/><path d="M1200,${WL - 300}Q1320,${WL - 350} 1500,${WL - 330}" stroke="#c8b898" stroke-width="5" opacity=".35" fill="none"/>
      <g id="${id}-jet" transform="translate(${o.jetX ?? 0},0)"><path d="M-560,${WL - 640}q30,10 40,40q40,200 20,${640}h-120q-20,-420 20,-610q10,-60 40,-70z" fill="#e8e8d0" opacity=".75"/>
        ${[0, 1, 2, 3, 4].map((k) => `<path class="cvj" d="M${-560 + k * 18},${WL - 600}q${10 + k * 4},180 ${-6 + k * 6},${600}" stroke="#f4f4e0" stroke-width="${6 - k * 0.6}" opacity=".7" stroke-dasharray="40 30" fill="none"/>`).join("")}</g>`;
    put(L.set, s);
    // the flood (above the actors): murky water from WL down, a bright surface edge, ripples round the bodies, the foam at the jet
    const rip = (o.ripples || []).map(([x, r]) => `<ellipse cx="${x}" cy="${WL + 6}" rx="${r}" ry="${f1(r * 0.16)}" fill="none" stroke="#e8e0c0" stroke-width="4" opacity=".55"/><ellipse cx="${x}" cy="${WL + 10}" rx="${r * 1.5}" ry="${f1(r * 0.22)}" fill="none" stroke="#e8e0c0" stroke-width="3" opacity=".3"/>`).join("");
    put(L.glow, `<g id="${id}-wtr"><rect x="-1400" y="${WL}" width="3900" height="2400" fill="url(#cvWater)"/>
      <path d="M-1400,${WL}Q-1000,${WL - 8} -600,${WL}T200,${WL}T1000,${WL}T1800,${WL}T2600,${WL}" stroke="#d8d0a8" stroke-width="5" fill="none" opacity=".6"/>
      <g opacity=".9"><ellipse cx="540" cy="${WL + 120}" rx="300" ry="150" fill="#6aa878" opacity=".35" filter="url(#p2Soft)"/><path d="M300,${WL + 260}Q310,${WL + 20} 540,${WL - 4}Q770,${WL + 20} 780,${WL + 260}" stroke="#9ad0a8" stroke-width="10" fill="none" opacity=".55"/><path d="M340,${WL + 260}Q350,${WL + 60} 540,${WL + 40}Q730,${WL + 60} 740,${WL + 260}" stroke="#c8f0c8" stroke-width="4" fill="none" opacity=".4" stroke-dasharray="30 20"/></g>${rip}<ellipse cx="${-560 + (o.jetX ?? 0)}" cy="${WL + 10}" rx="160" ry="30" fill="#f4f4e0" opacity=".5"/>
      <g opacity=".22">${Array.from({ length: 14 }, (_, k) => `<path d="M${-1300 + k * 270},${WL + 40 + (k % 3) * 60}h${80 + (k % 4) * 30}" stroke="#e8e0c0" stroke-width="3"/>`).join("")}</g></g>`);
    // the darkness with headlamp cones cut out of it, then the beams themselves (additive look)
    const beams = o.beams || [];
    const cone = ([x, y, d, len], w = 0.42) => { const a = (d * Math.PI) / 180, l = len || 1600, e1 = [x + Math.cos(a - w) * l, y + Math.sin(a - w) * l], e2 = [x + Math.cos(a + w) * l, y + Math.sin(a + w) * l];
      return `M${x},${y}L${f1(e1[0])},${f1(e1[1])}Q${f1(x + Math.cos(a) * l * 1.15)},${f1(y + Math.sin(a) * l * 1.15)} ${f1(e2[0])},${f1(e2[1])}Z`; };
    put(L.glow, `<mask id="${id}-mk"><rect x="-1400" y="-900" width="3900" height="3200" fill="#fff"/>${beams.map((b) => `<path d="${cone(b, 0.3)}" fill="#000" opacity=".7" filter="url(#p2Soft)"/><circle cx="${b[0]}" cy="${b[1]}" r="200" fill="#000" opacity=".55" filter="url(#p2Soft)"/>`).join("")}</mask>
      <rect id="${id}-dark" x="-1400" y="-900" width="3900" height="3200" fill="#040302" opacity="${o.dark ?? 0.86}" mask="url(#${id}-mk)"/>
      <g id="${id}-beams" style="mix-blend-mode:screen">${beams.map((b, k) => `<g id="${id}-b${k}"><path d="${cone(b, 0.24)}" fill="#ffe8a8" opacity=".12"/><path d="${cone(b, 0.1)}" fill="#fff6d8" opacity=".12"/><circle cx="${b[0]}" cy="${b[1]}" r="46" fill="url(#cvLamp)"/></g>`).join("")}</g>`);
  }

  // ---------------- the shark: split-level view at dusk ----------------
  const sharkG = (id) => `<g id="${id}"><path d="M-520,0C-420,-90 -150,-150 120,-130C300,-118 430,-70 520,-6C430,40 300,70 120,80C-120,96 -380,70 -520,0Z" fill="url(#skShark)" ${O(5)}/>
      <path d="M-40,-128L40,-300Q70,-240 120,-128Z" fill="#3a4a58" ${O(5)}/><path d="M-20,40L-170,190Q-60,150 60,64Z" fill="#4a5a68" ${O(5)}/>
      <path d="M-500,-4L-700,-200Q-640,-60 -660,10Q-640,90 -720,190Z" fill="#3a4a58" ${O(5)}/>
      ${[0, 1, 2, 3, 4].map((k) => `<path d="M${250 - k * 26},-56q-10,40 0,80" stroke="#2a323a" stroke-width="4" fill="none" opacity=".7"/>`).join("")}
      <circle cx="400" cy="-40" r="12" fill="#0a0c10"/><circle cx="404" cy="-44" r="3" fill="#fff" opacity=".6"/>
      <path d="M380,24Q440,30 500,6" stroke="#2a323a" stroke-width="5" fill="none"/><path d="M-300,-60Q0,-120 300,-80" stroke="#fff" stroke-width="8" opacity=".12" fill="none"/></g>`;
  function sharkSea(L, o = {}) {
    const id = o.id || "ss", SL = o.sl ?? 900;
    put(L.sky, `<rect x="-1400" y="-900" width="3900" height="${SL + 900}" fill="url(#skSky)"/><circle cx="1500" cy="${SL - 120}" r="110" fill="#fff0c8" opacity=".9"/><circle cx="1500" cy="${SL - 120}" r="260" fill="#ffe0a0" opacity=".25"/>${[[-600, 260, 1.4], [300, 120, 1], [1100, 340, 1.2], [1900, 200, 0.9]].map(([x, y, k]) => `<path d="M${x - 260 * k},${y}q60,-60 140,-30q50,-70 140,-30q80,-40 120,30q60,10 40,40H${x - 260 * k}Z" fill="#f0a888" opacity=".55"/>`).join("")}`);
    put(L.far, `<path d="M-1400,${SL - 30}Q-600,${SL - 120} 0,${SL - 60}Q500,${SL - 110} 900,${SL - 50}L900,${SL}H-1400Z" fill="#3a3048" opacity=".7"/>`);
    // the deep below the line: blue to black, sun shafts, drifting motes
    let mid = `<rect x="-1400" y="${SL}" width="3900" height="2600" fill="url(#skDeep)"/>
      ${[[-300, 0.9], [200, 1.3], [700, 1.0], [1150, 1.4], [1600, 0.8]].map(([x, w]) => `<path class="sksh" d="M${x - 40 * w},${SL}L${x + 40 * w},${SL}L${x + 340 * w},${SL + 1500}L${x - 120 * w},${SL + 1500}Z" fill="url(#skShaft)" opacity=".6"/>`).join("")}
      ${Array.from({ length: 40 }, (_, k) => `<circle cx="${-1200 + ((k * 211) % 3400)}" cy="${SL + 80 + ((k * 137) % 1400)}" r="${1.5 + (k % 3)}" fill="#cfefff" opacity=".35"/>`).join("")}`;
    put(L.mid, mid);
    const [sx, sy, ss, sr] = o.shark || [400, SL + 900, 1, -12];
    put(L.set, `<g id="${id}-sw"><g transform="translate(${sx},${sy}) rotate(${sr}) scale(${ss},${Math.abs(ss)})"><g opacity="${o.sharkOp ?? 0.92}">${sharkG(`${id}-shark`)}</g></g></g>`);
    // the surface: the swell above the line, the underside of the surface below it, the board, the fin and its wake
    const [fx, fs] = o.fin || [1400, 1];
    put(L.glow, `<rect x="-1400" y="${SL}" width="3900" height="2600" fill="#0a3a5a" opacity=".28"/>
      <path d="M-1400,${SL}Q-1100,${SL - 26} -800,${SL}T-200,${SL}T400,${SL}T1000,${SL}T1600,${SL}T2200,${SL}T2800,${SL}V${SL - 60}H-1400Z" fill="url(#skSwell)" opacity=".9"/>
      <path d="M-1400,${SL}Q-1100,${SL - 26} -800,${SL}T-200,${SL}T400,${SL}T1000,${SL}T1600,${SL}T2200,${SL}T2800,${SL}" stroke="#e8fbff" stroke-width="7" fill="none" opacity=".85"/>
      <path d="M-1400,${SL + 14}Q-1100,${SL + 34} -800,${SL + 14}T-200,${SL + 14}T400,${SL + 14}T1000,${SL + 14}T1600,${SL + 14}T2200,${SL + 14}T2800,${SL + 14}" stroke="#bfefff" stroke-width="5" fill="none" opacity=".5"/>
      ${Array.from({ length: 12 }, (_, k) => `<path d="M${-1300 + k * 330},${SL - 30 - (k % 3) * 12}q40,-10 80,0" stroke="#fff" stroke-width="3" opacity=".5" fill="none"/>`).join("")}${Array.from({ length: 10 }, (_, k) => `<path d="M${1440 - k * 10 + (k % 2) * 30},${SL - 54 + k * 5}h${60 - k * 3}" stroke="#ffe8b0" stroke-width="5" opacity=".8"/>`).join("")}
      <g id="${id}-finw"><g id="${id}-fin" transform="translate(${fx},${SL}) scale(${fs},${Math.abs(fs)})"><path d="M-160,4q80,-26 200,-6q60,10 120,0" stroke="#fff" stroke-width="7" fill="none" opacity=".8"/><path d="M-260,10q120,-10 240,0" stroke="#fff" stroke-width="4" fill="none" opacity=".5"/>
        <path d="M-40,6Q-10,-90 40,-170Q60,-110 90,6Z" fill="#3a4a58" ${O(5)}/><path d="M-10,0Q10,-70 38,-140" stroke="#8a9aa8" stroke-width="4" fill="none" opacity=".6"/></g></g>`);
    if (o.board) { const [bx, bs] = o.board;
      put(L.act, `<g transform="translate(${bx},${SL + 6}) scale(${bs})"><ellipse cx="0" cy="40" rx="300" ry="30" fill="#000" opacity=".25"/><path d="M-300,0Q-250,-26 0,-28Q260,-26 330,-4Q260,24 0,26Q-250,24 -300,0Z" fill="#f4f0e4" ${O(4)}/><path d="M-280,0H310" stroke="#e2382e" stroke-width="7"/><path d="M-240,6l-60,40" stroke="#2a2a2a" stroke-width="4" fill="none"/></g>`); }
  }
  Object.assign(Sets, { caveFlood, sharkSea });

  // ---------------- cast ----------------
  const { LINE, dk, hi } = Rig2;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const helmet = (c) => (x) => `<path d="M-64,-556C-70,-650 70,-650 64,-556Z" fill="${c}" ${ln(3)}/><path d="M-74,-556H74" stroke="${dk(c, 0.3)}" stroke-width="9" stroke-linecap="round"/>
    <path d="M-40,-626Q0,-646 40,-626" stroke="#fff" stroke-width="6" opacity=".35" fill="none"/><rect x="-22" y="-618" width="44" height="30" rx="8" fill="#2a2a30" ${ln(2.4)}/><circle cx="0" cy="-603" r="10" fill="#fffbe8"/>`;
  const wet = (c) => ({ kind: "shirt", c, sleeve: "short", neck: "crew", trim: dk(c, 0.2) });
  const cav = (skin, hc, shirt, girl) => ({ skin, iris: "#2a1a10", blush: 0.3, lash: girl, lip: girl ? "#c86a5a" : undefined,
    hair: { c: "#1a1410", s: "#000", sh: "#4a3a30", front: helmet(hc), back: girl ? (x) => `<path d="M30,-560Q70,-540 66,-470Q60,-440 70,-420Q40,-440 40,-480Z" fill="#1a1410" ${ln()}/>` : undefined },
    top: wet(shirt), print: `<path d="M-40,-420q40,30 80,0" stroke="#000" stroke-width="10" opacity=".12" fill="none"/>`, bottom: { kind: "shorts", c: "#3a3a40" }, feet: { kind: "sneaker", c: "#2a2a30" } });
  const surf = { skin: "#c88a5a", iris: "#2a1a10", lash: true, blush: 0.5, lip: "#c8584a",
    hair: { c: "#1a1410", s: "#000", sh: "#5a4a40", front: (x) => `<path d="M-50,-552C-58,-616 -14,-632 6,-630C36,-628 58,-606 52,-552Q46,-582 24,-592Q2,-600 -20,-590Q-40,-578 -50,-552Z" fill="#1a1410" ${ln()}/><path d="M-24,-600q-10,40 -40,60M10,-604q14,30 4,60" stroke="#000" stroke-width="5" fill="none" opacity=".4"/>`,
      back: (x) => `<path d="M20,-600Q80,-590 74,-500Q72,-460 60,-430Q40,-470 40,-520Z" fill="#1a1410" ${ln()}/>` },
    top: { kind: "shirt", c: "#e2582e", sleeve: "long", neck: "crew", trim: "#2a3a6a" }, print: `<path d="M-60,-440H60" stroke="#2a3a6a" stroke-width="12"/>`, bottom: { kind: "shorts", c: "#2a3a6a" }, feet: { kind: "sandal", c: "#2a3a6a" } };
  Object.assign(Rig.CAST, { cav1: { v2: cav("#c8946c", "#e8b020", "#4a6a8a", false) }, cav2: { v2: cav("#e8b890", "#e2582e", "#8a3a4a", true) }, cav3: { v2: cav("#a8784e", "#f4f0e4", "#2a4a3a", false) }, surf: { v2: surf } });
  const M = Rig.MODES;
  M.wade = (u) => { const b = Math.sin(u * 5.3), j = Math.sin(u * 31) * 1.2; return { ...M.idle(u, {}), uaF: -60 + 6 * b + j, faF: -70, uaB: -50 - 6 * b, faB: -60, torso: 4 + 2 * b, head: -6 + 2 * Math.sin(u * 3.1), bodyY: 6 * b }; };
  M.diveReady = (u) => { const b = Math.sin(u * 7); return { ...M.idle(u, {}), uaF: -170, faF: -10, uaB: -160, faB: -10, torso: 22 + 3 * b, head: 18, thF: -30, shF: 40, thB: 10, shB: 30, bodyY: 30 }; };
  M.grabArm = (u) => { const j = Math.sin(u * 23) * 2; return { ...M.idle(u, {}), uaF: -96 + j, faF: -6, uaB: -30, faB: -80, torso: -10, head: -4 + j, bodyY: 4 }; };
  M.boardSit = (u) => { const b = Math.sin(u * 2.2), j = Math.sin(u * 29) * 1.5; return { ...M.idle(u, {}), thF: -84, shF: 70, thB: -80, shB: 76, torso: -4 + 2 * b + j * 0.4, head: 6 + j, uaF: -30 + j, faF: -50, uaB: 20, faB: -30, bodyY: 150 + 4 * b }; };
  M.cower = (u) => { const j = Math.sin(u * 37) * 2; return { ...M.boardSit(u), uaF: -120 + j, faF: -120, uaB: -110 - j, faB: -110, torso: 10 + j * 0.5, head: 14 + j }; };
})();
