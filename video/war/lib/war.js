// ---------- ทางกลับบ้าน (war, lane A): the world, the cast and the cards — a FICTIONAL border war: no flags, no real uniforms, no maps of real
// countries, no blood or wounds on screen. Load after rabfx.js (uses QkUI coins/pop/life, RabFX motes/flash) and rig2.js.
//   Sets.border(L, o)    the border grassland at o.time "day" | "dusk": hazy layered ridges (the far ridge carries #id-glint: the sun flashing
//                        off binoculars, F6 clue), a dirt path through waist-high grass, an old tree with an X notch, crossed bamboo sticks
//                        (#id-bamboo, the mine sign) at o.bamboo x, a dead tree stump, a burnt-out cart wheel, tall foreground grass (fg)
//                        o.path true · o.glint true
//   War.blast(tl, L, x, y, t, o)   a mine going off in the grass: flash, a ring of dust, a tall dust column that rises and drifts, clods of earth
//                        and grass flying (no fire, no gore) · ids #id-col etc · o.s scale · camera shake is the shot's own
//   War.dust(tl, L, x, y, t0, dur, o)  the dust column still standing and drifting (later shots; F6: the other side can see it)
//   Sets.hedge(L, o)     a hedge line at the edge of a field: a thick bush (#id-bush), an earth bank (#id-bank) and a big tree (cover)
//   War.bullets(tl, L, t0, dur, o)  bullets cutting through the bush: streaks, leaves bursting and spinning off, twigs snapping · o.n, o.box
//   Sets.home(L, o)      the mother's house front at Songkran: wooden house, a som tam stall with a mortar, string flags (plain colours),
//                        a water basin, jasmine; a parcel on the step (#id-parcel) when o.parcel
//   Rig.CAST.tao / joe / mem / enemy / mom   cast (rig2): olive field uniforms (no insignia, no flag), helmets; enemy in grey
//   WarUI.tag(tl, layer, t0, dur, o)  the rule card = the squad's dog tag on its ball chain: stamped metal, both rules, 2.5D coins,
//                        o.active highlighted with a sheen sweep, o.done ticked with a ring burst; swings on its chain the whole time
//   WarUI.cover(tl, layer, t0, dur, o)  the card: concealment (bush, grass, shadow — the bullet goes through ✗) vs cover (tree, rock, earth bank — ✓)
//   WarUI.signs(tl, layer, t0, dur, o)  the card: 4 warning signs as 2.5D coins (crossed bamboo, X on a tree, animal bones, overgrown field)
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  let seq = 0; const nid = () => "wx" + (seq++);
  Sets.DEFS += `
    <linearGradient id="wrSkyD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7aa6c8"/><stop offset=".55" stop-color="#c8d6d0"/><stop offset="1" stop-color="#ead8b0"/></linearGradient>
    <linearGradient id="wrSkyK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a66"/><stop offset=".5" stop-color="#c4786a"/><stop offset="1" stop-color="#f2b276"/></linearGradient>
    <linearGradient id="wrGrass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8b46a"/><stop offset=".5" stop-color="#8a9a4a"/><stop offset="1" stop-color="#5a6e30"/></linearGradient>
    <linearGradient id="wrGrassK" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b08a5a"/><stop offset=".5" stop-color="#7a6a3a"/><stop offset="1" stop-color="#3e3a22"/></linearGradient>
    <radialGradient id="wrDust"><stop offset="0" stop-color="#c8b08a" stop-opacity="1"/><stop offset=".6" stop-color="#a8906a" stop-opacity=".85"/><stop offset="1" stop-color="#a89878" stop-opacity="0"/></radialGradient>
    <radialGradient id="wrFlash"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset=".4" stop-color="#ffd890" stop-opacity=".7"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>
    <radialGradient id="wrGlint"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset=".25" stop-color="#fff4c0" stop-opacity=".8"/><stop offset="1" stop-color="#fff4c0" stop-opacity="0"/></radialGradient>
    <linearGradient id="wrTag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6f8"/><stop offset=".45" stop-color="#b8c0c8"/><stop offset=".7" stop-color="#e2e6ea"/><stop offset="1" stop-color="#8a949e"/></linearGradient>
    <linearGradient id="wrTagE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a848e"/><stop offset="1" stop-color="#4a525a"/></linearGradient>`;

  // ---------------- the border grassland ----------------
  const tuft = (x, y, h, c, r) => { let s = ""; for (let k = 0; k < 7; k++) { const a = (k - 3) * 0.16 + (r() - 0.5) * 0.2, hh = h * (0.6 + r() * 0.5); s += `<path d="M${f1(x + (k - 3) * 4)},${y}Q${f1(x + (k - 3) * 4 + Math.sin(a) * hh * 0.5)},${f1(y - hh * 0.6)} ${f1(x + (k - 3) * 4 + Math.sin(a) * hh)},${f1(y - hh)}" stroke="${c}" stroke-width="${f1(3 + r() * 3)}" fill="none" stroke-linecap="round"/>`; } return s; };
  Sets.border = (L, o = {}) => {
    const id = o.id || "bd", r = mk(o.seed || 31), dusk = o.time === "dusk", G = o.ground ?? 1360;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${dusk ? "wrSkyK" : "wrSkyD"})"/>
      <circle cx="${dusk ? 300 : 820}" cy="${dusk ? 760 : 260}" r="${dusk ? 120 : 70}" fill="${dusk ? "#ffcf8a" : "#fffbe8"}" opacity=".9"/>
      ${[[-200, 300, 1.2], [500, 200, 0.9], [1200, 340, 1.1]].map(([x, y, s]) => `<g transform="translate(${x},${y}) scale(${s})" opacity=".85"><ellipse cx="0" cy="0" rx="160" ry="44" fill="#fff"/><ellipse cx="60" cy="-26" rx="90" ry="40" fill="#fff"/><ellipse cx="-70" cy="-12" rx="80" ry="34" fill="#f4f0e8"/></g>`).join("")}`);
    // far ridges (haze), the far ridge with the glint
    let far = "";
    [[G - 360, "#8aa0a8", 0.9], [G - 280, "#7a9088", 1]].forEach(([y, c, op], k) => {
      let d = `M-1300,${y}`; for (let x = -1300; x <= 2400; x += 120) d += `L${x},${f1(y - 60 - Math.sin(x * 0.004 + k) * 70 - r() * 30)}`; far += `<path d="${d}L2400,${G + 200}H-1300Z" fill="${dusk ? (k ? "#6a5a6a" : "#8a7080") : c}" opacity="${op}"/>`;
    });
    put(L.far, far + (o.glint !== false ? `<g id="${id}-glint" transform="translate(${o.glintX ?? 760},${G - 392})"><g id="${id}-glint-in"><circle r="46" fill="url(#wrGlint)"/><path d="M-90,0H90" stroke="#fffbe0" stroke-width="3.4" opacity=".9" stroke-linecap="round"/><path d="M0,-38V38M-20,-20L20,20M20,-20L-20,20" stroke="#fff" stroke-width="2.6" opacity=".9" stroke-linecap="round"/><circle r="9" fill="#fff"/></g></g>` : ""));
    // mid: grassland, a lone tree, scattered shrubs
    let mid = `<path d="M-1300,${G - 120}Q500,${G - 170} 2400,${G - 110}V${G + 600}H-1300Z" fill="url(#${dusk ? "wrGrassK" : "wrGrass"})" opacity=".95"/>`;
    for (let k = 0; k < 18; k++) { const x = -1200 + r() * 3500, y = G - 120 + r() * 60; mid += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="${f1(40 + r() * 70)}" ry="${f1(18 + r() * 20)}" fill="${dusk ? "#4a4a2a" : "#6a7a3a"}" opacity=".7"/>`; }
    put(L.mid, mid);
    // set: the ground, the path, the notched tree, the stump, the wheel, the bamboo sign
    let s = `<rect x="-1300" y="${G - 40}" width="3700" height="1600" fill="${dusk ? "#5a5030" : "#8a8a48"}"/>`;
    if (o.path !== false) s += `<path d="M${o.pathX ?? 420},${G + 900}C${(o.pathX ?? 420) + 60},${G + 400} ${(o.pathX ?? 420) - 60},${G + 100} ${(o.pathX ?? 420) + 120},${G - 40}L${(o.pathX ?? 420) + 180},${G - 40}C${(o.pathX ?? 420) + 60},${G + 100} ${(o.pathX ?? 420) + 220},${G + 400} ${(o.pathX ?? 420) + 260},${G + 900}Z" fill="${dusk ? "#7a5a3a" : "#b08a5a"}" opacity=".9"/>`;
    const tx = o.tree ?? 900;
    s += `<g transform="translate(${tx},${G})"><path d="M-22,0C-26,-120 -18,-260 -8,-380H14C24,-260 30,-120 26,0Z" fill="#5a4030" ${O(3)}/>${o.notch === false ? "" : `<path d="M-4,-200l14,14M10,-200l-14,14" stroke="#e8d8b0" stroke-width="5"/>`}
      ${[[-120, -420, 120], [60, -470, 140], [-20, -540, 110], [140, -400, 90]].map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="${dusk ? "#3a4a2a" : "#4e7a34"}" ${O(3)}/><circle cx="${x - rr * 0.3}" cy="${y - rr * 0.3}" r="${rr * 0.5}" fill="${dusk ? "#5a6a3a" : "#7aa04a"}" opacity=".6"/>`).join("")}</g>`;
    s += `<g transform="translate(-180,${G + 20})"><path d="M-40,0V-50Q0,-70 40,-50V0Z" fill="#6a4a30" ${O(3)}/><ellipse cy="-52" rx="40" ry="12" fill="#8a6a48" ${O(2.5)}/></g>`;
    if (o.bamboo !== false) { const bx = o.bamboo ?? 300; s += `<g id="${id}-bamboo" transform="translate(${bx},${G + 60})"><path d="M-60,0L50,-150M60,0L-50,-150" stroke="#c8a85a" stroke-width="14" stroke-linecap="round"/><path d="M-60,0L50,-150M60,0L-50,-150" stroke="${INK}" stroke-width="2.4" fill="none"/>
      ${[[-30, -40], [30, -40], [-6, -100], [6, -100]].map(([x, y]) => `<path d="M${x - 8},${y}h16" stroke="#8a6a2a" stroke-width="3"/>`).join("")}<ellipse cy="6" rx="70" ry="10" fill="#000" opacity=".2"/></g>`; }
    put(L.set, s);
    // foreground grass, blurred by the fg layer
    let fg = ""; for (let k = 0; k < 26; k++) fg += tuft(-200 + k * 60 + r() * 40, 2000, (o.fgH ?? 1) * (280 + r() * 260), dusk ? "#4a4a22" : (k % 2 ? "#6a8a34" : "#8aa04a"), r);
    put(L.fg, fg);
  };

  // ---------------- the blast ----------------
  const War = {};
  War.bushHTML = (x, y, id, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>${[[-130, -90, 110], [0, -140, 140], [130, -90, 110], [-60, -40, 100], [70, -40, 100]].map(([cx, cy, r], k) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${k % 2 ? "#4a7430" : "#4e7a34"}" ${O(3)}/><circle cx="${cx - r * 0.3}" cy="${cy - r * 0.3}" r="${r * 0.45}" fill="#7aa04a" opacity=".6"/>`).join("")}
    ${Array.from({ length: 22 }, (_, k) => { const a = k * 2.4, rr = 60 + (k * 37) % 120; return `<path d="M${f1(Math.cos(a) * rr)},${f1(-90 + Math.sin(a) * rr * 0.6)}q8,-10 16,0q-8,10 -16,0Z" fill="#8ab05a" opacity=".8"/>`; }).join("")}</g></g>`;
  War.blast = (tl, L, x, y, t, o = {}) => {
    const id = o.id || nid(), s = o.s ?? 1, r = mk(o.seed || 17);
    let clods = "";
    for (let k = 0; k < 16; k++) clods += `<g id="${id}-c${k}">${k % 3 ? `<path d="M${f1(-10 - r() * 6)},${f1(-4 - r() * 6)}Q-2,${f1(-14 - r() * 4)} ${f1(10 + r() * 6)},-6Q${f1(14 + r() * 4)},6 4,${f1(10 + r() * 4)}Q-10,12 -12,2Z" fill="${k % 2 ? "#6a5030" : "#5a4428"}" ${O(1.8)}/>` : `<path d="M0,10Q-4,-6 -10,-20M0,10Q2,-8 8,-22M0,10Q6,0 14,-10" stroke="#7a9a3a" stroke-width="4" fill="none" stroke-linecap="round"/>`}</g>`;
    put(L.glow, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}-fl" opacity="0"><circle cy="-60" r="260" fill="url(#wrFlash)"/><path d="M0,-60L-40,-300L10,-140L60,-320L40,-120L180,-220L60,-60Z" fill="#fff6d0" opacity=".85"/></g>
      <g id="${id}-ring" opacity="0"><ellipse rx="60" ry="18" fill="none" stroke="#e8dcc0" stroke-width="18"/></g>
      <g id="${id}-col" opacity="0">${[[0, -80, 90], [-40, -170, 110], [30, -260, 130], [-10, -370, 150], [40, -470, 140]].map(([cx, cy, rr]) => `<circle cx="${cx}" cy="${cy}" r="${rr}" fill="url(#wrDust)"/>`).join("")}</g>
      ${clods}</g>`);
    tl.set([`#${id}-fl`, `#${id}-ring`, `#${id}-col`], { opacity: 0 }, 0);
    tl.fromTo(`#${id}-fl`, { opacity: 1, scale: 0.5, transformOrigin: "50% 60%" }, { opacity: 0, scale: 1.6, transformOrigin: "50% 60%", duration: 0.4, ease: "power2.in", immediateRender: false }, t);
    if (o.screen !== false) RabFX.flash(tl, t, "#fff6dc", 0.6);
    tl.fromTo(`#${id}-ring`, { opacity: 0.9, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 0, scale: 3.2, transformOrigin: "50% 50%", duration: 0.7, ease: "power2.out", immediateRender: false }, t);
    tl.fromTo(`#${id}-col`, { opacity: 0, scaleY: 0.15, scaleX: 0.5, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, scaleX: 1, transformOrigin: "50% 100%", duration: 0.35, ease: "power3.out", immediateRender: false }, t + 0.03);
    tl.to(`#${id}-col`, { x: 60, y: -40, scaleX: 1.3, transformOrigin: "50% 100%", duration: o.linger ?? 3, ease: "sine.out" }, t + 0.38);
    for (let k = 0; k < 16; k++) { const a = -Math.PI / 2 + (r() - 0.5) * 2.2, v = 260 + r() * 360;
      tl.fromTo(`#${id}-c${k}`, { x: 0, y: 0, rotation: 0, opacity: 1 }, { keyframes: [{ x: Math.cos(a) * v * 0.6, y: Math.sin(a) * v * 0.9, rotation: 200, duration: 0.45, ease: "power2.out" }, { x: Math.cos(a) * v, y: 120 + r() * 80, rotation: 400, opacity: 0.8, duration: 0.55, ease: "power2.in" }], immediateRender: false }, t); }
  };
  War.dust = (tl, L, x, y, t0, dur, o = {}) => {
    const id = nid(), s = o.s ?? 1;
    put(L.mid, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}">${[[0, -80, 90], [-40, -170, 110], [30, -260, 130], [-10, -370, 150], [40, -470, 140], [90, -570, 150]].map(([cx, cy, rr]) => `<circle cx="${cx}" cy="${cy}" r="${rr}" fill="url(#wrDust)" opacity=".85"/>`).join("")}</g></g>`);
    tl.fromTo(`#${id}`, { x: 0, y: 0 }, { x: 80, y: -60, duration: dur, ease: "none", immediateRender: false }, t0);
  };

  // ---------------- the hedge line (cover vs concealment) ----------------
  Sets.hedge = (L, o = {}) => {
    const id = o.id || "hg", G = 1400;
    Sets.border(L, { id: id + "b", time: o.time || "day", bamboo: false, path: false, glint: false, notch: false, tree: o.tree ?? 820, ground: G });
    put(L.set, `<g transform="translate(${o.bank ?? 120},${G + 140})"><g id="${id}-bank"><path d="M-260,0Q-200,-150 0,-170Q200,-150 260,0Z" fill="#7a5a34" ${O(4)}/><path d="M-200,-60Q0,-140 200,-60" stroke="#9a7a4a" stroke-width="10" fill="none" opacity=".6"/>
      ${tuft(-120, -150, 50, "#6a8a34", mk(3))}${tuft(100, -140, 40, "#6a8a34", mk(4))}</g></g>
      ${o.bushFront ? "" : War.bushHTML(o.bush ?? 520, G + 160, id + "-bush")}`);
  };
  War.bullets = (tl, L, t0, dur, o = {}) => {
    const id = nid(), r = mk(o.seed || 23), [bx, by, bw, bh] = o.box || [300, 1080, 480, 260], n = o.n ?? 8;
    let g = "";
    for (let k = 0; k < n; k++) {
      const y = by + r() * bh;
      g += `<g transform="translate(0,${f1(y)})"><g id="${id}-s${k}" opacity="0"><path d="M0,0H420" stroke="#ffcf60" stroke-width="18" stroke-linecap="round" opacity=".3"/><path d="M0,0H420" stroke="#fff8d8" stroke-width="6" stroke-linecap="round" opacity=".9"/><circle r="8" fill="#fff"/></g></g>`;
      for (let j = 0; j < 4; j++) g += `<g transform="translate(${f1(bx + r() * bw)},${f1(y)})"><g id="${id}-l${k}-${j}" opacity="0"><path d="M0,-16Q16,0 0,18Q-16,0 0,-16Z" fill="${j % 2 ? "#8ab05a" : "#4e7a34"}" ${O(1.6)}/><path d="M0,-14V16" stroke="#3a5a24" stroke-width="1.6"/></g></g>`;
    }
    put(L.glow, `<g id="${id}">${g}</g>`);
    for (let k = 0; k < n; k++) {
      const t = t0 + (k / n) * dur * 0.8 + r() * 0.1;
      tl.fromTo(`#${id}-s${k}`, { x: 1300, opacity: 1 }, { x: -500, opacity: 0.8, duration: 0.3, ease: "none", immediateRender: false }, t);
      tl.set(`#${id}-s${k}`, { opacity: 0 }, t + 0.3);
      for (let j = 0; j < 4; j++) { const a = (r() - 0.5) * Math.PI, v = 80 + r() * 160;
        tl.fromTo(`#${id}-l${k}-${j}`, { x: 0, y: 0, rotation: 0, opacity: 1 }, { x: Math.cos(a) * v - 120, y: Math.sin(a) * v + 160, rotation: 360 * (r() > 0.5 ? 1 : -1), opacity: 0, duration: 0.9, ease: "power2.out", immediateRender: false }, t + 0.06); }
    }
  };

  // ---------------- home at Songkran ----------------
  Sets.home = (L, o = {}) => {
    const id = o.id || "hm", G = 1460;
    Sets.village2(L, { id: id + "v", time: o.time || "day", house: [-200, 1.5], fg: false, ground: G - 140 });
    let s = `<g transform="translate(760,${G})"><rect x="-150" y="-180" width="300" height="20" fill="#c8402e" ${O(3)}/><rect x="-140" y="-160" width="20" height="160" fill="#8a6a4a"/><rect x="120" y="-160" width="20" height="160" fill="#8a6a4a"/>
      <rect x="-150" y="-70" width="300" height="70" fill="#e8d8b8" ${O(3)}/><text x="0" y="-26" font-family="Kanit" font-weight="900" font-size="34" fill="#c8402e" text-anchor="middle">ส้มตำ</text>
      <g transform="translate(-60,-96)"><path d="M-28,0Q-30,24 0,26Q30,24 28,0Z" fill="#8a6a4a" ${O(2.5)}/><path d="M6,-2L30,-40" stroke="#c8a87a" stroke-width="8" stroke-linecap="round"/></g></g>`;
    let flags = ""; for (let k = 0; k < 14; k++) flags += `<path d="M${-200 + k * 90},${G - 520 + Math.sin(k) * 10}l30,0l-15,34Z" fill="${["#e2483c", "#ffd23a", "#2fa864", "#2f6fd0"][k % 4]}" ${O(1.6)}/>`;
    if (o.flags !== false) s += `<path d="M-220,${G - 520}Q500,${G - 470} 1300,${G - 520}" stroke="#5a4a3a" stroke-width="3" fill="none"/>${flags}`;
    if (o.parcel) s += `<g transform="translate(${o.parcelX ?? 420},${G + 40})"><g id="${id}-parcel"><rect x="-70" y="-90" width="140" height="90" rx="6" fill="#c8a06a" ${O(3.5)}/><path d="M-70,-50H70M0,-90V0" stroke="#8a6a3a" stroke-width="6"/>
      <rect x="-50" y="-80" width="60" height="30" fill="#fdfaf2" ${O(2)}/><path d="M-44,-70h44M-44,-60h30" stroke="#8a8a8a" stroke-width="2.4"/></g></g>`;
    put(L.set, s);
  };

  // ---------------- the cast (rig2) ----------------
  const C = Rig.CAST, LINE = Rig2.LINE;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round"`;
  const helmet = (c, cs) => () => `<path d="M-58,-552C-62,-628 -22,-650 6,-648C40,-646 66,-622 60,-552Q0,-566 -58,-552Z" fill="${c}" ${ln(3)}/>
    <path d="M-66,-552Q0,-570 68,-552L70,-540Q0,-556 -68,-540Z" fill="${cs}" ${ln(2.4)}/><path d="M-36,-616Q4,-640 40,-618" stroke="#fff" stroke-width="6" fill="none" opacity=".22" stroke-linecap="round"/>
    ${[[-30, -590], [0, -604], [28, -592], [-12, -575], [16, -578]].map(([x, y]) => `<path d="M${x - 6},${y}h12" stroke="${cs}" stroke-width="3" opacity=".7"/>`).join("")}`;
  const buzz = (h) => `<path d="M-46,-552C-50,-606 -18,-626 4,-624C30,-623 53,-604 49,-552Q46,-572 40,-580Q30,-588 16,-584Q4,-592 -10,-586Q-26,-590 -38,-580Q-44,-570 -46,-552Z" fill="${h.c}" ${ln()}/>`;
  const pockets = (c) => `<path d="M-50,-440h36v30h-36zM14,-440h36v30h-36z" fill="none" stroke="${Rig2.dk(c, 0.3)}" stroke-width="2.4"/><path d="M-50,-440h36M14,-440h36" stroke="${Rig2.dk(c, 0.35)}" stroke-width="5"/>
    <path d="M-60,-332H60" stroke="#3a3428" stroke-width="12"/><rect x="-10" y="-340" width="20" height="16" rx="3" fill="#b8a878" ${ln(2)}/>`;
  const tagChain = `<path d="M-20,-492Q0,-440 20,-492" stroke="#c8ccd0" stroke-width="2.4" fill="none" stroke-dasharray="2 3"/><rect x="-8" y="-452" width="16" height="22" rx="4" fill="url(#wrTag)" ${ln(1.6)}/>`;
  const soldier = (skin, c, o = {}) => ({ skin, iris: "#2e1c12", blush: 0.4, w: o.w ?? 1, limb: 1,
    hair: { c: "#17100c", s: "#060404", sh: "#5a4a40", front: o.bare ? (x) => buzz(x.hair) : helmet(o.helmet || "#5a6a3a", o.helmetS || "#3e4a28") },
    top: { kind: "shirt", c, sleeve: "long", neck: "collar", collar: Rig2.dk(c, 0.12), button: Rig2.dk(c, 0.3), trim: Rig2.dk(c, 0.15) },
    print: pockets(c), extra: o.enemy ? "" : tagChain, face: o.face || "",
    bottom: { kind: "trousers", c: Rig2.dk(c, 0.06) }, feet: { kind: "boot", c: "#2e2a24" } });
  C.tao = { v2: soldier("#c8946a", "#6a7a46") };
  C.taoBare = { v2: soldier("#c8946a", "#6a7a46", { bare: true }) };
  C.joe = { v2: { ...soldier("#a8764a", "#6a7a46"), face: `<path d="M-30,-548q6,-3 12,0" stroke="#5a3a20" stroke-width="2" opacity=".5"/>` } };
  C.mem = { v2: { ...soldier("#8a5a3a", "#5e6e3e", { w: 1.06 }), bags: true, face: `<path d="M-30,-560l14,6" stroke="#e8c8a8" stroke-width="3" opacity=".8"/><path d="M-16,-528q16,8 32,0" stroke="#2a1a12" stroke-width="7" stroke-linecap="round"/>` } };
  C.enemy = { v2: { ...soldier("#d0a07a", "#7a8088", { enemy: true, helmet: "#6a7078", helmetS: "#4a5058" }), face: `<path d="M24,-566l12,-4" stroke="#e8c8a8" stroke-width="3" opacity=".8"/>` } };
  C.mom = { v2: { ...C.yaiTide.v2, hair: { ...C.yaiTide.v2.hair, c: "#2a221e", s: "#120e0c", sh: "#6a5a50" }, top: { kind: "blouse", c: "#f2d0a8", sleeve: "elbow", trim: "#d8b088" }, print: "", extra: "" } };

  // ---------------- cards ----------------
  const WarUI = {};
  const RULES = ["เพื่อนล้มกลางทุ่ง อย่าพุ่งเข้าไป", "พุ่มไม้บังตา ไม่บังลูกปืน"];
  WarUI.RULES = RULES;
  WarUI.tag = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), act = o.active ?? 0, done = o.done ?? [], Y = o.y ?? 620;
    const rows = RULES.map((r, k) => { const on = k === act, d = done.includes(k), yy = 30 + k * 150;
      return `<g opacity="${on || d ? 1 : 0.35}"><g transform="translate(-330,${yy - 60})">${War.coin(k ? "bush" : "norush", 0, 0, 0.95, `${id}-c${k}`)}</g>
        <text x="-200" y="${yy + 2}" font-family="Kanit" font-weight="900" font-size="40" fill="#fff" opacity=".7">${r}</text>
        <text x="-200" y="${yy}" font-family="Kanit" font-weight="900" font-size="40" fill="${on ? "#8a1a12" : "#3a4048"}">${r}</text>
        ${d ? `<g transform="translate(330,${yy - 14})"><circle id="${id}-g${k}" r="40" fill="url(#rbOkGlow)" opacity="0"/><g id="${id}-t${k}"><circle r="30" fill="#2fb864" stroke="#fff" stroke-width="5"/><path d="M-14,0l9,10l18,-20" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g></g>` : ""}</g>`; }).join("");
    put(layer, `<g id="${id}" opacity="0"><g transform="translate(540,${Y})"><g id="${id}-sw">
      <path d="M-40,-300Q0,-380 40,-300" stroke="#c8ccd0" stroke-width="5" fill="none" stroke-dasharray="3 5"/>
      <rect x="-440" y="-250" width="880" height="${330 + RULES.length * 110}" rx="70" fill="url(#wrTagE)" transform="translate(10,16)"/>
      <rect x="-440" y="-250" width="880" height="${330 + RULES.length * 110}" rx="70" fill="url(#wrTag)" ${O(5)}/>
      <circle cx="0" cy="-200" r="22" fill="#5a646e" ${O(3)}/>
      <rect x="-410" y="-220" width="820" height="40" rx="20" fill="#fff" opacity=".35"/>
      <g clip-path="url(#${id}-cl)"><rect id="${id}-sh" x="-500" y="-260" width="120" height="${360 + RULES.length * 110}" fill="#fff" opacity=".35" transform="skewX(-20)"/></g>
      <defs><clipPath id="${id}-cl"><rect x="-440" y="-250" width="880" height="${330 + RULES.length * 110}" rx="70"/></clipPath></defs>
      <text x="0" y="-130" font-family="Kanit" font-weight="900" font-size="46" fill="#2a2e34" text-anchor="middle">กฎของจ่าเม่น</text>${rows}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { y: -900, rotation: -14, transformOrigin: "50% 0%" }, { y: 0, rotation: 0, transformOrigin: "50% 0%", duration: 0.8, ease: "back.out(1.4)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-sw`, { rotation: -2.5, transformOrigin: "50% 0%" }, { rotation: 2.5, transformOrigin: "50% 0%", duration: 1.3, repeat: Math.ceil(dur / 1.3), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.8);
    tl.fromTo(`#${id}-sh`, { x: 0 }, { x: 1100, duration: 0.8, repeat: Math.ceil(dur / 2.2), repeatDelay: 1.4, ease: "power1.inOut", immediateRender: false }, t0 + 0.9);
    RULES.forEach((_, k) => { const el = document.getElementById(`${id}-c${k}`); QkUI.iconPop(tl, el, t0 + 0.3 + k * 0.15); RabFX.life(tl, el, t0 + 1.0, dur); });
    done.forEach((k) => { const t = t0 + (o.tickAt ?? 0.9); tl.fromTo(`#${id}-t${k}`, { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t);
      tl.fromTo(`#${id}-g${k}`, { scale: 0.4, opacity: 1, transformOrigin: "50% 50%" }, { scale: 2, opacity: 0, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.out", immediateRender: false }, t + 0.1); });
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };
  WarUI.cover = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), Y = o.y ?? 560;
    const panel = (x, good, label, items) => `<g transform="translate(${x},0)"><rect x="-210" y="0" width="420" height="520" rx="30" fill="${good ? "#e2f4e6" : "#fbe4e0"}" ${O(4)}/>
      <text x="0" y="66" font-family="Kanit" font-weight="900" font-size="44" fill="${good ? "#1e7a48" : "#c8282a"}" text-anchor="middle">${label}</text>
      ${items.map((t, k) => `<text x="0" y="${150 + k * 58}" font-family="Kanit" font-weight="700" font-size="38" fill="#3a3430" text-anchor="middle">${t}</text>`).join("")}
      <g transform="translate(0,410)"><g id="${id}-${good ? "ok" : "x"}"><circle r="56" fill="${good ? "#2fb864" : "#e2382e"}" stroke="#fff" stroke-width="7"/>
        ${good ? `<path d="M-26,0l16,18l34,-38" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round"/>` : `<path d="M-22,-22L22,22M22,-22L-22,22" stroke="#fff" stroke-width="12" stroke-linecap="round"/>`}</g></g></g>`;
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-in"><g transform="translate(0,${Y})"><rect x="70" y="-60" width="940" height="680" rx="40" fill="#b8a888" transform="translate(0,14)" ${O(5)}/>
      <rect x="70" y="-60" width="940" height="680" rx="40" fill="url(#rbSlabF)" ${O(5)}/>
      ${panel(315, false, "บังตา", ["พุ่มไม้", "หญ้า", "เงามืด"])}${panel(765, true, "กันกระสุน", ["ต้นไม้ใหญ่", "หิน", "คันดิน"])}
      <g id="${id}-b"><path d="M80,330H560" stroke="#ffcf60" stroke-width="14" stroke-linecap="round" opacity=".35"/><path d="M80,330H560" stroke="#fff6c8" stroke-width="6" stroke-linecap="round"/></g></g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { scaleX: 0.6, scaleY: 1.3, y: 120, svgOrigin: "540 800" }, { scaleX: 1, scaleY: 1, y: 0, svgOrigin: "540 800", duration: 0.75, ease: "elastic.out(1,0.5)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { rotation: -1, svgOrigin: "540 500" }, { rotation: 1, svgOrigin: "540 500", duration: 1.5, repeat: Math.ceil(dur / 1.5), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.75);
    tl.fromTo(`#${id}-b`, { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.2, ease: "none", immediateRender: false }, t0 + 1.0);
    tl.fromTo(`#${id}-x`, { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t0 + 1.2);
    tl.fromTo(`#${id}-x`, { x: -12 }, { x: 0, duration: 0.4, ease: "elastic.out(1.2,0.3)", immediateRender: false }, t0 + 1.55);
    RabFX.flash(tl, t0 + 1.55, "#ff2a1a", 0.22);
    tl.fromTo(`#${id}-ok`, { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t0 + 1.9);
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };

  // ---------------- war coins (same 2.5D language as RabFX.coin; registered into QkUI.ICON) ----------------
  const PAL = { norush: ["#ffe2c8", "#fff8f0", "#e0703a", "#a84a1e"], bush: ["#d8f0c8", "#f7fff2", "#6aaa52", "#44803a"], bamboo: ["#fde59a", "#fffbe8", "#e3a632", "#a8741a"],
    treex: ["#e4f2cc", "#fbfff2", "#7aa83a", "#4e7a1e"], bones: ["#ece6da", "#fffdf6", "#a8a090", "#7a7262"], weeds: ["#e4f2cc", "#fbfff2", "#8aa83a", "#5a7a1e"],
    rock: ["#dde2e6", "#f8fafc", "#8a949e", "#5a646e"], medic: ["#ffffff", "#ffffff", "#c8ccd2", "#8a949e"], binoc: ["#d6ecfb", "#f6fbff", "#3a8ad0", "#22609a"],
    parcel: ["#f2dcb8", "#fffaf0", "#c8925a", "#8a6a3a"], notouch: ["#ffe2c8", "#fff8f0", "#e0703a", "#a84a1e"], shout: ["#fde59a", "#fffbe8", "#e3a632", "#a8741a"], radio: ["#d8f0c8", "#f7fff2", "#2fa864", "#1e7a48"], still: ["#d6ecfb", "#f6fbff", "#3a8ad0", "#22609a"], dust: ["#f2e4c8", "#fffaf0", "#b8a07a", "#8a7452"] };
  let cdefs = "";
  for (const [n, [b, l, r, rd]] of Object.entries(PAL)) cdefs += `<radialGradient id="wrF-${n}" cx=".33" cy=".25" r=".9"><stop offset="0" stop-color="${l}"/><stop offset=".55" stop-color="${b}"/><stop offset="1" stop-color="${r}" stop-opacity=".55"/></radialGradient>
    <linearGradient id="wrR-${n}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${r}"/><stop offset="1" stop-color="${rd}"/></linearGradient>`;
  Sets.DEFS += cdefs;
  const X = `<g class="rbAn" data-a="xpop"><path d="M30,30L90,90M90,30L30,90" stroke="#7a140e" stroke-width="14" stroke-linecap="round" opacity=".45" transform="translate(2,3)"/><path d="M30,30L90,90M90,30L30,90" stroke="#e2382e" stroke-width="12" stroke-linecap="round"/></g>`;
  const runner = `<g transform="translate(60,64)"><circle cx="6" cy="-34" r="10" fill="#3a4048"/><path d="M4,-22L-4,4L-20,20M-4,4L12,12L14,30M2,-14L-16,-4M2,-14L20,-20" stroke="#3a4048" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`;
  const WPICT = {
    norush: () => [`<g class="rbAn" data-a="push">${runner}</g>`, `<circle cx="60" cy="60" r="40" fill="none" stroke="#7a140e" stroke-width="11" opacity=".5" transform="translate(2,3)"/><circle cx="60" cy="60" r="40" fill="none" stroke="#e2382e" stroke-width="10"/><path d="M32,32L88,88" stroke="#e2382e" stroke-width="10" stroke-linecap="round"/>`],
    bush: () => [`${[[34, 76, 26], [60, 62, 32], [86, 76, 26], [60, 88, 26]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#4e7a34" ${O(3)}/><circle cx="${x - 8}" cy="${y - 8}" r="${r * 0.4}" fill="#7aa04a" opacity=".7"/>`).join("")}`,
      `<g class="rbAn" data-a="push"><path d="M6,64H112" stroke="#fff6c8" stroke-width="7" stroke-linecap="round"/><path d="M92,64H112" stroke="#ffb030" stroke-width="7" stroke-linecap="round"/></g>`],
    bamboo: () => [`<path d="M8,100Q60,92 112,100V120H8Z" fill="#a8b46a"/>`, `<g class="rbAn" data-a="bob"><path d="M30,100L88,24M90,100L32,24" stroke="#c8a85a" stroke-width="14" stroke-linecap="round"/><path d="M30,100L88,24M90,100L32,24" stroke="${INK}" stroke-width="2.4"/>
      <path d="M44,80h12M64,80h12M52,50h8M60,50h8" stroke="#8a6a2a" stroke-width="3"/></g>`],
    treex: () => [`<path d="M40,120C38,80 44,40 50,10H72C78,40 82,80 80,120Z" fill="#7a5a3a" ${O(3)}/>`, `<g class="rbAn" data-a="xpop"><path d="M48,46L72,70M72,46L48,70" stroke="#f4e8c8" stroke-width="9" stroke-linecap="round"/><path d="M48,46L72,70M72,46L48,70" stroke="#5a3a20" stroke-width="2"/></g>`],
    bones: () => [`<path d="M8,96Q60,88 112,96V120H8Z" fill="#a8b46a"/>`, `<g class="rbAn" data-a="bob"><g transform="rotate(-24 60 66)"><rect x="28" y="60" width="64" height="12" rx="6" fill="#f4eee0" ${O(3)}/>${[[28, 60], [28, 72], [92, 60], [92, 72]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="8" fill="#f4eee0" ${O(3)}/>`).join("")}</g>
      <g transform="rotate(30 62 80)"><rect x="40" y="76" width="44" height="9" rx="4.5" fill="#e8e0cc" ${O(2.5)}/></g></g>`],
    weeds: () => [`${Array.from({ length: 11 }, (_, k) => `<path d="M${10 + k * 10},120Q${14 + k * 10},${70 - (k % 3) * 12} ${6 + k * 10 + (k % 2) * 10},${40 - (k % 4) * 8}" stroke="${k % 2 ? "#5a7a2a" : "#8aa04a"}" stroke-width="6" fill="none" stroke-linecap="round"/>`).join("")}`, `<g class="rbAn" data-a="peek"><path d="M78,96L92,82M92,96L78,82" stroke="#e2382e" stroke-width="5" stroke-linecap="round"/></g>`],
    rock: () => [`<path d="M14,104Q20,52 54,40Q94,34 106,80Q110,100 100,108Z" fill="#9aa2aa" ${O(3.5)}/><path d="M34,62Q54,48 76,52" stroke="#c8d0d6" stroke-width="6" fill="none" stroke-linecap="round"/>`,
      `<g class="rbAn" data-a="bob"><circle cx="86" cy="34" r="16" fill="#2fb864" stroke="#fff" stroke-width="4"/><path d="M78,34l6,6l10,-12" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g>`],
    medic: () => ["", `<g class="rbAn" data-a="xpop"><path d="M48,24H72V48H96V72H72V96H48V72H24V48H48Z" fill="#e2382e" ${O(3.5)}/></g>`],
    binoc: () => ["", `<g class="rbAn" data-a="peek"><circle cx="40" cy="70" r="22" fill="#3a4048" ${O(3.5)}/><circle cx="80" cy="70" r="22" fill="#3a4048" ${O(3.5)}/><rect x="44" y="40" width="32" height="26" rx="6" fill="#4a525a" ${O(3)}/>
      <circle cx="40" cy="70" r="13" fill="#8ac8f0"/><circle cx="80" cy="70" r="13" fill="#8ac8f0"/><circle cx="35" cy="65" r="5" fill="#fff"/><circle cx="75" cy="65" r="5" fill="#fff"/></g>`],
    parcel: () => ["", `<g class="rbAn" data-a="bob"><path d="M22,48L60,30L98,48V92L60,110L22,92Z" fill="#c8a06a" ${O(3.5)}/><path d="M22,48L60,66L98,48M60,66V110" stroke="${INK}" stroke-width="3" fill="none"/><path d="M41,39L79,57V70" stroke="#8a6a3a" stroke-width="7" fill="none"/></g>`],
    still: () => [`<path d="M8,96Q60,86 112,96V120H8Z" fill="#a8b46a"/><g transform="translate(60,88)"><circle cx="-30" cy="-6" r="10" fill="#3a4048"/><path d="M-20,-4H26" stroke="#3a4048" stroke-width="11" stroke-linecap="round"/></g>`,
      `<g class="rbAn" data-a="bob"><path d="M44,62V30Q44,24 50,24Q56,24 56,30V20Q56,14 62,14Q68,14 68,20V26Q68,20 74,20Q80,20 80,26V58Q80,72 66,74H54Q44,72 44,62Z" fill="#f2c8a0" ${O(3)}/></g>`],
    notouch: () => [`<g class="rbAn" data-a="push"><path d="M40,96V58Q40,50 47,50Q54,50 54,58V40Q54,32 61,32Q68,32 68,40V50Q68,44 75,44Q82,44 82,52V86Q82,100 66,102H54Q40,100 40,96Z" fill="#f2c8a0" ${O(3)}/></g>`, `<circle cx="60" cy="60" r="40" fill="none" stroke="#7a140e" stroke-width="11" opacity=".5" transform="translate(2,3)"/><circle cx="60" cy="60" r="40" fill="none" stroke="#e2382e" stroke-width="10"/><path d="M32,32L88,88" stroke="#e2382e" stroke-width="10" stroke-linecap="round"/>`],
    shout: () => [`<circle cx="44" cy="62" r="24" fill="#c8946a" ${O(3)}/><path d="M50,72q8,4 12,-2" stroke="${INK}" stroke-width="3" fill="none"/><path d="M22,48Q30,34 46,38Q40,30 26,38Z" fill="#5a6a3a" ${O(2)}/>`, `<g class="rbAn" data-a="bob"><path d="M74,46Q86,60 74,76M84,38Q102,60 84,84M94,30Q118,60 94,92" stroke="#e2382e" stroke-width="6" fill="none" stroke-linecap="round"/></g>`],
    radio: () => ["", `<g class="rbAn" data-a="bob"><rect x="40" y="36" width="40" height="66" rx="8" fill="#3a4048" ${O(3.5)}/><path d="M70,36V12" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><rect x="47" y="46" width="26" height="18" rx="3" fill="#8ad0a0"/><circle cx="52" cy="80" r="4" fill="#c8ccd2"/><circle cx="68" cy="80" r="4" fill="#c8ccd2"/><circle cx="60" cy="92" r="4" fill="#c8ccd2"/></g>
      <g class="rbAn" data-a="peek"><path d="M84,20q10,8 0,18M92,14q16,14 0,30" stroke="#2fa864" stroke-width="4" fill="none" stroke-linecap="round"/></g>`],
    dust: () => [`<path d="M8,104Q60,96 112,104V120H8Z" fill="#a8b46a"/>`, `<g class="rbAn" data-a="push">${[[60, 86, 18], [52, 62, 20], [66, 40, 22], [56, 18, 18]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#d8c8a8" ${O(2.5)}/>`).join("")}</g>`],
  };
  const wcoin = (name) => { const [inside, top] = WPICT[name]();
    return `<ellipse class="quSh" cx="60" cy="120" rx="50" ry="9" fill="url(#quCoinSh)"/><g class="quBob"><g class="quSq">
      <circle cx="60" cy="67" r="52" fill="url(#wrR-${name})" ${O(4)}/><path d="M12,67A48,48 0 0 0 108,67" stroke="#000" stroke-width="3" fill="none" opacity=".18"/>
      <circle cx="60" cy="57" r="52" fill="url(#wrF-${name})" ${O(4)}/><circle cx="60" cy="57" r="45.5" fill="none" stroke="url(#quBev)" stroke-width="4"/>
      <g transform="translate(60,57) scale(.9) translate(-60,-60)">${inside ? `<g clip-path="url(#quPicClip)">${inside}</g>` : ""}${top}</g>
      <path d="M21,46A41,41 0 0 1 45,19" stroke="#fff" stroke-width="5.5" fill="none" opacity=".72" stroke-linecap="round"/><circle cx="53.5" cy="15.5" r="2.8" fill="#fff" opacity=".7"/></g></g>`; };
  Object.keys(WPICT).forEach((n) => (QkUI.ICON[n] = () => wcoin(n)));
  War.coin = (name, x, y, s = 1, id = "") => !WPICT[name] ? RabFX.coin(name, x, y, s, id) : `<g transform="translate(${x},${y}) scale(${s})"><g ${id ? `id="${id}"` : ""}>${wcoin(name)}</g></g>`;
  // the binocular glint on the far ridge: a slow twinkle with a star flare (F6 clue) — animate the inner group
  War.glint = (tl, id, t0, dur, o = {}) => { const sel = `#${id}-glint-in`, P = o.period ?? 1.6;
    tl.fromTo(sel, { scale: 0.55, opacity: 0.55, rotation: 0, transformOrigin: "50% 50%" }, { scale: 1.25, opacity: 1, rotation: 45, transformOrigin: "50% 50%", duration: P / 2, repeat: Math.ceil(dur / (P / 2)), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0); };
  // poses for the war cast
  Rig.MODES.reachUp = (u, o) => { const s = Math.sin(u * 7); return { ...Rig.MODES.lie(u, o), uaF: -150 + 10 * s, faF: -20 + 8 * s, head: -10 + 3 * s }; };
  Rig.MODES.stop = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.6); return { ...Rig.MODES.idle(u, o), uaF: -92 + b, faF: -84, torso: -2, head: -2 }; };
  Rig.MODES.hold = (u, o) => { const s = Math.sin(u * 13); return { ...Rig.MODES.idle(u, o), uaF: -70 + 5 * s, faF: -30, uaB: -60 - 5 * s, faB: -40, torso: -14, head: 4, thF: -14, shF: 18, thB: 18, bodyY: 10 }; };
  Rig.MODES.strain = (u, o) => { const s = Math.sin(u * 15); return { ...Rig.MODES.idle(u, o), uaF: -96 + 6 * s, faF: -10, uaB: -80 - 6 * s, faB: -8, torso: 16 + 2 * s, head: 6, thF: 22, shF: 26, thB: -20, shB: 10, bodyY: 14 }; };
  Rig.MODES.prone = (u, o) => { const s = Math.sin(u * 2 * Math.PI / 1.4); return { ...Rig.MODES.lie(u, o), uaF: -170 + 14 * s, faF: -30, uaB: -150 - 14 * s, faB: -30, thF: 6 * s, thB: -6 * s, head: -40 }; };
  Rig.MODES.kneel = (u, o) => { const b = Math.sin(u * 2 * Math.PI / 2.8); return { ...Rig.MODES.crouch(u, o), uaF: -60 + 3 * b, faF: -40, torso: 18, head: 8 }; };
  // the warning-signs card: four coins in a 2×2 grid that pop in turn and keep moving
  WarUI.signs = (tl, layer, t0, dur, o = {}) => {
    const id = nid(), Y = o.y ?? 560, items = o.items || [["bamboo", "ไม้ไขว้"], ["treex", "รอยกากบาทบนต้นไม้"], ["bones", "ซากสัตว์"], ["weeds", "ทุ่งรกไม่มีคนเดิน"]];
    put(layer, `<g id="${id}" opacity="0"><g id="${id}-in"><g transform="translate(0,${Y})"><rect x="70" y="-40" width="940" height="${o.h ?? 760}" rx="40" fill="#b8a888" transform="translate(0,14)" ${O(5)}/><rect x="70" y="-40" width="940" height="${o.h ?? 760}" rx="40" fill="url(#rbSlabF)" ${O(5)}/>
      ${o.title ? `<text x="540" y="40" font-family="Kanit" font-weight="900" font-size="48" fill="#7a140e" text-anchor="middle">${o.title}</text>` : ""}
      ${items.map(([c, t], k) => { const x = 300 + (k % 2) * 480, y = 90 + Math.floor(k / 2) * 330; return `<g transform="translate(${x - 90},${y})">${War.coin(c, 0, 0, 1.5, `${id}-c${k}`)}</g><text x="${x}" y="${y + 268}" font-family="Kanit" font-weight="800" font-size="38" fill="#3a3430" text-anchor="middle">${t}</text>`; }).join("")}</g></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0);
    tl.fromTo(`#${id}`, { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { scaleX: 0.6, scaleY: 1.3, y: 120, svgOrigin: "540 900" }, { scaleX: 1, scaleY: 1, y: 0, svgOrigin: "540 900", duration: 0.75, ease: "elastic.out(1,0.5)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-in`, { rotation: -0.8, svgOrigin: "540 900" }, { rotation: 0.8, svgOrigin: "540 900", duration: 1.6, repeat: Math.ceil(dur / 1.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.75);
    items.forEach((_, k) => { const el = document.getElementById(`${id}-c${k}`); QkUI.iconPop(tl, el, t0 + 0.35 + k * (o.step ?? 0.3)); RabFX.life(tl, el, t0 + 1.0, dur); });
    if (o.out !== false) tl.to(`#${id}`, { opacity: 0, duration: 0.25 }, t0 + dur - 0.25);
  };
  window.War = War; window.WarUI = WarUI;
})();
