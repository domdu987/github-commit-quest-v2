// "ทะเลลด" — the tsunami on a 3D relief map of the Andaman Sea, and an ocean cross-section that explains the drawback.
// Load after maps.js / mapsdata.js and quakemap.js (it borrows nothing from them at load time, only window.MAPDATA).
// Both scenes are redrawn every frame from one proxy tween, so seeking to any time gives the right picture.
// Frame both shots with a fixed identity camera: cam: { keys: [{ t: 0, ...fr(540, 960, 1, 540, 960, { drift: { s: 0 } }) }] }
//
//   Sets.tideMap3d(L, { id })      the map in L.set (#<id>-m3): bathymetry in terraced bands (turquoise shelf → navy basin → the dark
//                                  trench), land as slabs with lit walls (Thailand one step higher with a rim; small islands are low
//                                  slabs so they don't read as pillars), Sumatra, Simeulue, Nias, the
//                                  Andaman and Nicobar islands, Surin / Similan / Phi Phi, karst towers in Phang Nga Bay, mountains,
//                                  clouds and their shadows, haze; draws the first frame of the flight
//   TideMap.play(tl, L, id, t0, o) the quake and the flight: o.dur (shot length, default 9), o.quakeAt (the star bursts, 0.4),
//                                  o.ringsAt (the wave fronts start, 0.8), o.coastAt (the leading front touches the coast at the pin,
//                                  6.2), o.pinAt (the pin drops, 5.6), o.chipAt (top chip, 0.3), o.chip (its text, "คลื่นกำลังมา"),
//                                  o.epiLabel ("แผ่นดินไหวใต้ทะเล"), o.pinLabel ("บ้านแหลมหอย (สมมติ)"), o.cam ([{ t, lon, lat, tilt,
//                                  yaw, S, cy }] to override the flight), o.out (chip leaves).
//                                  Wave fronts are isochrones of a travel-time field (speed ∝ √depth, computed once), so they race
//                                  across the deep basin, slow down and bend on the shelf, and wrap around islands; three crests
//                                  follow each other; coast segments flare as the leading front reaches them.
//                                  ids: #<sid>-tm-chip (chipP, chipB, clk = minute hand), #<sid>-tm-el (elP), #<sid>-tm-pl (plP)
//   Sets.tideSection(L, { id })    an ocean cross-section as a diorama block: the cut face (rock layers following the seabed, the
//                                  water body with light rays) under a thin top strip (sea surface / exposed mud / beach / land seen
//                                  from above), deep plain → continental slope → shelf → beach → a village with palms and huts → a
//                                  hill with the blue evacuation-route sign; a longtail boat moored near the shore; the 2.5D speed
//                                  coins live in L.light (#<id>-coins). Sky, sun, clouds and karst silhouettes go in L.sky / L.far.
//   TideMap.section(tl, id, t0, dur, o) the mechanism, all within dur (k = 0..1; o.k0 / o.k1 play only part of it, o.ease): the seafloor jolts at the fault (k .10, a star, a
//                                  shake, rings on the strip), the wave pair leaves (trough in front, crest behind) and races over
//                                  the deep plain (jet coin, k .16 → crest at x 2150), slows on the shelf (car coin, → k .90), the
//                                  trough reaches the shore and the sea draws back (exposed mud, flopping fish, the boat tilts on
//                                  the mud, a tiny person walks out, the drawback callout, k .81–.95), then the crest comes in as a
//                                  turbulent bore (NOAA: a fast-rising flood / wall of water, not a curling breaker): a steep
//                                  churning white-and-teal wall with a ragged foam front, spray and debris, the sea behind it raised
//                                  like a fast tide (runner coin tethered to the person, who turns and runs, k .90–1).
//                                  The block's own camera glides from the whole section (vertical ×2.5) to the shore (×1).
//                                  o.labels = { jet, car, run, drawback } overrides the texts; "|" breaks a line.
//                                  Defaults (verified, from the coordinator): jet "กลางทะเล: เร็วได้ถึง 950 กม./ชม.|พอๆ กับ
//                                  เครื่องบินเจ็ต" (TMD) · car "ใกล้ฝั่ง: ราว 40 กม./ชม." (UNESCO-IOC) · run "ยังเร็วกว่าคนวิ่ง"
//                                  (NOAA) · drawback "ท้องคลื่นถึงฝั่งก่อน…|น้ำทะเลลดลงกะทันหัน" (TMD)
//   TideMap.P(lon, lat) / TideMap.LL(u, v)   map units ↔ degrees · TideMap.HOME the pin (lon, lat)
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
  const lerp = (a, b, k) => a + (b - a) * k;
  const hx = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, k) => { const A = hx(a), B = hx(b); k = clamp(k); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
  const D = () => window.MAPDATA.th;
  const P = (lon, lat) => { const d = D(); return [d.tx + d.k * lon * RAD, d.ty - d.k * Math.log(Math.tan(PI / 4 + (lat * RAD) / 2))]; };
  const LL = (u, v) => { const d = D(); return [(u - d.tx) / d.k / RAD, (2 * Math.atan(Math.exp((d.ty - v) / d.k)) - PI / 2) / RAD]; };

  const H = 12, HTH = 17;                      // land slab height and Thailand's (map units; 1° ≈ 79 units)
  const WIN = [85.5, 106, -5, 21];             // lon0, lon1, lat0, lat1
  const LN = (() => { const v = [-0.55, -0.62, 0.62], l = Math.hypot(...v); return v.map((x) => x / l); })();
  const EPI = [95.85, 3.3], HOME = [98.3, 8.66];
  const STAR = "M0,-42l12,24l28,-7l-16,23l22,18l-29,2l-2,29l-15,-24l-15,24l-2,-29l-29,-2l22,-18l-16,-23l28,7z";
  const F = 2500;

  Sets.DEFS += `
    <linearGradient id="tmSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe0ea"/><stop offset="1" stop-color="#e6f3f1"/></linearGradient>
    <linearGradient id="tmHaze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3f1f3" stop-opacity=".97"/><stop offset=".45" stop-color="#e3f1f3" stop-opacity=".6"/><stop offset="1" stop-color="#e3f1f3" stop-opacity="0"/></linearGradient>
    <linearGradient id="tmStar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2a0"/><stop offset=".55" stop-color="#ffd23a"/><stop offset="1" stop-color="#f29a1a"/></linearGradient>
    <radialGradient id="tmEpi"><stop offset="0" stop-color="#ffe08a" stop-opacity=".95"/><stop offset=".25" stop-color="#ff8a3a" stop-opacity=".7"/><stop offset=".65" stop-color="#e8382a" stop-opacity=".3"/><stop offset="1" stop-color="#e8382a" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmBurst"><stop offset="0" stop-color="#fff6c8"/><stop offset=".3" stop-color="#ffb04a" stop-opacity=".9"/><stop offset=".65" stop-color="#ff5a2a" stop-opacity=".35"/><stop offset="1" stop-color="#e8382a" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmCloud"><stop offset="0" stop-color="#ffffff" stop-opacity=".96"/><stop offset=".62" stop-color="#fbfdff" stop-opacity=".85"/><stop offset="1" stop-color="#eef6fa" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmCloudB"><stop offset="0" stop-color="#8fa8b8" stop-opacity=".5"/><stop offset="1" stop-color="#8fa8b8" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmShade"><stop offset="0" stop-color="#05203a" stop-opacity=".26"/><stop offset=".6" stop-color="#05203a" stop-opacity=".12"/><stop offset="1" stop-color="#05203a" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmGreen"><stop offset="0" stop-color="#8fbf6a" stop-opacity=".62"/><stop offset=".6" stop-color="#a8c97c" stop-opacity=".28"/><stop offset="1" stop-color="#a8c97c" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmHit"><stop offset="0" stop-color="#fff3d0" stop-opacity=".9"/><stop offset=".4" stop-color="#ff7a4a" stop-opacity=".55"/><stop offset="1" stop-color="#ff4a2e" stop-opacity="0"/></radialGradient>
    <linearGradient id="tmPin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a64"/><stop offset=".55" stop-color="#e2392c"/><stop offset="1" stop-color="#a81c16"/></linearGradient>
    <linearGradient id="tmFaceD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20384a"/><stop offset="1" stop-color="#0a1620"/></linearGradient>
    <linearGradient id="tmFaceC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf6"/><stop offset="1" stop-color="#eadcbc"/></linearGradient>
    <radialGradient id="tmSoft"><stop offset="0" stop-color="#000" stop-opacity=".38"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <radialGradient id="tmCoinB" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#e8f7ff"/><stop offset=".55" stop-color="#8fd0f0"/><stop offset="1" stop-color="#3f8fc0"/></radialGradient>
    <radialGradient id="tmCoinO" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff2c8"/><stop offset=".55" stop-color="#ffc64a"/><stop offset="1" stop-color="#e88a1a"/></radialGradient>
    <radialGradient id="tmCoinR" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffe0d6"/><stop offset=".55" stop-color="#ff8a6a"/><stop offset="1" stop-color="#d8402a"/></radialGradient>
    <linearGradient id="tmSecSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fcbe6"/><stop offset=".55" stop-color="#cbe9f0"/><stop offset="1" stop-color="#f3efe0"/></linearGradient>
    <radialGradient id="tmSun"><stop offset="0" stop-color="#fffbe6"/><stop offset=".25" stop-color="#fff2b8" stop-opacity=".9"/><stop offset=".6" stop-color="#ffe9a0" stop-opacity=".25"/><stop offset="1" stop-color="#ffe9a0" stop-opacity="0"/></radialGradient>
    <linearGradient id="tmFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9efe8" stop-opacity="0"/><stop offset=".25" stop-color="#dfe4dc"/><stop offset="1" stop-color="#c9cfc6"/></linearGradient>
    <linearGradient id="tmRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8fbff" stop-opacity=".22"/><stop offset="1" stop-color="#e8fbff" stop-opacity="0"/></linearGradient>`;

  // ---------------- geometry helpers ----------------
  const parse = (s) => s.split("M").filter(Boolean).map((r) => r.replace(/Z/g, "").split("L").map((p) => p.split(",").map(Number)));
  function dpOpen(pts, eps) {
    const n = pts.length; if (n < 3) return pts.slice();
    const keep = new Uint8Array(n); keep[0] = keep[n - 1] = 1;
    const st = [[0, n - 1]];
    while (st.length) {
      const [a, b] = st.pop(); const [ax, ay] = pts[a], [bx, by] = pts[b], dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy || 1e-9;
      let md = -1, mi = -1;
      for (let i = a + 1; i < b; i++) { const [px, py] = pts[i]; const t = clamp(((px - ax) * dx + (py - ay) * dy) / L2); const ex = ax + t * dx - px, ey = ay + t * dy - py, d = ex * ex + ey * ey; if (d > md) { md = d; mi = i; } }
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
  function clipEdge(pts, fn) {
    const out = [], n = pts.length;
    for (let i = 0; i < n; i++) {
      const a = pts[i], b = pts[(i + 1) % n], fa = fn(a), fb = fn(b);
      if (fa >= 0) out.push(a);
      if ((fa >= 0) !== (fb >= 0)) { const k = fa / (fa - fb); out.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]); }
    }
    return out;
  }
  const chaikin = (pts, it) => { for (let k = 0; k < it; k++) { const out = []; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; out.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25], [a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } pts = out; } return pts; };
  const area = (r) => { let A = 0; for (let i = 0; i < r.length; i++) { const a = r[i], b = r[(i + 1) % r.length]; A += a[0] * b[1] - b[0] * a[1]; } return A / 2; };
  const prepRing = (pts) => { const A = area(pts), s = A > 0 ? 1 : -1; const n = pts.map((a, i) => { const b = pts[(i + 1) % pts.length], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; return [(s * dy) / l, (-s * dx) / l]; }); return { pts, n }; };
  const lp = (pts) => pts.map(([lo, la]) => P(lo, la));
  const blob = (lo, la, r, n, seed) => { const g = mk(seed); return Array.from({ length: n }, (_, i) => { const a = (i / n) * PI * 2, rr = r * (0.75 + g() * 0.5); return [lo + Math.cos(a) * rr, la + Math.sin(a) * rr * 0.9]; }); };

  // ---------------- land that mapsdata.js does not have (lon, lat) ----------------
  const SUMATRA = [[95.2, 5.58], [95.25, 5.3], [95.38, 5.05], [95.55, 4.8], [95.75, 4.45], [96.1, 4.15], [96.45, 3.85], [96.85, 3.55], [97.2, 3.25], [97.45, 2.85],
    [97.75, 2.35], [98.2, 2.05], [98.75, 1.7], [98.95, 1.3], [99.15, 0.85], [99.4, 0.3], [99.75, -0.3], [100.2, -0.8], [100.55, -1.3], [100.9, -1.9], [101.4, -2.6],
    [102.3, -3.8], [104.0, -5.3], [105.8, -5.9], [106.1, -3.2], [105.6, -2.1], [104.5, -1.1], [103.7, -0.9], [103.4, -0.3], [103.1, 0.4], [102.3, 1.0], [101.8, 1.5],
    [101.4, 1.75], [100.9, 2.15], [100.3, 2.6], [99.8, 3.0], [99.2, 3.4], [98.75, 3.8], [98.3, 4.1], [97.95, 4.5], [97.5, 4.95], [97.15, 5.18], [96.6, 5.25], [96.0, 5.4], [95.6, 5.6], [95.35, 5.62]];
  const ISLANDS = [
    [[95.72, 2.95], [96.05, 2.75], [96.45, 2.45], [96.38, 2.33], [96.0, 2.52], [95.75, 2.72]],                                          // Simeulue
    [[97.05, 1.55], [97.45, 1.25], [97.85, 0.85], [97.95, 0.6], [97.75, 0.55], [97.35, 0.95], [97.05, 1.3]],                              // Nias
    [[95.25, 5.88], [95.38, 5.85], [95.35, 5.76], [95.24, 5.79]],                                                                          // Weh
    [[92.95, 13.62], [93.08, 13.4], [93.05, 13.05], [93.02, 12.75], [92.98, 12.4], [92.88, 12.05], [92.78, 11.75], [92.75, 11.52], [92.62, 11.5],
      [92.55, 11.7], [92.62, 12.05], [92.7, 12.35], [92.75, 12.75], [92.82, 13.15], [92.86, 13.48]],                                        // Andaman
    [[92.43, 10.92], [92.6, 10.82], [92.58, 10.52], [92.45, 10.5], [92.38, 10.7]],                                                          // Little Andaman
    [[92.7, 9.25], [92.82, 9.22], [92.8, 9.1], [92.7, 9.12]],                                                                              // Car Nicobar
    [[93.08, 8.34], [93.22, 8.27], [93.2, 8.1], [93.05, 8.16]], [[93.45, 8.12], [93.6, 8.02], [93.54, 7.9], [93.4, 7.98]],                  // Nicobar middle group
    [[93.62, 7.46], [93.78, 7.4], [93.75, 7.29], [93.6, 7.32]],                                                                            // Little Nicobar
    [[93.68, 7.22], [93.92, 7.1], [93.95, 6.85], [93.85, 6.74], [93.72, 6.85], [93.65, 7.05]],                                             // Great Nicobar
    blob(97.86, 9.42, 0.07, 7, 3), blob(97.64, 8.68, 0.045, 6, 5), blob(97.65, 8.55, 0.04, 6, 7), blob(98.77, 7.74, 0.05, 6, 9),            // Surin, Similan, Phi Phi
  ];
  // the Sunda trench (the plate edge, west of the island arc) and the rupture that unzips north from the star
  const TRENCH = [[97.4, -0.6], [96.4, 1.0], [95.2, 2.4], [94.2, 4.0], [93.3, 5.8], [92.6, 7.6], [91.95, 9.4], [91.65, 11.2], [91.75, 13.0], [92.1, 14.8]];
  const RUPTURE = [[95.85, 3.3], [95.3, 4.4], [94.65, 5.6], [94.1, 6.8], [93.55, 8.2], [93.15, 9.6], [92.85, 11.0], [92.75, 12.4], [92.85, 13.5]];
  // mountains: [polyline (lon, lat), step (deg), spread (deg), height min, max]
  const RANGES = [
    [[[98.6, 16.3], [98.95, 14.6], [99.15, 13.1], [99.25, 11.9], [98.9, 10.6], [98.7, 9.7]], 0.3, 0.18, 11, 19],           // Tenasserim
    [[[98.75, 9.7], [98.62, 9.1], [98.55, 8.7], [98.6, 8.35]], 0.22, 0.12, 9, 15],                                          // Khao Sok / Phang Nga
    [[[98.95, 9.6], [99.7, 8.8], [99.95, 7.7], [100.35, 6.75]], 0.3, 0.14, 8, 13],                                         // Nakhon Si Thammarat range
    [[[101.25, 6.3], [101.6, 5.0], [101.9, 3.7], [102.2, 2.9]], 0.3, 0.2, 11, 18],                                         // Titiwangsa
    [[[95.6, 5.05], [96.3, 4.45], [97.1, 3.75], [97.9, 2.95], [98.7, 2.15], [99.4, 1.25], [100.0, 0.35], [100.6, -0.6], [101.3, -1.7]], 0.26, 0.14, 12, 22], // Barisan
  ];
  const NAMES = [["เมียนมา", 98.4, 13.6, 26, 0], ["มาเลเซีย", 101.9, 4.4, 22, 0], ["อินโดนีเซีย", 98.2, 2.9, 22, 0], ["ไทย", 99.25, 10.25, 26, 2],
    ["ทะเลอันดามัน", 95.9, 9.6, 28, 1], ["มหาสมุทรอินเดีย", 91.0, 5.4, 22, 1]];
  const PLACES = [["ระนอง", 98.82, 9.9], ["ภูเก็ต", 98.34, 7.97], ["กระบี่", 99.0, 8.2], ["ตรัง", 99.7, 7.6]];
  const KARST = [[98.47, 8.27], [98.52, 8.21], [98.56, 8.29], [98.49, 8.15], [98.6, 8.18], [98.44, 8.2], [98.58, 8.1], [98.53, 8.33], [98.64, 8.25], [98.41, 8.31], [98.68, 8.15]];

  // ---------------- data, built once ----------------
  let DATA = null;
  function data() {
    if (DATA) return DATA;
    const d = D(), [wx0, wy0] = P(WIN[0], WIN[3]), [wx1, wy1] = P(WIN[1], WIN[2]);
    const clipWin = (r) => [(p) => p[0] - wx0, (p) => wx1 - p[0], (p) => p[1] - wy0, (p) => wy1 - p[1]].reduce((pts, fn) => (pts.length ? clipEdge(pts, fn) : pts), r);
    const prep = (rings, eps, sm) => rings.map((r) => clipWin(chaikin(dpRing(r, eps), sm))).filter((r) => r.length >= 3 && Math.abs(area(r)) > 1.5).map(prepRing);
    const heights = (rings, big, lo, hi) => { const amax = Math.max(...rings.map((R) => Math.abs(area(R.pts)))); rings.forEach((R) => { const a = Math.abs(area(R.pts)); R.z = a === amax && big ? big : lerp(lo, hi, clamp(Math.sqrt(a / 2500))); }); };
    const nb = Object.entries(d.nb).filter(([k]) => k !== "china").map(([k, s]) => ({ k, rings: prep(parse(s), 1.0, 1) }));
    const extra = { k: "extra", rings: prep([chaikin(lp(SUMATRA), 2), ...ISLANDS.map((r) => chaikin(lp(r), 2))], 0.4, 0) };
    const th = { k: "th", rings: prep(parse(d.th), 0.6, 2) };
    const neigh = [extra, ...nb];
    neigh.forEach((l) => heights(l.rings, 0, 3.5, H)); heights(th.rings, HTH, 4, 13);
    const allNb = neigh.flatMap((l) => l.rings.map((r) => r.pts));
    const inRing = (r, x, y) => { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
    th.rings.forEach((R) => { R.border = R.pts.map((a, i) => { const b = R.pts[(i + 1) % R.pts.length], mx = (a[0] + b[0]) / 2 + R.n[i][0] * 2.2, my = (a[1] + b[1]) / 2 + R.n[i][1] * 2.2; return allNb.some((q) => inRing(q, mx, my)); }); });
    // the grid: 0 sea, 1 land, 2 Thailand
    const cs = 5, nx = Math.ceil((wx1 - wx0) / cs) + 1, ny = Math.ceil((wy1 - wy0) / cs) + 1, grid = new Uint8Array(nx * ny), zgrid = new Float32Array(nx * ny);
    const fill = (rings, code) => rings.forEach(({ pts, z }) => {
      for (let j = 0; j < ny; j++) {
        const y = wy0 + j * cs, xs = [];
        for (let i = 0; i < pts.length; i++) { const [x1, y1] = pts[i], [x2, y2] = pts[(i + 1) % pts.length]; if ((y1 > y) !== (y2 > y)) xs.push(x1 + ((y - y1) * (x2 - x1)) / (y2 - y1)); }
        xs.sort((a, b) => a - b);
        for (let k = 0; k + 1 < xs.length; k += 2) { const i0 = Math.max(0, Math.ceil((xs[k] - wx0) / cs)), i1 = Math.min(nx - 1, Math.floor((xs[k + 1] - wx0) / cs)); for (let i = i0; i <= i1; i++) { const kk = j * nx + i; grid[kk] = Math.max(grid[kk], code); zgrid[kk] = code === 2 ? z : Math.max(zgrid[kk], z); } }
      }
    });
    neigh.forEach((l) => fill(l.rings, 1)); fill(th.rings, 2);
    const code = (u, v) => { const i = Math.round((u - wx0) / cs), j = Math.round((v - wy0) / cs); return i < 0 || j < 0 || i >= nx || j >= ny ? 0 : grid[j * nx + i]; };
    const hAt = (u, v) => { const i = Math.round((u - wx0) / cs), j = Math.round((v - wy0) / cs); return i < 0 || j < 0 || i >= nx || j >= ny ? 0 : zgrid[j * nx + i]; };
    // distance to land (chamfer 3-4), in map units
    const N = nx * ny, dist = new Float32Array(N);
    for (let k = 0; k < N; k++) dist[k] = grid[k] ? 0 : 1e9;
    const dpass = (fw) => {
      const js = fw ? [0, ny, 1] : [ny - 1, -1, -1], is = fw ? [0, nx, 1] : [nx - 1, -1, -1], nbr = fw ? [[-1, 0, 3], [0, -1, 3], [-1, -1, 4], [1, -1, 4]] : [[1, 0, 3], [0, 1, 3], [1, 1, 4], [-1, 1, 4]];
      for (let j = js[0]; j !== js[1]; j += js[2]) for (let i = is[0]; i !== is[1]; i += is[2]) {
        const k = j * nx + i; let v = dist[k];
        for (const [di, dj, w] of nbr) { const ii = i + di, jj = j + dj; if (ii < 0 || jj < 0 || ii >= nx || jj >= ny) continue; const c = dist[jj * nx + ii] + w; if (c < v) v = c; }
        dist[k] = v;
      }
    };
    dpass(true); dpass(false);
    // depth (metres, stylised): a shelf that is wide on the Thai / Malay side and narrow off Sumatra and the islands, the basin, the trench
    const tr = lp(TRENCH), segD = (x, y, a, b) => { const dx = b[0] - a[0], dy = b[1] - a[1], t = clamp(((x - a[0]) * dx + (y - a[1]) * dy) / (dx * dx + dy * dy)); return Math.hypot(a[0] + t * dx - x, a[1] + t * dy - y); };
    const depth = new Float32Array(N);
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const k = j * nx + i; if (grid[k]) { depth[k] = 0; continue; }
      const u = wx0 + i * cs, v = wy0 + j * cs, [lo, la] = LL(u, v), dd = (dist[k] / 3) * cs;
      let shelfW = lerp(16, 92, smooth((lo - 95.9) / 1.6));
      if (la > 14.3 && lo > 93.8) shelfW = Math.max(shelfW, 125);                       // the Gulf of Martaban

      let h = dd < shelfW ? 12 + 190 * smooth(dd / shelfW) : 202 + 3000 * smooth((dd - shelfW) / (2.4 * shelfW + 60));
      if (lo > 98.3 && la < 6.6) h = Math.min(h, 100);                                     // the Malacca Strait stays shallow
      if (lo > 99.3 && la > 6.6) h = Math.min(h, 80);                                      // the Gulf of Thailand
      if (lo > 102 && la < 7.5) h = Math.min(h, 90);                                       // the Sunda shelf
      let td = 1e9; for (let s = 0; s + 1 < tr.length; s++) td = Math.min(td, segD(u, v, tr[s], tr[s + 1]));
      if (td < 46) h += 2600 * (1 - (td / 46) ** 2);
      depth[k] = h;
    }
    // travel time (Dijkstra, 16 neighbours), speed ∝ √depth; the source unzips north along the rupture
    const T = new Float64Array(N).fill(1e9), heap = [], push = (k, v) => { heap.push([v, k]); let c = heap.length - 1; while (c > 0) { const p = (c - 1) >> 1; if (heap[p][0] <= heap[c][0]) break; [heap[p], heap[c]] = [heap[c], heap[p]]; c = p; } };
    const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let c = 0; for (;;) { const l = 2 * c + 1, r = l + 1; let m = c; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === c) break; [heap[m], heap[c]] = [heap[c], heap[m]]; c = m; } } return top; };
    const rp = lp(RUPTURE); let along = 0;
    for (let s = 0; s + 1 < rp.length; s++) {
      const a = rp[s], b = rp[s + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.ceil(l / cs);
      for (let q = 0; q <= n; q++) { const u = a[0] + ((b[0] - a[0]) * q) / n, v = a[1] + ((b[1] - a[1]) * q) / n, i = Math.round((u - wx0) / cs), j = Math.round((v - wy0) / cs), k = j * nx + i; const t0 = (along + (l * q) / n) / 420; if (!grid[k] && t0 < T[k]) { T[k] = t0; push(k, t0); } }
      along += l;
    }
    const NB = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]].map(([a, b]) => [a, b, Math.hypot(a, b) * cs]);
    const sp = new Float32Array(N); for (let k = 0; k < N; k++) sp[k] = Math.sqrt(Math.max(depth[k], 4));
    while (heap.length) {
      const [tv, k] = pop(); if (tv > T[k]) continue;
      const i = k % nx, j = (k / nx) | 0;
      for (const [di, dj, l] of NB) {
        const ii = i + di, jj = j + dj; if (ii < 0 || jj < 0 || ii >= nx || jj >= ny) continue;
        const k2 = jj * nx + ii; if (grid[k2]) continue;
        if (Math.abs(di) + Math.abs(dj) === 3 && (grid[j * nx + ii] || grid[jj * nx + i])) continue;   // no knight-jumps across thin land
        const c = tv + l / ((sp[k] + sp[k2]) / 2); if (c < T[k2]) { T[k2] = c; push(k2, c); }
      }
    }
    // the time the leading front reaches the coast at the pin: the sea cell nearest to it
    const [hu, hv] = P(...HOME); let tHome = 1e9;
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const k = j * nx + i; if (grid[k] || T[k] > 1e8) continue; const dd = Math.hypot(wx0 + i * cs - hu, wy0 + j * cs - hv); if (dd < 14 && T[k] < tHome) tHome = T[k]; }
    // isobath bands: closed loops of depth > level (marching squares, border padded with land)
    const val = (i, j) => (i <= 0 || j <= 0 || i >= nx - 1 || j >= ny - 1 ? -1e5 : -depth[j * nx + i]);   // inside = shallower than the level
    const loops = (lev) => {
      const seg = new Map(), ekey = (i, j, h) => (j * nx + i) * 2 + h, pt = (i, j, h) => { const a = h ? val(i, j) : val(i, j), b = h ? val(i + 1, j) : val(i, j + 1), k = (lev - a) / (b - a); return h ? [wx0 + (i + k) * cs, wy0 + j * cs] : [wx0 + i * cs, wy0 + (j + k) * cs]; };
      const P0 = new Map(), link = (ea, eb) => { (seg.get(ea) || seg.set(ea, []).get(ea)).push(eb); (seg.get(eb) || seg.set(eb, []).get(eb)).push(ea); };
      for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
        const a = val(i, j) > lev, b = val(i + 1, j) > lev, c = val(i + 1, j + 1) > lev, dd = val(i, j + 1) > lev, idx = (a ? 8 : 0) | (b ? 4 : 0) | (c ? 2 : 0) | (dd ? 1 : 0);
        if (!idx || idx === 15) continue;
        const top = ekey(i, j, 1), right = ekey(i + 1, j, 0), bot = ekey(i, j + 1, 1), left = ekey(i, j, 0);
        const E = { [top]: [i, j, 1], [right]: [i + 1, j, 0], [bot]: [i, j + 1, 1], [left]: [i, j, 0] };
        Object.entries(E).forEach(([kk, v]) => { if (!P0.has(+kk)) P0.set(+kk, pt(...v)); });
        const pairs = { 1: [[left, bot]], 2: [[bot, right]], 3: [[left, right]], 4: [[top, right]], 5: [[left, top], [bot, right]], 6: [[top, bot]], 7: [[left, top]], 8: [[left, top]], 9: [[top, bot]], 10: [[left, bot], [top, right]], 11: [[top, right]], 12: [[left, right]], 13: [[bot, right]], 14: [[left, bot]] }[idx];
        pairs.forEach(([x, y]) => link(x, y));
      }
      const used = new Set(), out = [];
      seg.forEach((_, start) => {
        if (used.has(start)) return;
        const ring = []; let cur = start, prev = -1;
        for (let n = 0; n < 200000; n++) { used.add(cur); ring.push(P0.get(cur)); const nx2 = (seg.get(cur) || []).find((e) => e !== prev && !used.has(e)); if (nx2 === undefined) break; prev = cur; cur = nx2; }
        if (ring.length > 6) out.push(chaikin(dpRing(ring, 0.8), 2));
      });
      return out;
    };
    const bands = [[3600, "#164a7e"], [2200, "#1b5f94"], [900, "#2277aa"], [200, "#2b95ba"], [60, "#46b9c8"], [22, "#74d3d0"]].map(([lev, col]) => ({ lev, col, rings: loops(-lev) }));
    // mountains along the ranges (only on land)
    const r = mk(77), peaks = [];
    RANGES.forEach(([line, step, spread, h0, h1]) => {
      for (let s = 0; s < line.length - 1; s++) {
        const [a0, a1] = line[s], [b0, b1] = line[s + 1], len = Math.hypot(b0 - a0, b1 - a1), n = Math.max(1, Math.round(len / (step * 1.45))), px = -(b1 - a1) / len, py = (b0 - a0) / len;
        for (let k = 0; k < n; k++) {
          const q = (k + r() * 0.6) / n, cnt = r() < 0.55 ? 2 : 1;
          for (let c = 0; c < cnt; c++) {
            const off = (r() * 2 - 1) * spread, [u, v] = P(a0 + (b0 - a0) * q + px * off, a1 + (b1 - a1) * q + py * off);
            const hh = (h0 + r() * (h1 - h0)) * 0.95, rad = hh * (0.85 + r() * 0.4), cc = code(u, v);
            if (!cc || [[rad, 0], [-rad, 0], [0, rad], [0, -rad]].some(([du, dv]) => !code(u + du, v + dv))) continue;
            const base = Array.from({ length: 6 }, (_, i) => { const a = (i / 6) * PI * 2 + r() * 0.45, rr = rad * (0.72 + r() * 0.4); return [Math.cos(a) * rr, Math.sin(a) * rr]; });
            peaks.push({ u, v, z: hAt(u, v), h: hh, r: rad, base, au: (r() - 0.5) * rad * 0.3, av: (r() - 0.5) * rad * 0.3, tint: r(), karst: false });
          }
        }
      }
    });
    // karst towers in Phang Nga Bay: steep, narrow, standing in the sea
    const rk = mk(404);
    KARST.forEach(([lo, la]) => { const [u, v] = P(lo, la); if (code(u, v)) return; const hh = 3.2 + rk() * 2.6, rad = 2.1 + rk() * 1.3; peaks.push({ u, v, z: 0, h: hh, r: rad, base: Array.from({ length: 7 }, (_, i) => { const a = (i / 7) * PI * 2, rr = rad * (0.75 + rk() * 0.4); return [Math.cos(a) * rr, Math.sin(a) * rr]; }), au: 0, av: 0, tint: rk(), karst: true }); });
    // vegetation tints
    const tints = [];
    RANGES.forEach(([line]) => line.forEach(([lo, la]) => { const [u, v] = P(lo, la); if (code(u, v)) tints.push([u, v, 30 + r() * 16]); }));
    // clouds (kept off the pin and the star)
    const rc = mk(31), clouds = [], [eu, ev] = P(...EPI);
    for (let k = 0; clouds.length < 10 && k < 300; k++) {
      const lo = 90 + rc() * 13, la = 1 + rc() * 15, [u, v] = P(lo, la);
      if (Math.hypot(u - hu, v - hv) < 120 || Math.hypot(u - eu, v - ev) < 110) continue;
      clouds.push({ u, v, z: 58 + rc() * 30, r: 30 + rc() * 40, blobs: Array.from({ length: 5 }, (_, i) => [(i - 2) * 0.42 + (rc() - 0.5) * 0.2, (rc() - 0.5) * 0.35 - (i % 2 ? 0.18 : 0), 0.42 + rc() * 0.32]) });
    }
    // glints on the water
    const rg = mk(211), glints = [];
    for (let k = 0; glints.length < 260 && k < 5000; k++) { const lo = 89 + rg() * 15, la = -1 + rg() * 17, [u, v] = P(lo, la); if (code(u, v) || code(u + 8, v) || code(u - 8, v)) continue; glints.push([u, v, 1.5 + rg() * 3, rg() * 6, 0.6 + rg() * 0.8]); }
    // Thai coast edges with the travel time just offshore (they flare when the front arrives)
    th.rings.forEach((R) => { R.tHit = R.pts.map((a, i) => { if (R.border[i]) return 1e9; const b = R.pts[(i + 1) % R.pts.length], mx = (a[0] + b[0]) / 2 + R.n[i][0] * 7, my = (a[1] + b[1]) / 2 + R.n[i][1] * 7, ii = Math.round((mx - wx0) / cs), jj = Math.round((my - wy0) / cs); if (ii < 0 || jj < 0 || ii >= nx || jj >= ny) return 1e9; return T[jj * nx + ii]; }); });
    DATA = { neigh, th, peaks, tints, clouds, glints, bands, hAt, code, T, nx, ny, cs, wx0, wy0, tHome, home: [hu, hv], epi: [eu, ev], rupture: rp, trench: tr, ruptureLen: along };
    return DATA;
  }

  // ---------------- camera (same model as quakemap.js) ----------------
  function camAt(keys, t) {
    let i = 0;
    while (i + 1 < keys.length && keys[i + 1].t <= t) i++;
    const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)];
    if (a === b || t <= a.t) return { ...a };
    const k = clamp((t - a.t) / (b.t - a.t)), e = i === 0 ? smooth(k) : ease3(k);
    const S = a.S * Math.pow(b.S / a.S, e);
    const [ua, va] = P(a.lon, a.lat), [ub, vb] = P(b.lon, b.lat), w = 1 - (1 - e) * (a.S / S);
    return { u: ua + (ub - ua) * w, v: va + (vb - va) * w, tilt: lerp(a.tilt, b.tilt, e), yaw: lerp(a.yaw, b.yaw, e), S, cy: lerp(a.cy, b.cy, e), uv: true };
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
  const nearFn = (C, z) => { const lim = (C.dist - C.near - z * C.ct) / C.st; return (p) => lim - (-(p[0] - C.u) * C.sy + (p[1] - C.v) * C.cyw); };
  function clipRingE(pts, fn) {
    const n = pts.length, f = pts.map(fn);
    if (f.every((x) => x >= 0)) return pts.map((p, i) => [p[0], p[1], i]);
    const out = [];
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n, a = pts[i], b = pts[j];
      if (f[i] >= 0) out.push([a[0], a[1], i]);
      if ((f[i] >= 0) !== (f[j] >= 0)) { const k = f[i] / (f[i] - f[j]); out.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, f[i] >= 0 ? -1 : i]); }
    }
    return out;
  }
  const pathOf = (pp) => { let s = ""; for (let i = 0; i < pp.length; i++) s += (i ? "L" : "M") + f1(pp[i][0]) + "," + f1(pp[i][1]); return s; };
  const ringPath = (C, pts, z, fn) => { const c = clipEdge(pts, fn); return c.length >= 3 ? pathOf(c.map((p) => proj(C, p[0], p[1], z))) + "Z" : ""; };
  const segClip = (a, b, fn) => { const fa = fn(a), fb = fn(b); if (fa < 0 && fb < 0) return null; if (fa >= 0 && fb >= 0) return [a, b]; const k = fa / (fa - fb), m = [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; return fa >= 0 ? [a, m] : [m, b]; };
  const lineOf = (C, pts, zf, fn) => { let s = ""; for (let i = 0; i + 1 < pts.length; i++) { const sg = segClip(pts[i], pts[i + 1], fn); if (!sg) continue; const p = proj(C, sg[0][0], sg[0][1], zf(sg[0])), q = proj(C, sg[1][0], sg[1][1], zf(sg[1])); s += `M${f1(p[0])},${f1(p[1])}L${f1(q[0])},${f1(q[1])}`; } return s; };
  const circ = (u, v, r, n = 40) => Array.from({ length: n }, (_, i) => [u + Math.cos((i / n) * PI * 2) * r, v + Math.sin((i / n) * PI * 2) * r]);

  // isochrones of the travel-time field at level lev (marching squares, stitched by shared cell edges, smoothed), map units
  const chaikinOpen = (pts, it) => { for (let k = 0; k < it; k++) { if (pts.length < 3) return pts; const out = [pts[0]]; for (let i = 0; i + 1 < pts.length; i++) { const a = pts[i], b = pts[i + 1]; out.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25], [a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } out.push(pts[pts.length - 1]); pts = out; } return pts; };
  function iso(Dd, lev) {
    const { T, nx, ny, cs, wx0, wy0 } = Dd, BIG = 1e8;
    const at = new Map(), link = (a, b) => { (at.get(a) || at.set(a, []).get(a)).push(b); (at.get(b) || at.set(b, []).get(b)).push(a); };
    const P0 = new Map();
    const hp = (i, j) => { const kk = (j * nx + i) * 2 + 1; if (!P0.has(kk)) { const a = T[j * nx + i], b = T[j * nx + i + 1], k = a > BIG || b > BIG ? 0.5 : (lev - a) / (b - a); P0.set(kk, [wx0 + (i + k) * cs, wy0 + j * cs]); } return kk; };
    const vp = (i, j) => { const kk = (j * nx + i) * 2; if (!P0.has(kk)) { const a = T[j * nx + i], b = T[(j + 1) * nx + i], k = a > BIG || b > BIG ? 0.5 : (lev - a) / (b - a); P0.set(kk, [wx0 + i * cs, wy0 + (j + k) * cs]); } return kk; };
    for (let j = 0; j < ny - 1; j++) {
      const r0 = j * nx, r1 = r0 + nx;
      for (let i = 0; i < nx - 1; i++) {
        const a = T[r0 + i] < lev, b = T[r0 + i + 1] < lev, c = T[r1 + i + 1] < lev, d = T[r1 + i] < lev;
        const idx = (a ? 8 : 0) | (b ? 4 : 0) | (c ? 2 : 0) | (d ? 1 : 0);
        if (!idx || idx === 15) continue;
        const top = () => hp(i, j), right = () => vp(i + 1, j), bot = () => hp(i, j + 1), left = () => vp(i, j);
        switch (idx) {
          case 1: case 14: link(left(), bot()); break;
          case 2: case 13: link(bot(), right()); break;
          case 3: case 12: link(left(), right()); break;
          case 4: case 11: link(top(), right()); break;
          case 6: case 9: link(top(), bot()); break;
          case 7: case 8: link(left(), top()); break;
          case 5: link(left(), top()); link(bot(), right()); break;
          case 10: link(left(), bot()); link(top(), right()); break;
        }
      }
    }
    const used = new Set(), lines = [];
    const walk = (start) => { const line = [P0.get(start)]; used.add(start); let prev = -1, cur = start; for (;;) { const nx2 = (at.get(cur) || []).find((e) => e !== prev && !used.has(e)); if (nx2 === undefined) break; used.add(nx2); line.push(P0.get(nx2)); prev = cur; cur = nx2; } return line; };
    at.forEach((nb, kk) => { if (!used.has(kk) && nb.length === 1) lines.push(walk(kk)); });   // open lines first (from their ends)
    at.forEach((nb, kk) => { if (!used.has(kk)) { const l = walk(kk); l.push(l[0]); lines.push(l); } }); // then closed loops
    return lines.filter((l) => l.length > 3).map((l) => chaikinOpen(l, 2));
  }

  // ---------------- one frame of the map ----------------
  const WALL = { nb: ["#6f5a3e", "#d3bb8e"], th: ["#82643f", "#e8cc98"] };
  function walls(C, land, isTh) {
    const shades = isTh ? WALL.th : WALL.nb, q = ["", "", "", "", "", ""];
    let foam = "", strata = "";
    land.rings.forEach((R) => {
      const c = clipRingE(R.pts, nearFn(C, R.z));
      for (let i = 0; i < c.length; i++) {
        const a = c[i], b = c[(i + 1) % c.length], e = a[2];
        if (e < 0) continue;
        const n = R.n[e], mu = (a[0] + b[0]) / 2, mv = (a[1] + b[1]) / 2;
        if ((C.gu - mu) * n[0] + (C.gv - mv) * n[1] <= 0) continue;
        const border = isTh && R.border[e], z0 = border ? H : 0, z1 = R.z;
        const lit = clamp(0.5 + 0.62 * (n[0] * LN[0] + n[1] * LN[1])), bucket = Math.round(lit * 5);
        const A0 = proj(C, a[0], a[1], z0), B0 = proj(C, b[0], b[1], z0), B1 = proj(C, b[0], b[1], z1), A1 = proj(C, a[0], a[1], z1);
        q[bucket] += `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}L${f1(B1[0])},${f1(B1[1])}L${f1(A1[0])},${f1(A1[1])}Z`;
        if (!border) {
          foam += `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}`;
          const Am = proj(C, a[0], a[1], z1 * 0.45), Bm = proj(C, b[0], b[1], z1 * 0.45);
          strata += `M${f1(Am[0])},${f1(Am[1])}L${f1(Bm[0])},${f1(Bm[1])}`;
        }
      }
    });
    let s = "";
    q.forEach((d, k) => { if (d) s += `<path d="${d}" fill="${mix(shades[0], shades[1], k / 5)}" stroke="${mix(shades[0], shades[1], k / 5)}" stroke-width="0.8" stroke-linejoin="round"/>`; });
    if (strata) s += `<path d="${strata}" stroke="#5c4428" stroke-width="1.6" opacity=".22" fill="none"/>`;
    if (foam) s += `<path d="${foam}" stroke="#f2fdff" stroke-width="2.6" opacity=".85" fill="none" stroke-linecap="round"/>`;
    return s;
  }

  function frame(inst, t) {
    const Dd = data(), o = inst.o, C = camera(camAt(inst.keys, t)), z0f = nearFn(C, 0), zHf = nearFn(C, H), zTf = nearFn(C, HTH);
    const S = C.S, out = [];
    // the sea: shallow turquoise plane, deeper bands on top, glints
    const sea = [P(60, 40), P(140, 40), P(140, -30), P(60, -30)];
    out.push(`<path d="${ringPath(C, sea, 0, z0f)}" fill="#103a66"/>`);
    Dd.bands.forEach(({ col, rings }) => { let d = ""; rings.forEach((r) => (d += ringPath(C, r, 0, z0f))); if (d) out.push(`<path d="${d}" fill="${col}" fill-rule="evenodd" stroke="${mix(col, "#ffffff", 0.35)}" stroke-width="${f1(clamp(0.5 * S, 1, 2.4))}" stroke-opacity=".45" stroke-linejoin="round"/>`); });
    // the trench as a dark seam, the graticule
    out.push(`<path d="${lineOf(C, Dd.trench, () => 0, z0f)}" stroke="#0a2a4c" stroke-width="${f1(clamp(4 * S, 6, 22))}" opacity=".35" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`);
    let gr = "";
    for (let lo = 88; lo <= 106; lo += 2) gr += lineOf(C, [P(lo, -4), P(lo, 18)], () => 0, z0f);
    for (let la = -2; la <= 18; la += 2) gr += lineOf(C, [P(86, la), P(108, la)], () => 0, z0f);
    out.push(`<path d="${gr}" stroke="#eaf8fc" stroke-width="1.3" opacity=".13" fill="none"/>`);
    let gl = "";
    Dd.glints.forEach(([u, v, l, ph, sp]) => { const op = 0.5 + 0.5 * Math.sin(t * 2.2 * sp + ph); if (op < 0.25) return; const uu = u + ((t * 2.4 * sp + ph * 9) % 18) - 9; const sg = segClip([uu - l, v], [uu + l, v], z0f); if (!sg) return; const a = proj(C, sg[0][0], sg[0][1], 0), b = proj(C, sg[1][0], sg[1][1], 0); gl += `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}`; });
    out.push(`<path d="${gl}" stroke="#f2fcff" stroke-width="${f1(clamp(0.5 * S, 1.2, 3))}" stroke-linecap="round" opacity=".42"/>`);
    // shallow rims along every coast, and the slabs' soft shadow on the water
    let coast = "", lsh = "";
    [...Dd.neigh, Dd.th].forEach((l) => l.rings.forEach((R) => { coast += ringPath(C, R.pts, 0, z0f); lsh += ringPath(C, R.pts.map((p) => [p[0] + H * 0.55, p[1] + H * 0.7]), 0, z0f); }));
    out.push(`<path d="${coast}" fill="none" stroke="#9fe8de" stroke-width="${f1(Math.min(30, 5 * S))}" opacity=".5" stroke-linejoin="round"/><path d="${lsh}" fill="#04243c" opacity=".2"/>`);
    const groundText = (txt, lo, la, size, z, fill, extra = "") => {
      const [u, v] = P(lo, la), p0 = proj(C, u, v, z), px = proj(C, u + 1, v, z), py = proj(C, u, v + 1, z);
      if (p0[2] < C.near * 1.5) return "";
      return `<text transform="matrix(${f1(px[0] - p0[0])} ${f1(px[1] - p0[1])} ${f1(py[0] - p0[0])} ${f1(py[1] - p0[1])} ${f1(p0[0])} ${f1(p0[1])})" text-anchor="middle" font-family="Kanit" font-size="${size}" fill="${fill}" ${extra}>${txt}</text>`;
    };
    NAMES.filter((n) => n[4] === 1).forEach(([txt, lo, la, sz]) => out.push(groundText(txt, lo, la, sz, 0, "#e6f8fb", `font-weight="700" font-style="italic" letter-spacing="3" opacity=".72"`)));

    // ---- the waves: three crests, each a raised ribbon (shadow on the water, a bright foam line above, a glow band) ----
    const tq = o.quakeAt ?? 0.4, tr = o.ringsAt ?? tq + 0.4, tc = o.coastAt ?? 6.2;
    const tau = t < tr ? -1 : ((t - tr) / Math.max(0.5, tc - tr)) * Dd.tHome;
    const GAP = Dd.tHome * 0.11, fronts = [];
    [0, 1, 2].forEach((n) => { const lev = tau - n * GAP; if (lev > 0.05) fronts.push([n, lev]); });
    fronts.reverse().forEach(([n, lev]) => {
      const lines = iso(Dd, lev), a = n === 0 ? 1 : n === 1 ? 0.62 : 0.4;
      let dS = "", dT = "";
      lines.forEach((l) => {
        let pen = false;
        for (let i = 0; i + 1 < l.length; i++) {
          const sg = segClip(l[i], l[i + 1], z0f); if (!sg) { pen = false; continue; }
          const A = proj(C, sg[0][0], sg[0][1], 0), B = proj(C, sg[1][0], sg[1][1], 0), A2 = proj(C, sg[0][0], sg[0][1], 2.4), B2 = proj(C, sg[1][0], sg[1][1], 2.4);
          if (!pen) { dS += `M${f1(A[0])},${f1(A[1])}`; dT += `M${f1(A2[0])},${f1(A2[1])}`; }
          dS += `L${f1(B[0])},${f1(B[1])}`; dT += `L${f1(B2[0])},${f1(B2[1])}`; pen = sg[1] === l[i + 1];
        }
      });
      if (!dS) return;
      out.push(`<path d="${dS}" stroke="#bff4ff" stroke-width="${f1(clamp(16 * S, 18, 80))}" opacity="${f1(0.09 * a)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="${dS}" stroke="#ffffff" stroke-width="${f1(clamp(8 * S, 12, 46))}" opacity="${f1(0.14 * a)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="${dS}" stroke="#032038" stroke-width="${f1(clamp(1.8 * S, 3, 9))}" opacity="${f1(0.45 * a)}" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate(${f1(clamp(0.8 * S, 1, 4))},${f1(clamp(1.2 * S, 1.5, 6))})"/>
        <path d="${dT}" stroke="${n === 0 ? "#fff8e6" : "#e6fbff"}" stroke-width="${f1(clamp(1.7 * S, 3, 9))}" opacity="${f1(0.95 * a)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="${dT}" stroke="#ffffff" stroke-width="${f1(clamp(0.55 * S, 1.1, 2.8))}" opacity="${f1(a)}" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate(0,${f1(-clamp(0.6 * S, 0.6, 3))})"/>`);
    });

    // the land: neighbours (walls, tops), tints, then Thailand one step up with its rim
    out.push(walls(C, { rings: Dd.neigh.flatMap((l) => l.rings) }, false));
    Dd.neigh.forEach((l) => { let d = ""; l.rings.forEach((R) => (d += ringPath(C, R.pts, R.z, nearFn(C, R.z)))); if (d) out.push(`<path d="${d}" fill="#e9dfbd" stroke="#c4ae86" stroke-width="1.6" stroke-linejoin="round"/>`); });
    let tn = "";
    Dd.tints.forEach(([u, v, rr]) => { const z = Dd.hAt(u, v); if (!z || Dd.code(u, v) !== 1) return; const d = ringPath(C, circ(u, v, rr, 20), z + 0.1, nearFn(C, z)); if (d) tn += `<path d="${d}" fill="url(#tmGreen)"/>`; });
    out.push(tn);
    out.push(walls(C, Dd.th, true));
    let thd = ""; Dd.th.rings.forEach((R) => (thd += ringPath(C, R.pts, R.z, nearFn(C, R.z))));
    out.push(`<path d="${thd}" fill="#fbf3d8" stroke="#b58e5c" stroke-width="2" stroke-linejoin="round"/><path d="${thd}" fill="none" stroke="#ffffff" stroke-width="2.2" opacity=".75" transform="translate(0,1.6)" stroke-linejoin="round"/>`);
    let tt = "";
    Dd.tints.forEach(([u, v, rr]) => { if (Dd.code(u, v) !== 2) return; const z = Dd.hAt(u, v); const d = ringPath(C, circ(u, v, rr, 20), z + 0.1, nearFn(C, z)); if (d) tt += `<path d="${d}" fill="url(#tmGreen)"/>`; });
    out.push(tt);
    NAMES.filter((n) => n[4] !== 1).forEach(([txt, lo, la, sz, kind]) => { const [u, v] = P(lo, la); out.push(groundText(txt, lo, la, sz, Dd.hAt(u, v) + 0.2, kind === 2 ? "#b88c4c" : "#9c8762", `font-weight="${kind === 2 ? 900 : 700}" letter-spacing="4" opacity="${kind === 2 ? 0.9 : 0.8}"`)); });
    PLACES.forEach(([txt, lo, la]) => { const [u, v] = P(lo, la); if (S < 2.2) return; out.push(groundText(txt, lo, la, 8, Dd.hAt(u, v) + 0.2, "#7c6440", `font-weight="700" opacity="${f1(clamp((S - 2.2) / 0.8) * 0.85)}"`)); });

    // the Thai coast flares where the leading front has arrived
    if (tau > 0) {
      let hit = "", hot = "";
      Dd.th.rings.forEach((R) => {
        const c = clipRingE(R.pts, nearFn(C, R.z));
        for (let i = 0; i < c.length; i++) {
          const a = c[i], b = c[(i + 1) % c.length], e = a[2]; if (e < 0) continue;
          const th0 = R.tHit[e]; if (th0 > tau) continue;
          const A0 = proj(C, a[0], a[1], 0.6), B0 = proj(C, b[0], b[1], 0.6), seg = `M${f1(A0[0])},${f1(A0[1])}L${f1(B0[0])},${f1(B0[1])}`;
          hit += seg; if (tau - th0 < Dd.tHome * 0.05) hot += seg;
        }
      });
      if (hit) out.push(`<path d="${hit}" stroke="#ff6a3a" stroke-width="${f1(clamp(2.4 * S, 4, 14))}" opacity=".55" fill="none" stroke-linecap="round"/><path d="${hit}" stroke="#ffffff" stroke-width="${f1(clamp(0.9 * S, 1.6, 5))}" opacity=".95" fill="none" stroke-linecap="round"/>`);
      if (hot) out.push(`<path d="${hot}" stroke="#fff3c8" stroke-width="${f1(clamp(5 * S, 8, 30))}" opacity=".5" fill="none" stroke-linecap="round"/>`);
    }

    // the rupture: a glowing seam that unzips north from the star along the arc
    const [eu, ev] = Dd.epi, pop = t < tq ? 0 : backOut((t - tq) / 0.45, 2.4), pulse = 1 + 0.12 * Math.sin(t * 9);
    if (pop > 0) {
      const d = ringPath(C, circ(eu, ev, 58 * pop * pulse, 36), 0.3, z0f); if (d) out.push(`<path d="${d}" fill="url(#tmEpi)"/>`);
      const len = Dd.ruptureLen * smooth((t - tq) / 1.8), rp = Dd.rupture, cut = [rp[0]]; let acc = 0;
      for (let s = 0; s + 1 < rp.length && acc < len; s++) { const a = rp[s], b = rp[s + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]), k = clamp((len - acc) / l); cut.push([a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]); acc += l; }
      if (cut.length > 1) { const cl = lineOf(C, cut, () => 0.5, z0f); out.push(`<path d="${cl}" stroke="#ff7a3a" stroke-width="${f1(clamp(6 * S, 14, 34))}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/><path d="${cl}" stroke="#3a0e06" stroke-width="${f1(clamp(2.4 * S, 5, 13))}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/><path d="${cl}" stroke="#ffc24a" stroke-width="${f1(clamp(0.9 * S, 2, 5))}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`); }
    }
    // cloud shadows
    const drift = 3.2 * t;
    Dd.clouds.forEach((c) => { const u = c.u + drift + c.z * 0.35, v = c.v + c.z * 0.45, z = Dd.hAt(u, v), d = ringPath(C, circ(u, v, c.r * 1.25, 18), z + 0.2, nearFn(C, z)); if (d) out.push(`<path d="${d}" fill="url(#tmShade)"/>`); });
    let msh = "";
    Dd.peaks.forEach((pk) => { const d = ringPath(C, circ(pk.u + pk.h * 0.18, pk.v + pk.h * 0.22, pk.r * 1.12, 12), pk.z + 0.1, nearFn(C, pk.z)); if (d) msh += d; });
    out.push(`<path d="${msh}" fill="#20301e" opacity=".14"/>`);

    // ---- things that stand up, far to near ----
    const objs = [], cam3 = [C.gu, C.gv, C.gz];
    const face = (pts3, base) => {
      const [a, b, c] = pts3, ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
      const cx = pts3.reduce((s, p) => s + p[0], 0) / pts3.length, cy = pts3.reduce((s, p) => s + p[1], 0) / pts3.length, cz = pts3.reduce((s, p) => s + p[2], 0) / pts3.length;
      if (nx * (cx - base[0]) + ny * (cy - base[1]) + nz * (cz - base[2]) < 0) { nx = -nx; ny = -ny; nz = -nz; }
      if (nx * (cam3[0] - cx) + ny * (cam3[1] - cy) + nz * (cam3[2] - cz) <= 0) return null;
      return { lit: clamp(0.3 + 0.75 * Math.max(0, nx * LN[0] + ny * LN[1] + nz * LN[2])), pp: pts3.map((p) => proj(C, p[0], p[1], p[2])) };
    };
    Dd.peaks.forEach((pk) => {
      const pc = proj(C, pk.u, pk.v, pk.z);
      if (pc[2] < C.near * 1.2 || pc[0] < -300 || pc[0] > 1380 || pc[1] < -400 || pc[1] > 2300) return;
      const ctr = [pk.u, pk.v, pk.z]; let s = "";
      if (pk.karst) { // a limestone tower: straight-ish walls, a jungle cap, a wet foot
        const nb = pk.base.length, top = pk.base.map(([x, y]) => [pk.u + x * 0.7, pk.v + y * 0.7, pk.z + pk.h]);
        for (let i = 0; i < nb; i++) { const b0 = pk.base[i], b1 = pk.base[(i + 1) % nb], f = face([[pk.u + b0[0], pk.v + b0[1], pk.z], [pk.u + b1[0], pk.v + b1[1], pk.z], top[(i + 1) % nb], top[i]], ctr); if (!f) continue; const col = mix("#6f8476", "#d8dcc4", Math.pow(f.lit, 1.2)); s += `<path d="${pathOf(f.pp)}Z" fill="${col}" stroke="${mix(col, "#2a3030", 0.5)}" stroke-width="0.9" stroke-linejoin="round"/>`; }
        const tp = top.map((p) => proj(C, ...p)), cap = proj(C, pk.u, pk.v, pk.z + pk.h * 1.12);
        s += `<path d="${pathOf(tp)}Z" fill="#4f8a46" stroke="#24401f" stroke-width="0.9"/><path d="M${tp.map((p) => `${f1((p[0] + cap[0]) / 2)},${f1((p[1] + cap[1]) / 2)}`).join("L")}Z" fill="#6aa65a" opacity=".9"/>`;
        objs.push([pc[2], s]); return;
      }
      const ap = [pk.u + pk.au, pk.v + pk.av, pk.z + pk.h];
      const lit0 = mix("#4f6a3a", "#6b5f3e", pk.tint), lit1 = mix("#d8d496", "#e8d6a2", pk.tint);
      const nb = pk.base.length;
      for (let i = 0; i < nb; i++) {
        const b0 = pk.base[i], b1 = pk.base[(i + 1) % nb], f = face([[pk.u + b0[0], pk.v + b0[1], pk.z], [pk.u + b1[0], pk.v + b1[1], pk.z], ap], ctr);
        if (!f) continue;
        const col = mix(lit0, lit1, Math.pow(f.lit, 1.25));
        s += `<path d="${pathOf(f.pp)}Z" fill="${col}" stroke="${mix(col, "#2a3018", 0.45)}" stroke-width="1" stroke-linejoin="round"/>`;
      }
      const ap2 = proj(C, ...ap), bl = proj(C, pk.u + pk.base[4][0] * 0.9, pk.v + pk.base[4][1] * 0.9, pk.z);
      s += `<path d="M${f1(ap2[0])},${f1(ap2[1])}L${f1(bl[0])},${f1(bl[1])}" stroke="#fffbe6" stroke-width="1.1" opacity=".45"/>`;
      objs.push([pc[2], s]);
    });
    objs.sort((a, b) => b[0] - a[0]);
    out.push(objs.map((x) => x[1]).join(""));

    // ---- above the ground: the star, the pin, clouds ----
    if (pop > 0) {
      const p = proj(C, eu, ev, 30), sc = clamp(S / 1.4, 0.8, 2.2), sq = 1 + 0.18 * Math.sin(t * 14) * clamp(1 - (t - tq) / 3), rot = 8 * Math.sin(t * 20), tether = proj(C, eu, ev, 0.5);
      out.push(`<path d="M${f1(tether[0])},${f1(tether[1])}L${f1(p[0])},${f1(p[1])}" stroke="#ff8a3a" stroke-width="3" opacity=".5"/>
        <g transform="translate(${f1(p[0])},${f1(p[1])}) scale(${f1(sc * pop)})"><circle r="${f1(110 * pulse)}" fill="url(#tmBurst)"/>
        <g transform="rotate(${f1(rot)}) scale(${f1(sq)},${f1(2 - sq)})"><path d="${STAR}" transform="translate(0,7)" fill="#9a3a10" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/><path d="${STAR}" fill="url(#tmStar)" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/><path d="M-7,-22l7,-14l7,14" stroke="#fffbe0" stroke-width="3.5" fill="none" opacity=".9" stroke-linecap="round" stroke-linejoin="round"/></g></g>`);
    }
    const [hu, hv] = Dd.home, pk0 = o.pinAt ?? 5.6;
    inst.pinHead = null;
    if (t > pk0) {
      const k = (t - pk0) / 0.65, drop = bounceOut(k), zp = HTH + 52 + (1 - drop) * 130 + (t > pk0 + 0.7 ? 2 * Math.sin((t - pk0) * 4) : 0);
      const head = proj(C, hu, hv, zp), foot = proj(C, hu, hv, HTH + 0.3), r = clamp(22 + 7 * Math.log2(S), 20, 44);
      const shd = ringPath(C, circ(hu, hv, 3 + 2.5 * drop, 18), HTH + 0.2, zTf);
      out.push(`${shd ? `<path d="${shd}" fill="url(#tmSoft)" opacity="${f1(clamp(k * 2))}"/>` : ""}<path d="M${f1(foot[0])},${f1(foot[1])}L${f1(head[0])},${f1(head[1])}" stroke="#140e0a" stroke-width="2.4" opacity="${f1(0.55 * clamp(k * 2))}" stroke-dasharray="5 5"/>
        <g transform="translate(${f1(head[0])},${f1(head[1])}) scale(${f1(r / 36)})" opacity="${f1(clamp(k * 3))}"><path d="M0,0C-30,-34 -36,-56 -36,-70A36,36 0 0 1 36,-70C36,-56 30,-34 0,0Z" fill="url(#tmPin)" stroke="#140e0a" stroke-width="4.5" stroke-linejoin="round"/>
        <path d="M-22,-84A26,26 0 0 1 2,-100" stroke="#ffc8b8" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/><circle cy="-70" r="13" fill="#fff" stroke="#140e0a" stroke-width="3"/></g>`);
      inst.pinHead = [head[0], head[1] - r * 2];
    }
    const cl = [];
    Dd.clouds.forEach((c) => {
      const p = proj(C, c.u + drift, c.v, H + c.z);
      if (p[2] < C.near * 1.6) return;
      const pr = (c.r * F) / p[2], fade = clamp((360 - pr) / 180) * 0.85;
      if (fade <= 0.02 || p[0] < -pr * 2 || p[0] > 1080 + pr * 2 || p[1] < -pr || p[1] > 2100 + pr) return;
      cl.push([p[2], `<g opacity="${f1(fade)}"><ellipse cx="${f1(p[0])}" cy="${f1(p[1] + pr * 0.22)}" rx="${f1(pr * 1.15)}" ry="${f1(pr * 0.34)}" fill="url(#tmCloudB)"/>${c.blobs.map(([ox, oy, br]) => `<ellipse cx="${f1(p[0] + ox * pr)}" cy="${f1(p[1] + oy * pr * 0.7)}" rx="${f1(br * pr)}" ry="${f1(br * pr * 0.72)}" fill="url(#tmCloud)"/>`).join("")}</g>`]);
    });
    cl.sort((a, b) => b[0] - a[0]);
    out.push(cl.map((c) => c[1]).join(""));
    const hz = 260 + 520 * clamp((C.tilt - 25) / 35);
    out.push(`<rect x="-60" y="-60" width="1200" height="${f1(hz + 60)}" fill="url(#tmHaze)"/>`);
    inst.g.innerHTML = out.join("");
    const pe = proj(C, eu, ev, 30);
    inst.anchor = { epi: [pe[0], pe[1]], S };
    return inst;
  }

  // the default flight: wide over the basin, follow the fronts east, settle low over Khao Lak's coast and orbit
  const flight = (o) => {
    const tr = o.ringsAt ?? (o.quakeAt ?? 0.4) + 0.4, tc = o.coastAt ?? 6.2, dur = o.dur ?? 9;
    return [
      { t: 0, lon: 95.9, lat: 7.2, tilt: 30, yaw: -4, S: 1.02, cy: 960 },
      { t: tr + 0.8, lon: 96.2, lat: 7.4, tilt: 33, yaw: -2, S: 1.12, cy: 980 },
      { t: Math.max(tr + 1.6, tc - 1.4), lon: 97.55, lat: 8.2, tilt: 44, yaw: 5, S: 2.0, cy: 1060 },
      { t: tc + 0.6, lon: 98.02, lat: 8.5, tilt: 50, yaw: 9, S: 3.3, cy: 1150 },
      { t: Math.max(tc + 1.2, dur), lon: 98.04, lat: 8.48, tilt: 52, yaw: 12, S: 3.55, cy: 1150 },
    ];
  };

  function tideMap3d(L, o = {}) {
    const id = o.id || "tm";
    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#tmSky)"/>`);
    put(L.set, `<g id="${id}-m3"></g>`);
    const inst = { id, o: { ...o }, keys: o.cam || flight(o), g: document.getElementById(`${id}-m3`) };
    L.tm3d = inst;
    frame(inst, 0);
  }

  // ---------------- 2.5D pills, coins (screen space) ----------------
  const pill = (w, h, o = {}) => {
    const r = o.r ?? h / 2, face = o.face || "url(#tmFaceD)", slab = o.slab || "#02060a", st = o.stroke || "#140e0a";
    return `<ellipse cx="0" cy="${f1(h / 2 + 18)}" rx="${f1(w * 0.46)}" ry="14" fill="url(#tmSoft)"/>
      <rect x="${f1(-w / 2)}" y="${f1(-h / 2 + 9)}" width="${w}" height="${h}" rx="${r}" fill="${slab}" stroke="#140e0a" stroke-width="4"/>
      <rect x="${f1(-w / 2)}" y="${f1(-h / 2)}" width="${w}" height="${h}" rx="${r}" fill="${face}" stroke="${st}" stroke-width="${o.sw ?? 4.5}"/>
      <path d="M${f1(-w / 2 + r * 0.9)},${f1(-h / 2 + 7)}H${f1(w / 2 - r * 0.9)}" stroke="#fff" stroke-width="3.5" opacity="${o.hi ?? 0.28}" stroke-linecap="round"/>`;
  };
  const popIn = (tl, sel, at) => {
    tl.fromTo(sel, { scaleX: 0.1, scaleY: 0.1, opacity: 0, svgOrigin: "0 0" }, { scaleX: 0.82, scaleY: 1.24, opacity: 1, svgOrigin: "0 0", duration: 0.14, ease: "power2.out", immediateRender: false }, at);
    tl.to(sel, { scaleX: 1.16, scaleY: 0.86, svgOrigin: "0 0", duration: 0.1, ease: "sine.inOut" }, at + 0.14);
    tl.to(sel, { scaleX: 1, scaleY: 1, svgOrigin: "0 0", duration: 0.42, ease: "elastic.out(1, 0.42)" }, at + 0.24);
  };
  // a clock face with a minute hand (#<id>) for the chip
  const clockIcon = (id) => `<circle r="30" fill="#fffaf0" stroke="#140e0a" stroke-width="4.5"/><circle r="30" fill="none" stroke="#ffd23a" stroke-width="3" opacity=".6" transform="scale(.82)"/>
    ${[0, 1, 2, 3].map((k) => `<path d="M0,-25V-20" stroke="#140e0a" stroke-width="3.5" stroke-linecap="round" transform="rotate(${k * 90})"/>`).join("")}
    <path d="M0,0L0,-13" stroke="#140e0a" stroke-width="4.5" stroke-linecap="round" transform="rotate(120)"/><g id="${id}"><path d="M0,3L0,-22" stroke="#e2392c" stroke-width="3.5" stroke-linecap="round"/></g><circle r="4" fill="#140e0a"/>`;

  function play(tl, L, sid, t0, o = {}) {
    const inst = L.tm3d, id = `${sid}-tm`, dur = o.dur ?? 9;
    Object.assign(inst.o, o);
    inst.keys = o.cam || flight(inst.o);
    put(L.light, `<g id="${id}-chip" transform="translate(540,200)"><g id="${id}-chipB"><g id="${id}-chipP" opacity="0">${pill(620, 104, { stroke: "#ffd23a", sw: 5 })}
        <g transform="translate(-246,0)">${clockIcon(`${id}-clk`)}</g>
        <text x="34" y="17" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="48" fill="#fff6e8">${o.chip || "คลื่นกำลังมา"}</text></g></g></g>
      <g id="${id}-el" transform="translate(-999,-999)"><g id="${id}-elB"><g id="${id}-elP" opacity="0">${pill(392, 78, { stroke: "#140e0a" })}
        <text y="13" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="36" fill="#ffd23a">${o.epiLabel || "แผ่นดินไหวใต้ทะเล"}</text></g></g></g>
      <g id="${id}-pl" transform="translate(-999,-999)"><g id="${id}-plB"><g id="${id}-plP" opacity="0">${pill(430, 84, { face: "url(#tmFaceC)", slab: "#a8936a", hi: 0.7 })}
        <text y="14" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="38" fill="#140e0a">${o.pinLabel || "บ้านแหลมหอย (สมมติ)"}</text></g></g></g>`);
    const $ = (s) => document.getElementById(`${id}-${s}`);
    const el = $("el"), pl = $("pl");
    const place = (t) => {
      frame(inst, t);
      const A = inst.anchor;
      el.setAttribute("transform", `translate(${f1(clamp(A.epi[0] + 40, 230, 850))},${f1(A.epi[1] + 110)})`);
      el.setAttribute("opacity", f1(clamp(Math.min((A.epi[0] + 60) / 160, (A.epi[1] - 240) / 120, (1960 - A.epi[1]) / 160))));
      if (inst.pinHead) pl.setAttribute("transform", `translate(${f1(clamp(inst.pinHead[0] + 210, 240, 850))},${f1(inst.pinHead[1] + 34)})`);
    };
    const px = { t: 0 };
    tl.fromTo(px, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: () => place(px.t) }, t0);
    place(0);
    const ca = o.chipAt ?? 0.3, tq = inst.o.quakeAt ?? 0.4, pk = inst.o.pinAt ?? 5.6;
    popIn(tl, `#${id}-chipP`, t0 + ca);
    tl.fromTo(`#${id}-clk`, { rotation: 0, svgOrigin: "0 0" }, { rotation: 360 * Math.max(1, Math.round(dur / 1.6)), svgOrigin: "0 0", duration: dur - ca, ease: "none", immediateRender: false }, t0 + ca);
    popIn(tl, `#${id}-elP`, t0 + tq + 0.5);
    tl.to(`#${id}-elP`, { opacity: 0, duration: 0.3 }, t0 + Math.max(tq + 2.4, pk - 1.8));
    popIn(tl, `#${id}-plP`, t0 + pk + 0.45);
    [["elB", 0], ["plB", 0.4], ["chipB", 0.8]].forEach(([s, ph]) => tl.fromTo(`#${id}-${s}`, { y: -3 }, { y: 3, duration: 0.9, repeat: Math.ceil(dur / 0.9), yoyo: true, ease: "sine.inOut", immediateRender: false }, t0 + ph));
    if (o.out !== undefined) tl.to(`#${id}-chipP`, { opacity: 0, duration: 0.2 }, t0 + o.out);
  }

  // =====================================================================================================================
  // ---------------- the cross-section ----------------
  // world units: x 0 → 3300 left (deep sea) to right (hill), z up from sea level; the block's cut face is at the front, the sea
  // surface and the land run back from it (an oblique offset that the block's camera sets per frame)
  const SX1 = 3300, ZBOT = -620, FAULT = 950;
  const zg0 = (x) => {
    if (x < 1700) return -520 + 10 * Math.sin(x * 0.004) + 6 * Math.sin(x * 0.011 + 1);
    if (x < 2050) return lerp(-520, -96, smooth((x - 1700) / 350));
    if (x < 2700) return lerp(-96, -16, (x - 2050) / 650) + 3 * Math.sin(x * 0.02);
    if (x < 2880) return lerp(-16, 14, smooth((x - 2700) / 180));
    if (x < 3050) return 14 + 4 * smooth((x - 2880) / 170);
    return 18 + 280 * smooth((x - 3050) / 250);
  };
  const upl = (x) => (x > 480 && x < FAULT ? 34 * smooth((x - 480) / 120) : x >= FAULT && x < 1300 ? -12 * (1 - smooth((x - FAULT) / 350)) : 0);
  const depthAt = (x) => Math.max(2, -zg0(x));
  // travel time of the crest from x=760 to the shore (∝ ∫ dx / √h), normalised to 1 at x=2640
  const TT = (() => { const xs = [], ts = []; let acc = 0; for (let x = 760; x <= 2700; x += 4) { xs.push(x); ts.push(acc); acc += 4 / Math.sqrt(depthAt(x)); } const iEnd = xs.findIndex((x) => x >= 2640); const tot = ts[iEnd]; return { xs, ts: ts.map((v) => v / tot) }; })();
  const crestAt = (p) => { const { xs, ts } = TT; if (p <= 0) return 760; for (let i = 1; i < ts.length; i++) if (ts[i] >= p) { const k = (p - ts[i - 1]) / (ts[i] - ts[i - 1]); return xs[i - 1] + 4 * k; } return xs[xs.length - 1]; };
  const width = (x) => clamp(380 * Math.sqrt(depthAt(x) / 520), 150, 380);
  const ampRaw = (x) => Math.min(300, 15 * Math.pow(520 / Math.max(depthAt(x), 4), 0.6));
  const ampC = (x) => ampRaw(x) * (1 + 2.1 * smooth((x - 2430) / 260));
  const zbot = (x) => zg0(x) - 170 - 18 * Math.sin(x * 0.004);
  const boreAt = (xc) => smooth((xc - 2250) / 330);

  function wave(x, k) { // surface height at x for normalised time k (0..1 of the mechanism)
    const t = k * 9;
    let eta = 1.8 * Math.sin(x * 0.03 - t * 3) + 1.2 * Math.sin(x * 0.071 + t * 2.2);
    const kq = 0.1;
    if (k < kq) return eta;
    // the first lift right over the moved seafloor, then a landward pair (trough in front, crest behind) and a seaward one
    const born = smooth((k - kq) / 0.05), fade0 = 1 - smooth((k - kq - 0.04) / 0.08);
    eta += born * fade0 * upl(x) * 0.9;
    const p = clamp((k - 0.14) / 0.83), xc = crestAt(p), go = smooth((k - kq - 0.03) / 0.06);
    const w = width(xc), near = smooth((xc - 1700) / 900), gap = lerp(440, 300, near), wt = lerp(380, 330, near), xt = xc + gap;
    const Ac = ampC(xc) * go, At = Math.min(130, 1.4 * ampRaw(xc)) * go;
    const steep = smooth((xc - 2420) / 220), wf = w * (0.75 - 0.35 * steep), wb = w * 1.2;
    const dx = x - xc, bore = boreAt(xc);
    const swell = Ac * Math.exp(-((dx / (dx > 0 ? wf : wb)) ** 2));
    // NOAA: near the shore it looks like a fast-rising flood or a wall of water (a bore), not a breaking wind wave
    const wfr = lerp(70, 15, bore), behind = Math.max(0, -dx), step = 1 / (1 + Math.exp(dx / wfr));
    const raised = 0.95 * Ac * step * Math.exp(-((behind / 1150) ** 2)) + (dx < 0 ? 5 * Math.sin(x * 0.09 + t * 7) * Math.exp(-behind / 420) * step : 0);
    eta += (1 - bore) * swell + bore * raised;
    eta -= At * Math.exp(-(((x - xt) / wt) ** 2));
    const xs = 760 - (xc - 760) * 0.9;
    eta += 0.6 * ampRaw(760) * go * (1 - smooth((k - 0.2) / 0.2)) * Math.exp(-(((x - xs) / 360) ** 2));
    return eta;
  }
  // the block's camera: scale, world x at screen centre, screen y of sea level, vertical exaggeration, the top strip's offset
  const SECV = (k) => {
    const a = smooth((k - 0.4) / 0.26), b = smooth((k - 0.66) / 0.2), c = smooth((k - 0.88) / 0.12);
    return {
      s: lerp(lerp(lerp(0.3, 0.6, a), 1.0, b), 1.06, c),
      cx: lerp(lerp(lerp(1650, 2250, a), 2640, b), 2700, c),
      sy: lerp(lerp(860, 960, a), 1030, b),
      ve: lerp(lerp(2.5, 1.6, a), 1.0, b),
      off: [lerp(lerp(22, 30, a), 40, b), lerp(lerp(-64, -84, a), -108, b)],
    };
  };

  const SEC = {};
  function tideSection(L, o = {}) {
    const id = o.id || "ts";
    put(L.sky, `<rect x="-600" y="-600" width="2400" height="3200" fill="url(#tmSecSky)"/>
      <circle cx="830" cy="300" r="260" fill="url(#tmSun)"/><circle cx="830" cy="300" r="46" fill="#fffbe8" opacity=".95"/>
      ${[[180, 270, 1.1], [430, 190, 0.8], [700, 470, 0.7], [960, 430, 0.9], [300, 480, 0.6]].map(([x, y, s]) => `<g transform="translate(${x},${y}) scale(${s})" opacity=".9">${[[-60, 8, 58], [-10, -14, 70], [48, 4, 56], [96, 14, 40]].map(([cx, cy, r]) => `<ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${r * 0.72}" fill="url(#tmCloud)"/>`).join("")}</g>`).join("")}
      <rect x="-600" y="1260" width="2400" height="1200" fill="url(#tmFloor)"/>`);
    put(L.far, `<g opacity=".45">${[[40, 1.0], [200, 0.75], [960, 1.1], [1060, 0.7]].map(([x, s]) => `<path d="M${x - 70 * s},640 C${x - 60 * s},500 ${x - 40 * s},460 ${x - 20 * s},440 C${x},410 ${x + 30 * s},420 ${x + 40 * s},480 C${x + 55 * s},540 ${x + 66 * s},600 ${x + 75 * s},640Z" fill="#8fb8b0"/>`).join("")}</g>`);
    put(L.set, `<g id="${id}-sec"><defs><clipPath id="${id}-wclip"><path id="${id}-wclipP" d="M0,0"/></clipPath>
        <linearGradient id="${id}-gW" gradientUnits="userSpaceOnUse" x1="0" y1="1000" x2="0" y2="1300"><stop offset="0" stop-color="#57d0dc"/><stop offset=".3" stop-color="#2496c0"/><stop offset="1" stop-color="#0b3a6c"/></linearGradient>
        <linearGradient id="${id}-gS" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1000" y2="0"><stop offset="0" stop-color="#3fc6d0" stop-opacity="0"/><stop offset="1" stop-color="#6ee6da" stop-opacity=".75"/></linearGradient>
        <linearGradient id="${id}-gR" gradientUnits="userSpaceOnUse" x1="0" y1="1000" x2="0" y2="1600"><stop offset="0" stop-color="#b8905e"/><stop offset="1" stop-color="#5e4230"/></linearGradient>
        <linearGradient id="${id}-gC" gradientUnits="userSpaceOnUse" x1="0" y1="700" x2="0" y2="1200"><stop offset="0" stop-color="#2a8f94"/><stop offset=".55" stop-color="#3aa9a8"/><stop offset="1" stop-color="#5cc6c0" stop-opacity="0"/></linearGradient></defs>
      <g id="${id}-dyn"></g></g>`);
    put(L.light, `<g id="${id}-coins"></g>`);
    SEC[id] = { id, g: document.getElementById(`${id}-dyn`), coins: document.getElementById(`${id}-coins`), labels: {} };
    sectionFrame(SEC[id], 0);
  }

  // coin icons (box ±40)
  const JET = `<g transform="translate(0,4)"><path d="M-46,4 C-30,-8 20,-10 40,-6 C50,-4 52,4 40,7 C20,11 -24,12 -40,10Z" fill="#f6fbff" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/>
    <path d="M-6,-2 L-26,-30 L-14,-30 L18,-3Z" fill="#3d8fd0" stroke="#140e0a" stroke-width="3.5" stroke-linejoin="round"/><path d="M-4,8 L-22,30 L-10,30 L16,8Z" fill="#2f78b8" stroke="#140e0a" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M-40,2 L-48,-20 L-38,-20 L-28,0Z" fill="#3d8fd0" stroke="#140e0a" stroke-width="3.5" stroke-linejoin="round"/>
    ${[-18, -9, 0, 9, 18].map((x) => `<circle cx="${x}" cy="-1" r="2.6" fill="#2a5a88"/>`).join("")}<path d="M34,-4 C38,-3 42,-1 43,2" stroke="#2a5a88" stroke-width="3" fill="none" stroke-linecap="round"/></g>`;
  const CAR = `<g transform="translate(0,6)"><path d="M-44,10 L-44,-6 L-24,-8 L-14,-24 L14,-24 L24,-8 L44,-4 L46,10Z" fill="#ff7a4a" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/>
    <path d="M-10,-20 L-18,-8 L-2,-8 L-2,-20Z M4,-20 L4,-8 L20,-8 L12,-20Z" fill="#cfefff" stroke="#140e0a" stroke-width="3" stroke-linejoin="round"/>
    <path d="M-38,0 H40" stroke="#ffd0b8" stroke-width="3" opacity=".8"/>${[-26, 26].map((x) => `<circle cx="${x}" cy="12" r="11" fill="#2a2a2a" stroke="#140e0a" stroke-width="3.5"/><circle cx="${x}" cy="12" r="4.5" fill="#c8c8c8"/>`).join("")}</g>`;
  const RUN = `<g transform="translate(-2,0)"><circle cx="10" cy="-30" r="10" fill="#e3ad84" stroke="#140e0a" stroke-width="3.5"/>
    <path d="M6,-18 L-4,6" stroke="#ff5a3a" stroke-width="13" stroke-linecap="round"/>
    <path d="M2,-12 L20,-4 L30,-14 M2,-12 L-14,-6 L-24,-16" stroke="#140e0a" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M-4,6 L10,20 L4,36 M-4,6 L-16,20 L-32,22" stroke="#2a4a8a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M-36,-10 H-50 M-34,2 H-52 M-30,14 H-44" stroke="#140e0a" stroke-width="3.5" stroke-linecap="round" opacity=".6"/></g>`;
  const coin = (icon, grad, slab) => `<ellipse cx="0" cy="74" rx="52" ry="12" fill="url(#tmSoft)"/>
    <circle cx="0" cy="10" r="58" fill="${slab}" stroke="#140e0a" stroke-width="4.5"/><circle r="58" fill="url(#${grad})" stroke="#140e0a" stroke-width="4.5"/>
    <circle r="47" fill="none" stroke="#ffffff" stroke-width="3" opacity=".55"/><path d="M-38,-26 A46,46 0 0 1 -6,-46" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity=".75"/>${icon}`;
  // label text: "|" breaks the line (the texts themselves contain "/"); width from the visible characters
  const vis = (t) => t.replace(/[ัิ-ฺ็-๎]/g, "").length;
  const labW = (txt) => Math.max(...txt.split("|").map(vis)) * 17.2 + 64;
  const label = (txt) => {
    const lines = txt.split("|"), w = labW(txt), h = 26 + 40 * lines.length;
    return `<g transform="translate(0,${f1(96 + h / 2)})">${pill(w, h, { stroke: "#140e0a", r: 30 })}${lines.map((l, i) => `<text y="${f1(12 + (i - (lines.length - 1) / 2) * 40)}" text-anchor="middle" font-family="Kanit" font-weight="800" font-size="31" fill="${i ? "#ffd23a" : "#fff6e8"}">${l}</text>`).join("")}</g>`;
  };
  const DEF = { jet: "กลางทะเล: เร็วได้ถึง 950 กม./ชม.|พอๆ กับเครื่องบินเจ็ต", car: "ใกล้ฝั่ง: ราว 40 กม./ชม.", run: "ยังเร็วกว่าคนวิ่ง", drawback: "ท้องคลื่นถึงฝั่งก่อน…|น้ำทะเลลดลงกะทันหัน" };
  const XCAR = 2150, KCAR = (() => { for (let q = 0.14; q < 1; q += 0.001) if (crestAt((q - 0.14) / 0.83) >= XCAR) return q; return 1; })(), KRUN = 0.9;

  function sectionFrame(inst, k) {
    const V = SECV(k), s = V.s, ve = V.ve, shake = k > 0.1 && k < 0.2 ? (1 - (k - 0.1) / 0.1) * 9 : 0;
    const jx = shake * Math.sin(k * 900), jy = shake * Math.cos(k * 700);
    const X = (x) => 540 + (x - V.cx) * s + jx, Y = (z) => V.sy - z * s * ve + jy, [ox, oy] = V.off;
    const uk = smooth((k - 0.1) / 0.04), zg = (x) => zg0(x) + upl(x) * uk;
    const xc = crestAt(clamp((k - 0.14) / 0.83)), bore = k > 0.14 ? boreAt(xc) : 0;
    const out = [], step = 6, xs = []; for (let x = 0; x <= SX1; x += step) xs.push(x);
    const eta = xs.map((x) => wave(x, k)), gnd = xs.map(zg), wet = xs.map((_, i) => eta[i] > gnd[i] + 0.5);
    const topZ = xs.map((_, i) => (wet[i] ? eta[i] : gnd[i])), bot = xs.map(zbot);
    const F0 = (i) => [X(xs[i]), Y(topZ[i])], B0 = (i, f = 1) => { const p = F0(i); return [p[0] + ox * f, p[1] + oy * f]; };
    const n = xs.length;
    // soft shadow of the block on the floor
    out.push(`<ellipse cx="${f1(X(V.cx) + ox * 0.5)}" cy="${f1(Math.max(...bot.map((z, i) => Y(z))) + 34)}" rx="${f1(Math.min(1300, SX1 * s * 0.5))}" ry="${f1(26 + 40 * s)}" fill="url(#tmSoft)" opacity=".5"/>`);
    // ---- the top strip: sea surface, exposed seabed, beach, land (shaded by slope, bucketed) ----
    const qW = Array(7).fill(""), qG = Array(7).fill(""), qE = Array(5).fill(""), qT = Array(7).fill("");
    for (let i = 0; i + 1 < n; i++) {
      const a = F0(i), b = F0(i + 1), c = B0(i + 1), d = B0(i), quad = `M${f1(a[0])},${f1(a[1])}L${f1(b[0])},${f1(b[1])}L${f1(c[0])},${f1(c[1])}L${f1(d[0])},${f1(d[1])}Z`;
      const slope = ((topZ[i + 1] - topZ[i]) / step) * ve;
      if (wet[i] && wet[i + 1] && topZ[i] > 12 && bore > 0.05) qT[clamp(Math.round(3 - slope * 3 + (Math.sin(xs[i] * 0.11 + k * 60) + 0.6 * Math.sin(xs[i] * 0.047 - k * 40) > 1.1 ? -2 : 0)), 0, 6)] += quad;   // the raised, churning water
      else if (wet[i] && wet[i + 1]) qW[clamp(Math.round(3 - slope * 3 + clamp((topZ[i] - 15) / 50) * 4), 0, 6)] += quad;
      else if (gnd[i] < 1.5 && !wet[i]) qE[clamp(Math.round(2 - slope * 4), 0, 4)] += quad;
      else qG[clamp(Math.round(3 - slope * 3), 0, 6)] += quad;
    }
    const wc = ["#d8fbfa", "#a8eef0", "#7adbe6", "#55c6de", "#3aaed4", "#2b92c0", "#1f76a4"], gc = ["#fff4d0", "#f8e6b0", "#eed494", "#ddbf7a", "#c8a866", "#ae8e56", "#907448"], ec = ["#a89474", "#93805e", "#7e6c50", "#6a5a44", "#584a38"];
    qG.forEach((d, j) => d && out.push(`<path d="${d}" fill="${gc[j]}" stroke="${gc[j]}" stroke-width=".7"/>`));
    qE.forEach((d, j) => d && out.push(`<path d="${d}" fill="${ec[j]}" stroke="${ec[j]}" stroke-width=".7"/>`));
    qW.forEach((d, j) => d && out.push(`<path d="${d}" fill="${wc[j]}" stroke="${wc[j]}" stroke-width=".7"/>`));
    const tc = ["#f2fffc", "#c8f1ea", "#9be0d6", "#74ccc4", "#58b6b2", "#46a0a0", "#378a8c"];
    qT.forEach((d, j) => d && out.push(`<path d="${d}" fill="${tc[j]}" stroke="${tc[j]}" stroke-width=".7"/>`));
    // grass on the land part of the strip, a sheen on the mud, sparkles on the water
    let grass = "", sheen = "", spark = "";
    for (let i = 0; i < n; i += 2) {
      const x = xs[i];
      if (!wet[i] && gnd[i] > 15 && x > 2900) { [0.25, 0.6, 0.9].forEach((f) => { const p = B0(i, f); grass += `M${f1(p[0])},${f1(p[1])}l${f1(-3 * s)},${f1(-9 * s)}M${f1(p[0] + 4 * s)},${f1(p[1])}l${f1(2 * s)},${f1(-11 * s)}`; }); }
      if (!wet[i] && gnd[i] < 0 && i % 4 === 0) { [0.3, 0.7].forEach((f, m) => { if (Math.sin(x * 0.05 + m * 2) > 0.2) { const p = B0(i, f); sheen += `M${f1(p[0] - 7 * s)},${f1(p[1])}H${f1(p[0] + 11 * s)}`; } }); }
      if (wet[i] && i % 6 === 0) { [0.2, 0.5, 0.8].forEach((f, m) => { if (Math.sin(x * 0.021 + m * 1.9 + k * 40) > 0.75) { const p = B0(i, f); spark += `M${f1(p[0] - 9 * s)},${f1(p[1])}H${f1(p[0] + 9 * s)}`; } }); }
    }
    if (grass) out.push(`<path d="${grass}" stroke="#5a9a3a" stroke-width="${f1(clamp(2.6 * s, 1, 3))}" stroke-linecap="round"/>`);
    if (sheen) out.push(`<path d="${sheen}" stroke="#eef6f2" stroke-width="${f1(clamp(3 * s, 1, 3))}" stroke-linecap="round" opacity=".5"/>`);
    if (spark) out.push(`<path d="${spark}" stroke="#ffffff" stroke-width="${f1(clamp(3.4 * s, 1.2, 3.6))}" stroke-linecap="round" opacity=".75"/>`);
    // the water's edge on the strip
    let edge = "";
    for (let i = 0; i + 1 < n; i++) if (wet[i] !== wet[i + 1]) { const a = F0(wet[i] ? i : i + 1); edge += `M${f1(a[0])},${f1(a[1])}l${f1(ox)},${f1(oy)}`; }
    if (edge) out.push(`<path d="${edge}" stroke="#ffffff" stroke-width="${f1(clamp(10 * s, 3, 11))}" opacity=".9" stroke-linecap="round"/>`);
    // quake rings on the strip right above the fault
    if (k > 0.1 && k < 0.34) { const kk = (k - 0.1) / 0.24, c = B0(Math.round(720 / step), 0.5); [0, 0.25, 0.5].forEach((d) => { const q = clamp(kk - d); if (q <= 0 || q >= 1) return; out.push(`<ellipse cx="${f1(c[0])}" cy="${f1(c[1])}" rx="${f1(30 + 260 * q * s)}" ry="${f1((30 + 260 * q * s) * 0.18)}" fill="none" stroke="#fff6d8" stroke-width="3" opacity="${f1(1 - q)}"/>`); }); }

    // ---- standing on the strip, far to near ----
    const objs = [];
    const onTop = (x, f) => { const i = clamp(Math.round(x / step), 0, n - 1); return [X(x) + ox * f, Y(topZ[i]) + oy * f, i]; };
    const palm = (x, f, h, lean) => { const [px, py] = onTop(x, f), sc = 1.25 * s * h * (1 - 0.15 * f); return [f, `<g transform="translate(${f1(px)},${f1(py)}) scale(${f1(sc)})"><ellipse cx="14" cy="2" rx="38" ry="8" fill="#4a3a20" opacity=".25"/><path d="M-4,0 C${lean},-60 ${lean * 1.6},-120 ${lean * 2.2},-170" stroke="#7a5a36" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M-4,0 C${lean},-60 ${lean * 1.6},-120 ${lean * 2.2},-170" stroke="#a07a4a" stroke-width="5" fill="none" stroke-linecap="round" stroke-dasharray="4 7"/>${[-150, -110, -60, -20, 20, 60, 110, 150].map((a) => `<path d="M${lean * 2.2},-170 q${f1(50 * Math.cos(((a - 90) * PI) / 180))},${f1(-30 + 40 * Math.sin(((a - 90) * PI) / 180))} ${f1(96 * Math.cos(((a - 90) * PI) / 180))},${f1(30 + 60 * Math.sin(((a - 90) * PI) / 180))}" stroke="${a % 40 ? "#2f8a3e" : "#46a64e"}" stroke-width="12" fill="none" stroke-linecap="round"/>`).join("")}</g>`]; };
    const hut = (x, f, w, hh, roof) => { const [px, py] = onTop(x, f), sc = 0.9 * s * (1 - 0.15 * f); return [f, `<g transform="translate(${f1(px)},${f1(py)}) scale(${f1(sc)})"><ellipse cx="10" cy="4" rx="${w * 0.75}" ry="9" fill="#3a2a10" opacity=".22"/><path d="M${-w / 2},0 v${-hh} h${w} v${hh}Z" fill="#d8aa70" stroke="#3a2a1a" stroke-width="4"/><path d="M${w / 2},0 v${-hh} l26,-16 v${hh}Z" fill="#a47a4a" stroke="#3a2a1a" stroke-width="4" stroke-linejoin="round"/><path d="M${-w / 2 - 14},${-hh} L${-w / 2 + 12},${-hh - 46} H${w / 2 + 40} L${w / 2 + 26},${-hh - 16} Z" fill="${roof}" stroke="#3a2a1a" stroke-width="4" stroke-linejoin="round"/><path d="M${-w / 2 - 14},${-hh} H${w / 2 + 26}" stroke="#3a2a1a" stroke-width="4"/><rect x="${-w / 2 + 14}" y="${-hh + 16}" width="22" height="20" fill="#3a5a6a" stroke="#3a2a1a" stroke-width="3"/><rect x="${w / 2 - 34}" y="${-hh + 22}" width="18" height="${hh - 22}" fill="#6a4a2a" stroke="#3a2a1a" stroke-width="3"/></g>`]; };
    objs.push(palm(2905, 0.85, 0.9, 10), hut(2975, 0.7, 90, 64, "#d8503a"), palm(3030, 0.5, 1.05, -8), hut(2935, 0.3, 80, 58, "#3a8ac8"), palm(2990, 0.1, 0.95, 12), palm(3140, 0.75, 0.85, 6), palm(3220, 0.4, 0.8, -6));
    { const [px, py] = onTop(3165, 0.3), sc = 0.75 * s; objs.push([0.3, `<g transform="translate(${f1(px)},${f1(py)}) scale(${f1(sc)})"><path d="M0,0V-110" stroke="#5a5a5a" stroke-width="8"/><g transform="translate(0,-150)"><rect x="-62" y="-44" width="124" height="88" rx="8" fill="#1f5fae" stroke="#140e0a" stroke-width="4"/><path d="M-50,10 c10,-18 22,-26 34,-10 c-14,-4 -20,8 -14,22 h-20Z" fill="#fff"/><circle cx="20" cy="-18" r="7" fill="#fff"/><path d="M18,-10 L12,8 L22,20 M12,8 L0,16 M16,-4 L30,2 M16,-4 L4,-8" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M38,30 H54 M48,24 L56,30 L48,36" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>`]); }
    // a longtail boat: floats, or lies tilted on the mud once the sea has gone
    { const bx = 2655, f = 0.55, [px, py, i] = onTop(bx, f), floating = wet[i], tilt = floating ? 3 * Math.sin(k * 40) : 13, bob = floating ? 2 * Math.sin(k * 50) : 0, sc = 0.95 * s * (1 - 0.15 * f);
      objs.push([f, `<g transform="translate(${f1(px)},${f1(py - (floating ? 6 * sc : 0) + bob)}) rotate(${f1(tilt)}) scale(${f1(sc)})"><path d="M-110,-6 C-60,10 60,12 96,-4 L116,-40 C80,-20 -50,-18 -120,-30Z" fill="#c25a2a" stroke="#2a160a" stroke-width="5" stroke-linejoin="round"/><path d="M-116,-26 C-50,-14 70,-16 108,-32" stroke="#f2d27a" stroke-width="6" fill="none"/><path d="M116,-40 l10,-26" stroke="#2a160a" stroke-width="6" stroke-linecap="round"/><path d="M118,-54 l18,-6 l-6,14 l14,4 l-20,6" fill="#ff4a8a" stroke="#2a160a" stroke-width="3"/><path d="M-120,-30 L-150,-6" stroke="#6a6a6a" stroke-width="5"/><path d="M-60,-24 h70 v-26 h-70z" fill="#3a6aa8" stroke="#2a160a" stroke-width="4"/></g>`]); }
    // fish flopping on the exposed seabed
    [[2470, 0.3, 1], [2520, 0.62, 2], [2590, 0.4, 3], [2640, 0.78, 4], [2690, 0.22, 5], [2730, 0.55, 6], [2610, 0.12, 7], [2555, 0.85, 8]].forEach(([fx, f, ph]) => {
      const [px, py, i] = onTop(fx, f); if (wet[i] || gnd[i] > 1) return;
      const flop = 28 * Math.sin(k * 140 + ph * 2), hop = -Math.abs(Math.sin(k * 70 + ph)) * 9, sc = 0.72 * s * (1 - 0.15 * f);
      objs.push([f, `<g transform="translate(${f1(px)},${f1(py + hop * sc)}) rotate(${f1(flop)}) scale(${f1(sc)})"><ellipse cx="0" cy="-6" rx="20" ry="8" fill="#a8d0e0" stroke="#1a2a36" stroke-width="3"/><path d="M18,-6 l12,-9 v18z" fill="#7fa8bc" stroke="#1a2a36" stroke-width="3" stroke-linejoin="round"/><circle cx="-12" cy="-8" r="2.2" fill="#1a2a36"/><path d="M-6,-12 q6,-5 12,0" stroke="#e8fbff" stroke-width="2" fill="none"/></g>`]);
    });
    // the person: walks out onto the mud (k .80–.92), then turns and runs (k > .92)
    let person = null;
    if (k > 0.78) {
      const walkK = clamp((k - 0.8) / 0.12), runK = clamp((k - 0.92) / 0.08), x = 2800 - 180 * smooth(walkK) + 150 * runK, f = 0.42;
      const [px, py] = onTop(x, f), sc = 0.85 * s * (1 - 0.15 * f), running = runK > 0, sw = running ? Math.sin(k * 260) : Math.sin(k * 120), flip = running ? 1 : -1;
      person = [px, py, sc];
      objs.push([f, `<g transform="translate(${f1(px)},${f1(py)}) scale(${f1(sc * flip)},${f1(sc)})"><ellipse cx="0" cy="2" rx="18" ry="5" fill="#000" opacity=".2"/>
        <path d="M0,-34 L${f1(-10 * sw)},-2 M0,-34 L${f1(10 * sw)},-2" stroke="#2a3a5a" stroke-width="7" stroke-linecap="round"/>
        <path d="M0,-62 L0,-34" stroke="#ff8a3a" stroke-width="15" stroke-linecap="round"/>
        <path d="M0,-58 L${f1(12 * sw + (running ? 8 : 0))},-40 M0,-58 L${f1(-12 * sw)},-40" stroke="#e3ad84" stroke-width="5" stroke-linecap="round"/>
        <circle cx="${running ? 4 : 0}" cy="-74" r="10" fill="#e3ad84" stroke="#2a1a10" stroke-width="2.5"/><path d="M${running ? -6 : -10},-80 q10,-12 20,0" fill="#2a1a10"/></g>`]);
    }
    objs.sort((a, b) => b[0] - a[0]);
    out.push(objs.map((x) => x[1]).join(""));

    // ---- the cut face: the ground (soil on land, wet sand under the sea, rock layers), the fault, the water body ----
    let rock = `M${f1(X(0))},${f1(Y(bot[0]))}`;
    for (let i = 0; i < n; i++) rock += `L${f1(X(xs[i]))},${f1(Y(gnd[i]))}`;
    for (let i = n - 1; i >= 0; i--) rock += `L${f1(X(xs[i]))},${f1(Y(bot[i]))}`;
    out.push(`<path d="${rock}Z" fill="url(#${inst.id}-gR)" stroke="#2a1a10" stroke-width="3" stroke-linejoin="round"/>`);
    let layers = "";
    for (let m = 1; m <= 5; m++) { let d = "", pen = false; for (let i = 0; i < n; i += 2) { const z = gnd[i] - m * 28 - 6 * Math.sin(xs[i] * 0.006 + m); if (z < bot[i] + 6) { pen = false; continue; } d += (pen ? "L" : "M") + f1(X(xs[i])) + "," + f1(Y(z)); pen = true; } layers += `<path d="${d}" stroke="${m % 2 ? "#7a5a3a" : "#e8c894"}" stroke-width="${f1(clamp(5 * s, 1.5, 5))}" fill="none" opacity="${m % 2 ? 0.35 : 0.28}"/>`; }
    out.push(layers);
    let topsoil = "";
    for (let i = 0; i < n; i++) topsoil += (i ? "L" : "M") + f1(X(xs[i])) + "," + f1(Y(gnd[i]) + 4);
    out.push(`<path d="${topsoil}" stroke="#e9cf96" stroke-width="${f1(clamp(9 * s, 2.5, 10))}" fill="none" opacity=".75"/>`);
    // the fault, glowing at the jolt
    const glow = k > 0.1 ? clamp(1 - (k - 0.1) / 0.25) : 0, iF = Math.round(FAULT / step);
    const fa = [X(FAULT), Y(gnd[iF])], fb = [X(FAULT - 70), Y(bot[iF])], fm = [(fa[0] + fb[0]) / 2 + 8, (fa[1] + fb[1]) / 2];
    out.push(`<path d="M${f1(fa[0])},${f1(fa[1])}L${f1(fm[0])},${f1(fm[1])}L${f1(fb[0])},${f1(fb[1])}" stroke="#2a1006" stroke-width="${f1(clamp(8 * s, 2.5, 7))}" fill="none" stroke-linejoin="round"/>`);
    if (glow > 0) out.push(`<path d="M${f1(fa[0])},${f1(fa[1])}L${f1(fm[0])},${f1(fm[1])}L${f1(fb[0])},${f1(fb[1])}" stroke="#ff8a3a" stroke-width="${f1(clamp(22 * s, 6, 18))}" fill="none" opacity="${f1(0.6 * glow)}"/>`);
    // the water on the cut face
    let wb = "";
    for (let i = 0; i < n;) {
      if (!wet[i]) { i++; continue; }
      let j = i; while (j + 1 < n && wet[j + 1]) j++;
      let d = `M${f1(X(xs[i]))},${f1(Y(gnd[i]))}`;
      for (let q = i; q <= j; q++) d += `L${f1(X(xs[q]))},${f1(Y(eta[q]))}`;
      for (let q = j; q >= i; q--) d += `L${f1(X(xs[q]))},${f1(Y(gnd[q]))}`;
      wb += d + "Z"; i = j + 1;
    }
    const setA = (sfx, a) => { const e = document.getElementById(`${inst.id}-${sfx}`); if (e) Object.entries(a).forEach(([kk, v]) => e.setAttribute(kk, v)); };
    setA("gW", { y1: f1(Y(20)), y2: f1(Y(-540)) }); setA("gS", { x1: f1(X(1750)), x2: f1(X(2750)) }); setA("gR", { y1: f1(Y(0)), y2: f1(Y(-700)) }); setA("wclipP", { d: wb || "M0,0" });
    if (wb) {
      out.push(`<path d="${wb}" fill="url(#${inst.id}-gW)"/><path d="${wb}" fill="url(#${inst.id}-gS)"/>`);
      let rays = "";
      for (let m = 0; m < 10; m++) { const x0 = 200 + m * 320 + 60 * Math.sin(k * 6 + m), w = 70 + 30 * Math.sin(m * 1.7); rays += `<path d="M${f1(X(x0))},${f1(Y(40))}L${f1(X(x0 + w))},${f1(Y(40))}L${f1(X(x0 + w - 150))},${f1(Y(-560))}L${f1(X(x0 - 150))},${f1(Y(-560))}Z" fill="url(#tmRay)"/>`; }
      out.push(`<g clip-path="url(#${inst.id}-wclip)">${rays}</g>`);
      let surf = ""; for (let q = 0; q < n; q++) if (wet[q]) surf += (q && wet[q - 1] ? "L" : "M") + f1(X(xs[q])) + "," + f1(Y(eta[q]));
      // the part of the wave standing above sea level: a darker body with foam streaks
      let crest = "";
      for (let i = 0; i < n;) {
        if (!(wet[i] && eta[i] > 6)) { i++; continue; }
        let j = i; while (j + 1 < n && wet[j + 1] && eta[j + 1] > 6) j++;
        if (j - i > 2) { let d = `M${f1(X(xs[i]))},${f1(Y(Math.max(0, gnd[i])))}`; for (let q = i; q <= j; q++) d += `L${f1(X(xs[q]))},${f1(Y(eta[q]))}`; for (let q = j; q >= i; q--) d += `L${f1(X(xs[q]))},${f1(Y(Math.max(0, gnd[q])))}`; crest += d + "Z"; }
        i = j + 1;
      }
      if (crest) {
        setA("gC", { y1: f1(Y(260)), y2: f1(Y(0)) });
        // churning foam: short ragged dashes, thickest near the front, reshuffled every few frames
        const rf = mk(Math.floor(k * 420) + 7);
        let streaks = "";
        for (let m = 0; m < 70 * bore; m++) {
          const back = Math.pow(rf(), 1.8) * 420, x0 = xc - back, ez = wave(x0, k); if (ez < 8) continue;
          const z0 = ez * (0.25 + 0.7 * rf()), L = (14 + rf() * 34) * s, w1 = (rf() - 0.5) * 10 * s;
          streaks += `M${f1(X(x0))},${f1(Y(z0))}q${f1(L * 0.5)},${f1(w1)} ${f1(L)},${f1(rf() * 4 - 2)}`;
        }
        out.push(`<path d="${crest}" fill="url(#${inst.id}-gC)" opacity="${f1(clamp((ampC(xc) - 20) / 80))}"/><g clip-path="url(#${inst.id}-wclip)"><path d="${streaks}" stroke="#f2fffd" stroke-width="${f1(clamp(5 * s, 1.4, 5.5))}" fill="none" stroke-linecap="round" opacity=".7"/></g>`);
      }
      out.push(`<path d="${surf}" stroke="#effeff" stroke-width="${f1(clamp(6 * s, 2, 6))}" fill="none" opacity=".95" stroke-linejoin="round"/><path d="${wb}" fill="none" stroke="#0c2a44" stroke-width="2.5" opacity=".5"/>`);
    }
    // the bore's front: a ragged, churning wall of white and teal foam across the cut face and the strip, spray, bits of debris
    if (bore > 0.05) {
      const rb = mk(Math.floor(k * 420) + 3), wfr = lerp(70, 15, bore);
      // where the front stands: the surface drops from the raised water to the sea ahead
      const fx = (z) => { let best = xc; for (let x = xc - 4 * wfr; x <= xc + 4 * wfr; x += 2) { if (wave(x, k) <= z) { best = x; break; } } return best; };
      const top = wave(xc - 3 * wfr, k);
      let blobs = "", teal = "", spray = "", debris = "";
      // on the cut face: stacked blobs up the wall, teal ones behind for depth
      // spilling curtains: ragged white strips running down the face from the top
      let curt = "";
      for (let m = 0; m < 5 * bore; m++) {
        const z0 = top * (0.92 + rb() * 0.1), z1 = top * (0.15 + rb() * 0.35), w = (6 + rb() * 10) * s; let d = "", e = "";
        for (let q = 0; q <= 8; q++) { const z = z0 + (z1 - z0) * (q / 8), xx = X(fx(z) + 2) + (rb() - 0.5) * 6 * s; d += (q ? "L" : "M") + f1(xx - w * (0.6 + rb() * 0.6)) + "," + f1(Y(z)); e = `L${f1(xx + w * (0.4 + rb() * 0.5))},${f1(Y(z))}` + e; }
        curt += d + e + "Z";
      }
      blobs += `<path d="${curt}" fill="#f6fffd" opacity=".9"/>`;
      for (let m = 0; m < 60 * bore; m++) {
        const zf = (rb() < 0.5 ? 0.7 + 0.35 * rb() : rb()) * top, x = fx(zf) + (rb() - 0.6) * 30, r = (5 + Math.pow(rb(), 1.5) * 19) * s, j = (rb() - 0.5) * 8 * s;
        const c = [X(x) + j, Y(zf) + j];
        if (rb() < 0.3) teal += `<circle cx="${f1(c[0] - 6 * s)}" cy="${f1(c[1])}" r="${f1(r * 1.1)}" fill="#7fd6cf"/>`;
        else blobs += `<circle cx="${f1(c[0])}" cy="${f1(c[1])}" r="${f1(r)}" fill="#ffffff" opacity="${f1(0.75 + rb() * 0.25)}"/>`;
      }
      // across the top strip: the front seen from above, a broken white band
      for (let m = 0; m < 30 * bore; m++) {
        const f = rb(), x = xc + (rb() - 0.55) * 40, ii = clamp(Math.round(x / step), 0, n - 1), r = (6 + rb() * 12) * s;
        const c = [X(x) + ox * f, Y(Math.max(topZ[ii], wave(x, k))) + oy * f];
        blobs += `<circle cx="${f1(c[0])}" cy="${f1(c[1])}" r="${f1(r)}" fill="#ffffff" opacity="${f1(0.7 + rb() * 0.3)}"/>`;
      }
      // spray thrown up and ahead of the wall
      for (let m = 0; m < 60 * bore; m++) {
        const f = rb(), x = xc + (rb() - 0.3) * 70, z = top * (0.6 + rb() * 0.6) + rb() * 30, c = [X(x) + ox * f, Y(z) + oy * f];
        spray += `<circle cx="${f1(c[0])}" cy="${f1(c[1])}" r="${f1((1.6 + rb() * 4.2) * clamp(s, 0.4, 1.2))}" fill="#ffffff" opacity="${f1(0.35 + rb() * 0.6)}"/>`;
      }
      // debris tumbling in the front: planks, a palm frond, a bucket, a tyre
      const DEB = [
        (sc) => `<rect x="-26" y="-5" width="52" height="10" rx="3" fill="#a0703e" stroke="#3a2410" stroke-width="3"/><path d="M-16,-1H8" stroke="#c89a62" stroke-width="2"/>`,
        (sc) => `<rect x="-20" y="-4" width="40" height="8" rx="2" fill="#8a6036" stroke="#3a2410" stroke-width="3"/>`,
        (sc) => `<path d="M-30,0 Q0,-10 30,-2" stroke="#3a7a32" stroke-width="5" fill="none"/>${[-20, -10, 0, 10, 20].map((x) => `<path d="M${x},${-4 + Math.abs(x) * 0.1} l-6,10 M${x},${-4 + Math.abs(x) * 0.1} l6,-10" stroke="#4e9a3e" stroke-width="3.5" stroke-linecap="round"/>`).join("")}`,
        (sc) => `<path d="M-11,-12 H11 L8,12 H-8Z" fill="#e2392c" stroke="#3a1008" stroke-width="3" stroke-linejoin="round"/><path d="M-11,-12 Q0,-22 11,-12" stroke="#3a1008" stroke-width="2.5" fill="none"/>`,
        (sc) => `<circle r="13" fill="#2a2a2a" stroke="#111" stroke-width="3"/><circle r="6" fill="#7fd6cf"/>`,
      ];
      DEB.forEach((dfn, m) => {
        const ph = m * 1.7, f = [0.25, 0.6, 0.4, 0.75, 0.15][m], zf = top * (0.2 + 0.6 * ((m * 0.37 + k * 3) % 1)), x = fx(zf) - (8 + m * 9), c = [X(x) + ox * f, Y(zf) + oy * f];
        debris += `<g transform="translate(${f1(c[0])},${f1(c[1])}) rotate(${f1((k * 900 + ph * 60) % 360)}) scale(${f1(clamp(s, 0.4, 1.2) * 0.9)})">${dfn()}</g>`;
      });
      out.push(`<g opacity="${f1(clamp(bore * 1.6))}">${teal}${debris}${blobs}${spray}</g>`);
    }
    // the block's ends (left: a plain cut, right: the hill's side face)
    const e0 = F0(0), e1 = F0(n - 1);
    out.push(`<path d="M${f1(e1[0])},${f1(e1[1])}l${f1(ox)},${f1(oy)}V${f1(Y(bot[n - 1]) + oy)}L${f1(e1[0])},${f1(Y(bot[n - 1]))}Z" fill="#6a4a30" stroke="#2a1a10" stroke-width="3" stroke-linejoin="round"/>
      <path d="M${f1(e0[0])},${f1(Y(bot[0]))}V${f1(e0[1])}l${f1(ox)},${f1(oy)}" stroke="#2a1a10" stroke-width="3" fill="none" stroke-linejoin="round"/>`);
    // the quake star at the fault on the cut face
    if (k > 0.1 && k < 0.36) {
      const kk = (k - 0.1) / 0.26, pp = backOut(kk / 0.35, 2.4) * (1 - smooth((kk - 0.7) / 0.3)), sq = 1 + 0.18 * Math.sin(k * 300), sc = clamp(s * 1.6, 0.5, 1) * pp;
      if (sc > 0.01) out.push(`<g transform="translate(${f1(fm[0])},${f1(fm[1])}) scale(${f1(sc)})"><circle r="120" fill="url(#tmBurst)"/><g transform="rotate(${f1(8 * Math.sin(k * 400))}) scale(${f1(sq)},${f1(2 - sq)})"><path d="${STAR}" transform="translate(0,7)" fill="#9a3a10" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/><path d="${STAR}" fill="url(#tmStar)" stroke="#140e0a" stroke-width="4" stroke-linejoin="round"/></g></g>`);
    }
    inst.g.innerHTML = out.join("");

    // ---- coins and the callout (screen space, constant size) ----
    const lab = { ...DEF, ...inst.labels }, coins = [];
    const crestTop = () => { let best = 1e9, bx = xc; for (let x = xc - 120; x <= xc + 60; x += 6) { const y = Y(wave(x, k)); if (y < best) { best = y; bx = x; } } return [X(bx) + ox * 0.5, best + oy * 0.5]; };
    const sx = (a) => clamp(a, 0, 1);
    const cxFit = (x, txt) => { const hw = Math.max(70, labW(txt) / 2 + 24); return clamp(x, hw, 1080 - hw); };
    if (k > 0.16 && k < KCAR + 0.02) {
      const [cx, cy] = crestTop(), fl = k < KCAR ? 1 : 1 - sx((k - KCAR) / 0.02), pop = backOut(sx((k - 0.16) / 0.03), 2.6);
      coins.push(`<g transform="translate(${f1(cxFit(cx, lab.jet))},${f1(clamp(cy - 270, 300, 1500))}) scale(${f1(fl * pop)},${f1(pop)})">${coin(JET, "tmCoinB", "#1f5a86")}${label(lab.jet)}</g>`);
    }
    if (k >= KCAR && k < KRUN + 0.02) {
      const [cx, cy] = crestTop(), fl = k < KCAR + 0.02 ? sx((k - KCAR) / 0.02) : k < KRUN ? 1 : 1 - sx((k - KRUN) / 0.02), sq = 1 + 0.06 * Math.sin(k * 90);
      coins.push(`<g transform="translate(${f1(cxFit(cx, lab.car))},${f1(clamp(cy - 250, 300, 1500))}) scale(${f1(fl * sq)},${f1(2 - sq)})">${coin(CAR, "tmCoinO", "#a85a10")}${label(lab.car)}</g>`);
    }
    if (k > 0.81 && k < 0.95) {
      const xa = 2660, ia = Math.round(xa / step), q = [X(xa) + ox * 0.5, Y(topZ[ia]) + oy * 0.5], a = sx((k - 0.81) / 0.03) * (1 - sx((k - 0.93) / 0.02)), bob = 6 * Math.sin(k * 60);
      const lines = lab.drawback.split("|"), w = labW(lab.drawback) + 30, h = 30 + 46 * lines.length, cx = cxFit(q[0] + 60, lab.drawback), top = q[1] + 150 + h / 2 + bob;
      coins.push(`<g opacity="${f1(a)}"><path d="M${f1(q[0])},${f1(q[1] + 6)}L${f1(cx - 40)},${f1(top - h / 2 - 4)}" stroke="#140e0a" stroke-width="4" stroke-dasharray="8 7"/><circle cx="${f1(q[0])}" cy="${f1(q[1] + 4)}" r="8" fill="#c0281e" stroke="#140e0a" stroke-width="3"/><g transform="translate(${f1(cx)},${f1(top)})">${pill(w, h, { face: "url(#tmFaceC)", slab: "#a8936a", hi: 0.7, r: 32 })}${lines.map((l, i) => `<text y="${f1(14 + (i - (lines.length - 1) / 2) * 46)}" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="38" fill="${i ? "#c0281e" : "#140e0a"}">${l}</text>`).join("")}</g></g>`);
    }
    if (k >= KRUN && person) {
      const [px, py] = person, pop = backOut(sx((k - KRUN) / 0.03), 2.6);
      const cx = cxFit(px + 110, lab.run), cy = clamp(py - 330, 300, 1500);
      coins.push(`<path d="M${f1(px)},${f1(py - 90 * s)}L${f1(cx)},${f1(cy + 60)}" stroke="#140e0a" stroke-width="4" stroke-dasharray="8 7" opacity="${f1(clamp(pop))}"/><g transform="translate(${f1(cx)},${f1(cy)}) scale(${f1(pop)})">${coin(RUN, "tmCoinR", "#8a2a1a")}${label(lab.run)}</g>`);
    }
    inst.coins.innerHTML = coins.join("");
  }

  function section(tl, id, t0, dur, o = {}) {
    const inst = SEC[id]; if (!inst) return;
    inst.labels = o.labels || {};
    const k0 = o.k0 ?? 0, k1 = o.k1 ?? 1, px = { k: k0 };
    tl.fromTo(px, { k: k0 }, { k: k1, duration: dur, ease: o.ease || "none", immediateRender: false, onUpdate: () => sectionFrame(inst, px.k) }, t0);
    sectionFrame(inst, k0);
  }

  Object.assign(Sets, { tideMap3d, tideSection });
  window.TideMap = { P, LL, HOME, play, section, data, frame, camAt };
})();
