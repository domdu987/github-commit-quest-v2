// "ชาละวันมาตอนน้ำท่วม" world kit (เลน B · 1–2 พ.ย. 2569): a riverside village on the Nan (fictional "บ้านวังตะเคียน"), the flood season,
// a teak house on stilts whose ground floor is going under, at night. Built on hooks.js (Hk.croc) and rig v2.
//   cast: pao (เปา 10) · dew (ดิว 15, dewPhone) · yaiEiam (ยายเอี่ยม 70) · lungChot (ลุงชด 62, the boatman)
//   Sets.cwRoom(L, o)    the ground floor at night, water to the knee: plank walls, the shelf shrine, the family photo, the clock, the TV
//                        cabinet, the fridge, the wall socket low on the wall with a power strip and a phone on charge (o.spark), the
//                        bare bulb (o.bulb 0..1 flicker), the stair going up on the right, lightning through the louvres (o.flash),
//                        floating things, o.croc (Hk.croc spec), o.water (y of the surface)
//   Sets.cwLane(L, o)    the village lane under water at night: stilt houses with lit windows, a power pole with a sagging line,
//                        a tethered boat, banana trees, reflections, o.torch (a torch beam from the wader), o.croc
//   Sets.cwRiver(L, o)   the river at dusk before the flood peaks: the house on stilts, the old ศาลชาละวัน (a small shrine with a
//                        crocodile figure and garlands) on the bank, the boat, the water already at the stilts
(function () {
  const INK = "#1e1a16";
  const OUT = (w = 4) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const f1 = (v) => (+v).toFixed(1);
  const Cw = (window.Cw = window.Cw || {});

  // ---------------------------------------------------------------- cast
  const { LINE } = Rig2;
  const C = Rig.CAST;
  const ln = (w = 2.6) => `stroke="${LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const base = (k) => (C[k] && C[k].v2) || {};
  const bowl = (h) => `<path d="M-50,-546C-58,-610 -24,-630 2,-630C30,-629 60,-610 52,-546Q50,-560 44,-566H-42Q-48,-560 -50,-546Z" fill="${h.c}" ${ln()}/><path d="M-42,-566H44" stroke="${h.s}" stroke-width="4"/><path d="M-28,-606Q2,-620 34,-604" stroke="${h.sh}" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>`;
  const croc = `<g transform="translate(0,-404)"><path d="M-34,0Q-20,-10 10,-8L34,-4Q38,0 34,4L10,8Q-20,10 -34,0Z" fill="#4e8a3a" ${ln(2)}/><circle cx="-2" cy="-6" r="3" fill="#fff" stroke="${LINE}" stroke-width="1.2"/><path d="M14,-2l3,4l3,-4l3,4l3,-4" stroke="#fff" stroke-width="1.6" fill="none"/></g>`;
  C.pao = { v2: { ...base("tang"), face: "", hair: { c: "#16100c", s: "#060404", sh: "#5a4a40", front: (x) => bowl(x.hair) }, top: { kind: "tank", c: "#e2483c", sleeve: "none" }, print: croc,
    bottom: { kind: "shorts", c: "#2e3e6a" }, feet: { kind: "bare" } } };
  const jv = base("june");
  const bob = (h) => `<path d="M-56,-500C-66,-600 -30,-632 4,-632C40,-631 70,-600 58,-500Q52,-540 44,-560Q10,-574 -24,-566Q-44,-556 -50,-536Z" fill="${h.c}" ${ln()}/><path d="M-30,-604Q4,-620 40,-600" stroke="${h.sh}" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/><g transform="translate(-40,-572) rotate(-30)"><rect x="-16" y="-5" width="32" height="10" rx="4" fill="#f2c230" ${ln(1.8)}/></g>`;
  const bobBack = (h) => `<path d="M-60,-560Q-74,-470 -46,-470H50Q76,-470 62,-560Z" fill="${h.c}" ${ln()}/>`;
  C.dew = { v2: { ...jv, hair: { c: "#120c0a", s: "#000", sh: "#5a4a40", front: (x) => bob(x.hair), back: (x) => bobBack(x.hair) }, top: { kind: "tee", c: "#3aa0a8", sleeve: "short" }, print: `<path d="M-30,-420h60M-30,-406h44" stroke="#e8fbf8" stroke-width="5" opacity=".75"/>`,
    bottom: { kind: "shorts", c: "#2a3446" }, feet: { kind: "sandal", c: "#f2c230" }, wristband: "#f2c230" } };
  const phone = () => `<g transform="translate(0,118) rotate(-10)"><rect x="-13" y="-26" width="26" height="46" rx="5" fill="#2a2a32" ${ln(2)}/><rect x="-10" y="-22" width="20" height="36" rx="2" fill="#8ac8f0"/></g>`;
  C.dewPhone = { ...C.dew, hand: phone(), keep: "F" };
  const yv = base("yaiTide");
  const perm = (h) => `<g>${Array.from({ length: 11 }, (_, k) => { const a = Math.PI * (0.95 + k * 0.11), cx = Math.cos(a) * 54, cy = -566 + Math.sin(a) * 52; return `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="22" fill="${h.c}" ${ln(2.2)}/>`; }).join("")}<path d="M-40,-600Q0,-618 40,-600" stroke="${h.sh}" stroke-width="5" fill="none" opacity=".7"/></g>`;
  const specs = `<g transform="translate(0,-536)"><circle cx="-20" r="15" fill="#cfe2ff" fill-opacity=".25" stroke="#3a2a1e" stroke-width="3.2"/><circle cx="20" r="15" fill="#cfe2ff" fill-opacity=".25" stroke="#3a2a1e" stroke-width="3.2"/><path d="M-5,0H5" stroke="#3a2a1e" stroke-width="3"/></g>`;
  const pakaoma = `<path d="M-60,-470L50,-330" stroke="#c84a3a" stroke-width="26" stroke-linecap="round"/><path d="M-60,-470L50,-330" stroke="#f4e8d0" stroke-width="26" stroke-dasharray="10 10" opacity=".6"/>`;
  C.yaiEiam = { v2: { ...yv, hair: { c: "#d8d4cc", s: "#a8a49c", sh: "#f4f2ee", front: (x) => perm(x.hair), back: () => "" }, faceTop: specs, top: { kind: "blouse", c: "#8ab0d8", sleeve: "elbow", trim: "#6a90b8" }, print: "", extra: pakaoma } };
  const jn = base("taJun");
  const hat = `<g><ellipse cx="0" cy="-596" rx="96" ry="22" fill="#d8b878" ${ln()}/><path d="M-46,-600Q-40,-650 0,-654Q40,-650 46,-600Z" fill="#e2c48a" ${ln()}/><path d="M-46,-606Q0,-596 46,-606" stroke="#a8743a" stroke-width="6" fill="none"/></g>`;
  C.lungChot = { v2: { ...jn, faceTop: hat, top: { kind: "shirt", c: "#5a7a5a", sleeve: "long", neck: "collar", collar: "#4a6a4a", button: "#e8e4d8" }, extra: "" } };

  Sets.DEFS += `
    <linearGradient id="cwPlank" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a3222"/><stop offset=".5" stop-color="#5e4230"/><stop offset="1" stop-color="#3e2a1c"/></linearGradient>
    <linearGradient id="cwTeak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a34"/><stop offset="1" stop-color="#4e3018"/></linearGradient>
    <radialGradient id="cwBulb"><stop offset="0" stop-color="#fff2c8" stop-opacity="1"/><stop offset=".2" stop-color="#ffd890" stop-opacity=".55"/><stop offset="1" stop-color="#ffb860" stop-opacity="0"/></radialGradient>
    <linearGradient id="cwRiver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a7a5a"/><stop offset=".5" stop-color="#5a4e36"/><stop offset="1" stop-color="#2e281c"/></linearGradient>
    <linearGradient id="cwDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2a4e"/><stop offset=".55" stop-color="#8a5a6a"/><stop offset="1" stop-color="#e8946a"/></linearGradient>
    <radialGradient id="cwArc"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="#9ae0ff" stop-opacity=".9"/><stop offset="1" stop-color="#4ab0ff" stop-opacity="0"/></radialGradient>`;

  const ripples = (r, n, x0, x1, y0, y1, op = 0.4) => Array.from({ length: n }, () => `<path d="M${f1(x0 + r() * (x1 - x0))},${f1(y0 + r() * (y1 - y0))}q30,-8 60,0t60,0" stroke="#8ab0b0" stroke-width="4" fill="none" opacity="${(op * (0.5 + r() * 0.5)).toFixed(2)}"/>`).join("");
  const rain = (r, n, op = 0.5) => Array.from({ length: n }, () => `<path d="M${f1(-900 + r() * 2900)},${f1(-600 + r() * 3400)}l-18,70" stroke="#a8b8d8" stroke-width="3" opacity="${op}"/>`).join("");
  // a crackling arc of electricity across the water from the socket
  Cw.spark = (x, y, s = 1, seed = 5) => {
    const r = mk(seed); let d = `M0,0`;
    for (let k = 1; k <= 8; k++) d += `L${f1(k * 26 + (r() - 0.5) * 20)},${f1(k * 22 + (r() - 0.5) * 30)}`;
    return `<g transform="translate(${x},${y}) scale(${s})"><circle r="120" fill="url(#cwArc)"/><path d="${d}" stroke="#9ae0ff" stroke-width="14" fill="none" opacity=".6" stroke-linejoin="round"/><path d="${d}" stroke="#fff" stroke-width="5" fill="none" stroke-linejoin="round"/>
      ${[[-40, -30], [30, -50], [-10, 40]].map(([a, b]) => `<path d="M0,0L${a},${b}" stroke="#e8f8ff" stroke-width="4" stroke-linecap="round"/>`).join("")}<ellipse cx="200" cy="200" rx="160" ry="30" fill="#9ae0ff" opacity=".35"/></g>`;
  };

  // ---------------------------------------------------------------- the ground floor at night, flooding
  Sets.cwRoom = function (L, o = {}) {
    const id = o.id || "cr", r = mk(o.seed || 401), W = o.water ?? 1420, fl = o.flash ?? 0, bulb = o.bulb ?? 1;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="#0c0e12"/>`);
    // plank walls, a louvred window with the storm, the shrine shelf, the photo, the clock, the TV, the fridge
    let f = `<rect x="-900" y="0" width="2900" height="1600" fill="url(#cwPlank)"/>`;
    for (let x = -900; x < 2000; x += 110) f += `<path d="M${x},0V1600" stroke="#2a1c12" stroke-width="5"/><path d="M${x + 8},0V1600" stroke="#7a5a42" stroke-width="2" opacity=".5"/>`;
    f += `<g><rect x="-460" y="380" width="380" height="440" fill="#141c2c" ${OUT(6)}/>${Array.from({ length: 9 }, (_, k) => `<path d="M-450,${420 + k * 44}H-90" stroke="#3a2a1e" stroke-width="16"/>`).join("")}
      <path d="M-300,400L-340,520L-300,526L-350,640" stroke="#e8f0ff" stroke-width="${fl > 0.2 ? 8 : 0}" fill="none"/>${rain(r, 0)}</g>`;
    f += `<g transform="translate(160,420)"><rect x="-150" y="0" width="300" height="24" fill="#6a4228" ${OUT(4)}/><path d="M-120,0V-120H120V0" fill="#2a1a10" opacity=".6"/>
      <path d="M-30,0Q-36,-70 0,-96Q36,-70 30,0Z" fill="#c8a040" ${OUT(3)}/><circle cy="-100" r="16" fill="#c8a040" ${OUT(3)}/>${[-100, 100].map((x) => `<g transform="translate(${x},0)"><path d="M0,0V-60" stroke="#e8d8a0" stroke-width="10"/><circle cy="-64" r="7" fill="#ffb24a"/><circle cy="-64" r="26" fill="url(#cwBulb)"/></g>`).join("")}
      <path d="M-110,24Q0,90 110,24" stroke="#f4f2e0" stroke-width="12" fill="none" stroke-dasharray="6 8"/></g>`;
    f += `<g transform="translate(560,380)"><rect x="-90" y="0" width="180" height="230" fill="#5a3a22" ${OUT(4)}/><rect x="-76" y="14" width="152" height="202" fill="#c8b89a"/>${[[-30, 100, 30], [30, 110, 26], [0, 150, 18]].map(([x, y, rr]) => `<circle cx="${x}" cy="${y}" r="${rr}" fill="#8a6a52"/>`).join("")}</g>`;
    f += `<g transform="translate(860,330)"><circle r="56" fill="#efe8d4" ${OUT(4)}/><path d="M0,0V-36M0,0L28,4" stroke="${INK}" stroke-width="6" stroke-linecap="round"/></g>`;
    f += `<g transform="translate(-300,${W - 10})"><rect x="-150" y="-260" width="300" height="300" fill="#4a3020" ${OUT(4)}/><rect x="-130" y="-430" width="260" height="170" rx="10" fill="#1a1c20" ${OUT(4)}/><rect x="-116" y="-416" width="232" height="142" fill="#2a3440"/></g>`;
    f += `<g transform="translate(1180,${W + 40})"><rect x="-120" y="-760" width="240" height="760" rx="18" fill="#d8dcd8" ${OUT(5)}/><path d="M-120,-480H120" stroke="${INK}" stroke-width="4"/><rect x="90" y="-700" width="10" height="120" rx="5" fill="#8a8e92"/></g>`;
    // the socket low on the wall (just above the water) with a power strip on the floor and a phone on charge — the lure
    const SX = o.sockX ?? 620, SY = W - 70;
    put(L.far, f);
    const SK = o.sockS ?? 1;
    const sock = `<g transform="translate(${SX},${SY}) scale(${SK}) translate(${-SX},${-SY})"><rect x="${SX - 40}" y="${SY - 50}" width="80" height="100" rx="10" fill="#efe8d8" ${OUT(4)}/>${[-16, 16].map((dy) => `<circle cx="${SX}" cy="${SY + dy}" r="12" fill="#2a2420"/>`).join("")}
      <path d="M${SX},${SY + 16}C${SX + 30},${SY + 50} ${SX + 120},${SY + 10} ${SX + 130},${SY - 90}" stroke="${INK}" stroke-width="12" fill="none"/><path d="M${SX},${SY + 16}C${SX + 30},${SY + 50} ${SX + 120},${SY + 10} ${SX + 130},${SY - 90}" stroke="#f4f4f0" stroke-width="6" fill="none"/>
      <rect x="${SX + 110}" y="${SY - 330}" width="40" height="20" rx="6" fill="#8a7a62" ${OUT(2.5)}/><g transform="translate(${SX + 130},${SY - 190}) rotate(6)"><rect x="-22" y="-40" width="44" height="78" rx="8" fill="#2a2a32" ${OUT(3)}/><rect x="-17" y="-34" width="34" height="62" rx="4" fill="#8ac8f0"/><rect x="-10" y="-8" width="20" height="10" rx="2" fill="#7ad86a"/><circle r="70" fill="#8ac8f0" opacity=".22"/></g></g>`;
    // the water, with the room's things floating
    let s = (o.sock === false ? "" : sock) + `<rect x="-900" y="${W}" width="2900" height="1500" fill="url(#hkWater)"/><path d="M-900,${W}H2000" stroke="#6a9090" stroke-width="6" opacity=".6"/>` + ripples(r, 26, -800, 1900, W + 30, W + 900);
    s += `<g transform="translate(-60,${W + 40}) rotate(-10)"><rect x="-80" y="-18" width="160" height="22" rx="8" fill="#e85a3a" ${OUT(3)}/><path d="M-70,-18V-90H70V-18" stroke="#e85a3a" stroke-width="14" fill="none"/></g>`;
    s += `<ellipse cx="380" cy="${W + 160}" rx="40" ry="14" fill="#2a8ac8" ${OUT(2.5)}/><ellipse cx="880" cy="${W + 90}" rx="36" ry="12" fill="#f2c230" ${OUT(2.5)}/><g transform="translate(200,${W + 300})"><ellipse rx="70" ry="22" fill="#e8e4d8" ${OUT(3)}/><ellipse rx="50" ry="12" fill="#c8c0a8"/></g>`;
    if (o.spark) s += Cw.spark(SX, SY + 20 * (o.sockS ?? 1), o.spark, 7);
    put(L.set, s);
    if (o.croc) put(L.set, `<g id="${id}-croc">${Hk.croc(o.croc.x, o.croc.y, o.croc.s, o.croc)}</g>`);
    // the stair up on the right
    let st = "";
    for (let k = 0; k < 9; k++) { const sx = 760 + k * 66, sy = W + 160 - k * 116; st += `<path d="M${sx},${sy}H2000V${sy + 116}H${sx}Z" fill="url(#cwTeak)" ${OUT(4)}/><path d="M${sx},${sy}H2000" stroke="#b8885a" stroke-width="6"/>`; }
    st += `<path d="M740,${W + 110}L1340,${W - 930}" stroke="${INK}" stroke-width="30" stroke-linecap="round"/><path d="M740,${W + 110}L1340,${W - 930}" stroke="#7a5236" stroke-width="20" stroke-linecap="round"/>`;
    if (o.stairs !== false) put(L.act, st);
    // front water over the actors' legs (stair side only), the bulb, lightning wash
    put(L.fg, `<rect x="${o.fgWaterX ?? 700}" y="${W + 40}" width="1600" height="1600" fill="url(#hkWater)" opacity=".7"/>` + (o.fgWaterAll ? `<rect x="-900" y="${W + 40}" width="2900" height="1600" fill="url(#hkWater)" opacity=".6"/>` : ""));
    put(L.glow, `<g id="${id}-bulb" opacity="${bulb}"><path d="M300,-600V180" stroke="${INK}" stroke-width="5"/><circle cx="300" cy="200" r="22" fill="#fff2c8" ${OUT(3)}/><circle cx="300" cy="200" r="620" fill="url(#cwBulb)" opacity=".75"/><ellipse cx="300" cy="${W + 30}" rx="420" ry="40" fill="#ffd890" opacity=".25"/></g>
      <rect x="-900" y="-600" width="2900" height="3400" fill="url(#hkFlash)" opacity="${f1(fl * 0.3)}"/>`);
  };

  // ---------------------------------------------------------------- the lane under water
  Sets.cwLane = function (L, o = {}) {
    const id = o.id || "cl", r = mk(o.seed || 409), W = o.water ?? 1300, fl = o.flash ?? 0;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#hkStorm)"/>` + rain(r, 120, 0.45));
    const stilt = (x, s, lit) => `<g transform="translate(${x},${W}) scale(${s})">${[-180, -60, 60, 180].map((px) => `<rect x="${px - 12}" y="-260" width="24" height="420" fill="#2a1c12"/>`).join("")}
      <rect x="-230" y="-640" width="460" height="380" fill="#3a2a1c" ${OUT(4)}/><path d="M-280,-640L0,-860L280,-640Z" fill="#2a1e14" ${OUT(4)}/>${[-120, 60].map((wx) => `<rect x="${wx}" y="-560" width="90" height="120" fill="${lit ? "#ffcf7a" : "#141a20"}" ${OUT(3)}/>`).join("")}
      ${lit ? `<circle cx="0" cy="-500" r="320" fill="url(#cwBulb)" opacity=".45"/>` : ""}</g>`;
    put(L.far, stilt(-520, 0.8, true) + stilt(980, 0.9, false) + stilt(250, 0.55, true) + `<g transform="translate(-60,${W})"><rect x="-14" y="-1000" width="28" height="1100" fill="#3a3a3a"/><path d="M-120,-960H120" stroke="#3a3a3a" stroke-width="16"/><rect x="40" y="-900" width="70" height="90" rx="10" fill="#5a5e62" ${OUT(3)}/>
      <path d="M-120,-960Q-400,-500 -560,-${f1(30)}" stroke="#141414" stroke-width="5" fill="none"/><path d="M120,-960Q500,-700 800,-620" stroke="#141414" stroke-width="5" fill="none"/></g>`);
    let s = `<rect x="-900" y="${W}" width="2900" height="1500" fill="url(#hkWater)"/><path d="M-900,${W}H2000" stroke="#6a9090" stroke-width="6" opacity=".6"/>`;
    s += [[-520, 0.8], [250, 0.55]].map(([x, sc]) => `<path d="M${x - 120 * sc},${W + 10}L${x + 120 * sc},${W + 10}L${x + 200 * sc},${W + 600}L${x - 200 * sc},${W + 600}Z" fill="#ffcf7a" opacity=".16"/>`).join("") + ripples(r, 30, -800, 1900, W + 20, W + 900, 0.45);
    s += `<g transform="translate(700,${W + 30})"><path d="M-220,-20Q0,40 220,-20L190,20Q0,60 -190,20Z" fill="#6a4a2a" ${OUT(4)}/><path d="M-200,-14Q0,30 200,-14" stroke="#9a7a4a" stroke-width="5" fill="none"/></g>`;
    s += `<g transform="translate(-760,${W - 40})"><path d="M0,40V-300" stroke="#3a5a2a" stroke-width="22"/>${[-1, 1].map((d) => `<path d="M0,-280Q${d * 160},-360 ${d * 260},-260Q${d * 140},-300 0,-260Z" fill="#2e4a24" ${OUT(3)}/>`).join("")}</g>`;
    put(L.set, s);
    if (o.croc) put(L.set, `<g id="${id}-croc">${Hk.croc(o.croc.x, o.croc.y, o.croc.s, o.croc)}</g>`);
    put(L.fg, `<rect x="-900" y="${W + 60}" width="2900" height="1600" fill="url(#hkWater)" opacity=".6"/>` + ripples(r, 10, -800, 1900, W + 70, W + 400, 0.5));
    put(L.glow, (o.torch ? `<path d="M${o.torch.x},${o.torch.y}L${o.torch.tx - 260},${o.torch.ty - 80}L${o.torch.tx + 260},${o.torch.ty + 80}Z" fill="#fff6d0" opacity=".22"/><ellipse cx="${o.torch.tx}" cy="${o.torch.ty}" rx="300" ry="90" fill="#fff6d0" opacity=".25"/>` : "")
      + `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#hkFlash)" opacity="${f1(fl * 0.3)}"/>`);
  };

  // ---------------------------------------------------------------- the river at dusk (look sheet / establishing)
  Sets.cwRiver = function (L, o = {}) {
    const id = o.id || "cv", r = mk(o.seed || 419), W = o.water ?? 1350;
    put(L.sky, `<rect x="-900" y="-600" width="2900" height="3400" fill="url(#cwDusk)"/><circle cx="820" cy="${W - 160}" r="90" fill="#ffd8a0" opacity=".9"/>` + Array.from({ length: 5 }, () => `<ellipse cx="${f1(-600 + r() * 2400)}" cy="${f1(150 + r() * 500)}" rx="${f1(200 + r() * 200)}" ry="${f1(30 + r() * 30)}" fill="#3a3a5a" opacity=".6"/>`).join(""));
    put(L.far, `<path d="M-900,${W - 60}Q0,${W - 140} 2000,${W - 80}V${W}H-900Z" fill="#2a3a2e"/>` + Array.from({ length: 18 }, (_, k) => Lt.bush(-900 + k * 170, W - 110, 70 + (k % 3) * 20, 700 + k, "far", { line: 1.5 })).join(""));
    let s = `<rect x="-900" y="${W}" width="2900" height="1500" fill="url(#cwRiver)"/>` + ripples(r, 30, -800, 1900, W + 20, W + 900, 0.35) + `<path d="M780,${W + 10}L860,${W + 10}L960,${W + 700}L680,${W + 700}Z" fill="#ffd8a0" opacity=".2"/>`;
    // the house on stilts, half its stilts under
    s += `<g transform="translate(-260,${W})">${[-260, -120, 20, 160, 300].map((px) => `<rect x="${px - 14}" y="-300" width="28" height="420" fill="#3a2414" ${OUT(3)}/>`).join("")}
      <rect x="-320" y="-760" width="680" height="460" fill="url(#cwTeak)" ${OUT(5)}/><path d="M-380,-760L20,-1060L420,-760Z" fill="#6a3a22" ${OUT(5)}/>${[-240, -40, 160].map((wx) => `<rect x="${wx}" y="-660" width="120" height="160" fill="#ffcf7a" ${OUT(3)}/>`).join("")}
      <path d="M-320,-300H360" stroke="#2a1a0e" stroke-width="12"/><path d="M360,-300L560,-60" stroke="#5a3a22" stroke-width="22"/></g>`;
    // the shrine of Chalawan on the bank: a small red-roofed spirit house on a post, a crocodile figure, garlands, incense
    s += `<g transform="translate(560,${W - 10})"><rect x="-10" y="-260" width="20" height="270" fill="#8a6a52" ${OUT(3)}/><rect x="-90" y="-380" width="180" height="120" fill="#c8a040" ${OUT(4)}/><path d="M-120,-380L0,-470L120,-380Z" fill="#c8302a" ${OUT(4)}/>
      <g transform="translate(0,-290)"><path d="M-70,0Q-40,-26 30,-20L70,-12Q74,0 70,8L30,14Q-40,18 -70,0Z" fill="#4e6a3a" ${OUT(2.5)}/><circle cx="18" cy="-12" r="4" fill="#ffd23a"/></g>
      ${[-60, 60].map((gx) => `<path d="M${gx},-262Q${gx},-200 ${gx + 10},-180" stroke="#f4f2e0" stroke-width="10" stroke-dasharray="6 6"/>`).join("")}<path d="M-30,-262V-300M30,-262V-300" stroke="#c8a060" stroke-width="3"/></g>`;
    s += `<g transform="translate(300,${W + 120})"><path d="M-240,-20Q0,40 240,-20L210,20Q0,60 -210,20Z" fill="#6a4a2a" ${OUT(4)}/></g>`;
    put(L.set, s);
    if (o.croc) put(L.set, Hk.croc(o.croc.x, o.croc.y, o.croc.s, o.croc));
  };
})();
