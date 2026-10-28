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
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
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
    // the route: a white underlay and a red dashed line, both revealed by #id-reveal drawing on inside a mask
    const pts = (o.route || [[100.52, 13.75], [103.55, 16.25]]).map(([lo, la]) => P(lo, la)), rd = smooth(pts);
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
    // arrival: the end pin drops, the shadow lands, a ripple ring, the label pops
    tl.fromTo(`#${id}-pin1`, { y: -200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: "bounce.out", immediateRender: false }, t0 + g1 - 0.1);
    tl.to(`#${id}-sh1`, { scale: 1, duration: 0.7, ease: "bounce.out" }, t0 + g1 - 0.1);
    tl.fromTo(`#${id}-rip`, { opacity: 0.9, scale: 0.3, svgOrigin: "0 0" }, { opacity: 0, scale: 2.6, duration: 0.8, ease: "power2.out", immediateRender: false }, t0 + g1 + 0.25);
    tl.fromTo(`#${id}-lab1`, { opacity: 0, scale: 0, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.6)", immediateRender: false }, t0 + g1 + 0.35);
    tl.to(`#${id}-car`, { opacity: 0, duration: 0.3 }, t0 + g1 + 0.1);
  }

  window.Maps = { route, P, VEH, smooth };
  Object.assign(Sets, { mapTH });
})();
