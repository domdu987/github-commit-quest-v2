// "ตึกโยก" sets, part 2 — room 2714 (มิว's condo), seen from the entrance toward the window wall, plus its close-ups.
// Load after quake.js (uses Qk.city). Same layer contract as pop2.js. Seeded RNG only.
//   Sets.qkRoom(L, o)    the room front on: back wall base GB = 1380, ceiling 300, floor converging to (1050, 860).
//                        Left to right: fridge (x -1250…-960), kitchen counter with the portable gas stove and its canister (#id-can),
//                        the shrine cabinet (x -300…160: Buddha, two candles #id-candles, a drawer #id-drawer), the wall clock (#id-cH /
//                        #id-cM hands around "270 600"), the floor-to-ceiling window x 380…1720, y 330…1360 (panes #id-pane0…3,
//                        cracks #id-crack, shards #id-shards), curtains, the bookshelf (#id-shelf: topple with rotation around "2160 1380"),
//                        the aquarium (#id-aqw water surface, #id-fish). The dining table in the middle (front legs at y 1640,
//                        top 1318…1392, x 690…1410; all of it in #id-tbl, Qk.tableFront redraws its near parts over people under it),
//                        two chairs, the glass of water (#id-cup), the pendant lamp (#id-lamp: swing it
//                        around "1050 300"; its light #id-lampGlow in glow).
//                        o.lampDown: the lamp already fallen onto the table · o.after: the aftermath (broken panes, shards on the floor, shelf down, books, the lamp on the table,
//                        the canister on the floor hissing (#id-gas shimmer), the clock stopped crooked) · o.dark: the lamp is off
//                        o.bag: the delivery bag on the table · o.frame "door": the corridor wall with 2714's door frame around the
//                        doorway (x 700…1400, y 330…1700) and the hooks inside the door (#id-hooks: school bag, the red emergency bag
//                        with a torch) · o.under: the table drawn huge in glow as a foreground frame for under-the-table shots
//   Sets.qkFridge(L, o)  the fridge door close: magnets, a child's drawing (#id-draw falls), a photo strip, the note's spot (#id-note)
//   Sets.qkCup(L, o)     insert on the tabletop: the glass of water (#id-rings ripple, #id-surf), มิว's phone showing the time
//                        (#id-t19 / #id-t20), crayons; the room soft behind
//   Sets.qkPlan(L, o)    แผนผังห้อง that แม่ drew on graph paper (top-down): walls, window (blue), door, table, chairs, shelf, tank,
//                        fridge, stove, the lamp; danger zones #id-z0…#id-z3 (glass, shelf, tank, gas; red, hatched) with labels #id-l0…#id-l3, the safe zone
//                        #id-safe (green) with two dots #id-you #id-mew and a tick #id-ok
(function () {
  const { mk, f1, put } = Pop2;
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const OUT3 = `stroke="${INK}" stroke-width="3" stroke-linejoin="round"`;
  const Qk = (window.Qk = window.Qk || {});
  const GB = 1380, CEIL = 300, VPX = 1050, VPY = 860;

  Sets.DEFS += `
    <linearGradient id="qkRoomWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4ede2"/><stop offset="1" stop-color="#e6dbca"/></linearGradient>
    <linearGradient id="qkFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d6ae80"/><stop offset="1" stop-color="#a87a4e"/></linearGradient>
    <linearGradient id="qkTable" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a5a36"/><stop offset=".5" stop-color="#a8764a"/><stop offset="1" stop-color="#7a4e2e"/></linearGradient>
    <linearGradient id="qkTableTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8875a"/><stop offset="1" stop-color="#a07048"/></linearGradient>
    <linearGradient id="qkPane" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".28"/><stop offset=".4" stop-color="#d8f0fa" stop-opacity=".06"/><stop offset=".55" stop-color="#ffffff" stop-opacity=".18"/><stop offset="1" stop-color="#d8f0fa" stop-opacity=".04"/></linearGradient>
    <linearGradient id="qkCurtain" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfc8bc"/><stop offset=".25" stop-color="#e8e2d8"/><stop offset=".5" stop-color="#c8c0b2"/><stop offset=".75" stop-color="#e4ddd2"/><stop offset="1" stop-color="#c6beb0"/></linearGradient>
    <linearGradient id="qkFridgeG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8eaea"/><stop offset=".6" stop-color="#f8f8f6"/><stop offset="1" stop-color="#d4d8da"/></linearGradient>
    <linearGradient id="qkLightShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6dc" stop-opacity=".5"/><stop offset="1" stop-color="#fff6dc" stop-opacity="0"/></linearGradient>
    <radialGradient id="qkLampG" cx=".5" cy=".1" r=".9"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".75"/><stop offset=".5" stop-color="#ffd88a" stop-opacity=".22"/><stop offset="1" stop-color="#ffd88a" stop-opacity="0"/></radialGradient>
    <linearGradient id="qkAq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fe2ee" stop-opacity=".85"/><stop offset="1" stop-color="#3a9cb8" stop-opacity=".9"/></linearGradient>
    <pattern id="qkGrid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40,0H0V40" fill="none" stroke="#9cc4dc" stroke-width="1.6" opacity=".7"/></pattern>
    <pattern id="qkHatch" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="22" height="22" fill="#e8443a" opacity=".22"/><path d="M0,0V22" stroke="#e8443a" stroke-width="7" opacity=".55"/></pattern>`;

  // floor boards converging on the vanishing point
  const floor = (x0, x1, y0, y1) => {
    let s = `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" fill="url(#qkFloor)"/>`;
    for (let x = x0; x <= x1; x += 140) { const k = (y1 - VPY) / (y0 - VPY); s += `<path d="M${x},${y0}L${f1(VPX + (x - VPX) * k)},${y1}" stroke="#8a5e38" stroke-width="3" opacity=".45"/>`; }
    for (let y = y0 + 40, g = 40; y < y1; g *= 1.18, y += g) s += `<path d="M${x0},${f1(y)}H${x1}" stroke="#8a5e38" stroke-width="2" opacity=".25"/>`;
    return s;
  };
  // the dining table front on (front legs stand at y = G), returns markup; o.top false leaves the top off
  Qk.table = (cx, G, w = 720, o = {}) => {
    const x0 = cx - w / 2, x1 = cx + w / 2, H = 282, top = G - H;
    let s = `<path d="M${x0 + 80},${top}V${G - 80}M${x1 - 80},${top}V${G - 80}" stroke="#6a4428" stroke-width="30"/>`;
    s += `<rect x="${x0 + 30}" y="${top + 34}" width="36" height="${H - 34}" fill="url(#qkTable)" ${OUT3}/><rect x="${x1 - 66}" y="${top + 34}" width="36" height="${H - 34}" fill="url(#qkTable)" ${OUT3}/>`;
    s += `<rect x="${x0 + 60}" y="${top + 34}" width="${w - 120}" height="22" fill="#7a4e2e" opacity=".8"/>`;
    if (o.top !== false) s += `<path d="M${x0 + 20},${top - 40}H${x1 - 20}L${x1},${top}H${x0}Z" fill="url(#qkTableTop)" ${OUT3}/><rect x="${x0}" y="${top}" width="${w}" height="34" fill="url(#qkTable)" ${OUT3}/>
      <path d="M${x0 + 60},${top - 26}H${x0 + 300}" stroke="#d8a878" stroke-width="5" opacity=".6" stroke-linecap="round"/>`;
    return s;
  };
  // the parts of the table nearer than whoever is under it (front legs, apron, the top): redraw them in glow over people under the table
  Qk.tableFront = (cx, G, w = 720) => {
    const x0 = cx - w / 2, x1 = cx + w / 2, H = 282, top = G - H;
    return `<rect x="${x0 + 30}" y="${top + 34}" width="36" height="${H - 34}" fill="url(#qkTable)" ${OUT3}/><rect x="${x1 - 66}" y="${top + 34}" width="36" height="${H - 34}" fill="url(#qkTable)" ${OUT3}/>
      <path d="M${x0 + 20},${top - 40}H${x1 - 20}L${x1},${top}H${x0}Z" fill="url(#qkTableTop)" ${OUT3}/><rect x="${x0}" y="${top}" width="${w}" height="34" fill="url(#qkTable)" ${OUT3}/>
      <path d="M${x0 + 60},${top - 26}H${x0 + 300}" stroke="#d8a878" stroke-width="5" opacity=".6" stroke-linecap="round"/>`;
  };
  const chair = (x, G, flip) => `<g transform="translate(${x},${G}) scale(${flip ? -1 : 1},1)"><path d="M-60,-170H60L66,-150H-66Z" fill="#a8764a" ${OUT3}/><path d="M-56,-150V0M56,-150V0" stroke="#7a4e2e" stroke-width="16"/>
    <path d="M-60,-170L-70,-430" stroke="#7a4e2e" stroke-width="18"/><rect x="-86" y="-440" width="44" height="200" rx="8" fill="#a8764a" ${OUT3}/></g>`;

  function qkRoom(L, o = {}) {
    const id = o.id || "rm", r = mk(o.seed || 31), A = !!o.after;
    Qk.city(L, { hz: 860, seed: 17, id: `${id}c`, below: true, sunX: 1350, x0: 200, x1: 1900 });
    let s = "";
    // the back wall with the window cut out (even-odd), its frame, mullions and panes
    s += `<path d="M-1600,-600H2900V${GB}H-1600Z M380,330V1360H1720V330Z" fill="url(#qkRoomWall)" fill-rule="evenodd"/>`;
    s += `<rect x="-1600" y="-600" width="4500" height="${CEIL + 600}" fill="#ece6dc"/><path d="M-1600,${CEIL}H2900" stroke="#d2c8b8" stroke-width="10"/>`;
    s += `<path d="M-1600,${GB - 24}H2900" stroke="#cfc3b0" stroke-width="20"/>`;
    // panes (each its own group so it can crack and burst)
    for (let k = 0; k < 4; k++) {
      const x = 380 + k * 335;
      s += `<g id="${id}-pane${k}">${A ? "" : `<rect x="${x}" y="330" width="335" height="1030" fill="url(#qkPane)"/><path d="M${x + 40},${430 + k * 30}L${x + 140},330M${x + 70},${600}L${x + 300},370" stroke="#fff" stroke-width="10" opacity=".22"/>`}</g>`;
    }
    if (A) for (let k = 0; k < 4; k++) { const x = 380 + k * 335; s += `<path d="M${x},330l60,90l-30,40l50,30L${x},${560 + k * 20}ZM${x + 335},1360l-80,-70l20,-50l-60,-30l120,-40Z" fill="#dff2fa" opacity=".5" ${OUT3}/>`; }
    s += [380, 715, 1050, 1385, 1720].map((x) => `<rect x="${x - 12}" y="320" width="24" height="1050" fill="#d8dcdc" ${OUT3}/>`).join("");
    s += `<rect x="370" y="316" width="1360" height="22" fill="#d8dcdc" ${OUT3}/><rect x="370" y="1352" width="1360" height="28" fill="#c8cccc" ${OUT3}/>`;
    // cracks across the panes (hidden; drawn on by the shot) and shards (hidden; fall when the glass bursts)
    let cr = "";
    for (let k = 0; k < 4; k++) {
      const cx = 380 + k * 335 + 120 + r() * 100, cy = 600 + r() * 400;
      for (let j = 0; j < 7; j++) { let d = `M${f1(cx)},${f1(cy)}`, x = cx, y = cy, a = (j / 7) * Math.PI * 2 + r() * 0.5; for (let q = 0; q < 4; q++) { x += Math.cos(a) * (40 + r() * 70); y += Math.sin(a) * (40 + r() * 70); a += (r() - 0.5) * 0.8; d += `L${f1(x)},${f1(y)}`; } cr += `<path d="${d}" stroke="#f4fbff" stroke-width="4" fill="none" opacity=".95"/><path d="${d}" stroke="#5a7a8a" stroke-width="1.5" fill="none" opacity=".6"/>`; }
      cr += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="30" fill="none" stroke="#f4fbff" stroke-width="3" opacity=".9"/>`;
    }
    s += `<g id="${id}-crack" opacity="0">${cr}</g>`;
    let sh = "";
    for (let k = 0; k < 46; k++) {
      const x = 400 + r() * 1300, y = 360 + r() * 980, w = 30 + r() * 70, h = 40 + r() * 90;
      sh += `<g class="qkShard" data-x="${f1(x)}" data-y="${f1(y)}"><path d="M${f1(x)},${f1(y)}l${f1(w)},${f1(h * 0.3)}l${f1(-w * 0.6)},${f1(h)}Z" fill="#e4f6fc" opacity=".75" stroke="#9cc4d4" stroke-width="2"/></g>`;
    }
    s += `<g id="${id}-shards" opacity="0">${sh}</g>`;
    // curtains
    s += `<path d="M250,300C290,700 260,1100 300,1380H460C420,1100 450,700 420,300Z" fill="url(#qkCurtain)" ${OUT3}/><path d="M1680,300C1650,700 1680,1100 1640,1380H1800C1840,1100 1810,700 1850,300Z" fill="url(#qkCurtain)" ${OUT3}/>
      <path d="M200,300H1900" stroke="#9a9a96" stroke-width="10" stroke-linecap="round"/>`;
    // daylight shafts on the floor from the window
    s += floor(-1600, 2900, GB, 2900);
    s += `<path d="M380,${GB}H1720L2100,2400H120Z" fill="url(#qkLightShaft)"/>`;
    // left: fridge, counter with the stove, shrine cabinet; clock and a photo on the wall
    s += `<rect x="-1250" y="720" width="290" height="${GB - 720}" rx="14" fill="url(#qkFridgeG)" ${OUT}/><path d="M-1250,980H-960" stroke="#b8bcbe" stroke-width="5"/><path d="M-990,780V940M-990,1020V1220" stroke="#9aa0a4" stroke-width="12" stroke-linecap="round"/>
      <rect x="-1200" y="800" width="130" height="150" fill="#fbf8ee" ${OUT3}/><path d="M-1186,836h90M-1186,866h80M-1186,896h96M-1186,926h60" stroke="#c8281e" stroke-width="5" opacity=".7"/><circle cx="-1135" cy="802" r="12" fill="#e8443a" ${OUT3}/>`;
    s += `<rect x="-940" y="1040" width="500" height="${GB - 1040}" fill="#e8e2d6" ${OUT3}/><rect x="-950" y="1024" width="520" height="24" fill="#5a5a58" ${OUT3}/>
      ${[-920, -760, -600].map((x) => `<rect x="${x}" y="1070" width="140" height="290" fill="#efe9de" ${OUT3}/><path d="M${x + 60},1100h20" stroke="#8a8a86" stroke-width="6" stroke-linecap="round"/>`).join("")}
      <rect x="-940" y="420" width="500" height="220" fill="#efe9de" ${OUT3}/><path d="M-690,420V640" stroke="${INK}" stroke-width="3"/>
      <g transform="translate(-560,1024)"><path d="M-40,0V-70Q-40,-120 0,-120Q40,-120 40,-70V0Z" fill="#c8ccce" ${OUT3}/><path d="M40,-80q30,0 30,30" stroke="${INK}" stroke-width="5" fill="none"/></g>`;
    // the portable gas stove and its canister (the canister falls in the aftermath)
    s += `<g id="${id}-stove" transform="translate(-820,1024)"><rect x="-90" y="-50" width="180" height="50" rx="8" fill="#2a2a2c" ${OUT3}/><circle cx="0" cy="-50" r="44" fill="none" stroke="#5a5a5a" stroke-width="8"/><circle cx="60" cy="-22" r="10" fill="#d8d8d8" ${OUT3}/></g>`;
    const canAt = A ? "translate(-690,1520) rotate(-70)" : "translate(-700,1024)";
    s += `<g id="${id}-can" transform="${canAt}"><rect x="-26" y="-130" width="52" height="130" rx="12" fill="#e8e8e2" ${OUT3}/><rect x="-26" y="-100" width="52" height="40" fill="#d8312a"/><path d="M-10,-130V-148H10V-130" fill="#9aa0a4" ${OUT3}/></g>`;
    // the shrine cabinet with the Buddha, candles, garland; a drawer for matches
    s += `<rect x="-300" y="1004" width="460" height="${GB - 1004}" fill="#7a4a2a" ${OUT}/><rect x="-310" y="990" width="480" height="24" fill="#8a5a36" ${OUT3}/>
      <g id="${id}-drawer"><rect x="-260" y="1050" width="380" height="110" fill="#8a5a36" ${OUT3}/><circle cx="-70" cy="1105" r="12" fill="#e8c46a" ${OUT3}/></g>
      <rect x="-260" y="1190" width="380" height="150" fill="#8a5a36" ${OUT3}/>
      <g transform="translate(-70,990)"><path d="M-70,0H70L54,-40H-54Z" fill="#c8a040" ${OUT3}/><path d="M-30,-40Q-34,-120 0,-150Q34,-120 30,-40Z" fill="#e8c04a" ${OUT3}/><circle cy="-170" r="28" fill="#e8c04a" ${OUT3}/><path d="M0,-198v-24" stroke="#e8c04a" stroke-width="8"/>
        <path d="M-14,-90q14,10 28,0" stroke="#9a7a20" stroke-width="3" fill="none"/></g>
      <g id="${id}-candles">${[-200, 60].map((x) => `<g transform="translate(${x},990)"><rect x="-16" y="-14" width="32" height="14" fill="#c8a040" ${OUT3}/><rect x="-9" y="-100" width="18" height="86" fill="#f4efe2" ${OUT3}/><path d="M0,-100v-10" stroke="${INK}" stroke-width="3"/></g>`).join("")}</g>
      <path d="M-160,992q20,30 40,0t40,0" stroke="#f2c230" stroke-width="10" fill="none"/><circle cx="-140" cy="996" r="8" fill="#e8443a"/>`;
    s += `<g transform="translate(-70,700)${A ? " rotate(9)" : ""}"><rect x="-90" y="-70" width="180" height="140" fill="#fbf8ee" ${OUT3}/><rect x="-74" y="-54" width="148" height="108" fill="#bcd8e6"/><circle cx="-24" cy="-6" r="20" fill="#e8b88e"/><circle cx="26" cy="4" r="14" fill="#e8b88e"/><path d="M-50,54q26,-40 52,0M8,54q18,-30 36,0" fill="#f6f6f2"/><path d="M-40,-24h32" stroke="#fff" stroke-width="8"/></g>`;
    const ca = A ? 4 : 0;
    s += `<g transform="rotate(${ca} 270 600)"><circle cx="270" cy="600" r="80" fill="#fbf8ee" ${OUT}/>${Array.from({ length: 12 }, (_, k) => { const a = (k / 12) * Math.PI * 2; return `<path d="M${f1(270 + Math.sin(a) * 64)},${f1(600 - Math.cos(a) * 64)}L${f1(270 + Math.sin(a) * 72)},${f1(600 - Math.cos(a) * 72)}" stroke="${INK}" stroke-width="${k % 3 ? 3 : 6}"/>`; }).join("")}
      <g id="${id}-cH"><path d="M270,600L${f1(270 + Math.sin(((1 + 20 / 60) / 12) * Math.PI * 2) * 38)},${f1(600 - Math.cos(((1 + 20 / 60) / 12) * Math.PI * 2) * 38)}" stroke="${INK}" stroke-width="8" stroke-linecap="round"/></g>
      <g id="${id}-cM"><path d="M270,600V546" stroke="${INK}" stroke-width="5" stroke-linecap="round" transform="rotate(${(o.min ?? 18) * 6} 270 600)"/></g><circle cx="270" cy="600" r="7" fill="${INK}"/></g>`;
    // right: the bookshelf and the aquarium on its cabinet
    let shelf = `<rect x="1880" y="590" width="280" height="790" fill="#9a6a42" ${OUT}/>`;
    for (let k = 0; k < 4; k++) {
      const y = 600 + k * 194;
      shelf += `<rect x="1896" y="${y}" width="248" height="176" fill="#6a4428"/>`;
      for (let x = 1900; x < 2130;) { const w = 18 + r() * 18, h = 110 + r() * 60, c = ["#c8463a", "#3a6a9a", "#e8b83a", "#4a8a5a", "#8a4a8a", "#e8e2d6"][Math.floor(r() * 6)]; shelf += `<rect x="${f1(x)}" y="${f1(y + 176 - h)}" width="${f1(w)}" height="${f1(h)}" fill="${c}" stroke="${INK}" stroke-width="2"/>`; x += w + 2; }
    }
    s += A ? `<g transform="rotate(84 2160 1380)">${shelf}</g>${Array.from({ length: 14 }, () => `<rect x="${f1(1900 + r() * 500)}" y="${f1(1400 + r() * 260)}" width="${f1(60 + r() * 30)}" height="${f1(18 + r() * 10)}" transform="rotate(${f1(r() * 60 - 30)} 2100 1500)" fill="${["#c8463a", "#3a6a9a", "#e8b83a", "#4a8a5a"][Math.floor(r() * 4)]}" stroke="${INK}" stroke-width="2"/>`).join("")}`
      : `<g id="${id}-shelf">${shelf}</g>`;
    s += `<rect x="2240" y="1150" width="380" height="${GB - 1150}" fill="#3a3a3c" ${OUT}/>
      <g id="${id}-tank"><rect x="2260" y="960" width="340" height="190" rx="6" fill="#d8f2f8" opacity=".35" ${OUT3}/>
        <defs><clipPath id="${id}-aqc"><rect x="2264" y="964" width="332" height="182"/></clipPath></defs>
        <g clip-path="url(#${id}-aqc)"><g id="${id}-aqw"><path d="M2200,${A ? 1040 : 990}Q2330,${A ? 1030 : 980} 2430,${A ? 1040 : 990}T2660,${A ? 1040 : 990}V1160H2200Z" fill="url(#qkAq)"/></g>
          <path d="M2300,1150q10,-60 -6,-110M2330,1150q-8,-50 10,-90M2560,1150q8,-40 -6,-80" stroke="#3e8a4a" stroke-width="8" fill="none"/>
          <g id="${id}-fish"><path d="M2400,1060q30,-18 56,0q-26,18 -56,0zM2456,1060l18,-12v24z" fill="#f47b20" ${OUT3}/><path d="M2500,1100q24,-14 44,0q-20,14 -44,0zM2544,1100l14,-10v20z" fill="#e8c43a" ${OUT3}/></g></g>
        ${A ? `<path d="M2290,970l40,60l-20,40l50,60" stroke="#fff" stroke-width="4" fill="none"/>` : ""}</g>
      ${A ? `<ellipse cx="2420" cy="1520" rx="300" ry="50" fill="#9adcf0" opacity=".45"/>` : ""}`;
    // the table, chairs, the glass of water, the delivery bag
    if (!o.under) s += chair(560, 1660, false) + chair(1540, 1660, true);
    s += `<g id="${id}-tbl"${o.under ? ' display="none"' : ""}>` + Qk.table(1050, 1640);
    s += `<g id="${id}-cup" transform="translate(900,1318)"><path d="M-26,-90L-20,0H20L26,-90Z" fill="#e8f6fa" opacity=".55" ${OUT3}/><path d="M-24,-56L-20,0H20L24,-56Z" fill="#9adcf0" opacity=".7"/><path d="M-16,-80V-10" stroke="#fff" stroke-width="5" opacity=".6"/></g>`;
    if (o.bag) s += `<g transform="translate(1210,1318)"><rect x="-80" y="-120" width="160" height="120" rx="10" fill="#2fa45a" ${OUT3}/><circle cx="0" cy="-60" r="28" fill="#fff4dc" ${OUT3}/><path d="M-16,-62h32q-2,15 -16,17q-14,-2 -16,-17z" fill="#e2a92e"/></g>`;
    if (A || o.lampDown) s += `<g transform="translate(1120,1300) rotate(-14)"><path d="M-110,0Q-100,-90 0,-96Q100,-90 110,0Z" fill="#e8dcc6" ${OUT}/><path d="M0,-96V-200" stroke="${INK}" stroke-width="4"/></g>`;
    s += `</g>`;
    put(L.set, s);
    // the pendant lamp (swings around 1050 300) and its light
    if (!A && !o.under && !o.lampDown) {
      put(L.set, `<g id="${id}-lamp"><path d="M1050,300V940" stroke="#2a2a2a" stroke-width="5"/><rect x="1036" y="296" width="28" height="12" fill="#2a2a2a"/>
        <path d="M940,1010Q944,940 1050,934Q1156,940 1160,1010Z" fill="#e8dcc6" ${OUT}/><path d="M960,1004Q1000,980 1040,982" stroke="#fff" stroke-width="6" opacity=".5" fill="none"/>
        <ellipse cx="1050" cy="1012" rx="40" ry="12" fill="${o.dark ? "#cfc6b0" : "#fff8dc"}"/></g>`);
      if (!o.dark) put(L.glow, `<g id="${id}-lampGlow"><path d="M950,1010L780,1380H1320L1150,1010Z" fill="url(#qkLampG)" opacity=".55"/><ellipse cx="1050" cy="1016" rx="90" ry="40" fill="#fff6d0" opacity=".5"/></g>`);
    }
    // gas shimmer over the fallen canister (the aftermath)
    if (A) put(L.glow, `<g id="${id}-gas" opacity="0">${[0, 1, 2, 3, 4].map((k) => `<path class="qkGas" d="M${-690 + k * 26},1470q-30,-60 0,-120t0,-120t0,-120" stroke="#cfe8d0" stroke-width="${18 - k * 2}" fill="none" opacity=".22" stroke-linecap="round"/>`).join("")}</g>`);
    // the corridor wall with the door frame around the doorway (we look in from outside 2714)
    if (o.frame === "door") {
      put(L.glow, `<path d="M-1600,-600H2900V2900H-1600Z M700,330V1700H1400V330Z" fill="url(#qkCorrWall)" fill-rule="evenodd"/>
        <path d="M670,300H1430V1700H1400V330H700V1700H670Z" fill="#7a5236" ${OUT}/><rect x="1470" y="700" width="140" height="70" rx="8" fill="#3a2a1c" ${OUT3}/><text x="1540" y="750" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="44" fill="#e8c46a">2714</text>
        <path d="M-1600,1700H2900V2900H-1600Z" fill="url(#qkCarpet)"/><path d="M700,330L560,250V1780L700,1700Z" fill="url(#qkDoorWood)" ${OUT3}/><circle cx="600" cy="1060" r="14" fill="#d8c070" ${OUT3}/>`);
      put(L.glow, `<g id="${id}-hooks" transform="translate(1310,780)"><circle r="8" fill="#9aa0a4"/><circle cx="-110" r="8" fill="#9aa0a4"/>
        <g transform="translate(-110,0)"><path d="M-50,10Q-60,120 -54,220H54Q60,120 50,10Q0,-6 -50,10Z" fill="#c8312a" ${OUT3}/><rect x="-34" y="60" width="68" height="60" rx="6" fill="#fff" opacity=".9"/><path d="M-12,90h24M0,78v24" stroke="#c8312a" stroke-width="8"/>
          <g transform="translate(40,140) rotate(-20)"><rect x="-10" y="-40" width="20" height="56" rx="5" fill="#2a2a2c" ${OUT3}/><rect x="-14" y="-52" width="28" height="16" rx="4" fill="#f2c230" ${OUT3}/></g></g>
        <g><path d="M-40,10Q-50,110 -44,200H44Q50,110 40,10Q0,-4 -40,10Z" fill="#8a6ac8" ${OUT3}/><rect x="-30" y="110" width="60" height="50" rx="6" fill="#a88ae0" ${OUT3}/></g></g>`);
    }
    // under the table: the table huge in the foreground (underside across the top, legs at the sides)
    if (o.under) {
      const u = o.under, cx = u.x ?? 1050, top = u.top ?? 1120, half = u.half ?? 560, G = u.G ?? 2050;
      put(L.glow, `<rect x="${cx - half - 240}" y="${top - 1400}" width="${2 * half + 480}" height="1400" fill="#5a3a22"/><rect x="${cx - half - 240}" y="${top - 70}" width="${2 * half + 480}" height="70" fill="url(#qkTable)" ${OUT}/>
        <path d="M${cx - half - 240},${top - 6}H${cx + half + 240}" stroke="#3a2414" stroke-width="10"/><rect x="${cx - half + 40}" y="${top}" width="${2 * half - 80}" height="40" fill="#6a4428" opacity=".8"/>
        <rect x="${cx - half - 110}" y="${top}" width="110" height="${G - top}" fill="url(#qkTable)" ${OUT}/><rect x="${cx + half}" y="${top}" width="110" height="${G - top}" fill="url(#qkTable)" ${OUT}/>
        <path d="M${cx - half - 80},${top + 40}V${G - 20}M${cx + half + 30},${top + 40}V${G - 20}" stroke="#d8a878" stroke-width="8" opacity=".4"/>`);
    }
  }

  // ---------------- the fridge door, close ----------------
  function qkFridge(L, o = {}) {
    const id = o.id || "fd";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#e6e8e8"/>`);
    let s = `<rect x="-400" y="-400" width="1880" height="2800" fill="url(#qkFridgeG)"/><path d="M-400,1500H1480" stroke="#c8ccce" stroke-width="10"/><path d="M960,300V1300" stroke="#b8bec2" stroke-width="40" stroke-linecap="round"/><path d="M948,320V1280" stroke="#fff" stroke-width="8" opacity=".7" stroke-linecap="round"/>
      <path d="M-400,-200L1480,600V700L-400,-100Z" fill="#fff" opacity=".18"/>`;
    // a child's drawing: แม่ in a nurse's cap holding มิว's hand under a sun
    s += `<g id="${id}-draw"><g transform="translate(250,1560) rotate(-6)"><rect x="-200" y="-160" width="400" height="300" fill="#fbf8ee" ${OUT3}/>
      <circle cx="140" cy="-110" r="30" fill="#f6c935"/><path d="M140,-160v-10M190,-110h10M176,-146l8,-8" stroke="#f6c935" stroke-width="5"/>
      <circle cx="-60" cy="-50" r="26" fill="none" stroke="#e8682a" stroke-width="5"/><path d="M-80,-78h40l-6,-12h-28z" fill="#fff" stroke="#3a6ad8" stroke-width="4"/><path d="M-60,-24V60M-60,0L-20,20M-60,0L-96,24M-60,60L-80,110M-60,60L-40,110" stroke="#3a6ad8" stroke-width="6" fill="none"/>
      <circle cx="30" cy="0" r="20" fill="none" stroke="#e8682a" stroke-width="5"/><path d="M30,20V80M30,40L-20,22M30,40L64,60M30,80L14,120M30,80L46,120" stroke="#d8312a" stroke-width="6" fill="none"/>
      <text x="0" y="120" text-anchor="middle" font-family="Mali" font-weight="700" font-size="30" fill="#8a4ac8">แม่กับมิว</text></g>
      <circle cx="240" cy="1406" r="26" fill="#e8443a" ${OUT3}/></g>`;
    // magnets and a photo strip
    s += `<g transform="translate(830,520) rotate(4)"><rect x="-60" y="-200" width="120" height="400" fill="#fff" ${OUT3}/>${[0, 1, 2].map((k) => `<rect x="-48" y="${-186 + k * 128}" width="96" height="112" fill="${["#f2c8a8", "#c8e0f0", "#f6e2a0"][k]}"/><circle cx="-10" cy="${-136 + k * 128}" r="20" fill="#e8b88e"/><circle cx="16" cy="${-126 + k * 128}" r="14" fill="#c99068"/>`).join("")}</g>
      <circle cx="830" cy="306" r="24" fill="#3aa0e8" ${OUT3}/>`;
    s += `<g id="${id}-note" transform="translate(370,820)"></g>`;
    put(L.set, s);
  }

  // ---------------- the glass of water, close ----------------
  function qkCup(L, o = {}) {
    const id = o.id || "cu";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#cfe6f0"/>`);
    // the room soft behind: the window's light, the lamp
    put(L.far, `<rect x="-600" y="-600" width="2300" height="1500" fill="#e8f4fa"/><rect x="-600" y="200" width="2300" height="700" fill="#bcdcee" opacity=".7"/>
      <circle cx="200" cy="300" r="90" fill="#fff" opacity=".6"/><circle cx="820" cy="180" r="140" fill="#fff6d0" opacity=".55"/><rect x="380" y="-600" width="30" height="1500" fill="#d8dcdc" opacity=".6"/>`);
    let s = `<path d="M-600,900H1700V2600H-600Z" fill="url(#qkTableTop)"/><path d="M-600,900H1700" stroke="#d8a878" stroke-width="10" opacity=".7"/>`;
    for (let k = 0; k < 9; k++) s += `<path d="M-600,${980 + k * 170}Q540,${960 + k * 170} 1700,${1000 + k * 170}" stroke="#8a5a36" stroke-width="4" fill="none" opacity=".3"/>`;
    // มิว's phone lying face up: the time flips 13:19 → 13:20
    s += `<g transform="translate(330,1400) rotate(-8)"><rect x="-130" y="-250" width="260" height="500" rx="34" fill="#1e2228" ${OUT}/><rect x="-112" y="-226" width="224" height="452" rx="22" fill="#3a5a8a"/>
      <text id="${id}-t19" x="0" y="-80" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="84" fill="#fff">13:19</text>
      <text id="${id}-t20" x="0" y="-80" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="84" fill="#fff" opacity="0">13:20</text>
      <text x="0" y="-30" text-anchor="middle" font-family="Kanit" font-weight="400" font-size="28" fill="#dfe8f4">วันศุกร์</text></g>`;
    s += `<g transform="translate(-40,1700) rotate(30)"><rect x="-90" y="-12" width="180" height="24" rx="6" fill="#e8443a" ${OUT3}/><path d="M90,-12l26,12l-26,12z" fill="#e8443a" ${OUT3}/></g>`;
    // the glass: water with rings (#id-rings) that pulse outward
    s += `<g transform="translate(780,1340)"><ellipse cx="0" cy="560" rx="230" ry="44" fill="#000" opacity=".12"/>
      <path d="M-210,-40L-170,540Q0,580 170,540L210,-40Z" fill="#eaf8fc" opacity=".45" ${OUT}/>
      <path d="M-196,150L-170,540Q0,580 170,540L196,150Z" fill="#9adcf0" opacity=".55"/>
      <g id="${id}-surf"><ellipse cx="0" cy="150" rx="196" ry="40" fill="#c8eef8" ${OUT3}/>
        <g id="${id}-rings">${[0, 1, 2].map((k) => `<ellipse class="qkRing" cx="0" cy="150" rx="${60 + k * 50}" ry="${12 + k * 10}" fill="none" stroke="#f4fcff" stroke-width="5" opacity=".9"/>`).join("")}</g></g>
      <path d="M-150,-10L-120,500" stroke="#fff" stroke-width="16" opacity=".55" stroke-linecap="round"/><ellipse cx="0" cy="-40" rx="210" ry="44" fill="none" ${OUT}/></g>`;
    put(L.set, s);
  }

  // ---------------- แม่'s plan of the room ----------------
  function qkPlan(L, o = {}) {
    const id = o.id || "pl";
    put(L.sky, `<rect x="-1000" y="-1000" width="3100" height="4000" fill="#8a6a4a"/>`);
    let s = `<g transform="rotate(-2 540 960)"><rect x="40" y="200" width="1000" height="1500" fill="#fbfaf4" ${OUT}/><rect x="40" y="200" width="1000" height="1500" fill="url(#qkGrid)"/>
      <text x="540" y="290" text-anchor="middle" font-family="Mali" font-weight="700" font-size="56" fill="#2a4a8a">ห้องเรา 2714</text>
      <path d="M120,380H960V1560H120Z" fill="none" stroke="#2a2a2a" stroke-width="12"/>
      <path d="M220,380H860" stroke="#3aa0e8" stroke-width="22"/><path d="M220,380H860" stroke="#e8f6fc" stroke-width="6"/>
      <text x="540" y="356" text-anchor="middle" font-family="Mali" font-weight="700" font-size="34" fill="#2a7ac8">หน้าต่างกระจก</text>
      <path d="M120,1400V1540" stroke="#fbfaf4" stroke-width="16"/><path d="M120,1400Q230,1410 240,1540" stroke="#2a2a2a" stroke-width="4" fill="none" stroke-dasharray="10 8"/><text x="180" y="1600" text-anchor="middle" font-family="Mali" font-weight="700" font-size="30" fill="#2a2a2a">ประตู</text>
      <rect x="380" y="760" width="320" height="200" rx="8" fill="#e8c898" stroke="#6a4428" stroke-width="6"/><text x="540" y="872" text-anchor="middle" font-family="Mali" font-weight="700" font-size="36" fill="#6a4428">โต๊ะ</text>
      ${[[370, 750], [690, 750], [370, 950], [690, 950]].map(([x, y]) => `<rect x="${x}" y="${y}" width="20" height="20" fill="#6a4428"/>`).join("")}
      <circle cx="540" cy="860" r="70" fill="none" stroke="#c8a040" stroke-width="5" stroke-dasharray="12 8"/>
      <rect x="820" y="560" width="120" height="300" fill="#c8a07a" stroke="#6a4428" stroke-width="5"/><text x="880" y="720" text-anchor="middle" font-family="Mali" font-weight="700" font-size="28" fill="#6a4428" transform="rotate(90 880 720)">ชั้นหนังสือ</text>
      <rect x="820" y="920" width="120" height="200" fill="#9adcf0" stroke="#2a7ac8" stroke-width="5"/><text x="880" y="1030" text-anchor="middle" font-family="Mali" font-weight="700" font-size="28" fill="#2a7ac8" transform="rotate(90 880 1030)">ตู้ปลา</text>
      <rect x="140" y="460" width="130" height="160" fill="#f4f4f2" stroke="#5a5a5a" stroke-width="5"/><text x="205" y="550" text-anchor="middle" font-family="Mali" font-weight="700" font-size="28" fill="#5a5a5a">ตู้เย็น</text>
      <rect x="140" y="660" width="130" height="300" fill="#e8e2d6" stroke="#5a5a5a" stroke-width="5"/><circle cx="205" cy="770" r="34" fill="none" stroke="#2a2a2a" stroke-width="5"/><text x="205" y="900" text-anchor="middle" font-family="Mali" font-weight="700" font-size="26" fill="#5a5a5a">เตาแก๊ส</text>`;
    // danger zones (red, hatched) and labels; the safe zone under the table (green)
    const Z = [[220, 390, 640, 160, "กระจกแตก"], [800, 540, 160, 340, "ของล้มทับ"], [800, 900, 160, 240, "ตู้ปลาแตก"], [130, 650, 160, 320, "แก๊ส"]];
    Z.forEach(([x, y, w, h, t], k) => {
      s += `<g id="${id}-z${k}" opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="url(#qkHatch)" stroke="#e8443a" stroke-width="6" stroke-dasharray="16 10"/></g>`;
      const lx = x + w / 2, ly = k === 0 ? y + h / 2 + 14 : y + h + 46;
      s += `<g id="${id}-l${k}" opacity="0"><rect x="${lx - 92}" y="${ly - 36}" width="184" height="50" rx="25" fill="#e8443a"/><text x="${lx}" y="${ly}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="#fff">${t}</text></g>`;
    });
    s += `<g id="${id}-safe" opacity="0"><rect x="388" y="768" width="304" height="184" rx="10" fill="#3fd07a" opacity=".35" stroke="#1e9a50" stroke-width="7"/></g>
      <g id="${id}-you" opacity="0"><circle cx="490" cy="880" r="30" fill="#2fa45a" stroke="#fff" stroke-width="6"/><text x="490" y="892" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="30" fill="#fff">คุณ</text></g>
      <g id="${id}-mew" opacity="0"><circle cx="600" cy="890" r="26" fill="#f2c230" stroke="#fff" stroke-width="6"/><text x="600" y="900" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="24" fill="#2a2a2a">มิว</text></g>
      <g id="${id}-ok" opacity="0"><circle cx="700" cy="1040" r="54" fill="#1e9a50" stroke="#fff" stroke-width="7"/><path d="M674,1040l20,20l34,-40" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <text x="540" y="1660" text-anchor="middle" font-family="Mali" font-weight="700" font-size="40" fill="#d8312a">ตึกโยก → มุดใต้โต๊ะ ห่างกระจก ♥ แม่</text></g>`;
    put(L.set, s);
  }

  Object.assign(Sets, { qkRoom, qkFridge, qkCup, qkPlan });
})();
