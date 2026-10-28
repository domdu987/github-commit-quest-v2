// "ผีแม่ม่าย" — motion graphics drawn to a professional standard (the user: "icon ต่างๆทำให้ดีกว่านี้ และให้เคลื่อนไหวสวยๆ แบบมืออาชีพ").
// One design language: ink outline 4–5, flat fills, one shade layer and one highlight, soft drop shadows, Kanit; everything enters
// with easing (back / elastic / bounce), staggered, then keeps a small secondary motion (beats, quivers, taps, traces).
//   Sets.flip3(L, o)   the อสม. flipchart (a printed ภาพพลิก on an easel at the sala). Ids from o.id:
//                      rows #id-rA (normal) #id-rB (ใหลตาย); hearts #id-A-hb / #id-B-hb (+ #id-B-q quiver wrapper), drops #id-A-d0..2,
//                      sparks #id-B-z0..5, the conduction pulse #id-A-pulse, ECG sweeps #id-A-sw #id-B-sw with dots #id-A-dot #id-B-dot,
//                      pills #id-pA #id-pB, text lines #id-tA0.. #id-tB0.., highlight #id-hl, stamp #id-stamp
//   MmUI.flipAnim(tl, id, t0, o)  plays it: page settles, row A (pulse → squeeze → blood up the aorta, ECG beats in sync, 3 beats),
//                      row B (short-circuit sparks, quiver, no blood, VF trace), the highlight, the stamp. o.b = when row B starts (s after t0)
//   MmUI.rule(tl, layer, t0, dur, o)  Bua's rule card on its lanyard: o.active (0..2), o.done [i…], o.y (card top, screen), o.s
//   MmUI.icon(k, x, y, s, id)    the three rule icons in their badges (k 0..2) · MmUI.iconAnim(tl, k, id, t0, dur) their idle motion
//   MmUI.source(tl, layer, t0, dur, o)  the source chip, o.text, o.y
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const { mk } = Pop2;
  const INK = "#26201c";
  const C = { red: "#e2382e", redD: "#a81e18", heart: "#ec5a50", heartD: "#b8322c", heartL: "#ffb0a6", blue: "#2f6fd0", blueL: "#d6e6fb", vein: "#5a6ad8",
    green: "#2fa864", greenD: "#1e7a48", greenL: "#e4f6ea", yellow: "#ffd23a", yellowL: "#fff1b0", slate: "#1e2630", paper: "#fdfaf2", muted: "#8a8f98", skin: "#e6ae80" };
  const O = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  Sets.DEFS += `
    <linearGradient id="muHead" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2fa864"/><stop offset="1" stop-color="#1e8a52"/></linearGradient>
    <linearGradient id="muPage" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf8"/><stop offset="1" stop-color="#f4efe2"/></linearGradient>
    <radialGradient id="muHeart" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ff8a7a"/><stop offset=".55" stop-color="#ec5a50"/><stop offset="1" stop-color="#c83a32"/></radialGradient>
    <linearGradient id="muAorta" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f2685c"/><stop offset="1" stop-color="#c8382e"/></linearGradient>
    <linearGradient id="muVein" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a8ae8"/><stop offset="1" stop-color="#4a58c0"/></linearGradient>
    <linearGradient id="muMon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26303c"/><stop offset="1" stop-color="#151b22"/></linearGradient>
    <radialGradient id="muSpark"><stop offset="0" stop-color="#fff8c8" stop-opacity=".95"/><stop offset=".4" stop-color="#ffd23a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd23a" stop-opacity="0"/></radialGradient>
    <radialGradient id="muDotG"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#9affc0" stop-opacity=".9"/><stop offset="1" stop-color="#3aff8a" stop-opacity="0"/></radialGradient>
    <radialGradient id="muDotR"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#ffb0a0" stop-opacity=".9"/><stop offset="1" stop-color="#ff4a3a" stop-opacity="0"/></radialGradient>
    <filter id="muDrop" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="8"/><feOffset dy="10"/><feComponentTransfer><feFuncA type="linear" slope=".3"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="muGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>`;

  // ---------------- the heart (front view, cartoon-anatomical), centred on its body; ~300 wide, ~380 tall ----------------
  const BODY = "M-92,-62C-142,-58 -168,4 -150,64C-132,126 -54,170 34,196C64,160 136,92 148,22C158,-40 128,-90 70,-92C42,-94 12,-84 -8,-72C-38,-84 -68,-82 -92,-62Z";
  const tube = (d, w, fill) => `<path d="${d}" stroke="${INK}" stroke-width="${w + 9}" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="${fill}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
  const heart = (pre, o = {}) => {
    let g = "";
    // vessels behind the body: the vena cava on the patient's right, the aortic arch with its three branches, the pulmonary trunk in front
    g += tube("M-78,-56C-80,-100 -78,-140 -70,-176", 30, "#7484e0") + `<path d="M-84,-160V-120" stroke="#aab6ff" stroke-width="6" stroke-linecap="round" opacity=".6"/>`;
    g += tube("M24,-60C22,-120 24,-176 70,-188C108,-196 128,-160 120,-104", 40, "#e2483e") + `<path d="M16,-80C14,-130 22,-170 58,-182" stroke="#ff9a8a" stroke-width="8" fill="none" stroke-linecap="round" opacity=".55"/>`;
    g += [[52, -186, 44, -236], [78, -192, 82, -240], [104, -180, 120, -224]].map(([x0, y0, x1, y1]) => tube(`M${x0},${y0}L${x1},${y1}`, 14, "#e2483e")).join("");
    g += tube("M40,-58C24,-92 -4,-110 -30,-118", 30, "#6a5ad0") + tube("M-30,-118L-52,-112M-30,-118L-38,-142", 16, "#6a5ad0");
    // the body with its shade (lower right), highlight (upper left), the groove and coronary vessels
    g += `<path d="${BODY}" fill="url(#muHeart)" ${O(5)}/>`;
    g += `<defs><clipPath id="${pre}-cb"><path d="${BODY}"/></clipPath></defs><g clip-path="url(#${pre}-cb)"><path d="M40,-120C120,-40 120,120 10,240L240,240L240,-120Z" fill="${C.heartD}" opacity=".35"/></g>`;
    g += `<path d="M-120,10C-124,-30 -100,-52 -70,-54" stroke="#fff" stroke-width="12" fill="none" opacity=".45" stroke-linecap="round"/><circle cx="-112" cy="34" r="6" fill="#fff" opacity=".45"/>`;
    g += `<path d="M10,-70C0,10 10,100 30,186" stroke="${C.heartD}" stroke-width="5" fill="none" opacity=".8" stroke-linecap="round"/>`;
    g += `<path d="M6,-40C40,-30 80,-10 100,30M4,20C40,40 70,70 80,110M-6,-20C-40,-10 -80,10 -100,50" stroke="#d8443a" stroke-width="4" fill="none" opacity=".75" stroke-linecap="round"/>`;
    return g;
  };
  // the conduction path drawn on the heart (a faint wire) and the pulse that runs along it
  const WIRE = "M-86,-34C-60,-12 -30,4 -8,14C2,60 14,110 28,170";
  const WIRE2 = "M28,170C70,140 108,90 120,30M28,170C-30,150 -90,110 -116,60";
  // ECG traces in a W×H strip (centre line at H/2), beats at the given x positions
  const ecg = (W, H, beats) => {
    const c = H / 2; let d = `M0,${c}`, x = 0;
    beats.forEach((bx) => {
      d += `L${f1(bx - 46)},${c}Q${f1(bx - 38)},${c - 9} ${f1(bx - 30)},${c}L${f1(bx - 10)},${c}L${f1(bx - 5)},${c + 8}L${f1(bx)},${c - H * 0.42}L${f1(bx + 6)},${c + H * 0.22}L${f1(bx + 11)},${c}L${f1(bx + 34)},${c}Q${f1(bx + 48)},${c - 14} ${f1(bx + 62)},${c}`;
      x = bx + 62;
    });
    return d + `L${W},${c}`;
  };
  const vf = (W, H, seed) => {
    const r = mk(seed), c = H / 2; let d = `M0,${c}`;
    for (let x = 6; x <= W; x += 6) { const a = 0.18 + 0.22 * Math.abs(Math.sin(x / 70)), y = c + Math.sin(x / 9 + Math.sin(x / 23) * 2) * H * a + (r() - 0.5) * H * 0.12; d += `L${x},${f1(y)}`; }
    return d;
  };
  // a monitor strip: dark glass, a fine grid, the trace revealed by a sweep (#pre-sw) with a glowing head (#pre-dot)
  const monitor = (pre, x, y, W, H, trace, col, dot) => `<g transform="translate(${x},${y})"><rect x="-10" y="-10" width="${W + 20}" height="${H + 20}" rx="18" fill="url(#muMon)" ${O(4)}/>
    ${Array.from({ length: Math.floor(W / 24) }, (_, k) => `<path d="M${(k + 1) * 24},0V${H}" stroke="#2e4a3e" stroke-width="1" opacity=".55"/>`).join("")}${Array.from({ length: Math.floor(H / 24) }, (_, k) => `<path d="M0,${(k + 1) * 24}H${W}" stroke="#2e4a3e" stroke-width="1" opacity=".55"/>`).join("")}
    <defs><clipPath id="${pre}-clip"><rect id="${pre}-sw" x="0" y="-20" width="${W}" height="${H + 40}"/></clipPath></defs>
    <g clip-path="url(#${pre}-clip)"><path d="${trace}" stroke="${col}" stroke-width="10" fill="none" opacity=".25" stroke-linejoin="round"/><path id="${pre}-tr" d="${trace}" stroke="${col}" stroke-width="4.5" fill="none" stroke-linejoin="round" stroke-linecap="round"/></g>
    <g id="${pre}-dot" opacity="0"><circle r="16" fill="url(#${dot})"/></g>
    <path d="M14,12Q${W / 2},-2 ${W - 14},12" stroke="#fff" stroke-width="3" opacity=".12" fill="none"/></g>`;
  const pill = (x, y, text, fill, id) => { const w = Math.round(text.length * 23 + 64);
    return `<g transform="translate(${x + w / 2},${y})"><g id="${id}"><rect x="${-w / 2}" y="-30" width="${w}" height="60" rx="30" fill="${fill}" ${O(4)}/><text x="0" y="13" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="38" fill="#fff">${text}</text></g></g>`; };
  const bolt = (pts) => { const d = `M${pts.map(([x, y]) => `${x},${y}`).join("L")}`; return `<path d="${d}" stroke="#ffe066" stroke-width="22" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".35"/><path d="${d}" stroke="${C.yellow}" stroke-width="11" fill="none" stroke-linejoin="round" stroke-linecap="round"/><path d="${d}" stroke="#fffdf0" stroke-width="4.5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`; };
  const BOLTS = [[[-140, -20], [-104, 4], [-122, 26], [-80, 52], [-96, 72]], [[-50, -54], [-24, -26], [-44, -8], [-6, 18], [-26, 40]], [[30, -50], [64, -20], [40, -4], [80, 26], [62, 44]], [[-110, 100], [-70, 86], [-80, 116], [-34, 116]], [[40, 76], [80, 60], [72, 96], [118, 84]], [[-20, 130], [8, 108], [4, 146], [36, 140]]];

  // ---------------- the flipchart ----------------
  function flip3(L, o = {}) {
    const id = o.id || "fc", r = mk(o.seed || 81);
    // the sala behind, out of focus: roof, posts, people on plastic chairs
    put(L.sky, `<rect x="-1300" y="-900" width="3700" height="3900" fill="#eadfc4"/><rect x="-1300" y="1000" width="3700" height="2000" fill="#cbb48c"/>`);
    let f = `<path d="M-1300,-900H2400V100H-1300Z" fill="#8a5a3a"/><path d="M-1300,100H2400" stroke="#5a3420" stroke-width="30"/>`;
    for (let k = 0; k < 8; k++) f += `<rect x="${-900 + k * 420}" y="100" width="60" height="1400" fill="url(#p2Wood)"/>`;
    f += `<rect x="-1300" y="380" width="3700" height="560" fill="#bfe0f4" opacity=".55"/>`;
    for (let k = 0; k < 10; k++) { const x = -800 + k * 300 + r() * 80, y = 1420 + (k % 2) * 80; f += `<g transform="translate(${f1(x)},${y})"><rect x="-70" y="-10" width="140" height="120" rx="12" fill="${["#d83a3a", "#3a6ad8", "#e8b030"][k % 3]}" opacity=".85"/><ellipse cx="0" cy="-130" rx="56" ry="64" fill="#4a3a30"/><path d="M-90,-10Q-90,-80 0,-80Q90,-80 90,-10Z" fill="${["#f4f0e6", "#5a8a6a", "#c88a5a"][k % 3]}"/></g>`; }
    put(L.far, f);
    // the page: 940 wide, 1150 tall, top-left at (70, 240), the spiral binding along the top, easel legs behind
    const PX = o.x ?? 70, PY = o.y ?? 240, W = 940;
    let s = `<path d="M${PX + 120},${PY + 1100}L${PX + 40},${PY + 1800}M${PX + W - 120},${PY + 1100}L${PX + W - 40},${PY + 1800}" stroke="#7a5a3a" stroke-width="24" stroke-linecap="round"/>`;
    let p = `<rect x="10" y="16" width="${W}" height="1150" rx="14" fill="#000" opacity=".22"/><rect x="0" y="0" width="${W}" height="1150" rx="14" fill="url(#muPage)" ${O(3)}/>`;
    // header band: the อสม. badge, the title, the subtitle (S5: ไฟฟ้าลัดวงจรในหัวใจ)
    p += `<path d="M0,14Q0,0 14,0H${W - 14}Q${W},0 ${W},14V150H0Z" fill="url(#muHead)"/><circle cx="84" cy="76" r="50" fill="#fff" ${O(3)}/><path d="M74,46h20v20h20v20h-20v20h-20v-20h-20v-20h20z" fill="${C.green}" transform="translate(0,-6) scale(1) translate(0,0)"/>
      <text x="84" y="120" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="20" fill="${C.greenD}">อสม.</text>
      <text x="160" y="84" font-family="Kanit" font-weight="900" font-size="74" fill="#fff">ใหลตาย</text>
      <text x="160" y="132" font-family="Kanit" font-weight="600" font-size="34" fill="#e8ffe8">ไม่ใช่ผี… คือไฟฟ้าลัดวงจรในหัวใจ</text>`;
    // row A: the normal heart
    const row = (y, fill, stroke) => `<rect x="26" y="${y}" width="${W - 52}" height="470" rx="26" fill="${fill}" stroke="${stroke}" stroke-width="4"/>`;
    p += `<g id="${id}-rA">${row(170, "#f2fbf5", "#9ad8b2")}${pill(52, 216, "ปกติ", C.green, `${id}-pA`)}
      <g transform="translate(220,430) scale(.78)"><g id="${id}-A-hb">${heart(`${id}-A`)}
        <path d="${WIRE}" stroke="${C.yellow}" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/><path d="${WIRE2}" stroke="${C.yellow}" stroke-width="4" fill="none" opacity=".45" stroke-linecap="round"/>
        <path id="${id}-A-pulse" d="${WIRE}" stroke="#fffbe0" stroke-width="10" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray=".14 1" stroke-dashoffset=".14" filter="url(#muGlow)" opacity="0"/>
        <circle cx="-86" cy="-34" r="11" fill="${C.yellow}" ${O(3)}/></g>
        ${[0, 1, 2].map((k) => `<g id="${id}-A-d${k}" opacity="0"><path d="M0,-12C6,-4 10,2 10,7A10,10 0 1 1 -10,7C-10,2 -6,-4 0,-12Z" fill="${C.red}" ${O(3)}/></g>`).join("")}</g>
      <g id="${id}-tA0"><text x="500" y="310" font-family="Kanit" font-weight="800" font-size="46" fill="${INK}">หัวใจบีบตัว</text></g>
      <g id="${id}-tA1"><text x="500" y="370" font-family="Kanit" font-weight="600" font-size="38" fill="#3a4a40">ส่งเลือดไปทั้งตัว</text><path d="M500,392H820" stroke="${C.green}" stroke-width="5" stroke-linecap="round" opacity=".5"/></g>
      ${monitor(`${id}-A`, 470, 470, 410, 120, ecg(410, 120, [70, 205, 340]), "#4aff8a", "muDotG")}</g>`;
    // row B: ใหลตาย
    p += `<g id="${id}-rB">${row(660, "#fff3f1", "#f2a49c")}${pill(52, 706, "ใหลตาย", C.red, `${id}-pB`)}
      <g transform="translate(220,920) scale(.78)"><g id="${id}-B-q"><g id="${id}-B-hb">${heart(`${id}-B`)}</g>
        ${BOLTS.map((b, k) => `<g id="${id}-B-z${k}" opacity="0">${bolt(b)}</g>`).join("")}
        <g id="${id}-B-glow" opacity="0"><circle cx="-10" cy="40" r="160" fill="url(#muSpark)" style="mix-blend-mode:screen"/></g></g>
        <g id="${id}-B-x" opacity="0" transform="translate(70,-200)"><circle r="30" fill="#fff" ${O(4)}/><path d="M-12,-12L12,12M12,-12L-12,12" stroke="${C.red}" stroke-width="8" stroke-linecap="round"/></g></g>
      <g id="${id}-tB0"><path d="M500,756l-14,30h16l-10,26l30,-38h-17l11,-18z" fill="${C.yellow}" ${O(3)}/><text x="540" y="796" font-family="Kanit" font-weight="800" font-size="44" fill="${INK}">ไฟฟ้าลัดวงจร</text></g>
      <g id="${id}-tB1"><text x="500" y="856" font-family="Kanit" font-weight="700" font-size="40" fill="#5a3a36">หัวใจเต้นระริก</text></g>
      <g id="${id}-tB2"><g transform="translate(494,884)"><rect id="${id}-hl" x="0" y="0" width="360" height="56" rx="10" fill="${C.yellow}" opacity=".8"/></g><text x="504" y="926" font-family="Kanit" font-weight="900" font-size="44" fill="${C.redD}">ไม่บีบเลือดเลย</text></g>
      ${monitor(`${id}-B`, 470, 960, 410, 120, vf(410, 120, 7), "#ff5a4a", "muDotR")}</g>`;
    // the stamp (S5: ทำให้หัวใจเปรียบเสมือนหยุดเต้น)
    p += `<g transform="translate(470,1118) rotate(-5) scale(.92)"><g id="${id}-stamp" opacity="0"><rect x="-230" y="-44" width="460" height="88" rx="14" fill="#fff" fill-opacity=".85" stroke="${C.red}" stroke-width="7"/><rect x="-218" y="-32" width="436" height="64" rx="9" fill="none" stroke="${C.red}" stroke-width="3"/>
      <text x="0" y="16" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="44" fill="${C.red}" letter-spacing="1">เหมือนหัวใจหยุดเต้น</text></g></g>`;
    s += `<g transform="translate(${PX},${PY})"><g id="${id}-page">${p}${Array.from({ length: 18 }, (_, k) => `<path d="M${36 + k * 51},-16q-12,20 0,36" stroke="#5a5e64" stroke-width="6" fill="none"/>`).join("")}<rect x="0" y="-30" width="${W}" height="20" rx="6" fill="#3a3e44"/></g></g>`;
    put(L.set, s);
    put(L.glow, `<circle cx="260" cy="160" r="1200" fill="url(#kiLampGlow)" opacity=".16" style="mix-blend-mode:screen"/>`);
  }

  // the glowing head of a monitor trace rides the trace's height as the sweep moves along it
  function ride(tl, pre, t, dur, W) {
    const tr = document.getElementById(`${pre}-tr`), dot = document.getElementById(`${pre}-dot`), n = 300, L = tr.getTotalLength(), pts = [];
    for (let i = 0; i <= n; i++) { const q = tr.getPointAtLength((L * i) / n); pts.push([q.x, q.y]); }
    const yAt = (x) => { let b = pts[0]; for (const q of pts) if (Math.abs(q[0] - x) < Math.abs(b[0] - x)) b = q; return b[1]; };
    const pr = { p: 0 };
    tl.set(dot, { opacity: 1 }, t);
    tl.fromTo(pr, { p: 0 }, { p: 1, duration: dur, ease: "none", immediateRender: false, onUpdate: () => { const x = pr.p * W; dot.setAttribute("transform", `translate(${f1(x)},${f1(yAt(x))})`); } }, t);
    tl.set(dot, { opacity: 0 }, t + dur);
  }

  // ---------------- the flipchart's animation ----------------
  function flipAnim(tl, id, t0, o = {}) {
    const r = mk(o.seed || 17), b = o.b ?? 3.6, period = 0.8;
    // the page swings in on its spiral and settles
    tl.fromTo(`#${id}-page`, { rotation: -4, y: -30, svgOrigin: "470 -20" }, { rotation: 0, y: 0, duration: 1.1, ease: "elastic.out(1, 0.45)", immediateRender: false }, t0);
    // row A: pill, text, then three beats in step with the trace
    tl.fromTo(`#${id}-pA`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.25);
    [0, 1].forEach((k) => tl.fromTo(`#${id}-tA${k}`, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, t0 + 0.45 + k * 0.15));
    const sweepA = 2.6, sA = t0 + 0.5;
    tl.fromTo(`#${id}-A-sw`, { attr: { width: 0 } }, { attr: { width: 410 }, duration: sweepA, ease: "none", immediateRender: false }, sA);
    ride(tl, `${id}-A`, sA, sweepA, 410);
    // beats land where the trace's R waves are (x 70, 205, 340 of 410)
    [70, 205, 340].forEach((bx) => {
      const tb = sA + (bx / 410) * sweepA;
      tl.fromTo(`#${id}-A-pulse`, { opacity: 1, attr: { "stroke-dashoffset": 0.14 } }, { attr: { "stroke-dashoffset": -1 }, duration: 0.32, ease: "none", immediateRender: false }, tb - 0.3);
      tl.set(`#${id}-A-pulse`, { opacity: 0 }, tb + 0.02);
      tl.to(`#${id}-A-hb`, { scaleX: 0.93, scaleY: 0.9, svgOrigin: "0 30", duration: 0.12, ease: "power2.in" }, tb);
      tl.to(`#${id}-A-hb`, { scaleX: 1, scaleY: 1, svgOrigin: "0 30", duration: 0.42, ease: "back.out(3)" }, tb + 0.12);
      [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-A-d${k}`, { opacity: 0, x: 24, y: -70 },
        { keyframes: [{ opacity: 1, x: 24, y: -130, duration: 0.18 }, { x: 60 - k * 4, y: -196, duration: 0.18 }, { x: [48, 82, 116][k], y: -262, opacity: 0, duration: 0.22 }], ease: "power1.out", immediateRender: false }, tb + 0.06 + k * 0.05));
    });
    // row B: the short circuit
    const tB = t0 + b;
    tl.fromTo(`#${id}-pB`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, tB);
    [0, 1, 2].forEach((k) => tl.fromTo(`#${id}-tB${k}`, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, tB + 0.25 + k * 0.45));
    tl.fromTo(`#${id}-hl`, { scaleX: 0, svgOrigin: "0 0" }, { scaleX: 1, duration: 0.45, ease: "power2.inOut", immediateRender: false }, tB + 1.3);
    const sweepB = 2.6, sB = tB + 0.3, endB = sB + sweepB + (o.hold ?? 1.2);
    tl.fromTo(`#${id}-B-sw`, { attr: { width: 0 } }, { attr: { width: 410 }, duration: sweepB, ease: "none", immediateRender: false }, sB);
    ride(tl, `${id}-B`, sB, sweepB, 410);
    // sparks flicker on and off at random, the heart quivers (tiny, fast, never still), no blood leaves it
    for (let t = sB; t < endB; t += 0.07) {
      for (let k = 0; k < 6; k++) tl.set(`#${id}-B-z${k}`, { opacity: r() > 0.55 ? 1 : 0 }, t);
      tl.set(`#${id}-B-q`, { x: f1((r() - 0.5) * 7), y: f1((r() - 0.5) * 5), rotation: f1((r() - 0.5) * 3), svgOrigin: "0 30" }, t);
      tl.set(`#${id}-B-glow`, { opacity: f1(0.25 + r() * 0.5) }, t);
    }
    tl.set([0, 1, 2, 3, 4, 5].map((k) => `#${id}-B-z${k}`), { opacity: 0 }, endB);
    tl.set(`#${id}-B-q`, { x: 0, y: 0, rotation: 0, svgOrigin: "0 30" }, endB);
    tl.fromTo(`#${id}-B-x`, { opacity: 0, scale: 0.2, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(3)", immediateRender: false }, tB + 1.1);
    // the stamp slams down, the page shakes once
    const tS = o.stampAt != null ? t0 + o.stampAt : tB + 2.4;
    tl.fromTo(`#${id}-stamp`, { opacity: 0, scale: 2.4, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in", immediateRender: false }, tS);
    tl.fromTo(`#${id}-page`, { x: 0 }, { keyframes: [{ x: -6, duration: 0.04 }, { x: 5, duration: 0.04 }, { x: -3, duration: 0.04 }, { x: 0, duration: 0.05 }], immediateRender: false }, tS + 0.2);
  }

  // ---------------- the rule icons (100-unit box, in a badge of radius 60) ----------------
  const ICONS = [
    // 0 · หลับแล้วเกร็ง อย่าเกรงจะปลุก: asleep on his side under a blanket, shaking (red tremor marks); a hand on his shoulder taps him
    (p) => `<path d="M-52,30H52" stroke="#c8c0d8" stroke-width="5" stroke-linecap="round"/>
      <g id="${p}-body"><rect x="-50" y="2" width="34" height="24" rx="11" fill="#f2f0fa" ${O(4)}/><path d="M-20,4Q-12,-12 6,-12H40Q50,-12 50,0V26H-20Z" fill="#5a86c8" ${O(4)}/><path d="M2,-2Q22,6 46,-2" stroke="#3a64a8" stroke-width="3.5" fill="none"/>
        <circle cx="-30" cy="-2" r="15" fill="${C.skin}" ${O(4)}/><path d="M-45,-6Q-42,-20 -26,-18Q-17,-16 -16,-8Q-30,-14 -45,-6Z" fill="#2a1e18"/><path d="M-37,1h8" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M-39,-6l5,1" stroke="${INK}" stroke-width="2.5" stroke-linecap="round"/></g>
      <g id="${p}-shake">${[[-50, -28], [-12, -32], [56, -6]].map(([x, y], k) => `<path d="M${x},${y}q${k === 2 ? 6 : -6},6 0,12M${x + (k === 2 ? 8 : -8)},${y - 3}q${k === 2 ? 7 : -7},9 0,18" stroke="${C.red}" stroke-width="4" fill="none" stroke-linecap="round"/>`).join("")}</g>
      <g transform="translate(46,-56)"><g id="${p}-hand"><path d="M10,-16L-34,34" stroke="#e8a23a" stroke-width="18" stroke-linecap="round"/><path d="M10,-16L-34,34" stroke="${INK}" stroke-width="24" stroke-linecap="round" opacity=".12"/>
        <path d="M-50,30Q-56,44 -46,50Q-30,56 -24,46Q-20,36 -30,30Z" fill="${C.skin}" ${O(4)}/><path d="M-50,40h-6M-48,46h-6M-44,50l-4,4" stroke="${INK}" stroke-width="3" stroke-linecap="round"/></g></g>
      <path d="M-2,-46q8,-6 14,2M-6,-56q12,-10 24,2" stroke="${C.blue}" stroke-width="4" fill="none" stroke-linecap="round"/>`,
    // 1 · ปลุกไม่ตื่น ปั๊มให้ฟื้น: a person on their back, straight arms from above, hands stacked on the middle of the chest; 1669
    (p) => `<path d="M-54,34H54" stroke="#c8c0d8" stroke-width="5" stroke-linecap="round"/>
      <circle cx="-38" cy="16" r="13" fill="${C.skin}" ${O(4)}/><path d="M-50,10Q-46,-2 -34,2" stroke="#2a1e18" stroke-width="6" fill="none" stroke-linecap="round"/>
      <g id="${p}-chest"><path d="M-24,32V12Q-24,4 -14,4H40Q50,4 50,14V32Z" fill="#e2483e" ${O(4)}/><path d="M-6,8V30" stroke="#b8322c" stroke-width="3"/></g>
      <g id="${p}-press"><path d="M-6,-60V-8" stroke="#3a64a8" stroke-width="20" stroke-linecap="round"/><path d="M-6,-60V-8" stroke="${INK}" stroke-width="26" stroke-linecap="round" opacity=".12"/>
        <ellipse cx="-6" cy="-2" rx="17" ry="9" fill="${C.skin}" ${O(4)}/><ellipse cx="-6" cy="-10" rx="15" ry="8" fill="#f2c094" ${O(3.5)}/><path d="M-16,-12h20" stroke="#c88a5a" stroke-width="2.5"/></g>
      <g id="${p}-arr"><path d="M24,-52V-24M16,-32l8,8l8,-8" stroke="${C.blue}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      <g transform="translate(-34,-38) rotate(-10)"><rect x="-16" y="-22" width="32" height="44" rx="7" fill="#2a2e34" ${O(3)}/><rect x="-12" y="-16" width="24" height="28" rx="3" fill="#fff4f2"/><text x="0" y="3" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="11" fill="${C.red}">1669</text></g>`,
    // 2 · ญาติเคยตาย ตรวจใจก่อนสาย: a heart with its trace, the family under it
    (p) => `<g id="${p}-ht"><path d="M0,10C-30,-10 -44,-30 -40,-48C-36,-62 -16,-66 0,-50C16,-66 36,-62 40,-48C44,-30 30,-10 0,10Z" fill="url(#muHeart)" ${O(4)}/><path d="M-30,-44Q-28,-54 -18,-56" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/></g>
      <path id="${p}-tr" d="M-52,-30H-24L-16,-44L-8,-14L0,-34L6,-30H52" stroke="#fff" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0"/>
      ${[[-30, 34, 1, "#5a86c8"], [0, 30, 1.1, "#e2382e"], [30, 38, 0.8, "#2fa864"]].map(([x, y, s, c]) => `<g transform="translate(${x},${y}) scale(${s})"><circle cx="0" cy="-8" r="9" fill="${C.skin}" ${O(3)}/><path d="M-14,16Q-14,2 0,2Q14,2 14,16Z" fill="${c}" ${O(3)}/></g>`).join("")}`,
  ];
  const BADGE = { done: "#e4f6ea", active: "#fff1b0", next: "#eef0f4" };
  const icon = (k, x, y, s, id, state = "active") => `<g transform="translate(${x},${y}) scale(${s})"><g id="${id}"><circle r="62" fill="${BADGE[state]}"/><circle r="62" fill="none" stroke="#fff" stroke-width="5" opacity=".6" transform="translate(-2,-3) scale(.92)"/>
    <defs><clipPath id="${id}-cl"><circle r="60"/></clipPath></defs><g clip-path="url(#${id}-cl)"><g transform="scale(.92)">${ICONS[k](id)}</g></g><circle r="62" fill="none" ${O(4)}/></g></g>`;
  // the idle motion of each icon
  function iconAnim(tl, k, id, t0, dur) {
    const end = t0 + dur;
    if (k === 0) {
      for (let t = t0; t < end; t += 0.12) tl.set(`#${id}-shake`, { opacity: Math.round((t - t0) / 0.12) % 2 ? 0.3 : 1 }, t);
      for (let t = t0; t < end; t += 0.05) tl.set(`#${id}-body`, { x: Math.round((t - t0) / 0.05) % 2 ? 1.4 : -1.4 }, t);
      for (let t = t0 + 0.2; t < end - 0.3; t += 0.8) { tl.to(`#${id}-hand`, { rotation: -10, svgOrigin: "10 -16", duration: 0.09, ease: "power2.in" }, t); tl.to(`#${id}-hand`, { rotation: 0, svgOrigin: "10 -16", duration: 0.14, ease: "power2.out" }, t + 0.09);
        tl.to(`#${id}-hand`, { rotation: -10, svgOrigin: "10 -16", duration: 0.09, ease: "power2.in" }, t + 0.26); tl.to(`#${id}-hand`, { rotation: 0, svgOrigin: "10 -16", duration: 0.14, ease: "power2.out" }, t + 0.35); }
    } else if (k === 1) {
      const beat = 60 / 110;
      for (let t = t0; t < end - beat; t += beat) { tl.to(`#${id}-press`, { y: 7, duration: beat * 0.4, ease: "power2.in" }, t); tl.to(`#${id}-press`, { y: 0, duration: beat * 0.6, ease: "power2.out" }, t + beat * 0.4);
        tl.to(`#${id}-chest`, { scaleY: 0.82, svgOrigin: "13 32", duration: beat * 0.4, ease: "power2.in" }, t); tl.to(`#${id}-chest`, { scaleY: 1, svgOrigin: "13 32", duration: beat * 0.6, ease: "power2.out" }, t + beat * 0.4);
        tl.fromTo(`#${id}-arr`, { opacity: 1, y: 0 }, { opacity: 0.3, y: 8, duration: beat * 0.8, ease: "power1.out", immediateRender: false }, t); }
    } else {
      for (let t = t0; t < end - 0.9; t += 1.0) { tl.fromTo(`#${id}-tr`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "none", immediateRender: false }, t);
        tl.to(`#${id}-ht`, { scale: 1.12, svgOrigin: "0 -28", duration: 0.1, ease: "power2.out" }, t + 0.3); tl.to(`#${id}-ht`, { scale: 1, svgOrigin: "0 -28", duration: 0.3, ease: "power2.inOut" }, t + 0.4); }
    }
  }

  // ---------------- Bua's rule card on its lanyard ----------------
  const RULES = ["หลับแล้วเกร็ง อย่าเกรงจะปลุก", "ปลุกไม่ตื่น ปั๊มให้ฟื้น", "ญาติเคยตาย ตรวจใจก่อนสาย"];
  let seq = 0;
  function rule(tl, layer, t0, dur, o = {}) {
    const id = `mr${seq++}`, active = o.active ?? 0, done = o.done || [], Y = o.y ?? 520, S = o.s ?? 1, W = 920, H = 640;
    let c = `<path d="M-60,-${Y + 40}L-14,-6M60,-${Y + 40}L14,-6" stroke="${C.green}" stroke-width="22"/><path d="M-60,-${Y + 40}L-14,-6M60,-${Y + 40}L14,-6" stroke="#fff" stroke-width="3" stroke-dasharray="14 18" opacity=".7"/>
      <rect x="-26" y="-20" width="52" height="40" rx="8" fill="#c8ccd0" ${O(3)}/>`;
    c += `<g filter="url(#muDrop)"><rect x="${-W / 2}" y="0" width="${W}" height="${H}" rx="34" fill="${C.paper}" ${O(4)}/></g><path d="M${-W / 2},34Q${-W / 2},0 ${-W / 2 + 34},0H${W / 2 - 34}Q${W / 2},0 ${W / 2},34V126H${-W / 2}Z" fill="url(#muHead)" ${O(4)}/>
      <rect x="-50" y="18" width="100" height="16" rx="8" fill="#1e6a40"/>
      <text x="0" y="104" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="50" fill="#fff">กฎ 3 ข้อของป้าบัว</text>`;
    RULES.forEach((t, k) => {
      const y = 200 + k * 150, state = done.includes(k) ? "done" : k === active ? "active" : "next";
      c += `<g id="${id}-row${k}" opacity="${state === "next" ? 0.35 : 1}">`;
      if (state === "active") c += `<g transform="translate(-260,${y - 34})"><rect id="${id}-hl" x="0" y="0" width="${t.length * 22 + 40}" height="68" rx="14" fill="${C.yellow}" opacity=".7"/></g>`;
      c += icon(k, -360, y, 0.95, `${id}-i${k}`, state);
      c += `<text x="-250" y="${y + 16}" font-family="Kanit" font-weight="${state === "active" ? 900 : 700}" font-size="44" fill="${INK}">${t}</text>`;
      if (state === "done") c += `<g transform="translate(400,${y})"><circle r="28" fill="${C.green}" ${O(3)}/><path id="${id}-ck${k}" d="M-12,0l8,9l16,-17" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0"/></g>`;
      c += `</g>`;
    });
    put(layer, `<g transform="translate(540,${Y}) scale(${S})"><g id="${id}" opacity="0">${c}</g></g>`);
    // in: drop from above on the lanyard, swing and settle; rows slide in; the active icon pops, its highlight wipes, it moves
    tl.set(`#${id}`, { opacity: 1 }, t0);
    tl.fromTo(`#${id}`, { y: -900 }, { y: 0, duration: 0.55, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`#${id}`, { rotation: 10, svgOrigin: `0 -${Y + 40}` }, { rotation: 0, svgOrigin: `0 -${Y + 40}`, duration: 1.8, ease: "elastic.out(1, 0.3)", immediateRender: false }, t0 + 0.2);
    RULES.forEach((_, k) => tl.fromTo(`#${id}-row${k}`, { x: 60 }, { x: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, t0 + 0.45 + k * 0.12));
    done.forEach((k) => tl.fromTo(`#${id}-ck${k}`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.35, ease: "power2.out", immediateRender: false }, t0 + 0.9 + k * 0.1));
    tl.fromTo(`#${id}-i${active}`, { scale: 0.4, svgOrigin: "0 0" }, { scale: 1, svgOrigin: "0 0", duration: 0.6, ease: "back.out(3)", immediateRender: false }, t0 + 0.75);
    if (document.getElementById(`${id}-hl`)) tl.fromTo(`#${id}-hl`, { scaleX: 0, svgOrigin: "0 0" }, { scaleX: 1, duration: 0.5, ease: "power2.inOut", immediateRender: false }, t0 + 1.0);
    iconAnim(tl, active, `${id}-i${active}`, t0 + 1.2, dur - 1.5);
    // out: lift away
    tl.to(`#${id}`, { y: -60, opacity: 0, duration: 0.3, ease: "power2.in" }, t0 + dur - 0.3);
    return id;
  }

  function source(tl, layer, t0, dur, o = {}) {
    const id = `ms${seq++}`, text = o.text || "", w = Math.round(text.length * 15 + 90), y = o.y ?? 1810;
    put(layer, `<g transform="translate(540,${y})"><g id="${id}" opacity="0"><rect x="${-w / 2}" y="-26" width="${w}" height="52" rx="26" fill="#1a1e24" opacity=".82"/><circle cx="${-w / 2 + 28}" cy="0" r="12" fill="${C.green}"/><path d="M${-w / 2 + 22},0l4,5l8,-9" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <text x="${-w / 2 + 50}" y="9" font-family="Kanit" font-weight="500" font-size="26" fill="#f4f0e6">${text}</text></g></g>`);
    tl.fromTo(`#${id}`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", immediateRender: false }, t0);
    tl.to(`#${id}`, { opacity: 0, duration: 0.3 }, t0 + dur - 0.3);
  }

  window.MmUI = { flipAnim, rule, icon, iconAnim, source, RULES };
  Object.assign(Sets, { flip3 });
})();
