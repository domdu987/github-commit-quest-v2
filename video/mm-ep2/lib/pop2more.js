// "เห็ดปอบ" v2 — the remaining story sets: the kitchen clock, the shadow-puppet legend, the pot from above, the folk tests on the
// bench, the boiling pot in cutaway, the footprints in the morning dirt, the community-forest sign, the ปอบ's face, and props.
//   Sets.clock2(L, o)     the clock on the post under the house; hands #id-hh #id-mm (rotate attr); o.night (2 a.m., moonlit)
//   Sets.legend2(L, o)    a หนังประโมทัย screen lit from behind; puppets #id-man #id-pob #id-inner (the ปอบ inside him), #id-lamp
//   Sets.potTop(L, o)     looking down into the curry pot: broth, mushroom slices, rice grains, the ladle #id-ladle; steam
//   Sets.testsTop(L, o)   the folk tests on the bamboo bench: rice #id-t0, silver spoon #id-t1, shallot #id-t2; stamps #id-x0..2, #id-verdict
//   Sets.potX(L, o)       the pot boiling, cut open: toxin specks #id-tox inside, a thermometer #id-therm, a timer #id-clock / #id-hand
//   Sets.printsTop(L, o)  dirt from above in morning light: long-toed bare footprints #id-p0..; the pot's foot at the top; Mint's shoe for scale
//   Sets.sign2(L, o)      end card: the community-forest sign on a trunk, a note pinned under it (o.ep, o.title) #id-sign #id-note
//   Pop2.pobFace(x, y, s, o)   the ปอบ's face filling the frame (jump scare); eyes #id-eyes
//   Pop2.PROP.{phone, ladle, noodles, suitcase, bowl}  props to hold (hand group coordinates: the palm at (0, 118))
(function () {
  const { mk, f1, put, blob } = Pop2;
  const LN = "#2a1e1a", BL = "#0a0c0b";
  const sideFlames = (x, y, k) => [-1, 1].map((sd) => [0, 1, 2].map((i) => { const fx = x + sd * (k + i * 26), fh = 70 + (i % 2) * 40; return `<path d="M${fx - 16},${y}Q${fx - 18},${y - fh * 0.6} ${fx + sd * 6},${y - fh}Q${fx + 20},${y - fh * 0.5} ${fx + 16},${y}Z" fill="#ffa030" opacity=".9"/><path d="M${fx - 7},${y}Q${fx - 7},${y - fh * 0.4} ${fx},${y - fh * 0.6}Q${fx + 9},${y - fh * 0.3} ${fx + 7},${y}Z" fill="#fff2a8"/>`; }).join("")).join("");

  Sets.DEFS += `
    <radialGradient id="lgScreen" cx=".5" cy=".55" r=".7"><stop offset="0" stop-color="#fff2c8"/><stop offset=".45" stop-color="#f4c47a"/><stop offset="1" stop-color="#9a5a2a"/></radialGradient>
    <radialGradient id="lgSpill"><stop offset="0" stop-color="#ffb860" stop-opacity=".45"/><stop offset="1" stop-color="#ffb860" stop-opacity="0"/></radialGradient>
    <radialGradient id="ptBroth" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#d8a43a"/><stop offset=".7" stop-color="#a8701e"/><stop offset="1" stop-color="#6a4210"/></radialGradient>
    <linearGradient id="ptRim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f2ee"/><stop offset=".5" stop-color="#a8a6a2"/><stop offset="1" stop-color="#5a5856"/></linearGradient>
    <linearGradient id="bnSlat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8b070"/><stop offset=".5" stop-color="#c49a5a"/><stop offset="1" stop-color="#a88044"/></linearGradient>
    <linearGradient id="bnLeaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ab04a"/><stop offset="1" stop-color="#3a7a2a"/></linearGradient>
    <linearGradient id="pxLiquid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8a43a" stop-opacity=".95"/><stop offset="1" stop-color="#8a5a18" stop-opacity=".95"/></linearGradient>
    <linearGradient id="prDirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6a46"/><stop offset="1" stop-color="#7a4e30"/></linearGradient>
    <radialGradient id="prMorning" cx=".3" cy=".2" r=".9"><stop offset="0" stop-color="#ffe8b8" stop-opacity=".55"/><stop offset="1" stop-color="#ffe8b8" stop-opacity="0"/></radialGradient>
    <linearGradient id="sgWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6a3e"/><stop offset="1" stop-color="#6a4426"/></linearGradient>
    <radialGradient id="pfGlow"><stop offset="0" stop-color="#1e2a22" stop-opacity=".9"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>`;

  // ---------------- props in hand (palm at (0, 118) in the hand group) ----------------
  const PROP = {
    phone: (o = {}) => `<g transform="translate(${o.dx ?? 4},${o.dy ?? 96}) rotate(${o.rot ?? -8})"><rect x="-17" y="-34" width="34" height="62" rx="7" fill="#22262c" stroke="${LN}" stroke-width="2.4"/><rect x="-14" y="-30" width="28" height="52" rx="4" fill="${o.screen || "#9ac4ff"}"/><path d="M-10,-26l12,0" stroke="#fff" stroke-width="2" opacity=".6"/></g>`,
    ladle: () => `<g transform="translate(2,112) rotate(-14)"><path d="M0,0V-150" stroke="#8a8680" stroke-width="7" stroke-linecap="round"/><path d="M0,0V-150" stroke="#d8d6d0" stroke-width="3" stroke-linecap="round"/><path d="M-26,-150Q-26,-182 0,-184Q26,-182 26,-150Z" fill="#c8c6c0" stroke="${LN}" stroke-width="2.4"/></g>`,
    noodles: () => `<g transform="translate(0,104)"><path d="M-28,-40H28L22,30H-22Z" fill="#f4ecd8" stroke="${LN}" stroke-width="2.4"/><path d="M-28,-40H28V-28H-28Z" fill="#e8433a"/><text x="0" y="6" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="15" fill="#e8433a">มาม่า</text><path d="M-10,-44q10,-26 20,0" stroke="#f4ecd8" stroke-width="4" fill="none" opacity=".7"/></g>`,
    suitcase: () => `<g transform="translate(0,118)"><path d="M-3,0V60" stroke="#3a3a40" stroke-width="6"/><rect x="-46" y="60" width="92" height="130" rx="12" fill="#e8a84a" stroke="${LN}" stroke-width="3"/><path d="M-46,100H46M-46,150H46" stroke="#c4882e" stroke-width="4"/><circle cx="-30" cy="194" r="9" fill="#2a2a2e"/><circle cx="30" cy="194" r="9" fill="#2a2a2e"/></g>`,
    bowl: () => `<g transform="translate(0,104)"><path d="M-40,-10Q-40,30 0,32Q40,30 40,-10Z" fill="#f2ece0" stroke="${LN}" stroke-width="2.4"/><path d="M-38,4h76" stroke="#3a6a9a" stroke-width="4"/><ellipse cx="0" cy="-10" rx="40" ry="9" fill="#c8902e"/><ellipse cx="-12" cy="-12" rx="10" ry="4" fill="#f2e8d4"/></g>`,
  };

  // ---------------- the clock on the post ----------------
  function clock2(L, o = {}) {
    const id = o.id || "ck", r = mk(o.seed || 5), night = !!o.night, CX = 540, CY = o.cy ?? 860;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="${night ? "#05070c" : "#1a120c"}"/>`);
    let far = "";
    if (!night) for (let k = 0; k < 14; k++) far += `<circle cx="${f1(-100 + r() * 1300)}" cy="${f1(100 + r() * 1600)}" r="${f1(30 + r() * 70)}" fill="#ffb860" opacity="${f1(0.06 + r() * 0.12)}"/>`;
    put(L.far, far);
    // the post and the plank wall behind it
    let s = `<rect x="-1300" y="-900" width="3700" height="3900" fill="${night ? "#0e0c14" : "#3a2618"}"/>`;
    for (let k = 0; k < 30; k++) s += `<rect x="${-600 + k * 80}" y="-900" width="76" height="3900" fill="${night ? ["#100e16", "#14121a"][k % 2] : ["#3e2a1c", "#46301e", "#3a2618"][k % 3]}"/>`;
    s += `<rect x="${CX - 150}" y="-900" width="300" height="3900" fill="url(#kiPost)"/>${[0, 1, 2, 3].map((k) => `<path d="M${CX - 110 + k * 70},-900V3000" stroke="#1a0e08" stroke-width="3" opacity=".35"/>`).join("")}`;
    // a calendar page hanging beside the clock
    s += `<g transform="translate(${CX + 330},${CY + 230}) rotate(4)"><rect x="-90" y="-120" width="180" height="230" fill="${night ? "#3a3a48" : "#efe6d2"}"/><rect x="-90" y="-120" width="180" height="44" fill="${night ? "#4a2a2a" : "#c8342a"}"/>
      <text x="0" y="40" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="96" fill="${night ? "#1a1a22" : "#3a2a22"}">15</text><path d="M0,-130v12" stroke="#222" stroke-width="3"/></g>`;
    // the clock: wooden case, cream face, hour marks, numbers, hands
    let c = `<circle r="250" fill="#000" opacity=".45" transform="translate(10,22)"/><circle r="250" fill="${night ? "#2a1e16" : "#6a3e22"}" stroke="${LN}" stroke-width="5"/><circle r="232" fill="${night ? "#3a2a1e" : "#8a5430"}"/>
      <circle r="206" fill="${night ? "#c8ccd8" : "#f6eedc"}" stroke="${LN}" stroke-width="4"/>`;
    for (let k = 0; k < 60; k++) c += `<path d="M0,-196V${k % 5 ? -186 : -172}" stroke="#3a2a22" stroke-width="${k % 5 ? 2 : 5}" transform="rotate(${k * 6})"/>`;
    for (let k = 1; k <= 12; k++) { const a = (k * 30 - 90) * Math.PI / 180; c += `<text x="${f1(Math.cos(a) * 148)}" y="${f1(Math.sin(a) * 148 + 14)}" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="40" fill="#3a2a22">${k}</text>`; }
    c += `<g id="${id}-hh" transform="rotate(${o.hh ?? 60})"><path d="M-7,20L-5,-100L0,-112L5,-100L7,20Z" fill="#2a1e1a"/></g><g id="${id}-mm" transform="rotate(${o.mm ?? 0})"><path d="M-4,26L-3,-160L0,-172L3,-160L4,26Z" fill="#2a1e1a"/></g>
      <g id="${id}-ss" transform="rotate(0)"><path d="M0,40V-176" stroke="#c8342a" stroke-width="3"/></g><circle r="11" fill="#c8a040" stroke="${LN}" stroke-width="2.4"/>
      <path d="M-150,-120Q-60,-200 60,-196" stroke="#fff" stroke-width="18" fill="none" opacity="${night ? 0.12 : 0.3}" stroke-linecap="round"/>`;
    s += `<g transform="translate(${CX},${CY})">${c}</g>`;
    put(L.set, s);
    put(L.glow, night ? `<path d="M-200,-200L300,-200L${CX + 420},2200L${CX - 380},2200Z" fill="#a8c4ff" opacity=".1" style="mix-blend-mode:screen"/>` :
      `<circle cx="${CX - 300}" cy="${CY - 500}" r="900" fill="url(#kiLampGlow)" opacity=".55" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- the shadow-puppet legend ----------------
  const holes = (pts) => pts.map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="url(#lgScreen)"/>`).join("");
  function manPuppet() { // a villager in profile facing right: topknot, big eye, sarong, an arm on a stick
    return `<path d="M-10,-470Q-30,-500 -6,-516Q14,-510 8,-484Z" fill="#1a120c"/>
      <path d="M-40,-440Q-46,-490 -4,-490Q34,-488 40,-456L52,-446L40,-436Q40,-410 22,-400L20,-380H-26Q-44,-400 -40,-440Z" fill="#1a120c"/>
      <path d="M-50,-380Q-66,-300 -50,-200H50Q66,-300 46,-380Z" fill="#1a120c"/>
      <path d="M-56,-200L-70,-20H70L58,-200Z" fill="#1a120c"/><path d="M-56,-20L-60,0H-10L-14,-20ZM14,-20L10,0H60L56,-20Z" fill="#1a120c"/>
      ${holes([[10, -452, 6], [-20, -320, 5], [0, -320, 5], [20, -320, 5], [-10, -290, 4], [10, -290, 4], [-30, -150, 5], [0, -150, 5], [30, -150, 5], [-15, -110, 4], [15, -110, 4], [-30, -70, 5], [0, -70, 5], [30, -70, 5]])}
      <path d="M-56,-150H58M-60,-90H62" stroke="url(#lgScreen)" stroke-width="4"/>
      <path d="M40,-370L120,-280L100,-200" stroke="#1a120c" stroke-width="18" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M100,-200L100,200" stroke="#2a1a10" stroke-width="5"/>
      <path d="M0,0V420" stroke="#2a1a10" stroke-width="7"/>`;
  }
  function pobPuppet() { // the ปอบ puppet: thin, hunched, wild hair, long nails, a cut-out eye
    return `<path d="M-60,-300Q-100,-420 -20,-470Q40,-490 70,-440Q80,-400 60,-380L40,-380Q30,-330 50,-260Q60,-160 30,-40L50,0H-10L-4,-60Q-30,-150 -60,-300Z" fill="#0c0806"/>
      ${Array.from({ length: 9 }, (_, k) => `<path d="M${-60 + k * 12},-460Q${-90 + k * 10},-380 ${-110 + k * 14},-300" stroke="#0c0806" stroke-width="7" fill="none" stroke-linecap="round"/>`).join("")}
      <path d="M40,-420l14,-4l-10,10z" fill="#9aff7a"/>${holes([[0, -300, 4], [10, -240, 4], [14, -180, 4], [10, -120, 4]])}
      <path d="M30,-340L140,-300L170,-330" stroke="#0c0806" stroke-width="12" fill="none" stroke-linecap="round"/>${[-16, -4, 8, 20].map((d) => `<path d="M170,-330l${30 + d * 0.4},${d}" stroke="#0c0806" stroke-width="5" stroke-linecap="round"/>`).join("")}
      <path d="M170,-330L170,100" stroke="#2a1a10" stroke-width="5"/><path d="M20,0V420" stroke="#2a1a10" stroke-width="7"/>`;
  }
  function legend2(L, o = {}) {
    const id = o.id || "lg", r = mk(o.seed || 41), CX = 540, CY = o.cy ?? 820, W = 900, H = 1100;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#07060a"/>`);
    let s = `<rect x="-1300" y="${CY + H / 2 + 40}" width="3700" height="1600" fill="#0e0a08"/>`;
    // the frame of bamboo poles, the cloth lit from behind with its folds
    s += `<g id="${id}-lamp"><rect x="${CX - W / 2}" y="${CY - H / 2}" width="${W}" height="${H}" fill="url(#lgScreen)"/></g>`;
    for (let k = 0; k < 9; k++) s += `<path d="M${CX - W / 2 + 60 + k * 100 + (r() - 0.5) * 20},${CY - H / 2}Q${CX - W / 2 + 70 + k * 100},${CY} ${CX - W / 2 + 56 + k * 100},${CY + H / 2}" stroke="#a8743a" stroke-width="3" fill="none" opacity=".25"/>`;
    s += `<rect x="${CX - W / 2 - 30}" y="${CY - H / 2 - 30}" width="${W + 60}" height="30" rx="12" fill="#5a3a1e"/><rect x="${CX - W / 2 - 30}" y="${CY + H / 2}" width="${W + 60}" height="30" rx="12" fill="#5a3a1e"/>
      <rect x="${CX - W / 2 - 30}" y="${CY - H / 2 - 200}" width="30" height="${H + 600}" rx="12" fill="#4a2e18"/><rect x="${CX + W / 2}" y="${CY - H / 2 - 200}" width="30" height="${H + 600}" rx="12" fill="#4a2e18"/>`;
    s += `<rect x="${CX - W / 2 - 40}" y="${CY + H / 2 + 30}" width="${W + 80}" height="400" fill="#1a1008"/><path d="M${CX - W / 2 - 40},${CY + H / 2 + 60}H${CX + W / 2 + 40}" stroke="#3a2412" stroke-width="6"/>`;
    // the puppets, pressed to the cloth (clipped to it)
    s += `<defs><clipPath id="${id}-clip"><rect x="${CX - W / 2}" y="${CY - H / 2}" width="${W}" height="${H}"/></clipPath></defs><g clip-path="url(#${id}-clip)">
      <g transform="translate(${CX - 120},${CY + 300})"><g id="${id}-man">${manPuppet()}<g id="${id}-inner" opacity="0"><g transform="translate(-6,-270) scale(.42)">${pobPuppet()}</g>
        ${[[-24, -230, 12], [18, -214, 10], [-4, -190, 9]].map(([x, y, rr]) => `<ellipse cx="${x}" cy="${y}" rx="${rr}" ry="${rr * 0.7}" fill="#8a2a1a"/>`).join("")}</g></g></g>
      <g transform="translate(${CX + 240},${CY + 300})"><g id="${id}-pob">${pobPuppet()}</g></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="${CX}" cy="${CY + H / 2 + 120}" r="700" fill="url(#lgSpill)" style="mix-blend-mode:screen"/>`);
    // the audience: heads and shoulders against the glow
    let fg = "";
    for (let k = 0; k < 7; k++) { const x = -60 + k * 190 + r() * 40, y = 1820 + r() * 60, s2 = 1 + r() * 0.3;
      fg += `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s2)})"><path d="M-110,200Q-110,40 -40,20Q0,10 40,20Q110,40 110,200Z" fill="#050404"/><ellipse cx="0" cy="-30" rx="56" ry="64" fill="#050404"/>${k % 3 === 0 ? `<circle cx="-30" cy="-84" r="22" fill="#050404"/>` : ""}</g>`; }
    put(L.fg, fg);
  }

  // ---------------- looking down into the pot ----------------
  function potTop(L, o = {}) {
    const id = o.id || "pt", r = mk(o.seed || 61), CX = o.cx ?? 540, CY = o.cy ?? 980, R = o.r ?? 470;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#140c08"/>`);
    let s = `<circle cx="${CX + 30}" cy="${CY + 50}" r="${R + 120}" fill="#000" opacity=".6"/>`;
    // the stove's rim under the pot, glowing
    s += `<circle cx="${CX}" cy="${CY}" r="${R + 80}" fill="#7a3a1a"/><circle cx="${CX}" cy="${CY}" r="${R + 60}" fill="#ff8a2a" opacity=".5"/>`;
    s += `<circle cx="${CX}" cy="${CY}" r="${R + 30}" fill="url(#ptRim)" stroke="${LN}" stroke-width="4"/><circle cx="${CX}" cy="${CY}" r="${R}" fill="#3a3632"/>`;
    s += `<path d="M${CX - R - 30},${CY - 20}h-70v40h70zM${CX + R + 30},${CY - 20}h70v40h-70z" fill="#4a4642" stroke="${LN}" stroke-width="3"/>`;
    s += `<circle cx="${CX}" cy="${CY}" r="${R - 14}" fill="url(#ptBroth)"/>`;
    // oil sheen, herbs, chillies, mushroom slices, rice grains
    for (let k = 0; k < 26; k++) { const a = r() * 6.283, d = Math.sqrt(r()) * (R - 60); s += `<ellipse cx="${f1(CX + Math.cos(a) * d)}" cy="${f1(CY + Math.sin(a) * d)}" rx="${f1(8 + r() * 20)}" ry="${f1(5 + r() * 12)}" fill="#ffd27a" opacity=".35"/>`; }
    for (let k = 0; k < 9; k++) { const a = r() * 6.283, d = Math.sqrt(r()) * (R - 90), x = CX + Math.cos(a) * d, y = CY + Math.sin(a) * d;
      s += `<path d="M${f1(x - 30)},${f1(y)}Q${f1(x)},${f1(y - 22)} ${f1(x + 30)},${f1(y)}Q${f1(x)},${f1(y + 16)} ${f1(x - 30)},${f1(y)}Z" fill="#4a8a2e" transform="rotate(${f1(r() * 180)} ${f1(x)} ${f1(y)})"/>`; }
    for (let k = 0; k < 5; k++) { const a = r() * 6.283, d = Math.sqrt(r()) * (R - 90), x = CX + Math.cos(a) * d, y = CY + Math.sin(a) * d; s += `<path d="M${f1(x)},${f1(y)}q30,-6 50,12" stroke="#d8342a" stroke-width="12" stroke-linecap="round" fill="none" transform="rotate(${f1(r() * 180)} ${f1(x)} ${f1(y)})"/>`; }
    for (let k = 0; k < 12; k++) { const a = r() * 6.283, d = Math.sqrt(r()) * (R - 100), x = CX + Math.cos(a) * d, y = CY + Math.sin(a) * d, rot = r() * 360;
      s += `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(rot)})"><path d="M-46,0C-44,-30 -20,-40 0,-40C20,-40 44,-30 46,0Q0,8 -46,0Z" fill="#f6efe0" stroke="#8a7458" stroke-width="2"/><path d="M-6,0V30H6V0" fill="#ece4d2" stroke="#8a7458" stroke-width="2"/>${[-30, -15, 0, 15, 30].map((gx) => `<path d="M${gx},-2L${gx * 0.3},-30" stroke="#d2c4a8" stroke-width="1.5"/>`).join("")}</g>`; }
    // the rice grains boiled in with it, still white
    s += `<g id="${id}-rice">`;
    for (let k = 0; k < 70; k++) { const a = r() * 6.283, d = Math.sqrt(r()) * 120, x = CX - 120 + Math.cos(a) * d, y = CY + 80 + Math.sin(a) * d * 0.8; s += `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="4" ry="9" fill="#fffaf0" stroke="#c8b898" stroke-width="1" transform="rotate(${f1(r() * 180)} ${f1(x)} ${f1(y)})"/>`; }
    s += `</g>`;
    s += `<circle cx="${CX}" cy="${CY}" r="${R - 14}" fill="none" stroke="#3a2008" stroke-width="18" opacity=".5"/><path d="M${CX - R + 60},${CY - R * 0.5}A${R - 40},${R - 40} 0 0 1 ${CX + R * 0.3},${CY - R + 50}" stroke="#fff" stroke-width="8" fill="none" opacity=".25"/>`;
    put(L.set, s);
    // the ladle comes up with a scoop of grains (id on the wrapper, positioned inside)
    if (o.ladle !== false) put(L.set, `<g id="${id}-ladle"><g transform="translate(${CX + 200},${CY + 60}) rotate(-30)"><path d="M0,0L700,0" stroke="#5a5652" stroke-width="30" stroke-linecap="round"/><path d="M0,0L700,0" stroke="#c8c4bc" stroke-width="18" stroke-linecap="round"/>
      <ellipse cx="-40" cy="0" rx="110" ry="88" fill="#d8d4cc" stroke="${LN}" stroke-width="4"/><ellipse cx="-40" cy="0" rx="92" ry="72" fill="#b8822a"/>${Array.from({ length: 30 }, () => { const a = r() * 6.283, d = Math.sqrt(r()) * 60, x = -40 + Math.cos(a) * d, y = Math.sin(a) * d * 0.8; return `<ellipse cx="${f1(x)}" cy="${f1(y)}" rx="5" ry="11" fill="#fffaf0" stroke="#c8b898" stroke-width="1" transform="rotate(${f1(r() * 180)} ${f1(x)} ${f1(y)})"/>`; }).join("")}
      <path d="M-120,-40Q-80,-80 -10,-80" stroke="#fff" stroke-width="7" fill="none" opacity=".6"/></g></g>`);
    put(L.glow, `<circle cx="${CX - 300}" cy="${CY - 600}" r="900" fill="url(#kiLampGlow)" opacity=".45" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- the folk tests on the bench ----------------
  function testsTop(L, o = {}) {
    const id = o.id || "tt", r = mk(o.seed || 71), UI = PopUI.ICON;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#2a1a0e"/>`);
    let s = "";
    for (let k = 0; k < 40; k++) s += `<rect x="-1300" y="${-900 + k * 96}" width="3700" height="90" fill="url(#bnSlat)"/><path d="M-1300,${-900 + k * 96 + 90}H2400" stroke="#5a3a1a" stroke-width="6"/>`;
    for (let k = 0; k < 30; k++) s += `<path d="M${f1(-200 + r() * 1500)},${f1(r() * 2000)}h${f1(60 + r() * 200)}" stroke="#8a6a3a" stroke-width="2" opacity=".5"/>`;
    const ITEMS = [[270, 540, "ต้มกับข้าวสาร", "rice"], [810, 540, "จุ่มช้อนเงิน", "spoon"], [540, 960, "ใส่หอมแดง", "shallot"]];
    ITEMS.forEach(([x, y, label, kind], i) => {
      s += `<g id="${id}-t${i}"><g transform="translate(${x},${y})"><ellipse cx="14" cy="22" rx="210" ry="170" fill="#000" opacity=".3"/><path d="M-200,-150Q0,-180 200,-150L190,160Q0,190 -200,160Z" fill="url(#bnLeaf)" stroke="#2a5a1a" stroke-width="4"/><path d="M-196,0H196" stroke="#2a5a1a" stroke-width="5" opacity=".6"/>${[-150, -90, -30, 30, 90, 150].map((lx) => `<path d="M${lx},0L${lx + 30},-140M${lx},0L${lx + 30},140" stroke="#9ac46a" stroke-width="2" opacity=".5"/>`).join("")}
        ${UI[kind](0, -10, 2.4)}<text x="0" y="230" text-anchor="middle" font-family="Mali" font-weight="700" font-size="50" fill="#fff6e0" stroke="#3a2210" stroke-width="10" paint-order="stroke">${label}</text></g></g>`;
      s += `<g id="${id}-x${i}" opacity="0"><g transform="translate(${x},${y - 10})"><circle r="150" fill="none" stroke="#e8302a" stroke-width="16" opacity=".9"/><path d="M-100,-100L100,100" stroke="#e8302a" stroke-width="18" stroke-linecap="round"/></g></g>`;
    });
    s += `<g id="${id}-verdict" opacity="0"><g transform="translate(540,1400) rotate(-4)"><rect x="-330" y="-90" width="660" height="150" rx="20" fill="#e8302a"/><text x="0" y="22" text-anchor="middle" font-family="Mali" font-weight="700" font-size="84" fill="#fff">ใช้ไม่ได้จริง!</text></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="300" cy="200" r="1100" fill="url(#kiLampGlow)" opacity=".35" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- the pot cut open: the poison does not cook out ----------------
  function potX(L, o = {}) {
    const id = o.id || "px", r = mk(o.seed || 81), CX = 430, G = 1560;
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#120c0a"/>`);
    let s = `<rect x="-1300" y="${G - 40}" width="3700" height="1600" fill="#1e140e"/>`;
    s += Pop2.stove2(CX, G + 140, 1.5, { id });
    const PW = 360, PH = 330, TOP = G + 140 - 1.5 * 170 - PH;
    // pot body with a cutaway window into the curry
    s += `<path d="M${CX - PW},${TOP + PH}C${CX - PW - 30},${TOP + 150} ${CX - PW - 20},${TOP + 40} ${CX - PW + 20},${TOP}H${CX + PW - 20}C${CX + PW + 20},${TOP + 40} ${CX + PW + 30},${TOP + 150} ${CX + PW},${TOP + PH}Q${CX},${TOP + PH + 30} ${CX - PW},${TOP + PH}Z" fill="url(#kiPot)" stroke="${LN}" stroke-width="4"/>`;
    s += `<path d="M${CX - PW + 30},${TOP + 50}H${CX + PW - 30}L${CX + PW - 20},${TOP + PH - 20}Q${CX},${TOP + PH + 4} ${CX - PW + 20},${TOP + PH - 20}Z" fill="url(#pxLiquid)" stroke="#f4f2ee" stroke-width="6" stroke-dasharray="18 10"/>`;
    s += `<defs><clipPath id="${id}-win"><path d="M${CX - PW + 30},${TOP + 50}H${CX + PW - 30}L${CX + PW - 20},${TOP + PH - 20}Q${CX},${TOP + PH + 4} ${CX - PW + 20},${TOP + PH - 20}Z"/></clipPath></defs><g clip-path="url(#${id}-win)">`;
    for (let k = 0; k < 6; k++) { const x = CX - 230 + k * 92, y = TOP + 130 + (k % 2) * 70; s += `<g transform="translate(${x},${y}) rotate(${k * 37})"><path d="M-40,0C-38,-26 -18,-34 0,-34C18,-34 38,-26 40,0Q0,7 -40,0Z" fill="#f6efe0" stroke="#8a7458" stroke-width="2"/></g>`; }
    s += `<g id="${id}-tox">${Array.from({ length: 14 }, (_, k) => { const x = CX - 260 + r() * 520, y = TOP + 90 + r() * 170; return `<g transform="translate(${f1(x)},${f1(y)}) scale(.36)">${PopUI.ICON.skull(0, 0, 1).replace(/#f4f0e6/g, "#7dff6a")}</g>`; }).join("")}</g>`;
    for (let k = 0; k < 12; k++) s += `<circle cx="${f1(CX - 260 + r() * 520)}" cy="${f1(TOP + 70 + r() * 200)}" r="${f1(5 + r() * 10)}" fill="none" stroke="#ffe8b8" stroke-width="3" opacity=".7"/>`;
    s += `</g><path d="M${CX - PW - 10},${TOP}H${CX + PW + 10}V${TOP - 22}H${CX - PW - 10}Z" fill="#c8c4bc" stroke="${LN}" stroke-width="4"/>`;
    s += `<g id="${id}-fire" style="mix-blend-mode:screen">${sideFlames(CX, TOP + PH + 6, PW - 10)}</g>`;
    // the thermometer and the timer on the right
    s += `<g id="${id}-therm"><g transform="translate(930,${TOP + 140})"><rect x="-26" y="-260" width="52" height="320" rx="26" fill="#f4f6f8" stroke="${LN}" stroke-width="5"/><circle cy="80" r="50" fill="#e8302a" stroke="${LN}" stroke-width="5"/><rect x="-12" y="-230" width="24" height="300" rx="12" fill="#e8302a"/>
      <text x="0" y="200" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="64" fill="#fff4e0" stroke="#3a2210" stroke-width="10" paint-order="stroke">100°C</text></g></g>`;
    s += `<g id="${id}-clock"><g transform="translate(900,${TOP - 250})"><circle r="92" fill="#fffaf0" stroke="${LN}" stroke-width="6"/>${[0, 90, 180, 270].map((a) => `<path d="M0,-80v14" stroke="${LN}" stroke-width="6" transform="rotate(${a})"/>`).join("")}<g id="${id}-hand" transform="rotate(0)"><path d="M0,10V-66" stroke="${LN}" stroke-width="8" stroke-linecap="round"/></g><circle r="8" fill="${LN}"/></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="${CX}" cy="${G}" r="800" fill="url(#kiFireGlow)" opacity=".8" style="mix-blend-mode:screen"/>`);
  }

  // ---------------- the footprints in the morning dirt ----------------
  function foot(x, y, rot, s, left, id) { // a bare print with toes far too long
    const m = left ? -1 : 1;
    return `<g ${id ? `id="${id}"` : ""}><g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(rot)}) scale(${f1(s * m)},${f1(s)})">
      <path d="M-34,60Q-46,0 -30,-60Q-14,-100 16,-96Q40,-80 36,-20Q34,40 18,80Q0,110 -20,96Q-34,86 -34,60Z" fill="#2e1608" opacity=".9"/>
      <path d="M-30,56Q-40,0 -26,-56" stroke="#2a1608" stroke-width="5" fill="none" opacity=".6"/>
      ${[[-24, -104, -30, -150, 24], [-2, -112, -2, -164, 20], [16, -108, 20, -156, 18], [30, -96, 38, -138, 16], [40, -76, 52, -112, 14]].map(([x0, y0, x1, y1, w]) => `<path d="M${x0},${y0}L${x1},${y1}" stroke="#4a2a16" stroke-width="${w}" stroke-linecap="round" opacity=".88"/><circle cx="${x1}" cy="${y1 - 6}" r="${w * 0.22}" fill="#2a1608"/>`).join("")}
      <path d="M-40,70Q-50,0 -36,-70" stroke="#c8946a" stroke-width="4" fill="none" opacity=".5"/></g></g>`;
  }
  // a print pressed into wet ground seen at an angle: squashed by perspective, a dark hollow, mud pushed up into a lit rim
  const SOLE = "M-34,60Q-46,0 -30,-60Q-14,-100 16,-96Q40,-80 36,-20Q34,40 18,80Q0,110 -20,96Q-34,86 -34,60Z";
  const TOES = [[-24, -104, -30, -150, 24], [-2, -112, -2, -164, 20], [16, -108, 20, -156, 18], [30, -96, 38, -138, 16], [40, -76, 52, -112, 14]];
  const printShape = (c, k = 1) => `<path d="${SOLE}" fill="${c}"/>` + TOES.map(([x0, y0, x1, y1, w]) => `<path d="M${x0},${y0}L${f1(x0 + (x1 - x0) * k)},${f1(y0 + (y1 - y0) * k)}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`).join("");
  function mudPrint(x, y, theta, s, left, squash = 0.45, o = {}) {
    const m = left ? -1 : 1;
    return `<g transform="translate(${f1(x)},${f1(y)}) scale(1,${squash}) rotate(${f1(theta)}) scale(${f1(s * m)},${f1(s)})">
      <g transform="translate(-6,-8)" opacity="${o.rim ?? 0.6}">${printShape(o.rimC || "#e2b282", o.toe)}</g>
      <g opacity="${o.op ?? 0.82}">${printShape(o.c || "#4a2610", o.toe)}</g>
      <g transform="translate(5,7) scale(.86)" opacity=".45">${printShape("#2a1206", o.toe)}</g></g>`;
  }
  // a line of prints walking away from (x0, y0) to (x1, y1): steps shrink with distance, feet alternate either side of the line
  function trail(x0, y0, x1, y1, n, s0, s1, o = {}) {
    const sq = o.squash ?? 0.45, ease = (u) => 1 - Math.pow(1 - u, 1.5), dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
    const theta = (Math.atan2(dx, -dy / sq) * 180) / Math.PI, px = -dy / len, py = dx / len;
    let g = "";
    for (let i = 0; i < n; i++) { const u = ease(i / (n - 1)), s = s0 + (s1 - s0) * u, side = i % 2 ? 1 : -1, off = side * 34 * s;
      g += `<g ${o.id ? `id="${o.id}-${i}"` : ""}>${mudPrint(x0 + dx * u + px * off, y0 + dy * u + py * off * sq, theta + side * 4, s, side < 0, sq, o)}</g>`; }
    return g;
  }
  function printsTop(L, o = {}) {
    const id = o.id || "pr", r = mk(o.seed || 91);
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#5a3a24"/>`);
    let s = `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#prDirt)"/>`;
    for (let k = 0; k < 160; k++) s += `<ellipse cx="${f1(-400 + r() * 2000)}" cy="${f1(-400 + r() * 2900)}" rx="${f1(2 + r() * 8)}" ry="${f1(2 + r() * 6)}" fill="${r() < 0.5 ? "#4a2a16" : "#b88a62"}" opacity=".6"/>`;
    for (let k = 0; k < 16; k++) s += `<path d="${blob(-300 + r() * 1700, -300 + r() * 2600, 60 + r() * 120, r, 9)}" fill="${r() < 0.5 ? "#6a4228" : "#a87a52"}" opacity=".25"/>`;
    // the curry pot's foot and the stove's corner at the top
    s += `<ellipse cx="300" cy="80" rx="360" ry="200" fill="#000" opacity=".35"/><ellipse cx="300" cy="40" rx="320" ry="170" fill="#7a3a1a" stroke="${LN}" stroke-width="4"/><ellipse cx="300" cy="30" rx="250" ry="120" fill="#3a2a22"/>`;
    // the trail: from the pot, down and away to the right
    const P = o.trail || [[380, 420, 160, true], [600, 640, 150, false], [520, 900, 165, true], [760, 1140, 150, false], [680, 1420, 162, true], [930, 1660, 152, false], [860, 1940, 160, true], [1120, 2180, 150, false]];
    P.forEach(([x, y, rot, left], i) => { s += foot(x, y, rot, 1.05, left, `${id}-p${i}`); });
    // her sneaker at the bottom-left for scale
    s += `<g transform="translate(140,1580) rotate(-10)"><path d="M-70,0Q-80,-150 -30,-200Q20,-230 60,-190Q90,-130 80,0Q70,60 0,64Q-60,60 -70,0Z" fill="#f6f4ee" stroke="${LN}" stroke-width="4"/><path d="M-70,0Q-80,-150 -30,-200" stroke="#ec5e7e" stroke-width="8" fill="none"/>
      <path d="M-30,-120h70M-34,-90h74M-36,-60h76" stroke="#b8b2a6" stroke-width="5"/><path d="M-60,40Q0,70 70,40" stroke="#d8d2c4" stroke-width="10" fill="none"/></g>`;
    put(L.set, s);
    put(L.glow, `<rect x="-200" y="-200" width="1500" height="2400" fill="url(#prMorning)" style="mix-blend-mode:screen"/>` +
      Array.from({ length: 5 }, (_, k) => `<path d="M${-300 + k * 260},-200L${-140 + k * 260},-200L${400 + k * 260},2300L${240 + k * 260},2300Z" fill="#fff0c8" opacity=".08" style="mix-blend-mode:screen"/>`).join(""));
  }

  // ---------------- the end card: the community-forest sign ----------------
  function sign2(L, o = {}) {
    const id = o.id || "sg";
    Sets.kok2(L, { id: `${id}k`, mound: false, fgTrunk: false, trunks: [[-200, 120], [1260, 110]], seed: 7 });
    let s = Pop2.trunk2(540, 2300, 3300, 300, Pop2.KPAL.day, mk(3), { cast: false });
    s += `<g id="${id}-sign"><g transform="translate(540,640)"><rect x="-400" y="-150" width="800" height="300" rx="18" fill="url(#sgWood)" stroke="${LN}" stroke-width="6"/>
      ${[0, 1, 2, 3].map((k) => `<path d="M-396,${-90 + k * 60}H396" stroke="#5a3a1e" stroke-width="3" opacity=".5"/>`).join("")}
      <circle cx="-370" cy="-120" r="10" fill="#4a4a4a"/><circle cx="370" cy="-120" r="10" fill="#4a4a4a"/><circle cx="-370" cy="120" r="10" fill="#4a4a4a"/><circle cx="370" cy="120" r="10" fill="#4a4a4a"/>
      <text x="0" y="-30" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="92" fill="#f2dfb4" stroke="#3a2210" stroke-width="6" paint-order="stroke">ป่าชุมชน</text>
      <text x="0" y="86" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="76" fill="#f2dfb4" stroke="#3a2210" stroke-width="6" paint-order="stroke">บ้านโคกเห็ด</text></g></g>`;
    s += `<g id="${id}-note"><g transform="translate(560,1120) rotate(-3)"><rect x="-300" y="-170" width="600" height="380" fill="url(#uiPaper)" filter="url(#uiShadow)"/><circle cx="0" cy="-150" r="14" fill="#c8342a" stroke="${LN}" stroke-width="3"/>
      <text x="0" y="-50" text-anchor="middle" font-family="Mali" font-weight="700" font-size="74" fill="#7a3a22">${o.ep || "ตอนที่ 2"}</text>
      <text x="0" y="60" text-anchor="middle" font-family="Mali" font-weight="700" font-size="62" fill="#3a2a22">${o.title || ""}</text>
      <text x="230" y="170" text-anchor="end" font-family="Mali" font-weight="600" font-size="34" fill="#8a6a50">— ยายคำ</text></g></g>`;
    put(L.set, s);
  }

  // ---------------- the ปอบ's face for the jump scare ----------------
  function pobFace(x, y, s, o = {}) {
    const id = o.id || "", r = mk(o.seed || 17);
    let g = `<circle r="900" fill="url(#pfGlow)"/><ellipse cx="0" cy="40" rx="300" ry="380" fill="${BL}"/>`;
    g += `<path d="M-180,40Q-170,-60 -110,-80Q-60,-40 -40,10Q-90,40 -180,40ZM180,40Q170,-60 110,-80Q60,-40 40,10Q90,40 180,40Z" fill="#000"/>`;
    g += `<path d="M-110,-40Q-60,-110 0,-70M110,-40Q60,-110 0,-70" stroke="#1e2620" stroke-width="10" fill="none"/>`;
    g += Pop2.eyePair(0, -10, 3.4, id ? `${id}-eyes` : "");
    g += `<path d="M-90,200Q0,170 90,200Q70,280 0,300Q-70,280 -90,200Z" fill="#000"/>${[-60, -30, 0, 30, 60].map((tx) => `<path d="M${tx - 10},${196 + Math.abs(tx) * 0.1}l10,26l10,-26" fill="#3a3a30"/>`).join("")}`;
    for (let k = 0; k < 40; k++) { const a = -Math.PI + (k / 39) * Math.PI, sx = Math.cos(a) * 280, sy = -300 + Math.sin(a) * 120, len = 500 + r() * 500; if (Math.abs(sx) < 170) continue;
      g += `<path d="M${f1(sx)},${f1(sy)}C${f1(sx * 1.2)},${f1(sy + len * 0.3)} ${f1(sx * (1.1 + r() * 0.4))},${f1(sy + len * 0.7)} ${f1(sx * (1 + r() * 0.6) + (r() - 0.5) * 200)},${f1(sy + len)}" stroke="${BL}" stroke-width="${f1(10 + r() * 22)}" fill="none" stroke-linecap="round"/>`; }
    for (let k = 0; k < 9; k++) { const sx = -200 + k * 50; if (Math.abs(sx) < 160) continue; g += `<path d="M${sx},-280C${sx + 20},-100 ${sx - 30},60 ${sx + (k % 2 ? 40 : -40)},320" stroke="${BL}" stroke-width="${12 + (k % 3) * 6}" fill="none" stroke-linecap="round"/>`; }
    g += `<path d="M-150,90Q-120,150 -70,170M150,90Q120,150 70,170M-14,40Q-6,100 -20,120M14,40Q6,100 20,120" stroke="#1e2a22" stroke-width="7" fill="none" stroke-linecap="round"/>`;
    return `<g ${id ? `id="${id}"` : ""}><g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${g}</g></g>`;
  }

  // ---------------- forest edge: the loner's house and fence inside kok2 ----------------
  const kok = Sets.kok2;
  Sets.kok2 = function (L, o = {}) {
    kok(L, o);
    if (o.house) { const [hx, hs] = o.house; put(L.set, Pop2.house2(hx, (o.ground ?? 1320) + 20, hs, { time: o.time === "night" ? "night" : "day", under: o.under })); }
    if (o.fence) { const [x0, n, y] = o.fence; put(o.fenceFront ? L.glow : L.set, fence(x0, n, y ?? (o.ground ?? 1320) + 60, o.time === "night")); }
  };
  function fence(x0, n = 14, G = 1380, night = false) {
    return `<g>${Array.from({ length: n }, (_, k) => `<rect x="${x0 + k * 62}" y="${G - 220 + (k % 3) * 8}" width="16" height="${226 - (k % 3) * 8}" rx="6" fill="${night ? "#1a1410" : k % 2 ? "#a88a5a" : "#b89a64"}" stroke="#3a2a1a" stroke-width="2"/>`).join("")}
      <path d="M${x0 - 20},${G - 170}H${x0 + n * 62}M${x0 - 20},${G - 80}H${x0 + n * 62}" stroke="${night ? "#1a1410" : "#7a5e34"}" stroke-width="9"/></g>`;
  }

  Object.assign(Sets, { clock2, legend2, potTop, testsTop, potX, printsTop, sign2 });
  Object.assign(Pop2, { pobFace, foot, PROP, fence, mudPrint, trail });
})();
