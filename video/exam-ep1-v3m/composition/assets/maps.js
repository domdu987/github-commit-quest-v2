// Travel maps for any story — every journey in a clip gets one (the user: "ถ้ามีฉากที่ต้องเดินทางทำแผนที่ด้วย").
// Thailand and its neighbours come from mapsdata.js (Natural Earth 1:50m, Mercator, a 900×1300 box). The map is a set, so the
// shot's camera can push in on the destination at the end.
//   Sets.mapTH(L, o)   the sea, the neighbours (named), Thailand with a raised edge and a soft relief, an optional region glow
//                      o.region [lon, lat, radius, "อีสาน"] (#id-region), the route o.route [[lon, lat]…] (dashed, #id-reveal draws it),
//                      pins #id-pin0 / #id-pin1 (+ #id-sh0 / #id-sh1 ground shadows) with labels #id-lab0 / #id-lab1 (o.from, o.to),
//                      o.toIcon: SVG drawn inside the end pin (24-unit circle), the vehicle #id-car (o.vehicle bus | van | moto | ambulance)
//                      placement in world space: o.x, o.y (top-left of the 900×1300 box), o.s
//   Maps.route(tl, id, t0, o)  the animation: start pin drops and its label pops (t0+0.2), the line draws on with the vehicle riding
//                      its head (o.go [start, end] seconds after t0, default [0.8, 4.2]), the region glows as the vehicle enters it,
//                      the end pin drops on arrival with a ripple; o.ease for the drive (default "power1.inOut")
//   Maps.P(lon, lat)   map units for a lon/lat (to place anything else)
//   Sets.mapVillage(L, o)  an illustrated village seen from above (not to scale): paddies, ponds, tree clumps, laterite lanes, the
//                      highway along the bottom with the village gate, houses each with a red shirt at the door, the sala, the temple,
//                      the loudspeaker tower, and to the right along the highway the town with the provincial hospital (x 980–1420).
//                      Same route contract as mapTH (o.route in map units, o.from / o.to, o.fromIcon / o.toIcon, o.vehicle, o.carS,
//                      o.labDx / o.labDy) plus o.stops [{ at: [x, y], label, icon }] — pins that drop as the vehicle passes (#id-st0…),
//                      o.name (the village name on the gate) · Maps.VIL names the places in map units (keng, piak, sala, gate, wat,
//                      tower, hospital) and Maps.VIL.roads the lane polylines to build routes along · Maps.ICON.{aed, house, hospital}
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const mk = (seed) => () => { seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const INK = "#2a2420";
  const D = () => window.MAPDATA.th;
  const P = (lon, lat) => { const d = D(), l = (lon * Math.PI) / 180, p = (lat * Math.PI) / 180; return [d.tx + d.k * l, d.ty - d.k * Math.log(Math.tan(Math.PI / 4 + p / 2))]; };

  Sets.DEFS += `
    <radialGradient id="mpSea" cx=".55" cy=".35" r=".9"><stop offset="0" stop-color="#cdeef0"/><stop offset=".6" stop-color="#a6d8de"/><stop offset="1" stop-color="#7cbcc8"/></radialGradient>
    <linearGradient id="mpLand" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#f6e8cc"/></linearGradient>
    <radialGradient id="mpGlow"><stop offset="0" stop-color="#7cd68a" stop-opacity=".75"/><stop offset=".6" stop-color="#7cd68a" stop-opacity=".35"/><stop offset="1" stop-color="#7cd68a" stop-opacity="0"/></radialGradient>
    <linearGradient id="mpPin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff6a5a"/><stop offset="1" stop-color="#c8241e"/></linearGradient>
    <linearGradient id="mpPinB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5a9cf0"/><stop offset="1" stop-color="#2a5cb8"/></linearGradient>
    <filter id="mpBlur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="9"/></filter>
    <filter id="mpDrop" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dy="6"/><feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>`;

  // a smooth line through the points (Catmull-Rom as cubic Béziers)
  const smooth = (pts) => {
    let d = `M${f1(pts[0][0])},${f1(pts[0][1])}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      d += `C${f1(p1[0] + (p2[0] - p0[0]) / 6)},${f1(p1[1] + (p2[1] - p0[1]) / 6)} ${f1(p2[0] - (p3[0] - p1[0]) / 6)},${f1(p2[1] - (p3[1] - p1[1]) / 6)} ${f1(p2[0])},${f1(p2[1])}`;
    }
    return d;
  };

  // vehicles, side view facing right, wheels on y 0, about 90 units long
  const wheel = (x) => `<circle cx="${x}" cy="-9" r="9" fill="#1e1e22" stroke="${INK}" stroke-width="2.4"/><circle cx="${x}" cy="-9" r="3.5" fill="#c8ccd0"/>`;
  const VEH = {
    bus: () => `<rect x="-48" y="-46" width="96" height="40" rx="9" fill="#f4f6f8" stroke="${INK}" stroke-width="3"/><path d="M-48,-22H48" stroke="#2a6ad0" stroke-width="7"/><path d="M-48,-14H48" stroke="#e2382e" stroke-width="4"/>
      <rect x="-40" y="-40" width="70" height="14" rx="3" fill="#7ab8e8"/><path d="M-22,-40V-26M-4,-40V-26M14,-40V-26" stroke="#4a88c0" stroke-width="2"/><path d="M34,-40H44Q48,-40 48,-34V-26H34Z" fill="#7ab8e8"/>${wheel(-28)}${wheel(28)}`,
    van: () => `<path d="M-44,-8V-38Q-44,-44 -38,-44H24Q32,-44 38,-36L46,-24V-8Z" fill="#f4f6f8" stroke="${INK}" stroke-width="3"/><rect x="-36" y="-38" width="44" height="13" rx="3" fill="#7ab8e8"/><path d="M14,-38H24L34,-26H14Z" fill="#7ab8e8"/><path d="M-44,-18H46" stroke="#2a6ad0" stroke-width="5"/>${wheel(-26)}${wheel(26)}`,
    moto: () => `<circle cx="-24" cy="-12" r="12" fill="#1e1e22" stroke="${INK}" stroke-width="2.4"/><circle cx="26" cy="-12" r="12" fill="#1e1e22" stroke="${INK}" stroke-width="2.4"/><path d="M-24,-12L-6,-26H18L26,-12" stroke="#2a5ab8" stroke-width="7" fill="none" stroke-linejoin="round"/>
      <path d="M-14,-30H8" stroke="#1a1a1e" stroke-width="6" stroke-linecap="round"/><path d="M18,-26L22,-44" stroke="#5a5e62" stroke-width="4"/><circle cx="-4" cy="-48" r="9" fill="#e8c040" stroke="${INK}" stroke-width="2.4"/><path d="M-6,-40L-10,-28L4,-28" stroke="#e8e2d4" stroke-width="7" fill="none"/>`,
    ambulance: () => `<path d="M-46,-8V-46H18L32,-30L46,-26V-8Z" fill="#fbfbfb" stroke="${INK}" stroke-width="3"/><rect x="18" y="-42" width="12" height="12" rx="2" fill="#7ab8e8"/><path d="M-46,-20H46" stroke="#e2382e" stroke-width="6"/>
      <path d="M-22,-40v14M-29,-33h14" stroke="#e2382e" stroke-width="5"/><rect x="-14" y="-54" width="16" height="8" rx="2" fill="#e2382e" stroke="${INK}" stroke-width="2"/>${wheel(-28)}${wheel(28)}`,
  };

  // a map pin: teardrop with a white disc; origin at its tip
  const pin = (fill, inner = "") => `<path d="M0,0C-6,-16 -30,-34 -30,-58A30,30 0 1 1 30,-58C30,-34 6,-16 0,0Z" fill="url(#${fill})" stroke="${INK}" stroke-width="3"/>
    <circle cx="0" cy="-58" r="18" fill="#fffaf0"/><g transform="translate(0,-58)">${inner}</g><path d="M-18,-74Q-12,-84 -2,-86" stroke="#fff" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>`;
  const label = (text, w) => `<rect x="${-w / 2}" y="-30" width="${w}" height="56" rx="28" fill="#fffaf0" stroke="${INK}" stroke-width="3"/><text x="0" y="10" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="32" fill="${INK}">${text}</text>`;
  const textW = (t, px = 32) => Math.round(t.length * px * 0.56 + 44);

  // the route (a white underlay and a red dashed line revealed by #id-reveal), the end pins with shadows and labels, the stops,
  // the arrival ripple and the vehicle; pts in map units
  function routeLayer(id, pts, o) {
    let m = "";
    // the route: a white underlay and a red dashed line, both revealed by #id-reveal drawing on inside a mask
    const rd = smooth(pts);
    m += `<defs><mask id="${id}-rm" maskUnits="userSpaceOnUse" x="-500" y="-500" width="2000" height="2400"><path id="${id}-reveal" d="${rd}" stroke="#fff" stroke-width="40" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="0"/></mask></defs>
      <g mask="url(#${id}-rm)"><path d="${rd}" stroke="#fffaf0" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/><path d="${rd}" stroke="#e2382e" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="18 14"/></g>
      <path id="${id}-path" d="${rd}" fill="none" stroke="none"/>`;
    // pins with their shadows and labels (the label sits above the pin)
    const [a, b] = [pts[0], pts[pts.length - 1]];
    const ends = [[a, "mpPinB", o.fromIcon || `<circle r="7" fill="#2a5cb8"/>`, o.from || "กรุงเทพฯ"], [b, "mpPin", o.toIcon || `<circle r="7" fill="#c8241e"/>`, o.to || ""]];
    ends.forEach(([[px, py], fill, inner, name], k) => {
      m += `<g transform="translate(${f1(px)},${f1(py)})"><g id="${id}-sh${k}"><ellipse cx="0" cy="0" rx="16" ry="6" fill="#3a2a10" opacity=".35"/></g></g>`;
      m += `<g transform="translate(${f1(px)},${f1(py)})"><g id="${id}-pin${k}">${pin(fill, inner)}</g></g>`;
      if (name) m += `<g transform="translate(${f1(px + (o.labDx?.[k] ?? 0))},${f1(py - 128 + (o.labDy?.[k] ?? 0))})"><g id="${id}-lab${k}" filter="url(#mpDrop)">${label(name, textW(name))}</g></g>`;
    });
    m += `<g transform="translate(${f1(b[0])},${f1(b[1])})"><g id="${id}-rip" opacity="0"><circle r="34" fill="none" stroke="#e2382e" stroke-width="5"/></g></g>`;
    m += `<g id="${id}-car" transform="translate(${f1(a[0])},${f1(a[1])})"><g transform="scale(${o.carS ?? 1})"><g id="${id}-bob">${(VEH[o.vehicle] || VEH.bus)()}</g></g></g>`;
    (o.stops || []).forEach((st, k) => {
      const [px, py] = st.at, nm = st.label || "";
      m += `<g transform="translate(${f1(px)},${f1(py)})"><g id="${id}-str${k}" opacity="0"><circle r="34" fill="none" stroke="#1e8a4c" stroke-width="5"/></g></g>`;
      m += `<g transform="translate(${f1(px)},${f1(py)})"><g id="${id}-st${k}" data-x="${f1(px)}" data-y="${f1(py)}">${pin(st.fill || "mpPinG", st.icon || ICON.aed)}</g></g>`;
      if (nm) m += `<g transform="translate(${f1(px + (st.dx ?? 0))},${f1(py - 128 + (st.dy ?? 0))})"><g id="${id}-stl${k}" filter="url(#mpDrop)">${label(nm, textW(nm))}</g></g>`;
    });
    return m;
  }

  function mapTH(L, o = {}) {
    const id = o.id || "mp", d = D(), X = o.x ?? 90, Y = o.y ?? 300, S = o.s ?? 1;
    const G = (inner) => `<g transform="translate(${X},${Y}) scale(${S})">${inner}</g>`;
    let sea = `<rect x="-3000" y="-3000" width="8000" height="9000" fill="url(#mpSea)"/>`;
    for (let k = 0; k < 26; k++) { const y = -600 + k * 120, x = -400 + (k % 3) * 90; sea += `<path d="M${x},${y}q30,-12 60,0t60,0" stroke="#fff" stroke-width="3" fill="none" opacity=".35"/><path d="M${x + 520},${y + 60}q30,-12 60,0t60,0" stroke="#fff" stroke-width="3" fill="none" opacity=".3"/>`; }
    put(L.sky, sea);
    // neighbours, then Thailand raised above them (a blurred shadow, the land, its coast)
    let m = Object.values(d.nb).map((p) => `<path d="${p}" fill="#efe4cc" stroke="#c8b48e" stroke-width="2"/>`).join("");
    const names = [["ลาว", 102.4, 19.9], ["กัมพูชา", 104.9, 12.9], ["เมียนมา", 97.0, 21.0], ["มาเลเซีย", 101.6, 5.3], ["เวียดนาม", 106.4, 16.9]];
    m += names.map(([n, lo, la]) => { const [px, py] = P(lo, la); return `<text x="${f1(px)}" y="${f1(py)}" text-anchor="middle" font-family="Kanit" font-weight="600" font-size="30" fill="#a8946e" letter-spacing="2">${n}</text>`; }).join("");
    const [gx, gy] = P(101.0, 10.6);
    m += `<text x="${f1(gx)}" y="${f1(gy)}" text-anchor="middle" font-family="Kanit" font-weight="600" font-style="italic" font-size="28" fill="#4a8a96" letter-spacing="3">อ่าวไทย</text>`;
    m += `<path d="${d.th}" fill="#3a2a10" opacity=".35" transform="translate(6,14)" filter="url(#mpBlur)"/><path d="${d.th}" fill="url(#mpLand)" stroke="#b08a5a" stroke-width="3.5" stroke-linejoin="round"/>`;
    m += `<defs><clipPath id="${id}-thc"><path d="${d.th}"/></clipPath></defs><path d="${d.th}" fill="none" stroke="#fff" stroke-width="10" opacity=".55" transform="translate(-3,-4)" clip-path="url(#${id}-thc)"/>`;
    if (o.region) { const [lo, la, rr, nm] = o.region, [rx, ry] = P(lo, la);
      m += `<g id="${id}-region" opacity=".85"><circle cx="${f1(rx)}" cy="${f1(ry)}" r="${rr}" fill="url(#mpGlow)" clip-path="url(#${id}-thc)"/></g>
        <text id="${id}-rlab" x="${f1(rx - rr * 0.2)}" y="${f1(ry + rr * 0.55)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="40" fill="#2a8a4a" letter-spacing="6" opacity=".9">${nm || ""}</text>`; }
    m += routeLayer(id, (o.route || [[100.52, 13.75], [103.55, 16.25]]).map(([lo, la]) => P(lo, la)), o);
    put(L.set, G(m));
  }

  function route(tl, id, t0, o = {}) {
    const [g0, g1] = o.go || [0.8, 4.2];
    const path = document.getElementById(`${id}-path`), car = document.getElementById(`${id}-car`), len = path.getTotalLength();
    const place = (p) => {
      const L0 = Math.max(0, Math.min(len, p * len)), q = path.getPointAtLength(L0), q2 = path.getPointAtLength(Math.min(len, L0 + 6)), q1 = path.getPointAtLength(Math.max(0, L0 - 6));
      let ang = (Math.atan2(q2.y - q1.y, q2.x - q1.x) * 180) / Math.PI, flip = 1;
      if (ang > 90 || ang < -90) { ang += 180; flip = -1; }
      car.setAttribute("transform", `translate(${f1(q.x)},${f1(q.y)}) rotate(${f1(ang)}) scale(${flip},1)`);
    };
    place(0);
    // start pin: drop in with a bounce, its shadow grows as it lands; the label pops
    tl.set(`#${id}-reveal`, { attr: { "stroke-dashoffset": 1 } }, t0);
    tl.set([`#${id}-pin0`, `#${id}-car`], { opacity: 0 }, t0);
    tl.set(`#${id}-lab0`, { scale: 0, svgOrigin: "0 0" }, t0);
    tl.set(`#${id}-sh0`, { scale: 0.2, svgOrigin: "0 0" }, t0);
    tl.fromTo(`#${id}-pin0`, { y: -160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "bounce.out", immediateRender: false }, t0 + 0.15);
    tl.fromTo(`#${id}-sh0`, { scale: 0.2, svgOrigin: "0 0" }, { scale: 1, duration: 0.6, ease: "bounce.out", immediateRender: false }, t0 + 0.15);
    tl.fromTo(`#${id}-lab0`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, t0 + 0.55);
    tl.set([`#${id}-pin1`, `#${id}-lab1`], { opacity: 0 }, t0);
    tl.set(`#${id}-sh1`, { scale: 0, svgOrigin: "0 0" }, t0);
    tl.fromTo(`#${id}-car`, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: false }, t0 + g0 - 0.2);
    // the drive: the line draws on and the vehicle rides its head
    const prog = { p: 0 };
    tl.fromTo(`#${id}-reveal`, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: g1 - g0, ease: o.ease || "power1.inOut", immediateRender: false }, t0 + g0);
    tl.fromTo(prog, { p: 0 }, { p: 1, duration: g1 - g0, ease: o.ease || "power1.inOut", immediateRender: false, onUpdate: () => place(prog.p) }, t0 + g0);
    // the vehicle bobs a little as it drives
    tl.fromTo(`#${id}-bob`, { y: 0 }, { y: -3, duration: 0.12, repeat: Math.max(1, Math.floor((g1 - g0) / 0.12)), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + g0);
    if (document.getElementById(`${id}-region`)) {
      tl.fromTo(`#${id}-region`, { opacity: 0.45 }, { opacity: 1, duration: 0.5, ease: "sine.out", immediateRender: false }, t0 + g0 + (g1 - g0) * 0.55);
      tl.fromTo(`#${id}-rlab`, { opacity: 0, y: 14 }, { opacity: 0.9, y: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, t0 + g0 + (g1 - g0) * 0.55);
    }
    // stops: each drops when the vehicle passes it (the nearest point of the path, through the drive's ease)
    const ez = gsap.parseEase(o.ease || "power1.inOut");
    for (let k = 0; document.getElementById(`${id}-st${k}`); k++) {
      const el = document.getElementById(`${id}-st${k}`), sx = +el.dataset.x, sy = +el.dataset.y;
      let best = 0, bd = Infinity;
      for (let s = 0; s <= len; s += 4) { const q = path.getPointAtLength(s), dd = (q.x - sx) ** 2 + (q.y - sy) ** 2; if (dd < bd) { bd = dd; best = s; } }
      const p = best / len;
      let lo = 0, hi = 1;
      for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; if (ez(m) < p) lo = m; else hi = m; }
      const ts = t0 + g0 + (g1 - g0) * lo;
      tl.set(`#${id}-st${k}`, { opacity: 0 }, t0);
      tl.fromTo(`#${id}-st${k}`, { y: -140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "bounce.out", immediateRender: false }, ts - 0.2);
      tl.set(`#${id}-stl${k}`, { scale: 0, svgOrigin: "0 0" }, t0);
      tl.fromTo(`#${id}-stl${k}`, { scale: 0, svgOrigin: "0 0" }, { scale: 1, duration: 0.45, ease: "back.out(2.6)", immediateRender: false }, ts + 0.25);
      tl.fromTo(`#${id}-str${k}`, { opacity: 0.9, scale: 0.3, svgOrigin: "0 0" }, { opacity: 0, scale: 2.6, duration: 0.8, ease: "power2.out", immediateRender: false }, ts + 0.3);
    }
    // arrival: the end pin drops, the shadow lands, a ripple ring, the label pops
    tl.fromTo(`#${id}-pin1`, { y: -200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: "bounce.out", immediateRender: false }, t0 + g1 - 0.1);
    tl.to(`#${id}-sh1`, { scale: 1, duration: 0.7, ease: "bounce.out" }, t0 + g1 - 0.1);
    tl.fromTo(`#${id}-rip`, { opacity: 0.9, scale: 0.3, svgOrigin: "0 0" }, { opacity: 0, scale: 2.6, duration: 0.8, ease: "power2.out", immediateRender: false }, t0 + g1 + 0.25);
    tl.fromTo(`#${id}-lab1`, { opacity: 0, scale: 0, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.6)", immediateRender: false }, t0 + g1 + 0.35);
    tl.to(`#${id}-car`, { opacity: 0, duration: 0.3 }, t0 + g1 + 0.1);
  }

  // ---------------- the village from above ----------------
  Sets.DEFS += `
    <linearGradient id="mvGround" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#fbf1d8"/><stop offset="1" stop-color="#f0dcb4"/></linearGradient>
    <linearGradient id="mvPond" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bfe6ea"/><stop offset="1" stop-color="#86c4d0"/></linearGradient>
    <linearGradient id="mpPinG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5ad08a"/><stop offset="1" stop-color="#1e8a4c"/></linearGradient>`;
  const ICON = {
    aed: `<path d="M0,9C-9,1 -16,-7 -14,-13C-12,-19 -4,-20 0,-13C4,-20 12,-19 14,-13C16,-7 9,1 0,9Z" fill="#2fa864"/><path d="M1,-15l-5,9h5l-3,8l8,-11h-5l3,-6z" fill="#fff"/>`,
    house: `<path d="M-12,2V-8L0,-17L12,-8V2Z" fill="#c8241e"/><rect x="-4" y="-5" width="8" height="7" fill="#fffaf0"/>`,
    hospital: `<rect x="-14" y="-14" width="28" height="28" rx="6" fill="#e2382e"/><path d="M0,-9V9M-9,0H9" stroke="#fff" stroke-width="6"/>`,
    moto: `<circle cx="-8" cy="4" r="5" fill="#2a2420"/><circle cx="9" cy="4" r="5" fill="#2a2420"/><path d="M-8,4L-2,-4H6L9,4" stroke="#2a5ab8" stroke-width="4" fill="none"/>`,
  };
  // named places and the lanes (map units in the 900×1300 box; the town runs on to x ≈ 1420 along the highway)
  const VIL = {
    gate: [300, 1128], keng: [212, 848], piak: [338, 900], sala: [552, 496], wat: [652, 236], tower: [372, 470], hospital: [1290, 1052],
    roads: {
      main: [[300, 1140], [312, 1000], [418, 872], [430, 700], [440, 526], [468, 330], [520, 150]],
      south: [[96, 884], [250, 872], [430, 864], [620, 872], [790, 884]],
      north: [[120, 548], [300, 532], [440, 526], [620, 528], [800, 534]],
      west: [[96, 884], [112, 720], [120, 548]],
      east: [[790, 884], [800, 720], [800, 534]],
      highway: [[-420, 1162], [300, 1160], [900, 1162], [1500, 1164]],
    },
  };
  function mapVillage(L, o = {}) {
    const id = o.id || "mv", r = mk(o.seed || 4242), X = o.x ?? 90, Y = o.y ?? 300, S = o.s ?? 1;
    const G = (inner) => `<g transform="translate(${X},${Y}) scale(${S})">${inner}</g>`;
    // paddies: tiles with raised bunds and a few flooded or darker plots
    let p = `<rect x="-3000" y="-3000" width="8000" height="9000" fill="#cfe6a4"/>`;
    for (let ty = -420; ty < 1720; ty += 96) for (let tx = -620; tx < 1900; tx += 124) {
      const k = r(), c = k < 0.12 ? "#bfe3e0" : k < 0.45 ? "#c4e096" : k < 0.8 ? "#d2e9a8" : "#b8d98a", jx = (r() - 0.5) * 10;
      p += `<rect x="${f1(tx + jx)}" y="${ty}" width="118" height="90" rx="6" fill="${c}" stroke="#e9f3cc" stroke-width="5"/>`;
      if (k > 0.3 && k < 0.8) p += `<path d="M${f1(tx + 14 + jx)},${ty + 24}h90M${f1(tx + 14 + jx)},${ty + 46}h90M${f1(tx + 14 + jx)},${ty + 68}h90" stroke="#a8cc78" stroke-width="2.4" opacity=".55" stroke-dasharray="6 8"/>`;
    }
    put(L.sky, G(p));
    let m = "";
    // the dry village ground, ponds, tree clumps at its rim
    m += `<path d="M60,460C40,300 180,150 360,130C520,110 760,150 860,330C930,470 900,700 870,880C850,1010 700,1080 500,1090C300,1100 120,1060 70,930C30,800 76,600 60,460Z" fill="#3a2a10" opacity=".14" transform="translate(6,12)"/>`;
    m += `<path d="M60,460C40,300 180,150 360,130C520,110 760,150 860,330C930,470 900,700 870,880C850,1010 700,1080 500,1090C300,1100 120,1060 70,930C30,800 76,600 60,460Z" fill="url(#mvGround)" stroke="#d8c08e" stroke-width="4"/>`;
    m += `<ellipse cx="660" cy="712" rx="96" ry="60" fill="url(#mvPond)" stroke="#6aaab8" stroke-width="4"/><path d="M610,700q20,-8 40,0t40,0" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>`;
    m += `<ellipse cx="-120" cy="620" rx="120" ry="70" fill="url(#mvPond)" stroke="#6aaab8" stroke-width="4"/>`;
    const tree = (x, y, s) => { let t = `<ellipse cx="${f1(x + 6)}" cy="${f1(y + 10)}" rx="${f1(26 * s)}" ry="${f1(22 * s)}" fill="#3a2a10" opacity=".18"/>`;
      for (let i = 0; i < 4; i++) { const a = i * 1.7 + r(), d = 12 * s; t += `<circle cx="${f1(x + Math.cos(a) * d)}" cy="${f1(y + Math.sin(a) * d)}" r="${f1((15 + r() * 7) * s)}" fill="${["#7cc070", "#6ab45e", "#88c87a"][i % 3]}" stroke="#4a7a3a" stroke-width="2.4"/>`; }
      return t + `<circle cx="${f1(x - 6 * s)}" cy="${f1(y - 8 * s)}" r="${f1(6 * s)}" fill="#b8e0a0" opacity=".7"/>`; };
    [[80, 380], [130, 250], [250, 170], [760, 220], [850, 420], [880, 640], [860, 980], [700, 1040], [120, 1000], [70, 700], [560, 640], [240, 660], [340, 300], [600, 380], [720, 960], [520, 980], [180, 420], [-200, 480], [1000, 700], [-160, 900], [960, 300], [460, 40], [180, 1240], [700, 1260]]
      .forEach(([x, y]) => (m += tree(x, y, 0.9 + r() * 0.5)));
    // roads: laterite lanes (edge, body, worn centre) and the asphalt highway with its centre dashes
    const R = VIL.roads, line = (pts) => smooth(pts);
    m += `<path d="${line(R.highway)}" stroke="#3a2a10" stroke-width="56" opacity=".14" fill="none" transform="translate(4,8)"/><path d="${line(R.highway)}" stroke="#5e626a" stroke-width="52" fill="none"/><path d="${line(R.highway)}" stroke="#80848c" stroke-width="44" fill="none"/><path d="${line(R.highway)}" stroke="#fffaf0" stroke-width="4" fill="none" stroke-dasharray="26 22"/>`;
    ["main", "south", "north", "west", "east"].forEach((k) => { const d = line(R[k]); m += `<path d="${d}" stroke="#a8683e" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="#d99a66" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="#e8b484" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/>`; });
    // the gate over the village road, its name
    const [gx, gy] = VIL.gate;
    m += `<g transform="translate(${gx},${gy})"><rect x="-44" y="-10" width="14" height="20" rx="3" fill="#e2cca4" stroke="${INK}" stroke-width="3"/><rect x="30" y="-10" width="14" height="20" rx="3" fill="#e2cca4" stroke="${INK}" stroke-width="3"/><rect x="-50" y="-4" width="100" height="8" rx="3" fill="#9a2218" stroke="${INK}" stroke-width="2.4"/></g>`;
    // houses: roofs from above (hip or gable), a soft shadow, the red shirt at the door
    const shirt = (x, y) => `<path d="M${x - 7},${y - 6}l4,-3h6l4,3l-2,4h-2v8h-8v-8h-2z" fill="#e2382e" stroke="#6a1410" stroke-width="1.6" stroke-linejoin="round"/>`;
    const roofC = ["#c8664a", "#9aa8b8", "#b89a7a", "#d88a5a", "#8a9aaa", "#c87858"];
    const house = (x, y, a, w = 56, h = 40, c = roofC[Math.floor(r() * roofC.length)], door = 1) => {
      let t = `<g transform="translate(${x},${y}) rotate(${a})"><rect x="${-w / 2 + 5}" y="${-h / 2 + 8}" width="${w}" height="${h}" rx="3" fill="#3a2a10" opacity=".2"/>
        <rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="3" fill="${c}" stroke="${INK}" stroke-width="2.6"/><path d="M${-w / 2 + 8},0H${w / 2 - 8}" stroke="${INK}" stroke-width="2.4" opacity=".55"/>
        <path d="M${-w / 2},${-h / 2}L${-w / 2 + 8},0L${-w / 2},${h / 2}M${w / 2},${-h / 2}L${w / 2 - 8},0L${w / 2},${h / 2}" stroke="${INK}" stroke-width="1.8" fill="none" opacity=".4"/>
        <path d="M${-w / 2 + 3},${-h / 2 + 3}H${w / 2 - 3}" stroke="#fff" stroke-width="3" opacity=".35"/>`;
      if (door) t += shirt(0, h / 2 + 12);
      return t + `</g>`;
    };
    const HS = [[212, 806, 0, 70, 46, "#c8664a"], [338, 942, 180, 60, 42, "#9aa8b8"], [120, 806, 0], [300, 806, 0], [520, 806, 0], [610, 806, 0], [700, 810, 0], [180, 942, 180], [480, 942, 180], [580, 946, 180], [680, 946, 180],
      [200, 470, 0], [290, 470, 0], [650, 470, 0], [730, 470, 0], [200, 600, 180], [290, 600, 180], [560, 600, 180], [740, 600, 180], [360, 700, 90], [500, 700, 270], [520, 260, 0], [380, 220, 0], [180, 330, 0], [740, 330, 0], [840, 760, 270], [60, 640, 90]];
    HS.forEach(([x, y, a, w, h, c]) => (m += house(x, y, a, w, h, c)));
    // the sala (open pavilion: a tiled hip roof, the white floor edge), the temple, the loudspeaker tower
    const [sx, sy] = VIL.sala;
    m += `<g transform="translate(${sx},${sy})"><rect x="-58" y="-36" width="124" height="80" rx="4" fill="#3a2a10" opacity=".2"/><rect x="-62" y="-44" width="124" height="80" rx="4" fill="#f4efe4" stroke="${INK}" stroke-width="2.6"/>
      <path d="M-54,-38H54V30H-54Z" fill="#e89a4a" stroke="${INK}" stroke-width="2.6"/><path d="M-54,-38L-24,-4H24L54,-38M-54,30L-24,-4M54,30L24,-4" stroke="${INK}" stroke-width="2.2" fill="none" opacity=".6"/></g>`;
    const [wx, wy] = VIL.wat;
    m += `<g transform="translate(${wx},${wy})"><rect x="-56" y="-30" width="118" height="70" rx="4" fill="#3a2a10" opacity=".2"/><rect x="-60" y="-36" width="120" height="72" rx="4" fill="#e8b040" stroke="${INK}" stroke-width="2.6"/><rect x="-44" y="-24" width="88" height="48" rx="3" fill="#c8402a" stroke="${INK}" stroke-width="2"/><path d="M-44,0H44" stroke="#ffd870" stroke-width="5"/>
      <circle cx="96" cy="-6" r="26" fill="#f4efe4" stroke="${INK}" stroke-width="2.6"/><circle cx="96" cy="-6" r="12" fill="#e8b040" stroke="${INK}" stroke-width="2"/><circle cx="96" cy="-6" r="3" fill="${INK}"/></g>`;
    const [tx, ty] = VIL.tower;
    m += `<g transform="translate(${tx},${ty})"><circle r="14" fill="#c8ccd0" stroke="${INK}" stroke-width="2.6"/>${[0, 90, 180, 270].map((a) => `<path d="M0,0L22,0" stroke="${INK}" stroke-width="3" transform="rotate(${a + 45})"/><circle cx="24" cy="0" r="5" fill="#e8e2d4" stroke="${INK}" stroke-width="2" transform="rotate(${a + 45})"/>`).join("")}</g>`;
    // the town on the highway: blocks of grey roofs, and the hospital (white, the red cross on its roof, the ambulance bay)
    if (o.town !== false) {
      m += `<path d="M960,960C1060,900 1300,900 1440,960C1520,1000 1520,1260 1440,1300C1300,1360 1040,1340 960,1280C900,1230 900,1000 960,960Z" fill="#e8e2d6" stroke="#c8bca4" stroke-width="4"/>`;
      [[1010, 1000], [1080, 1000], [1150, 990], [1010, 1240], [1090, 1250], [1170, 1250], [1380, 1000], [1400, 1250], [1320, 1250]].forEach(([x, y]) => (m += house(x, y, 0, 52, 40, ["#9aa0a8", "#b0b4ba", "#8a9098"][Math.floor(r() * 3)], 0)));
      const [hx, hy] = VIL.hospital;
      m += `<g transform="translate(${hx},${hy})"><rect x="-74" y="-48" width="160" height="104" rx="6" fill="#3a2a10" opacity=".2"/><rect x="-80" y="-56" width="160" height="104" rx="6" fill="#fbfbf8" stroke="${INK}" stroke-width="3"/>
        <rect x="-70" y="-46" width="140" height="84" rx="4" fill="#e8f0f4" stroke="#b8c8d0" stroke-width="2"/><path d="M0,-30V22M-26,-4H26" stroke="#e2382e" stroke-width="14"/><rect x="-34" y="48" width="68" height="16" rx="3" fill="#c8ccd0" stroke="${INK}" stroke-width="2"/></g>`;
    }
    if (o.name) m += `<g transform="translate(${gx + 120},${gy + 92})"><g filter="url(#mpDrop)">${label(o.name, textW(o.name, 30) - 8)}</g></g>`;
    m += routeLayer(id, o.route || [VIL.piak, VIL.sala], o);
    put(L.set, G(m));
  }

  window.Maps = { route, P, VEH, smooth, VIL, ICON };
  Object.assign(Sets, { mapTH, mapVillage });
})();
