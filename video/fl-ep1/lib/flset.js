// คนเดินดิน (story 4) · sets in the channel look (layered depth, both frames). Ground for people: y 1400. Load after ltset.js + flcast.js.
//   Sets.flCity(L, o)  the vertical city where everyone flies: sky (o.time day|dusk|night), the golden ring high up (far; o.ringNear {x,y,r} draws one in the set layer for framing),
//                      tower skylines far + mid with round flight openings and flyers, the plaza ground, the main tower on the right (face x 1150…2400, floor bands every 90 px, #id-tower)
//                      o.stairs → the iron zigzag stairs bolted on its left face (#id-stairs, scale it from the bottom to "weld" it up) · o.step1 → the big first step with the graffiti (#id-graf, opacity 0)
//                      o.nest → the launch ledge รังบิน on the left tower (platform x −260…520, top y 980) · o.mattress {x} → a mattress pile · o.screen → the giant screen on the left tower (#id-screen = inner group, screen x −160…620, y 300…860)
//                      o.stage → a stage at x 540 (top y 1300, #id-stage) · o.crowd → dark silhouettes along the ground · o.school → the school sign on the floor-40 band · o.flyers (count, default 7)
//   Sets.flRoom(L, o)  the boy's room at night: the window (x 260…820, y 380…980) with the ring and the lit city, the homemade telescope on a tripod at x 560 (#id-scope), the desk at x 1250 with a lamp and the open notebook (#id-note), the bed on the left
//   Sets.flClass(L, o) the classroom: the chalkboard (x 160…920, y 420…920, #id-board; draw the graph into #id-boardG), the teacher's desk x 1150, two pupil desks in front (y 1260, .act-front), windows on the right
(function () {
  const f = (v) => (+v).toFixed(1);
  const mk = (s) => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const T = (x, y, size, text, o = {}) => `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.anchor || "middle"}" font-family="${o.font || "Kanit"}" font-weight="${o.w || 800}" font-size="${size}" fill="${o.fill || "#222"}"${o.op ? ` opacity="${o.op}"` : ""}${o.rot ? ` transform="rotate(${o.rot} ${f(x)} ${f(y)})"` : ""}>${text}</text>`;
  Sets.DEFS += `
    <linearGradient id="flDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a7ac8"/><stop offset=".45" stop-color="#8ec0ea"/><stop offset=".85" stop-color="#e8e6dc"/><stop offset="1" stop-color="#f0ecdc"/></linearGradient>
    <linearGradient id="flDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2a60"/><stop offset=".45" stop-color="#7a4a80"/><stop offset=".75" stop-color="#e88a60"/><stop offset="1" stop-color="#f4c890"/></linearGradient>
    <linearGradient id="flNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05071a"/><stop offset=".5" stop-color="#101838"/><stop offset=".85" stop-color="#242c50"/><stop offset="1" stop-color="#343a58"/></linearGradient>
    <radialGradient id="flRingG"><stop offset="0" stop-color="#fff2b0" stop-opacity=".9"/><stop offset=".45" stop-color="#ffd060" stop-opacity=".35"/><stop offset="1" stop-color="#ffb030" stop-opacity="0"/></radialGradient>
    <linearGradient id="flGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0a0"/><stop offset=".5" stop-color="#e8b830"/><stop offset="1" stop-color="#a87820"/></linearGradient>
    <linearGradient id="flTowerD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8c4d8"/><stop offset="1" stop-color="#7a86a0"/></linearGradient>
    <linearGradient id="flTowerN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3050"/><stop offset="1" stop-color="#161a30"/></linearGradient>
    <linearGradient id="flIron" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a4e58"/><stop offset=".5" stop-color="#8a8f9a"/><stop offset="1" stop-color="#3a3e48"/></linearGradient>
    <linearGradient id="flPlaza" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8c4bc"/><stop offset="1" stop-color="#9a968e"/></linearGradient>
    <radialGradient id="flLampW"><stop offset="0" stop-color="#fff4c8" stop-opacity=".9"/><stop offset=".4" stop-color="#ffd890" stop-opacity=".35"/><stop offset="1" stop-color="#ff9a30" stop-opacity="0"/></radialGradient>
    <radialGradient id="flScreenG"><stop offset="0" stop-color="#9ad8ff" stop-opacity=".5"/><stop offset="1" stop-color="#3a70d0" stop-opacity="0"/></radialGradient>`;
  const SKY = { day: "flDay", dusk: "flDusk", night: "flNight" };
  const dark = (t) => t === "night";
  const ring = (x, y, r, o = {}) => `<g class="flRing" transform="translate(${f(x)},${f(y)})"><circle r="${f(r * 2.2)}" fill="url(#flRingG)" opacity="${o.glow ?? 0.8}"/><circle r="${f(r)}" fill="none" stroke="url(#flGold)" stroke-width="${f(r * 0.16)}"/><circle r="${f(r)}" fill="none" stroke="#fff6c0" stroke-width="${f(r * 0.04)}" opacity=".7"/>
    ${[0, 60, 120, 180, 240, 300].map((a) => `<circle cx="${f(Math.cos(a * Math.PI / 180) * r)}" cy="${f(Math.sin(a * Math.PI / 180) * r)}" r="${f(r * 0.05)}" fill="#fff6c0" opacity=".9"/>`).join("")}</g>`;
  // a tower: x, width, top (negative = tall), colour; floor bands every 90, windows, round flight openings on some floors
  const tower = (r, x, w, top, lit, o = {}) => { const c = o.c || (lit ? "url(#flTowerN)" : "url(#flTowerD)"); let s = `<rect x="${x}" y="${top}" width="${w}" height="${1400 - top}" fill="${c}"/>`;
    for (let y = top + 60; y < 1340; y += 90) { s += `<rect x="${x}" y="${y}" width="${w}" height="6" fill="#000" opacity=".12"/>`;
      for (let xx = x + 30; xx < x + w - 50; xx += 70) { const op = r() > 0.25; if (o.holes && r() > 0.95) s += `<rect x="${xx - 8}" y="${y + 8}" width="64" height="68" rx="28" fill="#141a30" opacity=".7"/><rect x="${xx - 8}" y="${y + 8}" width="64" height="68" rx="28" fill="none" stroke="#e8b830" stroke-width="3" opacity=".5"/>`; else s += `<rect class="flWin" x="${xx}" y="${y + 16}" width="36" height="46" rx="4" fill="${lit ? (r() > 0.4 ? "#ffd890" : "#8ad8ff") : "#5a7290"}" opacity="${lit ? f(0.5 + r() * 0.5) : (op ? 0.6 : 0.25)}"/>`; } }
    return s; };
  const flyer = (x, y, s, c, dir = 1) => `<g class="flFly" transform="translate(${f(x)},${f(y)}) scale(${f(dir * s)},${f(s)})">${[0].map(() => `<path d="M-120,0H-20" stroke="${c}" stroke-width="8" stroke-linecap="round" opacity=".35"/><path d="M-100,-10H-30M-90,10H-26" stroke="${c}" stroke-width="4" stroke-linecap="round" opacity=".25"/>`).join("")}<ellipse cx="0" cy="0" rx="30" ry="11" fill="${c}"/><circle cx="34" cy="-6" r="11" fill="${c}"/><path d="M-26,-4L-54,-16M-22,6L-50,18" stroke="${c}" stroke-width="7" stroke-linecap="round"/><path d="M26,-8L58,-26M26,-2L60,-6" stroke="${c}" stroke-width="7" stroke-linecap="round"/></g>`;
  const clouds = (r, y0, c, n = 6, op = 0.85) => [...Array(n)].map((_, k) => { const x = -2200 + k * 1000 + r() * 400, y = y0 + r() * 160, s = 0.7 + r() * 0.6; return `<g transform="translate(${f(x)},${f(y)}) scale(${f(s)})" opacity="${op}"><ellipse rx="380" ry="80" fill="${c}"/><ellipse cx="-140" cy="-46" rx="200" ry="100" fill="${c}"/><ellipse cx="130" cy="-60" rx="240" ry="120" fill="${c}"/></g>`; }).join("");
  const stars = (r, n = 50) => [...Array(n)].map(() => `<circle cx="${f(-1800 + r() * 5000)}" cy="${f(-2600 + r() * 2800)}" r="${f(0.8 + r() * 1.6)}" fill="#e8ecff" opacity="${f(0.3 + r() * 0.6)}"/>`).join("");
  // the iron zigzag stairs on the main tower's left face: flights between landings, from the ground up to `top`
  const stairs = (id, x0, top) => { let s = `<g id="${id}-stairs">`; const fl = 180, w = 150; let dir = 1, y = 1400; let k = 0;
    while (y > top) { const y1 = y - fl, xa = dir > 0 ? x0 : x0 + w, xb = dir > 0 ? x0 + w : x0;
      s += `<path d="M${xa},${y}L${xb},${y1}" stroke="#3a3e48" stroke-width="22" stroke-linecap="round"/>`;
      for (let i = 0; i < 9; i++) { const t = i / 9, sx = xa + (xb - xa) * t, sy = y + (y1 - y) * t; s += `<rect x="${f(sx - 14)}" y="${f(sy - 6)}" width="28" height="10" rx="2" fill="url(#flIron)"/>`; }
      s += `<path d="M${xa},${y - 60}L${xb},${y1 - 60}" stroke="#5a5e68" stroke-width="5" fill="none"/>${[0.3, 0.7].map((t) => `<path d="M${f(xa + (xb - xa) * t)},${f(y + (y1 - y) * t)}v-60" stroke="#5a5e68" stroke-width="4"/>`).join("")}`;
      s += `<rect x="${x0 - 10}" y="${y1 - 8}" width="${w + 20}" height="14" rx="3" fill="#4a4e58"/><path d="M${x0 + w + 10},${y1}L${x0 + w + 60},${y1 - 40}M${x0 + w + 10},${y1 - 90}L${x0 + w + 60},${y1 - 40}" stroke="#3a3e48" stroke-width="8"/>`;
      y = y1; dir = -dir; k++; }
    return s + "</g>"; };
  const mattress = (x) => `<g transform="translate(${x},1400)">${[0, 1, 2, 3].map((k) => `<rect x="-170" y="${-44 - k * 44}" width="340" height="40" rx="12" fill="${k % 2 ? "#e8d8c8" : "#d8c0b8"}"/><rect x="-170" y="${-44 - k * 44}" width="340" height="40" rx="12" fill="url(#flV)" opacity=".4"/><path d="M-120,${-24 - k * 44}h240" stroke="#b89a90" stroke-width="2" stroke-dasharray="14 10"/>`).join("")}</g>`;
  const silhouettes = (r, n = 22) => [...Array(n)].map((_, k) => { const x = -1400 + k * 180 + r() * 100, s = 0.9 + r() * 0.3, c = "#101424"; return `<g transform="translate(${f(x)},1400) scale(${f(s)})"><rect x="-22" y="-300" width="44" height="300" rx="20" fill="${c}"/><circle cy="-340" r="34" fill="${c}"/>${r() > 0.5 ? `<path d="M-30,-250L-60,-400" stroke="${c}" stroke-width="14" stroke-linecap="round"/>` : ""}<path d="M30,-250L60,-400" stroke="${c}" stroke-width="14" stroke-linecap="round"/></g>`; }).join("");
  Sets.flCity = (L, o = {}) => {
    const id = o.id || "flc", r = mk(o.seed || 5), time = o.time || "day", lit = dark(time) || time === "dusk";
    put(L.sky, `<rect x="-3000" y="-6000" width="8000" height="11000" fill="${time === "night" ? "#05071a" : time === "dusk" ? "#2a2a60" : "#3a7ac8"}"/><rect x="-3000" y="-3200" width="8000" height="4600" fill="url(#${SKY[time]})"/>
      ${time === "night" ? stars(r) : `<circle cx="300" cy="-200" r="520" fill="url(#flLampW)" opacity=".5"/>`}`);
    // far: the ring, high clouds, the distant towers
    let far = ring(540, -160, 230, { glow: time === "night" ? 1 : 0.7 }) + clouds(r, -500, time === "night" ? "#1a2040" : "#ffffff", 6, time === "night" ? 0.6 : 0.8);
    [[-2400, 420, -500], [-1900, 300, -1100], [-1500, 380, -300], [-1050, 260, -1400], [-650, 340, -700], [-250, 300, -1700], [160, 360, -400], [560, 280, -1200], [900, 320, -800], [1300, 400, -1500], [1750, 300, -500], [2100, 460, -1100], [2650, 360, -800], [3100, 420, -400]].forEach(([x, w, top]) => { far += tower(r, x, w, top, lit, { c: lit ? "#141a34" : "#9aa8c4" }); });
    far += `<rect x="-3000" y="900" width="8000" height="520" fill="url(#${lit ? "jkHazeW" : "jkHazeW"})" opacity="${lit ? 0.25 : 0.5}"/>`;
    for (let i = 0; i < (o.flyers ?? 7); i++) far += flyer(-1600 + i * 620 + r() * 300, -1600 + r() * 2000, 0.5 + r() * 0.4, lit ? "#2a3454" : "#6a7a98", r() > 0.5 ? 1 : -1);
    put(L.far, far);
    // mid: nearer towers with flight openings, mid flyers
    let mid = "";
    [[-1700, 520, -1000], [-900, 460, -1600], [-150, 420, -700], [2500, 560, -1300], [3200, 480, -900]].forEach(([x, w, top]) => { mid += tower(r, x, w, top, lit, { holes: true }); });
    for (let i = 0; i < 5; i++) mid += flyer(-1200 + i * 700 + r() * 300, -1200 + r() * 1600, 0.8 + r() * 0.4, lit ? "#1c2238" : "#4a5a78", r() > 0.5 ? 1 : -1);
    put(L.mid, mid);
    // set: the plaza, the main tower on the right, the left tower (nest / screen), props
    let s = `<rect x="-3000" y="1400" width="8000" height="1400" fill="url(#flPlaza)"/><rect x="-3000" y="1400" width="8000" height="14" fill="#7a766e"/>${[...Array(40)].map((_, k) => `<path d="M${-3000 + k * 200},1400v1400" stroke="#8a867e" stroke-width="2" opacity=".5"/>`).join("")}
      ${lit ? `<rect x="-3000" y="1400" width="8000" height="1400" fill="#0a0c18" opacity=".55"/>` : ""}`;
    // main tower right
    s += `<g id="${id}-tower">${tower(r, 1150, 1300, -3400, lit, { holes: true })}<rect x="1150" y="-3400" width="24" height="4800" fill="#000" opacity=".18"/>`;
    if (o.school) s += `<g transform="translate(1460,${o.schoolY ?? -2100})"><rect x="-260" y="-70" width="520" height="90" rx="12" fill="#f4ecd8"/><rect x="-260" y="-70" width="520" height="90" rx="12" fill="none" stroke="#3a3e48" stroke-width="5"/>${T(0, -8, 52, "โรงเรียน · ชั้น 40", { fill: "#2a2a34", w: 900 })}</g>`;
    s += `</g>`;
    if (o.stairs) s += stairs(id, 990, o.stairsTop ?? -3200);
    if (o.step1) s += `<g id="${id}-step1" transform="translate(1065,1400)"><rect x="-120" y="-70" width="240" height="70" rx="6" fill="#5a5e68"/><rect x="-120" y="-70" width="240" height="70" rx="6" fill="url(#flV)" opacity=".5"/><rect x="-120" y="-70" width="240" height="12" fill="#8a8f9a"/>
      <g id="${id}-graf" opacity="0">${T(0, -22, 40, "คนเดินดิน", { fill: "#ff5a2a", w: 900, rot: -3 })}<path d="M-90,-10q40,-8 80,0" stroke="#ff5a2a" stroke-width="4" fill="none" opacity=".7"/></g></g>`;
    // left tower face with the nest ledge or the giant screen
    if (o.nest || o.screen) s += tower(r, -1100, 840, -2600, lit, {});
    if (o.nest) s += `<g id="${id}-nest" transform="translate(0,980)"><path d="M-260,0H520Q560,0 560,40V60H-260Z" fill="#c8ccd4"/><path d="M-260,0H520Q560,0 560,40V60H-260Z" fill="url(#flV)" opacity=".5"/><rect x="-260" y="60" width="820" height="40" fill="#8a8f9a"/><path d="M-260,100L-200,420M520,100L400,420" stroke="#7a7e88" stroke-width="18"/>
      <path d="M-240,-150H-100M-240,0V-150" stroke="#e8b830" stroke-width="10" fill="none"/>${T(-60, -60, 34, "รังบิน", { fill: "#2a2a34", w: 900, anchor: "start" })}
      ${[-180, 40, 260, 480].map((x) => `<path d="M${x},-6v-120" stroke="#e8b830" stroke-width="8"/>`).join("")}<path d="M-240,-126H500" stroke="#e8b830" stroke-width="8"/></g>`;
    if (o.screen) s += `<g transform="translate(0,0)"><rect x="-190" y="270" width="840" height="620" rx="18" fill="#1a1c28"/><rect x="-160" y="300" width="780" height="560" rx="10" fill="#0a0c18"/><g id="${id}-screen"></g><rect x="-160" y="300" width="780" height="560" rx="10" fill="url(#flScreenG)" opacity=".35" style="mix-blend-mode:screen"/>
      ${[-120, 580].map((x) => `<circle cx="${x}" cy="290" r="10" fill="#ff3a2a"/>`).join("")}${T(-130, 335, 22, "● LIVE", { fill: "#ff5a4a", w: 900, anchor: "start" })}</g>`;
    if (o.stage) s += `<g id="${id}-stage" transform="translate(540,1400)"><rect x="-320" y="-100" width="640" height="100" rx="8" fill="#3a3040"/><rect x="-320" y="-100" width="640" height="100" rx="8" fill="url(#flV)" opacity=".6"/><rect x="-300" y="-112" width="600" height="18" rx="4" fill="#e8b830"/>${[-240, -80, 80, 240].map((x) => `<circle cx="${x}" cy="-116" r="8" fill="#fff6c0"/>`).join("")}</g>`;
    if (o.mattress) s += mattress(o.mattress.x ?? 300);
    if (o.crowd) s += silhouettes(r);
    put(L.set, s);
    if (o.ringNear) put(L.set, ring(o.ringNear.x, o.ringNear.y, o.ringNear.r, { glow: 1 }));
    if (lit) put(L.glow, `<g style="mix-blend-mode:screen">${[200, 760, 1400].map((x) => `<circle cx="${x}" cy="1300" r="220" fill="url(#flLampW)" opacity=".35"/>`).join("")}</g>`);
  };

  Sets.flRoom = (L, o = {}) => {
    const id = o.id || "flr", r = mk(o.seed || 11);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#2a2434"/>`);
    put(L.far, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#3a3448"/>`);
    // the wall with the window: outside = night city + the ring
    let s = `<rect x="-3000" y="-3000" width="8000" height="4400" fill="#3e3a50"/><rect x="-3000" y="-3000" width="8000" height="4400" fill="url(#flV)" opacity=".3"/><rect x="-3000" y="1400" width="8000" height="1400" fill="#5a4a3a"/><rect x="-3000" y="1400" width="8000" height="14" fill="#3a2a20"/>
      <g id="${id}-win"><rect x="240" y="360" width="600" height="640" rx="8" fill="#0a0c20"/><rect x="260" y="380" width="560" height="600" fill="url(#flNight)"/>${stars(r, 24).replace(/cy="[^"]*"/g, (m) => `cy="${f(400 + r() * 300)}"`).replace(/cx="[^"]*"/g, (m) => `cx="${f(280 + r() * 520)}"`)}
        ${ring(700, 470, 60, { glow: 1 })}${[[280, 160, 700], [420, 90, 760], [500, 130, 640], [640, 110, 720], [740, 80, 790]].map(([x, w, top]) => `<rect x="${x}" y="${top}" width="${w}" height="${980 - top}" fill="#141a34"/>${[...Array(4)].map((_, k) => `<rect x="${x + 14}" y="${top + 30 + k * 50}" width="14" height="18" fill="#ffd890" opacity=".8"/>`).join("")}`).join("")}
        <rect x="240" y="360" width="600" height="640" rx="8" fill="none" stroke="#e8e0d0" stroke-width="22"/><path d="M540,360V1000M240,680H840" stroke="#e8e0d0" stroke-width="12"/>
        <path d="M180,340H300V1020H180Z" fill="#8a5a7a"/><path d="M180,340H300V1020H180Z" fill="url(#flV)" opacity=".5"/></g>
      <g id="${id}-bed" transform="translate(-200,1400)"><rect x="-300" y="-260" width="620" height="260" rx="12" fill="#6a7aa8"/><rect x="-300" y="-260" width="620" height="260" rx="12" fill="url(#flV)" opacity=".5"/><rect x="-280" y="-300" width="200" height="70" rx="20" fill="#f4f0e8"/></g>
      <g id="${id}-desk" transform="translate(1250,1400)"><rect x="-260" y="-300" width="520" height="24" rx="4" fill="#8a6a4a"/><path d="M-240,-276V0M240,-276V0" stroke="#6a4a30" stroke-width="18"/><rect x="-250" y="-240" width="300" height="60" fill="#7a5a3a"/>
        <g transform="translate(170,-300)"><path d="M-20,0V-120" stroke="#3a3a44" stroke-width="8"/><path d="M-60,-120L20,-120L0,-170H-40Z" fill="#3a3a44"/><circle cx="-20" cy="-116" r="40" fill="url(#flLampW)" opacity=".9"/></g>
        <g id="${id}-note" transform="translate(-60,-300) rotate(-6)"><rect x="-120" y="-10" width="240" height="160" rx="4" fill="#f4ecd8"/><path d="M0,-10V150" stroke="#c8b8a0" stroke-width="2"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-104,${16 + k * 26}h90M14,${16 + k * 26}h90" stroke="#c8d0d8" stroke-width="1.5"/>`).join("")}</g></g>
      <g id="${id}-scope" transform="translate(560,1400)"><path d="M0,-520L-120,0M0,-520L120,0M0,-520L10,-40" stroke="#5a5e68" stroke-width="14" stroke-linecap="round"/><g transform="translate(0,-540) rotate(-34)"><rect x="-40" y="-60" width="80" height="420" rx="14" fill="#3a6a8a"/><rect x="-40" y="-60" width="80" height="420" rx="14" fill="url(#flV)" opacity=".6"/><rect x="-54" y="-80" width="108" height="50" rx="10" fill="#8a8f9a"/><rect x="-26" y="340" width="52" height="40" rx="6" fill="#2a2a34"/><path d="M-20,30h40M-20,120h40" stroke="#2a4a60" stroke-width="4"/><circle cx="0" cy="-70" r="24" fill="#cfe8ff" opacity=".7"/></g><circle cx="-60" cy="-470" r="26" fill="none" stroke="#8a8f9a" stroke-width="6"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M-60,-470l${f(Math.cos(k) * 24)},${f(Math.sin(k) * 24)}" stroke="#8a8f9a" stroke-width="2"/>`).join("")}</g>`;
    put(L.set, s);
    put(L.glow, `<g style="mix-blend-mode:screen"><circle cx="1400" cy="1050" r="260" fill="url(#flLampW)" opacity=".55"/><circle cx="540" cy="680" r="380" fill="url(#flRingG)" opacity=".35"/></g>`);
  };

  Sets.flClass = (L, o = {}) => {
    const id = o.id || "flk", r = mk(o.seed || 17);
    put(L.sky, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#e8e0cc"/>`);
    put(L.far, `<rect x="-3000" y="-3000" width="8000" height="8000" fill="#efe8d8"/>`);
    let s = `<rect x="-3000" y="-3000" width="8000" height="4400" fill="#f0e8d4"/><rect x="-3000" y="-3000" width="8000" height="4400" fill="url(#flV)" opacity=".2"/><rect x="-3000" y="1400" width="8000" height="1400" fill="#c8b8a0"/><rect x="-3000" y="1400" width="8000" height="12" fill="#9a8a70"/>${[...Array(40)].map((_, k) => `<path d="M${-3000 + k * 200},1400v1400" stroke="#b8a890" stroke-width="2"/>`).join("")}
      <g id="${id}-board" transform="translate(160,420)"><rect x="-20" y="-20" width="800" height="540" rx="10" fill="#6a4a30"/><rect x="0" y="0" width="760" height="500" fill="#2e5a48"/><rect x="0" y="0" width="760" height="500" fill="url(#flV)" opacity=".3"/><g id="${id}-boardG"></g><rect x="-20" y="500" width="800" height="24" rx="4" fill="#8a6a4a"/><rect x="40" y="494" width="60" height="10" rx="3" fill="#f4f0e8"/></g>
      <g transform="translate(540,300)"><rect x="-120" y="-30" width="240" height="60" rx="8" fill="#e8b830"/>${T(0, 12, 32, "ห้อง 40/1", { fill: "#2a2a34", w: 900 })}</g>
      <g transform="translate(1900,0)"><rect x="-500" y="300" width="300" height="640" rx="8" fill="#9ad0f0"/><rect x="-500" y="300" width="300" height="640" rx="8" fill="none" stroke="#f4f0e8" stroke-width="18"/><path d="M-350,300V940M-500,620H-200" stroke="#f4f0e8" stroke-width="10"/>${ring(-330, 420, 36, { glow: 1 })}</g>
      <g id="${id}-tdesk" transform="translate(1180,1400)"><rect x="-200" y="-300" width="400" height="300" rx="6" fill="#8a6a4a"/><rect x="-200" y="-300" width="400" height="300" rx="6" fill="url(#flV)" opacity=".5"/><rect x="-210" y="-312" width="420" height="22" rx="4" fill="#a8866a"/></g>
      <circle cx="1000" cy="330" r="46" fill="#f4f0e8" stroke="#3a3e48" stroke-width="6"/><path d="M1000,330V300M1000,330L1020,342" stroke="#3a3e48" stroke-width="5" stroke-linecap="round"/>`;
    put(L.set, s);
    put(L.set, `<g class="act-front">${[300, 760].map((x) => `<g transform="translate(${x},1400)"><rect x="-190" y="-160" width="380" height="26" rx="6" fill="#c8a070"/><rect x="-190" y="-160" width="380" height="26" rx="6" fill="url(#flV)" opacity=".4"/><path d="M-170,-134V0M170,-134V0" stroke="#8a6a4a" stroke-width="14"/><rect x="-150" y="-128" width="300" height="40" fill="#a8866a"/></g>`).join("")}</g>`);
    put(L.glow, `<g style="mix-blend-mode:screen"><rect x="1300" y="300" width="800" height="1100" fill="url(#flLampW)" opacity=".25"/></g>`);
  };
})();
