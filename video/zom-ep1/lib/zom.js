// Sets and props for "ชั้น 23": a Bangkok condo during an outbreak. A studio living room with the front door,
// the corridor through the door's peephole (with a front-facing face for the jump scare), the bathroom sink
// close-up of a bitten forearm, a bathtub being filled, the building's water system as a cross-section,
// the fire stairs (side landing and looking down the shaft) and the city at dusk. Same layer contract as sets.js.
(function () {
  const INK = "#2e2a26";
  const OUT = `stroke="${INK}" stroke-width="4" stroke-linejoin="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => v.toFixed(1);

  Sets.DEFS += `
    <linearGradient id="zWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8d1c6"/><stop offset="1" stop-color="#c4bcae"/></linearGradient>
    <linearGradient id="zTile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dfe7e4"/><stop offset="1" stop-color="#c9d4d0"/></linearGradient>
    <linearGradient id="zChrome" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#eef2f4"/><stop offset=".5" stop-color="#9aa6ad"/><stop offset="1" stop-color="#dfe5e8"/></linearGradient>
    <linearGradient id="zWater" x1="0" x2="1"><stop offset="0" stop-color="#cfe9f2" stop-opacity=".5"/><stop offset=".5" stop-color="#f4fbff" stop-opacity=".9"/><stop offset="1" stop-color="#cfe9f2" stop-opacity=".5"/></linearGradient>
    <linearGradient id="zTub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc3d6" stop-opacity=".75"/><stop offset="1" stop-color="#5f9fb8" stop-opacity=".85"/></linearGradient>
    <linearGradient id="zDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f52"/><stop offset=".55" stop-color="#b8566a"/><stop offset="1" stop-color="#f0a26a"/></linearGradient>
    <linearGradient id="zDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fc7e0"/><stop offset="1" stop-color="#e8eef0"/></linearGradient>
    <linearGradient id="zNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070d"/><stop offset="1" stop-color="#141a2a"/></linearGradient>
    <radialGradient id="zExit"><stop offset="0" stop-color="#4dff9a" stop-opacity=".55"/><stop offset=".5" stop-color="#1fbf6a" stop-opacity=".18"/><stop offset="1" stop-color="#1fbf6a" stop-opacity="0"/></radialGradient>
    <radialGradient id="zPhone"><stop offset="0" stop-color="#cfe6ff" stop-opacity=".7"/><stop offset=".5" stop-color="#9cc4ff" stop-opacity=".2"/><stop offset="1" stop-color="#9cc4ff" stop-opacity="0"/></radialGradient>
    <radialGradient id="zLens" cx=".5" cy=".5" r=".5"><stop offset=".78" stop-color="#000" stop-opacity="0"/><stop offset=".97" stop-color="#000" stop-opacity=".85"/><stop offset="1" stop-color="#000"/></radialGradient>
    <radialGradient id="zSkinF" cx=".45" cy=".4"><stop offset="0" stop-color="#c6d3bd"/><stop offset=".7" stop-color="#9fb197"/><stop offset="1" stop-color="#7c8d75"/></radialGradient>`;

  // ---------------- city skyline (window view): day / dusk / night, smoke, a hospital with its lights ----------------
  function city(r, time, y0, o = {}) {
    const night = time === "night", dusk = time === "dusk";
    let s = `<rect x="-900" y="-600" width="2900" height="${y0 + 1000}" fill="url(#${night ? "zNight" : dusk ? "zDusk" : "zDay"})"/>`;
    const col = night ? ["#0b0f19", "#111827", "#0d1320"] : dusk ? ["#3a2f45", "#45364f", "#2f2a3c"] : ["#9fb0bc", "#8a9cab", "#b2c0ca"];
    for (let layer = 0; layer < 2; layer++) for (let x = -800; x < 1900; x += 70 + r() * 80) {
      const w = 60 + r() * 90, h = (layer ? 200 : 380) + r() * (layer ? 260 : 520), top = y0 - h;
      s += `<rect x="${f1(x)}" y="${f1(top)}" width="${f1(w)}" height="${h + 600}" fill="${col[layer + (r() > 0.6 ? 1 : 0)]}"/>`;
      if (night || dusk) for (let k = 0; k < 10; k++) if (r() > 0.55) s += `<rect x="${f1(x + 8 + r() * (w - 20))}" y="${f1(top + 14 + r() * (h - 30))}" width="7" height="9" fill="${r() > 0.5 ? "#ffd58a" : "#bcd6ff"}" opacity="${f1(0.4 + r() * 0.5)}"/>`;
    }
    if (o.smoke) s += [[180, 0.9], [760, 1.2], [1180, 0.8]].map(([x, k]) => `<path class="smoke" d="M${x},${y0 - 300}c-60,-120 80,-220 0,-360c-60,-110 70,-200 10,-330" stroke="${night ? "#3b3f4a" : "#5a5560"}" stroke-width="${70 * k}" fill="none" stroke-linecap="round" opacity=".55"/>`).join("");
    if (o.hospital) {
      const hx = o.hospital;
      s += `<g transform="translate(${hx},${y0 - 470}) scale(1.25)"><rect x="-120" y="0" width="240" height="900" fill="${night ? "#1b2333" : "#5a5f78"}" ${OUT}/>
        ${Array.from({ length: 24 }, (_, k) => `<rect x="${-100 + (k % 6) * 36}" y="${60 + Math.floor(k / 6) * 60}" width="22" height="30" fill="#ffeab0" opacity="${0.4 + (k % 3) * 0.2}"/>`).join("")}
        <rect x="-44" y="-96" width="88" height="88" rx="10" fill="#f4f4f0" ${OUT}/><path d="M0,-82V-22M-30,-52H30" stroke="#d8322a" stroke-width="20"/>
        <circle class="beacon" cx="-150" cy="320" r="90" fill="#ff3b30" opacity=".35"/><circle class="beacon2" cx="160" cy="300" r="90" fill="#2f7bff" opacity=".35"/></g>`;
    }
    return s;
  }

  // ---------------- the studio: front door (left), desk, sofa, big window on the city (right) ----------------
  function condo(L, o = {}) {
    const id = o.id || "cd", r = mk(o.seed || 23), G = 1500, t = o.time || "day", night = t === "night";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#1a1d22"/>`);
    put(L.far, `<svg x="200" y="-100" width="1300" height="1500" viewBox="200 -100 1300 1500" overflow="hidden">${city(r, t, 1150, { smoke: o.smoke, hospital: o.hospital })}</svg>`);
    let s = `<path d="M-900,-600H2000V${G}H-900Z M600,300H1100V1160H600Z" fill="url(#zWall)" fill-rule="evenodd"/>`;
    s += `<rect x="586" y="286" width="528" height="888" fill="none" stroke="#e9e4da" stroke-width="28"/><path d="M850,300V1160M600,730H1100" stroke="#e9e4da" stroke-width="16"/>
      <path d="M560,280h580v30h-580z" fill="#b9b2a6"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${590 + k * 8},300v850" stroke="#efe9dc" stroke-width="5" opacity=".5"/>`).join("")}`;
    s += `<rect x="-900" y="${G - 24}" width="2900" height="24" fill="#9b9183"/><rect x="-900" y="${G}" width="2900" height="1200" fill="#b98f62"/>${Array.from({ length: 22 }, (_, k) => `<path d="M${-900 + k * 140},${G}V2700" stroke="#a37c52" stroke-width="4"/>`).join("")}`;
    // front door with peephole, chain and a little shoe rack
    s += `<g id="${id}-doorf"><rect x="40" y="740" width="260" height="${G - 740}" fill="#e3ddd2" ${OUT}/><g id="${id}-door"><rect x="56" y="756" width="228" height="${G - 756}" fill="#7a5a3e" ${OUT}/>
      <rect x="80" y="790" width="180" height="300" rx="6" fill="none" stroke="#5f442d" stroke-width="6"/><rect x="80" y="1130" width="180" height="300" rx="6" fill="none" stroke="#5f442d" stroke-width="6"/>
      <circle cx="170" cy="980" r="9" fill="#2a2420" stroke="#c9b48a" stroke-width="4"/><rect x="246" y="1120" width="22" height="60" rx="6" fill="url(#zChrome)" ${OUT}/>
      <path d="M262,1060q-30,20 -4,44q-26,20 2,44" stroke="#c9ccd0" stroke-width="5" fill="none"/></g></g>`;
    s += `<rect x="20" y="${G - 70}" width="300" height="20" fill="#5f442d"/><path d="M40,${G - 50}h70l10,-24h-80z M140,${G - 50}h70l10,-24h-80z" fill="#e8e2d4" ${OUT}/>`;
    // desk + laptop + lamp
    s += `<g transform="translate(390,${G})"><rect x="-80" y="-300" width="300" height="24" fill="#d9cdb8" ${OUT}/><path d="M-66,-276V0M206,-276V0" stroke="#8a7a62" stroke-width="12"/>
      <path d="M-10,-302l10,-120h130l10,120z" fill="#3d4148" ${OUT}/><rect x="6" y="-412" width="118" height="96" fill="${night ? "#9cc4ff" : "#c9e3ff"}"/><path d="M150,-300l40,-150l-30,-10" stroke="#3d3833" stroke-width="7" fill="none"/><path d="M140,-470h60l-14,-30h-32z" fill="#f2c55c" ${OUT}/>
      <rect x="-60" y="-340" width="40" height="38" rx="6" fill="#e07a3f" ${OUT}/></g>`;
    // sofa
    s += `<g transform="translate(780,${G})"><rect x="-260" y="-300" width="520" height="150" rx="40" fill="#5b6f7c" ${OUT}/><rect x="-280" y="-190" width="560" height="150" rx="30" fill="#6c8190" ${OUT}/>
      <rect x="-300" y="-240" width="70" height="200" rx="30" fill="#5b6f7c" ${OUT}/><rect x="230" y="-240" width="70" height="200" rx="30" fill="#5b6f7c" ${OUT}/>
      <rect x="-150" y="-260" width="110" height="70" rx="20" fill="#e2c46a" ${OUT}/><path d="M-250,-40v30M250,-40v30" stroke="#3a3f45" stroke-width="12"/></g>`;
    // ceiling lamp
    s += `<path d="M640,-600V120" stroke="#3a3f45" stroke-width="4"/><path d="M600,120h80l26,60h-132z" fill="#3a3f45"/>`;
    put(L.set, s);
    if (!night) put(L.glow, `<circle cx="640" cy="200" r="380" fill="url(#lantern)" opacity=".35"/>`);
  }

  // ---------------- the corridor through the peephole: fisheye lens over a long hall ----------------
  function peephole(L, o = {}) {
    const id = o.id || "ph", r = mk(o.seed || 31), vx = 540, vy = 880;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#1c1b19"/>`);
    let s = `<path d="M-400,-200L${vx - 70},${vy - 90}H${vx + 70}L1480,-200Z" fill="#d9d3c4"/>`;
    s += `<path d="M-400,2200L${vx - 70},${vy + 90}H${vx + 70}L1480,2200Z" fill="#6b3a34"/>`;
    s += `<path d="M-400,-200L${vx - 70},${vy - 90}V${vy + 90}L-400,2200Z" fill="#cbc3b2"/><path d="M1480,-200L${vx + 70},${vy - 90}V${vy + 90}L1480,2200Z" fill="#bfb7a6"/>`;
    s += `<rect x="${vx - 70}" y="${vy - 90}" width="140" height="180" fill="#9e9686"/><rect x="${vx - 34}" y="${vy - 70}" width="68" height="22" fill="#1fbf6a"/><circle cx="${vx}" cy="${vy - 59}" r="70" fill="url(#zExit)"/>`;
    for (let k = 0; k < 4; k++) { // doors in perspective on both walls
      const u0 = 0.12 + k * 0.2, u1 = u0 + 0.1, lerp = (a, b, u) => a + (b - a) * u;
      for (const side of [-1, 1]) {
        const xa = lerp(side < 0 ? -400 : 1480, vx + side * 70, u0), xb = lerp(side < 0 ? -400 : 1480, vx + side * 70, u1);
        const ya = lerp(-200, vy - 90, u0) + (lerp(2200, vy + 90, u0) - lerp(-200, vy - 90, u0)) * 0.3, yb = lerp(-200, vy - 90, u1) + (lerp(2200, vy + 90, u1) - lerp(-200, vy - 90, u1)) * 0.3;
        const fa = lerp(2200, vy + 90, u0), fb = lerp(2200, vy + 90, u1);
        s += `<path d="M${f1(xa)},${f1(ya)}L${f1(xb)},${f1(yb)}L${f1(xb)},${f1(fb)}L${f1(xa)},${f1(fa)}Z" fill="#7a5a3e" ${OUT}/>`;
      }
    }
    for (let k = 0; k < 5; k++) { const u = 0.08 + k * 0.19, y = -200 + (vy - 90 + 200) * u; s += `<rect x="${f1(vx - 40 - (1 - u) * 300)}" y="${f1(y)}" width="${f1(80 + (1 - u) * 600)}" height="${f1(6 + (1 - u) * 20)}" fill="#fff8e0" opacity=".8"/>`; }
    s += `<path d="M300,1700c40,-30 120,-20 160,10c-30,30 -120,40 -160,-10z" fill="#5a1010" opacity=".8"/>`;
    put(L.set, s);
    put(L.light, `<path d="M-200,-200H1280V2120H-200Z M540,960m-480,0a480,480 0 1,0 960,0a480,480 0 1,0 -960,0Z" fill="#050505" fill-rule="evenodd"/>
      <circle cx="540" cy="960" r="484" fill="url(#zLens)"/><circle cx="540" cy="960" r="482" fill="none" stroke="#2a2826" stroke-width="10"/>
      <path d="M330,700q90,-110 230,-120" stroke="#fff" stroke-width="16" fill="none" opacity=".12" stroke-linecap="round"/>`);
    if (o.face) put(L.act, zFace(`${id}-face`, 540, 960, 1));
  }
  // a front-facing infected face (peephole jump scare): milky eyes, dark veins, torn mouth, wet hair
  function zFace(id, x, y, s) {
    return `<g id="${id}" transform="translate(${x},${y}) scale(${s})" opacity="0"><g id="${id}-in">
      <path d="M-300,-60C-300,-330 -170,-430 0,-430C170,-430 300,-330 300,-60C300,190 180,380 0,400C-180,380 -300,190 -300,-60Z" fill="url(#zSkinF)" ${OUT}/>
      <path d="M-300,-120C-320,-380 -120,-470 20,-460C180,-450 330,-360 300,-140C260,-260 160,-330 30,-330C-120,-330 -230,-260 -300,-120Z" fill="#26201c" ${OUT}/>
      ${[-180, -120, 140, 200].map((x2, k) => `<path d="M${x2},-250C${x2 + 10},-140 ${x2 - 20},-40 ${x2},${60 + k * 20}" stroke="#26201c" stroke-width="22" fill="none" stroke-linecap="round"/>`).join("")}
      ${[-1, 1].map((d) => `<ellipse cx="${d * 110}" cy="-60" rx="70" ry="46" fill="#4a5a46" opacity=".55"/><ellipse cx="${d * 110}" cy="-64" rx="54" ry="36" fill="#e4ebde" ${OUT}/><circle cx="${d * 104}" cy="-60" r="7" fill="#606c5c"/>
        <path d="M${d * 60},-80l${d * -30},-10M${d * 160},-40l${d * 40},20M${d * 150},-90l${d * 50},-30" stroke="#b03a3a" stroke-width="3" opacity=".7"/>`).join("")}
      ${[[-240, 40, -180, 140], [230, 20, 190, 160], [-80, 200, -40, 300], [60, -200, 120, -280]].map(([a, b, c, d]) => `<path d="M${a},${b}Q${(a + c) / 2 + 20},${(b + d) / 2} ${c},${d}" stroke="#4c5f52" stroke-width="5" fill="none" opacity=".7"/>`).join("")}
      <path d="M-120,150Q0,110 120,150Q90,290 0,300Q-90,290 -120,150Z" fill="#2a0808" ${OUT}/><path d="M-100,156l20,26l20,-26l20,26l20,-26l20,26l20,-26l20,26l20,-26" stroke="#e9e2cf" stroke-width="7" fill="none"/>
      <path d="M-40,170q-6,60 -20,120M30,175q10,50 4,100" stroke="#7a1414" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M-20,20q20,30 0,60" stroke="#6b7b64" stroke-width="6" fill="none"/></g></g>`;
  }

  // ---------------- close-up: a forearm under the tap (bite with soap, or an old healed scar) ----------------
  function armClose(L, o = {}) {
    const id = o.id || "ac", r = mk(o.seed || 41), skin = o.skin || "#ecc29c", sleeve = o.sleeve || "#e07a3f", night = !!o.night;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="${night ? "#0c0f14" : "#cfd8d5"}"/>`);
    let far = `<rect x="-900" y="-600" width="2900" height="3200" fill="${night ? "#141a22" : "url(#zTile)"}"/>`;
    for (let k = 0; k < 24; k++) far += `<path d="M${-900 + k * 130},-600V2600" stroke="${night ? "#1b222c" : "#b9c6c1"}" stroke-width="4"/><path d="M-900,${-600 + k * 130}H2000" stroke="${night ? "#1b222c" : "#b9c6c1"}" stroke-width="4"/>`;
    put(L.far, far);
    let s = "";
    if (o.water !== false) {
      s += `<path d="M-200,1280Q540,1180 1300,1280V2400H-200Z" fill="#f4f6f4" ${OUT}/><ellipse cx="540" cy="1360" rx="520" ry="80" fill="#dfe6e4"/><ellipse cx="560" cy="1380" rx="60" ry="16" fill="#9aa6ad"/>
        <g transform="translate(200,0)"><path d="M140,380h160q30,0 30,30v60h170q40,0 40,40v40h-60v-24h-180v60h-130z" fill="url(#zChrome)" ${OUT}/><rect x="120" y="300" width="80" height="60" rx="14" fill="url(#zChrome)" ${OUT}/></g>
        <g id="${id}-stream" transform="translate(200,0)"><rect x="468" y="566" width="44" height="760" fill="url(#zWater)"/>${Array.from({ length: 8 }, (_, k) => `<path class="foam" d="M${478 + (k % 3) * 10},${580 + k * 90}v60" stroke="#ffffff" stroke-width="4" stroke-dasharray="20 30" opacity=".8"/>`).join("")}</g>`;
    }
    // forearm from the right edge, hand palm-down on the left
    const arm = `<g id="${id}-arm"><path d="M1300,1000L640,1010C600,1010 560,1000 520,1006L500,1110C540,1116 600,1110 640,1110L1300,1130Z" fill="${skin}" ${OUT}/>
      <path d="M530,1010C470,990 400,1000 360,1030C330,1050 300,1060 268,1062C250,1064 248,1080 266,1084L360,1090C380,1110 420,1124 470,1118L506,1110Z" fill="${skin}" ${OUT}/>
      <path d="M362,1040l-60,-6M372,1056l-70,4M380,1074l-64,12" stroke="${INK}" stroke-width="3" opacity=".5"/>
      <path d="M640,1100C780,1108 1000,1112 1300,1122" stroke="${INK}" stroke-width="3" opacity=".25" fill="none"/><path d="M560,1026C760,1028 1000,1032 1300,1040" stroke="#fff" stroke-width="12" opacity=".22" fill="none" stroke-linecap="round"/>
      ${o.mark === "scar" ? `<g id="${id}-scar"><path d="M626,1030q74,-40 156,0M632,1092q70,22 140,0" stroke="#f3c9b8" stroke-width="16" fill="none" stroke-linecap="round" opacity=".7"/>${[...Array(7)].map((_, k) => `<ellipse cx="${640 + k * 22}" cy="${1032 + Math.sin(k / 6 * Math.PI) * -10}" rx="6" ry="9" fill="#f0c4b4" stroke="#d49e8c" stroke-width="2"/>`).join("")}${[...Array(6)].map((_, k) => `<ellipse cx="${650 + k * 22}" cy="${1086 - Math.sin(k / 5 * Math.PI) * -8}" rx="6" ry="8" fill="#f0c4b4" stroke="#d49e8c" stroke-width="2"/>`).join("")}</g>`
        : `<g id="${id}-bite"><path d="M624,1040q70,-34 150,0" stroke="#b04040" stroke-width="5" fill="none" opacity=".6"/>${[...Array(7)].map((_, k) => `<ellipse cx="${630 + k * 22}" cy="${1034 + Math.sin(k / 6 * Math.PI) * -10}" rx="7" ry="10" fill="#8e1414"/>`).join("")}${[...Array(6)].map((_, k) => `<ellipse cx="${640 + k * 22}" cy="${1086 - Math.sin(k / 5 * Math.PI) * -8}" rx="7" ry="9" fill="#8e1414"/>`).join("")}
          <path id="${id}-drip" d="M700,1100c-6,30 -2,50 -8,70" stroke="#9e1414" stroke-width="9" fill="none" stroke-linecap="round"/></g>`}
      <g id="${id}-foam" opacity="0">${Array.from({ length: 26 }, () => `<circle cx="${f1(600 + r() * 220)}" cy="${f1(1000 + r() * 110)}" r="${f1(6 + r() * 16)}" fill="#ffffff" stroke="#d8e4ea" stroke-width="2" opacity=".9"/>`).join("")}</g>
      <rect x="860" y="980" width="460" height="170" rx="30" fill="${sleeve}" ${OUT}/><path d="M870,990v150" stroke="${INK}" stroke-width="3" opacity=".4"/>
      <g id="${id}-cuff" transform="translate(400,0)"><rect x="470" y="976" width="420" height="178" rx="30" fill="${sleeve}" ${OUT}/><path d="M480,986v154" stroke="${INK}" stroke-width="3" opacity=".4"/></g></g>`;
    s += arm;
    if (o.water !== false) s += `<g id="${id}-splash">${Array.from({ length: 12 }, () => `<circle class="foam" cx="${f1(640 + r() * 110)}" cy="${f1(960 + r() * 60)}" r="${f1(5 + r() * 9)}" fill="#e8f6fb" opacity=".85"/>`).join("")}</g>`;
    put(L.set, s);
    if (night) put(L.glow, `<circle cx="760" cy="900" r="700" fill="url(#zPhone)"/>`);
  }

  // ---------------- bathroom: tub filling, buckets and pots on the floor ----------------
  function bathroom(L, o = {}) {
    const id = o.id || "bt", G = 1520;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#cfd8d5"/>`);
    let far = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="url(#zTile)"/>`;
    for (let k = 0; k < 24; k++) far += `<path d="M${-900 + k * 120},-600V${G}" stroke="#b9c6c1" stroke-width="4"/><path d="M-900,${-600 + k * 120}H2000" stroke="#b9c6c1" stroke-width="4"/>`;
    put(L.far, far);
    let s = `<rect x="-900" y="${G}" width="2900" height="1200" fill="#a9b2b0"/>`;
    s += `<g><path d="M300,820h120q30,0 30,30v40h-40v-30h-110z" fill="url(#zChrome)" ${OUT}/></g>`;
    s += `<rect id="${id}-stream" x="400" y="890" width="30" height="${1440 - 890}" fill="url(#zWater)"/>`;
    s += `<defs><clipPath id="${id}-tc"><path d="M120,1200H780V1420Q780,1480 720,1480H180Q120,1480 120,1420Z"/></clipPath></defs>
      <path d="M100,1180H800V1430Q800,1500 730,1500H170Q100,1500 100,1430Z" fill="#f4f6f4" ${OUT}/>
      <g clip-path="url(#${id}-tc)"><rect id="${id}-water" x="100" y="1480" width="700" height="300" fill="url(#zTub)"/></g>
      <path d="M100,1180H800" stroke="${INK}" stroke-width="10"/><path d="M180,1500v30M720,1500v30" stroke="#9aa6ad" stroke-width="16"/>`;
    if (o.door) s += `<g transform="translate(860,0)"><rect x="0" y="700" width="230" height="${G - 700}" fill="#e8e2d8" ${OUT}/><rect x="14" y="714" width="202" height="${G - 724}" fill="#a88a68" ${OUT}/>
      <rect x="30" y="1080" width="24" height="56" rx="8" fill="url(#zChrome)" ${OUT}/><rect x="0" y="${G - 10}" width="230" height="10" fill="#fff4cf"/>
      <g id="${id}-feet" opacity="0"><ellipse cx="80" cy="${G - 4}" rx="34" ry="6" fill="#1a1612"/><ellipse cx="150" cy="${G - 4}" rx="34" ry="6" fill="#1a1612"/></g></g>`;
    if (!o.door) s += [[880, "#4f8fbf", 120], [1010, "#e07a3f", 100]].map(([x, c, w], k) => `<g transform="translate(${x},${G})"><path d="M${-w / 2},-160L${-w / 2 + 12},0H${w / 2 - 12}L${w / 2},-160Z" fill="${c}" ${OUT}/>
      <defs><clipPath id="${id}-bc${k}"><path d="M${-w / 2 + 6},-154L${-w / 2 + 16},-6H${w / 2 - 16}L${w / 2 - 6},-154Z"/></clipPath></defs><g clip-path="url(#${id}-bc${k})"><rect class="blevel" id="${id}-b${k}" x="${-w}" y="0" width="${w * 2}" height="200" fill="#8fc3d6" opacity=".9"/></g>
      <path d="M${-w / 2 + 6},-160q${w / 2 - 6},-60 ${w - 12},0" stroke="#3a3f45" stroke-width="5" fill="none"/></g>`).join("");
    put(L.set, s);
  }

  // ---------------- the building's water: pump in the basement → roof tank → taps (cross-section diagram) ----------------
  function tower(L, o = {}) {
    const id = o.id || "tw";
    put(L.sky, `<rect x="-900" y="-400" width="2900" height="2800" fill="url(#diagBg)"/>` + Array.from({ length: 18 }, (_, k) => `<path d="M-900,${k * 130}H2000" stroke="#22363d" stroke-width="2"/>`).join(""));
    let s = `<rect x="300" y="300" width="480" height="1400" fill="#22343b" stroke="#cfc4a8" stroke-width="5"/>`;
    for (let k = 0; k <= 23; k++) s += `<path d="M300,${1640 - k * 56}H780" stroke="#3f5650" stroke-width="3"/>`;
    s += `<rect x="300" y="1700" width="480" height="140" fill="#1b282d" stroke="#cfc4a8" stroke-width="5"/>`;
    s += `<g transform="translate(420,1772)"><rect x="-60" y="-40" width="120" height="80" rx="12" fill="#5f6b70" stroke="#cfc4a8" stroke-width="4"/><circle cx="0" cy="0" r="26" fill="#2e3a3f" stroke="#cfc4a8" stroke-width="4"/><path class="spin" d="M0,-20V20M-20,0H20" stroke="#cfc4a8" stroke-width="5"/></g>`;
    s += `<g transform="translate(640,210)"><rect x="-90" y="-60" width="180" height="120" rx="14" fill="#4f7f96" stroke="#cfc4a8" stroke-width="5"/><rect id="${id}-tank" x="-80" y="-20" width="160" height="70" fill="#8fc3d6"/></g>`;
    s += `<path d="M480,1772H560V270" stroke="#3f5650" stroke-width="18" fill="none"/><path id="${id}-up" d="M480,1772H560V270" stroke="#8fc3d6" stroke-width="10" fill="none" stroke-dasharray="30 24"/>`;
    s += `<path d="M700,270V1640" stroke="#3f5650" stroke-width="14"/><path id="${id}-down" d="M700,270V1640" stroke="#8fc3d6" stroke-width="7" fill="none" stroke-dasharray="24 22"/>`;
    s += `<g transform="translate(740,352)"><circle r="18" fill="#e8705a"/><circle r="34" fill="none" stroke="#e8705a" stroke-width="4"/></g>`;
    s += `<g id="${id}-bolt" transform="translate(230,1700)"><path d="M10,-80L-30,10H0L-10,80L40,-20H8L22,-80Z" fill="#f2c55c" stroke="#2e2a26" stroke-width="4"/></g>`;
    s += `<g id="${id}-x" opacity="0"><path d="M150,1610l160,160M310,1610l-160,160" stroke="#fff" stroke-width="30" stroke-linecap="round"/><path d="M150,1610l160,160M310,1610l-160,160" stroke="#e8443a" stroke-width="18" stroke-linecap="round"/>
      <path d="M380,1700l90,140M470,1700l-90,140" stroke="#e8443a" stroke-width="14" stroke-linecap="round"/></g>`;
    const tag = (x, y, t, c) => `<g transform="translate(${x},${y})"><rect x="${-t.length * 15}" y="-36" width="${t.length * 30}" height="60" rx="12" fill="#0d171b" stroke="${c}" stroke-width="4"/><text y="7" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="${c}">${t}</text></g>`;
    s += `<g id="${id}-tags">${tag(560, 1920, "ปั๊มน้ำ", "#8fc3d6")}${tag(170, 1560, "ไฟดับ", "#f2c55c")}</g>`;
    put(L.set, s);
  }

  // ---------------- fire stairs: a landing seen from the side, the floor number painted on the wall ----------------
  function stairwell(L, o = {}) {
    const id = o.id || "sw", G = 1500, fl = o.floor ?? 23;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#0d1110"/>`);
    let s = `<rect x="-900" y="-600" width="2900" height="${G + 600}" fill="#5d6460"/><rect x="-900" y="700" width="2900" height="40" fill="#4e5551"/>`;
    for (let k = 0; k < 12; k++) s += `<path d="M${-900 + k * 260},-600V${G}" stroke="#555c58" stroke-width="3"/>`;
    s += `<text id="${id}-num" x="520" y="1180" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="420" fill="#e8e2cf" opacity=".9">${fl}</text>`;
    s += `<g transform="translate(150,520)"><rect x="-70" y="-30" width="140" height="60" rx="6" fill="#1fbf6a" ${OUT}/><path d="M-40,0h40M10,-12l14,12l-14,12" stroke="#fff" stroke-width="7" fill="none"/></g>`;
    s += `<rect x="-900" y="${G}" width="1700" height="40" fill="#8a8f8a"/><rect x="-900" y="${G + 40}" width="1700" height="1200" fill="#3f4542"/>`;
    for (let k = 0; k < 10; k++) s += `<path d="M${800 + k * 90},${G + k * 70}h90v70" fill="none" stroke="#8a8f8a" stroke-width="16"/>`;
    s += `<path d="M800,${G}L1700,${G + 700}V2700H800Z" fill="#3f4542"/>`;
    s += `<path d="M-900,${G - 190}H800L1700,${G + 510}" stroke="#c9ccd0" stroke-width="12" fill="none"/>${Array.from({ length: 14 }, (_, k) => `<path d="M${-800 + k * 120},${G - 190}V${G}" stroke="#c9ccd0" stroke-width="6"/>`).join("")}`;
    put(L.set, s);
    put(L.glow, `<circle cx="150" cy="520" r="520" fill="url(#zExit)"/>`);
  }
  // looking straight down the stairwell shaft: rails spiral away, something looks up from far below
  function stairShaft(L, o = {}) {
    const id = o.id || "ss";
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3200" fill="#030404"/>`);
    let s = "";
    for (let k = 0; k < 9; k++) {
      const w = 980 * Math.pow(0.78, k), h = 1500 * Math.pow(0.78, k), x = 540 - w / 2, y = 960 - h / 2;
      s += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="none" stroke="${k % 2 ? "#5d6460" : "#7a807c"}" stroke-width="${f1(60 * Math.pow(0.8, k))}"/>`;
      s += `<rect x="${f1(x + 8)}" y="${f1(y + 8)}" width="${f1(w - 16)}" height="${f1(h - 16)}" fill="none" stroke="#c9ccd0" stroke-width="${f1(8 * Math.pow(0.8, k))}" opacity=".7"/>`;
      if (k % 2 === 0) s += `<circle cx="${f1(x + 30)}" cy="${f1(y + 30)}" r="${f1(140 * Math.pow(0.78, k))}" fill="url(#zExit)"/>`;
    }
    s += `<g id="${id}-up" opacity="0" transform="translate(560,960) scale(.16)">${zFace(`${id}-uf`, 0, 0, 1).replace('opacity="0"', "")}</g>`;
    s += `<g id="${id}-hand" opacity="0"><path d="M610,880q30,-10 50,4M612,892q34,-2 52,12M610,904q30,4 44,20" stroke="#a9b8a0" stroke-width="7" fill="none" stroke-linecap="round"/></g>`;
    put(L.set, s);
  }

  // looping motion for these sets
  function zlife(tl, scope, t0, dur) {
    const q = (c) => document.querySelectorAll(`${scope} ${c}`);
    q(".smoke").forEach((el, i) => tl.fromTo(el, { x: -10, opacity: 0.4 }, { x: 14, opacity: 0.6, duration: 2.4 + i * 0.4, repeat: Math.ceil(dur / 2.4), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0));
    q(".beacon").forEach((el) => tl.fromTo(el, { opacity: 0.1 }, { opacity: 0.6, duration: 0.25, repeat: Math.ceil(dur / 0.25), yoyo: true, immediateRender: false }, t0));
    q(".beacon2").forEach((el) => tl.fromTo(el, { opacity: 0.6 }, { opacity: 0.1, duration: 0.25, repeat: Math.ceil(dur / 0.25), yoyo: true, immediateRender: false }, t0));
    q(".spin").forEach((el) => tl.fromTo(el, { rotation: 0 }, { rotation: 360 * Math.ceil(dur), svgOrigin: "0 0", duration: dur, ease: "none", immediateRender: false }, t0));
  }

  Object.assign(Sets, { condo, peephole, armClose, bathroom, tower, stairwell, stairShaft });
  window.Zom = { zFace, zlife, city };
})();
