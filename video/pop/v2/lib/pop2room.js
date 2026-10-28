// "เห็ดปอบ" v2 — the room upstairs at night, the view down through the floor gap, and the ปอบ itself.
//   Sets.bedroom2(L, o)  plank walls with moonlight through the gaps, a shuttered window (o.window x), the floor in perspective with its
//                        gaps, a mattress under a mosquito net (o.bed x; the net's front panel goes in L.glow so it sits over the actor)
//                        o.phone (a phone glowing on the pillow) · ids: #id-net, #id-moon, #id-phone
//   Sets.gap2(L, o)      top-down POV through a crack in the floorboards: the boards fill the frame, the slit shows the kitchen below
//                        lit by embers: the pot and the ปอบ crouched beside it (#id-pob, its eyes #id-eyes), o.pob false = empty
//   Pop2.ghost2(x, y, s, o)  the ปอบ: coal-black, thin, hunched, long hair, long fingers, green eyes; o.pose "eat" | "peer" | "stand"
//                            ids from o.id: #id-eyes, #id-head
(function () {
  const { mk, f1, put, blob } = Pop2;
  const BL = "#0a0c0b", BL2 = "#151a17", RIM = "#2c3a32";

  Sets.DEFS += `
    <linearGradient id="brWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1820"/><stop offset="1" stop-color="#2a2430"/></linearGradient>
    <linearGradient id="brFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2228"/><stop offset="1" stop-color="#4a3a36"/></linearGradient>
    <linearGradient id="brBeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a8c4ff" stop-opacity="0"/><stop offset=".5" stop-color="#a8c4ff" stop-opacity=".22"/><stop offset="1" stop-color="#a8c4ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="brNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1226"/><stop offset="1" stop-color="#2a3a5a"/></linearGradient>
    <radialGradient id="brPhone"><stop offset="0" stop-color="#cfe4ff" stop-opacity=".8"/><stop offset=".3" stop-color="#8ab4ff" stop-opacity=".25"/><stop offset="1" stop-color="#8ab4ff" stop-opacity="0"/></radialGradient>
    <pattern id="brMesh" width="9" height="9" patternUnits="userSpaceOnUse"><path d="M0,0H9M0,0V9" stroke="#dfe8f4" stroke-width="1" opacity=".55"/></pattern>
    <linearGradient id="gpBoard" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a2a22"/><stop offset=".5" stop-color="#4e3a2e"/><stop offset="1" stop-color="#2e2018"/></linearGradient>
    <radialGradient id="gpEmber" cx=".5" cy=".7" r=".7"><stop offset="0" stop-color="#ff9a3a" stop-opacity=".55"/><stop offset=".5" stop-color="#8a2a10" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="pbEye"><stop offset="0" stop-color="#e8ffd0"/><stop offset=".25" stop-color="#9aff7a" stop-opacity=".9"/><stop offset=".55" stop-color="#4adf5a" stop-opacity=".28"/><stop offset="1" stop-color="#2adf4a" stop-opacity="0"/></radialGradient>`;

  // ---------------- the ปอบ ----------------
  const eyePair = (cx, cy, k, id) => `<g ${id ? `id="${id}"` : ""}>${[-1, 1].map((sd) => `<circle cx="${f1(cx + sd * 22 * k)}" cy="${f1(cy)}" r="${f1(42 * k)}" fill="url(#pbEye)" style="mix-blend-mode:screen"/>
    <path d="M${f1(cx + sd * 22 * k - 13 * k)},${f1(cy)}Q${f1(cx + sd * 22 * k)},${f1(cy - 9 * k)} ${f1(cx + sd * 22 * k + 13 * k)},${f1(cy + sd * 2 * k)}Q${f1(cx + sd * 22 * k)},${f1(cy + 6 * k)} ${f1(cx + sd * 22 * k - 13 * k)},${f1(cy)}Z" fill="#b8ff8a"/>
    <ellipse cx="${f1(cx + sd * 22 * k)}" cy="${f1(cy)}" rx="${f1(3.5 * k)}" ry="${f1(4 * k)}" fill="#f4ffe8"/>`).join("")}</g>`;
  function ghost2(x, y, s, o = {}) {
    const id = o.id || "", pose = o.pose || "eat", r = mk(o.seed || 13);
    const hair = (hx, hy, n, len, spread) => Array.from({ length: n }, (_, i) => { const dx = (i / (n - 1) - 0.5) * spread, L = len * (0.7 + r() * 0.5), w = 3 + r() * 6;
      return `<path d="M${f1(hx + dx * 0.5)},${f1(hy)}C${f1(hx + dx)},${f1(hy + L * 0.3)} ${f1(hx + dx * 1.3 + (r() - 0.5) * 30)},${f1(hy + L * 0.65)} ${f1(hx + dx * 1.2 + (r() - 0.5) * 40)},${f1(hy + L)}" stroke="${BL}" stroke-width="${f1(w)}" fill="none" stroke-linecap="round"/>`; }).join("");
    const limb = (pts, w) => `<path d="M${pts[0]}Q${pts[1]} ${pts[2]}" stroke="${BL}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
    const fingers = (hx, hy, ang, L) => [-24, -8, 8, 24].map((da, i) => { const a = (ang + da) * Math.PI / 180, l = L * (i === 0 || i === 3 ? 0.8 : 1);
      const mx = hx + Math.cos(a) * l * 0.55, my = hy + Math.sin(a) * l * 0.55, ex = hx + Math.cos(a + 0.35) * l, ey = hy + Math.sin(a + 0.35) * l;
      return `<path d="M${f1(hx)},${f1(hy)}Q${f1(mx)},${f1(my)} ${f1(ex)},${f1(ey)}" stroke="${BL}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M${f1(ex)},${f1(ey)}l${f1(Math.cos(a + 0.6) * 14)},${f1(Math.sin(a + 0.6) * 14)}" stroke="#1e221e" stroke-width="4" stroke-linecap="round"/>`; }).join("");
    let g = `<ellipse cx="0" cy="8" rx="${pose === "stand" ? 120 : 190}" ry="20" fill="#000" opacity=".55"/>`;
    if (pose === "stand") {
      g += limb(["-30,-300", "-40,-150", "-46,0"], 30) + limb(["30,-300", "36,-150", "40,0"], 30);
      g += `<path d="M-70,-560C-80,-480 -60,-380 -40,-290H40C60,-380 80,-480 70,-560Q0,-600 -70,-560Z" fill="${BL}"/>`;
      g += limb(["-70,-540", "-120,-380", "-110,-210"], 22) + limb(["70,-540", "120,-380", "112,-210"], 22) + fingers(-110, -210, 100, 70) + fingers(112, -210, 80, 70);
      g += `<ellipse cx="0" cy="-620" rx="52" ry="62" fill="${BL}"/>` + hair(0, -670, 16, 260, 130) + eyePair(0, -618, 1, id ? `${id}-eyes` : "");
    } else {
      // crouched on its heels: the back a long arch with the spine showing, knees up by the chest, the head hung forward
      // under a curtain of hair; long arms fold back to the mouth (eat) or reach down to the floor (peer)
      const peer = pose === "peer", HX = peer ? 120 : 112, HY = peer ? -400 : -352;
      // legs folded under: the far shin, the near thigh up to a knee by the chest, the near shin down to a long-toed foot
      g += limb(["-80,-110", "-104,-50", "-100,0"], 32) + `<path d="M-124,-6h70q12,4 0,12h-70z" fill="${BL}"/>`;
      // the torso: a full wedge, the back bowed up into a knobbled spine, the chest hollow
      const back = "M-136,-86C-200,-200 -150,-366 -10,-404C50,-416 100,-402 132,-372L64,-300C28,-250 6,-180 -6,-104Z";
      g += `<path d="${back}" fill="${BL}"/><path d="M-140,-96C-200,-210 -150,-366 -10,-404C50,-416 100,-402 132,-372" stroke="${RIM}" stroke-width="4.5" fill="none" opacity=".95"/>`;
      for (let k = 0; k < 8; k++) { const u = 0.12 + k * 0.1, px = -170 + u * 240 - Math.sin(u * 2.6) * 10, py = -120 - Math.sin(u * Math.PI * 0.86) * 290; g += `<path d="M${f1(px - 8)},${f1(py)}q8,-10 16,0" stroke="${RIM}" stroke-width="2.4" fill="none"/>`; }
      g += `<path d="M-90,-300q20,-30 50,-40M-110,-220q24,-24 50,-30" stroke="#1e2620" stroke-width="3" fill="none"/>`;
      g += limb(["-50,-120", "20,-240", "76,-236"], 46) + limb(["76,-236", "80,-110", "60,0"], 30) + `<path d="M40,-6h66q12,4 0,12h-66z" fill="${BL}"/>${[0, 1, 2, 3].map((k) => `<path d="M100,${-2 + k * 2}l${30 + k * 4},${-4 + k * 3}" stroke="${BL}" stroke-width="5" stroke-linecap="round"/>`).join("")}`;
      g += `<g ${id ? `id="${id}-head"` : ""}><ellipse cx="${HX}" cy="${HY}" rx="56" ry="60" fill="${BL}"/>`;
      // the hair: one dark curtain with a ragged hem, a few loose strands, a gap where the eyes catch the light
      const hem = Array.from({ length: 9 }, (_, k) => `${f1(HX - 70 + k * 18)},${f1(HY + (peer ? 120 : 170) + (k % 2 ? 30 : 0) + r() * 30)}`).join(" L");
      g += `<path d="M${HX - 62},${HY - 30}C${HX - 80},${HY + 40} ${HX - 80},${HY + 100} ${HX - 70},${HY + (peer ? 130 : 180)}L${hem}L${HX + 80},${HY + (peer ? 110 : 160)}C${HX + 84},${HY + 60} ${HX + 70},${HY - 10} ${HX + 56},${HY - 40}Z" fill="${BL}"/>`;
      g += hair(HX, HY + 60, 7, peer ? 140 : 200, 130);
      g += `<path d="M${HX - 50},${HY - 40}Q${HX},${HY - 80} ${HX + 52},${HY - 44}" stroke="${RIM}" stroke-width="4" fill="none" opacity=".8"/>`;
      g += `<path d="M${HX - 34},${HY + 2}Q${HX + 10},${HY - 14} ${HX + 50},${HY + 4}L${HX + 46},${HY + 30}Q${HX + 10},${HY + 18} ${HX - 30},${HY + 30}Z" fill="#000" opacity=".9"/>`;
      g += eyePair(HX + 8, HY + 14, peer ? 1.05 : 0.95, id ? `${id}-eyes` : "") + `</g>`;
      if (!peer) {
        g += limb(["50,-340", "200,-250", "150,-262"], 20) + fingers(150, -262, -160, 50);
        if (o.food !== false) g += `<g transform="translate(170,-236) rotate(-70) scale(.3)">${Pop2.mush2 ? Pop2.mush2(0, 60, 1, { v: "open", dirt: false }) : ""}</g>`;
        g += limb(["10,-330", "180,-180", "130,-226"], 18) + fingers(130, -226, -150, 46);
      } else { g += limb(["50,-340", "200,-200", "240,-30"], 20) + fingers(240, -30, 70, 60) + limb(["10,-330", "120,-160", "150,-16"], 18) + fingers(150, -16, 80, 56); }
    }
    return `<g ${id ? `id="${id}"` : ""} transform="translate(${f1(x)},${f1(y)}) scale(${o.flip ? -s : s},${s})" opacity="${o.op ?? 1}">${g}</g>`;
  }

  // ---------------- the room upstairs ----------------
  function bedroom2(L, o = {}) {
    const id = o.id || "br", r = mk(o.seed || 21), G = o.ground ?? 1500, WX = o.window ?? 820, BX = o.bed ?? 540;
    // sky (seen through the window and the wall gaps)
    let sky = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#brNight)"/><circle id="${id}-moon" cx="${WX + 60}" cy="520" r="300" fill="url(#kiMoon)"/><circle cx="${WX + 60}" cy="520" r="30" fill="#f4f6ff"/>`;
    for (let k = 0; k < 40; k++) sky += `<circle cx="${f1(-600 + r() * 2400)}" cy="${f1(-300 + r() * 1100)}" r="${f1(1 + r() * 1.5)}" fill="#e8ecff" opacity="${f1(0.2 + r() * 0.5)}"/>`;
    put(L.sky, sky);
    // the plank wall with gaps, the window cut out of it
    let w = `<defs><mask id="${id}-wm"><rect x="-1300" y="-900" width="3700" height="3900" fill="#fff"/><rect x="${WX - 150}" y="300" width="300" height="400" fill="#000"/></mask></defs><g mask="url(#${id}-wm)"><rect x="-1300" y="-900" width="3700" height="${G + 900 - 240}" fill="url(#brWall)"/>`;
    for (let k = 0; k < 60; k++) { const px = -1300 + k * 62; w += `<rect x="${px}" y="-900" width="58" height="${G + 900 - 240}" fill="${["#221e28", "#262230", "#1e1a24"][k % 3]}"/><path d="M${px + 59},-900V${G - 240}" stroke="#9ab4ff" stroke-width="2.4" opacity="${f1(0.12 + r() * 0.25)}"/>`; }
    w += `</g>`;
    // window frame and shutters, one open
    w += `<rect x="${WX - 160}" y="290" width="320" height="420" fill="none" stroke="#3a2e28" stroke-width="20"/><path d="M${WX - 150},300V700M${WX + 150},300V700" stroke="#2a201c" stroke-width="6"/>
      <path d="M${WX + 150},300L${WX + 300},270V740L${WX + 150},700Z" fill="#2e2620" stroke="#1a1410" stroke-width="3"/>${[0, 1, 2, 3, 4, 5].map((k) => `<path d="M${WX + 160},${330 + k * 64}L${WX + 290},${310 + k * 70}" stroke="#463a30" stroke-width="5"/>`).join("")}
      <path d="M${WX - 150},300L${WX - 230},320V690L${WX - 150},700Z" fill="#2a221c" stroke="#1a1410" stroke-width="3"/>`;
    put(L.mid, w);
    // the floor in perspective with gaps between the boards
    let s = `<rect x="-1300" y="${G - 240}" width="3700" height="1700" fill="url(#brFloor)"/>`;
    for (let k = 0; k < 14; k++) { const y = G - 240 + Math.pow(k / 13, 1.6) * 1200; s += `<path d="M-1300,${f1(y)}H2400" stroke="#0a0608" stroke-width="${f1(2 + k * 0.6)}" opacity=".85"/><path d="M-1300,${f1(y + 3 + k * 0.4)}H2400" stroke="#6a5048" stroke-width="1.6" opacity=".35"/>`; }
    for (let k = 0; k < 30; k++) { const y = G - 220 + r() * 1100, x = -1200 + r() * 3300; s += `<path d="M${f1(x)},${f1(y)}h${f1(40 + r() * 140)}" stroke="#1a1214" stroke-width="2" opacity=".35"/>`; }
    // moonlight from the window across the floor
    s += `<path d="M${WX - 150},700L${WX + 150},700L${WX - 160},${G + 700}L${WX - 900},${G + 700}Z" fill="#a8c4ff" opacity=".12"/>`;
    // the mattress, pillow, blanket
    s += `<g transform="translate(${BX},${G + 80})"><ellipse cx="0" cy="40" rx="430" ry="40" fill="#000" opacity=".5"/><path d="M-400,30L-380,-40H380L400,30Z" fill="#c8b8d8"/><path d="M-400,30H400V44H-400Z" fill="#8a7aa0"/>
      <path d="M-360,-40Q-370,-80 -300,-84H-150Q-120,-80 -130,-40Z" fill="#efe8f4"/><path d="M-60,-44Q100,-70 380,-40L390,26Q100,40 -40,24Z" fill="#6a8ab8"/><path d="M-40,-30Q100,-50 360,-30M-30,0Q100,-14 370,0" stroke="#4a6a98" stroke-width="3" fill="none"/></g>`;
    if (o.phone) s += `<g id="${id}-phone" transform="translate(${BX - 250},${G + 30}) rotate(-12)"><rect x="-26" y="-12" width="52" height="24" rx="5" fill="#1a1c20"/><rect x="-22" y="-9" width="44" height="18" rx="3" fill="#cfe4ff"/></g>`;
    put(L.set, s);
    // the mosquito net: back panel behind the actor, front panel over it (in the glow layer, which sits above the actors)
    const nx0 = BX - 440, nx1 = BX + 440, ny0 = G - 760, ny1 = G + 120;
    put(L.set, `<path d="M${nx0 + 60},${ny0}H${nx1 - 60}L${nx1 - 60},${ny1 - 120}H${nx0 + 60}Z" fill="#cfd8e8" opacity=".07"/><path d="M${nx0 + 60},${ny0}H${nx1 - 60}L${nx1 - 60},${ny1 - 120}H${nx0 + 60}Z" fill="url(#brMesh)" opacity=".25"/>`);
    let gl = `<g id="${id}-net"><path d="M${nx0},${ny0 + 30}L${nx0 + 60},${ny0}H${nx1 - 60}L${nx1},${ny0 + 30}V${ny1}Q${BX},${ny1 + 16} ${nx0},${ny1}Z" fill="#dfe6f2" opacity=".1"/>
      <path d="M${nx0},${ny0 + 30}L${nx0 + 60},${ny0}H${nx1 - 60}L${nx1},${ny0 + 30}V${ny1}Q${BX},${ny1 + 16} ${nx0},${ny1}Z" fill="url(#brMesh)" opacity=".35"/>
      <path d="M${nx0},${ny0 + 30}V${ny1}M${nx1},${ny0 + 30}V${ny1}M${nx0 + 60},${ny0}V${ny1 - 120}M${nx1 - 60},${ny0}V${ny1 - 120}" stroke="#e8eef8" stroke-width="2" opacity=".35"/>
      <path d="M${nx0 + 140},${ny0 + 30}Q${nx0 + 160},${(ny0 + ny1) / 2} ${nx0 + 130},${ny1}M${nx1 - 200},${ny0 + 30}Q${nx1 - 180},${(ny0 + ny1) / 2} ${nx1 - 210},${ny1}" stroke="#e8eef8" stroke-width="5" opacity=".14" fill="none"/>
      <path d="M${nx0 + 60},${ny0}L${nx0 + 30},-900M${nx1 - 60},${ny0}L${nx1 - 30},-900" stroke="#c8c8d0" stroke-width="2" opacity=".5"/></g>`;
    gl += `<path d="M${WX - 150},300L${WX + 150},300L${WX - 200},${G + 600}L${WX - 900},${G + 600}Z" fill="url(#brBeam)" style="mix-blend-mode:screen"/>`;
    if (o.phone) gl += `<circle cx="${BX - 250}" cy="${G + 30}" r="260" fill="url(#brPhone)" style="mix-blend-mode:screen"/>`;
    put(L.glow, gl);
  }

  // ---------------- through the floor gap ----------------
  function gap2(L, o = {}) {
    const id = o.id || "gp", r = mk(o.seed || 27), GX = o.gap ?? 560, GW = o.gw ?? 170;
    // below: the dark kitchen floor with the ember glow, the pot from above, the ปอบ crouched by it — clipped to the slit
    let below = `<defs><clipPath id="${id}-slit"><path d="M${GX - GW / 2},-200L${GX + GW / 2 + 10},-200L${GX + GW / 2 - 6},2200L${GX - GW / 2 + 8},2200Z"/></clipPath></defs>
      <g clip-path="url(#${id}-slit)"><rect x="-200" y="-200" width="1500" height="2400" fill="#0c0806"/><rect x="-200" y="-200" width="1500" height="2400" fill="url(#gpEmber)"/>
      <g transform="translate(${GX - 40},1180)"><circle r="190" fill="#3a3632"/><circle r="170" fill="#5a3a12"/><circle r="150" fill="#7a4e1a"/>${[[-40, -30], [30, 20], [60, -50], [-20, 60]].map(([mx, my]) => `<ellipse cx="${mx}" cy="${my}" rx="34" ry="12" fill="#e8dcc4" opacity=".8"/>`).join("")}<circle r="190" fill="none" stroke="#8a8680" stroke-width="10"/></g>`;
    if (o.pob !== false) below += ghost2(GX - 140, 1000 + 400 * 1.7, 1.7, { id: `${id}-pob`, pose: "peer" });
    below += `</g>`;
    put(L.mid, below);
    // the boards: wide planks filling the frame, worn edges at the slit, nail heads
    let b = "";
    const plank = (x0, x1) => `<path d="M${x0},-200H${x1}V2200H${x0}Z" fill="url(#gpBoard)"/>` +
      Array.from({ length: 6 }, (_, k) => { const gx = x0 + (x1 - x0) * (0.15 + k * 0.14) + (r() - 0.5) * 10; return `<path d="M${f1(gx)},-200C${f1(gx + 20)},500 ${f1(gx - 20)},1200 ${f1(gx + 10)},2200" stroke="#1e140e" stroke-width="${f1(1.5 + r() * 2)}" fill="none" opacity=".55"/>`; }).join("") +
      [400, 1500].map((ny) => `<circle cx="${f1(x0 + 30)}" cy="${ny}" r="7" fill="#1a1410"/><circle cx="${f1(x1 - 30)}" cy="${ny}" r="7" fill="#1a1410"/>`).join("");
    b += plank(-300, GX - GW / 2) + plank(GX + GW / 2, 1400);
    b += `<path d="M${GX - GW / 2},-200V2200" stroke="#6a5040" stroke-width="4" opacity=".7"/><path d="M${GX + GW / 2},-200V2200" stroke="#0a0604" stroke-width="10" opacity=".8"/>`;
    b += `<path d="M${GX - GW / 2 - 300},-200V2200" stroke="#0a0604" stroke-width="12"/>`;
    put(L.set, b);
    // the ember light spilling up through the slit onto the board edges
    put(L.glow, `<path d="M${GX - GW / 2 - 40},-200H${GX + GW / 2 + 40}V2200H${GX - GW / 2 - 40}Z" fill="url(#gpEmber)" opacity=".5" style="mix-blend-mode:screen"/>`);
  }

  Object.assign(Sets, { bedroom2, gap2 });
  Object.assign(Pop2, { ghost2, eyePair });
})();
