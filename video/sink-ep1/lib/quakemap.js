// "ตึกโยก" — the real quake (28 มี.ค. 2568) on a 3D relief map: Myanmar → Bangkok. Load after maps.js and quakeui.js.
// Not a picture: the Natural Earth polygons of mapsdata.js are projected every frame by a perspective camera looking down at a ground
// plane, so the camera can fly, tilt and orbit and every slab, mountain, cloud and tower keeps its depth. Everything inside the map
// group is a pure function of the shot time (redrawn from one proxy tween), so seeking to any frame gives the right picture.
//   Sets.qkMap3d(L, o)                 the map in L.set (o.id): sea with shallows and a graticule, land as slabs with shaded walls
//                                      (Thailand one step higher with a lit rim), low-poly mountains on the real ranges, rivers, country
//                                      names lying on the ground, clouds with their shadows, haze; draws the first frame of the flight
//   QkUI.quakeMap3d(tl, L, sid, t0, o) the quake and the camera flight: o.dur (shot length), o.chipAt (the date chip, screen top),
//                                      o.labelAt ("เมียนมา · ขนาด 8.2" at the epicentre), o.bkkAt (the Bangkok pin drops, its label pops),
//                                      o.count [c0, c1] (the card "ตึกสูงโยกนานกว่า N วินาที" counts 0 → 20+ above Bangkok), o.out (the
//                                      chip leaves), o.cam (override the flight: [{ t, lon, lat, tilt, yaw, S, cy }]). The epicentre
//                                      bursts at once with a red ground glow and a crack; rings run along the ground (mountains jolt as
//                                      the front passes) and reach Bangkok at o.wave (default 4.45 s), where the towers start to sway.
//                                      Frame the shot with a fixed identity camera: cam: { keys: [{ t: 0, ...fr(540, 960, 1, 540, 960, { drift: { s: 0 } }) }] }
//   QkMap3D.P(lon, lat) / QkMap3D.LL(u, v)   map units ↔ degrees · QkMap3D.FLIGHT the default camera keys
(function () {
  const f1 = (v) => (+v).toFixed(1);
  const put = (el, html) => el.insertAdjacentHTML("beforeend", html);
  const mk = (seed) => () => { seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const PI = Math.PI, RAD = PI / 180;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const smooth = (k) => { k = clamp(k); return k * k * (3 - 2 * k); };
  const ease3 = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
  const easeOut2 = (k) => { k = clamp(k); return 1 - (1 - k) * (1 - k); };
  const backOut = (k, s = 2.2) => { k = clamp(k) - 1; return 1 + (s + 1) * k * k * k + s * k * k; };
  const bounceOut = (k) => { k = clamp(k); const n = 7.5625, d = 2.75; if (k < 1 / d) return n * k * k; if (k < 2 / d) return n * (k -= 1.5 / d) * k + 0.75; if (k < 2.5 / d) return n * (k -= 2.25 / d) * k + 0.9375; return n * (k -= 2.625 / d) * k + 0.984375; };
  const hx = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, k) => { const A = hx(a), B = hx(b); k = clamp(k); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const D = () => window.MAPDATA.th;
  const P = (lon, lat) => { const d = D(); return [d.tx + d.k * lon * RAD, d.ty - d.k * Math.log(Math.tan(PI / 4 + (lat * RAD) / 2))]; };
  const LL = (u, v) => { const d = D(); return [(u - d.tx) / d.k / RAD, (2 * Math.atan(Math.exp((d.ty - v) / d.k)) - PI / 2) / RAD]; };

  const H = 12, HTH = 17;                      // land slab height and Thailand's (map units; 1° of longitude ≈ 79 units)
  const WIN = [86, 112, 0.5, 31];              // lon0, lon1, lat0, lat1: what gets drawn at all
  const LN = (() => { const v = [-0.55, -0.62, 0.62], l = Math.hypot(...v); return v.map((x) => x / l); })(); // light from the north-west, above
  const EPI = [95.9, 22.0], BKK = [100.5, 13.75];
  const STAR = "M0,-42l12,24l28,-7l-16,23l22,18l-29,2l-2,29l-15,-24l-15,24l-2,-29l-29,-2l22,-18l-16,-23l28,7z";
  const V = 185;                               // ring speed, map units per second (reaches Bangkok ≈ 4.15 s after it starts)
  const F = 2500;                              // focal length in px

  // the default flight: wide over both, a breath, then a dolly + tilt down onto Bangkok, a slow orbit to the end
  const FLIGHT = [
    { t: 0, lon: 98.1, lat: 17.0, tilt: 35, yaw: -8, S: 1.2, cy: 980 },
    { t: 3.6, lon: 98.2, lat: 16.85, tilt: 38, yaw: -6, S: 1.28, cy: 980 },
    { t: 6.7, lon: 100.5, lat: 13.92, tilt: 56, yaw: 5, S: 4.6, cy: 1110 },
    { t: 9.2, lon: 100.5, lat: 13.9, tilt: 60, yaw: 11, S: 5.2, cy: 1110 },
  ];

  Sets.DEFS += `
    <linearGradient id="qmSea" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1920"><stop offset="0" stop-color="#a9d3df"/><stop offset=".3" stop-color="#5aa9c6"/><stop offset=".62" stop-color="#2d84ad"/><stop offset="1" stop-color="#1c6893"/></linearGradient>
    <linearGradient id="qmHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6f1f2" stop-opacity=".97"/><stop offset=".45" stop-color="#e6f1f2" stop-opacity=".62"/><stop offset="1" stop-color="#e6f1f2" stop-opacity="0"/></linearGradient>
    <linearGradient id="qmSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe5ee"/><stop offset="1" stop-color="#e9f3f2"/></linearGradient>
    <linearGradient id="qmStar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2a0"/><stop offset=".55" stop-color="#ffd23a"/><stop offset="1" stop-color="#f29a1a"/></linearGradient>
    <radialGradient id="qmEpi"><stop offset="0" stop-color="#ffe08a" stop-opacity=".95"/><stop offset=".25" stop-color="#ff8a3a" stop-opacity=".75"/><stop offset=".65" stop-color="#e8382a" stop-opacity=".32"/><stop offset="1" stop-color="#e8382a" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmBurst"><stop offset="0" stop-color="#fff6c8"/><stop offset=".3" stop-color="#ffb04a" stop-opacity=".9"/><stop offset=".65" stop-color="#ff5a2a" stop-opacity=".35"/><stop offset="1" stop-color="#e8382a" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmCloud"><stop offset="0" stop-color="#ffffff" stop-opacity=".96"/><stop offset=".62" stop-color="#fbfdff" stop-opacity=".85"/><stop offset="1" stop-color="#eef6fa" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmCloudB"><stop offset="0" stop-color="#9fb6c4" stop-opacity=".55"/><stop offset="1" stop-color="#9fb6c4" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmShade"><stop offset="0" stop-color="#0b2a3c" stop-opacity=".26"/><stop offset=".6" stop-color="#0b2a3c" stop-opacity=".12"/><stop offset="1" stop-color="#0b2a3c" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmCity"><stop offset="0" stop-color="#b9ae98" stop-opacity=".75"/><stop offset=".7" stop-color="#cfc4ac" stop-opacity=".35"/><stop offset="1" stop-color="#cfc4ac" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmGreen"><stop offset="0" stop-color="#a9c47c" stop-opacity=".55"/><stop offset=".6" stop-color="#b8cc8a" stop-opacity=".25"/><stop offset="1" stop-color="#b8cc8a" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmPaddy"><stop offset="0" stop-color="#d8e6a0" stop-opacity=".6"/><stop offset=".65" stop-color="#dfe8ae" stop-opacity=".28"/><stop offset="1" stop-color="#dfe8ae" stop-opacity="0"/></radialGradient>
    <radialGradient id="qmPulse"><stop offset=".55" stop-color="#ffd23a" stop-opacity="0"/><stop offset=".85" stop-color="#ffd23a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd23a" stop-opacity="0"/></radialGradient>
    <linearGradient id="qmPin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a64"/><stop offset=".55" stop-color="#e2392c"/><stop offset="1" stop-color="#a81c16"/></linearGradient>
    <linearGradient id="qmFaceD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2e25"/><stop offset="1" stop-color="#140e0a"/></linearGradient>
    <linearGradient id="qmFaceC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#eadcbc"/></linearGradient>
    <radialGradient id="qmSoft"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>`;

  // ---------------- geometry helpers ----------------
  const parse = (s) => s.split("M").filter(Boolean).map((r) => r.replace(/Z/g, "").split("L").map((p) => p.split(",").map(Number)));
  function dpOpen(pts, eps) {
    const n = pts.length; if (n < 3) return pts.slice();
    const keep = new Uint8Array(n); keep[0] = keep[n - 1] = 1;
    const st = [[0, n - 1]];
    while (st.length) {
      const [a, b] = st.pop(); const [ax, ay] = pts[a], [bx, by] = pts[b], dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy || 1e-9;
      let md = -1, mi = -1;
      for (let i = a + 1; i < b; i++) { const [px, py] = pts[i]; let t = ((px - ax) * dx + (py - ay) * dy) / L2; t = clamp(t); const ex = ax + t * dx - px, ey = ay + t * dy - py, d = ex * ex + ey * ey; if (d > md) { md = d; mi = i; } }
      if (mi > 0 && md > eps * eps) { keep[mi] = 1; st.push([a, mi], [mi, b]); }
    }
    return pts.filter((_, i) => keep[i]);
  }
  function dpRing(pts, eps) {
    if (pts.length < 8) return pts;
    let j = 0, md = -1; const [x0, y0] = pts[0];
    pts.forEach(([x, y], i) => { const d = (x - x0) ** 2 + (y - y0) ** 2; if (d > md) { md = d; j = i; } });
    const a = dpOpen(pts.slice(0, j + 1), eps), b = dpOpen(pts.slice(j).concat([pts[0]]), eps);
    return a.concat(b.slice(1, -1));
  }
  function clipEdge(pts, fn) { // keep fn ≥ 0 (Sutherland–Hodgman, one plane)
    const out = [], n = pts.length;
    for (let i = 0; i < n; i++) {
      const a = pts[i], b = pts[(i + 1) % n], fa = fn(a), fb = fn(b);
      if (fa >= 0) out.push(a);
      if ((fa >= 0) !== (fb >= 0)) { const k = fa / (fa - fb); out.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]); }
    }
    return out;
  }
  const chaikin = (pts, it) => { for (let k = 0; k < it; k++) { const out = []; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; out.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25], [a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } pts = out; } return pts; };
  // a Catmull-Rom curve through a polyline, n points per span, with a gentle meander (rivers)
  const spline = (pts, n, r, wig = 0) => {
    const out = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)], dx = p2[0] - p1[0], dy = p2[1] - p1[1], l = Math.hypot(dx, dy) || 1, ph = r() * 6;
      for (let k = 0; k < n; k++) {
        const t = k / n, t2 = t * t, t3 = t2 * t, c = [0, 1].map((j) => 0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3));
        const m = wig * Math.sin(t * PI * 3 + ph) * Math.sin(t * PI);
        out.push([c[0] - (dy / l) * m, c[1] + (dx / l) * m]);
      }
    }
    out.push(pts[pts.length - 1]);
    return out;
  };
  const area = (r) => { let A = 0; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length]; A += a[0] * b[1] - b[0] * a[1]; } return A / 2; };
  const inRing = (r, x, y) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
  const prepRing = (pts) => { const A = area(pts), s = A > 0 ? 1 : -1; const n = pts.map((a, i) => { const b = pts[(i + 1) % pts.length], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; return [(s * dy) / l, (-s * dx) / l]; }); return { pts, n }; };
  const lp = (pts) => pts.map(([lo, la]) => P(lo, la));

  // the land west of Myanmar is not in mapsdata.js: a rough Bangladesh / India coast so the Bay of Bengal ends where it should
  const WEST = [[92.3, 20.75], [93.2, 21.3], [94.6, 22.6], [95.6, 24.6], [97.4, 27.6], [97.6, 31.5], [85, 31.5], [78, 31.5], [78, 14], [80.3, 15.6], [81.2, 16.3], [82.3, 17.0], [83.3, 17.7],
    [84.8, 19.3], [85.8, 19.85], [86.4, 20.1], [86.9, 20.8], [87.1, 21.5], [88.0, 21.65], [88.7, 21.62], [89.4, 21.8], [90.2, 21.9], [90.6, 22.2], [91.1, 22.45], [91.5, 22.6], [91.85, 22.25], [92.0, 21.4]];
  // ranges: [polyline (lon, lat), step (deg), spread (deg), height min, max]
  const RANGES = [
    [[[98.62, 20.0], [98.5, 18.6], [98.62, 17.3]], 0.26, 0.22, 15, 26],          // Thanon Thong Chai (Doi Inthanon)
    [[[99.35, 19.6], [99.42, 18.2], [99.3, 17.6]], 0.3, 0.2, 12, 19],            // Khun Tan
    [[[100.1, 20.1], [100.3, 18.9], [100.15, 17.9]], 0.3, 0.25, 12, 20],         // Phi Pan Nam
    [[[101.0, 19.7], [101.05, 18.5], [101.15, 17.6]], 0.3, 0.2, 12, 19],         // Luang Prabang range (border)
    [[[101.2, 17.4], [101.25, 16.3], [101.3, 15.4]], 0.32, 0.22, 10, 16],        // Phetchabun
    [[[101.4, 15.0], [102.0, 14.45], [102.6, 14.25]], 0.34, 0.15, 8, 13],        // Dong Phaya Yen
    [[[102.7, 14.3], [103.6, 14.35], [104.6, 14.4]], 0.4, 0.08, 6, 9],           // Dângrêk
    [[[103.0, 12.4], [103.4, 11.7], [104.0, 11.2]], 0.32, 0.25, 10, 16],         // Cardamom
    [[[97.0, 23.9], [97.2, 22.4], [97.15, 21.0], [97.0, 19.9]], 0.3, 0.32, 11, 21], // Shan hills, west edge
    [[[98.1, 23.6], [98.35, 22.0], [98.2, 20.8], [98.0, 19.6]], 0.3, 0.35, 12, 22],  // Shan hills
    [[[99.1, 22.4], [99.4, 21.2], [99.6, 20.6]], 0.32, 0.3, 11, 19],
    [[[97.35, 19.4], [97.8, 18.2], [98.25, 17.0]], 0.28, 0.2, 11, 18],          // Karen hills / Dawna
    [[[98.6, 16.3], [98.95, 14.6], [99.15, 13.1], [99.25, 11.9], [98.9, 10.6], [98.7, 9.7]], 0.3, 0.18, 11, 19], // Tenasserim
    [[[93.6, 24.1], [93.75, 22.6], [94.2, 20.6], [94.6, 18.8], [94.8, 17.5], [94.9, 16.5]], 0.3, 0.22, 12, 21], // Chin hills, Arakan Yoma
    [[[95.85, 19.9], [96.15, 18.3], [96.3, 17.3]], 0.36, 0.15, 6, 9],            // Bago Yoma
    [[[96.4, 26.4], [97.4, 25.0], [97.8, 24.0]], 0.34, 0.3, 14, 24],             // Kachin
    [[[99.4, 25.8], [100.6, 24.7], [102.0, 24.2], [103.4, 23.8]], 0.36, 0.45, 15, 26], // Yunnan
    [[[101.8, 21.6], [102.6, 20.7], [103.6, 20.3]], 0.32, 0.3, 12, 20],          // northern Laos
    [[[103.6, 22.5], [104.6, 21.8]], 0.34, 0.25, 14, 22],                        // Hoang Lien Son
    [[[103.7, 20.3], [104.6, 19.0], [105.6, 18.0], [106.6, 16.8], [107.3, 15.8], [107.8, 14.6], [108.2, 13.3], [108.3, 12.1]], 0.3, 0.25, 12, 20], // Annamite
    [[[101.25, 6.3], [101.6, 5.0], [101.9, 3.7], [102.2, 2.9]], 0.3, 0.2, 11, 18], // Titiwangsa
    [[[98.95, 9.6], [99.7, 8.8], [99.95, 7.7], [100.35, 6.75]], 0.3, 0.14, 8, 13], // southern Thailand
  ];
  const RIVERS = [
    [[100.58, 13.52], [100.5, 13.75], [100.52, 14.0], [100.57, 14.35], [100.4, 14.8], [100.2, 15.2], [100.12, 15.7], [99.85, 16.1], [99.55, 16.5], [99.12, 16.88], [98.95, 17.6], [98.98, 18.3], [98.99, 18.79], [98.95, 19.3]], // Chao Phraya · Ping
    [[100.12, 15.7], [100.27, 16.4], [100.26, 16.82], [100.4, 17.6], [100.78, 18.78]], // Nan
    [[97.4, 25.4], [96.9, 24.3], [96.2, 23.0], [96.05, 22.0], [95.4, 21.6], [95.0, 21.3], [94.9, 20.5], [94.95, 20.0], [95.1, 19.2], [95.2, 18.8], [95.4, 17.7], [95.45, 17.0], [95.2, 16.5], [95.0, 15.95]], // Irrawaddy
    [[98.9, 25.5], [98.7, 24.0], [98.2, 22.6], [98.0, 21.3], [97.7, 20.0], [97.75, 18.6], [97.75, 17.9], [97.6, 17.0], [97.62, 16.5]], // Salween
    [[101.2, 21.6], [100.6, 20.8], [100.2, 20.35], [101.0, 20.0], [102.13, 19.89], [101.7, 19.0], [101.9, 18.2], [102.6, 17.97], [103.5, 18.3], [104.0, 17.9], [104.8, 17.4], [104.75, 16.5], [105.6, 15.6], [105.8, 15.1], [105.9, 14.0], [106.0, 13.4], [105.95, 12.5], [105.4, 11.9], [104.92, 11.56], [105.2, 11.0], [105.6, 10.5], [106.4, 10.0], [106.7, 9.65]], // Mekong
  ];
  const NAMES = [["เมียนมา", 96.9, 19.3, 30, 0], ["ลาว", 102.6, 19.6, 24, 0], ["กัมพูชา", 104.6, 12.85, 22, 0], ["เวียดนาม", 106.8, 15.6, 22, 0], ["มาเลเซีย", 102.2, 4.6, 20, 0], ["อ่าวไทย", 101.0, 10.7, 22, 1], ["ทะเลอันดามัน", 96.4, 12.2, 20, 1]];

  // ---------------- data, built once ----------------
  let DATA = null;
  function data() {
    if (DATA) return DATA;
    const d = D(), [wx0, wy0] = P(WIN[0], WIN[3]), [wx1, wy1] = P(WIN[1], WIN[2]);
    const clipWin = (r) => [[(p) => p[0] - wx0], [(p) => wx1 - p[0]], [(p) => p[1] - wy0], [(p) => wy1 - p[1]]].reduce((pts, [fn]) => (pts.length ? clipEdge(pts, fn) : pts), r);
    const prep = (rings, eps, sm) => rings.map((r) => clipWin(chaikin(dpRing(r, eps), sm))).filter((r) => r.length >= 3 && Math.abs(area(r)) > 6).map(prepRing);
    const nb = Object.entries(d.nb).map(([k, s]) => ({ k, rings: prep(parse(s), k === "china" ? 1.6 : 1.1, k === "china" ? 0 : 1) }));
    const west = { k: "west", rings: prep([chaikin(lp(WEST), 2)], 1, 0) };
    const th = { k: "th", rings: prep(parse(d.th), 0.9, 2) };
    const neigh = [west, ...nb];
    // Thailand's edges: land borders (the step up from the neighbours) or coasts (the full wall down to the sea)
    const allNb = neigh.flatMap((l) => l.rings.map((r) => r.pts));
    th.rings.forEach((R) => { R.border = R.pts.map((a, i) => { const b = R.pts[(i + 1) % R.pts.length], mx = (a[0] + b[0]) / 2 + R.n[i][0] * 2.2, my = (a[1] + b[1]) / 2 + R.n[i][1] * 2.2; return allNb.some((q) => inRing(q, mx, my)); }); });
    // a height grid: 0 sea, 1 land, 2 Thailand (scanline fill)
    const cs = 3, nx = Math.ceil((wx1 - wx0) / cs), ny = Math.ceil((wy1 - wy0) / cs), grid = new Uint8Array(nx * ny);
    const fill = (rings, code) => rings.forEach(({ pts }) => {
      for (let j = 0; j < ny; j++) {
        const y = wy0 + (j + 0.5) * cs, xs = [];
        for (let i = 0; i < pts.length; i++) { const [x1, y1] = pts[i], [x2, y2] = pts[(i + 1) % pts.length]; if ((y1 > y) !== (y2 > y)) xs.push(x1 + ((y - y1) * (x2 - x1)) / (y2 - y1)); }
        xs.sort((a, b) => a - b);
        for (let k = 0; k + 1 < xs.length; k += 2) { const i0 = Math.max(0, Math.ceil((xs[k] - wx0) / cs - 0.5)), i1 = Math.min(nx - 1, Math.floor((xs[k + 1] - wx0) / cs - 0.5)); for (let i = i0; i <= i1; i++) grid[j * nx + i] = Math.max(grid[j * nx + i], code); }
      }
    });
    neigh.forEach((l) => fill(l.rings, 1)); fill(th.rings, 2);
    const code = (u, v) => { const i = Math.floor((u - wx0) / cs), j = Math.floor((v - wy0) / cs); return i < 0 || j < 0 || i >= nx || j >= ny ? 0 : grid[j * nx + i]; };
    const hAt = (u, v) => [0, H, HTH][code(u, v)];
    // mountains along the ranges (only on land, not hugging a coast)
    const r = mk(77), peaks = [];
    RANGES.forEach(([line, step, spread, h0, h1]) => {
      const pts = line.map(([lo, la]) => [lo, la]);
      for (let s = 0; s < pts.length - 1; s++) {
        const [a0, a1] = pts[s], [b0, b1] = pts[s + 1], len = Math.hypot(b0 - a0, b1 - a1), n = Math.max(1, Math.round(len / (step * 1.45))), px = -(b1 - a1) / len, py = (b0 - a0) / len;
        for (let k = 0; k < n; k++) {
          const q = (k + r() * 0.6) / n, cnt = r() < 0.55 ? 2 : 1;
          for (let c = 0; c < cnt; c++) {
            const off = (r() * 2 - 1) * spread, lo = a0 + (b0 - a0) * q + px * off, la = a1 + (b1 - a1) * q + py * off, [u, v] = P(lo, la);
            const hh = (h0 + r() * (h1 - h0)) * 1.45, rad = hh * (0.9 + r() * 0.45);
            const cc = code(u, v);
            if (!cc || [[rad, 0], [-rad, 0], [0, rad], [0, -rad]].some(([du, dv]) => !code(u + du, v + dv))) continue;
            const base = Array.from({ length: 6 }, (_, i) => { const a = (i / 6) * PI * 2 + r() * 0.45, rr = rad * (0.72 + r() * 0.4); return [Math.cos(a) * rr, Math.sin(a) * rr]; });
            peaks.push({ u, v, z: [0, H, HTH][cc], h: hh, r: rad, base, au: (r() - 0.5) * rad * 0.3, av: (r() - 0.5) * rad * 0.3, tint: r(), ph: r() * 6 });
          }
        }
      }
    });
    const rr0 = mk(53), rivers = RIVERS.map((l) => spline(lp(l), 7, rr0, 2.2));
    // vegetation tints: forest on the ranges, paddies on the central plain
    const tints = [];
    RANGES.forEach(([line]) => line.forEach(([lo, la]) => { const [u, v] = P(lo, la); if (code(u, v)) tints.push([u, v, 34 + r() * 20, "qmGreen"]); }));
    [[100.2, 15.2, 70], [100.35, 14.4, 60], [99.9, 16.2, 55], [102.8, 15.6, 80], [104.0, 16.0, 70], [95.6, 20.8, 60], [95.4, 18.4, 55], [95.6, 17.2, 60], [105.2, 10.6, 55]].forEach(([lo, la, rr]) => { const [u, v] = P(lo, la); tints.push([u, v, rr, "qmPaddy"]); });
    // Bangkok: a few tall towers and a ring of low blocks, all on Thailand's top
    const [bu, bv] = P(...BKK), towers = [], rt = mk(905);
    const spots = [[0, 0, 30], [-5, -3, 22], [5.2, -2.5, 25], [-2.5, 4.5, 18], [3.6, 4.2, 20], [-8.5, 2, 14], [8.6, 1.5, 15], [-1, -7.2, 16], [6.5, -7, 12], [-6.8, -7.5, 11], [1.8, 9, 10], [-6, 8.5, 9], [10.5, 7.5, 8], [-11, -2.5, 8], [12, -4, 9], [-3, -11, 10]];
    const PAL = [["#3d6a8c", "#d4ecf8"], ["#2f6f78", "#c8f0ee"], ["#8a8478", "#f6f0e2"]];
    spots.forEach(([du, dv, hh], i) => { const w = 3.4 + rt() * 2.0, dd = 3.2 + rt() * 1.8; if (hAt(bu + du * 1.8, bv + dv * 1.8) !== HTH) return; towers.push({ u: bu + du * 1.8 - w / 2, v: bv + dv * 1.8 - dd / 2, w, d: dd, h: hh * 1.8 * (0.9 + rt() * 0.2), f: 0.7 + (30 - hh) * 0.022 + rt() * 0.12, ph: rt() * 6, low: false, pal: i === 0 ? PAL[0] : PAL[Math.floor(rt() * 3)], spire: i === 0 }); });
    for (let k = 0; k < 46; k++) { const a = rt() * PI * 2, rr = 14 + rt() * 20, du = Math.cos(a) * rr * 1.2, dv = Math.sin(a) * rr; if (hAt(bu + du, bv + dv) !== HTH) continue; const w = 2.2 + rt() * 2.4; towers.push({ u: bu + du, v: bv + dv, w, d: 2 + rt() * 2.2, h: 2 + rt() * 5, f: 0, ph: 0, low: true }); }
    // clouds (kept away from Bangkok and the epicentre)
    const rc = mk(31), clouds = [], [eu, ev] = P(...EPI);
    for (let k = 0; clouds.length < 11 && k < 200; k++) {
      const lo = 93 + rc() * 13, la = 9 + rc() * 15, [u, v] = P(lo, la);
      if (Math.hypot(u - bu, v - bv) < 150 || Math.hypot(u - eu, v - ev) < 110) continue;
      clouds.push({ u, v, z: 58 + rc() * 30, r: 30 + rc() * 40, blobs: Array.from({ length: 5 }, (_, i) => [(i - 2) * 0.42 + (rc() - 0.5) * 0.2, (rc() - 0.5) * 0.35 - (i % 2 ? 0.18 : 0), 0.42 + rc() * 0.32]) });
    }
    // the crack across the epicentre, roughly north–south
    const rk = mk(19), crack = [];
    for (let k = 0; k <= 16; k++) { const q = k / 16 - 0.5; crack.push([eu + q * 22 + (k % 2 ? 1 : -1) * (2 + rk() * 3.5), ev + q * 250]); }
    // glints on the water
    const rg = mk(211), glints = [];
    for (let k = 0; glints.length < 220 && k < 4000; k++) { const lo = 92 + rg() * 16, la = 4 + rg() * 20, [u, v] = P(lo, la); if (code(u, v) || code(u + 8, v) || code(u - 8, v)) continue; glints.push([u, v, 1.5 + rg() * 3, rg() * 6, 0.6 + rg() * 0.8]); }
    DATA = { neigh, th, peaks, rivers, tints, towers, clouds, crack, glints, hAt, code, bkk: [bu, bv], epi: [eu, ev], win: [wx0, wy0, wx1, wy1] };
    return DATA;
  }

  // ---------------- camera ----------------
  function camAt(keys, t) {
    let i = 0;
    while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
    const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
    if (a === b || t <= a.t) return { ...a };
    const k = clamp((t - a.t) / (b.t - a.t)), e = i === 1 ? ease3(k) : i === 0 ? smooth(k) : easeOut2(k);
    const S = a.S * Math.pow(b.S / a.S, e);
    // pan so that the destination glides toward its screen spot as the zoom grows (no lurch at the end of the dolly)
    const [ua, va] = P(a.lon, a.lat), [ub, vb] = P(b.lon, b.lat), w = 1 - (1 - e) * (a.S / S);
    const lerp = (x, y) => x + (y - x) * e;
    return { u: ua + (ub - ua) * w, v: va + (vb - va) * w, tilt: lerp(a.tilt, b.tilt), yaw: lerp(a.yaw, b.yaw), S, cy: lerp(a.cy, b.cy), uv: true };
  }
  function camera(c) {
    const [u, v] = c.uv ? [c.u, c.v] : P(c.lon, c.lat), t = c.tilt * RAD, y = c.yaw * RAD, dist = F / c.S;
    const C = { u, v, st: Math.sin(t), ct: Math.cos(t), sy: Math.sin(y), cyw: Math.cos(y), dist, S: c.S, cx: 540, cy: c.cy, tilt: c.tilt };
    C.gu = u - dist * C.st * C.sy; C.gv = v + dist * C.st * C.cyw; C.gz = dist * C.ct;
    C.near = dist * 0.16;
    return C;
  }
  const proj = (C, u, v, z) => {
    const dx = u - C.u, dy = v - C.v, x = dx * C.cyw + dy * C.sy, y = -dx * C.sy + dy * C.cyw, dep = C.dist - y * C.st - z * C.ct;
    return [C.cx + (F * x) / dep, C.cy + (F * (y * C.ct - z * C.st)) / dep, dep];
  };
  // keep the part of the ground in front of the near plane at height z
  const nearFn = (C, z) => { const lim = (C.dist - C.near - z * C.ct) / C.st; return (p) => lim - (-(p[0] - C.u) * C.sy + (p[1] - C.v) * C.cyw); };
  // clip a ring, remembering which original edge each output edge belongs to (-1 = the clip line)
  function clipRingE(pts, fn) {
    const n = pts.length, f = pts.map(fn);
    if (f.every((x) => x >= 0)) return pts.map((p, i) => [p[0], p[1], i]);
    const out = [];
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n, a = pts[i], b = pts[j];
      if (f[i] >= 0) out.push([a[0], a[1], i]);
      // an exit point starts the clip line (-1), an entry point continues its original edge
      if ((f[i] >= 0) !== (f[j] >= 0)) { const k = f[i] / (f[i] - f[j]); out.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, f[i] >= 0 ? -1 : i]); }
    }
    return out;
  }
  const pathOf = (pp) => { let s = ""; for (let i = 0; i < pp.length; i++) s += (i ? "L" : "M") + f1(pp[i][0]) + "," + f1(pp[i][1]); return s; };
  const ringPath = (C, pts, z, fn) => { const c = clipEdge(pts, fn); return c.length >= 3 ? pathOf(c.map((p) => proj(C, p[0], p[1], z))) + "Z" : ""; };
  const segClip = (a, b, fn) => { const fa = fn(a), fb = fn(b); if (fa < 0 && fb < 0) return null; if (fa >= 0 && fb >= 0) return [a, b]; const k = fa / (fa - fb), m = [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; return fa >= 0 ? [a, m] : [m, b]; };
  const lineOf = (C, pts, zf, fn) => { let s = ""; for (let i = 0; i + 1 < pts.length; i++) { const sg = segClip(pts[i], pts[i + 1], fn); if (!sg) continue; const p = proj(C, sg[0][0], sg[0][1], zf(sg[0])), q = proj(C, sg[1][0], sg[1][1], zf(sg[1])); s += `M${f1(p[0])},${f1(p[1])}L${f1(q[0])},${f1(q[1])}`; } return s; };
  const circ = (u, v, r, n = 40) => Array.from({ length: n }, (_, i) => [u + Math.cos((i / n) * PI * 2) * r, v + Math.sin((i / n) * PI * 2) * r]);

  // ---------------- one frame ----------------
  const WALL = { nb: ["#7d6140", "#d4b98c"], th: ["#8c6a42", "#e6c995"] };
  function walls(C, land, isTh, acc) {
    const fn = nearFn(C, isTh ? HTH : H), shades = isTh ? WALL.th : WALL.nb;
    land.rings.forEach((R) => {
      const c = clipRingE(R.pts, fn);
      for (let i = 0; i < c.length; i++) {
        const a = c[i], b = c[(i + 1) % c.length], e = a[2];
        if (e < 0) continue;
        const n = R.n[e], mu = (a[0] + b[0]) / 2, mv = (a[1] + b[1]) / 2;
        if ((C.gu - mu) * n[0] + (C.gv - mv) * n[1] <= 0) continue;
        const border = isTh && R.border[e], z0 = border ? H : 0, z1 = isTh ? HTH : H;
        const lit = clamp(0.5 + 0.62 * (n[0] * LN[0] + n[1] * LN[1]));
        const bucket = Math.round(lit * 5);
        const A0 = proj(C, a[0], a[1], z0), B0 = proj(C, b[0], b[1], z0), B1 = proj(C, b[0], b[1], z1), A1 = proj(C, a[0], a[1], z1);
        acc.q[bucket] += `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}L${f1(B1[0])},${f1(B1[1])}L${f1(A1[0])},${f1(A1[1])}Z`;
        if (!border) {
          acc.foam += `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}`;
          const Am = proj(C, a[0], a[1], z1 * 0.45), Bm = proj(C, b[0], b[1], z1 * 0.45);
          acc.strata += `M${f1(Am[0])},${f1(Am[1])}L${f1(Bm[0])},${f1(Bm[1])}`;
        }
      }
    });
    let s = "";
    acc.q.forEach((d, k) => { if (d) s += `<path d="${d}" fill="${mix(shades[0], shades[1], k / 5)}" stroke="${mix(shades[0], shades[1], k / 5)}" stroke-width="0.8" stroke-linejoin="round"/>`; });
    if (acc.strata) s += `<path d="${acc.strata}" stroke="#5c4428" stroke-width="1.6" opacity=".22" fill="none"/>`;
    if (acc.foam) s += `<path d="${acc.foam}" stroke="#f2fdff" stroke-width="2.6" opacity=".8" fill="none" stroke-linecap="round"/>`;
    return s;
  }
  const newAcc = () => ({ q: ["", "", "", "", "", ""], foam: "", strata: "" });

  function frame(inst, t) {
    const Dd = data(), o = inst.o, C = camera(camAt(inst.keys, t)), z0f = nearFn(C, 0), zHf = nearFn(C, H), zTf = nearFn(C, HTH);
    const S = C.S, out = [];
    const gz = (p) => Dd.hAt(p[0], p[1]);
    // the sea: a huge plane, the graticule, the shallows along every coast
    const sea = [P(60, 50), P(140, 50), P(140, -25), P(60, -25)];
    out.push(`<path d="${ringPath(C, sea, 0, z0f)}" fill="url(#qmSea)"/>`);
    let gr = "";
    for (let lo = 88; lo <= 112; lo += 2) gr += lineOf(C, [P(lo, -2), P(lo, 32)], () => 0, z0f);
    for (let la = 0; la <= 30; la += 2) gr += lineOf(C, [P(84, la), P(114, la)], () => 0, z0f);
    out.push(`<path d="${gr}" stroke="#eaf8fc" stroke-width="1.4" opacity=".16" fill="none"/>`);
    let coast = "";
    [...Dd.neigh, Dd.th].forEach((l) => l.rings.forEach((R) => (coast += ringPath(C, R.pts, 0, z0f))));
    out.push(`<path d="${coast}" fill="none" stroke="#5fcbd0" stroke-width="${f1(Math.min(60, 12 * S))}" opacity=".26" stroke-linejoin="round"/><path d="${coast}" fill="none" stroke="#a6eadf" stroke-width="${f1(Math.min(26, 5 * S))}" opacity=".42" stroke-linejoin="round"/>`);
    // glints drifting on the water
    let gl = "";
    Dd.glints.forEach(([u, v, l, ph, sp]) => { const op = 0.5 + 0.5 * Math.sin(t * 2.2 * sp + ph); if (op < 0.25) return; const uu = u + ((t * 2.4 * sp + ph * 9) % 18) - 9; const sg = segClip([uu - l, v], [uu + l, v], z0f); if (!sg) return; const a = proj(C, sg[0][0], sg[0][1], 0), b = proj(C, sg[1][0], sg[1][1], 0); gl += `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}`; });
    out.push(`<path d="${gl}" stroke="#f2fcff" stroke-width="${f1(clamp(0.5 * S, 1.2, 3))}" stroke-linecap="round" opacity=".45"/>`);
    // the land slabs cast a soft shadow onto the water (south-east, away from the light)
    let lsh = "";
    [...Dd.neigh, Dd.th].forEach((l) => l.rings.forEach((R) => (lsh += ringPath(C, R.pts.map((p) => [p[0] + H * 0.55, p[1] + H * 0.7]), 0, z0f))));
    out.push(`<path d="${lsh}" fill="#0b3550" opacity=".2"/>`);
    // names on the water
    const groundText = (txt, lo, la, size, z, fill, extra = "") => {
      const [u, v] = P(lo, la), p0 = proj(C, u, v, z), px = proj(C, u + 1, v, z), py = proj(C, u, v + 1, z);
      if (p0[2] < C.near * 1.5) return "";
      return `<text transform="matrix(${f1(px[0] - p0[0])} ${f1(px[1] - p0[1])} ${f1(py[0] - p0[0])} ${f1(py[1] - p0[1])} ${f1(p0[0])} ${f1(p0[1])})" text-anchor="middle" font-family="Kanit" font-size="${size}" fill="${fill}" ${extra}>${txt}</text>`;
    };
    NAMES.filter((n) => n[4]).forEach(([txt, lo, la, sz]) => out.push(groundText(txt, lo, la, sz, 0, "#e8f7fb", `font-weight="600" font-style="italic" letter-spacing="3" opacity=".75"`)));
    // the neighbours: walls, then tops with their borders
    out.push(walls(C, { rings: Dd.neigh.flatMap((l) => l.rings) }, false, newAcc()));
    Dd.neigh.forEach((l) => { let d = ""; l.rings.forEach((R) => (d += ringPath(C, R.pts, H, zHf))); if (d) out.push(`<path d="${d}" fill="#ece1bf" stroke="#c4ae86" stroke-width="1.6" stroke-linejoin="round"/>`); });
    // vegetation tints, rivers and names on the neighbours' ground
    let tn = "";
    Dd.tints.forEach(([u, v, rr, g]) => { const z = Dd.hAt(u, v); if (!z) return; const d = ringPath(C, circ(u, v, rr, 20), z + 0.1, nearFn(C, z)); if (d) tn += `<path d="${d}" fill="url(#${g})"/>`; });
    out.push(tn);
    // Thailand one step up: its walls (a short step on the land borders, the full height on the coasts), the top, a lit rim
    out.push(walls(C, Dd.th, true, newAcc()));
    let thd = ""; Dd.th.rings.forEach((R) => (thd += ringPath(C, R.pts, HTH, zTf)));
    out.push(`<path d="${thd}" fill="#fbf3d8" stroke="#b58e5c" stroke-width="2" stroke-linejoin="round"/><path d="${thd}" fill="none" stroke="#ffffff" stroke-width="2.2" opacity=".75" transform="translate(0,1.6)" stroke-linejoin="round"/>`);
    // tints that fall on Thailand
    let tt = "";
    Dd.tints.forEach(([u, v, rr, g]) => { if (Dd.code(u, v) !== 2) return; const d = ringPath(C, circ(u, v, rr, 20), HTH + 0.1, zTf); if (d) tt += `<path d="${d}" fill="url(#${g})"/>`; });
    out.push(tt);
    // rivers on whatever ground they cross
    let rv = "";
    Dd.rivers.forEach((pts) => (rv += lineOf(C, pts, (p) => Dd.hAt(p[0], p[1]) + 0.2, zTf)));
    out.push(`<path d="${rv}" stroke="#4fa9cf" stroke-width="${f1(clamp(1.3 * S, 2.2, 7))}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/><path d="${rv}" stroke="#c8f0fa" stroke-width="${f1(clamp(0.45 * S, 0.8, 2.4))}" fill="none" stroke-linecap="round" opacity=".8"/>`);
    NAMES.filter((n) => !n[4]).forEach(([txt, lo, la, sz]) => { const [u, v] = P(lo, la); out.push(groundText(txt, lo, la, sz, Dd.hAt(u, v) + 0.2, "#9c8762", `font-weight="700" letter-spacing="4" opacity=".8"`)); });

    // ---- the quake on the ground ----
    const [eu, ev] = Dd.epi, [bu, bv] = Dd.bkk, tw = o.wave ?? 4.45;
    // Bangkok's built-up patch
    { const d = ringPath(C, circ(bu, bv, 30, 28), HTH + 0.15, zTf); if (d) out.push(`<path d="${d}" fill="url(#qmCity)"/>`); }
    // epicentre glow and the crack
    const pop = t < 0.1 ? 0 : backOut((t - 0.1) / 0.45, 2.4), pulse = 1 + 0.12 * Math.sin(t * 9);
    if (pop > 0) {
      const d = ringPath(C, circ(eu, ev, 62 * pop * pulse, 36), H + 0.3, zHf); if (d) out.push(`<path d="${d}" fill="url(#qmEpi)"/>`);
      const rev = clamp((t - 0.15) / 0.7), half = Math.ceil(((Dd.crack.length - 1) / 2) * rev), mid = (Dd.crack.length - 1) / 2;
      const cp = Dd.crack.slice(Math.max(0, Math.floor(mid - half)), Math.min(Dd.crack.length, Math.ceil(mid + half) + 1));
      if (cp.length > 1) { const cl = lineOf(C, cp, () => H + 0.4, zHf); out.push(`<path d="${cl}" stroke="#ff7a3a" stroke-width="${f1(clamp(3.6 * S, 8, 20))}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".28"/><path d="${cl}" stroke="#3a0e06" stroke-width="${f1(clamp(1.8 * S, 4, 11))}" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="${cl}" stroke="#ffb04a" stroke-width="${f1(clamp(0.6 * S, 1.4, 4))}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".95"/>`); }
    }
    // the rings: a translucent band behind a bright front, draped over sea, land and Thailand
    const rings = [];
    for (let k = 0; k < 16; k++) { const ts = 0.3 + k * 0.6, R = V * (t - ts); if (R > 4 && R < 1150) rings.push(R); }
    rings.forEach((R) => {
      const a = clamp(1 - R / 1150) * clamp(R / 40), pts = circ(eu, ev, R, 110), inner = circ(eu, ev, Math.max(1, R - clamp(70 / S, 8, 34)), 110);
      const zf = (p) => Dd.hAt(p[0], p[1]) + 0.6;
      const proj2 = (ps) => { const c = clipEdge(ps, z0f); return c.length > 2 ? pathOf(c.map((p) => proj(C, p[0], p[1], zf(p)))) + "Z" : ""; };
      const fr = proj2(pts), inr = proj2(inner);
      if (fr) out.push(`<path d="${fr}${inr}" fill="#ff3a24" fill-rule="evenodd" opacity="${f1(0.2 * a)}"/><path d="${fr}" fill="none" stroke="#ff4a2e" stroke-width="${f1(clamp(1.6 * S, 3.5, 8))}" opacity="${f1(0.92 * a)}" stroke-linejoin="round"/><path d="${fr}" fill="none" stroke="#fff3d0" stroke-width="${f1(clamp(0.5 * S, 1.2, 2.6))}" opacity="${f1(0.75 * a)}"/>`);
    });
    // Bangkok answers each ring with a gold pulse
    rings.forEach((R) => { const dB = Math.hypot(bu - eu, bv - ev), k = (R - dB) / 120; if (k > 0 && k < 1) { const d = ringPath(C, circ(bu, bv, 10 + 60 * k, 32), HTH + 0.3, zTf); if (d) out.push(`<path d="${d}" fill="url(#qmPulse)" opacity="${f1(1 - k)}"/>`); } });
    // cloud shadows on the ground
    const drift = 3.2 * t;
    Dd.clouds.forEach((c) => { const u = c.u + drift + c.z * 0.35, v = c.v + c.z * 0.45, z = Dd.hAt(u, v), d = ringPath(C, circ(u, v, c.r * 1.25, 18), z + 0.2, nearFn(C, z)); if (d) out.push(`<path d="${d}" fill="url(#qmShade)"/>`); });

    // mountains sit in their own soft shadow
    let msh = "";
    Dd.peaks.forEach((pk) => { const d = ringPath(C, circ(pk.u + pk.h * 0.18, pk.v + pk.h * 0.22, pk.r * 1.12, 12), pk.z + 0.1, nearFn(C, pk.z)); if (d) msh += d; });
    out.push(`<path d="${msh}" fill="#3a3a1e" opacity=".14"/>`);
    // ---- things that stand up, sorted far to near ----
    const objs = [], cam3 = [C.gu, C.gv, C.gz];
    const face = (pts3, base, edge) => { // pts3: 3D points of a planar face; shaded by its normal; skip if it faces away
      const [a, b, c] = pts3, ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
      const cx = pts3.reduce((s, p) => s + p[0], 0) / pts3.length, cy = pts3.reduce((s, p) => s + p[1], 0) / pts3.length, cz = pts3.reduce((s, p) => s + p[2], 0) / pts3.length;
      if (nx * (cx - base[0]) + ny * (cy - base[1]) + nz * (cz - base[2]) < 0) { nx = -nx; ny = -ny; nz = -nz; }
      if (nx * (cam3[0] - cx) + ny * (cam3[1] - cy) + nz * (cam3[2] - cz) <= 0) return null;
      return { lit: clamp(0.3 + 0.75 * Math.max(0, nx * LN[0] + ny * LN[1] + nz * LN[2])), pp: pts3.map((p) => proj(C, p[0], p[1], p[2])), edge };
    };
    // mountains: low-poly cones; the wave front makes them jolt as it passes
    Dd.peaks.forEach((pk) => {
      const pc = proj(C, pk.u, pk.v, pk.z);
      if (pc[2] < C.near * 1.2 || pc[0] < -300 || pc[0] > 1380 || pc[1] < -400 || pc[1] > 2300) return;
      const dE = Math.hypot(pk.u - eu, pk.v - ev);
      let j = 0; rings.forEach((R) => (j += Math.exp(-(((dE - R) / 22) ** 2)) * clamp(1 - R / 1150)));
      const ap = [pk.u + pk.au + j * 6 * Math.sin(t * 38 + pk.ph), pk.v + pk.av + j * 2.5 * Math.cos(t * 31 + pk.ph), pk.z + pk.h * (1 + 0.22 * j)];
      const lift = j * 2.4, ctr = [pk.u, pk.v, pk.z];
      const lit0 = mix("#55643a", "#6b5f3e", pk.tint), lit1 = mix("#dcd49a", "#e8d6a2", pk.tint);
      let s = "";
      const nb = pk.base.length;
      for (let i = 0; i < nb; i++) {
        const b0 = pk.base[i], b1 = pk.base[(i + 1) % nb], f = face([[pk.u + b0[0], pk.v + b0[1], pk.z + lift], [pk.u + b1[0], pk.v + b1[1], pk.z + lift], ap], ctr);
        if (!f) continue;
        const col = mix(lit0, lit1, Math.pow(f.lit, 1.25));
        s += `<path d="${pathOf(f.pp)}Z" fill="${col}" stroke="${mix(col, "#2a3018", 0.45)}" stroke-width="1" stroke-linejoin="round"/>`;
      }
      // a sunlit ridge line from the apex down the north-west side
      const ap2 = proj(C, ...ap), bl = proj(C, pk.u + pk.base[4][0] * 0.9, pk.v + pk.base[4][1] * 0.9, pk.z + lift);
      s += `<path d="M${f1(ap2[0])},${f1(ap2[1])}L${f1(bl[0])},${f1(bl[1])}" stroke="#fffbe6" stroke-width="1.1" opacity=".45"/>`;
      objs.push([pc[2], s]);
    });
    // Bangkok's towers: glass boxes; once the wave arrives they sway (a shear that grows with height)
    const swayA = smooth((t - tw) / 0.9);
    Dd.towers.forEach((tw0) => {
      const pc = proj(C, tw0.u + tw0.w / 2, tw0.v + tw0.d / 2, HTH);
      if (pc[2] < C.near * 1.2) return;
      const sx = tw0.low ? 0 : swayA * Math.sin(2 * PI * tw0.f * (t - tw) + tw0.ph) * tw0.h * 0.075, sv = tw0.low ? 0 : swayA * Math.cos(2 * PI * tw0.f * 0.7 * (t - tw) + tw0.ph) * tw0.h * 0.03;
      const z0 = HTH, z1 = HTH + tw0.h, u0 = tw0.u, u1 = tw0.u + tw0.w, v0 = tw0.v, v1 = tw0.v + tw0.d;
      const top = (u, v) => [u + sx, v + sv, z1], ctr = [u0 + tw0.w / 2, v0 + tw0.d / 2, z0 + tw0.h / 2];
      const sides = [[[u0, v1, z0], [u1, v1, z0], top(u1, v1), top(u0, v1)], [[u1, v0, z0], [u1, v1, z0], top(u1, v1), top(u1, v0)], [[u0, v0, z0], [u1, v0, z0], top(u1, v0), top(u0, v0)], [[u0, v0, z0], [u0, v1, z0], top(u0, v1), top(u0, v0)]];
      let s = "";
      const g0 = tw0.low ? "#a99c84" : tw0.pal[0], g1 = tw0.low ? "#efe6d2" : tw0.pal[1];
      sides.forEach((q) => {
        const f = face(q, ctr);
        if (!f) return;
        const col = mix(g0, g1, f.lit);
        s += `<path d="${pathOf(f.pp)}Z" fill="${col}" stroke="#23384a" stroke-width="${tw0.low ? 0.6 : 0.9}" stroke-linejoin="round"/>`;
        if (!tw0.low) { // floor bands
          let wl = "";
          for (let z = 1.6; z < tw0.h - 0.6; z += 1.5) { const k = z / tw0.h, A = q[0], B = q[1], pa = proj(C, A[0] + sx * k, A[1] + sv * k, z0 + z), pb = proj(C, B[0] + sx * k, B[1] + sv * k, z0 + z); wl += `M${f1(pa[0])},${f1(pa[1])}L${f1(pb[0])},${f1(pb[1])}`; }
          s += `<path d="${wl}" stroke="${mix(col, "#ffffff", 0.55)}" stroke-width="${f1(clamp(0.22 * S, 0.5, 1.8))}" opacity=".7"/>`;
        }
      });
      const tf = face([top(u0, v0), top(u1, v0), top(u1, v1), top(u0, v1)], ctr);
      if (tf) s += `<path d="${pathOf(tf.pp)}Z" fill="${tw0.low ? "#f4ecdc" : "#eef7fb"}" stroke="#23384a" stroke-width="0.8"/>`;
      if (tw0.spire) { const a = proj(C, u0 + tw0.w / 2 + sx, v0 + tw0.d / 2 + sv, z1), b = proj(C, u0 + tw0.w / 2 + sx * 1.15, v0 + tw0.d / 2 + sv * 1.15, z1 + tw0.h * 0.16); s += `<path d="M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}" stroke="#23384a" stroke-width="${f1(clamp(0.5 * S, 1.5, 3.5))}" stroke-linecap="round"/><circle cx="${f1(b[0])}" cy="${f1(b[1])}" r="${f1(clamp(0.5 * S, 2, 4.5))}" fill="#ff5a3a"/>`; }
      objs.push([pc[2], s]);
    });
    objs.sort((a, b) => b[0] - a[0]);
    out.push(objs.map((o) => o[1]).join(""));

    // ---- above the ground: the burst, the Bangkok pin, clouds ----
    if (pop > 0) {
      const p = proj(C, eu, ev, H + 26), sc = clamp(S / 1.4, 0.8, 2.2), sq = 1 + 0.18 * Math.sin(t * 14) * clamp(1 - (t - 0.1) / 3), rot = 8 * Math.sin(t * 20);
      const tether = proj(C, eu, ev, H + 0.5);
      out.push(`<path d="M${f1(tether[0])},${f1(tether[1])}L${f1(p[0])},${f1(p[1])}" stroke="#ff8a3a" stroke-width="3" opacity=".5"/>
        <g transform="translate(${f1(p[0])},${f1(p[1])}) scale(${f1(sc * pop)})"><circle r="${f1(110 * pulse)}" fill="url(#qmBurst)"/>
        <g transform="rotate(${f1(rot)}) scale(${f1(sq)},${f1(2 - sq)})"><path d="${STAR}" transform="translate(0,7)" fill="#9a3a10" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/><path d="${STAR}" fill="url(#qmStar)" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/><path d="M-7,-22l7,-14l7,14" stroke="#fffbe0" stroke-width="3.5" fill="none" opacity=".9" stroke-linecap="round" stroke-linejoin="round"/></g></g>`);
    }
    const bk = o.bkkAt ?? 4.2;
    if (t > bk) {
      const k = (t - bk) / 0.65, drop = bounceOut(k), zp = HTH + 66 + (1 - drop) * 150 + (t > bk + 0.7 ? 2.2 * Math.sin((t - bk) * 4) : 0);
      const head = proj(C, bu, bv, zp), foot = proj(C, bu, bv, HTH + 0.3), r = clamp(22 + 7 * Math.log2(S), 20, 44);
      const shd = ringPath(C, circ(bu, bv, 6 + 4 * drop, 18), HTH + 0.2, zTf);
      out.push(`${shd ? `<path d="${shd}" fill="url(#qmShade)" opacity="${f1(clamp(k * 2))}"/>` : ""}<path d="M${f1(foot[0])},${f1(foot[1])}L${f1(head[0])},${f1(head[1])}" stroke="#140e0a" stroke-width="2.4" opacity="${f1(0.55 * clamp(k * 2))}" stroke-dasharray="5 5"/>
        <g transform="translate(${f1(head[0])},${f1(head[1])}) scale(${f1(r / 36)})" opacity="${f1(clamp(k * 3))}"><path d="M0,0C-30,-34 -36,-56 -36,-70A36,36 0 0 1 36,-70C36,-56 30,-34 0,0Z" fill="url(#qmPin)" stroke="#140e0a" stroke-width="4.5" stroke-linejoin="round"/>
        <path d="M-22,-84A26,26 0 0 1 2,-100" stroke="#ffc8b8" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/><circle cy="-70" r="13" fill="#fff" stroke="#140e0a" stroke-width="3"/></g>`);
      inst.pinHead = [head[0], head[1] - r * 2];
    } else inst.pinHead = null;
    // clouds: soft billboards up in the air; the ones we fly into fade out
    const cl = [];
    Dd.clouds.forEach((c) => {
      const p = proj(C, c.u + drift, c.v, H + c.z);
      if (p[2] < C.near * 1.6) return;
      const pr = (c.r * F) / p[2], fade = clamp((560 - pr) / 220) * 0.92;
      if (fade <= 0.02 || p[0] < -pr * 2 || p[0] > 1080 + pr * 2 || p[1] < -pr || p[1] > 2100 + pr) return;
      cl.push([p[2], `<g opacity="${f1(fade)}"><ellipse cx="${f1(p[0])}" cy="${f1(p[1] + pr * 0.22)}" rx="${f1(pr * 1.15)}" ry="${f1(pr * 0.34)}" fill="url(#qmCloudB)"/>${c.blobs.map(([ox, oy, br]) => `<ellipse cx="${f1(p[0] + ox * pr)}" cy="${f1(p[1] + oy * pr * 0.7)}" rx="${f1(br * pr)}" ry="${f1(br * pr * 0.72)}" fill="url(#qmCloud)"/>`).join("")}</g>`]);
    });
    cl.sort((a, b) => b[0] - a[0]);
    out.push(cl.map((c) => c[1]).join(""));
    // haze toward the far distance (the top of the frame)
    const hz = 300 + 520 * clamp((C.tilt - 25) / 35);
    out.push(`<rect x="-60" y="-60" width="1200" height="${f1(hz + 60)}" fill="url(#qmHaze)"/>`);
    inst.g.innerHTML = out.join("");
    // where the billboards go
    const pe = proj(C, eu, ev, H + 26), pb = proj(C, bu, bv, HTH + 60);
    inst.anchor = { epi: [pe[0], pe[1]], bkk: [pb[0], pb[1]], bkkGround: proj(C, bu, bv, HTH).slice(0, 2), S };
    return inst;
  }

  // ---------------- the set ----------------
  function qkMap3d(L, o = {}) {
    const id = o.id || "mq";
    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#qmSky)"/>`);
    put(L.set, `<g id="${id}-m3"></g>`);
    const inst = { id, o: { ...o }, keys: o.cam || FLIGHT, g: document.getElementById(`${id}-m3`) };
    L.qm3d = inst;
    frame(inst, 0);
  }

  // ---------------- 2.5D pills and cards (screen space) ----------------
  const pill = (w, h, o = {}) => {
    const r = o.r ?? h / 2, face = o.face || "url(#qmFaceD)", slab = o.slab || "#05030a", st = o.stroke || "#140e0a";
    return `<ellipse cx="0" cy="${f1(h / 2 + 18)}" rx="${f1(w * 0.46)}" ry="14" fill="url(#qmSoft)"/>
      <rect x="${f1(-w / 2)}" y="${f1(-h / 2 + 9)}" width="${w}" height="${h}" rx="${r}" fill="${slab}" stroke="#140e0a" stroke-width="4"/>
      <rect x="${f1(-w / 2)}" y="${f1(-h / 2)}" width="${w}" height="${h}" rx="${r}" fill="${face}" stroke="${st}" stroke-width="${o.sw ?? 4.5}"/>
      <path d="M${f1(-w / 2 + r * 0.9)},${f1(-h / 2 + 7)}H${f1(w / 2 - r * 0.9)}" stroke="#fff" stroke-width="3.5" opacity="${o.hi ?? 0.28}" stroke-linecap="round"/>`;
  };
  // pop in with squash & stretch: stretch up, squash, settle with an elastic overshoot
  const popIn = (tl, sel, at) => {
    tl.fromTo(sel, { scaleX: 0.1, scaleY: 0.1, opacity: 0, svgOrigin: "0 0" }, { scaleX: 0.82, scaleY: 1.24, opacity: 1, svgOrigin: "0 0", duration: 0.14, ease: "power2.out", immediateRender: false }, at);
    tl.to(sel, { scaleX: 1.16, scaleY: 0.86, svgOrigin: "0 0", duration: 0.1, ease: "sine.inOut" }, at + 0.14);
    tl.to(sel, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 0.42, ease: "elastic.out(1, 0.42)" }, at + 0.24);
  };

  function quakeMap3d(tl, L, sid, t0, o = {}) {
    const inst = L.qm3d, id = `${sid}-q3`, dur = o.dur ?? 9;
    Object.assign(inst.o, o);
    if (o.cam) inst.keys = o.cam;
    const [c0, c1] = o.count || [5.9, 8.6];
    // billboards in screen space: each = a positioned group (moved per frame) → a bob group → a pop group (scale / opacity)
    put(L.light, `<g id="${id}-chip" transform="translate(540,200)"><g id="${id}-chipB"><g id="${id}-chipP" opacity="0">${pill(840, 104, { stroke: "#ffd23a", sw: 5 })}
        <text y="17" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="46" fill="#fff6e8">28 มี.ค. 2568 · 13:20 น.</text>
        <circle cx="-372" cy="0" r="12" fill="#ff4a2e"/><circle id="${id}-rec" cx="-372" cy="0" r="12" fill="none" stroke="#ff4a2e" stroke-width="4"/></g></g></g>
      <g id="${id}-el" transform="translate(-999,-999)"><g id="${id}-elB"><g id="${id}-elP" opacity="0">${pill(372, 78, { stroke: "#140e0a" })}
        <text y="13" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="37" fill="#ffd23a">เมียนมา · ขนาด 8.2</text></g></g></g>
      <g id="${id}-bl" transform="translate(-999,-999)"><g id="${id}-blB"><g id="${id}-blP" opacity="0">${pill(236, 82, { face: "url(#qmFaceC)", slab: "#a8936a", hi: 0.7 })}
        <text y="14" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="42" fill="#140e0a">กรุงเทพฯ</text></g></g></g>
      <path id="${id}-ld" d="M0,0" stroke="#ffd23a" stroke-width="4" stroke-dasharray="10 8" fill="none" stroke-linecap="round" opacity="0"/>
      <g id="${id}-ct" transform="translate(-999,-999)"><g id="${id}-ctB"><g id="${id}-ctP" opacity="0">${pill(560, 176, { r: 34, stroke: "#ffd23a", sw: 5 })}
        <g transform="translate(-206,40)"><g id="${id}-cti"><rect x="-26" y="-118" width="52" height="118" fill="#7fb0d0" stroke="#140e0a" stroke-width="4"/><path d="M26,-118l12,-8v120l-12,6z" fill="#4c7a9a" stroke="#140e0a" stroke-width="3" stroke-linejoin="round"/><path d="M-26,-118l12,-8h52l-12,8z" fill="#d8eef8" stroke="#140e0a" stroke-width="3" stroke-linejoin="round"/>
          ${[0, 1, 2, 3, 4].map((k) => `<path d="M-18,${-100 + k * 21}H18" stroke="#e8f6fc" stroke-width="5" stroke-linecap="round"/>`).join("")}</g></g>
        <text x="40" y="-24" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="34" fill="#f6efe0">ตึกสูงโยกนานกว่า</text>
        <text id="${id}-cnt" x="40" y="50" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="66" fill="#ffd23a">0 วินาที</text></g></g></g>`);
    const $ = (s) => document.getElementById(`${id}-${s}`);
    const el = $("el"), bl = $("bl"), ct = $("ct"), cnt = $("cnt"), ld = $("ld");
    const place = (t) => {
      frame(inst, t);
      const A = inst.anchor;
      el.setAttribute("transform", `translate(${f1(A.epi[0] + 120)},${f1(A.epi[1] + 104)})`);
      el.setAttribute("opacity", f1(clamp(Math.min((A.epi[0] + 40) / 160, (A.epi[1] - 230) / 120))));
      if (inst.pinHead) bl.setAttribute("transform", `translate(${f1(clamp(inst.pinHead[0] + 150, 150, 930))},${f1(inst.pinHead[1] + 26)})`);
      ct.setAttribute("transform", "translate(540,452)");
      if (inst.pinHead) ld.setAttribute("d", `M540,${f1(452 + 100)}L${f1(inst.pinHead[0])},${f1(Math.max(560, inst.pinHead[1] - 50))}`);
      const k = clamp((t - c0 - 0.2) / Math.max(0.3, c1 - c0 - 0.3)), v = 20 * k * k;
      cnt.textContent = `${Math.round(v)}${v >= 19.5 ? "+" : ""} วินาที`;
    };
    const px = { t: 0 };
    tl.fromTo(px, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => place(px.t) }, t0);
    place(0);
    // entries, squash and stretch, staggered
    popIn(tl, `#${id}-chipP`, t0 + (o.chipAt ?? 0.3));
    tl.fromTo(`#${id}-rec`, { attr: { r: 12 }, opacity: 0.9 }, { attr: { r: 26 }, opacity: 0, duration: 0.9, repeat: Math.ceil(dur / 0.9), ease: "power1.out", immediateRender: false }, t0 + (o.chipAt ?? 0.3) + 0.3);
    popIn(tl, `#${id}-elP`, t0 + (o.labelAt ?? 3));
    tl.to(`#${id}-elP`, { opacity: 0, duration: 0.3 }, t0 + c0 - 0.6);
    popIn(tl, `#${id}-blP`, t0 + (o.bkkAt ?? 4.2) + 0.42);
    popIn(tl, `#${id}-ctP`, t0 + c0);
    tl.fromTo(`#${id}-ld`, { opacity: 0, attr: { "stroke-dashoffset": 0 } }, { opacity: 0.9, duration: 0.3, immediateRender: false }, t0 + c0 + 0.25);
    tl.fromTo(`#${id}-ld`, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -36 }, duration: 0.6, repeat: Math.ceil(dur / 0.6), ease: "none", immediateRender: false }, t0 + c0 + 0.25);
    // secondary motion until the end: gentle bobbing, the little tower in the card sways
    [["elB", 0], ["blB", 0.4], ["ctB", 0.8]].forEach(([s, ph]) => tl.fromTo(`#${id}-${s}`, { y: -3 }, { y: 3, duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + ph));
    tl.fromTo(`#${id}-cti`, { rotation: -6, svgOrigin: "0 0" }, { rotation: 6, svgOrigin: "0 0", duration: 0.55, repeat: Math.ceil(dur / 0.55), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + c0 + 0.3);
    if (o.out !== undefined) tl.to(`#${id}-chipP`, { opacity: 0, duration: 0.2 }, t0 + o.out);
  }

  Sets.qkMap3d = qkMap3d;
  window.QkUI = window.QkUI || {};
  QkUI.quakeMap3d = quakeMap3d;
  window.QkMap3D = { P, LL, FLIGHT, camAt, camera, proj, data, frame };
})();
