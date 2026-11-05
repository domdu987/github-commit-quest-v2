// ---------- ทางกลับบ้าน · EP pieces (load after war2.js) ----------
//   Sets.draft(L, o)                 insert: the conscription draw — a clear box of folded black/red cards on a table, a hand lifting the red one (#id-hand)
//   War.rocket(layer, x, y, s, id)   the lure: an old brass rocket head stuck in the dirt, its band glinting (#id-gl)
//   War.lane(tl, layer, pts, t0, dur) the clearance lane: white marker sticks with red-white tape popping in along pts, the tape drawing on
//   War.runLine(tl, layer, a, b, t0, dur, o)  the dotted run line from a to b, crossed out ✗ (and a red danger zone ring at b)
//   War.column(tl, L, x, y, t0, dur, o) the dust column still hanging in the sky (billows, slowly drifting)
//   WarUI.steps(tl, layer, t0, items, o)  a row of coin pills popping at their own times: [{ icon, text, at }]
//   WarUI.endCard(tl, layer, t0, dur, o)   the red mine-danger triangle on a post in the grass + the pinned note for the next EP
//   Rig.CAST.eod                     the clearance team: tan blast vest, visor helmet
(function () {
  const INK = "#2a2420", f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const O = (w = 4, c = INK) => `stroke="${c}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  let seq = 0; const nid = () => "wz" + (seq++);
  const blob = Pop2.blob;
  Sets.DEFS += `
    <linearGradient id="wzWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8d8b0"/><stop offset="1" stop-color="#c8b088"/></linearGradient>
    <linearGradient id="wzTable" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6a42"/><stop offset="1" stop-color="#6a4428"/></linearGradient>
    <linearGradient id="wzBrass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6a2a"/><stop offset=".35" stop-color="#f2d27a"/><stop offset=".6" stop-color="#c8a04a"/><stop offset="1" stop-color="#6a4a1a"/></linearGradient>
    <linearGradient id="wzOD" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a5430"/><stop offset=".4" stop-color="#7a8448"/><stop offset="1" stop-color="#3a4224"/></linearGradient>
    <linearGradient id="wzSign" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a46"/><stop offset="1" stop-color="#c8281e"/></linearGradient>`;

  // ---------------- the draw (insert) ----------------
  Sets.draft = (L, o = {}) => {
    const id = o.id || "df", r = mk(o.seed || 5);
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="url(#wzWall)"/>`);
    // the hall behind, out of focus: a long table of officials, a fan, windows with light
    let far = ""; for (let k = 0; k < 4; k++) far += `<rect x="${-200 + k * 380}" y="300" width="220" height="380" rx="10" fill="#fff6dc" opacity=".8"/><rect x="${-190 + k * 380}" y="310" width="200" height="360" fill="#bfe0f0" opacity=".5"/>`;
    far += `<rect x="-400" y="820" width="1900" height="140" fill="#6a4a30"/>`;
    for (let k = 0; k < 7; k++) far += `<g transform="translate(${-150 + k * 210},780)"><circle cy="-70" r="46" fill="#3a2a22"/><path d="M-70,40Q-60,-30 0,-34Q60,-30 70,40Z" fill="${k % 2 ? "#e8e4dc" : "#6a7a46"}"/></g>`;
    put(L.far, far);
    put(L.set, `<rect x="-1300" y="1260" width="3700" height="1500" fill="url(#wzTable)"/><path d="M-1300,1262H2400" stroke="#c89a6a" stroke-width="8"/>
      ${Array.from({ length: 14 }, (_, k) => `<path d="M-1300,${1320 + k * 50}H2400" stroke="#5a3a20" stroke-width="2" opacity=".35"/>`).join("")}
      <g transform="translate(420,1290)"><path d="M-260,0V-330H260V0Z" fill="#dff2ff" fill-opacity=".35" ${O(5, "#6a8aa0")}/><path d="M-260,-330L-200,-380H320L260,-330Z" fill="#eaf6ff" fill-opacity=".5" ${O(4, "#6a8aa0")}/>
        <path d="M260,0L320,-50V-380L260,-330Z" fill="#cfe6f4" fill-opacity=".45" ${O(4, "#6a8aa0")}/>
        ${Array.from({ length: 26 }, () => { const x = -230 + r() * 450, y = -20 - r() * 160, a = (r() - 0.5) * 60, red = r() < 0.3; return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${f1(a)})"><path d="M-30,-14H30V14H-30Z" fill="${red ? "#d8342a" : "#2a2a2e"}" ${O(2)}/><path d="M-30,0H30" stroke="${red ? "#ff8a7a" : "#5a5a60"}" stroke-width="2"/></g>`; }).join("")}
        <path d="M-240,-310V-30" stroke="#fff" stroke-width="8" opacity=".5"/><path d="M-80,-335H80" stroke="#6a8aa0" stroke-width="10" stroke-linecap="round"/></g>`);
    // the hand: a white shirt cuff, fingers pinching the red card (lifted in fx)
    put(L.act, `<g transform="translate(470,1060)"><g id="${id}-hand">
      <path d="M150,420L60,90Q56,60 80,52L130,40Q160,40 170,70L250,420Z" fill="#f4f2ec" ${O(4)}/><path d="M66,96L150,72" stroke="#c8c4bc" stroke-width="10"/>
      <path d="M70,60Q40,40 20,10Q10,-12 30,-18Q46,-20 60,0Q66,-30 84,-30Q102,-28 100,0Q118,-14 132,-2Q140,14 128,40Q110,70 70,60Z" fill="#c8946a" ${O(4)}/>
      <g transform="translate(20,-30) rotate(-12)"><g id="${id}-card"><path d="M-80,-50H80V50H-80Z" fill="url(#wzSign)" ${O(4)}/><path d="M-80,0H80" stroke="#ff9a8a" stroke-width="3"/><path d="M-70,-40H70" stroke="#fff" stroke-width="5" opacity=".5"/></g></g>
      <path d="M36,-6Q22,-18 26,-30" stroke="${INK}" stroke-width="3" fill="none"/></g></g>`);
  };

  // ---------------- the lure ----------------
  War.rocket = (layer, x, y, s = 1, id = nid()) => put(layer, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}">
    <ellipse cx="30" cy="6" rx="110" ry="18" fill="#1a1a10" opacity=".3"/><path d="M-70,10Q-40,-16 0,-12Q50,-14 80,10Q40,24 0,22Q-40,24 -70,10Z" fill="#7a5a38"/>
    <g transform="rotate(24)"><path d="M-26,0V-150Q-26,-230 0,-270Q26,-230 26,-150V0Z" fill="url(#wzOD)" ${O(4)}/><rect x="-28" y="-150" width="56" height="34" fill="url(#wzBrass)" ${O(3)}/>
      <path d="M-26,-60H26" stroke="#2a2a1a" stroke-width="3"/><path d="M-14,-250Q-10,-200 -12,-160" stroke="#c8d0a0" stroke-width="5" opacity=".5" fill="none"/>
      <g transform="translate(-6,-136)"><g id="${id}-gl" opacity="0"><circle r="24" fill="url(#wyStar)"/><path d="M0,-20L3,-3L20,0L3,3L0,20L-3,3L-20,0L-3,-3Z" fill="#fff"/></g></g></g>
    <path d="M-60,4q20,-14 40,-6M30,0q20,-10 44,2" stroke="#5a4028" stroke-width="5" fill="none"/></g></g>`);
  War.sparkle = (tl, sel, t0, dur, period = 0.9) => tl.fromTo(sel, { opacity: 0, scale: 0.3, rotation: 0, transformOrigin: "50% 50%" }, { keyframes: [{ opacity: 1, scale: 1.2, rotation: 45, duration: 0.15 }, { opacity: 0, scale: 0.3, rotation: 90, duration: 0.3 }, { opacity: 0, duration: period - 0.45 }], repeat: Math.ceil(dur / period), immediateRender: false }, t0);

  // ---------------- the clearance lane ----------------
  War.lane = (tl, layer, pts, t0, dur, o = {}) => {
    const id = nid();
    let g = "", d = `M${pts[0][0]},${pts[0][1]}`;
    pts.forEach(([x, y], k) => { if (k) d += `L${x},${y}`; g += `<g transform="translate(${x},${y}) scale(${o.s ?? 1})"><g id="${id}-p${k}" opacity="0"><path d="M0,0V-110" stroke="#f6f2ea" stroke-width="9" ${""}/><path d="M0,0V-110" stroke="${INK}" stroke-width="2" fill="none" opacity=".6"/><path d="M-5,-96h10M-5,-70h10" stroke="#d8342a" stroke-width="6"/></g></g>`; });
    const len = pts.reduce((a, p, k) => (k ? a + Math.hypot(p[0] - pts[k - 1][0], p[1] - pts[k - 1][1]) : 0), 0);
    put(layer, `<g><path id="${id}-t" d="${d}" transform="translate(0,-84)" stroke="#d8342a" stroke-width="5" fill="none" stroke-dasharray="${f1(len)} ${f1(len)}" stroke-dashoffset="${f1(len)}" opacity="0"/>${g}</g>`);
    pts.forEach((_, k) => tl.fromTo(`#${id}-p${k}`, { opacity: 0, scaleY: 0.2, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, transformOrigin: "50% 100%", duration: 0.25, ease: "back.out(2.5)", immediateRender: false }, t0 + (k / pts.length) * dur * 0.8));
    tl.fromTo(`#${id}-t`, { opacity: 1, strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur * 0.85, ease: "none", immediateRender: false }, t0);
  };

  // ---------------- the run line, crossed out ----------------
  War.runLine = (tl, layer, a, b, t0, dur, o = {}) => {
    const id = nid(), mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 - (o.arc ?? 80);
    put(layer, `<g>
      <g transform="translate(${b[0]},${b[1]})"><g id="${id}-z" opacity="0"><ellipse rx="${o.zr ?? 230}" ry="${(o.zr ?? 230) * 0.32}" fill="#e2382e" fill-opacity=".18" stroke="#e2382e" stroke-width="6" stroke-dasharray="20 12"/></g></g>
      <path id="${id}-l" d="M${a[0]},${a[1]}Q${mx},${my} ${b[0]},${b[1]}" stroke="#fff" stroke-width="10" fill="none" stroke-dasharray="4 26" stroke-linecap="round" opacity="0"/>
      <g transform="translate(${mx},${my + (o.arc ?? 80) / 2})"><g id="${id}-x" opacity="0"><circle r="66" fill="#e2382e" stroke="#fff" stroke-width="8"/><path d="M-26,-26L26,26M26,-26L-26,26" stroke="#fff" stroke-width="14" stroke-linecap="round"/></g></g></g>`);
    tl.fromTo(`#${id}-z`, { opacity: 0, scale: 0.5, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.4, ease: "back.out(2)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-z`, { scale: 1 }, { scale: 1.06, transformOrigin: "50% 50%", duration: 0.45, repeat: Math.ceil(dur / 0.45), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.4);
    tl.fromTo(`#${id}-l`, { opacity: 1, strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: dur, ease: "none", immediateRender: false }, t0 + 0.2);
    tl.fromTo(`#${id}-x`, { opacity: 0, scale: 2.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.6)", immediateRender: false }, t0 + (o.xAt ?? 0.8));
    tl.fromTo(`#${id}-x`, { rotation: -16 }, { rotation: 0, transformOrigin: "50% 50%", duration: 0.5, ease: "elastic.out(1.4,0.3)", immediateRender: false }, t0 + (o.xAt ?? 0.8) + 0.3);
    RabFX.flash(tl, t0 + (o.xAt ?? 0.8) + 0.05, "#ff2a1a", 0.22);
  };

  // ---------------- the dust column still hanging ----------------
  War.column = (tl, L, x, y, t0, dur, o = {}) => {
    const id = nid(), r = mk(o.seed || 21), s = o.s ?? 1;
    let g = ""; for (let k = 0; k < 10; k++) { const px = (r() - 0.5) * 120 + k * 14, py = -k * 70, pr = 70 + k * 6 + r() * 30;
      g += `<path d="${blob(px + 8, py + 10, pr, r, 9)}" fill="${o.dusk ? "#6a4a48" : "#7a5e40"}" opacity=".85"/><path d="${blob(px, py, pr * 0.9, r, 9)}" fill="${o.dusk ? "#c08a70" : "#b0906a"}" opacity=".9"/><path d="${blob(px - pr * 0.25, py - pr * 0.25, pr * 0.45, r, 8)}" fill="${o.dusk ? "#f0b890" : "#dcc4a0"}" opacity=".8"/>`; }
    put(o.layer || L.mid, `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}">${g}</g></g>`);
    tl.fromTo(`#${id}`, { x: 0, y: 0, skewX: 0 }, { x: 70, y: -30, skewX: -8, duration: dur, ease: "none", immediateRender: false }, t0);
  };

  // ---------------- step pills ----------------
  WarUI.steps = (tl, layer, t0, items, o = {}) => {
    const id = nid(), Y = o.y ?? 300, n = items.length, W = o.w ?? 230, gap = o.gap ?? 16, x0 = 540 - (n * W + (n - 1) * gap) / 2;
    put(layer, items.map((it, k) => `<g transform="translate(${x0 + k * (W + gap) + W / 2},${Y})"><g id="${id}-${k}" opacity="0">
      <rect x="${-W / 2}" y="-70" width="${W}" height="190" rx="34" fill="#3a2a1a" opacity=".3" transform="translate(5,9)"/><rect x="${-W / 2}" y="-70" width="${W}" height="190" rx="34" fill="#fffaf0" ${O(4.5)}/>
      <g transform="translate(-60,-120)">${War.coin(it.icon, 0, 0, 1, `${id}-c${k}`)}</g>
      <text y="${it.text.length > 9 ? 84 : 92}" font-family="Kanit" font-weight="900" font-size="${it.text.length > 9 ? 32 : 38}" fill="${it.red ? "#8a1a12" : "#2a2420"}" text-anchor="middle">${it.text}</text></g></g>`).join(""));
    items.forEach((it, k) => { tl.set(`#${id}-${k}`, { opacity: 0 }, 0);
      tl.fromTo(`#${id}-${k}`, { opacity: 0, y: 60, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, y: 0, scale: 1, transformOrigin: "50% 50%", duration: 0.45, ease: "back.out(2.2)", immediateRender: false }, t0 + it.at);
      tl.fromTo(`#${id}-${k}`, { y: 0 }, { y: -8, duration: 0.8, repeat: Math.ceil((o.dur ?? 6) / 0.8), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + it.at + 0.5);
      const el = document.getElementById(`${id}-c${k}`); QkUI.iconPop(tl, el, t0 + it.at + 0.1); RabFX.life(tl, el, t0 + it.at + 0.6, o.dur ?? 6);
      if (o.out) tl.to(`#${id}-${k}`, { opacity: 0, duration: 0.2 }, t0 + o.out); });
  };

  // ---------------- end card ----------------
  WarUI.endCard = (tl, layer, t0, dur, o = {}) => {
    const id = nid();
    put(layer, `<g transform="translate(540,700)"><g id="${id}-b"><rect x="-16" y="40" width="32" height="1000" fill="#6a4a30" ${O(4)}/>
      <path d="M0,-330L300,190H-300Z" fill="#fff" ${O(6)}/><path d="M0,-280L254,160H-254Z" fill="url(#wzSign)" ${O(4)}/>
      <text y="30" font-family="Kanit" font-weight="900" font-size="78" fill="#fff" text-anchor="middle">อันตราย</text><text y="120" font-family="Kanit" font-weight="900" font-size="56" fill="#fff" text-anchor="middle">ทุ่นระเบิด</text>
      <path d="M-60,-150L60,-60M60,-150L-60,-60" stroke="#fff" stroke-width="22" stroke-linecap="round"/></g>
      <g transform="translate(40,300) rotate(3)"><g id="${id}-n"><rect x="-300" y="0" width="600" height="${o.next ? 120 + o.next.length * 62 : 150}" fill="#fdf6d8" ${O(3)}/><circle cx="0" cy="16" r="11" fill="#c8282a" ${O(2)}/>
        <text x="0" y="78" font-family="Kanit" font-weight="900" font-size="46" fill="#8a1a12" text-anchor="middle">${o.ep || ""}</text>
        ${(o.next || []).map((t, k) => `<text x="0" y="${146 + k * 60}" font-family="Mali" font-weight="700" font-size="38" fill="#3a3430" text-anchor="middle">${t}</text>`).join("")}</g></g></g>`);
    tl.fromTo(`#${id}-b`, { rotation: -6, y: -60, opacity: 0, transformOrigin: "50% 100%" }, { rotation: 0, y: 0, opacity: 1, transformOrigin: "50% 100%", duration: 0.6, ease: "elastic.out(1,0.5)", immediateRender: false }, t0);
    tl.fromTo(`#${id}-b`, { rotation: -1 }, { rotation: 1, transformOrigin: "50% 100%", duration: 1.2, repeat: Math.ceil(dur / 1.2), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 0.6);
    tl.fromTo(`#${id}-n`, { opacity: 0, y: 80, rotation: 10, transformOrigin: "50% 0%" }, { opacity: 1, y: 0, rotation: 0, transformOrigin: "50% 0%", duration: 0.5, ease: "back.out(2)", immediateRender: false }, t0 + 0.5);
    tl.fromTo(`#${id}-n`, { rotation: -1.5 }, { rotation: 1.5, transformOrigin: "50% 0%", duration: 1.0, repeat: Math.ceil(dur / 1.0), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + 1.0);
  };

  // ---------------- cast: the clearance team ----------------
  const C = Rig.CAST, base = C.tao.v2;
  const visor = (ctx) => `<path d="M-60,-548C-64,-630 -22,-654 8,-652C44,-650 70,-624 64,-548Q2,-562 -60,-548Z" fill="#c8b07a" stroke="#3a2622" stroke-width="3"/>
    <path d="M-50,-560Q4,-578 62,-560L58,-500Q4,-486 -46,-500Z" fill="#9ad0e8" fill-opacity=".45" stroke="#3a2622" stroke-width="2.6"/><path d="M-36,-552Q0,-566 30,-556" stroke="#fff" stroke-width="5" opacity=".6" fill="none"/>`;
  C.eod = { v2: { ...base, skin: "#b07a52", hair: { ...base.hair, front: visor }, top: { kind: "shirt", c: "#b8a070", sleeve: "long", neck: "collar", collar: "#a08a5a", button: "#7a6a40", trim: "#a08a5a" },
    print: `<path d="M-58,-470H58V-330H-58Z" fill="#8a7a4a" stroke="#3a2622" stroke-width="2.6"/><path d="M-58,-430H58M-58,-390H58M-58,-350H58" stroke="#6a5a34" stroke-width="3"/><rect x="-30" y="-460" width="60" height="18" fill="#3a6aa0" stroke="#3a2622" stroke-width="2"/>`,
    extra: "", bottom: { kind: "trousers", c: "#a8905e" } } };

  // ---------------- EP.2 pieces ----------------
  //   War.rock(layer, x, y, s) a big lit boulder · War.ditch(layer, x, y, w) a trench lower than the ground · War.crossFlag(layer, x, y, s, id)
  //   the red-cross flag on a pole (it waves: #id-fl) · War.bandage(tl, layer, x, y, t0, dur, s) a white bandage winding round · War.gap(tl, layer,
  //   x, y1, y2, t0, dur, label) a measuring bracket between the bullet line and the helmet · Sets.parcelTop(L, o) insert: the open box from above,
  //   binoculars (#id-bi) and the folded note (#id-note) that opens · Rig.CAST.medic, Rig.CAST.enemyHurt
  War.rock = (layer, x, y, s = 1) => put(layer, `<g transform="translate(${x},${y}) scale(${s})"><ellipse cx="60" cy="6" rx="210" ry="26" fill="#1a1a10" opacity=".3"/>
    <path d="M-170,0Q-180,-120 -90,-180Q20,-230 120,-170Q190,-110 170,0Z" fill="#8a9098" ${O(5)}/><path d="M60,-190Q150,-150 165,-20L170,0H90Q120,-100 60,-190Z" fill="#5e646c" opacity=".7"/>
    <path d="M-140,-90Q-110,-160 -40,-190" stroke="#d0d6dc" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M-60,-60l30,-20M40,-120l20,24" stroke="#4a5058" stroke-width="5"/></g>`);
  War.ditch = (layer, x, y, w = 520) => put(layer, `<g transform="translate(${x},${y})"><path d="M${-w / 2},0Q${-w / 2 + 40},70 0,80Q${w / 2 - 40},70 ${w / 2},0Z" fill="#3e2c1c" ${O(4)}/>
    <path d="M${-w / 2 + 30},10Q0,40 ${w / 2 - 30},10" stroke="#6a4a30" stroke-width="8" fill="none"/><path d="M${-w / 2 - 30},0Q0,-26 ${w / 2 + 30},0" stroke="#8a6440" stroke-width="16" fill="none" stroke-linecap="round"/></g>`);
  War.crossFlag = (layer, x, y, s = 1, id = nid()) => put(layer, `<g transform="translate(${x},${y}) scale(${s})"><path d="M0,0V-520" stroke="#6a5a4a" stroke-width="12" stroke-linecap="round"/>
    <g transform="translate(6,-510)"><g id="${id}-fl"><path d="M0,0Q90,-20 180,0V130Q90,110 0,130Z" fill="#fbfbf8" ${O(4)}/><path d="M70,25H110V55H140V85H110V115H70V85H40V55H70Z" fill="#e2382e"/></g></g></g>`);
  War.wave = (tl, sel, t0, dur) => tl.fromTo(sel, { skewY: -4, scaleX: 0.96, transformOrigin: "0% 50%" }, { skewY: 4, scaleX: 1.02, transformOrigin: "0% 50%", duration: 0.6, repeat: Math.ceil(dur / 0.6), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0);
  War.bandage = (tl, layer, x, y, t0, dur, s = 1) => { const id = nid();
    put(layer, `<g transform="translate(${x},${y}) scale(${s})">${[0, 1, 2, 3].map((k) => `<path id="${id}-${k}" d="M-36,${-30 + k * 18}Q0,${-42 + k * 18} 36,${-30 + k * 18}" stroke="#fdfdfa" stroke-width="16" fill="none" stroke-linecap="round" stroke-dasharray="90 90" stroke-dashoffset="90"/>`).join("")}</g>`);
    [0, 1, 2, 3].forEach((k) => tl.fromTo(`#${id}-${k}`, { strokeDashoffset: 90 }, { strokeDashoffset: 0, duration: dur / 4, ease: "power1.inOut", immediateRender: false }, t0 + (k * dur) / 4)); };
  War.gap = (tl, layer, x, y1, y2, t0, dur, label = "ไม่กี่นิ้ว") => { const id = nid();
    put(layer, `<g id="${id}" opacity="0"><path d="M${x},${y1}V${y2}M${x - 18},${y1}H${x + 18}M${x - 18},${y2}H${x + 18}" stroke="#ffd23a" stroke-width="6"/>
      <g transform="translate(${x + 30},${(y1 + y2) / 2 + 14})"><rect x="0" y="-38" width="${label.length * 30 + 30}" height="58" rx="29" fill="#fffaf0" ${O(4)}/><text x="${(label.length * 30 + 30) / 2}" y="2" font-family="Kanit" font-weight="900" font-size="36" fill="#8a1a12" text-anchor="middle">${label}</text></g></g>`);
    tl.set(`#${id}`, { opacity: 0 }, 0); tl.fromTo(`#${id}`, { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, t0); };
  Sets.parcelTop = (L, o = {}) => { const id = o.id || "pt";
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#8a6a48"/>${Array.from({ length: 20 }, (_, k) => `<path d="M-1300,${-900 + k * 200}H2400" stroke="#6a4a30" stroke-width="6" opacity=".5"/>`).join("")}`);
    put(L.set, `<g transform="translate(540,1000)"><rect x="-380" y="-300" width="760" height="600" fill="#3a2a1a" opacity=".35" transform="translate(16,22)"/>
      <rect x="-380" y="-300" width="760" height="600" fill="#c8a06a" ${O(6)}/><rect x="-340" y="-260" width="680" height="520" fill="#7a5a3a" ${O(4)}/>
      <path d="M-380,-300L-460,-420H-80L0,-300Z" fill="#d8b47a" ${O(5)}/><path d="M380,-300L460,-420H80L0,-300Z" fill="#d8b47a" ${O(5)}/>
      <g id="${id}-bi"><g transform="translate(-120,40) rotate(-12)"><circle cx="-80" cy="0" r="90" fill="#2a3038" ${O(5)}/><circle cx="90" cy="0" r="90" fill="#2a3038" ${O(5)}/><rect x="-40" y="-110" width="90" height="80" rx="16" fill="#3a424a" ${O(4)}/>
        <circle cx="-80" cy="0" r="58" fill="#5aa8d8"/><circle cx="90" cy="0" r="58" fill="#5aa8d8"/><circle cx="-96" cy="-16" r="18" fill="#fff" opacity=".8"/><circle cx="74" cy="-16" r="18" fill="#fff" opacity=".8"/>
        <path d="M-150,-20q-20,60 10,100" stroke="#5a646e" stroke-width="10" fill="none"/></g></g>
      <g transform="translate(170,-80) rotate(8)"><g id="${id}-note"><rect x="-150" y="-110" width="300" height="220" fill="#fbf6e8" ${O(4)}/>${[0, 1, 2, 3].map((k) => `<path d="M-120,${-60 + k * 44}H120" stroke="#c8d0e0" stroke-width="3"/>`).join("")}
        <g id="${id}-ink" opacity="0"><text x="0" y="-40" font-family="Mali" font-weight="700" font-size="30" fill="#2a3a6a" text-anchor="middle">ผมเห็นพวกคุณ</text><text x="0" y="4" font-family="Mali" font-weight="700" font-size="30" fill="#2a3a6a" text-anchor="middle">ตั้งแต่วันแรก…</text>
        <text x="0" y="56" font-family="Mali" font-weight="700" font-size="32" fill="#8a1a12" text-anchor="middle">แต่ผมเลือกไม่ยิง</text></g></g></g></g>`); };
  const C2 = Rig.CAST;
  C2.medic = { v2: { ...C2.eod.v2, skin: "#c8946a", hair: { ...C2.tao.v2.hair, front: (ctx) => `<path d="M-58,-552C-62,-628 -22,-650 6,-648C40,-646 66,-622 60,-552Q0,-566 -58,-552Z" fill="#f2f2ee" stroke="#3a2622" stroke-width="3"/><path d="M-8,-626h20v14h14v20h-14v14h-20v-14h-14v-20h14z" fill="#e2382e"/>` },
    top: { kind: "shirt", c: "#e8e6e0", sleeve: "long", neck: "collar", collar: "#d0cec8", button: "#9a9890", trim: "#d0cec8" },
    print: `<g transform="translate(-50,-440)"><rect x="-16" y="-14" width="32" height="28" fill="#fff" stroke="#3a2622" stroke-width="2"/><path d="M-4,-10h8v6h6v8h-6v6h-8v-6h-6v-8h6z" fill="#e2382e"/></g>`, bottom: { kind: "trousers", c: "#7a8088" } } };
  C2.enemyHurt = { v2: { ...C2.enemy.v2, face: `<path d="M24,-566l12,-4" stroke="#e8c8a8" stroke-width="3" opacity=".8"/><path d="M-30,-520q4,-2 8,0" stroke="#8a6a50" stroke-width="2" opacity=".5"/>` } };
})();
