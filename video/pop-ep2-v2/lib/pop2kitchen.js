// "เห็ดปอบ" v2 — the kitchen under the stilt house at night.
//   Sets.kitchen2(L, o)  o.time "evening" (lamp lit, fire up) | "late" (2 a.m.: embers, lamp out, moonlight)
//                        o.stove x (the clay stove and the curry pot) · o.platform x (the bamboo bench with bowls and the rice basket)
//                        o.pot false · o.lid "on" | "off" · o.seed
//                        ids: #id-fire (flames, flickered by Pop2.flicker), #id-coals, #id-pot, #id-lid, #id-lamp, #id-fireglow
//   Pop2.flicker(tl, id, t0, dur, o)  deterministic fire flicker on #id (flames) and its glow (#id + "glow")
//   Pop2.stove2(x, y, s, o) · Pop2.pot2(x, y, s, o) props, origin at the foot
(function () {
  const { mk, f1, put, blob } = Pop2;
  const LN = "#2a1e1a";

  Sets.DEFS += `
    <linearGradient id="kiSkyE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1428"/><stop offset=".7" stop-color="#2a3450"/><stop offset="1" stop-color="#4a4a5a"/></linearGradient>
    <linearGradient id="kiSkyL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04060c"/><stop offset=".7" stop-color="#101a2e"/><stop offset="1" stop-color="#1c2840"/></linearGradient>
    <linearGradient id="kiFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2a22"/><stop offset="1" stop-color="#1a120e"/></linearGradient>
    <linearGradient id="kiPost" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a5038"/><stop offset=".35" stop-color="#5a3a28"/><stop offset="1" stop-color="#22160e"/></linearGradient>
    <linearGradient id="kiPostL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#24180f"/><stop offset=".6" stop-color="#5a3a28"/><stop offset="1" stop-color="#a8683e"/></linearGradient>
    <linearGradient id="kiBoard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1c14"/><stop offset="1" stop-color="#4a3022"/></linearGradient>
    <linearGradient id="kiClay" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e09a62"/><stop offset=".5" stop-color="#b0683c"/><stop offset="1" stop-color="#5a2e18"/></linearGradient>
    <linearGradient id="kiPot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e8e4dc"/><stop offset=".25" stop-color="#b8b4ae"/><stop offset=".7" stop-color="#6a6660"/><stop offset="1" stop-color="#2e2c2a"/></linearGradient>
    <linearGradient id="kiSoot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1614" stop-opacity="0"/><stop offset="1" stop-color="#0c0a08" stop-opacity=".95"/></linearGradient>
    <radialGradient id="kiFireGlow"><stop offset="0" stop-color="#ffd27a" stop-opacity=".85"/><stop offset=".3" stop-color="#ff9a3a" stop-opacity=".38"/><stop offset=".7" stop-color="#ff6a1a" stop-opacity=".1"/><stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/></radialGradient>
    <radialGradient id="kiLampGlow"><stop offset="0" stop-color="#fff0c0" stop-opacity=".9"/><stop offset=".25" stop-color="#ffc870" stop-opacity=".35"/><stop offset="1" stop-color="#ffb050" stop-opacity="0"/></radialGradient>
    <radialGradient id="kiCoal"><stop offset="0" stop-color="#fff2b0"/><stop offset=".4" stop-color="#ff8a2a"/><stop offset="1" stop-color="#8a1a08"/></radialGradient>
    <radialGradient id="kiMoon"><stop offset="0" stop-color="#e8f0ff" stop-opacity=".9"/><stop offset=".15" stop-color="#a8c0e8" stop-opacity=".35"/><stop offset="1" stop-color="#6a88c0" stop-opacity="0"/></radialGradient>
    <linearGradient id="kiLeak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd890" stop-opacity=".55"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></linearGradient>`;

  // a hewn post: square-ish, lit on one side by the fire, with grain and a notch
  function post(x, top, base, w, litLeft, r) {
    let g = `<rect x="${f1(x - w / 2)}" y="${f1(top)}" width="${f1(w)}" height="${f1(base - top)}" fill="url(#${litLeft ? "kiPost" : "kiPostL"})"/>`;
    for (let k = 0; k < 4; k++) { const gx = x - w / 2 + w * (0.2 + k * 0.2) + (r() - 0.5) * 6; g += `<path d="M${f1(gx)},${f1(top)}Q${f1(gx + (r() - 0.5) * 10)},${f1((top + base) / 2)} ${f1(gx)},${f1(base)}" stroke="#1a0e08" stroke-width="2" fill="none" opacity=".35"/>`; }
    g += `<ellipse cx="${f1(x)}" cy="${f1(base)}" rx="${f1(w * 1.1)}" ry="${f1(w * 0.18)}" fill="#000" opacity=".45"/>`;
    return g;
  }
  function stove2(x, y, s, o = {}) {
    const id = o.id || "st";
    let g = `<ellipse cx="0" cy="4" rx="150" ry="22" fill="#000" opacity=".5"/>`;
    // the bucket of the อั้งโล่: clay inside a tin band, the draught mouth glowing at the front
    g += `<path d="M-110,-10L-124,-170Q0,-190 124,-170L110,-10Q0,8 -110,-10Z" fill="url(#kiClay)" stroke="${LN}" stroke-width="3"/>`;
    g += `<path d="M-120,-150Q0,-168 120,-150L118,-128Q0,-146 -118,-128Z" fill="#6a6a66" stroke="${LN}" stroke-width="2.4"/><path d="M-116,-40Q0,-24 116,-40L114,-22Q0,-6 -114,-22Z" fill="#6a6a66" stroke="${LN}" stroke-width="2.4"/>`;
    g += `<path d="M-46,-26L-40,-96Q0,-104 40,-96L46,-26Z" fill="#1a0a04" stroke="${LN}" stroke-width="2.4"/><g id="${id}-coals">${[[-24, -44, 14], [6, -40, 16], [28, -50, 12], [-6, -62, 12], [16, -70, 10]].map(([cx, cy, R]) => `<circle cx="${cx}" cy="${cy}" r="${R}" fill="url(#kiCoal)"/>`).join("")}</g>`;
    g += `<path d="M-124,-170Q0,-190 124,-170Q0,-150 -124,-170Z" fill="#2a1408"/>`;
    // the flames licking up round the pot
    return `<g ${o.gid ? `id="${o.gid}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`;
  }
  // flames licking up round the pot's foot from the stove's rim (drawn over the pot)
  function flames(x, y, s, id) {
    const F = [[-118, 56, -14], [-96, 80, -8], [-70, 46, -4], [74, 50, 4], [100, 78, 8], [120, 52, 14]];
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g id="${id}-fire" style="mix-blend-mode:screen">${F.map(([fx, fh, lean]) => `<path d="M${fx - 16},-168Q${fx - 18},${-168 - fh * 0.6} ${fx + lean},${-168 - fh}Q${fx + 20},${-168 - fh * 0.5} ${fx + 16},-168Z" fill="#ffa030" opacity=".9"/><path d="M${fx - 7},-168Q${fx - 7},${-168 - fh * 0.4} ${fx + lean * 0.6},${-168 - fh * 0.62}Q${fx + 9},${-168 - fh * 0.3} ${fx + 7},-168Z" fill="#fff2a8"/>`).join("")}
      <ellipse cx="0" cy="-170" rx="130" ry="16" fill="#ff8a2a" opacity=".55"/></g></g>`;
  }
  function pot2(x, y, s, o = {}) {
    const id = o.id || "pt";
    let g = `<path d="M-150,0C-170,-60 -164,-150 -140,-190H140C164,-150 170,-60 150,0Q0,22 -150,0Z" fill="url(#kiPot)" stroke="${LN}" stroke-width="3"/>
      <path d="M-150,0C-170,-60 -164,-150 -140,-190H140C164,-150 170,-60 150,0Q0,22 -150,0Z" fill="url(#kiSoot)"/>
      <path d="M-150,-190H150V-206H-150Z" fill="#c8c4bc" stroke="${LN}" stroke-width="3"/><path d="M-150,-190H150" stroke="#fff" stroke-width="3" opacity=".5"/>
      <path d="M-196,-170h46v14h-46zM150,-170h46v14h-46z" fill="#3a3632" stroke="${LN}" stroke-width="2.4"/>
      <path d="M-120,-170Q-130,-90 -120,-30" stroke="#fff" stroke-width="10" fill="none" opacity=".35" stroke-linecap="round"/>
      <path d="M-60,-110q10,6 20,0M30,-60q12,6 24,0M90,-140q8,5 16,0" stroke="#3a3632" stroke-width="3" fill="none" opacity=".5"/>`;
    if (o.lid !== "off") g += `<g id="${id}-lid" transform="rotate(${o.lid === "ajar" ? -8 : 0} 140 -206)"><path d="M-160,-206Q0,-280 160,-206Z" fill="url(#kiPot)" stroke="${LN}" stroke-width="3"/><path d="M-20,-246h40v-14h-40z" fill="#2a2622" stroke="${LN}" stroke-width="2.4"/><path d="M-120,-216Q-60,-250 0,-252" stroke="#fff" stroke-width="5" fill="none" opacity=".4"/></g>`;
    else g += `<ellipse cx="0" cy="-206" rx="146" ry="20" fill="#5a3a12"/><ellipse cx="0" cy="-208" rx="138" ry="15" fill="#8a5a1e"/>${[[-60, -208], [20, -206], [80, -210], [-10, -212]].map(([mx, my]) => `<ellipse cx="${mx}" cy="${my}" rx="22" ry="7" fill="#f2e6d0" opacity=".9"/>`).join("")}`;
    return `<g ${o.gid ? `id="${o.gid}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${s * 1.12},${s * 0.74})">${g}</g>`;
  }
  // the bamboo bench (แคร่) with bowls, the sticky-rice basket (กระติ๊บ) and a lamp-lit tray
  function platform(x, y, s, r) {
    let g = `<ellipse cx="0" cy="6" rx="330" ry="30" fill="#000" opacity=".45"/>`;
    [-290, -100, 100, 290].forEach((lx) => { g += `<rect x="${lx - 9}" y="-130" width="18" height="130" fill="#6a4a2a" stroke="${LN}" stroke-width="2"/>`; });
    g += `<path d="M-320,-130H320V-150H-320Z" fill="#8a6a3a" stroke="${LN}" stroke-width="2.4"/>`;
    for (let k = 0; k < 16; k++) g += `<path d="M${-316 + k * 40},-150V-130" stroke="#5a4020" stroke-width="2.4"/>`;
    g += `<path d="M-320,-150H320" stroke="#e8c890" stroke-width="2" opacity=".5"/>`;
    // bowls, the rice basket, a mortar
    g += `<path d="M-250,-150Q-250,-190 -190,-192Q-130,-190 -130,-150Z" fill="#e8e2d6" stroke="${LN}" stroke-width="2.4"/><path d="M-246,-170h112" stroke="#3a6a9a" stroke-width="4"/>`;
    g += `<path d="M-110,-150Q-110,-180 -66,-182Q-22,-180 -22,-150Z" fill="#e8e2d6" stroke="${LN}" stroke-width="2.4"/><path d="M-106,-166h80" stroke="#3a6a9a" stroke-width="4"/>`;
    g += `<g transform="translate(110,-150)"><path d="M-46,0L-56,-120Q0,-134 56,-120L46,0Z" fill="#c8a066" stroke="${LN}" stroke-width="2.4"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-54,${-110 + k * 22}Q0,${-104 + k * 22} 54,${-110 + k * 22}" stroke="#8a6a3a" stroke-width="2.4" fill="none"/>`).join("")}<path d="M-60,-120Q0,-160 60,-120Q0,-130 -60,-120Z" fill="#b08a52" stroke="${LN}" stroke-width="2.4"/><path d="M-40,-60Q-80,-120 -30,-150" stroke="#5a3a1a" stroke-width="4" fill="none"/></g>`;
    g += `<g transform="translate(250,-150)"><path d="M-50,0L-40,-80H40L50,0Z" fill="#7a5a3e" stroke="${LN}" stroke-width="2.4"/><ellipse cx="0" cy="-80" rx="40" ry="10" fill="#3a2a1e"/><path d="M10,-80L40,-150" stroke="#9a7a52" stroke-width="12" stroke-linecap="round"/></g>`;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g>`;
  }

  function kitchen2(L, o = {}) {
    const id = o.id || "ki", r = mk(o.seed || 55), G = o.ground ?? 1500, late = o.time === "late", SX = o.stove ?? 540;
    // sky: the night yard between the posts
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#${late ? "kiSkyL" : "kiSkyE"})"/><circle cx="${o.moonX ?? 900}" cy="${o.moonY ?? 420}" r="380" fill="url(#kiMoon)"/><circle cx="${o.moonX ?? 900}" cy="${o.moonY ?? 420}" r="34" fill="#f4f6ff"/>`;
    for (let k = 0; k < 50; k++) sky += `<circle cx="${f1(-900 + r() * 2900)}" cy="${f1(-600 + r() * 1300)}" r="${f1(1 + r() * 1.6)}" fill="#e8ecff" opacity="${f1(0.2 + r() * 0.5)}"/>`;
    put(L.sky, sky);
    // far: the yard, a neighbour's house with one lit window, trees
    let far = `<rect x="-1300" y="${G - 300}" width="3700" height="600" fill="#0c1018"/>`;
    for (let k = 0; k < 9; k++) far += `<path d="${blob(-1000 + k * 380 + r() * 100, G - 380 - r() * 120, 140 + r() * 80, r, 9)}" fill="#0a0e14"/>`;
    far += `<g transform="translate(${o.neighbour ?? 1480},${G - 300})"><path d="M-160,0V-180H160V0ZM-200,-180L0,-300L200,-180Z" fill="#0e121a"/>${late ? "" : `<rect x="-40" y="-140" width="60" height="50" fill="#ffc870" opacity=".85"/><rect x="-40" y="-140" width="60" height="50" fill="url(#kiLampGlow)" transform="scale(2.4)" transform-origin="-10 -115" opacity=".4"/>`}</g>`;
    for (let k = 0; k < 7; k++) far += post(-900 + k * 420, -400, G - 260, 26, true, r);
    put(L.far, far);
    // mid: the back screen of woven bamboo, a shelf with jars, the water jar, things hanging
    let mid = `<g transform="translate(${o.wall ?? 1060},0)"><rect x="-260" y="200" width="620" height="${G - 120 - 200}" fill="#3a2c1e"/>`;
    for (let k = 0; k < 30; k++) mid += `<path d="M-260,${220 + k * 40}h620" stroke="#2a1e14" stroke-width="10" opacity=".7"/>`;
    for (let k = 0; k < 16; k++) mid += `<path d="M${-260 + k * 40},200v${G - 320}" stroke="#4a3624" stroke-width="6" opacity=".5"/>`;
    mid += `<rect x="-200" y="620" width="300" height="16" fill="#5a4028"/>${[-170, -110, -50, 10, 60].map((jx, k) => `<path d="M${jx - 18},620q-6,-50 18,-60q24,10 18,60z" fill="${["#6a4a3a", "#8a7a5a", "#5a5a4a", "#7a5a3a", "#9a8a6a"][k]}" stroke="${LN}" stroke-width="2"/>`).join("")}`;
    mid += `<path d="M-120,300V420M-90,300V400M-60,300V430" stroke="#5a4028" stroke-width="2"/><path d="${blob(-120, 440, 20, r, 6)}" fill="#e8e0d0"/><path d="${blob(-90, 414, 16, r, 6)}" fill="#e8e0d0"/><path d="M-66,430q6,30 0,50M-54,430q-6,30 0,46" stroke="#c83a2a" stroke-width="7" stroke-linecap="round"/></g>`;
    mid += `<g transform="translate(${o.jar ?? 1260},${G - 110})"><ellipse cx="0" cy="4" rx="140" ry="20" fill="#000" opacity=".5"/><path d="M-90,0C-150,-60 -150,-200 -80,-250H80C150,-200 150,-60 90,0Z" fill="#5a3a24" stroke="${LN}" stroke-width="3"/><path d="M-84,-250H84V-266H-84Z" fill="#4a2e1c" stroke="${LN}" stroke-width="2.4"/><path d="M-110,-170Q0,-150 110,-170M-120,-110Q0,-90 120,-110" stroke="#c8a040" stroke-width="5" fill="none" opacity=".6"/><path d="M-100,-200Q-120,-120 -90,-40" stroke="#fff" stroke-width="10" fill="none" opacity=".12"/></g>`;
    put(L.mid, mid);
    // set: the floor, the overhead floor of the house with light leaking between boards, posts, the stove and pot, the bench
    let s = `<rect x="-1300" y="${G - 140}" width="3700" height="1600" fill="url(#kiFloor)"/>`;
    for (let k = 0; k < 40; k++) s += `<ellipse cx="${f1(-1100 + r() * 3300)}" cy="${f1(G - 100 + r() * 600)}" rx="${f1(30 + r() * 90)}" ry="${f1(6 + r() * 14)}" fill="${r() < 0.5 ? "#000" : "#5a4030"}" opacity=".18"/>`;
    // overhead: joists and boards
    s += `<rect x="-1300" y="-900" width="3700" height="1080" fill="url(#kiBoard)"/>`;
    for (let k = 0; k < 40; k++) s += `<path d="M${-1300 + k * 95},-900V180" stroke="#140c08" stroke-width="3" opacity=".7"/>`;
    for (let k = 0; k < 6; k++) s += `<rect x="-1300" y="${60 + k * 22}" width="3700" height="14" fill="#2a1a10"/>`;
    s += `<rect x="-1300" y="160" width="3700" height="40" fill="#3a2618" stroke="${LN}" stroke-width="2"/><path d="M-1300,162H2400" stroke="#ffb870" stroke-width="2" opacity=".3"/>`;
    // posts in front of the back wall
    [[-260, 66], [1440, 70], [180, 40], [880, 44]].forEach(([px, w], k) => { s += post(px, 160, G + (k < 2 ? 60 : -40), w, px < SX, r); });
    if (o.platform !== false) s += platform(o.platform ?? 120, G + 40, 1, r);
    if (o.firewood !== false) { let fw = ""; for (let k = 0; k < 7; k++) fw += `<rect x="${-80 + (k % 4) * 40 + (k > 3 ? 20 : 0)}" y="${k > 3 ? -70 : -36}" width="38" height="200" rx="12" transform="rotate(84 ${-60 + (k % 4) * 40} ${k > 3 ? -70 : -36})" fill="#6a4a2e" stroke="${LN}" stroke-width="2"/><circle cx="${-60 + (k % 4) * 40 + (k > 3 ? 20 : 0)}" cy="${k > 3 ? -52 : -18}" r="16" fill="#c89a62" stroke="${LN}" stroke-width="2"/>`; s += `<g transform="translate(${o.firewood ?? 860},${G + 60})">${fw}</g>`; }
    s += stove2(SX, G + 100, 1, { id, gid: `${id}-stove` });
    if (o.pot !== false) s += pot2(SX, G + 100 - 170, 0.82, { id, lid: o.lid, gid: `${id}-pot` });
    if (o.fire ?? !late) s += flames(SX, G + 100, 1, id);
    put(L.set, s);
    // glow: firelight on the floor and the posts, the hanging lamp, leaks of lamplight from the room above
    let gl = `<circle id="${id}-fireglow" cx="${SX}" cy="${G - 20}" r="${late ? 520 : 760}" fill="url(#kiFireGlow)" opacity="${late ? 0.55 : 0.9}" style="mix-blend-mode:screen"/>`;
    if (!late) {
      for (let k = 0; k < 9; k++) { const lx = -600 + k * 260 + r() * 60; gl += `<path d="M${f1(lx)},180L${f1(lx + 8)},180L${f1(lx + 180)},${G}L${f1(lx + 120)},${G}Z" fill="url(#kiLeak)" opacity="${f1(0.25 + r() * 0.3)}" style="mix-blend-mode:screen"/>`; }
      const LX = o.lamp ?? 260;
      gl += `<g id="${id}-lamp"><path d="M${LX},180V420" stroke="#1a120c" stroke-width="3"/><path d="M${LX - 26},430h52l-8,70h-36z" fill="#3a3a36" stroke="${LN}" stroke-width="2.4"/><ellipse cx="${LX}" cy="452" rx="16" ry="22" fill="#fff4c8"/><circle cx="${LX}" cy="460" r="520" fill="url(#kiLampGlow)" opacity=".75" style="mix-blend-mode:screen"/></g>`;
    }
    put(L.glow, gl);
    // fg: a near post and a fish trap hanging in the corner
    put(L.fg, post(o.fgPost ?? -40, -900, 2600, 150, false, r) + `<g transform="translate(1000,120)" opacity=".95"><path d="M0,0V120" stroke="#1a120c" stroke-width="4"/><path d="M-60,120Q-80,300 0,380Q80,300 60,120Z" fill="#3a2a1a"/>${[0, 1, 2, 3, 4].map((k) => `<path d="M-64,${150 + k * 46}Q0,${160 + k * 46} 64,${150 + k * 46}" stroke="#5a4028" stroke-width="5" fill="none"/>`).join("")}</g>`);
  }

  // fire flicker: deterministic jitter of the flames' scale and the glow's opacity
  function flicker(tl, id, t0, dur, o = {}) {
    const fire = document.getElementById(`${id}-fire`), glow = document.getElementById(`${id}-fireglow`), c = { t: 0 }, base = glow ? +glow.getAttribute("opacity") : 1;
    const go = (t) => { const n = 0.5 * Math.sin(t * 17.3) + 0.3 * Math.sin(t * 29.1 + 1.3) + 0.2 * Math.sin(t * 7.7 + 2.1);
      if (fire) fire.setAttribute("transform", `translate(0,${f1(-168 * n * 0.06)}) scale(1,${(1 + n * 0.06).toFixed(3)})`);
      if (glow) glow.setAttribute("opacity", (base * (0.85 + 0.15 * n)).toFixed(3)); };
    go(0);
    tl.to(c, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => go(c.t) }, t0);
  }

  Object.assign(Sets, { kitchen2 });
  Object.assign(Pop2, { flicker, stove2, pot2, post });
})();
